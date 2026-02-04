#!/usr/bin/env python3
"""
Papers QMD Generator
====================

Generates a knowledge/papers.qmd file with a nicely formatted listing
of all papers/sites from the Quarto YAML configs in the project root.

Usage:
    from dih_models.papers_qmd_generator import generate_papers_qmd
    generate_papers_qmd(project_root)

Output:
    knowledge/papers.qmd
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Add scripts directory to path for latex_utils import
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.latex_utils import sanitize_for_latex


def extract_paper_info(config_path: Path, config_name: str) -> Optional[Dict[str, Any]]:
    """
    Extract paper information from a Quarto config file.

    Args:
        config_path: Path to the _quarto-*.yml file
        config_name: Name of the config (e.g., "iab", "dfda-impact")

    Returns:
        Dict with paper info, or None if not a publishable paper
    """
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        return None

    # Skip test and manual configs
    if config_name in ("test", "manual"):
        return None

    # Extract from book or website section
    title = None
    description = None
    site_url = None

    if "book" in config:
        book = config["book"]
        title = book.get("title")
        description = book.get("description") or book.get("abstract")
        site_url = book.get("site-url")
    elif "website" in config:
        website = config["website"]
        title = website.get("title")
        description = website.get("description")
        site_url = website.get("site-url")

    # Skip if no title or URL
    if not title or not site_url:
        return None

    # Get metadata
    metadata = config.get("metadata", {})
    dih_render = config.get("dih-render", {})

    # Get PDF URL
    pdf_file = None
    if "format" in config and "pdf" in config["format"]:
        pdf_file = config["format"]["pdf"].get("output-file")
    if not pdf_file:
        pdf_file = dih_render.get("pdf-output-file")

    pdf_url = None
    if pdf_file and site_url:
        base_url = site_url.rstrip("/")
        pdf_url = f"{base_url}/{pdf_file}"

    # Get DOI
    doi = metadata.get("doi")
    doi_url = f"https://doi.org/{doi}" if doi else None

    # Get OG image - convert to relative path from knowledge/
    og_image = metadata.get("image", "")
    if og_image:
        # Strip site URL prefix if present
        if site_url and og_image.startswith(site_url):
            og_image = og_image[len(site_url.rstrip("/")):]
        # Strip leading slash and prepend ../ to make relative from knowledge/
        if og_image.startswith("/"):
            og_image = ".." + og_image
        elif not og_image.startswith((".", "http://", "https://")):
            # Relative path without leading slash - prepend ../
            og_image = "../" + og_image

    # Get keywords
    keywords = metadata.get("keywords", [])
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",")]

    # Get subject/category for grouping
    category = metadata.get("category", "")
    subject = metadata.get("subject", "")

    # Determine paper type/category for sorting
    paper_type = "Working Paper"
    if "book" in config:
        paper_type = "Book"
    elif metadata.get("format"):
        paper_type = metadata.get("format")

    return {
        "id": config_name,
        "title": title,
        "description": description,
        "site_url": site_url,
        "pdf_url": pdf_url,
        "doi": doi,
        "doi_url": doi_url,
        "og_image": og_image,
        "keywords": keywords[:5],  # Limit to 5 keywords for display
        "category": category,
        "subject": subject,
        "paper_type": paper_type,
        "edition": metadata.get("edition", ""),
        "version": metadata.get("version", ""),
    }


def generate_papers_qmd(project_root: Path, output_filename: str = "papers.qmd") -> Path:
    """
    Generate a QMD file listing all papers from Quarto configs.

    Args:
        project_root: Root directory of the project
        output_filename: Name of the output QMD file

    Returns:
        Path to the generated QMD file
    """
    # Find all _quarto-*.yml files in root
    quarto_configs = list(project_root.glob("_quarto-*.yml"))
    quarto_configs.sort(key=lambda p: p.name)

    papers = []
    for config_path in quarto_configs:
        match = re.match(r"_quarto-(.+)\.yml", config_path.name)
        if not match:
            continue

        config_name = match.group(1)

        try:
            paper_info = extract_paper_info(config_path, config_name)
            if paper_info:
                papers.append(paper_info)
        except Exception as e:
            print(f"[WARN] Failed to parse {config_path.name}: {e}")

    # Sort papers: Books first, then by title
    papers.sort(key=lambda p: (0 if p["paper_type"] == "Book" else 1, p["title"]))

    # Generate QMD content
    lines = [
        "---",
        "title: Papers & Publications",
        'description: "Academic papers and working drafts from the Disease Eradication Plan project."',
        "toc: true",
        "toc-depth: 2",
        "image: /assets/og-images/knowledge/papers-og-bw-academic.jpg",
        "aliases:",
        "  - /papers",
        "format:",
        "  html:",
        "    toc: true",
        "---",
        "",
        "This page provides an index of all academic papers, working drafts, and publications",
        "produced as part of the Disease Eradication Plan project.",
        "",
    ]

    # Group by type
    books = [p for p in papers if p["paper_type"] == "Book"]
    working_papers = [p for p in papers if p["paper_type"] != "Book"]

    if books:
        lines.append("## Books")
        lines.append("")
        for paper in books:
            lines.extend(_format_paper_entry(paper))

    if working_papers:
        lines.append("## Working Papers")
        lines.append("")
        for paper in working_papers:
            lines.extend(_format_paper_entry(paper))

    # Summary section
    lines.extend([
        "",
        "---",
        "",
    ])

    # Write output
    knowledge_dir = project_root / "knowledge"
    knowledge_dir.mkdir(exist_ok=True)
    output_path = knowledge_dir / output_filename

    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    print(f"[OK] Generated {output_path.relative_to(project_root)} with {len(papers)} papers")

    return output_path


def _format_paper_entry(paper: Dict[str, Any]) -> List[str]:
    """Format a single paper entry as QMD content."""
    lines = []

    # Title as link
    title = paper["title"]
    site_url = paper["site_url"]
    lines.append(f"### [{title}]({site_url})")
    lines.append("")

    # OG image as clickable thumbnail
    # Sanitize title for use in image caption (LaTeX compatibility)
    if paper.get("og_image"):
        safe_title = sanitize_for_latex(title)
        lines.append(f"[![{safe_title}]({paper['og_image']})]({site_url})")
        lines.append("")

    # Description
    if paper["description"]:
        # Truncate long descriptions
        desc = paper["description"]
        if len(desc) > 500:
            desc = desc[:497] + "..."
        lines.append(f"> {desc}")
        lines.append("")

    lines.append("")  # Extra spacing between entries

    return lines


def main():
    """CLI entry point."""
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

    project_root = Path(__file__).parent.parent.absolute()

    print("[*] Generating papers.qmd...")
    output_path = generate_papers_qmd(project_root)
    print(f"[OK] Output: {output_path}")


if __name__ == "__main__":
    main()
