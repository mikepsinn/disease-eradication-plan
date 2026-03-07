#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate audiobook files: strip numeric index prefix from filenames.

Renames files like:
    005-nih-fails-2-institute-health.wav  ->  nih-fails-2-institute-health.wav
    005-nih-fails-2-institute-health.prepared.txt  ->  nih-fails-2-institute-health.prepared.txt
    005-nih-fails-2-institute-health/  ->  nih-fails-2-institute-health/

Run with --dry-run to preview changes.

Usage:
    python scripts/migrate_strip_index_prefix.py --dry-run
    python scripts/migrate_strip_index_prefix.py
"""
import re
import sys
import argparse
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

PROJECT_ROOT = Path(__file__).parent.parent
AUDIOBOOK_DIR = PROJECT_ROOT / "assets" / "audiobook"

# Pattern: 3+ digit prefix followed by a dash (e.g. "001-", "034-")
INDEX_PREFIX = re.compile(r'^\d{3,}-')


def strip_prefix(name: str) -> str | None:
    """Strip numeric index prefix from a filename. Returns None if no prefix."""
    new_name = INDEX_PREFIX.sub('', name)
    return new_name if new_name != name else None


def migrate_directory(directory: Path, dry_run: bool) -> int:
    """Rename all index-prefixed files and directories in a directory. Returns count."""
    if not directory.exists():
        return 0

    count = 0

    # First pass: rename files
    for item in sorted(directory.iterdir()):
        if item.is_file():
            new_name = strip_prefix(item.name)
            if new_name:
                new_path = item.parent / new_name
                if new_path.exists():
                    print(f"  [SKIP] {item.name} -> {new_name} (target exists)")
                    continue
                print(f"  {item.name} -> {new_name}")
                if not dry_run:
                    item.rename(new_path)
                count += 1

    # Second pass: rename directories
    for item in sorted(directory.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            new_name = strip_prefix(item.name)
            if new_name:
                new_path = item.parent / new_name
                if new_path.exists():
                    print(f"  [SKIP] {item.name}/ -> {new_name}/ (target exists)")
                    continue
                print(f"  {item.name}/ -> {new_name}/")
                if not dry_run:
                    item.rename(new_path)
                count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description="Strip index prefixes from audiobook filenames")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview changes without renaming")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN - no files will be renamed\n")

    total = 0

    # Walk all config subdirectories under assets/audiobook/
    for config_dir in sorted(AUDIOBOOK_DIR.iterdir()):
        if not config_dir.is_dir() or config_dir.name.startswith('.'):
            continue

        print(f"\n{'=' * 60}")
        print(f"Config: {config_dir.name}")
        print(f"{'=' * 60}")

        # Directories to scan for index-prefixed files
        subdirs = [
            "narration-txt-chapters",
            "narration-txt-chunks",
            "wavs",
            "wavs/audio-chunks",
            "alignment",
            "subtitles",
            "mp3",
            "video",
            "video/scenes",
        ]

        for subdir_name in subdirs:
            subdir = config_dir / subdir_name
            if not subdir.exists():
                continue
            print(f"\n  [{subdir_name}]")
            count = migrate_directory(subdir, args.dry_run)
            total += count

            # For chunks and audio-chunks, also rename inside subdirectories
            if subdir_name in ("narration-txt-chunks", "wavs/audio-chunks", "video/scenes"):
                for nested_dir in sorted(subdir.iterdir()):
                    if nested_dir.is_dir():
                        # The nested dir itself was already renamed above if needed
                        # Now check if there are index-prefixed files inside
                        pass

    print(f"\n{'=' * 60}")
    action = "Would rename" if args.dry_run else "Renamed"
    print(f"{action} {total} files/directories")
    if args.dry_run and total > 0:
        print(f"\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
