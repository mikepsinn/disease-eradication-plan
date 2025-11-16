#!/usr/bin/env python3
"""
Render Complete Book
====================

Cross-platform script to render the complete book.
Copies _quarto-book.yml to _quarto.yml and renders the book.

Usage:
    python render-book.py                    # Basic render
    python render-book.py --validate         # With pre/post validation
    python render-book.py --help             # Show all options
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Render complete book',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--validate', action='store_true',
                        help='Use render_html.py with validation (recommended)')
    parser.add_argument('--output-dir', type=str, default='_book/warondisease',
                        help='Output directory (default: _book/warondisease)')
    parser.add_argument('quarto_args', nargs='*',
                        help='Additional arguments to pass to quarto render')

    args = parser.parse_args()

    # Get script directory (project root)
    project_root = Path(__file__).parent.absolute()
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

    # Build command
    if args.validate:
        # Use validated render with pre/post checks
        print("[*] Rendering with validation...")
        cmd = [
            sys.executable,
            'tools/render_html.py',
            '--output-dir', args.output_dir,
            '--command', 'quarto render'
        ]
        if args.quarto_args:
            cmd.extend(args.quarto_args)
    else:
        # Simple quarto render
        print("[*] Rendering complete book...")
        cmd = ['quarto', 'render'] + args.quarto_args

    # Run command
    try:
        result = subprocess.run(cmd, check=True)
        print("[OK] Render complete!")
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
