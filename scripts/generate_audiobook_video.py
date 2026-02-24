#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Video Generator

Generates animated video for audiobook chapters using:
1. Pre-existing scene-manifest.json (from generate_audiobook_scenes.py)
2. Keyframe image generation (Imagen)
3. Video animation (Veo 3.1)
4. Assembly with ffmpeg

Requires scene-manifest.json and audio to exist already. Run the earlier pipeline
steps first: generate_audiobook_text.py -> generate_audiobook.py -> generate_audiobook_scenes.py

Usage:
    python scripts/generate_audiobook_video.py --chapter 20 --keyframes-only
    python scripts/generate_audiobook_video.py --chapter 20
    python scripts/generate_audiobook_video.py --list
"""
import io
import sys
import re
import hashlib
import argparse
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if sys.platform == 'win32' and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

from pydub import AudioSegment

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.llm import generate_gemini_flash_content_with_image
from lib.veo import generate_image, generate_video
from dih_models.yaml_utils import load_quarto_config
from generate_audiobook import extract_book_metadata
from lib.audiobook_common import (
    PROJECT_ROOT, VIDEO_DIR, SCENES_DIR,
    extract_chapters as _extract_chapters,
    extract_title_from_qmd, safe_filename, chapter_slug,
    find_prepared_text, find_chapter_audio,
    resolve_chapter_titles,
    AudiobookPaths, config_name_from_path, get_paths,
    resolve_config_path, get_available_configs,
)
from lib.audiobook_manifest import update_chapter_fields as _update_chapter_fields
from lib.retry import RateLimiter
from lib.scenes import save_scene_manifest, load_scene_manifest

# --- Configuration ---
DEFAULT_CONFIG_NAME = "manual-paperback"

ASPECT_RATIOS = ["16:9", "9:16"]

# Video keyframe style (distinct from BW_ACADEMIC_STYLE used for book section images)
IMAGE_STYLE = "70s sci-fi surrealism"

# --- Prompt Variants ---
# Each variant is a function(scene_text, full_context, attempt) -> str
# scene_text = narration text for this scene (visual-cleaned)
# full_context = full chapter text (visual-cleaned)
# attempt = typo retry attempt (1=normal, 2=spell correctly, 3=no text)

def _prompt_original(scene_text, full_context, attempt):
    """Original: style + raw narration + full chapter context."""
    prompt = (
        f"Generate a {IMAGE_STYLE} illustration.\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---"
        )
    return prompt

def _prompt_metaphor(scene_text, full_context, attempt):
    """Original + metaphor instruction."""
    prompt = (
        f"Generate a {IMAGE_STYLE} illustration. Interpret metaphors visually; do not depict them literally.\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---"
        )
    return prompt

def _prompt_powerpoint(scene_text, full_context, attempt):
    """Two-step: conceptualize as presentation slide, then render as 70s sci-fi."""
    prompt = (
        f"Imagine how this concept would be depicted on a presentation slide given the full chapter context below. "
        f"Then generate that image in the style of a {IMAGE_STYLE} paperback book cover illustration.\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---"
        )
    return prompt

def _prompt_bookcover(scene_text, full_context, attempt):
    """Direct book cover framing."""
    prompt = (
        f"Generate an illustration for the cover of a {IMAGE_STYLE} paperback novel that captures this moment in the story:\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---"
        )
    return prompt

PROMPT_VARIANTS = {
    "original": _prompt_original,
    "metaphor": _prompt_metaphor,
    "powerpoint": _prompt_powerpoint,
    "bookcover": _prompt_bookcover,
}
DEFAULT_PROMPT_VARIANT = "original"

# Suppress Veo-generated speech so we can overlay our own TTS narration.
# Veo ambient audio (music + SFX) is kept and mixed at reduced volume.
VEO_NEGATIVE_PROMPT = "narration, dialogue, voice, speech, talking, spoken words"
VEO_AMBIENT_VOLUME = 0.15  # Veo ambient audio level (0-1) when mixed with TTS
VEO_PARALLEL_WORKERS = 8   # Concurrent Veo generation requests


# --- Quarto Config Parsing ---

def extract_chapters_from_config(config_path: Path) -> list[dict]:
    """Extract ordered chapter list from a Quarto book YAML config."""
    config = load_quarto_config(config_path)
    chapters = _extract_chapters(config)
    return resolve_chapter_titles(chapters)


# --- Chapter File Resolution ---

def get_chapter_dir(chapter: dict, paths: AudiobookPaths | None = None) -> Path:
    """Get the scene directory for a chapter."""
    scenes_dir = paths.scenes if paths else SCENES_DIR
    return scenes_dir / f"{chapter['index']:03d}-{chapter_slug(chapter)}"



def _narration_hash(scene: dict) -> str:
    """Compute a short hash of a scene's narration text for cache invalidation."""
    text = scene.get('narration_text')
    if not text:
        raise ValueError(
            f"Scene {scene.get('scene_index', '?')} has no narration_text. "
            f"Re-run scene segmentation to fix."
        )
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


# Imagen: 20 requests per minute
imagen_rate_limiter = RateLimiter(max_requests=18, window_seconds=60)  # 18 to stay safely under 20


def rate_limited_generate_image(prompt: str, output_path: Path, aspect_ratio: str, negative_prompt: str | None = None) -> Path:
    """Wrapper around generate_image that respects the Imagen rate limit."""
    imagen_rate_limiter.acquire()
    return generate_image(prompt=prompt, output_path=output_path, aspect_ratio=aspect_ratio, negative_prompt=negative_prompt)


# --- Image/Video Metadata ---

def _tag_image_metadata(image_path: Path, chapter: dict, scene: dict, book_meta: dict | None):
    """Embed EXIF/IPTC metadata into a JPEG keyframe image."""
    if not book_meta or not image_path.exists():
        return
    try:
        from PIL import Image as PILImage
        from PIL.PngImagePlugin import PngInfo
        img = PILImage.open(image_path)
        exif = img.getexif()
        # EXIF tags: 270=ImageDescription, 315=Artist, 305=Software, 40091=Title (XP)
        exif[270] = f"Chapter {chapter['index']}: {chapter['title']} - Scene {scene['scene_index']}: {scene.get('title', '')}"
        exif[315] = book_meta['author']
        exif[305] = f"Imagen 4.0 / {book_meta['title']}"
        img.save(image_path, exif=exif.tobytes())
    except Exception:
        pass  # metadata tagging is best-effort


# --- Step C: Keyframe Generation (with inline typo checking) ---

IMAGEN_PARALLEL_WORKERS = 4  # Concurrent Imagen requests
MAX_KEYFRAME_ATTEMPTS = 3    # Generate + check up to 3 times before crashing

KEYFRAME_TEXT_CHECK_PROMPT = """70s sci-fi surrealism image. Only flag text that is large, prominent, and clearly a misspelling of a real English word (e.g. "SCIENEC" instead of "SCIENCE"). Ignore small, decorative, atmospheric, alien, or garbled text on screens/signs/labels (normal for this style). If there are no obvious prominent misspellings, answer CLEAN.

Valid proper nouns: Wishonia, Moronia, Gollum, Gollums, Wishocracy, DALY, DALYs.

Answer ONLY: "CLEAN" or "TYPO: <description>"."""


def _check_keyframe_for_typos(image_path: Path) -> str | None:
    """Check a keyframe image for typos. Returns None if clean, or description if typo found."""
    image_bytes = image_path.read_bytes()
    mime = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    response = generate_gemini_flash_content_with_image(
        prompt=KEYFRAME_TEXT_CHECK_PROMPT,
        image_bytes=image_bytes,
        mime_type=mime,
    )
    result = response.strip()
    if result.upper().startswith("CLEAN"):
        return None
    return result


# --- TTS-to-visual text conversion ---

def _tts_to_visual(text: str) -> str:
    """Convert TTS-formatted text back to visual format for image prompts.

    The prepared text spells out numbers for TTS. We reverse the most
    visually important one: "one percent" -> "1%".
    """
    if not text:
        return text
    text = re.sub(r'\bone percent\b', '1%', text, flags=re.IGNORECASE)
    return text


def generate_keyframes(scenes: list[dict], chapter_dir: Path, chapter: dict | None = None, book_meta: dict | None = None, chapter_text: str = "", prompt_variant: str = DEFAULT_PROMPT_VARIANT) -> list[dict]:
    """Generate keyframe images for each scene using Imagen (parallel), with inline typo checking."""
    print("Step C: Generating keyframe images (with typo checking)...")
    keyframes_dir = chapter_dir / "keyframes"
    keyframes_dir.mkdir(parents=True, exist_ok=True)

    for scene in scenes:
        scene['keyframes'] = {}

    work_items = []
    for scene in scenes:
        nh = _narration_hash(scene)
        old_hash = scene.get('keyframe_hash', '')
        stale = old_hash and old_hash != nh

        for aspect in ASPECT_RATIOS:
            aspect_tag = aspect.replace(":", "x")
            filename = f"scene-{scene['scene_index']:02d}-{aspect_tag}.jpg"
            output_path = keyframes_dir / filename

            if output_path.exists() and not stale:
                print(f"    [CACHED] {filename}")
                scene['keyframes'][aspect] = f"keyframes/{filename}"
                continue

            if output_path.exists() and stale:
                print(f"    [STALE] {filename} narration changed ({old_hash} -> {nh})")
                output_path.unlink()

            work_items.append((scene, aspect, output_path, filename))

    if not work_items:
        print("    All keyframes cached.")
        return scenes

    print(f"    Generating {len(work_items)} keyframes ({IMAGEN_PARALLEL_WORKERS} parallel workers)...")

    def _build_prompt(scene, attempt=1, variant_name=None):
        scene_text = _tts_to_visual(scene['narration_text'].strip())
        full_context = _tts_to_visual(chapter_text) if chapter_text else ""
        vname = variant_name or prompt_variant
        prompt_fn = PROMPT_VARIANTS[vname]
        prompt = prompt_fn(scene_text, full_context, attempt)
        if attempt == 2:
            prompt += "\n\nAny text in the image must be spelled correctly."
        elif attempt >= 3:
            prompt += "\n\nDo NOT include any text, signs, labels, writing, or words of any kind in this image."
        return prompt

    def _generate_and_check(item):
        scene, aspect, output_path, filename = item
        aspect_tag = aspect.replace(":", "x")
        label = f"scene-{scene['scene_index']:02d}-{aspect_tag}"

        for attempt in range(1, MAX_KEYFRAME_ATTEMPTS + 1):
            prompt = _build_prompt(scene, attempt=attempt)
            # Save rendered prompt to manifest for review (only on first attempt, first aspect)
            if attempt == 1 and 'imagen_prompt' not in scene:
                scene['imagen_prompt'] = prompt
            rate_limited_generate_image(prompt=prompt, output_path=output_path, aspect_ratio=aspect)

            typo = _check_keyframe_for_typos(output_path)
            if typo is None:
                if attempt > 1:
                    print(f"    [FIXED] {label} (attempt {attempt})")
                if chapter and book_meta:
                    _tag_image_metadata(output_path, chapter, scene, book_meta)
                return scene['scene_index'], aspect, f"keyframes/{filename}"

            print(f"    [TYPO] {label} (attempt {attempt}/{MAX_KEYFRAME_ATTEMPTS}): {typo}")
            if attempt < MAX_KEYFRAME_ATTEMPTS:
                output_path.unlink(missing_ok=True)

        # Accept the last image with a warning instead of crashing
        print(f"    [WARN] {label}: accepting image with typos after {MAX_KEYFRAME_ATTEMPTS} attempts")
        if chapter and book_meta:
            _tag_image_metadata(output_path, chapter, scene, book_meta)
        return scene['scene_index'], aspect, f"keyframes/{filename}"

    errors = []
    with ThreadPoolExecutor(max_workers=IMAGEN_PARALLEL_WORKERS) as executor:
        futures = {executor.submit(_generate_and_check, item): item for item in work_items}
        for future in as_completed(futures):
            item = futures[future]
            scene_idx, aspect = item[0]['scene_index'], item[1]
            try:
                _, _, kf_rel = future.result()
                for s in scenes:
                    if s['scene_index'] == scene_idx:
                        s['keyframes'][aspect] = kf_rel
                        # Store narration hash so we can detect stale keyframes later
                        s['keyframe_hash'] = _narration_hash(s)
                        break
            except Exception as e:
                errors.append(str(e))
                print(f"    [ERROR] {e}")

    if errors:
        raise RuntimeError(f"Failed to generate {len(errors)} keyframe(s):\n" + "\n".join(errors))

    return scenes


# --- Prompt A/B Testing ---

def test_prompt_variants(scenes: list[dict], chapter_dir: Path, chapter_text: str = "", variants: list[str] | None = None, max_scenes: int | None = None):
    """Generate one 16:9 keyframe per variant per scene for side-by-side comparison.

    Output structure:
        chapter_dir/prompt-tests/
            original/scene-01.jpg
            metaphor/scene-01.jpg
            powerpoint/scene-01.jpg
            bookcover/scene-01.jpg
    """
    variants = variants or list(PROMPT_VARIANTS.keys())
    test_scenes = scenes[:max_scenes] if max_scenes else scenes
    test_dir = chapter_dir / "prompt-tests"

    total = len(variants) * len(test_scenes)
    print(f"\nPrompt A/B test: {len(variants)} variants x {len(test_scenes)} scenes = {total} images")
    print(f"  Output: {test_dir}")
    print(f"  Variants: {', '.join(variants)}")

    work_items = []
    for vname in variants:
        variant_dir = test_dir / vname
        variant_dir.mkdir(parents=True, exist_ok=True)
        for scene in test_scenes:
            scene_text = _tts_to_visual(scene['narration_text'].strip())
            full_context = _tts_to_visual(chapter_text) if chapter_text else ""
            prompt_fn = PROMPT_VARIANTS[vname]
            prompt = prompt_fn(scene_text, full_context, attempt=1)
            output_path = variant_dir / f"scene-{scene['scene_index']:02d}.jpg"
            if output_path.exists():
                print(f"  [CACHED] {vname}/scene-{scene['scene_index']:02d}.jpg")
                continue
            work_items.append((vname, scene['scene_index'], prompt, output_path))

    if not work_items:
        print("  All test images cached.")
        return

    print(f"  Generating {len(work_items)} images ({IMAGEN_PARALLEL_WORKERS} parallel)...")

    def _gen(item):
        vname, scene_idx, prompt, output_path = item
        rate_limited_generate_image(prompt=prompt, output_path=output_path, aspect_ratio="16:9")
        return vname, scene_idx

    errors = []
    with ThreadPoolExecutor(max_workers=IMAGEN_PARALLEL_WORKERS) as executor:
        futures = {executor.submit(_gen, item): item for item in work_items}
        for future in as_completed(futures):
            try:
                vname, scene_idx = future.result()
                print(f"  [OK] {vname}/scene-{scene_idx:02d}.jpg")
            except Exception as e:
                item = futures[future]
                errors.append(f"{item[0]}/scene-{item[1]:02d}: {e}")
                print(f"  [ERROR] {item[0]}/scene-{item[1]:02d}: {e}")

    if errors:
        print(f"\n  {len(errors)} errors during prompt testing:")
        for err in errors:
            print(f"    {err}")
    else:
        print(f"\n  All {total} test images generated!")
    print(f"  Compare results in: {test_dir}")


# --- Step D: Veo Animation ---

def animate_scenes(scenes: list[dict], chapter_dir: Path, use_keyframes: bool = True, chapter_text: str = "") -> list[dict]:
    """Generate video clips using Veo 3.1 with parallel requests.

    When use_keyframes=True (default), uses image-to-video with keyframe as first frame.
    When use_keyframes=False, uses text-to-video from animation prompt only.
    """
    mode = "image-to-video" if use_keyframes else "text-to-video"
    print(f"Step D: Generating video clips with Veo 3.1 ({mode})...")
    clips_dir = chapter_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    keyframes_dir = chapter_dir / "keyframes"

    # Initialize clips dict for all scenes
    for scene in scenes:
        scene['clips'] = {}

    # Build work items, skipping cached/missing
    work_items = []
    for scene in scenes:
        nh = _narration_hash(scene)
        old_hash = scene.get('clip_hash', '')
        stale = old_hash and old_hash != nh

        for aspect in ASPECT_RATIOS:
            aspect_tag = aspect.replace(":", "x")
            clip_filename = f"scene-{scene['scene_index']:02d}-{aspect_tag}.mp4"
            clip_path = clips_dir / clip_filename

            if clip_path.exists() and not stale:
                print(f"    [CACHED] {clip_filename}")
                scene['clips'][aspect] = f"clips/{clip_filename}"
                continue

            if clip_path.exists() and stale:
                print(f"    [STALE] {clip_filename} narration changed ({old_hash} -> {nh})")
                clip_path.unlink()

            keyframe_path = None
            if use_keyframes:
                keyframe_filename = f"scene-{scene['scene_index']:02d}-{aspect_tag}.jpg"
                keyframe_path = keyframes_dir / keyframe_filename
                if not keyframe_path.exists():
                    raise FileNotFoundError(f"Missing keyframe: {keyframe_path}")

            work_items.append((scene, aspect, keyframe_path, clip_path, clip_filename))

    if not work_items:
        print("    All clips cached.")
        return scenes

    print(f"    Generating {len(work_items)} clips ({VEO_PARALLEL_WORKERS} parallel workers)...")

    def _generate_one(item):
        scene, aspect, keyframe_path, clip_path, clip_filename = item
        scene_text = _tts_to_visual(scene['narration_text'].strip())
        full_context = _tts_to_visual(chapter_text) if chapter_text else ""
        veo_prompt = f"Generate a {IMAGE_STYLE} animation. Interpret metaphors visually; do not depict them literally.\n--- ILLUSTRATE THIS ---\n{scene_text}\n--- END ILLUSTRATE ---\n"
        if full_context:
            veo_prompt += f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n{full_context}\n--- END CONTEXT ---\n"
        veo_prompt += "No dialogue, narration, or speech."
        # Save rendered prompt to manifest for review (only first aspect)
        if 'veo_prompt' not in scene:
            scene['veo_prompt'] = veo_prompt
        generate_video(
            prompt=veo_prompt,
            output_path=clip_path,
            first_frame_path=keyframe_path,
            aspect_ratio=aspect,
            duration_seconds=8,
            negative_prompt=VEO_NEGATIVE_PROMPT,
        )
        return scene['scene_index'], aspect, f"clips/{clip_filename}"

    errors = []
    with ThreadPoolExecutor(max_workers=VEO_PARALLEL_WORKERS) as executor:
        futures = {executor.submit(_generate_one, item): item for item in work_items}
        for future in as_completed(futures):
            item = futures[future]
            scene_idx, aspect = item[0]['scene_index'], item[1]
            try:
                _, _, clip_rel = future.result()
                for s in scenes:
                    if s['scene_index'] == scene_idx:
                        s['clips'][aspect] = clip_rel
                        # Store narration hash so we can detect stale clips later
                        s['clip_hash'] = _narration_hash(s)
                        break
            except Exception as e:
                errors.append(f"Clip scene {scene_idx} ({aspect}): {e}")
                print(f"    [ERROR] Scene {scene_idx} ({aspect}): {e}")

    if errors:
        raise RuntimeError(f"Failed to generate {len(errors)} clip(s):\n" + "\n".join(errors))

    return scenes


# --- Step E: Assembly ---

def assemble_chapter_video(
    scenes: list[dict],
    chapter: dict,
    chapter_dir: Path,
    aspect: str,
    book_meta: dict | None = None,
    paths: AudiobookPaths | None = None,
) -> Path:
    """
    Assemble scene clips + audio into a chapter-level MP4.

    Keeps Veo ambient audio (music/SFX) at reduced volume and mixes
    with TTS narration at full volume.
    """
    video_dir = paths.video if paths else VIDEO_DIR
    aspect_tag = aspect.replace(":", "x")
    slug = chapter_slug(chapter)
    output_path = video_dir / f"{chapter['index']:03d}-{slug}-{aspect_tag}.mp4"

    audio_path = find_chapter_audio(chapter, paths=paths)
    if not audio_path:
        raise FileNotFoundError(f"No audio file for chapter {chapter['index']}. Run audiobook:audio first.")

    clips_dir = chapter_dir / "clips"

    # Get actual audio duration for padding calculation
    audio_duration_ms = len(AudioSegment.from_file(str(audio_path)))

    clip_entries = []
    for scene in scenes:
        clip_rel = scene.get('clips', {}).get(aspect)
        if not clip_rel:
            raise FileNotFoundError(f"No clip for scene {scene['scene_index']} ({aspect})")
        clip_path = chapter_dir / clip_rel
        if not clip_path.exists():
            raise FileNotFoundError(f"Clip file missing: {clip_path}")
        clip_entries.append((clip_path, scene['duration_ms']))

    # Ensure total video duration covers full audio (add 1s buffer to last clip)
    total_scene_ms = sum(ms for _, ms in clip_entries)
    if total_scene_ms < audio_duration_ms:
        gap = audio_duration_ms - total_scene_ms + 1000  # 1s buffer
        path, ms = clip_entries[-1]
        clip_entries[-1] = (path, ms + gap)
        print(f"  [FIX] Last clip extended by {gap}ms to cover audio ({audio_duration_ms}ms)")

    print(f"  Assembling {aspect} video ({len(clip_entries)} scenes, target {sum(ms for _,ms in clip_entries)/1000:.1f}s for {audio_duration_ms/1000:.1f}s audio)...")

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
            raise RuntimeError(f"ffmpeg adjust failed for scene {i+1}: {result.stderr[:300]}")

        temp_clips.append(adjusted_path)
        concat_lines.append(f"file '{adjusted_path.as_posix()}'")

    # Step 2: Concat all adjusted clips (video + Veo ambient audio)
    concat_file = clips_dir / f"_concat-{aspect_tag}.txt"
    concat_file.write_text('\n'.join(concat_lines), encoding='utf-8')

    # Step 3: Mix Veo ambient audio (reduced) with TTS narration (full volume)
    # [0:a] = Veo ambient (music/SFX), [1:a] = TTS narration
    # Use TTS duration as the master (duration=first refers to first input of amix = veo,
    # but we want TTS to control length). We use duration=longest so the full TTS plays,
    # and the video track (which we've padded to be >= audio) gets trimmed by -t.
    audio_duration_s = audio_duration_ms / 1000.0
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
        "-t", f"{audio_duration_s:.3f}",
        "-movflags", "+faststart",
        "-metadata", f"title={chapter['title']}",
    ]
    if book_meta:
        cmd.extend([
            "-metadata", f"artist={book_meta['author']}",
            "-metadata", f"album={book_meta['title']}",
            "-metadata", f"genre=Audiobook",
            "-metadata", f"track={chapter['index']}",
            "-metadata", f"comment={book_meta['description']}",
            "-metadata", f"date={book_meta['year']}",
        ])
    cmd.append(str(output_path))
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
            "-t", f"{audio_duration_s:.3f}",
            "-movflags", "+faststart",
            "-metadata", f"title={chapter['title']}",
            str(output_path),
        ]
        result = subprocess.run(cmd_fallback, capture_output=True, text=True)
        if result.returncode != 0:
            for tc in temp_clips:
                tc.unlink(missing_ok=True)
            concat_file.unlink(missing_ok=True)
            raise RuntimeError(f"ffmpeg assembly failed (both mix and fallback): {result.stderr[:300]}")

    for tc in temp_clips:
        tc.unlink(missing_ok=True)
    concat_file.unlink(missing_ok=True)

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"  [OK] {output_path.name} ({size_mb:.1f} MB)")
    return output_path


# --- Update Audiobook Manifest ---

def update_audiobook_manifest(chapter_index: int, video_16x9: Path | None, video_9x16: Path | None, scene_count: int, paths: AudiobookPaths | None = None):
    """Add video fields to manifest.json for a chapter."""
    fields = {'scenes': scene_count, 'video_status': 'generated'}
    if video_16x9:
        fields['video_16x9'] = str(video_16x9.relative_to(PROJECT_ROOT))
    if video_9x16:
        fields['video_9x16'] = str(video_9x16.relative_to(PROJECT_ROOT))
    _update_chapter_fields(chapter_index, paths=paths, **fields)
    print(f"  Audiobook manifest updated for chapter {chapter_index}")


# --- List Command ---

def list_chapters(chapters: list[dict], paths: AudiobookPaths | None = None):
    """Print all chapters with their video generation status."""
    video_dir = paths.video if paths else VIDEO_DIR
    print(f"\nChapter Video Status ({len(chapters)} chapters):")
    print("=" * 90)

    current_part = None
    for ch in chapters:
        if ch['part'] != current_part:
            current_part = ch['part']
            if current_part:
                print(f"\n  [{current_part}]")

        chapter_dir = get_chapter_dir(ch, paths=paths)
        scene_manifest = load_scene_manifest(chapter_dir)
        scene_count = len(scene_manifest['scenes']) if scene_manifest else 0

        text_file = find_prepared_text(ch, paths=paths)
        audio_file = find_chapter_audio(ch, paths=paths)
        text_chars = len(text_file.read_text(encoding='utf-8')) if text_file else 0

        has_video = False
        if video_dir.exists():
            for ar in ASPECT_RATIOS:
                pattern = f"{ch['index']:03d}-*-{ar.replace(':', 'x')}.mp4"
                if next(video_dir.glob(pattern), None):
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

def run_pipeline(chapter: dict, keyframes_only: bool = False, force: bool = False, max_scenes: int | None = None, no_keyframes: bool = False, book_meta: dict | None = None, prompt_variant: str = DEFAULT_PROMPT_VARIANT, test_prompts: bool = False, paths: AudiobookPaths | None = None):
    """Run the video generation pipeline for a single chapter.

    Requires pre-existing scene-manifest.json (produced by generate_audiobook_scenes.py)
    and audio file (produced by generate_audiobook.py).
    """
    print(f"\n{'=' * 60}")
    print(f"Chapter {chapter['index']}: {chapter['title']}")
    print(f"  QMD: {chapter['path']}")
    print(f"{'=' * 60}")

    chapter_dir = get_chapter_dir(chapter, paths=paths)

    # Load scene manifest (required)
    existing = load_scene_manifest(chapter_dir)
    if not existing or not existing.get('scenes'):
        raise FileNotFoundError(
            f"No scene-manifest.json for chapter {chapter['index']} ({chapter_dir}). "
            f"Run: python scripts/generate_audiobook_scenes.py --chapter {chapter['index']}"
        )

    scenes = existing['scenes']
    text_hash = existing.get('text_hash', '')
    total_duration_ms = existing.get('total_duration_ms', 0)
    print(f"  Loaded scene manifest: {len(scenes)} scenes")

    # Load audio (required)
    audio_path = find_chapter_audio(chapter, paths=paths)
    if not audio_path:
        raise FileNotFoundError(
            f"No audio for chapter {chapter['index']}. "
            f"Run: python scripts/generate_audiobook.py --chapter {chapter['index']}"
        )

    # Get actual audio duration for assembly
    audio = AudioSegment.from_wav(str(audio_path))
    total_duration_ms = len(audio)
    print(f"  Audio: {total_duration_ms:,}ms ({total_duration_ms / 1000:.1f}s)")

    # Load text for image prompt context
    text_file = find_prepared_text(chapter, paths=paths)
    text = text_file.read_text(encoding='utf-8') if text_file else ""
    if text:
        print(f"  Text: {len(text):,} chars ({text_file.name})")

    if max_scenes and len(scenes) > max_scenes:
        print(f"  --max-scenes {max_scenes}: truncating from {len(scenes)} scenes")
        scenes = scenes[:max_scenes]

    if force:
        subdirs_to_clean = ["clips"]
        if not no_keyframes:
            subdirs_to_clean.insert(0, "keyframes")
        for subdir in subdirs_to_clean:
            old_dir = chapter_dir / subdir
            if old_dir.exists():
                shutil.rmtree(old_dir)
                print(f"  --force: deleted {subdir}/")
        video_dir = paths.video if paths else VIDEO_DIR
        for aspect in ASPECT_RATIOS:
            aspect_tag = aspect.replace(":", "x")
            old_video = video_dir / f"{chapter['index']:03d}-{chapter_slug(chapter)}-{aspect_tag}.mp4"
            if old_video.exists():
                old_video.unlink()
                print(f"  --force: deleted {old_video.name}")

    if test_prompts:
        test_prompt_variants(scenes, chapter_dir, chapter_text=text, max_scenes=max_scenes)
        return

    if not no_keyframes:
        scenes = generate_keyframes(scenes, chapter_dir, chapter=chapter, book_meta=book_meta, chapter_text=text, prompt_variant=prompt_variant)
        save_scene_manifest(scenes, chapter, chapter_dir, total_duration_ms, text_hash)

        if keyframes_only:
            print("\n--keyframes-only: stopping after keyframe generation.")
            return

    scenes = animate_scenes(scenes, chapter_dir, use_keyframes=not no_keyframes, chapter_text=text)
    save_scene_manifest(scenes, chapter, chapter_dir, total_duration_ms, text_hash)

    print("\nAssembling final videos...")
    video_16x9 = assemble_chapter_video(scenes, chapter, chapter_dir, "16:9", book_meta=book_meta, paths=paths)
    video_9x16 = assemble_chapter_video(scenes, chapter, chapter_dir, "9:16", book_meta=book_meta, paths=paths)

    print("\nUpdating manifest...")
    update_audiobook_manifest(chapter['index'], video_16x9, video_9x16, len(scenes), paths=paths)

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
        "--limit", "-n",
        type=int,
        help="Max number of chapters to process"
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
    parser.add_argument(
        "--no-keyframes",
        action="store_true",
        help="Skip keyframe generation; use text-to-video instead of image-to-video"
    )
    parser.add_argument(
        "--prompt",
        choices=list(PROMPT_VARIANTS.keys()),
        default=DEFAULT_PROMPT_VARIANT,
        help=f"Prompt variant for keyframe generation (default: {DEFAULT_PROMPT_VARIANT})"
    )
    parser.add_argument(
        "--test-prompts",
        action="store_true",
        help="Generate one 16:9 keyframe per prompt variant per scene for A/B comparison"
    )
    args = parser.parse_args()

    try:
        config_path = resolve_config_path(args.config)
    except FileNotFoundError as e:
        parser.error(str(e))

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

    print(f"Config: {config_path.name} (output: assets/audiobook/{cfg_name}/)")

    # Load full config for book metadata
    full_config = load_quarto_config(config_path)
    chapters = extract_chapters_from_config(config_path)
    print(f"Found {len(chapters)} chapters")

    if args.list:
        list_chapters(chapters, paths=paths)
        return

    # Extract book metadata for tagging images/videos
    book_meta = extract_book_metadata(full_config)

    # Apply chapter/start/limit filters
    if args.chapter:
        chapters = [ch for ch in chapters if ch['index'] == args.chapter]
    else:
        if args.start:
            chapters = [ch for ch in chapters if ch['index'] >= args.start]
        if args.limit:
            chapters = chapters[:args.limit]
    if args.chapter or args.start or args.limit:
        print(f"Processing {len(chapters)} chapter(s)")

    if not chapters:
        print("No chapters to process.")
        return

    for chapter in chapters:
        run_pipeline(
            chapter=chapter,
            keyframes_only=args.keyframes_only,
            force=args.force,
            max_scenes=args.max_scenes,
            no_keyframes=args.no_keyframes,
            book_meta=book_meta,
            prompt_variant=args.prompt,
            test_prompts=args.test_prompts,
            paths=paths,
        )

    print(f"\n{'=' * 60}")
    print(f"All done! Processed {len(chapters)} chapter(s).")


if __name__ == "__main__":
    main()
