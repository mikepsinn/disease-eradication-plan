#!/usr/bin/env python3
"""
Parameter Validation - Detect Duplicates and Issues
===================================================

Checks parameters.py for:
- Duplicate parameter names (overwritten definitions)
- Duplicate values (potential copy-paste errors)
- Missing metadata in Parameter instances

Usage:
    python tools/validate-parameters.py
"""

import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple


def parse_parameter_definitions(parameters_path: Path) -> List[Tuple[str, int, str]]:
    """
    Parse parameters.py and extract all parameter definitions.

    Returns list of (name, line_number, full_line) tuples.
    """
    definitions = []

    with open(parameters_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            continue

        # Only check module-level assignments (no leading whitespace before variable name)
        # This excludes function-local variables which are indented
        match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*', line)
        if match:
            var_name = match.group(1)
            definitions.append((var_name, i, line.strip()))

    return definitions


def check_duplicate_names(definitions: List[Tuple[str, int, str]]) -> List[str]:
    """Check for duplicate parameter names (redefinitions)."""
    errors = []
    name_locations = defaultdict(list)

    for name, line_num, _ in definitions:
        name_locations[name].append(line_num)

    for name, locations in name_locations.items():
        if len(locations) > 1:
            loc_str = ", ".join(f"line {loc}" for loc in locations)
            errors.append(f"[ERROR] Duplicate parameter '{name}' defined at: {loc_str}")
            errors.append(f"        > Last definition (line {locations[-1]}) will be used, others ignored!")

    return errors


def check_duplicate_values(parameters_path: Path) -> List[str]:
    """Check for duplicate parameter values (potential errors)."""
    warnings = []

    # Import the parameters module to get actual values
    import importlib.util
    spec = importlib.util.spec_from_file_location("parameters", parameters_path)
    params_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params_module)

    # Group parameters by value
    value_to_params = defaultdict(list)
    for name in dir(params_module):
        if name.isupper():
            value = getattr(params_module, name)
            if isinstance(value, (int, float)):
                # Use float value for comparison (handles Parameter instances)
                float_val = float(value)
                value_to_params[float_val].append(name)

    # Report duplicates (skip common values like 0, 1, 100)
    common_values = {0, 0.0, 1, 1.0, 100, 100.0, 0.01, 0.1}
    for value, params in value_to_params.items():
        if len(params) > 1 and value not in common_values:
            params_str = ", ".join(params)
            warnings.append(f"[WARNING] Value {value} used by multiple parameters: {params_str}")
            warnings.append(f"          > This might be intentional, or a copy-paste error")

    return warnings


def check_parameter_metadata(parameters_path: Path) -> List[str]:
    """Check Parameter instances for missing metadata."""
    warnings = []

    # Import the parameters module
    import importlib.util
    spec = importlib.util.spec_from_file_location("parameters", parameters_path)
    params_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params_module)

    for name in dir(params_module):
        if name.isupper():
            value = getattr(params_module, name)

            # Check if it's a Parameter instance
            if hasattr(value, 'source_ref'):
                issues = []

                if not value.source_ref:
                    issues.append("missing source_ref")

                if not hasattr(value, 'description') or not value.description:
                    issues.append("missing description")

                if not hasattr(value, 'unit') or not value.unit:
                    issues.append("missing unit")

                if issues:
                    issues_str = ", ".join(issues)
                    warnings.append(f"[WARNING] Parameter '{name}' has incomplete metadata: {issues_str}")

    return warnings


def main():
    # Get project root
    project_root = Path(__file__).parent.parent.absolute()
    parameters_path = project_root / 'dih_models' / 'parameters.py'

    if not parameters_path.exists():
        print(f"[ERROR] Parameters file not found: {parameters_path}", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("PARAMETER VALIDATION REPORT")
    print("=" * 80)
    print()

    # Parse parameter definitions
    print("[*] Parsing parameter definitions...")
    definitions = parse_parameter_definitions(parameters_path)
    print(f"[OK] Found {len(definitions)} parameter definitions")
    print()

    # Check for duplicate names
    print("[*] Checking for duplicate parameter names...")
    name_errors = check_duplicate_names(definitions)
    if name_errors:
        for error in name_errors:
            print(error)
        print()
    else:
        print("[OK] No duplicate parameter names found")
        print()

    # Check for duplicate values
    print("[*] Checking for duplicate parameter values...")
    value_warnings = check_duplicate_values(parameters_path)
    if value_warnings:
        for warning in value_warnings[:20]:  # Limit to first 20
            print(warning)
        if len(value_warnings) > 20:
            print(f"... and {len(value_warnings) - 20} more")
        print()
    else:
        print("[OK] No suspicious duplicate values found")
        print()

    # Check Parameter metadata
    print("[*] Checking Parameter instances for metadata...")
    metadata_warnings = check_parameter_metadata(parameters_path)
    if metadata_warnings:
        for warning in metadata_warnings[:10]:  # Limit to first 10
            print(warning)
        if len(metadata_warnings) > 10:
            print(f"... and {len(metadata_warnings) - 10} more")
        print()
    else:
        print("[OK] All Parameter instances have complete metadata")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total_errors = len(name_errors)
    total_warnings = len(value_warnings) + len(metadata_warnings)

    print(f"Errors:   {total_errors}")
    print(f"Warnings: {total_warnings}")
    print()

    if total_errors > 0:
        print("[!] Fix errors before proceeding - duplicate names will cause bugs!")
        sys.exit(1)
    elif total_warnings > 0:
        print("[!] Review warnings - they may indicate issues")
        sys.exit(0)
    else:
        print("[OK] All validations passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
