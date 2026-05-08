#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update title/abstract/tags of existing OSF preprints to match local config.

Reads each _quarto-*.yml that has an OSF preprint URL recorded under
publishing.preprints.osf.id, extracts corrected metadata using the same
logic as upload-all-osf-and-save-urls.py, and PATCHes the OSF preprint.

Usage:
    python scripts/sync-osf-metadata.py                        # update all
    python scripts/sync-osf-metadata.py 1-pct-treaty-impact    # specific paper
    python scripts/sync-osf-metadata.py --dry-run              # show what would change
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import requests
import yaml
from lib.quarto_config_utils import discover_paper_configs
from lib.python_utils import load_project_dotenv

# Reuse the metadata extractor and stripper from the upload script (hyphenated filename)
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    "osf_upload_module",
    str(Path(__file__).parent / "upload-all-osf-and-save-urls.py"),
)
upload_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(upload_mod)


PROJECT_ROOT = Path(__file__).parent.parent
OSF_API = "https://api.osf.io/v2"


def get_osf_id_from_config(config_path: Path) -> str | None:
    """Extract OSF preprint ID from a config's publishing.preprints.osf entry."""
    text = config_path.read_text(encoding="utf-8")
    cfg = yaml.safe_load(text) or {}
    pubs = ((cfg.get("metadata") or {}).get("publishing") or {}).get("preprints") or []
    for p in pubs:
        if p.get("platform") == "osf" and p.get("id"):
            return p["id"]
    return None


def patch_preprint(token: str, preprint_id: str, title: str, abstract: str, tags: list[str]) -> None:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json",
    }
    payload = {
        "data": {
            "type": "preprints",
            "id": preprint_id,
            "attributes": {
                "title": title,
                "description": abstract[:5000],
                "tags": tags[:10],
            },
        }
    }
    r = requests.patch(f"{OSF_API}/preprints/{preprint_id}/", headers=headers, json=payload, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"PATCH {preprint_id} -> {r.status_code}: {r.text[:400]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("papers", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_project_dotenv(PROJECT_ROOT)
    token = os.environ.get("OSF_TOKEN")
    if not token:
        print("[ERROR] OSF_TOKEN not set")
        return 1

    papers = discover_paper_configs(PROJECT_ROOT)
    if args.papers:
        papers = {k: v for k, v in papers.items() if k in args.papers}

    print(f"Checking {len(papers)} paper config(s)...\n", flush=True)
    ok, fail, skip = 0, 0, 0
    for key, info in papers.items():
        cfg_path = info["config_path"]
        osf_id = get_osf_id_from_config(cfg_path)
        if not osf_id:
            print(f"=== {key} ===  [SKIP] no OSF id in config", flush=True)
            skip += 1
            continue
        print(f"=== {key} ===  ({osf_id})", flush=True)
        try:
            meta = upload_mod.get_paper_metadata(key, info)
            title = meta["title"]
            abstract = meta["abstract"]
            tags = meta["tags"]
            print(f"  Title:    {title[:80]}", flush=True)
            print(f"  Abstract: {abstract[:120]}...", flush=True)
            if args.dry_run:
                print(f"  [DRY-RUN] would PATCH {osf_id}", flush=True)
                continue
            patch_preprint(token, osf_id, title, abstract, tags)
            print(f"  [OK] updated", flush=True)
            ok += 1
        except Exception as e:
            print(f"  [FAIL] {e}", flush=True)
            fail += 1

    print(f"\n=== Summary ===\n  OK: {ok}  Fail: {fail}  Skip: {skip}", flush=True)
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
