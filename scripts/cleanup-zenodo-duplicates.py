#!/usr/bin/env python3
"""
Cleanup Zenodo Duplicate Drafts

Deletes incorrectly created draft deposits and updates configs to use concept DOIs.

Usage:
    python scripts/cleanup-zenodo-duplicates.py --dry-run    # Preview deletions
    python scripts/cleanup-zenodo-duplicates.py              # Execute deletions
"""

import sys
import io
import argparse
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "lib"))

import requests
import yaml
from python_utils import load_project_dotenv
from zenodo_client import get_zenodo_token

PROJECT_ROOT = Path(__file__).parent.parent
load_project_dotenv(PROJECT_ROOT)


# Mapping of paper -> (draft_to_delete, published_record, published_concept_doi)
CLEANUP_MAP = {
    'wishocracy': {
        'draft_id': 18523096,
        'published_id': 18480097,
        'concept_doi': '10.5281/zenodo.18205881',
    },
    'optimocracy': {
        'draft_id': 18523076,
        'published_id': 18480163,
        'concept_doi': '10.5281/zenodo.18356213',
    },
    'political-dysfunction-tax': {
        'draft_id': 18522028,
        'published_id': 18480175,
        'concept_doi': '10.5281/zenodo.18447493',
    },
    '1-pct-treaty-impact': {
        'draft_id': 18522797,
        'published_id': 18520926,
        'concept_doi': None,  # Need to fetch
    },
    'obg': {
        'draft_id': 18522045,
        'published_id': 18480086,
        'concept_doi': None,
    },
    'iab': {
        'draft_id': 18522041,
        'published_id': 18520942,
        'concept_doi': None,
    },
    'federal-efficiency-audit': {
        'draft_id': 18522037,
        'published_id': 18480151,
        'concept_doi': None,
    },
    'dfda-spec': {
        'draft_id': 18522035,
        'published_id': 18520941,
        'concept_doi': None,
    },
    'dfda-impact': {
        'draft_id': 18522033,
        'published_id': 18480062,
        'concept_doi': None,
    },
    'cost-of-change': {
        'draft_id': 18522031,
        'published_id': 18520935,
        'concept_doi': None,
    },
    'opg': {
        'draft_id': 18521983,
        'published_id': 18480092,
        'concept_doi': None,
    },
}


def fetch_concept_doi(record_id, token):
    """Fetch concept DOI for a published record."""
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(f'https://zenodo.org/api/records/{record_id}', headers=headers)
    if r.status_code == 200:
        return r.json().get('conceptdoi')
    return None


def delete_draft(draft_id, token, dry_run=False):
    """Delete a draft deposit."""
    headers = {'Authorization': f'Bearer {token}'}

    if dry_run:
        print(f"  [DRY-RUN] Would delete draft {draft_id}")
        return True

    r = requests.delete(f'https://zenodo.org/api/deposit/depositions/{draft_id}', headers=headers)
    if r.status_code in (204, 404):
        print(f"  [OK] Deleted draft {draft_id}")
        return True
    else:
        print(f"  [ERROR] Failed to delete draft {draft_id}: {r.status_code}")
        return False


def update_config_doi(paper_key, concept_doi, dry_run=False):
    """Update Quarto config to use concept DOI."""
    config_path = PROJECT_ROOT / f"_quarto-{paper_key}.yml"

    if not config_path.exists():
        print(f"  [WARN] Config not found: {config_path.name}")
        return False

    # Read config
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if DOI exists
    if 'doi:' not in content:
        print(f"  [WARN] No DOI field found in {config_path.name}")
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would update {config_path.name} to use concept DOI: {concept_doi}")
        return True

    # Replace DOI (both in metadata and publishing sections)
    import re

    # Replace metadata.doi
    content = re.sub(
        r'(metadata:\s*\n(?:.*\n)*?  doi:\s*["\']?)10\.5281/zenodo\.\d+(["\']?)',
        rf'\g<1>{concept_doi}\g<2>',
        content,
        count=1
    )

    # Replace publishing.preprints.doi
    content = re.sub(
        r'(doi:\s*["\']?)10\.5281/zenodo\.\d+(["\']?)',
        rf'\g<1>{concept_doi}\g<2>',
        content
    )

    # Write back
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] Updated {config_path.name} to concept DOI: {concept_doi}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Cleanup Zenodo duplicate drafts")
    parser.add_argument('--dry-run', action='store_true', help='Preview without executing')
    args = parser.parse_args()

    token = get_zenodo_token()
    if not token:
        print("ERROR: No Zenodo token found")
        sys.exit(1)

    print("=" * 60)
    print("ZENODO CLEANUP - Delete Duplicate Drafts")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)

    # Fetch missing concept DOIs
    print("\nFetching concept DOIs...")
    for paper_key, info in CLEANUP_MAP.items():
        if info['concept_doi'] is None:
            concept_doi = fetch_concept_doi(info['published_id'], token)
            if concept_doi:
                info['concept_doi'] = concept_doi
                print(f"  {paper_key}: {concept_doi}")
            else:
                print(f"  [WARN] {paper_key}: Failed to fetch concept DOI")

    # Delete drafts
    print("\nDeleting incorrect drafts...")
    deleted_count = 0
    for paper_key, info in CLEANUP_MAP.items():
        print(f"\n{paper_key}:")
        if delete_draft(info['draft_id'], token, args.dry_run):
            deleted_count += 1

    # Update configs
    print("\nUpdating configs to use concept DOIs...")
    updated_count = 0
    for paper_key, info in CLEANUP_MAP.items():
        if info['concept_doi']:
            print(f"\n{paper_key}:")
            if update_config_doi(paper_key, info['concept_doi'], args.dry_run):
                updated_count += 1

    # Summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Drafts deleted: {deleted_count}/{len(CLEANUP_MAP)}")
    print(f"Configs updated: {updated_count}/{len(CLEANUP_MAP)}")

    if args.dry_run:
        print("\nRun without --dry-run to execute")
    else:
        print("\nCleanup complete!")
        print("\nNext steps:")
        print("  1. Verify configs have concept DOIs")
        print("  2. Run upload script to create proper new versions")
        print("  3. Publish the new versions on Zenodo")


if __name__ == "__main__":
    main()
