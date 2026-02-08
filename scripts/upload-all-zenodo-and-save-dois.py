#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Upload All Papers to Zenodo

Rebuilds all PDFs and uploads them to Zenodo, saving DOIs to config files.

Usage:
    python scripts/upload-all-zenodo-and-save-dois.py
    python scripts/upload-all-zenodo-and-save-dois.py economics iab  # specific papers only
    python scripts/upload-all-zenodo-and-save-dois.py --verbose      # show full build output
    python scripts/upload-all-zenodo-and-save-dois.py               # smart: skips rebuild if PDF is fresh
    python scripts/upload-all-zenodo-and-save-dois.py --force-revalidate

Environment:
    ZENODO_TOKEN: API token from https://zenodo.org/account/settings/applications/
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import subprocess
import io
import shutil
import time
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Missing dependency. Run: pip install python-dotenv")
    sys.exit(1)

from lib.zenodo_client import ZenodoClient, upload_paper, get_zenodo_token
from lib.quarto_config_utils import (
    discover_paper_configs,
    count_qmd_files,
    get_newest_paper_source_mtime,
    check_and_download_remote_pdf,
)

PROJECT_ROOT = Path(__file__).parent.parent
PDF_VALIDATION_CACHE_PATH = PROJECT_ROOT / ".cache" / "pdf-validation-upload-cache.json"
VALIDATION_CACHE_VERSION = 3


def _get_preferred_python() -> str:
    """Prefer project virtualenv Python when available."""
    if sys.platform == "win32":
        venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def _cache_key_for_pdf(pdf_path: Path) -> str:
    """Build a stable cache key for a PDF path."""
    return str(pdf_path.resolve()).replace("\\", "/").lower()


def _compute_sha256(file_path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA256 hash for a file."""
    digest = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _compute_pdf_signature(pdf_path: Path) -> dict:
    """Compute signature fields used for validation cache matching."""
    stats = pdf_path.stat()
    return {
        "size_bytes": stats.st_size,
        "mtime_ns": stats.st_mtime_ns,
        "sha256": _compute_sha256(pdf_path),
    }


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


def _extract_validation_errors(output: str) -> list[str]:
    """Extract key validation errors from validator output."""
    errors = []
    seen = set()
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if (
            "[CRITICAL:" in stripped
            or " [CRITICAL]:" in stripped
            or "BROKEN_EXTERNAL_LINK" in stripped
            or "[ERROR]" in stripped
            or stripped.startswith("ERROR:")
            or stripped.startswith("FATAL:")
            or "validation failed" in stripped.lower()
        ):
            if stripped not in seen:
                seen.add(stripped)
                errors.append(stripped)
    return errors


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
            # Retry for transient file locks and permission issues.
            if winerror in (32, 33, 1224) or "being used by another process" in str(e).lower():
                if attempt < max_retries:
                    time.sleep(delay)
                    delay = min(delay * 1.5, 5.0)
                    continue
            raise
        except PermissionError as e:
            last_error = e
            if attempt < max_retries:
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
        "",
    ]

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
            "| Paper | Status | Source | Notes | Error Count |",
            "|-------|--------|--------|-------|-------------|",
        ])
        validation_error_details = []
        for paper_key, result in report_data['validation_results'].items():
            status = "OK" if result.get('success') else "FAILED"
            source = "cache" if result.get('from_cache') else "fresh"
            error_list = _normalize_list(result.get('errors'))
            note_text = str(result.get('notes', '')).strip()
            if not note_text and not result.get('success'):
                note_text = "Validation failed"
            notes = note_text.replace("|", "\\|")
            lines.append(f"| {paper_key} | {status} | {source} | {notes} | {len(error_list)} |")
            if error_list:
                validation_error_details.append((paper_key, error_list))
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

    if report_data['upload_results']:
        lines.extend([
            "## Upload Results",
            "",
            "| Paper | Status | DOI | Deposit ID | URL |",
            "|-------|--------|-----|------------|-----|",
        ])
        for paper_key, result in report_data['upload_results'].items():
            if result and result.get('verified'):
                status = "OK"
                doi = result.get('doi', 'N/A')
                deposit_id = result.get('id', 'N/A')
                url = result.get('url', 'N/A')
            else:
                status = "FAILED"
                doi = "N/A"
                deposit_id = "N/A"
                url = "N/A"
            lines.append(f"| {paper_key} | {status} | {doi} | {deposit_id} | {url} |")
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
    raw_papers = discover_paper_configs(PROJECT_ROOT)

    # Add qmd_count for sorting by size
    papers = {}
    for key, info in raw_papers.items():
        pdf_filename = info.get("pdf_filename") or Path(info["pdf_path"]).name
        papers[key] = {
            "config_path": info["config_path"],
            "config": info["config"],
            # Canonical freshness/upload target for this workflow.
            "pdf_path": f"assets/pdfs/{pdf_filename}",
            # Keep build output path as fallback only.
            "build_pdf_path": info["pdf_path"],
            "pdf_filename": pdf_filename,
            "qmd_count": count_qmd_files(info["config"]),
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
    llm_pages: int = 5,
    use_cache: bool = True,
    skip_url_check: bool = True,
) -> tuple[bool, list[str], bool]:
    """Run pdf-validation.py with required LLM checks and local result caching.

    Returns (passed, errors, from_cache).
    """
    validation_script = PROJECT_ROOT / "scripts" / "pdf-validation.py"

    signature = _compute_pdf_signature(pdf_path)
    cache_key = _cache_key_for_pdf(pdf_path)
    cache = _load_validation_cache() if use_cache else _default_validation_cache()
    cache_entries = cache.setdefault("entries", {})

    if use_cache:
        cached = cache_entries.get(cache_key)
        if (
            isinstance(cached, dict)
            and cached.get("signature") == signature
            and int(cached.get("llm_pages", -1)) == llm_pages
            and bool(cached.get("llm_completed", False))
        ):
            cached_passed = bool(cached.get("passed", False))
            cached_errors = cached.get("errors", [])
            if not isinstance(cached_errors, list):
                cached_errors = []
            if verbose:
                cache_status = "PASSED" if cached_passed else "FAILED"
                print(f"  Using cached validation result ({cache_status}) for {pdf_path.name}", flush=True)
            return cached_passed, cached_errors, True

    if not os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY"):
        return False, ["GOOGLE_GENERATIVE_AI_API_KEY is not set (required for LLM PDF validation)."], False

    python_exe = _get_preferred_python()
    cmd = [python_exe, str(validation_script), "--pdf", str(pdf_path), "--llm-pages", str(llm_pages)]
    if skip_url_check:
        cmd.append("--skip-url-check")
    if verbose:
        print(f"  Running: {' '.join(cmd)}", flush=True)

    result = subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    output = result.stdout or ""
    if verbose and output:
        print(output, flush=True)

    errors = _extract_validation_errors(output)
    llm_errors = [e for e in errors if "LLM_" in e]
    non_llm_errors = [e for e in errors if "LLM_" not in e]

    llm_skipped = "LLM validation skipped" in output
    llm_failed = "LLM validation failed for page" in output
    llm_completed = not (llm_skipped or llm_failed)

    if llm_skipped:
        non_llm_errors.append("LLM validation was skipped; uploads require completed LLM validation.")
    if llm_failed:
        non_llm_errors.append("LLM validation failed for one or more pages; rerun after fixing model/API issues.")

    # Gate uploads on both deterministic checks and LLM findings.
    all_errors = list(non_llm_errors) + list(llm_errors)
    passed = llm_completed and not all_errors

    if not passed and not all_errors:
        all_errors.append(f"Validation failed with exit code {result.returncode}")

    if use_cache:
        cache_entries[cache_key] = {
            "signature": signature,
            "validated_at": datetime.now().isoformat(),
            "llm_pages": llm_pages,
            "llm_completed": llm_completed,
            "passed": passed,
            "errors": all_errors,
            "llm_warnings": llm_errors,
            "returncode": result.returncode,
        }
        _save_validation_cache(cache)

    return passed, all_errors, False


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
        python_exe = _get_preferred_python()
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
        for line in process.stdout:
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


def save_report(report_data: dict, start_time: float) -> Path:
    """Generate and save report to project root.

    Returns the path to the saved report.
    """
    report_data['total_duration'] = time.time() - start_time
    report_path = PROJECT_ROOT / "zenodo-upload-report.md"
    report_path.write_text(generate_report(report_data), encoding='utf-8')
    print(f"\nReport saved to: {report_path}")
    return report_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch upload papers to Zenodo with validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python scripts/upload-all-zenodo-and-save-dois.py
  python scripts/upload-all-zenodo-and-save-dois.py economics iab
  python scripts/upload-all-zenodo-and-save-dois.py --verbose
  python scripts/upload-all-zenodo-and-save-dois.py economics
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
        "--llm-pages",
        type=int,
        default=5,
        help="Number of pages to sample in LLM PDF validation (default: 5)",
    )
    parser.add_argument(
        "--force-revalidate",
        action="store_true",
        help="Ignore cached PDF validation results and run validation again",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Initialize report data
    report_data = {
        'timestamp': timestamp,
        'papers_count': 0,
        'success_count': 0,
        'failed_count': 0,
        'build_results': {},
        'validation_results': {},
        'upload_results': {},
        'errors': {},
        'total_duration': 0,
    }

    load_dotenv(PROJECT_ROOT / ".env")

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

    print("Papers to process (sorted by size, smallest first):")
    for key in sorted_keys:
        print(f"  {key}: {papers[key]['qmd_count']} QMD files")
    print()

    assets_pdf_dir = PROJECT_ROOT / "assets" / "pdfs"
    assets_pdf_dir.mkdir(parents=True, exist_ok=True)

    # Unified flow: for each paper, get the freshest PDF available
    # 1. Local PDF newer than sources → use it (skip everything)
    # 2. Remote published PDF available → download it (skip rebuild)
    # 3. Neither fresh → rebuild locally
    print("Getting freshest PDFs...")
    for paper_key in sorted_keys:
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
                print(f"\nFATAL: Build failed for {paper_key}")
                report_data['errors'][paper_key] = build_result['errors']
                report_data['failed_count'] += 1
                save_report(report_data, start_time)
                return 1

            if not pdf_path.exists():
                print(f"\nFATAL: PDF not found after build: {pdf_path}")
                report_data['errors'][paper_key] = ["PDF not found after build"]
                report_data['failed_count'] += 1
                save_report(report_data, start_time)
                return 1

    # Validate all PDFs before starting uploads (prevents partial uploads).
    print("\nRunning required PDF validation (LLM enabled, cached by file signature)...")
    if args.force_revalidate:
        print("  Validation cache: disabled (--force-revalidate)")
    else:
        print(f"  Validation cache: {PDF_VALIDATION_CACHE_PATH.relative_to(PROJECT_ROOT)}")

    validation_failed_keys = []

    for paper_key in sorted_keys:
        info = papers[paper_key]
        pdf_path = PROJECT_ROOT / info["pdf_path"]

        if not pdf_path.exists():
            fallback_pdf = PROJECT_ROOT / info["build_pdf_path"]
            if fallback_pdf.exists():
                print(f"[WARN] Using fallback build PDF for validation: {fallback_pdf}")
                pdf_path = fallback_pdf

        if not pdf_path.exists():
            print(f"\nFATAL: PDF not found for validation: {pdf_path}")
            validation_errors = ["PDF not found for validation"]
            report_data['validation_results'][paper_key] = {
                'success': False,
                'from_cache': False,
                'notes': 'PDF not found',
                'errors': validation_errors,
            }
            report_data['errors'][paper_key] = validation_errors
            validation_failed_keys.append(paper_key)
            report_data['failed_count'] += 1
            continue

        print(f"\n[VALIDATE] {paper_key}: {pdf_path.name}")
        passed, validation_errors, from_cache = validate_existing_pdf(
            pdf_path=pdf_path,
            verbose=args.verbose,
            llm_pages=args.llm_pages,
            use_cache=not args.force_revalidate,
        )

        source_note = "cache hit" if from_cache else "fresh run"
        if passed:
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
        }

        if passed:
            print(f"[OK] Validation passed for {paper_key} ({source_note})")
            continue

        print(f"\nFATAL: Validation failed for {paper_key}")
        for error in validation_errors[:10]:
            print(f"  - {error}")
        if len(validation_errors) > 10:
            print(f"  - ...and {len(validation_errors) - 10} more")

        report_data['errors'][paper_key] = validation_errors or ["PDF validation failed"]
        validation_failed_keys.append(paper_key)
        report_data['failed_count'] += 1

    if validation_failed_keys:
        failed_list = ", ".join(validation_failed_keys)
        print(f"\nFATAL: Validation failed for {len(validation_failed_keys)} paper(s): {failed_list}")
        save_report(report_data, start_time)
        return 1

    # Upload each paper (same order as build, fail-fast on errors)
    for paper_key in sorted_keys:
        info = papers[paper_key]
        pdf_path = PROJECT_ROOT / info["pdf_path"]
        if not pdf_path.exists():
            fallback_pdf = PROJECT_ROOT / info["build_pdf_path"]
            if fallback_pdf.exists():
                print(f"[WARN] Using fallback build PDF for upload: {fallback_pdf}")
                pdf_path = fallback_pdf
        result = upload_paper(
            client=client,
            paper_key=paper_key,
            quarto_config=info["config"],
            pdf_path=pdf_path,
            draft=True,
            verbose=True,
            save_doi=True,
            config_path=info["config_path"],
        )

        report_data['upload_results'][paper_key] = result

        if not result or not result.get("verified"):
            print(f"\nFATAL: Upload failed for {paper_key}")
            print("  -> Stopping to prevent partial uploads")
            print("  -> Fix the issue and re-run the script")

            if paper_key not in report_data['errors']:
                report_data['errors'][paper_key] = []
            report_data['errors'][paper_key].append("Upload verification failed")
            report_data['failed_count'] += 1

            save_report(report_data, start_time)
            return 1

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary")
    print("=" * 60)

    success, failed = [], []
    for key, result in report_data['upload_results'].items():
        if result and result.get("verified"):
            success.append(key)
            print(f"  {key}: OK - DOI: {result.get('doi', 'N/A')}")
            report_data['success_count'] += 1
        else:
            failed.append(key)
            print(f"  {key}: FAILED")
            report_data['failed_count'] += 1

    if success:
        print(f"\nUpdated {len(success)} config(s). Next steps:")
        print("  1. git diff _quarto-*.yml")
        print("  2. Review drafts on Zenodo")
        print("  3. git add _quarto-*.yml && git commit -m 'update: Zenodo DOIs'")

    # Generate final report
    save_report(report_data, start_time)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
