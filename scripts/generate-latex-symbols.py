#!/usr/bin/env python3
"""
Generate a reviewable file of latex_symbol suggestions for all parameters.

Usage:
    python scripts/generate-latex-symbols.py

This creates scripts/latex-symbols-review.py containing:
- All parameter names
- Auto-generated latex_symbol suggestions
- Existing latex_symbol values (if any)

Review and edit the file, then run:
    python scripts/apply-latex-symbols.py
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import os
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dih_models import parameters as params_module
from dih_models.parameters import Parameter
from dih_models.latex_generation import create_latex_variable_name, smart_title_case


def get_all_parameters():
    """Get all Parameter instances from parameters.py"""
    parameters = {}
    for name in dir(params_module):
        if name.startswith('_'):
            continue
        value = getattr(params_module, name)
        if isinstance(value, Parameter):
            parameters[name] = {'value': value}
    return parameters


def generate_latex_symbol(param_name: str, param_value) -> str:
    """
    Generate a suggested latex_symbol for a parameter.
    
    Uses the same logic as create_latex_variable_name but returns
    a clean symbol suitable for the latex_symbol property.
    """
    display_name = getattr(param_value, 'display_name', '') or smart_title_case(param_name)
    
    # Use existing latex_generation logic
    symbol = create_latex_variable_name(param_name, display_name)
    
    return symbol


def main():
    print("[*] Loading parameters...")
    parameters = get_all_parameters()
    print(f"[OK] Found {len(parameters)} parameters")
    
    # Group by whether they already have latex_symbol
    has_symbol = []
    needs_symbol = []
    
    for name, data in sorted(parameters.items()):
        value = data.get('value')
        existing = getattr(value, 'latex_symbol', None)
        suggested = generate_latex_symbol(name, value)
        
        entry = {
            'name': name,
            'existing': existing,
            'suggested': suggested,
            'unit': getattr(value, 'unit', ''),
            'description': (getattr(value, 'description', '') or '')[:80],
        }
        
        if existing:
            has_symbol.append(entry)
        else:
            needs_symbol.append(entry)
    
    print(f"[INFO] {len(has_symbol)} parameters already have latex_symbol")
    print(f"[INFO] {len(needs_symbol)} parameters need latex_symbol")
    
    # Generate the review file
    output_path = os.path.join(os.path.dirname(__file__), 'latex-symbols-review.py')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('LATEX SYMBOL REVIEW FILE\n')
        f.write('========================\n')
        f.write('\n')
        f.write('This file contains suggested latex_symbol values for all parameters.\n')
        f.write('\n')
        f.write('HOW TO USE:\n')
        f.write('1. Review the SYMBOLS dict below\n')
        f.write('2. Edit any symbols that look wrong or could be improved\n')
        f.write('3. Set symbols to None to skip (keep auto-generated)\n')
        f.write('4. Run: python scripts/apply-latex-symbols.py\n')
        f.write('\n')
        f.write('SYMBOL GUIDELINES:\n')
        f.write('- Use subscripts for context: Cost_{platform}, OPEX_{dFDA}\n')
        f.write('- Keep it short but meaningful\n')
        f.write('- Use \\\\text{} for multi-letter words: \\\\text{OPEX}_{total}\n')
        f.write('- Common patterns:\n')
        f.write('    Cost_{X}, Benefit_{X}, ROI_{X}\n')
        f.write('    Deaths_{cause}, DALYs_{source}\n')
        f.write('    Years_{context}, Rate_{what}\n')
        f.write('"""\n\n')
        
        f.write('# Parameters that already have latex_symbol (for reference)\n')
        f.write('EXISTING_SYMBOLS = {\n')
        for entry in has_symbol:
            f.write(f'    # {entry["description"]}\n')
            f.write(f'    "{entry["name"]}": r"{entry["existing"]}",\n')
        f.write('}\n\n')
        
        f.write('# Parameters needing latex_symbol - REVIEW AND EDIT THESE\n')
        f.write('# Set to None to skip (use auto-generated symbol)\n')
        f.write('SYMBOLS = {\n')
        
        # Group by prefix for easier review
        prefixes = {}
        for entry in needs_symbol:
            parts = entry['name'].split('_')
            prefix = parts[0] if parts else 'OTHER'
            if prefix not in prefixes:
                prefixes[prefix] = []
            prefixes[prefix].append(entry)
        
        for prefix in sorted(prefixes.keys()):
            entries = prefixes[prefix]
            f.write(f'\n    # === {prefix} ({len(entries)} parameters) ===\n')
            for entry in entries:
                desc = entry['description']
                if len(desc) > 60:
                    desc = desc[:57] + '...'
                f.write(f'    # {desc}\n')
                f.write(f'    # Unit: {entry["unit"]}\n')
                f.write(f'    "{entry["name"]}": r"{entry["suggested"]}",\n')
                f.write('\n')
        
        f.write('}\n')
    
    print(f"\n[OK] Generated {output_path}")
    print(f"     Review and edit the SYMBOLS dict, then run:")
    print(f"     python scripts/apply-latex-symbols.py")


if __name__ == '__main__':
    main()
