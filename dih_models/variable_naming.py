#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared Quarto variable naming conventions for dih_models.

These helpers centralize the generated variable suffixes used by
_variables.yml exports and the per-paper filtering/normalization logic.
"""

from __future__ import annotations


CITE_VARIABLE_SUFFIX = "_cite"
LATEX_VARIABLE_SUFFIX = "_latex"
SHORT_VARIABLE_SUFFIX = "_short"  # Legacy normalization support
LONG_VARIABLE_SUFFIX = "_long"  # Legacy normalization support
NOUNIT_VARIABLE_SUFFIX = "_nounit"

_CORE_GENERATED_VARIABLE_SUFFIXES = (
    CITE_VARIABLE_SUFFIX,
    LATEX_VARIABLE_SUFFIX,
    NOUNIT_VARIABLE_SUFFIX,
)

_LEGACY_GENERATED_VARIABLE_SUFFIXES = (
    SHORT_VARIABLE_SUFFIX,
    LONG_VARIABLE_SUFFIX,
)

_AUTO_INCLUDED_COMPANION_SUFFIXES = (
    CITE_VARIABLE_SUFFIX,
    LATEX_VARIABLE_SUFFIX,
)


def get_generated_variable_suffixes(include_legacy: bool = True) -> tuple[str, ...]:
    """
    Return suffixes used for generated Quarto variable variants.

    Args:
        include_legacy: If True, include legacy suffixes still recognized by
            the filtering/normalization pipeline.
    """
    if include_legacy:
        return _CORE_GENERATED_VARIABLE_SUFFIXES + _LEGACY_GENERATED_VARIABLE_SUFFIXES
    return _CORE_GENERATED_VARIABLE_SUFFIXES


def get_auto_included_companion_suffixes() -> tuple[str, ...]:
    """Return suffixes automatically exported alongside a base variable."""
    return _AUTO_INCLUDED_COMPANION_SUFFIXES


def strip_generated_variable_suffix(var_name: str, include_legacy: bool = True) -> str:
    """
    Strip a known generated-variable suffix from a Quarto variable name.

    Matching is case-insensitive so callers can pass either lowercase Quarto
    names or uppercase parameter-like names.
    """
    lower_name = var_name.lower()
    for suffix in get_generated_variable_suffixes(include_legacy=include_legacy):
        if lower_name.endswith(suffix):
            return var_name[:-len(suffix)]
    return var_name


def variable_name_to_parameter_name(var_name: str, include_legacy: bool = True) -> str:
    """Convert a Quarto variable name to its base uppercase parameter name."""
    return strip_generated_variable_suffix(var_name, include_legacy=include_legacy).upper()
