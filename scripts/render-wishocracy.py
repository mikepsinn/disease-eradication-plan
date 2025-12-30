#!/usr/bin/env python3
"""
Render the Wishocracy paper as a standalone website.

This script:
1. Copies wishocracy-paper.qmd to index.qmd (creates landing page)
2. Copies _quarto-wishocracy.yml to _quarto.yml
3. Renders the site using Quarto
4. Optionally copies output to the wishocracy submodule for deployment
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from quarto_pre_build import prepare_wishocracy


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def main():
    project_root = get_project_root()
    os.chdir(project_root)

    print("=" * 80)
    print("WISHOCRACY PAPER RENDERER")
    print("=" * 80)

    # Step 1: Prepare paper (copy to index.qmd) and config
    if not prepare_wishocracy():
        print("[ERROR] Failed to prepare wishocracy paper")
        sys.exit(1)

    # Step 2: Render with Quarto
    print("=" * 80)
    print("Starting Wishocracy paper render: quarto render")
    print("Timeout (no output): 300s")
    print("Log file: build-wishocracy.log")
    print("-" * 80)

    try:
        result = subprocess.run(
            ["quarto", "render"],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )

        # Write log
        with open("build-wishocracy.log", "w", encoding="utf-8") as f:
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
        print(f"Output directory: _site/wishocracy")
        print("\nBuild completed successfully!")
        print("=" * 80)

        # Step 3: Optionally copy to wishocracy submodule
        wishocracy_repo = project_root.parent / "wishocracy" / "public" / "paper"

        if wishocracy_repo.parent.exists():
            print(f"\n[*] Copying output to wishocracy submodule: {wishocracy_repo}")

            # Create paper directory if it doesn't exist
            wishocracy_repo.mkdir(parents=True, exist_ok=True)

            # Copy the rendered site
            site_dir = project_root / "_site" / "wishocracy"
            if site_dir.exists():
                # Remove old content
                if wishocracy_repo.exists():
                    shutil.rmtree(wishocracy_repo)

                # Copy new content
                shutil.copytree(site_dir, wishocracy_repo)
                print(f"[OK] Copied to {wishocracy_repo}")
                print("\nNext steps:")
                print("  cd ../wishocracy")
                print("  git add public/paper")
                print("  git commit -m 'update: wishocracy paper'")
                print("  git push")
            else:
                print(f"[WARNING] Site directory not found: {site_dir}")
        else:
            print(f"\n[INFO] Wishocracy submodule not found at {wishocracy_repo.parent}")
            print("[INFO] Skipping copy to submodule")

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
