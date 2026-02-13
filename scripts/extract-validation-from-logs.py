#!/usr/bin/env python3
"""
Extract PDF validation errors from GitHub Actions logs and generate markdown checklists.

Usage:
    python scripts/extract-validation-from-logs.py <run-id>
    python scripts/extract-validation-from-logs.py 21972287999
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def parse_error_line(line: str) -> dict | None:
    """Parse a validation error line from the logs."""
    # Match pattern: /path/to/file.pdf:page N [SEVERITY:ERROR_TYPE] message - context
    pattern = r'([^:]+\.pdf):page (\d+) \[(\w+):([^\]]+)\] ([^-]+?)(?:\s+-\s+(.+))?$'
    match = re.search(pattern, line)

    if not match:
        return None

    pdf_path, page, severity, error_type, message, context = match.groups()

    # Extract PDF name from path
    pdf_name = Path(pdf_path).stem

    # Parse context fields
    suggested_fix = ""
    evidence_snippet = ""
    locator_hint = ""

    if context:
        for part in context.split(" | "):
            if part.startswith("suggested_fix="):
                suggested_fix = part[14:].strip()
            elif part.startswith("evidence_snippet="):
                evidence_snippet = part[17:].strip()
            elif part.startswith("locator_hint="):
                locator_hint = part[13:].strip()

    return {
        "pdf_name": pdf_name,
        "page": int(page),
        "severity": severity,
        "error_type": error_type,
        "message": message.strip(),
        "suggested_fix": suggested_fix,
        "evidence_snippet": evidence_snippet,
        "locator_hint": locator_hint,
    }


def generate_checklist(errors_by_pdf: dict) -> None:
    """Generate markdown checklist files for each PDF."""
    for pdf_name, errors_by_type in errors_by_pdf.items():
        output_file = Path(f"pdf-validation-checklist-{pdf_name}.md")

        # Count totals
        total = sum(len(errs) for errs in errors_by_type.values())
        critical = sum(len([e for e in errs if e["severity"] == "CRITICAL"]) for errs in errors_by_type.values())
        warnings = sum(len([e for e in errs if e["severity"] == "WARNING"]) for errs in errors_by_type.values())

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# PDF Validation Errors - Checklist\n\n")
            f.write(f"**PDF:** `{pdf_name}.pdf`\n")
            f.write(f"**Generated from GitHub Actions logs**\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Total issues:** {total}\n")
            f.write(f"- **Critical:** {critical}\n")
            f.write(f"- **Warnings:** {warnings}\n\n")
            f.write("---\n\n")

            # Group by error type
            for error_type, errors in sorted(errors_by_type.items()):
                severity_emoji = "🔴" if errors[0]["severity"] == "CRITICAL" else "🟡"
                f.write(f"## {severity_emoji} {error_type} ({len(errors)} issue(s))\n\n")
                f.write("### Occurrences\n\n")

                for error in sorted(errors, key=lambda e: e["page"]):
                    f.write(f"- [ ] **Page {error['page']}:** {error['message']}\n")

                    if error["suggested_fix"] or error["evidence_snippet"] or error["locator_hint"]:
                        context_parts = []
                        if error["suggested_fix"]:
                            context_parts.append(f"suggested_fix={error['suggested_fix']}")
                        if error["evidence_snippet"]:
                            context_parts.append(f"evidence_snippet={error['evidence_snippet']}")
                        if error["locator_hint"]:
                            context_parts.append(f"locator_hint={error['locator_hint']}")
                        f.write(f"  - Context: `{' | '.join(context_parts)}`\n")
                    f.write("\n")

        print(f"[✓] Generated: {output_file} ({total} issues)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract-validation-from-logs.py <run-id>")
        print("Example: python scripts/extract-validation-from-logs.py 21972287999")
        sys.exit(1)

    run_id = sys.argv[1]

    print(f"[*] Fetching logs for run {run_id}...")

    # Fetch logs using gh CLI
    import subprocess
    result = subprocess.run(
        ["gh", "run", "view", run_id, "--log"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        print(f"[ERROR] Failed to fetch logs: {result.stderr}")
        sys.exit(1)

    print(f"[*] Parsing validation errors...")

    # Parse errors from logs
    errors_by_pdf = defaultdict(lambda: defaultdict(list))

    for line in result.stdout.splitlines():
        error = parse_error_line(line)
        if error:
            pdf_name = error.pop("pdf_name")
            error_type = error["error_type"]
            errors_by_pdf[pdf_name][error_type].append(error)

    if not errors_by_pdf:
        print("[!] No validation errors found in logs")
        sys.exit(0)

    print(f"[*] Found errors in {len(errors_by_pdf)} PDF(s)")
    print(f"[*] Generating checklist files...")

    generate_checklist(errors_by_pdf)

    print(f"[✓] Done! Generated {len(errors_by_pdf)} checklist file(s)")


if __name__ == "__main__":
    main()
