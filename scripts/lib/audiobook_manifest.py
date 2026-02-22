"""Audiobook manifest read/merge/write with field preservation.

Fixes the bug where generate_audiobook_text.py's save_manifest() would overwrite
the entire manifest, destroying audio/video metadata added by other scripts.
"""
import json
from pathlib import Path

from lib.audiobook_common import MANIFEST_PATH, PROJECT_ROOT, TEXT_DIR


def read_manifest() -> dict:
    """Read manifest.json, returning empty structure if missing."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    return {'chapters': [], 'output_dir': str(TEXT_DIR.relative_to(PROJECT_ROOT))}


def write_manifest(manifest: dict):
    """Write manifest.json with consistent formatting."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )


def update_chapter_fields(chapter_index: int, **fields):
    """Merge fields into a specific chapter's manifest entry without destroying other fields.

    If no chapter entry exists for this index, creates one with the given fields.
    """
    manifest = read_manifest()
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
    write_manifest(manifest)


def save_text_results(results: list[dict]):
    """Update manifest with text generation results, MERGING with existing chapter data.

    This replaces the old destructive save_manifest() that would overwrite the entire file.
    Each result dict should have at minimum an 'index' key.
    """
    manifest = read_manifest()
    existing = {ch['index']: ch for ch in manifest.get('chapters', [])}

    for result in results:
        idx = result['index']
        if idx in existing:
            existing[idx].update(result)
        else:
            existing[idx] = result

    manifest['chapters'] = [existing[k] for k in sorted(existing.keys())]
    manifest['output_dir'] = str(TEXT_DIR.relative_to(PROJECT_ROOT))
    write_manifest(manifest)
    print(f"\nManifest saved to: {MANIFEST_PATH.relative_to(PROJECT_ROOT)}")
