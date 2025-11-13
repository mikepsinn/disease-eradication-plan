#!/usr/bin/env python3
"""
Render script for DIH Economic Models Quarto site
- Renders the economic models standalone site
- Logs to build-submodule.log
- Can be called independently or from main project
"""

import sys
import os
import subprocess
from datetime import datetime

def main():
    """Render the DIH Economic Models site"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Render DIH Economic Models HTML site'
    )
    parser.add_argument('--timeout', type=int, default=300,
                        help='Seconds with no output before killing build (default: 300)')
    parser.add_argument('--no-fail-on-warnings', action='store_true',
                        help='Do not fail build on warnings')
    parser.add_argument('--log-file', type=str, default='build-submodule.log',
                        help='Log file path (default: build-submodule.log)')

    args = parser.parse_args()

    # Get the submodule root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    submodule_root = os.path.dirname(script_dir)  # Go up from scripts/ to root

    # Change to submodule directory
    original_cwd = os.getcwd()
    os.chdir(submodule_root)

    print("=" * 80, flush=True)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] RENDERING DIH ECONOMIC MODELS", flush=True)
    print(f"Working directory: {os.getcwd()}", flush=True)
    print("=" * 80, flush=True)

    # Build command
    command = ['quarto', 'render', '.', '--to', 'html']

    # Run the build
    try:
        with open(args.log_file, 'w') as log_file:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            warning_count = 0

            for line in iter(process.stdout.readline, ''):
                if not line:
                    break

                # Write to log file
                log_file.write(line)
                log_file.flush()

                # Print to console
                print(line, end='', flush=True)

                # Count warnings
                if 'WARNING' in line or 'Warning' in line:
                    warning_count += 1

            process.wait()
            exit_code = process.returncode

            print("=" * 80, flush=True)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Render completed", flush=True)
            print(f"Exit code: {exit_code}", flush=True)
            print(f"Warnings: {warning_count}", flush=True)
            print("=" * 80, flush=True)

            # Change back to original directory
            os.chdir(original_cwd)

            # Check if we should fail on warnings
            if exit_code == 0 and warning_count > 0 and not args.no_fail_on_warnings:
                print(f"Build succeeded but found {warning_count} warnings. Failing due to warnings.", flush=True)
                sys.exit(1)

            sys.exit(exit_code)

    except Exception as e:
        print(f"ERROR: Failed to render: {e}", flush=True)
        os.chdir(original_cwd)
        sys.exit(1)

if __name__ == '__main__':
    main()
