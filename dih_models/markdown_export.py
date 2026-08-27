#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for exporting QMD content to portable Markdown."""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

from dih_models.variable_replacement import (
    clean_for_readme,
    load_variables,
    parameter_anchor_name,
    replace_variables,
)
from dih_models.yaml_utils import yaml_safe_load

MANUAL_BASE_URL = "https://manual.warondisease.org"


def strip_confidence_intervals(text: str) -> str:
    """Strip '(95% CI: ...)' or '(90% CI: ...)' from resolved variable text."""
    return re.sub(r'\s*\(9[05]% CI:\s*[^)]+\)', '', text)


def normalize_parameter_link_key(name: str) -> str:
    """Normalize parameter and display-variant names for link overrides."""
    return parameter_anchor_name(name.strip().lower())


def normalize_manual_url(url: str, manual_base_url: str = MANUAL_BASE_URL) -> str:
    """Use the configured manual host casing for generated manual URLs."""
    parsed = urlsplit(url)
    base = urlsplit(manual_base_url)
    if parsed.scheme in {'http', 'https'} and parsed.netloc.lower() == base.netloc.lower():
        return urlunsplit((base.scheme or parsed.scheme, base.netloc, parsed.path, parsed.query, parsed.fragment))
    return url


def chapter_mapping_to_link_overrides(
    chapter_mapping: Optional[Mapping[str, list]],
    manual_base_url: str = MANUAL_BASE_URL,
) -> Dict[str, str]:
    """Convert PARAM_NAME -> chapter pages into lowercase Markdown link overrides."""
    overrides: Dict[str, str] = {}
    if not chapter_mapping:
        return overrides

    for param_name, pages in chapter_mapping.items():
        if not pages:
            continue
        first_page = pages[0]
        if not isinstance(first_page, Mapping):
            continue
        url = first_page.get('url')
        if isinstance(url, str) and url:
            overrides[normalize_parameter_link_key(param_name)] = normalize_manual_url(url, manual_base_url)
    return overrides


def load_parameter_link_overrides_from_json(
    project_root: Path,
    manual_base_url: str = MANUAL_BASE_URL,
) -> Dict[str, str]:
    """Load parameter chapter URLs from the generated public parameters JSON."""
    json_path = project_root / "assets" / "json" / "parameters.json"
    if not json_path.exists():
        return {}

    data = json.loads(json_path.read_text(encoding='utf-8'))
    params = data.get('parameters') or {}
    overrides: Dict[str, str] = {}
    for param_name, entry in params.items():
        if not isinstance(entry, Mapping):
            continue
        url = entry.get('manualPageUrl') or entry.get('chapterUrl')
        if isinstance(url, str) and url:
            overrides[normalize_parameter_link_key(param_name)] = normalize_manual_url(url, manual_base_url)
    return overrides


def merge_link_overrides(
    *overrides: Optional[Mapping[str, str]],
) -> Dict[str, str]:
    """Merge link override maps using normalized parameter keys."""
    merged: Dict[str, str] = {}
    for override_map in overrides:
        if not override_map:
            continue
        for key, url in override_map.items():
            if url:
                merged[normalize_parameter_link_key(key)] = url
    return merged


def load_markdown_variables(
    variables_yml_path: Path,
    manual_base_url: str = MANUAL_BASE_URL,
    show_ci: bool = False,
    chapter_mapping: Optional[Mapping[str, list]] = None,
    link_overrides: Optional[Mapping[str, str]] = None,
) -> Dict[str, str]:
    """Load Quarto variables for Markdown, preserving parameter values as links."""
    merged_overrides = merge_link_overrides(
        link_overrides,
        chapter_mapping_to_link_overrides(chapter_mapping, manual_base_url),
    )
    variables = load_variables(
        variables_yml_path,
        preserve_links=True,
        link_base_url=manual_base_url,
        link_overrides=merged_overrides,
    )
    if show_ci:
        return variables
    return {key: strip_confidence_intervals(value) for key, value in variables.items()}


def split_qmd_frontmatter(content: str) -> Tuple[dict, str]:
    """Return parsed YAML frontmatter and body content."""
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n?', content)
    if not match:
        return {}, content

    metadata = yaml_safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        metadata = {}

    return metadata, content[match.end():]


def extract_content_after_frontmatter(content: str) -> str:
    """Return QMD content after YAML frontmatter."""
    _, body = split_qmd_frontmatter(content)
    return body


def qmd_rel_to_html_url(path: Path, project_root: Path, manual_base_url: str) -> str:
    """Convert a project QMD path to its public manual HTML URL."""
    rel_path = path.resolve().relative_to(project_root.resolve()).as_posix()
    if rel_path.endswith('.qmd'):
        rel_path = rel_path[:-4] + '.html'
    return f"{manual_base_url.rstrip('/')}/{rel_path}"


def qmd_path_to_html_path(path: str) -> str:
    """Convert a URL path ending in .qmd to the rendered .html path."""
    if path.endswith('.qmd'):
        return path[:-4] + '.html'
    return path


def resolve_manual_href(
    href: str,
    source_path: Path,
    project_root: Path,
    manual_base_url: str = MANUAL_BASE_URL,
) -> str:
    """Resolve local Markdown/QMD links to public manual URLs."""
    href = href.strip()
    if not href:
        return href

    source_url = qmd_rel_to_html_url(source_path, project_root, manual_base_url)

    if href.startswith('#'):
        return f"{source_url}{href}"

    if href.startswith(('mailto:', 'tel:', 'javascript:', '{{', '//')):
        return href

    parsed = urlsplit(href)

    if parsed.scheme in {'http', 'https'}:
        if parsed.netloc.lower() == 'manual.warondisease.org':
            path = qmd_path_to_html_path(parsed.path)
            return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))
        return href

    base = urlsplit(manual_base_url)
    scheme = base.scheme or 'https'
    netloc = base.netloc

    if href.startswith('/'):
        path = qmd_path_to_html_path(parsed.path)
        return urlunsplit((scheme, netloc, path, parsed.query, parsed.fragment))

    path = parsed.path.replace('\\', '/')
    if not path:
        return href

    if path.endswith(('.qmd', '.html')) or path.startswith(('assets/', './assets/', '../assets/')):
        resolved_path = (source_path.parent / path).resolve()
        rel_path = resolved_path.relative_to(project_root.resolve()).as_posix()
        rel_path = qmd_path_to_html_path(rel_path)
        return urlunsplit((scheme, netloc, f"/{rel_path}", parsed.query, parsed.fragment))

    return href


def absolutize_manual_links(
    content: str,
    source_path: Path,
    project_root: Path,
    manual_base_url: str = MANUAL_BASE_URL,
) -> str:
    """Convert local Markdown link targets to absolute manual URLs."""
    link_pattern = re.compile(r'(!?\[[^\]]*\]\()([^\s)]+)(\))')

    def replace_link(match: re.Match) -> str:
        return (
            match.group(1)
            + resolve_manual_href(match.group(2), source_path, project_root, manual_base_url)
            + match.group(3)
        )

    return link_pattern.sub(replace_link, content)


def qmd_content_to_markdown(
    content: str,
    source_path: Path,
    project_root: Path,
    variables: Dict[str, str],
    manual_base_url: str = MANUAL_BASE_URL,
    include_title: bool = False,
) -> str:
    """Resolve a QMD document body into portable Markdown."""
    metadata, body = split_qmd_frontmatter(content)

    if include_title and metadata.get('title'):
        body = f"# {metadata['title']}\n\n{body.lstrip()}"

    body = replace_variables(body, variables, highlight_missing=False)
    body = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', body, flags=re.IGNORECASE | re.DOTALL)
    body = clean_for_readme(body)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
    body = re.sub(r'<a\s+[^>]*>([^<]*)</a>', r'\1', body)
    body = absolutize_manual_links(body, source_path, project_root, manual_base_url)
    body = re.sub(r'\n{4,}', '\n\n\n', body)
    body = '\n'.join(line.rstrip() for line in body.splitlines())
    return body.strip() + '\n'
