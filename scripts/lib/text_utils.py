"""
Shared text normalization and similarity utilities.

Used by redundancy-check.py and generate-curation-report.py.
"""

import re
from typing import Set


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, collapse whitespace, strip punctuation)."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()


def strip_qmd_markup(content: str) -> str:
    """Extract prose from QMD content by stripping all non-prose markup.

    Removes: YAML frontmatter, code blocks, LaTeX, citations, Quarto
    shortcodes, markdown formatting, tables, HTML comments, images.
    """
    # YAML front matter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # Code blocks (fenced)
    content = re.sub(r'```[\s\S]*?```', '', content)
    # Inline code
    content = re.sub(r'`[^`]+`', '', content)
    # LaTeX display equations ($$...$$)
    content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
    # Inline LaTeX ($...$)
    content = re.sub(r'\$[^$]+\$', '', content)
    # Citations [@author2020] and @author2020
    content = re.sub(r'\[@?[a-zA-Z0-9_-]+(?:;\s*@?[a-zA-Z0-9_-]+)*\]', '', content)
    # Quarto callout blocks
    content = re.sub(r':::\s*\{\.callout.*?\n:::', '', content, flags=re.DOTALL)
    # Quarto div fences
    content = re.sub(r'^:::.*$', '', content, flags=re.MULTILINE)
    # Quarto includes
    content = re.sub(r'\{\{<\s*include.*?>\}\}', '', content)
    # Quarto variables
    content = re.sub(r'\{\{<\s*var\s+[^>]+>\}\}', '', content)
    # HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Markdown images
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    # Markdown links (keep text)
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    # Markdown headers
    content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
    # Bold/italic markers (keep text)
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    # Tables
    content = re.sub(r'^\|.*\|$', '', content, flags=re.MULTILINE)
    # Cell options (#| ...)
    content = re.sub(r'^#\|.*$', '', content, flags=re.MULTILINE)
    # Collapse whitespace
    content = re.sub(r'\n\n+', '\n\n', content)
    content = re.sub(r'  +', ' ', content)
    return content.strip()


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0
