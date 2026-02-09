#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared utilities for Quarto render scripts
"""

import importlib
import io
import json
import os
import platform
import re
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional, Tuple

try:
    from .pdf_validation_runner import run_pdf_validation as run_pdf_validation_subprocess
    from .python_utils import get_preferred_python, load_project_dotenv
except ImportError:
    from pdf_validation_runner import run_pdf_validation as run_pdf_validation_subprocess
    from python_utils import get_preferred_python, load_project_dotenv

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    stdout_reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(stdout_reconfigure):
        stdout_reconfigure(encoding="utf-8")

# Try to import psutil for LaTeX process detection (optional)
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Detect if running in GitHub Actions
IN_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"


def extract_latex_errors(log_dir: str, max_context_lines: int = 20) -> List[str]:
    """
    Extract relevant error information from LaTeX log files.

    Searches for .log files and extracts error context including:
    - LaTeX errors (! Error...)
    - Runaway arguments
    - File ended while scanning
    - Missing files
    - Package errors

    Args:
        log_dir: Directory containing LaTeX log files
        max_context_lines: Maximum lines of context around each error

    Returns:
        List of formatted error messages with context, sorted by severity
    """
    from pathlib import Path

    critical_errors = []  # Fatal errors that stop compilation
    other_errors = []     # Warnings and non-fatal issues
    log_path = Path(log_dir)

    if not log_path.exists():
        return []

    # Find all .log files
    log_files = list(log_path.glob("**/*.log"))

    # Error patterns to look for (priority order - critical first)
    # Tuple: (pattern, error_type, is_critical)
    error_patterns = [
        # Critical errors (stop compilation)
        (r"^! .*", "LaTeX Error", True),
        (r"Runaway argument\?", "Runaway Argument", True),
        (r"File ended while scanning", "Incomplete Input", True),
        (r"Emergency stop", "Emergency Stop", True),
        (r"@writefile", "Aux File Corruption", True),
        (r"! I can't find file", "Missing File", True),
        (r"Undefined control sequence", "Undefined Command", True),
        # Non-critical (warnings)
        (r"Missing \$ inserted", "Math Mode Error", False),
        (r"Package .* Error:", "Package Error", False),
        (r"LaTeX Error:", "LaTeX Error", False),
    ]

    # Patterns to skip (benign messages)
    skip_patterns = [
        r"No file .*\.aux",  # Normal on first run
        r"No file .*\.toc",  # Normal on first run
        r"No file .*\.lof",  # Normal on first run
        r"No file .*\.lot",  # Normal on first run
        r"Rerun to get",     # Normal LaTeX message
    ]

    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            found_patterns = set()  # Track which patterns we've found

            for i, line in enumerate(lines):
                # Skip benign patterns
                if any(re.search(skip, line) for skip in skip_patterns):
                    continue

                for pattern, error_type, is_critical in error_patterns:
                    # Only capture first occurrence of each error type
                    if pattern in found_patterns:
                        continue

                    if re.search(pattern, line):
                        found_patterns.add(pattern)

                        # Extract context around the error
                        start = max(0, i - 5)
                        end = min(len(lines), i + max_context_lines)
                        context_lines = lines[start:end]

                        # Format the error
                        severity = "CRITICAL" if is_critical else "WARNING"
                        error_msg = f"\n{'='*60}\n"
                        error_msg += f"[{severity}] {error_type} in {log_file.name} (line {i+1})\n"
                        error_msg += f"{'='*60}\n"
                        for j, ctx_line in enumerate(context_lines):
                            line_num = start + j + 1
                            marker = ">>> " if line_num == i + 1 else "    "
                            error_msg += f"{marker}{line_num:6d}: {ctx_line.rstrip()}\n"

                        if is_critical:
                            critical_errors.append(error_msg)
                        else:
                            other_errors.append(error_msg)

                        break  # Found a match, check next line

        except Exception as e:
            other_errors.append(f"Error reading {log_file}: {e}")

    # Return critical errors first
    return critical_errors + other_errors


def extract_aux_file_contents(log_dir: str, max_lines: int = 30) -> List[str]:
    """
    Extract and return contents of auxiliary files for debugging.

    When LaTeX has an @writefile error, the aux file may contain problematic
    content (very long lines, special characters, etc.). This function
    finds aux/toc/out files and extracts their tail for debugging.

    Args:
        log_dir: Directory containing LaTeX build output
        max_lines: Maximum lines to extract from each file's tail

    Returns:
        List of formatted strings with aux file contents
    """
    from pathlib import Path

    aux_contents = []
    log_path = Path(log_dir)

    if not log_path.exists():
        return []

    # Find auxiliary files - aux, toc, out, lof, lot (all can be corrupted)
    aux_extensions = ["*.aux", "*.toc", "*.out", "*.lof", "*.lot"]
    aux_files = []
    for ext in aux_extensions:
        aux_files.extend(log_path.glob(ext))  # Top-level only (index.aux, etc.)

    # Sort by size descending (main files are usually largest)
    aux_files = sorted(aux_files, key=lambda f: f.stat().st_size, reverse=True)

    for aux_file in aux_files[:3]:  # Show top 3 largest aux files
        try:
            file_size = aux_file.stat().st_size

            with open(aux_file, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            # Always show the file when debugging @writefile errors
            aux_msg = f"\n{'='*60}\n"
            aux_msg += f"FILE: {aux_file.name}\n"
            aux_msg += f"Size: {file_size:,} bytes, {len(lines):,} lines\n"

            # Check for obvious corruption signs
            corruption_hints = []
            if lines:
                content = ''.join(lines)
                open_braces = content.count('{')
                close_braces = content.count('}')
                if open_braces != close_braces:
                    corruption_hints.append(f"Unbalanced braces: {open_braces} open vs {close_braces} close")
                if not lines[-1].endswith('\n'):
                    corruption_hints.append("File ends without newline")
                if content.rstrip().endswith(('\\', '{', ',')):
                    corruption_hints.append("Ends with incomplete command")

            if corruption_hints:
                aux_msg += f"Corruption hints: {', '.join(corruption_hints)}\n"

            aux_msg += f"{'='*60}\n"
            aux_msg += f"LAST {max_lines} LINES:\n"

            # Show last N lines
            display_lines = lines[-max_lines:] if len(lines) > max_lines else lines
            start_line = len(lines) - len(display_lines) + 1

            for j, line in enumerate(display_lines):
                line_num = start_line + j
                # Highlight the last few lines where corruption likely is
                marker = ">>> " if j >= len(display_lines) - 5 else "    "
                # Truncate very long lines
                line_content = line.rstrip()[:200]
                if len(line.rstrip()) > 200:
                    line_content += "..."
                aux_msg += f"{marker}{line_num:6d}: {line_content}\n"

            aux_contents.append(aux_msg)

        except Exception as e:
            aux_contents.append(f"Error reading {aux_file}: {e}")

    return aux_contents


def print_latex_errors(log_dir: str, max_errors: int = 5) -> None:
    """
    Print LaTeX errors to console and emit GitHub Actions annotations.

    Also extracts and displays aux file contents when @writefile errors
    are detected (indicates corrupted aux file from previous build).

    Args:
        log_dir: Directory containing LaTeX log files
        max_errors: Maximum number of errors to display
    """
    errors = extract_latex_errors(log_dir)

    if not errors:
        print("[*] No LaTeX errors found in log files")
        return

    print(f"\n{'#'*80}")
    print("# LATEX ERROR DETAILS (extracted from .log files)")
    print(f"{'#'*80}\n")

    # Check if any errors mention aux files or @writefile
    has_aux_error = any('@writefile' in err.lower() or 'aux' in err.lower() for err in errors)

    for i, error in enumerate(errors[:max_errors]):
        print(error)
        if IN_GITHUB_ACTIONS:
            # Emit GitHub Actions error annotation
            # Extract first line for annotation
            first_line = error.split('\n')[2] if '\n' in error else error[:200]
            print(f"::error::LaTeX Error: {first_line.strip()}")

    if len(errors) > max_errors:
        print(f"\n... and {len(errors) - max_errors} more errors (see full log)")

    # If there's an aux file error, extract and display aux file contents
    if has_aux_error:
        print(f"\n{'#'*80}")
        print("# AUX FILE ANALYSIS")
        print(f"{'#'*80}")
        print("\nNOTE: @writefile errors occur when LaTeX encounters unexpected content")
        print("while writing/reading aux files. Common causes:")
        print("  - Very long figure captions or titles that break aux file format")
        print("  - Special characters that aren't properly escaped")
        print("  - Memory issues during large document compilation")
        print(f"\nSearching for aux files in: {log_dir}\n")

        aux_contents = extract_aux_file_contents(log_dir)
        if aux_contents:
            for aux_content in aux_contents:
                print(aux_content)
        else:
            # List what files exist in the directory for debugging
            from pathlib import Path
            log_path = Path(log_dir)
            if log_path.exists():
                all_files = list(log_path.glob("*"))
                print(f"[*] No aux/toc/out files found in {log_dir}")
                print(f"    Files present: {[f.name for f in all_files[:20]]}")
                if len(all_files) > 20:
                    print(f"    ... and {len(all_files) - 20} more files")
            else:
                print(f"[*] Directory does not exist: {log_dir}")

    print(f"\n{'#'*80}\n")


def setup_quarto_python_env():
    """
    Configure Quarto to use virtual environment Python (cross-platform)

    Sets QUARTO_PYTHON environment variable to point to the project's venv,
    preventing Quarto from using the wrong system Python installation.

    This solves PATH ordering issues when multiple Python installations exist.
    """
    from pathlib import Path

    # Detect project root (render_utils.py is in scripts/lib/)
    project_root = Path(__file__).parent.parent.parent.absolute()

    preferred_python = get_preferred_python(project_root)
    os.environ['QUARTO_PYTHON'] = preferred_python
    print(f"[*] Using Quarto Python: {preferred_python}")


# Auto-configure Quarto Python when this module is imported
setup_quarto_python_env()


def ensure_jupyter_kernel(kernel_name: str = "dih-project-kernel", display_name: str = "DIH Project") -> bool:
    """
    Ensure the Jupyter kernel exists, creating it if necessary.

    This function checks if the specified Jupyter kernel is installed,
    and if not, installs ipykernel in the venv and creates the kernel spec.

    Args:
        kernel_name: Name of the kernel (e.g., 'dih-project-kernel')
        display_name: Display name for the kernel

    Returns:
        bool: True if kernel exists or was created successfully, False on error
    """
    from pathlib import Path

    # Check if kernel already exists
    try:
        result = subprocess.run(
            ["jupyter", "kernelspec", "list", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        kernels = json.loads(result.stdout)
        if kernel_name in kernels.get("kernelspecs", {}):
            print(f"[OK] Jupyter kernel '{kernel_name}' found")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        pass  # Fall through to kernel creation

    print(f"[*] Jupyter kernel '{kernel_name}' not found, creating it...")

    # Find venv Python
    project_root = Path(__file__).parent.parent.parent.absolute()
    if sys.platform == 'win32':
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = project_root / ".venv" / "bin" / "python"

    if not venv_python.exists():
        print(f"[ERROR] Virtual environment Python not found: {venv_python}", file=sys.stderr)
        print("        Run 'python -m venv .venv' to create virtual environment", file=sys.stderr)
        return False

    # Ensure ipykernel is installed in venv
    print(f"[*] Ensuring ipykernel is installed in virtual environment...")
    try:
        # Show output so user can see download progress; timeout after 5 minutes
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "--progress-bar", "on", "ipykernel"],
            check=True,
            timeout=300  # 5 minute timeout
        )
    except subprocess.TimeoutExpired:
        print(f"[ERROR] pip install timed out after 5 minutes", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install ipykernel: {e}", file=sys.stderr)
        return False

    # Create kernel spec
    try:
        subprocess.run(
            [
                str(venv_python), "-m", "ipykernel", "install",
                "--user",
                "--name", kernel_name,
                "--display-name", display_name
            ],
            check=True,
            capture_output=True,
            timeout=60  # 1 minute timeout
        )
        print(f"[OK] Created Jupyter kernel '{kernel_name}'")
        return True
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Kernel creation timed out", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create kernel: {e}", file=sys.stderr)
        return False


def setup_jupyter_kernel(kernel_name: str = "dih-project-kernel", display_name: str = "DIH Project"):
    """
    Set up Jupyter kernel with user-friendly error handling.

    This is a convenience wrapper around ensure_jupyter_kernel() that:
    - Attempts to create the kernel if missing
    - Prints helpful warning messages if setup fails
    - Continues execution (soft failure) rather than exiting

    Use this in preview/render scripts for consistent error handling.

    Args:
        kernel_name: Name of the kernel (e.g., 'dih-project-kernel')
        display_name: Display name for the kernel
    """
    if not ensure_jupyter_kernel(kernel_name, display_name):
        print("\n[WARNING] Failed to set up Jupyter kernel (see errors above)", file=sys.stderr)
        print("          Preview will continue, but may fail if Python code cells are executed", file=sys.stderr)
        print("          To fix: Ensure .venv exists and run 'pip install ipykernel'\n", file=sys.stderr)


class BuildMonitor:
    def __init__(
        self,
        timeout_seconds: int = 180,
        fail_on_warnings: bool = True,
        log_file: str = "build.log",
        max_warnings_display: int = 0,  # 0 = show all
        max_errors_display: int = 0,  # 0 = show all
    ):
        """
        Initialize the build monitor

        Args:
            timeout_seconds: Max seconds with no output before killing build (default 180)
            fail_on_warnings: Whether to fail build on warnings (default True)
            log_file: Path to log file (default "build.log")
            max_warnings_display: Max warnings to show in summary (0 = all, default 0)
            max_errors_display: Max errors to show in summary (0 = all, default 0)
        """
        self.timeout_seconds = timeout_seconds
        self.fail_on_warnings = fail_on_warnings
        self.log_file = log_file
        self.max_warnings_display = max_warnings_display
        self.max_errors_display = max_errors_display
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

        # Profiling data
        self.build_start_time = time.time()
        self.current_file_start_time = None
        self.file_timings = []  # List of (file_name, duration_seconds)
        self.phase_timings = {}  # Dict of phase_name -> (start_time, end_time)

        # Open log file (append mode to preserve earlier output from render script)
        self.log_handle = open(self.log_file, "a", encoding="utf-8", newline='\n')

    def __del__(self):
        """Close log file on cleanup"""
        try:
            if hasattr(self, "log_handle") and self.log_handle:
                self.log_handle.close()
        except Exception:
            pass  # Ignore cleanup errors

    def get_timestamp(self) -> str:
        """Get formatted timestamp for log messages"""
        return datetime.now().strftime("%H:%M:%S")

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human-readable string"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.0f}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"

    def log(self, message: str, to_stderr: bool = False):
        """Log message to both console and file with timestamp"""
        timestamp = self.get_timestamp()
        formatted_message = f"[{timestamp}] {message}"
        output = sys.stderr if to_stderr else sys.stdout
        print(formatted_message, file=output, flush=True)
        self.log_handle.write(formatted_message + "\n")
        self.log_handle.flush()

    def is_noisy_line(self, line: str) -> bool:
        """
        Check if a line is noise that should be suppressed from console output.

        These lines are still logged to the log file but not shown to the user.
        """
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            return True

        # Skip Jupyter kernel startup messages (various formats)
        # "Starting dih-project-kernel kernel...Done"
        # "Starting python3 kernel...Done"
        if "Starting" in stripped and "kernel" in stripped:
            return True

        # Skip plain "Done" or "Done." lines (often from kernel startup)
        if stripped in ["Done", "Done."]:
            return True

        # Skip Quarto progress dots and other minimal output
        if stripped in [".", "..", "..."]:
            return True

        # Skip ipynb conversion messages (not useful to user)
        if ".quarto_ipynb" in stripped and "Rendering" not in stripped:
            return True

        return False

    def parse_line(
        self, line: str, custom_parsers: Optional[List[Callable[[str], Optional[str]]]] = None
    ) -> Optional[str]:
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
        file_match = re.match(r"\[\s*(\d+)/(\d+)\]\s+(.+\.qmd)", line)
        if file_match:
            # Track timing for previous file
            current_time = time.time()
            if self.current_file and self.current_file_start_time:
                duration = current_time - self.current_file_start_time
                self.file_timings.append((self.current_file, duration))

            # Start timing new file
            self.file_count = int(file_match.group(1))
            self.total_files = int(file_match.group(2))
            self.current_file = file_match.group(3)
            self.current_file_start_time = current_time

            # Calculate elapsed time since build start
            elapsed = current_time - self.build_start_time
            elapsed_str = self._format_duration(elapsed)

            return f"[{self.file_count}/{self.total_files}] {self.current_file} (elapsed: {elapsed_str})"

        # Match output creation
        if line.startswith("Output created:"):
            return line.strip()

        # Detect warnings (WARN: can appear anywhere in line, often with timestamps)
        if any(marker in line for marker in ["WARN:", "Warning:", "[WARNING]"]):
            # Ignore warnings about thinkbynumbers (Twitter handle in YAML, not a citation)
            if all(ignore_word not in line for ignore_word in ["thinkbynumbers", "warondisease"]):
                # Treat certain critical warnings as errors (content rendering failures)
                critical_warning_patterns = [
                    "Could not convert TeX math",  # LaTeX math failed to render
                    "Duplicate identifier",  # Anchor link collision
                ]
                is_critical = any(pattern in line for pattern in critical_warning_patterns)

                if is_critical:
                    self.errors.append(f"[CRITICAL WARNING] {line.strip()}")
                    return f"ERROR (critical warning): {line.strip()}"
                else:
                    self.warnings.append(line.strip())
                    return f"WARNING: {line.strip()}"
            return None  # Silently ignore thinkbynumbers and warondisease warnings

        # Detect errors
        if line.startswith("ERROR:") or line.startswith("Error:") or "error:" in line.lower():
            self.errors.append(line.strip())
            return f"ERROR: {line.strip()}"

        return None

    def check_timeout(self) -> bool:
        """Check if build has timed out (no output for timeout_seconds)

        Exception: If LaTeX processes are actively running, extend timeout
        since LaTeX compilation can be silent for long periods.
        """
        elapsed = time.time() - self.last_output_time

        # If LaTeX processes are running, allow longer timeout (LaTeX can be silent)
        if self._is_latex_running():
            # Allow up to 2x timeout when LaTeX is running
            if elapsed > (self.timeout_seconds * 2):
                return True
            return False

        # Normal timeout check
        if elapsed > self.timeout_seconds:
            return True
        return False

    def _is_latex_running(self) -> bool:
        """Check if any LaTeX processes are currently running"""
        if not PSUTIL_AVAILABLE:
            return False  # Can't detect without psutil

        try:
            latex_processes = ["lualatex", "pdflatex", "xelatex"]
            for proc in psutil.process_iter(["name"]):
                try:
                    proc_name = proc.info["name"] or ""
                    proc_name_lower = proc_name.lower()
                    # Check for LaTeX processes (handle .exe extension on Windows)
                    for latex_name in latex_processes:
                        if latex_name in proc_name_lower or f"{latex_name}.exe" in proc_name_lower:
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            # If psutil fails, fall back to normal timeout behavior
            pass
        return False

    def timeout_watchdog(self):
        """Background thread that monitors for timeout even when no output is produced"""
        last_log_time = time.time()
        while not self.stop_timeout_check.wait(1.0):  # Check every second
            # Check if process has already finished
            if self.process and self.process.poll() is not None:
                # Process finished, exit watchdog
                break

            elapsed_since_output = time.time() - self.last_output_time
            elapsed_since_log = time.time() - last_log_time

            # Log progress every 30 seconds when silent (helps debug GitHub Actions hangs)
            if elapsed_since_output > 30 and elapsed_since_log > 30:
                latex_status = " (LaTeX running)" if self._is_latex_running() else ""
                self.log(
                    f"Still processing... {int(elapsed_since_output)}s since last output{latex_status}", to_stderr=True
                )
                last_log_time = time.time()

            if self.check_timeout():
                self.timed_out = True
                # Double-check process is still running before killing
                if self.process and self.process.poll() is None:
                    elapsed = int(time.time() - self.last_output_time)
                    latex_status = " (LaTeX was running)" if self._is_latex_running() else ""
                    self.log(f"\nERROR: Build timed out after {elapsed}s with no output{latex_status}", to_stderr=True)
                    if self.current_file:
                        self.log(f"Last file being processed: {self.current_file}", to_stderr=True)
                    try:
                        self.process.kill()
                    except ProcessLookupError:
                        # Process already terminated, ignore
                        pass
                break

    def run_build(
        self,
        command: List[str],
        build_type: str = "render",
        custom_parsers: Optional[List[Callable[[str], Optional[str]]]] = None,
    ) -> int:
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
                encoding="utf-8",
                errors="replace",  # Replace invalid UTF-8 bytes instead of failing
                bufsize=1,
            )

            # Start timeout watchdog thread
            self.timeout_thread = threading.Thread(target=self.timeout_watchdog, daemon=True)
            self.timeout_thread.start()

            stdout_stream = self.process.stdout
            if stdout_stream is not None:
                for line in stdout_stream:
                    # Update last output time (ANY output resets the timeout)
                    self.last_output_time = time.time()

                    # Get timestamp for this line
                    timestamp = self.get_timestamp()

                    # Write timestamped line to log file (always log everything)
                    timestamped_line = f"[{timestamp}] {line}"
                    self.log_handle.write(timestamped_line)
                    self.log_handle.flush()

                    # Print to console only if not noisy (kernel messages, empty lines, etc.)
                    if not self.is_noisy_line(line):
                        print(timestamped_line, end="")

                    # Parse and extract relevant information for summary
                    parsed_result = self.parse_line(line, custom_parsers)

                    # Emit GitHub Actions error annotation for visibility
                    if IN_GITHUB_ACTIONS and parsed_result and parsed_result.startswith("ERROR"):
                        # Extract clean error message
                        error_msg = line.strip().replace('\n', ' ')
                        print(f"::error::{error_msg}", flush=True)

                    # Check if watchdog killed the process
                    if self.timed_out:
                        return 124  # Timeout exit code

            # Wait for process to complete
            try:
                return_code = self.process.wait()
            except Exception as e:
                # If wait() fails, try to get return code from poll()
                return_code = self.process.poll()
                if return_code is None:
                    # Process still running, this is unexpected
                    self.log(f"Warning: Process.wait() failed but process still running: {e}", to_stderr=True)
                    return_code = 1
                else:
                    self.log(f"Warning: Process.wait() failed, using poll() result: {return_code}", to_stderr=True)

            # Stop the timeout watchdog BEFORE any cleanup
            self.stop_timeout_check.set()
            if self.timeout_thread and self.timeout_thread.is_alive():
                try:
                    self.timeout_thread.join(timeout=2.0)
                except Exception:
                    pass  # Ignore thread join errors

            # Explicitly close process handles to avoid cleanup errors
            try:
                if self.process and hasattr(self.process, "stdout") and self.process.stdout:
                    self.process.stdout.close()
                if (
                    self.process
                    and hasattr(self.process, "stderr")
                    and self.process.stderr
                    and self.process.stderr != self.process.stdout
                ):
                    self.process.stderr.close()
            except (AttributeError, ValueError, OSError, AssertionError, TypeError):
                pass  # Ignore all cleanup errors - process may already be closed

            # Check if we timed out
            if self.timed_out:
                return 124

            # If return_code is None, process hasn't finished (shouldn't happen after wait())
            if return_code is None:
                self.log("Warning: Process return code is None after wait()", to_stderr=True)
                return_code = 1

            # Track final file timing if there was one
            if self.current_file and self.current_file_start_time:
                duration = time.time() - self.current_file_start_time
                self.file_timings.append((self.current_file, duration))

            # Calculate total build time
            total_build_time = time.time() - self.build_start_time

            # Print summary
            self.log("\n" + "=" * 80)
            self.log("BUILD SUMMARY")
            self.log("=" * 80)
            self.log(f"Exit code: {return_code}")
            self.log(f"Total build time: {self._format_duration(total_build_time)}")
            self.log(f"Files processed: {len(self.file_timings)}")
            self.log(f"Warnings: {len(self.warnings)}")
            self.log(f"Errors: {len(self.errors)}")

            # Show slowest files
            if self.file_timings:
                self.log("\nSlowest files (top 10):")
                sorted_timings = sorted(self.file_timings, key=lambda x: x[1], reverse=True)
                for file_name, duration in sorted_timings[:10]:
                    self.log(f"  {self._format_duration(duration):>8} - {file_name}")

                # Show average file processing time
                avg_time = sum(d for _, d in self.file_timings) / len(self.file_timings)
                self.log(f"\nAverage file time: {self._format_duration(avg_time)}")

            if self.warnings:
                self.log("\nWarnings detected:")
                display_limit = self.max_warnings_display if self.max_warnings_display > 0 else len(self.warnings)
                for warning in self.warnings[:display_limit]:
                    self.log(f"  - {warning}")
                if len(self.warnings) > display_limit:
                    self.log(f"  ... and {len(self.warnings) - display_limit} more")

            if self.errors:
                # Start a new GitHub Actions group for errors (makes it stand out)
                if IN_GITHUB_ACTIONS:
                    print("::endgroup::", flush=True)  # End any previous group
                    print("::group::❌ ERRORS DETECTED - BUILD FAILED", flush=True)

                # Make errors VERY visible
                self.log("\n" + "!" * 80)
                self.log("!" * 80)
                self.log("!!!  ERRORS DETECTED - BUILD FAILED  !!!")
                self.log("!" * 80)
                self.log("!" * 80)
                display_limit = self.max_errors_display if self.max_errors_display > 0 else len(self.errors)
                for error in self.errors[:display_limit]:
                    self.log(f"  {error}")
                    # Also emit GitHub Actions annotation for each error
                    if IN_GITHUB_ACTIONS:
                        print(f"::error::{error}", flush=True)
                if len(self.errors) > display_limit:
                    self.log(f"  ... and {len(self.errors) - display_limit} more")
                self.log("!" * 80)

                if IN_GITHUB_ACTIONS:
                    print("::endgroup::", flush=True)

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
                try:
                    self.process.kill()
                except (ProcessLookupError, AssertionError):
                    pass  # Process already terminated
            return 130
        except Exception as e:
            # Check if process actually completed successfully before failing
            process_finished = False
            process_exit_code = None
            if self.process:
                try:
                    process_exit_code = self.process.poll()
                    process_finished = process_exit_code is not None
                except Exception:
                    pass

            error_msg = str(e)
            is_cleanup_error = any(
                keyword in error_msg.lower()
                for keyword in ["cleanup", "child process", "already terminated", "assertion"]
            )

            if is_cleanup_error and process_finished:
                # Cleanup error but process finished - log warning but don't fail
                self.log(f"\nWarning: Cleanup error (process completed successfully): {e}", to_stderr=True)
                self.stop_timeout_check.set()
                # Use the process exit code instead of failing
                return process_exit_code if process_exit_code is not None else 0
            else:
                # Real error - fail the build
                self.log(f"\nUnexpected error: {e}", to_stderr=True)
                import traceback

                self.log(f"Traceback: {traceback.format_exc()}", to_stderr=True)
                self.stop_timeout_check.set()
                if self.process and self.process.poll() is None:
                    try:
                        self.process.kill()
                    except (ProcessLookupError, AssertionError, TypeError):
                        pass  # Process already terminated or cleanup error
                return 1
        finally:
            # Ensure cleanup happens gracefully
            self.stop_timeout_check.set()
            if self.timeout_thread:
                try:
                    self.timeout_thread.join(timeout=2.0)
                except Exception:
                    pass  # Ignore cleanup errors


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

        if system == "Windows":
            # Windows: Use taskkill to kill quarto.exe and optionally LaTeX processes
            processes_to_kill = ["quarto.exe"]
            if include_latex:
                processes_to_kill.extend(["lualatex.exe", "pdflatex.exe", "xelatex.exe"])

            for proc_name in processes_to_kill:
                try:
                    result = subprocess.run(
                        ["taskkill", "/F", "/IM", proc_name, "/T"],
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=5,
                    )
                    # Count processes killed (taskkill returns 0 if processes were found and killed)
                    if result.returncode == 0:
                        # Parse output to count killed processes
                        output_lines = result.stdout.split("\n")
                        for line in output_lines:
                            if "terminated" in line.lower() or "killed" in line.lower():
                                killed_count += 1
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
        else:
            # Unix-like: Use pkill or killall
            processes_to_kill = ["quarto"]
            if include_latex:
                processes_to_kill.extend(["lualatex", "pdflatex", "xelatex"])

            for proc_name in processes_to_kill:
                try:
                    # Try pkill first
                    subprocess.run(["pkill", "-9", proc_name], capture_output=True, timeout=5)
                    # Try killall as backup
                    subprocess.run(["killall", "-9", proc_name], capture_output=True, timeout=5)
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
    return datetime.now().strftime("%H:%M:%S")


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
    start_time = time.time()

    log_with_timestamp("=" * 80)
    log_with_timestamp("RUNNING PRE-VALIDATION")
    log_with_timestamp("=" * 80)

    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pre-render-validation.py")

    try:
        # Capture output so we can timestamp it
        result = subprocess.run(
            [sys.executable, script_path],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Log captured output with timestamps
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    log_with_timestamp(line)

        if result.stderr:
            for line in result.stderr.strip().split("\n"):
                if line.strip():
                    log_with_timestamp(line, to_stderr=True)

        elapsed = time.time() - start_time
        elapsed_str = f"{elapsed:.1f}s" if elapsed < 60 else f"{int(elapsed/60)}m {elapsed%60:.0f}s"

        if result.returncode != 0:
            log_with_timestamp(
                f"\nPre-validation failed with exit code {result.returncode} (took {elapsed_str})", to_stderr=True
            )
            return result.returncode

        log_with_timestamp(f"\nPre-validation passed! (took {elapsed_str})")
        log_with_timestamp("=" * 80)
        return 0
    except Exception as e:
        elapsed = time.time() - start_time
        elapsed_str = f"{elapsed:.1f}s" if elapsed < 60 else f"{int(elapsed/60)}m {elapsed%60:.0f}s"
        log_with_timestamp(f"\nError running pre-validation: {e} (took {elapsed_str})", to_stderr=True)
        return 1


def validate_pdf_for_python_code(pdf_path: str, search_string: str = "print(f") -> Tuple[bool, List[str]]:
    """
    Validate PDF for Python code leakage by searching for specific strings.

    Args:
        pdf_path: Path to PDF file to check
        search_string: String to search for (default: 'print(f')

    Returns:
        Tuple of (found_issues: bool, issues: list of context strings)
    """
    issues = []

    if not os.path.exists(pdf_path):
        return False, [f"PDF file not found: {pdf_path}"]

    try:
        # Try to extract text from PDF using PyPDF2
        try:
            import PyPDF2

            with open(pdf_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text_content = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        text_content += f"\n--- Page {page_num} ---\n{page_text}\n"
                    except Exception:
                        # Skip pages that can't be extracted
                        continue
        except ImportError:
            # Fallback: try pdfplumber
            try:
                pdfplumber = importlib.import_module("pdfplumber")

                text_content = ""
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text_content += f"\n--- Page {page_num} ---\n{page_text}\n"
                        except Exception:
                            continue
            except ImportError:
                # Last resort: try pdftotext command if available
                try:
                    result = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        text_content = result.stdout
                    else:
                        return False, ["Could not extract text from PDF. Install PyPDF2, pdfplumber, or pdftotext."]
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    return False, ["Could not extract text from PDF. Install PyPDF2, pdfplumber, or pdftotext."]

        # Search for the string in the extracted text
        lines = text_content.split("\n")
        for line_num, line in enumerate(lines, 1):
            if search_string in line:
                # Extract surrounding context (5 lines before and after)
                start_idx = max(0, line_num - 6)
                end_idx = min(len(lines), line_num + 5)
                context_lines = lines[start_idx:end_idx]

                # Find the exact line with the match
                match_line_idx = line_num - start_idx - 1

                # Build context string
                context = []
                for i, ctx_line in enumerate(context_lines):
                    marker = ">>> " if i == match_line_idx else "    "
                    context.append(f"{marker}Line {start_idx + i + 1}: {ctx_line}")

                issues.append(f"Found '{search_string}' in PDF:\n" + "\n".join(context))

        return len(issues) > 0, issues

    except Exception as e:
        return False, [f"Error validating PDF: {e}"]


def run_post_validation(output_dir: str = "_manual/warondisease") -> int:
    """
    Run post-validation script after building HTML

    Args:
        output_dir: Directory containing rendered HTML files

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    start_time = time.time()

    log_with_timestamp("=" * 80)
    log_with_timestamp("RUNNING POST-VALIDATION")
    log_with_timestamp("=" * 80)

    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "post-render-validation.py")

    try:
        # Capture output so we can timestamp it
        result = subprocess.run(
            [sys.executable, script_path, "--output-dir", output_dir],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Log captured output with timestamps
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    log_with_timestamp(line)

        if result.stderr:
            for line in result.stderr.strip().split("\n"):
                if line.strip():
                    log_with_timestamp(line, to_stderr=True)

        elapsed = time.time() - start_time
        elapsed_str = f"{elapsed:.1f}s" if elapsed < 60 else f"{int(elapsed/60)}m {elapsed%60:.0f}s"

        if result.returncode != 0:
            log_with_timestamp(
                f"\nPost-validation failed with exit code {result.returncode} (took {elapsed_str})", to_stderr=True
            )
            return result.returncode

        log_with_timestamp(f"\nPost-validation passed! (took {elapsed_str})")
        log_with_timestamp("=" * 80)
        return 0
    except Exception as e:
        elapsed = time.time() - start_time
        elapsed_str = f"{elapsed:.1f}s" if elapsed < 60 else f"{int(elapsed/60)}m {elapsed%60:.0f}s"
        log_with_timestamp(f"\nError running post-validation: {e} (took {elapsed_str})", to_stderr=True)
        return 1


def run_pdf_validation(
    pdf_path: str,
    skip_llm: bool = False,
    skip_url_check: bool = True,
    fail_on_warning: bool = False
) -> int:
    """
    Run comprehensive PDF validation using pdf-validation.py.

    Args:
        pdf_path: Path to PDF file to validate
        skip_llm: Force skip LLM validation
        skip_url_check: Skip external URL validation (default True for speed)
        fail_on_warning: Treat warnings as errors

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    start_time = time.time()

    log_with_timestamp("=" * 80)
    log_with_timestamp("RUNNING PDF VALIDATION")
    log_with_timestamp("=" * 80)

    # Ensure .env values are loaded for subprocesses that rely on process env.
    load_project_dotenv(Path(__file__).resolve().parent.parent.parent)

    # Check if LLM validation should be enabled
    gemini_key = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
    if not skip_llm and not gemini_key:
        log_with_timestamp(
            "[ERROR] GOOGLE_GENERATIVE_AI_API_KEY is not set; cannot run required LLM PDF validation",
            to_stderr=True,
        )
        return 1

    try:
        result = run_pdf_validation_subprocess(
            pdf_path=Path(pdf_path),
            cwd=Path(__file__).resolve().parent.parent.parent,
            python_executable=get_preferred_python(Path(__file__).resolve().parent.parent.parent),
            verbose=False,
            skip_url_check=skip_url_check,
            skip_llm=skip_llm,
            fail_on_warning=fail_on_warning,
            use_cache=True,
        )
        log_with_timestamp(f"[*] Command runner: scripts/lib/pdf_validation_runner.py")

        # Log captured output with timestamps
        if result.output:
            for line in result.output.strip().split("\n"):
                if line.strip():
                    log_with_timestamp(line)

        elapsed = time.time() - start_time
        elapsed_str = f"{elapsed:.1f}s" if elapsed < 60 else f"{int(elapsed/60)}m {elapsed%60:.0f}s"

        if result.returncode != 0:
            log_with_timestamp(
                f"\nPDF validation failed with exit code {result.returncode} (took {elapsed_str})",
                to_stderr=True
            )
            return result.returncode

        log_with_timestamp(f"\nPDF validation passed! (took {elapsed_str})")
        log_with_timestamp("=" * 80)
        return 0

    except Exception as e:
        elapsed = time.time() - start_time
        elapsed_str = f"{elapsed:.1f}s" if elapsed < 60 else f"{int(elapsed/60)}m {elapsed%60:.0f}s"
        log_with_timestamp(f"\nError running PDF validation: {e} (took {elapsed_str})", to_stderr=True)
        return 1


def create_latex_parser():
    """Create a parser function for LaTeX compilation phases"""

    def parse_latex(line: str) -> Optional[str]:
        # Match various LaTeX compilation patterns
        if re.search(r"running (lualatex|pdflatex|xelatex)", line, re.IGNORECASE):
            return f"LaTeX compilation: {line.strip()}"
        # Match LaTeX output patterns (even if Quarto doesn't explicitly say "running")
        if re.search(r"(lualatex|pdflatex|xelatex).*\.tex", line, re.IGNORECASE):
            return f"LaTeX processing: {line.strip()}"
        # Match LaTeX log patterns
        if re.search(r"\.(aux|log|out|toc|bbl|blg)", line, re.IGNORECASE):
            return f"LaTeX file: {line.strip()}"
        return None

    return parse_latex
