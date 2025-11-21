#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reusable Parameter Rename Utility
==================================

Renames parameters across the codebase, updating both:
- Python parameter names (UPPERCASE)
- Quarto variable names (lowercase)

Usage:
    python scripts/rename_parameters.py --mapping rename_map.json [--dry-run]
    python scripts/rename_parameters.py --old OLD_NAME --new NEW_NAME [--dry-run]

Example:
    python scripts/rename_parameters.py --old TREATY_DFDA_ICER_PER_QALY --new TREATY_DFDA_ICER_PER_QALY --dry-run
"""

import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_rename_mapping(mapping_file: Path) -> Dict[str, str]:
    """Load rename mapping from JSON file."""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_files_to_update(extensions: List[str]) -> List[Path]:
    """Find all files with given extensions in the project."""
    project_root = Path.cwd()
    files = []
    for ext in extensions:
        files.extend(project_root.glob(f'**/*{ext}'))
    # Exclude virtual environments, node_modules, and build directories
    files = [f for f in files if not any(excl in f.parts for excl in ['.venv', 'node_modules', '_book', '__pycache__'])]
    return files


def create_replacements(mapping: Dict[str, str]) -> Dict[str, str]:
    """
    Create both uppercase (Python) and lowercase (Quarto) replacements.

    Returns: {old_pattern: new_value, ...}
    """
    replacements = {}

    for old_name, new_name in mapping.items():
        # Python parameter names (UPPERCASE)
        replacements[old_name] = new_name

        # Quarto variable names (lowercase)
        old_lower = old_name.lower()
        new_lower = new_name.lower()
        replacements[old_lower] = new_lower

    return replacements


def replace_in_file(file_path: Path, replacements: Dict[str, str], dry_run: bool = False) -> Tuple[int, List[str]]:
    """
    Replace all occurrences in a file using word boundaries.

    Returns: (num_replacements, changes_made)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Skip binary files
        return 0, []

    original_content = content
    changes = []
    total_replacements = 0

    for old_name, new_name in replacements.items():
        # Use word boundaries to avoid partial matches
        # e.g., don't replace "ICER" in "TREATY_DFDA_ICER_INVESTOR_FUNDED"
        pattern = r'\b' + re.escape(old_name) + r'\b'

        # Find all matches for reporting
        matches = list(re.finditer(pattern, content))
        if matches:
            num_matches = len(matches)
            total_replacements += num_matches

            # Perform replacement
            content = re.sub(pattern, new_name, content)

            # Record change
            changes.append(f"  {old_name} -> {new_name} ({num_matches} occurrences)")

    # Write back if not dry run and changes were made
    if not dry_run and content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return total_replacements, changes


def main():
    parser = argparse.ArgumentParser(
        description='Rename parameters across Python and Quarto files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Two modes: single rename or mapping file
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--mapping', type=Path, help='JSON file with old->new mapping')
    group.add_argument('--old', help='Old parameter name (use with --new)')

    parser.add_argument('--new', help='New parameter name (use with --old)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    parser.add_argument('--extensions', nargs='+', default=['.py', '.qmd'], help='File extensions to process')

    args = parser.parse_args()

    # Build mapping
    if args.mapping:
        mapping = load_rename_mapping(args.mapping)
    else:
        if not args.new:
            parser.error('--new is required when using --old')
        mapping = {args.old: args.new}

    print(f"[*] Parameter Rename Utility")
    print(f"[*] Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"[*] Mapping:")
    for old, new in mapping.items():
        print(f"    {old} -> {new}")
    print()

    # Create replacements (both uppercase and lowercase)
    replacements = create_replacements(mapping)

    # Find files
    print(f"[*] Finding files with extensions: {', '.join(args.extensions)}")
    files = find_files_to_update(args.extensions)
    print(f"[OK] Found {len(files)} files")
    print()

    # Process files
    total_changes = 0
    files_changed = 0

    for file_path in files:
        num_replacements, changes = replace_in_file(file_path, replacements, dry_run=args.dry_run)

        if num_replacements > 0:
            files_changed += 1
            total_changes += num_replacements
            rel_path = file_path.relative_to(Path.cwd())
            print(f"[{'WOULD CHANGE' if args.dry_run else 'CHANGED'}] {rel_path}")
            for change in changes:
                print(change)
            print()

    # Summary
    print(f"[{'DRY RUN ' if args.dry_run else ''}SUMMARY]")
    print(f"  Files {'that would be ' if args.dry_run else ''}modified: {files_changed}")
    print(f"  Total replacements: {total_changes}")

    if args.dry_run:
        print()
        print("[*] Run without --dry-run to apply changes")

    return 0


if __name__ == '__main__':
    sys.exit(main())
