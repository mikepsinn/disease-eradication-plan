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
    print(f"Peace dividend: {format_billions(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT)}")
"""

# ---
# PEACE DIVIDEND PARAMETERS
# ---

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

# Conflict death breakdown (for QALY calculations)
# Source: brain/book/problem/cost-of-war.qmd#death-accounting
CONFLICT_DEATHS_ACTIVE_COMBAT = 233600  # ACLED data
CONFLICT_DEATHS_TERROR_ATTACKS = 8300  # Global Terrorism Database
CONFLICT_DEATHS_STATE_VIOLENCE = 2700  # Uppsala Conflict Data Program
# Note: Total should equal 244,600

# Treaty parameters
TREATY_REDUCTION_PCT = 0.01  # 1% reduction in military spending/war costs
TREATY_ANNUAL_FUNDING = MILITARY_SPENDING * TREATY_REDUCTION_PCT  # $27.18B
PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT = TOTAL_WAR_COST * TREATY_REDUCTION_PCT  # $113.55B, rounded to $114B

# ---
# HEALTH DIVIDEND PARAMETERS (dFDA)
# ---

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

# dFDA operational cost breakdown (in billions)
DFDA_OPEX_PLATFORM_MAINTENANCE = 0.015  # $15M
DFDA_OPEX_STAFF = 0.010  # $10M - minimal, AI-assisted
DFDA_OPEX_INFRASTRUCTURE = 0.008  # $8M - cloud, security
DFDA_OPEX_REGULATORY = 0.005  # $5M - regulatory coordination
DFDA_OPEX_COMMUNITY = 0.002  # $2M - community support
# Total should equal DFDA_ANNUAL_OPEX ($40M)

# Calculated benefits
DFDA_GROSS_SAVINGS = GLOBAL_TRIAL_MARKET * TRIAL_COST_REDUCTION_PCT  # $50B
DFDA_NET_SAVINGS = DFDA_GROSS_SAVINGS - DFDA_ANNUAL_OPEX  # $49.96B

# Simple ROI (not NPV-adjusted)
DFDA_ROI_SIMPLE = DFDA_GROSS_SAVINGS / DFDA_ANNUAL_OPEX  # 1,250:1
# NOTE: For NPV-adjusted ROI (463:1), use ROI_TIER_1_CONSERVATIVE below
# The NPV-based calculation accounts for time value of money and gradual adoption

# ---
# HEALTH IMPACT PARAMETERS
# ---

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

# ---
# CAMPAIGN COSTS
# ---

# Source: brain/book/economics/campaign-budget.qmd
CAMPAIGN_TOTAL_COST = 1.0  # $1B total campaign cost
CAMPAIGN_DURATION_YEARS = 4  # 3-5 year range, using midpoint
CAMPAIGN_ANNUAL_COST_AMORTIZED = CAMPAIGN_TOTAL_COST / CAMPAIGN_DURATION_YEARS  # $250M

# Campaign budget breakdown (in billions)
CAMPAIGN_BUDGET_VIRAL_REFERENDUM = 0.200  # $200M viral referendum
CAMPAIGN_BUDGET_AI_LOBBYING = 0.250  # $250M AI-assisted lobbying
CAMPAIGN_BUDGET_TECHNOLOGY = 0.250  # $250M technology platform
CAMPAIGN_BUDGET_LEGAL = 0.100  # $100M legal & compliance
CAMPAIGN_BUDGET_PARTNERSHIPS = 0.100  # $100M partnerships
CAMPAIGN_BUDGET_OPERATIONS = 0.050  # $50M operations
CAMPAIGN_BUDGET_RESERVE = 0.050  # $50M reserve
# Total should equal CAMPAIGN_TOTAL_COST ($1B)

# Total system costs
TOTAL_ANNUAL_COSTS = CAMPAIGN_ANNUAL_COST_AMORTIZED + DFDA_ANNUAL_OPEX  # $290M ($0.29B)

# ---
# COMBINED ECONOMICS
# ---

# Total annual benefits
TOTAL_ANNUAL_BENEFITS = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + DFDA_GROSS_SAVINGS  # $164B (rounded from $163.55B)

# Net benefit
NET_ANNUAL_BENEFIT = TOTAL_ANNUAL_BENEFITS - TOTAL_ANNUAL_COSTS  # $163.71B

# ICER calculation (Incremental Cost-Effectiveness Ratio)
# Negative ICER means society SAVES money while gaining QALYs
ICER_PER_QALY = (TOTAL_ANNUAL_COSTS - TOTAL_ANNUAL_BENEFITS) / TOTAL_QALYS_ANNUAL  # -$176,907 per QALY
COST_PER_LIFE_SAVED = ICER_PER_QALY * QALYS_PER_LIFE  # -$6.19M per life

# ---
# ROI TIERS
# ---

# Tier 1: Conservative - dFDA R&D savings only (10-year NPV)
# Source: brain/book/appendix/dfda-roi-calculations.qmd NPV analysis
ROI_TIER_1_CONSERVATIVE = 463  # 463:1 from NPV analysis

# Tier 2: Complete - All direct benefits
# Source: brain/book/economics.qmd complete case section
ROI_TIER_2_COMPLETE = 1222  # 1,222:1 from all 8 benefit categories

# Tier 3: Endgame - Year 20 with compounding effects
# Source: brain/book/economics.qmd endgame section
ROI_TIER_3_ENDGAME = 25781  # 25,781:1 at maturity with multiplier effects

# ---
# FINANCIAL PARAMETERS
# ---

# NPV analysis parameters
# Source: brain/book/appendix/dfda-calculation-framework.qmd
DISCOUNT_RATE = 0.08  # 8% annual discount rate (r)
TIME_HORIZON_YEARS = 10  # Standard 10-year analysis window (T)

# NPV Model - Upfront Costs (C0)
# Combines core platform build + medium broader initiative setup costs
DFDA_NPV_UPFRONT_COST = 0.040  # $40M core platform build
DIH_NPV_UPFRONT_COST_INITIATIVES = 0.22975  # $228M medium case broader initiatives
DIH_NPV_UPFRONT_COST_TOTAL = DFDA_NPV_UPFRONT_COST + DIH_NPV_UPFRONT_COST_INITIATIVES  # C0 = $0.26975B

# NPV Model - Annual Operational Costs (Cop)
# Combines core platform ops + medium broader initiative annual costs
DFDA_NPV_ANNUAL_OPEX = 0.01895  # $19M core platform (midpoint of $11-26.5M)
DIH_NPV_ANNUAL_OPEX_INITIATIVES = 0.02110  # $21.1M medium case broader initiatives
DIH_NPV_ANNUAL_OPEX_TOTAL = DFDA_NPV_ANNUAL_OPEX + DIH_NPV_ANNUAL_OPEX_INITIATIVES  # Cop = $0.04005B

# NPV Model - Savings Parameters
GLOBAL_TRIAL_MARKET = GLOBAL_TRIAL_MARKET  # Rd = $100B
TRIAL_COST_REDUCTION_PCT = TRIAL_COST_REDUCTION_PCT  # alpha = 0.50 (50%)

# NPV Model - Adoption Curve
# Linear ramp from 0% to 100% over 5 years, then constant at 100%
DFDA_ADOPTION_RAMP_YEARS = 5  # Years to reach full adoption

# Calculated NPV values
DIH_NPV_PV_ANNUAL_OPEX = DIH_NPV_ANNUAL_OPEX_TOTAL * (1 - (1 + DISCOUNT_RATE)**-TIME_HORIZON_YEARS) / DISCOUNT_RATE
DIH_NPV_TOTAL_COST = DIH_NPV_UPFRONT_COST_TOTAL + DIH_NPV_PV_ANNUAL_OPEX  # ~$0.54B
DFDA_NPV_NET_BENEFIT_CONSERVATIVE = DIH_NPV_TOTAL_COST * ROI_TIER_1_CONSERVATIVE # ~$249B

# NOTE: The NPV-based ROI (463:1) accounts for time value of money and gradual adoption
# The simple ROI (1,250:1) is gross savings / annual opex without discounting
# Use ROI_TIER_1_CONSERVATIVE (463:1) as the canonical figure for most purposes

# VICTORY bonds
# Source: brain/book/economics/victory-bonds.qmd
VICTORY_BOND_FUNDING_PCT = 0.10  # 10% of captured dividend funds bonds
VICTORY_BOND_ANNUAL_PAYOUT = TREATY_ANNUAL_FUNDING * VICTORY_BOND_FUNDING_PCT  # $2.718B
VICTORY_BOND_UPFRONT_RAISE = CAMPAIGN_TOTAL_COST  # $1B
VICTORY_BOND_ANNUAL_RETURN_PCT = VICTORY_BOND_ANNUAL_PAYOUT / VICTORY_BOND_UPFRONT_RAISE  # 271.8% (reported as 270%)
VICTORY_BOND_PAYBACK_MONTHS = 12 / VICTORY_BOND_ANNUAL_RETURN_PCT  # 4.4 months
DIVIDEND_COVERAGE_FACTOR = TREATY_ANNUAL_FUNDING / DFDA_ANNUAL_OPEX # ~679x

# DIH Treasury allocations (in billions)
# Source: brain/book/appendix/icer-full-calculation.qmd
DIH_TREASURY_MILITARY_REDIRECT = TREATY_ANNUAL_FUNDING  # $27B/year redirected from military budgets
DIH_TREASURY_TO_VICTORY_BONDS = VICTORY_BOND_ANNUAL_PAYOUT  # $2.7B/year to bondholders (10%)
DIH_TREASURY_TO_RESEARCH_PCT = 1 - VICTORY_BOND_FUNDING_PCT # 90%
DIH_TREASURY_TO_RESEARCH = DIH_TREASURY_MILITARY_REDIRECT - DIH_TREASURY_TO_VICTORY_BONDS  # $24.3B/year
DIH_TREASURY_DFDA_OPERATIONS = DFDA_ANNUAL_OPEX  # $40M/year for dFDA operations
DIH_TREASURY_TRIAL_SUBSIDIES_MIN = 10.0  # $10B/year clinical trial subsidies (minimum)
DIH_TREASURY_TRIAL_SUBSIDIES_MAX = 20.0  # $20B/year clinical trial subsidies (maximum)

# ---
# REFERENCE VALUES (for comparisons)
# ---

# Global economic context
GLOBAL_GDP = 111000  # billions USD (2024)
GLOBAL_HEALTHCARE_SPENDING = 9800  # billions USD
GLOBAL_MED_RESEARCH_SPENDING = 67.5  # billions USD government spending
TOTAL_GLOBAL_WASTE_SPEND = 118800 # billions USD, annual spend on military + disease

# Population
GLOBAL_POPULATION = 8.0  # billions of people
DAILY_DEATHS_CURABLE_DISEASES = 150000 # Daily deaths from curable diseases

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

# ---
# COMPLETE BENEFITS BREAKDOWN (for 1,222:1 ROI calculation)
# ---

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

# ---
# ENDGAME BENEFITS (for 25,781:1 ROI calculation)
# ---

# Source: brain/book/economics.qmd endgame section
ENDGAME_PRODUCTIVITY_GAINS = 8400.0  # $8.4T from healthier workforce
ENDGAME_GLOBAL_TRADE = 2400.0  # $2.4T from reduced conflict
ENDGAME_INFRASTRUCTURE = 1900.0  # $1.9T from preserved infrastructure
ENDGAME_AVOIDED_CRISES = 1500.0  # $1.5T from no refugee/war costs
ENDGAME_INNOVATION = 2000.0  # $2.0T from research acceleration

TOTAL_ENDGAME_BENEFITS = (
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT  # Base peace dividend
    + DFDA_GROSS_SAVINGS  # Base health dividend
    + ENDGAME_PRODUCTIVITY_GAINS
    + ENDGAME_GLOBAL_TRADE
    + ENDGAME_INFRASTRUCTURE
    + ENDGAME_AVOIDED_CRISES
    + ENDGAME_INNOVATION
)  # $16,514B (~$16.5T)

ENDGAME_ROI = TOTAL_ENDGAME_BENEFITS / (CAMPAIGN_TOTAL_COST * 0.64)  # 25,781:1 (using $640M annual opex)

# COST OF DELAY PARAMETERS
# Source: brain/book/economics.qmd
# Note: These are derived for illustrative purposes in the text
ENDGAME_BENEFIT_PER_DAY = TOTAL_ENDGAME_BENEFITS / 365 # ~$45.2B
ENDGAME_BENEFIT_PER_HOUR = ENDGAME_BENEFIT_PER_DAY / 24 # ~$1.9B
ENDGAME_BENEFIT_PER_SECOND = ENDGAME_BENEFIT_PER_HOUR / 3600 # ~$523K

# ---
# SCENARIO PARAMETERS
# ---

MILITARY_SPENDING_REMAINING = MILITARY_SPENDING * (1 - TREATY_REDUCTION_PCT) # $2,690.82B

# Partial success scenario (US, EU, UK only)
PARTIAL_SUCCESS_MILITARY_SPENDING_SHARE = 0.50  # ~50% of global spending
PARTIAL_SUCCESS_DIH_REVENUE = MILITARY_SPENDING * PARTIAL_SUCCESS_MILITARY_SPENDING_SHARE * TREATY_REDUCTION_PCT # ~$13.6B
PARTIAL_SUCCESS_BONDHOLDER_PAYOUT = PARTIAL_SUCCESS_DIH_REVENUE * VICTORY_BOND_FUNDING_PCT # ~$1.36B
PARTIAL_SUCCESS_RESEARCH_FUNDING = PARTIAL_SUCCESS_DIH_REVENUE * DIH_TREASURY_TO_RESEARCH_PCT # ~$12.2B
PARTIAL_SUCCESS_INVESTOR_ROI = PARTIAL_SUCCESS_BONDHOLDER_PAYOUT / CAMPAIGN_TOTAL_COST # ~135.9%

# ---
# SENSITIVITY ANALYSIS SCENARIOS
# ---

# Source: brain/book/appendix/icer-full-calculation.qmd sensitivity tables

# Conservative scenario
SENSITIVITY_PEACE_DIVIDEND_CONSERVATIVE = 50.0  # $50B
SENSITIVITY_DFDA_SAVINGS_CONSERVATIVE = 25.0  # $25B
SENSITIVITY_TOTAL_BENEFITS_CONSERVATIVE = 75.0  # $75B
SENSITIVITY_CAMPAIGN_COST_CONSERVATIVE = 0.333  # $333M/year (3-year amortization)
SENSITIVITY_DFDA_OPEX_CONSERVATIVE = 0.060  # $60M/year
SENSITIVITY_TOTAL_COSTS_CONSERVATIVE = 0.393  # $393M/year
SENSITIVITY_PEACE_QALYS_CONSERVATIVE = 17500  # 500 lives × 35 QALYs/life
SENSITIVITY_DFDA_QALYS_CONSERVATIVE = 420000  # Conservative health benefit
SENSITIVITY_TOTAL_QALYS_CONSERVATIVE = 437500  # Total QALYs
SENSITIVITY_NET_BENEFIT_CONSERVATIVE = 74.6  # $74.6B
SENSITIVITY_ICER_CONSERVATIVE = -170514  # -$170,514 per QALY
SENSITIVITY_COST_PER_LIFE_CONSERVATIVE = -5.97  # -$5.97M per life (in millions)

# Central scenario (baseline)
SENSITIVITY_PEACE_DIVIDEND_CENTRAL = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT  # $114B
SENSITIVITY_DFDA_SAVINGS_CENTRAL = DFDA_GROSS_SAVINGS  # $50B
SENSITIVITY_TOTAL_BENEFITS_CENTRAL = TOTAL_ANNUAL_BENEFITS  # $164B
SENSITIVITY_CAMPAIGN_COST_CENTRAL = CAMPAIGN_ANNUAL_COST_AMORTIZED  # $250M/year
SENSITIVITY_DFDA_OPEX_CENTRAL = DFDA_ANNUAL_OPEX  # $40M/year
SENSITIVITY_TOTAL_COSTS_CENTRAL = TOTAL_ANNUAL_COSTS  # $290M/year
SENSITIVITY_PEACE_QALYS_CENTRAL = PEACE_QALYS_ANNUAL  # 35,000 QALYs
SENSITIVITY_DFDA_QALYS_CENTRAL = DFDA_QALYS_ANNUAL  # 840,000 QALYs
SENSITIVITY_TOTAL_QALYS_CENTRAL = TOTAL_QALYS_ANNUAL  # 875,000 QALYs
SENSITIVITY_NET_BENEFIT_CENTRAL = NET_ANNUAL_BENEFIT  # $163.7B
SENSITIVITY_ICER_CENTRAL = -187097  # -$187,097 per QALY
SENSITIVITY_COST_PER_LIFE_CENTRAL = -6.55  # -$6.55M per life (in millions)
SENSITIVITY_LIVES_SAVED_CENTRAL = SENSITIVITY_TOTAL_QALYS_CENTRAL / QALYS_PER_LIFE # 25,000

# Optimistic scenario
SENSITIVITY_PEACE_DIVIDEND_OPTIMISTIC = 200.0  # $200B
SENSITIVITY_DFDA_SAVINGS_OPTIMISTIC = 95.0  # $95B
SENSITIVITY_TOTAL_BENEFITS_OPTIMISTIC = 295.0  # $295B
SENSITIVITY_CAMPAIGN_COST_OPTIMISTIC = 0.200  # $200M/year (5-year amortization)
SENSITIVITY_DFDA_OPEX_OPTIMISTIC = 0.030  # $30M/year
SENSITIVITY_TOTAL_COSTS_OPTIMISTIC = 0.230  # $230M/year
SENSITIVITY_PEACE_QALYS_OPTIMISTIC = 52500  # 1,500 lives × 35 QALYs/life
SENSITIVITY_DFDA_QALYS_OPTIMISTIC = 2100000  # Optimistic health benefit
SENSITIVITY_TOTAL_QALYS_OPTIMISTIC = 2152500  # Total QALYs
SENSITIVITY_NET_BENEFIT_OPTIMISTIC = 294.8  # $294.8B
SENSITIVITY_ICER_OPTIMISTIC = -136945  # -$136,945 per QALY
SENSITIVITY_COST_PER_LIFE_OPTIMISTIC = -4.79  # -$4.79M per life (in millions)

# Alternative ICER calculations based on funding perspective
# Source: icer-full-calculation.qmd alternative ICER table
ICER_CONSERVATIVE_ALL_COSTS = SENSITIVITY_ICER_CONSERVATIVE  # -$187,097 (counts all costs)
ICER_INVESTOR_FUNDED = -187429  # -$187,429 (campaign funded by VICTORY bonds, cost = $0)
ICER_OPPORTUNITY_COST = -156571  # -$156,571 (counts $27B redirected military spending)
ICER_WASTE_CONVERSION = None  # Undefined (military spending has negative ROI)

COST_PER_LIFE_CONSERVATIVE_ALL_COSTS = SENSITIVITY_COST_PER_LIFE_CENTRAL  # -$6.55M
COST_PER_LIFE_INVESTOR_FUNDED = -6.56  # -$6.56M
COST_PER_LIFE_OPPORTUNITY_COST = -5.48  # -$5.48M
COST_PER_LIFE_WASTE_CONVERSION = None  # Undefined

# ---
# HELPER FUNCTIONS
# ---

def format_billions(value):
    """Format a number as billions with B suffix

    Args:
        value: Number in billions

    Returns:
        Formatted string like "$50.0B"
    """
    if value >= 1000:
        return f"${value/1000:,.1f}T"
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
        return f"${value/1000:,.1f}T"
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

# ---
# VALIDATION FUNCTIONS
# ---

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
    if abs(DFDA_ROI_SIMPLE - expected_roi) > 1:
        errors.append(f"dFDA ROI mismatch: {DFDA_ROI_SIMPLE} vs {expected_roi}")

    # Check complete benefits sum
    calculated_complete = (BENEFIT_PEACE_DIVIDEND + BENEFIT_RD_SAVINGS + BENEFIT_EARLIER_ACCESS +
                          BENEFIT_RESEARCH_ACCELERATION + BENEFIT_RARE_DISEASES +
                          BENEFIT_DRUG_PRICE_REDUCTION + BENEFIT_PREVENTION + BENEFIT_MENTAL_HEALTH)
    if abs(TOTAL_COMPLETE_BENEFITS - calculated_complete) > 0.1:
        errors.append(f"Complete benefits mismatch: {TOTAL_COMPLETE_BENEFITS} vs {calculated_complete}")

    # Check campaign budget breakdown sums to total
    campaign_budget_sum = (CAMPAIGN_BUDGET_VIRAL_REFERENDUM + CAMPAIGN_BUDGET_AI_LOBBYING +
                          CAMPAIGN_BUDGET_TECHNOLOGY + CAMPAIGN_BUDGET_LEGAL +
                          CAMPAIGN_BUDGET_PARTNERSHIPS + CAMPAIGN_BUDGET_OPERATIONS + CAMPAIGN_BUDGET_RESERVE)
    if abs(campaign_budget_sum - CAMPAIGN_TOTAL_COST) > 0.001:
        errors.append(f"Campaign budget breakdown mismatch: {campaign_budget_sum} vs {CAMPAIGN_TOTAL_COST}")

    # Check dFDA opex breakdown sums to total
    dfda_opex_sum = (DFDA_OPEX_PLATFORM_MAINTENANCE + DFDA_OPEX_STAFF + DFDA_OPEX_INFRASTRUCTURE +
                    DFDA_OPEX_REGULATORY + DFDA_OPEX_COMMUNITY)
    if abs(dfda_opex_sum - DFDA_ANNUAL_OPEX) > 0.001:
        errors.append(f"dFDA opex breakdown mismatch: {dfda_opex_sum} vs {DFDA_ANNUAL_OPEX}")

    # Check conflict deaths sum to total
    conflict_deaths_sum = (CONFLICT_DEATHS_ACTIVE_COMBAT + CONFLICT_DEATHS_TERROR_ATTACKS +
                          CONFLICT_DEATHS_STATE_VIOLENCE)
    if abs(conflict_deaths_sum - ANNUAL_CONFLICT_DEATHS) > 1:
        errors.append(f"Conflict deaths breakdown mismatch: {conflict_deaths_sum} vs {ANNUAL_CONFLICT_DEATHS}")

    # Warnings for values that should be close but might differ slightly
    if abs(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT - 114.0) > 1.0:
        warnings.append(f"Societal dividend is {PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT}, expected ~114B")

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

# --- Module Initialization ---

if __name__ == "__main__":
    # Run validation when module is executed directly
    if not validate_parameters():
        exit(1)


# ---
# COST OF WAR DETAILS (for cost-of-war.qmd)
# ---

# Value of Statistical Life (VSL)
VALUE_OF_STATISTICAL_LIFE = 10_000_000  # $10 million, conservative value used in calculations
VSL_DOT_MILLIONS = 13.6  # $13.6M, reference value from Dept. of Transportation
VSL_EPA_MILLIONS = 9.6  # $9.6M, reference value from EPA

# Breakdown of Human Life Loss Costs (billions USD)
HUMAN_COST_ACTIVE_COMBAT = CONFLICT_DEATHS_ACTIVE_COMBAT * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000  # $2,336B
HUMAN_COST_TERROR_ATTACKS = CONFLICT_DEATHS_TERROR_ATTACKS * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000 # $83B
HUMAN_COST_STATE_VIOLENCE = CONFLICT_DEATHS_STATE_VIOLENCE * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000 # $27B

# Derived time-based costs
SECONDS_PER_YEAR = 365 * 24 * 60 * 60
DIRECT_COST_PER_SECOND = TOTAL_DIRECT_COSTS * 1_000_000_000 / SECONDS_PER_YEAR # ~$242,749

# Refugee parameters
FORCIBLY_DISPLACED_PEOPLE = 108_400_000
COST_PER_REFUGEE_PER_YEAR = 1384

# Grotesque Mathematics calculations
COST_PER_CONFLICT_DEATH_MILLIONS = TOTAL_WAR_COST * 1_000_000_000 / ANNUAL_CONFLICT_DEATHS / 1_000_000 # ~$46.4M
LIVES_SAVED_BY_MED_RESEARCH = 4_200_000
COST_PER_LIFE_SAVED_MED_RESEARCH = GLOBAL_MED_RESEARCH_SPENDING * 1_000_000_000 / LIVES_SAVED_BY_MED_RESEARCH # ~$16,071
MISALLOCATION_FACTOR_DEATH_VS_SAVING = (TOTAL_WAR_COST * 1_000_000_000 / ANNUAL_CONFLICT_DEATHS) / COST_PER_LIFE_SAVED_MED_RESEARCH # ~2,889x

# Specific budget items from text
NUCLEAR_WEAPONS_ANNUAL_BUDGET_INCREASE = 42.0 # billions USD

# ---
# COST OF WAR DETAILS (for cost-of-war.qmd) - Additional Parameters
# ---

# Military Spending Breakdown (billions USD)
MILITARY_SPENDING_PERSONNEL = 681.5
MILITARY_SPENDING_PROCUREMENT = 654.3
MILITARY_SPENDING_OPERATIONS_MAINTENANCE = 579.8
MILITARY_SPENDING_INFRASTRUCTURE = 520.4
MILITARY_SPENDING_INTELLIGENCE = 282.0

# Infrastructure Damage Breakdown (billions USD)
INFRASTRUCTURE_DAMAGE_TRANSPORTATION = 487.3
INFRASTRUCTURE_DAMAGE_ENERGY = 421.7
INFRASTRUCTURE_DAMAGE_COMMUNICATIONS = 298.1
INFRASTRUCTURE_DAMAGE_WATER = 267.8
INFRASTRUCTURE_DAMAGE_EDUCATION = 234.5
INFRASTRUCTURE_DAMAGE_HEALTHCARE = 165.6

# Trade Disruption Breakdown (billions USD)
TRADE_DISRUPTION_SHIPPING = 247.1
TRADE_DISRUPTION_SUPPLY_CHAIN = 186.8
TRADE_DISRUPTION_ENERGY_PRICE = 124.7
TRADE_DISRUPTION_CURRENCY = 57.4

# Opportunity Cost Parameters
GLOBAL_EDUCATION_FOR_ALL_COST = 30.0  # billions USD
POVERTY_ERADICATION_COST = 1000.0  # billions USD
MULTIPLIER_MILITARY_SPENDING = 0.6
MULTIPLIER_INFRASTRUCTURE = 1.6
MULTIPLIER_EDUCATION = 2.1
MULTIPLIER_HEALTHCARE = 4.3

# Refugee Parameters
REFUGEE_LOST_EARNING_POTENTIAL_PER_CAPITA_ANNUAL = 23400  # USD per year
REFUGEE_LOST_PRODUCTIVITY_GLOBAL_TOTAL = (FORCIBLY_DISPLACED_PEOPLE * REFUGEE_LOST_EARNING_POTENTIAL_PER_CAPITA_ANNUAL) / 1_000_000_000  # $2,536.6B

# Contextual / Comparison Parameters
GLOBAL_GDP_2023 = 89500  # billions USD, for 2023 comparison
TOTAL_WAR_COST_TO_WHO_BUDGET_RATIO = 168  # Total war cost is 168x WHO budget (or similar sized org)


# ---
# NEW PARAMETERS ADDED FROM CHAPTER ANALYSIS (2025-01-24)
# ---

# Alias for consistency with book text
CAPTURED_DIVIDEND = TREATY_ANNUAL_FUNDING # Alias for TREATY_ANNUAL_FUNDING as used in some chapter contexts

# Campaign & Strategy Specifics
CAMPAIGN_BUDGET_MASS_BRIBERY = 0.140 # billions USD, for bribing the masses (voting bloc build)
CAMPAIGN_VOTING_BLOC_SIZE_MILLIONS = 280 # millions of people, target voting bloc size
CAMPAIGN_BUDGET_SUPER_PACS = 0.800 # billions USD, for Super PACs/politician bribery
GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT = 0.035 # 3.5% rule for social change, key tipping point
CAMPAIGN_COST_PER_VOTE_MIN_USD = 0.20 # USD per vote, minimum for mass bribery campaign
CAMPAIGN_COST_PER_VOTE_MAX_USD = 0.50 # USD per vote, maximum for mass bribery campaign

# Clinical Trial Cost Examples & Comparisons
TRADITIONAL_PHASE3_COST_PER_PATIENT_EXAMPLE_48K = 48000 # USD per trial patient, specific example from text for comparison
TRADITIONAL_PHASE3_COST_PER_PATIENT_FDA_EXAMPLE_41K = 41000 # USD per patient, cited FDA cost example for comparison

# Historical & Comparison Multipliers
MILITARY_VS_MEDICAL_RESEARCH_RATIO = MILITARY_SPENDING / GLOBAL_MED_RESEARCH_SPENDING # Calculated ratio of military to medical research spending
DEATH_SPENDING_MISALLOCATION_FACTOR = 1750 # Multiplier for spending on death vs prevention (specific citation in text)
POST_WW2_MILITARY_CUT_PCT = 0.30 # Percentage military spending cut after WW2, historical precedent
SWITZERLAND_DEFENSE_SPENDING_PCT = 0.007 # Switzerland's defense spending as percentage of GDP
SWITZERLAND_GDP_PER_CAPITA_K = 93 # Thousands USD, Switzerland GDP per capita, for comparison
LOBBYING_ROI_DEFENSE = 1813 # Dollars returned per dollar spent lobbying defense, cited statistic
WW2_BOND_RETURN_PCT = 0.04 # WWII bond return percentage, historical comparison
AVERAGE_MARKET_RETURN_PCT = 0.10 # Average market return percentage for portfolio comparisons

# Victory Bonds derived payout (per unit of investment)
VICTORY_BOND_INVESTMENT_UNIT_USD = 1000 # USD, per bond investment unit for retail investors
VICTORY_BOND_PAYOUT_PER_UNIT_USD_ANNUAL = (VICTORY_BOND_ANNUAL_PAYOUT / VICTORY_BOND_UPFRONT_RAISE) * VICTORY_BOND_INVESTMENT_UNIT_USD # Derived from total payout and total raise

# Lobbyist compensation & incentives
LOBBYIST_BOND_INVESTMENT_MIN_MILLIONS = 5 # Millions USD, bond investment for lobbyists (min incentive)
LOBBYIST_BOND_INVESTMENT_MAX_MILLIONS = 20 # Millions USD, bond investment for lobbyists (max incentive)
LOBBYIST_SALARY_TYPICAL_K = 500 # Thousands USD, typical lobbyist salary, for comparison

# QALYs Breakdown & Treatment Acceleration Details
QALYS_FROM_FASTER_ACCESS = 200000 # QALYs gained annually from faster drug access
QALYS_FROM_PREVENTION = 140000 # QALYs gained annually from better prevention through real-world data
QALYS_FROM_NEW_THERAPIES = 500000 # QALYs gained annually from enabling new therapies for rare/untreatable diseases
TREATMENT_ACCELERATION_YEARS_TARGET = 2 # Years to market with dFDA (target)
TREATMENT_ACCELERATION_YEARS_CURRENT = 17 # Years to market with traditional FDA (current)

# Specific benefit sum (used for the $147.1B figure in the "Where Math Breaks" section)
# This sum is distinct from TOTAL_ANNUAL_BENEFITS which uses different categories for broader calculation.
COMBINED_PEACE_HEALTH_DIVIDENDS_FOR_ROI_CALC = BENEFIT_PEACE_DIVIDEND + BENEFIT_RD_SAVINGS

# System effectiveness & ROI comparisons
PROFIT_PER_LIFE_SAVED = 167771 # USD, profit per life saved from the system (specific calculation in text)
SYSTEM_PROFIT_PER_LIFE_SAVED_MILLIONS = 5.87 # Millions USD, system profit per life saved (specific phrasing in text)
SYSTEM_BENEFIT_VS_VACCINES_MULTIPLIER = 10 # Multiplier for system benefit vs childhood vaccines

# Price of Procrastination Metrics
DEATHS_DURING_READING_SECTION = 410 # Number of deaths from curable diseases during reading a section
DAILY_COST_INEFFICIENCY = 0.327 # billions USD, daily cost of inefficiency
