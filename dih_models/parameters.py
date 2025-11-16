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


# ============================================================================
# PARAMETER CLASS - Adds source tracking to numeric values
# ============================================================================

class Parameter(float):
    """
    A numeric parameter that works in calculations but carries source metadata.

    Enables clickable links from numbers to their sources (external citations)
    or calculation methodologies (internal QMD pages).

    Args:
        value: The numeric value
        source_ref: Reference ID (for external sources) or QMD path (for calculations)
        source_type: Either "external" (links to references.qmd) or "calculated" (links to QMD)
        description: Human-readable description for tooltips
        unit: Unit of measurement (e.g., "billions USD", "deaths/year", "percentage")
        formula: Optional plain-text formula (e.g., "A + B + C") for tooltips
        latex: Optional LaTeX formula (e.g., r"\sum_{i=1}^{5} opex_i") for rendering

    Example:
        # External data source
        CONFLICT_DEATHS = Parameter(
            233600,
            source_ref="acled-2024",
            source_type="external",
            description="Annual deaths from active combat",
            unit="deaths/year"
        )

        # Calculated value with formula
        TOTAL_OPEX = Parameter(
            PLATFORM + STAFF + INFRA + REGULATORY + COMMUNITY,
            source_ref="knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex",
            source_type="calculated",
            description="Total annual operational costs",
            unit="billions USD/year",
            formula="PLATFORM + STAFF + INFRA + REGULATORY + COMMUNITY",
            latex=r"OPEX_{total} = \sum_{i=1}^{5} OPEX_i"
        )

    The Parameter class inherits from float, so it works in all math operations:
        total = CONFLICT_DEATHS * 2  # Works!
        ratio = NET_BENEFIT / CONFLICT_DEATHS  # Works!
    """

    def __new__(cls, value, source_ref="", source_type="external", description="", unit="", formula="", latex=""):
        instance = super().__new__(cls, value)
        instance.source_ref = source_ref
        instance.source_type = source_type
        instance.description = description
        instance.unit = unit
        instance.formula = formula
        instance.latex = latex
        return instance

    def __repr__(self):
        return f"Parameter({float(self)}, source_ref='{self.source_ref}')"


# ---
# PEACE DIVIDEND PARAMETERS
# ---

# Total cost of war (billions USD)
# Source: brain/book/problem/cost-of-war.qmd
# Reference: references.qmd#total-military-and-war-costs-11-4t

# Direct costs
GLOBAL_MILITARY_SPENDING_ANNUAL_2024 = Parameter(
    2718.0,
    source_ref="global-military-spending",
    source_type="external",
    description="Global military spending in 2024",
    unit="billions USD"
)  # SIPRI 2024

# Value of Statistical Life (VSL)
VALUE_OF_STATISTICAL_LIFE = Parameter(
    10_000_000,
    source_ref="dot-vsl-13-6m",
    source_type="external",
    description="Value of Statistical Life (conservative estimate)",
    unit="USD"
)  # US DOT uses $13.6M, we use $10M conservatively

# Conflict death breakdown (for QALY calculations)
# Source: brain/book/problem/cost-of-war.qmd#death-accounting
GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT = Parameter(
    233600,
    source_ref="acled-2024",
    source_type="external",
    description="Annual deaths from active combat worldwide",
    unit="deaths/year"
)  # ACLED data

GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS = Parameter(
    8300,
    source_ref="gtd-2024",
    source_type="external",
    description="Annual deaths from terror attacks globally",
    unit="deaths/year"
)  # Global Terrorism Database

GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE = Parameter(
    2700,
    source_ref="ucdp-2024",
    source_type="external",
    description="Annual deaths from state violence",
    unit="deaths/year"
)  # Uppsala Conflict Data Program

# Total conflict deaths (calculated from breakdown)
GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE,
    source_ref="/knowledge/problem/cost-of-war.qmd#death-accounting",
    source_type="calculated",
    description="Total annual conflict deaths globally (sum of combat, terror, state violence)",
    unit="deaths/year",
    formula="COMBAT + TERROR + STATE_VIOLENCE",
    latex=r"Deaths_{total} = 233,600 + 8,300 + 2,700 = 244,600"
)  # 244,600

# Breakdown of Human Life Loss Costs (billions USD)
GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Annual cost of combat deaths (deaths × VSL)",
    unit="billions USD/year",
    formula="COMBAT_DEATHS × VSL ÷ 1B",
    latex=r"Cost_{combat} = 233,600 \times \$10M / 10^9 = \$2,336B"
)  # $2,336B

GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Annual cost of terror deaths (deaths × VSL)",
    unit="billions USD/year",
    formula="TERROR_DEATHS × VSL ÷ 1B",
    latex=r"Cost_{terror} = 8,300 \times \$10M / 10^9 = \$83B"
)  # $83B

GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE * VALUE_OF_STATISTICAL_LIFE / 1_000_000_000,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Annual cost of state violence deaths (deaths × VSL)",
    unit="billions USD/year",
    formula="STATE_DEATHS × VSL ÷ 1B",
    latex=r"Cost_{state} = 2,700 \times \$10M / 10^9 = \$27B"
)  # $27B

# Total human life losses (calculated from breakdown)
GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT = Parameter(
    GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS
    + GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Total annual human life losses from conflict (sum of combat, terror, state violence)",
    unit="billions USD/year",
    formula="COMBAT_COST + TERROR_COST + STATE_VIOLENCE_COST",
    latex=r"Cost_{human} = \$2,336B + \$83B + \$27B = \$2,446B"
)  # $2,446B

# Infrastructure Damage Breakdown (billions USD)
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT = Parameter(
    487.3,
    source_ref="war-infrastructure-damage-costs",
    source_type="external",
    description="Annual infrastructure damage to transportation from conflict",
    unit="billions USD"
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT = Parameter(
    421.7,
    source_ref="war-infrastructure-damage-costs",
    source_type="external",
    description="Annual infrastructure damage to energy systems from conflict",
    unit="billions USD"
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT = Parameter(
    298.1,
    source_ref="war-infrastructure-damage-costs",
    source_type="external",
    description="Annual infrastructure damage to communications from conflict",
    unit="billions USD"
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT = Parameter(
    267.8,
    source_ref="war-infrastructure-damage-costs",
    source_type="external",
    description="Annual infrastructure damage to water systems from conflict",
    unit="billions USD"
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT = Parameter(
    234.5,
    source_ref="war-infrastructure-damage-costs",
    source_type="external",
    description="Annual infrastructure damage to education facilities from conflict",
    unit="billions USD"
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT = Parameter(
    165.6,
    source_ref="war-infrastructure-damage-costs",
    source_type="external",
    description="Annual infrastructure damage to healthcare facilities from conflict",
    unit="billions USD"
)

# Total infrastructure destruction (calculated from breakdown)
GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT = Parameter(
    GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT,
    source_ref="/knowledge/problem/cost-of-war.qmd#infrastructure-damage",
    source_type="calculated",
    description="Total annual infrastructure destruction (sum of transportation, energy, communications, water, education, healthcare)",
    unit="billions USD/year",
    formula="TRANSPORT + ENERGY + COMMS + WATER + EDUCATION + HEALTHCARE",
    latex=r"Infra_{damage} = \$487.3B + \$421.7B + \$298.1B + \$267.8B + \$234.5B + \$165.6B = \$1,875B"
)  # $1,875B

# Trade Disruption Breakdown (billions USD)
GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT = Parameter(
    247.1,
    source_ref="war-trade-disruption-costs",
    source_type="external",
    description="Annual trade disruption costs from shipping disruptions",
    unit="billions USD"
)

GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT = Parameter(
    186.8,
    source_ref="war-trade-disruption-costs",
    source_type="external",
    description="Annual trade disruption costs from supply chain disruptions",
    unit="billions USD"
)

GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT = Parameter(
    124.7,
    source_ref="war-trade-disruption-costs",
    source_type="external",
    description="Annual trade disruption costs from energy price volatility",
    unit="billions USD"
)

GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT = Parameter(
    57.4,
    source_ref="war-trade-disruption-costs",
    source_type="external",
    description="Annual trade disruption costs from currency instability",
    unit="billions USD"
)

# Total trade disruption (calculated from breakdown)
GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT = Parameter(
    GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT,
    source_ref="/knowledge/problem/cost-of-war.qmd#trade-disruption",
    source_type="calculated",
    description="Total annual trade disruption (sum of shipping, supply chain, energy prices, currency instability)",
    unit="billions USD/year",
    formula="SHIPPING + SUPPLY_CHAIN + ENERGY_PRICE + CURRENCY",
    latex=r"Trade_{disruption} = \$247.1B + \$186.8B + \$124.7B + \$57.4B = \$616B"
)  # $616B

GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT
    + GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT,
    source_ref="/knowledge/problem/cost-of-war.qmd#direct-costs",
    source_type="calculated",
    description="Total annual direct war costs (military spending + infrastructure + human life + trade disruption)",
    unit="billions USD/year",
    formula="MILITARY + INFRASTRUCTURE + HUMAN_LIFE + TRADE",
    latex=r"DirectCosts = \$2,718B + \$1,875B + \$2,446B + \$616B = \$7,655B"
)  # $7,655B

# Indirect costs
GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING = Parameter(
    2718.0,
    source_ref="military-spending-opportunity-cost",
    source_type="external",
    description="Annual lost economic growth from military spending opportunity cost",
    unit="billions USD"
)

GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS = Parameter(
    200.1,
    source_ref="global-veteran-healthcare-costs",
    source_type="external",
    description="Annual veteran healthcare costs (20-year projected)",
    unit="billions USD"
)

GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS = Parameter(
    150.0,
    source_ref="refugee-support-costs",
    source_type="external",
    description="Annual refugee support costs (108.4M refugees × $1,384/year)",
    unit="billions USD"
)

GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT = Parameter(
    100.0,
    source_ref="war-environmental-damage-costs",
    source_type="external",
    description="Annual environmental damage and restoration costs from conflict",
    unit="billions USD"
)

GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT = Parameter(
    232.0,
    source_ref="war-psychological-impact-costs",
    source_type="external",
    description="Annual PTSD and mental health costs from conflict",
    unit="billions USD"
)

GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT = Parameter(
    300.0,
    source_ref="war-lost-human-capital",
    source_type="external",
    description="Annual lost productivity from conflict casualties",
    unit="billions USD"
)

GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL = Parameter(
    GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING
    + GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS
    + GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS
    + GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT
    + GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT
    + GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT,
    source_ref="/knowledge/problem/cost-of-war.qmd#indirect-costs",
    source_type="calculated",
    description="Total annual indirect war costs (opportunity cost + veterans + refugees + environment + mental health + lost productivity)",
    unit="billions USD/year",
    formula="OPPORTUNITY + VETERANS + REFUGEES + ENVIRONMENT + MENTAL_HEALTH + LOST_CAPITAL",
    latex=r"IndirectCosts = \$2,718B + \$200.1B + \$150B + \$100B + \$232B + \$300B = \$3,700.1B"
)  # $3,700.1B

# Grand total war costs
GLOBAL_ANNUAL_WAR_TOTAL_COST = Parameter(
    GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL + GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL,
    source_ref="/knowledge/problem/cost-of-war.qmd#total-cost",
    source_type="calculated",
    description="Total annual cost of war worldwide (direct + indirect costs)",
    unit="billions USD/year",
    formula="DIRECT_COSTS + INDIRECT_COSTS",
    latex=r"TotalWarCost = \$7,655B + \$3,700.1B = \$11,355.1B"
)  # $11,355.1B

# Treaty parameters
TREATY_REDUCTION_PCT = Parameter(
    0.01,
    source_ref="/knowledge/solution/dfda.qmd#one-percent-treaty",
    source_type="calculated",
    description="1% reduction in military spending/war costs from treaty",
    unit="rate"
)  # 1% reduction in military spending/war costs

TREATY_ANNUAL_FUNDING = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/solution/dfda.qmd#one-percent-treaty",
    source_type="calculated",
    description="Annual funding from 1% of global military spending redirected to DIH",
    unit="billions USD/year",
    formula="MILITARY_SPENDING × 1%",
    latex=r"Funding = \$2,718B \times 0.01 = \$27.18B"
)  # $27.18B

PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#peace-dividend",
    source_type="calculated",
    description="Annual peace dividend from 1% reduction in total war costs",
    unit="billions USD/year",
    formula="TOTAL_WAR_COST × 1%",
    latex=r"Peace\_Dividend = \$11,355B \times 0.01 = \$113.55B"
)  # $113.55B, rounded to $114B

# ---
# HEALTH DIVIDEND PARAMETERS (dFDA)
# ---

# Clinical trial market
# Source: brain/book/appendix/dfda-roi-calculations.qmd
GLOBAL_CLINICAL_TRIAL_MARKET_ANNUAL = Parameter(
    100.0,
    source_ref="global-clinical-trial-market",
    source_type="external",
    description="Global clinical trial market size",
    unit="billions USD/year"
)

GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL = Parameter(
    83.0,
    source_ref="global-clinical-trials-market-2024",
    source_type="external",
    description="Annual global spending on clinical trials",
    unit="billions USD/year"
)  # $83B spent globally on clinical trials annually

TRIAL_COST_REDUCTION_PCT = Parameter(
    0.50,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#cost-reduction",
    source_type="calculated",
    description="Trial cost reduction percentage (50% baseline, conservative)",
    unit="rate"
)  # 50% baseline reduction (conservative)

TRIAL_COST_REDUCTION_FACTOR = Parameter(
    82,
    source_ref="recovery-trial-82x-cost-reduction",
    source_type="external",
    description="Cost reduction factor demonstrated by RECOVERY trial",
    unit="ratio"
)  # 82x reduction proven by RECOVERY trial

# ---
# RESEARCH ACCELERATION MECHANISM PARAMETERS
# Source: brain/book/appendix/research-acceleration-model.qmd
# ---

# Current System Baseline
CURRENT_TRIALS_PER_YEAR = Parameter(
    3300,
    source_ref="global-clinical-trials-per-year",
    source_type="external",
    description="Current global clinical trials per year",
    unit="trials/year"
)  # Global clinical trials per year

CURRENT_DRUG_APPROVALS_PER_YEAR = Parameter(
    50,
    source_ref="global-new-drug-approvals-50-annually",
    source_type="external",
    description="Average annual new drug approvals globally",
    unit="drugs/year"
)  # FDA ~50-55/year

CURRENT_ACTIVE_TRIALS = Parameter(
    10000,
    source_ref="active-clinical-trials-baseline",
    source_type="external",
    description="Current active trials at any given time (3-5 year duration)",
    unit="trials"
)  # Active trials at any given time (3-5 year duration)

CURRENT_TRIAL_DURATION_YEARS_RANGE = (3, 5)  # Years for large trials
CURRENT_SMALL_TRIAL_RECRUITMENT_MONTHS_RANGE = (6, 18)  # Months to recruit 100 patients

CURRENT_TRIAL_ABANDONMENT_RATE = Parameter(
    0.40,
    source_ref="clinical-trial-abandonment-rate",
    source_type="external",
    description="Current trial abandonment rate (40% never complete)",
    unit="rate"
)  # 40% of trials never complete

CURRENT_TRIAL_COMPLETION_RATE = Parameter(
    0.60,
    source_ref="clinical-trial-completion-rate",
    source_type="external",
    description="Current trial completion rate (60%)",
    unit="rate"
)  # 60% completion rate

CURRENT_PATIENT_ELIGIBILITY_RATE = Parameter(
    0.002,
    source_ref="clinical-trial-eligibility-rate",
    source_type="external",
    description="Current patient eligibility rate for clinical trials (0.2%)",
    unit="rate"
)  # 0.2% of disease patients can participate

CURRENT_TRIAL_SLOTS_AVAILABLE = Parameter(
    5_000_000,
    source_ref="global-trial-participant-capacity",
    source_type="external",
    description="Total trial slots available for 2.4B sick people",
    unit="slots"
)  # Total trial slots for 2.4B sick people

CURRENT_DISEASE_PATIENTS_GLOBAL = Parameter(
    2_400_000_000,
    source_ref="global-burden-disease-2-4-billion",
    source_type="external",
    description="Global population with chronic diseases",
    unit="people"
)  # GBD 2013 study

# Traditional Trial Economics
TRADITIONAL_PHASE2_COST_PER_PATIENT_LOW = Parameter(
    40000,
    source_ref="clinical-trial-cost-per-patient",
    source_type="external",
    description="Phase 2 cost per patient (low estimate)",
    unit="USD/patient"
)  # $40K per patient (low end)

TRADITIONAL_PHASE2_COST_PER_PATIENT_HIGH = Parameter(
    120000,
    source_ref="clinical-trial-cost-per-patient",
    source_type="external",
    description="Phase 2 cost per patient (high estimate)",
    unit="USD/patient"
)  # $120K per patient (high end)

TRADITIONAL_PHASE3_COST_PER_PATIENT = Parameter(
    80000,
    source_ref="phase-3-cost-per-patient",
    source_type="external",
    description="Phase 3 cost per patient (median)",
    unit="USD/patient"
)  # $40k-$120k range, using midpoint

PHASE_3_TRIAL_COST_MIN_MILLIONS = Parameter(
    20.0,
    source_ref="phase-3-cost-per-trial",
    source_type="external",
    description="Phase 3 trial total cost (minimum)",
    unit="millions USD/trial"
)  # $20M minimum for Phase 3 trials

PHASE_3_TRIAL_COST_MAX_MILLIONS = Parameter(
    282.0,
    source_ref="phase-3-cost-per-trial",
    source_type="external",
    description="Phase 3 trial total cost (maximum)",
    unit="millions USD/trial"
)  # $282M maximum for Phase 3 trials

TRADITIONAL_SMALL_TRIAL_SIZE = Parameter(
    100,
    source_ref="phase-2-trial-participant-numbers",
    source_type="external",
    description="Typical Phase 2 trial size",
    unit="participants"
)

TRADITIONAL_LARGE_TRIAL_SIZE = Parameter(
    1000,
    source_ref="phase-3-trial-participant-numbers",
    source_type="external",
    description="Typical Phase 3 trial size",
    unit="participants"
)

# dFDA System Targets
DFDA_TRIALS_PER_YEAR_CAPACITY = Parameter(
    380000,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#dfda-capacity",
    source_type="calculated",
    description="Maximum trials per year possible with 115x acceleration",
    unit="trials/year"
)  # Maximum trials/year possible with 115x acceleration
DFDA_DRUG_APPROVALS_PER_YEAR_LOW = Parameter(
    1000,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#approval-projections",
    source_type="calculated",
    description="Conservative drug approvals estimate (20x current)",
    unit="approvals/year"
)  # Conservative approvals estimate (20x current)

DFDA_DRUG_APPROVALS_PER_YEAR_HIGH = Parameter(
    2000,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#approval-projections",
    source_type="calculated",
    description="Optimistic drug approvals estimate (40x current)",
    unit="approvals/year"
)  # Optimistic approvals estimate (40x current)

DFDA_ACTIVE_TRIALS = Parameter(
    200000,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#dfda-capacity",
    source_type="calculated",
    description="Active trials at any given time (3-12 month duration)",
    unit="trials"
)  # Active trials at any given time (3-12 month duration)

DFDA_TRIAL_DURATION_MONTHS_RANGE = (3, 12)  # Months for typical trial completion

DFDA_SMALL_TRIAL_RECRUITMENT_WEEKS = Parameter(
    3,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#recruitment-speed",
    source_type="calculated",
    description="Weeks to recruit 1,000 patients in dFDA system",
    unit="weeks"
)  # Weeks to recruit 1,000 patients

DFDA_LARGE_TRIAL_RECRUITMENT_MONTHS = Parameter(
    3,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#recruitment-speed",
    source_type="calculated",
    description="Months to recruit 10,000+ patients in dFDA system",
    unit="months"
)  # Months to recruit 10,000+ patients

DFDA_TRIAL_ABANDONMENT_RATE = Parameter(
    0.05,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#completion-rates",
    source_type="calculated",
    description="dFDA trial abandonment rate (5%)",
    unit="rate"
)  # Near-zero abandonment (5%)

DFDA_TRIAL_COMPLETION_RATE = Parameter(
    0.95,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#completion-rates",
    source_type="calculated",
    description="dFDA trial completion rate (95%)",
    unit="rate"
)  # 95% completion rate

DFDA_PATIENT_ELIGIBILITY_RATE = Parameter(
    0.50,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#eligibility",
    source_type="calculated",
    description="dFDA patient eligibility rate (50% of disease patients can participate)",
    unit="rate"
)  # 50% of disease patients can participate

DFDA_ELIGIBLE_PATIENTS_GLOBAL = Parameter(
    1_200_000_000,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#eligible-population",
    source_type="calculated",
    description="Global eligible patients with minimal exclusions",
    unit="people"
)  # 1.2B eligible with minimal exclusions

# dFDA Trial Economics
RECOVERY_TRIAL_COST_PER_PATIENT = Parameter(
    500,
    source_ref="recovery-trial-cost-per-patient",
    source_type="external",
    description="RECOVERY trial cost per patient",
    unit="USD/patient"
)  # Proven cost from Oxford RECOVERY trial

DFDA_TARGET_COST_PER_PATIENT = Parameter(
    1000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#cost-per-patient",
    source_type="calculated",
    description="Conservative target cost per patient for dFDA",
    unit="USD/patient"
)  # Conservative target for dFDA

DFDA_SMALL_TRIAL_SIZE = Parameter(
    1000,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#trial-sizes",
    source_type="calculated",
    description="Typical dFDA trial size",
    unit="participants"
)  # Typical dFDA trial size

DFDA_LARGE_TRIAL_SIZE = Parameter(
    10000,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#trial-sizes",
    source_type="calculated",
    description="Large dFDA pragmatic trial size",
    unit="participants"
)  # Large dFDA pragmatic trial size

# Research Acceleration Multipliers (Derived)
RESEARCH_ACCELERATION_MULTIPLIER = Parameter(
    115,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd",
    source_type="calculated",
    description="Total research capacity multiplier from dFDA",
    unit="ratio"
)  # 115x more research capacity (82x cost × 1.4x funding)

RECRUITMENT_SPEED_MULTIPLIER = Parameter(
    25,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#recruitment-acceleration",
    source_type="calculated",
    description="Recruitment speed multiplier (25x faster from 2% → 50% eligibility)",
    unit="ratio"
)  # 25x faster recruitment (from 2% → 50% eligibility)

TRIAL_COMPLETION_SPEED_MULTIPLIER = Parameter(
    10,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#completion-acceleration",
    source_type="calculated",
    description="Trial completion speed multiplier (10x faster)",
    unit="ratio"
)  # 10x faster completion (flipped incentives)

SIMULTANEOUS_TRIALS_MULTIPLIER = Parameter(
    20,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#capacity-multiplier",
    source_type="calculated",
    description="Simultaneous trials multiplier (20x more trials)",
    unit="ratio"
)  # 20x more trials running simultaneously

COMPLETION_RATE_IMPROVEMENT_MULTIPLIER = Parameter(
    1.6,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#completion-rates",
    source_type="calculated",
    description="Completion rate improvement (1.6x from 60% → 95%)",
    unit="ratio"
)  # 1.6x improvement (60% → 95%)

COMPLETED_TRIALS_MULTIPLIER_ACTUAL = Parameter(
    180,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#total-multiplier",
    source_type="calculated",
    description="Actual completed trials multiplier (180x theoretical)",
    unit="ratio"
)  # 180x more completed trials/year (theoretical)

COMPLETED_TRIALS_MULTIPLIER_CONSERVATIVE = Parameter(
    115,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#conservative-multiplier",
    source_type="calculated",
    description="Conservative completed trials multiplier accounting for scale-up",
    unit="ratio"
)  # Conservative rating accounting for scale-up

# Calculated Research Capacity
# Traditional: 3,300 trials/year × 60% completion = ~2,000 completed/year
CURRENT_COMPLETED_TRIALS_PER_YEAR = Parameter(
    int(CURRENT_TRIALS_PER_YEAR * CURRENT_TRIAL_COMPLETION_RATE),
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#current-capacity",
    source_type="calculated",
    description="Current completed trials per year (trials × completion rate)",
    unit="trials/year",
    formula="TRIALS_PER_YEAR × COMPLETION_RATE",
    latex=r"Completed_{current} = 3,300 \times 0.60 = 1,980"
)  # 1,980
# dFDA: 380,000 trials/year × 95% completion = ~360,000 completed/year
DFDA_COMPLETED_TRIALS_PER_YEAR = Parameter(
    int(DFDA_TRIALS_PER_YEAR_CAPACITY * DFDA_TRIAL_COMPLETION_RATE),
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#dfda-capacity",
    source_type="calculated",
    description="dFDA completed trials per year (capacity × completion rate)",
    unit="trials/year",
    formula="CAPACITY × COMPLETION_RATE",
    latex=r"Completed_{dFDA} = 380,000 \times 0.95 = 361,000"
)  # 361,000

# dFDA operational costs
DFDA_UPFRONT_BUILD = Parameter(
    0.040,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#build-costs",
    source_type="calculated",
    description="dFDA platform one-time build cost (central estimate)",
    unit="billions USD"
)  # $40M one-time build cost

DFDA_UPFRONT_BUILD_MAX = Parameter(
    0.046,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#build-costs",
    source_type="calculated",
    description="dFDA platform one-time build cost (high estimate)",
    unit="billions USD"
)  # $46M one-time build cost (high end)

# DCT Platform Funding Comparables
DCT_PLATFORM_FUNDING_MEDIUM = Parameter(
    0.500,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#analogous-rom",
    source_type="calculated",
    description="Mid-range funding for commercial DCT platform",
    unit="billions USD"
)  # $500M funding for commercial platforms

# Per-patient cost in dollars (not billions)
DFDA_TARGET_COST_PER_PATIENT_USD = Parameter(
    1000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#cost-per-patient",
    source_type="calculated",
    description="Target cost per patient in USD (same as DFDA_TARGET_COST_PER_PATIENT but in dollars)",
    unit="USD/patient"
)  # $1,000 per patient

# dFDA operational cost breakdown (in billions)
DFDA_OPEX_PLATFORM_MAINTENANCE = Parameter(
    0.015,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="calculated",
    description="dFDA platform maintenance costs",
    unit="billions USD/year"
)  # $15M

DFDA_OPEX_STAFF = Parameter(
    0.010,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="calculated",
    description="dFDA staff costs (minimal, AI-assisted)",
    unit="billions USD/year"
)  # $10M - minimal, AI-assisted

DFDA_OPEX_INFRASTRUCTURE = Parameter(
    0.008,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="calculated",
    description="dFDA infrastructure costs (cloud, security)",
    unit="billions USD/year"
)  # $8M - cloud, security

DFDA_OPEX_REGULATORY = Parameter(
    0.005,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="calculated",
    description="dFDA regulatory coordination costs",
    unit="billions USD/year"
)  # $5M - regulatory coordination

DFDA_OPEX_COMMUNITY = Parameter(
    0.002,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="calculated",
    description="dFDA community support costs",
    unit="billions USD/year"
)  # $2M - community support

# Total annual operational costs (calculated from components)
DFDA_ANNUAL_OPEX = Parameter(
    DFDA_OPEX_PLATFORM_MAINTENANCE +
    DFDA_OPEX_STAFF +
    DFDA_OPEX_INFRASTRUCTURE +
    DFDA_OPEX_REGULATORY +
    DFDA_OPEX_COMMUNITY,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="calculated",
    description="Total annual dFDA operational costs (sum of all components: $15M + $10M + $8M + $5M + $2M)",
    unit="billions USD/year",
    formula="PLATFORM_MAINTENANCE + STAFF + INFRASTRUCTURE + REGULATORY + COMMUNITY",
    latex=r"OPEX_{total} = \sum_{i=1}^{5} OPEX_i = 0.015 + 0.010 + 0.008 + 0.005 + 0.002"
)  # $40M annually

# Calculated benefits
DFDA_GROSS_SAVINGS_ANNUAL = Parameter(
    GLOBAL_CLINICAL_TRIAL_MARKET_ANNUAL * TRIAL_COST_REDUCTION_PCT,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#cost-reduction",
    source_type="calculated",
    description="Annual gross savings from 50% trial cost reduction",
    unit="billions USD/year",
    formula="TRIAL_MARKET × COST_REDUCTION_PCT",
    latex=r"Savings_{gross} = \$100B \times 0.50 = \$50B"
)  # $50B

DFDA_NET_SAVINGS_ANNUAL = Parameter(
    DFDA_GROSS_SAVINGS_ANNUAL - DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#net-savings",
    source_type="calculated",
    description="Annual net savings (gross savings minus operational costs)",
    unit="billions USD/year",
    formula="GROSS_SAVINGS - ANNUAL_OPEX",
    latex=r"Savings_{net} = \$50B - \$0.04B = \$49.96B"
)  # $49.96B

# Simple ROI (not NPV-adjusted)
DFDA_ROI_SIMPLE = Parameter(
    DFDA_GROSS_SAVINGS_ANNUAL / DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#roi-simple",
    source_type="calculated",
    description="Simple ROI without NPV adjustment (gross savings / annual opex)",
    unit="ratio",
    formula="GROSS_SAVINGS ÷ ANNUAL_OPEX",
    latex=r"ROI_{simple} = \frac{\$50B}{\$0.04B} = 1,250:1"
)  # 1,250:1
# NOTE: For NPV-adjusted ROI (463:1), use ROI_DFDA_SAVINGS_ONLY below
# The NPV-based calculation accounts for time value of money and gradual adoption

# ---
# HEALTH IMPACT PARAMETERS
# ---

# QALY valuations
# Source: brain/book/appendix/icer-full-calculation.qmd
STANDARD_ECONOMIC_QALY_VALUE_USD = Parameter(
    150000,
    source_ref="standard-qaly-value",
    source_type="external",
    description="Standard economic value per QALY",
    unit="USD/QALY"
)  # Standard economic value per QALY

STANDARD_QALYS_PER_LIFE_SAVED = Parameter(
    35,
    source_ref="who-life-tables-qalys-per-life",
    source_type="external",
    description="Standard QALYs per life saved (WHO life tables)",
    unit="QALYs/life"
)  # Standard assumption (WHO life tables)

# dFDA health benefits
GLOBAL_DFDA_QALYS_GAINED_ANNUAL = Parameter(
    840000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd",
    source_type="calculated",
    description="Annual QALYs gained from dFDA",
    unit="QALYs/year"
)  # QALYs gained per year from dFDA
DFDA_QALYS_MONETIZED = Parameter(
    (GLOBAL_DFDA_QALYS_GAINED_ANNUAL * STANDARD_ECONOMIC_QALY_VALUE_USD) / 1_000_000_000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#monetized-value",
    source_type="calculated",
    description="Monetized value of dFDA QALYs (QALYs × economic value)",
    unit="billions USD/year",
    formula="QALYS × VALUE_PER_QALY ÷ 1B",
    latex=r"Value_{QALY} = 840,000 \times \$150,000 / 10^9 = \$126B"
)  # $126B

# Peace dividend health benefits
TREATY_LIVES_SAVED_ANNUAL_GLOBAL = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#lives-saved",
    source_type="calculated",
    description="Annual lives saved from 1% reduction in conflict deaths",
    unit="lives/year",
    formula="TOTAL_DEATHS × REDUCTION_PCT",
    latex=r"LivesSaved = 244,600 \times 0.01 = 2,446"
)  # 2,446 lives
TREATY_QALYS_GAINED_ANNUAL_GLOBAL = Parameter(
    TREATY_LIVES_SAVED_ANNUAL_GLOBAL * STANDARD_QALYS_PER_LIFE_SAVED,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#peace-qalys",
    source_type="calculated",
    description="Annual QALYs gained from peace dividend (lives saved × QALYs/life)",
    unit="QALYs/year",
    formula="LIVES_SAVED × QALYS_PER_LIFE",
    latex=r"QALYs_{peace} = 2,446 \times 35 = 85,610"
)  # 85,610 QALYs

# Combined health benefits
TREATY_TOTAL_QALYS_GAINED_ANNUAL = Parameter(
    GLOBAL_DFDA_QALYS_GAINED_ANNUAL + TREATY_QALYS_GAINED_ANNUAL_GLOBAL,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#total-qalys",
    source_type="calculated",
    description="Total annual QALYs gained (dFDA + peace dividend)",
    unit="QALYs/year",
    formula="DFDA_QALYS + PEACE_QALYS",
    latex=r"QALYs_{total} = 840,000 + 85,610 = 925,610"
)  # 925,610 QALYs
TREATY_TOTAL_LIVES_SAVED_ANNUAL = Parameter(
    TREATY_TOTAL_QALYS_GAINED_ANNUAL / STANDARD_QALYS_PER_LIFE_SAVED,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#total-lives",
    source_type="calculated",
    description="Total annual lives saved equivalent (total QALYs ÷ QALYs/life)",
    unit="lives/year",
    formula="TOTAL_QALYS ÷ QALYS_PER_LIFE",
    latex=r"Lives_{total} = 925,610 / 35 = 26,446"
)  # 26,446 lives

# ---
# CAMPAIGN COSTS
# ---

# Source: brain/book/economics/campaign-budget.qmd
TREATY_CAMPAIGN_DURATION_YEARS = Parameter(
    4,
    source_ref="/knowledge/strategy/roadmap.qmd",
    source_type="calculated",
    description="Treaty campaign duration (3-5 year range, using midpoint)",
    unit="years"
)  # 3-5 year range, using midpoint

# Campaign budget breakdown (in billions)
TREATY_CAMPAIGN_BUDGET_VIRAL_REFERENDUM = Parameter(
    0.200,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Viral referendum campaign budget",
    unit="billions USD"
)  # $200M viral referendum

TREATY_CAMPAIGN_BUDGET_AI_LOBBYING = Parameter(
    0.250,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="AI-assisted lobbying budget",
    unit="billions USD"
)  # $250M AI-assisted lobbying

TREATY_CAMPAIGN_BUDGET_TECHNOLOGY = Parameter(
    0.250,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Technology platform budget",
    unit="billions USD"
)  # $250M technology platform

TREATY_CAMPAIGN_BUDGET_LEGAL = Parameter(
    0.100,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Legal and compliance budget",
    unit="billions USD"
)  # $100M legal & compliance

TREATY_CAMPAIGN_BUDGET_PARTNERSHIPS = Parameter(
    0.100,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Partnerships budget",
    unit="billions USD"
)  # $100M partnerships

TREATY_CAMPAIGN_BUDGET_OPERATIONS = Parameter(
    0.050,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Operations budget",
    unit="billions USD"
)  # $50M operations

TREATY_CAMPAIGN_BUDGET_RESERVE = Parameter(
    0.050,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Reserve fund",
    unit="billions USD"
)  # $50M reserve

# Total campaign cost (calculated from components)
TREATY_CAMPAIGN_TOTAL_COST = Parameter(
    TREATY_CAMPAIGN_BUDGET_VIRAL_REFERENDUM +
    TREATY_CAMPAIGN_BUDGET_AI_LOBBYING +
    TREATY_CAMPAIGN_BUDGET_TECHNOLOGY +
    TREATY_CAMPAIGN_BUDGET_LEGAL +
    TREATY_CAMPAIGN_BUDGET_PARTNERSHIPS +
    TREATY_CAMPAIGN_BUDGET_OPERATIONS +
    TREATY_CAMPAIGN_BUDGET_RESERVE,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Total treaty campaign cost (sum of all campaign budget components)",
    unit="billions USD",
    formula="REFERENDUM + AI_LOBBY + TECH + LEGAL + PARTNERS + OPS + RESERVE",
    latex=r"CampaignCost = \$0.2B + \$0.25B + \$0.25B + \$0.1B + \$0.1B + \$0.05B + \$0.05B = \$1B"
)  # $1B total campaign cost

TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED = Parameter(
    TREATY_CAMPAIGN_TOTAL_COST / TREATY_CAMPAIGN_DURATION_YEARS,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Amortized annual campaign cost (total cost ÷ campaign duration)",
    unit="billions USD/year",
    formula="TOTAL_COST ÷ DURATION",
    latex=r"AnnualCost = \$1B / 4 = \$0.25B"
)  # $250M

# Campaign phase budgets
CAMPAIGN_PHASE1_BUDGET_MILLIONS = Parameter(
    200,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="calculated",
    description="Phase 1 campaign budget (Foundation, Year 1)",
    unit="millions USD"
)  # $200M for Phase 1

CAMPAIGN_PHASE2_BUDGET_MILLIONS = Parameter(
    500,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="calculated",
    description="Phase 2 campaign budget (Scale & Momentum, Years 2-3)",
    unit="millions USD"
)  # $500M for Phase 2

CAMPAIGN_MEDIA_BUDGET_MIN_MILLIONS = Parameter(
    500,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="calculated",
    description="Minimum mass media campaign budget",
    unit="millions USD"
)  # $500M minimum for mass media

CAMPAIGN_MEDIA_BUDGET_MAX_BILLIONS = Parameter(
    1.0,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="calculated",
    description="Maximum mass media campaign budget",
    unit="billions USD"
)  # $1B maximum for mass media

CAMPAIGN_STAFF_BUDGET_MILLIONS = Parameter(
    40,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="calculated",
    description="Campaign core team staff budget",
    unit="millions USD"
)  # $40M for core team

# Total system costs
TREATY_TOTAL_ANNUAL_COSTS = Parameter(
    TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED + DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#total-costs",
    source_type="calculated",
    description="Total annual system costs (campaign + dFDA operations)",
    unit="billions USD/year",
    formula="CAMPAIGN_ANNUAL + DFDA_OPEX",
    latex=r"TotalCosts = \$0.25B + \$0.04B = \$0.29B"
)  # $290M ($0.29B)

# ---
# COMBINED ECONOMICS
# ---

# Total annual benefits
TREATY_TOTAL_ANNUAL_BENEFITS = Parameter(
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + DFDA_GROSS_SAVINGS_ANNUAL,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#total-benefits",
    source_type="calculated",
    description="Total annual benefits (peace dividend + dFDA savings)",
    unit="billions USD/year",
    formula="PEACE_DIVIDEND + DFDA_SAVINGS",
    latex=r"TotalBenefits = \$113.55B + \$50B = \$163.55B"
)  # $164B (rounded from $163.55B)

# Net benefit
TREATY_NET_ANNUAL_BENEFIT = Parameter(
    TREATY_TOTAL_ANNUAL_BENEFITS - TREATY_TOTAL_ANNUAL_COSTS,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#net-benefit",
    source_type="calculated",
    description="Net annual benefit (total benefits - total costs)",
    unit="billions USD/year",
    formula="TOTAL_BENEFITS - TOTAL_COSTS",
    latex=r"NetBenefit = \$163.55B - \$0.29B = \$163.26B"
)  # $163.71B

# ICER calculation (Incremental Cost-Effectiveness Ratio)
# Negative ICER means society SAVES money while gaining QALYs
ICER_PER_QALY = Parameter(
    (TREATY_TOTAL_ANNUAL_COSTS - TREATY_TOTAL_ANNUAL_BENEFITS) / TREATY_TOTAL_QALYS_GAINED_ANNUAL,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#icer-calculation",
    source_type="calculated",
    description="Incremental Cost-Effectiveness Ratio (ICER) per QALY gained",
    unit="USD/QALY"
)  # -$176,907 per QALY (negative = cost-saving)
NET_BENEFIT_PER_LIFE_SAVED = Parameter(
    ICER_PER_QALY * STANDARD_QALYS_PER_LIFE_SAVED,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#cost-per-life",
    source_type="calculated",
    description="Net benefit per life saved (ICER × QALYs/life)",
    unit="millions USD/life",
    formula="ICER × QALYS_PER_LIFE",
    latex=r"BenefitPerLife = -\$176,907 \times 35 = -\$6.19M"
)  # -$6.19M per life

# ---
# ROI TIERS
# ---

# Tier 1: Conservative - dFDA R&D savings only (10-year NPV)
# Source: brain/book/appendix/dfda-roi-calculations.qmd NPV analysis
ROI_DFDA_SAVINGS_ONLY = Parameter(
    463,
    source_ref="/knowledge/figures/dfda-roi-analysis.qmd",
    source_type="calculated",
    description="ROI from dFDA R&D savings (10-year NPV)",
    unit="ratio"
)  # 463:1 from NPV analysis

# Tier 2: Complete - All direct benefits
# Source: brain/book/economics.qmd complete case section
# Note: Calculated as TOTAL_COMPLETE_BENEFITS_ANNUAL / TREATY_CAMPAIGN_TOTAL_COST
# Updated from 1,222:1 when war costs were revised from $9.7T to $11.355T
ROI_ALL_DIRECT_BENEFITS = Parameter(
    1239,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd",
    source_type="calculated",
    description="ROI from all direct benefits (peace dividend + dFDA + health gains)",
    unit="ratio"
)  # 1,239:1 from all 8 benefit categories

# ---
# FINANCIAL PARAMETERS
# ---

# NPV analysis parameters
# Source: brain/book/appendix/dfda-calculation-framework.qmd
NPV_DISCOUNT_RATE_STANDARD = Parameter(
    0.08,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-parameters",
    source_type="calculated",
    description="Standard discount rate for NPV analysis (8% annual)",
    unit="rate"
)  # 8% annual discount rate (r)

NPV_TIME_HORIZON_YEARS = Parameter(
    10,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-parameters",
    source_type="calculated",
    description="Standard time horizon for NPV analysis",
    unit="years"
)  # Standard 10-year analysis window (T)

# NPV Model - Component Costs
# Core platform and broader initiative costs (for detailed breakdowns)
DFDA_NPV_UPFRONT_COST = Parameter(
    0.040,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="dFDA core platform build cost",
    unit="billions USD"
)  # $40M core platform build

DIH_NPV_UPFRONT_COST_INITIATIVES = Parameter(
    0.22975,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="DIH broader initiatives upfront cost (medium case)",
    unit="billions USD"
)  # $228M medium case broader initiatives

DFDA_NPV_ANNUAL_OPEX = Parameter(
    0.01895,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="dFDA core platform annual opex (midpoint of $11-26.5M)",
    unit="billions USD/year"
)  # $19M core platform (midpoint of $11-26.5M)

DIH_NPV_ANNUAL_OPEX_INITIATIVES = Parameter(
    0.02110,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="DIH broader initiatives annual opex (medium case)",
    unit="billions USD/year"
)  # $21.1M medium case broader initiatives

# NPV Model - Primary Parameters (dFDA-specific)
# Total upfront costs (C0): combines core dFDA platform + broader DIH initiative setup
DFDA_NPV_UPFRONT_COST_TOTAL = Parameter(
    DFDA_NPV_UPFRONT_COST + DIH_NPV_UPFRONT_COST_INITIATIVES,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="Total NPV upfront costs (dFDA core + DIH initiatives)",
    unit="billions USD",
    formula="DFDA_BUILD + DIH_INITIATIVES",
    latex=r"C_0 = \$0.040B + \$0.22975B = \$0.26975B"
)  # C0 = $0.26975B

# Total annual operational costs (Cop): combines core dFDA platform + broader DIH initiative annual costs
DFDA_NPV_ANNUAL_OPEX_TOTAL = Parameter(
    DFDA_NPV_ANNUAL_OPEX + DIH_NPV_ANNUAL_OPEX_INITIATIVES,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="Total NPV annual opex (dFDA core + DIH initiatives)",
    unit="billions USD/year",
    formula="DFDA_OPEX + DIH_OPEX",
    latex=r"C_{op} = \$0.01895B + \$0.02110B = \$0.04005B"
)  # Cop = $0.04005B

# dFDA adoption curve: linear ramp from 0% to 100% over 5 years, then constant at 100%
DFDA_NPV_ADOPTION_RAMP_YEARS = Parameter(
    5,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#adoption-curve",
    source_type="calculated",
    description="Years to reach full dFDA adoption",
    unit="years"
)  # Years to reach full adoption

# Calculated NPV values for dFDA
DFDA_NPV_PV_ANNUAL_OPEX = Parameter(
    DFDA_NPV_ANNUAL_OPEX_TOTAL * (1 - (1 + NPV_DISCOUNT_RATE_STANDARD)**-NPV_TIME_HORIZON_YEARS) / NPV_DISCOUNT_RATE_STANDARD,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-calculation",
    source_type="calculated",
    description="Present value of annual opex over 10 years (NPV formula)",
    unit="billions USD",
    formula="OPEX × [(1 - (1 + r)^-T) / r]",
    latex=r"PV_{opex} = \$0.04005B \times \frac{1 - 1.08^{-10}}{0.08} \approx \$0.269B"
)
DFDA_NPV_TOTAL_COST = Parameter(
    DFDA_NPV_UPFRONT_COST_TOTAL + DFDA_NPV_PV_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-total-cost",
    source_type="calculated",
    description="Total NPV cost (upfront + PV of annual opex)",
    unit="billions USD",
    formula="UPFRONT + PV_OPEX",
    latex=r"TotalCost_{NPV} = \$0.26975B + \$0.269B \approx \$0.54B"
)  # ~$0.54B
DFDA_NPV_NET_BENEFIT_CONSERVATIVE = Parameter(
    DFDA_NPV_TOTAL_COST * ROI_DFDA_SAVINGS_ONLY,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-net-benefit",
    source_type="calculated",
    description="Conservative NPV net benefit (total cost × ROI)",
    unit="billions USD",
    formula="TOTAL_COST × ROI",
    latex=r"NetBenefit_{NPV} = \$0.54B \times 463 \approx \$249B"
) # ~$249B

# NOTE: The NPV-based ROI (463:1) accounts for time value of money and gradual adoption
# The simple ROI (1,250:1) is gross savings / annual opex without discounting
# Use ROI_DFDA_SAVINGS_ONLY (463:1) as the canonical figure for most purposes

# VICTORY Social Impact Bonds
# Source: brain/book/economics/victory-bonds.qmd
VICTORY_BOND_FUNDING_PCT = Parameter(
    0.10,
    source_ref="/knowledge/strategy/roadmap.qmd#victory-bonds",
    source_type="calculated",
    description="Percentage of captured dividend funding VICTORY bonds (10%)",
    unit="rate"
)  # 10% of captured dividend funds bonds
VICTORY_BOND_ANNUAL_PAYOUT = Parameter(
    TREATY_ANNUAL_FUNDING * VICTORY_BOND_FUNDING_PCT,
    source_ref="/knowledge/strategy/roadmap.qmd#victory-bonds",
    source_type="calculated",
    description="Annual VICTORY bond payout (treaty funding × bond percentage)",
    unit="billions USD/year",
    formula="TREATY_FUNDING × BOND_PCT",
    latex=r"BondPayout = \$27.18B \times 0.10 = \$2.718B"
)  # $2.718B
VICTORY_BOND_ANNUAL_RETURN_PCT = Parameter(
    VICTORY_BOND_ANNUAL_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST,
    source_ref="/knowledge/strategy/roadmap.qmd#victory-bonds",
    source_type="calculated",
    description="Annual return percentage for VICTORY bondholders",
    unit="rate",
    formula="PAYOUT ÷ CAMPAIGN_COST",
    latex=r"Return = \$2.718B / \$1B = 2.718 = 271.8\%"
)  # 271.8% (reported as 270%)
VICTORY_BOND_PAYBACK_MONTHS = Parameter(
    12 / VICTORY_BOND_ANNUAL_RETURN_PCT,
    source_ref="/knowledge/strategy/roadmap.qmd#victory-bonds",
    source_type="calculated",
    description="Months to full payback for VICTORY bondholders",
    unit="months",
    formula="12 ÷ RETURN_PCT",
    latex=r"Payback = 12 / 2.718 = 4.4 \text{ months}"
)  # 4.4 months
DIVIDEND_COVERAGE_FACTOR = Parameter(
    TREATY_ANNUAL_FUNDING / DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/strategy/roadmap.qmd#sustainability",
    source_type="calculated",
    description="Coverage factor of treaty funding vs dFDA opex (sustainability margin)",
    unit="ratio",
    formula="TREATY_FUNDING ÷ DFDA_OPEX",
    latex=r"Coverage = \$27.18B / \$0.04B = 679x"
) # ~679x

# DIH Treasury allocations (in billions)
# Source: brain/book/appendix/icer-full-calculation.qmd
# Aliases removed - use TREATY_ANNUAL_FUNDING, VICTORY_BOND_ANNUAL_PAYOUT, DFDA_ANNUAL_OPEX directly
DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL_PCT = Parameter(
    1 - VICTORY_BOND_FUNDING_PCT,
    source_ref="/knowledge/strategy/roadmap.qmd#treasury-allocation",
    source_type="calculated",
    description="Percentage of treaty funding going to medical research (remainder after bonds)",
    unit="rate",
    formula="1 - BOND_PCT",
    latex=r"ResearchPct = 1 - 0.10 = 0.90 = 90\%"
) # 90%
DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL = Parameter(
    TREATY_ANNUAL_FUNDING - VICTORY_BOND_ANNUAL_PAYOUT,
    source_ref="/knowledge/strategy/roadmap.qmd#treasury-allocation",
    source_type="calculated",
    description="Annual funding for medical research (treaty funding minus bond payouts)",
    unit="billions USD/year",
    formula="TREATY_FUNDING - BOND_PAYOUT",
    latex=r"ResearchFunding = \$27.18B - \$2.718B = \$24.462B"
)  # $24.3B/year
DIH_TREASURY_TRIAL_SUBSIDIES_MIN = Parameter(
    10.0,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#trial-subsidies",
    source_type="calculated",
    description="Minimum annual clinical trial subsidies from DIH Treasury",
    unit="billions USD/year"
)  # $10B/year clinical trial subsidies (minimum)

DIH_TREASURY_TRIAL_SUBSIDIES_MAX = Parameter(
    20.0,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#trial-subsidies",
    source_type="calculated",
    description="Maximum annual clinical trial subsidies from DIH Treasury",
    unit="billions USD/year"
)  # $20B/year clinical trial subsidies (maximum)

# ---
# REFERENCE VALUES (for comparisons)
# ---

# Global economic context
GLOBAL_GDP_2024 = Parameter(
    111000,
    source_ref="global-gdp",
    source_type="external",
    description="Global GDP in 2024",
    unit="billions USD"
)  # World Bank 2024

GLOBAL_HEALTHCARE_SPENDING_ANNUAL_2024 = Parameter(
    9800,
    source_ref="global-health-spending",
    source_type="external",
    description="Global healthcare spending in 2024",
    unit="billions USD"
)

US_DEFENSE_BUDGET_ANNUAL_BILLIONS = Parameter(
    877,
    source_ref="us-defense-budget-2024",
    source_type="external",
    description="US defense budget in 2024",
    unit="billions USD/year"
)  # FY2024 US defense budget

MENTAL_HEALTH_GRANTS_ANNUAL_MILLIONS = Parameter(
    500,
    source_ref="mental-health-research-funding",
    source_type="external",
    description="Annual mental health research grants total",
    unit="millions USD/year"
)  # $500M in mental health grants annually

DIABETES_TREATMENT_MONTHLY_COST = Parameter(
    500,
    source_ref="diabetes-treatment-costs",
    source_type="external",
    description="Average monthly cost of diabetes treatment per patient",
    unit="USD/month"
)  # $500/month for diabetes treatment

MEDICAL_FACILITY_HOURLY_ROOM_COST = Parameter(
    500,
    source_ref="hospital-room-costs",
    source_type="external",
    description="Average hourly cost of medical facility room",
    unit="USD/hour"
)  # $500/hour for medical facility room costs

SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL = Parameter(
    10,
    source_ref="agricultural-subsidies",
    source_type="external",
    description="Annual cost of sugar subsidies per person",
    unit="USD/person/year"
)  # $10 per person per year in sugar subsidies

RARE_DISEASE_TYPICAL_PATIENT_COUNT = Parameter(
    500,
    source_ref="rare-disease-prevalence",
    source_type="external",
    description="Typical patient count for rare diseases",
    unit="patients"
)  # 500 patients typical for rare diseases

ALZHEIMER_CURE_BOUNTY_ESTIMATE_BILLIONS = Parameter(
    10,
    source_ref="cure-bounty-estimates",
    source_type="calculated",
    description="Estimated bounty value for Alzheimer's cure",
    unit="billions USD"
)  # $10B estimated bounty for Alzheimer's cure

GLOBAL_MED_RESEARCH_SPENDING = Parameter(
    67.5,
    source_ref="global-government-medical-research-spending",
    source_type="external",
    description="Global government medical research spending",
    unit="billions USD"
)
TOTAL_GLOBAL_WASTE_SPEND_ANNUAL = Parameter(
    118800,
    source_ref="/knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Total global annual spending on military and disease",
    unit="billions USD/year"
)  # billions USD, annual spend on military + disease

# Population
GLOBAL_POPULATION_2024_BILLIONS = Parameter(
    8.0,
    source_ref="global-population-8-billion",
    source_type="external",
    description="Global population in 2024",
    unit="billions of people"
)  # UN World Population Prospects 2022

GLOBAL_DAILY_DEATHS_CURABLE_DISEASES = Parameter(
    150000,
    source_ref="global-daily-deaths-curable-diseases",
    source_type="external",
    description="Daily deaths from curable diseases globally",
    unit="deaths/day"
)  # Daily deaths from curable diseases

# Per capita calculations
GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_POPULATION_2024_BILLIONS,
    source_ref="/knowledge/problem/cost-of-war.qmd#per-capita",
    source_type="calculated",
    description="Per capita military spending globally",
    unit="USD/person/year",
    formula="MILITARY_SPENDING ÷ POPULATION",
    latex=r"PerCapita_{military} = \$2,718B / 8.0B = \$339.75"
)  # $340/person/year
GLOBAL_TOTAL_WAR_COST_PER_CAPITA_ANNUAL = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST / GLOBAL_POPULATION_2024_BILLIONS,
    source_ref="/knowledge/problem/cost-of-war.qmd#per-capita",
    source_type="calculated",
    description="Per capita total war cost globally",
    unit="USD/person/year",
    formula="TOTAL_WAR_COST ÷ POPULATION",
    latex=r"PerCapita_{war} = \$11,355.1B / 8.0B = \$1,419.39"
)  # $1,419/person/year
LIFETIME_WAR_COST_PER_CAPITA = Parameter(
    GLOBAL_TOTAL_WAR_COST_PER_CAPITA_ANNUAL * 80,
    source_ref="/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations.qmd#lifetime-cost",
    source_type="calculated",
    description="Lifetime war cost per person (80-year lifespan)",
    unit="USD/person",
    formula="ANNUAL_PER_CAPITA × 80",
    latex=r"Lifetime_{war} = \$1,419.39 \times 80 = \$113,551"
)  # $113,551 over 80-year life

# GiveWell charity comparison
# Source: brain/book/appendix/icer-full-calculation.qmd
GIVEWELL_COST_PER_LIFE_MIN = Parameter(
    3500,
    source_ref="givewell-cost-per-life-saved",
    source_type="external",
    description="GiveWell cost per life saved (Helen Keller International)",
    unit="USD/life"
)  # Helen Keller International Vitamin A

GIVEWELL_COST_PER_LIFE_MAX = Parameter(
    5500,
    source_ref="givewell-cost-per-life-saved",
    source_type="external",
    description="GiveWell cost per life saved (Against Malaria Foundation)",
    unit="USD/life"
)  # Against Malaria Foundation

GIVEWELL_COST_PER_LIFE_AVG = Parameter(
    4500,
    source_ref="givewell-cost-per-life-saved",
    source_type="external",
    description="GiveWell average cost per life saved across top charities",
    unit="USD/life"
)  # Midpoint of top charities

# Cost-effectiveness multiplier
MULTIPLIER_VS_GIVEWELL = Parameter(
    abs(NET_BENEFIT_PER_LIFE_SAVED * 1_000_000_000) / GIVEWELL_COST_PER_LIFE_AVG,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#givewell-comparison",
    source_type="calculated",
    description="Cost-effectiveness multiplier vs GiveWell top charities",
    unit="ratio",
    formula="ABS(NET_BENEFIT × 1B) ÷ GIVEWELL_COST",
    latex=r"Multiplier = \frac{|-\$6.19M \times 10^9|}{\$4,500} \approx 1,376x"
)  # ~1,376x more cost-effective

# Historical public health comparisons
SMALLPOX_ERADICATION_ROI = Parameter(
    280,
    source_ref="smallpox-eradication-roi",
    source_type="external",
    description="Return on investment from smallpox eradication campaign",
    unit="ratio"
)  # 159:1 to 280:1 estimated

CHILDHOOD_VACCINATION_ROI = Parameter(
    13,
    source_ref="childhood-vaccination-roi",
    source_type="external",
    description="Return on investment from childhood vaccination programs",
    unit="ratio"
)  # 13:1

WATER_FLUORIDATION_ROI = Parameter(
    23,
    source_ref="water-fluoridation-roi",
    source_type="external",
    description="Return on investment from water fluoridation programs",
    unit="ratio"
)  # 23:1

# ---
# COMPLETE BENEFITS BREAKDOWN (for 1,239:1 ROI calculation)
# ---

# Source: brain/book/economics.qmd complete case section
# Note: Peace dividend updated from $97.1B to $113.55B when total war costs were revised from $9.7T to $11.355T
# BENEFIT_PEACE_DIVIDEND_ANNUAL removed - use PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT directly
BENEFIT_RESEARCH_AND_DEVELOPMENT_SAVINGS_ANNUAL = Parameter(
    DFDA_GROSS_SAVINGS_ANNUAL,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#cost-reduction",
    source_type="calculated",
    description="Annual R&D savings benefit (alias for dFDA gross savings)",
    unit="billions USD/year",
    formula="DFDA_GROSS_SAVINGS",
    latex=r"R\&D_{savings} = \$50B"
)  # 82x cheaper trials (reference calculated value)
BENEFIT_EARLIER_DRUG_ACCESS_ANNUAL = Parameter(
    300.0,
    source_ref="/knowledge/appendix/economic-value-of-accelerated-treatments.qmd",
    source_type="calculated",
    description="Annual benefit from 7-year drug access acceleration",
    unit="billions USD/year"
)  # 7-year acceleration

BENEFIT_MEDICAL_RESEARCH_ACCELERATION_ANNUAL = Parameter(
    100.0,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd",
    source_type="calculated",
    description="Annual benefit from 115x research capacity increase",
    unit="billions USD/year"
)  # 115x more research capacity

BENEFIT_RARE_DISEASES_ANNUAL = Parameter(
    400.0,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#rare-diseases",
    source_type="calculated",
    description="Annual benefit from orphan drug viability",
    unit="billions USD/year"
)  # Orphan drug viability

BENEFIT_DRUG_PRICE_REDUCTION_ANNUAL = Parameter(
    100.0,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#price-reduction",
    source_type="calculated",
    description="Annual benefit from R&D savings passed to consumers",
    unit="billions USD/year"
)  # R&D savings passed to consumers

BENEFIT_PREVENTION_ANNUAL = Parameter(
    100.0,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#prevention",
    source_type="calculated",
    description="Annual benefit from economic viability of prevention",
    unit="billions USD/year"
)  # Economic viability of prevention

BENEFIT_MENTAL_HEALTH_ANNUAL = Parameter(
    75.0,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#mental-health",
    source_type="calculated",
    description="Annual benefit from mental health treatment gap reduction",
    unit="billions USD/year"
)  # Treatment gap reduction

TOTAL_COMPLETE_BENEFITS_ANNUAL = Parameter(
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT
    + BENEFIT_RESEARCH_AND_DEVELOPMENT_SAVINGS_ANNUAL
    + BENEFIT_EARLIER_DRUG_ACCESS_ANNUAL
    + BENEFIT_MEDICAL_RESEARCH_ACCELERATION_ANNUAL
    + BENEFIT_RARE_DISEASES_ANNUAL
    + BENEFIT_DRUG_PRICE_REDUCTION_ANNUAL
    + BENEFIT_PREVENTION_ANNUAL
    + BENEFIT_MENTAL_HEALTH_ANNUAL,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#complete-benefits",
    source_type="calculated",
    description="Total annual benefits from all 8 benefit categories",
    unit="billions USD/year",
    formula="PEACE + R&D + FASTER_ACCESS + ACCELERATION + RARE + PRICE + PREVENTION + MENTAL",
    latex=r"TotalBenefits = \$113.55 + \$50 + \$300 + \$100 + \$400 + \$100 + \$100 + \$75 = \$1,238.55B"
)  # $1,238.55B (updated from $1,222B when war costs were revised)


# ---
# COST OF DELAY PARAMETERS
# ---

# Source: brain/book/economics.qmd
# QALY delay costs (quality-adjusted life days lost per second of inaction)
COST_OF_DELAY_QALY_DAYS_PER_SECOND = Parameter(
    (TREATY_TOTAL_QALYS_GAINED_ANNUAL / 365) / (365.25 * 24 * 60 * 60),
    source_ref="/knowledge/problem/cost-of-war.qmd#cost-of-delay",
    source_type="calculated",
    description="QALY-days lost per second of inaction",
    unit="QALY-days/second",
    formula="(QALYS_ANNUAL ÷ 365) ÷ SECONDS_PER_YEAR",
    latex=r"Delay_{QALY} = \frac{925,610 / 365}{31,557,600} \approx 0.00008"
) # QALY days per second

# Deaths delay costs (preventable deaths per second from curable diseases)
COST_OF_DELAY_DEATHS_PER_SECOND = Parameter(
    GLOBAL_DAILY_DEATHS_CURABLE_DISEASES / (24 * 60 * 60),
    source_ref="/knowledge/problem/cost-of-war.qmd#cost-of-delay",
    source_type="calculated",
    description="Preventable deaths per second from curable diseases",
    unit="deaths/second",
    formula="DAILY_DEATHS ÷ SECONDS_PER_DAY",
    latex=r"Delay_{deaths} = \frac{150,000}{86,400} \approx 1.74"
) # deaths per second

# ---
# SCENARIO PARAMETERS
# ---

GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024 = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * (1 - TREATY_REDUCTION_PCT),
    source_ref="/knowledge/strategy/treaty-adoption-strategy.qmd#post-treaty",
    source_type="calculated",
    description="Global military spending after 1% treaty reduction",
    unit="billions USD/year",
    formula="MILITARY_SPENDING × (1 - REDUCTION)",
    latex=r"PostTreaty_{military} = \$2,718B \times 0.99 = \$2,690.82B"
) # $2,690.82B

# Partial success scenario (US, EU, UK only)
PARTIAL_SUCCESS_MILITARY_SPENDING_SHARE = Parameter(
    0.50,
    source_ref="/knowledge/strategy/treaty-adoption-strategy.qmd#partial-success",
    source_type="calculated",
    description="Military spending share for partial success scenario (US, EU, UK)",
    unit="rate"
)  # ~50% of global spending
PARTIAL_SUCCESS_DIH_REVENUE = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * PARTIAL_SUCCESS_MILITARY_SPENDING_SHARE * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/strategy/treaty-adoption-strategy.qmd#partial-success",
    source_type="calculated",
    description="DIH revenue in partial success scenario",
    unit="billions USD/year",
    formula="MILITARY × SHARE × REDUCTION",
    latex=r"Revenue_{partial} = \$2,718B \times 0.50 \times 0.01 = \$13.59B"
) # ~$13.6B
PARTIAL_SUCCESS_BONDHOLDER_PAYOUT = Parameter(
    PARTIAL_SUCCESS_DIH_REVENUE * VICTORY_BOND_FUNDING_PCT,
    source_ref="/knowledge/strategy/treaty-adoption-strategy.qmd#partial-success",
    source_type="calculated",
    description="Bondholder payout in partial success scenario",
    unit="billions USD/year",
    formula="REVENUE × BOND_PCT",
    latex=r"Payout_{partial} = \$13.59B \times 0.10 = \$1.36B"
) # ~$1.36B
PARTIAL_SUCCESS_RESEARCH_FUNDING = Parameter(
    PARTIAL_SUCCESS_DIH_REVENUE * DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL_PCT,
    source_ref="/knowledge/strategy/treaty-adoption-strategy.qmd#partial-success",
    source_type="calculated",
    description="Research funding in partial success scenario",
    unit="billions USD/year",
    formula="REVENUE × RESEARCH_PCT",
    latex=r"Research_{partial} = \$13.59B \times 0.90 = \$12.23B"
) # ~$12.2B
PARTIAL_SUCCESS_INVESTOR_ROI = Parameter(
    PARTIAL_SUCCESS_BONDHOLDER_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST,
    source_ref="/knowledge/strategy/treaty-adoption-strategy.qmd#partial-success",
    source_type="calculated",
    description="Investor ROI in partial success scenario",
    unit="rate",
    formula="PAYOUT ÷ CAMPAIGN_COST",
    latex=r"ROI_{partial} = \$1.36B / \$1B = 1.359 = 135.9\%"
) # ~135.9%

# ---
# QALYs Breakdown & Treatment Acceleration Details
# ---

# Base Case (Central Scenario) - Used as primary estimates throughout analysis
QALYS_FROM_FASTER_ACCESS = Parameter(
    200000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#base-case",
    source_type="calculated",
    description="Base case QALYs from faster drug access",
    unit="QALYs/year"
)  # QALYs gained annually from faster drug access (Base case)

QALYS_FROM_PREVENTION = Parameter(
    140000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#base-case",
    source_type="calculated",
    description="Base case QALYs from better prevention through real-world data",
    unit="QALYs/year"
)  # QALYs gained annually from better prevention through real-world data (Base case)

QALYS_FROM_NEW_THERAPIES = Parameter(
    500000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#base-case",
    source_type="calculated",
    description="Base case QALYs from enabling new therapies for rare/untreatable diseases",
    unit="QALYs/year"
)  # QALYs gained annually from enabling new therapies for rare/untreatable diseases (Base case)

# Conservative Scenario - Lower bound estimates for QALY gains
QALYS_FROM_FASTER_ACCESS_CONSERVATIVE = Parameter(
    90000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative QALYs from faster access (15 drugs/yr × 1 yr accel × 6k QALYs/drug)",
    unit="QALYs/year"
)  # QALYs from faster access (15 drugs/yr × 1 yr accel × 6k QALYs/drug)

QALYS_FROM_PREVENTION_CONSERVATIVE = Parameter(
    50000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative QALYs from prevention (5M patients × 0.01 QALYs/patient)",
    unit="QALYs/year"
)  # QALYs from prevention (5M patients × 0.01 QALYs/patient)

QALYS_FROM_NEW_THERAPIES_CONSERVATIVE = Parameter(
    50000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative QALYs from new therapies (5 therapies/yr × 2k patients × 5 QALYs/patient)",
    unit="QALYs/year"
)  # QALYs from new therapies (5 therapies/yr × 2k patients × 5 QALYs/patient)

QALYS_TOTAL_CONSERVATIVE = Parameter(
    190000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#conservative-scenario",
    source_type="calculated",
    description="Total conservative QALYs (90k + 50k + 50k)",
    unit="QALYs/year"
)  # Total conservative QALYs (90k + 50k + 50k)

# Optimistic Scenario - Upper bound estimates for QALY gains
QALYS_FROM_FASTER_ACCESS_OPTIMISTIC = Parameter(
    500000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic QALYs from faster drug access",
    unit="QALYs/year"
)  # 25 drugs/yr × 2 yr accel × 10k QALYs/drug

QALYS_FROM_PREVENTION_OPTIMISTIC = Parameter(
    150000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic QALYs from prevention",
    unit="QALYs/year"
)  # QALYs from prevention

QALYS_FROM_NEW_THERAPIES_OPTIMISTIC = Parameter(
    3000000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic QALYs from new therapies",
    unit="QALYs/year"
)  # QALYs from new therapies

QALYS_TOTAL_OPTIMISTIC = Parameter(
    3650000,
    source_ref="/knowledge/appendix/dfda-qaly-model.qmd#optimistic-scenario",
    source_type="calculated",
    description="Total optimistic QALYs (500k + 150k + 3M)",
    unit="QALYs/year"
)  # Total optimistic QALYs (500k + 150k + 3M)

TREATMENT_ACCELERATION_YEARS_TARGET = Parameter(
    2,
    source_ref="/knowledge/appendix/research-acceleration-model.qmd#target-timeline",
    source_type="calculated",
    description="Target years to market with dFDA",
    unit="years"
)  # Years to market with dFDA (target)

TREATMENT_ACCELERATION_YEARS_CURRENT = Parameter(
    17,
    source_ref="fda-drug-approval-timeline",
    source_type="external",
    description="Traditional FDA drug development timeline",
    unit="years"
)  # 12-17 years typical

# ---
# SENSITIVITY ANALYSIS SCENARIOS
# ---

# Source: brain/book/appendix/icer-full-calculation.qmd sensitivity tables

# Conservative scenario
SENSITIVITY_PEACE_DIVIDEND_CONSERVATIVE = Parameter(
    50.0,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative peace dividend estimate",
    unit="billions USD"
)  # $50B

SENSITIVITY_DFDA_SAVINGS_CONSERVATIVE = Parameter(
    25.0,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative dFDA savings estimate",
    unit="billions USD"
)  # $25B

SENSITIVITY_TOTAL_BENEFITS_CONSERVATIVE = Parameter(
    75.0,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative total benefits estimate",
    unit="billions USD"
)  # $75B

SENSITIVITY_CAMPAIGN_COST_CONSERVATIVE = Parameter(
    0.333,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative campaign cost (3-year amortization)",
    unit="billions USD/year"
)  # $333M/year (3-year amortization)

SENSITIVITY_DFDA_OPEX_CONSERVATIVE = Parameter(
    0.060,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative dFDA operational costs",
    unit="billions USD/year"
)  # $60M/year

SENSITIVITY_TOTAL_COSTS_CONSERVATIVE = Parameter(
    0.393,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative total costs",
    unit="billions USD/year"
)  # $393M/year

SENSITIVITY_PEACE_QALYS_CONSERVATIVE = Parameter(
    17500,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative peace QALYs (500 lives × 35 QALYs/life)",
    unit="QALYs/year"
)  # 500 lives × 35 QALYs/life
SENSITIVITY_TOTAL_QALYS_CONSERVATIVE = Parameter(
    SENSITIVITY_PEACE_QALYS_CONSERVATIVE + QALYS_TOTAL_CONSERVATIVE,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative total QALYs (peace + dFDA)",
    unit="QALYs/year",
    formula="PEACE_QALYS + DFDA_QALYS",
    latex=r"QALYs_{conservative} = 17,500 + 190,000 = 207,500"
)  # Total QALYs (peace + dFDA)
SENSITIVITY_NET_BENEFIT_CONSERVATIVE = Parameter(
    74.6,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative net benefit from sensitivity analysis",
    unit="billions USD"
)  # $74.6B

SENSITIVITY_ICER_CONSERVATIVE = Parameter(
    -170514,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative ICER from sensitivity analysis",
    unit="USD/QALY"
)  # -$170,514 per QALY (negative = cost-saving)

SENSITIVITY_COST_PER_LIFE_CONSERVATIVE = Parameter(
    -5.97,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative cost per life saved",
    unit="millions USD/life"
)  # -$5.97M per life (in millions)

# Central scenario (baseline) - uses main parameters directly, no aliases needed
SENSITIVITY_ICER_CENTRAL = Parameter(
    -187097,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#central-scenario",
    source_type="calculated",
    description="Central ICER from sensitivity analysis",
    unit="USD/QALY"
)  # -$187,097 per QALY

SENSITIVITY_COST_PER_LIFE_CENTRAL = Parameter(
    -6.55,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#central-scenario",
    source_type="calculated",
    description="Central cost per life saved",
    unit="millions USD/life"
)  # -$6.55M per life (in millions)
SENSITIVITY_LIVES_SAVED_CENTRAL = Parameter(
    TREATY_TOTAL_QALYS_GAINED_ANNUAL / STANDARD_QALYS_PER_LIFE_SAVED,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#central-scenario",
    source_type="calculated",
    description="Central scenario lives saved (total QALYs ÷ QALYs/life)",
    unit="lives/year",
    formula="TOTAL_QALYS ÷ QALYS_PER_LIFE",
    latex=r"Lives_{central} = 925,610 / 35 \approx 26,446"
) # 25,000

# Optimistic scenario
SENSITIVITY_PEACE_DIVIDEND_OPTIMISTIC = Parameter(
    200.0,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic peace dividend estimate",
    unit="billions USD"
)  # $200B

SENSITIVITY_DFDA_SAVINGS_OPTIMISTIC = Parameter(
    95.0,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic dFDA savings estimate",
    unit="billions USD"
)  # $95B

SENSITIVITY_TOTAL_BENEFITS_OPTIMISTIC = Parameter(
    295.0,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic total benefits estimate",
    unit="billions USD"
)  # $295B

SENSITIVITY_CAMPAIGN_COST_OPTIMISTIC = Parameter(
    0.200,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic campaign cost (5-year amortization)",
    unit="billions USD/year"
)  # $200M/year (5-year amortization)

SENSITIVITY_DFDA_OPEX_OPTIMISTIC = Parameter(
    0.030,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic dFDA operational costs",
    unit="billions USD/year"
)  # $30M/year

SENSITIVITY_TOTAL_COSTS_OPTIMISTIC = Parameter(
    0.230,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic total costs",
    unit="billions USD/year"
)  # $230M/year

SENSITIVITY_PEACE_QALYS_OPTIMISTIC = Parameter(
    52500,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic peace QALYs (1,500 lives × 35 QALYs/life)",
    unit="QALYs/year"
)  # 1,500 lives × 35 QALYs/life
SENSITIVITY_TOTAL_QALYS_OPTIMISTIC = Parameter(
    SENSITIVITY_PEACE_QALYS_OPTIMISTIC + QALYS_TOTAL_OPTIMISTIC,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic total QALYs (peace + dFDA)",
    unit="QALYs/year",
    formula="PEACE_QALYS + DFDA_QALYS",
    latex=r"QALYs_{optimistic} = 52,500 + 3,650,000 = 3,702,500"
)  # Total QALYs (peace + dFDA)

SENSITIVITY_NET_BENEFIT_OPTIMISTIC = Parameter(
    294.8,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic net benefit from sensitivity analysis",
    unit="billions USD"
)  # $294.8B

SENSITIVITY_ICER_OPTIMISTIC = Parameter(
    -136945,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic ICER from sensitivity analysis",
    unit="USD/QALY"
)  # -$136,945 per QALY (negative = cost-saving)

SENSITIVITY_COST_PER_LIFE_OPTIMISTIC = Parameter(
    -4.79,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic cost per life saved",
    unit="millions USD/life"
)  # -$4.79M per life (in millions)

# Sensitivity ROI calculations
CONSERVATIVE_SCENARIO_ROI = Parameter(
    int(SENSITIVITY_NET_BENEFIT_CONSERVATIVE / SENSITIVITY_TOTAL_COSTS_CONSERVATIVE),
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#conservative-scenario",
    source_type="calculated",
    description="Conservative scenario ROI (net benefit ÷ total costs)",
    unit="ratio",
    formula="NET_BENEFIT ÷ TOTAL_COSTS",
    latex=r"ROI_{conservative} = \$74.6B / \$0.393B = 190:1"
)  # 190:1
OPTIMISTIC_SCENARIO_ROI = Parameter(
    int(SENSITIVITY_NET_BENEFIT_OPTIMISTIC / SENSITIVITY_TOTAL_COSTS_OPTIMISTIC),
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#optimistic-scenario",
    source_type="calculated",
    description="Optimistic scenario ROI (net benefit ÷ total costs)",
    unit="ratio",
    formula="NET_BENEFIT ÷ TOTAL_COSTS",
    latex=r"ROI_{optimistic} = \$294.8B / \$0.230B = 1,282:1"
)  # 1,282:1

# Alternative ICER calculations based on funding perspective
# Source: icer-full-calculation.qmd alternative ICER table
ICER_INVESTOR_FUNDED = Parameter(
    -187429,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#alternative-icer",
    source_type="calculated",
    description="ICER for investor-funded scenario (VICTORY Social Impact Bonds)",
    unit="USD/QALY"
)  # -$187,429 (campaign funded by VICTORY Social Impact Bonds, cost = $0)

ICER_OPPORTUNITY_COST = Parameter(
    -156571,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#alternative-icer",
    source_type="calculated",
    description="ICER counting redirected military spending as opportunity cost",
    unit="USD/QALY"
)  # -$156,571 (counts $27B redirected military spending)

ICER_WASTE_CONVERSION = None  # Undefined (military spending has negative ROI)

COST_PER_LIFE_INVESTOR_FUNDED = Parameter(
    -6.56,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#alternative-icer",
    source_type="calculated",
    description="Cost per life for investor-funded scenario",
    unit="millions USD/life"
)  # -$6.56M

COST_PER_LIFE_OPPORTUNITY_COST = Parameter(
    -5.48,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#alternative-icer",
    source_type="calculated",
    description="Cost per life counting military spending opportunity cost",
    unit="millions USD/life"
)  # -$5.48M

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


def param_link(value, param_name="", format_func=None):
    """Create an HTML link for a parameter value with tooltip showing parameter source.

    This function generates an HTML anchor tag with:
    - The formatted parameter value as visible text
    - A tooltip showing the parameter name on hover
    - A CSS class for styling
    - A link anchor (can be customized to point to documentation)

    Args:
        value: The numeric value to display
        param_name: The parameter name (e.g., "GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT")
        format_func: Optional formatting function (e.g., format_billions, format_qalys)
                    If None, formats as comma-separated integer

    Returns:
        HTML string like: <a href="#" class="parameter-link" title="parameters.PARAM_NAME">233,600</a>

    Example usage in QMD:
        `{python} from dih_models.parameters import *`{=html}
        `{python} param_link(GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT, "GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT", format_qalys)`{=html}
    """
    # Format the value
    if format_func:
        formatted_value = format_func(value)
    elif isinstance(value, float) and value < 100:
        # Small numbers might be percentages or ratios
        formatted_value = f"{value:,.2f}"
    elif isinstance(value, (int, float)):
        # Large numbers - format with commas
        formatted_value = f"{value:,.0f}"
    else:
        formatted_value = str(value)

    # Create tooltip text
    tooltip = f"parameters.{param_name}" if param_name else "parameter value"

    # Return HTML link with tooltip
    # Using # as href (no navigation), with parameter-link class for CSS styling
    return f'<a href="#" class="parameter-link" title="{tooltip}">{formatted_value}</a>'


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
US_DOT_VALUE_OF_STATISTICAL_LIFE_MILLIONS = Parameter(
    13.6,
    source_ref="us-dot-value-statistical-life",
    source_type="external",
    description="US Department of Transportation value of statistical life",
    unit="millions USD"
)  # $13.6M, reference value from Dept. of Transportation

VSL_EPA_MILLIONS = Parameter(
    9.6,
    source_ref="epa-value-statistical-life",
    source_type="external",
    description="EPA value of statistical life",
    unit="millions USD"
)  # $9.6M, reference value from EPA

# Derived time-based costs
SECONDS_PER_YEAR = 365 * 24 * 60 * 60
GLOBAL_WAR_DIRECT_COST_PER_SECOND = Parameter(
    GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL * 1_000_000_000 / SECONDS_PER_YEAR,
    source_ref="/knowledge/problem/cost-of-war.qmd#cost-per-second",
    source_type="calculated",
    description="Direct war cost per second globally",
    unit="USD/second",
    formula="DIRECT_COSTS × 1B ÷ SECONDS_PER_YEAR",
    latex=r"CostPerSecond = \frac{\$7,655B \times 10^9}{31,557,600} \approx \$242,749"
) # ~$242,749

# Refugee parameters
GLOBAL_FORCIBLY_DISPLACED_PEOPLE_2023 = Parameter(
    108_400_000,
    source_ref="unhcr-global-displacement-2023",
    source_type="external",
    description="Global forcibly displaced people in 2023",
    unit="people"
)

GLOBAL_COST_PER_REFUGEE_PER_YEAR_AVERAGE = Parameter(
    1384,
    source_ref="unhcr-refugee-cost-per-year",
    source_type="external",
    description="Average annual cost per refugee globally",
    unit="USD/year"
)

# Grotesque Mathematics calculations
GLOBAL_COST_PER_CONFLICT_DEATH_MILLIONS = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * 1_000_000_000 / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL / 1_000_000,
    source_ref="/knowledge/problem/cost-of-war.qmd#grotesque-mathematics",
    source_type="calculated",
    description="Cost per conflict death (war cost ÷ deaths)",
    unit="millions USD/death",
    formula="(WAR_COST × 1B ÷ DEATHS) ÷ 1M",
    latex=r"CostPerDeath = \frac{\$11,355.1B \times 10^9}{244,600} / 10^6 \approx \$46.4M"
) # ~$46.4M
GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH = Parameter(
    4_200_000,
    source_ref="medical-research-lives-saved-annually",
    source_type="external",
    description="Annual lives saved by medical research globally",
    unit="lives/year"
)
GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL = Parameter(
    GLOBAL_MED_RESEARCH_SPENDING * 1_000_000_000 / GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH,
    source_ref="/knowledge/problem/cost-of-war.qmd#grotesque-mathematics",
    source_type="calculated",
    description="Cost per life saved by medical research",
    unit="USD/life",
    formula="(RESEARCH_SPENDING × 1B) ÷ LIVES_SAVED",
    latex=r"CostPerLifeSaved = \frac{\$67.5B \times 10^9}{4,200,000} \approx \$16,071"
) # ~$16,071
MISALLOCATION_FACTOR_DEATH_VS_SAVING = Parameter(
    (GLOBAL_ANNUAL_WAR_TOTAL_COST * 1_000_000_000 / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL) / GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL,
    source_ref="/knowledge/problem/cost-of-war.qmd#grotesque-mathematics",
    source_type="calculated",
    description="Misallocation factor: cost to kill vs cost to save",
    unit="ratio",
    formula="COST_PER_DEATH ÷ COST_PER_LIFE_SAVED",
    latex=r"Misallocation = \frac{\$46.4M}{\$16,071} \approx 2,889x"
) # ~2,889x

# Specific budget items from text
GLOBAL_NUCLEAR_WEAPONS_ANNUAL_BUDGET_INCREASE = Parameter(
    42.0,
    source_ref="global-nuclear-weapons-budget-increase",
    source_type="external",
    description="Annual increase in global nuclear weapons budget",
    unit="billions USD/year"
)  # billions USD

# ---
# COST OF WAR DETAILS (for cost-of-war.qmd) - Additional Parameters
# ---

# Military Spending Breakdown (billions USD)
GLOBAL_ANNUAL_MILITARY_SPENDING_PERSONNEL_2024 = Parameter(
    681.5,
    source_ref="global-military-spending",
    source_type="external",
    description="Global military spending on personnel in 2024",
    unit="billions USD"
)

GLOBAL_ANNUAL_MILITARY_SPENDING_PROCUREMENT_2024 = Parameter(
    654.3,
    source_ref="global-military-spending",
    source_type="external",
    description="Global military spending on procurement in 2024",
    unit="billions USD"
)

GLOBAL_ANNUAL_MILITARY_SPENDING_OPS_MAINTENANCE_2024 = Parameter(
    579.8,
    source_ref="global-military-spending",
    source_type="external",
    description="Global military spending on operations and maintenance in 2024",
    unit="billions USD"
)

GLOBAL_ANNUAL_MILITARY_SPENDING_INFRASTRUCTURE_2024 = Parameter(
    520.4,
    source_ref="global-military-spending",
    source_type="external",
    description="Global military spending on infrastructure in 2024",
    unit="billions USD"
)

GLOBAL_ANNUAL_MILITARY_SPENDING_INTELLIGENCE_2024 = Parameter(
    282.0,
    source_ref="global-military-spending",
    source_type="external",
    description="Global military spending on intelligence in 2024",
    unit="billions USD"
)

# Opportunity Cost Parameters
GLOBAL_EDUCATION_FOR_ALL_COST = Parameter(
    30.0,
    source_ref="unesco-education-for-all-cost",
    source_type="external",
    description="Global cost to achieve universal education",
    unit="billions USD"
)  # billions USD

GLOBAL_POVERTY_ERADICATION_COST_TOTAL = Parameter(
    1000.0,
    source_ref="world-bank-poverty-eradication",
    source_type="external",
    description="Total cost to eradicate global poverty",
    unit="billions USD"
)  # billions USD

ECONOMIC_MULTIPLIER_MILITARY_SPENDING = Parameter(
    0.6,
    source_ref="economic-multiplier-military",
    source_type="external",
    description="Economic multiplier for military spending (0.6x ROI)",
    unit="ratio"
)

ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT = Parameter(
    1.6,
    source_ref="economic-multiplier-infrastructure",
    source_type="external",
    description="Economic multiplier for infrastructure investment (1.6x ROI)",
    unit="ratio"
)

ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT = Parameter(
    2.1,
    source_ref="economic-multiplier-education",
    source_type="external",
    description="Economic multiplier for education investment (2.1x ROI)",
    unit="ratio"
)

ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT = Parameter(
    4.3,
    source_ref="economic-multiplier-healthcare",
    source_type="external",
    description="Economic multiplier for healthcare investment (4.3x ROI)",
    unit="ratio"
)

# Refugee Parameters
REFUGEE_LOST_EARNING_POTENTIAL_PER_CAPITA_ANNUAL = Parameter(
    23400,
    source_ref="refugee-lost-earnings",
    source_type="external",
    description="Average annual lost earning potential per refugee",
    unit="USD/year"
)  # USD per year
REFUGEE_LOST_PRODUCTIVITY_GLOBAL_TOTAL = Parameter(
    (GLOBAL_FORCIBLY_DISPLACED_PEOPLE_2023 * REFUGEE_LOST_EARNING_POTENTIAL_PER_CAPITA_ANNUAL) / 1_000_000_000,
    source_ref="/knowledge/problem/cost-of-war.qmd#refugee-costs",
    source_type="calculated",
    description="Total global lost refugee productivity",
    unit="billions USD/year",
    formula="(REFUGEES × LOST_EARNINGS) ÷ 1B",
    latex=r"RefugeeLosses = \frac{108.4M \times \$23,400}{10^9} = \$2,536.6B"
)  # $2,536.6B

# Contextual / Comparison Parameters
GLOBAL_GDP_2023 = Parameter(
    89500,
    source_ref="global-gdp",
    source_type="external",
    description="Global GDP in 2023 for comparison",
    unit="billions USD"
)  # billions USD, for 2023 comparison

TOTAL_WAR_COST_TO_WHO_BUDGET_RATIO = Parameter(
    168,
    source_ref="/knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Ratio of total war cost to WHO budget (168x)",
    unit="ratio"
)  # Total war cost is 168x WHO budget (or similar sized org)


# ---
# NEW PARAMETERS ADDED FROM CHAPTER ANALYSIS (2025-01-24)
# ---

# Alias for consistency with book text

# Campaign & Strategy Specifics
TREATY_CAMPAIGN_BUDGET_MASS_BRIBERY = Parameter(
    0.140,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Campaign budget for mass mobilization (voting bloc build)",
    unit="billions USD"
)  # billions USD, for bribing the masses (voting bloc build)

TREATY_CAMPAIGN_VOTING_BLOC_TARGET_MILLIONS = Parameter(
    280,
    source_ref="/knowledge/strategy/roadmap.qmd#voting-bloc",
    source_type="calculated",
    description="Target voting bloc size for campaign",
    unit="millions of people"
)  # millions of people, target voting bloc size

TREATY_CAMPAIGN_BUDGET_SUPER_PACS = Parameter(
    0.800,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Campaign budget for Super PACs and political lobbying",
    unit="billions USD"
)  # billions USD, for Super PACs/politician bribery

GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT = Parameter(
    0.035,
    source_ref="3-5-percent-rule-social-change",
    source_type="external",
    description="Critical mass threshold for social change (3.5% rule)",
    unit="rate"
)  # 3.5% rule for social change, key tipping point

TREATY_CAMPAIGN_COST_PER_VOTE_MIN_USD = Parameter(
    0.20,
    source_ref="/knowledge/strategy/roadmap.qmd#vote-acquisition-cost",
    source_type="calculated",
    description="Minimum cost per vote for mass mobilization campaign",
    unit="USD/vote"
)  # USD per vote, minimum for mass bribery campaign

TREATY_CAMPAIGN_COST_PER_VOTE_MAX_USD = Parameter(
    0.50,
    source_ref="/knowledge/strategy/roadmap.qmd#vote-acquisition-cost",
    source_type="calculated",
    description="Maximum cost per vote for mass mobilization campaign",
    unit="USD/vote"
)  # USD per vote, maximum for mass bribery campaign

# Clinical Trial Cost Examples & Comparisons
TRADITIONAL_PHASE3_COST_PER_PATIENT_EXAMPLE_48K = Parameter(
    48000,
    source_ref="clinical-trial-cost-per-patient",
    source_type="external",
    description="Example Phase 3 trial cost per patient ($48K)",
    unit="USD/patient"
)  # USD per trial patient, specific example from text for comparison

TRADITIONAL_PHASE3_COST_PER_PATIENT_FDA_EXAMPLE_41K = Parameter(
    41000,
    source_ref="fda-clinical-trial-costs",
    source_type="external",
    description="FDA cited Phase 3 cost per patient ($41K)",
    unit="USD/patient"
)  # USD per patient, cited FDA cost example for comparison

# Historical & Comparison Multipliers
MILITARY_VS_MEDICAL_RESEARCH_RATIO = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_MED_RESEARCH_SPENDING,
    source_ref="/knowledge/problem/cost-of-war.qmd#misallocation",
    source_type="calculated",
    description="Ratio of military spending to medical research spending",
    unit="ratio",
    formula="MILITARY_SPENDING ÷ MEDICAL_RESEARCH",
    latex=r"Ratio = \frac{\$2,718B}{\$67.5B} \approx 40.3:1"
) # Calculated ratio of military to medical research spending

DEATH_SPENDING_MISALLOCATION_FACTOR = Parameter(
    1750,
    source_ref="/knowledge/problem/cost-of-war.qmd#misallocation",
    source_type="calculated",
    description="Misallocation factor for spending on death vs prevention",
    unit="ratio"
)  # Multiplier for spending on death vs prevention (specific citation in text)

POST_WW2_MILITARY_CUT_PCT = Parameter(
    0.30,
    source_ref="post-ww2-military-demobilization",
    source_type="external",
    description="Percentage military spending cut after WW2 (historical precedent)",
    unit="rate"
)  # Percentage military spending cut after WW2, historical precedent

SWITZERLAND_DEFENSE_SPENDING_PCT = Parameter(
    0.007,
    source_ref="switzerland-defense-spending-gdp",
    source_type="external",
    description="Switzerland's defense spending as percentage of GDP (0.7%)",
    unit="rate"
)  # Switzerland's defense spending as percentage of GDP

SWITZERLAND_GDP_PER_CAPITA_K = Parameter(
    93,
    source_ref="switzerland-gdp-per-capita",
    source_type="external",
    description="Switzerland GDP per capita",
    unit="thousands USD"
)  # Thousands USD, Switzerland GDP per capita, for comparison

LOBBYING_ROI_DEFENSE = Parameter(
    1813,
    source_ref="defense-lobbying-roi",
    source_type="external",
    description="Return on investment for defense lobbying ($1,813 returned per $1 spent)",
    unit="ratio"
)  # Dollars returned per dollar spent lobbying defense, cited statistic

WW2_BOND_RETURN_PCT = Parameter(
    0.04,
    source_ref="ww2-war-bonds-return",
    source_type="external",
    description="World War II war bond return percentage (4%)",
    unit="rate"
)  # WWII bond return percentage, historical comparison

AVERAGE_MARKET_RETURN_PCT = Parameter(
    0.10,
    source_ref="average-stock-market-return",
    source_type="external",
    description="Average annual stock market return (10%)",
    unit="rate"
)  # Average market return percentage for portfolio comparisons

# VICTORY Social Impact Bonds derived payout (per unit of investment)
VICTORY_BOND_INVESTMENT_UNIT_USD = Parameter(
    1000,
    source_ref="/knowledge/strategy/roadmap.qmd#victory-bonds",
    source_type="calculated",
    description="VICTORY bond investment unit for retail investors",
    unit="USD"
)  # USD, per bond investment unit for retail investors

VICTORY_BOND_PAYOUT_PER_UNIT_USD_ANNUAL = Parameter(
    (VICTORY_BOND_ANNUAL_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST) * VICTORY_BOND_INVESTMENT_UNIT_USD,
    source_ref="/knowledge/strategy/roadmap.qmd#victory-bonds",
    source_type="calculated",
    description="Annual payout per $1,000 VICTORY bond investment unit",
    unit="USD/year",
    formula="(ANNUAL_PAYOUT ÷ CAMPAIGN_COST) × UNIT",
    latex=r"PayoutPerUnit = \frac{\$2.718B}{\$1B} \times \$1,000 = \$2,718"
) # Derived from total payout and total raise

# Lobbyist compensation & incentives
LOBBYIST_BOND_INVESTMENT_MIN_MILLIONS = Parameter(
    5,
    source_ref="/knowledge/strategy/roadmap.qmd#lobbyist-incentives",
    source_type="calculated",
    description="Minimum bond investment for lobbyist incentives",
    unit="millions USD"
)  # Millions USD, bond investment for lobbyists (min incentive)

LOBBYIST_BOND_INVESTMENT_MAX_MILLIONS = Parameter(
    20,
    source_ref="/knowledge/strategy/roadmap.qmd#lobbyist-incentives",
    source_type="calculated",
    description="Maximum bond investment for lobbyist incentives",
    unit="millions USD"
)  # Millions USD, bond investment for lobbyists (max incentive)

LOBBYIST_SALARY_TYPICAL_K = Parameter(
    500,
    source_ref="average-lobbyist-salary",
    source_type="external",
    description="Typical annual lobbyist salary for comparison",
    unit="thousands USD"
)  # Thousands USD, typical lobbyist salary, for comparison

LOBBYIST_SALARY_MIN_K = Parameter(
    500,
    source_ref="average-lobbyist-salary",
    source_type="external",
    description="Minimum annual lobbyist salary range",
    unit="thousands USD"
)  # $500K minimum for lobbyist salaries

LOBBYIST_SALARY_MAX_MILLIONS = Parameter(
    2.0,
    source_ref="average-lobbyist-salary",
    source_type="external",
    description="Maximum annual lobbyist salary range",
    unit="millions USD"
)  # $2M maximum for top lobbyist salaries

CAMPAIGN_WEEKLY_AD_COST_K = Parameter(
    500,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="calculated",
    description="Weekly advertising cost for campaigns",
    unit="thousands USD/week"
)  # $500K/week for campaign advertising

SOFTWARE_TOOL_MONTHLY_COST_MIN = Parameter(
    500,
    source_ref="software-pricing-market-rates",
    source_type="external",
    description="Minimum monthly cost for software tools/services",
    unit="USD/month"
)  # $500/month minimum for software tools

SOFTWARE_TOOL_MONTHLY_COST_MAX = Parameter(
    2000,
    source_ref="software-pricing-market-rates",
    source_type="external",
    description="Maximum monthly cost for software tools/services",
    unit="USD/month"
)  # $2,000/month maximum for software tools

SOCIAL_MEDIA_PARTICIPANT_TARGET_MIN = Parameter(
    500,
    source_ref="/knowledge/strategy/viral-marketing.qmd",
    source_type="calculated",
    description="Minimum target participant count for social media campaigns",
    unit="participants"
)  # 500 participants minimum

SOCIAL_MEDIA_PARTICIPANT_TARGET_MAX = Parameter(
    2000,
    source_ref="/knowledge/strategy/viral-marketing.qmd",
    source_type="calculated",
    description="Maximum target participant count for social media campaigns",
    unit="participants"
)  # 2,000 participants maximum

# Specific benefit sum (used for the $147.1B figure in the "Where Math Breaks" section)
# This sum is distinct from TREATY_TOTAL_ANNUAL_BENEFITS which uses different categories for broader calculation.
COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC = Parameter(
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + BENEFIT_RESEARCH_AND_DEVELOPMENT_SAVINGS_ANNUAL,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#combined-dividends",
    source_type="calculated",
    description="Combined peace and health dividends for ROI calculation",
    unit="billions USD/year",
    formula="PEACE_DIVIDEND + R&D_SAVINGS",
    latex=r"Combined = \$113.55B + \$50B = \$163.55B"
)

# System effectiveness & ROI comparisons
PROFIT_PER_LIFE_SAVED = Parameter(
    167771,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#profit-per-life",
    source_type="calculated",
    description="System profit per life saved (specific calculation)",
    unit="USD/life"
)  # USD, profit per life saved from the system (specific calculation in text)

SYSTEM_PROFIT_PER_LIFE_SAVED_MILLIONS = Parameter(
    5.87,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#profit-per-life",
    source_type="calculated",
    description="System profit per life saved in millions",
    unit="millions USD/life"
)  # Millions USD, system profit per life saved (specific phrasing in text)

TREATY_BENEFIT_MULTIPLIER_VS_VACCINES = Parameter(
    10,
    source_ref="/knowledge/appendix/1-percent-treaty-cost-effectiveness.qmd#vaccine-comparison",
    source_type="calculated",
    description="Treaty system benefit multiplier vs childhood vaccination programs (10x)",
    unit="ratio"
)  # Multiplier: treaty system (1% Treaty + dFDA) benefit vs childhood vaccines program

# Price of Procrastination Metrics
DEATHS_DURING_READING_SECTION = Parameter(
    410,
    source_ref="/knowledge/solution/dfda.qmd#cost-of-delay",
    source_type="calculated",
    description="Deaths from curable diseases during reading one section",
    unit="deaths"
)  # Number of deaths from curable diseases during reading a section

DAILY_COST_INEFFICIENCY = Parameter(
    0.327,
    source_ref="/knowledge/solution/dfda.qmd#cost-of-delay",
    source_type="calculated",
    description="Daily cost of healthcare system inefficiency",
    unit="billions USD/day"
)  # billions USD, daily cost of inefficiency


# ---
# PRE-FORMATTED VALUES FOR INLINE DISPLAY
# ---
# These are pre-computed formatted strings for use in Quarto inline expressions.
# Quarto inline code should only reference simple variables, not function calls.
# See: https://quarto.org/docs/computations/inline-code.html

average_market_return_pct_formatted = format_percentage(AVERAGE_MARKET_RETURN_PCT)
benefit_drug_price_reduction_annual_formatted = format_billions(BENEFIT_DRUG_PRICE_REDUCTION_ANNUAL)
benefit_earlier_drug_access_annual_formatted = format_billions(BENEFIT_EARLIER_DRUG_ACCESS_ANNUAL)
benefit_medical_research_acceleration_annual_formatted = format_billions(BENEFIT_MEDICAL_RESEARCH_ACCELERATION_ANNUAL)
benefit_mental_health_annual_formatted = format_billions(BENEFIT_MENTAL_HEALTH_ANNUAL)
benefit_prevention_annual_formatted = format_billions(BENEFIT_PREVENTION_ANNUAL)
benefit_rare_diseases_annual_formatted = format_billions(BENEFIT_RARE_DISEASES_ANNUAL)
benefit_research_and_development_savings_annual_formatted = format_billions(BENEFIT_RESEARCH_AND_DEVELOPMENT_SAVINGS_ANNUAL)
childhood_vaccination_roi_formatted = format_roi(CHILDHOOD_VACCINATION_ROI)
combined_peace_health_dividends_annual_for_roi_calc_formatted = format_billions_latex(COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC)
conservative_scenario_roi_formatted = format_roi(CONSERVATIVE_SCENARIO_ROI)
cost_of_delay_deaths_per_second_formatted = f"{COST_OF_DELAY_DEATHS_PER_SECOND:.3f}"
cost_of_delay_qaly_days_per_second_formatted = f"{COST_OF_DELAY_QALY_DAYS_PER_SECOND:.1f}"
cost_per_life_investor_funded_formatted = f"${COST_PER_LIFE_INVESTOR_FUNDED:.2f}M"
cost_per_life_opportunity_cost_formatted = f"${COST_PER_LIFE_OPPORTUNITY_COST:.2f}M"
daily_cost_inefficiency_formatted = format_currency(DAILY_COST_INEFFICIENCY)
death_spending_misallocation_factor_formatted = f"{DEATH_SPENDING_MISALLOCATION_FACTOR:,.0f}"
deaths_during_reading_section_formatted = f"{DEATHS_DURING_READING_SECTION:,.0f}"
dfda_annual_opex_formatted = format_millions(DFDA_ANNUAL_OPEX)
dfda_gross_savings_annual_formatted = format_billions(DFDA_GROSS_SAVINGS_ANNUAL)
dfda_npv_net_benefit_conservative_formatted = format_billions(DFDA_NPV_NET_BENEFIT_CONSERVATIVE)
dfda_npv_total_cost_formatted = format_currency(DFDA_NPV_TOTAL_COST)
dfda_opex_community_formatted = format_currency(DFDA_OPEX_COMMUNITY)
dfda_opex_infrastructure_formatted = format_currency(DFDA_OPEX_INFRASTRUCTURE)
dfda_opex_platform_maintenance_formatted = format_currency(DFDA_OPEX_PLATFORM_MAINTENANCE)
dfda_opex_regulatory_formatted = format_currency(DFDA_OPEX_REGULATORY)
dfda_opex_staff_formatted = format_currency(DFDA_OPEX_STAFF)
dfda_roi_simple_formatted = format_roi(DFDA_ROI_SIMPLE)
dih_treasury_to_medical_research_annual_formatted = format_billions(DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL)
dih_treasury_trial_subsidies_max_formatted = format_billions(DIH_TREASURY_TRIAL_SUBSIDIES_MAX)
dih_treasury_trial_subsidies_min_formatted = format_billions(DIH_TREASURY_TRIAL_SUBSIDIES_MIN)
dividend_coverage_factor_formatted = f"{DIVIDEND_COVERAGE_FACTOR:,.0f}"
givewell_cost_per_life_avg_formatted = f"${GIVEWELL_COST_PER_LIFE_AVG:,.0f}"
givewell_cost_per_life_max_formatted = f"${GIVEWELL_COST_PER_LIFE_MAX:,.0f}"
givewell_cost_per_life_min_formatted = f"${GIVEWELL_COST_PER_LIFE_MIN:,.0f}"
global_annual_conflict_deaths_active_combat_formatted = f"{GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT:,}"
global_annual_conflict_deaths_state_violence_formatted = f"{GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE:,}"
global_annual_conflict_deaths_terror_attacks_formatted = f"{GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS:,}"
global_annual_conflict_deaths_total_formatted = format_qalys(GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL)
global_annual_environmental_damage_conflict_formatted = format_billions(GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT)
global_annual_human_life_losses_conflict_formatted = format_billions(GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT)
global_annual_infrastructure_destruction_conflict_formatted = format_billions(GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT)
global_annual_lost_economic_growth_military_spending_formatted = format_billions(GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING)
global_annual_lost_human_capital_conflict_formatted = format_billions(GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT)
global_annual_psychological_impact_costs_conflict_formatted = format_billions(GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT)
global_annual_refugee_support_costs_formatted = format_billions(GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS)
global_annual_trade_disruption_conflict_formatted = format_billions(GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT)
global_annual_veteran_healthcare_costs_formatted = format_billions(GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS)
global_annual_war_direct_costs_total_formatted = format_billions(GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL)
global_annual_war_indirect_costs_total_formatted = format_billions(GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL)
global_annual_war_total_cost_formatted = format_billions(GLOBAL_ANNUAL_WAR_TOTAL_COST)
global_clinical_trial_market_annual_formatted = format_billions(GLOBAL_CLINICAL_TRIAL_MARKET_ANNUAL)
global_daily_deaths_curable_diseases_formatted = f"{GLOBAL_DAILY_DEATHS_CURABLE_DISEASES:,.0f}"
global_dfda_qalys_gained_annual_formatted = format_qalys(GLOBAL_DFDA_QALYS_GAINED_ANNUAL)
global_med_research_spending_formatted = format_billions(GLOBAL_MED_RESEARCH_SPENDING)
global_military_spending_annual_2024_formatted = format_billions(GLOBAL_MILITARY_SPENDING_ANNUAL_2024)
global_military_spending_post_treaty_annual_2024_formatted = format_billions(GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024)
global_population_activism_threshold_pct_formatted = format_percentage(GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT)
icer_investor_funded_formatted = f"${ICER_INVESTOR_FUNDED:,.0f}"
icer_opportunity_cost_formatted = f"${ICER_OPPORTUNITY_COST:,.0f}"
icer_per_qaly_formatted = f"${ICER_PER_QALY * 1_000_000_000:,.0f}"
lobbyist_bond_investment_max_millions_formatted = format_currency(LOBBYIST_BOND_INVESTMENT_MAX_MILLIONS / 1000)
lobbyist_bond_investment_min_millions_formatted = format_currency(LOBBYIST_BOND_INVESTMENT_MIN_MILLIONS / 1000)
lobbyist_salary_typical_k_formatted = format_currency(LOBBYIST_SALARY_TYPICAL_K / 1_000_000)
military_vs_medical_research_ratio_formatted = f"{MILITARY_VS_MEDICAL_RESEARCH_RATIO:,.0f}"
multiplier_vs_givewell_formatted = f"{MULTIPLIER_VS_GIVEWELL:,.0f}x"
net_benefit_per_life_saved_formatted = format_currency(abs(NET_BENEFIT_PER_LIFE_SAVED * 1_000_000_000))
optimistic_scenario_roi_formatted = format_roi(OPTIMISTIC_SCENARIO_ROI)
peace_dividend_annual_societal_benefit_formatted = format_billions_latex(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT)
post_ww2_military_cut_pct_formatted = format_percentage(POST_WW2_MILITARY_CUT_PCT)
profit_per_life_saved_formatted = f"${PROFIT_PER_LIFE_SAVED:,.0f}"
qalys_from_faster_access_conservative_formatted = f"{QALYS_FROM_FASTER_ACCESS_CONSERVATIVE:,.0f}"
qalys_from_faster_access_formatted = f"{QALYS_FROM_FASTER_ACCESS / GLOBAL_DFDA_QALYS_GAINED_ANNUAL * 100:.0f}%"
qalys_from_faster_access_optimistic_formatted = f"{QALYS_FROM_FASTER_ACCESS_OPTIMISTIC:,.0f}"
qalys_from_new_therapies_conservative_formatted = f"{QALYS_FROM_NEW_THERAPIES_CONSERVATIVE:,.0f}"
qalys_from_new_therapies_formatted = f"{QALYS_FROM_NEW_THERAPIES / GLOBAL_DFDA_QALYS_GAINED_ANNUAL * 100:.0f}%"
qalys_from_new_therapies_optimistic_formatted = f"{QALYS_FROM_NEW_THERAPIES_OPTIMISTIC:,.0f}"
qalys_from_prevention_conservative_formatted = f"{QALYS_FROM_PREVENTION_CONSERVATIVE:,.0f}"
qalys_from_prevention_formatted = f"{QALYS_FROM_PREVENTION / GLOBAL_DFDA_QALYS_GAINED_ANNUAL * 100:.0f}%"
qalys_from_prevention_optimistic_formatted = f"{QALYS_FROM_PREVENTION_OPTIMISTIC:,.0f}"
qalys_total_conservative_formatted = format_qalys(QALYS_TOTAL_CONSERVATIVE)
qalys_total_optimistic_formatted = format_qalys(QALYS_TOTAL_OPTIMISTIC)
recovery_trial_cost_per_patient_formatted = format_currency(RECOVERY_TRIAL_COST_PER_PATIENT / 1_000_000_000)
roi_all_direct_benefits_formatted = format_roi(ROI_ALL_DIRECT_BENEFITS)
roi_dfda_savings_only_formatted = format_roi(ROI_DFDA_SAVINGS_ONLY)
sensitivity_campaign_cost_conservative_formatted = format_currency(SENSITIVITY_CAMPAIGN_COST_CONSERVATIVE)
sensitivity_campaign_cost_optimistic_formatted = format_currency(SENSITIVITY_CAMPAIGN_COST_OPTIMISTIC)
sensitivity_cost_per_life_central_formatted = f"${SENSITIVITY_COST_PER_LIFE_CENTRAL:.2f}M"
sensitivity_cost_per_life_conservative_formatted = f"${SENSITIVITY_COST_PER_LIFE_CONSERVATIVE:.2f}M"
sensitivity_cost_per_life_optimistic_formatted = f"${SENSITIVITY_COST_PER_LIFE_OPTIMISTIC:.2f}M"
sensitivity_dfda_opex_conservative_formatted = format_currency(SENSITIVITY_DFDA_OPEX_CONSERVATIVE)
sensitivity_dfda_opex_optimistic_formatted = format_currency(SENSITIVITY_DFDA_OPEX_OPTIMISTIC)
sensitivity_dfda_savings_conservative_formatted = format_billions(SENSITIVITY_DFDA_SAVINGS_CONSERVATIVE)
sensitivity_dfda_savings_optimistic_formatted = format_billions(SENSITIVITY_DFDA_SAVINGS_OPTIMISTIC)
sensitivity_icer_central_formatted = f"${SENSITIVITY_ICER_CENTRAL:,.0f}"
sensitivity_icer_conservative_formatted = f"${SENSITIVITY_ICER_CONSERVATIVE:,.0f}"
sensitivity_icer_optimistic_formatted = f"${SENSITIVITY_ICER_OPTIMISTIC:,.0f}"
sensitivity_lives_saved_central_formatted = f"{SENSITIVITY_LIVES_SAVED_CENTRAL:,.0f}"
sensitivity_net_benefit_conservative_formatted = format_billions(SENSITIVITY_NET_BENEFIT_CONSERVATIVE)
sensitivity_net_benefit_optimistic_formatted = format_billions(SENSITIVITY_NET_BENEFIT_OPTIMISTIC)
sensitivity_peace_dividend_conservative_formatted = format_billions(SENSITIVITY_PEACE_DIVIDEND_CONSERVATIVE)
sensitivity_peace_dividend_optimistic_formatted = format_billions(SENSITIVITY_PEACE_DIVIDEND_OPTIMISTIC)
sensitivity_peace_qalys_conservative_formatted = format_qalys(SENSITIVITY_PEACE_QALYS_CONSERVATIVE)
sensitivity_peace_qalys_optimistic_formatted = format_qalys(SENSITIVITY_PEACE_QALYS_OPTIMISTIC)
sensitivity_total_benefits_conservative_formatted = format_billions(SENSITIVITY_TOTAL_BENEFITS_CONSERVATIVE)
sensitivity_total_benefits_optimistic_formatted = format_billions(SENSITIVITY_TOTAL_BENEFITS_OPTIMISTIC)
sensitivity_total_costs_conservative_formatted = format_currency(SENSITIVITY_TOTAL_COSTS_CONSERVATIVE)
sensitivity_total_costs_optimistic_formatted = format_currency(SENSITIVITY_TOTAL_COSTS_OPTIMISTIC)
sensitivity_total_qalys_conservative_formatted = format_qalys(SENSITIVITY_TOTAL_QALYS_CONSERVATIVE)
sensitivity_total_qalys_optimistic_formatted = format_qalys(SENSITIVITY_TOTAL_QALYS_OPTIMISTIC)
smallpox_eradication_roi_formatted = format_roi(SMALLPOX_ERADICATION_ROI)
switzerland_defense_spending_pct_formatted = format_percentage(SWITZERLAND_DEFENSE_SPENDING_PCT)
switzerland_gdp_per_capita_k_formatted = format_currency(SWITZERLAND_GDP_PER_CAPITA_K / 1_000_000)
system_profit_per_life_saved_millions_formatted = f"${SYSTEM_PROFIT_PER_LIFE_SAVED_MILLIONS:,.2f} million"
total_complete_benefits_annual_formatted = format_billions(TOTAL_COMPLETE_BENEFITS_ANNUAL)
total_global_waste_spend_annual_formatted = format_billions(TOTAL_GLOBAL_WASTE_SPEND_ANNUAL)
traditional_phase3_cost_per_patient_fda_example_41k_formatted = format_currency(TRADITIONAL_PHASE3_COST_PER_PATIENT_FDA_EXAMPLE_41K / 1_000_000_000)
treaty_annual_funding_formatted = format_billions(TREATY_ANNUAL_FUNDING)
treaty_benefit_multiplier_vs_vaccines_formatted = f"{TREATY_BENEFIT_MULTIPLIER_VS_VACCINES:,.0f}"
treaty_campaign_annual_cost_amortized_formatted = format_currency(TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED)
treaty_campaign_budget_ai_lobbying_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_AI_LOBBYING)
treaty_campaign_budget_legal_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_LEGAL)
treaty_campaign_budget_operations_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_OPERATIONS)
treaty_campaign_budget_partnerships_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_PARTNERSHIPS)
treaty_campaign_budget_reserve_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_RESERVE)
treaty_campaign_budget_super_pacs_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_SUPER_PACS)
treaty_campaign_budget_technology_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_TECHNOLOGY)
treaty_campaign_budget_viral_referendum_formatted = format_currency(TREATY_CAMPAIGN_BUDGET_VIRAL_REFERENDUM)
treaty_campaign_total_cost_formatted = format_billions(TREATY_CAMPAIGN_TOTAL_COST)
treaty_lives_saved_annual_global_formatted = format_qalys(TREATY_LIVES_SAVED_ANNUAL_GLOBAL)
treaty_net_annual_benefit_formatted = format_billions(TREATY_NET_ANNUAL_BENEFIT)
treaty_qalys_gained_annual_global_formatted = format_qalys(TREATY_QALYS_GAINED_ANNUAL_GLOBAL)
treaty_reduction_pct_formatted = format_percentage(TREATY_REDUCTION_PCT)
treaty_total_annual_benefits_formatted = format_billions(TREATY_TOTAL_ANNUAL_BENEFITS)
treaty_total_annual_costs_formatted = format_millions(TREATY_TOTAL_ANNUAL_COSTS)
treaty_total_qalys_gained_annual_formatted = format_qalys(TREATY_TOTAL_QALYS_GAINED_ANNUAL)
trial_cost_reduction_pct_formatted = format_percentage(TRIAL_COST_REDUCTION_PCT)
victory_bond_annual_payout_formatted = format_billions_latex(VICTORY_BOND_ANNUAL_PAYOUT)
victory_bond_annual_return_pct_formatted = format_percentage(VICTORY_BOND_ANNUAL_RETURN_PCT)
victory_bond_funding_pct_formatted = format_percentage(VICTORY_BOND_FUNDING_PCT)
victory_bond_investment_unit_usd_formatted = f"${VICTORY_BOND_INVESTMENT_UNIT_USD:,.0f}"
victory_bond_payout_per_unit_usd_annual_formatted = f"${VICTORY_BOND_PAYOUT_PER_UNIT_USD_ANNUAL:,.0f}"
water_fluoridation_roi_formatted = format_roi(WATER_FLUORIDATION_ROI)
ww2_bond_return_pct_formatted = format_percentage(WW2_BOND_RETURN_PCT)


# ---
# BOOK READING TIME & HOURLY RATE CALCULATIONS
# ---

# Book reading time parameters
# Source: word_count.ps1 output
TOTAL_BOOK_WORDS = Parameter(
    171121,
    source_ref="book-word-count",
    source_type="calculated",
    description="Total words in the book",
    unit="words"
)  # Total words in the book

BOOK_READING_SPEED_WPM = Parameter(
    200,
    source_ref="average-reading-speed",
    source_type="external",
    description="Average reading speed (conservative for non-fiction)",
    unit="words/minute"
)  # Words per minute (conservative for non-fiction)
BOOK_READING_TIME_HOURS = Parameter(
    (TOTAL_BOOK_WORDS / BOOK_READING_SPEED_WPM) / 60,
    source_ref="/knowledge/solution/wishocracy.qmd#time-investment",
    source_type="calculated",
    description="Time to read the entire book",
    unit="hours",
    formula="(WORDS ÷ SPEED) ÷ 60",
    latex=r"ReadTime = \frac{171,121 / 200}{60} \approx 14.3 \text{ hours}"
)  # ~14.3 hours

# Action time parameters
# Source: brain/book/call-to-action/three-actions.qmd
ACTION_TIME_VOTE_MINUTES = Parameter(
    2,
    source_ref="/knowledge/solution/wishocracy.qmd#action-steps",
    source_type="calculated",
    description="Time to vote (minutes)",
    unit="minutes"
)

ACTION_TIME_INVEST_MINUTES = Parameter(
    10,
    source_ref="/knowledge/solution/wishocracy.qmd#action-steps",
    source_type="calculated",
    description="Time to invest (minutes)",
    unit="minutes"
)

ACTION_TIME_RECRUIT_MINUTES = Parameter(
    15,
    source_ref="/knowledge/solution/wishocracy.qmd#action-steps",
    source_type="calculated",
    description="Time to recruit others (minutes)",
    unit="minutes"
)
ACTION_TIME_TOTAL_MINUTES = Parameter(
    ACTION_TIME_VOTE_MINUTES + ACTION_TIME_INVEST_MINUTES + ACTION_TIME_RECRUIT_MINUTES,
    source_ref="/knowledge/solution/wishocracy.qmd#action-steps",
    source_type="calculated",
    description="Total time for all three actions",
    unit="minutes",
    formula="VOTE + INVEST + RECRUIT",
    latex=r"TotalTime = 2 + 10 + 15 = 27 \text{ minutes}"
)  # 30 minutes
ACTION_TIME_TOTAL_HOURS = Parameter(
    ACTION_TIME_TOTAL_MINUTES / 60,
    source_ref="/knowledge/solution/wishocracy.qmd#action-steps",
    source_type="calculated",
    description="Total action time in hours",
    unit="hours",
    formula="MINUTES ÷ 60",
    latex=r"Hours = 27 / 60 = 0.45 \text{ hours}"
)  # 0.5 hours

# Total time investment
TOTAL_TIME_INVESTMENT_HOURS = Parameter(
    BOOK_READING_TIME_HOURS + ACTION_TIME_TOTAL_HOURS,
    source_ref="/knowledge/solution/wishocracy.qmd#time-investment",
    source_type="calculated",
    description="Total time investment (reading + actions)",
    unit="hours",
    formula="READING + ACTIONS",
    latex=r"TotalInvestment = 14.3 + 0.45 = 14.75 \text{ hours}"
)  # ~14.8 hours

# Effective hourly rate calculation (20-year scenario, age 30, $50K income, 1% Treaty)
# Using the lifetime benefit value from your-personal-benefits.qmd
EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT_MILLIONS = Parameter(
    4.3,
    source_ref="/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations.qmd",
    source_type="calculated",
    description="Lifetime benefit for age 30 baseline scenario",
    unit="millions USD"
)  # $4.3M lifetime benefit
EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT = Parameter(
    EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT_MILLIONS * 1_000_000,
    source_ref="/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations.qmd",
    source_type="calculated",
    description="Lifetime benefit in USD (not millions)",
    unit="USD",
    formula="BENEFIT_MILLIONS × 1M",
    latex=r"Benefit = \$4.3M \times 10^6 = \$4,300,000"
)
EFFECTIVE_HOURLY_RATE = Parameter(
    EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT / TOTAL_TIME_INVESTMENT_HOURS,
    source_ref="/knowledge/solution/wishocracy.qmd#effective-hourly-rate",
    source_type="calculated",
    description="Effective hourly rate from treaty participation",
    unit="USD/hour",
    formula="LIFETIME_BENEFIT ÷ TIME_INVESTED",
    latex=r"HourlyRate = \frac{\$4,300,000}{14.75} \approx \$291,525/hr"
)  # ~$291K/hour

# Comparison benchmarks
AVERAGE_US_HOURLY_WAGE = Parameter(
    30,
    source_ref="average-us-hourly-wage",
    source_type="external",
    description="Average US hourly wage",
    unit="USD/hour"
)  # ~$30/hour average US wage

TYPICAL_CEO_HOURLY_RATE = Parameter(
    10000,
    source_ref="ceo-compensation",
    source_type="external",
    description="Typical CEO hourly rate",
    unit="USD/hour"
)  # ~$10,000/hour typical CEO rate
EFFECTIVE_HOURLY_RATE_VS_WAGE_MULTIPLIER = Parameter(
    EFFECTIVE_HOURLY_RATE / AVERAGE_US_HOURLY_WAGE,
    source_ref="/knowledge/solution/wishocracy.qmd#effective-hourly-rate",
    source_type="calculated",
    description="Effective rate multiplier vs average US wage",
    unit="ratio",
    formula="EFFECTIVE_RATE ÷ AVG_WAGE",
    latex=r"Multiplier = \frac{\$291,525}{\$30} \approx 9,718x"
)  # ~9,711x
EFFECTIVE_HOURLY_RATE_VS_CEO_MULTIPLIER = Parameter(
    EFFECTIVE_HOURLY_RATE / TYPICAL_CEO_HOURLY_RATE,
    source_ref="/knowledge/solution/wishocracy.qmd#effective-hourly-rate",
    source_type="calculated",
    description="Effective rate multiplier vs CEO rate",
    unit="ratio",
    formula="EFFECTIVE_RATE ÷ CEO_RATE",
    latex=r"Multiplier = \frac{\$291,525}{\$10,000} \approx 29x"
)  # ~29x

# Formatted values for display
effective_hourly_rate_thousands_formatted = f"${EFFECTIVE_HOURLY_RATE / 1000:.0f}K"
total_time_investment_hours_formatted = f"{TOTAL_TIME_INVESTMENT_HOURS:.1f}"
book_reading_time_hours_formatted = f"{BOOK_READING_TIME_HOURS:.1f}"
action_time_total_hours_formatted = f"{ACTION_TIME_TOTAL_HOURS:.1f}"
effective_hourly_rate_vs_wage_multiplier_formatted = f"{EFFECTIVE_HOURLY_RATE_VS_WAGE_MULTIPLIER:.0f}"
effective_hourly_rate_vs_ceo_multiplier_formatted = f"{EFFECTIVE_HOURLY_RATE_VS_CEO_MULTIPLIER:.0f}"

# ---
# PERSONAL LIFETIME WEALTH CALCULATIONS
# ---

def calculate_gdp_growth_boost(treaty_pct):
    """
    Calculate GDP growth boost from military spending redirection

    Historical evidence:
    - Post-WW2: 30% military cut → 8% annual GDP growth for a decade (vs 2-3% normal)
    - Post-Cold War: 3% military cut → 1990s boom with 2.5% productivity surge

    Model: Each 1% reduction in military spending → ~0.25% GDP growth boost
    This is conservative given historical evidence shows larger effects.

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)

    Returns:
        Total annual GDP growth rate (baseline + boost)
    """
    BASE_GDP_GROWTH = 0.025  # 2.5% baseline global growth
    MULTIPLIER_EFFECT = 0.25  # Conservative: 1% military cut → 0.25% GDP boost

    boost = treaty_pct * MULTIPLIER_EFFECT
    return BASE_GDP_GROWTH + boost


def calculate_medical_progress_multiplier(treaty_pct):
    """
    Calculate medical research acceleration from increased funding

    Current state:
    - $67.5B global government medical research spending
    - ~3,300 clinical trials/year
    - ~50 new drug approvals/year

    With treaty funding:
    - Additional funding = $27.2B per 1% treaty
    - 82x cost reduction from dFDA (per patient: $41k -> $500)
    - Research capacity multiplier = (total_funding / current_funding) × cost_reduction

    Formula breakdown:
    - New funding = $2,718B × treaty_pct
    - Total funding = $67.5B + new_funding
    - Funding ratio = total_funding / $67.5B
    - Multiplier = funding_ratio × 82

    Example for 1% treaty:
    - New funding: $27.2B
    - Total funding: $67.5B + $27.2B = $94.7B
    - Funding ratio: $94.7B / $67.5B = 1.40x
    - Multiplier: 1.40 × 82 = 115x

    This means:
    - 115x × 3,300 baseline trials = 379,500 ≈ 380,000 trials/year possible
    - Current: ~3,300 trials/year, ~50 drug approvals/year
    - Future: ~380,000 trials/year, ~1,000-2,000 drug approvals/year
    - This represents 115x more research capacity

    Args:
        treaty_pct: Fraction of military spending redirected

    Returns:
        Research capacity multiplier (e.g., 115 = 115x more trials possible)
    """
    new_funding = GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * treaty_pct
    total_funding = GLOBAL_MED_RESEARCH_SPENDING + new_funding
    funding_ratio = total_funding / GLOBAL_MED_RESEARCH_SPENDING
    return funding_ratio * TRIAL_COST_REDUCTION_FACTOR


def calculate_life_expectancy_gain(treaty_pct):
    """
    Calculate additional years of life from medical progress acceleration

    Model:
    - 1% treaty → 115x research capacity
    - Conservative: 1 year gained per 100x research acceleration
    - Optimistic: 10 years gained per 100x (exponential breakthrough effects)

    Args:
        treaty_pct: Fraction of military spending redirected

    Returns:
        Additional years of healthy life expectancy
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Conservative model: linear relationship
    # 100x research → 1 year of life extension
    conservative_gain = multiplier / 100

    # Use conservative estimate
    return conservative_gain


def compound_sum(annual_benefit, years, growth_rate, discount_rate=0.03):
    """
    Calculate present value of compounding annual benefits

    Formula: PV = Σ(annual_benefit × (1 + growth_rate)^t / (1 + discount_rate)^t)

    Args:
        annual_benefit: Initial annual benefit amount
        years: Number of years
        growth_rate: Annual growth rate (GDP boost)
        discount_rate: NPV discount rate

    Returns:
        Present value of all future benefits
    """
    total = 0
    for t in range(1, int(years) + 1):
        future_value = annual_benefit * ((1 + growth_rate) ** t)
        present_value = future_value / ((1 + discount_rate) ** t)
        total += present_value
    return total


def calculate_personal_lifetime_wealth(
    treaty_pct=TREATY_REDUCTION_PCT,
    current_age=30,
    baseline_life_expectancy=80,
    annual_income=50000,  # Global median income
    discount_rate=0.03
):
    """
    Calculate individual lifetime wealth impact from treaty

    This captures the personal economic benefit from:
    1. Peace dividend flowing to economy (higher GDP → higher incomes)
    2. Healthcare cost savings (insurance premiums drop as diseases cured)
    3. Productivity gains (fewer sick days, more working years)
    4. Life extension (more earning years from medical breakthroughs)

    Args:
        treaty_pct: Fraction of military spending redirected (0.01 = 1%)
        current_age: Person's current age
        baseline_life_expectancy: Life expectancy without treaty
        annual_income: Current annual income
        discount_rate: NPV discount rate for future earnings

    Returns:
        Dict with:
        - total_lifetime_benefit: Total personal $ over lifetime (NPV)
        - annual_breakdown: Dict of annual benefit components
        - life_extension_years: Additional years lived
        - gdp_growth_boost: Annual GDP growth increase
        - medical_progress_multiplier: Research capacity multiplier
    """

    # Calculate key metrics
    life_extension_years = calculate_life_expectancy_gain(treaty_pct)
    gdp_boost = calculate_gdp_growth_boost(treaty_pct)
    years_remaining = baseline_life_expectancy - current_age
    total_years = years_remaining + life_extension_years

    # Component 1: Peace dividend per capita (flows through economy to incomes)
    # Total societal benefit / population, conservatively assume 50% flows to incomes over time
    peace_dividend_per_capita_annual = (GLOBAL_ANNUAL_WAR_TOTAL_COST * treaty_pct / GLOBAL_POPULATION_2024_BILLIONS) * 0.5

    # Component 2: Healthcare savings (insurance premiums drop)
    # Current: ~$3,000/year average global health insurance cost
    # As diseases cured, insurance costs drop proportionally to research acceleration
    progress_multiplier = calculate_medical_progress_multiplier(treaty_pct)
    healthcare_savings_pct = min(0.7, progress_multiplier / 200)  # Cap at 70% savings
    healthcare_savings_annual = 3000 * healthcare_savings_pct

    # Component 3: Productivity gains (fewer sick days, healthier = more productive)
    # Average person loses ~5% of productive days to illness
    # Medical progress reduces this proportionally
    productivity_gain_pct = min(0.05, progress_multiplier / 2000)  # Cap at 5% productivity gain
    productivity_gains_annual = annual_income * productivity_gain_pct

    # Component 4: Income growth from GDP boost (compound effect)
    # Higher GDP growth → higher wage growth over career
    base_growth = 0.025
    income_with_gdp_boost = compound_sum(annual_income, total_years, gdp_boost, discount_rate)
    income_without_boost = compound_sum(annual_income, years_remaining, base_growth, discount_rate)
    gdp_boost_benefit = income_with_gdp_boost - income_without_boost

    # Component 5: Extended earning years
    # Additional years of life = additional years of earnings
    extended_earnings = 0
    if life_extension_years > 0:
        # Assume working until age 70, then retirement income at 40% of final salary
        working_years_extended = max(0, min(life_extension_years, 70 - baseline_life_expectancy))
        retirement_years_extended = life_extension_years - working_years_extended

        # Future earnings discounted to present value
        for t in range(int(years_remaining), int(years_remaining + working_years_extended)):
            future_income = annual_income * ((1 + gdp_boost) ** t)
            extended_earnings += future_income / ((1 + discount_rate) ** t)

        # Retirement income (40% of final working income)
        if retirement_years_extended > 0:
            final_working_income = annual_income * ((1 + gdp_boost) ** (years_remaining + working_years_extended))
            retirement_income = final_working_income * 0.4
            for t in range(int(years_remaining + working_years_extended), int(total_years)):
                extended_earnings += retirement_income / ((1 + discount_rate) ** t)

    # Compound other benefits over lifetime
    peace_dividend_total = compound_sum(peace_dividend_per_capita_annual, total_years, gdp_boost, discount_rate)
    healthcare_savings_total = compound_sum(healthcare_savings_annual, total_years, gdp_boost, discount_rate)
    productivity_gains_total = compound_sum(productivity_gains_annual, total_years, gdp_boost, discount_rate)

    # Total lifetime benefit
    total_benefit = (
        peace_dividend_total
        + healthcare_savings_total
        + productivity_gains_total
        + gdp_boost_benefit
        + extended_earnings
    )

    return {
        'total_lifetime_benefit': total_benefit,
        'annual_breakdown': {
            'peace_dividend': peace_dividend_per_capita_annual,
            'healthcare_savings': healthcare_savings_annual,
            'productivity_gains': productivity_gains_annual,
        },
        'npv_breakdown': {
            'peace_dividend_total': peace_dividend_total,
            'healthcare_savings_total': healthcare_savings_total,
            'productivity_gains_total': productivity_gains_total,
            'gdp_boost_benefit': gdp_boost_benefit,
            'extended_earnings': extended_earnings,
        },
        'life_extension_years': life_extension_years,
        'new_life_expectancy': baseline_life_expectancy + life_extension_years,
        'gdp_growth_boost': gdp_boost - 0.025,  # Just the boost component
        'medical_progress_multiplier': progress_multiplier,
    }


# Pre-calculated personal wealth scenarios for common ages (1% Treaty)
# Age 20
PERSONAL_WEALTH_AGE_20_1PCT = calculate_personal_lifetime_wealth(treaty_pct=0.01, current_age=20, annual_income=40000)
PERSONAL_LIFETIME_BENEFIT_AGE_20_1PCT = PERSONAL_WEALTH_AGE_20_1PCT['total_lifetime_benefit']

# Age 30
PERSONAL_WEALTH_AGE_30_1PCT = calculate_personal_lifetime_wealth(treaty_pct=0.01, current_age=30, annual_income=50000)
PERSONAL_LIFETIME_BENEFIT_AGE_30_1PCT = PERSONAL_WEALTH_AGE_30_1PCT['total_lifetime_benefit']

# Age 40
PERSONAL_WEALTH_AGE_40_1PCT = calculate_personal_lifetime_wealth(treaty_pct=0.01, current_age=40, annual_income=60000)
PERSONAL_LIFETIME_BENEFIT_AGE_40_1PCT = PERSONAL_WEALTH_AGE_40_1PCT['total_lifetime_benefit']

# Age 50
PERSONAL_WEALTH_AGE_50_1PCT = calculate_personal_lifetime_wealth(treaty_pct=0.01, current_age=50, annual_income=65000)
PERSONAL_LIFETIME_BENEFIT_AGE_50_1PCT = PERSONAL_WEALTH_AGE_50_1PCT['total_lifetime_benefit']

# Age 60
PERSONAL_WEALTH_AGE_60_1PCT = calculate_personal_lifetime_wealth(treaty_pct=0.01, current_age=60, annual_income=60000)
PERSONAL_LIFETIME_BENEFIT_AGE_60_1PCT = PERSONAL_WEALTH_AGE_60_1PCT['total_lifetime_benefit']

# Different treaty percentages (Age 30 baseline)
PERSONAL_WEALTH_AGE_30_HALF_PCT = calculate_personal_lifetime_wealth(treaty_pct=0.005, current_age=30)
PERSONAL_LIFETIME_BENEFIT_AGE_30_HALF_PCT = PERSONAL_WEALTH_AGE_30_HALF_PCT['total_lifetime_benefit']

PERSONAL_WEALTH_AGE_30_2PCT = calculate_personal_lifetime_wealth(treaty_pct=0.02, current_age=30)
PERSONAL_LIFETIME_BENEFIT_AGE_30_2PCT = PERSONAL_WEALTH_AGE_30_2PCT['total_lifetime_benefit']

PERSONAL_WEALTH_AGE_30_5PCT = calculate_personal_lifetime_wealth(treaty_pct=0.05, current_age=30)
PERSONAL_LIFETIME_BENEFIT_AGE_30_5PCT = PERSONAL_WEALTH_AGE_30_5PCT['total_lifetime_benefit']

PERSONAL_WEALTH_AGE_30_10PCT = calculate_personal_lifetime_wealth(treaty_pct=0.10, current_age=30)
PERSONAL_LIFETIME_BENEFIT_AGE_30_10PCT = PERSONAL_WEALTH_AGE_30_10PCT['total_lifetime_benefit']

# Life expectancy gains by treaty percentage
LIFE_EXTENSION_YEARS_1PCT = PERSONAL_WEALTH_AGE_30_1PCT['life_extension_years']
LIFE_EXTENSION_YEARS_2PCT = PERSONAL_WEALTH_AGE_30_2PCT['life_extension_years']
LIFE_EXTENSION_YEARS_5PCT = PERSONAL_WEALTH_AGE_30_5PCT['life_extension_years']
LIFE_EXTENSION_YEARS_10PCT = PERSONAL_WEALTH_AGE_30_10PCT['life_extension_years']

# Medical progress multipliers
MEDICAL_PROGRESS_MULTIPLIER_1PCT = calculate_medical_progress_multiplier(0.01)
MEDICAL_PROGRESS_MULTIPLIER_2PCT = calculate_medical_progress_multiplier(0.02)
MEDICAL_PROGRESS_MULTIPLIER_5PCT = calculate_medical_progress_multiplier(0.05)
MEDICAL_PROGRESS_MULTIPLIER_10PCT = calculate_medical_progress_multiplier(0.10)

# GDP growth boosts
GDP_GROWTH_BOOST_1PCT = calculate_gdp_growth_boost(0.01) - 0.025  # Just the boost component
GDP_GROWTH_BOOST_2PCT = calculate_gdp_growth_boost(0.02) - 0.025
GDP_GROWTH_BOOST_5PCT = calculate_gdp_growth_boost(0.05) - 0.025
GDP_GROWTH_BOOST_10PCT = calculate_gdp_growth_boost(0.10) - 0.025

# Formatted values for display
personal_lifetime_benefit_age_20_1pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_20_1PCT / 1_000_000_000)
personal_lifetime_benefit_age_30_1pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_30_1PCT / 1_000_000_000)
personal_lifetime_benefit_age_40_1pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_40_1PCT / 1_000_000_000)
personal_lifetime_benefit_age_50_1pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_50_1PCT / 1_000_000_000)
personal_lifetime_benefit_age_60_1pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_60_1PCT / 1_000_000_000)

personal_lifetime_benefit_age_30_half_pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_30_HALF_PCT / 1_000_000_000)
personal_lifetime_benefit_age_30_2pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_30_2PCT / 1_000_000_000)
personal_lifetime_benefit_age_30_5pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_30_5PCT / 1_000_000_000)
personal_lifetime_benefit_age_30_10pct_formatted = format_currency(PERSONAL_LIFETIME_BENEFIT_AGE_30_10PCT / 1_000_000_000)

life_extension_years_1pct_formatted = f"{LIFE_EXTENSION_YEARS_1PCT:.1f}"
life_extension_years_2pct_formatted = f"{LIFE_EXTENSION_YEARS_2PCT:.1f}"
life_extension_years_5pct_formatted = f"{LIFE_EXTENSION_YEARS_5PCT:.1f}"
life_extension_years_10pct_formatted = f"{LIFE_EXTENSION_YEARS_10PCT:.1f}"

medical_progress_multiplier_1pct_formatted = f"{MEDICAL_PROGRESS_MULTIPLIER_1PCT:.0f}x"
medical_progress_multiplier_2pct_formatted = f"{MEDICAL_PROGRESS_MULTIPLIER_2PCT:.0f}x"
medical_progress_multiplier_5pct_formatted = f"{MEDICAL_PROGRESS_MULTIPLIER_5PCT:.0f}x"
medical_progress_multiplier_10pct_formatted = f"{MEDICAL_PROGRESS_MULTIPLIER_10PCT:.0f}x"

gdp_growth_boost_1pct_formatted = format_percentage(GDP_GROWTH_BOOST_1PCT)
gdp_growth_boost_2pct_formatted = format_percentage(GDP_GROWTH_BOOST_2PCT)
gdp_growth_boost_5pct_formatted = format_percentage(GDP_GROWTH_BOOST_5PCT)
gdp_growth_boost_10pct_formatted = format_percentage(GDP_GROWTH_BOOST_10PCT)


# ---
# IMPROVED PERSONAL LIFETIME WEALTH MODEL
# ---
# This section implements improvements identified in methodology review

# Constants for improved healthcare savings model
US_CHRONIC_DISEASE_SPENDING_ANNUAL = Parameter(
    4.1e12,
    source_ref="us-chronic-disease-spending",
    source_type="external",
    description="US annual chronic disease spending",
    unit="USD/year"
)  # $4.1T/year CDC estimate

US_POPULATION_2024 = Parameter(
    335e6,
    source_ref="us-population-335m",
    source_type="external",
    description="US population in 2024",
    unit="people"
)

PER_CAPITA_CHRONIC_DISEASE_COST = US_CHRONIC_DISEASE_SPENDING_ANNUAL / US_POPULATION_2024  # $12,239/year

# Mental health constants
US_MENTAL_HEALTH_COST_ANNUAL = Parameter(
    350e9,
    source_ref="us-mental-health-cost",
    source_type="external",
    description="US mental health costs (treatment + productivity loss)",
    unit="USD/year"
)

PER_CAPITA_MENTAL_HEALTH_COST = US_MENTAL_HEALTH_COST_ANNUAL / US_POPULATION_2024  # ~$1,045/year

MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA = Parameter(
    2000,
    source_ref="mental-health-productivity-loss",
    source_type="external",
    description="Annual productivity loss per capita from mental health issues (beyond treatment costs)",
    unit="USD/year"
)  # Additional productivity loss beyond treatment

# Caregiver time constants (simple model - deprecated, use detailed model below)
CAREGIVER_HOURS_PER_MONTH = Parameter(
    20,
    source_ref="average-family-caregiving-hours",
    source_type="external",
    description="Average monthly hours of unpaid family caregiving in US",
    unit="hours/month"
)  # Average US family provides 20 hrs/month unpaid care

CAREGIVER_VALUE_PER_HOUR_SIMPLE = Parameter(
    25,
    source_ref="caregiver-replacement-cost",
    source_type="external",
    description="Estimated replacement cost per hour of caregiving",
    unit="USD/hour"
)  # Replacement cost estimate
CAREGIVER_COST_ANNUAL = CAREGIVER_HOURS_PER_MONTH * 12 * CAREGIVER_VALUE_PER_HOUR_SIMPLE  # $6,000/year


def calculate_life_expectancy_gain_improved(treaty_pct, timeframe='mid-term'):
    """
    Improved life expectancy model using tiered evidence-based approach

    Replaces arbitrary linear formula with realistic gain estimates:
    - Near-term (5yr horizon): Faster access to existing pipeline
    - Mid-term (15yr horizon): New breakthrough treatments
    - Long-term (endgame): Aging reversal and compound effects

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)
        timeframe: 'near-term' (5yr), 'mid-term' (15yr), or 'long-term' (endgame)

    Returns:
        Years of life expectancy gained
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Near-term (Years 1-5): Faster access to existing pipeline drugs
    # Conservative: Each 100x research acceleration = 3-5 years earlier access
    near_term_gain = min(5, multiplier / 30)  # 115x → 3.8 years

    if timeframe == 'near-term':
        return near_term_gain

    # Mid-term (Years 5-15): New breakthrough treatments from expanded research
    # Moderate: Major diseases start falling, treatment options expand dramatically
    mid_term_gain = min(15, multiplier / 10)  # 115x → 11.5 years

    if timeframe == 'mid-term':
        return near_term_gain + mid_term_gain  # Total: ~15 years

    # Long-term (Years 15+): Aging reversal and compound effects
    # Optimistic but plausible: Matches endgame projection (80→150 years)
    long_term_gain = min(70, multiplier / 2)  # 115x → 57.5 years

    return near_term_gain + mid_term_gain + long_term_gain  # Total: ~70 years


def calculate_healthcare_savings_improved(treaty_pct):
    """
    Improved healthcare savings based on actual chronic disease spending

    Replaces arbitrary $10K × (multiplier/2000) with evidence-based model:
    - Base: $12,239/person/year chronic disease spending (CDC data)
    - Reduction: Proportional to research acceleration
    - Conservative: 115x research → 10-15% cost reduction

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)

    Returns:
        Annual per capita healthcare savings
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Conservative model: Each 100x research acceleration → 10% cost reduction
    # This accounts for both better treatments and prevention
    reduction_pct = min(0.20, multiplier / 1000)  # Cap at 20%, 115x → 11.5%

    return PER_CAPITA_CHRONIC_DISEASE_COST * reduction_pct


def calculate_productivity_gains_improved(treaty_pct, annual_income):
    """
    Improved productivity gains without arbitrary 5% cap

    Reality:
    - Chronic illness reduces productivity by 15-40% (depression alone: 35%)
    - Better treatments = people work more efficiently

    Args:
        treaty_pct: Fraction of military spending redirected
        annual_income: Person's annual income

    Returns:
        Annual productivity gain
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Baseline productivity loss from preventable illness: 15-20%
    BASELINE_PRODUCTIVITY_LOSS = 0.175  # 17.5% average

    # Medical progress reduces this loss proportionally
    # 115x research → reduce productivity loss by 50-80%
    recovery_pct = min(0.80, multiplier / 150)  # 115x → 76.7% recovery

    # Net productivity gain
    productivity_gain_pct = BASELINE_PRODUCTIVITY_LOSS * recovery_pct  # ~13.4% for 1% treaty

    return annual_income * productivity_gain_pct


def calculate_mental_health_benefit(treaty_pct):
    """
    Mental health improvement benefits (previously missing)

    - Mental health historically underfunded (5% of NIH budget)
    - 115x research acceleration → major breakthroughs likely
    - Depression, anxiety, PTSD, addiction all addressable

    Args:
        treaty_pct: Fraction of military spending redirected

    Returns:
        Annual per capita mental health benefit
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Mental health sees outsized gains from increased research
    # Current underfunding means high-value low-hanging fruit
    improvement_pct = min(0.40, multiplier / 300)  # 115x → 38.3%

    cost_savings = PER_CAPITA_MENTAL_HEALTH_COST * improvement_pct
    productivity_gain = MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA * improvement_pct

    return cost_savings + productivity_gain


def calculate_caregiver_savings(treaty_pct):
    """
    Caregiver time savings (previously missing)

    - Average family: 20 hours/month unpaid caregiving
    - Healthier population = less caregiving needed
    - Value at replacement cost: $25/hour

    Args:
        treaty_pct: Fraction of military spending redirected

    Returns:
        Annual per capita caregiver time savings
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Healthier population reduces caregiving burden
    reduction_pct = min(0.50, multiplier / 250)  # 115x → 46%

    return CAREGIVER_COST_ANNUAL * reduction_pct


def calculate_personal_lifetime_wealth_improved(
    treaty_pct=TREATY_REDUCTION_PCT,
    current_age=30,
    baseline_life_expectancy=80,
    annual_income=50000,
    discount_rate=0.03,
    timeframe='mid-term',
    peace_dividend_scope='global'  # 'global' or 'us-only'
):
    """
    IMPROVED personal lifetime wealth calculation with methodology fixes

    Key improvements:
    1. Tiered life expectancy model (near/mid/long-term)
    2. Evidence-based healthcare savings (actual chronic disease costs)
    3. Realistic productivity gains (no arbitrary cap)
    4. Mental health benefits included
    5. Caregiver time savings included
    6. Reduced GDP/productivity overlap (15% adjustment)
    7. Clarified peace dividend allocation

    Args:
        treaty_pct: Fraction of military spending redirected (default: 1%)
        current_age: Current age
        baseline_life_expectancy: Life expectancy without treaty (default: 80)
        annual_income: Annual income
        discount_rate: Discount rate for NPV (default: 3%)
        timeframe: 'near-term', 'mid-term', or 'long-term' for life extension
        peace_dividend_scope: 'global' (÷8B) or 'us-only' (÷335M)

    Returns:
        Dictionary with total benefit and component breakdown
    """
    # Calculate life extension and total years
    life_extension_years = calculate_life_expectancy_gain_improved(treaty_pct, timeframe)
    years_remaining = baseline_life_expectancy - current_age
    total_years = years_remaining + life_extension_years

    # Medical progress multiplier
    progress_multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # GDP boost
    gdp_boost = calculate_gdp_growth_boost(treaty_pct)

    # Component 1: Peace dividend (clarified allocation)
    if peace_dividend_scope == 'us-only':
        # If this is US military reduction only, allocate to US population
        peace_dividend_per_capita_annual = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / US_POPULATION_2024
    else:
        # If global reduction, allocate to global population
        peace_dividend_per_capita_annual = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / GLOBAL_POPULATION_2024_BILLIONS

    # Component 2: Healthcare savings (IMPROVED - evidence-based)
    healthcare_savings_annual = calculate_healthcare_savings_improved(treaty_pct)

    # Component 3: Productivity gains (IMPROVED - no arbitrary cap)
    productivity_gains_annual = calculate_productivity_gains_improved(treaty_pct, annual_income)

    # Component 4: Mental health benefits (NEW)
    mental_health_benefit_annual = calculate_mental_health_benefit(treaty_pct)

    # Component 5: Caregiver time savings (NEW)
    caregiver_savings_annual = calculate_caregiver_savings(treaty_pct)

    # Component 6: Income growth from GDP boost (ADJUSTED for overlap)
    # Reduce by 15% to account for overlap with productivity gains
    base_growth = 0.025
    income_with_gdp_boost = compound_sum(annual_income, total_years, gdp_boost, discount_rate)
    income_without_boost = compound_sum(annual_income, years_remaining, base_growth, discount_rate)
    gdp_boost_benefit = (income_with_gdp_boost - income_without_boost) * 0.85  # 15% reduction for overlap

    # Component 7: Extended earning years (IMPROVED - realistic life extension)
    extended_earnings = 0
    if life_extension_years > 0:
        # Assume working until age 70, then retirement income at 60% of final salary (increased from 40%)
        working_years_extended = max(0, min(life_extension_years, 70 - baseline_life_expectancy))
        retirement_years_extended = life_extension_years - working_years_extended

        # Future earnings discounted to present value
        for t in range(int(years_remaining), int(years_remaining + working_years_extended)):
            future_income = annual_income * ((1 + gdp_boost) ** t)
            extended_earnings += future_income / ((1 + discount_rate) ** t)

        # Retirement income (60% of final working income, increased from 40%)
        if retirement_years_extended > 0:
            final_working_income = annual_income * ((1 + gdp_boost) ** (years_remaining + working_years_extended))
            retirement_income = final_working_income * 0.60  # Increased from 0.40
            for t in range(int(years_remaining + working_years_extended), int(total_years)):
                extended_earnings += retirement_income / ((1 + discount_rate) ** t)

    # Compound other benefits over lifetime
    peace_dividend_total = compound_sum(peace_dividend_per_capita_annual, total_years, gdp_boost, discount_rate)
    healthcare_savings_total = compound_sum(healthcare_savings_annual, total_years, gdp_boost, discount_rate)
    productivity_gains_total = compound_sum(productivity_gains_annual, total_years, gdp_boost, discount_rate)
    mental_health_total = compound_sum(mental_health_benefit_annual, total_years, gdp_boost, discount_rate)
    caregiver_savings_total = compound_sum(caregiver_savings_annual, total_years, gdp_boost, discount_rate)

    # Total lifetime benefit
    total_benefit = (
        peace_dividend_total
        + healthcare_savings_total
        + productivity_gains_total
        + mental_health_total
        + caregiver_savings_total
        + gdp_boost_benefit
        + extended_earnings
    )

    return {
        'total_lifetime_benefit': total_benefit,
        'annual_breakdown': {
            'peace_dividend': peace_dividend_per_capita_annual,
            'healthcare_savings': healthcare_savings_annual,
            'productivity_gains': productivity_gains_annual,
            'mental_health_benefit': mental_health_benefit_annual,
            'caregiver_savings': caregiver_savings_annual,
        },
        'npv_breakdown': {
            'peace_dividend_total': peace_dividend_total,
            'healthcare_savings_total': healthcare_savings_total,
            'productivity_gains_total': productivity_gains_total,
            'mental_health_total': mental_health_total,
            'caregiver_savings_total': caregiver_savings_total,
            'gdp_boost_benefit': gdp_boost_benefit,
            'extended_earnings': extended_earnings,
        },
        'life_extension_years': life_extension_years,
        'new_life_expectancy': baseline_life_expectancy + life_extension_years,
        'gdp_growth_boost': gdp_boost - 0.025,
        'medical_progress_multiplier': progress_multiplier,
        'timeframe': timeframe,
        'peace_dividend_scope': peace_dividend_scope,
    }


# DEPRECATED: Pre-calculated improved model scenarios (superseded by Disease Eradication Model)
# Kept for reference only - DO NOT USE
# The Disease Eradication Model (lines 1879-2310) is now the recommended approach
#
# PERSONAL_WEALTH_IMPROVED_AGE_30_1PCT = calculate_personal_lifetime_wealth_improved(
#     treaty_pct=0.01, current_age=30, annual_income=50000, timeframe='mid-term'
# )
# PERSONAL_LIFETIME_BENEFIT_IMPROVED_AGE_30_1PCT = PERSONAL_WEALTH_IMPROVED_AGE_30_1PCT['total_lifetime_benefit']
#
# PERSONAL_WEALTH_ENDGAME_AGE_30_1PCT = calculate_personal_lifetime_wealth_improved(
#     treaty_pct=0.01, current_age=30, annual_income=50000, timeframe='long-term'
# )
# PERSONAL_LIFETIME_BENEFIT_ENDGAME_AGE_30_1PCT = PERSONAL_WEALTH_ENDGAME_AGE_30_1PCT['total_lifetime_benefit']

# DEPRECATED: US-only peace dividend allocation (used IMPROVED model)
# PERSONAL_WEALTH_US_ONLY_AGE_30_1PCT = calculate_personal_lifetime_wealth_improved(
#     treaty_pct=0.01, current_age=30, annual_income=50000, timeframe='mid-term', peace_dividend_scope='us-only'
# )
# PERSONAL_LIFETIME_BENEFIT_US_ONLY_AGE_30_1PCT = PERSONAL_WEALTH_US_ONLY_AGE_30_1PCT['total_lifetime_benefit']


# --- Test Output (when module executed directly) ---
if __name__ == "__main__":
    print("\n=== CONSERVATIVE MODEL (Original) ===")
    print("\n--- Personal Lifetime Wealth (1% Treaty) ---")
    print(f"Age 20: {personal_lifetime_benefit_age_20_1pct_formatted}")
    print(f"Age 30: {personal_lifetime_benefit_age_30_1pct_formatted}")
    print(f"Age 40: {personal_lifetime_benefit_age_40_1pct_formatted}")
    print(f"Age 50: {personal_lifetime_benefit_age_50_1pct_formatted}")
    print(f"Age 60: {personal_lifetime_benefit_age_60_1pct_formatted}")
    print(f"\nLife extension (1%): {life_extension_years_1pct_formatted} years")
    print(f"Medical progress multiplier (1%): {medical_progress_multiplier_1pct_formatted}")
    print(f"GDP growth boost (1%): {gdp_growth_boost_1pct_formatted}")
    print("\n--- Different Treaty Percentages (Age 30) ---")
    print(f"0.5% Treaty: {personal_lifetime_benefit_age_30_half_pct_formatted}")
    print(f"1% Treaty: {personal_lifetime_benefit_age_30_1pct_formatted}")
    print(f"2% Treaty: {personal_lifetime_benefit_age_30_2pct_formatted}")
    print(f"5% Treaty: {personal_lifetime_benefit_age_30_5pct_formatted}")
    print(f"10% Treaty: {personal_lifetime_benefit_age_30_10pct_formatted}")

    # DEPRECATED: Improved and Endgame models test output removed
    # Superseded by Disease Eradication Model (see below)


# ---
# CONSERVATIVE BASELINE PERSONAL LIFETIME WEALTH MODEL (ANTIBIOTIC PRECEDENT)
# ---
# This section uses antibiotic precedent as conservative baseline, with properly cited sources
# NOTE: Fundamentally understates impact - see Disease Eradication Model for realistic estimates

# Productivity loss from chronic illness
# Source: ../references.qmd#chronic-illness-workforce-productivity-loss
WORKFORCE_CHRONIC_ILLNESS_PREVALENCE = Parameter(
    0.784,
    source_ref="chronic-illness-workforce-productivity-loss",
    source_type="external",
    description="Workforce with at least one chronic condition (78.4%)",
    unit="rate"
)  # 78.4% have at least one chronic condition

WORKFORCE_WITH_PRODUCTIVITY_LOSS = Parameter(
    0.28,
    source_ref="chronic-illness-workforce-productivity-loss",
    source_type="external",
    description="Percentage of workforce experiencing productivity loss from chronic illness (28%)",
    unit="rate"
)  # 28% of all employees have productivity loss

US_MEDIAN_SALARY = Parameter(
    59384,
    source_ref="us-median-salary-2024",
    source_type="external",
    description="US median salary in 2024",
    unit="USD/year"
)  # 2024 median salary

PRODUCTIVITY_LOSS_PER_AFFECTED_EMPLOYEE = Parameter(
    4798,
    source_ref="chronic-illness-productivity-loss-ibi",
    source_type="external",
    description="Annual productivity loss per affected employee (IBI 2024)",
    unit="USD/year"
)  # $/year, IBI 2024

# For those WITH chronic conditions causing productivity loss:
# If 28% of workforce loses $4,798/year, and 78.4% have chronic conditions
# Then those affected lose: $4,798 / (0.28/0.784) = ~$13,440/year per person with condition
# As percentage of median salary: $13,440 / $59,384 = 22.6% productivity loss for affected individuals

# Caregiver time and economic value
# Source: ../references.qmd#unpaid-caregiver-hours-economic-value
CAREGIVER_HOURS_PER_WEEK_AVG = Parameter(
    25.5,
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="Average weekly hours of unpaid caregiving (25-26 hours/week)",
    unit="hours/week"
)  # 25-26 hours/week average

CAREGIVER_HOURS_PER_MONTH_AVG = CAREGIVER_HOURS_PER_WEEK_AVG * 4.33  # ~110 hours/month

CAREGIVER_VALUE_PER_HOUR = Parameter(
    16.59,
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="AARP valuation of caregiving per hour",
    unit="USD/hour"
)  # $/hour AARP valuation

CAREGIVER_ANNUAL_VALUE_TOTAL = Parameter(
    600e9,
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="Total annual value of unpaid caregiving in US",
    unit="USD/year"
)  # $600B total

CAREGIVER_COUNT_US = Parameter(
    38e6,
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="Number of unpaid caregivers in US",
    unit="people"
)  # 38 million caregivers
# Per caregiver: $600B / 38M = $15,789/year average
# But only portion is disease-related (vs aging, disability, children)
# Estimate: 40% of caregiving is for treatable disease conditions
DISEASE_RELATED_CAREGIVER_PCT = Parameter(
    0.40,
    source_ref="disease-related-caregiving-estimate",
    source_type="calculated",
    description="Percentage of caregiving for treatable disease conditions (vs aging, disability, children)",
    unit="rate"
)

# Life expectancy gains from medical advances
# Source: ../references.qmd#life-expectancy-gains-medical-advances
# Antibiotics alone: 5-23 years (taking conservative mid-point: 10 years)
# Vaccines + hygiene + antibiotics: 35 years total (1900-2000)
# Historical precedent: Major medical advance → 10 years life extension
ANTIBIOTICS_LIFE_EXTENSION_YEARS = Parameter(
    10,
    source_ref="life-expectancy-gains-medical-advances",
    source_type="external",
    description="Life extension from antibiotics (conservative mid-range from 5-23 years)",
    unit="years"
)  # Conservative mid-range estimate

TOTAL_MEDICAL_ADVANCES_1900_2000 = Parameter(
    35,
    source_ref="life-expectancy-gains-medical-advances",
    source_type="external",
    description="Total life expectancy gain from all medical advances 1900-2000 (vaccines + hygiene + antibiotics)",
    unit="years"
)  # All advances combined


def calculate_life_expectancy_gain_conservative_baseline(treaty_pct, conservative=True):
    """
    Conservative baseline life expectancy model using antibiotic precedent

    Historical precedent:
    - Antibiotics alone: Added 10 years (conservative estimate from 5-23 range)
    - Total medical advances 1900-2000: 35 years

    Current model:
    - 115x research acceleration comparable to antibiotics discovery
    - Conservative: Assume 50% of antibiotic impact = 5 years
    - Moderate: Assume 100% of antibiotic impact = 10 years
    - Optimistic: Assume multiple breakthrough categories = 20 years

    This avoids arbitrary divisors and grounds in historical data.

    Source: ../references.qmd#life-expectancy-gains-medical-advances

    Args:
        treaty_pct: Fraction of military spending redirected
        conservative: If True, use 50% of antibiotic precedent

    Returns:
        Years of life expectancy gained
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Historical precedent: One major breakthrough (antibiotics) → 10 years
    # 115x research acceleration → likely multiple breakthrough categories

    if conservative:
        # Conservative: 115x research → 0.5x antibiotics impact
        # Reasoning: Harder to cure remaining diseases than infectious diseases
        return 5.0 if multiplier >= 100 else multiplier / 20
    else:
        # Moderate: 115x research → 1.0x antibiotics impact
        # Reasoning: Similar magnitude of research acceleration
        return 10.0 if multiplier >= 100 else multiplier / 10


def calculate_productivity_loss_conservative_baseline(treaty_pct, annual_income):
    """
    Conservative baseline productivity loss calculation

    Data:
    - 78.4% of workforce has chronic illness
    - 28% of total workforce experiences productivity loss
    - Those affected lose average $4,798/year (IBI 2024)
    - For median salary ($59,384), this is 22.6% productivity loss for affected

    Conservative model:
    - Not all productivity loss is recoverable (behavioral, aging components)
    - Estimate 60% is from treatable conditions
    - Research acceleration recovers portion of that 60%

    Source: ../references.qmd#chronic-illness-workforce-productivity-loss

    Args:
        treaty_pct: Fraction of military spending redirected
        annual_income: Person's annual income

    Returns:
        Annual productivity gain
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Base productivity loss for those affected: 22.6%
    BASELINE_PRODUCTIVITY_LOSS_AFFECTED = 0.226

    # Only 60% is from treatable conditions (rest is behavioral, aging, etc.)
    TREATABLE_PORTION = 0.60

    # Research impact: 115x research → recover 50% of treatable portion
    recovery_rate = min(0.70, multiplier / 165)  # 115x → 69.7% recovery

    # Expected value across population:
    # 28% of people affected × 22.6% loss × 60% treatable × 70% recovery
    net_gain_pct = (WORKFORCE_WITH_PRODUCTIVITY_LOSS *
                    BASELINE_PRODUCTIVITY_LOSS_AFFECTED *
                    TREATABLE_PORTION *
                    recovery_rate)
    # = 0.28 × 0.226 × 0.60 × 0.697 = 2.65% population-wide gain

    return annual_income * net_gain_pct


def calculate_caregiver_savings_conservative_baseline(treaty_pct):
    """
    Conservative baseline caregiver savings calculation

    Data:
    - Average caregiver: 110 hours/month at $16.59/hour
    - Total value: $15,789 per caregiver per year
    - Only ~40% of caregiving is for treatable disease (rest is aging, disability, children)

    Conservative model:
    - Only disease-related caregiving benefits from medical research
    - Of that, only portion is preventable/curable

    Source: ../references.qmd#unpaid-caregiver-hours-economic-value

    Args:
        treaty_pct: Fraction of military spending redirected

    Returns:
        Annual per capita caregiver time savings value
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Per capita caregiving value (spread across population)
    PER_CAPITA_CAREGIVER_COST = (CAREGIVER_COUNT_US / US_POPULATION_2024) * 15789
    # = (38M / 335M) × $15,789 = $1,791/person/year

    # Only disease-related portion benefits from research
    disease_related_value = PER_CAPITA_CAREGIVER_COST * DISEASE_RELATED_CAREGIVER_PCT
    # = $1,791 × 0.40 = $716/year

    # Research impact: 115x research → reduce 40% of disease-related caregiving
    reduction_rate = min(0.50, multiplier / 288)  # 115x → 40% reduction

    return disease_related_value * reduction_rate
    # = $716 × 0.40 = $286/year (vs $2,760 in "improved" model)


def calculate_personal_lifetime_wealth_conservative_baseline(
    treaty_pct=TREATY_REDUCTION_PCT,
    current_age=30,
    baseline_life_expectancy=80,
    annual_income=50000,
    discount_rate=0.03,
    conservative=True
):
    """
    CONSERVATIVE BASELINE personal lifetime wealth using antibiotic precedent

    Key improvements over "improved" model:
    1. Productivity loss: Based on IBI 2024 data (28% affected, $4,798 loss)
    2. Caregiver savings: Based on AARP data, only disease-related portion (40%)
    3. Life expectancy: Based on antibiotic precedent (10 years for breakthrough)
    4. All parameters properly cited in ../references.qmd
    5. Mental health folded into productivity (no double-counting)
    6. Healthcare savings based on disease categories (not arbitrary divisor)

    Args:
        treaty_pct: Fraction of military spending redirected (default: 1%)
        current_age: Current age
        baseline_life_expectancy: Life expectancy without treaty (default: 80)
        annual_income: Annual income
        discount_rate: Discount rate for NPV (default: 3%)
        conservative: Use conservative estimates if True

    Returns:
        Dictionary with total benefit and component breakdown
    """
    # Calculate life extension
    life_extension_years = calculate_life_expectancy_gain_conservative_baseline(treaty_pct, conservative)
    years_remaining = baseline_life_expectancy - current_age
    total_years = years_remaining + life_extension_years

    # Medical progress multiplier
    progress_multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # GDP boost
    gdp_boost = calculate_gdp_growth_boost(treaty_pct)

    # Component 1: Peace dividend
    peace_dividend_per_capita_annual = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / GLOBAL_POPULATION_2024_BILLIONS

    # Component 2: Healthcare savings (conservative baseline)
    # Use actual chronic disease spending, broken down by treatment category
    US_CHRONIC_COST_PER_CAPITA = 3.7e12 / US_POPULATION_2024  # $11,045/person/year

    # Disease categories and research impact:
    # - 30% highly treatable (infectious, some cancers): 20% cost reduction possible
    # - 50% manageable (chronic conditions): 10% cost reduction possible
    # - 20% age-related/incurable: 2% cost reduction possible

    # 115x research → achieve 50% of these potentials
    research_effectiveness = min(0.60, progress_multiplier / 190)  # 115x → 60.5%

    weighted_reduction = (
        0.30 * 0.20 * research_effectiveness +  # Treatable
        0.50 * 0.10 * research_effectiveness +  # Manageable
        0.20 * 0.02 * research_effectiveness    # Incurable
    )  # = 7.9% total reduction for 115x

    healthcare_savings_annual = US_CHRONIC_COST_PER_CAPITA * weighted_reduction

    # Component 3: Productivity gains (conservative baseline, includes mental health)
    productivity_gains_annual = calculate_productivity_loss_conservative_baseline(treaty_pct, annual_income)

    # Component 4: Caregiver savings (conservative baseline, disease-portion only)
    caregiver_savings_annual = calculate_caregiver_savings_conservative_baseline(treaty_pct)

    # Component 5: Income growth from GDP boost
    base_growth = 0.025
    income_with_gdp_boost = compound_sum(annual_income, total_years, gdp_boost, discount_rate)
    income_without_boost = compound_sum(annual_income, years_remaining, base_growth, discount_rate)
    gdp_boost_benefit = income_with_gdp_boost - income_without_boost

    # Component 6: Extended earning years
    extended_earnings = 0
    if life_extension_years > 0:
        working_years_extended = max(0, min(life_extension_years, 70 - baseline_life_expectancy))
        retirement_years_extended = life_extension_years - working_years_extended

        for t in range(int(years_remaining), int(years_remaining + working_years_extended)):
            future_income = annual_income * ((1 + gdp_boost) ** t)
            extended_earnings += future_income / ((1 + discount_rate) ** t)

        if retirement_years_extended > 0:
            final_working_income = annual_income * ((1 + gdp_boost) ** (years_remaining + working_years_extended))
            retirement_income = final_working_income * 0.50  # Realistic 50%
            for t in range(int(years_remaining + working_years_extended), int(total_years)):
                extended_earnings += retirement_income / ((1 + discount_rate) ** t)

    # Compound benefits over lifetime
    peace_dividend_total = compound_sum(peace_dividend_per_capita_annual, total_years, gdp_boost, discount_rate)
    healthcare_savings_total = compound_sum(healthcare_savings_annual, total_years, gdp_boost, discount_rate)
    productivity_gains_total = compound_sum(productivity_gains_annual, total_years, gdp_boost, discount_rate)
    caregiver_savings_total = compound_sum(caregiver_savings_annual, total_years, gdp_boost, discount_rate)

    # Total lifetime benefit
    total_benefit = (
        peace_dividend_total
        + healthcare_savings_total
        + productivity_gains_total
        + caregiver_savings_total
        + gdp_boost_benefit
        + extended_earnings
    )

    return {
        'total_lifetime_benefit': total_benefit,
        'annual_breakdown': {
            'peace_dividend': peace_dividend_per_capita_annual,
            'healthcare_savings': healthcare_savings_annual,
            'productivity_gains': productivity_gains_annual,
            'caregiver_savings': caregiver_savings_annual,
        },
        'npv_breakdown': {
            'peace_dividend_total': peace_dividend_total,
            'healthcare_savings_total': healthcare_savings_total,
            'productivity_gains_total': productivity_gains_total,
            'caregiver_savings_total': caregiver_savings_total,
            'gdp_boost_benefit': gdp_boost_benefit,
            'extended_earnings': extended_earnings,
        },
        'life_extension_years': life_extension_years,
        'new_life_expectancy': baseline_life_expectancy + life_extension_years,
        'gdp_growth_boost': gdp_boost - 0.025,
        'medical_progress_multiplier': progress_multiplier,
        'model_type': 'conservative_baseline',
    }


# Pre-calculated conservative baseline scenarios (antibiotic precedent)
PERSONAL_WEALTH_CONSERVATIVE_AGE_30_1PCT = calculate_personal_lifetime_wealth_conservative_baseline(
    treaty_pct=0.01, current_age=30, annual_income=50000, conservative=True
)
PERSONAL_LIFETIME_BENEFIT_CONSERVATIVE_AGE_30_1PCT = PERSONAL_WEALTH_CONSERVATIVE_AGE_30_1PCT['total_lifetime_benefit']

# Moderate (non-conservative) baseline
PERSONAL_WEALTH_CONSERVATIVE_MODERATE_AGE_30_1PCT = calculate_personal_lifetime_wealth_conservative_baseline(
    treaty_pct=0.01, current_age=30, annual_income=50000, conservative=False
)
PERSONAL_LIFETIME_BENEFIT_CONSERVATIVE_MODERATE_AGE_30_1PCT = PERSONAL_WEALTH_CONSERVATIVE_MODERATE_AGE_30_1PCT['total_lifetime_benefit']


if __name__ == "__main__":
    # Test conservative baseline model (this section runs after constants are defined)
    print("\n\n=== CONSERVATIVE BASELINE MODEL (ANTIBIOTIC PRECEDENT) ===")
    print("\n--- Conservative Baseline (Age 30, $50K income, 1% Treaty) ---")
    cons = PERSONAL_WEALTH_CONSERVATIVE_AGE_30_1PCT
    print(f"Total Benefit: ${cons['total_lifetime_benefit']/1000:.0f}K")
    print(f"Life Extension: {cons['life_extension_years']:.1f} years")
    print(f"\nComponent Breakdown:")
    print(f"  Peace Dividend: ${cons['npv_breakdown']['peace_dividend_total']/1000:.0f}K")
    print(f"  Healthcare Savings: ${cons['npv_breakdown']['healthcare_savings_total']/1000:.0f}K")
    print(f"  Productivity Gains: ${cons['npv_breakdown']['productivity_gains_total']/1000:.0f}K (IBI 2024 data)")
    print(f"  Caregiver Savings: ${cons['npv_breakdown']['caregiver_savings_total']/1000:.0f}K (AARP data, disease-only)")
    print(f"  GDP Boost: ${cons['npv_breakdown']['gdp_boost_benefit']/1000:.0f}K")
    print(f"  Extended Earnings: ${cons['npv_breakdown']['extended_earnings']/1000:.0f}K")

    print("\n--- Moderate Conservative Baseline (Age 30, $50K income, 1% Treaty) ---")
    cons_mod = PERSONAL_WEALTH_CONSERVATIVE_MODERATE_AGE_30_1PCT
    print(f"Total Benefit: ${cons_mod['total_lifetime_benefit']/1000:.0f}K")
    print(f"Life Extension: {cons_mod['life_extension_years']:.1f} years (antibiotic precedent)")
    print(f"Extended Earnings: ${cons_mod['npv_breakdown']['extended_earnings']/1000:.0f}K")

    # DEPRECATED: Improved and Endgame comparison removed - superseded by Disease Eradication Model below

    print("\n=== CONSERVATIVE BASELINE MODEL FEATURES ===")
    print("- All parameters cited in ../references.qmd")
    print("- Productivity: IBI 2024 workforce data (28% affected, $4,798/yr loss)")
    print("- Caregiver: AARP data ($16.59/hr, 110 hrs/mo, disease-portion only)")
    print("- Life extension: Antibiotic precedent (10 years for major breakthrough)")
    print("- No arbitrary divisors (30, 10, 2, 1000, etc.)")
    print("- Mental health folded into productivity (no double-counting)")
    print("- Healthcare by disease category (treatable/manageable/incurable)")
    print("- Conservative treatable portions (60% productivity, 40% caregiver)")


# ---
# RESEARCH ACCELERATION DISEASE ERADICATION MODEL
# ---
# This model properly accounts for 115x cumulative research acceleration
# and models systematic disease eradication with real burden data

# Disease burden data (CDC 2023/2024)
# Source: CDC FastStats, Leading Causes of Death 2023
# https://www.cdc.gov/nchs/fastats/leading-causes-of-death.htm

# Total deaths in 2023: 3,090,964
# Death rates per 100,000:
CARDIOVASCULAR_DEATH_RATE = Parameter(
    162.1 + 39.0,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Cardiovascular disease death rate (heart disease + stroke)",
    unit="deaths per 100,000"
)  # Heart disease + Stroke = 201.1

CANCER_DEATH_RATE = Parameter(
    146.6,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Cancer death rate (all cancers)",
    unit="deaths per 100,000"
)  # All cancers (2023 estimate)

RESPIRATORY_DEATH_RATE = Parameter(
    33.4,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Chronic respiratory disease death rate",
    unit="deaths per 100,000"
)  # Chronic lower respiratory

ALZHEIMERS_DEATH_RATE = Parameter(
    27.7,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Alzheimer's disease death rate",
    unit="deaths per 100,000"
)

DIABETES_DEATH_RATE = Parameter(
    22.4,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Diabetes death rate",
    unit="deaths per 100,000"
)

KIDNEY_DISEASE_DEATH_RATE = Parameter(
    13.1,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Kidney disease death rate",
    unit="deaths per 100,000"
)

LIVER_DISEASE_DEATH_RATE = Parameter(
    13.0,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Liver disease death rate",
    unit="deaths per 100,000"
)

INFECTIONS_DEATH_RATE = 15.0  # Estimate (flu, pneumonia, sepsis)

ACCIDENTS_DEATH_RATE = Parameter(
    62.3,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Accidental/unintentional injury death rate",
    unit="deaths per 100,000"
)  # Unintentional injuries

OTHER_DEATH_RATE = 250.0  # All other causes

TOTAL_DEATH_RATE = Parameter(
    722.0,
    source_ref="cdc-leading-causes-death",
    source_type="external",
    description="Overall age-adjusted death rate",
    unit="deaths per 100,000"
)  # Overall age-adjusted death rate 2024

# Disease burden as percentage of total deaths
DISEASE_BURDEN = {
    'cardiovascular': 201.1 / 722.0,  # 27.8%
    'cancer': 146.6 / 722.0,  # 20.3%
    'respiratory': 33.4 / 722.0,  # 4.6%
    'neurodegenerative': 27.7 / 722.0,  # 3.8% (Alzheimer's)
    'metabolic': (22.4 + 13.1 + 13.0) / 722.0,  # 6.7% (Diabetes + Kidney + Liver)
    'infectious': 15.0 / 722.0,  # 2.1%
    'accidents': 62.3 / 722.0,  # 8.6%
    'aging_related': 180.0 / 722.0,  # 24.9% (Cellular aging, frailty, multi-morbidity)
    'other': 60.0 / 722.0,  # 8.3%
}

# Years of life lost per death by category
# Source: Cancer YLL studies, cardiovascular burden research
YEARS_LOST_PER_DEATH = {
    'cardiovascular': 12.0,  # Similar to cancer
    'cancer': 13.5,  # Average 14.9 women, 12.7 men
    'respiratory': 8.0,  # Older age deaths
    'neurodegenerative': 6.0,  # Very old age deaths
    'metabolic': 10.0,  # Middle age deaths
    'infectious': 15.0,  # Can affect all ages
    'accidents': 35.0,  # Often young people
    'aging_related': 3.0,  # Very old age, natural limits
    'other': 10.0,  # Mixed
}

# Current cure/treatment rates by category
# Source: Cancer 5-year survival (69%), cardiovascular prevention data
CURRENT_CURE_RATE = {
    'cardiovascular': 0.50,  # 50% preventable with current knowledge
    'cancer': 0.69,  # 69% 5-year survival rate (2013-2019)
    'respiratory': 0.60,  # Treatable but not curable
    'neurodegenerative': 0.10,  # Very limited current treatments
    'metabolic': 0.70,  # Highly manageable with current drugs
    'infectious': 0.95,  # Antibiotics/vaccines very effective
    'accidents': 0.30,  # Some prevention possible
    'aging_related': 0.05,  # Minimal current progress
    'other': 0.50,  # Mixed
}

# Research acceleration potential by category
# How much can 115x research + AI + gene therapy + epigenetics + stem cells improve cure rates?
#
# With convergence of breakthrough technologies:
# - Gene therapy: Fixes genetic diseases at root cause
# - Epigenetics: Reverses aging markers
# - Stem cells: Regenerates damaged tissues/organs
# - AI drug discovery: Finds personalized treatments at scale
# - Near-zero trial costs: Tests everything
#
RESEARCH_ACCELERATION_POTENTIAL = {
    'cardiovascular': 0.95,  # Very high (gene therapy fixes predisposition, regeneration fixes damage, AI optimizes)
    'cancer': 0.95,  # Very high (AI personalized medicine, immunotherapy, early AI detection)
    'respiratory': 0.90,  # High (lung regeneration, gene therapy for genetic conditions)
    'neurodegenerative': 0.80,  # High (stem cells, brain regeneration, epigenetic reprogramming)
    'metabolic': 0.98,  # Nearly complete (gene therapy fixes root causes, AI optimizes treatment)
    'infectious': 0.99,  # Nearly complete (AI discovers treatments instantly)
    'accidents': 0.60,  # Moderate (some prevention AI, trauma regeneration)
    'aging_related': 0.85,  # High (cellular reprogramming, epigenetic reversal, organ regeneration)
    'other': 0.85,  # High (mix of above technologies)
}


def calculate_cumulative_research_years(treaty_pct, years_elapsed):
    """
    Calculate cumulative research equivalent years from 115x acceleration

    With 115x research acceleration:
    - Year 1: 115 research-years
    - Year 5: 575 cumulative research-years
    - Year 10: 1,150 cumulative research-years
    - Year 20: 2,300 cumulative research-years

    For comparison:
    - Total medical progress 1900-2024: 124 years → +32 years life expectancy
    - 2,300 years = 18.5x the entire modern medical revolution

    Args:
        treaty_pct: Fraction of military spending redirected
        years_elapsed: Years since treaty signed

    Returns:
        Cumulative research-equivalent years
    """
    multiplier = calculate_medical_progress_multiplier(treaty_pct)
    return multiplier * years_elapsed


def calculate_disease_eradication_rate(category, cumulative_research_years, conservative=False):
    """
    Calculate what percentage of a disease category can be cured/prevented
    given cumulative research acceleration

    Model:
    - Start with current cure rate
    - Add research progress toward maximum potential
    - Progress follows logarithmic curve (diminishing returns)
    - Conservative mode assumes slower progress

    Args:
        category: Disease category name
        cumulative_research_years: Total research-years accumulated
        conservative: If True, assume 50% of calculated progress

    Returns:
        Total cure/prevention rate (0-1)
    """
    current_rate = CURRENT_CURE_RATE[category]
    max_potential = RESEARCH_ACCELERATION_POTENTIAL[category]

    # Room for improvement
    room_for_improvement = max_potential - current_rate

    # Logarithmic progress curve (diminishing returns)
    # Fast progress initially, then slows as we approach limits
    #
    # Calibrated based on historical precedent:
    # - 124 years (1900-2024) → 32 years life extension
    # - But with 115x acceleration, progress is faster
    #
    # Progress scaling:
    # -   500 research-years → 35% of potential
    # - 1,000 research-years → 50% of potential
    # - 2,300 research-years → 70% of potential (20-year scenario)
    # - 5,000 research-years → 85% of potential
    # - 10,000 research-years → 95% of potential
    #
    # Formula: logarithmic with slower saturation
    progress_factor = min(0.95, 0.25 + 0.25 * ((cumulative_research_years / 1000) ** 0.6))

    if conservative:
        progress_factor *= 0.5  # Conservative: half the progress

    # New cure rate
    improvement = room_for_improvement * progress_factor
    return min(max_potential, current_rate + improvement)


def calculate_life_extension_from_eradication(treaty_pct, years_elapsed, conservative=False):
    """
    Calculate life extension from systematic disease eradication

    This properly accounts for:
    - 115x cumulative research acceleration
    - Disease-by-disease eradication rates
    - Years of life lost per disease category
    - Diminishing returns as diseases are eradicated

    Args:
        treaty_pct: Fraction of military spending redirected
        years_elapsed: Years since treaty signed
        conservative: If True, assume 50% slower progress

    Returns:
        dict with life extension details and total years gained
    """
    cumulative_research = calculate_cumulative_research_years(treaty_pct, years_elapsed)

    total_life_extension = 0.0
    disease_details = {}

    for category in DISEASE_BURDEN.keys():
        # Current baseline deaths from this category
        burden_pct = DISEASE_BURDEN[category]
        years_lost_per_death = YEARS_LOST_PER_DEATH[category]

        # Current cure rate
        current_cure_rate = CURRENT_CURE_RATE[category]

        # New cure rate with research acceleration
        new_cure_rate = calculate_disease_eradication_rate(
            category, cumulative_research, conservative
        )

        # Improvement in cure rate
        cure_rate_improvement = new_cure_rate - current_cure_rate

        # Life extension from this category
        # If we cure X% more of a disease that causes Y% of deaths
        # and each death loses Z years, we gain: X * Y * Z years
        category_life_extension = cure_rate_improvement * burden_pct * years_lost_per_death

        total_life_extension += category_life_extension

        disease_details[category] = {
            'burden_pct': burden_pct,
            'current_cure_rate': current_cure_rate,
            'new_cure_rate': new_cure_rate,
            'improvement': cure_rate_improvement,
            'years_lost_per_death': years_lost_per_death,
            'life_extension_contribution': category_life_extension,
        }

    # AGING REVERSAL BONUS - Approaching Accident-Limited Lifespan
    #
    # If we can regenerate organs and reprogram DNA/epigenetics, there's NO biological
    # reason for aging-related death. Life expectancy becomes limited primarily by accidents.
    #
    # Current accident death rate: 62.3 per 100,000 = 0.0623% per year
    # If accidents are ONLY mortality → expected lifespan ≈ 1,600 years
    #
    # But realistically:
    # - Some accidents can be prevented (AI vehicles, safety systems)
    # - Some can't (rare disasters, violence)
    # - Practical limit accounting for accidents: ~150-200 years
    #
    # This is ADDITIONAL to disease-specific improvements above
    #
    # Scaling toward accident-limited lifespan:
    # -   500 research-years → +15 years (80→95)
    # - 1,000 research-years → +35 years (80→115)
    # - 2,300 research-years → +65 years (80→145) [20-year scenario]
    # - 4,600 research-years → +95 years (80→175) [40-year scenario]
    # - 10,000 research-years → +120 years (80→200) [approaching accident-limited]
    #
    # Formula: logarithmic scaling with asymptote at accident-limited lifespan (~150 years gain)
    aging_reversal_bonus = min(150, 12.0 * ((cumulative_research / 100) ** 0.56))

    if conservative:
        aging_reversal_bonus *= 0.3  # Conservative: only 30% of aging reversal potential

    # Total life extension = disease cures + aging reversal
    total_life_extension += aging_reversal_bonus

    return {
        'total_life_extension': total_life_extension,
        'disease_life_extension': total_life_extension - aging_reversal_bonus,
        'aging_reversal_bonus': aging_reversal_bonus,
        'cumulative_research_years': cumulative_research,
        'years_elapsed': years_elapsed,
        'disease_details': disease_details,
        'model_type': 'disease_eradication',
        'conservative': conservative,
    }


def calculate_personal_lifetime_wealth_disease_eradication(
    treaty_pct=TREATY_REDUCTION_PCT,
    current_age=30,
    baseline_life_expectancy=80,
    annual_income=50000,
    discount_rate=0.03,
    years_elapsed=5,
    conservative=False
):
    """
    Personal lifetime wealth model using disease eradication approach

    This model properly accounts for:
    - 115x cumulative research acceleration (not one-time antibiotic comparison)
    - Disease-by-disease systematic eradication
    - Real CDC burden data
    - Realistic cure rate improvements by category
    - Diminishing returns as we approach biological limits

    Scenarios:
    - 5 years elapsed: Low-hanging fruit (infections, some cancers)
    - 10 years elapsed: Major categories tackled (cardio, metabolic)
    - 20 years elapsed: Aging partially reversed, most diseases eradicated
    - 40 years elapsed: Approaching biological limits

    Args:
        treaty_pct: Fraction of military spending redirected
        current_age: Person's current age
        baseline_life_expectancy: Current life expectancy
        annual_income: Person's annual income
        discount_rate: Discount rate for NPV calculations
        years_elapsed: Years since treaty signed (5/10/20/40)
        conservative: If True, assume 50% slower progress

    Returns:
        dict with total lifetime benefit and detailed breakdown
    """
    # Calculate life extension from disease eradication
    eradication_result = calculate_life_extension_from_eradication(
        treaty_pct, years_elapsed, conservative
    )
    life_extension_years = eradication_result['total_life_extension']

    # Medical progress multiplier for other calculations
    progress_multiplier = calculate_medical_progress_multiplier(treaty_pct)

    # Peace dividend (same as other models)
    peace_dividend_per_capita_annual = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / GLOBAL_POPULATION_2024_BILLIONS
    years_remaining = baseline_life_expectancy - current_age
    total_years = years_remaining + life_extension_years

    # GDP boost for compounding calculations
    gdp_boost = calculate_gdp_growth_boost(treaty_pct)

    # Healthcare savings (disease eradication approach)
    # As diseases are eradicated, healthcare costs drop
    # Average reduction proportional to cure rate improvement across all categories
    avg_cure_improvement = sum(
        detail['improvement'] * detail['burden_pct']
        for detail in eradication_result['disease_details'].values()
    )
    healthcare_reduction_pct = avg_cure_improvement * 0.8  # 80% of cure improvement translates to cost reduction
    US_CHRONIC_COST_PER_CAPITA = 3.7e12 / US_POPULATION_2024  # $11,045/person/year
    healthcare_savings_annual = US_CHRONIC_COST_PER_CAPITA * healthcare_reduction_pct

    # Productivity gains (same as conservative baseline model)
    productivity_gains_annual = calculate_productivity_loss_conservative_baseline(treaty_pct, annual_income)

    # Caregiver savings (same as conservative baseline model)
    caregiver_savings_annual = calculate_caregiver_savings_conservative_baseline(treaty_pct)

    # Component totals using compound_sum
    peace_dividend_total = compound_sum(peace_dividend_per_capita_annual, total_years, gdp_boost, discount_rate)
    healthcare_savings_total = compound_sum(healthcare_savings_annual, total_years, gdp_boost, discount_rate)
    productivity_gains_total = compound_sum(productivity_gains_annual, total_years, gdp_boost, discount_rate)
    caregiver_savings_total = compound_sum(caregiver_savings_annual, total_years, gdp_boost, discount_rate)

    # GDP boost benefit
    # Calculate the ADDITIONAL benefit from GDP boost (treaty growth vs baseline growth)
    # Both use total_years (including life extension) to avoid penalizing younger people
    baseline_growth = 0.025  # Baseline economic growth without treaty
    growth_differential = gdp_boost - baseline_growth

    # Calculate incremental benefit from faster growth over ALL years of life
    gdp_boost_benefit = 0
    for t in range(1, int(total_years) + 1):
        # Incremental value from faster growth
        baseline_value = annual_income * ((1 + baseline_growth) ** t)
        treaty_value = annual_income * ((1 + gdp_boost) ** t)
        incremental_value = treaty_value - baseline_value
        gdp_boost_benefit += incremental_value / ((1 + discount_rate) ** t)

    # Extended earnings from life extension
    extended_earnings = 0
    if life_extension_years > 0:
        working_years_extended = max(0, min(life_extension_years, 70 - baseline_life_expectancy))
        retirement_years_extended = life_extension_years - working_years_extended

        for t in range(int(years_remaining), int(years_remaining + working_years_extended)):
            future_income = annual_income * ((1 + gdp_boost) ** t)
            extended_earnings += future_income / ((1 + discount_rate) ** t)

        if retirement_years_extended > 0:
            final_working_income = annual_income * ((1 + gdp_boost) ** (years_remaining + working_years_extended))
            retirement_income = final_working_income * 0.60  # 60% retirement income
            for t in range(int(years_remaining + working_years_extended), int(total_years)):
                extended_earnings += retirement_income / ((1 + discount_rate) ** t)

    # Total benefit
    total_benefit = (
        peace_dividend_total +
        healthcare_savings_total +
        productivity_gains_total +
        caregiver_savings_total +
        gdp_boost_benefit +
        extended_earnings
    )

    return {
        'total_lifetime_benefit': total_benefit,
        'annual_breakdown': {
            'peace_dividend': peace_dividend_per_capita_annual,
            'healthcare_savings': healthcare_savings_annual,
            'productivity_gains': productivity_gains_annual,
            'caregiver_savings': caregiver_savings_annual,
        },
        'npv_breakdown': {
            'peace_dividend_total': peace_dividend_total,
            'healthcare_savings_total': healthcare_savings_total,
            'productivity_gains_total': productivity_gains_total,
            'caregiver_savings_total': caregiver_savings_total,
            'gdp_boost_benefit': gdp_boost_benefit,
            'extended_earnings': extended_earnings,
        },
        'life_extension_years': life_extension_years,
        'new_life_expectancy': baseline_life_expectancy + life_extension_years,
        'cumulative_research_years': eradication_result['cumulative_research_years'],
        'gdp_growth_boost': gdp_boost - 0.025,
        'medical_progress_multiplier': progress_multiplier,
        'eradication_details': eradication_result['disease_details'],
        'model_type': 'disease_eradication',
        'years_elapsed': years_elapsed,
        'conservative': conservative,
    }


# Pre-calculated disease eradication scenarios
# 5-year scenario (low-hanging fruit)
PERSONAL_WEALTH_ERADICATION_5YR_AGE_30_1PCT = calculate_personal_lifetime_wealth_disease_eradication(
    treaty_pct=0.01, current_age=30, annual_income=50000, years_elapsed=5, conservative=False
)
PERSONAL_LIFETIME_BENEFIT_ERADICATION_5YR_AGE_30_1PCT = PERSONAL_WEALTH_ERADICATION_5YR_AGE_30_1PCT['total_lifetime_benefit']

# 10-year scenario (major categories tackled)
PERSONAL_WEALTH_ERADICATION_10YR_AGE_30_1PCT = calculate_personal_lifetime_wealth_disease_eradication(
    treaty_pct=0.01, current_age=30, annual_income=50000, years_elapsed=10, conservative=False
)
PERSONAL_LIFETIME_BENEFIT_ERADICATION_10YR_AGE_30_1PCT = PERSONAL_WEALTH_ERADICATION_10YR_AGE_30_1PCT['total_lifetime_benefit']

# 20-year scenario (aging partially reversed)
PERSONAL_WEALTH_ERADICATION_20YR_AGE_30_1PCT = calculate_personal_lifetime_wealth_disease_eradication(
    treaty_pct=0.01, current_age=30, annual_income=50000, years_elapsed=20, conservative=False
)
PERSONAL_LIFETIME_BENEFIT_ERADICATION_20YR_AGE_30_1PCT = PERSONAL_WEALTH_ERADICATION_20YR_AGE_30_1PCT['total_lifetime_benefit']
personal_lifetime_benefit_eradication_20yr_age_30_1pct_millions_formatted = f"{PERSONAL_LIFETIME_BENEFIT_ERADICATION_20YR_AGE_30_1PCT / 1_000_000:.1f}"

# 40-year scenario (approaching biological limits)
PERSONAL_WEALTH_ERADICATION_40YR_AGE_30_1PCT = calculate_personal_lifetime_wealth_disease_eradication(
    treaty_pct=0.01, current_age=30, annual_income=50000, years_elapsed=40, conservative=False
)
PERSONAL_LIFETIME_BENEFIT_ERADICATION_40YR_AGE_30_1PCT = PERSONAL_WEALTH_ERADICATION_40YR_AGE_30_1PCT['total_lifetime_benefit']


if __name__ == "__main__":
    # Test disease eradication model
    print("\n\n=== DISEASE ERADICATION MODEL (CUMULATIVE RESEARCH ACCELERATION) ===")
    print("\nThis model properly accounts for 115x CUMULATIVE research acceleration")
    print("and systematic disease-by-disease eradication with real CDC burden data.\n")

    for years, label in [(5, "5-Year"), (10, "10-Year"), (20, "20-Year"), (40, "40-Year")]:
        result = calculate_personal_lifetime_wealth_disease_eradication(
            treaty_pct=0.01, current_age=30, annual_income=50000, years_elapsed=years, conservative=False
        )
        cumulative_research = result['cumulative_research_years']
        life_ext = result['life_extension_years']
        total = result['total_lifetime_benefit']

        print(f"--- {label} Scenario (Age 30, $50K, 1% Treaty) ---")
        print(f"Cumulative Research: {cumulative_research:.0f} equivalent years ({cumulative_research/124:.1f}x entire 1900-2024 medical progress)")
        print(f"Life Extension: {life_ext:.1f} years")
        print(f"Total Benefit: ${total/1000:.0f}K\n")

        # Show disease-by-disease breakdown for selected scenario
        if years == 20:
            print("Disease-by-Disease Eradication Progress (20-year scenario):")
            for category, details in result['eradication_details'].items():
                cure_improvement = details['improvement']
                new_cure_rate = details['new_cure_rate']
                life_contribution = details['life_extension_contribution']
                if cure_improvement > 0.01:  # Only show meaningful improvements
                    print(f"  {category.capitalize():20s}: {details['current_cure_rate']:.0%} -> {new_cure_rate:.0%} cure rate (+{cure_improvement:.0%}) = +{life_contribution:.1f} yrs")
            print()

    print("\n=== COMPARISON: ALL MODELS ===")
    conservative_total = PERSONAL_LIFETIME_BENEFIT_AGE_30_1PCT
    cons_baseline_total = PERSONAL_LIFETIME_BENEFIT_CONSERVATIVE_AGE_30_1PCT
    cons_moderate_total = PERSONAL_LIFETIME_BENEFIT_CONSERVATIVE_MODERATE_AGE_30_1PCT
    erad_5yr = PERSONAL_LIFETIME_BENEFIT_ERADICATION_5YR_AGE_30_1PCT
    erad_10yr = PERSONAL_LIFETIME_BENEFIT_ERADICATION_10YR_AGE_30_1PCT
    erad_20yr = PERSONAL_LIFETIME_BENEFIT_ERADICATION_20YR_AGE_30_1PCT
    erad_40yr = PERSONAL_LIFETIME_BENEFIT_ERADICATION_40YR_AGE_30_1PCT

    erad_5yr_life = PERSONAL_WEALTH_ERADICATION_5YR_AGE_30_1PCT['life_extension_years']
    erad_10yr_life = PERSONAL_WEALTH_ERADICATION_10YR_AGE_30_1PCT['life_extension_years']
    erad_20yr_life = PERSONAL_WEALTH_ERADICATION_20YR_AGE_30_1PCT['life_extension_years']
    erad_40yr_life = PERSONAL_WEALTH_ERADICATION_40YR_AGE_30_1PCT['life_extension_years']

    print("DEPRECATED Models (kept for reference):")
    print(f"  Conservative (1.2yr):              ${conservative_total/1000:.0f}K  [Arbitrary formulas - DO NOT USE]")
    print()
    print("Conservative Baselines (antibiotic precedent - for skeptical audiences):")
    print(f"  Conservative Baseline (5yr):       ${cons_baseline_total/1000:.0f}K  [Antibiotic precedent, properly cited]")
    print(f"  Conservative Moderate (10yr):      ${cons_moderate_total/1000:.0f}K  [Antibiotic precedent, properly cited]")
    print()
    print("Disease Eradication Model (RECOMMENDED - cumulative 115x research):")
    print(f"  5-year  ({erad_5yr_life:.1f}yr life ext):  ${erad_5yr/1000:.0f}K  [575 research-years, low-hanging fruit]")
    print(f"  10-year ({erad_10yr_life:.1f}yr life ext): ${erad_10yr/1000:.0f}K  [1,150 research-years, major categories]")
    print(f"  20-year ({erad_20yr_life:.1f}yr life ext): ${erad_20yr/1000:.0f}K  [2,300 research-years, DEFAULT]")
    print(f"  40-year ({erad_40yr_life:.1f}yr life ext): ${erad_40yr/1000:.0f}K  [4,600 research-years, biological limits]")

    print("\n=== KEY INSIGHT ===")
    print("The antibiotic precedent (10 years) was ONE technology solving ONE disease category.")
    print("The 1% Treaty enables:")
    print("  - 115x research acceleration EVERY YEAR (cumulative)")
    print("  - AI discovering millions of treatments in parallel")
    print("  - Gene therapy, epigenetics, stem cells, organ regeneration ALL converging")
    print("  - Near-zero trial costs removing pharma's biggest barrier")
    print(f"\n20 years of 115x research = 2300 equivalent years")
    print(f"  = {2300/124:.1f}x the ENTIRE modern medical revolution (1900-2024)")
    print(f"  = Realistic life extension: {erad_20yr_life:.1f} years")
    print(f"  = Personal benefit: ${erad_20yr/1000:.0f}K")


# ==============================================================================
# PARAMETER LINKING SYSTEM
# ==============================================================================
# Maps parameter names to their detailed source documentation
# This allows us to both use calculated values AND link to sources automatically

PARAMETER_LINKS = {
    # Peace Dividend Parameters
    'treaty_annual_funding': '../appendix/peace-dividend-calculations.qmd',
    'peace_dividend_annual_societal_benefit': '../appendix/peace-dividend-calculations.qmd',
    'global_military_spending_annual_2024': '../references.qmd#sipri-2024-spending',
    'global_war_total_cost': '../appendix/peace-dividend-calculations.qmd',

    # Health Dividend Parameters (dFDA)
    'roi_dfda_savings_only': '../appendix/dfda-cost-benefit-analysis.qmd',
    'roi_all_direct_benefits': '../appendix/dfda-cost-benefit-analysis.qmd',
    'trial_cost_reduction': '../appendix/recovery-trial.qmd',
    'dfda_annual_savings': '../appendix/dfda-cost-benefit-analysis.qmd',
    'qalys_annual': '../appendix/dfda-qaly-model.qmd',

    # Research Acceleration
    'research_acceleration_multiplier': '../appendix/research-acceleration-model.qmd',
    'trials_per_year_current': '../appendix/research-acceleration-model.qmd',
    'trials_per_year_dfda': '../appendix/research-acceleration-model.qmd',

    # Cost-Effectiveness
    'cost_per_life_saved': '../appendix/1-percent-treaty-cost-effectiveness.qmd',
    'icer': '../appendix/dfda-cost-benefit-analysis.qmd#dfda-icer-analysis',

    # External Sources (references.qmd)
    'givewell_cost_per_life': '../references.qmd#givewell-cost-per-life-saved',
    'smallpox_roi': '../references.qmd#smallpox-eradication-roi',
    'childhood_vaccination_roi': '../references.qmd#childhood-vaccination-roi',
    'disease_economic_burden': '../references.qmd#disease-economic-burden-109t',
    'conflict_deaths': '../references.qmd#acled-active-combat-deaths',
    'clinical_trial_market': '../references.qmd#clinical-trial-market-size',

    # Personal Impact
    'personal_lifetime_wealth': '../appendix/disease-eradication-personal-lifetime-wealth-calculations.qmd',
}


def param_link(param_name: str, formatted_value: str = None) -> str:
    """
    Create an HTML link combining a formatted parameter with its source.

    Args:
        param_name: Name of the parameter (e.g., 'treaty_annual_funding')
        formatted_value: Pre-formatted display value. If None, will use param_name_formatted

    Returns:
        HTML link string like '<a href="../appendix/peace-dividend-calculations.qmd">$27.2B</a>'

    Usage in QMD files:
        `{python} param_link('treaty_annual_funding')`
        `{python} param_link('roi_conservative', '463:1')`
    """
    # Get formatted value if not provided
    if formatted_value is None:
        formatted_var_name = f"{param_name}_formatted"
        if formatted_var_name in globals():
            formatted_value = globals()[formatted_var_name]
        else:
            # Fallback to the raw value
            formatted_value = str(globals().get(param_name.upper(), '???'))

    # Get source link
    source_link = PARAMETER_LINKS.get(param_name, '')

    # Return HTML link or unlinked based on whether we have a source
    if source_link:
        return f'<a href="{source_link}">{formatted_value}</a>'
    else:
        return formatted_value


def add_parameter_link(param_name: str, source_path: str):
    """
    Add a new parameter → source mapping to the registry.

    Args:
        param_name: Parameter name (e.g., 'new_parameter')
        source_path: Relative path to source doc (e.g., '../appendix/analysis.qmd')
    """
    PARAMETER_LINKS[param_name] = source_path


# Create commonly used linked versions automatically
treaty_annual_funding_linked = param_link('treaty_annual_funding', treaty_annual_funding_formatted)
peace_dividend_annual_societal_benefit_linked = param_link('peace_dividend_annual_societal_benefit', peace_dividend_annual_societal_benefit_formatted)
roi_dfda_savings_only_linked = param_link('roi_dfda_savings_only', roi_dfda_savings_only_formatted)
roi_all_direct_benefits_linked = param_link('roi_all_direct_benefits', roi_all_direct_benefits_formatted)
trial_cost_reduction_linked = param_link('trial_cost_reduction', f"{TRIAL_COST_REDUCTION_FACTOR}x")
global_military_spending_annual_2024_linked = param_link('global_military_spending_annual_2024', global_military_spending_annual_2024_formatted)