#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace legacy format_billions/millions/trillions with format_parameter_value

Finds all uses of the old formatting functions and replaces them with the
universal format_parameter_value() function.
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import re
from pathlib import Path

def replace_in_file(file_path):
    """Replace legacy format functions in a single file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Pattern 1: format_parameter_value(X) -> format_parameter_value(X)
        content = re.sub(
            r'format_billions\s*\(\s*([^)]+?)\s*/\s*1[eE]9\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 2: format_parameter_value(X) -> format_parameter_value(X)
        content = re.sub(
            r'format_billions\s*\(\s*([^)]+?)\s*/\s*1[_,]?000[_,]?000[_,]?000\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 3: format_parameter_value(X) -> format_parameter_value(X)
        content = re.sub(
            r'format_millions\s*\(\s*([^)]+?)\s*/\s*1[eE]6\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 4: format_parameter_value(X) -> format_parameter_value(X)
        content = re.sub(
            r'format_millions\s*\(\s*([^)]+?)\s*/\s*1[_,]?000[_,]?000\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 5: format_parameter_value(X) -> format_parameter_value(X)
        content = re.sub(
            r'format_trillions\s*\(\s*([^)]+?)\s*/\s*1[eE]12\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # Pattern 6: format_parameter_value(X) -> format_parameter_value(X)
        content = re.sub(
            r'format_trillions\s*\(\s*([^)]+?)\s*/\s*1[_,]?000[_,]?000[_,]?000[_,]?000\s*\)',
            r'format_parameter_value(\1)',
            content
        )

        # If no changes so far, check for plain calls (less common but possible)
        # These need manual review as they might expect pre-divided values
        if content == original:
            # Look for any remaining format_billions/millions/trillions calls
            if re.search(r'format_(?:billions|millions|trillions)\s*\(', content):
                return file_path, 'MANUAL_REVIEW_NEEDED', 0

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            changes = len(re.findall(r'format_parameter_value', content)) - len(re.findall(r'format_parameter_value', original))
            return file_path, 'UPDATED', changes

        return file_path, 'NO_CHANGES', 0

    except Exception as e:
        return file_path, f'ERROR: {e}', 0

def main():
    print("[*] Searching for files with legacy format functions...")

    # Find all QMD and PY files
    qmd_files = list(Path('knowledge').rglob('*.qmd'))
    qmd_files.extend([Path('index.qmd'), Path('index-book.qmd')])

    py_files = list(Path('dih_models').rglob('*.py'))
    py_files.extend(list(Path('scripts').rglob('*.py')))

    all_files = qmd_files + py_files

    updated_files = []
    manual_review_files = []
    error_files = []

    for file_path in all_files:
        if not file_path.exists():
            continue

        result = replace_in_file(file_path)
        file_path, status, changes = result

        if status == 'UPDATED':
            updated_files.append((file_path, changes))
            print(f"[OK] {file_path}: {changes} replacements")
        elif status == 'MANUAL_REVIEW_NEEDED':
            manual_review_files.append(file_path)
            print(f"[!] {file_path}: Manual review needed")
        elif status.startswith('ERROR'):
            error_files.append((file_path, status))
            print(f"[ERROR] {file_path}: {status}")

    print(f"\n{'='*80}")
    print(f"[*] Summary:")
    print(f"    {len(updated_files)} files updated")
    print(f"    {len(manual_review_files)} files need manual review")
    print(f"    {len(error_files)} files had errors")

    if updated_files:
        total_changes = sum(changes for _, changes in updated_files)
        print(f"\n[OK] Total replacements: {total_changes}")
        print("\nUpdated files:")
        for file_path, changes in updated_files[:20]:
            print(f"  - {file_path}: {changes} changes")
        if len(updated_files) > 20:
            print(f"  ... and {len(updated_files) - 20} more")

    if manual_review_files:
        print("\n[!] Files needing manual review:")
        for file_path in manual_review_files[:10]:
            print(f"  - {file_path}")
        if len(manual_review_files) > 10:
            print(f"  ... and {len(manual_review_files) - 10} more")

    if error_files:
        print("\n[ERROR] Files with errors:")
        for file_path, error in error_files:
            print(f"  - {file_path}: {error}")

if __name__ == '__main__':
    main()
