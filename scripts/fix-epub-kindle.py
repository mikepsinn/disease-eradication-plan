#!/usr/bin/env python3
"""Post-process EPUB for valid XHTML and correct OPF metadata.

Fixes issues that cause epubcheck errors and KDP rejections:
- Unclosed <br>, <hr>, <img> tags (must be self-closing in XHTML)
- <script> tags (unsupported by e-readers, can cause validation errors)
- Wrong media-type in OPF manifest (e.g., .jpg declared as image/png)

Usage:
    python scripts/fix-epub-kindle.py assets/epubs/How-to-End-War-and-Disease.epub
    python scripts/fix-epub-kindle.py input.epub --dry-run
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import os
import re
import zipfile
from pathlib import Path

# Map file extensions to correct MIME types
MEDIA_TYPE_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}


def fix_xhtml_content(content: bytes) -> tuple[bytes, list[str]]:
    """Fix common XHTML issues in EPUB chapter files."""
    fixes = []
    text = content.decode("utf-8", errors="replace")

    if "<br>" in text:
        text = text.replace("<br>", "<br/>")
        fixes.append("Fixed unclosed <br> tags")

    if "<hr>" in text:
        text = text.replace("<hr>", "<hr/>")
        fixes.append("Fixed unclosed <hr> tags")

    img_pattern = re.compile(r'<img([^>]*[^/])>')
    if img_pattern.search(text):
        text = img_pattern.sub(r'<img\1/>', text)
        fixes.append("Fixed unclosed <img> tags")

    script_pattern = re.compile(r'<script[^>]*>.*?</script>', re.DOTALL)
    if script_pattern.search(text):
        text = script_pattern.sub('', text)
        fixes.append("Removed <script> tags")

    return text.encode("utf-8"), fixes


def fix_opf_media_types(content: bytes) -> tuple[bytes, list[str]]:
    """Fix incorrect media-type declarations in OPF manifest.

    Pandoc sometimes declares .jpg files as image/png. This corrects
    the media-type based on the actual file extension in the href.
    """
    fixes = []
    text = content.decode("utf-8", errors="replace")

    def fix_item(match: re.Match) -> str:
        full = match.group(0)
        href = match.group(1)
        declared_type = match.group(2)

        ext = Path(href).suffix.lower()
        correct_type = MEDIA_TYPE_MAP.get(ext)

        if correct_type and correct_type != declared_type:
            fixes.append(f"{href}: {declared_type} -> {correct_type}")
            return full.replace(f'media-type="{declared_type}"', f'media-type="{correct_type}"')
        return full

    # Match <item ... href="..." ... media-type="..." ... />
    text = re.sub(
        r'<item[^>]*href="([^"]*)"[^>]*media-type="([^"]*)"[^>]*/?>',
        fix_item,
        text,
    )

    return text.encode("utf-8"), fixes


def process_epub(epub_path: str, dry_run: bool = False) -> dict:
    """Process an EPUB file, applying fixes in-place.

    Returns a summary dict of all changes made.
    """
    summary = {
        "xhtml_fixed": 0,
        "opf_media_fixed": 0,
        "changes": [],
    }

    xhtml_extensions = {".xhtml", ".html", ".htm"}

    if dry_run:
        with zipfile.ZipFile(epub_path, "r") as zf:
            for entry in zf.namelist():
                ext = Path(entry).suffix.lower()
                if ext in xhtml_extensions:
                    data = zf.read(entry)
                    _, fixes = fix_xhtml_content(data)
                    if fixes:
                        summary["xhtml_fixed"] += 1
                        summary["changes"].append({"file": entry, "xhtml_fixes": fixes})
                elif ext == ".opf":
                    data = zf.read(entry)
                    _, fixes = fix_opf_media_types(data)
                    if fixes:
                        summary["opf_media_fixed"] = len(fixes)
                        summary["changes"].append({"file": entry, "opf_fixes": fixes})
        return summary

    # Rewrite EPUB with fixes applied
    temp_path = epub_path + ".tmp"

    with zipfile.ZipFile(epub_path, "r") as zf_in:
        with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zf_out:
            for entry in zf_in.namelist():
                # mimetype must be first and uncompressed
                if entry == "mimetype":
                    zf_out.writestr(entry, zf_in.read(entry), compress_type=zipfile.ZIP_STORED)
                    continue

                ext = Path(entry).suffix.lower()
                data = zf_in.read(entry)

                if ext in xhtml_extensions:
                    data, fixes = fix_xhtml_content(data)
                    if fixes:
                        summary["xhtml_fixed"] += 1
                        summary["changes"].append({"file": entry, "xhtml_fixes": fixes})
                elif ext == ".opf":
                    data, fixes = fix_opf_media_types(data)
                    if fixes:
                        summary["opf_media_fixed"] = len(fixes)
                        summary["changes"].append({"file": entry, "opf_fixes": fixes})

                zf_out.writestr(entry, data)

    os.replace(temp_path, epub_path)
    return summary


def print_summary(summary: dict, file_path: str):
    """Print processing summary."""
    print(f"\n{'='*80}")
    print(f"EPUB Fix: {file_path}")
    print(f"{'='*80}")

    if not summary["changes"]:
        print("No changes needed - EPUB is already valid.")
        return

    if summary["xhtml_fixed"]:
        print(f"\nXHTML files fixed: {summary['xhtml_fixed']}")
    if summary["opf_media_fixed"]:
        print(f"OPF media-type fixes: {summary['opf_media_fixed']}")

    for change in summary["changes"]:
        file = change["file"]
        if "xhtml_fixes" in change:
            print(f"  {file}: {', '.join(change['xhtml_fixes'])}")
        if "opf_fixes" in change:
            for fix in change["opf_fixes"]:
                print(f"  {fix}")


def main():
    parser = argparse.ArgumentParser(description="Fix EPUB for e-reader compatibility")
    parser.add_argument("epub", help="Path to EPUB file")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would change without modifying")
    args = parser.parse_args()

    epub_path = args.epub
    if not os.path.exists(epub_path):
        print(f"Error: File not found: {epub_path}")
        sys.exit(1)

    if args.dry_run:
        print(f"DRY RUN - analyzing {epub_path}")

    summary = process_epub(epub_path, dry_run=args.dry_run)
    print_summary(summary, epub_path)

    if summary["changes"] and args.dry_run:
        print(f"\nRun without --dry-run to apply these fixes.")


if __name__ == "__main__":
    main()
