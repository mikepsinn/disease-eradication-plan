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
import time
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

# Cloudflare API
CLOUDFLARE_API = "https://api.cloudflare.com/client/v4"
CLOUDFLARE_ZONE_ID = "ee19b9351a3502167898f08136b11c09"  # warondisease.org zone


def get_netlify_token() -> str | None:
    """Get Netlify auth token from environment."""
    load_dotenv(PROJECT_ROOT / ".env")
    return os.environ.get("NETLIFY_AUTH_TOKEN")


def get_cloudflare_token() -> str | None:
    """Get Cloudflare API token from environment."""
    load_dotenv(PROJECT_ROOT / ".env")
    return os.environ.get("CLOUDFLARE_TOKEN")


def get_existing_dns_records(cf_token: str) -> dict[str, dict]:
    """Fetch existing DNS records from Cloudflare."""
    records = {}
    page = 1
    while True:
        resp = requests.get(
            f"{CLOUDFLARE_API}/zones/{CLOUDFLARE_ZONE_ID}/dns_records",
            headers={"Authorization": f"Bearer {cf_token}"},
            params={"type": "CNAME", "per_page": 100, "page": page},
        )
        if resp.status_code != 200:
            print(f"  [WARN] Could not fetch DNS records: {resp.status_code}")
            break

        data = resp.json()
        for record in data.get("result", []):
            # Store by subdomain name (e.g., "iab" from "iab.warondisease.org")
            name = record.get("name", "").replace(f".{BASE_DOMAIN}", "")
            records[name] = {
                "id": record.get("id"),
                "name": record.get("name"),
                "content": record.get("content"),
                "proxied": record.get("proxied"),
            }

        # Check if more pages
        result_info = data.get("result_info", {})
        if page >= result_info.get("total_pages", 1):
            break
        page += 1

    return records


def create_dns_record(cf_token: str, subdomain: str, cname_target: str) -> bool:
    """Create a CNAME record in Cloudflare."""
    resp = requests.post(
        f"{CLOUDFLARE_API}/zones/{CLOUDFLARE_ZONE_ID}/dns_records",
        headers={
            "Authorization": f"Bearer {cf_token}",
            "Content-Type": "application/json",
        },
        json={
            "type": "CNAME",
            "name": subdomain,  # Cloudflare auto-appends the zone domain
            "content": cname_target,
            "proxied": True,  # Orange cloud ON
            "ttl": 1,  # Auto TTL when proxied
        },
    )

    if resp.status_code in (200, 201):
        print(f"  [OK] Created DNS: {subdomain}.{BASE_DOMAIN} -> {cname_target}")
        return True
    else:
        error = resp.json().get("errors", [{}])[0].get("message", resp.text)
        print(f"  [ERROR] DNS creation failed: {error}")
        return False


def setup_dns_records(cf_token: str, configs: dict) -> int:
    """Create missing DNS records for all configs."""
    print("\n[*] Checking Cloudflare DNS records...")

    existing = get_existing_dns_records(cf_token)
    print(f"    Found {len(existing)} existing CNAME records")

    created = 0
    for config_name, info in configs.items():
        # Skip configs without CNAME info
        cname = info.get("netlify_cname")
        if not cname:
            continue

        # Extract subdomain from config name
        subdomain = config_name.replace("_", "-")

        # Skip if record already exists
        if subdomain in existing:
            current = existing[subdomain].get("content", "")
            if current == cname:
                print(f"  [OK] {subdomain}.{BASE_DOMAIN} already configured")
            else:
                print(f"  [WARN] {subdomain}.{BASE_DOMAIN} points to {current}, expected {cname}")
            continue

        # Create the record
        if create_dns_record(cf_token, subdomain, cname):
            created += 1

        time.sleep(0.5)  # Rate limit protection

    return created


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
        # Extract netlify subdomain for CNAME (e.g., "sitename.netlify.app")
        ssl_url = site.get("ssl_url") or site.get("url") or ""
        netlify_subdomain = ssl_url.replace("https://", "").replace("http://", "")

        print(f"  [OK] Created site: {site.get('url')}")
        print(f"       Site ID: {site.get('id')}")
        print(f"       Custom domain: {custom_domain}")
        print(f"       CNAME target: {netlify_subdomain}")
        return {
            "id": site.get("id"),
            "url": site.get("url"),
            "custom_domain": custom_domain,
            "netlify_subdomain": netlify_subdomain,
        }
    else:
        print(f"  [ERROR] Failed to create site: {resp.status_code}")
        print(f"          {resp.text}")

        # Check if site already exists with this name
        if "already been taken" in resp.text.lower():
            print(f"  [INFO] Site name '{site_name}' already exists. Trying to find it...")
            return find_existing_site(token, site_name)
        return None


def get_site_by_id(token: str, site_id: str) -> dict | None:
    """Fetch site info by ID to get the CNAME target."""
    resp = requests.get(
        f"{NETLIFY_API}/sites/{site_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    if resp.status_code == 200:
        site = resp.json()
        # Use site name to construct netlify subdomain (the actual CNAME target)
        site_name = site.get("name", "")
        netlify_subdomain = f"{site_name}.netlify.app" if site_name else ""
        return {
            "id": site.get("id"),
            "url": site.get("url"),
            "custom_domain": site.get("custom_domain"),
            "netlify_subdomain": netlify_subdomain,
        }
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
                ssl_url = site.get("ssl_url") or site.get("url") or ""
                netlify_subdomain = ssl_url.replace("https://", "").replace("http://", "")

                print(f"  [OK] Found existing site: {site.get('url')}")
                print(f"       Site ID: {site.get('id')}")
                print(f"       CNAME target: {netlify_subdomain}")
                return {
                    "id": site.get("id"),
                    "url": site.get("url"),
                    "custom_domain": site.get("custom_domain"),
                    "netlify_subdomain": netlify_subdomain,
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

        # Check for existing site ID and CNAME
        dih_render = config.get("dih-render", {})
        site_id = dih_render.get("netlify-site-id")
        netlify_cname = dih_render.get("netlify-cname")

        configs[config_name] = {
            "path": config_path,
            "config": config,
            "title": title,
            "project_type": project_type,
            "site_id": site_id,
            "netlify_cname": netlify_cname,
            "has_site": bool(site_id),
        }

    return configs


def update_config_with_netlify_info(config_path: Path, site_id: str, netlify_cname: str) -> bool:
    """
    Update a Quarto config file with Netlify site ID and CNAME.

    Adds/updates in dih-render section:
      - netlify-site-id: The Netlify site ID for deployments
      - netlify-cname: The CNAME target for DNS (e.g., "sitename.netlify.app")
    """
    try:
        content = config_path.read_text(encoding="utf-8")

        # Helper to add or update a property in dih-render
        def add_or_update_property(content: str, prop_name: str, prop_value: str) -> str:
            if f"{prop_name}:" in content:
                # Replace existing
                content = re.sub(
                    rf'{prop_name}:.*?(\n|$)',
                    rf'{prop_name}: "{prop_value}"\1',
                    content,
                )
            elif "dih-render:" in content:
                # Add to existing dih-render section (after the header)
                content = re.sub(
                    r'(dih-render:\n)',
                    rf'\1  {prop_name}: "{prop_value}"\n',
                    content,
                )
            return content

        # Ensure dih-render section exists
        if "dih-render:" not in content:
            content = re.sub(
                r'(project:\n.*?(?=\n\w|\nprofiles:|\nwebsite:|\nbook:|\nformat:|\nexecute:|\nmetadata:|\nbibliography:))',
                rf'\1\ndih-render:\n',
                content,
                flags=re.DOTALL,
            )

        # Add both properties
        content = add_or_update_property(content, "netlify-site-id", site_id)
        content = add_or_update_property(content, "netlify-cname", netlify_cname)

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


CLOUDFLARE_DNS_URL = "https://dash.cloudflare.com/52e6cea8444378116bd4a9c8834e1b27/warondisease.org/dns/records"


def print_dns_instructions():
    """Print DNS setup instructions."""
    print(f"""
DNS Setup (Cloudflare):
  1. Go to: {CLOUDFLARE_DNS_URL}
  2. Add CNAME record:
     - Type: CNAME
     - Name: [subdomain]  (e.g., "iab" for iab.warondisease.org)
     - Target: [netlify-cname from config]  (e.g., "iab-warondisease.netlify.app")
     - Proxy: ON (orange cloud)
  3. Save

The netlify-cname values are in each _quarto-*.yml under dih-render.""")


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


def update_existing_cnames(token: str, configs: dict) -> int:
    """Fetch and update CNAME info for configs that have site IDs."""
    updated = 0
    for config_name, info in configs.items():
        site_id = info.get("site_id")
        if not site_id:
            continue

        print(f"\n[*] {config_name}: Fetching site info...")
        site = get_site_by_id(token, site_id)
        if site and site.get("netlify_subdomain"):
            if update_config_with_netlify_info(info["path"], site_id, site["netlify_subdomain"]):
                print(f"  [OK] Updated {info['path'].name}")
                print(f"       CNAME: {site['netlify_subdomain']}")
                updated += 1
        else:
            print(f"  [WARN] Could not fetch site info for {site_id}")

        time.sleep(1)  # Rate limit protection

    return updated


def main():
    parser = argparse.ArgumentParser(description="Setup Netlify sites for Quarto configs")
    parser.add_argument("configs", nargs="*", help="Specific configs to process (default: all missing)")
    parser.add_argument("--list", "-l", action="store_true", help="List configs and exit")
    parser.add_argument("--force", "-f", action="store_true", help="Recreate sites even if ID exists")
    parser.add_argument("--update-cnames", "-u", action="store_true", help="Fetch CNAMEs for existing sites")
    parser.add_argument("--setup-dns", "-d", action="store_true", help="Create missing Cloudflare DNS records")
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

    # Update CNAMEs mode
    if args.update_cnames:
        print("\nFetching CNAMEs for existing sites...")
        configs_with_sites = {k: v for k, v in configs.items() if v["has_site"]}
        if not configs_with_sites:
            print("[OK] No configs with site IDs to update")
            return 0
        updated = update_existing_cnames(token, configs_with_sites)
        print(f"\n{'=' * 60}")
        print(f"Updated {updated} config(s) with CNAME info")
        if updated > 0:
            regenerate_workflow()
            print_dns_instructions()
        return 0

    # Setup DNS mode
    if args.setup_dns:
        cf_token = get_cloudflare_token()
        if not cf_token:
            print("[ERROR] CLOUDFLARE_TOKEN not set")
            print("  Get token at: https://dash.cloudflare.com/profile/api-tokens")
            print("  Add to .env: CLOUDFLARE_TOKEN=your_token")
            return 1

        # Re-discover to get latest CNAME values
        configs = discover_configs()
        created = setup_dns_records(cf_token, configs)
        print(f"\n{'=' * 60}")
        print(f"Created {created} DNS record(s)")
        return 0

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
    config_items = list(configs.items())
    for i, (config_name, info) in enumerate(config_items):
        print(f"\n[*] {config_name}: {info['title'][:50]}")

        site = create_netlify_site(token, config_name, info["title"])
        if site and site.get("id"):
            netlify_cname = site.get("netlify_subdomain", "")
            if update_config_with_netlify_info(info["path"], site["id"], netlify_cname):
                print(f"  [OK] Updated {info['path'].name} with site ID and CNAME")
                created += 1
            else:
                print(f"  [WARN] Site created but config not updated")

        # Rate limit protection: wait between API calls
        if i < len(config_items) - 1:
            time.sleep(2)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Created {created} Netlify site(s)")

    if created > 0:
        print_dns_instructions()
        print("\nNext steps:")
        print("  1. Add CNAME records (see above)")
        print("  2. Review changes: git diff _quarto-*.yml")
        print("  3. Commit: git add _quarto-*.yml .github/workflows/publish.yml")

        # Regenerate workflow
        print("\n[*] Regenerating GitHub Actions workflow...")
        regenerate_workflow()

    return 0


if __name__ == "__main__":
    sys.exit(main())
