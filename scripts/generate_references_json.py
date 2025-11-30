#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate JSON references file from references.qmd

Parses knowledge/references.qmd and converts it to a structured JSON format.
This is called by generate-variables-yml.py as part of the build process.

Usage:
    python scripts/generate-references-json.py
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def parse_yaml_frontmatter(content: str) -> tuple[dict[str, Any], int]:
    """
    Parse YAML frontmatter from QMD file.

    Returns:
        Tuple of (metadata dict, body start position)
    """
    yaml_match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n', content)
    if not yaml_match:
        return {}, 0

    yaml_content = yaml_match.group(1)
    metadata: dict[str, Any] = {}

    current_key: str | None = None
    current_array: list[str] = []

    for line in yaml_content.split('\n'):
        line = line.rstrip('\r')

        # Check for new key
        key_match = re.match(r'^(\w+):', line)
        if key_match:
            # Save previous array if exists
            if current_key and current_array:
                metadata[current_key] = current_array
                current_array = []
                current_key = None

            key = key_match.group(1)
            value = line[line.index(':') + 1:].strip()

            if value:
                # Handle boolean
                if value == 'true':
                    metadata[key] = True
                elif value == 'false':
                    metadata[key] = False
                else:
                    metadata[key] = value
                current_key = None
            else:
                # Empty value - expect array items
                current_key = key
        elif line.strip().startswith('- ') and current_key:
            # Array item
            current_array.append(line.strip()[2:])

    # Save last array if exists
    if current_key and current_array:
        metadata[current_key] = current_array

    return metadata, len(yaml_match.group(0))


def parse_references(content: str) -> list[dict[str, Any]]:
    """
    Parse reference entries from QMD content.

    Returns:
        List of reference dictionaries with id, title, quotes, sources, notes
    """
    references: list[dict[str, Any]] = []

    # Split by anchor tags
    anchor_pattern = r'<a id="([^"]+)"></a>'
    parts = re.split(anchor_pattern, content)

    # Skip first part (before first anchor)
    i = 1
    while i < len(parts):
        ref_id = parts[i]
        ref_content = parts[i + 1] if i + 1 < len(parts) else ''
        i += 2

        if not ref_content or not ref_content.strip():
            continue

        # Extract the bullet point content (title)
        bullet_match = re.search(r'^\s*-\s+\*\*(.*?)\*\*', ref_content, re.MULTILINE)
        if not bullet_match:
            continue

        title = bullet_match.group(1).strip()

        # Extract quotes (lines starting with >)
        quotes: list[str] = []
        for quote_match in re.finditer(r'^\s*>\s*(.+)$', ref_content, re.MULTILINE):
            quote_line = quote_match.group(1).strip()
            # Skip source lines (starting with —)
            if not quote_line.startswith('—') and not quote_line.startswith('--'):
                quotes.append(quote_line)

        # Extract sources (lines with —) and notes
        sources: list[dict[str, str]] = []
        notes: str | None = None

        for source_match in re.finditer(r'^\s*>\s*[—-]+\s*(.+)$', ref_content, re.MULTILINE):
            full_source_line = source_match.group(1).strip()

            # Split by pipe to get individual parts
            source_parts = [p.strip() for p in full_source_line.split('|')]

            for part in source_parts:
                # Check if this part is a note
                if part.lower().startswith('note:'):
                    notes = part[5:].strip()
                    continue

                # Parse markdown links: [text](url)
                link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
                matches = list(re.finditer(link_pattern, part))

                if matches:
                    prev_end = 0
                    for match in matches:
                        # Get prefix text before the link
                        prefix = part[prev_end:match.start()].strip()
                        link_text = match.group(1)
                        link_url = match.group(2)

                        # Combine prefix with link text if prefix exists
                        full_text = f"{prefix} {link_text}" if prefix else link_text
                        full_text = full_text.strip().rstrip(',').strip()

                        sources.append({
                            'text': full_text,
                            'url': link_url
                        })

                        prev_end = match.end()
                elif part:
                    # Plain text source
                    sources.append({'text': part})

        reference: dict[str, Any] = {
            'id': ref_id,
            'title': title,
            'quotes': quotes,
            'sources': sources
        }
        if notes:
            reference['notes'] = notes

        references.append(reference)

    return references


def generate_references_json(references_path: Path, output_path: Path) -> int:
    """
    Generate references.json from references.qmd.

    Args:
        references_path: Path to references.qmd
        output_path: Path to write references.json

    Returns:
        Number of references parsed
    """
    if not references_path.exists():
        print(f"[WARN] References file not found: {references_path}", file=sys.stderr)
        return 0

    content = references_path.read_text(encoding='utf-8')

    # Parse YAML frontmatter
    metadata, body_start = parse_yaml_frontmatter(content)

    # Parse references
    body = content[body_start:]
    references = parse_references(body)

    # Build output data
    data = {
        'metadata': metadata,
        'references': references
    }

    # Write JSON file
    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )

    total_quotes = sum(len(ref['quotes']) for ref in references)
    total_sources = sum(len(ref['sources']) for ref in references)

    print(f"[OK] Generated {output_path}")
    print(f"     {len(references)} references")
    print(f"     {total_quotes} total quotes")
    print(f"     {total_sources} total sources")

    return len(references)


def main():
    """Main entry point for standalone execution."""
    project_root = Path(__file__).parent.parent.absolute()

    references_path = project_root / "knowledge" / "references.qmd"
    output_path = project_root / "knowledge" / "references.json"

    print("[*] Generating references.json...")
    generate_references_json(references_path, output_path)


if __name__ == "__main__":
    main()
