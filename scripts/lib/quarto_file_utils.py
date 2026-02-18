#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quarto File Utilities
=====================

Centralized utilities for finding QMD files in the project.
Uses `git ls-files` to respect .gitignore patterns automatically.

Usage:
    from lib.quarto_file_utils import (
        get_all_qmd_files,      # All QMD files (respects .gitignore)
        get_book_qmd_files,     # Only files referenced in Quarto configs
        is_ignored_path,        # Check if a path would be ignored
    )
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Set

if sys.platform == 'win32':
    import io
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path for dih_models imports
_project_root = str(Path(__file__).parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


# =============================================================================
# Fallback Ignore Patterns (used when git is not available)
# =============================================================================

# Only used as fallback when git ls-files is not available
IGNORED_DIRS: Set[str] = {
    "_book", "_site", "_build_temp", ".quarto",
    "node_modules", ".venv", "venv", "__pycache__",
    ".git", ".claude", ".cursor", ".idea", ".vscode",
    "docs", "GUIDES", "__tests__",
}

# File patterns to skip
IGNORED_FILES: Set[str] = {
    "references.qmd",  # Auto-generated
}


# =============================================================================
# Project Root Detection
# =============================================================================

def find_project_root(start_path: Optional[Path] = None) -> Path:
    """Find the project root by looking for marker files."""
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path).resolve()
    markers = ["package.json", "_quarto-manual.yml", "_quarto.yml"]

    for path in [current] + list(current.parents):
        for marker in markers:
            if (path / marker).exists():
                return path

    return current


# =============================================================================
# File Discovery Functions
# =============================================================================

def is_ignored_path(path: str, project_root: Optional[Path] = None) -> bool:
    """
    Check if a path should be ignored based on IGNORED_DIRS and IGNORED_FILES.

    Args:
        path: File or directory path (relative or absolute)
        project_root: Project root for resolving relative paths

    Returns:
        True if the path should be ignored
    """
    if project_root is None:
        project_root = find_project_root()

    # Normalize path
    path_obj = Path(path)
    if not path_obj.is_absolute():
        path_obj = project_root / path_obj

    # Check if any parent directory is in IGNORED_DIRS
    try:
        rel_path = path_obj.relative_to(project_root)
    except ValueError:
        rel_path = path_obj

    for part in rel_path.parts:
        if part in IGNORED_DIRS:
            return True

    # Check if filename is in IGNORED_FILES
    if path_obj.name in IGNORED_FILES:
        return True

    return False


def find_files_by_extension(
    extensions: tuple,
    project_root: Optional[Path] = None,
) -> List[str]:
    """
    Find all files with given extensions, respecting .gitignore patterns.

    Uses `git ls-files` for accurate .gitignore handling.
    Falls back to os.walk with hardcoded ignores if git is not available.

    Args:
        extensions: Tuple of extensions to find (e.g., (".qmd", ".md"))
        project_root: Project root directory (auto-detected if None)

    Returns:
        List of file paths relative to project root, sorted alphabetically
    """
    if project_root is None:
        project_root = find_project_root()

    # Build glob patterns for git ls-files
    patterns = []
    for ext in extensions:
        ext_clean = ext.lstrip('.')
        patterns.extend([
            f"*.{ext_clean}",
            f"*/*.{ext_clean}",
            f"*/*/*.{ext_clean}",
            f"*/*/*/*.{ext_clean}",
            f"*/*/*/*/*.{ext_clean}",
        ])

    def should_skip(filepath: str) -> bool:
        """Check if filepath contains any ignored directory."""
        parts = filepath.replace('\\', '/').split('/')
        return any(part in IGNORED_DIRS for part in parts)

    # Try git ls-files first (respects .gitignore automatically)
    try:
        result = subprocess.run(
            ["git", "ls-files"] + patterns,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            files = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                # Normalize path
                filepath = line.replace('\\', '/')
                # Skip files in ignored directories
                if should_skip(filepath):
                    continue
                files.append(filepath)
            return sorted(files)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass  # Fall back to os.walk

    # Fallback: use os.walk with hardcoded ignores
    files: List[str] = []

    for dirpath, dirnames, filenames in os.walk(project_root):
        # Filter out ignored directories IN PLACE (prevents descending)
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]

        for filename in filenames:
            if not any(filename.endswith(ext) for ext in extensions):
                continue

            # Get relative path
            full_path = Path(dirpath) / filename
            rel_path = full_path.relative_to(project_root)

            # Normalize to forward slashes for consistency
            files.append(str(rel_path).replace('\\', '/'))

    return sorted(files)


def get_all_qmd_files(
    project_root: Optional[Path] = None,
    include_index: bool = False,
) -> List[str]:
    """
    Get all QMD files in the project, respecting .gitignore patterns.

    Uses `git ls-files` for accurate .gitignore handling.
    Falls back to os.walk with hardcoded ignores if git is not available.

    This is the authoritative function for finding QMD files.
    Use this instead of glob or os.walk with manual filtering.

    Args:
        project_root: Project root directory (auto-detected if None)
        include_index: Whether to include index.qmd (usually auto-generated)

    Returns:
        List of file paths relative to project root, sorted alphabetically
    """
    all_files = find_files_by_extension((".qmd",), project_root)

    # Filter out ignored files and optionally index.qmd
    qmd_files = []
    for filepath in all_files:
        filename = Path(filepath).name
        if filename in IGNORED_FILES:
            continue
        if not include_index and filename == "index.qmd":
            continue
        qmd_files.append(filepath)

    return sorted(qmd_files)


def get_book_qmd_files(
    project_root: Optional[Path] = None,
    config_name: str = "manual",
) -> List[str]:
    """
    Get QMD files that are part of a specific Quarto book/website config.

    This reads the actual config file to find which files are included.
    Use this when you need only the files in a specific build.

    Args:
        project_root: Project root directory (auto-detected if None)
        config_name: Name of config (e.g., "manual", "economics")

    Returns:
        List of file paths relative to project root
    """
    if project_root is None:
        project_root = find_project_root()

    from dih_models.yaml_utils import load_quarto_config

    config_path = project_root / f"_quarto-{config_name}.yml"
    if not config_path.exists():
        print(f"WARNING: Config not found: {config_path}", file=sys.stderr)
        return []

    try:
        config = load_quarto_config(config_path)
    except Exception as e:
        print(f"WARNING: Failed to load config: {e}", file=sys.stderr)
        return []

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


def get_all_configs_qmd_files(project_root: Optional[Path] = None) -> Set[str]:
    """
    Get all QMD files referenced in ANY Quarto config.

    Union of all files from all _quarto-*.yml configs.
    Use this for cross-config validations like duplicate anchor detection.

    Returns:
        Set of normalized file paths relative to project root
    """
    if project_root is None:
        project_root = find_project_root()

    all_files: Set[str] = set()

    for config_path in project_root.glob("_quarto-*.yml"):
        # Skip build temp copies
        if "_build_temp" in str(config_path):
            continue

        config_name = config_path.stem.replace("_quarto-", "")
        files = get_book_qmd_files(project_root, config_name)

        for f in files:
            # Normalize path separators
            normalized = f.replace('\\', '/')
            all_files.add(normalized)

    return all_files


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find QMD files in project")
    parser.add_argument("--all", action="store_true", help="Show all QMD files")
    parser.add_argument("--book", type=str, help="Show files from specific config")
    parser.add_argument("--configs", action="store_true", help="Show files from all configs")
    args = parser.parse_args()

    project_root = find_project_root()
    print(f"Project root: {project_root}\n")

    if args.book:
        print(f"QMD files in {args.book} config:")
        for f in get_book_qmd_files(project_root, args.book):
            print(f"  {f}")
    elif args.configs:
        print("QMD files in ALL configs:")
        for f in sorted(get_all_configs_qmd_files(project_root)):
            print(f"  {f}")
    else:
        files = get_all_qmd_files(project_root)
        print(f"All QMD files ({len(files)}):")
        for f in files:
            print(f"  {f}")
