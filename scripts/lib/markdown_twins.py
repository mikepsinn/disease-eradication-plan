#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write a markdown copy of each rendered page for AI tools.

AI fetch tools turn a page into text and cut it at a size limit (Claude Code
stops near 100,000 characters). A Quarto page spends much of that on
navigation, scripts, and hover tooltips. Each page gets page.llms.md beside
page.html, the name that Quarto's own llms-txt option uses. That option does
nothing for book projects before Quarto 1.11, garbles math, and keeps the
tooltips, so the build runs the same conversion with two fixes
(scripts/filters/llms-markdown.lua).

Each page also gets <link rel="alternate" type="text/markdown">, and the
site's llms.txt links to the copies. A Cloudflare URL Rewrite Rule sends the
copy to clients that ask for text/markdown (cloudflare/README.md).
"""

from __future__ import annotations

import html
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Optional, cast
from urllib.parse import quote

from lxml import html as lxml_html

TWIN_SUFFIX = ".llms.md"
LUA_FILTER = Path(__file__).resolve().parents[1] / "filters" / "llms-markdown.lua"
PANDOC_OUTPUT_FORMAT = "gfm-raw_html-tex_math_gfm+tex_math_dollars"

_MAIN_MARKER = 'id="quarto-document-content"'
# Parts of <main> that are not content. The loader and the Listen/Get bar come
# from assets/html/page-loader.html and platform-bar.html. The keyword list is
# the same on every page. The rest is what Quarto's llms-txt also removes.
_DROP_XPATH = " | ".join(
    [
        ".//script",
        ".//style",
        ".//noscript",
        ".//link",
        ".//meta",
        ".//*[@id='hash-loader-hint']",
        ".//*[@id='progress-bar']",
        ".//*[@id='calc-loader']",
        ".//*[@id='platform-bar']",
        ".//*[contains(concat(' ', normalize-space(@class), ' '), ' keywords ')]",
        ".//*[contains(concat(' ', normalize-space(@class), ' '), ' sidebar ')]",
        ".//*[contains(concat(' ', normalize-space(@class), ' '), ' quarto-page-breadcrumbs ')]",
    ]
)


def _quarto_llms_filter() -> Path:
    """Return Quarto's own HTML-to-markdown cleanup filter (Quarto 1.9 and later)."""
    paths = subprocess.run(["quarto", "--paths"], capture_output=True, text=True, check=True).stdout
    share_dir = Path(paths.splitlines()[1].strip())
    llms_filter = share_dir / "filters" / "llms" / "llms.lua"
    if not llms_filter.is_file():
        raise FileNotFoundError(f"{llms_filter} not found: markdown twins need Quarto 1.9 or later")
    return llms_filter


def _main_document(page_bytes: bytes) -> Optional[str]:
    """Return the content of the page's <main> as a small HTML document."""
    tree = lxml_html.fromstring(page_bytes, parser=lxml_html.HTMLParser(encoding="utf-8", huge_tree=True))
    mains = tree.xpath("//main[@id='quarto-document-content']")
    if not mains:
        return None
    main = mains[0]
    for element in main.xpath(_DROP_XPATH):
        element.drop_tree()
    body = html.escape(main.text or "") + "".join(
        cast(str, lxml_html.tostring(child, encoding="unicode")) for child in main
    )
    return f'<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8"></head>\n<body>\n{body}\n</body>\n</html>\n'


def _write_twin(page_path: Path, quarto_filter: Path) -> bool:
    """Convert one page. Returns False for HTML that is not a Quarto page."""
    document = _main_document(page_path.read_bytes())
    if document is None:
        return False
    twin_path = page_path.with_name(page_path.stem + TWIN_SUFFIX)
    result = subprocess.run(
        [
            "quarto", "pandoc", "--from", "html", "--to", PANDOC_OUTPUT_FORMAT, "--wrap=none", "--eol=lf",
            "--lua-filter", str(quarto_filter), "--lua-filter", str(LUA_FILTER), "--output", str(twin_path),
        ],
        input=document,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc could not convert {page_path}: {result.stderr}")
    return True


def _add_alternate_link(page_path: Path) -> None:
    """Advertise the twin in the page head, for agents that read <link> tags."""
    link = f'<link rel="alternate" type="text/markdown" href="{quote(page_path.stem + TWIN_SUFFIX)}">'
    content = page_path.read_text(encoding="utf-8")
    if link in content:
        return
    updated = content.replace("</head>", f"{link}\n</head>", 1)
    if updated == content:
        raise ValueError(f"{page_path} has no </head>")
    page_path.write_text(updated, encoding="utf-8", newline="\n")


def _link_llms_txt_to_twins(site_dir: Path, site_url: str) -> int:
    """Point llms.txt links for pages of this site at their twins. Returns the link count."""
    llms_txt = site_dir / "llms.txt"
    if not site_url or not llms_txt.is_file():
        return 0
    link_pattern = re.compile(r"\]\((" + re.escape(site_url.rstrip("/")) + r")(/[^)\s]*)?\)", re.IGNORECASE)
    linked = 0

    def to_twin(match: re.Match[str]) -> str:
        nonlocal linked
        page = (match.group(2) or "").lstrip("/") or "index.html"
        twin = page.removesuffix(".html") + TWIN_SUFFIX
        if not page.endswith(".html") or not (site_dir / twin).is_file():
            return match.group(0)
        linked += 1
        return f"]({match.group(1)}/{twin})"

    llms_txt.write_text(link_pattern.sub(to_twin, llms_txt.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
    return linked


def write_markdown_twins(site_dir: Path, site_url: str = "") -> Dict[str, int]:
    """Write page.llms.md for every Quarto page under site_dir, link it, and list it in llms.txt."""
    quarto_filter = _quarto_llms_filter()
    candidates = [
        path
        for path in sorted(site_dir.rglob("*.html"))
        if path.name != "404.html"
        and "site_libs" not in path.relative_to(site_dir).parts
        and _MAIN_MARKER in path.read_text(encoding="utf-8", errors="replace")
    ]
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        written = list(pool.map(lambda page: _write_twin(page, quarto_filter), candidates))
    pages = [page for page, ok in zip(candidates, written) if ok]
    for page in pages:
        _add_alternate_link(page)
    return {"twins": len(pages), "llms_txt_links": _link_llms_txt_to_twins(site_dir, site_url)}
