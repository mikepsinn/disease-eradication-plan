#!/usr/bin/env python3
"""
Seed feed-date into chapter QMD frontmatter using git last-modified dates.

Reads chapter list from _quarto-manual.yml, gets each file's last git
commit date, and inserts `feed-date: YYYY-MM-DD` into the YAML frontmatter.

Skips files that already have a feed-date field.

Usage:
    python scripts/seed-feed-dates.py
    python scripts/seed-feed-dates.py --dry-run
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

from dih_models.yaml_utils import load_quarto_config


def get_git_date(file_path: Path) -> str:
    """Get the last git commit date for a file as YYYY-MM-DD."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%aI", "--", str(file_path)],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return ""
    # Parse ISO date: 2026-03-01T14:30:00-05:00 -> 2026-03-01
    return result.stdout.strip()[:10]


def extract_chapters(config):
    """Extract all chapter .qmd paths from a Quarto book config."""
    chapters = []
    book = config.get("book", {})

    def walk(items):
        if not items:
            return
        for item in items:
            if isinstance(item, str):
                if item.endswith(".qmd"):
                    chapters.append(item)
            elif isinstance(item, dict):
                if "href" in item and item["href"].endswith(".qmd"):
                    chapters.append(item["href"])
                walk(item.get("chapters", []))
                walk(item.get("contents", []))

    walk(book.get("chapters", []))
    return chapters


def add_feed_date(qmd_path: Path, date_str: str, dry_run: bool) -> bool:
    """Add feed-date to frontmatter. Returns True if modified."""
    text = qmd_path.read_text(encoding="utf-8")

    # Check if already has feed-date
    if re.search(r"^feed-date\s*:", text, re.MULTILINE):
        return False

    # Find the closing --- of frontmatter
    match = re.match(r"(^---\s*\n)(.*?\n)(---)", text, re.DOTALL)
    if not match:
        print(f"  [SKIP] No frontmatter: {qmd_path.name}")
        return False

    # Insert feed-date before closing ---
    new_text = f"{match.group(1)}{match.group(2)}feed-date: \"{date_str}\"\n{match.group(3)}{text[match.end():]}"

    if dry_run:
        print(f"  [DRY] {qmd_path.name} -> feed-date: {date_str}")
    else:
        qmd_path.write_text(new_text, encoding="utf-8", newline="\n")
        print(f"  [OK]  {qmd_path.name} -> feed-date: {date_str}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Seed feed-date into chapter QMD files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without modifying files")
    args = parser.parse_args()

    config = load_quarto_config(PROJECT_ROOT / "_quarto-manual.yml")
    chapter_paths = extract_chapters(config)

    print(f"Found {len(chapter_paths)} chapters in _quarto-manual.yml")
    if args.dry_run:
        print("(dry run - no files will be modified)\n")

    modified = 0
    skipped = 0

    for rel_path in chapter_paths:
        qmd_path = PROJECT_ROOT / rel_path
        if not qmd_path.exists():
            print(f"  [MISS] {rel_path}")
            continue

        git_date = get_git_date(qmd_path)
        if not git_date:
            print(f"  [SKIP] No git history: {rel_path}")
            continue

        if add_feed_date(qmd_path, git_date, args.dry_run):
            modified += 1
        else:
            skipped += 1

    print(f"\nDone: {modified} modified, {skipped} already had feed-date")


if __name__ == "__main__":
    main()
