#!/usr/bin/env python3
"""
Shared utilities for Quarto render scripts
"""

import subprocess
import sys
import re
import time
import os
import threading
import platform
from datetime import datetime
from typing import Optional, List, Callable


class BuildMonitor:
    def __init__(self, timeout_seconds: int = 180, fail_on_warnings: bool = True, log_file: str = "build.log"):
        """
        Initialize the build monitor

        Args:
            timeout_seconds: Max seconds with no output before killing build (default 180)
            fail_on_warnings: Whether to fail build on warnings (default True)
            log_file: Path to log file (default "build.log")
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

    def get_timestamp(self) -> str:
        """Get formatted timestamp for log messages"""
        return datetime.now().strftime('%H:%M:%S')
    
    def log(self, message: str, to_stderr: bool = False):
        """Log message to both console and file with timestamp"""
        timestamp = self.get_timestamp()
        formatted_message = f"[{timestamp}] {message}"
        output = sys.stderr if to_stderr else sys.stdout
        print(formatted_message, file=output, flush=True)
        self.log_handle.write(formatted_message + '\n')
        self.log_handle.flush()

    def parse_line(self, line: str, custom_parsers: Optional[List[Callable[[str], Optional[str]]]] = None) -> Optional[str]:
        """
        Parse a line of output and extract relevant information
        
        Args:
            line: Line of output to parse
            custom_parsers: Optional list of custom parser functions to run before default parsing
        """
        # Run custom parsers first if provided
        if custom_parsers:
            for parser in custom_parsers:
                result = parser(line)
                if result:
                    return result

        # Match file progress: [ 42/110] path/to/file.qmd
        file_match = re.match(r'\[\s*(\d+)/(\d+)\]\s+(.+\.qmd)', line)
        if file_match:
            self.file_count = int(file_match.group(1))
            self.total_files = int(file_match.group(2))
            self.current_file = file_match.group(3)
            return f"[{self.file_count}/{self.total_files}] {self.current_file}"

        # Match output creation
        if line.startswith('Output created:'):
            return line.strip()

        # Detect warnings (WARN: can appear anywhere in line, often with timestamps)
        if 'WARN:' in line or 'Warning:' in line:
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

    def run_build(self, command: List[str], build_type: str = "render", custom_parsers: Optional[List[Callable[[str], Optional[str]]]] = None) -> int:
        """
        Run the build command with monitoring

        Args:
            command: Command to execute as list (e.g., ['quarto', 'render', '.', '--to', 'pdf'])
            build_type: Type of build for logging (e.g., 'PDF render', 'HTML render')
            custom_parsers: Optional list of custom parser functions for build-specific output

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        self.log(f"Starting {build_type}: {' '.join(command)}")
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
                encoding='utf-8',
                errors='replace',  # Replace invalid UTF-8 bytes instead of failing
                bufsize=1
            )

            # Start timeout watchdog thread
            self.timeout_thread = threading.Thread(target=self.timeout_watchdog, daemon=True)
            self.timeout_thread.start()

            for line in self.process.stdout:
                # Update last output time (ANY output resets the timeout)
                self.last_output_time = time.time()

                # Get timestamp for this line
                timestamp = self.get_timestamp()
                
                # Write timestamped line to log file
                timestamped_line = f"[{timestamp}] {line}"
                self.log_handle.write(timestamped_line)
                self.log_handle.flush()

                # Print timestamped output to console as well
                print(timestamped_line, end='')

                # Parse and extract relevant information for summary
                parsed = self.parse_line(line, custom_parsers)
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


def kill_existing_quarto_processes(include_latex: bool = False) -> int:
    """
    Kill all existing Quarto and optionally LaTeX processes before starting a new build
    
    Args:
        include_latex: Whether to also kill LaTeX processes (for PDF builds)
    
    Returns:
        Number of processes killed
    """
    killed_count = 0
    
    try:
        system = platform.system()
        
        if system == 'Windows':
            # Windows: Use taskkill to kill quarto.exe and optionally LaTeX processes
            processes_to_kill = ['quarto.exe']
            if include_latex:
                processes_to_kill.extend(['lualatex.exe', 'pdflatex.exe', 'xelatex.exe'])
            
            for proc_name in processes_to_kill:
                try:
                    result = subprocess.run(
                        ['taskkill', '/F', '/IM', proc_name, '/T'],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
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
            processes_to_kill = ['quarto']
            if include_latex:
                processes_to_kill.extend(['lualatex', 'pdflatex', 'xelatex'])
            
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


def get_timestamp() -> str:
    """Get formatted timestamp for log messages"""
    return datetime.now().strftime('%H:%M:%S')

def log_with_timestamp(message: str, to_stderr: bool = False):
    """Log message with timestamp"""
    timestamp = get_timestamp()
    formatted_message = f"[{timestamp}] {message}"
    output = sys.stderr if to_stderr else sys.stdout
    print(formatted_message, file=output, flush=True)

def run_pre_validation() -> int:
    """
    Run pre-validation script before building

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    log_with_timestamp("=" * 80)
    log_with_timestamp("RUNNING PRE-VALIDATION")
    log_with_timestamp("=" * 80)

    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pre-render-validation.py')

    try:
        # Capture output so we can timestamp it
        result = subprocess.run(
            [sys.executable, script_path],
            check=False,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Log captured output with timestamps
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    log_with_timestamp(line)
        
        if result.stderr:
            for line in result.stderr.strip().split('\n'):
                if line.strip():
                    log_with_timestamp(line, to_stderr=True)

        if result.returncode != 0:
            log_with_timestamp(f"\nPre-validation failed with exit code {result.returncode}", to_stderr=True)
            return result.returncode

        log_with_timestamp("\nPre-validation passed!")
        log_with_timestamp("=" * 80)
        return 0
    except Exception as e:
        log_with_timestamp(f"\nError running pre-validation: {e}", to_stderr=True)
        return 1


def run_post_validation(output_dir: str = '_book/warondisease') -> int:
    """
    Run post-validation script after building HTML

    Args:
        output_dir: Directory containing rendered HTML files

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    log_with_timestamp("=" * 80)
    log_with_timestamp("RUNNING POST-VALIDATION")
    log_with_timestamp("=" * 80)

    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'post-render-validation.py')

    try:
        # Capture output so we can timestamp it
        result = subprocess.run(
            [sys.executable, script_path, '--output-dir', output_dir],
            check=False,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Log captured output with timestamps
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    log_with_timestamp(line)
        
        if result.stderr:
            for line in result.stderr.strip().split('\n'):
                if line.strip():
                    log_with_timestamp(line, to_stderr=True)

        if result.returncode != 0:
            log_with_timestamp(f"\nPost-validation failed with exit code {result.returncode}", to_stderr=True)
            return result.returncode

        log_with_timestamp("\nPost-validation passed!")
        log_with_timestamp("=" * 80)
        return 0
    except Exception as e:
        log_with_timestamp(f"\nError running post-validation: {e}", to_stderr=True)
        return 1


def create_latex_parser():
    """Create a parser function for LaTeX compilation phases"""
    def parse_latex(line: str) -> Optional[str]:
        if re.match(r'running lualatex - \d+', line):
            return f"LaTeX compilation: {line.strip()}"
        return None
    return parse_latex

