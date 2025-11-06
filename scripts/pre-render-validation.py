#!/usr/bin/env python3
"""
Pre-render validation script
Validates .qmd files before Quarto rendering to catch errors early:
- LaTeX syntax errors (escaped dollar signs, malformed equations, etc.)
- Missing image files
- Invalid image paths
- GIF files not wrapped in HTML-only blocks (prevents PDF build failures)

Runs automatically via _quarto.yml pre-render hook
"""

import os
import re
import sys
from glob import glob
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class ValidationError:
    def __init__(self, file: str, line: int, message: str, context: str, column: Optional[int] = None):
        self.file = file
        self.line = line
        self.column = column
        self.message = message
        self.context = context

errors: List[ValidationError] = []

# Common LaTeX error patterns to check for
latex_patterns = [
    {
        'pattern': re.compile(r'\$\$\$'),
        'message': 'Triple dollar sign ($$$) - should be $$ for display math or single $ for inline',
    },
    {
        'pattern': re.compile(r'\\\$\$'),
        'message': 'Escaped double dollar sign (\\$$) - likely intended as single $ inside math mode',
    },
    {
        'pattern': re.compile(r'\$\$[^\n]*\\underbrace\{[^}]*\}[^\n]*\$\$'),
        'message': 'Check \\underbrace syntax - ensure all braces are properly closed',
        'validator': lambda match: check_brace_balance(match),
    },
    {
        'pattern': re.compile(r'\$\$[^\n]*\\\\\]'),
        'message': 'Malformed equation end (\\]) - should be ] without extra backslash',
    },
    {
        'pattern': re.compile(r'\\\}\\_\\\{'),
        'message': 'Malformed subscript (}_{) - should be }_{',
    },
]

def check_brace_balance(match: str) -> bool:
    """Check if braces are balanced in a match"""
    brace_count = 0
    for char in match:
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        if brace_count < 0:
            return False
    return brace_count == 0

def check_math_delimiters(content: str, filename: str):
    """Check for unmatched dollar signs in math mode"""
    lines = content.split('\n')
    in_math_block = False

    for line_index, line in enumerate(lines):
        # Skip code blocks
        if line.strip().startswith('```'):
            continue

        # Track display math mode ($$)
        display_math_matches = re.findall(r'\$\$', line)
        for _ in display_math_matches:
            in_math_block = not in_math_block

        # Check for single $ in display math mode (potential error)
        # BUT ignore \$ (escaped dollar signs, which are valid in \text{} blocks)
        if in_math_block and '$' in line and '$$' not in line:
            # Remove all \$ (escaped dollar signs) and \text{...} blocks
            cleaned_line = re.sub(r'\\text\{[^}]*\}', '', line)  # Remove \text{...} blocks
            cleaned_line = re.sub(r'\\\$', '', cleaned_line)      # Remove escaped dollar signs

            # Now check if there are any remaining unescaped $ signs
            if '$' in cleaned_line:
                context = line.strip()[:80]
                errors.append(ValidationError(
                    file=filename,
                    line=line_index + 1,
                    message='Unescaped $ inside display math mode ($$...$$)',
                    context=context
                ))

        # Check for * at the start of a line inside math block (markdown bullet interfering)
        if in_math_block and re.match(r'^\s+\*\s+', line):
            context = line.strip()[:80]
            errors.append(ValidationError(
                file=filename,
                line=line_index + 1,
                message='Markdown bullet (*) inside math block - use + for addition or \\cdot for multiplication',
                context=context
            ))

        # Check for blank lines inside math block (causes LaTeX errors)
        if in_math_block and line.strip() == '' and '$$' not in line:
            errors.append(ValidationError(
                file=filename,
                line=line_index + 1,
                message='Blank line inside math block ($$...$$) - remove blank line or close math block first',
                context='(blank line)'
            ))

def check_image_paths(content: str, filepath: str):
    """Check for missing image files"""
    lines = content.split('\n')
    file_dir = os.path.dirname(filepath)

    # Match markdown image syntax: ![alt text](path)
    markdown_image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    # Match HTML img tags: <img src="path" /> or <img src='path' />
    html_image_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)

    for line_index, line in enumerate(lines):
        # Check markdown image syntax
        markdown_matches = markdown_image_pattern.finditer(line)
        for match in markdown_matches:
            image_path = match.group(2)
            _check_single_image_path(image_path, filepath, file_dir, line_index + 1, line)

        # Check HTML img tags
        html_matches = html_image_pattern.finditer(line)
        for match in html_matches:
            image_path = match.group(1)
            _check_single_image_path(image_path, filepath, file_dir, line_index + 1, line)

def _check_single_image_path(image_path: str, filepath: str, file_dir: str, line_number: int, line: str):
    """Helper function to check a single image path"""
    # Skip URLs (http://, https://, etc.)
    if image_path.startswith('http://') or image_path.startswith('https://'):
        return

    # Resolve the image path relative to the .qmd file
    resolved_path = os.path.normpath(os.path.join(file_dir, image_path))

    if not os.path.exists(resolved_path):
        errors.append(ValidationError(
            file=filepath,
            line=line_number,
            message=f'Image file not found: {image_path}',
            context=line.strip()[:80]
        ))

def check_em_dashes(content: str, filepath: str):
    """
    Check for em-dashes (—) which should be replaced with comma and space
    Only flags em-dashes that are surrounded by letters (alpha characters)
    Examples:
    - "word—word" should be flagged (surrounded by letters)
    - "word—" or "—word" or "word—\"" should NOT be flagged (not surrounded by letters)
    """
    lines = content.split('\n')
    # Pattern to match em-dash surrounded by letters: letter—letter
    em_dash_pattern = re.compile(r'[a-zA-Z]—[a-zA-Z]')

    for line_index, line in enumerate(lines):
        # Find all em-dashes surrounded by letters
        matches = list(em_dash_pattern.finditer(line))
        if matches:
            for match in matches:
                # Find the column position of the em-dash
                column = match.start() + 2  # Position of the em-dash (after first letter)
                errors.append(ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    column=column,
                    message='Em-dash (—) surrounded by letters found. Replace with comma and space (", ")',
                    context=line.strip()[:80]
                ))

def check_gif_references(content: str, filepath: str):
    """
    Check for GIF files that aren't wrapped in HTML-only blocks
    GIF files cannot be included in PDF output and must be wrapped in:
    ::: {.content-visible when-format="html"}
    <img src="path/to/file.gif" />
    :::
    """
    lines = content.split('\n')
    in_html_only_block = False
    block_depth = 0

    for line_index, line in enumerate(lines):
        # Track HTML-only conditional blocks
        if '{.content-visible when-format="html"}' in line:
            in_html_only_block = True
            block_depth = 0
        elif in_html_only_block and line.strip().startswith(':::'):
            if block_depth == 0:
                in_html_only_block = False
            else:
                block_depth -= 1
        elif in_html_only_block and ':::' in line:
            block_depth += 1

        # Check for GIF references (markdown or HTML)
        markdown_gif_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]*\.gif[^)]*)\)', re.IGNORECASE)
        html_gif_pattern = re.compile(r'<img[^>]+src=["\']([^"\']*\.gif[^"\']*)["\']', re.IGNORECASE)

        markdown_matches = markdown_gif_pattern.finditer(line)
        html_matches = html_gif_pattern.finditer(line)

        # Check markdown GIF references
        for match in markdown_matches:
            if not in_html_only_block:
                errors.append(ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message='GIF file not wrapped in HTML-only block - will fail in PDF output. Use HTML <img> tag inside ::: {.content-visible when-format="html"}',
                    context=line.strip()[:80]
                ))
            else:
                # Even inside HTML-only block, markdown syntax might not work - warn to use HTML
                errors.append(ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message='GIF uses markdown syntax - use HTML <img> tag instead for better compatibility',
                    context=line.strip()[:80]
                ))

        # Check HTML GIF references
        for match in html_matches:
            if not in_html_only_block:
                errors.append(ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message='GIF file not wrapped in HTML-only block - will fail in PDF output. Wrap in ::: {.content-visible when-format="html"}',
                    context=line.strip()[:80]
                ))

def validate_file(filepath: str):
    """Validate a single file"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Check for common LaTeX patterns
    for pattern_config in latex_patterns:
        pattern = pattern_config['pattern']
        message = pattern_config['message']
        validator = pattern_config.get('validator')

        for match in pattern.finditer(content):
            # If there's a custom validator, use it
            if validator and validator(match.group(0)):
                continue  # Pattern is valid

            # Find line number
            before_match = content[:match.start()]
            line_number = before_match.count('\n') + 1
            line = lines[line_number - 1] if line_number <= len(lines) else ''

            errors.append(ValidationError(
                file=filepath,
                line=line_number,
                message=message,
                context=line.strip()[:80]
            ))

    # Check math delimiters
    check_math_delimiters(content, filepath)

    # Check image paths
    check_image_paths(content, filepath)

    # Check em-dashes
    check_em_dashes(content, filepath)

    # Check GIF references
    check_gif_references(content, filepath)

def main():
    """Main validation function"""
    print('Validating LaTeX in .qmd files...\n')

    # Find all .qmd files
    qmd_files = glob('**/*.qmd', recursive=True)
    # Filter out node_modules, _book, .quarto directories
    qmd_files = [f for f in qmd_files if not any(x in f for x in ['node_modules', '_book', '.quarto'])]
    # Exclude references.qmd from validation
    qmd_files = [f for f in qmd_files if not f.endswith('references.qmd')]

    print(f'Found {len(qmd_files)} .qmd files to validate\n')

    # Validate each file
    for qmd_file in qmd_files:
        validate_file(qmd_file)

    # Report results
    if len(errors) == 0:
        print('No LaTeX errors found!\n')
        sys.exit(0)
    else:
        print(f'Found {len(errors)} LaTeX validation error(s):\n', file=sys.stderr)

        # Group errors by file
        errors_by_file: Dict[str, List[ValidationError]] = {}
        for error in errors:
            if error.file not in errors_by_file:
                errors_by_file[error.file] = []
            errors_by_file[error.file].append(error)

        # Print errors grouped by file
        for file, file_errors in errors_by_file.items():
            print(f'\n{file}:', file=sys.stderr)
            for error in file_errors:
                print(f'   Line {error.line}: {error.message}', file=sys.stderr)
                print(f'   Context: {error.context}', file=sys.stderr)

        print('\nPlease fix the above errors before building the PDF.\n', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
