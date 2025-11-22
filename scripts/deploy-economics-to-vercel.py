#!/usr/bin/env python3
"""
Deploy Economics Website to Vercel
==================================

Builds the economics website and deploys it to Vercel.

Usage:
    python deploy-economics-to-vercel.py                    # Build and deploy to production
    python deploy-economics-to-vercel.py --preview          # Deploy as preview
    python deploy-economics-to-vercel.py --help              # Show all options
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from vercel_deploy import check_vercel_cli, deploy_to_vercel, verify_output_directory

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, continue without it


DEFAULT_OUTPUT_DIR = "_site/economics"
DEFAULT_PROJECT_NAME = "dih-models"


def build_economics(output_dir: str):
    """Build the economics website using render-economics-website.py."""
    print(f"[*] Building economics website to {output_dir}...")
    
    script_path = Path(__file__).parent / "render-economics-website.py"
    if not script_path.exists():
        print(f"[ERROR] Build script not found: {script_path}", file=sys.stderr)
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), "--output-dir", output_dir],
            check=True,
        )
        print("[OK] Economics build complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed with exit code {e.returncode}", file=sys.stderr)
        return False
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Build and deploy economics website to Vercel",
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
        "--project-name",
        type=str,
        default=DEFAULT_PROJECT_NAME,
        help=f"Vercel project name (default: {DEFAULT_PROJECT_NAME})",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Deploy as preview instead of production",
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
    print("Deploy Economics Website to Vercel")
    print("=" * 60)
    print()
    
    # Check prerequisites
    vercel_cmd = check_vercel_cli()
    if not vercel_cmd:
        sys.exit(1)
    
    # Build the economics site (unless skipped)
    if not args.skip_build:
        if not build_economics(args.output_dir):
            sys.exit(1)
        
        if not verify_output_directory(args.output_dir):
            sys.exit(1)
    else:
        print("[*] Skipping build (--skip-build flag set)")
        if not verify_output_directory(args.output_dir):
            print("[WARN] Output directory verification failed, but continuing...", file=sys.stderr)
    
    # Deploy to Vercel
    if not deploy_to_vercel(args.output_dir, vercel_cmd, production=not args.preview, project_name=args.project_name):
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("[OK] All done! Economics website deployed to Vercel.")
    print("=" * 60)


if __name__ == "__main__":
    main()


