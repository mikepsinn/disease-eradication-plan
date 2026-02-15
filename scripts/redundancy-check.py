#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redundancy Check Script
Analyzes QMD files for duplicated content at multiple levels:
1. Duplicate _latex variables (equation blocks)
2. Duplicate/similar sentences
3. Similar paragraphs (by word overlap)
4. Repeated phrases (n-grams)

Usage:
    python scripts/redundancy-check.py <file.qmd>
    python scripts/redundancy-check.py knowledge/economics/1-pct-treaty-impact.qmd --verbose
    python scripts/redundancy-check.py knowledge/economics/1-pct-treaty-impact.qmd --output redundancy-report.md

Features:
- Detects duplicate _latex variables and calculates their "redundancy cost"
- Finds duplicate/near-duplicate sentences across the document
- Identifies similar paragraphs using Jaccard word overlap
- Detects repeated n-gram phrases (5+ word sequences appearing multiple times)
- Shows section context for each finding
- Calculates total redundancy metrics
"""

import sys
import re
import os
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import Counter, defaultdict

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

# Allow imports from scripts/lib/
sys.path.insert(0, str(Path(__file__).parent))
from lib.text_utils import normalize_text, jaccard_similarity


@dataclass
class LatexOccurrence:
    """Represents a single occurrence of a _latex variable."""
    line_number: int
    section_header: str
    is_collapsible: bool
    context_before: str  # 2 lines before
    context_after: str   # 2 lines after
    in_callout: bool = False
    callout_type: str = ""


@dataclass
class LatexVariableInfo:
    """Information about a _latex variable and all its occurrences."""
    var_name: str
    occurrences: List[LatexOccurrence] = field(default_factory=list)
    expanded_line_count: int = 0  # How many lines this expands to in _variables.yml

    @property
    def redundancy_cost(self) -> int:
        """Total extra lines from duplication (occurrences - 1) * line_count."""
        if len(self.occurrences) <= 1:
            return 0
        return (len(self.occurrences) - 1) * self.expanded_line_count

    @property
    def is_duplicate(self) -> bool:
        return len(self.occurrences) > 1


@dataclass
class SentenceDuplicate:
    """Represents a duplicated sentence."""
    sentence: str
    line_numbers: List[int]
    sections: List[str]
    word_count: int

    @property
    def redundancy_cost(self) -> int:
        return (len(self.line_numbers) - 1) * self.word_count


@dataclass
class SimilarParagraphPair:
    """Represents two paragraphs that are similar."""
    para1_line: int
    para2_line: int
    para1_section: str
    para2_section: str
    para1_preview: str
    para2_preview: str
    similarity: float  # 0.0 to 1.0
    shared_words: int


@dataclass
class RepeatedPhrase:
    """A phrase (n-gram) that appears multiple times."""
    phrase: str
    occurrences: int
    line_numbers: List[int]
    word_count: int


def get_words(text: str) -> List[str]:
    """Extract words from text."""
    return normalize_text(text).split()


def extract_sentences(content: str) -> List[Tuple[str, int]]:
    """Extract sentences with their approximate line numbers."""
    lines = content.split('\n')
    sentences = []

    for line_num, line in enumerate(lines, 1):
        # Skip code blocks, YAML frontmatter, includes, etc.
        if line.strip().startswith(('```', '---', '{{<', '|', '$$', '#')):
            continue
        if re.match(r'^\s*[-*]\s*\*\*', line):  # Skip list item headers
            continue

        # Split line into sentences
        # Simple sentence boundary detection
        line_sentences = re.split(r'(?<=[.!?])\s+', line)
        for sent in line_sentences:
            sent = sent.strip()
            # Only consider substantial sentences
            if len(sent) > 50 and not sent.startswith(('{{<', '[')):
                sentences.append((sent, line_num))

    return sentences


def extract_paragraphs(content: str) -> List[Tuple[str, int, str]]:
    """Extract paragraphs with line numbers and section headers."""
    lines = content.split('\n')
    paragraphs = []
    current_para = []
    para_start_line = 1
    current_section = "(Top of document)"
    in_code_block = False
    in_yaml = False

    for line_num, line in enumerate(lines, 1):
        # Track YAML frontmatter
        if line.strip() == '---':
            in_yaml = not in_yaml
            continue
        if in_yaml:
            continue

        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Track section headers
        if line.startswith('#'):
            current_section = line.lstrip('#').strip()
            continue

        # Skip includes, LaTeX blocks, etc.
        if line.strip().startswith(('{{<', '$$', ':::', '|')):
            continue

        # Empty line ends paragraph
        if not line.strip():
            if current_para:
                para_text = ' '.join(current_para)
                if len(para_text) > 100:  # Only substantial paragraphs
                    paragraphs.append((para_text, para_start_line, current_section))
                current_para = []
            para_start_line = line_num + 1
        else:
            if not current_para:
                para_start_line = line_num
            current_para.append(line.strip())

    # Don't forget last paragraph
    if current_para:
        para_text = ' '.join(current_para)
        if len(para_text) > 100:
            paragraphs.append((para_text, para_start_line, current_section))

    return paragraphs


def find_duplicate_sentences(sentences: List[Tuple[str, int]], lines: List[str]) -> List[SentenceDuplicate]:
    """Find sentences that appear multiple times."""
    # Normalize sentences for comparison
    normalized_to_originals: Dict[str, List[Tuple[str, int]]] = defaultdict(list)

    for sent, line_num in sentences:
        normalized = normalize_text(sent)
        # Only compare sentences with 10+ words
        if len(normalized.split()) >= 10:
            normalized_to_originals[normalized].append((sent, line_num))

    duplicates = []
    for normalized, occurrences in normalized_to_originals.items():
        if len(occurrences) >= 2:
            line_numbers = [o[1] for o in occurrences]
            sections = [get_section_header(lines, ln - 1) for ln in line_numbers]
            duplicates.append(SentenceDuplicate(
                sentence=occurrences[0][0][:200] + "..." if len(occurrences[0][0]) > 200 else occurrences[0][0],
                line_numbers=line_numbers,
                sections=sections,
                word_count=len(normalized.split())
            ))

    duplicates.sort(key=lambda x: x.redundancy_cost, reverse=True)
    return duplicates


def find_similar_paragraphs(paragraphs: List[Tuple[str, int, str]], threshold: float = 0.5) -> List[SimilarParagraphPair]:
    """Find paragraph pairs with high similarity (Jaccard > threshold)."""
    similar_pairs = []

    for i in range(len(paragraphs)):
        para1_text, para1_line, para1_section = paragraphs[i]
        para1_words = set(get_words(para1_text))

        for j in range(i + 1, len(paragraphs)):
            para2_text, para2_line, para2_section = paragraphs[j]
            para2_words = set(get_words(para2_text))

            similarity = jaccard_similarity(para1_words, para2_words)

            if similarity >= threshold:
                shared = para1_words & para2_words
                similar_pairs.append(SimilarParagraphPair(
                    para1_line=para1_line,
                    para2_line=para2_line,
                    para1_section=para1_section,
                    para2_section=para2_section,
                    para1_preview=para1_text[:150] + "...",
                    para2_preview=para2_text[:150] + "...",
                    similarity=similarity,
                    shared_words=len(shared)
                ))

    similar_pairs.sort(key=lambda x: x.similarity, reverse=True)
    return similar_pairs[:20]  # Limit to top 20


def find_repeated_phrases(content: str, n: int = 5, min_occurrences: int = 3) -> List[RepeatedPhrase]:
    """Find n-word phrases that appear multiple times."""
    lines = content.split('\n')
    phrase_locations: Dict[str, List[int]] = defaultdict(list)

    for line_num, line in enumerate(lines, 1):
        # Skip special lines
        if line.strip().startswith(('```', '---', '{{<', '$$', '#', '|', ':::')):
            continue

        words = get_words(line)
        # Generate n-grams
        for i in range(len(words) - n + 1):
            phrase = ' '.join(words[i:i + n])
            # Skip phrases that are mostly numbers or short words
            if len(phrase) > 20:  # Minimum phrase length
                phrase_locations[phrase].append(line_num)

    # Filter to repeated phrases
    repeated = []
    for phrase, line_nums in phrase_locations.items():
        if len(set(line_nums)) >= min_occurrences:  # Use set to count unique lines
            repeated.append(RepeatedPhrase(
                phrase=phrase,
                occurrences=len(set(line_nums)),
                line_numbers=sorted(set(line_nums)),
                word_count=n
            ))

    repeated.sort(key=lambda x: x.occurrences * x.word_count, reverse=True)
    return repeated[:30]  # Top 30


@dataclass
class HeadingInfo:
    """Information about a section heading."""
    level: int
    text: str
    line_number: int
    normalized: str  # For similarity comparison


@dataclass
class OutlineAnalysis:
    """Analysis of document outline for redundancy clues."""
    headings: List[HeadingInfo]
    similar_headings: List[Tuple[HeadingInfo, HeadingInfo, float]]  # pairs with similarity
    summary_pattern_headings: List[HeadingInfo]  # headings suggesting recap
    derivation_clusters: Dict[str, List[HeadingInfo]]  # metric -> multiple derivation sections


# Keywords that suggest a section is summarizing/recapping
SUMMARY_KEYWORDS = [
    'summary', 'conclusion', 'key findings', 'key results', 'overview',
    'recap', 'in brief', 'takeaway', 'bottom line', 'highlights',
    'at a glance', 'quick reference', 'tl;dr', 'executive summary'
]

# Keywords suggesting derivation/calculation sections
DERIVATION_KEYWORDS = [
    'derivation', 'calculation', 'formula', 'how .* calculated',
    'methodology', 'computing', 'deriving'
]


def extract_outline(content: str) -> List[HeadingInfo]:
    """Extract all headings from the document."""
    lines = content.split('\n')
    headings = []

    for line_num, line in enumerate(lines, 1):
        if line.startswith('#'):
            # Count heading level
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break

            text = line[level:].strip()
            # Skip empty headings or special markers
            if not text or text.startswith('{'):
                continue

            normalized = normalize_text(text)
            headings.append(HeadingInfo(
                level=level,
                text=text,
                line_number=line_num,
                normalized=normalized
            ))

    return headings


def analyze_outline(headings: List[HeadingInfo]) -> OutlineAnalysis:
    """Analyze outline for redundancy patterns."""

    # 1. Find similar headings (might be covering same content)
    similar_headings = []
    for i in range(len(headings)):
        for j in range(i + 1, len(headings)):
            h1, h2 = headings[i], headings[j]
            # Calculate word overlap
            words1 = set(h1.normalized.split())
            words2 = set(h2.normalized.split())
            if words1 and words2:
                similarity = jaccard_similarity(words1, words2)
                if similarity >= 0.4:  # 40%+ word overlap
                    similar_headings.append((h1, h2, similarity))

    similar_headings.sort(key=lambda x: x[2], reverse=True)

    # 2. Find summary/recap headings
    summary_headings = []
    for h in headings:
        for keyword in SUMMARY_KEYWORDS:
            if keyword in h.normalized:
                summary_headings.append(h)
                break

    # 3. Find derivation clusters (same metric explained multiple times)
    derivation_headings = []
    for h in headings:
        for keyword in DERIVATION_KEYWORDS:
            if re.search(keyword, h.normalized):
                derivation_headings.append(h)
                break

    # Cluster derivations by what they're deriving
    derivation_clusters: Dict[str, List[HeadingInfo]] = defaultdict(list)
    for h in derivation_headings:
        # Try to extract what's being derived
        # Look for patterns like "ROI Derivation" or "Derivation of Cost per DALY"
        text = h.normalized
        # Remove derivation keywords to find the metric
        for kw in ['derivation', 'calculation', 'formula', 'methodology', 'computing', 'deriving']:
            text = text.replace(kw, '')
        text = text.strip()
        if text:
            # Use first significant word(s) as key
            key_words = [w for w in text.split() if len(w) > 3][:3]
            if key_words:
                key = ' '.join(key_words)
                derivation_clusters[key].append(h)

    # Filter to only clusters with 2+ entries
    derivation_clusters = {k: v for k, v in derivation_clusters.items() if len(v) >= 2}

    return OutlineAnalysis(
        headings=headings,
        similar_headings=similar_headings[:10],  # Top 10
        summary_pattern_headings=summary_headings,
        derivation_clusters=derivation_clusters
    )


def load_variables_yml() -> Dict[str, str]:
    """Load _variables.yml and return variable name -> value mapping."""
    variables = {}
    variables_path = Path("_variables.yml")

    if not variables_path.exists():
        print("Warning: _variables.yml not found, cannot calculate expanded sizes")
        return variables

    with open(variables_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The format is: "variable_name": "value" or "variable_name": "multi\n  line"
    # Find all variable definitions - handle both quoted and unquoted keys
    # Pattern: "var_name": "value" (possibly multi-line with continuation)

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        # Match quoted key: "variable_name": "value..." or "variable_name": "value\
        match = re.match(r'^"([a-z_]+)":\s*"(.*)$', line)
        if match:
            var_name = match.group(1)
            value_start = match.group(2)

            # Check if this is a multi-line value (ends with \ or doesn't end with ")
            if value_start.endswith('\\'):
                # Multi-line continuation
                value_parts = [value_start[:-1]]  # Remove trailing \
                i += 1
                while i < len(lines):
                    cont_line = lines[i]
                    # Continuation lines start with spaces and contain the value
                    if cont_line.startswith('  '):
                        cont_content = cont_line.strip()
                        if cont_content.endswith('\\'):
                            value_parts.append(cont_content[:-1])
                        elif cont_content.endswith('"'):
                            value_parts.append(cont_content[:-1])
                            break
                        else:
                            value_parts.append(cont_content)
                    else:
                        break
                    i += 1
                variables[var_name] = '\n'.join(value_parts)
            elif value_start.endswith('"'):
                # Single-line value
                variables[var_name] = value_start[:-1]
            else:
                # Value continues but without \
                variables[var_name] = value_start

        # Also try unquoted keys: variable_name: "value"
        elif re.match(r'^[a-z_]+:', line):
            match = re.match(r'^([a-z_]+):\s*"?(.*)$', line)
            if match:
                var_name = match.group(1)
                value = match.group(2)
                if value.endswith('"'):
                    value = value[:-1]
                variables[var_name] = value

        i += 1

    return variables


def get_section_header(lines: List[str], line_index: int) -> str:
    """Find the most recent section header above the given line."""
    for i in range(line_index - 1, -1, -1):
        line = lines[i].strip()
        if line.startswith('#'):
            # Clean up the header
            return line.lstrip('#').strip()
    return "(Top of document)"


def is_in_collapsible(lines: List[str], line_index: int) -> Tuple[bool, str]:
    """Check if line is within a collapsible callout section."""
    # Look backwards for callout opening
    in_callout = False
    callout_type = ""
    brace_depth = 0

    for i in range(line_index - 1, -1, -1):
        line = lines[i].strip()

        # Track ::: blocks
        if line.startswith(':::') and not line.startswith('::: {'):
            brace_depth -= 1
        elif line.startswith('::: {'):
            brace_depth += 1
            # Check if it's a collapsible callout
            if 'collapse=' in line or 'collapse="true"' in line.lower():
                in_callout = True
                # Extract callout type
                match = re.search(r'\.callout-(\w+)', line)
                if match:
                    callout_type = match.group(1)
                match = re.search(r'title="([^"]+)"', line)
                if match:
                    callout_type = match.group(1)
                break
            elif '.callout' in line:
                in_callout = True
                match = re.search(r'\.callout-(\w+)', line)
                if match:
                    callout_type = match.group(1)
                break

    return in_callout, callout_type


def analyze_file(filepath: str, variables: Dict[str, str]) -> List[LatexVariableInfo]:
    """Analyze a QMD file for _latex variable occurrences."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Pattern for _latex variables
    latex_pattern = re.compile(r'\{\{<\s*var\s+([a-z_]+_latex)\s*>\}\}')

    # Track all occurrences
    var_info: Dict[str, LatexVariableInfo] = {}

    for line_index, line in enumerate(lines):
        matches = latex_pattern.finditer(line)
        for match in matches:
            var_name = match.group(1)

            if var_name not in var_info:
                # Calculate expanded size
                expanded_size = 0
                if var_name in variables:
                    expanded_size = len(variables[var_name].split('\n'))

                var_info[var_name] = LatexVariableInfo(
                    var_name=var_name,
                    expanded_line_count=expanded_size
                )

            # Get context
            section = get_section_header(lines, line_index)
            is_collapse, callout_type = is_in_collapsible(lines, line_index)

            # Get surrounding context (2 lines before/after)
            context_before = '\n'.join(lines[max(0, line_index-2):line_index])
            context_after = '\n'.join(lines[line_index+1:min(len(lines), line_index+3)])

            occurrence = LatexOccurrence(
                line_number=line_index + 1,
                section_header=section,
                is_collapsible=is_collapse,
                context_before=context_before,
                context_after=context_after,
                in_callout=is_collapse,
                callout_type=callout_type
            )

            var_info[var_name].occurrences.append(occurrence)

    # Filter to only duplicates and sort by redundancy cost
    duplicates = [v for v in var_info.values() if v.is_duplicate]
    duplicates.sort(key=lambda x: x.redundancy_cost, reverse=True)

    return duplicates


def generate_report(
    duplicates: List[LatexVariableInfo],
    filepath: str,
    verbose: bool = False,
    sentence_dups: Optional[List[SentenceDuplicate]] = None,
    similar_paras: Optional[List[SimilarParagraphPair]] = None,
    repeated_phrases: Optional[List[RepeatedPhrase]] = None,
    outline: Optional[OutlineAnalysis] = None
) -> str:
    """Generate a markdown report of redundancy findings."""

    sentence_dups = sentence_dups or []
    similar_paras = similar_paras or []
    repeated_phrases = repeated_phrases or []

    total_redundant_lines = sum(d.redundancy_cost for d in duplicates)
    sentence_redundancy = sum(d.redundancy_cost for d in sentence_dups)

    # Count outline issues
    outline_issues = 0
    if outline:
        outline_issues = (
            len(outline.similar_headings) +
            len(outline.summary_pattern_headings) +
            len(outline.derivation_clusters)
        )

    report = []
    report.append(f"# Redundancy Report: {filepath}")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    report.append("| Category | Count | Redundancy Score |")
    report.append("|----------|-------|------------------|")
    report.append(f"| Duplicate _latex variables | {len(duplicates)} | {total_redundant_lines} lines |")
    report.append(f"| Duplicate sentences | {len(sentence_dups)} | {sentence_redundancy} words |")
    report.append(f"| Similar paragraphs (>50% overlap) | {len(similar_paras)} | Review needed |")
    report.append(f"| Repeated phrases (5+ words, 3+ times) | {len(repeated_phrases)} | Review needed |")
    report.append(f"| **Outline red flags** | {outline_issues} | **Manual review** |")
    report.append("")

    # --- OUTLINE ANALYSIS (at the top for manual review) ---
    if outline:
        report.append("## Document Outline Analysis")
        report.append("")
        report.append("Review these structural patterns that may indicate redundancy:")
        report.append("")

        # Full outline with indentation
        report.append("### Full Outline")
        report.append("")
        report.append("```")
        for h in outline.headings:
            indent = "  " * (h.level - 1)
            report.append(f"{indent}L{h.line_number}: {h.text}")
        report.append("```")
        report.append("")

        # Summary/recap headings
        if outline.summary_pattern_headings:
            report.append("### Summary/Recap Sections (potential overlap)")
            report.append("")
            report.append("These headings suggest summary content - check if they repeat each other:")
            report.append("")
            for h in outline.summary_pattern_headings:
                report.append(f"- **L{h.line_number}**: {h.text}")
            report.append("")
            report.append("**Action**: Compare these sections. Do they make the same points? Consider consolidating into ONE summary.")
            report.append("")

        # Similar headings
        if outline.similar_headings:
            report.append("### Similar Heading Pairs")
            report.append("")
            report.append("These heading pairs share >40% of their words - may cover similar content:")
            report.append("")
            for h1, h2, sim in outline.similar_headings:
                report.append(f"- **{sim:.0%} similar**:")
                report.append(f"  - L{h1.line_number}: \"{h1.text}\"")
                report.append(f"  - L{h2.line_number}: \"{h2.text}\"")
            report.append("")

        # Derivation clusters
        if outline.derivation_clusters:
            report.append("### Multiple Derivation Sections for Same Metric")
            report.append("")
            report.append("These metrics have multiple derivation/calculation sections:")
            report.append("")
            for metric, headings in outline.derivation_clusters.items():
                report.append(f"**\"{metric}\"** appears in {len(headings)} sections:")
                for h in headings:
                    report.append(f"  - L{h.line_number}: {h.text}")
            report.append("")
            report.append("**Action**: Consolidate derivations into ONE location. Link from other sections.")
            report.append("")

        report.append("---")
        report.append("")

    has_issues = duplicates or sentence_dups or similar_paras or repeated_phrases
    if not has_issues and not outline_issues:
        report.append("**No significant redundancy detected.**")
        return '\n'.join(report)

    report.append("## Duplicates by Redundancy Cost")
    report.append("")
    report.append("| Variable | Occurrences | Lines Each | Redundant Lines | Locations |")
    report.append("|----------|-------------|------------|-----------------|-----------|")

    for var in duplicates:
        locations = ', '.join([f"L{o.line_number}" for o in var.occurrences])
        report.append(f"| `{var.var_name}` | {len(var.occurrences)} | {var.expanded_line_count} | **{var.redundancy_cost}** | {locations} |")

    report.append("")
    report.append("## Detailed Analysis")
    report.append("")

    for var in duplicates:
        report.append(f"### `{var.var_name}`")
        report.append("")
        report.append(f"- **Occurrences**: {len(var.occurrences)}")
        report.append(f"- **Expanded size**: {var.expanded_line_count} lines")
        report.append(f"- **Redundancy cost**: {var.redundancy_cost} lines")
        report.append("")

        # Analyze which to keep
        collapsible_occurrences = [o for o in var.occurrences if o.is_collapsible]
        main_content_occurrences = [o for o in var.occurrences if not o.is_collapsible]

        report.append("**Occurrences:**")
        report.append("")

        for i, occ in enumerate(var.occurrences, 1):
            location_type = "COLLAPSIBLE" if occ.is_collapsible else "MAIN CONTENT"
            if occ.callout_type:
                location_type += f" ({occ.callout_type})"

            report.append(f"{i}. **Line {occ.line_number}** [{location_type}]")
            report.append(f"   - Section: *{occ.section_header}*")

            if verbose:
                report.append(f"   - Context before:")
                for ctx_line in occ.context_before.split('\n')[-2:]:
                    if ctx_line.strip():
                        report.append(f"     > {ctx_line[:80]}...")
                report.append(f"   - Context after:")
                for ctx_line in occ.context_after.split('\n')[:2]:
                    if ctx_line.strip():
                        report.append(f"     > {ctx_line[:80]}...")
            report.append("")

        # Recommendation
        report.append("**Recommendation:**")
        if len(collapsible_occurrences) >= 1 and len(main_content_occurrences) >= 1:
            report.append(f"- KEEP: Line {main_content_occurrences[0].line_number} (main content, section: {main_content_occurrences[0].section_header})")
            report.append(f"- REMOVE: Collapsible section occurrence(s) at lines {', '.join(str(o.line_number) for o in collapsible_occurrences)}")
            report.append(f"- Consider removing additional main content occurrences if they don't add context")
        elif len(var.occurrences) > 1:
            report.append(f"- KEEP: Line {var.occurrences[0].line_number} (first occurrence)")
            report.append(f"- REVIEW: Lines {', '.join(str(o.line_number) for o in var.occurrences[1:])} for removal")
        report.append("")
        report.append("---")
        report.append("")

    # Final recommendations
    report.append("## Consolidation Strategy")
    report.append("")
    report.append("### Option 1: Remove Collapsible Derivations Box")
    report.append("If the 'Key Metric Derivations' collapse box duplicates equations shown elsewhere,")
    report.append("consider removing it entirely. Readers can find formulas in context.")
    report.append("")
    report.append("### Option 2: Keep Only Collapse Box")
    report.append("Move all derivations to the collapse box, reference it from body text:")
    report.append('`See [Key Metric Derivations](#key-metric-derivations) for the full calculation.`')
    report.append("")
    report.append("### Option 3: Use Shorter Inline References")
    report.append("For repeated equations, show the result inline and link to full derivation:")
    report.append("`ROI = $389B / $611M = 637:1 (see [derivation](#roi-derivation))`")
    report.append("")

    # --- SENTENCE DUPLICATES ---
    if sentence_dups:
        report.append("---")
        report.append("")
        report.append("## Duplicate Sentences")
        report.append("")
        report.append("These exact (or near-exact) sentences appear multiple times:")
        report.append("")

        for i, dup in enumerate(sentence_dups[:15], 1):
            report.append(f"### {i}. Lines {', '.join(map(str, dup.line_numbers))}")
            report.append("")
            report.append(f"> {dup.sentence}")
            report.append("")
            report.append(f"- **Occurrences**: {len(dup.line_numbers)}")
            report.append(f"- **Sections**: {', '.join(set(dup.sections))}")
            report.append(f"- **Words**: {dup.word_count}")
            report.append("")

    # --- SIMILAR PARAGRAPHS ---
    if similar_paras:
        report.append("---")
        report.append("")
        report.append("## Similar Paragraphs")
        report.append("")
        report.append("These paragraph pairs share >50% of their words (may be paraphrasing the same content):")
        report.append("")

        for i, pair in enumerate(similar_paras[:10], 1):
            report.append(f"### Pair {i}: {pair.similarity:.0%} similarity")
            report.append("")
            report.append(f"**Paragraph 1** (Line {pair.para1_line}, {pair.para1_section}):")
            report.append(f"> {pair.para1_preview}")
            report.append("")
            report.append(f"**Paragraph 2** (Line {pair.para2_line}, {pair.para2_section}):")
            report.append(f"> {pair.para2_preview}")
            report.append("")
            report.append(f"- **Shared words**: {pair.shared_words}")
            report.append("")
            report.append("**Action**: Review if these paragraphs are making the same point. Consider consolidating.")
            report.append("")

    # --- REPEATED PHRASES ---
    if repeated_phrases:
        report.append("---")
        report.append("")
        report.append("## Repeated Phrases")
        report.append("")
        report.append("These 5+ word phrases appear 3+ times (may indicate repetitive writing):")
        report.append("")
        report.append("| Phrase | Occurrences | Lines |")
        report.append("|--------|-------------|-------|")

        for phrase in repeated_phrases[:20]:
            lines_preview = ', '.join(map(str, phrase.line_numbers[:5]))
            if len(phrase.line_numbers) > 5:
                lines_preview += f" (+{len(phrase.line_numbers) - 5} more)"
            report.append(f"| \"{phrase.phrase}\" | {phrase.occurrences} | {lines_preview} |")

        report.append("")
        report.append("**Note**: Some repeated phrases are intentional (technical terms, proper names).")
        report.append("Focus on phrases that suggest the same explanation is being given multiple times.")
        report.append("")

    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(description='Check QMD files for content redundancy')
    parser.add_argument('file', help='QMD file to analyze')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed context for each occurrence')
    parser.add_argument('--output', '-o', help='Output report to file (markdown)')
    parser.add_argument('--latex-only', action='store_true', help='Only check _latex variable duplicates')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    # Load file content
    with open(args.file, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    print(f"Loading _variables.yml...")
    variables = load_variables_yml()
    print(f"Loaded {len(variables)} variables")

    print(f"Analyzing {args.file}...")

    # 1. Analyze _latex duplicates
    duplicates = analyze_file(args.file, variables)
    print(f"  Found {len(duplicates)} duplicate _latex variables")

    sentence_dups = []
    similar_paras = []
    repeated_phrases = []
    outline = None

    if not args.latex_only:
        # 2. Analyze document outline
        print("  Extracting document outline...")
        headings = extract_outline(content)
        outline = analyze_outline(headings)
        print(f"  Found {len(headings)} headings, {len(outline.similar_headings)} similar pairs, {len(outline.summary_pattern_headings)} summary sections")

        # 3. Analyze sentence duplicates
        print("  Checking for duplicate sentences...")
        sentences = extract_sentences(content)
        sentence_dups = find_duplicate_sentences(sentences, lines)
        print(f"  Found {len(sentence_dups)} duplicate sentences")

        # 4. Analyze similar paragraphs
        print("  Checking for similar paragraphs...")
        paragraphs = extract_paragraphs(content)
        similar_paras = find_similar_paragraphs(paragraphs, threshold=0.5)
        print(f"  Found {len(similar_paras)} similar paragraph pairs")

        # 5. Analyze repeated phrases
        print("  Checking for repeated phrases...")
        repeated_phrases = find_repeated_phrases(content, n=5, min_occurrences=3)
        print(f"  Found {len(repeated_phrases)} repeated phrases")

    report = generate_report(
        duplicates,
        args.file,
        verbose=args.verbose,
        sentence_dups=sentence_dups,
        similar_paras=similar_paras,
        repeated_phrases=repeated_phrases,
        outline=outline
    )

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
