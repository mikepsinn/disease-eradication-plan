#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Podcast & YouTube Episode Image Generator

Generates per-chapter images for the audiobook podcast feed and YouTube:
  - Podcast: 1:1 square (1400x1400+) for Apple Podcasts / Spotify itunes:image
  - YouTube: 16:9 landscape thumbnails

Uses Imagen 4.
Prompts are built from prepared audiobook text (already variable-resolved).

Pipeline position:
    generate_audiobook_text.py -> THIS -> generate_audiobook.py (RSS uses images)

Usage:
    python scripts/generate_podcast_images.py                    # All chapters
    python scripts/generate_podcast_images.py --chapter 20       # Single chapter
    python scripts/generate_podcast_images.py --start 5 --end 10 # Range
    python scripts/generate_podcast_images.py --list             # Show status
    python scripts/generate_podcast_images.py --force            # Regenerate all
    python scripts/generate_podcast_images.py --podcast-only     # Skip YouTube thumbs
    python scripts/generate_podcast_images.py --youtube-only     # Skip podcast images
"""
import io
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if sys.platform == 'win32' and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.image_gen import rate_limited_generate_image
from dih_models.yaml_utils import load_quarto_config
from lib.audiobook_common import (
    PROJECT_ROOT, DEFAULT_CONFIG_PATH, IMAGE_STYLE, text_hash,
    extract_chapters, chapter_slug, find_prepared_text,
    find_podcast_image, find_youtube_thumbnail,
    resolve_chapter_titles, filter_chapters,
    AudiobookPaths, config_name_from_path, get_paths,
)

# --- Configuration ---
# Gemini 3.1 Pro: 10 RPM limit, rate limiter allows 8; keep workers <= 4
PARALLEL_WORKERS = 4


def _build_prompt(prepared_text: str, chapter_title: str) -> str:
    """Build an Imagen prompt from prepared audiobook text."""
    return (
        f"Generate a {IMAGE_STYLE} illustration that captures this chapter. "
        f"Do not include any text, titles, or author names in the image.\n"
        f"--- CHAPTER: {chapter_title} ---\n"
        f"{prepared_text[:4000]}\n"
        f"--- END ---"
    )


def _hash_file(path: Path) -> str:
    """Read the text hash marker from a sidecar .hash file, or empty string."""
    hash_path = path.with_suffix(path.suffix + '.hash')
    if hash_path.exists():
        return hash_path.read_text(encoding='utf-8').strip()
    return ''


def _write_hash(path: Path, content_hash: str):
    """Write a text hash sidecar so we can detect staleness."""
    hash_path = path.with_suffix(path.suffix + '.hash')
    hash_path.write_text(content_hash, encoding='utf-8')


def process_chapter(
    chapter: dict,
    force: bool = False,
    paths: AudiobookPaths | None = None,
    gen_podcast: bool = True,
    gen_youtube: bool = True,
) -> list[tuple[dict, str, Path]]:
    """Determine which images need generation for a chapter.

    Returns list of (chapter, aspect_ratio, output_path) work items.
    """
    slug = chapter_slug(chapter)
    img_dir = paths.podcast_images if paths else PROJECT_ROOT / "assets" / "audiobook" / "podcast-images"

    text_file = find_prepared_text(chapter, paths=paths)
    if not text_file:
        print(f"  [SKIP] Ch {chapter['index']}: {chapter['title']} -- no prepared text")
        return []

    text = text_file.read_text(encoding='utf-8')
    text_h = text_hash(text)

    work_items = []

    targets = []
    if gen_podcast:
        targets.append(("1:1", f"{slug}-podcast.jpg"))
    if gen_youtube:
        targets.append(("16:9", f"{slug}-youtube.jpg"))

    ch_label = f"Ch {chapter['index']}: {chapter['title']}"

    for aspect, filename in targets:
        output_path = img_dir / filename
        if output_path.exists() and not force:
            old_hash = _hash_file(output_path)
            if old_hash == text_h:
                print(f"  [CACHED] {ch_label} -> {filename}")
                continue
            if old_hash:
                print(f"  [STALE] {ch_label} -> {filename} (text changed)")
            else:
                print(f"  [CACHED] {ch_label} -> {filename} (no hash, assuming current)")
                continue

        work_items.append((chapter, aspect, output_path))

    return work_items


def generate_images(
    chapters: list[dict],
    force: bool = False,
    paths: AudiobookPaths | None = None,
    gen_podcast: bool = True,
    gen_youtube: bool = True,
):
    """Generate podcast and YouTube images for all given chapters."""
    all_work: list[tuple[dict, str, Path]] = []
    for ch in chapters:
        items = process_chapter(ch, force=force, paths=paths,
                                gen_podcast=gen_podcast, gen_youtube=gen_youtube)
        all_work.extend(items)

    if not all_work:
        print("\nAll images are up to date.")
        return

    print(f"\nGenerating {len(all_work)} image(s) ({PARALLEL_WORKERS} parallel workers)...")

    def _do_generate(item):
        chapter, aspect, output_path = item
        slug = chapter_slug(chapter)
        text_file = find_prepared_text(chapter, paths=paths)
        assert text_file, f"No prepared text for chapter {chapter['index']}"
        text = text_file.read_text(encoding='utf-8')
        text_h = text_hash(text)

        print(f"\n  [GEN] Ch {chapter['index']}: {chapter['title']} -> {output_path.name} ({aspect})")

        prompt = _build_prompt(text, chapter['title'])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        rate_limited_generate_image(prompt, output_path, aspect)
        _write_hash(output_path, text_h)
        return output_path

    errors = []
    with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as executor:
        futures = {executor.submit(_do_generate, item): item for item in all_work}
        for future in as_completed(futures):
            item = futures[future]
            chapter, aspect, output_path = item
            try:
                result_path = future.result()
                print(f"  [OK] {result_path.name} ({aspect})")
            except Exception as e:
                errors.append(f"Ch {chapter['index']} ({aspect}): {e}")
                print(f"  [ERROR] Ch {chapter['index']} {output_path.name}: {e}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")


def list_chapters(chapters: list[dict], paths: AudiobookPaths | None = None):
    """Print chapter status for podcast/YouTube images."""
    print(f"\nPodcast/YouTube Image Status ({len(chapters)} chapters):")
    print("=" * 90)

    for ch in chapters:
        slug = chapter_slug(ch)
        text_file = find_prepared_text(ch, paths=paths)
        podcast_img = find_podcast_image(ch, paths=paths)
        youtube_img = find_youtube_thumbnail(ch, paths=paths)

        parts = []
        if text_file:
            parts.append("T")
        if podcast_img:
            parts.append("P")
        if youtube_img:
            parts.append("YT")

        status = ",".join(parts) if parts else "-"
        text_info = f"{len(text_file.read_text(encoding='utf-8')):,} chars" if text_file else "no text"
        print(f"  {ch['index']:3d}. [{status:>6s}] {ch['title']} ({text_info})")

    print("=" * 90)
    print("  Legend: T=prepared text, P=podcast image (1:1), YT=YouTube thumbnail (16:9)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate podcast episode images and YouTube thumbnails"
    )
    parser.add_argument(
        "--config", "-cfg",
        default=str(DEFAULT_CONFIG_PATH),
        help=f"Quarto config YAML (default: {DEFAULT_CONFIG_PATH.name})"
    )
    parser.add_argument("--chapter", "-c", type=int, help="Process specific chapter number")
    parser.add_argument("--start", "-s", type=int, help="Start chapter (inclusive)")
    parser.add_argument("--end", "-e", type=int, help="End chapter (inclusive)")
    parser.add_argument("--list", "-l", action="store_true", help="Show image status")
    parser.add_argument("--force", "-f", action="store_true", help="Regenerate even if cached")
    parser.add_argument("--podcast-only", action="store_true", help="Only generate 1:1 podcast images")
    parser.add_argument("--youtube-only", action="store_true", help="Only generate 16:9 YouTube thumbnails")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

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

    gen_podcast = not args.youtube_only
    gen_youtube = not args.podcast_only

    types_str = []
    if gen_podcast:
        types_str.append("podcast (1:1)")
    if gen_youtube:
        types_str.append("YouTube (16:9)")
    print(f"Generating: {', '.join(types_str)}")
    print(f"Processing {len(chapters)} chapter(s)...")

    generate_images(chapters, force=args.force, paths=paths,
                    gen_podcast=gen_podcast, gen_youtube=gen_youtube)

    print(f"\nDone! Processed {len(chapters)} chapter(s).")


if __name__ == "__main__":
    main()
