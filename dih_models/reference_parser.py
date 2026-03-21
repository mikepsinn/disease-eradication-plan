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
import json
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.customization import convert_to_unicode
    HAS_BIBTEXPARSER = True
except ImportError:
    HAS_BIBTEXPARSER = False

# Pre-compiled patterns for URL extraction and key sanitization
_URL_PATTERN = re.compile(r'https?://[^\s<>\"\'\)]+[^\s<>\"\'\)\.,]')
_BIBTEX_KEY_NONALNUM = re.compile(r'[^a-zA-Z0-9\-_]')
_BIBTEX_KEY_MULTI_HYPHEN = re.compile(r'-+')
_REFERENCE_CACHE_VERSION = 1
_PARSED_REFERENCES_CACHE: Dict[Tuple[str, int, int], Dict[str, Dict[str, Any]]] = {}


def _get_bib_signature(bib_path: Path) -> Tuple[str, int, int]:
    """Return a cheap file signature for cache validation."""
    stat = bib_path.stat()
    return str(bib_path.resolve()), stat.st_size, stat.st_mtime_ns


def _get_cache_path(bib_path: Path) -> Path:
    """Store parsed-reference cache alongside Python bytecode artifacts."""
    cache_dir = Path(__file__).resolve().parent / "__pycache__"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{bib_path.stem}-parsed-references.json"


def _load_cached_references(bib_path: Path) -> Optional[Dict[str, Dict[str, Any]]]:
    """Load cached parsed references when the BibTeX file is unchanged."""
    signature = _get_bib_signature(bib_path)
    if signature in _PARSED_REFERENCES_CACHE:
        return _PARSED_REFERENCES_CACHE[signature]

    cache_path = _get_cache_path(bib_path)
    if not cache_path.exists():
        return None

    try:
        with open(cache_path, encoding="utf-8") as f:
            payload = json.load(f)
    except Exception:
        return None

    expected_path, expected_size, expected_mtime_ns = signature
    if (
        payload.get("cache_version") != _REFERENCE_CACHE_VERSION
        or payload.get("bib_path") != expected_path
        or payload.get("size") != expected_size
        or payload.get("mtime_ns") != expected_mtime_ns
    ):
        return None

    references = payload.get("references")
    if not isinstance(references, dict):
        return None

    _PARSED_REFERENCES_CACHE[signature] = references
    return references


def _write_cached_references(bib_path: Path, references: Dict[str, Dict[str, Any]]) -> None:
    """Persist parsed references for future runs."""
    cache_path = _get_cache_path(bib_path)
    bib_path_str, size, mtime_ns = _get_bib_signature(bib_path)
    payload = {
        "cache_version": _REFERENCE_CACHE_VERSION,
        "bib_path": bib_path_str,
        "size": size,
        "mtime_ns": mtime_ns,
        "references": references,
    }

    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
    except Exception:
        # Cache failures must never break generation.
        return

    _PARSED_REFERENCES_CACHE[(bib_path_str, size, mtime_ns)] = references


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

    bib_path = bib_path.resolve()
    cached_references = _load_cached_references(bib_path)
    if cached_references is not None:
        return cached_references

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
        for text in [abstract, note]:
            for url_match in _URL_PATTERN.finditer(text):
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

    _write_cached_references(bib_path, references)
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
    sanitized = _BIBTEX_KEY_NONALNUM.sub('-', sanitized)
    # Remove multiple consecutive hyphens
    sanitized = _BIBTEX_KEY_MULTI_HYPHEN.sub('-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    return sanitized
