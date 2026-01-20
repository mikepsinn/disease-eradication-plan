#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Netlify Site Setup Script

Scans _quarto-*.yml configs, creates Netlify sites for any missing site IDs,
and saves the site IDs back to the configs.

Usage:
    python scripts/setup-netlify-sites.py           # Create missing sites
    python scripts/setup-netlify-sites.py --list    # List all configs and their site status
    python scripts/setup-netlify-sites.py iab       # Create site for specific config only

Environment:
    NETLIFY_AUTH_TOKEN: Personal access token from https://app.netlify.com/user/applications#personal-access-tokens

The script will:
1. Scan all _quarto-*.yml files in project root
2. Check for existing netlify-site-id in dih-render section
3. Create new Netlify sites for configs without site IDs
4. Use config name as subdomain (e.g., iab -> iab.warondisease.org)
5. Save site ID back to the config file
6. Regenerate GitHub Actions workflow
"""

from __future__ import annotations

import os
import sys
import io
import re
import argparse
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import yaml
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install pyyaml requests python-dotenv")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent.parent
BASE_DOMAIN = "warondisease.org"
SKIP_CONFIGS = {"book", "test"}  # book uses main site, test doesn't need deployment

# Netlify API
NETLIFY_API = "https://api.netlify.com/api/v1"


def get_netlify_token() -> str | None:
    """Get Netlify auth token from environment."""
    load_dotenv(PROJECT_ROOT / ".env")
    return os.environ.get("NETLIFY_AUTH_TOKEN")


def get_netlify_team_slug(token: str) -> str | None:
    """Get the user's Netlify team slug."""
    resp = requests.get(
        f"{NETLIFY_API}/accounts",
        headers={"Authorization": f"Bearer {token}"}
    )
    if resp.status_code == 200:
        accounts = resp.json()
        if accounts:
            return accounts[0].get("slug")
    return None


def create_netlify_site(token: str, config_name: str, title: str) -> dict | None:
    """
    Create a new Netlify site.

    Args:
        token: Netlify auth token
        config_name: Config name (used as subdomain)
        title: Site title from Quarto config

    Returns:
        Site data dict with 'id' and 'url', or None on failure
    """
    subdomain = config_name.replace("_", "-")
    site_name = f"{subdomain}-warondisease"  # Netlify site name (globally unique)
    custom_domain = f"{subdomain}.{BASE_DOMAIN}"

    # Create site with no build settings (manual deploys only)
    payload = {
        "name": site_name,
        "custom_domain": custom_domain,
        "build_settings": {
            "cmd": "",  # No build command
            "dir": "",  # No publish directory (set per-deploy)
        },
        "processing_settings": {
            "skip": True,  # Skip post-processing
        },
    }

    resp = requests.post(
        f"{NETLIFY_API}/sites",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )

    if resp.status_code in (200, 201):
        site = resp.json()
        print(f"  [OK] Created site: {site.get('url')}")
        print(f"       Site ID: {site.get('id')}")
        print(f"       Custom domain: {custom_domain}")
        return {
            "id": site.get("id"),
            "url": site.get("url"),
            "custom_domain": custom_domain,
        }
    else:
        print(f"  [ERROR] Failed to create site: {resp.status_code}")
        print(f"          {resp.text}")

        # Check if site already exists with this name
        if "already been taken" in resp.text.lower():
            print(f"  [INFO] Site name '{site_name}' already exists. Trying to find it...")
            return find_existing_site(token, site_name)
        return None


def find_existing_site(token: str, site_name: str) -> dict | None:
    """Find an existing site by name."""
    resp = requests.get(
        f"{NETLIFY_API}/sites",
        headers={"Authorization": f"Bearer {token}"},
        params={"name": site_name, "filter": "all"},
    )

    if resp.status_code == 200:
        sites = resp.json()
        for site in sites:
            if site.get("name") == site_name:
                print(f"  [OK] Found existing site: {site.get('url')}")
                print(f"       Site ID: {site.get('id')}")
                return {
                    "id": site.get("id"),
                    "url": site.get("url"),
                    "custom_domain": site.get("custom_domain"),
                }
    return None


def discover_configs() -> dict:
    """
    Discover all Quarto configs and their Netlify status.

    Returns:
        Dict mapping config_name to config info
    """
    configs = {}

    for config_path in PROJECT_ROOT.glob("_quarto-*.yml"):
        # Skip build temp copies
        if "_build_temp" in str(config_path):
            continue

        config_name = config_path.stem.replace("_quarto-", "")

        # Skip special configs
        if config_name in SKIP_CONFIGS:
            continue

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"[WARN] Could not read {config_path}: {e}")
            continue

        # Get title
        project_type = config.get("project", {}).get("type", "website")
        if project_type == "book":
            title = config.get("book", {}).get("title", config_name)
        else:
            title = config.get("website", {}).get("title", config_name)

        # Check for existing site ID
        dih_render = config.get("dih-render", {})
        site_id = dih_render.get("netlify-site-id")

        configs[config_name] = {
            "path": config_path,
            "config": config,
            "title": title,
            "project_type": project_type,
            "site_id": site_id,
            "has_site": bool(site_id),
        }

    return configs


def update_config_with_site_id(config_path: Path, site_id: str) -> bool:
    """
    Update a Quarto config file with the Netlify site ID.

    Preserves existing content and adds/updates dih-render.netlify-site-id.
    """
    try:
        content = config_path.read_text(encoding="utf-8")

        # Check if dih-render section exists
        if "dih-render:" in content:
            # Check if netlify-site-id already exists in dih-render
            if "netlify-site-id:" in content:
                # Replace existing
                content = re.sub(
                    r'(dih-render:.*?)netlify-site-id:.*?(\n|$)',
                    rf'\1netlify-site-id: "{site_id}"\2',
                    content,
                    flags=re.DOTALL,
                )
            else:
                # Add to existing dih-render section
                content = re.sub(
                    r'(dih-render:\n)',
                    rf'\1  netlify-site-id: "{site_id}"\n',
                    content,
                )
        else:
            # Add new dih-render section after project section
            content = re.sub(
                r'(project:\n.*?(?=\n\w|\nprofiles:|\nwebsite:|\nbook:|\nformat:|\nexecute:|\nmetadata:|\nbibliography:))',
                rf'\1\ndih-render:\n  netlify-site-id: "{site_id}"\n',
                content,
                flags=re.DOTALL,
            )

        config_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to update config: {e}")
        return False


def regenerate_workflow():
    """Regenerate GitHub Actions workflow from configs."""
    try:
        from lib.workflow_generator import regenerate_workflow as regen
        regen(PROJECT_ROOT)
    except Exception as e:
        print(f"[WARN] Could not regenerate workflow: {e}")
        print("       Run manually: python scripts/lib/workflow_generator.py")


def list_configs(configs: dict):
    """Print status of all configs."""
    print("\nQuarto Configs Status:")
    print("=" * 70)
    print(f"{'Config':<20} {'Has Site ID':<12} {'Title'}")
    print("-" * 70)

    for name, info in sorted(configs.items()):
        status = "Yes" if info["has_site"] else "No"
        title = info["title"][:40] + "..." if len(info["title"]) > 40 else info["title"]
        print(f"{name:<20} {status:<12} {title}")

    print("-" * 70)
    missing = [n for n, i in configs.items() if not i["has_site"]]
    if missing:
        print(f"\nConfigs needing Netlify sites: {', '.join(missing)}")
    else:
        print("\nAll configs have Netlify site IDs.")


def main():
    parser = argparse.ArgumentParser(description="Setup Netlify sites for Quarto configs")
    parser.add_argument("configs", nargs="*", help="Specific configs to process (default: all missing)")
    parser.add_argument("--list", "-l", action="store_true", help="List configs and exit")
    parser.add_argument("--force", "-f", action="store_true", help="Recreate sites even if ID exists")
    args = parser.parse_args()

    print("=" * 60)
    print("Netlify Site Setup")
    print("=" * 60)

    # Discover configs
    configs = discover_configs()
    if not configs:
        print("[ERROR] No Quarto configs found")
        return 1

    # List mode
    if args.list:
        list_configs(configs)
        return 0

    # Get token
    token = get_netlify_token()
    if not token:
        print("[ERROR] NETLIFY_AUTH_TOKEN not set")
        print("  Get token at: https://app.netlify.com/user/applications#personal-access-tokens")
        print("  Add to .env: NETLIFY_AUTH_TOKEN=your_token")
        return 1

    # Filter to requested configs
    if args.configs:
        configs = {k: v for k, v in configs.items() if k in args.configs}
        if not configs:
            print(f"[ERROR] No matching configs: {', '.join(args.configs)}")
            return 1

    # Filter to configs needing sites (unless --force)
    if not args.force:
        configs = {k: v for k, v in configs.items() if not v["has_site"]}

    if not configs:
        print("[OK] All configs already have Netlify site IDs")
        print("     Use --list to see status, --force to recreate")
        return 0

    print(f"\nCreating Netlify sites for: {', '.join(configs.keys())}\n")

    # Create sites
    created = 0
    for config_name, info in configs.items():
        print(f"\n[*] {config_name}: {info['title'][:50]}")

        site = create_netlify_site(token, config_name, info["title"])
        if site and site.get("id"):
            if update_config_with_site_id(info["path"], site["id"]):
                print(f"  [OK] Updated {info['path'].name} with site ID")
                created += 1
            else:
                print(f"  [WARN] Site created but config not updated")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Created {created} Netlify site(s)")

    if created > 0:
        print("\nNext steps:")
        print("  1. Configure DNS: Add CNAME records for subdomains")
        print(f"     Example: iab.{BASE_DOMAIN} -> [netlify-site].netlify.app")
        print("  2. Review changes: git diff _quarto-*.yml")
        print("  3. Regenerate workflow (auto-attempted below)")
        print("  4. Commit: git add _quarto-*.yml .github/workflows/publish.yml")

        # Regenerate workflow
        print("\n[*] Regenerating GitHub Actions workflow...")
        regenerate_workflow()

    return 0


if __name__ == "__main__":
    sys.exit(main())
