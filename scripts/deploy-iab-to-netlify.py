#!/usr/bin/env python3
"""
Deploy IAB Paper to Netlify
============================

Builds the Incentive Alignment Bonds paper website and deploys it to Netlify.

Usage:
    python deploy-iab-to-netlify.py                    # Build and deploy to production
    python deploy-iab-to-netlify.py --draft            # Deploy as draft
    python deploy-iab-to-netlify.py --help             # Show all options
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


# Netlify site ID for the IAB paper site (iab.warondisease.org)
# Can be overridden via NETLIFY_IAB_SITE_ID environment variable
NETLIFY_SITE_ID = os.getenv("NETLIFY_IAB_SITE_ID", "")
DEFAULT_OUTPUT_DIR = "_site/iab"


def build_iab(output_dir: str):
    """Build the IAB paper website using render-iab.py."""
    print(f"[*] Building IAB paper website to {output_dir}...")

    script_path = Path(__file__).parent / "render-iab.py"
    if not script_path.exists():
        print(f"[ERROR] Build script not found: {script_path}", file=sys.stderr)
        return False

    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
        )
        print("[OK] IAB build complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed with exit code {e.returncode}", file=sys.stderr)
        return False
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Build and deploy IAB paper to Netlify",
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
        help=f"Netlify site ID (default: from NETLIFY_IAB_SITE_ID env var)",
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

    if not args.site_id:
        print("[ERROR] Netlify site ID not provided", file=sys.stderr)
        print("        Set NETLIFY_IAB_SITE_ID environment variable or use --site-id", file=sys.stderr)
        sys.exit(1)

    # Get project root (parent of scripts directory) and change to it
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)

    print("=" * 60)
    print("Deploy IAB Paper to Netlify")
    print("=" * 60)
    print()

    # Check prerequisites
    netlify_cmd = check_netlify_cli()
    if not netlify_cmd:
        sys.exit(1)

    # Build the IAB site (unless skipped)
    if not args.skip_build:
        if not build_iab(args.output_dir):
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
    print("[OK] All done! IAB paper deployed to Netlify.")
    print("=" * 60)


if __name__ == "__main__":
    main()
