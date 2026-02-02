#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-Paper Parameters and Calculations QMD Generator
=====================================================

Generate filtered parameters-and-calculations-{paper}.qmd files for standalone papers.
This ensures each paper's appendix only includes the parameters actually used,
plus all their transitive dependencies (inputs to calculated parameters).

Functions:
- get_all_required_parameters() - Trace dependencies to find all needed parameters
- generate_all_paper_parameters_qmd() - Process all standalone papers

Usage:
    from dih_models.paper_parameters_and_calculations_qmd_generator import generate_all_paper_parameters_qmd
    from pathlib import Path

    project_root = Path(".")
    results = generate_all_paper_parameters_qmd(project_root, parameters)
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

from dih_models.parameters_and_calculations_qmd_generator import (
    generate_parameters_and_calculations_qmd,
)
from dih_models.paper_bibliography_generator import (
    extract_variables_from_qmd,
    _extract_chapters_from_config,
)
from dih_models.reference_parser import parse_references_bib


def get_all_required_parameters(
    used_variables: Set[str],
    parameters: Dict[str, Dict[str, Any]]
) -> Set[str]:
    """
    Given directly-used variables, find ALL parameters needed
    (including transitive dependencies through inputs).

    For example, if a paper uses `treaty_roi` which depends on
    `peace_dividend` and `treaty_cost`, this function returns all three
    even if only `treaty_roi` was directly referenced.

    Args:
        used_variables: Set of lowercase variable names used in QMD files
        parameters: Full parameters dictionary from parse_parameters_file()

    Returns:
        Set of UPPERCASE parameter names including all dependencies
    """
    required: Set[str] = set()

    def add_with_dependencies(param_name: str, visited: Set[str]):
        """Recursively add a parameter and all its input dependencies."""
        if param_name in visited:
            return  # Cycle detection
        visited.add(param_name)

        if param_name not in parameters:
            return  # Unknown parameter

        required.add(param_name)

        # Get the parameter value
        meta = parameters.get(param_name, {})
        value = meta.get("value")

        # If it has inputs, recursively add them
        if value is not None and hasattr(value, "inputs") and value.inputs:
            for inp in value.inputs:  # type: ignore[union-attr]
                add_with_dependencies(inp, visited)

    # Process each used variable
    for var_name in used_variables:
        # Convert lowercase variable to UPPERCASE parameter name
        param_name = var_name.upper()

        # Handle special suffixes (_cite, _latex, etc.)
        # These refer to the base parameter
        for suffix in ('_CITE', '_LATEX', '_SHORT', '_LONG'):
            if param_name.endswith(suffix):
                param_name = param_name[:-len(suffix)]
                break

        if param_name in parameters:
            add_with_dependencies(param_name, set())

    return required


def generate_all_paper_parameters_qmd(
    project_root: Path,
    parameters: Dict[str, Dict[str, Any]],
    available_refs: Optional[Set[str]] = None,
    params_file: Optional[Path] = None,
    citation_data: Optional[Dict[str, Dict[str, Any]]] = None
) -> Dict[str, int]:
    """
    Generate filtered parameters-and-calculations QMD files for all Quarto configs.

    For each config defined in _quarto-*.yml (including book, manual, and standalone papers):
    1. Scans all QMD files listed in the config to find used variables
    2. Traces dependencies to find all required parameters
    3. Generates parameters-and-calculations-{config}.qmd with only needed parameters

    This ensures each output (book, manual, individual papers) gets a focused appendix
    containing only the parameters actually used in that document.

    Args:
        project_root: Path to project root
        parameters: Full parameters dictionary
        available_refs: Set of valid reference IDs from references.qmd
        params_file: Path to parameters.py for LaTeX generation
        citation_data: Pre-parsed citation data from parse_references_bib() (optional, for performance).
                       If not provided, will parse references.bib once and reuse for all papers.

    Returns:
        Dict mapping paper names to number of parameters in their appendix
    """
    results: Dict[str, int] = {}

    # Pre-parse citation data once for all papers (major performance optimization)
    if citation_data is None:
        bib_path = project_root / "references.bib"
        if bib_path.exists():
            citation_data = parse_references_bib(bib_path)

    # Find all Quarto configs (including book and manual)
    for config_file in project_root.glob("_quarto-*.yml"):
        config_name = config_file.stem.replace("_quarto-", "")

        with open(config_file, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        dih_render = config.get("dih-render", {})
        index_source = dih_render.get("index-source")

        # Collect all QMD files to scan
        qmd_files_to_scan: List[Path] = []

        if index_source:
            paper_path = project_root / index_source
            if paper_path.exists():
                qmd_files_to_scan.append(paper_path)

        # Also scan all chapters listed in book.chapters
        chapter_files = _extract_chapters_from_config(config)
        for chapter_file in chapter_files:
            chapter_path = project_root / chapter_file
            if chapter_path.exists() and chapter_path not in qmd_files_to_scan:
                qmd_files_to_scan.append(chapter_path)

        if not qmd_files_to_scan:
            continue

        # Aggregate variables from all files
        all_variables: Set[str] = set()
        for qmd_path in qmd_files_to_scan:
            file_vars = extract_variables_from_qmd(qmd_path, project_root)
            all_variables.update(file_vars)

        if not all_variables:
            print(f"[*] {config_name}: no variables found, skipping parameters appendix")
            continue

        # Trace dependencies to get all required parameters
        required_params = get_all_required_parameters(all_variables, parameters)

        print(f"[*] {config_name}: {len(all_variables)} variables -> {len(required_params)} parameters (with dependencies)")

        # Filter parameters to only those required
        filtered_parameters = {k: v for k, v in parameters.items() if k in required_params}

        if not filtered_parameters:
            continue

        # Generate the filtered QMD using the main generator
        output_path = project_root / "knowledge" / "appendix" / f"parameters-and-calculations-{config_name}.qmd"
        count = generate_parameters_and_calculations_qmd(
            parameters=filtered_parameters,
            output_path=output_path,
            available_refs=available_refs,
            params_file=params_file,
            citation_data=citation_data
        )

        if count > 0:
            results[config_name] = count

    return results


if __name__ == "__main__":
    # Run standalone for testing
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from dih_models.reference_parser import parse_references_bib_keys

    project_root = Path(__file__).parent.parent

    # Parse references from BibTeX
    bib_path = project_root / "references.bib"
    available_refs = parse_references_bib_keys(bib_path)

    # Parse parameters (simplified - normally done by main script)
    params_file = project_root / "dih_models" / "parameters.py"

    # Import the parsing function from main script
    sys.path.insert(0, str(project_root / "scripts"))
    from importlib import import_module
    gen_module = import_module("generate-everything-parameters-variables-calculations-references")
    parameters = gen_module.parse_parameters_file(params_file)

    print(f"[*] Loaded {len(parameters)} parameters")
    print(f"[*] Generating per-paper parameters appendices...")

    results = generate_all_paper_parameters_qmd(
        project_root=project_root,
        parameters=parameters,
        available_refs=available_refs,
        params_file=params_file
    )

    print(f"[OK] Generated {len(results)} paper-specific appendices")
