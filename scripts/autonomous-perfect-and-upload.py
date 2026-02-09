#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autonomous paper perfection + Zenodo upload runner.

This orchestrator loops until all selected papers pass validation and upload:
1) Run scripts/upload-all-zenodo-and-save-dois.py
2) If failed, parse zenodo-upload-report.md checklist
3) Invoke `codex exec` to fix issues (no commits)
4) Repeat until success or max cycles reached

The upload script's perfected-state cache is used to skip already perfected papers.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from lib.build_logger import run_logged_command_stream
from lib.python_utils import get_preferred_python

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_SCRIPT = PROJECT_ROOT / "scripts" / "upload-all-zenodo-and-save-dois.py"
REPORT_PATH = PROJECT_ROOT / "zenodo-upload-report.md"
AUTONOMY_LOG_DIR = PROJECT_ROOT / "AUTONOMOUS-PIPELINE-LOGS"
STATUS_PATH = PROJECT_ROOT / "AUTONOMOUS-PIPELINE-STATUS.md"
PROGRESS_LOG_PATH = PROJECT_ROOT / "AUTONOMOUS-PIPELINE-PROGRESS.log"
LOCK_PATH = PROJECT_ROOT / "AUTONOMOUS-PIPELINE.lock"


if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def run_and_tee(
    cmd: list[str],
    log_path: Path,
    cwd: Path = PROJECT_ROOT,
    progress_log_path: Path | None = None,
) -> int:
    """Run command, stream output to console, and write full log."""
    command_display = " ".join(shlex.quote(c) for c in cmd)
    progress_file = None
    try:
        if progress_log_path:
            progress_file = progress_log_path.open("a", encoding="utf-8", errors="replace")
            start_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            progress_file.write(f"\n[{start_stamp}] [RUN] {command_display}\n")
            progress_file.write(f"[{start_stamp}] [LOG] {log_path}\n")
            progress_file.flush()

        return_code, _ = run_logged_command_stream(
            cmd=cmd,
            cwd=cwd,
            log_path=log_path,
            log_mode="w",
            extra_sinks=[progress_file] if progress_file else None,
            print_banner=True,
        )
        if progress_file:
            end_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            progress_file.write(f"\n[{end_stamp}] [EXIT] rc={return_code}\n")
            progress_file.flush()
        return return_code
    finally:
        if progress_file:
            progress_file.close()


def read_report() -> str:
    if not REPORT_PATH.exists():
        return ""
    return REPORT_PATH.read_text(encoding="utf-8", errors="replace")


def ensure_status_file() -> None:
    """Create append-only status file when it does not yet exist."""
    if STATUS_PATH.exists():
        return
    STATUS_PATH.write_text(
        "\n".join(
            [
                "# Autonomous Pipeline Status",
                "",
                "Append-only run log for autonomous build/validate/fix/rebuild/upload cycles.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def ensure_progress_file() -> None:
    """Create append-only root progress log when it does not yet exist."""
    if PROGRESS_LOG_PATH.exists():
        return
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    PROGRESS_LOG_PATH.write_text(
        "\n".join(
            [
                "AUTONOMOUS PIPELINE PROGRESS LOG",
                f"Created: {created_at}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def append_status(lines: list[str]) -> None:
    """Append markdown lines to the root status file."""
    ensure_status_file()
    with STATUS_PATH.open("a", encoding="utf-8", errors="replace") as f:
        for line in lines:
            f.write(f"{line}\n")
        f.write("\n")


def parse_failed_checklist(report_text: str) -> dict[str, list[str]]:
    """
    Parse failed papers from the report checklist.

    Preferred source: "## Autonomous Fix Checklist"
    Fallback: "## Errors and Warnings"
    """
    lines = report_text.splitlines()
    failures: dict[str, list[str]] = {}

    def parse_section(section_title: str, checklist_items: bool) -> dict[str, list[str]]:
        parsed: dict[str, list[str]] = {}
        in_section = False
        current_paper: str | None = None

        for raw_line in lines:
            line = raw_line.rstrip()
            if line.strip() == section_title:
                in_section = True
                current_paper = None
                continue
            if in_section and line.startswith("## "):
                break
            if not in_section:
                continue

            if line.startswith("### "):
                current_paper = line[4:].strip()
                if current_paper:
                    parsed.setdefault(current_paper, [])
                continue

            if not current_paper:
                continue

            stripped = line.strip()
            if checklist_items:
                if stripped.startswith("- [ ] "):
                    item = stripped[6:].strip()
                    if item:
                        parsed[current_paper].append(item)
            else:
                if stripped.startswith("- "):
                    item = stripped[2:].strip()
                    if item:
                        parsed[current_paper].append(item)

        return {k: v for k, v in parsed.items() if v}

    failures = parse_section("## Autonomous Fix Checklist", checklist_items=True)
    if failures:
        return failures

    failures = parse_section("## Errors and Warnings", checklist_items=False)
    if failures:
        return failures

    # Last fallback: parse FAILED rows from Validation Results table.
    table_failures: dict[str, list[str]] = {}
    for line in lines:
        # | paper | FAILED | ...
        m = re.match(r"^\|\s*([a-zA-Z0-9._-]+)\s*\|\s*FAILED\s*\|", line.strip())
        if m:
            paper_key = m.group(1)
            table_failures.setdefault(paper_key, ["Failed validation or upload (see report details)."])
    return table_failures


def get_git_head(cwd: Path = PROJECT_ROOT) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def build_codex_prompt(
    failures: dict[str, list[str]],
    selected_papers: list[str],
) -> str:
    papers = sorted(failures.keys())
    selected_text = ", ".join(selected_papers) if selected_papers else "(all papers)"

    lines: list[str] = [
        "You are fixing a failing autonomous Zenodo upload pipeline in this repository.",
        "Hard constraints:",
        "- DO NOT commit.",
        "- DO NOT create branches.",
        "- DO NOT push.",
        "- Keep changes local and minimal.",
        "",
        "Goal:",
        "- Fix all current failures listed in zenodo-upload-report.md.",
        "- Re-run only failing papers while fixing.",
        "- Stop only when each currently failing paper passes validation + upload.",
        "",
        f"Selected paper scope for this run: {selected_text}",
        "LLM validation mode for uploader: full-PDF review.",
        "",
        "Current failing papers and checklist items:",
    ]

    for paper_key in papers:
        lines.append(f"- {paper_key}:")
        for item in failures.get(paper_key, []):
            lines.append(f"  - {item}")

    lines.extend(
        [
            "",
            "Execution plan you must follow:",
            "1) Read zenodo-upload-report.md.",
            "2) Fix root causes in source/QMD/scripts.",
            "3) Re-run failing papers with force flags:",
            "   python scripts/upload-all-zenodo-and-save-dois.py --force-reprocess --force-revalidate <paper-key>",
            "4) Repeat fix+rerun until those papers pass.",
            "5) Finally run the uploader for selected scope to verify green state.",
            "",
            "Do not ask for confirmation; execute autonomously.",
        ]
    )
    return "\n".join(lines)


def resolve_codex_executable() -> str | None:
    """Resolve codex CLI executable across PATH and local venv."""
    local_candidates: list[Path] = []
    if sys.platform == "win32":
        local_candidates.extend(
            [
                PROJECT_ROOT / ".venv" / "Scripts" / "codex.exe",
                PROJECT_ROOT / ".venv" / "Scripts" / "codex.cmd",
                PROJECT_ROOT / ".venv" / "Scripts" / "codex.bat",
            ]
        )
    else:
        local_candidates.append(PROJECT_ROOT / ".venv" / "bin" / "codex")

    for candidate in local_candidates:
        if candidate.exists():
            return str(candidate)

    path_candidates = ["codex"]
    if sys.platform == "win32":
        path_candidates.extend(["codex.cmd", "codex.exe", "codex.bat"])

    for name in path_candidates:
        resolved = shutil.which(name)
        if resolved:
            return resolved

    return None


def codex_available(codex_exe: str) -> bool:
    try:
        return subprocess.run(
            [codex_exe, "--version"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False,
        ).returncode == 0
    except OSError:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Autonomously fix, validate, and upload papers to Zenodo using codex exec."
    )
    parser.add_argument("papers", nargs="*", help="Optional paper keys to limit scope.")
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=12,
        help="Maximum autonomous fix cycles before stopping (default: 12).",
    )
    parser.add_argument(
        "--codex-model",
        default="",
        help="Optional codex model override for codex exec.",
    )
    parser.add_argument(
        "--continue-on-validation-error",
        "--collect-all-validation-errors",
        dest="continue_on_validation_error",
        action="store_true",
        help=(
            "Pass through to uploader: continue validating remaining papers even when one fails validation; "
            "failed-validation papers are not uploaded."
        ),
    )
    parser.add_argument(
        "--ignore-perfected-cache-first-pass",
        "--force-reprocess-first",
        "--force-first",
        dest="force_reprocess_first",
        action="store_true",
        help=(
            "Ignore perfected-cache only on cycle 1 (descriptive name). "
            "Aliases: --force-reprocess-first, --force-first."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not UPLOAD_SCRIPT.exists():
        print(f"ERROR: Missing upload script: {UPLOAD_SCRIPT}")
        return 1
    codex_exe = resolve_codex_executable()

    AUTONOMY_LOG_DIR.mkdir(parents=True, exist_ok=True)
    ensure_progress_file()
    python_exe = get_preferred_python(PROJECT_ROOT)
    selected_papers = list(args.papers)
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 72)
    print("Autonomous Perfect + Upload Runner")
    print("=" * 72)
    print(f"Project root: {PROJECT_ROOT}")
    print("LLM validation mode: full-PDF review")
    print(f"Max cycles: {args.max_cycles}")
    print(f"Continue on validation error: {bool(args.continue_on_validation_error)}")
    print("No-commit policy: enforced in codex prompt + HEAD guard")
    if selected_papers:
        print(f"Paper scope: {', '.join(selected_papers)}")
    else:
        print("Paper scope: all papers")
    with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
        progress_file.write(f"\n=== RUN {run_id} STARTED {run_started_at} ===\n")
        progress_file.write(f"Project root: {PROJECT_ROOT}\n")
        progress_file.write(f"Paper scope: {', '.join(selected_papers) if selected_papers else 'all papers'}\n")
        progress_file.write("LLM validation mode: full-PDF review\n")
        progress_file.write(f"Max cycles: {args.max_cycles}\n")
        progress_file.write(f"Continue on validation error: {bool(args.continue_on_validation_error)}\n")
        progress_file.flush()
    append_status(
        [
            f"## Run {run_id} Started ({run_started_at})",
            "- Status: running",
            f"- Project root: `{PROJECT_ROOT}`",
            f"- Paper scope: `{', '.join(selected_papers) if selected_papers else 'all papers'}`",
            "- LLM validation mode: `full-PDF review`",
            f"- Max cycles: `{args.max_cycles}`",
            f"- Continue on validation error: `{bool(args.continue_on_validation_error)}`",
            f"- No-commit policy: `{True}`",
            f"- Codex executable: `{codex_exe or 'not found at start'}`",
            f"- Live progress log: `{PROGRESS_LOG_PATH}`",
        ]
    )

    base_upload_cmd = [python_exe, str(UPLOAD_SCRIPT)]
    if args.continue_on_validation_error:
        base_upload_cmd.append("--continue-on-validation-error")
    if selected_papers:
        base_upload_cmd.extend(selected_papers)

    for cycle in range(1, args.max_cycles + 1):
        cycle_tag = datetime.now().strftime("%Y%m%d-%H%M%S")
        cycle_started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'=' * 72}")
        print(f"CYCLE {cycle}/{args.max_cycles}")
        print("=" * 72)

        upload_cmd = list(base_upload_cmd)
        if cycle == 1 and args.force_reprocess_first:
            upload_cmd.insert(2, "--force-reprocess")

        upload_log = AUTONOMY_LOG_DIR / f"{cycle_tag}-cycle{cycle}-upload.log"
        append_status(
            [
                f"### Cycle {cycle} Started ({cycle_started_at})",
                "- Doing: run uploader and parse validation/upload report",
                f"- Command: `{' '.join(shlex.quote(c) for c in upload_cmd)}`",
                f"- Upload log: `{upload_log}`",
            ]
        )
        upload_rc = run_and_tee(upload_cmd, upload_log, progress_log_path=PROGRESS_LOG_PATH)
        if upload_rc == 0:
            print("\nSUCCESS: uploader completed with no failures.")
            print(f"Final report: {REPORT_PATH}")
            with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
                progress_file.write(
                    f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=SUCCESS ===\n"
                )
            append_status(
                [
                    f"### Cycle {cycle} Result",
                    "- Result: success",
                    "- Next: none (converged)",
                    f"- Final report: `{REPORT_PATH}`",
                    f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                    "- Status: success",
                ]
            )
            return 0

        report_text = read_report()
        failures = parse_failed_checklist(report_text)
        if not failures:
            print("\nERROR: uploader failed but no actionable failures were parsed from report.")
            print(f"Check logs: {upload_log}")
            print(f"Report path: {REPORT_PATH}")
            append_status(
                [
                    f"### Cycle {cycle} Result",
                    "- Result: failed",
                    "- Reason: uploader failed but checklist could not be parsed",
                    f"- Upload log: `{upload_log}`",
                    f"- Report path: `{REPORT_PATH}`",
                    f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                    "- Status: failed",
                ]
            )
            with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
                progress_file.write(
                    f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=FAILED ===\n"
                )
            return 1

        print("\nParsed failing papers:")
        for paper_key, items in sorted(failures.items()):
            print(f"  - {paper_key}: {len(items)} checklist item(s)")

        if cycle >= args.max_cycles:
            print("\nERROR: reached max cycles before convergence.")
            append_status(
                [
                    f"### Cycle {cycle} Result",
                    "- Result: failed",
                    f"- Reason: reached max cycles (`{args.max_cycles}`)",
                    f"- Report path: `{REPORT_PATH}`",
                    f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                    "- Status: failed",
                ]
            )
            with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
                progress_file.write(
                    f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=FAILED ===\n"
                )
            return 1

        if not codex_exe:
            codex_exe = resolve_codex_executable()
        if not codex_exe:
            print("\nERROR: Codex CLI is required for autonomous fixing but was not found.")
            print("Install/authenticate Codex CLI (`codex`) and rerun.")
            append_status(
                [
                    f"### Cycle {cycle} Result",
                    "- Result: failed",
                    "- Reason: codex executable not found when fix step was required",
                    f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                    "- Status: failed",
                ]
            )
            with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
                progress_file.write(
                    f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=FAILED ===\n"
                )
            return 1

        if not codex_available(codex_exe):
            print("\nERROR: Codex CLI is present but not runnable.")
            print(f"Resolved path: {codex_exe}")
            print("Verify installation/authentication, then rerun.")
            append_status(
                [
                    f"### Cycle {cycle} Result",
                    "- Result: failed",
                    "- Reason: codex executable resolved but --version failed",
                    f"- Codex executable: `{codex_exe}`",
                    f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                    "- Status: failed",
                ]
            )
            with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
                progress_file.write(
                    f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=FAILED ===\n"
                )
            return 1

        prompt_text = build_codex_prompt(
            failures=failures,
            selected_papers=selected_papers,
        )

        head_before = get_git_head()
        codex_log = AUTONOMY_LOG_DIR / f"{cycle_tag}-cycle{cycle}-codex.log"
        codex_last_message = AUTONOMY_LOG_DIR / f"{cycle_tag}-cycle{cycle}-codex-last-message.txt"

        codex_cmd = [
            codex_exe,
            "exec",
            "--dangerously-bypass-approvals-and-sandbox",
            "--cd",
            str(PROJECT_ROOT),
            "--output-last-message",
            str(codex_last_message),
        ]
        if args.codex_model:
            codex_cmd.extend(["--model", args.codex_model])
        codex_cmd.append(prompt_text)
        append_status(
            [
                f"### Cycle {cycle} Plan",
                "- Doing next: run codex autonomous fixer for failing papers",
                f"- Failing papers: `{', '.join(sorted(failures.keys()))}`",
                f"- Codex log path (next): `{codex_log}`",
            ]
        )

        codex_rc = run_and_tee(codex_cmd, codex_log, progress_log_path=PROGRESS_LOG_PATH)
        if codex_rc != 0:
            print("\nERROR: codex exec failed in fix cycle.")
            print(f"Check codex log: {codex_log}")
            append_status(
                [
                    f"### Cycle {cycle} Result",
                    "- Result: failed",
                    "- Reason: codex fixer returned non-zero exit code",
                    f"- Codex log: `{codex_log}`",
                    f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                    "- Status: failed",
                ]
            )
            with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
                progress_file.write(
                    f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=FAILED ===\n"
                )
            return 1

        head_after = get_git_head()
        if head_before and head_after and head_before != head_after:
            print("\nERROR: commit detected during autonomous run, which is disallowed.")
            print("Revert/inspect commits manually before continuing.")
            append_status(
                [
                    f"### Cycle {cycle} Result",
                    "- Result: failed",
                    "- Reason: commit detected during autonomous run (no-commit policy)",
                    f"- HEAD before: `{head_before}`",
                    f"- HEAD after: `{head_after}`",
                    f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
                    "- Status: failed",
                ]
            )
            with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
                progress_file.write(
                    f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=FAILED ===\n"
                )
            return 1

        append_status(
            [
                f"### Cycle {cycle} Result",
                "- Result: fixer completed, rerun uploader next cycle",
                f"- Codex log: `{codex_log}`",
                f"- Codex last message: `{codex_last_message}`",
            ]
        )

        # Small pause to avoid immediate API thrash loops on transient failures.
        time.sleep(1.0)

    print("\nERROR: unexpected loop termination.")
    append_status(
        [
            f"## Run {run_id} Completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
            "- Status: failed",
            "- Reason: unexpected loop termination",
        ]
    )
    with PROGRESS_LOG_PATH.open("a", encoding="utf-8", errors="replace") as progress_file:
        progress_file.write(
            f"\n=== RUN {run_id} COMPLETED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS=FAILED ===\n"
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
