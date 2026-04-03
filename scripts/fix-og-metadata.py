#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Open Graph and Twitter Card metadata in rendered HTML files.

Quarto uses the book-level description for og:description on every page instead
of the page-level description. This script fixes that and adds missing social
media meta tags (Twitter Cards, og:url, og:type, author).

Runs as a post-render step in the build pipeline (render-quarto.py).

Usage:
    python scripts/fix-og-metadata.py <output-dir> [--site-url URL] [--twitter-site HANDLE]

Examples:
    python scripts/fix-og-metadata.py _manual/warondisease
    python scripts/fix-og-metadata.py _manual/warondisease --site-url https://manual.WarOnDisease.org
"""

import argparse
import io
import os
import re
import sys
from pathlib import Path

if sys.platform == 'win32':
    _stdout = sys.stdout
    if isinstance(_stdout, io.TextIOWrapper):
        _stdout.reconfigure(encoding='utf-8')

# Default values
DEFAULT_SITE_URL = "https://manual.WarOnDisease.org"
DEFAULT_TWITTER_SITE = "@warondisease"
DEFAULT_AUTHOR = "Mike P. Sinn"


def extract_meta(html: str, attr: str, value: str) -> str | None:
    """Extract content from a meta tag matching attr=value."""
    pattern = rf'<meta\s+(?:[^>]*?){attr}="{re.escape(value)}"[^>]*?content="([^"]*)"'
    match = re.search(pattern, html, re.IGNORECASE)
    if match:
        return match.group(1)
    # Try reversed order (content before property)
    pattern2 = rf'<meta\s+content="([^"]*)"[^>]*?{attr}="{re.escape(value)}"'
    match2 = re.search(pattern2, html, re.IGNORECASE)
    if match2:
        return match2.group(1)
    return None


def has_meta(html: str, attr: str, value: str) -> bool:
    """Check if a meta tag with attr=value exists."""
    return extract_meta(html, attr, value) is not None


def replace_meta_content(html: str, attr: str, value: str, new_content: str) -> str:
    """Replace the content of a meta tag matching attr=value."""
    # Escape backslashes in replacement to prevent re.sub interpreting them
    safe_content = new_content.replace("\\", "\\\\")
    pattern = rf'(<meta\s+(?:[^>]*?){attr}="{re.escape(value)}"[^>]*?content=")([^"]*?)(")'
    result, count = re.subn(pattern, rf'\g<1>{safe_content}\3', html, count=1, flags=re.IGNORECASE)
    if count:
        return result
    # Try reversed order
    pattern2 = rf'(<meta\s+content=")([^"]*?)("[^>]*?{attr}="{re.escape(value)}")'
    result2, count2 = re.subn(pattern2, rf'\g<1>{safe_content}\3', html, count=1, flags=re.IGNORECASE)
    if count2:
        return result2
    return html


def insert_meta_after(html: str, anchor_attr: str, anchor_value: str, new_tag: str) -> str:
    """Insert a new meta tag after the tag matching anchor_attr=anchor_value."""
    # Find the anchor tag
    pattern = rf'(<meta\s+[^>]*?{anchor_attr}="{re.escape(anchor_value)}"[^>]*?>)'
    match = re.search(pattern, html, re.IGNORECASE)
    if match:
        insert_pos = match.end()
        return html[:insert_pos] + "\n" + new_tag + html[insert_pos:]
    return html


def get_relative_path(html_file: Path, output_dir: Path) -> str:
    """Get the URL path relative to the site root."""
    rel = html_file.relative_to(output_dir)
    # Convert to forward slashes and normalize
    url_path = "/" + str(rel).replace("\\", "/")
    # Strip index.html from the end
    if url_path.endswith("/index.html"):
        url_path = url_path[:-len("index.html")]
    return url_path


def fix_html_file(html_file: Path, output_dir: Path, site_url: str,
                  twitter_site: str, author: str) -> dict:
    """Fix OG and Twitter metadata in a single HTML file. Returns change summary."""
    changes = []

    html = html_file.read_text(encoding="utf-8")

    # Only process files with a <head> section
    if "<head>" not in html and "<head " not in html:
        return {"file": str(html_file), "changes": []}

    original = html

    # --- Extract existing values ---
    page_description = extract_meta(html, "name", "description")
    og_description = extract_meta(html, "property", "og:description")
    og_title = extract_meta(html, "property", "og:title")
    og_image = extract_meta(html, "property", "og:image")
    og_site_name = extract_meta(html, "property", "og:site_name")

    # Determine the page URL path
    url_path = get_relative_path(html_file, output_dir)
    is_index = url_path == "/" or url_path.endswith("/index.html")
    canonical_url = site_url.rstrip("/") + url_path

    # --- 1. Fix og:description to use page description ---
    if page_description and og_description and page_description != og_description:
        html = replace_meta_content(html, "property", "og:description", page_description)
        changes.append(f"og:description: {og_description[:50]}... -> {page_description[:50]}...")

    # --- 2. Add og:url ---
    if not has_meta(html, "property", "og:url"):
        anchor = "og:site_name" if has_meta(html, "property", "og:site_name") else "og:title"
        tag = f'<meta property="og:url" content="{canonical_url}">'
        html = insert_meta_after(html, "property", anchor, tag)
        changes.append(f"og:url: {canonical_url}")

    # --- 3. Add og:type ---
    if not has_meta(html, "property", "og:type"):
        og_type = "website" if is_index else "article"
        anchor = "og:site_name" if has_meta(html, "property", "og:site_name") else "og:title"
        tag = f'<meta property="og:type" content="{og_type}">'
        html = insert_meta_after(html, "property", anchor, tag)
        changes.append(f"og:type: {og_type}")

    # --- 4. Add Twitter Card tags ---
    if not has_meta(html, "name", "twitter:card"):
        # Insert all twitter tags after the last og: tag
        twitter_tags = []
        twitter_tags.append(f'<meta name="twitter:card" content="summary_large_image">')

        if og_title and not has_meta(html, "name", "twitter:title"):
            twitter_tags.append(f'<meta name="twitter:title" content="{og_title}">')

        tw_desc = page_description or og_description
        if tw_desc and not has_meta(html, "name", "twitter:description"):
            # Escape any HTML entities in the description
            tw_desc_escaped = tw_desc.replace('"', '&quot;')
            twitter_tags.append(f'<meta name="twitter:description" content="{tw_desc_escaped}">')

        if og_image and not has_meta(html, "name", "twitter:image"):
            twitter_tags.append(f'<meta name="twitter:image" content="{og_image}">')

        if twitter_site and not has_meta(html, "name", "twitter:site"):
            twitter_tags.append(f'<meta name="twitter:site" content="{twitter_site}">')

        # Find last og: tag to insert after
        last_og = None
        for m in re.finditer(r'<meta\s+property="og:[^"]*"[^>]*>', html, re.IGNORECASE):
            last_og = m
        if not last_og:
            for m in re.finditer(r'<meta\s+[^>]*property="og:[^"]*"[^>]*>', html, re.IGNORECASE):
                last_og = m

        if last_og:
            insert_pos = last_og.end()
            twitter_block = "\n".join(twitter_tags)
            html = html[:insert_pos] + "\n" + twitter_block + html[insert_pos:]
            changes.append(f"twitter:card + {len(twitter_tags) - 1} twitter tags")

    # --- 5. Add meta author if missing ---
    if not has_meta(html, "name", "author") and author:
        # Insert after description
        if has_meta(html, "name", "description"):
            tag = f'<meta name="author" content="{author}">'
            html = insert_meta_after(html, "name", "description", tag)
            changes.append(f"author: {author}")

    # --- Write if changed ---
    if html != original:
        html_file.write_text(html, encoding="utf-8")

    return {"file": str(html_file.relative_to(output_dir)), "changes": changes}


def fix_og_metadata(output_dir: str, site_url: str = DEFAULT_SITE_URL,
                    twitter_site: str = DEFAULT_TWITTER_SITE,
                    author: str = DEFAULT_AUTHOR) -> int:
    """Fix OG metadata in all HTML files. Returns count of files modified."""
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"[ERROR] Output directory not found: {output_dir}", file=sys.stderr)
        return 0

    html_files = sorted(output_path.rglob("*.html"))
    if not html_files:
        print(f"[WARN] No HTML files found in {output_dir}", file=sys.stderr)
        return 0

    modified = 0
    total_changes = 0

    for html_file in html_files:
        # Skip site_libs and other non-content files
        rel = str(html_file.relative_to(output_path))
        if "site_libs" in rel or "libs" in rel:
            continue

        result = fix_html_file(html_file, output_path, site_url, twitter_site, author)
        if result["changes"]:
            modified += 1
            total_changes += len(result["changes"])
            for change in result["changes"]:
                print(f"  {result['file']}: {change}")

    print(f"[*] Fixed OG/Twitter metadata: {modified} files, {total_changes} changes")
    return modified


def main():
    parser = argparse.ArgumentParser(description="Fix OG and Twitter Card metadata in rendered HTML")
    parser.add_argument("output_dir", help="Directory containing rendered HTML files")
    parser.add_argument("--site-url", default=DEFAULT_SITE_URL, help="Site base URL")
    parser.add_argument("--twitter-site", default=DEFAULT_TWITTER_SITE, help="Twitter handle")
    parser.add_argument("--author", default=DEFAULT_AUTHOR, help="Author name")
    args = parser.parse_args()

    fix_og_metadata(args.output_dir, args.site_url, args.twitter_site, args.author)


if __name__ == "__main__":
    main()
