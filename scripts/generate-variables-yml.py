#!/usr/bin/env python3
"""
Generate _variables.yml and academic outputs from parameters.py
================================================================

Reads all numeric constants from dih_models/parameters.py and generates:
1. _variables.yml - Quarto-compatible variables with tooltips
2. knowledge/appendix/parameters-and-calculations.qmd - Academic reference with LaTeX
3. references.bib - BibTeX export for LaTeX submissions
4. (Optional) Inject citations into economics.qmd

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
from typing import Any, Dict

import yaml


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


def smart_title_case(param_name: str) -> str:
    """
    Convert parameter name to title case, preserving common acronyms.

    Examples:
        DFDA_ACTIVE_TRIALS → "dFDA Active Trials"
        ROI_DISCOUNT_1PCT → "ROI Discount 1%"
        QALYS_FROM_FASTER_ACCESS → "QALYs From Faster Access"
        GDP_GROWTH_BOOST_1PCT → "GDP Growth Boost 1%"
    """
    # Common acronyms to preserve (with proper capitalization)
    ACRONYMS = {
        'DFDA': 'dFDA',  # Decentralized FDA
        'DIH': 'DIH',    # Decentralized Institutes of Health
        'ROI': 'ROI',    # Return on Investment
        'QALY': 'QALY',  # Quality-Adjusted Life Year
        'QALYS': 'QALYs',
        'DALY': 'DALY',  # Disability-Adjusted Life Year
        'DALYS': 'DALYs',
        'NPV': 'NPV',    # Net Present Value
        'OPEX': 'OPEX',  # Operating Expenses
        'CAPEX': 'CAPEX', # Capital Expenses
        'GDP': 'GDP',    # Gross Domestic Product
        'VSL': 'VSL',    # Value of Statistical Life
        'EPA': 'EPA',    # Environmental Protection Agency
        'FDA': 'FDA',    # Food and Drug Administration
        'NIH': 'NIH',    # National Institutes of Health
        'US': 'US',
        'UK': 'UK',
        'EU': 'EU',
        'WHO': 'WHO',
        'UN': 'UN',
        'ICER': 'ICER',  # Incremental Cost-Effectiveness Ratio
        'RD': 'R&D',     # Research & Development
        'CEO': 'CEO',
        'CTO': 'CTO',
        'API': 'API',
        'URL': 'URL',
        'ID': 'ID',
    }

    # Special suffix replacements
    SUFFIX_REPLACEMENTS = {
        'PCT': '%',      # 1PCT → 1%
        'MIN': 'Min',
        'MAX': 'Max',
        'AVG': 'Avg',
        'MEAN': 'Mean',
        'STD': 'Std',
        'ANNUAL': 'Annual',
        'TOTAL': 'Total',
        'GLOBAL': 'Global',
    }

    # Split by underscores
    words = param_name.split('_')

    # Process each word
    result = []
    for word in words:
        # Check if it's a known acronym
        if word in ACRONYMS:
            result.append(ACRONYMS[word])
        # Check for suffix replacements
        elif word in SUFFIX_REPLACEMENTS:
            result.append(SUFFIX_REPLACEMENTS[word])
        # Check for numeric patterns with PCT suffix (e.g., "1PCT" → "1%")
        elif len(word) > 3 and word.endswith('PCT') and word[:-3].replace('.', '').isdigit():
            result.append(f"{word[:-3]}%")
        # Default: title case
        else:
            result.append(word.capitalize())

    return ' '.join(result)


def format_parameter_value(value: float, unit: str = "") -> str:
    """
    Format a numeric value with appropriate precision, thousand separators, and units.

    Uses 3 significant figures max, removes trailing zeros.

    Args:
        value: The numeric value (may be billions for currency)
        unit: The unit string from the Parameter (e.g., "billions USD/year", "percent", "deaths/year")

    Returns:
        Formatted string with units (e.g., "$50B", "50%", "244,600")
    """
    # Detect currency parameters
    is_currency = "USD" in unit or "usd" in unit or "dollar" in unit.lower()

    # Detect percentage parameters
    is_percentage = "%" in unit or "percent" in unit.lower() or "rate" in unit.lower()

    # Check if value is already in billions, millions, thousands, or in actual dollars
    is_in_billions = "billion" in unit.lower()
    is_in_millions = "million" in unit.lower()
    is_in_thousands = "thousand" in unit.lower()

    # Helper to remove trailing zeros and decimal point
    def clean_number(num_str: str) -> str:
        if "." in num_str:
            num_str = num_str.rstrip("0").rstrip(".")
        return num_str

    # Add currency formatting if applicable (3 significant figures)
    if is_currency:
        # Determine the absolute value for scaling
        abs_val = abs(value)

        if is_in_billions:
            # Value is already in billions
            if abs_val >= 1000:  # Trillions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"  # e.g., "$123T" (3 sig figs)
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"  # e.g., "$12.3T" (3 sig figs)
                else:
                    formatted = f"${scaled:.2f}T"  # e.g., "$1.23T" (3 sig figs)
            elif abs_val >= 1:  # Billions
                if abs_val >= 100:
                    formatted = f"${value:.0f}B"  # e.g., "$123B" (3 sig figs)
                elif abs_val >= 10:
                    formatted = f"${value:.1f}B"  # e.g., "$12.3B" (3 sig figs)
                else:
                    formatted = f"${value:.2f}B"  # e.g., "$1.23B" (3 sig figs)
            elif abs_val >= 0.001:  # Millions
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"  # e.g., "$123M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"  # e.g., "$12.3M"
                else:
                    formatted = f"${scaled:.2f}M"  # e.g., "$1.23M"
            else:  # Thousands or less
                formatted = f"${value*1000000:.0f}K"
        elif is_in_millions:
            # Value is already in millions
            if abs_val >= 1000:  # Billions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"  # e.g., "$123B" (3 sig figs)
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"  # e.g., "$12.3B" (3 sig figs)
                else:
                    formatted = f"${scaled:.2f}B"  # e.g., "$1.23B" (3 sig figs)
            elif abs_val >= 1:  # Millions
                if abs_val >= 100:
                    formatted = f"${value:.0f}M"  # e.g., "$123M" (3 sig figs)
                elif abs_val >= 10:
                    formatted = f"${value:.1f}M"  # e.g., "$12.3M" (3 sig figs)
                else:
                    formatted = f"${value:.2f}M"  # e.g., "$1.23M" (3 sig figs)
            elif abs_val >= 0.001:  # Thousands
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"  # e.g., "$123K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"  # e.g., "$12.3K"
                else:
                    formatted = f"${scaled:.2f}K"  # e.g., "$1.23K"
            else:
                # Less than 1000
                formatted = f"${value*1000:.0f}"
        elif is_in_thousands:
            # Value is already in thousands
            if abs_val >= 1000000:  # Billions
                scaled = value / 1000000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"  # e.g., "$123B" (3 sig figs)
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"  # e.g., "$12.3B" (3 sig figs)
                else:
                    formatted = f"${scaled:.2f}B"  # e.g., "$1.23B" (3 sig figs)
            elif abs_val >= 1000:  # Millions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"  # e.g., "$123M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"  # e.g., "$12.3M"
                else:
                    formatted = f"${scaled:.2f}M"  # e.g., "$1.23M"
            elif abs_val >= 1:  # Thousands
                if abs_val >= 100:
                    formatted = f"${value:.0f}K"  # e.g., "$123K" (3 sig figs)
                elif abs_val >= 10:
                    formatted = f"${value:.1f}K"  # e.g., "$12.3K" (3 sig figs)
                else:
                    formatted = f"${value:.2f}K"  # e.g., "$1.23K" (3 sig figs)
            else:
                # Less than 1000
                formatted = f"${value*1000:.0f}"
        else:
            # Value is in actual dollars, convert to appropriate scale
            if abs_val >= 1e12:  # Trillions
                scaled = value / 1e12
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"  # e.g., "$123T"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"  # e.g., "$12.3T"
                else:
                    formatted = f"${scaled:.2f}T"  # e.g., "$1.23T"
            elif abs_val >= 1e9:  # Billions
                scaled = value / 1e9
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"  # e.g., "$123B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"  # e.g., "$12.3B"
                else:
                    formatted = f"${scaled:.2f}B"  # e.g., "$1.23B"
            elif abs_val >= 1e6:  # Millions
                scaled = value / 1e6
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"  # e.g., "$123M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"  # e.g., "$12.3M"
                else:
                    formatted = f"${scaled:.2f}M"  # e.g., "$1.23M"
            elif abs_val >= 1e3:  # Thousands
                scaled = value / 1e3
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"  # e.g., "$123K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"  # e.g., "$12.3K"
                else:
                    formatted = f"${scaled:.2f}K"  # e.g., "$1.23K"
            else:
                # Less than 1000
                formatted = f"${value:.0f}"

        # Clean up trailing .0 (e.g., "$50.0B" → "$50B")
        return formatted.replace(".0B", "B").replace(".0M", "M").replace(".0T", "T").replace(".0K", "K")

    # Format plain numbers with appropriate precision
    # Auto-scale large numbers to M/B/K (like we do for currency)
    abs_val = abs(value)

    if abs_val >= 1e9:  # Billions
        scaled = value / 1e9
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}B"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}B"
        else:
            formatted_num = f"{scaled:.2f}B"
    elif abs_val >= 1e6:  # Millions
        scaled = value / 1e6
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}M"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}M"
        else:
            formatted_num = f"{scaled:.2f}M"
    elif abs_val >= 100_000:  # 100K+ (for readability, scale to K)
        scaled = value / 1e3
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}K"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}K"
        else:
            formatted_num = f"{scaled:.2f}K"
    elif value == int(value):
        # Integer value - no decimals needed, use comma separators
        formatted_num = f"{int(value):,}"
    elif abs_val >= 1000:
        # Large numbers (1K-99K): use comma separators
        formatted_num = f"{value:,.0f}"
    elif abs_val >= 1:
        # Medium numbers: up to 3 sig figs, remove trailing zeros
        if value >= 100:
            formatted_num = f"{value:,.0f}"  # No decimals for 100+
        elif value >= 10:
            formatted_num = clean_number(f"{value:,.1f}")  # 1 decimal for 10-99
        else:
            formatted_num = clean_number(f"{value:,.2f}")  # 2 decimals for 1-9
    else:
        # Small numbers: 3 sig figs
        formatted_num = clean_number(f"{value:.3g}")

    # Clean trailing zeros from scaled numbers
    formatted_num = formatted_num.replace(".0B", "B").replace(".0M", "M").replace(".0K", "K")

    # Add percentage formatting if applicable
    if is_percentage:
        # Convert ratio to percentage (e.g., 2.718 → 272%)
        pct_value = value * 100

        # Format with appropriate precision
        if abs(pct_value) >= 100:
            pct_formatted = f"{pct_value:.0f}"  # e.g., "272%"
        elif abs(pct_value) >= 10:
            pct_formatted = clean_number(f"{pct_value:.1f}")  # e.g., "27.2%"
        elif abs(pct_value) >= 1:
            pct_formatted = clean_number(f"{pct_value:.2f}")  # e.g., "2.72%"
        else:
            pct_formatted = clean_number(f"{pct_value:.3g}")  # e.g., "0.272%"

        return f"{pct_formatted}%"

    # Default: just the formatted number
    return formatted_num


def generate_html_with_tooltip(param_name: str, value: float, comment: str = "", include_citation: bool = False) -> str:
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
    if hasattr(value, "display_value") and value.display_value:
        formatted_value = value.display_value
    else:
        # Extract unit if available
        unit = ""
        if hasattr(value, "unit") and value.unit:
            unit = value.unit
        formatted_value = format_parameter_value(value, unit)

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
            link_text = "View source"
        else:
            # Link to calculation/methodology page (ensure absolute path)
            if not source_ref_value.startswith("/"):
                source_ref_value = f"/{source_ref_value}"
            href = source_ref_value
            link_text = "View calculation"

        # Build tooltip from Parameter metadata with credibility indicators
        tooltip_parts = []
        if hasattr(value, "description") and value.description:
            tooltip_parts.append(value.description)

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
    else:
        # Fallback: no source metadata, use span with basic tooltip
        tooltip_parts = [f"parameters.{param_name}"]
        if comment:
            tooltip_parts.append(comment)
        tooltip = " - ".join(tooltip_parts)

        html = f'<span class="parameter-link" title="{tooltip}">{formatted_value}</span>'

    return html


def generate_variables_yml(parameters: Dict[str, Dict[str, Any]], output_path: Path, citation_mode: str = "none"):
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

        # Export LaTeX equation if available (with $$ delimiters)
        if hasattr(value, "latex") and value.latex:
            latex_var_name = f"{var_name}_latex"
            # Include $$ delimiters so variable can be used directly
            variables[latex_var_name] = f"$$\n{value.latex}\n$$"

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
        f.write("#\n\n")

        # Write variables with proper quoting for HTML
        yaml.dump(variables, f, default_flow_style=False, allow_unicode=True, sort_keys=False, default_style='"')

    # Count exports by type
    latex_count = sum(1 for k in variables.keys() if k.endswith("_latex"))
    cite_count = sum(1 for k in variables.keys() if k.endswith("_cite"))
    param_count = len(variables) - latex_count - cite_count

    print(f"[OK] Generated {output_path}")
    print(f"     {param_count} parameters exported")
    print(f"     {latex_count} LaTeX equations exported")
    if citation_mode in ("separate", "both"):
        print(f"     {cite_count} citation keys exported")
    if citation_mode in ("inline", "both"):
        print(f"     Citation mode: inline [@key] for peer-reviewed sources")
    print("\nUsage in QMD files:")
    print(f"  {{{{< var {list(variables.keys())[0]} >}}}}")
    if cite_count > 0:
        # Find first parameter with citation
        cite_var = next((k for k in variables.keys() if k.endswith("_cite")), None)
        if cite_var:
            base_var = cite_var[:-5]  # Remove "_cite"
            print(f"  {{{{< var {base_var} >}}}} {{{{< var {cite_var} >}}}}")


def generate_parameters_qmd(parameters: Dict[str, Dict[str, Any]], output_path: Path):
    """
    Generate comprehensive parameters-and-calculations.qmd appendix.

    Creates an academic reference page with:
    - All parameters organized by type (external/calculated)
    - LaTeX equations where available
    - Citations and source links
    - Confidence indicators and metadata
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
        "This appendix provides comprehensive documentation of all parameters and calculations used in the economic analysis of the 1% Treaty and Decentralized FDA."
    )
    content.append("")
    content.append(f"**Total parameters**: {len(parameters)}")
    content.append("")
    content.append(f"- External sources (peer-reviewed): {len(external_params)}")
    content.append(f"- Calculated values: {len(calculated_params)}")
    content.append(f"- Core definitions: {len(definition_params)}")
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

            # Start callout box for external source
            content.append("::: {.callout-tip icon=false collapse=false}")
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
                content.append(f"**Source**: [{display_ref}](https://warondisease.org/knowledge/references.html#{source_ref_str})")
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

            content.append(":::")
            content.append("")

    # Calculated parameters section
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

            # Start callout box for calculated value
            content.append("::: {.callout-note icon=false collapse=false}")
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

            # LaTeX equation - prominently displayed
            if hasattr(value, "latex") and value.latex:
                content.append("$$")
                content.append(value.latex)
                content.append("$$")
                content.append("")
            elif hasattr(value, "formula") and value.formula:
                content.append(f"*Formula*: `{value.formula}`")
                content.append("")

            # Source reference (calculation methodology)
            if hasattr(value, "source_ref") and value.source_ref:
                source_ref = value.source_ref

                # Detect if this is an intra-document anchor (no path separators, no file extension)
                is_anchor = "/" not in source_ref and ".qmd" not in source_ref and ".md" not in source_ref

                # Friendly labels for common methodology references
                methodology_labels = {
                    "cure-bounty-estimates": "Cure Bounty Estimation Model",
                    "disease-related-caregiving-estimate": "Disease-Related Caregiving Analysis",
                    "calculated": "Direct Calculation",
                    "sipri-2024-spending": "SIPRI Military Spending Database",
                    "book-word-count": "Book Word Count Analysis",
                }

                if is_anchor:
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

                    link_target = source_ref
                    link_text = source_ref

                content.append(f"**Methodology**: [{link_text}]({link_target})")
                content.append("")

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

            # Generate display title with priority chain: display_name → smart_title_case() → .title()
            if hasattr(value, "display_name") and value.display_name:
                display_title = value.display_name
            else:
                display_title = smart_title_case(param_name)

            # Start callout box for definition
            content.append("::: {.callout-warning icon=false collapse=false}")
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

            content.append("*Core definition*")
            content.append("")

            content.append(":::")
            content.append("")

    # Write file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(external_params)} external parameters")
    print(f"     {len(calculated_params)} calculated parameters")
    print(f"     {len(definition_params)} core definitions")


def parse_references_qmd_detailed(references_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse knowledge/references.qmd and extract full citation metadata.

    Returns a dict mapping reference IDs to citation data:
    {
        'reference-id': {
            'id': 'reference-id',
            'title': 'The reference title',
            'author': 'Author Name',
            'year': '2024',
            'source': 'Journal/Publisher Name',
            'url': 'https://...',
            'urls': ['https://...', 'https://...'],  # All URLs
            'quote': 'The quoted text',
            'note': 'Additional context',
            'type': 'article'  # article, book, misc, report, etc.
        }
    }
    """
    if not references_path.exists():
        print(f"[WARN] References file not found: {references_path}", file=sys.stderr)
        return {}

    with open(references_path, encoding="utf-8") as f:
        lines = f.readlines()

    references = {}
    current_ref = None
    current_id = None
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Match anchor tags: <a id="reference-id"></a>
        anchor_match = re.match(r'<a\s+id="([^"]+)"\s*></a>', line)
        if anchor_match:
            ref_id = anchor_match.group(1)

            # Skip internal document references (contain / or .qmd)
            if '/' in ref_id or '.qmd' in ref_id:
                i += 1
                continue

            # Save PREVIOUS reference before starting new one
            if current_id and current_ref:
                # Determine entry type based on source
                source_lower = current_ref['source'].lower()
                if any(word in source_lower for word in ['journal', 'nature', 'science', 'lancet']):
                    current_ref['type'] = 'article'
                elif any(word in source_lower for word in ['congress.gov', 'law', 'act', 'bill']):
                    current_ref['type'] = 'legislation'
                elif any(word in source_lower for word in ['cdc', 'who', 'gao', 'fda', 'nih']):
                    current_ref['type'] = 'report'
                elif any(word in source_lower for word in ['book', 'press', 'publisher']):
                    current_ref['type'] = 'book'
                elif 'university' in source_lower or 'project' in source_lower:
                    current_ref['type'] = 'techreport'

                references[current_id] = current_ref

            # Start new reference
            current_id = ref_id
            current_ref = {
                'id': ref_id,
                'title': '',
                'author': '',
                'year': '',
                'source': '',
                'url': '',
                'urls': [],
                'quote': '',
                'note': '',
                'type': 'misc'
            }
            i += 1
            continue

        # Match title: - **Title text**
        if current_id and line.startswith('- **') and line.endswith('**'):
            title = line[4:-2].strip()
            current_ref['title'] = title
            i += 1
            continue

        # Match blockquote lines (citation data)
        if current_id and line.strip().startswith('>'):
            quote_line = line.strip()[1:].strip()  # Remove '>' and whitespace

            # Attribution line (starts with em dash): — Source, Year, [Link](URL)
            if quote_line.startswith('—') or quote_line.startswith('--'):
                attribution = quote_line.lstrip('—-').strip()

                # Extract all URLs from markdown links: [text](url)
                url_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                url_matches = re.findall(url_pattern, attribution)
                for link_text, url in url_matches:
                    current_ref['urls'].append(url)
                    if not current_ref['url']:
                        current_ref['url'] = url

                # Try to extract year (4-digit number)
                year_match = re.search(r'\b(19|20)\d{2}\b', attribution)
                if year_match:
                    current_ref['year'] = year_match.group(0)

                # Extract source/author (text before year or first comma)
                # Remove markdown links for cleaner parsing
                clean_attr = re.sub(url_pattern, r'\1', attribution)

                # Split by | to get individual sources
                sources = clean_attr.split('|')
                if sources:
                    first_source = sources[0].strip()
                    # Source format: "Name, Year, Link" or "Name, Link"
                    parts = [p.strip() for p in first_source.split(',')]
                    if parts:
                        current_ref['source'] = parts[0]
                        # Use source as author if no better info available
                        if not current_ref['author']:
                            current_ref['author'] = parts[0]

                # Store full attribution as note
                current_ref['note'] = clean_attr

            # Regular quote line
            elif quote_line.startswith('"') or 'Alternative title:' in quote_line:
                if current_ref['quote']:
                    current_ref['quote'] += ' '
                current_ref['quote'] += quote_line

            i += 1
            continue

        # Continue to next line
        i += 1

    # Save last reference if exists
    if current_id and current_ref:
        # Determine entry type based on source
        source_lower = current_ref['source'].lower()
        if any(word in source_lower for word in ['journal', 'nature', 'science', 'lancet']):
            current_ref['type'] = 'article'
        elif any(word in source_lower for word in ['congress.gov', 'law', 'act', 'bill']):
            current_ref['type'] = 'legislation'
        elif any(word in source_lower for word in ['cdc', 'who', 'gao', 'fda', 'nih']):
            current_ref['type'] = 'report'
        elif any(word in source_lower for word in ['book', 'press', 'publisher']):
            current_ref['type'] = 'book'
        elif 'university' in source_lower or 'project' in source_lower:
            current_ref['type'] = 'techreport'

        references[current_id] = current_ref

    return references


def parse_references_qmd(references_path: Path) -> set:
    """
    Parse knowledge/references.qmd and extract all reference IDs.

    Returns a set of all anchor IDs (for backward compatibility).
    For detailed citation data, use parse_references_qmd_detailed().

    Example: <a id="166-billion-compounds"></a> -> "166-billion-compounds"
    """
    detailed = parse_references_qmd_detailed(references_path)
    return set(detailed.keys())


def sanitize_bibtex_key(key: str) -> str:
    """
    Sanitize citation key for BibTeX (only alphanumeric, hyphens, underscores).

    Same logic as convert-references-to-bib.py for consistency.
    """
    sanitized = key
    sanitized = sanitized.replace('/', '-')
    sanitized = sanitized.replace('#', '-')
    sanitized = sanitized.replace('.qmd', '')
    sanitized = sanitized.replace('.', '-')
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '-', sanitized)
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    return sanitized


def validate_references(parameters: Dict[str, Dict[str, Any]], available_refs: set) -> tuple[list, list]:
    """
    Validate that all external source_refs exist in references.qmd.

    Args:
        parameters: Dict of parameter metadata
        available_refs: Set of reference IDs from references.qmd

    Returns:
        Tuple of (missing_refs, used_refs) where:
        - missing_refs: List of (param_name, source_ref) tuples for missing references
        - used_refs: List of source_refs that are actually used
    """
    missing_refs = []
    used_refs = []

    for param_name, param_data in parameters.items():
        value = param_data["value"]
        if hasattr(value, "source_type"):
            source_type_str = str(value.source_type.value) if hasattr(value.source_type, 'value') else str(value.source_type)
            if source_type_str == "external":
                if hasattr(value, "source_ref") and value.source_ref:
                    source_ref = value.source_ref
                    used_refs.append(source_ref)

                    # Check if reference exists
                    if source_ref not in available_refs:
                        missing_refs.append((param_name, source_ref))

    return missing_refs, used_refs


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
    for ref_id in sorted_refs:
        # Convert kebab-case to SCREAMING_SNAKE_CASE
        enum_name = ref_id.upper().replace("-", "_")

        # Handle special cases that start with numbers
        if enum_name[0].isdigit():
            enum_name = f"_{enum_name}"

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
            first_ref = f"_{first_ref}"
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
    content.append("% used in the economic analysis of the 1% Treaty and Decentralized FDA.")
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
                content.append(f"  urldate = {{2025-01-20}},")

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

    # Generate reference_ids.py enum SECOND (before loading parameters.py which imports it)
    print("[*] Generating dih_models/reference_ids.py...")
    reference_ids_path = project_root / "dih_models" / "reference_ids.py"
    generate_reference_ids_enum(available_refs, reference_ids_path)

    # Parse parameters file THIRD (now reference_ids.py is up to date)
    parameters_path = project_root / "dih_models" / "parameters.py"
    if not parameters_path.exists():
        print(f"[ERROR] Parameters file not found: {parameters_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Parsing {parameters_path}...")
    parameters = parse_parameters_file(parameters_path)
    print(f"[OK] Found {len(parameters)} numeric parameters")
    print()

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
        # Don't exit - continue generation but warn user
    else:
        print(f"[OK] All {len(set(used_refs))} external references validated")
        print()

    # Generate _variables.yml
    print(f"[*] Generating _variables.yml (citation mode: {citation_mode})...")
    output_path = project_root / "_variables.yml"
    generate_variables_yml(parameters, output_path, citation_mode=citation_mode)
    print()

    # Generate parameters-and-calculations.qmd
    print("[*] Generating parameters-and-calculations.qmd...")
    qmd_output = project_root / "knowledge" / "appendix" / "parameters-and-calculations.qmd"
    generate_parameters_qmd(parameters, qmd_output)
    print()

    # Generate references.bib (with full citation data from references.qmd)
    print("[*] Generating references.bib...")
    bib_output = project_root / "references.bib"
    generate_bibtex(parameters, bib_output, available_refs=available_refs, references_path=references_path)
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
    print(f"       - {bib_output.relative_to(project_root)}")
    print(f"       - {reference_ids_path.relative_to(project_root)}")
    print(f"       - OUTLINE-GENERATED.MD")
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
