#!/usr/bin/env python3
"""
Quarto Preparation Utilities
============================

Shared utilities for preparing Quarto files before rendering:
- Copying and updating relative paths for economics.qmd -> index.qmd
- Copying index-book.qmd -> index.qmd for book rendering
- Copying config files (_quarto-book.yml, _quarto-economics.yml -> _quarto.yml)
"""

import sys
import shutil
from pathlib import Path
from typing import Optional


def _find_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find the project root by looking for package.json or _quarto-book.yml.
    
    Args:
        start_path: Path to start searching from (default: current working directory)
        
    Returns:
        Path to project root
        
    Raises:
        FileNotFoundError: If project root cannot be found
    """
    if start_path is None:
        start_path = Path.cwd()
    
    current = Path(start_path).resolve()
    
    # Look for project root markers
    markers = ['package.json', '_quarto-book.yml', '_quarto-economics.yml']
    
    # Walk up the directory tree
    for path in [current] + list(current.parents):
        for marker in markers:
            if (path / marker).exists():
                return path
    
    # If we can't find markers, assume we're already at root
    return current


def prepare_economics_index(verbose: bool = True) -> bool:
    """
    Copy economics.qmd to index.qmd and update relative paths.
    
    Args:
        verbose: Whether to print status messages
        
    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()
    
    economics_qmd = project_root / 'knowledge' / 'economics' / 'economics.qmd'
    index_qmd = project_root / 'index.qmd'
    
    if not economics_qmd.exists():
        if verbose:
            print(f"[ERROR] Missing {economics_qmd.relative_to(project_root)}", file=sys.stderr)
            print("        Unable to prepare economics index.", file=sys.stderr)
        return False
    
    if verbose:
        print(f"[*] Copying {economics_qmd.relative_to(project_root)} -> index.qmd", flush=True)
    
    try:
        with open(economics_qmd, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update relative paths: ../ becomes knowledge/
        # This handles paths like ../figures/, ../appendix/, ../references.qmd, etc.
        content = content.replace('../', 'knowledge/')
        
        with open(index_qmd, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to copy economics.qmd: {e}", file=sys.stderr)
        return False


def prepare_book_index(verbose: bool = True) -> bool:
    """
    Copy index-book.qmd to index.qmd for book rendering.
    
    Args:
        verbose: Whether to print status messages
        
    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()
    
    index_book_qmd = project_root / 'index-book.qmd'
    index_qmd = project_root / 'index.qmd'
    
    if not index_book_qmd.exists():
        if verbose:
            print(f"[ERROR] Missing {index_book_qmd.relative_to(project_root)}", file=sys.stderr)
            print("        Unable to prepare book index.", file=sys.stderr)
        return False
    
    if verbose:
        print(f"[*] Copying {index_book_qmd.relative_to(project_root)} -> index.qmd", flush=True)
    
    try:
        shutil.copy2(index_book_qmd, index_qmd)
        return True
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to copy index-book.qmd: {e}", file=sys.stderr)
        return False


def prepare_quarto_config(config_name: str, verbose: bool = True) -> bool:
    """
    Copy a Quarto config file to _quarto.yml.
    
    Args:
        config_name: Name of config file (e.g., '_quarto-book.yml', '_quarto-economics.yml')
        verbose: Whether to print status messages
        
    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()
    
    config_file = project_root / config_name
    quarto_yml = project_root / '_quarto.yml'
    
    if not config_file.exists():
        if verbose:
            print(f"[ERROR] Missing {config_file.relative_to(project_root)}", file=sys.stderr)
        return False
    
    if verbose:
        print(f"[*] Copying {config_file.name} -> _quarto.yml", flush=True)
    
    try:
        shutil.copy2(config_file, quarto_yml)
        return True
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to copy config: {e}", file=sys.stderr)
        return False


def prepare_economics(verbose: bool = True) -> bool:
    """
    Prepare everything needed for economics rendering:
    - Copy _quarto-economics.yml to _quarto.yml
    - Copy economics.qmd to index.qmd with updated paths
    
    Args:
        verbose: Whether to print status messages
        
    Returns:
        True if successful, False otherwise
    """
    if not prepare_quarto_config('_quarto-economics.yml', verbose):
        return False
    
    if not prepare_economics_index(verbose):
        return False
    
    return True


def prepare_book(verbose: bool = True) -> bool:
    """
    Prepare everything needed for book rendering:
    - Copy _quarto-book.yml to _quarto.yml
    - Copy index-book.qmd to index.qmd
    
    Args:
        verbose: Whether to print status messages
        
    Returns:
        True if successful, False otherwise
    """
    if not prepare_quarto_config('_quarto-book.yml', verbose):
        return False
    
    if not prepare_book_index(verbose):
        return False
    
    return True

