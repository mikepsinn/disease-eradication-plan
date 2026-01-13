#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List all Quarto variables used in a QMD file with line numbers.

Helps identify:
1. Which variables are used in a file
2. Which variables have _latex counterparts available
3. Which calculated variables might need LaTeX equations

Usage:
    python scripts/list-qmd-variables.py knowledge/economics/economics.qmd
    python scripts/list-qmd-variables.py knowledge/economics/economics.qmd -o _analysis/economics-variables.txt
"""

import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict

# Handle Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def extract_variables_from_qmd(qmd_path: Path) -> list[tuple[int, str, str]]:
    """
    Extract all {{< var ... >}} references from a QMD file.

    Returns:
        List of (line_number, variable_name, full_context) tuples
    """
    variables = []

    # Pattern to match {{< var variable_name >}}
    var_pattern = re.compile(r'\{\{<\s*var\s+([a-zA-Z0-9_]+)\s*>\}\}')

    with open(qmd_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            matches = var_pattern.findall(line)
            for var_name in matches:
                # Get trimmed context (max 80 chars around the variable)
                context = line.strip()[:100]
                variables.append((line_num, var_name, context))

    return variables


def load_available_variables(variables_yml_path: Path) -> set[str]:
    """Load all variable names from a _variables.yml file."""
    variables = set()

    if not variables_yml_path.exists():
        return variables

    # Simple regex to extract variable names (keys in YAML)
    var_pattern = re.compile(r'^"?([a-zA-Z0-9_]+)"?\s*:')

    with open(variables_yml_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = var_pattern.match(line)
            if match:
                variables.add(match.group(1))

    return variables


def main():
    parser = argparse.ArgumentParser(
        description='List all Quarto variables used in a QMD file'
    )
    parser.add_argument('qmd_file', help='Path to the QMD file to analyze')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--variables-yml', help='Path to _variables.yml to check for _latex versions')
    parser.add_argument('--show-missing-latex', action='store_true',
                        help='Only show variables that might need _latex versions')

    args = parser.parse_args()

    # Resolve paths
    project_root = Path(__file__).parent.parent
    qmd_path = Path(args.qmd_file)
    if not qmd_path.is_absolute():
        qmd_path = project_root / qmd_path

    if not qmd_path.exists():
        print(f"ERROR: File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    # Load available variables if yml path provided
    available_vars = set()
    if args.variables_yml:
        yml_path = Path(args.variables_yml)
        if not yml_path.is_absolute():
            yml_path = project_root / yml_path
        available_vars = load_available_variables(yml_path)
    else:
        # Try to find the appropriate _variables file
        # Check for paper-specific first, then main
        paper_name = qmd_path.stem.split('-')[0] if '-' in qmd_path.stem else None

        # For economics.qmd, use _variables-economics.yml
        if 'economics' in str(qmd_path):
            yml_path = project_root / '_variables-economics.yml'
        else:
            yml_path = project_root / '_variables.yml'

        if yml_path.exists():
            available_vars = load_available_variables(yml_path)
            print(f"# Loaded {len(available_vars)} variables from {yml_path.name}", file=sys.stderr)

    # Extract variables from QMD
    variables = extract_variables_from_qmd(qmd_path)

    # Group by variable name to find unique uses
    var_usage = defaultdict(list)
    for line_num, var_name, context in variables:
        var_usage[var_name].append((line_num, context))

    # Prepare output
    output_lines = []
    output_lines.append(f"# Variables in {qmd_path.name}")
    output_lines.append(f"# Total references: {len(variables)}")
    output_lines.append(f"# Unique variables: {len(var_usage)}")
    output_lines.append("")

    # Categorize variables
    has_latex = []
    needs_latex = []
    cite_vars = []
    other_vars = []

    for var_name in sorted(var_usage.keys()):
        lines = var_usage[var_name]

        # Check if it's a citation variable
        if var_name.endswith('_cite'):
            cite_vars.append((var_name, lines))
            continue

        # Check if it already IS a latex variable
        if var_name.endswith('_latex'):
            has_latex.append((var_name, lines))
            continue

        # Check if a _latex version exists
        latex_name = f"{var_name}_latex"
        if latex_name in available_vars:
            has_latex.append((var_name, lines, latex_name))
        else:
            # Check if this looks like a calculated value that might need latex
            # (contains words like roi, cost, benefit, ratio, multiplier, etc.)
            calc_indicators = ['roi', 'cost', 'benefit', 'ratio', 'multiplier',
                              'total', 'annual', 'npv', 'pv', 'rate', 'factor',
                              'reduction', 'increase', 'savings', 'value']
            is_likely_calculated = any(ind in var_name.lower() for ind in calc_indicators)

            if is_likely_calculated:
                needs_latex.append((var_name, lines))
            else:
                other_vars.append((var_name, lines))

    # Output: Variables with _latex available
    output_lines.append("=" * 70)
    output_lines.append("VARIABLES WITH _LATEX AVAILABLE (consider using for equations)")
    output_lines.append("=" * 70)
    for item in has_latex:
        var_name = item[0]
        lines = item[1]
        latex_name = item[2] if len(item) > 2 else f"{var_name}_latex"
        line_nums = ', '.join(str(ln) for ln, _ in lines[:5])
        if len(lines) > 5:
            line_nums += f" (+{len(lines)-5} more)"
        output_lines.append(f"  {var_name}")
        output_lines.append(f"    -> {latex_name}")
        output_lines.append(f"    Lines: {line_nums}")
        output_lines.append("")

    # Output: Variables that might need _latex
    output_lines.append("")
    output_lines.append("=" * 70)
    output_lines.append("CALCULATED VARIABLES WITHOUT _LATEX (might need equations)")
    output_lines.append("=" * 70)
    for var_name, lines in needs_latex:
        line_nums = ', '.join(str(ln) for ln, _ in lines[:5])
        if len(lines) > 5:
            line_nums += f" (+{len(lines)-5} more)"
        # Show first context
        first_context = lines[0][1][:60] + "..." if len(lines[0][1]) > 60 else lines[0][1]
        output_lines.append(f"  {var_name}")
        output_lines.append(f"    Lines: {line_nums}")
        output_lines.append(f"    Context: {first_context}")
        output_lines.append("")

    # Output: Other variables (external data, definitions)
    if not args.show_missing_latex:
        output_lines.append("")
        output_lines.append("=" * 70)
        output_lines.append("OTHER VARIABLES (external data, definitions - likely don't need latex)")
        output_lines.append("=" * 70)
        for var_name, lines in other_vars:
            line_nums = ', '.join(str(ln) for ln, _ in lines[:3])
            if len(lines) > 3:
                line_nums += f" (+{len(lines)-3} more)"
            output_lines.append(f"  {var_name}: lines {line_nums}")

    # Output: Citation variables
    if not args.show_missing_latex:
        output_lines.append("")
        output_lines.append("=" * 70)
        output_lines.append(f"CITATION VARIABLES ({len(cite_vars)} total)")
        output_lines.append("=" * 70)
        output_lines.append("  (omitted - these are citation references)")

    # Summary
    output_lines.append("")
    output_lines.append("=" * 70)
    output_lines.append("SUMMARY")
    output_lines.append("=" * 70)
    output_lines.append(f"  Variables with _latex available: {len(has_latex)}")
    output_lines.append(f"  Calculated vars without _latex:  {len(needs_latex)}")
    output_lines.append(f"  Other variables:                 {len(other_vars)}")
    output_lines.append(f"  Citation variables:              {len(cite_vars)}")

    # Write output
    output_text = '\n'.join(output_lines)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = project_root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"Output written to {output_path}")
    else:
        print(output_text)


if __name__ == '__main__':
    main()
