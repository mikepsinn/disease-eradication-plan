#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rename Long Paths
=================

Renames directories and files with long names to shorter versions,
and updates all references in QMD/MD files.

Usage:
    python scripts/rename-long-paths.py [--dry-run]
"""

import re
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')


# Define renaming rules: old_name -> new_name
RENAMES = {
    "personal-lifetime-wealth-calc": "personal-lifetime-wealth-calc",
}


def find_project_root() -> Path:
    """Find the project root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "package.json").exists() or (current / "_quarto-manual.yml").exists():
            return current
        current = current.parent
    return Path.cwd()


def rename_files_and_dirs(project_root: Path, dry_run: bool = False) -> dict:
    """
    Rename directories and files matching the rename rules.

    Returns:
        Dict mapping old paths to new paths (relative to project root)
    """
    renames_made = {}

    for old_name, new_name in RENAMES.items():
        # Find directories with the old name
        for old_dir in project_root.rglob(old_name):
            if not old_dir.is_dir():
                continue
            if "_build_temp" in str(old_dir) or ".git" in str(old_dir):
                continue

            new_dir = old_dir.parent / new_name
            rel_old = old_dir.relative_to(project_root)
            rel_new = new_dir.relative_to(project_root)

            print(f"[DIR] {rel_old}")
            print(f"  ->  {rel_new}")

            if not dry_run:
                old_dir.rename(new_dir)

            renames_made[str(rel_old)] = str(rel_new)

            # Now rename files inside that have the old name as prefix
            search_dir = new_dir if not dry_run else old_dir
            for old_file in search_dir.iterdir():
                if not old_file.is_file():
                    continue
                if old_name not in old_file.name:
                    continue

                new_filename = old_file.name.replace(old_name, new_name)
                new_file = old_file.parent / new_filename

                # Calculate relative paths for the mapping
                if dry_run:
                    rel_old_file = str(old_file.relative_to(project_root))
                    rel_new_file = str(rel_new / new_filename)
                else:
                    rel_old_file = str(Path(str(rel_old)) / old_file.name.replace(new_name, old_name))
                    rel_new_file = str(new_file.relative_to(project_root))

                print(f"  [FILE] {old_file.name}")
                print(f"      -> {new_filename}")

                if not dry_run:
                    old_file.rename(new_file)

                renames_made[rel_old_file] = rel_new_file

    return renames_made


def update_references(project_root: Path, renames: dict, dry_run: bool = False) -> int:
    """
    Update references to renamed files in QMD/MD files.

    Returns:
        Number of files modified
    """
    files_modified = 0

    # Build regex patterns for all renames
    patterns = []
    for old_path, new_path in renames.items():
        # Match the old path in various forms (with different path separators)
        old_normalized = old_path.replace("\\", "/")
        new_normalized = new_path.replace("\\", "/")
        patterns.append((old_normalized, new_normalized))

        # Also match just the filename
        old_filename = Path(old_path).name
        new_filename = Path(new_path).name
        if old_filename != new_filename:
            patterns.append((old_filename, new_filename))

    # Also add the base directory/name replacements
    for old_name, new_name in RENAMES.items():
        patterns.append((old_name, new_name))

    # Remove duplicates while preserving order
    seen = set()
    unique_patterns = []
    for p in patterns:
        if p not in seen:
            seen.add(p)
            unique_patterns.append(p)
    patterns = unique_patterns

    # Find all QMD and MD files
    for ext in ["*.qmd", "*.md"]:
        for file_path in project_root.rglob(ext):
            if "_build_temp" in str(file_path) or ".git" in str(file_path):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"[WARN] Could not read {file_path}: {e}")
                continue

            original = content

            # Apply all replacements
            for old_pattern, new_pattern in patterns:
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)

            if content != original:
                rel_path = file_path.relative_to(project_root)
                print(f"[UPDATE] {rel_path}")

                if not dry_run:
                    file_path.write_text(content, encoding="utf-8")

                files_modified += 1

    return files_modified


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Rename long paths and update references")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()

    project_root = find_project_root()
    print(f"Project root: {project_root}\n")

    if args.dry_run:
        print("=== DRY RUN MODE ===\n")

    # Step 1: Rename files and directories
    print("=" * 60)
    print("RENAMING FILES AND DIRECTORIES")
    print("=" * 60)

    renames = rename_files_and_dirs(project_root, dry_run=args.dry_run)

    print(f"\nRenamed {len(renames)} items\n")

    # Step 2: Update references in QMD/MD files
    print("=" * 60)
    print("UPDATING REFERENCES IN QMD/MD FILES")
    print("=" * 60)

    files_modified = update_references(project_root, renames, dry_run=args.dry_run)

    print(f"\nModified {files_modified} files\n")

    # Summary
    print("=" * 60)
    if args.dry_run:
        print(f"DRY RUN: Would rename {len(renames)} items and modify {files_modified} files")
    else:
        print(f"DONE: Renamed {len(renames)} items and modified {files_modified} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
