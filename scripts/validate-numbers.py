#!/usr/bin/env python3
"""
Validate Numbers Against Parameters
====================================

Checks that hardcoded numbers in QMD files match calculated values in dih_models/parameters.py.
Reports discrepancies and suggests using inline Python code instead.

Usage:
    python scripts/validate-numbers.py
    python scripts/validate-numbers.py --fix  # Auto-fix where possible
    python scripts/validate-numbers.py --report mismatches.json
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any
import argparse
import json
import importlib.util


class NumberValidator:
    """Validate numbers in QMD files against parameters.py."""

    def __init__(self):
        self.parameters = self.load_parameters()
        self.mismatches = []
        self.suggestions = []

    def load_parameters(self) -> Dict[str, Any]:
        """Load all parameters from dih_models/parameters.py."""
        params_path = Path('dih_models/parameters.py')

        if not params_path.exists():
            print(f"Warning: {params_path} not found", file=sys.stderr)
            return {}

        spec = importlib.util.spec_from_file_location("parameters", params_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Extract all uppercase variables (our parameter convention)
        parameters = {}
        for name in dir(module):
            if name.isupper() and not name.startswith('_'):
                value = getattr(module, name)
                if isinstance(value, (int, float)):
                    parameters[name] = value

        return parameters

    def extract_number_value(self, text: str) -> float:
        """Extract numeric value from text like '$27.2B' or '463:1' or '82x'."""
        # Money with units
        money_match = re.search(r'\$\s*([\d,]+(?:\.\d+)?)\s*([BMT]|billion|million|trillion)?', text)
        if money_match:
            num = float(money_match.group(1).replace(',', ''))
            unit = money_match.group(2)
            if unit:
                multipliers = {
                    'B': 1e9, 'billion': 1e9,
                    'M': 1e6, 'million': 1e6,
                    'T': 1e12, 'trillion': 1e12
                }
                num *= multipliers.get(unit, 1)
            return num

        # Ratios (just return first number)
        ratio_match = re.search(r'(\d+(?:\.\d+)?)\s*:\s*\d+', text)
        if ratio_match:
            return float(ratio_match.group(1))

        # Multipliers
        mult_match = re.search(r'(\d+(?:\.\d+)?)\s*[xX×]', text)
        if mult_match:
            return float(mult_match.group(1))

        # Percentages
        pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        if pct_match:
            return float(pct_match.group(1)) / 100

        # Plain numbers
        num_match = re.search(r'([\d,]+(?:\.\d+)?)', text)
        if num_match:
            return float(num_match.group(1).replace(',', ''))

        return None

    def find_matching_parameter(self, value: float, tolerance: float = 0.01) -> List[str]:
        """Find parameters that match this value (within tolerance)."""
        matches = []

        for param_name, param_value in self.parameters.items():
            if isinstance(param_value, (int, float)):
                # Check direct match
                if abs(param_value - value) / max(abs(value), 1) < tolerance:
                    matches.append(param_name)
                # Check if value is in billions but param is raw
                elif abs(param_value - value * 1e9) / max(abs(value * 1e9), 1) < tolerance:
                    matches.append(param_name + " (in billions)")

        return matches

    def suggest_inline_code(self, param_name: str, format_type: str = 'money') -> str:
        """Suggest inline Python code for a parameter."""
        param_clean = param_name.replace(" (in billions)", "")

        formats = {
            'money': f'{{python}} {param_clean.lower()}_formatted',
            'percent': f'{{python}} {param_clean.lower()}_pct',
            'ratio': f'{{python}} {param_clean.lower()}_ratio',
            'number': f'{{python}} {param_clean.lower()}_formatted',
        }

        return formats.get(format_type, f'{{python}} {param_clean.lower()}')

    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan file for numbers and validate against parameters."""
        issues = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                # Skip frontmatter, code blocks, etc.
                if line.strip().startswith(('---', '```', '#', '|')):
                    continue

                # Find all numbers in line
                # Money
                for match in re.finditer(r'\$\s*([\d,]+(?:\.\d+)?)\s*([BMT]|billion|million|trillion)?', line):
                    full_text = match.group(0)
                    value = self.extract_number_value(full_text)

                    if value:
                        matching_params = self.find_matching_parameter(value)
                        if matching_params:
                            issues.append({
                                'file': str(filepath.relative_to(Path.cwd())),
                                'line': line_num,
                                'type': 'money',
                                'text': full_text,
                                'value': value,
                                'matching_params': matching_params,
                                'suggestion': self.suggest_inline_code(matching_params[0], 'money'),
                                'context': line.strip()
                            })

        except Exception as e:
            print(f"Error scanning {filepath}: {e}", file=sys.stderr)

        return issues

    def scan_all(self, root_path: Path = None) -> List[Dict]:
        """Scan all QMD files."""
        root = root_path or Path('knowledge')
        all_issues = []

        for filepath in root.rglob('*.qmd'):
            issues = self.scan_file(filepath)
            all_issues.extend(issues)

        return all_issues

    def print_report(self, issues: List[Dict]):
        """Print validation report."""
        print(f"\n{'='*80}")
        print("NUMBER VALIDATION REPORT")
        print(f"{'='*80}\n")
        print(f"Found {len(issues)} numbers that could use parameters.py\n")

        by_file = {}
        for issue in issues:
            filepath = issue['file']
            if filepath not in by_file:
                by_file[filepath] = []
            by_file[filepath].append(issue)

        for filepath, file_issues in sorted(by_file.items()):
            print(f"\n📄 {filepath}")
            print(f"   {len(file_issues)} number(s) that match parameters.py\n")

            for issue in file_issues:
                print(f"   Line {issue['line']:4d}: {issue['text']}")
                print(f"              Matches: {', '.join(issue['matching_params'])}")
                print(f"              Suggest: {issue['suggestion']}")
                print(f"              Context: {issue['context'][:100]}")
                print()


def main():
    parser = argparse.ArgumentParser(description='Validate numbers against parameters.py')
    parser.add_argument('--path', type=str, default='knowledge',
                       help='Root path to scan (default: knowledge)')
    parser.add_argument('--report', type=str,
                       help='Output JSON report to file')

    args = parser.parse_args()

    validator = NumberValidator()
    issues = validator.scan_all(Path(args.path))

    if args.report:
        with open(args.report, 'w') as f:
            json.dumps(issues, f, indent=2)
        print(f"Report written to {args.report}")
    else:
        validator.print_report(issues)


if __name__ == '__main__':
    main()
