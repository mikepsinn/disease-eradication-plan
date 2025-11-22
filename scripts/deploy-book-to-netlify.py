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
import shutil
import subprocess
import sys
from pathlib import Path


# Netlify site ID for the main book site (warondisease-org)
NETLIFY_SITE_ID = "4e36b0d6-9b80-49e2-bf16-eb4d2f79f062"
DEFAULT_OUTPUT_DIR = "_book/warondisease"


def check_netlify_cli():
    """Check if Netlify CLI is installed and available."""
    try:
        result = subprocess.run(
            ["netlify", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"[OK] Netlify CLI found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] Netlify CLI not found", file=sys.stderr)
        print("        Install it with: npm install -g netlify-cli", file=sys.stderr)
        return False


def build_book(output_dir: str):
    """Build the book website using render-book-website.py."""
    print(f"[*] Building book website to {output_dir}...")
    
    script_path = Path(__file__).parent / "render-book-website.py"
    if not script_path.exists():
        print(f"[ERROR] Build script not found: {script_path}", file=sys.stderr)
        return False
    
    try:
        result = subprocess.run(
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


def verify_output_directory(output_dir: str):
    """Verify that the output directory exists and contains files."""
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"[ERROR] Output directory does not exist: {output_dir}", file=sys.stderr)
        return False
    
    if not output_path.is_dir():
        print(f"[ERROR] Output path is not a directory: {output_dir}", file=sys.stderr)
        return False
    
    # Check for at least one HTML file
    html_files = list(output_path.glob("*.html"))
    if not html_files:
        print(f"[WARN] No HTML files found in {output_dir}", file=sys.stderr)
        print("       The build may have failed or output may be in a subdirectory", file=sys.stderr)
        return False
    
    print(f"[OK] Output directory verified: {len(html_files)} HTML file(s) found")
    return True


def deploy_to_netlify(output_dir: str, site_id: str, production: bool = True):
    """Deploy the built site to Netlify."""
    deploy_type = "production" if production else "draft"
    print(f"[*] Deploying to Netlify ({deploy_type})...")
    
    # Convert Windows path separators if needed
    deploy_dir = str(Path(output_dir).absolute())
    
    cmd = [
        "netlify",
        "deploy",
        "--dir", deploy_dir,
        "--site", site_id,
        "--no-build",  # Skip build since we already built locally
    ]
    
    if production:
        cmd.append("--prod")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
        )
        print(f"[OK] Deployment to {deploy_type} complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Deployment failed with exit code {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"        stdout: {e.stdout}", file=sys.stderr)
        if e.stderr:
            print(f"        stderr: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("[ERROR] Netlify CLI not found", file=sys.stderr)
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
    if not check_netlify_cli():
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
    if not deploy_to_netlify(args.output_dir, args.site_id, production=not args.draft):
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("[OK] All done! Book deployed to Netlify.")
    print("=" * 60)


if __name__ == "__main__":
    main()

