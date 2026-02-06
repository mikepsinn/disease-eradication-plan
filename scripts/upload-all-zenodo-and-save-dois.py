#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Upload All Papers to Zenodo

Rebuilds all PDFs and uploads them to Zenodo, saving DOIs to config files.

Usage:
    python scripts/upload-all-zenodo-and-save-dois.py
    python scripts/upload-all-zenodo-and-save-dois.py economics iab  # specific papers only
    python scripts/upload-all-zenodo-and-save-dois.py --verbose      # show full build output
    python scripts/upload-all-zenodo-and-save-dois.py --no-rebuild   # validate and upload existing PDFs

Environment:
    ZENODO_TOKEN: API token from https://zenodo.org/account/settings/applications/
"""

from __future__ import annotations

import argparse
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
    import yaml
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Missing dependency. Run: pip install pyyaml python-dotenv")
    sys.exit(1)

from lib.zenodo_client import ZenodoClient, upload_paper, get_zenodo_token
from lib.quarto_config_utils import discover_paper_configs, count_qmd_files

PROJECT_ROOT = Path(__file__).parent.parent


def generate_report(report_data: dict) -> str:
    """Generate markdown report from upload run data."""
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
                deposit_id = result.get('deposit_id', 'N/A')
                url = result.get('bucket_url', 'N/A')
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
        papers[key] = {
            "config_path": info["config_path"],
            "config": info["config"],
            "pdf_path": info["pdf_path"],
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


def validate_existing_pdf(pdf_path: Path, verbose: bool = False) -> bool:
    """Run pdf-validation.py on an existing PDF as a gate before upload.

    Returns True if validation passes (no critical errors).
    """
    validation_script = PROJECT_ROOT / "scripts" / "pdf-validation.py"
    cmd = [
        sys.executable, str(validation_script),
        "--pdf", str(pdf_path),
        "--skip-llm",
        "--skip-url-check",
    ]
    if verbose:
        print(f"  Running: {' '.join(cmd)}", flush=True)

    result = subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        capture_output=not verbose,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode == 0


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
        process = subprocess.Popen(
            [sys.executable, "-u", str(render_script), paper_key],
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


def save_report(report_data: dict) -> Path:
    """Generate and save report to _analysis/zenodo-upload-report.md.

    Returns the path to the saved report.
    """
    report_dir = PROJECT_ROOT / "_analysis"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "zenodo-upload-report.md"
    report_path.write_text(generate_report(report_data), encoding='utf-8')
    return report_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch upload papers to Zenodo with validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python scripts/upload-all-zenodo-and-save-dois.py
  python scripts/upload-all-zenodo-and-save-dois.py economics iab
  python scripts/upload-all-zenodo-and-save-dois.py --no-rebuild --verbose
  python scripts/upload-all-zenodo-and-save-dois.py --no-rebuild economics""",
    )
    parser.add_argument(
        "papers", nargs="*",
        help="Specific paper keys to upload (default: all papers)",
    )
    parser.add_argument(
        "--no-rebuild", action="store_true",
        help="Skip rebuild; validate and upload existing PDFs",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show full build/validation output",
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

    mode_label = "validate-only" if args.no_rebuild else "rebuild"
    print(f"Mode: {mode_label}")
    print("Papers to upload (sorted by size, smallest first):")
    for key in sorted_keys:
        print(f"  {key}: {papers[key]['qmd_count']} QMD files")
    print()

    assets_pdf_dir = PROJECT_ROOT / "assets" / "pdfs"
    assets_pdf_dir.mkdir(parents=True, exist_ok=True)

    if args.no_rebuild:
        # --no-rebuild: validate existing PDFs without rebuilding
        print("Validating existing PDFs (--no-rebuild)...")
        for paper_key in sorted_keys:
            info = papers[paper_key]
            pdf_path = PROJECT_ROOT / info["pdf_path"]

            if not pdf_path.exists():
                print(f"\nFATAL: PDF not found: {pdf_path}")
                report_data['errors'][paper_key] = [f"PDF not found: {pdf_path}"]
                report_data['failed_count'] += 1
                report_data['total_duration'] = time.time() - start_time
                report_path = save_report(report_data)
                print(f"\nReport saved to: {report_path}")
                return 1

            pdf_size_mb = pdf_path.stat().st_size / (1024 * 1024)
            page_count = get_pdf_page_count(pdf_path)

            print(f"\n[*] Validating {paper_key} ({pdf_size_mb:.1f} MB, {page_count or '?'} pages)...", flush=True)

            if not validate_existing_pdf(pdf_path, verbose=args.verbose):
                print(f"FATAL: PDF validation failed for {paper_key}")
                report_data['errors'][paper_key] = ["PDF validation failed (critical errors)"]
                report_data['failed_count'] += 1
                report_data['total_duration'] = time.time() - start_time
                report_path = save_report(report_data)
                print(f"\nReport saved to: {report_path}")
                return 1

            print(f"[OK] Validated {paper_key}", flush=True)

            report_data['build_results'][paper_key] = {
                'success': True,
                'duration_seconds': 0,
                'errors': [],
                'qmd_count': info['qmd_count'],
                'pdf_size': f"{pdf_size_mb:.2f} MB",
                'pages': page_count,
            }

            # Copy PDF to assets/pdfs/
            dest_path = assets_pdf_dir / pdf_path.name
            shutil.copy2(pdf_path, dest_path)
            print(f"  -> Copied to: assets/pdfs/{pdf_path.name}")
    else:
        # Default: rebuild all PDFs (fail fast if any build fails)
        print("Building PDFs (smallest first)...")
        for paper_key in sorted_keys:
            info = papers[paper_key]
            build_result = rebuild_paper(paper_key, verbose=args.verbose)

            # Store build result with additional metadata
            pdf_path = PROJECT_ROOT / info["pdf_path"]
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
                report_data['total_duration'] = time.time() - start_time
                report_path = save_report(report_data)
                print(f"\nReport saved to: {report_path}")
                return 1

            if not pdf_path.exists():
                print(f"\nFATAL: PDF not found after build: {pdf_path}")
                report_data['errors'][paper_key] = ["PDF not found after build"]
                report_data['failed_count'] += 1
                report_data['total_duration'] = time.time() - start_time
                report_path = save_report(report_data)
                print(f"\nReport saved to: {report_path}")
                return 1

            # Copy PDF to assets/pdfs/
            dest_path = assets_pdf_dir / pdf_path.name
            shutil.copy2(pdf_path, dest_path)
            print(f"  -> Copied to: assets/pdfs/{pdf_path.name}")

    # Upload each paper (same order as build, fail-fast on errors)
    for paper_key in sorted_keys:
        info = papers[paper_key]
        pdf_path = PROJECT_ROOT / info["pdf_path"]
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

            report_data['total_duration'] = time.time() - start_time
            report_path = save_report(report_data)
            print(f"\nReport saved to: {report_path}")
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
    report_data['total_duration'] = time.time() - start_time
    report_path = save_report(report_data)
    print(f"\nReport saved to: {report_path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
