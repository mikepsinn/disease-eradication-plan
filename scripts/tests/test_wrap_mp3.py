#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the MP3 wrapping and finalization pipeline.

Verifies that:
- Raw MP3s are never mutated (written to separate output dir)
- Double-wrapping is structurally impossible
- Mtime-based caching works correctly
- ID3 tags are preserved through wrapping
- Content-hash renaming and old version cleanup work
"""
import sys
import time
from pathlib import Path

import pytest
from pydub import AudioSegment
from pydub.generators import Sine

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def _make_mp3(path: Path, duration_ms: int = 1000, tags: dict | None = None) -> Path:
    """Create a short MP3 file with optional ID3 tags."""
    audio = Sine(440).to_audio_segment(duration=duration_ms)
    path.parent.mkdir(parents=True, exist_ok=True)
    audio.export(str(path), format="mp3", bitrate="128k")
    if tags:
        from mutagen.mp3 import MP3
        from mutagen.id3 import TIT2, TPE1
        mp3 = MP3(str(path))
        if mp3.tags is None:
            mp3.add_tags()
        tags_obj = mp3.tags
        if tags_obj is None:
            raise RuntimeError(f"Could not initialize ID3 tags for {path}")
        for key, val in tags.items():
            if key == 'title':
                tags_obj.add(TIT2(encoding=3, text=[val]))
            elif key == 'artist':
                tags_obj.add(TPE1(encoding=3, text=[val]))
        mp3.save()
    return path


def _make_wav(path: Path, duration_ms: int = 500) -> Path:
    """Create a short WAV file for use as intro/outro."""
    audio = Sine(880).to_audio_segment(duration=duration_ms)
    path.parent.mkdir(parents=True, exist_ok=True)
    audio.export(str(path), format="wav")
    return path


def _mp3_duration_ms(path: Path) -> int:
    """Get duration of an MP3 file in milliseconds."""
    return len(AudioSegment.from_mp3(str(path)))


class TestWrapMp3WithIntroOutro:
    """Tests for wrap_mp3_with_intro_outro()."""

    def test_wrap_creates_output_in_separate_dir(self, tmp_path: Path):
        """Wrapped file ends up in output dir; raw file is untouched."""
        from generate_audiobook import wrap_mp3_with_intro_outro

        raw_dir = tmp_path / "mp3-raw"
        out_dir = tmp_path / "mp3"
        raw_mp3 = _make_mp3(raw_dir / "ch1.mp3", duration_ms=2000)
        intro = _make_mp3(tmp_path / "intro.mp3", duration_ms=500)

        raw_size_before = raw_mp3.stat().st_size
        raw_mtime_before = raw_mp3.stat().st_mtime

        result = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro)

        assert result is not None
        assert result.parent == out_dir
        assert result.name == "ch1.mp3"
        assert result.exists()
        # Raw file must be untouched
        assert raw_mp3.stat().st_size == raw_size_before
        assert raw_mp3.stat().st_mtime == raw_mtime_before

    def test_wrap_never_double_wraps(self, tmp_path: Path):
        """Calling wrap twice produces same duration as calling it once."""
        from generate_audiobook import wrap_mp3_with_intro_outro

        raw_dir = tmp_path / "mp3-raw"
        out_dir = tmp_path / "mp3"
        raw_mp3 = _make_mp3(raw_dir / "ch1.mp3", duration_ms=2000)
        intro = _make_mp3(tmp_path / "intro.mp3", duration_ms=500)
        outro = _make_wav(tmp_path / "outro.wav", duration_ms=300)

        # First wrap
        result1 = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro, outro_path=outro)
        assert result1 is not None
        duration_after_first = _mp3_duration_ms(result1)

        # Force cache miss by touching raw file
        time.sleep(0.1)
        raw_mp3.touch()

        # Second wrap (reads from raw again, not from wrapped output)
        result2 = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro, outro_path=outro)
        assert result2 is not None
        duration_after_second = _mp3_duration_ms(result2)

        # Durations should be equal (no double-wrapping)
        assert abs(duration_after_first - duration_after_second) < 100  # within 100ms tolerance

    def test_wrap_skips_when_output_newer(self, tmp_path: Path):
        """Cache hit: mtime-based skip works when output is newer than all inputs."""
        from generate_audiobook import wrap_mp3_with_intro_outro

        raw_dir = tmp_path / "mp3-raw"
        out_dir = tmp_path / "mp3"
        raw_mp3 = _make_mp3(raw_dir / "ch1.mp3", duration_ms=1000)
        intro = _make_mp3(tmp_path / "intro.mp3", duration_ms=500)

        # First wrap creates the output
        result1 = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro)
        assert result1 is not None
        mtime1 = result1.stat().st_mtime

        # Second wrap should skip (output is newer)
        result2 = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro)
        assert result2 is not None
        mtime2 = result2.stat().st_mtime

        # Output file should not have been rewritten
        assert mtime1 == mtime2

    def test_wrap_rebuilds_when_intro_changes(self, tmp_path: Path):
        """Cache miss: new intro file triggers rebuild."""
        from generate_audiobook import wrap_mp3_with_intro_outro

        raw_dir = tmp_path / "mp3-raw"
        out_dir = tmp_path / "mp3"
        raw_mp3 = _make_mp3(raw_dir / "ch1.mp3", duration_ms=1000)
        intro = _make_mp3(tmp_path / "intro.mp3", duration_ms=500)

        # First wrap
        result1 = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro)
        assert result1 is not None
        duration1 = _mp3_duration_ms(result1)

        # Modify intro (longer duration, newer mtime)
        time.sleep(0.1)
        _make_mp3(tmp_path / "intro.mp3", duration_ms=1500)

        # Second wrap should rebuild
        result2 = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro)
        assert result2 is not None
        duration2 = _mp3_duration_ms(result2)

        # Duration should reflect the new, longer intro
        assert duration2 > duration1

    def test_wrap_preserves_id3_tags(self, tmp_path: Path):
        """ID3 tags from raw MP3 are copied to the wrapped output."""
        from generate_audiobook import wrap_mp3_with_intro_outro
        from mutagen.mp3 import MP3

        raw_dir = tmp_path / "mp3-raw"
        out_dir = tmp_path / "mp3"
        raw_mp3 = _make_mp3(
            raw_dir / "ch1.mp3", duration_ms=1000,
            tags={'title': 'Test Chapter', 'artist': 'Test Author'},
        )
        intro = _make_mp3(tmp_path / "intro.mp3", duration_ms=500)

        result = wrap_mp3_with_intro_outro(raw_mp3, out_dir, intro_path=intro)

        tagged = MP3(str(result))
        assert tagged.tags is not None
        assert str(tagged.tags.get('TIT2')) == 'Test Chapter'
        assert str(tagged.tags.get('TPE1')) == 'Test Author'

    def test_wrap_with_no_intro_outro_copies_raw(self, tmp_path: Path):
        """When no intro/outro provided, raw is copied to output dir."""
        from generate_audiobook import wrap_mp3_with_intro_outro

        raw_dir = tmp_path / "mp3-raw"
        out_dir = tmp_path / "mp3"
        raw_mp3 = _make_mp3(raw_dir / "ch1.mp3", duration_ms=1000)

        result = wrap_mp3_with_intro_outro(raw_mp3, out_dir)

        assert result is not None
        assert result.parent == out_dir
        assert result.exists()
        # Duration should match raw (no intro/outro added)
        raw_dur = _mp3_duration_ms(raw_mp3)
        out_dur = _mp3_duration_ms(result)
        assert abs(raw_dur - out_dur) < 50


class TestFinalizePodcastMp3:
    """Tests for finalize_podcast_mp3()."""

    def test_finalize_adds_content_hash(self, tmp_path: Path):
        """Output filename is {slug}.{hash8}.mp3."""
        from generate_audiobook import finalize_podcast_mp3
        from lib.audiobook_common import PODCAST_HASH_RE

        mp3 = _make_mp3(tmp_path / "ch1.mp3", duration_ms=1000)
        result = finalize_podcast_mp3(mp3)

        assert PODCAST_HASH_RE.match(result.name)
        assert result.name.startswith("ch1.")
        assert result.exists()
        # Original canonical name should be gone
        assert not mp3.exists()

    def test_finalize_cleans_old_versions(self, tmp_path: Path):
        """Old hashed files for the same slug are deleted."""
        from generate_audiobook import finalize_podcast_mp3

        # Create an old hashed version
        old = _make_mp3(tmp_path / "ch1.deadbeef.mp3", duration_ms=500)
        # Create the new canonical version
        mp3 = _make_mp3(tmp_path / "ch1.mp3", duration_ms=1000)

        result = finalize_podcast_mp3(mp3)

        assert result.exists()
        assert not old.exists()  # old version cleaned up
        assert not mp3.exists()  # canonical renamed away
