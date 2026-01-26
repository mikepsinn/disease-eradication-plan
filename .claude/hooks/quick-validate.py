#!/usr/bin/env python3
"""
Quick Validation Hook for Claude Code PostToolUse
=================================================

Runs after Edit|Write operations on *.qmd files.
Performs fast validation checks and auto-fixes, returning results as JSON.

Auto-fixes (deterministic, 100% safe):
- Curly quotes -> straight quotes
- .html extensions -> .qmd in internal links

Suggestions (require human judgment):
- Em-dashes -> various punctuation options
- Variable typos with fuzzy match corrections

Detection (reported but not auto-fixed):
- Broken variable references ({{< var unknown_var >}})
- Broken internal links (paths that don't exist)
- Obvious hardcoded values that match known parameters

Usage:
  python .claude/hooks/quick-validate.py <file_path>

Exit codes:
  0 - No issues found (or file is not a QMD)
  1 - Issues found or fixes applied (printed to stdout as JSON)
"""

import sys
import os
import json
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

# Add project root to path for imports
def _get_project_root():
    current = Path(os.getcwd())
    while current != current.parent:
        if (current / '_quarto.yml').exists() or (current / '_variables.yml').exists():
            return current
        current = current.parent
    return Path(os.getcwd())

PROJECT_ROOT = _get_project_root()
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))

# Import shared validation library
try:
    from lib.validation_core import (
        get_project_root,
        load_variables_from_yml,
        check_undefined_variables,
        check_broken_qmd_links,
        check_hardcoded_values,
        suggest_variable_typos,
        check_em_dashes,
        ValidationIssue
    )
    VALIDATION_CORE_AVAILABLE = True
except ImportError:
    VALIDATION_CORE_AVAILABLE = False

# Import autofix core (same directory) for auto-fix functionality
try:
    from autofix_core import apply_safe_fixes, load_autofix_config
except ImportError:
    # Fallback if module not found
    def apply_safe_fixes(content, file_path, config=None):
        class FixResult:
            fixed = []
            suggested = []
        return content, FixResult()

    def load_autofix_config():
        return {"enabled": False}


def validate_qmd_file(file_path):
    """Run all validations on a QMD file, applying safe fixes first.

    Returns dict with:
    - fixed: list of auto-applied fixes
    - suggested: list of suggested fixes (em-dashes, variable typos)
    - issues: list of detected issues
    """
    result = {
        'fixed': [],
        'suggested': [],
        'issues': []
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result['issues'] = [{'type': 'error', 'message': f'Could not read file: {e}'}]
        return result

    # Load autofix config and apply safe fixes
    config = load_autofix_config()

    if config.get('enabled', True):
        modified_content, fix_result = apply_safe_fixes(content, file_path, config)

        # Write back if fixes were applied
        if fix_result.fixed:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                content = modified_content
                result['fixed'] = fix_result.fixed
            except Exception as e:
                result['issues'].append({
                    'type': 'error',
                    'message': f'Could not write fixes: {e}'
                })

        # Add suggestions from autofix (em-dashes, variable typos)
        result['suggested'] = fix_result.suggested

    # Use shared validation library if available
    if VALIDATION_CORE_AVAILABLE:
        project_root = get_project_root()
        valid_variables = load_variables_from_yml()

        # Run detection checks using shared library
        for issue in check_undefined_variables(content, file_path, valid_variables):
            result['issues'].append(issue.to_dict())

        for issue in check_broken_qmd_links(content, file_path, project_root):
            result['issues'].append(issue.to_dict())

        # Hardcoded value check - limit to avoid noise
        hardcoded_issues = check_hardcoded_values(content, file_path)
        for issue in hardcoded_issues[:3]:
            result['issues'].append(issue.to_dict())
        if len(hardcoded_issues) > 3:
            result['issues'].append({
                'type': 'info',
                'message': f'... and {len(hardcoded_issues) - 3} more potential hardcoded values'
            })
    else:
        # Fallback to basic checks if shared library not available
        result['issues'].append({
            'type': 'warning',
            'message': 'Shared validation library not available - running limited checks'
        })

    return result


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

    validation_result = validate_qmd_file(file_path)

    # Check if there's anything to report
    has_fixes = len(validation_result.get('fixed', [])) > 0
    has_suggestions = len(validation_result.get('suggested', [])) > 0
    has_issues = len(validation_result.get('issues', [])) > 0

    if not (has_fixes or has_suggestions or has_issues):
        sys.exit(0)

    # Output result as JSON for Claude to process
    output = {
        'file': file_path,
        'fixedCount': len(validation_result.get('fixed', [])),
        'fixed': validation_result.get('fixed', []),
        'suggestCount': len(validation_result.get('suggested', [])),
        'suggested': validation_result.get('suggested', []),
        'issueCount': len(validation_result.get('issues', [])),
        'issues': validation_result.get('issues', [])
    }

    print(json.dumps(output, indent=2))
    sys.exit(1 if has_issues else 0)


if __name__ == '__main__':
    main()
