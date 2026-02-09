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
