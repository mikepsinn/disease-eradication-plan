#!/usr/bin/env python3
"""
Auto-Fix Core Library
=====================

Deterministic, safe auto-fixes for QMD files in PostToolUse hooks.

Safe fixes (100% confidence, deterministic):
- Curly quotes -> straight quotes
- .html extensions -> .qmd in internal links

Suggestions (require review):
- Em-dashes -> various punctuation options
- Variable typos with fuzzy matching

Uses shared validation_core library for common functions.
"""

import sys
import os
import re
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set, Optional

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

# Add project root to path for imports
def _get_project_root() -> Path:
    current = Path.cwd()
    while current != current.parent:
        if (current / '_quarto.yml').exists() or (current / '_variables.yml').exists():
            return current
        current = current.parent
    return Path.cwd()

PROJECT_ROOT = _get_project_root()
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))

# Import from shared validation library
try:
    from lib.validation_core import (
        get_project_root,
        load_variables_from_yml,
        levenshtein_distance,
        fuzzy_match_variable,
        EM_DASH_MESSAGE
    )
    VALIDATION_CORE_AVAILABLE = True
except ImportError:
    VALIDATION_CORE_AVAILABLE = False
    # Fallback implementations
    def get_project_root() -> Path:
        return PROJECT_ROOT

    def load_variables_from_yml() -> Set[str]:
        variables_file = PROJECT_ROOT / '_variables.yml'
        if not variables_file.exists():
            return set()
        variables = set()
        try:
            with open(variables_file, 'r', encoding='utf-8') as f:
                content = f.read()
                for match in re.finditer(r'^"?([a-z][a-z0-9_]+)"?\s*:', content, re.MULTILINE):
                    variables.add(match.group(1))
        except Exception:
            pass
        return variables

    def levenshtein_distance(s1: str, s2: str) -> int:
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

    def fuzzy_match_variable(name: str, valid_vars: Set[str], threshold: float = 0.85) -> Optional[Tuple[str, float]]:
        if not valid_vars or not name:
            return None
        best_match = None
        best_score = 0.0
        for var in valid_vars:
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

    EM_DASH_MESSAGE = 'Em-dash found. Replace with parenthesis, comma and space (", "), period, or semicolon as appropriate. Prefer periods and shortened sentences where appropriate.'


@dataclass
class FixResult:
    """Result of applying fixes to content."""
    fixed: List[Dict] = field(default_factory=list)
    suggested: List[Dict] = field(default_factory=list)


def load_autofix_config() -> Dict:
    """Load autofix configuration from autofix-config.json."""
    root = get_project_root()
    config_file = root / '.claude' / 'hooks' / 'autofix-config.json'

    default_config = {
        "enabled": True,
        "rules": {
            "em_dashes": "suggest",
            "curly_quotes": "auto",
            "html_extensions": "auto",
            "variable_typos": "suggest"
        },
        "confidence_threshold": 0.85
    }

    if not config_file.exists():
        return default_config

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            merged = default_config.copy()
            merged.update(config)
            if 'rules' in config:
                merged['rules'] = {**default_config['rules'], **config['rules']}
            return merged
    except Exception:
        return default_config


# Alias for backward compatibility
def load_valid_variables() -> Set[str]:
    """Load variable names from _variables.yml."""
    return load_variables_from_yml()


def suggest_em_dash_fixes(content: str) -> List[Dict]:
    """Find em-dashes and suggest replacements.

    Em-dashes should be replaced with parenthesis, comma and space, period,
    or semicolon as appropriate. Prefer periods and shortened sentences.

    Returns list of suggestions (does not modify content).
    """
    suggestions = []

    # Pattern for em-dash (U+2014)
    pattern = r'\u2014'

    for match in re.finditer(pattern, content):
        line_num = content[:match.start()].count('\n') + 1
        # Get context around the em-dash
        start = max(0, match.start() - 30)
        end = min(len(content), match.end() + 30)
        context = content[start:end].replace('\n', ' ')

        suggestions.append({
            'type': 'em_dash',
            'line': line_num,
            'context': f'...{context}...',
            'message': EM_DASH_MESSAGE
        })

    return suggestions


def fix_curly_quotes(content: str) -> Tuple[str, List[Dict]]:
    """Replace curly quotes with straight quotes.

    Returns (modified_content, list of fixes applied).
    """
    fixes = []

    # Curly quote patterns
    replacements = [
        ('\u201c', '"'),  # Left double quote
        ('\u201d', '"'),  # Right double quote
        ('\u2018', "'"),  # Left single quote
        ('\u2019', "'"),  # Right single quote (also apostrophe)
    ]

    for curly, straight in replacements:
        for match in re.finditer(re.escape(curly), content):
            line_num = content[:match.start()].count('\n') + 1
            fixes.append({
                'type': 'curly_quote',
                'line': line_num,
                'original': curly,
                'replacement': straight,
                'message': f'Replaced curly quote with straight quote'
            })

    modified = content
    for curly, straight in replacements:
        modified = modified.replace(curly, straight)

    return modified, fixes


def fix_html_extensions(content: str) -> Tuple[str, List[Dict]]:
    """Replace .html) with .qmd) in internal links.

    Returns (modified_content, list of fixes applied).
    """
    fixes = []

    # Pattern for internal links with .html extension
    # Match [text](path.html) or [text](path.html#anchor)
    pattern = r'(\[[^\]]*\]\([^)]*?)\.html(\)?(?:#[^)]*)?\))'

    for match in re.finditer(pattern, content):
        line_num = content[:match.start()].count('\n') + 1
        fixes.append({
            'type': 'html_extension',
            'line': line_num,
            'original': match.group(0),
            'replacement': match.group(1) + '.qmd' + match.group(2),
            'message': 'Changed .html to .qmd in internal link'
        })

    modified = re.sub(pattern, r'\1.qmd\2', content)
    return modified, fixes


def suggest_variable_fixes(content: str, valid_vars: Set[str], threshold: float = 0.85) -> List[Dict]:
    """Find variable references with typos and suggest corrections.

    Returns list of suggestions (does not modify content).
    """
    suggestions = []

    # Pattern for {{< var name >}}
    var_pattern = r'\{\{<\s*var\s+([a-z][a-z0-9_]+)\s*>\}\}'

    for match in re.finditer(var_pattern, content):
        var_name = match.group(1)

        # Skip if variable exists
        if var_name in valid_vars:
            continue

        # Try to find a fuzzy match
        result = fuzzy_match_variable(var_name, valid_vars, threshold)
        if result:
            suggested_var, confidence = result
            line_num = content[:match.start()].count('\n') + 1
            suggestions.append({
                'type': 'variable_typo',
                'line': line_num,
                'variable': var_name,
                'suggested': suggested_var,
                'confidence': round(confidence, 3),
                'message': f'Did you mean "{suggested_var}"? ({round(confidence * 100)}% match)'
            })

    return suggestions


def apply_safe_fixes(content: str, file_path: str, config: Optional[Dict] = None) -> Tuple[str, FixResult]:
    """Apply all safe, deterministic fixes to content.

    Args:
        content: File content to fix
        file_path: Path to file (for context)
        config: Autofix configuration (loads from settings.json if None)

    Returns:
        (modified_content, FixResult with applied fixes and suggestions)
    """
    if config is None:
        config = load_autofix_config()

    result = FixResult()
    modified = content

    if not config.get('enabled', True):
        return content, result

    rules = config.get('rules', {})
    threshold = config.get('confidence_threshold', 0.85)

    # Suggest em-dash fixes (context-dependent, not auto-fixable)
    if rules.get('em_dashes') in ('suggest', 'auto'):
        suggestions = suggest_em_dash_fixes(modified)
        result.suggested.extend(suggestions)

    # Apply curly quotes fix
    if rules.get('curly_quotes') == 'auto':
        modified, fixes = fix_curly_quotes(modified)
        result.fixed.extend(fixes)

    # Apply HTML extension fix
    if rules.get('html_extensions') == 'auto':
        modified, fixes = fix_html_extensions(modified)
        result.fixed.extend(fixes)

    # Suggest variable typo fixes (never auto-apply)
    if rules.get('variable_typos') in ('suggest', 'auto'):
        valid_vars = load_valid_variables()
        suggestions = suggest_variable_fixes(modified, valid_vars, threshold)
        result.suggested.extend(suggestions)

    return modified, result


if __name__ == '__main__':
    # Test the module
    test_content = '''
This is a test with em-dash \u2014 and "curly quotes".
Also a link: [test](../path/to/file.html)
And a variable: {{< var treaty_annual_fundng >}}
'''

    modified, result = apply_safe_fixes(test_content, 'test.qmd')
    print("Fixed:", len(result.fixed))
    for fix in result.fixed:
        print(f"  - {fix['type']}: {fix['message']}")
    print("Suggested:", len(result.suggested))
    for sug in result.suggested:
        print(f"  - {sug['type']}: {sug['message']}")
    print("\nModified content:")
    print(modified)
