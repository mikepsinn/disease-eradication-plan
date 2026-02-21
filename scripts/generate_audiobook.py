#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Generator

Generates an audiobook from all chapters in _quarto-manual-paperback.yml using Gemini TTS.

Preferred pipeline (two-step):
    1. python scripts/generate_audiobook_text.py   # QMD -> programmatic cleanup -> LLM polish -> audiobook/text/
    2. python scripts/generate_audiobook.py         # audiobook/text/ -> TTS -> audiobook/chapters/

If pre-generated text files exist in audiobook/text/, they are used automatically.
Otherwise falls back to raw QMD extraction (no variable resolution, no number conversion).

Usage:
    python scripts/generate_audiobook.py                    # Generate full audiobook
    python scripts/generate_audiobook.py --chapter 5       # Generate specific chapter
    python scripts/generate_audiobook.py --voice Zephyr    # Use different voice
    python scripts/generate_audiobook.py --list            # List all chapters
"""
import sys
import os
import re
import argparse
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from pydub import AudioSegment

# Add scripts directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))
# Add project root to path for dih_models imports
sys.path.insert(0, str(Path(__file__).parent.parent))
import subprocess
from lib.tts import generate_speech, AVAILABLE_VOICES, DEFAULT_VOICE, DEFAULT_SPEAKING_INSTRUCTIONS
from dih_models.yaml_utils import yaml_safe_load, load_quarto_config

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
QUARTO_BOOK_YML = PROJECT_ROOT / "_quarto-manual-paperback.yml"
OUTPUT_DIR = PROJECT_ROOT / "audiobook"
CHAPTER_AUDIO_DIR = OUTPUT_DIR / "chapters"
TEXT_DIR = OUTPUT_DIR / "text"

# Voice for narration (uses library default: Aoede with Cunk-style delivery)
NARRATOR_VOICE = DEFAULT_VOICE


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


def extract_prose_from_qmd(file_path: Path) -> str:
    """
    Extract readable prose content from a QMD file.

    Removes:
    - YAML frontmatter
    - Code blocks (```...```)
    - Python/R code blocks ({python}, {r})
    - Quarto includes
    - Quarto variables (replace with placeholder)
    - HTML tags
    - Markdown image syntax
    - Markdown link URLs (keep link text)
    - LaTeX math blocks
    - Comments
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove YAML frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Remove code blocks (fenced)
    content = re.sub(r'```[\s\S]*?```', '', content)

    # Remove Quarto code blocks with options
    content = re.sub(r'\{[#]?(?:python|r|julia|bash|sql)[\s\S]*?\}[\s\S]*?(?=\n\n|\n#|\Z)', '', content)

    # Remove Quarto includes
    content = re.sub(r'\{\{<\s*include\s+.*?>\}\}', '', content)

    # Remove Quarto video embeds
    content = re.sub(r'\{\{<\s*video\s+.*?>\}\}', '', content)

    # Replace Quarto variables with "value" placeholder for natural reading
    content = re.sub(r'\{\{<\s*var\s+\w+\s*>\}\}', 'the relevant value', content)

    # Remove LaTeX display math blocks
    content = re.sub(r'\$\$[\s\S]*?\$\$', '', content)

    # Remove inline LaTeX math
    content = re.sub(r'\$[^$]+\$', '', content)

    # Remove HTML tags but keep content
    content = re.sub(r'<[^>]+>', '', content)

    # Remove HTML comments
    content = re.sub(r'<!--[\s\S]*?-->', '', content)

    # Remove markdown images
    content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', content)

    # Convert markdown links to just text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # Remove reference-style link definitions
    content = re.sub(r'^\[[^\]]+\]:\s+.*$', '', content, flags=re.MULTILINE)

    # Remove horizontal rules
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*\*+$', '', content, flags=re.MULTILINE)

    # Clean up markdown formatting for speech
    # Remove bold/italic markers but keep text
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    content = re.sub(r'__([^_]+)__', r'\1', content)
    content = re.sub(r'_([^_]+)_', r'\1', content)

    # Convert headers to spoken form
    content = re.sub(r'^#{1,6}\s+(.+)$', r'\n\1.\n', content, flags=re.MULTILINE)

    # Remove bullet points but keep content
    content = re.sub(r'^\s*[-*+]\s+', '', content, flags=re.MULTILINE)

    # Remove numbered list markers
    content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)

    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Clean up whitespace
    content = content.strip()

    return content


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


def combine_chapter_audio(chapter_files: list[Path], output_path: Path):
    """
    Combine individual chapter audio files into a single audiobook.

    Args:
        chapter_files: List of paths to chapter WAV files (in order)
        output_path: Path for combined output file
    """
    print(f"\nCombining {len(chapter_files)} chapters into audiobook...")

    # Start with empty audio
    combined = AudioSegment.empty()

    # Add 2 seconds of silence between chapters
    silence = AudioSegment.silent(duration=2000)

    for i, chapter_file in enumerate(chapter_files):
        print(f"  Adding: {chapter_file.name}")

        try:
            chapter_audio = AudioSegment.from_wav(str(chapter_file))

            if i > 0:
                combined += silence
            combined += chapter_audio

        except Exception as e:
            print(f"    [ERROR] Failed to add {chapter_file.name}: {e}")

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
    duration_seconds = len(combined) / 1000
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = int(duration_seconds % 60)
    print(f"\nTotal duration: {hours}h {minutes}m {seconds}s")

    return mp3_path


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
            combined_path = OUTPUT_DIR / "How-to-End-War-and-Disease-Audiobook"
            combine_chapter_audio(all_chapter_files, combined_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
