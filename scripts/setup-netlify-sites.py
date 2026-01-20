#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Netlify Site Setup & Sync Script

Automatically sets up and syncs all Netlify sites for Quarto configs.
Does everything in one run - just execute with no arguments.

Usage:
    python scripts/setup-netlify-sites.py           # Do everything automatically
    python scripts/setup-netlify-sites.py --list    # Just show status (no changes)

Environment:
    NETLIFY_AUTH_TOKEN: Required - from https://app.netlify.com/user/applications#personal-access-tokens
    CLOUDFLARE_TOKEN:   Optional - enables automatic DNS setup

The script automatically:
1. Creates Netlify sites for any configs missing site IDs
2. Updates all sites to use {config-name}.warondisease.org custom domains
3. Renames sites to {config-name}-warondisease.netlify.app
4. Syncs CNAME info back to config files
5. Creates Cloudflare DNS records (if CLOUDFLARE_TOKEN set)
6. Regenerates GitHub Actions workflow
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
            "name": site_name,
            "url": site.get("url"),
            "custom_domain": site.get("custom_domain"),
            "netlify_subdomain": netlify_subdomain,
        }
    return None


def update_site_custom_domain(token: str, site_id: str, custom_domain: str) -> bool:
    """
    Update a Netlify site's custom domain.

    Args:
        token: Netlify auth token
        site_id: The Netlify site ID
        custom_domain: The custom domain to set (e.g., "iab.warondisease.org")

    Returns:
        True if successful, False otherwise
    """
    resp = requests.patch(
        f"{NETLIFY_API}/sites/{site_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"custom_domain": custom_domain},
    )

    if resp.status_code == 200:
        print(f"  [OK] Updated custom domain to: {custom_domain}")
        return True
    else:
        print(f"  [ERROR] Failed to update custom domain: {resp.status_code}")
        print(f"          {resp.text}")
        return False


def rename_netlify_site(token: str, site_id: str, new_name: str) -> bool:
    """
    Rename a Netlify site (changes the *.netlify.app subdomain).

    Args:
        token: Netlify auth token
        site_id: The Netlify site ID
        new_name: The new site name (will become new_name.netlify.app)

    Returns:
        True if successful, False otherwise
    """
    resp = requests.patch(
        f"{NETLIFY_API}/sites/{site_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"name": new_name},
    )

    if resp.status_code == 200:
        print(f"  [OK] Renamed site to: {new_name}.netlify.app")
        return True
    else:
        error_msg = resp.text
        if "already been taken" in error_msg.lower():
            print(f"  [WARN] Site name '{new_name}' already taken - keeping current name")
            return False
        print(f"  [ERROR] Failed to rename site: {resp.status_code}")
        print(f"          {error_msg}")
        return False


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


def update_netlify_domains(token: str, configs: dict) -> tuple[int, int]:
    """
    Update Netlify sites to use warondisease.org custom domains.

    For each config with a site ID:
    1. Fetch current site info from Netlify
    2. Calculate expected custom domain (config_name.warondisease.org)
    3. Update if different
    4. Also rename the site to match the expected name pattern

    Returns:
        Tuple of (domains_updated, sites_renamed)
    """
    domains_updated = 0
    sites_renamed = 0

    for config_name, info in configs.items():
        site_id = info.get("site_id")
        if not site_id:
            continue

        # Calculate expected values
        subdomain = config_name.replace("_", "-")
        expected_domain = f"{subdomain}.{BASE_DOMAIN}"
        expected_site_name = f"{subdomain}-warondisease"

        print(f"\n[*] {config_name}:")
        print(f"    Site ID: {site_id}")
        print(f"    Expected domain: {expected_domain}")

        # Fetch current site info
        site = get_site_by_id(token, site_id)
        if not site:
            print(f"  [ERROR] Could not fetch site info")
            continue

        current_domain = site.get("custom_domain", "")
        current_name = site.get("name", "")

        print(f"    Current domain: {current_domain or '(none)'}")
        print(f"    Current name: {current_name}")

        # Update custom domain if needed
        if current_domain != expected_domain:
            print(f"  [*] Updating custom domain: {current_domain} -> {expected_domain}")
            if update_site_custom_domain(token, site_id, expected_domain):
                domains_updated += 1
        else:
            print(f"  [OK] Custom domain already correct")

        # Rename site if needed (changes the *.netlify.app subdomain)
        if current_name != expected_site_name:
            print(f"  [*] Renaming site: {current_name} -> {expected_site_name}")
            if rename_netlify_site(token, site_id, expected_site_name):
                sites_renamed += 1
                # Update config with new CNAME
                new_cname = f"{expected_site_name}.netlify.app"
                update_config_with_netlify_info(info["path"], site_id, new_cname)

        time.sleep(1)  # Rate limit protection

    return domains_updated, sites_renamed


def main():
    parser = argparse.ArgumentParser(description="Setup and sync Netlify sites for all Quarto configs")
    parser.add_argument("--list", "-l", action="store_true", help="List configs and their status (no changes)")
    args = parser.parse_args()

    print("=" * 60)
    print("Netlify Site Setup & Sync")
    print("=" * 60)

    # Discover configs
    configs = discover_configs()
    if not configs:
        print("[ERROR] No Quarto configs found")
        return 1

    # List mode - just show status and exit
    if args.list:
        list_configs(configs)
        return 0

    # Get Netlify token (required)
    token = get_netlify_token()
    if not token:
        print("[ERROR] NETLIFY_AUTH_TOKEN not set")
        print("  Get token at: https://app.netlify.com/user/applications#personal-access-tokens")
        print("  Add to .env: NETLIFY_AUTH_TOKEN=your_token")
        return 1

    # Get Cloudflare token (optional - for DNS)
    cf_token = get_cloudflare_token()

    # Track totals
    sites_created = 0
    domains_updated = 0
    sites_renamed = 0
    dns_created = 0

    # ===========================================
    # STEP 1: Create missing Netlify sites
    # ===========================================
    configs_needing_sites = {k: v for k, v in configs.items() if not v["has_site"]}
    if configs_needing_sites:
        print(f"\n[1/4] Creating {len(configs_needing_sites)} missing Netlify site(s)...")
        for config_name, info in configs_needing_sites.items():
            print(f"\n  [*] {config_name}: {info['title'][:50]}")
            site = create_netlify_site(token, config_name, info["title"])
            if site and site.get("id"):
                netlify_cname = site.get("netlify_subdomain", "")
                if update_config_with_netlify_info(info["path"], site["id"], netlify_cname):
                    print(f"    [OK] Created and saved to {info['path'].name}")
                    sites_created += 1
                    # Update the config dict so later steps see the new site ID
                    configs[config_name]["site_id"] = site["id"]
                    configs[config_name]["has_site"] = True
            time.sleep(1)
    else:
        print("\n[1/4] All configs already have Netlify site IDs")

    # ===========================================
    # STEP 2: Update custom domains to warondisease.org
    # ===========================================
    print(f"\n[2/4] Syncing custom domains to {BASE_DOMAIN}...")
    configs_with_sites = {k: v for k, v in configs.items() if v.get("site_id")}
    if configs_with_sites:
        for config_name, info in configs_with_sites.items():
            site_id = info.get("site_id")
            subdomain = config_name.replace("_", "-")
            expected_domain = f"{subdomain}.{BASE_DOMAIN}"
            expected_site_name = f"{subdomain}-warondisease"

            site = get_site_by_id(token, site_id)
            if not site:
                print(f"  [WARN] Could not fetch {config_name}")
                continue

            current_domain = site.get("custom_domain", "")
            current_name = site.get("name", "")

            # Update custom domain if needed
            if current_domain != expected_domain:
                print(f"  [*] {config_name}: {current_domain or '(none)'} -> {expected_domain}")
                if update_site_custom_domain(token, site_id, expected_domain):
                    domains_updated += 1

            # Rename site if needed
            if current_name != expected_site_name:
                if rename_netlify_site(token, site_id, expected_site_name):
                    sites_renamed += 1
                    new_cname = f"{expected_site_name}.netlify.app"
                    update_config_with_netlify_info(info["path"], site_id, new_cname)

            time.sleep(0.5)

    if domains_updated == 0 and sites_renamed == 0:
        print("  [OK] All domains already correct")

    # ===========================================
    # STEP 3: Update CNAME info in config files
    # ===========================================
    print("\n[3/4] Syncing CNAME info to config files...")
    cnames_updated = 0
    for config_name, info in configs_with_sites.items():
        site_id = info.get("site_id")
        site = get_site_by_id(token, site_id)
        if site and site.get("netlify_subdomain"):
            # Check if CNAME in config matches
            current_cname = info.get("netlify_cname", "")
            if current_cname != site["netlify_subdomain"]:
                if update_config_with_netlify_info(info["path"], site_id, site["netlify_subdomain"]):
                    cnames_updated += 1
        time.sleep(0.3)

    if cnames_updated > 0:
        print(f"  [OK] Updated {cnames_updated} config file(s)")
    else:
        print("  [OK] All CNAMEs already correct")

    # ===========================================
    # STEP 4: Setup DNS records (if Cloudflare token available)
    # ===========================================
    if cf_token:
        print("\n[4/4] Setting up Cloudflare DNS records...")
        # Re-discover to get latest CNAME values
        configs = discover_configs()
        dns_created = setup_dns_records(cf_token, configs)
    else:
        print("\n[4/4] Skipping DNS setup (CLOUDFLARE_TOKEN not set)")
        print("  To enable: add CLOUDFLARE_TOKEN to .env")

    # ===========================================
    # Regenerate workflow if anything changed
    # ===========================================
    if sites_created > 0 or domains_updated > 0 or sites_renamed > 0:
        print("\n[*] Regenerating GitHub Actions workflow...")
        regenerate_workflow()

    # ===========================================
    # Summary
    # ===========================================
    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  Sites created:    {sites_created}")
    print(f"  Domains updated:  {domains_updated}")
    print(f"  Sites renamed:    {sites_renamed}")
    print(f"  DNS records:      {dns_created}")
    print("=" * 60)

    if not cf_token and (sites_created > 0 or domains_updated > 0):
        print_dns_instructions()

    return 0


if __name__ == "__main__":
    sys.exit(main())
