#!/usr/bin/env python3
"""
Unified PDF render script for Quarto PDF generation
- Runs pre-validation automatically
- Logs to both console and file
- Detects warnings and errors in real-time
- Times out if stuck on a step too long
- Fails fast on critical errors
- Provides progress updates
"""

import subprocess
import sys
import re
import time
import os
import threading
import platform
from datetime import datetime
from typing import Optional

class BuildMonitor:
    def __init__(self, timeout_seconds: int = 180, fail_on_warnings: bool = True, log_file: str = "build-pdf.log"):
        """
        Initialize the build monitor

        Args:
            timeout_seconds: Max seconds with no output before killing build (default 180)
            fail_on_warnings: Whether to fail build on warnings (default True)
            log_file: Path to log file (default "build-pdf.log")
        """
        self.timeout_seconds = timeout_seconds
        self.fail_on_warnings = fail_on_warnings
        self.log_file = log_file
        self.warnings = []
        self.errors = []
        self.current_file = None
        self.last_output_time = time.time()
        self.file_count = 0
        self.total_files = 110
        self.timed_out = False
        self.process = None
        self.timeout_thread = None
        self.stop_timeout_check = threading.Event()

        # Open log file
        self.log_handle = open(self.log_file, 'w', encoding='utf-8')

    def __del__(self):
        """Close log file on cleanup"""
        if hasattr(self, 'log_handle'):
            self.log_handle.close()

    def log(self, message: str, to_stderr: bool = False):
        """Log message to both console and file"""
        output = sys.stderr if to_stderr else sys.stdout
        print(message, file=output)
        self.log_handle.write(message + '\n')
        self.log_handle.flush()

    def parse_line(self, line: str) -> Optional[str]:
        """Parse a line of output and extract relevant information"""
        # Match file progress: [ 42/110] path/to/file.qmd
        file_match = re.match(r'\[\s*(\d+)/(\d+)\]\s+(.+\.qmd)', line)
        if file_match:
            self.file_count = int(file_match.group(1))
            self.total_files = int(file_match.group(2))
            self.current_file = file_match.group(3)
            return f"[{self.file_count}/{self.total_files}] {self.current_file}"

        # Match LaTeX compilation phases
        if re.match(r'running lualatex - \d+', line):
            return f"LaTeX compilation: {line.strip()}"

        # Match output creation
        if line.startswith('Output created:'):
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
        """Check if build has timed out (no output for timeout_seconds)"""
        elapsed = time.time() - self.last_output_time
        if elapsed > self.timeout_seconds:
            return True
        return False

    def timeout_watchdog(self):
        """Background thread that monitors for timeout even when no output is produced"""
        while not self.stop_timeout_check.wait(1.0):  # Check every second
            if self.check_timeout():
                self.timed_out = True
                if self.process and self.process.poll() is None:
                    self.log(f"\nERROR: Build timed out after {self.timeout_seconds}s with no output", to_stderr=True)
                    if self.current_file:
                        self.log(f"Last file being processed: {self.current_file}", to_stderr=True)
                    self.process.kill()
                break

    def run_build(self, command: list[str]) -> int:
        """
        Run the build command with monitoring

        Args:
            command: Command to execute as list (e.g., ['quarto', 'render', '.', '--to', 'pdf'])

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        self.log(f"Starting PDF render: {' '.join(command)}")
        self.log(f"Timeout (no output): {self.timeout_seconds}s")
        self.log(f"Fail on warnings: {self.fail_on_warnings}")
        self.log(f"Log file: {self.log_file}")
        self.log("-" * 80)

        try:
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Start timeout watchdog thread
            self.timeout_thread = threading.Thread(target=self.timeout_watchdog, daemon=True)
            self.timeout_thread.start()

            for line in self.process.stdout:
                # Update last output time (ANY output resets the timeout)
                self.last_output_time = time.time()

                # Write raw line to log file
                self.log_handle.write(line)
                self.log_handle.flush()

                # Print all output to console as well
                print(line, end='')

                # Parse and extract relevant information for summary
                parsed = self.parse_line(line)
                # Note: parsed info is already printed above, this is just for tracking

                # Check if watchdog killed the process
                if self.timed_out:
                    return 124  # Timeout exit code

            # Wait for process to complete
            return_code = self.process.wait()

            # Stop the timeout watchdog
            self.stop_timeout_check.set()
            if self.timeout_thread:
                self.timeout_thread.join(timeout=2.0)

            # Check if we timed out
            if self.timed_out:
                return 124

            # Print summary
            self.log("\n" + "=" * 80)
            self.log("BUILD SUMMARY")
            self.log("=" * 80)
            self.log(f"Exit code: {return_code}")
            self.log(f"Warnings: {len(self.warnings)}")
            self.log(f"Errors: {len(self.errors)}")

            if self.warnings:
                self.log("\nWarnings detected:")
                for warning in self.warnings[:10]:  # Show first 10
                    self.log(f"  - {warning}")
                if len(self.warnings) > 10:
                    self.log(f"  ... and {len(self.warnings) - 10} more")

            if self.errors:
                self.log("\nErrors detected:")
                for error in self.errors[:10]:  # Show first 10
                    self.log(f"  - {error}")
                if len(self.errors) > 10:
                    self.log(f"  ... and {len(self.errors) - 10} more")

            # Decide final exit code
            if return_code != 0:
                return return_code

            if self.fail_on_warnings and self.warnings:
                self.log("\nBuild failed due to warnings (fail_on_warnings=True)", to_stderr=True)
                return 1

            if self.errors:
                self.log("\nBuild failed due to errors", to_stderr=True)
                return 1

            self.log("\nBuild completed successfully!")
            return 0

        except KeyboardInterrupt:
            self.log("\nBuild interrupted by user", to_stderr=True)
            self.stop_timeout_check.set()
            if self.process and self.process.poll() is None:
                self.process.kill()
            return 130
        except Exception as e:
            self.log(f"\nUnexpected error: {e}", to_stderr=True)
            self.stop_timeout_check.set()
            if self.process and self.process.poll() is None:
                self.process.kill()
            return 1

def kill_existing_quarto_processes() -> int:
    """
    Kill all existing Quarto and related LaTeX processes before starting a new build
    
    Returns:
        Number of processes killed
    """
    killed_count = 0
    
    try:
        system = platform.system()
        
        if system == 'Windows':
            # Windows: Use taskkill to kill quarto.exe and related processes
            processes_to_kill = ['quarto.exe', 'lualatex.exe', 'pdflatex.exe', 'xelatex.exe']
            for proc_name in processes_to_kill:
                try:
                    result = subprocess.run(
                        ['taskkill', '/F', '/IM', proc_name, '/T'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    # Count processes killed (taskkill returns 0 if processes were found and killed)
                    if result.returncode == 0:
                        # Parse output to count killed processes
                        output_lines = result.stdout.split('\n')
                        for line in output_lines:
                            if 'terminated' in line.lower() or 'killed' in line.lower():
                                killed_count += 1
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
        else:
            # Unix-like: Use pkill or killall
            processes_to_kill = ['quarto', 'lualatex', 'pdflatex', 'xelatex']
            for proc_name in processes_to_kill:
                try:
                    # Try pkill first
                    subprocess.run(['pkill', '-9', proc_name], 
                                 capture_output=True, timeout=5)
                    # Try killall as backup
                    subprocess.run(['killall', '-9', proc_name], 
                                 capture_output=True, timeout=5)
                    killed_count += 1
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
        
        if killed_count > 0:
            print(f"Killed {killed_count} existing Quarto/LaTeX process(es)")
            time.sleep(1)  # Give processes time to fully terminate
        
        return killed_count
    except Exception as e:
        print(f"Warning: Could not kill existing processes: {e}", file=sys.stderr)
        return 0

def run_pre_validation() -> int:
    """
    Run pre-validation script before building

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    print("=" * 80)
    print("RUNNING PRE-VALIDATION")
    print("=" * 80)

    script_path = os.path.join(os.path.dirname(__file__), 'pre-render-validation.py')

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=False,
            capture_output=False
        )

        if result.returncode != 0:
            print(f"\nPre-validation failed with exit code {result.returncode}", file=sys.stderr)
            return result.returncode

        print("\nPre-validation passed!")
        print("=" * 80)
        return 0
    except Exception as e:
        print(f"\nError running pre-validation: {e}", file=sys.stderr)
        return 1

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Unified PDF render script with validation, logging, and monitoring'
    )
    parser.add_argument('--timeout', type=int, default=180,
                        help='Seconds with no output before killing build (default: 180)')
    parser.add_argument('--no-fail-on-warnings', action='store_true',
                        help='Do not fail build on warnings (warnings fail by default)')
    parser.add_argument('--skip-validation', action='store_true',
                        help='Skip pre-render validation')
    parser.add_argument('--log-file', type=str, default='build-pdf.log',
                        help='Log file path (default: build-pdf.log)')
    parser.add_argument('--command', type=str, default='quarto render . --to pdf',
                        help='Build command to run (default: quarto render . --to pdf)')
    parser.add_argument('--kill-existing', action='store_true',
                        help='Kill all existing Quarto/LaTeX processes before starting build')

    args = parser.parse_args()

    # Kill existing Quarto processes if requested
    if args.kill_existing:
        print("=" * 80)
        print("KILLING EXISTING QUARTO/LaTeX PROCESSES")
        print("=" * 80)
        kill_existing_quarto_processes()
        print("=" * 80)

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

    exit_code = monitor.run_build(command)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
