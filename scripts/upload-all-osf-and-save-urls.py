#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload papers as OSF preprints (default provider: SocArXiv).

Correct OSF preprint flow:
1. Find or create a node (project) for the paper
2. Create preprint (provider + node + root subject)
3. Upload PDF to PREPRINT's own storage (NOT the node's)
4. PATCH primary_file relationship to point at the uploaded file
5. PATCH license
6. PATCH is_published = True (submits to SocArXiv moderation)

Setup:
    1. Sign up at https://osf.io
    2. Generate token at https://osf.io/settings/tokens (scope: osf.full_write)
    3. Add to .env:  OSF_TOKEN=...

Usage:
    python scripts/upload-all-osf-and-save-urls.py                     # all papers, SocArXiv
    python scripts/upload-all-osf-and-save-urls.py 1-percent-treaty    # one paper
    python scripts/upload-all-osf-and-save-urls.py --dry-run           # preview
    python scripts/upload-all-osf-and-save-urls.py --no-publish        # leave as drafts
    python scripts/upload-all-osf-and-save-urls.py --provider socarxiv
"""
from __future__ import annotations

import argparse
import io
import os
import sys
import time
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

sys.path.insert(0, str(Path(__file__).parent))

import requests
import yaml
from lib.quarto_config_utils import discover_paper_configs
from lib.python_utils import load_project_dotenv
from lib.zenodo_client import resolve_quarto_variables


PROJECT_ROOT = Path(__file__).parent.parent
OSF_API = "https://api.osf.io/v2"
OSF_FILES = "https://files.osf.io/v1"

PROVIDER_ALIASES = {
    "socarxiv": "socarxiv",
    "osf": "osf",
    "psyarxiv": "psyarxiv",
    "metaarxiv": "metaarxiv",
    "engrxiv": "engrxiv",
    "lawarxiv": "lawarxiv",
    "lissa": "lissa",
}


def p(*a, **kw):
    """Print with forced flush."""
    print(*a, **kw, flush=True)


class OSFError(RuntimeError):
    pass


def osf_request(method: str, url: str, token: str, **kwargs) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }
    if "headers" in kwargs:
        headers.update(kwargs.pop("headers"))
    resp = requests.request(method, url, headers=headers, timeout=120, **kwargs)
    if resp.status_code >= 400:
        raise OSFError(f"{method} {url} -> {resp.status_code}: {resp.text[:500]}")
    return resp.json() if resp.text else {}


def get_root_subjects(provider_id: str, token: str) -> dict[str, str]:
    """Return {text: id} of highlighted (root-level) subjects for the provider."""
    data = osf_request("GET", f"{OSF_API}/providers/preprints/{provider_id}/subjects/highlighted/", token)
    return {s["attributes"]["text"]: s["id"] for s in data.get("data", [])}


def find_existing_node(token: str, title: str) -> str | None:
    """Find a node owned by the user with a matching title. Returns node ID or None."""
    page = 1
    while True:
        data = osf_request("GET", f"{OSF_API}/users/me/nodes/?page[size]=100&page={page}", token)
        for n in data.get("data", []):
            if n.get("attributes", {}).get("title") == title:
                return n["id"]
        if not (data.get("links") or {}).get("next"):
            return None
        page += 1


def create_node(token: str, title: str, description: str) -> str:
    payload = {
        "data": {"type": "nodes", "attributes": {
            "title": title, "category": "data",
            "description": (description or title)[:1000], "public": True,
        }}
    }
    data = osf_request("POST", f"{OSF_API}/nodes/", token, json=payload)
    return data["data"]["id"]


def find_existing_preprint(token: str, provider_id: str, node_id: str) -> str | None:
    """Find an existing preprint linked to this node and provider. Returns preprint ID or None."""
    page = 1
    while True:
        data = osf_request("GET", f"{OSF_API}/users/me/preprints/?page[size]=100&page={page}", token)
        for pp in data.get("data", []):
            rels = pp.get("relationships", {})
            pp_node = ((rels.get("node") or {}).get("data") or {}).get("id")
            pp_prov = ((rels.get("provider") or {}).get("data") or {}).get("id")
            if pp_node == node_id and pp_prov == provider_id:
                return pp["id"]
        if not (data.get("links") or {}).get("next"):
            return None
        page += 1


def create_preprint(token: str, provider_id: str, node_id: str,
                    title: str, abstract: str, root_subject_id: str,
                    tags: list[str] | None = None) -> str:
    """Create a preprint. Returns the preprint's full ID (e.g. 'abcdef_v1')."""
    attrs = {
        "title": title,
        "description": (abstract or title)[:5000],
        "subjects": [[root_subject_id]],
        "tags": (tags or [])[:10],
    }
    payload = {
        "data": {"type": "preprints", "attributes": attrs, "relationships": {
            "node": {"data": {"type": "nodes", "id": node_id}},
            "provider": {"data": {"type": "preprint-providers", "id": provider_id}},
        }}
    }
    data = osf_request("POST", f"{OSF_API}/preprints/", token, json=payload)
    return data["data"]["id"]


def upload_pdf_to_preprint(token: str, preprint_id: str, pdf_path: Path) -> str:
    """Upload PDF to the preprint's storage. Returns the file's GUID.

    OSF requires the FULL preprint ID (including any '_vN' version suffix) here.
    """
    url = f"{OSF_FILES}/resources/{preprint_id}/providers/osfstorage/"
    headers = {"Authorization": f"Bearer {token}"}
    with pdf_path.open("rb") as f:
        # retry once on transient connection issues
        last_err = None
        for attempt in range(3):
            try:
                resp = requests.put(url, headers=headers,
                                    params={"kind": "file", "name": pdf_path.name},
                                    data=f.read() if attempt > 0 else f,
                                    timeout=300)
                break
            except requests.exceptions.RequestException as e:
                last_err = e
                f.seek(0)
                time.sleep(2 ** attempt)
        else:
            raise OSFError(f"Upload failed after retries: {last_err}")
    if resp.status_code >= 400:
        raise OSFError(f"Upload failed: {resp.status_code} {resp.text[:400]}")
    body = resp.json()
    file_path = body["data"]["attributes"]["path"]  # like "/69fd..."
    return file_path.lstrip("/")


def patch_primary_file(token: str, preprint_id: str, file_guid: str) -> None:
    payload = {"data": {"type": "preprints", "id": preprint_id,
                        "relationships": {"primary_file": {"data": {"type": "files", "id": file_guid}}}}}
    osf_request("PATCH", f"{OSF_API}/preprints/{preprint_id}/", token, json=payload)


def patch_license(token: str, preprint_id: str, license_name: str) -> None:
    license_text_map = {
        "CC BY-NC 4.0": "CC-By Attribution-NonCommercial 4.0 International",
        "CC BY 4.0": "CC-By Attribution 4.0 International",
        "CC0": "CC0 1.0 Universal",
    }
    text = license_text_map.get(license_name)
    if not text:
        return
    try:
        data = osf_request("GET", f"{OSF_API}/licenses/?filter[name]={requests.utils.quote(text)}", token)
        if not data.get("data"):
            return
        lic_id = data["data"][0]["id"]
        payload = {"data": {"type": "preprints", "id": preprint_id,
                            "relationships": {"license": {"data": {"type": "licenses", "id": lic_id}}}}}
        osf_request("PATCH", f"{OSF_API}/preprints/{preprint_id}/", token, json=payload)
    except OSFError as e:
        p(f"    [WARN] license set failed: {str(e)[:200]}")


def patch_publish(token: str, preprint_id: str) -> None:
    """Submit/publish preprint. Tries direct publish first; falls back to
    review_actions.submit for providers with moderation (e.g. SocArXiv).
    """
    payload = {"data": {"type": "preprints", "id": preprint_id,
                        "attributes": {"is_published": True}}}
    try:
        osf_request("PATCH", f"{OSF_API}/preprints/{preprint_id}/", token, json=payload)
    except OSFError as e:
        if "moderation workflow" in str(e) or "review_actions" in str(e):
            action = {"data": {
                "type": "review_actions",
                "attributes": {"trigger": "submit", "comment": "Submitted via API"},
                "relationships": {"target": {"data": {"type": "preprints", "id": preprint_id}}}
            }}
            osf_request("POST", f"{OSF_API}/preprints/{preprint_id}/review_actions/", token, json=action)
        else:
            raise


import re as _re

def _strip_confidence_intervals(text: str) -> str:
    """Remove (95% CI: ...) parentheticals — they make abstracts unreadable."""
    return _re.sub(r"\s*\(95% CI:\s*[^)]+\)", "", text)


def get_paper_metadata(paper_key: str, info: dict) -> dict:
    config = info["config"]
    pdf_path = PROJECT_ROOT / "assets" / "pdfs" / info["pdf_filename"]

    # Title: try website.title -> book.title -> qmd frontmatter title -> paper_key
    title = (
        (config.get("website") or {}).get("title")
        or (config.get("book") or {}).get("title")
    )
    qmd_fm = {}
    index_source = (config.get("dih-render") or {}).get("index-source")
    if index_source:
        qmd = PROJECT_ROOT / index_source
        if qmd.exists():
            text = qmd.read_text(encoding="utf-8", errors="replace")
            if text.startswith("---"):
                end = text.find("\n---", 3)
                if end > 0:
                    try:
                        qmd_fm = yaml.safe_load(text[3:end].strip()) or {}
                    except Exception:
                        qmd_fm = {}
    if not title:
        title = qmd_fm.get("title") or paper_key

    # Abstract: prefer qmd frontmatter abstract, then book/website description
    abstract = (
        qmd_fm.get("abstract")
        or qmd_fm.get("description")
        or (config.get("website") or {}).get("description")
        or (config.get("book") or {}).get("description")
        or title
    )
    abstract = resolve_quarto_variables(abstract, PROJECT_ROOT).replace("\\$", "$").strip()
    abstract = _strip_confidence_intervals(abstract)
    title = resolve_quarto_variables(title, PROJECT_ROOT).strip()

    keywords = ((config.get("metadata") or {}).get("keywords")) or []
    tags = [str(k) for k in keywords[:10]] if isinstance(keywords, list) else []

    license_name = (config.get("metadata") or {}).get("license") or "CC BY-NC 4.0"
    zenodo_doi = (config.get("metadata") or {}).get("doi")

    return {
        "title": title, "abstract": abstract, "tags": tags,
        "license": license_name, "pdf_path": pdf_path, "zenodo_doi": zenodo_doi,
    }


def save_osf_url_to_config(config_path: Path, preprint_id: str, preprint_url: str) -> None:
    text = config_path.read_text(encoding="utf-8")
    if "platform: osf" in text:
        return
    osf_block = (f"      - platform: osf\n"
                 f"        status: published\n"
                 f"        url: \"{preprint_url}\"\n"
                 f"        id: \"{preprint_id}\"\n")
    if "      - platform: zenodo" in text:
        idx = text.find("      - platform: zenodo")
        # find end of zenodo block: next "      - platform:" or "    journals:" or end of preprints list
        next_platform = text.find("\n      - platform:", idx + 5)
        next_section = text.find("\n    journals:", idx)
        candidates = [c for c in [next_platform, next_section] if c > 0]
        if candidates:
            insert_at = min(candidates)
            text = text[:insert_at] + "\n" + osf_block.rstrip() + text[insert_at:]
            config_path.write_text(text, encoding="utf-8")
            return
    p(f"    [WARN] could not auto-insert osf entry into {config_path.name}")


def already_published_to_osf(config_path: Path) -> bool:
    text = config_path.read_text(encoding="utf-8")
    return "platform: osf" in text and "status: published" in text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("papers", nargs="*")
    ap.add_argument("--provider", default="socarxiv", choices=list(PROVIDER_ALIASES.keys()))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-publish", action="store_true", help="leave as draft instead of submitting")
    ap.add_argument("--force", action="store_true", help="re-upload even if config has osf URL")
    args = ap.parse_args()

    load_project_dotenv(PROJECT_ROOT)
    token = os.environ.get("OSF_TOKEN")
    if not token:
        p("[ERROR] OSF_TOKEN not set in .env")
        p("  Sign up at https://osf.io")
        p("  Generate token: https://osf.io/settings/tokens (scope: osf.full_write)")
        return 1

    provider_id = PROVIDER_ALIASES[args.provider]
    p(f"Provider: {provider_id}")

    if args.dry_run:
        p("[DRY-RUN] using placeholder subject")
        root_subject = "DRY-RUN"
    else:
        p("Loading root subjects...")
        roots = get_root_subjects(provider_id, token)
        if not roots:
            p("[ERROR] no root subjects available")
            return 1
        # Prefer Social and Behavioral Sciences for SocArXiv
        for prefer in ["Social and Behavioral Sciences", "Education", "Law", "Medicine and Health Sciences"]:
            if prefer in roots:
                root_subject = roots[prefer]
                p(f"  Using root subject: {prefer} ({root_subject})")
                break
        else:
            name, root_subject = next(iter(roots.items()))
            p(f"  Using fallback root subject: {name} ({root_subject})")

    papers = discover_paper_configs(PROJECT_ROOT)
    if args.papers:
        papers = {k: v for k, v in papers.items() if k in args.papers}
    p(f"\nProcessing {len(papers)} paper(s):")

    ok, fail, skip = 0, 0, 0
    for key, info in papers.items():
        p(f"\n=== {key} ===")
        try:
            if not args.force and already_published_to_osf(info["config_path"]):
                p("  [SKIP] already published to OSF (use --force to override)")
                skip += 1
                continue

            meta = get_paper_metadata(key, info)
            p(f"  Title: {meta['title']}")
            p(f"  PDF:   {meta['pdf_path'].name} ({meta['pdf_path'].stat().st_size//1024} KB)")
            if not meta["pdf_path"].exists():
                p(f"  [SKIP] PDF missing")
                skip += 1
                continue

            if args.dry_run:
                p("  [DRY-RUN] would create preprint, upload PDF, set primary_file, submit")
                continue

            # 1. Find or create node
            existing_node = find_existing_node(token, meta["title"])
            if existing_node:
                p(f"  Reusing existing node: {existing_node}")
                node_id = existing_node
            else:
                p("  Creating node...")
                node_id = create_node(token, meta["title"], meta["abstract"])
                p(f"    node: {node_id}")

            # 2. Find or create preprint linked to this node
            existing_pp = find_existing_preprint(token, provider_id, node_id)
            if existing_pp:
                p(f"  Reusing existing preprint: {existing_pp}")
                preprint_id = existing_pp
            else:
                p(f"  Creating preprint on {provider_id}...")
                preprint_id = create_preprint(
                    token, provider_id, node_id,
                    title=meta["title"], abstract=meta["abstract"],
                    root_subject_id=root_subject, tags=meta["tags"],
                )
                p(f"    preprint: {preprint_id}")

            # 3. Upload PDF to preprint storage
            p("  Uploading PDF to preprint storage...")
            file_guid = upload_pdf_to_preprint(token, preprint_id, meta["pdf_path"])
            p(f"    file: {file_guid}")

            # 4. Set primary_file
            p("  Setting primary_file...")
            patch_primary_file(token, preprint_id, file_guid)

            # 5. License
            p("  Setting license...")
            patch_license(token, preprint_id, meta["license"])

            # 6. Publish (or skip)
            if args.no_publish:
                p("  [--no-publish] leaving as draft")
            else:
                p("  Submitting...")
                patch_publish(token, preprint_id)

            preprint_url = f"https://osf.io/preprints/{provider_id}/{preprint_id}"
            p(f"  [OK] {preprint_url}")
            save_osf_url_to_config(info["config_path"], preprint_id, preprint_url)
            ok += 1
            time.sleep(1)
        except OSFError as e:
            p(f"  [FAIL] {e}")
            fail += 1
        except Exception as e:
            p(f"  [FAIL] unexpected: {type(e).__name__}: {e}")
            fail += 1

    p(f"\n=== Summary ===")
    p(f"  OK:    {ok}")
    p(f"  Fail:  {fail}")
    p(f"  Skip:  {skip}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
