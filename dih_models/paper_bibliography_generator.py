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

from dih_models.yaml_utils import yaml_safe_load, load_quarto_config
from dih_models.variable_naming import (
    get_auto_included_companion_suffixes,
    strip_generated_variable_suffix,
)

# Set UTF-8 encoding for stdout on Windows (reconfigure exists on TextIOWrapper in 3.7+)
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[reportAttributeAccessIssue]

# Pre-compiled regex patterns (avoid re-compiling in loops)
_RE_VAR = re.compile(r"\{\{<\s*var\s+([^\s>]+)\s*>\}\}")
_RE_INCLUDE = re.compile(r'\{\{<\s*include\s+([^>]+)\s*>\}\}')
_RE_BRACKETED_CITE = re.compile(r'\[-?@([a-zA-Z0-9_-]+)')
_RE_INLINE_CITE = re.compile(r'(?:^|[\s\[(])@([a-zA-Z][a-zA-Z0-9_-]+)(?=[,.\s\)\]:]|$)', re.MULTILINE)
_RE_DATA_SOURCE_REF = re.compile(r'data-source-ref="([^"]+)"')
_RE_VAR_CITE = re.compile(r'@([a-zA-Z][a-zA-Z0-9_-]+)')
_RE_BIB_ENTRY_START = re.compile(r'(@\w+)\{')
_RE_BIB_ENTRY_KEY = re.compile(r'@\w+\{([^,\s]+)')

# Module-level caches for cross-call reuse during a single generation run.
# These eliminate redundant file I/O and parsing when the same files are
# processed by multiple generators (bibliography, parameters, variables).
_file_content_cache: Dict[str, str] = {}
_extract_vars_cache: Dict[str, Set[str]] = {}
_extract_cites_cache: Dict[str, Set[str]] = {}
_variables_yml_cache: Dict[str, dict] = {}
_bib_entries_cache: Dict[str, list] = {}


def _cache_key_for_path(path: Path) -> str:
    """Return a normalized absolute path string without resolving symlinks."""
    return str(path.absolute())


def _read_file_cached(file_path: Path) -> str:
    """Read a file with content caching. Returns empty string if file doesn't exist."""
    key = _cache_key_for_path(file_path)
    if key not in _file_content_cache:
        if not file_path.exists():
            _file_content_cache[key] = ""
        else:
            with open(file_path, encoding='utf-8') as f:
                _file_content_cache[key] = f.read()
    return _file_content_cache[key]


def _load_variables_yml_cached(path: Path) -> dict:
    """Load and cache a YAML variables file (e.g., _variables.yml)."""
    key = _cache_key_for_path(path)
    if key not in _variables_yml_cache:
        if not path.exists():
            _variables_yml_cache[key] = {}
        else:
            with open(path, encoding='utf-8') as f:
                data = yaml_safe_load(f) or {}
            _variables_yml_cache[key] = data if isinstance(data, dict) else {}
    return _variables_yml_cache[key]


def _parse_bib_entries_cached(bib_path: Path) -> list:
    """Parse BibTeX entries with caching. Returns list of (entry_text, entry_key) tuples."""
    cache_key = _cache_key_for_path(bib_path)
    if cache_key not in _bib_entries_cache:
        content = _read_file_cached(Path(cache_key))
        if not content:
            _bib_entries_cache[cache_key] = []
        else:
            entries = []
            entry_starts = [(m.start(), m.group(1)) for m in _RE_BIB_ENTRY_START.finditer(content)]
            for i, (start, entry_type) in enumerate(entry_starts):
                key_match = _RE_BIB_ENTRY_KEY.match(content[start:])
                if not key_match:
                    continue
                entry_key = key_match.group(1).strip()
                end = entry_starts[i + 1][0] if i + 1 < len(entry_starts) else len(content)
                entry_text = content[start:end].strip()
                if not entry_text.endswith('}'):
                    last_brace = entry_text.rfind('}')
                    if last_brace > 0:
                        entry_text = entry_text[:last_brace + 1]
                entries.append((entry_text, entry_key))
            _bib_entries_cache[cache_key] = entries
    return _bib_entries_cache[cache_key]


def clear_file_caches() -> None:
    """Clear all file content and result caches (for testing or forced reload)."""
    _file_content_cache.clear()
    _extract_vars_cache.clear()
    _extract_cites_cache.clear()
    _variables_yml_cache.clear()
    _bib_entries_cache.clear()


def extract_variables_from_qmd(qmd_path: Path, project_root: Optional[Path] = None) -> Set[str]:
    """
    Extract all Quarto variable names used in a QMD file, including from {{< include >}} files.

    Pattern matched: {{< var variable_name >}}
    Results are cached per resolved file path for cross-call reuse.

    Args:
        qmd_path: Path to the QMD file to analyze
        project_root: Project root for resolving absolute include paths

    Returns:
        Set of variable names used in the file
    """
    cache_key = _cache_key_for_path(qmd_path)
    if cache_key in _extract_vars_cache:
        return _extract_vars_cache[cache_key].copy()

    if not qmd_path.exists():
        _extract_vars_cache[cache_key] = set()
        return set()

    variables: Set[str] = set()
    processed_files: Set[str] = set()

    def process_file(file_path: Path):
        """Recursively process a file and its includes."""
        resolved = _cache_key_for_path(file_path)
        if resolved in processed_files:
            return
        processed_files.add(resolved)

        content = _read_file_cached(file_path)
        if not content:
            return

        # Find all variable references
        for match in _RE_VAR.finditer(content):
            variables.add(match.group(1).strip())

        # Find and process {{< include >}} directives
        for match in _RE_INCLUDE.finditer(content):
            include_path_str = match.group(1).strip().strip('"\'')

            # Resolve include path
            if include_path_str.startswith('/'):
                if project_root:
                    include_path = project_root / include_path_str.lstrip('/')
                else:
                    include_path = Path(include_path_str.lstrip('/'))
            else:
                include_path = file_path.parent / include_path_str

            process_file(include_path.absolute())

    process_file(qmd_path.absolute())
    _extract_vars_cache[cache_key] = variables
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
    all_variables = _load_variables_yml_cached(variables_yml_path)
    if not all_variables:
        return set()

    citations: Set[str] = set()

    for var_name in variable_names:
        if var_name not in all_variables:
            continue

        value = str(all_variables[var_name])

        # Pattern 1: data-source-ref="citation-key" in HTML attributes
        for match in _RE_DATA_SOURCE_REF.finditer(value):
            ref = match.group(1).strip()
            # Skip empty refs and file paths
            if ref and not ref.startswith('/'):
                citations.add(ref)

        # Pattern 2: @citation-key (for _cite variables like @who-report-2024)
        for match in _RE_VAR_CITE.finditer(value):
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
    all_variables = _load_variables_yml_cached(full_variables_path)
    if not all_variables:
        print(f"[ERROR] Variables file not found or empty: {full_variables_path}")
        return 0

    # Filter to only requested variables
    filtered = {}
    for name in variable_names:
        if name in all_variables:
            filtered[name] = all_variables[name]

            # Base variables automatically bring along companion exports like
            # _cite and _latex. Generated variants (for example _nounit) do not.
            base_name = strip_generated_variable_suffix(name)
            if name == base_name:
                for suffix in get_auto_included_companion_suffixes():
                    companion_name = f"{base_name}{suffix}"
                    if companion_name in all_variables:
                        filtered[companion_name] = all_variables[companion_name]

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


def extract_citations_from_qmd(qmd_path: Path, project_root: Optional[Path] = None) -> Set[str]:
    """
    Extract all citation keys from a QMD file, including from {{< include >}} files.
    Results are cached per resolved file path for cross-call reuse.

    Args:
        qmd_path: Path to the QMD file to analyze
        project_root: Project root for resolving absolute include paths

    Returns:
        Set of citation keys (without @ prefix)
    """
    cache_key = _cache_key_for_path(qmd_path)
    if cache_key in _extract_cites_cache:
        return _extract_cites_cache[cache_key].copy()

    if not qmd_path.exists():
        _extract_cites_cache[cache_key] = set()
        return set()

    citations: Set[str] = set()
    processed_files: Set[str] = set()

    # Skip patterns and prefixes (defined once, not per file)
    skip_patterns = {
        'misc', 'article', 'book', 'inproceedings', 'techreport',
        'phdthesis', 'mastersthesis', 'incollection', 'manual',
        'proceedings', 'unpublished', 'booklet', 'conference',
        'property', 'media', 'keyframes', 'import', 'charset',
        'supports', 'layer', 'namespace', 'page', 'font-face',
    }
    skip_prefixes = ('eq-', 'fig-', 'tbl-', 'sec-', 'lst-', 'thm-', 'def-', 'lem-', 'cor-', 'prp-')

    def process_file(file_path: Path):
        """Recursively process a file and its includes."""
        resolved = _cache_key_for_path(file_path)
        if resolved in processed_files:
            return
        processed_files.add(resolved)

        content = _read_file_cached(file_path)
        if not content:
            return

        # Pattern 1: Bracketed citations [@key] or [-@key]
        for match in _RE_BRACKETED_CITE.finditer(content):
            key = match.group(1)
            if key not in skip_patterns and not key.startswith(skip_prefixes):
                citations.add(key)

        # Pattern 2: Inline citations @key
        for match in _RE_INLINE_CITE.finditer(content):
            key = match.group(1)
            if key not in skip_patterns and not key.startswith(skip_prefixes):
                citations.add(key)

        # Find and process {{< include >}} directives
        for match in _RE_INCLUDE.finditer(content):
            include_path_str = match.group(1).strip().strip('"\'')

            if include_path_str.startswith('/'):
                if project_root:
                    include_path = project_root / include_path_str.lstrip('/')
                else:
                    include_path = Path(include_path_str.lstrip('/'))
            else:
                include_path = file_path.parent / include_path_str

            process_file(include_path.absolute())

    process_file(qmd_path.absolute())
    _extract_cites_cache[cache_key] = citations
    return citations


def generate_paper_bibliography(
    paper_path: Path,
    main_bib_path: Path,
    output_bib_path: Path,
    project_root: Optional[Path] = None,
    variables_yml_path: Optional[Path] = None,
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

    # Parse BibTeX entries (cached - parsed once, reused across papers)
    if not main_bib_path.exists():
        print(f"[ERROR] Main bibliography not found: {main_bib_path}")
        return (0, used_variables)

    entries = _parse_bib_entries_cached(main_bib_path)

    # Filter entries to only include cited ones
    filtered_entries = []
    found_citations = set()

    for entry_text, entry_key in entries:
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
    output_content = [
        "% AUTO-GENERATED FILE - DO NOT EDIT",
        f"% Filtered bibliography for {paper_path.name}",
        f"% Re-generate with: python scripts/generate-everything-parameters-variables-calculations-references.py",
        "",
    ]
    output_content.extend(filtered_entries)

    output_bib_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_bib_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(output_content))

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

        config = load_quarto_config(config_file)

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

    # Use cached bib entries (parsed once, reused across all papers)
    entries = _parse_bib_entries_cached(main_bib_path)

    # Filter entries to only include cited ones
    filtered_entries = []
    found_citations = set()

    for entry_text, entry_key in entries:
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
    output_content = [
        "% AUTO-GENERATED FILE - DO NOT EDIT",
        f"% Filtered bibliography for {paper_name}",
        "% Re-generate with: python scripts/generate-everything-parameters-variables-calculations-references.py",
        "",
    ]
    output_content.extend(filtered_entries)

    output_bib_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_bib_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(output_content))

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
