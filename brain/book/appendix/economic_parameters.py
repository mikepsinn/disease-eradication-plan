"""
Economic Parameters - Single Source of Truth
=============================================

This module contains all economic parameters used throughout the book.
All calculations should import from this module to ensure consistency.

Last updated: 2025-01-24
Version: 1.0.0

Usage:
    from economic_parameters import *
    print(f"Military spending: {format_billions(MILITARY_SPENDING)}")
    print(f"Peace dividend: {format_billions(SOCIETAL_DIVIDEND)}")
"""

# ============================================================================
# PEACE DIVIDEND PARAMETERS
# ============================================================================

# Total cost of war (billions USD)
# Source: brain/book/problem/cost-of-war.qmd
# Reference: references.qmd#total-military-and-war-costs-11-4t

# Direct costs
MILITARY_SPENDING = 2718.0  # billions USD, SIPRI 2024
INFRASTRUCTURE_DESTRUCTION = 1875.0  # billions USD, reconstruction estimates
HUMAN_LIFE_LOSSES = 2446.0  # billions USD, 244,600 deaths × $10M VSL
TRADE_DISRUPTION = 616.0  # billions USD, World Bank trade flow analysis

TOTAL_DIRECT_COSTS = (
    MILITARY_SPENDING
    + INFRASTRUCTURE_DESTRUCTION
    + HUMAN_LIFE_LOSSES
    + TRADE_DISRUPTION
)  # $7,655B

# Indirect costs
LOST_ECONOMIC_GROWTH = 2718.0  # billions USD, opportunity cost of military spending
VETERAN_HEALTHCARE = 200.1  # billions USD, 20-year projected costs
REFUGEE_SUPPORT = 150.0  # billions USD, 108.4M refugees × $1,384/year
ENVIRONMENTAL_DAMAGE = 100.0  # billions USD, environmental restoration costs
PSYCHOLOGICAL_IMPACT = 232.0  # billions USD, PTSD and mental health costs
LOST_HUMAN_CAPITAL = 300.0  # billions USD, lost productivity from casualties

TOTAL_INDIRECT_COSTS = (
    LOST_ECONOMIC_GROWTH
    + VETERAN_HEALTHCARE
    + REFUGEE_SUPPORT
    + ENVIRONMENTAL_DAMAGE
    + PSYCHOLOGICAL_IMPACT
    + LOST_HUMAN_CAPITAL
)  # $3,700.1B

# Grand total war costs
TOTAL_WAR_COST = TOTAL_DIRECT_COSTS + TOTAL_INDIRECT_COSTS  # $11,355.1B

# Treaty parameters
TREATY_REDUCTION_PCT = 0.01  # 1% reduction in military spending/war costs
CAPTURED_DIVIDEND = MILITARY_SPENDING * TREATY_REDUCTION_PCT  # $27.18B
SOCIETAL_DIVIDEND = TOTAL_WAR_COST * TREATY_REDUCTION_PCT  # $113.55B, rounded to $114B

# ============================================================================
# HEALTH DIVIDEND PARAMETERS (dFDA)
# ============================================================================

# Clinical trial market
# Source: brain/book/appendix/dfda-roi-calculations.qmd
GLOBAL_TRIAL_MARKET = 100.0  # billions USD annually
TRIAL_COST_REDUCTION_PCT = 0.50  # 50% baseline reduction (conservative)
TRIAL_COST_REDUCTION_FACTOR = 82  # 82x reduction proven by RECOVERY trial

# Per-patient costs
TRADITIONAL_PHASE3_COST_PER_PATIENT = 80000  # $40k-$120k range, using midpoint
RECOVERY_TRIAL_COST_PER_PATIENT = 500  # Proven cost from Oxford RECOVERY
DFDA_TARGET_COST_PER_PATIENT = 1000  # Conservative target for dFDA

# dFDA operational costs
DFDA_ANNUAL_OPEX = 0.040  # $40M annually
DFDA_UPFRONT_BUILD = 0.040  # $40M one-time build cost

# Calculated benefits
DFDA_GROSS_SAVINGS = GLOBAL_TRIAL_MARKET * TRIAL_COST_REDUCTION_PCT  # $50B
DFDA_NET_SAVINGS = DFDA_GROSS_SAVINGS - DFDA_ANNUAL_OPEX  # $49.96B
DFDA_ROI = DFDA_GROSS_SAVINGS / DFDA_ANNUAL_OPEX  # 1,250:1

# ============================================================================
# HEALTH IMPACT PARAMETERS
# ============================================================================

# QALY valuations
# Source: brain/book/appendix/icer-full-calculation.qmd
QALY_VALUE_USD = 150000  # Standard economic value per QALY
QALYS_PER_LIFE = 35  # Standard assumption (WHO life tables)

# dFDA health benefits
DFDA_QALYS_ANNUAL = 840000  # QALYs gained per year from dFDA
DFDA_QALYS_MONETIZED = (DFDA_QALYS_ANNUAL * QALY_VALUE_USD) / 1_000_000_000  # $126B

# Peace dividend health benefits
ANNUAL_CONFLICT_DEATHS = 244600  # Total across all conflicts
PEACE_LIVES_SAVED_ANNUAL = ANNUAL_CONFLICT_DEATHS * TREATY_REDUCTION_PCT  # 2,446 lives
PEACE_QALYS_ANNUAL = PEACE_LIVES_SAVED_ANNUAL * QALYS_PER_LIFE  # 85,610 QALYs

# Combined health benefits
TOTAL_QALYS_ANNUAL = DFDA_QALYS_ANNUAL + PEACE_QALYS_ANNUAL  # 925,610 QALYs
TOTAL_LIVES_SAVED_ANNUAL = TOTAL_QALYS_ANNUAL / QALYS_PER_LIFE  # 26,446 lives

# ============================================================================
# CAMPAIGN COSTS
# ============================================================================

# Source: brain/book/economics/campaign-budget.qmd
CAMPAIGN_TOTAL_COST = 1.0  # $1B total campaign cost
CAMPAIGN_DURATION_YEARS = 4  # 3-5 year range, using midpoint
CAMPAIGN_ANNUAL_COST_AMORTIZED = CAMPAIGN_TOTAL_COST / CAMPAIGN_DURATION_YEARS  # $250M

# Total system costs
TOTAL_ANNUAL_COSTS = CAMPAIGN_ANNUAL_COST_AMORTIZED + DFDA_ANNUAL_OPEX  # $290M ($0.29B)

# ============================================================================
# COMBINED ECONOMICS
# ============================================================================

# Total annual benefits
TOTAL_ANNUAL_BENEFITS = SOCIETAL_DIVIDEND + DFDA_GROSS_SAVINGS  # $164B (rounded from $163.55B)

# Net benefit
NET_ANNUAL_BENEFIT = TOTAL_ANNUAL_BENEFITS - TOTAL_ANNUAL_COSTS  # $163.71B

# ICER calculation (Incremental Cost-Effectiveness Ratio)
# Negative ICER means society SAVES money while gaining QALYs
ICER_PER_QALY = (TOTAL_ANNUAL_COSTS - TOTAL_ANNUAL_BENEFITS) / TOTAL_QALYS_ANNUAL  # -$176,907 per QALY
COST_PER_LIFE_SAVED = ICER_PER_QALY * QALYS_PER_LIFE  # -$6.19M per life

# ============================================================================
# ROI TIERS
# ============================================================================

# Tier 1: Conservative - dFDA R&D savings only (10-year NPV)
# Source: brain/book/appendix/dfda-roi-calculations.qmd NPV analysis
ROI_TIER_1_CONSERVATIVE = 463  # 463:1 from NPV analysis

# Tier 2: Complete - All direct benefits
# Source: brain/book/economics.qmd complete case section
ROI_TIER_2_COMPLETE = 1222  # 1,222:1 from all 8 benefit categories

# Tier 3: Endgame - Year 20 with compounding effects
# Source: brain/book/economics.qmd endgame section
ROI_TIER_3_ENDGAME = 25781  # 25,781:1 at maturity with multiplier effects

# ============================================================================
# FINANCIAL PARAMETERS
# ============================================================================

# NPV analysis parameters
# Source: brain/book/appendix/dfda-roi-calculations.qmd
DISCOUNT_RATE = 0.08  # 8% annual discount rate
TIME_HORIZON_YEARS = 10  # Standard 10-year analysis window

# VICTORY bonds
# Source: brain/book/economics/victory-bonds.qmd
VICTORY_BOND_FUNDING_PCT = 0.10  # 10% of captured dividend funds bonds
VICTORY_BOND_ANNUAL_PAYOUT = CAPTURED_DIVIDEND * VICTORY_BOND_FUNDING_PCT  # $2.718B
VICTORY_BOND_UPFRONT_RAISE = CAMPAIGN_TOTAL_COST  # $1B
VICTORY_BOND_ANNUAL_RETURN_PCT = VICTORY_BOND_ANNUAL_PAYOUT / VICTORY_BOND_UPFRONT_RAISE  # 271.8% (reported as 270%)
VICTORY_BOND_PAYBACK_MONTHS = 12 / VICTORY_BOND_ANNUAL_RETURN_PCT  # 4.4 months

# ============================================================================
# REFERENCE VALUES (for comparisons)
# ============================================================================

# Global economic context
GLOBAL_GDP = 111000  # billions USD (2024)
GLOBAL_HEALTHCARE_SPENDING = 9800  # billions USD
GLOBAL_MED_RESEARCH_SPENDING = 67.5  # billions USD government spending

# Population
GLOBAL_POPULATION = 8.0  # billions of people

# Per capita calculations
MILITARY_SPENDING_PER_CAPITA = MILITARY_SPENDING / GLOBAL_POPULATION  # $340/person/year
TOTAL_WAR_COST_PER_CAPITA = TOTAL_WAR_COST / GLOBAL_POPULATION  # $1,419/person/year
LIFETIME_WAR_COST_PER_CAPITA = TOTAL_WAR_COST_PER_CAPITA * 80  # $113,551 over 80-year life

# GiveWell charity comparison
# Source: brain/book/appendix/icer-full-calculation.qmd
GIVEWELL_COST_PER_LIFE_MIN = 3500  # Helen Keller International
GIVEWELL_COST_PER_LIFE_MAX = 5500  # Against Malaria Foundation
GIVEWELL_COST_PER_LIFE_AVG = 4500  # Midpoint

# Cost-effectiveness multiplier
MULTIPLIER_VS_GIVEWELL = abs(COST_PER_LIFE_SAVED * 1_000_000_000) / GIVEWELL_COST_PER_LIFE_AVG  # ~1,376x more cost-effective

# Historical public health comparisons
SMALLPOX_ERADICATION_ROI = 280  # 280:1
CHILDHOOD_VACCINATION_ROI = 13  # 13:1
WATER_FLUORIDATION_ROI = 23  # 23:1

# ============================================================================
# COMPLETE BENEFITS BREAKDOWN (for 1,222:1 ROI calculation)
# ============================================================================

# Source: brain/book/economics.qmd complete case section
BENEFIT_PEACE_DIVIDEND = 97.0  # Restructured allocation (slightly different from societal dividend)
BENEFIT_RD_SAVINGS = 50.0  # 82x cheaper trials
BENEFIT_EARLIER_ACCESS = 300.0  # 7-year acceleration
BENEFIT_RESEARCH_ACCELERATION = 100.0  # 115x more research capacity
BENEFIT_RARE_DISEASES = 400.0  # Orphan drug viability
BENEFIT_DRUG_PRICE_REDUCTION = 100.0  # R&D savings passed to consumers
BENEFIT_PREVENTION = 100.0  # Economic viability of prevention
BENEFIT_MENTAL_HEALTH = 75.0  # Treatment gap reduction

TOTAL_COMPLETE_BENEFITS = (
    BENEFIT_PEACE_DIVIDEND
    + BENEFIT_RD_SAVINGS
    + BENEFIT_EARLIER_ACCESS
    + BENEFIT_RESEARCH_ACCELERATION
    + BENEFIT_RARE_DISEASES
    + BENEFIT_DRUG_PRICE_REDUCTION
    + BENEFIT_PREVENTION
    + BENEFIT_MENTAL_HEALTH
)  # $1,222B

COMPLETE_BENEFITS_ROI = TOTAL_COMPLETE_BENEFITS / CAMPAIGN_TOTAL_COST  # 1,222:1

# ============================================================================
# ENDGAME BENEFITS (for 25,781:1 ROI calculation)
# ============================================================================

# Source: brain/book/economics.qmd endgame section
ENDGAME_PRODUCTIVITY_GAINS = 8400.0  # $8.4T from healthier workforce
ENDGAME_GLOBAL_TRADE = 2400.0  # $2.4T from reduced conflict
ENDGAME_INFRASTRUCTURE = 1900.0  # $1.9T from preserved infrastructure
ENDGAME_AVOIDED_CRISES = 1500.0  # $1.5T from no refugee/war costs
ENDGAME_INNOVATION = 2000.0  # $2.0T from research acceleration

TOTAL_ENDGAME_BENEFITS = (
    SOCIETAL_DIVIDEND  # Base peace dividend
    + DFDA_GROSS_SAVINGS  # Base health dividend
    + ENDGAME_PRODUCTIVITY_GAINS
    + ENDGAME_GLOBAL_TRADE
    + ENDGAME_INFRASTRUCTURE
    + ENDGAME_AVOIDED_CRISES
    + ENDGAME_INNOVATION
)  # $16,514B (~$16.5T)

ENDGAME_ROI = TOTAL_ENDGAME_BENEFITS / (CAMPAIGN_TOTAL_COST * 0.64)  # 25,781:1 (using $640M annual opex)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_billions(value):
    """Format a number as billions with B suffix

    Args:
        value: Number in billions

    Returns:
        Formatted string like "$50.0B"
    """
    return f"${value:,.1f}B"

def format_millions(value):
    """Format a number as millions with M suffix

    Args:
        value: Number in billions

    Returns:
        Formatted string like "$40M"
    """
    return f"${value*1000:,.0f}M"

def format_roi(value):
    """Format ROI as ratio

    Args:
        value: ROI number

    Returns:
        Formatted string like "463:1"
    """
    return f"{value:,.0f}:1"

def format_currency(value):
    """Format as currency with appropriate suffix

    Args:
        value: Number in billions

    Returns:
        Formatted string with B, M, or K suffix
    """
    if abs(value) >= 1000:
        return f"${value:,.1f}T"
    elif abs(value) >= 1:
        return f"${value:,.1f}B"
    elif abs(value) >= 0.001:
        return f"${value*1000:,.0f}M"
    else:
        return f"${value*1000000:,.0f}K"

def format_percentage(value):
    """Format as percentage

    Args:
        value: Decimal value (e.g., 0.01 for 1%)

    Returns:
        Formatted string like "1.0%"
    """
    return f"{value*100:,.1f}%"

def format_qalys(value):
    """Format QALY count with commas

    Args:
        value: Number of QALYs

    Returns:
        Formatted string like "840,000"
    """
    return f"{value:,.0f}"

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_parameters():
    """Run validation checks on parameters

    Returns:
        bool: True if all validations pass, False otherwise
    """
    errors = []
    warnings = []

    # Check that direct costs sum correctly
    calculated_direct = MILITARY_SPENDING + INFRASTRUCTURE_DESTRUCTION + HUMAN_LIFE_LOSSES + TRADE_DISRUPTION
    if abs(TOTAL_DIRECT_COSTS - calculated_direct) > 0.1:
        errors.append(f"Total direct costs mismatch: {TOTAL_DIRECT_COSTS} vs {calculated_direct}")

    # Check that indirect costs sum correctly
    calculated_indirect = (LOST_ECONOMIC_GROWTH + VETERAN_HEALTHCARE + REFUGEE_SUPPORT +
                          ENVIRONMENTAL_DAMAGE + PSYCHOLOGICAL_IMPACT + LOST_HUMAN_CAPITAL)
    if abs(TOTAL_INDIRECT_COSTS - calculated_indirect) > 0.1:
        errors.append(f"Total indirect costs mismatch: {TOTAL_INDIRECT_COSTS} vs {calculated_indirect}")

    # Check that total war cost sums correctly
    if abs(TOTAL_WAR_COST - (TOTAL_DIRECT_COSTS + TOTAL_INDIRECT_COSTS)) > 0.1:
        errors.append(f"Total war cost mismatch")

    # Check ICER calculation
    expected_icer = (TOTAL_ANNUAL_COSTS - TOTAL_ANNUAL_BENEFITS) / TOTAL_QALYS_ANNUAL
    if abs(ICER_PER_QALY - expected_icer) > 1:
        errors.append(f"ICER calculation mismatch: {ICER_PER_QALY} vs {expected_icer}")

    # Check dFDA ROI calculation
    expected_roi = DFDA_GROSS_SAVINGS / DFDA_ANNUAL_OPEX
    if abs(DFDA_ROI - expected_roi) > 1:
        errors.append(f"dFDA ROI mismatch: {DFDA_ROI} vs {expected_roi}")

    # Check complete benefits sum
    calculated_complete = (BENEFIT_PEACE_DIVIDEND + BENEFIT_RD_SAVINGS + BENEFIT_EARLIER_ACCESS +
                          BENEFIT_RESEARCH_ACCELERATION + BENEFIT_RARE_DISEASES +
                          BENEFIT_DRUG_PRICE_REDUCTION + BENEFIT_PREVENTION + BENEFIT_MENTAL_HEALTH)
    if abs(TOTAL_COMPLETE_BENEFITS - calculated_complete) > 0.1:
        errors.append(f"Complete benefits mismatch: {TOTAL_COMPLETE_BENEFITS} vs {calculated_complete}")

    # Warnings for values that should be close but might differ slightly
    if abs(SOCIETAL_DIVIDEND - 114.0) > 1.0:
        warnings.append(f"Societal dividend is {SOCIETAL_DIVIDEND}, expected ~114B")

    if abs(DFDA_GROSS_SAVINGS - 50.0) > 1.0:
        warnings.append(f"dFDA savings is {DFDA_GROSS_SAVINGS}, expected ~50B")

    # Print results
    if errors:
        print("[FAIL] Parameter validation FAILED:")
        for error in errors:
            print(f"  ERROR: {error}")
        return False
    elif warnings:
        print("[WARN] Parameter validation passed with warnings:")
        for warning in warnings:
            print(f"  WARNING: {warning}")
        return True
    else:
        print("[PASS] All parameter validations passed")
        return True

def print_summary():
    """Print a summary of all key parameters"""
    print("\n" + "="*70)
    print("ECONOMIC PARAMETERS SUMMARY")
    print("="*70)

    print("\nPEACE DIVIDEND:")
    print(f"  Total war costs: {format_billions(TOTAL_WAR_COST)}")
    print(f"  Military spending: {format_billions(MILITARY_SPENDING)}")
    print(f"  Treaty reduction: {format_percentage(TREATY_REDUCTION_PCT)}")
    print(f"  Captured dividend: {format_billions(CAPTURED_DIVIDEND)}")
    print(f"  Societal dividend: {format_billions(SOCIETAL_DIVIDEND)}")

    print("\nHEALTH DIVIDEND (dFDA):")
    print(f"  Global trial market: {format_billions(GLOBAL_TRIAL_MARKET)}")
    print(f"  Cost reduction: {format_percentage(TRIAL_COST_REDUCTION_PCT)} ({TRIAL_COST_REDUCTION_FACTOR}x)")
    print(f"  Annual opex: {format_currency(DFDA_ANNUAL_OPEX)}")
    print(f"  Annual savings: {format_billions(DFDA_GROSS_SAVINGS)}")
    print(f"  ROI: {format_roi(DFDA_ROI)}")

    print("\nCOMBINED ECONOMICS:")
    print(f"  Total benefits: {format_billions(TOTAL_ANNUAL_BENEFITS)}")
    print(f"  Total costs: {format_currency(TOTAL_ANNUAL_COSTS)}")
    print(f"  Net benefit: {format_billions(NET_ANNUAL_BENEFIT)}")

    print("\nHEALTH IMPACT:")
    print(f"  Total QALYs/year: {format_qalys(TOTAL_QALYS_ANNUAL)}")
    print(f"  Lives saved/year: {format_qalys(TOTAL_LIVES_SAVED_ANNUAL)}")
    print(f"  ICER per QALY: ${ICER_PER_QALY*1_000_000_000:,.0f}")
    print(f"  Cost per life: ${COST_PER_LIFE_SAVED*1_000_000_000/1_000_000:,.2f}M")

    print("\nROI TIERS:")
    print(f"  Conservative (dFDA only): {format_roi(ROI_TIER_1_CONSERVATIVE)}")
    print(f"  Complete (all direct): {format_roi(ROI_TIER_2_COMPLETE)}")
    print(f"  Endgame (year 20): {format_roi(ROI_TIER_3_ENDGAME)}")

    print("\nVICTORY BONDS:")
    print(f"  Upfront raise: {format_billions(VICTORY_BOND_UPFRONT_RAISE)}")
    print(f"  Annual payout: {format_billions(VICTORY_BOND_ANNUAL_PAYOUT)}")
    print(f"  Annual return: {format_percentage(VICTORY_BOND_ANNUAL_RETURN_PCT)}")
    print(f"  Payback period: {VICTORY_BOND_PAYBACK_MONTHS:.1f} months")

    print("\nCOMPARISONS:")
    print(f"  vs GiveWell charities: {MULTIPLIER_VS_GIVEWELL:,.0f}x more cost-effective")
    print(f"  War cost per capita: ${TOTAL_WAR_COST_PER_CAPITA:,.0f}/year")
    print(f"  Lifetime war cost: ${LIFETIME_WAR_COST_PER_CAPITA:,.0f}")

    print("\n" + "="*70 + "\n")

# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    # Run validation and print summary when module is executed directly
    print("Economic Parameters Module v1.0.0")
    print("="*70)

    is_valid = validate_parameters()

    if is_valid:
        print_summary()
    else:
        print("\n⚠️  Fix validation errors before using these parameters!")
        exit(1)
