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
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
import yaml

# Add project root to path for dih_models imports
_project_root = str(Path(__file__).parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from dih_models.yaml_utils import yaml_safe_load

ZENODO_API = "https://zenodo.org/api"
ZENODO_COMMUNITY = "dih"
DEFAULT_ORCID = "0009-0006-0212-1094"
# No default publisher — must be specified in quarto config
REQUEST_TIMEOUT_SECONDS = 30


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
        self.timeout = REQUEST_TIMEOUT_SECONDS

    def _records_api_headers(self) -> dict:
        return {
            **self.headers,
            "Content-Type": "application/json",
        }

    def create_deposit(self) -> dict:
        """Create a new empty deposit."""
        response = requests.post(
            f"{self.base_url}/deposit/depositions",
            headers=self.headers,
            json={},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def create_version_draft(self, record_id: int) -> dict:
        """Create a new draft version from a published record using deposit API.

        Args:
            record_id: Latest published version ID (NOT concept ID)

        Returns:
            Dict with 'id', 'draft', and 'bucket' keys
        """
        # Use deposit API endpoint for creating new versions
        response = requests.post(
            f"{self.base_url}/deposit/depositions/{record_id}/actions/newversion",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        # Get latest_draft link from response
        latest_draft_url = data.get("links", {}).get("latest_draft")
        if not latest_draft_url:
            raise RuntimeError(f"No latest_draft link in response for record {record_id}")

        # Extract draft ID from URL
        new_id = _extract_numeric_id(latest_draft_url)
        if not new_id:
            raise RuntimeError(f"Could not extract draft ID from URL: {latest_draft_url}")

        # Fetch the draft details
        draft_response = requests.get(
            latest_draft_url,
            headers=self.headers,
            timeout=self.timeout,
        )
        draft_response.raise_for_status()
        draft = draft_response.json()

        # Get bucket URL for file uploads
        bucket_url = draft.get("links", {}).get("bucket")
        if not bucket_url:
            raise RuntimeError(f"Could not resolve bucket URL for draft {new_id}")

        return {"id": int(new_id), "draft": draft, "bucket": bucket_url}

    def update_metadata(self, deposit_id: int, metadata: dict) -> dict:
        """Update deposit metadata."""
        response = requests.put(
            f"{self.base_url}/deposit/depositions/{deposit_id}",
            headers=self.headers,
            json={"metadata": metadata},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def delete_deposit(self, deposit_id: int) -> bool:
        """Delete an entire deposit (draft only, cannot delete published records).

        Args:
            deposit_id: ID of the deposit to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        response = requests.delete(
            f"{self.base_url}/deposit/depositions/{deposit_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        # 204 = successfully deleted, 404 = already gone (also acceptable)
        return response.status_code in (204, 404)

    def delete_all_files(self, deposit_id: int) -> None:
        """Delete all files from a deposit (for updating versions)."""
        response = requests.get(
            f"{self.base_url}/deposit/depositions/{deposit_id}/files",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        for file_info in response.json():
            file_id = file_info["id"]
            delete_response = requests.delete(
                f"{self.base_url}/deposit/depositions/{deposit_id}/files/{file_id}",
                headers=self.headers,
                timeout=self.timeout,
            )
            delete_response.raise_for_status()

    def upload_file(self, deposit_id: int, file_path: Path, bucket_url: str) -> dict:
        """Upload a file to a deposit."""
        with open(file_path, "rb") as f:
            response = requests.put(
                f"{bucket_url}/{file_path.name}",
                headers=self.headers,
                data=f,
                timeout=self.timeout,
            )
        response.raise_for_status()
        return response.json()

    def publish(self, deposit_id: int) -> dict:
        """Publish a deposit (makes it public and assigns DOI)."""
        response = requests.post(
            f"{self.base_url}/deposit/depositions/{deposit_id}/actions/publish",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def publish_record_draft(self, draft_id: int) -> dict:
        """Publish a records API draft created from /records/{id}/versions."""
        response = requests.post(
            f"{self.base_url}/records/{draft_id}/draft/actions/publish",
            headers=self._records_api_headers(),
            json={},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_deposit(self, deposit_id: int) -> dict:
        """Get deposit details."""
        response = requests.get(
            f"{self.base_url}/deposit/depositions/{deposit_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_record(self, record_id: int) -> dict:
        """Get published record details from records API."""
        response = requests.get(
            f"{self.base_url}/records/{record_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def resolve_latest_version_id(self, record_id: int) -> Optional[int]:
        """Resolve a concept or version record ID to the latest published version ID.

        GET /api/records/{id} auto-resolves concept IDs to the latest version,
        so this works regardless of whether record_id is a concept ID or version ID.

        Args:
            record_id: Concept record ID or version record ID

        Returns:
            Latest published version's record ID, or None on failure
        """
        try:
            record = self.get_record(record_id)
            return record.get("id")
        except requests.HTTPError:
            return None

    def get_existing_draft_id(self, record_id: int) -> Optional[int]:
        """Check if a draft version exists for a published record.

        Tries multiple approaches:
        1. Records API 'draft' link
        2. Deposit API 'latest_draft' link

        Args:
            record_id: Published version record ID

        Returns:
            Draft deposit ID if exists, None otherwise
        """
        # Try records API first
        try:
            record = self.get_record(record_id)
            draft_url = record.get('links', {}).get('draft')
            if draft_url:
                draft_response = requests.get(
                    draft_url,
                    headers=self.headers,
                    timeout=self.timeout,
                )
                if draft_response.status_code == 200:
                    draft_data = draft_response.json()
                    draft_id = draft_data.get('id')
                    if draft_id:
                        return draft_id
        except Exception:
            pass

        # Try deposit API -- 'latest_draft' link on the deposit
        try:
            deposit = self.get_deposit(record_id)
            latest_draft_url = deposit.get('links', {}).get('latest_draft')
            if latest_draft_url:
                draft_id = _extract_numeric_id(latest_draft_url)
                if draft_id and draft_id != record_id:
                    # Verify the draft is accessible
                    draft_response = requests.get(
                        latest_draft_url,
                        headers=self.headers,
                        timeout=self.timeout,
                    )
                    if draft_response.status_code == 200:
                        return draft_id
        except Exception:
            pass

        return None

    def find_drafts_by_concept(self, concept_id: int) -> list[int]:
        """Find all draft deposits for a given concept record ID.

        Args:
            concept_id: The concept record ID

        Returns:
            List of draft deposit IDs for this concept
        """
        draft_ids = []
        page = 1

        try:
            while True:
                response = requests.get(
                    f"{self.base_url}/deposit/depositions",
                    headers=self.headers,
                    params={"page": page, "size": 100},
                    timeout=self.timeout,
                )

                if response.status_code == 403:
                    # Try without pagination params
                    response = requests.get(
                        f"{self.base_url}/deposit/depositions",
                        headers=self.headers,
                        timeout=self.timeout,
                    )

                response.raise_for_status()
                deposits = response.json()

                if not deposits:
                    break

                # Filter for drafts with matching concept ID
                for deposit in deposits:
                    is_draft = not deposit.get('submitted', False)
                    deposit_concept_id = deposit.get('conceptrecid')

                    # Convert both to int for comparison (API may return string or int)
                    if is_draft and deposit_concept_id and int(deposit_concept_id) == int(concept_id):
                        draft_ids.append(deposit.get('id'))

                # If we got fewer than page size, we're done
                if len(deposits) < 100:
                    break

                page += 1

        except Exception:
            pass

        return draft_ids

    def verify_bucket_access(self, bucket_url: str) -> bool:
        """Check that draft bucket is reachable."""
        response = requests.get(
            bucket_url,
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.status_code == 200

    def find_deposit_by_title(self, title: str) -> Optional[dict]:
        """Find an existing deposit (draft or published) by title.

        Returns the first matching deposit, preferring drafts over published.
        """
        draft_match = None
        published_match = None
        page = 1
        while True:
            response = requests.get(
                f"{self.base_url}/deposit/depositions",
                headers=self.headers,
                params={"page": page, "size": 100},
                timeout=self.timeout,
            )
            response.raise_for_status()
            deposits = response.json()
            if not deposits:
                break
            for deposit in deposits:
                deposit_title = deposit.get("metadata", {}).get("title", "")
                if deposit_title != title:
                    continue
                state = deposit.get("state", "")
                if state in ("unsubmitted", "inprogress") and draft_match is None:
                    draft_match = deposit
                elif state == "done" and published_match is None:
                    published_match = deposit
                if draft_match:
                    return draft_match  # Prefer drafts
            if len(deposits) < 100:
                break
            page += 1
        return draft_match or published_match


def _extract_numeric_id(value: str | None) -> Optional[int]:
    """Extract trailing numeric ID from Zenodo URL/identifier."""
    if not value:
        return None
    match = re.search(r"(\d+)(?:/?$)", value)
    if not match:
        return None
    return int(match.group(1))


def parse_bibtex_file(bib_path: Path) -> dict:
    """Parse a BibTeX file and return a dict of {cite_key: entry_dict}.

    Args:
        bib_path: Path to references.bib file

    Returns:
        Dict mapping citation keys to parsed BibTeX entries
    """
    if not bib_path.exists():
        return {}

    try:
        import bibtexparser
        from bibtexparser.bparser import BibTexParser

        with open(bib_path, 'r', encoding='utf-8') as f:
            parser = BibTexParser(common_strings=True)
            bib_database = bibtexparser.load(f, parser=parser)

        # Convert to dict keyed by ID
        return {entry['ID']: entry for entry in bib_database.entries}
    except ImportError:
        # bibtexparser not installed
        return {}
    except Exception:
        # Parsing failed
        return {}


def extract_cited_references(paper_key: str, quarto_config: dict, project_root: Path) -> tuple[list[str], list[dict]]:
    """Extract references that are actually cited in the paper.

    Args:
        paper_key: Paper identifier
        quarto_config: Quarto config dict
        project_root: Project root path

    Returns:
        Tuple of (references, related_identifiers):
        - references: list of plain strings for Zenodo references field
        - related_identifiers: list of dicts with identifier/relation/scheme for DOI cross-links
    """
    import re

    # Find the main QMD file and any included files
    dih_render = quarto_config.get("dih-render", {})
    index_source = dih_render.get("index-source")
    if not index_source:
        return [], []

    # Parse references.bib
    bib_path = project_root / "references.bib"
    bib_entries = parse_bibtex_file(bib_path)
    if not bib_entries:
        return [], []

    # Scan QMD files for citations
    cited_keys = set()
    qmd_files = []

    # Add main file
    main_qmd = project_root / index_source
    if main_qmd.exists():
        qmd_files.append(main_qmd)

    # Add any included chapters (for books)
    book_config = quarto_config.get("book", {})
    if isinstance(book_config, dict):
        chapters = book_config.get("chapters", [])
        for chapter in chapters:
            if isinstance(chapter, str):
                chapter_path = project_root / chapter
                if chapter_path.exists():
                    qmd_files.append(chapter_path)

    # Add files from project.render (e.g., appendix QMD files)
    project_config = quarto_config.get("project", {})
    if isinstance(project_config, dict):
        render_list = project_config.get("render", [])
        if isinstance(render_list, list):
            for render_entry in render_list:
                if isinstance(render_entry, str) and render_entry.endswith(".qmd"):
                    render_path = project_root / render_entry
                    if render_path.exists() and render_path not in qmd_files:
                        qmd_files.append(render_path)

    # Scan all QMD files for citation keys
    citation_pattern = re.compile(r'@([a-zA-Z0-9_-]+)')
    for qmd_file in qmd_files:
        try:
            content = qmd_file.read_text(encoding='utf-8')
            for match in citation_pattern.finditer(content):
                cite_key = match.group(1)
                if cite_key in bib_entries:
                    cited_keys.add(cite_key)
        except Exception:
            continue

    # Build Zenodo reference list (plain strings) and related_identifiers (for DOI cross-links)
    references = []
    related_identifiers = []
    for cite_key in sorted(cited_keys):
        entry = bib_entries[cite_key]

        # Format raw reference string
        authors = entry.get('author', 'Unknown')
        year = entry.get('year', 'n.d.')
        title = entry.get('title', 'Untitled')

        # Build citation string
        raw_ref = f"{authors} ({year}). {title}."

        # Add journal/publisher info if available
        if entry.get('journal'):
            raw_ref += f" {entry['journal']}"
            if entry.get('volume'):
                raw_ref += f", {entry['volume']}"
            if entry.get('pages'):
                raw_ref += f", {entry['pages']}"
            raw_ref += "."
        elif entry.get('publisher'):
            raw_ref += f" {entry['publisher']}."

        # Append DOI or URL to the string representation
        if entry.get('doi'):
            raw_ref += f" doi:{entry['doi']}"
            related_identifiers.append({
                "identifier": entry['doi'],
                "relation": "cites",
                "scheme": "doi",
            })
        elif entry.get('url'):
            raw_ref += f" {entry['url']}"

        references.append(raw_ref)

    return references, related_identifiers


def extract_abstract_from_qmd(paper_key: str, quarto_config: dict, project_root: Path) -> str:
    """Extract abstract from the main QMD file and resolve Quarto variables.

    Args:
        paper_key: Paper identifier (e.g., 'wishocracy')
        quarto_config: Quarto config dict
        project_root: Project root path

    Returns:
        Resolved abstract text, or empty string if not found
    """
    # Get the main QMD file path from dih-render.index-source
    dih_render = quarto_config.get("dih-render", {})
    index_source = dih_render.get("index-source")

    if not index_source:
        return ""

    qmd_path = project_root / index_source
    if not qmd_path.exists():
        return ""

    try:
        # Read the QMD file
        with open(qmd_path, encoding="utf-8") as f:
            content = f.read()

        # Try to extract abstract from frontmatter first
        import re
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            try:
                frontmatter = yaml_safe_load(frontmatter_match.group(1))
                if isinstance(frontmatter, dict) and "abstract" in frontmatter:
                    abstract = frontmatter["abstract"]
                    if abstract:
                        # Resolve variables and return
                        return resolve_quarto_variables(str(abstract), project_root)
            except:
                pass

        # Try to extract from content (look for ## Abstract or # Abstract heading)
        abstract_match = re.search(r'^##?\s+Abstract\s*\n\n(.*?)(?=\n##?\s+|\Z)', content, re.MULTILINE | re.DOTALL)
        if abstract_match:
            abstract = abstract_match.group(1).strip()
            # Clean up markdown formatting
            abstract = re.sub(r'\{.*?\}', '', abstract)  # Remove attributes
            abstract = re.sub(r'\n+', ' ', abstract)  # Collapse newlines
            abstract = re.sub(r'\s+', ' ', abstract)  # Collapse whitespace
            # Resolve variables and return
            return resolve_quarto_variables(abstract, project_root)

        return ""
    except Exception:
        return ""


def resolve_quarto_variables(text: str, project_root: Path) -> str:
    """Resolve Quarto variables like {{< var param_name >}} to actual values.

    Args:
        text: Text containing Quarto variables
        project_root: Project root path

    Returns:
        Text with variables resolved
    """
    from lib.yaml_sync_utils import substitute_quarto_variables

    # Load _variables.yml
    variables_path = project_root / "_variables.yml"
    if not variables_path.exists():
        return text

    try:
        with open(variables_path, encoding="utf-8") as f:
            variables = yaml_safe_load(f)
    except:
        return text

    # Use existing substitute_quarto_variables function
    return substitute_quarto_variables(text, variables)


def extract_zenodo_metadata(quarto_config: dict, paper_key: str, project_root: Path | None = None) -> dict:
    """
    Convert Quarto metadata to Zenodo metadata format.

    Args:
        quarto_config: Quarto configuration dict
        paper_key: Paper identifier
        project_root: Project root path (optional, for extracting abstract from QMD)

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

    # Fallback: extract abstract from main QMD file if not in config
    if not abstract and project_root:
        abstract = extract_abstract_from_qmd(paper_key, quarto_config, project_root)

    short_description = (
        book.get("description") or
        website.get("description") or
        metadata.get("description", "")
    )

    # Clean up abstract (remove extra whitespace from YAML multiline)
    if abstract:
        abstract = " ".join(abstract.split())

    # Resolve Quarto variables in short_description if project_root available
    if short_description and project_root:
        short_description = resolve_quarto_variables(short_description, project_root)

    # Escape dollar signs to prevent LaTeX/markdown interpretation issues
    # Do this AFTER resolving variables
    if abstract:
        abstract = abstract.replace("$", "\\$")
    if short_description:
        short_description = short_description.replace("$", "\\$")

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
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
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
        website_note = f'<p><strong>Website:</strong> <a href="{site_url}">{site_url}</a></p>'
        if description and not description.lstrip().startswith("<"):
            description = f"<p>{description}</p>"
        description = f"{website_note}{description}" if description else website_note
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

    # Subjects (Zenodo new API format: {"subject": "..."})
    subjects = []
    subject_text = metadata.get("subject", "")
    if subject_text:
        for subj in subject_text.split(","):
            subj = subj.strip()
            if subj:
                subjects.append({"subject": subj})

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

    zenodo_section = metadata.get("zenodo", {})
    if not isinstance(zenodo_section, dict):
        zenodo_section = {}
    publisher = zenodo_section.get("publisher") or metadata.get("publisher")
    if not publisher:
        raise ValueError(
            f"No publisher found in quarto config metadata. "
            f"Add 'publisher' to the zenodo section of your _quarto-*.yml config."
        )

    # Build copyright/rights statement
    primary_author = creators[0]['name'] if creators else "Unknown"
    current_year = datetime.now().year
    rights_statement = f"© {current_year} {primary_author}. Licensed under {quarto_license}."

    # Build Zenodo metadata
    zenodo_metadata = {
        "title": title,
        "description": description,
        "creators": creators,
        "keywords": keywords,
        "license": zenodo_license,
        "rights": rights_statement,
        "access_right": "open",
        "publication_date": datetime.now().strftime("%Y-%m-%d"),
        "upload_type": "publication",
        "publication_type": "workingpaper",
        "publisher": publisher,
        "language": zenodo_language,
        "version": version,
    }

    # Store existing DOI for lookup (not sent to Zenodo API, used internally)
    if existing_doi:
        zenodo_metadata["_existing_doi"] = existing_doi

    # Add references from .bib file (only cited references)
    if project_root:
        ref_strings, ref_related = extract_cited_references(paper_key, quarto_config, project_root)
        if ref_strings:
            zenodo_metadata["references"] = ref_strings
        if ref_related:
            related.extend(ref_related)

    # Add grants/funding if specified in config
    grants = metadata.get("grants") or zenodo_section.get("grants")
    if grants and isinstance(grants, list):
        zenodo_grants = []
        for grant in grants:
            if isinstance(grant, dict):
                grant_dict = {}
                if grant.get("title"):
                    grant_dict["title"] = grant["title"]
                if grant.get("code"):
                    grant_dict["code"] = grant["code"]
                if grant.get("funder"):
                    grant_dict["funder"] = {"name": grant["funder"]}
                if grant_dict:
                    zenodo_grants.append(grant_dict)
        if zenodo_grants:
            zenodo_metadata["grants"] = zenodo_grants

    # Add alternate identifiers (arXiv, SSRN, etc.)
    alternate_ids = metadata.get("alternate_ids") or zenodo_section.get("alternate_ids")
    if alternate_ids and isinstance(alternate_ids, list):
        zenodo_alt_ids = []
        for alt_id in alternate_ids:
            if isinstance(alt_id, dict) and alt_id.get("identifier") and alt_id.get("scheme"):
                zenodo_alt_ids.append({
                    "identifier": alt_id["identifier"],
                    "scheme": alt_id["scheme"]
                })
        if zenodo_alt_ids:
            zenodo_metadata["alternate_identifiers"] = zenodo_alt_ids

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


def save_doi_to_config(
    config_path: Path,
    doi: str,
    zenodo_url: str,
) -> bool:
    """
    Save concept DOI and Zenodo URL back to Quarto config file.
    Skips writing if the concept DOI already matches (avoids unnecessary rebuilds).
    Uses text-based replacement to preserve YAML formatting.

    Args:
        config_path: Path to _quarto-*.yml file
        doi: Concept DOI string (stable across versions)
        zenodo_url: Zenodo record URL

    Returns:
        True if saved (or already correct), False on error
    """
    try:
        lines = config_path.read_text(encoding='utf-8').splitlines(keepends=True)

        metadata_idx = next((i for i, line in enumerate(lines) if re.match(r"^metadata:\s*$", line.rstrip("\r\n"))), None)
        if metadata_idx is None:
            return False

        metadata_end = len(lines)
        for i in range(metadata_idx + 1, len(lines)):
            stripped = lines[i].strip()
            if stripped and not lines[i].startswith((" ", "\t", "#")):
                metadata_end = i
                break

        doi_idx = None
        doi_comment_idx = None
        changed = False

        for i in range(metadata_idx + 1, metadata_end):
            if re.match(r"^  # Zenodo Concept DOI", lines[i]):
                doi_comment_idx = i
            if re.match(r"^  doi:\s*", lines[i]):
                doi_idx = i

        # Check if DOI already matches -- skip writing to avoid unnecessary rebuilds
        if doi_idx is not None:
            existing_line = lines[doi_idx].strip()
            expected = f'doi: "{doi}"'
            if existing_line == expected:
                # DOI already correct; check zenodo platform block too
                zenodo_block_ok = True
                for i, line in enumerate(lines):
                    if re.match(r"^\s*-\s*platform:\s*zenodo\s*$", line):
                        item_indent = len(line) - len(line.lstrip(" "))
                        child_prefix = " " * (item_indent + 2)
                        block_end = len(lines)
                        for j in range(i + 1, len(lines)):
                            candidate = lines[j]
                            stripped_c = candidate.strip()
                            candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                            if stripped_c.startswith("- ") and candidate_indent == item_indent:
                                block_end = j
                                break
                            if stripped_c and candidate_indent < item_indent:
                                block_end = j
                                break
                        for j in range(i + 1, block_end):
                            if lines[j].startswith(f"{child_prefix}status:") and "auto-uploaded" not in lines[j]:
                                zenodo_block_ok = False
                            elif lines[j].startswith(f"{child_prefix}doi:") and doi not in lines[j]:
                                zenodo_block_ok = False
                        break
                if zenodo_block_ok:
                    return True  # Nothing to change

        # Add comment block if missing
        if doi_comment_idx is None:
            comment_block = [
                '  # Zenodo Concept DOI (stable across all versions - use for citations and new versions)\n',
            ]
            insert_pos = doi_idx if doi_idx is not None else metadata_idx + 1
            for line in reversed(comment_block):
                lines.insert(insert_pos, line)
            if doi_idx is not None:
                doi_idx += len(comment_block)
            changed = True

        # Update/add concept DOI
        if doi_idx is not None:
            new_line = f'  doi: "{doi}"\n'
            if lines[doi_idx] != new_line:
                lines[doi_idx] = new_line
                changed = True
        else:
            insert_pos = doi_comment_idx + 1 if doi_comment_idx is not None else metadata_idx + 1
            lines.insert(insert_pos, f'  doi: "{doi}"\n')
            changed = True

        # Update zenodo platform block
        for i, line in enumerate(lines):
            if not re.match(r"^\s*-\s*platform:\s*zenodo\s*$", line):
                continue
            item_indent = len(line) - len(line.lstrip(" "))
            child_prefix = " " * (item_indent + 2)
            block_end = len(lines)
            for j in range(i + 1, len(lines)):
                candidate = lines[j]
                stripped = candidate.strip()
                candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                if stripped.startswith("- ") and candidate_indent == item_indent:
                    block_end = j
                    break
                if stripped and candidate_indent < item_indent:
                    block_end = j
                    break

            for j in range(i + 1, block_end):
                if lines[j].startswith(f"{child_prefix}status:"):
                    new_line = f"{child_prefix}status: auto-uploaded\n"
                    if lines[j] != new_line:
                        lines[j] = new_line
                        changed = True
                elif lines[j].startswith(f"{child_prefix}url:"):
                    new_line = f'{child_prefix}url: "{zenodo_url}"\n'
                    if lines[j] != new_line:
                        lines[j] = new_line
                        changed = True
                elif lines[j].startswith(f"{child_prefix}doi:"):
                    new_line = f'{child_prefix}doi: "{doi}"\n'
                    if lines[j] != new_line:
                        lines[j] = new_line
                        changed = True
            break

        if changed:
            config_path.write_text("".join(lines), encoding='utf-8')
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
    project_root: Optional[Path] = None,
    metadata_only: bool = False,
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
        project_root: Project root path (optional, for extracting abstracts from QMD)
        metadata_only: If True, only update metadata (skip file delete/upload)

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

    # Extract metadata (with project_root for extracting abstracts from QMD)
    if project_root is None:
        # Try to infer from config_path if available
        if config_path:
            project_root = config_path.parent
        else:
            # Fallback: infer from pdf_path
            project_root = pdf_path.parent.parent

    metadata = extract_zenodo_metadata(quarto_config, paper_key, project_root=project_root)

    log(f"[OK] Title: {metadata['title']}")
    log(f"[OK] Authors: {', '.join(c['name'] for c in metadata['creators'])}")
    log(f"[OK] License: {metadata['license']}")

    try:
        # Check for existing deposit by DOI first (most reliable)
        existing_doi = metadata.pop("_existing_doi", None)
        record_id = get_record_id_from_doi(existing_doi) if existing_doi else None
        if record_id:
            resolved_id = client.resolve_latest_version_id(record_id)
            if resolved_id and resolved_id != record_id:
                log(f"[OK] Resolved concept record {record_id} -> latest version {resolved_id}")
                record_id = resolved_id
        deposit = None
        deposit_id = None
        bucket_url = None
        publish_via_records_api = False

        if record_id:
            log(f"[OK] Found DOI in config: {existing_doi}")
            log(f"[OK] Creating new version draft from existing record: {record_id}")
            try:
                version_info = client.create_version_draft(record_id)
                deposit_id = version_info["id"]
                bucket_url = version_info["bucket"]
                publish_via_records_api = True
                if not metadata_only:
                    client.delete_all_files(deposit_id)
                log(f"[OK] New version draft ID: {deposit_id}")
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    log(f"WARNING: Existing DOI record not found on Zenodo ({record_id}); falling back to draft/new deposit flow")
                elif e.response is not None and e.response.status_code == 400 and "remove all files" in e.response.text.lower():
                    # A draft already exists with files; find it, clean files, and reuse
                    log(f"WARNING: Existing draft has files; looking for draft to reuse...")
                    draft_id = client.get_existing_draft_id(record_id)
                    if draft_id:
                        log(f"[OK] Found existing draft: {draft_id}; clearing files and reusing")
                        client.delete_all_files(draft_id)
                        draft_deposit = client.get_deposit(draft_id)
                        deposit_id = draft_id
                        bucket_url = draft_deposit.get("links", {}).get("bucket")
                        publish_via_records_api = False
                        log(f"[OK] Reusing draft ID: {deposit_id}")
                    else:
                        log(f"WARNING: Could not find existing draft; falling back to new deposit")
                else:
                    raise

        # Fall back to title-based search if no DOI or DOI lookup failed
        if deposit_id is None:
            log("[OK] Checking for existing deposit by title...")
            existing = client.find_deposit_by_title(metadata["title"])

            if existing:
                found_id = existing["id"]
                state = existing.get("state", "unknown")
                log(f"[OK] Found existing deposit by title: {found_id} (state: {state})")

                if state == "done":
                    # Published deposit -- create new version from it
                    log(f"[OK] Published deposit found; creating new version from {found_id}...")
                    resolved_id = client.resolve_latest_version_id(found_id)
                    version_record_id = resolved_id or found_id
                    try:
                        version_info = client.create_version_draft(version_record_id)
                        deposit_id = version_info["id"]
                        bucket_url = version_info["bucket"]
                        publish_via_records_api = True
                        if not metadata_only:
                            client.delete_all_files(deposit_id)
                        log(f"[OK] New version draft ID: {deposit_id}")
                    except requests.HTTPError as e:
                        log(f"WARNING: Could not create new version from {version_record_id}: {e}")
                        log("  -> Creating new deposit instead...")
                        deposit = client.create_deposit()
                        deposit_id = deposit["id"]
                        bucket_url = deposit["links"]["bucket"]
                elif state == "inprogress":
                    # inprogress = submitted but not yet published; try to get editable draft
                    log("[OK] Deposit is 'inprogress' (submitted). Attempting to edit...")
                    try:
                        full_deposit = client.get_deposit(found_id)
                        deposit_id = found_id
                        bucket_url = full_deposit["links"]["bucket"]
                        if not metadata_only:
                            client.delete_all_files(deposit_id)
                    except requests.HTTPError as e:
                        log(f"WARNING: Cannot modify inprogress deposit {found_id}: {e}")
                        log("  -> Creating new deposit instead...")
                        deposit = client.create_deposit()
                        deposit_id = deposit["id"]
                        bucket_url = deposit["links"]["bucket"]
                elif state == "unsubmitted":
                    deposit_id = found_id
                    log("  -> Updating existing draft...")
                    full_deposit = client.get_deposit(deposit_id)
                    bucket_url = full_deposit["links"]["bucket"]
                    if not metadata_only:
                        client.delete_all_files(deposit_id)
                else:
                    log(f"WARNING: Deposit state '{state}' is not editable, creating new deposit...")
                    deposit = client.create_deposit()
                    deposit_id = deposit["id"]
                    bucket_url = deposit["links"]["bucket"]
            else:
                log("[OK] No existing deposit found, creating new...")
                deposit = client.create_deposit()
                deposit_id = deposit["id"]
                bucket_url = deposit["links"]["bucket"]

        assert deposit_id is not None, "No deposit ID resolved"
        assert bucket_url is not None, "No bucket URL resolved"

        log(f"[OK] Deposit ID: {deposit_id}")

        # Update metadata
        log("[OK] Updating metadata...")
        client.update_metadata(deposit_id, metadata)

        if metadata_only:
            log(f"[OK] Metadata-only update (skipping file upload for {pdf_path.name})")
            verified_deposit = client.get_deposit(deposit_id)
        else:
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
            if publish_via_records_api:
                result = client.publish_record_draft(deposit_id)
            else:
                result = client.publish(deposit_id)
            version_doi = result.get("doi")
            concept_doi = result.get("conceptdoi") or concept_doi
            concept_recid = result.get("conceptrecid") or concept_recid
            zenodo_url = result.get("links", {}).get("self_html") or result.get("links", {}).get("html") or zenodo_url
            log(f"\n[SUCCESS] Published!")
            log(f"  DOI: {version_doi}")
            if concept_doi:
                log(f"  Concept DOI: {concept_doi}")
            log(f"  URL: {zenodo_url}")

        # Use concept DOI/URL for config (stable across versions)
        concept_doi_for_config = concept_doi or version_doi
        concept_url_for_config = f"{client.base_url.replace('/api', '')}/record/{concept_recid}" if concept_recid else zenodo_url

        # Save concept DOI to config if requested
        if save_doi and config_path and concept_doi_for_config:
            log(f"[OK] Saving concept DOI to {config_path.name}...")
            if save_doi_to_config(config_path, concept_doi_for_config, concept_url_for_config):
                log(f"[OK] Config DOI: {concept_doi_for_config}")
            else:
                log("WARNING: Could not update config file")

        return {
            "id": deposit_id,
            "bucket": bucket_url,
            "doi": concept_doi_for_config,  # Primary DOI (concept, stable across versions)
            "concept_doi": concept_doi,      # Concept DOI (same as 'doi' field)
            "url": concept_url_for_config,
            "verified": True
        }

    except requests.HTTPError as e:
        print(f"ERROR: Zenodo API error: {e}", file=sys.stderr)
        response = e.response
        if response is not None:
            print(f"  Response: {response.text}", file=sys.stderr)
        return None
    except requests.RequestException as e:
        print(f"ERROR: Zenodo request failed: {e}", file=sys.stderr)
        return None


def get_zenodo_token() -> Optional[str]:
    """Get Zenodo API token from environment (checks ZENODO_TOKEN then ZENODO_ACCESS_TOKEN)."""
    return os.environ.get("ZENODO_TOKEN") or os.environ.get("ZENODO_ACCESS_TOKEN")


def load_quarto_config(config_path: Path) -> dict:
    """Load and parse a Quarto YAML config file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml_safe_load(f)
