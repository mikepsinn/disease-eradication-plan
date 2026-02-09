#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

import subprocess
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_ROOT / "render-validate-pdfs.log"


def run_and_tee(cmd: list[str], log_file) -> int:
    command_text = " ".join(cmd)
    print(f"[RUN] {command_text}", flush=True)
    log_file.write(f"\n[RUN] {command_text}\n")
    log_file.flush()

    process = subprocess.Popen(
        cmd,
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    for line in process.stdout or []:
        print(line, end="", flush=True)
        log_file.write(line)
    log_file.flush()
    process.wait()
    return int(process.returncode)


def main() -> int:
    print(f"[LOG] Writing all logs to: {LOG_PATH}", flush=True)

    with open(LOG_PATH, "w", encoding="utf-8") as log_file:
        log_file.write("=" * 80 + "\n")
        log_file.write("RENDER + VALIDATE PDF RUN\n")
        log_file.write(f"Started: {datetime.now().isoformat()}\n")
        log_file.write("=" * 80 + "\n")

        render_rc = run_and_tee(
            [sys.executable, "-u", "scripts/render-quarto.py", "manual", "--to", "pdf"],
            log_file,
        )
        if render_rc != 0:
            print(f"[ERROR] Render failed with exit code {render_rc}", flush=True)
            log_file.write(f"\n[ERROR] Render failed with exit code {render_rc}\n")
            return render_rc

        validate_rc = run_and_tee(
            [sys.executable, "-u", "scripts/pdf-validation.py", "--llm-pages", "0", "--skip-url-check"],
            log_file,
        )
        if validate_rc != 0:
            print(f"[ERROR] Validation failed with exit code {validate_rc}", flush=True)
            log_file.write(f"\n[ERROR] Validation failed with exit code {validate_rc}\n")
            return validate_rc

        print("[OK] Render and validation completed", flush=True)
        log_file.write("\n[OK] Render and validation completed\n")
        log_file.write(f"Finished: {datetime.now().isoformat()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
