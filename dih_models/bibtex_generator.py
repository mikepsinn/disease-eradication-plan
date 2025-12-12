#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BibTeX generation utilities for dih_models
===========================================

Generate references.bib from parameter metadata and references.qmd.

Functions:
- generate_bibtex() - Generate BibTeX file from external parameters

Usage:
    from dih_models.bibtex_generator import generate_bibtex
    from pathlib import Path

    # Generate BibTeX file
    bibtex_path = Path("references.bib")
    generate_bibtex(parameters, bibtex_path, available_refs=refs, references_path=refs_qmd)
"""

from pathlib import Path
from typing import Any, Dict

from dih_models.reference_parser import (
    parse_references_qmd_detailed,
    sanitize_bibtex_key,
)


def generate_bibtex(parameters: Dict[str, Dict[str, Any]], output_path: Path, available_refs: set = None, references_path: Path = None, export_all: bool = True):
    """
    Generate references.bib BibTeX file from references.qmd.

    Args:
        parameters: Dict of parameter metadata (used when export_all=False)
        output_path: Path to write references.bib
        available_refs: Set of valid reference IDs from references.qmd (optional)
        references_path: Path to references.qmd file for detailed citation data
        export_all: If True, export ALL entries from references.qmd (default: True)
                   If False, only export citations used in parameters
    """
    # Parse detailed citation data from references.qmd
    citation_data = {}
    if references_path and references_path.exists():
        citation_data = parse_references_qmd_detailed(references_path)

    # Collect citations based on export_all setting
    citations = set()

    if export_all:
        # Export ALL entries from references.qmd (single source of truth)
        citations = set(citation_data.keys())
    else:
        # Legacy behavior: Only export citations used in parameters with source_type="external"
        for param_name, param_data in parameters.items():
            value = param_data["value"]
            if hasattr(value, "source_type"):
                source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
                if source_type_str == "external":
                    if hasattr(value, "source_ref") and value.source_ref:
                        # Convert ReferenceID enum to string value
                        source_ref = value.source_ref
                        if hasattr(source_ref, 'value'):
                            # It's an enum, get the actual string value
                            source_ref = source_ref.value
                        else:
                            # It's already a string
                            source_ref = str(source_ref)

                        # Skip internal document references (contain / or .qmd)
                        if '/' in source_ref or '.qmd' in source_ref:
                            continue

                        # Optionally skip missing references
                        if available_refs and source_ref not in available_refs:
                            continue

                        citations.add(source_ref)

    # Generate BibTeX entries
    content = []
    content.append("% AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("% Generated from knowledge/references.qmd (single source of truth)")
    content.append("")
    content.append("% This file contains BibTeX entries for ALL citations in references.qmd")
    content.append("% For editing citations, add/modify entries in knowledge/references.qmd")
    content.append("")
    content.append("% Extracted citation data: author, year, source, URL, and notes.")
    content.append("% Re-generate by running: python scripts/generate-everything-parameters-variables-calculations-references.py")
    content.append("")

    entries_with_data = 0
    entries_placeholder = 0

    for citation_key in sorted(citations):
        # Sanitize citation key for BibTeX (remove /, #, etc.)
        sanitized_key = sanitize_bibtex_key(citation_key)

        # Get detailed citation data if available
        ref_data = citation_data.get(citation_key, {})

        if ref_data and ref_data.get('title'):
            # Create proper BibTeX entry with real data
            entry_type = ref_data.get('type', 'misc')
            title = ref_data.get('title', citation_key)
            author = ref_data.get('author', '')
            year = ref_data.get('year', 'n.d.')
            source = ref_data.get('source', '')
            url = ref_data.get('url', '')
            note = ref_data.get('note', '')

            # Build BibTeX entry
            content.append(f"@{entry_type}{{{sanitized_key},")

            # Title (required for all types)
            # Escape special LaTeX characters
            title_escaped = title.replace('&', '\\&').replace('%', '\\%')
            content.append(f"  title = {{{title_escaped}}},")

            # Author/organization
            if author:
                author_escaped = author.replace('&', '\\&')
                if entry_type in ['report', 'techreport', 'legislation']:
                    content.append(f"  institution = {{{author_escaped}}},")
                else:
                    content.append(f"  author = {{{author_escaped}}},")

            # Year
            content.append(f"  year = {{{year}}},")

            # Source/journal/publisher
            if source:
                source_escaped = source.replace('&', '\\&')
                if entry_type == 'article':
                    content.append(f"  journal = {{{source_escaped}}},")
                elif entry_type in ['book', 'report', 'techreport']:
                    content.append(f"  publisher = {{{source_escaped}}},")

            # Additional BibTeX fields from metadata dict (volume, number, pages, DOI, address)
            metadata = ref_data.get('metadata', {})
            if metadata:
                if 'volume' in metadata:
                    content.append(f"  volume = {{{metadata['volume']}}},")
                if 'number' in metadata:
                    content.append(f"  number = {{{metadata['number']}}},")
                if 'pages' in metadata:
                    pages = metadata['pages'].replace('--', '-')  # Normalize page ranges
                    content.append(f"  pages = {{{pages}}},")
                if 'doi' in metadata:
                    content.append(f"  doi = {{{metadata['doi']}}},")
                if 'address' in metadata:
                    content.append(f"  address = {{{metadata['address']}}},")

            # URL (with proper escaping)
            if url:
                url_escaped = url.replace('&', '\\&').replace('%', '\\%')
                content.append(f"  url = {{{url_escaped}}},")
                content.append("  urldate = {2025-01-20},")

            # Note (additional context)
            if note:
                note_escaped = note.replace('&', '\\&').replace('%', '\\%')
                # Truncate if too long
                if len(note_escaped) > 200:
                    note_escaped = note_escaped[:197] + "..."
                content.append(f"  note = {{{note_escaped}}},")

            content.append("}")
            content.append("")
            entries_with_data += 1

        else:
            # Fallback: create minimal placeholder entry
            content.append(f"@misc{{{sanitized_key},")
            content.append(f"  title = {{{citation_key}}},")
            content.append(f"  note = {{See https://warondisease.org/knowledge/references.html\\#{citation_key}}},")
            content.append(f"  url = {{https://warondisease.org/knowledge/references.html\\#{citation_key}}},")
            content.append("}")
            content.append("")
            entries_placeholder += 1

    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(citations)} unique citations")
    print(f"     {entries_with_data} with full citation data")
    if entries_placeholder > 0:
        print(f"     {entries_placeholder} placeholder entries (missing data in references.qmd)")
