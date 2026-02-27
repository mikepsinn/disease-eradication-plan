"""Shared scene segmentation logic for audiobook pipeline.

Used by generate_audiobook_scenes.py and generate_audiobook_video.py.
Extracted from generate_audiobook_video.py to allow scene segmentation
as a separate pipeline step.
"""
import json
import re
import time
import threading
from pathlib import Path

from lib.llm import generate_gemini_flash_content, GEMINI_FLASH_MODEL_ID


# --- Scene Segmentation Prompt ---

SCENE_SEGMENTATION_PROMPT = """Segment this audiobook narration into visual scenes. Read the ENTIRE text first.

Rules:
- Each scene: ~120-250 characters, breaking at natural narrative boundaries
- char_start/char_end: exact character offsets, no gaps, no overlaps
- narration_text: exact original text for that span
- context: relevant surrounding context from the chapter that explains the scene. Do NOT repeat the narration_text.
- animation_prompt: simple camera/subject motion for animating the keyframe image.

Return ONLY a JSON array:
[{{"scene_index": 1, "title": "Short Title", "narration_text": "exact text...", "context": "...", "animation_prompt": "...", "char_start": 0, "char_end": 120}}]

Text:
---
{text}
---"""

SCENE_SEGMENTATION_WITH_PROMPTS = """Segment this audiobook narration into visual scenes. Read the ENTIRE text first.

Visual style: {visual_style}
No-text rule: {no_text}

Rules:
- Each scene: ~120-250 characters, breaking at natural narrative boundaries
- char_start/char_end: exact character offsets, no gaps, no overlaps
- narration_text: exact original text for that span
- context: relevant surrounding context from the chapter that explains the scene. Do NOT repeat the narration_text.
- keyframe_prompt: A detailed image generation prompt in the visual style above. Describe the scene as a single illustration. Include the no-text rule. Do NOT include "Generate" or "Create".
- veo_prompt: A video animation prompt describing camera motion and subject motion to animate the keyframe. Keep it concise (1-2 sentences). Include "No dialogue, narration, or speech."

Return ONLY a JSON array:
[{{"scene_index": 1, "title": "Short Title", "narration_text": "exact text...", "context": "...", "keyframe_prompt": "...", "veo_prompt": "...", "char_start": 0, "char_end": 120}}]

Text:
---
{text}
---"""


LLM_CALL_TIMEOUT = 120  # seconds


def _call_llm_with_timeout(prompt: str, timeout: int = LLM_CALL_TIMEOUT) -> str:
    """Call Gemini Flash with a hard thread-based timeout."""
    result: list[str | None] = [None]
    error: list[Exception | None] = [None]

    def _call():
        try:
            result[0] = generate_gemini_flash_content(prompt)
        except Exception as e:
            error[0] = e

    t = threading.Thread(target=_call)
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise TimeoutError(f"LLM call hung for {timeout}s")
    if error[0] is not None:
        raise error[0]
    assert result[0] is not None
    return result[0]


def parse_json_array(response_text: str) -> list[dict]:
    """Extract a JSON array from LLM response text.

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


def segment_scenes(text: str) -> list[dict]:
    """Use Gemini Flash to segment narration text into visual scenes."""
    print("  Segmenting text into visual scenes...")
    prompt = SCENE_SEGMENTATION_PROMPT.format(text=text)
    for attempt in range(1, 4):
        try:
            response = _call_llm_with_timeout(prompt)
            break
        except Exception as e:
            if attempt < 3:
                wait = attempt * 15
                print(f"  [RETRY] LLM attempt {attempt}/3 failed: {e}")
                print(f"  [RETRY] Waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                raise
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
        anim = s.get('animation_prompt', '')
        anim_preview = f" | {anim[:60]}..." if len(anim) > 60 else (f" | {anim}" if anim else "")
        print(f"    Scene {s['scene_index']}: {s['title']} ({chars} chars, ~{pct:.0f}%){anim_preview}")

    return scenes


def segment_scenes_with_prompts(text: str, visual_style: str, no_text: str) -> list[dict]:
    """Segment narration text into scenes with keyframe_prompt and veo_prompt.

    Uses an enhanced prompt that instructs the LLM to generate image/video
    prompts alongside the segmentation.
    """
    print("  Segmenting text into visual scenes (with prompts)...")
    prompt = SCENE_SEGMENTATION_WITH_PROMPTS.format(
        text=text, visual_style=visual_style, no_text=no_text,
    )
    for attempt in range(1, 4):
        try:
            response = _call_llm_with_timeout(prompt)
            break
        except Exception as e:
            if attempt < 3:
                wait = attempt * 15
                print(f"  [RETRY] LLM attempt {attempt}/3 failed: {e}")
                print(f"  [RETRY] Waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                raise
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
        kp = s.get('keyframe_prompt', '')
        kp_preview = f" | {kp[:60]}..." if len(kp) > 60 else (f" | {kp}" if kp else "")
        print(f"    Scene {s['scene_index']}: {s['title']} ({chars} chars, ~{pct:.0f}%){kp_preview}")

    return scenes


# --- Individual Scene JSON Files ---

def save_scene_files(
    scenes: list[dict],
    chapter_dir: Path,
    force: bool = False,
    overwrite_edits: bool = False,
) -> list[dict]:
    """Save each scene as an individual JSON file (scene-NN.json).

    Preserves manual edits: if user has edited keyframe_prompt or veo_prompt
    (i.e. they differ from _auto_generated), the user's version is kept unless
    overwrite_edits=True.

    Returns the scenes list (possibly with restored manual edits).
    """
    scenes_dir = chapter_dir / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)

    for scene in scenes:
        idx = scene['scene_index']
        scene_path = scenes_dir / f"scene-{idx:02d}.json"

        # Store auto-generated prompts
        auto_gen = {
            'keyframe_prompt': scene.get('keyframe_prompt', ''),
            'veo_prompt': scene.get('veo_prompt', ''),
        }

        if scene_path.exists() and not overwrite_edits:
            existing = json.loads(scene_path.read_text(encoding='utf-8'))
            existing_auto = existing.get('_auto_generated', {})

            # Check if user manually edited prompts
            for field in ('keyframe_prompt', 'veo_prompt'):
                existing_val = existing.get(field, '')
                auto_val = existing_auto.get(field, '')
                if existing_val and auto_val and existing_val != auto_val:
                    # User has manually edited this field; preserve their edit
                    if not force or not overwrite_edits:
                        print(f"    Scene {idx}: preserving manual edit of {field}")
                        scene[field] = existing_val

        scene['_auto_generated'] = auto_gen

        scene_path.write_text(
            json.dumps(scene, indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8',
        )

    print(f"  Saved {len(scenes)} scene files to {scenes_dir}")
    return scenes


def load_scene_files(chapter_dir: Path) -> list[dict] | None:
    """Load individual scene JSON files from chapter_dir/scenes/.

    Returns sorted list of scenes, or None if no scene files exist.
    """
    scenes_dir = chapter_dir / "scenes"
    if not scenes_dir.exists():
        return None

    scene_files = sorted(scenes_dir.glob("scene-*.json"))
    if not scene_files:
        return None

    scenes = []
    for sf in scene_files:
        # Skip non-numbered files (e.g. scene-manifest.json)
        if not re.match(r'scene-\d+\.json$', sf.name):
            continue
        scene = json.loads(sf.read_text(encoding='utf-8'))
        scenes.append(scene)

    scenes.sort(key=lambda s: s.get('scene_index', 0))
    return scenes if scenes else None


def scene_has_manual_edits(scene: dict) -> bool:
    """Check if a scene's prompts have been manually edited."""
    auto = scene.get('_auto_generated', {})
    if not auto:
        return False
    for field in ('keyframe_prompt', 'veo_prompt'):
        if scene.get(field, '') != auto.get(field, '') and auto.get(field, ''):
            return True
    return False


def estimate_timestamps(scenes: list[dict], total_chars: int, total_duration_ms: int) -> list[dict]:
    """Map char offsets to audio timestamps using linear interpolation.

    Ensures the last scene extends to exactly total_duration_ms so the
    assembled video fully covers the audio track.
    """
    print("  Estimating audio timestamps (linear interpolation)...")
    for scene in scenes:
        scene['start_ms'] = int((scene['char_start'] / total_chars) * total_duration_ms)
        scene['end_ms'] = int((scene['char_end'] / total_chars) * total_duration_ms)
        scene['duration_ms'] = scene['end_ms'] - scene['start_ms']
        print(f"    Scene {scene['scene_index']}: {scene['start_ms']}ms - {scene['end_ms']}ms ({scene['duration_ms']}ms)")

    # Force last scene to extend to full audio duration to prevent cutoff
    if scenes:
        last = scenes[-1]
        if last['end_ms'] < total_duration_ms:
            gap = total_duration_ms - last['end_ms']
            last['end_ms'] = total_duration_ms
            last['duration_ms'] = last['end_ms'] - last['start_ms']
            print(f"    [FIX] Extended last scene by {gap}ms to cover full audio ({total_duration_ms}ms)")

    return scenes


def assign_timestamps_from_alignment(
    scenes: list[dict],
    alignment_words: list[dict],
    total_duration_ms: int,
) -> list[dict]:
    """Assign precise timestamps to scenes using word-level alignment data.

    Falls back to linear interpolation for scenes where alignment lookup fails.
    """
    from lib.alignment import timestamps_for_char_range

    print("  Assigning timestamps from alignment data...")
    for scene in scenes:
        start_ms, end_ms = timestamps_for_char_range(
            alignment_words, scene['char_start'], scene['char_end']
        )
        if start_ms > 0 or end_ms > 0:
            scene['start_ms'] = start_ms
            scene['end_ms'] = end_ms
            scene['duration_ms'] = end_ms - start_ms
            scene['timestamp_source'] = 'alignment'
        else:
            # Fallback to linear interpolation for this scene
            total_chars = max(s.get('char_end', 0) for s in scenes) if scenes else 1
            scene['start_ms'] = int((scene['char_start'] / total_chars) * total_duration_ms)
            scene['end_ms'] = int((scene['char_end'] / total_chars) * total_duration_ms)
            scene['duration_ms'] = scene['end_ms'] - scene['start_ms']
            scene['timestamp_source'] = 'interpolation'
        print(f"    Scene {scene['scene_index']}: {scene['start_ms']}ms - {scene['end_ms']}ms ({scene['duration_ms']}ms) [{scene.get('timestamp_source', '?')}]")

    # Force last scene to extend to full audio duration
    if scenes:
        last = scenes[-1]
        if last['end_ms'] < total_duration_ms:
            gap = total_duration_ms - last['end_ms']
            last['end_ms'] = total_duration_ms
            last['duration_ms'] = last['end_ms'] - last['start_ms']
            print(f"    [FIX] Extended last scene by {gap}ms to cover full audio ({total_duration_ms}ms)")

    return scenes


def save_scene_manifest(
    scenes: list[dict],
    chapter: dict,
    chapter_dir: Path,
    total_duration_ms: int,
    text_hash: str = "",
):
    """Save scene-manifest.json with all scene metadata."""
    manifest = {
        "chapter_index": chapter['index'],
        "chapter_title": chapter['title'],
        "total_chars": 0,
        "total_duration_ms": total_duration_ms,
        "model_used": GEMINI_FLASH_MODEL_ID,
        "text_hash": text_hash,
        "scenes": scenes,
    }
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
