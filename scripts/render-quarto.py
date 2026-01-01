#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render Quarto Config
====================

Unified script to render any Quarto configuration. Automatically handles:
- HTML rendering with post-processing link rewriting
- PDF rendering with pre-processing link rewriting in temp folder
- Mixed formats (renders both HTML and PDF as configured)
- Build monitoring with timeout detection (prevents hung CI builds)
- Real-time progress tracking and profiling
- PDF validation for Python code leakage

Usage:
    python render-quarto.py economics                # Render economics (all formats in config)
    python render-quarto.py wishocracy               # Render wishocracy (all formats in config)
    python render-quarto.py iab                      # Render IAB (all formats in config)
    python render-quarto.py test --verify            # Render test config with verification
    python render-quarto.py economics --to pdf       # Render only PDF format
    python render-quarto.py economics --to html      # Render only HTML format
    python render-quarto.py book --timeout 1800      # Custom timeout (30 min)
    python render-quarto.py book --kill-existing     # Kill stale Quarto processes first
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Force line buffering for GitHub Actions (ensures output appears immediately)
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from quarto_pre_build import (
    prepare_economics,
    prepare_wishocracy,
    prepare_iab,
    prepare_test,
    prepare_book,
    prepare_pdf_build_temp
)
from render_utils import (
    BuildMonitor,
    create_latex_parser,
    ensure_jupyter_kernel,
    kill_existing_quarto_processes,
    run_pre_validation,
    run_post_validation,
    validate_pdf_for_python_code
)


# Configuration mapping
CONFIGS = {
    "economics": {
        "config_file": "_quarto-economics.yml",
        "prepare_fn": prepare_economics,
        "description": "Economics models"
    },
    "wishocracy": {
        "config_file": "_quarto-wishocracy.yml",
        "prepare_fn": prepare_wishocracy,
        "description": "Wishocracy paper"
    },
    "iab": {
        "config_file": "_quarto-iab.yml",
        "prepare_fn": prepare_iab,
        "description": "Incentive Alignment Bonds paper"
    },
    "test": {
        "config_file": "_quarto-test.yml",
        "prepare_fn": prepare_test,
        "description": "Test configuration"
    },
    "book": {
        "config_file": "_quarto-book.yml",
        "prepare_fn": prepare_book,
        "description": "Complete book"
    }
}


def render_quarto(
    config_name: str,
    format_override: str = None,
    verify: bool = False,
    quarto_args: list = None,
    timeout: int = 900,
    log_file: str = None,
    fail_on_warnings: bool = True,
    kill_existing: bool = False
) -> int:
    """
    Render Quarto configuration.

    Args:
        config_name: Name of configuration (economics, wishocracy, iab, test, book)
        format_override: Override format (pdf, html, or None for all formats in config)
        verify: Run verification tests after rendering (test config only)
        quarto_args: Additional arguments to pass to quarto render
        timeout: Seconds with no output before killing build (default: 900 = 15min)
        log_file: Path to log file (default: build-{config}.log)
        fail_on_warnings: Whether to fail build on warnings (default: True)
        kill_existing: Kill existing Quarto/LaTeX processes before starting

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if config_name not in CONFIGS:
        print(f"[ERROR] Unknown config: {config_name}", file=sys.stderr)
        print(f"        Available configs: {', '.join(CONFIGS.keys())}", file=sys.stderr)
        return 1

    config = CONFIGS[config_name]

    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent.absolute()
    original_cwd = os.getcwd()

    # Set default log file if not specified
    if log_file is None:
        log_file = f"build-{config_name}.log"

    exit_code = 0
    build_temp = None
    monitor = None

    try:
        # Determine if we're rendering PDF
        rendering_pdf = format_override == "pdf" or format_override is None

        # Change to project root for setup
        os.chdir(project_root)

        # 0. Kill existing Quarto/LaTeX processes if requested
        if kill_existing:
            print("=" * 80)
            print("KILLING EXISTING QUARTO/LaTeX PROCESSES")
            print("=" * 80)
            killed = kill_existing_quarto_processes(include_latex=rendering_pdf)
            if killed > 0:
                print(f"[OK] Killed {killed} existing process(es)")
            else:
                print("[*] No existing processes found")
            print()

        # 1. Ensure Jupyter kernel exists
        print("=" * 80)
        print("SETUP: JUPYTER KERNEL")
        print("=" * 80)
        if not ensure_jupyter_kernel("dih-project-kernel", "DIH Project"):
            print("[WARNING] Jupyter kernel setup failed, continuing anyway...")
        print()

        # 2. Run pre-validation
        print("=" * 80)
        print("VALIDATION: PRE-RENDER")
        print("=" * 80)
        validation_exit = run_pre_validation()
        if validation_exit != 0:
            print("[ERROR] Pre-validation failed, aborting render", file=sys.stderr)
            return validation_exit
        print()

        # 3. Prepare files in project root (config + index)
        print("=" * 80)
        print(f"SETUP: PREPARING {config['description'].upper()} FILES")
        print("=" * 80)
        print(f"[*] Preparing {config['description']} files...")
        if not config["prepare_fn"]():
            return 1

        # If rendering PDF, use temp folder approach
        if rendering_pdf:
            print("=" * 80)
            print("CREATING TEMPORARY BUILD DIRECTORY FOR PDF")
            print("=" * 80)
            build_temp = prepare_pdf_build_temp(
                source_config=config["config_file"],
                target_config="_quarto-book.yml",
                target_url="https://manual.WarOnDisease.org",
                verbose=True
            )

            if build_temp is None:
                print("[ERROR] Failed to create temp build directory", file=sys.stderr)
                return 1

            # Change to temp directory for rendering
            os.chdir(build_temp)
            print(f"[*] Changed to temp directory: {build_temp}")

        # Build quarto render command
        print("=" * 80)
        print(f"RENDERING {config['description'].upper()}")
        print("=" * 80)
        cmd = ["quarto", "render"]

        # Add format override if specified
        if format_override:
            cmd.extend(["--to", format_override])

        # Add additional quarto args
        if quarto_args:
            cmd.extend(quarto_args)

        # Create BuildMonitor for timeout detection, logging, and progress tracking
        # Use longer timeout for PDF builds (LaTeX can be slow)
        effective_timeout = timeout if not rendering_pdf else max(timeout, 900)
        monitor = BuildMonitor(
            timeout_seconds=effective_timeout,
            fail_on_warnings=fail_on_warnings,
            log_file=log_file
        )

        # Set up custom parsers (LaTeX parser for PDF builds)
        custom_parsers = []
        if rendering_pdf:
            custom_parsers.append(create_latex_parser())

        # Run render command with monitoring
        build_type = f"{config['description']} ({format_override or 'all formats'})"
        exit_code = monitor.run_build(cmd, build_type=build_type, custom_parsers=custom_parsers)

        if exit_code != 0:
            print(f"[ERROR] {config['description']} render failed with exit code {exit_code}", file=sys.stderr)
            # Don't return yet - still need to copy outputs and clean up
        else:
            print(f"[OK] {config['description']} render complete!")

        # 4. Run post-validation for HTML builds
        if not rendering_pdf and exit_code == 0:
            print("=" * 80)
            print("VALIDATION: POST-RENDER (HTML)")
            print("=" * 80)
            # Determine output directory based on config
            output_dir = f"_site/{config_name}" if config_name != "book" else "_site"
            validation_exit = run_post_validation(output_dir=output_dir)
            if validation_exit != 0:
                print("[WARNING] Post-validation found issues", file=sys.stderr)
                # Don't fail the build, just warn
            print()

        # If we used temp folder, copy outputs back
        if build_temp:
            print("[*] Copying outputs from temp to original location...")

            # Copy PDFs to both project root and output directory
            for pdf_file in build_temp.glob("*.pdf"):
                # Report file size
                file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
                print(f"[*] {pdf_file.name}: {file_size_mb:.2f} MB")

                # Copy to project root (for convenience)
                dest_root = project_root / pdf_file.name
                shutil.copy2(pdf_file, dest_root)
                print(f"[OK] Copied {pdf_file.name} to project root")

                # Also copy to output directory (for deployment)
                # Determine output directory based on config
                if config_name == "book":
                    output_dir = project_root / "_book" / "warondisease"
                else:
                    output_dir = project_root / "_site" / config_name

                # Ensure output directory exists before copying
                output_dir.mkdir(parents=True, exist_ok=True)
                dest_output = output_dir / pdf_file.name
                shutil.copy2(pdf_file, dest_output)
                print(f"[OK] Copied {pdf_file.name} to {output_dir.relative_to(project_root)}")

                # Run PDF validation for Python code leakage
                print("=" * 80)
                print("VALIDATION: PDF PYTHON CODE CHECK")
                print("=" * 80)
                found_issues, issues = validate_pdf_for_python_code(str(dest_output))
                if found_issues:
                    print("[ERROR] PDF validation failed: Python code detected in PDF!", file=sys.stderr)
                    for issue in issues[:5]:  # Show first 5 issues
                        # Handle Unicode encoding issues
                        safe_issue = issue.encode("ascii", errors="replace").decode("ascii", errors="replace")
                        print(f"  {safe_issue}", file=sys.stderr)
                    if len(issues) > 5:
                        print(f"  ... and {len(issues) - 5} more issues", file=sys.stderr)
                    exit_code = 1
                else:
                    print("[OK] PDF validation passed: No Python code leakage detected")

            # Copy EPUBs and report file size
            for epub_file in build_temp.glob("*.epub"):
                file_size_mb = epub_file.stat().st_size / (1024 * 1024)
                print(f"[*] {epub_file.name}: {file_size_mb:.2f} MB")

                # Copy to project root
                dest_root = project_root / epub_file.name
                shutil.copy2(epub_file, dest_root)
                print(f"[OK] Copied {epub_file.name} to project root")

                # Copy to output directory
                if config_name == "book":
                    output_dir = project_root / "_book" / "warondisease"
                else:
                    output_dir = project_root / "_site" / config_name
                output_dir.mkdir(parents=True, exist_ok=True)
                dest_output = output_dir / epub_file.name
                shutil.copy2(epub_file, dest_output)
                print(f"[OK] Copied {epub_file.name} to {output_dir.relative_to(project_root)}")

            # Copy HTML output directory if it exists
            site_dir = build_temp / "_site"
            if site_dir.exists():
                dest_site = project_root / "_site"
                if dest_site.exists():
                    shutil.rmtree(dest_site)
                shutil.copytree(site_dir, dest_site)
                print(f"[OK] Copied _site/ directory")

            # Copy _book directory if it exists (for book config)
            book_dir = build_temp / "_book"
            if book_dir.exists():
                dest_book = project_root / "_book"
                if dest_book.exists():
                    shutil.rmtree(dest_book)
                shutil.copytree(book_dir, dest_book)
                print(f"[OK] Copied _book/ directory")

        # 5. Run verification tests if requested (test config only)
        if verify and config_name == "test" and exit_code == 0:
            print("=" * 80)
            print("VERIFICATION: PDF LINK TESTS")
            print("=" * 80)
            verify_script = project_root / "scripts" / "test" / "verify-pdf-links.py"
            if verify_script.exists() and build_temp:
                os.chdir(project_root)
                verify_result = subprocess.run(
                    [sys.executable, str(verify_script), str(build_temp)],
                    check=False
                )
                if verify_result.returncode != 0:
                    print("[ERROR] Verification tests failed", file=sys.stderr)
                    exit_code = verify_result.returncode
                print()
            else:
                print(f"[WARNING] Verification script not found or no temp folder", file=sys.stderr)
                print()

    except subprocess.CalledProcessError as e:
        # This catches errors from pre-validation, verification, etc. (not main render)
        print(f"[ERROR] Subprocess failed with exit code {e.returncode}", file=sys.stderr)
        exit_code = e.returncode
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        print("        Make sure Quarto is installed and in your PATH", file=sys.stderr)
        exit_code = 1
    except KeyboardInterrupt:
        print("\n[*] Build interrupted by user", file=sys.stderr)
        exit_code = 130
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        exit_code = 1
    finally:
        # Change back to original directory
        os.chdir(original_cwd)

        # Clean up temp directory
        if build_temp and build_temp.exists():
            print("=" * 80)
            print("CLEANING UP TEMP DIRECTORY")
            print("=" * 80)
            try:
                shutil.rmtree(build_temp)
                print(f"[OK] Removed temp directory: {build_temp}")
            except Exception as e:
                print(f"[WARNING] Failed to remove temp directory: {e}", file=sys.stderr)

        # Close BuildMonitor log file if it exists
        if monitor and hasattr(monitor, 'log_handle') and monitor.log_handle:
            try:
                monitor.log_handle.close()
            except Exception:
                pass

    return exit_code


def main():
    parser = argparse.ArgumentParser(
        description="Render Quarto configuration with build monitoring, timeout detection, and validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "config",
        choices=list(CONFIGS.keys()),
        help=f"Configuration to render: {', '.join(CONFIGS.keys())}"
    )
    parser.add_argument(
        "--to",
        type=str,
        choices=["pdf", "html", "epub", "all"],
        default=None,
        help="Format to render (default: all formats in config)"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run verification tests after rendering (test config only)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Seconds with no output before killing build (default: 900 = 15min)"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Log file path (default: build-{config}.log)"
    )
    parser.add_argument(
        "--no-fail-on-warnings",
        action="store_true",
        help="Do not fail build on warnings (warnings fail by default)"
    )
    parser.add_argument(
        "--kill-existing",
        action="store_true",
        help="Kill existing Quarto/LaTeX processes before starting"
    )
    parser.add_argument(
        "quarto_args",
        nargs="*",
        help="Additional arguments to pass to quarto render"
    )

    args = parser.parse_args()

    format_override = None if args.to == "all" else args.to

    exit_code = render_quarto(
        config_name=args.config,
        format_override=format_override,
        verify=args.verify,
        quarto_args=args.quarto_args,
        timeout=args.timeout,
        log_file=args.log_file,
        fail_on_warnings=not args.no_fail_on_warnings,
        kill_existing=args.kill_existing
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
