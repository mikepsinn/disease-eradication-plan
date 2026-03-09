#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run audiobook forced alignment for a single chapter in an isolated process.

This keeps native stable-ts / Whisper failures from taking down the parent
audio generation pipeline.
"""
import argparse
import sys
from pathlib import Path


if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # pyright: ignore[reportAttributeAccessIssue]
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")  # pyright: ignore[reportAttributeAccessIssue]


SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from lib.alignment import align_chapter, generate_srt, generate_vtt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run isolated audiobook alignment for one chapter")
    parser.add_argument("--wav", required=True, help="Path to chapter WAV file")
    parser.add_argument("--text", required=True, help="Path to prepared narration text file")
    parser.add_argument("--alignment-output", required=True, help="Path to alignment JSON output")
    parser.add_argument("--vtt-output", required=True, help="Path to VTT subtitle output")
    parser.add_argument("--srt-output", required=True, help="Path to SRT subtitle output")
    parser.add_argument("--chapter-index", type=int, required=True, help="Chapter index")
    parser.add_argument("--chapter-title", default="", help="Chapter title")
    parser.add_argument("--model-name", default="base", help="stable-ts model name")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    chapter = {
        "index": args.chapter_index,
        "title": args.chapter_title,
    }

    wav_path = Path(args.wav)
    text_path = Path(args.text)
    alignment_output = Path(args.alignment_output)
    vtt_output = Path(args.vtt_output)
    srt_output = Path(args.srt_output)

    words = align_chapter(
        wav_path=wav_path,
        text_path=text_path,
        output_path=alignment_output,
        model_name=args.model_name,
        chapter=chapter,
    )
    generate_vtt(words, vtt_output)
    generate_srt(words, srt_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
