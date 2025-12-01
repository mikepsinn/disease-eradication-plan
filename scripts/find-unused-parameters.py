#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find unused parameters and formatted variables in parameters.py

This script identifies:
1. Parameters defined in parameters.py but never used anywhere
2. Intermediate calculation parameters (used in formulas, not displayed)
3. Parameters actively used in QMD files or Python scripts
4. Formatted variables (e.g., param_name_formatted) that are unused

Checks for parameter usage in:
- Parameter calculations in parameters.py
- {{< var param_name >}} references in QMD files
- {{< var param_name_latex >}} references in QMD files
- {{< var param_name_formatted >}} references in QMD files
- Direct Python usage in QMD code blocks
- All Python files (*.py) that import from parameters.py
- Jupyter notebooks (*.ipynb) that import from parameters.py
"""

import sys
import re
from pathlib import Path
from typing import Set, Dict, List, Tuple
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


def find_all_formatted_variables(parameters_file: Path) -> Set[str]:
    """Extract all formatted variable names from parameters.py (e.g., param_name_formatted)"""
    formatted_vars = set()

    with open(parameters_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all lines like: some_name_formatted = format_...(...)  or  some_name_formatted = f"..."
    # These are lowercase variable names ending in _formatted
    pattern = r'^([a-z][a-z0-9_]*_formatted)\s*='
    for match in re.finditer(pattern, content, re.MULTILINE):
        formatted_vars.add(match.group(1))

    return formatted_vars


def find_dependents(parameters_file: Path, all_params: Set[str]) -> Dict[str, List[str]]:
    """
    Build a robust map of parameter dependencies by extracting the full
    Parameter(...) definition blocks using balanced parentheses, then
    scanning each block for references to other parameters.

    Returns: other_param -> [list of params that depend on it]
    """
    dependents: Dict[str, List[str]] = defaultdict(list)

    with open(parameters_file, 'r', encoding='utf-8') as f:
        file_text = f.read()

    lines = file_text.splitlines()

    # Build blocks with positional info: list of (name, start_line, end_line, text)
    blocks: List[Tuple[str, int, int, str]] = []

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = re.match(r'^([A-Z][A-Z0-9_]+)\s*=\s*Parameter\s*\(', line)
        if not m:
            i += 1
            continue

        param_name = m.group(1)
        start_line = i
        depth = 0
        block_lines = []

        first_paren_idx = line.find('(')
        if first_paren_idx != -1:
            segment = line[first_paren_idx:]
            depth += segment.count('(') - segment.count(')')
            block_lines.append(line)
        else:
            block_lines.append(line)

        i += 1
        while i < n and depth > 0:
            curr = lines[i]
            depth += curr.count('(') - curr.count(')')
            block_lines.append(curr)
            i += 1

        end_line = i - 1
        blocks.append((param_name, start_line, end_line, '\n'.join(block_lines)))

    # 1) Attribute references found inside blocks to that block's param
    for param, start_line, end_line, block_text in blocks:
        for other_param in all_params:
            if other_param == param:
                continue
            if re.search(rf'\b{other_param}\b', block_text):
                dependents[other_param].append(param)

    # 2) Heuristic: attribute free-standing references to the nearest preceding block
    #    Find all occurrences by line, then map to owning block by line range
    owner_by_line = {}
    for name, start, end, _ in blocks:
        for ln in range(start, end + 1):
            owner_by_line[ln] = name

    for idx, line in enumerate(lines):
        # Skip lines that are part of a known block (already handled)
        if idx in owner_by_line:
            continue
        for other_param in all_params:
            if re.search(rf'\b{other_param}\b', line):
                # Find nearest preceding block owner, if any
                prev_lines = [line_no for line_no in owner_by_line.keys() if line_no < idx]
                if prev_lines:
                    nearest = max(prev_lines)
                    owner = owner_by_line.get(nearest)
                    if owner and owner != other_param:
                        dependents[other_param].append(owner)

    # Deduplicate and stabilize order
    for k, v in dependents.items():
        dependents[k] = sorted(set(v))

    return dependents


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

    # Scan QMD files ONCE (search across the entire workspace, not just knowledge/)
    print("   [2/4] Scanning QMD files...")
    qmd_files = [f for f in root.rglob('*.qmd') if not should_skip_path(f)]
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
                elif var_name.endswith('_cite'):
                    # Citation variables map back to the base parameter
                    param_name = var_name[:-5].upper()
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


def build_formatted_var_usage_maps(root: Path, all_formatted_vars: Set[str]):
    """
    Build maps of formatted variable usage by scanning QMD files for {{< var ... >}} references.
    Returns: (qmd_refs, script_refs) where each is formatted_var -> list of files
    """
    parameters_file = root / 'dih_models' / 'parameters.py'
    
    qmd_refs = defaultdict(list)  # formatted_var -> [files...]
    script_refs = defaultdict(list)  # formatted_var -> [files...]

    # Scan QMD files for {{< var formatted_var_name >}} references
    qmd_files = [f for f in root.rglob('*.qmd') if not should_skip_path(f)]

    for qmd_file in qmd_files:
        try:
            with open(qmd_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all {{< var ... >}} references
            var_pattern = r'\{\{<\s*var\s+([a-z][a-z0-9_]+)\s*>\}\}'
            for match in re.finditer(var_pattern, content, re.IGNORECASE):
                var_name = match.group(1).lower()
                # Check if this is one of our formatted variables
                if var_name in all_formatted_vars:
                    qmd_refs[var_name].append(str(qmd_file.relative_to(root)))

            # If file imports parameters, check for direct Python usage
            if 'from dih_models.parameters import' in content:
                for fmt_var in all_formatted_vars:
                    if re.search(rf'\b{fmt_var}\b', content):
                        qmd_refs[fmt_var].append(str(qmd_file.relative_to(root)))

        except Exception as e:
            pass  # Silently skip - already warned during parameter scan

    # Scan Python files for direct usage
    py_files = [
        f for f in root.rglob('*.py')
        if not should_skip_path(f) and f.name != 'parameters.py'
    ]

    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'from dih_models.parameters import' not in content:
                continue

            for fmt_var in all_formatted_vars:
                if re.search(rf'\b{fmt_var}\b', content):
                    script_refs[fmt_var].append(str(py_file.relative_to(root)))

        except Exception as e:
            pass

    # Scan Jupyter notebooks
    nb_files = [f for f in root.rglob('*.ipynb') if not should_skip_path(f)]

    for nb_file in nb_files:
        try:
            with open(nb_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'from dih_models.parameters import' not in content:
                continue

            for fmt_var in all_formatted_vars:
                if re.search(rf'\b{fmt_var}\b', content):
                    script_refs[fmt_var].append(str(nb_file.relative_to(root)))

        except Exception as e:
            pass

    return qmd_refs, script_refs


def main():
    # Paths
    root = Path(__file__).parent.parent
    parameters_file = root / 'dih_models' / 'parameters.py'
    # Historically we scanned only 'knowledge/'. Now we scan the entire workspace
    # for QMD files, but keep qmd_dir param for compatibility.
    qmd_dir = root

    print("=" * 80)
    print("PARAMETER & FORMATTED VARIABLE USAGE ANALYSIS")
    print("=" * 80)
    print()

    # Find all parameters
    print("[1/5] Extracting all parameters from parameters.py...")
    all_params = find_all_parameters(parameters_file)
    print(f"      Found {len(all_params)} parameters")
    print()

    # Find all formatted variables
    print("[2/5] Extracting all formatted variables from parameters.py...")
    all_formatted_vars = find_all_formatted_variables(parameters_file)
    print(f"      Found {len(all_formatted_vars)} formatted variables")
    print()

    # Build usage maps
    print("[3/5] Building parameter usage maps (optimized single-pass)...")
    code_refs, qmd_refs, script_refs = build_parameter_usage_maps(root, qmd_dir, all_params)
    print("      Analysis complete!")
    print()

    # Build formatted variable usage maps
    print("[4/5] Building formatted variable usage maps...")
    fmt_qmd_refs, fmt_script_refs = build_formatted_var_usage_maps(root, all_formatted_vars)
    print("      Analysis complete!")
    print()
    
    # Find dependents
    print("[5/5] Analyzing parameter dependencies...")
    dependents = find_dependents(parameters_file, all_params)
    print("      Dependency analysis complete!")
    print()

    # Categorize parameters
    unused_params = []
    intermediate_params = []  # Used in calculations only
    used_params = []

    for param in sorted(all_params):
        code_count = code_refs.get(param, 0)
        qmd_files = qmd_refs.get(param, [])
        script_files = script_refs.get(param, [])
        dependent_params = dependents.get(param, [])

        all_external_files = qmd_files + script_files
        total_external = len(set(all_external_files))  # Unique files

        if code_count == 0 and total_external == 0:
            unused_params.append(param)
        elif total_external == 0:
            # Only used in calculations - intermediate value
            intermediate_params.append((param, code_count, dependent_params))
        else:
            used_params.append((param, total_external, all_external_files[:5]))

    # Categorize formatted variables
    unused_formatted = []
    used_formatted = []

    for fmt_var in sorted(all_formatted_vars):
        qmd_files = fmt_qmd_refs.get(fmt_var, [])
        script_files = fmt_script_refs.get(fmt_var, [])
        all_files = qmd_files + script_files
        total_refs = len(set(all_files))

        if total_refs == 0:
            unused_formatted.append(fmt_var)
        else:
            used_formatted.append((fmt_var, total_refs, all_files[:5]))

    # Report results
    print("RESULTS:")
    print()

    if unused_params:
        print(f"🗑️  COMPLETELY UNUSED ({len(unused_params)} parameters):")
        print("   These are not referenced anywhere - safe to delete!")
        print("-" * 80)
        for param in unused_params:
            print(f"   - {param}")
        print()
    else:
        print("✅ No completely unused parameters found!")
        print()

    if intermediate_params:
        print(f"🔧 INTERMEDIATE CALCULATION VALUES ({len(intermediate_params)} parameters):")
        print("   Used in other parameter formulas, not displayed in documents.")
        print("   These are REQUIRED for calculations - do NOT delete unless consolidating!")
        print("-" * 80)
        
        # Sort by usage count (lowest first - candidates for consolidation)
        intermediate_sorted = sorted(intermediate_params, key=lambda x: (x[1], len(x[2])))
        
        # Group by usage count
        single_use = [(p, c, d) for p, c, d in intermediate_sorted if c == 1]
        multi_use = [(p, c, d) for p, c, d in intermediate_sorted if c > 1]
        
        if single_use:
            print()
            print(f"   📍 SINGLE-USE ({len(single_use)} params) - could potentially inline:")
            for param, count, deps in single_use[:15]:
                dep_str = deps[0] if deps else "unknown"
                print(f"      - {param}")
                print(f"        └─ used by: {dep_str}")
                # Also list external files (QMD/Python/Notebook) where referenced
                ext_files = sorted(set((qmd_refs.get(param, []) + script_refs.get(param, []))))
                if ext_files:
                    short_list = ', '.join([ext_files[i].replace('\\', '/') for i in range(min(3, len(ext_files)))])
                    more = f" (+{len(ext_files) - 3} more)" if len(ext_files) > 3 else ""
                    print(f"        └─ files: {short_list}{more}")
            if len(single_use) > 15:
                print(f"      ... and {len(single_use) - 15} more single-use params")
        
        if multi_use:
            print()
            print(f"   🔗 MULTI-USE ({len(multi_use)} params) - keep these (reused across formulas):")
            for param, count, deps in multi_use[:10]:
                dep_list = ', '.join(deps[:3])
                if len(deps) > 3:
                    dep_list += f" (+{len(deps)-3} more)"
                print(f"      - {param} ({count}x)")
                print(f"        └─ used by: {dep_list}")
            if len(multi_use) > 10:
                print(f"      ... and {len(multi_use) - 10} more multi-use params")
        
        print()

    print(f"📊 ACTIVELY DISPLAYED ({len(used_params)} parameters):")
    print("   Used in QMD files or scripts - these appear in output documents.")
    print("-" * 80)

    # Show top 10 most used
    used_params_sorted = sorted(used_params, key=lambda x: x[1], reverse=True)
    print("   Top 10 most referenced:")
    for param, total_refs, files in used_params_sorted[:10]:
        file_list = ', '.join([f.split('\\')[-1] for f in files[:3]])
        if len(files) > 3:
            file_list += ", ..."
        print(f"      - {param}: {total_refs} files")
        print(f"        └─ {file_list}")

    if len(used_params_sorted) > 10:
        print(f"      ... and {len(used_params_sorted) - 10} more")
    print()

    # FORMATTED VARIABLES SECTION
    print("=" * 80)
    print("FORMATTED VARIABLES ANALYSIS")
    print("=" * 80)
    print()

    if unused_formatted:
        print(f"🗑️  UNUSED FORMATTED VARIABLES ({len(unused_formatted)}):")
        print("   These formatted variables are defined but never used in QMD files - safe to delete!")
        print("-" * 80)
        for fmt_var in unused_formatted:
            print(f"   - {fmt_var}")
        print()
    else:
        print("✅ No unused formatted variables found!")
        print()

    if used_formatted:
        print(f"📊 ACTIVELY USED FORMATTED VARIABLES ({len(used_formatted)}):")
        print("   Used in QMD files via {{< var ... >}} references.")
        print("-" * 80)
        
        # Show top 10 most used
        used_formatted_sorted = sorted(used_formatted, key=lambda x: x[1], reverse=True)
        print("   Top 10 most referenced:")
        for fmt_var, total_refs, files in used_formatted_sorted[:10]:
            file_list = ', '.join([f.split('\\')[-1].split('/')[-1] for f in files[:3]])
            if len(files) > 3:
                file_list += ", ..."
            print(f"      - {fmt_var}: {total_refs} files")
            print(f"        └─ {file_list}")
        
        if len(used_formatted_sorted) > 10:
            print(f"      ... and {len(used_formatted_sorted) - 10} more")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("PARAMETERS:")
    print(f"  Total parameters:              {len(all_params)}")
    print(f"  Completely unused:             {len(unused_params)} (can delete)")
    print(f"  Intermediate (calc only):      {len(intermediate_params)} (required for formulas)")
    print(f"    - Single-use:                {len([p for p, c, d in intermediate_params if c == 1])}")
    print(f"    - Multi-use:                 {len([p for p, c, d in intermediate_params if c > 1])}")
    print(f"  Actively displayed:            {len(used_params)} (appear in documents)")
    print()
    print("FORMATTED VARIABLES:")
    print(f"  Total formatted variables:     {len(all_formatted_vars)}")
    print(f"  Unused (can delete):           {len(unused_formatted)}")
    print(f"  Actively used:                 {len(used_formatted)}")
    print()

    if unused_params:
        print(f"🎯 Action: Delete {len(unused_params)} unused parameters")
        print("   Run this script again after deletion to verify!")
    
    if unused_formatted:
        print(f"🎯 Action: Delete {len(unused_formatted)} unused formatted variables")
        print("   These are defined in parameters.py but never referenced in QMD files.")
    
    if not unused_params and not unused_formatted:
        print("✅ No unused parameters or formatted variables - codebase is clean!")
        
    single_use_count = len([p for p, c, d in intermediate_params if c == 1])
    if single_use_count > 20:
        print()
        print(f"💡 Tip: {single_use_count} single-use intermediate params could potentially")
        print("   be inlined into their parent formulas to simplify parameters.py")
    
    print()

    # Return non-zero if there are unused items
    has_unused = len(unused_params) > 0 or len(unused_formatted) > 0
    return 1 if has_unused else 0


if __name__ == '__main__':
    sys.exit(main())
