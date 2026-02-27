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

SCENE_SEGMENTATION_WITH_PROMPTS = """Segment this audiobook narration into visual scenes. Read the ENTIRE text.

Rules:
- Each scene: ~100-150 characters of narration (~8 seconds of speech), breaking at natural narrative boundaries
- You MUST cover the ENTIRE text with no gaps and no overlaps
- char_start/char_end: exact character offsets into the text below
- narration_text: exact original text for that span (copy verbatim)
- context: brief surrounding context that explains the scene
- title: short descriptive title

Return ONLY a JSON array:
[{{"scene_index": 1, "title": "Short Title", "narration_text": "exact text...", "context": "...", "char_start": 0, "char_end": 120}}]

Text ({text_length} chars total, chunk starting at offset {chunk_offset}):
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


CHUNK_SIZE = 4000  # chars per LLM chunk


def _split_text_into_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> list[tuple[int, str]]:
    """Split text into chunks at paragraph boundaries. Returns (offset, chunk_text) pairs."""
    chunks = []
    pos = 0
    while pos < len(text):
        end = min(pos + chunk_size, len(text))
        if end < len(text):
            # Find last paragraph break within the chunk
            newline_pos = text.rfind('\n\n', pos, end)
            if newline_pos > pos + chunk_size // 2:
                end = newline_pos + 2  # include the double newline
            else:
                # Fall back to last single newline
                newline_pos = text.rfind('\n', pos, end)
                if newline_pos > pos + chunk_size // 2:
                    end = newline_pos + 1
        chunks.append((pos, text[pos:end]))
        pos = end
    return chunks


def _segment_chunk(chunk_text: str, chunk_offset: int, total_length: int, chunk_num: int, total_chunks: int) -> list[dict]:
    """Segment a single text chunk into scenes via LLM."""
    prompt = SCENE_SEGMENTATION_WITH_PROMPTS.format(
        text=chunk_text, text_length=total_length, chunk_offset=chunk_offset,
    )
    for attempt in range(1, 4):
        try:
            response = _call_llm_with_timeout(prompt)
            break
        except Exception as e:
            if attempt < 3:
                wait = attempt * 15
                print(f"    [RETRY] Chunk {chunk_num}/{total_chunks} attempt {attempt}/3 failed: {e}")
                time.sleep(wait)
            else:
                raise
    scenes = parse_json_array(response)

    # Fix char offsets: LLM returns offsets relative to chunk, adjust to full text
    for s in scenes:
        s['char_start'] = s.get('char_start', 0) + chunk_offset
        s['char_end'] = s.get('char_end', 0) + chunk_offset

    return scenes


def segment_scenes_with_prompts(text: str, visual_style: str, no_text: str) -> list[dict]:
    """Segment narration text into scenes using chunked LLM calls.

    Splits long text into ~4000 char chunks, segments each separately,
    then merges and re-indexes.
    """
    total_chars = len(text)
    chunks = _split_text_into_chunks(text)
    print(f"  Segmenting text into visual scenes ({len(chunks)} chunk(s), {total_chars:,} chars)...")

    all_scenes = []
    for i, (offset, chunk_text) in enumerate(chunks):
        print(f"    Chunk {i+1}/{len(chunks)}: offset {offset}, {len(chunk_text)} chars...")
        chunk_scenes = _segment_chunk(chunk_text, offset, total_chars, i + 1, len(chunks))
        print(f"      -> {len(chunk_scenes)} scenes")
        all_scenes.extend(chunk_scenes)

    # Sort by char_start and re-index
    all_scenes.sort(key=lambda s: s.get('char_start', 0))
    for i, s in enumerate(all_scenes, 1):
        s['scene_index'] = i

    if all_scenes:
        last_end = all_scenes[-1]['char_end']
        if abs(last_end - total_chars) > 50:
            print(f"  [WARN] Scene coverage ends at {last_end}, text is {total_chars} chars")

    print(f"  Segmented into {len(all_scenes)} scenes total")
    for s in all_scenes:
        chars = len(s.get('narration_text', ''))
        print(f"    Scene {s['scene_index']}: {s['title']} ({chars} chars, {s['char_start']}-{s['char_end']})")

    return all_scenes


# --- Chapter Scene JSON File ---

def scene_file_path(scenes_dir: Path, slug: str) -> Path:
    """Path to the scene JSON file: scenes_dir/{slug}.json"""
    return scenes_dir / f"{slug}.json"


def save_scene_files(
    scenes: list[dict],
    scenes_dir: Path,
    slug: str,
    force: bool = False,
    overwrite_edits: bool = False,
) -> list[dict]:
    """Save all scenes to a single JSON file ({slug}.json).

    Preserves manual edits: if user has edited keyframe_prompt or veo_prompt
    (i.e. they differ from _auto_generated), the user's version is kept unless
    overwrite_edits=True.

    Returns the scenes list (possibly with restored manual edits).
    """
    path = scene_file_path(scenes_dir, slug)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing scenes for edit preservation
    existing_by_idx: dict[int, dict] = {}
    if path.exists() and not overwrite_edits:
        existing_scenes = json.loads(path.read_text(encoding='utf-8'))
        for es in existing_scenes:
            existing_by_idx[es.get('scene_index', 0)] = es

    for scene in scenes:
        idx = scene['scene_index']

        # Store auto-generated prompts
        auto_gen = {
            'keyframe_prompt': scene.get('keyframe_prompt', ''),
            'veo_prompt': scene.get('veo_prompt', ''),
        }

        existing = existing_by_idx.get(idx)
        if existing and not overwrite_edits:
            existing_auto = existing.get('_auto_generated', {})
            for field in ('keyframe_prompt', 'veo_prompt'):
                existing_val = existing.get(field, '')
                auto_val = existing_auto.get(field, '')
                if existing_val and auto_val and existing_val != auto_val:
                    print(f"    Scene {idx}: preserving manual edit of {field}")
                    scene[field] = existing_val

        scene['_auto_generated'] = auto_gen

    path.write_text(
        json.dumps(scenes, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"  Saved {len(scenes)} scenes to {path.name}")
    return scenes


def load_scene_files(scenes_dir: Path, slug: str) -> list[dict] | None:
    """Load scenes from scenes_dir/{slug}.json.

    Returns sorted list of scenes, or None if no file exists.
    """
    path = scene_file_path(scenes_dir, slug)
    if not path.exists():
        return None

    scenes = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(scenes, list) or not scenes:
        return None

    scenes.sort(key=lambda s: s.get('scene_index', 0))
    return scenes


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
    scenes_dir: Path,
    slug: str,
    total_duration_ms: int,
    text_hash: str = "",
):
    """Save {slug}-manifest.json with all scene metadata."""
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

    scenes_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = scenes_dir / f"{slug}-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f"  Scene manifest saved: {manifest_path}")


def load_scene_manifest(scenes_dir: Path, slug: str) -> dict | None:
    """Load existing {slug}-manifest.json if present."""
    manifest_path = scenes_dir / f"{slug}-manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding='utf-8'))
    # Fallback: legacy path (scenes_dir/slug/scene-manifest.json)
    legacy = scenes_dir / slug / "scene-manifest.json"
    if legacy.exists():
        return json.loads(legacy.read_text(encoding='utf-8'))
    return None
