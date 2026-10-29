"""Audiobook manifest read/merge/write with field preservation.

Fixes the bug where generate_audiobook_text.py's save_manifest() would overwrite
the entire manifest, destroying audio/video metadata added by other scripts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.audiobook_common import AudiobookPaths

from lib.audiobook_common import MANIFEST_PATH, PROJECT_ROOT, NARRATION_DIR


def read_manifest(paths: AudiobookPaths | None = None) -> dict:
    """Read manifest.json, returning empty structure if missing."""
    manifest_path = paths.manifest if paths else MANIFEST_PATH
    narration_dir = paths.narration_txt if paths else NARRATION_DIR
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding='utf-8'))
    return {'chapters': [], 'output_dir': str(narration_dir.relative_to(PROJECT_ROOT))}


def write_manifest(manifest: dict, paths: AudiobookPaths | None = None):
    """Write manifest.json with consistent formatting."""
    manifest_path = paths.manifest if paths else MANIFEST_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )


def update_chapter_fields(chapter_index: int, paths: AudiobookPaths | None = None,
                          expected_path: str | None = None, **fields):
    """Merge fields into a specific chapter's manifest entry without destroying other fields.

    If no chapter entry exists for this index, creates one with the given fields.

    Args:
        expected_path: If provided, verifies the manifest entry's path matches.
            If it doesn't (chapter was reordered/inserted), stale audio/video
            fields are cleared before applying the update.
    """
    manifest = read_manifest(paths)
    chapters = manifest.get('chapters', [])

    # Also check path from fields themselves
    check_path = expected_path or fields.get('path')

    found = False
    for ch in chapters:
        if ch.get('index') == chapter_index:
            # If path changed, clear stale audio fields from old chapter
            if check_path and ch.get('path') and ch['path'] != check_path:
                for field in _AUDIO_FIELDS:
                    ch.pop(field, None)
            ch.update(fields)
            found = True
            break

    if not found:
        entry = {'index': chapter_index}
        entry.update(fields)
        chapters.append(entry)
        chapters.sort(key=lambda c: c['index'])

    manifest['chapters'] = chapters
    write_manifest(manifest, paths)


_AUDIO_FIELDS = {
    'audio_file', 'duration_ms', 'duration_formatted', 'audio_start_ms', 'audio_end_ms',
    'alignment_file', 'subtitle_file', 'scenes', 'video_status', 'video_16x9', 'video_9x16',
}


def sync_manifest_from_config(chapters: list[dict], paths: AudiobookPaths | None = None):
    """Sync manifest chapter entries with the current book config.

    Entries are matched to config chapters by QMD path and given that chapter's
    index/title/path/part, so when a chapter is inserted, cut or moved, every
    entry moves with its chapter instead of another chapter's audio landing on
    it. Audio fields that don't match the chapter's slug are cleared, and entries
    for chapters no longer in the config are removed.

    chapters must be the whole book config, not a filtered subset.
    """
    manifest = read_manifest(paths)
    by_path = {ch['path']: ch for ch in manifest.get('chapters', []) if ch.get('path')}
    synced = []

    for ch in chapters:
        expected_slug = Path(ch['path']).stem
        entry = by_path.pop(ch['path'], {})
        if entry and entry.get('index') != ch['index']:
            print(f"  [SYNC] {expected_slug}: index {entry.get('index')} -> {ch['index']}")
        old_audio = entry.get('audio_file', '')
        if old_audio and Path(old_audio).stem != expected_slug:
            for field in _AUDIO_FIELDS:
                entry.pop(field, None)
            print(f"  [SYNC] {expected_slug}: audio_file {Path(old_audio).stem} doesn't match, cleared stale audio fields")
        entry.update({'index': ch['index'], 'path': ch['path'], 'title': ch.get('title', ''), 'part': ch.get('part')})
        synced.append(entry)

    for stale in by_path.values():
        print(f"  [SYNC] Removing manifest entry for {Path(stale['path']).stem} (not in the book config)")

    manifest['chapters'] = synced
    write_manifest(manifest, paths)


def save_text_results(results: list[dict], paths: AudiobookPaths | None = None):
    """Update manifest with text generation results, MERGING with existing chapter data.

    This replaces the old destructive save_manifest() that would overwrite the entire file.
    Each result dict should have at minimum an 'index' key.

    When a chapter's path changes for a given index (e.g. a new chapter was inserted),
    stale audio/alignment/video fields from the old chapter are cleared.
    """
    manifest = read_manifest(paths)
    narration_dir = paths.narration_txt if paths else NARRATION_DIR
    manifest_path = paths.manifest if paths else MANIFEST_PATH
    existing = {ch['index']: ch for ch in manifest.get('chapters', [])}

    for result in results:
        idx = result['index']
        if idx in existing:
            old_path = existing[idx].get('path')
            new_path = result.get('path')
            if old_path and new_path and old_path != new_path:
                # Chapter at this index changed (insertion/reorder).
                # Clear stale audio fields that belong to the old chapter.
                for field in _AUDIO_FIELDS:
                    existing[idx].pop(field, None)
            existing[idx].update(result)
        else:
            existing[idx] = result

    manifest['chapters'] = [existing[k] for k in sorted(existing.keys())]
    manifest['output_dir'] = str(narration_dir.relative_to(PROJECT_ROOT))
    write_manifest(manifest, paths)
    print(f"\nManifest saved to: {manifest_path.relative_to(PROJECT_ROOT)}")
