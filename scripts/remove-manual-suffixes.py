#!/usr/bin/env python3
"""
Remove manual M/K/B suffixes from Quarto variable shortcodes
==========================================================

Removes manual suffixes since the formatter now adds them automatically:
- {{< var param_millions >}}M → {{< var param_millions >}}
- {{< var param_thousands >}}K → {{< var param_thousands >}}
- {{< var param_billions >}}B → {{< var param_billions >}}

Usage:
    python tools/remove-manual-suffixes.py
"""

import re
from pathlib import Path
from typing import List, Tuple


def find_manual_suffixes(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Find all manual suffixes in a file.

    Returns list of (line_num, old_line, new_line) tuples.
    """
    changes = []

    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        # Pattern: {{< var param_name_millions >}}M (and similar for K, B)
        # Match and capture the variable reference and the manual suffix
        pattern = r"(\{\{<\s*var\s+\w*_(?:millions|thousands|billions)\s*>\}\})(M|K|B)"

        matches = re.finditer(pattern, line)
        new_line = line

        for match in matches:
            var_ref = match.group(1)  # {{< var param_name_millions >}}
            suffix = match.group(2)  # M, K, or B

            # Only remove suffix if it matches the parameter name
            # millions → M, thousands → K, billions → B
            param_type = None
            if "_millions" in var_ref.lower():
                param_type = "M"
            elif "_thousands" in var_ref.lower():
                param_type = "K"
            elif "_billions" in var_ref.lower():
                param_type = "B"

            # Only remove if suffix matches parameter type
            if suffix == param_type:
                old_text = match.group(0)  # Full match with suffix
                new_text = var_ref  # Just the variable reference
                new_line = new_line.replace(old_text, new_text, 1)

        # If line changed, record it
        if new_line != line:
            changes.append((i, line, new_line))

    return changes


def remove_suffixes_from_file(file_path: Path, dry_run: bool = False) -> int:
    """
    Remove all manual suffixes from a file.

    Returns number of lines changed.
    """
    changes = find_manual_suffixes(file_path)

    if not changes:
        return 0

    if dry_run:
        print(f"\n[DRY RUN] {file_path}:")
        for line_num, old_line, new_line in changes:
            print(f"  Line {line_num}:")
            print(f"    - {old_line.rstrip()}")
            print(f"    + {new_line.rstrip()}")
        return len(changes)

    # Read all lines
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    # Apply changes
    for line_num, old_line, new_line in changes:
        lines[line_num - 1] = new_line

    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[FIXED] {file_path}: {len(changes)} lines updated")
    return len(changes)


def main():
    project_root = Path(__file__).parent.parent.absolute()
    knowledge_dir = project_root / "knowledge"

    # Find all QMD files
    qmd_files = list(knowledge_dir.rglob("*.qmd"))

    print(f"[*] Scanning {len(qmd_files)} QMD files for manual suffixes...\n")

    # First pass: dry run to show what will change
    total_changes = 0
    files_to_fix = []

    for qmd_file in sorted(qmd_files):
        changes = find_manual_suffixes(qmd_file)
        if changes:
            files_to_fix.append((qmd_file, len(changes)))
            total_changes += len(changes)

    if not files_to_fix:
        print("[OK] No manual suffixes found!")
        return

    print(f"[!] Found {total_changes} manual suffixes in {len(files_to_fix)} files:\n")
    for file_path, count in files_to_fix:
        rel_path = file_path.relative_to(project_root)
        print(f"  {rel_path}: {count} changes")

    # Second pass: actually remove suffixes
    print("\n[*] Removing manual suffixes...\n")

    total_fixed = 0
    for qmd_file in sorted(qmd_files):
        fixed = remove_suffixes_from_file(qmd_file, dry_run=False)
        total_fixed += fixed

    print(f"\n[OK] Removed {total_fixed} manual suffixes from {len(files_to_fix)} files")
    print("\n[*] Next steps:")
    print("    1. Review changes with: git diff")
    print("    2. Render documents to verify formatting")


if __name__ == "__main__":
    main()
