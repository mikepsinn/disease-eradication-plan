#!/usr/bin/env python3
"""Convert SVG images to PNG inside an EPUB for Kindle Enhanced Typesetting compatibility.

Kindle Enhanced Typesetting (required for KPF) supports max 25 SVGs.
Books with LaTeX equations rendered as SVG typically exceed this.
This script rasterizes SVGs to high-DPI PNGs using sharp (Node.js).

Usage:
    python scripts/convert-epub-svg-to-png.py assets/epubs/Book-kindle.epub
    python scripts/convert-epub-svg-to-png.py assets/epubs/Book-kindle.epub --output assets/epubs/Book-kindle-kpf-ready.epub
    python scripts/convert-epub-svg-to-png.py assets/epubs/Book-kindle.epub --dpi 300
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


DPI_SCALE = 3  # Render at 3x for crisp math equations (effective ~216 DPI)


def extract_epub(epub_path: Path, dest_dir: Path):
    """Extract EPUB to directory."""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        zf.extractall(dest_dir)


def repack_epub(source_dir: Path, epub_path: Path):
    """Repack directory into EPUB (mimetype must be first, uncompressed)."""
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first entry, stored uncompressed
        mimetype_path = source_dir / 'mimetype'
        if mimetype_path.exists():
            zf.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

        for root, dirs, files in os.walk(source_dir):
            # Sort for reproducibility
            dirs.sort()
            files.sort()
            for f in files:
                file_path = Path(root) / f
                arcname = file_path.relative_to(source_dir).as_posix()
                if arcname == 'mimetype':
                    continue  # Already added
                zf.write(file_path, arcname)


def convert_svgs_with_sharp(svg_dir: Path, png_dir: Path, scale: int) -> dict:
    """Convert all SVGs in a directory to PNGs using sharp (Node.js).

    Returns dict mapping svg filename -> png filename.
    """
    svg_files = sorted(svg_dir.glob('*.svg'))
    if not svg_files:
        return {}

    png_dir.mkdir(parents=True, exist_ok=True)

    # Build a manifest for batch processing
    manifest = []
    for svg_file in svg_files:
        png_name = svg_file.stem + '.png'
        manifest.append({
            'svg': str(svg_file).replace('\\', '/'),
            'png': str(png_dir / png_name).replace('\\', '/'),
        })

    manifest_path = svg_dir / '_convert_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f)

    # Single Node.js call to convert all SVGs
    node_script = f"""
const sharp = require('sharp');
const fs = require('fs');
const manifest = JSON.parse(fs.readFileSync('{str(manifest_path).replace(chr(92), "/")}', 'utf8'));

// 1x1 transparent PNG for zero-dimension SVGs (spacers/placeholders)
const TRANSPARENT_1PX = sharp({{
    create: {{ width: 1, height: 1, channels: 4, background: {{ r: 0, g: 0, b: 0, alpha: 0 }} }}
}}).png().toBuffer();

async function convertAll() {{
    const fallback = await TRANSPARENT_1PX;
    let success = 0, failed = 0, spacers = 0;
    for (const item of manifest) {{
        try {{
            // Check for zero-dimension SVGs first
            const svgContent = fs.readFileSync(item.svg, 'utf8');
            if (svgContent.includes("width='0pt'") || svgContent.includes('width="0pt"') ||
                svgContent.includes("viewBox='0 0 0 0'") || svgContent.includes('viewBox="0 0 0 0"')) {{
                fs.writeFileSync(item.png, fallback);
                spacers++;
                success++;
                continue;
            }}
            await sharp(item.svg, {{ density: 72 * {scale} }})
                .png()
                .toBuffer()
                .then(buf => fs.writeFileSync(item.png, buf));
            success++;
        }} catch (err) {{
            console.error('FAILED:', item.svg, err.message);
            failed++;
        }}
    }}
    console.log(JSON.stringify({{ success, failed, spacers, total: manifest.length }}));
}}
convertAll();
"""

    result = subprocess.run(
        ['node', '-e', node_script],
        capture_output=True, text=True, encoding='utf-8',
        cwd=str(Path(__file__).parent.parent),
        timeout=300,
    )

    if result.stderr:
        for line in result.stderr.strip().splitlines():
            print(f"  [sharp] {line}")

    # Parse result
    stats = {"success": 0, "failed": 0, "spacers": 0, "total": 0}
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line.startswith('{'):
            stats = json.loads(line)

    rendered = stats['success'] - stats.get('spacers', 0)
    msg = f"  Converted {stats['success']}/{stats['total']} SVGs to PNG"
    if stats.get('spacers'):
        msg += f" ({rendered} rendered, {stats['spacers']} zero-dimension spacers)"
    if stats['failed']:
        msg += f" ({stats['failed']} failed)"
    print(msg)

    # Return mapping
    mapping = {}
    for item in manifest:
        png_path = Path(item['png'])
        if png_path.exists():
            svg_name = Path(item['svg']).name
            mapping[svg_name] = png_path.name

    manifest_path.unlink(missing_ok=True)
    return mapping


def update_references(epub_dir: Path, svg_to_png: dict, svg_arcnames: dict):
    """Update XHTML, OPF, and NCX references from SVG to PNG."""
    # Build a mapping from SVG archive paths to PNG archive paths
    arc_mapping = {}  # old_path -> new_path
    for svg_name, png_name in svg_to_png.items():
        if svg_name in svg_arcnames:
            old_arc = svg_arcnames[svg_name]
            new_arc = old_arc.rsplit('.', 1)[0] + '.png'
            arc_mapping[old_arc] = new_arc

    updated_files = 0

    # Update all text-based files in the EPUB
    for root, dirs, files in os.walk(epub_dir):
        for f in files:
            file_path = Path(root) / f
            ext = file_path.suffix.lower()
            if ext not in ('.xhtml', '.html', '.htm', '.opf', '.ncx', '.xml', '.css'):
                continue

            content = file_path.read_text(encoding='utf-8', errors='replace')
            original = content

            # Replace SVG references
            for old_arc, new_arc in arc_mapping.items():
                # Match both full path and basename references
                old_basename = os.path.basename(old_arc)
                new_basename = os.path.basename(new_arc)

                # Replace in href, src, xlink:href attributes
                content = content.replace(old_basename, new_basename)

            # Update OPF media-type declarations
            if ext == '.opf':
                # Change media-type="image/svg+xml" to "image/png" for converted files
                for old_arc, new_arc in arc_mapping.items():
                    old_basename = os.path.basename(old_arc)
                    new_basename = os.path.basename(new_arc)
                    # Match: href="media/fileXXX.svg" media-type="image/svg+xml"
                    pattern = f'href="{re.escape(new_basename)}"(\\s+)media-type="image/svg\\+xml"'
                    replacement = f'href="{new_basename}"\\1media-type="image/png"'
                    content = re.sub(pattern, replacement, content)

                    # Also handle: media-type="image/svg+xml" href="..."
                    pattern2 = f'media-type="image/svg\\+xml"(\\s+)href="{re.escape(new_basename)}"'
                    replacement2 = f'media-type="image/png"\\1href="{new_basename}"'
                    content = re.sub(pattern2, replacement2, content)

            if content != original:
                file_path.write_text(content, encoding='utf-8')
                updated_files += 1

    print(f"  Updated references in {updated_files} files")
    return updated_files


def main():
    parser = argparse.ArgumentParser(description="Convert SVGs to PNGs in EPUB for Kindle KPF compatibility")
    parser.add_argument("epub", help="Path to EPUB file")
    parser.add_argument("--output", "-o", help="Output path (default: overwrite input)")
    parser.add_argument("--dpi-scale", type=int, default=DPI_SCALE,
                        help=f"DPI multiplier for rendering (default: {DPI_SCALE})")
    args = parser.parse_args()

    epub_path = Path(args.epub)
    if not epub_path.exists():
        print(f"Error: File not found: {epub_path}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else epub_path

    print(f"\n{'='*70}")
    print(f"EPUB SVG -> PNG Conversion")
    print(f"Input:  {epub_path}")
    print(f"Output: {output_path}")
    print(f"DPI scale: {args.dpi_scale}x (effective {72 * args.dpi_scale} DPI)")
    print(f"{'='*70}\n")

    # Count SVGs first
    with zipfile.ZipFile(epub_path, 'r') as zf:
        svg_entries = [n for n in zf.namelist() if n.lower().endswith('.svg')]

    if not svg_entries:
        print("No SVG files found in EPUB. Nothing to do.")
        sys.exit(0)

    print(f"Found {len(svg_entries)} SVG files in EPUB")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        epub_dir = tmpdir / 'epub_contents'
        svg_extract_dir = tmpdir / 'svgs'
        png_output_dir = tmpdir / 'pngs'

        # Step 1: Extract EPUB
        print("\n[1/5] Extracting EPUB...")
        extract_epub(epub_path, epub_dir)

        # Step 2: Collect SVGs
        print("[2/5] Collecting SVG files...")
        svg_extract_dir.mkdir()
        svg_arcnames = {}  # svg_temp_name -> original archive path relative

        for entry in svg_entries:
            full_path = epub_dir / entry.replace('/', os.sep)
            if full_path.exists():
                # Use a safe temp name
                safe_name = entry.replace('/', '_').replace('\\', '_')
                dest = svg_extract_dir / safe_name
                shutil.copy2(full_path, dest)
                svg_arcnames[safe_name] = entry

        print(f"  Collected {len(svg_arcnames)} SVGs")

        # Step 3: Convert SVGs to PNGs
        print("[3/5] Converting SVGs to PNGs with sharp...")
        svg_to_png = convert_svgs_with_sharp(svg_extract_dir, png_output_dir, args.dpi_scale)

        if not svg_to_png:
            print("  No SVGs were converted. Aborting.")
            sys.exit(1)

        # Step 4: Replace SVG files with PNGs in EPUB directory
        print("[4/5] Replacing SVG files with PNGs...")
        replaced = 0
        for svg_temp_name, png_name in svg_to_png.items():
            if svg_temp_name not in svg_arcnames:
                continue
            arc_path = svg_arcnames[svg_temp_name]
            svg_full = epub_dir / arc_path.replace('/', os.sep)
            png_src = png_output_dir / png_name

            # New path: same location but .png extension
            png_full = svg_full.with_suffix('.png')
            shutil.copy2(png_src, png_full)

            # Remove original SVG
            if svg_full.exists():
                svg_full.unlink()
            replaced += 1

        print(f"  Replaced {replaced} SVG files with PNGs")

        # Step 5: Update references
        print("[5/5] Updating references in XHTML/OPF...")
        update_references(epub_dir, svg_to_png, svg_arcnames)

        # Repack
        print("\nRepacking EPUB...")
        repack_epub(epub_dir, output_path)

    # Report
    original_size = epub_path.stat().st_size / (1024 * 1024)
    output_size = output_path.stat().st_size / (1024 * 1024)

    # Verify SVG count
    with zipfile.ZipFile(output_path, 'r') as zf:
        remaining_svgs = [n for n in zf.namelist() if n.lower().endswith('.svg')]

    print(f"\n{'='*70}")
    print(f"Done!")
    print(f"  Original size: {original_size:.1f} MB")
    print(f"  Output size:   {output_size:.1f} MB")
    print(f"  SVGs remaining: {len(remaining_svgs)} (was {len(svg_entries)})")
    if len(remaining_svgs) <= 25:
        print(f"  Enhanced Typesetting: ELIGIBLE (under 25 SVG limit)")
    else:
        print(f"  Enhanced Typesetting: STILL BLOCKED ({len(remaining_svgs)} > 25 SVGs)")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
