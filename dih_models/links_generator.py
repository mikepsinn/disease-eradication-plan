#!/usr/bin/env python3
"""
Links Page Generator
====================

Generates knowledge/links.qmd (Linktree-style page) from YAML config data.
Reads book distribution links from _quarto-manual.yml and social/action
links from _quarto-shared-defaults.yml.

Usage:
    from dih_models.links_generator import generate_links_qmd
    generate_links_qmd(project_root)

Output:
    knowledge/links.qmd
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from dih_models.yaml_utils import load_quarto_config

logger = logging.getLogger("dih.links")

# CSS for the Linktree-style page (kept in generator so the whole page is one source)
LINKS_CSS = """\
.links-page {
  max-width: 640px;
  margin: 0 auto;
  padding: 2rem 1rem;
  text-align: center;
}
.links-page h2 {
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #666;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;
}
.links-page .hero-img {
  max-width: 280px;
  margin: 0 auto 1.5rem;
  border-radius: 4px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.links-page .tagline {
  font-size: 1rem;
  color: #555;
  margin-bottom: 2rem;
  line-height: 1.5;
}
.link-btn {
  display: block;
  padding: 1rem 1.5rem;
  margin: 0.6rem 0;
  border-radius: 8px;
  text-decoration: none !important;
  font-size: 1.05rem;
  font-weight: 600;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  border: 2px solid #222;
  color: #222 !important;
  background: #fff;
}
.link-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.link-btn .btn-sub {
  display: block;
  font-size: 0.82rem;
  font-weight: 400;
  color: #777;
  margin-top: 0.15rem;
}
.link-btn.primary {
  background: #222;
  color: #fff !important;
  border-color: #222;
}
.link-btn.primary .btn-sub {
  color: #bbb;
}
.link-btn.primary:hover {
  background: #333;
}"""


def _render_link(link: Dict[str, Any]) -> str:
    """Render a single link button."""
    url = link["url"]
    label = link["label"]
    primary = link.get("primary", False)
    subtitle = link.get("subtitle", "")

    # Escape @ in URLs and subtitle text so Pandoc doesn't interpret as citation references
    url_escaped = url.replace("@", "&#64;")
    subtitle_escaped = subtitle.replace("@", "&#64;") if subtitle else ""

    cls = "link-btn primary" if primary else "link-btn"
    sub_html = f'\n  <span class="btn-sub">{subtitle_escaped}</span>' if subtitle_escaped else ""
    return f'<a href="{url_escaped}" class="{cls}">\n  {label}{sub_html}\n</a>'


def _render_section(heading: str, links: List[Dict[str, Any]]) -> str:
    """Render a section with heading and link buttons."""
    if not links:
        return ""
    buttons = "\n\n".join(_render_link(link) for link in links)
    return f"<h2>{heading}</h2>\n\n{buttons}"


def _load_configs(project_root: Path):
    """Load manual and shared YAML configs. Returns (manual_config, shared_config)."""
    manual_config = load_quarto_config(project_root / "_quarto-manual.yml")
    shared_config = load_quarto_config(project_root / "_quarto-shared-defaults.yml")
    return manual_config, shared_config


def generate_links_qmd(project_root: Path) -> Path:
    """
    Generate knowledge/links.qmd from YAML config data.

    Reads:
      - _quarto-manual.yml: links.read, links.buy, links.listen
      - _quarto-shared-defaults.yml: links.action, links.follow

    Returns:
        Path to the generated knowledge/links.qmd file
    """
    manual_config, shared_config = _load_configs(project_root)

    manual_links = manual_config.get("links", {})
    shared_links = shared_config.get("links", {})

    # Get book metadata for hero section
    book = manual_config.get("book", {})
    subtitle = book.get("subtitle", "")

    sections = [
        ("Take Action", shared_links.get("action", [])),
        ("Buy", manual_links.get("buy", [])),
        ("Read", manual_links.get("read", [])),
        ("Listen", manual_links.get("listen", [])),
        ("Follow", shared_links.get("follow", [])),
    ]

    sections_html = "\n\n".join(
        _render_section(heading, links)
        for heading, links in sections
        if links
    )

    content = f"""---
title: "Get the Manual"
description: "Read, buy, or listen to 'How to End War and Disease' - available free online, in print, ebook, and audiobook."
published: true
feed-date: false
page-layout: full
toc: false
aliases:
  - /links
---

```{{=html}}
<style>
{LINKS_CSS}
</style>

<div class="links-page">

<img src="/assets/cover/book-cover-3.jpg" alt="How to End War and Disease - Book Cover" class="hero-img">

<div class="tagline">
  {subtitle}
</div>

{sections_html}

</div>
```
"""

    output_path = project_root / "knowledge" / "links.qmd"
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    logger.debug("Generated %s", output_path.name)

    # Also generate the podcast page
    generate_podcast_qmd(project_root, manual_config)

    return output_path


def generate_podcast_qmd(project_root: Path, manual_config: Optional[Dict] = None) -> Path:
    """
    Generate knowledge/podcast.qmd with all podcast platform links.

    Reads links.podcast from _quarto-manual.yml and adds buy links as a
    conversion footer.

    Returns:
        Path to the generated knowledge/podcast.qmd file
    """
    if manual_config is None:
        manual_config = load_quarto_config(project_root / "_quarto-manual.yml")

    manual_links = manual_config.get("links", {})
    podcast_links = manual_links.get("podcast", [])
    buy_links = manual_links.get("buy", [])

    podcast_html = "\n\n".join(_render_link(link) for link in podcast_links)
    buy_html = "\n\n".join(_render_link(link) for link in buy_links[:2])  # Just top 2 buy links

    content = f"""---
title: "Listen to How to End War and Disease"
description: "Free audiobook podcast. Every chapter narrated. Available on Spotify, Apple Podcasts, YouTube Music, and all major podcast apps."
published: true
feed-date: false
page-layout: full
toc: false
aliases:
  - /podcast
---

```{{=html}}
<style>
{LINKS_CSS}
</style>

<div class="links-page">

<img src="/assets/cover/book-cover-3.jpg" alt="How to End War and Disease - Book Cover" class="hero-img">

<div class="tagline">
  Every chapter narrated. Free on all major podcast apps.
</div>

<h2>Listen</h2>

{podcast_html}

<h2>Prefer to Read?</h2>

<a href="https://manual.WarOnDisease.org" class="link-btn primary">
  Read Online
  <span class="btn-sub">Full manual, free, no account needed</span>
</a>

{buy_html}

</div>
```
"""

    output_path = project_root / "knowledge" / "podcast.qmd"
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    logger.debug("Generated %s", output_path.name)
    return output_path


def main():
    """CLI entry point."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    project_root = Path(__file__).parent.parent.absolute()
    output_path = generate_links_qmd(project_root)
    logger.debug("Output: %s", output_path)


if __name__ == "__main__":
    main()
