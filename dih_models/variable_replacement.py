#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared variable replacement utilities for QMD files.

Provides functions to load Quarto variables from _variables.yml and replace
{{< var name >}} patterns in content.
"""
from __future__ import annotations

import re
from html import unescape
from pathlib import Path
from typing import Dict, List, Tuple

from dih_models.yaml_utils import yaml_safe_load


def strip_html_tags(text: str) -> str:
    """Remove HTML tags and extract just the display text."""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Unescape HTML entities
    clean = unescape(clean)
    return clean.strip()


def load_variables(variables_yml_path: Path) -> Dict[str, str]:
    """
    Load variables from YAML and strip HTML for plain text values.

    Args:
        variables_yml_path: Path to _variables.yml file

    Returns:
        Dict mapping variable names to their plain text values
    """
    variables = {}

    if not variables_yml_path.exists():
        return variables

    with open(variables_yml_path, 'r', encoding='utf-8') as f:
        data = yaml_safe_load(f)

    if data:
        for key, value in data.items():
            if isinstance(value, str):
                # Strip HTML to get plain text value
                plain_value = strip_html_tags(value)
                variables[key] = plain_value
            else:
                variables[key] = str(value)

    return variables


def replace_variables(
    content: str,
    variables: Dict[str, str],
    highlight_missing: bool = True
) -> str:
    """
    Replace {{< var name >}} with actual values.

    Args:
        content: Content string with Quarto variable references
        variables: Dict mapping variable names to values
        highlight_missing: If True, replace missing vars with [MISSING: name]

    Returns:
        Content with variables replaced
    """
    def replacer(match):
        var_name = match.group(1)
        if var_name in variables:
            return variables[var_name]
        elif highlight_missing:
            return f"[MISSING: {var_name}]"
        else:
            return match.group(0)  # Keep original

    # Pattern to match {{< var variable_name >}}
    pattern = re.compile(r'\{\{<\s*var\s+([a-zA-Z0-9_]+)\s*>\}\}')
    return pattern.sub(replacer, content)


def remove_quarto_includes(content: str) -> str:
    """
    Remove {{< include ... >}} directives from content.

    These are Quarto-specific and don't make sense in plain markdown.
    """
    # Remove include directives (entire line)
    pattern = re.compile(r'^.*\{\{<\s*include\s+[^>]+>\}\}.*$', re.MULTILINE)
    return pattern.sub('', content)


def remove_quarto_videos(content: str) -> str:
    """
    Remove {{< video ... >}} directives from content.
    """
    pattern = re.compile(r'\{\{<\s*video\s+[^>]+>\}\}', re.MULTILINE)
    return pattern.sub('', content)


def remove_quarto_callouts(content: str) -> str:
    """
    Convert Quarto callouts to standard markdown blockquotes.

    ::: {.callout-note}
    **Note**: Content here
    :::

    Becomes:
    > **Note**: Content here
    """
    # Simple approach: remove ::: lines, content stays
    lines = content.split('\n')
    result = []
    in_callout = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('::: {.callout'):
            in_callout = True
            continue
        elif stripped == ':::' and in_callout:
            in_callout = False
            continue
        elif in_callout:
            # Convert to blockquote
            result.append('> ' + line if line.strip() else '')
        else:
            result.append(line)

    return '\n'.join(result)


def remove_quarto_content_hidden(content: str) -> str:
    """
    Remove ::: {.content-hidden ...} blocks and their contents.

    These wrap content meant only for specific formats (epub, pdf, html)
    and should not appear in a plain markdown README.
    """
    lines = content.split('\n')
    result = []
    hidden_depth = 0

    for line in lines:
        stripped = line.strip()
        if re.match(r'^:::\s*\{\.content-hidden', stripped):
            hidden_depth += 1
            continue
        elif stripped == ':::' and hidden_depth > 0:
            hidden_depth -= 1
            continue
        elif hidden_depth > 0:
            continue
        else:
            result.append(line)

    return '\n'.join(result)


def remove_citation_keys(content: str) -> str:
    """
    Remove [@citation-key] references from content.

    Handles single keys [@foo], multiple keys [@foo; @bar],
    and keys with surrounding semicolons/spaces.
    """
    # Remove standalone citation brackets: [@key] or [@key; @key2]
    content = re.sub(r'\s*\[(?:@[\w-]+(?:\s*;\s*@[\w-]+)*)\]', '', content)
    return content


def clean_for_readme(content: str) -> str:
    """
    Clean Quarto-specific syntax for plain markdown README.

    Removes includes, videos, content-hidden blocks, citations,
    and converts callouts to blockquotes.
    """
    content = remove_quarto_includes(content)
    content = remove_quarto_videos(content)
    content = remove_quarto_content_hidden(content)
    content = remove_quarto_callouts(content)
    content = remove_citation_keys(content)

    # Remove empty lines that result from removed content (max 2 consecutive)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content
