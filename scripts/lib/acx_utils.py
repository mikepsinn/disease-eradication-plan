"""ACX/Audible audio compliance utilities.

Reusable functions for normalizing audio to ACX specs:
  - MP3, CBR 192 kbps, 44.1 kHz, mono
  - RMS: -23 dB to -18 dB
  - Peak: -3 dB max
"""
import json
import subprocess
from pathlib import Path

# ACX spec constants
ACX_SAMPLE_RATE = 44100
ACX_BITRATE = 192  # kbps, CBR
ACX_RMS_MIN = -23.0
ACX_RMS_MAX = -18.0
ACX_PEAK_MAX = -3.0

DEFAULT_COVER = Path(__file__).parent.parent.parent / "assets" / "cover" / "h2ewd-twitter-summary-800x800.jpg"


def get_rms(file_path: Path) -> float | None:
    """Measure RMS level using ffmpeg astats (whole-file accumulation)."""
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
    """Measure peak level using ffmpeg astats (whole-file accumulation)."""
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


def loudnorm_measure(audio_path: Path) -> dict:
    """Pass 1: measure loudness stats with ffmpeg loudnorm."""
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(audio_path),
            "-af", "loudnorm=print_format=json",
            "-f", "null", "/dev/null",
        ],
        capture_output=True, text=True,
    )
    stderr = result.stderr
    json_start = stderr.rfind("{")
    json_end = stderr.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        raise RuntimeError(f"Could not parse loudnorm stats from {audio_path.name}")
    return json.loads(stderr[json_start:json_end])


def normalize_to_acx_mp3(
    input_path: Path,
    output_path: Path,
    target_rms: float = -20.0,
) -> dict:
    """Normalize any audio file to an ACX-compliant MP3.

    Two-pass loudnorm: measure, then apply in linear mode.
    Output: mono, 44.1 kHz, 192 kbps CBR, peak <= -3 dB.

    Returns dict with output_rms, output_peak, duration_secs, duration_fmt.
    """
    stats = loudnorm_measure(input_path)
    source_i = float(stats["input_i"])
    source_tp = float(stats["input_tp"])
    source_lra = float(stats["input_lra"])
    source_thresh = float(stats["input_thresh"])

    af = (
        f"loudnorm=I={target_rms}:TP={ACX_PEAK_MAX}:LRA=11"
        f":measured_I={source_i}:measured_TP={source_tp}"
        f":measured_LRA={source_lra}:measured_thresh={source_thresh}"
        f":linear=true:print_format=summary"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-af", af,
        "-ar", str(ACX_SAMPLE_RATE),
        "-ac", "1",
        "-b:a", f"{ACX_BITRATE}k",
        "-c:a", "libmp3lame",
        "-map", "0:a",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed for {input_path.name}:\n{result.stderr[-500:]}")

    out_rms = get_rms(output_path)
    out_peak = get_peak(output_path)
    duration = get_duration_secs(output_path)

    return {
        "source_rms": round(source_i, 2),
        "output_rms": round(out_rms, 2) if out_rms else None,
        "output_peak": round(out_peak, 2) if out_peak else None,
        "duration_secs": round(duration, 1),
        "duration_fmt": format_duration(duration),
    }


def tag_mp3(
    mp3_path: Path,
    title: str,
    album: str,
    artist: str,
    year: str,
    track_num: int | None = None,
    track_total: int | None = None,
    cover_path: Path | None = None,
) -> None:
    """Set ID3 tags and optional cover art on an MP3."""
    from mutagen.mp3 import MP3
    from mutagen.id3 import TIT2, TALB, TPE1, TPE2, TRCK, TDRC, TCON, APIC

    audio = MP3(str(mp3_path))
    if audio.tags is None:
        audio.add_tags()
    tags = audio.tags
    if tags is None:
        raise RuntimeError(f"Could not initialize ID3 tags for {mp3_path}")

    # Remove junk tags from external sources (Suno, etc.)
    for key in list(tags.keys()):
        if key.startswith(("COMM", "WOAS", "TXXX", "TSSE")):
            del tags[key]

    tags.add(TIT2(encoding=3, text=[title]))
    tags.add(TALB(encoding=3, text=[album]))
    tags.add(TPE1(encoding=3, text=[artist]))
    tags.add(TPE2(encoding=3, text=[artist]))
    tags.add(TDRC(encoding=3, text=[year]))
    tags.add(TCON(encoding=3, text=["Audiobook"]))

    if track_num is not None:
        track_str = str(track_num)
        if track_total is not None:
            track_str = f"{track_num}/{track_total}"
        tags.add(TRCK(encoding=3, text=[track_str]))

    if cover_path and cover_path.exists():
        tags.delall("APIC")
        tags.add(APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=cover_path.read_bytes(),
        ))

    audio.save()


def print_acx_report(path: Path) -> None:
    """Print ACX compliance info for an audio file."""
    rms = get_rms(path)
    peak = get_peak(path)
    dur = get_duration_secs(path)

    from mutagen.mp3 import MP3
    audio = MP3(str(path))
    channels = getattr(audio.info, "channels", 0)
    sample_rate = getattr(audio.info, "sample_rate", 0)
    bitrate = getattr(audio.info, "bitrate", 0)

    rms_ok = ACX_RMS_MIN <= (rms or -99) <= ACX_RMS_MAX
    peak_ok = (peak or 0) <= ACX_PEAK_MAX
    mono_ok = channels == 1

    print(f"  {path.name}")
    print(f"    Duration:    {format_duration(dur)}")
    print(f"    Channels:    {channels} ({'mono' if mono_ok else 'STEREO - NOT ACX COMPLIANT'})")
    print(f"    Sample rate: {sample_rate} Hz")
    print(f"    Bitrate:     {bitrate // 1000} kbps")
    print(f"    RMS:         {rms:.1f} dB {'OK' if rms_ok else '(!)'}")
    print(f"    Peak:        {peak:.1f} dB {'OK' if peak_ok else '(!)'}")
