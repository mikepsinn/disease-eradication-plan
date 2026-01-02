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
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, TextIO

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


class TeeWriter(TextIOWrapper):
    """Writes to both original stream and log file."""

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
