#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def find_hardcoded_numbers_in_file(file_path):
    """Find hardcoded numbers in a QMD file that should be replaced with variables."""

    content = Path(file_path).read_text(encoding='utf-8')
    lines = content.split('\n')

    findings = []

    # Common hardcoded values to look for
    patterns = [
        # Dollar amounts
        (r'\$50\.0*B\b', 'dfda_rd_gross_savings_annual', 'R&D gross savings'),
        (r'\$100\.0*B\b', 'global_clinical_trial_market_annual', 'Global clinical trial market'),
        (r'\$137M', 'dfda_daily_opportunity_cost', 'Daily opportunity cost'),
        (r'\$360B\b', 'us_prescription_drug_spending_annual', 'US prescription drug spending'),

        # Percentages
        (r'\b50\.0*%', 'trial_cost_reduction_pct (formatted as percentage)', 'Trial cost reduction percentage'),
        (r'\b50%', 'trial_cost_reduction_pct (formatted as percentage)', 'Trial cost reduction percentage'),

        # ROI values
        (r'\b463:1\b', 'dfda_roi_rd_only', 'Conservative ROI (R&D only)'),
        (r'\b66:1\b', 'ROI minimum from calculation', 'Minimum ROI estimate'),
        (r'\b2,?577:1\b', 'ROI maximum from calculation', 'Maximum ROI estimate'),
        (r'\b6,?489:1\b', 'dfda_roi_rd_plus_delay', 'Recommended ROI (with delay)'),
        (r'\b11,?540:1\b', 'dfda_roi_rd_plus_delay_plus_innovation', 'Full impact ROI'),

        # Specific cost values
        (r'\b\$40M?\b', 'dfda_annual_opex or related', 'Annual operational costs'),
    ]

    for line_num, line in enumerate(lines, 1):
        # Skip lines that already use variables
        if '{{< var' in line:
            continue

        # Skip LaTeX math blocks (they can't use variables)
        if line.strip().startswith('$$') or '\\text{' in line or '\\times' in line:
            continue

        for pattern, suggested_var, description in patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                findings.append({
                    'line': line_num,
                    'text': line.strip()[:100],
                    'hardcoded': match.group(0),
                    'suggested_var': suggested_var,
                    'description': description
                })

    return findings

def main():
    file_path = 'knowledge/appendix/dfda-cost-benefit-analysis.qmd'

    print(f"[*] Analyzing {file_path} for hardcoded numbers...\n")

    findings = find_hardcoded_numbers_in_file(file_path)

    if not findings:
        print("[OK] No hardcoded numbers found!")
        return

    print(f"[!] Found {len(findings)} potential hardcoded values:\n")

    # Group by suggested variable
    by_var = {}
    for f in findings:
        var = f['suggested_var']
        if var not in by_var:
            by_var[var] = []
        by_var[var].append(f)

    for var, items in sorted(by_var.items()):
        print(f"\n### {var}")
        print(f"Description: {items[0]['description']}")
        print(f"Occurrences: {len(items)}")
        print("\nLines:")
        for item in items[:10]:  # Show first 10
            print(f"  Line {item['line']}: {item['hardcoded']}")
            if len(item['text']) > 0:
                print(f"    Context: {item['text']}")
        if len(items) > 10:
            print(f"  ... and {len(items) - 10} more")

    print(f"\n\n[*] Total findings: {len(findings)}")
    print("[*] NOTE: LaTeX math blocks were skipped (variables don't work there)")
    print("[*] NOTE: Lines already using {{< var >}} were skipped")

if __name__ == '__main__':
    main()
