#!/usr/bin/env python3
"""
Discord Platform
================

Posts to a Discord channel via webhook. No library needed.

Required env vars:
    DISCORD_WEBHOOK_URL

Setup: Server Settings > Integrations > Webhooks > New Webhook > Copy URL
"""

import json
import os
import urllib.request
from typing import Dict


def is_configured() -> bool:
    return bool(os.environ.get("DISCORD_WEBHOOK_URL"))


def post(content: Dict) -> bool:
    """Post to Discord webhook. Returns True on success."""
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    # Discord embed for a rich card
    payload = {
        "embeds": [{
            "title": content["title"],
            "description": content["description"][:2048] if content["description"] else "",
            "url": content["url"],
            "color": 0x2F3136,
            "footer": {"text": "War on Disease"},
        }],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    response = urllib.request.urlopen(req)
    return response.status in (200, 204)
