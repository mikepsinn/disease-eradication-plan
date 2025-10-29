"""
Economic Parameters - Single Source of Truth
=============================================

This module contains all economic parameters used throughout the book.
All calculations should import from this module to ensure consistency.

Last updated: 2025-01-24
Version: 1.0.0

Usage:
    from economic_parameters import *
    print(f"Military spending: {format_billions(GLOBAL_MILITARY_SPENDING_ANNUAL_2024)}")
    print(f"Peace dividend: {format_billions(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT)}")
"""

# ---
# PEACE DIVIDEND PARAMETERS
# ---

# Total cost of war (billions USD)
# Source: brain/book/problem/cost-of-war.qmd
# Reference: references.qmd#total-military-and-war-costs-11-4t

# Direct costs
GLOBAL_MILITARY_SPENDING_ANNUAL_2024 = 2718.0  # billions USD, SIPRI 2024

# Value of Statistical Life (VSL)
VALUE_OF_STATISTICAL_LIFE = 10_000_000  # $10 million, conservative value used in calculations

# Conflict death breakdown (for QALY calculations)
# Source: brain/book/problem/cost-of-war.qmd#death-accounting
GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT = 233600  # ACLED data
GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS = 8300  # Global Terrorism Database
GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE = 2700  # Uppsala Conflict Data Program

# Total conflict deaths (calculated from breakdown)
GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL = (
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE
)  # 244,600

# Breakdown of Human Life Loss Costs (billions USD)
GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT = GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000  # $2,336B
GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS = GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000 # $83B
GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE = GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000 # $27B

# Total human life losses (calculated from breakdown)
GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT = (
    GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS
    + GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE
)  # $2,446B

# Infrastructure Damage Breakdown (billions USD)
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT = 487.3
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT = 421.7
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT = 298.1
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT = 267.8
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT = 234.5
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT = 165.6

# Total infrastructure destruction (calculated from breakdown)
GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT = (
    GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT
)  # $1,875B

# Trade Disruption Breakdown (billions USD)
GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT = 247.1
GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT = 186.8
GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT = 124.7
GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT = 57.4

# Total trade disruption (calculated from breakdown)
GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT = (
    GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT
)  # $616B

GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL = (
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT
    + GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT
)  # $7,655B

# Indirect costs
GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING = 2718.0  # billions USD, opportunity cost of military spending
GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS = 200.1  # billions USD, 20-year projected costs
GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS = 150.0  # billions USD, 108.4M refugees × $1,384/year
GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT = 100.0  # billions USD, environmental restoration costs
GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT = 232.0  # billions USD, PTSD and mental health costs
GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT = 300.0  # billions USD, lost productivity from casualties

GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL = (
    GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING
    + GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS
    + GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS
    + GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT
    + GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT
    + GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT
)  # $3,700.1B

# Grand total war costs
GLOBAL_ANNUAL_WAR_TOTAL_COST = GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL + GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL  # $11,355.1B

# Treaty parameters
TREATY_REDUCTION_PCT = 0.01  # 1% reduction in military spending/war costs
TREATY_ANNUAL_FUNDING = GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * TREATY_REDUCTION_PCT  # $27.18B
PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT = GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT  # $113.55B, rounded to $114B

# ---
# HEALTH DIVIDEND PARAMETERS (dFDA)
# ---

# Clinical trial market
# Source: brain/book/appendix/dfda-roi-calculations.qmd
GLOBAL_CLINICAL_TRIAL_MARKET_ANNUAL = 100.0  # billions USD annually
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
DFDA_GROSS_SAVINGS_ANNUAL = GLOBAL_CLINICAL_TRIAL_MARKET_ANNUAL * TRIAL_COST_REDUCTION_PCT  # $50B
DFDA_NET_SAVINGS_ANNUAL = DFDA_GROSS_SAVINGS_ANNUAL - DFDA_ANNUAL_OPEX  # $49.96B

# Simple ROI (not NPV-adjusted)
DFDA_ROI_SIMPLE = DFDA_GROSS_SAVINGS_ANNUAL / DFDA_ANNUAL_OPEX  # 1,250:1
# NOTE: For NPV-adjusted ROI (463:1), use ROI_DFDA_SAVINGS_ONLY below
# The NPV-based calculation accounts for time value of money and gradual adoption

# ---
# HEALTH IMPACT PARAMETERS
# ---

# QALY valuations
# Source: brain/book/appendix/icer-full-calculation.qmd
STANDARD_ECONOMIC_QALY_VALUE_USD = 150000  # Standard economic value per QALY
STANDARD_QALYS_PER_LIFE_SAVED = 35  # Standard assumption (WHO life tables)

# dFDA health benefits
GLOBAL_DFDA_QALYS_GAINED_ANNUAL = 840000  # QALYs gained per year from dFDA
DFDA_QALYS_MONETIZED = (GLOBAL_DFDA_QALYS_GAINED_ANNUAL * STANDARD_ECONOMIC_QALY_VALUE_USD) / 1_000_000_000  # $126B

# Peace dividend health benefits
TREATY_LIVES_SAVED_ANNUAL_GLOBAL = GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL * TREATY_REDUCTION_PCT  # 2,446 lives
TREATY_QALYS_GAINED_ANNUAL_GLOBAL = TREATY_LIVES_SAVED_ANNUAL_GLOBAL * STANDARD_QALYS_PER_LIFE_SAVED  # 85,610 QALYs

# Combined health benefits
TREATY_TOTAL_QALYS_GAINED_ANNUAL = GLOBAL_DFDA_QALYS_GAINED_ANNUAL + TREATY_QALYS_GAINED_ANNUAL_GLOBAL  # 925,610 QALYs
TREATY_TOTAL_LIVES_SAVED_ANNUAL = TREATY_TOTAL_QALYS_GAINED_ANNUAL / STANDARD_QALYS_PER_LIFE_SAVED  # 26,446 lives

# ---
# CAMPAIGN COSTS
# ---

# Source: brain/book/economics/campaign-budget.qmd
TREATY_CAMPAIGN_TOTAL_COST = 1.0  # $1B total campaign cost
TREATY_CAMPAIGN_DURATION_YEARS = 4  # 3-5 year range, using midpoint
TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED = TREATY_CAMPAIGN_TOTAL_COST / TREATY_CAMPAIGN_DURATION_YEARS  # $250M

# Campaign budget breakdown (in billions)
TREATY_CAMPAIGN_BUDGET_VIRAL_REFERENDUM = 0.200  # $200M viral referendum
TREATY_CAMPAIGN_BUDGET_AI_LOBBYING = 0.250  # $250M AI-assisted lobbying
TREATY_CAMPAIGN_BUDGET_TECHNOLOGY = 0.250  # $250M technology platform
TREATY_CAMPAIGN_BUDGET_LEGAL = 0.100  # $100M legal & compliance
TREATY_CAMPAIGN_BUDGET_PARTNERSHIPS = 0.100  # $100M partnerships
TREATY_CAMPAIGN_BUDGET_OPERATIONS = 0.050  # $50M operations
TREATY_CAMPAIGN_BUDGET_RESERVE = 0.050  # $50M reserve
# Total should equal TREATY_CAMPAIGN_TOTAL_COST ($1B)

# Total system costs
TREATY_TOTAL_ANNUAL_COSTS = TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED + DFDA_ANNUAL_OPEX  # $290M ($0.29B)

# ---
# COMBINED ECONOMICS
# ---

# Total annual benefits
TREATY_TOTAL_ANNUAL_BENEFITS = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + DFDA_GROSS_SAVINGS_ANNUAL  # $164B (rounded from $163.55B)

# Net benefit
TREATY_NET_ANNUAL_BENEFIT = TREATY_TOTAL_ANNUAL_BENEFITS - TREATY_TOTAL_ANNUAL_COSTS  # $163.71B

# ICER calculation (Incremental Cost-Effectiveness Ratio)
# Negative ICER means society SAVES money while gaining QALYs
ICER_PER_QALY = (TREATY_TOTAL_ANNUAL_COSTS - TREATY_TOTAL_ANNUAL_BENEFITS) / TREATY_TOTAL_QALYS_GAINED_ANNUAL  # -$176,907 per QALY
NET_BENEFIT_PER_LIFE_SAVED = ICER_PER_QALY * STANDARD_QALYS_PER_LIFE_SAVED  # -$6.19M per life

# ---
# ROI TIERS
# ---

# Tier 1: Conservative - dFDA R&D savings only (10-year NPV)
# Source: brain/book/appendix/dfda-roi-calculations.qmd NPV analysis
ROI_DFDA_SAVINGS_ONLY = 463  # 463:1 from NPV analysis

# Tier 2: Complete - All direct benefits
# Source: brain/book/economics.qmd complete case section
# Note: Calculated as TOTAL_COMPLETE_BENEFITS_ANNUAL / TREATY_CAMPAIGN_TOTAL_COST
# Updated from 1,222:1 when war costs were revised from $9.7T to $11.355T
ROI_ALL_DIRECT_BENEFITS = 1239  # 1,239:1 from all 8 benefit categories

# Tier 3: Endgame - Year 20 with compounding effects
# Source: brain/book/economics.qmd endgame section
ROI_WITH_MULTIPLIER_EFFECTS = 25781  # 25,781:1 at maturity with multiplier effects

# ---
# FINANCIAL PARAMETERS
# ---

# NPV analysis parameters
# Source: brain/book/appendix/dfda-calculation-framework.qmd
NPV_DISCOUNT_RATE_STANDARD = 0.08  # 8% annual discount rate (r)
NPV_TIME_HORIZON_YEARS = 10  # Standard 10-year analysis window (T)

# NPV Model - Component Costs
# Core platform and broader initiative costs (for detailed breakdowns)
DFDA_NPV_UPFRONT_COST = 0.040  # $40M core platform build
DIH_NPV_UPFRONT_COST_INITIATIVES = 0.22975  # $228M medium case broader initiatives
DFDA_NPV_ANNUAL_OPEX = 0.01895  # $19M core platform (midpoint of $11-26.5M)
DIH_NPV_ANNUAL_OPEX_INITIATIVES = 0.02110  # $21.1M medium case broader initiatives

# NPV Model - Primary Parameters (dFDA-specific)
# Total upfront costs (C0): combines core dFDA platform + broader DIH initiative setup
DFDA_NPV_UPFRONT_COST_TOTAL = DFDA_NPV_UPFRONT_COST + DIH_NPV_UPFRONT_COST_INITIATIVES  # C0 = $0.26975B

# Total annual operational costs (Cop): combines core dFDA platform + broader DIH initiative annual costs
DFDA_NPV_ANNUAL_OPEX_TOTAL = DFDA_NPV_ANNUAL_OPEX + DIH_NPV_ANNUAL_OPEX_INITIATIVES  # Cop = $0.04005B

# dFDA adoption curve: linear ramp from 0% to 100% over 5 years, then constant at 100%
DFDA_NPV_ADOPTION_RAMP_YEARS = 5  # Years to reach full adoption

# Calculated NPV values for dFDA
DFDA_NPV_PV_ANNUAL_OPEX = DFDA_NPV_ANNUAL_OPEX_TOTAL * (1 - (1 + NPV_DISCOUNT_RATE_STANDARD)**-NPV_TIME_HORIZON_YEARS) / NPV_DISCOUNT_RATE_STANDARD
DFDA_NPV_TOTAL_COST = DFDA_NPV_UPFRONT_COST_TOTAL + DFDA_NPV_PV_ANNUAL_OPEX  # ~$0.54B
DFDA_NPV_NET_BENEFIT_CONSERVATIVE = DFDA_NPV_TOTAL_COST * ROI_DFDA_SAVINGS_ONLY # ~$249B

# NOTE: The NPV-based ROI (463:1) accounts for time value of money and gradual adoption
# The simple ROI (1,250:1) is gross savings / annual opex without discounting
# Use ROI_DFDA_SAVINGS_ONLY (463:1) as the canonical figure for most purposes

# VICTORY bonds
# Source: brain/book/economics/victory-bonds.qmd
VICTORY_BOND_FUNDING_PCT = 0.10  # 10% of captured dividend funds bonds
VICTORY_BOND_ANNUAL_PAYOUT = TREATY_ANNUAL_FUNDING * VICTORY_BOND_FUNDING_PCT  # $2.718B
VICTORY_BOND_ANNUAL_RETURN_PCT = VICTORY_BOND_ANNUAL_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST  # 271.8% (reported as 270%)
VICTORY_BOND_PAYBACK_MONTHS = 12 / VICTORY_BOND_ANNUAL_RETURN_PCT  # 4.4 months
DIVIDEND_COVERAGE_FACTOR = TREATY_ANNUAL_FUNDING / DFDA_ANNUAL_OPEX # ~679x

# DIH Treasury allocations (in billions)
# Source: brain/book/appendix/icer-full-calculation.qmd
# Aliases removed - use TREATY_ANNUAL_FUNDING, VICTORY_BOND_ANNUAL_PAYOUT, DFDA_ANNUAL_OPEX directly
DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL_PCT = 1 - VICTORY_BOND_FUNDING_PCT # 90%
DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL = TREATY_ANNUAL_FUNDING - VICTORY_BOND_ANNUAL_PAYOUT  # $24.3B/year
DIH_TREASURY_TRIAL_SUBSIDIES_MIN = 10.0  # $10B/year clinical trial subsidies (minimum)
DIH_TREASURY_TRIAL_SUBSIDIES_MAX = 20.0  # $20B/year clinical trial subsidies (maximum)

# ---
# REFERENCE VALUES (for comparisons)
# ---

# Global economic context
GLOBAL_GDP_2024 = 111000  # billions USD (2024)
GLOBAL_HEALTHCARE_SPENDING_ANNUAL_2024 = 9800  # billions USD
GLOBAL_MED_RESEARCH_SPENDING = 67.5  # billions USD government spending
TOTAL_GLOBAL_WASTE_SPEND_ANNUAL = 118800 # billions USD, annual spend on military + disease

# Population
GLOBAL_POPULATION_2024 = 8.0  # billions of people
GLOBAL_DAILY_DEATHS_CURABLE_DISEASES = 150000 # Daily deaths from curable diseases

# Per capita calculations
GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL = GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_POPULATION_2024  # $340/person/year
GLOBAL_TOTAL_WAR_COST_PER_CAPITA_ANNUAL = GLOBAL_ANNUAL_WAR_TOTAL_COST / GLOBAL_POPULATION_2024  # $1,419/person/year
LIFETIME_WAR_COST_PER_CAPITA = GLOBAL_TOTAL_WAR_COST_PER_CAPITA_ANNUAL * 80  # $113,551 over 80-year life

# GiveWell charity comparison
# Source: brain/book/appendix/icer-full-calculation.qmd
GIVEWELL_COST_PER_LIFE_MIN = 3500  # Helen Keller International
GIVEWELL_COST_PER_LIFE_MAX = 5500  # Against Malaria Foundation
GIVEWELL_COST_PER_LIFE_AVG = 4500  # Midpoint

# Cost-effectiveness multiplier
MULTIPLIER_VS_GIVEWELL = abs(NET_BENEFIT_PER_LIFE_SAVED * 1_000_000_000) / GIVEWELL_COST_PER_LIFE_AVG  # ~1,376x more cost-effective

# Historical public health comparisons
SMALLPOX_ERADICATION_ROI = 280  # 280:1
CHILDHOOD_VACCINATION_ROI = 13  # 13:1
WATER_FLUORIDATION_ROI = 23  # 23:1

# ---
# COMPLETE BENEFITS BREAKDOWN (for 1,239:1 ROI calculation)
# ---

# Source: brain/book/economics.qmd complete case section
# Note: Peace dividend updated from $97.1B to $113.55B when total war costs were revised from $9.7T to $11.355T
# BENEFIT_PEACE_DIVIDEND_ANNUAL removed - use PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT directly
BENEFIT_RESEARCH_AND_DEVELOPMENT_SAVINGS_ANNUAL = 50.0  # 82x cheaper trials
BENEFIT_EARLIER_DRUG_ACCESS_ANNUAL = 300.0  # 7-year acceleration
BENEFIT_MEDICAL_RESEARCH_ACCELERATION_ANNUAL = 100.0  # 115x more research capacity
BENEFIT_RARE_DISEASES_ANNUAL = 400.0  # Orphan drug viability
BENEFIT_DRUG_PRICE_REDUCTION_ANNUAL = 100.0  # R&D savings passed to consumers
BENEFIT_PREVENTION_ANNUAL = 100.0  # Economic viability of prevention
BENEFIT_MENTAL_HEALTH_ANNUAL = 75.0  # Treatment gap reduction

TOTAL_COMPLETE_BENEFITS_ANNUAL = (
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT
    + BENEFIT_RESEARCH_AND_DEVELOPMENT_SAVINGS_ANNUAL
    + BENEFIT_EARLIER_DRUG_ACCESS_ANNUAL
    + BENEFIT_MEDICAL_RESEARCH_ACCELERATION_ANNUAL
    + BENEFIT_RARE_DISEASES_ANNUAL
    + BENEFIT_DRUG_PRICE_REDUCTION_ANNUAL
    + BENEFIT_PREVENTION_ANNUAL
    + BENEFIT_MENTAL_HEALTH_ANNUAL
)  # $1,238.55B (updated from $1,222B when war costs were revised)


# ---
# ENDGAME BENEFITS (for 25,781:1 ROI calculation)
# ---

# Source: brain/book/economics.qmd endgame section
ENDGAME_PRODUCTIVITY_GAINS_ANNUAL = 8400.0  # $8.4T from healthier workforce
ENDGAME_GLOBAL_TRADE_BENEFIT_ANNUAL = 2400.0  # $2.4T from reduced conflict
ENDGAME_INFRASTRUCTURE_SAVINGS_ANNUAL = 1900.0  # $1.9T from preserved infrastructure
ENDGAME_AVOIDED_CRISES_ANNUAL = 1500.0  # $1.5T from no refugee/war costs
ENDGAME_INNOVATION_BENEFIT_ANNUAL = 2000.0  # $2.0T from research acceleration

TOTAL_ENDGAME_BENEFITS_ANNUAL = (
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT  # Base peace dividend
    + DFDA_GROSS_SAVINGS_ANNUAL  # Base health dividend
    + ENDGAME_PRODUCTIVITY_GAINS_ANNUAL
    + ENDGAME_GLOBAL_TRADE_BENEFIT_ANNUAL
    + ENDGAME_INFRASTRUCTURE_SAVINGS_ANNUAL
    + ENDGAME_AVOIDED_CRISES_ANNUAL
    + ENDGAME_INNOVATION_BENEFIT_ANNUAL
)  # $16,514B (~$16.5T)


# COST OF DELAY PARAMETERS
# Source: brain/book/economics.qmd
# Note: These are derived for illustrative purposes in the text
ENDGAME_BENEFIT_PER_DAY = TOTAL_ENDGAME_BENEFITS_ANNUAL / 365 # ~$45.2B
ENDGAME_BENEFIT_PER_HOUR = ENDGAME_BENEFIT_PER_DAY / 24 # ~$1.9B
ENDGAME_BENEFIT_PER_SECOND = ENDGAME_BENEFIT_PER_HOUR / 3600 # ~$523K

# QALY delay costs (quality-adjusted life days lost per second of inaction)
COST_OF_DELAY_QALY_DAYS_PER_SECOND = (TREATY_TOTAL_QALYS_GAINED_ANNUAL / 365) / (365.25 * 24 * 60 * 60) # QALY days per second

# Deaths delay costs (preventable deaths per second from curable diseases)
COST_OF_DELAY_DEATHS_PER_SECOND = GLOBAL_DAILY_DEATHS_CURABLE_DISEASES / (24 * 60 * 60) # deaths per second

# ---
# SCENARIO PARAMETERS
# ---

GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024 = GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * (1 - TREATY_REDUCTION_PCT) # $2,690.82B

# Partial success scenario (US, EU, UK only)
PARTIAL_SUCCESS_MILITARY_SPENDING_SHARE = 0.50  # ~50% of global spending
PARTIAL_SUCCESS_DIH_REVENUE = GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * PARTIAL_SUCCESS_MILITARY_SPENDING_SHARE * TREATY_REDUCTION_PCT # ~$13.6B
PARTIAL_SUCCESS_BONDHOLDER_PAYOUT = PARTIAL_SUCCESS_DIH_REVENUE * VICTORY_BOND_FUNDING_PCT # ~$1.36B
PARTIAL_SUCCESS_RESEARCH_FUNDING = PARTIAL_SUCCESS_DIH_REVENUE * DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL_PCT # ~$12.2B
PARTIAL_SUCCESS_INVESTOR_ROI = PARTIAL_SUCCESS_BONDHOLDER_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST # ~135.9%

# ---
# QALYs Breakdown & Treatment Acceleration Details
# ---

# Base Case (Central Scenario) - Used as primary estimates throughout analysis
QALYS_FROM_FASTER_ACCESS = 200000 # QALYs gained annually from faster drug access (Base case)
QALYS_FROM_PREVENTION = 140000 # QALYs gained annually from better prevention through real-world data (Base case)
QALYS_FROM_NEW_THERAPIES = 500000 # QALYs gained annually from enabling new therapies for rare/untreatable diseases (Base case)

# Conservative Scenario - Lower bound estimates for QALY gains
QALYS_FROM_FASTER_ACCESS_CONSERVATIVE = 90000 # QALYs from faster access (15 drugs/yr × 1 yr accel × 6k QALYs/drug)
QALYS_FROM_PREVENTION_CONSERVATIVE = 50000 # QALYs from prevention (5M patients × 0.01 QALYs/patient)
QALYS_FROM_NEW_THERAPIES_CONSERVATIVE = 50000 # QALYs from new therapies (5 therapies/yr × 2k patients × 5 QALYs/patient)
QALYS_TOTAL_CONSERVATIVE = 190000 # Total conservative QALYs (90k + 50k + 50k)

# Optimistic Scenario - Upper bound estimates for QALY gains
QALYS_FROM_FASTER_ACCESS_OPTIMISTIC = 500000 # QALYs from faster access (25 drugs/yr × 2 yr accel × 10k QALYs/drug)
QALYS_FROM_PREVENTION_OPTIMISTIC = 150000 # QALYs from prevention (15M patients × 0.01 QALYs/patient)
QALYS_FROM_NEW_THERAPIES_OPTIMISTIC = 3000000 # QALYs from new therapies (20 therapies/yr × 10k patients × 15 QALYs/patient)
QALYS_TOTAL_OPTIMISTIC = 3650000 # Total optimistic QALYs (500k + 150k + 3M)

TREATMENT_ACCELERATION_YEARS_TARGET = 2 # Years to market with dFDA (target)
TREATMENT_ACCELERATION_YEARS_CURRENT = 17 # Years to market with traditional FDA (current)

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
SENSITIVITY_TOTAL_QALYS_CONSERVATIVE = SENSITIVITY_PEACE_QALYS_CONSERVATIVE + QALYS_TOTAL_CONSERVATIVE  # Total QALYs (peace + dFDA)
SENSITIVITY_NET_BENEFIT_CONSERVATIVE = 74.6  # $74.6B
SENSITIVITY_ICER_CONSERVATIVE = -170514  # -$170,514 per QALY
SENSITIVITY_COST_PER_LIFE_CONSERVATIVE = -5.97  # -$5.97M per life (in millions)

# Central scenario (baseline) - uses main parameters directly, no aliases needed
SENSITIVITY_ICER_CENTRAL = -187097  # -$187,097 per QALY
SENSITIVITY_COST_PER_LIFE_CENTRAL = -6.55  # -$6.55M per life (in millions)
SENSITIVITY_LIVES_SAVED_CENTRAL = TREATY_TOTAL_QALYS_GAINED_ANNUAL / STANDARD_QALYS_PER_LIFE_SAVED # 25,000

# Optimistic scenario
SENSITIVITY_PEACE_DIVIDEND_OPTIMISTIC = 200.0  # $200B
SENSITIVITY_DFDA_SAVINGS_OPTIMISTIC = 95.0  # $95B
SENSITIVITY_TOTAL_BENEFITS_OPTIMISTIC = 295.0  # $295B
SENSITIVITY_CAMPAIGN_COST_OPTIMISTIC = 0.200  # $200M/year (5-year amortization)
SENSITIVITY_DFDA_OPEX_OPTIMISTIC = 0.030  # $30M/year
SENSITIVITY_TOTAL_COSTS_OPTIMISTIC = 0.230  # $230M/year
SENSITIVITY_PEACE_QALYS_OPTIMISTIC = 52500  # 1,500 lives × 35 QALYs/life
SENSITIVITY_TOTAL_QALYS_OPTIMISTIC = SENSITIVITY_PEACE_QALYS_OPTIMISTIC + QALYS_TOTAL_OPTIMISTIC  # Total QALYs (peace + dFDA)
SENSITIVITY_NET_BENEFIT_OPTIMISTIC = 294.8  # $294.8B
SENSITIVITY_ICER_OPTIMISTIC = -136945  # -$136,945 per QALY
SENSITIVITY_COST_PER_LIFE_OPTIMISTIC = -4.79  # -$4.79M per life (in millions)

# Sensitivity ROI calculations
CONSERVATIVE_SCENARIO_ROI = int(SENSITIVITY_NET_BENEFIT_CONSERVATIVE / SENSITIVITY_TOTAL_COSTS_CONSERVATIVE)  # 190:1
OPTIMISTIC_SCENARIO_ROI = int(SENSITIVITY_NET_BENEFIT_OPTIMISTIC / SENSITIVITY_TOTAL_COSTS_OPTIMISTIC)  # 1,282:1

# Alternative ICER calculations based on funding perspective
# Source: icer-full-calculation.qmd alternative ICER table
ICER_INVESTOR_FUNDED = -187429  # -$187,429 (campaign funded by VICTORY bonds, cost = $0)
ICER_OPPORTUNITY_COST = -156571  # -$156,571 (counts $27B redirected military spending)
ICER_WASTE_CONVERSION = None  # Undefined (military spending has negative ROI)

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

def format_billions_latex(value):
    """Format a number as billions with B suffix for LaTeX (no $ sign to avoid escaping issues)

    Args:
        value: Number in billions

    Returns:
        Formatted string like "163.6B" for LaTeX compatibility (without $ to avoid escaping)
    """
    if value >= 1000:
        return f"{value/1000:,.1f}T"
    return f"{value:,.1f}B"

# --- Module Initialization ---

if __name__ == "__main__":
    # Print some key parameters when module is executed directly
    print(f"Military spending: {format_billions(GLOBAL_MILITARY_SPENDING_ANNUAL_2024)}")
    print(f"Total war costs: {format_billions(GLOBAL_ANNUAL_WAR_TOTAL_COST)}")
    print(f"Peace dividend: {format_billions(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT)}")
    print(f"dFDA savings: {format_billions(DFDA_GROSS_SAVINGS_ANNUAL)}")
    print(f"Total benefits: {format_billions(TREATY_TOTAL_ANNUAL_BENEFITS)}")


# ---
# COST OF WAR DETAILS (for cost-of-war.qmd)
# ---

# Reference VSL values (for comparisons)
US_DOT_VALUE_OF_STATISTICAL_LIFE_MILLIONS = 13.6  # $13.6M, reference value from Dept. of Transportation
VSL_EPA_MILLIONS = 9.6  # $9.6M, reference value from EPA

# Derived time-based costs
SECONDS_PER_YEAR = 365 * 24 * 60 * 60
GLOBAL_WAR_DIRECT_COST_PER_SECOND = GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL * 1_000_000_000 / SECONDS_PER_YEAR # ~$242,749

# Refugee parameters
GLOBAL_FORCIBLY_DISPLACED_PEOPLE_2023 = 108_400_000
GLOBAL_COST_PER_REFUGEE_PER_YEAR_AVERAGE = 1384

# Grotesque Mathematics calculations
GLOBAL_COST_PER_CONFLICT_DEATH_MILLIONS = GLOBAL_ANNUAL_WAR_TOTAL_COST * 1_000_000_000 / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL / 1_000_000 # ~$46.4M
GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH = 4_200_000
GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL = GLOBAL_MED_RESEARCH_SPENDING * 1_000_000_000 / GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH # ~$16,071
MISALLOCATION_FACTOR_DEATH_VS_SAVING = (GLOBAL_ANNUAL_WAR_TOTAL_COST * 1_000_000_000 / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL) / GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL # ~2,889x

# Specific budget items from text
GLOBAL_NUCLEAR_WEAPONS_ANNUAL_BUDGET_INCREASE = 42.0 # billions USD

# ---
# COST OF WAR DETAILS (for cost-of-war.qmd) - Additional Parameters
# ---

# Military Spending Breakdown (billions USD)
GLOBAL_ANNUAL_MILITARY_SPENDING_PERSONNEL_2024 = 681.5
GLOBAL_ANNUAL_MILITARY_SPENDING_PROCUREMENT_2024 = 654.3
GLOBAL_ANNUAL_MILITARY_SPENDING_OPS_MAINTENANCE_2024 = 579.8
GLOBAL_ANNUAL_MILITARY_SPENDING_INFRASTRUCTURE_2024 = 520.4
GLOBAL_ANNUAL_MILITARY_SPENDING_INTELLIGENCE_2024 = 282.0

# Opportunity Cost Parameters
GLOBAL_EDUCATION_FOR_ALL_COST = 30.0  # billions USD
GLOBAL_POVERTY_ERADICATION_COST_TOTAL = 1000.0  # billions USD
ECONOMIC_MULTIPLIER_MILITARY_SPENDING = 0.6
ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT = 1.6
ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT = 2.1
ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT = 4.3

# Refugee Parameters
REFUGEE_LOST_EARNING_POTENTIAL_PER_CAPITA_ANNUAL = 23400  # USD per year
REFUGEE_LOST_PRODUCTIVITY_GLOBAL_TOTAL = (GLOBAL_FORCIBLY_DISPLACED_PEOPLE_2023 * REFUGEE_LOST_EARNING_POTENTIAL_PER_CAPITA_ANNUAL) / 1_000_000_000  # $2,536.6B

# Contextual / Comparison Parameters
GLOBAL_GDP_2023 = 89500  # billions USD, for 2023 comparison
TOTAL_WAR_COST_TO_WHO_BUDGET_RATIO = 168  # Total war cost is 168x WHO budget (or similar sized org)


# ---
# NEW PARAMETERS ADDED FROM CHAPTER ANALYSIS (2025-01-24)
# ---

# Alias for consistency with book text

# Campaign & Strategy Specifics
TREATY_CAMPAIGN_BUDGET_MASS_BRIBERY = 0.140 # billions USD, for bribing the masses (voting bloc build)
TREATY_CAMPAIGN_VOTING_BLOC_TARGET_MILLIONS = 280 # millions of people, target voting bloc size
TREATY_CAMPAIGN_BUDGET_SUPER_PACS = 0.800 # billions USD, for Super PACs/politician bribery
GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT = 0.035 # 3.5% rule for social change, key tipping point
TREATY_CAMPAIGN_COST_PER_VOTE_MIN_USD = 0.20 # USD per vote, minimum for mass bribery campaign
TREATY_CAMPAIGN_COST_PER_VOTE_MAX_USD = 0.50 # USD per vote, maximum for mass bribery campaign

# Clinical Trial Cost Examples & Comparisons
TRADITIONAL_PHASE3_COST_PER_PATIENT_EXAMPLE_48K = 48000 # USD per trial patient, specific example from text for comparison
TRADITIONAL_PHASE3_COST_PER_PATIENT_FDA_EXAMPLE_41K = 41000 # USD per patient, cited FDA cost example for comparison

# Historical & Comparison Multipliers
MILITARY_VS_MEDICAL_RESEARCH_RATIO = GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_MED_RESEARCH_SPENDING # Calculated ratio of military to medical research spending
DEATH_SPENDING_MISALLOCATION_FACTOR = 1750 # Multiplier for spending on death vs prevention (specific citation in text)
POST_WW2_MILITARY_CUT_PCT = 0.30 # Percentage military spending cut after WW2, historical precedent
SWITZERLAND_DEFENSE_SPENDING_PCT = 0.007 # Switzerland's defense spending as percentage of GDP
SWITZERLAND_GDP_PER_CAPITA_K = 93 # Thousands USD, Switzerland GDP per capita, for comparison
LOBBYING_ROI_DEFENSE = 1813 # Dollars returned per dollar spent lobbying defense, cited statistic
WW2_BOND_RETURN_PCT = 0.04 # WWII bond return percentage, historical comparison
AVERAGE_MARKET_RETURN_PCT = 0.10 # Average market return percentage for portfolio comparisons

# Victory Bonds derived payout (per unit of investment)
VICTORY_BOND_INVESTMENT_UNIT_USD = 1000 # USD, per bond investment unit for retail investors
VICTORY_BOND_PAYOUT_PER_UNIT_USD_ANNUAL = (VICTORY_BOND_ANNUAL_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST) * VICTORY_BOND_INVESTMENT_UNIT_USD # Derived from total payout and total raise

# Lobbyist compensation & incentives
LOBBYIST_BOND_INVESTMENT_MIN_MILLIONS = 5 # Millions USD, bond investment for lobbyists (min incentive)
LOBBYIST_BOND_INVESTMENT_MAX_MILLIONS = 20 # Millions USD, bond investment for lobbyists (max incentive)
LOBBYIST_SALARY_TYPICAL_K = 500 # Thousands USD, typical lobbyist salary, for comparison

# Specific benefit sum (used for the $147.1B figure in the "Where Math Breaks" section)
# This sum is distinct from TREATY_TOTAL_ANNUAL_BENEFITS which uses different categories for broader calculation.
COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + BENEFIT_RESEARCH_AND_DEVELOPMENT_SAVINGS_ANNUAL

# System effectiveness & ROI comparisons
PROFIT_PER_LIFE_SAVED = 167771 # USD, profit per life saved from the system (specific calculation in text)
SYSTEM_PROFIT_PER_LIFE_SAVED_MILLIONS = 5.87 # Millions USD, system profit per life saved (specific phrasing in text)
TREATY_BENEFIT_MULTIPLIER_VS_VACCINES = 10 # Multiplier: treaty system (1% Treaty + dFDA) benefit vs childhood vaccines program

# Price of Procrastination Metrics
DEATHS_DURING_READING_SECTION = 410 # Number of deaths from curable diseases during reading a section
DAILY_COST_INEFFICIENCY = 0.327 # billions USD, daily cost of inefficiency
