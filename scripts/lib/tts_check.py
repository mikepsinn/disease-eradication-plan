"""Check a voiced TTS chunk against its text with Whisper.

Gemini TTS sometimes invents words, most often a sentence after the last line of
the chunk. check_chunk() transcribes the chunk, lines the transcript up with the
text, trims invented words that come after the last real word, and reports
anything it cannot fix (invented or skipped words mid-chunk) so the caller can
re-voice the chunk.

Requires: pip install faster-whisper
"""
import difflib
import re
import subprocess
import threading
from dataclasses import dataclass, field
from pathlib import Path

WHISPER_MODEL = "small.en"
# Whisper mishears a word or two all the time; runs this long are the TTS, not Whisper.
MAX_EXTRA_WORDS = 3     # invented words in one place
MAX_MISSING_WORDS = 6   # text words skipped in one place
TRIM_PAD_S = 0.3        # audio kept after the last real word when trimming

# Narration spells numbers out and Whisper writes digits, so numbers are left out of the comparison.
NUMBER_WORDS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
    "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
    "hundred", "thousand", "million", "billion", "trillion", "quadrillion", "point", "oh",
}

_model = None
_model_lock = threading.Lock()


@dataclass
class ChunkCheck:
    ok: bool
    trimmed_s: float = 0.0
    problems: list[str] = field(default_factory=list)


def _tokens(text: str) -> list[str]:
    """Lowercase words without punctuation or numbers; "C.E.O." becomes "ceo"."""
    text = text.lower().replace("’", "'")
    text = re.sub(r"(?<=\b[a-z])\.", "", text)
    return [t for t in re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)
            if t not in NUMBER_WORDS and not any(c.isdigit() for c in t)]


def _transcribe(wav_path: Path) -> list[tuple[str, float, float]]:
    """(token, start_s, end_s) for every word Whisper hears."""
    global _model
    with _model_lock:
        if _model is None:
            from faster_whisper import WhisperModel
            _model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        segments, _ = _model.transcribe(str(wav_path), language="en", word_timestamps=True)
        return [(tok, w.start, w.end)
                for seg in segments for w in (seg.words or []) for tok in _tokens(w.word)]


def _trim(wav_path: Path, end_s: float) -> None:
    trimmed = wav_path.with_name(wav_path.stem + ".trim.wav")
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", str(wav_path), "-t", f"{end_s:.3f}",
        "-af", f"afade=t=out:st={max(0.0, end_s - 0.05):.3f}:d=0.05", "-c:a", "pcm_s16le", str(trimmed),
    ], check=True)
    trimmed.replace(wav_path)


def check_chunk(wav_path: Path, text: str) -> ChunkCheck:
    """Compare the voiced chunk with its text; trim invented words after the end in place."""
    said = _tokens(text)
    heard = _transcribe(wav_path)
    heard_tokens = [tok for tok, _, _ in heard]
    opcodes = difflib.SequenceMatcher(None, said, heard_tokens, autojunk=False).get_opcodes()
    equal = [op for op in opcodes if op[0] == "equal"]
    if not equal:
        return ChunkCheck(ok=False, problems=["transcript does not match the text at all"])

    check = ChunkCheck(ok=True)
    _, _, last_i, _, last_j = equal[-1]
    # Invented words after the text ran out: cut them off at the end of the last real word.
    if len(said) - last_i <= 1 and len(heard_tokens) - last_j >= MAX_EXTRA_WORDS:
        end_s = heard[last_j - 1][2] + TRIM_PAD_S
        end_s = min(end_s, heard[last_j][1] - 0.02)
        check.trimmed_s = heard[-1][2] - end_s
        _trim(wav_path, end_s)
        opcodes = [op for op in opcodes if op[3] < last_j]

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            continue
        extra, missing = (j2 - j1) - (i2 - i1), (i2 - i1) - (j2 - j1)
        if extra >= MAX_EXTRA_WORDS:
            check.problems.append(f"invented {extra} words: \"{' '.join(heard_tokens[j1:j2])}\"")
        if missing >= MAX_MISSING_WORDS:
            check.problems.append(f"skipped {missing} words: \"{' '.join(said[i1:i2])}\"")
    check.ok = not check.problems
    return check
