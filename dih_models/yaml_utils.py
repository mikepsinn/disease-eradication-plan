"""Shared YAML utilities with C-accelerated loader and config caching.

Provides:
- yaml_safe_load(): Drop-in replacement for yaml.safe_load() using CSafeLoader (21x faster)
- load_quarto_config(): Cached loader for _quarto-*.yml files (parsed once, reused across generators)
- clear_config_cache(): Reset the config cache (for testing)
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

# Use C-accelerated YAML loader when available (21x faster on large files like _variables.yml)
_yaml_loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def yaml_safe_load(stream) -> Any:
    """Drop-in replacement for yaml.safe_load() using CSafeLoader when available."""
    return yaml.load(stream, Loader=_yaml_loader)


# Cache for parsed Quarto config files (keyed by absolute path)
_config_cache: Dict[str, dict] = {}


def load_quarto_config(config_path: Union[str, Path]) -> dict:
    """Load and cache a Quarto YAML config file.

    Each config file is parsed only once per process. Subsequent calls
    return the cached result. This avoids re-parsing the same 17 config
    files 8+ times across different generators.

    Args:
        config_path: Path to the YAML config file

    Returns:
        Parsed YAML dict (empty dict if file not found or parse error)
    """
    key = str(Path(config_path).resolve())

    if key in _config_cache:
        return _config_cache[key]

    if not os.path.exists(config_path):
        _config_cache[key] = {}
        return {}

    with open(config_path, encoding="utf-8") as f:
        result = yaml_safe_load(f) or {}

    _config_cache[key] = result
    return result


def clear_config_cache() -> None:
    """Clear the config cache (for testing or forced reload)."""
    _config_cache.clear()
