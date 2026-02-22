#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Video Generator

Generates animated video for audiobook chapters using:
1. LLM scene segmentation (Gemini Flash)
2. Keyframe image generation (Imagen)
3. Video animation (Veo 3.1)
4. Assembly with ffmpeg

Reads chapter list from any Quarto book YAML config.

Usage:
    python scripts/generate_audiobook_video.py --config _quarto-manual-paperback.yml --limit 1 --scenes-only
    python scripts/generate_audiobook_video.py --config _quarto-manual-paperback.yml --limit 3
    python scripts/generate_audiobook_video.py --config _quarto-manual-paperback.yml --list
"""
import io
import sys
import json
import re
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if sys.platform == 'win32' and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

from pydub import AudioSegment

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.llm import generate_gemini_flash_content, GEMINI_FLASH_MODEL_ID
from lib.veo import generate_image, generate_video
from dih_models.yaml_utils import load_quarto_config

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
AUDIOBOOK_DIR = PROJECT_ROOT / "audiobook"
VIDEO_DIR = AUDIOBOOK_DIR / "video"
SCENES_DIR = VIDEO_DIR / "scenes"
TEXT_DIR = AUDIOBOOK_DIR / "text"
CHAPTER_AUDIO_DIR = AUDIOBOOK_DIR / "chapters"
MANIFEST_PATH = AUDIOBOOK_DIR / "manifest.json"
DEFAULT_CONFIG_NAME = "manual-paperback"

ASPECT_RATIOS = ["16:9", "9:16"]

# Must match BW_ACADEMIC_STYLE from scripts/lib/image-prompts.ts
IMAGE_STYLE = "Use a black and white scientific illustration style."

# Suppress Veo-generated speech so we can overlay our own TTS narration.
# Veo ambient audio (music + SFX) is kept and mixed at reduced volume.
VEO_NEGATIVE_PROMPT = "narration, dialogue, voice, speech, talking, spoken words"
VEO_AMBIENT_VOLUME = 0.15  # Veo ambient audio level (0-1) when mixed with TTS
VEO_PARALLEL_WORKERS = 8   # Concurrent Veo generation requests


def resolve_config_path(name_or_path: str) -> Path:
    """
    Resolve a config name or path to an actual file.
    Accepts: 'manual-paperback', '_quarto-manual-paperback.yml', or a full path.
    """
    # Already a full path or filename with _quarto- prefix
    candidate = PROJECT_ROOT / name_or_path
    if candidate.exists():
        return candidate

    # Try as a config name -> _quarto-{name}.yml
    candidate = PROJECT_ROOT / f"_quarto-{name_or_path}.yml"
    if candidate.exists():
        return candidate

    raise FileNotFoundError(
        f"Config not found: tried '{name_or_path}' and '_quarto-{name_or_path}.yml' in {PROJECT_ROOT}"
    )


def get_available_configs() -> list[str]:
    """Discover available config names from _quarto-*.yml files."""
    configs = []
    for yml in PROJECT_ROOT.glob("_quarto-*.yml"):
        name = yml.stem.replace("_quarto-", "")
        configs.append(name)
    return sorted(configs)


# --- Quarto Config Parsing ---

def extract_title_from_qmd(file_path: Path) -> str:
    """Extract title from QMD file's YAML frontmatter."""
    if not file_path.exists():
        return file_path.stem.replace('-', ' ').replace('_', ' ').title()
    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        # Quick YAML title extraction without full parse
        for line in match.group(1).split('\n'):
            m = re.match(r'^title:\s*["\']?(.+?)["\']?\s*$', line)
            if m:
                return m.group(1)
    return file_path.stem.replace('-', ' ').replace('_', ' ').title()


def extract_chapters_from_config(config_path: Path) -> list[dict]:
    """
    Extract ordered chapter list from a Quarto book YAML config.
    Starts with the index-source file, then processes chapters in config order.

    Returns list of dicts with: index, path, title, part
    """
    config = load_quarto_config(config_path)
    book = config.get('book', {})
    index_source = config.get('dih-render', {}).get('index-source')

    def resolve_path(path: str) -> str:
        if index_source and path == 'index.qmd':
            return index_source
        return path

    chapters = []
    chapter_index = 0

    for item in book.get('chapters', []):
        if isinstance(item, str):
            chapter_index += 1
            path = resolve_path(item)
            chapters.append({
                'index': chapter_index,
                'path': path,
                'title': None,
                'part': None,
            })
        elif isinstance(item, dict):
            if 'href' in item:
                chapter_index += 1
                path = resolve_path(item['href'])
                chapters.append({
                    'index': chapter_index,
                    'path': path,
                    'title': item.get('text'),
                    'part': None,
                })
            elif 'part' in item:
                part_name = item['part']
                for sub in item.get('chapters', []):
                    chapter_index += 1
                    if isinstance(sub, str):
                        chapters.append({
                            'index': chapter_index,
                            'path': resolve_path(sub),
                            'title': None,
                            'part': part_name,
                        })
                    elif isinstance(sub, dict) and 'href' in sub:
                        chapters.append({
                            'index': chapter_index,
                            'path': resolve_path(sub['href']),
                            'title': sub.get('text'),
                            'part': part_name,
                        })

    # Resolve titles from QMD files where missing
    for ch in chapters:
        if not ch['title']:
            ch['title'] = extract_title_from_qmd(PROJECT_ROOT / ch['path'])

    return chapters


# --- Chapter File Resolution ---

def find_prepared_text(chapter: dict) -> Path | None:
    """Find the prepared audiobook text file for a chapter."""
    safe_title = re.sub(r'[^\w\s-]', '', chapter['title']).strip().replace(' ', '-')[:50]
    text_file = TEXT_DIR / f"{chapter['index']:03d}-{safe_title}.prepared.txt"
    if text_file.exists():
        return text_file
    # Fallback: match by chapter index prefix
    for f in TEXT_DIR.glob(f"{chapter['index']:03d}-*.prepared.txt"):
        return f
    return None


def find_chapter_audio(chapter: dict) -> Path | None:
    """Find the WAV audio file for a chapter."""
    safe_title = re.sub(r'[^\w\s-]', '', chapter['title']).strip().replace(' ', '-')[:50]
    audio_file = CHAPTER_AUDIO_DIR / f"{chapter['index']:03d}-{safe_title}.wav"
    if audio_file.exists():
        return audio_file
    for f in CHAPTER_AUDIO_DIR.glob(f"{chapter['index']:03d}-*.wav"):
        return f
    return None


def get_chapter_dir(chapter: dict) -> Path:
    """Get the scene directory for a chapter."""
    safe_title = re.sub(r'[^\w\s-]', '', chapter['title']).strip().replace(' ', '-')[:50]
    return SCENES_DIR / f"{chapter['index']:03d}-{safe_title}"


# --- JSON Extraction ---

def parse_json_array(response_text: str) -> list[dict]:
    """
    Extract a JSON array from LLM response text.
    Handles markdown code blocks and trailing text.
    """
    text = response_text.strip()
    # Strip markdown code blocks
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    text = text.strip()

    # Try direct parse first
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
    except json.JSONDecodeError:
        pass

    # Find the outermost balanced JSON array
    start = text.find('[')
    if start == -1:
        raise ValueError(f"No JSON array found in response: {text[:200]}...")

    depth = 0
    in_string = False
    escape_next = False
    for i in range(start, len(text)):
        c = text[i]
        if escape_next:
            escape_next = False
            continue
        if c == '\\' and in_string:
            escape_next = True
            continue
        if c == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                candidate = text[start:i + 1]
                return json.loads(candidate)

    raise ValueError(f"No balanced JSON array found in response: {text[:200]}...")


# --- Step A: Scene Segmentation ---

SCENE_SEGMENTATION_PROMPT = """Split this audiobook narration into visual scenes. Each scene is a stretch of narration that gets one visual on screen. Each scene becomes an 8-second video clip, so keep scenes short.

Rules:
- 80-150 characters per scene (roughly 6-10 seconds of narration)
- char_start/char_end are exact character offsets (no gaps, no overlaps)
- narration_text is the exact original text for that span
- Break at natural sentence or phrase boundaries

Return ONLY a JSON array:
[{{"scene_index": 1, "title": "Short Title", "narration_text": "exact text...", "char_start": 0, "char_end": 120}}]

Text:
---
{text}
---"""


def segment_scenes(text: str) -> list[dict]:
    """Use Gemini Flash to segment narration text into visual scenes."""
    print("Step A: Segmenting text into visual scenes...")
    prompt = SCENE_SEGMENTATION_PROMPT.format(text=text)
    response = generate_gemini_flash_content(prompt)
    scenes = parse_json_array(response)

    total_chars = len(text)
    if scenes:
        last_end = scenes[-1]['char_end']
        if abs(last_end - total_chars) > 10:
            print(f"  [WARN] Scene coverage ends at {last_end}, text is {total_chars} chars")

    print(f"  Segmented into {len(scenes)} scenes")
    for s in scenes:
        chars = len(s.get('narration_text', ''))
        pct = chars / total_chars * 100 if total_chars else 0
        print(f"    Scene {s['scene_index']}: {s['title']} ({chars} chars, ~{pct:.0f}%)")

    return scenes


# --- Step B: Timestamp Estimation ---

def estimate_timestamps(scenes: list[dict], total_chars: int, total_duration_ms: int) -> list[dict]:
    """Map char offsets to audio timestamps using linear interpolation."""
    print("Step B: Estimating audio timestamps...")
    for scene in scenes:
        scene['start_ms'] = int((scene['char_start'] / total_chars) * total_duration_ms)
        scene['end_ms'] = int((scene['char_end'] / total_chars) * total_duration_ms)
        scene['duration_ms'] = scene['end_ms'] - scene['start_ms']
        print(f"    Scene {scene['scene_index']}: {scene['start_ms']}ms - {scene['end_ms']}ms ({scene['duration_ms']}ms)")
    return scenes


# --- Step C: Keyframe Generation ---

def generate_keyframes(scenes: list[dict], chapter_dir: Path) -> list[dict]:
    """Generate keyframe images for each scene using Imagen."""
    print("Step C: Generating keyframe images...")
    keyframes_dir = chapter_dir / "keyframes"
    keyframes_dir.mkdir(parents=True, exist_ok=True)

    for scene in scenes:
        scene['keyframes'] = {}
        for aspect in ASPECT_RATIOS:
            aspect_tag = aspect.replace(":", "x")
            filename = f"scene-{scene['scene_index']:02d}-{aspect_tag}.jpg"
            output_path = keyframes_dir / filename

            if output_path.exists():
                print(f"    [CACHED] {filename}")
                scene['keyframes'][aspect] = f"keyframes/{filename}"
                continue

            prompt = f"{IMAGE_STYLE}\n\n{scene['narration_text']}"
            generate_image(
                prompt=prompt,
                output_path=output_path,
                aspect_ratio=aspect,
            )
            scene['keyframes'][aspect] = f"keyframes/{filename}"

    return scenes


# --- Step D: Veo Animation ---

def animate_keyframes(scenes: list[dict], chapter_dir: Path) -> list[dict]:
    """Animate each keyframe using Veo 3.1 with parallel requests."""
    print("Step D: Animating keyframes with Veo 3.1...")
    clips_dir = chapter_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    keyframes_dir = chapter_dir / "keyframes"

    # Initialize clips dict for all scenes
    for scene in scenes:
        scene['clips'] = {}

    # Build work items, skipping cached/missing
    work_items = []
    for scene in scenes:
        for aspect in ASPECT_RATIOS:
            aspect_tag = aspect.replace(":", "x")
            clip_filename = f"scene-{scene['scene_index']:02d}-{aspect_tag}.mp4"
            clip_path = clips_dir / clip_filename
            keyframe_filename = f"scene-{scene['scene_index']:02d}-{aspect_tag}.jpg"
            keyframe_path = keyframes_dir / keyframe_filename

            if clip_path.exists():
                print(f"    [CACHED] {clip_filename}")
                scene['clips'][aspect] = f"clips/{clip_filename}"
                continue

            if not keyframe_path.exists():
                print(f"    [SKIP] No keyframe for {clip_filename}")
                continue

            work_items.append((scene, aspect, keyframe_path, clip_path, clip_filename))

    if not work_items:
        print("    All clips cached.")
        return scenes

    print(f"    Generating {len(work_items)} clips ({VEO_PARALLEL_WORKERS} parallel workers)...")

    def _generate_one(item):
        scene, aspect, keyframe_path, clip_path, clip_filename = item
        generate_video(
            prompt=scene['narration_text'],
            first_frame_path=keyframe_path,
            output_path=clip_path,
            aspect_ratio=aspect,
            duration_seconds=8,
            negative_prompt=VEO_NEGATIVE_PROMPT,
        )
        return scene['scene_index'], aspect, f"clips/{clip_filename}"

    with ThreadPoolExecutor(max_workers=VEO_PARALLEL_WORKERS) as executor:
        futures = {executor.submit(_generate_one, item): item for item in work_items}
        for future in as_completed(futures):
            item = futures[future]
            scene_idx, aspect = item[0]['scene_index'], item[1]
            try:
                _, _, clip_rel = future.result()
                # Find the scene and update its clips
                for s in scenes:
                    if s['scene_index'] == scene_idx:
                        s['clips'][aspect] = clip_rel
                        break
            except Exception as e:
                print(f"    [ERROR] Scene {scene_idx} ({aspect}): {e}")

    return scenes


# --- Step E: Assembly ---

def assemble_chapter_video(
    scenes: list[dict],
    chapter: dict,
    chapter_dir: Path,
    aspect: str,
) -> Path | None:
    """
    Assemble scene clips + audio into a chapter-level MP4.

    Keeps Veo ambient audio (music/SFX) at reduced volume and mixes
    with TTS narration at full volume.
    """
    aspect_tag = aspect.replace(":", "x")
    safe_title = re.sub(r'[^\w\s-]', '', chapter['title']).strip().replace(' ', '-')[:50]
    output_path = VIDEO_DIR / f"{chapter['index']:03d}-{safe_title}-{aspect_tag}.mp4"

    audio_path = find_chapter_audio(chapter)
    if not audio_path:
        print(f"  [SKIP] No audio file for chapter {chapter['index']}")
        return None

    clips_dir = chapter_dir / "clips"

    clip_entries = []
    for scene in scenes:
        clip_rel = scene.get('clips', {}).get(aspect)
        if not clip_rel:
            print(f"  [SKIP] No clip for scene {scene['scene_index']} ({aspect})")
            return None
        clip_path = chapter_dir / clip_rel
        if not clip_path.exists():
            print(f"  [SKIP] Clip file missing: {clip_path}")
            return None
        clip_entries.append((clip_path, scene['duration_ms']))

    print(f"  Assembling {aspect} video ({len(clip_entries)} scenes)...")

    # Step 1: Speed-adjust each clip to match its scene duration (keep audio)
    temp_clips = []
    concat_lines = []

    for i, (clip_path, target_ms) in enumerate(clip_entries):
        target_seconds = max(1.0, target_ms / 1000.0)

        # Get actual clip duration via ffprobe
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(clip_path),
        ]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        clip_duration = float(probe_result.stdout.strip()) if probe_result.returncode == 0 else 8.0

        # Calculate speed adjustment
        time_scale = target_seconds / clip_duration
        speed_factor = 1.0 / time_scale  # atempo: >1 = faster, <1 = slower

        adjusted_path = clips_dir / f"_adjusted-{i:02d}-{aspect_tag}.mp4"

        if abs(time_scale - 1.0) < 0.02:
            # Close enough, just trim/pad without speed change
            cmd = [
                "ffmpeg", "-y",
                "-i", str(clip_path),
                "-t", f"{target_seconds:.3f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart",
                str(adjusted_path),
            ]
        else:
            # Speed-adjust video and audio
            # Clamp atempo to valid range (0.5 - 100.0)
            atempo = max(0.5, min(100.0, speed_factor))
            print(f"    Scene {i+1}: {clip_duration:.1f}s -> {target_seconds:.1f}s ({time_scale:.2f}x)")
            cmd = [
                "ffmpeg", "-y",
                "-i", str(clip_path),
                "-filter_complex",
                f"[0:v]setpts=PTS*{time_scale:.4f}[v];[0:a]atempo={atempo:.4f}[a]",
                "-map", "[v]", "-map", "[a]",
                "-t", f"{target_seconds:.3f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart",
                str(adjusted_path),
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    [ERROR] ffmpeg adjust failed for scene {i+1}: {result.stderr[:200]}")
            return None

        temp_clips.append(adjusted_path)
        concat_lines.append(f"file '{adjusted_path.as_posix()}'")

    # Step 2: Concat all adjusted clips (video + Veo ambient audio)
    concat_file = clips_dir / f"_concat-{aspect_tag}.txt"
    concat_file.write_text('\n'.join(concat_lines), encoding='utf-8')

    # Step 3: Mix Veo ambient audio (reduced) with TTS narration (full volume)
    # [0:a] = Veo ambient (music/SFX), [1:a] = TTS narration
    vol = VEO_AMBIENT_VOLUME
    filter_complex = (
        f"[0:a]volume={vol}[veo];"
        f"[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=mono[tts];"
        f"[veo][tts]amix=inputs=2:duration=longest:dropout_transition=2[mixed]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-i", str(audio_path),
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[mixed]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        "-metadata", f"title={chapter['title']}",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    [ERROR] ffmpeg mix failed: {result.stderr[:300]}")
        # Fallback: try without Veo audio mixing (just TTS)
        print(f"    [FALLBACK] Trying TTS-only audio...")
        cmd_fallback = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_file),
            "-i", str(audio_path),
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-map", "0:v", "-map", "1:a",
            "-shortest",
            "-movflags", "+faststart",
            "-metadata", f"title={chapter['title']}",
            str(output_path),
        ]
        result = subprocess.run(cmd_fallback, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    [ERROR] ffmpeg fallback failed: {result.stderr[:300]}")
            for tc in temp_clips:
                tc.unlink(missing_ok=True)
            concat_file.unlink(missing_ok=True)
            return None

    for tc in temp_clips:
        tc.unlink(missing_ok=True)
    concat_file.unlink(missing_ok=True)

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"  [OK] {output_path.name} ({size_mb:.1f} MB)")
    return output_path


# --- Scene Manifest ---

def save_scene_manifest(scenes: list[dict], chapter: dict, chapter_dir: Path, total_duration_ms: int):
    """Save scene-manifest.json with all scene metadata."""
    manifest = {
        "chapter_index": chapter['index'],
        "chapter_title": chapter['title'],
        "total_chars": len(scenes[-1].get('narration_text', '')) if scenes else 0,
        "total_duration_ms": total_duration_ms,
        "model_used": GEMINI_FLASH_MODEL_ID,
        "scenes": scenes,
    }
    # Compute total chars from scene coverage
    if scenes:
        manifest['total_chars'] = max(s.get('char_end', 0) for s in scenes)

    manifest_path = chapter_dir / "scene-manifest.json"
    chapter_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"  Scene manifest saved: {manifest_path}")


def load_scene_manifest(chapter_dir: Path) -> dict | None:
    """Load existing scene-manifest.json if present."""
    manifest_path = chapter_dir / "scene-manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding='utf-8'))
    return None


# --- Update Audiobook Manifest ---

def update_audiobook_manifest(chapter_index: int, video_16x9: Path | None, video_9x16: Path | None, scene_count: int):
    """Add video fields to audiobook/manifest.json for a chapter."""
    if not MANIFEST_PATH.exists():
        return
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    for ch in manifest.get('chapters', []):
        if ch['index'] == chapter_index:
            if video_16x9:
                ch['video_16x9'] = str(video_16x9.relative_to(PROJECT_ROOT))
            if video_9x16:
                ch['video_9x16'] = str(video_9x16.relative_to(PROJECT_ROOT))
            ch['scenes'] = scene_count
            ch['video_status'] = "generated"
            break
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"  Audiobook manifest updated for chapter {chapter_index}")


# --- List Command ---

def list_chapters(chapters: list[dict]):
    """Print all chapters with their video generation status."""
    print(f"\nChapter Video Status ({len(chapters)} chapters):")
    print("=" * 90)

    current_part = None
    for ch in chapters:
        if ch['part'] != current_part:
            current_part = ch['part']
            if current_part:
                print(f"\n  [{current_part}]")

        chapter_dir = get_chapter_dir(ch)
        scene_manifest = load_scene_manifest(chapter_dir)
        scene_count = len(scene_manifest['scenes']) if scene_manifest else 0

        text_file = find_prepared_text(ch)
        audio_file = find_chapter_audio(ch)
        text_chars = len(text_file.read_text(encoding='utf-8')) if text_file else 0

        has_video = False
        if VIDEO_DIR.exists():
            for ar in ASPECT_RATIOS:
                pattern = f"{ch['index']:03d}-*-{ar.replace(':', 'x')}.mp4"
                if next(VIDEO_DIR.glob(pattern), None):
                    has_video = True
                    break

        status_parts = []
        if text_file:
            status_parts.append("T")
        if audio_file:
            status_parts.append("A")
        if scene_count:
            status_parts.append(f"S{scene_count}")
        if has_video:
            status_parts.append("V")

        status = ",".join(status_parts) if status_parts else "-"
        chars_info = f"{text_chars:,} chars" if text_chars else "no text"
        print(f"    {ch['index']:3d}. [{status:>8s}] {ch['title']} ({chars_info})")

    print("=" * 90)
    print("  Legend: T=text, A=audio, S#=scenes, V=video")


# --- Main Pipeline ---

def run_pipeline(chapter: dict, scenes_only: bool = False, keyframes_only: bool = False, force: bool = False, max_scenes: int | None = None):
    """Run the video generation pipeline for a single chapter."""
    print(f"\n{'=' * 60}")
    print(f"Chapter {chapter['index']}: {chapter['title']}")
    print(f"  QMD: {chapter['path']}")
    print(f"{'=' * 60}")

    chapter_dir = get_chapter_dir(chapter)
    chapter_dir.mkdir(parents=True, exist_ok=True)

    # Load prepared text
    text_file = find_prepared_text(chapter)
    if not text_file:
        print(f"  [SKIP] No prepared text file for chapter {chapter['index']}.")
        print(f"  Run audiobook:text first: npm run audiobook:text -- --chapter {chapter['index']}")
        return

    text = text_file.read_text(encoding='utf-8')
    total_chars = len(text)
    print(f"Text: {total_chars:,} chars ({text_file.name})")

    # Get audio duration
    audio_path = find_chapter_audio(chapter)
    if audio_path:
        audio = AudioSegment.from_wav(str(audio_path))
        total_duration_ms = len(audio)
        print(f"Audio: {total_duration_ms:,}ms ({total_duration_ms / 1000:.1f}s)")
    else:
        # Estimate: ~150 wpm, ~5 chars/word
        total_duration_ms = int((total_chars / 5 / 150) * 60 * 1000)
        print(f"Audio: not found, estimated {total_duration_ms:,}ms")

    # Check for existing scene manifest
    existing = load_scene_manifest(chapter_dir)
    if existing and existing.get('scenes') and not force:
        print(f"  Found existing scene manifest ({len(existing['scenes'])} scenes)")
        scenes = existing['scenes']
    else:
        if force and existing:
            print(f"  --force: re-segmenting (was {len(existing.get('scenes', []))} scenes)")
        scenes = segment_scenes(text)

    if max_scenes and len(scenes) > max_scenes:
        print(f"  --max-scenes {max_scenes}: truncating from {len(scenes)} scenes")
        scenes = scenes[:max_scenes]

    scenes = estimate_timestamps(scenes, total_chars, total_duration_ms)
    save_scene_manifest(scenes, chapter, chapter_dir, total_duration_ms)

    if scenes_only:
        print("\n--scenes-only: stopping after scene segmentation.")
        return

    scenes = generate_keyframes(scenes, chapter_dir)
    save_scene_manifest(scenes, chapter, chapter_dir, total_duration_ms)

    if keyframes_only:
        print("\n--keyframes-only: stopping after keyframe generation.")
        return

    scenes = animate_keyframes(scenes, chapter_dir)
    save_scene_manifest(scenes, chapter, chapter_dir, total_duration_ms)

    print("\nStep E: Assembling final videos...")
    video_16x9 = assemble_chapter_video(scenes, chapter, chapter_dir, "16:9")
    video_9x16 = assemble_chapter_video(scenes, chapter, chapter_dir, "9:16")

    print("\nStep F: Updating manifest...")
    update_audiobook_manifest(chapter['index'], video_16x9, video_9x16, len(scenes))

    print(f"\nDone! Chapter {chapter['index']}: {chapter['title']}")
    if video_16x9:
        print(f"  16:9: {video_16x9}")
    if video_9x16:
        print(f"  9:16: {video_9x16}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate audiobook video from Quarto book chapters using LLM scenes + Veo animation"
    )
    available = get_available_configs()
    parser.add_argument(
        "config",
        nargs="?",
        default=DEFAULT_CONFIG_NAME,
        help=f"Config name or YAML file (default: {DEFAULT_CONFIG_NAME}). Available: {', '.join(available)}"
    )
    parser.add_argument(
        "--start", "-s",
        type=int,
        help="Start from this chapter number (inclusive)"
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        help="Max number of chapters to process"
    )
    parser.add_argument(
        "--scenes-only",
        action="store_true",
        help="Only run scene segmentation (dry run, no image/video generation)"
    )
    parser.add_argument(
        "--keyframes-only",
        action="store_true",
        help="Run scene segmentation + keyframe generation, skip Veo animation"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all chapters with video generation status"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force re-segmentation even if scene manifest exists"
    )
    parser.add_argument(
        "--max-scenes",
        type=int,
        help="Limit number of scenes to process (for quick testing)"
    )
    args = parser.parse_args()

    try:
        config_path = resolve_config_path(args.config)
    except FileNotFoundError as e:
        parser.error(str(e))

    print(f"Config: {config_path.name}")
    chapters = extract_chapters_from_config(config_path)
    print(f"Found {len(chapters)} chapters")

    if args.list:
        list_chapters(chapters)
        return

    # Apply start/limit filters
    if args.start:
        chapters = [ch for ch in chapters if ch['index'] >= args.start]
    if args.limit:
        chapters = chapters[:args.limit]
    if args.start or args.limit:
        print(f"Processing {len(chapters)} chapter(s)")

    if not chapters:
        print("No chapters to process.")
        return

    for chapter in chapters:
        run_pipeline(
            chapter=chapter,
            scenes_only=args.scenes_only,
            keyframes_only=args.keyframes_only,
            force=args.force,
            max_scenes=args.max_scenes,
        )

    print(f"\n{'=' * 60}")
    print(f"All done! Processed {len(chapters)} chapter(s).")


if __name__ == "__main__":
    main()
