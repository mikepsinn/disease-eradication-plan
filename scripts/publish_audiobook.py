#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Publish Pipeline

Single script that runs the full audiobook pipeline:
  1. Generate narration text from QMD chapters (LLM rewrite)
  2. Generate audio (TTS), combine, MP3s, RSS, alignment, subtitles
  3. Scene segmentation (LLM visual scenes with prompts)
  4. Video generation (keyframes + Veo animation + assembly)
  5. Audible/ACX export (compliant MP3s + upload instructions)
  6. Sync assets to Cloudflare R2

Passes all arguments through to the underlying scripts, so you can use
--chapter, --start, --end, --force, --list, etc.

Usage:
    python scripts/publish_audiobook.py                         # Full pipeline
    python scripts/publish_audiobook.py --chapter 5             # Single chapter
    python scripts/publish_audiobook.py --force                 # Regenerate everything
    python scripts/publish_audiobook.py --no-sync               # Skip R2 upload
    python scripts/publish_audiobook.py --video                 # Include video stages
    python scripts/publish_audiobook.py --no-audible            # Skip Audible export
    python scripts/publish_audiobook.py --audible-only          # Only run Audible export
    python scripts/publish_audiobook.py --keyframes-only        # Stop after keyframes
    python scripts/publish_audiobook.py --ken-burns             # Ken Burns stills video (no Veo)
    python scripts/publish_audiobook.py --combine              # Include combined audiobook MP3/M4B
    python scripts/publish_audiobook.py --list                  # List chapters and exit
    python scripts/publish_audiobook.py --dry-run               # Text dry-run only
"""
import sys
import subprocess
import argparse
import hashlib
import time
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

OUTRO_QMD_PATH = PROJECT_ROOT / "knowledge" / "appendix" / "podcast-outro.qmd"


def _ts() -> str:
    """Current timestamp for log lines."""
    return datetime.now().strftime("%H:%M:%S")


def run_step(label: str, script: str, args: list[str]) -> bool:
    """Run a pipeline step, returning True on success."""
    print(f"\n{'=' * 70}")
    print(f"  [{_ts()}] STEP: {label}")
    print(f"{'=' * 70}\n")

    t0 = time.monotonic()
    cmd = [sys.executable, "-u", str(SCRIPTS_DIR / script)] + args
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    elapsed = time.monotonic() - t0
    mins, secs = divmod(int(elapsed), 60)

    if result.returncode != 0:
        print(f"\n[{_ts()}] [FAILED] {label} (exit code {result.returncode}, {mins}m{secs:02d}s)")
        return False
    print(f"\n[{_ts()}] [OK] {label} ({mins}m{secs:02d}s)")
    return True


def print_staleness_summary(config_path: Path, chapter_filter: int | None,
                           start: int | None, end: int | None) -> None:
    """Print a summary of which QMD files have changed since last generation."""
    from lib.audiobook_common import (
        extract_chapters, chapter_slug, config_name_from_path, get_paths,
        VARIABLES_YML,
    )
    from dih_models.yaml_utils import load_quarto_config
    from dih_models.variable_replacement import load_variables, replace_variables

    config = load_quarto_config(config_path)
    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)
    chapters = extract_chapters(config)
    variables = load_variables(VARIABLES_YML) if VARIABLES_YML.exists() else {}

    # Apply chapter filters
    if chapter_filter is not None:
        chapters = [c for c in chapters if c['index'] == chapter_filter]
    if start is not None:
        chapters = [c for c in chapters if c['index'] >= start]
    if end is not None:
        chapters = [c for c in chapters if c['index'] <= end]

    stale = []
    cached = []
    missing = []

    for ch in chapters:
        slug = chapter_slug(ch)
        qmd_path = PROJECT_ROOT / ch['path']
        hash_file = paths.narration_txt / f"{slug}.source_hash"
        prepared_file = paths.narration_txt / f"{slug}.prepared.txt"

        if not qmd_path.exists():
            missing.append((ch, "QMD file missing"))
            continue

        raw = qmd_path.read_text(encoding='utf-8')
        # Match the hash from generate_audiobook_text.py: QMD with variables resolved
        current_hash = hashlib.sha256(
            replace_variables(raw, variables, highlight_missing=False).encode('utf-8')
        ).hexdigest()[:16]

        if not prepared_file.exists():
            stale.append((ch, "no prepared text yet"))
        elif not hash_file.exists():
            stale.append((ch, "no hash recorded"))
        else:
            old_hash = hash_file.read_text(encoding='utf-8').strip()
            if old_hash != current_hash:
                stale.append((ch, "QMD changed"))
            else:
                cached.append(ch)

    # Check outro
    outro_status = None
    if OUTRO_QMD_PATH.exists():
        chapters_dir = paths.chapters
        outro_hash_file = chapters_dir / "podcast-outro.qmdhash"
        outro_wav = chapters_dir / "podcast-outro.wav"

        qmd_content = OUTRO_QMD_PATH.read_text(encoding='utf-8')
        hash_input = qmd_content
        if VARIABLES_YML.exists():
            hash_input += VARIABLES_YML.read_text(encoding='utf-8')
        current_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]

        if not outro_wav.exists():
            outro_status = ("STALE", "no audio yet")
        elif not outro_hash_file.exists():
            outro_status = ("STALE", "no hash recorded")
        else:
            old_hash = outro_hash_file.read_text(encoding='utf-8').strip()
            if old_hash != current_hash:
                outro_status = ("STALE", "source or variables changed")
            else:
                outro_status = ("CACHED", "up to date")

    # Print summary
    print(f"\n{'=' * 70}")
    print(f"  [{_ts()}] STALENESS SUMMARY")
    print(f"{'=' * 70}\n")

    total = len(stale) + len(cached) + len(missing)
    print(f"  Chapters: {total} total, {len(stale)} stale, {len(cached)} cached, {len(missing)} missing")
    if outro_status:
        print(f"  Outro:    [{outro_status[0]}] {outro_status[1]}")
    print()

    if stale:
        print("  STALE (will regenerate):")
        for ch, reason in stale:
            print(f"    [{ch['index']:2d}] {ch['title']}")
            print(f"         {ch['path']} ({reason})")
        print()

    if missing:
        print("  MISSING:")
        for ch, reason in missing:
            print(f"    [{ch['index']:2d}] {ch['title']} - {reason}")
        print()

    if not stale and not missing and (not outro_status or outro_status[0] == "CACHED"):
        print("  Everything is up to date. Nothing to regenerate.")
        print()


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
    parser.add_argument("--video", action="store_true", help="Include scene segmentation and video generation (off by default)")
    parser.add_argument("--no-audible", action="store_true", help="Skip Audible/ACX export step")
    parser.add_argument("--audible-only", action="store_true", help="Only run Audible/ACX export (skip all other steps)")
    parser.add_argument("--target-rms", type=float, default=-20.0, help="Target RMS for Audible export (default: -20.0 dB)")
    parser.add_argument("--keyframes-only", action="store_true", help="Stop after keyframe generation (skip Veo animation)")
    parser.add_argument("--ken-burns", action="store_true", help="Generate Ken Burns stills video (pan/zoom on keyframes, no Veo)")
    parser.add_argument("--combine", action="store_true", help="Combine chapters into single audiobook MP3/M4B (off by default)")
    args = parser.parse_args()

    # --ken-burns implicitly enables --video
    if args.ken_burns:
        args.video = True

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

    # --- Audible-only mode: skip everything else ---
    if args.audible_only:
        audible_args = ["--config", args.config, "--target-rms", str(args.target_rms)]
        if args.force:
            audible_args.append("--force")
        if not run_step("Audible/ACX export", "generate_audible_export.py", audible_args):
            sys.exit(1)
        print(f"\n[{_ts()}] [DONE] Audible export complete.")
        return

    # --- Pre-flight: show what's changed ---
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path
    print_staleness_summary(config_path, args.chapter, args.start, args.end)

    # --- Step 1: Generate narration text ---
    text_args = list(shared)
    if args.force:
        text_args.append("--force")
    if args.dry_run:
        text_args.append("--dry-run")

    if not run_step("Generate narration text", "generate_audiobook_text.py", text_args):
        sys.exit(1)

    if args.dry_run:
        print(f"\n[{_ts()}] [DONE] Dry run complete (text only, no audio generated).")
        return

    # --- Step 2: Generate audio ---
    audio_args = list(shared)
    if args.force:
        audio_args.append("--force")
    if not args.combine:
        audio_args.append("--no-combine")

    if not run_step("Generate audio + MP3s + RSS", "generate_audiobook.py", audio_args):
        sys.exit(1)

    # --- Step 3: Scene segmentation ---
    if args.video:
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
        if args.ken_burns:
            video_args.append("--ken-burns")

        if args.keyframes_only:
            step_label = "Generate keyframes"
        elif args.ken_burns:
            step_label = "Generate Ken Burns stills video"
        else:
            step_label = "Generate video (keyframes + Veo + assembly)"
        if not run_step(step_label, "generate_audiobook_video.py", video_args):
            sys.exit(1)

    # --- Step 5: Audible/ACX export ---
    if not args.no_audible:
        audible_args = ["--config", args.config, "--target-rms", str(args.target_rms)]
        if args.force:
            audible_args.append("--force")
        if not run_step("Audible/ACX export", "generate_audible_export.py", audible_args):
            sys.exit(1)

    # --- Step 6: Sync to R2 ---
    if args.no_sync:
        print(f"\n[{_ts()}] [DONE] Pipeline complete (--no-sync: skipped R2 upload).")
        return

    if not run_step("Sync to Cloudflare R2", "sync_r2.py", []):
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print(f"  [{_ts()}] PUBLISH COMPLETE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
