#!/usr/bin/env python3
# type: ignore
"""
Generate _variables.yml and academic outputs from parameters.py
================================================================

Reads all numeric constants from dih_models/parameters.py and generates:
1. _variables.yml - Quarto-compatible variables with tooltips
2. knowledge/appendix/parameters-and-calculations.qmd - Academic reference with LaTeX
3. knowledge/references.json - Structured JSON from references.qmd
4. references.bib - BibTeX export for LaTeX submissions
5. (Optional) Inject citations into economics.qmd

Usage:
    python scripts/generate-variables-yml.py [options]

Options:
    --cite-mode=MODE      Citation handling mode:
                          - none: No inline citations (default)
                          - inline: Add [@key] after peer-reviewed parameters
                          - separate: Export {param}_cite variables
                          - both: Both inline AND separate variables

    --inject-citations    Add [@citation] tags to economics.qmd variables
                          (legacy option, use --cite-mode=inline instead)

Examples:
    # Default: no citations
    python scripts/generate-variables-yml.py

    # Inline citations for peer-reviewed sources
    python scripts/generate-variables-yml.py --cite-mode=inline

    # Separate citation variables (flexible usage)
    python scripts/generate-variables-yml.py --cite-mode=separate

    # Both inline AND separate (maximum flexibility)
    python scripts/generate-variables-yml.py --cite-mode=both

Output:
    _variables.yml in project root
    knowledge/appendix/parameters-and-calculations.qmd
    references.bib in project root

The generated files enable academic rigor with zero manual maintenance.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Union

import yaml

# Add scripts directory to path for local imports
_scripts_dir = Path(__file__).parent.absolute()
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from generate_references_json import generate_references_json  # noqa: E402
from chart_generators import (
    generate_tornado_chart_qmd,
    generate_sensitivity_table_qmd,
    generate_input_distribution_chart_qmd,
    generate_monte_carlo_distribution_chart_qmd,
    generate_cdf_chart_qmd,
)
# Delayed imports to allow reference_ids.py regeneration
# from dih_models.parameters import format_parameter_value
from dih_models.formatting import format_parameter_value
from dih_models.latex_generation import (
    generate_auto_latex,
    format_latex_value,
    create_latex_variable_name,
    create_short_label,
    infer_operation_from_compute,
    extract_lambda_body_from_file,
    lambda_to_sympy_latex,
    smart_title_case,
)
from dih_models.reference_parser import (
    parse_references_qmd_detailed,
    parse_references_qmd,
    sanitize_bibtex_key,
)
from dih_models.validation import (
    validate_references,
    validate_calculated_parameters,
    validate_calculated_params_no_uncertainty,
    validate_formula_uses_full_param_names,
    validate_compute_inputs_match,
    validate_inline_calculations_have_compute,
)

# Delayed imports placeholders
simulate = None
one_at_a_time_sensitivity = None
tornado_deltas = None
regression_sensitivity = None
Outcome = None


def init_uncertainty():
    """
    Initialize uncertainty module imports.
    Must be called AFTER generate_reference_ids_enum has run.
    """
    global simulate, one_at_a_time_sensitivity, tornado_deltas, regression_sensitivity, Outcome
    try:
        from dih_models.uncertainty import (
            simulate as _sim, 
            one_at_a_time_sensitivity as _oaat, 
            tornado_deltas as _td, 
            regression_sensitivity as _rs, 
            Outcome as _Out
        )
        simulate = _sim
        one_at_a_time_sensitivity = _oaat
        tornado_deltas = _td
        regression_sensitivity = _rs
        Outcome = _Out
    except ImportError:
        pass
    except Exception as e:
        print(f"[WARN] Failed to load uncertainty module: {e}")


def parse_parameters_file(parameters_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse parameters.py and extract all numeric constants with metadata.

    Imports the actual module to get Parameter instances with their metadata.

    Returns a dict mapping variable names to their metadata:
    {
        'PARAM_NAME': {
            'value': Parameter(123.45, ...) or 123.45,
            'line_num': 42,
            'comment': '# Source: https://...'
        }
    }
    """
    parameters = {}

    # Import the parameters module to get actual Parameter instances
    import importlib.util

    # Add dih_models directory to sys.path so it can find reference_ids
    dih_models_dir = str(parameters_path.parent)
    if dih_models_dir not in sys.path:
        sys.path.insert(0, dih_models_dir)

    spec = importlib.util.spec_from_file_location("parameters", parameters_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {parameters_path}")
    params_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params_module)

    # Also parse the file for line numbers and comments
    with open(parameters_path, encoding="utf-8") as f:
        lines = f.readlines()

    line_info = {}
    for i, line in enumerate(lines, 1):
        # Skip comments and empty lines
        if line.strip().startswith("#") or not line.strip():
            continue

        # Look for variable assignments
        match = re.match(r"^([A-Z_][A-Z0-9_]*)\s*=\s*", line.strip())
        if match:
            var_name = match.group(1)
            # Extract comment if present
            comment = ""
            if "#" in line:
                comment = line.split("#", 1)[1].strip()
            line_info[var_name] = {"line_num": i, "comment": comment}

    # Extract all uppercase constants from the module
    for name in dir(params_module):
        if name.isupper():  # Only uppercase constants
            value = getattr(params_module, name)

            # Only process numeric values (including Parameter instances)
            if isinstance(value, (int, float)):
                info = line_info.get(name, {"line_num": 0, "comment": ""})
                parameters[name] = {
                    "value": value,  # This will be Parameter instance if defined as such
                    "line_num": info["line_num"],
                    "comment": info["comment"],
                }

    return parameters



# LaTeX generation functions moved to dih_models/latex_generation.py
# (smart_title_case, infer_operation_from_compute, extract_lambda_body_from_file,
#  lambda_to_sympy_latex, generate_auto_latex, format_latex_value,
#  create_short_label, create_latex_variable_name)


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


def generate_variables_yml(parameters: Dict[str, Dict[str, Any]], output_path: Path, citation_mode: str = "none", params_file: Path = None):
    """
    Generate _variables.yml file from parameters.

    Creates YAML with lowercase variable names mapped to formatted HTML values.
    Also exports LaTeX equations as {param_name}_latex variables.

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write _variables.yml
        citation_mode: Citation handling mode:
            - "none": No inline citations (default)
            - "inline": Include [@key] after external peer-reviewed parameters
            - "separate": Export citation keys as {param_name}_cite variables
            - "both": Both inline AND separate variables
        params_file: Path to parameters.py for sympy-based LaTeX generation
    """
    variables = {}
    citation_count = 0

    # Sort parameters by name for consistent output
    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data["value"]
        comment = param_data["comment"]

        # Use lowercase name for Quarto variables (convention)
        var_name = param_name.lower()

        # Generate formatted HTML with tooltip
        include_inline_citation = citation_mode in ("inline", "both")
        html_value = generate_html_with_tooltip(param_name, value, comment, include_citation=include_inline_citation)

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
    with open(output_path, "w", encoding="utf-8") as f:
        # Add header comment
        f.write("# AUTO-GENERATED FILE - DO NOT EDIT\n")
        f.write("# Generated from dih_models/parameters.py\n")
        f.write("# Run: python tools/generate-variables-yml.py\n")
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


def generate_parameters_qmd(parameters: Dict[str, Dict[str, Any]], output_path: Path, available_refs: set = None, params_file: Path = None):
    """
    Generate comprehensive parameters-and-calculations.qmd appendix.

    Creates an academic reference page with:
    - All parameters organized by type (external/calculated)
    - LaTeX equations where available (hardcoded or auto-generated)
    - Citations and source links
    - Confidence indicators and metadata
    - Uncertainty ranges with human-friendly explanations

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write the QMD file
        available_refs: Set of valid reference IDs from references.qmd (optional, for detecting reference links)
        params_file: Path to parameters.py (for auto-generating latex equations)
    """
    # Categorize parameters
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

    # Calculated parameters section (moved first)
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

            # Show input parameters with links (NEW)
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
                        source_ref = "../" + source_ref[len("knowledge/") :]

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
            project_root / "_analysis" / f"tornado_{param_name}.json"
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
            
            # Generate sensitivity table if needed (dynamic generation)
            # Find input parameters via compute function or inputs list
            if hasattr(value, "inputs") and value.inputs and hasattr(value, "compute"):
                # We need to calculate sensitivity indices (regression coefficients)
                # This requires the dih_models.uncertainty module
                if regression_sensitivity and hasattr(value, "distribution"):
                     # This is logically where we would generate the table
                     # For now, we are relying on pre-calculated sensitivity files or on-demand generation elsewhere
                     pass

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


# Reference parsing and validation functions moved to dih_models/
# - parse_references_qmd_detailed() -> dih_models.reference_parser
# - parse_references_qmd() -> dih_models.reference_parser
# - sanitize_bibtex_key() -> dih_models.reference_parser
# - validate_references() -> dih_models.validation
# - validate_calculated_parameters() -> dih_models.validation
# - validate_calculated_params_no_uncertainty() -> dih_models.validation
# - validate_formula_uses_full_param_names() -> dih_models.validation
# - validate_compute_inputs_match() -> dih_models.validation
# - validate_inline_calculations_have_compute() -> dih_models.validation


def generate_reference_ids_enum(available_refs: set, output_path: Path):
    """
    Generate dih_models/reference_ids.py with enum of valid reference IDs.

    Creates a Python enum for IDE autocomplete and static type checking.
    Developers can use ReferenceID.CDC_LEADING_CAUSES_DEATH instead of strings.

    Args:
        available_refs: Set of reference IDs from references.qmd
        output_path: Path to write reference_ids.py
    """
    content = []
    content.append("#!/usr/bin/env python3")
    content.append('"""')
    content.append("AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("=" * 70)
    content.append("")
    content.append("Valid reference IDs extracted from knowledge/references.qmd")
    content.append("")
    content.append("Usage in parameters.py:")
    content.append("    from .reference_ids import ReferenceID")
    content.append("")
    content.append("    PARAM = Parameter(")
    content.append("        123.45,")
    content.append('        source_type="external",')
    content.append("        source_ref=ReferenceID.CDC_LEADING_CAUSES_DEATH,")
    content.append('        description="..."')
    content.append("    )")
    content.append("")
    content.append("Benefits:")
    content.append("  - IDE autocomplete shows all valid reference IDs")
    content.append("  - Static type checking catches typos before runtime")
    content.append("  - Refactoring safety when renaming references")
    content.append('"""')
    content.append("")
    content.append("from enum import Enum")
    content.append("")
    content.append("")
    content.append("class ReferenceID(str, Enum):")
    content.append('    """Valid reference IDs from knowledge/references.qmd"""')
    content.append("")

    # Sort reference IDs for consistent output
    sorted_refs = sorted(available_refs)

    # Convert reference IDs to enum member names
    # e.g., "cdc-leading-causes-death" -> "CDC_LEADING_CAUSES_DEATH"
    # e.g., "95-pct-diseases-no-treatment" -> "N95_PCT_DISEASES_NO_TREATMENT"
    for ref_id in sorted_refs:
        # Convert kebab-case to SCREAMING_SNAKE_CASE
        enum_name = ref_id.upper().replace("-", "_")

        # Handle special cases that start with numbers: prefix with 'N' instead of '_'
        # This avoids Python's protected member convention (_var)
        if enum_name[0].isdigit():
            enum_name = f"N{enum_name}"

        content.append(f'    {enum_name} = "{ref_id}"')

    content.append("")

    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(sorted_refs)} reference IDs exported as enum")
    print()
    print("Usage in parameters.py:")
    print("    from .reference_ids import ReferenceID")
    if sorted_refs:
        first_ref = sorted_refs[0].upper().replace("-", "_")
        if first_ref[0].isdigit():
            first_ref = f"N{first_ref}"
        print(f"    source_ref=ReferenceID.{first_ref}")
    print()


def generate_bibtex(parameters: Dict[str, Dict[str, Any]], output_path: Path, available_refs: set = None, references_path: Path = None):
    """
    Generate references.bib BibTeX file from external parameters.

    Extracts unique citations from parameters with source_type="external"
    and creates BibTeX entries using actual citation data from references.qmd.

    Args:
        parameters: Dict of parameter metadata
        output_path: Path to write references.bib
        available_refs: Set of valid reference IDs from references.qmd (optional)
        references_path: Path to references.qmd file for detailed citation data
    """
    # Parse detailed citation data from references.qmd
    citation_data = {}
    if references_path and references_path.exists():
        citation_data = parse_references_qmd_detailed(references_path)

    # Collect unique source_refs from external parameters
    citations = set()
    for param_name, param_data in parameters.items():
        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "external":
                if hasattr(value, "source_ref") and value.source_ref:
                    # Convert ReferenceID enum to string value
                    source_ref = value.source_ref
                    if hasattr(source_ref, 'value'):
                        # It's an enum, get the actual string value
                        source_ref = source_ref.value
                    else:
                        # It's already a string
                        source_ref = str(source_ref)

                    # Skip internal document references (contain / or .qmd)
                    if '/' in source_ref or '.qmd' in source_ref:
                        continue

                    # Optionally skip missing references
                    if available_refs and source_ref not in available_refs:
                        continue

                    citations.add(source_ref)

    # Generate BibTeX entries
    content = []
    content.append("% AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("% Generated from dih_models/parameters.py and knowledge/references.qmd")
    content.append("")
    content.append("% This file contains BibTeX references for all external data sources")
    content.append("% used in the economic analysis of a 1% treaty and decentralized framework for drug assessment.")
    content.append("")
    content.append("% Extracted from knowledge/references.qmd with author, year, source, and URL data.")
    content.append("% For manual curation or DOI-based enrichment, see references.qmd")
    content.append("")

    entries_with_data = 0
    entries_placeholder = 0

    for citation_key in sorted(citations):
        # Sanitize citation key for BibTeX (remove /, #, etc.)
        sanitized_key = sanitize_bibtex_key(citation_key)

        # Get detailed citation data if available
        ref_data = citation_data.get(citation_key, {})

        if ref_data and ref_data.get('title'):
            # Create proper BibTeX entry with real data
            entry_type = ref_data.get('type', 'misc')
            title = ref_data.get('title', citation_key)
            author = ref_data.get('author', '')
            year = ref_data.get('year', 'n.d.')
            source = ref_data.get('source', '')
            url = ref_data.get('url', '')
            note = ref_data.get('note', '')

            # Build BibTeX entry
            content.append(f"@{entry_type}{{{sanitized_key},")

            # Title (required for all types)
            # Escape special LaTeX characters
            title_escaped = title.replace('&', '\\&').replace('%', '\\%')
            content.append(f"  title = {{{title_escaped}}},")

            # Author/organization
            if author:
                author_escaped = author.replace('&', '\\&')
                if entry_type in ['report', 'techreport', 'legislation']:
                    content.append(f"  institution = {{{author_escaped}}},")
                else:
                    content.append(f"  author = {{{author_escaped}}},")

            # Year
            content.append(f"  year = {{{year}}},")

            # Source/journal/publisher
            if source:
                source_escaped = source.replace('&', '\\&')
                if entry_type == 'article':
                    content.append(f"  journal = {{{source_escaped}}},")
                elif entry_type in ['book', 'report', 'techreport']:
                    content.append(f"  publisher = {{{source_escaped}}},")

            # URL (with proper escaping)
            if url:
                url_escaped = url.replace('&', '\\&').replace('%', '\\%')
                content.append(f"  url = {{{url_escaped}}},")
                content.append("  urldate = {2025-01-20},")

            # Note (additional context)
            if note:
                note_escaped = note.replace('&', '\\&').replace('%', '\\%')
                # Truncate if too long
                if len(note_escaped) > 200:
                    note_escaped = note_escaped[:197] + "..."
                content.append(f"  note = {{{note_escaped}}},")

            content.append("}")
            content.append("")
            entries_with_data += 1

        else:
            # Fallback: create minimal placeholder entry
            content.append(f"@misc{{{sanitized_key},")
            content.append(f"  title = {{{citation_key}}},")
            content.append(f"  note = {{See https://warondisease.org/knowledge/references.html\\#{citation_key}}},")
            content.append(f"  url = {{https://warondisease.org/knowledge/references.html\\#{citation_key}}},")
            content.append("}")
            content.append("")
            entries_placeholder += 1

    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(citations)} unique citations")
    print(f"     {entries_with_data} with full citation data")
    if entries_placeholder > 0:
        print(f"     {entries_placeholder} placeholder entries (missing data in references.qmd)")


def inject_citations_into_qmd(parameters: Dict[str, Dict[str, Any]], qmd_path: Path):
    """
    Inject [@citation] tags into economics.qmd after variables with external sources.

    Finds {{< var param_name >}} patterns and adds [@source_ref] citations for
    parameters with source_type="external" and peer_reviewed=True.

    This is OPTIONAL and only runs when --inject-citations flag is used.
    """
    if not qmd_path.exists():
        print(f"[WARN] QMD file not found: {qmd_path}")
        return

    # Read file
    with open(qmd_path, encoding="utf-8") as f:
        content = f.read()

    # Build lookup map: param_name (lowercase) -> citation_key
    citation_map = {}
    for param_name, param_data in parameters.items():
        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "external":
                if hasattr(value, "peer_reviewed") and value.peer_reviewed:
                    if hasattr(value, "source_ref") and value.source_ref:
                        # Use lowercase param name (matches Quarto variable names)
                        citation_map[param_name.lower()] = value.source_ref

    # Pattern to match {{< var param_name >}}
    # We'll inject [@citation] right after if not already present
    def replace_var(match):
        var_name = match.group(1)
        full_match = match.group(0)

        # Check if citation already present after this variable
        # Look ahead to see if [@...] immediately follows
        remaining = content[match.end() :]
        if remaining.lstrip().startswith("[@"):
            return full_match  # Already has citation

        # Check if this variable should have a citation
        if var_name in citation_map:
            citation_key = citation_map[var_name]
            return f"{full_match} [@{citation_key}]"
        else:
            return full_match

    # Replace all variables
    pattern = r"\{\{<\s*var\s+([a-z_][a-z0-9_]*)\s*>\}\}"
    modified_content = re.sub(pattern, replace_var, content)

    # Count changes
    changes = sum(1 for a, b in zip(content, modified_content) if a != b)
    if changes > 0:
        # Write back
        with open(qmd_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

        print(f"[OK] Injected citations into {qmd_path}")
        print(f"     {len(citation_map)} parameters with citations available")
        print(f"     Modified {changes} characters")
    else:
        print("[OK] No citation injection needed (already present or no external params)")


# Chart generation functions moved to scripts/chart_generators.py
# - generate_tornado_chart_qmd() -> chart_generators
# - generate_sensitivity_table_qmd() -> chart_generators
# - generate_input_distribution_chart_qmd() -> chart_generators
# - generate_monte_carlo_distribution_chart_qmd() -> chart_generators
# - generate_cdf_chart_qmd() -> chart_generators


def main():
    # Parse command-line arguments
    inject_citations = "--inject-citations" in sys.argv

    # Citation mode: --cite-mode=inline|separate|both|none
    citation_mode = "separate"  # Default: always generate _cite variables for convenience
    for arg in sys.argv:
        if arg.startswith("--cite-mode="):
            citation_mode = arg.split("=")[1]
            if citation_mode not in ("none", "inline", "separate", "both"):
                print(f"[ERROR] Invalid citation mode: {citation_mode}", file=sys.stderr)
                print("Valid modes: none, inline, separate, both", file=sys.stderr)
                sys.exit(1)

    # Get project root
    project_root = Path(__file__).parent.parent.absolute()

    # Parse references.qmd FIRST (before parameters.py, to avoid circular dependency)
    print("[*] Parsing knowledge/references.qmd...")
    references_path = project_root / "knowledge" / "references.qmd"
    available_refs = parse_references_qmd(references_path)
    print(f"[OK] Found {len(available_refs)} reference entries")
    print()

    # Generate references.json from references.qmd
    print("[*] Generating knowledge/references.json...")
    references_json_path = project_root / "knowledge" / "references.json"
    generate_references_json(references_path, references_json_path)
    print()

    # Generate reference_ids.py enum SECOND (before loading parameters.py which imports it)
    print("[*] Generating dih_models/reference_ids.py...")
    reference_ids_path = project_root / "dih_models" / "reference_ids.py"
    generate_reference_ids_enum(available_refs, reference_ids_path)

    # Initialize uncertainty module now that dependencies are ready
    init_uncertainty()

    # Parse parameters file THIRD (now reference_ids.py is up to date)
    parameters_path = project_root / "dih_models" / "parameters.py"
    if not parameters_path.exists():
        print(f"[ERROR] Parameters file not found: {parameters_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Parsing {parameters_path}...")
    parameters = parse_parameters_file(parameters_path)
    print(f"[OK] Found {len(parameters)} numeric parameters")
    print()

    # Track fatal validation errors
    has_fatal_error = False

    # Validate that all external source_refs exist in references.qmd
    print("[*] Validating external source references...")
    missing_refs, used_refs = validate_references(parameters, available_refs)

    if missing_refs:
        print(f"[ERROR] Found {len(missing_refs)} missing references:", file=sys.stderr)
        for param_name, source_ref in missing_refs:
            print(f"  - Parameter '{param_name}' references missing citation: '{source_ref}'", file=sys.stderr)
        print(f"\n[ERROR] Please add missing references to {references_path}", file=sys.stderr)
        print(f"[ERROR] Format: <a id=\"{missing_refs[0][1]}\"></a>", file=sys.stderr)
        print()
        # Mark as fatal error so we exit with code 1 at the end
        has_fatal_error = True
    else:
        print(f"[OK] All {len(set(used_refs))} external references validated")
        print()

    # Validate calculated parameters have formulas
    print("[*] Validating calculated parameters...")
    suspicious_params = validate_calculated_parameters(parameters)

    if suspicious_params:
        print(f"[ERROR] Found {len(suspicious_params)} calculated parameters without formula/latex:", file=sys.stderr)
        for param_name, value in suspicious_params[:10]:  # Show first 10
            print(f"  - {param_name} = {value:,.2f} (marked as calculated but no formula)", file=sys.stderr)
        if len(suspicious_params) > 10:
            print(f"  ... and {len(suspicious_params) - 10} more", file=sys.stderr)
        print(file=sys.stderr)
        print("[ERROR] Calculated parameters MUST have 'formula' or 'latex' attributes.", file=sys.stderr)
        print("[ERROR] If these are intentional estimates, change source_type to 'definition'.", file=sys.stderr)
        has_fatal_error = True
        print()
    else:
        print("[OK] All calculated parameters have formulas or latex equations")
        print()

    # Validate calculated parameters don't have their own uncertainty (should derive from inputs)
    print("[*] Validating uncertainty is only on input parameters...")
    uncertainty_problems = validate_calculated_params_no_uncertainty(parameters)

    if uncertainty_problems:
        print(f"[ERROR] Found {len(uncertainty_problems)} calculated parameters with their own uncertainty:", file=sys.stderr)
        for param_name, issues in uncertainty_problems:
            print(f"  - {param_name} has: {', '.join(issues)}", file=sys.stderr)
        print(file=sys.stderr)
        print("[ERROR] Calculated parameters should derive uncertainty from inputs via compute function.", file=sys.stderr)
        print("[ERROR] Remove confidence_interval/distribution/std_error from these calculated parameters.", file=sys.stderr)
        print("[ERROR] Add uncertainty to their INPUT parameters instead.", file=sys.stderr)
        has_fatal_error = True
        print()
    else:
        print("[OK] All calculated parameters derive uncertainty from inputs")
        print()

    # Validate formula strings use full parameter names (informational only)
    # Note: LaTeX auto-generation now infers operation from compute(), so formula is optional
    print("[*] Checking formula strings (informational)...")
    formula_mismatches = validate_formula_uses_full_param_names(parameters)

    if formula_mismatches:
        print(f"[INFO] {len(formula_mismatches)} formulas use abbreviated names (this is OK - operation inferred from compute)")
        # Only show details if there are few
        if len(formula_mismatches) <= 5:
            for param_name, missing_input, formula in formula_mismatches:
                print(f"       {param_name}: \"{formula}\"")
        print()
    else:
        print("[OK] All formulas use full parameter names")
        print()

    # Validate compute functions match inputs list
    print("[*] Validating compute functions match inputs list...")
    compute_issues = validate_compute_inputs_match(parameters, parameters_path)

    if compute_issues:
        missing_issues = [(p, v) for p, t, v in compute_issues if t == 'missing_from_inputs']
        extra_issues = [(p, v) for p, t, v in compute_issues if t == 'extra_in_inputs']

        if missing_issues:
            print(f"[ERROR] {len(missing_issues)} parameters use ctx[] vars not in inputs list:", file=sys.stderr)
            for param_name, missing_vars in missing_issues[:10]:
                print(f"  - {param_name}: missing {missing_vars}", file=sys.stderr)
            if len(missing_issues) > 10:
                print(f"  ... and {len(missing_issues) - 10} more", file=sys.stderr)
            print(file=sys.stderr)
            print("[ERROR] Add these to the 'inputs' list for proper uncertainty propagation.", file=sys.stderr)
            has_fatal_error = True

        if extra_issues:
            print(f"[WARN] {len(extra_issues)} parameters have unused inputs (not fatal):")
            for param_name, extra_vars in extra_issues[:5]:
                print(f"  - {param_name}: unused {extra_vars}")
        print()
    else:
        print("[OK] All compute functions match their inputs list")
        print()

    # Validate inline calculations have inputs/compute metadata
    print("[*] Checking for inline calculations missing inputs/compute...")
    inline_issues = validate_inline_calculations_have_compute(parameters, parameters_path)

    if inline_issues:
        print(f"[ERROR] {len(inline_issues)} parameters have inline calculations but no inputs/compute:", file=sys.stderr)
        for param_name, first_arg in inline_issues[:10]:
            print(f"  - {param_name}: {first_arg}...", file=sys.stderr)
        if len(inline_issues) > 10:
            print(f"  ... and {len(inline_issues) - 10} more", file=sys.stderr)
        print(file=sys.stderr)
        print("[ERROR] Add 'inputs' and 'compute' to these parameters for uncertainty propagation.", file=sys.stderr)
        has_fatal_error = True
        print()
    else:
        print("[OK] All inline calculations have inputs/compute metadata")
        print()

    # Exit early if validation errors found
    if has_fatal_error:
        print("[FATAL] Validation errors found. Fix the issues above before continuing.", file=sys.stderr)
        sys.exit(1)

    # Generate _variables.yml
    print(f"[*] Generating _variables.yml (citation mode: {citation_mode})...")
    output_path = project_root / "_variables.yml"
    generate_variables_yml(parameters, output_path, citation_mode=citation_mode, params_file=parameters_path)
    print()

    # Generate references.bib (with full citation data from references.qmd)
    print("[*] Generating references.bib...")
    bib_output = project_root / "references.bib"
    generate_bibtex(parameters, bib_output, available_refs=available_refs, references_path=references_path)
    print()

    # Always generate uncertainty outputs when module is available
    try:
        if simulate is not None:
            print("[*] Generating uncertainty summaries...")
            # Choose a target calculated parameter if any
            target = next((name for name, meta in parameters.items()
                           if hasattr(meta.get("value"), "formula") and meta.get("value").formula), None)
            # Summaries directory
            analysis_dir = project_root / "_analysis"

            # Clean up stale analysis files before regenerating
            # This handles deleted/renamed parameters that would leave orphan files
            if analysis_dir.exists():
                import shutil
                stale_count = len(list(analysis_dir.glob("*.json")))
                if stale_count > 0:
                    print(f"[*] Cleaning {stale_count} stale analysis files...")
                    shutil.rmtree(analysis_dir)

            analysis_dir.mkdir(exist_ok=True)
            # Minimal inline summary generation to avoid duplicating logic
            from dih_models.uncertainty import simulate_with_propagation as _sim, one_at_a_time_sensitivity as _sens
            # Use fixed seed for reproducibility (avoids git churn from random variation)
            RANDOM_SEED = 42
            sims = _sim(parameters, n=10000, seed=RANDOM_SEED)
            import json
            try:
                import numpy as np
            except Exception:
                np = None  # type: ignore
            summaries = {}
            for name, arr in sims.items():
                if np is not None:
                    a = np.asarray(arr)
                    summaries[name] = {
                        "mean": float(np.mean(a)),
                        "std": float(np.std(a)),
                        "p5": float(np.percentile(a, 5)),
                        "p50": float(np.percentile(a, 50)),
                        "p95": float(np.percentile(a, 95)),
                    }
                else:
                    vals = list(arr)
                    m = sum(vals) / len(vals)
                    var = sum((v - m) ** 2 for v in vals) / len(vals)
                    std = var ** 0.5
                    vals_sorted = sorted(vals)

                    def pct(p: float):
                        i = int(p / 100 * (len(vals_sorted) - 1))
                        return vals_sorted[i]
                    summaries[name] = {
                        "mean": m,
                        "std": std,
                        "p5": pct(5),
                        "p50": pct(50),
                        "p95": pct(95),
                    }
            with open(analysis_dir / "samples.json", "w", encoding="utf-8") as f:
                json.dump(summaries, f, indent=2)
            print(f"[OK] Wrote {(analysis_dir / 'samples.json').relative_to(project_root)}")

            # Generate input distribution charts for parameters with uncertainty metadata
            print("[*] Generating input distribution charts...")
            input_dist_figures_dir = project_root / "knowledge" / "figures"
            input_dist_figures_dir.mkdir(parents=True, exist_ok=True)

            # First, delete stale QMD files (we regenerate all)
            stale_dist_qmd = list(input_dist_figures_dir.glob("distribution-*.qmd"))
            if stale_dist_qmd:
                print(f"[*] Cleaning {len(stale_dist_qmd)} existing distribution QMD files...")
                for f in stale_dist_qmd:
                    f.unlink()

            input_dist_count = 0
            input_dist_errors = []
            generated_dist_qmds = set()  # Track what we generate
            for param_name, param_data in parameters.items():
                try:
                    # Only generate for parameters with uncertainty metadata
                    dist_file = generate_input_distribution_chart_qmd(
                        param_name, param_data, input_dist_figures_dir
                    )
                    generated_dist_qmds.add(dist_file.name)
                    input_dist_count += 1
                except ValueError:
                    # Parameter doesn't have uncertainty metadata - skip silently
                    pass
                except Exception as e:
                    input_dist_errors.append(f"{param_name}: {e}")

            # Clean up orphaned PNG files (PNGs without matching QMD)
            orphaned_dist_pngs = []
            for png_file in input_dist_figures_dir.glob("distribution-*.png"):
                expected_qmd = png_file.stem + ".qmd"
                if expected_qmd not in generated_dist_qmds:
                    orphaned_dist_pngs.append(png_file)
            if orphaned_dist_pngs:
                print(f"[*] Cleaning {len(orphaned_dist_pngs)} orphaned distribution PNG files...")
                for f in orphaned_dist_pngs:
                    f.unlink()

            print(f"[OK] Generated {input_dist_count} input distribution charts in knowledge/figures/")
            for err in input_dist_errors:
                print(f"[WARN] {err}")

            if target and _sens is not None:
                sens = _sens(parameters, target_name=target, n=2000)
                with open(analysis_dir / "sensitivity.json", "w", encoding="utf-8") as f:
                    json.dump(sens, f, indent=2)
                print(f"[OK] Wrote {(analysis_dir / 'sensitivity.json').relative_to(project_root)}")
            else:
                print("[WARN] No calculated target found for sensitivity analysis.")

            # Generate rigorous outcomes, tornado, and sensitivity indices for parameters with compute
            if tornado_deltas and regression_sensitivity and Outcome:
                print("[*] Generating outcome distributions and sensitivity analysis...")

                figures_dir = project_root / "knowledge" / "figures"

                # Delete stale QMD files first (we regenerate all)
                # PNGs will be cleaned up after generation (only orphans)
                stale_tornado_qmd = list(figures_dir.glob("tornado-*.qmd"))
                stale_sensitivity_qmd = list(figures_dir.glob("sensitivity-table-*.qmd"))
                stale_mc_dist_qmd = list(figures_dir.glob("mc-distribution-*.qmd"))
                stale_exceedance_qmd = list(figures_dir.glob("exceedance-*.qmd"))
                stale_qmd_files = stale_tornado_qmd + stale_sensitivity_qmd + stale_mc_dist_qmd + stale_exceedance_qmd

                if stale_qmd_files:
                    print(f"[*] Cleaning {len(stale_qmd_files)} existing QMD files...")
                    for f in stale_qmd_files:
                        f.unlink()

                # Track generated QMD files for orphan PNG cleanup later
                generated_outcome_qmds = set()

                # Validate: Find calculated parameters missing inputs/compute
                validation_warnings = []
                for param_name, meta in parameters.items():
                    val = meta.get("value")
                    source_type = getattr(val, "source_type", None)
                    has_inputs = hasattr(val, "inputs") and val.inputs
                    has_compute = hasattr(val, "compute") and val.compute

                    if source_type == "calculated":
                        if not has_inputs:
                            validation_warnings.append(f"{param_name}: missing 'inputs' (calculated parameter)")
                        if not has_compute:
                            validation_warnings.append(f"{param_name}: missing 'compute' (calculated parameter)")

                if validation_warnings:
                    print(f"\n[ERROR] {len(validation_warnings)} calculated parameters missing inputs/compute:", file=sys.stderr)
                    # Show ALL warnings - do not truncate
                    for warning in validation_warnings:
                        print(f"  - {warning}", file=sys.stderr)
                    print("\n[ERROR] Calculated parameters MUST have 'inputs' and 'compute' defined.", file=sys.stderr)
                    print("[ERROR] Options to fix:", file=sys.stderr)
                    print("[ERROR]   1. Add inputs=[] and compute=lambda ctx: ... to the Parameter", file=sys.stderr)
                    print("[ERROR]   2. Change source_type='definition' if it's an estimate/assumption", file=sys.stderr)
                    print("[ERROR]   3. Change source_type='external' if it comes from a source", file=sys.stderr)
                    sys.exit(1)

                # Validate: Check for leaf input parameters missing uncertainty metadata
                # These cause zero-variance Monte Carlo outputs, making distribution charts meaningless

                def get_all_leaf_inputs(param_name: str, visited: set = None) -> set:
                    """Recursively find all leaf (non-calculated) inputs for a parameter."""
                    if visited is None:
                        visited = set()
                    if param_name in visited:
                        return set()
                    visited.add(param_name)

                    meta = parameters.get(param_name, {})
                    val = meta.get("value")

                    # If has inputs, recurse
                    if hasattr(val, "inputs") and val.inputs:
                        leaves = set()
                        for inp in val.inputs:
                            leaves.update(get_all_leaf_inputs(inp, visited))
                        return leaves
                    else:
                        # This is a leaf parameter
                        return {param_name}

                def has_uncertainty(val) -> bool:
                    """Check if a parameter has uncertainty metadata."""
                    has_dist = hasattr(val, "distribution") and val.distribution
                    has_std = hasattr(val, "std_error") and val.std_error
                    has_ci = hasattr(val, "confidence_interval") and val.confidence_interval
                    return bool(has_dist or has_std or has_ci)

                # Collect ALL leaf parameters that are used in calculations but lack uncertainty
                all_deterministic_leaves = set()
                all_uncertain_leaves = set()

                for param_name, meta in parameters.items():
                    val = meta.get("value")
                    if hasattr(val, "compute") and val.compute and hasattr(val, "inputs") and val.inputs:
                        # Find all leaf inputs for this calculated param
                        leaf_inputs = get_all_leaf_inputs(param_name)
                        for leaf in leaf_inputs:
                            leaf_meta = parameters.get(leaf, {})
                            leaf_val = leaf_meta.get("value")
                            if has_uncertainty(leaf_val):
                                all_uncertain_leaves.add(leaf)
                            else:
                                all_deterministic_leaves.add(leaf)

                # Only flag deterministic leaves that aren't also uncertain (some params may be checked multiple times)
                truly_deterministic = all_deterministic_leaves - all_uncertain_leaves

                if truly_deterministic:
                    print(f"\n[ERROR] {len(truly_deterministic)} leaf input parameters lack uncertainty metadata:", file=sys.stderr)
                    print("[ERROR] These cause zero-variance Monte Carlo outputs for calculated parameters.", file=sys.stderr)
                    for leaf in sorted(truly_deterministic)[:20]:  # Show first 20
                        leaf_meta = parameters.get(leaf, {})
                        leaf_val = leaf_meta.get("value")
                        val_str = f"{float(leaf_val):,.4g}" if leaf_val is not None else "?"
                        print(f"  - {leaf} = {val_str}", file=sys.stderr)
                    if len(truly_deterministic) > 20:
                        print(f"  ... and {len(truly_deterministic) - 20} more", file=sys.stderr)
                    print("\n[ERROR] To fix: Add one of these to each leaf parameter:", file=sys.stderr)
                    print("[ERROR]   - distribution='normal' + std_error=<value>", file=sys.stderr)
                    print("[ERROR]   - distribution='lognormal' + std_error=<value>", file=sys.stderr)
                    print("[ERROR]   - confidence_interval=(low, high)", file=sys.stderr)
                    print("[ERROR] Monte Carlo analysis requires uncertainty on ALL input parameters.", file=sys.stderr)
                    sys.exit(1)

                # Auto-discover parameters with compute functions
                analyzable_params = []
                for param_name, meta in parameters.items():
                    val = meta.get("value")
                    if hasattr(val, "compute") and val.compute and hasattr(val, "inputs") and val.inputs:
                        # Wrap as Outcome for tornado/sensitivity
                        outcome = Outcome(
                            name=param_name,
                            inputs=val.inputs,
                            compute=val.compute,
                            units=getattr(val, "unit", "")
                        )
                        analyzable_params.append(outcome)

                if not analyzable_params:
                    print("[WARN] No parameters found with compute() and inputs for sensitivity analysis")

                # Counters for summary output
                tornado_count = 0
                sensitivity_count = 0
                mc_dist_count = 0
                exceedance_count = 0
                analysis_json_count = 0

                outcomes_data = {}
                for outcome in analyzable_params:
                    try:
                        # Build baseline context
                        ctx = {}
                        for inp in outcome.inputs:
                            meta = parameters.get(inp, {})
                            val = meta.get("value")
                            ctx[inp] = float(val) if val is not None else 0.0
                        baseline = outcome.compute(ctx)

                        # MC samples for outcome
                        input_sims = {name: sims[name] for name in outcome.inputs if name in sims}
                        if input_sims:
                            n_samples = len(list(input_sims.values())[0])
                            outcome_samples = []
                            for i in range(n_samples):
                                ctx_i = {name: float(arr[i]) for name, arr in input_sims.items()}
                                outcome_samples.append(outcome.compute(ctx_i))

                            if np is not None:
                                oa = np.asarray(outcome_samples)
                                outcomes_data[outcome.name] = {
                                    "baseline": float(baseline),
                                    "mean": float(np.mean(oa)),
                                    "std": float(np.std(oa)),
                                    "p5": float(np.percentile(oa, 5)),
                                    "p50": float(np.percentile(oa, 50)),
                                    "p95": float(np.percentile(oa, 95)),
                                    "units": outcome.units,
                                }
                            else:
                                m = sum(outcome_samples) / len(outcome_samples)
                                var = sum((v - m) ** 2 for v in outcome_samples) / len(outcome_samples)
                                std = var ** 0.5
                                sorted_o = sorted(outcome_samples)

                                def pct_o(p: float):
                                    return sorted_o[int(p / 100 * (len(sorted_o) - 1))]
                                outcomes_data[outcome.name] = {
                                    "baseline": float(baseline),
                                    "mean": m,
                                    "std": std,
                                    "p5": pct_o(5),
                                    "p50": pct_o(50),
                                    "p95": pct_o(95),
                                    "units": outcome.units,
                                }

                            # Tornado deltas for this outcome
                            tornado = tornado_deltas(parameters, outcome)
                            with open(analysis_dir / f"tornado_{outcome.name}.json", "w", encoding="utf-8") as f:
                                json.dump(tornado, f, indent=2)
                            analysis_json_count += 1

                            # Generate tornado chart QMD
                            try:
                                figures_dir = project_root / "knowledge" / "figures"
                                param_meta = parameters.get(outcome.name, {})
                                tornado_qmd = generate_tornado_chart_qmd(
                                    outcome.name, tornado, figures_dir, param_meta,
                                    baseline=float(baseline),
                                    units=outcome.units
                                )
                                generated_outcome_qmds.add(tornado_qmd.name)
                                tornado_count += 1
                            except ValueError as val_err:
                                # STRICT MODE: Fail fast when tornado data is incomplete
                                # This forces developers to either:
                                # 1. Add proper inputs/compute to intermediate calculated parameters
                                # 2. Change source_type to "definition" if not truly calculated
                                # 3. Add uncertainty distributions to leaf input parameters
                                print(f"[ERROR] {val_err}", file=sys.stderr)
                                print(f"[ERROR] Parameter '{outcome.name}' has inputs/compute but no tornado sensitivity.", file=sys.stderr)
                                print("[ERROR] This usually means:", file=sys.stderr)
                                print("[ERROR]   - Input parameters need uncertainty distributions (std_error, confidence_interval, or distribution)", file=sys.stderr)
                                print("[ERROR]   - OR intermediate inputs need their own inputs/compute definitions", file=sys.stderr)
                                print("[ERROR]   - OR this should be source_type='definition' instead of 'calculated'", file=sys.stderr)
                                sys.exit(1)
                            except Exception as chart_err:
                                print(f"[ERROR] Failed to generate tornado chart for {outcome.name}: {chart_err}", file=sys.stderr)
                                sys.exit(1)

                            # Regression sensitivity indices (filter out zero-variance inputs)
                            filtered_input_sims = {}
                            for inp_name, inp_vals in input_sims.items():
                                if np is not None:
                                    std = float(np.std(np.asarray(inp_vals)))
                                else:
                                    vals = list(inp_vals)
                                    mean = sum(vals) / len(vals)
                                    variance = sum((v - mean) ** 2 for v in vals) / len(vals)
                                    std = variance ** 0.5

                                # Only include inputs that actually vary
                                if std > 1e-10:
                                    filtered_input_sims[inp_name] = inp_vals

                            if filtered_input_sims:
                                sens_indices = regression_sensitivity(filtered_input_sims, outcome_samples)
                            else:
                                sens_indices = {inp: 0.0 for inp in input_sims.keys()}

                            with open(analysis_dir / f"sensitivity_indices_{outcome.name}.json", "w", encoding="utf-8") as f:
                                json.dump(sens_indices, f, indent=2)
                            analysis_json_count += 1

                            # Generate sensitivity table QMD only if there's meaningful variance
                            # Skip tables where all coefficients are effectively zero (< 0.001)
                            max_coef = max(abs(v) for v in sens_indices.values()) if sens_indices else 0
                            if max_coef >= 0.001:
                                try:
                                    sens_qmd = generate_sensitivity_table_qmd(outcome.name, sens_indices, figures_dir, param_meta)
                                    generated_outcome_qmds.add(sens_qmd.name)
                                    sensitivity_count += 1
                                except Exception as table_err:
                                    print(f"[WARN] Failed to generate sensitivity table for {outcome.name}: {table_err}")

                            # Generate Monte Carlo distribution chart
                            # Skip if zero variance (all samples identical) - these are meaningless
                            try:
                                outcome_info = outcomes_data.get(outcome.name, {})
                                outcome_std = outcome_info.get("std", 0)
                                if outcome_samples and len(outcome_samples) > 100 and outcome_std > 0:
                                    mc_qmd = generate_monte_carlo_distribution_chart_qmd(
                                        outcome.name,
                                        outcome_info,
                                        outcome_samples,
                                        figures_dir,
                                        param_meta
                                    )
                                    generated_outcome_qmds.add(mc_qmd.name)
                                    mc_dist_count += 1

                                    # Generate standalone CDF/exceedance chart
                                    cdf_qmd = generate_cdf_chart_qmd(
                                        outcome.name,
                                        outcome_samples,
                                        figures_dir,
                                        param_meta
                                    )
                                    generated_outcome_qmds.add(cdf_qmd.name)
                                    exceedance_count += 1
                                elif outcome_samples and outcome_std == 0:
                                    print(f"[SKIP] MC distribution chart for {outcome.name}: zero variance (deterministic)")
                            except Exception as mc_err:
                                print(f"[WARN] Failed to generate MC distribution charts for {outcome.name}: {mc_err}")
                    except Exception as e:
                        print(f"[WARN] Skipped outcome {outcome.name}: {e}")

                with open(analysis_dir / "outcomes.json", "w", encoding="utf-8") as f:
                    json.dump(outcomes_data, f, indent=2)

                # Clean up orphaned PNG files (PNGs without matching QMD)
                orphaned_pngs = []
                for png_file in figures_dir.glob("tornado-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)
                for png_file in figures_dir.glob("sensitivity-table-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)
                for png_file in figures_dir.glob("mc-distribution-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)
                for png_file in figures_dir.glob("exceedance-*.png"):
                    expected_qmd = png_file.stem + ".qmd"
                    if expected_qmd not in generated_outcome_qmds:
                        orphaned_pngs.append(png_file)

                if orphaned_pngs:
                    print(f"[*] Cleaning {len(orphaned_pngs)} orphaned PNG files...")
                    for f in orphaned_pngs:
                        f.unlink()

                # Print summary of generated files
                print(f"[OK] Generated {tornado_count} tornado charts in knowledge/figures/")
                print(f"[OK] Generated {sensitivity_count} sensitivity tables in knowledge/figures/")
                print(f"[OK] Generated {mc_dist_count} MC distribution charts in knowledge/figures/")
                print(f"[OK] Generated {exceedance_count} exceedance charts in knowledge/figures/")
                print(f"[OK] Wrote {analysis_json_count + 2} analysis JSON files to _analysis/")

                # Discount rate sensitivity for ROI_complete
                try:
                    roi_outcome = next((o for o in analyzable_params if "ROI" in o.name.upper() and "COMPLETE" in o.name.upper()), None)
                    if roi_outcome:
                        discount_curve = []
                        for rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]:
                            ctx_disc = {}
                            for inp in roi_outcome.inputs:
                                meta = parameters.get(inp, {})
                                val = meta.get("value")
                                if inp == "NPV_DISCOUNT_RATE_STANDARD":
                                    ctx_disc[inp] = rate
                                else:
                                    ctx_disc[inp] = float(val) if val is not None else 0.0
                            roi_val = roi_outcome.compute(ctx_disc)
                            discount_curve.append({"discount_rate": rate, "roi": float(roi_val)})
                        with open(analysis_dir / "discount_curve_ROI.json", "w", encoding="utf-8") as f:
                            json.dump(discount_curve, f, indent=2)
                except Exception as e:
                    print(f"[WARN] Discount curve generation skipped: {e}")

                # Scenario bands for ROI_complete
                try:
                    roi_outcome = next((o for o in analyzable_params if "ROI" in o.name.upper() and "COMPLETE" in o.name.upper()), None)
                    if roi_outcome:
                        scenarios = {
                            "worst": 0.5,  # benefits half
                            "conservative": 0.8,
                            "baseline": 1.0,
                            "optimistic": 1.5,
                        }
                        scenario_results = []
                        for scenario_name, multiplier in scenarios.items():
                            ctx_scen = {}
                            for inp in roi_outcome.inputs:
                                meta = parameters.get(inp, {})
                                val = meta.get("value")
                                v = float(val) if val is not None else 0.0
                                # Scale benefits, keep costs fixed
                                if inp in ["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT", "TRIAL_COST_REDUCTION_PCT"]:
                                    v *= multiplier
                                ctx_scen[inp] = v
                            roi_val = roi_outcome.compute(ctx_scen)
                            scenario_results.append({"scenario": scenario_name, "roi": float(roi_val)})
                        with open(analysis_dir / "scenario_bands_ROI.json", "w", encoding="utf-8") as f:
                            json.dump(scenario_results, f, indent=2)
                except Exception as e:
                    print(f"[WARN] Scenario bands generation skipped: {e}")

            print()
        else:
            print("[WARN] Uncertainty module unavailable; skipping uncertainty summaries.")
            print()
    except Exception as e:
        print(f"[WARN] Uncertainty generation skipped: {e}")
        print()

    # Generate parameters-and-calculations.qmd AFTER uncertainty charts are created
    # so the file existence checks work correctly
    print("[*] Generating parameters-and-calculations.qmd...")
    qmd_output = project_root / "knowledge" / "appendix" / "parameters-and-calculations.qmd"
    generate_parameters_qmd(parameters, qmd_output, available_refs=available_refs, params_file=parameters_path)
    print()

    # Optionally inject citations
    if inject_citations:
        print("[*] Injecting citations into economics.qmd...")
        economics_qmd = project_root / "knowledge" / "economics" / "economics.qmd"
        inject_citations_into_qmd(parameters, economics_qmd)
        print()

    # Generate outline from updated headings
    print("[*] Regenerating outline from chapter headings...")
    generate_outline_script = project_root / "scripts" / "generate-outline.py"
    if generate_outline_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(generate_outline_script), "--output", "OUTLINE-GENERATED.MD"],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.returncode == 0:
                print("[OK] Outline regenerated")
            else:
                print(f"[WARN] Outline generation had issues: {result.stderr}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Could not regenerate outline: {e}", file=sys.stderr)
    else:
        print(f"[WARN] Outline script not found: {generate_outline_script}", file=sys.stderr)
    print()

    print("[OK] All academic outputs generated successfully!")
    print()
    print("[*] Next steps:")
    print("    1. Review generated files:")
    print(f"       - {output_path.relative_to(project_root)}")
    print(f"       - {qmd_output.relative_to(project_root)}")
    print(f"       - {references_json_path.relative_to(project_root)}")
    print(f"       - {bib_output.relative_to(project_root)}")
    print(f"       - {reference_ids_path.relative_to(project_root)}")
    print("       - OUTLINE-GENERATED.MD")
    if inject_citations:
        print(f"       - {economics_qmd.relative_to(project_root)} (citations injected)")
    print("    2. Render Quarto book to see results")
    print("    3. Zero manual maintenance required - just re-run this script!")
    print()
    if citation_mode == "none":
        print("[TIP] Want citations? Try:")
        print("      --cite-mode=inline    (automatic inline citations)")
        print("      --cite-mode=separate  (flexible citation variables)")
        print("      --cite-mode=both      (maximum control)")


if __name__ == "__main__":
    main()
