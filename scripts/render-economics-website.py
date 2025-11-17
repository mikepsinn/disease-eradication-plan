#!/usr/bin/env python3
"""
Render Economics Website
=========================

Cross-platform script to render the economics models as an HTML website.
Copies _quarto-economics.yml to _quarto.yml and renders to HTML.

Usage:
    python render-economics-website.py                    # Basic render
    python render-economics-website.py --validate         # With pre/post validation
    python render-economics-website.py --help             # Show all options
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Render economics models as HTML website (with validation)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--output-dir', type=str, default='_site',
                        help='Output directory (default: _site)')
    parser.add_argument('quarto_args', nargs='*',
                        help='Additional arguments to pass to quarto render')

    args = parser.parse_args()

    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    # Config files
    econ_config = project_root / '_quarto-economics.yml'
    quarto_yml = project_root / '_quarto.yml'

    # Check if economics config exists
    if not econ_config.exists():
        print(f"[ERROR] Missing {econ_config}", file=sys.stderr)
        print("        Unable to render economics website.", file=sys.stderr)
        sys.exit(1)

    # Copy config
    print(f"[*] Copying {econ_config.name} -> _quarto.yml")
    shutil.copy2(econ_config, quarto_yml)

    # Build command for HTML rendering with validation
    print("[*] Rendering economics HTML website with validation...")
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
        print("[OK] Economics website render complete!")
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
