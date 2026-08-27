#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QMD Video Generator.

Reads a QMD file with scene definitions, resolves variables, generates TTS
narration, keyframe images, Veo 3.1 animations, and assembles the final video.

Any QMD file following the scene convention can be used as input.

Pipeline: QMD -> resolve variables -> TTS -> keyframes -> Veo 3.1 -> ffmpeg

Usage:
    python scripts/generate_video_from_qmd.py knowledge/educational-film.qmd
    python scripts/generate_video_from_qmd.py knowledge/educational-film.qmd --tts-only
    python scripts/generate_video_from_qmd.py knowledge/educational-film.qmd --scene 3
    python scripts/generate_video_from_qmd.py knowledge/educational-film.qmd --list

QMD Convention:
  - YAML frontmatter with `video:` block (visual-style, tts-voice, tts-instructions,
    no-text, negative-prompt, output-dir)
  - Sections: ## Scene N: Title {.scene}
  - Direction divs: :::{.scene-direction} with numbered **Keyframe N:**/**Animation N:**
    pairs (one per ~8s of narration). Unnumbered **Keyframe:**/**Animation:** also works.
  - Narration as paragraph text (may use {{< var >}} references)
  - Keyframe images: :::{.scene-keyframe} ![](path) :::
"""
import io
import sys
import json
import re
import argparse
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from google.genai import types
from lib.tts import generate_speech, DEFAULT_VOICE, DEFAULT_SPEAKING_INSTRUCTIONS
from lib.alignment import align_chapter, timestamps_for_char_range
from lib.veo import generate_video
from lib.image_gen import google_client
from dih_models.variable_replacement import load_variables, replace_variables

PROJECT_ROOT = Path(__file__).parent.parent
VARIABLES_YML = PROJECT_ROOT / "_variables.yml"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2
VEO_PARALLEL_WORKERS = 4


# =============================================================================
# Path resolution (all derived from QMD slug + optional frontmatter override)
# =============================================================================

def _slugify(text: str) -> str:
    """Convert title to filename-safe slug: 'The Bond Machine' -> 'the-bond-machine'."""
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


class VideoPaths:
    """All output paths for a video project, derived from the QMD slug."""

    def __init__(self, slug: str, output_dir_override: str | None = None):
        self.slug = slug
        if output_dir_override:
            self.output_dir = PROJECT_ROOT / output_dir_override
        else:
            self.output_dir = (
                PROJECT_ROOT / "assets" / "audiobook" / "manual-paperback"
                / "video" / slug
            )
        self.keyframes_dir = PROJECT_ROOT / "assets" / "images" / slug
        self.clips_dir = self.output_dir / "clips"
        self.audio_path = self.output_dir / "narration.wav"
        self.manifest_path = self.output_dir / "manifest.json"
        self.prepared_txt = (
            PROJECT_ROOT / "assets" / "audiobook" / "manual-paperback"
            / "narration-txt-chapters" / f"{slug}.prepared.txt"
        )

    def keyframe(self, scene_index: int, kf_index: int) -> Path:
        """Path for keyframe image: assets/images/{slug}/SS-KK.jpg"""
        return self.keyframes_dir / f"{scene_index:02d}-{kf_index:02d}.jpg"

    def clip(self, scene_index: int, kf_index: int) -> Path:
        """Path for Veo clip: clips/scene-SS-KK.mp4"""
        return self.clips_dir / f"scene-{scene_index:02d}-{kf_index:02d}.mp4"

    def final_video(self, aspect: str) -> Path:
        tag = "16x9" if aspect == "16:9" else "9x16"
        return self.output_dir.parent / f"{self.slug}-{tag}.mp4"


# =============================================================================
# QMD Parser
# =============================================================================

def parse_qmd(qmd_path: Path) -> dict:
    """Parse a QMD file into frontmatter + scene list.

    Expects headings: ## Scene N: Title {.scene}
    Each scene section may contain:
      - One or more :::{.scene-direction} divs, each with **Keyframe:**/**Animation:**
        (one pair per div = new format, or numbered pairs in one div = old format)
      - Narration paragraphs (plain text with {{< var >}} references)
      - :::{.scene-keyframe} ![](path) ::: image blocks (ignored for generation)

    Returns dict with 'frontmatter' and 'scenes'. Each scene has:
      index, title, narration_text, keyframes (list of {keyframe_prompt, veo_prompt})
    """
    content = qmd_path.read_text(encoding="utf-8")

    # --- frontmatter ---
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    frontmatter = {}
    if fm_match:
        import yaml
        frontmatter = yaml.safe_load(fm_match.group(1)) or {}

    # --- split by scene headings ---
    scene_re = r"## Scene (\d+): (.+?) \{\.scene\}"
    parts = re.split(scene_re, content)

    scenes = []
    for i in range(1, len(parts), 3):
        index = int(parts[i])
        title = parts[i + 1].strip()
        body = parts[i + 2]

        # Extract keyframe/animation pairs from ALL direction divs in this scene.
        # Handles both formats:
        #   New: multiple divs, each with one **Keyframe:**/**Animation:** pair
        #   Old: one div with numbered **Keyframe N:**/**Animation N:** pairs
        keyframes = []
        for dir_match in re.finditer(
            r":::\{\.scene-direction\}\s*(.*?)\s*:::", body, re.DOTALL
        ):
            dt = dir_match.group(1)
            entries = re.findall(
                r"\*\*(Keyframe|Animation)\s*(\d*):\*\*\s*"
                r"(.*?)(?=\*\*(?:Keyframe|Animation)\s*\d*:|\Z)",
                dt, re.DOTALL,
            )
            kf_map: dict[int, str] = {}
            an_map: dict[int, str] = {}
            for kind, num_str, text in entries:
                num = int(num_str) if num_str else 1
                clean = " ".join(text.split())
                if kind == "Keyframe":
                    kf_map[num] = clean
                else:
                    an_map[num] = clean

            for n in sorted(set(kf_map) | set(an_map)):
                keyframes.append({
                    "keyframe_prompt": kf_map.get(n, ""),
                    "veo_prompt": an_map.get(n, ""),
                })

        if not keyframes:
            keyframes = [{"keyframe_prompt": "", "veo_prompt": ""}]

        # Extract per-keyframe narration chunks from the interleaved structure.
        # Split body by direction divs: text between them is the narration for
        # the keyframe that follows.
        dir_pattern = r":::\{\.scene-direction\}.*?:::"
        chunks = re.split(dir_pattern, body, flags=re.DOTALL)
        for ci, chunk in enumerate(chunks):
            chunk = re.sub(
                r":::\{\.scene-keyframe\}.*?:::", "", chunk, flags=re.DOTALL
            )
            chunk = re.sub(r"!\[.*?\]\(.*?\)(?:\{.*?\})?", "", chunk)
            chunk = re.sub(r"^---+\s*$", "", chunk, flags=re.MULTILINE)
            chunks[ci] = re.sub(r"\n{3,}", "\n\n", chunk).strip()

        # Map: chunks[i] is the narration preceding keyframes[i]
        for ki, kf in enumerate(keyframes):
            kf["narration_chunk"] = chunks[ki] if ki < len(chunks) else ""

        # Extract narration: strip direction divs, keyframe divs, images, rules
        narration = body
        narration = re.sub(
            r":::\{\.scene-direction\}.*?:::", "", narration, flags=re.DOTALL
        )
        narration = re.sub(
            r":::\{\.scene-keyframe\}.*?:::", "", narration, flags=re.DOTALL
        )
        narration = re.sub(r"!\[.*?\]\(.*?\)(?:\{.*?\})?", "", narration)
        narration = re.sub(r"^---+\s*$", "", narration, flags=re.MULTILINE)
        narration = re.sub(r"\n{3,}", "\n\n", narration).strip()

        scenes.append({
            "index": index,
            "title": title,
            "narration_text": narration,
            "keyframes": keyframes,
        })

    return {"frontmatter": frontmatter, "scenes": scenes}


# =============================================================================
# Variable resolution
# =============================================================================

def resolve_narration(scenes: list[dict], variables: dict):
    """Resolve {{< var >}} in each scene's narration_text -> narration_resolved."""
    for scene in scenes:
        resolved = replace_variables(
            scene["narration_text"], variables, highlight_missing=False
        )
        resolved = re.sub(r"\{\{<\s*var\s+\w+\s*>\}\}", "", resolved)
        resolved = _strip_ci(resolved)
        scene["narration_resolved"] = resolved


def _strip_ci(text: str) -> str:
    """Strip confidence intervals like '(95% CI: 324 years-712 years)' from resolved values."""
    return re.sub(r"\s*\(9[05]% CI:[^)]+\)", "", text)


def resolve_keyframe_prompts(scenes: list[dict], variables: dict):
    """Resolve {{< var >}} in keyframe prompts, veo prompts, and narration chunks."""
    for scene in scenes:
        for kf in scene.get("keyframes", []):
            for key in ("keyframe_prompt", "veo_prompt", "narration_chunk"):
                if kf.get(key):
                    resolved = replace_variables(
                        kf[key], variables, highlight_missing=False
                    )
                    resolved = re.sub(r"\{\{<\s*var\s+\w+\s*>\}\}", "", resolved)
                    resolved = _strip_ci(resolved)
                    kf[key] = resolved


def full_narration(scenes: list[dict]) -> str:
    return "\n\n".join(s["narration_resolved"] for s in scenes)


# =============================================================================
# Timestamp allocation
# =============================================================================

def allocate_timestamps(scenes: list[dict], total_s: float):
    """Distribute audio duration across scenes proportionally by text length.

    Fallback used when alignment data is not available.
    """
    total_chars = sum(len(s["narration_resolved"]) for s in scenes)
    cur = 0.0
    for s in scenes:
        dur = (len(s["narration_resolved"]) / total_chars) * total_s
        s["start_s"] = round(cur, 2)
        s["end_s"] = round(cur + dur, 2)
        cur += dur
    scenes[-1]["end_s"] = round(total_s, 2)


def allocate_timestamps_aligned(
    scenes: list[dict], audio_path: Path, text_path: Path, total_s: float
):
    """Use forced alignment (stable-ts) to find precise scene boundaries.

    Runs Whisper alignment on the full narration audio, then looks up the
    character range of each scene's text to get exact start/end timestamps.
    Falls back to proportional allocation on failure.
    """
    print("\n=== Forced Alignment ===")
    alignment_output = audio_path.parent / "alignment.json"

    chapter = {"index": 0, "title": "full-narration"}
    words = align_chapter(
        wav_path=audio_path,
        text_path=text_path,
        output_path=alignment_output,
        model_name="base",
        chapter=chapter,
    )

    if not words:
        print("  [WARN] Alignment returned no words, falling back to proportional")
        allocate_timestamps(scenes, total_s)
        return

    # Build the full narration text the same way full_narration() does
    full_text = "\n\n".join(s["narration_resolved"] for s in scenes)

    # Find each scene's character range in the full text
    cursor = 0
    for s in scenes:
        scene_text = s["narration_resolved"]
        char_start = full_text.find(scene_text, cursor)
        if char_start < 0:
            char_start = cursor
        char_end = char_start + len(scene_text)
        cursor = char_end

        start_ms, end_ms = timestamps_for_char_range(words, char_start, char_end)
        s["start_s"] = round(start_ms / 1000.0, 2)
        s["end_s"] = round(end_ms / 1000.0, 2)

    # Ensure first scene starts at 0 and last scene ends at total duration
    scenes[0]["start_s"] = 0.0
    scenes[-1]["end_s"] = round(total_s, 2)

    # Fill any gaps between scenes (alignment may leave small gaps)
    for i in range(1, len(scenes)):
        if scenes[i]["start_s"] != scenes[i - 1]["end_s"]:
            midpoint = (scenes[i]["start_s"] + scenes[i - 1]["end_s"]) / 2
            scenes[i - 1]["end_s"] = round(midpoint, 2)
            scenes[i]["start_s"] = round(midpoint, 2)

    print("  Scene timestamps (aligned):")
    for s in scenes:
        print(f"    {s['index']:2d}. {s['start_s']:6.1f}s - {s['end_s']:6.1f}s  {s['title']}")


def scene_dur(s: dict) -> float:
    return s.get("end_s", 0) - s.get("start_s", 0)


def clip_target_dur(s: dict) -> float:
    """Target duration for each Veo clip in a scene (scene_dur / n_keyframes)."""
    n = len(s.get("keyframes", [1]))
    return scene_dur(s) / max(n, 1)


# =============================================================================
# TTS
# =============================================================================

def generate_tts(text: str, cfg: dict, paths: VideoPaths) -> Path:
    print("\n=== Step 0: TTS Narration ===")
    if paths.audio_path.exists():
        print(f"  [CACHED] {paths.audio_path.name}")
        return paths.audio_path

    voice = cfg.get("tts-voice", DEFAULT_VOICE)
    instr = cfg.get("tts-instructions", DEFAULT_SPEAKING_INSTRUCTIONS)
    print(f"  Voice: {voice}  |  {len(text):,} chars")
    generate_speech(
        text=text, output_path=paths.audio_path, voice_name=voice,
        speaking_instructions=instr, verbose=True,
    )
    return paths.audio_path


def audio_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {r.stderr[:200]}")
    return float(r.stdout.strip())


# =============================================================================
# Keyframe generation
# =============================================================================

def generate_keyframe(scene_index: int, kf_index: int,
                      keyframe_prompt: str, style: str,
                      paths: VideoPaths,
                      narration_chunk: str = "",
                      full_narration: str = "") -> Path:
    paths.keyframes_dir.mkdir(parents=True, exist_ok=True)
    out = paths.keyframe(scene_index, kf_index)
    if out.exists():
        print(f"  [CACHED] {out.name}")
        return out

    print(f"  Generating keyframe {scene_index}-{kf_index}: {(narration_chunk or keyframe_prompt)[:60]}...")

    if narration_chunk:
        prompt = (
            f"Visual style: {style}\n\n"
            f"Illustrate this line:\n\"{narration_chunk}\"\n\n"
            f"Given its context in this script:\n{full_narration}\n\n"
        )
    else:
        prompt = f"{style} {keyframe_prompt}"

    prompt += "\nIMPORTANT: Generate image with aspect ratio 16:9."

    response = google_client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=[{"parts": [{"text": prompt}]}],
        config=types.GenerateContentConfig(
            response_modalities=["image"],
            safety_settings=[
                types.SafetySetting(
                    category=c, threshold=types.HarmBlockThreshold.BLOCK_NONE
                )
                for c in [
                    types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                ]
            ],
        ),
    )
    if not response.candidates or not response.candidates[0].content:
        raise RuntimeError(f"No image for keyframe {scene_index}-{kf_index}")

    import base64
    for part in response.candidates[0].content.parts or []:
        if part.inline_data and part.inline_data.data:
            data = part.inline_data.data
            img = base64.b64decode(data) if isinstance(data, str) else data
            out.write_bytes(img)
            print(f"  [OK] {out.name}")
            return out

    raise RuntimeError(f"No image data for keyframe {scene_index}-{kf_index}")


def generate_keyframes_all(scenes: list[dict], cfg: dict,
                           paths: VideoPaths) -> dict[tuple[int, int], Path]:
    """Generate all keyframe images across all scenes.

    Returns: {(scene_index, kf_index): Path}
    """
    print("\n=== Step 1: Keyframes ===")
    style = cfg.get("visual-style", "")
    total = sum(len(s["keyframes"]) for s in scenes)
    print(f"  {total} keyframes across {len(scenes)} scenes")

    # Build full narration for context
    full_narr = "\n\n".join(s.get("narration_resolved", s["narration_text"])
                            for s in scenes)

    kfs: dict[tuple[int, int], Path] = {}
    for scene in scenes:
        for ki, kf in enumerate(scene["keyframes"], 1):
            for attempt in range(3):
                try:
                    kfs[(scene["index"], ki)] = generate_keyframe(
                        scene["index"], ki, kf["keyframe_prompt"],
                        style, paths,
                        narration_chunk=kf.get("narration_chunk", ""),
                        full_narration=full_narr,
                    )
                    break
                except RuntimeError as e:
                    if attempt < 2:
                        print(f"  [RETRY] {scene['index']}-{ki} attempt {attempt+1}: {e}")
                        time.sleep(5)
                        paths.keyframe(scene["index"], ki).unlink(missing_ok=True)
                    else:
                        raise
    return kfs


# =============================================================================
# Veo animation
# =============================================================================

def animate_clip(scene_index: int, kf_index: int, veo_prompt: str,
                 kf_path: Path, cfg: dict, paths: VideoPaths) -> Path:
    paths.clips_dir.mkdir(parents=True, exist_ok=True)
    out = paths.clip(scene_index, kf_index)
    if out.exists():
        print(f"  [CACHED] {out.name}")
        return out

    print(f"  Animating {scene_index}-{kf_index}...")
    generate_video(
        prompt="Animate this image naturally.",
        output_path=out, first_frame_path=kf_path,
        aspect_ratio="16:9", duration_seconds=8,
    )
    return out


def animate_all(scenes: list[dict], kfs: dict[tuple[int, int], Path],
                cfg: dict, paths: VideoPaths) -> dict[tuple[int, int], Path]:
    """Animate all keyframes across all scenes.

    Returns: {(scene_index, kf_index): clip_path}
    """
    print("\n=== Step 2: Veo 3.1 Animation ===")
    clips: dict[tuple[int, int], Path] = {}
    work: list[tuple[int, int, str]] = []  # (scene_idx, kf_idx, veo_prompt)

    for s in scenes:
        for ki, kf in enumerate(s["keyframes"], 1):
            key = (s["index"], ki)
            cp = paths.clip(s["index"], ki)
            if cp.exists():
                print(f"  [CACHED] {cp.name}")
                clips[key] = cp
            else:
                work.append((s["index"], ki, kf["veo_prompt"]))
    if not work:
        print("  All clips cached.")
        return clips

    print(f"  Generating {len(work)} clips ({VEO_PARALLEL_WORKERS} workers)...")
    errors = []
    with ThreadPoolExecutor(max_workers=VEO_PARALLEL_WORKERS) as pool:
        futs = {
            pool.submit(
                animate_clip, si, ki, vp, kfs[(si, ki)], cfg, paths
            ): (si, ki)
            for si, ki, vp in work
        }
        for f in as_completed(futs):
            key = futs[f]
            try:
                clips[key] = f.result()
            except Exception as e:
                errors.append(f"Clip {key[0]}-{key[1]}: {e}")
                print(f"  [ERROR] Clip {key[0]}-{key[1]}: {e}")
    if errors:
        raise RuntimeError(
            f"Failed {len(errors)} clip(s):\n" + "\n".join(errors)
        )
    return clips


# =============================================================================
# Assembly
# =============================================================================

def assemble_video(scenes: list[dict], clips: dict[tuple[int, int], Path],
                   audio: Path, aspect: str, paths: VideoPaths,
                   title: str = "") -> Path:
    tag = "16x9" if aspect == "16:9" else "9x16"
    out = paths.final_video(aspect)
    adj_dir = paths.clips_dir / f"_adj-{tag}"
    adj_dir.mkdir(parents=True, exist_ok=True)
    dur = audio_duration(audio)
    print(f"\n=== Step 3: Assembly ({tag}, {dur:.1f}s) ===")

    concat, temps = [], []
    for s in sorted(scenes, key=lambda x: x["index"]):
        n_kf = len(s["keyframes"])
        target_per_clip = scene_dur(s) / max(n_kf, 1)

        for ki in range(1, n_kf + 1):
            key = (s["index"], ki)
            cp = clips[key]
            adj = adj_dir / f"scene-{s['index']:02d}-{ki:02d}.mp4"

            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(cp)],
                capture_output=True, text=True,
            )
            clip_s = float(probe.stdout.strip()) if probe.returncode == 0 else 8.0
            ts = target_per_clip / clip_s

            filt = []
            if abs(ts - 1.0) >= 0.05:
                filt.append(f"setpts=PTS*{ts:.4f}")
            if aspect == "9:16":
                filt += ["crop=ih*9/16:ih", "scale=1080:1920"]

            label = f"{ts:.2f}x" if abs(ts - 1.0) >= 0.05 else "1:1"
            print(
                f"    {s['index']:2d}-{ki:02d}: "
                f"{clip_s:.1f}s -> {target_per_clip:.1f}s ({label})"
            )

            cmd = ["ffmpeg", "-y", "-i", str(cp)]
            if filt:
                cmd += ["-filter:v", ",".join(filt)]
            cmd += [
                "-t", f"{target_per_clip:.3f}", "-c:v", "libx264",
                "-preset", "fast", "-crf", "23", "-an",
                "-movflags", "+faststart", str(adj),
            ]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(
                    f"ffmpeg clip {s['index']}-{ki}: {r.stderr[:300]}"
                )
            temps.append(adj)
            concat.append(f"file '{adj.as_posix()}'")

    concat_f = paths.clips_dir / f"_concat-{tag}.txt"
    concat_f.write_text("\n".join(concat), encoding="utf-8")

    meta_title = title or paths.slug.replace("-", " ").title()
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_f),
        "-i", str(audio),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.3f}", "-movflags", "+faststart",
        "-metadata", f"title={meta_title}",
        "-metadata", "artist=Wishonia",
        str(out),
    ]
    print("  Running ffmpeg assembly...")
    r = subprocess.run(cmd, capture_output=True, text=True)

    concat_f.unlink(missing_ok=True)
    for t in temps:
        t.unlink(missing_ok=True)
    import shutil
    shutil.rmtree(adj_dir, ignore_errors=True)

    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg assembly failed: {r.stderr[:500]}")

    mb = out.stat().st_size / 1024 / 1024
    print(f"  [OK] {out.name} ({mb:.1f} MB)")
    return out


# =============================================================================
# Status display
# =============================================================================

def show_scenes(scenes: list[dict], paths: VideoPaths):
    print(f"\n{paths.slug}: {len(scenes)} scenes")
    print("=" * 90)
    total_dur = 0.0
    total_kf = 0
    for s in scenes:
        d = scene_dur(s)
        n_kf = len(s["keyframes"])
        total_kf += n_kf
        kf_ok = sum(
            1 for ki in range(1, n_kf + 1)
            if paths.keyframe(s["index"], ki).exists()
        )
        cl_ok = sum(
            1 for ki in range(1, n_kf + 1)
            if paths.clip(s["index"], ki).exists()
        )
        kf_tag = f"K:{kf_ok}/{n_kf}"
        cl_tag = f"V:{cl_ok}/{n_kf}"
        per_clip = d / max(n_kf, 1)
        print(
            f"  {s['index']:2d}. [{kf_tag} {cl_tag}] "
            f"{s.get('start_s', 0):5.1f}-{s.get('end_s', 0):5.1f}s "
            f"({d:4.1f}s, {n_kf}kf, ~{per_clip:.1f}s/clip) {s['title']}"
        )
        total_dur += d
    print("=" * 90)
    print(
        f"  Total: {total_dur:.0f}s ({total_dur / 60:.1f}min)  |  "
        f"{total_kf} keyframes  |  K=keyframes V=clips"
    )
    if paths.audio_path.exists():
        print(f"  Audio: {paths.audio_path.name}")
    for tag in ["16x9", "9x16"]:
        aspect = "16:9" if tag == "16x9" else "9:16"
        f = paths.final_video(aspect)
        if f.exists():
            print(
                f"  Final ({tag}): {f.name} "
                f"({f.stat().st_size / 1024 / 1024:.1f} MB)"
            )


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate video from a QMD file with scene definitions"
    )
    parser.add_argument(
        "qmd", help="Path to the QMD file (relative to project root)"
    )
    parser.add_argument("--tts-only", action="store_true")
    parser.add_argument("--keyframes-only", action="store_true")
    parser.add_argument("--skip-keyframes", action="store_true")
    parser.add_argument("--skip-animate", action="store_true")
    parser.add_argument("--scene", type=int, help="Single scene number")
    parser.add_argument("--list", "-l", action="store_true")
    parser.add_argument("--force", "-f", action="store_true")
    parser.add_argument("--portrait-only", action="store_true")
    parser.add_argument("--landscape-only", action="store_true")
    args = parser.parse_args()

    # Resolve QMD path
    qmd_path = Path(args.qmd)
    if not qmd_path.is_absolute():
        qmd_path = PROJECT_ROOT / qmd_path
    if not qmd_path.exists():
        print(f"ERROR: {qmd_path} not found")
        sys.exit(1)

    slug = qmd_path.stem

    # Parse QMD
    parsed = parse_qmd(qmd_path)
    video_cfg = parsed["frontmatter"].get("video", {})
    all_scenes = parsed["scenes"]
    if not all_scenes:
        print("ERROR: No scenes found (need ## Scene N: Title {.scene} headings)")
        sys.exit(1)

    # Set up output paths (from frontmatter or slug)
    paths = VideoPaths(slug, video_cfg.get("output-dir"))

    total_kf = sum(len(s["keyframes"]) for s in all_scenes)
    print("QMD Video Generator")
    print(f"  Source: {qmd_path.relative_to(PROJECT_ROOT)}")
    print(f"  Slug:   {slug}")
    print(f"  Output: {paths.output_dir.relative_to(PROJECT_ROOT)}")
    print(f"  Scenes: {len(all_scenes)}  |  Keyframes: {total_kf}")

    # Resolve variables
    variables = load_variables(VARIABLES_YML)
    resolve_narration(all_scenes, variables)
    resolve_keyframe_prompts(all_scenes, variables)

    # --list
    if args.list:
        allocate_timestamps(all_scenes, 180.0)
        show_scenes(all_scenes, paths)
        return

    # --scene filter
    scenes = all_scenes
    if args.scene:
        scenes = [s for s in all_scenes if s["index"] == args.scene]
        if not scenes:
            print(f"ERROR: Scene {args.scene} not found")
            sys.exit(1)

    # --force cleanup
    if args.force:
        for s in scenes:
            for ki in range(1, len(s["keyframes"]) + 1):
                for p in [
                    paths.keyframe(s["index"], ki),
                    paths.clip(s["index"], ki),
                ]:
                    if p.exists():
                        p.unlink()
                        print(f"  --force: deleted {p.name}")
        if paths.audio_path.exists() and not args.scene:
            paths.audio_path.unlink()
            print("  --force: deleted TTS audio")

    # Step 0: TTS (skip if only generating keyframes)
    narration = full_narration(all_scenes)

    paths.prepared_txt.parent.mkdir(parents=True, exist_ok=True)
    paths.prepared_txt.write_text(narration, encoding="utf-8")
    print(f"  Saved: {paths.prepared_txt.name}")

    if args.keyframes_only:
        # Keyframes don't need audio; use estimate for display
        allocate_timestamps(all_scenes, 180.0)
        kfs = generate_keyframes_all(scenes, video_cfg, paths)
        show_scenes(all_scenes, paths)
        return

    audio = generate_tts(narration, video_cfg, paths)
    dur = audio_duration(audio)
    print(f"  Audio duration: {dur:.1f}s")

    allocate_timestamps_aligned(all_scenes, audio, paths.prepared_txt, dur)

    if args.tts_only:
        show_scenes(all_scenes, paths)
        return

    # Step 1: Keyframes
    if not args.skip_keyframes and not args.skip_animate:
        kfs = generate_keyframes_all(scenes, video_cfg, paths)
    else:
        kfs = {}
        for s in scenes:
            for ki in range(1, len(s["keyframes"]) + 1):
                p = paths.keyframe(s["index"], ki)
                if p.exists():
                    kfs[(s["index"], ki)] = p

    if args.keyframes_only:
        show_scenes(all_scenes, paths)
        return

    # Step 2: Veo animation
    if not args.skip_animate:
        clips = animate_all(scenes, kfs, video_cfg, paths)
    else:
        clips = {}
        for s in scenes:
            for ki in range(1, len(s["keyframes"]) + 1):
                p = paths.clip(s["index"], ki)
                if p.exists():
                    clips[(s["index"], ki)] = p

    # Step 3: Assembly (only with all scenes)
    if not args.scene:
        all_clips: dict[tuple[int, int], Path] = {}
        for s in all_scenes:
            for ki in range(1, len(s["keyframes"]) + 1):
                p = paths.clip(s["index"], ki)
                if p.exists():
                    all_clips[(s["index"], ki)] = p

        expected = sum(len(s["keyframes"]) for s in all_scenes)
        if len(all_clips) == expected:
            ratios = ["16:9", "9:16"]
            if args.portrait_only:
                ratios = ["9:16"]
            elif args.landscape_only:
                ratios = ["16:9"]
            title = parsed["frontmatter"].get("title", "")
            for ar in ratios:
                assemble_video(all_scenes, all_clips, audio, ar, paths, title)
        else:
            have = len(all_clips)
            print(f"\n  {have}/{expected} clips ready. Missing clips:")
            for s in all_scenes:
                for ki in range(1, len(s["keyframes"]) + 1):
                    if (s["index"], ki) not in all_clips:
                        print(f"    {s['index']}-{ki}")
    else:
        print(
            f"\n  Scene {args.scene} done. "
            "Run without --scene for full assembly."
        )

    # Save manifest
    manifest = {
        "source": str(qmd_path.relative_to(PROJECT_ROOT)),
        "audio": str(paths.audio_path.relative_to(PROJECT_ROOT)),
        "scenes": {},
    }
    for s in all_scenes:
        scene_kfs = {}
        for ki in range(1, len(s["keyframes"]) + 1):
            scene_kfs[str(ki)] = {
                "keyframe": f"{s['index']:02d}-{ki:02d}.jpg",
                "clip": f"scene-{s['index']:02d}-{ki:02d}.mp4",
            }
        manifest["scenes"][str(s["index"])] = {
            "title": s["title"],
            "start_s": s.get("start_s", 0),
            "end_s": s.get("end_s", 0),
            "n_keyframes": len(s["keyframes"]),
            "keyframes": scene_kfs,
        }
    paths.manifest_path.parent.mkdir(parents=True, exist_ok=True)
    paths.manifest_path.write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    show_scenes(all_scenes, paths)


if __name__ == "__main__":
    main()
