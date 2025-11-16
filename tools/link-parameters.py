#!/usr/bin/env python3
"""
Link Hardcoded Numbers to Parameters
=====================================

Finds hardcoded numbers in QMD files and links them to their parameter definitions
in dih_models/parameters.py to ensure all numbers are traceable for peer review.

Usage:
    python tools/link-parameters.py                    # Dry run - report findings
    python tools/link-parameters.py --fix              # Replace numbers with links
    python tools/link-parameters.py --file FILE.qmd    # Check specific file
    python tools/link-parameters.py --value 2718       # Find specific value
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from glob import glob
import ast


class Parameter:
    """Represents a parameter from parameters.py"""
    def __init__(self, name: str, value: float, line_num: int, comment: str = ""):
        self.name = name
        self.value = value
        self.line_num = line_num
        self.comment = comment

    def __repr__(self):
        return f"Parameter({self.name}={self.value})"


class NumberMatch:
    """Represents a hardcoded number found in a QMD file"""
    def __init__(self, file_path: str, line_num: int, line_text: str,
                 number_str: str, numeric_value: float, matched_param: Optional[Parameter] = None):
        self.file_path = file_path
        self.line_num = line_num
        self.line_text = line_text
        self.number_str = number_str
        self.numeric_value = numeric_value
        self.matched_param = matched_param

    def __repr__(self):
        param_info = f" => {self.matched_param.name}" if self.matched_param else ""
        return f"{self.file_path}:{self.line_num} {self.number_str}{param_info}"


def parse_parameters_file(parameters_path: Path) -> Dict[float, List[Parameter]]:
    """
    Parse parameters.py and extract all numeric constants.

    Returns a dict mapping numeric values to list of parameters with that value.
    """
    parameters = {}

    with open(parameters_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        # Skip comments and empty lines
        if line.strip().startswith('#') or not line.strip():
            continue

        # Look for variable assignments like: VAR_NAME = 123.45
        match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)(?:\s*#.*)?$', line.strip())
        if not match:
            continue

        var_name = match.group(1)
        value_expr = match.group(2).strip()

        # Try to evaluate the expression to get numeric value
        try:
            # Handle Python number formatting (underscores)
            value_expr_clean = value_expr.replace('_', '')

            # Try to evaluate as a simple literal
            value = ast.literal_eval(value_expr_clean)

            # Only process numeric values
            if isinstance(value, (int, float)):
                if value not in parameters:
                    parameters[value] = []

                # Extract comment if present
                comment = ""
                if '#' in line:
                    comment = line.split('#', 1)[1].strip()

                param = Parameter(var_name, value, i, comment)
                parameters[value].append(param)

        except (ValueError, SyntaxError):
            # Skip calculated expressions - we'll handle those separately
            pass

    return parameters


def extract_number_from_text(text: str) -> List[Tuple[str, float]]:
    """
    Extract numbers from text, handling various formats:
    - Currency: $2.7T, $2,718B, $100M, $10K
    - Percentages: 12.5%, 1%
    - Plain numbers: 2718, 2,718.0, 244,600
    - Ratios: 463:1

    Returns list of (original_string, numeric_value_in_billions) tuples.
    """
    results = []

    # Pattern for currency with scale suffix
    # Matches: $2.7T, $2,718B, $100M, $10.5K, etc.
    currency_pattern = r'\$\s*([0-9,]+(?:\.[0-9]+)?)\s*([TMKB])\b'
    for match in re.finditer(currency_pattern, text):
        number_str = match.group(1).replace(',', '')
        scale = match.group(2)

        try:
            value = float(number_str)

            # Convert to billions for comparison with parameters
            if scale == 'T':
                value_billions = value * 1000
            elif scale == 'B':
                value_billions = value
            elif scale == 'M':
                value_billions = value / 1000
            elif scale == 'K':
                value_billions = value / 1000000
            else:
                continue

            results.append((match.group(0), value_billions))
        except ValueError:
            pass

    # Pattern for plain large numbers (likely in billions)
    # Matches: 2,718 or 2718 (but not years like 2024)
    large_number_pattern = r'\b([0-9]{1,3}(?:,[0-9]{3})+)\b'
    for match in re.finditer(large_number_pattern, text):
        number_str = match.group(1).replace(',', '')
        try:
            value = float(number_str)
            # Assume numbers > 100 without currency are in their natural unit (billions if large)
            if value >= 100:
                results.append((match.group(0), value))
        except ValueError:
            pass

    # Pattern for percentages
    percentage_pattern = r'\b([0-9]+(?:\.[0-9]+)?)\s*%'
    for match in re.finditer(percentage_pattern, text):
        number_str = match.group(1)
        try:
            value = float(number_str)
            results.append((match.group(0), value))
        except ValueError:
            pass

    return results


def find_hardcoded_numbers(qmd_path: Path, parameters: Dict[float, List[Parameter]],
                          tolerance: float = 0.01) -> List[NumberMatch]:
    """
    Find hardcoded numbers in a QMD file that match parameters.

    Args:
        qmd_path: Path to QMD file
        parameters: Dict mapping values to Parameter objects
        tolerance: Relative tolerance for matching (1% default)
    """
    matches = []

    with open(qmd_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        # Skip code blocks and inline code
        if '```' in line or line.strip().startswith('`'):
            continue

        # Skip lines that already reference parameters
        if 'parameters.' in line or '{python}' in line:
            continue

        # Extract numbers from this line
        numbers = extract_number_from_text(line)

        for number_str, numeric_value in numbers:
            # Try to find matching parameter
            matched_param = None

            # Exact match first
            if numeric_value in parameters:
                matched_param = parameters[numeric_value][0]  # Take first if multiple
            else:
                # Fuzzy match within tolerance
                for param_value, param_list in parameters.items():
                    # Skip zero values and negative values (like ICER)
                    if param_value == 0 or param_value < 0:
                        continue

                    # Use absolute value in denominator to handle negatives correctly
                    # Also skip if values are too far apart in absolute terms (different scales)
                    abs_diff = abs(param_value - numeric_value)
                    relative_diff = abs_diff / abs(param_value)

                    # Only match if within tolerance AND values are in same ballpark
                    # (to avoid matching percentages to billions, etc.)
                    if relative_diff <= tolerance and abs_diff < abs(param_value) * 2:
                        matched_param = param_list[0]
                        break

            if matched_param:
                match = NumberMatch(
                    file_path=str(qmd_path),
                    line_num=i,
                    line_text=line.strip(),
                    number_str=number_str,
                    numeric_value=numeric_value,
                    matched_param=matched_param
                )
                matches.append(match)

    return matches


def generate_report(all_matches: List[NumberMatch]) -> str:
    """Generate a human-readable report of findings."""
    if not all_matches:
        return "[OK] No hardcoded numbers found that match parameters!"

    report = []
    report.append("=" * 80)
    report.append(f"HARDCODED NUMBERS REPORT - Found {len(all_matches)} matches")
    report.append("=" * 80)
    report.append("")

    # Group by file
    by_file = {}
    for match in all_matches:
        if match.file_path not in by_file:
            by_file[match.file_path] = []
        by_file[match.file_path].append(match)

    for file_path in sorted(by_file.keys()):
        matches = by_file[file_path]
        report.append(f"\n{file_path} ({len(matches)} matches):")
        report.append("-" * 80)

        for match in matches:
            report.append(f"  Line {match.line_num}: {match.number_str}")
            report.append(f"    => {match.matched_param.name} = {match.matched_param.value}")
            report.append(f"    Context: {match.line_text[:100]}...")
            report.append("")

    report.append("=" * 80)
    report.append(f"Total: {len(all_matches)} hardcoded numbers found")
    report.append("=" * 80)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description='Find and link hardcoded numbers to parameter definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--fix', action='store_true',
                        help='Replace hardcoded numbers with parameter links')
    parser.add_argument('--file', type=str,
                        help='Check specific QMD file only')
    parser.add_argument('--value', type=float,
                        help='Search for specific numeric value')
    parser.add_argument('--tolerance', type=float, default=0.01,
                        help='Relative tolerance for matching (default: 0.01 = 1%%)')
    parser.add_argument('--output', type=str,
                        help='Write report to file instead of stdout')

    args = parser.parse_args()

    # Get project root
    project_root = Path(__file__).parent.parent.absolute()

    # Parse parameters file
    parameters_path = project_root / 'dih_models' / 'parameters.py'
    if not parameters_path.exists():
        print(f"[ERROR] Parameters file not found: {parameters_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Parsing {parameters_path}...")
    parameters = parse_parameters_file(parameters_path)
    print(f"[OK] Found {len(parameters)} unique parameter values")

    # Get QMD files to check
    if args.file:
        qmd_files = [Path(args.file)]
    else:
        qmd_files = [Path(f) for f in glob(str(project_root / 'knowledge' / '**' / '*.qmd'), recursive=True)]
        qmd_files = [f for f in qmd_files if '_site' not in str(f) and '_book' not in str(f)]

    print(f"[*] Checking {len(qmd_files)} QMD files...")

    # Find all matches
    all_matches = []
    for qmd_file in qmd_files:
        matches = find_hardcoded_numbers(qmd_file, parameters, args.tolerance)
        all_matches.extend(matches)

    # Filter by value if requested
    if args.value is not None:
        all_matches = [m for m in all_matches if abs(m.numeric_value - args.value) / max(abs(args.value), 1) <= args.tolerance]

    # Generate report
    report = generate_report(all_matches)

    # Output report
    if args.output:
        # Create output directory if needed
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"[OK] Report written to {args.output}")
    else:
        # Print with proper encoding handling for Windows console
        try:
            print(report)
        except UnicodeEncodeError:
            # Fall back to ASCII-safe output
            print(report.encode('ascii', errors='replace').decode('ascii'))

    # TODO: Implement --fix mode to actually replace numbers
    if args.fix:
        print("\n[WARNING] --fix mode not yet implemented", file=sys.stderr)
        print("          This would require careful context analysis to avoid breaking existing links", file=sys.stderr)
        sys.exit(1)

    # Exit with error code if matches found
    sys.exit(0 if not all_matches else 1)


if __name__ == '__main__':
    main()
