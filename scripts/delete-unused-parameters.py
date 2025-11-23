#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Delete unused parameters from parameters.py

This script removes parameter definitions that are not used anywhere in the codebase.
It preserves all other content, including comments and formatting.
"""

import sys
import re
from pathlib import Path
from typing import Set

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# List of unused parameters from find-unused-parameters.py analysis
UNUSED_PARAMS = {
    'ACCIDENTS_DEATH_RATE',
    'ALZHEIMERS_DEATH_RATE',
    'ALZHEIMER_CURE_BOUNTY_ESTIMATE',
    'ANTIBIOTICS_LIFE_EXTENSION_YEARS',
    'BIOMETRIC_VERIFICATION_COST_PER_USER_HIGH_USD',
    'BIOMETRIC_VERIFICATION_COST_PER_USER_LOW_USD',
    'CAMPAIGN_WEEKLY_AD_COST_K',
    'CANCER_DEATH_RATE',
    'CARDIOVASCULAR_DEATH_RATE',
    'CAREGIVER_HOURS_PER_MONTH_AVG',
    'CAREGIVER_VALUE_PER_HOUR',
    'DFDA_LIVES_SAVED_DAILY',
    'DFDA_NET_INCREMENTAL_COST_ANNUAL',
    'DIABETES_CURE_PAYMENT_ESTIMATE',
    'DIABETES_DEATH_RATE',
    'DIABETES_TREATMENT_MONTHLY_COST',
    'DISEASE_ERADICATION_PLUS_ACCELERATION_ANNUAL_LOSS',
    'DRUG_PRICE_REDUCTION_SAVINGS_HIGH',
    'DRUG_PRICE_REDUCTION_SAVINGS_LOW',
    'FOUNDATION_FUNDING_BASE_CASE',
    'FOUNDATION_FUNDING_PERCENTAGE',
    'FOUNDATION_FUNDING_REALISTIC',
    'FOUNDATION_FUNDING_WORST_CASE',
    'FOUNDATION_LEGAL_COMPLIANCE_REALISTIC',
    'FOUNDATION_LOBBYING_REALISTIC',
    'FOUNDATION_OPERATIONS_REALISTIC',
    'FOUNDATION_PARTNERSHIPS_REALISTIC',
    'FOUNDATION_RESERVE_REALISTIC',
    'FOUNDATION_TECH_RD_REALISTIC',
    'FOUNDATION_VIRAL_REFERENDUM_REALISTIC',
    'GLOBAL_ANNUAL_MILITARY_SPENDING_INFRASTRUCTURE_2024',
    'GLOBAL_ANNUAL_MILITARY_SPENDING_INTELLIGENCE_2024',
    'GLOBAL_ANNUAL_MILITARY_SPENDING_OPS_MAINTENANCE_2024',
    'GLOBAL_ANNUAL_MILITARY_SPENDING_PERSONNEL_2024',
    'GLOBAL_ANNUAL_MILITARY_SPENDING_PROCUREMENT_2024',
    'GLOBAL_COST_PER_CONFLICT_DEATH',
    'GLOBAL_COST_PER_REFUGEE_PER_YEAR_AVERAGE',
    'GLOBAL_GDP_2023',
    'GLOBAL_GDP_2024',
    'GLOBAL_HEALTHCARE_SPENDING_ANNUAL_2024',
    'GLOBAL_NUCLEAR_WEAPONS_ANNUAL_BUDGET_INCREASE',
    'GLOBAL_POVERTY_ERADICATION_COST_TOTAL',
    'GLOBAL_WAR_DIRECT_COST_PER_SECOND',
    'HIGH_NET_WORTH_INVESTOR_MIN',
    'KIDNEY_DISEASE_DEATH_RATE',
    'LIFETIME_WAR_COST_PER_CAPITA',
    'LIVER_DISEASE_DEATH_RATE',
    'LOBBYING_ROI_DEFENSE',
    'LONGEVITY_THERAPY_SAVINGS_30YR',
    'MEDICAL_FACILITY_HOURLY_ROOM_COST',
    'MENTAL_HEALTH_GRANTS_ANNUAL',
    'OTHER_DEATH_RATE',
    'PARTIAL_SUCCESS_INVESTOR_ROI',
    'PARTIAL_SUCCESS_RESEARCH_FUNDING',
    'PATIENT_CURE_COPAY_MAX',
    'PEACE_DIVIDEND_ROI',
    'PERSONAL_LIFE_EXTENSION_YEARS_AGE_30',
    'PETITION_SIGNATURE_COST_PER_VERIFIED_2024',
    'PHARMA_CURE_PAYMENT_PER_PATIENT',
    'PHASE_3_TRIAL_COST_MAX',
    'PRODUCTIVITY_LOSS_PER_AFFECTED_EMPLOYEE',
    'QUALIFIED_INVESTOR_MIN',
    'RARE_DISEASE_TYPICAL_PATIENT_COUNT',
    'REFERRAL_PAYMENT_EARLY_ADOPTERS_USD',
    'REFERRAL_PAYMENT_LAGGARDS_USD',
    'REFERRAL_PAYMENT_LATE_MAJORITY_USD',
    'REFERRAL_PAYMENT_MAINSTREAM_USD',
    'REFUGEE_LOST_PRODUCTIVITY_GLOBAL_TOTAL',
    'RESPIRATORY_DEATH_RATE',
    'SOCIAL_MEDIA_PARTICIPANT_TARGET_MAX',
    'SOCIAL_MEDIA_PARTICIPANT_TARGET_MIN',
    'SOFTWARE_TOOL_MONTHLY_COST_MAX',
    'SOFTWARE_TOOL_MONTHLY_COST_MIN',
    'TOTAL_DEATH_RATE',
    'TOTAL_MEDICAL_ADVANCES_1900_2000',
    'TOTAL_WAR_COST_TO_WHO_BUDGET_RATIO',
    'TREATMENT_ACCELERATION_YEARS_TARGET',
    'TREATY_ANNUAL_SUFFERING_HOURS_ELIMINATED',
    'TREATY_CAMPAIGN_BUDGET_MASS_BRIBERY',
    'TREATY_CAMPAIGN_COST_PER_VERIFIED_VOTE_REALISTIC_USD',
    'TREATY_CAMPAIGN_COST_PER_VOTE_MAX_USD',
    'TREATY_CAMPAIGN_COST_PER_VOTE_MIN_USD',
    'TREATY_CAMPAIGN_TOTAL_COST_BASE_CASE',
    'TREATY_CAMPAIGN_TOTAL_COST_REALISTIC',
    'TREATY_CAMPAIGN_TOTAL_COST_WORST_CASE',
    'TREATY_CAMPAIGN_VERIFICATION_ATTEMPTS_MULTIPLIER',
    'US_ANNUAL_DRUG_SPENDING',
    'US_DEFENSE_BUDGET_ANNUAL',
    'US_DOT_VALUE_OF_STATISTICAL_LIFE',
    'US_DRUG_PRICE_MULTIPLIER_VS_PEER_COUNTRIES',
    'US_MEDIAN_SALARY',
    'VERIFICATION_CONVERSION_RATE_GOOD_UX',
    'VERIFICATION_CONVERSION_RATE_POOR_UX',
    'VICTORY_BOND_FUNDING_BASE_CASE',
    'VICTORY_BOND_FUNDING_PERCENTAGE',
    'VICTORY_BOND_FUNDING_REALISTIC',
    'VICTORY_BOND_FUNDING_WORST_CASE',
    'VICTORY_BOND_PAYBACK_MONTHS',
    'VICTORY_LEGAL_COMPLIANCE_REALISTIC',
    'VICTORY_LOBBYING_REALISTIC',
    'VICTORY_OPERATIONS_REALISTIC',
    'VICTORY_PARTNERSHIPS_REALISTIC',
    'VICTORY_RESERVE_REALISTIC',
    'VICTORY_TECH_RD_REALISTIC',
    'VICTORY_VIRAL_REFERENDUM_REALISTIC',
    'VSL_EPA',
    'WORKFORCE_CHRONIC_ILLNESS_PREVALENCE',
}


def find_parameter_blocks(content: str) -> dict:
    """
    Find all parameter definition blocks in the file.
    Returns: {param_name: (start_pos, end_pos, full_text)}
    """
    blocks = {}

    # Pattern to match parameter definitions
    # Matches: PARAM_NAME = Parameter(...)
    pattern = r'^([A-Z][A-Z0-9_]+)\s*=\s*Parameter\('

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        match = re.match(pattern, line)

        if match:
            param_name = match.group(1)
            start_line = i

            # Find the end of this parameter definition
            # It ends with a closing paren followed by optional comma/newline
            paren_count = 0
            in_param = False
            end_line = i

            for j in range(i, len(lines)):
                current_line = lines[j]

                # Count parentheses
                for char in current_line:
                    if char == '(':
                        paren_count += 1
                        in_param = True
                    elif char == ')':
                        paren_count -= 1

                        if in_param and paren_count == 0:
                            end_line = j
                            break

                if in_param and paren_count == 0:
                    break

            # Extract the full block (including any preceding comment lines)
            block_start = start_line

            # Check for comment lines immediately before this parameter
            for k in range(start_line - 1, -1, -1):
                prev_line = lines[k].strip()
                if prev_line.startswith('#') or prev_line == '':
                    block_start = k
                else:
                    break

            # Calculate character positions
            char_start = sum(len(lines[j]) + 1 for j in range(block_start))
            char_end = sum(len(lines[j]) + 1 for j in range(end_line + 1))

            block_text = '\n'.join(lines[block_start:end_line + 1])
            blocks[param_name] = (char_start, char_end, block_text)

            i = end_line + 1
        else:
            i += 1

    return blocks


def delete_unused_parameters(parameters_file: Path, unused_params: Set[str], dry_run: bool = True):
    """
    Delete unused parameters from parameters.py

    Args:
        parameters_file: Path to parameters.py
        unused_params: Set of parameter names to delete
        dry_run: If True, only show what would be deleted without actually deleting
    """
    print("=" * 80)
    print("DELETE UNUSED PARAMETERS")
    print("=" * 80)
    print()

    # Read file
    print(f"[1/4] Reading {parameters_file}...")
    with open(parameters_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)
    print(f"      Original file size: {original_size:,} bytes")
    print()

    # Find all parameter blocks
    print("[2/4] Finding parameter blocks...")
    blocks = find_parameter_blocks(content)
    print(f"      Found {len(blocks)} parameter definitions")
    print()

    # Identify blocks to delete
    print("[3/4] Identifying unused parameters to delete...")
    to_delete = {}
    for param_name in unused_params:
        if param_name in blocks:
            to_delete[param_name] = blocks[param_name]

    print(f"      Found {len(to_delete)} unused parameters in file")

    if len(to_delete) < len(unused_params):
        missing = unused_params - set(to_delete.keys())
        print(f"      Warning: {len(missing)} parameters not found in file:")
        for param in sorted(missing)[:5]:
            print(f"        - {param}")
        if len(missing) > 5:
            print(f"        ... and {len(missing) - 5} more")
    print()

    # Delete blocks (in reverse order to preserve positions)
    print(f"[4/4] {'[DRY RUN] Simulating deletion' if dry_run else 'Deleting parameters'}...")

    # Sort by position (reverse order)
    sorted_blocks = sorted(to_delete.items(), key=lambda x: x[1][0], reverse=True)

    new_content = content
    deleted_count = 0

    for param_name, (start, end, block_text) in sorted_blocks:
        # Show what we're deleting
        lines = block_text.split('\n')
        preview = lines[0] if len(lines) == 1 else f"{lines[0]}... ({len(lines)} lines)"
        print(f"      {'[DRY RUN] Would delete' if dry_run else 'Deleting'}: {param_name}")
        print(f"               {preview}")

        if not dry_run:
            # Delete the block (including trailing newline)
            new_content = new_content[:start] + new_content[end:]
            deleted_count += 1

    print()
    print(f"      {'Would delete' if dry_run else 'Deleted'} {len(to_delete)} parameters")
    print(f"      New file size: {len(new_content):,} bytes ({original_size - len(new_content):,} bytes removed)")
    print()

    if not dry_run:
        # Write back
        print(f"Writing updated file to {parameters_file}...")
        with open(parameters_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Done!")
    else:
        print("=" * 80)
        print("DRY RUN COMPLETE - No changes made")
        print("Run with --execute flag to actually delete parameters")
        print("=" * 80)

    print()
    return len(to_delete)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Delete unused parameters from parameters.py')
    parser.add_argument('--execute', action='store_true',
                       help='Actually delete parameters (default is dry-run)')

    args = parser.parse_args()

    root = Path(__file__).parent.parent
    parameters_file = root / 'dih_models' / 'parameters.py'

    if not parameters_file.exists():
        print(f"Error: {parameters_file} not found!")
        return 1

    deleted = delete_unused_parameters(
        parameters_file,
        UNUSED_PARAMS,
        dry_run=not args.execute
    )

    if args.execute and deleted > 0:
        print("IMPORTANT: Now run these commands:")
        print("  1. python scripts/generate-variables-yml.py")
        print("  2. python scripts/find-unused-parameters.py  (to verify)")
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
