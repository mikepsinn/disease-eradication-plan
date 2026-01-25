#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zenodo Upload Script

Uploads Quarto-generated PDFs to Zenodo as drafts.
Reads metadata from _quarto-*.yml files and creates drafts with proper academic metadata.
You publish manually on Zenodo when ready (https://zenodo.org/me/uploads).

Usage:
    python scripts/publish-zenodo.py --draft            # Upload all papers as drafts
    python scripts/publish-zenodo.py --draft --paper iab  # Upload specific paper
    python scripts/publish-zenodo.py --dry-run          # Show what would be uploaded

Environment variables:
    ZENODO_TOKEN: API token for Zenodo (required)
"""

from __future__ import annotations

import sys
import os
import json
import argparse
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
    extract_zenodo_metadata,
    upload_paper,
    get_zenodo_token,
    load_quarto_config,
    get_record_id_from_doi,
)
from quarto_config_utils import discover_paper_configs

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


def discover_papers() -> dict:
    """
    Auto-discover Quarto paper configs using shared discovery utility.

    Returns dict mapping paper key to config info.
    """
    raw_papers = discover_paper_configs(PROJECT_ROOT)

    papers = {}
    for key, info in raw_papers.items():
        # Look for bibliography file
        bib_file = f"references-{key}.bib"
        if not (PROJECT_ROOT / bib_file).exists():
            bib_file = f"{key}-references.bib"
            if not (PROJECT_ROOT / bib_file).exists():
                bib_file = None

        papers[key] = {
            "quarto_config": info["config_path"].name,
            "pdf_path": info["pdf_path"],
            "bib_file": bib_file,
            "resource_type": "publication-workingpaper",
        }

    return papers


def publish_paper_with_config(
    paper_key: str,
    paper_config: dict,
    client: Optional[ZenodoClient],
    dry_run: bool = False,
    skip_publish: bool = False,
) -> Optional[dict]:
    """
    Upload a paper to Zenodo using config dict.

    Args:
        paper_key: Short identifier for the paper
        paper_config: Config dict with quarto_config, pdf_path, etc.
        client: ZenodoClient instance (None for dry-run)
        dry_run: If True, show what would be uploaded without uploading
        skip_publish: If True, create draft without publishing

    Returns the deposit info if successful, None otherwise.
    """
    print(f"\n{'='*60}")
    print(f"Uploading: {paper_key}")
    print(f"{'='*60}")

    # Check if PDF exists
    pdf_path = PROJECT_ROOT / paper_config["pdf_path"]
    if not pdf_path.exists():
        print(f"WARNING: PDF not found at {pdf_path}")
        print("  -> Skipping (build the paper first)")
        return None

    print(f"[OK] PDF found: {pdf_path.name} ({pdf_path.stat().st_size / 1024:.1f} KB)")

    # Load Quarto config
    config_file = PROJECT_ROOT / paper_config["quarto_config"]
    quarto_config = load_quarto_config(config_file)
    metadata = extract_zenodo_metadata(quarto_config, paper_key)

    print(f"[OK] Title: {metadata['title']}")
    print(f"[OK] Authors: {', '.join(c['name'] for c in metadata['creators'])}")
    print(f"[OK] License: {metadata['license']}")
    print(f"[OK] Version: {metadata.get('version', 'N/A')}")

    if dry_run:
        print("\n[DRY RUN] Would upload with metadata:")
        print(json.dumps(metadata, indent=2))
        return None

    # Use shared upload function (with verification but no DOI saving)
    return upload_paper(
        client=client,
        paper_key=paper_key,
        quarto_config=quarto_config,
        pdf_path=pdf_path,
        draft=skip_publish,
        verbose=True,
        save_doi=False,  # Don't save DOI in CI - use local script instead
        config_path=None
    )


def main():
    # Discover papers first
    papers = discover_papers()

    if not papers:
        print("ERROR: No Quarto paper configs found (_quarto-*.yml)")
        return 1

    parser = argparse.ArgumentParser(
        description="Upload Quarto papers to Zenodo as drafts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--paper",
        choices=list(papers.keys()),
        help="Upload specific paper (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be uploaded without uploading",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Create draft without publishing (allows manual review)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_papers",
        help="List configured papers and exit",
    )

    args = parser.parse_args()

    if args.list_papers:
        print(f"Discovered {len(papers)} paper(s):")
        for key, config in sorted(papers.items()):
            bib_status = "[bib]" if config.get("bib_file") else ""
            print(f"  {key}: {config['quarto_config']} {bib_status}")
        return 0

    # Load .env file if present
    load_dotenv(PROJECT_ROOT / ".env")

    # Get API token (not required for dry-run)
    client = None
    if not args.dry_run:
        token = get_zenodo_token()
        if not token:
            print("ERROR: ZENODO_TOKEN environment variable not set")
            print("  Get token at: https://zenodo.org/account/settings/applications/")
            return 1
        client = ZenodoClient(token)

    print("Zenodo Environment: PRODUCTION")
    if client:
        print(f"API: {client.base_url}")
    else:
        print("API: (dry-run mode - no connection)")

    # Determine which papers to upload
    papers_to_upload = [args.paper] if args.paper else list(papers.keys())

    results = {}
    for paper_key in papers_to_upload:
        result = publish_paper_with_config(
            paper_key,
            papers[paper_key],
            client,
            dry_run=args.dry_run,
            skip_publish=args.draft,
        )
        results[paper_key] = result

    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")

    failed = False
    for paper_key, result in results.items():
        if result is None and not args.dry_run:
            # Check if PDF existed
            pdf_path = PROJECT_ROOT / papers[paper_key]["pdf_path"]
            if not pdf_path.exists():
                status = "[--] Skipped (no PDF)"
            else:
                status = "[ERROR] Failed"
                failed = True
        elif result:
            status = "[OK] Uploaded"
        else:
            status = "[--] Dry run"
        print(f"  {paper_key}: {status}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
