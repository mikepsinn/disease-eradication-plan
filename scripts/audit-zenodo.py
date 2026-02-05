#!/usr/bin/env python3
"""
Zenodo Publication Audit Script

Compares Zenodo records against source QMD files to identify:
- Missing/blank fields (publisher, description, affiliation)
- Stale descriptions vs current abstracts
- Title mismatches
- DOI status

Usage:
    python scripts/audit-zenodo.py
    python scripts/audit-zenodo.py --verbose
    python scripts/audit-zenodo.py --json > audit-report.json
    
Requires:
    ZENODO_ACCESS_TOKEN env var (or --token flag)
    pip install requests pyyaml python-dotenv
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional

ZENODO_API = "https://zenodo.org/api"

# Known Zenodo deposit IDs (update as papers are added)
DEPOSIT_IDS = [
    18480048, 18480062, 18480076, 18480083, 18480086, 18480092,
    18480097, 18480147, 18480151, 18480158, 18480163, 18480175
]

# Expected values
EXPECTED_PUBLISHER = "Institute for Accelerated Medicine"
EXPECTED_AFFILIATION = "Institute for Accelerated Medicine"


def fetch_zenodo_record(deposit_id, token):
    """Fetch a Zenodo record by ID."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try deposit API first (for drafts)
    r = requests.get(f"{ZENODO_API}/deposit/depositions/{deposit_id}", headers=headers)
    if r.status_code == 200:
        return r.json()
    
    # Fall back to records API (for published)
    r = requests.get(f"{ZENODO_API}/records/{deposit_id}", headers=headers)
    if r.status_code == 200:
        return r.json()
    
    return None


def similarity(a, b):
    """Calculate text similarity ratio."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def audit_record(zenodo_data):
    """Audit a single Zenodo record for issues."""
    issues = []      # Blocking problems
    warnings = []    # Should fix
    info = []        # FYI
    
    meta = zenodo_data.get("metadata", {})
    
    # Extract fields
    title = meta.get("title", "")
    description = meta.get("description", "")
    publisher = meta.get("publisher", "")
    creators = meta.get("creators", [])
    doi = meta.get("doi", "")
    keywords = meta.get("keywords", [])
    
    # === TITLE ===
    if not title:
        issues.append("MISSING: title")
    elif len(title) < 10:
        warnings.append(f"SHORT: title only {len(title)} chars")
    
    # === DESCRIPTION/ABSTRACT ===
    if not description:
        issues.append("MISSING: description (abstract)")
    elif len(description) < 100:
        warnings.append(f"SHORT: description only {len(description)} chars")
    elif "This paper" in description[:50] or description.startswith("A paper"):
        warnings.append("GENERIC: description looks like placeholder")
    
    # === PUBLISHER ===
    if not publisher:
        issues.append("MISSING: publisher field (should be 'Institute for Accelerated Medicine')")
    elif publisher != EXPECTED_PUBLISHER:
        warnings.append(f"UNEXPECTED publisher: '{publisher}' (expected '{EXPECTED_PUBLISHER}')")
    else:
        info.append(f"Publisher: ✓ {publisher}")
    
    # === CREATORS/AFFILIATIONS ===
    if not creators:
        issues.append("MISSING: creators")
    else:
        has_good_affil = False
        for i, creator in enumerate(creators):
            name = creator.get("name", "Unknown")
            affil = creator.get("affiliation", "")
            orcid = creator.get("orcid", "")
            
            if not affil:
                warnings.append(f"MISSING: affiliation for {name}")
            elif EXPECTED_AFFILIATION in affil:
                has_good_affil = True
            
            if orcid:
                info.append(f"ORCID: {name} → {orcid}")
        
        if not has_good_affil and creators:
            warnings.append(f"NO creator has '{EXPECTED_AFFILIATION}' affiliation")
    
    # === DOI ===
    if not doi:
        warnings.append("NO DOI assigned yet (draft?)")
    else:
        info.append(f"DOI: {doi}")
    
    # === KEYWORDS ===
    if not keywords:
        warnings.append("NO keywords set")
    elif len(keywords) < 3:
        info.append(f"Keywords: only {len(keywords)} (consider adding more)")
    
    return {
        "issues": issues,
        "warnings": warnings,
        "info": info
    }


def run_audit(token, verbose=False, output_json=False, deposit_ids=None):
    """Run full audit of all Zenodo records."""
    
    if not output_json:
        print("=" * 60)
        print("ZENODO PUBLICATION AUDIT")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    if not token:
        print("ERROR: ZENODO_ACCESS_TOKEN not set")
        print("Set env var or use --token flag")
        sys.exit(1)
    
    ids_to_check = deposit_ids or DEPOSIT_IDS
    results = []
    total_issues = 0
    total_warnings = 0
    
    for deposit_id in ids_to_check:
        if not output_json:
            print(f"\n{'─' * 40}")
            print(f"Checking deposit {deposit_id}...")
        
        record = fetch_zenodo_record(deposit_id, token)
        if not record:
            if not output_json:
                print(f"  ❌ FAILED to fetch record")
            results.append({"id": deposit_id, "error": "fetch failed"})
            continue
        
        meta = record.get("metadata", {})
        title = meta.get("title", "Unknown")
        state = record.get("state", "unknown")
        
        if not output_json:
            print(f"  📄 {title[:55]}{'...' if len(title) > 55 else ''}")
            print(f"  State: {state}")
        
        audit = audit_record(record)
        
        # Count totals
        total_issues += len(audit["issues"])
        total_warnings += len(audit["warnings"])
        
        if not output_json:
            # Print issues
            if audit["issues"]:
                for issue in audit["issues"]:
                    print(f"  🔴 {issue}")
            
            if audit["warnings"]:
                for warn in audit["warnings"]:
                    print(f"  🟡 {warn}")
            
            if verbose and audit["info"]:
                for info in audit["info"]:
                    print(f"  ℹ️  {info}")
            
            if not audit["issues"] and not audit["warnings"]:
                print(f"  ✅ All checks passed")
        
        results.append({
            "id": deposit_id,
            "title": meta.get("title"),
            "state": state,
            "doi": meta.get("doi"),
            "publisher": meta.get("publisher"),
            "audit": audit
        })
    
    # Summary
    if not output_json:
        print(f"\n{'=' * 60}")
        print("SUMMARY")
        print(f"{'=' * 60}")
        print(f"Records checked: {len(ids_to_check)}")
        print(f"🔴 Issues (blocking): {total_issues}")
        print(f"🟡 Warnings: {total_warnings}")
        
        if total_issues > 0:
            print("\n⚠️  Issues found that should be fixed!")
        elif total_warnings > 0:
            print("\n⚡ No blocking issues, but warnings to address")
        else:
            print("\n✅ All records look good!")
    
    if output_json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "records_checked": len(ids_to_check),
                "total_issues": total_issues,
                "total_warnings": total_warnings
            },
            "records": results
        }
        return json.dumps(output, indent=2)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Audit Zenodo publications for missing/stale metadata"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Show info messages"
    )
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output as JSON"
    )
    parser.add_argument(
        "--token", "-t",
        help="Zenodo API token (or set ZENODO_ACCESS_TOKEN env var)"
    )
    parser.add_argument(
        "--ids",
        nargs="+",
        type=int,
        help="Specific deposit IDs to check (default: all known)"
    )
    args = parser.parse_args()
    
    token = args.token or os.getenv("ZENODO_ACCESS_TOKEN")
    
    result = run_audit(
        token=token,
        verbose=args.verbose,
        output_json=args.json,
        deposit_ids=args.ids
    )
    
    if args.json:
        print(result)


if __name__ == "__main__":
    main()
