#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Inline Python Expressions in Quarto Files

This script:
1. Scans all .qmd files for inline Python expressions with function calls
2. Extracts unique patterns like `format_billions(TREATY_ANNUAL_FUNDING)`
3. Generates formatted variable names with _formatted suffix
4. Adds them to economic_parameters.py
5. Replaces complex expressions in all .qmd files with simple variable names

Usage:
    python scripts/fix_inline_python.py [--dry-run]
"""

import re
import os
import sys
from pathlib import Path
from collections import defaultdict
import argparse

# Set UTF-8 encoding for stdout to handle unicode characters
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Patterns to match inline Python expressions
INLINE_PYTHON_PATTERN = r'`\{python\}\s+([^`]+)`'

# Function call patterns we want to replace
FUNCTION_PATTERNS = [
    r'format_billions\(([^)]+)\)',
    r'format_millions\(([^)]+)\)',
    r'format_percentage\(([^)]+)\)',
    r'format_currency\(([^)]+)\)',
    r'format_roi\(([^)]+)\)',
    r'format_qalys\(([^)]+)\)',
    r'format_billions_latex\(([^)]+)\)',
    r'f"([^"]+)"',  # f-strings
]


def find_qmd_files(root_dir='.'):
    """Find all .qmd files in the project"""
    qmd_files = []
    for path in Path(root_dir).rglob('*.qmd'):
        qmd_files.append(str(path))
    return qmd_files


def extract_inline_expressions(file_path):
    """Extract all inline Python expressions from a .qmd file (excluding code blocks)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove Python code blocks (```{python} ... ```)
    # This prevents matching inline expressions inside code blocks
    content_without_blocks = re.sub(
        r'```\{python\}.*?```',
        '',
        content,
        flags=re.DOTALL
    )

    expressions = []
    for match in re.finditer(INLINE_PYTHON_PATTERN, content_without_blocks):
        expr = match.group(1).strip()
        expressions.append(expr)

    return expressions


def needs_replacement(expr):
    """Check if an expression contains function calls or f-strings"""
    for pattern in FUNCTION_PATTERNS:
        if re.search(pattern, expr):
            return True
    return False


def generate_variable_name(expr):
    """Generate a formatted variable name from an expression

    Examples:
        format_billions(TREATY_ANNUAL_FUNDING) -> treaty_annual_funding_formatted
        format_percentage(VICTORY_BOND_ANNUAL_RETURN_PCT) -> victory_bond_annual_return_pct_formatted
        f"{GLOBAL_DAILY_DEATHS_CURABLE_DISEASES:,.0f}" -> global_daily_deaths_curable_diseases_formatted
    """
    # Extract the main variable name

    # Try to find a constant name (uppercase with underscores)
    const_match = re.search(r'([A-Z][A-Z0-9_]+)', expr)
    if const_match:
        const_name = const_match.group(1)
        # Convert to lowercase and add _formatted suffix
        return const_name.lower() + '_formatted'

    # If no constant found, try to create a name from the expression
    # Remove special characters and convert to snake_case
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', expr)
    clean = re.sub(r'_+', '_', clean).strip('_').lower()
    return clean + '_formatted'


def generate_formatted_value(expr):
    """Generate the Python code to create the formatted value

    Examples:
        format_billions(TREATY_ANNUAL_FUNDING) -> format_billions(TREATY_ANNUAL_FUNDING)
        f"{GLOBAL_DAILY_DEATHS:,.0f}" -> f"{GLOBAL_DAILY_DEATHS:,.0f}"
    """
    return expr


def scan_all_expressions():
    """Scan all .qmd files and collect expressions that need formatting"""
    expressions_by_var = {}  # var_name -> expression
    files_with_expressions = defaultdict(list)  # file -> [(original_expr, var_name)]

    qmd_files = find_qmd_files()
    print(f"Found {len(qmd_files)} .qmd files")

    for file_path in qmd_files:
        expressions = extract_inline_expressions(file_path)

        for expr in expressions:
            if needs_replacement(expr):
                var_name = generate_variable_name(expr)

                # Store the expression
                if var_name not in expressions_by_var:
                    expressions_by_var[var_name] = expr

                # Track which files use which expressions
                files_with_expressions[file_path].append((expr, var_name))

    print(f"Found {len(expressions_by_var)} unique expressions to format")
    return expressions_by_var, files_with_expressions


def update_economic_parameters(expressions_by_var, dry_run=False):
    """Add formatted variables to economic_parameters.py"""
    params_file = 'brain/book/appendix/economic_parameters.py'

    with open(params_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where to insert the formatted values section
    # Look for the end of the file or a specific marker

    # Generate the new formatted values section
    formatted_section = "\n# ---\n"
    formatted_section += "# PRE-FORMATTED VALUES FOR INLINE DISPLAY\n"
    formatted_section += "# ---\n"
    formatted_section += "# These are pre-computed formatted strings for use in Quarto inline expressions.\n"
    formatted_section += "# Quarto inline code should only reference simple variables, not function calls.\n"
    formatted_section += "# See: https://quarto.org/docs/computations/inline-code.html\n\n"

    # Sort variables alphabetically
    for var_name in sorted(expressions_by_var.keys()):
        expr = expressions_by_var[var_name]
        formatted_section += f"{var_name} = {expr}\n"

    formatted_section += "\n"

    if dry_run:
        print("\n=== Would add to economic_parameters.py ===")
        print(formatted_section)
    else:
        # Check if the section already exists
        if "# PRE-FORMATTED VALUES FOR INLINE DISPLAY" in content:
            # Remove old section and add new one
            pattern = r'# ---\n# PRE-FORMATTED VALUES FOR INLINE DISPLAY\n.*?(?=\n# ---|$)'
            content = re.sub(pattern, formatted_section.rstrip(), content, flags=re.DOTALL)
        else:
            # Append to end of file
            content = content.rstrip() + "\n\n" + formatted_section

        with open(params_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Updated {params_file} with {len(expressions_by_var)} formatted variables")


def update_qmd_files(files_with_expressions, dry_run=False):
    """Replace complex inline expressions with simple variable names in .qmd files"""

    for file_path, replacements in files_with_expressions.items():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Sort replacements by length (longest first) to avoid partial replacements
        replacements.sort(key=lambda x: len(x[0]), reverse=True)

        for original_expr, var_name in replacements:
            # Escape special regex characters in the expression
            escaped_expr = re.escape(original_expr)
            pattern = r'`\{python\}\s+' + escaped_expr + r'`'
            replacement = f'`{{python}} {var_name}`'

            content = re.sub(pattern, replacement, content)

        if content != original_content:
            if dry_run:
                print(f"\n=== Would update {file_path} ===")
                print(f"  {len(replacements)} replacements")
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Updated {file_path} ({len(replacements)} replacements)")


def main():
    parser = argparse.ArgumentParser(description='Fix inline Python expressions in Quarto files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    args = parser.parse_args()

    print("Scanning .qmd files for inline Python expressions...")
    expressions_by_var, files_with_expressions = scan_all_expressions()

    if not expressions_by_var:
        print("No expressions found that need formatting")
        return

    print(f"\nFound {len(files_with_expressions)} files with expressions to replace")

    # Update economic_parameters.py
    update_economic_parameters(expressions_by_var, dry_run=args.dry_run)

    # Update .qmd files
    update_qmd_files(files_with_expressions, dry_run=args.dry_run)

    if args.dry_run:
        print("\n=== DRY RUN - No files were modified ===")
    else:
        print("\n✓ Done! All inline expressions have been simplified")


if __name__ == '__main__':
    main()
