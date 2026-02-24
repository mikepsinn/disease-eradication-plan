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
from typing import Any, TYPE_CHECKING, cast

if sys.platform == "win32":
    # sys.stdout.reconfigure exists at runtime on CPython, but is missing from TextIO stubs
    cast(Any, sys.stdout).reconfigure(encoding="utf-8")

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
GEMINI_IMAGE_MODEL_ID = "gemini-3.1-pro-preview"

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
    negative_prompt: str | None = None,
) -> Path:
    """
    Generate an image using Imagen.

    Args:
        prompt: Text prompt describing the desired image.
        output_path: Where to save the generated image (JPEG).
        aspect_ratio: Imagen aspect ratio. Supported: "1:1", "3:4", "4:3", "9:16", "16:9".
        negative_prompt: What to exclude from the image (e.g., "photorealistic, anime").

    Returns:
        Path to the saved image.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Generating image ({aspect_ratio}): {prompt[:80]}...")

    config = types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio=aspect_ratio,
        output_mime_type="image/jpeg",
        negative_prompt=negative_prompt,
    )

    response = google_client.models.generate_images(
        model=IMAGEN_MODEL_ID,
        prompt=prompt,
        config=config,
    )

    if not response.generated_images:
        raise RuntimeError(f"No images generated. Prompt: {prompt[:100]}")

    image = response.generated_images[0].image
    if image is None:
        raise RuntimeError("Generated image object is None (possibly safety filtered).")

    image.save(str(output_path))
    print(f"  Image saved: {output_path.name}")
    return output_path


import base64


def generate_image_gemini(
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "16:9",
    negative_prompt: str | None = None,
) -> Path:
    """
    Generate an image using Gemini 3.1 Pro via generateContent with IMAGE response modality.

    Same interface as generate_image() but uses the Gemini model instead of Imagen,
    which produces better edge-to-edge compositions.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Generating image via Gemini ({aspect_ratio}): {prompt[:80]}...")

    full_prompt = prompt + f"\n\nIMPORTANT: Generate image with aspect ratio {aspect_ratio}."
    if negative_prompt:
        full_prompt += f"\n\nDO NOT include: {negative_prompt}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=full_prompt)],
        ),
    ]

    config = types.GenerateContentConfig(
        response_modalities=["image"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
        ],
    )

    response = google_client.models.generate_content(
        model=GEMINI_IMAGE_MODEL_ID,
        contents=contents,
        config=config,
    )

    if not response.candidates or not response.candidates[0].content:
        raise RuntimeError(f"No image generated. Prompt: {prompt[:100]}")

    for part in response.candidates[0].content.parts or []:
        if part.inline_data and part.inline_data.data:
            image_bytes = base64.b64decode(part.inline_data.data) if isinstance(part.inline_data.data, str) else part.inline_data.data
            output_path.write_bytes(image_bytes)
            print(f"  Image saved: {output_path.name}")
            return output_path

    raise RuntimeError("Response contained no image data (possibly safety filtered).")


# --- Rate-limited wrapper (shared by video and podcast pipelines) ---

if TYPE_CHECKING:
    # For static type checkers, always use the local retry module.
    from .retry import RateLimiter
else:
    # At runtime, fall back to absolute import when run as a stand-alone script.
    try:
        from .retry import RateLimiter
    except ImportError:
        from retry import RateLimiter

# Gemini: 10 requests per minute for pro models; 8 to stay safely under
_gemini_image_rate_limiter = RateLimiter(max_requests=8, window_seconds=60)

# Imagen: 20 requests per minute; 18 to stay safely under
_imagen_rate_limiter = RateLimiter(max_requests=18, window_seconds=60)


def rate_limited_generate_image(
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "16:9",
    negative_prompt: str | None = None,
) -> Path:
    """Generate an image with Gemini 3.1 Pro (rate limited 8 req/min)."""
    _gemini_image_rate_limiter.acquire()
    return generate_image_gemini(prompt=prompt, output_path=output_path,
                                 aspect_ratio=aspect_ratio, negative_prompt=negative_prompt)


def rate_limited_generate_image_imagen(
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "16:9",
    negative_prompt: str | None = None,
) -> Path:
    """Generate an image with Imagen 4.0 (rate limited 18 req/min)."""
    _imagen_rate_limiter.acquire()
    return generate_image(prompt=prompt, output_path=output_path,
                          aspect_ratio=aspect_ratio, negative_prompt=negative_prompt)


def generate_video(
    prompt: str,
    output_path: Path,
    first_frame_path: Path | None = None,
    aspect_ratio: str = "16:9",
    duration_seconds: int = 8,
    negative_prompt: str | None = None,
) -> Path:
    """
    Generate a video clip using Veo 3.1.

    Supports both text-to-video (no image) and image-to-video (with first frame).

    Args:
        prompt: Animation prompt describing the desired motion/scene.
        output_path: Where to save the generated MP4 clip.
        first_frame_path: Optional keyframe image (JPEG) to use as first frame.
                          If None, generates from text prompt only.
        aspect_ratio: "16:9" or "9:16".
        duration_seconds: Clip duration (5-8 seconds).
        negative_prompt: What to exclude from the video (e.g., "narration, dialogue").

    Returns:
        Path to the saved MP4 clip.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    mode = "img2vid" if first_frame_path else "txt2vid"
    print(f"  Generating video [{mode}] ({aspect_ratio}, {duration_seconds}s): {prompt[:80]}...")

    config_kwargs: dict = {
        "aspect_ratio": aspect_ratio,
        "duration_seconds": duration_seconds,
        "number_of_videos": 1,
    }
    if negative_prompt:
        config_kwargs["negative_prompt"] = negative_prompt

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
    print(f"  Imagen model: {IMAGEN_MODEL_ID}")
    print(f"  Gemini image model: {GEMINI_IMAGE_MODEL_ID}")
    print(f"  API key configured: {'yes' if GOOGLE_GENERATIVE_AI_API_KEY else 'no'}")
