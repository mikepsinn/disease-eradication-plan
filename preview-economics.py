#!/usr/bin/env python3
"""
Preview Economics Models Site
==============================

Quickly start preview server for the economics models website.
Copies _quarto-economics.yml to _quarto.yml and starts live preview.

Usage:
    python preview-economics.py                # Start preview server
    python preview-economics.py --port 4200    # Custom port
    python preview-economics.py --help         # Show all options
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Preview economics models website with live reload',
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

    # Get script directory (project root)
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)

    # Config files
    econ_config = project_root / '_quarto-economics.yml'
    quarto_yml = project_root / '_quarto.yml'

    # Check if economics config exists
    if not econ_config.exists():
        print(f"[ERROR] Missing {econ_config}", file=sys.stderr)
        print("        Unable to preview economics website.", file=sys.stderr)
        sys.exit(1)

    # Copy config
    print(f"[*] Copying {econ_config.name} -> _quarto.yml")
    shutil.copy2(econ_config, quarto_yml)

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
    print("[*] Starting preview server for economics models site...")
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
