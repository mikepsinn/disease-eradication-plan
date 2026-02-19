#!/usr/bin/env python3
"""
Remove Duplicate Units from QMD Files
======================================

Extracts unit information from parameters.py and removes duplicate units
from variable references in QMD files.

Example duplicates:
- {{< var diseases_without_effective_treatment >}} diseases
  → {{< var diseases_without_effective_treatment >}}
- {{< var dfda_trial_capacity_plus_efficacy_lag_lives_saved >}} deaths
  → {{< var dfda_trial_capacity_plus_efficacy_lag_lives_saved >}}

Usage:
    python scripts/review/remove-duplicate-units-from-qmd.py [--preview]
"""
import sys
import re
from pathlib import Path
from typing import Dict, Set

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dih_models import parameters


def extract_units_from_parameters() -> Dict[str, str]:
    """Extract unit text for each parameter from parameters.py"""
    unit_mappings = {}

    # Get all uppercase constants from parameters module
    for name in dir(parameters):
        if name.isupper():
            value = getattr(parameters, name)

            # Only process Parameter instances with unit field
            if hasattr(value, 'unit'):
                unit = value.unit
                if unit:
                    # Convert unit to prose text for matching
                    unit_text = None

                    # Skip units that don't create text duplicates
                    if unit in ("USD", "USD/year", "percentage", "ratio", "rate", "multiplier"):
                        continue

                    # Map technical units to prose text
                    unit_map = {
                        "years": "years",
                        "months": "months",
                        "days": "days",
                        "people": "people",
                        "patients": "patients",
                        "deaths": "deaths",
                        "deaths/year": "deaths",
                        "diseases": "diseases",
                        "pairings": "pairings",
                        "members": "members",
                        "senators": "senators",
                        "drugs": "drugs",
                        "trials": "trials",
                        "lives": "lives",
                        "compounds": "compounds",
                        "combinations": "combinations",
                        "relationships": "relationships",
                        "physicians": "physicians",
                        "trials/year": "trials/year",
                    }

                    unit_text = unit_map.get(unit)

                    if unit_text:
                        # Convert to lowercase for variable name (Quarto variables are lowercase)
                        var_name_lower = name.lower()
                        unit_mappings[var_name_lower] = unit_text

    return unit_mappings


def create_pattern(var_name: str, unit: str) -> re.Pattern:
    """Create regex pattern to match variable + duplicate unit"""
    # Escape regex special characters in variable name
    var_pattern = r'\{\{< var ' + re.escape(var_name) + r' >\}\}'

    # Make unit pattern match singular/plural
    unit_words = unit.split()
    unit_patterns = []
    for word in unit_words:
        # Add optional 's' for plural (but not if word already ends in 's')
        if word.endswith('s'):
            unit_patterns.append(re.escape(word))
        else:
            unit_patterns.append(re.escape(word) + 's?')

    unit_pattern = r'\s+'.join(unit_patterns)

    # Match variable, whitespace, then unit (with word boundary)
    return re.compile(f'({var_pattern})\\s+({unit_pattern})\\b', re.IGNORECASE)


def find_and_replace_duplicates(
    qmd_files: list[Path],
    unit_mappings: Dict[str, str],
    preview: bool = True
) -> tuple[int, int]:
    """Find and remove duplicate units in QMD files

    Returns:
        (files_modified, total_replacements)
    """
    files_modified = 0
    total_replacements = 0

    for file_path in qmd_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            file_replacements = 0

            # Apply replacements for all variables
            for var_name, unit in unit_mappings.items():
                pattern = create_pattern(var_name, unit)
                matches = list(pattern.finditer(content))

                if matches:
                    # Replace with just the variable reference (group 1)
                    content = pattern.sub(r'\1', content)
                    file_replacements += len(matches)

                # For trials/year variables, also match "trials per year"
                if unit == "trials/year":
                    alt_pattern = create_pattern(var_name, "trials per year")
                    matches = list(alt_pattern.finditer(content))
                    if matches:
                        content = alt_pattern.sub(r'\1', content)
                        file_replacements += len(matches)

                # For years variables, also match -year compound adjective
                # e.g., {{< var efficacy_lag_years >}}-year → renders as "8.2 years-year"
                if unit == "years":
                    var_pat = r'\{\{< var ' + re.escape(var_name) + r' >\}\}'
                    year_pat = re.compile(f'({var_pat})-years?\\b', re.IGNORECASE)
                    matches = list(year_pat.finditer(content))
                    if matches:
                        content = year_pat.sub(r'\1', content)
                        file_replacements += len(matches)

            if content != original_content:
                files_modified += 1
                total_replacements += file_replacements

                if not preview:
                    # Write changes
                    file_path.write_text(content, encoding='utf-8')
                    print(f"✓ {file_path.relative_to(project_root)}: {file_replacements} duplicate(s) removed")
                else:
                    print(f"  {file_path.relative_to(project_root)}: {file_replacements} duplicate(s) found")

        except Exception as e:
            print(f"[ERROR] Failed to process {file_path}: {e}", file=sys.stderr)

    return files_modified, total_replacements


def get_all_qmd_files(project_root: Path) -> list[Path]:
    """Get all QMD files in the project"""
    qmd_files = []

    # Get knowledge/** QMD files
    knowledge_dir = project_root / "knowledge"
    if knowledge_dir.exists():
        qmd_files.extend(knowledge_dir.glob("**/*.qmd"))

    # Get root-level QMD files
    qmd_files.extend(project_root.glob("*.qmd"))

    return sorted(qmd_files)


def main():
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    # Check for preview mode
    preview = '--preview' in sys.argv

    print("[*] Removing duplicate units from QMD files...")
    print()

    # Step 1: Extract units from parameters.py
    print("[*] Extracting units from parameters.py...")
    unit_mappings = extract_units_from_parameters()
    print(f"[OK] Found {len(unit_mappings)} variables with text units")
    print()

    # Step 2: Get all QMD files
    qmd_files = get_all_qmd_files(project_root)
    print(f"[*] Scanning {len(qmd_files)} QMD files...")
    print()

    # Step 3: Find and replace duplicates
    if preview:
        print("[*] PREVIEW MODE - No changes will be made")
        print()

    files_modified, total_replacements = find_and_replace_duplicates(
        qmd_files, unit_mappings, preview
    )

    # Summary
    print()
    print("=" * 80)
    if preview:
        print("PREVIEW COMPLETE")
        print("=" * 80)
        print(f"Found {total_replacements} duplicate unit(s) in {files_modified} file(s)")
        print()
        print("To apply these changes, run without --preview flag:")
        print("  python scripts/review/remove-duplicate-units-from-qmd.py")
    else:
        print("REMOVAL COMPLETE")
        print("=" * 80)
        print(f"Removed {total_replacements} duplicate unit(s) from {files_modified} file(s)")
    print("=" * 80)


if __name__ == "__main__":
    main()
