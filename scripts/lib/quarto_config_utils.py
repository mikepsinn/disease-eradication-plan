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

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

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
    count = 0

    def count_items(items):
        nonlocal count
        if not items:
            return
        for item in items:
            if isinstance(item, str):
                if item.endswith('.qmd'):
                    count += 1
            elif isinstance(item, dict):
                if 'href' in item and item['href'].endswith('.qmd'):
                    count += 1
                for key in ('chapters', 'contents', 'parts'):
                    if key in item:
                        count_items(item[key])

    # Book format
    book = config.get('book', {})
    if book.get('chapters'):
        count_items(book['chapters'])

    # Website format
    project = config.get('project', {})
    if project.get('render'):
        count_items(project['render'])

    return count


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
