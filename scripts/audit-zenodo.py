#!/usr/bin/env python3
"""
Zenodo Publication Audit Script

Auto-discovers papers from _quarto-*.yml configs and audits their Zenodo records:
- Missing/blank fields (publisher, description, affiliation)
- Title/description drift between config and Zenodo
- Duplicate deposits (same title or DOI across records)
- Orphaned Zenodo deposits (no matching local config)
- DOI status

Usage:
    python scripts/audit-zenodo.py
    python scripts/audit-zenodo.py --verbose
    python scripts/audit-zenodo.py --json > audit-report.json
    python scripts/audit-zenodo.py --write-todos
    python scripts/audit-zenodo.py --ids 18480048 18480062

Requires:
    ZENODO_TOKEN env var (or ZENODO_ACCESS_TOKEN, or --token flag)
    pip install requests pyyaml python-dotenv
"""

import sys
import json
import argparse
import io
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "lib"))

import requests

from python_utils import load_project_dotenv  # type: ignore[import-not-found]
from zenodo_client import (  # type: ignore[import-not-found]
    extract_zenodo_metadata,
    get_zenodo_token,
    get_record_id_from_doi,
)
from quarto_config_utils import discover_paper_configs  # type: ignore[import-not-found]

ZENODO_API = "https://zenodo.org/api"
PROJECT_ROOT = Path(__file__).parent.parent
load_project_dotenv(PROJECT_ROOT)

DUPLICATE_SIMILARITY_THRESHOLD = 0.9


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


def audit_record(zenodo_data, local_metadata=None):
    """Audit a single Zenodo record for issues.

    Args:
        zenodo_data: Zenodo API response dict
        local_metadata: Optional local metadata from extract_zenodo_metadata() for drift comparison
    """
    issues = []      # Blocking problems
    warnings = []    # Should fix
    info = []        # FYI

    meta = zenodo_data.get("metadata", {})

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
        issues.append("MISSING: publisher field")
    elif local_metadata and local_metadata.get("publisher"):
        expected_pub = local_metadata["publisher"]
        if publisher != expected_pub:
            warnings.append(f"PUBLISHER MISMATCH: '{publisher}' (expected '{expected_pub}' from config)")

    # === CREATORS/AFFILIATIONS ===
    if not creators:
        issues.append("MISSING: creators")
    else:
        for creator in creators:
            name = creator.get("name", "Unknown")
            affil = creator.get("affiliation", "")
            orcid = creator.get("orcid", "")

            if not affil:
                warnings.append(f"MISSING: affiliation for {name}")

            if orcid:
                info.append(f"ORCID: {name} -> {orcid}")

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

    # === CONFIG DRIFT COMPARISON ===
    if local_metadata:
        local_title = local_metadata.get("title", "")
        if local_title and title:
            title_sim = similarity(local_title, title)
            if title_sim < 0.8:
                warnings.append(f"DRIFT: title on Zenodo differs from config (similarity: {title_sim:.0%})")
                info.append(f"  Local:  {local_title[:60]}")
                info.append(f"  Zenodo: {title[:60]}")
            elif title_sim < 1.0:
                info.append(f"Title similarity: {title_sim:.0%}")

        local_desc = local_metadata.get("description", "")
        if local_desc and description:
            desc_sim = similarity(local_desc, description)
            if desc_sim < 0.7:
                warnings.append(f"DRIFT: description on Zenodo differs from config (similarity: {desc_sim:.0%})")

    return {
        "issues": issues,
        "warnings": warnings,
        "info": info
    }


def discover_deposit_ids(papers):
    """Extract Zenodo record IDs from discovered paper configs.

    Args:
        papers: Dict from discover_paper_configs()

    Returns:
        Dict mapping record_id -> paper_key
    """
    id_to_key = {}
    for key, info in papers.items():
        config = info["config"]
        metadata = config.get("metadata", {})

        # Check metadata.doi
        doi = metadata.get("doi", "")
        record_id = get_record_id_from_doi(doi)
        if record_id:
            id_to_key[record_id] = key
            continue

        # Check publishing.preprints for zenodo entry
        publishing = metadata.get("publishing", {})
        preprints = publishing.get("preprints", [])
        for preprint in preprints:
            if isinstance(preprint, dict) and preprint.get("platform") == "zenodo":
                preprint_doi = preprint.get("doi", "")
                record_id = get_record_id_from_doi(preprint_doi)
                if record_id:
                    id_to_key[record_id] = key
                    break

                # Try extracting from URL
                url = preprint.get("url", "")
                if "zenodo.org" in url and "/record/" in url:
                    try:
                        record_id = int(url.rstrip("/").split("/record/")[-1].split("?")[0])
                        id_to_key[record_id] = key
                    except ValueError:
                        pass
                break

    return id_to_key


def fetch_all_user_deposits(token, status=None):
    """Fetch all deposits for the authenticated user.

    Args:
        token: Zenodo API token
        status: Filter by status ('draft', 'published', or None for all)

    Returns:
        List of deposit dicts
    """
    headers = {"Authorization": f"Bearer {token}"}
    all_deposits = []
    page = 1

    while True:
        params = {"page": page, "size": 25}
        if status:
            params["status"] = status

        r = requests.get(f"{ZENODO_API}/deposit/depositions", headers=headers, params=params)
        if r.status_code == 403:
            print("WARNING: Token lacks deposit:read scope. Cannot list all deposits for duplicate check.")
            print("  Regenerate token with deposit:read at: https://zenodo.org/account/settings/applications/")
            break
        if r.status_code != 200:
            print(f"WARNING: Failed to fetch deposits page {page}: {r.status_code}")
            break

        data = r.json()
        if not isinstance(data, list) or not data:
            break

        all_deposits.extend(data)
        page += 1

        # Safety limit
        if page > 20:
            break

    return all_deposits


def check_duplicates(deposits, id_to_key, resolved_ids=None):
    """Check for duplicate deposits.

    Args:
        deposits: List of deposit dicts from Zenodo API
        id_to_key: Dict mapping concept record_id -> paper_key
        resolved_ids: Set of actual deposit IDs that concept IDs resolved to

    Returns list of finding dicts with type, message, and details.
    """
    findings = []

    # Check for similar titles
    titled_deposits = [(d["id"], d.get("metadata", {}).get("title", "")) for d in deposits if d.get("metadata", {}).get("title")]

    for i, (id_a, title_a) in enumerate(titled_deposits):
        for id_b, title_b in titled_deposits[i + 1:]:
            sim = similarity(title_a, title_b)
            if sim >= DUPLICATE_SIMILARITY_THRESHOLD:
                findings.append({
                    "type": "DUPLICATE",
                    "message": f'"{title_a[:50]}" (deposit {id_a}) and "{title_b[:50]}" (deposit {id_b}) appear to be duplicates (similarity: {sim:.0%})',
                    "ids": [id_a, id_b],
                })

    # Check for multiple configs pointing to the same record ID
    key_to_ids = {}
    for record_id, key in id_to_key.items():
        key_to_ids.setdefault(key, []).append(record_id)
    for key, ids in key_to_ids.items():
        if len(ids) > 1:
            findings.append({
                "type": "MULTI_ID",
                "message": f"Config '{key}' maps to multiple record IDs: {ids}",
                "ids": ids,
            })

    # Check for orphaned deposits (on Zenodo but no local config)
    # Include both concept IDs and resolved version IDs as "known"
    known_ids = set(id_to_key.keys()) | set(resolved_ids) if resolved_ids else set(id_to_key.keys())
    for deposit in deposits:
        dep_id = deposit["id"]
        if dep_id not in known_ids:
            title = deposit.get("metadata", {}).get("title", "Unknown")
            state = deposit.get("state", "unknown")
            findings.append({
                "type": "ORPHANED",
                "message": f'Deposit {dep_id} "{title[:50]}" exists on Zenodo but has no matching local config (state: {state})',
                "ids": [dep_id],
            })

    return findings


def write_todos(findings, drift_warnings, todo_path):
    """Append actionable findings to TODO.md.

    Args:
        findings: List of duplicate/orphan finding dicts
        drift_warnings: List of (paper_key, warning_message) tuples
        todo_path: Path to TODO.md
    """
    if not findings and not drift_warnings:
        return False

    # Check for existing audit section to avoid duplicates
    existing_content = ""
    if todo_path.exists():
        existing_content = todo_path.read_text(encoding="utf-8")

    date_str = datetime.now().strftime("%Y-%m-%d")
    lines = [f"\n## Zenodo Audit Findings ({date_str})\n"]

    for finding in findings:
        ftype = finding["type"]
        msg = finding["message"]
        if ftype == "DUPLICATE":
            lines.append(f"- [ ] DUPLICATE: {msg} - consolidate or remove one")
        elif ftype == "ORPHANED":
            lines.append(f"- [ ] ORPHANED: {msg} - archive or delete")
        elif ftype == "MULTI_ID":
            lines.append(f"- [ ] MULTI_ID: {msg} - verify which is correct")

    for key, warning in drift_warnings:
        if "DRIFT" in warning:
            lines.append(f"- [ ] DRIFT ({key}): {warning} - re-upload to sync")

    todo_text = "\n".join(lines) + "\n"

    # Don't add if identical entries already exist
    if todo_text.strip() in existing_content:
        print("[--] TODO entries already exist, skipping")
        return False

    with open(todo_path, "a", encoding="utf-8") as f:
        f.write(todo_text)

    print(f"[OK] Appended {len(findings) + len(drift_warnings)} items to {todo_path.name}")
    return True


def generate_report(results, duplicate_findings, papers, id_to_key, total_issues, total_warnings):
    """Generate a markdown audit report.

    Returns:
        Markdown string
    """
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Zenodo Publication Audit Report",
        f"",
        f"Generated: {date_str}",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Papers discovered | {len(papers)} |",
        f"| Records with Zenodo IDs | {len(id_to_key)} |",
        f"| Records audited | {len(results)} |",
        f"| Blocking issues | {total_issues} |",
        f"| Warnings | {total_warnings} |",
        f"| Duplicate/orphan findings | {len(duplicate_findings)} |",
        f"",
        f"## Records",
        f"",
    ]

    for record in results:
        if "error" in record:
            lines.append(f"### Deposit {record['id']} - FETCH FAILED")
            lines.append("")
            continue

        title = record.get("title", "Unknown")
        key_label = f" (`{record.get('paper_key')}`)" if record.get("paper_key") else ""
        lines.append(f"### {title}{key_label}")
        lines.append(f"")
        lines.append(f"- **Deposit ID**: {record['id']}")
        lines.append(f"- **State**: {record.get('state', 'unknown')}")
        lines.append(f"- **DOI**: {record.get('doi') or 'N/A'}")
        lines.append(f"- **Publisher**: {record.get('publisher') or 'N/A'}")
        lines.append(f"")

        audit = record.get("audit", {})
        if audit.get("issues"):
            lines.append("**Issues:**")
            for issue in audit["issues"]:
                lines.append(f"- {issue}")
            lines.append("")

        if audit.get("warnings"):
            lines.append("**Warnings:**")
            for warn in audit["warnings"]:
                lines.append(f"- {warn}")
            lines.append("")

        if not audit.get("issues") and not audit.get("warnings"):
            lines.append("All checks passed.")
            lines.append("")

    if duplicate_findings:
        lines.append("## Duplicate / Orphan Findings")
        lines.append("")
        for finding in duplicate_findings:
            lines.append(f"- **{finding['type']}**: {finding['message']}")
        lines.append("")

    return "\n".join(lines)


def run_audit(token, verbose=False, output_json=False, deposit_ids=None, write_todos_flag=False, report_path=None):
    """Run full audit of Zenodo records."""

    if not output_json:
        print("=" * 60)
        print("ZENODO PUBLICATION AUDIT")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    if not token:
        print("ERROR: No Zenodo token found")
        print("Set ZENODO_TOKEN env var or use --token flag")
        sys.exit(1)

    # Auto-discover papers and their Zenodo record IDs
    papers = discover_paper_configs(PROJECT_ROOT)
    id_to_key = discover_deposit_ids(papers)

    if not output_json:
        print(f"\nDiscovered {len(papers)} paper config(s), {len(id_to_key)} with Zenodo record IDs")
        if verbose:
            for record_id, key in sorted(id_to_key.items()):
                print(f"  {key}: record {record_id}")
            papers_without_id = set(papers.keys()) - set(id_to_key.values())
            if papers_without_id:
                print(f"  Papers without Zenodo ID: {', '.join(sorted(papers_without_id))}")

    # Determine which IDs to check
    if deposit_ids:
        ids_to_check = deposit_ids
    else:
        ids_to_check = sorted(id_to_key.keys())

    if not ids_to_check and not deposit_ids:
        print("WARNING: No Zenodo record IDs found in any config")
        print("  Make sure configs have DOIs set in metadata.doi or publishing.preprints[zenodo].doi")
        return []

    results = []
    total_issues = 0
    total_warnings = 0
    drift_warnings = []
    resolved_ids = set()  # Actual deposit IDs that concept IDs resolved to

    for deposit_id in ids_to_check:
        if not output_json:
            print(f"\n{'--' * 20}")
            print(f"Checking deposit {deposit_id}...")

        record = fetch_zenodo_record(deposit_id, token)
        if not record:
            if not output_json:
                print(f"  FAILED to fetch record")
            results.append({"id": deposit_id, "error": "fetch failed"})
            continue

        # Track resolved ID (concept ID may resolve to a different actual deposit ID)
        actual_id = record.get("id", deposit_id)
        resolved_ids.add(actual_id)
        resolved_ids.add(deposit_id)

        meta = record.get("metadata", {})
        title = meta.get("title", "Unknown")
        state = record.get("state", "unknown")
        paper_key = id_to_key.get(deposit_id)

        if not output_json:
            key_label = f" [{paper_key}]" if paper_key else ""
            print(f"  {title[:55]}{'...' if len(title) > 55 else ''}{key_label}")
            print(f"  State: {state}")

        # Get local metadata for drift comparison
        local_metadata = None
        if paper_key and paper_key in papers:
            local_metadata = extract_zenodo_metadata(papers[paper_key]["config"], paper_key)

        audit = audit_record(record, local_metadata=local_metadata)

        total_issues += len(audit["issues"])
        total_warnings += len(audit["warnings"])

        # Track drift warnings for --write-todos
        if paper_key:
            for w in audit["warnings"]:
                if "DRIFT" in w:
                    drift_warnings.append((paper_key, w))

        if not output_json:
            if audit["issues"]:
                for issue in audit["issues"]:
                    print(f"  [ISSUE] {issue}")

            if audit["warnings"]:
                for warn in audit["warnings"]:
                    print(f"  [WARN]  {warn}")

            if verbose and audit["info"]:
                for info_msg in audit["info"]:
                    print(f"  [INFO]  {info_msg}")

            if not audit["issues"] and not audit["warnings"]:
                print(f"  [OK] All checks passed")

        results.append({
            "id": deposit_id,
            "paper_key": paper_key,
            "title": meta.get("title"),
            "state": state,
            "doi": meta.get("doi"),
            "publisher": meta.get("publisher"),
            "audit": audit
        })

    # Duplicate detection: fetch all user deposits and compare
    duplicate_findings = []
    if not deposit_ids:  # Only run duplicate check on full audit
        if not output_json:
            print(f"\n{'--' * 20}")
            print("Checking for duplicates...")

        all_deposits = fetch_all_user_deposits(token)
        if all_deposits:
            duplicate_findings = check_duplicates(all_deposits, id_to_key, resolved_ids=resolved_ids)

            if not output_json:
                if duplicate_findings:
                    for finding in duplicate_findings:
                        print(f"  [WARN] {finding['type']}: {finding['message']}")
                else:
                    print(f"  [OK] No duplicates found among {len(all_deposits)} deposits")

    # Summary
    if not output_json:
        print(f"\n{'=' * 60}")
        print("SUMMARY")
        print(f"{'=' * 60}")
        print(f"Records checked: {len(ids_to_check)}")
        print(f"Issues (blocking): {total_issues}")
        print(f"Warnings: {total_warnings}")
        if duplicate_findings:
            print(f"Duplicate/orphan findings: {len(duplicate_findings)}")

        if total_issues > 0:
            print("\nIssues found that should be fixed!")
        elif total_warnings > 0 or duplicate_findings:
            print("\nNo blocking issues, but warnings to address")
        else:
            print("\nAll records look good!")

    # Write TODOs if requested
    if write_todos_flag:
        todo_path = PROJECT_ROOT / "TODO.md"
        write_todos(duplicate_findings, drift_warnings, todo_path)

    # Generate markdown report if requested
    if report_path:
        report_md = generate_report(results, duplicate_findings, papers, id_to_key, total_issues, total_warnings)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_md, encoding="utf-8")
        if not output_json:
            print(f"\n[OK] Report written to {report_path}")

    if output_json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "records_checked": len(ids_to_check),
                "total_issues": total_issues,
                "total_warnings": total_warnings,
                "duplicate_findings": len(duplicate_findings),
            },
            "records": results,
            "duplicates": duplicate_findings,
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
        help="Zenodo API token (or set ZENODO_TOKEN env var)"
    )
    parser.add_argument(
        "--ids",
        nargs="+",
        type=int,
        help="Specific deposit IDs to check (overrides auto-discovery)"
    )
    parser.add_argument(
        "--write-todos",
        action="store_true",
        help="Append actionable findings to TODO.md"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate markdown report at _analysis/zenodo-audit-report.md"
    )
    args = parser.parse_args()

    token = args.token or get_zenodo_token()

    report_path = None
    if args.report:
        report_path = PROJECT_ROOT / "_analysis" / "zenodo-audit-report.md"

    result = run_audit(
        token=token,
        verbose=args.verbose,
        output_json=args.json,
        deposit_ids=args.ids,
        write_todos_flag=args.write_todos,
        report_path=report_path,
    )

    if args.json:
        print(result)


if __name__ == "__main__":
    main()
