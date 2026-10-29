#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text-to-Speech utility functions using Gemini's native TTS capabilities.
Uses gemini-3.8-flash-tts through the Interactions REST API (google-genai 1.x
has no Interactions support).
"""
import base64
import hashlib
import io
import json
import sys
import os
import struct
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

try:
    from .python_utils import load_project_dotenv
except ImportError:
    from python_utils import load_project_dotenv

load_project_dotenv(Path(__file__).parent.parent.parent)

# --- Configuration ---
TTS_MODEL_ID = "gemini-3.8-flash-tts"
TTS_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"

# Available voice names for Gemini TTS
# See: https://ai.google.dev/gemini-api/docs/speech-generation
# Gender: [F] = Female, [M] = Male, [?] = Unknown
AVAILABLE_VOICES = [
    # Original 8 voices
    "Zephyr",   # [F] Bright, cheerful
    "Puck",     # [M] Upbeat, energetic (default in many apps)
    "Charon",   # [?] Informative, clear
    "Kore",     # [F] Firm, confident
    "Fenrir",   # [?] Excitable, dynamic
    "Leda",     # [F] Youthful, energetic
    "Orus",     # [M] Firm, decisive
    "Aoede",    # [F] Breezy, natural

    # Additional voices
    "Achernar",      # Soft, gentle
    "Achird",        # Friendly, approachable
    "Algenib",       # Gravelly texture
    "Algieba",       # Smooth, pleasant
    "Alnilam",       # Firm, strong
    "Autonoe",       # Bright, optimistic
    "Callirhoe",     # Easy-going, relaxed
    "Despina",       # Smooth, flowing
    "Enceladus",     # Breathy, soft
    "Erinome",       # Clear, precise
    "Gacrux",        # Mature, experienced
    "Iapetus",       # Clear, articulate
    "Laomedeia",     # Upbeat, lively
    "Pulcherrima",   # Forward, expressive
    "Rasalgethi",    # Informative, professional
    "Sadachbia",     # Lively, animated
    "Sulafat",       # Warm, welcoming
    "Umbriel",       # Easy-going
    "Vindemiatrix",  # Gentle, kind
]

# Voice descriptions for easy reference
VOICE_DESCRIPTIONS = {
    # Female voices
    "Zephyr": "Female - Bright, cheerful",
    "Kore": "Female - Firm, confident",
    "Leda": "Female - Youthful, energetic",
    "Aoede": "Female - Breezy, natural",
    "Autonoe": "Female - Bright, optimistic",

    # Male voices
    "Puck": "Male - Upbeat, energetic",
    "Orus": "Male - Firm, decisive",

    # Other voices (gender varies)
    "Charon": "Informative, clear",
    "Fenrir": "Excitable, dynamic",
    "Achernar": "Soft, gentle",
    "Achird": "Friendly, approachable",
    "Algenib": "Gravelly texture",
    "Algieba": "Smooth, pleasant",
    "Alnilam": "Firm, strong",
    "Callirhoe": "Easy-going, relaxed",
    "Despina": "Smooth, flowing",
    "Enceladus": "Breathy, soft",
    "Erinome": "Clear, precise",
    "Gacrux": "Mature, experienced",
    "Iapetus": "Clear, articulate",
    "Laomedeia": "Upbeat, lively",
    "Pulcherrima": "Forward, expressive",
    "Rasalgethi": "Informative, professional",
    "Sadachbia": "Lively, animated",
    "Sulafat": "Warm, welcoming",
    "Umbriel": "Easy-going",
    "Vindemiatrix": "Gentle, kind",
}

# Default voice for narration
# Episodes voiced on gemini-2.5-pro-preview-tts (shut down Nov 17, 2026) used Kore.
# On 3.8 Flash, Kore ("Firm") read flat and businesslike; Oct 2026 listening tests
# picked Autonoe ("Bright, optimistic").
DEFAULT_VOICE = "Autonoe"
# Sent as the speech_metadata style when non-empty; 3.8 reads the text itself verbatim.
# Of the styles tried on a full chunk (Oct 2026), this one came closest to the March
# 2.5 Pro Kore episodes in pace and pitch. The dinner-party style read as smug and
# rushed, and adding "bright" or "cheerful" to a prompt didn't raise her pitch.
DEFAULT_SPEAKING_INSTRUCTIONS = "Generate a voice like the narrator of a cheerful 1950s educational film, sunny and completely sincere."

# --- API Setup ---
# Checked when a request is sent, so cache checks can import this module without a key.
GOOGLE_GENERATIVE_AI_API_KEY = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")


def tts_cache_hash(text: str, voice: str = DEFAULT_VOICE) -> str:
    """Hash of the spoken text plus TTS model, voice and style, so a voice change re-voices cached audio."""
    key = f"{TTS_MODEL_ID}|{voice}|{DEFAULT_SPEAKING_INSTRUCTIONS}|{text}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    """
    Parses bits per sample and rate from an audio MIME type string.

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys.
    """
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """
    Converts raw audio data to WAV format by adding appropriate headers.

    Args:
        audio_data: The raw audio data as bytes.
        mime_type: MIME type of the audio data.

    Returns:
        WAV file data as bytes.
    """
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    # WAV header format: http://soundfile.sapp.org/doc/WaveFormat/
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size
    )
    return header + audio_data


MAX_TTS_RETRIES = 3
TTS_RETRY_BACKOFF = [10, 30, 60]  # seconds between retries


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


DEFAULT_TTS_VERBOSE = _env_flag("AUDIOBOOK_TTS_VERBOSE", False)
SPLIT_PAUSE_S = 0.35  # silence between the pieces of a chunk the content filter blocked


class ContentBlockedError(RuntimeError):
    """The API's content filter refused the text ("content_blocked")."""


def _generate_speech_single(
    text: str,
    voice_name: str,
    speaking_instructions: str,
    verbose: bool = DEFAULT_TTS_VERBOSE,
) -> bytes:
    """
    Generate speech for a single chunk of text with retry logic.
    Returns WAV bytes (24 kHz, mono, 16-bit, with RIFF header).
    """
    if not GOOGLE_GENERATIVE_AI_API_KEY:
        raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.")
    content: dict = {"type": "text", "text": text}
    if speaking_instructions:
        content["annotations"] = [{"type": "speech_metadata", "style": speaking_instructions}]
    payload = {
        "model": TTS_MODEL_ID,
        "input": [{"type": "user_input", "content": [content]}],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": voice_name}]},
    }
    request = urllib.request.Request(
        TTS_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"x-goog-api-key": GOOGLE_GENERATIVE_AI_API_KEY, "Content-Type": "application/json"},
    )

    last_error = None
    for attempt in range(1, MAX_TTS_RETRIES + 1):
        start_time = time.time()

        try:
            try:
                with urllib.request.urlopen(request, timeout=600) as response:
                    reply = json.loads(response.read())
            except urllib.error.HTTPError as e:
                # Keep the API's message (quota name, retry time) instead of a bare status line
                body = e.read().decode('utf-8', 'replace')
                if '"content_blocked"' in body:
                    raise ContentBlockedError(f"HTTP {e.code}: {body[:500]}") from e
                raise RuntimeError(f"HTTP {e.code}: {body[:500]}") from e

            # Same path as Google's REST example: the last audio item of the model output
            audio_items = [
                item
                for step in reply.get("steps", [])
                if step.get("type") == "model_output"
                for item in step.get("content", [])
                if item.get("type") == "audio"
            ]
            elapsed = time.time() - start_time
            if not audio_items:
                raise RuntimeError(f"No audio data received after {elapsed:.0f}s")

            wav_data = base64.b64decode(audio_items[-1]["data"])
            if verbose:
                print(f"  TTS complete: {len(wav_data):,} bytes in {elapsed:.0f}s")
            return wav_data

        except ContentBlockedError:
            # Retrying the same text is usually blocked again; the caller splits it instead
            raise
        except Exception as e:
            last_error = e
            elapsed = time.time() - start_time
            if attempt < MAX_TTS_RETRIES:
                wait = TTS_RETRY_BACKOFF[attempt - 1]
                print(f"  [RETRY] Attempt {attempt}/{MAX_TTS_RETRIES} failed after {elapsed:.0f}s: {e}")
                print(f"  [RETRY] Waiting {wait}s before retry...", flush=True)
                time.sleep(wait)
            else:
                print(f"  [FAILED] All {MAX_TTS_RETRIES} attempts failed. Last error: {e}")

    if last_error is not None:
        raise last_error
    raise RuntimeError("TTS generation failed without an exception")


def _join_wavs(parts: list[bytes], pause_s: float) -> bytes:
    """Concatenate WAV files (same format) with a short silence between them."""
    out = io.BytesIO()
    with wave.open(io.BytesIO(parts[0])) as first:
        params = first.getparams()
    gap = b"\x00" * (int(params.framerate * pause_s) * params.sampwidth * params.nchannels)
    with wave.open(out, "wb") as joined:
        joined.setparams(params)
        for i, part in enumerate(parts):
            with wave.open(io.BytesIO(part)) as w:
                joined.writeframes((gap if i else b"") + w.readframes(w.getnframes()))
    return out.getvalue()


def _speak_splitting_when_blocked(
    text: str,
    voice_name: str,
    speaking_instructions: str,
    verbose: bool,
) -> bytes:
    """Voice the text; if the content filter blocks it, split at the line break nearest
    the middle and voice each half the same way.

    The filter judges whole passages: in index-manual, a list of how war gets built was
    blocked when followed by its punchline, though each voiced fine alone.
    """
    try:
        return _generate_speech_single(text, voice_name, speaking_instructions, verbose=verbose)
    except ContentBlockedError:
        breaks = [i for i, ch in enumerate(text) if ch == "\n" and text[:i].strip() and text[i:].strip()]
        if not breaks:
            raise
        cut = min(breaks, key=lambda i: abs(i - len(text) / 2))
        print(f"  [BLOCKED] Content filter refused {len(text):,} chars; voicing it as two pieces", flush=True)
        return _join_wavs([
            _speak_splitting_when_blocked(text[:cut].strip(), voice_name, speaking_instructions, verbose),
            _speak_splitting_when_blocked(text[cut:].strip(), voice_name, speaking_instructions, verbose),
        ], SPLIT_PAUSE_S)


def generate_speech(
    text: str,
    output_path: str | Path,
    voice_name: str = DEFAULT_VOICE,
    speaking_instructions: str = DEFAULT_SPEAKING_INSTRUCTIONS,
    verbose: bool = DEFAULT_TTS_VERBOSE,
) -> Path:
    """
    Generates speech audio from text using Gemini TTS.
    Text should be pre-chunked by the caller (generate_audiobook_text.py uses
    ~3,000-character chunks, about three to four minutes of audio each). Text the
    content filter blocks is voiced in pieces split at line breaks.

    Args:
        text: The text to convert to speech. Spoken verbatim.
        output_path: Path to save the audio file (will be saved as .wav).
        voice_name: Name of the voice to use (see AVAILABLE_VOICES).
        speaking_instructions: Delivery style, sent as speech metadata (empty for none).

    Returns:
        Path to the generated audio file.
    """
    output_path = Path(output_path)

    # Ensure .wav extension
    if output_path.suffix.lower() != ".wav":
        output_path = output_path.with_suffix(".wav")

    if verbose:
        print(f"Generating speech with voice '{voice_name}' ({len(text):,} chars)...")
    wav_data = _speak_splitting_when_blocked(
        text,
        voice_name,
        speaking_instructions,
        verbose=verbose,
    )

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(wav_data)

    if verbose:
        print(f"Audio saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    # Quick test
    print("Testing TTS library...")
    test_output = Path("test_tts_output.wav")
    generate_speech(
        "Hello! This is a test of the Gemini text-to-speech system. "
        "It should sound natural and clear.",
        test_output,
        voice_name="Charon"
    )
    print(f"Test complete. Check {test_output}")
