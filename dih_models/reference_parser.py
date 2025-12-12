#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reference parsing utilities for dih_models
==========================================

Parse knowledge/references.qmd and extract citation metadata.

Functions:
- parse_references_qmd_detailed() - Extract full citation metadata
- parse_references_qmd() - Extract just reference IDs (simple wrapper)
- sanitize_bibtex_key() - Sanitize citation keys for BibTeX compatibility

Usage:
    from dih_models.reference_parser import parse_references_qmd_detailed, sanitize_bibtex_key
    from pathlib import Path

    # Parse full citation metadata
    refs_path = Path("knowledge/references.qmd")
    citations = parse_references_qmd_detailed(refs_path)

    # Get just the IDs
    ref_ids = parse_references_qmd(refs_path)

    # Sanitize BibTeX key
    clean_key = sanitize_bibtex_key("my/reference#key")
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict


def parse_references_qmd_detailed(references_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse knowledge/references.qmd and extract full citation metadata.

    Returns a dict mapping reference IDs to citation data:
    {
        'reference-id': {
            'id': 'reference-id',
            'title': 'The reference title',
            'author': 'Author Name',
            'year': '2024',
            'source': 'Journal/Publisher Name',
            'url': 'https://...',
            'urls': ['https://...', 'https://...'],  # All URLs
            'quote': 'The quoted text',
            'note': 'Additional context',
            'type': 'article'  # article, book, misc, report, etc.
        }
    }
    """
    if not references_path.exists():
        print(f"[WARN] References file not found: {references_path}", file=sys.stderr)
        return {}

    with open(references_path, encoding="utf-8") as f:
        lines = f.readlines()

    references = {}
    current_ref = None
    current_id = None
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Match anchor tags: <a id="reference-id"></a>
        anchor_match = re.match(r'<a\s+id="([^"]+)"\s*></a>', line)
        if anchor_match:
            ref_id = anchor_match.group(1)

            # Skip internal document references (contain / or .qmd)
            if '/' in ref_id or '.qmd' in ref_id:
                i += 1
                continue

            # Save PREVIOUS reference before starting new one
            if current_id and current_ref:
                # Only infer type from source if type wasn't explicitly set
                if current_ref['type'] == 'misc' and current_ref['source']:
                    source_lower = current_ref['source'].lower()
                    if any(word in source_lower for word in ['journal', 'nature', 'science', 'lancet']):
                        current_ref['type'] = 'article'
                    elif any(word in source_lower for word in ['congress.gov', 'law', 'act', 'bill']):
                        current_ref['type'] = 'legislation'
                    elif any(word in source_lower for word in ['cdc', 'who', 'gao', 'fda', 'nih']):
                        current_ref['type'] = 'report'
                    elif any(word in source_lower for word in ['book', 'press', 'publisher']):
                        current_ref['type'] = 'book'
                    elif 'university' in source_lower or 'project' in source_lower:
                        current_ref['type'] = 'techreport'

                references[current_id] = current_ref

            # Start new reference
            current_id = ref_id
            current_ref = {
                'id': ref_id,
                'title': '',
                'author': '',
                'year': '',
                'source': '',
                'url': '',
                'urls': [],
                'quote': '',
                'note': '',
                'type': 'misc'
            }
            i += 1
            continue

        # Match title: - **Title text**
        if current_id and current_ref and line.startswith('- **') and line.endswith('**'):
            title = line[4:-2].strip()
            current_ref['title'] = title
            i += 1
            continue

        # Match structured property lines: "property: value" (no indentation required)
        # Must contain colon but not be a blockquote or markdown title
        if current_id and current_ref and ':' in line and not line.strip().startswith('>') and not line.strip().startswith('-'):
            # Extract property name and value
            stripped = line.strip()
            if ':' in stripped:
                # Split on first colon only (URLs contain colons)
                prop_name, prop_value = stripped.split(':', 1)
                prop_name = prop_name.strip().lower()
                prop_value = prop_value.strip()

                # Map property names to reference fields
                if prop_name == 'title':
                    current_ref['title'] = prop_value
                elif prop_name == 'type':
                    current_ref['type'] = prop_value
                elif prop_name == 'author':
                    current_ref['author'] = prop_value
                elif prop_name == 'year':
                    current_ref['year'] = prop_value
                elif prop_name == 'journal':
                    current_ref['source'] = prop_value  # Use source field for journal
                elif prop_name == 'publisher':
                    if not current_ref['source']:  # Only set if source not already set
                        current_ref['source'] = prop_value
                elif prop_name == 'url':
                    current_ref['url'] = prop_value
                    current_ref['urls'].append(prop_value)
                elif prop_name == 'note':
                    current_ref['note'] = prop_value
                elif prop_name in ['volume', 'number', 'pages', 'doi', 'address']:
                    # Store additional BibTeX fields in a metadata dict
                    if 'metadata' not in current_ref:
                        current_ref['metadata'] = {}
                    current_ref['metadata'][prop_name] = prop_value

            i += 1
            continue

        # Match blockquote lines (citation data)
        if current_id and current_ref and line.strip().startswith('>'):
            quote_line = line.strip()[1:].strip()  # Remove '>' and whitespace

            # Attribution line (starts with em dash): — Source, Year, [Link](URL)
            if quote_line.startswith('—') or quote_line.startswith('--'):
                attribution = quote_line.lstrip('—-').strip()

                # Extract all URLs from markdown links: [text](url)
                url_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                url_matches = re.findall(url_pattern, attribution)
                for link_text, url in url_matches:
                    current_ref['urls'].append(url)
                    if not current_ref['url']:
                        current_ref['url'] = url

                # Try to extract year (4-digit number)
                year_match = re.search(r'\b(19|20)\d{2}\b', attribution)
                if year_match:
                    current_ref['year'] = year_match.group(0)

                # Extract source/author (text before year or first comma)
                # Remove markdown links for cleaner parsing
                clean_attr = re.sub(url_pattern, r'\1', attribution)

                # Split by | to get individual sources
                sources = clean_attr.split('|')
                if sources:
                    first_source = sources[0].strip()
                    # Source format: "Name, Year, Link" or "Name, Link"
                    parts = [p.strip() for p in first_source.split(',')]
                    if parts:
                        current_ref['source'] = parts[0]
                        # Use source as author if no better info available
                        if not current_ref['author']:
                            current_ref['author'] = parts[0]

                # Store full attribution as note
                current_ref['note'] = clean_attr

            # Regular quote line
            elif quote_line.startswith('"') or 'Alternative title:' in quote_line:
                if current_ref['quote']:
                    current_ref['quote'] += ' '
                current_ref['quote'] += quote_line

            i += 1
            continue

        # Continue to next line
        i += 1

    # Save last reference if exists
    if current_id and current_ref:
        # Determine entry type based on source
        source_lower = current_ref['source'].lower()
        if any(word in source_lower for word in ['journal', 'nature', 'science', 'lancet']):
            current_ref['type'] = 'article'
        elif any(word in source_lower for word in ['congress.gov', 'law', 'act', 'bill']):
            current_ref['type'] = 'legislation'
        elif any(word in source_lower for word in ['cdc', 'who', 'gao', 'fda', 'nih']):
            current_ref['type'] = 'report'
        elif any(word in source_lower for word in ['book', 'press', 'publisher']):
            current_ref['type'] = 'book'
        elif 'university' in source_lower or 'project' in source_lower:
            current_ref['type'] = 'techreport'

        references[current_id] = current_ref

    return references


def parse_references_qmd(references_path: Path) -> set:
    """
    Parse knowledge/references.qmd and extract all reference IDs.

    Returns a set of all anchor IDs (for backward compatibility).
    For detailed citation data, use parse_references_qmd_detailed().

    Example: <a id="166-billion-compounds"></a> -> "166-billion-compounds"
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
