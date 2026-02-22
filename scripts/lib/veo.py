#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veo 3.1 video generation wrapper using google-genai SDK.
Follows same patterns as scripts/lib/tts.py (shared google_client, env var auth).
"""
import sys
import os
import time
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from google import genai
from google.genai import types

try:
    from .python_utils import load_project_dotenv
except ImportError:
    from python_utils import load_project_dotenv

load_project_dotenv(Path(__file__).parent.parent.parent)

# --- Configuration ---
VEO_MODEL_ID = "veo-3.1-generate-preview"
IMAGEN_MODEL_ID = "imagen-4.0-generate-001"

MAX_RETRIES = 3
RETRY_BACKOFF = [10, 30, 60]
POLL_INTERVAL_SECONDS = 10

# --- API Setup ---
GOOGLE_GENERATIVE_AI_API_KEY = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")

if not GOOGLE_GENERATIVE_AI_API_KEY:
    raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.")

google_client = genai.Client(api_key=GOOGLE_GENERATIVE_AI_API_KEY)


def generate_image(
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "16:9",
) -> Path:
    """
    Generate an image using Imagen.

    Args:
        prompt: Text prompt describing the desired image.
        output_path: Where to save the generated image (JPEG).
        aspect_ratio: "16:9" or "9:16".

    Returns:
        Path to the saved image.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Generating image ({aspect_ratio}): {prompt[:80]}...")

    response = google_client.models.generate_images(
        model=IMAGEN_MODEL_ID,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=aspect_ratio,
            output_mime_type="image/jpeg",
        ),
    )

    if not response.generated_images:
        raise RuntimeError(f"No images generated. Prompt: {prompt[:100]}")

    image = response.generated_images[0].image
    if image is None:
        raise RuntimeError("Generated image object is None (possibly safety filtered).")

    image.save(str(output_path))
    print(f"  Image saved: {output_path.name}")
    return output_path


def generate_video(
    prompt: str,
    first_frame_path: Path,
    output_path: Path,
    aspect_ratio: str = "16:9",
    duration_seconds: int = 8,
    negative_prompt: str | None = None,
) -> Path:
    """
    Generate an animated video clip using Veo 3.1 from a keyframe image.

    Args:
        prompt: Animation prompt describing the desired motion/scene.
        first_frame_path: Path to the keyframe image (JPEG) to use as first frame.
        output_path: Where to save the generated MP4 clip.
        aspect_ratio: "16:9" or "9:16".
        duration_seconds: Clip duration (5-8 seconds).
        negative_prompt: What to exclude from the video (e.g., "narration, dialogue").

    Returns:
        Path to the saved MP4 clip.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Generating video ({aspect_ratio}, {duration_seconds}s): {prompt[:80]}...")

    config_kwargs: dict = {
        "aspect_ratio": aspect_ratio,
        "duration_seconds": duration_seconds,
        "number_of_videos": 1,
    }
    if negative_prompt:
        config_kwargs["negative_prompt"] = negative_prompt

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        start_time = time.time()
        try:
            operation = google_client.models.generate_videos(
                model=VEO_MODEL_ID,
                prompt=prompt,
                image=types.Image.from_file(location=str(first_frame_path)),
                config=types.GenerateVideosConfig(**config_kwargs),
            )

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

    raise last_error


if __name__ == "__main__":
    print("Veo library loaded successfully.")
    print(f"  Veo model: {VEO_MODEL_ID}")
    print(f"  Imagen model: {IMAGEN_MODEL_ID}")
    print(f"  API key configured: {'yes' if GOOGLE_GENERATIVE_AI_API_KEY else 'no'}")
