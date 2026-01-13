#!/usr/bin/env python3
"""
Apply reviewed latex_symbol values to parameters.py.

Usage:
    python scripts/apply-latex-symbols.py [--dry-run]

This reads scripts/latex-symbols-review.py and adds latex_symbol to
each parameter definition in dih_models/parameters.py.

Options:
    --dry-run    Show what would be changed without modifying files
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import os
import re
import importlib.util

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def load_symbols_from_review():
    """Load the SYMBOLS dict from latex-symbols-review.py"""
    review_path = os.path.join(os.path.dirname(__file__), 'latex-symbols-review.py')
    
    if not os.path.exists(review_path):
        print(f"[ERROR] Review file not found: {review_path}")
        print(f"        Run: python scripts/generate-latex-symbols.py first")
        sys.exit(1)
    
    spec = importlib.util.spec_from_file_location("review", review_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return getattr(module, 'SYMBOLS', {})


def apply_symbols(symbols: dict, dry_run: bool = False):
    """Apply latex_symbol values to parameters.py"""
    params_path = os.path.join(project_root, 'dih_models', 'parameters.py')
    
    with open(params_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    skipped = 0
    already_has = 0
    
    for param_name, latex_symbol in symbols.items():
        # Skip None values (user chose to skip)
        if latex_symbol is None:
            skipped += 1
            continue
        
        # Find the parameter definition
        # Pattern: PARAM_NAME = Parameter(
        #     ...
        # )
        
        # First check if it already has latex_symbol
        pattern_existing = rf'^({param_name}\s*=\s*Parameter\([^)]*?)(latex_symbol\s*=)'
        if re.search(pattern_existing, content, re.MULTILINE | re.DOTALL):
            already_has += 1
            continue
        
        # Find the closing of the Parameter() call
        # We need to add latex_symbol before the closing )
        # Pattern: find the parameter, then find its closing )
        
        # Strategy: Find "PARAM_NAME = Parameter(" then find the matching ")"
        param_start_pattern = rf'^{param_name}\s*=\s*Parameter\('
        match = re.search(param_start_pattern, content, re.MULTILINE)
        
        if not match:
            print(f"[WARN] Parameter not found: {param_name}")
            continue
        
        start_pos = match.end()
        
        # Find matching closing parenthesis
        # Count parens to handle nested structures
        paren_depth = 1
        pos = start_pos
        while pos < len(content) and paren_depth > 0:
            if content[pos] == '(':
                paren_depth += 1
            elif content[pos] == ')':
                paren_depth -= 1
            pos += 1
        
        if paren_depth != 0:
            print(f"[WARN] Could not find closing ) for: {param_name}")
            continue
        
        # pos is now just after the closing )
        close_pos = pos - 1  # Position of the )
        
        # Find the last non-whitespace before )
        insert_pos = close_pos
        while insert_pos > start_pos and content[insert_pos-1] in ' \t\n':
            insert_pos -= 1
        
        # Check if there's a trailing comma
        has_comma = content[insert_pos-1] == ','
        
        # Build the insertion text
        # Find the indentation level by looking at previous lines
        line_start = content.rfind('\n', 0, insert_pos) + 1
        line = content[line_start:insert_pos]
        # Extract leading whitespace
        indent_match = re.match(r'^(\s*)', line)
        indent = indent_match.group(1) if indent_match else '    '
        
        # Escape the latex_symbol for Python string
        escaped_symbol = latex_symbol.replace('\\', '\\\\')
        
        if has_comma:
            insertion = f'\n{indent}latex_symbol=r"{latex_symbol}",  # LaTeX symbol for equations'
        else:
            insertion = f',\n{indent}latex_symbol=r"{latex_symbol}",  # LaTeX symbol for equations'
        
        # Insert before the closing )
        content = content[:insert_pos] + insertion + content[insert_pos:]
        changes_made += 1
        
        if dry_run:
            print(f"[DRY-RUN] Would add to {param_name}: latex_symbol=r\"{latex_symbol}\"")
    
    print(f"\n[SUMMARY]")
    print(f"  Changes to make: {changes_made}")
    print(f"  Already have latex_symbol: {already_has}")
    print(f"  Skipped (set to None): {skipped}")
    
    if dry_run:
        print(f"\n[DRY-RUN] No changes written. Remove --dry-run to apply.")
        return
    
    if changes_made == 0:
        print(f"\n[OK] No changes needed.")
        return
    
    # Write the changes
    with open(params_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[OK] Updated {params_path}")
    print(f"     {changes_made} parameters updated with latex_symbol")
    print(f"\n     Next: Run python scripts/generate-everything-parameters-variables-calculations-references.py")


def main():
    dry_run = '--dry-run' in sys.argv
    
    if dry_run:
        print("[*] DRY RUN MODE - no changes will be made\n")
    
    print("[*] Loading symbols from latex-symbols-review.py...")
    symbols = load_symbols_from_review()
    print(f"[OK] Found {len(symbols)} symbol definitions")
    
    # Filter out None values for count
    non_none = {k: v for k, v in symbols.items() if v is not None}
    print(f"[INFO] {len(non_none)} symbols to apply ({len(symbols) - len(non_none)} set to None/skip)")
    
    print(f"\n[*] Applying symbols to parameters.py...")
    apply_symbols(symbols, dry_run)


if __name__ == '__main__':
    main()
