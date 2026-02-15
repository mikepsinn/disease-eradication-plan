"""
Shared text normalization and similarity utilities.

Used by redundancy-check.py and collect-chapter-metrics.py.
"""

import re
from typing import Set


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, collapse whitespace, strip punctuation)."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0
