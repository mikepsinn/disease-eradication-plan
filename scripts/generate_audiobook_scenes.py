#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Scene Segmentation

Segments prepared audiobook text into visual scenes with precise timestamps
from forced alignment data. Falls back to linear interpolation if alignment
is unavailable.

This is a standalone pipeline step between audio generation and video generation:
    generate_audiobook_text.py -> generate_audiobook.py -> generate_audiobook_scenes.py -> generate_audiobook_video.py

Usage:
    python scripts/generate_audiobook_scenes.py                    # All chapters
    python scripts/generate_audiobook_scenes.py --chapter 20       # Single chapter
    python scripts/generate_audiobook_scenes.py --start 5 --end 10 # Range
    python scripts/generate_audiobook_scenes.py --list             # List status
    python scripts/generate_audiobook_scenes.py --force            # Re-segment
"""
import io
import sys
import hashlib
import argparse
from pathlib import Path

if sys.platform == 'win32' and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

from pydub import AudioSegment

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from dih_models.yaml_utils import load_quarto_config
from lib.audiobook_common import (
    PROJECT_ROOT, AUDIOBOOK_DIR, ALIGNMENT_DIR, SCENES_DIR,
    DEFAULT_CONFIG_PATH, extract_chapters, extract_title_from_qmd,
    safe_filename, find_prepared_text, find_chapter_audio,
    resolve_chapter_titles, filter_chapters,
)
from lib.scenes import (
    segment_scenes, estimate_timestamps, assign_timestamps_from_alignment,
    save_scene_manifest, load_scene_manifest,
)


def get_chapter_dir(chapter: dict) -> Path:
    """Get the scene directory for a chapter."""
    return SCENES_DIR / f"{chapter['index']:03d}-{safe_filename(chapter['title'])}"


def find_alignment(chapter: dict) -> Path | None:
    """Find alignment JSON for a chapter."""
    title = chapter.get('title') or ''
    safe = safe_filename(title)
    alignment_file = ALIGNMENT_DIR / f"{chapter['index']:03d}-{safe}.alignment.json"
    if alignment_file.exists():
        return alignment_file
    for f in ALIGNMENT_DIR.glob(f"{chapter['index']:03d}-*.alignment.json"):
        return f
    return None


def process_chapter(chapter: dict, force: bool = False):
    """Run scene segmentation for a single chapter."""
    print(f"\n{'=' * 60}")
    print(f"Chapter {chapter['index']}: {chapter['title']}")
    print(f"{'=' * 60}")

    # Find required files
    text_file = find_prepared_text(chapter)
    if not text_file:
        print(f"  [SKIP] No prepared text. Run generate_audiobook_text.py first.")
        return

    audio_path = find_chapter_audio(chapter)
    if not audio_path:
        print(f"  [SKIP] No audio file. Run generate_audiobook.py first.")
        return

    chapter_dir = get_chapter_dir(chapter)

    # Check existing manifest
    existing = load_scene_manifest(chapter_dir)
    text = text_file.read_text(encoding='utf-8')
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

    if existing and existing.get('scenes') and not force:
        existing_hash = existing.get('text_hash', '')
        if existing_hash == text_hash:
            print(f"  [SKIP] Scene manifest up to date ({len(existing['scenes'])} scenes, hash: {text_hash})")
            return
        print(f"  Text changed (old: {existing_hash}, new: {text_hash}), re-segmenting...")

    total_chars = len(text)
    print(f"  Text: {total_chars:,} chars ({text_file.name}) [hash: {text_hash}]")

    # Get audio duration
    audio = AudioSegment.from_wav(str(audio_path))
    total_duration_ms = len(audio)
    print(f"  Audio: {total_duration_ms:,}ms ({total_duration_ms / 1000:.1f}s)")

    # LLM scene segmentation
    scenes = segment_scenes(text)

    # Assign timestamps: prefer alignment, fall back to interpolation
    alignment_path = find_alignment(chapter)
    if alignment_path:
        print(f"  Using alignment: {alignment_path.name}")
        from lib.alignment import load_alignment
        alignment_words = load_alignment(alignment_path)
        scenes = assign_timestamps_from_alignment(scenes, alignment_words, total_duration_ms)
    else:
        print(f"  [WARN] No alignment data; using linear interpolation")
        scenes = estimate_timestamps(scenes, total_chars, total_duration_ms)

    save_scene_manifest(scenes, chapter, chapter_dir, total_duration_ms, text_hash)
    print(f"  Done: {len(scenes)} scenes")


def list_chapters(chapters: list[dict]):
    """Print all chapters with scene segmentation status."""
    print(f"\nScene Segmentation Status ({len(chapters)} chapters):")
    print("=" * 90)

    current_part = None
    for ch in chapters:
        if ch['part'] != current_part:
            current_part = ch['part']
            if current_part:
                print(f"\n  [{current_part}]")

        chapter_dir = get_chapter_dir(ch)
        manifest = load_scene_manifest(chapter_dir)
        scene_count = len(manifest['scenes']) if manifest else 0

        text_file = find_prepared_text(ch)
        audio_file = find_chapter_audio(ch)
        alignment_file = find_alignment(ch)

        status_parts = []
        if text_file:
            status_parts.append("T")
        if audio_file:
            status_parts.append("A")
        if alignment_file:
            status_parts.append("AL")
        if scene_count:
            status_parts.append(f"S{scene_count}")

        ts_source = ""
        if manifest and manifest.get('scenes'):
            sources = set(s.get('timestamp_source', 'interpolation') for s in manifest['scenes'])
            if sources == {'alignment'}:
                ts_source = " [aligned]"
            elif 'alignment' in sources:
                ts_source = " [mixed]"
            elif scene_count:
                ts_source = " [interp]"

        status = ",".join(status_parts) if status_parts else "-"
        text_chars = len(text_file.read_text(encoding='utf-8')) if text_file else 0
        chars_info = f"{text_chars:,} chars" if text_chars else "no text"
        print(f"    {ch['index']:3d}. [{status:>12s}] {ch['title']} ({chars_info}){ts_source}")

    print("=" * 90)
    print("  Legend: T=text, A=audio, AL=alignment, S#=scenes")


def main():
    parser = argparse.ArgumentParser(
        description="Segment audiobook chapters into visual scenes with precise timestamps"
    )
    parser.add_argument(
        "--chapter", "-c",
        type=int,
        help="Process only specific chapter number"
    )
    parser.add_argument(
        "--start", "-s",
        type=int,
        help="Start from this chapter number (inclusive)"
    )
    parser.add_argument(
        "--end", "-e",
        type=int,
        help="End at this chapter number (inclusive)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all chapters with scene status"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force re-segmentation even if manifest exists"
    )
    args = parser.parse_args()

    print("Loading book configuration...")
    config = load_quarto_config(DEFAULT_CONFIG_PATH)
    chapters = extract_chapters(config)
    chapters = resolve_chapter_titles(chapters)
    print(f"Found {len(chapters)} chapters")

    if args.list:
        list_chapters(chapters)
        return

    chapters = filter_chapters(chapters, chapter=args.chapter, start=args.start, end=args.end)
    if not chapters:
        print("No chapters to process.")
        return

    print(f"Processing {len(chapters)} chapter(s)...")
    for chapter in chapters:
        process_chapter(chapter, force=args.force)

    print(f"\n{'=' * 60}")
    print(f"All done! Processed {len(chapters)} chapter(s).")


if __name__ == "__main__":
    main()
