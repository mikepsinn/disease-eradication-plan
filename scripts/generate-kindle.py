#!/usr/bin/env python3
"""Generate Kindle-ready EPUB from the Quarto book.

Full pipeline:
1. Render EPUB via Quarto (optional, skip with --skip-render)
2. Analyze images for issues
3. Fix EPUB for Kindle compatibility (resize images, fix XHTML)
4. Validate Kindle compatibility
5. Convert to MOBI/KPF via Calibre (optional)

Usage:
    python scripts/generate-kindle.py                    # Full pipeline
    python scripts/generate-kindle.py --skip-render      # Fix existing EPUB
    python scripts/generate-kindle.py --convert mobi     # Also convert to MOBI
    python scripts/generate-kindle.py --convert kpf      # Convert to KPF (Kindle Package Format)
    python scripts/generate-kindle.py --validate-only    # Just validate
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import os
import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
EPUB_DIR = PROJECT_DIR / "assets" / "epubs"
EPUB_FILE = EPUB_DIR / "How-to-End-War-and-Disease.epub"
KINDLE_FILE = EPUB_DIR / "How-to-End-War-and-Disease-kindle.epub"
PYTHON = str(PROJECT_DIR / ".venv" / "Scripts" / "python.exe")

# Detect platform for Python path
if not os.path.exists(PYTHON):
    PYTHON = str(PROJECT_DIR / ".venv" / "bin" / "python")
if not os.path.exists(PYTHON):
    PYTHON = sys.executable


def run_step(name: str, cmd: list[str], check: bool = True) -> bool:
    """Run a pipeline step, printing output in real-time."""
    print(f"\n{'='*80}")
    print(f"STEP: {name}")
    print(f"{'='*80}")
    print(f"Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=str(PROJECT_DIR))

    if result.returncode != 0:
        print(f"\n** STEP FAILED: {name} (exit code {result.returncode})")
        if check:
            return False
    else:
        print(f"\n-- Step passed: {name}")

    return True


def render_epub() -> bool:
    """Render EPUB via Quarto."""
    render_script = SCRIPT_DIR / "render-quarto.py"
    if not render_script.exists():
        print(f"Error: render-quarto.py not found at {render_script}")
        print("Attempting direct quarto render...")
        return run_step(
            "Render EPUB",
            ["quarto", "render", "--config", "_quarto-manual.yml", "--to", "epub"],
        )

    return run_step(
        "Render EPUB",
        [PYTHON, "-u", str(render_script), "manual", "--to", "epub"],
    )


def analyze_images(epub_path: str) -> bool:
    """Analyze images in the EPUB."""
    return run_step(
        "Analyze Images",
        [PYTHON, "-u", str(SCRIPT_DIR / "analyze-docx-images.py"), epub_path],
        check=False,  # Don't fail pipeline on analysis - fix step handles it
    )


def fix_epub(input_path: str, output_path: str) -> bool:
    """Fix EPUB for Kindle compatibility."""
    return run_step(
        "Fix EPUB for Kindle",
        [PYTHON, "-u", str(SCRIPT_DIR / "fix-epub-kindle.py"), input_path, "--output", output_path],
    )


def validate_kindle(epub_path: str, strict: bool = False) -> bool:
    """Validate Kindle compatibility."""
    cmd = [PYTHON, "-u", str(SCRIPT_DIR / "validate-kindle-compat.py"), epub_path]
    if strict:
        cmd.append("--strict")
    return run_step("Validate Kindle Compatibility", cmd)


def convert_format(epub_path: str, target_format: str) -> bool:
    """Convert EPUB to another format using Calibre."""
    ebook_convert = shutil.which("ebook-convert")
    if not ebook_convert:
        print(f"\nError: ebook-convert not found. Install Calibre: https://calibre-ebook.com")
        print("  Calibre provides the best EPUB-to-MOBI/AZW3 conversion.")
        return False

    output_path = str(Path(epub_path).with_suffix(f".{target_format}"))

    # Calibre conversion options optimized for Kindle
    cmd = [
        ebook_convert,
        epub_path,
        output_path,
        "--output-profile", "kindle_oasis",
        "--no-inline-toc",
        "--smarten-punctuation",
    ]

    if target_format in ("mobi", "azw3"):
        cmd.extend([
            "--mobi-file-type", "both",  # Generate both KF8 and old MOBI
        ])

    return run_step(f"Convert to {target_format.upper()}", cmd)


def main():
    parser = argparse.ArgumentParser(description="Generate Kindle-ready EPUB")
    parser.add_argument("--skip-render", action="store_true", help="Skip Quarto render, use existing EPUB")
    parser.add_argument("--validate-only", action="store_true", help="Only validate, don't fix")
    parser.add_argument("--convert", choices=["mobi", "azw3", "kpf"], help="Also convert to this format")
    parser.add_argument("--strict", action="store_true", help="Strict validation (warnings = errors)")
    parser.add_argument("--input", help="Input EPUB path (default: auto-detected)")
    parser.add_argument("--output", help="Output EPUB path (default: *-kindle.epub)")
    args = parser.parse_args()

    input_epub = args.input or str(EPUB_FILE)
    output_epub = args.output or str(KINDLE_FILE)

    print(f"Kindle Generation Pipeline")
    print(f"Input:  {input_epub}")
    print(f"Output: {output_epub}")

    # Step 1: Render
    if not args.skip_render and not args.validate_only:
        if not render_epub():
            print("\n** Pipeline failed at render step")
            sys.exit(1)

    # Check input exists
    if not os.path.exists(input_epub):
        print(f"\nError: EPUB not found: {input_epub}")
        print("Run without --skip-render to render first, or specify --input")
        sys.exit(1)

    # Step 2: Analyze (informational)
    if not args.validate_only:
        analyze_images(input_epub)

    # Step 3: Fix
    if not args.validate_only:
        if not fix_epub(input_epub, output_epub):
            print("\n** Pipeline failed at fix step")
            sys.exit(1)
        validate_target = output_epub
    else:
        validate_target = input_epub

    # Step 4: Validate
    passed = validate_kindle(validate_target, strict=args.strict)

    # Step 5: Convert (optional)
    if args.convert and not args.validate_only:
        convert_path = validate_target
        if args.convert == "kpf":
            print("\nNote: KPF conversion requires Kindle Previewer 3.")
            print("  Download: https://www.amazon.com/Kindle-Previewer/b?ie=UTF8&node=21381691011")
            print("  Open the EPUB in Kindle Previewer and export as KPF.")
            print(f"  EPUB ready at: {validate_target}")
        else:
            if not convert_format(convert_path, args.convert):
                print(f"\n** Conversion to {args.convert} failed")
                sys.exit(1)

    # Summary
    print(f"\n{'='*80}")
    print("PIPELINE SUMMARY")
    print(f"{'='*80}")
    if args.validate_only:
        print(f"Validation: {'PASSED' if passed else 'FAILED'}")
    else:
        print(f"Kindle EPUB: {validate_target}")
        print(f"Validation:  {'PASSED' if passed else 'PASSED WITH WARNINGS' if not args.strict else 'FAILED'}")
        file_size_mb = os.path.getsize(validate_target) / (1024 * 1024)
        print(f"File size:   {file_size_mb:.2f}MB")

    if not passed and args.strict:
        sys.exit(1)

    if not args.validate_only:
        print(f"\nNext steps:")
        print(f"  1. Open {validate_target} in Kindle Previewer 3 to verify rendering")
        print(f"  2. Upload to KDP: https://kdp.amazon.com")
        print(f"  3. Or convert: python scripts/generate-kindle.py --skip-render --convert mobi")


if __name__ == "__main__":
    main()
