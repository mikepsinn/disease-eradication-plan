#!/usr/bin/env python3
"""
Delete Zenodo Draft Deposits

Lists all draft deposits and optionally deletes them.
Useful for cleaning up before running sync-zenodo-metadata.py.

Usage:
    python scripts/delete-zenodo-drafts.py --list          # List all drafts
    python scripts/delete-zenodo-drafts.py --delete-all    # Delete all drafts
    python scripts/delete-zenodo-drafts.py --delete 12345  # Delete specific draft ID
"""

import sys
import argparse
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "lib"))

from python_utils import load_project_dotenv
from zenodo_client import ZenodoClient, get_zenodo_token
import requests

PROJECT_ROOT = Path(__file__).parent.parent
load_project_dotenv(PROJECT_ROOT)


def list_all_drafts(client: ZenodoClient) -> list:
    """List all draft deposits (paginated)."""
    all_drafts = []
    page = 1

    while True:
        try:
            response = requests.get(
                f"{client.base_url}/deposit/depositions",
                headers=client.headers,
                params={"page": page, "size": 20},
                timeout=client.timeout,
            )

            if response.status_code == 403:
                # Try without params
                response = requests.get(
                    f"{client.base_url}/deposit/depositions",
                    headers=client.headers,
                    timeout=client.timeout,
                )

            response.raise_for_status()
            deposits = response.json()

            if not deposits:
                break

            # Filter for drafts (not submitted)
            drafts = [d for d in deposits if not d.get('submitted', False)]
            all_drafts.extend(drafts)

            # If we got fewer than page size, we're done
            if len(deposits) < 20:
                break

            page += 1

        except requests.HTTPError as e:
            print(f"Error fetching deposits: {e}")
            break

    return all_drafts


def main():
    parser = argparse.ArgumentParser(
        description="List and delete Zenodo draft deposits"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all draft deposits"
    )
    parser.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all draft deposits"
    )
    parser.add_argument(
        "--delete",
        type=int,
        help="Delete specific draft deposit by ID"
    )
    args = parser.parse_args()

    if not any([args.list, args.delete_all, args.delete]):
        parser.print_help()
        sys.exit(1)

    token = get_zenodo_token()
    if not token:
        print("ERROR: No Zenodo token found")
        print("Set ZENODO_TOKEN env var")
        sys.exit(1)

    client = ZenodoClient(token)

    if args.list or args.delete_all:
        print("Fetching draft deposits...")
        drafts = list_all_drafts(client)

        if not drafts:
            print("No draft deposits found")
            return

        print(f"\nFound {len(drafts)} draft deposit(s):\n")
        for draft in drafts:
            draft_id = draft.get('id')
            title = draft.get('title', 'N/A')
            conceptrecid = draft.get('conceptrecid', 'N/A')
            print(f"  ID: {draft_id}")
            print(f"     Concept: {conceptrecid}")
            print(f"     Title: {title[:70]}")
            print(f"     URL: https://zenodo.org/deposit/{draft_id}")
            print()

        if args.delete_all:
            confirm = input(f"\nDelete all {len(drafts)} draft(s)? (yes/no): ")
            if confirm.lower() == 'yes':
                for draft in drafts:
                    draft_id = draft.get('id')
                    if client.delete_deposit(draft_id):
                        print(f"[OK] Deleted draft {draft_id}")
                    else:
                        print(f"[ERROR] Failed to delete draft {draft_id}")
            else:
                print("Cancelled")

    elif args.delete:
        draft_id = args.delete
        print(f"Deleting draft {draft_id}...")
        if client.delete_deposit(draft_id):
            print(f"[OK] Deleted draft {draft_id}")
        else:
            print(f"[ERROR] Failed to delete draft {draft_id}")


if __name__ == "__main__":
    main()
