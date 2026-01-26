#!/usr/bin/env python3
"""
Quick Validation Hook for Claude Code PostToolUse
=================================================

Runs after Edit|Write operations on *.qmd files.
Performs fast validation checks and returns issues as JSON for Claude context injection.

Checks performed:
- Broken variable references ({{< var unknown_var >}})
- Broken internal links (paths that don't exist)
- Obvious hardcoded values that match known parameters

Usage:
  python .claude/hooks/quick-validate.py <file_path>

Exit codes:
  0 - No issues found (or file is not a QMD)
  1 - Issues found (printed to stdout as JSON)
"""

import sys
import os
import re
import json
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]


def get_project_root():
    """Find project root by looking for _quarto.yml or _variables.yml"""
    current = Path(os.getcwd())
    while current != current.parent:
        if (current / '_quarto.yml').exists() or (current / '_variables.yml').exists():
            return current
        current = current.parent
    return Path(os.getcwd())


def load_variables():
    """Load variable names from _variables.yml"""
    root = get_project_root()
    variables_file = root / '_variables.yml'

    if not variables_file.exists():
        return set()

    variables = set()
    try:
        with open(variables_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple regex to extract variable names (keys before colons)
            for match in re.finditer(r'^  ([a-z][a-z0-9_]+):', content, re.MULTILINE):
                variables.add(match.group(1))
    except Exception:
        pass

    return variables


def check_broken_variables(content, valid_variables):
    """Check for variable references that don't exist in _variables.yml"""
    issues = []

    # Find all {{< var name >}} references
    var_pattern = r'\{\{<\s*var\s+([a-z][a-z0-9_]+)\s*>\}\}'

    for match in re.finditer(var_pattern, content):
        var_name = match.group(1)
        if var_name not in valid_variables:
            # Get line number
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'type': 'broken_variable',
                'line': line_num,
                'variable': var_name,
                'message': f'Undefined variable: {var_name}'
            })

    return issues


def check_broken_links(content, file_path):
    """Check for internal links to files that don't exist"""
    issues = []
    root = get_project_root()
    file_dir = Path(file_path).parent

    # Find internal links: [text](path.qmd) or [text](../path.qmd)
    link_pattern = r'\[([^\]]*)\]\(([^)]+\.qmd(?:#[^)]*)?)\)'

    for match in re.finditer(link_pattern, content):
        link_text = match.group(1)
        link_path = match.group(2)

        # Remove anchor
        path_only = link_path.split('#')[0]

        # Skip external URLs
        if path_only.startswith('http'):
            continue

        # Resolve relative path
        if path_only.startswith('/'):
            full_path = root / path_only[1:]
        else:
            full_path = file_dir / path_only

        full_path = full_path.resolve()

        if not full_path.exists():
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'type': 'broken_link',
                'line': line_num,
                'path': path_only,
                'message': f'Broken link: {path_only}'
            })

    return issues


def check_hardcoded_values(content):
    """Check for obvious hardcoded values that should be variables"""
    issues = []

    # Common patterns that should probably be parameters
    hardcoded_patterns = [
        # Large dollar amounts
        (r'\$(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(?:trillion|billion|million)',
         'Consider using a variable for this dollar amount'),
        # Specific percentages in text (not in LaTeX)
        (r'(?<!\$)\b(\d{1,2}(?:\.\d+)?)\s*%(?![\s}]*>)',
         'Consider using a variable for this percentage'),
    ]

    for pattern, message in hardcoded_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            # Skip if inside a {{< var >}} block
            start = match.start()
            context_before = content[max(0, start-50):start]
            if '{{< var' in context_before and '>}}' not in context_before:
                continue

            # Skip if inside LaTeX blocks
            if '$' in content[max(0, start-5):start]:
                continue

            line_num = content[:start].count('\n') + 1
            issues.append({
                'type': 'hardcoded_value',
                'line': line_num,
                'value': match.group(0),
                'message': message
            })

    return issues


def validate_qmd_file(file_path):
    """Run all validations on a QMD file"""
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [{'type': 'error', 'message': f'Could not read file: {e}'}]

    # Load valid variables
    valid_variables = load_variables()

    # Run checks
    issues.extend(check_broken_variables(content, valid_variables))
    issues.extend(check_broken_links(content, file_path))

    # Hardcoded value check - only return first few to avoid noise
    hardcoded = check_hardcoded_values(content)
    if hardcoded:
        issues.extend(hardcoded[:3])  # Limit to 3 to avoid overwhelming
        if len(hardcoded) > 3:
            issues.append({
                'type': 'info',
                'message': f'... and {len(hardcoded) - 3} more potential hardcoded values'
            })

    return issues


def main():
    if len(sys.argv) < 2:
        print('Usage: python quick-validate.py <file_path>', file=sys.stderr)
        sys.exit(0)

    file_path = sys.argv[1]

    # Only validate QMD files
    if not file_path.endswith('.qmd'):
        sys.exit(0)

    # Skip if file doesn't exist (might have been deleted)
    if not os.path.exists(file_path):
        sys.exit(0)

    issues = validate_qmd_file(file_path)

    if not issues:
        sys.exit(0)

    # Output issues as JSON for Claude to process
    result = {
        'file': file_path,
        'issueCount': len(issues),
        'issues': issues
    }

    print(json.dumps(result, indent=2))
    sys.exit(1)


if __name__ == '__main__':
    main()
