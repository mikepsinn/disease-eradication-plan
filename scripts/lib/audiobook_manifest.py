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

from lib.audiobook_common import MANIFEST_PATH, PROJECT_ROOT, TEXT_DIR


def read_manifest(paths: AudiobookPaths | None = None) -> dict:
    """Read manifest.json, returning empty structure if missing."""
    manifest_path = paths.manifest if paths else MANIFEST_PATH
    text_dir = paths.text if paths else TEXT_DIR
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding='utf-8'))
    return {'chapters': [], 'output_dir': str(text_dir.relative_to(PROJECT_ROOT))}


def write_manifest(manifest: dict, paths: AudiobookPaths | None = None):
    """Write manifest.json with consistent formatting."""
    manifest_path = paths.manifest if paths else MANIFEST_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )


def update_chapter_fields(chapter_index: int, paths: AudiobookPaths | None = None, **fields):
    """Merge fields into a specific chapter's manifest entry without destroying other fields.

    If no chapter entry exists for this index, creates one with the given fields.
    """
    manifest = read_manifest(paths)
    chapters = manifest.get('chapters', [])

    found = False
    for ch in chapters:
        if ch.get('index') == chapter_index:
            ch.update(fields)
            found = True
            break

    if not found:
        entry = {'index': chapter_index}
        entry.update(fields)
        chapters.append(entry)
        chapters.sort(key=lambda c: c.get('index', 0))

    manifest['chapters'] = chapters
    write_manifest(manifest, paths)


def save_text_results(results: list[dict], paths: AudiobookPaths | None = None):
    """Update manifest with text generation results, MERGING with existing chapter data.

    This replaces the old destructive save_manifest() that would overwrite the entire file.
    Each result dict should have at minimum an 'index' key.
    """
    manifest = read_manifest(paths)
    text_dir = paths.text if paths else TEXT_DIR
    manifest_path = paths.manifest if paths else MANIFEST_PATH
    existing = {ch['index']: ch for ch in manifest.get('chapters', [])}

    for result in results:
        idx = result['index']
        if idx in existing:
            existing[idx].update(result)
        else:
            existing[idx] = result

    manifest['chapters'] = [existing[k] for k in sorted(existing.keys())]
    manifest['output_dir'] = str(text_dir.relative_to(PROJECT_ROOT))
    write_manifest(manifest, paths)
    print(f"\nManifest saved to: {manifest_path.relative_to(PROJECT_ROOT)}")
