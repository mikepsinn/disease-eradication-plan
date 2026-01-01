#!/usr/bin/env python3
"""
Render Quarto Config
====================

Unified script to render any Quarto configuration. Automatically handles:
- HTML rendering with post-processing link rewriting
- PDF rendering with pre-processing link rewriting in temp folder
- Mixed formats (renders both HTML and PDF as configured)

Usage:
    python render-quarto.py economics                # Render economics (all formats in config)
    python render-quarto.py wishocracy               # Render wishocracy (all formats in config)
    python render-quarto.py iab                      # Render IAB (all formats in config)
    python render-quarto.py test --verify            # Render test config with verification
    python render-quarto.py economics --to pdf       # Render only PDF format
    python render-quarto.py economics --to html      # Render only HTML format
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

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
    ensure_jupyter_kernel,
    run_pre_validation,
    run_post_validation
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
    quarto_args: list = None
) -> int:
    """
    Render Quarto configuration.

    Args:
        config_name: Name of configuration (economics, wishocracy, iab, test, book)
        format_override: Override format (pdf, html, or None for all formats in config)
        verify: Run verification tests after rendering (test config only)
        quarto_args: Additional arguments to pass to quarto render

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

    exit_code = 0
    build_temp = None

    try:
        # Determine if we're rendering PDF
        rendering_pdf = format_override == "pdf" or format_override is None

        # Change to project root for setup
        os.chdir(project_root)

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

        # Run render command
        subprocess.run(cmd, check=True)
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

            # Debug: List all PDFs found in temp directory
            pdf_files = list(build_temp.glob("*.pdf"))
            print(f"[DEBUG] Found {len(pdf_files)} PDF file(s) in temp directory: {[p.name for p in pdf_files]}")

            # Copy PDFs to both project root and output directory
            for pdf_file in pdf_files:
                print(f"[DEBUG] Processing PDF: {pdf_file.name} (size: {pdf_file.stat().st_size} bytes)")

                # Copy to project root (for convenience)
                dest_root = project_root / pdf_file.name
                shutil.copy2(pdf_file, dest_root)
                print(f"[OK] Copied {pdf_file.name} to project root: {dest_root}")

                # Also copy to output directory (for deployment)
                # Determine output directory based on config
                if config_name == "book":
                    output_dir = project_root / "_book" / "warondisease"
                else:
                    output_dir = project_root / "_site" / config_name

                print(f"[DEBUG] Target deployment directory: {output_dir}")

                # Ensure output directory exists before copying
                output_dir.mkdir(parents=True, exist_ok=True)
                dest_output = output_dir / pdf_file.name
                shutil.copy2(pdf_file, dest_output)
                print(f"[OK] Copied {pdf_file.name} to deployment directory: {dest_output}")
                print(f"[DEBUG] Deployment file size: {dest_output.stat().st_size} bytes")

            if not pdf_files:
                print("[WARNING] No PDF files found in temp directory to copy!")

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
        print(f"[ERROR] Render failed with exit code {e.returncode}", file=sys.stderr)
        exit_code = e.returncode
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        print("        Make sure Quarto is installed and in your PATH", file=sys.stderr)
        exit_code = 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        exit_code = 1
    finally:
        # Change back to original directory
        os.chdir(original_cwd)

        # Validate PDF exists in deployment directory before cleanup
        if build_temp and rendering_pdf and exit_code == 0:
            print("=" * 80)
            print("VALIDATION: PDF DEPLOYMENT CHECK")
            print("=" * 80)
            print(f"[DEBUG] build_temp={build_temp}")
            print(f"[DEBUG] rendering_pdf={rendering_pdf}")
            print(f"[DEBUG] exit_code={exit_code}")
            print(f"[DEBUG] config_name={config_name}")

            # Read PDF filename from Quarto config
            import yaml

            quarto_config_path = project_root / "_quarto.yml"
            print(f"[DEBUG] Looking for Quarto config at: {quarto_config_path}")
            print(f"[DEBUG] Config exists: {quarto_config_path.exists()}")

            if quarto_config_path.exists():
                try:
                    with open(quarto_config_path, 'r', encoding='utf-8') as f:
                        quarto_config = yaml.safe_load(f)

                    print(f"[DEBUG] Config has 'format' key: {'format' in quarto_config}")
                    if 'format' in quarto_config:
                        print(f"[DEBUG] Config has 'pdf' in format: {'pdf' in quarto_config['format']}")

                    # Get PDF output filename from config
                    expected_pdf = None
                    if 'format' in quarto_config and 'pdf' in quarto_config['format']:
                        pdf_config = quarto_config['format']['pdf']
                        if 'output-file' in pdf_config:
                            expected_pdf = pdf_config['output-file']
                            print(f"[DEBUG] Expected PDF filename from config: {expected_pdf}")

                    if expected_pdf:
                        # Determine deployment directory from config
                        if 'project' in quarto_config and 'output-dir' in quarto_config['project']:
                            output_dir_str = quarto_config['project']['output-dir']
                            deployment_dir = project_root / output_dir_str
                            print(f"[DEBUG] Using output-dir from config: {output_dir_str}")
                        else:
                            # Fallback to default locations
                            if config_name == "book":
                                deployment_dir = project_root / "_book" / "warondisease"
                            else:
                                deployment_dir = project_root / "_site" / config_name
                            print(f"[DEBUG] Using fallback deployment directory")

                        print(f"[DEBUG] Deployment directory: {deployment_dir}")
                        print(f"[DEBUG] Deployment directory exists: {deployment_dir.exists()}")

                        expected_path = deployment_dir / expected_pdf
                        print(f"[DEBUG] Checking for PDF at: {expected_path}")
                        print(f"[DEBUG] PDF exists: {expected_path.exists()}")

                        if expected_path.exists():
                            print(f"[DEBUG] PDF file size: {expected_path.stat().st_size} bytes")

                        # List all files in deployment directory for debugging
                        if deployment_dir.exists():
                            all_files = list(deployment_dir.glob("*"))
                            print(f"[DEBUG] Files in deployment directory ({len(all_files)}): {[f.name for f in all_files[:20]]}")  # First 20 files

                        if not expected_path.exists():
                            error_msg = (
                                f"[FATAL] PDF not found in deployment directory!\n"
                                f"        Expected: {expected_path}\n"
                                f"        Config: {config_name} ({quarto_config_path.name})\n"
                                f"        PDF filename from config: {expected_pdf}\n"
                                f"        This PDF will NOT be deployed to production.\n"
                                f"        Aborting to prevent incomplete deployment."
                            )
                            print(error_msg, file=sys.stderr)
                            raise FileNotFoundError(error_msg)
                        else:
                            print(f"[OK] PDF verified in deployment directory: {expected_path.relative_to(project_root)}")
                    else:
                        print(f"[INFO] No PDF output-file specified in {quarto_config_path.name}")

                except Exception as e:
                    print(f"[WARNING] Failed to validate PDF from config: {e}", file=sys.stderr)
            else:
                print(f"[WARNING] Quarto config not found: {quarto_config_path}", file=sys.stderr)

            print()

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

    return exit_code


def main():
    parser = argparse.ArgumentParser(
        description="Render Quarto configuration (auto-handles PDF preprocessing)",
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
        choices=["pdf", "html", "all"],
        default=None,
        help="Format to render (default: all formats in config)"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run verification tests after rendering (test config only)"
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
        quarto_args=args.quarto_args
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
