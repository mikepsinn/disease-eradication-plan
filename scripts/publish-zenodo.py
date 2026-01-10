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
    python scripts/publish-zenodo.py --sandbox --draft  # Use Zenodo sandbox for testing
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


def load_dotenv(env_file: Path) -> None:
    """Load environment variables from a .env file if it exists."""
    if not env_file.exists():
        return

    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Parse KEY=VALUE format
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                # Remove surrounding quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                # Only set if not already in environment
                if key and key not in os.environ:
                    os.environ[key] = value

# Zenodo API endpoints
ZENODO_API = "https://zenodo.org/api"
ZENODO_SANDBOX_API = "https://sandbox.zenodo.org/api"

# Zenodo community ID (https://zenodo.org/communities/dih)
ZENODO_COMMUNITY = "dih"

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


def discover_papers() -> dict:
    """
    Auto-discover Quarto paper configs from _quarto-*.yml files.

    Only includes configs that:
    - Have a PDF output file configured
    - Have dih-render.zenodo set to true, OR
    - Are not in the skip list (book, test, etc.)

    Returns dict mapping paper key to config info:
    {
        "iab": {
            "quarto_config": "_quarto-iab.yml",
            "pdf_path": "_build_temp/iab/_site/iab/paper.pdf",
            "bib_file": "references-iab.bib",
            "resource_type": "publication-workingpaper",
        },
        ...
    }
    """
    papers = {}

    # Configs to skip (not standalone papers)
    SKIP_CONFIGS = {"book", "test", "main", "base"}

    # Find all _quarto-*.yml files (exclude base _quarto.yml)
    for config_path in PROJECT_ROOT.glob("_quarto-*.yml"):
        # Extract paper key from filename: _quarto-iab.yml -> iab
        key = config_path.stem.replace("_quarto-", "")

        # Skip if key is empty, just "quarto", or in skip list
        if not key or key == "quarto" or key in SKIP_CONFIGS:
            continue

        # Load config to get PDF filename
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"WARNING: Could not read {config_path}: {e}")
            continue

        # Check for explicit zenodo flag in dih-render section
        dih_render = config.get("dih-render", {})

        # If zenodo is explicitly set to false, skip this config
        if dih_render.get("zenodo") is False:
            continue

        # Get PDF filename from config (check multiple locations)
        pdf_filename = None

        # Check dih-render.pdf-output-file first (our custom field)
        if dih_render.get("pdf-output-file"):
            pdf_filename = dih_render["pdf-output-file"]

        # Fall back to format.pdf.output-file
        if not pdf_filename:
            format_config = config.get("format", {})
            pdf_config = format_config.get("pdf", {})
            if pdf_config.get("output-file"):
                pdf_filename = pdf_config["output-file"]

        # Fall back to default naming
        if not pdf_filename:
            pdf_filename = f"{key}-paper.pdf"

        # Construct PDF path using build convention
        pdf_path = f"_build_temp/{key}/_site/{key}/{pdf_filename}"

        # Look for bibliography file
        bib_file = f"references-{key}.bib"
        if not (PROJECT_ROOT / bib_file).exists():
            # Try alternate naming
            bib_file = f"{key}-references.bib"
            if not (PROJECT_ROOT / bib_file).exists():
                bib_file = None

        papers[key] = {
            "quarto_config": config_path.name,
            "pdf_path": pdf_path,
            "bib_file": bib_file,
            "resource_type": "publication-workingpaper",
        }

    return papers



def get_git_dates(file_path: str) -> dict:
    """
    Get creation and last modification dates from git history.

    Returns dict with 'created' and 'updated' dates in ISO format,
    or empty dict if git info unavailable.
    """
    import subprocess

    dates = {}
    full_path = PROJECT_ROOT / file_path

    if not full_path.exists():
        return dates

    try:
        # Get first commit date (creation)
        result = subprocess.run(
            ["git", "log", "--follow", "--format=%aI", "--reverse", str(full_path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            first_line = result.stdout.strip().split("\n")[0]
            dates["created"] = first_line[:10]  # Just the date part

        # Get last commit date (updated)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", str(full_path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            dates["updated"] = result.stdout.strip()[:10]

    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return dates


def load_quarto_config(config_file: str) -> dict:
    """Load and parse a Quarto YAML config file."""
    config_path = PROJECT_ROOT / config_file
    if not config_path.exists():
        raise FileNotFoundError(f"Quarto config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_bibtex_references(bib_file: str) -> list[str]:
    """
    Parse a BibTeX file and return formatted citation strings for Zenodo.

    Returns a list of citation strings like:
    "Author (Year). Title. Journal/Publisher."
    """
    bib_path = PROJECT_ROOT / bib_file
    if not bib_path.exists():
        return []

    references = []

    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Simple regex-based BibTeX parser
    # Match entries like @article{key, ... } or @book{key, ... }
    import re
    entry_pattern = re.compile(
        r'@(\w+)\s*\{\s*([^,]+)\s*,([^@]*?)(?=\n@|\Z)',
        re.DOTALL
    )

    for match in entry_pattern.finditer(content):
        entry_type = match.group(1).lower()
        fields_text = match.group(3)

        # Parse individual fields
        fields = {}
        # Match field = {value} or field = "value" patterns
        field_pattern = re.compile(
            r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)")',
            re.DOTALL
        )
        for field_match in field_pattern.finditer(fields_text):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2) or field_match.group(3) or ""
            # Clean up whitespace
            field_value = " ".join(field_value.split())
            fields[field_name] = field_value

        # Format citation string
        author = fields.get("author", "Unknown Author")
        year = fields.get("year", "n.d.")
        title = fields.get("title", "Untitled")

        # Get journal/publisher based on entry type
        venue = ""
        if entry_type == "article":
            venue = fields.get("journal", "")
            if fields.get("volume"):
                venue += f", {fields['volume']}"
                if fields.get("number"):
                    venue += f"({fields['number']})"
                if fields.get("pages"):
                    venue += f", {fields['pages']}"
        elif entry_type == "book":
            venue = fields.get("publisher", "")
        elif entry_type == "inproceedings":
            venue = fields.get("booktitle", "")
        elif entry_type == "misc" or entry_type == "online":
            venue = fields.get("howpublished", fields.get("url", ""))

        # Build citation string
        citation = f"{author} ({year}). {title}."
        if venue:
            citation += f" {venue}."

        # Add DOI if present
        if fields.get("doi"):
            citation += f" https://doi.org/{fields['doi']}"

        references.append(citation)

    return references


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

    # Description: prefer abstract (longer, more detailed) over description
    abstract = book.get("abstract") or website.get("abstract") or metadata.get("abstract", "")
    short_description = (
        book.get("description") or
        website.get("description") or
        metadata.get("description", "")
    )

    # Clean up abstract (remove extra whitespace from YAML multiline)
    if abstract:
        abstract = " ".join(abstract.split())

    # Use abstract as description if available, otherwise use short description
    # For Zenodo, a rich description helps with discoverability
    if abstract:
        description = f"<p><strong>Abstract:</strong> {abstract}</p>"
        if short_description:
            description += f"<p><strong>Summary:</strong> {short_description}</p>"
    else:
        description = short_description

    # Authors/Creators
    author_name = metadata.get("human-author", metadata.get("creator", "Mike P. Sinn"))
    creators = [{"name": author_name}]

    # Add ORCID if available in metadata, otherwise use default for Mike P. Sinn
    orcid = metadata.get("orcid")
    if orcid:
        creators[0]["orcid"] = orcid
    elif "Mike" in author_name and "Sinn" in author_name:
        creators[0]["orcid"] = "0000-0002-4817-1912"

    # Add affiliation
    creators[0]["affiliation"] = metadata.get("publisher", "Decentralized Institutes of Health")

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

    # Language (ISO 639-3 code - "eng" for English)
    language_map = {
        "en-US": "eng",
        "en-GB": "eng",
        "en": "eng",
    }
    quarto_language = metadata.get("language", "en-US")
    zenodo_language = language_map.get(quarto_language, "eng")

    # Version
    version = metadata.get("version", "1.0")

    # Subjects - map Quarto subject/category to Zenodo subjects
    # Zenodo uses free-text subjects for custom classifications
    subjects = []
    subject_text = metadata.get("subject", "")
    if subject_text:
        # Split comma-separated subjects and clean them up
        for subj in subject_text.split(","):
            subj = subj.strip()
            if subj:
                subjects.append({"term": subj, "scheme": "user-defined"})

    # Contributors (editors, data curators, etc.)
    contributors = []
    contributor_list = metadata.get("contributors", [])
    if isinstance(contributor_list, list):
        for contrib in contributor_list:
            if isinstance(contrib, dict):
                contributors.append({
                    "name": contrib.get("name", ""),
                    "type": contrib.get("type", "Other"),
                    "affiliation": contrib.get("affiliation", ""),
                })
            elif isinstance(contrib, str):
                contributors.append({"name": contrib, "type": "Other"})

    # Method/methodology (if available)
    method = metadata.get("method", "")

    # Build Zenodo metadata
    zenodo_metadata = {
        "title": title,
        "description": description,
        "creators": creators,
        "keywords": keywords,
        "license": zenodo_license,
        "access_right": "open",  # Open access for all papers
        "publication_date": datetime.now().strftime("%Y-%m-%d"),
        "upload_type": "publication",
        "publication_type": "workingpaper",
        "publisher": metadata.get("publisher", "Decentralized Institutes of Health"),
        "language": zenodo_language,
        "version": version,
    }

    if related:
        zenodo_metadata["related_identifiers"] = related

    if subjects:
        zenodo_metadata["subjects"] = subjects

    if contributors:
        zenodo_metadata["contributors"] = contributors

    if method:
        zenodo_metadata["method"] = method

    # Add community
    zenodo_metadata["communities"] = [{"identifier": ZENODO_COMMUNITY}]

    # Add notes with category/genre information if available
    notes_parts = []
    category = metadata.get("category")
    if category:
        notes_parts.append(f"Category: {category}")
    genre = metadata.get("genre")
    if genre:
        notes_parts.append(f"Genre: {genre}")
    audience = metadata.get("audience")
    if audience:
        notes_parts.append(f"Target Audience: {audience}")

    if notes_parts:
        zenodo_metadata["notes"] = " | ".join(notes_parts)

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

    def find_draft_by_title(self, title: str) -> Optional[dict]:
        """Find an existing draft deposit by title."""
        response = requests.get(
            f"{self.base_url}/deposit/depositions",
            headers=self.headers,
            params={"status": "draft"},
        )
        response.raise_for_status()

        for deposit in response.json():
            deposit_title = deposit.get("metadata", {}).get("title", "")
            if deposit_title == title:
                return deposit
        return None


def publish_paper(
    paper_key: str,
    paper_config: dict,
    client: Optional["ZenodoClient"],
    dry_run: bool = False,
    skip_publish: bool = False,
) -> Optional[dict]:
    """
    Upload a paper to Zenodo as a draft.

    Args:
        paper_key: Short identifier for the paper (e.g., "iab", "dfda")
        paper_config: Config dict with quarto_config, pdf_path, bib_file, resource_type
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

    # Load Quarto config and extract metadata
    quarto_config = load_quarto_config(paper_config["quarto_config"])
    metadata = extract_zenodo_metadata(quarto_config, paper_key)

    # Note: Git dates are intentionally NOT submitted to Zenodo.
    # Zenodo validates dates against their server time and rejects "future" dates,
    # which causes issues when local system time differs from Zenodo's server.
    # The publication_date field (set to today) is sufficient for Zenodo metadata.

    # Parse and add bibliography references
    bib_file = paper_config.get("bib_file")
    if bib_file:
        references = parse_bibtex_references(bib_file)
        if references:
            metadata["references"] = references

    print(f"[OK] Title: {metadata['title']}")
    print(f"[OK] Authors: {', '.join(c['name'] for c in metadata['creators'])}")
    print(f"[OK] License: {metadata['license']}")
    print(f"[OK] Version: {metadata.get('version', 'N/A')}")
    print(f"[OK] Language: {metadata.get('language', 'N/A')}")
    if metadata.get('subjects'):
        print(f"[OK] Subjects: {len(metadata['subjects'])} subject(s)")
    if metadata.get('references'):
        print(f"[OK] References: {len(metadata['references'])} citation(s)")
    if metadata.get('communities'):
        print(f"[OK] Community: {metadata['communities'][0]['identifier']}")
    desc_preview = metadata.get('description', '')[:100]
    if desc_preview:
        print(f"[OK] Description: {desc_preview}...")

    if dry_run:
        print("\n[DRY RUN] Would upload with metadata:")
        print(json.dumps(metadata, indent=2))
        return None

    # Client is required for actual uploads (not dry-run)
    assert client is not None, "Client is required for non-dry-run operations"

    try:
        # Check for existing draft with same title (to update instead of creating duplicates)
        print("[OK] Checking for existing draft...")
        existing_draft = client.find_draft_by_title(metadata["title"])

        if existing_draft:
            deposit_id = existing_draft["id"]
            print(f"[OK] Found existing draft: {deposit_id}")
            print("  -> Updating existing draft...")
            # Get full deposit details to get bucket URL
            full_deposit = client.get_deposit(deposit_id)
            bucket_url = full_deposit["links"]["bucket"]
            # Delete old files before uploading new one
            client.delete_all_files(deposit_id)
        else:
            print("[OK] No existing draft found, creating new deposit...")
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
            print("[OK] Draft saved (not published)")
            print(f"  -> Review at: {client.base_url.replace('/api', '')}/deposit/{deposit_id}")
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

        return {"id": deposit_id, "bucket": bucket_url}

    except requests.HTTPError as e:
        print(f"ERROR: Zenodo API error: {e}")
        print(f"  Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return None


def main():
    # Discover papers first so we can use them in argument choices
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

    env_name = "SANDBOX" if args.sandbox else "PRODUCTION"
    print(f"Zenodo Environment: {env_name}")
    if client:
        print(f"API: {client.base_url}")
    else:
        print("API: (dry-run mode - no connection)")

    # Determine which papers to upload
    papers_to_upload = [args.paper] if args.paper else list(papers.keys())

    results = {}
    for paper_key in papers_to_upload:
        result = publish_paper(
            paper_key,
            papers[paper_key],  # Pass config directly
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
        if result is None:
            status = "[ERROR] Failed"
            failed = True
        elif result:
            status = "[OK] Uploaded"
        else:
            status = "[--] Skipped"
        print(f"  {paper_key}: {status}")

    # Exit with error code if any upload failed
    if failed:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
