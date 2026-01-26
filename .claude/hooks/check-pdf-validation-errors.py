#!/usr/bin/env python3
"""
Claude Code Hook: Check for pending PDF validation errors.

This hook runs at SessionStart and after Bash commands to check if there are
unresolved PDF validation errors that need attention.

Output format: JSON with optional 'description' field that gets injected into context.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Project root (parent of .claude directory)
PROJECT_ROOT = Path(__file__).parent.parent.parent
BUILD_TEMP = PROJECT_ROOT / "_build_temp"

# How old can error logs be before we ignore them (hours)
MAX_LOG_AGE_HOURS = 24


def find_recent_error_logs() -> list[Path]:
    """Find PDF validation error logs that are recent."""
    if not BUILD_TEMP.exists():
        return []

    cutoff = datetime.now() - timedelta(hours=MAX_LOG_AGE_HOURS)
    recent_logs = []

    for log_file in BUILD_TEMP.glob("pdf-validation-errors-*.md"):
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        if mtime > cutoff:
            recent_logs.append(log_file)

    return sorted(recent_logs, key=lambda p: p.stat().st_mtime, reverse=True)


def parse_error_summary(log_path: Path) -> dict:
    """Extract summary info from an error log."""
    content = log_path.read_text(encoding="utf-8")

    summary = {
        "file": str(log_path),
        "pdf": "",
        "total": 0,
        "critical": 0,
        "warnings": 0,
    }

    for line in content.split("\n"):
        if line.startswith("**PDF:**"):
            summary["pdf"] = line.split("`")[1] if "`" in line else ""
        elif "**Total issues:**" in line:
            try:
                summary["total"] = int(line.split("**")[-1].strip())
            except ValueError:
                pass
        elif "**Critical:**" in line:
            try:
                summary["critical"] = int(line.split("**")[-1].strip())
            except ValueError:
                pass
        elif "**Warnings:**" in line:
            try:
                summary["warnings"] = int(line.split("**")[-1].strip())
            except ValueError:
                pass

    return summary


def main():
    """Check for pending PDF validation errors and output context if found."""
    recent_logs = find_recent_error_logs()

    if not recent_logs:
        # No errors to report - exit silently
        print(json.dumps({"status": "ok"}))
        return 0

    # Parse all recent error logs
    summaries = [parse_error_summary(log) for log in recent_logs]

    # Check if any have critical errors
    has_critical = any(s["critical"] > 0 for s in summaries)
    total_issues = sum(s["total"] for s in summaries)

    if total_issues == 0:
        print(json.dumps({"status": "ok"}))
        return 0

    # Build context message for Claude
    context_lines = [
        "## Pending PDF Validation Errors",
        "",
        f"There are **{total_issues} unresolved issues** from recent PDF validation:",
        "",
    ]

    for summary in summaries:
        pdf_name = Path(summary["pdf"]).name if summary["pdf"] else "Unknown"
        status = "CRITICAL" if summary["critical"] > 0 else "warnings"
        context_lines.append(
            f"- **{pdf_name}**: {summary['total']} issues ({summary['critical']} critical, {summary['warnings']} warnings)"
        )
        context_lines.append(f"  - Log file: `{summary['file']}`")

    context_lines.extend([
        "",
        "**Action:** Read the log file(s) above with the `Read` tool for detailed fix instructions.",
        "",
    ])

    # Output JSON with description field (injected into Claude's context)
    output = {
        "status": "pending_errors",
        "description": "\n".join(context_lines),
        "error_logs": [str(log) for log in recent_logs],
        "has_critical": has_critical,
        "total_issues": total_issues,
    }

    print(json.dumps(output))

    # Return 0 to not block, but context is injected
    return 0


if __name__ == "__main__":
    sys.exit(main())
