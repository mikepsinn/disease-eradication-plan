#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zenodo Publishing Script

Automates publishing of Quarto-generated PDFs to Zenodo.
Reads metadata from _quarto-*.yml files and uploads PDFs with proper academic metadata.

Usage:
    python scripts/publish-zenodo.py                    # Publish all papers
    python scripts/publish-zenodo.py --paper iab        # Publish specific paper
    python scripts/publish-zenodo.py --sandbox          # Use Zenodo sandbox for testing
    python scripts/publish-zenodo.py --dry-run          # Show what would be uploaded

Environment variables:
    ZENODO_TOKEN: API token for Zenodo (required)
    ZENODO_SANDBOX_TOKEN: API token for Zenodo sandbox (optional, for testing)
"""

from __future__ import annotations

import sys
import os
import json
import argparse
import io
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# Zenodo API endpoints
ZENODO_API = "https://zenodo.org/api"
ZENODO_SANDBOX_API = "https://sandbox.zenodo.org/api"

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Paper configurations
PAPERS = {
    "iab": {
        "quarto_config": "_quarto-iab.yml",
        "pdf_path": "_build_temp/iab/_site/iab/incentive-alignment-bonds-paper.pdf",
        "resource_type": "publication-workingpaper",
    },
    "dfda": {
        "quarto_config": "_quarto-dfda.yml",
        "pdf_path": "_build_temp/dfda/_site/dfda/dfda-paper.pdf",
        "resource_type": "publication-workingpaper",
    },
    "economics": {
        "quarto_config": "_quarto-economics.yml",
        "pdf_path": "_build_temp/economics/_site/economics/1-percent-treaty-impact.pdf",
        "resource_type": "publication-workingpaper",
    },
    "wishocracy": {
        "quarto_config": "_quarto-wishocracy.yml",
        "pdf_path": "_build_temp/wishocracy/_site/wishocracy/wishocracy-rappa-paper.pdf",
        "resource_type": "publication-workingpaper",
    },
}

# Zenodo deposit IDs file (tracks existing deposits for versioning)
ZENODO_IDS_FILE = PROJECT_ROOT / "zenodo-deposits.json"


def load_zenodo_ids() -> dict:
    """Load existing Zenodo deposit IDs from config file."""
    if ZENODO_IDS_FILE.exists():
        with open(ZENODO_IDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"production": {}, "sandbox": {}}


def save_zenodo_ids(ids: dict) -> None:
    """Save Zenodo deposit IDs to config file."""
    with open(ZENODO_IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(ids, f, indent=2)
    print(f"[OK] Saved deposit IDs to {ZENODO_IDS_FILE}")


def load_quarto_config(config_file: str) -> dict:
    """Load and parse a Quarto YAML config file."""
    config_path = PROJECT_ROOT / config_file
    if not config_path.exists():
        raise FileNotFoundError(f"Quarto config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_zenodo_metadata(quarto_config: dict, paper_key: str) -> dict:
    """
    Convert Quarto metadata to Zenodo metadata format.

    See: https://developers.zenodo.org/#representation
    """
    # Get metadata from various sections
    metadata = quarto_config.get("metadata", {})
    website = quarto_config.get("website", {})
    book = quarto_config.get("book", {})

    # Title: prefer book/website title over metadata
    title = book.get("title") or website.get("title") or metadata.get("title", f"Paper: {paper_key}")

    # Description
    description = (
        book.get("description") or
        website.get("description") or
        metadata.get("description", "")
    )

    # Authors/Creators
    author_name = metadata.get("human-author", metadata.get("creator", "Mike P. Sinn"))
    creators = [{"name": author_name}]

    # Add ORCID if available (you can add this to your _quarto-*.yml files)
    orcid = metadata.get("orcid")
    if orcid:
        creators[0]["orcid"] = orcid

    # Keywords
    keywords = metadata.get("keywords", [])
    if isinstance(keywords, list):
        keywords = keywords[:10]  # Zenodo limits keywords

    # License mapping (Quarto to Zenodo)
    license_map = {
        "CC BY-NC 4.0": "cc-by-nc-4.0",
        "CC BY 4.0": "cc-by-4.0",
        "CC BY-SA 4.0": "cc-by-sa-4.0",
        "MIT": "mit",
    }
    quarto_license = metadata.get("license", "CC BY-NC 4.0")
    zenodo_license = license_map.get(quarto_license, "cc-by-nc-4.0")

    # Related identifiers (link to live website)
    related = []
    site_url = book.get("site-url") or website.get("site-url")
    if site_url:
        related.append({
            "identifier": site_url,
            "relation": "isSupplementedBy",
            "resource_type": "publication-softwaredocumentation",
        })

    # GitHub repo
    repo_url = metadata.get("repo-url") or metadata.get("source-url")
    if repo_url:
        related.append({
            "identifier": repo_url,
            "relation": "isSupplementedBy",
            "resource_type": "software",
        })

    # Build Zenodo metadata
    zenodo_metadata = {
        "title": title,
        "description": description,
        "creators": creators,
        "keywords": keywords,
        "license": {"id": zenodo_license},
        "publication_date": datetime.now().strftime("%Y-%m-%d"),
        "resource_type": {"id": PAPERS[paper_key]["resource_type"]},
        "publisher": metadata.get("publisher", "Decentralized Institutes of Health"),
    }

    if related:
        zenodo_metadata["related_identifiers"] = related

    # Add subject/category if available
    subject = metadata.get("subject")
    if subject:
        zenodo_metadata["notes"] = f"Subject: {subject}"

    return zenodo_metadata


class ZenodoClient:
    """Simple Zenodo API client."""

    def __init__(self, token: str, sandbox: bool = False):
        self.token = token
        self.base_url = ZENODO_SANDBOX_API if sandbox else ZENODO_API
        self.sandbox = sandbox
        self.headers = {"Authorization": f"Bearer {token}"}

    def create_deposit(self) -> dict:
        """Create a new empty deposit."""
        response = requests.post(
            f"{self.base_url}/deposit/depositions",
            headers=self.headers,
            json={},
        )
        response.raise_for_status()
        return response.json()

    def create_new_version(self, deposit_id: int) -> dict:
        """Create a new version of an existing deposit."""
        response = requests.post(
            f"{self.base_url}/deposit/depositions/{deposit_id}/actions/newversion",
            headers=self.headers,
        )
        response.raise_for_status()

        # Get the new version draft
        data = response.json()
        new_version_url = data["links"]["latest_draft"]

        response = requests.get(new_version_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_metadata(self, deposit_id: int, metadata: dict) -> dict:
        """Update deposit metadata."""
        response = requests.put(
            f"{self.base_url}/deposit/depositions/{deposit_id}",
            headers=self.headers,
            json={"metadata": metadata},
        )
        response.raise_for_status()
        return response.json()

    def delete_all_files(self, deposit_id: int) -> None:
        """Delete all files from a deposit (for updating versions)."""
        response = requests.get(
            f"{self.base_url}/deposit/depositions/{deposit_id}/files",
            headers=self.headers,
        )
        response.raise_for_status()

        for file_info in response.json():
            file_id = file_info["id"]
            requests.delete(
                f"{self.base_url}/deposit/depositions/{deposit_id}/files/{file_id}",
                headers=self.headers,
            )

    def upload_file(self, deposit_id: int, file_path: Path, bucket_url: str) -> dict:
        """Upload a file to a deposit."""
        with open(file_path, "rb") as f:
            response = requests.put(
                f"{bucket_url}/{file_path.name}",
                headers=self.headers,
                data=f,
            )
        response.raise_for_status()
        return response.json()

    def publish(self, deposit_id: int) -> dict:
        """Publish a deposit (makes it public and assigns DOI)."""
        response = requests.post(
            f"{self.base_url}/deposit/depositions/{deposit_id}/actions/publish",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def get_deposit(self, deposit_id: int) -> dict:
        """Get deposit details."""
        response = requests.get(
            f"{self.base_url}/deposit/depositions/{deposit_id}",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()


def publish_paper(
    paper_key: str,
    client: ZenodoClient,
    zenodo_ids: dict,
    dry_run: bool = False,
    skip_publish: bool = False,
) -> Optional[dict]:
    """
    Publish a single paper to Zenodo.

    Returns the deposit info if successful, None otherwise.
    """
    paper_config = PAPERS[paper_key]
    env_key = "sandbox" if client.sandbox else "production"

    print(f"\n{'='*60}")
    print(f"Publishing: {paper_key}")
    print(f"{'='*60}")

    # Check if PDF exists
    pdf_path = PROJECT_ROOT / paper_config["pdf_path"]
    if not pdf_path.exists():
        print(f"WARNING: PDF not found at {pdf_path}")
        print("  -> Skipping (build the paper first)")
        return None

    print(f"[OK] PDF found: {pdf_path.name} ({pdf_path.stat().st_size / 1024:.1f} KB)")

    # Load Quarto config and extract metadata
    quarto_config = load_quarto_config(paper_config["quarto_config"])
    metadata = extract_zenodo_metadata(quarto_config, paper_key)

    print(f"[OK] Title: {metadata['title']}")
    print(f"[OK] Authors: {', '.join(c['name'] for c in metadata['creators'])}")
    print(f"[OK] License: {metadata['license']['id']}")

    if dry_run:
        print("\n[DRY RUN] Would upload with metadata:")
        print(json.dumps(metadata, indent=2))
        return None

    # Check for existing deposit
    existing_id = zenodo_ids.get(env_key, {}).get(paper_key)

    try:
        if existing_id:
            print(f"[OK] Found existing deposit: {existing_id}")
            print("  -> Creating new version...")
            deposit = client.create_new_version(existing_id)
            # Delete old files from draft
            client.delete_all_files(deposit["id"])
        else:
            print("[OK] Creating new deposit...")
            deposit = client.create_deposit()

        deposit_id = deposit["id"]
        bucket_url = deposit["links"]["bucket"]

        print(f"[OK] Deposit ID: {deposit_id}")

        # Update metadata
        print("[OK] Updating metadata...")
        client.update_metadata(deposit_id, metadata)

        # Upload PDF
        print(f"[OK] Uploading {pdf_path.name}...")
        client.upload_file(deposit_id, pdf_path, bucket_url)

        if skip_publish:
            print("[OK] Skipping publish (draft saved)")
            print(f"  -> Edit at: {client.base_url.replace('/api', '')}/deposit/{deposit_id}")
        else:
            # Publish
            print("[OK] Publishing...")
            result = client.publish(deposit_id)

            doi = result.get("doi")
            concept_doi = result.get("conceptdoi")

            print(f"\n[SUCCESS] Published!")
            print(f"  DOI: {doi}")
            print(f"  Concept DOI: {concept_doi}")
            print(f"  URL: {result['links']['html']}")

            # Save the concept record ID for future versions
            zenodo_ids.setdefault(env_key, {})[paper_key] = result["conceptrecid"]
            save_zenodo_ids(zenodo_ids)

        return deposit

    except requests.HTTPError as e:
        print(f"ERROR: Zenodo API error: {e}")
        print(f"  Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Publish Quarto papers to Zenodo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--paper",
        choices=list(PAPERS.keys()),
        help="Publish specific paper (default: all)",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo sandbox for testing",
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
        print("Configured papers:")
        for key, config in PAPERS.items():
            print(f"  {key}: {config['quarto_config']}")
        return 0

    # Get API token
    if args.sandbox:
        token = os.environ.get("ZENODO_SANDBOX_TOKEN")
        if not token:
            print("ERROR: ZENODO_SANDBOX_TOKEN environment variable not set")
            print("  Get token at: https://sandbox.zenodo.org/account/settings/applications/")
            return 1
    else:
        token = os.environ.get("ZENODO_TOKEN")
        if not token:
            print("ERROR: ZENODO_TOKEN environment variable not set")
            print("  Get token at: https://zenodo.org/account/settings/applications/")
            return 1

    # Initialize client
    client = ZenodoClient(token, sandbox=args.sandbox)
    zenodo_ids = load_zenodo_ids()

    env_name = "SANDBOX" if args.sandbox else "PRODUCTION"
    print(f"Zenodo Environment: {env_name}")
    print(f"API: {client.base_url}")

    # Determine which papers to publish
    papers_to_publish = [args.paper] if args.paper else list(PAPERS.keys())

    results = {}
    for paper_key in papers_to_publish:
        result = publish_paper(
            paper_key,
            client,
            zenodo_ids,
            dry_run=args.dry_run,
            skip_publish=args.draft,
        )
        results[paper_key] = result

    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")

    for paper_key, result in results.items():
        status = "[OK] Published" if result else "[--] Skipped"
        print(f"  {paper_key}: {status}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
