#!/usr/bin/env python3
"""
Sync Zenodo Metadata from Local Configs

Updates Zenodo record metadata to match current _quarto-*.yml configs.
Creates new version drafts for published records to update metadata.

Usage:
    python scripts/sync-zenodo-metadata.py --dry-run    # Preview changes only
    python scripts/sync-zenodo-metadata.py              # Apply updates
    python scripts/sync-zenodo-metadata.py --paper economics  # Specific paper only

Requires:
    ZENODO_TOKEN env var with deposit:write scope
"""

import sys
import argparse
import io
from pathlib import Path
from datetime import datetime
from difflib import unified_diff
import requests

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "lib"))

from python_utils import load_project_dotenv
from zenodo_client import (
    ZenodoClient,
    extract_zenodo_metadata,
    get_zenodo_token,
    get_record_id_from_doi,
)
from quarto_config_utils import discover_paper_configs

PROJECT_ROOT = Path(__file__).parent.parent
load_project_dotenv(PROJECT_ROOT)


def compare_metadata(local_meta, zenodo_meta):
    """Compare local and Zenodo metadata, return dict of differences.

    Returns:
        Dict with keys that differ, or empty dict if identical
    """
    differences = {}

    # Compare key fields
    fields_to_compare = [
        'title',
        'description',
        'publisher',
        'license',
        'keywords',
        'creators',
    ]

    for field in fields_to_compare:
        local_val = local_meta.get(field)
        zenodo_val = zenodo_meta.get(field)

        # Normalize for comparison
        if isinstance(local_val, str):
            local_val = local_val.strip()
        if isinstance(zenodo_val, str):
            zenodo_val = zenodo_val.strip()

        if local_val != zenodo_val:
            differences[field] = {
                'local': local_val,
                'zenodo': zenodo_val,
            }

    return differences


def format_diff(field_name, local_val, zenodo_val):
    """Format a unified diff for display."""
    if isinstance(local_val, (list, dict)):
        local_str = str(local_val)
        zenodo_str = str(zenodo_val)
    else:
        local_str = str(local_val) if local_val else ''
        zenodo_str = str(zenodo_val) if zenodo_val else ''

    if not local_str and not zenodo_str:
        return f"  {field_name}: (both empty)"

    if '\n' in local_str or '\n' in zenodo_str or len(local_str) > 100 or len(zenodo_str) > 100:
        # Multi-line diff
        local_lines = local_str.splitlines(keepends=True)
        zenodo_lines = zenodo_str.splitlines(keepends=True)
        diff = unified_diff(
            zenodo_lines,
            local_lines,
            fromfile='zenodo',
            tofile='local',
            lineterm='',
        )
        return f"  {field_name}:\n" + ''.join(f"    {line}" for line in diff)
    else:
        # Single-line diff
        return f"  {field_name}:\n    - zenodo: {zenodo_val}\n    + local:  {local_val}"


def sync_paper_metadata(
    client: ZenodoClient,
    paper_key: str,
    paper_info: dict,
    dry_run: bool = True,
    verbose: bool = False,
    keep_drafts: bool = False,
):
    """Sync metadata for a single paper.

    Args:
        client: Zenodo API client
        paper_key: Paper identifier
        paper_info: Paper config info
        dry_run: Preview changes only
        verbose: Show detailed output
        keep_drafts: Skip papers with existing drafts instead of replacing them

    Returns:
        Dict with status and details
    """
    config = paper_info["config"]
    local_metadata = extract_zenodo_metadata(config, paper_key, project_root=PROJECT_ROOT)

    # Get existing DOI
    existing_doi = local_metadata.pop("_existing_doi", None)
    if not existing_doi:
        return {
            'status': 'skip',
            'reason': 'No DOI in config',
        }

    record_id = get_record_id_from_doi(existing_doi)
    if not record_id:
        return {
            'status': 'skip',
            'reason': f'Could not parse record ID from DOI: {existing_doi}',
        }

    print(f"\n{'='*60}")
    print(f"Paper: {paper_key}")
    print(f"DOI: {existing_doi}")
    print(f"Record ID: {record_id}")
    print(f"{'='*60}")

    # Fetch current Zenodo metadata
    try:
        record = client.get_record(record_id)
        zenodo_meta = record.get('metadata', {})
    except Exception as e:
        return {
            'status': 'error',
            'reason': f'Failed to fetch record: {e}',
        }

    # Get the latest version ID (needed for creating new version)
    # When querying a concept ID, Zenodo returns the latest published version
    version_doi = zenodo_meta.get('doi', '')
    latest_version_id = get_record_id_from_doi(version_doi)
    if not latest_version_id:
        return {
            'status': 'error',
            'reason': f'Could not extract latest version ID from DOI: {version_doi}',
        }

    if verbose:
        print(f"[INFO] Latest version ID: {latest_version_id} (from DOI: {version_doi})")

    # Compare metadata
    differences = compare_metadata(local_metadata, zenodo_meta)

    if not differences:
        print("[OK] Metadata already matches - no update needed")
        return {
            'status': 'ok',
            'reason': 'Already in sync',
        }

    # Show differences
    print(f"\n[DIFF] Found {len(differences)} difference(s):")
    for field, values in differences.items():
        print(format_diff(field, values['local'], values['zenodo']))

    if dry_run:
        print("\n[DRY-RUN] Would create new version draft with updated metadata")
        return {
            'status': 'dry_run',
            'differences': differences,
        }

    # Check for existing drafts for this concept and handle them
    existing_draft_ids = client.find_drafts_by_concept(record_id)
    if existing_draft_ids:
        if keep_drafts:
            print(f"[SKIP] {len(existing_draft_ids)} draft(s) already exist: {existing_draft_ids}")
            print("       Remove --keep-drafts flag to replace existing drafts")
            return {
                'status': 'skip',
                'reason': 'Draft already exists (remove --keep-drafts to replace)',
            }
        else:
            # Default: automatically replace existing drafts
            print(f"[INFO] Found {len(existing_draft_ids)} existing draft(s), deleting...")
            for draft_id in existing_draft_ids:
                if client.delete_deposit(draft_id):
                    print(f"[OK] Deleted existing draft {draft_id}")
                else:
                    print(f"[WARN] Could not delete draft {draft_id}")
                    return {
                        'status': 'error',
                        'reason': f'Failed to delete existing draft {draft_id}',
                    }

    # Create new version draft using latest version ID
    print("\n[UPDATE] Creating new version draft...")
    try:
        version_info = client.create_version_draft(latest_version_id)
        draft_id = version_info["id"]
        print(f"[OK] Created draft: {draft_id}")
    except requests.HTTPError as e:
        error_msg = f'Failed to create version draft: {e} (status: {e.response.status_code if e.response else "unknown"})'
        print(f"[ERROR] {error_msg}")
        return {
            'status': 'error',
            'reason': error_msg,
        }
    except Exception as e:
        error_msg = f'Failed to create version draft: {e}'
        print(f"[ERROR] {error_msg}")
        return {
            'status': 'error',
            'reason': error_msg,
        }

    # Update metadata
    print("[UPDATE] Updating metadata...")
    try:
        client.update_metadata(draft_id, local_metadata)
        print("[OK] Metadata updated successfully")
    except Exception as e:
        return {
            'status': 'error',
            'reason': f'Failed to update metadata: {e}',
        }

    # Get draft URL
    draft_url = f"https://zenodo.org/deposit/{draft_id}"
    print(f"\n[SUCCESS] Metadata sync complete!")
    print(f"  Review draft at: {draft_url}")
    print(f"  Publish when ready")

    return {
        'status': 'updated',
        'draft_id': draft_id,
        'draft_url': draft_url,
        'differences': differences,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Sync Zenodo metadata from local configs"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them"
    )
    parser.add_argument(
        "--paper",
        help="Specific paper key to sync (e.g., 'economics')"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "--keep-drafts",
        action="store_true",
        help="Skip papers with existing drafts instead of replacing them"
    )
    args = parser.parse_args()

    token = get_zenodo_token()
    if not token:
        print("ERROR: No Zenodo token found")
        print("Set ZENODO_TOKEN env var")
        sys.exit(1)

    client = ZenodoClient(token)

    # Discover papers
    papers = discover_paper_configs(PROJECT_ROOT)

    # Filter to specific paper if requested
    if args.paper:
        if args.paper not in papers:
            print(f"ERROR: Paper '{args.paper}' not found")
            print(f"Available: {', '.join(sorted(papers.keys()))}")
            sys.exit(1)
        papers = {args.paper: papers[args.paper]}

    print("=" * 60)
    print("ZENODO METADATA SYNC")
    print(f"Mode: {'DRY-RUN (preview only)' if args.dry_run else 'LIVE (will update)'}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"\nFound {len(papers)} paper(s) to check")

    results = {}
    for paper_key, paper_info in papers.items():
        result = sync_paper_metadata(
            client=client,
            paper_key=paper_key,
            paper_info=paper_info,
            dry_run=args.dry_run,
            verbose=args.verbose,
            keep_drafts=args.keep_drafts,
        )
        results[paper_key] = result

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    status_counts = {}
    for paper_key, result in results.items():
        status = result['status']
        status_counts[status] = status_counts.get(status, 0) + 1

    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

    if args.dry_run and any(r['status'] == 'dry_run' for r in results.values()):
        print("\nRun without --dry-run to apply changes")
    elif any(r['status'] == 'updated' for r in results.values()):
        print("\nDrafts created - review and publish on Zenodo")
    else:
        print("\nAll metadata already in sync!")


if __name__ == "__main__":
    main()
