#!/usr/bin/env python3
"""
Suggest Reference Links for Numbers
====================================

Analyzes numbers in QMD files and suggests appropriate reference links
based on common sources in references.qmd.

Usage:
    python scripts/suggest-links.py
    python scripts/suggest-links.py --file knowledge/economics/economics.qmd
    python scripts/suggest-links.py --apply  # Auto-apply suggestions (use with caution)
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class ReferenceSource:
    """A known reference source with typical values."""

    name: str
    anchor: str
    typical_values: List[float]
    keywords: List[str]
    units: str = ""


class LinkSuggester:
    """Suggest appropriate reference links for numbers."""

    # Known reference sources and their typical values
    REFERENCE_SOURCES = [
        ReferenceSource(
            name="SIPRI 2024 Military Spending",
            anchor="sipri-2024-spending",
            typical_values=[2718, 2.718],  # Billions or trillions
            keywords=["military", "defense", "spending", "sipri", "global"],
            units="money",
        ),
        ReferenceSource(
            name="Total War Costs",
            anchor="total-military-and-war-costs-11-4t",
            typical_values=[11355, 11.355, 11.4],
            keywords=["war", "conflict", "total cost"],
            units="money",
        ),
        ReferenceSource(
            name="RECOVERY Trial Cost Reduction",
            anchor="recovery-trial-cost-reduction",
            typical_values=[82, 80],
            keywords=["recovery", "trial", "cost", "reduction", "oxford"],
            units="multiplier",
        ),
        ReferenceSource(
            name="Clinical Trial Market Size",
            anchor="clinical-trial-market-size",
            typical_values=[100, 83],
            keywords=["clinical trial", "market", "global"],
            units="money",
        ),
        ReferenceSource(
            name="GiveWell Cost Per Life Saved",
            anchor="givewell-cost-per-life-saved",
            typical_values=[3500, 5500],
            keywords=["givewell", "cost per life", "charity"],
            units="money",
        ),
        ReferenceSource(
            name="Smallpox Eradication ROI",
            anchor="smallpox-eradication-roi",
            typical_values=[159, 400],
            keywords=["smallpox", "eradication", "roi"],
            units="ratio",
        ),
        ReferenceSource(
            name="Childhood Vaccination ROI",
            anchor="childhood-vaccination-roi",
            typical_values=[10, 16],
            keywords=["vaccination", "childhood", "roi"],
            units="ratio",
        ),
        ReferenceSource(
            name="Disease Economic Burden",
            anchor="disease-economic-burden-109t",
            typical_values=[109000, 109],
            keywords=["disease", "economic burden", "global"],
            units="money",
        ),
        ReferenceSource(
            name="ACLED Active Combat Deaths",
            anchor="acled-active-combat-deaths",
            typical_values=[233600, 244600],
            keywords=["deaths", "conflict", "acled", "combat"],
            units="number",
        ),
    ]

    def __init__(self):
        self.suggestions = []

    def extract_context(self, line: str, num_match: re.Match) -> str:
        """Extract surrounding context for a number."""
        start = max(0, num_match.start() - 50)
        end = min(len(line), num_match.end() + 50)
        return line[start:end].lower()

    def match_reference(self, value: float, context: str, num_type: str) -> Optional[ReferenceSource]:
        """Find best matching reference source for a number."""
        best_match = None
        best_score = 0

        for source in self.REFERENCE_SOURCES:
            score = 0

            # Check if value matches (within 5%)
            for typical_val in source.typical_values:
                if abs(value - typical_val) / max(abs(typical_val), 1) < 0.05:
                    score += 3
                    break

            # Check if keywords appear in context
            for keyword in source.keywords:
                if keyword.lower() in context:
                    score += 1

            # Check if units match
            if source.units == num_type:
                score += 1

            if score > best_score:
                best_score = score
                best_match = source

        # Only return if we have reasonable confidence
        return best_match if best_score >= 3 else None

    def extract_number_value(self, text: str) -> Tuple[Optional[float], str]:
        """Extract numeric value and determine type."""
        # Money with units
        money_match = re.search(r"\$\s*([\d,]+(?:\.\d+)?)\s*([BMT]|billion|million|trillion)?", text)
        if money_match:
            num = float(money_match.group(1).replace(",", ""))
            unit = money_match.group(2)
            if unit:
                multipliers = {"B": 1e9, "billion": 1e9, "M": 1e6, "million": 1e6, "T": 1e12, "trillion": 1e12}
                # Store in billions for easier matching
                num = num * multipliers.get(unit, 1) / 1e9
            return num, "money"

        # Ratios
        ratio_match = re.search(r"(\d+(?:\.\d+)?)\s*:\s*\d+", text)
        if ratio_match:
            return float(ratio_match.group(1)), "ratio"

        # Multipliers
        mult_match = re.search(r"(\d+(?:\.\d+)?)\s*[xX×]", text)
        if mult_match:
            return float(mult_match.group(1)), "multiplier"

        # Deaths/large numbers
        num_match = re.search(r"([\d,]+)", text)
        if num_match:
            return float(num_match.group(1).replace(",", "")), "number"

        return None, ""

    def scan_line(self, line: str, line_num: int, filepath: Path) -> List[Dict]:
        """Scan a line for numbers that need links."""
        suggestions = []

        # Skip if already has a link
        if "](../" in line or "](#" in line:
            return suggestions

        # Find all potential numbers
        patterns = [
            (r"\$\s*([\d,]+(?:\.\d+)?)\s*([BMT]|billion|million|trillion)?", "money"),
            (r"(\d+(?:\.\d+)?)\s*[xX×]", "multiplier"),
            (r"(\d+(?:\.\d+)?)\s*:\s*\d+", "ratio"),
            (r"(\d[\d,]*)", "number"),
        ]

        for pattern, num_type in patterns:
            for match in re.finditer(pattern, line):
                num_text = match.group(0)
                value, detected_type = self.extract_number_value(num_text)

                if value:
                    context = self.extract_context(line, match)
                    ref_source = self.match_reference(value, context, detected_type)

                    if ref_source:
                        suggestions.append(
                            {
                                "file": str(filepath.relative_to(Path.cwd())),
                                "line": line_num,
                                "number": num_text,
                                "value": value,
                                "type": detected_type,
                                "reference": ref_source.name,
                                "anchor": ref_source.anchor,
                                "suggestion": f"[{num_text}](../references.qmd#{ref_source.anchor})",
                                "context": line.strip(),
                            }
                        )

        return suggestions

    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan a file for numbers that need reference links."""
        suggestions = []

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

                if in_frontmatter or in_code_block:
                    continue

                # Track code blocks
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue

                # Scan line
                line_suggestions = self.scan_line(line, line_num, filepath)
                suggestions.extend(line_suggestions)

        except Exception as e:
            print(f"Error scanning {filepath}: {e}", file=sys.stderr)

        return suggestions

    def scan_all(self, root_path: Path = None) -> List[Dict]:
        """Scan all QMD files."""
        root = root_path or Path("knowledge")
        all_suggestions = []

        for filepath in root.rglob("*.qmd"):
            suggestions = self.scan_file(filepath)
            all_suggestions.extend(suggestions)

        return all_suggestions

    def print_suggestions(self, suggestions: List[Dict]):
        """Print linking suggestions."""
        print(f"\n{'='*80}")
        print("REFERENCE LINK SUGGESTIONS")
        print(f"{'='*80}\n")
        print(f"Found {len(suggestions)} numbers that could be linked to references.qmd\n")

        by_file = {}
        for sug in suggestions:
            filepath = sug["file"]
            if filepath not in by_file:
                by_file[filepath] = []
            by_file[filepath].append(sug)

        for filepath, file_sugs in sorted(by_file.items()):
            print(f"\n📄 {filepath}")
            print(f"   {len(file_sugs)} number(s) to link\n")

            for sug in file_sugs:
                print(f"   Line {sug['line']:4d}: {sug['number']}")
                print(f"              Reference: {sug['reference']}")
                print(f"              Replace with: {sug['suggestion']}")
                print(f"              Context: {sug['context'][:80]}")
                print()


def main():
    parser = argparse.ArgumentParser(description="Suggest reference links for numbers")
    parser.add_argument("--path", type=str, default="knowledge", help="Root path to scan (default: knowledge)")
    parser.add_argument("--file", type=str, help="Scan specific file only")

    args = parser.parse_args()

    suggester = LinkSuggester()

    if args.file:
        suggestions = suggester.scan_file(Path(args.file))
    else:
        suggestions = suggester.scan_all(Path(args.path))

    suggester.print_suggestions(suggestions)


if __name__ == "__main__":
    main()
