#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image generation wrapper using google-genai SDK.
Supports Imagen 4.0 and Gemini 3.1 Pro image generation.
"""
import sys
import os
import base64
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast

if sys.platform == "win32":
    cast(Any, sys.stdout).reconfigure(encoding="utf-8")

from google import genai
from google.genai import types

try:
    from .python_utils import load_project_dotenv
except ImportError:
    from python_utils import load_project_dotenv

load_project_dotenv(Path(__file__).parent.parent.parent)

# --- Configuration ---
IMAGEN_MODEL_ID = "imagen-4.0-generate-001"
GEMINI_IMAGE_MODEL_ID = "gemini-3.1-flash-image-preview"  # Nano Banana 2

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
    Generate an image using Imagen 4.0.

    Args:
        prompt: Text prompt describing the desired image.
        output_path: Where to save the generated image (JPEG).
        aspect_ratio: Supported: "1:1", "3:4", "4:3", "9:16", "16:9".
        negative_prompt: What to exclude from the image.

    Returns:
        Path to the saved image.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Generating image via Imagen ({aspect_ratio}): {prompt[:80]}...")

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

    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=full_prompt)],
    )

    config = types.GenerateContentConfig(
        response_modalities=["image"],  # type: ignore[reportCallIssue]
        safety_settings=[  # type: ignore[reportCallIssue]
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
        ],
    )

    import re as _re
    for _attempt in range(1, 4):
        try:
            response = google_client.models.generate_content(
                model=GEMINI_IMAGE_MODEL_ID,
                contents=user_content,
                config=config,
            )
            break
        except Exception as _e:
            err_str = str(_e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                # Extract retry delay from error if available
                delay_match = _re.search(r'retryDelay.*?(\d+)', err_str)
                wait = int(delay_match.group(1)) + 5 if delay_match else 30
                if _attempt < 3:
                    print(f"  [429] Rate limited, waiting {wait}s (attempt {_attempt}/3)...")
                    import time as _time
                    _time.sleep(wait)
                    continue
            raise

    if not response.candidates:
        raise RuntimeError(
            f"No image generated. prompt_feedback={getattr(response, 'prompt_feedback', None)}, "
            f"prompt: {prompt[:120]}"
        )
    candidate = response.candidates[0]
    content = candidate.content
    if not content:
        raise RuntimeError(
            f"No image generated. finish_reason={getattr(candidate, 'finish_reason', None)}, "
            f"safety_ratings={getattr(candidate, 'safety_ratings', None)}, prompt: {prompt[:120]}"
        )

    for part in content.parts or []:
        if part.inline_data and part.inline_data.data:
            image_bytes = base64.b64decode(part.inline_data.data) if isinstance(part.inline_data.data, str) else part.inline_data.data
            output_path.write_bytes(image_bytes)
            print(f"  Image saved: {output_path.name}")
            return output_path

    # Response had candidates but no image bytes
    parts_info = [(type(p).__name__, bool(getattr(p, 'inline_data', None))) for p in (content.parts or [])]
    finish = getattr(candidate, 'finish_reason', None)
    safety = getattr(candidate, 'safety_ratings', None)
    raise RuntimeError(
        f"Response contained no image data. finish_reason={finish}, "
        f"safety_ratings={safety}, parts={parts_info}, "
        f"prompt: {prompt[:120]}"
    )


# --- Rate-limited wrappers ---

if TYPE_CHECKING:
    from .retry import RateLimiter
else:
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


if __name__ == "__main__":
    print("Image generation library loaded successfully.")
    print(f"  Imagen model: {IMAGEN_MODEL_ID}")
    print(f"  Gemini image model: {GEMINI_IMAGE_MODEL_ID}")
    print(f"  API key configured: {'yes' if GOOGLE_GENERATIVE_AI_API_KEY else 'no'}")
