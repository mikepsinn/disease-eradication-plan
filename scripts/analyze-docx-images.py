#!/usr/bin/env python3
"""Analyze DOCX files for oversized images that cause Word/Kindle errors.

Extracts all images from a DOCX, reports dimensions, DPI, and physical size.
Flags images exceeding configurable thresholds (default: 22 inches for Word,
1600x2560px for Kindle).

Usage:
    python scripts/analyze-docx-images.py [path-to-docx]
    python scripts/analyze-docx-images.py --fix  # resize in-place
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import argparse
import io
import os
import zipfile
from pathlib import Path

from PIL import Image

# Limits
WORD_MAX_INCHES = 22.0
KINDLE_MAX_WIDTH_PX = 1600
KINDLE_MAX_HEIGHT_PX = 2560
KINDLE_MAX_FILE_KB = 127  # flowable content
DEFAULT_DPI = 96  # Word default when no DPI metadata


def get_image_info(img_bytes: bytes, name: str) -> dict:
    """Extract dimension/DPI info from image bytes."""
    try:
        img = Image.open(io.BytesIO(img_bytes))
    except Exception as e:
        return {"name": name, "error": str(e)}

    width_px, height_px = img.size
    dpi_x, dpi_y = img.info.get("dpi", (DEFAULT_DPI, DEFAULT_DPI))

    # Some images report 0 DPI
    if dpi_x == 0:
        dpi_x = DEFAULT_DPI
    if dpi_y == 0:
        dpi_y = DEFAULT_DPI

    width_inches = width_px / dpi_x
    height_inches = height_px / dpi_y
    size_kb = len(img_bytes) / 1024

    return {
        "name": name,
        "format": img.format or "unknown",
        "width_px": width_px,
        "height_px": height_px,
        "dpi_x": round(dpi_x),
        "dpi_y": round(dpi_y),
        "width_inches": round(width_inches, 2),
        "height_inches": round(height_inches, 2),
        "size_kb": round(size_kb, 1),
        "mode": img.mode,
    }


def analyze_docx(docx_path: str) -> list[dict]:
    """Extract and analyze all images from a DOCX file."""
    results = []
    with zipfile.ZipFile(docx_path, "r") as zf:
        for entry in zf.namelist():
            if entry.startswith("word/media/"):
                img_bytes = zf.read(entry)
                info = get_image_info(img_bytes, entry)
                results.append(info)
    return results


def analyze_epub(epub_path: str) -> list[dict]:
    """Extract and analyze all images from an EPUB file."""
    results = []
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tiff"}
    with zipfile.ZipFile(epub_path, "r") as zf:
        for entry in zf.namelist():
            ext = Path(entry).suffix.lower()
            if ext in image_extensions:
                img_bytes = zf.read(entry)
                if ext == ".svg":
                    results.append({
                        "name": entry,
                        "format": "SVG",
                        "size_kb": round(len(img_bytes) / 1024, 1),
                        "note": "SVG - dimensions depend on viewport",
                    })
                else:
                    info = get_image_info(img_bytes, entry)
                    results.append(info)
    return results


def check_issues(info: dict) -> list[str]:
    """Return list of issues for an image."""
    issues = []
    if "error" in info:
        issues.append(f"CORRUPT: {info['error']}")
        return issues

    if info.get("format") == "SVG":
        return issues

    w_in = info.get("width_inches", 0)
    h_in = info.get("height_inches", 0)
    w_px = info.get("width_px", 0)
    h_px = info.get("height_px", 0)
    size_kb = info.get("size_kb", 0)

    if w_in > WORD_MAX_INCHES or h_in > WORD_MAX_INCHES:
        issues.append(f"WORD_OVERSIZE: {w_in}x{h_in} inches (max {WORD_MAX_INCHES})")

    if w_px > KINDLE_MAX_WIDTH_PX:
        issues.append(f"KINDLE_WIDE: {w_px}px (max {KINDLE_MAX_WIDTH_PX})")

    if h_px > KINDLE_MAX_HEIGHT_PX:
        issues.append(f"KINDLE_TALL: {h_px}px (max {KINDLE_MAX_HEIGHT_PX})")

    if size_kb > KINDLE_MAX_FILE_KB:
        issues.append(f"KINDLE_LARGE: {size_kb}KB (max {KINDLE_MAX_FILE_KB}KB)")

    if info.get("dpi_x", DEFAULT_DPI) < 72:
        issues.append(f"LOW_DPI: {info['dpi_x']} (min recommended: 72)")

    return issues


def print_report(results: list[dict], file_path: str):
    """Print analysis report."""
    print(f"\n{'='*80}")
    print(f"Image Analysis: {file_path}")
    print(f"{'='*80}")
    print(f"Total images: {len(results)}")

    all_issues = []
    for info in results:
        issues = check_issues(info)
        if issues:
            all_issues.append((info, issues))

    if not all_issues:
        print("\nAll images are within acceptable limits.")
    else:
        print(f"\nISSUES FOUND: {len(all_issues)} images with problems\n")
        for info, issues in all_issues:
            print(f"  {info['name']}")
            if "error" not in info and info.get("format") != "SVG":
                print(f"    Dimensions: {info['width_px']}x{info['height_px']}px")
                print(f"    DPI: {info['dpi_x']}x{info['dpi_y']}")
                print(f"    Physical: {info['width_inches']}x{info['height_inches']} inches")
                print(f"    File size: {info['size_kb']} KB")
            for issue in issues:
                print(f"    ** {issue}")
            print()

    # Summary table of all images sorted by size
    print(f"\n{'='*80}")
    print("All images (sorted by physical size, largest first):")
    print(f"{'='*80}")
    print(f"{'Name':<50} {'Pixels':<15} {'DPI':<10} {'Inches':<15} {'KB':<8} {'Issues'}")
    print("-" * 120)

    def sort_key(info):
        if "error" in info or info.get("format") == "SVG":
            return 0
        return info.get("width_inches", 0) * info.get("height_inches", 0)

    for info in sorted(results, key=sort_key, reverse=True):
        if "error" in info:
            print(f"  {info['name']:<50} CORRUPT: {info['error']}")
            continue
        if info.get("format") == "SVG":
            print(f"  {info['name']:<50} {'SVG':<15} {'--':<10} {'--':<15} {info['size_kb']:<8}")
            continue

        pixels = f"{info['width_px']}x{info['height_px']}"
        dpi = f"{info['dpi_x']}x{info['dpi_y']}"
        inches = f"{info['width_inches']}x{info['height_inches']}"
        issues = check_issues(info)
        flag = " !! " + "; ".join(issues) if issues else ""
        print(f"  {info['name']:<50} {pixels:<15} {dpi:<10} {inches:<15} {info['size_kb']:<8}{flag}")

    return len(all_issues)


def main():
    parser = argparse.ArgumentParser(description="Analyze images in DOCX/EPUB files")
    parser.add_argument("file", nargs="?", help="Path to DOCX or EPUB file")
    parser.add_argument("--docx-dir", default="assets/docx", help="Directory containing DOCX files")
    parser.add_argument("--epub-dir", default="assets/epubs", help="Directory containing EPUB files")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.parent
    total_issues = 0

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        ext = file_path.suffix.lower()
        if ext == ".docx":
            results = analyze_docx(str(file_path))
        elif ext == ".epub":
            results = analyze_epub(str(file_path))
        else:
            print(f"Error: Unsupported file type: {ext}")
            sys.exit(1)
        total_issues = print_report(results, str(file_path))
    else:
        # Analyze all DOCX and EPUB files in default directories
        for dir_name, analyzer in [
            (args.docx_dir, analyze_docx),
            (args.epub_dir, analyze_epub),
        ]:
            dir_path = script_dir / dir_name
            if not dir_path.exists():
                print(f"Skipping {dir_path} (not found)")
                continue
            for f in sorted(dir_path.iterdir()):
                if f.suffix.lower() in (".docx", ".epub"):
                    results = analyzer(str(f))
                    total_issues += print_report(results, str(f))

    if total_issues > 0:
        print(f"\n** {total_issues} images with issues found. Run fix-epub-kindle.py to fix.")
        sys.exit(1)
    else:
        print("\nAll images pass validation.")
        sys.exit(0)


if __name__ == "__main__":
    main()
