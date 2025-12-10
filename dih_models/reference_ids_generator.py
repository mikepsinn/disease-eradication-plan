#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reference IDs enum generation utilities for dih_models
=======================================================

Generate dih_models/reference_ids.py enum from references.qmd.

Functions:
- generate_reference_ids_enum() - Generate ReferenceID enum for IDE autocomplete

Usage:
    from dih_models.reference_ids_generator import generate_reference_ids_enum
    from pathlib import Path

    # Generate reference IDs enum
    output_path = Path("dih_models/reference_ids.py")
    generate_reference_ids_enum(available_refs, output_path)
"""

from pathlib import Path


def generate_reference_ids_enum(available_refs: set, output_path: Path):
    """
    Generate dih_models/reference_ids.py with enum of valid reference IDs.

    Creates a Python enum for IDE autocomplete and static type checking.
    Developers can use ReferenceID.CDC_LEADING_CAUSES_DEATH instead of strings.

    Args:
        available_refs: Set of reference IDs from references.qmd
        output_path: Path to write reference_ids.py
    """
    content = []
    content.append("#!/usr/bin/env python3")
    content.append('"""')
    content.append("AUTO-GENERATED FILE - DO NOT EDIT")
    content.append("=" * 70)
    content.append("")
    content.append("Valid reference IDs extracted from knowledge/references.qmd")
    content.append("")
    content.append("Usage in parameters.py:")
    content.append("    from .reference_ids import ReferenceID")
    content.append("")
    content.append("    PARAM = Parameter(")
    content.append("        123.45,")
    content.append('        source_type="external",')
    content.append("        source_ref=ReferenceID.CDC_LEADING_CAUSES_DEATH,")
    content.append('        description="..."')
    content.append("    )")
    content.append("")
    content.append("Benefits:")
    content.append("  - IDE autocomplete shows all valid reference IDs")
    content.append("  - Static type checking catches typos before runtime")
    content.append("  - Refactoring safety when renaming references")
    content.append('"""')
    content.append("")
    content.append("from enum import Enum")
    content.append("")
    content.append("")
    content.append("class ReferenceID(str, Enum):")
    content.append('    """Valid reference IDs from knowledge/references.qmd"""')
    content.append("")

    # Sort reference IDs for consistent output
    sorted_refs = sorted(available_refs)

    # Convert reference IDs to enum member names
    # e.g., "cdc-leading-causes-death" -> "CDC_LEADING_CAUSES_DEATH"
    # e.g., "95-pct-diseases-no-treatment" -> "N95_PCT_DISEASES_NO_TREATMENT"
    for ref_id in sorted_refs:
        # Convert kebab-case to SCREAMING_SNAKE_CASE
        enum_name = ref_id.upper().replace("-", "_")

        # Handle special cases that start with numbers: prefix with 'N' instead of '_'
        # This avoids Python's protected member convention (_var)
        if enum_name[0].isdigit():
            enum_name = f"N{enum_name}"

        content.append(f'    {enum_name} = "{ref_id}"')

    content.append("")

    # Write file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"[OK] Generated {output_path}")
    print(f"     {len(sorted_refs)} reference IDs exported as enum")
    print()
    print("Usage in parameters.py:")
    print("    from .reference_ids import ReferenceID")
    if sorted_refs:
        first_ref = sorted_refs[0].upper().replace("-", "_")
        if first_ref[0].isdigit():
            first_ref = f"N{first_ref}"
        print(f"    source_ref=ReferenceID.{first_ref}")
    print()
