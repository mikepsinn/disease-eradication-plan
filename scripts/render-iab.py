#!/usr/bin/env python3
"""
Render the Incentive Alignment Bonds paper as a standalone website.

This script:
1. Copies incentive-alignment-bonds-paper.qmd to index.qmd (creates landing page)
2. Copies _quarto-iab.yml to _quarto.yml
3. Renders the site using Quarto
4. Output goes to _site/iab/
"""

import os
import subprocess
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from quarto_pre_build import prepare_iab


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def main():
    project_root = get_project_root()
    os.chdir(project_root)

    print("=" * 80)
    print("INCENTIVE ALIGNMENT BONDS PAPER RENDERER")
    print("=" * 80)

    # Step 1: Prepare paper (copy to index.qmd) and config
    if not prepare_iab():
        print("[ERROR] Failed to prepare IAB paper")
        sys.exit(1)

    # Step 2: Render with Quarto
    print("=" * 80)
    print("Starting IAB paper render: quarto render")
    print("Timeout (no output): 300s")
    print("Log file: build-iab.log")
    print("-" * 80)

    try:
        result = subprocess.run(
            ["quarto", "render"],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )

        # Write log
        with open("build-iab.log", "w", encoding="utf-8") as f:
            f.write(result.stdout)
            f.write(result.stderr)

        # Print output
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode != 0:
            print(f"\n[ERROR] Quarto render failed with exit code {result.returncode}")
            sys.exit(result.returncode)

        print("\n" + "=" * 80)
        print("BUILD SUMMARY")
        print("=" * 80)
        print(f"Exit code: {result.returncode}")
        print(f"Output directory: _site/iab")
        print("\nBuild completed successfully!")
        print("=" * 80)

        print(f"\n[INFO] Rendered IAB paper available at _site/iab/")
        print("[INFO] Deploy to https://iab.warondisease.org")

    except subprocess.TimeoutExpired:
        print("[ERROR] Render timed out after 600 seconds")
        sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] Quarto not found. Please install Quarto: https://quarto.org/docs/get-started/")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
