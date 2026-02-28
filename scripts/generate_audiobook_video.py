#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Video Generator

Generates animated video for audiobook chapters using:
1. Pre-existing scene JSON files (from generate_audiobook_scenes.py)
2. Keyframe image generation (Imagen)
3. Video animation (Veo 3.1)
4. Assembly with ffmpeg

Requires scene files and audio to exist already. Run the earlier pipeline
steps first: generate_audiobook_text.py -> generate_audiobook.py -> generate_audiobook_scenes.py

Output structure (flat, slug-prefixed):
    video/scenes/{slug}.json
    video/keyframes/{slug}-scene-01-16x9.jpg
    video/clips/{slug}-scene-01-16x9.mp4
    video/{slug}-16x9.mp4

Usage:
    python scripts/generate_audiobook_video.py --chapter 20 --keyframes-only
    python scripts/generate_audiobook_video.py --chapter 20
    python scripts/generate_audiobook_video.py --chapter 20 --scene 3 --skip-keyframes --force
    python scripts/generate_audiobook_video.py --chapter 20 --skip-keyframes --skip-animate
    python scripts/generate_audiobook_video.py --list
"""
import io
import sys
import re
import hashlib
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if sys.platform == 'win32' and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

from pydub import AudioSegment

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.llm import generate_gemini_flash_content_with_image, generate_gemini_flash_content
from lib.image_gen import generate_image, rate_limited_generate_image
from lib.veo import generate_video
from dih_models.yaml_utils import load_quarto_config
from generate_audiobook import extract_book_metadata
from lib.audiobook_common import (
    PROJECT_ROOT, VIDEO_DIR, SCENES_DIR, IMAGE_STYLE, text_hash,
    extract_chapters as _extract_chapters,
    extract_title_from_qmd, safe_filename, chapter_slug,
    find_prepared_text, find_chapter_audio,
    resolve_chapter_titles,
    AudiobookPaths, config_name_from_path, get_paths,
    resolve_config_path, get_available_configs,
)
from lib.audiobook_manifest import update_chapter_fields as _update_chapter_fields
from lib.scenes import (
    save_scene_manifest, load_scene_manifest,
    load_scene_files, scene_has_manual_edits,
)
from lib.scene_config import (
    load_scene_config, get_visual_style, get_no_text_instruction,
    get_veo_negative_prompt, get_aspect_ratios, get_veo_parallel_workers,
)

# --- Configuration ---
DEFAULT_CONFIG_NAME = "manual-paperback"

# Visual style - set from scenes-config.json at runtime, falls back to IMAGE_STYLE
_visual_style = IMAGE_STYLE

# --- Prompt Variants ---

NO_TEXT_INSTRUCTION = "Do not include any text, words, letters, or numbers in the image."

_SAFETY_REPHRASE_PROMPT = """The following text was rejected by an AI image generator's safety filter.
Rephrase it to convey the same visual concept without words that could trigger content filters.
Replace references to violence, weapons, military, controversial organizations, death, etc.
with neutral synonyms that preserve the visual meaning.

Return ONLY the rephrased text, nothing else.

Original text:
{text}"""


def _rephrase_for_safety(text: str) -> str:
    """Use Gemini Flash to rephrase text that triggered the image safety filter."""
    result = generate_gemini_flash_content(_SAFETY_REPHRASE_PROMPT.format(text=text))
    return result.strip() if result else text


def _prompt_original(scene_text, full_context, attempt):
    """Style + raw narration + full chapter context."""
    prompt = (
        f"{NO_TEXT_INSTRUCTION}\n"
        f"Generate a {_visual_style} illustration.\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---\n"
        )
    prompt += NO_TEXT_INSTRUCTION
    return prompt

def _prompt_metaphor(scene_text, full_context, attempt):
    """Original + metaphor instruction."""
    prompt = (
        f"{NO_TEXT_INSTRUCTION}\n"
        f"Generate a {_visual_style} illustration. Interpret metaphors visually; do not depict them literally.\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---\n"
        )
    prompt += NO_TEXT_INSTRUCTION
    return prompt

def _prompt_powerpoint(scene_text, full_context, attempt):
    """Two-step: conceptualize as presentation slide, then render in style."""
    prompt = (
        f"{NO_TEXT_INSTRUCTION}\n"
        f"Imagine how this concept would be depicted on a presentation slide given the full chapter context below. "
        f"Then generate that image in {_visual_style} style.\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---\n"
        )
    prompt += NO_TEXT_INSTRUCTION
    return prompt

def _prompt_bookcover(scene_text, full_context, attempt):
    """Direct scene illustration."""
    prompt = (
        f"{NO_TEXT_INSTRUCTION}\n"
        f"Generate a {_visual_style} illustration that captures this moment in the story.\n"
        f"--- ILLUSTRATE THIS ---\n"
        f"{scene_text}\n"
        f"--- END ILLUSTRATE ---\n"
    )
    if full_context:
        prompt += (
            f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n"
            f"{full_context}\n"
            f"--- END CONTEXT ---\n"
        )
    prompt += NO_TEXT_INSTRUCTION
    return prompt

PROMPT_VARIANTS = {
    "original": _prompt_original,
    "metaphor": _prompt_metaphor,
    "powerpoint": _prompt_powerpoint,
    "bookcover": _prompt_bookcover,
}
DEFAULT_PROMPT_VARIANT = "original"

# Suppress Veo-generated speech so we can overlay our own TTS narration.
VEO_NEGATIVE_PROMPT = "narration, dialogue, voice, speech, talking, spoken words"
VEO_AMBIENT_VOLUME = 0.15
VEO_PARALLEL_WORKERS = 8


# --- Filename helpers ---

def _keyframe_filename(slug: str, scene_index: int, aspect: str) -> str:
    aspect_tag = aspect.replace(":", "x")
    return f"{slug}-scene-{scene_index:02d}-{aspect_tag}.jpg"


def _clip_filename(slug: str, scene_index: int, aspect: str) -> str:
    aspect_tag = aspect.replace(":", "x")
    return f"{slug}-scene-{scene_index:02d}-{aspect_tag}.mp4"


# --- Quarto Config Parsing ---

def extract_chapters_from_config(config_path: Path) -> list[dict]:
    """Extract ordered chapter list from a Quarto book YAML config."""
    config = load_quarto_config(config_path)
    chapters = _extract_chapters(config)
    return resolve_chapter_titles(chapters)


def _narration_hash(scene: dict) -> str:
    """Compute a short hash of a scene's narration text for cache invalidation."""
    text = scene.get('narration_text')
    if not text:
        raise ValueError(
            f"Scene {scene.get('scene_index', '?')} has no narration_text. "
            f"Re-run scene segmentation to fix."
        )
    return text_hash(text)


# --- Image/Video Metadata ---

def _tag_image_metadata(image_path: Path, chapter: dict, scene: dict, book_meta: dict | None):
    """Embed EXIF/IPTC metadata into a JPEG keyframe image."""
    if not book_meta or not image_path.exists():
        return
    try:
        from PIL import Image as PILImage
        img = PILImage.open(image_path)
        exif = img.getexif()
        exif[270] = f"Chapter {chapter['index']}: {chapter['title']} - Scene {scene['scene_index']}: {scene.get('title', '')}"
        exif[315] = book_meta['author']
        exif[305] = f"Imagen 4.0 / {book_meta['title']}"
        img.save(image_path, exif=exif.tobytes())
    except Exception:
        pass


# --- Step C: Keyframe Generation ---

IMAGEN_PARALLEL_WORKERS = 4
MAX_KEYFRAME_ATTEMPTS = 3

KEYFRAME_TEXT_CHECK_PROMPT = """Check this generated image for two problems:

1. PROMPT BLEED: The image contains text leaked from the generation prompt, such as "ILLUSTRATE THIS", "CONTEXT ONLY", "END ILLUSTRATE", "END CONTEXT", "Generate a", or any instruction-like text that clearly came from a prompt rather than being part of the illustration.

2. TYPOS: Large, prominent text that is clearly a misspelling of a real English word (e.g. "SCIENEC" instead of "SCIENCE"). Ignore small, decorative, atmospheric, or garbled text on screens/signs/labels.

Valid proper nouns (not typos): Wishonia, Moronia, Gollum, Gollums, Wishocracy, DALY, DALYs.

Answer ONLY one of:
- "CLEAN" if no problems found
- "PROMPT_BLEED: <description>" if prompt text leaked into the image
- "TYPO: <description>" if there is a prominent misspelling"""


def _check_keyframe_for_typos(image_path: Path) -> str | None:
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


def _tts_to_visual(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'\bone percent\b', '1%', text, flags=re.IGNORECASE)
    return text


def generate_keyframes(
    scenes: list[dict],
    video_dir: Path,
    slug: str,
    chapter: dict | None = None,
    book_meta: dict | None = None,
    chapter_text: str = "",
    prompt_variant: str = DEFAULT_PROMPT_VARIANT,
    aspect_ratios: list[str] | None = None,
) -> list[dict]:
    """Generate keyframe images for each scene using Imagen (parallel), with inline typo checking."""
    if aspect_ratios is None:
        aspect_ratios = ["16:9", "9:16"]

    print("Step C: Generating keyframe images (with typo checking)...")
    keyframes_dir = video_dir / "keyframes"
    keyframes_dir.mkdir(parents=True, exist_ok=True)

    for scene in scenes:
        scene['keyframes'] = {}

    work_items = []
    for scene in scenes:
        nh = _narration_hash(scene)
        old_hash = scene.get('keyframe_hash', '')
        stale = old_hash and old_hash != nh

        for aspect in aspect_ratios:
            filename = _keyframe_filename(slug, scene['scene_index'], aspect)
            output_path = keyframes_dir / filename

            if output_path.exists() and not stale:
                print(f"    [CACHED] {filename}")
                scene['keyframes'][aspect] = str(output_path.relative_to(video_dir))
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
            prompt += "\n\nAny text in the image must be spelled correctly. Do NOT include any text from the prompt instructions."
        elif attempt >= 3:
            prompt += "\n\nDo NOT include any text, signs, labels, writing, or words of any kind in this image."
        return prompt

    def _is_safety_block(err: Exception) -> bool:
        msg = str(err)
        return 'block_reason' in msg or 'IMAGE_SAFETY' in msg

    def _generate_and_check(item):
        scene, aspect, output_path, filename = item
        label = filename.replace('.jpg', '')
        last_issue = None

        for attempt in range(1, MAX_KEYFRAME_ATTEMPTS + 1):
            prompt = _build_prompt(scene, attempt=attempt)
            if attempt == 1 and 'imagen_prompt' not in scene:
                scene['imagen_prompt'] = prompt

            try:
                rate_limited_generate_image(prompt=prompt, output_path=output_path, aspect_ratio=aspect)
            except RuntimeError as e:
                if _is_safety_block(e):
                    # Rephrase the narration via LLM to avoid safety triggers
                    print(f"    [SAFETY] {label} (attempt {attempt}): blocked, rephrasing via LLM")
                    rephrased_text = _rephrase_for_safety(scene['narration_text'].strip())
                    rephrased_prompt = (
                        f"{NO_TEXT_INSTRUCTION}\n"
                        f"Generate a {_visual_style} illustration.\n"
                        f"--- ILLUSTRATE THIS ---\n{rephrased_text}\n--- END ILLUSTRATE ---\n"
                        f"{NO_TEXT_INSTRUCTION}"
                    )
                    try:
                        rate_limited_generate_image(prompt=rephrased_prompt, output_path=output_path, aspect_ratio=aspect)
                    except RuntimeError as e2:
                        if _is_safety_block(e2):
                            # Last resort: use only the scene title
                            title = scene.get('title', 'a conceptual scene')
                            fallback_prompt = (
                                f"{NO_TEXT_INSTRUCTION}\n"
                                f"Generate a {_visual_style} illustration of: {title}\n"
                                f"{NO_TEXT_INSTRUCTION}"
                            )
                            print(f"    [SAFETY] {label}: rephrased prompt also blocked, using title-only fallback")
                            rate_limited_generate_image(prompt=fallback_prompt, output_path=output_path, aspect_ratio=aspect)
                        else:
                            raise
                else:
                    raise

            issue = _check_keyframe_for_typos(output_path)
            if issue is None:
                if attempt > 1:
                    print(f"    [FIXED] {label} (attempt {attempt})")
                if chapter and book_meta:
                    _tag_image_metadata(output_path, chapter, scene, book_meta)
                return scene['scene_index'], aspect, str(output_path.relative_to(video_dir))

            is_bleed = issue.upper().startswith("PROMPT_BLEED")
            tag = "PROMPT_BLEED" if is_bleed else "TYPO"
            print(f"    [{tag}] {label} (attempt {attempt}/{MAX_KEYFRAME_ATTEMPTS}): {issue}")
            last_issue = issue
            if attempt < MAX_KEYFRAME_ATTEMPTS:
                output_path.unlink(missing_ok=True)

        print(f"    [WARN] {label}: accepting image after {MAX_KEYFRAME_ATTEMPTS} attempts ({last_issue})")
        if chapter and book_meta:
            _tag_image_metadata(output_path, chapter, scene, book_meta)
        return scene['scene_index'], aspect, str(output_path.relative_to(video_dir))

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
                        s['keyframe_hash'] = _narration_hash(s)
                        break
            except Exception as e:
                errors.append(str(e))
                print(f"    [ERROR] {e}")

    if errors:
        raise RuntimeError(f"Failed to generate {len(errors)} keyframe(s):\n" + "\n".join(errors))

    return scenes


# --- Prompt A/B Testing ---

def test_prompt_variants(scenes: list[dict], video_dir: Path, slug: str, chapter_text: str = "", variants: list[str] | None = None, max_scenes: int | None = None):
    variants = variants or list(PROMPT_VARIANTS.keys())
    test_scenes = scenes[:max_scenes] if max_scenes else scenes
    test_dir = video_dir / "prompt-tests" / slug

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

def animate_scenes(
    scenes: list[dict],
    video_dir: Path,
    slug: str,
    use_keyframes: bool = True,
    chapter_text: str = "",
    veo_negative_prompt: str = VEO_NEGATIVE_PROMPT,
    veo_parallel_workers: int = VEO_PARALLEL_WORKERS,
    aspect_ratios: list[str] | None = None,
) -> list[dict]:
    if aspect_ratios is None:
        aspect_ratios = ["16:9", "9:16"]

    mode = "image-to-video" if use_keyframes else "text-to-video"
    print(f"Step D: Generating video clips with Veo 3.1 ({mode})...")
    clips_dir = video_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    keyframes_dir = video_dir / "keyframes"

    for scene in scenes:
        scene['clips'] = {}

    work_items = []
    for scene in scenes:
        nh = _narration_hash(scene)
        old_hash = scene.get('clip_hash', '')
        stale = old_hash and old_hash != nh

        for aspect in aspect_ratios:
            filename = _clip_filename(slug, scene['scene_index'], aspect)
            clip_path = clips_dir / filename

            if clip_path.exists() and not stale:
                print(f"    [CACHED] {filename}")
                scene['clips'][aspect] = str(clip_path.relative_to(video_dir))
                continue

            if clip_path.exists() and stale:
                print(f"    [STALE] {filename} narration changed ({old_hash} -> {nh})")
                clip_path.unlink()

            keyframe_path = None
            if use_keyframes:
                kf_name = _keyframe_filename(slug, scene['scene_index'], aspect)
                keyframe_path = keyframes_dir / kf_name
                if not keyframe_path.exists():
                    raise FileNotFoundError(f"Missing keyframe: {keyframe_path}")

            work_items.append((scene, aspect, keyframe_path, clip_path, filename))

    if not work_items:
        print("    All clips cached.")
        return scenes

    print(f"    Generating {len(work_items)} clips ({veo_parallel_workers} parallel workers)...")

    def _generate_one(item):
        scene, aspect, keyframe_path, clip_path, filename = item

        scene_text = _tts_to_visual(scene['narration_text'].strip())
        # Truncate context for Veo (max ~2000 chars to stay within prompt limits)
        full_context = _tts_to_visual(chapter_text)[:2000] if chapter_text else ""
        veo_prompt = f"{NO_TEXT_INSTRUCTION}\nGenerate a {_visual_style} animation.\n--- ILLUSTRATE THIS ---\n{scene_text}\n--- END ILLUSTRATE ---\n"
        if full_context:
            veo_prompt += f"--- CONTEXT ONLY (for background understanding, do not illustrate directly) ---\n{full_context}\n--- END CONTEXT ---\n"
        veo_prompt += f"No dialogue, narration, or speech. {NO_TEXT_INSTRUCTION}"

        if 'veo_prompt_used' not in scene:
            scene['veo_prompt_used'] = veo_prompt
        generate_video(
            prompt=veo_prompt,
            output_path=clip_path,
            first_frame_path=keyframe_path,
            aspect_ratio=aspect,
            duration_seconds=8,
            negative_prompt=veo_negative_prompt,
        )
        return scene['scene_index'], aspect, str(clip_path.relative_to(video_dir))

    errors = []
    with ThreadPoolExecutor(max_workers=veo_parallel_workers) as executor:
        futures = {executor.submit(_generate_one, item): item for item in work_items}
        for future in as_completed(futures):
            item = futures[future]
            scene_idx, aspect = item[0]['scene_index'], item[1]
            try:
                _, _, clip_rel = future.result()
                for s in scenes:
                    if s['scene_index'] == scene_idx:
                        s['clips'][aspect] = clip_rel
                        s['clip_hash'] = _narration_hash(s)
                        break
            except Exception as e:
                errors.append(f"Clip scene {scene_idx} ({aspect}): {e}")
                print(f"    [ERROR] Scene {scene_idx} ({aspect}): {e}")

    if errors:
        raise RuntimeError(f"Failed to generate {len(errors)} clip(s):\n" + "\n".join(errors))

    return scenes


# --- Step E: Assembly ---

MAX_SLOWDOWN = 1.3  # Stretch up to this factor is labeled "stretch"; beyond is still stretch but slower
VEO_CLIP_DURATION_S = 8.0  # Veo clips are always ~8s


def _cleanup_temp_dir(temp_dir: Path) -> None:
    """Remove temp assembly directory, tolerating Windows file locks."""
    import shutil
    try:
        shutil.rmtree(str(temp_dir), ignore_errors=True)
    except Exception:
        pass


def _prepare_scene_clip(
    scene: dict,
    clip_path: Path,
    keyframe_path: Path | None,
    temp_dir: Path,
    scene_idx: int,
) -> Path:
    """Create a time-correct clip for one scene.

    Two strategies based on scene duration vs 8s Veo clip:
      - Trim: scene < 8s, cut the clip shorter
      - Stretch: scene >= 8s, slow down clip to match duration
    """
    duration_ms = scene.get('duration_ms') or (scene.get('end_ms', 8000) - scene.get('start_ms', 0))
    if duration_ms <= 0:
        duration_ms = 8000
    duration_s = duration_ms / 1000.0
    ratio = duration_s / VEO_CLIP_DURATION_S
    out_path = temp_dir / f"scene-{scene_idx:03d}.mp4"

    if ratio < 1.0:
        # TRIM: scene is shorter than clip
        cmd = [
            "ffmpeg", "-y", "-i", str(clip_path),
            "-t", f"{duration_s:.3f}",
            "-vf", "format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-an", str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg trim failed for scene {scene_idx}: {result.stderr[:300]}")

    elif ratio <= MAX_SLOWDOWN:
        # STRETCH: slow down clip slightly (imperceptible)
        setpts = f"PTS*{ratio:.4f}"
        cmd = [
            "ffmpeg", "-y", "-i", str(clip_path),
            "-filter:v", f"setpts={setpts},format=yuv420p",
            "-t", f"{duration_s:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-an", str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg stretch failed for scene {scene_idx}: {result.stderr[:300]}")

    else:
        # STRETCH: slow down clip to fill the full scene duration
        setpts = f"PTS*{ratio:.4f}"
        cmd = [
            "ffmpeg", "-y", "-i", str(clip_path),
            "-filter:v", f"setpts={setpts},format=yuv420p",
            "-t", f"{duration_s:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-an", str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg stretch-fallback failed for scene {scene_idx}: {result.stderr[:300]}")

    return out_path


def assemble_chapter_video(
    scenes: list[dict],
    chapter: dict,
    video_dir: Path,
    slug: str,
    aspect: str,
    book_meta: dict | None = None,
    paths: AudiobookPaths | None = None,
) -> Path:
    """Assemble scene clips + audio into a chapter-level MP4.

    Two-pass sync-correct assembly:
      Pass 1: Prepare per-scene clips matching each scene's duration_ms
      Pass 2: Concat prepared clips + mix audio
    """
    aspect_tag = aspect.replace(":", "x")
    output_path = video_dir / f"{slug}-{aspect_tag}.mp4"

    audio_path = find_chapter_audio(chapter, paths=paths)
    if not audio_path:
        raise FileNotFoundError(f"No audio file for chapter {chapter['index']}. Run audiobook:audio first.")

    audio_duration_ms = len(AudioSegment.from_file(str(audio_path)))

    # Check if we're assembling a subset of scenes (e.g. --max-scenes)
    last_scene_end_ms = scenes[-1].get('end_ms', audio_duration_ms) if scenes else audio_duration_ms
    is_partial = last_scene_end_ms < audio_duration_ms * 0.9

    if is_partial:
        audio_duration_ms = last_scene_end_ms
        print(f"  [PARTIAL] Trimming audio to {audio_duration_ms/1000:.1f}s (covers scenes 1-{scenes[-1]['scene_index']})")

    # Validate clip availability
    for scene in scenes:
        clip_rel = scene.get('clips', {}).get(aspect)
        if not clip_rel:
            raise FileNotFoundError(f"No clip for scene {scene['scene_index']} ({aspect})")
        clip_path = video_dir / clip_rel
        if not clip_path.exists():
            raise FileNotFoundError(f"Clip file missing: {clip_path}")

    keyframes_dir = video_dir / "keyframes"
    temp_dir = video_dir / f"_temp-assembly-{slug}-{aspect_tag}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    # --- Pass 1: Prepare time-correct clips ---
    total_video_ms = 0
    prepared = []
    stats = {"trim": 0, "stretch": 0}

    for scene in scenes:
        idx = scene['scene_index']
        dur_ms = scene.get('duration_ms') or (scene.get('end_ms', 8000) - scene.get('start_ms', 0))
        if dur_ms <= 0:
            dur_ms = 8000
        ratio = dur_ms / (VEO_CLIP_DURATION_S * 1000)

        clip_rel = scene['clips'][aspect]
        clip_path = video_dir / clip_rel
        kf_path = keyframes_dir / _keyframe_filename(slug, idx, aspect)

        tier = "trim" if ratio < 1.0 else "stretch"
        stats[tier] += 1

        prepared_path = _prepare_scene_clip(scene, clip_path, kf_path, temp_dir, idx)
        prepared.append(prepared_path)
        total_video_ms += dur_ms
        print(f"    Scene {idx}: {dur_ms}ms -> {tier} (ratio {ratio:.2f})")

    print(f"  Strategy: {stats['trim']} trim, {stats['stretch']} stretch")
    print(f"  Total video: {total_video_ms/1000:.1f}s for {audio_duration_ms/1000:.1f}s audio")

    # --- Pass 2: Concat prepared clips + audio mix ---
    concat_lines = [f"file '{p.as_posix()}'" for p in prepared]
    concat_file = temp_dir / "concat.txt"
    concat_file.write_text('\n'.join(concat_lines), encoding='utf-8')

    audio_duration_s = audio_duration_ms / 1000.0

    # Clips are generated with -an (no audio), so concat has no audio stream.
    # Use TTS narration audio directly as the sole audio track.
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(audio_path),
        "-filter_complex", "[0:v]format=yuv420p[vout]",
        "-map", "[vout]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-profile:v", "high",
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
        _cleanup_temp_dir(temp_dir)
        raise RuntimeError(f"ffmpeg assembly failed: {result.stderr[:500]}")

    _cleanup_temp_dir(temp_dir)

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"  [OK] {output_path.name} ({size_mb:.1f} MB)")
    return output_path


# --- Update Audiobook Manifest ---

def update_audiobook_manifest(chapter_index: int, video_16x9: Path | None, video_9x16: Path | None, scene_count: int, paths: AudiobookPaths | None = None):
    fields = {'scenes': scene_count, 'video_status': 'generated'}
    if video_16x9:
        fields['video_16x9'] = str(video_16x9.relative_to(PROJECT_ROOT))
    if video_9x16:
        fields['video_9x16'] = str(video_9x16.relative_to(PROJECT_ROOT))
    _update_chapter_fields(chapter_index, paths=paths, **fields)
    print(f"  Audiobook manifest updated for chapter {chapter_index}")


# --- List Command ---

def list_chapters(chapters: list[dict], paths: AudiobookPaths | None = None, scene_config: dict | None = None):
    video_dir = paths.video if paths else VIDEO_DIR
    scenes_dir = paths.scenes if paths else SCENES_DIR
    aspect_ratios = get_aspect_ratios(scene_config) if scene_config else ["16:9", "9:16"]

    print(f"\nChapter Video Status ({len(chapters)} chapters):")
    print("=" * 100)

    current_part = None
    for ch in chapters:
        if ch['part'] != current_part:
            current_part = ch['part']
            if current_part:
                print(f"\n  [{current_part}]")

        slug = chapter_slug(ch)
        scene_files = load_scene_files(scenes_dir, slug)
        scene_manifest = load_scene_manifest(scenes_dir, slug)
        scenes = scene_files or (scene_manifest.get('scenes', []) if scene_manifest else [])
        scene_count = len(scenes)

        text_file = find_prepared_text(ch, paths=paths)
        audio_file = find_chapter_audio(ch, paths=paths)
        text_chars = len(text_file.read_text(encoding='utf-8')) if text_file else 0

        has_video = False
        for ar in aspect_ratios:
            aspect_tag = ar.replace(":", "x")
            if (video_dir / f"{slug}-{aspect_tag}.mp4").exists():
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
        print(f"    {ch['index']:3d}. [{status:>10s}] {ch['title']} ({chars_info})")

        # Per-scene detail
        if scenes:
            keyframes_dir = video_dir / "keyframes"
            clips_dir = video_dir / "clips"
            for s in scenes:
                idx = s.get('scene_index', 0)
                title = s.get('title', '')[:40]

                kf_exists = any(
                    (keyframes_dir / _keyframe_filename(slug, idx, ar)).exists()
                    for ar in aspect_ratios
                )
                clip_exists = any(
                    (clips_dir / _clip_filename(slug, idx, ar)).exists()
                    for ar in aspect_ratios
                )

                markers = ""
                if kf_exists:
                    markers += "K"
                if clip_exists:
                    markers += "V"
                markers = f"[{markers:>2s}]" if markers else "[  ]"

                edited = " [edited]" if scene_has_manual_edits(s) else ""
                dur_ms = s.get('duration_ms', 0)
                dur_s = dur_ms / 1000.0 if dur_ms else 0
                print(f"          {idx:2d}. {markers} {title} ({dur_s:.1f}s){edited}")

    print("=" * 100)
    print("  Legend: T=text, A=audio, S#=scenes, V=video | K=keyframe, V=clip, [edited]=manual prompt edits")


# --- Main Pipeline ---

def run_pipeline(
    chapter: dict,
    keyframes_only: bool = False,
    force: bool = False,
    max_scenes: int | None = None,
    no_keyframes: bool = False,
    skip_animate: bool = False,
    scene_index: int | None = None,
    book_meta: dict | None = None,
    prompt_variant: str = DEFAULT_PROMPT_VARIANT,
    test_prompts: bool = False,
    scene_config: dict | None = None,
    paths: AudiobookPaths | None = None,
):
    slug = chapter_slug(chapter)
    video_dir = paths.video if paths else VIDEO_DIR
    scenes_dir = paths.scenes if paths else SCENES_DIR

    print(f"\n{'=' * 60}")
    print(f"Chapter {chapter['index']}: {chapter['title']}")
    print(f"  QMD: {chapter['path']}")
    print(f"{'=' * 60}")

    # Load scene config
    if not scene_config:
        scene_config = load_scene_config(video_dir)
    global _visual_style
    _visual_style = get_visual_style(scene_config)
    aspect_ratios = get_aspect_ratios(scene_config)
    veo_negative_prompt = get_veo_negative_prompt(scene_config)
    veo_workers = get_veo_parallel_workers(scene_config)

    # Load scenes: prefer scene file, fall back to manifest
    scene_files = load_scene_files(scenes_dir, slug)
    if scene_files:
        scenes = scene_files
        print(f"  Loaded {len(scenes)} scenes from {slug}.json")
    else:
        existing = load_scene_manifest(scenes_dir, slug)
        if not existing or not existing.get('scenes'):
            raise FileNotFoundError(
                f"No scene file for chapter {chapter['index']}. "
                f"Run: python scripts/generate_audiobook_scenes.py --chapter {chapter['index']}"
            )
        scenes = existing['scenes']
        print(f"  Loaded scene manifest: {len(scenes)} scenes")

    text_hash_val = ""
    manifest = load_scene_manifest(scenes_dir, slug)
    if manifest:
        text_hash_val = manifest.get('text_hash', '')
    total_duration_ms = manifest.get('total_duration_ms', 0) if manifest else 0

    # Load audio (required)
    audio_path = find_chapter_audio(chapter, paths=paths)
    if not audio_path:
        raise FileNotFoundError(
            f"No audio for chapter {chapter['index']}. "
            f"Run: python scripts/generate_audiobook.py --chapter {chapter['index']}"
        )

    audio = AudioSegment.from_wav(str(audio_path))
    total_duration_ms = len(audio)
    print(f"  Audio: {total_duration_ms:,}ms ({total_duration_ms / 1000:.1f}s)")

    # Load text for image prompt context
    text_file = find_prepared_text(chapter, paths=paths)
    text = text_file.read_text(encoding='utf-8') if text_file else ""
    if text:
        print(f"  Text: {len(text):,} chars ({text_file.name})")

    # Filter to single scene if requested
    if scene_index is not None:
        scenes = [s for s in scenes if s['scene_index'] == scene_index]
        if not scenes:
            print(f"  [ERROR] Scene {scene_index} not found")
            return
        print(f"  Processing scene {scene_index} only")

    if max_scenes and len(scenes) > max_scenes:
        print(f"  --max-scenes {max_scenes}: truncating from {len(scenes)} scenes")
        scenes = scenes[:max_scenes]

    # Force cleanup: delete specific files (slug-prefixed, so safe)
    if force:
        keyframes_dir = video_dir / "keyframes"
        clips_dir = video_dir / "clips"
        delete_keyframes = not no_keyframes and not skip_animate
        delete_clips = True

        if scene_index is not None:
            # Single scene
            for ar in aspect_ratios:
                if delete_keyframes and keyframes_dir.exists():
                    f = keyframes_dir / _keyframe_filename(slug, scene_index, ar)
                    if f.exists():
                        f.unlink()
                        print(f"  --force: deleted {f.name}")
                if delete_clips and clips_dir.exists():
                    f = clips_dir / _clip_filename(slug, scene_index, ar)
                    if f.exists():
                        f.unlink()
                        print(f"  --force: deleted {f.name}")
        else:
            # All scenes for this chapter
            if delete_keyframes and keyframes_dir.exists():
                for f in keyframes_dir.glob(f"{slug}-scene-*"):
                    f.unlink()
                    print(f"  --force: deleted {f.name}")
            if delete_clips and clips_dir.exists():
                for f in clips_dir.glob(f"{slug}-scene-*"):
                    f.unlink()
                    print(f"  --force: deleted {f.name}")
            for ar in aspect_ratios:
                aspect_tag = ar.replace(":", "x")
                old_video = video_dir / f"{slug}-{aspect_tag}.mp4"
                if old_video.exists():
                    old_video.unlink()
                    print(f"  --force: deleted {old_video.name}")

    if test_prompts:
        test_prompt_variants(scenes, video_dir, slug, chapter_text=text, max_scenes=max_scenes)
        return

    if not no_keyframes:
        scenes = generate_keyframes(
            scenes, video_dir, slug, chapter=chapter, book_meta=book_meta,
            chapter_text=text, prompt_variant=prompt_variant,
            aspect_ratios=aspect_ratios,
        )
        save_scene_manifest(scenes, chapter, scenes_dir, slug, total_duration_ms, text_hash_val)

        if keyframes_only:
            print("\n--keyframes-only: stopping after keyframe generation.")
            return

    if not skip_animate:
        scenes = animate_scenes(
            scenes, video_dir, slug, use_keyframes=not no_keyframes,
            chapter_text=text, veo_negative_prompt=veo_negative_prompt,
            veo_parallel_workers=veo_workers, aspect_ratios=aspect_ratios,
        )
        save_scene_manifest(scenes, chapter, scenes_dir, slug, total_duration_ms, text_hash_val)

    # Assembly (skip if processing single scene)
    if scene_index is not None:
        print(f"\nScene {scene_index} processed. Run without --scene to assemble full video.")
        return

    # For assembly, use all scenes unless --max-scenes limits them
    if max_scenes:
        all_scenes = scenes
    else:
        all_scenes = load_scene_files(scenes_dir, slug) or scenes

    # Populate clip paths for assembly
    clips_dir = video_dir / "clips"
    missing_clips = False
    for s in all_scenes:
        if 'clips' not in s:
            s['clips'] = {}
        for ar in aspect_ratios:
            filename = _clip_filename(slug, s['scene_index'], ar)
            clip_path = clips_dir / filename
            if clip_path.exists():
                s['clips'][ar] = str(clip_path.relative_to(video_dir))
            else:
                missing_clips = True

    if missing_clips and skip_animate:
        print("\n[WARN] Some clips missing; cannot assemble. Run without --skip-animate first.")
        return

    print("\nAssembling final videos...")
    video_16x9 = assemble_chapter_video(all_scenes, chapter, video_dir, slug, "16:9", book_meta=book_meta, paths=paths) if "16:9" in aspect_ratios else None
    video_9x16 = assemble_chapter_video(all_scenes, chapter, video_dir, slug, "9:16", book_meta=book_meta, paths=paths) if "9:16" in aspect_ratios else None

    print("\nUpdating manifest...")
    update_audiobook_manifest(chapter['index'], video_16x9, video_9x16, len(all_scenes), paths=paths)

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
        "config", nargs="?", default=DEFAULT_CONFIG_NAME,
        help=f"Config name or YAML file (default: {DEFAULT_CONFIG_NAME}). Available: {', '.join(available)}"
    )
    parser.add_argument("--chapter", "-c", type=int, help="Process only specific chapter number")
    parser.add_argument("--scene", type=int, help="Process only a specific scene number (requires --chapter)")
    parser.add_argument("--start", "-s", type=int, help="Start from this chapter number (inclusive)")
    parser.add_argument("--limit", "-n", type=int, help="Max number of chapters to process")
    parser.add_argument("--keyframes-only", action="store_true", help="Run keyframe generation only, skip Veo animation")
    parser.add_argument("--skip-keyframes", action="store_true", help="Skip keyframe generation (use existing keyframes)")
    parser.add_argument("--skip-animate", action="store_true", help="Skip Veo animation, go straight to assembly from existing clips")
    parser.add_argument("--list", "-l", action="store_true", help="List all chapters with video generation status")
    parser.add_argument("--force", "-f", action="store_true", help="Force regeneration (delete cached files)")
    parser.add_argument("--max-scenes", type=int, help="Limit number of scenes to process (for quick testing)")
    parser.add_argument("--no-keyframes", action="store_true", help="Skip keyframe generation; use text-to-video instead of image-to-video")
    parser.add_argument("--prompt", choices=list(PROMPT_VARIANTS.keys()), default=DEFAULT_PROMPT_VARIANT, help=f"Prompt variant (default: {DEFAULT_PROMPT_VARIANT})")
    parser.add_argument("--test-prompts", action="store_true", help="Generate one 16:9 keyframe per prompt variant per scene for A/B comparison")
    args = parser.parse_args()

    if args.scene and not args.chapter:
        parser.error("--scene requires --chapter")

    try:
        config_path = resolve_config_path(args.config)
    except FileNotFoundError as e:
        parser.error(str(e))

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)
    scene_config = load_scene_config(paths.video)

    print(f"Config: {config_path.name} (output: assets/audiobook/{cfg_name}/)")

    full_config = load_quarto_config(config_path)
    chapters = extract_chapters_from_config(config_path)
    print(f"Found {len(chapters)} chapters")

    if args.list:
        list_chapters(chapters, paths=paths, scene_config=scene_config)
        return

    book_meta = extract_book_metadata(full_config)

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
            no_keyframes=args.no_keyframes or args.skip_keyframes,
            skip_animate=args.skip_animate,
            scene_index=args.scene,
            book_meta=book_meta,
            prompt_variant=args.prompt,
            test_prompts=args.test_prompts,
            scene_config=scene_config,
            paths=paths,
        )

    print(f"\n{'=' * 60}")
    print(f"All done! Processed {len(chapters)} chapter(s).")


if __name__ == "__main__":
    main()
