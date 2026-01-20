#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search Index Generator for Quarto Projects

Generates JSON search indexes with rich metadata for each Quarto configuration.
Extracts frontmatter, excerpts, section headings, and builds comprehensive search data.
"""

import sys
import yaml
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class SearchIndexEntry:
    """Represents a single entry in the search index."""

    def __init__(
        self,
        path: str,
        url: str,
        title: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        image: Optional[str] = None,
        excerpt: Optional[str] = None,
        sections: Optional[List[str]] = None,
        published: bool = True,
        lastmod: Optional[str] = None
    ):
        self.path = path
        self.url = url
        self.title = title
        self.description = description
        self.tags = tags or []
        self.image = image
        self.excerpt = excerpt
        self.sections = sections or []
        self.published = published
        self.lastmod = lastmod

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": self.path,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "image": self.image,
            "excerpt": self.excerpt,
            "sections": self.sections,
            "published": self.published,
            "lastmod": self.lastmod
        }


class QMDParser:
    """Parser for extracting metadata from QMD files."""

    @staticmethod
    def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
        """Extract YAML frontmatter from QMD content."""
        # Match YAML frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?\n)---\s*\n', content, re.DOTALL)
        if not match:
            return None

        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None

    @staticmethod
    def extract_excerpt(content: str, max_length: int = 200) -> Optional[str]:
        """Extract first non-heading paragraph as excerpt."""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Remove comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        # Find first paragraph (non-heading, non-empty line)
        lines = content.split('\n')
        paragraph_lines = []

        for line in lines:
            line = line.strip()
            # Skip headings, empty lines, code blocks, Quarto directives
            if (not line or
                line.startswith('#') or
                line.startswith('```') or
                line.startswith('{{<') or  # Quarto shortcodes
                line.startswith('::')):    # Quarto divs
                if paragraph_lines:  # Found end of first paragraph
                    break
                continue
            paragraph_lines.append(line)

        if not paragraph_lines:
            return None

        excerpt = ' '.join(paragraph_lines)
        # Remove markdown formatting
        excerpt = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', excerpt)  # Links
        excerpt = re.sub(r'[*_`]', '', excerpt)  # Bold, italic, code
        excerpt = re.sub(r'\{\{<.*?>\}\}', '', excerpt)  # Remaining shortcodes

        # Truncate to max_length
        if len(excerpt) > max_length:
            excerpt = excerpt[:max_length].rsplit(' ', 1)[0] + '...'

        return excerpt

    @staticmethod
    def extract_sections(content: str) -> List[str]:
        """Extract section headings (h2, h3)."""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        sections = []
        for line in content.split('\n'):
            # Match h2 (##) and h3 (###) headings
            match = re.match(r'^#{2,3}\s+(.+)', line)
            if match:
                heading = match.group(1).strip()
                # Remove markdown formatting and anchors
                heading = re.sub(r'\{#[^}]+\}', '', heading)  # {#anchor}
                heading = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', heading)  # Links
                heading = re.sub(r'[*_`]', '', heading)  # Bold, italic, code
                sections.append(heading.strip())

        return sections


class SearchIndexGenerator:
    """Generates search indexes for Quarto projects."""

    # Configs to skip (test configs, base config that gets overwritten)
    SKIP_CONFIGS = {'_quarto.yml', '_quarto-test.yml'}

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.parser = QMDParser()
        self.quarto_configs = self._discover_quarto_configs()

    def _discover_quarto_configs(self) -> Dict[str, Dict[str, Any]]:
        """Dynamically discover and load all Quarto config files.

        Handles both project types:
        - 'book' type: uses book.site-url and book.chapters
        - 'website' type: uses website.site-url and project.render
        """
        configs = {}

        # Find all _quarto*.yml files in project root
        for config_path in self.project_root.glob('_quarto*.yml'):
            if config_path.name in self.SKIP_CONFIGS:
                continue

            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    quarto_yaml = yaml.safe_load(f)

                if not quarto_yaml:
                    continue

                # Extract config name from filename
                # _quarto-manual.yml -> book
                # _quarto-1-pct-treaty-impact.yml -> 1-pct-treaty-impact
                config_name = config_path.stem.replace('_quarto-', '').replace('_quarto', 'default')

                # Extract required fields from YAML
                project = quarto_yaml.get('project', {})
                book = quarto_yaml.get('book', {})
                website = quarto_yaml.get('website', {})
                project_type = project.get('type', 'book')

                # Get output directory (always in project section)
                output_dir = project.get('output-dir')

                # Determine project type and get files/base_url accordingly
                # Priority: book.chapters > project.render
                has_book_chapters = bool(book.get('chapters'))
                has_render_list = bool(project.get('render'))

                if has_book_chapters:
                    # Book type: uses book.site-url (or website.site-url) and book.chapters
                    base_url = book.get('site-url') or website.get('site-url')
                    files = book.get('chapters', [])
                    project_type = 'book'
                elif has_render_list:
                    # Website type: uses website.site-url and project.render
                    base_url = website.get('site-url') or book.get('site-url')
                    files = project.get('render', [])
                    project_type = 'website'
                else:
                    # No files defined
                    files = []
                    base_url = book.get('site-url') or website.get('site-url')

                # Skip configs without required fields
                if not output_dir:
                    print(f"[WARN] Skipping {config_path.name}: missing output-dir")
                    continue

                if not base_url:
                    print(f"[WARN] Skipping {config_path.name}: missing site-url")
                    continue

                if not files:
                    print(f"[WARN] Skipping {config_path.name}: no files/chapters defined")
                    continue

                configs[config_name] = {
                    'config_file': config_path.name,
                    'output_dir': output_dir,
                    'base_url': base_url,
                    'chapters': files,  # Store files list (works for both types)
                    'project_type': project_type,
                }

                print(f"[OK] Loaded config: {config_name} ({config_path.name}) [{project_type}]")

            except yaml.YAMLError as e:
                print(f"[WARN] Failed to parse {config_path.name}: {e}")
            except Exception as e:
                print(f"[WARN] Error loading {config_path.name}: {e}")

        return configs

    def get_qmd_files_for_config(self, config_name: str) -> List[Path]:
        """Get list of QMD files to index for a specific config."""
        config = self.quarto_configs.get(config_name)
        if not config:
            return []

        chapters = config.get('chapters', [])
        qmd_files = []

        def extract_files(chapter_list: List) -> None:
            """Recursively extract QMD files from chapter list."""
            for chapter in chapter_list:
                if isinstance(chapter, str):
                    qmd_path = self.project_root / chapter
                    if qmd_path.exists() and qmd_path.suffix == '.qmd':
                        qmd_files.append(qmd_path)
                elif isinstance(chapter, dict):
                    # Handle various nested structures:
                    # - part: "Title" with chapters: [...]
                    # - href: "file.qmd"
                    if 'href' in chapter:
                        href = chapter['href']
                        if href.endswith('.qmd'):
                            qmd_path = self.project_root / href
                            if qmd_path.exists():
                                qmd_files.append(qmd_path)
                    if 'chapters' in chapter:
                        extract_files(chapter['chapters'])
                    if 'contents' in chapter:
                        extract_files(chapter['contents'])

        extract_files(chapters)
        return qmd_files

    def qmd_to_url(self, qmd_path: Path, config_name: str) -> str:
        """Convert QMD file path to URL based on config."""
        config = self.quarto_configs[config_name]

        # Convert path to relative from project root
        try:
            rel_path = qmd_path.relative_to(self.project_root)
        except ValueError:
            rel_path = qmd_path

        # Convert .qmd to .html
        url_path = str(rel_path).replace('\\', '/').replace('.qmd', '.html')

        # Handle index.qmd -> / mapping
        if url_path == 'index.html':
            return '/'

        # Remove knowledge/ prefix for cleaner URLs
        url_path = url_path.replace('knowledge/', '')

        return f"/{url_path}"

    def parse_qmd_file(self, qmd_path: Path, config_name: str) -> Optional[SearchIndexEntry]:
        """Parse a single QMD file and create search index entry."""
        try:
            with open(qmd_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            frontmatter = self.parser.extract_frontmatter(content)
            if not frontmatter:
                frontmatter = {}

            # Get title (required)
            title = frontmatter.get('title', qmd_path.stem.replace('-', ' ').title())

            # Get description
            description = frontmatter.get('description') or frontmatter.get('abstract')

            # Get tags
            tags = frontmatter.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]

            # Get image
            image = frontmatter.get('image')

            # Extract excerpt
            excerpt = self.parser.extract_excerpt(content)

            # Extract sections
            sections = self.parser.extract_sections(content)

            # Get published status
            published = frontmatter.get('published', True)

            # Get last modified date
            lastmod = None
            if qmd_path.exists():
                mtime = qmd_path.stat().st_mtime
                lastmod = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

            # Generate URL
            url = self.qmd_to_url(qmd_path, config_name)

            # Generate relative path
            try:
                rel_path = str(qmd_path.relative_to(self.project_root))
            except ValueError:
                rel_path = str(qmd_path)

            return SearchIndexEntry(
                path=rel_path.replace('\\', '/'),
                url=url,
                title=title,
                description=description,
                tags=tags,
                image=image,
                excerpt=excerpt,
                sections=sections,
                published=published,
                lastmod=lastmod
            )

        except Exception as e:
            print(f"[WARN] Failed to parse {qmd_path}: {e}")
            return None

    def generate_index_for_config(self, config_name: str) -> List[SearchIndexEntry]:
        """Generate search index for a specific Quarto config."""
        print(f"[*] Generating search index for {config_name}...")

        qmd_files = self.get_qmd_files_for_config(config_name)
        if not qmd_files:
            print(f"[WARN] No QMD files found for {config_name}")
            return []

        entries = []
        for qmd_path in qmd_files:
            entry = self.parse_qmd_file(qmd_path, config_name)
            if entry:
                entries.append(entry)

        print(f"[OK] Generated {len(entries)} search index entries for {config_name}")
        return entries

    def write_index_json(self, config_name: str, entries: List[SearchIndexEntry]) -> Path:
        """Write search index to JSON file."""
        config = self.quarto_configs[config_name]
        output_dir = self.project_root / config['output_dir']
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / 'search-index.json'

        # Convert entries to dictionaries
        data = [entry.to_dict() for entry in entries]

        # Write JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Wrote search index to {output_file.relative_to(self.project_root)}")
        return output_file

    def generate_all_indexes(self) -> Dict[str, Path]:
        """Generate search indexes for all Quarto configs."""
        print("\n" + "="*60)
        print("GENERATING SEARCH INDEXES")
        print("="*60 + "\n")

        output_files = {}

        for config_name in self.quarto_configs.keys():
            entries = self.generate_index_for_config(config_name)
            if entries:
                output_file = self.write_index_json(config_name, entries)
                output_files[config_name] = output_file
            print()

        print("="*60)
        print(f"[OK] Generated {len(output_files)} search indexes")
        print("="*60 + "\n")

        return output_files


def generate_search_indexes(project_root: Path) -> Dict[str, Path]:
    """
    Main entry point for search index generation.

    Args:
        project_root: Path to project root directory

    Returns:
        Dict mapping config names to output file paths
    """
    generator = SearchIndexGenerator(project_root)
    return generator.generate_all_indexes()


if __name__ == "__main__":
    # For testing standalone
    project_root = Path(__file__).parent.parent
    generate_search_indexes(project_root)
