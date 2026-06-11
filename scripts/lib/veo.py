#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veo 3.1 video generation wrapper using google-genai SDK.
Follows same patterns as scripts/lib/tts.py (shared google_client, env var auth).

Image generation has moved to scripts/lib/image_gen.py.
"""
import sys
import time
from pathlib import Path
from typing import Any, cast

if sys.platform == "win32":
    cast(Any, sys.stdout).reconfigure(encoding="utf-8")

from google.genai import types

# Re-export image functions for backwards compatibility
from .image_gen import (  # noqa: F401
    google_client,
    generate_image,
    generate_image_gemini,
    rate_limited_generate_image,
    rate_limited_generate_image_imagen,
)

# --- Configuration ---
VEO_MODEL_ID = "veo-3.1-generate-preview"

MAX_RETRIES = 3
RETRY_BACKOFF = [10, 30, 60]
POLL_INTERVAL_SECONDS = 10


def generate_video(
    prompt: str,
    output_path: Path,
    first_frame_path: Path | None = None,
    reference_image_paths: list[Path] | None = None,
    aspect_ratio: str = "16:9",
    duration_seconds: int = 8,
    negative_prompt: str | None = None,
) -> Path:
    """
    Generate a video clip using Veo 3.1.

    Supports text-to-video, image-to-video (first frame), and reference images
    for character/style consistency across scenes.

    Args:
        prompt: Animation prompt describing the desired motion/scene.
        output_path: Where to save the generated MP4 clip.
        first_frame_path: Optional keyframe image (JPEG) to use as first frame.
                          If None, generates from text prompt only.
        reference_image_paths: Optional list of up to 3 reference images for
                               character/style consistency across scenes.
        aspect_ratio: "16:9" or "9:16".
        duration_seconds: Clip duration (5-8 seconds).
        negative_prompt: What to exclude from the video (e.g., "narration, dialogue").

    Returns:
        Path to the saved MP4 clip.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    reference_paths = reference_image_paths or []
    has_refs = len(reference_paths) > 0
    mode = "img2vid" if first_frame_path else ("ref2vid" if has_refs else "txt2vid")
    print(f"  Generating video [{mode}] ({aspect_ratio}, {duration_seconds}s): {prompt[:80]}...")

    config_kwargs: dict = {
        "aspect_ratio": aspect_ratio,
        "duration_seconds": duration_seconds,
        "number_of_videos": 1,
    }
    if negative_prompt:
        config_kwargs["negative_prompt"] = negative_prompt
    if has_refs:
        config_kwargs["reference_images"] = [
            types.Image.from_file(location=str(p)) for p in reference_paths
        ]

    gen_kwargs: dict = {
        "model": VEO_MODEL_ID,
        "prompt": prompt,
        "config": types.GenerateVideosConfig(**config_kwargs),
    }
    if first_frame_path:
        gen_kwargs["image"] = types.Image.from_file(location=str(first_frame_path))

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        start_time = time.time()
        try:
            operation = google_client.models.generate_videos(**gen_kwargs)

            # Poll until complete
            while not operation.done:
                elapsed = time.time() - start_time
                print(f"    Polling... ({elapsed:.0f}s elapsed)", flush=True)
                time.sleep(POLL_INTERVAL_SECONDS)
                operation = google_client.operations.get(operation)

            elapsed = time.time() - start_time

            if operation.error:
                raise RuntimeError(f"Veo generation failed: {operation.error}")

            if not operation.result or not operation.result.generated_videos:
                raise RuntimeError("No videos in operation result.")

            generated = operation.result.generated_videos[0]
            if generated.video is None:
                raise RuntimeError("Generated video object is None (possibly safety filtered).")

            # Download video bytes via SDK (handles auth for remote URIs)
            video_bytes = google_client.files.download(file=generated)
            with open(output_path, "wb") as f:
                f.write(video_bytes)

            print(f"  Video saved: {output_path.name} ({elapsed:.0f}s)")
            return output_path

        except Exception as e:
            last_error = e
            elapsed = time.time() - start_time
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF[attempt - 1]
                print(f"  [RETRY] Attempt {attempt}/{MAX_RETRIES} failed after {elapsed:.0f}s: {e}")
                print(f"  [RETRY] Waiting {wait}s before retry...", flush=True)
                time.sleep(wait)
            else:
                print(f"  [FAILED] All {MAX_RETRIES} attempts failed. Last error: {e}")

    if last_error is not None:
        raise last_error
    raise RuntimeError("Video generation failed for an unknown reason.")


if __name__ == "__main__":
    print("Veo library loaded successfully.")
    print(f"  Veo model: {VEO_MODEL_ID}")
