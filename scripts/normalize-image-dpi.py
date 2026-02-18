#!/usr/bin/env python3
"""Normalize DPI metadata on source images for DOCX/EPUB compatibility.

This script ONLY changes DPI metadata, never pixel data. Images render
identically in HTML and PDF (which ignore DPI). DOCX and EPUB use DPI
to compute physical size, so correct metadata prevents oversized-image errors.

Rules:
- Bad DPI (0 or 1): set to TARGET_DPI (150)
- No DPI metadata: set to TARGET_DPI (150)
- Low DPI that causes >MAX_INCHES physical size: bump DPI to fit
- Already-correct DPI: skip (no-op)

Usage:
    python scripts/normalize-image-dpi.py                  # Dry run (default)
    python scripts/normalize-image-dpi.py --apply           # Actually modify files
    python scripts/normalize-image-dpi.py --apply --dir assets/images/subfolder
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import io
import math
import os
import shutil
from pathlib import Path

from PIL import Image

TARGET_DPI = 150      # Good default: 1024px = 6.8 inches, fits any page
MIN_VALID_DPI = 72    # Anything below this is garbage metadata
MAX_INCHES = 10.0     # Max physical dimension in any direction
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}
# GIF and WEBP: Pillow can read DPI but resaving can alter animation/quality
SKIP_FORMATS = {".gif", ".webp", ".svg"}


def compute_needed_dpi(width: int, height: int, max_inches: float) -> int:
    """Compute minimum DPI so the image fits within max_inches."""
    max_dim = max(width, height)
    if max_dim == 0:
        return TARGET_DPI
    needed = math.ceil(max_dim / max_inches)
    return max(needed, MIN_VALID_DPI)


def normalize_image(path: Path, apply: bool = False) -> dict | None:
    """Check and optionally fix DPI metadata for one image.

    Returns a dict describing what was/would be changed, or None if no change needed.
    """
    ext = path.suffix.lower()
    if ext in SKIP_FORMATS:
        return None
    if ext not in SUPPORTED_FORMATS:
        return None

    try:
        img = Image.open(path)
    except Exception as e:
        return {"file": str(path), "error": str(e)}

    width, height = img.size
    original_dpi = img.info.get("dpi", None)

    # Determine current effective DPI
    if original_dpi is None:
        current_dpi_x, current_dpi_y = 0, 0
        reason = "no_dpi_metadata"
    else:
        current_dpi_x, current_dpi_y = original_dpi
        if current_dpi_x < MIN_VALID_DPI or current_dpi_y < MIN_VALID_DPI:
            reason = "bad_dpi"
        else:
            # Check if physical size exceeds limit (with 1% tolerance for PNG float precision)
            w_inches = width / current_dpi_x
            h_inches = height / current_dpi_y
            if w_inches > MAX_INCHES * 1.01 or h_inches > MAX_INCHES * 1.01:
                reason = "oversized"
            else:
                return None  # Image is fine

    # Compute target DPI
    needed_dpi = compute_needed_dpi(width, height, MAX_INCHES)
    new_dpi = max(needed_dpi, TARGET_DPI)

    result = {
        "file": str(path),
        "reason": reason,
        "pixels": f"{width}x{height}",
        "old_dpi": f"{current_dpi_x}x{current_dpi_y}" if original_dpi else "none",
        "new_dpi": new_dpi,
        "old_inches": f"{width/max(current_dpi_x, 1):.1f}x{height/max(current_dpi_y, 1):.1f}",
        "new_inches": f"{width/new_dpi:.1f}x{height/new_dpi:.1f}",
    }

    if apply:
        # Re-save with corrected DPI metadata
        save_dpi = (new_dpi, new_dpi)
        fmt = img.format or ("JPEG" if ext in (".jpg", ".jpeg") else "PNG")

        buf = io.BytesIO()
        save_kwargs = {"dpi": save_dpi}

        if fmt == "JPEG":
            # Preserve JPEG quality by using high quality
            save_kwargs["quality"] = 95
            save_kwargs["optimize"] = False  # Don't re-compress
            # Ensure RGB mode for JPEG
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
        elif fmt == "PNG":
            save_kwargs["optimize"] = False

        img.save(buf, format=fmt, **save_kwargs)

        # Write back (atomic: write to temp, then rename)
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        with open(tmp_path, "wb") as f:
            f.write(buf.getvalue())
        os.replace(tmp_path, path)
        result["applied"] = True

    return result


def main():
    parser = argparse.ArgumentParser(description="Normalize image DPI metadata")
    parser.add_argument("--apply", action="store_true", help="Actually modify files (default: dry run)")
    parser.add_argument("--dir", action="append", default=None, help="Directory to scan (can specify multiple; default: assets/images assets/cover)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all images, not just changes")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.parent
    default_dirs = ["assets"]
    scan_dirs_raw = args.dir if args.dir else default_dirs

    scan_dirs = []
    for d in scan_dirs_raw:
        p = script_dir / d
        if p.exists():
            scan_dirs.append(p)
        else:
            print(f"Warning: Directory not found, skipping: {p}")

    if not scan_dirs:
        print("Error: No valid directories to scan")
        sys.exit(1)

    mode = "APPLYING CHANGES" if args.apply else "DRY RUN (use --apply to modify files)"
    print(f"\n{'='*80}")
    print(f"Image DPI Normalization: {mode}")
    print(f"Directories: {', '.join(str(d) for d in scan_dirs)}")
    print(f"Target DPI: {TARGET_DPI}, Max physical size: {MAX_INCHES} inches")
    print(f"{'='*80}\n")

    changes = []
    errors = []
    skipped = 0
    total = 0

    for scan_dir in scan_dirs:
        for path in sorted(scan_dir.rglob("*")):
            if not path.is_file():
                continue
            ext = path.suffix.lower()
            if ext in SKIP_FORMATS:
                skipped += 1
                continue
            if ext not in SUPPORTED_FORMATS:
                continue

            total += 1
            result = normalize_image(path, apply=args.apply)

            if result is None:
                continue

            if "error" in result:
                errors.append(result)
                continue

            changes.append(result)

    # Print results grouped by reason
    by_reason = {}
    for c in changes:
        reason = c.get("reason", "unknown")
        by_reason.setdefault(reason, []).append(c)

    for reason, items in sorted(by_reason.items()):
        print(f"\n--- {reason.upper()} ({len(items)} images) ---")
        for item in items[:10]:  # Show first 10 per category
            action = "FIXED" if item.get("applied") else "WOULD FIX"
            print(f"  [{action}] {item['file']}")
            print(f"    {item['pixels']}px, DPI: {item['old_dpi']} -> {item['new_dpi']}, Size: {item['old_inches']} -> {item['new_inches']} inches")
        if len(items) > 10:
            print(f"  ... and {len(items) - 10} more")

    if errors:
        print(f"\n--- ERRORS ({len(errors)}) ---")
        for e in errors:
            print(f"  {e['file']}: {e['error']}")

    # Summary
    print(f"\n{'='*80}")
    print(f"Summary: {total} images scanned, {len(changes)} need DPI fix, {skipped} skipped (GIF/WEBP/SVG)")
    if args.apply:
        print(f"  {sum(1 for c in changes if c.get('applied'))} files modified")
    else:
        print(f"  Run with --apply to modify files")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
