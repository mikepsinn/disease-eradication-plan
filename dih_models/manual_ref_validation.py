"""Shared validation for Parameter.manual_ref targets."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


GENERATED_CALCULATIONS_PREFIX = "parameters-and-calculations"


@dataclass(frozen=True)
class ManualRefValidationResult:
    checked: int
    unique_refs: int


def normalize_manual_ref(manual_ref: str, description: str = "", value: float | None = None) -> str:
    """Normalize and cheaply validate a root-relative manual QMD path."""
    if not manual_ref:
        value_text = f" (value={value})" if value is not None else ""
        raise ValueError(
            f"Parameter missing required 'manual_ref': {description or 'unnamed'}{value_text}. "
            "Set manual_ref to a root-relative .qmd path listed in _quarto-manual.yml."
        )
    if not isinstance(manual_ref, str):
        raise TypeError(f"manual_ref must be a string: {manual_ref!r}")
    if "://" in manual_ref:
        raise ValueError(f"manual_ref must be a root-relative .qmd path, not a URL: {manual_ref}")

    normalized = manual_ref.replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]

    path = PurePosixPath(normalized)
    if path.is_absolute() or normalized.startswith("/") or ".." in path.parts:
        raise ValueError(f"manual_ref must stay inside the project root: {manual_ref}")
    if not normalized.endswith(".qmd"):
        raise ValueError(f"manual_ref must point to a .qmd file: {manual_ref}")
    if path.name.startswith(GENERATED_CALCULATIONS_PREFIX):
        raise ValueError(
            f"manual_ref must point to a human-facing manual chapter, not a generated calculations appendix: {manual_ref}"
        )
    return normalized


def collect_manual_qmd_refs(items: Any, refs: set[str] | None = None) -> set[str]:
    """Collect root-relative QMD paths from a Quarto book chapters tree."""
    collected = refs if refs is not None else set()
    for item in items or []:
        if isinstance(item, str):
            if item.endswith(".qmd"):
                collected.add(item)
            continue
        if not isinstance(item, dict):
            continue
        href = item.get("href")
        if isinstance(href, str) and href.endswith(".qmd"):
            collected.add(href)
        for key in ("chapters", "contents"):
            collect_manual_qmd_refs(item.get(key), collected)
    return collected


@lru_cache(maxsize=None)
def _load_manual_qmd_refs_cached(project_root: str) -> frozenset[str]:
    try:
        from .yaml_utils import load_quarto_config
    except ImportError:
        from yaml_utils import load_quarto_config

    root = Path(project_root)
    config_path = root / "_quarto-manual.yml"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing manual config for manual_ref validation: {config_path}")

    config = load_quarto_config(config_path)
    refs = collect_manual_qmd_refs((config.get("book") or {}).get("chapters", []))
    return frozenset(refs)


def load_manual_qmd_refs(project_root: Path) -> set[str]:
    """Load all QMD paths listed in _quarto-manual.yml."""
    return set(_load_manual_qmd_refs_cached(str(project_root.resolve())))


def get_parameter_manual_ref(parameters: Mapping[str, Any] | None, param_name: str) -> str | None:
    """Return a normalized manual_ref for a parameter metadata mapping."""
    if not parameters:
        return None
    meta = parameters.get(param_name)
    value_obj = meta.get("value") if isinstance(meta, dict) else meta
    manual_ref = getattr(value_obj, "manual_ref", None)
    if not manual_ref:
        return None
    description = getattr(value_obj, "description", "")
    numeric_value = float(value_obj) if isinstance(value_obj, (int, float)) else None
    return normalize_manual_ref(str(manual_ref), description, numeric_value)


def validate_manual_refs(parameters: Mapping[str, Any], project_root: Path) -> ManualRefValidationResult:
    """Validate every Parameter.manual_ref against disk and _quarto-manual.yml."""
    manual_qmd_refs = load_manual_qmd_refs(project_root)
    errors: list[str] = []
    checked = 0
    unique_refs: set[str] = set()

    for param_name in sorted(parameters):
        meta = parameters[param_name]
        value_obj = meta.get("value") if isinstance(meta, dict) else meta
        if not hasattr(value_obj, "manual_ref"):
            continue

        checked += 1
        try:
            manual_ref = get_parameter_manual_ref(parameters, param_name)
        except (TypeError, ValueError) as exc:
            errors.append(f"{param_name}: {exc}")
            continue

        if not manual_ref:
            errors.append(f"{param_name}: missing required manual_ref")
            continue

        unique_refs.add(manual_ref)
        if not (project_root / manual_ref).exists():
            errors.append(f"{param_name}: manual_ref points to a missing QMD file: {manual_ref}")
        if manual_ref not in manual_qmd_refs:
            errors.append(f"{param_name}: manual_ref must be listed in _quarto-manual.yml: {manual_ref}")

    if errors:
        shown = "\n".join(f"  - {error}" for error in errors[:25])
        if len(errors) > 25:
            shown += f"\n  ... and {len(errors) - 25} more"
        raise ValueError(f"Found {len(errors)} invalid manual_ref target(s):\n{shown}")

    return ManualRefValidationResult(checked=checked, unique_refs=len(unique_refs))
