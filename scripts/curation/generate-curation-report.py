#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Curation Report - Phase 4 of Book Curation Pipeline

Aggregates automated metrics (Phase 1) + LLM evaluation scores (Phase 2) +
cross-chapter analysis (Phase 3) into a final curation report.

Usage:
    python scripts/curation/generate-curation-report.py
    python scripts/curation/generate-curation-report.py --metrics-only

Output:
    _analysis/curation-report.json  - Machine-readable scores and classifications
    _analysis/curation-report.md    - Human-readable report with tables
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
METRICS_FILE = PROJECT_ROOT / "_analysis" / "curation-metrics.json"
EVALS_DIR = PROJECT_ROOT / "_analysis" / "curation-evaluations"
CROSS_CHAPTER_FILE = PROJECT_ROOT / "_analysis" / "curation-cross-chapter.json"
REPORT_JSON = PROJECT_ROOT / "_analysis" / "curation-report.json"
REPORT_MD = PROJECT_ROOT / "_analysis" / "curation-report.md"

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


def classify_chs(chs: float) -> str:
    """Classify CHS into GREEN/YELLOW/ORANGE/RED."""
    if chs >= 85:
        return "GREEN"
    elif chs >= 70:
        return "YELLOW"
    elif chs >= 50:
        return "ORANGE"
    else:
        return "RED"


def action_for_class(classification: str) -> str:
    """Default action based on classification."""
    return {
        "GREEN": "Keep as-is",
        "YELLOW": "Polish",
        "ORANGE": "Significant work needed",
        "RED": "Major decision (cut/merge/rewrite)",
    }.get(classification, "Review")


def compute_chs(scores: dict) -> float:
    """Compute weighted Chapter Health Score (0-100)."""
    total_weight = 0.0
    weighted_sum = 0.0

    for dim_key, dim_info in DIMENSIONS.items():
        score = scores.get(dim_key)
        if score is not None:
            weighted_sum += score * dim_info["weight"]
            total_weight += dim_info["weight"]

    if total_weight == 0:
        return 0.0

    # Scale 1-5 to 0-100
    raw = weighted_sum / total_weight
    return round((raw - 1) / 4 * 100, 1)


def load_metrics() -> dict:
    """Load Phase 1 automated metrics."""
    if not METRICS_FILE.exists():
        print(f"WARNING: {METRICS_FILE} not found. Run collect-chapter-metrics.py first.")
        return {"chapters": []}
    return json.loads(METRICS_FILE.read_text(encoding="utf-8"))


def load_evaluations() -> Dict[str, dict]:
    """Load Phase 2 per-chapter evaluation JSONs."""
    evals = {}
    if not EVALS_DIR.exists():
        return evals
    for f in EVALS_DIR.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        href = data.get("href", f.stem)
        evals[href] = data
    return evals


def load_cross_chapter() -> dict:
    """Load Phase 3 cross-chapter analysis."""
    if not CROSS_CHAPTER_FILE.exists():
        return {}
    return json.loads(CROSS_CHAPTER_FILE.read_text(encoding="utf-8"))


def merge_chapter_data(metrics: dict, evals: Dict[str, dict]) -> List[dict]:
    """Merge metrics and evaluation scores per chapter."""
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
            "intra_redundancy": ch_metrics.get("intra_redundancy", 0),
            # LLM evaluation scores (1-5)
            "scores": scores,
            "chs": chs,
            "classification": classification,
            "action": action_for_class(classification) if chs is not None else "Needs evaluation",
            # Per-dimension rationale
            "rationale": evaluation.get("rationale", {}),
            "recommendations": evaluation.get("recommendations", []),
        }
        chapters.append(merged)

    return chapters


def generate_priority_actions(chapters: List[dict], cross_chapter: dict) -> List[str]:
    """Generate top priority action items."""
    actions = []

    # From cross-chapter overlap analysis
    for overlap in cross_chapter.get("overlaps", []):
        if overlap.get("similarity", 0) > 0.3:
            actions.append(
                f"MERGE {overlap['chapter_a']} INTO {overlap['chapter_b']} "
                f"({int(overlap['similarity'] * 100)}% overlap)"
            )

    # From chapter classifications
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

    # Page efficiency outliers
    for ch in chapters:
        pages = ch.get("page_estimate", 0)
        d6 = ch.get("scores", {}).get("D6_page_efficiency")
        if pages > 15 and d6 is not None and d6 <= 2:
            actions.append(
                f"CONDENSE: {ch['href']} ({pages}p, D6={d6})"
            )

    return actions[:20]  # Top 20


def generate_markdown_report(chapters: List[dict], metrics: dict,
                              cross_chapter: dict, actions: List[str]) -> str:
    """Generate the human-readable Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_chapters = len(chapters)
    total_pages = metrics.get("total_pages", 0)

    evaluated = [c for c in chapters if c["chs"] is not None]
    avg_chs = (round(sum(c["chs"] for c in evaluated) / len(evaluated), 1)
               if evaluated else 0)

    # Classification counts
    class_counts = {"GREEN": 0, "YELLOW": 0, "ORANGE": 0, "RED": 0, "UNEVALUATED": 0}
    for ch in chapters:
        cls = ch.get("classification", "UNEVALUATED")
        class_counts[cls] = class_counts.get(cls, 0) + 1

    lines = []
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
    parts = {}
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

    # Metrics-only quick reference
    lines.append("## Automated Metrics Quick Reference")
    lines.append("")
    lines.append("| Chapter | Words | Pg | Cites | Vars | Hardcoded | BrokenLinks | Readability |")
    lines.append("|---------|-------|----|-------|------|-----------|-------------|-------------|")
    for ch in sorted(chapters, key=lambda c: c.get("chapter_index", 0)):
        name = Path(ch["href"]).stem
        if len(name) > 20:
            name = name[:17] + "..."
        lines.append(
            f"| {name} "
            f"| {ch.get('word_count', 0)} "
            f"| {ch.get('page_estimate', 0)} "
            f"| {ch.get('citation_count', 0)} "
            f"| {ch.get('var_count', 0)} "
            f"| {ch.get('hardcoded_count', 0)} "
            f"| {ch.get('broken_link_count', 0)} "
            f"| {ch.get('readability_grade', 0)} |"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate book curation report")
    parser.add_argument("--metrics-only", action="store_true",
                        help="Generate report from metrics only (skip LLM evaluations)")
    args = parser.parse_args()

    print("Loading data...")
    metrics = load_metrics()
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
