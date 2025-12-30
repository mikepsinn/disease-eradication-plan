#!/usr/bin/env python3
"""
Test PDF Rendering
==================

Fast test script for testing PDF rendering of any QMD file.
Automatically regenerates parameters/charts before testing.
Generates a minimal book config with the specified file as a chapter.

Usage:
    python scripts/test-pdf-render.py <file_path>

    # Test parameters-and-calculations.qmd
    python scripts/test-pdf-render.py knowledge/appendix/parameters-and-calculations.qmd

    # Test a specific file
    python scripts/test-pdf-render.py knowledge/appendix/regulatory-mortality-analysis.qmd

    # With venv:
    .venv/Scripts/python.exe scripts/test-pdf-render.py knowledge/appendix/parameters-and-calculations.qmd
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Test PDF rendering of a QMD file (regenerates parameters/charts first)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "file_path",
        help="Path to QMD file to test",
    )
    args = parser.parse_args()

    # Get project root (parent of scripts directory) and change to it
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    # Resolve file path
    test_file = project_root / args.file_path
    if not test_file.exists():
        print(f"[ERROR] File not found: {test_file}", file=sys.stderr)
        sys.exit(1)

    # Regenerate parameters/charts first
    print()
    print("=" * 80)
    print("[*] Regenerating parameters, charts, and calculations...")
    print("=" * 80)
    print()

    gen_script = project_root / "scripts" / "generate-everything-parameters-variables-calculations-references.py"
    gen_cmd = [sys.executable, str(gen_script)]

    try:
        result = subprocess.run(gen_cmd, check=True)
        if result.returncode != 0:
            print(f"[ERROR] Generation failed with exit code {result.returncode}", file=sys.stderr)
            sys.exit(result.returncode)
    except FileNotFoundError:
        print(f"[ERROR] Generation script not found: {gen_script}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print()
    print("=" * 80)
    print("[OK] Generation complete, starting PDF test...")
    print("=" * 80)
    print()

    # Clear Quarto caches to force re-execution of Python cells
    print("[*] Clearing Quarto caches...")
    import shutil
    cache_dirs = ["_freeze", "_site", "index_files", "knowledge/appendix/parameters-and-calculations_files"]
    for cache_dir in cache_dirs:
        cache_path = project_root / cache_dir
        if cache_path.exists():
            shutil.rmtree(cache_path)
            print(f"    Removed: {cache_dir}")
    print()

    # Get relative path from project root
    try:
        relative_path = test_file.relative_to(project_root)
    except ValueError:
        print(f"[ERROR] File must be inside project: {test_file}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Testing PDF rendering: {relative_path}")
    print()

    # Generate minimal _quarto.yml
    print("[*] Generating minimal _quarto.yml")
    quarto_config = project_root / "_quarto.yml"

    config_content = f"""project:
  type: book
  output-dir: _site/test
  execute-dir: project

book:
  title: "PDF Test: {relative_path.stem}"
  chapters:
    - index.qmd
    - {relative_path.as_posix()}

execute:
  fig-path: "knowledge/figures/"
  cache: false
  freeze: auto
  daemon: 300
  daemon-restart: false
  env:
    PYTHONPATH: "."

jupyter: dih-project-kernel

format:
  pdf:
    output-file: "test-{relative_path.stem}.pdf"
    documentclass: report
    echo: false
    toc: true
    toc-depth: 2
    number-sections: false
    colorlinks: true
    geometry:
      - top=1in
      - bottom=1in
      - left=1in
      - right=1in
    fontsize: 11pt
"""

    with open(quarto_config, 'w', encoding='utf-8') as f:
        f.write(config_content)

    # Create minimal index.qmd
    print("[*] Creating minimal index.qmd")
    index_qmd = project_root / "index.qmd"
    with open(index_qmd, 'w', encoding='utf-8') as f:
        f.write("---\ntitle: PDF Test\n---\n\n# PDF Rendering Test\n\nThis is a test render.\n")

    print(f"[*] Using Python: {sys.executable}")
    print()
    print("=" * 80)
    print("[*] Rendering PDF with Quarto...")
    print("=" * 80)

    # Set QUARTO_PYTHON to current Python (works for both system and venv)
    env = os.environ.copy()
    env["QUARTO_PYTHON"] = sys.executable

    # Run quarto render
    cmd = ["quarto", "render", "index.qmd", "--to", "pdf"]

    try:
        result = subprocess.run(cmd, env=env, check=False)

        print()
        print("=" * 80)
        if result.returncode == 0:
            print("[OK] PDF test render complete!")
            output_pdf = project_root / "_site" / "test" / "index.pdf"
            if output_pdf.exists():
                size_mb = output_pdf.stat().st_size / (1024 * 1024)
                print(f"[*] Output PDF: {output_pdf} ({size_mb:.1f} MB)")
        else:
            print(f"[ERROR] Render failed with exit code {result.returncode}")
            print()
            print("[*] Check index.log for detailed LaTeX errors")

            # Show last 30 lines of log if it exists
            log_file = project_root / "index.log"
            if log_file.exists():
                print()
                print("=" * 80)
                print("Last 30 lines of index.log:")
                print("=" * 80)
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines[-30:]:
                        print(line.rstrip())

        print("=" * 80)
        sys.exit(result.returncode)

    except FileNotFoundError:
        print("[ERROR] Quarto not found. Make sure Quarto is installed and in your PATH", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
