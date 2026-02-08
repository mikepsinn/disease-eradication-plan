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
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_SCRIPT = PROJECT_ROOT / "scripts" / "upload-all-zenodo-and-save-dois.py"
REPORT_PATH = PROJECT_ROOT / "zenodo-upload-report.md"
AUTONOMY_CACHE_DIR = PROJECT_ROOT / ".cache" / "autonomous-perfect-upload"
AUTONOMY_LOG_DIR = AUTONOMY_CACHE_DIR / "logs"


if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def get_preferred_python() -> str:
    if sys.platform == "win32":
        venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = PROJECT_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def run_and_tee(cmd: list[str], log_path: Path, cwd: Path = PROJECT_ROOT) -> int:
    """Run command, stream output to console, and write full log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\n[RUN] {' '.join(shlex.quote(c) for c in cmd)}", flush=True)
    print(f"[LOG] {log_path}", flush=True)

    with log_path.open("w", encoding="utf-8", errors="replace") as log_file:
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
            print(line, end="")
            log_file.write(line)
        process.wait()
        return int(process.returncode)


def read_report() -> str:
    if not REPORT_PATH.exists():
        return ""
    return REPORT_PATH.read_text(encoding="utf-8", errors="replace")


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
    llm_pages: int,
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
        f"LLM pages setting for uploader: {llm_pages} (0 means full PDF).",
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
            "   python scripts/upload-all-zenodo-and-save-dois.py --force-reprocess --force-revalidate "
            + "--llm-pages "
            + str(llm_pages)
            + " <paper-key>",
            "4) Repeat fix+rerun until those papers pass.",
            "5) Finally run the uploader for selected scope to verify green state.",
            "",
            "Do not ask for confirmation; execute autonomously.",
        ]
    )
    return "\n".join(lines)


def codex_available() -> bool:
    return subprocess.run(
        ["codex", "--version"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        check=False,
    ).returncode == 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Autonomously fix, validate, and upload papers to Zenodo using codex exec."
    )
    parser.add_argument("papers", nargs="*", help="Optional paper keys to limit scope.")
    parser.add_argument(
        "--llm-pages",
        type=int,
        default=0,
        help="LLM pages for uploader (0 = full PDF, default: 0).",
    )
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
        "--force-reprocess-first",
        action="store_true",
        help="Force first uploader pass to process selected papers even if perfected cache exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not UPLOAD_SCRIPT.exists():
        print(f"ERROR: Missing upload script: {UPLOAD_SCRIPT}")
        return 1
    if not codex_available():
        print("ERROR: `codex` CLI not found in PATH.")
        print("Install/authenticate Codex CLI first, then rerun this script.")
        return 1

    AUTONOMY_LOG_DIR.mkdir(parents=True, exist_ok=True)
    python_exe = get_preferred_python()
    selected_papers = list(args.papers)

    print("=" * 72)
    print("Autonomous Perfect + Upload Runner")
    print("=" * 72)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"LLM pages: {args.llm_pages} ({'full PDF' if args.llm_pages == 0 else 'sampled'})")
    print(f"Max cycles: {args.max_cycles}")
    print("No-commit policy: enforced in codex prompt + HEAD guard")
    if selected_papers:
        print(f"Paper scope: {', '.join(selected_papers)}")
    else:
        print("Paper scope: all papers")

    base_upload_cmd = [python_exe, str(UPLOAD_SCRIPT), "--llm-pages", str(args.llm_pages)]
    if selected_papers:
        base_upload_cmd.extend(selected_papers)

    for cycle in range(1, args.max_cycles + 1):
        cycle_tag = datetime.now().strftime("%Y%m%d-%H%M%S")
        print(f"\n{'=' * 72}")
        print(f"CYCLE {cycle}/{args.max_cycles}")
        print("=" * 72)

        upload_cmd = list(base_upload_cmd)
        if cycle == 1 and args.force_reprocess_first:
            upload_cmd.insert(2, "--force-reprocess")

        upload_log = AUTONOMY_LOG_DIR / f"{cycle_tag}-cycle{cycle}-upload.log"
        upload_rc = run_and_tee(upload_cmd, upload_log)
        if upload_rc == 0:
            print("\nSUCCESS: uploader completed with no failures.")
            print(f"Final report: {REPORT_PATH}")
            return 0

        report_text = read_report()
        failures = parse_failed_checklist(report_text)
        if not failures:
            print("\nERROR: uploader failed but no actionable failures were parsed from report.")
            print(f"Check logs: {upload_log}")
            print(f"Report path: {REPORT_PATH}")
            return 1

        print("\nParsed failing papers:")
        for paper_key, items in sorted(failures.items()):
            print(f"  - {paper_key}: {len(items)} checklist item(s)")

        if cycle >= args.max_cycles:
            print("\nERROR: reached max cycles before convergence.")
            return 1

        prompt_text = build_codex_prompt(
            failures=failures,
            llm_pages=args.llm_pages,
            selected_papers=selected_papers,
        )

        head_before = get_git_head()
        codex_log = AUTONOMY_LOG_DIR / f"{cycle_tag}-cycle{cycle}-codex.log"
        codex_last_message = AUTONOMY_LOG_DIR / f"{cycle_tag}-cycle{cycle}-codex-last-message.txt"

        codex_cmd = [
            "codex",
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

        codex_rc = run_and_tee(codex_cmd, codex_log)
        if codex_rc != 0:
            print("\nERROR: codex exec failed in fix cycle.")
            print(f"Check codex log: {codex_log}")
            return 1

        head_after = get_git_head()
        if head_before and head_after and head_before != head_after:
            print("\nERROR: commit detected during autonomous run, which is disallowed.")
            print("Revert/inspect commits manually before continuing.")
            return 1

        # Small pause to avoid immediate API thrash loops on transient failures.
        time.sleep(1.0)

    print("\nERROR: unexpected loop termination.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

