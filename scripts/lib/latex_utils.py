#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX Utilities
===============

Reusable utilities for sanitizing text for LaTeX compatibility.

Usage:
    from lib.latex_utils import sanitize_for_latex

    safe_caption = sanitize_for_latex("Cost is $250M (50% savings)")
    # Returns: "Cost is 250M (50 percent savings)"
"""

import re


def sanitize_for_latex(text: str) -> str:
    """
    Sanitize text for LaTeX compatibility.

    Replaces characters that break LaTeX rendering:
      - \\% or % -> " percent" (with smart spacing)
      - \\$ or $ -> removed (just the symbol, numbers remain)
      - & -> " and "
      - _ -> "-" (in subscript patterns)

    Args:
        text: Input text that may contain LaTeX-unsafe characters

    Returns:
        Sanitized text safe for LaTeX rendering
    """
    result = text

    # First normalize escaped versions
    result = result.replace('\\%', '%')
    result = result.replace('\\$', '$')
    result = result.replace('\\&', '&')
    result = result.replace('\\_', '_')

    # Replace % with " percent" (smart spacing)
    # Pattern: number followed by % (e.g., "3.5%" -> "3.5 percent")
    result = re.sub(r'(\d)%', r'\1 percent', result)
    # Any remaining % (shouldn't be common)
    result = result.replace('%', ' percent')
    # Clean up double spaces
    result = re.sub(r' +percent', ' percent', result)

    # Remove $ entirely (e.g., "$27.2B" -> "27.2B")
    # Pattern: $number - just remove the $
    result = re.sub(r'\$(\d)', r'\1', result)
    # Any remaining $ (shouldn't be common)
    result = result.replace('$', '')

    # Replace & with " and "
    result = re.sub(r'\s*&\s*', ' and ', result)

    # Replace _ in subscript-like patterns (e.g., "t_p" -> "t-p")
    # Only replace _ between alphanumeric characters
    result = re.sub(r'(\w)_(\w)', r'\1-\2', result)
    # Any remaining underscores
    result = result.replace('_', '-')

    # Clean up any double spaces created
    result = re.sub(r'  +', ' ', result)

    return result


def has_latex_unsafe_chars(text: str) -> bool:
    """
    Check if text contains any LaTeX-unsafe characters.

    Args:
        text: Text to check

    Returns:
        True if text contains characters that need sanitization
    """
    unsafe_chars = ['%', '$', '&', '_', '\\%', '\\$', '\\&', '\\_']
    return any(c in text for c in unsafe_chars)
