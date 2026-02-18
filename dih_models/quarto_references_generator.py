#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quarto References Generator
===========================

Scans root-level _quarto-*.yml config files and adds papers with DOIs
to references.bib if not already present.

This ensures all project papers are citable with proper academic attribution.

Usage:
    from dih_models.quarto_references_generator import update_references_from_quarto
    added = update_references_from_quarto(project_root)

Output:
    Appends new entries to references.bib

Functions:
- extract_paper_citation_info() - Extract citation-relevant info from Quarto config
- generate_bibtex_entry() - Generate BibTeX entry from paper metadata
- update_references_from_quarto() - Main function to scan and update references.bib
"""

import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from dih_models.yaml_utils import load_quarto_config

from dih_models.reference_parser import parse_references_bib
from dih_models.references_bib_utils import parse_bib_entries, save_references_bib


def extract_paper_citation_info(config_path: Path, config_name: str) -> Optional[Dict[str, Any]]:
    """
    Extract citation-relevant info from a Quarto config file.

    Similar to papers_qmd_generator.extract_paper_info() but focused on
    fields needed for BibTeX citations.

    Args:
        config_path: Path to the _quarto-*.yml file
        config_name: Name of the config (e.g., "iab", "dfda-impact")

    Returns:
        Dict with citation info, or None if not citable (no DOI)
    """
    config = load_quarto_config(config_path)

    if not config:
        return None

    # Skip test and manual configs
    if config_name in ("test", "manual"):
        return None

    # Extract title from book or website section
    title = None
    description = None
    site_url = None

    if "book" in config:
        book = config["book"]
        title = book.get("title")
        description = book.get("description") or book.get("abstract")
        site_url = book.get("site-url")
    elif "website" in config:
        website = config["website"]
        title = website.get("title")
        description = website.get("description")
        site_url = website.get("site-url")

    # Skip if no title
    if not title:
        return None

    # Get metadata section
    metadata = config.get("metadata", {}) or {}

    # Get DOI (required for academic citation)
    doi = metadata.get("doi")
    if not doi:
        # Check preprints section
        publishing = metadata.get("publishing", {}) or {}
        preprints = publishing.get("preprints", []) or []
        for preprint in preprints:
            if preprint.get("doi"):
                doi = preprint["doi"]
                break

    if not doi:
        return None  # Skip papers without DOI

    # Get author info from config.author list
    authors = config.get("author", [])
    author_name = None

    if isinstance(authors, list) and authors:
        author_name = authors[0].get("name")
        # Get institution from first author's affiliations
        affiliations = authors[0].get("affiliations", [])
        if affiliations and isinstance(affiliations, list):
            institution = affiliations[0].get("name", "")
        else:
            institution = ""
    elif isinstance(authors, dict):
        author_name = authors.get("name")
        institution = ""
    else:
        author_name = metadata.get("primary-author") or metadata.get("human-author")
        institution = ""

    if not author_name:
        author_name = "Unknown"

    # Default institution if not found
    if not institution:
        institution = "Institute for Accelerated Medicine"

    # Convert "Mike P. Sinn" to "Sinn, Mike P." for BibTeX
    author_bibtex = author_name
    if author_name and " " in author_name:
        parts = author_name.rsplit(" ", 1)
        if len(parts) == 2:
            author_bibtex = f"{parts[1]}, {parts[0]}"

    # Get year from metadata
    year = metadata.get("copyright-year", str(date.today().year))

    # Get URL
    url = site_url or ""

    # Get paper type/edition
    paper_type = metadata.get("format", "Working Paper")
    edition = metadata.get("edition", "")

    # Generate citation key: config-name-paper-year
    # e.g., dfda-impact-paper-2025
    citation_key = f"{config_name}-paper-{year}"

    return {
        "citation_key": citation_key,
        "title": title,
        "author": author_bibtex,
        "year": year,
        "doi": doi,
        "url": url,
        "description": description or "",
        "institution": institution,
        "paper_type": paper_type,
        "edition": edition,
        "source_file": config_path.name,
    }


def generate_bibtex_entry(metadata: Dict[str, Any]) -> str:
    """
    Generate a BibTeX @techreport entry from paper metadata.

    Args:
        metadata: Dict with citation info from extract_paper_citation_info()

    Returns:
        BibTeX entry string
    """
    # Escape special characters for BibTeX
    def escape_bibtex(text: str) -> str:
        if not text:
            return ""
        text = text.replace("$", r"\$")
        text = text.replace("%", r"\%")
        text = text.replace("&", r"\&")
        text = text.replace("_", r"\_")
        return text

    title = escape_bibtex(metadata["title"])
    description = escape_bibtex(metadata["description"])

    # Build note field - only include edition if present, no internal metadata
    note = metadata.get("edition", "") or ""

    entry = f"""@techreport{{{metadata['citation_key']},
  title = {{{title}}},
  author = {{{metadata['author']}}},
  year = {{{metadata['year']}}},
  institution = {{{metadata['institution']}}},
  type = {{{metadata['paper_type']}}},
  doi = {{{metadata['doi']}}},
  url = {{{metadata['url']}}},
  urldate = {{{date.today().isoformat()}}},
  note = {{{note}}},
  abstract = {{{description}}},
}}"""
    return entry


def needs_update(existing: Dict[str, Any], new_metadata: Dict[str, Any]) -> bool:
    """
    Check if an existing reference needs to be updated based on new metadata.

    Compares key fields that might change in Quarto configs.
    """
    # Fields to compare (normalized for comparison)
    def normalize(text: str) -> str:
        if not text:
            return ""
        # Remove BibTeX escapes and normalize whitespace
        text = text.replace(r"\$", "$").replace(r"\%", "%").replace(r"\&", "&").replace(r"\_", "_")
        return " ".join(text.split()).strip()

    # Compare title
    if normalize(existing.get("title", "")) != normalize(new_metadata.get("title", "")):
        return True

    # Compare abstract/description
    if normalize(existing.get("quote", "")) != normalize(new_metadata.get("description", "")):
        return True

    # Compare URL
    if existing.get("url", "") != new_metadata.get("url", ""):
        return True

    # Compare DOI
    if existing.get("doi", "").lower() != new_metadata.get("doi", "").lower():
        return True

    # Check for junk in note field that needs cleaning
    existing_note = existing.get("note", "")
    if "Auto-generated from" in existing_note:
        return True

    return False


def update_references_from_quarto(
    project_root: Path,
    existing_citation_data: Optional[Dict[str, Dict[str, Any]]] = None,
) -> List[Tuple[str, str]]:
    """
    Scan Quarto YAML configs and add/update papers in references.bib.

    Reads all _quarto-*.yml files in project root, extracts citation info
    for papers with DOIs, and either adds new entries or updates existing
    ones if the metadata has changed.

    Uses the shared save_references_bib() utility which:
    - Auto-alphabetizes entries on save
    - Detects and errors on duplicates (key, DOI, title)
    - Logs all issues before crashing

    Args:
        project_root: Root directory of the project
        existing_citation_data: Pre-parsed citation data from parse_references_bib().
                                If provided, skips re-parsing references.bib (saves ~2s).

    Returns:
        List of (citation_key, title) tuples for papers that were added or updated
    """
    bib_path = project_root / "references.bib"

    # Parse existing entries using shared utility (preserves full text)
    existing_entries = parse_bib_entries(bib_path)
    entries_by_key = {e["key"]: e for e in existing_entries}

    # Get existing citation data (full metadata) for needs_update checks
    # Reuse pre-parsed data if available (avoids expensive bibtexparser re-parse)
    existing_refs = existing_citation_data if existing_citation_data is not None else parse_references_bib(bib_path)
    existing_keys = set(existing_refs.keys())

    # Also build a map of DOIs to keys (to detect duplicates by DOI)
    existing_dois = {}
    for key, data in existing_refs.items():
        doi = data.get("doi", "")
        if doi:
            existing_dois[doi.lower()] = key

    # Find all root-level Quarto config files
    yaml_files = sorted(project_root.glob("_quarto-*.yml"))

    added_papers = []
    updated_papers = []
    modified = False

    for yaml_path in yaml_files:
        # Extract config name from filename
        match = re.match(r"_quarto-(.+)\.yml", yaml_path.name)
        if not match:
            continue

        config_name = match.group(1)

        try:
            metadata = extract_paper_citation_info(yaml_path, config_name)
        except Exception as e:
            print(f"[WARN] Could not parse {yaml_path.name}: {e}")
            continue

        if not metadata:
            continue

        citation_key = metadata["citation_key"]
        doi = metadata["doi"]
        doi_lower = doi.lower() if doi else ""

        # Check if already exists by key
        if citation_key in existing_keys:
            # Check if it needs updating
            existing_data = existing_refs.get(citation_key, {})
            if needs_update(existing_data, metadata):
                new_entry_text = generate_bibtex_entry(metadata)
                # Update in memory
                entries_by_key[citation_key]["text"] = new_entry_text
                updated_papers.append((citation_key, metadata["title"]))
                modified = True
            continue

        # Check if already exists by DOI (different key, same paper)
        if doi_lower and doi_lower in existing_dois:
            existing_key = existing_dois[doi_lower]
            # Update the existing entry with new metadata
            existing_data = existing_refs.get(existing_key, {})
            if needs_update(existing_data, metadata):
                new_entry_text = generate_bibtex_entry(metadata)
                entries_by_key[existing_key]["text"] = new_entry_text
                updated_papers.append((existing_key, metadata["title"]))
                modified = True
            continue

        # Check for similar keys (in case year changed)
        base_key = citation_key.rsplit("-", 1)[0]  # Remove year
        similar_keys = [k for k in existing_keys if k.startswith(base_key)]
        if similar_keys:
            # Update the existing similar key
            existing_key = similar_keys[0]
            existing_data = existing_refs.get(existing_key, {})
            if needs_update(existing_data, metadata):
                new_entry_text = generate_bibtex_entry(metadata)
                entries_by_key[existing_key]["text"] = new_entry_text
                updated_papers.append((existing_key, metadata["title"]))
                modified = True
            continue

        # Generate BibTeX entry for new paper
        entry_text = generate_bibtex_entry(metadata)
        new_entry = {
            "key": citation_key,
            "type": "techreport",
            "text": entry_text,
            "doi": doi,
            "title": metadata["title"],
        }
        entries_by_key[citation_key] = new_entry
        added_papers.append((citation_key, metadata["title"]))
        modified = True

        # Track to prevent duplicates in this run
        existing_keys.add(citation_key)
        if doi_lower:
            existing_dois[doi_lower] = citation_key

    # Save using shared utility (auto-alphabetizes, validates for duplicates)
    if modified:
        all_entries = list(entries_by_key.values())
        save_references_bib(bib_path, all_entries, strict=True)

    # Print summary
    if added_papers:
        print(f"[OK] Added {len(added_papers)} new references from Quarto configs")
        for key, title in added_papers:
            display_title = title[:60] + "..." if len(title) > 60 else title
            print(f"     + {key}: {display_title}")

    if updated_papers:
        print(f"[OK] Updated {len(updated_papers)} references from Quarto configs")
        for key, title in updated_papers:
            display_title = title[:60] + "..." if len(title) > 60 else title
            print(f"     ~ {key}: {display_title}")

    return added_papers + updated_papers


def main():
    """CLI entry point for testing."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    project_root = Path(__file__).parent.parent.absolute()

    print("[*] Scanning Quarto configs for papers to add to references.bib...")
    added = update_references_from_quarto(project_root)

    if not added:
        print("[OK] All Quarto papers already in references.bib")


if __name__ == "__main__":
    main()
