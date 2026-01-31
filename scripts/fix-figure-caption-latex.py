#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix problematic LaTeX characters in figure captions.

Replaces:
- $X → X USD (currency amounts)
- X% → X percent
- & → and (but not HTML entities)
"""

import io
import os
import re
import sys
from typing import cast

if sys.platform == 'win32':
    cast(io.TextIOWrapper, sys.stdout).reconfigure(encoding='utf-8')
    cast(io.TextIOWrapper, sys.stderr).reconfigure(encoding='utf-8')

from lib.quarto_file_utils import find_files_by_extension


def fix_caption(caption: str) -> str:
    """Fix problematic LaTeX characters in a figure caption."""
    original = caption

    # Fix currency: $X.XX → X.XX USD, $X → X USD
    # Handle different patterns separately for accuracy:

    # Pattern 1: $X trillion/billion/million/thousand (with space)
    # Examples: $2.6 billion, $250 million
    caption = re.sub(
        r'\$(\d[\d,\.]*)\s+(trillion|billion|million|thousand)',
        r'\1 \2 USD',
        caption,
        flags=re.IGNORECASE
    )

    # Pattern 2: $XM, $XB, $XK, $XT (no space, letter suffix)
    # Examples: $30M, $2.5B, $500K
    # Use word boundary to avoid matching first letter of next word
    caption = re.sub(
        r'\$(\d[\d,\.]*)(T|B|M|K)\b',
        r'\1\2 USD',
        caption
    )

    # Pattern 3: Plain $X with no suffix (must be followed by space or punctuation)
    # Examples: $500, $3,500, $41,000
    caption = re.sub(
        r'\$(\d[\d,\.]*)(?=\s|,|\.|\)|$)',
        r'\1 USD',
        caption
    )

    # Clean up any double spaces
    caption = re.sub(r'  +', ' ', caption)

    # Fix percentages: X% → X percent (but not inside words)
    caption = re.sub(r'(\d+(?:\.\d+)?)\s*%', r'\1 percent', caption)

    # Fix ampersand: & → and (but not HTML entities like &amp; &lt; &gt;)
    # Only replace & that's surrounded by spaces or at word boundaries
    caption = re.sub(r'\s+&\s+', ' and ', caption)
    caption = re.sub(r'^&\s+', 'and ', caption)
    caption = re.sub(r'\s+&$', ' and', caption)
    # Also handle R&D specifically
    caption = re.sub(r'R&D', 'R and D', caption)

    return caption


def process_file(filepath: str, dry_run: bool = True) -> int:
    """Process a single file and fix figure captions. Returns number of fixes."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes = 0

    # Pattern for markdown images: ![caption](path)
    pattern = re.compile(r'(!\[)([^\]]*?)(\]\([^)]+\))')

    def replace_caption(match):
        nonlocal fixes
        prefix = match.group(1)  # ![
        caption = match.group(2)  # the caption
        suffix = match.group(3)  # ](path)

        fixed_caption = fix_caption(caption)
        if fixed_caption != caption:
            fixes += 1
            if dry_run:
                print(f"  Line ~{content[:match.start()].count(chr(10)) + 1}:")
                print(f"    - {caption[:70]}...")
                print(f"    + {fixed_caption[:70]}...")
            return prefix + fixed_caption + suffix
        return match.group(0)

    new_content = pattern.sub(replace_caption, content)

    if not dry_run and new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return fixes


def main():
    dry_run = '--apply' not in sys.argv

    if dry_run:
        print("DRY RUN MODE - use --apply to make changes\n")
    else:
        print("APPLYING CHANGES\n")

    # Find all QMD files
    qmd_files = find_files_by_extension(('.qmd',))

    total_fixes = 0
    files_with_fixes = 0

    for filepath in sorted(qmd_files):
        fixes = process_file(filepath, dry_run=dry_run)
        if fixes > 0:
            rel_path = os.path.relpath(filepath)
            print(f"\n{rel_path}: {fixes} fix(es)")
            total_fixes += fixes
            files_with_fixes += 1

    print(f"\n{'Would fix' if dry_run else 'Fixed'} {total_fixes} caption(s) in {files_with_fixes} file(s)")

    if dry_run and total_fixes > 0:
        print("\nRun with --apply to make changes")


if __name__ == '__main__':
    main()
