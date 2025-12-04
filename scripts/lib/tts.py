#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text-to-Speech utility functions using Gemini's native TTS capabilities.
Uses the gemini-2.5-pro-preview-tts model for high-quality speech synthesis.
"""
import sys
import os
import struct
import mimetypes
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
TTS_MODEL_ID = "gemini-2.5-pro-preview-tts"

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
DEFAULT_VOICE = "Aoede"

# Default speaking style - Philomena Cunk-inspired: innocent, childlike, warm
DEFAULT_SPEAKING_INSTRUCTIONS = "British accent. Innocent, childlike delivery. Read like a curious child presenting a school report. No judgment, matter-of-fact. Warm and friendly tone."

# --- API Setup ---
GOOGLE_API_KEY = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is not set in the .env file.")

# Initialize client
google_client = genai.Client(api_key=GOOGLE_API_KEY)


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


def generate_speech(
    text: str,
    output_path: str | Path,
    voice_name: str = DEFAULT_VOICE,
    speaking_instructions: str = DEFAULT_SPEAKING_INSTRUCTIONS
) -> Path:
    """
    Generates speech audio from text using Gemini TTS.

    Args:
        text: The text to convert to speech.
        output_path: Path to save the audio file (will be saved as .wav).
        voice_name: Name of the voice to use (see AVAILABLE_VOICES).
        speaking_instructions: Instructions for how to read the text.

    Returns:
        Path to the generated audio file.
    """
    output_path = Path(output_path)

    # Ensure .wav extension
    if output_path.suffix.lower() != ".wav":
        output_path = output_path.with_suffix(".wav")

    # Prepare the prompt with speaking instructions
    prompt_text = f"{speaking_instructions}\n\n{text}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            ),
        ),
    )

    print(f"Generating speech with voice '{voice_name}'...")

    # Collect all audio chunks
    audio_chunks = []
    mime_type = None

    for chunk in google_client.models.generate_content_stream(
        model=TTS_MODEL_ID,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        part = chunk.candidates[0].content.parts[0]
        if part.inline_data and part.inline_data.data:
            audio_chunks.append(part.inline_data.data)
            if mime_type is None:
                mime_type = part.inline_data.mime_type

    if not audio_chunks:
        raise RuntimeError("No audio data received from TTS API")

    # Combine all chunks
    combined_audio = b"".join(audio_chunks)

    # Convert to WAV format
    if mime_type:
        wav_data = convert_to_wav(combined_audio, mime_type)
    else:
        # Assume default parameters if mime_type is missing
        wav_data = convert_to_wav(combined_audio, "audio/L16;rate=24000")

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(wav_data)

    print(f"Audio saved to: {output_path}")
    return output_path


def generate_speech_multi_speaker(
    script: list[dict[str, str]],
    output_path: str | Path,
    speaker_voices: dict[str, str] | None = None,
    speaking_instructions: str = "Read in a natural, conversational tone"
) -> Path:
    """
    Generates multi-speaker speech audio from a script.

    Args:
        script: List of dicts with 'speaker' and 'text' keys.
                Example: [{"speaker": "Speaker 1", "text": "Hello!"}, ...]
        output_path: Path to save the audio file.
        speaker_voices: Dict mapping speaker names to voice names.
                       Example: {"Speaker 1": "Zephyr", "Speaker 2": "Puck"}
        speaking_instructions: Instructions for how to read the script.

    Returns:
        Path to the generated audio file.
    """
    output_path = Path(output_path)

    if output_path.suffix.lower() != ".wav":
        output_path = output_path.with_suffix(".wav")

    # Get unique speakers from script
    speakers = list(set(item["speaker"] for item in script))

    # Assign default voices if not provided
    if speaker_voices is None:
        speaker_voices = {}

    for i, speaker in enumerate(speakers):
        if speaker not in speaker_voices:
            speaker_voices[speaker] = AVAILABLE_VOICES[i % len(AVAILABLE_VOICES)]

    # Format script as text with speaker labels
    script_text = "\n".join(
        f"{item['speaker']}: {item['text']}" for item in script
    )
    prompt_text = f"{speaking_instructions}\n\n{script_text}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)],
        ),
    ]

    # Build speaker voice configs
    speaker_voice_configs = [
        types.SpeakerVoiceConfig(
            speaker=speaker,
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            ),
        )
        for speaker, voice_name in speaker_voices.items()
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=speaker_voice_configs
            ),
        ),
    )

    print(f"Generating multi-speaker speech...")
    print(f"Speakers: {speaker_voices}")

    audio_chunks = []
    mime_type = None

    for chunk in google_client.models.generate_content_stream(
        model=TTS_MODEL_ID,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        part = chunk.candidates[0].content.parts[0]
        if part.inline_data and part.inline_data.data:
            audio_chunks.append(part.inline_data.data)
            if mime_type is None:
                mime_type = part.inline_data.mime_type

    if not audio_chunks:
        raise RuntimeError("No audio data received from TTS API")

    combined_audio = b"".join(audio_chunks)

    if mime_type:
        wav_data = convert_to_wav(combined_audio, mime_type)
    else:
        wav_data = convert_to_wav(combined_audio, "audio/L16;rate=24000")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(wav_data)

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
