"""Forced alignment module using stable-ts (Whisper-based).

Provides word-level timestamps with character offsets for audiobook chapters.
Used by generate_audiobook.py (alignment step) and generate_audiobook_scenes.py
(precise timestamp lookup).

Requires: pip install stable-ts
Graceful degradation: functions raise ImportError if stable-ts is not installed;
callers catch and skip/fallback.
"""
import json
import re
from pathlib import Path


def _check_stable_ts():
    """Check if stable-ts is available. Raises ImportError if not."""
    try:
        import stable_whisper  # noqa: F401
    except ImportError:
        raise ImportError(
            "stable-ts is not installed. Install with: pip install stable-ts\n"
            "Alignment will be skipped."
        )


def align_chapter(
    wav_path: Path,
    text_path: Path,
    output_path: Path,
    model_name: str = "base",
    chapter: dict | None = None,
) -> list[dict]:
    """Run stable-ts forced alignment. Returns list of word dicts.

    Each word: {"word": "Moronia", "start_ms": 11850, "end_ms": 12200,
                "char_start": 45, "char_end": 52}

    char_start/char_end are computed by scanning through the source text,
    matching words sequentially.
    """
    _check_stable_ts()
    import stable_whisper

    source_text = text_path.read_text(encoding="utf-8")

    print(f"  Aligning audio to text ({model_name} model)...")
    model = stable_whisper.load_model(model_name)
    result = model.align(str(wav_path), source_text)

    # Extract word-level data from stable-ts result
    raw_words = []
    for segment in result.segments:
        for word_obj in segment.words:
            raw_words.append({
                "word": word_obj.word.strip(),
                "start_ms": int(word_obj.start * 1000),
                "end_ms": int(word_obj.end * 1000),
            })

    # Compute character offsets by walking through source text
    words = _compute_char_offsets(raw_words, source_text)

    # Build alignment JSON
    total_duration_ms = raw_words[-1]["end_ms"] if raw_words else 0
    alignment_data = {
        "chapter_index": chapter["index"] if chapter else 0,
        "chapter_title": chapter.get("title", "") if chapter else "",
        "wav_file": str(wav_path),
        "text_file": str(text_path),
        "total_chars": len(source_text),
        "total_duration_ms": total_duration_ms,
        "model": model_name,
        "words": words,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(alignment_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  Alignment saved: {output_path.name} ({len(words)} words)")
    return words


def _compute_char_offsets(raw_words: list[dict], source_text: str) -> list[dict]:
    """Walk source text and raw word list in parallel to assign char offsets.

    For each word from stable-ts, find its position in the source text
    (advancing a cursor). Matching is case-insensitive and strips punctuation
    from both sides to handle Whisper's text normalization.
    """
    cursor = 0
    words_with_offsets = []
    source_lower = source_text.lower()

    for w in raw_words:
        whisper_word = w["word"].strip()
        if not whisper_word:
            continue

        # Normalize: strip punctuation for matching
        clean_word = re.sub(r"[^\w]", "", whisper_word).lower()
        if not clean_word:
            # Pure punctuation token; skip
            continue

        # Search forward from cursor for this word
        best_pos = -1
        search_start = cursor
        # Allow some lookahead (words might be reordered slightly)
        search_end = min(len(source_text), cursor + max(500, len(clean_word) * 10))

        for i in range(search_start, search_end):
            # Check if clean_word matches at this position (ignoring punctuation in source)
            src_slice = source_lower[i:i + len(clean_word) + 20]
            src_clean = ""
            src_positions = []  # maps clean index -> source index
            for j, ch in enumerate(src_slice):
                if re.match(r"\w", ch):
                    src_positions.append(i + j)
                    src_clean += ch
                    if len(src_clean) >= len(clean_word):
                        break

            if src_clean[:len(clean_word)] == clean_word and len(src_clean) >= len(clean_word):
                best_pos = src_positions[0]
                # Find the end: the source position of the last matched char + 1
                end_pos = src_positions[len(clean_word) - 1] + 1
                break

        if best_pos >= 0:
            words_with_offsets.append({
                "word": whisper_word,
                "start_ms": w["start_ms"],
                "end_ms": w["end_ms"],
                "char_start": best_pos,
                "char_end": end_pos,
            })
            cursor = end_pos
        else:
            # Could not find word in source; include without char offsets
            words_with_offsets.append({
                "word": whisper_word,
                "start_ms": w["start_ms"],
                "end_ms": w["end_ms"],
                "char_start": cursor,
                "char_end": cursor,
            })

    return words_with_offsets


def load_alignment(alignment_path: Path) -> list[dict]:
    """Load alignment JSON from disk. Returns the words list."""
    data = json.loads(alignment_path.read_text(encoding="utf-8"))
    return data.get("words", [])


def load_alignment_data(alignment_path: Path) -> dict:
    """Load the full alignment JSON (including metadata)."""
    return json.loads(alignment_path.read_text(encoding="utf-8"))


def timestamps_for_char_range(
    words: list[dict], char_start: int, char_end: int
) -> tuple[int, int]:
    """Look up precise audio timestamps for a character range.

    Finds the first word whose char_end > char_start and the last word
    whose char_start < char_end. Returns (start_ms, end_ms).
    """
    first_ms = None
    last_ms = None

    for w in words:
        w_cs = w.get("char_start", 0)
        w_ce = w.get("char_end", 0)

        # Word overlaps with the requested range
        if w_ce > char_start and w_cs < char_end:
            if first_ms is None:
                first_ms = w["start_ms"]
            last_ms = w["end_ms"]

    if first_ms is None or last_ms is None:
        # Fallback: return 0,0 if no overlap found
        return (0, 0)

    return (first_ms, last_ms)


def generate_vtt(words: list[dict], output_path: Path, chars_per_cue: int = 120):
    """Generate WebVTT subtitle file from word-level alignment.

    Groups words into cues of ~chars_per_cue characters, breaking at
    sentence boundaries when possible.
    """
    if not words:
        return

    cues = []
    current_words: list[dict] = []
    current_chars = 0

    for w in words:
        word_text = w["word"]
        current_words.append(w)
        current_chars += len(word_text) + 1  # +1 for space

        # Check if we should break here
        at_sentence_end = word_text.rstrip().endswith((".", "!", "?", '."', '!"', '?"'))
        over_limit = current_chars >= chars_per_cue

        if at_sentence_end and current_chars >= chars_per_cue * 0.5:
            # Break at sentence boundary if we're at least half-full
            cues.append(_make_cue(current_words))
            current_words = []
            current_chars = 0
        elif over_limit:
            # Hard break at word boundary
            cues.append(_make_cue(current_words))
            current_words = []
            current_chars = 0

    # Flush remaining words
    if current_words:
        cues.append(_make_cue(current_words))

    # Write VTT
    lines = ["WEBVTT", ""]
    for i, cue in enumerate(cues, 1):
        lines.append(str(i))
        lines.append(f"{_format_vtt_time(cue['start_ms'])} --> {_format_vtt_time(cue['end_ms'])}")
        lines.append(cue["text"])
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Subtitles saved: {output_path.name} ({len(cues)} cues)")


def _make_cue(words: list[dict]) -> dict:
    """Create a VTT cue from a list of word dicts."""
    text = " ".join(w["word"] for w in words)
    return {
        "start_ms": words[0]["start_ms"],
        "end_ms": words[-1]["end_ms"],
        "text": text,
    }


def _format_vtt_time(ms: int) -> str:
    """Format milliseconds as HH:MM:SS.mmm for WebVTT."""
    hours = ms // 3_600_000
    minutes = (ms % 3_600_000) // 60_000
    seconds = (ms % 60_000) // 1000
    millis = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"
