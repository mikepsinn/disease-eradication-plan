#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-Paper Bibliography and Variables Generator
===============================================

Generate filtered .bib and _variables.yml files for standalone papers.
This ensures:
1. PDFs include only cited references (not all 700+ from references.bib)
2. Citeproc doesn't warn about citations embedded in unused variables

Functions:
- extract_citations_from_qmd() - Find all [@key] citations in a QMD file
- extract_variables_from_qmd() - Find all {{< var name >}} usages in a QMD file
- extract_citations_from_variable_values() - Find @citations embedded in variable HTML
- generate_filtered_variables_yml() - Create filtered _variables-{paper}.yml
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
from typing import Set, Dict, List, Optional, Tuple, Any

import yaml

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def extract_variables_from_qmd(qmd_path: Path, project_root: Path = None) -> Set[str]:
    """
    Extract all Quarto variable names used in a QMD file, including from {{< include >}} files.

    Pattern matched: {{< var variable_name >}}

    Args:
        qmd_path: Path to the QMD file to analyze
        project_root: Project root for resolving absolute include paths

    Returns:
        Set of variable names used in the file
    """
    if not qmd_path.exists():
        return set()

    variables: Set[str] = set()
    processed_files: Set[Path] = set()

    # Pattern to match Quarto variable references: {{< var variable_name >}}
    var_pattern = re.compile(r"\{\{<\s*var\s+([^\s>]+)\s*>\}\}")

    def process_file(file_path: Path):
        """Recursively process a file and its includes."""
        if file_path in processed_files or not file_path.exists():
            return
        processed_files.add(file_path)

        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Find all variable references
        for match in var_pattern.finditer(content):
            var_name = match.group(1).strip()
            variables.add(var_name)

        # Find and process {{< include >}} directives
        include_pattern = r'\{\{<\s*include\s+([^>]+)\s*>\}\}'
        for match in re.finditer(include_pattern, content):
            include_path_str = match.group(1).strip().strip('"\'')

            # Resolve include path
            if include_path_str.startswith('/'):
                if project_root:
                    include_path = project_root / include_path_str.lstrip('/')
                else:
                    include_path = Path(include_path_str.lstrip('/'))
            else:
                include_path = file_path.parent / include_path_str

            process_file(include_path.resolve())

    process_file(qmd_path.resolve())
    return variables


def extract_citations_from_variable_values(
    variable_names: Set[str],
    variables_yml_path: Path
) -> Set[str]:
    """
    Extract citation keys embedded in the values of specific variables.

    Variable values contain citations in two forms:
    1. data-source-ref="citation-key" attributes in HTML
    2. @citation-key patterns (in _cite variables)

    Args:
        variable_names: Set of variable names to check
        variables_yml_path: Path to _variables.yml

    Returns:
        Set of citation keys found in the variable values
    """
    if not variables_yml_path.exists():
        return set()

    with open(variables_yml_path, encoding='utf-8') as f:
        all_variables = yaml.safe_load(f)

    if not isinstance(all_variables, dict):
        return set()

    citations: Set[str] = set()

    for var_name in variable_names:
        if var_name not in all_variables:
            continue

        value = str(all_variables[var_name])

        # Pattern 1: data-source-ref="citation-key" in HTML attributes
        for match in re.finditer(r'data-source-ref="([^"]+)"', value):
            ref = match.group(1).strip()
            # Skip empty refs and file paths
            if ref and not ref.startswith('/'):
                citations.add(ref)

        # Pattern 2: @citation-key (for _cite variables like @who-report-2024)
        # Match @ followed by valid citation key characters
        for match in re.finditer(r'@([a-zA-Z][a-zA-Z0-9_-]+)', value):
            citations.add(match.group(1))

    return citations


def generate_filtered_variables_yml(
    variable_names: Set[str],
    full_variables_path: Path,
    output_path: Path
) -> int:
    """
    Generate a filtered _variables.yml containing only specified variables.

    Args:
        variable_names: Set of variable names to include
        full_variables_path: Path to the full _variables.yml
        output_path: Path to write the filtered file

    Returns:
        Number of variables in the filtered file
    """
    if not full_variables_path.exists():
        print(f"[ERROR] Variables file not found: {full_variables_path}")
        return 0

    with open(full_variables_path, encoding='utf-8') as f:
        all_variables = yaml.safe_load(f)

    if not isinstance(all_variables, dict):
        return 0

    # Filter to only requested variables
    filtered = {}
    for name in variable_names:
        if name in all_variables:
            filtered[name] = all_variables[name]
            # Also include the _cite variant if it exists
            cite_name = f"{name}_cite"
            if cite_name in all_variables:
                filtered[cite_name] = all_variables[cite_name]
            # Also include the _latex variant if it exists
            latex_name = f"{name}_latex"
            if latex_name in all_variables:
                filtered[latex_name] = all_variables[latex_name]

    # Write filtered variables
    # Use the same format as the source file to preserve LaTeX equation formatting
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write("# AUTO-GENERATED FILTERED VARIABLES - DO NOT EDIT\n")
        f.write(f"# Contains only variables used in this paper ({len(filtered)} entries)\n")
        f.write("# Re-generate with: python scripts/generate-everything-parameters-variables-calculations-references.py\n\n")
        # Use default_style='"' to preserve double-quoted strings with escaped newlines
        # This matches the format of _variables.yml and prevents LaTeX equations
        # from being reformatted with literal newlines (which can cause issues)
        yaml.dump(filtered, f, allow_unicode=True, default_flow_style=False, sort_keys=True, default_style='"')

    return len(filtered)


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
        # 1. [@key] or [-@key] - standard and suppress-author bracketed citations
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

        # Pattern 1: Bracketed citations [@key] or [-@key] (suppress-author format)
        for match in re.finditer(r'\[-?@([a-zA-Z0-9_-]+)', content):
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
    project_root: Path = None,
    variables_yml_path: Path = None
) -> Tuple[int, Set[str]]:
    """
    Generate a filtered .bib file containing only citations used in a paper.

    Includes citations from:
    1. Direct [@key] citations in QMD content
    2. Citations embedded in variable values (data-source-ref and @citation patterns)

    Args:
        paper_path: Path to the paper's QMD file
        main_bib_path: Path to the main references.bib file
        output_bib_path: Path to write the filtered .bib file
        project_root: Project root for resolving include paths
        variables_yml_path: Path to _variables.yml for extracting variable citations

    Returns:
        Tuple of (number of entries in filtered bibliography, set of used variable names)
    """
    # Extract direct citations from the paper content
    citations = extract_citations_from_qmd(paper_path, project_root)

    # Extract variables used in the paper
    used_variables = extract_variables_from_qmd(paper_path, project_root)

    # Extract citations embedded in those variable values
    if variables_yml_path and variables_yml_path.exists() and used_variables:
        variable_citations = extract_citations_from_variable_values(
            used_variables, variables_yml_path
        )
        citations = citations | variable_citations

    if not citations:
        print(f"[WARN] No citations found in {paper_path.name}")
        return (0, used_variables)

    # Read the main bibliography
    if not main_bib_path.exists():
        print(f"[ERROR] Main bibliography not found: {main_bib_path}")
        return (0, used_variables)

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

    return (len(filtered_entries), used_variables)


def _extract_chapters_from_config(config: dict) -> List[str]:
    """
    Extract list of QMD files from a Quarto config's book.chapters section.

    Handles nested structures with sections and various formats.

    Args:
        config: Parsed Quarto YAML config

    Returns:
        List of QMD file paths
    """
    files: List[str] = []

    def extract_items(items):
        if not isinstance(items, list):
            return
        for item in items:
            if isinstance(item, str):
                if item.endswith('.qmd'):
                    files.append(item)
            elif isinstance(item, dict):
                if "href" in item:
                    href = item["href"]
                    if href.endswith('.qmd'):
                        files.append(href)
                if "chapters" in item:
                    extract_items(item["chapters"])
                if "contents" in item:
                    extract_items(item["contents"])

    book = config.get("book", {})
    if "chapters" in book:
        extract_items(book["chapters"])

    return files


def generate_all_paper_bibliographies(project_root: Path) -> Dict[str, int]:
    """
    Generate filtered bibliographies AND filtered _variables.yml for all standalone papers.

    For each paper defined in _quarto-*.yml configs:
    1. Scans the index-source file AND all book.chapters for variable usage
    2. Generates references-{paper}.bib with only used citations
    3. Generates _variables-{paper}.yml with only used variables

    This ensures:
    - PDFs only include cited references (not all 700+ entries)
    - Citeproc doesn't warn about citations in unused variable values

    Args:
        project_root: Path to project root

    Returns:
        Dict mapping paper names to number of entries in their bibliography
    """
    main_bib = project_root / "references.bib"
    if not main_bib.exists():
        print("[ERROR] references.bib not found")
        return {}

    variables_yml = project_root / "_variables.yml"
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

        # Collect all QMD files to scan: index-source + all chapters
        qmd_files_to_scan: List[Path] = []

        if index_source:
            paper_path = project_root / index_source
            if paper_path.exists():
                qmd_files_to_scan.append(paper_path)
            else:
                print(f"[WARN] Paper not found: {index_source}")

        # Also scan all chapters listed in book.chapters
        chapter_files = _extract_chapters_from_config(config)
        for chapter_file in chapter_files:
            chapter_path = project_root / chapter_file
            if chapter_path.exists() and chapter_path not in qmd_files_to_scan:
                qmd_files_to_scan.append(chapter_path)

        if not qmd_files_to_scan:
            continue

        # Aggregate citations and variables from all files
        all_citations: Set[str] = set()
        all_variables: Set[str] = set()

        for qmd_path in qmd_files_to_scan:
            # Extract variables
            file_vars = extract_variables_from_qmd(qmd_path, project_root)
            all_variables.update(file_vars)

            # Extract direct citations
            file_citations = extract_citations_from_qmd(qmd_path, project_root)
            all_citations.update(file_citations)

        # Extract citations embedded in variable values
        if variables_yml.exists() and all_variables:
            variable_citations = extract_citations_from_variable_values(
                all_variables, variables_yml
            )
            all_citations.update(variable_citations)

        print(f"[*] {config_name}: scanned {len(qmd_files_to_scan)} files, found {len(all_variables)} variables, {len(all_citations)} citations")

        # Generate filtered bibliography
        if all_citations:
            output_bib = project_root / f"references-{config_name}.bib"
            count = _write_filtered_bibliography(
                citations=all_citations,
                main_bib_path=main_bib,
                output_bib_path=output_bib,
                paper_name=config_name
            )
            if count > 0:
                print(f"[OK] Generated {output_bib.name}: {count} entries")
                results[config_name] = count

        # Generate filtered variables file
        if all_variables:
            output_vars = project_root / f"_variables-{config_name}.yml"
            var_count = generate_filtered_variables_yml(
                variable_names=all_variables,
                full_variables_path=variables_yml,
                output_path=output_vars
            )
            if var_count > 0:
                print(f"[OK] Generated {output_vars.name}: {var_count} variables")
        else:
            # Create empty variables file if no variables used
            output_vars = project_root / f"_variables-{config_name}.yml"
            output_vars.write_text(
                "# AUTO-GENERATED - No variables used in this paper\n",
                encoding='utf-8'
            )
            print(f"[OK] Generated {output_vars.name}: 0 variables (empty)")

    return results


def _write_filtered_bibliography(
    citations: Set[str],
    main_bib_path: Path,
    output_bib_path: Path,
    paper_name: str
) -> int:
    """
    Write a filtered .bib file containing only specified citations.

    Args:
        citations: Set of citation keys to include
        main_bib_path: Path to the main references.bib file
        output_bib_path: Path to write the filtered .bib file
        paper_name: Name of the paper for header comment

    Returns:
        Number of entries written
    """
    if not main_bib_path.exists():
        print(f"[ERROR] Main bibliography not found: {main_bib_path}")
        return 0

    with open(main_bib_path, encoding='utf-8') as f:
        main_bib_content = f.read()

    # Parse BibTeX entries
    entries = []
    entry_starts = [(m.start(), m.group(1)) for m in re.finditer(r'(@\w+)\{', main_bib_content)]

    for i, (start, entry_type) in enumerate(entry_starts):
        key_match = re.match(r'@\w+\{([^,\s]+)', main_bib_content[start:])
        if not key_match:
            continue
        entry_key = key_match.group(1).strip()

        if i + 1 < len(entry_starts):
            end = entry_starts[i + 1][0]
        else:
            end = len(main_bib_content)

        entry_text = main_bib_content[start:end].strip()
        if not entry_text.endswith('}'):
            last_brace = entry_text.rfind('}')
            if last_brace > 0:
                entry_text = entry_text[:last_brace + 1]

        entries.append((entry_text, entry_key))

    # Filter entries to only include cited ones
    filtered_entries = []
    found_citations = set()

    for entry_text, entry_key in entries:
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
        f"% Filtered bibliography for {paper_name}",
        "% Re-generate with: python scripts/generate-everything-parameters-variables-calculations-references.py",
        "",
    ]
    content.extend(filtered_entries)

    output_bib_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_bib_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(content))

    return len(filtered_entries)


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
