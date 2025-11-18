#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate Quarto Render Output

This script checks rendered HTML files for common issues:
1. Unrendered inline Python expressions (literal `{python}` in output)
2. Blacklisted patterns (findfont warnings, echo: false leaks, Python errors, frontmatter leaks)
3. Other rendering failures

Usage:
    python scripts/post-render-validation.py [--output-dir _book/warondisease]

Exit codes:
    0 - All checks passed
    1 - Validation errors found
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

# Set UTF-8 encoding for stdout
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class ValidationError:
    def __init__(self, file_path, line_num, error_type, context):
        self.file_path = file_path
        self.line_num = line_num
        self.error_type = error_type
        self.context = context

    def __str__(self):
        return f"{self.file_path}:{self.line_num} [{self.error_type}] {self.context}"


BLACKLISTED_PATTERNS = [
    {
        "regex": re.compile(r'findfont:', re.IGNORECASE),
        "error_type": "FINDFONT_WARNING",
        "message": "Matplotlib font warning in output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r'echo:\s*false', re.IGNORECASE),
        "error_type": "ECHO_FALSE_LEAK",
        "message": "Cell option 'echo: false' leaked into output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
        "skip_if": lambda line: line.strip().startswith('<!--') or 'href=' in line or 'class=' in line,
    },
    {
        "regex": re.compile(r'NameError:|AttributeError:|ImportError:|ModuleNotFoundError:|KeyError:|TypeError:'),
        "error_type": "PYTHON_ERROR",
        "message": "Python error in output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r'lastToneElevationWithHumorHash|lastInstructionalVoiceHash|lastFormattedHash|lastFactCheckHash|lastStyleCheckHash|lastStructureCheckHash|lastLatexCheckHash|lastParamCheckHash'),
        "error_type": "FRONTMATTER_LEAK",
        "message": "Frontmatter metadata leaked into output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r'<span[^>]*>[^<]*quarto-shortcode[^<]*</span>', re.IGNORECASE),
        "error_type": "QUARTO_SHORTCODE_TEXT",
        "message": "Quarto shortcode rendered as literal span text",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
]


def find_html_files(output_dir):
    """Find all HTML files in the output directory"""
    html_files = []
    for path in Path(output_dir).rglob('*.html'):
        # Skip site_libs and other infrastructure
        if 'site_libs' not in str(path):
            html_files.append(path)
    return html_files


def check_unrendered_inline_python(content, file_path):
    """Check for literal `{python} ...` expressions in HTML output"""
    errors = []

    # Pattern: <code>{python} something</code>
    # This indicates inline Python didn't evaluate
    pattern = r'<code>\{python\}\s+([^<]+)</code>'

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        matches = re.finditer(pattern, line)
        for match in matches:
            var_name = match.group(1).strip()
            context = f"Unrendered inline expression: `{{python}} {var_name}`"
            errors.append(ValidationError(file_path, i, "UNRENDERED_PYTHON", context))

    return errors


def check_dollar_python_pattern(content, file_path):
    """Check for literal `{python} ...` patterns in HTML output"""
    errors = []

    # Pattern: {python} something - this is the inline Python syntax that should be rendered
    # If it appears literally in the HTML, it means Quarto didn't evaluate it
    # Look for {python} followed by content (variable name or expression)
    # Pattern matches: {python} followed by word characters, dots, spaces, or simple expressions
    pattern = r'\{python\}\s*[^\s<}]+'

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Skip HTML comments and script tags
        if '<!--' in line:
            continue
        if '<script' in line.lower():
            continue

        # Only skip if it's in a <pre><code> documentation block (multi-line code examples)
        # Don't skip standalone <code> tags - those are where unrendered inline Python appears!
        if '<pre' in line.lower() and '<code' in line.lower():
            # This is likely a code example showing syntax - skip it
            python_pos = line.find('{python}')
            if python_pos != -1:
                pre_start = line.lower().find('<pre')
                pre_end = line.lower().find('</pre>')
                if pre_start != -1 and pre_end != -1 and pre_start < python_pos < pre_end:
                    continue  # It's in a documentation code block, skip it

        matches = re.finditer(pattern, line)
        for match in matches:
            matched_text = match.group(0)
            # Extract context (first 100 chars)
            context_text = matched_text[:100].strip()
            # Get surrounding context (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(line), match.end() + 50)
            context = f"Unrendered {{python}} pattern: `{context_text}` (context: ...{line[start:end]}...)"
            errors.append(ValidationError(file_path, i, "UNRENDERED_PYTHON_INLINE", context))

    return errors


def check_blacklisted_strings(content, file_path):
    """Check for generic blacklisted string patterns in rendered output"""
    errors = []
    lines = content.split('\n')

    for pattern_config in BLACKLISTED_PATTERNS:
        regex = pattern_config["regex"]
        skip_in_comments = pattern_config.get("skip_in_comments", False)
        skip_in_scripts = pattern_config.get("skip_in_scripts", False)
        skip_if = pattern_config.get("skip_if", None)
        
        for i, line in enumerate(lines, 1):
            # Apply skip conditions
            if skip_in_comments and '<!--' in line:
                continue
            if skip_in_scripts and '<script' in line.lower():
                continue
            if skip_if and skip_if(line):
                continue
            
            # Check for pattern match
            match = regex.search(line)
            if match:
                # Get surrounding context (50 chars before and after match)
                start = max(0, match.start() - 50)
                end = min(len(line), match.end() + 50)
                snippet = line[start:end].strip()
                context = f"{pattern_config['message']}: ...{snippet}..."
                errors.append(ValidationError(file_path, i, pattern_config["error_type"], context))

    return errors


def validate_file(file_path):
    """Run all validation checks on a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [ValidationError(file_path, 0, "READ_ERROR", f"Failed to read file: {e}")]

    errors = []
    errors.extend(check_unrendered_inline_python(content, file_path))
    errors.extend(check_dollar_python_pattern(content, file_path))
    errors.extend(check_blacklisted_strings(content, file_path))

    return errors


def main():
    parser = argparse.ArgumentParser(description='Validate Quarto render output for common issues')
    parser.add_argument('--output-dir', default='_book/warondisease',
                        help='Directory containing rendered HTML files')
    parser.add_argument('--fail-on-warnings', action='store_true',
                        help='Treat warnings as errors')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        print(f"[ERROR] Output directory not found: {output_dir}")
        return 1

    print(f"[VALIDATION] Validating rendered HTML in {output_dir}...")

    html_files = find_html_files(output_dir)
    print(f"   Found {len(html_files)} HTML files to check")

    all_errors = []
    errors_by_type = defaultdict(list)

    for file_path in html_files:
        errors = validate_file(file_path)
        if errors:
            all_errors.extend(errors)
            for error in errors:
                errors_by_type[error.error_type].append(error)

    # Print results
    if not all_errors:
        print("[OK] All validation checks passed!")
        return 0

    print(f"\n[ERROR] Found {len(all_errors)} validation error(s):\n")

    # Group errors by type for better readability
    for error_type, errors in sorted(errors_by_type.items()):
        print(f"  {error_type}: {len(errors)} error(s)")
        for error in errors[:10]:  # Show first 10 of each type
            print(f"    {error}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        print()

    # Provide suggestions
    print("[SUGGESTIONS]")
    if 'UNRENDERED_PYTHON' in errors_by_type:
        print("   - Unrendered inline Python: This happens when Quarto uses cached")
        print("     computations. Clear freeze directories: rm -rf _freeze .quarto/_freeze")
        print("   - Or render with: quarto render --execute-daemon restart")
        print("   - Check that variables are defined before use")
    if 'UNRENDERED_PYTHON_INLINE' in errors_by_type:
        print("   - Unrendered `{python}` pattern: Inline Python expressions didn't evaluate")
        print("     Clear freeze directories: rm -rf _freeze .quarto/_freeze")
        print("   - Or render with: quarto render --execute-daemon restart")
        print("   - Ensure Python code blocks execute before inline expressions")
        print("   - Check that variables referenced in `{python}` are defined")
    if 'ECHO_FALSE_LEAK' in errors_by_type:
        print("   - 'echo: false' in output: Use cell option format: #| echo: false")
        print("     (with #| prefix, not as YAML)")
    if 'PYTHON_ERROR' in errors_by_type:
        print("   - Python errors: Check Python code cells for exceptions")
    if 'FRONTMATTER_LEAK' in errors_by_type:
        print("   - Frontmatter leakage: YAML frontmatter from included files is appearing in output")
        print("     This usually means {{< include >}} is not properly stripping frontmatter")
        print("     Check that included files have properly formatted YAML (--- at start and end)")
        print("     Or remove frontmatter from files that are only meant to be included")
    if 'FINDFONT_WARNING' in errors_by_type:
        print("   - Matplotlib findfont warnings: Ensure the required fonts are installed")
        print("     or configure Matplotlib to use bundled fonts to avoid runtime warnings")

    return 1


if __name__ == '__main__':
    sys.exit(main())
