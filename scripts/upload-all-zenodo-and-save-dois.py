#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Upload All Papers to Zenodo

Rebuilds all PDFs and uploads them to Zenodo, saving DOIs to config files.
By default, automatically publishes papers that pass validation.

Usage:
    python scripts/upload-all-zenodo-and-save-dois.py                # auto-publish after validation
    python scripts/upload-all-zenodo-and-save-dois.py --draft        # create drafts only (manual publish)
    python scripts/upload-all-zenodo-and-save-dois.py economics iab  # specific papers only
    python scripts/upload-all-zenodo-and-save-dois.py --verbose      # show full build output
    python scripts/upload-all-zenodo-and-save-dois.py --force-revalidate

Environment:
    ZENODO_TOKEN: API token from https://zenodo.org/account/settings/applications/
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import subprocess
import io
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Final

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

from lib.zenodo_client import ZenodoClient, upload_paper, get_zenodo_token
from lib.zenodo_client import get_record_id_from_doi
from lib.quarto_config_utils import (
    discover_pdf_work_items_sorted,
    get_newest_paper_source_mtime,
    get_paper_source_files,
    check_and_download_remote_pdf,
)
from lib.hash_utils import compute_sha256, compute_md5
from lib.pdf_validation_runner import run_pdf_validation
from lib.python_utils import get_preferred_python, load_project_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
PDF_VALIDATION_CACHE_PATH = PROJECT_ROOT / ".cache" / "pdf-validation-upload-cache.json"
VALIDATION_CACHE_VERSION = 5
PERFECTED_STATE_PATH = PROJECT_ROOT / ".cache" / "zenodo-perfect-upload-state.json"
PERFECTED_STATE_VERSION = 2
REPORT_ARCHIVE_DIR = PROJECT_ROOT / "ZENODO-UPLOAD-REPORTS"
VALIDATION_ERROR_REPORT_DIR = PROJECT_ROOT / "ZENODO-VALIDATION-ERRORS"
DEFAULT_LLM_BLOCKING_TYPES: Final[tuple[str, ...]] = (
    "LLM_UNRENDERED_CODE_OR_VARIABLE",
    "LLM_PLACEHOLDER_TEXT",
    "LLM_LEAKED_SOURCE_CODE",
    "LLM_CORRUPTED_OR_GARBLED_TEXT",
    "LLM_TRUNCATED_SENTENCE",
    "LLM_BROKEN_REFERENCE_ENTRY",
    "LLM_BROKEN_REFERENCE_LINK",
    "LLM_OTHER_HIGH_CONFIDENCE",
)
DEFAULT_LLM_WARNING_TYPES: Final[tuple[str, ...]] = ()

def _cache_key_for_pdf(pdf_path: Path) -> str:
    """Build a stable cache key for a PDF path."""
    return str(pdf_path.resolve()).replace("\\", "/").lower()


def _compute_pdf_signature(pdf_path: Path) -> dict:
    """Compute content-hash signature used for validation cache matching."""
    return {
        "sha256": compute_sha256(pdf_path),
    }


def _extract_record_file_checksum_md5(record: dict, target_filename: str) -> str | None:
    """Extract md5 checksum for a file from Zenodo records API response."""
    files = record.get("files", [])
    if not isinstance(files, list):
        return None

    for file_info in files:
        if not isinstance(file_info, dict):
            continue
        filename = (
            file_info.get("filename")
            or file_info.get("key")
            or file_info.get("name")
            or ""
        )
        if filename != target_filename:
            continue
        checksum = str(file_info.get("checksum", "")).strip()
        if checksum.startswith("md5:"):
            return checksum.removeprefix("md5:").strip().lower()
        return None

    return None


def _should_skip_upload_by_remote_checksum(
    client: ZenodoClient,
    quarto_config: dict,
    pdf_path: Path,
) -> tuple[bool, str]:
    """Return (skip, reason) if remote latest version has same PDF content."""
    metadata = quarto_config.get("metadata", {})
    if not isinstance(metadata, dict):
        return False, "No metadata section"

    existing_doi = str(metadata.get("doi", "")).strip()
    if not existing_doi:
        return False, "No existing DOI in config"

    record_id = get_record_id_from_doi(existing_doi)
    if not record_id:
        return False, f"Could not parse record id from DOI: {existing_doi}"

    try:
        record = client.get_record(record_id)
    except Exception as e:
        return False, f"Could not fetch record {record_id}: {e}"

    remote_md5 = _extract_record_file_checksum_md5(record, pdf_path.name)
    if not remote_md5:
        return False, f"No remote checksum found for {pdf_path.name}"

    local_md5 = compute_md5(pdf_path)
    if local_md5.lower() == remote_md5.lower():
        return True, f"Remote checksum matches local ({pdf_path.name})"
    return False, f"Remote checksum differs for {pdf_path.name}"


def _default_validation_cache() -> dict:
    return {"version": VALIDATION_CACHE_VERSION, "entries": {}}


def _load_validation_cache(cache_path: Path = PDF_VALIDATION_CACHE_PATH) -> dict:
    """Load PDF validation cache from disk."""
    if not cache_path.exists():
        return _default_validation_cache()
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                if data.get("version") != VALIDATION_CACHE_VERSION:
                    return _default_validation_cache()
                data.setdefault("version", VALIDATION_CACHE_VERSION)
                data.setdefault("entries", {})
                return data
    except (json.JSONDecodeError, OSError):
        pass
    return _default_validation_cache()


def _save_validation_cache(cache: dict, cache_path: Path = PDF_VALIDATION_CACHE_PATH) -> None:
    """Save PDF validation cache to disk."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def _default_perfected_state() -> dict:
    return {"version": PERFECTED_STATE_VERSION, "entries": {}}


def _load_perfected_state(state_path: Path = PERFECTED_STATE_PATH) -> dict:
    """Load uploaded/perfected paper state from disk."""
    if not state_path.exists():
        return _default_perfected_state()
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                if data.get("version") != PERFECTED_STATE_VERSION:
                    return _default_perfected_state()
                data.setdefault("version", PERFECTED_STATE_VERSION)
                data.setdefault("entries", {})
                return data
    except (json.JSONDecodeError, OSError):
        pass
    return _default_perfected_state()


def _save_perfected_state(state: dict, state_path: Path = PERFECTED_STATE_PATH) -> None:
    """Save uploaded/perfected paper state to disk."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def _compute_source_signature(paper_key: str, paper_config: dict) -> dict:
    """Compute a stable signature for all source files that influence one paper."""
    source_files = get_paper_source_files(
        paper_key=paper_key,
        paper_config=paper_config,
        project_root=PROJECT_ROOT,
    )
    digest = hashlib.sha256()
    tracked = []
    project_root_resolved = PROJECT_ROOT.resolve()

    for source_path in sorted(source_files, key=lambda p: str(p).lower()):
        if not source_path.exists():
            continue
        try:
            rel_path = source_path.resolve().relative_to(project_root_resolved)
            rel_str = str(rel_path).replace("\\", "/")
        except Exception:
            rel_str = str(source_path.resolve()).replace("\\", "/")

        file_sha = compute_sha256(source_path)
        digest.update(f"{rel_str}|{file_sha}\n".encode("utf-8", errors="replace"))
        tracked.append(
            {
                "path": rel_str,
                "sha256": file_sha,
            }
        )
    return {
        "file_count": len(tracked),
        "fingerprint": digest.hexdigest(),
    }


def _pdf_signature_matches(pdf_path: Path, expected_signature: dict | None) -> bool:
    """Compare on-disk PDF with cached content hash (mtime ignored)."""
    if not expected_signature or not isinstance(expected_signature, dict):
        return False
    if not pdf_path.exists():
        return False

    expected_sha = str(expected_signature.get("sha256", "")).strip()
    if not expected_sha:
        return False
    return compute_sha256(pdf_path) == expected_sha


def _is_perfected_entry_valid(
    entry: dict | None,
    source_signature: dict,
    pdf_path: Path,
) -> bool:
    """Check whether a paper can be skipped as already perfected/uploaded."""
    if not entry or not isinstance(entry, dict):
        return False
    if not bool(entry.get("upload_verified", False)):
        return False
    if not bool(entry.get("validation_passed", False)):
        return False
    if entry.get("source_signature") != source_signature:
        return False
    return _pdf_signature_matches(pdf_path, entry.get("pdf_signature"))


def _extract_llm_error_type(error_line: str) -> str | None:
    """Extract LLM error type token from a validator output line."""
    # Detailed line format: [CRITICAL:LLM_SOMETHING]
    detailed_match = re.search(r"\[(?:CRITICAL|WARNING|INFO):(LLM_[A-Z0-9_/\-]+)\]", error_line)
    if detailed_match:
        return detailed_match.group(1).replace("/", "_")

    # Summary line format: LLM_SOMETHING [CRITICAL]:
    summary_match = re.match(r"^(LLM_[A-Z0-9_/\-]+)\s+\[", error_line.strip())
    if summary_match:
        return summary_match.group(1).replace("/", "_")

    return None


def _normalize_llm_type_token(token: str) -> str:
    """Normalize CLI/config tokens to canonical LLM_* form."""
    normalized = token.strip().upper().replace("-", "_").replace(" ", "_")
    normalized = re.sub(r"[^A-Z0-9_]", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    if not normalized:
        return ""
    if not normalized.startswith("LLM_"):
        normalized = f"LLM_{normalized}"
    return normalized


def _parse_llm_type_csv(raw_value: str | None, default_types: tuple[str, ...]) -> set[str]:
    """Parse comma-separated LLM issue types into a normalized set."""
    if raw_value is None:
        return {t for t in default_types}

    raw_value = raw_value.strip()
    if not raw_value:
        return set()

    parsed: set[str] = set()
    for token in raw_value.split(","):
        normalized = _normalize_llm_type_token(token)
        if normalized:
            parsed.add(normalized)
    return parsed


def _classify_llm_error(
    error_line: str,
    blocking_types: set[str],
    warning_types: set[str],
) -> tuple[bool, str | None]:
    """Classify one LLM validator line as blocking or warning."""
    error_type = _extract_llm_error_type(error_line)
    if not error_type:
        # Unknown LLM line: conservative default is blocking.
        return True, None

    normalized_type = _normalize_llm_type_token(error_type)
    if normalized_type in warning_types and normalized_type not in blocking_types:
        return False, normalized_type

    if normalized_type in blocking_types:
        return True, normalized_type

    # Any unclassified LLM finding remains blocking by default.
    return True, normalized_type


def copy_with_retry(
    src: Path,
    dst: Path,
    max_retries: int = 10,
    initial_delay_seconds: float = 0.5,
) -> None:
    """Copy a file with retries to tolerate transient Windows file locks."""
    delay = initial_delay_seconds
    last_error: Exception | None = None
    dst.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        try:
            shutil.copy2(src, dst)
            return
        except OSError as e:
            last_error = e
            winerror = getattr(e, "winerror", None)
            # Retry for transient file locks, permission issues, and PermissionError (subclass of OSError).
            is_retryable = (
                winerror in (32, 33, 1224)
                or "being used by another process" in str(e).lower()
                or isinstance(e, PermissionError)
            )
            if is_retryable and attempt < max_retries:
                time.sleep(delay)
                delay = min(delay * 1.5, 5.0)
                continue
            raise

    if last_error:
        raise last_error


def generate_report(report_data: dict) -> str:
    """Generate markdown report from upload run data."""
    def _normalize_list(value) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        return []

    skipped_results = report_data.get("skipped_results", {})
    skipped_count = len(skipped_results)

    lines = [
        "# Zenodo Upload Report",
        "",
        f"**Date:** {report_data['timestamp']}",
        f"**Duration:** {report_data['total_duration']:.1f} seconds",
        f"**Papers Processed:** {report_data['papers_count']}",
        "",
        "## Summary",
        "",
        f"- **Successful:** {report_data['success_count']}",
        f"- **Failed:** {report_data['failed_count']}",
        f"- **Skipped (already perfected/uploaded):** {skipped_count}",
        f"- **LLM Blocking Types:** `{', '.join(report_data.get('llm_blocking_types', list(DEFAULT_LLM_BLOCKING_TYPES))) or '(none)'}`",
        f"- **LLM Warning Types:** `{', '.join(report_data.get('llm_warning_types', list(DEFAULT_LLM_WARNING_TYPES))) or '(none)'}`",
        f"- **Continue On Validation Error:** `{bool(report_data.get('continue_on_validation_error', False))}`",
        "",
    ]

    if skipped_results:
        lines.extend([
            "## Already Perfected (Skipped)",
            "",
            "| Paper | Reason | DOI |",
            "|-------|--------|-----|",
        ])
        for paper_key, result in skipped_results.items():
            reason = str(result.get("reason", "Already perfected")).replace("|", "\\|")
            doi = str(result.get("doi", "N/A")).replace("|", "\\|")
            lines.append(f"| {paper_key} | {reason} | {doi} |")
        lines.append("")

    if report_data['build_results']:
        lines.extend([
            "## Build Results",
            "",
            "| Paper | Status | Duration | QMD Files | Pages | PDF Size |",
            "|-------|--------|----------|-----------|-------|----------|",
        ])
        for paper_key, result in report_data['build_results'].items():
            status = "OK" if result['success'] else "FAILED"
            duration = f"{result['duration_seconds']:.1f}s"
            qmd_count = result.get('qmd_count', 'N/A')
            pages = result.get('pages') or 'N/A'
            pdf_size = result.get('pdf_size', 'N/A')
            lines.append(f"| {paper_key} | {status} | {duration} | {qmd_count} | {pages} | {pdf_size} |")
        lines.append("")

    if report_data.get('validation_results'):
        lines.extend([
            "## Validation Results",
            "",
            "| Paper | Status | Source | Notes | Error Count | Warning Count | AI Fix Log |",
            "|-------|--------|--------|-------|-------------|---------------|------------|",
        ])
        validation_error_details = []
        validation_warning_details = []
        for paper_key, result in report_data['validation_results'].items():
            if result.get("skipped"):
                status = "SKIPPED"
                source = "perfected-cache"
            else:
                status = "OK" if result.get('success') else "FAILED"
                source = "cache" if result.get('from_cache') else "fresh"
            error_list = _normalize_list(result.get('errors'))
            warning_list = _normalize_list(result.get('warnings'))
            note_text = str(result.get('notes', '')).strip()
            if not note_text and not result.get('success'):
                note_text = "Validation failed"
            notes = note_text.replace("|", "\\|")
            ai_fix_log = str(result.get("ai_fix_log_path", "") or "").strip()
            ai_fix_log_display = f"`{ai_fix_log}`" if ai_fix_log else "-"
            lines.append(
                f"| {paper_key} | {status} | {source} | {notes} | {len(error_list)} | {len(warning_list)} | {ai_fix_log_display} |"
            )
            if error_list:
                validation_error_details.append((paper_key, error_list))
            if warning_list:
                validation_warning_details.append((paper_key, warning_list))
        lines.append("")

        if validation_error_details:
            lines.extend([
                "### Validation Error Details",
                "",
            ])
            for paper_key, error_list in validation_error_details:
                lines.append(f"#### {paper_key}")
                lines.append("")
                for error in error_list:
                    message = str(error).replace("\n", " ").strip()
                    lines.append(f"- {message}")
                lines.append("")

        if validation_warning_details:
            lines.extend([
                "### Validation Warning Details",
                "",
            ])
            for paper_key, warning_list in validation_warning_details:
                lines.append(f"#### {paper_key}")
                lines.append("")
                for warning in warning_list:
                    message = str(warning).replace("\n", " ").strip()
                    lines.append(f"- {message}")
                lines.append("")

    if report_data['upload_results']:
        lines.extend([
            "## Upload Results",
            "",
            "| Paper | Status | DOI | Deposit ID | URL | Notes |",
            "|-------|--------|-----|------------|-----|-------|",
        ])
        for paper_key, result in report_data['upload_results'].items():
            if result and result.get('skipped'):
                status = "SKIPPED"
                doi = result.get('doi', 'N/A')
                deposit_id = result.get('id', 'N/A')
                url = result.get('url', 'N/A')
                notes = str(result.get("reason", "Skipped")).replace("|", "\\|")
            elif result and result.get('verified'):
                status = "OK"
                doi = result.get('doi', 'N/A')
                deposit_id = result.get('id', 'N/A')
                url = result.get('url', 'N/A')
                notes = str(result.get("reason", "") or "-").replace("|", "\\|")
            else:
                status = "FAILED"
                doi = "N/A"
                deposit_id = "N/A"
                url = "N/A"
                notes = str((result or {}).get("reason", "Upload not completed")).replace("|", "\\|")
            lines.append(f"| {paper_key} | {status} | {doi} | {deposit_id} | {url} | {notes} |")
        lines.append("")

    if report_data['errors']:
        lines.extend([
            "## Errors and Warnings",
            "",
        ])
        for paper_key, errors in report_data['errors'].items():
            if errors:
                lines.append(f"### {paper_key}")
                lines.append("")
                for error in errors:
                    lines.append(f"- {error}")
                lines.append("")

    if report_data.get('warnings'):
        lines.extend([
            "## Non-Blocking Warnings",
            "",
        ])
        for paper_key, warnings in report_data['warnings'].items():
            if warnings:
                lines.append(f"### {paper_key}")
                lines.append("")
                for warning in warnings:
                    lines.append(f"- {warning}")
                lines.append("")

    if report_data['errors']:
        lines.extend([
            "## Autonomous Fix Checklist",
            "",
        ])
        for paper_key, errors in report_data['errors'].items():
            if not errors:
                continue
            lines.append(f"### {paper_key}")
            lines.append("")
            lines.append("- [ ] Resolve all issues listed below for this paper.")
            for error in errors:
                lines.append(f"- [ ] {error}")

            validation_result = report_data.get("validation_results", {}).get(paper_key, {})
            ai_fix_log = str(validation_result.get("ai_fix_log_path", "") or "").strip()
            if ai_fix_log:
                lines.append(f"- [ ] Read AI fix guide: `{ai_fix_log}`")

            lines.append(
                f"- [ ] Re-run this paper: `python scripts/upload-all-zenodo-and-save-dois.py {paper_key} --force-revalidate`"
            )
            lines.append("")

        lines.extend([
            "### Agent Prompt",
            "",
            "Use the checklist above as the source of truth.",
            "After each fix, rerun only the failing paper command.",
            "Continue until this report shows zero failed papers and no checklist items.",
            "",
        ])

    if report_data.get("actions"):
        lines.extend([
            "## Action Log",
            "",
        ])
        for action in report_data.get("actions", []):
            lines.append(f"- {action}")
        lines.append("")

    lines.extend([
        "## Next Steps",
        "",
        "1. Review the results above",
        "2. Check drafts on Zenodo: https://zenodo.org/me/uploads",
        "3. Review config changes: `git diff _quarto-*.yml`",
        "4. Commit updates: `git add _quarto-*.yml && git commit -m 'update: Zenodo DOIs'`",
        "",
    ])

    return "\n".join(lines)


def discover_papers() -> dict:
    """Find all Quarto paper configs using shared discovery utility."""
    items = discover_pdf_work_items_sorted(project_root=PROJECT_ROOT)
    papers = {}
    for item in items:
        key = item["config_name"]
        papers[key] = {
            "config_path": item["config_path"],
            "config": item["config"],
            "pdf_path": item["assets_pdf_rel_path"],
            "build_pdf_path": str(item["build_pdf_path"].relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "pdf_filename": item["pdf_filename"],
            "qmd_count": item["qmd_count"],
        }
    return papers


def get_pdf_page_count(pdf_path: Path) -> int | None:
    """Get page count from a PDF using PyMuPDF."""
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        count = len(doc)
        doc.close()
        return count
    except Exception:
        return None


def validate_existing_pdf(
    pdf_path: Path,
    verbose: bool = False,
    use_cache: bool = True,
    skip_url_check: bool = True,
    llm_blocking_types: set[str] | None = None,
    llm_warning_types: set[str] | None = None,
) -> tuple[bool, list[str], list[str], bool, str | None]:
    """Run pdf-validation.py with required LLM checks and local result caching.

    Returns (passed, blocking_errors, warnings, from_cache, ai_fix_log_path).
    """
    blocking_types: set[str]
    warning_types: set[str]
    if llm_blocking_types is None:
        blocking_types = set(DEFAULT_LLM_BLOCKING_TYPES)
    else:
        blocking_types = set(llm_blocking_types)
    if llm_warning_types is None:
        warning_types = set(DEFAULT_LLM_WARNING_TYPES)
    else:
        warning_types = set(llm_warning_types)
    warning_types -= blocking_types

    signature = _compute_pdf_signature(pdf_path)
    cache_key = _cache_key_for_pdf(pdf_path)
    cache = _load_validation_cache() if use_cache else _default_validation_cache()
    cache_entries = cache.setdefault("entries", {})

    if use_cache:
        cached = cache_entries.get(cache_key)
        cached_blocking_types = cached.get("llm_blocking_types", []) if isinstance(cached, dict) else []
        if not isinstance(cached_blocking_types, list):
            cached_blocking_types = []
        cached_warning_types = cached.get("llm_warning_types", []) if isinstance(cached, dict) else []
        if not isinstance(cached_warning_types, list):
            cached_warning_types = []
        if (
            isinstance(cached, dict)
            and cached.get("signature") == signature
            and set(cached_blocking_types) == blocking_types
            and set(cached_warning_types) == warning_types
            and bool(cached.get("llm_completed", False))
        ):
            cached_passed = bool(cached.get("passed", False))
            cached_errors = cached.get("errors", [])
            if not isinstance(cached_errors, list):
                cached_errors = []
            cached_warnings = cached.get("warnings", [])
            if not isinstance(cached_warnings, list):
                cached_warnings = []
            cached_fix_log = cached.get("ai_fix_log_path")
            if cached_fix_log and not isinstance(cached_fix_log, str):
                cached_fix_log = None
            if verbose:
                cache_status = "PASSED" if cached_passed else "FAILED"
                print(f"  Using cached validation result ({cache_status}) for {pdf_path.name}", flush=True)
            return cached_passed, cached_errors, cached_warnings, True, cached_fix_log

    if not os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY"):
        return (
            False,
            ["GOOGLE_GENERATIVE_AI_API_KEY is not set (required for LLM PDF validation)."],
            [],
            False,
            None,
        )

    python_exe = get_preferred_python(PROJECT_ROOT)
    print(
        f"  Starting PDF validation for {pdf_path.name} (full-PDF LLM review). "
        "This can take a while for full-document validation...",
        flush=True,
    )
    validation_result = run_pdf_validation(
        pdf_path=pdf_path,
        cwd=PROJECT_ROOT,
        python_executable=python_exe,
        verbose=True,  # Always show validation output
        skip_url_check=skip_url_check,
        use_cache=use_cache,
        include_broken_external_errors=True,
        line_filter=None,  # Show all output (no filtering)
    )
    output = validation_result.output
    validation_duration = validation_result.duration_seconds
    print(
        f"  PDF validation finished for {pdf_path.name} in {validation_duration:.1f}s (rc={validation_result.returncode})",
        flush=True,
    )

    extracted_errors = validation_result.errors
    ai_fix_log_path = validation_result.ai_fix_log_path
    llm_errors = [e for e in extracted_errors if "LLM_" in e]
    non_llm_errors = [e for e in extracted_errors if "LLM_" not in e]

    llm_skipped = "LLM validation skipped" in output
    llm_failed = "LLM validation failed for page" in output
    llm_completed = not (llm_skipped or llm_failed)

    llm_blocking_errors = []
    llm_warnings = []
    for llm_error in llm_errors:
        is_blocking, normalized_type = _classify_llm_error(
            llm_error,
            blocking_types=blocking_types,
            warning_types=warning_types,
        )
        if is_blocking:
            llm_blocking_errors.append(llm_error)
        else:
            if normalized_type:
                llm_warnings.append(f"{llm_error} [type={normalized_type}]")
            else:
                llm_warnings.append(llm_error)

    if llm_skipped:
        non_llm_errors.append("LLM validation was skipped; uploads require completed LLM validation.")
    if llm_failed:
        non_llm_errors.append("LLM validation failed for one or more pages; rerun after fixing model/API issues.")

    # Gate uploads on deterministic checks + configured blocking LLM findings.
    blocking_errors = list(non_llm_errors) + list(llm_blocking_errors)
    passed = llm_completed and not blocking_errors

    if not passed and not blocking_errors:
        blocking_errors.append(f"Validation failed with exit code {validation_result.returncode}")

    if use_cache:
        cache_entries[cache_key] = {
            "signature": signature,
            "validated_at": datetime.now().isoformat(),
            "llm_blocking_types": sorted(blocking_types),
            "llm_warning_types": sorted(warning_types),
            "llm_completed": llm_completed,
            "passed": passed,
            "errors": blocking_errors,
            "warnings": llm_warnings,
            "llm_warnings": llm_warnings,
            "ai_fix_log_path": ai_fix_log_path,
            "returncode": validation_result.returncode,
        }
        _save_validation_cache(cache)

    return passed, blocking_errors, llm_warnings, validation_result.from_cache, ai_fix_log_path


def rebuild_paper(paper_key: str, verbose: bool = False) -> dict:
    """Rebuild a paper using render-quarto.py.

    Returns:
        dict with keys: success (bool), duration_seconds (float), errors (list)
    """
    print(f"\n[*] Building {paper_key}...", flush=True)
    render_script = PROJECT_ROOT / "scripts" / "render-quarto.py"
    start_time = time.time()
    errors = []

    # Patterns to filter out (noisy output for batch mode)
    noise_patterns = (
        # Pip/package installation
        "Requirement already satisfied",
        "Installing collected packages",
        "Successfully installed",
        "Downloading",
        "Using cached",
        "Collecting",
        "  Preparing metadata",
        "Building wheel",
        "Created wheel",
        "Stored in directory",
        # Validation/generation details (success assumed unless error)
        "[OK]",
        "[*] Parsing",
        "[*] Generating",
        "[*] Validating",
        "[*] Cleaning",
        "[*] Checking",
        "[*] Syncing",
        "[*] Regenerating",
        "[*] Loading",
        "[*] Ensuring",
        "[*] Using venv",
        "[*] Jupyter kernel",
        "[*] Created build",
        "[*] Copying",
        "[*] Preprocessing",
        "[*] Changed to",
        "[*] Next steps",
        "Loaded config:",
        "Loaded ",
        "Found ",
        "Running pre-render",
        "Pre-validation passed",
        "No pre-validation errors",
        # Separator lines
        "=" * 10,
        "─" * 10,
        "━" * 10,
    )

    # Patterns to always show (important status)
    show_patterns = (
        "ERROR",
        "FATAL",
        "WARNING",
        "FAILED",
        "Build failed",
        "not found",
        "Exception",
        "Traceback",
        "pandoc",  # Quarto/pandoc progress
        "Output created",
        "rendering",
    )

    try:
        python_exe = get_preferred_python(PROJECT_ROOT)
        process = subprocess.Popen(
            [python_exe, "-u", str(render_script), paper_key],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Stream output, filtering noise
        for line in (process.stdout or []):
            line = line.rstrip()
            if not line:
                continue

            # Capture errors for report
            if any(p in line for p in ("ERROR", "FATAL", "FAILED", "Exception")):
                errors.append(line)

            # In verbose mode, show everything
            if verbose:
                print(f"  {line}", flush=True)
                continue

            # Always show important patterns (errors, warnings, progress)
            if any(p in line for p in show_patterns):
                print(f"  {line}", flush=True)
                continue

            # Skip noisy lines
            if any(p in line for p in noise_patterns):
                continue

            # Show anything else that made it through
            print(f"  {line}", flush=True)

        process.wait(timeout=600)
        duration = time.time() - start_time

        if process.returncode == 0:
            print(f"[OK] Built {paper_key}", flush=True)
            return {"success": True, "duration_seconds": duration, "errors": errors}
        print(f"ERROR: Build failed for {paper_key}", flush=True)
        errors.append(f"Build failed with return code {process.returncode}")
        return {"success": False, "duration_seconds": duration, "errors": errors}
    except subprocess.TimeoutExpired:
        process.kill()
        duration = time.time() - start_time
        print(f"ERROR: Build timeout for {paper_key}", flush=True)
        errors.append("Build timeout after 600 seconds")
        return {"success": False, "duration_seconds": duration, "errors": errors}
    except Exception as e:
        duration = time.time() - start_time
        print(f"ERROR: {e}", flush=True)
        errors.append(str(e))
        return {"success": False, "duration_seconds": duration, "errors": errors}


def _resolve_run_id(report_data: dict) -> str:
    """Resolve a stable run id used for report archive filenames."""
    run_id = str(report_data.get("run_id", "") or "").strip()
    if run_id:
        return run_id
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def _generate_validation_error_report(report_data: dict) -> str | None:
    """Build a dedicated validation error report containing all blocking validation errors."""
    validation_results = report_data.get("validation_results", {})
    if not isinstance(validation_results, dict):
        return None

    failed_entries: list[tuple[str, list[str], str]] = []
    for paper_key, result in validation_results.items():
        if not isinstance(result, dict):
            continue
        errors = result.get("errors", [])
        if not isinstance(errors, list):
            continue
        normalized_errors = [str(e).strip() for e in errors if str(e).strip()]
        if not normalized_errors:
            continue
        note = str(result.get("notes", "") or "").strip()
        failed_entries.append((str(paper_key), normalized_errors, note))

    if not failed_entries:
        return None

    lines = [
        "# Zenodo Validation Errors",
        "",
        f"**Date:** {report_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}",
        f"**Run ID:** {report_data.get('run_id', 'N/A')}",
        f"**Failed Papers:** {len(failed_entries)}",
        "",
        "## Errors",
        "",
    ]

    for paper_key, errors, note in failed_entries:
        lines.append(f"### {paper_key}")
        lines.append("")
        if note:
            lines.append(f"- **Summary:** {note}")
        lines.append(f"- **Blocking Errors:** {len(errors)}")
        lines.append("")
        for error in errors:
            lines.append(f"- {error}")
        lines.append("")

    return "\n".join(lines)


def save_report(report_data: dict, start_time: float) -> Path:
    """Generate and save report to project root.

    Returns the path to the saved report.
    """
    report_data['total_duration'] = time.time() - start_time
    run_id = _resolve_run_id(report_data)
    report_data["run_id"] = run_id
    report_text = generate_report(report_data)

    # Save latest report to root (overwrite)
    report_path = PROJECT_ROOT / "zenodo-upload-report.md"
    report_path.write_text(report_text, encoding='utf-8')
    
    # Append report to the single log file
    try:
        log_file = PROJECT_ROOT / "zenodo-upload.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n" + "="*80 + "\n")
            f.write("FINAL REPORT\n")
            f.write("="*80 + "\n")
            f.write(report_text)
            f.write("\n" + "="*80 + "\n")
    except Exception as e:
        print(f"[WARNING] Failed to append report to log: {e}")

    print(f"\nReport saved to: {report_path}")
    # Archives and separate validation error files are disabled to reduce clutter
    
    return report_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch upload papers to Zenodo with validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python scripts/upload-all-zenodo-and-save-dois.py                # auto-publish
  python scripts/upload-all-zenodo-and-save-dois.py --draft        # create drafts only
  python scripts/upload-all-zenodo-and-save-dois.py economics iab  # specific papers
  python scripts/upload-all-zenodo-and-save-dois.py --verbose      # show full output
  python scripts/upload-all-zenodo-and-save-dois.py --force-revalidate""",
    )
    parser.add_argument(
        "papers", nargs="*",
        help="Specific paper keys to upload (default: all papers)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show full build/validation output",
    )
    parser.add_argument(
        "--force-revalidate",
        action="store_true",
        help="Ignore cached PDF validation results and run validation again",
    )
    parser.add_argument(
        "--force-reprocess",
        action="store_true",
        help="Ignore perfected/uploaded state cache and process all selected papers again",
    )
    parser.add_argument(
        "--continue-on-validation-error",
        action="store_true",
        help=(
            "Continue processing remaining non-perfect papers when a paper fails validation. "
            "Failed-validation papers are not uploaded."
        ),
    )
    parser.add_argument(
        "--llm-blocking-types",
        default=",".join(DEFAULT_LLM_BLOCKING_TYPES),
        help=(
            "Comma-separated LLM issue types that block upload. "
            "Defaults to all core high-confidence issue types."
        ),
    )
    parser.add_argument(
        "--llm-warning-types",
        default=",".join(DEFAULT_LLM_WARNING_TYPES),
        help=(
            "Comma-separated LLM issue types treated as non-blocking warnings. "
            "Empty by default."
        ),
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Create drafts without publishing (default: auto-publish after validation)"
    )
    return parser.parse_args()


class Tee:
    """Duplicate output to a file and the original stream."""
    def __init__(self, name, mode, encoding='utf-8'):
        self.file = open(name, mode, encoding=encoding)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def __del__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
        self.file.flush()
        self.stdout.flush()

    def flush(self):
        self.file.flush()
        self.stdout.flush()

def main():
    # Setup root logging
    try:
        log_file = PROJECT_ROOT / "zenodo-upload.log"
        tee = Tee(str(log_file), "a", encoding="utf-8")
        print(f"[LOG] Writing full execution log to: {log_file}")
    except Exception as e:
        print(f"[WARNING] Failed to setup file logging: {e}")

    args = parse_args()
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    llm_blocking_types = _parse_llm_type_csv(
        args.llm_blocking_types,
        DEFAULT_LLM_BLOCKING_TYPES,
    )
    llm_warning_types = _parse_llm_type_csv(
        args.llm_warning_types,
        DEFAULT_LLM_WARNING_TYPES,
    )
    llm_warning_types -= llm_blocking_types

    # Initialize report data
    report_data = {
        'run_id': run_id,
        'timestamp': timestamp,
        'papers_count': 0,
        'success_count': 0,
        'failed_count': 0,
        'llm_blocking_types': sorted(llm_blocking_types),
        'llm_warning_types': sorted(llm_warning_types),
        'continue_on_validation_error': bool(args.continue_on_validation_error),
        'skipped_results': {},
        'build_results': {},
        'validation_results': {},
        'upload_results': {},
        'errors': {},
        'warnings': {},
        'actions': [],
        'total_duration': 0,
    }

    def log_action(message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        report_data["actions"].append(f"[{stamp}] {message}")

    load_project_dotenv(PROJECT_ROOT)

    token = get_zenodo_token()
    if not token:
        print("ERROR: ZENODO_TOKEN not set")
        print("  Get token at: https://zenodo.org/account/settings/applications/")
        return 1

    client = ZenodoClient(token)

    print("=" * 60)
    print("Zenodo Batch Upload")
    print("=" * 60)

    papers = discover_papers()
    if not papers:
        print("ERROR: No paper configs found")
        return 1

    # Filter to specific papers if args provided
    if args.papers:
        requested = set(args.papers)
        papers = {k: v for k, v in papers.items() if k in requested}
        if not papers:
            print(f"ERROR: No matching papers: {', '.join(requested)}")
            return 1

    # Sort papers by QMD file count (smallest first for faster feedback)
    sorted_keys = sorted(papers.keys(), key=lambda k: papers[k]["qmd_count"])

    report_data['papers_count'] = len(sorted_keys)

    print("Papers selected (sorted by size, smallest first):")
    for key in sorted_keys:
        print(f"  {key}: {papers[key]['qmd_count']} QMD files")
    print()
    log_action(f"Selected {len(sorted_keys)} paper(s): {', '.join(sorted_keys)}")

    perfected_state = _load_perfected_state()
    perfected_entries = perfected_state.setdefault("entries", {})
    source_signatures: dict[str, dict] = {}
    process_keys: list[str] = []

    assets_pdf_dir = PROJECT_ROOT / "assets" / "pdfs"
    assets_pdf_dir.mkdir(parents=True, exist_ok=True)

    print("LLM validation mode: full document (all pages)")
    print(
        "LLM blocking types: "
        + (", ".join(sorted(llm_blocking_types)) if llm_blocking_types else "(none)")
    )
    print(
        "LLM warning types: "
        + (", ".join(sorted(llm_warning_types)) if llm_warning_types else "(none)")
    )
    print(f"Publication mode: {'create drafts only' if args.draft else 'auto-publish after validation'}")
    if args.continue_on_validation_error:
        print("Validation behavior: continue past validation failures (skip upload for failed papers)")
    else:
        print("Validation behavior: fail-fast on first failed PDF")
    log_action(
        "Validation configured with "
        f"llm_blocking_types={','.join(sorted(llm_blocking_types)) or '(none)'}, "
        f"llm_warning_types={','.join(sorted(llm_warning_types)) or '(none)'}, "
        f"continue_on_validation_error={bool(args.continue_on_validation_error)}"
    )

    if args.force_reprocess:
        print("Perfected state cache: ignored (--force-reprocess)")
    else:
        print(f"Perfected state cache: {PERFECTED_STATE_PATH.relative_to(PROJECT_ROOT)}")

    for paper_key in sorted_keys:
        info = papers[paper_key]
        source_signature = _compute_source_signature(paper_key, info)
        source_signatures[paper_key] = source_signature

        pdf_path = PROJECT_ROOT / info["pdf_path"]

        if args.force_reprocess:
            process_keys.append(paper_key)
            continue

        state_entry = perfected_entries.get(paper_key)
        if _is_perfected_entry_valid(
            entry=state_entry,
            source_signature=source_signature,
            pdf_path=pdf_path,
        ):
            doi = state_entry.get("doi", "N/A")
            print(f"[SKIP] {paper_key}: already perfected/uploaded and unchanged")
            log_action(f"Skipped {paper_key} (perfected cache hit)")
            report_data["skipped_results"][paper_key] = {
                "reason": "Already perfected/uploaded; source+PDF signatures unchanged",
                "doi": doi,
            }
            report_data["validation_results"][paper_key] = {
                "success": True,
                "from_cache": True,
                "skipped": True,
                "notes": "Skipped (perfected cache hit)",
                "errors": [],
                "warnings": [],
                "ai_fix_log_path": None,
            }
            report_data["upload_results"][paper_key] = {
                "verified": True,
                "skipped": True,
                "doi": doi,
                "id": state_entry.get("deposit_id", "N/A"),
                "url": state_entry.get("url", "N/A"),
            }
            continue

        process_keys.append(paper_key)

    if not process_keys:
        print("\nAll selected papers are already perfected and uploaded. Nothing to do.")
        log_action("No processing required: all selected papers were already perfected/uploaded")
        report_data["success_count"] = len(report_data["upload_results"])
        save_report(report_data, start_time)
        return 0

    # Unified flow: for each paper, get the freshest PDF available
    # 1. Local PDF newer than sources → use it (skip everything)
    # 2. Remote published PDF available → download it (skip rebuild)
    # 3. Neither fresh → rebuild locally
    # 4. Validate the paper immediately (either fail-fast or continue mode)
    print("Getting freshest PDFs...")
    print("\nRunning required PDF validation (LLM enabled, cached by file signature)...")
    if args.force_revalidate:
        print("  Validation cache: disabled (--force-revalidate)")
    else:
        print(f"  Validation cache: {PDF_VALIDATION_CACHE_PATH.relative_to(PROJECT_ROOT)}")

    upload_candidates: list[str] = []

    for paper_key in process_keys:
        info = papers[paper_key]
        pdf_path = PROJECT_ROOT / info["pdf_path"]
        build_pdf_path = PROJECT_ROOT / info["build_pdf_path"]
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        newest_source_mtime = get_newest_paper_source_mtime(
            paper_key=paper_key,
            paper_config=info,
            project_root=PROJECT_ROOT,
        )

        # Step 1: Sync freshest local PDF into assets/pdfs.
        if build_pdf_path.exists() and (
            not pdf_path.exists() or build_pdf_path.stat().st_mtime > pdf_path.stat().st_mtime
        ):
            copy_with_retry(build_pdf_path, pdf_path)
            print(f"  -> Synced newer local build PDF to: {info['pdf_path']}")

        # Step 2: Check remote and download only if it's newer than local assets PDF.
        # Force remote download destination to assets/pdfs for freshness + upload.
        download_target = dict(info)
        download_target["pdf_path"] = info["pdf_path"]
        downloaded_pdf = check_and_download_remote_pdf(
            paper_key=paper_key,
            paper_config=download_target,
            project_root=PROJECT_ROOT,
            timeout=30,
        )
        if downloaded_pdf:
            pdf_path = downloaded_pdf

        # Step 3: Is the canonical assets PDF newer than sources?
        if pdf_path.exists() and pdf_path.stat().st_mtime >= newest_source_mtime:
            print(f"\n[OK] PDF is fresh for {paper_key}", flush=True)
            build_result = {"success": True, "duration_seconds": 0.0, "errors": []}
        else:
            # Step 4: PDF is stale or missing — rebuild
            print(f"\n[BUILD] Rebuilding {paper_key} (PDF older than sources)", flush=True)
            build_result = rebuild_paper(paper_key, verbose=args.verbose)

            # Keep assets/pdfs as source of truth, sync from build output when newer/missing.
            if build_pdf_path.exists() and (
                not pdf_path.exists() or build_pdf_path.stat().st_mtime > pdf_path.stat().st_mtime
            ):
                pdf_path.parent.mkdir(parents=True, exist_ok=True)
                copy_with_retry(build_pdf_path, pdf_path)
                print(f"  -> Copied rebuilt PDF to: {info['pdf_path']}")

            # Store build result with additional metadata
            build_result['qmd_count'] = info['qmd_count']

            if pdf_path.exists():
                pdf_size_mb = pdf_path.stat().st_size / (1024 * 1024)
                build_result['pdf_size'] = f"{pdf_size_mb:.2f} MB"
                build_result['pages'] = get_pdf_page_count(pdf_path)
            else:
                build_result['pdf_size'] = "N/A"
                build_result['pages'] = None

            report_data['build_results'][paper_key] = build_result

            if not build_result['success']:
                print(f"\n[FATAL] Build failed for {paper_key}")
                report_data['errors'][paper_key] = build_result['errors']
                report_data['failed_count'] += 1
                log_action(f"Build failed for {paper_key}")
                save_report(report_data, start_time)
                raise RuntimeError(f"Build failed for {paper_key}")

            if not pdf_path.exists():
                print(f"\n[FATAL] PDF not found after build: {pdf_path}")
                report_data['errors'][paper_key] = ["PDF not found after build"]
                report_data['failed_count'] += 1
                log_action(f"Build failed for {paper_key}: PDF not found after build")
                save_report(report_data, start_time)
                raise RuntimeError(f"PDF not found after build for {paper_key}: {pdf_path}")

        # Validate each paper immediately after selecting/building its PDF.
        print(f"\n[VALIDATE] {paper_key}: {pdf_path.name}")
        passed, validation_errors, validation_warnings, from_cache, ai_fix_log_path = validate_existing_pdf(
            pdf_path=pdf_path,
            verbose=args.verbose,
            use_cache=not args.force_revalidate,
            llm_blocking_types=llm_blocking_types,
            llm_warning_types=llm_warning_types,
        )

        source_note = "cache hit" if from_cache else "fresh run"
        if passed:
            if validation_warnings:
                note = f"{source_note}; {len(validation_warnings)} warning(s)"
            else:
                note = source_note
        elif validation_errors:
            extra_count = len(validation_errors) - 1
            suffix = f" (+{extra_count} more)" if extra_count > 0 else ""
            note = f"{validation_errors[0]}{suffix}"
        else:
            note = "Validation failed"

        report_data['validation_results'][paper_key] = {
            'success': passed,
            'from_cache': from_cache,
            'notes': note,
            'errors': validation_errors,
            'warnings': validation_warnings,
            'ai_fix_log_path': ai_fix_log_path,
        }
        if validation_warnings:
            report_data['warnings'][paper_key] = validation_warnings

        if passed:
            print(f"[OK] Validation passed for {paper_key} ({source_note})")
            if validation_warnings:
                print(f"[WARN] Non-blocking LLM warnings for {paper_key}: {len(validation_warnings)}")
                for warning in validation_warnings[:10]:
                    print(f"  - {warning}")
                if len(validation_warnings) > 10:
                    print(f"  - ...and {len(validation_warnings) - 10} more")
            log_action(
                f"Validated {paper_key}: passed ({source_note})"
                + (f" with {len(validation_warnings)} warning(s)" if validation_warnings else "")
            )
            upload_candidates.append(paper_key)
            continue

        print(f"\n[ERROR] Validation failed for {paper_key}")
        for error in validation_errors[:10]:
            print(f"  - {error}")
        if len(validation_errors) > 10:
            print(f"  - ...and {len(validation_errors) - 10} more")
        if validation_warnings:
            print(f"  Non-blocking warnings also found: {len(validation_warnings)}")

        report_data['errors'][paper_key] = validation_errors or ["PDF validation failed"]
        report_data['failed_count'] += 1
        report_data['upload_results'][paper_key] = {
            "verified": False,
            "reason": "Skipped upload because validation failed",
            "validation_blocked": True,
        }
        log_action(
            f"Validation failed for {paper_key}; blocking errors={len(validation_errors)} warnings={len(validation_warnings)}"
        )
        save_report(report_data, start_time)
        raise RuntimeError(f"Validation failed for {paper_key}: {validation_errors[0] if validation_errors else 'unknown'}")

    if not upload_candidates:
        print("\nNo papers eligible for upload after validation.")
        log_action("No papers eligible for upload after validation")

    # Upload each validated paper (crash on errors)
    for paper_key in upload_candidates:
        info = papers[paper_key]
        pdf_path = PROJECT_ROOT / info["pdf_path"]
        log_action(f"Uploading {paper_key}")
        if not pdf_path.exists():
            fallback_pdf = PROJECT_ROOT / info["build_pdf_path"]
            if fallback_pdf.exists():
                print(f"[WARN] Using fallback build PDF for upload: {fallback_pdf}")
                pdf_path = fallback_pdf

        skip_remote_upload, skip_reason = _should_skip_upload_by_remote_checksum(
            client=client,
            quarto_config=info["config"],
            pdf_path=pdf_path,
        )
        if skip_remote_upload:
            metadata = info["config"].get("metadata", {}) if isinstance(info["config"], dict) else {}
            doi = str(metadata.get("doi", "N/A")) if isinstance(metadata, dict) else "N/A"
            print(f"[SKIP] {paper_key}: {skip_reason}")
            report_data["upload_results"][paper_key] = {
                "verified": True,
                "skipped": True,
                "doi": doi,
                "id": "N/A",
                "url": f"https://zenodo.org/record/{get_record_id_from_doi(doi)}" if get_record_id_from_doi(doi) else "N/A",
                "reason": f"Skipped upload; {skip_reason}",
            }
            perfected_entries[paper_key] = {
                "updated_at": datetime.now().isoformat(),
                "source_signature": source_signatures.get(paper_key, {}),
                "pdf_signature": _compute_pdf_signature(pdf_path),
                "validation_passed": True,
                "upload_verified": True,
                "doi": doi,
                "deposit_id": "N/A",
                "url": report_data["upload_results"][paper_key]["url"],
            }
            _save_perfected_state(perfected_state)
            log_action(f"Skipped upload for {paper_key}: remote checksum matched local PDF")
            continue
        print(f"[*] {paper_key}: remote checksum check unavailable/different, proceeding with upload ({skip_reason})")

        result = upload_paper(
            client=client,
            paper_key=paper_key,
            quarto_config=info["config"],
            pdf_path=pdf_path,
            draft=args.draft,
            verbose=True,
            save_doi=True,
            config_path=info["config_path"],
            project_root=PROJECT_ROOT,
        )

        report_data['upload_results'][paper_key] = result

        if not result or not result.get("verified"):
            print(f"\n[FATAL] Upload failed for {paper_key}")
            if paper_key not in report_data['errors']:
                report_data['errors'][paper_key] = []
            report_data['errors'][paper_key].append("Upload verification failed")
            report_data['failed_count'] += 1
            perfected_entries.pop(paper_key, None)
            _save_perfected_state(perfected_state)
            log_action(f"Upload failed for {paper_key}")
            save_report(report_data, start_time)
            raise RuntimeError(f"Upload failed for {paper_key}")

        log_action(f"Upload verified for {paper_key}: DOI {result.get('doi', 'N/A')}")
        perfected_entries[paper_key] = {
            "updated_at": datetime.now().isoformat(),
            "source_signature": source_signatures.get(paper_key, {}),
            "pdf_signature": _compute_pdf_signature(pdf_path),
            "validation_passed": True,
            "upload_verified": True,
            "doi": result.get("doi"),
            "deposit_id": result.get("id"),
            "url": result.get("url"),
        }
        _save_perfected_state(perfected_state)

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary")
    print("=" * 60)

    success, failed, skipped = [], [], []
    for key in sorted_keys:
        result = report_data['upload_results'].get(key)
        if result and result.get("skipped"):
            skipped.append(key)
            print(f"  {key}: SKIPPED - already perfected/uploaded")
        elif result and result.get("verified"):
            success.append(key)
            print(f"  {key}: OK - DOI: {result.get('doi', 'N/A')}")
        else:
            failed.append(key)
            print(f"  {key}: FAILED")

    report_data['success_count'] = len(success) + len(skipped)
    report_data['failed_count'] = len(failed)

    if success:
        print(f"\nUpdated {len(success)} config(s). Next steps:")
        print("  1. git diff _quarto-*.yml")
        print("  2. Review drafts on Zenodo")
        print("  3. git add _quarto-*.yml && git commit -m 'update: Zenodo DOIs'")

    if skipped:
        print(f"\nSkipped {len(skipped)} already-perfected paper(s).")

    # Generate final report
    save_report(report_data, start_time)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
