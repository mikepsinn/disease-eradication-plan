"""Shared constants and functions for the audiobook pipeline.

Used by generate_audiobook_text.py, generate_audiobook.py, generate_audiobook_scenes.py,
and generate_audiobook_video.py.
"""
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

# --- Style constant (shared across image/video generation) ---
IMAGE_STYLE = "retro academic"

# --- Path constants (legacy, kept for backward compat) ---
PROJECT_ROOT = Path(__file__).parent.parent.parent
AUDIOBOOK_DIR = PROJECT_ROOT / "assets" / "audiobook"
NARRATION_DIR = AUDIOBOOK_DIR / "narration-txt-chapters"
NARRATION_CHUNKS_DIR = AUDIOBOOK_DIR / "narration-txt-chunks"
WAVS_DIRNAME = "wavs"
WAV_AUDIO_DIR = AUDIOBOOK_DIR / WAVS_DIRNAME
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
    narration_txt: Path
    narration_txt_chunks: Path
    wavs: Path
    alignment: Path
    subtitles: Path
    video: Path
    scenes: Path
    podcast_images: Path
    raw_mp3: Path
    manifest: Path


def get_paths(config_name: str) -> AudiobookPaths:
    """Create an AudiobookPaths for the given config name.

    Output structure: assets/audiobook/{config_name}/narration-txt-chapters/, wavs/, etc.
    """
    root = AUDIOBOOK_DIR / config_name
    video = root / "video"
    return AudiobookPaths(
        root=root,
        narration_txt=root / "narration-txt-chapters",
        narration_txt_chunks=root / "narration-txt-chunks",
        wavs=root / WAVS_DIRNAME,
        alignment=root / "alignment",
        subtitles=root / "subtitles",
        video=video,
        scenes=video / "scenes",
        podcast_images=root / "podcast-images",
        raw_mp3=root / "mp3-raw",
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


def text_hash(text: str) -> str:
    """SHA-256 hash prefix for content-based cache invalidation."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


# --- Podcast MP3 cache-busting ---
# Hashed filenames: {slug}.{8-hex-chars}.mp3
PODCAST_HASH_LEN = 8
PODCAST_HASH_RE = re.compile(r'^(.+)\.([0-9a-f]{8})\.mp3$')


def mp3_content_hash(path: Path) -> str:
    """MD5 hash prefix of MP3 file content for cache-busting filenames."""
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()[:PODCAST_HASH_LEN]


def find_current_mp3(slug: str, mp3_dir: Path) -> Path | None:
    """Find existing MP3 for a slug (hashed or canonical).

    Returns hashed version if found, else canonical, else None.
    """
    # Prefer hashed version
    for p in mp3_dir.glob(f"{slug}.*.mp3"):
        if PODCAST_HASH_RE.match(p.name):
            return p
    # Fall back to canonical
    canonical = mp3_dir / f"{slug}.mp3"
    if canonical.exists():
        return canonical
    return None


def parse_hashed_mp3(filename: str) -> tuple[str, str] | None:
    """Parse a hashed MP3 filename into (slug, hash).

    Returns None if the filename is not hashed.
    """
    m = PODCAST_HASH_RE.match(filename)
    if m:
        return m.group(1), m.group(2)
    return None


def safe_filename(title: str, max_len: int = 50) -> str:
    """Sanitize a title for filesystem use."""
    return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-')[:max_len]


def _parse_qmd_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a QMD file.

    Returns the frontmatter dict, or empty dict on failure.
    """
    if not file_path.exists():
        return {}

    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    try:
        from dih_models.yaml_utils import yaml_safe_load
        fm = yaml_safe_load(match.group(1))
        return fm if isinstance(fm, dict) else {}
    except Exception:
        # Fall back to regex extraction of key: value pairs
        result = {}
        for line in match.group(1).split('\n'):
            m = re.match(r'^(\w+):\s*["\']?(.+?)["\']?\s*$', line)
            if m:
                result[m.group(1)] = m.group(2)
        return result


def extract_title_from_qmd(file_path: Path) -> str:
    """Extract title from QMD file's YAML frontmatter."""
    fm = _parse_qmd_frontmatter(file_path)
    if 'title' in fm:
        return fm['title']
    return file_path.stem.replace('-', ' ').replace('_', ' ').title()


def extract_description_from_qmd(file_path: Path) -> str:
    """Extract description from QMD file's YAML frontmatter.

    Returns empty string if no description found.
    """
    fm = _parse_qmd_frontmatter(file_path)
    return fm.get('description', '')


def _load_quarto_variables() -> dict:
    """Load _variables.yml for resolving Quarto shortcodes in descriptions."""
    if not VARIABLES_YML.exists():
        return {}
    try:
        from dih_models.yaml_utils import yaml_safe_load
        return yaml_safe_load(VARIABLES_YML.read_text(encoding='utf-8')) or {}
    except Exception:
        return {}


def _resolve_quarto_vars(text: str, variables: dict) -> str:
    """Replace {{< var name >}} shortcodes with plain-text values, stripping CI intervals."""
    if '{{< var' not in text:
        return text
    from lib.yaml_sync_utils import substitute_quarto_variables, strip_confidence_intervals
    resolved = substitute_quarto_variables(text, variables)
    return strip_confidence_intervals(resolved)


def extract_chapters(config: dict) -> list[dict]:
    """Extract all chapters from a Quarto book config in order.

    Returns list of dicts with: index, path, title, part, description.
    """
    chapters = []
    idx = 0
    book = config.get('book', {})
    index_source = config.get('dih-render', {}).get('index-source')
    variables = _load_quarto_variables()

    def resolve_path(path: str) -> str:
        if index_source and path == 'index.qmd':
            return index_source
        return path

    def add_chapter(path: str, _config_text: str | None, part: str | None) -> None:
        nonlocal idx
        idx += 1
        resolved = resolve_path(path)
        qmd_path = PROJECT_ROOT / resolved
        # Always use QMD frontmatter title (config text: is for TOC, not narration)
        title = extract_title_from_qmd(qmd_path)
        if not title:
            raise ValueError(
                f"Chapter {idx} ({resolved}) has no title in QMD frontmatter"
            )
        description = extract_description_from_qmd(qmd_path)
        if description:
            description = _resolve_quarto_vars(description, variables)
        fm = _parse_qmd_frontmatter(qmd_path)
        # podcast: false in frontmatter excludes from podcast feed (still generates audio)
        podcast_include = fm.get('podcast', True)
        if isinstance(podcast_include, str):
            podcast_include = podcast_include.lower() not in ('false', 'no', '0')
        chapters.append({
            'path': resolved, 'title': title, 'part': part,
            'index': idx, 'description': description,
            'podcast_image': fm.get('podcast-image'),
            'youtube_thumbnail': fm.get('youtube-thumbnail'),
            'podcast': bool(podcast_include),
        })

    for item in book.get('chapters', []):
        if isinstance(item, str):
            add_chapter(item, None, None)
        elif isinstance(item, dict):
            if 'href' in item:
                add_chapter(item['href'], item.get('text'), None)
            elif 'part' in item:
                for sub in item.get('chapters', []):
                    if isinstance(sub, str):
                        add_chapter(sub, None, item['part'])
                    elif isinstance(sub, dict) and 'href' in sub:
                        add_chapter(sub['href'], sub.get('text'), item['part'])

    for item in book.get('appendices', []):
        if isinstance(item, dict) and 'part' in item:
            for sub in item.get('chapters', []):
                if isinstance(sub, str):
                    add_chapter(sub, None, f"Appendix: {item['part']}")
                elif isinstance(sub, dict) and 'href' in sub:
                    add_chapter(sub['href'], sub.get('text'), f"Appendix: {item['part']}")

    return chapters


def chapter_slug(chapter: dict) -> str:
    """Stable filename slug derived from the QMD path, not the title.

    Titles change; filenames shouldn't. Uses the QMD stem (e.g. 'cost-of-war')
    which is stable across title renames.
    """
    return Path(chapter['path']).stem


def find_prepared_text(chapter: dict, paths: AudiobookPaths | None = None) -> Path | None:
    """Find the prepared audiobook text file for a chapter."""
    text_dir = paths.narration_txt if paths else NARRATION_DIR
    slug = chapter_slug(chapter)
    text_file = text_dir / f"{slug}.prepared.txt"
    if text_file.exists():
        return text_file
    # Fallback: legacy index-prefixed name (e.g. 005-nih-fails.prepared.txt)
    for f in sorted(text_dir.glob(f"*-{slug}.prepared.txt")):
        return f
    return None


def find_chapter_audio(chapter: dict, paths: AudiobookPaths | None = None) -> Path | None:
    """Find the WAV audio file for a chapter."""
    wavs_dir = paths.wavs if paths else WAV_AUDIO_DIR
    slug = chapter_slug(chapter)
    audio_file = wavs_dir / f"{slug}.wav"
    if audio_file.exists():
        return audio_file
    # Fallback: legacy index-prefixed name (e.g. 005-nih-fails.wav)
    for f in sorted(wavs_dir.glob(f"*-{slug}.wav")):
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


def find_podcast_image(chapter: dict, paths: AudiobookPaths | None = None) -> Path | None:
    """Find the podcast episode image for a chapter.

    Checks the podcast-image frontmatter property first, then falls back
    to the convention-based slug lookup in the podcast-images directory.
    """
    # Check frontmatter podcast-image property (e.g. /assets/podcast/foo-podcast.jpg)
    fm_image = chapter.get('podcast_image')
    if fm_image:
        # Strip leading slash to make it relative to project root
        img = PROJECT_ROOT / fm_image.lstrip('/')
        if img.exists():
            return img

    # Fallback: convention-based slug lookup
    img_dir = paths.podcast_images if paths else AUDIOBOOK_DIR / "podcast-images"
    slug = chapter_slug(chapter)
    img = img_dir / f"{slug}-podcast.jpg"
    return img if img.exists() else None


def find_youtube_thumbnail(chapter: dict, paths: AudiobookPaths | None = None) -> Path | None:
    """Find the YouTube thumbnail image for a chapter.

    Checks the youtube-thumbnail frontmatter property first, then falls back
    to the convention-based slug lookup in the podcast-images directory.
    """
    # Check frontmatter youtube-thumbnail property (e.g. /assets/podcast/foo-youtube.jpg)
    fm_image = chapter.get('youtube_thumbnail')
    if fm_image:
        img = PROJECT_ROOT / fm_image.lstrip('/')
        if img.exists():
            return img

    # Fallback: convention-based slug lookup
    img_dir = paths.podcast_images if paths else AUDIOBOOK_DIR / "podcast-images"
    slug = chapter_slug(chapter)
    img = img_dir / f"{slug}-youtube.jpg"
    return img if img.exists() else None
