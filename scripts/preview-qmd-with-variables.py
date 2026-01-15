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
import yaml
from pathlib import Path
from html import unescape
from typing import Dict, List, Tuple

# Handle Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def strip_html_tags(text: str) -> str:
    """Remove HTML tags and extract just the display text."""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Unescape HTML entities
    clean = unescape(clean)
    return clean.strip()


def load_variables(variables_yml_path: Path) -> Dict[str, str]:
    """Load variables from YAML and strip HTML for plain text values."""
    variables = {}

    if not variables_yml_path.exists():
        print(f"WARNING: Variables file not found: {variables_yml_path}", file=sys.stderr)
        return variables

    with open(variables_yml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if data:
        for key, value in data.items():
            if isinstance(value, str):
                # Strip HTML to get plain text value
                plain_value = strip_html_tags(value)
                variables[key] = plain_value
            else:
                variables[key] = str(value)

    return variables


def replace_variables(content: str, variables: Dict[str, str], highlight_missing: bool = True) -> str:
    """Replace {{< var name >}} with actual values."""

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
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(preview)
        print(f"Preview written to {output_path}")
    else:
        print(preview)


if __name__ == '__main__':
    main()
