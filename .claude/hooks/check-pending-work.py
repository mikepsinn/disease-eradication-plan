#!/usr/bin/env python3
"""
Claude Code Hook: Check for pending book work at session start.

Checks for:
1. PDF validation errors from recent renders
2. Book health issues from recent checks
3. Stale health reports that need refresh

Output: JSON with 'description' field injected into Claude's context.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
BUILD_TEMP = PROJECT_ROOT / "_build_temp"

# Thresholds
MAX_LOG_AGE_HOURS = 24
HEALTH_REPORT_STALE_HOURS = 12


def check_pdf_validation_errors() -> dict:
    """Check for recent PDF validation error logs."""
    if not BUILD_TEMP.exists():
        return {"found": False}

    cutoff = datetime.now() - timedelta(hours=MAX_LOG_AGE_HOURS)
    recent_logs = []

    for log_file in BUILD_TEMP.glob("pdf-validation-errors-*.md"):
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        if mtime > cutoff:
            # Parse summary
            content = log_file.read_text(encoding="utf-8")
            critical = 0
            total = 0
            for line in content.split("\n"):
                if "**Critical:**" in line:
                    try:
                        critical = int(line.split("**")[-1].strip())
                    except ValueError:
                        pass
                elif "**Total issues:**" in line:
                    try:
                        total = int(line.split("**")[-1].strip())
                    except ValueError:
                        pass

            recent_logs.append({
                "file": str(log_file),
                "name": log_file.stem.replace("pdf-validation-errors-", ""),
                "critical": critical,
                "total": total,
            })

    if not recent_logs:
        return {"found": False}

    return {
        "found": True,
        "logs": recent_logs,
        "total_critical": sum(l["critical"] for l in recent_logs),
        "total_issues": sum(l["total"] for l in recent_logs),
    }


def check_health_report() -> dict:
    """Check for recent book health report."""
    report_path = BUILD_TEMP / "book-health-report.md"

    if not report_path.exists():
        return {"found": False, "stale": True}

    mtime = datetime.fromtimestamp(report_path.stat().st_mtime)
    age_hours = (datetime.now() - mtime).total_seconds() / 3600

    if age_hours > HEALTH_REPORT_STALE_HOURS:
        return {"found": True, "stale": True, "age_hours": int(age_hours)}

    # Parse summary
    content = report_path.read_text(encoding="utf-8")
    total_issues = 0
    for line in content.split("\n"):
        if "**Total Issues:**" in line:
            try:
                total_issues = int(line.split("**")[-1].strip())
            except ValueError:
                pass
            break

    return {
        "found": True,
        "stale": False,
        "age_hours": int(age_hours),
        "total_issues": total_issues,
        "file": str(report_path),
    }


def main():
    """Check all pending work and output context."""
    pdf_errors = check_pdf_validation_errors()
    health_report = check_health_report()

    # Build context message
    context_lines = []
    has_work = False

    # PDF Validation Errors
    if pdf_errors.get("found"):
        has_work = True
        total = pdf_errors["total_issues"]
        critical = pdf_errors["total_critical"]

        if critical > 0:
            context_lines.append(f"## 🔴 PDF Validation: {critical} CRITICAL errors")
        else:
            context_lines.append(f"## 🟡 PDF Validation: {total} issues")

        context_lines.append("")
        for log in pdf_errors["logs"]:
            status = "🔴 CRITICAL" if log["critical"] > 0 else "🟡"
            context_lines.append(f"- {status} **{log['name']}**: {log['total']} issues")
            context_lines.append(f"  - Log: `{log['file']}`")
        context_lines.append("")
        context_lines.append("**Action:** Read the log file(s) for fix instructions.")
        context_lines.append("")

    # Book Health Report
    if health_report.get("stale"):
        context_lines.append("## ⚪ Book Health Check Needed")
        context_lines.append("")
        if health_report.get("found"):
            context_lines.append(f"Last health check was {health_report['age_hours']} hours ago.")
        else:
            context_lines.append("No health report found.")
        context_lines.append("")
        context_lines.append("**Action:** Run `/book-autopilot check` to assess book health.")
        context_lines.append("")
        has_work = True
    elif health_report.get("found") and health_report.get("total_issues", 0) > 0:
        has_work = True
        context_lines.append(f"## 📋 Book Health: {health_report['total_issues']} pending issues")
        context_lines.append("")
        context_lines.append(f"Report: `{health_report['file']}`")
        context_lines.append("")
        context_lines.append("**Action:** Run `/book-autopilot fix` to address issues.")
        context_lines.append("")

    if not has_work:
        print(json.dumps({"status": "ok", "message": "No pending work"}))
        return 0

    # Output context
    output = {
        "status": "pending_work",
        "description": "\n".join(context_lines),
        "pdf_errors": pdf_errors,
        "health_report": health_report,
    }

    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
