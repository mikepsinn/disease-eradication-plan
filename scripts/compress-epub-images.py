#!/usr/bin/env python3
"""Compress images inside an EPUB to meet KDP's 95 MB size limit.

Resizes and recompresses JPEG/PNG images in-place within the EPUB zip.
Targets AI-generated 1024x1024 illustrations that are oversized for e-readers
(typically 600-800px display width).

Usage:
    python scripts/compress-epub-images.py assets/epubs/book.epub
    python scripts/compress-epub-images.py book.epub --max-px 600 --quality 65
    python scripts/compress-epub-images.py book.epub --dry-run
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import io
import os
import zipfile
from pathlib import Path

from PIL import Image

# Default settings tuned for e-readers
DEFAULT_MAX_PX = 768       # Max dimension (e-readers are ~600-800px wide)
DEFAULT_QUALITY = 70       # JPEG quality (70 is good for e-ink/tablet)
SKIP_BELOW_KB = 50         # Don't recompress tiny images (icons, bullets)
COVER_MIN_PX = 1000        # Don't resize cover images below this


def compress_image(data: bytes, filename: str, max_px: int, quality: int, is_cover: bool) -> tuple[bytes, dict]:
    """Resize and recompress a single image.

    Returns (new_bytes, stats_dict). stats_dict is empty if no change was made.
    """
    original_size = len(data)

    # Skip tiny images
    if original_size < SKIP_BELOW_KB * 1024:
        return data, {}

    img = Image.open(io.BytesIO(data))
    orig_w, orig_h = img.size
    ext = Path(filename).suffix.lower()

    # Determine target max dimension
    target_max = max(max_px, COVER_MIN_PX) if is_cover else max_px

    # Only resize if larger than target
    needs_resize = max(orig_w, orig_h) > target_max
    if needs_resize:
        img.thumbnail((target_max, target_max), Image.Resampling.LANCZOS)

    # Convert RGBA PNGs to RGB for JPEG output (smaller)
    output_format = "JPEG"
    if ext == ".png":
        # Keep PNGs as PNG (they may have transparency for diagrams)
        output_format = "PNG"
    if img.mode in ("RGBA", "P") and output_format == "JPEG":
        img = img.convert("RGB")
    elif img.mode == "RGBA" and output_format == "PNG":
        pass  # keep transparency

    buf = io.BytesIO()
    if output_format == "JPEG":
        img.save(buf, format="JPEG", quality=quality, optimize=True)
    else:
        img.save(buf, format="PNG", optimize=True)

    new_data = buf.getvalue()
    new_size = len(new_data)

    # Only use compressed version if it's actually smaller
    if new_size >= original_size:
        return data, {}

    new_w, new_h = img.size
    return new_data, {
        "original_size": original_size,
        "new_size": new_size,
        "original_dims": (orig_w, orig_h),
        "new_dims": (new_w, new_h),
        "saved": original_size - new_size,
    }


def process_epub(epub_path: str, max_px: int, quality: int, dry_run: bool = False) -> dict:
    """Process all images in an EPUB, compressing in-place.

    Returns summary dict with stats.
    """
    image_extensions = {".jpg", ".jpeg", ".png"}
    original_file_size = os.path.getsize(epub_path)

    summary = {
        "original_file_size": original_file_size,
        "images_processed": 0,
        "images_compressed": 0,
        "bytes_saved": 0,
        "details": [],
    }

    # Read all entries
    entries = {}
    with zipfile.ZipFile(epub_path, "r") as zf:
        for name in zf.namelist():
            entries[name] = zf.read(name)

    # Detect cover image (usually referenced in OPF or named "cover")
    cover_names = set()
    for name in entries:
        lower = name.lower()
        if "cover" in lower and Path(lower).suffix in image_extensions:
            cover_names.add(name)

    # Process images
    for name, data in entries.items():
        ext = Path(name).suffix.lower()
        if ext not in image_extensions:
            continue

        summary["images_processed"] += 1
        is_cover = name in cover_names

        new_data, stats = compress_image(data, name, max_px, quality, is_cover)
        if stats:
            summary["images_compressed"] += 1
            summary["bytes_saved"] += stats["saved"]
            summary["details"].append({"file": name, **stats})
            if not dry_run:
                entries[name] = new_data

    if dry_run:
        return summary

    # Rewrite EPUB
    temp_path = epub_path + ".tmp"
    with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zf_out:
        for name in entries:
            # mimetype must be first and uncompressed per EPUB spec
            if name == "mimetype":
                zf_out.writestr(name, entries[name], compress_type=zipfile.ZIP_STORED)
            else:
                zf_out.writestr(name, entries[name])

    os.replace(temp_path, epub_path)
    summary["new_file_size"] = os.path.getsize(epub_path)
    return summary


def main():
    parser = argparse.ArgumentParser(description="Compress images inside an EPUB for KDP")
    parser.add_argument("epub", help="Path to EPUB file")
    parser.add_argument("--max-px", type=int, default=DEFAULT_MAX_PX,
                        help=f"Max image dimension in pixels (default: {DEFAULT_MAX_PX})")
    parser.add_argument("--quality", type=int, default=DEFAULT_QUALITY,
                        help=f"JPEG quality 1-95 (default: {DEFAULT_QUALITY})")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Show savings without modifying")
    args = parser.parse_args()

    if not os.path.exists(args.epub):
        print(f"Error: File not found: {args.epub}")
        sys.exit(1)

    print(f"[*] Processing: {args.epub}")
    print(f"[*] Settings: max {args.max_px}px, JPEG quality {args.quality}")
    if args.dry_run:
        print("[*] DRY RUN - no changes will be made")

    summary = process_epub(args.epub, args.max_px, args.quality, dry_run=args.dry_run)

    orig_mb = summary["original_file_size"] / (1024 * 1024)
    saved_mb = summary["bytes_saved"] / (1024 * 1024)

    print(f"\n{'='*60}")
    print(f"Images found:      {summary['images_processed']}")
    print(f"Images compressed: {summary['images_compressed']}")
    print(f"Original EPUB:     {orig_mb:.1f} MB")
    print(f"Data saved:        {saved_mb:.1f} MB")

    if "new_file_size" in summary:
        new_mb = summary["new_file_size"] / (1024 * 1024)
        print(f"New EPUB:          {new_mb:.1f} MB")
        reduction = (1 - summary["new_file_size"] / summary["original_file_size"]) * 100
        print(f"Reduction:         {reduction:.0f}%")
        if new_mb < 95:
            print(f"[OK] Under 95 MB KDP limit")
        else:
            print(f"[WARN] Still over 95 MB KDP limit - try --max-px 600 or --quality 60")
    elif args.dry_run:
        est_mb = orig_mb - saved_mb
        print(f"Estimated new:     {est_mb:.1f} MB")

    print(f"{'='*60}")

    # Show top 10 largest savings
    if summary["details"]:
        top = sorted(summary["details"], key=lambda x: x["saved"], reverse=True)[:10]
        print(f"\nTop savings:")
        for d in top:
            name = Path(d["file"]).name
            ow, oh = d["original_dims"]
            nw, nh = d["new_dims"]
            saved_kb = d["saved"] / 1024
            print(f"  {name}: {ow}x{oh} -> {nw}x{nh}, saved {saved_kb:.0f} KB")


if __name__ == "__main__":
    main()
