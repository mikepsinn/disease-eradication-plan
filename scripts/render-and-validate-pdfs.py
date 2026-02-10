#!/usr/bin/env python3
import argparse
import sys
if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.build_logger import run_command_stream, suppress_pip_requirement_noise
from lib.quarto_config_utils import discover_pdf_work_items_sorted
from lib.pdf_validation_runner import run_pdf_validation
from lib.python_utils import get_preferred_python


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_ROOT / "render-validate-pdfs.log"
REPORT_PATH = PROJECT_ROOT / "render-validate-pdfs-report.md"


def run_and_tee(cmd: list[str], log_file) -> tuple[int, str]:
    command_text = " ".join(cmd)
    print(f"[RUN] {command_text}", flush=True)
    log_file.write(f"\n[RUN] {command_text}\n")
    log_file.flush()
    filters = [suppress_pip_requirement_noise] if "scripts/render-quarto.py" in command_text else []
    return run_command_stream(
        cmd=cmd,
        cwd=PROJECT_ROOT,
        log_file=log_file,
        suppress_filters=filters,
    )


def discover_configs_sorted_by_qmd_count(selected_configs: list[str] | None = None) -> list[dict]:
    """Discover configs for render/validate, optionally filtered by config names."""
    items = discover_pdf_work_items_sorted(
        project_root=PROJECT_ROOT,
        selected_configs=selected_configs,
    )
    if selected_configs:
        selected_set = {name.strip() for name in selected_configs if name.strip()}
        found_set = {item["config_name"] for item in items}
        missing = sorted(selected_set - found_set)
        if missing:
            print(f"[ERROR] Unknown config(s): {', '.join(missing)}", flush=True)
            print("[ERROR] Expected files like _quarto-<config>.yml in project root", flush=True)
            return []
    return [
        {
            "config_name": item["config_name"],
            "pdf_path": item["assets_pdf_path"],
            "qmd_count": item["qmd_count"],
        }
        for item in items
    ]


def extract_render_errors(output: str) -> list[str]:
    errors: list[str] = []
    seen = set()
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if (
            "ERROR" in stripped
            or "FATAL" in stripped
            or "Traceback" in stripped
            or "Exception" in stripped
            or "FAILED" in stripped
        ):
            if stripped not in seen:
                seen.add(stripped)
                errors.append(stripped)
    return errors


def write_report(results: list[dict]) -> None:
    passed = [r for r in results if r["status"] == "passed"]
    failed = [r for r in results if r["status"] != "passed"]

    lines = [
        "# Render and Validate PDFs Report",
        "",
        f"**Generated:** {datetime.now().isoformat()}",
        f"**Log file:** `{LOG_PATH}`",
        "",
        "## Summary",
        "",
        f"- Total configs: {len(results)}",
        f"- Passed: {len(passed)}",
        f"- Failed: {len(failed)}",
        "",
    ]

    if failed:
        lines.extend(
            [
                "## Fix Checklist",
                "",
            ]
        )
        for result in failed:
            lines.append(f"### {result['config_name']}")
            lines.append("")
            lines.append(f"- [ ] Resolve failures for `{result['config_name']}`")
            if result.get("render_rc", 0) != 0:
                lines.append(f"- [ ] Fix render failure (exit code {result['render_rc']})")
                for err in result.get("render_errors", []):
                    lines.append(f"- [ ] {err}")
            if result.get("validation_rc") is not None and result.get("validation_rc", 0) != 0:
                lines.append(f"- [ ] Fix validation failure (exit code {result['validation_rc']})")
                for err in result.get("validation_errors", []):
                    lines.append(f"- [ ] {err}")
            if result.get("ai_fix_log_path"):
                lines.append(f"- [ ] Review AI fix guide: `{result['ai_fix_log_path']}`")
            lines.append("")

    lines.extend(
        [
            "## Per Config Results",
            "",
            "| Config | QMD Files | Status | Render RC | Validation RC | PDF |",
            "|--------|-----------|--------|-----------|---------------|-----|",
        ]
    )
    for result in results:
        lines.append(
            f"| {result['config_name']} | {result['qmd_count']} | {result['status']} | "
            f"{result.get('render_rc', 'N/A')} | {result.get('validation_rc', 'N/A')} | "
            f"`{result['pdf_path']}` |"
        )
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render and validate PDFs for Quarto configs")
    parser.add_argument(
        "--config",
        action="append",
        help="Specific config name to process (e.g., --config test). Can be provided multiple times.",
    )
    args = parser.parse_args()

    print(f"[LOG] Writing all logs to: {LOG_PATH}", flush=True)
    print(f"[REPORT] Checklist report will be saved to: {REPORT_PATH}", flush=True)
    print("[VALIDATION] Using scripts/pdf-validation.py", flush=True)

    python_exe = get_preferred_python(PROJECT_ROOT)

    with open(LOG_PATH, "w", encoding="utf-8") as log_file:
        log_file.write("=" * 80 + "\n")
        log_file.write("RENDER + VALIDATE PDF RUN\n")
        log_file.write(f"Started: {datetime.now().isoformat()}\n")
        log_file.write("=" * 80 + "\n")
        log_file.flush()

        papers = discover_configs_sorted_by_qmd_count(args.config)
        if not papers:
            print("[ERROR] No configs found to render", flush=True)
            log_file.write("\n[ERROR] No configs found to render\n")
            write_report([])
            return 1

        print("[*] Render order by QMD count (smallest first):", flush=True)
        for paper in papers:
            order_line = f"  - {paper['config_name']}: {paper['qmd_count']} QMD files"
            print(order_line, flush=True)
            log_file.write(order_line + "\n")
        log_file.flush()

        results: list[dict] = []
        for paper in papers:
            config_name = paper["config_name"]
            pdf_path = paper["pdf_path"]
            result = {
                "config_name": config_name,
                "qmd_count": paper["qmd_count"],
                "pdf_path": str(pdf_path),
                "status": "pending",
                "render_rc": None,
                "validation_rc": None,
                "render_errors": [],
                "validation_errors": [],
                "ai_fix_log_path": None,
            }
            print(f"\n[*] Rendering {config_name}...", flush=True)
            render_rc, render_output = run_and_tee(
                [python_exe, "-u", "scripts/render-quarto.py", config_name],
                log_file,
            )
            result["render_rc"] = render_rc
            result["render_errors"] = extract_render_errors(render_output)
            if render_rc != 0:
                print(f"[ERROR] Render failed for {config_name} with exit code {render_rc}", flush=True)
                log_file.write(f"\n[ERROR] Render failed for {config_name} with exit code {render_rc}\n")
                result["status"] = "render_failed"
                results.append(result)
                continue

            print(f"[*] Validating {pdf_path.name}...", flush=True)
            validation_result = run_pdf_validation(
                pdf_path=pdf_path,
                cwd=PROJECT_ROOT,
                python_executable=python_exe,
                skip_url_check=True,
                use_cache=True,
                verbose=True,
                line_filter=lambda display_line: (
                    display_line.startswith("[VALIDATION]")
                    or display_line.startswith("   Validating:")
                    or display_line.startswith("[LLM]")
                    or display_line.startswith("[WARNING]")
                    or display_line.startswith("[ERROR]")
                    or display_line.startswith("ERROR:")
                    or display_line.startswith("FATAL:")
                    or display_line.startswith("[OK]")
                    or "validation failed" in display_line.lower()
                ),
            )
            log_file.write(validation_result.output)
            log_file.flush()
            result["validation_rc"] = validation_result.returncode
            result["validation_errors"] = validation_result.errors
            result["ai_fix_log_path"] = validation_result.ai_fix_log_path
            llm_skipped = (
                "LLM validation skipped" in validation_result.output
                or "LLM library not available, skipping LLM validation" in validation_result.output
            )
            if llm_skipped and validation_result.returncode == 0:
                result["validation_errors"].append(
                    "LLM validation was skipped; treating as failure for render-and-validate flow."
                )
                result["validation_rc"] = 1
            if validation_result.returncode != 0:
                print(
                    f"[ERROR] Validation failed for {pdf_path.name} with exit code {validation_result.returncode}",
                    flush=True,
                )
                log_file.write(
                    f"\n[ERROR] Validation failed for {pdf_path.name} with exit code {validation_result.returncode}\n"
                )
                result["status"] = "validation_failed"
                results.append(result)
                continue
            if result["validation_rc"] != 0:
                print(
                    f"[ERROR] Validation failed for {pdf_path.name} (LLM validation skipped)",
                    flush=True,
                )
                log_file.write(
                    f"\n[ERROR] Validation failed for {pdf_path.name} (LLM validation skipped)\n"
                )
                result["status"] = "validation_failed"
                results.append(result)
                continue

            result["status"] = "passed"
            results.append(result)

        write_report(results)
        failed_count = len([r for r in results if r["status"] != "passed"])
        if failed_count > 0:
            print(f"[ERROR] Completed with {failed_count} failing config(s)", flush=True)
            print(f"[REPORT] Review checklist: {REPORT_PATH}", flush=True)
            log_file.write(f"\n[ERROR] Completed with {failed_count} failing config(s)\n")
            log_file.write(f"[REPORT] Review checklist: {REPORT_PATH}\n")
            log_file.write(f"Finished: {datetime.now().isoformat()}\n")
            return 1

        print("[OK] Render and validation completed", flush=True)
        print(f"[REPORT] Checklist report saved to: {REPORT_PATH}", flush=True)
        log_file.write("\n[OK] Render and validation completed\n")
        log_file.write(f"[REPORT] Checklist report saved to: {REPORT_PATH}\n")
        log_file.write(f"Finished: {datetime.now().isoformat()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
