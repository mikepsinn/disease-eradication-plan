#!/usr/bin/env python3
"""
Twitter/X Platform
==================

Posts to Twitter/X using the v2 API via tweepy.

Required env vars:
    TWITTER_API_KEY
    TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_SECRET

Install: pip install tweepy
"""

import os
from typing import Dict


def is_configured() -> bool:
    return all(os.environ.get(k) for k in [
        "TWITTER_API_KEY", "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET",
    ])


def post(content: Dict) -> bool:
    """Post a tweet. Returns True on success."""
    try:
        import tweepy
    except ImportError:
        print("      [!] pip install tweepy")
        return False

    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
    )

    text = content["short_post"]

    # Add hashtags if they fit
    tags = " ".join(f"#{t}" for t in content["hashtags"][:2])
    if len(text) + len(tags) + 2 <= 280:
        text = f"{text}\n\n{tags}"

    response = client.create_tweet(text=text)
    return response.data is not None
