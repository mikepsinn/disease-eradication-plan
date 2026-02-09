#!/usr/bin/env python3
"""Shared helpers for parsing validation output logs."""

from pathlib import Path


def extract_validation_errors(output: str, include_broken_external: bool = True) -> list[str]:
    """Extract key validation error lines from validator output."""
    errors: list[str] = []
    seen = set()
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        is_match = (
            "[CRITICAL:" in stripped
            or " [CRITICAL]:" in stripped
            or "[ERROR]" in stripped
            or stripped.startswith("ERROR:")
            or stripped.startswith("FATAL:")
            or "validation failed" in stripped.lower()
        )
        if include_broken_external:
            is_match = is_match or "BROKEN_EXTERNAL_LINK" in stripped

        if is_match and stripped not in seen:
            seen.add(stripped)
            errors.append(stripped)
    return errors


def extract_ai_fix_log_path(output: str) -> str | None:
    """Extract AI fix log file path emitted by pdf-validation.py output."""
    lines = [line.rstrip() for line in output.splitlines()]
    for idx, line in enumerate(lines):
        if "detailed fix instructions written to" not in line.lower():
            continue

        # Handle "written to: <path>" on same line.
        if ":" in line:
            candidate = line.split(":", 1)[1].strip()
            if candidate and not candidate.lower().startswith("to fix these issues"):
                return str(Path(candidate))

        # Handle path on following line.
        for next_idx in range(idx + 1, min(len(lines), idx + 5)):
            candidate = lines[next_idx].strip()
            if not candidate:
                continue
            if candidate.lower().startswith("to fix these issues"):
                break
            if candidate.lower().startswith("claude/ai:"):
                break
            return str(Path(candidate))
    return None
