#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collect Chapter Metrics - Phase 1 of Book Curation Pipeline

Collects quantitative metrics per chapter (no LLM). Parses _quarto-manual.yml
for active chapters and measures word count, citations, variables, readability,
hardcoded values, broken links, and intra-file redundancy.

Usage:
    python scripts/curation/collect-chapter-metrics.py
    python scripts/curation/collect-chapter-metrics.py --chapter cost-of-war
    python scripts/curation/collect-chapter-metrics.py --force
    python scripts/curation/collect-chapter-metrics.py --changed-only

Output:
    _analysis/curation-metrics.json
"""

import io
import sys

if sys.platform == 'win32' and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import textstat

# Allow imports from scripts/lib/
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.quarto_config_utils import _load_config
from lib.hash_store import HashStore
from lib.text_utils import normalize_text, jaccard_similarity

PROJECT_ROOT = Path(__file__).parent.parent.parent
QUARTO_CONFIG = PROJECT_ROOT / "_quarto-manual.yml"
OUTPUT_FILE = PROJECT_ROOT / "_analysis" / "curation-metrics.json"

HASH_FIELD = "lastCurationHash"
WORDS_PER_PAGE = 250


# ---------------------------------------------------------------------------
# Chapter list extraction from Quarto config
# ---------------------------------------------------------------------------

def extract_chapter_list(config: dict) -> List[dict]:
    """Extract ordered chapter list with part info from _quarto-manual.yml config.

    Returns list of dicts: {href, part_name, part_index, chapter_index}
    """
    chapters = []
    book_chapters = config.get("book", {}).get("chapters", [])
    part_index = 0

    for entry in book_chapters:
        if isinstance(entry, str):
            # Top-level chapter (e.g. index.qmd)
            chapters.append({
                "href": entry,
                "part_name": None,
                "part_index": 0,
                "chapter_index": len(chapters),
            })
        elif isinstance(entry, dict):
            if "href" in entry and "part" not in entry:
                # Single chapter with text/href
                chapters.append({
                    "href": entry["href"],
                    "part_name": entry.get("text"),
                    "part_index": 0,
                    "chapter_index": len(chapters),
                })
            elif "part" in entry:
                part_index += 1
                part_name = entry["part"]
                for ch in entry.get("chapters", []):
                    href = ch if isinstance(ch, str) else ch.get("href", "")
                    if href and not href.startswith("http"):
                        chapters.append({
                            "href": href,
                            "part_name": part_name,
                            "part_index": part_index,
                            "chapter_index": len(chapters),
                        })

    return chapters


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

def strip_yaml_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from QMD content."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].lstrip("\n")
    return content


def strip_code_blocks(content: str) -> str:
    """Remove fenced code blocks."""
    return re.sub(r'```[\s\S]*?```', '', content)


def get_prose_lines(content: str) -> List[str]:
    """Get non-code, non-frontmatter, non-comment prose lines."""
    text = strip_yaml_frontmatter(content)
    lines = text.split("\n")
    result = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Skip HTML comments, cell options, shortcodes-only lines
        stripped = line.strip()
        if stripped.startswith("<!--") or stripped.startswith("#|"):
            continue
        if stripped.startswith(":::"):
            continue
        result.append(line)
    return result


# ---------------------------------------------------------------------------
# Per-chapter metric collectors
# ---------------------------------------------------------------------------

def count_headings(prose_lines: List[str]) -> Tuple[int, int]:
    """Returns (heading_count, max_depth)."""
    count = 0
    max_depth = 0
    for line in prose_lines:
        m = re.match(r'^(#{1,6})\s', line)
        if m:
            count += 1
            depth = len(m.group(1))
            max_depth = max(max_depth, depth)
    return count, max_depth


def count_variables(content: str) -> int:
    """Count {{< var ... >}} references."""
    return len(re.findall(r'\{\{<\s*var\s+\w+\s*>\}\}', content))


def count_citations(content: str) -> int:
    """Count @citation references (excluding emails and URLs)."""
    # Match @ followed by word chars, but exclude emails and URLs
    matches = re.findall(r'(?<!\w)@([a-zA-Z][\w-]*)', content)
    # Filter out things that look like email prefixes
    return len([m for m in matches if not re.search(r'@\w+\.\w+', '@' + m)])


def count_hardcoded_values(prose_lines: List[str]) -> int:
    """Count hardcoded dollar amounts and large numbers (not in variables)."""
    count = 0
    patterns = [
        r'\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|trillion|M|B|T))?',
        r'\b\d{1,3}(?:,\d{3})+\b',
    ]
    for line in prose_lines:
        if "{{< var" in line:
            continue
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                raw = match.replace(",", "").replace("$", "")
                try:
                    num = float(raw.split()[0]) if raw else 0
                    if num >= 100 or "$" in match:
                        count += 1
                except ValueError:
                    pass
    return count


def count_broken_links(content: str, file_path: Path) -> int:
    """Count internal .qmd links that don't resolve."""
    pattern = r'\[([^\]]*)\]\(([^)]*\.qmd(?:#[^)]*)?)\)'
    matches = re.findall(pattern, content)
    broken = 0
    for _, link_target in matches:
        file_part = link_target.split("#")[0]
        if file_part.startswith("http"):
            continue
        if file_part.startswith("/"):
            target = PROJECT_ROOT / file_part.lstrip("/")
        else:
            target = file_path.parent / file_part
        if not target.resolve().exists():
            broken += 1
    return broken


def count_missing_citations(prose_lines: List[str]) -> int:
    """Count lines with statistical claims lacking citations."""
    claim_patterns = [
        r'(?:studies?\s+(?:show|indicate|suggest|found|demonstrate))',
        r'(?:research\s+(?:shows?|indicates?|suggests?))',
        r'(?:according\s+to)',
        r'(?:data\s+(?:shows?|suggests?))',
    ]
    combined = "|".join(claim_patterns)
    count = 0
    for line in prose_lines:
        if re.search(combined, line, re.IGNORECASE):
            # Check if there's a citation on this line
            if not re.search(r'@\w+', line) and not re.search(r'\[\d+\]', line):
                count += 1
    return count


def count_long_sentences(prose_lines: List[str], threshold: int = 40) -> int:
    """Count sentences exceeding word threshold."""
    text = " ".join(prose_lines)
    sentences = re.split(r'[.!?]+', text)
    return sum(1 for s in sentences if len(s.split()) > threshold)


def compute_intra_redundancy(prose_lines: List[str]) -> float:
    """Compute intra-file redundancy score (0-1) via paragraph Jaccard similarity."""
    # Split into paragraphs (groups of non-empty lines separated by blank lines)
    paragraphs = []
    current = []
    for line in prose_lines:
        if line.strip():
            current.append(line)
        else:
            if current:
                para = " ".join(current)
                if len(para.split()) >= 10:
                    paragraphs.append(para)
                current = []
    if current:
        para = " ".join(current)
        if len(para.split()) >= 10:
            paragraphs.append(para)

    if len(paragraphs) < 2:
        return 0.0

    # Compute pairwise Jaccard similarity
    word_sets = [set(normalize_text(p).split()) for p in paragraphs]
    total_sim = 0.0
    comparisons = 0

    for i in range(len(word_sets)):
        for j in range(i + 1, len(word_sets)):
            sim = jaccard_similarity(word_sets[i], word_sets[j])
            if sim > 0.3:  # Only count meaningful overlap
                total_sim += sim
            comparisons += 1

    if comparisons == 0:
        return 0.0

    return round(total_sim / comparisons, 3)


def extract_title(content: str) -> str:
    """Extract chapter title from frontmatter or first heading."""
    # Check frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[3:end]
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
            if m:
                return m.group(1).strip()
    # Fall back to first heading
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


# ---------------------------------------------------------------------------
# Main metrics collection
# ---------------------------------------------------------------------------

def collect_metrics_for_chapter(file_path: Path, chapter_info: dict) -> dict:
    """Collect all metrics for a single chapter file."""
    content = file_path.read_text(encoding="utf-8")
    prose_lines = get_prose_lines(content)
    prose_text = " ".join(prose_lines)
    words = re.findall(r'\b\w+\b', prose_text)
    word_count = len(words)

    heading_count, max_depth = count_headings(prose_lines)
    citation_count = count_citations(content)
    var_count = count_variables(content)

    return {
        "href": chapter_info["href"],
        "file_path": str(file_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "title": extract_title(content),
        "part_name": chapter_info.get("part_name"),
        "part_index": chapter_info.get("part_index", 0),
        "chapter_index": chapter_info.get("chapter_index", 0),
        "word_count": word_count,
        "page_estimate": round(word_count / WORDS_PER_PAGE, 1),
        "heading_count": heading_count,
        "heading_max_depth": max_depth,
        "var_count": var_count,
        "citation_count": citation_count,
        "citation_density": round(citation_count / max(word_count / 1000, 0.1), 2),
        "hardcoded_count": count_hardcoded_values(prose_lines),
        "broken_link_count": count_broken_links(content, file_path),
        "missing_citation_count": count_missing_citations(prose_lines),
        "long_sentence_count": count_long_sentences(prose_lines),
        "readability_grade": round(max(textstat.flesch_kincaid_grade(prose_text), 0.0), 1) if prose_text.strip() else 0.0,
        "intra_redundancy": compute_intra_redundancy(prose_lines),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect chapter metrics for book curation")
    parser.add_argument("--chapter", help="Only process chapters matching this name")
    parser.add_argument("--force", action="store_true", help="Ignore hash cache, reprocess all")
    parser.add_argument("--changed-only", action="store_true", help="Only process changed files")
    args = parser.parse_args()

    if not QUARTO_CONFIG.exists():
        print(f"ERROR: {QUARTO_CONFIG} not found")
        return 1

    print("Loading chapter list from _quarto-manual.yml...")
    config = _load_config(QUARTO_CONFIG)
    if config is None:
        print(f"ERROR: Could not parse {QUARTO_CONFIG}")
        return 1
    chapter_list = extract_chapter_list(config)
    print(f"Found {len(chapter_list)} active chapters")

    # Filter by chapter name if specified
    if args.chapter:
        chapter_list = [c for c in chapter_list if args.chapter in c["href"]]
        print(f"Filtered to {len(chapter_list)} chapters matching '{args.chapter}'")

    # Load existing metrics and hash store
    existing_metrics = {}
    if OUTPUT_FILE.exists():
        data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        for ch in data.get("chapters", []):
            existing_metrics[ch["href"]] = ch

    hash_store = HashStore(PROJECT_ROOT)

    # Collect metrics
    results = []
    processed = 0
    skipped = 0

    for chapter_info in chapter_list:
        href = chapter_info["href"]
        file_path = PROJECT_ROOT / href

        if not file_path.exists():
            print(f"  SKIP (missing): {href}")
            continue

        rel_path = href.replace("\\", "/")

        # Check cache
        if not args.force and not hash_store.is_stale(rel_path, HASH_FIELD):
            if rel_path in existing_metrics or href in existing_metrics:
                key = rel_path if rel_path in existing_metrics else href
                results.append(existing_metrics[key])
                skipped += 1
                continue

        print(f"  Processing: {href}")
        metrics = collect_metrics_for_chapter(file_path, chapter_info)
        results.append(metrics)

        # Update hash
        hash_store.mark_processed(rel_path, HASH_FIELD)
        processed += 1

    # Compute summary stats
    total_words = sum(r["word_count"] for r in results)
    total_pages = round(total_words / WORDS_PER_PAGE, 1)
    avg_readability = (round(sum(r["readability_grade"] for r in results) / len(results), 1)
                       if results else 0)

    output = {
        "generated": datetime.now().isoformat(),
        "total_chapters": len(results),
        "total_words": total_words,
        "total_pages": total_pages,
        "avg_readability_grade": avg_readability,
        "chapters": results,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone: {processed} processed, {skipped} cached")
    print(f"Total: {len(results)} chapters, ~{total_pages} pages, avg grade {avg_readability}")
    print(f"Output: {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
