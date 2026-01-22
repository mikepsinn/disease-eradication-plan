#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reference parsing utilities for dih_models
==========================================

Parse references.bib (BibTeX) and extract citation metadata.

Functions:
- parse_references_bib() - Extract full citation metadata from BibTeX
- parse_references_bib_keys() - Extract just reference keys (simple wrapper)
- sanitize_bibtex_key() - Sanitize citation keys for BibTeX compatibility

Usage:
    from dih_models.reference_parser import parse_references_bib
    from pathlib import Path

    # Parse full citation metadata from BibTeX
    bib_path = Path("references.bib")
    citations = parse_references_bib(bib_path)

    # Get just the keys
    ref_keys = parse_references_bib_keys(bib_path)
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, Set

try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.customization import convert_to_unicode
    HAS_BIBTEXPARSER = True
except ImportError:
    HAS_BIBTEXPARSER = False


def parse_references_bib(bib_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse references.bib and extract full citation metadata.

    Returns a dict mapping citation keys to citation data:
    {
        'citation-key': {
            'id': 'citation-key',
            'title': 'The reference title',
            'author': 'Author Name',
            'year': '2024',
            'source': 'Journal/Publisher Name',
            'url': 'https://...',
            'urls': ['https://...', 'https://...'],  # All URLs
            'quote': 'The abstract/quoted text',
            'note': 'Additional context',
            'type': 'article'  # article, book, misc, report, etc.
        }
    }
    """
    if not bib_path.exists():
        print(f"[WARN] BibTeX file not found: {bib_path}", file=sys.stderr)
        return {}

    if not HAS_BIBTEXPARSER:
        print("[ERROR] bibtexparser not installed. Run: pip install bibtexparser", file=sys.stderr)
        return {}

    with open(bib_path, encoding="utf-8") as f:
        bib_content = f.read()

    # Parse with unicode conversion
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    bib_database = bibtexparser.loads(bib_content, parser=parser)

    references = {}
    for entry in bib_database.entries:
        entry_key = entry.get('ID', '')
        if not entry_key:
            continue

        # Extract URLs (may be in 'url' field or 'urldate')
        urls = []
        primary_url = entry.get('url', '')
        if primary_url:
            urls.append(primary_url)

        # Some entries have additional URLs in abstract or note fields
        abstract = entry.get('abstract', '')
        note = entry.get('note', '')

        # Extract additional URLs from abstract/note
        url_pattern = r'https?://[^\s<>\"\'\)]+[^\s<>\"\'\)\.,]'
        for text in [abstract, note]:
            for url_match in re.finditer(url_pattern, text):
                url = url_match.group(0)
                if url not in urls:
                    urls.append(url)

        # Determine source (journal, publisher, or booktitle)
        source = (
            entry.get('journal', '') or
            entry.get('publisher', '') or
            entry.get('booktitle', '') or
            entry.get('institution', '')
        )

        # Build reference data structure (compatible with old format)
        ref_data = {
            'id': entry_key,
            'title': entry.get('title', ''),
            'author': entry.get('author', ''),
            'year': entry.get('year', ''),
            'source': source,
            'url': primary_url,
            'urls': urls,
            'quote': abstract,  # BibTeX abstract maps to quote
            'note': note,
            'type': entry.get('ENTRYTYPE', 'misc'),
            # Additional BibTeX fields
            'doi': entry.get('doi', ''),
            'volume': entry.get('volume', ''),
            'pages': entry.get('pages', ''),
            'number': entry.get('number', ''),
        }

        references[entry_key] = ref_data

    return references


def parse_references_bib_keys(bib_path: Path) -> Set[str]:
    """
    Parse references.bib and extract all citation keys.

    Returns a set of all citation keys (for backward compatibility).
    For detailed citation data, use parse_references_bib().
    """
    references = parse_references_bib(bib_path)
    return set(references.keys())


# Legacy aliases for backward compatibility
def parse_references_qmd_detailed(references_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    DEPRECATED: Use parse_references_bib() instead.

    This function now parses references.bib instead of references.qmd.
    The references_path argument is ignored - it always reads references.bib
    from the project root.
    """
    # Determine project root from the path
    # If path contains 'knowledge', go up to find project root
    path_parts = references_path.parts
    if 'knowledge' in path_parts:
        idx = path_parts.index('knowledge')
        project_root = Path(*path_parts[:idx])
    else:
        project_root = references_path.parent

    bib_path = project_root / "references.bib"

    # Fall back to same directory if project root doesn't have bib
    if not bib_path.exists():
        bib_path = references_path.parent.parent / "references.bib"

    if not bib_path.exists():
        # Try absolute path from CWD
        bib_path = Path("references.bib")

    return parse_references_bib(bib_path)


def parse_references_qmd(references_path: Path) -> Set[str]:
    """
    DEPRECATED: Use parse_references_bib_keys() instead.

    This function now parses references.bib instead of references.qmd.
    """
    detailed = parse_references_qmd_detailed(references_path)
    return set(detailed.keys())


def sanitize_bibtex_key(key: str) -> str:
    """
    Sanitize citation key for BibTeX (only alphanumeric, hyphens, underscores).

    Same logic as convert-references-to-bib.py for consistency.
    """
    sanitized = key
    sanitized = sanitized.replace('/', '-')
    sanitized = sanitized.replace('#', '-')
    sanitized = sanitized.replace('.qmd', '')
    sanitized = sanitized.replace('.', '-')
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '-', sanitized)
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    return sanitized
