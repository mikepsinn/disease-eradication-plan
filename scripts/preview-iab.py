#!/usr/bin/env python3
"""
Preview IAB Paper Site
======================

Quickly start preview server for the Incentive Alignment Bonds paper website.
Copies _quarto-iab.yml to _quarto.yml, copies incentive-alignment-bonds-paper.qmd to index.qmd
(with updated relative paths), runs pre-render validation, and starts live preview.

Usage:
    python scripts/preview-iab.py                # Start preview server
    python scripts/preview-iab.py --port 4200    # Custom port
    python scripts/preview-iab.py --help         # Show all options
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from quarto_prep import prepare_iab


def main():
    parser = argparse.ArgumentParser(
        description="Preview IAB paper website with live reload",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--port", type=int, help="Port for preview server (default: Quarto chooses)")
    parser.add_argument("--host", type=str, help="Host for preview server (default: localhost)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    parser.add_argument("quarto_args", nargs="*", help="Additional arguments to pass to quarto preview")

    args = parser.parse_args()

    # Get project root (parent of scripts directory) and change to it
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    # Prepare IAB files (config + index) - project_root auto-detected from cwd
    if not prepare_iab():
        sys.exit(1)

    # Run pre-render validation to catch errors early
    print("[*] Running pre-render validation...")
    validation_script = project_root / "scripts" / "pre-render-validation.py"
    try:
        result = subprocess.run(
            [sys.executable, str(validation_script)],
            check=False,
            capture_output=False,  # Let validation output go to console
        )
        if result.returncode != 0:
            print(f"\n[ERROR] Pre-render validation failed with exit code {result.returncode}", file=sys.stderr)
            print("        Please fix validation errors before starting preview.", file=sys.stderr)
            sys.exit(result.returncode)
        print("[OK] Pre-render validation passed!\n")
    except FileNotFoundError:
        print("[WARNING] Pre-render validation script not found, skipping validation", file=sys.stderr)
        print(f"        Expected: {validation_script}", file=sys.stderr)
    except Exception as e:
        print(f"[ERROR] Failed to run pre-render validation: {e}", file=sys.stderr)
        sys.exit(1)

    # Build preview command
    cmd = ["quarto", "preview"]

    if args.port:
        cmd.extend(["--port", str(args.port)])
    if args.host:
        cmd.extend(["--host", args.host])
    if args.no_browser:
        cmd.append("--no-browser")

    cmd.extend(args.quarto_args)

    # Start preview server
    print("[*] Starting preview server for IAB paper site...")
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


if __name__ == "__main__":
    main()
