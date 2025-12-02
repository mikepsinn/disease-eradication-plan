#!/usr/bin/env python3
"""
Audit Parameter Uncertainty
===========================

Identifies input parameters (external/definition) in dih_models/parameters.py
that are missing uncertainty/sensitivity metadata (distribution, CI, SE).

Generates a TODO list for filling in these gaps.
"""

import sys
import inspect
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dih_models.parameters import Parameter

def audit_parameters():
    import dih_models.parameters as params_module

    missing_uncertainty = []

    # Get all Parameter instances
    for name, obj in inspect.getmembers(params_module):
        if isinstance(obj, Parameter):
            # Check if it's an input parameter
            source_type = obj.source_type
            # Handle both Enum and string types
            st_value = source_type.value if hasattr(source_type, 'value') else str(source_type)

            if st_value in ['external', 'definition']:
                # Check for missing uncertainty metadata
                has_dist = obj.distribution is not None
                has_ci = obj.confidence_interval is not None
                has_se = obj.std_error is not None

                if not (has_dist or has_ci or has_se):
                    # Check if it's a significant parameter (heuristic)
                    # Skip 0 or 1 if they are just flags/switches (though PCTs are 0-1)
                    # Actually, list all inputs to be safe

                    # Get line number for sorting
                    try:
                        lines, line_num = inspect.getsourcelines(params_module)
                        # This is hard for attributes. Let's just trust file order from dir()?
                        # dir() is alphabetical.
                        # We can read the file to find line numbers.
                        pass
                    except:
                        pass

                    missing_uncertainty.append({
                        'name': name,
                        'value': float(obj),
                        'type': st_value,
                        'unit': obj.unit
                    })

    # Sort by type then name
    missing_uncertainty.sort(key=lambda x: (x['type'], x['name']))

    print("# Parameter Uncertainty TODO List")
    print(f"\nFound {len(missing_uncertainty)} input parameters missing uncertainty metadata.\n")

    print("## Priority 1: Key Assumptions (Definitions)")
    for p in missing_uncertainty:
        if p['type'] == 'definition':
             print(f"- [ ] `{p['name']}` (Value: {p['value']}, Unit: {p['unit']})")

    print("\n## Priority 2: External Data (Inputs)")
    for p in missing_uncertainty:
        if p['type'] == 'external':
             print(f"- [ ] `{p['name']}` (Value: {p['value']}, Unit: {p['unit']})")

if __name__ == "__main__":
    audit_parameters()
