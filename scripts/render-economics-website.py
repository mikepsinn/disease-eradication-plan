#!/usr/bin/env python3
"""
Render Economics Website
=========================

Cross-platform script to render the economics models as an HTML website.
Copies _quarto-economics.yml to _quarto.yml, copies economics.qmd to index.qmd
(with updated relative paths), and renders to HTML.

Usage:
    python render-economics-website.py                    # Basic render
    python render-economics-website.py --validate         # With pre/post validation
    python render-economics-website.py --help             # Show all options
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from quarto_prep import prepare_economics


def main():
    parser = argparse.ArgumentParser(
        description="Render economics models as HTML website (with validation)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="_site/economics",
        help="Output directory (default: _site/economics to match _quarto-economics.yml)",
    )
    parser.add_argument("quarto_args", nargs="*", help="Additional arguments to pass to quarto render")

    args = parser.parse_args()

    # Get project root (parent of scripts directory) and change to it
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    # Prepare economics files (config + index) - project_root auto-detected from cwd
    if not prepare_economics():
        sys.exit(1)

    # Build command for HTML rendering with validation
    print("[*] Rendering economics HTML website with validation...")
    cmd = [
        sys.executable,
        "scripts/render_html.py",
        "--output-dir",
        args.output_dir,
        "--command",
        "quarto render --to html",
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


if __name__ == "__main__":
    main()
