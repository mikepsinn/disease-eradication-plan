#!/usr/bin/env python3
"""
Render Book Website
===================

Cross-platform script to render the book as an HTML website.
Copies _quarto-book.yml to _quarto.yml and renders to HTML.

Usage:
    python render-book-website.py                    # Basic render
    python render-book-website.py --validate         # With pre/post validation
    python render-book-website.py --help             # Show all options
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Render book as HTML website (with validation)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--output-dir', type=str, default='_book/warondisease',
                        help='Output directory (default: _book/warondisease)')
    parser.add_argument('quarto_args', nargs='*',
                        help='Additional arguments to pass to quarto render')

    args = parser.parse_args()

    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    # Config files
    book_config = project_root / '_quarto-book.yml'
    quarto_yml = project_root / '_quarto.yml'

    # Check if book config exists
    if not book_config.exists():
        print(f"[ERROR] Missing {book_config}", file=sys.stderr)
        print("        Unable to render book.", file=sys.stderr)
        sys.exit(1)

    # Copy config
    print(f"[*] Copying {book_config.name} -> _quarto.yml")
    shutil.copy2(book_config, quarto_yml)

    # Build command for HTML rendering with validation
    print("[*] Rendering HTML website with validation...")
    cmd = [
        sys.executable,
        'scripts/render_html.py',
        '--output-dir', args.output_dir,
        '--command', 'quarto render --to html'
    ]
    if args.quarto_args:
        cmd.extend(args.quarto_args)

    # Run command
    try:
        result = subprocess.run(cmd, check=True)
        print("[OK] Website render complete!")
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Render failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        print("        Make sure Quarto is installed and in your PATH", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
