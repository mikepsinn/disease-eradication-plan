#!/usr/bin/env python3
"""Shared Python interpreter resolution helpers."""

from pathlib import Path
import sys


def get_preferred_python(project_root: Path) -> str:
    """Prefer project virtualenv Python when available."""
    if sys.platform == "win32":
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = project_root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def load_project_dotenv(project_root: Path, override: bool = True) -> bool:
    """
    Load .env from project root when python-dotenv is available.

    Returns True when loading succeeded, False when dotenv is unavailable
    or loading raised an exception.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return False
    try:
        env_path = project_root / ".env"
        load_dotenv(env_path, override=override)
        return True
    except Exception:
        return False
