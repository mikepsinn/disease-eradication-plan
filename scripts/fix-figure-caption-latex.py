#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix LaTeX-Unsafe Characters in Figure Captions
===============================================

Sanitizes figure captions (![caption](image.jpg)) by replacing characters
that break LaTeX rendering:
  - % -> percent
  - $ -> removed (just the symbol, numbers remain)
  - & -> and
  - _ -> - (in subscript-like patterns)

Usage:
    .venv\\Scripts\\python.exe scripts/fix-figure-caption-latex.py           # Dry run
    .venv\\Scripts\\python.exe scripts/fix-figure-caption-latex.py --fix     # Apply fixes
"""

import re
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from lib.quarto_file_utils import get_all_qmd_files, find_project_root


def sanitize_caption(caption: str) -> str:
    """
    Sanitize a figure caption for LaTeX compatibility.

    Replacements:
      - \\% or % -> " percent" (with smart spacing)
      - \\$ or $ -> removed (just the symbol)
      - & -> " and "
      - _ -> "-" (in subscript patterns)
    """
    result = caption

    # First normalize escaped versions
    result = result.replace('\\%', '%')
    result = result.replace('\\$', '$')
    result = result.replace('\\&', '&')
    result = result.replace('\\_', '_')

    # Replace % with " percent" (smart spacing)
    # Pattern: number followed by % (e.g., "3.5%" -> "3.5 percent")
    result = re.sub(r'(\d)%', r'\1 percent', result)
    # Any remaining % (shouldn't be common)
    result = result.replace('%', ' percent')
    # Clean up double spaces
    result = re.sub(r' +percent', ' percent', result)

    # Remove $ entirely (e.g., "$27.2B" -> "27.2B")
    # Pattern: $number - just remove the $
    result = re.sub(r'\$(\d)', r'\1', result)
    # Any remaining $ (shouldn't be common)
    result = result.replace('$', '')

    # Replace & with " and "
    result = re.sub(r'\s*&\s*', ' and ', result)

    # Replace _ in subscript-like patterns (e.g., "t_p" -> "t-p")
    # Only replace _ between alphanumeric characters
    result = re.sub(r'(\w)_(\w)', r'\1-\2', result)
    # Any remaining underscores
    result = result.replace('_', '-')

    # Clean up any double spaces created
    result = re.sub(r'  +', ' ', result)

    return result


def process_file(filepath: Path, apply_fix: bool = False) -> list:
    """
    Process a single QMD file for figure captions with LaTeX-unsafe characters.

    Returns list of changes made (or would be made in dry run).
    """
    changes = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"ERROR: Cannot read {filepath}: {e}")
        return changes

    # Find all figure references: ![caption](path)
    # Pattern captures the full match and the caption separately
    pattern = r'!\[([^\]]*)\]\([^)]+\)'

    def replace_caption(match):
        full_match = match.group(0)
        caption = match.group(1)

        # Check if caption has any problematic characters
        if not any(c in caption for c in ['%', '$', '&', '_', '\\%', '\\$', '\\&', '\\_']):
            return full_match

        sanitized = sanitize_caption(caption)

        if sanitized != caption:
            # Record the change
            changes.append({
                'original': caption,
                'sanitized': sanitized,
            })
            # Replace caption in the full match
            return full_match.replace(f'[{caption}]', f'[{sanitized}]')

        return full_match

    new_content = re.sub(pattern, replace_caption, content)

    if changes and apply_fix:
        try:
            filepath.write_text(new_content, encoding='utf-8')
        except Exception as e:
            print(f"ERROR: Cannot write {filepath}: {e}")

    return changes


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fix LaTeX-unsafe characters in figure captions"
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Apply fixes (default is dry run)'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Process a single file instead of all QMD files'
    )
    args = parser.parse_args()

    project_root = find_project_root()

    if args.file:
        files = [args.file]
    else:
        files = get_all_qmd_files(project_root, include_index=True)

    total_changes = 0
    files_changed = 0

    mode = "FIXING" if args.fix else "DRY RUN"
    print(f"\n=== {mode}: LaTeX Figure Caption Sanitizer ===\n")

    for filepath_str in files:
        filepath = project_root / filepath_str

        if not filepath.exists():
            continue

        changes = process_file(filepath, apply_fix=args.fix)

        if changes:
            files_changed += 1
            total_changes += len(changes)

            print(f"\n{filepath_str}:")
            for change in changes:
                print(f"  - \"{change['original']}\"")
                print(f"  + \"{change['sanitized']}\"")

    print(f"\n=== Summary ===")
    print(f"Files scanned: {len(files)}")
    print(f"Files with changes: {files_changed}")
    print(f"Total caption fixes: {total_changes}")

    if not args.fix and total_changes > 0:
        print(f"\nRun with --fix to apply these changes.")


if __name__ == "__main__":
    main()
