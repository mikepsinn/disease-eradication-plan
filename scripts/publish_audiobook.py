#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Publish Pipeline

Single script that runs the full audiobook pipeline:
  1. Generate narration text from QMD chapters (LLM rewrite)
  2. Generate podcast episode images (skips existing)
  3. Generate audio (TTS), combine, MP3s, RSS, alignment, subtitles
  4. Sync assets to Cloudflare R2

Passes all arguments through to the underlying scripts, so you can use
--chapter, --start, --end, --force, --list, etc.

Usage:
    python scripts/publish_audiobook.py                         # Full pipeline
    python scripts/publish_audiobook.py --chapter 5             # Single chapter
    python scripts/publish_audiobook.py --force                 # Regenerate everything
    python scripts/publish_audiobook.py --no-sync               # Skip R2 upload
    python scripts/publish_audiobook.py --list                  # List chapters and exit
    python scripts/publish_audiobook.py --dry-run               # Text dry-run only
"""
import sys
import subprocess
import argparse
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent


def run_step(label: str, script: str, args: list[str]) -> bool:
    """Run a pipeline step, returning True on success."""
    print(f"\n{'=' * 70}")
    print(f"  STEP: {label}")
    print(f"{'=' * 70}\n")

    cmd = [sys.executable, "-u", str(SCRIPTS_DIR / script)] + args
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))

    if result.returncode != 0:
        print(f"\n[FAILED] {label} (exit code {result.returncode})")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Full audiobook publish pipeline: text -> audio -> R2 sync"
    )
    parser.add_argument(
        "--config", "-cfg",
        default="_quarto-manual-paperback.yml",
        help="Quarto config YAML (default: _quarto-manual-paperback.yml)"
    )
    parser.add_argument("--chapter", "-c", type=int, help="Process only specific chapter")
    parser.add_argument("--start", type=int, help="Start from chapter number (inclusive)")
    parser.add_argument("--end", type=int, help="End at chapter number (inclusive)")
    parser.add_argument("--force", "-f", action="store_true", help="Regenerate even if cached")
    parser.add_argument("--list", "-l", action="store_true", help="List chapters and exit")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Text dry-run (skip LLM)")
    parser.add_argument("--no-sync", action="store_true", help="Skip R2 sync step")
    args = parser.parse_args()

    # Build shared args that get passed to text + audio scripts
    shared = ["--config", args.config]
    if args.chapter:
        shared += ["--chapter", str(args.chapter)]
    if args.start:
        shared += ["--start", str(args.start)]
    if args.end:
        shared += ["--end", str(args.end)]

    # --- List mode: just list from audio script and exit ---
    if args.list:
        run_step("List chapters", "generate_audiobook.py", shared + ["--list"])
        return

    # --- Step 1: Generate narration text ---
    text_args = list(shared)
    if args.force:
        text_args.append("--force")
    if args.dry_run:
        text_args.append("--dry-run")

    if not run_step("Generate narration text", "generate_audiobook_text.py", text_args):
        sys.exit(1)

    if args.dry_run:
        print("\n[DONE] Dry run complete (text only, no audio generated).")
        return

    # --- Step 2: Generate podcast episode images ---
    img_args = list(shared)
    if args.force:
        img_args.append("--force")
    img_args.append("--podcast-only")

    if not run_step("Generate podcast images", "generate_podcast_images.py", img_args):
        sys.exit(1)

    # --- Step 3: Generate audio ---
    audio_args = list(shared)
    if args.force:
        audio_args.append("--force")

    if not run_step("Generate audio + MP3s + RSS", "generate_audiobook.py", audio_args):
        sys.exit(1)

    # --- Step 4: Sync to R2 ---
    if args.no_sync:
        print("\n[DONE] Audio generation complete (--no-sync: skipped R2 upload).")
        return

    if not run_step("Sync to Cloudflare R2", "sync_r2.py", []):
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print("  PUBLISH COMPLETE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
