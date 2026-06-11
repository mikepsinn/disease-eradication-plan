#!/usr/bin/env python3
"""
Content Distributor
===================

Reads the RSS feed, finds entries ready to post (feed-date <= today,
not yet posted), and distributes them to all configured platforms.

Tracks posted items in scripts/distribute/posted.json to prevent
double-posting.

Usage:
    python scripts/distribute/distributor.py              # Post today's entries
    python scripts/distribute/distributor.py --dry-run    # Preview without posting
    python scripts/distribute/distributor.py --backfill   # Post all past entries not yet posted
    python scripts/distribute/distributor.py --platform twitter  # Post to one platform only

Environment variables (set in .env):
    See scripts/distribute/platforms/*.py for per-platform requirements.

Designed to run as a daily cron job or GitHub Action.
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # pyright: ignore[reportAttributeAccessIssue]

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
FEED_PATH = PROJECT_ROOT / "assets" / "feed.xml"
POSTED_PATH = Path(__file__).parent / "posted.json"
PLATFORMS_DIR = Path(__file__).parent / "platforms"

# Dynamic platform loading - import all modules from platforms/
import importlib.util

def _load_platform(name: str):
    """Load a platform module by name."""
    mod_path = PLATFORMS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"platforms.{name}", mod_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load platform module: {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_platform_names = [p.stem for p in PLATFORMS_DIR.glob("*.py") if p.stem != "__init__"]
_platform_modules = {name: _load_platform(name) for name in _platform_names}

PLATFORMS = {
    name: {"post": mod.post, "configured": mod.is_configured}
    for name, mod in _platform_modules.items()
}


def load_posted() -> Dict:
    """Load the posted tracking file."""
    if POSTED_PATH.exists():
        return json.loads(POSTED_PATH.read_text(encoding="utf-8"))
    return {}


def save_posted(data: Dict):
    """Save the posted tracking file."""
    POSTED_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_feed() -> List[Dict]:
    """Parse the RSS feed and return entries as dicts."""
    if not FEED_PATH.exists():
        print(f"[ERROR] Feed not found: {FEED_PATH}")
        return []

    tree = ET.parse(str(FEED_PATH))
    entries = []

    for item in tree.findall(".//item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        description = item.findtext("description", "")
        pub_date_str = item.findtext("pubDate", "")

        # Parse RFC 822 date -> YYYY-MM-DD
        if pub_date_str:
            dt = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
            date_str = dt.strftime("%Y-%m-%d")
        else:
            continue

        entries.append({
            "title": title,
            "url": link,
            "description": description,
            "date": date_str,
            "guid": link,
        })

    return entries


def get_ready_entries(entries: List[Dict], posted: Dict, backfill: bool = False) -> List[Dict]:
    """Filter to entries that are ready to post and haven't been posted yet."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ready = []

    for entry in entries:
        # Only include entries whose date has arrived
        if entry["date"] > today:
            continue

        # If not backfilling, only include today's entry
        if not backfill and entry["date"] != today:
            continue

        ready.append(entry)

    return ready


def format_post(entry: Dict) -> Dict:
    """Format an entry into platform-agnostic post content."""
    title = entry["title"]
    description = entry["description"]
    url = entry["url"]

    # Short post (Twitter, Bluesky): description + URL
    # If description is too long, truncate for Twitter's 280 char limit
    short_text = description if description else title
    if len(short_text) + len(url) + 2 > 275:
        short_text = short_text[:275 - len(url) - 5] + "..."
    short_post = f"{short_text}\n\n{url}"

    # Long post (Medium, Reddit, LinkedIn): title + description + URL
    long_post = f"{title}\n\n{description}\n\n{url}" if description else f"{title}\n\n{url}"

    return {
        "title": title,
        "description": description,
        "url": url,
        "short_post": short_post,
        "long_post": long_post,
        "hashtags": ["WarOnDisease", "EndDisease", "ClinicalTrials"],
    }


def distribute(
    entries: List[Dict],
    platforms: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict[str, List[str]]:
    """
    Distribute entries to configured platforms.
    Returns dict of {platform: [posted_guids]}.
    """
    posted = load_posted()
    results: Dict[str, List[str]] = {}

    # Filter to requested platforms
    active_platforms = {}
    for name, funcs in PLATFORMS.items():
        if platforms and name not in platforms:
            continue
        if funcs["configured"]():
            active_platforms[name] = funcs
        else:
            if not platforms:
                pass  # Silent skip for unconfigured platforms in auto mode
            else:
                print(f"  [{name.upper()}] Not configured (missing env vars)")

    if not active_platforms:
        print("\n[WARN] No platforms configured. Set environment variables in .env:")
        print("  Twitter:  TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET")
        print("  Bluesky:  BLUESKY_HANDLE, BLUESKY_APP_PASSWORD")
        print("  Reddit:   REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD")
        print("  Discord:  DISCORD_WEBHOOK_URL")
        print("  Telegram: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        print("  LinkedIn: LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN")
        return results

    for entry in entries:
        content = format_post(entry)
        guid = entry["guid"]

        print(f"\n  [{entry['date']}] {entry['title']}")

        for name, funcs in active_platforms.items():
            # Check if already posted to this platform
            platform_posted = posted.get(name, [])
            if guid in platform_posted:
                print(f"    [{name.upper()}] Already posted, skipping")
                continue

            if dry_run:
                print(f"    [{name.upper()}] Would post: {content['short_post'][:80]}...")
            else:
                success = funcs["post"](content)
                if success:
                    print(f"    [{name.upper()}] Posted")
                    if name not in posted:
                        posted[name] = []
                    posted[name].append(guid)
                    results.setdefault(name, []).append(guid)
                else:
                    print(f"    [{name.upper()}] FAILED")

    if not dry_run:
        save_posted(posted)

    return results


def main():
    parser = argparse.ArgumentParser(description="Distribute RSS feed entries to social platforms")
    parser.add_argument("--dry-run", action="store_true", help="Preview without posting")
    parser.add_argument("--backfill", action="store_true", help="Post all past entries not yet posted")
    parser.add_argument("--platform", type=str, help="Post to a single platform only")
    args = parser.parse_args()

    # Load .env if python-dotenv is available
    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass

    print("Content Distributor")
    print("=" * 40)

    entries = parse_feed()
    if not entries:
        print("No entries in feed.")
        return

    posted = load_posted()
    platforms = [args.platform] if args.platform else None

    ready = get_ready_entries(entries, posted, backfill=args.backfill)
    if not ready:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"No entries ready for {today}.")
        next_entries = [e for e in entries if e["date"] > today]
        if next_entries:
            next_entries.sort(key=lambda e: e["date"])
            print(f"Next entry: {next_entries[0]['title']} on {next_entries[0]['date']}")
        return

    print(f"{len(ready)} entries ready to distribute")
    if args.dry_run:
        print("(dry run)")

    results = distribute(ready, platforms=platforms, dry_run=args.dry_run)

    if results:
        total = sum(len(v) for v in results.values())
        print(f"\nPosted {total} items across {len(results)} platforms")
    elif not args.dry_run:
        print("\nNo new items posted")


if __name__ == "__main__":
    main()
