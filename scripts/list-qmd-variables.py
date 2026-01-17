#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a comprehensive variable usage report for a QMD file.

Produces a detailed analysis including:
1. Usage frequency (identifying duplicates)
2. Missing LaTeX definitions for calculated values
3. Categorized variable reference including context

Usage:
    python scripts/list-qmd-variables.py knowledge/economics/economics.qmd
"""

import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Handle Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def extract_variables_from_qmd(qmd_path: Path) -> list[tuple[int, str, str]]:
    """Extract all {{< var ... >}} references from a QMD file."""
    variables = []
    # Pattern to match {{< var variable_name >}}
    var_pattern = re.compile(r'\{\{<\s*var\s+([a-zA-Z0-9_]+)\s*>\}\}')

    try:
        with open(qmd_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                matches = var_pattern.findall(line)
                for var_name in matches:
                    # Get trimmed context (max 80 chars around the variable)
                    context = line.strip()
                    if len(context) > 100:
                        context = context[:100] + "..."
                    variables.append((line_num, var_name, context))
    except Exception as e:
        print(f"Error reading {qmd_path}: {e}", file=sys.stderr)
        sys.exit(1)

    return variables


def load_available_variables(variables_yml_path: Path) -> set[str]:
    """Load all variable names from a _variables.yml file."""
    variables = set()

    if not variables_yml_path.exists():
        return variables

    # Simple regex to extract variable names (keys in YAML)
    var_pattern = re.compile(r'^"?([a-zA-Z0-9_]+)"?\s*:')

    try:
        with open(variables_yml_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = var_pattern.match(line)
                if match:
                    variables.add(match.group(1))
    except Exception as e:
        print(f"Error reading {variables_yml_path}: {e}", file=sys.stderr)
        
    return variables


def main():
    parser = argparse.ArgumentParser(
        description='Generate a comprehensive variable usage report for a QMD file'
    )
    parser.add_argument('qmd_file', help='Path to the QMD file to analyze')
    
    args = parser.parse_args()

    # Resolve paths
    project_root = Path(__file__).parent.parent
    qmd_path = Path(args.qmd_file)
    if not qmd_path.is_absolute():
        qmd_path = project_root / qmd_path

    if not qmd_path.exists():
        print(f"ERROR: File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    # Load available variables
    # Check for paper-specific first, then main
    available_vars = set()
    paper_name = qmd_path.stem.split('-')[0] if '-' in qmd_path.stem else None
    
    if 'economics' in str(qmd_path):
        yml_path = project_root / '_variables-economics.yml'
    else:
        yml_path = project_root / '_variables.yml'

    if yml_path.exists():
        available_vars = load_available_variables(yml_path)

    # Extract variables from QMD
    variables = extract_variables_from_qmd(qmd_path)

    # Group by variable name
    var_usage = defaultdict(list)
    for line_num, var_name, context in variables:
        var_usage[var_name].append((line_num, context))

    # Process all keys
    keys_to_process = sorted(var_usage.keys())

    # Categorize variables
    has_latex = []
    needs_latex = []
    cite_vars = []
    other_vars = []

    for var_name in keys_to_process:
        lines = var_usage[var_name]

        if var_name.endswith('_cite'):
            cite_vars.append((var_name, lines))
            continue

        if var_name.endswith('_latex'):
            has_latex.append((var_name, lines))
            continue

        latex_name = f"{var_name}_latex"
        if latex_name in available_vars:
            has_latex.append((var_name, lines, latex_name))
        else:
            calc_indicators = ['roi', 'cost', 'benefit', 'ratio', 'multiplier',
                              'total', 'annual', 'npv', 'pv', 'rate', 'factor',
                              'reduction', 'increase', 'savings', 'value']
            is_likely_calculated = any(ind in var_name.lower() for ind in calc_indicators)

            if is_likely_calculated:
                needs_latex.append((var_name, lines))
            else:
                other_vars.append((var_name, lines))

    # --- GENERATE REPORT ---
    output_lines = []
    
    # Header
    output_lines.append(f"# Variable Report: {qmd_path.name}")
    output_lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append(f"# Source: {qmd_path}")
    if yml_path.exists():
        output_lines.append(f"# Variable Definitions: {yml_path.name}")
    output_lines.append("-" * 80)
    
    # Section 1: Usage Frequency (Highlighting Duplicates)
    output_lines.append("")
    output_lines.append("## 1. ALL VARIABLES BY FREQUENCY")
    output_lines.append("Complete list of variable occurrences, sorted by frequency.")
    output_lines.append("")
    output_lines.append(f"{'Count':<6} | {'Variable Name':<55} | {'Line Numbers'}")
    output_lines.append("-" * 6 + "-+-" + "-" * 55 + "-+-" + "-" * 15)

    # Sort all processed keys by count desc
    all_usage = [(k, var_usage[k]) for k in keys_to_process]
    sorted_usage = sorted(all_usage, key=lambda x: (-len(x[1]), x[0]))

    for var_name, lines in sorted_usage:
        count = len(lines)
        line_str = ', '.join(str(ln) for ln, _ in lines[:5])
        if len(lines) > 5:
            line_str += f" (+{len(lines)-5} more)"
        output_lines.append(f"{count:<6} | {var_name:<55} | {line_str}")

    # Section 1.5: LaTeX Equations Specific Section
    output_lines.append("")
    output_lines.append("## 2. LATEX EQUATIONS USAGE")
    output_lines.append("Specific usage of LaTeX variables (ending in _latex). Check for redundant displays.")
    output_lines.append("")
    output_lines.append(f"{'Count':<6} | {'LaTeX Variable':<55} | {'Line Numbers'}")
    output_lines.append("-" * 6 + "-+-" + "-" * 55 + "-+-" + "-" * 15)
    
    latex_usage = [(k, v) for k, v in all_usage if k.endswith('_latex')]
    sorted_latex_usage = sorted(latex_usage, key=lambda x: (-len(x[1]), x[0]))
    
    if sorted_latex_usage:
        for var_name, lines in sorted_latex_usage:
            count = len(lines)
            line_str = ', '.join(str(ln) for ln, _ in lines) # Show ALL lines for LaTeX vars
            output_lines.append(f"{count:<6} | {var_name:<55} | {line_str}")
    else:
        output_lines.append("No variables ending in _latex found.")

    # Section 2: Missing LaTeX Definitions
    if needs_latex:
        output_lines.append("")
        output_lines.append("## 3. POTENTIAL MISSING LATEX DEFINITIONS")
        output_lines.append("These variables look like calculated values but have no corresponding _latex variable defined.")
        output_lines.append("")
        for var_name, lines in needs_latex:
            output_lines.append(f"- {var_name} (Used on lines: {', '.join(str(ln) for ln, _ in lines[:3])}...)")
            # output_lines.append(f"  Context: {lines[0][1]}")

    # Section 3: Variables with LaTeX Available
    output_lines.append("")
    output_lines.append("## 4. VARIABLES WITH LATEX AVAILABLE")
    output_lines.append("Verifying usage of available LaTeX formats.")
    output_lines.append("")
    
    for item in has_latex:
        var_name = item[0]
        # If tuple has 3 elements, it means it DOES NOT end in _latex but has a companion
        # If tuple has 2 elements, it ALREADY ends in _latex
        
        if len(item) == 3:
            # Var name -> Latex name usage
            latex_counterpart = item[2]
            output_lines.append(f"- {var_name} [Has companion: {latex_counterpart}]")
        else:
            # Is a latex var
            output_lines.append(f"- {var_name} [Is LaTeX variable]")

    # Section 4: Summary Stats
    output_lines.append("")
    output_lines.append("-" * 80)
    output_lines.append("## SUMMARY STATISTICS")
    output_lines.append(f"- Total Variable References: {len(variables)}")
    output_lines.append(f"- Unique Variables:          {len(var_usage)}")
    output_lines.append(f"- Variables with Duplicates: {len([v for v in var_usage.values() if len(v) > 1])}")
    output_lines.append(f"- Missing LaTeX Candidates:  {len(needs_latex)}")
    output_lines.append("-" * 80)

    # Output
    output_text = '\n'.join(output_lines)
    
    # Always save to root of repo
    output_filename = f"variable-report-{qmd_path.stem}.md"
    output_path = project_root / output_filename
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"Report saved to: {output_path}")
    except Exception as e:
        print(f"Error saving report: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
