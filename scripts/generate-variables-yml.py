#!/usr/bin/env python3
"""
Generate _variables.yml from parameters.py
===========================================

Reads all numeric constants from dih_models/parameters.py and generates
a Quarto-compatible _variables.yml file with formatted values and tooltips.

Usage:
    python tools/generate-variables-yml.py

Output:
    _variables.yml in project root

The generated file allows using {{< var param_name >}} in QMD files.
"""

import sys
import ast
import re
from pathlib import Path
from typing import Dict, Any
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
    spec = importlib.util.spec_from_file_location("parameters", parameters_path)
    params_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params_module)

    # Also parse the file for line numbers and comments
    with open(parameters_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    line_info = {}
    for i, line in enumerate(lines, 1):
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            continue

        # Look for variable assignments
        match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*', line.strip())
        if match:
            var_name = match.group(1)
            # Extract comment if present
            comment = ""
            if '#' in line:
                comment = line.split('#', 1)[1].strip()
            line_info[var_name] = {'line_num': i, 'comment': comment}

    # Extract all uppercase constants from the module
    for name in dir(params_module):
        if name.isupper():  # Only uppercase constants
            value = getattr(params_module, name)

            # Only process numeric values (including Parameter instances)
            if isinstance(value, (int, float)):
                info = line_info.get(name, {'line_num': 0, 'comment': ''})
                parameters[name] = {
                    'value': value,  # This will be Parameter instance if defined as such
                    'line_num': info['line_num'],
                    'comment': info['comment']
                }

    return parameters


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
    is_currency = 'USD' in unit or 'usd' in unit or 'dollar' in unit.lower()

    # Detect percentage parameters
    is_percentage = '%' in unit or 'percent' in unit.lower() or 'rate' in unit.lower()

    # Check if value is already in billions, millions, thousands, or in actual dollars
    is_in_billions = 'billion' in unit.lower()
    is_in_millions = 'million' in unit.lower()
    is_in_thousands = 'thousand' in unit.lower()

    # Helper to remove trailing zeros and decimal point
    def clean_number(num_str: str) -> str:
        if '.' in num_str:
            num_str = num_str.rstrip('0').rstrip('.')
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
        return formatted.replace('.0B', 'B').replace('.0M', 'M').replace('.0T', 'T').replace('.0K', 'K')

    # Format plain numbers with appropriate precision
    if value == int(value):
        # Integer value - no decimals needed
        formatted_num = f"{int(value):,}"
    elif abs(value) >= 1000:
        # Large numbers: no decimals, with thousand separators
        formatted_num = f"{value:,.0f}"
    elif abs(value) >= 1:
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


def generate_html_with_tooltip(param_name: str, value: float, comment: str = "") -> str:
    """
    Generate HTML link with tooltip for a parameter.

    Args:
        param_name: The parameter name (e.g., 'GLOBAL_ANNUAL_CONFLICT_DEATHS')
        value: The numeric value (may be Parameter instance with metadata)
        comment: Optional comment from parameters.py

    Returns:
        HTML string with formatted value, clickable link, and tooltip
    """
    # Extract unit if available
    unit = ""
    if hasattr(value, 'unit') and value.unit:
        unit = value.unit

    formatted_value = format_parameter_value(value, unit)

    # Check if value is a Parameter instance with source metadata
    has_source = hasattr(value, 'source_ref') and value.source_ref
    is_definition = hasattr(value, 'source_type') and value.source_type == "definition"

    if has_source:
        # Determine link destination based on source type
        if hasattr(value, 'source_type') and value.source_type == "external":
            # Link to citation in references.qmd (absolute path from site root)
            href = f"/knowledge/references.qmd#{value.source_ref}"
            link_text = "View source"
        else:
            # Link to calculation/methodology page (ensure absolute path)
            source_ref = value.source_ref
            if not source_ref.startswith('/'):
                source_ref = f"/{source_ref}"
            href = source_ref
            link_text = "View calculation"

        # Build tooltip from Parameter metadata with credibility indicators
        tooltip_parts = []
        if hasattr(value, 'description') and value.description:
            tooltip_parts.append(value.description)

        # Add confidence level with emoji indicators
        if hasattr(value, 'confidence') and value.confidence:
            confidence_indicators = {
                "high": "✓ High confidence",
                "medium": "~ Medium confidence",
                "low": "? Low confidence",
                "estimated": "≈ Estimated"
            }
            tooltip_parts.append(confidence_indicators.get(value.confidence, value.confidence))

        # Show if peer-reviewed (prestigious!)
        if hasattr(value, 'peer_reviewed') and value.peer_reviewed:
            tooltip_parts.append("📊 Peer-reviewed")

        # Show if conservative estimate
        if hasattr(value, 'conservative') and value.conservative:
            tooltip_parts.append("Conservative estimate")

        # Show sensitivity/uncertainty range
        if hasattr(value, 'sensitivity') and value.sensitivity:
            sensitivity_str = format_parameter_value(value.sensitivity, unit)
            tooltip_parts.append(f"±{sensitivity_str}")

        # Show last updated date
        if hasattr(value, 'last_updated') and value.last_updated:
            tooltip_parts.append(f"Updated: {value.last_updated}")

        if hasattr(value, 'formula') and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")
        if hasattr(value, 'unit') and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")
        tooltip_parts.append(f"Click to {link_text.lower()}")

        tooltip = " | ".join(tooltip_parts)

        # Generate clickable link
        html = f'<a href="{href}" class="parameter-link" title="{tooltip}">{formatted_value}</a>'
    elif is_definition:
        # Core definition: show value with tooltip but no link
        tooltip_parts = []
        if hasattr(value, 'description') and value.description:
            tooltip_parts.append(value.description)
        if hasattr(value, 'unit') and value.unit:
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


def generate_variables_yml(parameters: Dict[str, Dict[str, Any]], output_path: Path):
    """
    Generate _variables.yml file from parameters.

    Creates YAML with lowercase variable names mapped to formatted HTML values.
    """
    variables = {}

    # Sort parameters by name for consistent output
    for param_name in sorted(parameters.keys()):
        param_data = parameters[param_name]
        value = param_data['value']
        comment = param_data['comment']

        # Use lowercase name for Quarto variables (convention)
        var_name = param_name.lower()

        # Generate formatted HTML with tooltip
        html_value = generate_html_with_tooltip(param_name, value, comment)

        variables[var_name] = html_value

    # Write YAML file
    with open(output_path, 'w', encoding='utf-8') as f:
        # Add header comment
        f.write("# AUTO-GENERATED FILE - DO NOT EDIT\n")
        f.write("# Generated from dih_models/parameters.py\n")
        f.write("# Run: python tools/generate-variables-yml.py\n")
        f.write("#\n")
        f.write("# Use in QMD files with: {{< var param_name >}}\n")
        f.write("#\n\n")

        # Write variables with proper quoting for HTML
        yaml.dump(variables, f, default_flow_style=False, allow_unicode=True, sort_keys=False, default_style='"')

    print(f"[OK] Generated {output_path}")
    print(f"     {len(variables)} parameters exported")
    print(f"\nUsage in QMD files:")
    print(f'  {{{{< var {list(variables.keys())[0]} >}}}}')


def main():
    # Get project root
    project_root = Path(__file__).parent.parent.absolute()

    # Parse parameters file
    parameters_path = project_root / 'dih_models' / 'parameters.py'
    if not parameters_path.exists():
        print(f"[ERROR] Parameters file not found: {parameters_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Parsing {parameters_path}...")
    parameters = parse_parameters_file(parameters_path)
    print(f"[OK] Found {len(parameters)} numeric parameters")

    # Generate _variables.yml
    output_path = project_root / '_variables.yml'
    generate_variables_yml(parameters, output_path)

    print("\n[*] Next steps:")
    print("    1. Review _variables.yml")
    print("    2. Run: python tools/link-parameters.py --fix")
    print("    3. Render your Quarto documents")


if __name__ == '__main__':
    main()
