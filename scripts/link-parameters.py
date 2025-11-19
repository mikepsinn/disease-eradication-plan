#!/usr/bin/env python3
"""
Link Hardcoded Numbers to Parameters
=====================================

Finds hardcoded numbers in QMD files that match the formatted display strings
in _variables.yml and replaces them with Quarto variable references.

This approach:
- Searches for exact display strings (e.g., "$50B", "50%", "244,600")
- Only replaces when the formatting matches exactly
- Preserves all symbols and units automatically
- Simple and reliable - no false positives from numeric parsing

Usage:
    python tools/link-parameters.py                 # Dry run - report findings
    python tools/link-parameters.py --fix           # Replace numbers with links
    python tools/link-parameters.py --file FILE.qmd # Check specific file
"""

import argparse
import sys
from glob import glob
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List

import yaml


class HTMLStripper(HTMLParser):
    """Strip HTML tags to get plain text display value"""

    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return "".join(self.text)


def strip_html(html_str: str) -> str:
    """Extract plain text from HTML string"""
    stripper = HTMLStripper()
    stripper.feed(html_str)
    return stripper.get_text()


def load_variable_display_strings(variables_yml_path: Path) -> Dict[str, str]:
    """
    Load _variables.yml and extract display_string -> var_name mapping.

    Returns:
        Dict mapping display strings (e.g., "$50.0B") to variable names
    """
    with open(variables_yml_path, encoding="utf-8") as f:
        variables = yaml.safe_load(f)

    display_to_var = {}

    for var_name, html_value in variables.items():
        # Strip HTML to get the plain display text
        display_str = strip_html(html_value)

        # Skip empty or very short values
        if not display_str or len(display_str) < 2:
            continue

        # Store mapping from display string to variable name
        display_to_var[display_str] = var_name

    return display_to_var


def find_matches_in_file(qmd_path: Path, display_to_var: Dict[str, str], skip_common: bool = True) -> List[tuple]:
    """
    Find hardcoded numbers in a QMD file that match variable display strings.

    Args:
        qmd_path: Path to QMD file
        display_to_var: Mapping of display strings to variable names
        skip_common: Skip common small numbers (1, 2, 5, etc.)

    Returns:
        List of (line_num, line_text, match_str, var_name) tuples
    """
    matches = []

    with open(qmd_path, encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        # Skip code blocks
        if "```" in line or line.strip().startswith("`"):
            continue

        # Skip YAML frontmatter (lines 1-30 typically)
        if i <= 30 and (":" in line or line.strip().startswith("-")):
            continue

        # Skip lines that already have Quarto variables
        if "{{< var " in line:
            continue

        # Search for each display string in this line
        for display_str, var_name in display_to_var.items():
            # Only match formatted numbers (with symbols or commas)
            has_formatting = (
                "$" in display_str
                or "%" in display_str
                or "," in display_str
                or "B" in display_str
                or "M" in display_str
                or "T" in display_str
                or "K" in display_str
            )

            # Skip plain small numbers (< 1000) without formatting
            if not has_formatting:
                try:
                    num_val = float(display_str.replace(",", ""))
                    if num_val < 1000:
                        continue  # Too generic
                except:
                    pass

            # Skip fractional currency amounts (too context-specific)
            # Examples: $0.72, $0.02, $0.20, $0.30
            if display_str.startswith("$") and "." in display_str:
                try:
                    amount = float(display_str.replace("$", ""))
                    if amount < 1:
                        continue  # Skip sub-dollar amounts
                except:
                    pass

            # Skip currency amounts under $10 (too generic and context-dependent)
            # Examples: $0, $4, $6 (these are often partial matches)
            if display_str.startswith("$") and not any(suffix in display_str for suffix in ["B", "M", "T", "K"]):
                try:
                    amount = float(display_str.replace("$", "").replace(",", ""))
                    if amount < 10:
                        continue  # Too generic, likely partial matches
                except:
                    pass

            # Check if this display string appears in the line with word boundaries
            # Use regex to ensure we don't match "$6" inside "$686" or "1,000" inside "$41,000"
            # Pattern: not preceded by digit or period, match the string, not followed by digit or period
            if display_str in line:
                # Find all occurrences to check context
                import re

                # Escape special regex characters in display_str
                escaped = re.escape(display_str)
                # Ensure not preceded or followed by a digit or decimal point
                # (?<!\d) = negative lookbehind (not preceded by digit)
                # (?<!\.) = negative lookbehind (not preceded by decimal)
                # (?!\d) = negative lookahead (not followed by digit)
                # (?!\.) = negative lookahead (not followed by decimal)
                pattern = r"(?<!\d)(?<!\.)" + escaped + r"(?!\d)(?!\.)"
                if re.search(pattern, line):
                    matches.append((i, line.strip(), display_str, var_name))

    return matches


def apply_fixes(qmd_path: Path, matches: List[tuple]) -> int:
    """
    Replace matched display strings with Quarto variable references.

    Returns number of replacements made.
    """
    if not matches:
        return 0

    with open(qmd_path, encoding="utf-8") as f:
        lines = f.readlines()

    # Group matches by line number
    matches_by_line = {}
    for line_num, _, display_str, var_name in matches:
        if line_num not in matches_by_line:
            matches_by_line[line_num] = []
        matches_by_line[line_num].append((display_str, var_name))

    replacements = 0

    # Process each line with matches
    for line_num, line_matches in matches_by_line.items():
        line_idx = line_num - 1
        line = lines[line_idx]

        # Sort matches by length (longest first) to avoid partial replacements
        line_matches.sort(key=lambda x: len(x[0]), reverse=True)

        modified_line = line
        for display_str, var_name in line_matches:
            if display_str in modified_line:
                # Replace with Quarto variable reference
                var_expr = f"{{{{< var {var_name} >}}}}"
                modified_line = modified_line.replace(display_str, var_expr, 1)
                replacements += 1

        lines[line_idx] = modified_line

    # Write back to file
    with open(qmd_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return replacements


def main():
    parser = argparse.ArgumentParser(
        description="Find and link hardcoded numbers to parameter definitions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--fix", action="store_true", help="Replace hardcoded numbers with parameter links")
    parser.add_argument("--file", type=str, help="Check specific QMD file only")
    parser.add_argument(
        "--no-skip-common", action="store_true", help="Include common values (1, 2, 5, etc.) in matches"
    )

    args = parser.parse_args()

    # Get project root
    project_root = Path(__file__).parent.parent.absolute()

    # Load _variables.yml
    variables_yml = project_root / "_variables.yml"
    if not variables_yml.exists():
        print(f"[ERROR] {variables_yml} not found", file=sys.stderr)
        print("        Run: python tools/generate-variables-yml.py", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Loading {variables_yml}...")
    display_to_var = load_variable_display_strings(variables_yml)
    print(f"[OK] Loaded {len(display_to_var)} variable display strings")

    # Get list of QMD files to check
    if args.file:
        qmd_files = [Path(args.file)]
    else:
        qmd_files = [Path(p) for p in glob(str(project_root / "knowledge/**/*.qmd"), recursive=True)]

    print(f"[*] Checking {len(qmd_files)} QMD files...")

    # Find matches
    all_matches = []
    files_with_matches = 0

    for qmd_path in qmd_files:
        # Skip figures directory
        if "/figures/" in str(qmd_path) or "\\figures\\" in str(qmd_path):
            continue

        # Skip references.qmd
        if qmd_path.name == "references.qmd":
            continue

        matches = find_matches_in_file(qmd_path, display_to_var, skip_common=not args.no_skip_common)

        if matches:
            all_matches.extend([(qmd_path, *m) for m in matches])
            files_with_matches += 1

    # Print report
    print("=" * 80)
    print(f"HARDCODED NUMBERS REPORT - Found {len(all_matches)} matches in {files_with_matches} files")
    print("=" * 80)
    print()

    if all_matches:
        # Group by file
        by_file = {}
        for qmd_path, line_num, line_text, display_str, var_name in all_matches:
            if qmd_path not in by_file:
                by_file[qmd_path] = []
            by_file[qmd_path].append((line_num, line_text, display_str, var_name))

        # Print matches by file
        for qmd_path, matches in sorted(by_file.items()):
            print(f"\n{qmd_path} ({len(matches)} matches):")
            print("-" * 80)
            for line_num, line_text, display_str, var_name in matches[:10]:  # Limit to first 10 per file
                # Handle Unicode encoding errors for Windows console
                try:
                    context = line_text[:100]
                except:
                    context = line_text[:100].encode("ascii", errors="replace").decode("ascii")

                print(f"  Line {line_num}: {display_str}")
                print(f"    => {var_name}")
                try:
                    print(f"    Context: {context}...")
                except UnicodeEncodeError:
                    print(f"    Context: {context.encode('ascii', errors='replace').decode('ascii')}...")

            if len(matches) > 10:
                print(f"  ... and {len(matches) - 10} more matches")

    print()
    print("=" * 80)
    print(f"Total: {len(all_matches)} hardcoded numbers found")
    print("=" * 80)

    # Apply fixes if requested
    if args.fix and all_matches:
        print("\n[*] Applying fixes...")

        files_modified = 0
        total_replacements = 0

        # Group by file
        by_file = {}
        for qmd_path, line_num, line_text, display_str, var_name in all_matches:
            if qmd_path not in by_file:
                by_file[qmd_path] = []
            by_file[qmd_path].append((line_num, line_text, display_str, var_name))

        for qmd_path, matches in by_file.items():
            replacements = apply_fixes(qmd_path, matches)
            if replacements > 0:
                files_modified += 1
                total_replacements += replacements
                print(f"  [*] Modified {qmd_path} ({replacements} replacements)")

        print(f"\n[OK] Modified {files_modified} files")
        print(f"     Made {total_replacements} replacements")
        print("     Format: {{< var param_name >}}")
        print("     Values will auto-update when _variables.yml is regenerated")

    sys.exit(0 if not all_matches else 1)


if __name__ == "__main__":
    main()
