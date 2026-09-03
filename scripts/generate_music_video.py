#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Music Video Generator for the Podcast Theme Song.

Generates a Broadway-style animated music video for the Wishonia theme song using:
1. Keyframe generation via TS generate-image.ts (Gemini)
2. Video animation via Veo 3.1 with reference images for character consistency
3. Assembly with ffmpeg

The Wishonia avatar is used as a reference image across all scenes to maintain
her retro atomic-age appearance (bob haircut, orange halo, mid-century aesthetic).

Usage:
    python scripts/generate_music_video.py                    # Full pipeline
    python scripts/generate_music_video.py --keyframes-only   # Just generate keyframes
    python scripts/generate_music_video.py --skip-keyframes   # Skip to Veo animation
    python scripts/generate_music_video.py --scene 3          # Process single scene
    python scripts/generate_music_video.py --list             # Show scene breakdown
"""
import io
import sys
import json
import argparse
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))

from google.genai import types
from lib.veo import generate_video
from lib.image_gen import google_client

# --- Paths ---
PROJECT_ROOT = Path(__file__).parent.parent
AVATAR_PATH = PROJECT_ROOT / "assets" / "images" / "wishonia-avatar.png"
AVATAR_FULLBODY_PATH = PROJECT_ROOT / "assets" / "images" / "wishonia" / "wishonia-full-body.png"
SONG_PATH = PROJECT_ROOT / "assets" / "music" / "podcast-theme-song.mp3"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "music-video"
KEYFRAMES_DIR = OUTPUT_DIR / "keyframes"
CLIPS_DIR = OUTPUT_DIR / "clips"
MANIFEST_PATH = OUTPUT_DIR / "music-video-manifest.json"

# --- Style ---
# Matches the Wishonia avatar: retro mid-century, orange/navy palette
NO_TEXT = "Do not include any text, words, titles, labels, signs, banners, or writing of any kind in the image."

VISUAL_STYLE = (
    "Retro 1950s illustration style with mid-century modern geometric patterns. "
    "Color palette: deep navy blue, warm orange, cream white. "
    "Saul Bass poster aesthetic."
)

VEO_NEGATIVE_PROMPT = (
    "narration, dialogue, voice, speech, talking, spoken words, "
    "realistic photography, 3D render, CGI, Pixar, Disney, DreamWorks, "
    "smooth shading, soft gradients, glossy, plastic, ray tracing"
)
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2
VEO_PARALLEL_WORKERS = 4

# --- Character Descriptions ---
WISHONIA_PLANET = (
    "A massive glowing alien planet floating in space, covered in beautiful "
    "utopian cities and glowing circuits, with a giant friendly smiley face on its surface"
)
WISHONIA_CHARACTER = (
    "A cute smiling white-skinned humanoid alien young woman with big cute eyes, "
    "little antennae, a black bob haircut, "
    "wearing a spacey dress with glowing rings orbiting around her"
)

# --- Scene Definitions ---
# Timestamps from Whisper transcription of podcast-theme-song.mp3.
# Each scene has start_s/end_s matching actual lyric timing.
# Veo generates 8s clips; ffmpeg speed-adjusts to match target duration.
SCENES = [
    {
        "index": 1,
        "lyrics": "[Intro] Hello, human! Glad you're here!",
        "start_s": 0.0,
        "end_s": 5.7,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            f"{WISHONIA_PLANET} sending a radio transmission and hearts to a "
            "small Earth in the distance. "
        ),
        "veo_prompt": (
            f"{WISHONIA_PLANET} smiles and waves at tiny Earth. "
            "Glowing hearts float from the planet toward Earth. "
            "The planet pulses brighter with excitement. "
            "1950s sci-fi."
        ),
    },
    {
        "index": 2,
        "lyrics": "Your organs are failing...",
        "start_s": 5.7,
        "end_s": 9.6,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A cartoon young boy and girl. "
            "Behind them, a creeping grim reaper skeleton in a dark hooded robe "
            "creeps up holding a giant scythe."
        ),
        "veo_prompt": (
            "The boy and girl gradually age and deteriorate into skeletons. "
            "The towering grim reaper creeps closer and closer. "
            "1950s illustration style."
        ),
    },
    {
        "index": 3,
        "lyrics": "bribe the right politicians... right time,",
        "start_s": 9.6,
        "end_s": 13.5,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A lineup of cartoon characters in a row: a rich man in a top hat, "
            "a loud woman with a megaphone, a sneaky superpac lobbyist in a trench coat, "
            "and a politician at podium. "
            "Each holds a stack of dollar bills."
        ),
        "veo_prompt": (
            "The characters pass dollar bills down the line like a relay race: "
            "rich man to megaphone guy to lobbyist to Super PAC man to politician. "
            "Each handoff has a sparkle. Assembly line of legal bribery. "
            "1950s style."
        ),
    },
    {
        "index": 4,
        "lyrics": "you can trade the nuclear warheads for medicine -- not even a crime!",
        "start_s": 13.5,
        "end_s": 20.5,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A grumpy nuclear warhead standing next to a magician's top hat. "
            "A magician stands behind the hat. "
            "A policeman stands off to the side watching with arms crossed."
        ),
        "veo_prompt": (
            "The magician shoves the grumpy warhead into the hat. "
            "A happy medicine bottle pops out the other side with sparkles. "
            "The policeman smiles and gives a big thumbs up. "
            "Slapstick magic trick. 1950s style."
        ),
    },
    {
        "index": 5,
        "lyrics": "[break] One dollar on clinical trials,",
        "start_s": 20.5,
        "end_s": 26.5,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A comically tiny dollar bill on a massive empty plate. "
            "A sad cartoon scientist in a white lab coat peers at it through a magnifying glass."
        ),
        "veo_prompt": (
            "A rich lobbyist in a top hat comedically steals the tiny dollar bill "
            "off the plate while the sad scientist watches helplessly. "
            "1950s sad comedy."
        ),
    },
    {
        "index": 6,
        "lyrics": "six hundred on making you dead!",
        "start_s": 26.5,
        "end_s": 31.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A small pile of money bags and dollar bills next to anthropomorphic cartoon missiles. "
            "Happy skeletons stand nearby."
        ),
        "veo_prompt": (
            "The pile of money bags grows into an enormous mountain. "
            "Missiles pile up higher and higher. "
            "Happy skeletons dance around giving thumbs up. "
            "Darkly comedic. 1950s animation."
        ),
    },
    {
        "index": 7,
        "lyrics": "Your leaders aren't evil -- they're just doing what the money said!",
        "start_s": 31.0,
        "end_s": 39.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A Giant anthropomorphic dollar bill holds the puppet strings from above controlling a man in "
            "a suit with strings attached to his limbs. The puppet man is sticking a shovel into a pile of money from a government treasury on his left and there's a bomb factory on his right."
        ),
        "veo_prompt": (
            "The anthropromorphic dollar bills pull the marionette strings. The puppet "
            "shovels the money from the government treasury on the left into the bomb factory on the right. "
        ),
    },
    {
        "index": 8,
        "lyrics": "I'm the World Integrated System for High-Efficiency Optimization,",
        "start_s": 39.0,
        "end_s": 47.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            f"{WISHONIA_PLANET}. "
            "Tiny Earth visible in the distance."
        ),
        "veo_prompt": (
            f"{WISHONIA_PLANET} pulses with energy. "
            "The giant smiley face beams. Camera slowly zooms in. 1950s sci-fi."
        ),
    },
    {
        "index": 9,
        "lyrics": "Networked Intelligence, and Allocation. But you can call me Wishonia!",
        "start_s": 47.0,
        "end_s": 55.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            f"{WISHONIA_CHARACTER} at a holographic dashboard "
            "with glowing data visualizations of health and happiness data."
        ),
        "veo_prompt": (
            f"{WISHONIA_CHARACTER} swipes and flicks holographic data "
            "visualizations floating in the air. Health and happiness charts "
            "stream past. She smiles and winks with a sparkle at the end. 1950s sci-fi. Navy background, warm orange glow."
        ),
    },
    {
        "index": 10,
        "lyrics": "Take one percent of the murder budget, slide it to the medicine side!",
        "start_s": 55.0,
        "end_s": 62.5,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} "
            "A giant pie chart. 99% of the pie is dark navy filled with bombs, "
            "skulls, and missiles."
            "Doctors and sick cancer patients staring to pull a tiny 1% orange slice out of the pie chart. "
            'A parchment scroll below reads "1% Treaty". Navy background.'
        ),
        "veo_prompt": (
            "doctors and sick cancer patients pull the tiny 1% orange slice slides out of the giant bomb-and-skull pie chart "
            "The slice transforms into glowing medicine bottles. "
            'A parchment unfurls reading "1% Treaty". '
            "1950s style. Orange and navy."
        ),
    },
    {
        "index": 11,
        "lyrics": "Nobody has to be a better person -- just let the greed decide!",
        "start_s": 62.5,
        "end_s": 71.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A greedy businessman with dollar signs in his eyes standing next to an elaborate "
            "Rube Goldberg machine illustrating the corrupt political system and producing bombs. He holds a wad of money near the input funnel."
        ),
        "veo_prompt": (
            "The businessman shoves money into the Rube Goldberg machine that's initially producing bombs. "
            "It bounces through gears, dominoes, catapults, and tubes in a comedic chain reaction. "
            "Medicine bottles eventually pop out the other end instead of bombs. 1950s animation."
        ),
    },
    {
        "index": 12,
        "lyrics": "How to End War and Disease -- A Step-by-Step Guide",
        "start_s": 71.0,
        "end_s": 79.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} "
            'Illustrate a goofy man reading a book with title '
            '"How to End War and Disease" visible on the cover.  A trash can and a small cockroach are to the side.  '
        ),
        "veo_prompt": (
            "The man reads the book upside down and then throws the book in the trash can. "
            " The man pulls out a cell phone showing a girl dancing. "
            "The man ages and turns into a skeleton while staring at the phone. "
            "A cockroach crawls up, evolves intelligence, "
            "pulls the book out of the trash, and starts reading it. "
            "1950s comedy."
        ),
    },
    {
        "index": 13,
        "lyrics": "to Optimizing Your",
        "start_s": 79.0,
        "end_s": 86.5,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "Sick patients stand in a dystopian war-torn city with lots of bombs lying around looking confused at a path made of dollar bills going off the screen."
        ),
        "veo_prompt": (
            "The patients stumble along the path of money. "
            "Every step accidentally turns the bombs into flowers and medicine "
            "a futuristic utopian paradise city slowly appears before them in the distance as they make their way closer. "
            "Use a 1950s animation style with solid colors only."
        ),
    },
    {
        "index": 14,
        "lyrics": "Terrible Civilization!",
        "start_s": 86.5,
        "end_s": 93.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} {NO_TEXT} "
            "A beautiful utopian paradise city with happy anthropomorphic buildings with smiling faces, "
            "flying cars, tree-lined boulevards, happy people dancing in the streets."
        ),
        "veo_prompt": (
            "Zoom out from the scene to reveal the entire utopian paradise city. "
            "The buildings of the utopian paradise city come alive with smiling faces and start dancing. "
            "Hearts emanate from the buildings toward the happy people below. "
            "Everyone and everything is dancing. Flying cars zoom overhead. "
            "Use a 1950s animation style with solid colors only."
        ),
    },
    {
        "index": 15,
        "lyrics": "[outro / curtain call]",
        "start_s": 93.0,
        "end_s": 100.0,
        "keyframe_prompt": (
            f"{VISUAL_STYLE} "
            "All characters in a line in a utopian city: grumpy warhead, puppet politicians, "
            "dancing skeletons, grim reaper, confused general, happy medicine bottle. "
            f"{WISHONIA_CHARACTER} in the center. "
            'A neon sign reads "How to End War and Disease".'
        ),
        "veo_prompt": (
            "A grumpy warhead, puppet politician, "
            "skeleton, grim reaper, confused military general, happy medicine bottle, "
            f"and {WISHONIA_CHARACTER} march into the scene. "
            "They take a bow together. Confetti cannons explode. "
            'A flickering neon sign appears above reading "How to End War and Disease". '
            "Classic showstopper ending. "
            "Use a 1950s animation style with solid colors only."
        ),
    },
]


def load_manifest() -> dict:
    """Load existing manifest or create empty one."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"scenes": {}, "song": str(SONG_PATH.relative_to(PROJECT_ROOT)), "avatar": str(AVATAR_PATH.relative_to(PROJECT_ROOT))}


def save_manifest(manifest: dict):
    """Save manifest to disk."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_keyframe(scene: dict) -> Path:
    """Generate a keyframe image for a scene using Gemini image generation."""
    KEYFRAMES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg"

    if output_path.exists():
        print(f"  [CACHED] keyframe scene-{scene['index']:02d}.jpg")
        return output_path

    print(f"  Generating keyframe for scene {scene['index']}: {scene['lyrics'][:50]}...")

    prompt = scene["keyframe_prompt"]
    prompt += f"\n\nIMPORTANT: Generate image with aspect ratio 16:9."

    response = google_client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=[{"parts": [{"text": prompt}]}],
        config=types.GenerateContentConfig(
            response_modalities=["image"],
            safety_settings=[
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            ],
        ),
    )

    if not response.candidates or not response.candidates[0].content:
        raise RuntimeError(f"No image generated for scene {scene['index']}")

    for part in response.candidates[0].content.parts or []:
        if part.inline_data and part.inline_data.data:
            import base64
            image_bytes = base64.b64decode(part.inline_data.data) if isinstance(part.inline_data.data, str) else part.inline_data.data
            output_path.write_bytes(image_bytes)
            print(f"  [OK] keyframe scene-{scene['index']:02d}.jpg")
            return output_path

    raise RuntimeError(f"Response contained no image data for scene {scene['index']}")


def generate_keyframes_all(scenes: list[dict]) -> dict[int, Path]:
    """Generate keyframes for all scenes."""
    print("\n=== Step 1: Generating Keyframes ===")
    keyframes = {}
    # First pass: generate all scenes that use Gemini (skip keyframe_from_clip scenes)
    deferred = []
    for scene in scenes:
        if scene.get("keyframe_from_clip"):
            deferred.append(scene)
            continue
        for attempt in range(3):
            try:
                keyframes[scene["index"]] = generate_keyframe(scene)
                break
            except RuntimeError as e:
                if attempt < 2:
                    print(f"  [RETRY] Keyframe scene {scene['index']} attempt {attempt + 1}/3 failed: {e}")
                    time.sleep(5)
                    # Delete partial file if exists
                    kf = KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg"
                    kf.unlink(missing_ok=True)
                else:
                    raise
    # Deferred scenes will have keyframes extracted after their source clip is animated
    for scene in deferred:
        src = scene["keyframe_from_clip"]
        output_path = KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg"
        print(f"  [DEFERRED] Scene {scene['index']} keyframe will be extracted from scene {src} clip after animation")
        keyframes[scene["index"]] = output_path
    return keyframes


def animate_scene(scene: dict, keyframe_path: Path) -> Path:
    """Animate a single scene with Veo 3.1 using reference images."""
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    clip_path = CLIPS_DIR / f"scene-{scene['index']:02d}.mp4"

    if clip_path.exists():
        print(f"  [CACHED] clip scene-{scene['index']:02d}.mp4")
        return clip_path

    print(f"  Animating scene {scene['index']}: {scene['lyrics'][:50]}...")

    generate_video(
        prompt=scene["veo_prompt"],
        output_path=clip_path,
        first_frame_path=keyframe_path,
        reference_image_paths=None,  # Can't combine with first_frame in current API
        aspect_ratio="16:9",
        duration_seconds=8,  # Veo always generates 8s; ffmpeg speed-adjusts later
        negative_prompt=VEO_NEGATIVE_PROMPT,
    )

    return clip_path


def extract_last_frame(clip_path: Path, output_path: Path) -> Path:
    """Extract the last frame from a video clip as a JPEG keyframe."""
    import subprocess
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-sseof", "-0.1", "-i", str(clip_path),
         "-frames:v", "1", "-q:v", "2", "-update", "1", str(output_path)],
        capture_output=True, check=True,
    )
    print(f"  [EXTRACTED] keyframe scene-{output_path.stem.split('-')[1]}.jpg from last frame of {clip_path.name}")
    return output_path


def animate_all(scenes: list[dict], keyframes: dict[int, Path]) -> dict[int, Path]:
    """Animate all scenes with Veo 3.1 (parallel)."""
    print("\n=== Step 2: Animating Scenes with Veo 3.1 ===")
    clips = {}

    # Split into independent scenes and scenes that depend on another clip
    deferred = []
    work_items = []
    for scene in scenes:
        clip_path = CLIPS_DIR / f"scene-{scene['index']:02d}.mp4"
        if clip_path.exists() and not scene.get("keyframe_from_clip"):
            print(f"  [CACHED] clip scene-{scene['index']:02d}.mp4")
            clips[scene["index"]] = clip_path
        elif scene.get("keyframe_from_clip"):
            deferred.append(scene)
        else:
            work_items.append(scene)

    if not work_items and not deferred:
        print("  All clips cached.")
        return clips

    # Animate independent scenes in parallel
    if work_items:
        print(f"  Generating {len(work_items)} clips ({VEO_PARALLEL_WORKERS} parallel workers)...")

        def _gen(scene):
            kf = keyframes[scene["index"]]
            return scene["index"], animate_scene(scene, kf)

        errors = []
        with ThreadPoolExecutor(max_workers=VEO_PARALLEL_WORKERS) as executor:
            futures = {executor.submit(_gen, s): s for s in work_items}
            for future in as_completed(futures):
                scene = futures[future]
                try:
                    idx, clip_path = future.result()
                    clips[idx] = clip_path
                except Exception as e:
                    errors.append(f"Scene {scene['index']}: {e}")
                    print(f"  [ERROR] Scene {scene['index']}: {e}")

        if errors:
            raise RuntimeError(f"Failed to animate {len(errors)} scene(s):\n" + "\n".join(errors))

    # Now handle deferred scenes (keyframe extracted from another scene's clip)
    for scene in deferred:
        src_idx = scene["keyframe_from_clip"]
        src_clip = clips.get(src_idx) or (CLIPS_DIR / f"scene-{src_idx:02d}.mp4")
        if not src_clip.exists():
            raise RuntimeError(f"Scene {scene['index']} needs clip from scene {src_idx}, but it doesn't exist")
        kf_path = KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg"
        extract_last_frame(src_clip, kf_path)
        keyframes[scene["index"]] = kf_path
        clip_path = CLIPS_DIR / f"scene-{scene['index']:02d}.mp4"
        if clip_path.exists():
            print(f"  [CACHED] clip scene-{scene['index']:02d}.mp4")
            clips[scene["index"]] = clip_path
        else:
            clip = animate_scene(scene, kf_path)
            clips[scene["index"]] = clip

    return clips


def _scene_duration(scene: dict) -> float:
    """Get the target duration in seconds for a scene."""
    return scene["end_s"] - scene["start_s"]


def assemble_video(scenes: list[dict], clips: dict[int, Path]) -> Path:
    """Assemble all clips + song audio into the final music video.

    Each Veo clip is 8s. We speed-adjust each to match the scene's actual
    duration (from Whisper timestamps), then concat and overlay the song audio.
    """
    print("\n=== Step 3: Assembling Final Video ===")

    output_path = OUTPUT_DIR / "wishonia-theme-song-music-video.mp4"
    adjusted_dir = CLIPS_DIR / "_adjusted"
    adjusted_dir.mkdir(parents=True, exist_ok=True)

    # Get song duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(SONG_PATH),
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    song_duration = float(probe_result.stdout.strip()) if probe_result.returncode == 0 else 100.0
    print(f"  Song duration: {song_duration:.1f}s")

    # Speed-adjust each clip to match its scene duration
    concat_lines = []
    temp_clips = []
    for scene in sorted(scenes, key=lambda s: s["index"]):
        clip_path = clips[scene["index"]]
        target_s = _scene_duration(scene)
        adjusted_path = adjusted_dir / f"scene-{scene['index']:02d}.mp4"

        # Get actual clip duration
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(clip_path)],
            capture_output=True, text=True,
        )
        clip_s = float(probe.stdout.strip()) if probe.returncode == 0 else 8.0

        time_scale = target_s / clip_s
        speed_factor = 1.0 / time_scale

        if abs(time_scale - 1.0) < 0.05:
            # Close enough, just trim
            print(f"    Scene {scene['index']:2d}: {clip_s:.1f}s -> {target_s:.1f}s (no change)")
            cmd = [
                "ffmpeg", "-y", "-i", str(clip_path),
                "-t", f"{target_s:.3f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-an",  # strip Veo audio
                "-movflags", "+faststart",
                str(adjusted_path),
            ]
        else:
            print(f"    Scene {scene['index']:2d}: {clip_s:.1f}s -> {target_s:.1f}s ({time_scale:.2f}x)")
            cmd = [
                "ffmpeg", "-y", "-i", str(clip_path),
                "-filter:v", f"setpts=PTS*{time_scale:.4f}",
                "-t", f"{target_s:.3f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-an",  # strip Veo audio
                "-movflags", "+faststart",
                str(adjusted_path),
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg adjust failed for scene {scene['index']}: {result.stderr[:300]}")

        temp_clips.append(adjusted_path)
        concat_lines.append(f"file '{adjusted_path.as_posix()}'")

    # Concat adjusted clips
    concat_file = CLIPS_DIR / "_concat.txt"
    concat_file.write_text("\n".join(concat_lines), encoding="utf-8")

    # Merge video + song audio
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-i", str(SONG_PATH),
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{song_duration:.3f}",
        "-movflags", "+faststart",
        "-metadata", "title=How to End War and Disease - Theme Song",
        "-metadata", "artist=Wishonia",
        "-metadata", "genre=Musical",
        str(output_path),
    ]

    print(f"  Running ffmpeg assembly...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Cleanup temp files
    concat_file.unlink(missing_ok=True)
    for tc in temp_clips:
        tc.unlink(missing_ok=True)
    if adjusted_dir.exists():
        import shutil
        shutil.rmtree(adjusted_dir, ignore_errors=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg assembly failed: {result.stderr[:500]}")

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"  [OK] {output_path.name} ({size_mb:.1f} MB, {song_duration:.0f}s)")
    return output_path


def list_scenes():
    """Print scene breakdown."""
    print(f"\nMusic Video Scene Breakdown ({len(SCENES)} scenes)")
    print("=" * 90)
    total_s = 0.0
    for scene in SCENES:
        dur = _scene_duration(scene)
        kf_exists = (KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg").exists()
        clip_exists = (CLIPS_DIR / f"scene-{scene['index']:02d}.mp4").exists()
        status = ""
        if kf_exists:
            status += "K"
        if clip_exists:
            status += "V"
        status = f"[{status:>2s}]" if status else "[  ]"
        print(f"  {scene['index']:2d}. {status} {scene['start_s']:5.1f}-{scene['end_s']:5.1f}s ({dur:4.1f}s) {scene['lyrics']}")
        total_s += dur
    print("=" * 90)
    print(f"  Total: {total_s:.0f}s ({total_s / 60:.1f}min)  |  Legend: K=keyframe, V=video clip")
    final = OUTPUT_DIR / "wishonia-theme-song-music-video.mp4"
    if final.exists():
        size_mb = final.stat().st_size / 1024 / 1024
        print(f"  Final video: {final.name} ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Generate Wishonia theme song Broadway music video")
    parser.add_argument("--keyframes-only", action="store_true", help="Only generate keyframe images")
    parser.add_argument("--skip-keyframes", action="store_true", help="Skip keyframes, go straight to Veo animation")
    parser.add_argument("--skip-animate", action="store_true", help="Skip Veo, go straight to assembly")
    parser.add_argument("--scene", type=int, help="Process only a specific scene number (1-13)")
    parser.add_argument("--list", "-l", action="store_true", help="List scene breakdown and status")
    parser.add_argument("--force", "-f", action="store_true", help="Force regeneration (delete cached files)")
    args = parser.parse_args()

    print("Wishonia Theme Song Music Video Generator")
    print(f"  Avatar: {AVATAR_PATH}")
    print(f"  Song:   {SONG_PATH}")
    print(f"  Output: {OUTPUT_DIR}")

    if not AVATAR_PATH.exists():
        print(f"ERROR: Avatar not found: {AVATAR_PATH}")
        sys.exit(1)
    if not SONG_PATH.exists():
        print(f"ERROR: Song not found: {SONG_PATH}")
        sys.exit(1)

    if args.list:
        list_scenes()
        return

    scenes = SCENES
    if args.scene:
        scenes = [s for s in SCENES if s["index"] == args.scene]
        if not scenes:
            print(f"ERROR: Scene {args.scene} not found (valid: 1-{len(SCENES)})")
            sys.exit(1)
        # Auto-include dependent scenes (keyframe_from_clip chain)
        if args.force:
            included = {s["index"] for s in scenes}
            changed = True
            while changed:
                changed = False
                for s in SCENES:
                    if s["index"] not in included and s.get("keyframe_from_clip") in included:
                        scenes.append(s)
                        included.add(s["index"])
                        changed = True
            scenes.sort(key=lambda s: s["index"])
        if len(scenes) == 1:
            print(f"  Processing scene {args.scene} only")
        else:
            print(f"  Processing scenes {', '.join(str(s['index']) for s in scenes)} (including dependents)")

    if args.force:
        for scene in scenes:
            kf = KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg"
            clip = CLIPS_DIR / f"scene-{scene['index']:02d}.mp4"
            if not args.skip_keyframes and kf.exists():
                kf.unlink()
                print(f"  --force: deleted keyframe scene-{scene['index']:02d}")
            if not args.skip_animate and clip.exists():
                clip.unlink()
                print(f"  --force: deleted clip scene-{scene['index']:02d}")

    # Step 1: Keyframes
    if not args.skip_keyframes and not args.skip_animate:
        keyframes = generate_keyframes_all(scenes)
    else:
        # Load from disk
        keyframes = {}
        for scene in scenes:
            kf = KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg"
            if kf.exists():
                keyframes[scene["index"]] = kf
            else:
                print(f"  WARNING: Missing keyframe for scene {scene['index']}")

    if args.keyframes_only:
        print("\n--keyframes-only: stopping after keyframe generation.")
        list_scenes()
        return

    # Step 2: Veo animation
    if not args.skip_animate:
        clips = animate_all(scenes, keyframes)
    else:
        clips = {}
        for scene in scenes:
            clip = CLIPS_DIR / f"scene-{scene['index']:02d}.mp4"
            if clip.exists():
                clips[scene["index"]] = clip

    # Step 3: Assembly (only if processing all scenes)
    if not args.scene:
        # Verify all clips exist
        all_clips = {}
        for scene in SCENES:
            clip = CLIPS_DIR / f"scene-{scene['index']:02d}.mp4"
            if clip.exists():
                all_clips[scene["index"]] = clip
        if len(all_clips) == len(SCENES):
            final = assemble_video(SCENES, all_clips)
            print(f"\nDone! Final video: {final}")
        else:
            missing = [s["index"] for s in SCENES if s["index"] not in all_clips]
            print(f"\nSkipping assembly: missing clips for scenes {missing}")
            print("Run without --scene to generate all scenes first.")
    else:
        print(f"\nScene {args.scene} processed. Run without --scene to assemble full video.")

    # Save manifest
    manifest = load_manifest()
    for scene in scenes:
        key = str(scene["index"])
        manifest["scenes"][key] = {
            "lyrics": scene["lyrics"],
            "keyframe": str(KEYFRAMES_DIR / f"scene-{scene['index']:02d}.jpg"),
            "clip": str(CLIPS_DIR / f"scene-{scene['index']:02d}.mp4"),
        }
    save_manifest(manifest)

    list_scenes()


if __name__ == "__main__":
    main()
