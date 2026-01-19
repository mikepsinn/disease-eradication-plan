#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Upload All Papers to Zenodo and Save DOIs

This script:
1. Discovers all Quarto paper configs (_quarto-*.yml)
2. Checks if PDFs exist (optionally rebuilds them)
3. Uploads each PDF to Zenodo (creates drafts by default)
4. Verifies uploads with GET requests
5. Saves DOIs back to config files
6. Updates publication tracking status
7. Shows summary of what was uploaded and updated

After running, you can review the config changes and commit them to git.

Usage:
    # Upload all papers as drafts and save DOIs (default)
    python scripts/upload-all-zenodo-and-save-dois.py

    # Rebuild PDFs before uploading
    python scripts/upload-all-zenodo-and-save-dois.py --rebuild

    # Use Zenodo sandbox for testing
    python scripts/upload-all-zenodo-and-save-dois.py --sandbox

    # Publish immediately (not recommended - use drafts for review)
    python scripts/upload-all-zenodo-and-save-dois.py --publish

    # Upload specific papers only
    python scripts/upload-all-zenodo-and-save-dois.py --papers economics iab dfda-impact

Environment variables:
    ZENODO_TOKEN: API token for Zenodo (required)
    ZENODO_SANDBOX_TOKEN: API token for Zenodo sandbox (optional, for testing)
"""

from __future__ import annotations

import sys
import argparse
import subprocess
import io
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    import yaml
    from dotenv import load_dotenv
except ImportError as e:
    print(f"ERROR: Missing dependency. Run: pip install pyyaml python-dotenv")
    sys.exit(1)

from zenodo_client import (
    ZenodoClient,
    upload_paper,
    get_zenodo_token,
    load_quarto_config,
)

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Skip these configs (not papers)
SKIP_CONFIGS = {"book", "test", "main", "base"}


def discover_papers() -> dict:
    """
    Auto-discover Quarto paper configs from _quarto-*.yml files.

    Returns dict mapping paper key to config info.
    """
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

        # Get PDF filename
        pdf_filename = dih_render.get("pdf-output-file")
        if not pdf_filename:
            format_config = config.get("format", {})
            pdf_config = format_config.get("pdf", {})
            pdf_filename = pdf_config.get("output-file", f"{key}-paper.pdf")

        pdf_path = f"_build_temp/{key}/_site/{key}/{pdf_filename}"

        papers[key] = {
            "quarto_config_path": config_path,
            "quarto_config": config,
            "pdf_path": pdf_path,
            "pdf_filename": pdf_filename,
        }

    return papers


def rebuild_paper(paper_key: str) -> bool:
    """
    Rebuild a paper using render-quarto.py.

    Args:
        paper_key: Paper identifier (e.g., "economics")

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[*] Rebuilding {paper_key}...")
    render_script = PROJECT_ROOT / "scripts" / "render-quarto.py"

    if not render_script.exists():
        print(f"ERROR: render-quarto.py not found at {render_script}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(render_script), paper_key],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=600  # 10 minutes max
        )

        if result.returncode == 0:
            print(f"[OK] Rebuilt {paper_key}")
            return True
        else:
            print(f"ERROR: Failed to rebuild {paper_key}")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"ERROR: Rebuild timeout for {paper_key}")
        return False
    except Exception as e:
        print(f"ERROR: Could not rebuild {paper_key}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Batch upload all papers to Zenodo and save DOIs to configs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild PDFs before uploading",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo sandbox for testing",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish immediately (default: create drafts for review)",
    )
    parser.add_argument(
        "--papers",
        nargs="+",
        help="Upload specific papers only (default: all)",
    )

    args = parser.parse_args()

    # Load .env file if present
    load_dotenv(PROJECT_ROOT / ".env")

    # Get API token
    token = get_zenodo_token(sandbox=args.sandbox)
    if not token:
        env_var = "ZENODO_SANDBOX_TOKEN" if args.sandbox else "ZENODO_TOKEN"
        print(f"ERROR: {env_var} environment variable not set")
        print(f"  Get token at: https://{'sandbox.' if args.sandbox else ''}zenodo.org/account/settings/applications/")
        return 1

    client = ZenodoClient(token, sandbox=args.sandbox)

    env_name = "SANDBOX" if args.sandbox else "PRODUCTION"
    print(f"{'='*60}")
    print(f"Zenodo Batch Upload - {env_name}")
    print(f"{'='*60}")
    print(f"API: {client.base_url}")
    print()

    # Discover papers
    papers = discover_papers()
    if not papers:
        print("ERROR: No Quarto paper configs found (_quarto-*.yml)")
        return 1

    # Filter to specific papers if requested
    if args.papers:
        papers = {k: v for k, v in papers.items() if k in args.papers}
        if not papers:
            print(f"ERROR: No matching papers found for: {', '.join(args.papers)}")
            return 1

    print(f"Found {len(papers)} paper(s) to upload:")
    for key in sorted(papers.keys()):
        print(f"  - {key}")
    print()

    # Rebuild PDFs if requested
    if args.rebuild:
        print("Rebuilding PDFs...")
        for paper_key in papers.keys():
            if not rebuild_paper(paper_key):
                print(f"WARNING: Failed to rebuild {paper_key}, will try to upload existing PDF")
        print()

    # Upload each paper
    results = {}
    for paper_key, paper_config in papers.items():
        pdf_path = PROJECT_ROOT / paper_config["pdf_path"]

        result = upload_paper(
            client=client,
            paper_key=paper_key,
            quarto_config=paper_config["quarto_config"],
            pdf_path=pdf_path,
            draft=not args.publish,
            verbose=True,
            save_doi=True,  # Save DOI to config
            config_path=paper_config["quarto_config_path"],
        )

        results[paper_key] = result

    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")

    updated_configs = []
    failed = []
    skipped = []

    for paper_key, result in results.items():
        pdf_path = PROJECT_ROOT / papers[paper_key]["pdf_path"]

        if not pdf_path.exists():
            status = "[SKIP] PDF not found"
            skipped.append(paper_key)
        elif result is None:
            status = "[FAIL] Upload failed"
            failed.append(paper_key)
        elif result.get("verified"):
            doi = result.get("doi", "N/A")
            status = f"[OK] Uploaded - DOI: {doi}"
            updated_configs.append(paper_key)
        else:
            status = "[WARN] Uploaded but not verified"

        print(f"  {paper_key}: {status}")

    print()

    if updated_configs:
        print(f"[OK] Updated {len(updated_configs)} config file(s) with DOIs:")
        for paper_key in updated_configs:
            config_path = papers[paper_key]["quarto_config_path"]
            print(f"  - {config_path.name}")

        print()
        print("Next steps:")
        print("  1. Review config changes: git diff _quarto-*.yml")
        print("  2. Review drafts on Zenodo (links above)")
        print("  3. Commit config changes: git add _quarto-*.yml && git commit -m 'update: Zenodo DOIs'")
        print("  4. Publish drafts manually on Zenodo when ready")

    if failed:
        print(f"\n[WARN] {len(failed)} upload(s) failed:")
        for paper_key in failed:
            print(f"  - {paper_key}")

    if skipped:
        print(f"\n[INFO] {len(skipped)} paper(s) skipped (no PDF):")
        for paper_key in skipped:
            print(f"  - {paper_key}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
