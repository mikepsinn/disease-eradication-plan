#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parameters and Calculations QMD Generator for dih_models
=========================================================

Generate the parameters-and-calculations.qmd appendix file with comprehensive
documentation of all parameters used in the economic analysis.

Functions:
- generate_parameters_and_calculations_qmd() - Generate the appendix QMD file

Usage:
    from dih_models.parameters_and_calculations_qmd_generator import (
        generate_parameters_and_calculations_qmd
    )

    # Generate the appendix
    generate_parameters_and_calculations_qmd(
        parameters=parameters_dict,
        output_path=Path("knowledge/appendix/parameters-and-calculations.qmd"),
        available_refs=reference_ids_set,
        params_file=Path("dih_models/parameters.py")
    )
"""

from pathlib import Path
from typing import Any, Dict

from dih_models.formatting import format_parameter_value
from dih_models.latex_generation import generate_auto_latex, smart_title_case
from dih_models.quarto_formatting import convert_qmd_to_html, generate_uncertainty_section


def generate_parameters_and_calculations_qmd(
    parameters: Dict[str, Dict[str, Any]],
    output_path: Path,
    available_refs: set = None,
    params_file: Path = None
):
    """
    Generate comprehensive parameters-and-calculations.qmd appendix.

    Creates an academic reference page with:
    - All parameters organized by type (external/calculated/definition)
    - LaTeX equations where available (hardcoded or auto-generated)
    - Citations and source links
    - Confidence indicators and metadata
    - Uncertainty ranges with human-friendly explanations
    - Links to sensitivity analysis charts and Monte Carlo distributions

    Args:
        parameters: Dict of parameter metadata from parse_parameters_file()
        output_path: Path to write the QMD file
        available_refs: Set of valid reference IDs from references.qmd (optional, for detecting reference links)
        params_file: Path to parameters.py (for auto-generating latex equations)
    """
    # Categorize parameters by source type
    external_params = []
    calculated_params = []
    definition_params = []

    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data["value"]

        if hasattr(value, "source_type"):
            # Handle both enum and string source_type
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)

            if source_type_str == "external":
                external_params.append((param_name, param_data))
            elif source_type_str == "calculated":
                calculated_params.append((param_name, param_data))
            elif source_type_str == "definition":
                definition_params.append((param_name, param_data))
        else:
            # No source_type - treat as definition
            definition_params.append((param_name, param_data))

    # Generate QMD content
    content = []
    content.append("---")
    content.append('title: "Parameters and Calculations Reference"')
    content.append('subtitle: "Comprehensive Documentation of Economic Model Variables"')
    content.append("format:")
    content.append("  html:")
    content.append("    toc: true")
    content.append("    toc-depth: 3")
    content.append("    number-sections: true")
    content.append("    code-fold: true")
    content.append("---")
    content.append("")
    content.append("## Overview")
    content.append("")
    content.append(
        "This appendix provides comprehensive documentation of all parameters and calculations used in the economic analysis of a 1% treaty and decentralized framework for drug assessment."
    )
    content.append("")
    content.append(f"**Total parameters**: {len(parameters)}")
    content.append("")
    content.append(f"- External sources (peer-reviewed): {len(external_params)}")
    content.append(f"- Calculated values: {len(calculated_params)}")
    content.append(f"- Core definitions: {len(definition_params)}")
    content.append("")

    # Calculated parameters section (moved first for prominence)
    if calculated_params:
        content.append("## Calculated Values {#sec-calculated}")
        content.append("")
        content.append("Parameters derived from mathematical formulas and economic models.")
        content.append("")

        for param_name, param_data in calculated_params:
            value = param_data["value"]

            # Generate display title with priority chain: display_name → smart_title_case() → .title()
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            content.append(f"### {display_title} {{#sec-{param_name.lower()}}}")
            content.append("")

            # Value
            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)
            content.append(f"**Value**: {formatted}")
            content.append("")

            # Description
            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            # Show input parameters with links
            if hasattr(value, "inputs") and value.inputs:
                content.append("**Inputs**:")
                content.append("")
                for inp_name in value.inputs:
                    inp_meta = parameters.get(inp_name, {})
                    inp_value = inp_meta.get('value')

                    if inp_value is None:
                        # Handle missing input gracefully
                        content.append(f"- [{smart_title_case(inp_name)}](#sec-{inp_name.lower()}): *not found*")
                        continue

                    # Get display name
                    if hasattr(inp_value, "display_name") and inp_value.display_name:
                        inp_display = inp_value.display_name
                    else:
                        inp_display = smart_title_case(inp_name)

                    # Format value
                    inp_unit = getattr(inp_value, "unit", "")
                    inp_formatted = format_parameter_value(inp_value, inp_unit)

                    # Add uncertainty information if available (verbose format)
                    uncertainty_str = ""
                    if hasattr(inp_value, "confidence_interval") and inp_value.confidence_interval:
                        low, high = inp_value.confidence_interval
                        low_str = format_parameter_value(low, inp_unit)
                        high_str = format_parameter_value(high, inp_unit)
                        uncertainty_str = f" (95% CI: {low_str} - {high_str})"
                    elif hasattr(inp_value, "std_error") and inp_value.std_error:
                        se_str = format_parameter_value(inp_value.std_error, inp_unit)
                        uncertainty_str = f" (SE: ±{se_str})"

                    # Get source type for visual indicator
                    source_type_indicator = ""
                    if hasattr(inp_value, "source_type"):
                        source_type_str = str(inp_value.source_type.value) if hasattr(inp_value.source_type, 'value') else str(inp_value.source_type)
                        if source_type_str == "external":
                            source_type_indicator = " 📊"  # External data
                        elif source_type_str == "calculated":
                            source_type_indicator = " 🔢"  # Calculated value

                    # Link to parameter section
                    content.append(f"- [{inp_display}](#sec-{inp_name.lower()}){source_type_indicator}: {inp_formatted}{uncertainty_str}")

                content.append("")

            # LaTeX equation - prominently displayed
            # Priority: hardcoded latex > auto-generated latex > formula
            hardcoded_latex = getattr(value, "latex", None)
            auto_latex = generate_auto_latex(param_name, value, parameters, params_file=params_file) if not hardcoded_latex else None

            if hardcoded_latex:
                content.append("$$")
                content.append(hardcoded_latex)
                content.append("$$")
                content.append("")
            elif auto_latex:
                content.append("$$")
                content.append(auto_latex)
                content.append("$$")
                content.append("")
            elif hasattr(value, "formula") and value.formula:
                content.append(f"*Formula*: `{value.formula}`")
                content.append("")

            # Source reference (calculation methodology)
            if hasattr(value, "source_ref") and value.source_ref:
                source_ref = value.source_ref

                # Convert ReferenceID enum to string value (if needed)
                if hasattr(source_ref, 'value'):
                    source_ref = source_ref.value
                else:
                    source_ref = str(source_ref)

                # Detect if this is an intra-document anchor (no path separators, no file extension)
                is_anchor = "/" not in source_ref and ".qmd" not in source_ref and ".md" not in source_ref

                # Check if this anchor-like value is actually a reference ID from references.qmd
                is_reference_id = False
                if is_anchor and available_refs is not None:
                    is_reference_id = source_ref in available_refs

                # Friendly labels for common methodology references
                methodology_labels = {
                    "cure-bounty-estimates": "Cure Bounty Estimation Model",
                    "disease-related-caregiving-estimate": "Disease-Related Caregiving Analysis",
                    "calculated": "Direct Calculation",
                    "sipri-2024-spending": "SIPRI Military Spending Database",
                    "book-word-count": "Book Word Count Analysis",
                }

                if is_reference_id:
                    # This is a reference ID - link to references (extensionless for format-agnostic links)
                    # Quarto will resolve to references.html (HTML), references.pdf (PDF), or references.epub (EPUB)
                    link_target = f"../references#{source_ref}"
                    link_text = methodology_labels.get(source_ref, source_ref)
                elif is_anchor:
                    # Intra-document anchor - add # prefix
                    link_target = f"#{source_ref}"
                    link_text = methodology_labels.get(source_ref, source_ref)
                else:
                    # File path - convert to relative path
                    if source_ref.startswith("/"):
                        source_ref = source_ref.lstrip("/")

                    if source_ref.startswith("knowledge/"):
                        # Remove 'knowledge/' prefix and add '../' to go up from appendix/
                        source_ref = "../" + source_ref[len("knowledge/"):]

                    # Convert .qmd to .html for rendered output
                    link_target = convert_qmd_to_html(source_ref)
                    # Use the converted path for link text too (shows .html instead of .qmd)
                    link_text = link_target

                content.append(f"**Methodology**: [{link_text}]({link_target})")
                content.append("")

            # Uncertainty section with human-friendly explanations (for calculated values too)
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            # Confidence and notes
            metadata = []
            if hasattr(value, "confidence") and value.confidence:
                confidence_labels = {
                    "high": "✓ High confidence",
                    "medium": "~ Medium confidence",
                    "low": "? Low confidence",
                    "estimated": "≈ Estimated",
                }
                metadata.append(confidence_labels.get(value.confidence, value.confidence))

            if hasattr(value, "conservative") and value.conservative:
                metadata.append("⚖️ Conservative estimate")

            if metadata:
                content.append("*" + " • ".join(metadata) + "*")
                content.append("")

            # Add uncertainty visualization if tornado/sensitivity data exists
            project_root = output_path.parent.parent.parent  # Go up from knowledge/appendix/ to project root
            tornado_qmd = project_root / "knowledge" / "figures" / f"tornado-{param_name.lower()}.qmd"
            sensitivity_qmd = project_root / "knowledge" / "figures" / f"sensitivity-table-{param_name.lower()}.qmd"
            mc_dist_qmd = project_root / "knowledge" / "figures" / f"mc-distribution-{param_name.lower()}.qmd"
            exceedance_qmd = project_root / "knowledge" / "figures" / f"exceedance-{param_name.lower()}.qmd"

            if tornado_qmd.exists():
                content.append("#### Sensitivity Analysis")
                content.append("")
                content.append(f"{{{{< include ../figures/tornado-{param_name.lower()}.qmd >}}}}")
                content.append("")

                if sensitivity_qmd.exists():
                    content.append(f"{{{{< include ../figures/sensitivity-table-{param_name.lower()}.qmd >}}}}")
                    content.append("")

            # Add Monte Carlo distribution chart if exists
            if mc_dist_qmd.exists():
                content.append("#### Monte Carlo Distribution")
                content.append("")
                content.append(f"{{{{< include ../figures/mc-distribution-{param_name.lower()}.qmd >}}}}")
                content.append("")

            # Add exceedance/CDF chart if exists
            if exceedance_qmd.exists():
                content.append("#### Exceedance Probability")
                content.append("")
                content.append(f"{{{{< include ../figures/exceedance-{param_name.lower()}.qmd >}}}}")
                content.append("")

            content.append("")

    # External parameters section
    if external_params:
        content.append("## External Data Sources {#sec-external}")
        content.append("")
        content.append(
            "Parameters sourced from peer-reviewed publications, institutional databases, and authoritative reports."
        )
        content.append("")

        for param_name, param_data in external_params:
            value = param_data["value"]

            # Generate display title with priority chain: display_name → smart_title_case() → .title()
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            content.append(f"### {display_title} {{#sec-{param_name.lower()}}}")
            content.append("")

            # Value
            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)
            content.append(f"**Value**: {formatted}")
            content.append("")

            # Description
            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            # Source citation
            if hasattr(value, "source_ref") and value.source_ref:
                source_ref = value.source_ref
                # Convert ReferenceID enum to string value for URL
                source_ref_str = source_ref.value if hasattr(source_ref, 'value') else str(source_ref)
                # Use the reference ID value for display (not the enum representation)
                display_ref = source_ref_str
                # Check if source_ref is a .qmd file path or a references.qmd anchor
                # Use relative paths for multi-format compatibility (HTML, PDF, EPUB)
                if source_ref_str.endswith('.qmd'):
                    # It's a path to another .qmd document
                    # Convert absolute path to relative from knowledge/appendix/
                    if source_ref_str.startswith('/knowledge/'):
                        # /knowledge/appendix/foo.qmd -> foo (same dir)
                        # /knowledge/foo.qmd -> ../foo (parent dir)
                        rel_path = source_ref_str[len('/knowledge/'):]
                        if rel_path.startswith('appendix/'):
                            rel_path = rel_path[len('appendix/'):]
                        else:
                            rel_path = '../' + rel_path
                    else:
                        rel_path = source_ref_str
                    # Remove .qmd extension for format-agnostic links
                    rel_path = convert_qmd_to_html(rel_path)
                    content.append(f"**Source**: [{display_ref}]({rel_path})")
                else:
                    # It's a reference anchor ID - link to references.qmd (relative path)
                    content.append(f"**Source**: [{display_ref}](../references.qmd#{source_ref_str})")
                content.append("")

            # Uncertainty section with human-friendly explanations
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            # Add input distribution chart if exists (for external params with uncertainty)
            project_root = output_path.parent.parent.parent  # Go up from knowledge/appendix/ to project root
            dist_qmd = project_root / "knowledge" / "figures" / f"distribution-{param_name.lower()}.qmd"
            if dist_qmd.exists():
                content.append("#### Input Distribution")
                content.append("")
                content.append(f"{{{{< include ../figures/distribution-{param_name.lower()}.qmd >}}}}")
                content.append("")

            # Confidence and metadata - cleaner formatting
            metadata = []
            if hasattr(value, "confidence") and value.confidence:
                confidence_labels = {
                    "high": "✓ High confidence",
                    "medium": "~ Medium confidence",
                    "low": "? Low confidence",
                    "estimated": "≈ Estimated",
                }
                metadata.append(confidence_labels.get(value.confidence, value.confidence))

            if hasattr(value, "peer_reviewed") and value.peer_reviewed:
                metadata.append("📊 Peer-reviewed")

            # Only show last_updated if it's not None/empty
            if hasattr(value, "last_updated") and value.last_updated:
                metadata.append(f"Updated {value.last_updated}")

            if metadata:
                content.append("*" + " • ".join(metadata) + "*")
                content.append("")

            content.append("")

    # Core definitions section
    if definition_params:
        content.append("## Core Definitions {#sec-definitions}")
        content.append("")
        content.append("Fundamental parameters and constants used throughout the analysis.")
        content.append("")

        for param_name, param_data in definition_params:
            value = param_data["value"]

            # Generate display title with priority chain: display_name → smart_title_case() → .title()
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            content.append(f"### {display_title} {{#sec-{param_name.lower()}}}")
            content.append("")

            # Value
            unit = getattr(value, "unit", "")
            formatted = format_parameter_value(value, unit)
            content.append(f"**Value**: {formatted}")
            content.append("")

            # Description
            if hasattr(value, "description") and value.description:
                content.append(f"{value.description}")
                content.append("")

            # Uncertainty section with human-friendly explanations (for definitions too)
            uncertainty_content = generate_uncertainty_section(value, unit)
            content.extend(uncertainty_content)

            content.append("*Core definition*")
            content.append("")
            content.append("")

    # Write file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(external_params)} external parameters")
    print(f"     {len(calculated_params)} calculated parameters")
    print(f"     {len(definition_params)} core definitions")
