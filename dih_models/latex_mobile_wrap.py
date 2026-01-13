#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX Mobile-Friendly Wrapping Utilities
=========================================

Converts wide LaTeX equations to mobile-responsive format using aligned environments.

Functions:
- wrap_latex_for_mobile: Convert single long equation to wrapped format
- process_all_latex_variables: Process _variables.yml and wrap long equations

Usage:
    from dih_models.latex_mobile_wrap import wrap_latex_for_mobile

    # Wrap a single equation
    wrapped = wrap_latex_for_mobile(long_latex, max_width=60)

    # Or run directly to process _variables.yml:
    python -m dih_models.latex_mobile_wrap
"""

from __future__ import annotations

import re
from typing import Optional


def _split_at_top_level_equals(latex: str) -> list[str]:
    r"""
    Split LaTeX string on '=' signs, but only at the top level.

    Does NOT split on '=' inside braces (e.g., \sum_{t=1} stays intact).

    Args:
        latex: LaTeX equation string

    Returns:
        List of parts split by top-level '=' signs
    """
    parts = []
    current = []
    brace_depth = 0
    i = 0

    while i < len(latex):
        char = latex[i]

        if char == '{':
            brace_depth += 1
            current.append(char)
        elif char == '}':
            brace_depth -= 1
            current.append(char)
        elif char == '=' and brace_depth == 0:
            # Top-level equals sign - split here
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(char)

        i += 1

    # Don't forget the last part
    if current:
        parts.append(''.join(current).strip())

    return parts


def wrap_latex_for_mobile(latex: str, max_width: int = 60) -> str:
    """
    Convert a wide LaTeX equation to mobile-friendly wrapped format.

    Uses \\begin{aligned} environment with line breaks at logical points:
    - After = signs (main equation structure)
    - After + signs in long sums
    - After \\times in long products

    Args:
        latex: LaTeX equation string (without $$ delimiters)
        max_width: Target maximum width per line (approximate)

    Returns:
        Wrapped LaTeX string using aligned environment
    """
    latex = latex.strip()

    # If already using aligned environment, wrap WITHIN it
    if '\\begin{aligned}' in latex:
        return _wrap_within_aligned(latex, max_width)
    
    # Skip other environments (array, matrix, etc.) - too complex
    if '\\begin{' in latex:
        return latex

    # Skip short equations
    if len(latex) <= max_width:
        return latex

    # Strategy 1: Break on multiple = signs (common pattern: X = A + B = result)
    # Split by = but ONLY at top level (not inside braces like \sum_{t=1})
    equals_parts = _split_at_top_level_equals(latex)

    if len(equals_parts) >= 2:
        # Use aligned environment for multi-step equations
        lines = []
        for i, part in enumerate(equals_parts):
            part = part.strip()
            if i == 0:
                # First part (LHS)
                lines.append(part)
            else:
                # Subsequent parts get & = alignment
                # Check if this part is long and contains + or \\times
                if len(part) > max_width:
                    # Try to break long sums/products within this part
                    wrapped_part = _break_long_expression(part, max_width)
                    lines.append(f"&= {wrapped_part}")
                else:
                    lines.append(f"&= {part}")

        # Join with line breaks
        wrapped = " \\\\\n".join(lines)
        return f"\\begin{{aligned}}\n{wrapped}\n\\end{{aligned}}"

    # Strategy 2: Break long sums (no = signs)
    if '+' in latex and len(latex) > max_width:
        wrapped = _break_long_expression(latex, max_width)
        if '\n' in wrapped:
            return f"\\begin{{aligned}}\n{wrapped}\n\\end{{aligned}}"
        return wrapped

    # Strategy 3: Break long products
    if '\\times' in latex and len(latex) > max_width:
        wrapped = _break_long_expression(latex, max_width, break_on='\\times')
        if '\n' in wrapped:
            return f"\\begin{{aligned}}\n{wrapped}\n\\end{{aligned}}"
        return wrapped

    # Can't wrap effectively - return original
    return latex


def _split_at_top_level_operator(expr: str, operator: str) -> list[str]:
    """
    Split expression on operator, but only at top level (not inside braces).

    Args:
        expr: Expression to split
        operator: Operator to split on ('+' or '\\times')

    Returns:
        List of parts
    """
    parts = []
    current = []
    brace_depth = 0
    i = 0

    while i < len(expr):
        # Check for multi-char operator like \times
        if operator == '\\times' and expr[i:i+6] == '\\times' and brace_depth == 0:
            parts.append(''.join(current).strip())
            current = []
            i += 6
            # Skip whitespace after operator
            while i < len(expr) and expr[i] in ' \t':
                i += 1
            continue

        char = expr[i]

        if char == '{':
            brace_depth += 1
            current.append(char)
        elif char == '}':
            brace_depth -= 1
            current.append(char)
        elif char == '+' and operator == '+' and brace_depth == 0:
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(char)

        i += 1

    if current:
        parts.append(''.join(current).strip())

    return parts


def _break_long_expression(expr: str, max_width: int, break_on: str = '+') -> str:
    r"""
    Break a long expression at + or \\times operators.

    Args:
        expr: Expression to break
        max_width: Target width per line
        break_on: Operator to break on ('+' or '\\times')

    Returns:
        Expression with line breaks (using \\\\ and &)
    """
    # Determine the split pattern - use brace-aware splitting
    if break_on == '+':
        parts = _split_at_top_level_operator(expr, '+')
        joiner = ' + '
        continuation = '&\\quad + '
    elif break_on == '\\times':
        parts = _split_at_top_level_operator(expr, '\\times')
        joiner = ' \\times '
        continuation = '&\\quad \\times '
    else:
        return expr

    if len(parts) <= 1:
        return expr

    # Build lines respecting max_width
    lines = []
    current_line = parts[0]

    for part in parts[1:]:
        # Check if adding this part would exceed width
        test_line = current_line + joiner + part
        if len(test_line) <= max_width:
            current_line = test_line
        else:
            # Start new line
            lines.append(current_line)
            current_line = continuation.lstrip('&') + part

    # Don't forget last line
    lines.append(current_line)

    if len(lines) == 1:
        return lines[0]

    # Format for aligned environment
    result = lines[0] + " \\\\\n"
    for line in lines[1:-1]:
        result += "&" + line.lstrip() + " \\\\\n"
    result += "&" + lines[-1].lstrip()

    return result


def _wrap_within_aligned(latex: str, max_width: int) -> str:
    r"""
    Wrap long lines WITHIN an existing aligned environment.

    The generate_expanded_latex function produces equations with \begin{aligned}
    but individual lines (especially "where" clauses) can still be very long.
    This function breaks those long lines at + signs.

    Args:
        latex: LaTeX string containing \begin{aligned}...\end{aligned}
        max_width: Target maximum width per line

    Returns:
        LaTeX with long lines broken into multiple lines
    """
    # Extract content between \begin{aligned} and \end{aligned}
    # Also capture any prefix (like $$\n) and suffix (like \n$$)
    match = re.search(r'(.*?)(\\begin\{aligned\})(.*?)(\\end\{aligned\})(.*)', latex, re.DOTALL)
    if not match:
        return latex

    prefix = match.group(1)      # e.g., "$$\n"
    begin_tag = match.group(2)   # "\begin{aligned}"
    content = match.group(3)      # content inside aligned
    end_tag = match.group(4)     # "\end{aligned}"
    suffix = match.group(5)      # e.g., "\n$$"

    # Split into lines (aligned environment uses \\ for line breaks)
    # Need to handle both \\ and \\[spacing] variants
    lines = re.split(r'\\\\(?:\[[\d.]+em\])?', content)

    wrapped_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this line is too long
        # Strip LaTeX commands for length estimation
        plain_length = len(re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', 'X', line))

        if plain_length <= max_width:
            wrapped_lines.append(line)
            continue

        # Line is too long - try to break it
        # Common pattern: "\\text{where } X = A + B + C + D = result"
        # We want to break after A + B and continue with + C + D

        # Check if it's a "where" clause with a sum
        if '+' in line and plain_length > max_width:
            wrapped_line = _wrap_single_aligned_line(line, max_width)
            wrapped_lines.append(wrapped_line)
        else:
            # Can't wrap effectively, keep as-is
            wrapped_lines.append(line)

    # Reconstruct the aligned environment
    # Use \\[0.5em] for spacing between major lines
    result_content = " \\\\[0.5em]\n".join(wrapped_lines)
    result = f"{prefix}{begin_tag}\n{result_content}\n{end_tag}{suffix}"

    return result


def _wrap_single_aligned_line(line: str, max_width: int) -> str:
    r"""
    Wrap a single line from an aligned environment that contains sums.

    Handles patterns like:
    - "\\text{where } X = A + B + C = result"
    - "X &= A + B + C = result"

    Args:
        line: Single line from aligned environment
        max_width: Target width

    Returns:
        Wrapped line with continuation markers
    """
    # Preserve leading alignment markers and "where"
    prefix_match = re.match(r'^(&?\s*(?:\\text\{where\s*\}\s*)?)', line)
    prefix = prefix_match.group(1) if prefix_match else ""
    rest = line[len(prefix):]

    # Find the equation structure: LHS = middle terms = RHS
    # Split on top-level = signs
    parts = _split_at_top_level_equals(rest)

    if len(parts) < 2:
        return line  # Not an equation, return as-is

    # Check which part is long (usually the middle with many + terms)
    wrapped_parts = []
    for i, part in enumerate(parts):
        part = part.strip()
        part_plain_len = len(re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', 'X', part))

        if part_plain_len > max_width and '+' in part:
            # This part needs wrapping
            sub_parts = _split_at_top_level_operator(part, '+')
            if len(sub_parts) > 2:
                # Break into groups of 2-3 terms
                grouped_parts = []
                current_group = []
                current_len = 0

                for sp in sub_parts:
                    sp_len = len(re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', 'X', sp))
                    if current_len + sp_len + 3 > max_width and current_group:
                        grouped_parts.append(' + '.join(current_group))
                        current_group = [sp]
                        current_len = sp_len
                    else:
                        current_group.append(sp)
                        current_len += sp_len + 3  # +3 for " + "

                if current_group:
                    grouped_parts.append(' + '.join(current_group))

                if len(grouped_parts) > 1:
                    # Join groups with line continuation
                    wrapped_part = grouped_parts[0]
                    for gp in grouped_parts[1:]:
                        wrapped_part += " \\\\\n&\\quad + " + gp
                    wrapped_parts.append(wrapped_part)
                else:
                    wrapped_parts.append(part)
            else:
                wrapped_parts.append(part)
        else:
            wrapped_parts.append(part)

    # Reconstruct the equation
    # Handle first part specially (may have prefix)
    result = prefix + wrapped_parts[0]
    for wp in wrapped_parts[1:]:
        # Check if this part contains line breaks
        if '\n' in wp:
            result += " = " + wp
        else:
            result += " = " + wp

    return result


def estimate_rendered_width(latex: str) -> int:
    """
    Estimate the rendered width of a LaTeX expression.

    This is approximate - LaTeX commands like \\frac take less space
    than their character count suggests.

    Args:
        latex: LaTeX string

    Returns:
        Estimated width in "characters"
    """
    # Remove LaTeX commands (they render smaller than their text length)
    cleaned = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', lambda m: 'X' * min(len(m.group(0))//3, 5), latex)
    # Remove braces
    cleaned = re.sub(r'[{}]', '', cleaned)
    return len(cleaned)


def process_variables_yml(
    input_path: str = "_variables.yml",
    output_path: Optional[str] = None,
    max_width: int = 60,
    dry_run: bool = False
) -> dict:
    """
    Process _variables.yml and wrap all long LaTeX equations.

    Args:
        input_path: Path to input _variables.yml
        output_path: Path to write output (None = overwrite input)
        max_width: Target maximum width per line
        dry_run: If True, don't write output, just return stats

    Returns:
        Dict with statistics: {'total': N, 'wrapped': M, 'unchanged': K}
    """
    import yaml

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML preserving structure
    # We need to process the raw text to preserve formatting

    stats = {'total': 0, 'wrapped': 0, 'unchanged': 0, 'examples': []}

    # Find all _latex variables
    # Pattern: "name_latex": "$$\n...content...\n$$"
    def wrap_latex_match(match):
        name = match.group(1)
        full_value = match.group(2)

        stats['total'] += 1

        # Extract content between $$ markers
        inner_match = re.search(r'\$\$\\n(.+?)\\n\$\$', full_value, re.DOTALL)
        if not inner_match:
            # Try without \\n escaping
            inner_match = re.search(r'\$\$\n(.+?)\n\$\$', full_value, re.DOTALL)

        if not inner_match:
            stats['unchanged'] += 1
            return match.group(0)

        inner_latex = inner_match.group(1)
        # Unescape the LaTeX
        inner_latex = inner_latex.replace('\\n', '\n').replace('\\"', '"')

        # Check if needs wrapping
        if len(inner_latex.replace('\n', '')) <= max_width:
            stats['unchanged'] += 1
            return match.group(0)

        # Wrap it
        wrapped = wrap_latex_for_mobile(inner_latex, max_width)

        if wrapped == inner_latex:
            stats['unchanged'] += 1
            return match.group(0)

        stats['wrapped'] += 1
        if len(stats['examples']) < 3:
            stats['examples'].append({
                'name': name,
                'before': inner_latex[:60] + '...',
                'after': wrapped[:80] + '...'
            })

        # Re-escape for YAML
        wrapped_escaped = wrapped.replace('\n', '\\n').replace('"', '\\"')
        new_value = f'$$\\n{wrapped_escaped}\\n$$'

        return f'"{name}": "{new_value}"'

    # Process all _latex entries
    pattern = r'"(\w+_latex)": "((?:[^"\\]|\\.)*)"'
    new_content = re.sub(pattern, wrap_latex_match, content)

    if not dry_run and output_path:
        with open(output_path or input_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)

    return stats


if __name__ == "__main__":
    import sys

    # Set UTF-8 encoding for stdout on Windows
    if sys.platform == 'win32':
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

    print("LaTeX Mobile Wrapping Utility")
    print("=" * 40)
    print()

    # Run dry-run first to show stats
    stats = process_variables_yml(dry_run=True, max_width=60)

    print(f"Total _latex variables: {stats['total']}")
    print(f"Would wrap: {stats['wrapped']}")
    print(f"Unchanged: {stats['unchanged']}")
    print()

    if stats['examples']:
        print("Example transformations:")
        for ex in stats['examples']:
            print(f"\n{ex['name']}:")
            print(f"  Before: {ex['before']}")
            print(f"  After:  {ex['after']}")

    print()
    print("To apply changes, run:")
    print("  python -c \"from dih_models.latex_mobile_wrap import process_variables_yml; process_variables_yml(dry_run=False)\"")
