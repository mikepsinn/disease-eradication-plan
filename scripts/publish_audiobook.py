#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Publish Pipeline

Single script that runs the full audiobook pipeline:
  1. Generate narration text from QMD chapters (LLM rewrite)
  2. Generate audio (TTS), combine, MP3s, RSS, alignment, subtitles
  3. Scene segmentation (LLM visual scenes with prompts)
  4. Video generation (keyframes + Veo animation + assembly)
  5. Sync assets to Cloudflare R2

Passes all arguments through to the underlying scripts, so you can use
--chapter, --start, --end, --force, --list, etc.

Usage:
    python scripts/publish_audiobook.py                         # Full pipeline
    python scripts/publish_audiobook.py --chapter 5             # Single chapter
    python scripts/publish_audiobook.py --force                 # Regenerate everything
    python scripts/publish_audiobook.py --no-sync               # Skip R2 upload
    python scripts/publish_audiobook.py --no-video              # Skip video stages
    python scripts/publish_audiobook.py --keyframes-only        # Stop after keyframes
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
        description="Full audiobook publish pipeline: text -> audio -> scenes -> video -> R2 sync"
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
    parser.add_argument("--no-video", action="store_true", help="Skip scene segmentation and video generation")
    parser.add_argument("--keyframes-only", action="store_true", help="Stop after keyframe generation (skip Veo animation)")
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

    # --- Step 2: Generate audio ---
    audio_args = list(shared)
    if args.force:
        audio_args.append("--force")

    if not run_step("Generate audio + MP3s + RSS", "generate_audiobook.py", audio_args):
        sys.exit(1)

    # --- Step 3: Scene segmentation ---
    if not args.no_video:
        scene_args = list(shared)
        if args.force:
            scene_args.append("--force")

        if not run_step("Scene segmentation", "generate_audiobook_scenes.py", scene_args):
            sys.exit(1)

        # --- Step 4: Video generation ---
        # Derive config name for the video script (positional arg, not --config)
        config_name = args.config
        # Strip _quarto- prefix and .yml suffix if present
        if config_name.startswith("_quarto-"):
            config_name = config_name[len("_quarto-"):]
        if config_name.endswith(".yml"):
            config_name = config_name[:-4]

        video_args = [config_name]
        if args.chapter:
            video_args += ["--chapter", str(args.chapter)]
        if args.start:
            video_args += ["--start", str(args.start)]
        if args.force:
            video_args.append("--force")
        if args.keyframes_only:
            video_args.append("--keyframes-only")

        step_label = "Generate keyframes" if args.keyframes_only else "Generate video (keyframes + Veo + assembly)"
        if not run_step(step_label, "generate_audiobook_video.py", video_args):
            sys.exit(1)

    # --- Step 5: Sync to R2 ---
    if args.no_sync:
        print("\n[DONE] Pipeline complete (--no-sync: skipped R2 upload).")
        return

    if not run_step("Sync to Cloudflare R2", "sync_r2.py", []):
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print("  PUBLISH COMPLETE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
