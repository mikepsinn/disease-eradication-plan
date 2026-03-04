#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audible/ACX Export

Converts chapter WAVs to Audible-compliant MP3s and generates upload instructions.

ACX Requirements:
  - MP3, CBR 192 kbps, 44.1 kHz, mono
  - RMS: -23 dB to -18 dB
  - Peak: -3 dB max
  - Noise floor: -60 dB or lower
  - ID3 tags: track number, title, album, artist, album artist, year

Usage:
    python scripts/generate_audible_export.py                    # Export all chapters
    python scripts/generate_audible_export.py --force            # Re-export even if cached
    python scripts/generate_audible_export.py --target-rms -20   # Custom RMS target
    python scripts/generate_audible_export.py --config _quarto-manual-paperback.yml
"""
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.audiobook_common import (
    PROJECT_ROOT, extract_chapters, config_name_from_path,
    get_paths, extract_title_from_qmd, chapter_slug,
)
from dih_models.yaml_utils import load_quarto_config

# ACX spec constants
ACX_SAMPLE_RATE = 44100
ACX_BITRATE = 192  # kbps, CBR
ACX_RMS_MIN = -23.0
ACX_RMS_MAX = -18.0
ACX_PEAK_MAX = -3.0


def get_rms(file_path: Path) -> float | None:
    """Measure RMS level of an audio file using ffmpeg astats.

    Uses reset=0 so stats accumulate over the whole file.
    The LAST line is the correct overall value.
    """
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(file_path),
            "-af", "astats=metadata=1:reset=0,ametadata=print:key=lavfi.astats.Overall.RMS_level",
            "-f", "null", "/dev/null",
        ],
        capture_output=True, text=True,
    )
    last_val = None
    for line in result.stderr.splitlines():
        if "lavfi.astats.Overall.RMS_level=" in line:
            val = line.split("=")[-1].strip()
            if val != "-inf":
                last_val = float(val)
    return last_val


def get_peak(file_path: Path) -> float | None:
    """Measure peak level of an audio file using ffmpeg astats.

    Uses reset=0 so stats accumulate over the whole file.
    The LAST line is the correct overall value.
    """
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(file_path),
            "-af", "astats=metadata=1:reset=0,ametadata=print:key=lavfi.astats.Overall.Peak_level",
            "-f", "null", "/dev/null",
        ],
        capture_output=True, text=True,
    )
    last_val = None
    for line in result.stderr.splitlines():
        if "lavfi.astats.Overall.Peak_level=" in line:
            val = line.split("=")[-1].strip()
            if val != "-inf":
                last_val = float(val)
    return last_val


def get_duration_secs(file_path: Path) -> float:
    """Get duration in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(file_path)],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def format_duration(secs: float) -> str:
    """Format seconds as HH:MM:SS."""
    h, rem = divmod(int(secs), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _loudnorm_measure(wav_path: Path) -> dict:
    """Pass 1: measure loudness stats with ffmpeg loudnorm in print mode."""
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(wav_path),
            "-af", "loudnorm=print_format=json",
            "-f", "null", "/dev/null",
        ],
        capture_output=True, text=True,
    )
    # Parse the JSON block from stderr
    stderr = result.stderr
    json_start = stderr.rfind("{")
    json_end = stderr.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        raise RuntimeError(f"Could not parse loudnorm stats from {wav_path.name}")
    import json as _json
    return _json.loads(stderr[json_start:json_end])


def convert_to_audible_mp3(
    wav_path: Path,
    mp3_path: Path,
    target_rms: float,
    track_num: int,
    track_total: int,
    title: str,
    album: str,
    artist: str,
    year: str,
) -> dict:
    """Convert a WAV to ACX-compliant MP3 with two-pass loudnorm normalization.

    Pass 1: Measure integrated loudness, true peak, LRA via loudnorm
    Pass 2: Apply loudnorm in linear mode with measured values, then encode

    ACX wants RMS between -23 and -18 dB, peak <= -3 dB.
    We target an integrated loudness (LUFS) that maps to the desired RMS range.
    For speech, LUFS ~ RMS, so we use target_rms as the LUFS target.
    """
    # Pass 1: measure
    stats = _loudnorm_measure(wav_path)
    source_i = float(stats["input_i"])
    source_tp = float(stats["input_tp"])
    source_lra = float(stats["input_lra"])
    source_thresh = float(stats["input_thresh"])

    # Pass 2: apply loudnorm with measured values (linear mode for better quality)
    # Target: integrated loudness = target_rms LUFS, true peak = -3 dB
    af = (
        f"loudnorm=I={target_rms}:TP={ACX_PEAK_MAX}:LRA=11"
        f":measured_I={source_i}:measured_TP={source_tp}"
        f":measured_LRA={source_lra}:measured_thresh={source_thresh}"
        f":linear=true:print_format=summary"
    )

    mp3_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-af", af,
        "-ar", str(ACX_SAMPLE_RATE),
        "-ac", "1",  # mono
        "-b:a", f"{ACX_BITRATE}k",
        "-c:a", "libmp3lame",
        "-map", "0:a",
        str(mp3_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed for {wav_path.name}:\n{result.stderr[-500:]}")

    # Tag with ID3 using mutagen
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, TDRC, TCON

    audio = MP3(str(mp3_path))
    if audio.tags is None:
        audio.add_tags()
    tags = audio.tags
    tags.add(TIT2(encoding=3, text=[title]))
    tags.add(TALB(encoding=3, text=[album]))
    tags.add(TPE1(encoding=3, text=[artist]))
    tags.add(TPE2(encoding=3, text=[artist]))
    tags.add(TRCK(encoding=3, text=[f"{track_num}/{track_total}"]))
    tags.add(TDRC(encoding=3, text=[year]))
    tags.add(TCON(encoding=3, text=["Audiobook"]))
    audio.save()

    # Measure output
    out_rms = get_rms(mp3_path)
    out_peak = get_peak(mp3_path)
    duration = get_duration_secs(mp3_path)

    return {
        "source_rms": round(source_i, 2),
        "volume_adj": round(target_rms - source_i, 2),
        "output_rms": round(out_rms, 2) if out_rms else None,
        "output_peak": round(out_peak, 2) if out_peak else None,
        "duration_secs": round(duration, 1),
        "duration_fmt": format_duration(duration),
    }


def generate_retail_sample(
    output_dir: Path,
    chapters: list[dict],
    max_duration_secs: float = 300.0,
) -> Path | None:
    """Generate a retail audio sample from the beginning of chapter 1.

    Audible requires a sample of 5 minutes or less, starting from the beginning
    of the audiobook for a seamless transition into the full audiobook.

    Takes the already-exported chapter 1 MP3 and trims it.
    """
    if not chapters:
        print("  SKIP retail sample: no chapters")
        return None

    first_ch = chapters[0]
    slug = chapter_slug(first_ch)
    source_mp3 = output_dir / f"{first_ch['index']:02d}-{slug}.mp3"

    if not source_mp3.exists():
        print(f"  SKIP retail sample: {source_mp3.name} not found")
        return None

    sample_path = output_dir / "retail-sample.mp3"

    # Check source duration to decide if trimming is needed
    source_dur = get_duration_secs(source_mp3)
    if source_dur <= max_duration_secs:
        # Chapter 1 is short enough to use as-is (unlikely but handle it)
        import shutil
        shutil.copy2(source_mp3, sample_path)
        print(f"  Retail sample: {sample_path.name} (full chapter 1, {format_duration(source_dur)})")
        return sample_path

    # Trim to max_duration_secs with a short fade-out at the end
    fade_secs = 3.0
    cmd = [
        "ffmpeg", "-y",
        "-i", str(source_mp3),
        "-t", str(max_duration_secs),
        "-af", f"afade=t=out:st={max_duration_secs - fade_secs}:d={fade_secs}",
        "-c:a", "libmp3lame",
        "-b:a", f"{ACX_BITRATE}k",
        "-ar", str(ACX_SAMPLE_RATE),
        "-ac", "1",
        str(sample_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED retail sample: {result.stderr[-300:]}")
        return None

    sample_dur = get_duration_secs(sample_path)
    print(f"  Retail sample: {sample_path.name} ({format_duration(sample_dur)}, "
          f"first {int(max_duration_secs)}s of chapter 1 with fade-out)")
    return sample_path


def generate_upload_instructions(
    chapters: list[dict],
    results: list[dict],
    output_dir: Path,
    album: str,
    artist: str,
    instructions_path: Path,
) -> None:
    """Generate a markdown file with Audible upload instructions."""
    total_secs = sum(r["duration_secs"] for r in results)

    lines = [
        f"# Audible/ACX Upload Instructions",
        f"",
        f"**Book:** {album}",
        f"**Author/Narrator:** {artist}",
        f"**Total Duration:** {format_duration(total_secs)}",
        f"**Chapters:** {len(chapters)}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"## Audio Specifications",
        f"",
        f"| Spec | Value |",
        f"|------|-------|",
        f"| Format | MP3 |",
        f"| Bit Rate | {ACX_BITRATE} kbps CBR |",
        f"| Sample Rate | {ACX_SAMPLE_RATE / 1000:.1f} kHz |",
        f"| Channels | Mono |",
        f"| RMS Target | -23 to -18 dB |",
        f"| Peak Limit | -3 dB |",
        f"| ID3 Tags | Track #, Title, Album, Artist, Year, Genre |",
        f"",
        f"## File Upload Order",
        f"",
        f"Upload these files **in order**:",
        f"",
        f"| # | File Path | Chapter Title | Duration | RMS (dB) | Peak (dB) |",
        f"|---|-----------|--------------|----------|----------|-----------|",
    ]

    for ch, r in zip(chapters, results):
        num = ch["index"]
        filename = f"{num:02d}-{chapter_slug(ch)}.mp3"
        full_path = output_dir / filename
        rms_ok = ACX_RMS_MIN <= (r["output_rms"] or -99) <= ACX_RMS_MAX
        peak_ok = (r["output_peak"] or 0) <= ACX_PEAK_MAX
        rms_flag = "" if rms_ok else " (!)"
        peak_flag = "" if peak_ok else " (!)"
        lines.append(
            f"| {num} | `{full_path}` | {ch['title']} | {r['duration_fmt']} | "
            f"{r['output_rms']}{rms_flag} | {r['output_peak']}{peak_flag} |"
        )

    lines += [
        f"",
        f"## Upload Checklist",
        f"",
        f"1. Log in to [ACX.com](https://www.acx.com/) or your Audible dashboard",
        f"2. Go to your title and select **Upload Audio**",
        f"3. Upload each file in the order listed above",
        f"4. Set the **Chapter Title** for each file to match the table above",
        f"5. ACX will run automated QA (bit rate, sample rate, RMS, peak, noise floor)",
        f"6. If any file fails QA, re-run this script with adjusted `--target-rms`",
        f"",
        f"## Notes",
        f"",
        f"- Opening Credits (copyright) should be the first file uploaded",
        f"- The retail sample is typically drawn from Chapter 1 (the introduction)",
        f"- ACX requires each file to be at least ~1 minute long",
        f"- Files flagged with (!) in the table above may need manual review",
        f"",
    ]

    instructions_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Export audiobook chapters as Audible/ACX-compliant MP3s")
    parser.add_argument("--config", "-cfg", default="_quarto-manual-paperback.yml",
                        help="Quarto config YAML (default: _quarto-manual-paperback.yml)")
    parser.add_argument("--force", "-f", action="store_true", help="Re-export even if MP3 already exists")
    parser.add_argument("--target-rms", type=float, default=-20.0,
                        help="Target RMS in dB (default: -20.0, midpoint of ACX range)")
    args = parser.parse_args()

    config_path = PROJECT_ROOT / args.config
    config = load_quarto_config(str(config_path))
    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

    chapters = extract_chapters(config)
    book = config.get("book", {})
    album = book.get("title", "Audiobook")
    authors = book.get("author", [])
    if isinstance(authors, list) and authors:
        artist = authors[0].get("name") if isinstance(authors[0], dict) else str(authors[0])
    else:
        artist = config.get("metadata", {}).get("creator", "Unknown")
    year = str(config.get("metadata", {}).get("copyright-year", datetime.now().year))

    output_dir = paths.root / "audible-export"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Audible/ACX Export")
    print(f"  Config:     {args.config}")
    print(f"  Album:      {album}")
    print(f"  Artist:     {artist}")
    print(f"  Target RMS: {args.target_rms} dB")
    print(f"  Output:     {output_dir}")
    print(f"  Chapters:   {len(chapters)}")
    print()

    results = []
    for ch in chapters:
        slug = chapter_slug(ch)
        wav_path = paths.chapters / f"{slug}.wav"
        mp3_filename = f"{ch['index']:02d}-{slug}.mp3"
        mp3_path = output_dir / mp3_filename

        if not wav_path.exists():
            print(f"  [{ch['index']:2d}] SKIP (no WAV): {slug}")
            results.append({
                "source_rms": None, "volume_adj": 0, "output_rms": None,
                "output_peak": None, "duration_secs": 0, "duration_fmt": "00:00:00",
            })
            continue

        if mp3_path.exists() and not args.force:
            # Already exported; measure existing
            rms = get_rms(mp3_path)
            peak = get_peak(mp3_path)
            dur = get_duration_secs(mp3_path)
            print(f"  [{ch['index']:2d}] CACHED: {mp3_filename} ({format_duration(dur)}, RMS={rms:.1f})")
            results.append({
                "source_rms": None, "volume_adj": 0,
                "output_rms": round(rms, 2) if rms else None,
                "output_peak": round(peak, 2) if peak else None,
                "duration_secs": round(dur, 1),
                "duration_fmt": format_duration(dur),
            })
            continue

        print(f"  [{ch['index']:2d}] Converting: {slug}.wav -> {mp3_filename} ...", end=" ", flush=True)
        r = convert_to_audible_mp3(
            wav_path=wav_path,
            mp3_path=mp3_path,
            target_rms=args.target_rms,
            track_num=ch["index"],
            track_total=len(chapters),
            title=ch["title"],
            album=album,
            artist=artist,
            year=year,
        )
        results.append(r)
        print(f"OK (RMS={r['output_rms']}, peak={r['output_peak']}, {r['duration_fmt']})")

    # Generate retail audio sample (first 5 min of chapter 1)
    generate_retail_sample(output_dir, chapters)

    # Generate upload instructions markdown
    instructions_path = output_dir / "AUDIBLE-UPLOAD-INSTRUCTIONS.md"
    generate_upload_instructions(chapters, results, output_dir, album, artist, instructions_path)

    # Summary
    exported = sum(1 for r in results if r["duration_secs"] > 0)
    total_secs = sum(r["duration_secs"] for r in results)
    print()
    print(f"Export complete: {exported}/{len(chapters)} chapters, {format_duration(total_secs)} total")
    print(f"Instructions:   {instructions_path}")
    print(f"Upload folder:  {output_dir}")

    # Warn about short chapters
    for ch, r in zip(chapters, results):
        if 0 < r["duration_secs"] < 60:
            print(f"  WARNING: Chapter {ch['index']} '{ch['title']}' is only {r['duration_fmt']} "
                  f"(ACX may reject files under 1 minute)")


if __name__ == "__main__":
    main()
