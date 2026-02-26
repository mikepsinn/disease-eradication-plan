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
import os
import re
import hashlib
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TypedDict

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

from pydub import AudioSegment

# Add scripts directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))
# Add project root to path for dih_models imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.tts import generate_speech, AVAILABLE_VOICES, DEFAULT_VOICE
from dih_models.yaml_utils import load_quarto_config
from lib.audiobook_common import (
    PROJECT_ROOT, AUDIOBOOK_DIR, CHAPTER_AUDIO_DIR,
    DEFAULT_CONFIG_PATH, extract_chapters, extract_title_from_qmd, safe_filename,
    chapter_slug, find_prepared_text, find_chapter_audio, find_podcast_image,
    AudiobookPaths, config_name_from_path, get_paths,
)
from lib.audiobook_manifest import read_manifest, write_manifest, update_chapter_fields
from lib.retry import RateLimiter

# TTS parallelization: Gemini TTS allows concurrent requests.
# Conservative limit; increase if your quota allows.
TTS_PARALLEL_WORKERS = 4
tts_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

# Voice for narration (Kore + dinner-party energy, winner from A/B testing)
NARRATOR_VOICE = DEFAULT_VOICE


def extract_book_metadata(config: dict) -> dict:
    """Extract book metadata (title, author, year, publisher, cover, etc.) from quarto config."""
    book = config.get('book')
    if not book:
        raise ValueError("Quarto config missing required 'book' section")
    metadata = config.get('metadata', {})

    # Author: first entry in book.author list, or fallback to metadata.creator
    authors = book.get('author', [])
    if isinstance(authors, list) and authors:
        first = authors[0]
        author = first.get('name') if isinstance(first, dict) else str(first)
        email = first.get('email', '') if isinstance(first, dict) else ''
    else:
        author = metadata.get('creator')
        email = metadata.get('author-email', '')

    # Cover art: portrait (for MP3/M4B embedding) and square (for podcast RSS)
    cover_path = config.get('format', {}).get('epub', {}).get('epub-cover-image')
    if cover_path:
        cover_art = PROJECT_ROOT / cover_path
    else:
        cover_art = PROJECT_ROOT / "assets" / "cover" / "book-cover-3.jpg"
    if not cover_art.exists():
        raise FileNotFoundError(f"Cover art not found: {cover_art}")

    # Square podcast cover (1400x1400+ required by Apple/Spotify)
    podcast_cover = PROJECT_ROOT / "assets" / "cover" / "podcast-cover.jpg"
    if not podcast_cover.exists():
        raise FileNotFoundError(
            f"Podcast cover not found: {podcast_cover}. "
            f"Generate a 1400x1400+ square cover (Apple/Spotify requirement)."
        )

    # Site URL from website or book config
    site_url = (
        config.get('website', {}).get('site-url')
        or book.get('site-url', '')
    )

    title = book.get('title')
    year = metadata.get('copyright-year')
    publisher = metadata.get('publisher')

    missing = []
    if not title:
        missing.append('book.title')
    if not author:
        missing.append('book.author (or metadata.creator)')
    if not site_url:
        missing.append('book.site-url (or website.site-url)')
    if not year:
        missing.append('metadata.copyright-year')
    if not publisher:
        missing.append('metadata.publisher')
    if missing:
        raise ValueError(f"Quarto config missing required fields: {', '.join(missing)}")

    description = book.get('description')
    if not description:
        missing.append('book.description')
    if not email:
        missing.append('book.author[0].email (or metadata.author-email)')

    # Podcast-specific overrides from dih-podcast config section
    podcast = config.get('dih-podcast', {})
    podcast_author = podcast.get('author', author)
    podcast_description = podcast.get('podcast-description', '')
    podcast_description_suffix = podcast.get('description-suffix', '')

    return {
        'title': title,
        'subtitle': book.get('subtitle', ''),
        'description': description or '',
        'author': author,
        'email': email or '',
        'year': year,
        'publisher': publisher,
        'cover_art': cover_art,
        'podcast_cover': podcast_cover,
        'site_url': site_url.rstrip('/'),
        'narrator': 'WISHONIA',
        'podcast_author': podcast_author,
        'podcast_description': podcast_description,
        'podcast_description_suffix': podcast_description_suffix,
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


def load_book_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """Load and parse a Quarto book config."""
    return load_quarto_config(config_path)


def generate_chapter_audio(
    chapter: dict,
    voice: str = NARRATOR_VOICE,
    force: bool = False,
    paths: AudiobookPaths | None = None,
    config_path: Path = DEFAULT_CONFIG_PATH,
) -> tuple[Path | None, bool]:
    """
    Generate audio for a single chapter.

    Regenerates prepared text first (via subprocess), then converts to audio via TTS.
    Uses content hashes to detect stale audio chunks when source text changes.

    Args:
        chapter: Chapter dict with path, title, part, index
        voice: TTS voice name
        force: Regenerate even if file exists
        paths: Config-specific output paths
        config_path: Quarto config path (passed to text subprocess)

    Returns:
        Tuple of (path to generated audio file or None, whether audio was regenerated)
    """
    chapters_dir = paths.chapters if paths else CHAPTER_AUDIO_DIR
    qmd_path = PROJECT_ROOT / chapter['path']

    if not qmd_path.exists():
        print(f"  [SKIP] File not found: {qmd_path}")
        return None, False

    # Get or extract title
    title = chapter['title'] or extract_title_from_qmd(qmd_path)

    # Create output filename using QMD slug (stable across title renames)
    slug = chapter_slug(chapter)
    output_filename = f"{slug}.wav"
    output_path = chapters_dir / output_filename

    # Regenerate prepared text via subprocess (has its own hash-based caching)
    print(f"  Preparing text...")
    text_script = Path(__file__).parent / "generate_audiobook_text.py"
    text_cmd = [sys.executable, "-u", str(text_script), "--chapter", str(chapter['index']),
                "--config", str(config_path)]
    if force:
        text_cmd.append("--force")
    result = subprocess.run(text_cmd, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        print(f"  [ERROR] Text preparation failed (exit code {result.returncode})")
        return None, False

    # Find text chunk files (produced by generate_audiobook_text.py)
    text_file = find_prepared_text(chapter, paths=paths)
    if not text_file:
        print(f"  [SKIP] No text file found after preparation")
        return None, False

    # Chunks are in the adjacent narration-txt-chunks/ dir, not nested under narration-txt-chapters/
    chunk_dir = text_file.parent.parent / "narration-txt-chunks" / text_file.stem
    chunk_files = sorted(chunk_dir.glob("chunk-*.txt")) if chunk_dir.exists() else []

    if not chunk_files:
        # Single chunk - use the main text file directly
        chunk_files = [text_file]

    chapters_dir.mkdir(parents=True, exist_ok=True)
    audio_chunk_dir = chapters_dir / "audio-chunks" / output_path.stem
    audio_chunk_dir.mkdir(parents=True, exist_ok=True)

    # Clean stale audio chunks from previous runs with different chunk counts.
    # e.g. old run had 10 chunks (chunk-*-of-10.wav), new run has 9. Without
    # cleanup the combine step globs all .wav files and double-concatenates.
    expected_tag = f"-of-{len(chunk_files):02d}"
    for old_file in list(audio_chunk_dir.glob("chunk-*.wav")):
        if expected_tag not in old_file.stem:
            print(f"    [CLEAN] Removing stale chunk: {old_file.name}")
            old_file.unlink()
            old_file.with_suffix('.texthash').unlink(missing_ok=True)

    # Build work items, skipping cached chunks whose source text hasn't changed
    work_items = []
    for i, chunk_file in enumerate(chunk_files):
        audio_chunk_path = audio_chunk_dir / f"chunk-{i+1:02d}-of-{len(chunk_files):02d}.wav"
        hash_path = audio_chunk_path.with_suffix('.texthash')

        if audio_chunk_path.exists():
            # Check if source text has changed since this audio was generated
            text_content = chunk_file.read_text(encoding='utf-8')
            text_hash = hashlib.sha256(text_content.encode('utf-8')).hexdigest()[:16]
            old_hash = hash_path.read_text(encoding='utf-8').strip() if hash_path.exists() else ''

            if old_hash == text_hash:
                print(f"    [CACHED] audio chunk {i+1}/{len(chunk_files)} ({audio_chunk_path.stat().st_size:,} bytes)")
                continue
            else:
                print(f"    [STALE] audio chunk {i+1}/{len(chunk_files)} text changed ({old_hash or 'none'} -> {text_hash}), regenerating")
                audio_chunk_path.unlink()
                hash_path.unlink(missing_ok=True)

        work_items.append((i, chunk_file, audio_chunk_path))

    # If nothing to regenerate and chapter WAV exists, skip
    if not work_items and output_path.exists() and not force:
        print(f"  [SKIP] All audio chunks fresh, chapter WAV up to date: {output_path.name}")
        return output_path, False

    # If force and no stale chunks detected, still regenerate all
    if force and not work_items:
        work_items = [
            (i, cf, audio_chunk_dir / f"chunk-{i+1:02d}-of-{len(chunk_files):02d}.wav")
            for i, cf in enumerate(chunk_files)
        ]

    print(f"  Generating audio for: {title} ({len(work_items)} of {len(chunk_files)} chunks to generate)")

    if work_items:
        def _generate_one(item):
            idx, cf, out_path = item
            chunk_text = cf.read_text(encoding='utf-8')
            label = f"chunk {idx+1}/{len(chunk_files)}"
            print(f"    [{label}] Starting ({len(chunk_text):,} chars)")
            tts_rate_limiter.acquire()
            generate_speech(text=chunk_text, output_path=out_path, voice_name=voice)
            # Write text hash sidecar so we can detect stale audio later
            text_hash = hashlib.sha256(chunk_text.encode('utf-8')).hexdigest()[:16]
            out_path.with_suffix('.texthash').write_text(text_hash, encoding='utf-8')
            print(f"    [{label}] Done")
            return idx

        workers = min(TTS_PARALLEL_WORKERS, len(work_items))
        print(f"  Generating {len(work_items)} audio chunks ({workers} parallel workers)...")
        errors = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_generate_one, item): item for item in work_items}
            for future in as_completed(futures):
                item = futures[future]
                try:
                    future.result()
                except Exception as e:
                    errors.append(f"chunk {item[0]+1}: {e}")
                    print(f"    [ERROR] Failed on chunk {item[0]+1}: {e}")
        if errors:
            print(f"  [ERROR] {len(errors)} chunk(s) failed")
            return None, False

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
    return output_path, True


def _get_wav_duration_ms(wav_path: Path) -> int:
    """Get WAV duration in milliseconds using ffprobe (no memory load)."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(wav_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # Fallback: load just enough to get duration
        audio = AudioSegment.from_wav(str(wav_path))
        return len(audio)
    return int(float(result.stdout.strip()) * 1000)


def combine_chapter_audio(
    chapters: list[dict],
    output_path: Path,
    paths: AudiobookPaths | None = None,
) -> tuple[Path, list[ChapterTimestamp]]:
    """
    Combine individual chapter audio files into a single audiobook.

    Uses ffmpeg concat demuxer to avoid loading all audio into memory
    (32+ chapters of WAV would exceed available RAM with pydub).

    Ordering comes from the config chapter list, not filename sorting.

    Args:
        chapters: Chapter metadata dicts from extract_chapters() (defines order)
        output_path: Path for combined output file
        paths: Config-specific audiobook paths

    Returns:
        Tuple of (mp3_path, list of ChapterTimestamp dicts)
    """
    # Resolve WAV files from config chapter order (not filesystem glob)
    chapter_files: list[tuple[dict, Path]] = []
    for ch in chapters:
        audio_path = find_chapter_audio(ch, paths=paths)
        if audio_path:
            chapter_files.append((ch, audio_path))

    if len(chapter_files) < 2:
        raise ValueError(f"Need at least 2 chapter WAVs to combine, found {len(chapter_files)}")

    print(f"\nCombining {len(chapter_files)} chapters into audiobook...")

    # Generate 2s silence file for inter-chapter gaps
    silence_path = output_path.parent / "_silence_2s.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", "2", str(silence_path)],
        capture_output=True,
    )

    # Build concat list and collect timestamps (using ffprobe, not memory)
    concat_file = output_path.parent / "_concat_chapters.txt"
    timestamps: list[ChapterTimestamp] = []
    current_position_ms = 0
    concat_lines = []

    for i, (ch, chapter_file) in enumerate(chapter_files):
        duration_ms = _get_wav_duration_ms(chapter_file)
        print(f"  Adding: {chapter_file.name} ({format_duration(duration_ms)})")

        if i > 0:
            concat_lines.append(f"file '{silence_path.as_posix()}'")
            current_position_ms += 2000

        concat_lines.append(f"file '{chapter_file.as_posix()}'")

        start_ms = current_position_ms
        end_ms = current_position_ms + duration_ms
        current_position_ms = end_ms

        timestamps.append(ChapterTimestamp(
            index=ch['index'],
            title=ch['title'],
            part=ch.get('part'),
            file=chapter_file.name,
            start_ms=start_ms,
            end_ms=end_ms,
            duration_ms=duration_ms,
            duration_formatted=format_duration(duration_ms),
        ))

    concat_file.write_text('\n'.join(concat_lines), encoding='utf-8')

    # Export as MP3 directly via ffmpeg (streaming, no memory spike)
    print(f"\nExporting combined audiobook...")
    mp3_path = output_path.with_suffix('.mp3')
    result = subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-codec:a", "libmp3lame", "-b:a", "192k",
        "-movflags", "+faststart",
        str(mp3_path),
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg MP3 export failed:\n{result.stderr[:500]}")
    mp3_size = mp3_path.stat().st_size / 1024 / 1024
    print(f"  [OK] MP3: {mp3_path.name} ({mp3_size:.1f} MB)")

    # Clean up temp files
    concat_file.unlink(missing_ok=True)
    silence_path.unlink(missing_ok=True)

    total_ms = current_position_ms
    print(f"\nTotal duration: {format_duration(total_ms)}")

    return mp3_path, timestamps


def list_chapters(chapters: list[dict], paths: AudiobookPaths | None = None):
    """Print a formatted list of all chapters."""
    chapters_dir = paths.chapters if paths else CHAPTER_AUDIO_DIR
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
        slug = chapter_slug(ch)
        audio_file = find_chapter_audio(ch, paths=paths)
        status = "[x]" if audio_file else "[ ]"

        print(f"  {status} {ch['index']:3d}. {title}")

    print("=" * 80)
    print(f"Total: {len(chapters)} chapters")


def update_manifest(timestamps: list[ChapterTimestamp], total_duration_ms: int, paths: AudiobookPaths | None = None):
    """Update manifest.json with duration and timing data."""
    for ts in timestamps:
        update_chapter_fields(
            ts['index'],
            paths=paths,
            duration_ms=ts['duration_ms'],
            duration_formatted=ts['duration_formatted'],
            audio_start_ms=ts['start_ms'],
            audio_end_ms=ts['end_ms'],
            audio_file=ts['file'],
        )

    manifest = read_manifest(paths)
    manifest['total_duration_ms'] = total_duration_ms
    manifest['total_duration_formatted'] = format_duration(total_duration_ms)
    write_manifest(manifest, paths)
    manifest_path = paths.manifest if paths else AUDIOBOOK_DIR / "manifest.json"
    print(f"  [OK] Updated manifest: {manifest_path.relative_to(PROJECT_ROOT)}")


def tag_mp3(mp3_path: Path, timestamps: list[ChapterTimestamp], book_meta: dict):
    """Embed ID3v2.4 tags with chapter markers and cover art into the combined MP3."""
    from mutagen.mp3 import MP3
    from mutagen.id3 import (  # pyright: ignore[reportPrivateImportUsage]
        ID3, TIT2, TPE1, TPE2, TALB, TCON, TDRC, TPUB, APIC, CHAP, CTOC, CTOCFlags,
        TXXX, TLAN, COMM,
    )

    print(f"\nTagging MP3 with metadata and chapter markers...")

    audio = MP3(str(mp3_path))
    if audio.tags is None:
        audio.add_tags()
    assert audio.tags is not None
    tag = audio.tags

    # Basic metadata
    tag.add(TIT2(encoding=3, text=[book_meta['title']]))
    tag.add(TPE1(encoding=3, text=[book_meta['author']]))
    tag.add(TPE2(encoding=3, text=[book_meta['author']]))  # Album artist
    tag.add(TALB(encoding=3, text=[book_meta['title']]))
    tag.add(TCON(encoding=3, text=["Audiobook"]))
    tag.add(TDRC(encoding=3, text=[book_meta['year']]))
    tag.add(TPUB(encoding=3, text=[book_meta['publisher']]))
    tag.add(TLAN(encoding=3, text=["eng"]))
    # Narrator (custom TXXX frame, recognized by Apple Books/Audible/Overcast)
    narrator = book_meta['narrator']
    tag.add(TXXX(encoding=3, desc='narrator', text=[narrator]))
    # Description
    if book_meta.get('description'):
        tag.add(COMM(encoding=3, lang='eng', desc='', text=[book_meta['description']]))

    # Cover art (validated in extract_book_metadata)
    cover_art: Path = book_meta['cover_art']
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

    # Add cover art (validated in extract_book_metadata)
    cover_art: Path = book_meta['cover_art']
    cmd.extend(["-i", str(cover_art)])
    cmd.extend([
        "-map", "0:a",           # Audio from MP3
        "-map", "2:v",           # Cover art (keep as JPEG, don't re-encode)
        "-c:v", "copy",
        "-disposition:v:0", "attached_pic",
    ])

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
        metadata_path.unlink(missing_ok=True)
        raise RuntimeError(f"M4B export failed:\n{result.stderr[:500]}")

    # Clean up temp metadata file
    metadata_path.unlink(missing_ok=True)

    m4b_size = m4b_path.stat().st_size
    print(f"  [OK] M4B: {m4b_path} ({m4b_size / 1024 / 1024:.1f} MB)")


def normalize_loudness(wav_path: Path, target_lufs: float = -16.0) -> Path:
    """Normalize audio loudness using ffmpeg's loudnorm filter (two-pass).

    Args:
        wav_path: Input WAV file.
        target_lufs: Target integrated loudness (default -16 LUFS for streaming;
                     use -23 for Audible/broadcast).

    Returns:
        Path to normalized WAV (overwrites input).
    """
    temp_path = wav_path.with_suffix('.norm.wav')

    # Pass 1: Measure loudness
    null_out = "NUL" if sys.platform == "win32" else "/dev/null"
    measure_cmd = [
        "ffmpeg", "-y", "-i", str(wav_path),
        "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", null_out
    ]
    result = subprocess.run(measure_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [WARN] Loudness measurement failed, skipping normalization")
        return wav_path

    # Parse measured values from stderr
    import json as _json
    stderr = result.stderr
    json_start = stderr.rfind('{')
    json_end = stderr.rfind('}') + 1
    if json_start < 0:
        raise RuntimeError(
            f"Could not parse loudnorm JSON from ffmpeg stderr for {wav_path.name}. "
            f"Stderr: {stderr[-500:]}"
        )

    stats = _json.loads(stderr[json_start:json_end])
    required_keys = ['input_i', 'input_tp', 'input_lra', 'input_thresh', 'target_offset']
    missing_keys = [k for k in required_keys if k not in stats]
    if missing_keys:
        raise RuntimeError(
            f"ffmpeg loudnorm missing keys {missing_keys} for {wav_path.name}. "
            f"Got: {stats}"
        )
    measured_i = stats['input_i']
    measured_tp = stats['input_tp']
    measured_lra = stats['input_lra']
    measured_thresh = stats['input_thresh']
    target_offset = stats['target_offset']

    print(f"  Loudness: {measured_i} LUFS (target: {target_lufs} LUFS)")

    # Skip if already within 0.5 LUFS of target (avoids quality loss from re-normalizing)
    if abs(float(measured_i) - target_lufs) < 0.5:
        print(f"  [SKIP] Already at target loudness ({measured_i} LUFS)")
        return wav_path

    # Pass 2: Apply normalization with measured values
    norm_cmd = [
        "ffmpeg", "-y", "-i", str(wav_path),
        "-af", (
            f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11:"
            f"measured_I={measured_i}:measured_TP={measured_tp}:"
            f"measured_LRA={measured_lra}:measured_thresh={measured_thresh}:"
            f"offset={target_offset}:linear=true"
        ),
        str(temp_path),
    ]
    result = subprocess.run(norm_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [WARN] Loudness normalization failed: {result.stderr[:200]}")
        temp_path.unlink(missing_ok=True)
        return wav_path

    # Replace original with normalized version
    import shutil as _shutil
    _shutil.move(str(temp_path), str(wav_path))
    print(f"  [OK] Normalized to {target_lufs} LUFS")
    return wav_path


def export_chapter_mp3s(
    chapters: list[dict],
    book_meta: dict,
    paths: AudiobookPaths | None = None,
) -> list[Path]:
    """Export each chapter WAV as a tagged MP3 for per-chapter distribution.

    Iterates chapters in config order. Each MP3 gets ID3 tags: title, artist,
    album, narrator, track number, cover art, and genre.
    """
    from mutagen.mp3 import MP3
    from mutagen.id3 import (  # pyright: ignore[reportPrivateImportUsage]
        TIT2, TPE1, TPE2, TALB, TCON, TDRC, TPUB, APIC, TRCK, TLAN, TXXX, COMM,
    )

    mp3_dir = paths.root / "mp3" if paths else AUDIOBOOK_DIR / "mp3"
    mp3_dir.mkdir(parents=True, exist_ok=True)

    # Load cover art once (validated in extract_book_metadata)
    cover_art: Path = book_meta['cover_art']
    cover_data = cover_art.read_bytes()
    cover_mime = 'image/png' if cover_art.suffix.lower() == '.png' else 'image/jpeg'

    mp3_files = []
    narrator = book_meta['narrator']
    total_chapters = len(chapters)

    for track_num, ch in enumerate(chapters, 1):
        chapter_file = find_chapter_audio(ch, paths=paths)
        if not chapter_file:
            print(f"  [SKIP] No WAV for chapter {ch['index']}: {ch['title']}")
            continue

        mp3_path = mp3_dir / chapter_file.with_suffix('.mp3').name

        # Convert WAV to MP3 via pydub
        audio = AudioSegment.from_wav(str(chapter_file))
        audio.export(str(mp3_path), format="mp3", bitrate="192k")

        # Tag with ID3
        mp3 = MP3(str(mp3_path))
        if mp3.tags is None:
            mp3.add_tags()
        assert mp3.tags is not None
        tag = mp3.tags

        tag.add(TIT2(encoding=3, text=[ch['title']]))
        tag.add(TPE1(encoding=3, text=[book_meta['author']]))
        tag.add(TPE2(encoding=3, text=[book_meta['author']]))
        tag.add(TALB(encoding=3, text=[book_meta['title']]))
        tag.add(TCON(encoding=3, text=["Audiobook"]))
        tag.add(TDRC(encoding=3, text=[book_meta['year']]))
        tag.add(TPUB(encoding=3, text=[book_meta['publisher']]))
        tag.add(TRCK(encoding=3, text=[f"{track_num}/{total_chapters}"]))
        tag.add(TLAN(encoding=3, text=["eng"]))
        tag.add(TXXX(encoding=3, desc='narrator', text=[narrator]))
        if book_meta.get('description'):
            tag.add(COMM(encoding=3, lang='eng', desc='', text=[book_meta['description']]))

        tag.add(APIC(encoding=3, mime=cover_mime, type=3, desc='Cover', data=cover_data))

        mp3.save()
        size_mb = mp3_path.stat().st_size / 1024 / 1024
        print(f"  [OK] {mp3_path.name} ({size_mb:.1f} MB)")
        mp3_files.append(mp3_path)

    print(f"  Exported {len(mp3_files)} chapter MP3s to {mp3_dir}")
    return mp3_files


def generate_podcast_rss(
    chapter_mp3s: list[Path],
    chapters: list[dict],
    timestamps: list[ChapterTimestamp],
    book_meta: dict,
    paths: AudiobookPaths | None = None,
) -> Path:
    """Generate a podcast RSS 2.0 feed with iTunes namespace tags.

    MP3 URLs are constructed relative to the site URL so the feed works
    when deployed to the book's Netlify site.
    """
    from xml.sax.saxutils import escape

    rss_dir = paths.root if paths else AUDIOBOOK_DIR
    rss_path = rss_dir / "feed.xml"

    site_url = book_meta.get('site_url', 'https://manual.WarOnDisease.org')
    # MP3s served from R2 (falls back to site URL if R2_PUBLIC_URL not set)
    cdn_url = os.environ.get('R2_PUBLIC_URL', site_url).rstrip('/')
    mp3_base = paths.root.relative_to(PROJECT_ROOT) if paths else Path("assets/audiobook")
    mp3_url_base = f"{cdn_url}/{mp3_base.as_posix()}/mp3"

    # Build timestamp lookup
    ts_by_index = {ts['index']: ts for ts in timestamps}

    title = escape(book_meta['title'])
    author = escape(book_meta.get('podcast_author', book_meta['author']))
    description = escape(book_meta.get('podcast_description') or book_meta['description'])
    desc_suffix = book_meta.get('podcast_description_suffix', '')
    narrator = escape(book_meta['narrator'])
    podcast_cover: Path = book_meta['podcast_cover']
    cover_filename = podcast_cover.relative_to(PROJECT_ROOT).as_posix()
    cover_url = f"{cdn_url}/{cover_filename}"

    from datetime import datetime, timezone, timedelta
    # Each chapter gets a pubDate 1 day apart so podcast apps sort them correctly
    base_date = datetime.now(timezone.utc)

    # Build MP3 lookup by slug for matching with timestamps
    mp3_by_slug = {mp3.stem: mp3 for mp3 in chapter_mp3s}

    # Build per-episode lookups from chapter list (keyed by slug)
    ep_image_urls: dict[str, str] = {}
    ep_descriptions: dict[str, str] = {}
    for ch in chapters:
        s = chapter_slug(ch)
        img = find_podcast_image(ch, paths=paths)
        if img:
            img_rel = img.relative_to(PROJECT_ROOT).as_posix()
            ep_image_urls[s] = f"{cdn_url}/{img_rel}"
        if ch.get('description'):
            ep_descriptions[s] = ch['description']

    items = []
    total_eps = len(chapter_mp3s)
    for ep_num, ts in enumerate(timestamps):
        slug = Path(ts['file']).stem  # WAV slug -> MP3 slug
        mp3_path = mp3_by_slug.get(slug)
        if not mp3_path:
            print(f"  [WARN] No MP3 for timestamp entry: {ts['file']}")
            continue

        ch_title = escape(ts['title'])
        part = ts.get('part', '')
        ep_title = f"{ch_title}" if not part else f"{part}: {ch_title}"

        # Use QMD description if available, fall back to generic; append CTA suffix
        ep_desc = ep_descriptions.get(slug, f"Chapter {ep_num + 1} of {title}")
        if desc_suffix:
            ep_desc = f"{ep_desc}\n\n{desc_suffix}"

        duration_fmt = ts['duration_formatted']
        file_size = mp3_path.stat().st_size
        mp3_url = f"{mp3_url_base}/{mp3_path.name}"
        pub_date = (base_date - timedelta(days=total_eps - ep_num)).strftime(
            "%a, %d %b %Y %H:%M:%S +0000"
        )

        ep_img = ep_image_urls.get(slug)
        image_tag = f'\n      <itunes:image href="{escape(ep_img)}"/>' if ep_img else ''

        items.append(f"""    <item>
      <title>{escape(ep_title)}</title>
      <enclosure url="{escape(mp3_url)}" length="{file_size}" type="audio/mpeg"/>
      <pubDate>{pub_date}</pubDate>
      <itunes:duration>{duration_fmt}</itunes:duration>
      <itunes:episode>{ep_num + 1}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <guid isPermaLink="false">chapter-{slug}</guid>
      <description>{escape(ep_desc)}</description>{image_tag}
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:podcast="https://podcastindex.org/namespace/1.0"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{title}</title>
    <link>{escape(site_url)}</link>
    <description>{description + chr(10) + chr(10) + escape(desc_suffix) if desc_suffix else description}</description>
    <language>en-us</language>
    <itunes:author>{author}</itunes:author>
    <itunes:owner>
      <itunes:name>{escape(book_meta['author'])}</itunes:name>
      <itunes:email>{escape(book_meta['email'])}</itunes:email>
    </itunes:owner>
    <itunes:image href="{escape(cover_url)}"/>
    <itunes:category text="Society &amp; Culture"/>
    <itunes:category text="Science">
      <itunes:category text="Medicine"/>
    </itunes:category>
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>serial</itunes:type>
    <pubDate>{base_date.strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
    <podcast:medium>audiobook</podcast:medium>
    <atom:link href="{escape(cdn_url)}/{mp3_base.as_posix()}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""

    rss_path.write_text(feed, encoding='utf-8')
    print(f"\n  [OK] Podcast RSS: {rss_path.relative_to(PROJECT_ROOT)}")
    print(f"  Feed URL: {site_url}/{mp3_base.as_posix()}/feed.xml")
    return rss_path


def _run_alignment(chapter: dict, audio_path: Path, title: str, force: bool = False, paths: AudiobookPaths | None = None, audio_changed: bool = False):
    """Run forced alignment and generate subtitles for a chapter.

    Gracefully skips if stable-ts is not installed.
    """
    from lib.audiobook_common import ALIGNMENT_DIR, SUBTITLES_DIR
    alignment_dir = paths.alignment if paths else ALIGNMENT_DIR
    subtitles_dir = paths.subtitles if paths else SUBTITLES_DIR

    slug = chapter_slug(chapter)
    alignment_path = alignment_dir / f"{slug}.alignment.json"
    vtt_path = subtitles_dir / f"{slug}.vtt"

    if alignment_path.exists() and not force and not audio_changed:
        print(f"  [SKIP] Alignment exists: {alignment_path.name}")
        return
    if audio_changed and alignment_path.exists():
        print(f"  [STALE] Audio changed, regenerating alignment...")

    text_file = find_prepared_text(chapter, paths=paths)
    if not text_file:
        print(f"  [SKIP] No text file for alignment")
        return

    try:
        from lib.alignment import align_chapter, generate_vtt, generate_srt
    except ImportError as e:
        print(f"  [SKIP] {e}")
        return

    srt_path = subtitles_dir / f"{slug}.srt"

    alignment_dir.mkdir(parents=True, exist_ok=True)
    subtitles_dir.mkdir(parents=True, exist_ok=True)
    words = align_chapter(audio_path, text_file, alignment_path, chapter=chapter)
    generate_vtt(words, vtt_path)
    generate_srt(words, srt_path)

    update_chapter_fields(
        chapter['index'],
        paths=paths,
        alignment_file=str(alignment_path.relative_to(PROJECT_ROOT)),
        subtitle_file=str(vtt_path.relative_to(PROJECT_ROOT)),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate audiobook from Quarto book chapters"
    )
    parser.add_argument(
        "--config", "-cfg",
        default=str(DEFAULT_CONFIG_PATH),
        help=f"Quarto config YAML (default: {DEFAULT_CONFIG_PATH.name})"
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
        "--no-align",
        action="store_true",
        help="Skip forced alignment and subtitle generation"
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

    # Resolve config and derive paths
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

    # Load book config
    print(f"Loading book configuration: {config_path.name} (output: assets/audiobook/{cfg_name}/)")
    config = load_book_config(config_path)
    chapters = extract_chapters(config)
    print(f"Found {len(chapters)} chapters")

    # List mode
    if args.list:
        list_chapters(chapters, paths=paths)
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
    print(f"Output: {paths.root.relative_to(PROJECT_ROOT)}")
    print()

    # Generate chapter audio
    generated_files = []
    for chapter in chapters:
        qmd_path = PROJECT_ROOT / chapter['path']
        title = chapter['title'] or (extract_title_from_qmd(qmd_path) if qmd_path.exists() else chapter['path'])

        print(f"\n[{chapter['index']}/{len(chapters)}] {title}")

        audio_path, audio_changed = generate_chapter_audio(chapter, voice=args.voice, force=args.force, paths=paths, config_path=config_path)
        if audio_path:
            generated_files.append(audio_path)

            # Run forced alignment + subtitle generation
            if not args.no_align:
                _run_alignment(chapter, audio_path, title, force=args.force, paths=paths, audio_changed=audio_changed)

    print(f"\n{'=' * 60}")
    print(f"Generated {len(generated_files)} audio files")

    # Normalize loudness on each generated chapter WAV
    if generated_files:
        print(f"\nNormalizing loudness (-16 LUFS)...")
        for wav_file in generated_files:
            normalize_loudness(wav_file, target_lufs=-16.0)

    # Combine into single audiobook + export per-chapter MP3s + podcast RSS
    # Uses config chapter list for ordering (not filesystem glob)
    if not args.no_combine:
        full_config = load_book_config(config_path)
        all_chapters = extract_chapters(full_config)
        book_meta = extract_book_metadata(full_config)

        # Count how many chapters have audio on disk
        chapters_with_audio = [ch for ch in all_chapters if find_chapter_audio(ch, paths=paths)]
        if len(chapters_with_audio) > 1:
            combined_path = paths.root / f"{safe_filename(book_meta['title'], max_len=80)}-Audiobook"
            mp3_path, timestamps = combine_chapter_audio(all_chapters, combined_path, paths=paths)

            total_duration_ms = sum(ts['duration_ms'] for ts in timestamps)

            update_manifest(timestamps, total_duration_ms, paths=paths)
            tag_mp3(mp3_path, timestamps, book_meta)
            export_m4b(mp3_path, timestamps, book_meta)

            # Export per-chapter MP3s with ID3 tags
            chapter_mp3s = export_chapter_mp3s(all_chapters, book_meta, paths=paths)

            # Generate podcast RSS feed
            generate_podcast_rss(chapter_mp3s, all_chapters, timestamps, book_meta, paths=paths)

    print("\nDone!")


if __name__ == "__main__":
    main()
