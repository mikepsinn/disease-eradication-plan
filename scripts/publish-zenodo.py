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
import re
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    import yaml
    import requests
    from dotenv import load_dotenv
except ImportError as e:
    print(f"ERROR: Missing dependency. Run: pip install pyyaml python-dotenv")
    sys.exit(1)

from zenodo_client import (
    ZenodoClient,
    extract_zenodo_metadata,
    upload_paper,
    get_zenodo_token,
    get_record_id_from_doi,
)
from quarto_config_utils import discover_paper_configs

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

ZENODO_RECORD_ID_MAP = {
    "1-pct-treaty-impact": 18161561,
    "iab": 18203222,
    "dfda-spec": 18203376,
    "wishocracy": 18205882,
    "dfda-impact": 18243915,
    "obg": 18356210,
    "opg": 18356212,
    "optimocracy": 18356214,
    "cost-of-change": 18356216,
    "invisible-graveyard": 18356232,
    "federal-efficiency-audit": 18447477,
    "political-dysfunction-tax": 18447494,
}


def _extract_numeric_id(value: str | None) -> Optional[int]:
    """Extract trailing numeric ID from arbitrary Zenodo link/identifier text."""
    if not value:
        return None
    match = re.search(r"(\d+)(?:/?$)", value)
    if not match:
        return None
    return int(match.group(1))


def resolve_record_id(paper_key: str, metadata: dict) -> Optional[int]:
    """Resolve existing published Zenodo record ID for version updates."""
    # Preferred source: explicit map supplied for published versions.
    if paper_key in ZENODO_RECORD_ID_MAP:
        return ZENODO_RECORD_ID_MAP[paper_key]

    # Fallback: parse DOI from config metadata.
    existing_doi = metadata.get("_existing_doi")
    return get_record_id_from_doi(existing_doi) if existing_doi else None


def _records_api_headers(client: ZenodoClient) -> dict:
    return {
        **client.headers,
        "Content-Type": "application/json",
    }


def create_version_draft_via_records_api(client: ZenodoClient, record_id: int) -> dict:
    """
    Create new draft version from a published record using Zenodo records API.
    Returns dict with `new_id`, `draft`, `bucket_url`.
    """
    response = requests.post(
        f"{client.base_url}/records/{record_id}/versions",
        headers=_records_api_headers(client),
        json={},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    # Prefer direct id in response, otherwise parse latest_draft link.
    new_id = data.get("id")
    latest_draft_url = data.get("links", {}).get("latest_draft")
    if not new_id and latest_draft_url:
        new_id = _extract_numeric_id(latest_draft_url)
    if not new_id:
        raise RuntimeError(f"Could not resolve new draft ID from /records/{record_id}/versions response")

    # Fetch draft details from records API.
    draft_url = latest_draft_url or f"{client.base_url}/records/{new_id}/draft"
    draft_resp = requests.get(draft_url, headers=client.headers, timeout=60)
    draft_resp.raise_for_status()
    draft = draft_resp.json()

    # Bucket URL may appear in different places depending on API shape.
    bucket_url = (
        draft.get("links", {}).get("bucket")
        or data.get("links", {}).get("bucket")
    )
    if not bucket_url:
        # Fallback to deposition endpoint for bucket details.
        deposit = client.get_deposit(new_id)
        bucket_url = deposit.get("links", {}).get("bucket")
    if not bucket_url:
        raise RuntimeError(f"Could not resolve bucket URL for draft {new_id}")

    return {
        "new_id": int(new_id),
        "draft": draft,
        "bucket_url": bucket_url,
    }


def publish_draft_via_records_api(client: ZenodoClient, draft_id: int) -> dict:
    """Publish draft via records API."""
    response = requests.post(
        f"{client.base_url}/records/{draft_id}/draft/actions/publish",
        headers=_records_api_headers(client),
        json={},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def verify_bucket_access(client: ZenodoClient, bucket_url: str) -> bool:
    """Check that bucket is reachable and writable-context endpoint is unlocked."""
    response = requests.get(bucket_url, headers=client.headers, timeout=60)
    return response.status_code == 200


def publish_paper_with_config(
    paper_key: str,
    paper_config: dict,
    client: Optional[ZenodoClient],
    dry_run: bool = False,
    skip_publish: bool = False,
    update_versions: bool = False,
) -> Optional[dict]:
    """
    Upload a paper to Zenodo using config dict.

    Args:
        paper_key: Short identifier for the paper
        paper_config: Config dict from discover_paper_configs()
        client: ZenodoClient instance (None for dry-run)
        dry_run: If True, show what would be uploaded without uploading
        skip_publish: If True, create draft without publishing

    Returns the deposit info if successful, None otherwise.
    """
    pdf_path = PROJECT_ROOT / paper_config["pdf_path"]
    config_file = paper_config["config_path"]
    quarto_config = paper_config["config"]

    if dry_run and not update_versions:
        metadata = extract_zenodo_metadata(quarto_config, paper_key)
        print(f"\n{'='*60}")
        print(f"[DRY RUN] {paper_key}")
        print(f"{'='*60}")
        print(f"PDF: {pdf_path} ({'exists' if pdf_path.exists() else 'MISSING'})")
        print(json.dumps(metadata, indent=2))
        return None

    if update_versions:
        if client is None:
            print("ERROR: update-versions requires a Zenodo client")
            return None

        metadata = extract_zenodo_metadata(quarto_config, paper_key)
        record_id = resolve_record_id(paper_key, metadata)

        print(f"\n{'='*60}")
        mode_label = "VERSION UPDATE DRY RUN" if dry_run else "VERSION UPDATE"
        print(f"[{mode_label}] {paper_key}")
        print(f"{'='*60}")
        print(f"PDF: {pdf_path} ({'exists' if pdf_path.exists() else 'MISSING'})")

        if not record_id:
            print("ERROR: Could not resolve existing Zenodo record ID")
            return None
        if not pdf_path.exists() and not dry_run:
            print("ERROR: PDF missing, cannot update version")
            return None

        # Internal-only field; never send to API.
        metadata.pop("_existing_doi", None)

        try:
            print(f"[OK] Target record ID: {record_id}")
            print("[OK] Creating new version draft via /api/records/{id}/versions ...")
            version_info = create_version_draft_via_records_api(client, record_id)
            new_id = version_info["new_id"]
            bucket_url = version_info["bucket_url"]
            print(f"[OK] New draft ID: {new_id}")

            if verify_bucket_access(client, bucket_url):
                print(f"[OK] Bucket access verified: {bucket_url}")
            else:
                print("ERROR: Bucket access verification failed")
                return None

            if dry_run:
                print("[OK] Dry run complete (no metadata update, file delete/upload, or publish)")
                return {
                    "id": new_id,
                    "bucket": bucket_url,
                    "verified": True,
                    "dry_run": True,
                }

            print("[OK] Deleting old files from new draft bucket...")
            client.delete_all_files(new_id)

            print("[OK] Updating metadata on new draft...")
            client.update_metadata(new_id, metadata)

            print(f"[OK] Uploading {pdf_path.name} to new draft...")
            client.upload_file(new_id, pdf_path, bucket_url)

            print("[OK] Verifying uploaded file...")
            verified_deposit = client.get_deposit(new_id)
            files = verified_deposit.get("files", [])
            uploaded_file = next((f for f in files if f["filename"] == pdf_path.name), None)
            if not uploaded_file:
                print(f"ERROR: Uploaded file {pdf_path.name} not found on draft {new_id}")
                return None

            local_size = pdf_path.stat().st_size
            remote_size = uploaded_file.get("filesize", 0)
            if local_size != remote_size:
                print(f"ERROR: File size mismatch (local={local_size}, remote={remote_size})")
                return None

            base_web_url = client.base_url.replace("/api", "")
            if skip_publish:
                print("[OK] Draft updated (not published)")
                print(f"  -> Review at: {base_web_url}/deposit/{new_id}")
                return {
                    "id": new_id,
                    "bucket": bucket_url,
                    "url": f"{base_web_url}/deposit/{new_id}",
                    "verified": True,
                    "published": False,
                }

            print("[OK] Publishing new version via /api/records/{id}/draft/actions/publish ...")
            result = publish_draft_via_records_api(client, new_id)
            return {
                "id": new_id,
                "bucket": bucket_url,
                "doi": result.get("conceptdoi") or result.get("doi"),
                "version_doi": result.get("doi"),
                "concept_doi": result.get("conceptdoi"),
                "url": result.get("links", {}).get("self_html") or result.get("links", {}).get("html"),
                "verified": True,
                "published": True,
            }
        except requests.HTTPError as e:
            print(f"ERROR: Zenodo API error while updating version: {e}")
            if getattr(e, "response", None) is not None:
                print(f"  Response: {e.response.text}")
            return None
        except requests.RequestException as e:
            print(f"ERROR: Network/API request failed while updating version: {e}")
            return None

    # upload_paper() handles PDF check, logging, metadata, and upload
    return upload_paper(
        client=client,
        paper_key=paper_key,
        quarto_config=quarto_config,
        pdf_path=pdf_path,
        draft=skip_publish,
        verbose=True,
        save_doi=False,
        config_path=None
    )


def main():
    # Discover papers using shared utility
    papers = discover_paper_configs(PROJECT_ROOT)

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
    parser.add_argument(
        "--update-versions",
        action="store_true",
        help="Update existing published records by creating/publishing new versions",
    )

    args = parser.parse_args()

    if args.list_papers:
        print(f"Discovered {len(papers)} paper(s):")
        for key, info in sorted(papers.items()):
            print(f"  {key}: {info['config_path'].name} - {info['title'][:50]}")
        return 0

    # Load .env file if present
    load_dotenv(PROJECT_ROOT / ".env")

    # Get API token (required for normal uploads and version-update dry runs)
    client = None
    if (not args.dry_run) or args.update_versions:
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
            update_versions=args.update_versions,
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
