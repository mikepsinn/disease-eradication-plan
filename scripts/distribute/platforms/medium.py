#!/usr/bin/env python3
"""
Medium Platform
===============

Creates draft posts on Medium via their API.

Required env vars:
    MEDIUM_TOKEN    (integration token from https://medium.com/me/settings/security)

Note: Medium's API is officially deprecated but still functional.
Posts are created as drafts so you can review before publishing.
"""

import json
import os
import urllib.request
from typing import Dict


def is_configured() -> bool:
    return bool(os.environ.get("MEDIUM_TOKEN"))


def _get_user_id(token: str) -> str:
    """Get the authenticated user's Medium ID."""
    req = urllib.request.Request(
        "https://api.medium.com/v1/me",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    return data["data"]["id"]


def post(content: Dict) -> bool:
    """Create a Medium draft post. Returns True on success."""
    token = os.environ["MEDIUM_TOKEN"]
    user_id = _get_user_id(token)

    # Medium accepts HTML content
    html_body = (
        f"<p>{_escape_html(content['description'])}</p>"
        f"<p><a href=\"{content['url']}\">Read the full chapter</a></p>"
        f"<p><em>From <a href=\"https://manual.WarOnDisease.org\">How to End War and Disease</a></em></p>"
    )

    payload = {
        "title": content["title"],
        "contentFormat": "html",
        "content": html_body,
        "canonicalUrl": content["url"],
        "tags": content["hashtags"][:5],
        "publishStatus": "draft",  # Review before publishing
    }

    url = f"https://api.medium.com/v1/users/{user_id}/posts"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    response = urllib.request.urlopen(req)
    result = json.loads(response.read())
    return "data" in result


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
