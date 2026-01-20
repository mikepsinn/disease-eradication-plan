#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Upload All Papers to Zenodo

Rebuilds all PDFs and uploads them to Zenodo, saving DOIs to config files.

Usage:
    python scripts/upload-all-zenodo-and-save-dois.py
    python scripts/upload-all-zenodo-and-save-dois.py economics iab  # specific papers only
    python scripts/upload-all-zenodo-and-save-dois.py --verbose      # show full build output

Environment:
    ZENODO_TOKEN: API token from https://zenodo.org/account/settings/applications/
"""

from __future__ import annotations

import sys
import subprocess
import io
import shutil
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

PROJECT_ROOT = Path(__file__).parent.parent
SKIP_CONFIGS = {"manual", "test", "main", "base"}


def count_qmd_files(config: dict) -> int:
    """Count QMD files referenced in a Quarto config."""
    count = 0

    def count_items(items):
        """Recursively count QMD files in chapter/render list."""
        nonlocal count
        if not items:
            return
        for item in items:
            if isinstance(item, str):
                if item.endswith('.qmd'):
                    count += 1
            elif isinstance(item, dict):
                if 'href' in item and item['href'].endswith('.qmd'):
                    count += 1
                # Recurse into nested structures
                for key in ('chapters', 'contents', 'parts'):
                    if key in item:
                        count_items(item[key])

    # Check book.chapters (book type)
    book = config.get('book', {})
    if book.get('chapters'):
        count_items(book['chapters'])

    # Check project.render (website type)
    project = config.get('project', {})
    if project.get('render'):
        count_items(project['render'])

    return count


def discover_papers() -> dict:
    """Find all Quarto paper configs."""
    papers = {}
    for config_path in PROJECT_ROOT.glob("_quarto-*.yml"):
        key = config_path.stem.replace("_quarto-", "")
        if not key or key == "quarto" or key in SKIP_CONFIGS:
            continue

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"WARNING: Could not read {config_path}: {e}")
            continue

        dih_render = config.get("dih-render", {})
        if dih_render.get("zenodo") is False:
            continue

        pdf_filename = dih_render.get("pdf-output-file")
        if not pdf_filename:
            pdf_config = config.get("format", {}).get("pdf", {})
            pdf_filename = pdf_config.get("output-file", f"{key}-paper.pdf")

        qmd_count = count_qmd_files(config)
        papers[key] = {
            "config_path": config_path,
            "config": config,
            "pdf_path": f"_build_temp/{key}/_site/{key}/{pdf_filename}",
            "qmd_count": qmd_count,
        }
    return papers


def rebuild_paper(paper_key: str, verbose: bool = False) -> bool:
    """Rebuild a paper using render-quarto.py."""
    print(f"\n[*] Building {paper_key}...", flush=True)
    render_script = PROJECT_ROOT / "scripts" / "render-quarto.py"

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

        if process.returncode == 0:
            print(f"[OK] Built {paper_key}", flush=True)
            return True
        print(f"ERROR: Build failed for {paper_key}", flush=True)
        return False
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"ERROR: Build timeout for {paper_key}", flush=True)
        return False
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        return False


def main():
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

    # Parse args
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Filter to specific papers if args provided
    if args:
        requested = set(args)
        papers = {k: v for k, v in papers.items() if k in requested}
        if not papers:
            print(f"ERROR: No matching papers: {', '.join(requested)}")
            return 1

    # Sort papers by QMD file count (smallest first for faster feedback)
    sorted_keys = sorted(papers.keys(), key=lambda k: papers[k]["qmd_count"])

    print("Papers to upload (sorted by size, smallest first):")
    for key in sorted_keys:
        print(f"  {key}: {papers[key]['qmd_count']} QMD files")
    print()

    # Build all PDFs first (fail fast if any build fails)
    print("Building PDFs (smallest first)...")
    assets_pdf_dir = PROJECT_ROOT / "assets" / "pdfs"
    assets_pdf_dir.mkdir(parents=True, exist_ok=True)

    for paper_key in sorted_keys:
        info = papers[paper_key]
        if not rebuild_paper(paper_key, verbose=verbose):
            print(f"\nFATAL: Build failed for {paper_key}")
            return 1

        pdf_path = PROJECT_ROOT / info["pdf_path"]
        if not pdf_path.exists():
            print(f"\nFATAL: PDF not found after build: {pdf_path}")
            return 1

        # Copy PDF to assets/pdfs/
        dest_path = assets_pdf_dir / pdf_path.name
        shutil.copy2(pdf_path, dest_path)
        print(f"  -> Copied to: assets/pdfs/{pdf_path.name}")

    # Upload each paper (same order as build, fail-fast on errors)
    results = {}
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

        if not result or not result.get("verified"):
            print(f"\nFATAL: Upload failed for {paper_key}")
            print("  -> Stopping to prevent partial uploads")
            print("  -> Fix the issue and re-run the script")
            return 1

        results[paper_key] = result

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary")
    print("=" * 60)

    success, failed = [], []
    for key, result in results.items():
        if result and result.get("verified"):
            success.append(key)
            print(f"  {key}: OK - DOI: {result.get('doi', 'N/A')}")
        else:
            failed.append(key)
            print(f"  {key}: FAILED")

    if success:
        print(f"\nUpdated {len(success)} config(s). Next steps:")
        print("  1. git diff _quarto-*.yml")
        print("  2. Review drafts on Zenodo")
        print("  3. git add _quarto-*.yml && git commit -m 'update: Zenodo DOIs'")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
