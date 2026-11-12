"""Tests for the Whisper transcript check's handling of spelled-out acronyms."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tts_check import _join_spelled, _tokens


def _heard(*words: str) -> list[tuple[str, float, float]]:
    return [(w, float(i), i + 0.5) for i, w in enumerate(words)]


def test_spelled_acronym_joins_into_the_texts_word():
    said = set(_tokens("Cost per D.A.L.Y. averted"))
    out = _join_spelled(_heard("cost", "per", "d", "a", "l", "y", "averted"), said)
    assert [w for w, _, _ in out] == ["cost", "per", "daly", "averted"]
    assert out[2][1:] == (2.0, 5.5)


def test_article_before_an_acronym_stays_a_word():
    said = set(_tokens("a U.S. and C. law"))
    out = _join_spelled(_heard("a", "u", "s", "and", "c", "law"), said)
    assert [w for w, _, _ in out] == ["a", "us", "and", "c", "law"]


def test_letters_that_spell_nothing_in_the_text_are_left_alone():
    said = set(_tokens("I think so"))
    out = _join_spelled(_heard("i", "x", "think", "so"), said)
    assert [w for w, _, _ in out] == ["i", "x", "think", "so"]
