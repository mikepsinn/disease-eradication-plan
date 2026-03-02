#!/usr/bin/env python3
"""
Telegram Platform
=================

Posts to a Telegram channel/group via Bot API. No library needed.

Required env vars:
    TELEGRAM_BOT_TOKEN   (from @BotFather)
    TELEGRAM_CHAT_ID     (channel @username or numeric chat ID)

Setup:
    1. Message @BotFather on Telegram, /newbot
    2. Get the bot token
    3. Add bot to your channel as admin
    4. Chat ID: use @username for public channels, or get numeric ID via getUpdates API
"""

import json
import os
import urllib.request
from typing import Dict


def is_configured() -> bool:
    return all(os.environ.get(k) for k in ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"])


def post(content: Dict) -> bool:
    """Post to Telegram. Returns True on success."""
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    # Telegram supports HTML formatting
    text = (
        f"<b>{_escape_html(content['title'])}</b>\n\n"
        f"{_escape_html(content['description'])}\n\n"
        f"<a href=\"{content['url']}\">Read more</a>"
    )

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,  # Show link preview
    }

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    response = urllib.request.urlopen(req)
    result = json.loads(response.read())
    return result.get("ok", False)


def _escape_html(text: str) -> str:
    """Escape HTML special chars for Telegram."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
