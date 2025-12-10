#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quarto HTML and tooltip formatting utilities for dih_models
============================================================

Generate HTML tooltips, links, and uncertainty explanations for Quarto output.

Functions:
- convert_qmd_to_html() - Remove .qmd extension for format-agnostic links
- generate_html_with_tooltip() - Generate clickable parameter tooltips
- generate_uncertainty_section() - Generate human-friendly uncertainty explanations

Usage:
    from dih_models.quarto_formatting import generate_html_with_tooltip

    # Generate HTML with tooltip
    html = generate_html_with_tooltip(
        param_name="GLOBAL_MILITARY_SPENDING",
        value=parameter_instance,
        include_citation=True
    )

    # Generate uncertainty section for QMD
    uncertainty_lines = generate_uncertainty_section(parameter_instance, unit="USD")
"""

from typing import Any, Union

from dih_models.formatting import format_parameter_value


def convert_qmd_to_html(path: str) -> str:
    """
    Remove .qmd extension from paths for format-agnostic links.
    Quarto will resolve extensionless paths appropriately for each output format:
    - HTML: resolves to .html files
    - PDF: resolves to internal PDF references
    - EPUB: resolves to internal EPUB references

    Args:
        path: Path that may contain .qmd extension

    Returns:
        Path with .qmd extension removed (format-agnostic)
    """
    if path.endswith('.qmd'):
        return path[:-4]  # Remove .qmd extension
    elif '.qmd#' in path:
        # Handle paths with fragments like "file.qmd#section"
        return path.replace('.qmd#', '#')  # Remove .qmd, keep #
    return path


def generate_html_with_tooltip(param_name: str, value: Union[float, int, Any], comment: str = "", include_citation: bool = False) -> str:
    """
    Generate HTML link with tooltip for a parameter.

    Args:
        param_name: The parameter name (e.g., 'GLOBAL_ANNUAL_CONFLICT_DEATHS')
        value: The numeric value (may be Parameter instance with metadata)
        comment: Optional comment from parameters.py
        include_citation: If True, append Quarto citation [@key] for external sources

    Returns:
        HTML string with formatted value, clickable link, and tooltip
    """
    # Check for display_value override (NEW v2.0)
    unit = ""
    if hasattr(value, "unit") and value.unit:
        unit = value.unit

    if hasattr(value, "display_value") and value.display_value:
        formatted_value = value.display_value
    else:
        formatted_value = format_parameter_value(value, unit, include_unit=False)

    # Check if value is a Parameter instance with source metadata
    has_source = hasattr(value, "source_ref") and value.source_ref

    # Handle both enum and string source_type (backwards compatibility)
    source_type_str = ""
    if hasattr(value, "source_type"):
        source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)

    is_definition = source_type_str == "definition"

    if has_source:
        # Convert ReferenceID enum to string value
        source_ref_value = value.source_ref
        if hasattr(source_ref_value, 'value'):
            # It's an enum, get the actual string value
            source_ref_value = source_ref_value.value
        else:
            # Already a string
            source_ref_value = str(source_ref_value)

        # Determine link destination based on source type
        if source_type_str == "external":
            # Link to citation in references.html (full URL)
            href = f"https://warondisease.org/knowledge/references.html#{source_ref_value}"
            link_text = "View source citation"
        else:
            # Link to calculation/methodology page (ensure absolute path)
            if not source_ref_value.startswith("/"):
                source_ref_value = f"/{source_ref_value}"
            # Convert .qmd to .html for rendered output
            href = convert_qmd_to_html(source_ref_value)
            link_text = "View methodology & calculation"

        # Build tooltip from Parameter metadata with credibility indicators
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

        # Show input parameters if this is a calculated parameter
        if source_type_str == "calculated" and hasattr(value, "inputs") and value.inputs:
            num_inputs = len(value.inputs)
            tooltip_parts.append(f"Calculated from {num_inputs} input{'s' if num_inputs != 1 else ''}")

        # Add confidence level with emoji indicators
        if hasattr(value, "confidence") and value.confidence:
            confidence_indicators = {
                "high": "✓ High confidence",
                "medium": "~ Medium confidence",
                "low": "? Low confidence",
                "estimated": "≈ Estimated",
            }
            tooltip_parts.append(confidence_indicators.get(value.confidence, value.confidence))

        # Show if peer-reviewed (prestigious!)
        if hasattr(value, "peer_reviewed") and value.peer_reviewed:
            tooltip_parts.append("📊 Peer-reviewed")

        # Show if conservative estimate
        if hasattr(value, "conservative") and value.conservative:
            tooltip_parts.append("Conservative estimate")

        # Show sensitivity/uncertainty range
        if hasattr(value, "sensitivity") and value.sensitivity:
            sensitivity_str = format_parameter_value(value.sensitivity, unit)
            tooltip_parts.append(f"±{sensitivity_str}")

        # Show NEW uncertainty metadata (v2.0)
        if hasattr(value, "confidence_interval") and value.confidence_interval:
            low, high = value.confidence_interval
            low_str = format_parameter_value(low, unit)
            high_str = format_parameter_value(high, unit)
            tooltip_parts.append(f"95% CI: [{low_str}, {high_str}]")

        if hasattr(value, "distribution") and value.distribution:
            dist_name = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)
            dist_str = f"Dist: {dist_name.title()}"
            if hasattr(value, "std_error") and value.std_error:
                se_str = format_parameter_value(value.std_error, unit)
                dist_str += f" (SE: {se_str})"
            tooltip_parts.append(dist_str)

        # Show last updated date
        if hasattr(value, "last_updated") and value.last_updated:
            tooltip_parts.append(f"Updated: {value.last_updated}")

        if hasattr(value, "formula") and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")
        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")
        tooltip_parts.append(f"Click to {link_text.lower()}")

        tooltip = " | ".join(tooltip_parts)

        # Build data attributes for CSS/JS customization
        data_attrs = f'data-source-ref="{source_ref_value}" data-source-type="{source_type_str}"'
        if hasattr(value, "peer_reviewed") and value.peer_reviewed:
            data_attrs += ' data-peer-reviewed="true"'
        if hasattr(value, "confidence") and value.confidence:
            data_attrs += f' data-confidence="{value.confidence}"'

        # Generate clickable link with optional inline citation
        html = f'<a href="{href}" class="parameter-link" {data_attrs} title="{tooltip}">{formatted_value}</a>'

        # Add Quarto citation inline for external peer-reviewed sources (if requested)
        if include_citation and source_type_str == "external":
            if hasattr(value, "peer_reviewed") and value.peer_reviewed:
                html += f' [@{source_ref_value}]'
    elif is_definition:
        # Core definition: show value with tooltip but no link
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)
        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")
        tooltip_parts.append("Core definition")

        tooltip = " | ".join(tooltip_parts)

        html = f'<span class="parameter-definition" title="{tooltip}">{formatted_value}</span>'
    elif source_type_str == "calculated":
        # Calculated parameter without source_ref: link to parameters-and-calculations.qmd
        # Auto-link to the generated section in parameters-and-calculations.qmd
        # Use absolute path for consistency with other calculated parameters
        href = f"/knowledge/appendix/parameters-and-calculations#sec-{param_name.lower()}"

        # Build tooltip from available metadata
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

        if hasattr(value, "formula") and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")

        # Show input parameters if available
        if hasattr(value, "inputs") and value.inputs:
            num_inputs = len(value.inputs)
            tooltip_parts.append(f"Calculated from {num_inputs} input{'s' if num_inputs != 1 else ''}")

        if hasattr(value, "confidence") and value.confidence:
            confidence_indicators = {
                "high": "✓ High confidence",
                "medium": "~ Medium confidence",
                "low": "? Low confidence",
                "estimated": "≈ Estimated",
            }
            tooltip_parts.append(confidence_indicators.get(value.confidence, value.confidence))

        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")

        # More informative call-to-action
        tooltip_parts.append("Click for equation, sensitivity analysis & Monte Carlo distribution")
        tooltip = " | ".join(tooltip_parts)

        # Build data attributes
        data_attrs = f'data-source-type="calculated"'
        if hasattr(value, "confidence") and value.confidence:
            data_attrs += f' data-confidence="{value.confidence}"'

        html = f'<a href="{href}" class="parameter-link" {data_attrs} title="{tooltip}">{formatted_value}</a>'
    else:
        # Fallback: truly bare parameter with no metadata
        # Build best tooltip we can from available info
        tooltip_parts = []

        # Try to extract description from Parameter object
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

        # Show formula if available
        if hasattr(value, "formula") and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")

        # Show unit if available
        if hasattr(value, "unit") and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")

        # Add comment from source code if we have it
        if comment:
            tooltip_parts.append(comment)

        # Only fall back to param name if we have NOTHING else
        if not tooltip_parts:
            tooltip_parts.append(f"Parameter: {param_name}")

        tooltip = " | ".join(tooltip_parts)
        html = f'<span class="parameter-link" title="{tooltip}">{formatted_value}</span>'

    return html


def generate_uncertainty_section(value: Any, unit: str = "") -> list[str]:
    """
    Generate human-friendly uncertainty explanation for a parameter.

    Returns both technical notation (for economists) and plain-language
    explanations (for general readers).

    Args:
        value: Parameter instance with uncertainty metadata
        unit: Unit string for formatting

    Returns:
        List of content lines to append to the QMD
    """
    content = []

    # Check if we have any uncertainty metadata
    has_ci = hasattr(value, "confidence_interval") and value.confidence_interval
    has_dist = hasattr(value, "distribution") and value.distribution
    has_se = hasattr(value, "std_error") and value.std_error
    has_sensitivity = hasattr(value, "sensitivity") and value.sensitivity

    if not (has_ci or has_dist or has_se or has_sensitivity):
        return content

    content.append("#### Uncertainty Range")
    content.append("")

    # Technical notation line
    technical_parts = []

    if has_ci:
        low, high = value.confidence_interval
        low_str = format_parameter_value(low, unit)
        high_str = format_parameter_value(high, unit)
        technical_parts.append(f"95% CI: [{low_str}, {high_str}]")

    if has_dist:
        dist_name = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)
        dist_str = dist_name.title()
        if has_se:
            se_str = format_parameter_value(value.std_error, unit)
            dist_str += f" (SE: {se_str})"
        technical_parts.append(f"Distribution: {dist_str}")

    if has_sensitivity and not has_ci:
        sens_str = format_parameter_value(value.sensitivity, unit)
        technical_parts.append(f"Sensitivity: ±{sens_str}")

    if technical_parts:
        content.append("**Technical**: " + " • ".join(technical_parts))
        content.append("")

    # Human-friendly explanation
    main_value = float(value)

    if has_ci:
        low, high = value.confidence_interval

        # Calculate percentage range from central value
        low_pct = abs((main_value - low) / main_value * 100) if main_value != 0 else 0
        high_pct = abs((high - main_value) / main_value * 100) if main_value != 0 else 0
        avg_pct = (low_pct + high_pct) / 2

        # Format the bounds nicely
        low_str = format_parameter_value(low, unit)
        high_str = format_parameter_value(high, unit)

        # Generate plain-language explanation based on uncertainty size
        if avg_pct <= 10:
            certainty_phrase = "We're quite confident in this estimate"
            range_desc = "a narrow range"
        elif avg_pct <= 25:
            certainty_phrase = "This estimate has moderate uncertainty"
            range_desc = "a reasonable range"
        elif avg_pct <= 50:
            certainty_phrase = "There's significant uncertainty here"
            range_desc = "a wide range"
        else:
            certainty_phrase = "This estimate is highly uncertain"
            range_desc = "a very wide range"

        content.append(f"**What this means**: {certainty_phrase}. The true value likely falls between {low_str} and {high_str} (±{avg_pct:.0f}%). This represents {range_desc} that our Monte Carlo simulations account for when calculating overall uncertainty in the results.")
        content.append("")

        # Add distribution explanation if present
        if has_dist:
            dist_name = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)

            dist_explanations = {
                "normal": "values cluster around the center with equal chances of being higher or lower",
                "lognormal": "values can't go negative and have a longer tail toward higher values (common for costs and populations)",
                "uniform": "any value in the range is equally likely",
                "triangular": "values cluster around a most-likely point but can range higher or lower",
                "beta": "values are bounded and can skew toward one end",
                "pert": "values cluster around a most-likely estimate with defined min/max bounds",
            }

            explanation = dist_explanations.get(dist_name.lower(), "values follow a specific statistical pattern")
            content.append(f"*The {dist_name.lower()} distribution means {explanation}.*")
            content.append("")

    elif has_sensitivity:
        sens = value.sensitivity
        sens_str = format_parameter_value(sens, unit)
        sens_pct = abs(sens / main_value * 100) if main_value != 0 else 0

        content.append(f"**What this means**: This value could reasonably vary by ±{sens_str} (±{sens_pct:.0f}%) based on different assumptions or data sources.")
        content.append("")

    return content
