#!/usr/bin/env python3
"""
Unified EPUB render script for Quarto EPUB generation
- Runs pre-validation automatically
- Logs to both console and file
- Detects warnings and errors in real-time
- Times out if stuck on a step too long
- Fails fast on critical errors
- Provides progress updates

Usage:
    python scripts/render_epub.py                    # Run with all defaults
    python scripts/render_epub.py --skip-validation  # Skip pre-validation
    python scripts/render_epub.py --timeout 1800     # Custom timeout

All parameters are optional - script works with defaults if none provided.
"""

import os
import sys

# Add scripts/lib to path so we can import render_utils
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, "lib")
sys.path.insert(0, lib_dir)

from render_utils import BuildMonitor, run_pre_validation


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Unified EPUB render script with validation, logging, and monitoring")
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Seconds with no output before killing build (default: 900 = 15min for EPUB builds)",
    )
    parser.add_argument(
        "--no-fail-on-warnings", action="store_true", help="Do not fail build on warnings (warnings fail by default)"
    )
    parser.add_argument("--skip-validation", action="store_true", help="Skip pre-render validation")
    parser.add_argument("--log-file", type=str, default="build-epub.log", help="Log file path (default: build-epub.log)")
    parser.add_argument(
        "--command",
        type=str,
        default="quarto render . --to epub",
        help="Build command to run (default: quarto render . --to epub)",
    )

    args = parser.parse_args()

    # Force output flush to ensure GitHub Actions sees output immediately
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    # Log script start immediately
    from datetime import datetime

    print("=" * 80, flush=True)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting EPUB render script", flush=True)
    print("=" * 80, flush=True)

    # Run pre-validation unless skipped
    if not args.skip_validation:
        validation_exit_code = run_pre_validation()
        if validation_exit_code != 0:
            sys.exit(validation_exit_code)

    # Parse command into list
    command = args.command.split()

    # Create monitor and run build
    monitor = BuildMonitor(
        timeout_seconds=args.timeout, fail_on_warnings=not args.no_fail_on_warnings, log_file=args.log_file
    )

    exit_code = monitor.run_build(command, build_type="EPUB render")

    # Check if EPUB was generated
    if exit_code == 0:
        from pathlib import Path

        output_dir = Path("_book/warondisease")
        epub_files = list(output_dir.glob("*.epub"))

        if epub_files:
            epub_path = epub_files[0]
            file_size_mb = epub_path.stat().st_size / (1024 * 1024)
            print("=" * 80, flush=True)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] EPUB generated successfully!", flush=True)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] File: {epub_path}", flush=True)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Size: {file_size_mb:.2f} MB", flush=True)
            print("=" * 80, flush=True)
        else:
            print(f"⚠️  Warning: No EPUB file found in {output_dir}", flush=True)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
