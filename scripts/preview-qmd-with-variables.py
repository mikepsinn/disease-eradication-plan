#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preview a QMD file with Quarto variables replaced by their actual values.

Useful for reviewing hardcoded numbers vs. variables and catching inconsistencies.

Usage:
    python scripts/preview-qmd-with-variables.py knowledge/appendix/incentive-alignment-bonds-paper.qmd
    python scripts/preview-qmd-with-variables.py knowledge/appendix/incentive-alignment-bonds-paper.qmd -o preview.md
    python scripts/preview-qmd-with-variables.py knowledge/appendix/incentive-alignment-bonds-paper.qmd --numbers-only
"""
from __future__ import annotations

import sys
import re
import argparse
from pathlib import Path
from typing import List, Tuple

# Handle Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root to path for imports
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from dih_models.variable_replacement import load_variables, replace_variables


def strip_confidence_intervals(text: str) -> str:
    """Strip '(95% CI: ...)' from resolved variable text to match rendered HTML."""
    return re.sub(r'\s*\(95% CI:\s*[^)]+\)', '', text)


def find_hardcoded_numbers(content: str) -> List[Tuple[int, str, str, str]]:
    """
    Find lines with hardcoded numbers that might need to be variables.

    Returns list of (line_number, number_found, context)
    """
    findings = []

    # Patterns for numbers that are often hardcoded when they shouldn't be
    patterns = [
        # Dollar amounts: $100M, $1.5B, $500,000
        (r'\$[\d,.]+\s*[BMKbmk](?:illion)?', 'dollar_amount'),
        # Billions/millions in text: 100 billion, 1.5 million
        (r'\b\d+(?:\.\d+)?\s*(?:billion|million|trillion)\b', 'large_number'),
        # Percentages: 50%, 12.5%
        (r'\b\d+(?:\.\d+)?%', 'percentage'),
        # Ratios: 100:1, 4.75:1
        (r'\b\d+(?:\.\d+)?:\d+', 'ratio'),
        # Large plain numbers: 100000, 1,000,000
        (r'\b\d{1,3}(?:,\d{3})+\b', 'large_plain_number'),
        # Year ranges that might be parameters
        (r'\b20\d{2}-20\d{2}\b', 'year_range'),
    ]

    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Skip lines that are already using variables
        if '{{< var' in line:
            continue
        # Skip code blocks
        if line.strip().startswith('```') or line.strip().startswith('$$'):
            continue
        # Skip YAML frontmatter markers
        if line.strip() == '---':
            continue

        for pattern, num_type in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                # Get context around the number
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = line[start:end].strip()
                if start > 0:
                    context = '...' + context
                if end < len(line):
                    context = context + '...'

                findings.append((line_num, match.group(), context, num_type))

    return findings


def main():
    parser = argparse.ArgumentParser(
        description='Preview QMD file with variables replaced'
    )
    parser.add_argument('qmd_file', help='Path to the QMD file')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--variables-yml', default='_variables.yml',
                        help='Path to variables YAML file')
    parser.add_argument('--numbers-only', action='store_true',
                        help='Only show potential hardcoded numbers, not full preview')
    parser.add_argument('--show-ci', action='store_true',
                        help='Show confidence intervals (stripped by default to match rendered HTML)')
    parser.add_argument('--line-range', type=str,
                        help='Only show lines in range, e.g., "100-200"')

    args = parser.parse_args()

    # Resolve paths
    project_root = Path(__file__).parent.parent
    qmd_path = Path(args.qmd_file)
    if not qmd_path.is_absolute():
        qmd_path = project_root / qmd_path

    yml_path = Path(args.variables_yml)
    if not yml_path.is_absolute():
        yml_path = project_root / yml_path

    if not qmd_path.exists():
        print(f"ERROR: File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    # Load variables
    variables = load_variables(yml_path)
    print(f"# Loaded {len(variables)} variables from {yml_path.name}", file=sys.stderr)

    # Read QMD content
    with open(qmd_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if args.numbers_only:
        # Just find and report hardcoded numbers
        findings = find_hardcoded_numbers(content)

        print(f"\n# Potential Hardcoded Numbers in {qmd_path.name}")
        print(f"# Total found: {len(findings)}")
        print("=" * 80)

        # Group by type
        by_type = {}
        for line_num, number, context, num_type in findings:
            if num_type not in by_type:
                by_type[num_type] = []
            by_type[num_type].append((line_num, number, context))

        for num_type in ['dollar_amount', 'large_number', 'percentage', 'ratio', 'large_plain_number', 'year_range']:
            if num_type in by_type:
                print(f"\n## {num_type.upper().replace('_', ' ')} ({len(by_type[num_type])} found)")
                print("-" * 60)
                for line_num, number, context in by_type[num_type][:50]:  # Limit to 50 per type
                    print(f"  Line {line_num}: {number}")
                    print(f"    Context: {context}")
                if len(by_type[num_type]) > 50:
                    print(f"  ... and {len(by_type[num_type]) - 50} more")

        return

    # Strip CIs from variable values unless --show-ci is set
    if not args.show_ci:
        variables = {k: strip_confidence_intervals(v) for k, v in variables.items()}

    # Replace variables
    preview = replace_variables(content, variables)

    # Apply line range filter if specified
    if args.line_range:
        start, end = map(int, args.line_range.split('-'))
        lines = preview.split('\n')
        preview_lines = []
        for i, line in enumerate(lines, 1):
            if start <= i <= end:
                preview_lines.append(f"{i:5d} | {line}")
        preview = '\n'.join(preview_lines)

    # Output
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = project_root / output_path
        # Add source link at top of preview file
        rel_source = qmd_path.relative_to(project_root).as_posix()
        header = f"<!-- Source: {rel_source} -->\n\n"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(header + preview)
        print(f"Preview written to {output_path}")
    else:
        print(preview)


if __name__ == '__main__':
    main()
