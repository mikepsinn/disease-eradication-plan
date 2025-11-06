#!/usr/bin/env python3
"""
Monitored build script for Quarto PDF generation
- Detects warnings and errors in real-time
- Times out if stuck on a step too long
- Fails fast on critical errors
- Provides progress updates
"""

import subprocess
import sys
import re
import time
from datetime import datetime
from typing import Optional

class BuildMonitor:
    def __init__(self, timeout_per_file: int = 120, fail_on_warnings: bool = False):
        """
        Initialize the build monitor

        Args:
            timeout_per_file: Max seconds allowed per file (default 120)
            fail_on_warnings: Whether to fail build on warnings (default False)
        """
        self.timeout_per_file = timeout_per_file
        self.fail_on_warnings = fail_on_warnings
        self.warnings = []
        self.errors = []
        self.current_file = None
        self.last_progress_time = time.time()
        self.file_count = 0
        self.total_files = 110

    def parse_line(self, line: str) -> Optional[str]:
        """Parse a line of output and extract relevant information"""
        # Match file progress: [ 42/110] path/to/file.qmd
        file_match = re.match(r'\[\s*(\d+)/(\d+)\]\s+(.+\.qmd)', line)
        if file_match:
            self.file_count = int(file_match.group(1))
            self.total_files = int(file_match.group(2))
            self.current_file = file_match.group(3)
            self.last_progress_time = time.time()
            return f"[{self.file_count}/{self.total_files}] {self.current_file}"

        # Match LaTeX compilation phases
        if re.match(r'running lualatex - \d+', line):
            self.last_progress_time = time.time()
            return f"LaTeX compilation: {line.strip()}"

        # Match output creation
        if line.startswith('Output created:'):
            self.last_progress_time = time.time()
            return line.strip()

        # Detect warnings
        if line.startswith('WARN:') or 'Warning:' in line:
            self.warnings.append(line.strip())
            return f"WARNING: {line.strip()}"

        # Detect errors
        if line.startswith('ERROR:') or line.startswith('Error:') or 'error:' in line.lower():
            self.errors.append(line.strip())
            return f"ERROR: {line.strip()}"

        return None

    def check_timeout(self) -> bool:
        """Check if current operation has timed out"""
        elapsed = time.time() - self.last_progress_time
        if elapsed > self.timeout_per_file:
            return True
        return False

    def run_build(self, command: list[str]) -> int:
        """
        Run the build command with monitoring

        Args:
            command: Command to execute as list (e.g., ['pnpm', 'run', 'build:pdf'])

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        print(f"Starting monitored build: {' '.join(command)}")
        print(f"Timeout per file: {self.timeout_per_file}s")
        print(f"Fail on warnings: {self.fail_on_warnings}")
        print("-" * 80)

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                # Check for timeout
                if self.check_timeout():
                    print(f"\nERROR: Build timed out after {self.timeout_per_file}s with no progress", file=sys.stderr)
                    if self.current_file:
                        print(f"Stuck on file: {self.current_file}", file=sys.stderr)
                    process.kill()
                    return 124  # Timeout exit code

                # Parse and display relevant information
                parsed = self.parse_line(line)
                if parsed:
                    print(parsed)

                # Print all output to log file (optional)
                sys.stdout.flush()

            # Wait for process to complete
            return_code = process.wait()

            # Print summary
            print("\n" + "=" * 80)
            print("BUILD SUMMARY")
            print("=" * 80)
            print(f"Exit code: {return_code}")
            print(f"Warnings: {len(self.warnings)}")
            print(f"Errors: {len(self.errors)}")

            if self.warnings:
                print("\nWarnings detected:")
                for warning in self.warnings[:10]:  # Show first 10
                    print(f"  - {warning}")
                if len(self.warnings) > 10:
                    print(f"  ... and {len(self.warnings) - 10} more")

            if self.errors:
                print("\nErrors detected:")
                for error in self.errors[:10]:  # Show first 10
                    print(f"  - {error}")
                if len(self.errors) > 10:
                    print(f"  ... and {len(self.errors) - 10} more")

            # Decide final exit code
            if return_code != 0:
                return return_code

            if self.fail_on_warnings and self.warnings:
                print("\nBuild failed due to warnings (fail_on_warnings=True)", file=sys.stderr)
                return 1

            if self.errors:
                print("\nBuild failed due to errors", file=sys.stderr)
                return 1

            print("\nBuild completed successfully!")
            return 0

        except KeyboardInterrupt:
            print("\nBuild interrupted by user", file=sys.stderr)
            if process:
                process.kill()
            return 130
        except Exception as e:
            print(f"\nUnexpected error: {e}", file=sys.stderr)
            return 1

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Monitor Quarto PDF build with timeout and error detection')
    parser.add_argument('--timeout', type=int, default=120,
                        help='Timeout per file in seconds (default: 120)')
    parser.add_argument('--fail-on-warnings', action='store_true',
                        help='Fail build if warnings are detected')
    parser.add_argument('--command', type=str, default='pnpm run build:pdf',
                        help='Build command to run (default: pnpm run build:pdf)')

    args = parser.parse_args()

    # Parse command into list
    command = args.command.split()

    # Create monitor and run build
    monitor = BuildMonitor(
        timeout_per_file=args.timeout,
        fail_on_warnings=args.fail_on_warnings
    )

    exit_code = monitor.run_build(command)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
