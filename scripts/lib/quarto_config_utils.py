#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quarto Config Discovery Utilities
=================================

Shared functions for discovering and filtering Quarto config files.
Provides consistent skip lists across all scripts.

Usage:
    from lib.quarto_config_utils import (
        discover_paper_configs,  # For Zenodo upload
        discover_deployable_configs,  # For Netlify deploy
        discover_syncable_configs,  # For config sync
        get_all_config_names,  # For rendering (all configs)
    )
"""

import os
import sys
import subprocess
from pathlib import Path
from email.utils import parsedate_to_datetime
from datetime import timezone
from typing import Any, Dict, List, Optional, Set
from urllib.parse import urljoin

if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

try:
    import yaml
except ImportError:
    print("ERROR: Missing pyyaml. Run: pip install pyyaml")
    sys.exit(1)


# =============================================================================
# Config Categories - Central Source of Truth
# =============================================================================

# Configs that are never papers (not uploadable to Zenodo)
NON_PAPER_CONFIGS: Set[str] = {
    "manual",           # Full book/manual - not a standalone paper
    "book",             # Main book config (alias for manual in some contexts)
    "test",             # Test config for CI
    "base",             # Base config (if exists)
    "shared-defaults",  # Shared defaults template - not a renderable config
}

# Configs that should never be deployed to Netlify
NON_DEPLOYABLE_CONFIGS: Set[str] = {
    "test",             # Test config
    "shared-defaults",  # Template file
}

# Configs to skip during config sync (have different structures)
NON_SYNCABLE_CONFIGS: Set[str] = {
    "manual",           # Book config (different structure)
    "test",             # Test config
    "shared-defaults",  # The defaults file itself
}

# Full filenames for configs that should be skipped (used by quarto_config_sync)
SKIP_CONFIG_FILES: Set[str] = {
    "_quarto.yml",              # Base Quarto config (generated)
    "_quarto-manual.yml",       # Book config (different structure)
    "_quarto-test.yml",         # Test config
    "_quarto-shared-defaults.yml",  # The defaults file itself
}


# =============================================================================
# Discovery Functions
# =============================================================================

def _find_project_root(start_path: Optional[Path] = None) -> Path:
    """Find the project root by looking for package.json or _quarto-manual.yml."""
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path).resolve()
    markers = ["package.json", "_quarto-manual.yml", "_quarto-1-pct-treaty-impact.yml"]

    for path in [current] + list(current.parents):
        for marker in markers:
            if (path / marker).exists():
                return path

    return current


def _extract_config_key(config_path: Path) -> str:
    """Extract config key from path (e.g., 'economics' from '_quarto-economics.yml')."""
    return config_path.stem.replace("_quarto-", "")


def _load_config(config_path: Path) -> Optional[Dict[str, Any]]:
    """Safely load a YAML config file."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[WARN] Could not read {config_path}: {e}")
        return None


def get_all_config_paths(project_root: Optional[Path] = None) -> List[Path]:
    """
    Get all _quarto-*.yml config file paths (excludes _build_temp copies).

    Returns:
        List of Path objects for all Quarto config files
    """
    if project_root is None:
        project_root = _find_project_root()

    configs = []
    for config_path in project_root.glob("_quarto-*.yml"):
        # Skip build temp copies
        if "_build_temp" in str(config_path):
            continue
        configs.append(config_path)

    return sorted(configs)


def get_all_config_names(project_root: Optional[Path] = None) -> List[str]:
    """
    Get all config names (for rendering - no filtering).

    Returns:
        List of config names like ['economics', 'iab', 'manual', 'test', ...]
    """
    return [_extract_config_key(p) for p in get_all_config_paths(project_root)]


def discover_paper_configs(
    project_root: Optional[Path] = None,
    include_disabled: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    Discover Quarto configs that represent standalone papers (for Zenodo upload).

    Excludes: manual, book, test, base, shared-defaults, and configs with zenodo: false

    Args:
        project_root: Project root directory (auto-detected if None)
        include_disabled: If True, include configs with zenodo: false

    Returns:
        Dict mapping config key to config info:
        {
            "economics": {
                "config_path": Path(...),
                "config": {...},
                "pdf_path": "...",
                "title": "...",
            },
            ...
        }
    """
    if project_root is None:
        project_root = _find_project_root()

    papers = {}

    for config_path in get_all_config_paths(project_root):
        key = _extract_config_key(config_path)

        # Skip non-paper configs
        if key in NON_PAPER_CONFIGS or not key or key == "quarto":
            continue

        config = _load_config(config_path)
        if config is None:
            continue

        # Check for explicit zenodo disable
        dih_render = config.get("dih-render", {})
        if not include_disabled and dih_render.get("zenodo") is False:
            continue

        # Get PDF filename
        pdf_filename = dih_render.get("pdf-output-file")
        if not pdf_filename:
            pdf_config = config.get("format", {}).get("pdf", {})
            pdf_filename = pdf_config.get("output-file", f"{key}-paper.pdf")

        # Get title
        title = (
            config.get("book", {}).get("title") or
            config.get("website", {}).get("title") or
            key.replace("-", " ").title()
        )

        papers[key] = {
            "config_path": config_path,
            "config": config,
            "pdf_path": f"_build_temp/{key}/_site/{key}/{pdf_filename}",
            "pdf_filename": pdf_filename,
            "title": title,
            "dih_render": dih_render,
        }

    return papers


def discover_pdf_work_items_sorted(
    project_root: Optional[Path] = None,
    selected_configs: Optional[List[str]] = None,
    include_disabled: bool = False,
) -> List[Dict[str, Any]]:
    """
    Discover config items for PDF workflows, sorted by QMD count (smallest first).

    When `selected_configs` is provided, includes exactly those config names (if present),
    even if they are non-paper configs such as test/manual.
    When omitted, defaults to standalone paper configs from discover_paper_configs().

    Returns items with these keys:
    - config_name
    - config_path
    - config
    - qmd_count
    - pdf_filename
    - assets_pdf_rel_path
    - assets_pdf_path
    - build_pdf_path
    """
    if project_root is None:
        project_root = _find_project_root()

    items: List[Dict[str, Any]] = []

    if selected_configs:
        selected_set = {name.strip() for name in selected_configs if name and name.strip()}
        for config_name in sorted(selected_set):
            config_path = project_root / f"_quarto-{config_name}.yml"
            if not config_path.exists():
                continue
            config = _load_config(config_path)
            if config is None:
                continue
            pdf_filename = _get_pdf_output_filename_for_paper(config_name, config)
            assets_pdf_rel_path = f"assets/pdfs/{pdf_filename}"
            items.append(
                {
                    "config_name": config_name,
                    "config_path": config_path,
                    "config": config,
                    "qmd_count": count_qmd_files(config),
                    "pdf_filename": pdf_filename,
                    "assets_pdf_rel_path": assets_pdf_rel_path,
                    "assets_pdf_path": project_root / assets_pdf_rel_path,
                    "build_pdf_path": project_root / "_build_temp" / config_name / "_site" / config_name / pdf_filename,
                }
            )
    else:
        papers = discover_paper_configs(project_root=project_root, include_disabled=include_disabled)
        for config_name, info in papers.items():
            pdf_filename = info.get("pdf_filename") or Path(info["pdf_path"]).name
            assets_pdf_rel_path = f"assets/pdfs/{pdf_filename}"
            items.append(
                {
                    "config_name": config_name,
                    "config_path": info["config_path"],
                    "config": info["config"],
                    "qmd_count": count_qmd_files(info["config"]),
                    "pdf_filename": pdf_filename,
                    "assets_pdf_rel_path": assets_pdf_rel_path,
                    "assets_pdf_path": project_root / assets_pdf_rel_path,
                    "build_pdf_path": project_root / info["pdf_path"],
                }
            )

    items.sort(key=lambda item: item["qmd_count"])
    return items


def discover_deployable_configs(
    project_root: Optional[Path] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Discover Quarto configs that can be deployed to Netlify.

    Excludes: test, shared-defaults

    Args:
        project_root: Project root directory (auto-detected if None)

    Returns:
        Dict mapping config key to config info with Netlify-relevant fields
    """
    if project_root is None:
        project_root = _find_project_root()

    configs = {}

    for config_path in get_all_config_paths(project_root):
        key = _extract_config_key(config_path)

        # Skip non-deployable configs
        if key in NON_DEPLOYABLE_CONFIGS or not key or key == "quarto":
            continue

        config = _load_config(config_path)
        if config is None:
            continue

        # Get project info
        project_type = config.get("project", {}).get("type", "website")
        output_dir = config.get("project", {}).get("output-dir", f"_site/{key}")

        # Get title and site URL
        if project_type == "book":
            section = config.get("book", {})
        else:
            section = config.get("website", {})

        title = section.get("title", key.replace("-", " ").title())
        site_url = section.get("site-url")

        # Also check website section for books that have both
        if not site_url and "website" in config:
            site_url = config["website"].get("site-url")

        # Get Netlify info
        dih_render = config.get("dih-render", {})

        configs[key] = {
            "config_path": config_path,
            "config": config,
            "title": title,
            "project_type": project_type,
            "output_dir": output_dir,
            "site_url": site_url,
            "site_id": dih_render.get("netlify-site-id"),
            "netlify_cname": dih_render.get("netlify-cname"),
        }

    return configs


def discover_syncable_configs(
    project_root: Optional[Path] = None,
) -> List[Path]:
    """
    Discover Quarto configs that should be synced with shared defaults.

    Excludes: _quarto.yml, manual, test, shared-defaults

    Args:
        project_root: Project root directory (auto-detected if None)

    Returns:
        List of config file paths that should be synced
    """
    if project_root is None:
        project_root = _find_project_root()

    configs = []

    for config_path in get_all_config_paths(project_root):
        # Skip by full filename
        if config_path.name in SKIP_CONFIG_FILES:
            continue

        key = _extract_config_key(config_path)

        # Skip by key
        if key in NON_SYNCABLE_CONFIGS or not key or key == "quarto":
            continue

        configs.append(config_path)

    return sorted(configs)


def is_paper_config(config_name: str) -> bool:
    """Check if a config name represents a paper (vs book/test/etc)."""
    return config_name not in NON_PAPER_CONFIGS and config_name and config_name != "quarto"


def is_deployable_config(config_name: str) -> bool:
    """Check if a config name can be deployed to Netlify."""
    return config_name not in NON_DEPLOYABLE_CONFIGS and config_name and config_name != "quarto"


def is_syncable_config(config_name: str) -> bool:
    """Check if a config name should be synced with shared defaults."""
    return config_name not in NON_SYNCABLE_CONFIGS and config_name and config_name != "quarto"


# =============================================================================
# Helper for QMD file counting (used by upload scripts)
# =============================================================================

def count_qmd_files(config: Dict[str, Any]) -> int:
    """Count QMD files referenced in a Quarto config."""
    return len(get_qmd_files_from_config(config))


def get_qmd_files_from_config(config: Dict[str, Any]) -> List[str]:
    """
    Get list of QMD file paths referenced in a Quarto config.

    Extracts from book.chapters, project.render, appendices, etc.
    Returns paths as they appear in the config (relative to project root).
    """
    files: List[str] = []

    def extract_items(items):
        if not items:
            return
        for item in items:
            if isinstance(item, str):
                if item.endswith('.qmd'):
                    files.append(item)
            elif isinstance(item, dict):
                if 'href' in item and item['href'].endswith('.qmd'):
                    files.append(item['href'])
                for key in ('chapters', 'contents', 'parts', 'appendices'):
                    if key in item:
                        extract_items(item[key])

    # Book format
    book = config.get('book', {})
    if book.get('chapters'):
        extract_items(book['chapters'])
    if book.get('appendices'):
        extract_items(book['appendices'])

    # Website format
    project = config.get('project', {})
    if project.get('render'):
        extract_items(project['render'])

    return files


def get_all_book_qmd_files(project_root: Optional[Path] = None) -> Set[str]:
    """
    Get all QMD files that are part of any Quarto book/website config.

    This is the authoritative source for which QMD files matter for
    duplicate anchor detection and other cross-file validations.

    Returns:
        Set of normalized file paths relative to project root
    """
    if project_root is None:
        project_root = _find_project_root()

    all_files: Set[str] = set()

    for config_path in get_all_config_paths(project_root):
        config = _load_config(config_path)
        if config is None:
            continue

        # Get QMD files from this config
        qmd_files = get_qmd_files_from_config(config)

        # Normalize paths
        for f in qmd_files:
            # Normalize path separators
            normalized = f.replace('\\', '/')
            all_files.add(normalized)

    return all_files


def get_paper_source_files(
    paper_key: str,
    paper_config: Dict[str, Any],
    project_root: Optional[Path] = None,
) -> List[Path]:
    """
    Get source files that determine whether a paper PDF is stale.

    Includes:
    - _quarto-<key>.yml
    - _quarto-shared-defaults.yml
    - references.bib (global citation source of truth)
    - dih-render.index-source (authoritative editable source for paper configs)
    - all .qmd files from project.render/book sections
    """
    if project_root is None:
        project_root = _find_project_root()

    config_path = paper_config.get("config_path") or (project_root / f"_quarto-{paper_key}.yml")
    config = paper_config.get("config", {}) or {}

    files: List[Path] = [
        Path(config_path),
        project_root / "_quarto-shared-defaults.yml",
        project_root / "references.bib",
    ]

    # Most paper configs render index.qmd but author edits occur in dih-render.index-source.
    # Include both so staleness checks catch direct edits to source files.
    dih_render = config.get("dih-render", {})
    if isinstance(dih_render, dict):
        index_source = dih_render.get("index-source")
        if isinstance(index_source, str) and index_source.strip():
            files.append(project_root / index_source)

    for qmd_file in get_qmd_files_from_config(config):
        files.append(project_root / qmd_file)

    # De-duplicate while preserving order
    seen: Set[Path] = set()
    deduped: List[Path] = []
    for path in files:
        resolved = Path(path)
        if resolved in seen:
            continue
        seen.add(resolved)
        deduped.append(resolved)

    return deduped


def get_newest_paper_source_mtime(
    paper_key: str,
    paper_config: Dict[str, Any],
    project_root: Optional[Path] = None,
) -> float:
    """Get newest source mtime for a paper. Returns 0.0 when no source files exist."""
    source_files = get_paper_source_files(paper_key, paper_config, project_root)
    mtimes = [p.stat().st_mtime for p in source_files if p.exists()]
    return max(mtimes) if mtimes else 0.0


def paper_sources_have_uncommitted_changes(
    paper_key: str,
    paper_config: Dict[str, Any],
    project_root: Optional[Path] = None,
) -> bool:
    """
    Check whether any paper source files have uncommitted changes.

    If git status cannot be checked, returns True (conservative: force rebuild).
    """
    if project_root is None:
        project_root = _find_project_root()

    source_files = get_paper_source_files(paper_key, paper_config, project_root)
    relative_paths: List[str] = []
    root_resolved = project_root.resolve()
    for path in source_files:
        try:
            relative_paths.append(str(path.resolve().relative_to(root_resolved)))
        except Exception:
            relative_paths.append(str(path))

    if not relative_paths:
        return True

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--", *relative_paths],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return True

    if result.returncode != 0:
        return True

    return bool(result.stdout.strip())


def _get_site_url_for_paper(config: Dict[str, Any]) -> Optional[str]:
    """Get site-url from project, website, or book section."""
    project_site = config.get("project", {}).get("site-url")
    if project_site:
        return str(project_site)

    website_site = config.get("website", {}).get("site-url")
    if website_site:
        return str(website_site)

    book_site = config.get("book", {}).get("site-url")
    if book_site:
        return str(book_site)

    return None


def _get_pdf_output_filename_for_paper(paper_key: str, config: Dict[str, Any]) -> str:
    """Get PDF output filename from format.pdf.output-file with safe fallbacks."""
    pdf_config = config.get("format", {}).get("pdf", {})
    if isinstance(pdf_config, dict):
        output_file = pdf_config.get("output-file")
        if output_file:
            return str(output_file)

    dih_render = config.get("dih-render", {})
    if isinstance(dih_render, dict):
        output_file = dih_render.get("pdf-output-file")
        if output_file:
            return str(output_file)

    return f"{paper_key}-paper.pdf"


def check_and_download_remote_pdf(
    paper_key: str,
    paper_config: Dict[str, Any],
    project_root: Optional[Path] = None,
    timeout: int = 30,
) -> Optional[Path]:
    """
    Download a remote published PDF when sources are clean (no uncommitted changes).

    Returns:
        Path to downloaded PDF when successful, otherwise None.
    """
    if project_root is None:
        project_root = _find_project_root()

    config = paper_config.get("config", {}) or {}

    if paper_sources_have_uncommitted_changes(paper_key, paper_config, project_root):
        return None

    site_url = _get_site_url_for_paper(config)
    if not site_url:
        return None

    output_filename = _get_pdf_output_filename_for_paper(paper_key, config)
    remote_url = urljoin(site_url.rstrip("/") + "/", output_filename)

    pdf_rel_path = paper_config.get("pdf_path")
    if pdf_rel_path:
        destination = project_root / str(pdf_rel_path)
    else:
        destination = project_root / "_build_temp" / paper_key / "_site" / paper_key / output_filename

    try:
        import requests
    except ImportError:
        print("WARN: requests not available; skipping remote PDF download")
        return None

    try:
        head_response = requests.head(remote_url, allow_redirects=True, timeout=timeout)
        if head_response.status_code != 200:
            return None

        # Parse remote modified time when available so we can make a real freshness decision.
        remote_mtime: Optional[float] = None
        last_modified = head_response.headers.get("Last-Modified")
        if last_modified:
            try:
                dt = parsedate_to_datetime(last_modified)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                remote_mtime = dt.timestamp()
            except Exception:
                remote_mtime = None

        if destination.exists():
            local_mtime = destination.stat().st_mtime
            if remote_mtime is not None and local_mtime >= remote_mtime:
                return destination
            if remote_mtime is None:
                # If remote timestamp is unknown, keep local file to avoid downgrading.
                return destination

        get_response = requests.get(remote_url, stream=True, timeout=timeout)
        if get_response.status_code != 200:
            return None

        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "wb") as f:
            for chunk in get_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Preserve remote modified time when available.
        if remote_mtime is not None:
            os.utime(destination, (remote_mtime, remote_mtime))
    except Exception:
        return None

    if destination.exists() and destination.stat().st_size > 0:
        return destination

    return None


if __name__ == "__main__":
    # Test discovery functions
    project_root = _find_project_root()
    print(f"Project root: {project_root}\n")

    print("All configs:")
    for name in get_all_config_names(project_root):
        print(f"  {name}")

    print("\nPaper configs (for Zenodo):")
    for key, info in discover_paper_configs(project_root).items():
        print(f"  {key}: {info['title'][:50]}")

    print("\nDeployable configs (for Netlify):")
    for key, info in discover_deployable_configs(project_root).items():
        site_id = info.get('site_id', '(none)')[:20] if info.get('site_id') else '(none)'
        print(f"  {key}: {site_id}")

    print("\nSyncable configs:")
    for path in discover_syncable_configs(project_root):
        print(f"  {path.name}")
