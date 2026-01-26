#!/usr/bin/env python3
"""
Shared Validation Core Library
==============================

Common validation functions used by:
- .claude/hooks/quick-validate.py (PostToolUse hook)
- scripts/pre-render-validation.py (pre-render validation)

This consolidates duplicate validation logic to ensure consistent behavior
and error messages across all validation entry points.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]


# =============================================================================
# Data Classes
# =============================================================================

class ValidationIssue:
    """Represents a validation issue found in a file."""

    def __init__(
        self,
        file_path: str,
        line: int,
        issue_type: str,
        message: str,
        context: str = "",
        column: Optional[int] = None,
        severity: str = "error"  # "error", "warning", "suggestion"
    ):
        self.file_path = file_path
        self.line = line
        self.column = column
        self.issue_type = issue_type
        self.message = message
        self.context = context
        self.severity = severity

    def __str__(self):
        col_str = f":{self.column}" if self.column else ""
        return f"{self.file_path}:{self.line}{col_str} [{self.issue_type}] {self.message}"

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'type': self.issue_type,
            'line': self.line,
            'column': self.column,
            'message': self.message,
            'context': self.context,
            'severity': self.severity
        }


# =============================================================================
# Path Resolution
# =============================================================================

def get_project_root(start_path: Optional[str] = None) -> Path:
    """Find project root by looking for _quarto.yml or _variables.yml."""
    current = Path(start_path) if start_path else Path.cwd()
    while current != current.parent:
        if (current / '_quarto.yml').exists() or (current / '_variables.yml').exists():
            return current
        current = current.parent
    return Path.cwd()


def resolve_link_path(link_path: str, file_dir: str, project_root: Optional[Path] = None) -> str:
    """
    Resolve a link path to an absolute filesystem path.

    Handles:
    - Relative paths (resolved relative to file_dir)
    - Absolute paths starting with / (resolved from project root)

    Args:
        link_path: The path from the markdown link (may start with / for absolute)
        file_dir: The directory containing the file with the link
        project_root: Project root directory (auto-detected if None)

    Returns:
        Normalized absolute path to the target file
    """
    if project_root is None:
        project_root = get_project_root()

    if link_path.startswith("/"):
        # Absolute path from project root
        return os.path.normpath(str(project_root / link_path[1:]))
    else:
        # Relative path from the file's directory
        return os.path.normpath(os.path.join(file_dir, link_path))


# =============================================================================
# Variable Loading
# =============================================================================

def load_variables_from_yml(variables_file: Optional[Path] = None) -> Set[str]:
    """
    Load variable names from _variables.yml.

    Returns a set of variable names that are defined.
    """
    if variables_file is None:
        variables_file = get_project_root() / '_variables.yml'

    if not variables_file.exists():
        return set()

    variables = set()
    try:
        with open(variables_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract variable names (keys before colons, with or without quotes)
            # Matches: "variable_name": or   variable_name:
            for match in re.finditer(r'^"?([a-z][a-z0-9_]+)"?\s*:', content, re.MULTILINE):
                variables.add(match.group(1))
    except Exception:
        pass

    return variables


# =============================================================================
# Em-Dash Detection
# =============================================================================

EM_DASH_MESSAGE = 'Em-dash found. Replace with parenthesis, comma and space (", "), period, or semicolon as appropriate. Prefer periods and shortened sentences where appropriate.'


def check_em_dashes(content: str, file_path: str) -> List[ValidationIssue]:
    """
    Check for em-dashes which should be replaced with other punctuation.

    Detects ALL em-dashes except those in safe contexts:
    - Code blocks (``` ... ```)
    - Inline code (`...`)
    - URLs
    """
    issues = []
    lines = content.split("\n")
    in_code_block = False

    # Patterns
    em_dash_pattern = re.compile(r"—")
    inline_code_pattern = re.compile(r"`[^`]*—[^`]*`")
    url_pattern = re.compile(r"https?://[^\s]*—[^\s]*")

    for line_index, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Skip if em-dash is inside inline code
        if inline_code_pattern.search(line):
            continue

        # Skip if em-dash is inside a URL
        if url_pattern.search(line):
            continue

        # Find all em-dashes
        for match in em_dash_pattern.finditer(line):
            column = match.start() + 1
            issues.append(ValidationIssue(
                file_path=file_path,
                line=line_index + 1,
                column=column,
                issue_type='em_dash',
                message=EM_DASH_MESSAGE,
                context=line.strip()[:80],
                severity='suggestion'
            ))

    return issues


# =============================================================================
# Variable Validation
# =============================================================================

def check_undefined_variables(
    content: str,
    file_path: str,
    valid_variables: Set[str]
) -> List[ValidationIssue]:
    """
    Check for Quarto variable references that are not defined in _variables.yml.

    Pattern: {{< var variable_name >}}
    """
    if not valid_variables:
        return []

    issues = []
    lines = content.split("\n")

    # Pattern to match Quarto variable references
    var_pattern = re.compile(r"\{\{<\s*var\s+([a-z][a-z0-9_]+)\s*>\}\}")

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if re.match(r"^\s*<!--", line.strip()) or ("<!--" in line and "-->" in line):
            continue

        for match in var_pattern.finditer(line):
            var_name = match.group(1)
            if var_name not in valid_variables:
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line=line_index + 1,
                    issue_type='undefined_variable',
                    message=f"Undefined variable: {{{{< var {var_name} >}}}} - not defined in _variables.yml",
                    context=line.strip()[:80]
                ))

    return issues


# =============================================================================
# Link Validation
# =============================================================================

def check_broken_qmd_links(
    content: str,
    file_path: str,
    project_root: Optional[Path] = None
) -> List[ValidationIssue]:
    """
    Check for broken cross-reference links to .qmd files.

    Matches patterns like: [text](path/to/file.qmd)
    """
    if project_root is None:
        project_root = get_project_root()

    issues = []
    lines = content.split("\n")
    file_dir = os.path.dirname(file_path)

    # Match markdown link syntax to .qmd files
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)#]+\.qmd(?:#[^)]*)?)\)")

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if re.match(r"^\s*<!--", line.strip()):
            continue

        for match in link_pattern.finditer(line):
            # Skip if inside HTML comment on same line
            before_match = line[:match.start()]
            after_match = line[match.end():]
            if "<!--" in before_match and "-->" in after_match:
                continue

            link_path = match.group(2).split("#")[0]  # Remove anchor

            # Skip URLs
            if link_path.startswith("http://") or link_path.startswith("https://"):
                continue

            # Resolve the path
            resolved_path = resolve_link_path(link_path, file_dir, project_root)

            if not os.path.exists(resolved_path):
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line=line_index + 1,
                    issue_type='broken_link',
                    message=f"Broken link: {link_path} (target file not found)",
                    context=line.strip()[:80]
                ))

    return issues


def check_html_extension_links(content: str, file_path: str) -> List[ValidationIssue]:
    """
    Check for links using .html extension instead of .qmd.

    In source files, links should use .qmd extension (Quarto converts them).
    """
    issues = []
    lines = content.split("\n")

    # Pattern for internal links with .html extension
    # Match [text](path.html) or [text](path.html#anchor)
    pattern = re.compile(r'\[([^\]]*)\]\(([^)]*?)\.html(\)?(?:#[^)]*)?\))')

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if re.match(r"^\s*<!--", line.strip()):
            continue

        for match in pattern.finditer(line):
            full_match = match.group(0)
            path_part = match.group(2)

            # Skip external URLs
            if path_part.startswith("http://") or path_part.startswith("https://"):
                continue

            issues.append(ValidationIssue(
                file_path=file_path,
                line=line_index + 1,
                issue_type='html_extension',
                message=f"Link uses .html extension - should use .qmd in source files",
                context=line.strip()[:80],
                severity='warning'
            ))

    return issues


# =============================================================================
# Include Directive Validation
# =============================================================================

def check_broken_includes(
    content: str,
    file_path: str,
    project_root: Optional[Path] = None
) -> List[ValidationIssue]:
    """
    Check for broken Quarto include directives.

    Pattern: {{< include path.qmd >}}
    """
    if project_root is None:
        project_root = get_project_root()

    issues = []
    lines = content.split("\n")
    file_dir = os.path.dirname(file_path)

    # Match Quarto include syntax
    include_pattern = re.compile(r"\{\{<\s*include\s+([^\s>]+)\s*>\}\}")

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if re.match(r"^\s*<!--", line.strip()) or ("<!--" in line and "-->" in line):
            continue

        for match in include_pattern.finditer(line):
            include_path = match.group(1).strip()

            # Skip URLs
            if include_path.startswith("http://") or include_path.startswith("https://"):
                continue

            # Resolve the path
            resolved_path = resolve_link_path(include_path, file_dir, project_root)

            if not os.path.exists(resolved_path):
                issues.append(ValidationIssue(
                    file_path=file_path,
                    line=line_index + 1,
                    issue_type='broken_include',
                    message=f"Broken include: {include_path} (target file not found)",
                    context=line.strip()[:80]
                ))

    return issues


# =============================================================================
# Hardcoded Value Detection
# =============================================================================

def check_hardcoded_values(content: str, file_path: str) -> List[ValidationIssue]:
    """
    Check for obvious hardcoded values that should be variables.

    Detects:
    - Large dollar amounts ($X million/billion/trillion)
    - Specific percentages in prose (not in LaTeX)
    """
    issues = []
    lines = content.split("\n")
    in_code_block = False

    # Patterns for hardcoded values
    hardcoded_patterns = [
        # Large dollar amounts
        (r'\$(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(?:trillion|billion|million)',
         'Consider using a variable for this dollar amount'),
        # Specific percentages in text (not in LaTeX)
        (r'(?<!\$)\b(\d{1,2}(?:\.\d+)?)\s*%(?![\s}]*>)',
         'Consider using a variable for this percentage'),
    ]

    for line_index, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        for pattern, message in hardcoded_patterns:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                start = match.start()

                # Skip if inside a {{< var >}} block
                context_before = line[max(0, start-50):start]
                if '{{< var' in context_before and '>}}' not in context_before:
                    continue

                # Skip if inside LaTeX blocks
                if '$' in line[max(0, start-5):start]:
                    continue

                issues.append(ValidationIssue(
                    file_path=file_path,
                    line=line_index + 1,
                    issue_type='hardcoded_value',
                    message=message,
                    context=line.strip()[:80],
                    severity='suggestion'
                ))

    return issues


# =============================================================================
# Fuzzy Variable Matching
# =============================================================================

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def fuzzy_match_variable(
    name: str,
    valid_vars: Set[str],
    threshold: float = 0.85
) -> Optional[Tuple[str, float]]:
    """
    Find closest matching variable name using fuzzy matching.

    Returns (best_match, confidence) or None if no match above threshold.
    """
    if not valid_vars or not name:
        return None

    best_match = None
    best_score = 0.0

    for var in valid_vars:
        # Skip if lengths are too different
        if abs(len(var) - len(name)) > max(len(var), len(name)) * 0.3:
            continue

        distance = levenshtein_distance(name.lower(), var.lower())
        max_len = max(len(name), len(var))
        similarity = 1 - (distance / max_len)

        if similarity > best_score:
            best_score = similarity
            best_match = var

    if best_match and best_score >= threshold:
        return (best_match, best_score)

    return None


def suggest_variable_typos(
    content: str,
    file_path: str,
    valid_variables: Set[str],
    threshold: float = 0.85
) -> List[ValidationIssue]:
    """
    Find variable references with typos and suggest corrections.

    Returns list of suggestions for undefined variables that have close matches.
    """
    if not valid_variables:
        return []

    suggestions = []
    var_pattern = re.compile(r'\{\{<\s*var\s+([a-z][a-z0-9_]+)\s*>\}\}')

    for match in var_pattern.finditer(content):
        var_name = match.group(1)

        # Skip if variable exists
        if var_name in valid_variables:
            continue

        # Try to find a fuzzy match
        result = fuzzy_match_variable(var_name, valid_variables, threshold)
        if result:
            suggested_var, confidence = result
            line_num = content[:match.start()].count('\n') + 1
            suggestions.append(ValidationIssue(
                file_path=file_path,
                line=line_num,
                issue_type='variable_typo',
                message=f'Did you mean "{suggested_var}"? ({round(confidence * 100)}% match)',
                context=f'{{{{< var {var_name} >}}}}',
                severity='suggestion'
            ))

    return suggestions


# =============================================================================
# Convenience Functions
# =============================================================================

def run_quick_validation(
    content: str,
    file_path: str,
    valid_variables: Optional[Set[str]] = None,
    project_root: Optional[Path] = None
) -> List[ValidationIssue]:
    """
    Run quick validation checks suitable for PostToolUse hooks.

    Checks:
    - Undefined variables
    - Variable typos (suggestions)
    - Broken .qmd links
    - Em-dashes (suggestions)
    - Hardcoded values (suggestions)
    """
    if valid_variables is None:
        valid_variables = load_variables_from_yml()

    if project_root is None:
        project_root = get_project_root()

    issues = []

    # Core checks
    issues.extend(check_undefined_variables(content, file_path, valid_variables))
    issues.extend(check_broken_qmd_links(content, file_path, project_root))

    # Suggestions
    issues.extend(check_em_dashes(content, file_path))
    issues.extend(suggest_variable_typos(content, file_path, valid_variables))

    # Limit hardcoded value suggestions to avoid noise
    hardcoded = check_hardcoded_values(content, file_path)
    issues.extend(hardcoded[:3])

    return issues
