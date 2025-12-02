#!/usr/bin/env python3
"""
Netlify Deployment Utilities
============================

Shared utilities for deploying sites to Netlify.
"""

import subprocess
import sys
from pathlib import Path

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, continue without it


def check_netlify_cli():
    """Check if Netlify CLI is installed and available.

    Returns:
        str or None: The working Netlify command, or None if not found
    """
    # Try different command variations for Windows
    commands = ["netlify", "netlify.cmd", "netlify.ps1"]

    for cmd in commands:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
                check=True,
                shell=(sys.platform == "win32"),
            )
            print(f"[OK] Netlify CLI found: {result.stdout.strip()}")
            return cmd  # Return the working command
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    print("[ERROR] Netlify CLI not found", file=sys.stderr)
    print("        Install it with: npm install -g netlify-cli", file=sys.stderr)
    return None


def verify_output_directory(output_dir: str):
    """Verify that the output directory exists and contains HTML files.

    Args:
        output_dir: Path to the output directory

    Returns:
        bool: True if directory exists and contains HTML files
    """
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"[ERROR] Output directory does not exist: {output_dir}", file=sys.stderr)
        return False

    if not output_path.is_dir():
        print(f"[ERROR] Output path is not a directory: {output_dir}", file=sys.stderr)
        return False

    # Check for at least one HTML file (recursively)
    html_files = list(output_path.rglob("*.html"))
    if not html_files:
        print(f"[WARN] No HTML files found in {output_dir}", file=sys.stderr)
        print("       The build may have failed or output may be in a subdirectory", file=sys.stderr)
        return False

    print(f"[OK] Output directory verified: {len(html_files)} HTML file(s) found")
    return True


def deploy_to_netlify(output_dir: str, site_id: str, netlify_cmd: str, production: bool = True):
    """Deploy the built site to Netlify.

    Args:
        output_dir: Path to the directory containing the built site
        site_id: Netlify site ID
        netlify_cmd: The Netlify CLI command to use
        production: If True, deploy to production; if False, deploy as draft

    Returns:
        bool: True if deployment succeeded, False otherwise
    """
    deploy_type = "production" if production else "draft"
    print(f"[*] Deploying to Netlify ({deploy_type})...")

    # Convert Windows path separators if needed
    deploy_dir = str(Path(output_dir).absolute())

    cmd = [
        netlify_cmd,
        "deploy",
        "--dir", deploy_dir,
        "--site", site_id,
        "--no-build",  # Skip build since we already built locally
    ]

    if production:
        cmd.append("--prod")

    try:
        subprocess.run(
            cmd,
            check=True,
            text=True,
            shell=(sys.platform == "win32"),
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


