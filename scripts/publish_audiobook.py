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
    python scripts/publish_audiobook.py --no-sync               # Skip all R2 uploads
    python scripts/publish_audiobook.py --video                 # Include video stages
    python scripts/publish_audiobook.py --no-audible            # Skip Audible export
    python scripts/publish_audiobook.py --audible-only          # Only run Audible export
    python scripts/publish_audiobook.py --keyframes-only        # Stop after keyframes
    python scripts/publish_audiobook.py --ken-burns             # Ken Burns stills video (no Veo)
    python scripts/publish_audiobook.py --combine              # Include combined audiobook MP3/M4B
    python scripts/publish_audiobook.py --regenerate-outro     # Force-regenerate outro + rewrap chapter MP3s
    python scripts/publish_audiobook.py --rewrap-outro-only    # Regenerate outro + rewrap chapter MP3s
    python scripts/publish_audiobook.py --no-sync-each-chapter  # Disable immediate per-chapter R2 uploads
    python scripts/publish_audiobook.py --list                  # List chapters and exit
    python scripts/publish_audiobook.py --dry-run               # Text dry-run only
"""
import sys
import subprocess
import argparse
import hashlib
import json
import time
import atexit
import re
from collections import deque
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

OUTRO_QMD_PATH = PROJECT_ROOT / "knowledge" / "appendix" / "podcast-outro.qmd"

from lib.script_lock import acquire_script_lock, ScriptLockError


def _ts() -> str:
    """Current timestamp for log lines."""
    return datetime.now().strftime("%H:%M:%S")


def _fmt_elapsed(seconds: float) -> str:
    """Format elapsed seconds as '1h02m03s', '5m23s', or '12s'."""
    total = int(seconds)
    hrs, remainder = divmod(total, 3600)
    mins, secs = divmod(remainder, 60)
    if hrs > 0:
        return f"{hrs}h{mins:02d}m{secs:02d}s"
    if mins > 0:
        return f"{mins}m{secs:02d}s"
    return f"{secs}s"


# Accumulates (label, elapsed_seconds, success, indent) for the final summary
_step_timings: list[tuple[str, float, bool, int]] = []

# Set after audio generation so the timing summary can include chapter stats
_manifest_path: Path | None = None

# Per-run debug logs directory and monotonic step counter
_run_log_dir: Path | None = None
_step_counter: int = 0


def _slugify(text: str) -> str:
    """Filesystem-safe slug for step log names."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "step"


def run_step(label: str, script: str, args: list[str]) -> bool:
    """Run a pipeline step, returning True on success."""
    global _step_counter
    _step_counter += 1
    step_id = f"{_step_counter:02d}"

    print(f"\n{'=' * 70}")
    print(f"  [{_ts()}] STEP {step_id}: {label}")
    print(f"{'=' * 70}\n")

    t0 = time.monotonic()
    cmd = [sys.executable, "-u", str(SCRIPTS_DIR / script)] + args
    cmd_display = " ".join(cmd)

    step_log_path: Path | None = None
    if _run_log_dir is not None:
        step_log_path = _run_log_dir / f"{step_id}-{_slugify(label)}.log"
        step_log_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  [{_ts()}] CMD: {cmd_display}")
    if step_log_path is not None:
        print(f"  [{_ts()}] DEBUG LOG: {step_log_path}")
    print()

    tail_lines: deque[str] = deque(maxlen=40)
    return_code = 0
    if step_log_path is None:
        result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
        return_code = int(result.returncode)
    else:
        with open(step_log_path, "w", encoding="utf-8", newline="\n") as step_log:
            step_log.write(f"[RUN] {cmd_display}\n\n")
            step_log.flush()
            process = subprocess.Popen(
                cmd,
                cwd=str(PROJECT_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            for line in (process.stdout or []):
                step_log.write(line)
                tail_lines.append(line.rstrip("\n"))
                print(line, end="", flush=True)
            process.wait()
            return_code = int(process.returncode or 0)

    elapsed = time.monotonic() - t0

    if return_code != 0:
        _step_timings.append((label, elapsed, False, 0))
        print(f"\n[{_ts()}] [FAILED] {label} (exit code {return_code}, {_fmt_elapsed(elapsed)})")
        if tail_lines:
            print(f"[{_ts()}] Last output lines:")
            for line in tail_lines:
                print(f"  {line}")
        if step_log_path is not None:
            print(f"[{_ts()}] Full debug log: {step_log_path}")
        return False
    _step_timings.append((label, elapsed, True, 0))
    print(f"\n[{_ts()}] [OK] {label} ({_fmt_elapsed(elapsed)})")
    return True


def _inject_substep_timings(timing_report: Path) -> None:
    """Read .audio-timing.json and replace the last top-level step with substeps."""
    if not timing_report.exists():
        return
    substeps: dict[str, float] = json.loads(timing_report.read_text(encoding="utf-8"))
    # Remove the last entry (the aggregate "Generate audio" step)
    if not _step_timings:
        return
    parent_label, parent_elapsed, parent_ok, _ = _step_timings.pop()
    # Add substeps with indent=1
    for sub_label, sub_elapsed in substeps.items():
        _step_timings.append((sub_label, sub_elapsed, True, 1))
    # Re-add the parent as a total line
    _step_timings.append((parent_label + " (total)", parent_elapsed, parent_ok, 0))


def _print_chapter_stats() -> None:
    """Print chapter-level stats from manifest.json (counts, durations)."""
    if not _manifest_path or not _manifest_path.exists():
        return
    manifest = json.loads(_manifest_path.read_text(encoding="utf-8"))
    chapters = manifest.get("chapters", [])
    if not chapters:
        return

    generated = sum(1 for c in chapters if c.get("status") == "generated")
    cached = sum(1 for c in chapters if c.get("status") == "cached")
    total = len(chapters)
    total_dur_ms = sum(c.get("duration_ms", 0) for c in chapters)

    # Format total duration as hours:minutes
    total_secs = total_dur_ms // 1000
    hrs, remainder = divmod(total_secs, 3600)
    mins, secs = divmod(remainder, 60)
    if hrs > 0:
        dur_str = f"{hrs}h{mins:02d}m{secs:02d}s"
    else:
        dur_str = f"{mins}m{secs:02d}s"

    print(f"  Chapters: {total} total, {generated} generated, {cached} cached")
    print(f"  Total audio duration: {dur_str}")

    # Video stats if any chapters have them
    with_video = sum(1 for c in chapters if c.get("video_status") == "generated")
    if with_video:
        print(f"  Video: {with_video}/{total} chapters have video")
    print()


def _print_timing_summary(pipeline_start: float) -> None:
    """Print a table of all step durations and total pipeline time."""
    total_elapsed = time.monotonic() - pipeline_start
    print(f"\n{'=' * 70}")
    print(f"  [{_ts()}] TIMING SUMMARY")
    print(f"{'=' * 70}\n")

    _print_chapter_stats()

    if _step_timings:
        max_label = max(len(lbl) + indent * 2 for lbl, _, _, indent in _step_timings)
        max_label = max(max_label, 6)
        for label, elapsed, success, indent in _step_timings:
            status = "OK" if success else "FAILED"
            display_label = ("  " * indent) + label
            print(f"  [{status:>6}] {display_label:<{max_label}}  {_fmt_elapsed(elapsed):>10}")
        print(f"  {'-' * (max_label + 22)}")

    print(f"  {'TOTAL':<{max_label + 9 if _step_timings else 14}}  {_fmt_elapsed(total_elapsed):>10}")
    print()


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
        wavs_dir = paths.wavs
        outro_hash_file = wavs_dir / "podcast-outro.qmdhash"
        outro_wav = wavs_dir / "podcast-outro.wav"

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
    parser.add_argument("--no-sync", action="store_true", help="Skip all R2 uploads (per-chapter and final sync step)")
    parser.add_argument("--video", action="store_true", help="Include scene segmentation and video generation (off by default)")
    parser.add_argument("--no-audible", action="store_true", help="Skip Audible/ACX export step")
    parser.add_argument("--audible-only", action="store_true", help="Only run Audible/ACX export (skip all other steps)")
    parser.add_argument("--target-rms", type=float, default=-20.0, help="Target RMS for Audible export (default: -20.0 dB)")
    parser.add_argument("--keyframes-only", action="store_true", help="Stop after keyframe generation (skip Veo animation)")
    parser.add_argument("--ken-burns", action="store_true", help="Generate Ken Burns stills video (pan/zoom on keyframes, no Veo)")
    parser.add_argument("--combine", action="store_true", help="Combine chapters into single audiobook MP3/M4B (off by default)")
    parser.add_argument(
        "--regenerate-outro",
        action="store_true",
        help="Force-regenerate podcast outro and rewrap chapter MP3s with the new outro (implies --rewrap-outro-only --force --no-sync-each-chapter)",
    )
    parser.add_argument(
        "--rewrap-outro-only",
        action="store_true",
        help="Regenerate podcast outro and rewrap existing chapter MP3s (skip text/audio/video/audible generation)",
    )
    parser.add_argument("--sync-each-chapter", dest="sync_each_chapter", action="store_true",
                        help="Immediately upload each newly generated chapter MP3 + refreshed feed/manifest to R2 (default: enabled)")
    parser.add_argument("--no-sync-each-chapter", dest="sync_each_chapter", action="store_false",
                        help="Disable immediate per-chapter R2 upload during audio generation")
    parser.set_defaults(sync_each_chapter=True)
    args = parser.parse_args()

    try:
        lock = acquire_script_lock(
            "publish-audiobook",
            PROJECT_ROOT,
            command=" ".join(sys.argv),
        )
        atexit.register(lock.release)
    except ScriptLockError as e:
        print(f"[{_ts()}] [ERROR] {e}")
        sys.exit(2)

    pipeline_start = time.monotonic()
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    global _run_log_dir, _step_counter
    _step_counter = 0
    _run_log_dir = PROJECT_ROOT / "logs" / "publish-audiobook" / run_id
    _run_log_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[{_ts()}] Pipeline started")
    print(f"[{_ts()}] Debug logs: {_run_log_dir}")

    # --ken-burns implicitly enables --video
    if args.ken_burns:
        args.video = True
    # Convenience mode: one flag for forced outro regen + rewrap, without noisy per-chapter sync.
    if args.regenerate_outro:
        args.rewrap_outro_only = True
        args.force = True
        args.sync_each_chapter = False
    # --no-sync is a hard override for all R2 uploads.
    if args.no_sync and args.sync_each_chapter:
        args.sync_each_chapter = False

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
            _print_timing_summary(pipeline_start)
            sys.exit(1)
        _print_timing_summary(pipeline_start)
        print(f"[{_ts()}] [DONE] Audible export complete.")
        return

    # --- Rewrap-only mode: regenerate outro + rewrap chapter MP3s ---
    if args.rewrap_outro_only:
        audio_args = list(shared)
        if args.force:
            audio_args.append("--force")
        if args.sync_each_chapter:
            audio_args.append("--sync-each-chapter")
        else:
            audio_args.append("--no-sync-each-chapter")
        audio_args.append("--rewrap-only")

        step_label = "Regenerate outro + rewrap chapter MP3s"
        if not run_step(step_label, "generate_audiobook.py", audio_args):
            _print_timing_summary(pipeline_start)
            sys.exit(1)

        # Inject substep timings from the audio generation step
        from lib.audiobook_common import config_name_from_path, get_paths
        config_path = Path(args.config)
        if not config_path.is_absolute():
            config_path = PROJECT_ROOT / config_path
        cfg_name = config_name_from_path(config_path)
        audio_paths = get_paths(cfg_name)
        _inject_substep_timings(audio_paths.root / ".audio-timing.json")

        global _manifest_path
        _manifest_path = audio_paths.root / "manifest.json"

        if args.no_sync:
            _print_timing_summary(pipeline_start)
            print(f"[{_ts()}] [DONE] Outro rewrap complete (--no-sync: skipped R2 upload).")
            return

        if not run_step("Sync to Cloudflare R2", "sync_r2.py", []):
            _print_timing_summary(pipeline_start)
            sys.exit(1)

        _print_timing_summary(pipeline_start)
        print(f"[{_ts()}] [DONE] Outro rewrap complete.")
        return

    # --- Pre-flight: show what's changed ---
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    t0_stale = time.monotonic()
    print_staleness_summary(config_path, args.chapter, args.start, args.end)
    stale_elapsed = time.monotonic() - t0_stale
    _step_timings.append(("Staleness check", stale_elapsed, True, 0))
    print(f"  [{_ts()}] Staleness check took {_fmt_elapsed(stale_elapsed)}")

    # --- Step 1: Generate narration text ---
    text_args = list(shared)
    if args.force:
        text_args.append("--force")
    if args.dry_run:
        text_args.append("--dry-run")

    if not run_step("Generate narration text", "generate_audiobook_text.py", text_args):
        _print_timing_summary(pipeline_start)
        sys.exit(1)

    if args.dry_run:
        _print_timing_summary(pipeline_start)
        print(f"[{_ts()}] [DONE] Dry run complete (text only, no audio generated).")
        return

    # --- Step 2: Generate audio ---
    audio_args = list(shared)
    if args.force:
        audio_args.append("--force")
    if not args.combine:
        audio_args.append("--no-combine")
    if args.sync_each_chapter:
        audio_args.append("--sync-each-chapter")
    else:
        audio_args.append("--no-sync-each-chapter")
    # Step 1 already prepared narration text; avoid duplicate per-chapter text subprocesses.
    audio_args.append("--skip-text-prep")

    step_label = "Generate audio + MP3s + RSS"
    if not run_step(step_label, "generate_audiobook.py", audio_args):
        _print_timing_summary(pipeline_start)
        sys.exit(1)

    # Inject substep timings from the audio generation step
    from lib.audiobook_common import config_name_from_path, get_paths
    cfg_name = config_name_from_path(config_path)
    audio_paths = get_paths(cfg_name)
    _inject_substep_timings(audio_paths.root / ".audio-timing.json")

    _manifest_path = audio_paths.root / "manifest.json"

    # List generated MP3s
    mp3_dir = audio_paths.root / "mp3"
    if mp3_dir.exists():
        mp3_files = sorted(mp3_dir.glob("*.mp3"))
        if mp3_files:
            print(f"\n  Generated {len(mp3_files)} MP3 files:")
            for mp3 in mp3_files:
                print(f"    {mp3}")
            print()

    # --- Step 3: Scene segmentation ---
    if args.video:
        scene_args = list(shared)
        if args.force:
            scene_args.append("--force")

        if not run_step("Scene segmentation", "generate_audiobook_scenes.py", scene_args):
            _print_timing_summary(pipeline_start)
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
            _print_timing_summary(pipeline_start)
            sys.exit(1)

    # --- Step 5: Audible/ACX export ---
    if not args.no_audible:
        audible_args = ["--config", args.config, "--target-rms", str(args.target_rms)]
        if args.force:
            audible_args.append("--force")
        if not run_step("Audible/ACX export", "generate_audible_export.py", audible_args):
            _print_timing_summary(pipeline_start)
            sys.exit(1)

    # --- Step 6: Sync to R2 ---
    if args.no_sync:
        _print_timing_summary(pipeline_start)
        print(f"[{_ts()}] [DONE] Pipeline complete (--no-sync: skipped R2 upload).")
        return

    if not run_step("Sync to Cloudflare R2", "sync_r2.py", []):
        _print_timing_summary(pipeline_start)
        sys.exit(1)

    _print_timing_summary(pipeline_start)
    print(f"{'=' * 70}")
    print(f"  [{_ts()}] PUBLISH COMPLETE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
