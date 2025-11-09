#!/usr/bin/env python3
"""
Unified PDF render script for Quarto PDF generation
- Runs pre-validation automatically
- Logs to both console and file
- Detects warnings and errors in real-time
- Times out if stuck on a step too long
- Fails fast on critical errors
- Provides progress updates

Usage:
    python scripts/render_pdf.py                    # Run with all defaults
    python scripts/render_pdf.py --skip-validation  # Skip pre-validation
    python scripts/render_pdf.py --timeout 1800     # Custom timeout

All parameters are optional - script works with defaults if none provided.
"""

import sys
import os

# Add scripts/lib to path so we can import render_utils
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, 'lib')
sys.path.insert(0, lib_dir)

from render_utils import BuildMonitor, kill_existing_quarto_processes, run_pre_validation, create_latex_parser


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Unified PDF render script with validation, logging, and monitoring'
    )
    parser.add_argument('--timeout', type=int, default=900,
                        help='Seconds with no output before killing build (default: 900 = 15min for PDF builds)')
    parser.add_argument('--no-fail-on-warnings', action='store_true',
                        help='Do not fail build on warnings (warnings fail by default)')
    parser.add_argument('--skip-validation', action='store_true',
                        help='Skip pre-render validation')
    parser.add_argument('--log-file', type=str, default='build-pdf.log',
                        help='Log file path (default: build-pdf.log)')
    parser.add_argument('--command', type=str, default='quarto render . --to pdf',
                        help='Build command to run (default: quarto render . --to pdf)')
    parser.add_argument('--kill-existing', action='store_true',
                        help='Kill all existing Quarto/LaTeX processes before starting build')

    args = parser.parse_args()

    # Force output flush to ensure GitHub Actions sees output immediately
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
    
    # Log script start immediately
    from datetime import datetime
    print("=" * 80, flush=True)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting PDF render script", flush=True)
    print("=" * 80, flush=True)

    # Kill existing Quarto processes if requested
    if args.kill_existing:
        print("=" * 80, flush=True)
        print("KILLING EXISTING QUARTO/LaTeX PROCESSES", flush=True)
        print("=" * 80, flush=True)
        kill_existing_quarto_processes(include_latex=True)
        print("=" * 80, flush=True)

    # Run pre-validation unless skipped
    if not args.skip_validation:
        validation_exit_code = run_pre_validation()
        if validation_exit_code != 0:
            sys.exit(validation_exit_code)

    # Parse command into list
    command = args.command.split()

    # Create LaTeX parser for PDF builds
    latex_parser = create_latex_parser()

    # Create monitor and run build
    monitor = BuildMonitor(
        timeout_seconds=args.timeout,
        fail_on_warnings=not args.no_fail_on_warnings,
        log_file=args.log_file
    )

    exit_code = monitor.run_build(command, build_type="PDF render", custom_parsers=[latex_parser])
    
    # Run post-render PDF validation if build succeeded
    if exit_code == 0:
        from render_utils import validate_pdf_for_python_code
        from pathlib import Path
        
        # Find the generated PDF file
        output_dir = Path("_book/warondisease")
        pdf_files = list(output_dir.glob("*.pdf"))
        
        if pdf_files:
            pdf_path = str(pdf_files[0])  # Use first PDF found
            print("=" * 80, flush=True)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Running PDF validation for Python code leakage", flush=True)
            print("=" * 80, flush=True)
            
            found_issues, issues = validate_pdf_for_python_code(pdf_path, search_string='print(f')
            
            if found_issues:
                print("\n" + "=" * 80, flush=True)
                print("[ERROR] PDF VALIDATION FAILED: Python code detected in PDF!", flush=True)
                print("=" * 80, flush=True)
                for issue in issues:
                    # Handle Unicode encoding issues - replace problematic characters
                    safe_issue = issue.encode('ascii', errors='replace').decode('ascii', errors='replace')
                    print(f"\n{safe_issue}\n", flush=True)
                print("=" * 80, flush=True)
                print("Please fix the source files to remove Python code from PDF output.", flush=True)
                print("=" * 80, flush=True)
                sys.exit(1)
            else:
                print("[OK] PDF validation passed: No Python code leakage detected.", flush=True)
        else:
            print(f"⚠️  Warning: No PDF file found in {output_dir} for validation", flush=True)
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
