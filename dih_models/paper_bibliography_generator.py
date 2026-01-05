#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-Paper Bibliography Generator
================================

Generate filtered .bib files for standalone papers, containing only citations
actually used in each paper. This ensures PDFs include only relevant references.

Functions:
- extract_citations_from_qmd() - Find all [@key] citations in a QMD file
- generate_paper_bibliography() - Create filtered .bib for a single paper
- generate_all_paper_bibliographies() - Process all standalone papers

Usage:
    from dih_models.paper_bibliography_generator import generate_all_paper_bibliographies
    from pathlib import Path

    project_root = Path(".")
    generate_all_paper_bibliographies(project_root)
"""

import re
import sys
from pathlib import Path
from typing import Set, Dict, List, Optional

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def extract_citations_from_qmd(qmd_path: Path, project_root: Path = None) -> Set[str]:
    """
    Extract all citation keys from a QMD file, including from {{< include >}} files.

    Args:
        qmd_path: Path to the QMD file to analyze
        project_root: Project root for resolving absolute include paths

    Returns:
        Set of citation keys (without @ prefix)
    """
    if not qmd_path.exists():
        return set()

    citations: Set[str] = set()
    processed_files: Set[Path] = set()

    def process_file(file_path: Path):
        """Recursively process a file and its includes."""
        if file_path in processed_files or not file_path.exists():
            return
        processed_files.add(file_path)

        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Find all citation patterns:
        # 1. [@key] - standard bracketed citations
        # 2. @key (followed by punctuation/whitespace) - inline citations (Pandoc style)
        # Skip @ patterns in code blocks, frontmatter, and URLs
        skip_patterns = {
            # BibTeX entry types
            'misc', 'article', 'book', 'inproceedings', 'techreport',
            'phdthesis', 'mastersthesis', 'incollection', 'manual',
            'proceedings', 'unpublished', 'booklet', 'conference',
            # CSS @ rules
            'property', 'media', 'keyframes', 'import', 'charset',
            'supports', 'layer', 'namespace', 'page', 'font-face',
        }
        # Skip cross-reference prefixes (eq-, fig-, tbl-, sec-, etc.)
        skip_prefixes = ('eq-', 'fig-', 'tbl-', 'sec-', 'lst-', 'thm-', 'def-', 'lem-', 'cor-', 'prp-')

        # Pattern 1: Bracketed citations [@key]
        for match in re.finditer(r'\[@([a-zA-Z0-9_-]+)', content):
            key = match.group(1)
            if key not in skip_patterns and not key.startswith(skip_prefixes):
                citations.add(key)

        # Pattern 2: Inline citations @key (followed by punctuation, comma, period, or whitespace)
        # Must be preceded by whitespace or start of line to avoid matching URLs like user@example.com
        for match in re.finditer(r'(?:^|[\s\[(])@([a-zA-Z][a-zA-Z0-9_-]+)(?=[,.\s\)\]:]|$)', content, re.MULTILINE):
            key = match.group(1)
            if key not in skip_patterns and not key.startswith(skip_prefixes):
                citations.add(key)

        # Find and process {{< include >}} directives
        include_pattern = r'\{\{<\s*include\s+([^>]+)\s*>\}\}'
        for match in re.finditer(include_pattern, content):
            include_path_str = match.group(1).strip().strip('"\'')

            # Resolve include path
            if include_path_str.startswith('/'):
                # Absolute path from project root
                if project_root:
                    include_path = project_root / include_path_str.lstrip('/')
                else:
                    include_path = Path(include_path_str.lstrip('/'))
            else:
                # Relative path from current file
                include_path = file_path.parent / include_path_str

            process_file(include_path.resolve())

    process_file(qmd_path.resolve())
    return citations


def generate_paper_bibliography(
    paper_path: Path,
    main_bib_path: Path,
    output_bib_path: Path,
    project_root: Path = None
) -> int:
    """
    Generate a filtered .bib file containing only citations used in a paper.

    Args:
        paper_path: Path to the paper's QMD file
        main_bib_path: Path to the main references.bib file
        output_bib_path: Path to write the filtered .bib file
        project_root: Project root for resolving include paths

    Returns:
        Number of entries in the filtered bibliography
    """
    # Extract citations from the paper
    citations = extract_citations_from_qmd(paper_path, project_root)

    if not citations:
        print(f"[WARN] No citations found in {paper_path.name}")
        return 0

    # Read the main bibliography
    if not main_bib_path.exists():
        print(f"[ERROR] Main bibliography not found: {main_bib_path}")
        return 0

    with open(main_bib_path, encoding='utf-8') as f:
        main_bib_content = f.read()

    # Parse BibTeX entries
    # Split by @type{ patterns to find entry boundaries
    # This handles multi-line entries properly
    entries = []
    # Find all entry start positions
    entry_starts = [(m.start(), m.group(1)) for m in re.finditer(r'(@\w+)\{', main_bib_content)]

    for i, (start, entry_type) in enumerate(entry_starts):
        # Find entry key (between { and ,)
        key_match = re.match(r'@\w+\{([^,\s]+)', main_bib_content[start:])
        if not key_match:
            continue
        entry_key = key_match.group(1).strip()

        # Find entry end (next entry or end of file)
        if i + 1 < len(entry_starts):
            end = entry_starts[i + 1][0]
        else:
            end = len(main_bib_content)

        entry_text = main_bib_content[start:end].strip()
        # Ensure entry ends with }
        if not entry_text.endswith('}'):
            # Find the last }
            last_brace = entry_text.rfind('}')
            if last_brace > 0:
                entry_text = entry_text[:last_brace + 1]

        entries.append((entry_text, entry_key))

    # Filter entries to only include cited ones
    filtered_entries = []
    found_citations = set()

    for entry_text, entry_key in entries:
        # Normalize key (strip whitespace)
        entry_key = entry_key.strip()
        if entry_key in citations:
            filtered_entries.append(entry_text)
            found_citations.add(entry_key)

    # Check for missing citations
    missing = citations - found_citations
    if missing:
        print(f"[WARN] Citations not found in references.bib: {', '.join(sorted(missing)[:10])}")
        if len(missing) > 10:
            print(f"       ... and {len(missing) - 10} more")

    # Write filtered bibliography
    content = [
        "% AUTO-GENERATED FILE - DO NOT EDIT",
        f"% Filtered bibliography for {paper_path.name}",
        f"% Re-generate with: python scripts/generate-everything-parameters-variables-calculations-references.py",
        "",
    ]
    content.extend(filtered_entries)

    output_bib_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_bib_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(content))

    return len(filtered_entries)


def generate_all_paper_bibliographies(project_root: Path) -> Dict[str, int]:
    """
    Generate filtered bibliographies for all standalone papers.

    Looks for papers defined in _quarto-*.yml configs with dih-render.index-source.

    Args:
        project_root: Path to project root

    Returns:
        Dict mapping paper names to number of entries in their bibliography
    """
    import yaml

    main_bib = project_root / "references.bib"
    if not main_bib.exists():
        print("[ERROR] references.bib not found")
        return {}

    results: Dict[str, int] = {}

    # Find all standalone paper configs
    for config_file in project_root.glob("_quarto-*.yml"):
        config_name = config_file.stem.replace("_quarto-", "")

        # Skip book config (it uses all references by design)
        if config_name == "book":
            continue

        with open(config_file, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        dih_render = config.get("dih-render", {})
        index_source = dih_render.get("index-source")

        if not index_source:
            continue

        paper_path = project_root / index_source
        if not paper_path.exists():
            print(f"[WARN] Paper not found: {index_source}")
            continue

        # Generate filtered bibliography
        output_bib = project_root / f"references-{config_name}.bib"
        count = generate_paper_bibliography(
            paper_path=paper_path,
            main_bib_path=main_bib,
            output_bib_path=output_bib,
            project_root=project_root
        )

        if count > 0:
            print(f"[OK] Generated {output_bib.name}: {count} entries")
            results[config_name] = count

    return results


def update_paper_frontmatter(paper_path: Path, new_bib_path: str) -> bool:
    """
    Update a paper's frontmatter to use a filtered bibliography.

    Args:
        paper_path: Path to the paper's QMD file
        new_bib_path: New bibliography path to set

    Returns:
        True if updated, False if no change needed
    """
    with open(paper_path, encoding='utf-8') as f:
        content = f.read()

    # Find and replace bibliography in frontmatter
    # Pattern matches bibliography: - path or bibliography: path
    old_pattern = r'(bibliography:\s*\n\s*-\s*)[^\n]+'
    new_value = f'\\1{new_bib_path}'

    new_content, count = re.subn(old_pattern, new_value, content)

    if count == 0:
        # Try single-line format
        old_pattern = r'(bibliography:\s*)[^\n]+'
        new_content, count = re.subn(old_pattern, new_value, content)

    if count > 0 and new_content != content:
        with open(paper_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        return True

    return False


if __name__ == "__main__":
    # Run standalone for testing
    project_root = Path(__file__).parent.parent
    print(f"[*] Generating per-paper bibliographies in {project_root}")
    results = generate_all_paper_bibliographies(project_root)
    print(f"[OK] Generated {len(results)} filtered bibliographies")
