#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Generator

Generates an audiobook from all chapters in _quarto-manual-paperback.yml using Gemini TTS.

Pipeline: Regenerates prepared text (via generate_audiobook_text.py subprocess),
then converts each text chunk to audio via Gemini TTS, and combines into chapter WAVs.

Usage:
    python scripts/generate_audiobook.py                    # Generate full audiobook
    python scripts/generate_audiobook.py --chapter 5       # Generate specific chapter
    python scripts/generate_audiobook.py --voice Zephyr    # Use different voice
    python scripts/generate_audiobook.py --list            # List all chapters
"""
import sys
import json
import re
import argparse
import subprocess
from pathlib import Path
from typing import TypedDict

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from pydub import AudioSegment

# Add scripts directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))
# Add project root to path for dih_models imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.tts import generate_speech, AVAILABLE_VOICES, DEFAULT_VOICE
from dih_models.yaml_utils import yaml_safe_load, load_quarto_config

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
QUARTO_BOOK_YML = PROJECT_ROOT / "_quarto-manual-paperback.yml"
OUTPUT_DIR = PROJECT_ROOT / "audiobook"
CHAPTER_AUDIO_DIR = OUTPUT_DIR / "chapters"
TEXT_DIR = OUTPUT_DIR / "text"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"

# Voice for narration (Kore + dinner-party energy, winner from A/B testing)
NARRATOR_VOICE = DEFAULT_VOICE


def extract_book_metadata(config: dict) -> dict:
    """Extract book metadata (title, author, year, publisher, cover) from quarto config."""
    book = config.get('book', {})
    metadata = config.get('metadata', {})

    # Author: first entry in book.author list, or fallback to metadata.creator
    authors = book.get('author', [])
    if isinstance(authors, list) and authors:
        author = authors[0].get('name', '') if isinstance(authors[0], dict) else str(authors[0])
    else:
        author = metadata.get('creator', 'Unknown')

    # Cover art: from epub config, fall back to conventional path
    cover_path = config.get('format', {}).get('epub', {}).get('epub-cover-image')
    if cover_path:
        cover_art = PROJECT_ROOT / cover_path
    else:
        cover_art = PROJECT_ROOT / "assets" / "cover" / "book-cover-3.jpg"

    return {
        'title': book.get('title', 'Untitled'),
        'author': author,
        'year': metadata.get('copyright-year', ''),
        'publisher': metadata.get('publisher', ''),
        'cover_art': cover_art,
    }


class ChapterTimestamp(TypedDict):
    index: int
    title: str
    part: str | None
    file: str
    start_ms: int
    end_ms: int
    duration_ms: int
    duration_formatted: str


def format_duration(ms: int) -> str:
    """Format milliseconds as H:MM:SS or M:SS."""
    total_seconds = ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def load_book_config() -> dict:
    """Load and parse _quarto-manual.yml."""
    return load_quarto_config(QUARTO_BOOK_YML)


def extract_chapters(config: dict) -> list[dict]:
    """
    Extract all chapters from the book config in order.

    Returns list of dicts with:
        - path: Path to the QMD file
        - title: Chapter title (from part or inferred from file)
        - part: Part name if applicable
        - index: Chapter number
    """
    chapters = []
    chapter_index = 0

    book = config.get('book', {})
    # Some configs use index-source to map index.qmd -> actual source file
    index_source = config.get('dih-render', {}).get('index-source')

    def resolve_path(path: str) -> str:
        if index_source and path == 'index.qmd':
            return index_source
        return path

    # Process main chapters
    for item in book.get('chapters', []):
        if isinstance(item, str):
            # Simple chapter reference
            chapter_index += 1
            chapters.append({
                'path': resolve_path(item),
                'title': None,  # Will be extracted from file
                'part': None,
                'index': chapter_index
            })
        elif isinstance(item, dict):
            if 'href' in item:
                # Chapter with explicit text/href
                chapter_index += 1
                chapters.append({
                    'path': resolve_path(item['href']),
                    'title': item.get('text'),
                    'part': None,
                    'index': chapter_index
                })
            elif 'part' in item:
                # Part with sub-chapters
                part_name = item['part']
                for sub_chapter in item.get('chapters', []):
                    chapter_index += 1
                    if isinstance(sub_chapter, str):
                        chapters.append({
                            'path': resolve_path(sub_chapter),
                            'title': None,
                            'part': part_name,
                            'index': chapter_index
                        })
                    elif isinstance(sub_chapter, dict) and 'href' in sub_chapter:
                        chapters.append({
                            'path': resolve_path(sub_chapter['href']),
                            'title': sub_chapter.get('text'),
                            'part': part_name,
                            'index': chapter_index
                        })

    # Process appendices
    for item in book.get('appendices', []):
        if isinstance(item, dict) and 'part' in item:
            part_name = item['part']
            for sub_chapter in item.get('chapters', []):
                chapter_index += 1
                if isinstance(sub_chapter, str):
                    chapters.append({
                        'path': resolve_path(sub_chapter),
                        'title': None,
                        'part': f"Appendix: {part_name}",
                        'index': chapter_index
                    })
                elif isinstance(sub_chapter, dict) and 'href' in sub_chapter:
                    chapters.append({
                        'path': resolve_path(sub_chapter['href']),
                        'title': sub_chapter.get('text'),
                        'part': f"Appendix: {part_name}",
                        'index': chapter_index
                    })

    return chapters


def extract_title_from_qmd(file_path: Path) -> str:
    """Extract title from QMD file's YAML frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            frontmatter = yaml_safe_load(match.group(1))
            if frontmatter and 'title' in frontmatter:
                return frontmatter['title']
    except Exception:
        pass

    # Fallback: use filename
    return file_path.stem.replace('-', ' ').replace('_', ' ').title()


def find_text_file(chapter: dict, title: str) -> Path | None:
    """
    Look for a pre-generated audiobook text file for this chapter.
    Returns the path if found, None otherwise.
    """
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')[:50]
    text_file = TEXT_DIR / f"{chapter['index']:03d}-{safe_title}.prepared.txt"
    if text_file.exists():
        return text_file

    # Fallback: match by chapter index prefix in case title changed
    for f in TEXT_DIR.glob(f"{chapter['index']:03d}-*.prepared.txt"):
        return f

    return None


def generate_chapter_audio(
    chapter: dict,
    voice: str = NARRATOR_VOICE,
    force: bool = False,
) -> Path | None:
    """
    Generate audio for a single chapter.

    Regenerates prepared text first (via subprocess), then converts to audio via TTS.

    Args:
        chapter: Chapter dict with path, title, part, index
        voice: TTS voice name
        force: Regenerate even if file exists

    Returns:
        Path to generated audio file, or None on error
    """
    qmd_path = PROJECT_ROOT / chapter['path']

    if not qmd_path.exists():
        print(f"  [SKIP] File not found: {qmd_path}")
        return None

    # Get or extract title
    title = chapter['title'] or extract_title_from_qmd(qmd_path)

    # Create output filename
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')[:50]
    output_filename = f"{chapter['index']:03d}-{safe_title}.wav"
    output_path = CHAPTER_AUDIO_DIR / output_filename

    # Skip if already exists (unless force)
    if output_path.exists() and not force:
        print(f"  [SKIP] Already exists: {output_path.name}")
        return output_path

    # Regenerate prepared text via subprocess (avoids API client conflicts)
    print(f"  Preparing text...")
    text_script = Path(__file__).parent / "generate_audiobook_text.py"
    result = subprocess.run(
        [sys.executable, "-u", str(text_script), "--chapter", str(chapter['index']), "--force"],
        cwd=str(PROJECT_ROOT),
    )
    if result.returncode != 0:
        print(f"  [ERROR] Text preparation failed (exit code {result.returncode})")
        return None

    # Find text chunk files (produced by generate_audiobook_text.py)
    text_file = find_text_file(chapter, title)
    if not text_file:
        print(f"  [SKIP] No text file found after preparation")
        return None

    chunk_dir = text_file.parent / "chunks" / text_file.stem
    chunk_files = sorted(chunk_dir.glob("chunk-*.txt")) if chunk_dir.exists() else []

    if not chunk_files:
        # Single chunk - use the main text file directly
        chunk_files = [text_file]

    print(f"  Generating audio for: {title} ({len(chunk_files)} text chunks)")
    CHAPTER_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio_chunk_dir = CHAPTER_AUDIO_DIR / "audio-chunks" / output_path.stem
    audio_chunk_dir.mkdir(parents=True, exist_ok=True)

    for i, chunk_file in enumerate(chunk_files):
        chunk_text = chunk_file.read_text(encoding='utf-8')
        audio_chunk_path = audio_chunk_dir / f"chunk-{i+1:02d}-of-{len(chunk_files):02d}.wav"

        if audio_chunk_path.exists():
            print(f"    [CACHED] audio chunk {i+1}/{len(chunk_files)} ({audio_chunk_path.stat().st_size:,} bytes)")
            continue

        print(f"    Chunk {i+1}/{len(chunk_files)} ({len(chunk_text):,} chars)")
        try:
            generate_speech(
                text=chunk_text,
                output_path=audio_chunk_path,
                voice_name=voice
            )
        except Exception as e:
            print(f"    [ERROR] Failed on chunk {i+1}: {e}")
            return None

    # Combine audio chunks into final chapter WAV
    audio_chunk_files = sorted(audio_chunk_dir.glob("chunk-*.wav"))
    if len(audio_chunk_files) == 1:
        # Single chunk - just copy
        import shutil
        shutil.copy2(audio_chunk_files[0], output_path)
    else:
        print(f"  Combining {len(audio_chunk_files)} audio chunks...")
        combined = AudioSegment.empty()
        for acf in audio_chunk_files:
            combined += AudioSegment.from_wav(str(acf))
        combined.export(str(output_path), format="wav")

    print(f"    [OK] Saved: {output_path.name}")
    return output_path


def combine_chapter_audio(
    chapter_files: list[Path],
    chapters: list[dict],
    output_path: Path,
) -> tuple[Path, list[ChapterTimestamp]]:
    """
    Combine individual chapter audio files into a single audiobook.

    Args:
        chapter_files: List of paths to chapter WAV files (in order)
        chapters: Chapter metadata dicts from extract_chapters()
        output_path: Path for combined output file

    Returns:
        Tuple of (mp3_path, list of ChapterTimestamp dicts)
    """
    print(f"\nCombining {len(chapter_files)} chapters into audiobook...")

    # Build lookup: chapter index -> metadata (parse "001-" prefix from filename)
    chapter_meta_by_index: dict[int, dict] = {}
    for ch in chapters:
        chapter_meta_by_index[ch['index']] = ch

    # Start with empty audio
    combined = AudioSegment.empty()
    timestamps: list[ChapterTimestamp] = []

    # Add 2 seconds of silence between chapters
    silence = AudioSegment.silent(duration=2000)
    current_position_ms = 0

    for i, chapter_file in enumerate(chapter_files):
        print(f"  Adding: {chapter_file.name}")

        chapter_audio = AudioSegment.from_wav(str(chapter_file))

        if i > 0:
            combined += silence
            current_position_ms += len(silence)

        start_ms = current_position_ms
        combined += chapter_audio
        end_ms = current_position_ms + len(chapter_audio)
        current_position_ms = end_ms
        duration_ms = len(chapter_audio)

        # Match metadata by parsing index prefix from filename (e.g. "001-Start-Here.wav")
        index_match = re.match(r'^(\d+)-', chapter_file.stem)
        chapter_index = int(index_match.group(1)) if index_match else i + 1
        meta = chapter_meta_by_index.get(chapter_index, {})

        title = meta.get('title') or chapter_file.stem.split('-', 1)[-1].replace('-', ' ')

        timestamps.append(ChapterTimestamp(
            index=chapter_index,
            title=title,
            part=meta.get('part'),
            file=chapter_file.name,
            start_ms=start_ms,
            end_ms=end_ms,
            duration_ms=duration_ms,
            duration_formatted=format_duration(duration_ms),
        ))

    # Export combined audio
    print(f"\nExporting combined audiobook...")

    # Export as MP3 for smaller file size
    mp3_path = output_path.with_suffix('.mp3')
    combined.export(str(mp3_path), format="mp3", bitrate="192k")
    print(f"  [OK] MP3: {mp3_path}")

    # Also export as WAV for highest quality
    wav_path = output_path.with_suffix('.wav')
    combined.export(str(wav_path), format="wav")
    print(f"  [OK] WAV: {wav_path}")

    # Print duration
    total_ms = len(combined)
    print(f"\nTotal duration: {format_duration(total_ms)}")

    return mp3_path, timestamps


def list_chapters(chapters: list[dict]):
    """Print a formatted list of all chapters."""
    print("\nBook Chapters:")
    print("=" * 80)

    current_part = None
    for ch in chapters:
        # Print part header if changed
        if ch['part'] != current_part:
            current_part = ch['part']
            if current_part:
                print(f"\n[{current_part}]")

        # Get title
        qmd_path = PROJECT_ROOT / ch['path']
        title = ch['title']
        if not title and qmd_path.exists():
            title = extract_title_from_qmd(qmd_path)
        title = title or ch['path']

        # Check if audio exists
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')[:50]
        audio_file = CHAPTER_AUDIO_DIR / f"{ch['index']:03d}-{safe_title}.wav"
        status = "[x]" if audio_file.exists() else "[ ]"

        print(f"  {status} {ch['index']:3d}. {title}")

    print("=" * 80)
    print(f"Total: {len(chapters)} chapters")


def update_manifest(timestamps: list[ChapterTimestamp], total_duration_ms: int):
    """Update audiobook/manifest.json with duration and timing data."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))

    # Build lookup by chapter index
    ts_by_index = {ts['index']: ts for ts in timestamps}

    for chapter in manifest.get('chapters', []):
        ts = ts_by_index.get(chapter['index'])
        if ts:
            chapter['duration_ms'] = ts['duration_ms']
            chapter['duration_formatted'] = ts['duration_formatted']
            chapter['audio_start_ms'] = ts['start_ms']
            chapter['audio_end_ms'] = ts['end_ms']
            chapter['audio_file'] = ts['file']

    manifest['total_duration_ms'] = total_duration_ms
    manifest['total_duration_formatted'] = format_duration(total_duration_ms)

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"  [OK] Updated manifest: {MANIFEST_PATH}")


def tag_mp3(mp3_path: Path, timestamps: list[ChapterTimestamp], book_meta: dict):
    """Embed ID3v2.4 tags with chapter markers and cover art into the combined MP3."""
    from mutagen.mp3 import MP3
    from mutagen.id3 import (
        ID3, TIT2, TPE1, TALB, TCON, TDRC, TPUB, APIC, CHAP, CTOC, CTOCFlags,
    )

    print(f"\nTagging MP3 with metadata and chapter markers...")

    audio = MP3(str(mp3_path))
    if audio.tags is None:
        audio.add_tags()
    tag = audio.tags

    # Basic metadata
    tag.add(TIT2(encoding=3, text=[book_meta['title']]))
    tag.add(TPE1(encoding=3, text=[book_meta['author']]))
    tag.add(TALB(encoding=3, text=[book_meta['title']]))
    tag.add(TCON(encoding=3, text=["Audiobook"]))
    tag.add(TDRC(encoding=3, text=[book_meta['year']]))
    tag.add(TPUB(encoding=3, text=[book_meta['publisher']]))

    # Cover art
    cover_art: Path = book_meta['cover_art']
    if cover_art.exists():
        cover_data = cover_art.read_bytes()
        mime = 'image/png' if cover_art.suffix.lower() == '.png' else 'image/jpeg'
        tag.add(APIC(
            encoding=3,
            mime=mime,
            type=3,  # Front cover
            desc='Cover',
            data=cover_data,
        ))
        print(f"  [OK] Embedded cover art ({len(cover_data):,} bytes)")

    # Chapter markers (CHAP frames)
    chapter_ids = []
    for ts in timestamps:
        element_id = f"chp{ts['index']:02d}"
        chapter_ids.append(element_id)

        tag.add(CHAP(
            element_id=element_id,
            start_time=ts['start_ms'],
            end_time=ts['end_ms'],
            start_offset=0xFFFFFFFF,  # Not used
            end_offset=0xFFFFFFFF,    # Not used
            sub_frames=[
                TIT2(encoding=3, text=[ts['title']]),
            ],
        ))

    # Table of contents (CTOC frame)
    tag.add(CTOC(
        element_id="toc",
        flags=CTOCFlags.TOP_LEVEL | CTOCFlags.ORDERED,
        child_element_ids=chapter_ids,
        sub_frames=[
            TIT2(encoding=3, text=["Table of Contents"]),
        ],
    ))

    audio.save()
    print(f"  [OK] Tagged {len(timestamps)} chapters in {mp3_path.name}")


def export_m4b(mp3_path: Path, timestamps: list[ChapterTimestamp], book_meta: dict):
    """Export M4B audiobook with chapter metadata using ffmpeg."""
    m4b_path = mp3_path.with_suffix('.m4b')
    metadata_path = mp3_path.with_suffix('.ffmetadata')

    print(f"\nExporting M4B audiobook...")

    # Write ffmetadata file with chapter entries
    lines = [";FFMETADATA1"]
    lines.append(f"title={book_meta['title']}")
    lines.append(f"artist={book_meta['author']}")
    lines.append(f"album={book_meta['title']}")
    lines.append(f"genre=Audiobook")
    lines.append(f"date={book_meta['year']}")
    lines.append("")

    for ts in timestamps:
        lines.append("[CHAPTER]")
        lines.append("TIMEBASE=1/1000")
        lines.append(f"START={ts['start_ms']}")
        lines.append(f"END={ts['end_ms']}")
        lines.append(f"title={ts['title']}")
        lines.append("")

    metadata_path.write_text('\n'.join(lines), encoding='utf-8')

    # Build ffmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-i", str(mp3_path),
        "-i", str(metadata_path),
    ]

    # Add cover art if available
    cover_art: Path = book_meta['cover_art']
    if cover_art.exists():
        cmd.extend(["-i", str(cover_art)])
        cmd.extend([
            "-map", "0:a",           # Audio from MP3
            "-map", "2:v",           # Cover art
            "-disposition:v:0", "attached_pic",
        ])
    else:
        cmd.extend(["-map", "0:a"])

    cmd.extend([
        "-map_metadata", "1",    # Metadata from ffmetadata file
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "mp4",
        str(m4b_path),
    ])

    print(f"  Running ffmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] ffmpeg failed:\n{result.stderr}")
        metadata_path.unlink(missing_ok=True)
        return

    # Clean up temp metadata file
    metadata_path.unlink(missing_ok=True)

    m4b_size = m4b_path.stat().st_size
    print(f"  [OK] M4B: {m4b_path} ({m4b_size / 1024 / 1024:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate audiobook from Quarto book chapters"
    )
    parser.add_argument(
        "--chapter", "-c",
        type=int,
        help="Generate only specific chapter number"
    )
    parser.add_argument(
        "--voice", "-v",
        default=NARRATOR_VOICE,
        choices=AVAILABLE_VOICES,
        help=f"TTS voice (default: {NARRATOR_VOICE})"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all chapters and exit"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Regenerate audio even if files exist"
    )
    parser.add_argument(
        "--no-combine",
        action="store_true",
        help="Skip combining chapters into single audiobook"
    )
    parser.add_argument(
        "--start",
        type=int,
        help="Start from chapter number (inclusive)"
    )
    parser.add_argument(
        "--end",
        type=int,
        help="End at chapter number (inclusive)"
    )
    args = parser.parse_args()

    # Load book config
    print("Loading book configuration...")
    config = load_book_config()
    chapters = extract_chapters(config)
    print(f"Found {len(chapters)} chapters")

    # List mode
    if args.list:
        list_chapters(chapters)
        return

    # Filter chapters if specified
    if args.chapter:
        chapters = [ch for ch in chapters if ch['index'] == args.chapter]
        if not chapters:
            print(f"Error: Chapter {args.chapter} not found")
            return
    elif args.start or args.end:
        start = args.start or 1
        end = args.end or len(chapters)
        chapters = [ch for ch in chapters if start <= ch['index'] <= end]

    print(f"\nGenerating audio for {len(chapters)} chapter(s)...")
    print(f"Voice: {args.voice}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    # Generate chapter audio
    generated_files = []
    for chapter in chapters:
        qmd_path = PROJECT_ROOT / chapter['path']
        title = chapter['title'] or (extract_title_from_qmd(qmd_path) if qmd_path.exists() else chapter['path'])

        print(f"\n[{chapter['index']}/{len(chapters)}] {title}")

        audio_path = generate_chapter_audio(chapter, voice=args.voice, force=args.force)
        if audio_path:
            generated_files.append(audio_path)

    print(f"\n{'=' * 60}")
    print(f"Generated {len(generated_files)} audio files")

    # Combine into single audiobook
    if not args.no_combine and len(generated_files) > 1:
        # Get all chapter files in order (including previously generated)
        all_chapter_files = sorted(CHAPTER_AUDIO_DIR.glob("*.wav"))

        if all_chapter_files:
            # Reload full config for metadata matching
            full_config = load_book_config()
            all_chapters = extract_chapters(full_config)
            book_meta = extract_book_metadata(full_config)

            combined_path = OUTPUT_DIR / "How-to-End-War-and-Disease-Audiobook"
            mp3_path, timestamps = combine_chapter_audio(all_chapter_files, all_chapters, combined_path)

            total_duration_ms = sum(ts['duration_ms'] for ts in timestamps)

            update_manifest(timestamps, total_duration_ms)
            tag_mp3(mp3_path, timestamps, book_meta)
            export_m4b(mp3_path, timestamps, book_meta)

    print("\nDone!")


if __name__ == "__main__":
    main()
