"""Shared constants and functions for the audiobook pipeline.

Used by generate_audiobook_text.py, generate_audiobook.py, generate_audiobook_scenes.py,
and generate_audiobook_video.py.
"""
import re
from dataclasses import dataclass
from pathlib import Path

# --- Path constants (legacy, kept for backward compat) ---
PROJECT_ROOT = Path(__file__).parent.parent.parent
AUDIOBOOK_DIR = PROJECT_ROOT / "audiobook"
TEXT_DIR = AUDIOBOOK_DIR / "text"
CHAPTER_AUDIO_DIR = AUDIOBOOK_DIR / "chapters"
ALIGNMENT_DIR = AUDIOBOOK_DIR / "alignment"
SUBTITLES_DIR = AUDIOBOOK_DIR / "subtitles"
VIDEO_DIR = AUDIOBOOK_DIR / "video"
SCENES_DIR = VIDEO_DIR / "scenes"
MANIFEST_PATH = AUDIOBOOK_DIR / "manifest.json"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "_quarto-manual-paperback.yml"
VARIABLES_YML = PROJECT_ROOT / "_variables.yml"


# --- Config-aware path management ---

@dataclass(frozen=True)
class AudiobookPaths:
    """All output paths for a single audiobook config."""
    root: Path
    text: Path
    chapters: Path
    alignment: Path
    subtitles: Path
    video: Path
    scenes: Path
    manifest: Path


def get_paths(config_name: str) -> AudiobookPaths:
    """Create an AudiobookPaths for the given config name.

    Output structure: audiobook/{config_name}/text/, chapters/, etc.
    """
    root = AUDIOBOOK_DIR / config_name
    video = root / "video"
    return AudiobookPaths(
        root=root,
        text=root / "text",
        chapters=root / "chapters",
        alignment=root / "alignment",
        subtitles=root / "subtitles",
        video=video,
        scenes=video / "scenes",
        manifest=root / "manifest.json",
    )


def config_name_from_path(config_path: Path) -> str:
    """Derive a short config name from a Quarto config path.

    _quarto-manual-paperback.yml -> manual-paperback
    """
    stem = config_path.stem  # e.g. "_quarto-manual-paperback"
    name = re.sub(r'^_quarto-', '', stem)
    return name


def resolve_config_path(name_or_path: str) -> Path:
    """Resolve a config name or path to an actual file.

    Accepts: 'manual-paperback', '_quarto-manual-paperback.yml', or a full path.
    """
    candidate = PROJECT_ROOT / name_or_path
    if candidate.exists():
        return candidate

    candidate = PROJECT_ROOT / f"_quarto-{name_or_path}.yml"
    if candidate.exists():
        return candidate

    raise FileNotFoundError(
        f"Config not found: tried '{name_or_path}' and '_quarto-{name_or_path}.yml' in {PROJECT_ROOT}"
    )


def get_available_configs() -> list[str]:
    """Discover available config names from _quarto-*.yml files."""
    configs = []
    for yml in PROJECT_ROOT.glob("_quarto-*.yml"):
        name = yml.stem.replace("_quarto-", "")
        configs.append(name)
    return sorted(configs)


def safe_filename(title: str, max_len: int = 50) -> str:
    """Sanitize a title for filesystem use."""
    return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')[:max_len]


def extract_title_from_qmd(file_path: Path) -> str:
    """Extract title from QMD file's YAML frontmatter.

    Uses proper YAML parsing when available, falls back to regex.
    """
    if not file_path.exists():
        return file_path.stem.replace('-', ' ').replace('_', ' ').title()

    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            from dih_models.yaml_utils import yaml_safe_load
            frontmatter = yaml_safe_load(match.group(1))
            if frontmatter and 'title' in frontmatter:
                return frontmatter['title']
        except Exception:
            # Fall back to regex extraction
            for line in match.group(1).split('\n'):
                m = re.match(r'^title:\s*["\']?(.+?)["\']?\s*$', line)
                if m:
                    return m.group(1)
    return file_path.stem.replace('-', ' ').replace('_', ' ').title()


def extract_chapters(config: dict) -> list[dict]:
    """Extract all chapters from a Quarto book config in order.

    Returns list of dicts with: index, path, title, part.
    """
    chapters = []
    idx = 0
    book = config.get('book', {})
    index_source = config.get('dih-render', {}).get('index-source')

    def resolve_path(path: str) -> str:
        if index_source and path == 'index.qmd':
            return index_source
        return path

    for item in book.get('chapters', []):
        if isinstance(item, str):
            idx += 1
            chapters.append({'path': resolve_path(item), 'title': None, 'part': None, 'index': idx})
        elif isinstance(item, dict):
            if 'href' in item:
                idx += 1
                chapters.append({'path': resolve_path(item['href']), 'title': item.get('text'), 'part': None, 'index': idx})
            elif 'part' in item:
                for sub in item.get('chapters', []):
                    idx += 1
                    if isinstance(sub, str):
                        chapters.append({'path': resolve_path(sub), 'title': None, 'part': item['part'], 'index': idx})
                    elif isinstance(sub, dict) and 'href' in sub:
                        chapters.append({'path': resolve_path(sub['href']), 'title': sub.get('text'), 'part': item['part'], 'index': idx})

    for item in book.get('appendices', []):
        if isinstance(item, dict) and 'part' in item:
            for sub in item.get('chapters', []):
                idx += 1
                if isinstance(sub, str):
                    chapters.append({'path': sub, 'title': None, 'part': f"Appendix: {item['part']}", 'index': idx})
                elif isinstance(sub, dict) and 'href' in sub:
                    chapters.append({'path': sub['href'], 'title': sub.get('text'), 'part': f"Appendix: {item['part']}", 'index': idx})

    return chapters


def find_prepared_text(chapter: dict, paths: AudiobookPaths | None = None) -> Path | None:
    """Find the prepared audiobook text file for a chapter."""
    text_dir = paths.text if paths else TEXT_DIR
    title = chapter.get('title') or ''
    safe = safe_filename(title)
    text_file = text_dir / f"{chapter['index']:03d}-{safe}.prepared.txt"
    if text_file.exists():
        return text_file
    # Fallback: match by chapter index prefix
    for f in text_dir.glob(f"{chapter['index']:03d}-*.prepared.txt"):
        return f
    return None


def find_chapter_audio(chapter: dict, paths: AudiobookPaths | None = None) -> Path | None:
    """Find the WAV audio file for a chapter."""
    chapters_dir = paths.chapters if paths else CHAPTER_AUDIO_DIR
    title = chapter.get('title') or ''
    safe = safe_filename(title)
    audio_file = chapters_dir / f"{chapter['index']:03d}-{safe}.wav"
    if audio_file.exists():
        return audio_file
    for f in chapters_dir.glob(f"{chapter['index']:03d}-*.wav"):
        return f
    return None


def filter_chapters(chapters: list[dict], chapter=None, start=None, end=None, limit=None) -> list[dict]:
    """Filter chapters by index, range, and/or limit.

    Args:
        chapter: Single chapter index to select
        start: Start index (inclusive)
        end: End index (inclusive)
        limit: Max number of chapters to return
    """
    if chapter is not None:
        chapters = [ch for ch in chapters if ch['index'] == chapter]
    elif start is not None or end is not None:
        lo = start or 1
        hi = end or max(ch['index'] for ch in chapters)
        chapters = [ch for ch in chapters if lo <= ch['index'] <= hi]
    if limit is not None:
        chapters = chapters[:limit]
    return chapters


def resolve_chapter_titles(chapters: list[dict]) -> list[dict]:
    """Fill in missing titles from QMD files."""
    for ch in chapters:
        if not ch['title']:
            ch['title'] = extract_title_from_qmd(PROJECT_ROOT / ch['path'])
    return chapters
