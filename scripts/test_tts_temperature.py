#!/usr/bin/env python3
"""Test TTS with different temperatures and speaking instructions.

Generates ch1 chunk1 with various settings for A/B comparison.
Output: assets/audiobook/test-temperature/
"""
import sys
import os
import time

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pathlib import Path
from lib.python_utils import load_project_dotenv

load_project_dotenv(Path(__file__).parent.parent)

from google import genai
from google.genai import types
from lib.tts import convert_to_wav, TTS_MODEL_ID, DEFAULT_SPEAKING_INSTRUCTIONS

client = genai.Client(api_key=os.getenv('GOOGLE_GENERATIVE_AI_API_KEY'))

PROJECT_ROOT = Path(__file__).parent.parent
CHUNK_PATH = PROJECT_ROOT / "assets/audiobook/manual-paperback/narration-txt-chunks/index-manual.prepared/chunk-01-of-13.txt"
OUTDIR = PROJECT_ROOT / "assets/audiobook/test-temperature"
OUTDIR.mkdir(exist_ok=True)

MAX_RETRIES = 3
RETRY_WAIT = [10, 30, 60]


def generate_test(text: str, voice: str, speaking: str, temperature: float, label: str):
    out = OUTDIR / f"{label}.wav"
    if out.exists():
        print(f"\n[SKIP] {label} (already exists)")
        return

    print(f"\n[GEN] {label} (temp={temperature})...")
    config = types.GenerateContentConfig(
        temperature=temperature,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
            ),
        ),
    )
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=f"{speaking}\n\n{text}")])]

    for attempt in range(1, MAX_RETRIES + 1):
        audio_chunks = []
        mime_type = None
        t0 = time.time()
        try:
            for chunk in client.models.generate_content_stream(
                model=TTS_MODEL_ID, contents=contents, config=config,  # pyright: ignore[reportArgumentType]
            ):
                if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                    part = chunk.candidates[0].content.parts[0]
                    if part.inline_data and part.inline_data.data:
                        audio_chunks.append(part.inline_data.data)
                        if not mime_type:
                            mime_type = part.inline_data.mime_type
                        total = sum(len(c) for c in audio_chunks)
                        elapsed = time.time() - t0
                        print(f"  streaming: {total:,} bytes ({elapsed:.0f}s)", flush=True)

            if audio_chunks:
                raw = b"".join(audio_chunks)
                wav = convert_to_wav(raw, mime_type or "audio/L16;rate=24000")
                out.write_bytes(wav)
                elapsed = time.time() - t0
                print(f"  [OK] {out.name} ({len(raw):,} bytes, {elapsed:.0f}s)")
                return
            else:
                raise RuntimeError("No audio data returned")

        except Exception as e:
            elapsed = time.time() - t0
            if attempt < MAX_RETRIES:
                wait = RETRY_WAIT[attempt - 1]
                print(f"  [RETRY {attempt}/{MAX_RETRIES}] Failed after {elapsed:.0f}s: {e}")
                print(f"  Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  [FAILED] {label}: {e}")


def main():
    text = CHUNK_PATH.read_text(encoding="utf-8")
    print(f"Chunk: {len(text)} chars from {CHUNK_PATH.name}")

    current = DEFAULT_SPEAKING_INSTRUCTIONS

    enhanced = (
        "You are narrating an audiobook written by a naive alien observing Earth. "
        "Read with dry wit and comic timing. Pause slightly before punchlines. "
        "Deliver absurd observations deadpan, as if they are perfectly reasonable conclusions. "
        "Warm, engaging, slightly amused. Like a favorite teacher telling a funny story. "
        "Never robotic or monotone. Vary your pitch and pace naturally."
    )

    tests = [
        ("Kore", current, 0.5, "ch1-temp0.5-current"),
        ("Kore", current, 1.0, "ch1-temp1.0-current"),
        ("Kore", enhanced, 1.0, "ch1-temp1.0-enhanced"),
        ("Kore", enhanced, 0.7, "ch1-temp0.7-enhanced"),
    ]

    for voice, speaking, temp, label in tests:
        generate_test(text, voice, speaking, temp, label)
        time.sleep(3)

    print(f"\nDone! Compare files in {OUTDIR.relative_to(PROJECT_ROOT)}/")


if __name__ == "__main__":
    main()
