#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared Build Logger
====================

Provides consistent logging across all build scripts with:
- Timestamped output to both console and log file
- Automatic log file rotation (creates new file each build)
- Section headers and status indicators
- Thread-safe logging
- TeeWriter for capturing ALL stdout/stderr to log file

Usage:
    from build_logger import BuildLogger

    # Option 1: Use logger directly
    logger = BuildLogger("build-economics.log")
    logger.section("BUILDING ECONOMICS")
    logger.info("Starting build...")
    logger.ok("Build complete!")
    logger.close()

    # Option 2: Capture ALL output (including subprocess)
    with BuildLogger("build-economics.log") as logger:
        logger.start_capture()  # Redirects stdout/stderr
        print("This goes to both console AND log file")
        subprocess.run(["quarto", "render"])  # Output captured too
        logger.stop_capture()  # Restores original stdout/stderr
"""

import sys
import threading
import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, TextIO, Callable, Iterable, Sequence, cast

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    stdout_reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(stdout_reconfigure):
        stdout_reconfigure(encoding='utf-8')


class TeeWriter:
    """Writes to both original stream and log file.

    Does NOT inherit from TextIOWrapper to avoid segfaults when code calls
    sys.stdout.reconfigure() on the replaced stream (the C-level buffer
    would be uninitialized).
    """

    def __init__(self, original: TextIO, log_file: TextIO):
        self.original = original
        self.log_file = log_file
        self._lock = threading.Lock()

    def write(self, text: str) -> int:
        with self._lock:
            # Write to original stream (console)
            self.original.write(text)
            self.original.flush()
            # Write to log file
            if self.log_file and not self.log_file.closed:
                self.log_file.write(text)
                self.log_file.flush()
        return len(text)

    def flush(self) -> None:
        with self._lock:
            self.original.flush()
            if self.log_file and not self.log_file.closed:
                self.log_file.flush()

    def fileno(self) -> int:
        return self.original.fileno()

    @property
    def encoding(self) -> str:
        return self.original.encoding

    def isatty(self) -> bool:
        return self.original.isatty()

    def reconfigure(self, **kwargs) -> None:
        """Delegate reconfigure to the original stream."""
        reconfigure_fn = getattr(self.original, 'reconfigure', None)
        if callable(reconfigure_fn):
            reconfigure_fn(**kwargs)


class BuildLogger:
    """Thread-safe logger that writes to both console and log file."""

    def __init__(self, log_file: Optional[str] = None, logs_dir: Optional[Path] = None):
        """
        Initialize logger.

        Args:
            log_file: Log file name (e.g., "build-economics.log")
            logs_dir: Directory for logs (default: project_root/logs/)
        """
        self._lock = threading.Lock()
        self.start_time = datetime.now()
        self.log_handle = None
        self.log_path = None

        if log_file:
            # Determine logs directory
            if logs_dir is None:
                # Default to project_root/logs/
                project_root = Path(__file__).parent.parent.parent
                logs_dir = project_root / "logs"

            logs_dir.mkdir(exist_ok=True)
            self.log_path = logs_dir / log_file

            # Open log file (overwrites previous)
            self.log_handle = open(self.log_path, "w", encoding="utf-8", newline='\n')
            self._write_header()

    def _write_header(self) -> None:
        """Write log file header."""
        if self.log_handle:
            self.log_handle.write(f"Build Log - {self.start_time.isoformat()}\n")
            self.log_handle.write("=" * 80 + "\n\n")
            self.log_handle.flush()

    def _timestamp(self) -> str:
        """Get formatted timestamp."""
        return datetime.now().strftime("[%H:%M:%S]")

    def _write(self, message: str, to_stderr: bool = False) -> None:
        """Write message to console and log file."""
        with self._lock:
            # Write to console
            output = sys.stderr if to_stderr else sys.stdout
            print(message, file=output, flush=True)

            # Write to log file
            if self.log_handle and not self.log_handle.closed:
                # Add timestamp to log file only
                timestamped = f"{self._timestamp()} {message}"
                self.log_handle.write(timestamped + "\n")
                self.log_handle.flush()

    def section(self, title: str) -> None:
        """Print a section header."""
        header = "=" * 80 + f"\n{title}\n" + "=" * 80
        self._write(header)

    def info(self, message: str) -> None:
        """Print info message with [*] prefix."""
        self._write(f"[*] {message}")

    def ok(self, message: str) -> None:
        """Print success message with [OK] prefix."""
        self._write(f"[OK] {message}")

    def warning(self, message: str) -> None:
        """Print warning message with [WARNING] prefix."""
        self._write(f"[WARNING] {message}", to_stderr=True)

    def error(self, message: str) -> None:
        """Print error message with [ERROR] prefix."""
        self._write(f"[ERROR] {message}", to_stderr=True)

    def print(self, message: str) -> None:
        """Print plain message (no prefix)."""
        self._write(message)

    def blank(self) -> None:
        """Print blank line."""
        self._write("")

    def start_capture(self) -> None:
        """
        Start capturing ALL stdout/stderr to the log file.

        After calling this, any print() or subprocess output will go
        to both console AND log file automatically.
        """
        if not self.log_handle or self.log_handle.closed:
            return

        # Save original streams
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        # Replace with TeeWriters
        sys.stdout = TeeWriter(self._original_stdout, self.log_handle)
        sys.stderr = TeeWriter(self._original_stderr, self.log_handle)

    def stop_capture(self) -> None:
        """
        Stop capturing stdout/stderr and restore original streams.
        """
        if hasattr(self, '_original_stdout'):
            sys.stdout = self._original_stdout
        if hasattr(self, '_original_stderr'):
            sys.stderr = self._original_stderr

    def close(self, exit_code: int = 0) -> None:
        """Close logger and write summary."""
        if self.log_handle and not self.log_handle.closed:
            duration = datetime.now() - self.start_time
            self.log_handle.write("\n" + "=" * 80 + "\n")
            self.log_handle.write(f"Build finished: {datetime.now().isoformat()}\n")
            self.log_handle.write(f"Duration: {duration}\n")
            self.log_handle.write(f"Exit code: {exit_code}\n")
            self.log_handle.close()
            print(f"[*] Log saved to: {self.log_path}")

    def __enter__(self) -> "BuildLogger":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        exit_code = 1 if exc_type else 0
        self.close(exit_code)


class SingleLineProgress:
    """Single-line progress printer with optional fallback to regular line output."""

    def __init__(self, enabled: bool = True, stream: Optional[TextIO] = None):
        self.enabled = enabled
        self.stream = stream or sys.stdout
        # When stdout is a TeeWriter, render in-place updates on the underlying
        # terminal stream and keep logs concise.
        self.render_stream = cast(TextIO, getattr(self.stream, "original", self.stream))
        self.capture_stream = self.stream if self.render_stream is not self.stream else None
        self._active = False
        self._width = 0
        self._lock = threading.Lock()
        isatty_fn = getattr(self.render_stream, "isatty", None)
        self._supports_inline = bool(callable(isatty_fn) and isatty_fn())

    def update(self, message: str, final: bool = False) -> None:
        """Update the progress line."""
        with self._lock:
            if not self.enabled:
                print(message, file=self.stream, flush=True)
                return

            if not self._supports_inline:
                # Non-interactive output: keep logs concise by emitting only the final snapshot.
                if final:
                    print(message, file=self.stream, flush=True)
                return

            self._width = max(self._width, len(message))
            padded = message.ljust(self._width)
            self.render_stream.write("\r" + padded)
            self.render_stream.flush()
            self._active = True

            if final:
                self.render_stream.write("\n")
                self.render_stream.flush()
                if self.capture_stream:
                    self.capture_stream.write(message + "\n")
                    self.capture_stream.flush()
                self._active = False

    def clear(self) -> None:
        """Terminate an active progress line so subsequent logs start cleanly."""
        with self._lock:
            if self._active:
                self.render_stream.write("\n")
                self.render_stream.flush()
                self._active = False


def suppress_pip_requirement_noise(line: str) -> bool:
    """Filter noisy pip dependency output lines."""
    stripped = line.strip()
    if not stripped:
        return False
    noisy_prefixes = (
        "Requirement already satisfied",
        "Collecting ",
        "Using cached ",
        "Downloading ",
        "Installing collected packages",
        "Successfully installed ",
    )
    return stripped.startswith(noisy_prefixes)


def any_suppress_filter(line: str, filters: Iterable[Callable[[str], bool]]) -> bool:
    """Return True if any suppress filter matches the line."""
    for filter_fn in filters:
        try:
            if filter_fn(line):
                return True
        except Exception:
            # Never let a filter crash command logging.
            continue
    return False


def run_command_stream(
    cmd: list[str],
    cwd: Path,
    log_file: TextIO,
    suppress_filters: Optional[Sequence[Callable[[str], bool]]] = None,
    extra_sinks: Optional[Sequence[TextIO]] = None,
) -> tuple[int, str]:
    """
    Run command, stream output to console and log, and optionally extra sinks.

    Returns:
        (return_code, captured_output)
    """
    suppress_filters = suppress_filters or ()
    extra_sinks = extra_sinks or ()

    process = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    output_lines: list[str] = []
    for line in (process.stdout or []):
        if suppress_filters and any_suppress_filter(line, suppress_filters):
            continue
        print(line, end="", flush=True)
        log_file.write(line)
        output_lines.append(line)
        for sink in extra_sinks:
            sink.write(line)
        log_file.flush()
        os.fsync(log_file.fileno())
        for sink in extra_sinks:
            sink.flush()

    log_file.flush()
    os.fsync(log_file.fileno())
    for sink in extra_sinks:
        sink.flush()
    process.wait()
    return int(process.returncode), "".join(output_lines)


def run_logged_command_stream(
    cmd: list[str],
    cwd: Path,
    log_path: Path,
    *,
    log_mode: str = "w",
    suppress_filters: Optional[Sequence[Callable[[str], bool]]] = None,
    extra_sinks: Optional[Sequence[TextIO]] = None,
    print_banner: bool = True,
) -> tuple[int, str]:
    """
    Run command with streamed console output and persistent file logging.

    This wraps `run_command_stream` and centralizes common boilerplate used
    by workflow scripts that need [RUN]/[LOG] banners plus full output logs.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command_text = " ".join(cmd)
    if print_banner:
        print(f"[RUN] {command_text}", flush=True)
        print(f"[LOG] {log_path}", flush=True)
    with open(log_path, log_mode, encoding="utf-8") as log_file_raw:
        log_file = cast(TextIO, log_file_raw)
        if print_banner:
            log_file.write(f"\n[RUN] {command_text}\n")
            log_file.flush()
        return run_command_stream(
            cmd=cmd,
            cwd=cwd,
            log_file=log_file,
            suppress_filters=suppress_filters,
            extra_sinks=extra_sinks,
        )


# Singleton instance for simple usage
_default_logger: Optional[BuildLogger] = None


def get_logger(log_file: Optional[str] = None, logs_dir: Optional[Path] = None) -> BuildLogger:
    """
    Get or create the default logger instance.

    Args:
        log_file: Log file name (only used when creating new logger)
        logs_dir: Directory for logs (only used when creating new logger)

    Returns:
        BuildLogger instance
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = BuildLogger(log_file, logs_dir)
    return _default_logger


def reset_logger() -> None:
    """Reset the default logger (for testing or new builds)."""
    global _default_logger
    if _default_logger:
        _default_logger.close()
    _default_logger = None
