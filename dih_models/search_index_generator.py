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
import logging

from dih_models.yaml_utils import yaml_safe_load, load_quarto_config
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Iterable
from datetime import datetime, timezone

from dih_models.variable_replacement import load_variables

logger = logging.getLogger("dih.search_index")

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


_QUARTO_SHORTCODE_PATTERN = re.compile(r'\{\{<[^>]*>\}\}')
_QUARTO_CALLOUT_PATTERN = re.compile(r'^:::\s*\{[^}]*\}\s*$|^:::\s*$', re.MULTILINE)
_QUARTO_INCLUDE_PATTERN = re.compile(r'^\{\{<\s*include\s+.*>\}\}\s*$', re.MULTILINE)
_HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
_MULTIPLE_SPACES_PATTERN = re.compile(r'[ \t]+')
_MULTIPLE_NEWLINES_PATTERN = re.compile(r'\n{3,}')

# Frontmatter fields excluded from the full metadata dump on each entry.
# These are Quarto rendering-config fields that have no value to external API
# consumers of search-index.json. Everything else in the qmd frontmatter passes
# through untouched via entry["metadata"].
_EXCLUDED_METADATA_FIELDS = frozenset({
    'fig-cap-location',
    'format',
    'jupyter',
    'number-sections',
    'page-layout',
    'search',
    'tbl-cap-location',
    'toc',
    'toc-depth',
    'feed-date',
})


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
        lastmod: Optional[str] = None,
        text: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        figures: Optional[List[Dict[str, str]]] = None,
        syndicate: bool = True,
        scores: Optional[Dict[str, int]] = None,
        metadata: Optional[Dict[str, Any]] = None,
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
        self.text = text
        self.parameters = parameters or {}
        self.figures = figures or []
        self.syndicate = syndicate
        self.scores = scores
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "path": self.path,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "image": self.image,
            "sections": self.sections,
            "published": self.published,
            "lastmod": self.lastmod,
            "syndicate": self.syndicate,
        }
        if self.scores:
            result["scores"] = self.scores
        if self.metadata:
            result["metadata"] = self.metadata
        if self.text:
            result["text"] = self.text
        if self.parameters:
            result["parameters"] = self.parameters
        if self.figures:
            result["figures"] = self.figures
        return result


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

    @staticmethod
    def extract_figures(content: str) -> List[Dict[str, str]]:
        """Extract image references ![caption](path) before they get stripped."""
        figures = []
        for m in re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)', content):
            caption, path = m.group(1), m.group(2)
            # Skip tiny icons, og images
            if any(skip in path.lower() for skip in ('icon', '-og-', 'og-image', 'favicon')):
                continue
            figures.append({'path': path.lstrip('/'), 'caption': caption})
        return figures

    @staticmethod
    def extract_body_text(content: str) -> str:
        """Extract plain body text from QMD content for search indexing.

        Strips frontmatter, Quarto shortcodes, callouts, includes, HTML tags,
        markdown formatting, and normalizes whitespace. No truncation — the
        chat RAG needs full chapter text for accurate retrieval.
        """
        # Remove frontmatter
        text = _FRONTMATTER_PATTERN.sub('', content, count=1)
        # Remove include directives
        text = _QUARTO_INCLUDE_PATTERN.sub('', text)
        # Remove callout fences
        text = _QUARTO_CALLOUT_PATTERN.sub('', text)
        # Remove Quarto shortcodes (variables replaced separately upstream)
        text = _QUARTO_SHORTCODE_PATTERN.sub('', text)
        # Remove HTML tags
        text = _HTML_TAG_PATTERN.sub('', text)
        # Remove heading markers
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # Remove markdown links but keep text
        text = _MARKDOWN_LINK_PATTERN.sub(r'\1', text)
        # Remove markdown formatting chars
        text = _MARKDOWN_FORMAT_PATTERN.sub('', text)
        # Remove image references ![alt](url)
        text = re.sub(r'!\[[^\]]*\]\([^\)]*\)', '', text)
        # Remove citation references [@key]
        text = re.sub(r'\[@[^\]]+\]', '', text)
        # Remove $$ display math blocks
        text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
        # Remove inline $..$ math but NOT dollar amounts like $27.2B
        # LaTeX inline math: $x + y$ (letters/operators inside)
        # Dollar amounts: $27.2B, $500, $2.72T (digit after $)
        text = re.sub(r'\$(?!\d)[^$]+\$', '', text)
        # Remove {.class} annotations
        text = re.sub(r'\{[.#][^}]+\}', '', text)
        # Normalize whitespace
        text = _MULTIPLE_SPACES_PATTERN.sub(' ', text)
        text = _MULTIPLE_NEWLINES_PATTERN.sub('\n\n', text)
        text = text.strip()
        return text


class SearchIndexGenerator:
    """Generates search indexes for Quarto projects."""

    # Configs to skip (test configs, base config that gets overwritten)
    SKIP_CONFIGS = {'_quarto.yml', '_quarto-test.yml'}
    GIT_LOG_ARG_CHARS_LIMIT = 24000

    def __init__(self, project_root: Path, variables: Optional[Dict[str, str]] = None):
        self.project_root = project_root
        self.parser = QMDParser()
        # Load variables from _variables.yml if not provided
        if variables is None:
            variables_path = project_root / '_variables.yml'
            self.variables = load_variables(variables_path) if variables_path.exists() else {}
        else:
            self.variables = variables
        # Also load raw YAML values (with HTML) for parameter metadata extraction
        variables_path = project_root / '_variables.yml'
        if variables_path.exists():
            self._raw_variables = yaml.safe_load(variables_path.read_text(encoding='utf-8')) or {}
        else:
            self._raw_variables = {}
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

    def _normalize_rel_key(self, source_path: Path) -> str:
        """Normalize a path to the relative key format used by git cache lookups."""
        try:
            rel_path = source_path.relative_to(self.project_root)
        except ValueError:
            rel_path = source_path
        return str(rel_path).replace('\\', '/')

    def _resolve_actual_source_path(self, qmd_path: Path, config_name: str) -> Path:
        """Resolve the real source path used for indexing and lastmod lookup."""
        config = self.quarto_configs.get(config_name)
        if qmd_path.name == 'index.qmd' and config and config.get('index_source'):
            source_path = self.project_root / config['index_source']
            if source_path.exists():
                return source_path
        return qmd_path

    def _iter_git_log_batches(self, rel_keys: Iterable[str]) -> Iterable[List[str]]:
        """Yield path batches small enough for Windows command-line limits."""
        batch: List[str] = []
        batch_chars = 0

        for rel_key in rel_keys:
            rel_key_chars = len(rel_key) + 1
            if batch and batch_chars + rel_key_chars > self.GIT_LOG_ARG_CHARS_LIMIT:
                yield batch
                batch = []
                batch_chars = 0

            batch.append(rel_key)
            batch_chars += rel_key_chars

        if batch:
            yield batch

    def _prefetch_git_lastmods(self, source_paths: Iterable[Path]) -> None:
        """Batch-populate git lastmod dates for a set of files."""
        if not self._ensure_git_available():
            return

        rel_keys = []
        for source_path in source_paths:
            rel_key = self._normalize_rel_key(source_path)
            if rel_key not in self._git_lastmod_cache:
                rel_keys.append(rel_key)

        if not rel_keys:
            return

        unique_rel_keys = list(dict.fromkeys(rel_keys))
        for batch in self._iter_git_log_batches(unique_rel_keys):
            batch_set = set(batch)
            try:
                result = subprocess.run(
                    ["git", "-C", str(self.project_root), "log", "--format=%ct", "--name-only", "--", *batch],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except Exception:
                result = None

            if result and result.returncode == 0:
                current_lastmod: Optional[str] = None
                resolved_count = 0

                for raw_line in result.stdout.splitlines():
                    line = raw_line.strip()
                    if not line:
                        continue
                    if line.isdigit():
                        current_lastmod = datetime.fromtimestamp(int(line), tz=timezone.utc).strftime('%Y-%m-%d')
                        continue

                    rel_key = line.replace('\\', '/')
                    if current_lastmod and rel_key in batch_set and rel_key not in self._git_lastmod_cache:
                        self._git_lastmod_cache[rel_key] = current_lastmod
                        resolved_count += 1
                        if resolved_count == len(batch_set):
                            break

            for rel_key in batch:
                self._git_lastmod_cache.setdefault(rel_key, None)

    def _get_git_lastmod(self, source_path: Path) -> Optional[str]:
        """Return YYYY-MM-DD from last git commit touching the file."""
        if not self._ensure_git_available():
            return None

        rel_key = self._normalize_rel_key(source_path)
        if rel_key not in self._git_lastmod_cache:
            self._prefetch_git_lastmods([source_path])
        return self._git_lastmod_cache.get(rel_key)

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
                    logger.warning("Skipping %s: missing output-dir", config_path.name)
                    continue

                if not base_url:
                    logger.warning("Skipping %s: missing site-url", config_path.name)
                    continue

                if not files:
                    logger.warning("Skipping %s: no files/chapters defined", config_path.name)
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

                logger.debug("Loaded config: %s (%s) [%s]", config_name, config_path.name, project_type)

            except yaml.YAMLError as e:
                logger.warning("Failed to parse %s: %s", config_path.name, e)
            except Exception as e:
                logger.warning("Error loading %s: %s", config_path.name, e)

        return configs

    def get_qmd_files_for_config(self, config_name: str) -> List[Path]:
        """Get list of QMD files to index for a specific config."""
        config = self.quarto_configs.get(config_name)
        if not config:
            return []

        chapters = config.get('chapters', [])
        qmd_files = []

        # Get index-source fallback (used when index.qmd doesn't exist yet)
        index_source = config.get('index_source')

        def extract_files(chapter_list: List) -> None:
            """Recursively extract QMD files from chapter list."""
            for chapter in chapter_list:
                if isinstance(chapter, str):
                    qmd_path = self.project_root / chapter
                    if qmd_path.exists() and qmd_path.suffix == '.qmd':
                        qmd_files.append(qmd_path)
                    elif chapter == 'index.qmd' and index_source:
                        # Fall back to index-source when index.qmd doesn't exist yet
                        source_path = self.project_root / index_source
                        if source_path.exists() and source_path.suffix == '.qmd':
                            qmd_files.append(source_path)
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

    def _extract_parameter_metadata(self, content: str) -> Dict[str, Dict[str, Any]]:
        """Extract structured metadata from parameter HTML for all {{< var >}} refs in content.

        Parses the <a> or <span> HTML in variable values to extract:
        - display: rendered display text (e.g. "$27.2B")
        - href: link to parameters page with calculation details
        - formula: calculation formula if present
        - source_ref: BibTeX citation key
        - source_type: "external", "calculated", or "definition"
        - confidence: "high", "medium", "low"
        - unit: parameter unit
        - latex: full LaTeX equation from _latex variant if available
        """
        params: Dict[str, Dict[str, Any]] = {}

        for match in _QUARTO_VAR_PATTERN.finditer(content):
            var_name = match.group(1)
            if var_name in params:
                continue
            # Skip _latex, _nounit, _cite variants
            if var_name.endswith(('_latex', '_nounit', '_cite')):
                continue

            html_val = self._raw_variables.get(var_name)
            if not html_val:
                continue

            meta: Dict[str, Any] = {}

            # Extract display text from <a ...>text</a> or <span ...>text</span>
            display_match = re.search(r'>([^<]+)</(?:a|span)>', html_val)
            if display_match:
                display = display_match.group(1).strip()
                # Strip CI from display: "$500 (95% CI: $400-$2.5K)" -> "$500"
                display = re.sub(r'\s*\(95% CI:[^)]+\)', '', display)
                meta['display'] = display
            else:
                meta['display'] = re.sub(r'<[^>]+>', '', html_val).strip()

            # Extract href
            href_match = re.search(r'href="([^"]+)"', html_val)
            if href_match:
                meta['href'] = href_match.group(1)

            # Extract data attributes
            for attr in ('source-ref', 'source-type', 'confidence'):
                attr_match = re.search(rf'data-{attr}="([^"]*)"', html_val)
                if attr_match and attr_match.group(1):
                    meta[attr.replace('-', '_')] = attr_match.group(1)

            # Extract formula and unit from title attribute
            title_match = re.search(r'title="([^"]*)"', html_val)
            if title_match:
                title_text = title_match.group(1)
                formula_match = re.search(r'Formula:\s*([^|]+)', title_text)
                if formula_match:
                    meta['formula'] = formula_match.group(1).strip()
                unit_match = re.search(r'Unit:\s*([^|]+)', title_text)
                if unit_match:
                    meta['unit'] = unit_match.group(1).strip()

            # Include _latex equation if available
            latex_key = var_name + '_latex'
            if latex_key in self._raw_variables:
                latex_val = self._raw_variables[latex_key]
                # Strip HTML wrapping if any
                latex_clean = re.sub(r'<[^>]+>', '', latex_val).strip()
                if latex_clean:
                    meta['latex'] = latex_clean

            if meta.get('display'):
                params[var_name] = meta

        return params

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
            actual_source_path = self._resolve_actual_source_path(qmd_path, config_name)
            if actual_source_path != qmd_path:
                config = self.quarto_configs.get(config_name)
                if config and config.get('index_source'):
                    logger.debug("Using index-source: %s", config['index_source'])

            with open(actual_source_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            frontmatter = self.parser.extract_frontmatter(content)
            if not frontmatter:
                frontmatter = {}

            # Skip pages that opt out of search indexing
            if frontmatter.get('search') is False:
                logger.debug("Skipping %s: search: false in frontmatter", qmd_path.name)
                return None

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

            # Get syndication flag (exclude utility pages from external feeds)
            syndicate = frontmatter.get('syndicate', True)

            # Get content scores (quality, value, timeliness — each 1-10)
            scores = frontmatter.get('scores')
            if isinstance(scores, dict):
                scores = {k: int(v) for k, v in scores.items() if v is not None}
            else:
                scores = None

            # Build full metadata dump from frontmatter for API consumers who
            # need fields beyond the curated top-level set. Quarto rendering
            # config is filtered out via _EXCLUDED_METADATA_FIELDS.
            metadata = {
                k: v for k, v in frontmatter.items()
                if k not in _EXCLUDED_METADATA_FIELDS and v is not None
            }

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

            # Extract parameter metadata BEFORE variable replacement strips the HTML
            parameters = self._extract_parameter_metadata(content)

            # Extract figures BEFORE image markdown gets stripped
            figures = self.parser.extract_figures(content)

            # Extract body text for full-text search / RAG
            # Replace variables first (before stripping markdown), then extract plain text
            # For variable replacement, strip parameter HTML to plain display text
            def _var_to_display(m):
                var_name = m.group(1)
                html_val = self.variables.get(var_name) if self.variables else None
                if html_val is None:
                    html_val = m.group(0)
                # Extract display text from <a>text</a> or <span>text</span>
                display_match = re.search(r'>([^<]+)</(?:a|span)>', html_val)
                if display_match:
                    display = display_match.group(1).strip()
                    return re.sub(r'\s*\(95% CI:[^)]+\)', '', display)
                return re.sub(r'<[^>]+>', '', html_val).strip()

            content_with_vars = _QUARTO_VAR_PATTERN.sub(_var_to_display, content)
            body_text = self.parser.extract_body_text(content_with_vars)

            return SearchIndexEntry(
                path=rel_path.replace('\\', '/'),
                url=url,
                title=title,
                description=description,
                tags=tags,
                image=image,
                sections=sections,
                published=published,
                lastmod=lastmod,
                text=body_text,
                parameters=parameters,
                figures=figures,
                syndicate=syndicate,
                scores=scores,
                metadata=metadata,
            )

        except Exception as e:
            logger.warning("Failed to parse %s: %s", qmd_path, e)
            return None

    def generate_index_for_config(self, config_name: str) -> List[SearchIndexEntry]:
        """Generate search index for a specific Quarto config.

        Results are cached so repeated calls (e.g., from generate_sites_metadata
        after generate_search_indexes) don't re-parse QMD files.
        """
        # Return cached result if available
        if config_name in self._index_cache:
            return self._index_cache[config_name]

        logger.debug("Generating search index for %s...", config_name)

        qmd_files = self.get_qmd_files_for_config(config_name)
        if not qmd_files:
            logger.warning("No QMD files found for %s", config_name)
            self._index_cache[config_name] = []
            return []

        self._prefetch_git_lastmods(
            self._resolve_actual_source_path(qmd_path, config_name) for qmd_path in qmd_files
        )

        entries = []
        for qmd_path in qmd_files:
            entry = self.parse_qmd_file(qmd_path, config_name)
            if entry:
                entries.append(entry)

        logger.debug("Generated %d search index entries for %s", len(entries), config_name)
        self._index_cache[config_name] = entries
        return entries

    # Canonical search index path for the chat widget RAG system.
    # Generated from _quarto-manual.yml (the comprehensive config with all chapters).
    CANONICAL_INDEX_PATH = "assets/json/search-index.json"

    def generate_chat_index(self) -> Path:
        """Generate the canonical search index for the chat widget RAG system.

        Builds from the 'manual' config (_quarto-manual.yml) which contains all
        chapters. Writes to assets/json/search-index.json. Quarto generates its
        own search.json during render; this index is specifically for the chat RAG.

        Returns:
            Path to the generated search-index.json
        """
        config_name = 'manual'
        if config_name not in self.quarto_configs:
            raise ValueError(f"Config '{config_name}' not found. Available: {list(self.quarto_configs.keys())}")

        # Prefetch git dates for all manual files
        qmd_files = self.get_qmd_files_for_config(config_name)
        self._prefetch_git_lastmods(
            self._resolve_actual_source_path(qmd_path, config_name) for qmd_path in qmd_files
        )

        entries = self.generate_index_for_config(config_name)

        output_path = self.project_root / self.CANONICAL_INDEX_PATH
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = [entry.to_dict() for entry in entries]
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.debug("Wrote chat search index: %s (%d entries)", self.CANONICAL_INDEX_PATH, len(data))
        return output_path


def generate_search_indexes(project_root: Path, variables: Optional[Dict[str, str]] = None) -> Path:
    """
    Generate the chat search index from _quarto-manual.yml.

    Args:
        project_root: Path to project root directory
        variables: Optional dict of variable names to values. If not provided,
                   loads from _variables.yml in project_root.

    Returns:
        Path to the generated assets/json/search-index.json
    """
    generator = SearchIndexGenerator(project_root, variables)
    return generator.generate_chat_index()


if __name__ == "__main__":
    # For testing standalone
    project_root = Path(__file__).parent.parent
    generate_search_indexes(project_root)
