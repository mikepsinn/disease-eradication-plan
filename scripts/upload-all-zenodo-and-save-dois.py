#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Upload All Papers to Zenodo

Rebuilds all PDFs and uploads them to Zenodo, saving DOIs to config files.

Usage:
    python scripts/upload-all-zenodo-and-save-dois.py
    python scripts/upload-all-zenodo-and-save-dois.py economics iab  # specific papers only

Environment:
    ZENODO_TOKEN: API token from https://zenodo.org/account/settings/applications/
"""

from __future__ import annotations

import sys
import subprocess
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    import yaml
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Missing dependency. Run: pip install pyyaml python-dotenv")
    sys.exit(1)

from zenodo_client import ZenodoClient, upload_paper, get_zenodo_token

PROJECT_ROOT = Path(__file__).parent.parent
SKIP_CONFIGS = {"book", "test", "main", "base"}


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

        papers[key] = {
            "config_path": config_path,
            "config": config,
            "pdf_path": f"_build_temp/{key}/_site/{key}/{pdf_filename}",
        }
    return papers


def rebuild_paper(paper_key: str) -> bool:
    """Rebuild a paper using render-quarto.py."""
    print(f"\n[*] Building {paper_key}...")
    render_script = PROJECT_ROOT / "scripts" / "render-quarto.py"

    try:
        result = subprocess.run(
            [sys.executable, str(render_script), paper_key],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=600
        )
        if result.returncode == 0:
            print(f"[OK] Built {paper_key}")
            return True
        print(f"ERROR: Build failed for {paper_key}")
        print(result.stderr)
        return False
    except subprocess.TimeoutExpired:
        print(f"ERROR: Build timeout for {paper_key}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
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

    # Filter to specific papers if args provided
    if len(sys.argv) > 1:
        requested = set(sys.argv[1:])
        papers = {k: v for k, v in papers.items() if k in requested}
        if not papers:
            print(f"ERROR: No matching papers: {', '.join(requested)}")
            return 1

    print(f"Papers to upload: {', '.join(sorted(papers.keys()))}\n")

    # Build all PDFs first
    print("Building PDFs...")
    for paper_key in papers:
        rebuild_paper(paper_key)

    # Upload each paper
    results = {}
    for paper_key, info in papers.items():
        pdf_path = PROJECT_ROOT / info["pdf_path"]
        results[paper_key] = upload_paper(
            client=client,
            paper_key=paper_key,
            quarto_config=info["config"],
            pdf_path=pdf_path,
            draft=True,
            verbose=True,
            save_doi=True,
            config_path=info["config_path"],
        )

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary")
    print("=" * 60)

    success, failed, skipped = [], [], []
    for key, result in results.items():
        pdf_path = PROJECT_ROOT / papers[key]["pdf_path"]
        if not pdf_path.exists():
            skipped.append(key)
            print(f"  {key}: SKIPPED (no PDF)")
        elif result and result.get("verified"):
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
