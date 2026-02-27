#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Scene Segmentation

Segments prepared audiobook text into visual scenes with precise timestamps
from forced alignment data. Falls back to linear interpolation if alignment
is unavailable. Generates keyframe_prompt and veo_prompt per scene.

This is a standalone pipeline step between audio generation and video generation:
    generate_audiobook_text.py -> generate_audiobook.py -> generate_audiobook_scenes.py -> generate_audiobook_video.py

Usage:
    python scripts/generate_audiobook_scenes.py                    # All chapters
    python scripts/generate_audiobook_scenes.py --chapter 20       # Single chapter
    python scripts/generate_audiobook_scenes.py --chapter 8 --scene 3  # Single scene prompt regen
    python scripts/generate_audiobook_scenes.py --start 5 --end 10 # Range
    python scripts/generate_audiobook_scenes.py --list             # List status
    python scripts/generate_audiobook_scenes.py --force            # Re-segment
    python scripts/generate_audiobook_scenes.py --force --overwrite-edits  # Overwrite manual edits
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
    PROJECT_ROOT, ALIGNMENT_DIR, SCENES_DIR,
    DEFAULT_CONFIG_PATH, extract_chapters, extract_title_from_qmd,
    safe_filename, chapter_slug, find_prepared_text, find_chapter_audio,
    resolve_chapter_titles, filter_chapters,
    AudiobookPaths, config_name_from_path, get_paths,
)
from lib.scenes import (
    segment_scenes, segment_scenes_with_prompts,
    estimate_timestamps, assign_timestamps_from_alignment,
    save_scene_manifest, load_scene_manifest,
    save_scene_files, load_scene_files, scene_has_manual_edits,
    scene_file_path,
)
from lib.scene_config import (
    load_scene_config, get_visual_style, get_no_text_instruction,
)


def find_alignment(chapter: dict, paths: AudiobookPaths | None = None) -> Path | None:
    """Find alignment JSON for a chapter."""
    alignment_dir = paths.alignment if paths else ALIGNMENT_DIR
    slug = chapter_slug(chapter)
    alignment_file = alignment_dir / f"{slug}.alignment.json"
    if alignment_file.exists():
        return alignment_file
    # Fallback: legacy index-prefixed name
    for f in sorted(alignment_dir.glob(f"*-{slug}.alignment.json")):
        return f
    return None


def regenerate_single_scene_prompt(
    chapter: dict,
    scene_index: int,
    text: str,
    visual_style: str,
    no_text: str,
    overwrite_edits: bool,
    scenes_dir: Path,
    slug: str,
):
    """Regenerate prompts for a single scene using the LLM."""
    from lib.scenes import _call_llm_with_timeout
    import json

    scenes = load_scene_files(scenes_dir, slug)
    if not scenes:
        print(f"  [ERROR] No scene file found. Run full segmentation first.")
        return

    target = None
    for s in scenes:
        if s['scene_index'] == scene_index:
            target = s
            break
    if not target:
        print(f"  [ERROR] Scene {scene_index} not found (available: {[s['scene_index'] for s in scenes]})")
        return

    # Check for manual edits
    if scene_has_manual_edits(target) and not overwrite_edits:
        print(f"  [SKIP] Scene {scene_index} has manual edits. Use --overwrite-edits to regenerate.")
        return

    narration = target.get('narration_text', '')
    context = target.get('context', '')

    prompt = (
        f"Generate a keyframe_prompt and veo_prompt for this scene.\n\n"
        f"Visual style: {visual_style}\n"
        f"No-text rule: {no_text}\n\n"
        f"Scene narration: {narration}\n"
        f"Context: {context}\n\n"
        f"keyframe_prompt: A detailed image generation prompt in the visual style above. "
        f"Describe the scene as a single illustration. Include the no-text rule. "
        f"Do NOT include 'Generate' or 'Create'.\n"
        f"veo_prompt: A video animation prompt describing camera motion and subject motion. "
        f"Keep it concise (1-2 sentences). Include 'No dialogue, narration, or speech.'\n\n"
        f"Return ONLY a JSON object:\n"
        f'{{"keyframe_prompt": "...", "veo_prompt": "..."}}'
    )

    print(f"  Regenerating prompts for scene {scene_index}...")
    response = _call_llm_with_timeout(prompt)
    response_text = response.strip()
    # Strip markdown
    import re
    response_text = re.sub(r'^```(?:json)?\s*\n?', '', response_text)
    response_text = re.sub(r'\n?```\s*$', '', response_text)
    result = json.loads(response_text)

    target['keyframe_prompt'] = result['keyframe_prompt']
    target['veo_prompt'] = result['veo_prompt']
    target['_auto_generated'] = {
        'keyframe_prompt': result['keyframe_prompt'],
        'veo_prompt': result['veo_prompt'],
    }

    # Save back the full scenes list
    path = scene_file_path(scenes_dir, slug)
    path.write_text(
        json.dumps(scenes, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"  [OK] Scene {scene_index} prompts regenerated")
    print(f"    keyframe: {target['keyframe_prompt'][:80]}...")
    print(f"    veo: {target['veo_prompt'][:80]}...")


def process_chapter(
    chapter: dict,
    force: bool = False,
    overwrite_edits: bool = False,
    scene_index: int | None = None,
    scene_config: dict | None = None,
    paths: AudiobookPaths | None = None,
):
    """Run scene segmentation for a single chapter."""
    slug = chapter_slug(chapter)
    scenes_dir = paths.scenes if paths else SCENES_DIR

    print(f"\n{'=' * 60}")
    print(f"Chapter {chapter['index']}: {chapter['title']}")
    print(f"{'=' * 60}")

    # Find required files
    text_file = find_prepared_text(chapter, paths=paths)
    if not text_file:
        print(f"  [SKIP] No prepared text. Run generate_audiobook_text.py first.")
        return

    audio_path = find_chapter_audio(chapter, paths=paths)
    if not audio_path:
        print(f"  [SKIP] No audio file. Run generate_audiobook.py first.")
        return

    text = text_file.read_text(encoding='utf-8')
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

    # Load scene config for visual style
    if not scene_config:
        video_dir = paths.video if paths else scenes_dir.parent
        scene_config = load_scene_config(video_dir)
    visual_style = get_visual_style(scene_config)
    no_text = get_no_text_instruction(scene_config)

    # Single scene prompt regeneration
    if scene_index is not None:
        regenerate_single_scene_prompt(
            chapter, scene_index, text, visual_style, no_text,
            overwrite_edits, scenes_dir, slug,
        )
        return

    # Check existing scene files first, then fall back to manifest
    existing_scenes = load_scene_files(scenes_dir, slug)
    existing_manifest = load_scene_manifest(scenes_dir, slug)

    if existing_scenes and not force:
        existing_hash = ""
        if existing_manifest:
            existing_hash = existing_manifest.get('text_hash', '')
        if existing_hash == text_hash:
            print(f"  [SKIP] Scene file up to date ({len(existing_scenes)} scenes, hash: {text_hash})")
            return
        if existing_hash:
            print(f"  Text changed (old: {existing_hash}, new: {text_hash}), re-segmenting...")
    elif existing_manifest and existing_manifest.get('scenes') and not force:
        existing_hash = existing_manifest.get('text_hash', '')
        if existing_hash == text_hash:
            print(f"  [SKIP] Scene manifest up to date ({len(existing_manifest['scenes'])} scenes, hash: {text_hash})")
            return
        print(f"  Text changed (old: {existing_hash}, new: {text_hash}), re-segmenting...")

    total_chars = len(text)
    print(f"  Text: {total_chars:,} chars ({text_file.name}) [hash: {text_hash}]")

    # Get audio duration
    audio = AudioSegment.from_wav(str(audio_path))
    total_duration_ms = len(audio)
    print(f"  Audio: {total_duration_ms:,}ms ({total_duration_ms / 1000:.1f}s)")

    # LLM scene segmentation (with prompts)
    scenes = segment_scenes_with_prompts(text, visual_style, no_text)

    # Assign timestamps: prefer alignment, fall back to interpolation
    alignment_path = find_alignment(chapter, paths=paths)
    if alignment_path:
        print(f"  Using alignment: {alignment_path.name}")
        from lib.alignment import load_alignment
        alignment_words = load_alignment(alignment_path)
        scenes = assign_timestamps_from_alignment(scenes, alignment_words, total_duration_ms)
    else:
        print(f"  [WARN] No alignment data; using linear interpolation")
        scenes = estimate_timestamps(scenes, total_chars, total_duration_ms)

    # Save scene file (preserving manual edits)
    scenes = save_scene_files(scenes, scenes_dir, slug, force=force, overwrite_edits=overwrite_edits)

    # Also save legacy manifest for backward compatibility
    save_scene_manifest(scenes, chapter, scenes_dir, slug, total_duration_ms, text_hash)
    print(f"  Done: {len(scenes)} scenes")


def list_chapters(chapters: list[dict], paths: AudiobookPaths | None = None):
    """Print all chapters with scene segmentation status."""
    scenes_dir = paths.scenes if paths else SCENES_DIR

    print(f"\nScene Segmentation Status ({len(chapters)} chapters):")
    print("=" * 90)

    current_part = None
    for ch in chapters:
        if ch['part'] != current_part:
            current_part = ch['part']
            if current_part:
                print(f"\n  [{current_part}]")

        slug = chapter_slug(ch)
        manifest = load_scene_manifest(scenes_dir, slug)
        scene_files = load_scene_files(scenes_dir, slug)
        scene_count = len(scene_files) if scene_files else (len(manifest['scenes']) if manifest else 0)

        text_file = find_prepared_text(ch, paths=paths)
        audio_file = find_chapter_audio(ch, paths=paths)
        alignment_file = find_alignment(ch, paths=paths)

        status_parts = []
        if text_file:
            status_parts.append("T")
        if audio_file:
            status_parts.append("A")
        if alignment_file:
            status_parts.append("AL")
        if scene_count:
            status_parts.append(f"S{scene_count}")

        # Count edited scenes
        edited_count = 0
        if scene_files:
            edited_count = sum(1 for s in scene_files if scene_has_manual_edits(s))

        ts_source = ""
        scenes_data = scene_files or (manifest.get('scenes', []) if manifest else [])
        if scenes_data:
            sources = set(s.get('timestamp_source', 'interpolation') for s in scenes_data)
            if sources == {'alignment'}:
                ts_source = " [aligned]"
            elif 'alignment' in sources:
                ts_source = " [mixed]"
            elif scene_count:
                ts_source = " [interp]"

        edit_marker = f" [{edited_count} edited]" if edited_count else ""

        status = ",".join(status_parts) if status_parts else "-"
        text_chars = len(text_file.read_text(encoding='utf-8')) if text_file else 0
        chars_info = f"{text_chars:,} chars" if text_chars else "no text"
        print(f"    {ch['index']:3d}. [{status:>12s}] {ch['title']} ({chars_info}){ts_source}{edit_marker}")

    print("=" * 90)
    print("  Legend: T=text, A=audio, AL=alignment, S#=scenes")


def main():
    parser = argparse.ArgumentParser(
        description="Segment audiobook chapters into visual scenes with precise timestamps"
    )
    parser.add_argument(
        "--config", "-cfg",
        default=str(DEFAULT_CONFIG_PATH),
        help=f"Quarto config YAML (default: {DEFAULT_CONFIG_PATH.name})"
    )
    parser.add_argument(
        "--chapter", "-c",
        type=int,
        help="Process only specific chapter number"
    )
    parser.add_argument(
        "--scene",
        type=int,
        help="Regenerate prompts for a single scene (requires --chapter)"
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
    parser.add_argument(
        "--overwrite-edits",
        action="store_true",
        help="Overwrite manually edited prompts (default: preserve edits)"
    )
    args = parser.parse_args()

    if args.scene and not args.chapter:
        parser.error("--scene requires --chapter")

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

    # Load scene config
    scene_config = load_scene_config(paths.video)

    print(f"Loading book configuration: {config_path.name} (output: assets/audiobook/{cfg_name}/)")
    config = load_quarto_config(config_path)
    chapters = extract_chapters(config)
    chapters = resolve_chapter_titles(chapters)
    print(f"Found {len(chapters)} chapters")

    if args.list:
        list_chapters(chapters, paths=paths)
        return

    chapters = filter_chapters(chapters, chapter=args.chapter, start=args.start, end=args.end)
    if not chapters:
        print("No chapters to process.")
        return

    print(f"Processing {len(chapters)} chapter(s)...")
    for chapter in chapters:
        process_chapter(
            chapter,
            force=args.force,
            overwrite_edits=args.overwrite_edits,
            scene_index=args.scene,
            scene_config=scene_config,
            paths=paths,
        )

    print(f"\n{'=' * 60}")
    print(f"All done! Processed {len(chapters)} chapter(s).")


if __name__ == "__main__":
    main()
