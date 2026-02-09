#!/usr/bin/env python3
"""Shared runner for scripts/pdf-validation.py."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable
import os
import subprocess
import sys
import time

try:
    from .validation_output_utils import extract_validation_errors, extract_ai_fix_log_path
except ImportError:
    from validation_output_utils import extract_validation_errors, extract_ai_fix_log_path


@dataclass
class PDFValidationRunResult:
    returncode: int
    output: str
    errors: list[str]
    ai_fix_log_path: str | None
    from_cache: bool
    duration_seconds: float


def build_pdf_validation_command(
    pdf_path: Path,
    python_executable: str,
    *,
    skip_url_check: bool = True,
    skip_llm: bool = False,
    fail_on_warning: bool = False,
    use_cache: bool = True,
) -> list[str]:
    """Build pdf-validation.py command with common flags."""
    cmd = [python_executable, "-u", "scripts/pdf-validation.py", "--pdf", str(pdf_path)]
    if skip_llm:
        cmd.append("--skip-llm")
    if skip_url_check:
        cmd.append("--skip-url-check")
    if fail_on_warning:
        cmd.append("--fail-on-warning")
    disable_cache_env = os.environ.get("PDF_VALIDATION_DISABLE_CACHE", "").lower() in {
        "1", "true", "yes", "on"
    }
    if (not use_cache) or disable_cache_env:
        cmd.append("--no-cache")
    return cmd


def run_pdf_validation(
    pdf_path: Path,
    *,
    cwd: Path,
    python_executable: str | None = None,
    verbose: bool = False,
    skip_url_check: bool = True,
    skip_llm: bool = False,
    fail_on_warning: bool = False,
    use_cache: bool = True,
    include_broken_external_errors: bool = True,
    line_filter: Callable[[str], bool] | None = None,
) -> PDFValidationRunResult:
    """
    Execute pdf-validation.py and parse useful outputs.

    If `line_filter` is provided and `verbose` is False, lines are printed only
    when the filter returns True.
    """
    if python_executable is None:
        python_executable = sys.executable

    cmd = build_pdf_validation_command(
        pdf_path=pdf_path,
        python_executable=python_executable,
        skip_url_check=skip_url_check,
        skip_llm=skip_llm,
        fail_on_warning=fail_on_warning,
        use_cache=use_cache,
    )

    started_at = time.time()
    output_lines: list[str] = []
    process = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    for line in (process.stdout or []):
        output_lines.append(line)
        display_line = line.rstrip("\r\n")
        if not display_line:
            continue
        if verbose:
            print(display_line, flush=True)
            continue
        if line_filter is None:
            continue
        if line_filter(display_line):
            print(display_line, flush=True)

    process.wait()
    output = "".join(output_lines)
    duration_seconds = time.time() - started_at

    errors = extract_validation_errors(
        output,
        include_broken_external=include_broken_external_errors,
    )
    ai_fix_log_path = extract_ai_fix_log_path(output)
    from_cache = "Using cached validation results" in output

    return PDFValidationRunResult(
        returncode=process.returncode,
        output=output,
        errors=errors,
        ai_fix_log_path=ai_fix_log_path,
        from_cache=from_cache,
        duration_seconds=duration_seconds,
    )
