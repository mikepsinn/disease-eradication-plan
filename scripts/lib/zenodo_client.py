#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zenodo Client Library

Upload papers to Zenodo with DOI tracking.

Example:
    from lib.zenodo_client import ZenodoClient, upload_paper, get_zenodo_token

    client = ZenodoClient(get_zenodo_token())
    result = upload_paper(client, "economics", config, pdf_path, draft=True)
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
import yaml

ZENODO_API = "https://zenodo.org/api"
ZENODO_COMMUNITY = "dih"
DEFAULT_ORCID = "0009-0006-0212-1094"


def get_record_id_from_doi(doi: str) -> Optional[int]:
    """
    Extract Zenodo record ID from a DOI.

    Args:
        doi: DOI string like "10.5281/zenodo.18243915"

    Returns:
        Record ID (e.g., 18243915) or None if not a valid Zenodo DOI
    """
    if not doi:
        return None
    # Handle both formats: "10.5281/zenodo.18243915" and "zenodo.18243915"
    if "zenodo." in doi.lower():
        try:
            return int(doi.lower().split("zenodo.")[-1])
        except ValueError:
            return None
    return None


class ZenodoClient:
    """Zenodo API client."""

    def __init__(self, token: str):
        self.token = token
        self.base_url = ZENODO_API
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
    if abstract:
        description = f"<p><strong>Abstract:</strong> {abstract}</p>"
        if short_description:
            description += f"<p><strong>Summary:</strong> {short_description}</p>"
    else:
        description = short_description

    # Authors/Creators — read from Quarto's structured author field
    # Quarto puts authors under book.author, website.author, root-level author, or metadata.author
    author_list = (
        book.get("author")
        or website.get("author")
        or quarto_config.get("author")
        or metadata.get("author")
        or []
    )
    if isinstance(author_list, str):
        author_list = [{"name": author_list}]
    elif isinstance(author_list, dict):
        author_list = [author_list]

    creators = []
    for author in author_list:
        if isinstance(author, str):
            creator = {"name": author}
        elif isinstance(author, dict):
            creator = {"name": author.get("name", "Unknown")}
            # ORCID
            if author.get("orcid"):
                creator["orcid"] = author["orcid"]
            # Affiliation — read from author.affiliations list
            affiliations = author.get("affiliations", [])
            if affiliations and isinstance(affiliations, list):
                first_aff = affiliations[0]
                if isinstance(first_aff, str):
                    creator["affiliation"] = first_aff
                elif isinstance(first_aff, dict):
                    creator["affiliation"] = first_aff.get("name", "")
        else:
            continue
        creators.append(creator)

    # Fallback if no authors found
    if not creators:
        fallback_name = metadata.get("human-author", metadata.get("creator", "Mike P. Sinn"))
        creators = [{"name": fallback_name, "orcid": DEFAULT_ORCID}]

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

    # Language (ISO 639-3 code)
    language_map = {"en-US": "eng", "en-GB": "eng", "en": "eng"}
    quarto_language = metadata.get("language", "en-US")
    zenodo_language = language_map.get(quarto_language, "eng")

    # Version
    version = metadata.get("version", "1.0")

    # Subjects
    subjects = []
    subject_text = metadata.get("subject", "")
    if subject_text:
        for subj in subject_text.split(","):
            subj = subj.strip()
            if subj:
                subjects.append({"term": subj, "scheme": "user-defined"})

    # Contributors
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

    # Get existing DOI from config (for updating existing deposits)
    existing_doi = metadata.get("doi")

    # Build Zenodo metadata
    zenodo_metadata = {
        "title": title,
        "description": description,
        "creators": creators,
        "keywords": keywords,
        "license": zenodo_license,
        "access_right": "open",
        "publication_date": datetime.now().strftime("%Y-%m-%d"),
        "upload_type": "publication",
        "publication_type": "workingpaper",
        "publisher": metadata.get("publisher", "Decentralized Institutes of Health"),
        "language": zenodo_language,
        "version": version,
    }

    # Store existing DOI for lookup (not sent to Zenodo API, used internally)
    if existing_doi:
        zenodo_metadata["_existing_doi"] = existing_doi

    if related:
        zenodo_metadata["related_identifiers"] = related
    if subjects:
        zenodo_metadata["subjects"] = subjects
    if contributors:
        zenodo_metadata["contributors"] = contributors

    # Add community
    zenodo_metadata["communities"] = [{"identifier": ZENODO_COMMUNITY}]

    # Add notes with category/genre information
    notes_parts = []
    if metadata.get("category"):
        notes_parts.append(f"Category: {metadata['category']}")
    if metadata.get("genre"):
        notes_parts.append(f"Genre: {metadata['genre']}")
    if metadata.get("audience"):
        notes_parts.append(f"Target Audience: {metadata['audience']}")
    if notes_parts:
        zenodo_metadata["notes"] = " | ".join(notes_parts)

    return zenodo_metadata


def save_doi_to_config(config_path: Path, doi: str, zenodo_url: str) -> bool:
    """
    Save DOI and Zenodo URL back to Quarto config file.
    Uses text-based replacement to preserve YAML formatting.

    Args:
        config_path: Path to _quarto-*.yml file
        doi: DOI string (e.g., "10.5281/zenodo.12345678")
        zenodo_url: Zenodo record URL

    Returns:
        True if successful, False otherwise
    """
    import re

    try:
        content = config_path.read_text(encoding='utf-8')

        # Update metadata.doi field
        if re.search(r'^\s+doi:\s*["\']?.*["\']?\s*$', content, re.MULTILINE):
            # DOI field exists, update it
            content = re.sub(
                r'(^\s+doi:\s*["\']?).*?(["\']?\s*$)',
                rf'\g<1>{doi}\g<2>',
                content,
                flags=re.MULTILINE
            )
        else:
            # Add DOI field after metadata section starts
            content = re.sub(
                r'(^metadata:\s*$)',
                rf'\g<1>\n  doi: "{doi}"',
                content,
                flags=re.MULTILINE
            )

        # Update publishing.preprints[zenodo] section if it exists
        # Match the zenodo preprint block and update status + url
        zenodo_section_pattern = r'(- platform: zenodo\s+status: )[^\n]+(.*?url: ")[^"]*(")'
        if re.search(zenodo_section_pattern, content, re.DOTALL):
            content = re.sub(
                zenodo_section_pattern,
                rf'\g<1>auto-uploaded\g<2>{zenodo_url}\g<3>',
                content,
                flags=re.DOTALL
            )
            # Also update the doi: field within the zenodo preprint section
            zenodo_doi_pattern = r'(- platform: zenodo\b.*?doi:\s*)["\']?[^"\'\n]*["\']?'
            if re.search(zenodo_doi_pattern, content, re.DOTALL):
                content = re.sub(
                    zenodo_doi_pattern,
                    rf'\g<1>"{doi}"',
                    content,
                    flags=re.DOTALL
                )

        config_path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"WARNING: Could not save DOI to {config_path}: {e}")
        return False


def upload_paper(
    client: ZenodoClient,
    paper_key: str,
    quarto_config: dict,
    pdf_path: Path,
    draft: bool = True,
    verbose: bool = True,
    save_doi: bool = False,
    config_path: Optional[Path] = None,
) -> Optional[dict]:
    """
    Upload a paper to Zenodo.

    Args:
        client: ZenodoClient instance
        paper_key: Short identifier for the paper (e.g., "iab")
        quarto_config: Parsed Quarto YAML config
        pdf_path: Path to the PDF file
        draft: If True, create draft without publishing
        verbose: Print progress messages
        save_doi: If True, save DOI back to config file after upload
        config_path: Path to config file (required if save_doi=True)

    Returns:
        Dict with deposit info, DOI, and URL if successful, None otherwise
    """
    import sys

    def log(msg: str):
        if verbose:
            print(msg)

    log(f"\n{'='*60}")
    log(f"Uploading: {paper_key}")
    log(f"{'='*60}")

    # Check if PDF exists
    if not pdf_path.exists():
        log(f"WARNING: PDF not found at {pdf_path}")
        log("  -> Skipping (build the paper first)")
        return None

    log(f"[OK] PDF found: {pdf_path.name} ({pdf_path.stat().st_size / 1024:.1f} KB)")

    # Extract metadata
    metadata = extract_zenodo_metadata(quarto_config, paper_key)

    log(f"[OK] Title: {metadata['title']}")
    log(f"[OK] Authors: {', '.join(c['name'] for c in metadata['creators'])}")
    log(f"[OK] License: {metadata['license']}")

    try:
        # Check for existing deposit by DOI first (most reliable)
        existing_doi = metadata.pop("_existing_doi", None)
        record_id = get_record_id_from_doi(existing_doi) if existing_doi else None
        deposit = None
        deposit_id = None
        bucket_url = None

        if record_id:
            log(f"[OK] Found DOI in config: {existing_doi}")
            log(f"[OK] Looking up Zenodo record ID: {record_id}")
            try:
                deposit = client.get_deposit(record_id)
                deposit_id = deposit["id"]
                state = deposit.get("state", "unknown")
                log(f"[OK] Found existing deposit (state: {state})")

                if state == "done":
                    # Published record - create new version
                    log("[OK] Creating new version of published record...")
                    deposit = client.create_new_version(record_id)
                    deposit_id = deposit["id"]
                    bucket_url = deposit["links"]["bucket"]
                    # Clear old files from new version
                    client.delete_all_files(deposit_id)
                    log(f"[OK] New version draft ID: {deposit_id}")
                elif state == "unsubmitted":
                    # Existing draft - update it
                    log("[OK] Updating existing draft...")
                    bucket_url = deposit["links"]["bucket"]
                    client.delete_all_files(deposit_id)
                else:
                    log(f"WARNING: Unexpected deposit state '{state}', creating new deposit...")
                    deposit = None
            except requests.HTTPError as e:
                if e.response.status_code == 404:
                    log(f"WARNING: Record {record_id} not found (may be on different Zenodo instance)")
                    log("  -> Will check for draft by title or create new deposit...")
                else:
                    raise

        # Fall back to title-based search if no DOI or DOI lookup failed
        if deposit is None:
            log("[OK] Checking for existing draft by title...")
            existing_draft = client.find_draft_by_title(metadata["title"])

            if existing_draft:
                deposit_id = existing_draft["id"]
                state = existing_draft.get("state", "unknown")
                log(f"[OK] Found existing deposit by title: {deposit_id} (state: {state})")

                if state == "done":
                    # Published record — must create new version
                    log("[OK] Creating new version of published record...")
                    deposit = client.create_new_version(deposit_id)
                    deposit_id = deposit["id"]
                    bucket_url = deposit["links"]["bucket"]
                    client.delete_all_files(deposit_id)
                    log(f"[OK] New version draft ID: {deposit_id}")
                elif state == "inprogress":
                    # inprogress = submitted but not yet published; try to get editable draft
                    log("[OK] Deposit is 'inprogress' (submitted). Attempting to edit...")
                    try:
                        full_deposit = client.get_deposit(deposit_id)
                        bucket_url = full_deposit["links"]["bucket"]
                        client.delete_all_files(deposit_id)
                    except requests.HTTPError as e:
                        log(f"WARNING: Cannot modify inprogress deposit {deposit_id}: {e}")
                        log("  -> Creating new deposit instead...")
                        deposit = client.create_deposit()
                        deposit_id = deposit["id"]
                        bucket_url = deposit["links"]["bucket"]
                elif state == "unsubmitted":
                    log("  -> Updating existing draft...")
                    full_deposit = client.get_deposit(deposit_id)
                    bucket_url = full_deposit["links"]["bucket"]
                    client.delete_all_files(deposit_id)
                else:
                    log(f"WARNING: Unknown state '{state}', creating new deposit...")
                    deposit = client.create_deposit()
                    deposit_id = deposit["id"]
                    bucket_url = deposit["links"]["bucket"]
            else:
                log("[OK] No existing deposit found, creating new...")
                deposit = client.create_deposit()
                deposit_id = deposit["id"]
                bucket_url = deposit["links"]["bucket"]

        log(f"[OK] Deposit ID: {deposit_id}")

        # Update metadata
        log("[OK] Updating metadata...")
        client.update_metadata(deposit_id, metadata)

        # Upload PDF
        log(f"[OK] Uploading {pdf_path.name}...")
        client.upload_file(deposit_id, pdf_path, bucket_url)

        # Verify upload with GET request
        log("[OK] Verifying upload...")
        verified_deposit = client.get_deposit(deposit_id)
        files = verified_deposit.get("files", [])
        if not files:
            log("ERROR: Upload verification failed - no files found in deposit")
            log("  -> This usually means the upload silently failed")
            return None

        uploaded_file = next((f for f in files if f["filename"] == pdf_path.name), None)
        if not uploaded_file:
            log(f"ERROR: Upload verification failed - {pdf_path.name} not found in deposit")
            log(f"  -> Files in deposit: {[f['filename'] for f in files]}")
            return None

        # Verify file size matches (catch truncated uploads)
        local_size = pdf_path.stat().st_size
        remote_size = uploaded_file.get("filesize", 0)
        if remote_size != local_size:
            log(f"ERROR: File size mismatch!")
            log(f"  -> Local:  {local_size:,} bytes")
            log(f"  -> Remote: {remote_size:,} bytes")
            log("  -> Upload may have been corrupted or truncated")
            return None

        log(f"[OK] Verified: {uploaded_file['filename']} ({remote_size / 1024:.1f} KB, size matches)")

        # Get DOI and URL -- prefer concept DOI (stable across versions)
        version_doi = verified_deposit.get("doi") or verified_deposit.get("metadata", {}).get("prereserve_doi", {}).get("doi")
        concept_doi = verified_deposit.get("conceptdoi")
        concept_recid = verified_deposit.get("conceptrecid")
        zenodo_url = f"{client.base_url.replace('/api', '')}/record/{deposit_id}"

        if draft:
            log("[OK] Draft saved (not published)")
            log(f"  -> Review at: {client.base_url.replace('/api', '')}/deposit/{deposit_id}")
            if version_doi:
                log(f"  -> Pre-reserved DOI: {version_doi}")
            if concept_doi:
                log(f"  -> Concept DOI: {concept_doi}")
        else:
            log("[OK] Publishing...")
            result = client.publish(deposit_id)
            version_doi = result.get("doi")
            concept_doi = result.get("conceptdoi") or concept_doi
            concept_recid = result.get("conceptrecid") or concept_recid
            zenodo_url = result['links']['html']
            log(f"\n[SUCCESS] Published!")
            log(f"  DOI: {version_doi}")
            if concept_doi:
                log(f"  Concept DOI: {concept_doi}")
            log(f"  URL: {zenodo_url}")

        # Use concept DOI/URL for config (stable across versions)
        doi_for_config = concept_doi or version_doi
        url_for_config = f"{client.base_url.replace('/api', '')}/record/{concept_recid}" if concept_recid else zenodo_url

        # Save DOI to config if requested
        if save_doi and config_path and doi_for_config:
            log(f"[OK] Saving concept DOI to {config_path.name}...")
            if save_doi_to_config(config_path, doi_for_config, url_for_config):
                log(f"[OK] Updated config with DOI: {doi_for_config}")
            else:
                log("WARNING: Could not update config file")

        return {
            "id": deposit_id,
            "bucket": bucket_url,
            "doi": doi_for_config,
            "version_doi": version_doi,
            "concept_doi": concept_doi,
            "url": url_for_config,
            "verified": True
        }

    except requests.HTTPError as e:
        print(f"ERROR: Zenodo API error: {e}", file=sys.stderr)
        if hasattr(e, 'response'):
            print(f"  Response: {e.response.text}", file=sys.stderr)
        return None


def get_zenodo_token() -> Optional[str]:
    """Get Zenodo API token from environment (checks ZENODO_TOKEN then ZENODO_ACCESS_TOKEN)."""
    return os.environ.get("ZENODO_TOKEN") or os.environ.get("ZENODO_ACCESS_TOKEN")


def load_quarto_config(config_path: Path) -> dict:
    """Load and parse a Quarto YAML config file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
