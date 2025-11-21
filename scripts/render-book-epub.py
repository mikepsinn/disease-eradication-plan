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

    # Prepare book files (config + index) - project_root auto-detected from cwd
    if not prepare_book():
        sys.exit(1)

    # Build command for EPUB rendering
    print("[*] Rendering EPUB for e-readers...")
    cmd = [sys.executable, "scripts/render_epub.py", "--command", "quarto render --to epub"]
    if args.quarto_args:
        cmd.extend(args.quarto_args)

    # Run command
    try:
        result = subprocess.run(cmd, check=True)
        print("[OK] EPUB render complete!")

        # Find and display the generated EPUB file
        output_dir = Path(args.output_dir)
        epub_files = list(output_dir.glob("*.epub"))
        if epub_files:
            print(f"[*] Generated EPUB: {epub_files[0]}")

        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Render failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        print("        Make sure Quarto is installed and in your PATH", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
