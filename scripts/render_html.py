#!/usr/bin/env python3
"""
Unified HTML render script for Quarto HTML generation
- Runs pre-validation automatically
- Logs to both console and file
- Detects warnings and errors in real-time
- Times out if stuck on a step too long
- Fails fast on critical errors
- Provides progress updates
"""

import sys
import os

# Add scripts/lib to path so we can import render_utils
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, 'lib')
sys.path.insert(0, lib_dir)

from render_utils import BuildMonitor, kill_existing_quarto_processes, run_pre_validation, run_post_validation


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Unified HTML render script with validation, logging, and monitoring'
    )
    parser.add_argument('--timeout', type=int, default=300,
                        help='Seconds with no output before killing build (default: 300)')
    parser.add_argument('--no-fail-on-warnings', action='store_true',
                        help='Do not fail build on warnings (warnings fail by default)')
    parser.add_argument('--skip-validation', action='store_true',
                        help='Skip pre-render validation')
    parser.add_argument('--skip-post-validation', action='store_true',
                        help='Skip post-render validation')
    parser.add_argument('--output-dir', type=str, default='_book/warondisease',
                        help='Output directory for post-validation (default: _book/warondisease)')
    parser.add_argument('--log-file', type=str, default='build-html.log',
                        help='Log file path (default: build-html.log)')
    parser.add_argument('--command', type=str, default='quarto render . --to html',
                        help='Build command to run (default: quarto render . --to html)')
    parser.add_argument('--kill-existing', action='store_true',
                        help='Kill all existing Quarto processes before starting build')

    args = parser.parse_args()

    # Force output flush to ensure GitHub Actions sees output immediately
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    # Log script start immediately
    from datetime import datetime
    print("=" * 80, flush=True)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting HTML render script", flush=True)
    print("=" * 80, flush=True)

    # Kill existing Quarto processes if requested
    if args.kill_existing:
        print("=" * 80, flush=True)
        print("KILLING EXISTING QUARTO PROCESSES", flush=True)
        print("=" * 80, flush=True)
        kill_existing_quarto_processes(include_latex=False)
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
        timeout_seconds=args.timeout,
        fail_on_warnings=not args.no_fail_on_warnings,
        log_file=args.log_file
    )

    exit_code = monitor.run_build(command, build_type="HTML render")

    # Run post-validation if build succeeded and not skipped
    if exit_code == 0 and not args.skip_post_validation:
        validation_exit_code = run_post_validation(output_dir=args.output_dir)
        if validation_exit_code != 0:
            sys.exit(validation_exit_code)

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
