#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find unused parameters in parameters.py

This script identifies:
1. Parameters defined in parameters.py but never used anywhere
2. Parameters only used in calculations, never displayed (orphaned)
3. Parameters actively used in QMD files or Python scripts

Checks for parameter usage in:
- Parameter calculations in parameters.py
- {{< var param_name >}} references in QMD files
- {{< var param_name_latex >}} references in QMD files
- Direct Python usage in QMD code blocks
- All Python files (*.py) that import from parameters.py
- Jupyter notebooks (*.ipynb) that import from parameters.py
"""

import sys
import re
from pathlib import Path
from typing import Set, Dict, List
from collections import defaultdict

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Directories to skip (similar to .gitignore)
SKIP_DIRS = {
    '.git', 'node_modules', '.venv', 'venv', '__pycache__',
    '_book', '_site', 'dist', 'build', '.quarto', '.ipynb_checkpoints',
    'index_files'  # Quarto generated files
}


def should_skip_path(path: Path) -> bool:
    """Check if path should be skipped based on SKIP_DIRS"""
    return any(skip_dir in path.parts for skip_dir in SKIP_DIRS)


def find_all_parameters(parameters_file: Path) -> Set[str]:
    """Extract all parameter names from parameters.py"""
    params = set()

    with open(parameters_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all lines like: PARAM_NAME = Parameter(
    pattern = r'^([A-Z][A-Z0-9_]+)\s*=\s*Parameter\('
    for match in re.finditer(pattern, content, re.MULTILINE):
        params.add(match.group(1))

    return params


def build_parameter_usage_maps(root: Path, qmd_dir: Path, all_params: Set[str]):
    """
    Build maps of parameter usage by reading each file ONCE.
    Returns: (code_refs, qmd_refs, script_refs)
    """
    parameters_file = root / 'dih_models' / 'parameters.py'

    # Maps: param_name -> count or list of files
    code_refs = defaultdict(int)  # param -> count in parameters.py
    qmd_refs = defaultdict(list)  # param -> [(file, count), ...]
    script_refs = defaultdict(list)  # param -> [(file, count), ...]

    print("   [1/4] Scanning parameters.py for calculation references...")
    with open(parameters_file, 'r', encoding='utf-8') as f:
        params_content = f.read()

    for param in all_params:
        # Count references (excluding definition line)
        pattern = rf'\b{param}\b(?!\s*=\s*Parameter)'
        matches = list(re.finditer(pattern, params_content))

        # Subtract 1 if on definition line
        count = len(matches)
        if count > 0:
            definition_pattern = rf'^{param}\s*='
            for match in matches:
                line_start = params_content.rfind('\n', 0, match.start()) + 1
                line = params_content[line_start:params_content.find('\n', match.start())]
                if re.match(definition_pattern, line.strip()):
                    count -= 1
                    break

        code_refs[param] = count

    # Scan QMD files ONCE
    print("   [2/4] Scanning QMD files...")
    qmd_files = [f for f in qmd_dir.rglob('*.qmd') if not should_skip_path(f)]
    print(f"         Found {len(qmd_files)} QMD files to scan")

    for idx, qmd_file in enumerate(qmd_files, 1):
        if idx % 50 == 0:
            print(f"         Progress: {idx}/{len(qmd_files)} QMD files...", flush=True)

        try:
            with open(qmd_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all {{< var ... >}} references
            var_pattern = r'\{\{<\s*var\s+([a-z][a-z0-9_]+)\s*>\}\}'
            for match in re.finditer(var_pattern, content, re.IGNORECASE):
                var_name = match.group(1).lower()
                # Could be base param or param_latex
                if var_name.endswith('_latex'):
                    param_name = var_name[:-6].upper()
                else:
                    param_name = var_name.upper()

                if param_name in all_params:
                    qmd_refs[param_name].append(str(qmd_file.relative_to(root)))

            # If file imports parameters, check for direct Python usage
            if 'from dih_models.parameters import' in content:
                for param in all_params:
                    pattern = rf'\b{param}\b(?!\s*=\s*Parameter)'
                    if re.search(pattern, content):
                        qmd_refs[param].append(str(qmd_file.relative_to(root)))

        except Exception as e:
            print(f"Warning: Could not read {qmd_file}: {e}")

    # Scan Python files ONCE
    print("   [3/4] Scanning Python files...")
    py_files = [
        f for f in root.rglob('*.py')
        if not should_skip_path(f) and f.name != 'parameters.py'
    ]
    print(f"         Found {len(py_files)} Python files to scan")

    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'from dih_models.parameters import' not in content:
                continue

            for param in all_params:
                pattern = rf'\b{param}\b(?!\s*=\s*Parameter)'
                if re.search(pattern, content):
                    script_refs[param].append(str(py_file.relative_to(root)))

        except Exception as e:
            print(f"Warning: Could not read {py_file}: {e}")

    # Scan Jupyter notebooks ONCE
    print("   [4/4] Scanning Jupyter notebooks...")
    nb_files = [f for f in root.rglob('*.ipynb') if not should_skip_path(f)]
    print(f"         Found {len(nb_files)} notebook(s) to scan")

    for nb_file in nb_files:
        try:
            with open(nb_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'from dih_models.parameters import' not in content:
                continue

            for param in all_params:
                pattern = rf'\b{param}\b(?!\s*=\s*Parameter)'
                if re.search(pattern, content):
                    script_refs[param].append(str(nb_file.relative_to(root)))

        except Exception as e:
            print(f"Warning: Could not read {nb_file}: {e}")

    return code_refs, qmd_refs, script_refs


def main():
    # Paths
    root = Path(__file__).parent.parent
    parameters_file = root / 'dih_models' / 'parameters.py'
    qmd_dir = root / 'knowledge'

    print("=" * 80)
    print("FINDING UNUSED PARAMETERS")
    print("=" * 80)
    print()

    # Find all parameters
    print("[1/3] Extracting all parameters from parameters.py...")
    all_params = find_all_parameters(parameters_file)
    print(f"      Found {len(all_params)} parameters")
    print()

    # Build usage maps
    print("[2/3] Building parameter usage maps (optimized single-pass)...")
    code_refs, qmd_refs, script_refs = build_parameter_usage_maps(root, qmd_dir, all_params)
    print("      Analysis complete!")
    print()

    # Categorize parameters
    unused_params = []
    orphaned_params = []
    used_params = []

    for param in sorted(all_params):
        code_count = code_refs.get(param, 0)
        qmd_files = qmd_refs.get(param, [])
        script_files = script_refs.get(param, [])

        all_external_files = qmd_files + script_files
        total_external = len(set(all_external_files))  # Unique files

        if code_count == 0 and total_external == 0:
            unused_params.append(param)
        elif code_count == 0 and total_external > 0:
            used_params.append((param, total_external, all_external_files[:5]))
        elif code_count > 0 and total_external == 0:
            orphaned_params.append((param, code_count))
        else:
            used_params.append((param, total_external, all_external_files[:5]))

    # Report results
    print("[3/3] Results:")
    print()

    if unused_params:
        print(f"COMPLETELY UNUSED ({len(unused_params)} parameters):")
        print("These are not referenced anywhere - safe to delete!")
        print("-" * 80)
        for param in unused_params:
            print(f"  - {param}")
        print()
    else:
        print("No completely unused parameters found!")
        print()

    if orphaned_params:
        print(f"ORPHANED PARAMETERS ({len(orphaned_params)} parameters):")
        print("Only used in calculations, never used in QMD files or scripts")
        print("-" * 80)
        for param, count in orphaned_params:
            print(f"  - {param} (used {count}x in calculations)")
        print()
        print("Note: These might be intermediate calculation values.")
        print("Review before deleting - they may be needed for formulas!")
        print()

    print(f"ACTIVELY USED PARAMETERS ({len(used_params)} parameters):")
    print("Used in QMD files or scripts - keep these!")
    print("-" * 80)

    # Show top 10 most used
    used_params_sorted = sorted(used_params, key=lambda x: x[1], reverse=True)
    print("Top 10 most referenced:")
    for param, total_refs, files in used_params_sorted[:10]:
        file_list = ', '.join([f.split('/')[-1] for f in files[:3]])
        if len(files) > 3:
            file_list += f", ... ({total_refs} files total)"
        print(f"  - {param}: {total_refs} files - {file_list}")

    if len(used_params_sorted) > 10:
        print(f"  ... and {len(used_params_sorted) - 10} more")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total parameters:        {len(all_params)}")
    print(f"Completely unused:       {len(unused_params)} (can delete)")
    print(f"Orphaned (calc only):    {len(orphaned_params)} (review carefully)")
    print(f"Actively used:           {len(used_params)} (keep)")
    print()

    if unused_params:
        print(f"Suggested action: Delete {len(unused_params)} unused parameters")
        print("Run this script again after deletion to verify!")
    else:
        print("No unused parameters found - codebase is clean!")
    print()

    return 0 if len(unused_params) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
