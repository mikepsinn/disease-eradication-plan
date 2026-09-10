"""Resolve images hosted by this Quarto project without network requests."""

from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

from dih_models.yaml_utils import load_quarto_config


@lru_cache(maxsize=8)
def _project_site_hosts(project_root: Path) -> frozenset[str]:
    hosts = set()
    for config_path in project_root.glob("_quarto-*.yml"):
        config = load_quarto_config(config_path)
        for section in ("book", "website"):
            site_url = config.get(section, {}).get("site-url", "")
            host = urlsplit(site_url).hostname
            if host:
                hosts.add(host)
    return frozenset(hosts)


def local_image_path(image_url: str, project_root: Path) -> str | None:
    """Return the URL path for local/project-hosted images, None for external ones.

    Keep URL escaping intact for generated Markdown. Filesystem callers should
    unquote the result. Query strings and fragments are not part of the filename.
    """
    parsed = urlsplit(image_url)
    if parsed.netloc:
        if parsed.scheme not in ("", "http", "https"):
            return None
        if parsed.hostname not in _project_site_hosts(project_root.resolve()):
            return None
    elif parsed.scheme:
        return None
    return parsed.path or None
