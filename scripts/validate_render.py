#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate Quarto Render Output

This script checks rendered HTML files for common issues:
1. Unrendered inline Python expressions (literal `{python}` in output)
2. "echo: false" appearing in output (indicates cell option leaked)
3. Other rendering failures

Usage:
    python scripts/validate_render.py [--output-dir _book/warondisease]

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


def check_echo_false_in_output(content, file_path):
    """Check for 'echo: false' appearing in rendered output"""
    errors = []

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Look for "echo: false" in the visible content (not in HTML attributes/comments)
        # This usually appears when cell options leak into output
        if 'echo: false' in line or 'echo:false' in line:
            # Skip if it's in a comment or HTML attribute
            if not (line.strip().startswith('<!--') or 'href=' in line or 'class=' in line):
                context = "Cell option 'echo: false' leaked into output"
                errors.append(ValidationError(file_path, i, "ECHO_FALSE_LEAK", context))

    return errors


def check_python_errors(content, file_path):
    """Check for Python error messages in output"""
    errors = []

    # Common Python error patterns
    error_patterns = [
        r'NameError:',
        r'AttributeError:',
        r'ImportError:',
        r'ModuleNotFoundError:',
        r'KeyError:',
        r'TypeError:',
    ]

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for pattern in error_patterns:
            if re.search(pattern, line):
                context = f"Python error in output: {line[:100]}"
                errors.append(ValidationError(file_path, i, "PYTHON_ERROR", context))
                break

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
    errors.extend(check_echo_false_in_output(content, file_path))
    errors.extend(check_python_errors(content, file_path))

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
        print(f"❌ Error: Output directory not found: {output_dir}")
        return 1

    print(f"🔍 Validating rendered HTML in {output_dir}...")

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
        print("✅ All validation checks passed!")
        return 0

    print(f"\n❌ Found {len(all_errors)} validation error(s):\n")

    # Group errors by type for better readability
    for error_type, errors in sorted(errors_by_type.items()):
        print(f"  {error_type}: {len(errors)} error(s)")
        for error in errors[:10]:  # Show first 10 of each type
            print(f"    {error}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        print()

    # Provide suggestions
    print("💡 Suggestions:")
    if 'UNRENDERED_PYTHON' in errors_by_type:
        print("   - Unrendered inline Python: This happens when Quarto uses cached")
        print("     computations. Clear freeze directories: rm -rf _freeze .quarto/_freeze")
        print("   - Or render with: quarto render --execute-daemon restart")
        print("   - Check that variables are defined before use")
    if 'ECHO_FALSE_LEAK' in errors_by_type:
        print("   - 'echo: false' in output: Use cell option format: #| echo: false")
        print("     (with #| prefix, not as YAML)")
    if 'PYTHON_ERROR' in errors_by_type:
        print("   - Python errors: Check Python code cells for exceptions")

    return 1


if __name__ == '__main__':
    sys.exit(main())
