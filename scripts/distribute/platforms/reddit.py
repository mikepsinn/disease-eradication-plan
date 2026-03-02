#!/usr/bin/env python3
"""
Reddit Platform
===============

Posts to Reddit subreddits using PRAW.

Required env vars:
    REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET
    REDDIT_USERNAME
    REDDIT_PASSWORD
    REDDIT_SUBREDDITS     (comma-separated, e.g., "healthpolicy,publichealth,science")

Install: pip install praw
"""

import os
from typing import Dict


def is_configured() -> bool:
    return all(os.environ.get(k) for k in [
        "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET",
        "REDDIT_USERNAME", "REDDIT_PASSWORD",
    ])


def post(content: Dict) -> bool:
    """Post a link to configured subreddits. Returns True if at least one succeeds."""
    try:
        import praw
    except ImportError:
        print("      [!] pip install praw")
        return False

    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent="WarOnDisease-Distributor/1.0",
    )

    subreddits = os.environ.get("REDDIT_SUBREDDITS", "healthpolicy").split(",")
    success = False

    for sub_name in subreddits:
        sub_name = sub_name.strip()
        if not sub_name:
            continue
        try:
            subreddit = reddit.subreddit(sub_name)
            subreddit.submit(
                title=content["title"],
                url=content["url"],
            )
            print(f"      r/{sub_name}: posted")
            success = True
        except Exception as e:
            print(f"      r/{sub_name}: failed ({e})")

    return success
