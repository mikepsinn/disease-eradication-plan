#!/usr/bin/env python3
"""Diagnose what blocks Kindle Enhanced Typesetting by progressively stripping EPUB content.

Creates modified EPUB variants, attempts KPF conversion on each, and logs which
change (if any) makes Enhanced Typesetting work.

Strategy:
1. Try broad category removals first (SVGs, images, chapters, CSS)
2. If a category works, binary search within it to find the threshold

Usage:
    python scripts/diagnose-kindle-enhanced-typesetting.py
    python scripts/diagnose-kindle-enhanced-typesetting.py --epub path/to/book.epub
    python scripts/diagnose-kindle-enhanced-typesetting.py --skip-to 5   # resume from trial 5
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import csv
import os
import re
import shutil
import subprocess
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path


KINDLE_PREVIEWER = Path(r"C:\Users\m\AppData\Local\Amazon\Kindle Previewer 3\Kindle Previewer 3.exe")
PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_EPUB = PROJECT_ROOT / "assets" / "epubs" / "How-to-End-War-and-Disease.epub"
DIAG_DIR = PROJECT_ROOT / "assets" / "kindle-diagnosis"


@dataclass
class Trial:
    name: str
    description: str
    enhanced_typesetting: str = ""
    conversion_status: str = ""
    error_count: int = 0
    epub_size_mb: float = 0.0
    spine_items: int = 0
    image_count: int = 0
    svg_count: int = 0
    duration_sec: float = 0.0


def count_epub_stats(epub_path: str) -> dict:
    """Count spine items, images, SVGs in an EPUB."""
    stats = {"spine_items": 0, "images": 0, "svgs": 0, "size_mb": 0.0}
    stats["size_mb"] = os.path.getsize(epub_path) / (1024 * 1024)

    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}
    with zipfile.ZipFile(epub_path, "r") as zf:
        for name in zf.namelist():
            ext = Path(name).suffix.lower()
            if ext in image_exts:
                stats["images"] += 1
            elif ext == ".svg":
                stats["svgs"] += 1
            elif ext in (".xhtml", ".html"):
                # Check if it's in the spine (content file, not nav)
                if "nav" not in name.lower():
                    stats["spine_items"] += 1
    return stats


def try_kpf_conversion(epub_path: str, output_dir: str) -> dict:
    """Attempt KPF conversion and parse results."""
    # Clean output dir
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    start = time.time()
    try:
        subprocess.run(
            [str(KINDLE_PREVIEWER), epub_path, "-convert", "-output", output_dir],
            capture_output=True, text=True, timeout=600,
        )
    except subprocess.TimeoutExpired:
        return {"enhanced_typesetting": "Timeout", "conversion_status": "Timeout",
                "error_count": -1, "duration": time.time() - start}

    duration = time.time() - start

    # Parse summary log
    summary_csv = Path(output_dir) / "Summary_Log.csv"
    result = {"enhanced_typesetting": "Unknown", "conversion_status": "Unknown",
              "error_count": -1, "duration": duration}

    if summary_csv.exists():
        with open(summary_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                result["enhanced_typesetting"] = row.get("Enhanced Typesetting Status", "Unknown")
                result["conversion_status"] = row.get("Conversion Status", "Unknown")
                result["error_count"] = int(row.get("Error Count", -1))
                break

    # Check if KPF was actually generated
    kpf_files = list(Path(output_dir).glob("*.kpf"))
    result["kpf_generated"] = len(kpf_files) > 0

    return result


def create_variant(source_epub: str, output_epub: str, modifier_fn) -> dict:
    """Create a modified EPUB variant using the modifier function.

    modifier_fn(entry_name, data, zf_namelist) -> (include: bool, new_data: bytes | None)
    Returns stats about what was modified.
    """
    stats = {"removed": 0, "modified": 0, "kept": 0}

    with zipfile.ZipFile(source_epub, "r") as zf_in:
        names = zf_in.namelist()
        with zipfile.ZipFile(output_epub, "w", zipfile.ZIP_DEFLATED) as zf_out:
            for entry in names:
                if entry == "mimetype":
                    zf_out.writestr(entry, zf_in.read(entry), compress_type=zipfile.ZIP_STORED)
                    stats["kept"] += 1
                    continue

                data = zf_in.read(entry)
                include, new_data = modifier_fn(entry, data, names)

                if not include:
                    stats["removed"] += 1
                    continue

                if new_data is not None:
                    zf_out.writestr(entry, new_data)
                    stats["modified"] += 1
                else:
                    zf_out.writestr(entry, data)
                    stats["kept"] += 1

    return stats


def remove_svgs(entry, data, names):
    """Remove all SVG files and references."""
    if entry.lower().endswith(".svg"):
        return False, None
    # Update OPF to remove SVG items
    if entry.lower().endswith(".opf"):
        text = data.decode("utf-8", errors="replace")
        text = re.sub(r'<item[^>]*media-type="image/svg\+xml"[^>]*/>\s*', '', text)
        return True, text.encode("utf-8")
    return True, None


def remove_all_images(entry, data, names):
    """Remove all image files."""
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".svg"}
    if Path(entry).suffix.lower() in image_exts:
        return False, None
    if entry.lower().endswith(".opf"):
        text = data.decode("utf-8", errors="replace")
        text = re.sub(r'<item[^>]*media-type="image/[^"]*"[^>]*/>\s*', '', text)
        return True, text.encode("utf-8")
    return True, None


def strip_inline_block_css(entry, data, names):
    """Remove inline-block from CSS."""
    if Path(entry).suffix.lower() in (".css", ".xhtml", ".html"):
        text = data.decode("utf-8", errors="replace")
        if "inline-block" in text:
            text = text.replace("inline-block", "inline")
            return True, text.encode("utf-8")
    return True, None


def make_chapter_filter(keep_ratio: float):
    """Create a filter that keeps only a fraction of chapters."""
    def filter_fn(entry, data, names):
        ext = Path(entry).suffix.lower()
        if ext not in (".xhtml", ".html"):
            # For OPF, we need to remove spine/manifest entries for removed chapters
            if ext == ".opf":
                # We'll handle this after we know which files to keep
                pass
            return True, None

        # Get all content files (not nav, not toc)
        content_files = sorted([
            n for n in names
            if Path(n).suffix.lower() in (".xhtml", ".html")
            and "nav" not in n.lower()
            and "toc" not in n.lower()
            and "cover" not in n.lower()
            and "titlepage" not in n.lower()
        ])

        keep_count = max(1, int(len(content_files) * keep_ratio))
        keep_set = set(content_files[:keep_count])

        # Always keep nav, toc, cover, titlepage
        if "nav" in entry.lower() or "toc" in entry.lower() or "cover" in entry.lower() or "titlepage" in entry.lower():
            return True, None

        return entry in keep_set, None

    return filter_fn


def make_opf_cleaner(kept_files: set):
    """Remove OPF manifest/spine entries for files not in kept_files."""
    def clean_opf(entry, data, names):
        if not entry.lower().endswith(".opf"):
            return True, None

        text = data.decode("utf-8", errors="replace")

        # Find manifest items that reference removed files
        removed_ids = set()
        new_lines = []
        for line in text.splitlines(keepends=True):
            item_match = re.search(r'<item\s+id="([^"]*)"[^>]*href="([^"]*)"', line)
            if item_match:
                item_id = item_match.group(1)
                href = item_match.group(2)
                # Check if the referenced file exists in our kept set
                # href is relative to OPF location
                full_path = None
                for name in names:
                    if name.endswith(href) or href in name:
                        full_path = name
                        break
                if full_path and full_path not in kept_files:
                    removed_ids.add(item_id)
                    continue  # skip this manifest item
            new_lines.append(line)

        text = "".join(new_lines)

        # Remove spine entries for removed items
        for rid in removed_ids:
            text = re.sub(rf'<itemref\s+idref="{re.escape(rid)}"[^>]*/>\s*', '', text)

        return True, text.encode("utf-8")

    return clean_opf


def create_reduced_epub(source_epub: str, output_epub: str, keep_ratio: float) -> dict:
    """Create EPUB with only a fraction of chapters, properly updating OPF."""
    content_files = []

    with zipfile.ZipFile(source_epub, "r") as zf:
        names = zf.namelist()
        content_files = sorted([
            n for n in names
            if Path(n).suffix.lower() in (".xhtml", ".html")
            and "nav" not in n.lower()
            and "toc" not in n.lower()
            and "cover" not in n.lower()
            and "titlepage" not in n.lower()
        ])

    keep_count = max(1, int(len(content_files) * keep_ratio))
    keep_chapters = set(content_files[:keep_count])

    # Build full set of kept files (chapters + everything non-chapter)
    all_kept = set()
    with zipfile.ZipFile(source_epub, "r") as zf:
        for name in zf.namelist():
            ext = Path(name).suffix.lower()
            if ext in (".xhtml", ".html"):
                if name in keep_chapters or "nav" in name.lower() or "toc" in name.lower() or "cover" in name.lower() or "titlepage" in name.lower():
                    all_kept.add(name)
            else:
                all_kept.add(name)

    stats = {"total_chapters": len(content_files), "kept_chapters": keep_count,
             "removed_chapters": len(content_files) - keep_count}

    with zipfile.ZipFile(source_epub, "r") as zf_in:
        with zipfile.ZipFile(output_epub, "w", zipfile.ZIP_DEFLATED) as zf_out:
            for entry in zf_in.namelist():
                if entry == "mimetype":
                    zf_out.writestr(entry, zf_in.read(entry), compress_type=zipfile.ZIP_STORED)
                    continue

                if entry not in all_kept:
                    continue

                data = zf_in.read(entry)

                # Clean up OPF
                if entry.lower().endswith(".opf"):
                    text = data.decode("utf-8", errors="replace")
                    removed_ids = set()
                    new_lines = []
                    for line in text.splitlines(keepends=True):
                        item_match = re.search(r'<item\s+id="([^"]*)"[^>]*href="([^"]*)"', line)
                        if item_match:
                            href = item_match.group(1)
                            item_href = item_match.group(2)
                            # Resolve href relative to OPF
                            opf_dir = str(Path(entry).parent)
                            full_href = f"{opf_dir}/{item_href}" if opf_dir != "." else item_href
                            if full_href not in all_kept:
                                # Also try without directory prefix
                                found = any(n.endswith(item_href) for n in all_kept)
                                if not found:
                                    removed_ids.add(href)
                                    continue
                        new_lines.append(line)

                    text = "".join(new_lines)
                    for rid in removed_ids:
                        text = re.sub(rf'<itemref\s+idref="{re.escape(rid)}"[^>]*/>\s*', '', text)
                    data = text.encode("utf-8")

                zf_out.writestr(entry, data)

    return stats


def run_trials(epub_path: str, skip_to: int = 0):
    """Run progressive trials to find what blocks Enhanced Typesetting."""
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    results_file = DIAG_DIR / "diagnosis-results.csv"

    trials = [
        ("baseline", "Original EPUB, no modifications", None),
        ("no-svgs", "Remove all SVG files", remove_svgs),
        ("no-inline-block", "Replace inline-block with inline in CSS", strip_inline_block_css),
        ("no-svgs-no-inline-block", "Remove SVGs + fix inline-block", None),  # combined
        ("chapters-50pct", "Keep only first 50% of chapters", 0.5),
        ("chapters-25pct", "Keep only first 25% of chapters", 0.25),
        ("chapters-10pct", "Keep only first 10% of chapters", 0.10),
        ("no-images", "Remove ALL images (including SVGs)", remove_all_images),
        ("chapters-10pct-no-images", "10% chapters + no images", None),  # combined
        ("chapters-5pct", "Keep only first 5% of chapters (~22)", 0.05),
        ("chapters-1pct", "Keep only first 1% of chapters (~4)", 0.01),
    ]

    results = []
    print(f"\n{'='*90}")
    print(f"Kindle Enhanced Typesetting Diagnosis")
    print(f"Source: {epub_path}")
    print(f"Output: {DIAG_DIR}")
    print(f"{'='*90}\n")

    # Get baseline stats
    base_stats = count_epub_stats(epub_path)
    print(f"Baseline EPUB: {base_stats['size_mb']:.1f} MB, {base_stats['spine_items']} spine items, "
          f"{base_stats['images']} images, {base_stats['svgs']} SVGs\n")

    for i, (name, desc, modifier) in enumerate(trials):
        if i < skip_to:
            print(f"[{i}] SKIP {name}: {desc}")
            continue

        print(f"[{i}] {name}: {desc}")
        variant_epub = str(DIAG_DIR / f"variant-{name}.epub")
        variant_output = str(DIAG_DIR / f"output-{name}")

        # Create variant
        if modifier is None and name == "baseline":
            shutil.copy2(epub_path, variant_epub)
        elif modifier is None and name == "no-svgs-no-inline-block":
            # Combined: start from no-svgs, then strip inline-block
            source = str(DIAG_DIR / "variant-no-svgs.epub")
            if not os.path.exists(source):
                print(f"     Skipping (depends on no-svgs variant)")
                continue
            create_variant(source, variant_epub, strip_inline_block_css)
        elif modifier is None and name == "chapters-10pct-no-images":
            source = str(DIAG_DIR / "variant-chapters-10pct.epub")
            if not os.path.exists(source):
                print(f"     Skipping (depends on chapters-10pct variant)")
                continue
            create_variant(source, variant_epub, remove_all_images)
        elif isinstance(modifier, float):
            # Chapter reduction
            mod_stats = create_reduced_epub(epub_path, variant_epub, modifier)
            print(f"     Kept {mod_stats['kept_chapters']}/{mod_stats['total_chapters']} chapters")
        elif callable(modifier):
            mod_stats = create_variant(epub_path, variant_epub, modifier)
            print(f"     Removed: {mod_stats['removed']}, Modified: {mod_stats['modified']}")

        # Get stats
        stats = count_epub_stats(variant_epub)
        print(f"     Size: {stats['size_mb']:.1f} MB, Spine: {stats['spine_items']}, "
              f"Images: {stats['images']}, SVGs: {stats['svgs']}")

        # Try conversion
        print(f"     Converting...", end="", flush=True)
        result = try_kpf_conversion(variant_epub, variant_output)
        et = result["enhanced_typesetting"]
        status = result["conversion_status"]
        duration = result["duration"]

        trial = Trial(
            name=name, description=desc,
            enhanced_typesetting=et, conversion_status=status,
            error_count=result["error_count"],
            epub_size_mb=stats["size_mb"], spine_items=stats["spine_items"],
            image_count=stats["images"], svg_count=stats["svgs"],
            duration_sec=duration,
        )
        results.append(trial)

        icon = "OK" if et == "Supported" else "FAIL"
        print(f" [{icon}] ET={et}, Status={status}, Errors={result['error_count']}, "
              f"Time={duration:.0f}s")

        # If Enhanced Typesetting succeeded, we found our answer!
        if et == "Supported":
            print(f"\n*** FOUND IT! Enhanced Typesetting works with: {name} ***")
            print(f"    Description: {desc}")
            print(f"    This means the blocker is related to what was removed/changed.")

            # If it was a chapter reduction, try binary search
            if isinstance(modifier, float) and modifier < 1.0:
                print(f"\n    Consider binary searching between {modifier*100:.0f}% and the previous trial")
                print(f"    to find the exact threshold.")
            break

        # Clean up variant EPUB to save disk space (keep output logs)
        if name != "baseline":
            try:
                os.remove(variant_epub)
            except OSError:
                pass

    # Write results CSV
    print(f"\n{'='*90}")
    print(f"Results Summary")
    print(f"{'='*90}")
    print(f"{'Trial':<35} {'ET Status':<15} {'Size MB':<10} {'Spine':<8} {'Images':<8} {'SVGs':<6} {'Time':<8}")
    print("-" * 90)
    for t in results:
        print(f"{t.name:<35} {t.enhanced_typesetting:<15} {t.epub_size_mb:<10.1f} "
              f"{t.spine_items:<8} {t.image_count:<8} {t.svg_count:<6} {t.duration_sec:<8.0f}")

    with open(results_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Trial", "Description", "Enhanced Typesetting", "Conversion Status",
                          "Errors", "Size MB", "Spine Items", "Images", "SVGs", "Duration (s)"])
        for t in results:
            writer.writerow([t.name, t.description, t.enhanced_typesetting, t.conversion_status,
                              t.error_count, f"{t.epub_size_mb:.1f}", t.spine_items,
                              t.image_count, t.svg_count, f"{t.duration_sec:.0f}"])

    print(f"\nResults saved to: {results_file}")

    if not any(t.enhanced_typesetting == "Supported" for t in results):
        print("\nNo trial succeeded. The book may be fundamentally too complex for Enhanced Typesetting.")
        print("KDP will still accept it with basic typesetting. Consider uploading the clean EPUB directly.")


def main():
    parser = argparse.ArgumentParser(description="Diagnose Kindle Enhanced Typesetting blockers")
    parser.add_argument("--epub", default=str(DEFAULT_EPUB), help="Path to source EPUB")
    parser.add_argument("--skip-to", type=int, default=0, help="Skip to trial number N")
    args = parser.parse_args()

    if not KINDLE_PREVIEWER.exists():
        print(f"Error: Kindle Previewer not found at {KINDLE_PREVIEWER}")
        print("Install from: https://www.amazon.com/Kindle-Previewer/b?node=21381691011")
        sys.exit(1)

    if not os.path.exists(args.epub):
        print(f"Error: EPUB not found: {args.epub}")
        sys.exit(1)

    run_trials(args.epub, skip_to=args.skip_to)


if __name__ == "__main__":
    main()
