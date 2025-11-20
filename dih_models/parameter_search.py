#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search utility for finding parameters by keywords.

Usage:
    python -m dih_models.parameter_search "7.7T"
    python -m dih_models.parameter_search "conflict cost"
    python -m dih_models.parameter_search "multiplier"
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import inspect
from dih_models.parameters import Parameter

def search_parameters(query: str, search_in=["name", "description", "keywords", "unit"]):
    """
    Search for parameters by name, description, keywords, or unit.

    Args:
        query: Search string (case-insensitive)
        search_in: Fields to search ("name", "description", "keywords", "unit")

    Returns:
        List of (param_name, param_value) tuples matching query
    """
    query_lower = query.lower()
    query_words = query_lower.split()  # Split multi-word queries
    results = []

    # Get all Parameter instances from parameters module
    params_module = sys.modules['dih_models.parameters']
    for name, value in inspect.getmembers(params_module):
        if not name.isupper():
            continue
        if not isinstance(value, Parameter):
            continue

        match = False

        # Check if query appears in parameter name
        if "name" in search_in:
            if query_lower in name.lower():
                match = True
            # Also check if all query words appear in name
            elif all(word in name.lower() for word in query_words):
                match = True

        # Check description
        if "description" in search_in and hasattr(value, "description"):
            if value.description:
                if query_lower in value.description.lower():
                    match = True
                # Check if all words appear in description
                elif all(word in value.description.lower() for word in query_words):
                    match = True

        # Check keywords - either exact match or all words present
        if "keywords" in search_in and hasattr(value, "keywords"):
            keywords_str = ' '.join(value.keywords)
            if query_lower in keywords_str:
                match = True
            # Check if all query words appear in keywords
            elif all(any(word in kw for kw in value.keywords) for word in query_words):
                match = True

        # Check unit
        if "unit" in search_in and hasattr(value, "unit"):
            if value.unit and query_lower in value.unit.lower():
                match = True

        if match:
            results.append((name, value))

    # Pretty print results
    if not results:
        print(f"No parameters found matching '{query}'")
        return []

    print(f"Found {len(results)} parameter(s) matching '{query}':\n")
    for name, value in results:
        # Format value nicely
        if hasattr(value, 'display_value') and value.display_value:
            display = value.display_value
        else:
            display = f"{float(value):,.0f}" if float(value) >= 1000 else str(float(value))

        print(f"  {name} = {display}")

        if hasattr(value, "description") and value.description:
            desc = value.description[:80] + "..." if len(value.description) > 80 else value.description
            print(f"    Description: {desc}")

        if hasattr(value, "unit") and value.unit:
            print(f"    Unit: {value.unit}")

        if hasattr(value, "keywords") and value.keywords:
            print(f"    Keywords: {', '.join(value.keywords[:8])}")
            if len(value.keywords) > 8:
                print(f"              ... and {len(value.keywords)-8} more")

        print()

    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_parameters(" ".join(sys.argv[1:]))
    else:
        print("Usage: python -m dih_models.parameter_search <query>")
        print("\nExamples:")
        print("  python -m dih_models.parameter_search '7.7T'")
        print("  python -m dih_models.parameter_search 'conflict cost'")
        print("  python -m dih_models.parameter_search 'multiplier'")
        print("  python -m dih_models.parameter_search 'roi'")
