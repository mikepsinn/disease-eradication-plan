#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publish all pending Zenodo drafts in your account.

By default, fetches all drafts owned by the authenticated user and publishes
each one. Pass specific deposit IDs as args to publish only those.

Usage:
    python scripts/publish-zenodo-drafts.py                        # publish all your drafts
    python scripts/publish-zenodo-drafts.py 20076883 20076884      # specific IDs
    python scripts/publish-zenodo-drafts.py --dry-run              # list only, don't publish
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

import requests
from lib.zenodo_client import ZenodoClient, get_zenodo_token
from lib.python_utils import load_project_dotenv


def list_user_drafts(client: ZenodoClient) -> list[dict]:
    """Return all drafts (unsubmitted depositions) owned by the user."""
    drafts = []
    page = 1
    while True:
        url = f"{client.base_url}/deposit/depositions"
        params = {"status": "draft", "size": 100, "page": page}
        resp = requests.get(url, params=params, headers=client.headers, timeout=30)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        drafts.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return drafts


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish Zenodo drafts")
    parser.add_argument("ids", nargs="*", type=int, help="Specific deposit IDs (default: all your drafts)")
    parser.add_argument("--dry-run", action="store_true", help="List only, don't publish")
    args = parser.parse_args()

    load_project_dotenv(Path(__file__).parent.parent)
    token = get_zenodo_token()
    if not token:
        print("[ERROR] ZENODO_TOKEN not set in .env")
        return 1
    client = ZenodoClient(token)

    if args.ids:
        targets = args.ids
        print(f"Targeting {len(targets)} specified deposit ID(s)")
    else:
        print("Fetching all drafts in your account...")
        drafts = list_user_drafts(client)
        targets = [d["id"] for d in drafts]
        print(f"Found {len(targets)} draft(s)")
        for d in drafts:
            title = d.get("title") or d.get("metadata", {}).get("title") or "(untitled)"
            print(f"  {d['id']}: {title[:80]}")

    if not targets:
        print("Nothing to publish.")
        return 0

    if args.dry_run:
        print("\n[DRY-RUN] Would publish the IDs above. Re-run without --dry-run to apply.")
        return 0

    print(f"\nPublishing {len(targets)} draft(s)...")
    ok, fail = 0, 0
    for did in targets:
        try:
            result = client.publish(did)
            doi = result.get("doi") or result.get("metadata", {}).get("doi") or "(no doi)"
            url = (result.get("links", {}) or {}).get("html") or ""
            print(f"  [OK] {did}  doi={doi}  {url}")
            ok += 1
        except Exception as e:
            msg = str(e)
            response = getattr(e, "response", None)
            if response is not None:
                try:
                    body = response.json()
                    msg = f"{response.status_code} {body}"
                except Exception:
                    msg = f"{response.status_code} {response.text[:200]}"
            print(f"  [FAIL] {did}: {msg}")
            fail += 1

    print(f"\nDone. Published: {ok}   Failed: {fail}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
