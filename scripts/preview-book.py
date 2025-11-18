#!/usr/bin/env python3
"""
Preview Complete Book
=====================

Quickly start preview server for the complete book.
Copies _quarto-book.yml to _quarto.yml and starts live preview.

Usage:
    python scripts/preview-book.py                # Start preview server
    python scripts/preview-book.py --port 4200    # Custom port
    python scripts/preview-book.py --help         # Show all options
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Preview complete book with live reload',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--port', type=int,
                        help='Port for preview server (default: Quarto chooses)')
    parser.add_argument('--host', type=str,
                        help='Host for preview server (default: localhost)')
    parser.add_argument('--no-browser', action='store_true',
                        help='Do not open browser automatically')
    parser.add_argument('quarto_args', nargs='*',
                        help='Additional arguments to pass to quarto preview')

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
        print("        Unable to preview book.", file=sys.stderr)
        sys.exit(1)

    # Copy config
    print(f"[*] Copying {book_config.name} -> _quarto.yml", flush=True)
    shutil.copy2(book_config, quarto_yml)

    # Build preview command
    cmd = ['quarto', 'preview']

    if args.port:
        cmd.extend(['--port', str(args.port)])
    if args.host:
        cmd.extend(['--host', args.host])
    if args.no_browser:
        cmd.append('--no-browser')

    cmd.extend(args.quarto_args)

    # Start preview server
    print("[*] Starting preview server for complete book...")
    print(f"[*] Command: {' '.join(cmd)}")
    print()

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n[*] Preview server stopped")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Preview failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("[ERROR] Quarto not found", file=sys.stderr)
        print("        Make sure Quarto is installed and in your PATH", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
