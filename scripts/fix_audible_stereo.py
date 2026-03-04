#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-off fix: normalize theme song + retail sample to ACX-compliant mono MP3s.

Fixes the Audible rejection: "uploaded audio files contain both mono and stereo files"
by normalizing the stereo theme song to mono and regenerating the retail sample.
"""
import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

sys.path.insert(0, str(Path(__file__).parent))

from lib.acx_utils import (
    normalize_to_acx_mp3, tag_mp3, print_acx_report,
    get_duration_secs, format_duration, DEFAULT_COVER,
    ACX_SAMPLE_RATE, ACX_BITRATE,
)

PROJECT_ROOT = Path(__file__).parent.parent
THEME_SRC = PROJECT_ROOT / "assets" / "music" / "podcast-theme-song.mp3"
AUDIBLE_DIR = PROJECT_ROOT / "assets" / "audiobook" / "manual-paperback" / "audible-export"
THEME_AUDIBLE = AUDIBLE_DIR / "podcast-theme-song-audible.mp3"
CHAPTER_1 = AUDIBLE_DIR / "01-index-manual.mp3"
SAMPLE_OUT = AUDIBLE_DIR / "retail-sample.mp3"

ALBUM = "How to End War and Disease"
ARTIST = "Mike P. Sinn"
YEAR = "2025"


def fix_theme_song():
    """Normalize theme song to ACX mono MP3."""
    print("\n=== Normalizing theme song ===")
    if not THEME_SRC.exists():
        print(f"  SKIP: {THEME_SRC} not found")
        return

    result = normalize_to_acx_mp3(THEME_SRC, THEME_AUDIBLE, target_rms=-20.0)
    print(f"  Normalized: RMS={result['output_rms']} dB, peak={result['output_peak']} dB, "
          f"duration={result['duration_fmt']}")

    tag_mp3(THEME_AUDIBLE, title="How to End War and Disease - Theme Song",
            album=ALBUM, artist=ARTIST, year=YEAR, cover_path=DEFAULT_COVER)
    print(f"  Tagged: {THEME_AUDIBLE.name}")
    print_acx_report(THEME_AUDIBLE)


def fix_retail_sample():
    """Regenerate retail sample from normalized mono theme + chapter 1."""
    print("\n=== Regenerating retail sample ===")
    if not CHAPTER_1.exists():
        print(f"  SKIP: {CHAPTER_1} not found")
        return

    # Use normalized theme if available, otherwise just chapter 1
    import subprocess
    inputs = []
    if THEME_AUDIBLE.exists():
        theme_dur = get_duration_secs(THEME_AUDIBLE)
        print(f"  Using normalized theme ({format_duration(theme_dur)})")
        inputs.append(THEME_AUDIBLE)
    elif THEME_SRC.exists():
        print("  WARNING: normalized theme not found, using source (will be stereo!)")
        inputs.append(THEME_SRC)

    inputs.append(CHAPTER_1)

    max_duration = 300.0
    fade_secs = 3.0

    input_args = []
    filter_inputs = []
    for i, path in enumerate(inputs):
        input_args += ["-i", str(path)]
        filter_inputs.append(f"[{i}:a]")

    concat_filter = f"{''.join(filter_inputs)}concat=n={len(inputs)}:v=0:a=1[joined]"
    trim_filter = (
        f"[joined]atrim=0:{max_duration},"
        f"afade=t=out:st={max_duration - fade_secs}:d={fade_secs}[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", f"{concat_filter};{trim_filter}",
        "-map", "[out]",
        "-ar", str(ACX_SAMPLE_RATE),
        "-ac", "1",
        "-b:a", f"{ACX_BITRATE}k",
        "-c:a", "libmp3lame",
        str(SAMPLE_OUT),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[-500:]}")
        return

    tag_mp3(SAMPLE_OUT, title="How to End War and Disease - Retail Sample",
            album=ALBUM, artist=ARTIST, year=YEAR, cover_path=DEFAULT_COVER)

    sample_dur = get_duration_secs(SAMPLE_OUT)
    print(f"  Generated: {SAMPLE_OUT.name} ({format_duration(sample_dur)})")
    print_acx_report(SAMPLE_OUT)


def main():
    fix_theme_song()
    fix_retail_sample()
    print("\n=== Done ===")
    print(f"  Theme:  {THEME_AUDIBLE}")
    print(f"  Sample: {SAMPLE_OUT}")
    print(f"\nUpload these to Audible as INTRO and SAMPLE respectively.")


if __name__ == "__main__":
    main()
