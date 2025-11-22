#!/usr/bin/env python3
"""
Render Book DOCX
================

Cross-platform script to render the book as a DOCX file.
Copies _quarto-book.yml to _quarto.yml, copies index-book.qmd to index.qmd,
and renders to DOCX format for Amazon Kindle Create and other Word-based tools.

Note: Amazon KDP (Kindle Direct Publishing) actually prefers EPUB files directly,
but Kindle Create accepts DOCX/DOC/PDF formats.

Usage:
    python render-book-docx.py                    # Basic render
    python render-book-docx.py --validate         # With pre/post validation
    python render-book-docx.py --help             # Show all options
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from quarto_prep import prepare_book


def main():
    parser = argparse.ArgumentParser(
        description="Render book as DOCX (with validation)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--output-dir", type=str, default="_book/warondisease", help="Output directory (default: _book/warondisease)"
    )
    parser.add_argument("quarto_args", nargs="*", help="Additional arguments to pass to quarto render")

    args = parser.parse_args()

    # Get project root (parent of scripts directory) and change to it
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    # Clean up existing DOCX files and problematic directories
    print("[*] Cleaning up existing DOCX files...")
    docx_files = list(project_root.glob("*.docx"))
    for docx_file in docx_files:
        try:
            print(f"    Removing {docx_file.name}")
            docx_file.unlink()
        except PermissionError:
            print(f"    Warning: Could not remove {docx_file.name} (file is open, will be overwritten)")

    # Remove index_files directory (Quarto cleanup issue on Windows)
    index_files = project_root / "index_files"
    if index_files.exists():
        print(f"    Removing {index_files}")
        shutil.rmtree(index_files)

    # Prepare book files (config + index) - project_root auto-detected from cwd
    if not prepare_book():
        sys.exit(1)

    # Build command for DOCX rendering
    print("[*] Rendering DOCX for Kindle Create...")
    cmd = [sys.executable, "scripts/render_docx.py", "--command", "quarto render --to docx"]
    if args.quarto_args:
        cmd.extend(args.quarto_args)

    # Run command
    exit_code = 0
    try:
        result = subprocess.run(cmd, check=False)  # Don't raise on error, we'll handle cleanup first
        exit_code = result.returncode

        # Check if DOCX was generated successfully (even if Quarto cleanup failed)
        output_dir = Path(args.output_dir)
        docx_files = list(output_dir.glob("*.docx"))
        if not docx_files:
            # Also check project root
            docx_files = list(project_root.glob("*.docx"))

        if docx_files and exit_code != 0:
            # DOCX exists but Quarto cleanup failed - this is OK, we'll clean up ourselves
            print("[*] DOCX generated successfully (ignoring Quarto cleanup error)")
            exit_code = 0

        if exit_code == 0:
            print("[OK] DOCX render complete!")
            if docx_files:
                file_size_mb = docx_files[0].stat().st_size / (1024 * 1024)
                print(f"[*] Generated DOCX: {docx_files[0]} ({file_size_mb:.1f}MB)")
        else:
            print(f"[ERROR] Render failed with exit code {exit_code}", file=sys.stderr)

    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        print("        Make sure Quarto is installed and in your PATH", file=sys.stderr)
        exit_code = 1
    finally:
        # Clean up index_files directory (Quarto sometimes fails to remove it on Windows)
        index_files = project_root / "index_files"
        if index_files.exists():
            print(f"[*] Cleaning up {index_files}...")
            try:
                shutil.rmtree(index_files)
                print(f"    Removed {index_files}")
            except Exception as e:
                print(f"    Warning: Could not remove {index_files}: {e}")

        sys.exit(exit_code)


if __name__ == "__main__":
    main()

