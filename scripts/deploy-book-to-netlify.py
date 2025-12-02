#!/usr/bin/env python3
"""
Deploy Book to Netlify
======================

Builds the book website and deploys it to Netlify.

Usage:
    python deploy-book-to-netlify.py                    # Build and deploy to production
    python deploy-book-to-netlify.py --draft            # Deploy as draft
    python deploy-book-to-netlify.py --help             # Show all options
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from netlify_deploy import check_netlify_cli, deploy_to_netlify, verify_output_directory

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, continue without it


# Netlify site ID for the main book site (warondisease-org)
# Can be overridden via NETLIFY_MAIN_SITE_ID environment variable
NETLIFY_SITE_ID = os.getenv("NETLIFY_MAIN_SITE_ID", "4e36b0d6-9b80-49e2-bf16-eb4d2f79f062")
DEFAULT_OUTPUT_DIR = "_book/warondisease"


def build_book(output_dir: str):
    """Build the book website using render-book-website.py."""
    print(f"[*] Building book website to {output_dir}...")

    script_path = Path(__file__).parent / "render-book-website.py"
    if not script_path.exists():
        print(f"[ERROR] Build script not found: {script_path}", file=sys.stderr)
        return False

    try:
        subprocess.run(
            [sys.executable, str(script_path), "--output-dir", output_dir],
            check=True,
        )
        print("[OK] Book build complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed with exit code {e.returncode}", file=sys.stderr)
        return False
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        return False




def main():
    parser = argparse.ArgumentParser(
        description="Build and deploy book website to Netlify",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for built site (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--site-id",
        type=str,
        default=NETLIFY_SITE_ID,
        help=f"Netlify site ID (default: {NETLIFY_SITE_ID})",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Deploy as draft instead of production",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip building and only deploy (assumes site is already built)",
    )

    args = parser.parse_args()

    # Get project root (parent of scripts directory) and change to it
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    print("=" * 60)
    print("Deploy Book to Netlify")
    print("=" * 60)
    print()

    # Check prerequisites
    netlify_cmd = check_netlify_cli()
    if not netlify_cmd:
        sys.exit(1)

    # Build the book (unless skipped)
    if not args.skip_build:
        if not build_book(args.output_dir):
            sys.exit(1)

        if not verify_output_directory(args.output_dir):
            sys.exit(1)
    else:
        print("[*] Skipping build (--skip-build flag set)")
        if not verify_output_directory(args.output_dir):
            print("[WARN] Output directory verification failed, but continuing...", file=sys.stderr)

    # Deploy to Netlify
    if not deploy_to_netlify(args.output_dir, args.site_id, netlify_cmd, production=not args.draft):
        sys.exit(1)

    print()
    print("=" * 60)
    print("[OK] All done! Book deployed to Netlify.")
    print("=" * 60)


if __name__ == "__main__":
    main()

