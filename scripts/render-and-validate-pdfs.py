#!/usr/bin/env python3
import argparse
import sys
if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime
from pathlib import Path
import os
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from lib.build_logger import run_command_stream, suppress_pip_requirement_noise
from lib.quarto_config_utils import discover_paper_configs, count_qmd_files
from lib.validation_output_utils import extract_validation_errors, extract_ai_fix_log_path


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


def discover_papers_sorted_by_qmd_count() -> list[dict]:
    raw_papers = discover_paper_configs(PROJECT_ROOT)
    papers: list[dict] = []

    for config_name, info in raw_papers.items():
        pdf_filename = info.get("pdf_filename") or Path(info["pdf_path"]).name
        papers.append(
            {
                "config_name": config_name,
                "pdf_path": PROJECT_ROOT / "assets" / "pdfs" / pdf_filename,
                "qmd_count": count_qmd_files(info["config"]),
            }
        )

    papers.sort(key=lambda paper: paper["qmd_count"])
    return papers


def discover_configs_sorted_by_qmd_count(selected_configs: list[str] | None = None) -> list[dict]:
    """Discover configs for render/validate, optionally filtered by config names."""
    if not selected_configs:
        return discover_papers_sorted_by_qmd_count()

    selected_set = {name.strip() for name in selected_configs if name.strip()}
    configs: list[dict] = []
    missing: list[str] = []

    for config_name in sorted(selected_set):
        config_path = PROJECT_ROOT / f"_quarto-{config_name}.yml"
        if not config_path.exists():
            missing.append(config_name)
            continue
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        dih_render = config.get("dih-render", {})
        pdf_filename = (
            dih_render.get("pdf-output-file")
            or config.get("format", {}).get("pdf", {}).get("output-file")
            or f"{config_name}-paper.pdf"
        )
        configs.append(
            {
                "config_name": config_name,
                "pdf_path": PROJECT_ROOT / "assets" / "pdfs" / pdf_filename,
                "qmd_count": count_qmd_files(config),
            }
        )

    if missing:
        print(f"[ERROR] Unknown config(s): {', '.join(missing)}", flush=True)
        print("[ERROR] Expected files like _quarto-<config>.yml in project root", flush=True)
        return []

    configs.sort(key=lambda cfg: cfg["qmd_count"])
    return configs


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


def build_pdf_validation_command(pdf_path: Path) -> list[str]:
    """Build pdf-validation command."""
    cmd = [sys.executable, "-u", "scripts/pdf-validation.py", "--pdf", str(pdf_path)]
    if os.environ.get("PDF_VALIDATION_DISABLE_CACHE", "").lower() in {"1", "true", "yes", "on"}:
        cmd.append("--no-cache")
    return cmd


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
                [sys.executable, "-u", "scripts/render-quarto.py", config_name],
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
            validate_rc, validate_output = run_and_tee(
                build_pdf_validation_command(pdf_path),
                log_file,
            )
            result["validation_rc"] = validate_rc
            result["validation_errors"] = extract_validation_errors(validate_output)
            result["ai_fix_log_path"] = extract_ai_fix_log_path(validate_output)
            if validate_rc != 0:
                print(f"[ERROR] Validation failed for {pdf_path.name} with exit code {validate_rc}", flush=True)
                log_file.write(f"\n[ERROR] Validation failed for {pdf_path.name} with exit code {validate_rc}\n")
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
