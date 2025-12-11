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
from dih_models.reference_parser import parse_references_qmd_detailed


def format_citation(ref_data: Dict[str, Any]) -> str:
    """
    Format citation data as a professional-looking citation string.

    Examples:
        - "SIPRI (2024) - Global Military Expenditure Database"
        - "WHO (2024) - Global Health Estimates"
        - "Smith et al. (2021) - Pragmatic Trial Design"

    Args:
        ref_data: Citation metadata from parse_references_qmd_detailed()

    Returns:
        Formatted citation string
    """
    author = ref_data.get('author', '')
    source = ref_data.get('source', '')
    year = ref_data.get('year', '')
    title = ref_data.get('title', '')

    # Use source if author not available (common for institutional reports)
    citation_author = author if author else source

    # Build citation: "Author (Year) - Title" or "Author (Year)"
    parts = []
    if citation_author:
        if year:
            parts.append(f"{citation_author} ({year})")
        else:
            parts.append(citation_author)

    if title and title != citation_author:
        # Add title if it's different from author/source
        citation = f"{parts[0]} - {title}" if parts else title
    else:
        citation = parts[0] if parts else "Unknown Source"

    return citation


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
    # Parse references.qmd for professional citation formatting
    references_path = output_path.parent.parent / "references.qmd"  # knowledge/references.qmd
    citation_data = parse_references_qmd_detailed(references_path)

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
    content.append("aliases:")
    content.append("  - calculations.html")
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
        content.append(" • ".join(nav_links))
        content.append("")
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
                    # This is a reference ID - format as professional citation
                    link_target = f"../references.qmd#{source_ref}"
                    # Try to use formatted citation from references.qmd
                    if source_ref in citation_data:
                        link_text = format_citation(citation_data[source_ref])
                    else:
                        # Fallback to friendly label or reference ID
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

            # Add uncertainty visualization if tornado/sensitivity data exists
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

                # Check if source_ref is a .qmd file path or a references.qmd anchor
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
                    content.append(f"**Source**: [{source_ref_str}]({rel_path})")
                else:
                    # It's a reference anchor ID - format as professional citation
                    if source_ref_str in citation_data:
                        formatted_citation = format_citation(citation_data[source_ref_str])
                        content.append(f"**Source**: [{formatted_citation}](../references.qmd#{source_ref_str})")
                    else:
                        # Fallback to reference ID if not found in citations
                        content.append(f"**Source**: [{source_ref_str}](../references.qmd#{source_ref_str})")
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

    # Add lazy-loading script for images (Intersection Observer with conservative threshold)
    content.append("")
    content.append("```{=html}")
    content.append("<script>")
    content.append("// Conservative lazy loading: only load images actually in viewport")
    content.append("(function() {")
    content.append("  'use strict';")
    content.append("  ")
    content.append("  let imageObserver = null;")
    content.append("  let loadTimeout = null;")
    content.append("  ")
    content.append("  function enableLazyLoading() {")
    content.append("    const images = document.querySelectorAll('img');")
    content.append("    ")
    content.append("    // Use Intersection Observer with conservative threshold")
    content.append("    // rootMargin: '50px' means only load images within 50px of viewport")
    content.append("    // This prevents loading images passed through during hash navigation")
    content.append("    imageObserver = new IntersectionObserver((entries, observer) => {")
    content.append("      entries.forEach(entry => {")
    content.append("        if (entry.isIntersecting && entry.intersectionRatio > 0) {")
    content.append("          const img = entry.target;")
    content.append("          // Only load if image is actually visible (not just passed through)")
    content.append("          if (img.dataset.src) {")
    content.append("            img.src = img.dataset.src;")
    content.append("            img.removeAttribute('data-src');")
    content.append("          } else if (!img.hasAttribute('loading')) {")
    content.append("            // For images without data-src, use native lazy loading")
    content.append("            img.setAttribute('loading', 'lazy');")
    content.append("          }")
    content.append("          observer.unobserve(img);")
    content.append("        }")
    content.append("      });")
    content.append("    }, {")
    content.append("      rootMargin: '50px',  // Only load images within 50px of viewport")
    content.append("      threshold: 0.01      // Trigger when at least 1% visible")
    content.append("    });")
    content.append("    ")
    content.append("    images.forEach(img => {")
    content.append("      imageObserver.observe(img);")
    content.append("    });")
    content.append("  }")
    content.append("  ")
    content.append("  // Handle hash navigation (clicking links to sections)")
    content.append("  // Delay loading to avoid loading images passed through during jump")
    content.append("  function handleHashNavigation() {")
    content.append("    if (loadTimeout) clearTimeout(loadTimeout);")
    content.append("    // Wait 300ms after navigation to let scroll settle")
    content.append("    // Images will load naturally via Intersection Observer when visible")
    content.append("    loadTimeout = setTimeout(() => {")
    content.append("      // Scroll has settled, Intersection Observer will handle visible images")
    content.append("      // No action needed - observer is already watching")
    content.append("    }, 300);")
    content.append("  }")
    content.append("  ")
    content.append("  // Initialize on page load")
    content.append("  if (document.readyState === 'loading') {")
    content.append("    document.addEventListener('DOMContentLoaded', enableLazyLoading);")
    content.append("  } else {")
    content.append("    enableLazyLoading();")
    content.append("  }")
    content.append("  ")
    content.append("  // Handle hash changes (clicking anchor links)")
    content.append("  window.addEventListener('hashchange', handleHashNavigation);")
    content.append("  ")
    content.append("  // Also handle initial hash if page loads with one")
    content.append("  if (window.location.hash) {")
    content.append("    setTimeout(handleHashNavigation, 100);")
    content.append("  }")
    content.append("})();")
    content.append("</script>")
    content.append("```")

    # Write file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(external_params)} external parameters")
    print(f"     {len(calculated_params)} calculated parameters")
    print(f"     {len(definition_params)} core definitions")
