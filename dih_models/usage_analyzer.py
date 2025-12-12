#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Usage Analyzer - Parse QMD files for parameter usage patterns
======================================================================

Analyze how parameters are used in economics.qmd to compute usage scores:
- Frequency: How many times does it appear?
- Position: Where does it first appear? (earlier = more important)
- Narrative weight: Is it in headlines, section titles, key claims?

Usage:
    from dih_models.usage_analyzer import analyze_document_usage
    usage_data = analyze_document_usage("knowledge/economics/economics.qmd")
"""

import sys
import re
from pathlib import Path
from typing import Dict, Any

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def analyze_document_usage(qmd_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Analyze parameter usage in a QMD document.

    Returns:
        Dict mapping parameter names to usage metrics:
        {
            'PARAMETER_NAME': {
                'frequency': 12,           # Total occurrences
                'first_appearance': 0.15,  # Fraction through document (0.0-1.0)
                'in_headlines': 2,         # Appears in ## headers
                'in_claims': 3,            # Appears in bold/italic emphasis
                'sections': ['intro', 'cost-benefit', ...],  # Which sections
                'position_weight': 0.85,   # Earlier = higher (1.0 - first_appearance)
                'narrative_weight': 0.6    # Composite of headlines/claims
            }
        }
    """
    if not qmd_path.exists():
        print(f"[WARN] Document not found: {qmd_path}", file=sys.stderr)
        return {}

    with open(qmd_path, encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Regex to find Quarto variables: {{< var parameter_name >}}
    var_pattern = re.compile(r'\{\{<\s*var\s+([a-z0-9_]+)\s*>\}\}', re.IGNORECASE)

    # Track all variable occurrences
    usage = {}
    total_lines = len(lines)
    current_section = "introduction"

    for line_num, line in enumerate(lines):
        # Track section headers (# or ##)
        if line.startswith('# ') or line.startswith('## '):
            # Extract section ID from header or use text
            section_match = re.search(r'\{#([a-z0-9-]+)\}', line)
            if section_match:
                current_section = section_match.group(1)
            else:
                # Use sanitized header text
                header_text = re.sub(r'[^a-z0-9-]', '-', line.lower().strip('# '))
                current_section = header_text[:50]  # Truncate long headers

        # Find all variable references in this line
        for match in var_pattern.finditer(line):
            var_name = match.group(1).upper()  # Convert to uppercase for parameter name

            if var_name not in usage:
                usage[var_name] = {
                    'frequency': 0,
                    'first_appearance': line_num / total_lines,  # Fraction through doc
                    'in_headlines': 0,
                    'in_claims': 0,
                    'sections': set(),
                    'line_numbers': []
                }

            # Increment frequency
            usage[var_name]['frequency'] += 1
            usage[var_name]['sections'].add(current_section)
            usage[var_name]['line_numbers'].append(line_num)

            # Check if in headline (## header line)
            if line.startswith('#'):
                usage[var_name]['in_headlines'] += 1

            # Check if in emphasized text (bold/italic - indicates key claim)
            if '**' in line or '_' in line or line.strip().startswith('>'):
                usage[var_name]['in_claims'] += 1

    # Compute composite scores
    for param_name, metrics in usage.items():
        # Position weight: earlier appearance = higher weight (0-30 points)
        position_weight = 1.0 - metrics['first_appearance']  # 0.0-1.0

        # Narrative weight: headlines and claims (0-30 points)
        headline_score = min(1.0, metrics['in_headlines'] / 5.0)  # Cap at 5 headlines
        claim_score = min(1.0, metrics['in_claims'] / 10.0)       # Cap at 10 claims
        narrative_weight = (headline_score * 0.6 + claim_score * 0.4)

        # Frequency weight (0-30 points)
        freq_score = min(1.0, metrics['frequency'] / 20.0)  # Cap at 20 occurrences

        # Combined usage score (0-30 points)
        usage_score = (
            freq_score * 0.4 +
            position_weight * 0.3 +
            narrative_weight * 0.3
        ) * 30  # Scale to 0-30

        metrics['position_weight'] = position_weight
        metrics['narrative_weight'] = narrative_weight
        metrics['usage_score'] = usage_score
        metrics['sections'] = list(metrics['sections'])  # Convert set to list for JSON

    return usage


def print_usage_report(usage_data: Dict[str, Dict[str, Any]], top_n: int = 20):
    """Print human-readable usage report"""
    # Sort by usage_score
    sorted_params = sorted(
        usage_data.items(),
        key=lambda x: x[1].get('usage_score', 0),
        reverse=True
    )

    print(f"\n=== Top {top_n} Parameters by Document Usage ===\n")
    print(f"{'Rank':<6} {'Parameter':<45} {'Score':<8} {'Freq':<6} {'1st %':<8} {'Headlines':<10} {'Sections':<8}")
    print("-" * 110)

    for rank, (param_name, metrics) in enumerate(sorted_params[:top_n], start=1):
        score = metrics.get('usage_score', 0)
        freq = metrics.get('frequency', 0)
        first_pct = metrics.get('first_appearance', 0) * 100
        headlines = metrics.get('in_headlines', 0)
        sections = len(metrics.get('sections', []))

        print(f"{rank:<6} {param_name:<45} {score:>6.1f} {freq:>6} {first_pct:>6.1f}% {headlines:>10} {sections:>8}")


if __name__ == "__main__":
    # Analyze economics.qmd
    qmd_path = Path("knowledge/economics/economics.qmd")

    if not qmd_path.exists():
        print(f"[ERROR] File not found: {qmd_path}")
        sys.exit(1)

    print(f"Analyzing parameter usage in {qmd_path}...")
    usage_data = analyze_document_usage(qmd_path)

    print(f"[OK] Found {len(usage_data)} unique parameters")

    # Print top 20 by usage
    print_usage_report(usage_data, top_n=20)

    # Save to JSON
    import json
    output_path = Path("_analysis/document-usage.json")
    output_path.parent.mkdir(exist_ok=True, parents=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(usage_data, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Saved usage data to {output_path}")
