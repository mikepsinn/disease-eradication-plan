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


def format_parameter_value(value: float) -> str:
    """Format a numeric value with appropriate precision and thousand separators."""
    if isinstance(value, float) and value < 100 and value != int(value):
        # Small floats: show 2 decimal places
        return f"{value:,.2f}"
    elif abs(value) >= 1:
        # Large numbers: no decimals, with thousand separators
        return f"{value:,.0f}"
    else:
        # Very small numbers: show 4 decimal places
        return f"{value:.4f}"


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
    formatted_value = format_parameter_value(value)

    # Check if value is a Parameter instance with source metadata
    has_source = hasattr(value, 'source_ref') and value.source_ref

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

        # Build tooltip from Parameter metadata
        tooltip_parts = []
        if hasattr(value, 'description') and value.description:
            tooltip_parts.append(value.description)
        if hasattr(value, 'formula') and value.formula:
            tooltip_parts.append(f"Formula: {value.formula}")
        if hasattr(value, 'unit') and value.unit:
            tooltip_parts.append(f"Unit: {value.unit}")
        tooltip_parts.append(f"Click to {link_text.lower()}")

        tooltip = " | ".join(tooltip_parts)

        # Generate clickable link
        html = f'<a href="{href}" class="parameter-link" title="{tooltip}">{formatted_value}</a>'
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
