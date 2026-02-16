#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Curation Report - Consolidated Book Curation Pipeline

Collects per-chapter metrics (word count, readability, citations, etc.),
optionally loads LLM evaluations and cross-chapter analysis, and produces
a final curation report with enriched readability data.

Usage:
    python scripts/curation/generate-curation-report.py
    python scripts/curation/generate-curation-report.py --metrics-only
    python scripts/curation/generate-curation-report.py --chapter cost-of-war
    python scripts/curation/generate-curation-report.py --force
    python scripts/curation/generate-curation-report.py --chapter cost-of-war --force

Output:
    _analysis/curation-metrics.json  - Per-chapter metrics (cached)
    _analysis/curation-report.json   - Machine-readable scores and classifications
    _analysis/curation-report.md     - Human-readable report with tables
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
from lib.text_utils import normalize_text, jaccard_similarity, strip_qmd_markup

PROJECT_ROOT = Path(__file__).parent.parent.parent
QUARTO_CONFIG = PROJECT_ROOT / "_quarto-manual.yml"
METRICS_FILE = PROJECT_ROOT / "_analysis" / "curation-metrics.json"
EVALS_DIR = PROJECT_ROOT / "_analysis" / "curation-evaluations"
CROSS_CHAPTER_FILE = PROJECT_ROOT / "_analysis" / "curation-cross-chapter.json"
REPORT_JSON = PROJECT_ROOT / "_analysis" / "curation-report.json"
REPORT_MD = PROJECT_ROOT / "_analysis" / "curation-report.md"

HASH_FIELD = "lastCurationHash"
WORDS_PER_PAGE = 250

# Dimension weights for Chapter Health Score (CHS)
DIMENSIONS = {
    "D1_mission_necessity": {"label": "Mission Necessity", "weight": 0.20},
    "D2_uniqueness": {"label": "Uniqueness", "weight": 0.15},
    "D3_placement": {"label": "Placement", "weight": 0.05},
    "D4_writing_quality": {"label": "Writing Quality", "weight": 0.15},
    "D5_evidence_quality": {"label": "Evidence Quality", "weight": 0.15},
    "D6_page_efficiency": {"label": "Page Efficiency", "weight": 0.10},
    "D7_accessibility": {"label": "Accessibility", "weight": 0.10},
    "D8_policy_rigor": {"label": "Policy/Investor Rigor", "weight": 0.10},
}

# Chapters excluded from metrics (auto-generated content skews averages)
AUTO_GENERATED = [
    "parameters-and-calculations",
    "papers.qmd",
    "index.qmd",
    "right-to-trial-fda-upgrade-act.qmd",
]

# Passive voice detection patterns
PASSIVE_PATTERNS = [
    re.compile(r'\b(is|are|was|were|be|been|being)\s+\w+ed\b', re.IGNORECASE),
    re.compile(r'\b(is|are|was|were|be|been|being)\s+\w+en\b', re.IGNORECASE),
]

# Hedging language patterns
HEDGING_PATTERNS = [
    re.compile(r'\b(may|might|could|would|should|perhaps|possibly|probably|likely)\b', re.IGNORECASE),
    re.compile(r'\b(seems?|appears?|suggests?|indicates?)\s+to\b', re.IGNORECASE),
    re.compile(r'\b(somewhat|relatively|fairly|quite|rather|pretty)\b', re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Chapter list extraction from Quarto config
# ---------------------------------------------------------------------------

def extract_chapter_list(config: dict) -> List[dict]:
    """Extract ordered chapter list with part info from _quarto-manual.yml."""
    chapters = []
    book_chapters = config.get("book", {}).get("chapters", [])
    part_index = 0

    for entry in book_chapters:
        if isinstance(entry, str):
            chapters.append({
                "href": entry,
                "part_name": None,
                "part_index": 0,
                "chapter_index": len(chapters),
            })
        elif isinstance(entry, dict):
            if "href" in entry and "part" not in entry:
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
# Text utilities for metric collection
# ---------------------------------------------------------------------------

def get_prose_lines(content: str) -> List[str]:
    """Get non-code, non-frontmatter, non-comment prose lines."""
    # Strip YAML frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:].lstrip("\n")

    lines = content.split("\n")
    result = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        stripped = line.strip()
        if stripped.startswith("<!--") or stripped.startswith("#|"):
            continue
        if stripped.startswith(":::"):
            continue
        result.append(line)
    return result


def split_sentences(text: str) -> List[str]:
    """Split text into sentences (simple heuristic)."""
    sentences = re.split(r'[.!?]+\s+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]


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
    return len(re.findall(r'\{\{<\s*var\s+\w+\s*>\}\}', content))


def count_citations(content: str) -> int:
    matches = re.findall(r'(?<!\w)@([a-zA-Z][\w-]*)', content)
    return len([m for m in matches if not re.search(r'@\w+\.\w+', '@' + m)])


def count_hardcoded_values(prose_lines: List[str]) -> int:
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
            if not re.search(r'@\w+', line) and not re.search(r'\[\d+\]', line):
                count += 1
    return count


def count_long_sentences(prose_lines: List[str], threshold: int = 40) -> int:
    text = " ".join(prose_lines)
    sentences = re.split(r'[.!?]+', text)
    return sum(1 for s in sentences if len(s.split()) > threshold)


def compute_intra_redundancy(prose_lines: List[str]) -> float:
    paragraphs = []
    current: List[str] = []
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

    word_sets = [set(normalize_text(p).split()) for p in paragraphs]
    total_sim = 0.0
    comparisons = 0

    for i in range(len(word_sets)):
        for j in range(i + 1, len(word_sets)):
            sim = jaccard_similarity(word_sets[i], word_sets[j])
            if sim > 0.3:
                total_sim += sim
            comparisons += 1

    if comparisons == 0:
        return 0.0
    return round(total_sim / comparisons, 3)


def extract_title(content: str) -> str:
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[3:end]
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
            if m:
                return m.group(1).strip()
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def count_passive_voice(sentences: List[str]) -> int:
    count = 0
    for sentence in sentences:
        for pattern in PASSIVE_PATTERNS:
            if pattern.search(sentence):
                count += 1
                break
    return count


def count_hedging(text: str) -> int:
    count = 0
    for pattern in HEDGING_PATTERNS:
        count += len(pattern.findall(text))
    return count


# ---------------------------------------------------------------------------
# Main metrics collection (absorbed from collect-chapter-metrics.py)
# ---------------------------------------------------------------------------

def collect_metrics_for_chapter(file_path: Path, chapter_info: dict) -> dict:
    """Collect all metrics for a single chapter file, including rich readability."""
    content = file_path.read_text(encoding="utf-8")
    prose_lines = get_prose_lines(content)
    prose_text = " ".join(prose_lines)
    words = re.findall(r'\b\w+\b', prose_text)
    word_count = len(words)

    heading_count, max_depth = count_headings(prose_lines)
    citation_count = count_citations(content)
    var_count = count_variables(content)

    # Rich readability via strip_qmd_markup (cleaner prose extraction)
    clean_prose = strip_qmd_markup(content)
    sentences = split_sentences(clean_prose)

    fk_grade = 0.0
    flesch_ease = 0.0
    gunning_fog = 0.0
    dale_chall = 0.0
    avg_sentence_length = 0.0
    difficult_word_count = 0
    passive_count = 0
    hedge_count = 0

    if clean_prose.strip():
        fk_grade = round(max(textstat.flesch_kincaid_grade(clean_prose), 0.0), 1)
        flesch_ease = round(textstat.flesch_reading_ease(clean_prose), 1)
        gunning_fog = round(textstat.gunning_fog(clean_prose), 1)
        dale_chall = round(textstat.dale_chall_readability_score(clean_prose), 1)
        avg_sentence_length = round(textstat.words_per_sentence(clean_prose), 1)
        difficult_word_count = textstat.difficult_words(clean_prose)
        passive_count = count_passive_voice(sentences)
        hedge_count = count_hedging(clean_prose)

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
        "readability_grade": fk_grade,
        "flesch_reading_ease": flesch_ease,
        "gunning_fog": gunning_fog,
        "dale_chall": dale_chall,
        "avg_sentence_length": avg_sentence_length,
        "difficult_word_count": difficult_word_count,
        "passive_voice_count": passive_count,
        "hedging_count": hedge_count,
        "intra_redundancy": compute_intra_redundancy(prose_lines),
    }


def collect_all_metrics(chapter_filter: Optional[str], force: bool) -> dict:
    """Collect metrics for all active chapters (with hash-based caching)."""
    if not QUARTO_CONFIG.exists():
        print(f"ERROR: {QUARTO_CONFIG} not found")
        return {"chapters": []}

    print("Loading chapter list from _quarto-manual.yml...")
    config = _load_config(QUARTO_CONFIG)
    if config is None:
        print(f"ERROR: Could not parse {QUARTO_CONFIG}")
        return {"chapters": []}

    chapter_list = extract_chapter_list(config)
    print(f"Found {len(chapter_list)} active chapters")

    # Exclude auto-generated chapters
    excluded = [c for c in chapter_list if any(pat in c["href"] for pat in AUTO_GENERATED)]
    if excluded:
        chapter_list = [c for c in chapter_list if not any(pat in c["href"] for pat in AUTO_GENERATED)]
        for ex in excluded:
            print(f"  Excluded from metrics: {ex['href']}")
        print(f"  {len(chapter_list)} chapters after excluding auto-generated")

    # Filter by chapter name if specified
    if chapter_filter:
        chapter_list = [c for c in chapter_list if chapter_filter in c["href"]]
        print(f"Filtered to {len(chapter_list)} chapters matching '{chapter_filter}'")

    # Load existing metrics and hash store
    existing_metrics: Dict[str, dict] = {}
    if METRICS_FILE.exists():
        data = json.loads(METRICS_FILE.read_text(encoding="utf-8"))
        for ch in data.get("chapters", []):
            existing_metrics[ch["href"]] = ch

    hash_store = HashStore(PROJECT_ROOT)

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
        if not force and not hash_store.is_stale(rel_path, HASH_FIELD):
            if rel_path in existing_metrics or href in existing_metrics:
                key = rel_path if rel_path in existing_metrics else href
                results.append(existing_metrics[key])
                skipped += 1
                continue

        print(f"  Processing: {href}")
        metrics = collect_metrics_for_chapter(file_path, chapter_info)
        results.append(metrics)
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

    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    METRICS_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nMetrics: {processed} processed, {skipped} cached")
    print(f"Total: {len(results)} chapters, ~{total_pages} pages, avg grade {avg_readability}")
    print(f"Output: {METRICS_FILE}")

    return output


# ---------------------------------------------------------------------------
# CHS scoring and classification
# ---------------------------------------------------------------------------

def classify_chs(chs: float) -> str:
    if chs >= 85:
        return "GREEN"
    elif chs >= 70:
        return "YELLOW"
    elif chs >= 50:
        return "ORANGE"
    else:
        return "RED"


def action_for_class(classification: str) -> str:
    return {
        "GREEN": "Keep as-is",
        "YELLOW": "Polish",
        "ORANGE": "Significant work needed",
        "RED": "Major decision (cut/merge/rewrite)",
    }.get(classification, "Review")


def compute_chs(scores: dict) -> float:
    total_weight = 0.0
    weighted_sum = 0.0
    for dim_key, dim_info in DIMENSIONS.items():
        score = scores.get(dim_key)
        if score is not None:
            weighted_sum += score * dim_info["weight"]
            total_weight += dim_info["weight"]
    if total_weight == 0:
        return 0.0
    raw = weighted_sum / total_weight
    return round((raw - 1) / 4 * 100, 1)


# ---------------------------------------------------------------------------
# Data loading (LLM evaluations, cross-chapter)
# ---------------------------------------------------------------------------

def load_evaluations() -> Dict[str, dict]:
    evals = {}
    if not EVALS_DIR.exists():
        return evals
    for f in EVALS_DIR.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        href = data.get("href", f.stem)
        evals[href] = data
    return evals


def load_cross_chapter() -> dict:
    if not CROSS_CHAPTER_FILE.exists():
        return {}
    return json.loads(CROSS_CHAPTER_FILE.read_text(encoding="utf-8"))


def merge_chapter_data(metrics: dict, evals: Dict[str, dict]) -> List[dict]:
    chapters = []
    for ch_metrics in metrics.get("chapters", []):
        href = ch_metrics["href"]
        evaluation = evals.get(href, {})
        scores = evaluation.get("scores", {})

        chs = compute_chs(scores) if scores else None
        classification = classify_chs(chs) if chs is not None else "UNEVALUATED"

        merged = {
            "href": href,
            "title": ch_metrics.get("title", ""),
            "part_name": ch_metrics.get("part_name"),
            "part_index": ch_metrics.get("part_index", 0),
            "chapter_index": ch_metrics.get("chapter_index", 0),
            # Automated metrics
            "word_count": ch_metrics.get("word_count", 0),
            "page_estimate": ch_metrics.get("page_estimate", 0),
            "citation_count": ch_metrics.get("citation_count", 0),
            "citation_density": ch_metrics.get("citation_density", 0),
            "var_count": ch_metrics.get("var_count", 0),
            "hardcoded_count": ch_metrics.get("hardcoded_count", 0),
            "broken_link_count": ch_metrics.get("broken_link_count", 0),
            "missing_citation_count": ch_metrics.get("missing_citation_count", 0),
            "long_sentence_count": ch_metrics.get("long_sentence_count", 0),
            "readability_grade": ch_metrics.get("readability_grade", 0),
            "flesch_reading_ease": ch_metrics.get("flesch_reading_ease", 0),
            "gunning_fog": ch_metrics.get("gunning_fog", 0),
            "dale_chall": ch_metrics.get("dale_chall", 0),
            "avg_sentence_length": ch_metrics.get("avg_sentence_length", 0),
            "difficult_word_count": ch_metrics.get("difficult_word_count", 0),
            "passive_voice_count": ch_metrics.get("passive_voice_count", 0),
            "hedging_count": ch_metrics.get("hedging_count", 0),
            "intra_redundancy": ch_metrics.get("intra_redundancy", 0),
            # LLM evaluation scores (1-5)
            "scores": scores,
            "chs": chs,
            "classification": classification,
            "action": action_for_class(classification) if chs is not None else "Needs evaluation",
            "rationale": evaluation.get("rationale", {}),
            "recommendations": evaluation.get("recommendations", []),
        }
        chapters.append(merged)

    return chapters


# ---------------------------------------------------------------------------
# Priority actions
# ---------------------------------------------------------------------------

def generate_priority_actions(chapters: List[dict], cross_chapter: dict) -> List[str]:
    actions = []

    for overlap in cross_chapter.get("overlaps", []):
        if overlap.get("similarity", 0) > 0.3:
            actions.append(
                f"MERGE {overlap['chapter_a']} INTO {overlap['chapter_b']} "
                f"({int(overlap['similarity'] * 100)}% overlap)"
            )

    red_chapters = [c for c in chapters if c["classification"] == "RED"]
    for ch in sorted(red_chapters, key=lambda c: c.get("chs", 0)):
        actions.append(
            f"MAJOR: {ch['href']} (CHS={ch.get('chs', '?')}, "
            f"{ch.get('page_estimate', '?')}p) - {', '.join(ch.get('recommendations', ['Review']))[:80]}"
        )

    orange_chapters = [c for c in chapters if c["classification"] == "ORANGE"]
    for ch in sorted(orange_chapters, key=lambda c: c.get("chs", 0)):
        low_dims = []
        for dim_key in DIMENSIONS:
            score = ch.get("scores", {}).get(dim_key)
            if score is not None and score <= 2:
                low_dims.append(f"{dim_key.split('_', 1)[0]}={score}")
        dim_info = f" ({', '.join(low_dims)})" if low_dims else ""
        actions.append(
            f"REWORK: {ch['href']} (CHS={ch.get('chs', '?')}, "
            f"{ch.get('page_estimate', '?')}p){dim_info}"
        )

    for ch in chapters:
        pages = ch.get("page_estimate", 0)
        d6 = ch.get("scores", {}).get("D6_page_efficiency")
        if pages > 15 and d6 is not None and d6 <= 2:
            actions.append(f"CONDENSE: {ch['href']} ({pages}p, D6={d6})")

    return actions[:20]


# ---------------------------------------------------------------------------
# Markdown report generation
# ---------------------------------------------------------------------------

def generate_markdown_report(chapters: List[dict], metrics: dict,
                              cross_chapter: dict, actions: List[str]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_chapters = len(chapters)
    total_pages = metrics.get("total_pages", 0)

    evaluated = [c for c in chapters if c["chs"] is not None]
    avg_chs = (round(sum(c["chs"] for c in evaluated) / len(evaluated), 1)
               if evaluated else 0)

    class_counts = {"GREEN": 0, "YELLOW": 0, "ORANGE": 0, "RED": 0, "UNEVALUATED": 0}
    for ch in chapters:
        cls = ch.get("classification", "UNEVALUATED")
        class_counts[cls] = class_counts.get(cls, 0) + 1

    lines: List[str] = []
    lines.append("# Book Curation Report")
    lines.append("")
    lines.append(f"**Generated:** {now} | **{total_chapters} chapters, ~{total_pages} pages**"
                 f" | **Avg CHS: {avg_chs}/100**")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Class | Count | Action |")
    lines.append("|-------|-------|--------|")
    for cls in ["GREEN", "YELLOW", "ORANGE", "RED", "UNEVALUATED"]:
        count = class_counts[cls]
        if count > 0:
            lines.append(f"| {cls} | {count} | {action_for_class(cls)} |")
    lines.append("")

    # Priority actions
    if actions:
        lines.append("## Priority Actions")
        lines.append("")
        for i, action in enumerate(actions, 1):
            lines.append(f"{i}. {action}")
        lines.append("")

    # Per-part chapter tables
    parts: Dict[str, List[dict]] = {}
    for ch in chapters:
        part = ch.get("part_name") or "Introduction"
        if part not in parts:
            parts[part] = []
        parts[part].append(ch)

    dim_short = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
    dim_keys = list(DIMENSIONS.keys())

    for part_name, part_chapters in parts.items():
        lines.append(f"## {part_name}")
        lines.append("")
        lines.append("| Chapter | Pg | CHS | " + " | ".join(dim_short) + " | Action |")
        lines.append("|---------|----|----|" + "|".join(["----"] * 8) + "|--------|")

        for ch in sorted(part_chapters, key=lambda c: c.get("chapter_index", 0)):
            name = Path(ch["href"]).stem
            if len(name) > 25:
                name = name[:22] + "..."
            pg = ch.get("page_estimate", "?")
            chs = ch.get("chs")
            chs_str = str(int(chs)) if chs is not None else "-"

            dim_vals = []
            for dk in dim_keys:
                v = ch.get("scores", {}).get(dk)
                dim_vals.append(str(v) if v is not None else "-")

            action = ch.get("action", "-")
            if len(action) > 25:
                action = action[:22] + "..."

            lines.append(f"| {name} | {pg} | {chs_str} | "
                         + " | ".join(dim_vals) + f" | {action} |")

        lines.append("")

    # Cross-chapter overlap section
    overlaps = cross_chapter.get("overlaps", [])
    if overlaps:
        lines.append("## Cross-Chapter Overlaps")
        lines.append("")
        lines.append("| Chapter A | Chapter B | Similarity | Recommendation |")
        lines.append("|-----------|-----------|------------|----------------|")
        for ov in sorted(overlaps, key=lambda o: o.get("similarity", 0), reverse=True)[:15]:
            lines.append(
                f"| {Path(ov.get('chapter_a', '')).stem} "
                f"| {Path(ov.get('chapter_b', '')).stem} "
                f"| {int(ov.get('similarity', 0) * 100)}% "
                f"| {ov.get('recommendation', '-')} |"
            )
        lines.append("")

    # Narrative flow
    flow = cross_chapter.get("narrative_flow", {})
    if flow:
        lines.append("## Narrative Flow")
        lines.append("")
        for key in ["gaps", "redundancies", "strongest_sequences"]:
            items = flow.get(key, [])
            if items:
                lines.append(f"### {key.replace('_', ' ').title()}")
                for item in items:
                    lines.append(f"- {item}")
                lines.append("")

    # Page budget analysis
    budget = cross_chapter.get("page_budget", {})
    if budget:
        lines.append("## Page Budget Analysis")
        lines.append("")
        for key, value in budget.items():
            lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        lines.append("")

    # Readability Flags section
    flagged_grade = [c for c in chapters if c.get("readability_grade", 0) > 12]
    flagged_sentence = [c for c in chapters if c.get("avg_sentence_length", 0) > 20]
    flagged_passive = [c for c in chapters if c.get("passive_voice_count", 0) > 20]
    flagged_hedging = [c for c in chapters if c.get("hedging_count", 0) > 30]

    if flagged_grade or flagged_sentence or flagged_passive or flagged_hedging:
        lines.append("## Readability Flags")
        lines.append("")

        if flagged_grade:
            lines.append("### Grade Level > 12 (College+)")
            for ch in sorted(flagged_grade, key=lambda c: c.get("readability_grade", 0), reverse=True):
                lines.append(f"- **{Path(ch['href']).stem}**: grade {ch['readability_grade']}")
            lines.append("")

        if flagged_sentence:
            lines.append("### Avg Sentence Length > 20 Words")
            for ch in sorted(flagged_sentence, key=lambda c: c.get("avg_sentence_length", 0), reverse=True):
                lines.append(f"- **{Path(ch['href']).stem}**: {ch['avg_sentence_length']} words/sentence")
            lines.append("")

        if flagged_passive:
            lines.append("### High Passive Voice (> 20 instances)")
            for ch in sorted(flagged_passive, key=lambda c: c.get("passive_voice_count", 0), reverse=True):
                lines.append(f"- **{Path(ch['href']).stem}**: {ch['passive_voice_count']} passive constructions")
            lines.append("")

        if flagged_hedging:
            lines.append("### High Hedging Language (> 30 instances)")
            for ch in sorted(flagged_hedging, key=lambda c: c.get("hedging_count", 0), reverse=True):
                lines.append(f"- **{Path(ch['href']).stem}**: {ch['hedging_count']} hedging words")
            lines.append("")

    # Automated Metrics Quick Reference (enriched with readability)
    lines.append("## Automated Metrics Quick Reference")
    lines.append("")
    lines.append("| Chapter | Words | Pg | Grade | Flesch | Fog | AvgSent | Passive | Hedge | Cites | Vars | Hardcoded |")
    lines.append("|---------|-------|----|-------|--------|-----|---------|---------|-------|-------|------|-----------|")
    for ch in sorted(chapters, key=lambda c: c.get("chapter_index", 0)):
        name = Path(ch["href"]).stem
        if len(name) > 20:
            name = name[:17] + "..."
        lines.append(
            f"| {name} "
            f"| {ch.get('word_count', 0)} "
            f"| {ch.get('page_estimate', 0)} "
            f"| {ch.get('readability_grade', 0)} "
            f"| {ch.get('flesch_reading_ease', 0)} "
            f"| {ch.get('gunning_fog', 0)} "
            f"| {ch.get('avg_sentence_length', 0)} "
            f"| {ch.get('passive_voice_count', 0)} "
            f"| {ch.get('hedging_count', 0)} "
            f"| {ch.get('citation_count', 0)} "
            f"| {ch.get('var_count', 0)} "
            f"| {ch.get('hardcoded_count', 0)} |"
        )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Collect metrics and generate book curation report")
    parser.add_argument("--metrics-only", action="store_true",
                        help="Generate report from metrics only (skip LLM evaluations)")
    parser.add_argument("--chapter", help="Only process chapters matching this name")
    parser.add_argument("--force", action="store_true",
                        help="Ignore hash cache, reprocess all chapters")
    args = parser.parse_args()

    # Phase 1: Collect metrics (integrated)
    print("=== Phase 1: Collecting chapter metrics ===")
    metrics = collect_all_metrics(args.chapter, args.force)

    if not metrics.get("chapters"):
        print("No chapters found. Exiting.")
        return 1

    # Phase 2-3: Load LLM evaluations and cross-chapter data (if available)
    print("\n=== Phase 4: Generating report ===")
    evals = {} if args.metrics_only else load_evaluations()
    cross_chapter = {} if args.metrics_only else load_cross_chapter()

    print(f"  Metrics: {len(metrics.get('chapters', []))} chapters")
    print(f"  Evaluations: {len(evals)} chapters")
    print(f"  Cross-chapter: {'loaded' if cross_chapter else 'none'}")

    # Merge data
    chapters = merge_chapter_data(metrics, evals)

    # Generate actions
    actions = generate_priority_actions(chapters, cross_chapter)

    # Build JSON report
    report = {
        "generated": datetime.now().isoformat(),
        "total_chapters": len(chapters),
        "total_pages": metrics.get("total_pages", 0),
        "total_words": metrics.get("total_words", 0),
        "avg_readability": metrics.get("avg_readability_grade", 0),
        "classifications": {
            cls: len([c for c in chapters if c["classification"] == cls])
            for cls in ["GREEN", "YELLOW", "ORANGE", "RED", "UNEVALUATED"]
        },
        "priority_actions": actions,
        "chapters": chapters,
        "cross_chapter": cross_chapter,
    }

    # Write JSON
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  JSON: {REPORT_JSON}")

    # Write Markdown
    md = generate_markdown_report(chapters, metrics, cross_chapter, actions)
    REPORT_MD.write_text(md, encoding="utf-8")
    print(f"  Markdown: {REPORT_MD}")

    # Print summary
    evaluated = [c for c in chapters if c["chs"] is not None]
    if evaluated:
        avg_chs = round(sum(c["chs"] for c in evaluated) / len(evaluated), 1)
        print(f"\nAvg CHS: {avg_chs}/100 ({len(evaluated)} evaluated)")
    else:
        print("\nNo chapters evaluated yet. Run /curate-book to evaluate with LLM.")

    for cls in ["GREEN", "YELLOW", "ORANGE", "RED", "UNEVALUATED"]:
        count = report["classifications"][cls]
        if count:
            print(f"  {cls}: {count}")

    if actions:
        print(f"\nTop actions:")
        for a in actions[:5]:
            print(f"  - {a}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
