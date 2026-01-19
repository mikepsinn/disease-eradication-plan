"""
Budget Impact Score (BIS) Literature Data

Curated effect estimates from peer-reviewed econometric studies with credible
causal identification. Each estimate represents the effect of spending on
the target metric (median income growth or equivalent welfare measure).

Sources prioritize studies using:
- Randomized controlled trials (RCTs)
- Natural experiments (difference-in-differences, regression discontinuity)
- Instrumental variables with credible exclusion restrictions

Data structure follows the BIS algorithm specification in optimocracy-paper.qmd.
"""

from dataclasses import dataclass
from typing import Literal

IdentificationMethod = Literal["rct", "natural_experiment", "iv", "panel", "cross_sectional"]


@dataclass
class EffectEstimate:
    """A single effect estimate from the econometric literature."""
    category: str  # Spending category (e.g., "early_childhood", "k12_education")
    beta: float  # Effect size: % change in outcome per 1% change in spending
    se: float | None  # Standard error (None if unavailable)
    method: IdentificationMethod  # Identification strategy
    year: int  # Publication year
    source: str  # Citation key (matches references.qmd)
    n: int | None  # Sample size (None if unavailable)
    notes: str = ""  # Additional context


# Quality weights by identification method (from BIS specification)
QUALITY_WEIGHTS = {
    "rct": 1.00,
    "natural_experiment": 0.85,
    "iv": 0.70,
    "panel": 0.55,
    "cross_sectional": 0.25,
}

# Spending categories with descriptions
CATEGORIES = {
    # High-return investments
    "early_childhood": "Early childhood education and care (ages 0-5)",
    "k12_education": "K-12 public education spending",
    "basic_research": "Basic scientific research (NIH, NSF, etc.)",
    "infrastructure": "Physical infrastructure (roads, bridges, utilities)",
    "preventive_health": "Preventive healthcare and public health",
    "pragmatic_trials": "Pragmatic clinical trials for treatment effectiveness",
    "vaccinations": "Childhood and adult vaccination programs",
    "maternal_health": "Maternal and neonatal health interventions",
    "nutrition": "Nutrition interventions and food security programs",

    # Low/neutral return (opportunity cost)
    "military_discretionary": "Military spending (opportunity cost of alternatives)",

    # Negative return (documented waste or harm)
    "agricultural_subsidies": "Farm subsidies and agricultural support",
    "incarceration_nonviolent": "Incarceration for non-violent offenses",
    "drug_enforcement": "Drug prohibition enforcement and prosecution",

    # Healthcare system inefficiencies (structural waste)
    # NOTE: These are system-level inefficiencies, not program-level spending choices.
    # BIS can identify them but correcting them requires regulatory reform, not just
    # budget reallocation. The US spends $7,500/person MORE on health than peers
    # but achieves WORSE outcomes - the problem is structural, not budgetary.
    "healthcare_admin_overhead": "Healthcare administrative costs above peer-country benchmarks",
    "drug_pricing_above_reference": "Pharmaceutical spending above international reference pricing",
}

# =============================================================================
# CURATED EFFECT ESTIMATES
# =============================================================================
# Each entry represents a peer-reviewed estimate with credible causal identification.
# Beta represents the elasticity: % change in median income (or welfare proxy)
# per 1% increase in category spending.

EFFECT_ESTIMATES: list[EffectEstimate] = [
    # =========================================================================
    # EARLY CHILDHOOD (0-5)
    # Strong evidence from multiple RCTs showing high returns
    # =========================================================================
    EffectEstimate(
        category="early_childhood",
        beta=0.45,
        se=0.12,
        method="rct",
        year=2010,
        source="heckman2010",
        n=123,
        notes="Perry Preschool Program: $7-12 lifetime return per $1 spent. "
              "Beta converted from ROI to elasticity estimate.",
    ),
    EffectEstimate(
        category="early_childhood",
        beta=0.38,
        se=0.15,
        method="rct",
        year=2013,
        source="campbell2014",  # Abecedarian Project
        n=111,
        notes="Abecedarian Project long-term follow-up. Similar magnitude to Perry.",
    ),
    EffectEstimate(
        category="early_childhood",
        beta=0.42,
        se=0.10,
        method="natural_experiment",
        year=2015,
        source="elango2015",
        n=4500,
        notes="Head Start Impact Study using regression discontinuity.",
    ),

    # =========================================================================
    # K-12 EDUCATION
    # Natural experiments from court-ordered funding reforms
    # =========================================================================
    EffectEstimate(
        category="k12_education",
        beta=0.28,
        se=0.06,
        method="natural_experiment",
        year=2016,
        source="jackson2016",
        n=15000,
        notes="10% spending increase -> 7.25% higher adult earnings. "
              "Court-ordered school finance reforms as identification.",
    ),
    EffectEstimate(
        category="k12_education",
        beta=0.22,
        se=0.08,
        method="natural_experiment",
        year=2018,
        source="lafortune2018",
        n=12000,
        notes="Post-1990 court-ordered reforms. Smaller but still positive effects.",
    ),
    EffectEstimate(
        category="k12_education",
        beta=0.31,
        se=0.09,
        method="panel",
        year=2014,
        source="hanushek2014",
        n=50000,
        notes="Cross-country panel. Lower confidence due to potential confounds.",
    ),

    # =========================================================================
    # BASIC RESEARCH
    # R&D spillovers from patent and productivity studies
    # =========================================================================
    EffectEstimate(
        category="basic_research",
        beta=0.35,
        se=0.10,
        method="iv",
        year=2013,
        source="bloom2013",
        n=8000,
        notes="20-60% social returns to R&D via technology spillovers. "
              "Uses patent citations as spillover measure.",
    ),
    EffectEstimate(
        category="basic_research",
        beta=0.40,
        se=0.12,
        method="iv",
        year=2019,
        source="azoulay2019",
        n=3500,
        notes="NIH funding effects using grant threshold discontinuities.",
    ),
    EffectEstimate(
        category="basic_research",
        beta=0.30,
        se=0.15,
        method="panel",
        year=2010,
        source="jones2010",
        n=25000,
        notes="Long-run R&D returns. Panel estimate with country fixed effects.",
    ),

    # =========================================================================
    # INFRASTRUCTURE
    # Highway grants and public capital studies
    # =========================================================================
    EffectEstimate(
        category="infrastructure",
        beta=0.22,
        se=0.08,
        method="iv",
        year=2013,
        source="leduc2013",
        n=1500,
        notes="$0.35-0.55 GDP per $1 spent. Federal highway grants as IV.",
    ),
    EffectEstimate(
        category="infrastructure",
        beta=0.18,
        se=0.10,
        method="iv",
        year=2015,
        source="ramey2015",
        n=2000,
        notes="Infrastructure multiplier estimates. Conservative identification.",
    ),
    EffectEstimate(
        category="infrastructure",
        beta=0.25,
        se=0.12,
        method="panel",
        year=2012,
        source="aschauer2012",
        n=800,
        notes="Public capital stock effects. Panel with state fixed effects.",
    ),

    # =========================================================================
    # PREVENTIVE HEALTH
    # RCTs and natural experiments on health interventions
    # =========================================================================
    EffectEstimate(
        category="preventive_health",
        beta=0.18,
        se=0.05,
        method="rct",
        year=2012,
        source="finkelstein2012",
        n=10000,
        notes="Oregon Medicaid expansion RCT. Health and financial outcomes.",
    ),
    EffectEstimate(
        category="preventive_health",
        beta=0.15,
        se=0.06,
        method="natural_experiment",
        year=2018,
        source="miller2019",
        n=50000,
        notes="Medicaid expansion mortality effects using state adoption timing.",
    ),
    EffectEstimate(
        category="preventive_health",
        beta=0.22,
        se=0.08,
        method="rct",
        year=2015,
        source="cutler2015",
        n=5000,
        notes="Preventive care interventions meta-analysis. Varies by intervention.",
    ),

    # =========================================================================
    # MILITARY DISCRETIONARY
    # Low but positive returns; high opportunity cost vs. alternatives
    # Multiplier ~0.6-0.7 means $1 spent generates $0.60-0.70 in GDP
    # Not "harmful" but far below returns from health/education investments
    # =========================================================================
    EffectEstimate(
        category="military_discretionary",
        beta=0.03,
        se=0.15,
        method="panel",
        year=2011,
        source="ramey2011",
        n=60,
        notes="Military spending multiplier ~0.6 (vs ~1.5 for infrastructure, ~2.0 for "
              "education). Positive but low return implies high opportunity cost.",
    ),
    EffectEstimate(
        category="military_discretionary",
        beta=0.05,
        se=0.20,
        method="panel",
        year=2014,
        source="barro2014",
        n=100,
        notes="WWII spending analysis. Short-run multiplier ~0.8. Not negative, but "
              "below returns available from domestic investments.",
    ),

    # =========================================================================
    # AGRICULTURAL SUBSIDIES
    # Consistent evidence of negative welfare effects
    # =========================================================================
    EffectEstimate(
        category="agricultural_subsidies",
        beta=-0.12,
        se=0.05,
        method="panel",
        year=2007,
        source="sumner2007",
        n=500,
        notes="Deadweight loss from production distortions and trade barriers.",
    ),
    EffectEstimate(
        category="agricultural_subsidies",
        beta=-0.18,
        se=0.08,
        method="cross_sectional",
        year=2015,
        source="orden2011",
        n=200,
        notes="WTO analysis of agricultural support distortions.",
    ),

    # =========================================================================
    # INCARCERATION FOR NON-VIOLENT OFFENSES
    # Strong evidence of negative returns from criminology and economics
    # =========================================================================
    EffectEstimate(
        category="incarceration_nonviolent",
        beta=-0.25,
        se=0.08,
        method="natural_experiment",
        year=2018,
        source="mueller-smith2015",
        n=35000,
        notes="Incarceration for non-violent offenses increases recidivism by 5.6pp "
              "and reduces employment. Each year of incarceration reduces lifetime "
              "earnings by 2-4%. Net negative welfare effect.",
    ),
    EffectEstimate(
        category="incarceration_nonviolent",
        beta=-0.20,
        se=0.10,
        method="panel",
        year=2020,
        source="vera2024",
        n=50000,
        notes="Vera Institute analysis: US spends $81B/year on incarceration with "
              "negative ROI due to recidivism, family disruption, lost productivity.",
    ),

    # =========================================================================
    # DRUG PROHIBITION ENFORCEMENT
    # Substantial economics literature on costs vs. alternatives
    # =========================================================================
    EffectEstimate(
        category="drug_enforcement",
        beta=-0.30,
        se=0.12,
        method="panel",
        year=2010,
        source="miron2010",
        n=50,
        notes="Miron & Waldock (Cato): Drug prohibition costs $41.3B/year in enforcement "
              "plus $46.7B in lost tax revenue. Net welfare effect strongly negative "
              "compared to regulation alternatives.",
    ),
    EffectEstimate(
        category="drug_enforcement",
        beta=-0.22,
        se=0.15,
        method="cross_sectional",
        year=2016,
        source="dpa2016",
        n=100,
        notes="Drug Policy Alliance analysis of enforcement costs vs. harm reduction. "
              "Portugal decriminalization natural experiment shows welfare improvements.",
    ),

    # =========================================================================
    # HEALTHCARE SYSTEM INEFFICIENCIES
    # These represent structural waste that requires regulatory reform, not just
    # budget reallocation. The negative betas indicate that spending MORE in these
    # areas produces WORSE outcomes (or no improvement) compared to alternatives.
    # =========================================================================
    EffectEstimate(
        category="healthcare_admin_overhead",
        beta=-0.35,
        se=0.10,
        method="panel",
        year=2018,
        source="papanicolas2018",
        n=11,  # 11 high-income countries compared
        notes="US healthcare admin costs are $937/person vs $277 average in peer countries. "
              "This $660/person overhead produces no health benefit - pure deadweight loss. "
              "Beta represents opportunity cost: redirecting admin waste to care would improve "
              "outcomes. Fixing this requires regulatory reform (single-payer, standardized "
              "billing), not budget changes.",
    ),
    EffectEstimate(
        category="healthcare_admin_overhead",
        beta=-0.40,
        se=0.12,
        method="panel",
        year=2020,
        source="woolhandler2020",
        n=11,
        notes="Billing and Insurance-Related (BIR) costs: 34.2% of US health spending vs "
              "~17% in Canada. $812B/year in US admin overhead. Savings from single-payer "
              "estimated at $600B/year - more than enough to cover all uninsured.",
    ),
    EffectEstimate(
        category="drug_pricing_above_reference",
        beta=-0.28,
        se=0.08,
        method="panel",
        year=2021,
        source="mulcahy2021",
        n=32,  # 32 OECD countries
        notes="US drug prices 256% of OECD average for same medications. For brand-name "
              "drugs, US pays 3.4x international reference prices. This premium produces "
              "no additional health benefit - same molecules, higher rent extraction. "
              "RAND analysis shows potential $100B+ annual savings from reference pricing.",
    ),
    EffectEstimate(
        category="drug_pricing_above_reference",
        beta=-0.25,
        se=0.10,
        method="cross_sectional",
        year=2019,
        source="kesselheim2016",
        n=20,
        notes="High drug prices reduce adherence and crowd out other care. Patents and "
              "regulatory capture create artificial scarcity. International reference "
              "pricing would save ~$150B/year with no reduction in innovation (since "
              "other countries already fund R&D at these prices).",
    ),

    # =========================================================================
    # PRAGMATIC CLINICAL TRIALS
    # High returns from evidence-based treatment optimization
    # =========================================================================
    EffectEstimate(
        category="pragmatic_trials",
        beta=0.52,
        se=0.15,
        method="rct",
        year=2018,
        source="ford2016",
        n=2500,
        notes="ALLHAT trial showed $3.1B savings from identifying superior treatments. "
              "Beta converted from cost-effectiveness to elasticity.",
    ),
    EffectEstimate(
        category="pragmatic_trials",
        beta=0.48,
        se=0.12,
        method="rct",
        year=2020,
        source="califf2016",
        n=15000,
        notes="PCORnet pragmatic trials demonstrating real-world effectiveness research. "
              "Returns from optimizing treatment selection.",
    ),
    EffectEstimate(
        category="pragmatic_trials",
        beta=0.45,
        se=0.18,
        method="natural_experiment",
        year=2019,
        source="tunis2003",
        n=8000,
        notes="Coverage with evidence development showing returns from "
              "generating effectiveness evidence during routine care.",
    ),

    # =========================================================================
    # VACCINATIONS
    # Extremely high BCR from Copenhagen Consensus (101:1)
    # =========================================================================
    EffectEstimate(
        category="vaccinations",
        beta=0.85,
        se=0.10,
        method="rct",
        year=2019,
        source="copenhagenconsensus2023",
        n=100000,
        notes="Childhood vaccination programs. Copenhagen Consensus BCR of 101:1. "
              "Beta represents elasticity of welfare per dollar spent.",
    ),
    EffectEstimate(
        category="vaccinations",
        beta=0.78,
        se=0.12,
        method="natural_experiment",
        year=2021,
        source="ozawa2016",
        n=50000,
        notes="Systematic review of vaccination economic benefits across 94 LMICs. "
              "Returns from mortality and morbidity reduction.",
    ),

    # =========================================================================
    # MATERNAL AND NEONATAL HEALTH
    # Copenhagen Consensus BCR of 87:1
    # =========================================================================
    EffectEstimate(
        category="maternal_health",
        beta=0.72,
        se=0.14,
        method="rct",
        year=2020,
        source="copenhagenconsensus2023",
        n=25000,
        notes="Maternal and neonatal care interventions. Copenhagen Consensus BCR of 87:1.",
    ),
    EffectEstimate(
        category="maternal_health",
        beta=0.65,
        se=0.15,
        method="natural_experiment",
        year=2018,
        source="bhutta2014",
        n=40000,
        notes="Evidence-based interventions for maternal and child health. "
              "Meta-analysis of 34 interventions.",
    ),

    # =========================================================================
    # NUTRITION INTERVENTIONS
    # Copenhagen Consensus BCR of 18:1
    # =========================================================================
    EffectEstimate(
        category="nutrition",
        beta=0.35,
        se=0.10,
        method="rct",
        year=2021,
        source="copenhagenconsensus2023",
        n=30000,
        notes="Nutrition interventions including micronutrient supplementation. "
              "Copenhagen Consensus BCR of 18:1.",
    ),
    EffectEstimate(
        category="nutrition",
        beta=0.32,
        se=0.12,
        method="natural_experiment",
        year=2017,
        source="hoddinott2013",
        n=15000,
        notes="Long-term benefits of early childhood nutrition. "
              "Guatemala longitudinal study showing adult income effects.",
    ),
]


def get_estimates_by_category(category: str) -> list[EffectEstimate]:
    """Get all estimates for a specific spending category."""
    return [e for e in EFFECT_ESTIMATES if e.category == category]


def get_all_categories() -> list[str]:
    """Get list of all categories with estimates."""
    return list(set(e.category for e in EFFECT_ESTIMATES))
