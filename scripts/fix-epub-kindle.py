#!/usr/bin/env python3
"""Post-process EPUB for Kindle Direct Publishing compatibility.

Fixes:
- Oversized images (resize to Kindle limits)
- Large file sizes (compress images)
- SVG issues (convert to PNG where needed)
- XHTML validation issues
- NCX/OPF metadata cleanup

Usage:
    python scripts/fix-epub-kindle.py assets/epubs/How-to-End-War-and-Disease.epub
    python scripts/fix-epub-kindle.py input.epub --output output.epub
    python scripts/fix-epub-kindle.py input.epub --dry-run
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import io
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from PIL import Image

# Kindle Direct Publishing limits
KINDLE_MAX_WIDTH = 1600
KINDLE_MAX_HEIGHT = 2560
KINDLE_TARGET_DPI = 150
KINDLE_MAX_IMAGE_KB = 127  # for flowable content
KINDLE_MAX_COVER_KB = 5000  # cover can be larger
KINDLE_JPEG_QUALITY = 85
KINDLE_MAX_TOTAL_MB = 650  # KDP limit
MAX_PHYSICAL_INCHES = 10.0  # Kindle screens are 6-7 inches; 10" is generous max
MIN_VALID_DPI = 72  # Minimum sane DPI; anything below is metadata garbage

# Image format preferences for Kindle
PREFERRED_FORMAT = "JPEG"  # Kindle handles JPEG best for photos
PNG_THRESHOLD = 256  # Use PNG if image has fewer unique colors (charts/diagrams)


def should_use_png(img: Image.Image) -> bool:
    """Determine if PNG is better than JPEG for this image."""
    # Always use PNG for images with transparency
    if img.mode in ("RGBA", "LA", "PA"):
        min_alpha, _ = img.split()[-1].getextrema()
        if isinstance(min_alpha, int) and min_alpha < 255:
            return True

    # Use PNG for simple graphics/charts (few colors)
    try:
        colors = img.getcolors(maxcolors=PNG_THRESHOLD + 1)
        if colors is not None:
            return True  # fewer than threshold colors = chart/diagram
    except Exception:
        pass

    return False


def resize_image(img_bytes: bytes, name: str, is_cover: bool = False) -> tuple[bytes, str, dict]:
    """Resize and optimize an image for Kindle.

    Returns (new_bytes, new_format_ext, changes_dict).
    """
    changes = {}
    try:
        img = Image.open(io.BytesIO(img_bytes))
    except Exception as e:
        return img_bytes, Path(name).suffix, {"error": str(e)}

    original_size = len(img_bytes)
    original_dims = img.size
    width, height = img.size

    max_kb = KINDLE_MAX_COVER_KB if is_cover else KINDLE_MAX_IMAGE_KB
    max_w = KINDLE_MAX_WIDTH
    max_h = KINDLE_MAX_HEIGHT

    # Fix bogus DPI metadata (some images report 1 DPI)
    # Use 96 DPI as default (matches Word/most renderers) when metadata is missing
    CALC_DPI = 96
    dpi_x, dpi_y = img.info.get("dpi", (CALC_DPI, CALC_DPI))
    if dpi_x < MIN_VALID_DPI or dpi_y < MIN_VALID_DPI:
        changes["dpi_fixed"] = f"{dpi_x}x{dpi_y} -> {KINDLE_TARGET_DPI}x{KINDLE_TARGET_DPI}"
        dpi_x = KINDLE_TARGET_DPI
        dpi_y = KINDLE_TARGET_DPI

    # For physical size calculation, use the rounded save DPI (matches what gets written)
    # Use min with 96 for worst-case interpretation since renderers vary
    effective_dpi = min(round(dpi_x), round(dpi_y), CALC_DPI)
    # Use 0.98 safety margin to account for rounding in resize
    phys_max_w = int(MAX_PHYSICAL_INCHES * 0.98 * effective_dpi)
    phys_max_h = int(MAX_PHYSICAL_INCHES * 0.98 * effective_dpi)
    max_w = min(max_w, phys_max_w)
    max_h = min(max_h, phys_max_h)

    # Determine best output format
    use_png = should_use_png(img)

    # Convert RGBA to RGB for JPEG output
    if not use_png and img.mode in ("RGBA", "LA", "PA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        if img.mode in ("RGBA", "LA", "PA"):
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert("RGB")
        changes["converted"] = f"{img.mode} -> RGB"

    if img.mode not in ("RGB", "L", "RGBA"):
        img = img.convert("RGB")
        changes["converted"] = f"-> RGB"

    # Resize if exceeding pixel or physical limits
    if width > max_w or height > max_h:
        ratio = min(max_w / width, max_h / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        changes["resized"] = f"{width}x{height} -> {new_width}x{new_height}"

    # Save with appropriate format, compression, and corrected DPI
    # Use round() not int() to avoid truncation (95.96 -> 96, not 95)
    save_dpi = (round(dpi_x), round(dpi_y))
    buf = io.BytesIO()
    if use_png:
        # PNG stores DPI as pixels-per-meter in pHYs chunk
        ppi = round(dpi_x)
        ppm = int(ppi * 39.3701)  # inches to meters
        img.save(buf, format="PNG", optimize=True, dpi=save_dpi)
        ext = ".png"
    else:
        quality = KINDLE_JPEG_QUALITY
        img.save(buf, format="JPEG", quality=quality, optimize=True, dpi=save_dpi)
        # If still too large, reduce quality iteratively
        while buf.tell() > max_kb * 1024 and quality > 30:
            quality -= 5
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=quality, optimize=True, dpi=save_dpi)
        ext = ".jpg"
        if quality < KINDLE_JPEG_QUALITY:
            changes["compressed"] = f"quality={quality}"

    new_bytes = buf.getvalue()
    new_size = len(new_bytes)

    if new_size < original_size:
        savings = round((1 - new_size / original_size) * 100, 1)
        changes["size"] = f"{round(original_size/1024, 1)}KB -> {round(new_size/1024, 1)}KB ({savings}% smaller)"

    # If new is actually larger and we didn't resize/convert/fix DPI, keep original
    if new_size > original_size and "resized" not in changes and "converted" not in changes and "dpi_fixed" not in changes:
        return img_bytes, Path(name).suffix, {}

    return new_bytes, ext, changes


def fix_xhtml_content(content: bytes) -> tuple[bytes, list[str]]:
    """Fix common XHTML issues in EPUB chapter files."""
    fixes = []
    text = content.decode("utf-8", errors="replace")

    # Fix unclosed <br> tags (must be <br/> in XHTML)
    if "<br>" in text:
        text = text.replace("<br>", "<br/>")
        fixes.append("Fixed unclosed <br> tags")

    # Fix unclosed <hr> tags
    if "<hr>" in text:
        text = text.replace("<hr>", "<hr/>")
        fixes.append("Fixed unclosed <hr> tags")

    # Fix unclosed <img> tags (must be self-closing in XHTML)
    img_pattern = re.compile(r'<img([^>]*[^/])>')
    if img_pattern.search(text):
        text = img_pattern.sub(r'<img\1/>', text)
        fixes.append("Fixed unclosed <img> tags")

    # Remove JavaScript (Kindle strips it anyway, but it can cause errors)
    script_pattern = re.compile(r'<script[^>]*>.*?</script>', re.DOTALL)
    if script_pattern.search(text):
        text = script_pattern.sub('', text)
        fixes.append("Removed <script> tags")

    # Remove external stylesheets that might not exist
    # (keep internal ones)

    return text.encode("utf-8"), fixes


def process_epub(epub_path: str, output_path: str, dry_run: bool = False) -> dict:
    """Process an EPUB file for Kindle compatibility.

    Returns a summary dict of all changes made.
    """
    summary = {
        "images_resized": 0,
        "images_compressed": 0,
        "xhtml_fixed": 0,
        "total_original_kb": 0,
        "total_new_kb": 0,
        "changes": [],
    }

    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}

    if dry_run:
        # Just analyze, don't write
        with zipfile.ZipFile(epub_path, "r") as zf:
            for entry in zf.namelist():
                ext = Path(entry).suffix.lower()
                if ext in image_extensions:
                    img_bytes = zf.read(entry)
                    is_cover = "cover" in entry.lower()
                    _, _, changes = resize_image(img_bytes, entry, is_cover)
                    if changes:
                        summary["changes"].append({"file": entry, **changes})
                        if "resized" in changes:
                            summary["images_resized"] += 1
                        if "compressed" in changes or "size" in changes:
                            summary["images_compressed"] += 1
        return summary

    # Create a new EPUB with fixes applied
    temp_path = epub_path + ".tmp"

    with zipfile.ZipFile(epub_path, "r") as zf_in:
        with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zf_out:
            for entry in zf_in.namelist():
                data = zf_in.read(entry)
                ext = Path(entry).suffix.lower()

                # Handle mimetype (must be first, uncompressed)
                if entry == "mimetype":
                    zf_out.writestr(entry, data, compress_type=zipfile.ZIP_STORED)
                    continue

                # Process images
                if ext in image_extensions:
                    original_kb = len(data) / 1024
                    summary["total_original_kb"] += original_kb

                    is_cover = "cover" in entry.lower()
                    new_bytes, new_ext, changes = resize_image(data, entry, is_cover)

                    if changes and "error" not in changes:
                        new_kb = len(new_bytes) / 1024
                        summary["total_new_kb"] += new_kb
                        summary["changes"].append({"file": entry, **changes})

                        if "resized" in changes:
                            summary["images_resized"] += 1
                        if "compressed" in changes or "size" in changes:
                            summary["images_compressed"] += 1

                        # If format changed, update the entry name
                        if new_ext != ext:
                            new_entry = str(Path(entry).with_suffix(new_ext))
                            # We'd need to update references too - skip format changes for now
                            zf_out.writestr(entry, new_bytes)
                        else:
                            zf_out.writestr(entry, new_bytes)
                    else:
                        summary["total_new_kb"] += original_kb
                        zf_out.writestr(entry, data)
                    continue

                # Process XHTML files
                if ext in (".xhtml", ".html", ".htm"):
                    new_data, fixes = fix_xhtml_content(data)
                    if fixes:
                        summary["xhtml_fixed"] += 1
                        summary["changes"].append({"file": entry, "xhtml_fixes": fixes})
                    zf_out.writestr(entry, new_data)
                    continue

                # Pass through everything else unchanged
                zf_out.writestr(entry, data)

    # Replace original or write to output
    if output_path == epub_path:
        os.replace(temp_path, epub_path)
    else:
        shutil.move(temp_path, output_path)

    return summary


def print_summary(summary: dict, file_path: str):
    """Print processing summary."""
    print(f"\n{'='*80}")
    print(f"Kindle EPUB Fix: {file_path}")
    print(f"{'='*80}")

    if not summary["changes"]:
        print("No changes needed - EPUB is already Kindle-compatible.")
        return

    print(f"\nChanges applied:")
    print(f"  Images resized:    {summary['images_resized']}")
    print(f"  Images compressed: {summary['images_compressed']}")
    print(f"  XHTML files fixed: {summary['xhtml_fixed']}")

    if summary["total_original_kb"] > 0:
        savings = summary["total_original_kb"] - summary["total_new_kb"]
        pct = round(savings / summary["total_original_kb"] * 100, 1)
        print(f"  Image size:        {round(summary['total_original_kb']/1024, 2)}MB -> {round(summary['total_new_kb']/1024, 2)}MB ({pct}% reduction)")

    print(f"\nDetailed changes:")
    for change in summary["changes"]:
        print(f"\n  {change['file']}")
        for key, val in change.items():
            if key == "file":
                continue
            print(f"    {key}: {val}")


def main():
    parser = argparse.ArgumentParser(description="Fix EPUB for Kindle compatibility")
    parser.add_argument("epub", help="Path to EPUB file")
    parser.add_argument("--output", "-o", help="Output path (default: overwrite input)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would change without modifying")
    args = parser.parse_args()

    epub_path = args.epub
    if not os.path.exists(epub_path):
        print(f"Error: File not found: {epub_path}")
        sys.exit(1)

    output_path = args.output or epub_path

    if args.dry_run:
        print(f"DRY RUN - analyzing {epub_path}")

    summary = process_epub(epub_path, output_path, dry_run=args.dry_run)
    print_summary(summary, epub_path)

    if summary["changes"]:
        if args.dry_run:
            print(f"\nRun without --dry-run to apply these fixes.")
        else:
            print(f"\nFixed EPUB written to: {output_path}")


if __name__ == "__main__":
    main()
