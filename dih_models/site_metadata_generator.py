#!/usr/bin/env python3
"""
Site Metadata Generator
=======================

Extracts metadata from all Quarto config files and generates a unified JSON file
containing site information (titles, descriptions, URLs, icons, OG images, etc.)
that can be used by other sites to display a list of papers/projects.

Usage:
    from dih_models.site_metadata_generator import generate_sites_metadata
    generate_sites_metadata(project_root)

Output:
    assets/sites-metadata.json
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def extract_site_metadata(config_path: Path, config_name: str) -> Optional[Dict[str, Any]]:
    """
    Extract relevant metadata from a single Quarto config file.

    Args:
        config_path: Path to the _quarto-*.yml file
        config_name: Name of the config (e.g., "book", "economics", "iab")

    Returns:
        Dict with site metadata, or None if not a publishable site
    """
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        return None

    # Skip test configs
    if config_name == "test":
        return None

    # Determine project type (book or website)
    project_type = config.get("project", {}).get("type", "website")

    # Extract title and description from book or website section
    title = None
    description = None
    abstract = None
    site_url = None
    favicon = None
    author = None

    if "book" in config:
        book = config["book"]
        title = book.get("title")
        description = book.get("description")
        abstract = book.get("abstract")
        site_url = book.get("site-url")
        favicon = book.get("favicon")
        author_data = book.get("author", [])
        if isinstance(author_data, list) and author_data:
            author = author_data[0].get("name") if isinstance(author_data[0], dict) else author_data[0]
        elif isinstance(author_data, str):
            author = author_data
    elif "website" in config:
        website = config["website"]
        title = website.get("title")
        description = website.get("description")
        site_url = website.get("site-url")
        favicon = website.get("favicon")

    # Skip if no title (not a real site config)
    if not title:
        return None

    # Get metadata section
    metadata = config.get("metadata", {})

    # Get dih-render section
    dih_render = config.get("dih-render", {})

    # Get PDF output file from format.pdf or dih-render
    pdf_file = None
    if "format" in config and "pdf" in config["format"]:
        pdf_file = config["format"]["pdf"].get("output-file")
    if not pdf_file:
        pdf_file = dih_render.get("pdf-output-file")

    # Build absolute URLs for favicon and OG image
    og_image = metadata.get("image", "")

    # If favicon is relative, make it absolute using site-url
    if favicon and site_url and not favicon.startswith("http"):
        # Clean up site URL (remove trailing slash)
        base_url = site_url.rstrip("/")
        # Clean up favicon path (remove leading slash if present)
        favicon_path = favicon.lstrip("/")
        favicon_url = f"{base_url}/{favicon_path}"
    else:
        favicon_url = favicon

    # Build PDF URL if we have a PDF file
    pdf_url = None
    if pdf_file and site_url:
        base_url = site_url.rstrip("/")
        pdf_url = f"{base_url}/{pdf_file}"

    # Extract keywords (can be string or list)
    keywords = metadata.get("keywords", [])
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",")]

    # Extract publishing info
    publishing = metadata.get("publishing", {})

    # Build the metadata object
    site_meta = {
        "id": config_name,
        "type": project_type,
        "title": title,
        "description": description or abstract or "",
        "abstract": abstract,
        "siteUrl": site_url,
        "favicon": favicon_url,
        "ogImage": og_image,
        "pdfUrl": pdf_url,
        "author": author or metadata.get("creator") or metadata.get("primary-author"),
        "authorEmail": metadata.get("author-email"),
        "authorUrl": metadata.get("author-url"),
        "orcid": metadata.get("orcid"),
        "doi": metadata.get("doi"),
        "version": metadata.get("version"),
        "edition": metadata.get("edition"),
        "copyright": metadata.get("copyright"),
        "copyrightYear": metadata.get("copyright-year"),
        "license": metadata.get("license"),
        "licenseUrl": metadata.get("license-url"),
        "publisher": metadata.get("publisher"),
        "publisherUrl": metadata.get("publisher-url"),
        "subject": metadata.get("subject"),
        "category": metadata.get("category"),
        "keywords": keywords,
        "audience": metadata.get("audience"),
        "format": metadata.get("format"),
        "genre": metadata.get("genre"),
        "language": metadata.get("language", "en-US"),
        "twitterSite": metadata.get("twitter-site"),
        "twitterCreator": metadata.get("twitter-creator"),
        # Netlify deployment info
        "netlify": {
            "siteId": dih_render.get("netlify-site-id"),
            "cname": dih_render.get("netlify-cname"),
        } if dih_render.get("netlify-site-id") else None,
        # Source file info
        "indexSource": dih_render.get("index-source"),
        "outputDir": config.get("project", {}).get("output-dir"),
        # Publishing status
        "publishing": {
            "ownSite": publishing.get("own-site"),
            "preprints": publishing.get("preprints", []),
            "journals": publishing.get("journals", []),
        } if publishing else None,
    }

    # Remove None values to keep JSON clean
    site_meta = {k: v for k, v in site_meta.items() if v is not None}

    return site_meta


def generate_sites_metadata(project_root: Path, output_filename: str = "sites-metadata.json") -> Path:
    """
    Generate a JSON file containing metadata for all Quarto sites.

    Args:
        project_root: Root directory of the project
        output_filename: Name of the output JSON file

    Returns:
        Path to the generated JSON file
    """
    # Find all _quarto-*.yml files in root (not _build_temp)
    quarto_configs = list(project_root.glob("_quarto-*.yml"))

    # Sort alphabetically for consistent output
    quarto_configs.sort(key=lambda p: p.name)

    sites = []

    for config_path in quarto_configs:
        # Extract config name from filename (e.g., "_quarto-book.yml" -> "book")
        match = re.match(r"_quarto-(.+)\.yml", config_path.name)
        if not match:
            continue

        config_name = match.group(1)

        try:
            site_meta = extract_site_metadata(config_path, config_name)
            if site_meta:
                sites.append(site_meta)
                print(f"[OK] Extracted metadata from {config_path.name}: {site_meta.get('title', 'Untitled')[:50]}")
        except Exception as e:
            print(f"[WARN] Failed to parse {config_path.name}: {e}")

    # Create output structure
    output_data = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "generatedAt": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "projectRoot": str(project_root),
        "totalSites": len(sites),
        "sites": sites,
    }

    # Write to assets folder
    assets_dir = project_root / "assets"
    assets_dir.mkdir(exist_ok=True)

    output_path = assets_dir / output_filename

    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated {output_path.relative_to(project_root)} with {len(sites)} sites")

    return output_path


def main():
    """CLI entry point."""
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    project_root = Path(__file__).parent.parent.absolute()

    print("[*] Generating site metadata JSON...")
    output_path = generate_sites_metadata(project_root)
    print(f"[OK] Output: {output_path}")


if __name__ == "__main__":
    main()
