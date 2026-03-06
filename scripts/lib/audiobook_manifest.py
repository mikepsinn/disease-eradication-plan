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

    For each chapter in the config, ensures the manifest entry has the correct
    index/title/path/part. If the path at a given index changed (chapter was
    inserted/reordered), stale audio fields are cleared. Entries for indices
    no longer in the config are removed.

    Useful after chapter insertion/reordering to fix stale manifest entries.
    """
    manifest = read_manifest(paths)
    manifest_path = paths.manifest if paths else MANIFEST_PATH
    existing = {ch['index']: ch for ch in manifest.get('chapters', [])}
    config_indices = set()

    for ch in chapters:
        idx = ch['index']
        config_indices.add(idx)
        new_path = ch['path']
        expected_slug = Path(new_path).stem
        new_fields = {'index': idx, 'path': new_path, 'title': ch.get('title', ''), 'part': ch.get('part')}

        if idx in existing:
            old_path = existing[idx].get('path')
            old_audio = existing[idx].get('audio_file', '')
            old_audio_slug = Path(old_audio).stem if old_audio else ''

            if (old_path and old_path != new_path) or (old_audio_slug and old_audio_slug != expected_slug):
                # Path changed at this index OR audio_file doesn't match the slug:
                # clear stale audio fields
                for field in _AUDIO_FIELDS:
                    existing[idx].pop(field, None)
                reason = f"path {Path(old_path).stem} -> {expected_slug}" if old_path != new_path else f"audio_file {old_audio_slug} != {expected_slug}"
                print(f"  [SYNC] Index {idx}: {reason}, cleared stale audio fields")
            existing[idx].update(new_fields)
        else:
            existing[idx] = new_fields

    # Remove entries for indices no longer in config
    removed = set(existing.keys()) - config_indices
    for idx in removed:
        print(f"  [SYNC] Removing stale manifest entry for index {idx}")
        del existing[idx]

    manifest['chapters'] = [existing[k] for k in sorted(existing.keys())]
    write_manifest(manifest, paths)
    print(f"  [OK] Manifest synced with config ({len(chapters)} chapters): {manifest_path.relative_to(PROJECT_ROOT)}")


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
