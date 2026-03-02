#!/usr/bin/env python3
"""
RSS Feed Generator
==================

Generates an RSS 2.0 feed from book chapters that have a `feed-date`
field in their YAML frontmatter. Only chapters with feed-date are
included, giving full editorial control over what appears in the feed.

Usage:
    from dih_models.feed_generator import generate_rss_feed
    generate_rss_feed(project_root)

Output:
    assets/feed.xml
"""

import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.sax.saxutils import escape

from dih_models.yaml_utils import load_quarto_config

logger = logging.getLogger("dih.feed")


def _parse_frontmatter(qmd_path: Path) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from a QMD file."""
    try:
        text = qmd_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    # Minimal YAML parsing for the fields we need
    fm: Dict[str, Any] = {}
    for line in match.group(1).splitlines():
        # Match simple key: value pairs (not nested)
        kv = re.match(r"^(\w[\w-]*)\s*:\s*(.+)$", line)
        if kv:
            key = kv.group(1)
            val = kv.group(2).strip().strip("'\"")
            fm[key] = val
    return fm


def _extract_chapters(config: Dict[str, Any]) -> List[str]:
    """Extract all chapter .qmd paths from a Quarto book config."""
    chapters = []
    book = config.get("book", {})

    def _walk(items):
        if not items:
            return
        for item in items:
            if isinstance(item, str):
                if item.endswith(".qmd"):
                    chapters.append(item)
            elif isinstance(item, dict):
                if "href" in item and item["href"].endswith(".qmd"):
                    chapters.append(item["href"])
                _walk(item.get("chapters", []))
                _walk(item.get("contents", []))

    _walk(book.get("chapters", []))
    return chapters


def _date_to_rfc822(date_str: str) -> str:
    """Convert YYYY-MM-DD to RFC 822 date string."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def generate_rss_feed(project_root: Path) -> Path:
    """
    Generate assets/feed.xml from chapters with feed-date frontmatter.

    Returns:
        Path to the generated feed.xml file
    """
    config = load_quarto_config(project_root / "_quarto-manual.yml")
    book = config.get("book", {})
    site_url = book.get("site-url", "https://manual.WarOnDisease.org")
    book_title = book.get("title", "How to End War and Disease")
    book_desc = book.get("description", "")

    chapter_paths = _extract_chapters(config)
    entries: List[Dict[str, str]] = []

    for rel_path in chapter_paths:
        qmd_path = project_root / rel_path
        if not qmd_path.exists():
            continue

        fm = _parse_frontmatter(qmd_path)
        if not fm or "feed-date" not in fm:
            continue
        if fm["feed-date"] in ("false", "False", "no", "No"):
            continue

        title = fm.get("title", qmd_path.stem)
        description = fm.get("description", "")
        feed_date = fm["feed-date"]

        # Strip Quarto shortcodes ({{< var ... >}}) from title/description
        # since RSS readers show raw text, not rendered output
        shortcode_re = r"\{\{<[^>]+>\}\}"
        title = re.sub(shortcode_re, "", title).strip()
        description = re.sub(shortcode_re, "", description).strip()

        # Build URL: knowledge/solution/1-percent-treaty.qmd -> /knowledge/solution/1-percent-treaty.html
        html_path = rel_path.replace(".qmd", ".html")
        url = f"{site_url}/{html_path}"

        entries.append({
            "title": title,
            "description": description,
            "url": url,
            "date": feed_date,
        })

    # Only include entries whose date has arrived (no future items)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entries = [e for e in entries if e["date"] <= today]

    # Sort by date descending (newest first)
    entries.sort(key=lambda e: e["date"], reverse=True)

    latest_date = entries[0]["date"] if entries else today

    items_xml = []
    for entry in entries:
        items_xml.append(f"""    <item>
      <title>{escape(entry['title'])}</title>
      <link>{escape(entry['url'])}</link>
      <guid>{escape(entry['url'])}</guid>
      <description>{escape(entry['description'])}</description>
      <pubDate>{_date_to_rfc822(entry['date'])}</pubDate>
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(book_title)}</title>
    <link>{escape(site_url)}</link>
    <description>{escape(book_desc)}</description>
    <language>en-us</language>
    <lastBuildDate>{_date_to_rfc822(latest_date)}</lastBuildDate>
    <atom:link href="{escape(site_url)}/assets/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items_xml)}
  </channel>
</rss>
"""

    output_path = project_root / "assets" / "feed.xml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(feed, encoding="utf-8")

    logger.debug("Generated %s with %d entries", output_path.relative_to(project_root), len(entries))
    return output_path


def main():
    """CLI entry point."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    project_root = Path(__file__).parent.parent.absolute()
    output_path = generate_rss_feed(project_root)
    print(f"Generated {output_path} with RSS feed")


if __name__ == "__main__":
    main()
