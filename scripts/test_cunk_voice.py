#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Philomena Cunk-style voice with Gemini TTS.
Bemused British lady explaining obvious things to confused humans.
"""
import sys
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add scripts directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))
from lib.tts import generate_speech

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "audiobook" / "voice-previews"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Test with all female voices
VOICES = ["Aoede", 
#"Kore", 
#"Zephyr",
 #"Leda", 
 #"Autonoe"
 ]

# Sample text in the book's style
SAMPLE_TEXT = """You spend forty times more on killing people than curing them. I checked the math. It's correct."""

# Refined prompts - variations on the childlike documentary narrator
STYLES = {
    "base": "British accent. Innocent, childlike delivery. Read like a curious child presenting a school report about something confusing. No judgment, just stated matter-of-factly.",
    "faster": "British accent. Innocent, childlike delivery. Read like a curious child presenting a school report. No judgment, matter-of-fact. Slightly faster pace, keep it moving.",
    "warmer": "British accent. Innocent, childlike delivery. Read like a curious child presenting a school report. No judgment, matter-of-fact. Warm and friendly tone.",
    "drier": "British accent. Innocent, childlike delivery. Read like a curious child presenting a school report. No judgment, matter-of-fact. Very dry, almost deadpan.",
    "lighter": "British accent. Innocent, childlike delivery. Read like a curious child presenting a school report. No judgment, matter-of-fact. Light and airy, slight smile in voice.",
    "calmer": "British accent. Innocent, childlike delivery. Read like a curious child presenting a school report. No judgment, matter-of-fact. Calm, relaxed, unhurried but not slow.",
}

def main():
    print(f"Testing all style/voice combinations...")
    print(f"Voices: {VOICES}")
    print(f"Styles: {list(STYLES.keys())}")
    print(f"Total: {len(VOICES) * len(STYLES)} combinations")
    print(f"Output: {OUTPUT_DIR}\n")

    for voice in VOICES:
        for style_name, instruction in STYLES.items():
            print(f"Generating {voice} + {style_name}...")
            output_path = OUTPUT_DIR / f"{style_name}-{voice.lower()}.wav"

            try:
                generate_speech(
                    text=SAMPLE_TEXT,
                    output_path=output_path,
                    voice_name=voice,
                    speaking_instructions=instruction
                )
                print(f"  [OK] {output_path.name}\n")
            except Exception as e:
                print(f"  [ERROR] {e}\n")

    print("Done! Compare all combinations.")


if __name__ == "__main__":
    main()
