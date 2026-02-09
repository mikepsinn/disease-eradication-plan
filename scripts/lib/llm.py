#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM utility functions for Gemini and Claude APIs.
Python equivalent of scripts/lib/llm.ts
"""
import sys
import os
import json
import re

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

from google import genai
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)

# --- Model IDs ---
# Updated January 2026 - Gemini 3 models (preview)
GEMINI_PRO_MODEL_ID = "gemini-3-pro-preview"
GEMINI_FLASH_MODEL_ID = "gemini-3-flash-preview"
CLAUDE_OPUS_4_1_MODEL_ID = "claude-opus-4-1-20250805"
CLAUDE_SONNET_4_5_MODEL_ID = "claude-sonnet-4-5-20250929"

# --- Pricing metadata (USD per 1M tokens) ---
MODEL_PRICING_PER_1M_USD: dict[str, tuple[float, float]] = {
    # Source: https://ai.google.dev/gemini-api/docs/pricing (Gemini 3 Flash Preview, paid tier)
    GEMINI_FLASH_MODEL_ID: (0.50, 3.00),  # (input, output)
}

# --- API Setup ---
GOOGLE_GENERATIVE_AI_API_KEY = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Request timeout for Gemini client (milliseconds).
# google-genai HttpOptions.timeout is ms.
DEFAULT_LLM_REQUEST_TIMEOUT_MS = 180_000
try:
    LLM_REQUEST_TIMEOUT_MS = max(
        1_000,
        int(os.getenv("LLM_REQUEST_TIMEOUT_MS", str(DEFAULT_LLM_REQUEST_TIMEOUT_MS))),
    )
except ValueError:
    LLM_REQUEST_TIMEOUT_MS = DEFAULT_LLM_REQUEST_TIMEOUT_MS

# Initialize clients lazily based on available credentials.
# This avoids import-time failures when only one provider is needed.
google_client = None
if GOOGLE_GENERATIVE_AI_API_KEY:
    google_client = genai.Client(
        api_key=GOOGLE_GENERATIVE_AI_API_KEY,
        http_options=genai.types.HttpOptions(timeout=LLM_REQUEST_TIMEOUT_MS),
    )

anthropic_client = None
if ANTHROPIC_API_KEY:
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

_gemini_key_fingerprint_logged = False
_claude_key_fingerprint_logged = False


def _log_key_fingerprint_once(provider: str, key: str | None) -> None:
    """Log masked API key fingerprint once for runtime diagnostics."""
    global _gemini_key_fingerprint_logged, _claude_key_fingerprint_logged
    if provider == "gemini":
        if _gemini_key_fingerprint_logged:
            return
        _gemini_key_fingerprint_logged = True
    elif provider == "claude":
        if _claude_key_fingerprint_logged:
            return
        _claude_key_fingerprint_logged = True
    else:
        return

    if not key:
        print(f"[LLM] {provider} key fingerprint: <missing>")
        return

    tail_len = 6 if len(key) >= 6 else len(key)
    tail = key[-tail_len:]
    print(
        f"[LLM] {provider} key fingerprint: len={len(key)}, tail={tail}",
        flush=True,
    )


# --- Content Generation Functions ---

def generate_gemini_pro_content(prompt: str) -> str:
    """Generate content using Gemini Pro model."""
    if google_client is None:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is required for Gemini requests.")
    _log_key_fingerprint_once("gemini", GOOGLE_GENERATIVE_AI_API_KEY)
    response = google_client.models.generate_content(
        model=GEMINI_PRO_MODEL_ID,
        contents=prompt
    )
    return response.text or ""


def generate_gemini_flash_content(prompt: str) -> str:
    """Generate content using Gemini Flash model."""
    if google_client is None:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is required for Gemini requests.")
    _log_key_fingerprint_once("gemini", GOOGLE_GENERATIVE_AI_API_KEY)
    response = google_client.models.generate_content(
        model=GEMINI_FLASH_MODEL_ID,
        contents=prompt
    )
    return response.text or ""


def generate_gemini_flash_content_with_image(
    prompt: str,
    image_bytes: bytes,
    mime_type: str = "image/png",
) -> str:
    """Generate content using Gemini Flash model with image input."""
    if google_client is None:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is required for Gemini requests.")
    _log_key_fingerprint_once("gemini", GOOGLE_GENERATIVE_AI_API_KEY)
    response = google_client.models.generate_content(
        model=GEMINI_FLASH_MODEL_ID,
        contents=[
            prompt,
            genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
    )
    return response.text or ""


def generate_gemini_flash_content_with_pdf(
    prompt: str,
    pdf_path: str,
) -> str:
    """Generate content using Gemini Flash model with a full PDF input via Files API."""
    if google_client is None:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is required for Gemini requests.")
    _log_key_fingerprint_once("gemini", GOOGLE_GENERATIVE_AI_API_KEY)
    uploaded_file = google_client.files.upload(file=pdf_path)
    file_uri = getattr(uploaded_file, "uri", None)
    mime_type = getattr(uploaded_file, "mime_type", None) or "application/pdf"
    if not file_uri:
        raise ValueError("Gemini file upload succeeded but did not return a URI.")
    response = google_client.models.generate_content(
        model=GEMINI_FLASH_MODEL_ID,
        contents=[
            genai.types.Part.from_uri(file_uri=file_uri, mime_type=mime_type),
            prompt,
        ],
    )
    return response.text or ""


def generate_claude_opus_content(prompt: str) -> str:
    """Generate content using Claude Opus 4.1 model."""
    if anthropic_client is None:
        raise ValueError("ANTHROPIC_API_KEY is required for Claude requests.")
    _log_key_fingerprint_once("claude", ANTHROPIC_API_KEY)
    message = anthropic_client.messages.create(
        model=CLAUDE_OPUS_4_1_MODEL_ID,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    response_block = message.content[0]
    if response_block.type != "text":
        raise ValueError("Unexpected response format from Anthropic API. Expected a text block.")
    return response_block.text


def generate_claude_sonnet_content(prompt: str) -> str:
    """Generate content using Claude Sonnet 4.5 model."""
    if anthropic_client is None:
        raise ValueError("ANTHROPIC_API_KEY is required for Claude requests.")
    _log_key_fingerprint_once("claude", ANTHROPIC_API_KEY)
    message = anthropic_client.messages.create(
        model=CLAUDE_SONNET_4_5_MODEL_ID,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    response_block = message.content[0]
    if response_block.type != "text":
        raise ValueError("Unexpected response format from Anthropic API. Expected a text block.")
    return response_block.text


# --- Utility Functions ---

def estimate_tokens(text: str) -> float:
    """
    Rough token estimate from characters.
    Uses ~4 chars/token approximation for English text.
    """
    return max(1.0, len(text) / 4.0)


def get_cost_rates_per_1m(
    model_id: str,
    input_env_key: str = "PDF_VALIDATION_LLM_INPUT_COST_PER_1M",
    output_env_key: str = "PDF_VALIDATION_LLM_OUTPUT_COST_PER_1M",
) -> tuple[float, float, str]:
    """
    Resolve input/output cost rates for a model in USD per 1M tokens.

    Resolution order:
    1) Explicit env vars (both must be set and parseable)
    2) Built-in model defaults
    3) Zero fallback
    """
    try:
        env_input = os.environ.get(input_env_key)
        input_rate = float(env_input) if env_input is not None else None
    except ValueError:
        input_rate = None
    try:
        env_output = os.environ.get(output_env_key)
        output_rate = float(env_output) if env_output is not None else None
    except ValueError:
        output_rate = None

    if input_rate is not None and output_rate is not None:
        return max(0.0, input_rate), max(0.0, output_rate), "env"

    model_rates = MODEL_PRICING_PER_1M_USD.get(model_id)
    if model_rates is not None:
        return model_rates[0], model_rates[1], "model-default"

    return 0.0, 0.0, "unset"


def estimate_request_cost_usd(
    model_id: str,
    prompt_text: str,
    response_text: str,
    input_env_key: str = "PDF_VALIDATION_LLM_INPUT_COST_PER_1M",
    output_env_key: str = "PDF_VALIDATION_LLM_OUTPUT_COST_PER_1M",
) -> dict[str, float | str]:
    """
    Estimate per-request token usage and USD cost.
    """
    input_tokens_est = estimate_tokens(prompt_text)
    output_tokens_est = estimate_tokens(response_text)
    input_rate, output_rate, source = get_cost_rates_per_1m(
        model_id=model_id,
        input_env_key=input_env_key,
        output_env_key=output_env_key,
    )
    request_cost_est = (
        (input_tokens_est / 1_000_000.0) * input_rate
        + (output_tokens_est / 1_000_000.0) * output_rate
    )
    return {
        "input_tokens_est": input_tokens_est,
        "output_tokens_est": output_tokens_est,
        "input_rate_per_1m": input_rate,
        "output_rate_per_1m": output_rate,
        "pricing_source": source,
        "request_cost_est_usd": request_cost_est,
    }

def extract_json_from_response(response_text: str, context: str = "LLM response") -> dict:
    """
    Extracts JSON object from LLM response text, handling markdown code blocks.
    """
    # Try to find JSON object
    json_match = re.search(r'\{[\s\S]*\}', response_text)
    if not json_match:
        # Try to find JSON array
        json_match = re.search(r'\[[\s\S]*\]', response_text)

    if not json_match:
        raise ValueError(f"No JSON found in {context}. Response: {response_text[:500]}...")

    return json.loads(json_match.group(0))


def load_prompt_template(template_path: str, replacements: dict[str, str]) -> str:
    """
    Loads a prompt template and replaces placeholders.
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        prompt = f.read()

    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, value)

    return prompt


if __name__ == "__main__":
    # Quick test
    print("Testing LLM library...")
    response = generate_gemini_flash_content("Say 'Hello from Gemini!' in exactly those words.")
    print(f"Gemini Flash response: {response}")
