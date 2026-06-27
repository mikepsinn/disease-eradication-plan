#!/usr/bin/env python3
"""
llms.txt Generator
==================

Generates llms.txt and robots.txt files from Quarto config metadata.

The llms.txt format follows the specification at https://llmstxt.org/
It provides LLM-friendly content describing the project and its papers.

robots.txt explicitly allows all major AI crawlers.

Usage:
    from dih_models.llms_txt_generator import generate_llms_txt, generate_robots_txt
    generate_llms_txt(project_root)
    generate_robots_txt(project_root)

Output:
    llms.txt in project root (copied to all site outputs via resources)
    robots.txt in project root
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from dih_models.yaml_utils import load_quarto_config

logger = logging.getLogger("dih.llms_txt")


def extract_site_info(config_path: Path, config_name: str) -> Optional[Dict[str, Any]]:
    """
    Extract minimal info needed for llms.txt from a Quarto config.

    Args:
        config_path: Path to the _quarto-*.yml file
        config_name: Name of the config (e.g., "dfda-spec", "iab")

    Returns:
        Dict with title, description, site_url, pdf_url or None if not a real site
    """
    config = load_quarto_config(config_path)

    if not config:
        return None

    # Skip test configs
    if config_name == "test":
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

    if not title:
        return None

    # Get PDF from format.pdf or dih-render
    dih_render = config.get("dih-render", {})
    pdf_file = None
    if "format" in config and "pdf" in config["format"]:
        pdf_file = config["format"]["pdf"].get("output-file")
    if not pdf_file:
        pdf_file = dih_render.get("pdf-output-file")

    # Build PDF URL
    pdf_url = None
    if pdf_file and site_url:
        base_url = site_url.rstrip("/")
        pdf_url = f"{base_url}/{pdf_file}"

    # Clean description (remove Quarto variable syntax for plain text)
    if description:
        # Remove {{< var ... >}} patterns - they won't render in plain text
        import re
        description = re.sub(r'\{\{<\s*var\s+[^>]+>\}\}', '[value]', description)

    return {
        "id": config_name,
        "title": title,
        "description": description or "",
        "site_url": site_url,
        "pdf_url": pdf_url,
    }


def _read_qmd_frontmatter(path: Path) -> Dict[str, Any]:
    """Parse the YAML frontmatter (title, description) out of a .qmd chapter."""
    import yaml

    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except Exception:
        return {}


def extract_book_chapters(project_root: Path) -> List[Dict[str, Any]]:
    """Walk the main book's chapter tree (_quarto-manual.yml) and pull each
    chapter's title + description from its .qmd frontmatter.

    Papers are covered by the Quarto-config pass; this covers the ACTUAL book
    chapters (proofs, solutions, problem analyses) that were previously invisible
    to llms.txt. Returns a list of parts: {"part": name, "chapters": [...]}.
    """
    import re

    config = load_quarto_config(project_root / "_quarto-manual.yml")
    if not config or "book" not in config:
        return []
    book = config["book"]
    site_url = (book.get("site-url") or "https://manual.warondisease.org").rstrip("/")

    def info(href: Optional[str]) -> Optional[Dict[str, str]]:
        if not href or not isinstance(href, str) or not href.endswith(".qmd"):
            return None
        meta = _read_qmd_frontmatter(project_root / href)
        title = meta.get("title") or href
        if isinstance(title, str):
            title = title.strip().strip('"').strip("'")
        desc = meta.get("description") or meta.get("abstract") or ""
        if isinstance(desc, str):
            desc = re.sub(r"\{\{<\s*var\s+[^>]+>\}\}", "[value]", desc)
            desc = re.sub(r"\s+", " ", desc).strip()
        else:
            desc = ""
        return {"title": str(title), "url": f"{site_url}/{href.replace('.qmd', '.html')}", "description": desc}

    parts: List[Dict[str, Any]] = []
    top: List[Dict[str, str]] = []
    for entry in book.get("chapters", []):
        if isinstance(entry, dict) and "part" in entry:
            chapters = []
            for c in entry.get("chapters", []):
                href = c if isinstance(c, str) else (c.get("href") if isinstance(c, dict) else None)
                ci = info(href)
                if ci:
                    chapters.append(ci)
            if chapters:
                parts.append({"part": entry["part"], "chapters": chapters})
        else:
            href = entry if isinstance(entry, str) else (entry.get("href") if isinstance(entry, dict) else None)
            ci = info(href)
            if ci:
                top.append(ci)
    if top:
        parts.insert(0, {"part": "Start Here", "chapters": top})
    return parts


def generate_llms_txt(project_root: Path) -> Path:
    """
    Generate llms.txt from all Quarto configs.

    Args:
        project_root: Root directory of the project

    Returns:
        Path to the generated llms.txt file
    """
    # Find all _quarto-*.yml files
    quarto_configs = sorted(project_root.glob("_quarto-*.yml"), key=lambda p: p.name)

    sites = []
    for config_path in quarto_configs:
        import re
        match = re.match(r"_quarto-(.+)\.yml", config_path.name)
        if not match:
            continue

        config_name = match.group(1)
        try:
            info = extract_site_info(config_path, config_name)
            if info and info.get("site_url"):
                sites.append(info)
        except Exception as e:
            logger.warning("Failed to parse %s for llms.txt: %s", config_path.name, e)

    # Build llms.txt content following the spec at llmstxt.org
    lines = [
        "# Disease Eradication Plan",
        "",
        "> Academic research project proposing the 1% Treaty: redirecting 1% of global military spending to pragmatic clinical trials. Contains peer-reviewed analyses, governance frameworks, and implementation strategies.",
        "",
        "This project consists of multiple interconnected research papers on health economics, regulatory reform, and democratic governance. All content is licensed under CC BY-NC 4.0.",
        "",
        "## Core Concepts",
        "",
        "- **1% Treaty**: International agreement to redirect 1% of military budgets to health research",
        "- **dFDA**: Framework for automated drug assessment using real-world evidence",
        "- **Predictor Impact Score**: Novel metric for causal inference from observational health data",
        "",
        "## Research Papers",
        "",
    ]

    # Add each site as a paper entry
    for site in sites:
        title = site["title"]
        url = site["site_url"]
        desc = site["description"]

        # Format: - [Title](url): Description
        # No truncation - LLMs can handle full descriptions
        if desc:
            lines.append(f"- [{title}]({url}): {desc}")
        else:
            lines.append(f"- [{title}]({url})")

    # Add the full book chapter map (papers were covered above; chapters were not).
    book_parts = extract_book_chapters(project_root)
    chapter_count = sum(len(p["chapters"]) for p in book_parts)
    if book_parts:
        lines.extend(["", "## Book: How to End War and Disease", ""])
        for part in book_parts:
            lines.append(f"### {part['part']}")
            lines.append("")
            for ch in part["chapters"]:
                if ch["description"]:
                    lines.append(f"- [{ch['title']}]({ch['url']}): {ch['description']}")
                else:
                    lines.append(f"- [{ch['title']}]({ch['url']})")
            lines.append("")

    lines.extend([
        "",
        "## Author",
        "",
        "Mike P. Sinn",
        "- Email: mike@warondisease.org",
        "- Website: https://mikesinn.com",
        "- ORCID: 0009-0006-0212-1094",
        "",
        "## Organization",
        "",
        "International Campaign to End War and Disease",
        "- Website: https://WarOnDisease.org",
        "",
        "## Source Code",
        "",
        "- [GitHub Repository](https://github.com/wishonia/earth-optimization-protocol)",
        "",
        "## License",
        "",
        "CC BY-NC 4.0 - Creative Commons Attribution-NonCommercial 4.0 International",
        "",
    ])

    # Write file
    output_path = project_root / "llms.txt"
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    logger.debug("Generated %s with %d papers and %d book chapters", output_path.name, len(sites), chapter_count)
    return output_path


def generate_robots_txt(project_root: Path) -> Path:
    """
    Generate robots.txt that allows all crawlers.

    User-agent: * with Allow: / permits all crawlers (including AI).
    No need to explicitly list each one.

    Args:
        project_root: Root directory of the project

    Returns:
        Path to the generated robots.txt file
    """
    content = """# robots.txt - Allow all crawlers (including AI)
# https://www.robotstxt.org/

User-agent: *
Allow: /
"""

    output_path = project_root / "robots.txt"
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    logger.debug("Generated %s", output_path.name)
    return output_path


def main():
    """CLI entry point."""
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

    project_root = Path(__file__).parent.parent.absolute()

    logger.debug("Generating llms.txt and robots.txt...")
    generate_robots_txt(project_root)
    generate_llms_txt(project_root)
    logger.debug("Done")


if __name__ == "__main__":
    main()
