#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find all references to "85%" in the project for updating to 86.1%

This helps ensure all clinical trial exclusion percentages are updated
to match the sourced data from Zimmerman et al. (2015).
"""
import sys
from pathlib import Path
import re

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def find_85_percent_references(root_dir: Path):
    """Find all references to 85% in markdown and QMD files."""

    # Patterns to search for
    patterns = [
        r'85\s*%',           # "85%" or "85 %"
        r'85\s*percent',      # "85 percent"
        r'eighty-five\s*%',   # "eighty-five%"
    ]

    results = []

    # File patterns to search
    file_patterns = ['**/*.qmd', '**/*.md', '**/*.json']

    for pattern in file_patterns:
        try:
            for file_path in root_dir.glob(pattern):
                # Skip if symlink or doesn't exist
                if file_path.is_symlink() or not file_path.exists():
                    continue

                # Skip generated files and certain directories
                if any(skip in str(file_path) for skip in [
                    '_book/', 'node_modules/', '.git/', 'venv/', '_variables.yml',
                    'OUTLINE-GENERATED', '.venv/'
                ]):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    for line_num, line in enumerate(lines, 1):
                        for search_pattern in patterns:
                            if re.search(search_pattern, line, re.IGNORECASE):
                                results.append({
                                    'file': str(file_path.relative_to(root_dir)),
                                    'line': line_num,
                                    'content': line.strip()
                                })
                                break  # Only report once per line

                except Exception as e:
                    print(f"[WARN] Could not read {file_path}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Error globbing {pattern}: {e}", file=sys.stderr)

    return results

def main():
    project_root = Path(__file__).parent.parent.absolute()

    print("[*] Searching for 85% references...")
    print()

    results = find_85_percent_references(project_root)

    if not results:
        print("[OK] No 85% references found!")
        return

    print(f"[FOUND] {len(results)} references to 85%:")
    print()

    # Group by file
    by_file = {}
    for result in results:
        file_path = result['file']
        if file_path not in by_file:
            by_file[file_path] = []
        by_file[file_path].append(result)

    # Print grouped results
    for file_path in sorted(by_file.keys()):
        print(f"File: {file_path}")
        for result in by_file[file_path]:
            print(f"  Line {result['line']}: {result['content'][:100]}")
        print()

    print("[*] Update strategy:")
    print("    1. Replace '85%' with '86.1%' (sourced from Zimmerman et al., 2015)")
    print("    2. Add hyperlink: [86.1% excluded](../references.qmd#antidepressant-trial-exclusion-rates)")
    print("    3. Benefit: Unique percentage makes future searches easier")
    print()
    print(f"[OK] Found {len(results)} total references in {len(by_file)} files")

if __name__ == "__main__":
    main()
