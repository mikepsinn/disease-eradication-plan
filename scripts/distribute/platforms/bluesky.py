#!/usr/bin/env python3
"""
Bluesky Platform
================

Posts to Bluesky using the AT Protocol.

Required env vars:
    BLUESKY_HANDLE       (e.g., warondisease.bsky.social)
    BLUESKY_APP_PASSWORD (generate at https://bsky.app/settings/app-passwords)

Install: pip install atproto
"""

import os
from typing import Dict


def is_configured() -> bool:
    return all(os.environ.get(k) for k in ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"])


def _create_link_facet(text: str, url: str, byte_start: int, byte_end: int) -> dict:
    """Create an AT Protocol link facet for rich text."""
    return {
        "index": {"byteStart": byte_start, "byteEnd": byte_end},
        "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}],
    }


def post(content: Dict) -> bool:
    """Post to Bluesky. Returns True on success."""
    try:
        from atproto import Client
    except ImportError:
        print("      [!] pip install atproto")
        return False

    client = Client()
    client.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_APP_PASSWORD"])

    text = content["short_post"]

    # Build facets for the URL so it's clickable
    url = content["url"]
    facets = []
    url_start = text.encode("utf-8").find(url.encode("utf-8"))
    if url_start >= 0:
        url_end = url_start + len(url.encode("utf-8"))
        facets.append(_create_link_facet(text, url, url_start, url_end))

    # Add hashtag facets
    for tag in content["hashtags"][:2]:
        hashtag = f"#{tag}"
        tag_pos = text.encode("utf-8").find(hashtag.encode("utf-8"))
        if tag_pos >= 0:
            facets.append({
                "index": {"byteStart": tag_pos, "byteEnd": tag_pos + len(hashtag.encode("utf-8"))},
                "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": tag}],
            })

    # Create post with external embed (link card)
    embed = {
        "$type": "app.bsky.embed.external",
        "external": {
            "uri": url,
            "title": content["title"],
            "description": content["description"][:300] if content["description"] else "",
        },
    }

    client.send_post(text=text, facets=facets if facets else None, embed=embed)  # pyright: ignore[reportArgumentType]
    return True
