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

from lib.latex_utils import sanitize_for_latex  # type: ignore[import-not-found]


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

    # Extract abstract (full text for submissions)
    abstract = None
    if "book" in config:
        abstract = config["book"].get("abstract") or config["book"].get("description")
    elif "website" in config:
        abstract = config["website"].get("description")

    # Extract author info from book.author or root author
    author_info: Dict[str, Any] = {}
    authors_list = None
    if "book" in config and "author" in config["book"]:
        authors_list = config["book"]["author"]
    elif "author" in config:
        authors_list = config["author"]
    if authors_list and isinstance(authors_list, list) and len(authors_list) > 0:
        first_author = authors_list[0]
        author_info["name"] = first_author.get("name", "")
        author_info["email"] = first_author.get("email", "")
        author_info["orcid"] = first_author.get("orcid", "")
        affiliations = first_author.get("affiliations", [])
        if affiliations and isinstance(affiliations, list):
            author_info["affiliation"] = affiliations[0].get("name", "")
        else:
            author_info["affiliation"] = ""

    return {
        "id": config_name,
        "title": title,
        "description": description,
        "site_url": site_url,
        "pdf_url": pdf_url,
        "pdf_file": pdf_file,
        "doi": doi,
        "doi_url": doi_url,
        "og_image": og_image,
        "keywords": keywords[:5],  # Limit to 5 keywords for display
        "all_keywords": keywords,  # Full list for submission block
        "category": category,
        "subject": subject,
        "paper_type": paper_type,
        "edition": metadata.get("edition", ""),
        "version": metadata.get("version", ""),
        "abstract": abstract,
        "author_info": author_info,
        "genre": metadata.get("genre", ""),
        "license": metadata.get("license", ""),
        "copyright_year": metadata.get("copyright-year", ""),
        "publishing": metadata.get("publishing", {}),
        "coi_statement": metadata.get("coi-statement", ""),
        "funding": metadata.get("funding", ""),
        "ethics_statement": metadata.get("ethics-statement", ""),
        "data_availability": metadata.get("data-availability", ""),
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

        lines.append("")
        for paper in books:
            lines.extend(_format_paper_entry(paper))
            lines.extend(_format_submission_block(paper))

    if working_papers:

        lines.append("")
        for paper in working_papers:
            lines.extend(_format_paper_entry(paper))
            lines.extend(_format_submission_block(paper))

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


def _unslugify_keyword(slug: str) -> str:
    """Convert a slugified keyword to title case: 'war-on-disease' -> 'War on Disease'."""
    # Handle all-caps acronyms (e.g., "RAPPA", "PAC", "dfda" -> "dFDA")
    known_acronyms = {"dfda", "dih", "roi", "pac", "rappa", "nsv"}
    if slug.lower() in known_acronyms:
        return slug.upper() if slug.lower() != "dfda" else "dFDA"
    words = slug.replace("-", " ").split()
    # Title-case but keep short prepositions lowercase
    small_words = {"on", "of", "the", "a", "an", "in", "for", "and", "or", "to", "vs"}
    result = []
    for i, word in enumerate(words):
        if i > 0 and word.lower() in small_words:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    return " ".join(result)


def _format_submission_block(paper: Dict[str, Any]) -> List[str]:
    """Format a hidden HTML comment block with copy/paste submission info."""
    lines = []
    title = paper["title"]
    lines.append("<!--")
    lines.append(f"=== SUBMISSION INFO: {title} ===")
    lines.append("")
    lines.append(f"TITLE: {title}")
    lines.append("")

    # Abstract
    abstract = paper.get("abstract") or paper.get("description") or ""
    if abstract:
        lines.append("ABSTRACT:")
        lines.append(abstract)
        lines.append("")

    # Author info
    author = paper.get("author_info", {})
    if author.get("name"):
        lines.append(f"AUTHOR: {author['name']}")
    if author.get("email"):
        lines.append(f"EMAIL: {author['email']}")
    if author.get("affiliation"):
        lines.append(f"AFFILIATION: {author['affiliation']}")
    if author.get("orcid"):
        lines.append(f"ORCID: {author['orcid']}")
    if author:
        lines.append("")

    # Keywords (un-slugified)
    all_keywords = paper.get("all_keywords", [])
    if all_keywords:
        display_keywords = [_unslugify_keyword(k) for k in all_keywords]
        lines.append(f"KEYWORDS: {', '.join(display_keywords)}")
        lines.append("")

    # Subject areas and category
    if paper.get("subject"):
        lines.append(f"SUBJECT AREAS: {paper['subject']}")
    if paper.get("category"):
        lines.append(f"CATEGORY: {paper['category']}")
    if paper.get("genre"):
        lines.append(f"GENRE: {paper['genre']}")
    if paper.get("subject") or paper.get("category") or paper.get("genre"):
        lines.append("")

    # PDF and identifiers
    if paper.get("pdf_url"):
        lines.append(f"PDF: {paper['pdf_url']}")
    if paper.get("doi"):
        lines.append(f"DOI: {paper['doi']}")
    if paper.get("license"):
        lines.append(f"LICENSE: {paper['license']}")
    if paper.get("copyright_year"):
        lines.append(f"COPYRIGHT YEAR: {paper['copyright_year']}")
    if paper.get("pdf_url") or paper.get("doi") or paper.get("license"):
        lines.append("")

    # Publishing status
    publishing = paper.get("publishing", {})
    if publishing:
        lines.append("--- PLATFORM STATUS ---")

        # Own site
        own_site = publishing.get("own-site", {})
        if own_site:
            lines.append(f"WEBSITE: {own_site.get('status', '')} | {own_site.get('url', '')}")

        # Preprints
        preprints = publishing.get("preprints", [])
        for pp in preprints:
            platform = pp.get("platform", "").upper()
            status = pp.get("status", "")
            url = pp.get("url", "")
            category_str = pp.get("category", "")
            parts = [status]
            if url:
                parts.append(url)
            if category_str:
                parts.append(f"category: {category_str}")
            lines.append(f"{platform}: {' | '.join(parts)}")

        lines.append("")

        # Journals
        journals = publishing.get("journals", [])
        if journals:
            lines.append("--- JOURNAL TARGETS ---")
            for j in journals:
                name = j.get("name", "")
                tier = j.get("tier", "")
                status = j.get("status", "")
                j_type = j.get("type", "")
                tier_str = f" (Tier {tier})" if tier else ""
                type_str = f" ({j_type})" if j_type else ""
                lines.append(f"{name}{tier_str}: {status}{type_str}")
            lines.append("")

    # Statements
    coi = paper.get("coi_statement", "")
    funding = paper.get("funding", "")
    ethics = paper.get("ethics_statement", "")
    data_avail = paper.get("data_availability", "")
    if coi or funding or ethics or data_avail:
        lines.append("--- STATEMENTS (for journal submissions) ---")
        if coi:
            lines.append(f"COI: {coi}")
        if funding:
            lines.append(f"FUNDING: {funding}")
        if ethics:
            lines.append(f"ETHICS: {ethics}")
        if data_avail:
            lines.append(f"DATA: {data_avail}")
        lines.append("")

    lines.append("-->")
    lines.append("")

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
