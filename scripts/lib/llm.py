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

load_dotenv()

# --- Model IDs ---
# Updated January 2026 - Gemini 3 models (preview)
GEMINI_PRO_MODEL_ID = "gemini-3-pro-preview"
GEMINI_FLASH_MODEL_ID = "gemini-3-flash-preview"
CLAUDE_OPUS_4_1_MODEL_ID = "claude-opus-4-1-20250805"
CLAUDE_SONNET_4_5_MODEL_ID = "claude-sonnet-4-5-20250929"

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


# --- Content Generation Functions ---

def generate_gemini_pro_content(prompt: str) -> str:
    """Generate content using Gemini Pro model."""
    if google_client is None:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is required for Gemini requests.")
    response = google_client.models.generate_content(
        model=GEMINI_PRO_MODEL_ID,
        contents=prompt
    )
    return response.text or ""


def generate_gemini_flash_content(prompt: str) -> str:
    """Generate content using Gemini Flash model."""
    if google_client is None:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is required for Gemini requests.")
    response = google_client.models.generate_content(
        model=GEMINI_FLASH_MODEL_ID,
        contents=prompt
    )
    return response.text or ""


def generate_claude_opus_content(prompt: str) -> str:
    """Generate content using Claude Opus 4.1 model."""
    if anthropic_client is None:
        raise ValueError("ANTHROPIC_API_KEY is required for Claude requests.")
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
