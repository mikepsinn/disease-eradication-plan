#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preview a QMD file with Quarto variables replaced by their actual values.

Useful for reviewing hardcoded numbers vs. variables and catching inconsistencies.

Usage:
    python scripts/preview-qmd-with-variables.py knowledge/appendix/incentive-alignment-bonds-paper.qmd
    python scripts/preview-qmd-with-variables.py knowledge/appendix/incentive-alignment-bonds-paper.qmd -o preview.md
    python scripts/preview-qmd-with-variables.py knowledge/appendix/incentive-alignment-bonds-paper.qmd --numbers-only
    python scripts/preview-qmd-with-variables.py knowledge/strategy/questions.qmd --export-markdown -o _analysis/questions-export.md
"""
from __future__ import annotations

import sys
import re
import argparse
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlsplit, urlunsplit

# Handle Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path for imports
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from dih_models.variable_replacement import clean_for_readme, load_variables, replace_variables
from dih_models.yaml_utils import yaml_safe_load

MANUAL_BASE_URL = "https://manual.warondisease.org"


def strip_confidence_intervals(text: str) -> str:
    """Strip '(95% CI: ...)' from resolved variable text to match rendered HTML."""
    return re.sub(r'\s*\(95% CI:\s*[^)]+\)', '', text)


def split_qmd_frontmatter(content: str) -> Tuple[dict, str]:
    """Return parsed YAML frontmatter and body content."""
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n?', content)
    if not match:
        return {}, content

    metadata = yaml_safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        metadata = {}

    return metadata, content[match.end():]


def qmd_rel_to_html_url(path: Path, project_root: Path, manual_base_url: str) -> str:
    """Convert a project QMD path to its public manual HTML URL."""
    rel_path = path.resolve().relative_to(project_root.resolve()).as_posix()
    if rel_path.endswith('.qmd'):
        rel_path = rel_path[:-4] + '.html'
    return f"{manual_base_url.rstrip('/')}/{rel_path}"


def qmd_path_to_html_path(path: str) -> str:
    """Convert a URL path ending in .qmd to the rendered .html path."""
    if path.endswith('.qmd'):
        return path[:-4] + '.html'
    return path


def resolve_manual_href(
    href: str,
    source_path: Path,
    project_root: Path,
    manual_base_url: str,
) -> str:
    """Resolve local Markdown/QMD links to public manual URLs."""
    href = href.strip()
    if not href:
        return href

    source_url = qmd_rel_to_html_url(source_path, project_root, manual_base_url)

    if href.startswith('#'):
        return f"{source_url}{href}"

    if href.startswith(('mailto:', 'tel:', 'javascript:', '{{', '//')):
        return href

    parsed = urlsplit(href)

    if parsed.scheme in {'http', 'https'}:
        if parsed.netloc.lower() == 'manual.warondisease.org':
            path = qmd_path_to_html_path(parsed.path)
            return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))
        return href

    if href.startswith('/'):
        path = qmd_path_to_html_path(parsed.path)
        return urlunsplit(('https', urlsplit(manual_base_url).netloc, path, parsed.query, parsed.fragment))

    path = parsed.path.replace('\\', '/')
    if not path:
        return href

    if path.endswith(('.qmd', '.html')) or path.startswith(('assets/', './assets/', '../assets/')):
        resolved_path = (source_path.parent / path).resolve()
        rel_path = resolved_path.relative_to(project_root.resolve()).as_posix()
        rel_path = qmd_path_to_html_path(rel_path)
        return urlunsplit(('https', urlsplit(manual_base_url).netloc, f"/{rel_path}", parsed.query, parsed.fragment))

    return href


def absolutize_manual_links(
    content: str,
    source_path: Path,
    project_root: Path,
    manual_base_url: str,
) -> str:
    """Convert local Markdown link targets to absolute manual URLs."""
    link_pattern = re.compile(r'(!?\[[^\]]*\]\()([^\s)]+)(\))')

    def replace_link(match: re.Match) -> str:
        return (
            match.group(1)
            + resolve_manual_href(match.group(2), source_path, project_root, manual_base_url)
            + match.group(3)
        )

    return link_pattern.sub(replace_link, content)


def clean_for_export_markdown(
    content: str,
    source_path: Path,
    project_root: Path,
    manual_base_url: str,
) -> str:
    """Build exportable Markdown from a resolved QMD body."""
    metadata, body = split_qmd_frontmatter(content)

    title = metadata.get('title')
    if title:
        body = f"# {title}\n\n{body.lstrip()}"

    body = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', body, flags=re.IGNORECASE | re.DOTALL)
    body = clean_for_readme(body)
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
    body = absolutize_manual_links(body, source_path, project_root, manual_base_url)
    body = re.sub(r'\n{4,}', '\n\n\n', body)
    return body.strip() + '\n'


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
    parser.add_argument('output_file', nargs='?',
                        help='Optional output file shorthand, equivalent to --output')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--variables-yml', default='_variables.yml',
                        help='Path to variables YAML file')
    parser.add_argument('--numbers-only', action='store_true',
                        help='Only show potential hardcoded numbers, not full preview')
    parser.add_argument('--show-ci', action='store_true',
                        help='Show confidence intervals (stripped by default to match rendered HTML)')
    parser.add_argument('--line-range', type=str,
                        help='Only show lines in range, e.g., "100-200"')
    parser.add_argument('--absolute-manual-links', action='store_true',
                        help='Convert local .qmd/.html links to absolute manual.warondisease.org URLs')
    parser.add_argument('--export-markdown', dest='export_markdown', action='store_true',
                        help='Export Markdown: title, resolved vars, no QMD-only syntax, absolute manual links')
    parser.add_argument('--copy-markdown', dest='export_markdown', action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument('--manual-base-url', default=MANUAL_BASE_URL,
                        help=f'Base URL for absolute manual links (default: {MANUAL_BASE_URL})')

    args = parser.parse_args()
    if args.output_file and not args.output:
        args.output = args.output_file

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

    if args.export_markdown:
        preview = clean_for_export_markdown(preview, qmd_path, project_root, args.manual_base_url)
    elif args.absolute_manual_links:
        preview = absolutize_manual_links(preview, qmd_path, project_root, args.manual_base_url)

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
        header = ""
        if not args.export_markdown:
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
