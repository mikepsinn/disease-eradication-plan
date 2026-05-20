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
    import requests
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install requests")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent.parent
BASE_DOMAIN = "warondisease.org"
MANUAL_NETLIFY_CNAME = "manual-warondisease-org.netlify.app"

# Add project root and scripts/lib to path for imports
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "lib"))

from dih_models.yaml_utils import load_quarto_config
from quarto_config_utils import NON_DEPLOYABLE_CONFIGS  # type: ignore[import-not-found]
from python_utils import load_project_dotenv  # type: ignore[import-not-found]

# Netlify API
NETLIFY_API = "https://api.netlify.com/api/v1"

# Cloudflare API
CLOUDFLARE_API = "https://api.cloudflare.com/client/v4"
CLOUDFLARE_ZONE_ID = "ee19b9351a3502167898f08136b11c09"  # warondisease.org zone


def get_netlify_token() -> str | None:
    """Get Netlify auth token from environment."""
    load_project_dotenv(PROJECT_ROOT)
    return os.environ.get("NETLIFY_AUTH_TOKEN")


def get_cloudflare_token() -> str | None:
    """Get Cloudflare API token from environment."""
    load_project_dotenv(PROJECT_ROOT)
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


def update_dns_record(cf_token: str, record_id: str, subdomain: str, cname_target: str) -> bool:
    """Update an existing CNAME record in Cloudflare."""
    resp = requests.patch(
        f"{CLOUDFLARE_API}/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record_id}",
        headers={
            "Authorization": f"Bearer {cf_token}",
            "Content-Type": "application/json",
        },
        json={
            "content": cname_target,
            "proxied": True,  # Orange cloud ON
        },
    )

    if resp.status_code == 200:
        print(f"  [OK] Updated DNS: {subdomain}.{BASE_DOMAIN} -> {cname_target}")
        return True
    else:
        error = resp.json().get("errors", [{}])[0].get("message", resp.text)
        print(f"  [ERROR] DNS update failed: {error}")
        return False


def setup_dns_records(cf_token: str, configs: dict) -> tuple[int, int]:
    """Create or update DNS records for all configs. Returns (created, updated) counts."""
    print("\n[*] Checking Cloudflare DNS records...")

    existing = get_existing_dns_records(cf_token)
    print(f"    Found {len(existing)} existing CNAME records")

    created = 0
    updated = 0
    for config_name, info in configs.items():
        # Skip configs without CNAME info
        cname = info.get("netlify_cname")
        if not cname:
            continue

        # Use subdomain from config's site-url (or fallback to config name)
        subdomain = info.get("subdomain", config_name.replace("_", "-"))

        # Check if record already exists
        if subdomain in existing:
            current = existing[subdomain].get("content", "")
            if current == cname:
                print(f"  [OK] {subdomain}.{BASE_DOMAIN} already configured")
            else:
                # Update the record to point to correct CNAME
                record_id = existing[subdomain].get("id")
                if record_id:
                    print(f"  [*] Updating {subdomain}.{BASE_DOMAIN}: {current} -> {cname}")
                    if update_dns_record(cf_token, record_id, subdomain, cname):
                        updated += 1
                else:
                    print(f"  [WARN] {subdomain}.{BASE_DOMAIN} needs update but no record ID")
        else:
            # Create the record
            if create_dns_record(cf_token, subdomain, cname):
                created += 1

        time.sleep(0.5)  # Rate limit protection

    return created, updated


def get_netlify_team_slug(token: str) -> str | None:
    """Get the user's Netlify team slug."""
    # First check environment variable override
    load_project_dotenv(PROJECT_ROOT)
    env_slug = os.environ.get("NETLIFY_TEAM_SLUG")
    if env_slug:
        return env_slug

    # Try the accounts endpoint
    resp = requests.get(
        f"{NETLIFY_API}/accounts",
        headers={"Authorization": f"Bearer {token}"}
    )
    if resp.status_code == 200:
        accounts = resp.json()
        if accounts:
            return accounts[0].get("slug")

    # Fallback: try common slugs that might work with this token
    # This handles tokens with restricted permissions
    common_slugs = ["mikepsinn"]  # Add your account slug here as fallback
    for slug in common_slugs:
        test_resp = requests.get(
            f"{NETLIFY_API}/{slug}/sites",
            headers={"Authorization": f"Bearer {token}"},
            params={"per_page": 1}
        )
        if test_resp.status_code == 200:
            return slug

    return None


def create_netlify_site(token: str, config_name: str, title: str, custom_domain: str | None = None) -> dict | None:
    """
    Create a new Netlify site.

    Args:
        token: Netlify auth token
        config_name: Config name (for logging)
        title: Site title from Quarto config
        custom_domain: Full custom domain to use (e.g., dfda-impact.warondisease.org). If None, derives from config_name.

    Returns:
        Site data dict with 'id' and 'url', or None on failure
    """
    if not custom_domain:
        custom_domain = f"{config_name.replace('_', '-')}.{BASE_DOMAIN}"
    # Generate site name from the domain (replace dots with dashes for Netlify naming)
    site_name = custom_domain.replace(".", "-")

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


def get_all_sites(token: str) -> dict[str, dict]:
    """
    Fetch all sites from the account. Returns dict mapping site_id to site info.
    Uses the account-scoped endpoint which has better permissions than direct site lookup.
    """
    # First get the account slug
    team_slug = get_netlify_team_slug(token)
    if not team_slug:
        return {}

    resp = requests.get(
        f"{NETLIFY_API}/{team_slug}/sites",
        headers={"Authorization": f"Bearer {token}"},
    )

    if resp.status_code != 200:
        print(f"  [WARN] Could not fetch sites list: {resp.status_code}")
        return {}

    sites = {}
    for site in resp.json():
        site_id = site.get("id")
        site_name = site.get("name", "")
        sites[site_id] = {
            "id": site_id,
            "name": site_name,
            "url": site.get("url"),
            "custom_domain": site.get("custom_domain"),
            "netlify_subdomain": f"{site_name}.netlify.app" if site_name else "",
            "status": "ok",
        }
    return sites


# Cache for all sites (populated once per run)
_all_sites_cache: dict[str, dict] | None = None


def get_site_by_id(token: str, site_id: str, debug: bool = False) -> dict | None:
    """Fetch site info by ID. Uses cached bulk fetch for better API compatibility."""
    global _all_sites_cache

    # Try cache first (bulk fetch has better permissions)
    if _all_sites_cache is None:
        _all_sites_cache = get_all_sites(token)

    if site_id in _all_sites_cache:
        return _all_sites_cache[site_id]

    # Fallback to direct API call
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
            "status": "ok",
        }
    # Return error info instead of None so we can display helpful messages
    error_info = {
        "id": site_id,
        "status": "error",
        "status_code": resp.status_code,
    }
    if resp.status_code == 401:
        error_info["error"] = "Unauthorized - site may be deleted or owned by different account"
    elif resp.status_code == 404:
        error_info["error"] = "Site not found - ID may be invalid or site was deleted"
    else:
        error_info["error"] = f"API error {resp.status_code}: {resp.text[:100]}"
    return error_info


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


def extract_subdomain_from_url(url: str) -> str | None:
    """Extract subdomain from a site URL like https://impact.warondisease.org -> impact"""
    if not url:
        return None
    # Remove protocol
    url = url.replace("https://", "").replace("http://", "")
    # Get the hostname part (before any path)
    hostname = url.split("/")[0].lower()
    # Check if it's a subdomain of warondisease.org
    if hostname.endswith(f".{BASE_DOMAIN.lower()}"):
        subdomain = hostname.replace(f".{BASE_DOMAIN.lower()}", "")
        return subdomain
    return None


def extract_custom_domain_from_url(url: str) -> str | None:
    """Extract the full hostname from a site URL to use as custom domain.

    Examples:
        https://impact.warondisease.org -> impact.warondisease.org
        https://dfda-impact.warondisease.org -> dfda-impact.warondisease.org
    """
    if not url:
        return None
    # Remove protocol
    url = url.replace("https://", "").replace("http://", "")
    # Get the hostname part (before any path)
    hostname = url.split("/")[0].lower()
    return hostname if hostname else None


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

        # Skip non-deployable configs (test, shared-defaults, etc.)
        if config_name in NON_DEPLOYABLE_CONFIGS or not config_name or config_name == "quarto":
            continue

        try:
            config = load_quarto_config(config_path)
        except Exception as e:
            print(f"[WARN] Could not read {config_path}: {e}")
            continue

        # Get title and site-url based on project type
        project_type = config.get("project", {}).get("type", "website")
        site_url = None
        if project_type == "book":
            book = config.get("book", {})
            title = book.get("title", config_name)
            site_url = book.get("site-url")
        else:
            website = config.get("website", {})
            title = website.get("title", config_name)
            site_url = website.get("site-url")

        # Also check website section for books (some have both)
        if not site_url and "website" in config:
            site_url = config["website"].get("site-url")

        # Check for existing site ID, CNAME, and legacy redirect host
        dih_render = config.get("dih-render", {})
        site_id = dih_render.get("netlify-site-id")
        netlify_cname = dih_render.get("netlify-cname")
        redirect_from = dih_render.get("redirect-from")

        # DNS is managed for the legacy host when a config redirects into the manual.
        # The canonical site-url may be a manual page, not the old paper hostname.
        dns_source_url = redirect_from or site_url

        # Extract subdomain from redirect-from/site-url, or fall back to config name
        subdomain = extract_subdomain_from_url(dns_source_url)
        if not subdomain:
            subdomain = config_name.replace("_", "-")

        # Extract full custom domain from redirect-from/site-url
        custom_domain = extract_custom_domain_from_url(dns_source_url)
        if not custom_domain:
            custom_domain = f"{subdomain}.{BASE_DOMAIN}"
        redirect_only = bool(redirect_from and netlify_cname == MANUAL_NETLIFY_CNAME)

        configs[config_name] = {
            "path": config_path,
            "config": config,
            "title": title,
            "project_type": project_type,
            "site_id": site_id,
            "netlify_cname": netlify_cname,
            "has_site": bool(site_id),
            "site_url": site_url,
            "redirect_from": redirect_from,
            "redirect_only": redirect_only,
            "subdomain": subdomain,  # The subdomain part (for warondisease.org sites)
            "custom_domain": custom_domain,  # The full DNS hostname being managed
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


def list_configs(configs: dict, token: str | None = None, cf_token: str | None = None):
    """Print detailed status of all configs including domains and DNS."""
    global _all_sites_cache
    _all_sites_cache = None  # Reset cache for fresh data

    print("\n" + "=" * 90)
    print("QUARTO SITES STATUS")
    print("=" * 90)

    # Fetch all Netlify sites at once (better API compatibility)
    if token:
        print("[*] Fetching Netlify sites...")
        all_sites = get_all_sites(token)
        print(f"    Found {len(all_sites)} sites in account")

    # Fetch Cloudflare DNS records if token available
    dns_records = {}
    if cf_token:
        print("[*] Fetching Cloudflare DNS records...")
        dns_records = get_existing_dns_records(cf_token)
        print(f"    Found {len(dns_records)} CNAME records")
    else:
        print("[INFO] Set CLOUDFLARE_TOKEN to see DNS records")

    print()

    # Track invalid sites during listing
    invalid_sites = []

    for name, info in sorted(configs.items()):
        expected_domain = info.get("custom_domain", f"{name.replace('_', '-')}.{BASE_DOMAIN}")
        expected_cname = info.get("netlify_cname") or f"{expected_domain.replace('.', '-')}.netlify.app"
        redirect_only = info.get("redirect_only", False)

        print(f"\n{'─' * 90}")
        print(f"CONFIG: {name}")
        print(f"  Title: {info['title'][:70]}")
        print(f"  Site URL: {info.get('site_url', '(not set)')}")
        if info.get("redirect_from"):
            print(f"  Redirect From: {info.get('redirect_from')}")
        print(f"  Expected DNS Host: https://{expected_domain}")
        print(f"  Expected CNAME: {expected_cname or '(not set)'}")

        # Netlify info
        site_id = info.get("site_id")
        if site_id:
            print(f"\n  NETLIFY:")
            print(f"    Site ID: {site_id}")

            # Fetch live info from Netlify API
            if token:
                time.sleep(0.3)  # Rate limit protection
                site = get_site_by_id(token, site_id)
                if site and site.get("status") == "ok":
                    netlify_url = site.get("netlify_subdomain", "")
                    custom_domain = site.get("custom_domain", "")
                    print(f"    Netlify URL: https://{netlify_url}")
                    print(f"    Custom Domain: {custom_domain or '(not set)'}")

                    # Redirect-only configs serve their legacy host from the manual site.
                    if redirect_only:
                        print(f"    [INFO] Redirect-only DNS target is {expected_cname}")

                    # Check if custom domain matches expected
                    if not redirect_only and custom_domain and custom_domain != expected_domain:
                        print(f"    [WARN] Expected: {expected_domain}")

                    # Check if netlify URL matches expected CNAME
                    if not redirect_only and netlify_url and netlify_url != expected_cname:
                        print(f"    [INFO] CNAME target differs from expected: {expected_cname}")
                elif site and site.get("status") == "error":
                    print(f"    [ERROR] {site.get('error', 'Unknown error')}")
                    print(f"    [ACTION] Remove netlify-site-id from config and run 'npm run netlify:setup' to create new site")
                    invalid_sites.append(name)
                else:
                    print(f"    [ERROR] Could not fetch site info")
            else:
                print(f"    Config CNAME: {info.get('netlify_cname', '(not set)')}")
        else:
            print(f"\n  NETLIFY: [NOT CONFIGURED]")

        # Cloudflare DNS info (only for warondisease.org subdomains)
        if cf_token:
            print(f"\n  CLOUDFLARE DNS:")
            # Check if this is a warondisease.org subdomain
            subdomain = info.get("subdomain")  # Only set for warondisease.org domains
            if subdomain and expected_domain.endswith(f".{BASE_DOMAIN}"):
                dns_record = dns_records.get(subdomain)
                if dns_record:
                    record_target = dns_record.get("content", "")
                    proxied = dns_record.get("proxied", False)
                    proxy_status = "proxied (orange cloud)" if proxied else "DNS only (gray cloud)"
                    print(f"    {subdomain}.{BASE_DOMAIN} -> {record_target}")
                    print(f"    Status: {proxy_status}")

                    # Check if DNS points to correct Netlify site
                    config_cname = info.get("netlify_cname", "")
                    if record_target and config_cname and record_target != config_cname:
                        print(f"    [WARN] DNS points to {record_target}")
                        print(f"           Config expects {config_cname}")
                else:
                    print(f"    [NOT FOUND] No CNAME record for {subdomain}.{BASE_DOMAIN}")
            else:
                print(f"    [INFO] Domain {expected_domain} is not managed by Cloudflare (warondisease.org)")

    # Summary
    print(f"\n{'=' * 90}")
    print("SUMMARY")
    print("=" * 90)

    total = len(configs)
    with_sites = sum(1 for c in configs.values() if c.get("site_id"))
    missing_sites = [
        n for n, c in configs.items()
        if not c.get("site_id") and not c.get("redirect_only")
    ]

    print(f"  Total configs: {total}")
    print(f"  With Netlify sites: {with_sites}")
    print(f"  Missing sites: {len(missing_sites)}")
    if invalid_sites:
        print(f"  Invalid/inaccessible sites: {len(invalid_sites)}")

    if missing_sites:
        print(f"\n  Configs needing setup: {', '.join(missing_sites)}")

    if invalid_sites:
        print(f"\n  [!] Sites with invalid IDs (need recreation): {', '.join(invalid_sites)}")
        print(f"      To fix: Remove 'netlify-site-id' from these configs, then run 'npm run netlify:setup'")

    if cf_token:
        # Check for orphaned DNS records - use actual subdomains from site-url, not config names
        config_subdomains = {info.get("subdomain", n.replace("_", "-")) for n, info in configs.items()}
        orphaned = [r for r in dns_records.keys() if r not in config_subdomains and r != "www" and r != "@"]
        if orphaned:
            print(f"\n  Orphaned DNS records (no matching config): {', '.join(orphaned[:10])}")
            if len(orphaned) > 10:
                print(f"    ... and {len(orphaned) - 10} more")

    print(f"\n{'=' * 90}")


def update_existing_cnames(token: str, configs: dict) -> int:
    """Fetch and update CNAME info for configs that have site IDs."""
    updated = 0
    for config_name, info in configs.items():
        if info.get("redirect_only"):
            continue

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
    Update Netlify sites to use custom domains from Quarto configs.

    For each config with a site ID:
    1. Fetch current site info from Netlify
    2. Get expected custom domain from config's site-url
    3. Update if different
    4. Also rename the site to match the expected name pattern

    Returns:
        Tuple of (domains_updated, sites_renamed)
    """
    domains_updated = 0
    sites_renamed = 0

    for config_name, info in configs.items():
        if info.get("redirect_only"):
            print(f"\n[*] {config_name}: redirect-only, leaving Netlify custom domain unchanged")
            continue

        site_id = info.get("site_id")
        if not site_id:
            continue

        # Use the custom domain directly from site-url in config
        expected_domain = info.get("custom_domain", f"{config_name.replace('_', '-')}.{BASE_DOMAIN}")
        # Generate site name from the domain (replace dots with dashes for Netlify naming)
        expected_site_name = expected_domain.replace(".", "-")

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

        # Never rename existing sites - it breaks DNS records pointing to the old .netlify.app name
        if current_name != expected_site_name:
            print(f"  [INFO] Site name '{current_name}' differs from expected '{expected_site_name}' - keeping existing name to preserve DNS")

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

    # List mode - show detailed status and exit
    if args.list:
        token = get_netlify_token()
        cf_token = get_cloudflare_token()
        list_configs(configs, token, cf_token)
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
    configs_needing_sites = {
        k: v for k, v in configs.items()
        if not v["has_site"] and not v.get("redirect_only")
    }
    if configs_needing_sites:
        print(f"\n[1/4] Creating {len(configs_needing_sites)} missing Netlify site(s)...")
        for config_name, info in configs_needing_sites.items():
            print(f"\n  [*] {config_name}: {info['title'][:50]}")
            custom_domain = info.get("custom_domain", f"{config_name.replace('_', '-')}.{BASE_DOMAIN}")
            site = create_netlify_site(token, config_name, info["title"], custom_domain)
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
    # STEP 2: Update custom domains from Quarto configs
    # ===========================================
    print("\n[2/4] Syncing custom domains for standalone Netlify sites...")
    configs_with_sites = {
        k: v for k, v in configs.items()
        if v.get("site_id") and not v.get("redirect_only")
    }
    if configs_with_sites:
        for config_name, info in configs_with_sites.items():
            site_id = info.get("site_id")
            # Use the custom domain directly from site-url in config
            expected_domain = info.get("custom_domain", f"{config_name.replace('_', '-')}.{BASE_DOMAIN}")
            # Generate site name from the domain (replace dots with dashes for Netlify naming)
            expected_site_name = expected_domain.replace(".", "-")

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

            # Never rename existing sites - it breaks DNS records pointing to the old .netlify.app name
            if current_name != expected_site_name:
                print(f"  [INFO] Site name '{current_name}' differs from expected '{expected_site_name}' - keeping existing name to preserve DNS")

            time.sleep(0.5)

    if domains_updated == 0:
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
    dns_updated = 0
    if cf_token:
        print("\n[4/4] Setting up Cloudflare DNS records...")
        # Re-discover to get latest CNAME values
        configs = discover_configs()
        dns_created, dns_updated = setup_dns_records(cf_token, configs)
    else:
        print("\n[4/4] Skipping DNS setup (CLOUDFLARE_TOKEN not set)")
        print("  To enable: add CLOUDFLARE_TOKEN to .env")

    # ===========================================
    # Regenerate workflow if anything changed
    # ===========================================
    if sites_created > 0 or domains_updated > 0:
        print("\n[*] Regenerating GitHub Actions workflow...")
        regenerate_workflow()

    # ===========================================
    # Summary
    # ===========================================
    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  Sites created:    {sites_created}")
    print(f"  Domains updated:  {domains_updated}")
    print(f"  DNS created:      {dns_created}")
    print(f"  DNS updated:      {dns_updated}")
    print("=" * 60)

    if not cf_token and (sites_created > 0 or domains_updated > 0):
        print_dns_instructions()

    return 0


if __name__ == "__main__":
    sys.exit(main())
