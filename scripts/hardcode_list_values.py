#!/usr/bin/env python3
"""
Hardcode inline Python values in markdown list items.

This script replaces inline Python expressions like `{python} var_name` with their
actual hardcoded values when they appear in markdown list items.

This is necessary because Quarto doesn't evaluate inline Python in list contexts.
"""

import re
import sys
from pathlib import Path

# Add economic_parameters to path
# Find project root
project_root = Path.cwd()
if project_root.name != 'decentralized-institutes-of-health':
    while project_root.name != 'decentralized-institutes-of-health' and project_root.parent != project_root:
        project_root = project_root.parent
sys.path.insert(0, str(project_root))
from economic_parameters import *

# Build VALUE_MAP dynamically from economic_parameters module
VALUE_MAP = {}
all_vars = dir()
for var in all_vars:
    if not var.startswith('_'):
        try:
            value = eval(var)
            # Include formatted variables and numeric constants
            if '_formatted' in var or (var.isupper() and isinstance(value, (int, float))):
                VALUE_MAP[var] = str(value)
        except:
            pass

print(f"Loaded {len(VALUE_MAP)} variables from economic_parameters.py\n")

def find_qmd_files():
    """Find all .qmd files in brain/book directory and root"""
    files = list(Path('brain/book').rglob('*.qmd'))
    # Also include root-level .qmd files
    files.extend(list(Path('.').glob('*.qmd')))
    return files

def replace_inline_python_in_lists(content):
    """Replace inline Python expressions in markdown (lists and paragraphs)"""
    lines = content.split('\n')
    modified = False

    for i, line in enumerate(lines):
        # Skip code blocks and frontmatter
        if line.strip().startswith('```') or line.strip().startswith('---'):
            continue

        # Find all inline Python expressions in this line
        pattern = r'`\{python\}\s+([^`]+)`'

        def replace_match(match):
            nonlocal modified
            var_name = match.group(1).strip()
            if var_name in VALUE_MAP:
                modified = True
                value = VALUE_MAP[var_name]
                print(f"  Replacing `{{python}} {var_name}` with {value}")
                return value
            else:
                print(f"  WARNING: Unknown variable: {var_name}")
                return match.group(0)  # Return original if not found

        lines[i] = re.sub(pattern, replace_match, line)

    return '\n'.join(lines), modified

def main():
    qmd_files = find_qmd_files()
    print(f"Found {len(qmd_files)} .qmd files to process\n")

    total_files_modified = 0
    total_replacements = 0

    for file_path in qmd_files:
        print(f"Processing {file_path}...")

        try:
            content = file_path.read_text(encoding='utf-8')
            new_content, modified = replace_inline_python_in_lists(content)

            if modified:
                file_path.write_text(new_content, encoding='utf-8')
                total_files_modified += 1
                print(f"  [OK] Modified")
            else:
                print(f"  - No changes needed")
        except Exception as e:
            print(f"  [ERROR] Error: {e}")

        print()

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Files modified: {total_files_modified}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
