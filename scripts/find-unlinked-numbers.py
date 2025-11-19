#!/usr/bin/env python3
"""
Find Unlinked Numbers in QMD Files
===================================

Scans all .qmd files for numeric values that aren't:
1. Inside inline Python code blocks {python}
2. Inside links [text](url)
3. Inside math blocks $$ or $

Reports numbers that should probably be linked to sources or calculations.

Usage:
    python scripts/find-unlinked-numbers.py
    python scripts/find-unlinked-numbers.py --path knowledge/economics
    python scripts/find-unlinked-numbers.py --format json > unlinked-numbers.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List


class NumberFinder:
    """Find and categorize numeric values in QMD files."""

    # Patterns for numbers we want to find
    MONEY_PATTERN = r"\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*([BMT]|billion|million|trillion)?"
    PERCENT_PATTERN = r"(\d+(?:\.\d+)?)\s*%"
    LARGE_NUMBER_PATTERN = r"\b(\d{1,3}(?:,\d{3})+)\b"
    RATIO_PATTERN = r"(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)"
    MULTIPLIER_PATTERN = r"(\d+(?:\.\d+)?)\s*[xX×]"

    # Patterns for contexts where numbers are already linked/sourced
    SKIP_PATTERNS = [
        r"`{python}[^`]+`",  # Inline Python code
        r"\[([^\]]+)\]\(([^)]+)\)",  # Markdown links
        r"\$\$[^$]+\$\$",  # Display math
        r"\$[^$]+\$",  # Inline math
        r"```[^`]+```",  # Code blocks
        r"^\s*\|",  # Table rows (often have linked headers)
    ]

    def __init__(self, root_path: Path = None):
        self.root_path = root_path or Path.cwd() / "knowledge"

    def find_qmd_files(self) -> List[Path]:
        """Find all .qmd files in the project."""
        return list(self.root_path.rglob("*.qmd"))

    def extract_numbers(self, text: str, line_num: int) -> List[Dict]:
        """Extract all numbers from a line of text with context."""
        numbers = []

        # Skip if line is in a context we don't check
        for skip_pattern in self.SKIP_PATTERNS:
            if re.search(skip_pattern, text):
                return numbers

        # Find money values
        for match in re.finditer(self.MONEY_PATTERN, text):
            numbers.append(
                {
                    "value": match.group(0),
                    "number": match.group(1),
                    "unit": match.group(2) or "",
                    "type": "money",
                    "line": line_num,
                    "context": text.strip(),
                }
            )

        # Find percentages
        for match in re.finditer(self.PERCENT_PATTERN, text):
            numbers.append(
                {
                    "value": match.group(0),
                    "number": match.group(1),
                    "unit": "%",
                    "type": "percent",
                    "line": line_num,
                    "context": text.strip(),
                }
            )

        # Find ratios (ROI, etc.)
        for match in re.finditer(self.RATIO_PATTERN, text):
            numbers.append(
                {
                    "value": match.group(0),
                    "number": f"{match.group(1)}:{match.group(2)}",
                    "unit": "ratio",
                    "type": "ratio",
                    "line": line_num,
                    "context": text.strip(),
                }
            )

        # Find multipliers
        for match in re.finditer(self.MULTIPLIER_PATTERN, text):
            numbers.append(
                {
                    "value": match.group(0),
                    "number": match.group(1),
                    "unit": "x",
                    "type": "multiplier",
                    "line": line_num,
                    "context": text.strip(),
                }
            )

        # Find large comma-separated numbers
        for match in re.finditer(self.LARGE_NUMBER_PATTERN, text):
            # Skip if already captured in money pattern
            if not any(match.group(0) in n["value"] for n in numbers):
                numbers.append(
                    {
                        "value": match.group(0),
                        "number": match.group(1),
                        "unit": "",
                        "type": "large_number",
                        "line": line_num,
                        "context": text.strip(),
                    }
                )

        return numbers

    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan a single QMD file for unlinked numbers."""
        results = []

        try:
            with open(filepath, encoding="utf-8") as f:
                lines = f.readlines()

            in_frontmatter = False
            in_code_block = False

            for line_num, line in enumerate(lines, 1):
                # Track frontmatter
                if line.strip() == "---":
                    in_frontmatter = not in_frontmatter
                    continue

                # Skip frontmatter
                if in_frontmatter:
                    continue

                # Track code blocks
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue

                # Skip code blocks
                if in_code_block:
                    continue

                # Extract numbers from this line
                numbers = self.extract_numbers(line, line_num)

                for num in numbers:
                    num["file"] = str(filepath.relative_to(Path.cwd()))
                    results.append(num)

        except Exception as e:
            print(f"Error scanning {filepath}: {e}", file=sys.stderr)

        return results

    def scan_all(self) -> Dict[str, List[Dict]]:
        """Scan all QMD files and return results grouped by file."""
        all_files = self.find_qmd_files()
        results = {}

        for filepath in all_files:
            file_results = self.scan_file(filepath)
            if file_results:
                rel_path = str(filepath.relative_to(Path.cwd()))
                results[rel_path] = file_results

        return results

    def print_results(self, results: Dict[str, List[Dict]], format: str = "text"):
        """Print results in specified format."""
        if format == "json":
            print(json.dumps(results, indent=2))
            return

        # Text format
        total_numbers = sum(len(nums) for nums in results.values())
        print(f"\n{'='*80}")
        print("UNLINKED NUMBERS REPORT")
        print(f"{'='*80}\n")
        print(f"Found {total_numbers} potentially unlinked numbers in {len(results)} files\n")

        for filepath, numbers in sorted(results.items()):
            print(f"\n📄 {filepath}")
            print(f"   {len(numbers)} unlinked number(s)\n")

            for num in numbers:
                print(f"   Line {num['line']:4d} | {num['type']:12s} | {num['value']}")
                print(f"              Context: {num['context'][:100]}")
                print()

        # Summary by type
        print(f"\n{'='*80}")
        print("SUMMARY BY TYPE")
        print(f"{'='*80}\n")

        type_counts = {}
        for numbers in results.values():
            for num in numbers:
                type_counts[num["type"]] = type_counts.get(num["type"], 0) + 1

        for num_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {num_type:15s}: {count:4d}")


def main():
    parser = argparse.ArgumentParser(description="Find unlinked numbers in QMD files")
    parser.add_argument("--path", type=str, default="knowledge", help="Root path to scan (default: knowledge)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")

    args = parser.parse_args()

    finder = NumberFinder(Path(args.path))
    results = finder.scan_all()
    finder.print_results(results, args.format)


if __name__ == "__main__":
    main()
