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
                 number_str: str, numeric_value: float, number_type: str = "plain",
                 matched_param: Optional[Parameter] = None):
        self.file_path = file_path
        self.line_num = line_num
        self.line_text = line_text
        self.number_str = number_str
        self.numeric_value = numeric_value
        self.number_type = number_type  # "currency", "percentage", or "plain"
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


def extract_number_from_text(text: str) -> List[Tuple[str, float, str]]:
    """
    Extract numbers from text, handling various formats:
    - Currency: $2.7T, $2,718B, $100M, $10K
    - Percentages: 12.5%, 1%
    - Plain numbers: 2718, 2,718.0, 244,600
    - Ratios: 463:1

    Returns list of (original_string, numeric_value_in_billions, number_type) tuples.
    number_type is one of: "currency", "percentage", "plain"
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

            results.append((match.group(0), value_billions, "currency"))
        except ValueError:
            pass

    # Pattern for percentages
    percentage_pattern = r'\b([0-9]+(?:\.[0-9]+)?)\s*%'
    for match in re.finditer(percentage_pattern, text):
        number_str = match.group(1)
        try:
            value = float(number_str)
            results.append((match.group(0), value, "percentage"))
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
                results.append((match.group(0), value, "plain"))
        except ValueError:
            pass

    return results


def is_compatible_unit(param: Parameter, number_type: str, numeric_value: float) -> bool:
    """
    Check if a parameter's unit is compatible with the detected number type.

    Args:
        param: The parameter to check
        number_type: One of "currency", "percentage", "plain"
        numeric_value: The numeric value extracted from text

    Returns:
        True if the parameter and number type are compatible
    """
    param_name = param.name.upper()

    # Detect parameter type from name
    is_currency_param = any(keyword in param_name for keyword in [
        'SPENDING', 'COST', 'BUDGET', 'USD', 'REVENUE', 'PRICE',
        'DIVIDEND', 'SAVINGS', 'VALUE', 'NPV', 'CAPEX', 'OPEX',
        'BILLION', 'TRILLION', 'MILLION', 'DAMAGE', 'LOSS', 'BENEFIT',
        'ECONOMIC', 'FINANCIAL', 'INVESTMENT', 'MARKET'
    ])

    is_count_param = any(keyword in param_name for keyword in [
        'DEATHS', 'PARTICIPANTS', 'PEOPLE', 'COUNT', 'SIZE',
        'POPULATION', 'NUMBER', 'TRIALS', 'APPROVALS'
    ])

    is_rate_param = any(keyword in param_name for keyword in [
        'RATE', 'PERCENT', 'REDUCTION', 'SHARE', 'RATIO'
    ]) and not is_currency_param  # "REDUCTION" could be in cost reduction

    is_year_param = any(keyword in param_name for keyword in [
        'YEARS', 'YEAR', 'AGE', 'DURATION'
    ])

    # Match number type to parameter type
    if number_type == "currency":
        # Currency symbols should match currency parameters
        return is_currency_param

    elif number_type == "percentage":
        # Percentages could match rates or small plain numbers (< 100)
        return is_rate_param or (param.value < 100 and not is_count_param and not is_currency_param)

    elif number_type == "plain":
        # Plain numbers should NOT match currency parameters
        # They can match counts, years, or other plain values
        return not is_currency_param or is_count_param

    # Default: allow match if we can't determine
    return True


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

        for number_str, numeric_value, number_type in numbers:
            # Try to find matching parameter
            matched_param = None

            # Exact match first
            if numeric_value in parameters:
                # Check if parameter type is compatible
                param_candidates = parameters[numeric_value]
                for param in param_candidates:
                    if is_compatible_unit(param, number_type, numeric_value):
                        matched_param = param
                        break
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
                        # Check unit compatibility
                        for param in param_list:
                            if is_compatible_unit(param, number_type, numeric_value):
                                matched_param = param
                                break
                        if matched_param:
                            break

            if matched_param:
                match = NumberMatch(
                    file_path=str(qmd_path),
                    line_num=i,
                    line_text=line.strip(),
                    number_str=number_str,
                    numeric_value=numeric_value,
                    number_type=number_type,
                    matched_param=matched_param
                )
                matches.append(match)

    return matches


def apply_fixes(all_matches: List[NumberMatch]) -> int:
    """
    Apply fixes by converting numbers to inline Python expressions that reference parameters.

    Modifies QMD files in place, converting numbers like:
    233,600 -> `{python} param_link(GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT, "GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT")`{=html}

    This approach:
    - Imports parameter values from dih_models/parameters.py
    - Uses the param_link() function to generate HTML links
    - Values automatically update if parameters change
    - Tooltips show the parameter source

    Returns the number of files modified.
    """
    # Group matches by file
    by_file = {}
    for match in all_matches:
        if match.file_path not in by_file:
            by_file[match.file_path] = []
        by_file[match.file_path].append(match)

    files_modified = 0

    for file_path, matches in by_file.items():
        # Skip references.qmd - contains data from external sources
        if file_path.endswith('references.qmd'):
            continue

        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check if file already has the import statement
        content = ''.join(lines)
        has_import = "from dih_models.parameters import" in content

        # Sort matches by line number (descending) to avoid offset issues
        matches_sorted = sorted(matches, key=lambda m: m.line_num, reverse=True)

        # Apply fixes from bottom to top
        modified = False
        for match in matches_sorted:
            line_idx = match.line_num - 1  # Convert to 0-indexed
            if line_idx >= len(lines):
                continue
            line = lines[line_idx]

            # Skip if already converted to Python expression
            if "{python}" in line and match.matched_param.name in line:
                continue

            # Skip if number is already in a markdown link
            if f"[{match.number_str}]" in line:
                continue

            number_str = match.number_str

            # Only add link if the number appears in the line
            if number_str in line:
                # Create inline Python expression
                # Format: `{python} param_link(PARAM_NAME, "PARAM_NAME")`{=html}
                param_expr = f'`{{python}} param_link({match.matched_param.name}, "{match.matched_param.name}")`{{=html}}'

                # Replace the number with the Python expression
                new_line = line.replace(
                    number_str,
                    param_expr,
                    1  # Replace only first occurrence
                )
                lines[line_idx] = new_line
                modified = True

        # If we modified the file and it doesn't have the import, add it after the YAML header
        if modified:
            if not has_import:
                # Find the end of YAML front matter (after closing ---)
                yaml_end = -1
                in_yaml = False
                for i, line in enumerate(lines):
                    if line.strip() == '---':
                        if not in_yaml:
                            in_yaml = True
                        else:
                            yaml_end = i
                            break

                # Insert import after YAML header
                if yaml_end >= 0:
                    import_line = "\n```{python}\n#| echo: false\nimport sys\nfrom pathlib import Path\n# Find project root (where dih_models is located)\nproject_root = Path.cwd()\nwhile not (project_root / 'dih_models').exists() and project_root.parent != project_root:\n    project_root = project_root.parent\nsys.path.insert(0, str(project_root))\nfrom dih_models.parameters import *\n```\n\n"
                    lines.insert(yaml_end + 1, import_line)

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            files_modified += 1
            print(f"  [*] Modified {file_path}")

    return files_modified


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

    # Apply fixes if requested
    if args.fix:
        print("\n[*] Applying fixes...")
        files_modified = apply_fixes(all_matches)
        print(f"[OK] Modified {files_modified} files")
        print("    Converted numbers to inline Python expressions")
        print("    Format: `{python} param_link(PARAM_NAME, \"PARAM_NAME\")`{=html}")
        print("    Values will auto-update if parameters change")
        print("    Added Python import blocks where needed")

    # Exit with error code if matches found
    sys.exit(0 if not all_matches else 1)


if __name__ == '__main__':
    main()
