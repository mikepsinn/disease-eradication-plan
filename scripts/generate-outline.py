#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Project Outline
========================

Generates OUTLINE.md with complete project structure from ALL Quarto configs.
Shows chapters with titles, descriptions, section headings, orphaned files,
paper citations, and health check results.

Usage:
    python scripts/generate-outline.py
"""

import re
import sys
import yaml
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Set UTF-8 encoding for stdout and stderr on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]


def extract_headings_from_file(filepath: Path) -> List[Tuple[int, str]]:
    """Extract all headings from a .qmd file, ignoring code blocks."""
    if not filepath.exists():
        return []

    headings = []
    in_code_block = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith('```'):
                    in_code_block = not in_code_block
                    continue

                if in_code_block:
                    continue

                match = re.match(r'^(#{1,6})\s+(.+)$', line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2).strip()
                    if text:
                        headings.append((level, text))

    except Exception as e:
        print(f"Warning: Error reading {filepath}: {e}", file=sys.stderr)
        return []

    return headings


def format_heading(level: int, text: str) -> str:
    """Format a heading with tree-style indentation."""
    indent = "  " * (level - 1)
    return f"{indent}- {text}"


def extract_frontmatter(filepath: Path) -> Dict:
    """Extract YAML frontmatter from a QMD file."""
    if not filepath.exists():
        return {}

    try:
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        if lines and lines[0].strip() == '---':
            end_idx = None
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_idx = i
                    break

            if end_idx:
                frontmatter_text = '\n'.join(lines[1:end_idx])
                return yaml.safe_load(frontmatter_text) or {}
    except Exception:
        pass

    return {}


def get_qmd_stats(filepath: Path) -> Dict[str, int]:
    """Get word and line count for a QMD file."""
    if not filepath.exists():
        return {"words": 0, "lines": 0}

    try:
        content = filepath.read_text(encoding='utf-8')
        return {
            "words": len(content.split()),
            "lines": len(content.split('\n')),
        }
    except Exception:
        return {"words": 0, "lines": 0}


def get_all_included_files(project_root: Path) -> Set[str]:
    """Get all QMD files included in any _quarto-*.yml config."""
    included = set()

    for config_path in project_root.glob("_quarto-*.yml"):
        if "shared-defaults" in config_path.name:
            continue

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        except Exception:
            continue

        def collect_files(items):
            if not items:
                return
            for item in items:
                if isinstance(item, str):
                    if item.endswith('.qmd'):
                        included.add(item)
                elif isinstance(item, dict):
                    if 'href' in item and item['href'].endswith('.qmd'):
                        included.add(item['href'])
                    if 'file' in item and item['file'].endswith('.qmd'):
                        included.add(item['file'])
                    for key in ('chapters', 'contents', 'parts', 'sections', 'appendices'):
                        if key in item:
                            collect_files(item[key])

        # Check dih-render.index-source (single-file paper configs)
        dih_render = config.get('dih-render', {})
        if dih_render:
            index_source = dih_render.get('index-source', '')
            if index_source and index_source.endswith('.qmd'):
                included.add(index_source)

        # Book chapters
        if 'book' in config:
            collect_files(config['book'].get('chapters', []))
            collect_files(config['book'].get('appendices', []))

        # Website sidebar
        if 'website' in config:
            sidebar = config['website'].get('sidebar', {})
            if isinstance(sidebar, list):
                for s in sidebar:
                    if isinstance(s, dict):
                        collect_files(s.get('contents', []))
            elif isinstance(sidebar, dict):
                collect_files(sidebar.get('contents', []))

        # Project render list
        if 'project' in config:
            collect_files(config['project'].get('render', []))

    return included


def find_orphaned_qmd_files(project_root: Path, included_files: Set[str]) -> List[Tuple[Path, Dict]]:
    """Find QMD files in knowledge/ not in any Quarto config."""
    orphans = []

    knowledge_dir = project_root / "knowledge"
    if not knowledge_dir.exists():
        return orphans

    for qmd_file in knowledge_dir.rglob("*.qmd"):
        rel_path = str(qmd_file.relative_to(project_root)).replace("\\", "/")

        if rel_path in included_files:
            continue

        # Skip auto-generated and special files
        if "parameters-and-calculations" in rel_path:
            continue
        if "/figures/" in rel_path:
            continue
        if "/includes/" in rel_path:
            continue

        fm = extract_frontmatter(qmd_file)
        orphans.append((qmd_file, fm))

    orphans.sort(key=lambda x: str(x[0]))
    return orphans


def get_paper_configs(project_root: Path) -> List[Dict]:
    """Get all paper configs with citation info."""
    papers = []

    for config_path in project_root.glob("_quarto-*.yml"):
        match = re.match(r"_quarto-(.+)\.yml", config_path.name)
        if not match:
            continue

        config_name = match.group(1)
        if config_name in ("manual", "test", "shared-defaults"):
            continue

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        except Exception:
            continue

        title = None
        site_url = None
        if "book" in config:
            title = config["book"].get("title")
            site_url = config["book"].get("site-url")
        elif "website" in config:
            title = config["website"].get("title")
            site_url = config["website"].get("site-url")

        if not title:
            continue

        metadata = config.get("metadata", {}) or {}
        doi = metadata.get("doi")
        if not doi:
            publishing = metadata.get("publishing", {}) or {}
            preprints = publishing.get("preprints", []) or []
            for preprint in preprints:
                if preprint.get("doi"):
                    doi = preprint["doi"]
                    break

        year = metadata.get("copyright-year", str(date.today().year))
        cite_key = f"{config_name}-paper-{year}"

        papers.append({
            "config_name": config_name,
            "config_file": config_path.name,
            "title": title,
            "cite_key": cite_key,
            "doi": doi or "",
            "url": site_url or "",
        })

    papers.sort(key=lambda x: x["config_name"])
    return papers


def extract_chapters_from_config(config: Dict, project_root: Path) -> List[Dict[str, Any]]:
    """Extract all chapters with metadata from a config."""
    chapters = []

    def process_items(items, current_part: str = "", is_appendix: bool = False):
        if not items:
            return

        for item in items:
            if isinstance(item, str):
                if item.endswith('.qmd'):
                    qmd_path = project_root / item
                    fm = extract_frontmatter(qmd_path)
                    stats = get_qmd_stats(qmd_path)
                    chapters.append({
                        "part": current_part,
                        "href": item,
                        "title": fm.get("title", Path(item).stem),
                        "description": fm.get("description", ""),
                        "words": stats["words"],
                        "lines": stats["lines"],
                        "exists": qmd_path.exists(),
                        "is_appendix": is_appendix,
                    })
            elif isinstance(item, dict):
                if 'part' in item:
                    part_name = item['part']
                    if 'chapters' in item:
                        process_items(item['chapters'], part_name, is_appendix)
                    if 'contents' in item:
                        process_items(item['contents'], part_name, is_appendix)
                elif 'section' in item:
                    section_name = item['section']
                    if 'contents' in item:
                        process_items(item['contents'], current_part, is_appendix)
                    if 'chapters' in item:
                        process_items(item['chapters'], current_part, is_appendix)
                elif 'href' in item:
                    href = item['href']
                    if href.endswith('.qmd'):
                        qmd_path = project_root / href
                        fm = extract_frontmatter(qmd_path)
                        stats = get_qmd_stats(qmd_path)
                        chapters.append({
                            "part": current_part,
                            "href": href,
                            "title": item.get("text", fm.get("title", Path(href).stem)),
                            "description": fm.get("description", ""),
                            "words": stats["words"],
                            "lines": stats["lines"],
                            "exists": qmd_path.exists(),
                            "is_appendix": is_appendix,
                        })

    # Book chapters
    book = config.get('book', {})
    if book.get('chapters'):
        process_items(book['chapters'])
    if book.get('appendices'):
        process_items(book['appendices'], is_appendix=True)

    # Website sidebar
    website = config.get('website', {})
    if website.get('sidebar'):
        sidebar = website['sidebar']
        if isinstance(sidebar, list):
            for s in sidebar:
                if isinstance(s, dict) and s.get('contents'):
                    process_items(s['contents'])
        elif isinstance(sidebar, dict) and sidebar.get('contents'):
            process_items(sidebar['contents'])

    # dih-render index-source (single-file papers)
    dih_render = config.get('dih-render', {})
    if dih_render:
        index_source = dih_render.get('index-source', '')
        if index_source and index_source.endswith('.qmd'):
            qmd_path = project_root / index_source
            fm = extract_frontmatter(qmd_path)
            stats = get_qmd_stats(qmd_path)
            chapters.append({
                "part": "",
                "href": index_source,
                "title": fm.get("title", Path(index_source).stem),
                "description": fm.get("description", ""),
                "words": stats["words"],
                "lines": stats["lines"],
                "exists": qmd_path.exists(),
                "is_appendix": False,
            })

    return chapters


def generate_outline(project_root: Path) -> str:
    """Generate complete project outline from all Quarto configs."""
    outline_lines = []
    config_summaries = []

    # Find all Quarto configs
    configs = sorted(project_root.glob("_quarto-*.yml"))
    configs = [c for c in configs if "shared-defaults" not in c.name]

    # Process each config
    for config_path in configs:
        config_name = re.match(r"_quarto-(.+)\.yml", config_path.name).group(1)

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        except Exception:
            continue

        # Get title
        title = (
            config.get('book', {}).get('title') or
            config.get('website', {}).get('title') or
            config_name.replace('-', ' ').title()
        )

        # Get project type
        project_type = config.get('project', {}).get('type', 'website')

        # Extract chapters
        chapters = extract_chapters_from_config(config, project_root)

        # Calculate totals
        total_words = sum(c['words'] for c in chapters)
        missing_files = [c for c in chapters if not c['exists']]

        config_summaries.append({
            "name": config_name,
            "file": config_path.name,
            "title": title,
            "type": project_type,
            "chapters": chapters,
            "total_words": total_words,
            "missing_files": missing_files,
        })

    # Build outline header
    outline_lines.extend([
        "# Project Outline",
        "",
        "**Quarto Project Overview:**",
        f"- Total configs: {len(config_summaries)}",
        f"- Total QMD files: {len(set(c['href'] for cs in config_summaries for c in cs['chapters']))}",
        "",
        "---",
        "",
    ])

    # Add each config section
    for cs in config_summaries:
        outline_lines.extend([
            f"## {cs['file']}",
            f"**Title:** {cs['title']}",
            f"**Type:** {cs['type']}",
            f"**Files:** {len(cs['chapters'])} | **Words:** {cs['total_words']:,}",
            "",
        ])

        if cs['missing_files']:
            outline_lines.append(f"**Missing:** {len(cs['missing_files'])} files")
            outline_lines.append("")

        # Group chapters by part
        current_part = None
        for ch in cs['chapters']:
            if ch['part'] != current_part:
                current_part = ch['part']
                if current_part:
                    outline_lines.append(f"### {current_part}")
                    outline_lines.append("")

            # Add chapter info
            status = "" if ch['exists'] else " (NOT FOUND)"
            outline_lines.append(f"#### {ch['href']}{status}")
            outline_lines.append(f"**Title:** {ch['title']}")
            if ch['description']:
                desc = ch['description'][:200] + ('...' if len(ch['description']) > 200 else '')
                outline_lines.append(f"**Description:** {desc}")
            outline_lines.append(f"**Stats:** {ch['words']:,} words | {ch['lines']:,} lines")
            outline_lines.append("")

            # Add section headings
            if ch['exists']:
                full_path = project_root / ch['href']
                headings = extract_headings_from_file(full_path)
                if headings:
                    for level, text in headings:
                        outline_lines.append(format_heading(level, text))
                    outline_lines.append("")

        outline_lines.append("---")
        outline_lines.append("")

    # Add orphaned files section
    all_included = get_all_included_files(project_root)
    orphans = find_orphaned_qmd_files(project_root, all_included)

    if orphans:
        outline_lines.extend([
            "## ORPHANED FILES (not in any config)",
            "",
            f"*{len(orphans)} QMD files in knowledge/ not in any Quarto config:*",
            "",
        ])

        for qmd_path, fm in orphans:
            rel_path = str(qmd_path.relative_to(project_root)).replace("\\", "/")
            title = fm.get('title', qmd_path.stem)
            description = fm.get('description', '')
            stats = get_qmd_stats(qmd_path)

            outline_lines.append(f"#### {rel_path}")
            outline_lines.append(f"- **Title:** {title}")
            if description:
                desc = description[:100] + ('...' if len(description) > 100 else '')
                outline_lines.append(f"- **Description:** {desc}")
            outline_lines.append(f"- **Words:** {stats['words']:,}")
            outline_lines.append("")

        outline_lines.append("---")
        outline_lines.append("")

    # Add paper citations section
    papers = get_paper_configs(project_root)
    if papers:
        outline_lines.extend([
            "## PAPER CITATIONS (for Quarto cross-references)",
            "",
            "*Use these citation keys to reference papers in other chapters:*",
            "",
            "| Config | Title | Citation Key | DOI |",
            "|--------|-------|--------------|-----|",
        ])
        for p in papers:
            title_short = p['title'][:50] + ('...' if len(p['title']) > 50 else '')
            doi_str = p['doi'] if p['doi'] else '-'
            outline_lines.append(f"| {p['config_file']} | {title_short} | `@{p['cite_key']}` | {doi_str} |")
        outline_lines.extend([
            "",
            "**Usage:** `[@dfda-impact-paper-2025]` or `@dfda-impact-paper-2025`",
            "",
            "---",
            "",
        ])

    # Add summary
    unique_files = set(c['href'] for cs in config_summaries for c in cs['chapters'])
    total_words = sum(cs['total_words'] for cs in config_summaries)

    outline_lines.extend([
        "## SUMMARY",
        "",
        f"- Quarto configs: {len(config_summaries)}",
        f"- Unique QMD files: {len(unique_files)}",
        f"- Total words: {total_words:,}",
        f"- Orphaned files: {len(orphans)}",
        f"- Paper configs: {len(papers)}",
    ])

    return "\n".join(outline_lines)


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Generate outline
    outline = generate_outline(project_root)

    # Always write to OUTLINE.md
    output_path = project_root / "OUTLINE.md"
    try:
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(outline)
        print(f"Outline written to {output_path}")
    except Exception as e:
        print(f"Error: Could not write to {output_path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
