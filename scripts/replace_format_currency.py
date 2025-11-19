#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace format_currency calls with format_parameter_value

The old format_currency expected values pre-divided into billions/millions.
The new format_parameter_value handles raw values and auto-scales.

Patterns to replace:
- format_currency(X / 1e9) -> format_parameter_value(X)
- format_currency(X / 1_000_000_000) -> format_parameter_value(X)
- format_currency(X / 1000) -> format_parameter_value(X)
- format_currency(X / 1e6) -> format_parameter_value(X)
- format_currency(X) -> format_parameter_value(X)
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import re
from pathlib import Path

def replace_format_currency(file_path):
    """Replace format_currency calls in a single file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Pattern 1: format_currency(X / 1e9) -> format_parameter_value(X)
        content = re.sub(
            r'format_currency\s*\(\s*([^)]+?)\s*/\s*1[eE]9\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 2: format_currency(X / 1_000_000_000) -> format_parameter_value(X)
        content = re.sub(
            r'format_currency\s*\(\s*([^)]+?)\s*/\s*1[_,]?000[_,]?000[_,]?000\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 3: format_currency(X / 1e6) -> format_parameter_value(X)
        content = re.sub(
            r'format_currency\s*\(\s*([^)]+?)\s*/\s*1[eE]6\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 4: format_currency(X / 1_000_000) -> format_parameter_value(X)
        content = re.sub(
            r'format_currency\s*\(\s*([^)]+?)\s*/\s*1[_,]?000[_,]?000\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 5: format_currency(X / 1000) -> format_parameter_value(X)
        content = re.sub(
            r'format_currency\s*\(\s*([^)]+?)\s*/\s*1000\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 6: format_currency(abs(X)) -> format_parameter_value(abs(X))
        # This handles special cases with abs()
        content = re.sub(
            r'format_currency\s*\(\s*abs\(([^)]+)\)\s*\)',
            r'format_parameter_value(abs(\1))',
            content
        )

        # Pattern 7: Plain format_currency(X) -> format_parameter_value(X)
        # Only if no division was already matched
        content = re.sub(
            r'format_currency\s*\(',
            r'format_parameter_value(',
            content
        )

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            changes = content.count('format_parameter_value') - original.count('format_parameter_value')
            return file_path, 'UPDATED', changes

        return file_path, 'NO_CHANGES', 0

    except Exception as e:
        return file_path, f'ERROR: {e}', 0

def main():
    print("[*] Replacing format_currency with format_parameter_value...")

    # Only process parameters.py (where all the _formatted variables are defined)
    params_file = Path('dih_models/parameters.py')

    if not params_file.exists():
        print(f"[ERROR] {params_file} not found")
        sys.exit(1)

    result = replace_format_currency(params_file)
    file_path, status, changes = result

    if status == 'UPDATED':
        print(f"[OK] {file_path}: {changes} replacements")
    elif status == 'NO_CHANGES':
        print(f"[INFO] {file_path}: No changes needed")
    else:
        print(f"[ERROR] {file_path}: {status}")
        sys.exit(1)

    print(f"\n{'='*80}")
    print("[OK] Replacement complete!")
    print("     All format_currency calls replaced with format_parameter_value")
    print("\n[*] Next step: Regenerate _variables.yml")

if __name__ == '__main__':
    main()
