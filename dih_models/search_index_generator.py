#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search Index Generator for Quarto Projects

Generates JSON search indexes with rich metadata for each Quarto configuration.
Extracts frontmatter, section headings, and builds comprehensive search data.
"""

import sys
import yaml
import json

from dih_models.yaml_utils import yaml_safe_load, load_quarto_config
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from dih_models.variable_replacement import load_variables

# Set UTF-8 encoding for stdout on Windows (reconfigure exists on TextIOWrapper at runtime)
if sys.platform == 'win32':
    getattr(sys.stdout, 'reconfigure', lambda **kwargs: None)(encoding='utf-8')

# Pre-compiled regex patterns (avoid recompiling per-file or per-line)
_FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?\n)---\s*\n', re.DOTALL)
_HEADING_PATTERN = re.compile(r'^#{2,3}\s+(.+)')
_QUARTO_ATTR_PATTERN = re.compile(r'\{(?![{<])[^}]+\}')
_MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\([^\)]+\)')
_MARKDOWN_FORMAT_PATTERN = re.compile(r'[*_`]')
_QUARTO_VAR_PATTERN = re.compile(r'\{\{<\s*var\s+([a-zA-Z0-9_]+)\s*>\}\}')


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
            "sections": self.sections,
            "published": self.published,
            "lastmod": self.lastmod
        }


class QMDParser:
    """Parser for extracting metadata from QMD files."""

    @staticmethod
    def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
        """Extract YAML frontmatter from QMD content."""
        match = _FRONTMATTER_PATTERN.match(content)
        if not match:
            return None

        try:
            return yaml_safe_load(match.group(1))
        except yaml.YAMLError:
            return None

    @staticmethod
    def extract_sections(content: str) -> List[str]:
        """Extract section headings (h2, h3)."""
        # Remove frontmatter
        content = _FRONTMATTER_PATTERN.sub('', content, count=1)

        sections = []
        for line in content.split('\n'):
            match = _HEADING_PATTERN.match(line)
            if match:
                heading = match.group(1).strip()
                # Remove markdown formatting and anchors/attributes
                # BUT preserve Quarto variables {{< var ... >}} for later replacement
                heading = _QUARTO_ATTR_PATTERN.sub('', heading)
                heading = _MARKDOWN_LINK_PATTERN.sub(r'\1', heading)
                heading = _MARKDOWN_FORMAT_PATTERN.sub('', heading)
                heading = heading.strip()
                if heading:
                    sections.append(heading)

        return sections


class SearchIndexGenerator:
    """Generates search indexes for Quarto projects."""

    # Configs to skip (test configs, base config that gets overwritten)
    SKIP_CONFIGS = {'_quarto.yml', '_quarto-test.yml'}

    def __init__(self, project_root: Path, variables: Optional[Dict[str, str]] = None):
        self.project_root = project_root
        self.parser = QMDParser()
        # Load variables from _variables.yml if not provided
        if variables is None:
            variables_path = project_root / '_variables.yml'
            self.variables = load_variables(variables_path) if variables_path.exists() else {}
        else:
            self.variables = variables
        self.quarto_configs = self._discover_quarto_configs()
        # Cache for generated index entries (avoids re-parsing QMD files)
        self._index_cache: Dict[str, List[SearchIndexEntry]] = {}
        # Cache git-derived lastmod values (same files can appear in multiple configs)
        self._git_lastmod_cache: Dict[str, Optional[str]] = {}
        self._git_available: Optional[bool] = None

    def _ensure_git_available(self) -> bool:
        """Check whether git metadata can be queried for this project."""
        if self._git_available is not None:
            return self._git_available

        try:
            result = subprocess.run(
                ["git", "-C", str(self.project_root), "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                check=False,
            )
            self._git_available = result.returncode == 0
        except Exception:
            self._git_available = False

        return self._git_available

    def _get_git_lastmod(self, source_path: Path) -> Optional[str]:
        """Return YYYY-MM-DD from last git commit touching the file."""
        if not self._ensure_git_available():
            return None

        try:
            rel_path = source_path.relative_to(self.project_root)
        except ValueError:
            rel_path = source_path

        rel_key = str(rel_path).replace('\\', '/')
        if rel_key in self._git_lastmod_cache:
            return self._git_lastmod_cache[rel_key]

        try:
            result = subprocess.run(
                ["git", "-C", str(self.project_root), "log", "-1", "--format=%ct", "--", rel_key],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                ts_text = result.stdout.strip()
                if ts_text:
                    ts = int(ts_text)
                    git_lastmod = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')
                    self._git_lastmod_cache[rel_key] = git_lastmod
                    return git_lastmod
        except Exception:
            pass

        self._git_lastmod_cache[rel_key] = None
        return None

    def _get_lastmod_date(self, source_path: Path) -> Optional[str]:
        """Prefer git commit date; fall back to filesystem modified date."""
        git_lastmod = self._get_git_lastmod(source_path)
        if git_lastmod:
            return git_lastmod

        if source_path.exists():
            mtime = source_path.stat().st_mtime
            return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

        return None

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
                quarto_yaml = load_quarto_config(config_path)

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

                # Get index-source from dih-render section (used to copy actual content to index.qmd)
                dih_render = quarto_yaml.get('dih-render', {})
                index_source = dih_render.get('index-source')

                configs[config_name] = {
                    'config_file': config_path.name,
                    'output_dir': output_dir,
                    'base_url': base_url,
                    'chapters': files,  # Store files list (works for both types)
                    'project_type': project_type,
                    'index_source': index_source,  # Path to actual source file for index.qmd
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

    def _replace_variables_strict(self, text: str, source_path: Path) -> str:
        """Replace Quarto variables, raising error if any are missing.

        Args:
            text: Text containing {{< var name >}} patterns
            source_path: Path to source file (for error messages)

        Returns:
            Text with variables replaced

        Raises:
            ValueError: If a variable is referenced but not defined
        """
        def replacer(match):
            var_name = match.group(1)
            if var_name not in self.variables:
                raise ValueError(
                    f"Missing variable '{var_name}' in {source_path.relative_to(self.project_root)}"
                )
            return self.variables[var_name]

        return _QUARTO_VAR_PATTERN.sub(replacer, text)

    def _replace_variables_in_headings(self, content: str, source_path: Path) -> str:
        """Replace Quarto variables only in heading lines.

        This preserves variables in code blocks, LaTeX, etc. while ensuring
        heading variables are replaced before markdown stripping mangles them.

        Args:
            content: Full file content
            source_path: Path to source file (for error messages)

        Returns:
            Content with variables replaced in headings only
        """
        lines = content.split('\n')
        result = []

        for line in lines:
            # Only process heading lines (h2, h3)
            if _HEADING_PATTERN.match(line):
                line = self._replace_variables_strict(line, source_path)
            result.append(line)

        return '\n'.join(result)

    def parse_qmd_file(self, qmd_path: Path, config_name: str) -> Optional[SearchIndexEntry]:
        """Parse a single QMD file and create search index entry."""
        try:
            # For index.qmd, use index-source if defined in config
            # This is because index.qmd gets overwritten by the render script with content
            # from the actual source file specified in dih-render.index-source
            config = self.quarto_configs.get(config_name)
            actual_source_path = qmd_path

            if qmd_path.name == 'index.qmd' and config and config.get('index_source'):
                source_path = self.project_root / config['index_source']
                if source_path.exists():
                    actual_source_path = source_path
                    print(f"  [*] Using index-source: {config['index_source']}")

            with open(actual_source_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            frontmatter = self.parser.extract_frontmatter(content)
            if not frontmatter:
                frontmatter = {}

            # Get title and apply variable replacement (strict mode - crash on missing)
            title = frontmatter.get('title', qmd_path.stem.replace('-', ' ').title())
            title = self._replace_variables_strict(title, qmd_path)

            # Get description and apply variable replacement
            description = frontmatter.get('description') or frontmatter.get('abstract')
            if description:
                description = self._replace_variables_strict(description, qmd_path)

            # Get tags
            tags = frontmatter.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]

            # Get image
            image = frontmatter.get('image')

            # Apply variable replacement to content BEFORE extracting sections
            # This ensures variable names with underscores aren't mangled by markdown stripping
            content_for_sections = self._replace_variables_in_headings(content, qmd_path)
            sections = self.parser.extract_sections(content_for_sections)

            # Get published status
            published = frontmatter.get('published', True)

            # Get last modified date from the actual content source file.
            # Prefer git commit date for stable lastmod values across rebuilds/checkouts.
            lastmod = self._get_lastmod_date(actual_source_path)

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
                sections=sections,
                published=published,
                lastmod=lastmod
            )

        except Exception as e:
            print(f"[WARN] Failed to parse {qmd_path}: {e}")
            return None

    def generate_index_for_config(self, config_name: str) -> List[SearchIndexEntry]:
        """Generate search index for a specific Quarto config.

        Results are cached so repeated calls (e.g., from generate_sites_metadata
        after generate_search_indexes) don't re-parse QMD files.
        """
        # Return cached result if available
        if config_name in self._index_cache:
            return self._index_cache[config_name]

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
        self._index_cache[config_name] = entries
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


def generate_search_indexes(project_root: Path, variables: Optional[Dict[str, str]] = None) -> Dict[str, Path]:
    """
    Main entry point for search index generation.

    Args:
        project_root: Path to project root directory
        variables: Optional dict of variable names to values. If not provided,
                   loads from _variables.yml in project_root.

    Returns:
        Dict mapping config names to output file paths
    """
    generator = SearchIndexGenerator(project_root, variables)
    return generator.generate_all_indexes()


if __name__ == "__main__":
    # For testing standalone
    project_root = Path(__file__).parent.parent
    generate_search_indexes(project_root)
