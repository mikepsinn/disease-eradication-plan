#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variables YAML generation utilities for dih_models
===================================================

Generate _variables.yml from parameter metadata for Quarto.

Functions:
- generate_variables_yml() - Generate _variables.yml with formatted parameters

Usage:
    from dih_models.variables_yml_generator import generate_variables_yml
    from pathlib import Path

    # Generate variables YAML file
    output_path = Path("_variables.yml")
    generate_variables_yml(parameters, output_path, citation_mode="separate")
"""

from pathlib import Path
from typing import Any, Dict, Optional
import json

import yaml

from dih_models.latex_generation import generate_auto_latex
from dih_models.quarto_formatting import generate_html_with_tooltip
from dih_models.reference_parser import sanitize_bibtex_key
from dih_models.formatting import format_parameter_value


class ValueWithCI:
    """Wrapper to override display_value with confidence interval."""
    def __init__(self, original_value: Any, display_override: str):
        self._original = original_value
        self.display_value = display_override
        # Copy all attributes from original
        for attr in dir(original_value):
            if not attr.startswith('_') and attr != 'display_value':
                try:
                    setattr(self, attr, getattr(original_value, attr))
                except (AttributeError, TypeError):
                    pass

    def __float__(self) -> float:
        return float(self._original)


def generate_variables_yml(
    parameters: Dict[str, Dict[str, Any]],
    output_path: Path,
    citation_mode: str = "none",
    params_file: Optional[Path] = None,
    samples_json_path: Optional[Path] = None
):
    """
    Generate _variables.yml file from parameters.

    Creates YAML with lowercase variable names mapped to formatted HTML values.
    Also exports LaTeX equations as {param_name}_latex variables.

    For calculated parameters with Monte Carlo uncertainty (from samples.json),
    embeds 95% confidence intervals in the base variable value.

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write _variables.yml
        citation_mode: Citation handling mode:
            - "none": No inline citations (default)
            - "inline": Include [@key] after external peer-reviewed parameters
            - "separate": Export citation keys as {param_name}_cite variables
            - "both": Both inline AND separate variables
        params_file: Path to parameters.py for sympy-based LaTeX generation
        samples_json_path: Optional path to samples.json with Monte Carlo uncertainty data
    """
    variables = {}
    citation_count = 0

    # Load Monte Carlo uncertainty data if available
    uncertainty_data = {}
    if samples_json_path and samples_json_path.exists():
        with open(samples_json_path, "r", encoding="utf-8") as f:
            uncertainty_data = json.load(f)

    # Sort parameters by name for consistent output
    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data["value"]
        comment = param_data["comment"]

        # Use lowercase name for Quarto variables (convention)
        var_name = param_name.lower()

        # Check if this parameter has uncertainty data to embed in display value
        # Priority: 1) Specified confidence_interval on parameter, 2) Monte Carlo derived CI
        value_with_ci = value
        unit = getattr(value, "unit", None)
        central_value = float(value)

        # First, check if parameter has an explicitly specified confidence_interval
        # This is preferred as it represents the author's judgment about plausible ranges
        specified_ci = getattr(value, "confidence_interval", None)

        if specified_ci and len(specified_ci) == 2:
            ci_low, ci_high = specified_ci
            # Check if there's meaningful uncertainty in the specified CI
            has_meaningful_uncertainty = abs(ci_high - ci_low) > 0.001

            if has_meaningful_uncertainty:
                # Format central value WITH unit for cleaner display
                central_formatted = format_parameter_value(central_value, unit, include_unit=True)

                # Format CI bounds - for percentages, multiply by 100 and format as percent
                if unit == "percentage":
                    ci_low_formatted = f"{ci_low * 100:.0f}%"
                    ci_high_formatted = f"{ci_high * 100:.0f}%"
                else:
                    # Include units in CI bounds for clarity
                    ci_low_formatted = format_parameter_value(ci_low, unit, include_unit=True)
                    ci_high_formatted = format_parameter_value(ci_high, unit, include_unit=True)

                # Embed specified CI in display value: "184.6M deaths (95% CI: 150M deaths-220M deaths)"
                display_value_with_ci = f"{central_formatted} (95% CI: {ci_low_formatted}-{ci_high_formatted})"
                value_with_ci = ValueWithCI(value, display_value_with_ci)

        # Fall back to Monte Carlo derived CI if no specified CI
        elif param_name in uncertainty_data:
            unc = uncertainty_data[param_name]
            p5 = unc.get("p5")
            p50 = unc.get("p50")
            p95 = unc.get("p95")

            # Only embed CI if there's meaningful uncertainty
            # Skip if p5 == p95 (zero variance) or variance < 0.1% of median
            has_meaningful_uncertainty = False
            if p50 != 0:
                relative_variance = abs(p95 - p5) / abs(p50)
                has_meaningful_uncertainty = relative_variance > 0.001  # >0.1% variance
            else:
                has_meaningful_uncertainty = abs(p95 - p5) > 0

            if has_meaningful_uncertainty:
                # Always use deterministic baseline for consistency with tooltips, LaTeX, and parameter-summary.md
                # The confidence interval will still show Monte Carlo uncertainty range
                # Include units in all formatted values for cleaner display
                central_formatted = format_parameter_value(central_value, unit, include_unit=True)
                p5_formatted = format_parameter_value(p5, unit, include_unit=True)
                p95_formatted = format_parameter_value(p95, unit, include_unit=True)

                # Embed CI in display value: "184.6M deaths (95% CI: 150M deaths-220M deaths)"
                display_value_with_ci = f"{central_formatted} (95% CI: {p5_formatted}-{p95_formatted})"
                value_with_ci = ValueWithCI(value, display_value_with_ci)

        # Generate formatted HTML with tooltip
        include_inline_citation = citation_mode in ("inline", "both")
        html_value = generate_html_with_tooltip(param_name, value_with_ci, comment, include_citation=include_inline_citation)

        variables[var_name] = html_value

        # Export citation key separately for external sources (if mode enabled)
        if citation_mode in ("separate", "both"):
            if hasattr(value, "source_type") and hasattr(value, "source_ref"):
                source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
                if source_type_str == "external" and value.source_ref:
                    # Sanitize citation key for BibTeX compatibility
                    sanitized_ref = sanitize_bibtex_key(value.source_ref)
                    variables[f"{var_name}_cite"] = f"@{sanitized_ref}"
                    citation_count += 1

        # Export LaTeX equation: prefer hardcoded (hand-crafted with good labels),
        # fall back to auto-generated for params without hardcoded latex
        hardcoded_latex = getattr(value, "latex", None)
        auto_latex = generate_auto_latex(param_name, value, parameters, params_file=params_file)

        if hardcoded_latex:
            # Use hardcoded (preferred - hand-crafted with semantic labels)
            latex_var_name = f"{var_name}_latex"
            variables[latex_var_name] = f"$$\n{hardcoded_latex}\n$$"
        elif auto_latex:
            # Fall back to auto-generated for params without hardcoded
            latex_var_name = f"{var_name}_latex"
            variables[latex_var_name] = f"$$\n{auto_latex}\n$$"

    # Count exports by type BEFORE adding metadata variables
    latex_count = sum(1 for k in variables.keys() if k.endswith("_latex"))
    cite_count = sum(1 for k in variables.keys() if k.endswith("_cite"))
    param_count = len(variables) - latex_count - cite_count

    # Add metadata variables for use in QMD files
    variables["total_parameter_count"] = str(param_count)
    variables["total_latex_equation_count"] = str(latex_count)
    if citation_mode in ("separate", "both"):
        variables["total_citation_count"] = str(cite_count)

    # Write YAML file
    with open(output_path, "w", encoding="utf-8", newline='\n') as f:
        # Add header comment
        f.write("# AUTO-GENERATED FILE - DO NOT EDIT\n")
        f.write("# Generated from dih_models/parameters.py\n")
        f.write("# Run: python scripts/generate-everything-parameters-variables-calculations-references.py\n")
        f.write("#\n")
        f.write("# Use in QMD files with: {{< var param_name >}}\n")
        if citation_mode in ("separate", "both"):
            f.write("# Citations available as: {{< var param_name_cite >}}\n")
        f.write("#\n")
        f.write("# Metadata variables:\n")
        f.write("#   {{< var total_parameter_count >}} - Number of parameters\n")
        f.write("#   {{< var total_latex_equation_count >}} - Number of LaTeX equations\n")
        if citation_mode in ("separate", "both"):
            f.write("#   {{< var total_citation_count >}} - Number of citations\n")
        f.write("#\n\n")

        # Write variables with proper quoting for HTML
        yaml.dump(variables, f, default_flow_style=False, allow_unicode=True, sort_keys=False, default_style='"')

    print(f"[OK] Generated {output_path}")
    print(f"     {param_count} parameters exported")
    print(f"     {latex_count} LaTeX equations exported")
    if citation_mode in ("separate", "both"):
        print(f"     {cite_count} citation keys exported")
    if citation_mode in ("inline", "both"):
        print("     Citation mode: inline [@key] for peer-reviewed sources")
    print("\nUsage in QMD files:")
    print(f"  {{{{< var {list(variables.keys())[0]} >}}}}")
    if latex_count > 0:
        # Find first latex equation
        latex_var = next((k for k in variables.keys() if k.endswith("_latex")), None)
        if latex_var:
            print(f"  {{{{< var {latex_var} >}}}}  (equation)")
    if cite_count > 0:
        # Find first parameter with citation
        cite_var = next((k for k in variables.keys() if k.endswith("_cite")), None)
        if cite_var:
            base_var = cite_var[:-5]  # Remove "_cite"
            print(f"  {{{{< var {base_var} >}}}} {{{{< var {cite_var} >}}}}")
