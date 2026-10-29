"""Word timings for the podcast outro at the end of the episode MP3, which the audiobook
pipeline does not align. Writes ../../outro-words.json, which tools/word-timings.mjs merges.

    python tools/outro-words.py <episode MP3> <outro start in seconds>
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
mp3, start = sys.argv[1], float(sys.argv[2])
plan = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
    wav = Path(tmp) / "outro.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-i", mp3, "-ac", "1", "-ar", "16000", str(wav)], check=True)
    segments, _ = WhisperModel("small.en", compute_type="int8").transcribe(str(wav), word_timestamps=True)
    words: list[dict] = []
    for w in (w for seg in segments for w in (seg.words or [])):
        text = w.word.strip()
        if words and text[:1] in ".,%":  # Whisper splits "2.6", "468,000" and "1%" into pieces
            words[-1]["word"] += text
            words[-1]["end"] = round(start + w.end, 3)
            continue
        words.append({"start": round(start + w.start, 3), "end": round(start + w.end, 3), "word": text})
(plan / "outro-words.json").write_text(json.dumps(words, indent=0) + "\n", encoding="utf-8")
print(f"{len(words)} outro words from {start:.2f} s: {' '.join(w['word'] for w in words)[:300]}")
