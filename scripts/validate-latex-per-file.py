#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate LaTeX rendering for individual QMD files.

Renders each QMD file to PDF individually to isolate LaTeX errors.
Much faster for finding which specific file has issues than rendering the whole book.

Usage:
    python scripts/validate-latex-per-file.py                    # Test all QMD files
    python scripts/validate-latex-per-file.py --parallel 4       # Run 4 files in parallel
    python scripts/validate-latex-per-file.py --file path.qmd    # Test single file
    python scripts/validate-latex-per-file.py --quick            # Quick mode (first error stops)
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple, Optional

# Set UTF-8 encoding for Windows (reconfigure exists on TextIOWrapper at runtime)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


def get_qmd_files() -> List[Path]:
    """Get all QMD files that should be validated."""
    qmd_files = []

    # Directories to search
    search_dirs = [
        PROJECT_ROOT / "knowledge",
        PROJECT_ROOT / "index-manual.qmd",
    ]

    # Also include top-level QMD files
    for f in PROJECT_ROOT.glob("*.qmd"):
        if f.name not in ["references.qmd", "index.qmd"]:  # Skip special files
            qmd_files.append(f)

    # Search knowledge directory
    knowledge_dir = PROJECT_ROOT / "knowledge"
    if knowledge_dir.exists():
        for f in knowledge_dir.rglob("*.qmd"):
            # Skip figure files (they're not standalone documents)
            if "figures" not in str(f):
                qmd_files.append(f)

    return sorted(qmd_files)


def render_qmd_to_pdf(qmd_file: Path, temp_dir: Path) -> Tuple[Path, bool, str]:
    """
    Render a single QMD file to PDF.

    Returns:
        Tuple of (file_path, success, error_message)
    """
    # Create a minimal standalone QMD wrapper
    file_name = qmd_file.stem
    output_dir = temp_dir / file_name
    output_dir.mkdir(exist_ok=True)

    try:
        # Run quarto render on the single file
        result = subprocess.run(
            [
                "quarto", "render", str(qmd_file),
                "--to", "pdf",
                "--output-dir", str(output_dir),
                "--no-clean",  # Keep intermediate files for debugging
            ],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout per file
            cwd=PROJECT_ROOT,
        )

        if result.returncode == 0:
            return (qmd_file, True, "")
        else:
            # Extract relevant error from output
            error_msg = extract_latex_error(result.stderr + result.stdout)
            return (qmd_file, False, error_msg)

    except subprocess.TimeoutExpired:
        return (qmd_file, False, "TIMEOUT: Render took longer than 120 seconds")
    except Exception as e:
        return (qmd_file, False, f"EXCEPTION: {str(e)}")


def extract_latex_error(output: str) -> str:
    """Extract the most relevant LaTeX error from quarto output."""
    lines = output.split('\n')
    error_lines = []

    # Look for common error patterns
    capture = False
    for i, line in enumerate(lines):
        # Start capturing on error indicators
        if any(x in line.lower() for x in ['error:', '! ', 'fatal error', '@writefile']):
            capture = True

        if capture:
            error_lines.append(line)
            if len(error_lines) > 10:  # Limit context
                break

    if error_lines:
        return '\n'.join(error_lines)

    # Fallback: return last 5 lines
    return '\n'.join(lines[-5:]) if lines else "Unknown error"


def validate_with_chktex(qmd_file: Path) -> Tuple[Path, List[str]]:
    """
    Run chktex on the LaTeX generated from a QMD file.
    This is faster than full PDF rendering.

    Returns:
        Tuple of (file_path, list_of_warnings)
    """
    # First, render to tex only
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        try:
            # Render to LaTeX only (faster than PDF)
            result = subprocess.run(
                [
                    "quarto", "render", str(qmd_file),
                    "--to", "latex",
                    "--output-dir", str(temp_path),
                ],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=PROJECT_ROOT,
            )

            if result.returncode != 0:
                return (qmd_file, [f"Quarto render failed: {result.stderr[:200]}"])

            # Find generated .tex file
            tex_files = list(temp_path.glob("*.tex"))
            if not tex_files:
                return (qmd_file, ["No .tex file generated"])

            # Run chktex if available
            chktex_result = subprocess.run(
                ["chktex", "-q", str(tex_files[0])],
                capture_output=True,
                text=True,
                timeout=30,
            )

            warnings = [line for line in chktex_result.stdout.split('\n') if line.strip()]
            return (qmd_file, warnings)

        except FileNotFoundError:
            return (qmd_file, ["chktex not installed - install with: choco install chktex"])
        except subprocess.TimeoutExpired:
            return (qmd_file, ["TIMEOUT"])
        except Exception as e:
            return (qmd_file, [str(e)])


def main():
    parser = argparse.ArgumentParser(description="Validate LaTeX rendering for QMD files")
    parser.add_argument("--file", "-f", help="Test a specific file")
    parser.add_argument("--parallel", "-p", type=int, default=1, help="Number of parallel renders")
    parser.add_argument("--quick", "-q", action="store_true", help="Stop on first error")
    parser.add_argument("--chktex", action="store_true", help="Use chktex instead of full render")
    parser.add_argument("--list", "-l", action="store_true", help="List files that would be tested")
    args = parser.parse_args()

    # Get files to test
    if args.file:
        qmd_files = [Path(args.file)]
    else:
        qmd_files = get_qmd_files()

    if args.list:
        print(f"Found {len(qmd_files)} QMD files to validate:")
        for f in qmd_files:
            print(f"  {f.relative_to(PROJECT_ROOT)}")
        return

    print(f"Validating {len(qmd_files)} QMD files...")
    print("=" * 60)

    failed_files = []
    passed_files = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        if args.parallel > 1:
            # Parallel execution
            with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                if args.chktex:
                    futures = {executor.submit(validate_with_chktex, f): f for f in qmd_files}
                else:
                    futures = {executor.submit(render_qmd_to_pdf, f, temp_path): f for f in qmd_files}

                for future in as_completed(futures):
                    result = future.result()
                    process_result(result, passed_files, failed_files, args.chktex)

                    if args.quick and failed_files:
                        print("\n[QUICK MODE] Stopping after first error")
                        break
        else:
            # Sequential execution
            for qmd_file in qmd_files:
                print(f"Testing: {qmd_file.relative_to(PROJECT_ROOT)}...", end=" ", flush=True)

                if args.chktex:
                    result = validate_with_chktex(qmd_file)
                else:
                    result = render_qmd_to_pdf(qmd_file, temp_path)

                process_result(result, passed_files, failed_files, args.chktex)

                if args.quick and failed_files:
                    print("\n[QUICK MODE] Stopping after first error")
                    break

    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {len(passed_files)} passed, {len(failed_files)} failed")

    if failed_files:
        print("\nFAILED FILES:")
        for f, error in failed_files:
            print(f"\n  {f.relative_to(PROJECT_ROOT)}:")
            for line in error.split('\n')[:5]:
                print(f"    {line}")
        sys.exit(1)
    else:
        print("\nAll files passed LaTeX validation!")
        sys.exit(0)


def process_result(result, passed_files, failed_files, is_chktex):
    """Process a validation result."""
    if is_chktex:
        file_path, warnings = result
        if warnings and not all('not installed' in w for w in warnings):
            failed_files.append((file_path, '\n'.join(warnings)))
            print("WARNINGS")
        else:
            passed_files.append(file_path)
            print("OK")
    else:
        file_path, success, error = result
        if success:
            passed_files.append(file_path)
            print("OK")
        else:
            failed_files.append((file_path, error))
            print("FAILED")


if __name__ == "__main__":
    main()
