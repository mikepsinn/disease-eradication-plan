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
- generate_paper_parameters_qmd() - Generate filtered QMD for a single paper
- generate_all_paper_parameters_qmd() - Process all standalone papers

Usage:
    from dih_models.paper_parameters_generator import generate_all_paper_parameters_qmd
    from pathlib import Path

    project_root = Path(".")
    results = generate_all_paper_parameters_qmd(project_root, parameters)
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from dih_models.formatting import format_parameter_value
from dih_models.latex_generation import generate_auto_latex, generate_expanded_latex, smart_title_case
from dih_models.latex_mobile_wrap import wrap_latex_for_mobile
from dih_models.paper_bibliography_generator import (
    extract_variables_from_qmd,
    _extract_chapters_from_config,
)
from dih_models.quarto_formatting import convert_qmd_to_html, generate_uncertainty_section
from dih_models.reference_parser import parse_references_qmd_detailed


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
        if hasattr(value, "inputs") and value.inputs:
            for inp in value.inputs:
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


def format_citation(ref_data: Dict[str, Any]) -> str:
    """
    Format citation data as a professional-looking citation string.

    Examples:
        - "SIPRI (2024) - Global Military Expenditure Database"
        - "WHO (2024) - Global Health Estimates"
    """
    author = ref_data.get('author', '')
    source = ref_data.get('source', '')
    year = ref_data.get('year', '')
    title = ref_data.get('title', '')

    citation_author = author if author else source

    parts = []
    if citation_author:
        if year:
            parts.append(f"{citation_author} ({year})")
        else:
            parts.append(citation_author)

    if title and title != citation_author:
        citation = f"{parts[0]} - {title}" if parts else title
    else:
        citation = parts[0] if parts else "Unknown Source"

    return citation


def generate_paper_parameters_qmd(
    paper_name: str,
    required_params: Set[str],
    all_parameters: Dict[str, Dict[str, Any]],
    output_path: Path,
    available_refs: Set[str] = None,
    params_file: Path = None
) -> int:
    """
    Generate filtered parameters-and-calculations-{paper}.qmd containing
    only the parameters needed for this paper.

    Args:
        paper_name: Name of the paper (e.g., "dfda-spec")
        required_params: Set of UPPERCASE parameter names to include
        all_parameters: Full parameters dictionary
        output_path: Path to write the QMD file
        available_refs: Set of valid reference IDs from references.qmd
        params_file: Path to parameters.py for auto-generating LaTeX

    Returns:
        Number of parameters included in the generated file
    """
    # Filter to only required parameters
    parameters = {k: v for k, v in all_parameters.items() if k in required_params}

    if not parameters:
        return 0

    # Parse references.qmd for professional citation formatting
    references_path = output_path.parent.parent / "references.qmd"
    citation_data = parse_references_qmd_detailed(references_path)

    # Categorize parameters by source type
    external_params = []
    calculated_params = []
    definition_params = []

    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data["value"]

        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)

            if source_type_str == "external":
                external_params.append((param_name, param_data))
            elif source_type_str == "calculated":
                calculated_params.append((param_name, param_data))
            elif source_type_str == "definition":
                definition_params.append((param_name, param_data))
        else:
            definition_params.append((param_name, param_data))

    # Generate QMD content
    content = []
    content.append("---")
    content.append(f'title: "Methodology, Parameters, and Calculations"')
    content.append(f'description: "Parameter definitions, formulas, uncertainty ranges, and data sources."')
    content.append("format:")
    content.append("  html:")
    content.append("    toc: true")
    content.append("    toc-depth: 3")
    content.append("    number-sections: true")
    content.append("    code-fold: true")
    content.append("---")
    content.append("")
    content.append("::: {.content-visible when-format=\"html\"}")
    content.append("")
    content.append(f"**{len(parameters)} parameters** used in this paper:")
    content.append("")
    content.append(
        f"This appendix documents the {len(parameters)} parameters used in this paper. "
        ""
    )
    content.append("")
    content.append(f"**Total parameters**: {len(parameters)}")
    content.append("")
    content.append(f"- External sources (peer-reviewed): {len(external_params)}")
    content.append(f"- Calculated values: {len(calculated_params)}")
    content.append(f"- Core definitions: {len(definition_params)}")
    content.append("")

    # Quick Navigation
    content.append("### Quick Navigation")
    content.append("")
    nav_links = []
    if calculated_params:
        nav_links.append(f"[Calculated Values](#sec-calculated) ({len(calculated_params)} parameters)")
    if external_params:
        nav_links.append(f"[External Data Sources](#sec-external) ({len(external_params)} parameters)")
    if definition_params:
        nav_links.append(f"[Core Definitions](#sec-definitions) ({len(definition_params)} parameters)")
    if nav_links:
        content.append(" | ".join(nav_links))
        content.append("")
    content.append("")

    # Calculated parameters section
    if calculated_params:
        content.append("## Calculated Values {#sec-calculated}")
        content.append("")
        content.append("Parameters derived from mathematical formulas and economic models.")
        content.append("")

        for param_name, param_data in calculated_params:
            value = param_data["value"]

            # Display title
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            # Value
            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)

            content.append(f"### {display_title}: {formatted} {{#sec-{param_name.lower()}}}")
            content.append("")

            # Collapsible details
            content.append("::: {.callout-note collapse=\"true\" title=\"Show details\"}")
            content.append("")

            # Description
            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            # Input parameters with links
            if hasattr(value, "inputs") and value.inputs:
                content.append("**Inputs**:")
                content.append("")
                for inp_name in value.inputs:
                    inp_meta = all_parameters.get(inp_name, {})
                    inp_value = inp_meta.get('value')

                    if inp_value is None:
                        content.append(f"- [{smart_title_case(inp_name)}](#sec-{inp_name.lower()}): *not found*")
                        continue

                    if hasattr(inp_value, "display_name") and inp_value.display_name:
                        inp_display = inp_value.display_name
                    else:
                        inp_display = smart_title_case(inp_name)

                    inp_unit = getattr(inp_value, "unit", "")
                    inp_formatted = format_parameter_value(inp_value, inp_unit)

                    # Uncertainty info
                    uncertainty_str = ""
                    if hasattr(inp_value, "confidence_interval") and inp_value.confidence_interval:
                        low, high = inp_value.confidence_interval
                        low_str = format_parameter_value(low, inp_unit)
                        high_str = format_parameter_value(high, inp_unit)
                        uncertainty_str = f" (95% CI: {low_str} - {high_str})"
                    elif hasattr(inp_value, "std_error") and inp_value.std_error:
                        se_str = format_parameter_value(inp_value.std_error, inp_unit)
                        uncertainty_str = f" (SE: +/-{se_str})"

                    content.append(f"- [{inp_display}](#sec-{inp_name.lower()}): {inp_formatted}{uncertainty_str}")

                content.append("")

            # LaTeX equation
            hardcoded_latex = getattr(value, "latex", None)
            expanded_latex = generate_expanded_latex(param_name, value, all_parameters, params_file=params_file) if not hardcoded_latex else None

            if hardcoded_latex:
                wrapped_latex = wrap_latex_for_mobile(hardcoded_latex, max_width=60)
                content.append("$$")
                content.append(wrapped_latex)
                content.append("$$")
                content.append("")
            elif expanded_latex:
                wrapped_latex = wrap_latex_for_mobile(expanded_latex, max_width=60)
                content.append("$$")
                content.append(wrapped_latex)
                content.append("$$")
                content.append("")
            elif hasattr(value, "formula") and value.formula:
                content.append(f"*Formula*: `{value.formula}`")
                content.append("")

            # Source reference
            if hasattr(value, "source_ref") and value.source_ref:
                source_ref = value.source_ref
                if hasattr(source_ref, 'value'):
                    source_ref = source_ref.value
                else:
                    source_ref = str(source_ref)

                is_anchor = "/" not in source_ref and ".qmd" not in source_ref and ".md" not in source_ref
                is_reference_id = is_anchor and available_refs and source_ref in available_refs

                if is_reference_id:
                    link_target = f"../references.qmd#{source_ref}"
                    if source_ref in citation_data:
                        link_text = format_citation(citation_data[source_ref])
                    else:
                        link_text = source_ref
                elif is_anchor:
                    link_target = f"#{source_ref}"
                    link_text = source_ref
                else:
                    if source_ref.startswith("/"):
                        source_ref = source_ref.lstrip("/")
                    if source_ref.startswith("knowledge/"):
                        source_ref = "../" + source_ref[len("knowledge/"):]
                    link_target = convert_qmd_to_html(source_ref)
                    link_text = link_target

                content.append(f"**Methodology**: [{link_text}]({link_target})")
                content.append("")

            # Uncertainty section
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            # Confidence metadata
            metadata = []
            if hasattr(value, "confidence") and value.confidence:
                confidence_labels = {
                    "high": "High confidence",
                    "medium": "Medium confidence",
                    "low": "Low confidence",
                    "estimated": "Estimated",
                }
                metadata.append(confidence_labels.get(value.confidence, value.confidence))

            if hasattr(value, "conservative") and value.conservative:
                metadata.append("Conservative estimate")

            if metadata:
                content.append("*" + " | ".join(metadata) + "*")
                content.append("")

            # Include sensitivity charts if they exist
            project_root = output_path.parent.parent.parent
            tornado_qmd = project_root / "knowledge" / "figures" / f"tornado-{param_name.lower()}.qmd"
            if tornado_qmd.exists():
                content.append("#### Sensitivity Analysis")
                content.append("")
                content.append(f"{{{{< include ../figures/tornado-{param_name.lower()}.qmd >}}}}")
                content.append("")

            mc_dist_qmd = project_root / "knowledge" / "figures" / f"mc-distribution-{param_name.lower()}.qmd"
            if mc_dist_qmd.exists():
                content.append("#### Monte Carlo Distribution")
                content.append("")
                content.append(f"{{{{< include ../figures/mc-distribution-{param_name.lower()}.qmd >}}}}")
                content.append("")

            content.append(":::")
            content.append("")

    # External parameters section
    if external_params:
        content.append("## External Data Sources {#sec-external}")
        content.append("")
        content.append("Parameters sourced from peer-reviewed publications and authoritative reports.")
        content.append("")

        for param_name, param_data in external_params:
            value = param_data["value"]

            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)

            content.append(f"### {display_title}: {formatted} {{#sec-{param_name.lower()}}}")
            content.append("")

            content.append("::: {.callout-note collapse=\"true\" title=\"Show details\"}")
            content.append("")

            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            # Source citation
            if hasattr(value, "source_ref") and value.source_ref:
                source_ref = value.source_ref
                source_ref_str = source_ref.value if hasattr(source_ref, 'value') else str(source_ref)

                if source_ref_str.endswith('.qmd'):
                    if source_ref_str.startswith('/knowledge/'):
                        rel_path = source_ref_str[len('/knowledge/'):]
                        if rel_path.startswith('appendix/'):
                            rel_path = rel_path[len('appendix/'):]
                        else:
                            rel_path = '../' + rel_path
                    else:
                        rel_path = source_ref_str
                    rel_path = convert_qmd_to_html(rel_path)
                    content.append(f"**Source**: [{source_ref_str}]({rel_path})")
                else:
                    if source_ref_str in citation_data:
                        formatted_citation = format_citation(citation_data[source_ref_str])
                        content.append(f"**Source**: [{formatted_citation}](../references.qmd#{source_ref_str})")
                    else:
                        content.append(f"**Source**: [{source_ref_str}](../references.qmd#{source_ref_str})")
                content.append("")

            # Uncertainty section
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            # Distribution chart if exists
            project_root = output_path.parent.parent.parent
            dist_qmd = project_root / "knowledge" / "figures" / f"distribution-{param_name.lower()}.qmd"
            if dist_qmd.exists():
                content.append("#### Input Distribution")
                content.append("")
                content.append(f"{{{{< include ../figures/distribution-{param_name.lower()}.qmd >}}}}")
                content.append("")

            # Metadata
            metadata = []
            if hasattr(value, "confidence") and value.confidence:
                confidence_labels = {
                    "high": "High confidence",
                    "medium": "Medium confidence",
                    "low": "Low confidence",
                    "estimated": "Estimated",
                }
                metadata.append(confidence_labels.get(value.confidence, value.confidence))

            if hasattr(value, "peer_reviewed") and value.peer_reviewed:
                metadata.append("Peer-reviewed")

            if hasattr(value, "last_updated") and value.last_updated:
                metadata.append(f"Updated {value.last_updated}")

            if metadata:
                content.append("*" + " | ".join(metadata) + "*")
                content.append("")

            content.append(":::")
            content.append("")

    # Core definitions section
    if definition_params:
        content.append("## Core Definitions {#sec-definitions}")
        content.append("")
        content.append("Fundamental parameters and constants used throughout the analysis.")
        content.append("")

        for param_name, param_data in definition_params:
            value = param_data["value"]

            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)

            content.append(f"### {display_title}: {formatted} {{#sec-{param_name.lower()}}}")
            content.append("")

            content.append("::: {.callout-note collapse=\"true\" title=\"Show details\"}")
            content.append("")

            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            content.append("*Core definition*")
            content.append("")

            content.append(":::")
            content.append("")

    # Close content-visible block
    content.append(":::")
    content.append("")

    # Write file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline='\n') as f:
        f.write("\n".join(content))

    return len(parameters)


def generate_all_paper_parameters_qmd(
    project_root: Path,
    parameters: Dict[str, Dict[str, Any]],
    available_refs: Set[str] = None,
    params_file: Path = None
) -> Dict[str, int]:
    """
    Generate filtered parameters-and-calculations QMD files for all standalone papers.

    For each paper defined in _quarto-*.yml configs:
    1. Scans all QMD files to find used variables
    2. Traces dependencies to find all required parameters
    3. Generates parameters-and-calculations-{paper}.qmd with only needed parameters

    Args:
        project_root: Path to project root
        parameters: Full parameters dictionary
        available_refs: Set of valid reference IDs from references.qmd
        params_file: Path to parameters.py for LaTeX generation

    Returns:
        Dict mapping paper names to number of parameters in their appendix
    """
    results: Dict[str, int] = {}

    # Find all standalone paper configs
    for config_file in project_root.glob("_quarto-*.yml"):
        config_name = config_file.stem.replace("_quarto-", "")

        # Skip book config (it uses the full parameters file)
        if config_name == "book":
            continue

        # Skip test config
        if config_name == "test":
            continue

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

        # Generate the filtered QMD
        output_path = project_root / "knowledge" / "appendix" / f"parameters-and-calculations-{config_name}.qmd"
        count = generate_paper_parameters_qmd(
            paper_name=config_name,
            required_params=required_params,
            all_parameters=parameters,
            output_path=output_path,
            available_refs=available_refs,
            params_file=params_file
        )

        if count > 0:
            print(f"[OK] Generated {output_path.name}: {count} parameters")
            results[config_name] = count

    return results


if __name__ == "__main__":
    # Run standalone for testing
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from dih_models.reference_parser import parse_references_qmd

    project_root = Path(__file__).parent.parent

    # Parse references
    references_path = project_root / "knowledge" / "references.qmd"
    available_refs = parse_references_qmd(references_path)

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
