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
    python scripts/generate_audiobook.py --no-sync-each-chapter  # Disable immediate R2 sync after each chapter
"""
import sys
import os
import re
import json
import time
import atexit
import hashlib
import argparse
import subprocess
import contextlib
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
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
    find_youtube_thumbnail,
    AudiobookPaths, config_name_from_path, get_paths,
    mp3_content_hash, find_current_mp3, parse_hashed_mp3, PODCAST_HASH_RE,
)
from lib.audiobook_manifest import read_manifest, write_manifest, update_chapter_fields
from lib.build_logger import BuildLogger
from lib.retry import RateLimiter
from lib.script_lock import acquire_script_lock, ScriptLockError

# TTS parallelization: Gemini TTS allows concurrent requests.
# Conservative limit; increase if your quota allows.
TTS_PARALLEL_WORKERS = 4
tts_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


# Per-chapter sync defaults to concise mode to avoid log spam.
SYNC_VERBOSE = _env_flag("AUDIOBOOK_SYNC_VERBOSE", False)

# Silence detection: trim audio chunks with silence longer than this threshold.
# Gemini TTS occasionally produces WAVs with enormous silent tails (e.g. 10 min).
# Natural speech pauses are 1-3s; anything beyond 5s is a TTS bug.
MAX_SILENCE_SECONDS = 5

# Voice for narration (Kore + dinner-party energy, winner from A/B testing)
NARRATOR_VOICE = DEFAULT_VOICE

# Podcast intro/outro assets
THEME_SONG_PATH = PROJECT_ROOT / "assets" / "music" / "podcast-theme-song.mp3"
OUTRO_QMD_PATH = PROJECT_ROOT / "knowledge" / "appendix" / "podcast-outro.qmd"


def _retry_fs_op(op, label: str = "", retries: int = 8, delay: float = 1.0):
    """Retry a filesystem operation on Windows PermissionError (stale handles)."""
    for attempt in range(retries):
        try:
            return op()
        except PermissionError:
            if attempt < retries - 1:
                print(f"  [retry {attempt+1}/{retries}] {label} - file locked, waiting {delay}s...")
                time.sleep(delay)
            else:
                raise


def _detect_silence(audio_path: Path, min_silence_s: float = MAX_SILENCE_SECONDS) -> list[tuple[float, float, float]]:
    """Detect silent regions in an audio file using ffmpeg silencedetect.

    Returns a list of (start_s, end_s, duration_s) for silences >= min_silence_s.
    """
    null_out = "NUL" if sys.platform == "win32" else "/dev/null"
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise=-40dB:d={min_silence_s}",
        "-f", "null", null_out,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    regions = []
    current_start = None
    for line in result.stderr.splitlines():
        if "silence_start:" in line:
            match = re.search(r'silence_start:\s*([\d.]+)', line)
            if match:
                current_start = float(match.group(1))
        elif "silence_end:" in line and current_start is not None:
            match = re.search(r'silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)', line)
            if match:
                regions.append((current_start, float(match.group(1)), float(match.group(2))))
                current_start = None
    return regions


def trim_silence(audio_path: Path, max_silence_s: float = MAX_SILENCE_SECONDS, label: str = "") -> bool:
    """Trim silent regions exceeding max_silence_s from an audio file in-place.

    Uses ffmpeg silenceremove to strip trailing silence and silencedetect to
    find/trim interior silence. Logs warnings for any trimmed regions.

    Returns True if the file was modified.
    """
    regions = _detect_silence(audio_path, min_silence_s=max_silence_s)
    if not regions:
        return False

    tag = f" ({label})" if label else ""
    details = "; ".join(f"{s:.1f}s-{e:.1f}s ({d:.0f}s)" for s, e, d in regions)
    total_trimmed = sum(d for _, _, d in regions)
    print(f"    [WARN SILENCE]{tag} {audio_path.name} has {len(regions)} silent region(s) "
          f">={max_silence_s}s: {details} (TTS bug, trimming {total_trimmed:.0f}s)")

    # Use ffmpeg to trim: keep 2s of silence max at boundaries between speech
    temp_path = audio_path.with_suffix('.trimmed.wav')
    # silenceremove: stop_periods=-1 means process all silence regions
    # stop_duration = max allowed silence; stop_threshold = noise floor
    cmd = [
        "ffmpeg", "-y", "-i", str(audio_path),
        "-af", (
            f"silenceremove="
            f"stop_periods=-1:"
            f"stop_duration=2:"
            f"stop_threshold=-40dB"
        ),
        str(temp_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    [WARN] Silence trimming failed, keeping original: {result.stderr[-200:]}")
        temp_path.unlink(missing_ok=True)
        return False

    # Verify trimmed file is reasonable (not empty, not too short)
    if not temp_path.exists() or temp_path.stat().st_size < 1000:
        print(f"    [WARN] Trimmed file too small, keeping original")
        temp_path.unlink(missing_ok=True)
        return False

    _retry_fs_op(lambda: os.replace(str(temp_path), str(audio_path)), f"replace {audio_path.name}")
    old_dur = sum(d for _, _, d in regions)
    new_size = audio_path.stat().st_size
    print(f"    [TRIMMED]{tag} Removed ~{old_dur:.0f}s of silence ({new_size:,} bytes)")
    return True


def _read_mp3_source_hash(mp3_path: Path) -> str | None:
    """Read the source_qmd_hash TXXX frame from an MP3 file.

    Returns the hash string, or None if the frame doesn't exist or the file
    can't be read (e.g. not yet tagged with this field).
    """
    try:
        from mutagen.mp3 import MP3
        audio = MP3(str(mp3_path))
        if audio.tags is None:
            return None
        frame = audio.tags.get('TXXX:source_qmd_hash')
        if frame and frame.text:
            return frame.text[0]
    except Exception:
        pass
    return None


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
        'narrator': 'Wishonia',
        'podcast_author': podcast_author,
        'podcast_description': podcast_description,
        'podcast_description_suffix': podcast_description_suffix,
        # Rich metadata from config
        'copyright': metadata.get('copyright', f'(c) {year} {author}'),
        'license': metadata.get('license', ''),
        'license_url': metadata.get('license-url', ''),
        'version': metadata.get('version', ''),
        'subject': metadata.get('subject', ''),
        'keywords': metadata.get('keywords', ''),
        'author_url': metadata.get('author-website', ''),
        'publisher_url': metadata.get('publisher-url', ''),
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
    skip_text_prep: bool = False,
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
        skip_text_prep: Skip the text preparation subprocess (caller already prepared text)

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
    if not skip_text_prep:
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
        if skip_text_prep:
            print("  [SKIP] No prepared text file found (run generate_audiobook_text.py first)")
        else:
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
    removed_stale_chunks: list[str] = []
    for old_file in list(audio_chunk_dir.glob("chunk-*.wav")):
        if expected_tag not in old_file.stem:
            removed_stale_chunks.append(old_file.name)
            old_file.unlink()
            old_file.with_suffix('.texthash').unlink(missing_ok=True)
    if removed_stale_chunks:
        preview = ", ".join(removed_stale_chunks[:3])
        suffix = f", ... (+{len(removed_stale_chunks) - 3} more)" if len(removed_stale_chunks) > 3 else ""
        print(
            f"    [CLEAN] Removed {len(removed_stale_chunks)} stale audio chunk(s): "
            f"{preview}{suffix}"
        )

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
                # Trim any silence in cached chunks (catches pre-existing TTS bugs)
                trim_silence(audio_chunk_path, label=f"cached chunk {i+1}/{len(chunk_files)}")
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
            # Trim silent regions from TTS output (Gemini sometimes produces long silent tails)
            trim_silence(out_path, label=label)
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

    print(f"    [{datetime.now().strftime('%H:%M:%S')}] [OK] Saved: {output_path.name}")
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
    # Write to temp file first, then replace (avoids Windows file lock issues
    # from Search Indexer, Defender, or Obsidian holding the existing MP3)
    tmp_mp3 = mp3_path.with_suffix('.mp3.tmp')
    result = subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-ar", "24000", "-ac", "1",
        "-codec:a", "libmp3lame", "-b:a", "192k",
        "-f", "mp3",
        str(tmp_mp3),
    ], capture_output=True, text=True)
    if result.returncode != 0:
        tmp_mp3.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg MP3 export failed:\n{result.stderr[-1000:]}")
    # Replace old file (os.replace is atomic on same filesystem, bypasses most locks)
    _retry_fs_op(lambda: os.replace(str(tmp_mp3), str(mp3_path)), f"replace {mp3_path.name}")
    mp3_size = mp3_path.stat().st_size / 1024 / 1024
    print(f"  [OK] MP3: {mp3_path.name} ({mp3_size:.1f} MB)")

    # Clean up temp files (retry on Windows where ffmpeg may still hold the handle)
    for _tmp in (concat_file, silence_path):
        _retry_fs_op(lambda p=_tmp: p.unlink(missing_ok=True), f"clean {_tmp.name}")

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


def update_manifest(timestamps: list[ChapterTimestamp], total_duration_ms: int,
                    chapters: list[dict] | None = None, paths: AudiobookPaths | None = None,
                    quiet: bool = False):
    """Update manifest.json with duration and timing data."""
    # Build path lookup for stale-entry detection
    path_by_index = {ch['index']: ch['path'] for ch in chapters} if chapters else {}
    for ts in timestamps:
        update_chapter_fields(
            ts['index'],
            paths=paths,
            expected_path=path_by_index.get(ts['index']),
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
    if not quiet:
        print(f"  [OK] Updated manifest: {manifest_path.relative_to(PROJECT_ROOT)}")


def build_chapter_timestamps(chapters: list[dict], paths: AudiobookPaths | None = None,
                             gap_ms: int = 2000) -> tuple[list[ChapterTimestamp], int]:
    """Build timeline timestamps from per-chapter WAV files in config order.

    This is used to keep manifest timing fields fresh even when --no-combine
    skips the full combined audiobook packaging step.
    """
    timestamps: list[ChapterTimestamp] = []
    current_position_ms = 0

    for ch in chapters:
        audio_path = find_chapter_audio(ch, paths=paths)
        if not audio_path:
            continue

        # Match combine_chapter_audio timeline semantics (2s between chapters).
        if timestamps:
            current_position_ms += gap_ms

        duration_ms = _get_wav_duration_ms(audio_path)
        start_ms = current_position_ms
        end_ms = start_ms + duration_ms

        timestamps.append(ChapterTimestamp(
            index=ch['index'],
            title=ch['title'],
            part=ch.get('part'),
            file=audio_path.name,
            start_ms=start_ms,
            end_ms=end_ms,
            duration_ms=duration_ms,
            duration_formatted=format_duration(duration_ms),
        ))
        current_position_ms = end_ms

    return timestamps, current_position_ms


def refresh_manifest_and_feed(chapters: list[dict], book_meta: dict,
                              paths: AudiobookPaths, mp3_dir: Path,
                              quiet: bool = False) -> Path | None:
    """Refresh manifest timing data and regenerate podcast feed.xml.

    Returns feed path if generated, otherwise None.
    """
    timestamps, _ = build_chapter_timestamps(chapters, paths=paths)
    if not timestamps:
        print("  [WARN] No chapter WAVs found, skipping manifest/feed refresh")
        return None

    total_duration_ms = timestamps[-1]['end_ms']
    update_manifest(timestamps, total_duration_ms, chapters=chapters, paths=paths, quiet=quiet)

    chapter_mp3s = []
    for ch in chapters:
        slug = chapter_slug(ch)
        mp3 = find_current_mp3(slug, mp3_dir)
        if mp3:
            chapter_mp3s.append(mp3)

    if not chapter_mp3s:
        print(f"  [WARN] No per-chapter MP3s found in {mp3_dir}, skipping podcast RSS generation")
        return None

    generate_podcast_rss(chapter_mp3s, chapters, timestamps, book_meta, paths=paths, quiet=quiet)
    feed_path = paths.root / "feed.xml"
    return feed_path if feed_path.exists() else None


def sync_chapter_assets_immediately(mp3_path: Path, chapters: list[dict], book_meta: dict,
                                    paths: AudiobookPaths, mp3_dir: Path) -> None:
    """Upload newly generated chapter MP3 + refreshed feed/manifest to R2 immediately.

    Best-effort only: logs warnings and continues pipeline on any sync failure.
    """
    feed_path = refresh_manifest_and_feed(
        chapters, book_meta, paths, mp3_dir, quiet=not SYNC_VERBOSE
    )

    upload_paths = [mp3_path, paths.manifest]
    if feed_path:
        upload_paths.append(feed_path)

    try:
        from sync_r2 import upload_selected_files
        if SYNC_VERBOSE:
            uploaded, skipped, errors = upload_selected_files(upload_paths, dry_run=False)
        else:
            sync_log = io.StringIO()
            with contextlib.redirect_stdout(sync_log):
                uploaded, skipped, errors = upload_selected_files(upload_paths, dry_run=False)
            # Bubble up only warning/error lines from the suppressed verbose sync output.
            warn_lines = [
                line.strip()
                for line in sync_log.getvalue().splitlines()
                if "[WARN]" in line or "FAILED" in line or "ERROR" in line
            ]
            for line in warn_lines[:3]:
                print(f"  {line}")
            if len(warn_lines) > 3:
                print(f"  [SYNC WARN] ... {len(warn_lines) - 3} more warning/error line(s)")

        refreshed = "manifest+feed" if feed_path else "manifest"
        print(
            f"  [SYNC] {mp3_path.name} uploaded={uploaded} skipped={skipped} "
            f"errors={errors} refreshed={refreshed}"
        )
    except SystemExit:
        # sync_r2 exits when R2 creds are missing; keep audiobook generation running.
        print("  [WARN] Immediate sync skipped (R2 not configured in environment)")
    except Exception as e:
        print(f"  [WARN] Immediate sync failed: {e}")


def tag_mp3(mp3_path: Path, timestamps: list[ChapterTimestamp], book_meta: dict,
            chapters: list[dict] | None = None, paths: AudiobookPaths | None = None):
    """Embed ID3v2.4 tags with chapter markers, cover art, and per-chapter podcast images into the combined MP3."""
    from mutagen.mp3 import MP3
    from mutagen.id3 import (  # pyright: ignore[reportPrivateImportUsage]
        ID3, TIT2, TPE1, TPE2, TALB, TCON, TDRC, TPUB, APIC, CHAP, CTOC, CTOCFlags,
        TXXX, TLAN, COMM, TCOP, WOAF, WOAR, WPUB,
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

    # Copyright and license
    if book_meta.get('copyright'):
        tag.add(TCOP(encoding=3, text=[book_meta['copyright']]))
    if book_meta.get('license'):
        tag.add(TXXX(encoding=3, desc='license', text=[book_meta['license']]))
    if book_meta.get('license_url'):
        tag.add(TXXX(encoding=3, desc='license_url', text=[book_meta['license_url']]))

    # URLs
    if book_meta.get('site_url'):
        tag.add(WOAF(url=book_meta['site_url']))
    if book_meta.get('author_url'):
        tag.add(WOAR(url=book_meta['author_url']))
    if book_meta.get('publisher_url'):
        tag.add(WPUB(url=book_meta['publisher_url']))

    # Provenance and discoverability
    if book_meta.get('version'):
        tag.add(TXXX(encoding=3, desc='version', text=[book_meta['version']]))
    if book_meta.get('subject'):
        tag.add(TXXX(encoding=3, desc='subject', text=[book_meta['subject']]))
    if book_meta.get('keywords'):
        tag.add(TXXX(encoding=3, desc='keywords', text=[book_meta['keywords']]))

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

    # Build chapter-to-podcast-image lookup
    ch_by_index = {}
    if chapters:
        ch_by_index = {ch['index']: ch for ch in chapters}

    # Chapter markers (CHAP frames) with per-chapter podcast images
    chapter_ids = []
    for ts in timestamps:
        element_id = f"chp{ts['index']:02d}"
        chapter_ids.append(element_id)

        sub_frames = [TIT2(encoding=3, text=[ts['title']])]

        # Add per-chapter podcast image if available
        ch = ch_by_index.get(ts['index'])
        if ch:
            ep_image = find_podcast_image(ch, paths=paths)
            if ep_image and ep_image.exists():
                img_data = ep_image.read_bytes()
                img_mime = 'image/png' if ep_image.suffix.lower() == '.png' else 'image/jpeg'
                sub_frames.append(APIC(encoding=3, mime=img_mime, type=3, desc=f"Chapter {ts['index']}", data=img_data))

        tag.add(CHAP(
            element_id=element_id,
            start_time=ts['start_ms'],
            end_time=ts['end_ms'],
            start_offset=0xFFFFFFFF,  # Not used
            end_offset=0xFFFFFFFF,    # Not used
            sub_frames=sub_frames,
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
    # ffmetadata escapes: = ; # \ and newlines must be escaped with backslash
    def _esc(val: str) -> str:
        return val.replace('\\', '\\\\').replace('=', '\\=').replace(';', '\\;').replace('#', '\\#').replace('\n', '\\\n')

    lines = [";FFMETADATA1"]
    lines.append(f"title={_esc(book_meta['title'])}")
    lines.append(f"artist={_esc(book_meta['author'])}")
    lines.append(f"album={_esc(book_meta['title'])}")
    lines.append(f"genre=Audiobook")
    lines.append(f"date={book_meta['year']}")

    # Rich metadata
    if book_meta.get('subtitle'):
        lines.append(f"subtitle={_esc(book_meta['subtitle'])}")
    if book_meta.get('description'):
        lines.append(f"description={_esc(book_meta['description'])}")
        lines.append(f"comment={_esc(book_meta['description'])}")
    if book_meta.get('copyright'):
        lines.append(f"copyright={_esc(book_meta['copyright'])}")
    if book_meta.get('publisher'):
        lines.append(f"publisher={_esc(book_meta['publisher'])}")
    narrator = book_meta.get('narrator', '')
    if narrator:
        lines.append(f"narrator={_esc(narrator)}")
        lines.append(f"composer={_esc(narrator)}")
    if book_meta.get('license'):
        lines.append(f"license={_esc(book_meta['license'])}")
    if book_meta.get('license_url'):
        lines.append(f"license_url={_esc(book_meta['license_url'])}")
    if book_meta.get('site_url'):
        lines.append(f"url={_esc(book_meta['site_url'])}")
    if book_meta.get('version'):
        lines.append(f"version={_esc(book_meta['version'])}")
    if book_meta.get('subject'):
        lines.append(f"subject={_esc(book_meta['subject'])}")
    if book_meta.get('keywords'):
        lines.append(f"keywords={_esc(book_meta['keywords'])}")
    lines.append("language=eng")
    lines.append("media_type=Audiobook")
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
    # Preserve original sample rate (loudnorm internally resamples to 192kHz)
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "stream=sample_rate",
         "-of", "csv=p=0", str(wav_path)],
        capture_output=True, text=True,
    )
    orig_rate = probe.stdout.strip().split('\n')[0] if probe.returncode == 0 else "24000"
    norm_cmd = [
        "ffmpeg", "-y", "-i", str(wav_path),
        "-af", (
            f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11:"
            f"measured_I={measured_i}:measured_TP={measured_tp}:"
            f"measured_LRA={measured_lra}:measured_thresh={measured_thresh}:"
            f"offset={target_offset}:linear=true"
        ),
        "-ar", orig_rate,
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


def generate_outro_audio(
    voice: str = NARRATOR_VOICE,
    force: bool = False,
    paths: AudiobookPaths | None = None,
    config_path: Path = DEFAULT_CONFIG_PATH,
) -> Path | None:
    """Generate TTS audio for the podcast outro from podcast-outro.qmd.

    Processes the outro QMD through the same text preparation + TTS pipeline
    as regular chapters. Caches based on source QMD hash.

    Returns path to the outro WAV file, or None on failure.
    """
    if not OUTRO_QMD_PATH.exists():
        print(f"  [SKIP OUTRO] {OUTRO_QMD_PATH.name} not found")
        return None

    chapters_dir = paths.chapters if paths else CHAPTER_AUDIO_DIR
    outro_wav = chapters_dir / "podcast-outro.wav"

    # Hash-based cache check: hash both QMD source AND _variables.yml
    # so the outro regenerates when variable values change (e.g. voter_lives_saved)
    from lib.audiobook_common import VARIABLES_YML
    qmd_content = OUTRO_QMD_PATH.read_text(encoding='utf-8')
    hash_input = qmd_content
    if VARIABLES_YML.exists():
        hash_input += VARIABLES_YML.read_text(encoding='utf-8')
    current_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]
    hash_file = chapters_dir / "podcast-outro.qmdhash"

    if outro_wav.exists() and not force:
        old_hash = hash_file.read_text(encoding='utf-8').strip() if hash_file.exists() else ''
        if old_hash == current_hash:
            print(f"  [CACHED OUTRO] {outro_wav.name}")
            return outro_wav
        print(f"  [STALE OUTRO] source or variables changed ({old_hash or 'none'} -> {current_hash})")

    # Build a fake chapter dict so we can reuse generate_chapter_audio()
    outro_chapter = {
        'index': 9999,
        'path': str(OUTRO_QMD_PATH.relative_to(PROJECT_ROOT)),
        'title': 'Podcast Outro',
        'part': None,
        'podcast': False,
    }

    # Prepare text file directly (the outro QMD isn't in the Quarto config,
    # so the text subprocess would fail looking up chapter 9999)
    text_dir = paths.narration_txt if paths else (AUDIOBOOK_DIR / "manual-paperback" / "narration-txt-chapters")
    text_dir.mkdir(parents=True, exist_ok=True)
    slug = chapter_slug(outro_chapter)
    prepared_path = text_dir / f"{slug}.prepared.txt"

    # Strip frontmatter and include directives, resolve variables
    lines = qmd_content.split('\n')
    in_frontmatter = False
    text_lines = []
    for line in lines:
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if re.match(r'\{\{<\s*include\s+', line.strip()):
            continue
        text_lines.append(line)
    prepared_text = '\n'.join(text_lines).strip()

    # Resolve {{< var ... >}} shortcodes
    if '{{< var' in prepared_text:
        from dih_models.variable_replacement import load_variables, replace_variables
        from lib.audiobook_common import VARIABLES_YML
        variables = load_variables(VARIABLES_YML)
        prepared_text = replace_variables(prepared_text, variables)

    # Strip markup (CI intervals, HTML tags, etc.) - same as regular chapters
    from generate_audiobook_text import strip_qmd_markup
    prepared_text = strip_qmd_markup(prepared_text)

    prepared_path.write_text(prepared_text, encoding='utf-8')

    audio_path, _ = generate_chapter_audio(
        outro_chapter, voice=voice, force=force, paths=paths,
        config_path=config_path, skip_text_prep=True,
    )
    if audio_path:
        # Normalize loudness to match chapters
        normalize_loudness(audio_path, target_lufs=-16.0)
        # Write hash for cache
        chapters_dir.mkdir(parents=True, exist_ok=True)
        hash_file.write_text(current_hash, encoding='utf-8')

    return audio_path


def wrap_mp3_with_intro_outro(
    raw_mp3_path: Path,
    wrapped_mp3_dir: Path,
    intro_path: Path | None = None,
    outro_path: Path | None = None,
) -> Path | None:
    """Wrap a raw MP3 with intro/outro audio, writing to a separate output directory.

    Reads from raw_mp3_path (never mutated), writes to wrapped_mp3_dir/{slug}.mp3.
    Uses mtime comparison for caching: skips if output exists and is newer than
    all inputs (raw MP3 + intro + outro). ID3 tags are copied from raw to wrapped.

    Returns the wrapped MP3 path, or None if no wrapping was needed (no intro/outro).
    """
    import shutil
    from mutagen.mp3 import MP3

    wrapped_mp3_dir.mkdir(parents=True, exist_ok=True)
    output_path = wrapped_mp3_dir / raw_mp3_path.name

    if not intro_path and not outro_path:
        # No wrapping needed; just copy raw to output dir
        if output_path.exists() and output_path.stat().st_mtime >= raw_mp3_path.stat().st_mtime:
            print(f"  [SKIP WRAP] No intro/outro, copy up to date: {output_path.name}")
            return output_path
        shutil.copy2(str(raw_mp3_path), str(output_path))
        print(f"  [COPY] {raw_mp3_path.name} -> {output_path.parent.name}/")
        return output_path

    # Mtime-based cache: skip if output is newer than all inputs
    if output_path.exists():
        out_mtime = output_path.stat().st_mtime
        input_mtimes = [raw_mp3_path.stat().st_mtime]
        if intro_path and intro_path.exists():
            input_mtimes.append(intro_path.stat().st_mtime)
        if outro_path and outro_path.exists():
            input_mtimes.append(outro_path.stat().st_mtime)
        if out_mtime > max(input_mtimes):
            size_mb = output_path.stat().st_size / 1024 / 1024
            print(f"  [SKIP WRAP] Already wrapped: {output_path.name} ({size_mb:.1f} MB)")
            return output_path

    # Read tags from raw MP3
    raw_mp3 = MP3(str(raw_mp3_path))
    saved_tags = raw_mp3.tags

    # Build combined audio: intro + chapter + outro
    # Normalize to 48kHz mono: preserves theme song quality (brass/cymbals up to 24kHz)
    # while keeping mono for efficient bitrate. TTS (24kHz native) upsamples cleanly.
    TARGET_RATE = 48000
    TARGET_CHANNELS = 1

    chapter_audio = AudioSegment.from_mp3(str(raw_mp3_path))
    chapter_audio = chapter_audio.set_frame_rate(TARGET_RATE).set_channels(TARGET_CHANNELS)
    combined = AudioSegment.empty()

    if intro_path and intro_path.exists():
        if intro_path.suffix.lower() == '.mp3':
            intro_audio = AudioSegment.from_mp3(str(intro_path))
        else:
            intro_audio = AudioSegment.from_wav(str(intro_path))
        intro_audio = intro_audio.set_frame_rate(TARGET_RATE).set_channels(TARGET_CHANNELS)
        combined += intro_audio

    combined += chapter_audio

    if outro_path and outro_path.exists():
        if outro_path.suffix.lower() == '.mp3':
            outro_audio = AudioSegment.from_mp3(str(outro_path))
        else:
            outro_audio = AudioSegment.from_wav(str(outro_path))
        outro_audio = outro_audio.set_frame_rate(TARGET_RATE).set_channels(TARGET_CHANNELS)
        combined += outro_audio

    combined.export(str(output_path), format="mp3", bitrate="192k")

    # Copy ID3 tags from raw to wrapped
    if saved_tags:
        tagged = MP3(str(output_path))
        tagged.tags = saved_tags
        tagged.save()

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"  [OK WRAP] {output_path.name} ({size_mb:.1f} MB)")
    return output_path


def export_single_chapter_mp3(
    chapter: dict,
    book_meta: dict,
    track_num: int,
    total_chapters: int,
    voice: str = NARRATOR_VOICE,
    paths: AudiobookPaths | None = None,
) -> Path | None:
    """Export a single chapter WAV as a tagged MP3.

    Each MP3 gets ID3 tags: title, artist, album, narrator, track number,
    cover art, genre, copyright, license, source QMD hash, TTS voice, and
    generation date.  Per-chapter descriptions and podcast images from QMD
    frontmatter are used when available, falling back to book-level defaults.

    Returns the MP3 path, or None if no WAV exists for this chapter.
    """
    from datetime import datetime, timezone
    from mutagen.mp3 import MP3
    from mutagen.id3 import (  # pyright: ignore[reportPrivateImportUsage]
        TIT2, TPE1, TPE2, TALB, TCON, TDRC, TPUB, APIC, TRCK, TLAN, TXXX, COMM,
        TCOP, WOAF,
    )

    raw_mp3_dir = paths.raw_mp3 if paths else AUDIOBOOK_DIR / "mp3-raw"
    raw_mp3_dir.mkdir(parents=True, exist_ok=True)

    chapter_file = find_chapter_audio(chapter, paths=paths)
    if not chapter_file:
        print(f"  [SKIP MP3] No WAV for chapter {chapter['index']}: {chapter['title']}")
        return None

    slug = chapter_file.stem
    mp3_path = raw_mp3_dir / f"{slug}.mp3"

    # Check if raw MP3 is already up-to-date via embedded source_qmd_hash
    qmd_path = PROJECT_ROOT / chapter['path']
    current_qmd_hash = ''
    if qmd_path.exists():
        qmd_content = qmd_path.read_text(encoding='utf-8')
        current_qmd_hash = hashlib.sha256(qmd_content.encode('utf-8')).hexdigest()[:16]

    if mp3_path.exists() and current_qmd_hash:
        existing_hash = _read_mp3_source_hash(mp3_path)
        if existing_hash == current_qmd_hash:
            if chapter_file.stat().st_mtime <= mp3_path.stat().st_mtime:
                size_mb = mp3_path.stat().st_size / 1024 / 1024
                print(f"  [SKIP RAW MP3] Up to date (hash {current_qmd_hash}): {mp3_path.name} ({size_mb:.1f} MB)")
                return mp3_path
            else:
                print(f"  [STALE RAW MP3] WAV newer than MP3, re-exporting")
        else:
            print(f"  [STALE RAW MP3] QMD hash changed ({existing_hash or 'none'} -> {current_qmd_hash}), re-exporting")
    elif mp3_path.exists():
        print(f"  [STALE RAW MP3] No hash to verify, re-exporting")
    else:
        print(f"  [NEW RAW MP3] Exporting: {slug}.mp3")

    # Convert WAV to MP3 via pydub
    # Force 24kHz mono (TTS native rate; loudnorm may have upsampled WAV to 192kHz)
    audio = AudioSegment.from_wav(str(chapter_file))
    audio = audio.set_frame_rate(24000).set_channels(1)
    audio.export(str(mp3_path), format="mp3", bitrate="192k")

    # Book-level cover art (fallback for chapters without podcast images)
    cover_art: Path = book_meta['cover_art']
    book_cover_data = cover_art.read_bytes()
    book_cover_mime = 'image/png' if cover_art.suffix.lower() == '.png' else 'image/jpeg'

    # Tag with ID3
    mp3 = MP3(str(mp3_path))
    if mp3.tags is None:
        mp3.add_tags()
    assert mp3.tags is not None
    tag = mp3.tags

    narrator = book_meta['narrator']
    generation_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Basic metadata
    tag.add(TIT2(encoding=3, text=[chapter['title']]))
    tag.add(TPE1(encoding=3, text=[book_meta['author']]))
    tag.add(TPE2(encoding=3, text=[book_meta['author']]))
    tag.add(TALB(encoding=3, text=[book_meta['title']]))
    tag.add(TCON(encoding=3, text=["Audiobook"]))
    tag.add(TDRC(encoding=3, text=[book_meta['year']]))
    tag.add(TPUB(encoding=3, text=[book_meta['publisher']]))
    tag.add(TRCK(encoding=3, text=[f"{track_num}/{total_chapters}"]))
    tag.add(TLAN(encoding=3, text=["eng"]))
    tag.add(TXXX(encoding=3, desc='narrator', text=[narrator]))

    # Per-chapter description (fall back to book-level)
    ch_desc = chapter.get('description') or book_meta.get('description', '')
    if ch_desc:
        tag.add(COMM(encoding=3, lang='eng', desc='', text=[ch_desc]))

    # Copyright and license
    if book_meta.get('copyright'):
        tag.add(TCOP(encoding=3, text=[book_meta['copyright']]))
    if book_meta.get('license'):
        tag.add(TXXX(encoding=3, desc='license', text=[book_meta['license']]))

    # Official URL
    if book_meta.get('site_url'):
        tag.add(WOAF(url=book_meta['site_url']))

    # Per-chapter podcast image (fall back to book cover)
    ep_image = find_podcast_image(chapter, paths=paths)
    if ep_image and ep_image.exists():
        img_data = ep_image.read_bytes()
        img_mime = 'image/png' if ep_image.suffix.lower() == '.png' else 'image/jpeg'
    else:
        img_data = book_cover_data
        img_mime = book_cover_mime
    tag.add(APIC(encoding=3, mime=img_mime, type=3, desc='Cover', data=img_data))

    # Source QMD hash for provenance (reuse hash computed at top of function)
    if current_qmd_hash:
        tag.add(TXXX(encoding=3, desc='source_qmd_hash', text=[current_qmd_hash]))
        tag.add(TXXX(encoding=3, desc='source_qmd_path', text=[chapter['path']]))

    # TTS provenance
    tag.add(TXXX(encoding=3, desc='tts_voice', text=[voice]))
    tag.add(TXXX(encoding=3, desc='generation_date', text=[generation_date]))
    if book_meta.get('version'):
        tag.add(TXXX(encoding=3, desc='version', text=[book_meta['version']]))

    mp3.save()
    size_mb = mp3_path.stat().st_size / 1024 / 1024
    print(f"  [OK MP3] {mp3_path} ({size_mb:.1f} MB, hash {current_qmd_hash or 'none'})")
    return mp3_path


def export_chapter_mp3s(
    chapters: list[dict],
    book_meta: dict,
    voice: str = NARRATOR_VOICE,
    paths: AudiobookPaths | None = None,
) -> list[Path]:
    """Export all chapter WAVs as tagged MP3s for per-chapter distribution."""
    total = len(chapters)
    mp3_files = []
    for track_num, ch in enumerate(chapters, 1):
        mp3_path = export_single_chapter_mp3(ch, book_meta, track_num, total, voice=voice, paths=paths)
        if mp3_path:
            mp3_files.append(mp3_path)
    raw_mp3_dir = paths.raw_mp3 if paths else AUDIOBOOK_DIR / "mp3-raw"
    print(f"  Exported {len(mp3_files)} raw chapter MP3s to {raw_mp3_dir}")
    return mp3_files


def finalize_podcast_mp3(mp3_path: Path) -> Path:
    """Rename an MP3 to include a content hash for podcast cache busting.

    Converts {slug}.mp3 (or {slug}.{oldhash}.mp3) to {slug}.{newhash}.mp3.
    Cleans up old hashed versions of the same slug.
    Returns the new path (unchanged if hash already matches).
    """
    # Determine the base slug (strip existing hash if present)
    parsed = parse_hashed_mp3(mp3_path.name)
    slug = parsed[0] if parsed else mp3_path.stem

    content_hash = mp3_content_hash(mp3_path)
    target = mp3_path.parent / f"{slug}.{content_hash}.mp3"

    if target == mp3_path:
        return mp3_path  # already has correct hash

    # Clean up old hashed versions (different hash, same slug)
    for old in mp3_path.parent.glob(f"{slug}.*.mp3"):
        if PODCAST_HASH_RE.match(old.name) and old != mp3_path and old != target:
            _retry_fs_op(lambda p=old: p.unlink(), f"clean {old.name}")
            print(f"  [CLEAN] Removed old version: {old.name}")

    _retry_fs_op(lambda: mp3_path.replace(target), f"rename {mp3_path.name}")
    print(f"  [HASH] {mp3_path.name} -> {target.name}")
    return target


def generate_podcast_rss(
    chapter_mp3s: list[Path],
    chapters: list[dict],
    timestamps: list[ChapterTimestamp],
    book_meta: dict,
    paths: AudiobookPaths | None = None,
    quiet: bool = False,
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

    def _to_html_paragraphs(text: str) -> str:
        """Convert plain text with blank-line-separated paragraphs to HTML <p> tags.

        Spotify, Apple Podcasts, etc. ignore plain-text newlines in <description>.
        HTML <p> tags inside CDATA sections are the industry standard fix.
        """
        import re
        paragraphs = re.split(r'\n\s*\n', text.strip())
        paragraphs = [' '.join(p.split()) for p in paragraphs if p.strip()]
        return ''.join(f'<p>{escape(p)}</p>' for p in paragraphs)

    title = escape(book_meta['title'])
    author = escape(book_meta.get('podcast_author', book_meta['author']))
    raw_desc = book_meta.get('podcast_description') or book_meta['description']
    desc_suffix = book_meta.get('podcast_description_suffix', '')
    # Build HTML channel description with suffix
    channel_desc_text = raw_desc
    if desc_suffix:
        channel_desc_text = f"{channel_desc_text}\n\n{desc_suffix}"
    channel_desc_html = _to_html_paragraphs(channel_desc_text)
    narrator = escape(book_meta['narrator'])
    podcast_cover: Path = book_meta['podcast_cover']
    cover_filename = podcast_cover.relative_to(PROJECT_ROOT).as_posix()
    cover_url = f"{cdn_url}/{cover_filename}"

    from datetime import datetime, timezone, timedelta

    # Get git last-modified dates for each chapter QMD file.
    # Falls back to file mtime if git fails, then to a spaced-out synthetic date.
    def _git_last_modified(qmd_path: str) -> datetime | None:
        """Get the last git commit date for a file."""
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", qmd_path],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT),
        )
        if result.returncode == 0 and result.stdout.strip():
            return datetime.fromisoformat(result.stdout.strip())
        return None

    ch_pub_dates: dict[int, datetime] = {}
    fallback_date = datetime.now(timezone.utc)
    for ch in chapters:
        git_date = _git_last_modified(ch['path'])
        if git_date:
            ch_pub_dates[ch['index']] = git_date
        else:
            # Fallback: file modification time
            qmd_file = PROJECT_ROOT / ch['path']
            if qmd_file.exists():
                mtime = qmd_file.stat().st_mtime
                ch_pub_dates[ch['index']] = datetime.fromtimestamp(mtime, tz=timezone.utc)
            else:
                ch_pub_dates[ch['index']] = fallback_date

    # Ensure dates are monotonically INCREASING in chapter order so that
    # serial podcast apps (Spotify, Apple) show episode 1 first naturally.
    # The <itunes:type>serial</itunes:type> + <itunes:episode> numbers
    # control reading order; ascending pubDates reinforce that ordering.
    sorted_indices = sorted(ch_pub_dates.keys())
    for i in range(1, len(sorted_indices)):
        prev_idx = sorted_indices[i - 1]
        curr_idx = sorted_indices[i]
        if ch_pub_dates[curr_idx] <= ch_pub_dates[prev_idx]:
            ch_pub_dates[curr_idx] = ch_pub_dates[prev_idx] + timedelta(minutes=1)

    # Channel pubDate = last chapter's date (the latest after monotonic fix)
    latest_date = ch_pub_dates[sorted_indices[-1]] if sorted_indices else fallback_date

    # Build MP3 lookup by slug for matching with timestamps.
    # Handles both hashed ({slug}.{hash8}.mp3) and canonical ({slug}.mp3) filenames.
    mp3_by_slug: dict[str, Path] = {}
    for mp3 in chapter_mp3s:
        parsed = parse_hashed_mp3(mp3.name)
        slug_key = parsed[0] if parsed else mp3.stem
        mp3_by_slug[slug_key] = mp3

    # Build chapter lookup by index for podcast exclusion check
    ch_by_index = {ch['index']: ch for ch in chapters}

    # Build per-episode lookups from chapter list (keyed by slug)
    ep_image_urls: dict[str, str] = {}
    ep_wide_image_urls: dict[str, str] = {}
    ep_descriptions: dict[str, str] = {}
    for ch in chapters:
        s = chapter_slug(ch)
        img = find_podcast_image(ch, paths=paths)
        if img:
            img_rel = img.relative_to(PROJECT_ROOT).as_posix()
            ep_image_urls[s] = f"{cdn_url}/{img_rel}"
        wide_img = find_youtube_thumbnail(ch, paths=paths)
        if wide_img:
            wide_rel = wide_img.relative_to(PROJECT_ROOT).as_posix()
            ep_wide_image_urls[s] = f"{cdn_url}/{wide_rel}"
        if ch.get('description'):
            ep_descriptions[s] = ch['description']

    items = []
    total_eps = len(chapter_mp3s)
    skipped_not_podcast = 0
    missing_mp3 = 0
    for ep_num, ts in enumerate(timestamps):
        # Skip chapters with podcast: false in frontmatter
        ch = ch_by_index.get(ts['index'])
        if ch and not ch.get('podcast', True):
            skipped_not_podcast += 1
            if not quiet:
                print(f"  [SKIP RSS] {ts['title']} (podcast: false)")
            continue

        slug = Path(ts['file']).stem  # WAV slug -> MP3 slug
        mp3_path = mp3_by_slug.get(slug)
        if not mp3_path:
            missing_mp3 += 1
            if not quiet:
                print(f"  [WARN] No MP3 for timestamp entry: {ts['file']}")
            continue

        ch_title = escape(ts['title'])
        part = ts.get('part', '')
        ep_title = f"{ch_title}" if not part else f"{part}: {ch_title}"

        # Use QMD description if available, fall back to generic; append CTA suffix
        ep_desc_text = ep_descriptions.get(slug, f"Chapter {ep_num + 1} of {title}")
        if desc_suffix:
            ep_desc_text = f"{ep_desc_text}\n\n{desc_suffix}"
        ep_desc_html = _to_html_paragraphs(ep_desc_text)

        duration_fmt = ts['duration_formatted']
        file_size = mp3_path.stat().st_size
        mp3_url = f"{mp3_url_base}/{mp3_path.name}"
        ep_date = ch_pub_dates.get(ts['index'], fallback_date)
        pub_date = ep_date.strftime("%a, %d %b %Y %H:%M:%S +0000")

        ep_img = ep_image_urls.get(slug)
        ep_wide = ep_wide_image_urls.get(slug)
        image_tag = f'\n      <itunes:image href="{escape(ep_img)}"/>' if ep_img else ''

        # Build podcast:images srcset with available sizes
        srcset_parts = []
        if ep_wide:
            srcset_parts.append(f"{escape(ep_wide)} 1920w")
        if ep_img:
            srcset_parts.append(f"{escape(ep_img)} 3000w")
        podcast_images_tag = ''
        if srcset_parts:
            podcast_images_tag = f'\n      <podcast:images srcset="{", ".join(srcset_parts)}"/>'

        items.append(f"""    <item>
      <title>{escape(ep_title)}</title>
      <enclosure url="{escape(mp3_url)}" length="{file_size}" type="audio/mpeg"/>
      <pubDate>{pub_date}</pubDate>
      <itunes:duration>{duration_fmt}</itunes:duration>
      <itunes:episode>{ep_num + 1}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <guid isPermaLink="false">chapter-{slug}</guid>
      <description><![CDATA[{ep_desc_html}]]></description>{image_tag}{podcast_images_tag}
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:podcast="https://podcastindex.org/namespace/1.0"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{title}</title>
    <link>{escape(site_url)}</link>
    <description><![CDATA[{channel_desc_html}]]></description>
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
    <pubDate>{latest_date.strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
    <lastBuildDate>{datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
    <podcast:medium>audiobook</podcast:medium>
    <atom:link href="{escape(cdn_url)}/{mp3_base.as_posix()}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""

    rss_path.write_text(feed, encoding='utf-8')
    if not quiet:
        print(f"\n  [OK] Podcast RSS: {rss_path.relative_to(PROJECT_ROOT)}")
        print(f"  Feed URL: {site_url}/{mp3_base.as_posix()}/feed.xml")
    elif skipped_not_podcast or missing_mp3:
        print(
            f"  [RSS] refreshed ({len(items)} episode(s); "
            f"skipped={skipped_not_podcast}, missing-mp3={missing_mp3})"
        )
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
        expected_path=chapter['path'],
        alignment_file=str(alignment_path.relative_to(PROJECT_ROOT)),
        subtitle_file=str(vtt_path.relative_to(PROJECT_ROOT)),
    )


def _cleanup_wraphash_sidecars(mp3_dir: Path) -> None:
    """Remove legacy .wraphash sidecar files from the mp3 directory."""
    if not mp3_dir.exists():
        return
    for f in mp3_dir.glob("*.wraphash"):
        f.unlink()
        print(f"  [CLEAN] Removed legacy sidecar: {f.name}")


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
        "--skip-text-prep",
        action="store_true",
        help="Assume narration text is already prepared; skip per-chapter text subprocess",
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
    parser.add_argument(
        "--sync-each-chapter",
        dest="sync_each_chapter",
        action="store_true",
        help="After each chapter MP3 is finalized, immediately upload MP3 + refreshed feed/manifest to R2 (default: enabled)",
    )
    parser.add_argument(
        "--no-sync-each-chapter",
        dest="sync_each_chapter",
        action="store_false",
        help="Disable immediate per-chapter R2 upload of MP3/feed/manifest",
    )
    parser.set_defaults(sync_each_chapter=True)
    args = parser.parse_args()

    try:
        lock = acquire_script_lock(
            "generate-audiobook",
            PROJECT_ROOT,
            command=" ".join(sys.argv),
        )
        atexit.register(lock.release)
    except ScriptLockError as e:
        print(f"ERROR: {e}")
        sys.exit(2)

    # Resolve config and derive paths
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

    # Set up logging (file-only; TeeWriter segfaults on Windows with subprocess I/O)
    logger = BuildLogger("generate-audiobook.log")

    # Load book config
    print(f"Loading book configuration: {config_path.name} (output: assets/audiobook/{cfg_name}/)")
    config = load_book_config(config_path)
    chapters = extract_chapters(config)
    print(f"Found {len(chapters)} chapters")

    # List mode
    if args.list:
        list_chapters(chapters, paths=paths)
        logger.close()
        return

    # Filter chapters if specified
    if args.chapter:
        chapters = [ch for ch in chapters if ch['index'] == args.chapter]
        if not chapters:
            print(f"Error: Chapter {args.chapter} not found")
            logger.close()
            return
    elif args.start or args.end:
        start = args.start or 1
        end = args.end or len(chapters)
        chapters = [ch for ch in chapters if start <= ch['index'] <= end]

    # Load book metadata upfront (needed for per-chapter MP3 tagging)
    book_meta = extract_book_metadata(config)
    all_chapters = extract_chapters(config)
    total_chapters = len(all_chapters)

    print(f"\nGenerating audio for {len(chapters)} chapter(s)...")
    print(f"Voice: {args.voice}")
    print(f"Output: {paths.root.relative_to(PROJECT_ROOT)}")
    if args.skip_text_prep:
        print("Text prep: skipped (using existing prepared narration text)")
    print()

    # Substep timing accumulator: {label: elapsed_seconds}
    _substep_times: dict[str, float] = {
        "Outro audio": 0.0,
        "TTS generation": 0.0,
        "Loudness normalization": 0.0,
        "Alignment + subtitles": 0.0,
        "MP3 export + wrapping": 0.0,
        "Combine audiobook": 0.0,
        "Manifest timing refresh": 0.0,
        "Podcast RSS feed": 0.0,
    }

    # Clean up legacy .wraphash sidecars
    mp3_dir = paths.root / "mp3"
    _cleanup_wraphash_sidecars(mp3_dir)

    # Generate podcast outro audio (once, before chapter loop)
    outro_wav = None
    t_sub = time.monotonic()
    if OUTRO_QMD_PATH.exists():
        print("=" * 60)
        print("  Generating podcast outro audio...")
        print("=" * 60)
        outro_wav = generate_outro_audio(
            voice=args.voice, force=args.force, paths=paths, config_path=config_path
        )
        if outro_wav:
            print(f"  [OK] Outro audio: {outro_wav.name}")
        else:
            print(f"  [WARN] Outro audio generation failed, chapters will not have outro")
    else:
        print(f"  [INFO] No outro QMD found at {OUTRO_QMD_PATH.name}, skipping outro")
    _substep_times["Outro audio"] = time.monotonic() - t_sub

    # Check for theme song
    intro_mp3 = THEME_SONG_PATH if THEME_SONG_PATH.exists() else None
    if intro_mp3:
        print(f"  [OK] Theme song: {intro_mp3.name}")
    else:
        print(f"  [INFO] No theme song at {THEME_SONG_PATH}, skipping intro")
    print()

    # Per-chapter pipeline: text -> WAV -> normalize -> align -> raw MP3 -> wrap -> finalize
    generated_files = []
    for chapter in chapters:
        qmd_path = PROJECT_ROOT / chapter['path']
        title = chapter['title'] or (extract_title_from_qmd(qmd_path) if qmd_path.exists() else chapter['path'])

        print(f"\n[{chapter['index']}/{total_chapters}] {title}")

        # 1. Generate audio (text prep + TTS + combine chunks -> WAV)
        t_sub = time.monotonic()
        audio_path, audio_changed = generate_chapter_audio(
            chapter,
            voice=args.voice,
            force=args.force,
            paths=paths,
            config_path=config_path,
            skip_text_prep=args.skip_text_prep,
        )
        _substep_times["TTS generation"] += time.monotonic() - t_sub
        if not audio_path:
            continue

        generated_files.append(audio_path)

        # 2. Normalize loudness
        t_sub = time.monotonic()
        normalize_loudness(audio_path, target_lufs=-16.0)
        _substep_times["Loudness normalization"] += time.monotonic() - t_sub

        # 3. Forced alignment + subtitle generation
        if not args.no_align:
            t_sub = time.monotonic()
            _run_alignment(chapter, audio_path, title, force=args.force, paths=paths, audio_changed=audio_changed)
            _substep_times["Alignment + subtitles"] += time.monotonic() - t_sub

        # 4. Export raw tagged chapter MP3 (to mp3-raw/)
        t_sub = time.monotonic()
        track_num = next((i for i, ch in enumerate(all_chapters, 1) if ch['index'] == chapter['index']), chapter['index'])
        raw_mp3 = export_single_chapter_mp3(chapter, book_meta, track_num, total_chapters, voice=args.voice, paths=paths)

        # 5. Wrap with intro/outro (raw mp3-raw/ -> wrapped mp3/)
        if raw_mp3:
            wrapped = wrap_mp3_with_intro_outro(raw_mp3, mp3_dir, intro_path=intro_mp3, outro_path=outro_wav)

            # 6. Rename to content-hashed filename for podcast cache busting
            if wrapped:
                wrapped = finalize_podcast_mp3(wrapped)
                if args.sync_each_chapter:
                    sync_chapter_assets_immediately(
                        wrapped,
                        all_chapters,
                        book_meta,
                        paths,
                        mp3_dir,
                    )
        _substep_times["MP3 export + wrapping"] += time.monotonic() - t_sub

    print(f"\n{'=' * 60}")
    print(f"Processed {len(generated_files)} chapters")

    # Combine into single audiobook (optional, off by default)
    t_sub = time.monotonic()
    manifest_timestamps: list[ChapterTimestamp] = []
    manifest_source = "chapter WAVs"
    if not args.no_combine:
        chapters_with_audio = [ch for ch in all_chapters if find_chapter_audio(ch, paths=paths)]
        if len(chapters_with_audio) > 1:
            combined_path = paths.root / f"{safe_filename(book_meta['title'], max_len=80)}-Audiobook"
            mp3_path, manifest_timestamps = combine_chapter_audio(all_chapters, combined_path, paths=paths)
            manifest_source = "combined timeline"
            tag_mp3(mp3_path, manifest_timestamps, book_meta, chapters=all_chapters, paths=paths)
            export_m4b(mp3_path, manifest_timestamps, book_meta)
        elif chapters_with_audio:
            print("  [INFO] Skipping combined audiobook: need at least 2 chapter WAVs")
        else:
            print("  [INFO] Skipping combined audiobook: no chapter WAVs found")
    _substep_times["Combine audiobook"] = time.monotonic() - t_sub

    # Refresh manifest timing fields regardless of --no-combine.
    t_sub = time.monotonic()
    if not manifest_timestamps:
        manifest_timestamps, _ = build_chapter_timestamps(all_chapters, paths=paths)
    if manifest_timestamps:
        total_duration_ms = manifest_timestamps[-1]['end_ms']
        print(f"\nRefreshing manifest timing fields from {manifest_source} ({len(manifest_timestamps)} chapters)...")
        update_manifest(manifest_timestamps, total_duration_ms, chapters=all_chapters, paths=paths)
    else:
        print("\n  [WARN] No chapter WAVs found, skipping manifest timing update")
    _substep_times["Manifest timing refresh"] = time.monotonic() - t_sub

    # Generate podcast RSS feed (always, independent of --no-combine)
    t_sub = time.monotonic()
    chapter_mp3s = []
    for ch in all_chapters:
        slug = chapter_slug(ch)
        mp3 = find_current_mp3(slug, mp3_dir)
        if mp3:
            chapter_mp3s.append(mp3)

    if chapter_mp3s:
        from lib.audiobook_manifest import read_manifest
        manifest = read_manifest(paths=paths)
        timestamps_from_manifest: list[ChapterTimestamp] = []
        for ch_data in manifest.get("chapters", []):
            if "duration_ms" not in ch_data or "audio_file" not in ch_data:
                continue
            timestamps_from_manifest.append(ChapterTimestamp(
                index=ch_data["index"],
                title=ch_data["title"],
                part=ch_data.get("part"),
                file=ch_data["audio_file"],
                start_ms=ch_data.get("audio_start_ms", 0),
                end_ms=ch_data.get("audio_end_ms", ch_data["duration_ms"]),
                duration_ms=ch_data["duration_ms"],
                duration_formatted=ch_data.get("duration_formatted", "0:00"),
            ))
        if timestamps_from_manifest:
            generate_podcast_rss(chapter_mp3s, all_chapters, timestamps_from_manifest, book_meta, paths=paths)
        else:
            print("  [WARN] No timestamps in manifest, skipping podcast RSS generation")
    else:
        print(f"  [WARN] No per-chapter MP3s found in {mp3_dir}, skipping podcast RSS generation")
    _substep_times["Podcast RSS feed"] = time.monotonic() - t_sub

    # Write timing report for publish_audiobook.py to read
    timing_report_path = paths.root / ".audio-timing.json"
    timing_report_path.write_text(
        json.dumps(_substep_times, indent=2), encoding="utf-8"
    )

    print("\nDone!")
    logger.close()


if __name__ == "__main__":
    main()
