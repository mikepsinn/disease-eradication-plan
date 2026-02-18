#!/usr/bin/env python3
"""Validate EPUB for Kindle Direct Publishing compatibility.

Checks:
- Image dimensions and file sizes
- Total EPUB file size
- XHTML well-formedness
- Required metadata (title, author, language)
- Cover image presence and size
- NCX table of contents
- Chapter file sizes
- Unsupported features (JavaScript, video, audio, SVG fonts)

Usage:
    python scripts/validate-kindle-compat.py assets/epubs/How-to-End-War-and-Disease.epub
    python scripts/validate-kindle-compat.py --strict input.epub
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import io
import os
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

# KDP limits
KINDLE_MAX_WIDTH_PX = 1600
KINDLE_MAX_HEIGHT_PX = 2560
KINDLE_MAX_IMAGE_KB = 127
KINDLE_MAX_COVER_KB = 5000
KINDLE_MAX_TOTAL_MB = 650
KINDLE_MAX_CHAPTER_KB = 260  # recommended max per chapter file
KINDLE_MIN_COVER_WIDTH = 625   # minimum cover width
KINDLE_IDEAL_COVER_WIDTH = 1600
KINDLE_IDEAL_COVER_HEIGHT = 2560
COVER_ASPECT_MIN = 1.33  # height/width ratio
COVER_ASPECT_MAX = 2.0

DEFAULT_DPI = 96


class ValidationResult:
    def __init__(self):
        self.errors = []    # Must fix
        self.warnings = []  # Should fix
        self.info = []      # FYI

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def note(self, msg: str):
        self.info.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


def validate_images(zf: zipfile.ZipFile, result: ValidationResult):
    """Check all images for Kindle compatibility."""
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}
    image_count = 0
    total_image_kb = 0

    for entry in zf.namelist():
        ext = Path(entry).suffix.lower()
        if ext not in image_extensions:
            continue

        image_count += 1
        img_bytes = zf.read(entry)
        size_kb = len(img_bytes) / 1024
        total_image_kb += size_kb
        is_cover = "cover" in entry.lower()

        try:
            img = Image.open(io.BytesIO(img_bytes))
            width, height = img.size
        except Exception as e:
            result.error(f"CORRUPT IMAGE: {entry} - {e}")
            continue

        dpi_x, dpi_y = img.info.get("dpi", (DEFAULT_DPI, DEFAULT_DPI))
        if dpi_x == 0:
            dpi_x = DEFAULT_DPI
        if dpi_y == 0:
            dpi_y = DEFAULT_DPI

        # Fix bogus DPI for calculation (don't modify the actual image here)
        eff_dpi_x = dpi_x if dpi_x >= 72 else DEFAULT_DPI
        eff_dpi_y = dpi_y if dpi_y >= 72 else DEFAULT_DPI
        width_inches = width / eff_dpi_x
        height_inches = height / eff_dpi_y

        # Flag bogus DPI metadata
        if dpi_x < 72 or dpi_y < 72:
            result.error(f"BAD_DPI: {entry} has DPI {dpi_x}x{dpi_y} (min: 72). Effective physical size at {DEFAULT_DPI} DPI: {width_inches:.1f}x{height_inches:.1f} inches")

        # Check physical size (10-inch max for Kindle page fit)
        if width_inches > 10 or height_inches > 10:
            result.error(f"OVERSIZE: {entry} is {width_inches:.1f}x{height_inches:.1f} inches (max: 10 inches). DPI: {eff_dpi_x}x{eff_dpi_y}, Pixels: {width}x{height}")

        # Check pixel dimensions
        if width > KINDLE_MAX_WIDTH_PX:
            result.warn(f"WIDE: {entry} is {width}px wide (Kindle max: {KINDLE_MAX_WIDTH_PX})")
        if height > KINDLE_MAX_HEIGHT_PX:
            result.warn(f"TALL: {entry} is {height}px tall (Kindle max: {KINDLE_MAX_HEIGHT_PX})")

        # Check file size
        max_kb = KINDLE_MAX_COVER_KB if is_cover else KINDLE_MAX_IMAGE_KB
        if size_kb > max_kb:
            result.warn(f"LARGE: {entry} is {size_kb:.1f}KB (Kindle max: {max_kb}KB)")

        # Cover-specific checks
        if is_cover:
            if width < KINDLE_MIN_COVER_WIDTH:
                result.error(f"COVER TOO SMALL: {width}px wide (min: {KINDLE_MIN_COVER_WIDTH}px)")
            aspect = height / width if width > 0 else 0
            if aspect < COVER_ASPECT_MIN or aspect > COVER_ASPECT_MAX:
                result.warn(f"COVER ASPECT: {aspect:.2f} (recommended: {COVER_ASPECT_MIN}-{COVER_ASPECT_MAX})")

    result.note(f"Total images: {image_count}, total image size: {total_image_kb/1024:.2f}MB")


def validate_metadata(zf: zipfile.ZipFile, result: ValidationResult):
    """Check OPF metadata for required fields."""
    opf_path = None
    for entry in zf.namelist():
        if entry.endswith(".opf"):
            opf_path = entry
            break

    if not opf_path:
        result.error("NO OPF: Missing .opf package file")
        return

    try:
        opf_content = zf.read(opf_path).decode("utf-8")
        root = ET.fromstring(opf_content)
    except Exception as e:
        result.error(f"OPF PARSE ERROR: {e}")
        return

    ns = {
        "opf": "http://www.idpf.org/2007/opf",
        "dc": "http://purl.org/dc/elements/1.1/",
    }

    metadata = root.find("opf:metadata", ns) or root.find("metadata")
    if metadata is None:
        # Try without namespace
        for child in root:
            if "metadata" in child.tag.lower():
                metadata = child
                break

    if metadata is None:
        result.error("NO METADATA: Missing <metadata> element in OPF")
        return

    # Check required fields
    has_title = False
    has_author = False
    has_language = False

    for elem in metadata:
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "title" and elem.text:
            has_title = True
            result.note(f"Title: {elem.text.strip()}")
        elif tag == "creator" and elem.text:
            has_author = True
            result.note(f"Author: {elem.text.strip()}")
        elif tag == "language" and elem.text:
            has_language = True
            result.note(f"Language: {elem.text.strip()}")

    if not has_title:
        result.error("MISSING TITLE: No <dc:title> in OPF metadata")
    if not has_author:
        result.warn("MISSING AUTHOR: No <dc:creator> in OPF metadata")
    if not has_language:
        result.error("MISSING LANGUAGE: No <dc:language> in OPF metadata (Kindle requires this)")


def validate_xhtml(zf: zipfile.ZipFile, result: ValidationResult):
    """Check XHTML files for common issues."""
    xhtml_count = 0
    large_chapters = 0

    for entry in zf.namelist():
        ext = Path(entry).suffix.lower()
        if ext not in (".xhtml", ".html", ".htm"):
            continue

        xhtml_count += 1
        content = zf.read(entry)
        size_kb = len(content) / 1024

        if size_kb > KINDLE_MAX_CHAPTER_KB:
            result.warn(f"LARGE CHAPTER: {entry} is {size_kb:.1f}KB (recommended max: {KINDLE_MAX_CHAPTER_KB}KB)")
            large_chapters += 1

        text = content.decode("utf-8", errors="replace")

        # Check for JavaScript
        if re.search(r'<script', text, re.IGNORECASE):
            result.warn(f"JAVASCRIPT: {entry} contains <script> tags (Kindle strips these)")

        # Check for video/audio
        if re.search(r'<(video|audio)', text, re.IGNORECASE):
            result.warn(f"MEDIA: {entry} contains <video> or <audio> tags (not supported on basic Kindle)")

        # Check for unclosed tags
        if re.search(r'<br(?!\s*/)', text):
            result.warn(f"XHTML: {entry} has unclosed <br> tags (should be <br/>)")
        if re.search(r'<hr(?!\s*/)', text):
            result.warn(f"XHTML: {entry} has unclosed <hr> tags (should be <hr/>)")
        if re.search(r'<img(?![^>]*/)', text):
            result.warn(f"XHTML: {entry} has unclosed <img> tags (should be self-closing)")

    result.note(f"Total XHTML files: {xhtml_count}")
    if large_chapters:
        result.note(f"Large chapters (>{KINDLE_MAX_CHAPTER_KB}KB): {large_chapters}")


def validate_structure(zf: zipfile.ZipFile, result: ValidationResult):
    """Check EPUB structure."""
    names = zf.namelist()

    # Check mimetype
    if "mimetype" not in names:
        result.error("MISSING MIMETYPE: No mimetype file in EPUB")
    elif names[0] != "mimetype":
        result.warn("MIMETYPE ORDER: mimetype should be the first file in the archive")

    # Check for NCX (required for Kindle)
    has_ncx = any(n.endswith(".ncx") for n in names)
    if not has_ncx:
        result.warn("NO NCX: Missing .ncx navigation file (required for older Kindle devices)")

    # Check for nav.xhtml (EPUB3)
    has_nav = any("nav" in n.lower() and n.endswith((".xhtml", ".html")) for n in names)
    if not has_nav:
        result.note("No nav.xhtml found (EPUB3 navigation)")

    # Check total file size
    total_size_mb = os.path.getsize(zf.filename) / (1024 * 1024) if zf.filename else 0
    result.note(f"Total EPUB size: {total_size_mb:.2f}MB")
    if total_size_mb > KINDLE_MAX_TOTAL_MB:
        result.error(f"TOO LARGE: EPUB is {total_size_mb:.1f}MB (Kindle max: {KINDLE_MAX_TOTAL_MB}MB)")

    # Check for SVG
    svg_count = sum(1 for n in names if n.endswith(".svg"))
    if svg_count > 0:
        result.note(f"SVG files: {svg_count} (Kindle has limited SVG support)")


def validate_epub(epub_path: str, strict: bool = False) -> ValidationResult:
    """Run all validation checks on an EPUB file."""
    result = ValidationResult()

    if not os.path.exists(epub_path):
        result.error(f"File not found: {epub_path}")
        return result

    try:
        with zipfile.ZipFile(epub_path, "r") as zf:
            validate_structure(zf, result)
            validate_metadata(zf, result)
            validate_images(zf, result)
            validate_xhtml(zf, result)
    except zipfile.BadZipFile:
        result.error(f"CORRUPT EPUB: {epub_path} is not a valid ZIP file")
    except Exception as e:
        result.error(f"UNEXPECTED ERROR: {e}")

    # In strict mode, warnings become errors
    if strict:
        result.errors.extend(result.warnings)
        result.warnings = []

    return result


def print_results(result: ValidationResult, epub_path: str):
    """Print validation results."""
    print(f"\n{'='*80}")
    print(f"Kindle Compatibility Validation: {epub_path}")
    print(f"{'='*80}")

    status = "PASS" if result.passed else "FAIL"
    print(f"\nResult: {status}")

    if result.errors:
        print(f"\nERRORS ({len(result.errors)}) - must fix before uploading to KDP:")
        for e in result.errors:
            print(f"  [ERROR] {e}")

    if result.warnings:
        print(f"\nWARNINGS ({len(result.warnings)}) - recommended fixes:")
        for w in result.warnings:
            print(f"  [WARN]  {w}")

    if result.info:
        print(f"\nINFO:")
        for i in result.info:
            print(f"  [INFO]  {i}")

    if not result.passed:
        print(f"\nRun 'python scripts/fix-epub-kindle.py {epub_path}' to auto-fix image issues.")

    return result.passed


def main():
    parser = argparse.ArgumentParser(description="Validate EPUB for Kindle compatibility")
    parser.add_argument("epub", help="Path to EPUB file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    result = validate_epub(args.epub, strict=args.strict)
    passed = print_results(result, args.epub)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
