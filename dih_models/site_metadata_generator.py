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

from dih_models.search_index_generator import SearchIndexGenerator, SearchIndexEntry
from scripts.lib.yaml_sync_utils import substitute_quarto_variables


def extract_site_metadata(config_path: Path, config_name: str, variables: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Extract relevant metadata from a single Quarto config file.

    Args:
        config_path: Path to the _quarto-*.yml file
        config_name: Name of the config (e.g., "book", "economics", "iab")
        variables: Dictionary from _variables.yml for substituting Quarto variables

    Returns:
        Dict with site metadata, or None if not a publishable site
    """
    if variables is None:
        variables = {}
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

    # Substitute Quarto variables with plain text values
    if title:
        title = substitute_quarto_variables(title, variables)
    if description:
        description = substitute_quarto_variables(description, variables)
    if abstract:
        abstract = substitute_quarto_variables(abstract, variables)

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


def extract_pages_for_site(search_generator: SearchIndexGenerator, config_name: str) -> List[Dict[str, Any]]:
    """
    Extract page-level metadata for a site using the search index generator.

    Args:
        search_generator: Initialized SearchIndexGenerator instance
        config_name: Name of the config (e.g., "manual", "economics")

    Returns:
        List of page metadata dictionaries
    """
    config = search_generator.quarto_configs.get(config_name)
    if not config:
        return []

    base_url = config.get("base_url", "").rstrip("/")
    entries = search_generator.generate_index_for_config(config_name)

    pages = []
    for entry in entries:
        # Build absolute URL for this page
        page_url = f"{base_url}{entry.url}" if base_url else entry.url

        # Build absolute image URL if relative
        image_url = entry.image
        if image_url and not image_url.startswith("http"):
            image_url = f"{base_url}/{image_url.lstrip('/')}" if base_url else image_url

        page_meta = {
            "path": entry.path,
            "url": page_url,
            "title": entry.title,
            "description": entry.description,
            "image": image_url,
            "tags": entry.tags if entry.tags else None,
            "sections": entry.sections if entry.sections else None,
            "published": entry.published,
            "lastmod": entry.lastmod,
        }

        # Remove None values to keep JSON clean
        page_meta = {k: v for k, v in page_meta.items() if v is not None}
        pages.append(page_meta)

    return pages


def generate_sites_metadata(
    project_root: Path,
    output_filename: str = "sites-metadata.json",
    search_generator: Optional[SearchIndexGenerator] = None,
) -> Path:
    """
    Generate a JSON file containing metadata for all Quarto sites.

    Args:
        project_root: Root directory of the project
        output_filename: Name of the output JSON file
        search_generator: Optional pre-initialized SearchIndexGenerator instance.
                          If provided, reuses it instead of creating a new one
                          (avoids re-parsing all YAML configs and _variables.yml).

    Returns:
        Path to the generated JSON file
    """
    # Find all _quarto-*.yml files in root (not _build_temp)
    quarto_configs = list(project_root.glob("_quarto-*.yml"))

    # Sort alphabetically for consistent output
    quarto_configs.sort(key=lambda p: p.name)

    # Load variables for Quarto variable substitution
    variables_path = project_root / "_variables.yml"
    variables = {}
    if variables_path.exists():
        with open(variables_path, encoding="utf-8") as f:
            variables = yaml.safe_load(f) or {}
        print(f"[OK] Loaded {len(variables)} variables from _variables.yml")
    else:
        print("[WARN] _variables.yml not found - Quarto variables will not be substituted")

    # Reuse existing search generator if provided, otherwise create new one
    if search_generator is None:
        search_generator = SearchIndexGenerator(project_root)

    sites = []

    for config_path in quarto_configs:
        # Extract config name from filename (e.g., "_quarto-manual.yml" -> "book")
        match = re.match(r"_quarto-(.+)\.yml", config_path.name)
        if not match:
            continue

        config_name = match.group(1)

        try:
            site_meta = extract_site_metadata(config_path, config_name, variables)
            if site_meta:
                # Add pages array if this config is known to search generator
                if config_name in search_generator.quarto_configs:
                    pages = extract_pages_for_site(search_generator, config_name)
                    site_meta["pages"] = pages
                    site_meta["pageCount"] = len(pages)

                sites.append(site_meta)
                page_count = site_meta.get("pageCount", 0)
                print(f"[OK] Extracted metadata from {config_path.name}: {site_meta.get('title', 'Untitled')[:50]} ({page_count} pages)")
        except Exception as e:
            print(f"[WARN] Failed to parse {config_path.name}: {e}")

    # Calculate total pages across all sites
    total_pages = sum(site.get("pageCount", 0) for site in sites)

    # Create output structure
    output_data = {
        "totalSites": len(sites),
        "totalPages": total_pages,
        "sites": sites,
    }

    # Write to assets/json folder
    assets_dir = project_root / "assets" / "json"
    assets_dir.mkdir(parents=True, exist_ok=True)

    output_path = assets_dir / output_filename

    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated {output_path.relative_to(project_root)} with {len(sites)} sites, {total_pages} total pages")

    return output_path


def main():
    """CLI entry point."""
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

    project_root = Path(__file__).parent.parent.absolute()

    print("[*] Generating site metadata JSON...")
    output_path = generate_sites_metadata(project_root)
    print(f"[OK] Output: {output_path}")


if __name__ == "__main__":
    main()
