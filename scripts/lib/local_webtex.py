#!/usr/bin/env python3
"""
Local WebTeX Caching Server
============================

Drop-in replacement for latex.codecogs.com that caches SVG equations locally.
On cache miss, fetches from codecogs (with timeout). On cache hit, serves instantly.

This eliminates build failures when codecogs is unreachable: equations rendered
once are cached permanently and served from disk on subsequent builds.

Usage (from render-quarto.py):
    from local_webtex import start_server, stop_server
    port = start_server(cache_dir=Path("_build_temp/.webtex-cache"))
    # ... build with url: "http://127.0.0.1:{port}/svg.latex?" ...
    stop_server()
"""

import hashlib
import sys
import threading
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

CODECOGS_BASE = "https://latex.codecogs.com/svg.latex?"
FETCH_TIMEOUT = 15  # seconds per equation fetch (vs Pandoc's ~30s default)

_cache_dir: Optional[Path] = None
_server: Optional[HTTPServer] = None
_thread: Optional[threading.Thread] = None
_stats = {"hits": 0, "fetches": 0, "errors": 0}


def _cache_key(equation: str) -> str:
    """Stable cache key from equation content."""
    return hashlib.sha256(equation.encode("utf-8")).hexdigest()[:16]


def _fetch_from_codecogs(equation: str) -> Optional[bytes]:
    """Fetch SVG from codecogs with timeout."""
    url = CODECOGS_BASE + urllib.parse.quote(equation, safe="")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QuartoBuild/1.0"})
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            return resp.read()
    except Exception:
        return None


def _get_svg(equation: str, cache_dir: Path) -> Optional[bytes]:
    """Get SVG for equation: cache hit or fetch from codecogs."""
    key = _cache_key(equation)
    cache_file = cache_dir / f"{key}.svg"

    if cache_file.exists():
        _stats["hits"] += 1
        return cache_file.read_bytes()

    svg = _fetch_from_codecogs(equation)
    if svg:
        _stats["fetches"] += 1
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file.write_bytes(svg)
        return svg

    _stats["errors"] += 1
    return None


class _WebtexHandler(BaseHTTPRequestHandler):
    """HTTP handler mimicking the codecogs /svg.latex? endpoint."""

    def do_GET(self):
        if not self.path.startswith("/svg.latex"):
            self.send_error(404)
            return

        idx = self.path.find("?")
        if idx == -1:
            self.send_error(400, "No equation provided")
            return

        equation = urllib.parse.unquote(self.path[idx + 1:])

        cache_dir = _cache_dir
        if cache_dir is None:
            self.send_error(500, "Cache directory not initialized")
            return

        svg = _get_svg(equation, cache_dir)
        if svg is None:
            self.send_error(502, "Failed to render equation (codecogs unreachable)")
            return

        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Content-Length", str(len(svg)))
        self.send_header("Cache-Control", "public, max-age=31536000")
        self.end_headers()
        self.wfile.write(svg)

    def log_message(self, format, *args):
        """Suppress per-request logging (summary printed at shutdown)."""
        pass


def start_server(cache_dir: Path, port: int = 0) -> int:
    """Start local webtex caching server. Returns the assigned port."""
    global _cache_dir, _server, _thread, _stats

    _cache_dir = cache_dir
    _cache_dir.mkdir(parents=True, exist_ok=True)
    _stats = {"hits": 0, "fetches": 0, "errors": 0}

    _server = HTTPServer(("127.0.0.1", port), _WebtexHandler)
    actual_port = _server.server_address[1]

    _thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _thread.start()

    # Report cached equation count
    cached = len(list(_cache_dir.glob("*.svg")))
    if cached:
        print(f"[OK] Local webtex server on port {actual_port} ({cached} cached equations)")
    else:
        print(f"[OK] Local webtex server on port {actual_port} (empty cache, will fetch from codecogs)")

    return actual_port


def stop_server() -> None:
    """Stop server and print stats."""
    global _server, _thread

    if _server:
        _server.shutdown()
        _server = None
    _thread = None

    total = _stats["hits"] + _stats["fetches"] + _stats["errors"]
    if total > 0:
        print(
            f"[OK] Webtex stats: {_stats['hits']} cache hits, "
            f"{_stats['fetches']} fetched, {_stats['errors']} errors"
        )


def warm_cache(cache_dir: Path, equations: list[str]) -> int:
    """Pre-fetch equations into cache (useful for CI). Returns count fetched."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    fetched = 0
    for eq in equations:
        key = _cache_key(eq)
        cache_file = cache_dir / f"{key}.svg"
        if not cache_file.exists():
            svg = _fetch_from_codecogs(eq)
            if svg:
                cache_file.write_bytes(svg)
                fetched += 1
    return fetched
