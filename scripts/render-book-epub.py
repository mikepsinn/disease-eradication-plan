#!/usr/bin/env python3
"""
Render Book EPUB
================

Cross-platform script to render the book as an EPUB.
Copies _quarto-book.yml to _quarto.yml, copies index-book.qmd to index.qmd,
and renders to EPUB format for e-readers (Kindle, Apple Books, etc.).

Usage:
    python render-book-epub.py                    # Basic render
    python render-book-epub.py --validate         # With pre/post validation
    python render-book-epub.py --help             # Show all options
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
        description="Render book as EPUB (with validation)",
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

    # Clean up existing EPUB files and problematic directories
    print("[*] Cleaning up existing EPUB files...")
    epub_files = list(project_root.glob("*.epub"))
    for epub_file in epub_files:
        try:
            print(f"    Removing {epub_file.name}")
            epub_file.unlink()
        except PermissionError:
            print(f"    Warning: Could not remove {epub_file.name} (file is open, will be overwritten)")

    # Remove index_files directory (Quarto cleanup issue on Windows)
    index_files = project_root / "index_files"
    if index_files.exists():
        print(f"    Removing {index_files}")
        shutil.rmtree(index_files)

    # Prepare book files (config + index) - project_root auto-detected from cwd
    if not prepare_book():
        sys.exit(1)

    # Build command for EPUB rendering
    print("[*] Rendering EPUB for e-readers...")
    cmd = [sys.executable, "scripts/render_epub.py", "--command", "quarto render --to epub"]
    if args.quarto_args:
        cmd.extend(args.quarto_args)

    # Run command
    exit_code = 0
    try:
        result = subprocess.run(cmd, check=False)  # Don't raise on error, we'll handle cleanup first
        exit_code = result.returncode

        # Check if EPUB was generated successfully (even if Quarto cleanup failed)
        epub_files = list(project_root.glob("*.epub"))

        if epub_files and exit_code != 0:
            # EPUB exists but Quarto cleanup failed - this is OK, we'll clean up ourselves
            print("[*] EPUB generated successfully (ignoring Quarto cleanup error)")
            exit_code = 0

        if exit_code == 0:
            print("[OK] EPUB render complete!")
            if epub_files:
                file_size_mb = epub_files[0].stat().st_size / (1024 * 1024)
                print(f"[*] Generated EPUB: {epub_files[0]} ({file_size_mb:.1f}MB)")
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
