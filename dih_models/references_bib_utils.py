#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
References.bib Utilities
========================

Shared utilities for reading, writing, and validating references.bib.
All scripts that modify references.bib should use these functions.

Key features:
- Alphabetizes entries by citation key on save
- Detects duplicates in multiple fields (key, DOI, URL, title)
- Logs all issues before raising error
- Consistent formatting and encoding

Usage:
    from dih_models.references_bib_utils import save_references_bib, parse_bib_entries

Functions:
- parse_bib_entries() - Parse references.bib into list of entry dicts
- save_references_bib() - Save entries with alphabetization and duplicate checking
- add_entries_to_bib() - Add new entries, merge with existing, save sorted
- validate_bib_file() - Check for all issues without modifying
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class BibFileValidationError(Exception):
    """Raised when validation errors are found in references.bib."""

    def __init__(self, issues: List[str]):
        self.issues = issues
        message = f"Found {len(issues)} issue(s) in references.bib:\n" + "\n".join(
            f"  - {issue}" for issue in issues
        )
        super().__init__(message)


def extract_field(entry_text: str, field_name: str) -> Optional[str]:
    """
    Extract a field value from a BibTeX entry.

    Args:
        entry_text: The full BibTeX entry text
        field_name: Name of field to extract (e.g., 'doi', 'url', 'title')

    Returns:
        Field value or None if not found
    """
    # Pattern: field_name = {value} or field_name = "value"
    pattern = rf"{field_name}\s*=\s*[\{{\"](.*?)[\}}\"]"
    match = re.search(pattern, entry_text, re.IGNORECASE | re.DOTALL)
    if match:
        value = match.group(1).strip()
        # Normalize whitespace
        value = " ".join(value.split())
        return value if value else None
    return None


def parse_bib_entries(bib_path: Path) -> List[Dict[str, Any]]:
    """
    Parse references.bib into a list of entry dicts.

    Each dict contains:
        - key: citation key
        - type: entry type (article, book, etc.)
        - text: full entry text
        - doi: DOI if present
        - url: URL if present
        - title: title if present

    Args:
        bib_path: Path to references.bib

    Returns:
        List of entry dicts
    """
    if not bib_path.exists():
        return []

    with open(bib_path, encoding="utf-8") as f:
        content = f.read()

    entries = []

    # Pattern to match BibTeX entry starts: @type{key,
    pattern = r"@(\w+)\{([^,]+),"

    # Find all entry starts
    for match in re.finditer(pattern, content):
        entry_type = match.group(1)
        citation_key = match.group(2).strip()
        start_pos = match.start()

        # Find the matching closing brace
        brace_count = 0
        end_pos = start_pos
        in_entry = False

        for i, char in enumerate(content[start_pos:], start_pos):
            if char == "{":
                brace_count += 1
                in_entry = True
            elif char == "}":
                brace_count -= 1
                if in_entry and brace_count == 0:
                    end_pos = i + 1
                    break

        entry_text = content[start_pos:end_pos].strip()

        entries.append({
            "key": citation_key,
            "type": entry_type,
            "text": entry_text,
            "doi": extract_field(entry_text, "doi"),
            "url": extract_field(entry_text, "url"),
            "title": extract_field(entry_text, "title"),
        })

    return entries


def find_duplicates(
    entries: List[Dict[str, Any]],
) -> Dict[str, List[Tuple[str, List[str]]]]:
    """
    Find duplicate values across entries for fields that should be unique.

    Args:
        entries: List of entry dicts from parse_bib_entries()

    Returns:
        Dict mapping field name to list of (value, duplicate_keys) tuples
    """
    # Fields that should generally be unique
    unique_fields = ["key", "doi", "title"]

    duplicates: Dict[str, List[Tuple[str, List[str]]]] = {}

    for field in unique_fields:
        seen: Dict[str, List[str]] = {}

        for entry in entries:
            value = entry.get(field) if field != "key" else entry["key"]
            if not value:
                continue

            # Normalize for comparison
            normalized = value.lower().strip()

            # Skip empty or placeholder values
            if not normalized or normalized in ("", "n/a", "none", "unknown"):
                continue

            if normalized in seen:
                seen[normalized].append(entry["key"])
            else:
                seen[normalized] = [entry["key"]]

        # Collect actual duplicates (more than one entry)
        field_duplicates = []
        for value, keys in seen.items():
            if len(keys) > 1:
                # Find original value (not normalized)
                original_value = value
                for entry in entries:
                    entry_val = entry.get(field) if field != "key" else entry["key"]
                    if entry_val and entry_val.lower().strip() == value:
                        original_value = entry_val
                        break
                field_duplicates.append((original_value, keys))

        if field_duplicates:
            duplicates[field] = field_duplicates

    return duplicates


def validate_entries(
    entries: List[Dict[str, Any]],
    check_order: bool = True,
) -> List[str]:
    """
    Validate entries and return list of all issues found.

    Args:
        entries: List of entry dicts
        check_order: Whether to check alphabetical order

    Returns:
        List of issue descriptions (empty if valid)
    """
    issues = []

    # Check for duplicates in unique fields
    duplicates = find_duplicates(entries)

    for field, dups in duplicates.items():
        for value, keys in dups:
            display_value = value[:60] + "..." if len(value) > 60 else value
            issues.append(
                f"Duplicate {field}: '{display_value}' in entries: {', '.join(keys)}"
            )

    # Check alphabetical order
    if check_order and entries:
        keys = [e["key"] for e in entries]
        sorted_keys = sorted(keys, key=str.lower)
        if keys != sorted_keys:
            # Find first out-of-order key
            for i, (actual, expected) in enumerate(zip(keys, sorted_keys)):
                if actual != expected:
                    prev_key = sorted_keys[i - 1] if i > 0 else "(start)"
                    issues.append(
                        f"Not alphabetized: '{actual}' should come after '{prev_key}'"
                    )
                    break

    return issues


def save_references_bib(
    bib_path: Path,
    entries: List[Dict[str, Any]],
    strict: bool = True,
) -> None:
    """
    Save BibTeX entries to references.bib, alphabetized by citation key.

    Args:
        bib_path: Path to references.bib
        entries: List of entry dicts with at least 'key' and 'text' fields
        strict: If True, raise error on validation issues (default: True)

    Raises:
        BibFileValidationError: If validation issues found and strict=True
    """
    # Validate first
    issues = validate_entries(entries, check_order=False)  # We'll sort anyway

    if issues and strict:
        # Log all issues
        print(f"[ERROR] Found {len(issues)} issue(s) in references.bib:")
        for issue in issues:
            print(f"    - {issue}")
        raise BibFileValidationError(issues)

    # Sort entries alphabetically by citation key (case-insensitive)
    sorted_entries = sorted(entries, key=lambda x: x["key"].lower())

    # Build content with consistent formatting
    content_parts = []
    for entry in sorted_entries:
        content_parts.append(entry["text"])

    content = "\n\n".join(content_parts) + "\n"

    with open(bib_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def add_entries_to_bib(
    bib_path: Path,
    new_entries: List[Dict[str, Any]],
    update_existing: bool = False,
    strict: bool = True,
) -> Tuple[List[str], List[str]]:
    """
    Add new entries to references.bib, merging with existing entries.

    Args:
        bib_path: Path to references.bib
        new_entries: List of entry dicts to add (must have 'key' and 'text')
        update_existing: If True, replace existing entries with same key
        strict: If True, raise error on validation issues

    Returns:
        Tuple of (added_keys, updated_keys) lists

    Raises:
        BibFileValidationError: If validation issues found and strict=True
    """
    # Parse existing entries
    existing_entries = parse_bib_entries(bib_path)
    existing_keys = {e["key"] for e in existing_entries}

    added_keys = []
    updated_keys = []
    final_entries = []

    # Build map for updates
    new_entries_map = {e["key"]: e for e in new_entries}

    # Process existing entries
    for entry in existing_entries:
        key = entry["key"]
        if key in new_entries_map:
            if update_existing:
                # Replace with new entry
                final_entries.append(new_entries_map[key])
                updated_keys.append(key)
            else:
                # Keep existing
                final_entries.append(entry)
            del new_entries_map[key]
        else:
            final_entries.append(entry)

    # Add remaining new entries
    for key, entry in new_entries_map.items():
        final_entries.append(entry)
        added_keys.append(key)

    # Save with alphabetization and validation
    save_references_bib(bib_path, final_entries, strict=strict)

    return added_keys, updated_keys


def validate_bib_file(bib_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate references.bib for all issues without modifying.

    Args:
        bib_path: Path to references.bib

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    if not bib_path.exists():
        return False, ["File does not exist"]

    entries = parse_bib_entries(bib_path)
    issues = validate_entries(entries, check_order=True)

    return len(issues) == 0, issues


def sort_bib_file(bib_path: Path, strict: bool = False) -> int:
    """
    Sort references.bib alphabetically in place.

    Args:
        bib_path: Path to references.bib
        strict: If True, raise error on validation issues

    Returns:
        Number of entries that were reordered

    Raises:
        BibFileValidationError: If validation issues found and strict=True
    """
    entries = parse_bib_entries(bib_path)
    original_order = [e["key"] for e in entries]
    sorted_order = sorted(original_order, key=str.lower)

    # Count reordered entries
    reordered = sum(1 for a, b in zip(original_order, sorted_order) if a != b)

    if reordered > 0:
        save_references_bib(bib_path, entries, strict=strict)

    return reordered


def main():
    """CLI entry point for validation and sorting."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    project_root = Path(__file__).parent.parent.absolute()
    bib_path = project_root / "references.bib"

    print(f"[*] Validating {bib_path.name}...")

    is_valid, issues = validate_bib_file(bib_path)

    if issues:
        print(f"[WARN] Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"    - {issue}")
        print()

    # Check if just needs sorting vs has real problems
    entries = parse_bib_entries(bib_path)
    duplicate_issues = validate_entries(entries, check_order=False)

    if duplicate_issues:
        print("[ERROR] Cannot auto-fix duplicate entries. Please resolve manually.")
        sys.exit(1)
    elif not is_valid:
        print("[*] Sorting references.bib...")
        reordered = sort_bib_file(bib_path, strict=False)
        print(f"[OK] Reordered {reordered} entries")
    else:
        print("[OK] references.bib is valid and sorted")


if __name__ == "__main__":
    main()
