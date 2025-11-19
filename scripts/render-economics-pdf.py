#!/usr/bin/env python3
"""
Render Economics PDF
====================

Cross-platform script to render the economics models as a PDF.
Copies _quarto-economics.yml to _quarto.yml, copies economics.qmd to index.qmd
(with updated relative paths), and renders to PDF.

Usage:
    python render-economics-pdf.py                    # Basic render
    python render-economics-pdf.py --validate         # With pre/post validation
    python render-economics-pdf.py --help             # Show all options
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from quarto_prep import prepare_economics


def main():
    parser = argparse.ArgumentParser(
        description='Render economics models as PDF (with validation)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--output-dir', type=str, default='_site',
                        help='Output directory (default: _site)')
    parser.add_argument('quarto_args', nargs='*',
                        help='Additional arguments to pass to quarto render')

    args = parser.parse_args()

    # Get project root (parent of scripts directory) and change to it
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    # Prepare economics files (config + index) - project_root auto-detected from cwd
    if not prepare_economics():
        sys.exit(1)

    # Build command for PDF rendering with validation
    print("[*] Rendering economics PDF with validation...")
    cmd = [
        sys.executable,
        'scripts/render_pdf.py',
        '--command', 'quarto render --to pdf'
    ]
    if args.quarto_args:
        cmd.extend(args.quarto_args)

    # Run command
    try:
        result = subprocess.run(cmd, check=True)
        print("[OK] Economics PDF render complete!")
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
