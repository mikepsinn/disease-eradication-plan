"""
Economic Parameters - Single Source of Truth
=============================================

This module contains all economic parameters used throughout the book.
All calculations should import from this module to ensure consistency.

Last updated: 2025-01-24
Version: 2.0.0

Usage:
    from economic_parameters import *
    print(f"Military spending: {format_parameter_value(GLOBAL_MILITARY_SPENDING_ANNUAL_2024)}")
    print(f"Peace dividend: {format_parameter_value(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT)}")
"""
from __future__ import annotations

import csv
import math
import warnings
from enum import Enum
from pathlib import Path
from typing import Optional, List, Tuple, Union, Callable, Any  # noqa: F401

# Import compute context type for type-safe compute lambdas
try:
    from .compute_context import ComputeContext
except ImportError:
    # Handle direct execution (not as package)
    from compute_context import ComputeContext

# Import valid reference IDs for type-safe citations
try:
    from .reference_ids import ReferenceID
except ImportError:
    # Handle direct execution (not as package)
    from reference_ids import ReferenceID

try:
    from .manual_ref_validation import normalize_manual_ref
except ImportError:
    # Handle direct execution (not as package)
    from manual_ref_validation import normalize_manual_ref


def _sum_excess_military_spending_above_1900_freeze(baseline_annual_usd: float) -> float:
    if baseline_annual_usd < 1_000_000_000:
        raise ValueError("baseline_annual_usd must be in dollars")
    data_path = (
        Path(__file__).resolve().parents[1]
        / "knowledge"
        / "data"
        / "global-military-spending-1900-2024-constant-2023-usd.csv"
    )
    with data_path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return sum(
            max(0.0, float(row["Spending_2023_USD_Billions"]) * 1_000_000_000 - baseline_annual_usd)
            for row in rows
        )


# ============================================================================
# PARAMETER CLASS - Adds source tracking to numeric values
# ============================================================================


class SourceType(str, Enum):
    """Valid source types for Parameter metadata.

    Attributes:
        EXTERNAL: Data from external sources (links to references.qmd)
        CALCULATED: Derived from formulas (links to calculation QMD)
        DEFINITION: Core definition/assumption (no external link)
    """
    EXTERNAL = "external"
    CALCULATED = "calculated"
    DEFINITION = "definition"


class DistributionType(str, Enum):
    """Probability distributions for Probabilistic Sensitivity Analysis (PSA).

    Attributes:
        NORMAL: Symmetric uncertainty (mean, sd). Good for large samples.
        LOGNORMAL: Right-skewed, strictly positive. Good for costs, relative risks.
        BETA: Bounded [0,1]. Good for probabilities, utilities.
        GAMMA: Right-skewed, strictly positive. Good for costs.
        TRIANGULAR: Defined by min, mode, max. Good when data is scarce.
        UNIFORM: Equal probability between min/max. Good for deep uncertainty.
        FIXED: No uncertainty (deterministic).
    """
    NORMAL = "normal"
    LOGNORMAL = "lognormal"
    BETA = "beta"
    GAMMA = "gamma"
    TRIANGULAR = "triangular"
    UNIFORM = "uniform"
    FIXED = "fixed"


class Parameter(float):
    r"""A numeric parameter that works in calculations but carries source metadata.

    Enables clickable links from numbers to their sources (external citations)
    or calculation methodologies (internal QMD pages). Enhanced with academic
    credibility indicators and economic validation for rigorous analysis.

    Args:
        value: The numeric value
        manual_ref: Root-relative QMD page where this parameter should link in the manual
        source_ref: Reference ID (for external sources) or QMD path (for calculations)
        source_type: SourceType enum - EXTERNAL, CALCULATED, or DEFINITION
        description: Human-readable description for tooltips
        unit: Unit of measurement (e.g., "USD", "deaths/year", "percentage")
        formula: Optional plain-text formula (e.g., "A + B + C") for tooltips
        latex: Optional LaTeX formula (e.g., r"\sum_{i=1}^{5} opex_i") for rendering
        confidence: Data quality level - "high", "medium", "low", or "estimated"
        last_updated: Date when source data was last updated (YYYY-MM-DD or YYYY-MM)
        peer_reviewed: Whether the source is from peer-reviewed literature
        conservative: Whether this is a conservative estimate (vs. optimistic)
        sensitivity: Optional uncertainty range (±value in same units)

        # NEW FIELDS (v2.0):
        display_value: Optional override for formatted display (e.g., "$2.7T" instead of auto-format)
        display_name: Optional override for parameter title in documentation (e.g., "Active Trials")
        chart_label: Optional concise label for generated chart axes and titles
        interval_label: Optional label describing an uncertainty interval
        keywords: List of search keywords for parameter discovery
        validation_min: Minimum valid value (hard constraint for validation)
        validation_max: Maximum valid value (hard constraint for validation)
        confidence_interval: Tuple of (lower, upper) for statistical confidence
        std_error: Standard error for statistical parameters
        distribution: DistributionType for Probabilistic Sensitivity Analysis

    Examples:
        # External data source with high confidence
        CONFLICT_DEATHS = Parameter(
            233600,
            manual_ref="knowledge/problem/cost-of-war.qmd",
            source_ref=ReferenceID.ACLED_ACTIVE_COMBAT_DEATHS,
            source_type=SourceType.EXTERNAL,
            description="Annual deaths from active combat",
            display_name="Annual Deaths from Active Combat",
            unit="deaths/year",
            confidence="high",
            last_updated="2024-01",
            peer_reviewed=True,
            keywords=["conflict", "deaths", "war", "combat", "casualties"]
        )

        # Calculated value with formula and validation
        TOTAL_OPEX = Parameter(
            PLATFORM + STAFF + INFRA + REGULATORY + COMMUNITY,
            manual_ref="knowledge/solution/dfda.qmd",
            source_type=SourceType.CALCULATED,
            description="Total annual operational costs",
            display_name="Total Annual Operational Costs",
            unit="USD/year",
            formula="PLATFORM + STAFF + INFRA + REGULATORY + COMMUNITY",
            latex=r"OPEX_{total} = \$15M \text{ (plat)} + \$10M \text{ (staff)} + \$8M \text{ (infra)} + \$5M \text{ (reg)} + \$2M \text{ (comm)} = \$40M",
            confidence="medium",
            conservative=True,
            sensitivity=0.01,
            validation_min=0,  # Cannot be negative
            keywords=["costs", "operations", "expenses", "budget"]
        )

        # Core definition with display override
        TREATY_PCT = Parameter(
            0.01,
            manual_ref="knowledge/solution/1-percent-treaty.qmd",
            source_type=SourceType.DEFINITION,
            description="1% treaty reduction target",
            display_name="1% Treaty Reduction Target",
            unit="percentage",
            display_value="1%",
            keywords=["treaty", "1%", "reduction", "target"]
        )

        # Statistical parameter with confidence interval
        GDP_MULTIPLIER = Parameter(
            2.7,
            manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
            source_ref="nber-wp-12345",
            source_type=SourceType.EXTERNAL,
            description="Healthcare investment GDP multiplier",
            display_name="Healthcare Investment GDP Multiplier",
            confidence_interval=(2.0, 3.5),
            std_error=0.3,
            keywords=["multiplier", "gdp", "healthcare", "economics"]
        )

    The Parameter class inherits from float, so it works in all math operations:
        total = CONFLICT_DEATHS * 2  # Works!
        ratio = NET_BENEFIT / CONFLICT_DEATHS  # Works!
    """

    __slots__ = (
        'manual_ref', 'source_ref', 'source_type', 'description', 'unit', 'formula', 'latex',
        'confidence', 'last_updated', 'peer_reviewed', 'conservative',
        'sensitivity', 'display_value', 'display_name', 'chart_label', 'interval_label', 'keywords',
        'validation_min', 'validation_max', 'confidence_interval', 'std_error',
        'distribution', 'inputs', 'compute', 'latex_symbol', 'hide_ci'
    )

    # Type annotations for Pylance/Pyright
    manual_ref: str
    source_ref: str
    source_type: "SourceType"
    description: str
    unit: str
    formula: str
    latex: str
    confidence: str
    last_updated: "str | None"
    peer_reviewed: bool
    conservative: bool
    sensitivity: "float | None"
    display_value: "str | None"
    display_name: "str | None"
    chart_label: "str | None"
    interval_label: "str | None"
    keywords: "list[str]"
    validation_min: "float | None"
    validation_max: "float | None"
    confidence_interval: "tuple[float, float] | None"
    std_error: "float | None"
    distribution: "DistributionType | None"
    inputs: "list[str]"
    compute: "Callable[[ComputeContext], float] | None"
    latex_symbol: "str | None"  # LaTeX symbol for this parameter in equations, e.g. "Cost_{trial}"
    hide_ci: bool  # Suppress confidence interval display in _variables.yml

    def __new__(
        cls,
        value: float,
        manual_ref: str = "",
        source_ref: str = "",
        source_type: Union[SourceType, str] = SourceType.EXTERNAL,
        description: str = "",
        unit: str = "",
        formula: str = "",
        latex: str = "",
        confidence: str = "high",
        last_updated: Optional[str] = None,
        peer_reviewed: bool = False,
        conservative: bool = False,
        sensitivity: Optional[float] = None,
        # NEW v2.0 parameters
        display_value: Optional[str] = None,
        display_name: Optional[str] = None,
        chart_label: Optional[str] = None,
        interval_label: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        validation_min: Optional[float] = None,
        validation_max: Optional[float] = None,
        confidence_interval: Optional[Tuple[float, float]] = None,
        std_error: Optional[float] = None,
        distribution: Union[DistributionType, str, None] = None,
        inputs: Optional[List[str]] = None,
        compute: Optional[Callable[[ComputeContext], float]] = None,
        latex_symbol: Optional[str] = None,  # LaTeX symbol for equations, e.g. "Cost_{trial}"
        hide_ci: bool = False,  # Suppress confidence interval display in _variables.yml
    ):
        # Convert string source_type to enum (backwards compatibility)
        if not isinstance(source_type, SourceType):
            source_type = SourceType(source_type)

        # Convert string distribution to enum
        if distribution is not None and not isinstance(distribution, DistributionType):
            distribution = DistributionType(distribution)

        # Validation: check bounds
        if validation_min is not None and value < validation_min:
            raise ValueError(
                f"Value {value} < validation_min {validation_min}. "
                f"Desc: {description or 'N/A'}"
            )
        if validation_max is not None and value > validation_max:
            raise ValueError(
                f"Value {value} > validation_max {validation_max}. "
                f"Desc: {description or 'N/A'}"
            )

        # Validation: confidence interval should contain value
        if confidence_interval is not None:
            lower, upper = confidence_interval
            if not (lower <= value <= upper):
                raise ValueError(
                    f"Value {value} outside interval [{lower}, {upper}]. "
                    f"Desc: {description or 'N/A'}"
                )

        # Validation: require unit to be specified (units are required for proper formatting)
        if not unit:
            raise ValueError(
                f"Parameter missing required 'unit': {description or 'unnamed'} (value={value}). "
                f"All parameters must specify unit='USD', 'years', 'deaths', 'ratio', 'multiplier', 'percentage', etc. "
                f"This ensures consistent formatting with auto-scaling (e.g., $27.2B, 8.2 years, 463:1)."
            )
        manual_ref = normalize_manual_ref(manual_ref, description, value)

        instance = super().__new__(cls, value)
        instance.manual_ref = manual_ref
        instance.source_ref = source_ref
        instance.source_type = source_type
        instance.description = description
        instance.unit = unit
        instance.formula = formula
        instance.latex = latex
        instance.confidence = confidence
        instance.last_updated = last_updated
        instance.peer_reviewed = peer_reviewed
        instance.conservative = conservative
        instance.sensitivity = sensitivity

        # NEW v2.0 attributes
        instance.display_value = display_value
        instance.display_name = display_name
        instance.chart_label = chart_label
        instance.interval_label = interval_label
        instance.keywords = keywords or []
        instance.validation_min = validation_min
        instance.validation_max = validation_max
        instance.confidence_interval = confidence_interval
        instance.std_error = std_error
        instance.distribution = distribution
        instance.inputs = inputs or []
        instance.compute = compute
        instance.latex_symbol = latex_symbol  # LaTeX symbol for equations, e.g. "Cost_{trial}"
        instance.hide_ci = hide_ci  # Suppress confidence interval display

        return instance

    def __repr__(self):
        return f"Parameter({float(self)}, source_ref='{self.source_ref}', confidence='{self.confidence}')"

    def __str__(self):
        """Return just the numeric value as a string for display purposes."""
        return str(float(self))

    def __format__(self, format_spec: str) -> str:
        """Format the numeric value according to format_spec for f-strings."""
        return format(float(self), format_spec)


# ---
# TIME CONSTANTS
# ---
# Base time unit constants for consistent calculations
DAYS_PER_YEAR = 365
HOURS_PER_DAY = 24
MONTHS_PER_YEAR = 12
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
HOURS_PER_YEAR = HOURS_PER_DAY * DAYS_PER_YEAR  # 8760
SECONDS_PER_YEAR = DAYS_PER_YEAR * HOURS_PER_DAY * MINUTES_PER_HOUR * SECONDS_PER_MINUTE  # 31,536,000


# ---
# PEACE DIVIDEND PARAMETERS
# ---

# Total cost of war (billions USD)
# Source: knowledge/problem/cost-of-war.qmd
# Reference: references.qmd#total-military-and-war-costs-11-4t

# Direct costs
GLOBAL_MILITARY_SPENDING_ANNUAL_2024 = Parameter(
    2_720_000_000_000,  # 3 sig figs
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GLOBAL_MILITARY_SPENDING,
    source_type="external",
    description="Global military spending in 2024",
    display_name="Global Military Spending in 2024",
    unit="USD",
    distribution="fixed",  # Using point estimate for clean presentation throughout book
    keywords=["2024", "2.7t", "dod", "pentagon", "national security", "army", "navy"],
    latex_symbol=r"Spending_{mil}",  # LaTeX symbol for equations
)  # SIPRI 2024 (rounded to 3 sig figs for clarity)

# Military spending trend data (SIPRI)
GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR = Parameter(
    0.034,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_ref=ReferenceID.SIPRI_MILEX_2024,
    source_type="external",
    description="Real compound annual growth rate of global military spending over the last decade "
                "(2014-2024). SIPRI reports 10 consecutive annual increases, with 2024 up 9.4% in "
                "real terms. The 10-year CAGR is approximately 3.4% real.",
    display_name="Military Spending Real CAGR (10-Year)",
    unit="percent",
    distribution="fixed",
    keywords=["military", "spending", "growth", "CAGR", "SIPRI", "trend", "decade"],
    latex_symbol=r"g_{mil,10yr}",
)

GLOBAL_MILITARY_SPENDING_ANNUAL_2005 = Parameter(
    1_621_800_000_000,
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_ref=ReferenceID.SIPRI_MILEX_2024,
    source_type="external",
    description="Global military spending in 2005, constant 2023 USD (SIPRI World total). "
                "Used as the 20-year reference point for computing the long-horizon real CAGR.",
    display_name="Global Military Spending in 2005 (Constant 2023 USD)",
    unit="USD",
    distribution="fixed",
    keywords=["2005", "historical", "sipri", "military", "spending", "baseline"],
    latex_symbol=r"Spending_{mil,2005}",
)

GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR = Parameter(
    (2_720_000_000_000 / 1_621_800_000_000) ** (1 / 19) - 1,
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_type="calculated",
    description="Real compound annual growth rate of global military spending over the last 20 years "
                "(2005-2024), computed from SIPRI World totals in constant 2023 USD. This window "
                "deliberately includes the 2011-2014 drawdown, so it cannot be attacked as "
                "trough-to-peak cherry picking. The 20-year rate (~2.75%) is actually lower than the "
                "10-year rate (3.4%) precisely because the drawdown pulls the average down.",
    display_name="Military Spending Real CAGR (20-Year)",
    unit="percent",
    formula="(GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_MILITARY_SPENDING_ANNUAL_2005)^(1/19) - 1",
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "GLOBAL_MILITARY_SPENDING_ANNUAL_2005"],
    compute=lambda ctx: (ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2005"]) ** (1 / 19) - 1,
    keywords=["military", "spending", "growth", "CAGR", "SIPRI", "20-year", "trend", "drawdown"],
    latex_symbol=r"g_{mil,20yr}",
)

# Cybercrime economic data
GLOBAL_CYBERCRIME_COST_ANNUAL_2025 = Parameter(
    10_500_000_000_000,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_ref=ReferenceID.CYBERCRIME_ECONOMY_10_5T,
    source_type="external",
    description="Projected global cybercrime costs in 2025. Includes data theft, productivity loss, "
                "IP theft, fraud. More profitable than global trade of all major illegal drugs combined. "
                "If measured as a country, would be the 3rd largest economy after US and China.",
    display_name="Global Cybercrime Costs (2025)",
    unit="USD",
    distribution="fixed",
    keywords=["cybercrime", "cost", "2025", "theft", "fraud", "hacking"],
    latex_symbol=r"Cost_{cyber}",
)

GLOBAL_CYBERCRIME_CAGR = Parameter(
    0.15,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_ref=ReferenceID.CYBERCRIME_ECONOMY_10_5T,
    source_type="external",
    description="Compound annual growth rate of global cybercrime costs. "
                "Cybersecurity Ventures: $3T (2015) -> $6T (2021) -> $10.5T (2025). "
                "AI-enhanced attacks are accelerating this trend.",
    display_name="Cybercrime Cost CAGR",
    unit="percent",
    distribution="fixed",
    keywords=["cybercrime", "growth", "CAGR", "trend"],
    latex_symbol=r"g_{cyber}",
)

# Destructive economy aggregate (military + cybercrime + conflict costs)
GLOBAL_DESTRUCTIVE_ECONOMY_ANNUAL_2025 = Parameter(
    2_720_000_000_000 + 10_500_000_000_000,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Combined annual cost of military spending and cybercrime. "
                "The 'destructive economy' that competes with the productive economy.",
    display_name="Global Destructive Economy (2025)",
    unit="USD",
    formula="GLOBAL_MILITARY_SPENDING_ANNUAL_2024 + GLOBAL_CYBERCRIME_COST_ANNUAL_2025",
    keywords=["destructive", "economy", "military", "cybercrime", "total"],
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "GLOBAL_CYBERCRIME_COST_ANNUAL_2025"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] + ctx["GLOBAL_CYBERCRIME_COST_ANNUAL_2025"],
    latex_symbol=r"Cost_{destruct}",
)

GLOBAL_DESTRUCTIVE_ECONOMY_PCT_GDP = Parameter(
    (2_720_000_000_000 + 10_500_000_000_000) / 115_000_000_000_000,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Destructive economy (military + cybercrime) as percentage of global GDP.",
    display_name="Destructive Economy as % of GDP",
    unit="percent",
    formula="GLOBAL_DESTRUCTIVE_ECONOMY_ANNUAL_2025 / GLOBAL_GDP_2025",
    keywords=["destructive", "economy", "GDP", "percentage"],
    inputs=["GLOBAL_DESTRUCTIVE_ECONOMY_ANNUAL_2025", "GLOBAL_GDP_2025"],
    compute=lambda ctx: ctx["GLOBAL_DESTRUCTIVE_ECONOMY_ANNUAL_2025"] / ctx["GLOBAL_GDP_2025"],
    latex_symbol=r"r_{destruct:GDP}",
)

# Destructive economy timeline projections
# Calculate the year when destructive economy (military + cybercrime at current growth rates)
# reaches critical thresholds as % of GDP
import math as _math

# Weighted growth rate of destructive economy
# Military ($2.72T at 3.4%) + Cybercrime ($10.5T at 15%) = weighted by share
_mil_share = 2_720_000_000_000 / (2_720_000_000_000 + 10_500_000_000_000)
_cyber_share = 10_500_000_000_000 / (2_720_000_000_000 + 10_500_000_000_000)
_destructive_growth = _mil_share * 0.034 + _cyber_share * 0.15  # ~12.6% weighted

DESTRUCTIVE_ECONOMY_BASE_YEAR = Parameter(
    2025,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="definition",
    distribution="fixed",
    description="Base year for destructive economy projections. All threshold timelines are measured from this year.",
    display_name="Destructive Economy Base Year",
    unit="year",
    keywords=["destructive", "economy", "base year"],
    latex_symbol=r"Y_0",
)

# Year when destructive economy reaches 25% of GDP (historical instability threshold)
# Solve: 0.115 * (1 + g_destruct - g_gdp)^n = 0.25
# n = ln(0.25/0.115) / ln(1 + 0.126 - 0.025)
_ratio_growth = _destructive_growth - 0.025  # net growth of ratio
_years_to_25pct = _math.log(0.25 / 0.115) / _math.log(1 + _ratio_growth)
_years_to_35pct = _math.log(0.35 / 0.115) / _math.log(1 + _ratio_growth)
_years_to_50pct = _math.log(0.50 / 0.115) / _math.log(1 + _ratio_growth)

# Calendar years when destructive economy thresholds are reached
_destruct_inputs = ["DESTRUCTIVE_ECONOMY_BASE_YEAR", "GLOBAL_DESTRUCTIVE_ECONOMY_PCT_GDP", "GLOBAL_CYBERCRIME_CAGR", "GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR", "GDP_BASELINE_GROWTH_RATE", "GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "GLOBAL_DESTRUCTIVE_ECONOMY_ANNUAL_2025", "GLOBAL_CYBERCRIME_COST_ANNUAL_2025"]

def _destruct_year_compute(threshold):
    """Return a compute lambda for the calendar year when destructive economy reaches threshold."""
    return lambda ctx: ctx["DESTRUCTIVE_ECONOMY_BASE_YEAR"] + round(
        _math.log(threshold / ctx["GLOBAL_DESTRUCTIVE_ECONOMY_PCT_GDP"])
        / _math.log(1 + (
            (ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_DESTRUCTIVE_ECONOMY_ANNUAL_2025"]) * ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR"]
            + (ctx["GLOBAL_CYBERCRIME_COST_ANNUAL_2025"] / ctx["GLOBAL_DESTRUCTIVE_ECONOMY_ANNUAL_2025"]) * ctx["GLOBAL_CYBERCRIME_CAGR"]
        ) - ctx["GDP_BASELINE_GROWTH_RATE"])
    )

DESTRUCTIVE_ECONOMY_25PCT_YEAR = Parameter(
    2025 + round(_years_to_25pct),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Calendar year when the destructive economy (military + cybercrime) reaches 25% of GDP "
                "at current growth rates. Historical precedent suggests societies become unstable "
                "when extraction rates exceed 20-30% of economic output.",
    display_name="Year Destructive Economy Reaches 25% of GDP",
    unit="year",
    formula="DESTRUCTIVE_ECONOMY_BASE_YEAR + ln(0.25 / DESTRUCTIVE_PCT_GDP) / ln(1 + DESTRUCTIVE_GROWTH - GDP_GROWTH)",
    keywords=["destructive", "economy", "timeline", "year", "25%", "instability"],
    inputs=_destruct_inputs,
    compute=_destruct_year_compute(0.25),
    latex_symbol=r"Y_{25\%}",
)

DESTRUCTIVE_ECONOMY_35PCT_YEAR = Parameter(
    2025 + round(_years_to_35pct),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Calendar year when the destructive economy (military + cybercrime) reaches 35% of GDP "
                "at current growth rates. Historical evidence from the Soviet Union, Yugoslavia, "
                "Argentina, and Zimbabwe shows that total extractive burdens of 35-45% consistently "
                "trigger self-reinforcing death spirals. This is the empirically-derived terminal "
                "parasitic load threshold.",
    display_name="Year Destructive Economy Reaches 35% of GDP (Terminal Parasitic Load)",
    unit="year",
    formula="DESTRUCTIVE_ECONOMY_BASE_YEAR + ln(0.35 / DESTRUCTIVE_PCT_GDP) / ln(1 + DESTRUCTIVE_GROWTH - GDP_GROWTH)",
    keywords=["destructive", "economy", "timeline", "year", "35%", "terminal parasitic load", "collapse"],
    inputs=_destruct_inputs,
    compute=_destruct_year_compute(0.35),
    latex_symbol=r"Y_{35\%}",
)

DESTRUCTIVE_ECONOMY_50PCT_YEAR = Parameter(
    2025 + round(_years_to_50pct),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Calendar year when the destructive economy (military + cybercrime) reaches 50% of GDP "
                "at current growth rates. At that point, half of all economic activity is "
                "destructive, so stealing starts to beat creating for individuals, firms, and "
                "states because whatever gets created gets looted fast enough to kill productive investment.",
    display_name="Year Destructive Economy Reaches 50% of GDP",
    unit="year",
    formula="DESTRUCTIVE_ECONOMY_BASE_YEAR + ln(0.50 / DESTRUCTIVE_PCT_GDP) / ln(1 + DESTRUCTIVE_GROWTH - GDP_GROWTH)",
    keywords=["destructive", "economy", "timeline", "year", "50%", "crossover"],
    inputs=_destruct_inputs,
    compute=_destruct_year_compute(0.50),
    latex_symbol=r"Y_{50\%}",
)

# Value of Statistical Life (VSL)
VALUE_OF_STATISTICAL_LIFE = Parameter(
    10_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.DOT_VSL_13_6M,
    source_type="external",
    description="Value of Statistical Life (conservative estimate)",
    display_name="Value of Statistical Life",
    unit="USD",
    distribution=DistributionType.GAMMA,
    std_error=3_000_000,  # Significant variation in VSL estimates
    validation_min=1_000_000,  # Hard lower bound
    confidence_interval=(5_000_000, 15_000_000),
    keywords=["10.0m", "low estimate", "cautious", "pessimistic", "worst case", "conservative", "underestimate"],
    latex_symbol=r"VSL",  # LaTeX symbol for equations
)  # US DOT uses $13.6M, we use $10M conservatively

# Conflict death breakdown (for QALY calculations)
# Source: knowledge/problem/cost-of-war.qmd#death-accounting
GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT = Parameter(
    233600,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.ACLED_ACTIVE_COMBAT_DEATHS,
    source_type="external",
    description="Annual deaths from active combat worldwide",
    display_name="Annual Deaths from Active Combat Worldwide",
    unit="deaths/year",
    keywords=["234k", "worldwide", "yearly", "fatalities", "casualties", "mortality", "active"],
    distribution="lognormal",
    confidence_interval=(180_000, 300_000),  # ±20% - conflict data has high uncertainty
    latex_symbol=r"Deaths_{combat}",  # LaTeX symbol for equations
)  # ACLED data

GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS = Parameter(
    8300,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.GTD_TERROR_ATTACK_DEATHS,
    source_type="external",
    description="Annual deaths from terror attacks globally",
    display_name="Annual Deaths from Terror Attacks Globally",
    unit="deaths/year",
    keywords=["8k", "worldwide", "yearly", "fatalities", "casualties", "mortality", "terror"],
    distribution="lognormal",
    confidence_interval=(6_000, 12_000),  # ±25% - terrorism data varies by definition
    latex_symbol=r"Deaths_{terror}",  # LaTeX symbol for equations
)  # Global Terrorism Database

GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE = Parameter(
    2700,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.UCDP_STATE_VIOLENCE_DEATHS,
    source_type="external",
    description="Annual deaths from state violence",
    display_name="Annual Deaths from State Violence",
    unit="deaths/year",
    keywords=["3k", "worldwide", "yearly", "fatalities", "casualties", "mortality", "state"],
    distribution="lognormal",
    confidence_interval=(1_500, 5_000),  # ±40% - state violence often underreported
    latex_symbol=r"Deaths_{state}",  # LaTeX symbol for equations
)  # Uppsala Conflict Data Program

# Historical democide (government murder of unarmed civilians, 1900-1999)
# Source: R.J. Rummel, "Death by Government" (1994) and "Statistics of Democide" (1998)
DEMOCIDE_TOTAL_20TH_CENTURY = Parameter(
    262_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.RUMMEL_DEATH_BY_GOVERNMENT,
    source_type="external",
    description="Total people murdered by governments worldwide, 1900-1999 (Rummel's democide estimate)",
    display_name="20th-Century Government Democide Total",
    unit="deaths",
    keywords=["democide", "genocide", "government", "murder", "rummel", "20th century", "262 million"],
    distribution="uniform",
    confidence_interval=(200_000_000, 272_000_000),  # Rummel's range: 200M-272M+
    latex_symbol=r"D_{democide,20C}",
)

# Total conflict deaths (calculated from breakdown)
GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Total annual conflict deaths globally (sum of combat, terror, state violence)",
    display_name="Total Annual Conflict Deaths Globally",
    unit="deaths/year",
    formula="COMBAT + TERROR + STATE_VIOLENCE",    keywords=["worldwide", "yearly", "fatalities", "casualties", "mortality", "armed conflict", "loss of life"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT', 'GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE', 'GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT"]
    + ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS"]
    + ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE"],
    latex_symbol=r"Deaths_{conflict}",  # LaTeX symbol for equations
)  # 244,600

# Breakdown of Human Life Loss Costs (billions USD)
GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Annual cost of combat deaths (deaths × VSL)",
    display_name="Annual Cost of Combat Deaths",
    unit="USD/year",
    formula="COMBAT_DEATHS × VSL ",
    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "mortality"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT', 'VALUE_OF_STATISTICAL_LIFE'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    latex_symbol=r"Cost_{combat,human}",  # LaTeX symbol for equations
)  # $2,336B

GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Annual cost of terror deaths (deaths × VSL)",
    display_name="Annual Cost of Terror Deaths",
    unit="USD/year",
    formula="TERROR_DEATHS × VSL ",
    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "mortality"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS', 'VALUE_OF_STATISTICAL_LIFE'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    latex_symbol=r"Cost_{terror,human}",  # LaTeX symbol for equations
)  # $83B

GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Annual cost of state violence deaths (deaths × VSL)",
    display_name="Annual Cost of State Violence Deaths",
    unit="USD/year",
    formula="STATE_DEATHS × VSL ",
    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "mortality"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE', 'VALUE_OF_STATISTICAL_LIFE'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    latex_symbol=r"Cost_{state,human}",  # LaTeX symbol for equations
)  # $27B

# Total human life losses (calculated from breakdown)
GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT = Parameter(
    GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS
    + GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Total annual human life losses from conflict (sum of combat, terror, state violence)",
    display_name="Total Annual Human Life Losses from Conflict",
    unit="USD/year",
    formula="COMBAT_COST + TERROR_COST + STATE_VIOLENCE_COST",    keywords=["worldwide", "yearly", "human", "life", "losses", "armed conflict", "military action"],
    inputs=['GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT', 'GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE', 'GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT"]
    + ctx["GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS"]
    + ctx["GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE"],
    latex_symbol=r"Loss_{life,conflict}",  # LaTeX symbol for equations
)  # $2,446B

# Infrastructure Damage Breakdown (billions USD)
GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT = Parameter(
    487_300_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.ENVIRONMENTAL_COST_OF_WAR,
    source_type="external",
    description="Annual infrastructure damage to transportation from conflict",
    display_name="Annual Infrastructure Damage to Transportation from Conflict",
    unit="USD",
    keywords=["487.3b", "worldwide", "yearly", "infrastructure", "damage", "transportation", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(340_000_000_000, 680_000_000_000),  # ±30% - damage estimates highly variable
    latex_symbol=r"Damage_{transport}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT = Parameter(
    421_700_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.ENVIRONMENTAL_COST_OF_WAR,
    source_type="external",
    description="Annual infrastructure damage to energy systems from conflict",
    display_name="Annual Infrastructure Damage to Energy Systems from Conflict",
    unit="USD",
    keywords=["421.7b", "worldwide", "yearly", "infrastructure", "damage", "energy", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(295_000_000_000, 590_000_000_000),  # ±30%
    latex_symbol=r"Damage_{energy}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT = Parameter(
    298_100_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.ENVIRONMENTAL_COST_OF_WAR,
    source_type="external",
    description="Annual infrastructure damage to communications from conflict",
    display_name="Annual Infrastructure Damage to Communications from Conflict",
    unit="USD",
    keywords=["298.1b", "worldwide", "yearly", "infrastructure", "damage", "communications", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(209_000_000_000, 418_000_000_000),  # ±30%
    latex_symbol=r"Damage_{comms}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT = Parameter(
    267_800_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.ENVIRONMENTAL_COST_OF_WAR,
    source_type="external",
    description="Annual infrastructure damage to water systems from conflict",
    display_name="Annual Infrastructure Damage to Water Systems from Conflict",
    unit="USD",
    keywords=["267.8b", "worldwide", "yearly", "infrastructure", "damage", "water", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(187_000_000_000, 375_000_000_000),  # ±30%
    latex_symbol=r"Damage_{water}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT = Parameter(
    234_500_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.ENVIRONMENTAL_COST_OF_WAR,
    source_type="external",
    description="Annual infrastructure damage to education facilities from conflict",
    display_name="Annual Infrastructure Damage to Education Facilities from Conflict",
    unit="USD",
    keywords=["234.5b", "worldwide", "yearly", "infrastructure", "damage", "education", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(164_000_000_000, 328_000_000_000),  # ±30%
    latex_symbol=r"Damage_{edu}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT = Parameter(
    165_600_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.ENVIRONMENTAL_COST_OF_WAR,
    source_type="external",
    description="Annual infrastructure damage to healthcare facilities from conflict",
    display_name="Annual Infrastructure Damage to Healthcare Facilities from Conflict",
    unit="USD",
    keywords=["165.6b", "worldwide", "yearly", "infrastructure", "damage", "healthcare", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(116_000_000_000, 232_000_000_000),  # ±30%
    latex_symbol=r"Damage_{health}",  # LaTeX symbol for equations
)

# Total infrastructure destruction (calculated from breakdown)
GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT = Parameter(
    GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Total annual infrastructure destruction (sum of transportation, energy, communications, water, education, healthcare)",
    display_name="Total Annual Infrastructure Destruction",
    unit="USD/year",
    formula="TRANSPORT + ENERGY + COMMS + WATER + EDUCATION + HEALTHCARE",    keywords=["worldwide", "yearly", "infrastructure", "destruction", "armed conflict", "military action", "international"],
    inputs=['GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT"],
    latex_symbol=r"Damage_{infra,total}",  # LaTeX symbol for equations
)  # $1,875B

# Trade Disruption Breakdown (billions USD)
GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT = Parameter(
    247_100_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.WORLD_BANK_TRADE_DISRUPTION_CONFLICT,
    source_type="external",
    description="Annual trade disruption costs from shipping disruptions",
    display_name="Annual Trade Disruption Costs from Shipping Disruptions",
    unit="USD",
    keywords=["247.1b", "worldwide", "yearly", "trade", "disruption", "shipping", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(173_000_000_000, 346_000_000_000),  # ±30% - economic cost estimates variable
    latex_symbol=r"Disruption_{shipping}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT = Parameter(
    186_800_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.WORLD_BANK_TRADE_DISRUPTION_CONFLICT,
    source_type="external",
    description="Annual trade disruption costs from supply chain disruptions",
    display_name="Annual Trade Disruption Costs from Supply Chain Disruptions",
    unit="USD",
    keywords=["186.8b", "worldwide", "yearly", "trade", "disruption", "supply", "chain"],
    distribution="lognormal",
    confidence_interval=(131_000_000_000, 262_000_000_000),  # ±30%
    latex_symbol=r"Disruption_{supply}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT = Parameter(
    124_700_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.WORLD_BANK_TRADE_DISRUPTION_CONFLICT,
    source_type="external",
    description="Annual trade disruption costs from energy price volatility",
    display_name="Annual Trade Disruption Costs from Energy Price Volatility",
    unit="USD",
    keywords=["124.7b", "worldwide", "yearly", "trade", "disruption", "energy", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(87_000_000_000, 175_000_000_000),  # ±30%
    latex_symbol=r"Disruption_{energy}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT = Parameter(
    57_400_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.WORLD_BANK_TRADE_DISRUPTION_CONFLICT,
    source_type="external",
    description="Annual trade disruption costs from currency instability",
    display_name="Annual Trade Disruption Costs from Currency Instability",
    unit="USD",
    keywords=["57.4b", "worldwide", "yearly", "trade", "disruption", "currency", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(40_000_000_000, 80_000_000_000),  # ±30%
    latex_symbol=r"Disruption_{currency}",  # LaTeX symbol for equations
)

# Total trade disruption (calculated from breakdown)
GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT = Parameter(
    GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Total annual trade disruption (sum of shipping, supply chain, energy prices, currency instability)",
    display_name="Total Annual Trade Disruption",
    unit="USD/year",
    formula="SHIPPING + SUPPLY_CHAIN + ENERGY_PRICE + CURRENCY",    keywords=["worldwide", "yearly", "trade", "disruption", "armed conflict", "military action", "international"],
    inputs=['GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT"],
    latex_symbol=r"Disruption_{trade}",  # LaTeX symbol for equations
)  # $616B

GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT
    + GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Total annual direct war costs (military spending + infrastructure + human life + trade disruption)",
    display_name="Total Annual Direct War Costs",
    unit="USD/year",
    formula="MILITARY + INFRASTRUCTURE + HUMAN_LIFE + TRADE",    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "worldwide"],
    inputs=['GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT', 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT"],
    latex_symbol=r"Cost_{war,direct}",  # LaTeX symbol for equations
)  # $7,655B

# Indirect costs
GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING = Parameter(
    2_718_000_000_000,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_ref=ReferenceID.DISPARITY_RATIO_WEAPONS_VS_CURES,
    source_type="external",
    description="Annual foregone economic output from military spending vs productive alternatives. This estimate implicitly captures fiscal multiplier differences (military ~0.6x vs healthcare ~4.3x GDP multiplier). Do not add separate GDP multiplier adjustment to avoid double-counting.",
    display_name="Annual Lost Economic Growth from Military Spending Opportunity Cost",
    unit="USD",
    keywords=["2.7t", "dod", "pentagon", "national security", "army", "navy", "armed forces"],
    distribution="lognormal",
    confidence_interval=(1_900_000_000_000, 3_800_000_000_000),
    latex_symbol=r"Loss_{growth,mil}",
)

GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS = Parameter(
    200_100_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.VETERAN_HEALTHCARE_COST_PROJECTIONS,
    source_type="external",
    description="Annual veteran healthcare costs (20-year projected)",
    display_name="Annual Veteran Healthcare Costs",
    unit="USD",
    keywords=["200.1b", "worldwide", "yearly", "funding", "investment", "veteran", "healthcare"],
    distribution="lognormal",
    confidence_interval=(140_000_000_000, 280_000_000_000),  # ±30%
    latex_symbol=r"Cost_{vet}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS = Parameter(
    150_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.UNHCR_REFUGEE_SUPPORT_COST,
    source_type="external",
    description="Annual refugee support costs (108.4M refugees × $1,384/year)",
    display_name="Annual Refugee Support Costs",
    unit="USD",
    keywords=["150.0b", "worldwide", "yearly", "funding", "investment", "refugee", "support"],
    distribution="lognormal",
    confidence_interval=(105_000_000_000, 210_000_000_000),  # ±30%
    latex_symbol=r"Cost_{refugee}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT = Parameter(
    100_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.ENVIRONMENTAL_COST_OF_WAR,
    source_type="external",
    description="Annual environmental damage and restoration costs from conflict",
    display_name="Annual Environmental Damage and Restoration Costs from Conflict",
    unit="USD",
    keywords=["100.0b", "worldwide", "yearly", "environmental", "damage", "armed conflict", "military action"],
    distribution="lognormal",
    confidence_interval=(70_000_000_000, 140_000_000_000),  # ±30%
    latex_symbol=r"Damage_{env}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT = Parameter(
    232_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.PSYCHOLOGICAL_IMPACT_WAR_COST,
    source_type="external",
    description="Annual PTSD and mental health costs from conflict",
    display_name="Annual PTSD and Mental Health Costs from Conflict",
    unit="USD",
    keywords=["232.0b", "worldwide", "yearly", "funding", "investment", "psychological", "impact"],
    distribution="lognormal",
    confidence_interval=(162_000_000_000, 325_000_000_000),  # ±30%
    latex_symbol=r"Cost_{psych}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT = Parameter(
    300_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.LOST_HUMAN_CAPITAL_WAR_COST,
    source_type="external",
    description="Annual lost productivity from conflict casualties",
    display_name="Annual Lost Productivity from Conflict Casualties",
    unit="USD",
    keywords=["300.0b", "worldwide", "yearly", "lost", "human", "capital", "armed conflict"],
    distribution="lognormal",
    confidence_interval=(210_000_000_000, 420_000_000_000),  # ±30%
    latex_symbol=r"Loss_{capital,conflict}",  # LaTeX symbol for equations
)

GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL = Parameter(
    GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING
    + GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS
    + GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS
    + GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT
    + GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT
    + GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Total annual indirect war costs (opportunity cost + veterans + refugees + environment + mental health + lost productivity)",
    display_name="Total Annual Indirect War Costs",
    unit="USD/year",
    formula="OPPORTUNITY + VETERANS + REFUGEES + ENVIRONMENT + MENTAL_HEALTH + LOST_CAPITAL",    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "worldwide"],
    inputs=['GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT', 'GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING', 'GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT', 'GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT', 'GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS', 'GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING"]
    + ctx["GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS"]
    + ctx["GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS"]
    + ctx["GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT"],
    latex_symbol=r"Cost_{war,indirect}",  # LaTeX symbol for equations
)  # $3,700.1B

# Grand total war costs
GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST = Parameter(
    GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL + GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Total annual cost of war worldwide (direct + indirect costs)",
    display_name="Total Annual Cost of War Worldwide",
    unit="USD/year",
    formula="DIRECT_COSTS + INDIRECT_COSTS",    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "war"],
    # Uncertainty derived from inputs (DIRECT + INDIRECT costs)
    validation_min=8_000_000_000_000,   # Floor: Direct costs only, conservative VSL
    validation_max=16_000_000_000_000,  # Ceiling: Including all indirect/long-term costs
    inputs=["GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL", "GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL"] + ctx["GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL"],
    latex_symbol=r"Cost_{war,total}",  # LaTeX symbol for equations
)  # $11,355.1B

# Treaty parameters
TREATY_REDUCTION_PCT = Parameter(
    0.01,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="",  # Core definition - not sourced, it's what we're proposing
    source_type="definition",
    description="1% reduction in military spending/war costs from treaty",
    display_name="1% Reduction in Military Spending/War Costs from Treaty",
    unit="rate",
    keywords=["1%", "dod", "pentagon", "national security", "army", "navy", "one percent"],
    distribution="fixed",  # Policy choice: the 1% is our proposal, not uncertain
    latex_symbol=r"Reduce_{treaty}",  # LaTeX symbol for equations
)  # Core treaty definition - the 1% is our proposal, not derived from external data

TREATY_ANNUAL_FUNDING = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="",
    source_type="calculated",  # Derived from military spending and treaty percentage
    description="Annual funding from 1% of global military spending redirected to DIH",
    display_name="Annual Funding from 1% of Global Military Spending Redirected to DIH",
    unit="USD/year",
    formula="MILITARY_SPENDING × 1%",
    keywords=["1%", "dod", "pentagon", "distributed research", "global research", "national security", "open science"],
    inputs=['GLOBAL_MILITARY_SPENDING_ANNUAL_2024', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Funding_{treaty}",  # LaTeX symbol for equations
)  # $27.2B (clean display throughout book)

# ==============================================================================
# PEACE DIVIDEND - RECURRING ANNUAL BENEFIT ($114B/year perpetual)
# ==============================================================================
# A 1% treaty redirects 1% of military spending ($27.2B/year) to pragmatic clinical trials.
# This generates recurring annual benefits from reduced conflict costs:
#   - Direct military savings
#   - Reduced infrastructure destruction
#   - Fewer casualties and refugee costs
#   - Reduced lost economic growth
# Total recurring peace dividend: $114B/year (happens every year forever)
# ==============================================================================

PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT = Parameter(
    GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Annual peace dividend from 1% reduction in total war costs (theoretical maximum at ε=1.0)",
    display_name="Annual Peace Dividend from 1% Reduction in Total War Costs",
    unit="USD/year",
    formula="TOTAL_WAR_COST × 1% × ε (baseline ε=1.0)",
    keywords=["conflict resolution", "international agreement", "peace treaty", "yearly", "armistice", "ceasefire", "conflict"],
    # Note: CI ($70B-$180B) derived from input parameter uncertainties via Monte Carlo
    validation_min=70_000_000_000,   # Floor: Conservative war cost estimates, 50% realization
    validation_max=180_000_000_000,  # Ceiling: Including all indirect costs, full compliance
    inputs=["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST", "TREATY_REDUCTION_PCT"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Benefit_{peace,soc}",  # LaTeX symbol for equations
)  # $113.55B, rounded to $114B

PEACE_DIVIDEND_CONFLICT_ELASTICITY = Parameter(
    1.0,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="definition",
    description="Conflict reduction elasticity: how much conflict costs decrease per 1% military spending cut. ε=0: no effect (spending cuts don't reduce conflict). ε=0.5: moderate linkage (conservative). ε=1.0: proportional (baseline assumption). ε>1.0: shared enemy amplification (redirecting to disease creates unity).",
    display_name="Peace Dividend Conflict Elasticity",
    unit="ratio",
    distribution="beta",
    confidence_interval=(0.25, 1.5),
    validation_min=0.0,
    validation_max=2.0,
    formula="1% spending cut → ε% conflict cost reduction",
    latex_symbol=r"\varepsilon_{conflict}",
)

# ==============================================================================
# LONG-TERM PEACE DIVIDEND (80-year horizon against SIPRI 20-year trend)
# ==============================================================================
# The baseline war cost isn't flat. SIPRI shows global military spending grew at
# ~2.76% real per year over 2005-2024, a window that includes the 2011-2014
# drawdown (so it's not cherry-picked). Project that growth forward over one
# full human lifespan (80 years, matching the "per person lifetime tab"
# framing the chapter opens with) and the numbers diverge: within a century,
# war spending mathematically exceeds the entire current world GDP. The treaty
# doesn't just save ~$114B/year, it replaces an exponential trajectory with a
# flat one.
# ==============================================================================

import math as _pd_math

# --- War costs projected forward (these are costs, not dividends) ---

GLOBAL_WAR_COST_YEAR_80_BASELINE = Parameter(
    float(GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST) * (1 + float(GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR)) ** 80,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Projected annual war cost in year 80 under the baseline trajectory, assuming the "
                "SIPRI 20-year real CAGR continues. At ~2.76% real growth, this approaches current "
                "world GDP (which is why the baseline trajectory breaks math around year 85).",
    display_name="Annual War Cost in Year 80 (Baseline Trajectory)",
    unit="USD/year",
    formula="GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST × (1 + g_{mil,20yr})^80",
    inputs=["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST", "GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] * (1 + ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"]) ** 80,
    keywords=["baseline", "projection", "year 80", "war cost", "trajectory", "lifetime"],
    latex_symbol=r"Cost_{war,yr80}",
)

# Closed-form cumulative war cost over 80 years on the baseline trajectory:
# Σ_{t=0..79} C(1+g)^t = C · ((1+g)^80 - 1) / g
_pd_C = float(GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST)
_pd_g = float(GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR)
_pd_p = float(TREATY_REDUCTION_PCT)
_pd_lt_baseline_cum = _pd_C * ((1 + _pd_g) ** 80 - 1) / _pd_g
_pd_lt_treaty_cum = _pd_C * (1 - _pd_p) * 80
_pd_lt_savings = _pd_lt_baseline_cum - _pd_lt_treaty_cum

GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE = Parameter(
    _pd_lt_baseline_cum,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Cumulative global war cost over 80 years (one human lifespan) on the baseline "
                "trajectory, where war costs keep compounding at SIPRI's 20-year real CAGR (2.76%). "
                "This is what the world pays if nothing changes.",
    display_name="Cumulative 80-Year War Cost (Baseline Trajectory)",
    unit="USD",
    formula="C × ((1 + g)^80 - 1) / g",
    inputs=["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST", "GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] * (
        ((1 + ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"]) ** 80 - 1)
        / ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"]
    ),
    keywords=["cumulative", "80 years", "lifetime", "baseline", "war cost", "trajectory"],
    latex_symbol=r"Cost_{war,cum,baseline}",
)

GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_TREATY = Parameter(
    _pd_lt_treaty_cum,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Cumulative global war cost over 80 years under the treaty trajectory, where costs "
                "drop 1% immediately and then hold flat (no growth). This is what the world pays "
                "after the treaty passes.",
    display_name="Cumulative 80-Year War Cost (Treaty Trajectory)",
    unit="USD",
    formula="C × (1 - TREATY_REDUCTION_PCT) × 80",
    inputs=["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST", "TREATY_REDUCTION_PCT"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] * (1 - ctx["TREATY_REDUCTION_PCT"]) * 80,
    keywords=["cumulative", "80 years", "lifetime", "treaty", "war cost", "flat"],
    latex_symbol=r"Cost_{war,cum,treaty}",
)

GLOBAL_WAR_COST_LIFETIME_PER_PERSON_FLAT = Parameter(
    float(GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST) * 80 / 8_000_000_000,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Per-person 80-year lifetime tab for global war costs, assuming costs stay flat at "
                "today's level. This is the conservative floor the chapter opens with. The actual "
                "figure is higher because war costs have been compounding in real terms.",
    display_name="Per-Person 80-Year War Cost (Flat Assumption)",
    unit="USD",
    formula="GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST × 80 / GLOBAL_POPULATION_2024",
    inputs=["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] * 80 / ctx["GLOBAL_POPULATION_2024"],
    keywords=["per-person", "lifetime", "80 years", "flat", "war cost"],
    latex_symbol=r"Cost_{war,pp,flat}",
)

GLOBAL_WAR_COST_LIFETIME_PER_PERSON_BASELINE = Parameter(
    _pd_lt_baseline_cum / 8_000_000_000,
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_type="calculated",
    description="Per-person 80-year lifetime tab for global war costs on the SIPRI baseline "
                "trajectory (2.76% real growth). About 3.5x the flat-assumption figure the chapter "
                "opens with, because war costs have been compounding while nobody updated the "
                "invoice.",
    display_name="Per-Person 80-Year War Cost (Baseline Trajectory)",
    unit="USD",
    formula="GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE / GLOBAL_POPULATION_2024",
    inputs=["GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["per-person", "lifetime", "80 years", "baseline", "SIPRI", "war cost"],
    latex_symbol=r"Cost_{war,pp,baseline}",
)

GLOBAL_WAR_COST_YEARS_UNTIL_EXCEEDS_GDP = Parameter(
    _pd_math.log(115_000_000_000_000 / _pd_C) / _pd_math.log(1 + _pd_g),
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Years until annual war cost exceeds current world GDP at the SIPRI 20-year real "
                "growth rate. At ~2.76% real growth and $11.4T current war cost, this happens in "
                "under a century. The baseline trajectory is therefore a countdown, not a plan.",
    display_name="Years Until Baseline War Cost Exceeds Current World GDP",
    unit="years",
    formula="log(GLOBAL_GDP_2025 / GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST) / log(1 + g_{mil,20yr})",
    inputs=["GLOBAL_GDP_2025", "GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST", "GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"],
    compute=lambda ctx: _pd_math.log(ctx["GLOBAL_GDP_2025"] / ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"])
        / _pd_math.log(1 + ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"]),
    keywords=["countdown", "exponential", "GDP", "limit", "baseline"],
    latex_symbol=r"T_{GDP}",
)

# --- Actual peace dividend (these are savings) ---

PEACE_DIVIDEND_LIFETIME_TOTAL = Parameter(
    _pd_lt_savings,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Cumulative peace dividend over 80 years (one human lifespan): the baseline "
                "80-year war cost (SIPRI trajectory) minus the treaty 80-year war cost (flat at "
                "99% of today). Assumes elasticity of 1.0 between military spending and war costs, "
                "which is almost certainly conservative because the political act of passing the "
                "treaty itself would reflect and reinforce a 'war is stupid' consensus that "
                "reduces externalities super-proportionally.",
    display_name="Cumulative Peace Dividend Over 80 Years",
    unit="USD",
    formula="GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE - GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_TREATY",
    inputs=["GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE", "GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_TREATY"],
    compute=lambda ctx: ctx["GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE"] - ctx["GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_TREATY"],
    keywords=["cumulative", "80 years", "lifetime", "peace dividend", "savings", "trajectory"],
    latex_symbol=r"Savings_{LT}",
)

PEACE_DIVIDEND_LIFETIME_PER_PERSON = Parameter(
    _pd_lt_savings / 8_000_000_000,
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_type="calculated",
    description="Per-person share of the 80-year cumulative peace dividend, averaged across the "
                "global population. Not literally a check in the reader's pocket: most of it "
                "arrives as infrastructure not destroyed, wages not taxed to rebuild things that "
                "should not have been destroyed, and conflicts that never happen. Per-capita "
                "division hides that the poorest bear far more than the average today.",
    display_name="Per-Person 80-Year Peace Dividend",
    unit="USD",
    formula="PEACE_DIVIDEND_LIFETIME_TOTAL / GLOBAL_POPULATION_2024",
    inputs=["PEACE_DIVIDEND_LIFETIME_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["PEACE_DIVIDEND_LIFETIME_TOTAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["per-person", "lifetime", "80 years", "peace dividend", "savings"],
    latex_symbol=r"Savings_{pp,LT}",
)

PEACE_DIVIDEND_INVESTMENT_REAL_RETURN_RATE = Parameter(
    0.13,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="definition",
    description="Illustrative long-term real return rate used to compound the peace dividend "
                "stream into a future value at year 80. 13% is the approximate long-run real CAGR "
                "of the Nasdaq-100 index since its 1985 inception: accessible via passive ETFs "
                "(QQQ), grounded in 40+ years of data, and does not require assuming unique skill "
                "(Buffett) or access (VC/private markets). Chosen as more optimistic than 60/40 "
                "portfolio (5%) or S&P 500 (7%) because growth-tilted founder-led companies have "
                "historically outperformed the broad market.",
    display_name="Assumed Long-Term Real Return for Investment Compounding",
    unit="percent",
    distribution="fixed",
    keywords=["return", "compound", "real", "investment", "nasdaq", "historical"],
    latex_symbol=r"r_{inv}",
)

# Closed-form future value at year 80 of the treaty savings stream:
# FV = Σ_{t=0..79} [C(1+g)^t - C(1-p)] · (1+r)^(79-t)
# Split into two geometric series:
#   Term 1: C · Σ (1+g)^t · (1+r)^(79-t)
#   Term 2: C(1-p) · Σ (1+r)^(79-t)
def _pd_compound_fv(C, g, p, r, N):
    total = 0.0
    for t in range(N):
        saving_t = C * (1 + g) ** t - C * (1 - p)
        total += saving_t * (1 + r) ** (N - 1 - t)
    return total

def _pd_compound_fv_abolition(C, g, r, N):
    total = 0.0
    for t in range(N):
        total += C * (1 + g) ** t * (1 + r) ** (N - 1 - t)
    return total

_pd_r = 0.13
_pd_fv_treaty = _pd_compound_fv(_pd_C, _pd_g, _pd_p, _pd_r, 80)
_pd_fv_abolition = _pd_compound_fv_abolition(_pd_C, _pd_g, _pd_r, 80)

PEACE_DIVIDEND_LIFETIME_PER_PERSON_COMPOUNDED = Parameter(
    _pd_fv_treaty / 8_000_000_000,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Per-person future value at year 80 of the treaty peace dividend stream, "
                "compounded at the illustrative long-term real return rate (13%, Nasdaq-100 "
                "historical). Each year's savings are invested at the end of that year and "
                "compound until year 80. This is an opportunity-cost framing, not a promise of "
                "cash in the reader's pocket: the 'return' is the real productive use of capital "
                "that weapons spending displaced, not a literal brokerage account.",
    display_name="Per-Person Peace Dividend Compounded at 13% over 80 Years",
    unit="USD",
    formula="[Σ_{t=0..79} (C(1+g)^t - C(1-p)) × (1+r)^(79-t)] / GLOBAL_POPULATION_2024",
    inputs=[
        "GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST",
        "GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR",
        "TREATY_REDUCTION_PCT",
        "PEACE_DIVIDEND_INVESTMENT_REAL_RETURN_RATE",
        "GLOBAL_POPULATION_2024",
    ],
    compute=lambda ctx: _pd_compound_fv(
        ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"],
        ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"],
        ctx["TREATY_REDUCTION_PCT"],
        ctx["PEACE_DIVIDEND_INVESTMENT_REAL_RETURN_RATE"],
        80,
    ) / ctx["GLOBAL_POPULATION_2024"],
    keywords=["per-person", "compounded", "future value", "investment", "peace dividend"],
    latex_symbol=r"FV_{pp,treaty}",
)

GLOBAL_WAR_COST_LIFETIME_PER_PERSON_ABOLITION_COMPOUNDED = Parameter(
    _pd_fv_abolition / 8_000_000_000,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Per-person future value at year 80 of the full baseline war cost stream, "
                "compounded at the illustrative long-term real return rate (13%, Nasdaq-100 "
                "historical). This is the hypothetical opportunity cost per person of running "
                "the baseline SIPRI trajectory rather than abolishing war entirely and "
                "redirecting every dollar. Serves as the ceiling on the peace dividend ladder: "
                "the treaty gets you a large fraction of this number, full abolition gets you "
                "all of it.",
    display_name="Per-Person War Cost (Full Abolition) Compounded at 13% over 80 Years",
    unit="USD",
    formula="[Σ_{t=0..79} C(1+g)^t × (1+r)^(79-t)] / GLOBAL_POPULATION_2024",
    inputs=[
        "GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST",
        "GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR",
        "PEACE_DIVIDEND_INVESTMENT_REAL_RETURN_RATE",
        "GLOBAL_POPULATION_2024",
    ],
    compute=lambda ctx: _pd_compound_fv_abolition(
        ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"],
        ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_20YR"],
        ctx["PEACE_DIVIDEND_INVESTMENT_REAL_RETURN_RATE"],
        80,
    ) / ctx["GLOBAL_POPULATION_2024"],
    keywords=["per-person", "abolition", "compounded", "future value", "ceiling"],
    latex_symbol=r"FV_{pp,abolition}",
)

PEACE_DIVIDEND_SHARE_OF_80YR_BASELINE_WAR_COST = Parameter(
    _pd_lt_savings / _pd_lt_baseline_cum,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Fraction of the baseline 80-year war cost avoided by the treaty. Because the "
                "baseline compounds exponentially while the treaty holds spending flat, cutting 1% "
                "today and halting the growth trajectory avoids about 72% of the cumulative "
                "80-year war cost. Most of the savings come from the halted growth, not the "
                "headline 1% cut.",
    display_name="Share of 80-Year War Cost Avoided by Treaty",
    unit="percent",
    formula="PEACE_DIVIDEND_LIFETIME_TOTAL / GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE",
    inputs=["PEACE_DIVIDEND_LIFETIME_TOTAL", "GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE"],
    compute=lambda ctx: ctx["PEACE_DIVIDEND_LIFETIME_TOTAL"] / ctx["GLOBAL_WAR_COST_LIFETIME_CUMULATIVE_BASELINE"],
    keywords=["percent", "fraction", "avoided", "lifetime", "80 years", "ratio"],
    latex_symbol=r"\phi_{avoided}",
    distribution="fixed",  # Algebraic cancellation: BASELINE cancels in numerator and denominator
)

# Individual peace dividend components (1% savings breakdown)
PEACE_DIVIDEND_DIRECT_COSTS = Parameter(
    GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in direct war costs",
    display_name="Annual Savings from 1% Reduction in Direct War Costs",
    unit="USD/year",
    formula="DIRECT_COSTS × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "conflict"],
    inputs=['GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{direct}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_INFRASTRUCTURE = Parameter(
    GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in infrastructure destruction",
    display_name="Annual Savings from 1% Reduction in Infrastructure Destruction",
    unit="USD/year",
    formula="INFRASTRUCTURE_DESTRUCTION × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{infra}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_HUMAN_CASUALTIES = Parameter(
    GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in human casualties",
    display_name="Annual Savings from 1% Reduction in Human Casualties",
    unit="USD/year",
    formula="HUMAN_LIFE_LOSSES × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{casualties}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_TRADE_DISRUPTION = Parameter(
    GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in trade disruption",
    display_name="Annual Savings from 1% Reduction in Trade Disruption",
    unit="USD/year",
    formula="TRADE_DISRUPTION × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{trade}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_INDIRECT_COSTS = Parameter(
    GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in indirect war costs",
    display_name="Annual Savings from 1% Reduction in Indirect War Costs",
    unit="USD/year",
    formula="INDIRECT_COSTS × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "conflict"],
    inputs=['GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{indirect}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_LOST_ECONOMIC_GROWTH = Parameter(
    GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in lost economic growth",
    display_name="Annual Savings from 1% Reduction in Lost Economic Growth",
    unit="USD/year",
    formula="LOST_ECONOMIC_GROWTH × 1%",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict resolution"],
    inputs=['GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{growth}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_VETERAN_HEALTHCARE = Parameter(
    GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in veteran healthcare costs",
    display_name="Annual Savings from 1% Reduction in Veteran Healthcare Costs",
    unit="USD/year",
    formula="VETERAN_HEALTHCARE × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{vet}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_REFUGEE_SUPPORT = Parameter(
    GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in refugee support costs",
    display_name="Annual Savings from 1% Reduction in Refugee Support Costs",
    unit="USD/year",
    formula="REFUGEE_SUPPORT × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{refugee}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_ENVIRONMENTAL = Parameter(
    GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in environmental damage",
    display_name="Annual Savings from 1% Reduction in Environmental Damage",
    unit="USD/year",
    formula="ENVIRONMENTAL_DAMAGE × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{env}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_PTSD = Parameter(
    GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in PTSD and mental health costs",
    display_name="Annual Savings from 1% Reduction in PTSD and Mental Health Costs",
    unit="USD/year",
    formula="PTSD_COSTS × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{PTSD}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_LOST_HUMAN_CAPITAL = Parameter(
    GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in lost human capital",
    display_name="Annual Savings from 1% Reduction in Lost Human Capital",
    unit="USD/year",
    formula="LOST_HUMAN_CAPITAL × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Savings_{capital}",  # LaTeX symbol for equations
)

# Separate peace dividend into confidence levels
PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS = Parameter(
    float(TREATY_ANNUAL_FUNDING),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.SIPRI2024,
    source_type="definition",  # This is a policy-derived value (1% of military spending)
    confidence="high",
    formula="TREATY_ANNUAL_FUNDING",
    description="Direct fiscal savings from 1% military spending reduction (high confidence)",
    display_name="Direct Fiscal Savings from 1% Military Spending Reduction",
    unit="USD/year",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict resolution"],
    latex_symbol=r"Savings_{fiscal}",  # LaTeX symbol for equations
)

PEACE_DIVIDEND_CONFLICT_REDUCTION = Parameter(
    float(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT) - float(TREATY_ANNUAL_FUNDING),
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_ref="calculated",
    source_type="calculated",
    confidence="low",
    formula="PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT - TREATY_ANNUAL_FUNDING",    description="Conflict reduction benefits from 1% less military spending (lower confidence - assumes proportional relationship)",
    display_name="Conflict Reduction Benefits from 1% Less Military Spending",
    unit="USD/year",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict resolution"],
    inputs=['PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT', 'TREATY_ANNUAL_FUNDING'],
    compute=lambda ctx: float(ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"]) - float(ctx["TREATY_ANNUAL_FUNDING"]),
    latex_symbol=r"Savings_{conflict}",  # LaTeX symbol for equations
)

# ---
# HEALTH DIVIDEND PARAMETERS (dFDA)
# ---

# Clinical trial market
# Source: knowledge/appendix/dfda-roi-calculations.qmd
# Updated from market size ($83B) to conservative pharma R&D-based estimate ($60B)
# Industry ($45-60B = 15-20% of $300B pharma R&D) + Government ($3-6B) + Nonprofits ($2-5B) = $50-71B total
# Market reports ($83B) inflate actual spending by including CRO revenue projections and double-counting
GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL = Parameter(
    60_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.INDUSTRY_CLINICAL_TRIAL_SPENDING_ESTIMATE,
    source_type=SourceType.EXTERNAL,
    description="Annual global spending on clinical trials (Industry: $45-60B + Government: $3-6B + Nonprofits: $2-5B). Conservative estimate using 15-20% of $300B total pharma R&D, not inflated market size projections.",
    display_name="Annual Global Spending on Clinical Trials",
    unit="USD",
    display_value="$60B",
    distribution=DistributionType.LOGNORMAL,
    std_error=10_000_000_000,
    confidence_interval=(50_000_000_000, 75_000_000_000),
    keywords=["60b", "clinical trials", "pharma r&d", "global spending", "research", "industry", "conservative"],
    latex_symbol=r"Spending_{trials}",  # LaTeX symbol for equations
)

GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL = Parameter(
    4_500_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GLOBAL_GOVERNMENT_CLINICAL_TRIAL_SPENDING_ESTIMATE,
    source_type=SourceType.EXTERNAL,
    description="Annual global government spending on interventional clinical trials (~5-10% of total)",
    display_name="Annual Global Government Spending on Clinical Trials",
    unit="USD",
    display_value="$4.5B",
    distribution=DistributionType.LOGNORMAL,
    std_error=1_000_000_000,
    confidence_interval=(3_000_000_000, 6_000_000_000),
    keywords=["4.5b", "clinical trials", "government spending", "nih", "public funding"],
    latex_symbol=r"Spending_{trials,gov}",  # LaTeX symbol for equations
)

NIH_ANNUAL_BUDGET = Parameter(
    47_000_000_000,
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_ref="nih-budget-fy2025",
    source_type=SourceType.EXTERNAL,
    description="NIH annual budget (FY2024/2025)",
    display_name="NIH Annual Budget",
    unit="USD",
    confidence="high",
    confidence_interval=(45_000_000_000, 50_000_000_000),
    keywords=["$47", "47b", "nih", "budget", "annual", "national institutes of health"],
    latex_symbol=r"Budget_{NIH}",  # LaTeX symbol for equations
)

FDA_ANNUAL_PROGRAM_BUDGET = Parameter(
    7_055_869_000,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_ref="fda-fy2026-operating-plan",
    source_type=SourceType.EXTERNAL,
    description="FDA total program level in the FY 2026 operating plan. This is used only for a budget-scale comparison, not as an estimate of FDA cost-effectiveness.",
    display_name="FDA Annual Program Budget",
    unit="USD",
    confidence="high",
    distribution="fixed",
    keywords=["fda", "budget", "annual", "program level", "fy 2026"],
    latex_symbol=r"Budget_{FDA}",
)

NIH_CLINICAL_TRIALS_SPENDING_PCT = Parameter(
    0.033,
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_ref=ReferenceID.NIH_CLINICAL_TRIALS_SPENDING_PCT_3_3,
    source_type=SourceType.EXTERNAL,
    description="Percentage of NIH budget spent on clinical trials (3.3%)",
    display_name="NIH Clinical Trials Spending Percentage",
    unit="percentage",
    display_value="3.3%",
    distribution=DistributionType.BETA,
    confidence_interval=(0.02, 0.05),
    keywords=["3.3%", "nih", "clinical trials", "budget", "percentage"],
    latex_symbol=r"Pct_{NIH,trials}",  # LaTeX symbol for equations
)

MILITARY_TO_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_ref="",
    source_type=SourceType.CALCULATED,
    description="Ratio of global military spending to government clinical trials spending",
    display_name="Ratio of Military to Government Clinical Trials Spending",
    unit="ratio",
    formula="MILITARY_SPENDING / GOVT_CLINICAL_TRIALS_SPENDING",
    keywords=["ratio", "military", "clinical trials", "disparity", "spending", "government"],
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    latex_symbol=r"Ratio_{mil:gov}",  # LaTeX symbol for equations
)

PENTAGON_UNACCOUNTED_FUNDS = Parameter(
    2_460_000_000_000,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_ref=ReferenceID.PENTAGON_UNACCOUNTED_2_5T,
    source_type=SourceType.EXTERNAL,
    description="Funds the Department of Defense has failed to account for across seven consecutive failed audits",
    display_name="Pentagon Unaccounted Funds",
    unit="USD",
    distribution="fixed",
    keywords=["pentagon", "dod", "audit", "misplaced", "unaccounted", "2.46 trillion"],
    latex_symbol=r"Funds_{pentagon,unaccounted}",
)

CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER = Parameter(
    3,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_ref=ReferenceID.DOJ_FALSE_CLAIMS_ACT,
    source_type=SourceType.EXTERNAL,
    description="Treble-damages multiplier from the False Claims Act, used here as the corporate-defendant "
                "analogy for audit and public-money claims in Humanity v. Government.",
    display_name="Corporate Analog False Claims Act Treble Multiplier",
    unit="multiplier",
    distribution="fixed",
    keywords=["corporate", "false claims", "treble damages", "pentagon", "audit", "damages"],
    latex_symbol=r"m_{FCA}",
)

PENTAGON_UNACCOUNTED_FALSE_CLAIMS_ANALOG_EXPOSURE = Parameter(
    PENTAGON_UNACCOUNTED_FUNDS * CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="False Claims Act-style treble-damages exposure on Pentagon unaccounted funds, used as a "
                "corporate-defendant audit analogy rather than a literal claim under existing sovereign law.",
    display_name="Pentagon Unaccounted Funds False Claims Analog Exposure",
    unit="USD",
    formula="PENTAGON_UNACCOUNTED_FUNDS × CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER",
    inputs=["PENTAGON_UNACCOUNTED_FUNDS", "CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER"],
    compute=lambda ctx: (
        ctx["PENTAGON_UNACCOUNTED_FUNDS"]
        * ctx["CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER"]
    ),
    keywords=["pentagon", "false claims", "treble damages", "audit", "corporate", "exposure"],
    latex_symbol=r"Exposure_{pentagon,FCA}",
)

PENTAGON_UNACCOUNTED_CLINICAL_TRIAL_YEARS = Parameter(
    PENTAGON_UNACCOUNTED_FUNDS / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_ref="",
    source_type=SourceType.CALCULATED,
    description="Number of years of clinical trial funding at current government spending levels that the Pentagon's unaccounted funds could have provided",
    display_name="Pentagon Unaccounted Funds in Clinical Trial Years",
    unit="years",
    formula="PENTAGON_UNACCOUNTED_FUNDS / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL",
    inputs=["PENTAGON_UNACCOUNTED_FUNDS", "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    compute=lambda ctx: ctx["PENTAGON_UNACCOUNTED_FUNDS"] / ctx["GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    latex_symbol=r"Years_{pentagon,trials}",
)

# ---
# CENTRAL BANKS CHAPTER: CUMULATIVE SPENDING & CLINICAL TRIAL YEAR CONVERSIONS
# These stats appear in 2+ places and/or are calculated from other params.
# ---

# Cumulative military spending: Fed era (1913-2025)
# Synthesis: SIPRI 1988-2024 (~$65-72T) + Cold War (~$50-70T) + WWI/WWII/interwar (~$33T)
CUMULATIVE_MILITARY_SPENDING_FED_ERA = Parameter(
    170_000_000_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.SIPRI_MILEX_2024,
    source_type="definition",
    confidence="low",
    description="Cumulative global military spending since 1913 (Fed era) in constant 2024 dollars. "
                "Built from: SIPRI 1988-2024 ($65-72T), Cold War 1946-1987 ($50-70T reconstructed), "
                "WWI+WWII+interwar ($33T from Harrison). Range: $150-190T.",
    display_name="Cumulative Military Spending (Fed Era)",
    unit="USD",
    distribution="fixed",
    keywords=["cumulative", "military", "spending", "fed", "century", "total"],
    latex_symbol=r"Spending_{mil,cum,fed}",
)

# Cumulative military spending: all recorded history
CUMULATIVE_MILITARY_SPENDING_ALL_HISTORY = Parameter(
    180_000_000_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.SIPRI_MILEX_2024,
    source_type="definition",
    confidence="low",
    description="Cumulative global military spending across all recorded history in constant 2024 dollars. "
                "Fed era ($170T) + 19th century ($3T) + pre-1800 GDP-share estimate ($4-20T). "
                "Range: $150-225T. 75% was spent after 1945.",
    display_name="Cumulative Military Spending (All History)",
    unit="USD",
    distribution="fixed",
    keywords=["cumulative", "military", "spending", "history", "total", "all time"],
    latex_symbol=r"Spending_{mil,cum,all}",
)

GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL = Parameter(
    GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL - GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="",
    source_type=SourceType.CALCULATED,
    description="Annual global industry spending on clinical trials (Total - Government)",
    display_name="Annual Global Industry Spending on Clinical Trials",
    unit="USD",
    formula="TOTAL_CLINICAL_TRIALS - GOVT_CLINICAL_TRIALS",
    inputs=["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    compute=lambda ctx: ctx["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"] - ctx["GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    latex_symbol=r"Spending_{trials,industry}",  # LaTeX symbol for equations
)

INDUSTRY_VS_GOVERNMENT_CLINICAL_TRIALS_SPENDING_RATIO = Parameter(
    (GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL - GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL) / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
    manual_ref="knowledge/appendix/global-government-medical-research-spending.qmd",
    source_ref=ReferenceID.INDUSTRY_VS_GOVERNMENT_TRIAL_SPENDING_SPLIT,
    source_type=SourceType.CALCULATED,
    description="Ratio of Industry to Government spending on clinical trials (approx 90/10 split)",
    display_name="Ratio of Industry to Government Clinical Trials Spending",
    unit="ratio",
    formula="(TOTAL - GOVT) / GOVT",
    keywords=["ratio", "industry", "government", "clinical trials", "funding"],
    inputs=["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    compute=lambda ctx: (ctx["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"] - ctx["GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"]) / ctx["GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    latex_symbol=r"Ratio_{ind:gov}",  # LaTeX symbol for equations
)

# Total pharma R&D spending (clinical trials are 15-20% of this)
GLOBAL_PHARMA_RD_SPENDING_ANNUAL = Parameter(
    300_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="global-pharma-rd-spending-300b",  # TODO: Add to references.qmd
    source_type=SourceType.EXTERNAL,
    description="Total global pharmaceutical R&D spending ($300B annually, clinical trials represent 15-20% of this total)",
    display_name="Annual Global Pharmaceutical R&D Spending",
    unit="USD",
    display_value="$300B",
    keywords=["pharma", "r&d", "research", "development", "300b", "pharmaceutical", "drug", "industry"],
    latex_symbol=r"Spending_{pharma,RD}",  # LaTeX symbol for equations
)

# Nonprofit clinical trials funding
GLOBAL_NONPROFIT_CLINICAL_TRIALS_SPENDING_ANNUAL = Parameter(
    3_500_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.NONPROFIT_CLINICAL_TRIAL_SPENDING_ESTIMATE,
    source_type=SourceType.EXTERNAL,
    description="Annual global nonprofit spending on clinical trials (foundations, disease advocacy groups)",
    display_name="Annual Global Nonprofit Spending on Clinical Trials",
    unit="USD",
    display_value="$3.5B",
    confidence_interval=(2_000_000_000, 5_000_000_000),
    keywords=["nonprofit", "foundation", "clinical trials", "2-5b", "philanthropy", "advocacy"],
    latex_symbol=r"Spending_{trials,nonprofit}",  # LaTeX symbol for equations
)

# ---
# RESEARCH ACCELERATION MECHANISM PARAMETERS
# ---

# Current System Baseline
CURRENT_TRIALS_PER_YEAR = Parameter(
    3300,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GLOBAL_CLINICAL_TRIALS_MARKET_2024,
    source_type="external",
    description="Current global clinical trials per year",
    display_name="Current Global Clinical Trials per Year",
    unit="trials/year",
    keywords=["3k", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research"],
    distribution="lognormal",  # Count data with right skew; different registries report 3000-4000
    confidence_interval=(2640, 3960),  # ±20% to account for registry counting differences
    latex_symbol=r"Trials_{ann,curr}",  # LaTeX symbol for equations
)  # Global clinical trials per year

CURRENT_DRUG_APPROVALS_PER_YEAR = Parameter(
    50,
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_ref=ReferenceID.GLOBAL_NEW_DRUG_APPROVALS_50_ANNUALLY,
    source_type="external",
    description="Average annual new drug approvals globally",
    display_name="Average Annual New Drug Approvals Globally",
    unit="drugs/year",
    keywords=["worldwide", "yearly", "current", "drug", "approvals", "year", "baseline"],
    distribution="lognormal",  # Count data with right skew
    confidence_interval=(45, 60),  # FDA approval rate varies 45-60/year
    latex_symbol=r"Drugs_{ann,curr}",  # LaTeX symbol for equations
)  # FDA ~50-55/year

# Historical FDA/Drug Development Parameters
OXFORD_RECOVERY_TRIAL_DURATION_MONTHS = Parameter(
    3,
    manual_ref="knowledge/solution/dfda.qmd",
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="external",
    description="Oxford RECOVERY trial duration (found life-saving treatment in 3 months)",
    distribution="fixed",  # Historical fact: exact observed trial duration, not uncertain
    display_name="Oxford RECOVERY Trial Duration",
    unit="months",
    confidence="high",
    keywords=["recovery", "covid", "trial", "timeline", "duration", "oxford", "pragmatic"],
    latex_symbol=r"T_{RECOVERY}",  # LaTeX symbol for equations
)

FDA_PHASE_1_TO_APPROVAL_YEARS = Parameter(
    10.5,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.BIO_CLINICAL_DEVELOPMENT_2021,
    source_type="external",
    description="FDA timeline from Phase 1 start to approval. Derived from BIO 2021 industry survey: Phase 1 (2.3 years) + efficacy lag (8.2 years) = 10.5 years. Consistent with PMC meta-analysis finding 9.1 years median (95% CI: 8.2-10.0).",
    display_name="FDA Phase 1 to Approval Timeline",
    unit="years",
    confidence="high",
    distribution=DistributionType.GAMMA,
    std_error=2.0,  # Timeline variation
    confidence_interval=(6.0, 12.0),
    keywords=["fda", "clinical", "development", "timeline", "approval", "phase 1", "phase 2", "phase 3"],
    latex_symbol=r"T_{FDA}",  # LaTeX symbol for equations
)  # Clinical development + NDA review: 10.5 years (BIO 2021: Phase 1 + efficacy lag)

POST_1962_DRUG_APPROVAL_REDUCTION_PCT = Parameter(
    0.70,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.POST_1962_DRUG_APPROVAL_DROP,
    source_type="external",
    description="Reduction in new drug approvals after 1962 Kefauver-Harris Amendment (70% drop from 43→17 drugs/year)",
    display_name="Post-1962 Drug Approval Reduction",
    unit="percentage",
    confidence="high",
    last_updated="1962-1970",
    keywords=["kefauver", "harris", "amendment", "1962", "regulation", "fda", "approval", "drop", "decline"],
    latex_symbol=r"Reduce_{post62}",  # LaTeX symbol for equations
)


PRE_1962_PHYSICIAN_COUNT = Parameter(
    144_000,
    manual_ref="knowledge/appendix/real-world-evidence-historical-success.qmd",
    source_ref=ReferenceID.PRE_1962_PHYSICIAN_TRIALS,
    source_type="external",
    description="Estimated physicians conducting real-world efficacy trials pre-1962 (unverified estimate)",
    display_name="Pre-1962 Physician Count (Unverified)",
    unit="physicians",
    confidence="low",
    keywords=["pre-1962", "physician", "doctor", "clinical", "trials", "real-world", "evidence"],
    latex_symbol=r"N_{physicians,pre62}",  # LaTeX symbol for equations
)  # Note: Specific "144,000 physicians" figure not verified in sources; AMA opposed amendments but no count documented

# CPI inflation adjustment from 1980 to 2024
CPI_MULTIPLIER_1980_TO_2024 = Parameter(
    3.80,
    manual_ref="knowledge/appendix/drug-development-cost-analysis.qmd",
    source_ref="bls-cpi-inflation-calculator",
    source_type="external",
    description="CPI inflation multiplier from 1980 to 2024 (280.48% cumulative inflation)",
    display_name="CPI Multiplier: 1980 to 2024",
    unit="ratio",
    confidence="high",
    peer_reviewed=False,  # BLS official data
    keywords=["cpi", "inflation", "1980", "2024", "multiplier", "purchasing power", "bls"],
    distribution="normal",
    confidence_interval=(3.75, 3.85),  # Narrow CI for official government data
    latex_symbol=r"CPI_{80-24}",  # LaTeX symbol for equations
)  # BLS CPI data: CPI-U 82.4 (1980) → 313.5 (2024) = 3.80× multiplier; average 3.08% annual inflation

PRE_1962_DRUG_DEVELOPMENT_COST_1980_USD = Parameter(
    6_500_000,
    manual_ref="knowledge/appendix/drug-development-cost-analysis.qmd",
    source_ref="pre-1962-drug-costs-baily-1972",
    source_type="external",
    description="Average drug development cost before 1962 FDA efficacy regulations, adjusted to 1980 dollars (Baily 1972)",
    display_name="Pre-1962 Drug Development Cost (1980 Dollars)",
    unit="USD_1980",
    confidence="high",
    peer_reviewed=True,  # Baily (1972) academic study
    keywords=["pre-1962", "drug", "development", "cost", "1980", "dollars", "historical", "fda", "regulation", "1962", "baily"],
    distribution="lognormal",
    confidence_interval=(5_200_000, 7_800_000),  # ±20% for measurement uncertainty
    latex_symbol=r"Cost_{pre62,80}",  # LaTeX symbol for equations
)  # Baily (1972): $6.5M in 1980 dollars

PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD = Parameter(
    PRE_1962_DRUG_DEVELOPMENT_COST_1980_USD * CPI_MULTIPLIER_1980_TO_2024,  # Calculated value stays in sync with inputs
    manual_ref="knowledge/appendix/drug-development-cost-analysis.qmd",
    source_ref="pre-1962-drug-costs-baily-1972",
    source_type="external",  # Marked as external to avoid Monte Carlo simulation (distribution defined manually below)
    description="Pre-1962 drug development cost adjusted to 2024 dollars ($6.5M × 3.80 = $24.7M, CPI-adjusted from Baily 1972)",
    display_name="Pre-1962 Drug Development Cost (2024 Dollars)",
    unit="USD",
    confidence="high",
    peer_reviewed=True,  # Based on Baily (1972) academic study, inflated to 2024 USD
    keywords=["pre-1962", "drug", "development", "cost", "2024", "dollars", "historical", "fda", "regulation", "1962", "baily", "inflation-adjusted"],
    distribution="lognormal",
    confidence_interval=(19_500_000, 30_000_000),  # Propagated uncertainty: ($5.2M-$7.8M) × (3.75-3.85) = $19.5M-$30.0M
    latex_symbol=r"Cost_{pre62,24}",  # LaTeX symbol for equations
)  # Baily (1972): $6.5M (1980 dollars) × 3.80× CPI multiplier = $24.7M (2024 dollars)

CURRENT_ACTIVE_TRIALS = Parameter(
    10000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.CLINICALTRIALS_GOV_ENROLLMENT_DATA_2025,
    source_type="external",
    description="Current active trials at any given time (3-5 year duration)",
    display_name="Current Active Trials at Any Given Time",
    unit="trials",
    keywords=["10k", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research"],
    latex_symbol=r"Trials_{active}",  # LaTeX symbol for equations
)  # Active trials at any given time (3-5 year duration)

CURRENT_TRIAL_DURATION_YEARS_RANGE = (3, 5)  # Years for large trials
CURRENT_SMALL_TRIAL_RECRUITMENT_MONTHS_RANGE = (6, 18)  # Months to recruit 100 patients

CURRENT_TRIAL_ABANDONMENT_RATE = Parameter(
    0.40,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="clinical-trial-abandonment-rate",
    source_type="external",
    description="Current trial abandonment rate (40% never complete)",
    display_name="Current Trial Abandonment Rate",
    unit="rate",
    keywords=["40%", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research"],
    latex_symbol=r"Rate_{abandon}",  # LaTeX symbol for equations
)  # 40% of trials never complete

CURRENT_TRIAL_SLOTS_AVAILABLE = Parameter(
    1_900_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="global-trial-participant-capacity",
    source_type="external",
    description="Annual global clinical trial participants (IQVIA 2022: 1.9M post-COVID normalization)",
    display_name="Annual Global Clinical Trial Participants",
    unit="patients/year",
    confidence_interval=(1_500_000, 2_300_000),  # ±20% - trial capacity data variable
    distribution="lognormal",
    keywords=["1.9m", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research", "iqvia"],
    latex_symbol=r"Slots_{curr}",  # LaTeX symbol for equations
)  # 1.9M patients/year (IQVIA 2022, post-COVID normalization from 4M peak in 2021)

# Calculated: Cost per participant
CLINICAL_TRIAL_COST_PER_PARTICIPANT_ANNUAL = Parameter(
    GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL / CURRENT_TRIAL_SLOTS_AVAILABLE,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="",
    source_type=SourceType.CALCULATED,
    description="Average annual cost per clinical trial participant (total spending ÷ participants)",
    display_name="Annual Cost Per Clinical Trial Participant",
    unit="USD",
    formula="TOTAL_SPENDING / PARTICIPANTS",    keywords=["cost", "participant", "per patient", "trial cost", "enrollment"],
    inputs=["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "CURRENT_TRIAL_SLOTS_AVAILABLE"],
    compute=lambda ctx: ctx["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"] / ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"],
    latex_symbol=r"Cost_{trial,pt,ann}",  # LaTeX symbol for equations
)

# Calculated: Cost per approved drug (from trials only)
CLINICAL_TRIAL_COST_PER_APPROVED_DRUG = Parameter(
    GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL / CURRENT_DRUG_APPROVALS_PER_YEAR,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="",
    source_type=SourceType.CALCULATED,
    description="Annual clinical trial spending per approved drug (trials only, excluding other R&D costs like discovery, preclinical, manufacturing)",
    display_name="Clinical Trial Cost Per Approved Drug",
    unit="USD",
    formula="TOTAL_TRIAL_SPENDING / NEW_DRUGS",    keywords=["cost", "drug", "approval", "fda", "trial cost"],
    inputs=["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "CURRENT_DRUG_APPROVALS_PER_YEAR"],
    compute=lambda ctx: ctx["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"] / ctx["CURRENT_DRUG_APPROVALS_PER_YEAR"],
    latex_symbol=r"Cost_{trial,drug}",  # LaTeX symbol for equations
)

# Calculated: Military vs ALL clinical trials ratio
MILITARY_TO_CLINICAL_TRIALS_SPENDING_RATIO = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_ref="",
    source_type=SourceType.CALCULATED,
    description="Ratio of global military spending to all clinical trials spending (government + industry + nonprofit)",
    display_name="Ratio of Military to Clinical Trials Spending",
    unit="ratio",
    formula="MILITARY_SPENDING / TOTAL_CLINICAL_TRIALS",    keywords=["ratio", "military", "clinical trials", "disparity", "spending", "misallocation"],
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    latex_symbol=r"Ratio_{mil:trials}",  # LaTeX symbol for equations
)

CURRENT_DISEASE_PATIENTS_GLOBAL = Parameter(
    2_400_000_000,
    manual_ref="knowledge/solution/dfda.qmd",
    source_ref=ReferenceID.DISEASE_PREVALENCE_2_BILLION,
    source_type="external",
    description="Global population with chronic diseases",
    display_name="Global Population with Chronic Diseases",
    unit="people",
    keywords=["2.4b", "participant", "subject", "volunteer", "enrollee", "people", "worldwide"],
    distribution="lognormal",  # Population count with diagnostic/definitional uncertainty
    confidence_interval=(2_000_000_000, 2_800_000_000),  # ±15-17%: GBD methodology + definitional variance
    latex_symbol=r"N_{patients}",  # LaTeX symbol for equations
)  # GBD 2013 study

CURRENT_PATIENT_PARTICIPATION_RATE = Parameter(
    CURRENT_TRIAL_SLOTS_AVAILABLE / CURRENT_DISEASE_PATIENTS_GLOBAL,
    manual_ref="knowledge/problem.qmd",
    source_ref="clinical-trial-patient-participation-rate",
    source_type="calculated",
    description="Current patient participation rate in clinical trials (0.08% = 1.9M participants / 2.4B disease patients)",
    display_name="Current Patient Participation Rate in Clinical Trials",
    unit="rate",
    formula="CURRENT_TRIAL_SLOTS / DISEASE_PATIENTS",
    keywords=["0%", "rct", "participant", "subject", "volunteer", "enrollee", "clinical study"],
    inputs=['CURRENT_TRIAL_SLOTS_AVAILABLE', 'CURRENT_DISEASE_PATIENTS_GLOBAL'],
    compute=lambda ctx: ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"] / ctx["CURRENT_DISEASE_PATIENTS_GLOBAL"],
    latex_symbol=r"Rate_{part}",  # LaTeX symbol for equations
)  # 0.08% of disease patients participate in trials (1.9M / 2.4B, IQVIA 2022)

# Traditional Trial Economics
PHASE_3_TRIAL_COST_MIN = Parameter(
    20_000_000,
    manual_ref="knowledge/appendix/dfda-spec-paper.qmd",
    source_ref=ReferenceID.PHASE_3_COST_PER_TRIAL_RANGE,
    source_type="external",
    description="Phase 3 trial total cost (minimum)",
    display_name="Phase 3 Trial Total Cost (Minimum)",
    unit="USD/trial",
    keywords=["20.0m", "confirmatory trial", "third phase", "rct", "p3", "phase iii", "clinical study"],
    latex_symbol=r"Cost_{P3,min}",  # LaTeX symbol for equations
)  # $20M minimum for Phase 3 trials

# (DFDA_ACTIVE_TRIALS moved to after DFDA_TRIAL_CAPACITY_MULTIPLIER definition)

# =============================================================================
# dFDA DATA STORAGE AND PROCESSING COSTS
# =============================================================================
# Per-patient infrastructure costs for decentralized clinical trials
# Source: knowledge/appendix/data-storage-costs.qmd
# Total typical storage: ~1GB per patient

# Component costs (per patient per month)
DFDA_STORAGE_COST_RAW_PER_PATIENT_MONTHLY = Parameter(
    0.02,
    manual_ref="knowledge/solution/dfda.qmd",
    source_type="definition",
    description="Raw cloud storage cost per patient per month. Based on standard cloud storage rates for ~1GB patient data.",
    display_name="Raw Storage Cost per Patient (Monthly)",
    unit="USD/patient/month",
    confidence_interval=(0.01, 0.05),  # Cloud storage prices vary by provider
    distribution="lognormal",
    keywords=["storage", "cloud", "s3", "azure", "gcp", "data"],
    latex_symbol=r"Cost_{storage,raw}",
)

DFDA_STORAGE_COST_COMPUTE_PER_PATIENT_MONTHLY = Parameter(
    0.20,
    manual_ref="knowledge/solution/dfda.qmd",
    source_type="definition",
    description="Compute and API cost per patient per month. For data processing, correlation analysis, and PIS calculation.",
    display_name="Compute/API Cost per Patient (Monthly)",
    unit="USD/patient/month",
    confidence_interval=(0.10, 0.50),  # Depends on analysis frequency and complexity
    distribution="lognormal",
    keywords=["compute", "api", "processing", "analysis", "pis"],
    latex_symbol=r"Cost_{compute}",
)

DFDA_STORAGE_COST_DATABASE_PER_PATIENT_MONTHLY = Parameter(
    0.30,
    manual_ref="knowledge/solution/dfda.qmd",
    source_type="definition",
    description="Database cost per patient per month. For structured data storage and querying.",
    display_name="Database Cost per Patient (Monthly)",
    unit="USD/patient/month",
    confidence_interval=(0.15, 0.60),  # Database costs vary significantly
    distribution="lognormal",
    keywords=["database", "sql", "postgres", "structured"],
    latex_symbol=r"Cost_{database}",
)

DFDA_STORAGE_COST_BACKUP_PER_PATIENT_MONTHLY = Parameter(
    0.20,
    manual_ref="knowledge/solution/dfda.qmd",
    source_type="definition",
    description="Backup and redundancy cost per patient per month. For data safety and compliance.",
    display_name="Backup/Redundancy Cost per Patient (Monthly)",
    unit="USD/patient/month",
    confidence_interval=(0.10, 0.40),  # Depends on retention policy
    distribution="lognormal",
    keywords=["backup", "redundancy", "disaster recovery", "compliance"],
    latex_symbol=r"Cost_{backup}",
)

# Total monthly cost (calculated from components)
DFDA_STORAGE_COST_TOTAL_PER_PATIENT_MONTHLY = Parameter(
    DFDA_STORAGE_COST_RAW_PER_PATIENT_MONTHLY
    + DFDA_STORAGE_COST_COMPUTE_PER_PATIENT_MONTHLY
    + DFDA_STORAGE_COST_DATABASE_PER_PATIENT_MONTHLY
    + DFDA_STORAGE_COST_BACKUP_PER_PATIENT_MONTHLY,
    manual_ref="knowledge/solution/dfda.qmd",
    source_type="calculated",
    description="Total infrastructure cost per patient per month. Sum of storage, compute, database, and backup costs.",
    display_name="Total Infrastructure Cost per Patient (Monthly)",
    unit="USD/patient/month",
    formula="RAW + COMPUTE + DATABASE + BACKUP",
    inputs=[
        "DFDA_STORAGE_COST_RAW_PER_PATIENT_MONTHLY",
        "DFDA_STORAGE_COST_COMPUTE_PER_PATIENT_MONTHLY",
        "DFDA_STORAGE_COST_DATABASE_PER_PATIENT_MONTHLY",
        "DFDA_STORAGE_COST_BACKUP_PER_PATIENT_MONTHLY",
    ],
    compute=lambda ctx: (
        ctx["DFDA_STORAGE_COST_RAW_PER_PATIENT_MONTHLY"]
        + ctx["DFDA_STORAGE_COST_COMPUTE_PER_PATIENT_MONTHLY"]
        + ctx["DFDA_STORAGE_COST_DATABASE_PER_PATIENT_MONTHLY"]
        + ctx["DFDA_STORAGE_COST_BACKUP_PER_PATIENT_MONTHLY"]
    ),
    keywords=["total", "infrastructure", "monthly", "per patient"],
    latex_symbol=r"Cost_{infra,monthly}",
)  # $0.72/patient/month

# Annual cost (for long-term tracking)
DFDA_STORAGE_COST_TOTAL_PER_PATIENT_ANNUAL = Parameter(
    DFDA_STORAGE_COST_TOTAL_PER_PATIENT_MONTHLY * 12,
    manual_ref="knowledge/solution/dfda.qmd",
    source_type="calculated",
    description="Total infrastructure cost per patient per year. Monthly cost × 12.",
    display_name="Total Infrastructure Cost per Patient (Annual)",
    unit="USD/patient/year",
    formula="MONTHLY_COST × 12",
    inputs=["DFDA_STORAGE_COST_TOTAL_PER_PATIENT_MONTHLY"],
    compute=lambda ctx: ctx["DFDA_STORAGE_COST_TOTAL_PER_PATIENT_MONTHLY"] * 12,
    keywords=["annual", "yearly", "infrastructure", "per patient"],
    latex_symbol=r"Cost_{infra,annual}",
)  # $8.64/patient/year

# Stage 1 observational analysis cost
# Order-of-magnitude estimate validated by FDA Sentinel (~$1/patient/year for similar analysis)
# The exact value matters less than the order-of-magnitude difference vs trials ($500-41,000)
DFDA_OBSERVATIONAL_COST_PER_PATIENT = Parameter(
    0.10,
    manual_ref="knowledge/appendix/dfda-spec-paper.qmd",
    source_type="definition",
    description="Order-of-magnitude estimate for Stage 1 observational signal detection (PIS calculation). Validated by FDA Sentinel benchmark (~$1/patient/year for similar drug safety analysis at 100M+ scale). True cost varies with scale and complexity; exact value less important than order-of-magnitude difference vs pragmatic trials (~$500-929/patient) and traditional Phase 3 (~$41,000/patient).",
    display_name="Stage 1 Observational Analysis Cost per Patient",
    unit="USD/patient",
    confidence_interval=(0.03, 1.00),  # Wide range: pure marginal compute to FDA Sentinel annual
    distribution="lognormal",
    keywords=["observational", "signal detection", "stage 1", "pis", "data analysis", "n-of-1", "fda sentinel"],
    latex_symbol=r"Cost_{obs,pt}",
)  # ~$0.10/patient; FDA Sentinel proves $1/patient/year viable at 100M scale

# =============================================================================
# dFDA TRIAL ECONOMICS (Stage 2)
# =============================================================================

# Stage 2: Pragmatic Trial Confirmation
RECOVERY_TRIAL_COST_PER_PATIENT = Parameter(
    500,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.RECOVERY_COST_500,
    source_type="external",
    description="RECOVERY trial cost per patient. Note: RECOVERY was an outlier - hospital-based during COVID emergency, minimal extra procedures, existing NHS infrastructure, streamlined consent. Replicating this globally will be harder.",
    display_name="Recovery Trial Cost per Patient",
    unit="USD/patient",
    confidence_interval=(400, 2500),  # Widened to reflect implementation challenges:
                                       # - Floor ($400): Best-case RECOVERY-like efficiency
                                       # - Ceiling ($2,500): More typical pragmatic trial costs
                                       # Economist rationale: RECOVERY may not be replicable at scale
                                       # Standard pragmatic trials cost $2k-$5k/patient
    distribution="lognormal",
    keywords=["rct", "participant", "subject", "volunteer", "enrollee", "clinical study", "clinical trial"],
    latex_symbol=r"Cost_{RECOVERY,pt}",  # LaTeX symbol for equations
)  # RECOVERY achieved $500, but scaling globally may cost more

# ADAPTABLE Trial - PCORnet's First Large-Scale Pragmatic Trial
# Source: PCORI 2015 award ($14M grant), PCORnet summary (15,076 patients)
# Note: $14M is the PCORI grant; true costs may be 10-40% higher with in-kind contributions
ADAPTABLE_TRIAL_TOTAL_COST = Parameter(
    14_000_000,  # $14M PCORI grant (floor estimate)
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
    source_type="external",
    description="PCORI grant for ADAPTABLE trial (2016-2019). Note: Direct funding only; total costs including site overhead and in-kind contributions from health systems may be higher.",
    display_name="ADAPTABLE Trial Total Cost",
    unit="USD",
    confidence="medium",  # Medium: in-kind costs not included in $14M figure
    confidence_interval=(14_000_000, 20_000_000),  # Grant to estimated true cost
    distribution="lognormal",
    keywords=["adaptable", "pcornet", "pragmatic", "trial", "cost"],
    latex_symbol=r"Cost_{ADAPT}",  # LaTeX symbol for equations
)

ADAPTABLE_TRIAL_PATIENTS = Parameter(
    15076,  # 15,076 patients enrolled (precise count)
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
    source_type="definition",  # Precise count, no uncertainty
    description="Patients enrolled in ADAPTABLE trial (PCORnet 2016-2019). Enrolled across 40 clinical sites. Precise count from trial completion records.",
    display_name="ADAPTABLE Trial Patients Enrolled",
    unit="patients",
    confidence="high",
    keywords=["adaptable", "pcornet", "enrollment", "patients"],
    latex_symbol=r"N_{ADAPT}",  # LaTeX symbol for equations
)

ADAPTABLE_TRIAL_COST_PER_PATIENT = Parameter(
    929,  # $14M / 15,076 patients = $929/patient
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
    source_type="external",
    description="Cost per patient in ADAPTABLE trial ($14M PCORI grant / 15,076 patients). Note: This is the direct grant cost; true cost including in-kind may be 10-40% higher.",
    display_name="ADAPTABLE Trial Cost per Patient",
    unit="USD/patient",
    confidence="medium",
    confidence_interval=(929, 1400),  # Grant cost to estimated true cost with in-kind
    distribution="lognormal",
    keywords=["adaptable", "pcornet", "cost per patient", "pragmatic"],
    latex_symbol=r"Cost_{ADAPT,pt}",  # LaTeX symbol for equations
)  # $929/patient from PCORI grant; up to ~$1,400 with in-kind

# dFDA Pragmatic Trial Cost - Based on ADAPTABLE Trial (DELIBERATELY CONSERVATIVE)
# Harvard review of 108 embedded pragmatic trials (Ramsberg & Platt 2018); 64 had cost data, median $97/patient
# We use ADAPTABLE ($929) - a 10x more conservative estimate for credibility
# Reference: embedded-pragmatic-trials-meta-analysis in references.qmd
# Central estimate uses ADAPTABLE's empirical cost ($929)
# Meta-analysis shows median is only $97 - we use the HIGHER value for credibility
# This means our projections likely UNDERSTATE the true potential by ~10x
DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT = Parameter(
    929,  # ADAPTABLE trial empirical cost - CONSERVATIVE choice
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
    source_type="external",
    description="Embedded pragmatic trial cost per patient. Uses ADAPTABLE trial ($929) as DELIBERATELY CONSERVATIVE central estimate. Ramsberg & Platt (2018) reviewed 108 embedded pragmatic trials; 64 with cost data had median of only $97/patient - this estimate may overstate costs by 10x. Confidence interval spans meta-analysis median to complex chronic disease trials.",
    display_name="Pragmatic Trial Cost per Patient",
    unit="USD/patient",
    confidence="medium",
    keywords=["dfda", "pragmatic", "trial", "cost", "per patient", "pcornet", "adaptable", "conservative"],
    distribution="lognormal",
    confidence_interval=(97, 3000),  # Evidence-based range:
                                      # - Floor ($97): Meta-analysis median (64 trials with cost data, out of 108 reviewed)
                                      # - Central ($929): ADAPTABLE trial (conservative choice)
                                      # - Ceiling ($3,000): Complex chronic disease trials
    latex_symbol=r"Cost_{pragmatic,pt}",  # LaTeX symbol for equations
)  # Central = ADAPTABLE (conservative); meta-analysis suggests $97 median

# Traditional Phase 3 Cost (baseline for comparison)
TRADITIONAL_PHASE3_COST_PER_PATIENT = Parameter(
    41000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.TRIAL_COSTS_FDA_STUDY,
    source_type="external",
    description="Phase 3 cost per patient (median from FDA study)",
    display_name="Phase 3 Cost per Patient",
    unit="USD/patient",
    distribution=DistributionType.LOGNORMAL,  # Right-skewed: simple trials ~$20K, complex ~$120K+
    confidence_interval=(20000, 120000),  # Range from Moore et al. 2020 FDA study
    keywords=["41k", "confirmatory trial", "third phase", "rct", "participant", "subject", "volunteer", "median"],
    latex_symbol=r"Cost_{P3,pt}",  # LaTeX symbol for equations
)  # Median cost per patient from FDA/JAMA study (Moore et al. 2020)

# Trial Cost Reduction Factors (calculated from cost per patient comparisons)

# RECOVERY Trial Cost Reduction (historical evidence)
RECOVERY_TRIAL_COST_REDUCTION_FACTOR = Parameter(
    TRADITIONAL_PHASE3_COST_PER_PATIENT / RECOVERY_TRIAL_COST_PER_PATIENT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="calculated",
    description="Cost reduction factor demonstrated by RECOVERY trial (traditional Phase 3 cost / RECOVERY cost per patient)",
    display_name="RECOVERY Trial Cost Reduction Factor",
    unit="multiplier",
    formula="TRADITIONAL_PHASE3_COST / RECOVERY_COST",    keywords=["oxford", "recovery", "82x", "rct", "clinical trial", "cost reduction", "historical"],
    inputs=['TRADITIONAL_PHASE3_COST_PER_PATIENT', 'RECOVERY_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"] / ctx["RECOVERY_TRIAL_COST_PER_PATIENT"],
    latex_symbol=r"k_{RECOVERY}",  # LaTeX symbol for equations
)

# Pragmatic Trial Cost Reduction (forward-looking projection)
DFDA_TRIAL_COST_REDUCTION_FACTOR = Parameter(
    TRADITIONAL_PHASE3_COST_PER_PATIENT / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Cost reduction factor projected for embedded pragmatic trials (traditional Phase 3 cost / pragmatic trial cost per patient)",
    display_name="Pragmatic Trial Cost Reduction Factor",
    unit="multiplier",
    formula="TRADITIONAL_PHASE3_COST / PRAGMATIC_TRIAL_COST",    keywords=["pragmatic", "rct", "clinical trial", "cost reduction", "projected"],
    inputs=['TRADITIONAL_PHASE3_COST_PER_PATIENT', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    latex_symbol=r"k_{reduce}",  # LaTeX symbol for equations
)

# Pragmatic Trial Cost Reduction as Percentage (derived from factor)
DFDA_TRIAL_COST_REDUCTION_PCT = Parameter(
    1 - (DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT / TRADITIONAL_PHASE3_COST_PER_PATIENT),
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Trial cost reduction percentage: 1 - (pragmatic trial cost / traditional Phase 3 cost)",
    display_name="Pragmatic Trial Cost Reduction Percentage",
    unit="percentage",
    formula="1 - (PRAGMATIC_TRIAL_COST / TRADITIONAL_COST)",
    # RECOVERY trial achieved higher reduction (98.8%), so this is conservative relative to historical evidence
    validation_min=0.90,   # Floor: 90% reduction (minimum based on RECOVERY-like efficiency)
    validation_max=0.99,   # Ceiling: 99% reduction (approaching theoretical maximum)
    inputs=["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT", "TRADITIONAL_PHASE3_COST_PER_PATIENT"],
    compute=lambda ctx: 1 - (ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"] / ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"]),
    keywords=["97%", "rct", "clinical study", "clinical trial", "cost reduction", "research trial", "randomized controlled trial"],
    latex_symbol=r"Reduce_{pct}",  # LaTeX symbol for equations
)

ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE = Parameter(
    0.861,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.ANTIDEPRESSANT_TRIAL_EXCLUSION_RATES,
    source_type="external",
    description="Mean exclusion rate in antidepressant trials (86.1% of real-world patients excluded)",
    display_name="Antidepressant Trial Exclusion Rate",
    unit="percentage",
    keywords=["exclusion", "trial", "antidepressant", "eligibility", "real-world", "pragmatic"],
    latex_symbol=r"Rate_{excl}",  # LaTeX symbol for equations
)

PRE_1962_VALIDATION_YEARS = Parameter(
    77,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.LIFE_EXPECTANCY_INCREASE_PRE_1962,
    source_type="definition",
    description="Years of empirical validation for physician-led pragmatic trials (1883-1960)",
    display_name="Pre-1962 Validation Years",
    unit="years",
    formula="1960 - 1883",
    keywords=["pre-1962", "historical", "validation", "physician", "trials", "life expectancy"],
    latex_symbol=r"T_{validate,pre62}",  # LaTeX symbol for equations
)

# Life Expectancy Data Points - Historical Evidence for Regulatory Impact
# Source: knowledge/data/us-life-expectancy-fda-budget-1543-2019.csv
# Uncertainty: ±0.5 years for historical census/vital statistics data

US_LIFE_EXPECTANCY_1880 = Parameter(
    39.41,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.LIFE_EXPECTANCY_INCREASE_PRE_1962,
    source_type="external",
    description="US life expectancy in 1880 (closest available data point to 1883).",
    display_name="US Life Expectancy (1880)",
    unit="years",
    confidence="high",
    confidence_interval=(38.9, 39.9),
    distribution="normal",
    peer_reviewed=True,
    keywords=["life expectancy", "1880", "historical", "baseline"],
    latex_symbol=r"LE_{US,1880}",  # LaTeX symbol for equations
)

US_LIFE_EXPECTANCY_1962 = Parameter(
    70.064,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.LIFE_EXPECTANCY_INCREASE_PRE_1962,
    source_type="external",
    description="US life expectancy in 1962 (year of Kefauver-Harris Amendments).",
    display_name="US Life Expectancy (1962)",
    unit="years",
    confidence="high",
    confidence_interval=(69.8, 70.3),
    distribution="normal",
    peer_reviewed=True,
    keywords=["life expectancy", "1962", "kefauver-harris", "baseline"],
    latex_symbol=r"LE_{US,1962}",  # LaTeX symbol for equations
)

US_LIFE_EXPECTANCY_2019 = Parameter(
    78.862,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.POST_1962_LIFE_EXPECTANCY_SLOWDOWN,
    source_type="external",
    description="US life expectancy in 2019 (latest available data).",
    display_name="US Life Expectancy (2019)",
    unit="years",
    confidence="high",
    confidence_interval=(78.6, 79.1),
    distribution="normal",
    peer_reviewed=True,
    keywords=["life expectancy", "2019", "current", "baseline"],
    latex_symbol=r"LE_{US,2019}",  # LaTeX symbol for equations
)

# Life Expectancy Gain Rates - Calculated from data points
LIFE_EXPECTANCY_GAIN_1883_1962_YEARS_PER_DECADE = Parameter(
    (US_LIFE_EXPECTANCY_1962 - US_LIFE_EXPECTANCY_1880) / 7.9,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.LIFE_EXPECTANCY_INCREASE_PRE_1962,
    source_type="calculated",
    description="US life expectancy linear gain rate 1883-1962 (pre-Kefauver-Harris).",
    display_name="Life Expectancy Gain Rate (1883-1962)",
    unit="years/decade",
    formula="(life_exp_1962 - life_exp_1880) / 7.9 decades",
    confidence="high",
    peer_reviewed=True,
    keywords=["life expectancy", "pre-1962", "historical", "biomedical progress", "years per decade"],
    inputs=["US_LIFE_EXPECTANCY_1962", "US_LIFE_EXPECTANCY_1880"],
    compute=lambda ctx: (ctx["US_LIFE_EXPECTANCY_1962"] - ctx["US_LIFE_EXPECTANCY_1880"]) / 7.9,
    latex_symbol=r"\Delta LE_{pre62}",  # LaTeX symbol for equations
)

LIFE_EXPECTANCY_GAIN_1962_2019_YEARS_PER_DECADE = Parameter(
    (US_LIFE_EXPECTANCY_2019 - US_LIFE_EXPECTANCY_1962) / 5.7,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.POST_1962_LIFE_EXPECTANCY_SLOWDOWN,
    source_type="calculated",
    description="US life expectancy linear gain rate 1962-2019 (post-Kefauver-Harris).",
    display_name="Life Expectancy Gain Rate (1962-2019)",
    unit="years/decade",
    formula="(life_exp_2019 - life_exp_1962) / 5.7 decades",
    confidence="high",
    peer_reviewed=True,
    keywords=["life expectancy", "post-1962", "slowdown", "biomedical progress", "years per decade", "kefauver-harris"],
    inputs=["US_LIFE_EXPECTANCY_2019", "US_LIFE_EXPECTANCY_1962"],
    compute=lambda ctx: (ctx["US_LIFE_EXPECTANCY_2019"] - ctx["US_LIFE_EXPECTANCY_1962"]) / 5.7,
    latex_symbol=r"\Delta LE_{post62}",  # LaTeX symbol for equations
    distribution="fixed",  # Narrow CIs on both LE inputs; variance is sub-tolerance
)

# Research Acceleration Multipliers - MOVED to after GLOBAL_MED_RESEARCH_SPENDING (line ~2971)
# See calculation block after TOTAL_RESEARCH_FUNDING_WITH_TREATY

# (DFDA_COMPLETED_TRIALS_PER_YEAR moved to after DFDA_TRIALS_PER_YEAR_CAPACITY definition)

# ===================================================================
# THERAPEUTIC FRONTIER - Drug Discovery Space Analysis
# ===================================================================
# Quantifies the unexplored space of potential drug-disease combinations
# using existing safe compounds (FDA-approved + GRAS substances).
# Shows that <1% of testable combinations have been explored.
# ===================================================================

# Input parameters: Safe compound counts from external sources

FDA_APPROVED_PRODUCTS_COUNT = Parameter(
    20_000,
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_ref=ReferenceID.FDA_APPROVED_PRODUCTS_20K,
    source_type="external",
    description="Total FDA-approved drug products in the U.S.",
    display_name="FDA-Approved Drug Products",
    unit="products",
    keywords=["fda", "approved", "drugs", "products", "pharmaceuticals", "medicines"],
    latex_symbol=r"N_{FDA,products}",  # LaTeX symbol for equations
)

FDA_APPROVED_UNIQUE_ACTIVE_INGREDIENTS = Parameter(
    1_650,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_ref=ReferenceID.FDA_APPROVED_PRODUCTS_20K,
    source_type="external",
    description="Unique active pharmaceutical ingredients in FDA-approved products (midpoint of 1,300-2,000 range)",
    display_name="FDA-Approved Unique Active Ingredients",
    unit="compounds",
    keywords=["fda", "active ingredients", "unique", "pharmaceutical", "compounds"],
    confidence_interval=(1_300, 2_000),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{FDA,ingredients}",  # LaTeX symbol for equations
)

PHASE_1_PASSED_COMPOUNDS_GLOBAL = Parameter(
    7_500,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_ref=ReferenceID.BIO_CLINICAL_DEVELOPMENT_2021,
    source_type="external",
    description="Investigational compounds that have passed Phase I globally (midpoint of 5,000-10,000 range)",
    display_name="Phase I-Passed Compounds Globally",
    unit="compounds",
    keywords=["phase 1", "clinical trials", "investigational", "pipeline", "drug development"],
    confidence_interval=(5_000, 10_000),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{P1,passed}",  # LaTeX symbol for equations
)

FDA_GRAS_SUBSTANCES_COUNT = Parameter(
    635,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_ref=ReferenceID.FDA_GRAS_LIST_COUNT,
    source_type="external",
    description="FDA Generally Recognized as Safe (GRAS) substances (midpoint of 570-700 range)",
    display_name="FDA GRAS Substances",
    unit="substances",
    keywords=["gras", "fda", "safe", "food additives", "supplements"],
    confidence_interval=(570, 700),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{GRAS}",  # LaTeX symbol for equations
)

# Calculated: Total safe compounds available for repurposing

SAFE_COMPOUNDS_COUNT = Parameter(
    9_500,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="definition",
    description="Total safe compounds available for repurposing (FDA-approved + GRAS substances, midpoint of 7,000-12,000 range)",
    display_name="Safe Compounds Available for Testing",
    unit="compounds",
    keywords=["safe", "compounds", "repurposing", "drug discovery", "therapeutic frontier", "fda", "gras"],
    confidence_interval=(7_000, 12_000),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{safe}",  # LaTeX symbol for equations
)

# Input parameters: Disease targets

ICD_10_TOTAL_CODES = Parameter(
    14_000,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_ref=ReferenceID.ICD_10_CODE_COUNT,
    source_type="external",
    description="Total ICD-10 diagnostic codes for human diseases and conditions",
    display_name="ICD-10 Total Codes",
    unit="codes",
    keywords=["icd-10", "disease", "diagnosis", "medical codes", "classification"],
    latex_symbol=r"N_{ICD10}",  # LaTeX symbol for equations
)

TRIAL_RELEVANT_DISEASES_COUNT = Parameter(
    1_000,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="definition",
    description="Consolidated count of trial-relevant diseases worth targeting (after grouping ICD-10 codes)",
    display_name="Trial-Relevant Diseases",
    unit="diseases",
    keywords=["disease", "targets", "clinical trials", "therapeutic", "conditions"],
    confidence_interval=(800, 1_200),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{diseases,trial}",  # LaTeX symbol for equations
)

# Calculated: Combinatorial space

DRUG_DISEASE_COMBINATIONS_POSSIBLE = Parameter(
    SAFE_COMPOUNDS_COUNT * TRIAL_RELEVANT_DISEASES_COUNT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total possible drug-disease combinations using existing safe compounds",
    display_name="Possible Drug-Disease Combinations",
    unit="combinations",
    formula="SAFE_COMPOUNDS × DISEASES",
    keywords=["combinatorial space", "drug-disease", "therapeutic frontier", "unexplored", "potential"],
    inputs=["SAFE_COMPOUNDS_COUNT", "TRIAL_RELEVANT_DISEASES_COUNT"],
    compute=lambda ctx: ctx["SAFE_COMPOUNDS_COUNT"] * ctx["TRIAL_RELEVANT_DISEASES_COUNT"],
    latex_symbol=r"N_{combos}",  # LaTeX symbol for equations
)

# Input parameters: What's been tested

APPROVED_DRUG_DISEASE_PAIRINGS = Parameter(
    1_750,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="definition",
    description="Unique approved drug-disease pairings (FDA-approved uses, midpoint of 1,500-2,000 range)",
    display_name="Approved Drug-Disease Pairings",
    unit="pairings",
    keywords=["approved", "indications", "drug-disease", "fda", "uses"],
    confidence_interval=(1_500, 2_000),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{approved}",  # LaTeX symbol for equations
)

DRUG_REPURPOSING_SUCCESS_RATE = Parameter(
    0.30,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.DRUG_REPURPOSING_RATE,
    source_type="external",
    description="Percentage of drugs that gain at least one new indication after initial approval",
    display_name="Drug Repurposing Success Rate",
    unit="percentage",
    keywords=["repurposing", "new indications", "drug discovery", "success rate"],
    latex_symbol=r"Rate_{repurpose}",  # LaTeX symbol for equations
)

TESTED_RELATIONSHIPS_ESTIMATE = Parameter(
    32_500,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="definition",
    description="Estimated drug-disease relationships actually tested (approved uses + repurposed + failed trials, midpoint of 15,000-50,000 range)",
    display_name="Tested Drug-Disease Relationships",
    unit="relationships",
    keywords=["tested", "clinical trials", "drug-disease", "explored", "research"],
    confidence_interval=(15_000, 50_000),
    distribution=DistributionType.LOGNORMAL,
    latex_symbol=r"N_{tested}",  # LaTeX symbol for equations
)

# Calculated: Exploration ratio

EXPLORATION_RATIO = Parameter(
    TESTED_RELATIONSHIPS_ESTIMATE / DRUG_DISEASE_COMBINATIONS_POSSIBLE,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Fraction of possible drug-disease space actually tested (<1%)",
    display_name="Therapeutic Frontier Exploration Ratio",
    unit="percentage",
    formula="TESTED / POSSIBLE",    keywords=["exploration", "untapped", "therapeutic frontier", "unexplored", "discovery"],
    inputs=["TESTED_RELATIONSHIPS_ESTIMATE", "DRUG_DISEASE_COMBINATIONS_POSSIBLE"],
    compute=lambda ctx: ctx["TESTED_RELATIONSHIPS_ESTIMATE"] / ctx["DRUG_DISEASE_COMBINATIONS_POSSIBLE"],
    latex_symbol=r"Ratio_{explore}",  # LaTeX symbol for equations
)

UNEXPLORED_RATIO = Parameter(
    1 - (TESTED_RELATIONSHIPS_ESTIMATE / DRUG_DISEASE_COMBINATIONS_POSSIBLE),
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_type="calculated",
    description="Fraction of possible drug-disease space that remains unexplored (>99%)",
    display_name="Unexplored Therapeutic Frontier",
    unit="percentage",
    formula="1 - EXPLORATION_RATIO",
    keywords=["unexplored", "untapped", "therapeutic frontier", "opportunity", "discovery"],
    inputs=["TESTED_RELATIONSHIPS_ESTIMATE", "DRUG_DISEASE_COMBINATIONS_POSSIBLE"],
    compute=lambda ctx: 1 - (ctx["TESTED_RELATIONSHIPS_ESTIMATE"] / ctx["DRUG_DISEASE_COMBINATIONS_POSSIBLE"]),
    latex_symbol=r"Ratio_{unexplored}",  # LaTeX symbol for equations
)

# =============================================================================
# THERAPEUTIC SPACE: EMERGING MODALITIES (Tier 2)
# =============================================================================
# Beyond known safe small molecules, emerging modalities vastly expand the
# therapeutic frontier: gene therapies, mRNA, epigenetics, cell therapies.

HUMAN_PROTEIN_CODING_GENES = Parameter(
    20_000,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="definition",
    description="Human protein-coding genes targetable by gene therapy, mRNA, or biologics (Human Genome Project consensus)",
    display_name="Human Protein-Coding Genes",
    unit="genes",
    keywords=["genes", "genome", "protein", "targets", "gene therapy", "mRNA"],
    confidence_interval=(19_000, 21_000),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{genes}",  # LaTeX symbol for equations
)

GENE_THERAPY_DISEASE_COMBINATIONS = Parameter(
    HUMAN_PROTEIN_CODING_GENES * TRIAL_RELEVANT_DISEASES_COUNT,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Gene therapy target-disease combinations (CRISPR, base editing, viral vectors)",
    display_name="Gene Therapy Combinations",
    unit="combinations",
    formula="GENES × DISEASES",
    keywords=["gene therapy", "crispr", "base editing", "combinations", "therapeutic frontier"],
    inputs=["HUMAN_PROTEIN_CODING_GENES", "TRIAL_RELEVANT_DISEASES_COUNT"],
    compute=lambda ctx: ctx["HUMAN_PROTEIN_CODING_GENES"] * ctx["TRIAL_RELEVANT_DISEASES_COUNT"],
    latex_symbol=r"Combos_{gene}",  # LaTeX symbol for equations
)

MRNA_THERAPEUTIC_COMBINATIONS = Parameter(
    HUMAN_PROTEIN_CODING_GENES * TRIAL_RELEVANT_DISEASES_COUNT,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="mRNA therapeutic combinations (protein replacement, vaccines, enzyme delivery)",
    display_name="mRNA Therapeutic Combinations",
    unit="combinations",
    formula="PROTEINS × DISEASES",
    keywords=["mrna", "rna", "protein replacement", "combinations", "therapeutic frontier"],
    inputs=["HUMAN_PROTEIN_CODING_GENES", "TRIAL_RELEVANT_DISEASES_COUNT"],
    compute=lambda ctx: ctx["HUMAN_PROTEIN_CODING_GENES"] * ctx["TRIAL_RELEVANT_DISEASES_COUNT"],
    latex_symbol=r"Combos_{mRNA}",  # LaTeX symbol for equations
)

EPIGENETIC_TARGETS_COUNT = Parameter(
    1_500,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="definition",
    description="Druggable epigenetic targets (HDACs, DNMTs, histone modifiers, bromodomains)",
    display_name="Epigenetic Drug Targets",
    unit="targets",
    keywords=["epigenetic", "hdac", "dnmt", "histone", "chromatin", "reprogramming"],
    confidence_interval=(1_000, 2_000),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{epi}",  # LaTeX symbol for equations
)

EPIGENETIC_DISEASE_COMBINATIONS = Parameter(
    EPIGENETIC_TARGETS_COUNT * TRIAL_RELEVANT_DISEASES_COUNT,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Epigenetic reprogramming target-disease combinations",
    display_name="Epigenetic Therapy Combinations",
    unit="combinations",
    formula="EPIGENETIC_TARGETS × DISEASES",
    keywords=["epigenetic", "reprogramming", "combinations", "therapeutic frontier"],
    inputs=["EPIGENETIC_TARGETS_COUNT", "TRIAL_RELEVANT_DISEASES_COUNT"],
    compute=lambda ctx: ctx["EPIGENETIC_TARGETS_COUNT"] * ctx["TRIAL_RELEVANT_DISEASES_COUNT"],
    latex_symbol=r"Combos_{epi}",  # LaTeX symbol for equations
)

CELL_THERAPY_APPROACHES = Parameter(
    500,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="definition",
    description="Distinct cell therapy approaches (CAR-T variants, iPSCs, MSCs, organoids)",
    display_name="Cell Therapy Approaches",
    unit="approaches",
    keywords=["cell therapy", "car-t", "ipsc", "stem cell", "msc", "organoid"],
    confidence_interval=(300, 800),
    distribution=DistributionType.UNIFORM,
    latex_symbol=r"N_{cell}",  # LaTeX symbol for equations
)

CELL_THERAPY_DISEASE_COMBINATIONS = Parameter(
    CELL_THERAPY_APPROACHES * TRIAL_RELEVANT_DISEASES_COUNT,
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Cell therapy approach-disease combinations",
    display_name="Cell Therapy Combinations",
    unit="combinations",
    formula="CELL_APPROACHES × DISEASES",
    keywords=["cell therapy", "combinations", "therapeutic frontier"],
    inputs=["CELL_THERAPY_APPROACHES", "TRIAL_RELEVANT_DISEASES_COUNT"],
    compute=lambda ctx: ctx["CELL_THERAPY_APPROACHES"] * ctx["TRIAL_RELEVANT_DISEASES_COUNT"],
    latex_symbol=r"Combos_{cell}",  # LaTeX symbol for equations
)

# Total emerging modalities
EMERGING_MODALITY_COMBINATIONS = Parameter(
    int(GENE_THERAPY_DISEASE_COMBINATIONS) + int(MRNA_THERAPEUTIC_COMBINATIONS) +
    int(EPIGENETIC_DISEASE_COMBINATIONS) + int(CELL_THERAPY_DISEASE_COMBINATIONS),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Total emerging modality combinations (gene therapy + mRNA + epigenetics + cell therapy)",
    display_name="Emerging Modality Combinations",
    unit="combinations",
    formula="GENE + MRNA + EPIGENETIC + CELL",
    keywords=["emerging", "modalities", "gene therapy", "mrna", "epigenetic", "cell therapy", "total"],
    inputs=["GENE_THERAPY_DISEASE_COMBINATIONS", "MRNA_THERAPEUTIC_COMBINATIONS",
            "EPIGENETIC_DISEASE_COMBINATIONS", "CELL_THERAPY_DISEASE_COMBINATIONS"],
    compute=lambda ctx: (ctx["GENE_THERAPY_DISEASE_COMBINATIONS"] +
                         ctx["MRNA_THERAPEUTIC_COMBINATIONS"] +
                         ctx["EPIGENETIC_DISEASE_COMBINATIONS"] +
                         ctx["CELL_THERAPY_DISEASE_COMBINATIONS"]),
    latex_symbol=r"N_{emerging}",  # LaTeX symbol for equations
)

# Total testable therapeutic space (Tier 1 + Tier 2)
TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS = Parameter(
    float(DRUG_DISEASE_COMBINATIONS_POSSIBLE) + float(EMERGING_MODALITY_COMBINATIONS),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Total testable therapeutic combinations (known safe compounds + emerging modalities)",
    display_name="Total Testable Therapeutic Space",
    unit="combinations",
    formula="KNOWN_SAFE + EMERGING_MODALITIES",
    keywords=["total", "testable", "therapeutic", "combinations", "frontier", "all modalities"],
    inputs=["DRUG_DISEASE_COMBINATIONS_POSSIBLE", "EMERGING_MODALITY_COMBINATIONS"],
    compute=lambda ctx: ctx["DRUG_DISEASE_COMBINATIONS_POSSIBLE"] + ctx["EMERGING_MODALITY_COMBINATIONS"],
    latex_symbol=r"N_{testable}",  # LaTeX symbol for equations
)

# =============================================================================
# COMBINATION THERAPY SPACE
# =============================================================================
# Pairwise combinations of known safe compounds - highly defensible because
# combination therapy is standard practice in oncology, HIV, cardiology, etc.

COMBINATION_THERAPY_PAIRS = Parameter(
    int(SAFE_COMPOUNDS_COUNT * (SAFE_COMPOUNDS_COUNT - 1) / 2),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Unique pairwise drug combinations from known safe compounds (n choose 2)",
    display_name="Pairwise Drug Combinations",
    unit="combinations",
    formula="SAFE_COMPOUNDS_COUNT × (SAFE_COMPOUNDS_COUNT - 1) ÷ 2",
    latex=r"N_{combo} = \frac{N_{safe} \cdot (N_{safe} - 1)}{2}",
    keywords=["combination", "pairwise", "polypharmacy", "multi-drug", "synergy"],
    inputs=["SAFE_COMPOUNDS_COUNT"],
    compute=lambda ctx: ctx["SAFE_COMPOUNDS_COUNT"] * (ctx["SAFE_COMPOUNDS_COUNT"] - 1) / 2,
    latex_symbol=r"N_{combo}",  # LaTeX symbol for equations
)

COMBINATION_THERAPY_DISEASE_SPACE = Parameter(
    float(COMBINATION_THERAPY_PAIRS) * float(TRIAL_RELEVANT_DISEASES_COUNT),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total combination therapy space (pairwise drug combinations × diseases). Standard in oncology, HIV, cardiology.",
    display_name="Combination Therapy Space",
    unit="combinations",
    formula="DRUG_PAIRS × DISEASES",
    keywords=["combination", "therapy", "space", "polypharmacy", "frontier"],
    inputs=["COMBINATION_THERAPY_PAIRS", "TRIAL_RELEVANT_DISEASES_COUNT"],
    compute=lambda ctx: ctx["COMBINATION_THERAPY_PAIRS"] * ctx["TRIAL_RELEVANT_DISEASES_COUNT"],
    latex_symbol=r"Space_{combo}",  # LaTeX symbol for equations
)

# Additional context: Biological targets

HUMAN_INTERACTOME_TARGETED_PCT = Parameter(
    0.12,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.CLINICAL_TRIALS_PUZZLE_INTERACTOME,
    source_type="external",
    description="Percentage of human interactome (protein-protein interactions) targeted by drugs",
    display_name="Human Interactome Targeted by Drugs",
    unit="percentage",
    keywords=["interactome", "targets", "proteins", "biology", "drug discovery", "untapped"],
    latex_symbol=r"Pct_{interactome}",  # LaTeX symbol for equations
)

# Pragmatic trial platform operational costs
DFDA_UPFRONT_BUILD = Parameter(
    40_000_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="definition",
    description="Pragmatic trial platform one-time build cost (central estimate)",
    display_name="Pragmatic Trial Platform One-Time Build Cost",
    unit="USD",
    keywords=["40.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    latex_symbol=r"Cost_{build}",  # LaTeX symbol for equations
)  # $40M one-time build cost

DFDA_UPFRONT_BUILD_MAX = Parameter(
    46_000_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="definition",
    description="Pragmatic trial platform one-time build cost (high estimate)",
    display_name="Pragmatic Trial Platform One-Time Build Cost (Maximum)",
    unit="USD",
    keywords=["46.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    latex_symbol=r"Cost_{build,max}",  # LaTeX symbol for equations
)  # $46M one-time build cost (high end)

# DCT Platform Funding Comparables
DCT_PLATFORM_FUNDING_MEDIUM = Parameter(
    500_000_000,
    manual_ref="knowledge/solution/dfda.qmd",
    source_type="definition",
    description="Mid-range funding for commercial DCT platform",
    display_name="Mid-Range Funding for Commercial Dct Platform",
    unit="USD",
    keywords=["500.0m", "pragmatic trials", "real world evidence", "capital", "finance", "money", "decentralized trials"],
    latex_symbol=r"Funding_{DCT}",  # LaTeX symbol for equations
)  # $500M funding for commercial platforms

# Per-patient cost in dollars (not billions)
DFDA_TARGET_COST_PER_PATIENT_USD = Parameter(
    1000,
    manual_ref="knowledge/solution.qmd",
    source_type="definition",
    description="Target pragmatic trial cost per patient in USD",
    display_name="Target Pragmatic Trial Cost per Patient",
    unit="USD/patient",
    keywords=["1k", "pragmatic trials", "real world evidence", "participant", "subject", "volunteer", "enrollee"],
    latex_symbol=r"Cost_{target,pt}",  # LaTeX symbol for equations
)  # $1,000 per patient

# Pragmatic trial platform operational cost breakdown (in dollars)
DFDA_OPEX_PLATFORM_MAINTENANCE = Parameter(
    15_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Pragmatic trial platform maintenance costs",
    display_name="Pragmatic Trial Platform Maintenance Costs",
    unit="USD/year",
    keywords=["15.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(10_000_000, 22_000_000),  # $10M-$22M (±30%)
    latex_symbol=r"Cost_{platform}",  # LaTeX symbol for equations
)  # $15M

DFDA_OPEX_STAFF = Parameter(
    10_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Pragmatic trial platform staff costs (minimal, AI-assisted)",
    display_name="Pragmatic Trial Platform Staff Costs",
    unit="USD/year",
    keywords=["10.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(7_000_000, 15_000_000),  # $7M-$15M (±30%)
    latex_symbol=r"Cost_{staff}",  # LaTeX symbol for equations
)  # $10M - minimal, AI-assisted

DFDA_OPEX_INFRASTRUCTURE = Parameter(
    8_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Pragmatic trial platform infrastructure costs (cloud, security)",
    display_name="Pragmatic Trial Platform Infrastructure Costs",
    unit="USD/year",
    keywords=["8.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(5_000_000, 12_000_000),  # $5M-$12M (±30%)
    latex_symbol=r"Cost_{infra}",  # LaTeX symbol for equations
)  # $8M - cloud, security

DFDA_OPEX_REGULATORY = Parameter(
    5_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Pragmatic trial platform regulatory coordination costs",
    display_name="Pragmatic Trial Platform Regulatory Coordination Costs",
    unit="USD/year",
    keywords=["5.0m", "pragmatic trials", "real world evidence", "approval", "authorization", "oversight", "regulation"],
    distribution="lognormal",
    confidence_interval=(3_000_000, 8_000_000),  # $3M-$8M (±30%)
    latex_symbol=r"Cost_{regulatory}",  # LaTeX symbol for equations
)  # $5M - regulatory coordination

DFDA_OPEX_COMMUNITY = Parameter(
    2_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Pragmatic trial platform community support costs",
    display_name="Pragmatic Trial Platform Community Support Costs",
    unit="USD/year",
    keywords=["2.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(1_000_000, 3_000_000),  # $1M-$3M (±30%)
    latex_symbol=r"Cost_{community}",  # LaTeX symbol for equations
)  # $2M - community support

# Total annual operational costs (calculated from components)
DFDA_ANNUAL_OPEX = Parameter(
    DFDA_OPEX_PLATFORM_MAINTENANCE
    + DFDA_OPEX_STAFF
    + DFDA_OPEX_INFRASTRUCTURE
    + DFDA_OPEX_REGULATORY
    + DFDA_OPEX_COMMUNITY,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total annual pragmatic trial platform operational costs (sum of all components: platform + staff + infra + regulatory + community)",
    display_name="Total Annual Pragmatic Trial Platform Operational Costs",
    unit="USD/year",
    formula="PLATFORM_MAINTENANCE + STAFF + INFRASTRUCTURE + REGULATORY + COMMUNITY",    keywords=["pragmatic trials", "real world evidence", "approval", "authorization", "oversight", "regulation", "decentralized trials"],
    # Uncertainty derived from component inputs
    validation_min=25_000_000,   # Floor: Lean MVP with minimal regulatory team
    validation_max=80_000_000,   # Ceiling: Full global compliance + 24/7 support + security audit responses
    inputs=["DFDA_OPEX_PLATFORM_MAINTENANCE", "DFDA_OPEX_STAFF", "DFDA_OPEX_INFRASTRUCTURE", "DFDA_OPEX_REGULATORY", "DFDA_OPEX_COMMUNITY"],
    latex_symbol=r"OPEX_{trial}",  # LaTeX symbol for equations
    compute=lambda ctx: sum([ctx["DFDA_OPEX_PLATFORM_MAINTENANCE"], ctx["DFDA_OPEX_STAFF"], ctx["DFDA_OPEX_INFRASTRUCTURE"], ctx["DFDA_OPEX_REGULATORY"], ctx["DFDA_OPEX_COMMUNITY"]])
)

# ===================================================================
# STANDALONE PRAGMATIC TRIAL FUNDING CHAIN (source-agnostic)
# ===================================================================
# These parameters represent a reference annual funding level WITHOUT
# specifying the source (treaty, philanthropy, government, etc.).
# The treaty-derived chain (DIH_TREASURY_*) is kept separately for
# the treaty impact paper.

DFDA_ANNUAL_TRIAL_FUNDING = Parameter(
    21_800_000_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="definition",
    distribution="fixed",
    description="Reference annual funding level used for direct-funding comparisons. Source-agnostic: funds could come from treaty reallocation, philanthropy, or public appropriation, and are modeled as funding available for pragmatic clinical trials rather than funding owed to any one organization.",
    display_name="Reference Annual Pragmatic Trial Funding",
    unit="USD/year",
    keywords=["funding", "annual", "trials", "pragmatic trials"],
    latex_symbol=r"Funding_{trial,ref}",
)  # $21.8B/year (source-agnostic)

DFDA_TRIAL_SUBSIDIES_ANNUAL = Parameter(
    DFDA_ANNUAL_TRIAL_FUNDING - DFDA_ANNUAL_OPEX,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Annual patient-level pragmatic trial subsidies after operating costs at the reference funding level",
    display_name="Reference Annual Trial Subsidies",
    unit="USD/year",
    formula="REFERENCE_TRIAL_FUNDING - TRIAL_PLATFORM_OPEX",
    keywords=["subsidy", "trial", "patient", "funding", "pragmatic trials"],
    inputs=["DFDA_ANNUAL_TRIAL_FUNDING", "DFDA_ANNUAL_OPEX"],
    compute=lambda ctx: ctx["DFDA_ANNUAL_TRIAL_FUNDING"] - ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"Subsidies_{trial,ref}",
)  # $21.76B/year

DFDA_PATIENTS_FUNDABLE_ANNUALLY = Parameter(
    DFDA_TRIAL_SUBSIDIES_ANNUAL / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Number of patients fundable annually at the reference pragmatic trial funding level and empirical pragmatic trial cost. Source-agnostic counterpart of DIH_PATIENTS_FUNDABLE_ANNUALLY.",
    display_name="Patients Fundable Annually at Reference Funding",
    unit="patients/year",
    formula="REFERENCE_TRIAL_SUBSIDIES / PRAGMATIC_TRIAL_COST_PER_PATIENT",
    keywords=["patients", "fundable", "trial", "capacity", "pragmatic trials"],
    inputs=["DFDA_TRIAL_SUBSIDIES_ANNUAL", "DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    compute=lambda ctx: ctx["DFDA_TRIAL_SUBSIDIES_ANNUAL"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    latex_symbol=r"N_{fundable,ref}",
)  # ~23.4M patients/year

# ===================================================================
# dFDA BENEFIT STRUCTURE (SIMPLIFIED)
# ===================================================================
# RECURRING ANNUAL BENEFITS (Happen every year forever):
#   - R&D Savings from 82× trial cost reduction: ~$50B/year
#   - Peace Dividend from 1% military cut: $113.55B/year
#   - Total Recurring: ~$163B/year perpetual
#
# ONE-TIME TIMELINE SHIFT BENEFIT (Happens once at launch):
#   - 8.2-year disease eradication acceleration: 449M deaths avoided (TOTAL)
#   - See section "ONE-TIME TIMELINE SHIFT BENEFITS" below
#   - WARNING: NOT a recurring $149T/year - that's (total ÷ 8.2 years)!
# ===================================================================

# ==============================================================================
# RECURRING ANNUAL BENEFITS (These repeat every year forever)
# ==============================================================================

# R&D Savings from Trial Cost Reduction (~$50B/year recurring)
DFDA_BENEFIT_RD_ONLY_ANNUAL = Parameter(
    GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL * DFDA_TRIAL_COST_REDUCTION_PCT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Annual benefit from pragmatic trial R&D savings (trial cost reduction, secondary component)",
    display_name="Annual R&D Savings from Pragmatic Trials",
    unit="USD/year",
    formula="TRIAL_SPENDING × COST_REDUCTION_PCT",
    keywords=["rd savings", "pragmatic trials", "real world evidence", "rct", "clinical trial"],
    # Uncertainty derived from inputs (TRIAL_SPENDING × COST_REDUCTION_PCT)
    validation_min=25_000_000_000,   # Floor: 30% cost reduction at $83B market
    validation_max=65_000_000_000,   # Ceiling: 70% cost reduction at $97B market
    inputs=["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "DFDA_TRIAL_COST_REDUCTION_PCT"],
    compute=lambda ctx: ctx["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"] * ctx["DFDA_TRIAL_COST_REDUCTION_PCT"],
    latex_symbol=r"Benefit_{RD,ann}",  # LaTeX symbol for equations
)  # $41.5B from automating Phase 2/3/4 trials

# Note: DFDA_BENEFIT_DISEASE_ERADICATION_DELAY_ANNUAL defined later (after DFDA_AVOIDED_DISEASE_ERADICATION_DELAY_COST_ANNUAL)

DFDA_RD_SAVINGS_DAILY = Parameter(
    DFDA_BENEFIT_RD_ONLY_ANNUAL / DAYS_PER_YEAR,
    manual_ref="knowledge/economics/health-dividend.qmd",
    source_type="calculated",
    description="Daily R&D savings from trial cost reduction (opportunity cost of delay)",
    display_name="Daily R&D Savings from Trial Cost Reduction",
    unit="USD/day",
    formula="ANNUAL_RD_SAVINGS ÷ DAYS_PER_YEAR",    keywords=["137m", "daily", "per day", "each day", "opportunity cost", "delay cost"],
    inputs=['DFDA_BENEFIT_RD_ONLY_ANNUAL'],
    compute=lambda ctx: ctx["DFDA_BENEFIT_RD_ONLY_ANNUAL"] / DAYS_PER_YEAR,
    latex_symbol=r"Savings_{RD,daily}",  # LaTeX symbol for equations
)  # $113.7M/day

DFDA_NET_SAVINGS_RD_ONLY_ANNUAL = Parameter(
    DFDA_BENEFIT_RD_ONLY_ANNUAL - DFDA_ANNUAL_OPEX,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Annual net savings from R&D cost reduction only (gross savings minus operational costs, excludes regulatory delay value)",
    display_name="Annual Net Savings from Pragmatic Trials (R&D Only)",
    unit="USD/year",
    formula="GROSS_SAVINGS - ANNUAL_OPEX",    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "yearly", "conservative"],
    inputs=["DFDA_BENEFIT_RD_ONLY_ANNUAL", "DFDA_ANNUAL_OPEX"],
    compute=lambda ctx: ctx["DFDA_BENEFIT_RD_ONLY_ANNUAL"] - ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"Savings_{RD,ann}",  # LaTeX symbol for equations
)  # $41.46B (R&D savings only, most conservative financial estimate)


# ---
# HEALTH IMPACT PARAMETERS
# ---

# QALY valuations
# Source: knowledge/appendix/icer-full-calculation.qmd
STANDARD_ECONOMIC_QALY_VALUE_USD = Parameter(
    150000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.QALY_VALUE,
    source_type="external",
    description="Standard economic value per QALY",
    display_name="Standard Economic Value per QALY",
    unit="USD/QALY",
    keywords=["150k", "qaly", "quality adjusted", "disability adjusted", "health metric", "health benefit", "quality of life"],
    distribution="normal",  # Normal appropriate: symmetric uncertainty around central VSL estimate
    std_error=30000,  # ±$30k (20%): Reflects policy debate range in VSL literature
                      # Economist rationale: OECD/EPA use $100k-$200k range; WHO uses $150k median
                      # Widened to ±20% to capture discount rate debate (Stern 1.4% vs Nordhaus 4.5%)
                      # Full literature ($50k-$500k) too wide; using consensus ±2σ = $90k-$210k
    validation_min=100000,  # Floor: OECD lower bound, emerging economy valuations
    validation_max=200000,  # Ceiling: US EPA upper bound ($10M VSL / 50 years)
    latex_symbol=r"Value_{QALY}",  # LaTeX symbol for equations
)  # Standard economic value per QALY

# --- Cumulative war death toll and QALY valuation (cost-of-war chapter) ---

# Total war + democide deaths since 1900
# Source: Leitenberg 2006 (CISSM) ~231M; Matthew White (necrometrics) ~123-203M; Hobsbawm ~187M
WAR_DEATHS_SINCE_1900 = Parameter(
    310_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref="leitenberg-deaths-wars-2006",
    source_type="definition",
    confidence="low",
    description="Total deaths from wars, conflicts, genocides, and policy-induced famines since 1900. "
                "Built from non-overlapping categories: Rummel democide 264M (incl 21st century) + "
                "battle deaths 39M + collateral civilian deaths 30M - overlap adjustment 25M = 308M, "
                "rounded to 310M. Range: White low 200M to Rummel-high-plus-military 340M.",
    display_name="Total War and Conflict Deaths Since 1900",
    unit="deaths",
    distribution="uniform",
    confidence_interval=(200_000_000, 340_000_000),
    keywords=["war", "deaths", "cumulative", "20th century", "total", "since 1900"],
    latex_symbol=r"Deaths_{war,1900}",
)

# Average years of life lost per war death
# Soldiers average ~23 (Vietnam data); civilians skew older; weighted average ~28
# Mid-20th-century global life expectancy ~55; 55 - 28 = 27 years lost per death
WAR_AVG_YEARS_LIFE_LOST_PER_DEATH = Parameter(
    27,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref="necrometrics-20th-century",
    source_type="definition",
    confidence="low",
    description="Average years of life lost per war/conflict death. Based on avg age at death ~28 "
                "(soldiers ~23, civilians older) vs mid-century life expectancy ~55.",
    display_name="Average Years of Life Lost per War Death",
    unit="years",
    distribution="uniform",
    confidence_interval=(20, 35),
    keywords=["war", "life years", "lost", "average", "QALY"],
    latex_symbol=r"YLL_{war}",
)

# Total life-years lost to war since 1900
WAR_LIFE_YEARS_LOST_SINCE_1900 = Parameter(
    WAR_DEATHS_SINCE_1900 * WAR_AVG_YEARS_LIFE_LOST_PER_DEATH,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Total life-years stolen by war since 1900 (deaths x avg years lost per death)",
    display_name="Total Life-Years Lost to War Since 1900",
    unit="life-years",
    formula="WAR_DEATHS_SINCE_1900 × WAR_AVG_YEARS_LIFE_LOST_PER_DEATH",
    inputs=["WAR_DEATHS_SINCE_1900", "WAR_AVG_YEARS_LIFE_LOST_PER_DEATH"],
    compute=lambda ctx: ctx["WAR_DEATHS_SINCE_1900"] * ctx["WAR_AVG_YEARS_LIFE_LOST_PER_DEATH"],
    keywords=["war", "life years", "lost", "cumulative", "QALY", "since 1900"],
    latex_symbol=r"YLL_{war,total}",
)

# QALY-based economic value of life-years lost to war since 1900
WAR_QALY_VALUE_LOST_SINCE_1900 = Parameter(
    WAR_LIFE_YEARS_LOST_SINCE_1900 * STANDARD_ECONOMIC_QALY_VALUE_USD,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Economic value of life-years destroyed by war since 1900, at $150K/QALY",
    display_name="QALY Value of Life Lost to War Since 1900",
    unit="USD",
    formula="WAR_LIFE_YEARS_LOST_SINCE_1900 × STANDARD_ECONOMIC_QALY_VALUE_USD",
    inputs=["WAR_LIFE_YEARS_LOST_SINCE_1900", "STANDARD_ECONOMIC_QALY_VALUE_USD"],
    compute=lambda ctx: ctx["WAR_LIFE_YEARS_LOST_SINCE_1900"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    keywords=["war", "QALY", "value", "economic", "life years", "cumulative", "since 1900"],
    latex_symbol=r"V_{war,QALY}",
)

# Children killed in wars since 1900
# ~33% of total: children are majority of famine deaths (de Waal 2017: under-5 = 50-67%),
# ~50% of civilian casualties (APA 2001), but small share of combatants.
# Conservative one-in-three estimate across combat, civilian, genocide, and famine categories.
WAR_CHILD_DEATH_PCT = Parameter(
    0.33,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.DE_WAAL_FAMINE_CHILD_MORTALITY_2018,
    source_type="definition",
    confidence="low",
    description="Estimated share of war deaths since 1900 that were children under 18. "
                "Constructed from category-weighted estimates: combat ~3%, civilian ~35%, "
                "genocide ~33%, famine ~60%. Conservative aggregate ~33%. "
                "Sources: de Waal 2017 (famine child mortality), APA 2001 (civilian child share).",
    display_name="Child Share of War Deaths Since 1900",
    unit="rate",
    distribution="uniform",
    confidence_interval=(0.25, 0.40),
    keywords=["children", "war", "deaths", "percentage", "child casualties"],
    latex_symbol=r"Pct_{war,child}",
)

WAR_CHILDREN_KILLED_SINCE_1900 = Parameter(
    WAR_DEATHS_SINCE_1900 * WAR_CHILD_DEATH_PCT,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    description="Estimated children under 18 killed in wars, conflicts, genocides, and "
                "policy-induced famines since 1900",
    display_name="Children Killed in Wars Since 1900",
    unit="deaths",
    formula="WAR_DEATHS_SINCE_1900 × WAR_CHILD_DEATH_PCT",
    inputs=["WAR_DEATHS_SINCE_1900", "WAR_CHILD_DEATH_PCT"],
    compute=lambda ctx: ctx["WAR_DEATHS_SINCE_1900"] * ctx["WAR_CHILD_DEATH_PCT"],
    keywords=["children", "war", "deaths", "killed", "since 1900"],
    latex_symbol=r"Deaths_{war,child}",
)

# Global nuclear weapons spending and apocalypse metrics
GLOBAL_NUCLEAR_WEAPONS_SPENDING = Parameter(
    92_000_000_000,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_ref=ReferenceID.GLOBAL_NUCLEAR_WEAPON_MAINTENANCE_100B,
    source_type="external",
    confidence="high",
    description="Annual global spending on nuclear weapons across all nine nuclear-armed "
                "states. US: $51.5B, China: $11.8B, UK: $8.1B, Russia: $8.3B, France: $6.8B, "
                "India: ~$2.7B, Israel: ~$1.2B, Pakistan: ~$1.1B, North Korea: ~$0.7B.",
    display_name="Global Nuclear Weapons Spending",
    unit="USD",
    distribution="fixed",
    keywords=["nuclear", "spending", "weapons", "arsenal", "annual", "ICAN"],
    latex_symbol=r"S_{nuke}",
)

NUCLEAR_WINTER_WARHEAD_THRESHOLD = Parameter(
    100,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_ref=ReferenceID.NUKE_WINTER_150TG,
    source_type="external",
    confidence="medium",
    description="Approximate number of warheads needed to trigger a regional-scale "
                "nuclear winter sufficient to collapse the global food system. A 100-warhead "
                "regional exchange (Robock/Toon 2007, extended by Xia et al. 2022) injects "
                "~5 Tg of soot into the stratosphere, drops global temperatures ~1.8C for a "
                "decade, shortens growing seasons worldwide, and kills ~2 billion people from "
                "famine. Civilization as the median human experiences it does not survive. "
                "Xia 2022 shows total agricultural collapse (~5B deaths) at ~4,400 warheads; "
                "this parameter uses the lower threshold for median-human civilizational collapse.",
    display_name="Nuclear Winter Warhead Threshold",
    unit="warheads",
    distribution="uniform",
    confidence_interval=(50, 300),
    keywords=["nuclear", "winter", "warheads", "threshold", "soot", "famine"],
    latex_symbol=r"W_{winter}",
)

GLOBAL_WARHEAD_COUNT = Parameter(
    12_241,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_ref=ReferenceID.WORLD_WARHEADS,
    source_type="external",
    confidence="high",
    description="Total global nuclear warhead inventory across nine nuclear-armed states. "
                "Includes deployed, reserve, and retired warheads awaiting dismantlement.",
    display_name="Global Nuclear Warhead Count",
    unit="warheads",
    distribution="fixed",
    keywords=["nuclear", "warheads", "arsenal", "global", "inventory", "FAS"],
    latex_symbol=r"W_{global}",
)

NUCLEAR_WINTER_OVERKILL_FACTOR = Parameter(
    12_241 / 100,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="How many times the global nuclear arsenal exceeds the threshold for "
                "civilizational collapse via regional-scale nuclear winter (~100 warheads, "
                "~5 Tg soot, ~2 billion famine deaths, global food system collapse). "
                "The arsenal-based overkill factor against the apocalypse the median "
                "human experiences.",
    display_name="Nuclear Winter Overkill Factor",
    unit="x",
    formula="GLOBAL_WARHEAD_COUNT / NUCLEAR_WINTER_WARHEAD_THRESHOLD",
    inputs=["GLOBAL_WARHEAD_COUNT", "NUCLEAR_WINTER_WARHEAD_THRESHOLD"],
    compute=lambda ctx: ctx["GLOBAL_WARHEAD_COUNT"] / ctx["NUCLEAR_WINTER_WARHEAD_THRESHOLD"],
    keywords=["nuclear", "winter", "overkill", "arsenal", "warheads"],
    latex_symbol=r"Overkill_{winter}",
)

NUCLEAR_WINTER_SPARE_APOCALYPSES = Parameter(
    (12_241 / 100) - 1,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="Spare apocalypses: how many civilization-ending nuclear winters the global "
                "arsenal can trigger beyond the one that would already end civilization. "
                "The nuclear winter overkill factor minus one. Used wherever the manual "
                "jokes about the surplus (the apocalypses kept in case the first does not "
                "take).",
    display_name="Spare Apocalypses (Overkill Factor Minus One)",
    unit="apocalypses",
    formula="NUCLEAR_WINTER_OVERKILL_FACTOR - 1",
    inputs=["NUCLEAR_WINTER_OVERKILL_FACTOR"],
    compute=lambda ctx: ctx["NUCLEAR_WINTER_OVERKILL_FACTOR"] - 1,
    keywords=["nuclear", "winter", "overkill", "spare", "apocalypse", "surplus"],
    latex_symbol=r"Overkill_{spare}",
)

# Price of Apocalypse and Apocalypse Markup
# The cost of triggering one nuclear winter, and the markup above it
PRICE_OF_APOCALYPSE = Parameter(
    92_000_000_000 / (12_241 / 100),
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="The Price of Apocalypse: the annual cost of maintaining enough nuclear "
                "warheads to trigger a civilization-ending nuclear winter (~100 warheads, "
                "~5 Tg soot, ~2 billion famine deaths, global food system collapse). "
                "Calculated as global nuclear spending divided by the nuclear winter "
                "overkill factor.",
    display_name="Price of Apocalypse (Minimum Viable Apocalypse)",
    unit="USD",
    formula="GLOBAL_NUCLEAR_WEAPONS_SPENDING / NUCLEAR_WINTER_OVERKILL_FACTOR",
    inputs=["GLOBAL_NUCLEAR_WEAPONS_SPENDING", "NUCLEAR_WINTER_OVERKILL_FACTOR"],
    compute=lambda ctx: ctx["GLOBAL_NUCLEAR_WEAPONS_SPENDING"] / ctx["NUCLEAR_WINTER_OVERKILL_FACTOR"],
    keywords=["apocalypse", "price", "minimum", "nuclear", "winter", "cost"],
    latex_symbol=r"P_{apocalypse}",
)

APOCALYPSE_MARKUP = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 - (92_000_000_000 / (12_241 / 100)),
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="The Apocalypse Markup: total military spending beyond the Price of "
                "Apocalypse. The amount governments spend above what is needed to trigger "
                "nuclear winter and end civilization once.",
    display_name="Apocalypse Markup",
    unit="USD",
    formula="GLOBAL_MILITARY_SPENDING_ANNUAL_2024 - PRICE_OF_APOCALYPSE",
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "PRICE_OF_APOCALYPSE"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] - ctx["PRICE_OF_APOCALYPSE"],
    keywords=["apocalypse", "markup", "waste", "overkill", "redundant", "excess"],
    latex_symbol=r"M_{apocalypse}",
)

APOCALYPSE_MARKUP_MULTIPLIER = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / (92_000_000_000 / (12_241 / 100)),
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="How many times total military spending exceeds the Price of Apocalypse. "
                "The markup multiplier on the cost of ending civilization.",
    display_name="Apocalypse Markup Multiplier",
    unit="x",
    formula="GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / PRICE_OF_APOCALYPSE",
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "PRICE_OF_APOCALYPSE"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["PRICE_OF_APOCALYPSE"],
    keywords=["apocalypse", "markup", "multiplier", "ratio"],
    latex_symbol=r"M_{apocalypse,x}",
)

# Bullet purchasing power (complements nuclear overkill with a more visceral metric)
BULLET_COST_556_NATO = Parameter(
    0.40,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_ref=ReferenceID.NATO_556_AMMO_COST,
    source_type="external",
    confidence="medium",
    description="Cost per round of 5.56x45mm NATO ammunition (military bulk procurement). "
                "Based on U.S. military procurement contracts for M855 ball ammunition. "
                "Civilian retail floor is ~$0.37; $0.40 is a conservative midpoint.",
    display_name="Cost per 5.56mm NATO Round (Bulk)",
    unit="USD",
    distribution="uniform",
    confidence_interval=(0.25, 0.60),
    keywords=["bullet", "ammunition", "cost", "5.56", "NATO", "small arms", "round"],
    latex_symbol=r"c_{bullet}",
)

BULLETS_FIRED_PER_KILL_IRAQ_AFGHANISTAN = Parameter(
    250_000,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_ref=ReferenceID.NATO_556_ROUNDS_PER_KILL,
    source_type="external",
    confidence="medium",
    description="Rounds of small-arms ammunition fired per insurgent killed in Iraq and "
                "Afghanistan. Based on GAO figures: ~6 billion rounds expended 2002-2005. "
                "Calculated by military researcher John Pike of GlobalSecurity.org.",
    display_name="Bullets Fired per Kill (Iraq/Afghanistan)",
    unit="rounds",
    distribution="fixed",
    keywords=["bullets", "rounds", "per kill", "Iraq", "Afghanistan", "combat", "ammunition"],
    latex_symbol=r"n_{rounds/kill}",
)

GLOBAL_BULLETS_PURCHASABLE_ANNUAL = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / BULLET_COST_556_NATO,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="Number of 5.56mm NATO rounds purchasable with the entire global military "
                "budget at bulk procurement prices. Pure purchasing power calculation, "
                "not a combat efficiency estimate.",
    display_name="Bullets Purchasable with Global Military Budget",
    unit="rounds",
    formula="GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / BULLET_COST_556_NATO",
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "BULLET_COST_556_NATO"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["BULLET_COST_556_NATO"],
    keywords=["bullets", "purchasing power", "military budget", "ammunition", "rounds"],
    latex_symbol=r"N_{bullets,yr}",
)

# Annual terrorism death risk
ANNUAL_TERRORISM_DEATH_RISK_DENOMINATOR = Parameter(
    30_000_000,
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_ref=ReferenceID.CHANCE_OF_DYING_FROM_TERRORISM_1_IN_30M,
    source_type="external",
    confidence="high",
    description="Annual probability of being killed by terrorism expressed as '1 in X'. "
                "An American's annual odds of dying in a terrorist attack are approximately 1 in 30 million.",
    display_name="Annual Terrorism Death Risk (1 in X)",
    unit="people",
    distribution="fixed",
    keywords=["terrorism", "risk", "odds", "probability", "annual", "chance", "1 in 30 million"],
    latex_symbol=r"Risk_{terror,denom}",
)

# Cumulative military spending expressed in years of government clinical trial spending
CUMULATIVE_MILITARY_IN_GOVT_TRIAL_YEARS = Parameter(
    CUMULATIVE_MILITARY_SPENDING_FED_ERA / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
    manual_ref="knowledge/strategy/declaration-of-optimization.qmd",
    source_type=SourceType.CALCULATED,
    description="Cumulative military spending since 1913 expressed in equivalent years of "
                "government clinical trial spending ($170T / $4.5B per year)",
    display_name="Military Spending in Government Clinical Trial Years",
    unit="years",
    formula="CUMULATIVE_MILITARY_SPENDING_FED_ERA / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL",
    inputs=["CUMULATIVE_MILITARY_SPENDING_FED_ERA", "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    compute=lambda ctx: ctx["CUMULATIVE_MILITARY_SPENDING_FED_ERA"] / ctx["GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"],
    keywords=["military", "clinical trials", "equivalent", "years", "government", "spending"],
    latex_symbol=r"Years_{mil \to trials,gov}",
)

WAR_TRIAL_REDIRECT_1900_FREEZE_BASELINE_ANNUAL = Parameter(
    66_100_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.CORRELATES_OF_WAR_NMC,
    source_type=SourceType.EXTERNAL,
    confidence="low",
    description="Global military spending in 1900 in constant 2023 USD, from the Correlates of War "
                "National Material Capabilities (NMC) dataset (knowledge/data/global-military-spending-"
                "1900-2024-constant-2023-usd.csv, COW_NMC source). Used as the annual real spending "
                "cap in the 1900-freeze counterfactual.",
    display_name="1900 Military Spending Freeze Baseline",
    unit="USD/year",
    distribution="uniform",
    confidence_interval=(50_000_000_000, 90_000_000_000),
    keywords=["war", "military", "1900", "freeze", "baseline", "counterfactual"],
    latex_symbol=r"Spending_{mil,1900}",
)

WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE = Parameter(
    _sum_excess_military_spending_above_1900_freeze(float(WAR_TRIAL_REDIRECT_1900_FREEZE_BASELINE_ANNUAL)),
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.CORRELATES_OF_WAR_NMC,
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Dataset-derived aggregate: cumulative global military spending above a 1900 real-spending "
                "freeze, 1900-2024, calculated from knowledge/data/global-military-spending-1900-2024-"
                "constant-2023-usd.csv (Correlates of War NMC) as the sum of max(0, annual spending - "
                "1900 baseline) across years. The stricter medical redirect pot, distinct from total "
                "cumulative military spending.",
    display_name="Excess Military Spending Above 1900 Freeze",
    unit="USD",
    formula="for t=1900..2024: sum max(0, MILITARY_SPENDING_YEAR - WAR_TRIAL_REDIRECT_1900_FREEZE_BASELINE_ANNUAL)",
    inputs=["WAR_TRIAL_REDIRECT_1900_FREEZE_BASELINE_ANNUAL"],
    compute=lambda ctx: _sum_excess_military_spending_above_1900_freeze(ctx["WAR_TRIAL_REDIRECT_1900_FREEZE_BASELINE_ANNUAL"]),
    keywords=["war", "military", "1900", "freeze", "excess", "counterfactual", "clinical trials"],
    latex_symbol=r"Spending_{mil,excess1900}",
)

WAR_TRIAL_REDIRECT_EXCESS_MILITARY_TRIAL_YEARS = Parameter(
    WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Clinical-trial years funded by military spending above a 1900 real-spending freeze. "
                "This is the literal 1900-freeze medical redirect capacity, not total cumulative "
                "military spending.",
    display_name="Excess Military Spending Above 1900 Freeze in Clinical Trial Years",
    unit="years",
    formula="WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE / GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL",
    inputs=[
        "WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE",
        "GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL",
    ],
    compute=lambda ctx: (
        ctx["WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE"]
        / ctx["GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL"]
    ),
    keywords=["war", "medical opportunity cost", "1900 freeze", "clinical trials", "trial years"],
    latex_symbol=r"Years_{excess1900 \to trials,gov}",
)

WAR_TRIAL_REDIRECT_START_YEAR = Parameter(
    1900,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.DEFINITION,
    confidence="high",
    description="Start year for the aggressive prosecutor medical redirect counterfactual.",
    display_name="War-Redirect Medical Counterfactual Start Year",
    unit="year",
    distribution="fixed",
    keywords=["war", "medical opportunity cost", "1900", "clinical trials", "counterfactual"],
    latex_symbol=r"Y_{redirect,start}",
)

WAR_TRIAL_REDIRECT_TOOLCHAIN_BOOTSTRAP_YEARS = Parameter(
    14,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.DEFINITION,
    confidence="low",
    description="Estimated minimum physical build time for the medical toolchain even with 10x capital: "
                "diagnostics, cell culture, manufacturing scale-up, trained researchers, surveillance, "
                "and trial infrastructure. Fermi rationale: (1) scientific breakthroughs are treated as "
                "largely proportional to investment -- more money attracts talent from finance and other "
                "high-paying sectors, more researchers mean more parallel experiments and more shots on "
                "goal, so conceptual barriers are not treated as exogenous; (2) even so, a physical floor "
                "exists -- you cannot train a molecular biologist in a year or build a penicillin factory "
                "overnight regardless of capital; (3) prize-based and market-incentive funding is assumed, "
                "not NIH grant-style funding -- prizes pay for results, not process, yielding roughly "
                "5-10x more useful output per dollar, making this estimate conservative relative to "
                "current NIH efficiency as a baseline; (4) Operation Warp Speed compressed a 10-15 year "
                "vaccine timeline to 9 months with advance purchase commitments -- ~15x acceleration -- "
                "suggesting the physical floor is around 12-18 months for known-science applications. "
                "14 years reflects the harder case of building infrastructure for unknown-science "
                "applications from a 1900 starting point. Confidence interval (0-40) reflects genuine "
                "uncertainty; the central estimate is not reverse-engineered to hit any target year.",
    display_name="War-Redirect Medical Toolchain Bootstrap Years",
    unit="years",
    distribution="triangular",
    confidence_interval=(0, 40),
    keywords=["war", "medical opportunity cost", "toolchain", "bootstrap", "clinical trials", "counterfactual"],
    latex_symbol=r"T_{tool,bootstrap}",
)

WAR_TRIAL_REDIRECT_AGING_LAG_AFTER_DISEASE_CONTROL_YEARS = Parameter(
    40,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.DEFINITION,
    confidence="low",
    description="Additional lag after broad disease-control capacity before biological aging becomes "
                "a treatable risk factor in the aggressive prosecutor model. Fermi rationale: aging "
                "research requires the molecular biology toolchain (DNA structure, oncogenes, telomere "
                "biology, cellular senescence) which itself builds on the disease-control infrastructure. "
                "With investment proportional to funding and prizes accelerating iteration, the hallmarks-"
                "of-aging framework (telomeres, senolytics, mTOR) likely emerges ~15-20 years faster than "
                "the historical timeline -- but geroscience is genuinely downstream of molecular biology "
                "and cannot be fully parallelized with disease-control research. 40 years is the central "
                "estimate; confidence interval (10-65) is wide because this is the most speculative "
                "component of the model.",
    display_name="War-Redirect Aging Lag After Disease Control",
    unit="years",
    distribution="triangular",
    confidence_interval=(10, 65),
    keywords=["war", "medical opportunity cost", "aging", "geroscience", "clinical trials", "counterfactual"],
    latex_symbol=r"T_{aging,lag}",
)

WAR_TRIAL_REDIRECT_PLEADING_END_YEAR = Parameter(
    2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.DEFINITION,
    confidence="high",
    description="End year for the aggressive prosecutor post-cutoff plaintiff count.",
    display_name="War-Redirect Pleading End Year",
    unit="year",
    distribution="fixed",
    keywords=["war", "medical misallocation", "pleading", "end year", "plaintiffs", "prosecutor"],
    latex_symbol=r"Y_{plead,end}",
)

MEDICAL_TOOLCHAIN_HGP_COST_USD = Parameter(
    2_700_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.HUMAN_GENOME_AND_GENETIC_EDITING,
    source_type=SourceType.EXTERNAL,
    confidence="medium",
    description="Approximate Human Genome Project cost used as an observed medical-toolchain anchor.",
    display_name="Medical Toolchain Human Genome Project Cost",
    unit="USD",
    distribution="fixed",
    keywords=["medical toolchain", "human genome project", "genomics", "anchor cost"],
    latex_symbol=r"C_{tool,HGP}",
)

MEDICAL_TOOLCHAIN_CRISPR_NIH_FUNDING_2011_2018 = Parameter(
    3_100_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.CRS_CRISPR_NIH_FUNDING_2011_2018,
    source_type=SourceType.EXTERNAL,
    confidence="high",
    description="Rounded NIH CRISPR-related research funding for FY2011-FY2018 from CRS Table 1.",
    display_name="Medical Toolchain NIH CRISPR Funding, FY2011-FY2018",
    unit="USD",
    distribution="fixed",
    keywords=["medical toolchain", "CRISPR", "NIH", "gene editing", "anchor cost"],
    latex_symbol=r"C_{tool,CRISPR}",
)

MEDICAL_TOOLCHAIN_BRAIN_INITIATIVE_PLANNED_BUDGET = Parameter(
    4_500_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.NIH_BRAIN_INITIATIVE_PLANNED_BUDGET,
    source_type=SourceType.EXTERNAL,
    confidence="high",
    description="Planned NIH BRAIN Initiative commitment described in the BRAIN 2025 scientific vision.",
    display_name="Medical Toolchain BRAIN Initiative Planned Budget",
    unit="USD",
    distribution="fixed",
    keywords=["medical toolchain", "BRAIN Initiative", "neuroscience", "anchor cost"],
    latex_symbol=r"C_{tool,BRAIN}",
)

MEDICAL_TOOLCHAIN_PCORNET_INFRASTRUCTURE_FUNDING = Parameter(
    325_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.PCORNET_INFRASTRUCTURE_FUNDING,
    source_type=SourceType.EXTERNAL,
    confidence="medium",
    description="Rounded PCORI-funded PCORnet Studies amount from the Q4 2025 PCORnet dashboard. "
                "Used as a network-scale pragmatic-trial infrastructure anchor.",
    display_name="Medical Toolchain PCORnet Infrastructure Funding Anchor",
    unit="USD",
    distribution="fixed",
    keywords=["medical toolchain", "PCORnet", "PCORI", "pragmatic trials", "infrastructure"],
    latex_symbol=r"C_{tool,PCORnet}",
)

MEDICAL_TOOLCHAIN_HITECH_EHR_INCENTIVE_ESTIMATED_SPENDING = Parameter(
    30_000_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.HITECH_EHR_INCENTIVE_ESTIMATED_SPENDING,
    source_type=SourceType.EXTERNAL,
    confidence="high",
    description="GAO estimate of Medicare and Medicaid EHR incentive program spending from 2011 through 2019.",
    display_name="Medical Toolchain HITECH EHR Incentive Estimated Spending",
    unit="USD",
    distribution="fixed",
    keywords=["medical toolchain", "HITECH", "EHR", "health data", "anchor cost"],
    latex_symbol=r"C_{tool,EHR}",
)

MEDICAL_TOOLCHAIN_OWS_POTENTIAL_VACCINE_AWARDS = Parameter(
    18_000_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.OPERATION_WARP_SPEED_POTENTIAL_VACCINE_AWARDS,
    source_type=SourceType.EXTERNAL,
    confidence="high",
    description="GAO-reported total potential estimated value of Operation Warp Speed vaccine candidate awards.",
    display_name="Medical Toolchain Operation Warp Speed Potential Vaccine Awards",
    unit="USD",
    distribution="fixed",
    keywords=["medical toolchain", "Operation Warp Speed", "vaccines", "manufacturing", "anchor cost"],
    latex_symbol=r"C_{tool,OWS}",
)

MEDICAL_TOOLCHAIN_OBSERVED_ANCHOR_COSTS = Parameter(
    MEDICAL_TOOLCHAIN_HGP_COST_USD
    + MEDICAL_TOOLCHAIN_CRISPR_NIH_FUNDING_2011_2018
    + MEDICAL_TOOLCHAIN_BRAIN_INITIATIVE_PLANNED_BUDGET
    + MEDICAL_TOOLCHAIN_PCORNET_INFRASTRUCTURE_FUNDING
    + MEDICAL_TOOLCHAIN_HITECH_EHR_INCENTIVE_ESTIMATED_SPENDING
    + MEDICAL_TOOLCHAIN_OWS_POTENTIAL_VACCINE_AWARDS,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="Sum of observed anchor costs for major medical toolchain programs. This is anchor "
                "evidence for the prosecutor reserve, not a claim that these programs alone cure disease.",
    display_name="Observed Medical Toolchain Anchor Costs",
    unit="USD",
    formula="HGP + CRISPR + BRAIN + PCORnet + HITECH + OWS",
    inputs=[
        "MEDICAL_TOOLCHAIN_HGP_COST_USD",
        "MEDICAL_TOOLCHAIN_CRISPR_NIH_FUNDING_2011_2018",
        "MEDICAL_TOOLCHAIN_BRAIN_INITIATIVE_PLANNED_BUDGET",
        "MEDICAL_TOOLCHAIN_PCORNET_INFRASTRUCTURE_FUNDING",
        "MEDICAL_TOOLCHAIN_HITECH_EHR_INCENTIVE_ESTIMATED_SPENDING",
        "MEDICAL_TOOLCHAIN_OWS_POTENTIAL_VACCINE_AWARDS",
    ],
    compute=lambda ctx: (
        ctx["MEDICAL_TOOLCHAIN_HGP_COST_USD"]
        + ctx["MEDICAL_TOOLCHAIN_CRISPR_NIH_FUNDING_2011_2018"]
        + ctx["MEDICAL_TOOLCHAIN_BRAIN_INITIATIVE_PLANNED_BUDGET"]
        + ctx["MEDICAL_TOOLCHAIN_PCORNET_INFRASTRUCTURE_FUNDING"]
        + ctx["MEDICAL_TOOLCHAIN_HITECH_EHR_INCENTIVE_ESTIMATED_SPENDING"]
        + ctx["MEDICAL_TOOLCHAIN_OWS_POTENTIAL_VACCINE_AWARDS"]
    ),
    keywords=["medical toolchain", "anchor costs", "prizes", "infrastructure"],
    latex_symbol=r"C_{tool,anchors}",
)

WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET = Parameter(
    20_000_000_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.DEFINITION,
    confidence="low",
    description="Aggressive prosecutor reserve for buying the missing medical toolchain: prizes, "
                "diagnostics, EHRs, sequencing, AI, factories, surveillance, and pragmatic-trial "
                "infrastructure before counting remaining money as direct trial capacity.",
    display_name="War Medical Toolchain Prize Budget",
    unit="USD",
    distribution="triangular",
    confidence_interval=(5_000_000_000_000, 50_000_000_000_000),
    keywords=["war", "medical toolchain", "prize budget", "trials", "infrastructure", "prosecutor"],
    latex_symbol=r"C_{tool,prize}",
)

WAR_MEDICAL_TOOLCHAIN_PRIZE_OVERPAY_MULTIPLE = Parameter(
    WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET / MEDICAL_TOOLCHAIN_OBSERVED_ANCHOR_COSTS,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="How many times larger the prosecutor's medical-toolchain prize reserve is than "
                "the observed anchor costs listed here.",
    display_name="War Medical Toolchain Prize Overpay Multiple",
    unit="x",
    formula="WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET / MEDICAL_TOOLCHAIN_OBSERVED_ANCHOR_COSTS",
    inputs=["WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET", "MEDICAL_TOOLCHAIN_OBSERVED_ANCHOR_COSTS"],
    compute=lambda ctx: ctx["WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET"] / ctx["MEDICAL_TOOLCHAIN_OBSERVED_ANCHOR_COSTS"],
    keywords=["war", "medical toolchain", "overpay", "prize budget", "anchor costs"],
    latex_symbol=r"m_{tool,overpay}",
)

# --- Moved here from later in file so war counterfactual params can reference them ---

# Global GDP (2025) - needed for global opportunity cost calculations
GLOBAL_GDP_2025 = Parameter(
    115_000_000_000_000,  # $115 trillion (2025 estimate from Political Dysfunction Tax paper)
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="high",
    distribution="fixed",  # Official aggregate estimate
    description="Global nominal GDP (2025 estimate). From Political Dysfunction Tax paper citing "
                "StatisticsTimes/IMF World Economic Outlook. Used for calculating global opportunity costs "
                "as percentage of world economic output. Note: Latest IMF data shows $117T.",
    display_name="Global GDP (2025)",
    unit="USD",
    keywords=["GDP", "global", "world", "economy", "2025"],
    latex_symbol=r"GDP_{global}",
)

GLOBAL_GOVERNMENT_EXPENSE_PCT_GDP = Parameter(
    0.3178,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_ref=ReferenceID.WORLD_BANK_GOVERNMENT_EXPENSE_PCT_GDP,
    source_type=SourceType.EXTERNAL,
    confidence="medium",
    distribution="fixed",
    description="World general government total expense as a share of GDP, using World Bank indicator "
                "GC.XPN.TOTL.GD.ZS. The most recent world aggregate in the cited source is 2021.",
    display_name="Global Government Expense Share of GDP",
    unit="percent",
    keywords=["government", "expense", "GDP", "public spending", "world bank", "taxes"],
    latex_symbol=r"p_{gov,expense}",
)

GLOBAL_GOVERNMENT_EXPENSE_ANNUAL = Parameter(
    GLOBAL_GDP_2025 * GLOBAL_GOVERNMENT_EXPENSE_PCT_GDP,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="Approximate annual global government expenditure, computed as global GDP times the "
                "World Bank general-government expense share of GDP.",
    display_name="Annual Global Government Expense",
    unit="USD/year",
    formula="GLOBAL_GDP_2025 × GLOBAL_GOVERNMENT_EXPENSE_PCT_GDP",
    inputs=["GLOBAL_GDP_2025", "GLOBAL_GOVERNMENT_EXPENSE_PCT_GDP"],
    compute=lambda ctx: ctx["GLOBAL_GDP_2025"] * ctx["GLOBAL_GOVERNMENT_EXPENSE_PCT_GDP"],
    keywords=["government", "expense", "annual", "public spending", "taxes", "global"],
    latex_symbol=r"Expense_{gov,global}",
)

# Population
GLOBAL_POPULATION_2024 = Parameter(
    8_000_000_000,
    manual_ref="knowledge/solution/dih.qmd",
    source_ref=ReferenceID.GLOBAL_POPULATION_8_BILLION,
    source_type="external",
    description="Global population in 2024",
    display_name="Global Population in 2024",
    unit="of people",
    confidence_interval=(7_800_000_000, 8_200_000_000),  # ±2% census estimate uncertainty
    distribution="lognormal",
    keywords=["2024", "8.0b", "people", "worldwide", "citizens", "individuals", "inhabitants"],
    latex_symbol=r"Pop_{global}",  # LaTeX symbol for equations
)  # UN World Population Prospects 2022

WAR_TRIAL_REDIRECT_NET_TRIAL_BUDGET = Parameter(
    CUMULATIVE_MILITARY_SPENDING_FED_ERA - WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Cumulative military spending since the Federal Reserve era after reserving the "
                "aggressive prosecutor's medical-toolchain prize budget.",
    display_name="War Trial Redirect Net Trial Budget After Toolchain Reserve",
    unit="USD",
    formula="CUMULATIVE_MILITARY_SPENDING_FED_ERA - WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET",
    inputs=["CUMULATIVE_MILITARY_SPENDING_FED_ERA", "WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET"],
    compute=lambda ctx: ctx["CUMULATIVE_MILITARY_SPENDING_FED_ERA"] - ctx["WAR_MEDICAL_TOOLCHAIN_PRIZE_BUDGET"],
    keywords=["war", "medical misallocation", "toolchain reserve", "trial budget", "prosecutor"],
    latex_symbol=r"B_{trials,net}",
)

WAR_TRIAL_REDIRECT_PATIENT_SLOTS_FUNDED = Parameter(
    WAR_TRIAL_REDIRECT_NET_TRIAL_BUDGET / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Patient-slots funded by the net redirected war budget at pragmatic trial cost per "
                "patient. Patient-slots are repeated experimental opportunities, not unique people.",
    display_name="War Trial Redirect Patient Slots Funded",
    unit="patient-slots",
    formula="WAR_TRIAL_REDIRECT_NET_TRIAL_BUDGET / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT",
    inputs=["WAR_TRIAL_REDIRECT_NET_TRIAL_BUDGET", "DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_NET_TRIAL_BUDGET"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    keywords=["war", "medical misallocation", "patient slots", "pragmatic trials", "prosecutor"],
    latex_symbol=r"N_{slots,war}",
)

WAR_TRIAL_REDIRECT_PATIENT_SLOTS_PER_LIVING_HUMAN = Parameter(
    WAR_TRIAL_REDIRECT_PATIENT_SLOTS_FUNDED / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Patient-slots funded per living human, used to avoid implying hundreds of billions "
                "of unique patients. It means repeated trial opportunities across time and indications.",
    display_name="War Trial Redirect Patient Slots Per Living Human",
    unit="patient-slots/person",
    formula="WAR_TRIAL_REDIRECT_PATIENT_SLOTS_FUNDED / GLOBAL_POPULATION_2024",
    inputs=["WAR_TRIAL_REDIRECT_PATIENT_SLOTS_FUNDED", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_PATIENT_SLOTS_FUNDED"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["war", "medical misallocation", "patient slots", "population", "prosecutor"],
    latex_symbol=r"N_{slots,pc}",
)

# Global life expectancy at birth, used as the cohort-lifetime horizon for representative
# full-life damages calculations and as the YLL anchor in the regulatory-delay QALY chain.
# Moved here from later in the file so lost-prosperity-only damages params can reference it.
GLOBAL_LIFE_EXPECTANCY_2024 = Parameter(
    73.4,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Global life expectancy at birth (2024), WHO global figure. Was previously set to 79 "
                "(developed-country treatment access), which the adversarial review flagged: a measured "
                "external parameter must carry the measured value; access optimism belongs in explicit "
                "forward-looking parameters, not in a present-day data point.",
    display_name="Global Life Expectancy (2024)",
    unit="years",
    confidence="high",
    last_updated="2024",
    peer_reviewed=True,
    keywords=["life expectancy", "longevity", "lifespan", "actuarial", "demographics"],
    distribution="normal",  # Normal appropriate: tight empirical data, slow-changing
    std_error=2,  # ±2 years (2.5% CV): Captures measurement + projection uncertainty
    # WHO global: 73.4. Regional variance:
    #   - High-income: 80.3 years (Japan 84, US 77)
    #   - Low-income: 63.7 years (Chad 54, Nigeria 55)
    # Tight ±2 years appropriate: actuarial tables very stable, no sudden shifts expected
    validation_min=70,  # Floor: Pessimistic scenario (global conflicts, pandemics)
    validation_max=85,  # Ceiling: Optimistic scenario (longevity breakthroughs, developed countries)
    latex_symbol=r"LE_{global}",  # LaTeX symbol for equations
)

# Bullets per person (depends on GLOBAL_POPULATION_2024 above)
BULLETS_PER_PERSON_ANNUAL = Parameter(
    GLOBAL_BULLETS_PURCHASABLE_ANNUAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/extinction-surplus.qmd",
    source_type=SourceType.CALCULATED,
    confidence="medium",
    description="Number of bullets per person on Earth that could be purchased annually "
                "with the global military budget. A purchasing power metric illustrating "
                "the scale of military spending.",
    display_name="Bullets Purchasable Per Person Per Year",
    unit="rounds/person/year",
    formula="GLOBAL_BULLETS_PURCHASABLE_ANNUAL / GLOBAL_POPULATION_2024",
    inputs=["GLOBAL_BULLETS_PURCHASABLE_ANNUAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["GLOBAL_BULLETS_PURCHASABLE_ANNUAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["bullets", "per person", "per capita", "overkill", "purchasing power"],
    latex_symbol=r"n_{bullets/person}",
)

GLOBAL_AVG_INCOME_2025 = Parameter(
    GLOBAL_GDP_2025 / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Global average income (GDP per capita) in 2025 baseline.",
    display_name="Global Average Income (2025 Baseline)",
    unit="USD",
    formula="GLOBAL_GDP_2025 ÷ GLOBAL_POPULATION_2024",
    keywords=["income", "per capita", "baseline", "2025", "global"],
    inputs=["GLOBAL_GDP_2025", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["GLOBAL_GDP_2025"] / ctx["GLOBAL_POPULATION_2024"],
    latex_symbol=r"\bar{y}_{0}",
)

# Cumulative property/infrastructure destruction from wars since 1900
WAR_PROPERTY_DESTRUCTION_SINCE_1900 = Parameter(
    45_000_000_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref="harrison-economics-wwii",
    source_type="definition",
    confidence="low",
    description="Cumulative property and infrastructure destruction from major wars since 1900 (2024 USD). "
                "WWI ~$5T, WWII ~$23T, Korea ~$0.5T, Vietnam ~$1T, post-9/11 ~$8T, other ~$7.5T.",
    display_name="Cumulative Property Destruction from War Since 1900",
    unit="USD",
    distribution="uniform",
    confidence_interval=(30_000_000_000_000, 60_000_000_000_000),
    keywords=["war", "property", "destruction", "infrastructure", "cumulative", "since 1900"],
    latex_symbol=r"D_{property}",
)

# Cumulative environmental destruction from wars since 1900
WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900 = Parameter(
    5_000_000_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref="brown-costs-of-war-environmental",
    source_type="definition",
    confidence="low",
    description="Cumulative environmental destruction from wars since 1900 (2024 USD). "
                "Nuclear testing, Agent Orange, Gulf War oil fires, DU contamination, "
                "Zone Rouge, military CO2 emissions, land mines.",
    display_name="Cumulative Environmental Destruction from War Since 1900",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(2_000_000_000_000, 10_000_000_000_000),
    keywords=["war", "environmental", "destruction", "contamination", "cumulative", "since 1900"],
    latex_symbol=r"D_{env}",
)

# Global GDP per capita in 1900 (2024 dollars, Maddison Project)
GLOBAL_GDP_PER_CAPITA_1900 = Parameter(
    3_150,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref="maddison-project-2020",
    source_type="external",
    confidence="medium",
    description="Global GDP per capita in 1900 in constant 2024 USD. Maddison Project: ~$1,260 "
                "in 1990 international dollars, adjusted to 2024 USD (~2.5x).",
    display_name="Global GDP per Capita in 1900",
    unit="USD/person",
    distribution="normal",
    std_error=500,
    keywords=["GDP", "per capita", "1900", "historical", "baseline", "Maddison"],
    latex_symbol=r"GDP_{pc,1900}",
)

# Compound opportunity cost of war: stacked growth boost from 8 non-overlapping channels
# Ch1: productive reallocation (budget redirect + innovation merged, 0.8-1.5pp)
# Ch2: preserved capital stock (0.2-0.4pp)
# Ch3: population (310M lives + descendants, 0.2-0.4pp)
# Ch4: no trade/refugee drag (0.1-0.3pp)
# Ch5: no environmental damage (0.1-0.2pp)
# Ch6: no Cold War economic isolation (0.1-0.3pp)
# Ch7: institutional quality / no authoritarianism (0.1-0.3pp)
# Ch8: international scientific collaboration (0.05-0.15pp)
WAR_COUNTERFACTUAL_ANNUAL_GROWTH_BOOST = Parameter(
    0.026,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref="costa-rica-peace-dividend",
    source_type="definition",
    confidence="low",
    description="Stacked annual growth boost from 8 non-overlapping war channels. "
                "Ch1: productive reallocation 0.8-1.5pp (budget + innovation merged). "
                "Ch2: preserved capital 0.2-0.4pp. Ch3: population 0.2-0.4pp. "
                "Ch4: no trade drag 0.1-0.3pp. Ch5: no environmental damage 0.1-0.2pp. "
                "Ch6: no Cold War isolation 0.1-0.3pp. Ch7: better institutions 0.1-0.3pp. "
                "Ch8: open scientific collaboration 0.05-0.15pp. "
                "Low 1.65pp, mid 2.6pp, high 3.55pp.",
    display_name="Peace Growth Boost (8 Channels, Overlap-Corrected)",
    unit="percentage points",
    distribution="uniform",
    confidence_interval=(0.0165, 0.0355),
    keywords=["war", "growth", "compound", "opportunity cost", "GDP", "penalty"],
    latex_symbol=r"g_{war,penalty}",
)

# Counterfactual GDP per capita if no wars since 1900
WAR_COUNTERFACTUAL_GDP_PER_CAPITA = Parameter(
    GLOBAL_GDP_PER_CAPITA_1900 * (1 + (GLOBAL_AVG_INCOME_2025 / GLOBAL_GDP_PER_CAPITA_1900) ** (1/124) - 1 + WAR_COUNTERFACTUAL_ANNUAL_GROWTH_BOOST) ** 124,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    confidence="low",
    description="Counterfactual global GDP per capita if all wars abolished since 1900. "
                "Actual is $14,375. Mid-range counterfactual: $333,636 (23.2x richer). "
                "8 non-overlapping channels at +2.6pp.",
    display_name="GDP per Capita in Peace Timeline",
    unit="USD/person",
    formula="GLOBAL_GDP_PER_CAPITA_1900 × (1 + ACTUAL_CAGR + WAR_COUNTERFACTUAL_ANNUAL_GROWTH_BOOST)^124",
    latex=r"""\begin{aligned}
GDP_{pc,peace} &= GDP_{pc,1900} \times \left(1 + \left(\frac{\bar{y}_{0}}{GDP_{pc,1900}}\right)^{1/124} - 1 + g_{war,penalty}\right)^{124} \\
&= \$3.15K \times \left(1 + \left(\frac{\$14.4K}{\$3.15K}\right)^{1/124} - 1 + 2.6\%\right)^{124} \\
&= \$334K
\end{aligned}""",
    inputs=["GLOBAL_GDP_PER_CAPITA_1900", "WAR_COUNTERFACTUAL_ANNUAL_GROWTH_BOOST", "GLOBAL_AVG_INCOME_2025"],
    compute=lambda ctx: ctx["GLOBAL_GDP_PER_CAPITA_1900"] * (1 + (ctx["GLOBAL_AVG_INCOME_2025"] / ctx["GLOBAL_GDP_PER_CAPITA_1900"]) ** (1/124) - 1 + ctx["WAR_COUNTERFACTUAL_ANNUAL_GROWTH_BOOST"]) ** 124,
    keywords=["war", "counterfactual", "GDP", "per capita", "opportunity cost"],
    latex_symbol=r"GDP_{pc,peace}",
)

# Lost GDP per capita (counterfactual minus actual)
WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA = Parameter(
    WAR_COUNTERFACTUAL_GDP_PER_CAPITA - GLOBAL_AVG_INCOME_2025,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Annual GDP per capita lost due to compound war effects since 1900",
    display_name="Annual Lost GDP per Capita from War",
    unit="USD/person/year",
    formula="WAR_COUNTERFACTUAL_GDP_PER_CAPITA - GLOBAL_AVG_INCOME_2025",
    inputs=["WAR_COUNTERFACTUAL_GDP_PER_CAPITA", "GLOBAL_AVG_INCOME_2025"],
    compute=lambda ctx: ctx["WAR_COUNTERFACTUAL_GDP_PER_CAPITA"] - ctx["GLOBAL_AVG_INCOME_2025"],
    keywords=["war", "lost", "GDP", "per capita", "opportunity cost"],
    latex_symbol=r"GDP_{pc,lost}",
)

# Total annual lost GDP (lost per capita × world population)
WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL = Parameter(
    WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA * GLOBAL_POPULATION_2024,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    confidence="low",
    description="Total annual global GDP lost to compound war effects since 1900. "
                "Lost GDP per capita × 8 billion people.",
    display_name="Annual Lost GDP Global from War",
    unit="USD/year",
    formula="WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA × GLOBAL_POPULATION_2024",
    inputs=["WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA"] * ctx["GLOBAL_POPULATION_2024"],
    keywords=["war", "lost", "GDP", "total", "compound", "opportunity cost", "annual"],
    latex_symbol=r"GDP_{lost,total}",
)

# The headline number: how many times richer every person would be without war
WAR_COUNTERFACTUAL_INCOME_MULTIPLE = Parameter(
    WAR_COUNTERFACTUAL_GDP_PER_CAPITA / GLOBAL_AVG_INCOME_2025,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    confidence="low",
    description="How many times richer the average person would be if wars had been abolished in 1900. "
                "Counterfactual GDP per capita / actual GDP per capita.",
    display_name="Peace Income Multiple (How Much Richer Without War)",
    unit="x",
    formula="WAR_COUNTERFACTUAL_GDP_PER_CAPITA / GLOBAL_AVG_INCOME_2025",
    inputs=["WAR_COUNTERFACTUAL_GDP_PER_CAPITA", "GLOBAL_AVG_INCOME_2025"],
    compute=lambda ctx: ctx["WAR_COUNTERFACTUAL_GDP_PER_CAPITA"] / ctx["GLOBAL_AVG_INCOME_2025"],
    keywords=["war", "income", "multiple", "richer", "counterfactual", "compound"],
    latex_symbol=r"M_{war,income}",
)

# Lost-prosperity-only damages: representative full-life cohort exposure, undiscounted,
# single-coherent-theory pleading. NOT a per-individual award, it is the lifetime exposure
# computed for a representative person who experiences the full WHO global life-expectancy
# horizon. Actual per-individual award would scale by remaining life expectancy at the
# time of pleading. Implicitly captures war deaths, property destruction, and medical
# opportunity cost via their drag on compound growth, so it cannot be added to the body-
# count ledger.
LOST_PROSPERITY_LIFETIME_DAMAGES_PER_CAPITA = Parameter(
    WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA * GLOBAL_LIFE_EXPECTANCY_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Representative full-life cohort exposure: lifetime lost earnings under the "
                "8-channel compound peace economy counterfactual, undiscounted, over WHO global "
                "life expectancy at birth. NOT a uniform per-individual award. A 5-year-old, "
                "45-year-old, and 85-year-old plaintiff would each have a different remaining-life "
                "horizon; this number is the representative full-cohort exposure used as the "
                "single-theory headline. Implicitly captures war deaths, property destruction, and "
                "medical opportunity cost via their drag on compound growth, so cannot be added to "
                "the body-count ledger.",
    display_name="Lost-Prosperity-Only Lifetime Damages, Representative Full-Life Cohort",
    unit="USD/person",
    formula="WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA × GLOBAL_LIFE_EXPECTANCY_2024",
    inputs=["WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA", "GLOBAL_LIFE_EXPECTANCY_2024"],
    compute=lambda ctx: ctx["WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA"] * ctx["GLOBAL_LIFE_EXPECTANCY_2024"],
    keywords=["lost prosperity", "lifetime", "damages", "per capita", "cohort", "single theory", "lost profits"],
    latex_symbol=r"D_{prosperity,life,pc}",
)

LOST_PROSPERITY_LIFETIME_DAMAGES_TOTAL = Parameter(
    WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL * GLOBAL_LIFE_EXPECTANCY_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Global lifetime lost prosperity damages, undiscounted, WHO global life expectancy "
                "horizon. Single coherent damages theory under corporate-liability lost-profits "
                "doctrine: the integral of the productive economy that didn't happen because of the "
                "destructive economy. Cannot be added to the body-count ledger; replaces it as a "
                "single-theory pleading.",
    display_name="Lost-Prosperity-Only Lifetime Damages Total (Cohort Horizon)",
    unit="USD",
    formula="WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL × GLOBAL_LIFE_EXPECTANCY_2024",
    inputs=["WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL", "GLOBAL_LIFE_EXPECTANCY_2024"],
    compute=lambda ctx: ctx["WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL"] * ctx["GLOBAL_LIFE_EXPECTANCY_2024"],
    keywords=["lost prosperity", "lifetime", "damages", "total", "cohort", "single theory", "lost profits"],
    latex_symbol=r"D_{prosperity,life}",
)

# Historical sunk cost total (one-time, not ongoing)
WAR_TOTAL_COST_SINCE_1900 = Parameter(
    CUMULATIVE_MILITARY_SPENDING_FED_ERA + WAR_PROPERTY_DESTRUCTION_SINCE_1900 + WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900 + WAR_QALY_VALUE_LOST_SINCE_1900,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    confidence="low",
    description="Total historical sunk cost of war since 1900: military spending ($170T) + "
                "property destruction ($45T) + environmental ($5T) + QALY value of lives ($1.26Q).",
    display_name="Total Historical Cost of War Since 1900",
    unit="USD",
    formula="CUMULATIVE_MILITARY_SPENDING_FED_ERA + WAR_PROPERTY_DESTRUCTION_SINCE_1900 + WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900 + WAR_QALY_VALUE_LOST_SINCE_1900",
    inputs=["CUMULATIVE_MILITARY_SPENDING_FED_ERA", "WAR_PROPERTY_DESTRUCTION_SINCE_1900", "WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900", "WAR_QALY_VALUE_LOST_SINCE_1900"],
    compute=lambda ctx: ctx["CUMULATIVE_MILITARY_SPENDING_FED_ERA"] + ctx["WAR_PROPERTY_DESTRUCTION_SINCE_1900"] + ctx["WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900"] + ctx["WAR_QALY_VALUE_LOST_SINCE_1900"],
    keywords=["war", "total", "historical", "cost", "cumulative", "quadrillion"],
    latex_symbol=r"C_{war,hist}",
)

WHO_QALY_THRESHOLD_COST_EFFECTIVE = Parameter(
    50000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.WHO_COST_EFFECTIVENESS_THRESHOLD,
    source_type="external",
    description="Cost-effectiveness threshold widely used in US health economics ($50,000/QALY, from 1980s dialysis costs)",
    display_name="Cost-Effectiveness Threshold ($50,000/QALY)",
    unit="USD/QALY",
    keywords=["50k", "qaly", "cost effective", "threshold", "health economics", "dialysis", "benchmark"],
    latex_symbol=r"Threshold_{WHO}",  # LaTeX symbol for equations
)  # Widely-used $50,000/QALY cost-effectiveness threshold

STANDARD_QALYS_PER_LIFE_SAVED = Parameter(
    35,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.QALY_VALUE,
    source_type="external",
    description="Standard QALYs per life saved (WHO life tables)",
    display_name="Standard QALYs per Life Saved",
    unit="QALYs/life",
    keywords=["quality adjusted", "disability adjusted", "health metric", "health benefit", "quality of life", "health status", "life satisfaction"],
    distribution="normal",  # Life expectancy tables well-established
    std_error=7,  # ±20%: reflects age-at-death variance and quality-weighting methodology
    latex_symbol=r"QALY_{life}",  # LaTeX symbol for equations
)  # Standard assumption (WHO life tables)

# Efficacy Lag Duration
EFFICACY_LAG_YEARS = Parameter(
    8.2,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.BIO_CLINICAL_DEVELOPMENT_2021,
    source_type="external",
    description="Regulatory delay for efficacy testing (Phase II/III) post-safety verification. Based on BIO 2021 industry survey. Note: This is for drugs that COMPLETE the pipeline - survivor bias means actual delay for any given disease may be longer if candidates fail and must restart.",
    display_name="Regulatory Delay for Efficacy Testing Post-Safety Verification",
    unit="years",
    formula="TOTAL_TIME_TO_MARKET - PHASE_1_DURATION",
    confidence="medium",  # Downgraded: survivor bias + therapeutic area heterogeneity
    last_updated="2021",
    peer_reviewed=True,
    keywords=["approval lag", "drug lag", "fda delay", "bureaucratic delay", "efficacy lag", "approval", "authorization"],
    distribution="normal",  # Normal appropriate: well-measured empirical data
    std_error=2.0,  # ±2.0 years (~24% CV): Widened to capture:
                    # - Therapeutic area variance (oncology 9.2y, vaccines 7.3y, rare disease 12+y)
                    # - Survivor bias (failed programs not counted in averages)
                    # - Geographic variation (FDA vs EMA vs other regulators)
                    # Economist rationale: 95% CI of ~4-12 years is more defensible
    validation_min=4.0,   # Floor: Breakthrough + priority (COVID vaccines proved <4y possible)
    validation_max=15.0,  # Ceiling: Rare disease with complex endpoints, multiple failures
    latex_symbol=r"T_{lag}",  # LaTeX symbol for equations
)  # 8.2 years efficacy lag (widened uncertainty)

FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER = Parameter(
    (EFFICACY_LAG_YEARS * MONTHS_PER_YEAR) / OXFORD_RECOVERY_TRIAL_DURATION_MONTHS,
    manual_ref="knowledge/problem/fda-is-unsafe-and-ineffective.qmd",
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="calculated",
    description="Efficacy testing time vs Oxford RECOVERY trial (8.2 years ÷ 3 months = 32.8x slower). Compares efficacy lag only (post-safety Phase II/III) since RECOVERY was an efficacy trial.",
    display_name="FDA Efficacy Testing to Oxford RECOVERY Trial Time Multiplier",
    unit="multiplier",
    formula="EFFICACY_LAG_YEARS × MONTHS_PER_YEAR ÷ OXFORD_RECOVERY_TRIAL_DURATION_MONTHS",
    confidence="high",
    keywords=["recovery", "covid", "trial", "fda", "timeline", "comparison", "speed", "multiplier", "oxford"],
    inputs=['EFFICACY_LAG_YEARS', 'OXFORD_RECOVERY_TRIAL_DURATION_MONTHS'],
    compute=lambda ctx: (ctx["EFFICACY_LAG_YEARS"] * MONTHS_PER_YEAR) / ctx["OXFORD_RECOVERY_TRIAL_DURATION_MONTHS"],
    latex_symbol=r"k_{FDA:RECOVERY}",  # LaTeX symbol for equations
)

# ===================================================================
# DISEASE ERADICATION DELAY MODEL (PRIMARY METHODOLOGY)
# ===================================================================
# Simplified approach: Assumes medical progress will eventually cure/manage
# all diseases, but regulatory delay shifts that timeline back 8.2 years.
# This is conservative because many cures would arrive >8 years sooner.
# ===================================================================

# Base WHO global mortality data
GLOBAL_DISEASE_DEATHS_DAILY = Parameter(
    150_000,
    manual_ref="knowledge/strategy/questions.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Total global deaths per day from all disease and aging (WHO Global Burden of Disease 2024)",
    display_name="Global Daily Deaths from Disease and Aging",
    unit="deaths/day",
    confidence="high",
    peer_reviewed=True,
    keywords=["mortality", "global burden", "disease", "aging", "WHO", "daily deaths"],
    distribution="normal",  # Well-established WHO methodology with systematic data collection
    std_error=7500,  # ±5%: reflects reporting gaps + cause-of-death coding variance
    latex_symbol=r"Deaths_{disease,daily}",  # LaTeX symbol for equations
    hide_ci=True,  # CI clutters display for this well-known WHO statistic
)  # 150,000 deaths/day from all disease/aging

GLOBAL_DISEASE_DEATHS_PER_MINUTE = Parameter(
    GLOBAL_DISEASE_DEATHS_DAILY / 1440,
    manual_ref="knowledge/strategy/questions.qmd",
    source_type="calculated",
    description="Global deaths per minute from all disease and aging",
    display_name="Global Deaths per Minute from Disease",
    unit="deaths/minute",
    formula="GLOBAL_DISEASE_DEATHS_DAILY / 1440",
    confidence="high",
    keywords=["mortality", "per minute", "disease", "aging"],
    latex_symbol=r"Deaths_{disease,min}",
    inputs=["GLOBAL_DISEASE_DEATHS_DAILY"],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DEATHS_DAILY"] / 1440,
)

# ===================================================================
# DISEASE BURDEN AND RESEARCH ACCELERATION POTENTIAL
# ===================================================================
# These dictionaries define the disease categories, current cure rates,
# and maximum achievable cure rates with advanced biotechnology.
# Used to calculate fundamentally unavoidable death percentage.
# ===================================================================

# Disease burden as percentage of total deaths
DISEASE_BURDEN = {
    "cardiovascular": 201.1 / 774.6,  # 26.0%
    "cancer": 146.6 / 774.6,  # 18.9%
    "respiratory": 33.4 / 774.6,  # 4.3%
    "neurodegenerative": 27.7 / 774.6,  # 3.6% (Alzheimer's)
    "metabolic": (22.4 + 13.1 + 13.0) / 774.6,  # 6.3% (Diabetes + Kidney + Liver)
    "infectious": 15.0 / 774.6,  # 1.9%
    "accidents": 62.3 / 774.6,  # 8.0%
    "aging_related": 180.0 / 774.6,  # 23.2% (Cellular aging, frailty, multi-morbidity)
    "other": 60.0 / 774.6,  # 7.7%
}

# Current cure/treatment rates by category
# Source: Cancer 5-year survival (69%), cardiovascular prevention data
CURRENT_CURE_RATE = {
    "cardiovascular": 0.50,  # 50% preventable with current knowledge
    "cancer": 0.69,  # 69% 5-year survival rate (2013-2019)
    "respiratory": 0.60,  # Treatable but not curable
    "neurodegenerative": 0.10,  # Very limited current treatments
    "metabolic": 0.70,  # Highly manageable with current drugs
    "infectious": 0.95,  # Antibiotics/vaccines very effective
    "accidents": 0.30,  # Some prevention possible
    "aging_related": 0.05,  # Minimal current progress
    "other": 0.50,  # Mixed
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
    "cardiovascular": 0.95,  # Very high (gene therapy fixes predisposition, regeneration fixes damage, AI optimizes)
    "cancer": 0.95,  # Very high (AI personalized medicine, immunotherapy, early AI detection)
    "respiratory": 0.90,  # High (lung regeneration, gene therapy for genetic conditions)
    "neurodegenerative": 0.80,  # High (stem cells, brain regeneration, epigenetic reprogramming)
    "metabolic": 0.98,  # Nearly complete (gene therapy fixes root causes, AI optimizes treatment)
    "infectious": 0.99,  # Nearly complete (AI discovers treatments instantly)
    "accidents": 0.60,  # Moderate (some prevention AI, trauma regeneration)
    "aging_related": 0.99,  # Nearly complete (cellular reprogramming, epigenetic reversal, organ regeneration) - if we can regenerate organs and reprogram DNA/epigenetics, no biological reason for aging deaths
    "other": 0.95,  # Very high (mix of above technologies)
}

# Calculate fundamentally unavoidable death percentage
# Based on disease burden × (1 - max potential) across all categories
_unavoidable_pct = sum(
    DISEASE_BURDEN[cat] * (1 - RESEARCH_ACCELERATION_POTENTIAL[cat])
    for cat in DISEASE_BURDEN.keys()
)

FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT = Parameter(
    _unavoidable_pct,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Percentage of deaths that are fundamentally unavoidable even with perfect biotechnology (primarily accidents). Calculated as Σ(disease_burden × (1 - max_cure_potential)) across all disease categories.",
    display_name="Fundamentally Unavoidable Death Percentage",
    unit="percentage",
    formula="Σ(DISEASE_BURDEN[cat] × (1 - RESEARCH_ACCELERATION_POTENTIAL[cat]))",
    confidence="medium",
    latex_symbol=r"Pct_{unavoid}",  # LaTeX symbol for equations
)  # ~7.9% unavoidable with aging_related at 0.99

EVENTUALLY_AVOIDABLE_DEATH_PCT = Parameter(
    1 - _unavoidable_pct,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="definition",
    description="Percentage of deaths that are eventually avoidable with sufficient biomedical research and technological advancement. Central estimate ~92% based on ~7.9% fundamentally unavoidable (primarily accidents). Wide uncertainty reflects debate over: (1) aging as addressable vs. fundamental, (2) asymptotic difficulty of last diseases, (3) multifactorial disease complexity.",
    display_name="Eventually Avoidable Death Percentage",
    unit="percentage",
    formula="1 - FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT",
    confidence="low",  # Downgraded: major assumption with genuine uncertainty
    distribution=DistributionType.BETA,  # Bounded [0,1], appropriate for probabilities
    confidence_interval=(0.50, 0.98),  # Skeptical floor: 50% (aging+complex diseases intractable)
                                        # Optimistic ceiling: 98% (only true accidents unavoidable)
                                        # Economist rationale: Extraordinary claim requires wide CI
    latex_symbol=r"Pct_{avoid,death}",  # LaTeX symbol for equations
)  # ~92.1% central, but 50-98% plausible range

GLOBAL_EVENTUALLY_AVOIDABLE_DISEASE_DEATHS_DAILY = Parameter(
    GLOBAL_DISEASE_DEATHS_DAILY * (1 - _unavoidable_pct),
    manual_ref="knowledge/appendix/bombs-vs-biotech-roi.qmd",
    source_type="calculated",
    description="Daily global deaths that are eventually avoidable with sufficient biomedical research. Each day the disease-eradication date slips adds roughly this many deaths to the total schedule cost.",
    display_name="Eventually Avoidable Deaths per Day",
    unit="deaths/day",
    formula="GLOBAL_DISEASE_DEATHS_DAILY × EVENTUALLY_AVOIDABLE_DEATH_PCT",
    confidence="medium",
    keywords=["mortality", "delay", "eventually avoidable", "daily deaths", "schedule cost"],
    latex_symbol=r"Deaths_{avoid,daily}",
    inputs=["GLOBAL_DISEASE_DEATHS_DAILY", "EVENTUALLY_AVOIDABLE_DEATH_PCT"],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DEATHS_DAILY"] * ctx["EVENTUALLY_AVOIDABLE_DEATH_PCT"],
)

# ============================================================================
# GLOBAL DALY BURDEN (WHO Global Burden of Disease)
# ============================================================================
# Used for calculating DALYs averted from accelerating cures

GLOBAL_ANNUAL_DALY_BURDEN = Parameter(
    2_880_000_000,  # 2.88 billion DALYs/year
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.IHME_GBD_2021,
    source_type="external",
    description="Global annual DALY burden from all diseases and injuries (WHO/IHME Global Burden of Disease 2021). Includes both YLL (years of life lost) and YLD (years lived with disability) from all causes.",
    display_name="Global Annual DALY Burden",
    unit="DALYs/year",
    confidence="high",
    peer_reviewed=True,
    keywords=["DALY", "disability", "burden", "WHO", "GBD", "global", "annual", "YLL", "YLD"],
    distribution="normal",
    std_error=150_000_000,  # ~5% uncertainty in measurement methodology
    latex_symbol=r"DALYs_{global,ann}",  # LaTeX symbol for equations
)  # 2.88B DALYs/year (GBD 2021)

# YLD as proportion of total DALYs (for suffering hours calculation)
GLOBAL_YLD_PROPORTION_OF_DALYS = Parameter(
    0.39,  # ~39% of DALYs are YLD (GBD 2021: 1.13B YLD / 2.88B DALYs)
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.IHME_GBD_2021,
    source_type="external",
    description="Proportion of global DALYs that are YLD (years lived with disability) vs YLL (years of life lost). From GBD 2021: 1.13B YLD out of 2.88B total DALYs = 39%.",
    display_name="YLD Proportion of Total DALYs",
    unit="proportion",
    confidence="high",
    peer_reviewed=True,
    keywords=["YLD", "YLL", "DALY", "proportion", "disability", "mortality", "GBD"],
    distribution="normal",
    std_error=0.03,  # ~8% relative uncertainty (range 33-45% across regions/years)
    latex_symbol=r"Pct_{YLD}",  # LaTeX symbol for equations
)  # 39% YLD, 61% YLL

# Eventually avoidable DALY percentage
# Similar to death percentage but accounts for non-fatal chronic conditions
EVENTUALLY_AVOIDABLE_DALY_PCT = Parameter(
    1 - _unavoidable_pct,  # Use same base calculation as deaths
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Percentage of DALYs that are eventually avoidable with sufficient biomedical research. Uses same methodology as EVENTUALLY_AVOIDABLE_DEATH_PCT. Most non-fatal chronic conditions (arthritis, depression, chronic pain) are also addressable through research, so the percentage is similar to deaths.",
    display_name="Eventually Avoidable DALY Percentage",
    unit="percentage",
    formula="1 - FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT",
    confidence="low",
    distribution=DistributionType.BETA,
    confidence_interval=(0.50, 0.98),  # Same range as death percentage
    keywords=["DALY", "avoidable", "curable", "disability", "chronic disease"],
    latex_symbol=r"Pct_{avoid,DALY}",  # LaTeX symbol for equations
)  # ~92% - assumes most disease burden is eventually addressable

# Disease Eradication Delay (PRIMARY ESTIMATE)
# Assumes regulatory delay shifts disease eradication timeline back by efficacy lag period
# Adjusted to exclude fundamentally unavoidable deaths (primarily accidents)
DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED = Parameter(
    int(GLOBAL_DISEASE_DEATHS_DAILY * EFFICACY_LAG_YEARS * DAYS_PER_YEAR * (1 - _unavoidable_pct)),
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Total eventually avoidable deaths from delaying disease eradication by 8.2 years (PRIMARY estimate, conservative). Excludes fundamentally unavoidable deaths (primarily accidents ~7.9%).",
    display_name="Total Deaths from Disease Eradication Delay",
    unit="deaths",
    formula="ANNUAL_DEATHS × EFFICACY_LAG_YEARS × EVENTUALLY_AVOIDABLE_DEATH_PCT",
    confidence="medium",
    keywords=["disease eradication", "regulatory delay", "efficacy lag", "primary estimate", "eventually avoidable"],
    # Uncertainty derived from inputs (DEATHS_DAILY × EFFICACY_LAG × AVOIDABILITY)
    validation_min=250_000_000,  # Floor: Pessimistic avoidability (70%), lower lag (6y)
    validation_max=600_000_000,  # Ceiling: Optimistic avoidability (98%), higher lag (10y)
    inputs=['EFFICACY_LAG_YEARS', 'GLOBAL_DISEASE_DEATHS_DAILY'],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DEATHS_DAILY"] * ctx["EFFICACY_LAG_YEARS"] * DAYS_PER_YEAR * (1 - _unavoidable_pct),
    latex_symbol=r"Deaths_{lag}",  # LaTeX symbol for equations
)  # 413.4M eventually avoidable deaths (down from 449M raw total)

# DELETED: DISEASE_ERADICATION_DELAY_DEATHS_ANNUAL, HISTORICAL_PROGRESS_DEATHS_ANNUAL,
# and DISEASE_ERADICATION_PLUS_ACCELERATION_DEATHS_ANNUAL
# Reason: These "annual" parameters were confusing - they represented the annual rate during
# a one-time 8.2-year timeline shift, NOT perpetual benefits. Replaced with TOTAL parameters
# that show the complete one-time benefit from eliminating the efficacy lag.

# Component values for DALY calculations
REGULATORY_DELAY_MEAN_AGE_OF_DEATH = Parameter(
    62,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Mean age of preventable death from post-safety efficacy testing regulatory delay (Phase 2-4)",
    display_name="Mean Age of Preventable Death from Post-Safety Efficacy Delay",
    unit="years",
    confidence="medium",
    peer_reviewed=True,
    keywords=["age", "mortality", "death", "average", "life expectancy", "post-safety", "efficacy testing"],
    distribution="normal",  # Normal appropriate: age distributions typically Gaussian
    std_error=3,  # ±3 years (~5% CV): Reflects variance across disease categories
    # Economist justification: WHO GBD shows wide age-at-death distribution:
    #   - CVD deaths: mean age 70 (older)
    #   - Cancer deaths: mean age 65 (mid)
    #   - Infectious disease: mean age 45 (younger, esp. developing countries)
    # Using 62 ± 3 is population-weighted average. Consider disease-specific sub-models.
    # Critique: Assumes regulatory delay affects all age groups equally, may overweight elderly
    validation_min=50,  # Floor: Infectious disease-dominated scenario (HIV, TB, malaria)
    validation_max=75,  # Ceiling: Chronic disease-dominated scenario (cancer, CVD, Alzheimer's)
    latex_symbol=r"Age_{death,delay}",  # LaTeX symbol for equations
)

GLOBAL_LIFE_EXPECTANCY_REMAINING_AT_AGE_60 = Parameter(
    21.0,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="who-gho-life-expectancy-age-60-2021",
    source_type="external",
    description="Additional years a person alive at age 60 can expect to live, global both-sexes "
                "(WHO life tables: 21.0 years in 2019; 19.6 in COVID-depressed 2021). This is "
                "CONDITIONAL remaining life expectancy, not life-expectancy-at-birth minus age: "
                "at-birth figures carry child mortality that someone who reached 60 already "
                "survived, so subtracting an age from them understates remaining years by roughly "
                "40% at this age. Used for years-of-life-lost per efficacy-lag death. The GBD "
                "reference life table would give more (~23 years at 60); WHO period tables are "
                "the lower of the two standard choices.",
    display_name="Remaining Life Expectancy at Age 60 (Global)",
    unit="years",
    confidence="high",
    distribution="normal",
    confidence_interval=(19.6, 22.0),
    keywords=["life expectancy", "age 60", "remaining years", "conditional", "WHO", "life table"],
    latex_symbol=r"e_{60}",
)

# Expected life extension from 1% treaty research acceleration (25x trial capacity)
# Bounds are physically constrained: 0 (failure) to accident-limited lifespan - current
# Distribution encodes beliefs about where in that range we'll land
LIFE_EXTENSION_YEARS = Parameter(
    20,  # Conservative median: meaningful progress without assuming miracles
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_ref=ReferenceID.LONGEVITY_ESCAPE_VELOCITY,
    source_type="external",
    description="Expected years of life extension from 1% treaty research acceleration (25x trial capacity). Bounds: 0 (complete failure) to ~150 (accident-limited lifespan minus current). Lognormal distribution allows for breakthrough scenarios.",
    display_name="Life Extension from Treaty Research Acceleration",
    unit="years",
    confidence="low",
    keywords=["life extension", "longevity", "lifespan", "aging", "disease eradication", "research acceleration", "longevity escape velocity"],
    distribution="lognormal",  # Right-skewed: aging reversal scenarios create long tail
    confidence_interval=(5, 100),  # 80% CI: 5 years (minimal progress) to 100 years (LEV achieved)
    # Physically constrained bounds:
    #   - 0 years: Complete failure, nothing works
    #   - 150 years: Accident-limited lifespan (~230 years) minus current (~80 years)
    # Distribution rationale:
    #   - 5 years (P10): Minimal progress, similar to single drug class breakthrough
    #   - 20 years (median): Conservative expectation - disease reduction without aging reversal
    #   - 100 years (P90): Longevity escape velocity achieved (aging reversal works)
    # Context: 25x trial capacity + CRISPR + AI drug discovery + epigenetic reprogramming
    # Key evidence: 109% lifespan extension demonstrated in aged mice (Yamanaka factors)
    validation_min=0,   # Floor: Complete failure
    validation_max=150,  # Ceiling: Accident-limited lifespan (~230 years - 80 baseline)
    latex_symbol=r"T_{extend}",  # LaTeX symbol for equations
)

REGULATORY_DELAY_SUFFERING_PERIOD_YEARS = Parameter(
    6,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Pre-death suffering period during post-safety efficacy testing delay (average years lived with untreated condition while awaiting Phase 2-4 completion)",
    display_name="Pre-Death Suffering Period During Post-Safety Efficacy Delay",
    unit="years",
    confidence="medium",
    peer_reviewed=True,
    keywords=["suffering", "disability", "morbidity", "disease burden", "quality of life", "post-safety", "efficacy testing"],
    distribution="lognormal",  # Lognormal critical: right-skewed, some suffer >>mean duration
    confidence_interval=(4.0, 9.0),  # 80% CI: 4-9 years (widened to ±40% from mean)
    # Economist critique addressed: Widened CI to reflect massive disease heterogeneity
    # CRITICAL: 6 years is CONSTRUCTED ASSUMPTION (not measured): time-to-diagnosis (2y) +
    # time-in-clinical-trial (4-8y). Label as "model assumption" not "external data"
    # Disease-specific variance enormous (3 orders of magnitude):
    #   - Acute (sepsis, stroke): days-weeks (near zero)
    #   - Chronic progressive (ALS, Alzheimer's): 5-15 years
    #   - Manageable chronic (diabetes, hypertension): decades (but not captured in deaths)
    # Using 6 years (CI: 4-9) weighted toward fatal conditions (cancer 5y, CVD 7y, respiratory 4y)
    # Right skew critical: Long-tail (neurodegenerative) suffers 10-15y → lognormal shape matters
    # RECOMMENDATION: Disease-stratified sub-models essential for robustness (acute/chronic/terminal)
    validation_min=2,   # Floor: Acute-dominated scenario (infectious, trauma, fast-progressing cancer)
    validation_max=15,  # Ceiling: Chronic-dominated scenario (Alzheimer's, Parkinson's, long cancers)
    latex_symbol=r"T_{suffering}",  # LaTeX symbol for equations
)

CHRONIC_DISEASE_DISABILITY_WEIGHT = Parameter(
    0.35,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Disability weight for untreated chronic conditions (WHO Global Burden of Disease)",
    display_name="Disability Weight for Untreated Chronic Conditions",
    unit="weight",
    confidence="medium",
    peer_reviewed=True,
    keywords=["disability", "daly", "quality of life", "disease burden", "morbidity", "health status"],
    distribution="normal",  # Normal acceptable: bounded [0,1], symmetric around mid-range
    std_error=0.07,  # ±0.07 (20% CV): Reflects preference heterogeneity + measurement error
    # Economist justification: GBD disability weights methodology (person trade-off, time trade-off)
    # Disease-specific weights show massive variance:
    #   - Mild conditions (tension headache): 0.01-0.05
    #   - Moderate (major depression): 0.40-0.60
    #   - Severe (metastatic cancer, end-stage dementia): 0.70-0.90
    # Using 0.35 ± 0.07 assumes mid-severity chronic (controlled diabetes, mild-moderate COPD)
    # Critique: Weighted average may hide bimodal distribution (many mild + many severe)
    # Preference heterogeneity matters: cultural differences in disability valuation ±20-30%
    # Widened to ±20% (from ±14%) to reflect stated-preference literature variance
    # Justification: Cross-cultural studies show ±25-30% variation; using ±20% as conservative
    validation_min=0.20,  # Floor: Optimistic (mild symptoms, good palliative care access)
    validation_max=0.50,  # Ceiling: Pessimistic (severe symptoms, poor healthcare access)
    latex_symbol=r"DW_{chronic}",  # LaTeX symbol for equations
)

# Morbidity Analysis (DALYs) - Based on Disease Eradication Delay Model
DFDA_EFFICACY_LAG_ELIMINATION_YLL = Parameter(
    DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED
    * (GLOBAL_LIFE_EXPECTANCY_REMAINING_AT_AGE_60 - (REGULATORY_DELAY_MEAN_AGE_OF_DEATH - 60)),
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Years of Life Lost from disease eradication delay deaths (PRIMARY estimate). "
                "Years lost per death = WHO conditional remaining life expectancy at 60, adjusted "
                "down to the mean lag-death age of 62 (~19 years/death). Replaces life-expectancy-"
                "at-birth minus age, which mixed an at-birth measure (carrying child mortality the "
                "deceased already survived) with a conditional question and understated the loss "
                "by ~40%. The linear age adjustment slightly understates remaining years "
                "(conditional life expectancy falls by less than one year per year of age).",
    display_name="Years of Life Lost from Disease Eradication Delay",
    unit="years",
    formula="DEATHS_TOTAL × (REMAINING_LIFE_EXPECTANCY_AT_60 - (MEAN_AGE_OF_DEATH - 60))",
    confidence="medium",
    keywords=["disease eradication", "YLL", "years of life lost", "disease burden", "mortality burden"],
    inputs=["DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED", "GLOBAL_LIFE_EXPECTANCY_REMAINING_AT_AGE_60", "REGULATORY_DELAY_MEAN_AGE_OF_DEATH"],
    compute=lambda ctx: ctx["DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED"]
    * (ctx["GLOBAL_LIFE_EXPECTANCY_REMAINING_AT_AGE_60"] - (ctx["REGULATORY_DELAY_MEAN_AGE_OF_DEATH"] - 60)),
    latex_symbol=r"YLL_{lag}",  # LaTeX symbol for equations
)  # ~7.9B years

DFDA_EFFICACY_LAG_ELIMINATION_YLD = Parameter(
    DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED * REGULATORY_DELAY_SUFFERING_PERIOD_YEARS * CHRONIC_DISEASE_DISABILITY_WEIGHT,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Years Lived with Disability during disease eradication delay (PRIMARY estimate)",
    display_name="Years Lived with Disability During Disease Eradication Delay",
    unit="years",
    formula="DEATHS_TOTAL × SUFFERING_PERIOD × DISABILITY_WEIGHT",
    confidence="medium",
    keywords=["disease eradication", "YLD", "years lived with disability", "disease burden", "morbidity"],
    inputs=["DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED", "REGULATORY_DELAY_SUFFERING_PERIOD_YEARS", "CHRONIC_DISEASE_DISABILITY_WEIGHT"],
    compute=lambda ctx: ctx["DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED"] * ctx["REGULATORY_DELAY_SUFFERING_PERIOD_YEARS"] * ctx["CHRONIC_DISEASE_DISABILITY_WEIGHT"],
    latex_symbol=r"YLD_{lag}",  # LaTeX symbol for equations
)  # 943M years

DFDA_EFFICACY_LAG_ELIMINATION_DALYS = Parameter(
    DFDA_EFFICACY_LAG_ELIMINATION_YLL + DFDA_EFFICACY_LAG_ELIMINATION_YLD,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Total Disability-Adjusted Life Years lost from disease eradication delay (PRIMARY estimate)",
    display_name="Total DALYs Lost from Disease Eradication Delay",
    unit="DALYs",
    formula="YLL + YLD",    confidence="medium",
    keywords=["disease eradication", "DALYs", "disease burden", "primary estimate"],
    # UNCERTAINTY: Propagates from YLL and YLD components (no manual override)
    # Expected uncertainty drivers from components:
    #   - Eventually avoidable death fraction: 85-95% (using 92%) → ±5%
    #   - Mean age of death: 55-65 years (using 62) → ±8%
    #   - Disability weights: 0.25-0.45 (using 0.35) → ±14%
    # Compound: √(5%² + 8%² + 14%²) ≈ 17% measurement uncertainty
    # CRITICAL: This is PARAMETRIC uncertainty. STRUCTURAL uncertainty (eventually avoidable
    # assumption itself) needs separate scenario analysis at 70%, 85%, 95% avoidability
    # Tornado analysis will show which components (YLL vs YLD) drive most variance
    validation_min=4_000_000_000,  # Floor: Pessimistic (higher unavoidable %, lower disability)
    validation_max=12_000_000_000,  # Ceiling: Optimistic (aggressive eradication timeline)
    inputs=["DFDA_EFFICACY_LAG_ELIMINATION_YLL", "DFDA_EFFICACY_LAG_ELIMINATION_YLD"],
    compute=lambda ctx: ctx["DFDA_EFFICACY_LAG_ELIMINATION_YLL"] + ctx["DFDA_EFFICACY_LAG_ELIMINATION_YLD"],
    latex_symbol=r"DALYs_{lag}",  # LaTeX symbol for equations
)  # 7.90B DALYs

# ===== TREATMENT BENEFICIARY MORBIDITY (IQVIA-BASED) =====
# Captures suffering of patients with non-terminal chronic diseases during drug approval delay
# This is SEPARATE from mortality burden - represents people who eventually got treatment
# but suffered during the 8.2-year lag before their medication was available

GLOBAL_CHRONIC_THERAPY_DAYS_ANNUAL = Parameter(
    1_280_000_000_000,  # 1.8 trillion total days of therapy × 71% for chronic conditions
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="iqvia-global-medicines-2024",
    source_type="external",
    description="Annual days of therapy for chronic conditions globally (diabetes, CVD, respiratory, cancer). IQVIA reports 1.8 trillion total days of therapy in 2019, with 71% for chronic conditions.",
    display_name="Annual Days of Chronic Disease Therapy",
    unit="days",
    confidence="medium",
    peer_reviewed=False,  # Industry report, not peer-reviewed
    keywords=["pharmaceutical utilization", "chronic disease", "days of therapy", "IQVIA", "morbidity"],
    distribution="lognormal",  # Utilization data: can't be negative, right-skewed
    confidence_interval=(1_000_000_000_000, 1_500_000_000_000),  # ±20% based on regional variation
    validation_min=800_000_000_000,  # Floor: Conservative estimate
    validation_max=2_000_000_000_000,  # Ceiling: Including under-reported LMICs
    latex_symbol=r"DOT_{chronic}",
)

# Derivation: 1.28T days ÷ 365 days/year ÷ 2.5 avg medications per patient × 70% post-1962 drugs
# = 1.28T ÷ 365 ÷ 2.5 × 0.7 ≈ 980M, rounded to 1B
CHRONIC_DISEASE_TREATED_PATIENTS_ANNUAL = Parameter(
    GLOBAL_CHRONIC_THERAPY_DAYS_ANNUAL / 365 / 2.5 * 0.70,  # Derived from days of therapy
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="iqvia-global-medicines-2024",
    source_type="calculated",
    description="Estimated unique patients receiving chronic disease treatment annually. Derived from IQVIA days of therapy (1.28T) divided by 365 days divided by 2.5 average medications per patient times 70% post-1962 drugs.",
    display_name="Annual Chronic Disease Patients Treated",
    unit="people",
    confidence="low",  # Multiple derivation steps introduce uncertainty
    keywords=["pharmaceutical utilization", "chronic disease", "treatment beneficiaries", "morbidity burden"],
    # Key assumptions:
    #   - 2.5 medications per chronic patient (literature range: 2-4)
    #   - 70% of chronic disease drugs are post-1962 (conservative; could be 80-90%)
    #   - Days of therapy maps to unique patients (polypharmacy adjustment)
    validation_min=500_000_000,  # Floor: Very conservative
    validation_max=2_000_000_000,  # Ceiling: Less adjustment for polypharmacy
    formula="GLOBAL_CHRONIC_THERAPY_DAYS ÷ 365 ÷ 2.5 × 0.70",
    inputs=["GLOBAL_CHRONIC_THERAPY_DAYS_ANNUAL"],
    compute=lambda ctx: ctx["GLOBAL_CHRONIC_THERAPY_DAYS_ANNUAL"] / 365 / 2.5 * 0.70,
    latex_symbol=r"N_{treated}",
)

# Disability weight REDUCTION from treatment (untreated - treated)
# Untreated chronic disease: ~0.35 weight (CHRONIC_DISEASE_DISABILITY_WEIGHT above)
# Treated chronic disease: ~0.10 weight (well-controlled conditions)
# Difference = 0.25 disability avoided per year of treatment
TREATMENT_DISABILITY_REDUCTION = Parameter(
    0.25,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="gbd-disability-weights",
    source_type="external",
    description="Average disability weight reduction from pharmaceutical treatment. Untreated chronic disease averages 0.35 disability weight, treated disease averages 0.10, difference is 0.25.",
    display_name="Treatment Disability Reduction",
    unit="weight",  # Disability weight (0-1 scale)
    confidence="medium",
    peer_reviewed=True,  # GBD disability weights are peer-reviewed
    keywords=["disability weight", "treatment effect", "quality of life", "morbidity reduction"],
    distribution="normal",  # Bounded [0,1], symmetric around mid-range
    confidence_interval=(0.15, 0.35),  # Reflects disease mix and treatment efficacy variation
    # Sensitivity:
    #   - Mild conditions (hypertension): 0.10-0.15 reduction
    #   - Moderate (diabetes, COPD): 0.25-0.35 reduction
    #   - Severe (cancer, heart failure): 0.30-0.50 reduction
    # Using 0.25 as weighted average reflecting chronic disease treatment portfolio
    validation_min=0.10,  # Floor: Mostly mild conditions
    validation_max=0.40,  # Ceiling: Mostly severe conditions with good treatment response
    latex_symbol=r"\Delta DW_{treat}",
)

# Annual YLD from treatment delay - represents suffering during the 8.2 years before
# patients' medications became available. This is SEPARATE from mortality burden.
EFFICACY_LAG_TREATMENT_DELAY_YLD_ANNUAL = Parameter(
    CHRONIC_DISEASE_TREATED_PATIENTS_ANNUAL * EFFICACY_LAG_YEARS * TREATMENT_DISABILITY_REDUCTION,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Annual YLD from treatment delay: patients receiving chronic disease treatment would have collectively avoided this disability if treatments were available 8.2 years earlier. Represents morbidity burden for treatment beneficiaries (distinct from mortality burden).",
    display_name="Treatment Delay YLD - Annual",
    unit="DALYs",
    confidence="low",  # Multiple uncertain inputs
    keywords=["treatment delay", "YLD", "morbidity burden", "chronic disease", "efficacy lag"],
    formula="PATIENTS × EFFICACY_LAG × DISABILITY_REDUCTION",
    inputs=["CHRONIC_DISEASE_TREATED_PATIENTS_ANNUAL", "EFFICACY_LAG_YEARS", "TREATMENT_DISABILITY_REDUCTION"],
    compute=lambda ctx: ctx["CHRONIC_DISEASE_TREATED_PATIENTS_ANNUAL"] * ctx["EFFICACY_LAG_YEARS"] * ctx["TREATMENT_DISABILITY_REDUCTION"],
    # Expected result: 1B × 8.2 × 0.25 = 2.05B YLD/year
    # This is ~150x larger than the mortality-based YLD (14M/year)
    # Reflects that morbidity burden vastly exceeds mortality burden
    latex_symbol=r"YLD_{treat\_delay}",
)

# Economic Valuation (using standardized $150k VSLY)
DFDA_EFFICACY_LAG_ELIMINATION_ECONOMIC_VALUE = Parameter(
    DFDA_EFFICACY_LAG_ELIMINATION_DALYS * STANDARD_ECONOMIC_QALY_VALUE_USD,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total economic loss from delaying disease eradication by 8.2 years (PRIMARY estimate, 2024 USD). Values global DALYs at standardized US/International normative rate ($150k) rather than local ability-to-pay, representing the full human capital loss.",
    display_name="Total Economic Loss from Disease Eradication Delay",
    unit="USD",
    formula="DALYS_TOTAL × VSLY",    confidence="medium",
    keywords=["disease eradication", "economic loss", "deadweight loss", "primary estimate"],
    inputs=['DFDA_EFFICACY_LAG_ELIMINATION_DALYS', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["DFDA_EFFICACY_LAG_ELIMINATION_DALYS"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Value_{lag}",  # LaTeX symbol for equations
)  # $1.191 Quadrillion total economic loss

# TOTAL Economic Loss Parameters (One-Time Benefits from Eliminating 8.2-Year Delay)
# These represent the complete, one-time benefit of eliminating the efficacy lag
# NOT amortized annual values that could mislead by suggesting recurring benefits

# ===== LICHTENBERG (2019) PHARMACEUTICAL IMPACT PARAMETERS =====
# Primary source: NBER WP 25483 "How Many Life-Years Have New Drugs Saved?"
# Key finding: Drugs launched after 1981 saved 148.7M life-years in 2013 across 22 countries
# CI propagated from Table 2 standard errors: β₀₋₁₁=-0.031 (SE=0.008), β₁₂₊=-0.057 (SE=0.013)

# PRIMARY METRIC: Life-years saved (what Lichtenberg actually measured)
PHARMA_LIFE_YEARS_SAVED_ANNUAL = Parameter(
    148_700_000,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="lichtenberg-life-years-saved-2019",
    source_type="external",
    description="Annual life-years saved by pharmaceutical innovations globally. Lichtenberg (2019, NBER WP 25483) found that drugs launched after 1981 saved 148.7M life-years in 2013 across 22 countries using 3-way fixed-effects regression (disease-country-year). 95% CI [79.4M, 239.8M] propagated from Table 2 regression standard errors (β₀₋₁₁=-0.031±0.008, β₁₂₊=-0.057±0.013).",
    display_name="Annual Life-Years Saved by Pharmaceuticals",
    unit="life-years",
    confidence="medium",
    confidence_interval=(79_400_000, 239_800_000),  # Propagated from Lichtenberg Table 2 SEs
    distribution="lognormal",
    keywords=["148.7m", "life-years", "pharmaceutical", "lichtenberg", "nber"],
    latex_symbol=r"LY_{saved,annual}",
)  # 148.7M life-years/year (Lichtenberg 2019), CI: [79.4M, 239.8M]

# Conversion factor: Average life extension per beneficiary
# Used to convert life-years saved to approximate number of lives saved
AVG_LIFE_EXTENSION_PER_BENEFICIARY = Parameter(
    12,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="lichtenberg-life-years-saved-2019",
    source_type="definition",
    description="Average years of life extension per person saved by pharmaceutical interventions. Assumption used to convert life-years saved to approximate lives saved. Based on Lichtenberg's methodology where life-years are calculated from Years of Life Lost (YLL) reductions.",
    display_name="Average Life Extension per Beneficiary",
    unit="years",
    confidence="low",  # This is an assumption, not directly measured
    confidence_interval=(8, 18),  # Wide uncertainty: could be shorter (elderly) or longer (younger patients)
    distribution="triangular",
    keywords=["life extension", "conversion", "assumption"],
    latex_symbol=r"T_{ext}",
)  # 12 years average life extension (assumed)

# DERIVED METRIC: Lives saved (converted from life-years for intuitive communication)
PHARMA_LIVES_SAVED_ANNUAL = Parameter(
    PHARMA_LIFE_YEARS_SAVED_ANNUAL / AVG_LIFE_EXTENSION_PER_BENEFICIARY,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="lichtenberg-life-years-saved-2019",
    source_type="calculated",
    description="Annual lives saved by pharmaceutical interventions globally. Derived from Lichtenberg (2019) finding of 148.7M life-years saved, divided by assumed 12-year average life extension per beneficiary. Note: Life-years is the primary metric; lives is an approximation for intuitive communication.",
    display_name="Annual Lives Saved by Pharmaceuticals",
    unit="deaths",
    confidence="low",  # Lower than life-years due to conversion assumption
    formula="PHARMA_LIFE_YEARS_SAVED_ANNUAL ÷ AVG_LIFE_EXTENSION_PER_BENEFICIARY",
    keywords=["12m", "annual", "lives saved", "pharmaceutical", "lichtenberg", "derived"],
    inputs=['PHARMA_LIFE_YEARS_SAVED_ANNUAL', 'AVG_LIFE_EXTENSION_PER_BENEFICIARY'],
    compute=lambda ctx: ctx["PHARMA_LIFE_YEARS_SAVED_ANNUAL"] / ctx["AVG_LIFE_EXTENSION_PER_BENEFICIARY"],
    latex_symbol=r"Lives_{saved,annual}",
)  # ~12M lives/year (derived from 148.7M life-years ÷ 12 years/life)

# Historical Progress - TOTAL (existing drugs only, excludes future innovation effects)
EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL = Parameter(
    PHARMA_LIVES_SAVED_ANNUAL * EFFICACY_LAG_YEARS,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Total deaths from delaying existing drugs over 8.2-year efficacy lag. One-time impact of eliminating Phase 2-4 testing delay for drugs already approved 1962-2024. Based on Lichtenberg (2019) estimate of 12M lives saved annually × 8.2 years efficacy lag. Excludes innovation acceleration effects.",
    display_name="Total Deaths from Historical Progress Delays",
    unit="deaths",
    formula="PHARMA_LIVES_SAVED_ANNUAL × EFFICACY_LAG_YEARS",
    confidence="medium",
    keywords=["98.4m", "historical", "total", "one-time", "existing drugs"],
    inputs=['PHARMA_LIVES_SAVED_ANNUAL', 'EFFICACY_LAG_YEARS'],
    compute=lambda ctx: ctx["PHARMA_LIVES_SAVED_ANNUAL"] * ctx["EFFICACY_LAG_YEARS"],
    latex_symbol=r"Deaths_{lag,total}",  # LaTeX symbol for equations
)  # 98.4M total deaths (central estimate)

EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS = Parameter(
    EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL
    * (GLOBAL_LIFE_EXPECTANCY_REMAINING_AT_AGE_60 - (REGULATORY_DELAY_MEAN_AGE_OF_DEATH - 60))
    * STANDARD_ECONOMIC_QALY_VALUE_USD,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Total economic loss from delaying existing drugs over 8.2-year efficacy lag. "
                "One-time benefit of eliminating Phase 2-4 delay. Excludes innovation acceleration "
                "effects. Years lost per death uses WHO conditional remaining life expectancy at "
                "60 adjusted to the mean lag-death age (~19 years/death), not life-expectancy-at-"
                "birth minus age, which understated remaining years by ~40%.",
    display_name="Total Economic Loss from Historical Progress Delays",
    unit="USD",
    formula="DEATHS_TOTAL × (REMAINING_LIFE_EXPECTANCY_AT_60 - (MEAN_AGE_OF_DEATH - 60)) × VSLY",
    confidence="medium",  # Inherited from PHARMA_LIVES_SAVED_ANNUAL uncertainty
    keywords=["historical", "total", "one-time", "existing drugs", "efficacy lag"],
    inputs=['GLOBAL_LIFE_EXPECTANCY_REMAINING_AT_AGE_60', 'EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL', 'REGULATORY_DELAY_MEAN_AGE_OF_DEATH', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL"]
    * (ctx["GLOBAL_LIFE_EXPECTANCY_REMAINING_AT_AGE_60"] - (ctx["REGULATORY_DELAY_MEAN_AGE_OF_DEATH"] - 60))
    * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Loss_{lag}",  # LaTeX symbol for equations
)  # ~$290T total (existing drugs only)

# DELETED: EFFICACY_LAG_WITH_INNOVATION_CASCADE_DEATHS_TOTAL and EFFICACY_LAG_WITH_INNOVATION_CASCADE_ECONOMIC_LOSS
# Reason: These used an arbitrary 2× "innovation cascade" multiplier. Replaced by the more rigorous
# queue-based model: TRIAL_CAPACITY_PLUS_EFFICACY_LAG_* parameters which use the empirically-derived
# trial capacity multiplier to calculate cure acceleration.

# Type I vs Type II Error Ratio - Thalidomide Baseline

# Thalidomide disaster parameters (1957-1962)
THALIDOMIDE_CASES_WORLDWIDE = Parameter(
    15_000,  # Conservative midpoint of 10,000-20,000 estimate
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="thalidomide-scandal",
    source_type="external",
    description="Total thalidomide birth defect cases worldwide (1957-1962)",
    display_name="Thalidomide Cases Worldwide",
    unit="cases",
    confidence="medium",
    confidence_interval=(10_000, 20_000),  # Documented range 10,000-20,000 cases
    distribution="lognormal",
    keywords=["thalidomide", "birth defects", "drug safety"],
    latex_symbol=r"N_{thal,global}",  # LaTeX symbol for equations
)

THALIDOMIDE_MORTALITY_RATE = Parameter(
    0.40,  # 40% died within first year
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="thalidomide-scandal",
    source_type="external",
    description="Mortality rate for thalidomide-affected infants (died within first year)",
    display_name="Thalidomide Mortality Rate",
    unit="percentage",
    confidence="high",
    confidence_interval=(0.35, 0.45),  # ±15% on mortality rate
    distribution="lognormal",
    keywords=["thalidomide", "mortality", "infant deaths"],
    latex_symbol=r"Rate_{thal,mort}",  # LaTeX symbol for equations
)

THALIDOMIDE_US_POPULATION_SHARE_1960 = Parameter(
    0.06,  # US was ~6% of world population in 1960
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="us-census-world-population-1960",
    source_type="external",
    description="US share of world population in 1960",
    display_name="US Population Share 1960",
    unit="percentage",
    confidence="high",
    confidence_interval=(0.055, 0.065),  # ±10% on census data
    distribution="lognormal",
    keywords=["population", "demographics"],
    latex_symbol=r"Pct_{US,1960}",  # LaTeX symbol for equations
)

THALIDOMIDE_US_CASES_PREVENTED = Parameter(
    int(THALIDOMIDE_CASES_WORLDWIDE * THALIDOMIDE_US_POPULATION_SHARE_1960),
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Estimated US thalidomide cases prevented by FDA rejection",
    display_name="Thalidomide US Cases Prevented",
    unit="cases",
    formula="WORLDWIDE_CASES × US_POPULATION_SHARE",    confidence="medium",
    keywords=["thalidomide", "FDA", "prevention"],
    inputs=['THALIDOMIDE_CASES_WORLDWIDE', 'THALIDOMIDE_US_POPULATION_SHARE_1960'],
    compute=lambda ctx: ctx["THALIDOMIDE_CASES_WORLDWIDE"] * ctx["THALIDOMIDE_US_POPULATION_SHARE_1960"],
    latex_symbol=r"N_{thal,US,prevent}",  # LaTeX symbol for equations
)

THALIDOMIDE_DISABILITY_WEIGHT = Parameter(
    0.40,  # Moderate-severe disability for limb deformities
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="thalidomide-survivors-health",
    source_type="external",
    description="Disability weight for thalidomide survivors (limb deformities, organ damage)",
    display_name="Thalidomide Disability Weight",
    unit="ratio",
    confidence="medium",
    confidence_interval=(0.32, 0.48),  # ±20% on disability weight
    distribution="lognormal",
    keywords=["thalidomide", "disability", "quality of life"],
    latex_symbol=r"DW_{thal}",  # LaTeX symbol for equations
)

THALIDOMIDE_SURVIVOR_LIFESPAN = Parameter(
    60,  # Many survivors still living in 2020s at ~65 years old
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="thalidomide-survivors-health",
    source_type="external",
    description="Average lifespan for thalidomide survivors",
    display_name="Thalidomide Survivor Lifespan",
    unit="years",
    confidence="medium",
    confidence_interval=(50, 70),  # ±15% on lifespan estimate
    distribution="lognormal",
    keywords=["thalidomide", "longevity", "life expectancy"],
    latex_symbol=r"LE_{thal}",  # LaTeX symbol for equations
)

# Calculate DALYs per "Thalidomide Event"
THALIDOMIDE_DEATHS_PER_EVENT = Parameter(
    float(THALIDOMIDE_US_CASES_PREVENTED) * float(THALIDOMIDE_MORTALITY_RATE),
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Deaths per US-scale thalidomide event",
    display_name="Thalidomide Deaths Per Event",
    unit="deaths",
    formula="US_CASES × MORTALITY_RATE",    confidence="medium",
    keywords=["thalidomide", "mortality"],
    inputs=['THALIDOMIDE_MORTALITY_RATE', 'THALIDOMIDE_US_CASES_PREVENTED'],
    compute=lambda ctx: ctx["THALIDOMIDE_US_CASES_PREVENTED"] * ctx["THALIDOMIDE_MORTALITY_RATE"],
    latex_symbol=r"Deaths_{thal}",  # LaTeX symbol for equations
)

THALIDOMIDE_YLL_PER_EVENT = Parameter(
    THALIDOMIDE_DEATHS_PER_EVENT * 80,  # Infant deaths, 80 years lost per death
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Years of Life Lost per thalidomide event (infant deaths)",
    display_name="Thalidomide YLL Per Event",
    unit="years",
    formula="DEATHS × 80 years",    confidence="medium",
    keywords=["thalidomide", "YLL", "mortality"],
    inputs=['THALIDOMIDE_DEATHS_PER_EVENT'],
    compute=lambda ctx: ctx["THALIDOMIDE_DEATHS_PER_EVENT"] * 80,
    latex_symbol=r"YLL_{thal}",  # LaTeX symbol for equations
)

THALIDOMIDE_SURVIVORS_PER_EVENT = Parameter(
    float(THALIDOMIDE_US_CASES_PREVENTED) * (1 - float(THALIDOMIDE_MORTALITY_RATE)),
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Survivors per US-scale thalidomide event",
    display_name="Thalidomide Survivors Per Event",
    unit="cases",
    formula="US_CASES × (1 - MORTALITY_RATE)",
    confidence="medium",
    keywords=["thalidomide", "survivors"],
    inputs=['THALIDOMIDE_MORTALITY_RATE', 'THALIDOMIDE_US_CASES_PREVENTED'],
    compute=lambda ctx: ctx["THALIDOMIDE_US_CASES_PREVENTED"] * (1 - ctx["THALIDOMIDE_MORTALITY_RATE"]),
    latex_symbol=r"N_{thal,survive}",  # LaTeX symbol for equations
)

THALIDOMIDE_YLD_PER_EVENT = Parameter(
    THALIDOMIDE_SURVIVORS_PER_EVENT * THALIDOMIDE_SURVIVOR_LIFESPAN * THALIDOMIDE_DISABILITY_WEIGHT,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Years Lived with Disability per thalidomide event",
    display_name="Thalidomide YLD Per Event",
    unit="years",
    formula="SURVIVORS × LIFESPAN × DISABILITY_WEIGHT",
    confidence="medium",
    keywords=["thalidomide", "YLD", "disability"],
    inputs=['THALIDOMIDE_DISABILITY_WEIGHT', 'THALIDOMIDE_SURVIVORS_PER_EVENT', 'THALIDOMIDE_SURVIVOR_LIFESPAN'],
    compute=lambda ctx: ctx["THALIDOMIDE_SURVIVORS_PER_EVENT"] * ctx["THALIDOMIDE_SURVIVOR_LIFESPAN"] * ctx["THALIDOMIDE_DISABILITY_WEIGHT"],
    latex_symbol=r"YLD_{thal}",  # LaTeX symbol for equations
)

THALIDOMIDE_DALYS_PER_EVENT = Parameter(
    THALIDOMIDE_YLL_PER_EVENT + THALIDOMIDE_YLD_PER_EVENT,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Total DALYs per US-scale thalidomide event (YLL + YLD)",
    display_name="Thalidomide DALYs Per Event",
    unit="DALYs",
    formula="YLL + YLD",    confidence="medium",
    keywords=["thalidomide", "DALYs", "disease burden"],
    inputs=['THALIDOMIDE_YLD_PER_EVENT', 'THALIDOMIDE_YLL_PER_EVENT'],
    compute=lambda ctx: ctx["THALIDOMIDE_YLL_PER_EVENT"] + ctx["THALIDOMIDE_YLD_PER_EVENT"],
    latex_symbol=r"DALY_{thal}",  # LaTeX symbol for equations
)

# Type I Error: Assuming one Thalidomide-scale disaster EVERY YEAR for 62 years (extreme overestimate)
TYPE_I_ERROR_BENEFIT_DALYS = Parameter(
    THALIDOMIDE_DALYS_PER_EVENT * 62,  # 1962-2024 period
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Maximum DALYs saved by FDA preventing unsafe drugs over 62-year period 1962-2024 (extreme overestimate: one Thalidomide-scale event per year)",
    display_name="Maximum DALYs Saved by FDA Preventing Unsafe Drugs (1962-2024)",
    unit="DALYs",
    formula="THALIDOMIDE_DALYS_PER_EVENT × 62 years",    confidence="low",
    conservative=False,  # This is an extreme overestimate of benefits
    keywords=["Type I error", "FDA", "drug safety", "disease burden", "disability burden", "global burden of disease", "suffering", "approval", "1962-2024"],
    inputs=['THALIDOMIDE_DALYS_PER_EVENT'],
    compute=lambda ctx: ctx["THALIDOMIDE_DALYS_PER_EVENT"] * 62,
    latex_symbol=r"DALY_{TypeI}",  # LaTeX symbol for equations
)

TYPE_II_ERROR_COST_RATIO = Parameter(
    DFDA_EFFICACY_LAG_ELIMINATION_DALYS / TYPE_I_ERROR_BENEFIT_DALYS,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Ratio of Type II error cost to Type I error benefit (harm from delay vs. harm prevented)",
    display_name="Ratio of Type II Error Cost to Type I Error Benefit",
    unit="ratio",
    formula="TYPE_II_COST ÷ TYPE_I_BENEFIT",
    confidence="medium",
    keywords=["approval lag", "drug lag", "fda delay", "bureaucratic delay", "efficacy lag", "approval"],
    inputs=['DFDA_EFFICACY_LAG_ELIMINATION_DALYS', 'TYPE_I_ERROR_BENEFIT_DALYS'],
    compute=lambda ctx: ctx["DFDA_EFFICACY_LAG_ELIMINATION_DALYS"] / ctx["TYPE_I_ERROR_BENEFIT_DALYS"],
    latex_symbol=r"Ratio_{TypeII}",  # LaTeX symbol for equations
)

# Peace dividend health benefits
TREATY_LIVES_SAVED_ANNUAL_GLOBAL = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL * TREATY_REDUCTION_PCT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Annual lives saved from 1% reduction in conflict deaths",
    display_name="Annual Lives Saved from 1% Reduction in Conflict Deaths",
    unit="lives/year",
    formula="TOTAL_DEATHS × REDUCTION_PCT",
    keywords=["1%", "deaths prevented", "life saving", "mortality reduction", "deaths averted", "one percent", "international agreement"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL"] * ctx["TREATY_REDUCTION_PCT"],
    latex_symbol=r"Lives_{treaty,ann}",  # LaTeX symbol for equations
)  # 2,446 lives
TREATY_QALYS_GAINED_ANNUAL_GLOBAL = Parameter(
    TREATY_LIVES_SAVED_ANNUAL_GLOBAL * STANDARD_QALYS_PER_LIFE_SAVED,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Annual QALYs gained from peace dividend (lives saved × QALYs/life)",
    display_name="Annual QALYs Gained from Peace Dividend",
    unit="QALYs/year",
    formula="LIVES_SAVED × QALYS_PER_LIFE",
    keywords=["1%", "cost effectiveness", "value for money", "disease burden", "cost per daly", "cost per qaly", "deaths prevented"],
    inputs=['STANDARD_QALYS_PER_LIFE_SAVED', 'TREATY_LIVES_SAVED_ANNUAL_GLOBAL'],
    compute=lambda ctx: ctx["TREATY_LIVES_SAVED_ANNUAL_GLOBAL"] * ctx["STANDARD_QALYS_PER_LIFE_SAVED"],
    latex_symbol=r"QALY_{treaty,ann}",  # LaTeX symbol for equations
)  # 85,610 QALYs


# DELETED: TREATY_TOTAL_LIVES_SAVED_DAILY
# Was derived from deleted TREATY_TOTAL_LIVES_SAVED_ANNUAL (which mixed one-time + recurring)

# ---
# CAMPAIGN COSTS
# ---
# Updated to $1B VICTORY Incentive Alignment Bond model: Lobbying $650M + Referendum $300M + Reserve $50M
# Tech R&D removed from campaign (post-treaty implementation funded by $27B/year)
# Legal/ops/partnerships rolled into main campaign categories

# Source: /knowledge/appendix/campaign-financing-roadmap.qmd#capital-structure-campaign-vs-implementation
TREATY_CAMPAIGN_DURATION_YEARS = Parameter(
    4,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="definition",
    description="Treaty campaign duration (3-5 year range, using midpoint)",
    display_name="Treaty Campaign Duration",
    unit="years",
    keywords=["1%", "one percent", "international agreement", "peace treaty", "agreement", "pact", "duration"],
    distribution="triangular",  # Documented range with most likely midpoint
    confidence_interval=(3, 5),  # 3-5 year range as specified
    latex_symbol=r"T_{campaign}",  # LaTeX symbol for equations
)  # 3-5 year range, using midpoint

# Campaign budget breakdown - Three main categories

# Viral Referendum Budget (with uncertainty range from optimistic to worst-case scenarios)
# Calculation for 280M verified votes:
# - Optimistic ($150M): $0.20/vote avg (strong virality, minimal tiered pricing) = $35M platform + $58M verification + $56M referrals + $5M marketing
# - Realistic ($250M): $0.50/vote avg (moderate tiered pricing per diffusion curve) = $35M platform + $62M verification + $140M referrals + $15M marketing
# - Worst-case ($410M): $1.05/vote avg (heavy tiered to reach laggards) = $35M platform + $67M verification + $294M referrals + $15M marketing
# Based on research: PayPal optimal $10-20/referral (1999-2001, ~$18-36 inflation-adjusted), but survey votes worth less than financial product signups.
# Biometric verification: $0.15-0.25 at 300M+ scale (ComplyCube, Ondato pricing data from references.qmd).
# Diffusion theory predicts increasing marginal costs: innovators/early adopters ($0.20-0.25), early majority ($0.50), late majority ($0.75-1.00), laggards ($1.50-2.00).
TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE = Parameter(
    250_000_000,  # Realistic scenario with $0.50/vote average
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    confidence_interval=(150_000_000, 410_000_000),  # Optimistic ($0.20/vote) to worst-case ($1.05/vote)
    source_type="definition",
    description="Viral referendum budget for 280M verified votes (base: $250M realistic with $0.50/vote avg, range: $150M optimistic $0.20/vote to $410M worst-case $1.05/vote). Components: platform ($35M), verification infrastructure (280M × friction × $0.18-0.20), tiered referral payments (varies by virality and marginal cost curve per diffusion theory), marketing seed ($5-15M). Based on PayPal referral economics ($18-36 inflation-adjusted) and biometric verification pricing ($0.15-0.25 at 300M+ scale).",
    display_name="Viral Referendum Budget",
    unit="USD",
    formula="PLATFORM + VERIFICATION + PAYMENTS (tiered by adopter segment) + MARKETING",
    confidence="medium",
    keywords=["150.0m", "250.0m", "410.0m", "1%", "viral referendum", "global survey", "one percent", "campaign budget", "referendum cost", "280m votes", "0.20 per vote", "0.50 per vote"],
    latex_symbol=r"Budget_{viral,base}",  # LaTeX symbol for equations
    hide_ci=True,  # CI clutters display for budget components
)  # Base: $250M (realistic $0.50/vote avg), Range: $150M (optimistic $0.20/vote) to $410M (worst-case $1.05/vote)

TREATY_CAMPAIGN_BUDGET_LOBBYING = Parameter(
    650_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Political lobbying campaign: direct lobbying (US/EU/G20), Super PACs, opposition research, staff, legal/compliance. Budget exceeds combined pharma ($300M/year) and military-industrial complex ($150M/year) lobbying to ensure competitive positioning. Referendum relies on grassroots mobilization and earned media, while lobbying requires matching or exceeding opposition spending for political viability.",
    display_name="Political Lobbying Campaign: Direct Lobbying, Super Pacs, Opposition Research, Staff, Legal/Compliance",
    unit="USD",
    confidence="low",  # Most uncertain component
    keywords=["650.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"],
    distribution="lognormal",  # Heavily right-skewed: opposition spending unpredictable
    confidence_interval=(325e6, 1300e6),  # 80% CI: $325M-$1.3B (±50% uncertainty, asymmetric)
    # Rationale: Must outspend pharma ($300M) + MIC ($150M) = $450M baseline.
    # If opposition mobilizes heavily (e.g., full MIC + Big Pharma alliance),
    # could need $1B+. If unopposed, could be as low as $325M.
    # Planning fallacy + political unpredictability = wide right-skewed range
    validation_min=200_000_000,   # Floor: Minimal lobbying (weak opposition)
    validation_max=2_000_000_000,  # Ceiling: Full-scale opposition war chest
    latex_symbol=r"Budget_{lobby,treaty}",  # LaTeX symbol for equations
    hide_ci=True,  # CI clutters display for budget components
)  # $650M total lobbying (outspends pharma + MIC combined)

TREATY_CAMPAIGN_BUDGET_RESERVE = Parameter(
    100_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Reserve fund / contingency buffer (10% of total campaign cost). Using industry standard 10% for complex campaigns with potential for unforeseen legal challenges, opposition response, or regulatory delays. Conservative lower bound of $20M (2%) reflects transparent budget allocation and predictable referendum/lobbying costs.",
    display_name="Reserve Fund / Contingency Buffer",
    unit="USD",
    confidence="medium",
    keywords=["100.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"],
    distribution="lognormal",
    confidence_interval=(20e6, 150e6),  # 80% CI: $20M-$150M (reflects 2-15% contingency range)
    # Rationale: Contingency by definition covers unknowns. Could be barely tapped ($20M)
    # or fully depleted + need more ($100M). Wide range reflects inherent unpredictability.
    validation_min=10_000_000,   # Floor: Minimal contingency
    validation_max=150_000_000,  # Ceiling: Major unforeseen costs
    latex_symbol=r"Budget_{reserve}",  # LaTeX symbol for equations
    hide_ci=True,  # CI clutters display for budget components
)  # $50M reserve

# Total campaign cost (calculated from components)
TREATY_CAMPAIGN_TOTAL_COST = Parameter(
    TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE + TREATY_CAMPAIGN_BUDGET_LOBBYING + TREATY_CAMPAIGN_BUDGET_RESERVE,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total treaty campaign cost (100% VICTORY Incentive Alignment Bonds)",
    display_name="Total 1% Treaty Campaign Cost",
    unit="USD",
    formula="REFERENDUM + LOBBYING + RESERVE",    confidence="high",
    keywords=["1%", "impact investing", "pay for success", "one percent", "debt instrument", "development finance", "fixed income"],
    # UNCERTAINTY: Propagates from component budgets (REFERENDUM, LOBBYING, RESERVE)
    # Expected ±50% given unprecedented scale (no manual override)
    # Comparables: Brexit campaigns ~£40M, Ottawa Treaty ~$10M (1997 dollars)
    # This is 20x larger than any treaty campaign, weak precedents justify wide uncertainty
    # Right skew expected: cost overruns more likely than savings (planning fallacy, scope creep)
    # Tornado analysis will show which budget components drive most variance
    validation_min=500_000_000,   # Floor: Bare minimum (digital-only, no paid media)
    validation_max=3_000_000_000,  # Ceiling: Full traditional + opposition response
    inputs=["TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE", "TREATY_CAMPAIGN_BUDGET_LOBBYING", "TREATY_CAMPAIGN_BUDGET_RESERVE"],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE"] + ctx["TREATY_CAMPAIGN_BUDGET_LOBBYING"] + ctx["TREATY_CAMPAIGN_BUDGET_RESERVE"],
    latex_symbol=r"Cost_{campaign}",  # LaTeX symbol for equations
    hide_ci=True,  # CI clutters display for this summary cost
)  # $1B total campaign cost (all VICTORY Incentive Alignment Bonds)

TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED = Parameter(
    TREATY_CAMPAIGN_TOTAL_COST / TREATY_CAMPAIGN_DURATION_YEARS,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Amortized annual campaign cost (total cost ÷ campaign duration)",
    display_name="Amortized Annual Treaty Campaign Cost",
    unit="USD/year",
    formula="TOTAL_COST ÷ DURATION",    keywords=["1%", "one percent", "international agreement", "peace treaty", "yearly", "agreement", "costs"],
    inputs=['TREATY_CAMPAIGN_DURATION_YEARS', 'TREATY_CAMPAIGN_TOTAL_COST'],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_TOTAL_COST"] / ctx["TREATY_CAMPAIGN_DURATION_YEARS"],
    latex_symbol=r"Cost_{camp,amort}",  # LaTeX symbol for equations
)  # $250M

# Campaign phase budgets
CAMPAIGN_PHASE1_BUDGET = Parameter(
    200_000_000,
    manual_ref="knowledge/solution/ai-coordination-army.qmd",
    source_type="definition",
    description="Phase 1 campaign budget (Foundation, Year 1)",
    display_name="Phase 1 Campaign Budget",
    unit="USD",
    keywords=["200.0m", "first phase", "safety trial", "p1", "phase i", "phase1", "campaign"],
    confidence_interval=(140_000_000, 260_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{phase1}",  # LaTeX symbol for equations
)  # $200M for Phase 1

CAMPAIGN_PHASE2_BUDGET = Parameter(
    500_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Phase 2 campaign budget (Scale & Momentum, Years 2-3)",
    display_name="Phase 2 Campaign Budget",
    unit="USD",
    keywords=["500.0m", "efficacy trial", "second phase", "p2", "phase ii", "phase2", "campaign"],
    confidence_interval=(350_000_000, 650_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{phase2}",  # LaTeX symbol for equations
)  # $500M for Phase 2

CAMPAIGN_MEDIA_BUDGET_MIN = Parameter(
    500_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Minimum mass media campaign budget",
    display_name="Minimum Mass Media Campaign Budget",
    unit="USD",
    keywords=["campaign", "media", "budget", "min", "500.0m"],
    confidence_interval=(350_000_000, 650_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{media,min}",  # LaTeX symbol for equations
)  # $500M minimum for mass media

CAMPAIGN_MEDIA_BUDGET_MAX = Parameter(
    1_000_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Maximum mass media campaign budget",
    display_name="Maximum Mass Media Campaign Budget",
    unit="USD",
    keywords=["campaign", "media", "budget", "max", "1.0b"],
    confidence_interval=(700_000_000, 1_300_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{media,max}",  # LaTeX symbol for equations
)  # $1B maximum for mass media

CAMPAIGN_STAFF_BUDGET = Parameter(
    40_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Campaign core team staff budget",
    display_name="Campaign Core Team Staff Budget",
    unit="USD",
    keywords=["campaign", "staff", "budget", "40.0m"],
    confidence_interval=(28_000_000, 52_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{staff}",  # LaTeX symbol for equations
)  # $40M for core team

# Detailed campaign budget line items (in millions USD)
CAMPAIGN_LEGAL_AI_BUDGET = Parameter(
    50_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="AI-assisted legal work budget",
    display_name="AI-Assisted Legal Work Budget",
    unit="USD",
    keywords=["campaign", "legal", "budget", "50.0m"],
    confidence_interval=(35_000_000, 65_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{legal,AI}",  # LaTeX symbol for equations
)

CAMPAIGN_VIRAL_CONTENT_BUDGET = Parameter(
    40_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Viral marketing content creation budget",
    display_name="Viral Marketing Content Creation Budget",
    unit="USD",
    keywords=["campaign", "viral", "content", "budget", "40.0m"],
    confidence_interval=(28_000_000, 52_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{viral}",  # LaTeX symbol for equations
)

CAMPAIGN_COMMUNITY_ORGANIZING = Parameter(
    30_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Community organizing and ambassador program budget",
    display_name="Community Organizing and Ambassador Program Budget",
    unit="USD",
    keywords=["campaign", "community", "organizing", "30.0m"],
    confidence_interval=(21_000_000, 39_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{community}",  # LaTeX symbol for equations
)

CAMPAIGN_LOBBYING_US = Parameter(
    50_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="US lobbying campaign budget",
    display_name="US Lobbying Campaign Budget",
    unit="USD",
    keywords=["campaign", "lobbying", "50.0m"],
    confidence_interval=(35_000_000, 65_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{lobby,US}",  # LaTeX symbol for equations
)

CAMPAIGN_LOBBYING_EU = Parameter(
    40_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="EU lobbying campaign budget",
    display_name="EU Lobbying Campaign Budget",
    unit="USD",
    keywords=["campaign", "lobbying", "40.0m"],
    confidence_interval=(28_000_000, 52_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{lobby,EU}",  # LaTeX symbol for equations
)

CAMPAIGN_LOBBYING_G20_MILLIONS = Parameter(
    35_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="G20 countries lobbying budget",
    display_name="G20 Countries Lobbying Budget",
    unit="USD",
    keywords=["campaign", "lobbying", "g20", "millions", "35.0m"],
    latex_symbol=r"Budget_{lobby,G20}",  # LaTeX symbol for equations
)

CAMPAIGN_DEFENSE_LOBBYIST_BUDGET = Parameter(
    50_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Budget for co-opting defense industry lobbyists",
    display_name="Budget for Co-Opting Defense Industry Lobbyists",
    unit="USD",
    keywords=["50.0m", "armed forces", "conflict", "lobbyist", "armed conflict", "military action", "warfare"],
    confidence_interval=(35_000_000, 65_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{lobby,def}",  # LaTeX symbol for equations
)

DEFENSE_LOBBYING_ANNUAL = Parameter(
    198_000_000,
    manual_ref="knowledge/appendix/faq.qmd",
    source_ref=ReferenceID.LOBBYING_SPEND_DEFENSE,
    source_type="external",
    confidence="high",
    description="Annual military sector lobbying spending. OpenSecrets reports the 2025 actual at "
                "$198.0 million, the top of a three-year climb: $142.9M (2023), $159.5M (2024), "
                "$198.0M (2025)",
    display_name="Annual Military Sector Lobbying",
    unit="USD/year",
    peer_reviewed=True,
    last_updated="2025",
    confidence_interval=(190_000_000, 210_000_000),  # 2025 actual; narrow band around reported figure
    keywords=["198.0m", "armed forces", "yearly", "conflict", "costs", "funding", "investment"],
    latex_symbol=r"Lobby_{def,ann}",  # LaTeX symbol for equations
)

CAMPAIGN_SUPER_PAC_BUDGET = Parameter(
    30_000_000,
    manual_ref="knowledge/legal/election-law.qmd",
    source_type="definition",
    description="Super PAC campaign expenditures",
    display_name="Super PAC Campaign Expenditures",
    unit="USD",
    keywords=["campaign", "super", "pac", "budget", "30.0m"],
    confidence_interval=(21_000_000, 39_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{PAC}",  # LaTeX symbol for equations
)

CAMPAIGN_OPPOSITION_RESEARCH = Parameter(
    25_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Opposition research and rapid response",
    display_name="Opposition Research and Rapid Response",
    unit="USD",
    keywords=["25.0m", "investigation", "r&d", "science", "study", "discovery", "innovation"],
    confidence_interval=(17_500_000, 32_500_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{oppo}",  # LaTeX symbol for equations
)

CAMPAIGN_PILOT_PROGRAMS = Parameter(
    30_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Pilot program testing in small countries",
    display_name="Pilot Program Testing in Small Countries",
    unit="USD",
    keywords=["campaign", "pilot", "programs", "30.0m"],
    confidence_interval=(21_000_000, 39_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{pilot}",  # LaTeX symbol for equations
)

CAMPAIGN_LEGAL_WORK = Parameter(
    60_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Legal drafting and compliance work",
    display_name="Legal Drafting and Compliance Work",
    unit="USD",
    keywords=["campaign", "legal", "work", "60.0m"],
    distribution="lognormal",
    confidence_interval=(50_000_000, 80_000_000),  # $50M-$80M (±30%)
    # Economist rationale: International treaty drafting requires 193 jurisdictions.
    # Ottawa Treaty legal costs: ~$10M (1997). Paris Climate Agreement: ~$50M (2015).
    # Adjusting for inflation and complexity: $60M baseline ±30% for legal contestation risk.
    # CRITICAL: Legal disputes (pharma, military contractors) could escalate costs 2-3x.
    validation_min=40_000_000,   # Floor: Lean legal team, minimal dispute resolution
    validation_max=120_000_000,  # Ceiling: Protracted legal challenges from industry groups
    latex_symbol=r"Budget_{legal}",  # LaTeX symbol for equations
)

CAMPAIGN_REGULATORY_NAVIGATION = Parameter(
    20_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Regulatory compliance and navigation",
    display_name="Regulatory Compliance and Navigation",
    unit="USD",
    keywords=["20.0m", "approval", "authorization", "oversight", "regulation", "compliance", "regulatory"],
    confidence_interval=(14_000_000, 26_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{reg}",  # LaTeX symbol for equations
)

CAMPAIGN_LEGAL_DEFENSE = Parameter(
    20_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Legal defense fund",
    display_name="Legal Defense Fund",
    unit="USD",
    keywords=["20.0m", "armed forces", "conflict", "legal", "armed conflict", "military action", "warfare"],
    confidence_interval=(14_000_000, 26_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{legal,def}",  # LaTeX symbol for equations
)

CAMPAIGN_DEFENSE_CONVERSION = Parameter(
    50_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Defense industry conversion program",
    display_name="Defense Industry Conversion Program",
    unit="USD",
    keywords=["50.0m", "armed forces", "conflict", "conversion", "armed conflict", "military action", "warfare"],
    distribution="lognormal",
    confidence_interval=(40_000_000, 70_000_000),  # $40M-$70M (±35%)
    # Economist rationale: Defense industry transition programs historically underfunded.
    # Post-Cold War conversion: $2B over 10 years ($200M/year) for entire US defense sector.
    # Our $50M targets key stakeholders only. Right-skewed: industry resistance could escalate costs.
    # CRITICAL: Lockheed, Raytheon lobbying power, conversion could require 2-3x budget if contested.
    validation_min=30_000_000,   # Floor: Minimal outreach, focus on willing partners
    validation_max=100_000_000,  # Ceiling: Full industry engagement + job retraining programs
    latex_symbol=r"Budget_{conversion}",  # LaTeX symbol for equations
)

CAMPAIGN_HEALTHCARE_ALIGNMENT = Parameter(
    35_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Healthcare industry alignment and partnerships",
    display_name="Healthcare Industry Alignment and Partnerships",
    unit="USD",
    keywords=["campaign", "healthcare", "alignment", "35.0m"],
    confidence_interval=(24_500_000, 45_500_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{health}",  # LaTeX symbol for equations
)

CAMPAIGN_TECH_PARTNERSHIPS = Parameter(
    25_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Tech industry partnerships and infrastructure",
    display_name="Tech Industry Partnerships and Infrastructure",
    unit="USD",
    keywords=["campaign", "tech", "partnerships", "25.0m"],
    confidence_interval=(17_500_000, 32_500_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{tech}",  # LaTeX symbol for equations
)

CAMPAIGN_CELEBRITY_ENDORSEMENT = Parameter(
    15_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Celebrity and influencer endorsements",
    display_name="Celebrity and Influencer Endorsements",
    unit="USD",
    keywords=["campaign", "celebrity", "endorsement", "15.0m"],
    confidence_interval=(10_500_000, 19_500_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{celeb}",  # LaTeX symbol for equations
)

CAMPAIGN_INFRASTRUCTURE = Parameter(
    20_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Campaign operational infrastructure",
    display_name="Campaign Operational Infrastructure",
    unit="USD",
    keywords=["campaign", "infrastructure", "20.0m"],
    confidence_interval=(14_000_000, 26_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{infra}",  # LaTeX symbol for equations
)

CAMPAIGN_CONTINGENCY = Parameter(
    50_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Contingency fund for unexpected costs",
    display_name="Contingency Fund for Unexpected Costs",
    unit="USD",
    keywords=["50.0m", "contingency", "most likely", "campaign", "base case", "central", "expenditure"],
    distribution="uniform",  # Uniform by definition, contingency is for unknown unknowns
    confidence_interval=(30_000_000, 80_000_000),  # $30M-$80M (wide for true contingency)
    # Economist rationale: Contingency should be 10-20% of total project cost ($1B × 10-20% = $100M-$200M).
    # Using $50M as baseline (5% of $1B) is conservative. Uniform distribution reflects epistemic uncertainty,
    # we don't know what we don't know. Historical precedent: mega-projects require 15-30% contingency.
    # CRITICAL: This is NOT lognormal, contingency spending is bounded and uniform by construction.
    validation_min=20_000_000,   # Floor: Minimal buffer (2% of $1B)
    validation_max=150_000_000,  # Ceiling: Full 15% contingency for mega-project risk
    latex_symbol=r"Budget_{contingency}",  # LaTeX symbol for equations
)

CAMPAIGN_TREATY_IMPLEMENTATION = Parameter(
    40_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Post-victory treaty implementation support",
    display_name="Post-Victory Treaty Implementation Support",
    unit="USD",
    keywords=["40.0m", "1%", "impact investing", "pay for success", "one percent", "development finance", "impact bond"],
    distribution="lognormal",
    confidence_interval=(30_000_000, 55_000_000),  # $30M-$55M (±30%)
    # Economist rationale: Post-treaty implementation varies with compliance enforcement needs.
    # Ottawa Treaty implementation: $20M/year for 10 years ($200M total). Paris Climate: $100M/year ongoing.
    # Our $40M is 1-year support (campaign phase), ongoing DIH funding covers long-term implementation.
    # Right-skewed: compliance failures (e.g., Syria violating Ottawa Treaty) require surge funding.
    validation_min=25_000_000,   # Floor: Lean monitoring team, voluntary compliance
    validation_max=80_000_000,   # Ceiling: Full enforcement mechanism + dispute resolution
    latex_symbol=r"Budget_{impl}",  # LaTeX symbol for equations
)

CAMPAIGN_SCALING_PREP = Parameter(
    30_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Scaling preparation and blueprints",
    display_name="Scaling Preparation and Blueprints",
    unit="USD",
    keywords=["campaign", "scaling", "prep", "30.0m"],
    confidence_interval=(21_000_000, 39_000_000),  # ±30% uncertainty on budget estimate
    confidence="medium",
    latex_symbol=r"Budget_{scale}",  # LaTeX symbol for equations
)

CAMPAIGN_PLATFORM_DEVELOPMENT = Parameter(
    35_000_000,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Voting platform and technology development",
    display_name="Voting Platform and Technology Development",
    unit="USD",
    keywords=["campaign", "platform", "development", "35.0m"],
    distribution="lognormal",  # Software projects famously right-skewed (Standish Chaos Report)
    confidence_interval=(25_000_000, 50_000_000),  # $25M-$50M (±35%)
    # Economist rationale: Voting platforms require enterprise security + global scale.
    # Healthcare.gov: $93M budgeted → $1.7B actual (18x overrun). Iowa caucus app: $60K → $170K (3x).
    # Blockchain voting platforms: $10M-$100M depending on security requirements.
    # Using $35M baseline ±35% reflects software project overrun reality (Standish: 45% average).
    # CRITICAL: Security audit failures or DDoS attacks could require emergency fixes (2-3x budget).
    validation_min=20_000_000,   # Floor: MVP with minimal security (not recommended)
    validation_max=80_000_000,   # Ceiling: Enterprise-grade with 24/7 security ops + pen testing
    latex_symbol=r"Budget_{platform}",  # LaTeX symbol for equations
)

# Investment tier minimums (in millions USD or thousands USD)
INSTITUTIONAL_INVESTOR_MIN = Parameter(
    10_000_000,
    manual_ref="knowledge/solution/incentive-alignment-bonds.qmd",
    source_type="definition",
    description="Minimum investment for institutional investors",
    display_name="Minimum Investment for Institutional Investors",
    unit="USD",
    keywords=["10.0m", "impact investing", "pay for success", "debt instrument", "development finance", "fixed income", "impact bond"],
    latex_symbol=r"Invest_{inst,min}",  # LaTeX symbol for equations
)

FAMILY_OFFICE_INVESTMENT_MIN = Parameter(
    5_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_type="definition",
    description="Minimum investment for family offices",
    display_name="Minimum Investment for Family Offices",
    unit="USD",
    keywords=["5.0m", "impact investing", "pay for success", "capital", "finance", "money", "debt instrument"],
    latex_symbol=r"Invest_{family,min}",  # LaTeX symbol for equations
)


# Total system costs
TREATY_TOTAL_ANNUAL_COSTS = Parameter(
    TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED + DFDA_ANNUAL_OPEX,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total annual treaty system costs (campaign + pragmatic trial platform operations)",
    display_name="Total Annual Treaty System Costs",
    unit="USD/year",
    formula="CAMPAIGN_ANNUAL + TRIAL_PLATFORM_OPEX",
    keywords=["1%", "pragmatic trials", "real world evidence", "one percent", "decentralized trials", "drug agency", "food and drug administration"],
    inputs=['DFDA_ANNUAL_OPEX', 'TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED'],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED"] + ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"Cost_{treaty,ann}",  # LaTeX symbol for equations
)  # $290M ($0.29B)

# ---
# COMBINED ECONOMICS
# ---

# Basic annual benefits (peace dividend + R&D savings only, excludes regulatory delay & other benefits)
TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS = Parameter(
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + DFDA_BENEFIT_RD_ONLY_ANNUAL,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Basic annual benefits: peace dividend + pragmatic trial R&D savings only (2 of 8 benefit categories, excludes regulatory delay value)",
    display_name="1% treaty Basic Annual Benefits (Peace + R&D Savings)",
    unit="USD/year",
    formula="PEACE_DIVIDEND + PRAGMATIC_TRIAL_RD_SAVINGS",
    keywords=["1%", "pragmatic trials", "real world evidence", "one percent", "conflict resolution", "decentralized trials", "drug agency", "basic benefits"],
    inputs=["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT", "DFDA_BENEFIT_RD_ONLY_ANNUAL"],
    compute=lambda ctx: ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"] + ctx["DFDA_BENEFIT_RD_ONLY_ANNUAL"],
    latex_symbol=r"Benefit_{peace+RD}",  # LaTeX symbol for equations
)  # $155.05B (peace + R&D only)

# ---
# FINANCIAL PARAMETERS - NPV ANALYSIS
# ---

# NPV analysis parameters
# Source: knowledge/appendix/dfda-calculation-framework.qmd
NPV_DISCOUNT_RATE_STANDARD = Parameter(
    0.03,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="",
    source_type="definition",
    description="Standard discount rate for NPV analysis (3% annual, social discount rate)",
    display_name="Standard Discount Rate for NPV Analysis",
    unit="rate",
    keywords=["3%", "yearly", "npv", "discount", "standard", "pa", "per annum"],
    distribution="fixed",  # Methodological choice - not empirical uncertainty
    # Economist rationale: Using 3% social discount rate per:
    #   - OMB Circular A-4 (2023): 2% for regulatory analysis
    #   - EPA/HHS: 3% for health benefit analysis
    #   - Stern Review: 1.4% for climate/long-term
    #   - Academic consensus for intergenerational projects: 2-4%
    # NOTE: Previous 8% corporate WACC is inappropriate for:
    #   - Public health benefits (not corporate investment)
    #   - Intergenerational benefits (lives saved decades from now)
    #   - Social welfare analysis (not shareholder returns)
    # 3% balances time preference with ethical weight of future lives.
    validation_min=0.01,  # Floor: Near-zero for very long-term analysis
    validation_max=0.10,  # Ceiling: High corporate rate (inappropriate for health)
    latex_symbol=r"r_{discount}",  # LaTeX symbol for equations
)  # 3% annual social discount rate (r)

NPV_TIME_HORIZON_YEARS = Parameter(
    10, source_ref="", source_type="definition", description="Standard time horizon for NPV analysis", unit="years",
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    display_name="Standard Time Horizon for NPV Analysis",
    keywords=["npv", "time", "horizon", "years"],
    distribution="fixed",  # Methodological choice: standard 10-year NPV analysis window
    latex_symbol=r"T_{horizon}",  # LaTeX symbol for equations
)  # Standard 10-year analysis window (T)

# Lost-prosperity-only damages: NPV of perpetual annual lost-income flow at the
# standard 3% social discount rate, under a NO-CURE / NO-CONVERGENCE baseline
# assumption (the gap continues forever). This is a sensitivity exposure, not a
# claim that the gap actually persists indefinitely. A finite-horizon NPV would
# be slightly smaller (a 100-year truncated NPV at 3% captures ~94.7% of the
# perpetuity, so the assumption matters less than the discount-rate choice).
LOST_PROSPERITY_NPV_PERPETUITY_PER_CAPITA = Parameter(
    WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA / NPV_DISCOUNT_RATE_STANDARD,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Net present value of perpetual annual lost-income flow per representative living "
                "human, at the standard 3% social discount rate, under a no-cure/no-convergence "
                "baseline. Sensitivity exposure for the corporate-liability lost-profits theory. "
                "Treats the lost-prosperity flow as continuing indefinitely; a finite-horizon "
                "convergence assumption would shrink this slightly (~5% reduction at 100 years). "
                "Single-theory pleading; cannot be added to the body-count ledger.",
    display_name="Lost-Prosperity-Only NPV Perpetuity Per Capita (3%, No-Cure Baseline)",
    unit="USD/person",
    formula="WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA / NPV_DISCOUNT_RATE_STANDARD",
    inputs=["WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA", "NPV_DISCOUNT_RATE_STANDARD"],
    compute=lambda ctx: ctx["WAR_COUNTERFACTUAL_LOST_GDP_PER_CAPITA"] / ctx["NPV_DISCOUNT_RATE_STANDARD"],
    keywords=["lost prosperity", "NPV", "perpetuity", "per capita", "no-cure", "single theory", "lost profits"],
    latex_symbol=r"D_{prosperity,NPV,pc}",
)

LOST_PROSPERITY_NPV_PERPETUITY_TOTAL = Parameter(
    WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL / NPV_DISCOUNT_RATE_STANDARD,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Net present value of perpetual lost-income flow globally, at the standard 3% "
                "social discount rate, under a no-cure/no-convergence baseline. Sensitivity "
                "exposure under corporate-liability lost-profits doctrine. Cannot be added to the "
                "body-count ledger.",
    display_name="Lost-Prosperity-Only NPV Perpetuity Total (3%, No-Cure Baseline)",
    unit="USD",
    formula="WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL / NPV_DISCOUNT_RATE_STANDARD",
    inputs=["WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL", "NPV_DISCOUNT_RATE_STANDARD"],
    compute=lambda ctx: ctx["WAR_COUNTERFACTUAL_LOST_GDP_GLOBAL"] / ctx["NPV_DISCOUNT_RATE_STANDARD"],
    keywords=["lost prosperity", "NPV", "perpetuity", "total", "no-cure", "single theory", "lost profits"],
    latex_symbol=r"D_{prosperity,NPV}",
)

# ---
# FINANCIAL PARAMETERS - NPV MODEL COMPONENTS
# ---

# NPV Model - Component Costs
# Core framework and broader initiative costs (for detailed breakdowns)
DFDA_NPV_UPFRONT_COST = Parameter(
    40_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Pragmatic trial platform core framework build cost",
    display_name="Pragmatic Trial Platform Core Framework Build Cost",
    unit="USD",
    keywords=["40.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(25_000_000, 65_000_000),  # $25M-$65M (±40% - IT projects have high variance)
    latex_symbol=r"Cost_{upfront}",  # LaTeX symbol for equations
)  # $40M Core framework build

DIH_NPV_UPFRONT_COST_INITIATIVES = Parameter(
    229_750_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="DIH broader initiatives upfront cost (medium case)",
    display_name="DIH Broader Initiatives Upfront Cost",
    unit="USD",
    keywords=["229.8m", "pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials"],
    distribution="lognormal",
    confidence_interval=(150_000_000, 350_000_000),  # $150M-$350M (±40%)
    latex_symbol=r"Cost_{DIH,init}",  # LaTeX symbol for equations
)  # $228M medium case broader initiatives

DFDA_NPV_ANNUAL_OPEX = Parameter(
    18_950_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="definition",
    description="Pragmatic trial platform core framework annual opex (midpoint of $11-26.5M)",
    display_name="Pragmatic Trial Platform Core Framework Annual OPEX",
    unit="USD/year",
    keywords=["18.9m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(11_000_000, 26_500_000),  # $11M-$26.5M (actual range from source)
    latex_symbol=r"OPEX_{ann}",  # LaTeX symbol for equations
)  # $19M Core framework (midpoint of $11-26.5M)

DIH_NPV_ANNUAL_OPEX_INITIATIVES = Parameter(
    21_100_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="definition",
    description="DIH broader initiatives annual opex (medium case)",
    display_name="DIH Broader Initiatives Annual OPEX",
    unit="USD/year",
    keywords=["21.1m", "pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials"],
    distribution="lognormal",
    confidence_interval=(14_000_000, 32_000_000),  # $14M-$32M (±30%)
    latex_symbol=r"OPEX_{DIH,ann}",  # LaTeX symbol for equations
)  # $21.1M medium case broader initiatives

# NPV Model - Primary Parameters (pragmatic trial platform)
# Total upfront costs (C0): combines core pragmatic trial framework + broader DIH initiative setup
DFDA_NPV_UPFRONT_COST_TOTAL = Parameter(
    DFDA_NPV_UPFRONT_COST + DIH_NPV_UPFRONT_COST_INITIATIVES,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total NPV upfront costs (pragmatic trial platform core + DIH initiatives)",
    display_name="Pragmatic Trial Platform Total NPV Upfront Costs",
    unit="USD",
    formula="TRIAL_PLATFORM_BUILD + DIH_INITIATIVES",    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials", "drug agency"],
    # Uncertainty derived from inputs (DFDA_BUILD + DIH_INITIATIVES)
    validation_min=150_000_000,  # Floor: MVP + essential initiatives only
    validation_max=800_000_000,  # Ceiling: Full scope creep + regulatory capture (raised from $500M)
    inputs=['DFDA_NPV_UPFRONT_COST', 'DIH_NPV_UPFRONT_COST_INITIATIVES'],
    compute=lambda ctx: ctx["DFDA_NPV_UPFRONT_COST"] + ctx["DIH_NPV_UPFRONT_COST_INITIATIVES"],
    latex_symbol=r"Cost_{upfront,total}",  # LaTeX symbol for equations
)  # C0 = $0.26975B

# Total annual operational costs (Cop): combines core pragmatic trial framework + broader DIH initiative annual costs
DFDA_NPV_ANNUAL_OPEX_TOTAL = Parameter(
    DFDA_NPV_ANNUAL_OPEX + DIH_NPV_ANNUAL_OPEX_INITIATIVES,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Total NPV annual opex (pragmatic trial platform core + DIH initiatives)",
    display_name="Pragmatic Trial Platform Total NPV Annual OPEX",
    unit="USD/year",
    formula="TRIAL_PLATFORM_OPEX + DIH_OPEX",    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials", "drug agency"],
    inputs=['DFDA_NPV_ANNUAL_OPEX', 'DIH_NPV_ANNUAL_OPEX_INITIATIVES'],
    compute=lambda ctx: ctx["DFDA_NPV_ANNUAL_OPEX"] + ctx["DIH_NPV_ANNUAL_OPEX_INITIATIVES"],
    latex_symbol=r"OPEX_{total}",  # LaTeX symbol for equations
)  # Cop = $0.04005B

# Pragmatic trial platform adoption curve: linear ramp from 0% to 100% over 5 years, then constant at 100%
DFDA_NPV_ADOPTION_RAMP_YEARS = Parameter(
    5,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Years to reach full pragmatic trial platform adoption",
    display_name="Years to Reach Full Pragmatic Trial Platform Adoption",
    unit="years",
    keywords=["pragmatic trials", "real world evidence", "deployment rate", "market penetration", "participation rate", "uptake", "usage rate"],
    latex_symbol=r"T_{ramp}",  # LaTeX symbol for equations
)  # Years to reach full adoption

# Calculated NPV values for pragmatic trial platform
DFDA_NPV_PV_ANNUAL_OPEX = Parameter(
    DFDA_NPV_ANNUAL_OPEX_TOTAL
    * (1 - (1 + NPV_DISCOUNT_RATE_STANDARD) ** -NPV_TIME_HORIZON_YEARS)
    / NPV_DISCOUNT_RATE_STANDARD,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Present value of annual opex over 10 years (NPV formula)",
    display_name="Pragmatic Trial Platform Present Value of Annual OPEX Over 10 Years",
    unit="USD",
    formula="OPEX × [(1 - (1 + r)^-T) / r]",
    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "yearly"],
    inputs=['DFDA_NPV_ANNUAL_OPEX_TOTAL', 'NPV_DISCOUNT_RATE_STANDARD', 'NPV_TIME_HORIZON_YEARS'],
    compute=lambda ctx: ctx["DFDA_NPV_ANNUAL_OPEX_TOTAL"]
    * (1 - (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** -ctx["NPV_TIME_HORIZON_YEARS"])
    / ctx["NPV_DISCOUNT_RATE_STANDARD"],
    latex_symbol=r"PV_{OPEX}",  # LaTeX symbol for equations
)
DFDA_NPV_TOTAL_COST = Parameter(
    DFDA_NPV_UPFRONT_COST_TOTAL + DFDA_NPV_PV_ANNUAL_OPEX,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Total NPV cost (upfront + PV of annual opex)",
    display_name="Pragmatic Trial Platform Total NPV Cost",
    unit="USD",
    formula="UPFRONT + PV_OPEX",    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "costs"],
    inputs=['DFDA_NPV_PV_ANNUAL_OPEX', 'DFDA_NPV_UPFRONT_COST_TOTAL'],
    compute=lambda ctx: ctx["DFDA_NPV_UPFRONT_COST_TOTAL"] + ctx["DFDA_NPV_PV_ANNUAL_OPEX"],
    latex_symbol=r"Cost_{platform,total}",  # LaTeX symbol for equations
)  # ~$0.54B

# NPV of pragmatic trial benefits with 5-year linear adoption ramp
# Years 1-5: 20%, 40%, 60%, 80%, 100% adoption
# Years 6-10: 100% adoption
# Discounted at 8% annual rate
DFDA_NPV_BENEFIT_RD_ONLY = Parameter(
    sum(
        [
            DFDA_NET_SAVINGS_RD_ONLY_ANNUAL * (min(year, 5) / 5) / (1 + NPV_DISCOUNT_RATE_STANDARD) ** year
            for year in range(1, 11)
        ]
    ),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="NPV of pragmatic trial R&D savings only with 5-year adoption ramp (10-year horizon, most conservative financial estimate)",
    display_name="NPV of Pragmatic Trial Benefits (R&D Only, 10-Year Discounted)",
    unit="USD",
    formula="SUM[Savings × adoption(t) / (1+r)^t] for t=1..10",
    latex=r"NPV_{RD} = \sum_{t=1}^{10} \frac{Savings_{RD,ann} \cdot \frac{\min(t,5)}{5}}{(1+r)^t}",
    keywords=["pragmatic trials", "real world evidence", "deployment rate", "market penetration", "participation rate", "uptake", "usage rate", "conservative"],
    inputs=['DFDA_NET_SAVINGS_RD_ONLY_ANNUAL', 'NPV_DISCOUNT_RATE_STANDARD'],
    compute=lambda ctx: sum(
        [
            ctx["DFDA_NET_SAVINGS_RD_ONLY_ANNUAL"] * (min(year, 5) / 5) / (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** year
            for year in range(1, 11)
        ]
    ),
    latex_symbol=r"NPV_{RD}",
    # Hand-crafted LaTeX for complex NPV formula with adoption ramp
)  # ~$249.3B NPV of R&D savings only (conservative financial case)

DFDA_NPV_NET_BENEFIT_RD_ONLY = Parameter(
    DFDA_NPV_BENEFIT_RD_ONLY - DFDA_NPV_TOTAL_COST,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="NPV net benefit using R&D savings only (benefits minus costs)",
    display_name="NPV Net Benefit (R&D Only)",
    unit="USD",
    formula="NPV_BENEFIT - NPV_COST",
    keywords=["pragmatic trials", "real world evidence", "net benefit", "conservative"],
    inputs=['DFDA_NPV_BENEFIT_RD_ONLY', 'DFDA_NPV_TOTAL_COST'],
    compute=lambda ctx: ctx["DFDA_NPV_BENEFIT_RD_ONLY"] - ctx["DFDA_NPV_TOTAL_COST"],
    latex_symbol=r"NPV_{net,RD}",  # LaTeX symbol for equations
)  # ~$248.7B (benefits minus costs)

# NPV of Regulatory Delay Avoidance (Disease Eradication Delay Elimination)
# This calculates the present value of eliminating the 8.2-year regulatory delay,
# assuming diseases are cured 100 years in the future on average.
#
# Key assumption: If diseases are cured at year 100, eliminating the regulatory delay
# brings them 8.2 years earlier (years 92-100). This is a simple timeline shift -
# the full annual benefit applies for all 8.2 years.
#
# Far-future discounting dramatically reduces NPV compared to immediate benefits,
# but the delay avoidance still provides value by bringing cures 8 years earlier.
# DELETED: DFDA_NPV_BENEFIT_DELAY_AVOIDANCE
# Depended on deleted DFDA_QALYS_RD_PLUS_DELAY_MONETIZED
# NPV calculations for timeline shift benefits are conceptually problematic anyway

# ---
# ROI TIERS
# ---

# Tier 1: Conservative - pragmatic trial R&D savings only (10-year NPV)
# Source: knowledge/appendix/dfda-roi-calculations.qmd NPV analysis
DFDA_ROI_RD_ONLY = Parameter(
    DFDA_NPV_BENEFIT_RD_ONLY / DFDA_NPV_TOTAL_COST,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="ROI from pragmatic trial R&D savings only (10-year NPV, most conservative estimate)",
    display_name="ROI from Pragmatic Trial R&D Savings Only",
    unit="ratio",
    formula="NPV_BENEFIT ÷ NPV_TOTAL_COST",
    keywords=["pragmatic trials", "real world evidence", "bcr", "benefit cost ratio", "economic return", "investment return", "low estimate"],
    inputs=["DFDA_NPV_BENEFIT_RD_ONLY", "DFDA_NPV_TOTAL_COST"],
    compute=lambda ctx: ctx["DFDA_NPV_BENEFIT_RD_ONLY"] / ctx["DFDA_NPV_TOTAL_COST"],
    latex_symbol=r"ROI_{RD}",  # LaTeX symbol for equations
)  # ~637:1 - Most conservative, R&D cost savings only (NPV-adjusted)


# ---
# POLITICAL SUCCESS PROBABILITY AND EXPECTED VALUE ANALYSIS
# ---

# Single political success probability parameter with full uncertainty distribution
# Replaces 6 discrete probability parameters - Monte Carlo/sensitivity analysis handles the range
#
# Rationale for 10% central estimate (see knowledge/appendix/treaty-feasibility.qmd):
# - 0.7% ODA target: Only 5-6 of ~30 DAC countries meet it despite 50+ years of commitment (~20% compliance)
# - Kyoto Protocol: ~55% of emissions covered initially, but US never ratified, Canada withdrew
# - Paris Agreement: High adoption but non-binding; actual NDC compliance ~15-25%
# - International financial commitments requiring ongoing budget allocation historically have <25% full compliance
# - A 1% military→health reallocation is HARDER than most precedents (touches defense budgets)
# - However, unique advantages exist: self-funding mechanism, bipartisan health appeal, referendum pathway
#
# Conservative 10% central estimate with 2%-25% range reflects:
# - Floor (2%): Black swan scenario requiring unprecedented global cooperation
# - Central (1%): conservative - assumes 99% chance of failure
# - Floor (0.1%): Near-impossibility scenarios (gridlock, competing crises)
# - Ceiling (10%): Optimistic scenario where major crisis creates political window
POLITICAL_SUCCESS_PROBABILITY = Parameter(
    0.01,  # Central estimate: 1% - assumes 99% failure rate, yet still 7x better than bed nets
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.ICBL_OTTAWA_TREATY,
    source_type="external",
    confidence="low",
    description="Estimated probability of treaty ratification and sustained implementation. "
                "Central estimate 1% is conservative. This assumes 99% chance of failure. ",
    display_name="Political Success Probability",
    unit="rate",
    distribution=DistributionType.BETA,  # Bounded [0,1], appropriate for probabilities
    confidence_interval=(0.001, 0.10),  # 0.1% floor to 10% ceiling
    std_error=0.02,  # Tighter spread around 1% central
    keywords=["probability", "political", "treaty", "ratification", "implementation", "uncertainty",
              "adoption", "success", "campaign", "voting", "referendum"],
              latex_symbol=r"P_{success}",  # LaTeX symbol for equations
)

# NOTE: TREATY_EXPECTED_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG is defined later in the file (after TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG)
# because it depends on that parameter which is calculated from other treaty parameters.

# ---
# POLITICAL DYSFUNCTION TAX: EMPIRICAL FIGURES FROM PAPER
# ---
# Source: knowledge/appendix/political-dysfunction-tax.qmd
# These are empirically-sourced figures from "The Political Dysfunction Tax: A Forensic Audit
# of Global Governance Efficiency" paper. Unlike the theoretical decomposition above,
# these are specific, citable waste and opportunity cost figures.
#
# IMPORTANT: Figures are scoped by geography (US_ or GLOBAL_) to enable proper
# percentage calculations. US waste should be divided by US GDP, not global GDP.
#
# Structure:
#   Part 1: Waste Ledger (burned capital) - mostly US-specific
#   Part 2: Opportunity Ledger (unrealized potential) - global
#   Derived: Percentages and totals with correct GDP bases

# (GLOBAL_GDP_2025 moved earlier in file for war counterfactual params)

# US GDP (2024) - needed for US waste percentage calculations
US_GDP_2024 = Parameter(
    28_780_000_000_000,  # $28.78 trillion (2024 estimate)
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="worldbank-gdp",
    source_type="external",
    confidence="high",
    distribution="fixed",  # Official statistic
    description="US GDP in 2024 dollars for calculating policy costs as percentage of GDP.",
    display_name="US GDP (2024)",
    unit="USD",
    keywords=["GDP", "US", "economy", "2024"],
    latex_symbol=r"GDP_{US}",
)


# =============================================================================
# PART 1: WASTE LEDGER (GLOBAL)
# =============================================================================
# Global-scope waste figures

POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES = Parameter(
    1_300_000_000_000,  # $1.3T annually
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="high",
    description="Global explicit fossil fuel subsidies (governments undercharging for energy "
                "supply costs). IMF 2022 estimate. These subsidies actively encourage consumption "
                "of negative-externality goods, working against climate goals. "
                "Note: IMF implicit subsidies (externalities) are much larger (~$7T).",
    display_name="Global Fossil Fuel Subsidies",
    unit="USD",
    distribution=DistributionType.NORMAL,
    confidence_interval=(1_100_000_000_000, 1_500_000_000_000),
    std_error=100_000_000_000,
    keywords=["fossil fuel", "subsidy", "global", "IMF", "climate", "waste"],
    latex_symbol=r"W_{ff,global}",
)

# =============================================================================
# PART 2: OPPORTUNITY LEDGER (GLOBAL)
# =============================================================================
# These represent unrealized potential from governance failures - global scope.
# Source: Political Dysfunction Tax paper, Part 2

POLITICAL_DYSFUNCTION_GLOBAL_HEALTH_OPPORTUNITY_COST = Parameter(
    34_000_000_000_000,  # $34T annually
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="low",
    description="Annual opportunity cost of slow-motion regulatory environment for health innovation. "
                "Murphy-Topel (2006) valued cancer cure at $50T (inflation-adjusted ~$100T in 2025). "
                "Longevity dividend of 1 extra year = $38T globally. "
                "PCTs could accelerate cures by 10+ years; NPV of 10-year delay at 3% discount = ~$25T. "
                "Conservative estimate: $34T annually in lives lost and healthspan denied.",
    display_name="Global Health Opportunity Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(20_000_000_000_000, 80_000_000_000_000),  # Very wide - speculative
    std_error=15_000_000_000_000,
    keywords=["health", "opportunity cost", "global", "longevity", "FDA", "regulatory"],
    latex_symbol=r"O_{health}",
)

POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST = Parameter(
    4_000_000_000_000,  # $4T annually
    manual_ref="knowledge/appendix/optimocracy-paper.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="low",
    description="Annual opportunity cost from outcome-blind research allocation. "
                "Human Genome Project: $3.8B cost, $796B-1T impact (141:1 ROI). "
                "Fusion DEMO plant: $5-10B could solve energy/climate permanently. "
                "Current system funds inputs (grants, process) rather than outcomes (cures, working reactors). "
                "Reallocating $200B from military waste at 20x multiplier = $4T foregone growth.",
    display_name="Global R&D Misallocation Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(2_000_000_000_000, 10_000_000_000_000),
    std_error=2_000_000_000_000,
    keywords=["science", "R&D", "opportunity cost", "global", "fusion", "misallocation"],
    latex_symbol=r"O_{science}",
)

POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST = Parameter(
    6_000_000_000_000,  # $6T annually
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="high",
    description="Global cost of lead exposure: World Bank/Lancet estimate. "
                "765 million IQ points lost annually, 5.5 million premature CVD deaths. "
                "Cost to eliminate lead from paint, spices, batteries is trivial compared to damage. "
                "This is an arbitrage opportunity of immense scale that governance has failed to execute.",
    display_name="Global Lead Poisoning Cost",
    unit="USD",
    distribution=DistributionType.NORMAL,
    confidence_interval=(4_000_000_000_000, 8_000_000_000_000),
    std_error=1_000_000_000_000,
    keywords=["lead", "poisoning", "IQ", "opportunity cost", "global", "World Bank"],
    latex_symbol=r"O_{lead}",
)

# ---------------------------------------------------------------------------
# The Ethyl Gasoline Corporation counterfactual (i-am-retarded.qmd)
#
# How much richer would Ethyl's own shareholders have been if the board had
# switched to ethanol in 1923 instead of lobbying for seventy years to keep
# tetraethyl lead in gasoline?
#
# Mechanism: leaded gasoline lowered average US IQ (McFarland 2022: 824M
# cumulative points, ~2.6/person, 5.9 for peak cohorts). National average IQ
# raises GDP growth (~0.11pp/point/year, Jones & Schneider 2006). A
# diversified shareholder's terminal wealth scales with the economy, so the
# counterfactual wealth gain is the compounded growth differential over the
# TEL era (1923-1996). Foregone TEL royalties are second-order against an
# economy-wide compounding effect and are ignored.
# ---------------------------------------------------------------------------

LEADED_GASOLINE_US_AVG_IQ_LOSS_POINTS = Parameter(
    2.6,
    manual_ref="knowledge/problem/i-am-retarded.qmd",
    source_ref=ReferenceID.MCFARLAND_LEAD_IQ_2022,
    source_type="external",
    confidence="medium",
    description="Average IQ points lost per person from childhood leaded-gasoline exposure "
                "(McFarland et al. 2022: 824M cumulative points across the 2015 US population, "
                "average 2.6/person, 5.9 for the worst-hit 1966-1970 birth cohorts). Used as the "
                "era-average workforce IQ deficit: lower in the 1930s, higher by the 1980s.",
    display_name="US Average IQ Loss from Leaded Gasoline",
    unit="IQ points",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(1.5, 5.9),
    keywords=["lead", "IQ", "ethyl", "leaded gasoline", "McFarland", "brain damage"],
    latex_symbol=r"\Delta IQ_{lead}",
)

NATIONAL_IQ_GDP_GROWTH_EFFECT_PER_POINT = Parameter(
    0.0011,
    manual_ref="knowledge/problem/i-am-retarded.qmd",
    source_ref=ReferenceID.JONES_SCHNEIDER_IQ_GROWTH_2006,
    source_type="external",
    confidence="low",
    description="Jones & Schneider (2006) BACE estimate: one national-IQ point is associated with "
                "a persistent 0.11 percentage-point higher annual GDP per capita growth rate "
                "(significant in 99.8% of 1,330 growth regressions). Wide CI reflects the contested "
                "cross-country IQ data underlying the estimate and the authors' own caveat that "
                "transitory vs steady-state growth cannot be distinguished.",
    display_name="GDP Growth Effect per National IQ Point",
    unit="rate",
    distribution=DistributionType.NORMAL,
    confidence_interval=(0.0004, 0.0018),
    keywords=["IQ", "GDP growth", "human capital", "Jones", "Schneider", "BACE"],
    latex_symbol=r"\beta_{IQ}",
)

LEADED_GASOLINE_ERA_YEARS = Parameter(
    73,
    manual_ref="knowledge/problem/i-am-retarded.qmd",
    source_ref=ReferenceID.KOVARIK_LEADED_GASOLINE_HISTORY_2005,
    source_type="definition",
    description="Duration of the US leaded-gasoline era: first commercial TEL sale (February 1923) "
                "to the completed on-road ban (January 1, 1996).",
    display_name="Leaded Gasoline Era Duration",
    unit="years",
    distribution="fixed",
    keywords=["lead", "ethyl", "TEL", "era", "1923", "1996"],
    latex_symbol=r"T_{lead}",
)

ETHYL_SHAREHOLDER_COUNTERFACTUAL_WEALTH_GAIN = Parameter(
    (1 + LEADED_GASOLINE_US_AVG_IQ_LOSS_POINTS * NATIONAL_IQ_GDP_GROWTH_EFFECT_PER_POINT)
    ** LEADED_GASOLINE_ERA_YEARS - 1,
    manual_ref="knowledge/problem/i-am-retarded.qmd",
    source_type="calculated",
    description="How much richer a diversified Ethyl Gasoline Corporation shareholder would have been "
                "by 1996 had the board switched to ethanol in 1923: the economy compounds faster without "
                "the lead-induced IQ loss, and diversified shareholder wealth scales with the economy. "
                "Central ~23%; the Monte Carlo range spans roughly 'twenty to sixty percent richer'. "
                "Foregone TEL royalties are second-order against the economy-wide effect.",
    display_name="Ethyl Shareholder Counterfactual Wealth Gain (Ethanol Switch, 1923)",
    unit="percent",
    formula="(1 + LEADED_GASOLINE_US_AVG_IQ_LOSS_POINTS * NATIONAL_IQ_GDP_GROWTH_EFFECT_PER_POINT) ** LEADED_GASOLINE_ERA_YEARS - 1",
    inputs=[
        "LEADED_GASOLINE_US_AVG_IQ_LOSS_POINTS",
        "NATIONAL_IQ_GDP_GROWTH_EFFECT_PER_POINT",
        "LEADED_GASOLINE_ERA_YEARS",
    ],
    compute=lambda ctx: (
        (1 + ctx["LEADED_GASOLINE_US_AVG_IQ_LOSS_POINTS"] * ctx["NATIONAL_IQ_GDP_GROWTH_EFFECT_PER_POINT"])
        ** ctx["LEADED_GASOLINE_ERA_YEARS"] - 1
    ),
    keywords=["ethyl", "counterfactual", "shareholder", "lead", "ethanol", "20-60%", "wealth"],
    latex_symbol=r"\Delta W_{Ethyl}",
)

POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST = Parameter(
    57_000_000_000_000,  # $57T annually (Clemens 2011 lower bound)
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="low",
    description="Unrealized output from migration restrictions. Clemens (2011) estimated "
                "eliminating labor mobility barriers could increase global GDP by 50-150%. "
                "At $115T global GDP, Clemens lower bound = $57T; upper bound = $170T. "
                "The estimate is controversial: critics argue it assumes full global labor "
                "mobility and ignores fiscal and social adjustment costs. Skeptical lower "
                "bound: ~$5T (partial reforms only). Even 5% workforce mobility would "
                "generate trillions, exceeding all foreign aid ever given. "
                "This is the largest and most uncertain single component of the dysfunction tax.",
    display_name="Global Migration Opportunity Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(5_000_000_000_000, 170_000_000_000_000),
    std_error=30_000_000_000_000,
    keywords=["migration", "labor mobility", "opportunity cost", "global", "Clemens"],
    latex_symbol=r"O_{migration}",
)

# Total global opportunity cost
POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL = Parameter(
    (POLITICAL_DYSFUNCTION_GLOBAL_HEALTH_OPPORTUNITY_COST +
     POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST +
     POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST +
     POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST),
    manual_ref="knowledge/appendix/optimocracy-paper.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="calculated",
    confidence="low",
    description="Total global opportunity cost from governance failures: "
                "health innovation delays ($34T), outcome-blind R&D allocation ($4T), "
                "lead poisoning ($6T), migration restrictions ($57T). "
                "Sum: $101T annually in unrealized potential.",
    display_name="Global Opportunity Cost Total",
    unit="USD",
    formula="HEALTH + SCIENCE + LEAD + MIGRATION",
    inputs=[
        "POLITICAL_DYSFUNCTION_GLOBAL_HEALTH_OPPORTUNITY_COST",
        "POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST",
        "POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST",
        "POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST",
    ],
    compute=lambda ctx: (
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_HEALTH_OPPORTUNITY_COST"] +
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST"] +
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST"] +
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST"]
    ),
    keywords=["opportunity cost", "global", "total", "dysfunction"],
    latex_symbol=r"O_{total}",
)

# ============================================================
# EOS equity valuation parameters
# ============================================================

# Fraction of social value EOS captures as shareholder returns.
# Base: Nordhaus (2004) found innovators capture ~2.2% of social surplus on average.
# This is a benchmark, not a guaranteed floor. Governance benefits are partly public
# goods, so EOS equity may capture less than the social surplus it creates. It may
# also capture more than the ordinary benchmark if the thesis is tradable before it
# is obvious, EOS owns the constrained assets first, and later investors reprice
# those assets after EOS proves the governance case.
# CI: 0.5% (spillovers dominate) to 5% (durable thesis ownership).
EOS_SOCIAL_VALUE_CAPTURE_PCT = Parameter(
    0.022,
    manual_ref="knowledge/economics/earth-optimization-fund.qmd",
    source_type="external",
    source_ref=ReferenceID.NORDHAUS2004,
    confidence="low",
    description="Fraction of political dysfunction tax value that EOS captures as "
                "shareholder returns via portfolio appreciation. Base case from "
                "Nordhaus (2004): innovators capture 2.2% of social surplus. "
                "Could be lower because governance gains are partly public goods. "
                "Could be higher if the thesis is tradable before it is obvious, "
                "EOS owns constrained assets first, and later investors reprice "
                "those assets after EOS proves the governance case. "
                "Skeptical case: 0.5%. Bull case: 5%.",
    display_name="EOS Social Value Capture Rate",
    unit="percent",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(0.005, 0.05),
    std_error=0.01,
    keywords=["EOS", "value capture", "Nordhaus", "activist", "equity"],
    latex_symbol=r"\phi_{capture}",
)

# Total addressable value for EOS equity (NPV of captured dysfunction tax).
# Formula: dysfunction_tax_annual × capture_pct / discount_rate
# At base values: $101T × 2.2% / 3% = ~$74T
# This is V in the share price formula: price = P(I) × V / total_shares.
EOS_EQUITY_VALUE_V = Parameter(
    POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL * EOS_SOCIAL_VALUE_CAPTURE_PCT / NPV_DISCOUNT_RATE_STANDARD,
    manual_ref="knowledge/economics/earth-optimization-fund.qmd",
    source_type="calculated",
    confidence="low",
    description="Total addressable value for EOS equity: NPV of the fraction of "
                "political dysfunction tax EOS captures as portfolio appreciation. "
                "V in the share price formula: price = P(I) x V / total_shares. "
                "Calculated as dysfunction_tax x capture_pct / discount_rate.",
    display_name="EOS Equity Value (V)",
    unit="USD",
    formula="POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL * EOS_SOCIAL_VALUE_CAPTURE_PCT / NPV_DISCOUNT_RATE_STANDARD",
    inputs=[
        "POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL",
        "EOS_SOCIAL_VALUE_CAPTURE_PCT",
        "NPV_DISCOUNT_RATE_STANDARD",
    ],
    compute=lambda ctx: (
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"] *
        ctx["EOS_SOCIAL_VALUE_CAPTURE_PCT"] /
        ctx["NPV_DISCOUNT_RATE_STANDARD"]
    ),
    keywords=["EOS", "equity", "valuation", "V", "share price"],
    latex_symbol=r"V_{EOS}",
)

EOS_STAGE_1_HII_TERMINAL_VALUE = Parameter(
    330_000_000,
    manual_ref="knowledge/economics/earth-optimization-fund.qmd",
    source_type="definition",
    confidence="low",
    description="Modeled terminal stage value if the first EOS governance campaign "
                "redirects Huntington Ingalls Industries lobbying and creates a "
                "credible activist-governance proof point. This is not probability-"
                "weighted expected value; the calculator applies probability separately.",
    display_name="EOS Stage 1 HII Terminal Value",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(100_000_000, 1_000_000_000),
    std_error=250_000_000,
    keywords=["EOS", "stage 1", "HII", "Huntington Ingalls", "valuation"],
    latex_symbol=r"V_{EOS,1}",
)

EOS_STAGE_2_DEFENSE_PRIMES_TERMINAL_VALUE = Parameter(
    7_000_000_000,
    manual_ref="knowledge/economics/earth-optimization-fund.qmd",
    source_type="definition",
    confidence="low",
    description="Modeled terminal stage value if EOS extends the governance campaign "
                "from HII to the major U.S. military prime contractors and redirects "
                "sector lobbying toward shareholder-positive policy. This is not "
                "probability-weighted expected value; the calculator applies "
                "probability separately.",
    display_name="EOS Stage 2 Defense-Primes Terminal Value",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(1_500_000_000, 30_000_000_000),
    std_error=6_000_000_000,
    keywords=["EOS", "stage 2", "military primes", "defense contractors", "valuation"],
    latex_symbol=r"V_{EOS,2}",
)

EOS_STAGE_3_LOBBYING_SECTORS_TERMINAL_VALUE = Parameter(
    452_000_000_000,
    manual_ref="knowledge/economics/earth-optimization-fund.qmd",
    source_type="definition",
    confidence="low",
    description="Modeled terminal stage value if EOS applies the same governance "
                "pressure across major lobbying-heavy sectors whose current policy "
                "positions destroy shareholder value. This is not probability-"
                "weighted expected value; the calculator applies probability separately.",
    display_name="EOS Stage 3 Lobbying-Sectors Terminal Value",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(100_000_000_000, 2_000_000_000_000),
    std_error=400_000_000_000,
    keywords=["EOS", "stage 3", "lobbying sectors", "activist governance", "valuation"],
    latex_symbol=r"V_{EOS,3}",
)

# Global opportunity cost as percentage of global GDP
POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_PCT_GDP = Parameter(
    POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL / GLOBAL_GDP_2025,
    manual_ref="knowledge/solution/optimocracy.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="calculated",
    confidence="low",
    unit="percent",
    description="Global opportunity cost as percentage of global GDP. "
                "$101T / $115T = ~88% of current GDP in unrealized potential. "
                "This represents the 'buried multipliers' of the global economy.",
    display_name="Global Opportunity Cost as % of GDP",
    formula="POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL / GLOBAL_GDP_2025",
    inputs=["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL", "GLOBAL_GDP_2025"],
    compute=lambda ctx: ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"] / ctx["GLOBAL_GDP_2025"],
    keywords=["opportunity cost", "global", "GDP", "percentage"],
    latex_symbol=r"O_{\%GDP}",
)

# =============================================================================
# US GOVERNMENT WASTE: MERGED AUTHORITATIVE SET
# =============================================================================
# Consolidates prior deprecated parameter sets (POLITICAL_DYSFUNCTION_US_*,
# BAD_POLICY_COST_US_*) into
# a single authoritative tally. Excludes speculative Tier 2 items (migration
# restrictions, fossil fuel externalities, occupational licensing) for defensibility.
#
# SOURCES: Papanicolas 2018 JAMA (healthcare), Hsieh & Moretti 2019 (housing),
# Competitive Enterprise Institute (regulatory), Tax Foundation (tax compliance),
# Cato Institute (corporate welfare), Yale Budget Lab (tariffs),
# Drug Policy Alliance (drug war), IMF (fossil fuel), USDA/EWG (agriculture)
# =============================================================================

# US Federal Budget baseline for percentage calculations
US_FEDERAL_SPENDING_2024 = Parameter(
    6_800_000_000_000,  # $6.8 trillion federal spending FY2024
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="cbo-long-term-budget-2024",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US federal government spending in FY2024. CBO reports outlays of $6.8T "
                "(23.9% of GDP). Includes mandatory spending, discretionary spending, "
                "and net interest ($888B).",
    display_name="US Federal Spending (FY2024)",
    unit="USD",
    keywords=["federal", "spending", "budget", "US", "FY2024"],
    latex_symbol=r"Spending_{US,fed}",
)

# ==============================================================================
# CATEGORY 1: DIRECT FEDERAL SPENDING WASTE (~$1.01T)
# Components representing actual federal budget allocations that could be
# redirected. Solution: Budget reallocation.
# ==============================================================================

# ==============================================================================
# FIRST-PRINCIPLES US HOMELAND DEFENSE BUDGET
# Bottom-up derivation of what actually defending the United States costs, by
# threat tier, at efficient (non-cost-plus) prices. This REPLACES the earlier
# anchored "strict deterrence" figure (~$285B) and the peer-benchmarked
# $300-550B range used previously. The optimum is dominated by the single threat
# US geography does not already neutralize: a survivable nuclear second strike.
# Invasion/conquest of the homeland is already a near-zero risk (two oceans, weak
# neighbors, the nuclear deterrent, and WWII-proven mobilization capacity), so
# marginal spending against it buys almost nothing. Honest range ~$130-280B.
# Derivation home: knowledge/economics/eisenhower-curve.qmd
# ==============================================================================

US_DEFENSE_FP_NUCLEAR_DETERRENT = Parameter(
    30_000_000_000,
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="definition",
    confidence="medium",
    distribution=DistributionType.NORMAL,
    confidence_interval=(20_000_000_000, 50_000_000_000),
    std_error=8_000_000_000,
    description="Survivable nuclear second strike: an SSBN-centric minimum credible deterrent "
                "(~100-200 survivable warheads on ballistic-missile submarines). The one threat "
                "geography does not neutralize. Drops the first-strike-attractive ICBM silos and "
                "the bomber leg. The UK and France each sustain continuous-at-sea deterrents within "
                "total defense budgets under $80B.",
    display_name="First-Principles Defense: Nuclear Second Strike",
    unit="USD",
    keywords=["defense", "first principles", "nuclear", "deterrent", "second strike", "SSBN"],
    latex_symbol=r"D_{nuclear}",
)

US_DEFENSE_FP_HOMELAND_AIR_MISSILE = Parameter(
    35_000_000_000,
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="definition",
    confidence="medium",
    distribution=DistributionType.NORMAL,
    confidence_interval=(25_000_000_000, 50_000_000_000),
    std_error=7_000_000_000,
    description="Continental air and missile defense plus early warning (NORAD, ground-based "
                "midcourse defense, interceptor aircraft). Defensive only; no expeditionary or "
                "power-projection air power.",
    display_name="First-Principles Defense: Homeland Air & Missile Defense",
    unit="USD",
    keywords=["defense", "first principles", "air defense", "missile defense", "NORAD"],
    latex_symbol=r"D_{air}",
)

US_DEFENSE_FP_COAST_GUARD = Parameter(
    14_000_000_000,
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="definition",
    confidence="high",
    distribution=DistributionType.NORMAL,
    confidence_interval=(12_000_000_000, 16_000_000_000),
    std_error=1_500_000_000,
    description="US Coast Guard (actual budget ~$14B). Maritime homeland security and coastal "
                "defense.",
    display_name="First-Principles Defense: Coast Guard",
    unit="USD",
    keywords=["defense", "first principles", "coast guard", "maritime", "homeland"],
    latex_symbol=r"D_{cg}",
)

US_DEFENSE_FP_NATIONAL_GUARD = Parameter(
    30_000_000_000,
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="definition",
    confidence="medium",
    distribution=DistributionType.NORMAL,
    confidence_interval=(24_000_000_000, 40_000_000_000),
    std_error=4_000_000_000,
    description="National Guard / territorial land defense: a citizen-soldier reserve (the "
                "Switzerland model) for homeland defense and disaster response.",
    display_name="First-Principles Defense: National Guard",
    unit="USD",
    keywords=["defense", "first principles", "national guard", "reserve", "territorial"],
    latex_symbol=r"D_{guard}",
)

US_DEFENSE_FP_CYBER = Parameter(
    15_000_000_000,
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="definition",
    confidence="medium",
    distribution=DistributionType.NORMAL,
    confidence_interval=(10_000_000_000, 25_000_000_000),
    std_error=4_000_000_000,
    description="Cyber defense of critical infrastructure: the primary modern attack vector that "
                "crosses oceans in milliseconds and is not stopped by geography.",
    display_name="First-Principles Defense: Cyber Defense",
    unit="USD",
    keywords=["defense", "first principles", "cyber", "infrastructure", "CYBERCOM"],
    latex_symbol=r"D_{cyber}",
)

US_DEFENSE_FP_MOBILIZATION_HEDGE = Parameter(
    60_000_000_000,
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="definition",
    confidence="medium",
    distribution=DistributionType.NORMAL,
    confidence_interval=(40_000_000_000, 100_000_000_000),
    std_error=15_000_000_000,
    description="Mobilization hedge: defense R&D, a maintained industrial base, and a professional "
                "cadre force. The WWII lesson is to maintain the capacity to scale, not a standing "
                "empire: a peer buildup gives years of warning, and the US went from the 17th-ranked "
                "army in 1939 to victory in four years. This is the cheapest insurance and the most "
                "neglected.",
    display_name="First-Principles Defense: Mobilization Hedge",
    unit="USD",
    keywords=["defense", "first principles", "mobilization", "R&D", "industrial base", "cadre"],
    latex_symbol=r"D_{hedge}",
)

# First-principles optimal homeland-defense budget = sum of the threat-tier components.
US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL = Parameter(
    (US_DEFENSE_FP_NUCLEAR_DETERRENT +
     US_DEFENSE_FP_HOMELAND_AIR_MISSILE +
     US_DEFENSE_FP_COAST_GUARD +
     US_DEFENSE_FP_NATIONAL_GUARD +
     US_DEFENSE_FP_CYBER +
     US_DEFENSE_FP_MOBILIZATION_HEDGE),
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="calculated",
    confidence="medium",
    description="First-principles optimal US homeland-defense budget: the bottom-up sum of what "
                "defending the United States actually requires at efficient prices. Nuclear second "
                "strike $30B + homeland air/missile defense $35B + Coast Guard $14B + National Guard "
                "$30B + cyber defense $15B + mobilization hedge $60B = ~$184B. Honest range "
                "~$130-260B. Compare: current ~$886B. Restraint-school proposals (Posen, Cato) and "
                "peer benchmarks land higher (~$450-675B) because they cost reduced hegemony and "
                "allied/peer deterrence, not homeland defense.",
    display_name="First-Principles Optimal US Defense Budget",
    unit="USD",
    formula="Nuclear + HomelandAirMissile + CoastGuard + NationalGuard + Cyber + MobilizationHedge",
    inputs=[
        "US_DEFENSE_FP_NUCLEAR_DETERRENT",
        "US_DEFENSE_FP_HOMELAND_AIR_MISSILE",
        "US_DEFENSE_FP_COAST_GUARD",
        "US_DEFENSE_FP_NATIONAL_GUARD",
        "US_DEFENSE_FP_CYBER",
        "US_DEFENSE_FP_MOBILIZATION_HEDGE",
    ],
    compute=lambda ctx: (
        ctx["US_DEFENSE_FP_NUCLEAR_DETERRENT"] +
        ctx["US_DEFENSE_FP_HOMELAND_AIR_MISSILE"] +
        ctx["US_DEFENSE_FP_COAST_GUARD"] +
        ctx["US_DEFENSE_FP_NATIONAL_GUARD"] +
        ctx["US_DEFENSE_FP_CYBER"] +
        ctx["US_DEFENSE_FP_MOBILIZATION_HEDGE"]
    ),
    keywords=["defense", "first principles", "optimal", "homeland", "deterrence", "budget"],
    latex_symbol=r"D_{optimal}",
)

# Component 1.1: Military overspend [CATEGORY 1: Direct Spending]
# = current US military spending minus the first-principles homeland-defense optimum.
US_GOV_WASTE_MILITARY_OVERSPEND = Parameter(
    886_000_000_000 - US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL,  # current (US_MILITARY_SPENDING_2024_ANNUAL) - optimum
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="US military spending above the first-principles homeland-defense optimum. Current "
                "US military spending (~$886B) supports global power projection (~750 overseas "
                "bases). A bottom-up, threat-by-threat homeland-defense budget is ~$184B (nuclear "
                "second strike $30B, homeland air/missile defense $35B, Coast Guard $14B, National "
                "Guard $30B, cyber defense $15B, mobilization hedge $60B). Delta = $886B - $184B = "
                "~$702B 'Hegemony Tax'. [CATEGORY 1: Direct Spending]",
    display_name="Military Overspend",
    unit="USD",
    formula="US_MILITARY_SPENDING_2024_ANNUAL - US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL",
    inputs=["US_MILITARY_SPENDING_2024_ANNUAL", "US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL"],
    compute=lambda ctx: ctx["US_MILITARY_SPENDING_2024_ANNUAL"] - ctx["US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL"],
    keywords=["military", "defense", "overspend", "hegemony", "pentagon", "category_1_direct_spending"],
    latex_symbol=r"W_{military}",
)

# Implied cut from current US military spending to the first-principles optimum.
US_DEFENSE_FIRST_PRINCIPLES_CUT_PCT = Parameter(
    1 - (US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL / 886_000_000_000),  # 1 - optimum / current
    manual_ref="knowledge/economics/eisenhower-curve.qmd",
    source_type="calculated",
    confidence="medium",
    description="Implied cut from current US military spending (~$886B) to the first-principles "
                "homeland-defense optimum (~$184B): ~79%. For comparison, the US cut military "
                "spending 87.6% in two years after WWII.",
    display_name="First-Principles Defense Cut (%)",
    unit="percent",
    formula="1 - (US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL / US_MILITARY_SPENDING_2024_ANNUAL)",
    inputs=["US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL", "US_MILITARY_SPENDING_2024_ANNUAL"],
    compute=lambda ctx: 1 - (ctx["US_DEFENSE_FIRST_PRINCIPLES_OPTIMAL"] / ctx["US_MILITARY_SPENDING_2024_ANNUAL"]),
    keywords=["defense", "cut", "first principles", "reduction", "percent"],
    latex_symbol=r"Cut_{FP}",
)

# What the annual military overspend could buy in clinical trials, computed the SAME way as the
# 1% treaty's 12.3x capacity figure: patients fundable at the pragmatic-trial cost, relative to
# the people currently in trials. NOT a ratio of current dollar spending (which would price trials
# at today's ~$41k traditional cost and break the comparison with the treaty methodology).
US_MILITARY_OVERSPEND_PATIENTS_FUNDABLE = Parameter(
    US_GOV_WASTE_MILITARY_OVERSPEND / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    manual_ref="knowledge/appendix/cost-benefit-of-hegemony.qmd",
    source_type="calculated",
    confidence="medium",
    description="Trial participants the annual US military overspend (~$702B) could fund at the "
                "empirical pragmatic-trial cost (~$929/patient): ~756M patients/year. Patient-based, "
                "the direct parallel of DFDA_PATIENTS_FUNDABLE_ANNUALLY (the treaty's ~23.4M).",
    display_name="Patients Fundable by Military Overspend (Pragmatic Trials)",
    unit="patients/year",
    formula="US_GOV_WASTE_MILITARY_OVERSPEND / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT",
    inputs=["US_GOV_WASTE_MILITARY_OVERSPEND", "DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    compute=lambda ctx: ctx["US_GOV_WASTE_MILITARY_OVERSPEND"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    keywords=["overspend", "patients", "fundable", "pragmatic trials", "capacity"],
    latex_symbol=r"N_{fundable,overspend}",
)

US_MILITARY_OVERSPEND_TRIAL_CAPACITY_MULTIPLIER = Parameter(
    US_MILITARY_OVERSPEND_PATIENTS_FUNDABLE / CURRENT_TRIAL_SLOTS_AVAILABLE,
    manual_ref="knowledge/appendix/cost-benefit-of-hegemony.qmd",
    source_type="calculated",
    confidence="medium",
    description="Patients the overspend could fund in pragmatic trials (~756M/year at ~$929 each) "
                "relative to the ~1.9M people currently in trials: ~398x. Identical methodology to "
                "the treaty's DFDA_TRIAL_CAPACITY_MULTIPLIER (12.3x), scaled to the overspend. The "
                "current 1.9M is capped by the ~$41k cost of a traditional trial, NOT by a shortage "
                "of patients: aging is a universal trial population and billions have suboptimally-"
                "treated chronic disease. The binding constraint is building decentralized trial "
                "infrastructure, not patient supply.",
    display_name="Military Overspend Pragmatic Trial Capacity Multiplier",
    unit="x",
    formula="US_MILITARY_OVERSPEND_PATIENTS_FUNDABLE / CURRENT_TRIAL_SLOTS_AVAILABLE",
    inputs=["US_MILITARY_OVERSPEND_PATIENTS_FUNDABLE", "CURRENT_TRIAL_SLOTS_AVAILABLE"],
    compute=lambda ctx: ctx["US_MILITARY_OVERSPEND_PATIENTS_FUNDABLE"] / ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"],
    keywords=["overspend", "clinical trials", "capacity", "multiplier", "pragmatic"],
    latex_symbol=r"k_{capacity,overspend}",
)

# Component 1.2: Corporate welfare ($181B) [CATEGORY 1: Direct Spending]
US_GOV_WASTE_CORPORATE_WELFARE = Parameter(
    181_000_000_000,  # $181B annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="high",
    description="Direct US federal corporate welfare: subsidies to agriculture ($16.4B), "
                "green energy tax credits, semiconductor aid, aviation support. "
                "Agricultural subsidies are highly regressive (top 10% receive 63%). "
                "Cato Institute forensic tally. [CATEGORY 1: Direct Spending]",
    display_name="Corporate Welfare Waste",
    unit="USD",
    distribution=DistributionType.NORMAL,
    confidence_interval=(150_000_000_000, 220_000_000_000),
    std_error=20_000_000_000,
    keywords=["corporate welfare", "subsidy", "waste", "agriculture", "capture", "category_1_direct_spending"],
    latex_symbol=r"W_{corporate}",
)

# Component 1.3: Drug war ($90B) [CATEGORY 1: Direct Spending]
US_GOV_WASTE_DRUG_WAR = Parameter(
    90_000_000_000,  # $90B annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="drugpolicyalliance2021",
    source_type="external",
    confidence="medium",
    description="Annual cost of drug war: ~$41B federal drug control budget, "
                "~$10B state/local enforcement, ~$40B incarceration and lost productivity. "
                "After 50+ years and $1T+ spent, drug use is higher than ever. "
                "[CATEGORY 1: Direct Spending]",
    display_name="Drug War Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(60_000_000_000, 150_000_000_000),
    std_error=30_000_000_000,
    keywords=["drug war", "incarceration", "enforcement", "prohibition", "failed", "category_1_direct_spending"],
    latex_symbol=r"W_{drugs}",
)

# Component 1.4: Fossil fuel subsidies - explicit only ($50B) [CATEGORY 1: Direct Spending]
US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES = Parameter(
    50_000_000_000,  # $50B annually (explicit only, not externalities)
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="imf-fossilfuel2023",
    source_type="external",
    confidence="medium",
    description="US explicit fossil fuel subsidies (direct payments, tax breaks). "
                "IMF estimates US total subsidies at $649B but ~92% is implicit (externalities). "
                "This figure includes only explicit subsidies (~$50B) for defensibility. "
                "[CATEGORY 1: Direct Spending]",
    display_name="Fossil Fuel Subsidies (Explicit)",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(30_000_000_000, 80_000_000_000),
    std_error=15_000_000_000,
    keywords=["fossil fuel", "subsidy", "oil", "gas", "coal", "category_1_direct_spending"],
    latex_symbol=r"W_{fossil}",
)

# Component 1.5: Agricultural subsidies deadweight loss ($75B) [CATEGORY 1: Direct Spending]
US_GOV_WASTE_AGRICULTURAL_SUBSIDIES = Parameter(
    75_000_000_000,  # $75B annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="ewg-farm-subsidies",
    source_type="external",
    confidence="high",
    description="Deadweight loss from US agricultural subsidies. Direct subsidies ~$30B/yr but create "
                "larger distortions: overproduction, environmental damage, benefits concentrated in large "
                "farms (top 10% receive 78% of subsidies). Total welfare loss ~$75B. "
                "Textbook example of capture; very high economist consensus. [CATEGORY 1: Direct Spending]",
    display_name="Agricultural Subsidies Deadweight Loss",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(50_000_000_000, 120_000_000_000),
    std_error=25_000_000_000,
    keywords=["agriculture", "farm", "subsidy", "deadweight", "capture", "category_1_direct_spending"],
    latex_symbol=r"W_{agriculture}",
)

# ==============================================================================
# CATEGORY 2: COMPLIANCE BURDEN ON PRIVATE SECTOR (~$1.13T)
# Private sector resources consumed by government-imposed compliance requirements.
# Solution: Simplification (tax code reform, regulatory streamlining).
# ==============================================================================

# Component 2.1: Tax compliance ($546B) [CATEGORY 2: Compliance Burden]
US_GOV_WASTE_TAX_COMPLIANCE = Parameter(
    546_000_000_000,  # $546B annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="taxfoundation2024-compliance",
    source_type="external",
    confidence="high",
    description="Annual cost of US tax code compliance: 7.9 billion hours of lost productivity ($413B) "
                "plus $133B in out-of-pocket costs. Equals nearly 2% of GDP. "
                "Could be largely eliminated with simplified tax code or return-free filing. "
                "[CATEGORY 2: Compliance Burden]",
    display_name="Tax Compliance Waste",
    unit="USD",
    distribution=DistributionType.NORMAL,
    confidence_interval=(450_000_000_000, 650_000_000_000),
    std_error=50_000_000_000,
    keywords=["tax", "compliance", "IRS", "bureaucracy", "waste", "category_2_compliance"],
    latex_symbol=r"W_{tax}",
)

# Component 2.2: Regulatory red tape ($580B) [CATEGORY 2: Compliance Burden]
US_GOV_WASTE_REGULATORY_RED_TAPE = Parameter(
    580_000_000_000,  # $580B annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="medium",
    description="Deadweight loss from US regulatory red tape (procedural friction without "
                "safety benefits). Competitive Enterprise Institute estimates total regulatory "
                "burden at $2.15T; European studies find red tape costs 0.1-4% of GDP. "
                "Conservative estimate: ~2% of US GDP = $580B. [CATEGORY 2: Compliance Burden]",
    display_name="Regulatory Red Tape Waste",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(290_000_000_000, 1_000_000_000_000),
    std_error=200_000_000_000,
    keywords=["regulatory", "red tape", "bureaucracy", "waste", "compliance", "category_2_compliance"],
    latex_symbol=r"W_{regulatory}",
)

# ==============================================================================
# CATEGORY 3: POLICY-INDUCED GDP LOSS (~$1.56T)
# Economic output foregone due to policy constraints on markets.
# Solution: Policy reform (zoning liberalization, trade policy).
# ==============================================================================

# Component 3.1: Housing/zoning restrictions ($1.4T) [CATEGORY 3: GDP Loss]
US_GOV_WASTE_HOUSING_ZONING = Parameter(
    1_400_000_000_000,  # $1.4T annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="hsieh-moretti2019",
    source_type="external",
    confidence="medium",
    description="GDP loss from housing/zoning restrictions. Original Hsieh-Moretti (2019 AEJ:Macro) estimate "
                "of 36% GDP growth reduction was substantially revised by Greaney (2023). "
                "Current $1.4T represents a moderate estimate; revised lower bound implies ~$500B. "
                "[CATEGORY 3: GDP Loss]",
    display_name="Housing/Zoning Restrictions Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(500_000_000_000, 2_000_000_000_000),
    std_error=300_000_000_000,
    keywords=["housing", "zoning", "NIMBY", "land use", "productivity", "misallocation", "category_3_gdp_loss"],
    latex_symbol=r"W_{housing}",
)

# Component 3.2: Tariffs ($160B) [CATEGORY 3: GDP Loss]
US_GOV_WASTE_TARIFFS = Parameter(
    160_000_000_000,  # $160B annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="yalebudgetlab2025",
    source_type="external",
    confidence="medium",
    description="Annual GDP reduction from US tariffs and retaliation. "
                "Yale Budget Lab estimates 0.6% smaller GDP in long run, equivalent to $160B annually. "
                "Trade barriers reduce efficiency and raise consumer prices. [CATEGORY 3: GDP Loss]",
    display_name="Tariff Cost (GDP Loss)",
    unit="USD",
    distribution=DistributionType.NORMAL,
    confidence_interval=(90_000_000_000, 250_000_000_000),
    std_error=50_000_000_000,
    keywords=["tariffs", "trade", "protectionism", "GDP loss", "category_3_gdp_loss"],
    latex_symbol=r"W_{tariffs}",
)

# ==============================================================================
# CATEGORY 4: TOTAL SYSTEM INEFFICIENCY (~$1.20T)
# Fundamental system design failures requiring structural redesign.
# Solution: System redesign (competitive market models like Singapore/Switzerland).
# ==============================================================================

# Component 4.1: Healthcare system inefficiency ($1.2T) [CATEGORY 4: System Inefficiency]
US_GOV_WASTE_HEALTHCARE_INEFFICIENCY = Parameter(
    1_200_000_000_000,  # $1.2T annually
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="papanicolas2018",
    source_type="external",
    confidence="high",
    description="US healthcare spending inefficiency. US spends ~$4.5T/yr (18% GDP) vs 9-11% in comparable "
                "OECD countries with similar/better outcomes. Papanicolas et al. (2018 JAMA) and multiple "
                "studies document $1-1.5T in excess spending from administrative complexity, high prices, "
                "and poor care coordination. Very high economist consensus. [CATEGORY 4: System Inefficiency]",
    display_name="Healthcare System Inefficiency",
    unit="USD",
    distribution=DistributionType.NORMAL,
    confidence_interval=(1_000_000_000_000, 1_500_000_000_000),
    std_error=150_000_000_000,
    keywords=["healthcare", "inefficiency", "administrative", "waste", "OECD", "category_4_system"],
    latex_symbol=r"W_{health}",
)

# ==============================================================================
# CATEGORY SUBTOTALS
# Aggregated totals for each dysfunction category
# ==============================================================================

# Category 1 Subtotal: Direct Federal Spending Waste (~$1.01T)
US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING = Parameter(
    (US_GOV_WASTE_MILITARY_OVERSPEND +
     US_GOV_WASTE_CORPORATE_WELFARE +
     US_GOV_WASTE_DRUG_WAR +
     US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES +
     US_GOV_WASTE_AGRICULTURAL_SUBSIDIES),
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="Category 1: Direct Federal Spending Waste. Actual federal budget allocations "
                "that could be redirected. Includes military overspend ($615B), corporate welfare "
                "($181B), drug war ($90B), fossil fuel subsidies ($50B), and agricultural subsidies "
                "($75B). Total: ~$1.01T annually. Solution: Budget reallocation.",
    display_name="Category 1: Direct Spending Waste",
    unit="USD",
    formula="Military + Corporate + Drug War + Fossil + Agriculture",
    inputs=[
        "US_GOV_WASTE_MILITARY_OVERSPEND",
        "US_GOV_WASTE_CORPORATE_WELFARE",
        "US_GOV_WASTE_DRUG_WAR",
        "US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES",
        "US_GOV_WASTE_AGRICULTURAL_SUBSIDIES",
    ],
    compute=lambda ctx: (
        ctx["US_GOV_WASTE_MILITARY_OVERSPEND"] +
        ctx["US_GOV_WASTE_CORPORATE_WELFARE"] +
        ctx["US_GOV_WASTE_DRUG_WAR"] +
        ctx["US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES"] +
        ctx["US_GOV_WASTE_AGRICULTURAL_SUBSIDIES"]
    ),
    keywords=["category_1", "direct_spending", "budget", "waste", "reallocation"],
    latex_symbol=r"W_{cat1}",
)

# Category 2 Subtotal: Compliance Burden (~$1.13T)
US_GOV_WASTE_CATEGORY_2_COMPLIANCE = Parameter(
    US_GOV_WASTE_TAX_COMPLIANCE + US_GOV_WASTE_REGULATORY_RED_TAPE,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="Category 2: Compliance Burden on Private Sector. Private sector resources consumed "
                "by government-imposed compliance requirements. Includes tax compliance ($546B) and "
                "regulatory red tape ($580B). Total: ~$1.13T annually. Solution: Simplification "
                "(tax code reform, regulatory streamlining).",
    display_name="Category 2: Compliance Burden",
    unit="USD",
    formula="Tax Compliance + Regulatory Red Tape",
    inputs=[
        "US_GOV_WASTE_TAX_COMPLIANCE",
        "US_GOV_WASTE_REGULATORY_RED_TAPE",
    ],
    compute=lambda ctx: (
        ctx["US_GOV_WASTE_TAX_COMPLIANCE"] +
        ctx["US_GOV_WASTE_REGULATORY_RED_TAPE"]
    ),
    keywords=["category_2", "compliance", "red_tape", "waste", "simplification"],
    latex_symbol=r"W_{cat2}",
)

# Category 3 Subtotal: Policy-Induced GDP Loss (~$1.56T)
US_GOV_WASTE_CATEGORY_3_GDP_LOSS = Parameter(
    US_GOV_WASTE_HOUSING_ZONING + US_GOV_WASTE_TARIFFS,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="Category 3: Policy-Induced GDP Loss. Economic output foregone due to policy "
                "constraints on markets. Includes housing/zoning restrictions ($1.4T) and tariffs "
                "($160B). Total: ~$1.56T annually. Solution: Policy reform (zoning liberalization, "
                "trade policy).",
    display_name="Category 3: GDP Loss",
    unit="USD",
    formula="Housing/Zoning + Tariffs",
    inputs=[
        "US_GOV_WASTE_HOUSING_ZONING",
        "US_GOV_WASTE_TARIFFS",
    ],
    compute=lambda ctx: (
        ctx["US_GOV_WASTE_HOUSING_ZONING"] +
        ctx["US_GOV_WASTE_TARIFFS"]
    ),
    keywords=["category_3", "gdp_loss", "policy", "waste", "reform"],
    latex_symbol=r"W_{cat3}",
)

# Category 4 Subtotal: System Inefficiency (~$1.20T)
US_GOV_WASTE_CATEGORY_4_SYSTEM = Parameter(
    US_GOV_WASTE_HEALTHCARE_INEFFICIENCY,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="high",
    description="Category 4: Total System Inefficiency. Fundamental system design failures requiring "
                "structural redesign. Currently only healthcare system inefficiency ($1.2T). "
                "Solution: System redesign using competitive market models (Singapore's catastrophic "
                "coverage + HSAs, Switzerland's regulated competition).",
    display_name="Category 4: System Inefficiency",
    unit="USD",
    formula="Healthcare Inefficiency",
    inputs=["US_GOV_WASTE_HEALTHCARE_INEFFICIENCY"],
    compute=lambda ctx: ctx["US_GOV_WASTE_HEALTHCARE_INEFFICIENCY"],
    keywords=["category_4", "system", "healthcare", "waste", "redesign"],
    latex_symbol=r"W_{cat4}",
)

# Overlap discount factor (removed - categories treated as additive)
US_GOV_WASTE_OVERLAP_DISCOUNT = Parameter(
    1.0,  # No overlap discount applied
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="definition",
    confidence="high",
    distribution="fixed",
    description="Overlap discount factor between US government waste categories. "
                "Set to 1.0 (no discount). Categories are treated as additive, "
                "recognizing that any overlap is offset by excluded categories "
                "(state/local inefficiency, implicit subsidies, behavioral effects).",
    display_name="Overlap Discount Factor",
    unit="ratio",
    keywords=["overlap", "discount", "double counting"],
    latex_symbol=r"\delta_{overlap}",
)

# Raw total (before overlap discount)
US_GOV_WASTE_RAW_TOTAL = Parameter(
    (US_GOV_WASTE_HEALTHCARE_INEFFICIENCY +
     US_GOV_WASTE_HOUSING_ZONING +
     US_GOV_WASTE_MILITARY_OVERSPEND +
     US_GOV_WASTE_REGULATORY_RED_TAPE +
     US_GOV_WASTE_TAX_COMPLIANCE +
     US_GOV_WASTE_CORPORATE_WELFARE +
     US_GOV_WASTE_TARIFFS +
     US_GOV_WASTE_DRUG_WAR +
     US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES +
     US_GOV_WASTE_AGRICULTURAL_SUBSIDIES),
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="Raw sum of US government waste components before overlap discount: "
                "healthcare ($1.2T) + housing ($1.4T) + military ($615B) + regulatory ($580B) + "
                "tax ($546B) + corporate ($181B) + tariffs ($160B) + drug war ($90B) + "
                "fossil fuel ($50B) + agriculture ($75B) = ~$4.9T raw.",
    display_name="US Gov Waste (Raw Total)",
    unit="USD",
    formula="SUM(all 10 components)",
    inputs=[
        "US_GOV_WASTE_HEALTHCARE_INEFFICIENCY",
        "US_GOV_WASTE_HOUSING_ZONING",
        "US_GOV_WASTE_MILITARY_OVERSPEND",
        "US_GOV_WASTE_REGULATORY_RED_TAPE",
        "US_GOV_WASTE_TAX_COMPLIANCE",
        "US_GOV_WASTE_CORPORATE_WELFARE",
        "US_GOV_WASTE_TARIFFS",
        "US_GOV_WASTE_DRUG_WAR",
        "US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES",
        "US_GOV_WASTE_AGRICULTURAL_SUBSIDIES",
    ],
    compute=lambda ctx: (
        ctx["US_GOV_WASTE_HEALTHCARE_INEFFICIENCY"] +
        ctx["US_GOV_WASTE_HOUSING_ZONING"] +
        ctx["US_GOV_WASTE_MILITARY_OVERSPEND"] +
        ctx["US_GOV_WASTE_REGULATORY_RED_TAPE"] +
        ctx["US_GOV_WASTE_TAX_COMPLIANCE"] +
        ctx["US_GOV_WASTE_CORPORATE_WELFARE"] +
        ctx["US_GOV_WASTE_TARIFFS"] +
        ctx["US_GOV_WASTE_DRUG_WAR"] +
        ctx["US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES"] +
        ctx["US_GOV_WASTE_AGRICULTURAL_SUBSIDIES"]
    ),
    keywords=["waste", "US", "raw total", "government"],
    latex_symbol=r"W_{raw,US}",
)

# Total US government waste (no overlap discount)
US_GOV_WASTE_TOTAL = Parameter(
    US_GOV_WASTE_RAW_TOTAL * US_GOV_WASTE_OVERLAP_DISCOUNT,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="Total annual US government waste (additive sum of components). "
                "Consolidates healthcare ($1.2T), housing ($1.4T), military ($615B), "
                "regulatory ($580B), tax ($546B), corporate ($181B), tariffs ($160B), "
                "drug war ($90B), fossil fuel ($50B), agriculture ($75B). "
                "Categories treated as additive; any overlap offset by excluded categories "
                "(state/local inefficiency, implicit subsidies, behavioral effects). ~$4.9T annually.",
    display_name="US Government Waste (Total)",
    unit="USD",
    formula="SUM(all components)",
    inputs=["US_GOV_WASTE_RAW_TOTAL", "US_GOV_WASTE_OVERLAP_DISCOUNT"],
    compute=lambda ctx: ctx["US_GOV_WASTE_RAW_TOTAL"] * ctx["US_GOV_WASTE_OVERLAP_DISCOUNT"],
    keywords=["waste", "US", "total", "government", "dysfunction"],
    latex_symbol=r"W_{total,US}",
)

# US Federal Discretionary Spending (FY2024) - denominator for discretionary efficiency
US_FED_DISCRETIONARY_SPENDING_2024 = Parameter(
    1_700_000_000_000,  # $886B defense + ~$814B non-defense
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="cbo-long-term-budget-2024",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US federal discretionary spending in FY2024. Approximately $886B defense + "
                "~$814B non-defense discretionary = ~$1.7T. Used as denominator for "
                "discretionary efficiency rating (Cat 1 waste items are discretionary/fungible).",
    display_name="US Federal Discretionary Spending (FY2024)",
    unit="USD",
    keywords=["federal", "discretionary", "spending", "budget", "US", "FY2024"],
    latex_symbol=r"Spending_{US,disc}",
)

# Cat 1 direct waste as percentage of discretionary spending
US_FED_DISCRETIONARY_WASTE_PCT = Parameter(
    US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING / US_FED_DISCRETIONARY_SPENDING_2024,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="Category 1 direct spending waste as percentage of federal discretionary spending. "
                "~$1.01T Cat 1 waste / $1.7T discretionary = ~59%. Uses discretionary spending as "
                "denominator because Cat 1 items (military overspend, corporate welfare, drug war, "
                "fossil/ag subsidies) are fungible policy choices within discretionary budget.",
    display_name="Discretionary Waste (%)",
    unit="percent",
    formula="US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING / US_FED_DISCRETIONARY_SPENDING_2024",
    inputs=["US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING", "US_FED_DISCRETIONARY_SPENDING_2024"],
    compute=lambda ctx: ctx["US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING"] / ctx["US_FED_DISCRETIONARY_SPENDING_2024"],
    keywords=["waste", "US", "discretionary", "spending", "percentage"],
    latex_symbol=r"W_{US,\%disc}",
)

# US federal discretionary efficiency (complement of Cat 1 waste / discretionary)
US_FED_DISCRETIONARY_EFFICIENCY = Parameter(
    1 - (US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING / US_FED_DISCRETIONARY_SPENDING_2024),
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    unit="percent",
    description="US federal discretionary spending efficiency. What fraction of discretionary "
                "spending avoids direct waste (Cat 1 only: military overspend, corporate welfare, "
                "drug war, fossil/ag subsidies). ~41%. Some Cat 1 items (farm subsidies, tax "
                "expenditures) are technically mandatory/off-budget but are fungible policy choices.",
    display_name="US Discretionary Efficiency",
    formula="1 - (CAT1 / DISCRETIONARY)",
    inputs=["US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING", "US_FED_DISCRETIONARY_SPENDING_2024"],
    compute=lambda ctx: 1 - (ctx["US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING"] / ctx["US_FED_DISCRETIONARY_SPENDING_2024"]),
    keywords=["efficiency", "rating", "US", "federal", "discretionary"],
    latex_symbol=r"E_{US,disc}",
)

# US governance efficiency (total waste as share of GDP)
US_GOVERNANCE_EFFICIENCY_GDP = Parameter(
    1 - (US_GOV_WASTE_TOTAL / US_GDP_2024),
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    unit="percent",
    description="Total US governance efficiency: all 4 waste categories as share of GDP. "
                "1 - ($4.9T / $28.78T) = ~83%. This broader metric captures direct spending waste, "
                "compliance burden, policy-induced GDP loss, and system inefficiency relative to "
                "total economic output.",
    display_name="US Governance Efficiency (GDP)",
    formula="1 - (US_GOV_WASTE_TOTAL / US_GDP)",
    inputs=["US_GOV_WASTE_TOTAL", "US_GDP_2024"],
    compute=lambda ctx: 1 - (ctx["US_GOV_WASTE_TOTAL"] / ctx["US_GDP_2024"]),
    keywords=["efficiency", "rating", "US", "governance", "GDP"],
    latex_symbol=r"E_{US,GDP}",
)

# US waste as percentage of GDP
US_GOV_WASTE_PCT_GDP = Parameter(
    US_GOV_WASTE_TOTAL / US_GDP_2024,
    manual_ref="knowledge/appendix/optimocracy-paper.qmd",
    source_type="calculated",
    confidence="medium",
    description="US government waste as percentage of GDP. "
                "~$4.90T waste / $28.78T GDP = ~17%. This represents the 'dysfunction tax' "
                "that American citizens effectively pay through inefficient governance.",
    display_name="US Waste (% GDP)",
    unit="percent",
    formula="US_GOV_WASTE_TOTAL / US_GDP",
    inputs=["US_GOV_WASTE_TOTAL", "US_GDP_2024"],
    compute=lambda ctx: ctx["US_GOV_WASTE_TOTAL"] / ctx["US_GDP_2024"],
    keywords=["waste", "US", "GDP", "percentage", "dysfunction"],
    latex_symbol=r"W_{US,\%GDP}",
)

# ---
# VALUATION STANDARDS FOR HUMAN COST QUANTIFICATION
# ---

# DOT Value of Statistical Life ($13.7M) - used in federal efficiency audit
DOT_VALUE_OF_STATISTICAL_LIFE = Parameter(
    13_700_000,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="dot-vsl-2024",
    source_type="external",
    description="DOT Value of Statistical Life (2024). Used by federal agencies to "
                "evaluate safety regulations and quantify the economic value of mortality risk reductions.",
    display_name="DOT VSL",
    unit="USD",
    distribution="fixed",
    confidence="high",
    latex_symbol=r"VSL_{DOT}",
    keywords=["VSL", "value of statistical life", "safety", "DOT", "mortality"],
)

# Medical cost-effectiveness QALY threshold ($100K)
MEDICAL_QALY_THRESHOLD = Parameter(
    100_000,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="qaly-threshold-history",
    source_type="external",
    description="Medical cost-effectiveness QALY threshold. Standard threshold for "
                "evaluating whether health interventions are cost-effective. "
                "Interventions below $100K/QALY are generally considered cost-effective.",
    display_name="Medical QALY Threshold",
    unit="USD/QALY",
    distribution="fixed",
    confidence="high",
    latex_symbol=r"QALY_{threshold}",
    keywords=["QALY", "cost-effectiveness", "health economics", "threshold"],
)

# US waste expressed as VSL equivalents
US_GOV_WASTE_VSL_EQUIVALENTS = Parameter(
    US_GOV_WASTE_TOTAL / DOT_VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="US government waste expressed as VSL equivalents. "
                "This is an economic equivalent, NOT literal deaths. "
                "Dividing the efficiency gap by VSL yields a measure of foregone welfare.",
    display_name="US Waste (VSL Equivalents)",
    unit="people",
    formula="US_GOV_WASTE_TOTAL / DOT_VSL",
    inputs=["US_GOV_WASTE_TOTAL", "DOT_VALUE_OF_STATISTICAL_LIFE"],
    compute=lambda ctx: ctx["US_GOV_WASTE_TOTAL"] / ctx["DOT_VALUE_OF_STATISTICAL_LIFE"],
    latex_symbol=r"W_{US,VSL}",
    keywords=["VSL", "equivalents", "waste", "human cost"],
)

# US waste expressed as QALY equivalents
US_GOV_WASTE_QALY_EQUIVALENTS = Parameter(
    US_GOV_WASTE_TOTAL / MEDICAL_QALY_THRESHOLD,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="US government waste expressed as QALY equivalents. "
                "This is an economic equivalent, NOT epidemiological health outcomes. "
                "Dividing by QALY threshold yields a measure of foregone welfare.",
    display_name="US Waste (QALY Equivalents)",
    unit="QALYs",
    formula="US_GOV_WASTE_TOTAL / QALY_THRESHOLD",
    inputs=["US_GOV_WASTE_TOTAL", "MEDICAL_QALY_THRESHOLD"],
    compute=lambda ctx: ctx["US_GOV_WASTE_TOTAL"] / ctx["MEDICAL_QALY_THRESHOLD"],
    latex_symbol=r"W_{US,QALY}",
    keywords=["QALY", "equivalents", "waste", "human cost"],
)

# US waste vs treaty funding multiplier
US_GOV_WASTE_VS_TREATY_MULTIPLIER = Parameter(
    US_GOV_WASTE_TOTAL / TREATY_ANNUAL_FUNDING,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="medium",
    description="How many times the US government efficiency gap could fund the 1% Treaty. "
                "The efficiency gap represents capital that could fund transformative "
                "health research many times over.",
    display_name="Efficiency Gap / Treaty Funding",
    unit="ratio",
    formula="US_GOV_WASTE_TOTAL / TREATY_ANNUAL_FUNDING",
    inputs=["US_GOV_WASTE_TOTAL", "TREATY_ANNUAL_FUNDING"],
    compute=lambda ctx: ctx["US_GOV_WASTE_TOTAL"] / ctx["TREATY_ANNUAL_FUNDING"],
    latex_symbol=r"k_{waste:treaty}",
    keywords=["multiplier", "treaty", "waste", "funding"],
)

# Recoverable capital (if US improved to OECD median 80% efficiency)
US_GOV_WASTE_RECOVERABLE = Parameter(
    US_GOV_WASTE_TOTAL * 0.50,  # ~50% of gap is recoverable (38% -> 80%)
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    confidence="low",
    description="Recoverable capital if US improved to OECD median efficiency. "
                "Current US efficiency ~38-48%; OECD median ~75-85%. "
                "Closing to ~80% would recover approximately half the gap.",
    display_name="Recoverable Capital",
    unit="USD",
    formula="US_GOV_WASTE_TOTAL x 0.50",
    inputs=["US_GOV_WASTE_TOTAL"],
    compute=lambda ctx: ctx["US_GOV_WASTE_TOTAL"] * 0.50,
    latex_symbol=r"W_{US,recoverable}",
    keywords=["recoverable", "OECD", "efficiency", "waste"],
)

# =============================================================================
# EFFICIENCY CALCULATION
# =============================================================================
# From paper Part 3: E = Adjusted W_real / W_max
# NOTE: Moved here after US_GOV_WASTE_TOTAL is defined to avoid forward reference error

POLITICAL_DYSFUNCTION_GLOBAL_WASTE_TOTAL = Parameter(
    US_GOV_WASTE_TOTAL + POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    confidence="medium",
    description="Global waste deduction used in Political Dysfunction Tax efficiency accounting. "
                "Combines US governance waste estimate with global explicit fossil-fuel subsidies.",
    display_name="Global Waste Total (Efficiency Accounting)",
    unit="USD",
    formula="US_GOV_WASTE_TOTAL + POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES",
    inputs=["US_GOV_WASTE_TOTAL", "POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES"],
    compute=lambda ctx: (
        ctx["US_GOV_WASTE_TOTAL"] +
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES"]
    ),
    keywords=["waste", "global", "efficiency", "ledger"],
    latex_symbol=r"W_{waste}",
)

POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED = Parameter(
    GLOBAL_GDP_2025 - POLITICAL_DYSFUNCTION_GLOBAL_WASTE_TOTAL,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    confidence="medium",
    description="Adjusted realized welfare after subtracting measured governance waste from global GDP.",
    display_name="Adjusted Realized Welfare",
    unit="USD",
    formula="GLOBAL_GDP_2025 - POLITICAL_DYSFUNCTION_GLOBAL_WASTE_TOTAL",
    inputs=["GLOBAL_GDP_2025", "POLITICAL_DYSFUNCTION_GLOBAL_WASTE_TOTAL"],
    compute=lambda ctx: (
        ctx["GLOBAL_GDP_2025"] - ctx["POLITICAL_DYSFUNCTION_GLOBAL_WASTE_TOTAL"]
    ),
    keywords=["welfare", "adjusted", "realized", "global"],
    latex_symbol=r"W_{real}",
)

POLITICAL_DYSFUNCTION_GLOBAL_THEORETICAL_MAX_WELFARE = Parameter(
    POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED + POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    confidence="low",
    description="Conservative theoretical maximum welfare under opportunity-cost recapture assumptions.",
    display_name="Theoretical Maximum Welfare (Conservative)",
    unit="USD",
    formula="POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED + POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL",
    inputs=["POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED", "POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"],
    compute=lambda ctx: (
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED"] +
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"]
    ),
    keywords=["welfare", "theoretical", "max", "global", "conservative"],
    latex_symbol=r"W_{max}",
)

POLITICAL_DYSFUNCTION_GLOBAL_EFFICIENCY_SCORE = Parameter(
    POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED /
    POLITICAL_DYSFUNCTION_GLOBAL_THEORETICAL_MAX_WELFARE,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="calculated",
    confidence="low",
    unit="percent",
    description="Global Governance Efficiency Score from Political Dysfunction Tax paper. "
                "E = Adjusted W_real / W_max, where W_real = GDP - waste, W_max = W_real + opportunity cost. "
                "Paper calculates 30-52% efficiency (using $110.9T adjusted / $211.9T maximum). "
                "This means civilization operates at roughly half its technological potential.",
    display_name="Global Governance Efficiency Score",
    formula="POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED / POLITICAL_DYSFUNCTION_GLOBAL_THEORETICAL_MAX_WELFARE",
    inputs=[
        "POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED",
        "POLITICAL_DYSFUNCTION_GLOBAL_THEORETICAL_MAX_WELFARE",
    ],
    compute=lambda ctx: (
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_REALIZED_WELFARE_ADJUSTED"] /
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_THEORETICAL_MAX_WELFARE"]
    ),
    keywords=["efficiency", "governance", "global", "score"],
    latex_symbol=r"E_{gov}",
)

# ---
# INTERNATIONAL GOVERNANCE EFFICIENCY COMPARISON
# ---
# Compare US outcomes to well-governed peer countries to estimate "dysfunction premium"
# Countries spending LESS as % of GDP achieve BETTER outcomes
# This provides independent evidence for the Political Dysfunction Tax

# US baseline for comparison
US_GOVT_SPENDING_PCT_GDP = Parameter(
    38.0,  # ~38% of GDP (federal + state + local)
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="oecd-govt-spending",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US total government spending as percentage of GDP (federal + state + local). "
                "OECD average is ~40%, but US gets worse outcomes for similar spending.",
    display_name="US Govt Spending (% GDP)",
    unit="percent",
    keywords=["government", "spending", "GDP", "US"],
    latex_symbol=r"G_{US}",
)

US_LIFE_EXPECTANCY_2023 = Parameter(
    77.5,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="cdc-life-expectancy",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US life expectancy at birth (2023). Lowest among high-income OECD countries "
                "despite highest healthcare spending.",
    display_name="US Life Expectancy",
    unit="years",
    keywords=["life expectancy", "US", "health", "outcomes"],
    latex_symbol=r"LE_{US}",
)

US_MEDIAN_HOUSEHOLD_INCOME_2023 = Parameter(
    80_610,  # $80,610 median household income 2023
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="census-income-2023",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US median household income (2023). High in absolute terms but adjusted for "
                "healthcare costs and inequality, purchasing power is lower than peers.",
    display_name="US Median Household Income",
    unit="USD",
    keywords=["income", "median", "household", "US"],
    latex_symbol=r"\bar{y}_{US}",
)

# SWITZERLAND - Lower spending, better outcomes
SWITZERLAND_GOVT_SPENDING_PCT_GDP = Parameter(
    35.0,  # ~35% of GDP
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="oecd-govt-spending",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Switzerland government spending as percentage of GDP. 3 percentage points LOWER "
                "than US (35% vs 38%) yet achieves dramatically better outcomes.",
    display_name="Switzerland Govt Spending (% GDP)",
    unit="percent",
    keywords=["government", "spending", "GDP", "Switzerland"],
    latex_symbol=r"G_{CH}",
)

SWITZERLAND_LIFE_EXPECTANCY = Parameter(
    84.0,
    manual_ref="knowledge/appendix/faq.qmd",
    source_ref="who-life-expectancy",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Switzerland life expectancy at birth. 6.5 years LONGER than US (84.0 vs 77.5) "
                "despite lower government spending as % of GDP.",
    display_name="Switzerland Life Expectancy",
    unit="years",
    keywords=["life expectancy", "Switzerland", "health", "outcomes"],
    latex_symbol=r"LE_{CH}",
)

SWITZERLAND_MEDIAN_INCOME_PPP = Parameter(
    65_000,  # ~$65K median income PPP
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="oecd-median-income",
    source_type="external",
    confidence="medium",
    distribution="fixed",
    description="Switzerland median household income (PPP-adjusted). Higher than US when "
                "adjusted for cost of healthcare and other expenses.",
    display_name="Switzerland Median Income (PPP)",
    unit="USD",
    keywords=["income", "median", "Switzerland"],
    latex_symbol=r"\bar{y}_{CH}",
)

# SINGAPORE - Much lower spending, excellent outcomes
SINGAPORE_GOVT_SPENDING_PCT_GDP = Parameter(
    15.0,  # ~15% of GDP - very lean government
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="imf-singapore-spending",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Singapore government spending as percentage of GDP. Less than HALF the US rate "
                "(15% vs 38%) yet achieves excellent outcomes through efficiency.",
    display_name="Singapore Govt Spending (% GDP)",
    unit="percent",
    keywords=["government", "spending", "GDP", "Singapore"],
    latex_symbol=r"G_{SG}",
)

SINGAPORE_LIFE_EXPECTANCY = Parameter(
    84.1,
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_ref="who-life-expectancy",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Singapore life expectancy at birth. 6.6 years LONGER than US (84.1 vs 77.5) "
                "despite government spending at less than half the rate.",
    display_name="Singapore Life Expectancy",
    unit="years",
    keywords=["life expectancy", "Singapore", "health", "outcomes"],
    latex_symbol=r"LE_{SG}",
)

SINGAPORE_GDP_PER_CAPITA_PPP = Parameter(
    105_000,  # ~$105K GDP per capita PPP
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="worldbank-singapore-gdp",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Singapore GDP per capita (PPP-adjusted). Among highest in world, "
                "demonstrating that lean government can coexist with prosperity.",
    display_name="Singapore GDP per Capita (PPP)",
    unit="USD",
    keywords=["GDP", "per capita", "Singapore"],
    latex_symbol=r"GDP_{pc,SG}",
)

# Comparison metrics: US vs international benchmarks
# These are definitions based on fixed government statistics (no uncertainty propagation needed)
US_VS_SWITZERLAND_LIFE_EXPECTANCY_GAP = Parameter(
    6.5,  # 84.0 - 77.5 = 6.5 years
    manual_ref="knowledge/solution/optimocracy.qmd",
    source_ref="who-life-expectancy",
    source_type="definition",
    confidence="high",
    distribution="fixed",
    description="Life expectancy gap: Switzerland vs US. Switzerland achieves 6.5 extra years "
                "of life while spending 3% LESS of GDP on government.",
    display_name="Switzerland-US Life Expectancy Gap",
    unit="years",
    formula="SWITZERLAND_LE - US_LE = 84.0 - 77.5",
    keywords=["life expectancy", "gap", "comparison"],
    latex_symbol=r"\Delta LE_{CH:US}",
)

US_VS_SWITZERLAND_SPENDING_GAP = Parameter(
    3.0,  # 38.0 - 35.0 = 3.0%
    manual_ref="knowledge/solution/optimocracy.qmd",
    source_ref="oecd-govt-spending",
    source_type="definition",
    confidence="high",
    distribution="fixed",
    description="Government spending gap: US spends 3 percentage points MORE of GDP than "
                "Switzerland yet achieves worse outcomes.",
    display_name="US-Switzerland Spending Gap",
    unit="percent",
    formula="US_SPENDING - SWITZERLAND_SPENDING = 38% - 35%",
    keywords=["spending", "gap", "comparison"],
    latex_symbol=r"\Delta G_{US:CH}",
)

US_VS_SINGAPORE_SPENDING_GAP = Parameter(
    23.0,  # 38.0 - 15.0 = 23.0%
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="oecd-govt-spending",
    source_type="definition",
    confidence="high",
    distribution="fixed",
    description="Government spending gap: US spends 23 percentage points MORE of GDP than "
                "Singapore yet achieves 6.6 fewer years of life expectancy.",
    display_name="US-Singapore Spending Gap",
    unit="percent",
    formula="US_SPENDING - SINGAPORE_SPENDING = 38% - 15%",
    keywords=["spending", "gap", "comparison", "Singapore"],
    latex_symbol=r"\Delta G_{US:SG}",
)

# Implied dysfunction premium: US spends more but gets worse outcomes
# If US achieved Swiss efficiency, same spending would yield better outcomes
# If US achieved Singapore efficiency, same outcomes could be achieved with 60% less spending
US_DYSFUNCTION_PREMIUM_VS_SWITZERLAND = Parameter(
    3.0,  # 3% of GDP more spending for worse outcomes (38% - 35%)
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_ref="oecd-govt-spending",
    source_type="definition",
    confidence="high",
    distribution="fixed",
    description="US 'dysfunction premium' vs Switzerland: US spends 3% more of GDP yet "
                "achieves 6.5 fewer years of life expectancy. This premium represents "
                "pure waste from governance inefficiency. Calculated as: 38% (US) - 35% (CH).",
    display_name="US Dysfunction Premium vs Switzerland",
    unit="percent",
    formula="US_GOVT_SPENDING_PCT_GDP - SWITZERLAND_GOVT_SPENDING_PCT_GDP",
    keywords=["dysfunction", "premium", "waste", "comparison"],
    latex_symbol=r"\tau_{US-CH}",
)

# ---
# POLITICAL CAPTURE COST ANALYSIS
# ---
# Source: knowledge/appendix/cost-of-change-analysis.qmd
# These parameters calculate the "worst case" cost to achieve political change through incentivization
# Used to answer the question: "If you think this is politically impossible, how much would it cost to MAKE it possible?"

# US Political System Costs
# Source: FEC 2024 Summary, OpenSecrets Lobbying Data, US Senate Treaties Guide
# These are estimates based on publicly available data

US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024 = Parameter(
    20_000_000_000,  # $20B total federal campaign spending 2024 cycle
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_ref=ReferenceID.FEC_2024_SUMMARY,
    source_type="external",
    description="Total US federal election spending in 2024 cycle including presidential, congressional, party committees, and PACs. Source: FEC Statistical Summary 2024.",
    display_name="US Federal Campaign Spending (2024)",
    unit="USD",
    confidence="high",
    confidence_interval=(18_000_000_000, 22_000_000_000),  # ±10% uncertainty
    keywords=["campaign", "election", "political", "spending", "federal", "2024"],
    latex_symbol=r"Cost_{US,campaign}",
)

US_TOTAL_LOBBYING_ANNUAL = Parameter(
    4_400_000_000,  # $4.4B record lobbying in 2024
    manual_ref="knowledge/appendix/algorithmic-public-administration-paper.qmd",
    source_ref=ReferenceID.OPENSECRETS_LOBBYING_2024,
    source_type="external",
    description="Total US federal lobbying expenditure in 2024 (record year). Source: OpenSecrets.",
    display_name="US Total Lobbying (2024)",
    unit="USD",
    confidence="high",
    confidence_interval=(3_740_000_000, 5_060_000_000),  # ±15% uncertainty
    keywords=["lobbying", "political", "spending", "k street", "influence"],
    latex_symbol=r"Cost_{US,lobby}",
)

US_CONGRESS_MEMBER_COUNT = Parameter(
    535,  # 100 senators + 435 representatives
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    source_ref="",
    source_type="definition",
    description="Total members of US Congress (100 senators + 435 representatives)",
    display_name="US Congress Members",
    unit="members",  # Reads naturally: "535 members" (not "535 count")
    confidence="high",
    distribution="fixed",  # Constitutional constant - no uncertainty
    keywords=["congress", "senator", "representative", "legislator"],
    latex_symbol=r"N_{congress}",
)

US_SENATORS_FOR_TREATY = Parameter(
    67,  # 2/3 majority required for treaty ratification
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_ref=ReferenceID.US_SENATE_TREATIES,
    source_type="external",
    description="Senators needed for treaty ratification (2/3 majority per Article II, Section 2)",
    display_name="Senators for Treaty Ratification",
    unit="senators",  # Reads naturally: "67 senators" (not "67 count")
    confidence="high",
    distribution="fixed",  # Constitutional constant - no uncertainty
    keywords=["senate", "treaty", "ratification", "two-thirds", "majority"],
    latex_symbol=r"N_{senators,treaty}",
)

POLITICIAN_POST_OFFICE_CAREER_VALUE = Parameter(
    10_000_000,  # ~$10M NPV of post-office career premium
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_ref=ReferenceID.OPENSECRETS_REVOLVING_DOOR,
    source_type="external",
    description="Net present value of post-office career premium for average congressperson (10 years x $1M/year premium). Based on documented cases: Gephardt $7M/year, Daschle $2M+/year.",
    display_name="Post-Office Career Value (per politician)",
    unit="USD",
    confidence="medium",
    confidence_interval=(5e6, 20e6),  # Wide range based on seniority/connections
    keywords=["revolving door", "lobbying", "post-office", "career", "salary"],
    latex_symbol=r"V_{post-office}",
)

# US Political Reform Investment Costs (calculated from components)
# These represent the cost of matching concentrated interests' political spending
# to enable diffuse beneficiaries to participate in the democratic process at scale
US_SENATE_TREATY_ADVOCACY_COST = Parameter(
    US_SENATORS_FOR_TREATY * POLITICIAN_POST_OFFICE_CAREER_VALUE,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Upper-bound advocacy cost to match career incentives for 67 senators (treaty ratification threshold)",
    display_name="US Senate Treaty Advocacy Cost",
    unit="USD",
    formula="SENATORS_FOR_TREATY x POST_OFFICE_VALUE",
    confidence="medium",
    keywords=["political reform", "advocacy", "senate", "treaty", "democratic participation"],
    inputs=["US_SENATORS_FOR_TREATY", "POLITICIAN_POST_OFFICE_CAREER_VALUE"],
    compute=lambda ctx: ctx["US_SENATORS_FOR_TREATY"] * ctx["POLITICIAN_POST_OFFICE_CAREER_VALUE"],
    latex_symbol=r"Cost_{US,senate}",
)

US_CONGRESS_FULL_ADVOCACY_COST = Parameter(
    US_CONGRESS_MEMBER_COUNT * POLITICIAN_POST_OFFICE_CAREER_VALUE,
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_type="calculated",
    description="Upper-bound advocacy cost to match career incentives for all 535 members of Congress",
    display_name="US Congress Full Advocacy Cost",
    unit="USD",
    formula="CONGRESS_MEMBERS x POST_OFFICE_VALUE",
    confidence="medium",
    keywords=["political reform", "advocacy", "congress", "democratic participation"],
    inputs=["US_CONGRESS_MEMBER_COUNT", "POLITICIAN_POST_OFFICE_CAREER_VALUE"],
    compute=lambda ctx: ctx["US_CONGRESS_MEMBER_COUNT"] * ctx["POLITICIAN_POST_OFFICE_CAREER_VALUE"],
    latex_symbol=r"Cost_{US,congress}",
)

# What fraction of total political spending (campaign + lobbying) do you need to match?
# <1 means partial matching is sufficient; >1 means you need to outspend incumbents
US_POLITICAL_EFFORT_MULTIPLIER = Parameter(
    0.7,
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_type="definition",
    description="Fraction of campaign + lobbying spending needed to achieve policy reform. Accounts for efficiency gains from coordination, message clarity, and public interest alignment. Range 0.4-1.2 reflects uncertainty about political dynamics.",
    display_name="Political Effort Multiplier (US)",
    unit="multiplier",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(0.4, 1.2),
    keywords=["political reform", "effort", "spending", "matching", "multiplier"],
    latex_symbol=r"\mu_{effort}",
)

# Base political spending = one election cycle of campaigns + 2 years of lobbying
_US_BASE_POLITICAL_SPENDING = float(US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024) + float(US_TOTAL_LOBBYING_ANNUAL) * 2

US_POLITICAL_REFORM_INVESTMENT_TOTAL = Parameter(
    _US_BASE_POLITICAL_SPENDING * float(US_POLITICAL_EFFORT_MULTIPLIER) + float(US_CONGRESS_FULL_ADVOCACY_COST),
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_type="calculated",
    description="Total upper-bound investment for US political reform: (campaign spending + 2 years lobbying) × effort multiplier + Congress career advocacy. Represents cost to achieve democratic parity with incumbent interests.",
    display_name="US Political Reform Investment (Total)",
    unit="USD",
    formula="(CAMPAIGN + LOBBYING×2) × EFFORT_MULTIPLIER + CONGRESS_CAREER",
    latex=r"Cost_{US,total} = (Cost_{campaign} + Cost_{lobby} \times 2) \times \mu_{effort} + Cost_{career}",
    confidence="low",
    keywords=["political reform", "advocacy", "investment", "democratic parity", "us"],
    inputs=["US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024", "US_TOTAL_LOBBYING_ANNUAL", "US_POLITICAL_EFFORT_MULTIPLIER", "US_CONGRESS_FULL_ADVOCACY_COST"],
    compute=lambda ctx: (ctx["US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024"] + ctx["US_TOTAL_LOBBYING_ANNUAL"] * 2) * ctx["US_POLITICAL_EFFORT_MULTIPLIER"] + ctx["US_CONGRESS_FULL_ADVOCACY_COST"],
    latex_symbol=r"Cost_{US,total}",
)

# Global Political Costs
NATO_DEFENSE_SPENDING_ANNUAL = Parameter(
    1_506_000_000_000,  # $1.506T NATO defense spending 2024
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_ref=ReferenceID.SIPRI2024,
    source_type="external",
    description="Total NATO member defense spending in 2024. Source: SIPRI.",
    display_name="NATO Defense Spending (2024)",
    unit="USD",
    confidence="high",
    keywords=["nato", "defense", "military", "spending", "alliance"],
    latex_symbol=r"Cost_{NATO,defense}",
)

# Ratio of global to US political reform costs
# Based on discretionary government spending: global ~$15T vs US ~$1.7T = ~9x
# Discounted ~50% because non-US political systems tend to be less transparent/expensive
GLOBAL_TO_US_POLITICAL_COST_RATIO = Parameter(
    5.0,
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_type="definition",
    description="Ratio of global to US political reform costs. Based on discretionary spending ratio (~9x) discounted by ~50% for less transparent/expensive non-US political systems. Range 3-8 reflects uncertainty about non-US political dynamics and hidden influence channels.",
    display_name="Global-to-US Political Cost Ratio",
    unit="ratio",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(3.0, 8.0),
    keywords=["political reform", "global", "ratio", "scaling", "international", "discretionary spending"],
    latex_symbol=r"\rho_{global/US}",
)

GLOBAL_POLITICAL_REFORM_INVESTMENT = Parameter(
    float(US_POLITICAL_REFORM_INVESTMENT_TOTAL) * float(GLOBAL_TO_US_POLITICAL_COST_RATIO),
    manual_ref="knowledge/appendix/cost-of-change-analysis.qmd",
    source_type="calculated",
    description="Estimated global advocacy investment for policy reform. Calculated as US costs × global ratio (based on discretionary spending). Upper bound representing full democratic engagement at scale.",
    display_name="Global Political Reform Investment",
    unit="USD",
    formula="US_POLITICAL_REFORM × GLOBAL_RATIO",
    confidence="low",
    keywords=["political reform", "advocacy", "global", "world", "democratic engagement"],
    inputs=["US_POLITICAL_REFORM_INVESTMENT_TOTAL", "GLOBAL_TO_US_POLITICAL_COST_RATIO"],
    compute=lambda ctx: ctx["US_POLITICAL_REFORM_INVESTMENT_TOTAL"] * ctx["GLOBAL_TO_US_POLITICAL_COST_RATIO"],
    latex_symbol=r"Cost_{global,reform}",
)

# Breakeven and ROI calculations at various political costs
# These show the intervention remains cost-effective even at extreme political costs

# ---
# VICTORY SOCIAL IMPACT BONDS
# ---

# VICTORY Incentive Alignment Bonds
# Source: knowledge/economics/victory-bonds.qmd
VICTORY_BOND_FUNDING_PCT = Parameter(
    0.10,
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_ref="",
    source_type="definition",
    description="Percentage of captured dividend funding VICTORY Incentive Alignment Bonds (10%)",
    display_name="Percentage of Captured Dividend Funding VICTORY Incentive Alignment Bonds",
    unit="rate",
    keywords=["10%", "social impact bond", "sib", "impact investing", "pay for success", "investor return", "development impact bond"],
    distribution="fixed",  # Policy choice: bond allocation percentage is a design decision
    latex_symbol=r"Pct_{bond}",  # LaTeX symbol for equations
)  # 10% of captured dividend funds bonds
VICTORY_BOND_ANNUAL_PAYOUT = Parameter(
    TREATY_ANNUAL_FUNDING * VICTORY_BOND_FUNDING_PCT,
    manual_ref="knowledge/economics/treaty-financial-plan.qmd",
    source_ref="",
    source_type="calculated",
    description="Annual VICTORY Incentive Alignment Bond payout (treaty funding × bond percentage)",
    display_name="Annual VICTORY Incentive Alignment Bond Payout",
    unit="USD/year",
    formula="TREATY_FUNDING × BOND_PCT",
    keywords=["social impact bond", "sib", "impact investing", "pay for success", "investor return", "development impact bond", "bcr"],
    inputs=['TREATY_ANNUAL_FUNDING', 'VICTORY_BOND_FUNDING_PCT'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] * ctx["VICTORY_BOND_FUNDING_PCT"],
    latex_symbol=r"Payout_{bond,ann}",  # LaTeX symbol for equations
)  # $2.718B
VICTORY_BOND_ANNUAL_RETURN_PCT = Parameter(
    VICTORY_BOND_ANNUAL_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST,
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_ref="",
    source_type="calculated",
    description="Annual return percentage for VICTORY Incentive Alignment Bondholders",
    display_name="Annual Return Percentage for VICTORY Incentive Alignment Bondholders",
    unit="rate",
    formula="PAYOUT ÷ CAMPAIGN_COST",
    keywords=["social impact bond", "sib", "impact investing", "pay for success", "investor return", "development impact bond", "bcr"],
    inputs=["VICTORY_BOND_ANNUAL_PAYOUT", "TREATY_CAMPAIGN_TOTAL_COST"],
    compute=lambda ctx: ctx["VICTORY_BOND_ANNUAL_PAYOUT"] / ctx["TREATY_CAMPAIGN_TOTAL_COST"],
    hide_ci=True,  # Suppress CI display - uncertainty is in campaign costs, not the ratio itself
    latex_symbol=r"r_{bond}",  # LaTeX symbol for equations
)  # 271.8% (reported as 270%)

# ---
# INCENTIVE ALIGNMENT BONDS (IABs)
# ---

# IAB mechanism funding for political incentives (PACs, fellowships, scoring infrastructure)
# Source: knowledge/solution/incentive-alignment-bonds.qmd
IAB_POLITICAL_INCENTIVE_FUNDING_PCT = Parameter(
    0.10,
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_ref="",
    source_type="definition",
    description="Percentage of treaty funding allocated to Incentive Alignment Bond mechanism for political incentives (independent expenditures/PACs, post-office fellowships, Public Good Score infrastructure)",
    display_name="IAB Political Incentive Funding Percentage",
    unit="rate",
    keywords=["10%", "incentive alignment bond", "iab", "political incentives", "pac", "fellowship", "scoring", "public good score"],
    distribution="fixed",  # Policy choice: IAB allocation percentage is a design decision
    latex_symbol=r"Pct_{political}",  # LaTeX symbol for equations
)  # 10% of treaty funding for political incentive mechanisms

IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL = Parameter(
    TREATY_ANNUAL_FUNDING * IAB_POLITICAL_INCENTIVE_FUNDING_PCT,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_ref="",
    source_type="calculated",  # Derived from treaty funding and IAB allocation percentage
    description="Annual funding for IAB political incentive mechanism (independent expenditures supporting high-scoring politicians, post-office fellowship endowments, Public Good Score infrastructure)",
    display_name="Annual IAB Political Incentive Funding",
    unit="USD/year",
    formula="TREATY_FUNDING × IAB_POLITICAL_INCENTIVE_PCT",    keywords=["incentive alignment bond", "iab", "political incentives", "pac", "fellowship", "scoring", "electoral", "public good score"],
    inputs=['TREATY_ANNUAL_FUNDING', 'IAB_POLITICAL_INCENTIVE_FUNDING_PCT'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] * ctx["IAB_POLITICAL_INCENTIVE_FUNDING_PCT"],
    latex_symbol=r"Funding_{political,ann}",  # LaTeX symbol for equations
)  # $2.718B/year for political incentive mechanisms

# ---
# TREATY EXPANSION RATCHET ECONOMICS
# ---
# Quantifies the expected value of the IAB ratchet mechanism:
# how much additional funding flows to medical research over 20 years
# if the treaty expands (due to bondholder lobbying) vs stagnates at 1%.
# Roadmap timeline modeled here (first 20 years):
#   1% (yr 1-3), 2% (yr 4-7), 5% (yr 8-12), 10% (yr 13-20)

# IAB political incentive funding vs defense industry lobbying at 1% treaty level
IAB_VS_DEFENSE_LOBBY_RATIO_AT_1PCT = Parameter(
    IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL / DEFENSE_LOBBYING_ANNUAL,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Ratio of IAB political incentive funding to defense industry lobbying at 1% treaty level. "
                "At just 1%, the health lobby already outguns the defense lobby by this factor.",
    display_name="IAB vs Defense Lobbying Ratio at 1% Treaty",
    unit="x",
    formula="IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL / DEFENSE_LOBBYING_ANNUAL",
    keywords=["ratchet", "lobbying", "defense", "political", "ratio", "incentive", "iab"],
    inputs=["IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL", "DEFENSE_LOBBYING_ANNUAL"],
    compute=lambda ctx: ctx["IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL"] / ctx["DEFENSE_LOBBYING_ANNUAL"],
    latex_symbol=r"k_{IAB:defense}",
)

# prize pool resolution horizon is tied to the destructive economy 50% threshold year
# (DESTRUCTIVE_ECONOMY_50PCT_YEAR). The pool resolves at the collapse deadline.
# Duration for compounding: _years_to_50pct (private var, currently 15 years).

# ── Global Capital Context ───────────────────────────────────────────────────

GLOBAL_SAVINGS_RATE_PCT = Parameter(
    0.27,
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_ref=ReferenceID.WORLD_BANK_GROSS_SAVINGS_2023,
    source_type="external",
    confidence="high",
    description="Global gross savings as share of GDP (World Bank, ~27% average 2023-2024)",
    display_name="Global Gross Savings Rate",
    unit="percent",
    keywords=["savings", "global", "GDP", "world bank"],
    confidence_interval=(0.24, 0.30),  # Historical range ~24-30% globally
    distribution="normal",
    latex_symbol=r"s_{global}",
)

GLOBAL_ANNUAL_SAVINGS = Parameter(
    GLOBAL_SAVINGS_RATE_PCT * GLOBAL_GDP_2025,
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Global annual savings in USD (savings rate × GDP)",
    display_name="Global Annual Savings",
    unit="USD",
    formula="GLOBAL_SAVINGS_RATE_PCT × GLOBAL_GDP_2025",
    inputs=["GLOBAL_SAVINGS_RATE_PCT", "GLOBAL_GDP_2025"],
    compute=lambda ctx: ctx["GLOBAL_SAVINGS_RATE_PCT"] * ctx["GLOBAL_GDP_2025"],
    keywords=["savings", "global", "annual", "capacity"],
    latex_symbol=r"S_{annual}",
)

# Moved here from IAB PAPER PARAMETERS section to keep wealth inputs available for downstream calculations
GLOBAL_HOUSEHOLD_WEALTH_USD = Parameter(
    454e12,
    manual_ref="knowledge/appendix/incentive-alignment-bonds-paper.qmd",
    source_ref=ReferenceID.CS_GLOBAL_WEALTH_REPORT_2023,
    source_type="external",
    confidence="high",
    description="Total global household wealth (2022/2023 estimate)",
    display_name="Global Household Wealth",
    unit="USD",
    keywords=["wealth", "household", "global", "assets", "capital"],
    distribution="fixed",
    latex_symbol=r"Wealth_{household}",  # LaTeX symbol for equations
)  # $454T

# ---
# THE RATCHET KNOB (single source for the treaty take-hold schedule)
# ---
# The IAB-ratchet schedule is 1% x 3y -> 2% x 4y -> 5% x 5y -> terminal thereafter.
# The terminal share is THE ratchet assumption, parameterized exactly once so that
# (a) every treaty-trajectory number binds the same knob, and (b) setting it to 0.01
# turns ratcheting OFF (the treaty stays at 1% forever) across the entire book in
# one edit. Intermediate steps degrade gracefully: years 4-7 use min(2%, terminal),
# years 8-12 use min(5%, terminal).

TREATY_RATCHET_TERMINAL_SHARE = Parameter(
    0.10,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="definition",
    description="Terminal share of military spending redirected under the IAB-ratchet take-hold "
                "schedule (1% for 3 years, 2% for 4, 5% for 5, terminal thereafter). The single "
                "ratchet knob: every treaty-trajectory parameter binds it, so setting it to 0.01 "
                "switches ratcheting off everywhere (the treaty stays at its initial 1% forever) "
                "and every treaty number degrades to its flat-1% bound. Uncertainty spans "
                "never-expands (0.01, the 95% lower bound) to overshooting the schedule (0.19): "
                "expansion is driven by bondholder lobbying incentives, which do not stop at 10% "
                "if they work at all.",
    display_name="Treaty Ratchet Terminal Redirect Share",
    unit="percent",
    confidence="low",
    distribution="normal",
    confidence_interval=(0.01, 0.19),
    keywords=["ratchet", "terminal", "treaty", "expansion", "schedule", "knob", "iab"],
    latex_symbol=r"s_{ratchet}",
)

_S_ratchet = float(TREATY_RATCHET_TERMINAL_SHARE)

# Cumulative treaty funding over 20 years WITH IAB ratchet expansion
TREATY_CUMULATIVE_20YR_WITH_RATCHET = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * (
        0.01 * 3                        # Years 1-3: 1%
        + min(0.02, _S_ratchet) * 4     # Years 4-7: 2%
        + min(0.05, _S_ratchet) * 5     # Years 8-12: 5%
        + _S_ratchet * 8                # Years 13-20: terminal
    ),
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Cumulative treaty funding over 20 years with IAB ratchet expansion following roadmap timeline. "
                "Expansion driven by bondholder lobbying incentives (10% of treaty inflows).",
    display_name="Cumulative Treaty Funding over 20 Years with IAB Ratchet Expansion",
    unit="USD",
    formula="GLOBAL_MILITARY × (0.01×3 + min(0.02, TREATY_RATCHET_TERMINAL_SHARE)×4 + min(0.05, TREATY_RATCHET_TERMINAL_SHARE)×5 + TREATY_RATCHET_TERMINAL_SHARE×8)",
    keywords=["cumulative", "20 year", "ratchet", "expansion", "dynamic", "iab", "roadmap"],
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "TREATY_RATCHET_TERMINAL_SHARE"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] * (
        0.01 * 3
        + min(0.02, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 4
        + min(0.05, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 5
        + ctx["TREATY_RATCHET_TERMINAL_SHARE"] * 8
    ),
    latex_symbol=r"Fund_{20yr,ratchet}",
)

# War costs on current trajectory (20 years at current levels)
WAR_COSTS_CUMULATIVE_20YR_CURRENT_TRAJECTORY = Parameter(
    GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST * 20,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Cumulative global war costs over 20 years if current spending levels continue. "
                "The price tag of the status quo trajectory.",
    display_name="Cumulative War Costs over 20 Years (Current Trajectory)",
    unit="USD",
    formula="GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST × 20",
    keywords=["war costs", "cumulative", "20 year", "current", "trajectory", "status quo"],
    inputs=["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] * 20,
    latex_symbol=r"Cost_{war,20yr}",
)

# War costs saved as treaty expands via IAB ratchet (same timeline as funding ratchet)
# Assumes war costs decline proportionally to military spending cuts (e=1.0)
WAR_COSTS_SAVED_PEACE_TRAJECTORY_20YR = Parameter(
    GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST * (
        0.01 * 3                        # Years 1-3: 1% reduction
        + min(0.02, _S_ratchet) * 4     # Years 4-7: 2% reduction
        + min(0.05, _S_ratchet) * 5     # Years 8-12: 5% reduction
        + _S_ratchet * 8                # Years 13-20: terminal
    ),
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Cumulative war costs saved over 20 years as treaty expands via IAB ratchet. "
                "Assumes war costs decline proportionally to spending cuts (e=1.0); "
                "Pape research suggests e>1.0 due to terrorism feedback loops, so the "
                "proportional assumption sits at the low end of the evidence.",
    display_name="War Costs Saved via Peace Trajectory (20yr)",
    unit="USD",
    formula="GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST × (0.01×3 + min(0.02, TREATY_RATCHET_TERMINAL_SHARE)×4 + min(0.05, TREATY_RATCHET_TERMINAL_SHARE)×5 + TREATY_RATCHET_TERMINAL_SHARE×8)",
    keywords=["war costs", "savings", "peace", "trajectory", "ratchet", "20 year", "moronia"],
    inputs=["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST", "TREATY_RATCHET_TERMINAL_SHARE"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] * (
        0.01 * 3
        + min(0.02, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 4
        + min(0.05, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 5
        + ctx["TREATY_RATCHET_TERMINAL_SHARE"] * 8
    ),
    latex_symbol=r"Savings_{war,20yr}",
)

# Total trajectory differential: research funding redirected + war externality costs saved
PEACE_TRAJECTORY_TOTAL_DIFFERENTIAL_20YR = Parameter(
    TREATY_CUMULATIVE_20YR_WITH_RATCHET + WAR_COSTS_SAVED_PEACE_TRAJECTORY_20YR,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Total 20-year value of the peace trajectory: research funding redirected to medicine "
                "plus war externality costs avoided. The full differential between the IAB trajectory "
                "and the current trajectory. Does not include existential risk reduction.",
    display_name="Peace Trajectory Total Differential (20yr)",
    unit="USD",
    formula="TREATY_CUMULATIVE_20YR_WITH_RATCHET + WAR_COSTS_SAVED_PEACE_TRAJECTORY_20YR",
    keywords=["peace", "trajectory", "total", "differential", "20 year", "moronia", "expected value"],
    inputs=["TREATY_CUMULATIVE_20YR_WITH_RATCHET", "WAR_COSTS_SAVED_PEACE_TRAJECTORY_20YR"],
    compute=lambda ctx: ctx["TREATY_CUMULATIVE_20YR_WITH_RATCHET"] + ctx["WAR_COSTS_SAVED_PEACE_TRAJECTORY_20YR"],
    latex_symbol=r"V_{peace,20yr}",
)

# ---
# FUNDING ALLOCATION (Updated to include IAB)
# ---

DIVIDEND_COVERAGE_FACTOR = Parameter(
    TREATY_ANNUAL_FUNDING / DFDA_ANNUAL_OPEX,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Coverage factor of treaty funding vs pragmatic trial platform opex (sustainability margin)",
    display_name="Coverage Factor of Treaty Funding vs Pragmatic Trial Platform OPEX",
    unit="ratio",
    formula="TREATY_FUNDING ÷ TRIAL_PLATFORM_OPEX",    keywords=["pragmatic trials", "real world evidence", "multiple", "decentralized trials", "drug agency", "food and drug administration", "international agreement"],
    inputs=['DFDA_ANNUAL_OPEX', 'TREATY_ANNUAL_FUNDING'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] / ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"k_{coverage}",  # LaTeX symbol for equations
)  # ~679x
DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL = Parameter(
    TREATY_ANNUAL_FUNDING - VICTORY_BOND_ANNUAL_PAYOUT - IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="",
    source_type="calculated",  # Derived from treaty funding minus bond and IAB allocations
    description="Annual 1% Treaty funding available for pragmatic clinical trials after bond payouts and political incentive funding.",
    display_name="1% Treaty Pragmatic Trial Funding",
    unit="USD/year",
    formula="TREATY_FUNDING - BOND_PAYOUT - IAB_POLITICAL_INCENTIVE_FUNDING",
    keywords=["impact investing", "pay for success", "distributed research", "global research", "open science", "debt instrument", "development finance"],
    inputs=['TREATY_ANNUAL_FUNDING', 'VICTORY_BOND_ANNUAL_PAYOUT', 'IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] - ctx["VICTORY_BOND_ANNUAL_PAYOUT"] - ctx["IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL"],
    latex_symbol=r"Treasury_{RD,ann}",  # LaTeX symbol for equations
)  # $21.744B/year (80% of treaty funding)
DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL = Parameter(
    DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL - DFDA_ANNUAL_OPEX,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Annual 1% Treaty patient-level pragmatic trial subsidies after platform operating costs",
    display_name="1% Treaty Annual Trial Subsidies",
    unit="USD/year",
    formula="ONE_PERCENT_TREATY_TRIAL_FUNDING - TRIAL_PLATFORM_OPEX",    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "rct", "patient subsidy"],
    inputs=['DFDA_ANNUAL_OPEX', 'DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL'],
    compute=lambda ctx: ctx["DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL"] - ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"Subsidies_{trial,ann}",  # LaTeX symbol for equations
)  # $24.422B/year - ALL remaining funds go to subsidizing patient trial participation

DIH_PATIENTS_FUNDABLE_ANNUALLY = Parameter(
    DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Number of patients fundable annually from 1% Treaty pragmatic trial subsidies at empirical pragmatic trial cost (RECOVERY to PCORnet range).",
    display_name="Patients Fundable Annually Under the 1% Treaty",
    unit="patients/year",
    formula="ONE_PERCENT_TREATY_TRIAL_SUBSIDIES ÷ PRAGMATIC_TRIAL_COST_PER_PATIENT",    keywords=["trial", "participant", "enrollment", "capacity", "patient"],
    inputs=['DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    latex_symbol=r"N_{fundable,ann}",  # LaTeX symbol for equations
)

# Funding allocation percentages (calculated from absolute values)
DIH_TREASURY_MEDICAL_RESEARCH_PCT = Parameter(
    DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL / TREATY_ANNUAL_FUNDING,
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_type="calculated",
    description="Percentage of treaty funding allocated to medical research (after bond payouts and IAB incentives)",
    display_name="Medical Research Percentage of Treaty Funding",
    unit="rate",
    formula="MEDICAL_RESEARCH_FUNDING / TREATY_FUNDING",
    confidence="high",
    keywords=["allocation", "percentage", "medical research", "funding"],
    inputs=["DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL", "TREATY_ANNUAL_FUNDING"],
    compute=lambda ctx: ctx["DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL"] / ctx["TREATY_ANNUAL_FUNDING"],
    latex_symbol=r"Pct_{treasury,RD}",  # LaTeX symbol for equations
)  # 80%

DIH_TREASURY_TRIAL_SUBSIDIES_PCT = Parameter(
    DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL / TREATY_ANNUAL_FUNDING,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Percentage of treaty funding going directly to patient trial subsidies",
    display_name="Patient Trial Subsidies Percentage of Treaty Funding",
    unit="rate",
    formula="TRIAL_SUBSIDIES / TREATY_FUNDING",
    confidence="high",
    keywords=["allocation", "percentage", "patient", "trial", "subsidy"],
    inputs=["DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL", "TREATY_ANNUAL_FUNDING"],
    compute=lambda ctx: ctx["DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL"] / ctx["TREATY_ANNUAL_FUNDING"],
    latex_symbol=r"Pct_{subsidies}",  # LaTeX symbol for equations
)  # 79.85%

DFDA_OPEX_PCT_OF_TREATY_FUNDING = Parameter(
    DFDA_ANNUAL_OPEX / TREATY_ANNUAL_FUNDING,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Percentage of treaty funding allocated to pragmatic trial platform overhead",
    display_name="Pragmatic Trial Platform Overhead Percentage of Treaty Funding",
    unit="rate",
    formula="TRIAL_PLATFORM_OPEX / TREATY_FUNDING",
    confidence="high",
    keywords=["allocation", "percentage", "overhead", "platform", "opex"],
    inputs=["DFDA_ANNUAL_OPEX", "TREATY_ANNUAL_FUNDING"],
    compute=lambda ctx: ctx["DFDA_ANNUAL_OPEX"] / ctx["TREATY_ANNUAL_FUNDING"],
    latex_symbol=r"OPEX_{pct}",  # LaTeX symbol for equations
)  # 0.15%

SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL = Parameter(
    10,
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    source_ref=ReferenceID.SUGAR_SUBSIDIES_COST,
    source_type="external",
    description="Annual cost of sugar subsidies per person",
    display_name="Annual Cost of Sugar Subsidies per Person",
    unit="USD/person/year",
    keywords=["average person", "yearly", "costs", "funding", "investment", "household benefit", "typical individual"],
    latex_symbol=r"Cost_{sugar,pc}",  # LaTeX symbol for equations
)  # $10 per person per year in sugar subsidies

GLOBAL_MED_RESEARCH_SPENDING = Parameter(
    67_500_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GLOBAL_GOV_MED_RESEARCH_SPENDING,
    source_type="external",
    description="Global government medical research spending",
    display_name="Global Government Medical Research Spending",
    unit="USD",
    keywords=["67.5b", "worldwide", "investigation", "r&d", "science", "study", "costs"],
    distribution="lognormal",
    confidence_interval=(54_000_000_000, 81_000_000_000),  # ±20% - government spending estimates vary
    latex_symbol=r"Spending_{RD}",  # LaTeX symbol for equations
)

TOTAL_RESEARCH_FUNDING_WITH_TREATY = Parameter(
    GLOBAL_MED_RESEARCH_SPENDING + TREATY_ANNUAL_FUNDING,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total global research funding (baseline + 1% treaty funding)",
    display_name="Total Global Research Funding (Baseline + 1% treaty Funding)",
    unit="USD",
    formula="GLOBAL_MED_RESEARCH_SPENDING + TREATY_ANNUAL_FUNDING",
    keywords=["research", "funding", "total", "dih", "treaty"],
    inputs=['GLOBAL_MED_RESEARCH_SPENDING', 'TREATY_ANNUAL_FUNDING'],
    compute=lambda ctx: ctx["GLOBAL_MED_RESEARCH_SPENDING"] + ctx["TREATY_ANNUAL_FUNDING"],
    latex_symbol=r"Funding_{RD,total}",  # LaTeX symbol for equations
)

# Trial Capacity Multiplier (Simple Economic Calculation)
# Treaty-scale reference funding can support ~23.4M patients/year at pragmatic trial cost ($929/patient)
# Current global trial capacity: 1.9M patients/year (IQVIA 2022)
# Capacity Multiplier = treaty-scale pragmatic trial capacity / current capacity
DFDA_TRIAL_CAPACITY_MULTIPLIER = Parameter(
    DFDA_PATIENTS_FUNDABLE_ANNUALLY / CURRENT_TRIAL_SLOTS_AVAILABLE,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Trial capacity multiplier from treaty-scale pragmatic trial funding capacity vs. current global trial participation",
    display_name="Pragmatic Trial Capacity Multiplier at Treaty-Scale Funding",
    unit="x",
    formula="PATIENTS_FUNDABLE_AT_REFERENCE_FUNDING ÷ CURRENT_TRIAL_SLOTS",
    keywords=["pragmatic trials", "real world evidence", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "multiple"],
    inputs=['CURRENT_TRIAL_SLOTS_AVAILABLE', 'DFDA_PATIENTS_FUNDABLE_ANNUALLY'],
    compute=lambda ctx: ctx["DFDA_PATIENTS_FUNDABLE_ANNUALLY"] / ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"],
    latex_symbol=r"k_{capacity}",  # LaTeX symbol for equations
)  # Trial capacity multiplier from simple funding economics (reference patients fundable / current trial slots)

TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR = Parameter(
    float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * 20,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Cumulative trial-capacity-equivalent years over 20-year period",
    display_name="Cumulative Trial Capacity Years Over 20 Years",
    unit="years",
    formula="PRAGMATIC_TRIAL_CAPACITY_MULTIPLIER × 20 YEARS",
    keywords=["trial", "capacity", "cumulative", "20 years"],
    inputs=['DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * 20,
    latex_symbol=r"Capacity_{20yr}",  # LaTeX symbol for equations
)  # Auto-generated LaTeX from calculated value

# ==============================================================================
# CURE TIMELINE ACCELERATION PARAMETERS
# ==============================================================================
# These parameters model how increased trial capacity and cost elimination
# accelerate the timeline for discovering and approving cures.
#
# Two mechanisms:
# 1. PARALLEL SEARCH: Higher trial capacity means testing more candidates
#    simultaneously, compressing discovery timelines
# 2. COST BARRIER REMOVAL: Eliminating Phase 2/3 costs enables more drugs
#    to enter development (valley of death elimination)
# ==============================================================================

# Clinical Trial Phase Cost Breakdown
# Source: Global clinical trials market ~$60B annually
# Phase 2: ~$15-25B (24%), Phase 3: ~$29-45B (45%), combined ~69%
PHASE_2_3_CLINICAL_TRIAL_COST_PCT = Parameter(
    0.69,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GLOBAL_CLINICAL_TRIALS_MARKET_2024,
    source_type="external",
    description="Percentage of total clinical trial spending on Phase 2/3 efficacy testing (Phase 2: 24% + Phase 3: 45%)",
    display_name="Phase 2/3 Share of Clinical Trial Costs",
    unit="percentage",
    confidence="high",
    keywords=["phase 2", "phase 3", "efficacy", "cost", "clinical trials", "breakdown"],
    distribution="normal",
    std_error=0.05,  # ±7% uncertainty in cost allocation estimates
    latex_symbol=r"Pct_{P2+P3}",  # LaTeX symbol for equations
)  # 69% of trial costs are Phase 2/3 efficacy testing

# Cost barrier pharma faces for Phase 2/3 (per drug)
# Current drug development: $2.6B (PHARMA_DRUG_DEVELOPMENT_COST_CURRENT), ~60% is Phase 2/3/4 efficacy testing
PHARMA_PHASE_2_3_COST_BARRIER = Parameter(
    1_560_000_000,  # $2.6B × 60% = $1.56B
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.DRUG_DEVELOPMENT_COST,
    source_type="definition",  # Model estimate: 60% of $2.6B total drug dev cost
    description="Average Phase 2/3 efficacy testing cost per drug that pharma must fund (~60% of total drug development cost)",
    display_name="Pharma Phase 2/3 Cost Barrier Per Drug",
    unit="USD",
    confidence="high",
    keywords=["phase 2", "phase 3", "cost", "barrier", "pharma", "drug development"],
    distribution="normal",
    std_error=200_000_000,  # ±$200M uncertainty in cost allocation
    latex_symbol=r"Cost_{P2+P3}",  # LaTeX symbol for equations
)  # $1.56B cost barrier per drug for Phase 2/3 testing

# ===== CUMULATIVE EFFICACY TESTING COST SINCE 1962 =====
# Uses Phase 2/3 cost directly - what we KNOW is spent on efficacy testing.
# This is a lower bound: excludes opportunity cost of delay, abandoned compounds,
# regulatory overhead, etc. Pre-1962 system had efficacy monitoring via AMA
# doctors and JAMA - the cost is from switching to pre-market RCTs.

DRUGS_APPROVED_SINCE_1962 = Parameter(
    CURRENT_DRUG_APPROVALS_PER_YEAR * 62,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.GLOBAL_NEW_DRUG_APPROVALS_50_ANNUALLY,
    source_type="calculated",
    description="Estimated total drugs approved globally since 1962 (62 years × average approval rate). Conservative: uses current rate, actual historical rate was lower in 1960s-80s.",
    display_name="Total Drugs Approved Since 1962",
    unit="drugs",
    confidence="medium",
    keywords=["drugs", "approved", "1962", "total", "fda", "history"],
    formula="APPROVALS_PER_YEAR × 62",
    inputs=["CURRENT_DRUG_APPROVALS_PER_YEAR"],
    compute=lambda ctx: ctx["CURRENT_DRUG_APPROVALS_PER_YEAR"] * 62,
    latex_symbol=r"N_{drugs,62}",
)  # ~3,100 drugs

EFFICACY_LAG_CUMULATIVE_EXCESS_COST = Parameter(
    PHARMA_PHASE_2_3_COST_BARRIER * DRUGS_APPROVED_SINCE_1962,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Cumulative Phase 2/3 efficacy testing cost since 1962. Uses direct Phase 2/3 cost per drug - this is a LOWER BOUND because it excludes opportunity cost of delays, compounds abandoned due to cost barrier, and regulatory overhead.",
    display_name="Cumulative Efficacy Testing Cost (1962-2024)",
    unit="USD",
    confidence="medium",
    keywords=["cumulative", "efficacy", "cost", "1962", "total", "drug", "development", "trillion", "phase 2", "phase 3"],
    formula="PHASE_2_3_COST × DRUGS_APPROVED",
    inputs=["PHARMA_PHASE_2_3_COST_BARRIER", "DRUGS_APPROVED_SINCE_1962"],
    compute=lambda ctx: ctx["PHARMA_PHASE_2_3_COST_BARRIER"] * ctx["DRUGS_APPROVED_SINCE_1962"],
    latex_symbol=r"Cost_{eff,cumul}",
)  # ~$4.8 trillion (lower bound - excludes knock-on effects)

# ===== 9/11 EQUIVALENTS FOR SCALE =====
# To make mortality figures viscerally understandable

SEPT_11_DEATHS = Parameter(
    2977,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref="september-11-memorial",  # National September 11 Memorial & Museum
    source_type="external",
    description="Total deaths in the September 11, 2001 attacks. 2,977 victims (excluding 19 hijackers). Used as a reference point for scale comparisons.",
    display_name="September 11 Deaths",
    unit="people",
    confidence="high",
    keywords=["9/11", "september 11", "deaths", "terrorism", "scale", "reference"],
    distribution="fixed",  # Historical fact - no uncertainty
    latex_symbol=r"N_{9/11}",
)  # 2,977 people

EFFICACY_LAG_DEATHS_911_EQUIVALENTS = Parameter(
    EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL / SEPT_11_DEATHS,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_type="calculated",
    description="Total deaths from efficacy lag expressed in 9/11 equivalents. Makes the mortality cost viscerally understandable: how many September 11ths worth of deaths did the 1962 efficacy requirements cause?",
    display_name="Efficacy Lag Deaths (9/11 Equivalents)",
    unit="9/11s",
    confidence="medium",
    keywords=["9/11", "equivalents", "scale", "deaths", "efficacy lag", "comparison"],
    formula="EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL ÷ SEPT_11_DEATHS",
    inputs=["EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL", "SEPT_11_DEATHS"],
    compute=lambda ctx: ctx["EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL"] / ctx["SEPT_11_DEATHS"],
    latex_symbol=r"N_{9/11,equiv}",
)  # ~34,000 9/11s

# Valley of Death: Percentage of Phase 1-passed compounds abandoned due to Phase 2/3 costs
# Evidence: Only 12 drugs/year approved from 7,500+ Phase 1-passed compounds
# ~99.8% attrition, but not all due to cost - maybe 30-50% could succeed if funded
VALLEY_OF_DEATH_ATTRITION_PCT = Parameter(
    0.40,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.VALLEY_OF_DEATH_ATTRITION,
    source_type="external",
    description="Percentage of promising Phase 1-passed compounds abandoned primarily due to Phase 2/3 cost barriers (not scientific failure). Conservative estimate: many rare disease, natural compound, and low-margin drugs never tested.",
    display_name="Valley of Death Attrition Rate",
    unit="percentage",
    confidence="medium",
    keywords=["valley of death", "attrition", "abandoned", "cost barrier", "phase 2", "phase 3"],
    distribution="uniform",
    confidence_interval=(0.25, 0.55),  # Wide range: 25-55% abandoned due to cost
    latex_symbol=r"Attrition_{valley}",  # LaTeX symbol for equations
)  # ~40% of Phase 1-passed compounds abandoned due to cost (not science)

# ==============================================================================
# SIMPLIFIED CURE ACCELERATION MODEL
# ==============================================================================
# Simple model: Speedup factor × baseline time = acceleration
#
# Speedup from two sources (multiplicative):
# 1. Trial capacity multiplier - test more compounds in parallel
# 2. Cost barrier rescue factor (~1.4×) - valley of death elimination
#
# Combined speedup = Trial capacity × Cost barrier rescue
# Acceleration = Baseline × (1 - 1/Speedup)
#
# With higher speedup, cures that would take T years now take T/speedup.
# Acceleration ≈ T × (1 - 1/speedup) (you get most of the baseline time back).
#
# Uncertainty is primarily in the BASELINE estimate:
# - Well-funded diseases: maybe 30-50 years to cure
# - Underfunded/rare diseases: could be 200-500+ years (or never)
# - Average across ALL diseases (including neglected 90%): wide range
# ==============================================================================

# Additional drug approvals when Phase 2/3 cost barrier eliminated
# Conservative: 40% of abandoned compounds could succeed = 40% more drugs
# 50 drugs/year × 40% valley-of-death compounds = 20 additional drugs/year
ADDITIONAL_DRUGS_FROM_COST_ELIMINATION = Parameter(
    float(CURRENT_DRUG_APPROVALS_PER_YEAR) * float(VALLEY_OF_DEATH_ATTRITION_PCT),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Additional drug approvals per year when Phase 2/3 cost barrier eliminated. Assumes valley-of-death compounds (abandoned due to cost) would have similar success rate to funded compounds.",
    display_name="Additional Drug Approvals from Cost Elimination",
    unit="drugs/year",
    formula="CURRENT_APPROVALS × VALLEY_OF_DEATH_PCT",    confidence="medium",
    keywords=["additional", "drugs", "cost", "elimination", "valley of death"],
    inputs=['CURRENT_DRUG_APPROVALS_PER_YEAR', 'VALLEY_OF_DEATH_ATTRITION_PCT'],
    compute=lambda ctx: ctx["CURRENT_DRUG_APPROVALS_PER_YEAR"] * ctx["VALLEY_OF_DEATH_ATTRITION_PCT"],
    latex_symbol=r"Drugs_{new}",  # LaTeX symbol for equations
)  # ~20 additional drugs/year from eliminating cost barrier

# Valley of death rescue multiplier: eliminating Phase 2/3 costs rescues abandoned drugs
# 40% more drugs enter development when cost barrier removed
DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER = Parameter(
    1 + float(VALLEY_OF_DEATH_ATTRITION_PCT),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Factor increase in drugs entering development when pragmatic trial subsidies remove the Phase 2/3 cost barrier. Valley-of-death attrition (40%) becomes new drugs, so 1 + 0.40 = 1.4× more drugs.",
    display_name="Valley of Death Rescue Multiplier",
    unit="multiplier",
    formula="1 + VALLEY_OF_DEATH_ATTRITION_PCT",    confidence="medium",
    keywords=["pragmatic trials", "valley of death", "rescue", "multiplier", "cost barrier"],
    inputs=['VALLEY_OF_DEATH_ATTRITION_PCT'],
    compute=lambda ctx: 1 + ctx["VALLEY_OF_DEATH_ATTRITION_PCT"],
    latex_symbol=r"k_{rescue}",  # LaTeX symbol for equations
)  # 1.4x more drugs when pragmatic trial subsidies eliminate the cost barrier

# Combined treatment discovery speedup from pragmatic trial expansion
# Trial capacity multiplier × valley of death rescue multiplier
DFDA_COMBINED_TREATMENT_SPEEDUP_MULTIPLIER = Parameter(
    float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * float(DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Combined speedup factor for treatment discovery from pragmatic trial expansion. Trial capacity multiplier times valley of death rescue multiplier. Diseases that would take T years to get first treatment now take T/speedup years.",
    display_name="Combined Treatment Discovery Speedup Multiplier",
    unit="multiplier",
    formula="PRAGMATIC_TRIAL_CAPACITY_MULTIPLIER × VALLEY_OF_DEATH_RESCUE_MULTIPLIER",
    confidence="medium",
    keywords=["pragmatic trials", "treatment", "speedup", "combined", "multiplier"],
    inputs=['DFDA_TRIAL_CAPACITY_MULTIPLIER', 'DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * ctx["DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER"],
    latex_symbol=r"k_{speedup}",  # LaTeX symbol for equations
)  # Auto-generated LaTeX from calculated value

# Rare diseases (moved here to enable calculated parameters below)
RARE_DISEASES_COUNT_GLOBAL = Parameter(
    7000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.N95_PCT_DISEASES_NO_TREATMENT,
    source_type="external",
    description="Total number of rare diseases globally",
    display_name="Total Number of Rare Diseases Globally",
    unit="diseases",
    keywords=["7k", "worldwide", "illness", "rare", "diseases", "count", "international"],
    distribution="normal",
    confidence_interval=(6000, 10000),  # Could be 6K-10K depending on definitions
    latex_symbol=r"N_{rare}",  # LaTeX symbol for equations
)  # ~7,000 rare diseases

# Diseases without effective treatment (queue size for curing all diseases)
# 95% of ~7,000 rare diseases have no treatment
DISEASES_WITHOUT_EFFECTIVE_TREATMENT = Parameter(
    float(RARE_DISEASES_COUNT_GLOBAL) * 0.95,  # ~6,650 diseases
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.RARE_DISEASE_ONLY_5PCT_HAVE_TREATMENT,
    source_type="calculated",
    description="Number of diseases without effective treatment. 95% of 7,000 rare diseases lack FDA-approved treatment (per Orphanet 2024). This represents the therapeutic search space that remains unexplored.",
    display_name="Diseases Without Effective Treatment",
    unit="diseases",
    formula="RARE_DISEASES_COUNT_GLOBAL × 0.95",    confidence="medium",
    keywords=["diseases", "untreatable", "no treatment", "queue", "rare diseases"],
    inputs=['RARE_DISEASES_COUNT_GLOBAL'],
    compute=lambda ctx: ctx["RARE_DISEASES_COUNT_GLOBAL"] * 0.95,
    latex_symbol=r"N_{untreated}",  # LaTeX symbol for equations
)  # ~6,650 diseases (uncertainty propagated from RARE_DISEASES_COUNT_GLOBAL)

# Diseases getting FIRST effective treatment per year under status quo
# ~9 rare diseases/year (350 over 40 years of ODA) + ~5-10 common diseases
NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR = Parameter(
    15,  # Central estimate: ~15 diseases/year get FIRST treatment
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.DISEASES_GETTING_FIRST_TREATMENT_ANNUALLY,
    source_type="external",
    description="Number of diseases that receive their FIRST effective treatment each year under current system. ~9 rare diseases/year (based on 40 years of ODA: 350 with treatment ÷ 40 years), plus ~5-10 common diseases. Note: FDA approves ~50 drugs/year, but most are for diseases that already have treatments.",
    display_name="Diseases Getting First Treatment Per Year",
    unit="diseases/year",
    confidence="low",
    keywords=["first treatment", "new cures", "diseases per year", "status quo", "rate"],
    distribution="lognormal",
    confidence_interval=(8.0, 30.0),  # Narrowed from (5, 40) to keep queue times reasonable:
                                       # - Floor (8/yr): Strict definition → ~830yr queue max
                                       # - Ceiling (30/yr): Liberal definition → ~220yr queue min
                                       # Prevents extreme 1000+ year scenarios that strain credibility
    latex_symbol=r"Treatments_{new,ann}",  # LaTeX symbol for equations
)  # ~15 diseases/year get FIRST treatment

# Time to explore entire therapeutic search space under status quo
# ~6,650 diseases ÷ ~15 cures/year = ~443 years to find treatments for ALL diseases
STATUS_QUO_QUEUE_CLEARANCE_YEARS = Parameter(
    float(DISEASES_WITHOUT_EFFECTIVE_TREATMENT) / float(NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.STATUS_QUO_CURE_TIMELINE_ESTIMATE,
    source_type="calculated",
    description="Years to explore the entire therapeutic search space under current system. At current discovery rate of ~15 diseases/year getting first treatments, finding treatments for all ~6,650 untreated diseases would take ~443 years.",
    display_name="Status Quo Therapeutic Space Exploration Time",
    unit="years",
    formula="DISEASES_WITHOUT_EFFECTIVE_TREATMENT ÷ NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR",    confidence="low",
    keywords=["status quo", "queue", "clearance", "total", "years"],
    inputs=['DISEASES_WITHOUT_EFFECTIVE_TREATMENT', 'NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR'],
    compute=lambda ctx: ctx["DISEASES_WITHOUT_EFFECTIVE_TREATMENT"] / ctx["NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR"],
    latex_symbol=r"T_{queue,SQ}",  # LaTeX symbol for equations
)  # ~443 years to cure ALL diseases

# Average time to first treatment under current/status quo system (BASELINE)
# Average disease is in middle of the therapeutic space, so waits half the exploration time
# ~443 years ÷ 2 = ~222 years for the average disease
STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT = Parameter(
    float(STATUS_QUO_QUEUE_CLEARANCE_YEARS) / 2,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.STATUS_QUO_CURE_TIMELINE_ESTIMATE,
    source_type="calculated",
    description="Average years until first treatment discovered for a typical disease under current system. At current discovery rates, the average disease waits half the total exploration time (~443/2 = ~222 years).",
    display_name="Status Quo Average Years to First Treatment",
    unit="years",
    formula="STATUS_QUO_QUEUE_CLEARANCE_YEARS ÷ 2",    confidence="low",
    keywords=["status quo", "current system", "average", "time", "first treatment", "years", "baseline"],
    inputs=['STATUS_QUO_QUEUE_CLEARANCE_YEARS'],
    compute=lambda ctx: ctx["STATUS_QUO_QUEUE_CLEARANCE_YEARS"] / 2,
    latex_symbol=r"T_{first,SQ}",  # LaTeX symbol for equations
)  # ~222 years for average disease (half the exploration time)

# Treatment timeline acceleration from pragmatic trial expansion (trial capacity only)
# Calculated as: Status Quo Baseline × (1 - 1/Speedup)
# Uses only trial capacity multiplier, not combined with valley of death rescue,
# because valley of death rescue adds more drug candidates but doesn't directly speed therapeutic space exploration
DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS = Parameter(
    float(STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT) * (1 - 1 / float(DFDA_TRIAL_CAPACITY_MULTIPLIER)),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Years earlier the average first treatment arrives due to increased pragmatic trial capacity. Calculated as the status quo timeline reduced by the inverse of the capacity multiplier. Uses only trial capacity multiplier (not combined with valley of death rescue) because additional candidates do not directly speed therapeutic space exploration.",
    display_name="Treatment Timeline Acceleration from Pragmatic Trial Capacity",
    unit="years",
    formula="STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT × (1 - 1/PRAGMATIC_TRIAL_CAPACITY_MULTIPLIER)",
    confidence="low",
    keywords=["pragmatic trials", "acceleration", "first treatment", "timeline", "years"],
    inputs=['STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT', 'DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT"] * (1 - 1 / ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"]),
    latex_symbol=r"T_{accel}",  # LaTeX symbol for equations
)

# ============================================================================
# TRIAL CAPACITY BENEFITS (treatment acceleration from trial capacity alone)
# ============================================================================
# These parameters capture the benefits from increased trial capacity ALONE,
# separate from efficacy lag elimination. The trial capacity increase allows
# more diseases to receive first treatments simultaneously, reducing the average wait time.

DFDA_TRIAL_CAPACITY_LIVES_SAVED = Parameter(
    float(GLOBAL_DISEASE_DEATHS_DAILY) * float(DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS) * DAYS_PER_YEAR * (1 - _unavoidable_pct),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total eventually avoidable deaths from trial capacity increase alone. Represents first treatments arriving earlier due to faster therapeutic space exploration from increased trial capacity.",
    display_name="Lives Saved from Trial Capacity Increase",
    unit="deaths",
    formula="ANNUAL_DEATHS × TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS × AVOIDABLE_PCT",
    confidence="low",
    keywords=["trial capacity", "lives saved", "treatment acceleration"],
    inputs=['GLOBAL_DISEASE_DEATHS_DAILY', 'DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS'],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DEATHS_DAILY"] * ctx["DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS"] * DAYS_PER_YEAR * (1 - _unavoidable_pct),
    latex_symbol=r"Lives_{capacity}",  # LaTeX symbol for equations
)

# DALYs averted from trial capacity increase
# Using same DALY multiplier as efficacy lag calculation
# Define DALY multiplier here (ratio of DALYs to deaths from efficacy lag data)
_daly_multiplier_from_deaths = float(DFDA_EFFICACY_LAG_ELIMINATION_DALYS) / float(DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED)

# Define YLD ratio for calculating suffering hours from complete scenario DALYs
_yld_ratio_of_dalys = float(DFDA_EFFICACY_LAG_ELIMINATION_YLD) / float(DFDA_EFFICACY_LAG_ELIMINATION_DALYS)

DFDA_TRIAL_CAPACITY_DALYS_AVERTED = Parameter(
    float(GLOBAL_ANNUAL_DALY_BURDEN) * float(EVENTUALLY_AVOIDABLE_DALY_PCT) * float(DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total DALYs averted from trial capacity increase alone. Calculated as annual global DALY burden × eventually avoidable percentage × treatment acceleration years. Includes both fatal and non-fatal diseases.",
    display_name="DALYs Averted from Trial Capacity Increase",
    unit="DALYs",
    formula="GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT × TREATMENT_ACCELERATION_YEARS",
    confidence="low",
    keywords=["trial capacity", "dalys", "treatment acceleration", "WHO", "GBD"],
    inputs=['GLOBAL_ANNUAL_DALY_BURDEN', 'EVENTUALLY_AVOIDABLE_DALY_PCT', 'DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DALY_BURDEN"] * ctx["EVENTUALLY_AVOIDABLE_DALY_PCT"] * ctx["DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS"],
    latex_symbol=r"DALYs_{capacity}",  # LaTeX symbol for equations
)

DFDA_TRIAL_CAPACITY_ECONOMIC_VALUE = Parameter(
    float(DFDA_TRIAL_CAPACITY_DALYS_AVERTED) * float(STANDARD_ECONOMIC_QALY_VALUE_USD),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total economic value from trial capacity increase alone. DALYs valued at standard economic rate.",
    display_name="Economic Value from Trial Capacity Increase",
    unit="USD",
    formula="TRIAL_CAPACITY_DALYS_AVERTED × STANDARD_QALY_VALUE",
    confidence="low",
    keywords=["trial capacity", "economic", "value", "USD"],
    inputs=['DFDA_TRIAL_CAPACITY_DALYS_AVERTED', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_DALYS_AVERTED"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Value_{capacity}",  # LaTeX symbol for equations
)

# ============================================================================
# COMBINED BENEFITS (Trial Capacity + Efficacy Lag)
# ============================================================================
# Combines two independent effects:
# 1. Treatment timeline acceleration - average disease gets first treatment earlier due to increased capacity
# 2. Efficacy lag elimination - once discovered, treatments deploy without post-safety delay
DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS = Parameter(
    float(DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS) + float(EFFICACY_LAG_YEARS),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Average years earlier patients receive treatments from increased pragmatic trial capacity plus efficacy lag elimination for treatments already discovered.",
    display_name="Average Total Treatment Timeline Shift",
    unit="years",
    formula="TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS + EFFICACY_LAG_YEARS",
    confidence="low",
    keywords=["pragmatic trials", "total", "timeline", "shift", "acceleration", "efficacy lag", "years", "average"],
    inputs=['DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS', 'EFFICACY_LAG_YEARS'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS"] + ctx["EFFICACY_LAG_YEARS"],
    latex_symbol=r"T_{accel,max}",  # LaTeX symbol for equations
)  # ~207 years average total timeline shift from dFDA

# Pragmatic trial treatment rate (diseases getting first treatment per year)
DFDA_FIRST_TREATMENTS_PER_YEAR = Parameter(
    float(NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR) * float(DFDA_TRIAL_CAPACITY_MULTIPLIER),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Diseases per year receiving their first effective treatment with treaty-scale pragmatic trial capacity. Scales proportionally with trial capacity multiplier.",
    display_name="New Treatments Per Year at Treaty-Scale Trial Capacity",
    unit="diseases/year",
    formula="NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR × PRAGMATIC_TRIAL_CAPACITY_MULTIPLIER",
    confidence="low",
    keywords=["pragmatic trials", "cures", "diseases", "per year", "rate", "first treatment"],
    inputs=['NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR', 'DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR"] * ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"],
    latex_symbol=r"Treatments_{trial,ann}",  # LaTeX symbol for equations
)

# Time to explore entire therapeutic space with treaty-scale pragmatic trial capacity
DFDA_QUEUE_CLEARANCE_YEARS = Parameter(
    float(STATUS_QUO_QUEUE_CLEARANCE_YEARS) / float(DFDA_TRIAL_CAPACITY_MULTIPLIER),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Years to explore the entire therapeutic search space with treaty-scale pragmatic trial capacity. At increased discovery rate, finding first treatments for all currently untreatable diseases takes ~36 years instead of ~443.",
    display_name="Therapeutic Space Exploration Time at Treaty-Scale Trial Capacity",
    unit="years",
    formula="STATUS_QUO_QUEUE_CLEARANCE_YEARS ÷ PRAGMATIC_TRIAL_CAPACITY_MULTIPLIER",
    confidence="low",
    keywords=["pragmatic trials", "queue", "clearance", "all diseases", "cure all", "years"],
    inputs=['STATUS_QUO_QUEUE_CLEARANCE_YEARS', 'DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["STATUS_QUO_QUEUE_CLEARANCE_YEARS"] / ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"],
    latex_symbol=r"T_{queue,trial}",  # LaTeX symbol for equations
)

WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR = Parameter(
    round(
        float(WAR_TRIAL_REDIRECT_START_YEAR)
        + float(WAR_TRIAL_REDIRECT_TOOLCHAIN_BOOTSTRAP_YEARS)
        + float(DFDA_QUEUE_CLEARANCE_YEARS)
    ),
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Aggressive prosecutor pleading cutoff year for presumptive disease-death plaintiffs. "
                "Calculated as the 1900 redirect start year plus medical-toolchain bootstrap years "
                "plus the treaty-scale therapeutic queue-clearance years.",
    display_name="War-Redirect Disease Pleading Cutoff Year",
    unit="year",
    formula="round(WAR_TRIAL_REDIRECT_START_YEAR + WAR_TRIAL_REDIRECT_TOOLCHAIN_BOOTSTRAP_YEARS + DFDA_QUEUE_CLEARANCE_YEARS)",
    inputs=[
        "WAR_TRIAL_REDIRECT_START_YEAR",
        "WAR_TRIAL_REDIRECT_TOOLCHAIN_BOOTSTRAP_YEARS",
        "DFDA_QUEUE_CLEARANCE_YEARS",
    ],
    compute=lambda ctx: round(
        ctx["WAR_TRIAL_REDIRECT_START_YEAR"]
        + ctx["WAR_TRIAL_REDIRECT_TOOLCHAIN_BOOTSTRAP_YEARS"]
        + ctx["DFDA_QUEUE_CLEARANCE_YEARS"]
    ),
    keywords=["war", "medical misallocation", "pleading", "disease deaths", "plaintiffs", "prosecutor"],
    latex_symbol=r"Y_{disease,plead}",
)

WAR_TRIAL_REDIRECT_INFECTIOUS_DISEASE_CONTROL_YEAR = Parameter(
    WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Counterfactual calendar year for practical infectious-disease control in the "
                "aggressive medical-redirect model. Uses the calculated disease pleading cutoff year.",
    display_name="War-Redirect Infectious Disease Control Year",
    unit="year",
    formula="WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR",
    inputs=["WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR"],
    keywords=["war", "medical opportunity cost", "infectious disease", "clinical trials", "counterfactual"],
    latex_symbol=r"Y_{infectious,redirect}",
)

WAR_TRIAL_REDIRECT_NONAGING_DISEASE_CONTROL_YEAR = Parameter(
    WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Counterfactual calendar year for practical control of major non-aging disease burden "
                "in the aggressive medical-redirect model. Uses the calculated disease pleading cutoff year.",
    display_name="War-Redirect Major Non-Aging Disease Control Year",
    unit="year",
    formula="WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR",
    inputs=["WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR"],
    keywords=["war", "medical opportunity cost", "non-aging disease control", "clinical trials", "counterfactual"],
    latex_symbol=r"Y_{disease,redirect}",
)

WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR = Parameter(
    WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR
    + WAR_TRIAL_REDIRECT_AGING_LAG_AFTER_DISEASE_CONTROL_YEARS,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Aggressive prosecutor pleading cutoff year for presumptive aging-death plaintiffs. "
                "Calculated as the disease cutoff plus the geroscience lag assumption.",
    display_name="War-Redirect Aging Pleading Cutoff Year",
    unit="year",
    formula="WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR + WAR_TRIAL_REDIRECT_AGING_LAG_AFTER_DISEASE_CONTROL_YEARS",
    inputs=[
        "WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR",
        "WAR_TRIAL_REDIRECT_AGING_LAG_AFTER_DISEASE_CONTROL_YEARS",
    ],
    compute=lambda ctx: (
        ctx["WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR"]
        + ctx["WAR_TRIAL_REDIRECT_AGING_LAG_AFTER_DISEASE_CONTROL_YEARS"]
    ),
    keywords=["war", "medical misallocation", "pleading", "aging", "plaintiffs", "prosecutor"],
    latex_symbol=r"Y_{aging,plead}",
)

WAR_TRIAL_REDIRECT_AGING_CONTROL_SENSITIVITY_YEAR = Parameter(
    WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Counterfactual calendar year when biological aging becomes a treatable risk factor "
                "in the aggressive medical-redirect model. Uses the calculated aging pleading cutoff year.",
    display_name="War-Redirect Biological Aging Control Year",
    unit="year",
    formula="WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR",
    inputs=["WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR"],
    keywords=["war", "medical opportunity cost", "aging", "longevity", "clinical trials", "sensitivity"],
    latex_symbol=r"Y_{aging,redirect}",
)

# ============================================================================
# TOTAL LIVES SAVED FROM COMBINED TIMELINE SHIFT
# ============================================================================
# These parameters use the combined timeline shift from both cure acceleration
# and efficacy lag elimination.

DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED = Parameter(
    float(GLOBAL_DISEASE_DEATHS_DAILY) * float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS) * DAYS_PER_YEAR * (1 - _unavoidable_pct),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total eventually avoidable deaths from the combined treatment timeline shift. Represents deaths prevented when cures arrive earlier due to both increased trial capacity and eliminated efficacy lag.",
    display_name="Total Lives Saved from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
    unit="deaths",
    formula="ANNUAL_DEATHS × TOTAL_TIMELINE_SHIFT_YEARS × AVOIDABLE_PCT",
    confidence="low",
    keywords=["total", "lives saved", "timeline shift", "cure acceleration", "efficacy lag", "average"],
    inputs=['GLOBAL_DISEASE_DEATHS_DAILY', 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS'],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DEATHS_DAILY"] * ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS"] * DAYS_PER_YEAR * (1 - _unavoidable_pct),
    latex_symbol=r"Lives_{max}",  # LaTeX symbol for equations
)

DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS = Parameter(
    float(GLOBAL_ANNUAL_DALY_BURDEN) * float(EVENTUALLY_AVOIDABLE_DALY_PCT) * float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total DALYs averted from the combined treatment timeline shift. Calculated as annual global DALY burden × eventually avoidable percentage × timeline shift years. Includes both fatal and non-fatal diseases (WHO GBD methodology).",
    display_name="Total DALYs from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
    unit="DALYs",
    formula="GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT × TIMELINE_SHIFT",
    confidence="low",
    keywords=["total", "dalys", "timeline shift", "cure acceleration", "efficacy lag", "WHO", "GBD"],
    inputs=['GLOBAL_ANNUAL_DALY_BURDEN', 'EVENTUALLY_AVOIDABLE_DALY_PCT', 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DALY_BURDEN"] * ctx["EVENTUALLY_AVOIDABLE_DALY_PCT"] * ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS"],
    latex_symbol=r"DALYs_{max}",  # LaTeX symbol for equations
)  # ~549B DALYs averted (vs old 200B - now includes non-fatal chronic diseases)

DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS) * float(STANDARD_ECONOMIC_QALY_VALUE_USD),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total economic value from the combined treatment timeline shift. DALYs valued at standard economic rate.",
    display_name="Total Economic Benefit from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
    unit="USD",
    formula="DALYS × STANDARD_QALY_VALUE",
    confidence="low",
    keywords=["total", "economic", "value", "timeline shift", "USD"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Value_{max}",  # LaTeX symbol for equations
)

CORPORATE_DAMAGES_WAR_DEATHS_VSL = Parameter(
    WAR_DEATHS_SINCE_1900 * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Corporate-defendant wrongful-death valuation for war deaths since 1900 using the standard value of a statistical life.",
    display_name="Corporate Damages War Deaths VSL",
    unit="USD",
    formula="WAR_DEATHS_SINCE_1900 * VALUE_OF_STATISTICAL_LIFE",
    inputs=["WAR_DEATHS_SINCE_1900", "VALUE_OF_STATISTICAL_LIFE"],
    compute=lambda ctx: ctx["WAR_DEATHS_SINCE_1900"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    keywords=["corporate", "damages", "war deaths", "VSL", "prosecutor"],
    latex_symbol=r"V_{war,VSL}",
)

CORPORATE_DAMAGES_EFFICACY_LAG_DEATHS_VSL = Parameter(
    EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Corporate-defendant wrongful-death valuation for existing-drug efficacy-lag deaths using the standard value of a statistical life.",
    display_name="Corporate Damages Efficacy Lag Deaths VSL",
    unit="USD",
    formula="EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL * VALUE_OF_STATISTICAL_LIFE",
    inputs=["EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL", "VALUE_OF_STATISTICAL_LIFE"],
    compute=lambda ctx: ctx["EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    keywords=["corporate", "damages", "efficacy lag", "VSL", "prosecutor"],
    latex_symbol=r"V_{lag,VSL}",
)

CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_DEATHS = Parameter(
    300_000_000,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.DEFINITION,
    description="Aggressive prosecutor pleading estimate for deaths from drugs never developed because regulatory cost and misallocated trial capacity suppressed development. Based on the Humanity v. Government exclusion note that drugs never developed may double or triple Count Two; this uses the high end of that pleading range.",
    display_name="Corporate Damages Drugs Never Developed Deaths",
    unit="deaths",
    distribution="fixed",
    keywords=["corporate", "damages", "drugs never developed", "Count Two", "prosecutor"],
    latex_symbol=r"Deaths_{neverdev}",
)

CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_VSL = Parameter(
    CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_DEATHS * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Corporate-defendant wrongful-death valuation for the aggressive prosecutor estimate of deaths from drugs never developed.",
    display_name="Corporate Damages Drugs Never Developed VSL",
    unit="USD",
    formula="CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_DEATHS * VALUE_OF_STATISTICAL_LIFE",
    inputs=["CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_DEATHS", "VALUE_OF_STATISTICAL_LIFE"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_DEATHS"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    keywords=["corporate", "damages", "drugs never developed", "VSL", "prosecutor"],
    latex_symbol=r"V_{neverdev,VSL}",
)

CORPORATE_DAMAGES_PROPERTY_ENVIRONMENTAL_DESTRUCTION = Parameter(
    WAR_PROPERTY_DESTRUCTION_SINCE_1900 + WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Property and environmental destruction from war since 1900, separated from war death valuation to avoid adding the QALY component embedded in the broader historical sunk-cost parameter.",
    display_name="Corporate Damages Property Plus Environmental Destruction",
    unit="USD",
    formula="WAR_PROPERTY_DESTRUCTION_SINCE_1900 + WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900",
    inputs=["WAR_PROPERTY_DESTRUCTION_SINCE_1900", "WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900"],
    compute=lambda ctx: ctx["WAR_PROPERTY_DESTRUCTION_SINCE_1900"] + ctx["WAR_ENVIRONMENTAL_DESTRUCTION_SINCE_1900"],
    keywords=["corporate", "damages", "property", "environmental", "war"],
    latex_symbol=r"D_{property+env}",
)

CORPORATE_DAMAGES_PENTAGON_FCA_PENALTY_INCREMENT = Parameter(
    PENTAGON_UNACCOUNTED_FALSE_CLAIMS_ANALOG_EXPOSURE - PENTAGON_UNACCOUNTED_FUNDS,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="False Claims Act-style penalty increment on Pentagon unaccounted funds, calculated as treble exposure minus principal so the principal is not counted twice.",
    display_name="Corporate Damages Pentagon FCA Penalty Increment",
    unit="USD",
    formula="PENTAGON_UNACCOUNTED_FALSE_CLAIMS_ANALOG_EXPOSURE - PENTAGON_UNACCOUNTED_FUNDS",
    inputs=["PENTAGON_UNACCOUNTED_FALSE_CLAIMS_ANALOG_EXPOSURE", "PENTAGON_UNACCOUNTED_FUNDS"],
    compute=lambda ctx: ctx["PENTAGON_UNACCOUNTED_FALSE_CLAIMS_ANALOG_EXPOSURE"] - ctx["PENTAGON_UNACCOUNTED_FUNDS"],
    keywords=["corporate", "damages", "false claims", "pentagon", "audit", "penalty increment"],
    latex_symbol=r"Penalty_{pentagon,FCA}",
)

CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL = Parameter(
    CORPORATE_DAMAGES_WAR_DEATHS_VSL
    + CORPORATE_DAMAGES_EFFICACY_LAG_DEATHS_VSL
    + CORPORATE_DAMAGES_PROPERTY_ENVIRONMENTAL_DESTRUCTION
    + WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE
    + CORPORATE_DAMAGES_PENTAGON_FCA_PENALTY_INCREMENT,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Strict non-duplicative corporate damages floor: war-death VSL, existing-drug efficacy-lag VSL, property and environmental destruction, excess military spending above the 1900 freeze, and the Pentagon FCA-style penalty increment.",
    display_name="Corporate Damages Strict Floor Total",
    unit="USD",
    formula="CORPORATE_DAMAGES_WAR_DEATHS_VSL + CORPORATE_DAMAGES_EFFICACY_LAG_DEATHS_VSL + CORPORATE_DAMAGES_PROPERTY_ENVIRONMENTAL_DESTRUCTION + WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE + CORPORATE_DAMAGES_PENTAGON_FCA_PENALTY_INCREMENT",
    inputs=[
        "CORPORATE_DAMAGES_WAR_DEATHS_VSL",
        "CORPORATE_DAMAGES_EFFICACY_LAG_DEATHS_VSL",
        "CORPORATE_DAMAGES_PROPERTY_ENVIRONMENTAL_DESTRUCTION",
        "WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE",
        "CORPORATE_DAMAGES_PENTAGON_FCA_PENALTY_INCREMENT",
    ],
    compute=lambda ctx: (
        ctx["CORPORATE_DAMAGES_WAR_DEATHS_VSL"]
        + ctx["CORPORATE_DAMAGES_EFFICACY_LAG_DEATHS_VSL"]
        + ctx["CORPORATE_DAMAGES_PROPERTY_ENVIRONMENTAL_DESTRUCTION"]
        + ctx["WAR_TRIAL_REDIRECT_EXCESS_MILITARY_SPENDING_ABOVE_1900_FREEZE"]
        + ctx["CORPORATE_DAMAGES_PENTAGON_FCA_PENALTY_INCREMENT"]
    ),
    keywords=["corporate", "damages", "strict floor", "non-duplicative", "prosecutor"],
    latex_symbol=r"D_{corp,floor}",
)

CORPORATE_DAMAGES_STRICT_FLOOR_PER_CAPITA = Parameter(
    CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Strict non-duplicative corporate damages floor per living human.",
    display_name="Corporate Damages Strict Floor Per Capita",
    unit="USD/person",
    formula="CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL / GLOBAL_POPULATION_2024",
    inputs=["CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["corporate", "damages", "strict floor", "per capita", "prosecutor"],
    latex_symbol=r"D_{corp,floor,pc}",
)

CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL = Parameter(
    CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL + CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_VSL,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Aggressive corporate-liability prosecutor base ask: strict floor plus the aggressive pleading estimate for deaths from drugs never developed. Excludes punitive damages, disgorgement, ongoing lost-income damages, and forward treaty settlement value.",
    display_name="Corporate Damages Prosecutor Base Ask Total",
    unit="USD",
    formula="CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL + CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_VSL",
    inputs=["CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL", "CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_VSL"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL"] + ctx["CORPORATE_DAMAGES_DRUGS_NEVER_DEVELOPED_VSL"],
    keywords=["corporate", "damages", "base ask", "prosecutor", "drugs never developed"],
    latex_symbol=r"D_{corp,ask}",
)

CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_PER_CAPITA = Parameter(
    CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Aggressive corporate-liability prosecutor base ask per living human.",
    display_name="Corporate Damages Prosecutor Base Ask Per Capita",
    unit="USD/person",
    formula="CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL / GLOBAL_POPULATION_2024",
    inputs=["CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["corporate", "damages", "base ask", "per capita", "prosecutor"],
    latex_symbol=r"D_{corp,ask,pc}",
)

CORPORATE_DAMAGES_TREBLE_EXPOSURE_TOTAL = Parameter(
    CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL * CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Treble-style exposure if the prosecutor base ask is multiplied under a False Claims Act-style corporate penalty analogy.",
    display_name="Corporate Damages Treble-Style Exposure Total",
    unit="USD",
    formula="CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL * CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER",
    inputs=["CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL", "CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL"] * ctx["CORPORATE_ANALOG_FALSE_CLAIMS_TREBLE_MULTIPLIER"],
    keywords=["corporate", "damages", "treble", "false claims", "exposure"],
    latex_symbol=r"D_{corp,treble}",
)

CORPORATE_DAMAGES_TREBLE_EXPOSURE_PER_CAPITA = Parameter(
    CORPORATE_DAMAGES_TREBLE_EXPOSURE_TOTAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Treble-style exposure per living human under the False Claims Act-style corporate penalty analogy.",
    display_name="Corporate Damages Treble-Style Exposure Per Capita",
    unit="USD/person",
    formula="CORPORATE_DAMAGES_TREBLE_EXPOSURE_TOTAL / GLOBAL_POPULATION_2024",
    inputs=["CORPORATE_DAMAGES_TREBLE_EXPOSURE_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_TREBLE_EXPOSURE_TOTAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["corporate", "damages", "treble", "per capita", "exposure"],
    latex_symbol=r"D_{corp,treble,pc}",
)

CORPORATE_DAMAGES_STATE_FARM_CEILING_MULTIPLIER = Parameter(
    10,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_ref=ReferenceID.STATE_FARM_V_CAMPBELL_2003,
    source_type=SourceType.EXTERNAL,
    description="Total exposure multiplier for a 9:1 punitive-to-compensatory ratio, meaning base damages plus nine times base damages. Used as constitutional-ceiling exposure under State Farm v. Campbell, not a typical award.",
    display_name="State Farm Constitutional-Ceiling Exposure Multiplier",
    unit="multiplier",
    distribution="fixed",
    keywords=["corporate", "damages", "State Farm", "punitive", "constitutional ceiling"],
    latex_symbol=r"m_{StateFarm}",
)

CORPORATE_DAMAGES_STATE_FARM_CEILING_EXPOSURE_TOTAL = Parameter(
    CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL * CORPORATE_DAMAGES_STATE_FARM_CEILING_MULTIPLIER,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Constitutional-ceiling exposure under State Farm v. Campbell: prosecutor base ask plus a 9:1 punitive-to-compensatory multiplier. This is exposure, not a typical award.",
    display_name="Corporate Damages State Farm Constitutional-Ceiling Exposure Total",
    unit="USD",
    formula="CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL * CORPORATE_DAMAGES_STATE_FARM_CEILING_MULTIPLIER",
    inputs=["CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL", "CORPORATE_DAMAGES_STATE_FARM_CEILING_MULTIPLIER"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_PROSECUTOR_BASE_ASK_TOTAL"] * ctx["CORPORATE_DAMAGES_STATE_FARM_CEILING_MULTIPLIER"],
    keywords=["corporate", "damages", "State Farm", "punitive", "constitutional ceiling", "exposure"],
    latex_symbol=r"D_{corp,StateFarm}",
)

CORPORATE_DAMAGES_STATE_FARM_CEILING_EXPOSURE_PER_CAPITA = Parameter(
    CORPORATE_DAMAGES_STATE_FARM_CEILING_EXPOSURE_TOTAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    description="Constitutional-ceiling exposure per living human under State Farm v. Campbell. This is exposure, not a typical award.",
    display_name="Corporate Damages State Farm Constitutional-Ceiling Exposure Per Capita",
    unit="USD/person",
    formula="CORPORATE_DAMAGES_STATE_FARM_CEILING_EXPOSURE_TOTAL / GLOBAL_POPULATION_2024",
    inputs=["CORPORATE_DAMAGES_STATE_FARM_CEILING_EXPOSURE_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_STATE_FARM_CEILING_EXPOSURE_TOTAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["corporate", "damages", "State Farm", "punitive", "per capita", "exposure"],
    latex_symbol=r"D_{corp,StateFarm,pc}",
)

CORPORATE_DAMAGES_FORWARD_SETTLEMENT_VALUE_PER_CAPITA = Parameter(
    DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/solution/court-of-humanity.qmd",
    source_type=SourceType.CALCULATED,
    description="Forward treaty settlement value per living human from the 1% Treaty impact model. Kept separate from historical corporate damages.",
    display_name="Corporate Damages Forward Settlement Value Per Capita",
    unit="USD/person",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE / GLOBAL_POPULATION_2024",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["corporate", "damages", "forward settlement", "treaty", "per capita"],
    latex_symbol=r"V_{settlement,pc}",
)

DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS) * float(GLOBAL_YLD_PROPORTION_OF_DALYS) * HOURS_PER_YEAR,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Hours of suffering eliminated from the combined treatment timeline shift. Calculated from YLD component of DALYs (39% of total DALYs × hours per year). One-time benefit, not annual recurring.",
    display_name="Suffering Hours Eliminated from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
    unit="hours",
    formula="TOTAL_TIMELINE_SHIFT_DALYS × GLOBAL_YLD_PROPORTION × HOURS_PER_YEAR",
    confidence="low",
    keywords=["suffering", "disability", "pain", "morbidity", "quality of life", "one-time benefit", "disease burden", "trial capacity", "efficacy lag", "YLD", "hours"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS', 'GLOBAL_YLD_PROPORTION_OF_DALYS'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"] * ctx["GLOBAL_YLD_PROPORTION_OF_DALYS"] * HOURS_PER_YEAR,
    latex_symbol=r"Hours_{suffer,max}",  # LaTeX symbol for equations
)  # ~1,875 trillion hours from full timeline shift (vs old 193T - now based on WHO YLD proportion)

# ============================================================================
# UNIVERSAL RIGHT TO TRY WITH EVIDENCE
# Conditional impact if all 50 states adopt and the system remains in force.
# The model intentionally has two uncertain inputs: total philanthropic cost
# and the resulting treatment-discovery multiplier. Existing global disease
# burden parameters supply the rest of the Treaty-style calculation.
# ============================================================================

STATE_RTT_PHILANTHROPIC_COST_TOTAL = Parameter(
    65_000_000,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="definition",
    description="Total philanthropic cost of adopting Universal Right to Try with Evidence in all 50 states: a central $15 million campaign estimate covering legislation or amendment in all 50 states plus $50 million for the shared registry's first ten years. The model bill requires participating centers to fund continued registry operation after year ten. This philanthropic numerator excludes patient or payer spending on treatment delivery, trial-site services, and permitted study costs. The wide interval represents campaign and infrastructure cost uncertainty without separate scenario parameters.",
    display_name="Universal Right to Try with Evidence Philanthropic Cost",
    unit="USD",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(25_000_000, 200_000_000),
    keywords=["right to try", "right to trial", "state legislation", "campaign", "registry", "philanthropy"],
    latex_symbol=r"C_{RTT}",
    hide_ci=True,
)

STATE_RTT_TREATMENT_DISCOVERY_MULTIPLIER = Parameter(
    5.48,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="definition",
    description="Conditional multiplier on the worldwide first-treatment discovery rate after all 50 states adopt and a mature pooled pragmatic-trial system operates under applicable federal authorization. The 5.48x central calibration reproduces the prior model's 82.2 versus 15 first treatments per year; it is an assumption, not an observed effect estimate. This single input incorporates patient or payer funding of treatment delivery, trial-site services, and permitted study costs, newly viable post-Phase-1 treatment-condition pairs, evaluable protocol quality, candidate supply, and scientific success. Its range describes productivity of an operating system, not the separate probability that advocacy achieves full adoption and implementation.",
    display_name="Universal Right to Try with Evidence Treatment Discovery Multiplier",
    unit="x",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(1.1, 15.0),
    keywords=["right to try", "right to trial", "treatment discovery", "trial capacity", "self-funding", "multiplier"],
    latex_symbol=r"k_{RTT}",
    hide_ci=True,
)

STATE_RTT_TREATMENT_ACCELERATION_YEARS = Parameter(
    float(STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT)
    * (1 - 1 / float(STATE_RTT_TREATMENT_DISCOVERY_MULTIPLIER)),
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Average years earlier the first effective treatment arrives across the global therapeutic frontier after all 50 states adopt Universal Right to Try with Evidence. Uses the same schedule-shift structure as the 1% Treaty impact model: the status quo discovery timeline multiplied by one minus the inverse treatment-discovery multiplier.",
    display_name="Average Treatment Acceleration from Universal Right to Try with Evidence",
    unit="years",
    formula="STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT × (1 - 1 / STATE_RTT_TREATMENT_DISCOVERY_MULTIPLIER)",
    confidence="low",
    inputs=["STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT", "STATE_RTT_TREATMENT_DISCOVERY_MULTIPLIER"],
    compute=lambda ctx: ctx["STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT"]
    * (1 - 1 / ctx["STATE_RTT_TREATMENT_DISCOVERY_MULTIPLIER"]),
    keywords=["right to try", "right to trial", "treatment acceleration", "cure schedule", "years"],
    latex_symbol=r"T_{accel,RTT}",
    hide_ci=True,
)

STATE_RTT_TREATMENT_ACCELERATION_DALYS = Parameter(
    float(GLOBAL_ANNUAL_DALY_BURDEN)
    * float(EVENTUALLY_AVOIDABLE_DALY_PCT)
    * float(STATE_RTT_TREATMENT_ACCELERATION_YEARS),
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Conditional lifetime DALYs averted by shifting the global treatment-discovery schedule forward. By design, this applies the therapeutic-discovery timeline proxy to the eventually avoidable burden of all global diseases and aging-related degeneration. It is a schedule-shift calculation across future generations, not an observed epidemiological forecast.",
    display_name="DALYs Averted from Universal Right to Try with Evidence",
    unit="DALYs",
    formula="GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT × STATE_RTT_TREATMENT_ACCELERATION_YEARS",
    confidence="low",
    inputs=["GLOBAL_ANNUAL_DALY_BURDEN", "EVENTUALLY_AVOIDABLE_DALY_PCT", "STATE_RTT_TREATMENT_ACCELERATION_YEARS"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DALY_BURDEN"]
    * ctx["EVENTUALLY_AVOIDABLE_DALY_PCT"]
    * ctx["STATE_RTT_TREATMENT_ACCELERATION_YEARS"],
    keywords=["right to try", "right to trial", "DALY", "disease burden", "schedule shift"],
    latex_symbol=r"DALYs_{RTT}",
    hide_ci=True,
)

STATE_RTT_TREATMENT_ACCELERATION_LIVES_SAVED = Parameter(
    float(GLOBAL_DISEASE_DEATHS_DAILY)
    * DAYS_PER_YEAR
    * float(EVENTUALLY_AVOIDABLE_DEATH_PCT)
    * float(STATE_RTT_TREATMENT_ACCELERATION_YEARS),
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Conditional cumulative premature deaths from global diseases and aging prevented across future generations by shifting the treatment-discovery schedule forward. The total can exceed the current population because it sums deaths prevented over the full acceleration period.",
    display_name="Lives Saved from Universal Right to Try with Evidence",
    unit="deaths",
    formula="GLOBAL_DISEASE_DEATHS_DAILY × DAYS_PER_YEAR × EVENTUALLY_AVOIDABLE_DEATH_PCT × STATE_RTT_TREATMENT_ACCELERATION_YEARS",
    confidence="low",
    inputs=["GLOBAL_DISEASE_DEATHS_DAILY", "EVENTUALLY_AVOIDABLE_DEATH_PCT", "STATE_RTT_TREATMENT_ACCELERATION_YEARS"],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DEATHS_DAILY"]
    * DAYS_PER_YEAR
    * ctx["EVENTUALLY_AVOIDABLE_DEATH_PCT"]
    * ctx["STATE_RTT_TREATMENT_ACCELERATION_YEARS"],
    keywords=["right to try", "right to trial", "lives saved", "premature deaths", "schedule shift"],
    latex_symbol=r"Lives_{RTT}",
    hide_ci=True,
)

STATE_RTT_TREATMENT_ACCELERATION_SUFFERING_HOURS = Parameter(
    float(STATE_RTT_TREATMENT_ACCELERATION_DALYS)
    * float(GLOBAL_YLD_PROPORTION_OF_DALYS)
    * HOURS_PER_YEAR,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Conditional disability-equivalent hours prevented by the treatment schedule shift. Converts the years-lived-with-disability share of DALYs into hours; it does not claim every hour is an hour of conscious pain.",
    display_name="Disability-Equivalent Suffering Hours Prevented by Universal Right to Try with Evidence",
    unit="hours",
    formula="STATE_RTT_TREATMENT_ACCELERATION_DALYS × GLOBAL_YLD_PROPORTION_OF_DALYS × HOURS_PER_YEAR",
    confidence="low",
    inputs=["STATE_RTT_TREATMENT_ACCELERATION_DALYS", "GLOBAL_YLD_PROPORTION_OF_DALYS"],
    compute=lambda ctx: ctx["STATE_RTT_TREATMENT_ACCELERATION_DALYS"]
    * ctx["GLOBAL_YLD_PROPORTION_OF_DALYS"]
    * HOURS_PER_YEAR,
    keywords=["right to try", "right to trial", "suffering", "disability", "YLD", "hours"],
    latex_symbol=r"Hours_{suffer,RTT}",
    hide_ci=True,
)

STATE_RTT_PHILANTHROPIC_COST_PER_DALY = Parameter(
    float(STATE_RTT_PHILANTHROPIC_COST_TOTAL) / float(STATE_RTT_TREATMENT_ACCELERATION_DALYS),
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Conditional philanthropic cost per DALY if all 50 states adopt, a mature pooled pragmatic-trial system operates under applicable federal authorization, and the modeled treatment-discovery acceleration occurs. The numerator includes the 50-state campaign and ten-year registry launch costs, excludes patient or payer spending on treatment delivery, trial-site services, and permitted study costs, and assumes center assessments fund the registry thereafter. The denominator counts the global treatment schedule shift once.",
    display_name="Universal Right to Try with Evidence Philanthropic Cost per DALY",
    unit="USD/DALY",
    formula="STATE_RTT_PHILANTHROPIC_COST_TOTAL ÷ STATE_RTT_TREATMENT_ACCELERATION_DALYS",
    confidence="low",
    inputs=["STATE_RTT_PHILANTHROPIC_COST_TOTAL", "STATE_RTT_TREATMENT_ACCELERATION_DALYS"],
    compute=lambda ctx: ctx["STATE_RTT_PHILANTHROPIC_COST_TOTAL"]
    / ctx["STATE_RTT_TREATMENT_ACCELERATION_DALYS"],
    keywords=["right to try", "right to trial", "cost per DALY", "GiveWell", "philanthropy"],
    latex_symbol=r"Cost_{RTT,DALY}",
    hide_ci=True,
)

STATE_RTT_PHILANTHROPIC_COST_PER_LIFE_SAVED = Parameter(
    float(STATE_RTT_PHILANTHROPIC_COST_TOTAL) / float(STATE_RTT_TREATMENT_ACCELERATION_LIVES_SAVED),
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Conditional philanthropic cost per modeled premature death prevented if all 50 states adopt, a mature pooled pragmatic-trial system operates, and the modeled treatment-discovery acceleration occurs. This uses the same campaign and registry numerator as the cost-per-DALY estimate.",
    display_name="Universal Right to Try with Evidence Philanthropic Cost per Life Saved",
    unit="USD/life",
    formula="STATE_RTT_PHILANTHROPIC_COST_TOTAL ÷ STATE_RTT_TREATMENT_ACCELERATION_LIVES_SAVED",
    confidence="low",
    inputs=["STATE_RTT_PHILANTHROPIC_COST_TOTAL", "STATE_RTT_TREATMENT_ACCELERATION_LIVES_SAVED"],
    compute=lambda ctx: ctx["STATE_RTT_PHILANTHROPIC_COST_TOTAL"]
    / ctx["STATE_RTT_TREATMENT_ACCELERATION_LIVES_SAVED"],
    keywords=["right to try", "right to trial", "cost per life saved", "GiveWell", "philanthropy"],
    latex_symbol=r"Cost_{RTT,life}",
    hide_ci=True,
)

STATE_RTT_FDA_BUDGET_EQUIVALENT_HOURS = Parameter(
    float(STATE_RTT_PHILANTHROPIC_COST_TOTAL) / float(FDA_ANNUAL_PROGRAM_BUDGET) * HOURS_PER_YEAR,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Hours of the FDA annual program budget equal to the full central philanthropic launch cost for adopting Universal Right to Try with Evidence in all 50 states. This is a scale comparison, not a claim about FDA cost-effectiveness.",
    display_name="Universal Right to Try with Evidence Cost in FDA Budget Hours",
    unit="hours",
    formula="STATE_RTT_PHILANTHROPIC_COST_TOTAL ÷ FDA_ANNUAL_PROGRAM_BUDGET × 8,760",
    confidence="low",
    inputs=["STATE_RTT_PHILANTHROPIC_COST_TOTAL", "FDA_ANNUAL_PROGRAM_BUDGET"],
    compute=lambda ctx: ctx["STATE_RTT_PHILANTHROPIC_COST_TOTAL"]
    / ctx["FDA_ANNUAL_PROGRAM_BUDGET"]
    * HOURS_PER_YEAR,
    keywords=["right to try", "right to trial", "fda", "budget", "hours", "scale comparison"],
    latex_symbol=r"Hours_{RTT,FDA}",
    hide_ci=True,
)

STATE_RTT_NIH_BUDGET_EQUIVALENT_HOURS = Parameter(
    float(STATE_RTT_PHILANTHROPIC_COST_TOTAL) / float(NIH_ANNUAL_BUDGET) * HOURS_PER_YEAR,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Hours of the NIH annual budget equal to the full central philanthropic launch cost for adopting Universal Right to Try with Evidence in all 50 states. This is a scale comparison, not a claim about NIH cost-effectiveness.",
    display_name="Universal Right to Try with Evidence Cost in NIH Budget Hours",
    unit="hours",
    formula="STATE_RTT_PHILANTHROPIC_COST_TOTAL ÷ NIH_ANNUAL_BUDGET × 8,760",
    confidence="low",
    inputs=["STATE_RTT_PHILANTHROPIC_COST_TOTAL", "NIH_ANNUAL_BUDGET"],
    compute=lambda ctx: ctx["STATE_RTT_PHILANTHROPIC_COST_TOTAL"]
    / ctx["NIH_ANNUAL_BUDGET"]
    * HOURS_PER_YEAR,
    keywords=["right to try", "right to trial", "nih", "budget", "hours", "scale comparison"],
    latex_symbol=r"Hours_{RTT,NIH}",
    hide_ci=True,
)

STATE_RTT_US_MILITARY_OVERSPEND_EQUIVALENT_HOURS = Parameter(
    float(STATE_RTT_PHILANTHROPIC_COST_TOTAL) / float(US_GOV_WASTE_MILITARY_OVERSPEND) * HOURS_PER_YEAR,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Hours of estimated annual US military spending above the first-principles baseline for preventing direct attacks on people in the United States equal to the full central philanthropic launch cost for adopting Universal Right to Try with Evidence in all 50 states.",
    display_name="Universal Right to Try with Evidence Cost in US Military Overspend Hours",
    unit="hours",
    formula="STATE_RTT_PHILANTHROPIC_COST_TOTAL ÷ US_GOV_WASTE_MILITARY_OVERSPEND × 8,760",
    confidence="low",
    inputs=["STATE_RTT_PHILANTHROPIC_COST_TOTAL", "US_GOV_WASTE_MILITARY_OVERSPEND"],
    compute=lambda ctx: ctx["STATE_RTT_PHILANTHROPIC_COST_TOTAL"]
    / ctx["US_GOV_WASTE_MILITARY_OVERSPEND"]
    * HOURS_PER_YEAR,
    keywords=["right to try", "right to trial", "military overspend", "budget", "hours", "reallocation"],
    latex_symbol=r"Hours_{RTT,mil}",
    hide_ci=True,
)

# Pragmatic trial system targets (using trial capacity multiplier)
DFDA_TRIALS_PER_YEAR_CAPACITY = Parameter(
    float(CURRENT_TRIALS_PER_YEAR) * float(DFDA_TRIAL_CAPACITY_MULTIPLIER),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Maximum trials per year possible with trial capacity multiplier",
    display_name="Maximum Trials per Year at Treaty-Scale Trial Capacity",
    unit="trials/year",
    formula="CURRENT_TRIALS × PRAGMATIC_TRIAL_CAPACITY_MULTIPLIER",
    keywords=["pragmatic trials", "real world evidence", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect"],
    inputs=['CURRENT_TRIALS_PER_YEAR', 'DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["CURRENT_TRIALS_PER_YEAR"] * ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"],
    latex_symbol=r"Capacity_{trials}",  # LaTeX symbol for equations
)  # Maximum trials/year possible with trial capacity multiplier

# =============================================================================
# THERAPEUTIC SPACE EXPLORATION TIMELINES
# =============================================================================
# How long to systematically test all therapeutic combinations at current vs treaty-scale capacity

CURRENT_KNOWN_SAFE_EXPLORATION_YEARS = Parameter(
    float(DRUG_DISEASE_COMBINATIONS_POSSIBLE) / float(CURRENT_TRIALS_PER_YEAR),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Years to test all known safe drug-disease combinations at current global trial capacity",
    display_name="Known Safe Exploration Time (Current)",
    unit="years",
    formula="DRUG_DISEASE_COMBINATIONS ÷ CURRENT_TRIALS_PER_YEAR",
    keywords=["exploration", "therapeutic frontier", "timeline", "current pace", "known safe", "years"],
    inputs=["DRUG_DISEASE_COMBINATIONS_POSSIBLE", "CURRENT_TRIALS_PER_YEAR"],
    compute=lambda ctx: ctx["DRUG_DISEASE_COMBINATIONS_POSSIBLE"] / ctx["CURRENT_TRIALS_PER_YEAR"],
    latex_symbol=r"T_{explore,safe}",  # LaTeX symbol for equations
)

DFDA_KNOWN_SAFE_EXPLORATION_YEARS = Parameter(
    float(DRUG_DISEASE_COMBINATIONS_POSSIBLE) / float(DFDA_TRIALS_PER_YEAR_CAPACITY),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Years to test all known safe drug-disease combinations with treaty-scale pragmatic trial capacity",
    display_name="Known Safe Exploration Time at Treaty-Scale Trial Capacity",
    unit="years",
    formula="DRUG_DISEASE_COMBINATIONS ÷ TREATY_SCALE_TRIALS_PER_YEAR",
    keywords=["exploration", "therapeutic frontier", "timeline", "accelerated", "known safe", "years"],
    inputs=["DRUG_DISEASE_COMBINATIONS_POSSIBLE", "DFDA_TRIALS_PER_YEAR_CAPACITY"],
    compute=lambda ctx: ctx["DRUG_DISEASE_COMBINATIONS_POSSIBLE"] / ctx["DFDA_TRIALS_PER_YEAR_CAPACITY"],
    latex_symbol=r"T_{safe,trial}",  # LaTeX symbol for equations
)

CURRENT_TOTAL_EXPLORATION_YEARS = Parameter(
    float(TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS) / float(CURRENT_TRIALS_PER_YEAR),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Years to test all therapeutic combinations (known safe + emerging modalities) at current capacity",
    display_name="Total Exploration Time (Current)",
    unit="years",
    formula="TOTAL_COMBINATIONS ÷ CURRENT_TRIALS_PER_YEAR",
    keywords=["exploration", "total", "all modalities", "timeline", "current pace", "years"],
    inputs=["TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS", "CURRENT_TRIALS_PER_YEAR"],
    compute=lambda ctx: ctx["TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS"] / ctx["CURRENT_TRIALS_PER_YEAR"],
    latex_symbol=r"T_{explore,total}",  # LaTeX symbol for equations
)

DFDA_TOTAL_EXPLORATION_YEARS = Parameter(
    float(TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS) / float(DFDA_TRIALS_PER_YEAR_CAPACITY),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Years to test all therapeutic combinations (known safe + emerging modalities) with treaty-scale pragmatic trial capacity",
    display_name="Total Exploration Time at Treaty-Scale Trial Capacity",
    unit="years",
    formula="TOTAL_COMBINATIONS ÷ TREATY_SCALE_TRIALS_PER_YEAR",
    keywords=["exploration", "total", "all modalities", "timeline", "accelerated", "years"],
    inputs=["TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS", "DFDA_TRIALS_PER_YEAR_CAPACITY"],
    compute=lambda ctx: ctx["TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS"] / ctx["DFDA_TRIALS_PER_YEAR_CAPACITY"],
    latex_symbol=r"T_{explore,trial}",  # LaTeX symbol for equations
)

# Combination therapy exploration (pairwise drug combinations - standard in modern medicine)
CURRENT_COMBINATION_EXPLORATION_YEARS = Parameter(
    float(COMBINATION_THERAPY_DISEASE_SPACE) / float(CURRENT_TRIALS_PER_YEAR),
    manual_ref="knowledge/problem/untapped-therapeutic-frontier.qmd",
    source_type="calculated",
    description="Years to test all pairwise drug combinations at current trial capacity. Combination therapy is standard in oncology, HIV, cardiology.",
    display_name="Combination Therapy Exploration Time (Current)",
    unit="years",
    formula="COMBINATION_SPACE ÷ CURRENT_TRIALS_PER_YEAR",
    keywords=["combination", "exploration", "timeline", "years", "polypharmacy"],
    inputs=["COMBINATION_THERAPY_DISEASE_SPACE", "CURRENT_TRIALS_PER_YEAR"],
    compute=lambda ctx: ctx["COMBINATION_THERAPY_DISEASE_SPACE"] / ctx["CURRENT_TRIALS_PER_YEAR"],
    latex_symbol=r"T_{explore,combo}",  # LaTeX symbol for equations
)

# PMC Systematic Review - Pragmatic Trial Costs
# Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6508852/
# Note: 25% of trials <$19/patient, 10 trials >$1,000/patient
# U.S. median $187, non-U.S. median $27 (2015 USD)
PMC_PRAGMATIC_TRIAL_MEDIAN_COST_PER_PATIENT = Parameter(
    97.0,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref="pmc-pragmatic-trial-cost",
    source_type="external",
    description="Median cost per patient in embedded pragmatic clinical trials (Ramsberg & Platt 2018: 108 trials reviewed, 64 with cost data). IQR: $19-$478 (2015 USD).",
    display_name="Pragmatic Trial Median Cost per Patient (PMC Review)",
    unit="USD/patient",
    confidence="high",
    confidence_interval=(19, 478),  # IQR from the study (2015 USD)
    distribution="lognormal",
    keywords=["$97", "pmc", "pragmatic", "trial cost", "median", "embedded"],
    latex_symbol=r"Cost_{pragmatic,median}",  # LaTeX symbol for equations
)

# (GLOBAL_POPULATION_2024 moved earlier in file for war counterfactual params)

GLOBAL_ANNUAL_SAVINGS_PER_CAPITA = Parameter(
    GLOBAL_ANNUAL_SAVINGS / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Global annual savings divided by global population. Useful as a rough average-person "
                "default for prize-contribution sizing.",
    display_name="Global Annual Savings Per Capita",
    unit="USD/person/year",
    formula="GLOBAL_ANNUAL_SAVINGS / GLOBAL_POPULATION_2024",
    inputs=["GLOBAL_ANNUAL_SAVINGS", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_SAVINGS"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["savings", "per capita", "global", "personal", "default"],
    latex_symbol=r"S_{annual,pc}",
)

POLITICAL_DYSFUNCTION_TAX_PER_PERSON_ANNUAL = Parameter(
    POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    confidence="low",
    description="Annual per-person burden implied by global Political Dysfunction Tax opportunity costs.",
    display_name="Political Dysfunction Tax per Person (Annual)",
    unit="USD/year",
    formula="POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL ÷ GLOBAL_POPULATION_2024",
    inputs=["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: (
        ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"] / ctx["GLOBAL_POPULATION_2024"]
    ),
    keywords=["political dysfunction tax", "per person", "annual", "global"],
    latex_symbol=r"T_{pd,pc}",
)

POLITICAL_DYSFUNCTION_TAX_PER_HOUSEHOLD_OF_FOUR_ANNUAL = Parameter(
    POLITICAL_DYSFUNCTION_TAX_PER_PERSON_ANNUAL * 4,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    confidence="low",
    description="Annual household burden for a 4-person household implied by global Political Dysfunction Tax.",
    display_name="Political Dysfunction Tax per Household of Four (Annual)",
    unit="USD/year",
    formula="POLITICAL_DYSFUNCTION_TAX_PER_PERSON_ANNUAL × 4",
    inputs=["POLITICAL_DYSFUNCTION_TAX_PER_PERSON_ANNUAL"],
    compute=lambda ctx: ctx["POLITICAL_DYSFUNCTION_TAX_PER_PERSON_ANNUAL"] * 4,
    keywords=["political dysfunction tax", "household", "annual", "global"],
    latex_symbol=r"T_{pd,hh4}",
)

# NOTE: Daily deaths (150k/day) defined above as GLOBAL_DISEASE_DEATHS_DAILY (line ~1903)
# Annual disease deaths (from WHO global health estimates)
GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES = Parameter(
    55_000_000,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Annual deaths from all diseases and aging globally",
    display_name="Annual Deaths from All Diseases and Aging Globally",
    unit="deaths/year",
    keywords=["worldwide", "yearly", "fatalities", "casualties"],
    confidence="high",
    distribution="normal",
    std_error=5_000_000,  # ±5M (~10% uncertainty in WHO estimates)
    latex_symbol=r"Deaths_{curable,ann}",  # LaTeX symbol for equations
)  # 55 million deaths/year from WHO (all diseases + aging)

WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS = Parameter(
    WAR_TRIAL_REDIRECT_PLEADING_END_YEAR
    - WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR
    + 1,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Inclusive number of years in the aggressive prosecutor disease-death plaintiff window.",
    display_name="War Trial Redirect Post-Cutoff Disease Years",
    unit="years",
    formula="WAR_TRIAL_REDIRECT_PLEADING_END_YEAR - WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR + 1",
    inputs=["WAR_TRIAL_REDIRECT_PLEADING_END_YEAR", "WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR"],
    compute=lambda ctx: (
        ctx["WAR_TRIAL_REDIRECT_PLEADING_END_YEAR"]
        - ctx["WAR_TRIAL_REDIRECT_DISEASE_PLEADING_CUTOFF_YEAR"]
        + 1
    ),
    keywords=["war", "medical misallocation", "post-cutoff", "years", "prosecutor"],
    latex_symbol=r"T_{post,disease}",
)

WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_YEARS = Parameter(
    WAR_TRIAL_REDIRECT_PLEADING_END_YEAR
    - WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR
    + 1,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Inclusive number of years in the aggressive prosecutor aging-death intake window.",
    display_name="War Trial Redirect Post-Cutoff Aging Years",
    unit="years",
    formula="WAR_TRIAL_REDIRECT_PLEADING_END_YEAR - WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR + 1",
    inputs=["WAR_TRIAL_REDIRECT_PLEADING_END_YEAR", "WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR"],
    compute=lambda ctx: (
        ctx["WAR_TRIAL_REDIRECT_PLEADING_END_YEAR"]
        - ctx["WAR_TRIAL_REDIRECT_AGING_PLEADING_CUTOFF_YEAR"]
        + 1
    ),
    keywords=["war", "medical misallocation", "post-cutoff", "aging", "years", "prosecutor"],
    latex_symbol=r"T_{post,aging}",
)

WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_PLAINTIFFS = Parameter(
    WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS
    * GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES
    * EVENTUALLY_AVOIDABLE_DEATH_PCT,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Aggressive prosecutor pleading count for post-cutoff disease-death plaintiffs: "
                "inclusive years from the disease cutoff through the pleading end year, multiplied "
                "by annual disease deaths and the eventually avoidable death share.",
    display_name="War Trial Redirect Post-Cutoff Disease Plaintiffs",
    unit="plaintiffs",
    formula="WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS * GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES * EVENTUALLY_AVOIDABLE_DEATH_PCT",
    inputs=[
        "WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS",
        "GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES",
        "EVENTUALLY_AVOIDABLE_DEATH_PCT",
    ],
    compute=lambda ctx: (
        ctx["WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS"]
        * ctx["GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES"]
        * ctx["EVENTUALLY_AVOIDABLE_DEATH_PCT"]
    ),
    keywords=["war", "medical misallocation", "plaintiffs", "disease deaths", "prosecutor"],
    latex_symbol=r"N_{plaintiffs,disease}",
)

WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_PLAINTIFFS = Parameter(
    WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_YEARS
    * GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES
    * EVENTUALLY_AVOIDABLE_DEATH_PCT,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Aggressive prosecutor aging intake count after the aging cutoff year. This overlaps "
                "with the broader disease-death plaintiff class because the annual-deaths parameter "
                "covers all disease and aging deaths; it is an intake class, not an additive damages line.",
    display_name="War Trial Redirect Post-Cutoff Aging Plaintiffs",
    unit="plaintiffs",
    formula="WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_YEARS * GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES * EVENTUALLY_AVOIDABLE_DEATH_PCT",
    inputs=[
        "WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_YEARS",
        "GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES",
        "EVENTUALLY_AVOIDABLE_DEATH_PCT",
    ],
    compute=lambda ctx: (
        ctx["WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_YEARS"]
        * ctx["GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES"]
        * ctx["EVENTUALLY_AVOIDABLE_DEATH_PCT"]
    ),
    keywords=["war", "medical misallocation", "aging", "plaintiffs", "prosecutor"],
    latex_symbol=r"N_{plaintiffs,aging}",
)

WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_DALYS = Parameter(
    WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS
    * GLOBAL_ANNUAL_DALY_BURDEN
    * EVENTUALLY_AVOIDABLE_DALY_PCT,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Aggressive prosecutor estimate of post-cutoff avoidable disease DALYs. This measures "
                "disease-years, disability, and suffering after the disease cutoff, separate from the "
                "death-plaintiff VSL count.",
    display_name="War Trial Redirect Post-Cutoff Disease DALYs",
    unit="DALYs",
    formula="WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS * GLOBAL_ANNUAL_DALY_BURDEN * EVENTUALLY_AVOIDABLE_DALY_PCT",
    inputs=[
        "WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS",
        "GLOBAL_ANNUAL_DALY_BURDEN",
        "EVENTUALLY_AVOIDABLE_DALY_PCT",
    ],
    compute=lambda ctx: (
        ctx["WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_YEARS"]
        * ctx["GLOBAL_ANNUAL_DALY_BURDEN"]
        * ctx["EVENTUALLY_AVOIDABLE_DALY_PCT"]
    ),
    keywords=["war", "medical misallocation", "DALYs", "disease years", "suffering", "prosecutor"],
    latex_symbol=r"DALYs_{post,disease}",
)

CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE = Parameter(
    WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_PLAINTIFFS * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Gross pleading exposure for post-cutoff medical misallocation disease plaintiffs "
                "valued at VSL. This is pleading exposure, not a final non-duplicative award.",
    display_name="Corporate Damages Prosecutor Gross Medical Misallocation Exposure",
    unit="USD",
    formula="WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_PLAINTIFFS * VALUE_OF_STATISTICAL_LIFE",
    inputs=["WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_PLAINTIFFS", "VALUE_OF_STATISTICAL_LIFE"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_PLAINTIFFS"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    keywords=["corporate", "damages", "medical misallocation", "gross pleading exposure", "prosecutor"],
    latex_symbol=r"D_{corp,med,gross}",
)

CORPORATE_DAMAGES_PROSECUTOR_GROSS_AGING_INTAKE_EXPOSURE = Parameter(
    WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_PLAINTIFFS * VALUE_OF_STATISTICAL_LIFE,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Gross pleading exposure for the overlapping aging intake class valued at VSL. "
                "Displayed separately because it overlaps with the broader disease-death class.",
    display_name="Corporate Damages Prosecutor Gross Aging Intake Exposure",
    unit="USD",
    formula="WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_PLAINTIFFS * VALUE_OF_STATISTICAL_LIFE",
    inputs=["WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_PLAINTIFFS", "VALUE_OF_STATISTICAL_LIFE"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_POST_CUTOFF_AGING_PLAINTIFFS"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
    keywords=["corporate", "damages", "medical misallocation", "aging", "gross pleading exposure", "prosecutor"],
    latex_symbol=r"D_{corp,aging,gross}",
)

CORPORATE_DAMAGES_PROSECUTOR_GROSS_DISEASE_DALY_EXPOSURE = Parameter(
    WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_DALYS * STANDARD_ECONOMIC_QALY_VALUE_USD,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Gross pleading exposure for post-cutoff disease DALYs valued at the standard QALY "
                "value. This is disease-year and suffering exposure, not a final non-duplicative award.",
    display_name="Corporate Damages Prosecutor Gross Disease DALY Exposure",
    unit="USD",
    formula="WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_DALYS * STANDARD_ECONOMIC_QALY_VALUE_USD",
    inputs=["WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_DALYS", "STANDARD_ECONOMIC_QALY_VALUE_USD"],
    compute=lambda ctx: ctx["WAR_TRIAL_REDIRECT_POST_CUTOFF_DISEASE_DALYS"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    keywords=["corporate", "damages", "medical misallocation", "DALYs", "gross pleading exposure", "prosecutor"],
    latex_symbol=r"D_{corp,DALY,gross}",
)

CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_TOTAL = Parameter(
    CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL
    + CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Aggressive prosecutor gross pleading exposure: strict non-duplicative floor plus "
                "gross medical misallocation exposure. This is gross pleading exposure, not a final award.",
    display_name="Corporate Damages Prosecutor Gross Pleading Exposure Total",
    unit="USD",
    formula="CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL + CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE",
    inputs=[
        "CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL",
        "CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE",
    ],
    compute=lambda ctx: (
        ctx["CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL"]
        + ctx["CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE"]
    ),
    keywords=["corporate", "damages", "gross pleading exposure", "medical misallocation", "prosecutor"],
    latex_symbol=r"D_{corp,plead,gross}",
)

CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_PER_CAPITA = Parameter(
    CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_TOTAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Gross death-based pleading exposure per living human if the judgment were distributed "
                "as universal residual restitution. This is not a final award.",
    display_name="Corporate Damages Prosecutor Gross Pleading Exposure Per Living Human",
    unit="USD/person",
    formula="CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_TOTAL / GLOBAL_POPULATION_2024",
    inputs=["CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_TOTAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["corporate", "damages", "gross pleading exposure", "per capita", "restitution", "prosecutor"],
    latex_symbol=r"D_{corp,plead,gross,pc}",
)

CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_WITH_DALYS = Parameter(
    CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL
    + CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE
    + CORPORATE_DAMAGES_PROSECUTOR_GROSS_DISEASE_DALY_EXPOSURE,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Aggressive prosecutor stacked gross pleading exposure: strict floor plus post-cutoff "
                "disease-death VSL exposure plus post-cutoff disease DALY exposure. This intentionally "
                "shows the full pleading stack and may overlap; it is not a final non-duplicative award.",
    display_name="Corporate Damages Prosecutor Gross Pleading Exposure With DALYs",
    unit="USD",
    formula="CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL + CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE + CORPORATE_DAMAGES_PROSECUTOR_GROSS_DISEASE_DALY_EXPOSURE",
    inputs=[
        "CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL",
        "CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE",
        "CORPORATE_DAMAGES_PROSECUTOR_GROSS_DISEASE_DALY_EXPOSURE",
    ],
    compute=lambda ctx: (
        ctx["CORPORATE_DAMAGES_STRICT_FLOOR_TOTAL"]
        + ctx["CORPORATE_DAMAGES_PROSECUTOR_GROSS_MEDICAL_MISALLOCATION_EXPOSURE"]
        + ctx["CORPORATE_DAMAGES_PROSECUTOR_GROSS_DISEASE_DALY_EXPOSURE"]
    ),
    keywords=["corporate", "damages", "gross pleading exposure", "DALYs", "medical misallocation", "prosecutor"],
    latex_symbol=r"D_{corp,plead,DALY}",
)

CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_WITH_DALYS_PER_CAPITA = Parameter(
    CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_WITH_DALYS / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/humanity-v-government.qmd",
    source_type=SourceType.CALCULATED,
    confidence="low",
    description="Gross stacked pleading exposure per living human if the death and DALY pleading stack "
                "were distributed as universal residual restitution. This is not a final award.",
    display_name="Corporate Damages Prosecutor Gross Pleading Exposure With DALYs Per Living Human",
    unit="USD/person",
    formula="CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_WITH_DALYS / GLOBAL_POPULATION_2024",
    inputs=["CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_WITH_DALYS", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: (
        ctx["CORPORATE_DAMAGES_PROSECUTOR_GROSS_PLEADING_EXPOSURE_WITH_DALYS"]
        / ctx["GLOBAL_POPULATION_2024"]
    ),
    keywords=["corporate", "damages", "gross pleading exposure", "DALYs", "per capita", "restitution"],
    latex_symbol=r"D_{corp,plead,DALY,pc}",
)

# Disease economic burden
GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL = Parameter(
    8_200_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="external",
    description="Annual global spending on symptomatic disease treatment",
    display_name="Annual Global Spending on Symptomatic Disease Treatment",
    unit="USD/year",
    keywords=["8.2t", "deadweight loss", "economic damage", "productivity loss", "gdp loss", "worldwide", "yearly"],
    distribution="lognormal",  # Economic estimates with methodological variance
    confidence_interval=(6_500_000_000_000, 10_000_000_000_000),  # ±20-22%: reflects definitional + accounting differences
    latex_symbol=r"Spending_{symptom}",  # LaTeX symbol for equations
)  # $8.2 trillion annually

# Disease cost breakdown components (standalone market-cost parameters, NOT summed into welfare burden)
GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL = Parameter(
    9_900_000_000_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="external",
    description="Direct medical costs of disease globally (treatment, hospitalization, medication). Standalone market-cost metric; not included in DALY-based welfare burden to avoid double-counting.",
    display_name="Global Annual Direct Medical Costs of Disease",
    unit="USD/year",
    keywords=["9.9t", "medical", "healthcare", "treatment", "hospitalization"],
    distribution="lognormal",
    confidence_interval=(7_000_000_000_000, 14_000_000_000_000),  # ±30% - global healthcare cost estimates vary widely
    latex_symbol=r"Cost_{medical,direct}",  # LaTeX symbol for equations
)  # $9.9 trillion annually

GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL = Parameter(
    5_000_000_000_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="external",
    description="Annual productivity loss from disease globally (absenteeism, reduced output). Standalone market-cost metric; not included in DALY-based welfare burden to avoid double-counting.",
    display_name="Global Annual Productivity Loss from Disease",
    unit="USD/year",
    keywords=["5.0t", "productivity", "lost work", "economic loss", "absenteeism"],
    distribution="lognormal",
    confidence_interval=(3_500_000_000_000, 7_000_000_000_000),  # ±30%
    latex_symbol=r"Loss_{productivity}",  # LaTeX symbol for equations
)  # $5 trillion annually

GLOBAL_DISEASE_TOTAL_MARKET_COST_ANNUAL = Parameter(
    GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL + GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_type="calculated",
    description="Total annual market cost of disease globally: direct medical costs ($9.9T) plus lost productivity from people too sick to work ($5T). This is the cash-cost sum a payer or economy actually bears, distinct from the DALY-based welfare burden, and is deliberately NOT added to that burden to avoid double-counting.",
    display_name="Global Annual Total Market Cost of Disease",
    unit="USD/year",
    formula="GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL + GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL",
    inputs=["GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL", "GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL"],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL"] + ctx["GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL"],
    keywords=["15t", "disease cost", "total", "market cost", "productivity", "direct medical"],
    latex_symbol=r"Cost_{disease,market}",
)  # ~$15 trillion annually

# Annual welfare cost of disease: DALYs × avoidable % × QALY value
# Uses consistent QALY valuation ($150K) matching all other health impact calculations.
# Medical costs and productivity losses are standalone market-cost metrics, NOT summed here,
# because QALY valuation already captures productivity and healthcare welfare losses.
GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL = Parameter(
    float(GLOBAL_ANNUAL_DALY_BURDEN) * float(EVENTUALLY_AVOIDABLE_DALY_PCT) * float(STANDARD_ECONOMIC_QALY_VALUE_USD),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Annual welfare cost of avoidable disease globally. Calculated as global DALY burden × eventually avoidable percentage × standard QALY value ($150K). Uses consistent QALY valuation matching all other health impact calculations. Medical costs and productivity losses are NOT added separately to avoid double-counting (QALY valuation already captures these welfare components).",
    display_name="Annual Welfare Cost of Avoidable Disease",
    unit="USD/year",
    formula="GLOBAL_ANNUAL_DALY_BURDEN × EVENTUALLY_AVOIDABLE_DALY_PCT × STANDARD_ECONOMIC_QALY_VALUE_USD",
    keywords=["400t", "deadweight loss", "economic damage", "welfare", "daly", "qaly", "worldwide", "yearly"],
    inputs=['GLOBAL_ANNUAL_DALY_BURDEN', 'EVENTUALLY_AVOIDABLE_DALY_PCT', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DALY_BURDEN"] * ctx["EVENTUALLY_AVOIDABLE_DALY_PCT"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Burden_{disease}",  # LaTeX symbol for equations
)  # ~$400 trillion annually (2.88B DALYs × 92.6% avoidable × $150K/QALY)

GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL = Parameter(
    GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST + GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total annual welfare cost of war and disease. Disease burden uses DALY-based welfare valuation; war costs use direct + indirect economic costs. Symptomatic treatment costs NOT added separately (already captured in QALY valuation).",
    display_name="Total Annual Cost of War and Disease",
    unit="USD/year",
    formula="WAR_TOTAL_COSTS + DISEASE_WELFARE_BURDEN",
    keywords=["deadweight loss", "economic damage", "productivity loss", "gdp loss", "worldwide", "yearly", "conflict"],
    inputs=['GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST', 'GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] + ctx["GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL"],
    latex_symbol=r"Cost_{health+war}",  # LaTeX symbol for equations
)  # ~$411T = $11.355T (war with externalities) + ~$400T (disease welfare burden)

# Industry profit margin comparisons (Damodaran, NYU Stern, January 2026)
DEFENSE_NET_PROFIT_MARGIN = Parameter(
    0.0499,
    manual_ref="knowledge/appendix/love-letter.qmd",
    source_ref="",
    source_type="external",
    description="Net profit margin for Aerospace/Defense industry (79 firms, Damodaran Jan 2026)",
    display_name="Aerospace/Defense Net Profit Margin",
    unit="percent",
    confidence_interval=(0.040, 0.060),  # year-to-year variation in Damodaran's annual tables
    keywords=["defense", "aerospace", "profit", "margin", "military", "contractor"],
    latex_symbol=r"Margin_{def}",
)

PHARMA_NET_PROFIT_MARGIN = Parameter(
    0.1854,
    manual_ref="knowledge/appendix/love-letter.qmd",
    source_ref="",
    source_type="external",
    description="Net profit margin for Drugs (Pharmaceutical) industry (228 firms, Damodaran Jan 2026)",
    display_name="Pharmaceutical Net Profit Margin",
    unit="percent",
    confidence_interval=(0.15, 0.22),  # year-to-year variation in Damodaran's annual tables
    keywords=["pharma", "pharmaceutical", "biotech", "biotechnology", "profit", "margin", "drug"],
    latex_symbol=r"Margin_{pharma}",
)

PHARMA_VS_DEFENSE_NET_MARGIN_RATIO = Parameter(
    float(PHARMA_NET_PROFIT_MARGIN) / float(DEFENSE_NET_PROFIT_MARGIN),
    manual_ref="knowledge/appendix/love-letter.qmd",
    source_ref="",
    source_type="calculated",
    description="Ratio of pharmaceutical to defense net profit margins",
    display_name="Pharma-to-Defense Net Profit Margin Ratio",
    unit="x",
    keywords=["pharma", "defense", "margin", "ratio", "comparison"],
    formula="PHARMA_NET_PROFIT_MARGIN / DEFENSE_NET_PROFIT_MARGIN",
    inputs=["PHARMA_NET_PROFIT_MARGIN", "DEFENSE_NET_PROFIT_MARGIN"],
    compute=lambda ctx: ctx["PHARMA_NET_PROFIT_MARGIN"] / ctx["DEFENSE_NET_PROFIT_MARGIN"],
    latex_symbol=r"\frac{Margin_{pharma}}{Margin_{def}}",
)

# Defense and research participation rates
DEFENSE_SECTOR_RETENTION_PCT = Parameter(
    0.99,
    manual_ref="knowledge/solution.qmd",
    source_ref="",
    source_type="definition",
    description="Percentage of budget the military sector keeps under 1% treaty",
    display_name="Percentage of Budget Military Sector Keeps Under 1% Treaty",
    unit="rate",
    keywords=["99%", "armed forces", "international agreement", "peace treaty", "conflict", "sector", "retention"],
    latex_symbol=r"Retain_{def}",  # LaTeX symbol for equations
)  # 99% retention

CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE = Parameter(
    0.0006,
    manual_ref="knowledge/solution/dfda.qmd",
    source_ref=ReferenceID.CLINICAL_TRIAL_PATIENT_PARTICIPATION_RATE,
    source_type="external",
    description="Current clinical trial participation rate (0.06% of population)",
    display_name="Current Clinical Trial Participation Rate",
    unit="rate",
    keywords=["0%", "rct", "people", "clinical study", "clinical trial", "research trial", "randomized controlled trial"],
    latex_symbol=r"Rate_{part,curr}",  # LaTeX symbol for equations
)  # 0.06% participation

PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT = Parameter(
    0.448,
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_ref=ReferenceID.PATIENT_WILLINGNESS_CLINICAL_TRIALS,
    source_type="external",
    description="Patient willingness to participate in drug trials (44.8% in surveys, 88% when actually approached)",
    display_name="Patient Willingness to Participate in Clinical Trials",
    unit="percentage",
    confidence="medium",
    keywords=["willingness", "willing", "volunteer", "interest", "clinical trial", "participation", "survey"],
    distribution="normal",
    confidence_interval=(0.40, 0.50),  # ±11% variation from survey heterogeneity
    std_error=0.025,  # Survey response variance across populations
    latex_symbol=r"Pct_{willing}",  # LaTeX symbol for equations
)  # 44.8% willing for drug trials specifically

WILLING_TRIAL_PARTICIPANTS_GLOBAL = Parameter(
    CURRENT_DISEASE_PATIENTS_GLOBAL * PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Global chronic disease patients willing to participate in trials (2.4B × 44.8%)",
    display_name="Global Patients Willing to Participate in Clinical Trials",
    unit="people",
    formula="CURRENT_DISEASE_PATIENTS_GLOBAL × PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT",    confidence="medium",
    keywords=["willing", "volunteer", "participants", "chronic disease", "trial capacity", "1.075b", "1.1b"],
    inputs=['CURRENT_DISEASE_PATIENTS_GLOBAL', 'PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT'],
    compute=lambda ctx: ctx["CURRENT_DISEASE_PATIENTS_GLOBAL"] * ctx["PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT"],
    latex_symbol=r"N_{willing}",  # LaTeX symbol for equations
)  # 1.075 billion willing participants

DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL = Parameter(
    WILLING_TRIAL_PARTICIPANTS_GLOBAL / CURRENT_TRIAL_SLOTS_AVAILABLE,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Physical upper bound on trial-capacity multiplier from participant availability. "
                "Even with unlimited funding, annual trial enrollment cannot exceed willing participant pool.",
    display_name="Maximum Trial Capacity Multiplier (Physical Limit)",
    unit="x",
    formula="WILLING_TRIAL_PARTICIPANTS_GLOBAL ÷ CURRENT_TRIAL_SLOTS_AVAILABLE",
    confidence="medium",
    keywords=["trial capacity", "physical limit", "participants", "upper bound", "dfda"],
    inputs=["WILLING_TRIAL_PARTICIPANTS_GLOBAL", "CURRENT_TRIAL_SLOTS_AVAILABLE"],
    compute=lambda ctx: ctx["WILLING_TRIAL_PARTICIPANTS_GLOBAL"] / ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"],
    latex_symbol=r"k_{capacity,max}",
)  # ~568x absolute cap from willing participants


US_MILITARY_SPENDING_PCT_GDP = Parameter(
    0.035,
    manual_ref="knowledge/problem.qmd",
    source_ref=ReferenceID.US_MILITARY_BUDGET_3_5_PCT_GDP,
    source_type="external",
    description="US military spending as percentage of GDP (2024)",
    display_name="US Military Spending as Percentage of GDP",
    unit="rate",
    keywords=["4%", "dod", "pentagon", "national security", "army", "navy", "armed forces"],
    latex_symbol=r"Pct_{mil,GDP}",  # LaTeX symbol for equations
)  # 3.5% of GDP

# Historical terrorism deaths
TERRORISM_DEATHS_911 = Parameter(
    2996,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.CHANCE_OF_DYING_FROM_TERRORISM_1_IN_30M,
    source_type="external",
    description="Deaths from 9/11 terrorist attacks",
    display_name="Deaths from 9/11 Terrorist Attacks",
    unit="deaths",
    keywords=["911", "3k", "fatalities", "casualties", "mortality", "terrorism", "loss of life"],
    confidence="high",
    distribution="fixed",  # Historical fact, no uncertainty
    latex_symbol=r"Deaths_{9/11}",  # LaTeX symbol for equations
)  # 2,996 deaths

# Research acceleration multipliers
# Calculated ratios and comparisons
DISEASE_VS_TERRORISM_DEATHS_RATIO = Parameter(
    GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES / TERRORISM_DEATHS_911,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Ratio of annual disease deaths to 9/11 terrorism deaths",
    display_name="Ratio of Annual Disease Deaths to 9/11 Terrorism Deaths",
    unit="ratio",
    formula="ANNUAL_DISEASE_DEATHS ÷ 911_DEATHS",
    keywords=["fatalities", "casualties", "illness", "mortality", "worldwide", "yearly", "disease"],
    inputs=["GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES", "TERRORISM_DEATHS_911"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES"] / ctx["TERRORISM_DEATHS_911"],
    latex_symbol=r"Ratio_{dis:terror}",  # LaTeX symbol for equations
)  # ~18,274:1

DISEASE_VS_WAR_DEATHS_RATIO = Parameter(
    GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Ratio of annual disease deaths to war deaths",
    display_name="Ratio of Annual Disease Deaths to War Deaths",
    unit="ratio",
    formula="ANNUAL_DISEASE_DEATHS ÷ WAR_DEATHS",
    keywords=["armed forces", "conflict", "fatalities", "casualties", "illness", "mortality", "worldwide"],
    inputs=["GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES", "GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES"] / ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL"],
    latex_symbol=r"Ratio_{dis:war}",  # LaTeX symbol for equations
)  # ~137:1

# Medical research as percentage of disease burden
MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN = Parameter(
    GLOBAL_MED_RESEARCH_SPENDING / GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Medical research spending as percentage of total disease burden",
    display_name="Medical Research Spending as Percentage of Total Disease Burden",
    unit="rate",
    formula="MED_RESEARCH ÷ TOTAL_BURDEN",
    keywords=["deadweight loss", "economic damage", "productivity loss", "gdp loss", "investigation", "r&d", "science"],
    inputs=['GLOBAL_MED_RESEARCH_SPENDING', 'GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL'],
    compute=lambda ctx: ctx["GLOBAL_MED_RESEARCH_SPENDING"] / ctx["GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL"],
    latex_symbol=r"Pct_{RD:burden}",  # LaTeX symbol for equations
)  # 0.052%

# Per capita calculations
GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/problem.qmd",
    source_type="calculated",
    description="Per capita military spending globally",
    display_name="Per Capita Military Spending Globally",
    unit="USD/person/year",
    formula="MILITARY_SPENDING ÷ POPULATION",
    keywords=["dod", "pentagon", "average person", "national security", "army", "individual", "navy"],
    inputs=['GLOBAL_MILITARY_SPENDING_ANNUAL_2024', 'GLOBAL_POPULATION_2024'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_POPULATION_2024"],
    latex_symbol=r"Spending_{mil,pc}",  # LaTeX symbol for equations
)  # $340/person/year

# GiveWell charity comparison
# Source: knowledge/appendix/icer-full-calculation.qmd
GIVEWELL_COST_PER_LIFE_MIN = Parameter(
    3500,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="GiveWell cost per life saved (Helen Keller International)",
    display_name="Givewell Cost per Life Saved (Minimum)",
    unit="USD/life",
    keywords=["4k", "costs", "funding", "investment", "givewell", "life", "min"],
    latex_symbol=r"Cost_{GW,min}",  # LaTeX symbol for equations
)  # Helen Keller International Vitamin A

GIVEWELL_COST_PER_LIFE_MAX = Parameter(
    5500,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="GiveWell cost per life saved (Against Malaria Foundation)",
    display_name="Givewell Cost per Life Saved (Maximum)",
    unit="USD/life",
    keywords=["6k", "costs", "funding", "investment", "givewell", "life", "max"],
    latex_symbol=r"Cost_{GW,max}",  # LaTeX symbol for equations
)  # Against Malaria Foundation

GIVEWELL_COST_PER_LIFE_AVG = Parameter(
    4500,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="Midpoint of GiveWell's cited $3,500 to $5,500 modeled cost-per-life-saved range across top charities",
    display_name="GiveWell Midpoint of Modeled Cost per Life Saved Range",
    unit="USD/life",
    distribution="fixed",
    keywords=["4k", "costs", "funding", "investment", "givewell", "life", "avg"],
    latex_symbol=r"Cost_{GW,avg}",  # LaTeX symbol for equations
)  # Midpoint of cited $3,500 to $5,500 range

# Historical public health comparisons
SMALLPOX_ERADICATION_ROI = Parameter(
    280,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.SMALLPOX_ERADICATION_ROI,
    source_type="external",
    description="Return on investment from smallpox eradication campaign",
    display_name="Return on Investment from Smallpox Eradication Campaign",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"],
    latex_symbol=r"ROI_{smallpox}",  # LaTeX symbol for equations
)  # 159:1 to 280:1 estimated

CHILDHOOD_VACCINATION_ROI = Parameter(
    13,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.CHILDHOOD_VACCINATION_ROI,
    source_type="external",
    description="Return on investment from childhood vaccination programs",
    display_name="Return on Investment from Childhood Vaccination Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"],
    latex_symbol=r"ROI_{vax}",  # LaTeX symbol for equations
)  # 13:1

POLIO_VACCINATION_ROI = Parameter(
    39,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.POLIO_VACCINATION_ROI,
    source_type="external",
    description="Return on investment from sustaining polio vaccination assets and integrating into expanded immunization programs",
    display_name="Return on Investment from Sustaining Polio Vaccination Assets and Integrating into Expanded Immunization Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"],
    latex_symbol=r"ROI_{polio}",  # LaTeX symbol for equations
)  # 39:1 (WHO 2019, 8 priority countries)

MEASLES_VACCINATION_ROI = Parameter(
    14,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.MEASLES_VACCINATION_ROI,
    source_type="external",
    description="Return on investment from measles (MMR) vaccination programs",
    display_name="Return on Investment from Measles Vaccination Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"],
    latex_symbol=r"ROI_{measles}",  # LaTeX symbol for equations
)  # 14:1 (MMR), range: 10.3:1 to 167:1 depending on program type

CHILDHOOD_VACCINATION_ANNUAL_BENEFIT = Parameter(
    15_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="childhood-vaccination-economic-benefits",  # Will use ReferenceID enum after regeneration
    source_type="external",
    description="Estimated annual global economic benefit from childhood vaccination programs (measles, polio, etc.)",
    display_name="Estimated Annual Global Economic Benefit from Childhood Vaccination Programs",
    unit="USD/year",
    keywords=["15.0b", "yearly", "profit", "return", "worldwide", "childhood", "vaccination"],
    distribution="lognormal",  # Economic benefit estimates with methodological variance
    std_error=4_500_000_000,  # ±30%: reflects program-specific and valuation methodology differences
    latex_symbol=r"Benefit_{vax,ann}",  # LaTeX symbol for equations
)  # ~$15B annual benefit from preventing measles, polio, etc.

WATER_FLUORIDATION_ROI = Parameter(
    23,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.CLEAN_WATER_SANITATION_ROI,
    source_type="external",
    description="Return on investment from water fluoridation programs",
    display_name="Return on Investment from Water Fluoridation Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"],
    latex_symbol=r"ROI_{fluoride}",  # LaTeX symbol for equations
)  # 23:1

# Historical intervention total benefits (for comparison charts)

SMALLPOX_ERADICATION_TOTAL_BENEFIT = Parameter(
    1_420_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.SMALLPOX_ERADICATION_ROI,
    source_type="external",
    description="Total economic benefit from smallpox eradication campaign",
    display_name="Total Economic Benefit from Smallpox Eradication Campaign",
    unit="USD",
    keywords=["historical", "one-time", "total benefit", "eradication", "public health"],
    latex_symbol=r"Benefit_{smallpox}",  # LaTeX symbol for equations
)  # $1.42B total benefit ($350M + $1,070M benefits, $298M cost, ~159-280:1 ROI)

HUMAN_GENOME_PROJECT_TOTAL_ECONOMIC_IMPACT = Parameter(
    1_000_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.HUMAN_GENOME_AND_GENETIC_EDITING,
    source_type="external",
    description="Estimated total economic impact of Human Genome Project",
    display_name="Estimated Total Economic Impact of Human Genome Project",
    unit="USD",
    keywords=["historical", "one-time", "total benefit", "genomics", "research"],
    latex_symbol=r"Impact_{HGP}",  # LaTeX symbol for equations
)  # ~$1T commonly cited economic impact estimate (cost ~$2.7B)

# Annual benefit parameters (used for 100-year cumulative comparisons)

WATER_FLUORIDATION_ANNUAL_BENEFIT = Parameter(
    800_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.CLEAN_WATER_SANITATION_ROI,
    source_type="external",
    description="Estimated annual global economic benefit from water fluoridation programs",
    display_name="Estimated Annual Global Economic Benefit from Water Fluoridation Programs",
    unit="USD/year",
    keywords=["yearly", "profit", "return", "worldwide", "fluoridation", "dental"],
    latex_symbol=r"Benefit_{fluoride}",  # LaTeX symbol for equations
)  # ~$800M annual benefit

SMOKING_CESSATION_ANNUAL_BENEFIT = Parameter(
    12_000_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="life-expectancy-gains-smoking-reduction",
    source_type="external",
    description="Estimated annual global economic benefit from smoking cessation programs",
    display_name="Estimated Annual Global Economic Benefit from Smoking Cessation Programs",
    unit="USD/year",
    keywords=["yearly", "profit", "return", "worldwide", "tobacco", "smoking"],
    latex_symbol=r"Benefit_{smoking}",  # LaTeX symbol for equations
)  # ~$12B annual benefit


# Three-tier ROI analysis based on TOTAL one-time health benefits
TREATY_ROI_EXISTING_DRUGS_ONLY = Parameter(
    EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS / TREATY_CAMPAIGN_TOTAL_COST,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Treaty ROI based on historical rate of drug development (existing drugs only). Total one-time benefit from avoiding regulatory delay for drugs already in development divided by campaign cost. Excludes future innovation effects.",
    display_name="Treaty ROI - Historical Rate (Existing Drugs)",
    unit="ratio",
    formula="HISTORICAL_PROGRESS_TOTAL ÷ CAMPAIGN_COST",
    confidence="high",
    keywords=["250920", "historical", "existing drugs", "roi"],
    inputs=['EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS', 'TREATY_CAMPAIGN_TOTAL_COST'],
    compute=lambda ctx: ctx["EXISTING_DRUGS_EFFICACY_LAG_ECONOMIC_LOSS"] / ctx["TREATY_CAMPAIGN_TOTAL_COST"],
    latex_symbol=r"ROI_{drugs}",  # LaTeX symbol for equations
)  # 250,920:1 ROI (existing drugs only)

TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG = Parameter(
    DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE / TREATY_CAMPAIGN_TOTAL_COST,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Treaty ROI from elimination of efficacy lag plus earlier treatment discovery from increased trial throughput. Total one-time benefit divided by campaign cost. This is the primary ROI estimate for total health benefits.",
    display_name="Treaty ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput",
    unit="ratio",
    formula="TOTAL_TIMELINE_SHIFT_ECONOMIC_VALUE ÷ CAMPAIGN_COST",
    confidence="medium",
    keywords=["trial capacity", "efficacy lag", "primary", "timeline shift", "roi"],
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE", "TREATY_CAMPAIGN_TOTAL_COST"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE"] / ctx["TREATY_CAMPAIGN_TOTAL_COST"],
    latex_symbol=r"ROI_{max}",  # LaTeX symbol for equations
)

# ---
# EXPECTED ROI WITH POLITICAL UNCERTAINTY
# ---

# Expected ROI accounting for political implementation uncertainty
# Uses the uncertain POLITICAL_SUCCESS_PROBABILITY - Monte Carlo will sample the full distribution
TREATY_EXPECTED_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG = Parameter(
    float(TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG) * float(POLITICAL_SUCCESS_PROBABILITY),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="calculated",
    source_type="calculated",
    description="Expected ROI for 1% treaty accounting for political success probability uncertainty. "
                "Monte Carlo samples POLITICAL_SUCCESS_PROBABILITY from beta(0.1%, 10%) distribution "
                "to generate full expected value distribution. Central value uses 1% probability.",
    display_name="Expected Treaty ROI (Risk-Adjusted)",
    unit="ratio",
    formula="TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG × POLITICAL_SUCCESS_PROBABILITY",
    confidence="low",
    keywords=["expected value", "risk-adjusted", "political risk", "bcr", "benefit cost ratio",
              "economic return", "uncertainty", "monte carlo"],
    inputs=["TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG", "POLITICAL_SUCCESS_PROBABILITY"],
    compute=lambda ctx: ctx["TREATY_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG"] * ctx["POLITICAL_SUCCESS_PROBABILITY"],
    latex_symbol=r"E[ROI_{max}]",  # LaTeX symbol for equations
)

# Scale Comparison Parameters (demonstrating intervention magnitude)
# DELETED: OPPORTUNITY_COST_PER_DAY and OPPORTUNITY_COST_PER_SECOND
# Reason: These parameters were conceptually confused. They calculated the daily cost by dividing
# DFDA_EFFICACY_LAG_ELIMINATION_ECONOMIC_VALUE by 8.2 years, but that $529T was itself derived from
# daily disease burden × 8.2 years, making the calculation circular. The daily disease burden
# should be calculated directly from GLOBAL_DISEASE_DEATHS_DAILY (150,000 deaths/day)
# rather than through this circular division.

# ---
# SCENARIO PARAMETERS
# ---

GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024 = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * (1 - TREATY_REDUCTION_PCT),
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_type="calculated",  # Derived from military spending and treaty reduction percentage
    description="Global military spending after 1% treaty reduction",
    display_name="Global Military Spending After 1% Treaty Reduction",
    unit="USD/year",
    formula="MILITARY_SPENDING × (1 - REDUCTION)",
    keywords=["2024", "dod", "pentagon", "deployment rate", "market penetration", "participation rate", "national security"],
    inputs=['GLOBAL_MILITARY_SPENDING_ANNUAL_2024', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] * (1 - ctx["TREATY_REDUCTION_PCT"]),
    latex_symbol=r"Spending_{mil,post}",  # LaTeX symbol for equations
)  # $2,690.82B


DRUG_DISCOVERY_TO_APPROVAL_YEARS = Parameter(
    14,
    manual_ref="knowledge/problem.qmd",
    source_ref=ReferenceID.BIO_CLINICAL_DEVELOPMENT_2021,
    source_type="external",
    description="Full drug development timeline from discovery to FDA approval. Typical range is 12-15 years based on BIO 2021 and PMC meta-analyses. Breakdown: preclinical 4-6 years + clinical 10.5 years. Using 14 years as central estimate.",
    display_name="Drug Discovery to Approval Timeline",
    unit="years",
    std_error=1.5,
    confidence_interval=(12, 17),
    keywords=["drug discovery", "full timeline", "preclinical", "clinical", "fda approval", "development time", "innovation lag"],
    latex_symbol=r"T_{discovery}",
)

# ============================================================================
# REGULATORY MORTALITY COST PARAMETERS
# ============================================================================
# Quantitative analysis of Type II regulatory errors (delayed access)
# Based on: "The Human Cost of Regulatory Latency" (2025)
# See: knowledge/appendix/invisible-graveyard.qmd

# Drug Development Phase Durations
PHASE_1_SAFETY_DURATION_YEARS = Parameter(
    2.3,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.BIO_CLINICAL_DEVELOPMENT_2021,
    source_type="external",
    description="Phase I safety trial duration",
    display_name="Phase I Safety Trial Duration",
    unit="years",
    confidence="high",
    last_updated="2021",
    peer_reviewed=True,
    keywords=["rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "study", "discovery"],
    latex_symbol=r"T_{P1}",  # LaTeX symbol for equations
)

# Baseline Lives Saved by Modern Medicine
BASELINE_LIVES_SAVED_ANNUAL = Parameter(
    12.0,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Baseline annual lives saved by pharmaceuticals (conservative aggregate)",
    display_name="Baseline Annual Lives Saved by Pharmaceuticals",
    unit="deaths/year",
    confidence="medium",
    last_updated="2024",
    peer_reviewed=True,
    conservative=True,
    keywords=["deaths prevented", "life saving", "mortality reduction", "deaths averted", "low estimate", "yearly", "cautious"],
    latex_symbol=r"Lives_{base,ann}",  # LaTeX symbol for equations
)

# ---
# COMPREHENSIVE ROI CALCULATIONS WITH REGULATORY DELAY AVOIDANCE
# ---

# Tier 2: Recommended - R&D plus regulatory delay elimination (D_lag only, avoids double-counting)
# DELETED: Obsolete 3-tier ROI parameters
# These parameters were part of the old RD/DELAY/INNOVATION 3-tier structure.
# Now using simplified disease eradication delay model with PRIMARY estimate only.

# ---
# ROI HIERARCHY FOR DIFFERENT AUDIENCES
# ---
# Self-documenting parameter names clarify exactly what's included:
#
# - DFDA_ROI_RD_ONLY (637:1):
#   R&D cost savings only (NPV-adjusted, 10-year timeframe)
#   Most conservative estimate
#
# - DFDA_ROI_RD_PLUS_DELAY (6,489:1): **RECOMMENDED**
#   R&D savings + regulatory delay elimination (D_lag only)
#   Avoids double-counting with innovation loss estimates
#   Uses rigorous DALY-based regulatory mortality analysis
#   Most defensible figure for balanced presentations
#
# - DFDA_ROI_RD_PLUS_DELAY_PLUS_INNOVATION (11,540:1):
#   R&D savings + delay elimination + lost innovation (D_lag + D_void)
#   Full impact estimate, consolidates overlapping benefit categories
#   Use cautiously, appropriate for comprehensive/academic analyses
#
# Usage guidelines:
# - Skeptical audiences / conservative pitches: DFDA_ROI_RD_ONLY (637:1)
# - Balanced presentations / general use: DFDA_ROI_RD_PLUS_DELAY (6,489:1) **RECOMMENDED**
# - Academic/comprehensive analyses: Show full range 637:1 to 11,540:1
# - Advocacy (use cautiously): DFDA_ROI_RD_PLUS_DELAY_PLUS_INNOVATION (11,540:1)


# Cost per DALY benchmarks for comparison
BED_NETS_COST_PER_DALY = Parameter(
    89,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    peer_reviewed=True,  # GiveWell synthesizes peer-reviewed research and undergoes extensive expert review
    description="GiveWell cost per DALY for insecticide-treated bed nets (midpoint estimate, range $78-100). DALYs (Disability-Adjusted Life Years) measure disease burden by combining years of life lost and years lived with disability. Bed nets prevent malaria deaths and are considered a gold standard benchmark for cost-effective global health interventions - if an intervention costs less per DALY than bed nets, it's exceptionally cost-effective. GiveWell synthesizes peer-reviewed academic research with transparent, rigorous methodology and extensive external expert review.",
    display_name="Bed Nets Cost per DALY",
    unit="USD/DALY",
    confidence="high",
    keywords=["givewell", "bed nets", "malaria", "cost effectiveness", "benchmark", "comparison"],
    distribution="normal",  # Well-studied intervention with systematic cost tracking
    confidence_interval=(78, 100),  # Documented GiveWell range
    latex_symbol=r"Cost_{nets}",  # LaTeX symbol for equations
)

DEWORMING_COST_PER_DALY = Parameter(
    55,  # Midpoint of $28-82 range from GiveWell 2011 analysis
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.DEWORMING_COST_PER_DALY,
    source_type="external",
    description="Cost per DALY for deworming programs (range $28-82, midpoint estimate). GiveWell notes this 2011 estimate is outdated and their current methodology focuses on long-term income effects rather than short-term health DALYs.",
    display_name="Deworming Cost per DALY",
    unit="USD/DALY",
    confidence="low",
    keywords=["givewell", "deworming", "worms", "cost effectiveness", "benchmark", "comparison", "soil-transmitted helminths", "schistosomiasis"],
    latex_symbol=r"Cost_{deworm,DALY}",  # LaTeX symbol for equations
)

VITAMIN_A_COST_PER_DALY = Parameter(
    37,  # Midpoint of $23-50 India estimate (most conservative published estimate)
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.VITAMIN_A_COST_PER_DALY,
    source_type="external",
    description="Cost per DALY for vitamin A supplementation programs (India: $23-50; Africa: $40-255; wide variation by region and baseline VAD prevalence). Using India midpoint as conservative estimate.",
    display_name="Vitamin A Supplementation Cost per DALY",
    unit="USD/DALY",
    confidence="medium",
    keywords=["givewell", "vitamin a", "helen keller", "cost effectiveness", "benchmark", "comparison", "supplementation", "micronutrient"],
    latex_symbol=r"Cost_{vitA,DALY}",  # LaTeX symbol for equations
)

CHILDHOOD_VACCINATION_COST_PER_DALY = Parameter(
    30,  # Estimated from ROI and benefit parameters; US studies use QALYs not DALYs
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref="childhood-vaccination-roi",
    source_type="definition",
    description="Estimated cost per DALY for US childhood vaccination programs. Note: US cost-effectiveness studies primarily use cost per QALY (Quality-Adjusted Life Year) rather than cost per DALY. This estimate is derived from program costs and benefits for comparison purposes only.",
    display_name="Childhood Vaccination Cost per DALY (Estimated)",
    unit="USD/DALY",
    confidence="low",
    keywords=["vaccination", "immunization", "childhood", "cost effectiveness", "benchmark", "comparison", "vaccines for children", "VFC"],
    latex_symbol=r"Cost_{vax,DALY}",  # LaTeX symbol for equations
)

# ---
# NIH vs PRAGMATIC TRIAL COST-EFFECTIVENESS COMPARISON
# ---
# These compare the efficiency of standard NIH-funded research vs pragmatic trials like RECOVERY

# RECOVERY trial component parameters for calculating cost per QALY
RECOVERY_TRIAL_TOTAL_COST = Parameter(
    20_000_000,  # ~$20M total trial cost (£20M, ~$20M USD)
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="external",
    description="Total cost of UK RECOVERY trial. Enrolled tens of thousands of patients across "
                "multiple treatment arms. Discovered dexamethasone reduces COVID mortality by ~1/3 in severe cases.",
    display_name="RECOVERY Trial Total Cost",
    unit="USD",
    confidence="high",
    confidence_interval=(15_000_000, 25_000_000),  # Accounting for currency conversion uncertainty
    distribution=DistributionType.LOGNORMAL,
    keywords=["recovery", "trial", "cost", "total", "uk", "pragmatic"],
    latex_symbol=r"Cost_{RECOVERY}",  # LaTeX symbol for equations
)

RECOVERY_TRIAL_GLOBAL_LIVES_SAVED = Parameter(
    1_000_000,  # ~1 million lives saved globally from dexamethasone adoption (NHS England, March 2021)
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_ref=ReferenceID.RECOVERY_TRIAL_1M_LIVES_SAVED,
    source_type="external",
    description="Estimated lives saved globally by RECOVERY trial's dexamethasone discovery. "
                "NHS England estimate (March 2021). Based on Águas et al. Nature Communications 2021 "
                "methodology applying RECOVERY trial mortality reductions (36% ventilated, 18% oxygen) "
                "to global COVID hospitalizations. Wide uncertainty range reflects extrapolation assumptions.",
    display_name="RECOVERY Trial Global Lives Saved",
    unit="lives",
    confidence="medium",
    confidence_interval=(500_000, 2_000_000),  # Águas et al. reported 240K-1.4M for 6 months; extrapolated
    distribution=DistributionType.LOGNORMAL,
    keywords=["recovery", "lives", "saved", "dexamethasone", "global", "impact", "nhs england"],
    latex_symbol=r"Lives_{RECOVERY}",  # LaTeX symbol for equations
)

QALYS_PER_COVID_DEATH_AVERTED = Parameter(
    5,  # Conservative: COVID deaths skewed toward elderly, so fewer remaining life-years
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="definition",
    description="Average QALYs gained per COVID death averted. Conservative estimate reflecting "
                "older age distribution of COVID mortality. See confidence_interval for range.",
    display_name="QALYs per COVID Death Averted",
    unit="QALYs/death",
    confidence="low",
    confidence_interval=(3, 10),  # Lower for elderly, higher if including long COVID prevention
    distribution=DistributionType.LOGNORMAL,
    keywords=["qaly", "covid", "death", "averted", "life years"],
    latex_symbol=r"QALY_{COVID}",  # LaTeX symbol for equations
)

RECOVERY_TRIAL_TOTAL_QALYS_GENERATED = Parameter(
    RECOVERY_TRIAL_GLOBAL_LIVES_SAVED * QALYS_PER_COVID_DEATH_AVERTED,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Total QALYs generated by RECOVERY trial's discoveries (lives saved × QALYs per life). "
                "Uses global impact methodology: counts all downstream health gains from the discovery.",
    display_name="RECOVERY Trial Total QALYs Generated",
    unit="QALYs",
    formula="LIVES_SAVED × QALYS_PER_DEATH_AVERTED",
    confidence="medium",
    keywords=["recovery", "qalys", "total", "generated", "global"],
    inputs=["RECOVERY_TRIAL_GLOBAL_LIVES_SAVED", "QALYS_PER_COVID_DEATH_AVERTED"],
    compute=lambda ctx: ctx["RECOVERY_TRIAL_GLOBAL_LIVES_SAVED"] * ctx["QALYS_PER_COVID_DEATH_AVERTED"],
    latex_symbol=r"QALY_{RECOVERY}",  # LaTeX symbol for equations
)  # ~5 million QALYs

NIH_STANDARD_RESEARCH_COST_PER_QALY = Parameter(
    50_000,  # Midpoint of $20,000-$100,000 range
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.STANDARD_MEDICAL_RESEARCH_ROI,
    source_type="external",
    description="Typical cost per QALY for standard NIH-funded medical research portfolio. "
                "Reflects the inefficiency of traditional RCTs and basic research-heavy allocation. "
                "See confidence_interval for range; ICER uses higher thresholds for value-based pricing.",
    display_name="NIH Standard Research Cost per QALY",
    unit="USD/QALY",
    confidence="medium",
    confidence_interval=(20_000, 100_000),
    distribution=DistributionType.LOGNORMAL,
    keywords=["nih", "research", "cost effectiveness", "qaly", "standard", "traditional", "rct"],
    latex_symbol=r"Cost_{NIH,QALY}",  # LaTeX symbol for equations
)

PRAGMATIC_TRIAL_COST_PER_QALY = Parameter(
    RECOVERY_TRIAL_TOTAL_COST / RECOVERY_TRIAL_TOTAL_QALYS_GENERATED,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="calculated",
    description="Cost per QALY for pragmatic platform trials, calculated from RECOVERY trial data. "
                "Uses global impact methodology: trial cost divided by total QALYs from downstream adoption. "
                "This measures research efficiency (discovery value), not clinical intervention ICER.",
    display_name="Pragmatic Trial Cost per QALY (RECOVERY)",
    unit="USD/QALY",
    formula="TRIAL_COST ÷ TOTAL_QALYS_GENERATED",
    confidence="medium",
    keywords=["pragmatic", "recovery", "trial", "cost effectiveness", "qaly", "efficient", "platform", "global impact"],
    inputs=["RECOVERY_TRIAL_TOTAL_COST", "RECOVERY_TRIAL_TOTAL_QALYS_GENERATED"],
    compute=lambda ctx: ctx["RECOVERY_TRIAL_TOTAL_COST"] / ctx["RECOVERY_TRIAL_TOTAL_QALYS_GENERATED"],
    latex_symbol=r"Cost_{pragmatic,QALY}",  # LaTeX symbol for equations
)  # ~$4/QALY (global impact methodology)

NIH_TRADITIONAL_TRIAL_MAX_EFFICIENCY_PCT = Parameter(
    DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT / TRADITIONAL_PHASE3_COST_PER_PATIENT,
    manual_ref="knowledge/problem/nih-fails-2-institute-health.qmd",
    source_type="calculated",
    description="Maximum efficiency of NIH traditional Phase 3 trials relative to pragmatic trials, "
                "expressed as a percentage. Calculated as pragmatic cost / traditional cost. "
                "This is a CEILING on NIH trial efficiency because: (1) only 3.3% of NIH budget goes to "
                "clinical trials at all, and (2) the other 96.7% funds basic research with far lower "
                "marginal value when thousands of safe compounds already await testing.",
    display_name="NIH Traditional Trial Maximum Efficiency vs Pragmatic (%)",
    unit="percent",
    formula="PRAGMATIC_TRIAL_COST ÷ TRADITIONAL_PHASE3_COST",
    confidence="medium",
    keywords=["efficiency", "traditional", "pragmatic", "nih", "comparison", "cost", "ceiling", "maximum"],
    inputs=["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT", "TRADITIONAL_PHASE3_COST_PER_PATIENT"],
    compute=lambda ctx: ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"] / ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"],
    latex_symbol=r"\eta_{NIH,max}",
)  # ~2.3%, ceiling because 96.7% of NIH budget isn't even spent on trials

# Cost per DALY - Primary cost-effectiveness metric
# Note: ICER (Incremental Cost-Effectiveness Ratio) is not calculated because this is a
# cost-dominant intervention that saves money while improving health. Traditional ICER
# is designed for interventions that cost money, not those that generate net economic surplus.
# Instead, we calculate cost per DALY using only the campaign cost, which understates the
# value since it ignores the $77B/year in economic benefits (R&D savings + peace dividend).

TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG = Parameter(
    TREATY_CAMPAIGN_TOTAL_COST / DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Cost per DALY averted from elimination of efficacy lag plus earlier treatment discovery from increased trial throughput. Only counts campaign cost; ignores economic benefits from funding and R&D savings.",
    display_name="Cost per DALY Averted (Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput)",
    unit="USD/DALY",
    formula="CAMPAIGN_COST ÷ DALYS_TIMELINE_SHIFT",
    confidence="high",
    keywords=["bang for buck", "cost effectiveness", "value for money", "disease burden", "cost per daly", "givewell"],
    inputs=["TREATY_CAMPAIGN_TOTAL_COST", "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_TOTAL_COST"] / ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"],
    latex_symbol=r"Cost_{treaty,DALY}",  # LaTeX symbol for equations
)  # Cost per DALY using full timeline shift

# Expected cost per DALY using the unified political success probability
# The "conservative" label is retained for compatibility, but uses the unified parameter
TREATY_EXPECTED_COST_PER_DALY = Parameter(
    TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG / POLITICAL_SUCCESS_PROBABILITY,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description=f"Expected cost per DALY accounting for political success probability uncertainty. "
                f"Monte Carlo samples from beta(0.1%, 10%) distribution. At the conservative 1% estimate, "
                f"this is still more cost-effective than bed nets (${BED_NETS_COST_PER_DALY}/DALY).",
    display_name="Expected Cost per DALY (Risk-Adjusted)",
    unit="USD/DALY",
    formula="CONDITIONAL_COST_PER_DALY ÷ POLITICAL_SUCCESS_PROBABILITY",    confidence="low",
    keywords=["expected value", "probability weighted", "cost effectiveness", "givewell", "political risk", "uncertainty"],
    inputs=["TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG", "POLITICAL_SUCCESS_PROBABILITY"],
    compute=lambda ctx: ctx["TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG"] / ctx["POLITICAL_SUCCESS_PROBABILITY"],
    latex_symbol=r"E[Cost_{DALY}]",  # LaTeX symbol for equations
)  # Expected cost per DALY at 1% probability (still better than bed nets)

# ---
# DIRECT FUNDING SCENARIO
# ---
# Cost-effectiveness of directly funding ~$21.8B/year in pragmatic clinical trials.

# NPV of direct funding for therapeutic space exploration period
DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV = Parameter(
    DFDA_ANNUAL_TRIAL_FUNDING
    * (1 - (1 + NPV_DISCOUNT_RATE_STANDARD) ** -DFDA_QUEUE_CLEARANCE_YEARS)
    / NPV_DISCOUNT_RATE_STANDARD,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",  # NPV calculation from funding, discount rate, and time horizon
    description="NPV of annual direct funding for the therapeutic space exploration period. Funding period equals exploration time (queue clearance years at given capacity multiplier). After exploration completes, the full timeline shift benefit is realized.",
    display_name="Direct Pragmatic Trial Funding NPV (Exploration Period)",
    unit="USD",
    formula="ANNUAL_FUNDING × [(1 - (1 + r)^-T) / r] where T = exploration time",
    keywords=["philanthropy", "direct funding", "alternative", "npv", "exploration"],
    inputs=['DFDA_ANNUAL_TRIAL_FUNDING', 'NPV_DISCOUNT_RATE_STANDARD', 'DFDA_QUEUE_CLEARANCE_YEARS'],
    compute=lambda ctx: ctx["DFDA_ANNUAL_TRIAL_FUNDING"]
        * (1 - (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** -ctx["DFDA_QUEUE_CLEARANCE_YEARS"])
        / ctx["NPV_DISCOUNT_RATE_STANDARD"],
    latex_symbol=r"NPV_{direct}",  # LaTeX symbol for equations
)  # ~$541.9B NPV

# Cost per DALY for direct funding scenario
DFDA_DIRECT_FUNDING_COST_PER_DALY = Parameter(
    DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV / DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",  # Derived from NPV and DALYs
    description="Cost per DALY at direct funding level for the therapeutic space exploration period. Still highly cost-effective vs bed nets.",
    display_name="Direct Pragmatic Trial Funding Cost per DALY",
    unit="USD/DALY",
    formula="NPV_DIRECT_FUNDING ÷ DALYS_TIMELINE_SHIFT",    confidence="medium",
    keywords=["philanthropy", "direct funding", "cost effectiveness"],
    inputs=["DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV", "DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"],
    compute=lambda ctx: ctx["DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV"] / ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"],
    latex_symbol=r"Cost_{direct,DALY}",  # LaTeX symbol for equations
)  # ~$0.98/DALY

# Direct funding ROI
DFDA_DIRECT_FUNDING_ROI_TRIAL_CAPACITY_PLUS_EFFICACY_LAG = Parameter(
    DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE / DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="ROI from directly funding pragmatic clinical trials over the therapeutic space exploration period.",
    display_name="Direct Funding ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput",
    unit="ratio",
    formula="ECONOMIC_VALUE ÷ DIRECT_FUNDING_NPV",
    confidence="high",
    keywords=["direct funding", "philanthropy", "roi", "timeline shift", "trial capacity", "efficacy lag"],
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE", "DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE"] / ctx["DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV"],
    latex_symbol=r"ROI_{direct,max}",  # LaTeX symbol for equations
)  # ~152,000:1 ROI

# Direct funding vs bed nets comparison
DFDA_DIRECT_FUNDING_VS_BED_NETS_MULTIPLIER = Parameter(
    BED_NETS_COST_PER_DALY / DFDA_DIRECT_FUNDING_COST_PER_DALY,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="How many times more cost-effective direct funding of medical research is vs bed nets.",
    display_name="Direct Funding Cost-Effectiveness vs Bed Nets",
    unit="x",
    formula="BED_NETS_COST_PER_DALY ÷ DIRECT_FUNDING_COST_PER_DALY",
    confidence="high",
    keywords=["direct funding", "bed nets", "cost effectiveness", "comparison"],
    inputs=['BED_NETS_COST_PER_DALY', 'DFDA_DIRECT_FUNDING_COST_PER_DALY'],
    compute=lambda ctx: ctx["BED_NETS_COST_PER_DALY"] / ctx["DFDA_DIRECT_FUNDING_COST_PER_DALY"],
    latex_symbol=r"k_{direct,nets}",  # LaTeX symbol for equations
)  # ~90× more cost-effective than bed nets

STATE_RTT_VS_GIVEWELL_PHILANTHROPIC_COST_PER_LIFE_MULTIPLIER = Parameter(
    GIVEWELL_COST_PER_LIFE_AVG / STATE_RTT_PHILANTHROPIC_COST_PER_LIFE_SAVED,
    manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
    source_type="calculated",
    description="Conditional philanthropic cost-effectiveness of adopting Universal Right to Try with Evidence in all 50 states relative to the midpoint of GiveWell's cited modeled cost-per-life-saved range. The cost scopes differ: the Right to Try numerator excludes patient and payer spending on treatment delivery, trial-site services, and permitted study costs, while the GiveWell figure includes full program costs. This comparison is valid only if full adoption and mature implementation produce the modeled treatment schedule shift.",
    display_name="Universal Right to Try with Evidence Cost-Effectiveness vs GiveWell Range Midpoint",
    unit="x",
    formula="GIVEWELL_COST_PER_LIFE_AVG ÷ STATE_RTT_PHILANTHROPIC_COST_PER_LIFE_SAVED",
    confidence="low",
    inputs=["GIVEWELL_COST_PER_LIFE_AVG", "STATE_RTT_PHILANTHROPIC_COST_PER_LIFE_SAVED"],
    compute=lambda ctx: ctx["GIVEWELL_COST_PER_LIFE_AVG"] / ctx["STATE_RTT_PHILANTHROPIC_COST_PER_LIFE_SAVED"],
    keywords=["right to try", "right to trial", "GiveWell", "cost per life saved", "cost effectiveness", "philanthropy"],
    latex_symbol=r"k_{RTT,GiveWell}",
    hide_ci=True,
)

# Treaty campaign leverage vs direct funding
TREATY_VS_DIRECT_FUNDING_LEVERAGE = Parameter(
    DFDA_DIRECT_FUNDING_COST_PER_DALY / TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",  # Ratio of cost per DALY metrics
    description="How many times more cost-effective the treaty campaign is vs direct pragmatic trial funding. Treaty campaign unlocks government funding at scale, avoiding need for philanthropists/NIH to directly commit equivalent amounts. Both approaches achieve same DALY timeline shift benefit. Treaty spreads cost across governments while building sustainable public funding infrastructure.",
    display_name="Treaty Campaign Leverage vs Direct Funding",
    unit="x",
    formula="DIRECT_PRAGMATIC_TRIAL_FUNDING_COST_PER_DALY ÷ TREATY_COST_PER_DALY",    confidence="high",
    keywords=["leverage", "campaign effectiveness", "treaty advantage", "cost comparison", "therapeutic space"],
    inputs=['DFDA_DIRECT_FUNDING_COST_PER_DALY', 'TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG'],
    compute=lambda ctx: ctx["DFDA_DIRECT_FUNDING_COST_PER_DALY"] / ctx["TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG"],
    latex_symbol=r"Leverage_{treaty}",  # LaTeX symbol for equations
)  # ~542× - treaty campaign achieves massive leverage

# Cost-effectiveness multipliers vs. bed nets
TREATY_VS_BED_NETS_MULTIPLIER = Parameter(
    BED_NETS_COST_PER_DALY / TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="How many times more cost-effective than bed nets (using bed net cost per DALY midpoint estimate)",
    display_name="Cost-Effectiveness vs Bed Nets Multiplier",
    unit="x",
    formula="BED_NETS_COST_PER_DALY ÷ TREATY_COST_PER_DALY",
    confidence="high",
    inputs=['BED_NETS_COST_PER_DALY', 'TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG'],
    compute=lambda ctx: ctx["BED_NETS_COST_PER_DALY"] / ctx["TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG"],
    latex_symbol=r"k_{treaty:nets}",  # LaTeX symbol for equations
)

TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER = Parameter(
    BED_NETS_COST_PER_DALY / TREATY_EXPECTED_COST_PER_DALY,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Expected value multiplier vs bed nets (accounts for political uncertainty at 1% success rate)",
    display_name="Expected Cost-Effectiveness vs Bed Nets Multiplier",
    unit="x",
    formula="BED_NETS_COST_PER_DALY ÷ TREATY_EXPECTED_COST_PER_DALY",
    confidence="low",
    inputs=['BED_NETS_COST_PER_DALY', 'TREATY_EXPECTED_COST_PER_DALY'],
    compute=lambda ctx: ctx["BED_NETS_COST_PER_DALY"] / ctx["TREATY_EXPECTED_COST_PER_DALY"],
    latex_symbol=r"E[k_{nets}]",  # LaTeX symbol for equations
)

# ---
# COURT OF HUMANITY COST-EFFECTIVENESS
# ---

COURT_BUILD_COST = Parameter(
    30_000_000,  # midpoint of $10M-$50M; Monte Carlo distribution carries uncertainty
    manual_ref="knowledge/solution/court-of-humanity.qmd",
    source_type=SourceType.DEFINITION,
    description="One-time cost to build the Court of Humanity. Range reflects digital-first "
                "institutional design (no physical courtrooms, no detention, AI-assisted "
                "evidence triage, cryptographic provenance, stratified random jury "
                "infrastructure). Lower bound: minimal viable institution. Upper bound: "
                "fully-staffed initial operations, roughly 27% of one year of ICC operating "
                "budget (the ICC funds physical courtrooms, detention, and 425+ staff).",
    display_name="Court of Humanity Build Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(10_000_000, 50_000_000),
    confidence="estimated",
    keywords=["court", "build cost", "court of humanity", "estimate"],
    latex_symbol=r"Cost_{court}",
)

# ---
# HELPER FUNCTIONS
# ---


from dih_models.formatting import (
    format_parameter_value,
    format_roi,
    format_percentage,
    format_qalys
)



# Formatter functions moved to dih_models/formatting.py


# --- Module Initialization ---

if __name__ == "__main__":
    # Print some key parameters when module is executed directly
    print(f"Military spending: {format_parameter_value(GLOBAL_MILITARY_SPENDING_ANNUAL_2024)}")
    print(f"Total war costs: {format_parameter_value(GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST)}")
    print(f"Peace dividend: {format_parameter_value(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT)}")
    print(f"Decentralized Framework for Drug Assessment savings: {format_parameter_value(DFDA_BENEFIT_RD_ONLY_ANNUAL)}")
    print(f"Total benefits: {format_parameter_value(TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS)}")

# Derived time-based costs (SECONDS_PER_YEAR defined in TIME CONSTANTS section)
# SECONDS_PER_YEAR = DAYS_PER_YEAR * HOURS_PER_DAY * 60 * 60
GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH = Parameter(
    4_200_000,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_ref="medical-research-lives-saved-annually",
    source_type="external",
    description="Annual lives saved by medical research globally",
    display_name="Annual Lives Saved by Medical Research Globally",
    unit="lives/year",
    keywords=["4.2m", "deaths prevented", "life saving", "mortality reduction", "deaths averted", "worldwide", "yearly"],
    distribution="lognormal",
    confidence_interval=(3_000_000, 6_000_000),  # ±30% - attribution difficult to measure
    latex_symbol=r"Lives_{RD,ann}",  # LaTeX symbol for equations
)
GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL = Parameter(
    GLOBAL_MED_RESEARCH_SPENDING / GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Cost per life saved by medical research",
    display_name="Cost per Life Saved by Medical Research",
    unit="USD/life",
    formula="(RESEARCH_SPENDING × 1B) ÷ LIVES_SAVED",    keywords=["worldwide", "yearly", "investigation", "r&d", "science", "study", "conflict"],
    inputs=['GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH', 'GLOBAL_MED_RESEARCH_SPENDING'],
    compute=lambda ctx: ctx["GLOBAL_MED_RESEARCH_SPENDING"] / ctx["GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH"],
    latex_symbol=r"Cost_{life,RD}",  # LaTeX symbol for equations
)  # ~$16,071
MISALLOCATION_FACTOR_DEATH_VS_SAVING = Parameter(
    (GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL)
    / GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL,
    manual_ref="knowledge/appendix/dfda-impact-paper.qmd",
    source_type="calculated",
    description="Misallocation factor: cost to kill vs cost to save",
    display_name="Misallocation Factor: Cost to Kill vs Cost to Save",
    unit="x",
    formula="COST_PER_DEATH ÷ COST_PER_LIFE_SAVED",
    keywords=["multiple", "fatalities", "casualties", "deaths", "investigation", "r&d", "science"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL', 'GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST', 'GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL'],
    compute=lambda ctx: (ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] / ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL"])
    / ctx["GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL"],
    latex_symbol=r"k_{misalloc}",  # LaTeX symbol for equations
)  # ~2,889x

# Opportunity Cost Parameters
ECONOMIC_MULTIPLIER_MILITARY_SPENDING = Parameter(
    0.6,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.MILITARY_SPENDING_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for military spending (0.6x ROI). Literature range 0.4-1.0×.",
    display_name="Economic Multiplier for Military Spending",
    unit="x",
    distribution="lognormal",
    confidence_interval=(0.4, 0.9),
    keywords=["60%", "dod", "pentagon", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect"],
    latex_symbol=r"k_{mil}",  # LaTeX symbol for equations
)

ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT = Parameter(
    1.6,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.INFRASTRUCTURE_INVESTMENT_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for infrastructure investment (1.6x ROI)",
    display_name="Economic Multiplier for Infrastructure Investment",
    unit="x",
    keywords=["economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple", "capital"],
    latex_symbol=r"k_{infra}",  # LaTeX symbol for equations
)

ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT = Parameter(
    2.1,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_ref=ReferenceID.EDUCATION_INVESTMENT_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for education investment (2.1x ROI)",
    display_name="Economic Multiplier for Education Investment",
    unit="x",
    keywords=["economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple", "capital"],
    latex_symbol=r"k_{edu}",  # LaTeX symbol for equations
)

ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT = Parameter(
    4.3,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.HEALTHCARE_INVESTMENT_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for healthcare investment (4.3x ROI). Literature range 3.0-6.0×.",
    display_name="Economic Multiplier for Healthcare Investment",
    unit="x",
    distribution="lognormal",
    confidence_interval=(3.0, 6.0),
    keywords=["economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple", "capital"],
    latex_symbol=r"k_{health}",  # LaTeX symbol for equations
)

# Healthcare vs Military Spending Multiplier Ratio
HEALTHCARE_VS_MILITARY_MULTIPLIER_RATIO = Parameter(
    float(ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT) / float(ECONOMIC_MULTIPLIER_MILITARY_SPENDING),
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Ratio of healthcare to military fiscal multipliers. Healthcare investment generates 7× more "
                "economic activity per dollar than military spending.",
    display_name="Healthcare vs Military Multiplier Ratio",
    unit="x",
    formula="ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT / ECONOMIC_MULTIPLIER_MILITARY_SPENDING",
    inputs=["ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT", "ECONOMIC_MULTIPLIER_MILITARY_SPENDING"],
    compute=lambda ctx: ctx["ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT"] / ctx["ECONOMIC_MULTIPLIER_MILITARY_SPENDING"],
    keywords=["healthcare", "military", "multiplier", "ratio", "comparison"],
    latex_symbol=r"r_{health/mil}",
)

GLOBAL_REGISTERED_VOTERS = Parameter(
    4_128_142_495,
    manual_ref="knowledge/strategy/global-referendum.qmd",
    source_ref=ReferenceID.INTERNATIONAL_IDEA_VOTER_TURNOUT_DATABASE_2026,
    source_type="external",
    description="Best current register-based estimate of the number of registered voters worldwide, "
                "calculated by summing the latest available country-level electoral-roll counts "
                "in International IDEA's Voter Turnout Database export. Used as the verified-human "
                "headcount proxy for the majority-of-humanity coordination target.",
    display_name="Global Registered Voters",
    unit="of people",
    latex=r"""
\begin{gathered}
N_{voters,global} \\
= 4{,}128{,}142{,}495 \\
\approx 4.13B
\end{gathered}
""".strip(),
    distribution="fixed",
    keywords=["registered voters", "global electorate", "4.13 billion", "voters worldwide", "electoral rolls", "majority of humanity"],
    latex_symbol=r"N_{voters,global}",
)

GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT = Parameter(
    0.035,
    manual_ref="knowledge/strategy/global-referendum.qmd",
    source_ref=ReferenceID.N3_5_RULE,
    source_type="external",
    description="Critical mass threshold for social change (3.5% rule). Chenoweth studied national "
                "regime changes; applying to a global treaty adds uncertainty. Lower bound: some movements "
                "succeeded at ~1%. Upper bound: entrenched defense-industry opposition and weaker signal "
                "from digital signatures vs sustained protest may require up to 10%.",
    display_name="Critical Mass Threshold for Social Change",
    unit="percent",
    confidence_interval=(0.01, 0.10),  # 1-10%: Chenoweth national data applied to global treaty context
    distribution="lognormal",
    keywords=["4%", "people", "worldwide", "citizens", "individuals", "inhabitants", "persons"],
    latex_symbol=r"Threshold_{activism}",  # LaTeX symbol for equations
)  # 3.5% rule for social change, key tipping point

THREE_POINT_FIVE_PERCENT_OF_GLOBAL_POPULATION = Parameter(
    GLOBAL_POPULATION_2024 * GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT,
    manual_ref="knowledge/economics/campaign-budget.qmd",
    source_type="calculated",
    description="Headcount implied by the 3.5% activism threshold applied to global population. "
                "This is a historical tipping-point benchmark, not the public majority-of-humanity "
                "coordination target. Wide CI reflects uncertainty in applying Chenoweth's national "
                "threshold to global treaty adoption.",
    display_name="3.5% Activism Benchmark",
    unit="of people",
    formula="GLOBAL_POPULATION_2024 × GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT",
    keywords=["3.5 percent", "global population", "280.0m", "international agreement", "peace treaty", "agreement", "pact", "tipping point"],
    inputs=['GLOBAL_POPULATION_2024', 'GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT'],
    compute=lambda ctx: ctx["GLOBAL_POPULATION_2024"] * ctx["GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT"],
    latex_symbol=r"N_{activism}",  # LaTeX symbol for equations
)  # 280M people = 3.5% of 8B (critical mass threshold)

# Per-voter impact (total impact ÷ majority-of-humanity coordination target)
# Used in podcast outro CTA and campaign materials
VOTER_LIVES_SAVED = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED) / float(GLOBAL_REGISTERED_VOTERS),
    manual_ref="knowledge/strategy/nonprofit-coalition-strategy.qmd",
    source_type="calculated",
    description="Average lives saved per verified voter if the treaty passes "
                "(total lives saved divided by the majority-of-humanity coordination target).",
    display_name="Lives Saved per Verified Voter",
    unit="lives",
    formula="TOTAL_TIMELINE_SHIFT_LIVES_SAVED ÷ GLOBAL_REGISTERED_VOTERS",
    keywords=["per voter", "individual impact", "lives saved", "CTA", "campaign", "majority of humanity"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED', 'GLOBAL_REGISTERED_VOTERS'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED"] / ctx["GLOBAL_REGISTERED_VOTERS"],
    latex_symbol=r"Lives_{voter}",
    hide_ci=True,  # CTA copy uses the point estimate.
)

VOTER_SUFFERING_HOURS_PREVENTED = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS) / float(GLOBAL_REGISTERED_VOTERS),
    manual_ref="knowledge/strategy/nonprofit-coalition-strategy.qmd",
    source_type="calculated",
    description="Average suffering hours prevented per verified voter if the treaty passes "
                "(total suffering hours divided by the majority-of-humanity coordination target).",
    display_name="Suffering Hours Prevented per Verified Voter",
    unit="hours",
    formula="TOTAL_TIMELINE_SHIFT_SUFFERING_HOURS ÷ GLOBAL_REGISTERED_VOTERS",
    keywords=["per voter", "individual impact", "suffering", "CTA", "campaign", "majority of humanity"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS', 'GLOBAL_REGISTERED_VOTERS'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS"] / ctx["GLOBAL_REGISTERED_VOTERS"],
    latex_symbol=r"Hours_{suffer,voter}",
    hide_ci=True,  # CTA copy uses the point estimate.
)

# ── Earth Optimization Prize Fund ────────────────────────────────────────────
# Models the prize pool as an actively allocated investment fund rather than
# passive escrow. Baseline = venture gross return (fee-free, illiquid),
# adjusted for scale compression, crowd allocation alpha, and home-bias
# elimination, plus six first-order feedback loops.

# --- Structural inputs ---

VENTURE_GROSS_RETURN = Parameter(
    0.17,
    manual_ref="knowledge/economics/earth-optimization-prize-treasury.qmd",
    source_type="external",
    description="Venture capital / private equity gross return (before 2-and-20 fees). "
                "Cambridge Associates US VC index 25-year pooled gross IRR. "
                "The Prize Fund charges zero fees, so gross return is the correct baseline. "
                "Lockup premium is already embedded: VC/PE IS illiquid.",
    display_name="Venture Capital Gross Return",
    unit="percent",
    confidence_interval=(0.13, 0.22),
    distribution="normal",
    keywords=["venture", "capital", "gross", "return", "PE", "private equity", "baseline", "IRR"],
    latex_symbol=r"r_{VC,gross}",
)

SCALE_COMPRESSION_FACTOR = Parameter(
    -0.025,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="definition",
    description="Diminishing-returns drag as the venture market expands ~15x "
                "(current global VC ~$300B/yr; Prize Fund deploys ~$4.7T/yr). "
                "More capital chasing deals compresses returns. Partially offset by "
                "market expansion (every viable idea gets funded, oligopolies face "
                "real competition). Point estimate is moderate; CI spans optimistic "
                "to pessimistic.",
    display_name="Scale Compression Factor",
    unit="percent",
    confidence_interval=(-0.05, -0.01),
    distribution="normal",
    keywords=["scale", "compression", "diminishing", "returns", "venture", "expansion"],
    latex_symbol=r"\Delta r_{scale}",
)

CROWD_DECISION_ACCURACY = Parameter(
    0.91,
    manual_ref="knowledge/solution/wishocracy.qmd",
    source_ref=ReferenceID.SUROWIECKI_2004,
    source_type="external",
    distribution="fixed",
    description="Crowd accuracy on Who Wants to Be a Millionaire ask-the-audience lifeline. "
                "Studio audience picked the correct answer 91% of the time (Surowiecki 2004). "
                "Used as lower bound for wishocratic allocation accuracy.",
    display_name="Crowd Decision Accuracy (Millionaire)",
    unit="percent",
    keywords=["crowd", "accuracy", "millionaire", "ask the audience", "91", "surowiecki", "wisdom"],
    latex_symbol=r"Acc_{crowd}",
)

EXPERT_DECISION_ACCURACY = Parameter(
    0.65,
    manual_ref="knowledge/solution/wishocracy.qmd",
    source_ref=ReferenceID.SUROWIECKI_2004,
    source_type="external",
    distribution="fixed",
    description="Expert accuracy on Who Wants to Be a Millionaire phone-a-friend lifeline. "
                "Credentialed expert picked the correct answer 65% of the time (Surowiecki 2004). "
                "Used as baseline for conventional fund manager / committee allocation.",
    display_name="Expert Decision Accuracy (Millionaire)",
    unit="percent",
    keywords=["expert", "accuracy", "millionaire", "phone a friend", "65", "surowiecki"],
    latex_symbol=r"Acc_{expert}",
)

ALLOCATION_DECISION_SPREAD = Parameter(
    0.08,
    manual_ref="knowledge/solution/wishocracy.qmd",
    source_type="definition",
    description="Return spread between the best and worst major asset-class sectors "
                "(biotech vs. coal, growth vs. value, emerging vs. declining). "
                "The accuracy advantage of crowds over experts is multiplied by this spread "
                "to estimate the allocation alpha from wishocratic decision-making.",
    display_name="Allocation Decision Return Spread",
    unit="percent",
    confidence_interval=(0.05, 0.12),
    distribution="normal",
    keywords=["allocation", "spread", "sector", "return", "difference", "alpha"],
    latex_symbol=r"S_{alloc}",
)

HOME_BIAS_ALPHA = Parameter(
    0.008,
    manual_ref="knowledge/economics/earth-optimization-prize-treasury.qmd",
    source_type="external",
    description="Return drag from home bias in fragmented national pension systems. "
                "70+ countries each overweight domestic assets, missing global diversification. "
                "IMF and Vanguard studies estimate 0.3-1.5% annual return cost. "
                "Wishocratic allocation is inherently global, eliminating this drag.",
    display_name="Home Bias Return Drag",
    unit="percent",
    confidence_interval=(0.003, 0.015),
    distribution="normal",
    keywords=["home", "bias", "pension", "diversification", "drag", "alpha", "global"],
    latex_symbol=r"\alpha_{home}",
)

GLOBAL_RETIREMENT_ASSETS = Parameter(
    70_000_000_000_000,
    manual_ref="knowledge/economics/earth-optimization-prize-treasury.qmd",
    source_type="external",
    description="Total global pension and retirement assets (OECD 2024). "
                "This is the capital pool that the Prize Fund competes with "
                "and could partially absorb.",
    display_name="Global Retirement Assets",
    unit="USD",
    distribution="fixed",
    keywords=["retirement", "pension", "assets", "global", "70 trillion", "OECD"],
    latex_symbol=r"Assets_{retire}",
)

CONVENTIONAL_RETIREMENT_RETURN = Parameter(
    0.065,
    manual_ref="knowledge/economics/earth-optimization-prize-treasury.qmd",
    source_type="external",
    description="Average retail after-fee return on conventional retirement portfolios "
                "(60/40 stock/bond mix, ~1% advisory fees, ~0.4% fund fees). "
                "Used as the opportunity cost comparison: depositors are LOSING money "
                "by NOT participating in the Prize Fund.",
    display_name="Conventional Retirement Return (After Fees)",
    unit="percent",
    confidence_interval=(0.05, 0.08),
    distribution="normal",
    keywords=["retirement", "conventional", "return", "60/40", "after fee", "opportunity cost"],
    latex_symbol=r"r_{retire}",
)

CONVENTIONAL_RETIREMENT_HORIZON_MULTIPLE = Parameter(
    (1 + float(CONVENTIONAL_RETIREMENT_RETURN)) ** round(_years_to_50pct),
    manual_ref="knowledge/economics/earth-optimization-prize-treasury.qmd",
    source_type="calculated",
    description="Compound multiple for conventional retirement investing over the prize pool resolution horizon "
                "(tied to the destructive economy 50% threshold year).",
    display_name="Conventional Retirement Horizon Multiple",
    unit="x",
    formula="(1 + CONVENTIONAL_RETIREMENT_RETURN) ^ (DESTRUCTIVE_ECONOMY_50PCT_YEAR - DESTRUCTIVE_ECONOMY_BASE_YEAR)",
    inputs=["CONVENTIONAL_RETIREMENT_RETURN", "DESTRUCTIVE_ECONOMY_50PCT_YEAR", "DESTRUCTIVE_ECONOMY_BASE_YEAR"],
    compute=lambda ctx: (1 + ctx["CONVENTIONAL_RETIREMENT_RETURN"]) ** (ctx["DESTRUCTIVE_ECONOMY_50PCT_YEAR"] - ctx["DESTRUCTIVE_ECONOMY_BASE_YEAR"]),
    keywords=["retirement", "conventional", "multiple", "horizon", "compound"],
    latex_symbol=r"M_{retire}",
)

# --- Calculated: crowd allocation alpha ---

WISHOCRATIC_CROWD_ALPHA = Parameter(
    0.005,
    manual_ref="knowledge/economics/earth-optimization-prize-treasury.qmd",
    source_type="definition",
    description="Allocation alpha from wishocratic sector- and manager-level capital routing. "
                "Crowds route capital across sectors and managers at least as well as "
                "cap-weighted indices or committee allocators. SPIVA shows 88% of active large-cap "
                "managers underperform their benchmark over 15 years; Preqin shows top-quartile vs "
                "bottom-quartile VC manager dispersion of 5-15%. The 0.5% central value assumes "
                "only that RAPPA avoids the bottom half of manager dispersion at the allocation "
                "level, not that it finds the top quartile. This is not a claim that crowds beat "
                "experts at picking individual companies; power-law outlier selection is the one "
                "thing crowds are empirically worse at than specialists.",
    display_name="Wishocratic Crowd Allocation Alpha",
    unit="percent",
    confidence_interval=(0.0, 0.015),
    distribution="normal",
    keywords=["crowd", "alpha", "allocation", "wishocratic", "advantage", "SPIVA", "Preqin", "sector"],
    latex_symbol=r"\alpha_{crowd}",
)

# --- Calculated: canonical prize pool return and multiple ---

PRIZE_POOL_ANNUAL_RETURN = Parameter(
    float(VENTURE_GROSS_RETURN) + float(SCALE_COMPRESSION_FACTOR) + float(WISHOCRATIC_CROWD_ALPHA) + float(HOME_BIAS_ALPHA),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Canonical annual return used for prize pool growth. "
                "Venture gross return + scale compression + crowd allocation alpha + home bias elimination. "
                "This is the structural pool return before contingent macro feedback loops.",
    display_name="PRIZE Pool Annual Return",
    unit="percent",
    formula="VENTURE_GROSS_RETURN + SCALE_COMPRESSION_FACTOR + WISHOCRATIC_CROWD_ALPHA + HOME_BIAS_ALPHA",
    inputs=["VENTURE_GROSS_RETURN", "SCALE_COMPRESSION_FACTOR", "WISHOCRATIC_CROWD_ALPHA", "HOME_BIAS_ALPHA"],
    compute=lambda ctx: ctx["VENTURE_GROSS_RETURN"] + ctx["SCALE_COMPRESSION_FACTOR"] + ctx["WISHOCRATIC_CROWD_ALPHA"] + ctx["HOME_BIAS_ALPHA"],
    keywords=["prize", "pool", "annual", "return", "structural", "fund"],
    latex_symbol=r"r_{pool}",
)

PRIZE_POOL_HORIZON_MULTIPLE = Parameter(
    (1 + float(PRIZE_POOL_ANNUAL_RETURN)) ** round(_years_to_50pct),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Compound multiple for prize pool growth over the resolution horizon "
                "(tied to the destructive economy 50% threshold year).",
    display_name="PRIZE Pool Horizon Multiple",
    unit="x",
    formula="(1 + PRIZE_POOL_ANNUAL_RETURN) ^ (DESTRUCTIVE_ECONOMY_50PCT_YEAR - DESTRUCTIVE_ECONOMY_BASE_YEAR)",
    inputs=["PRIZE_POOL_ANNUAL_RETURN", "DESTRUCTIVE_ECONOMY_50PCT_YEAR", "DESTRUCTIVE_ECONOMY_BASE_YEAR"],
    compute=lambda ctx: (1 + ctx["PRIZE_POOL_ANNUAL_RETURN"]) ** (ctx["DESTRUCTIVE_ECONOMY_50PCT_YEAR"] - ctx["DESTRUCTIVE_ECONOMY_BASE_YEAR"]),
    keywords=["prize", "pool", "multiple", "horizon", "compound", "fund"],
    latex_symbol=r"M_{pool}",
)

GLOBAL_INVESTABLE_ASSETS = Parameter(
    305_000_000_000_000,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="external",
    description="Total global financial wealth (2024): equities, bonds, cash/deposits, and "
                "investment funds. Excludes real estate and physical assets. This is the "
                "addressable capital pool for Prize deposits.",
    display_name="Global Investable Financial Assets",
    unit="USD",
    distribution="fixed",
    keywords=["investable", "financial", "assets", "global", "wealth", "305 trillion", "BCG"],
    latex_symbol=r"Assets_{invest}",
)

PRIZE_POOL_PARTICIPATION_RATE = Parameter(
    0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="definition",
    description="Fraction of global investable financial assets that flow into the prize pool. "
                "1% central estimate parallels the 1% Treaty ask: 1% of your weapons money, "
                "1% of your savings.",
    display_name="Prize Pool Participation Rate",
    unit="percent",
    distribution="lognormal",
    confidence_interval=(0.001, 0.10),
    keywords=["participation", "rate", "prize", "pool", "deposit", "fraction", "1 percent"],
    latex_symbol=r"R_{pool}",
)

PRIZE_POOL_SIZE = Parameter(
    float(GLOBAL_INVESTABLE_ASSETS) * float(PRIZE_POOL_PARTICIPATION_RATE) * float(PRIZE_POOL_HORIZON_MULTIPLE),
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_type="calculated",
    description="Terminal prize pool size: global investable assets × participation rate × "
                "compound multiple over the resolution horizon.",
    display_name="Prize Pool Size",
    unit="USD",
    formula="GLOBAL_INVESTABLE_ASSETS × PRIZE_POOL_PARTICIPATION_RATE × PRIZE_POOL_HORIZON_MULTIPLE",
    inputs=["GLOBAL_INVESTABLE_ASSETS", "PRIZE_POOL_PARTICIPATION_RATE", "PRIZE_POOL_HORIZON_MULTIPLE"],
    compute=lambda ctx: ctx["GLOBAL_INVESTABLE_ASSETS"] * ctx["PRIZE_POOL_PARTICIPATION_RATE"] * ctx["PRIZE_POOL_HORIZON_MULTIPLE"],
    keywords=["prize", "pool", "size", "investable", "assets", "participation"],
    latex_symbol=r"Pool",
)

GLOBAL_COORDINATION_TARGET_PCT = Parameter(
    float(GLOBAL_REGISTERED_VOTERS) / float(GLOBAL_POPULATION_2024),
    manual_ref="knowledge/strategy/global-referendum.qmd",
    source_type="calculated",
    description="Majority-of-humanity public coordination target as a share of global population, "
                "using global registered voters as the current verified-human headcount proxy.",
    display_name="Majority of Humanity Coordination Target",
    unit="percent",
    formula="GLOBAL_REGISTERED_VOTERS / GLOBAL_POPULATION_2024",
    inputs=["GLOBAL_REGISTERED_VOTERS", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["GLOBAL_REGISTERED_VOTERS"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["majority of humanity", "registered voters", "global population", "share", "electorate", "51.6 percent"],
    latex_symbol=r"R_{humanity,majority}",
)

GLOBAL_COORDINATION_ACTIVATION_REWARD_PER_VERIFIED_PARTICIPANT = Parameter(
    5.0,
    manual_ref="knowledge/strategy/nonprofit-coalition-strategy.qmd",
    source_type="definition",
    description="Planning midpoint for the direct cash incentive required to make a successful verified recruit "
                "materially worth sharing at global scale. Intended as a research-backed blended reward across "
                "referrer and recruit, not as the long-dated PRIZE claim value.",
    display_name="Activation Reward per Verified Participant",
    unit="USD",
    confidence="medium",
    confidence_interval=(2.0, 10.0),
    std_error=1.5,
    distribution="normal",
    validation_min=2.0,
    validation_max=10.0,
    keywords=["activation", "reward", "verified participant", "referral", "coordination", "cash incentive"],
    latex_symbol=r"R_{activate}",
)

GLOBAL_COORDINATION_VERIFICATION_AND_PAYMENT_COST_PER_PARTICIPANT = Parameter(
    1.5,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="definition",
    description="Planning midpoint for non-reward variable cost per successful verified participant: identity "
                "verification, payment rails, fraud checks, support, and completion friction.",
    display_name="Verification and Payment Cost per Participant",
    unit="USD",
    confidence="medium",
    confidence_interval=(1.0, 3.0),
    std_error=0.5,
    distribution="normal",
    validation_min=1.0,
    validation_max=3.0,
    keywords=["activation", "verification", "payment", "cost", "participant", "fraud", "identity"],
    latex_symbol=r"C_{verify,pp}",
)

GLOBAL_COORDINATION_PLATFORM_AND_OPERATIONS_COST = Parameter(
    4_000_000_000,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="definition",
    description="Fixed cost to run a global activation campaign toward majority-of-humanity participation: "
                "platform buildout, localization, customer support, compliance, "
                "payout operations, fraud response, and regional launch infrastructure.",
    display_name="Global Coordination Platform and Operations Cost",
    unit="USD",
    confidence="medium",
    confidence_interval=(2_000_000_000, 8_000_000_000),
    std_error=1_500_000_000,
    distribution="normal",
    validation_min=2_000_000_000,
    validation_max=8_000_000_000,
    keywords=["activation", "platform", "operations", "global", "campaign", "infrastructure"],
    latex_symbol=r"C_{ops}",
)

GLOBAL_COORDINATION_ACTIVATION_COST_PER_PARTICIPANT = Parameter(
    float(GLOBAL_COORDINATION_ACTIVATION_REWARD_PER_VERIFIED_PARTICIPANT) + float(GLOBAL_COORDINATION_VERIFICATION_AND_PAYMENT_COST_PER_PARTICIPANT),
    manual_ref="knowledge/strategy/global-referendum.qmd",
    source_type="calculated",
    description="Blended variable activation cost per successful verified participant: direct incentive plus "
                "verification and payment operations.",
    display_name="Activation Cost per Participant",
    unit="USD",
    formula="GLOBAL_COORDINATION_ACTIVATION_REWARD_PER_VERIFIED_PARTICIPANT + GLOBAL_COORDINATION_VERIFICATION_AND_PAYMENT_COST_PER_PARTICIPANT",
    inputs=["GLOBAL_COORDINATION_ACTIVATION_REWARD_PER_VERIFIED_PARTICIPANT", "GLOBAL_COORDINATION_VERIFICATION_AND_PAYMENT_COST_PER_PARTICIPANT"],
    compute=lambda ctx: ctx["GLOBAL_COORDINATION_ACTIVATION_REWARD_PER_VERIFIED_PARTICIPANT"] + ctx["GLOBAL_COORDINATION_VERIFICATION_AND_PAYMENT_COST_PER_PARTICIPANT"],
    keywords=["activation", "cost per participant", "verified participant", "coordination", "referral"],
    latex_symbol=r"C_{activate,pp}",
)

GLOBAL_COORDINATION_ACTIVATION_BUDGET = Parameter(
    float(GLOBAL_REGISTERED_VOTERS) * float(GLOBAL_COORDINATION_ACTIVATION_COST_PER_PARTICIPANT) + float(GLOBAL_COORDINATION_PLATFORM_AND_OPERATIONS_COST),
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_type="calculated",
    description="Canonical institutional activation threshold: capital required to make participation by the "
                "majority-of-humanity coordination target credible through direct referral incentives, verification, "
                "payment rails, and global launch operations. "
                "This is the main institutional ask, not the prize pool seed benchmark.",
    display_name="Global Coordination Activation Budget",
    unit="USD",
    formula="GLOBAL_REGISTERED_VOTERS × GLOBAL_COORDINATION_ACTIVATION_COST_PER_PARTICIPANT + GLOBAL_COORDINATION_PLATFORM_AND_OPERATIONS_COST",
    inputs=["GLOBAL_REGISTERED_VOTERS", "GLOBAL_COORDINATION_ACTIVATION_COST_PER_PARTICIPANT", "GLOBAL_COORDINATION_PLATFORM_AND_OPERATIONS_COST"],
    compute=lambda ctx: ctx["GLOBAL_REGISTERED_VOTERS"] * ctx["GLOBAL_COORDINATION_ACTIVATION_COST_PER_PARTICIPANT"] + ctx["GLOBAL_COORDINATION_PLATFORM_AND_OPERATIONS_COST"],
    keywords=["activation", "budget", "coordination", "institutional", "referral", "verification", "majority of humanity"],
    latex_symbol=r"B_{activate}",
)

RETIREMENT_EQUIVALENT_2_CLAIMS_TARGET_PAYOUT = Parameter(
    float(GLOBAL_ANNUAL_SAVINGS_PER_CAPITA) * float(CONVENTIONAL_RETIREMENT_HORIZON_MULTIPLE),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Target success-side payout for two referred votes: what one representative annual savings contribution "
                "would become in a conventional retirement account by PRIZE resolution.",
    display_name="Retirement-Equivalent 2-Claims Target Payout",
    unit="USD",
    formula="GLOBAL_ANNUAL_SAVINGS_PER_CAPITA × CONVENTIONAL_RETIREMENT_HORIZON_MULTIPLE",
    inputs=["GLOBAL_ANNUAL_SAVINGS_PER_CAPITA", "CONVENTIONAL_RETIREMENT_HORIZON_MULTIPLE"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_SAVINGS_PER_CAPITA"] * ctx["CONVENTIONAL_RETIREMENT_HORIZON_MULTIPLE"],
    keywords=["retirement", "equivalent", "2 claims", "payout", "annual savings", "target"],
    latex_symbol=r"V_{2claims,target}",
)

RETIREMENT_EQUIVALENT_CLAIM_VALUE_TARGET = Parameter(
    float(RETIREMENT_EQUIVALENT_2_CLAIMS_TARGET_PAYOUT) / 2,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Target value of one referred-voter claim when two claims are meant to match the conventional-retirement "
                "future value of one representative annual savings contribution.",
    display_name="Retirement-Equivalent Claim Value Target",
    unit="USD",
    formula="RETIREMENT_EQUIVALENT_2_CLAIMS_TARGET_PAYOUT / 2",
    inputs=["RETIREMENT_EQUIVALENT_2_CLAIMS_TARGET_PAYOUT"],
    compute=lambda ctx: ctx["RETIREMENT_EQUIVALENT_2_CLAIMS_TARGET_PAYOUT"] / 2,
    keywords=["retirement", "equivalent", "claim", "value", "target", "referred voter"],
    latex_symbol=r"V_{claim,target}",
)

PRIZE_POOL_RETIREMENT_EQUIVALENT_PRINCIPAL = Parameter(
    float(GLOBAL_REGISTERED_VOTERS) * float(RETIREMENT_EQUIVALENT_CLAIM_VALUE_TARGET) / float(PRIZE_POOL_HORIZON_MULTIPLE),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Secondary PRIZE seed benchmark: initial principal required so that the pool can make two referred votes "
                "retirement-equivalent on success at the majority-of-humanity coordination target. This is a "
                "stronger-incentive visible-pool benchmark, not the minimum capital required to make "
                "majority-of-humanity participation credible.",
    display_name="PRIZE Pool Retirement-Equivalent Principal",
    unit="USD",
    formula="GLOBAL_REGISTERED_VOTERS × RETIREMENT_EQUIVALENT_CLAIM_VALUE_TARGET / PRIZE_POOL_HORIZON_MULTIPLE",
    inputs=["GLOBAL_REGISTERED_VOTERS", "RETIREMENT_EQUIVALENT_CLAIM_VALUE_TARGET", "PRIZE_POOL_HORIZON_MULTIPLE"],
    compute=lambda ctx: ctx["GLOBAL_REGISTERED_VOTERS"] * ctx["RETIREMENT_EQUIVALENT_CLAIM_VALUE_TARGET"] / ctx["PRIZE_POOL_HORIZON_MULTIPLE"],
    keywords=["prize", "pool", "retirement equivalent", "principal", "seed", "benchmark", "deposit"],
    latex_symbol=r"P_{retire-eq}",
)

# VOTE token value (pool size ÷ majority-of-humanity coordination target)
EARTH_OPTIMIZATION_POINT_VALUE = Parameter(
    float(PRIZE_POOL_SIZE) / float(GLOBAL_REGISTERED_VOTERS),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Value of a single Earth Optimization Point based on the modeled prize pool size "
                "(investable assets × participation rate × horizon multiple). "
                "CI range reflects participation uncertainty (0.1%-10%).",
    display_name="Earth Optimization Point Value",
    unit="USD",
    formula="PRIZE_POOL_SIZE / GLOBAL_REGISTERED_VOTERS",
    inputs=["PRIZE_POOL_SIZE", "GLOBAL_REGISTERED_VOTERS"],
    compute=lambda ctx: ctx["PRIZE_POOL_SIZE"] / ctx["GLOBAL_REGISTERED_VOTERS"],
    keywords=["vote", "token", "value", "prize", "pool", "incentive", "recruitment"],
    latex_symbol=r"V_{vote}",
)

EARTH_OPTIMIZATION_TWO_POINTS_PAYOUT = Parameter(
    2 * float(PRIZE_POOL_SIZE) / float(GLOBAL_REGISTERED_VOTERS),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Payout for a depositor who recruits 2 verified participants "
                "(earning 2 Earth Optimization Points). CI range reflects participation uncertainty.",
    display_name="Earth Optimization Points Payout (2 Claims)",
    unit="USD",
    formula="2 × EARTH_OPTIMIZATION_POINT_VALUE",
    inputs=["EARTH_OPTIMIZATION_POINT_VALUE"],
    compute=lambda ctx: 2 * ctx["EARTH_OPTIMIZATION_POINT_VALUE"],
    keywords=["vote", "2 claims", "payout", "recruit", "two", "deposit"],
    latex_symbol=r"V_{2claims}",
)

# ============================================================================
# SHIRT CAMPAIGN PARAMETERS
# ============================================================================
# Inputs and derived ratios for the foundation-pitch on the wearable referral
# campaign. The argument: ~1M visible humans wearing the message breaks the
# social-proof barrier, after which everyone else can write it on a shirt they
# already own with permanent marker. Foundations escrow the seed cost via the
# Earth Optimization Prize assurance contract.
# ============================================================================

SHIRT_SEED_WEARERS_THRESHOLD = Parameter(
    1_000_000,
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="definition",
    description="Planning estimate for the number of visible humans who must wear the "
                "End-War-and-Disease message before the social-proof barrier breaks and "
                "imitation becomes spontaneous. Sized between the ALS Ice Bucket (~17M "
                "participants) and Livestrong (~87M bracelets) cascade trigger points, "
                "discounted for the lower-friction permanent-marker version.",
    display_name="Shirt Seed Wearers Threshold",
    unit="of people",
    confidence="low",
    confidence_interval=(100_000, 5_000_000),
    distribution="lognormal",
    keywords=["shirt", "seed", "threshold", "cascade", "social proof", "weirdness barrier"],
    latex_symbol=r"N_{seed,shirt}",
)

SHIRT_SEED_COST_PER_WEARER_USD = Parameter(
    50.0,
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="definition",
    description="Blended cost per seed wearer: printed shirt, small honorarium, and "
                "campaign admin. Includes a mix of professionally-printed shirts for "
                "influencers and bulk-print runs for university chapters, athletes, and "
                "micro-celebrities. Excludes top-tier celebrity placements (handled "
                "through separate sponsorship; see Getting Started celebrity layer).",
    display_name="Shirt Seed Cost per Wearer",
    unit="USD",
    confidence="low",
    confidence_interval=(10.0, 200.0),
    distribution="lognormal",
    keywords=["shirt", "seed", "cost", "per wearer", "influencer", "honorarium"],
    latex_symbol=r"C_{seed,wearer}",
)

SHIRT_WEARING_FRICTION_COST_USD = Parameter(
    5.0,
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="definition",
    description="Perceived social friction cost of wearing a political message in public, "
                "expressed in dollar-equivalent terms. Sets the minimum per-wearer expected "
                "Earth Optimization Prize payout required to make participation rational at "
                "scale. Anchored to the GLOBAL_COORDINATION_ACTIVATION_REWARD_PER_VERIFIED_PARTICIPANT "
                "midpoint, which serves the same role for the verified-vote action.",
    display_name="Shirt Wearing Friction Cost",
    unit="USD",
    confidence="low",
    confidence_interval=(1.0, 25.0),
    distribution="lognormal",
    keywords=["shirt", "friction", "social cost", "wearing", "perceived"],
    latex_symbol=r"C_{friction,shirt}",
)

SHIRT_CASCADE_PROBABILITY_GIVEN_SEED = Parameter(
    0.25,
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="definition",
    description="Subjective probability that the seed program triggers a viral cascade to "
                "majority-of-humanity participation, conditional on the seed threshold being "
                "met. Deliberately conservative: even at 25% the expected-value math beats "
                "every conventional foundation intervention. Sensitivity range covers "
                "skeptic and base-case scenarios.",
    display_name="Shirt Cascade Probability Given Seed",
    unit="rate",
    confidence="low",
    confidence_interval=(0.05, 0.6),
    distribution="beta",
    keywords=["shirt", "cascade", "probability", "viral", "social proof", "diffusion"],
    latex_symbol=r"P_{cascade,shirt}",
)

SHIRT_SEED_PROGRAM_TOTAL_USD = Parameter(
    float(SHIRT_SEED_WEARERS_THRESHOLD) * float(SHIRT_SEED_COST_PER_WEARER_USD),
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="calculated",
    description="Total foundation escrow required to fund the seed-wearer program: "
                "threshold of visible humans multiplied by blended cost per wearer. "
                "Held in Earth Optimization Prize assurance contract; refunded at "
                "structural EOP return rate if neither treaty passage nor target hit.",
    display_name="Shirt Seed Program Total Cost",
    unit="USD",
    formula="SHIRT_SEED_WEARERS_THRESHOLD × SHIRT_SEED_COST_PER_WEARER_USD",
    inputs=["SHIRT_SEED_WEARERS_THRESHOLD", "SHIRT_SEED_COST_PER_WEARER_USD"],
    compute=lambda ctx: ctx["SHIRT_SEED_WEARERS_THRESHOLD"] * ctx["SHIRT_SEED_COST_PER_WEARER_USD"],
    keywords=["shirt", "seed", "program", "total", "foundation", "escrow", "ask"],
    latex_symbol=r"C_{seed,total}",
)

SHIRT_VALUE_PER_WEARER_USD = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE) / float(GLOBAL_POPULATION_2024),
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="calculated",
    description="Treaty-trajectory economic value per shirt-wearing human: total treaty "
                "value (DFDA trial capacity plus efficacy lag elimination) divided by the "
                "8B-human target wearer base. This is the headline framing for the "
                "foundation pitch: each marginal wearer carries this much unrealized "
                "treaty value. Computationally identical to "
                "CORPORATE_DAMAGES_FORWARD_SETTLEMENT_VALUE_PER_CAPITA under a different "
                "semantic frame.",
    display_name="Shirt Value per Wearer",
    unit="USD",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE / GLOBAL_POPULATION_2024",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["shirt", "value", "per wearer", "per capita", "treaty value", "foundation pitch"],
    latex_symbol=r"V_{wearer}",
)

SHIRT_PROGRAM_ROI_RATIO = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE) / float(SHIRT_SEED_PROGRAM_TOTAL_USD),
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="calculated",
    description="Unconditional ROI ratio: treaty-trajectory total economic value divided "
                "by the seed-program escrow. Headline 'X-to-one' framing for foundations. "
                "Does NOT discount for cascade probability; see "
                "SHIRT_PROGRAM_EXPECTED_VALUE_PER_DOLLAR for the probability-weighted view.",
    display_name="Shirt Program ROI Ratio",
    unit="ratio",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE / SHIRT_SEED_PROGRAM_TOTAL_USD",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE", "SHIRT_SEED_PROGRAM_TOTAL_USD"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE"] / ctx["SHIRT_SEED_PROGRAM_TOTAL_USD"],
    keywords=["shirt", "roi", "ratio", "foundation", "headline", "value per dollar"],
    latex_symbol=r"ROI_{shirt}",
)

SHIRT_PROGRAM_EXPECTED_VALUE_PER_DOLLAR = Parameter(
    (float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE) * float(SHIRT_CASCADE_PROBABILITY_GIVEN_SEED)) / float(SHIRT_SEED_PROGRAM_TOTAL_USD),
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="calculated",
    description="Probability-weighted expected value per foundation-escrow dollar: treaty "
                "value multiplied by the cascade probability given seed, divided by the "
                "seed-program escrow. The defensible expected-value pitch for a skeptical "
                "foundation officer who does not want to bet on the headline ROI.",
    display_name="Shirt Program Expected Value per Dollar",
    unit="ratio",
    formula="(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE × SHIRT_CASCADE_PROBABILITY_GIVEN_SEED) / SHIRT_SEED_PROGRAM_TOTAL_USD",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE", "SHIRT_CASCADE_PROBABILITY_GIVEN_SEED", "SHIRT_SEED_PROGRAM_TOTAL_USD"],
    compute=lambda ctx: (ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE"] * ctx["SHIRT_CASCADE_PROBABILITY_GIVEN_SEED"]) / ctx["SHIRT_SEED_PROGRAM_TOTAL_USD"],
    keywords=["shirt", "expected value", "probability weighted", "foundation", "skeptic"],
    latex_symbol=r"EV_{shirt}",
)

# ── Laughter accounting for the funniest-joke-in-universe-history claim ──

HUMAN_LAUGHS_PER_DAY_AVERAGE = Parameter(
    17.0,
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="definition",
    description="Folkloric estimate of average adult laughter rate. Widely cited as "
                "approximately 17 laughs per day; primary sources are diffuse and the "
                "true value varies enormously across individuals, ages, and cultures. "
                "Used here as a planning constant for the quantitative-case argument "
                "in the shirt paper. Children laugh substantially more (~10x), so the "
                "value here is conservative for blended human population.",
    display_name="Human Laughs per Day (Average Adult)",
    unit="laughs",
    confidence="low",
    confidence_interval=(5.0, 50.0),
    distribution="lognormal",
    keywords=["laughs", "laughter", "comedy", "human behavior", "folklore"],
    latex_symbol=r"L_{day}",
)

HUMAN_LAUGHS_PER_HEALTHY_LIFE_YEAR = Parameter(
    float(HUMAN_LAUGHS_PER_DAY_AVERAGE) * 365.0,
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="calculated",
    description="Laughs occurring across one healthy life-year, computed as the adult "
                "daily laughter rate multiplied by days in a year. The conversion factor "
                "between DALYs averted (healthy life-years restored) and total laughs "
                "preserved.",
    display_name="Human Laughs per Healthy Life-Year",
    unit="laughs",
    formula="HUMAN_LAUGHS_PER_DAY_AVERAGE × 365",
    inputs=["HUMAN_LAUGHS_PER_DAY_AVERAGE"],
    compute=lambda ctx: ctx["HUMAN_LAUGHS_PER_DAY_AVERAGE"] * 365.0,
    keywords=["laughs", "laughter", "DALY", "healthy life year", "comedy"],
    latex_symbol=r"L_{year}",
)

SHIRT_INDUCED_LAUGHS_GAINED = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS) * float(HUMAN_LAUGHS_PER_HEALTHY_LIFE_YEAR),
    manual_ref="knowledge/appendix/joke.qmd",
    source_type="calculated",
    description="Conservative first-order count of additional laughs across human history "
                "attributable to the shirt-triggered cascade. Computed as DALYs averted "
                "(healthy life-years restored by disease eradication) multiplied by "
                "laughs per healthy life-year. Does not count second-order laughs in "
                "future generations of human and post-human civilization whose existence "
                "is contingent on cascade triggering.",
    display_name="Shirt-Induced Laughs Gained",
    unit="laughs",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS × HUMAN_LAUGHS_PER_HEALTHY_LIFE_YEAR",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS", "HUMAN_LAUGHS_PER_HEALTHY_LIFE_YEAR"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"] * ctx["HUMAN_LAUGHS_PER_HEALTHY_LIFE_YEAR"],
    keywords=["laughs", "shirt", "comedy", "DALY", "joke", "funniest"],
    latex_symbol=r"L_{shirt}",
)

# Historical & Comparison Multipliers
MILITARY_VS_MEDICAL_RESEARCH_RATIO = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_MED_RESEARCH_SPENDING,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Ratio of military spending to medical research spending",
    display_name="Ratio of Military Spending to Medical Research Spending",
    unit="ratio",
    formula="MILITARY_SPENDING ÷ MEDICAL_RESEARCH",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict"],
    inputs=['GLOBAL_MED_RESEARCH_SPENDING', 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_MED_RESEARCH_SPENDING"],
    latex_symbol=r"Ratio_{mil:RD}",  # LaTeX symbol for equations
)  # Calculated ratio of military to medical research spending

# WW2 demobilization: historical military spending in constant 2024 dollars
US_MILITARY_SPENDING_1939_ANNUAL_2024USD = Parameter(
    29_000_000_000,
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    source_ref=ReferenceID.US_MILITARY_SPENDING_HISTORICAL_CONSTANT_DOLLARS,
    source_type="external",
    description="US military spending in 1939 (pre-WW2 baseline) in constant 2024 dollars",
    display_name="US Military Spending in 1939 (Constant 2024 Dollars)",
    unit="USD",
    distribution="fixed",
    keywords=["1939", "pre-war", "baseline", "constant dollars", "inflation-adjusted"],
    latex_symbol=r"Spending_{US,1939}",
)

US_MILITARY_SPENDING_1945_PEAK_ANNUAL_2024USD = Parameter(
    1_420_000_000_000,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_ref=ReferenceID.US_MILITARY_SPENDING_HISTORICAL_CONSTANT_DOLLARS,
    source_type="external",
    description="US military spending at WW2 peak (1945) in constant 2024 dollars",
    display_name="US Military Spending at WW2 Peak (Constant 2024 Dollars)",
    unit="USD",
    distribution="fixed",
    keywords=["1945", "ww2", "peak", "constant dollars", "inflation-adjusted"],
    latex_symbol=r"Spending_{US,1945}",
)

US_MILITARY_SPENDING_1947_ANNUAL_2024USD = Parameter(
    176_000_000_000,
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_ref=ReferenceID.US_MILITARY_SPENDING_HISTORICAL_CONSTANT_DOLLARS,
    source_type="external",
    description="US military spending in 1947 (post-WW2 trough, 2 years after peak) in constant 2024 dollars",
    display_name="US Military Spending in 1947 (Constant 2024 Dollars)",
    unit="USD",
    distribution="fixed",
    keywords=["1947", "post-war", "demobilization", "trough", "constant dollars"],
    latex_symbol=r"Spending_{US,1947}",
)

US_MILITARY_SPENDING_2024_ANNUAL = Parameter(
    886_000_000_000,
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    source_ref=ReferenceID.US_MILITARY_SPENDING_HISTORICAL_CONSTANT_DOLLARS,
    source_type="external",
    description="US military spending in 2024 in constant dollars",
    display_name="US Military Spending in 2024",
    unit="USD",
    distribution="fixed",
    keywords=["2024", "current", "peacetime", "constant dollars"],
    latex_symbol=r"Spending_{US,2024}",
)

POST_WW2_MILITARY_CUT_PCT = Parameter(
    1 - (US_MILITARY_SPENDING_1947_ANNUAL_2024USD / US_MILITARY_SPENDING_1945_PEAK_ANNUAL_2024USD),
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Percentage US military spending cut after WW2 (1945-1947, inflation-adjusted: $1,420B to $176B in constant 2024 dollars)",
    display_name="Percentage Military Spending Cut After WW2",
    unit="percent",
    formula="1 - (US_MILITARY_SPENDING_1947 / US_MILITARY_SPENDING_1945_PEAK)",
    keywords=["88%", "demobilization", "ww2", "dod", "pentagon", "historical precedent"],
    inputs=["US_MILITARY_SPENDING_1947_ANNUAL_2024USD", "US_MILITARY_SPENDING_1945_PEAK_ANNUAL_2024USD"],
    compute=lambda ctx: 1 - (ctx["US_MILITARY_SPENDING_1947_ANNUAL_2024USD"] / ctx["US_MILITARY_SPENDING_1945_PEAK_ANNUAL_2024USD"]),
    latex_symbol=r"Cut_{WW2}",
)  # 87.6% cut in 2 years (1945->1947) in constant 2024 dollars

US_MILITARY_SPENDING_CURRENT_VS_PREWAR_MULTIPLIER = Parameter(
    US_MILITARY_SPENDING_2024_ANNUAL / US_MILITARY_SPENDING_1939_ANNUAL_2024USD,
    manual_ref="knowledge/problem/cost-of-war.qmd",
    source_type="calculated",
    description="Ratio of current US military spending to pre-WW2 baseline in constant dollars ($886B / $29B)",
    display_name="Current US Military Spending vs Pre-WW2 Baseline (Multiplier)",
    unit="x",
    formula="US_MILITARY_SPENDING_2024 / US_MILITARY_SPENDING_1939",
    keywords=["multiplier", "30x", "ratchet", "inflation-adjusted", "peacetime"],
    inputs=["US_MILITARY_SPENDING_2024_ANNUAL", "US_MILITARY_SPENDING_1939_ANNUAL_2024USD"],
    compute=lambda ctx: ctx["US_MILITARY_SPENDING_2024_ANNUAL"] / ctx["US_MILITARY_SPENDING_1939_ANNUAL_2024USD"],
    latex_symbol=r"Ratio_{US,2024:1939}",
)

US_1939_MILITARY_SPENDING_PCT_LOWER_THAN_CURRENT = Parameter(
    1 - (US_MILITARY_SPENDING_1939_ANNUAL_2024USD / US_MILITARY_SPENDING_2024_ANNUAL),
    manual_ref="knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="How much lower pre-WW2 (1939) US military spending was than today's peacetime budget, in constant 2024 dollars",
    display_name="Pre-WW2 US Military Spending % Lower than Current",
    unit="percent",
    formula="1 - (US_MILITARY_SPENDING_1939 / US_MILITARY_SPENDING_2024)",
    keywords=["97%", "pre-ww2", "peacetime", "ratchet", "historical baseline"],
    inputs=["US_MILITARY_SPENDING_1939_ANNUAL_2024USD", "US_MILITARY_SPENDING_2024_ANNUAL"],
    compute=lambda ctx: 1 - (ctx["US_MILITARY_SPENDING_1939_ANNUAL_2024USD"] / ctx["US_MILITARY_SPENDING_2024_ANNUAL"]),
    latex_symbol=r"Pct_{1939<2024}",
)

SWITZERLAND_DEFENSE_SPENDING_PCT = Parameter(
    0.007,
    manual_ref="knowledge/problem.qmd",
    source_ref=ReferenceID.SWISS_MILITARY_BUDGET_0_7_PCT_GDP,
    source_type="external",
    description="Switzerland's defense spending as percentage of GDP (0.7%)",
    display_name="Switzerland's Defense Spending as Percentage of GDP",
    unit="rate",
    keywords=["1%", "armed forces", "international agreement", "peace treaty", "conflict", "costs", "funding"],
    latex_symbol=r"Spending_{CH,def}",  # LaTeX symbol for equations
)  # Switzerland's defense spending as percentage of GDP

SWITZERLAND_GDP_PER_CAPITA_K = Parameter(
    93_000,
    manual_ref="knowledge/problem.qmd",
    source_ref=ReferenceID.SWISS_VS_US_GDP_PER_CAPITA,
    source_type="external",
    description="Switzerland GDP per capita",
    display_name="Switzerland GDP per Capita",
    unit="USD",
    keywords=["93k", "average person", "individual", "per person", "household benefit", "per individual", "typical individual"],
    latex_symbol=r"GDP_{CH,pc}",  # LaTeX symbol for equations
)  # Thousands USD, Switzerland GDP per capita, for comparison

AVERAGE_MARKET_RETURN_PCT = Parameter(
    0.10,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref=ReferenceID.WARREN_BUFFETT_CAREER_AVERAGE_RETURN_20_PCT,
    source_type="external",
    description="Average annual stock market return (10%)",
    display_name="Average Annual Stock Market Return",
    unit="rate",
    keywords=["10%", "benefit", "profit", "yield", "yearly", "average", "market"],
    latex_symbol=r"r_{market}",  # LaTeX symbol for equations
)  # Average market return percentage for portfolio comparisons

# Lobbyist compensation & incentives
LOBBYIST_BOND_INVESTMENT_MAX = Parameter(
    20_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_type="definition",
    description="Maximum bond investment for lobbyist incentives",
    display_name="Maximum Bond Investment for Lobbyist Incentives",
    unit="USD",
    keywords=["20.0m", "social impact bond", "sib", "impact investing", "pay for success", "capital", "finance"],
    latex_symbol=r"Invest_{lobby,max}",  # LaTeX symbol for equations
)  # Millions USD, bond investment for lobbyists (max incentive)

LOBBYIST_SALARY_MIN_K = Parameter(
    500_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref=ReferenceID.LOBBYIST_STATISTICS_DC,
    source_type="external",
    description="Minimum annual lobbyist salary range",
    display_name="Minimum Annual Lobbyist Salary Range",
    unit="USD",
    keywords=["500k", "yearly", "lobbyist", "min", "pa", "per annum", "per year"],
    latex_symbol=r"Salary_{lobby,min}",  # LaTeX symbol for equations
)  # $500K minimum for lobbyist salaries

LOBBYIST_SALARY_MAX = Parameter(
    2_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref=ReferenceID.LOBBYIST_STATISTICS_DC,
    source_type="external",
    description="Maximum annual lobbyist salary range",
    display_name="Maximum Annual Lobbyist Salary Range",
    unit="USD",
    keywords=["2.0m", "yearly", "lobbyist", "max", "pa", "per annum", "per year"],
    latex_symbol=r"Salary_{lobby,max}",  # LaTeX symbol for equations
)  # $2M maximum for top lobbyist salaries

# Infinite ROI equation - redirected spending means $0 new cost
# Note: Uses hardcoded latex because float('inf') breaks Monte Carlo simulation
# The dividend value is calculated dynamically from TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS
_infinite_roi_dividends = round(float(TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS) / 1e9)
TREATY_REDIRECTED_SPENDING_INFINITE_ROI = Parameter(
    0,  # Placeholder - conceptual parameter for the latex equation only
    manual_ref="knowledge/solution/1-percent-treaty.qmd",
    source_type="definition",
    description="ROI when redirecting existing spending (no new costs = infinite return)",
    display_name="Infinite ROI from Redirected Spending",
    unit="ratio",
    formula="COMBINED_DIVIDENDS ÷ 0 = ∞",
    keywords=["infinite", "roi", "redirected", "spending", "zero cost"],
    latex=f'''\\text{{ROI}} = \\frac{{\\text{{Annual Benefits}}}}{{\\text{{New Spending}}}} = \\frac{{\\${_infinite_roi_dividends}B}}{{0}} = \\infty''',
    latex_symbol=r"ROI_{\infty}",  # LaTeX symbol for equations
)

TREATY_BENEFIT_MULTIPLIER_VS_VACCINES = Parameter(
    TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS / CHILDHOOD_VACCINATION_ANNUAL_BENEFIT,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_type="calculated",
    description="Treaty system benefit multiplier vs childhood vaccination programs",
    display_name="Treaty System Benefit Multiplier vs Childhood Vaccination Programs",
    unit="x",
    formula="TREATY_CONSERVATIVE_BENEFIT ÷ CHILDHOOD_VACCINATION_BENEFIT",
    keywords=["1%", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple"],
    inputs=['CHILDHOOD_VACCINATION_ANNUAL_BENEFIT', 'TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS'],
    compute=lambda ctx: ctx["TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS"] / ctx["CHILDHOOD_VACCINATION_ANNUAL_BENEFIT"],
    latex_symbol=r"k_{treaty:vax}",  # LaTeX symbol for equations
)  # ~11:1 ratio (treaty system is 11x larger in economic impact)



# ---
# PERSONAL LIFETIME WEALTH CALCULATIONS
# ---


def calculate_gdp_growth_boost(treaty_pct: float) -> float:
    """
    Calculate annual GDP growth from military spending redirection.

    Calibrated so a 30% reallocation maps to ~5.5 percentage points
    of annual growth boost at baseline spillover assumptions.

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)

    Returns:
        Total annual GDP growth rate (baseline + boost)
    """
    base_growth = float(GDP_BASELINE_GROWTH_RATE)
    # Inline calibration: 30% reallocation -> MILITARY_REDIRECT_GDP_BOOST_AT_30PCT.
    # Spillover normalization keeps the 30% anchor unchanged at spillover=2.
    effective_coeff = (
        float(MILITARY_REDIRECT_GDP_BOOST_AT_30PCT) / 0.30
    ) * (float(RD_SPILLOVER_MULTIPLIER) / 2.0)
    return base_growth + treaty_pct * effective_coeff


def calculate_trial_capacity_multiplier(treaty_pct: float) -> float:
    """
    Calculate trial capacity multiplier for a given treaty percentage.

    Uses linear scaling from the base DFDA_TRIAL_CAPACITY_MULTIPLIER at 1% treaty,
    then applies a physical cap from willing participant availability.

    Formula:
        Multiplier = min(
            DFDA_TRIAL_CAPACITY_MULTIPLIER × (treaty_pct / 0.01),
            DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL
        )

    Examples (assuming base multiplier of ~12.3x):
    - 1% treaty: 12.3 × (0.01 / 0.01) = 12.3x
    - 2% treaty: 12.3 × (0.02 / 0.01) = 24.6x
    - 5% treaty: 12.3 × (0.05 / 0.01) = 61.5x
    - 10% treaty: 12.3 × (0.10 / 0.01) = 123x

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)

    Returns:
        Trial capacity multiplier (scales with treaty percentage)
    """
    scaled = float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (treaty_pct / 0.01)
    physical_cap = float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL)
    return min(scaled, physical_cap)


def compound_sum(annual_benefit: float, years: float, growth_rate: float, discount_rate: float = 0.03) -> float:
    """
    Calculate present value of compounding annual benefits

    Formula: PV = Σ(annual_benefit × (1 + growth_rate)^t / (1 + discount_rate)^t)

    LaTeX:
        PV = \\sum_{t=1}^{T} \frac{Benefit_{annual} \times (1 + r_{growth})^t}{(1 + r_{discount})^t}

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


# ---
# GDP TRAJECTORY PARAMETERS AND FUNCTIONS
# ---
# Models three diverging GDP trajectories over 20 years:
# Current Trajectory (status quo), Treaty Trajectory (military+health), Wishonia Trajectory (full package)

RD_SPILLOVER_MULTIPLIER = Parameter(
    2.0,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="definition",
    distribution=DistributionType.NORMAL,
    description="R&D spillover multiplier: each $1 in directed medical research produces $2 in "
                "adjacent sector GDP growth (biotech, AI, computing, materials science, manufacturing). "
                "Conservative estimate; military R&D spillover produced the internet, GPS, jet engines. "
                "Medical R&D spillover already produced CRISPR, mRNA platforms, AI protein folding.",
    display_name="R&D Spillover Multiplier",
    unit="x",
    confidence="medium",
    confidence_interval=(1.5, 2.5),
    std_error=0.25,
    keywords=["R&D", "spillover", "multiplier", "innovation"],
    latex_symbol=r"m_{spillover}",
)

GDP_BASELINE_GROWTH_RATE = Parameter(
    0.025,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="definition",
    distribution="fixed",
    description="Status-quo baseline annual global GDP growth rate.",
    display_name="Baseline Global GDP Growth Rate",
    unit="rate",
    keywords=["GDP", "baseline", "growth", "status quo", "2.5%"],
    latex_symbol=r"g_{base}",
)

MILITARY_REDIRECT_GDP_BOOST_AT_30PCT = Parameter(
    0.055,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="definition",
    distribution=DistributionType.NORMAL,
    description="Historical calibration target: 30% military reallocation maps to ~5.5 percentage points annual GDP growth boost.",
    display_name="GDP Growth Boost at 30% Military Reallocation",
    unit="rate",
    confidence="medium",
    confidence_interval=(0.035, 0.075),
    std_error=0.01,
    keywords=["GDP", "military", "reallocation", "historical calibration", "5.5%"],
    latex_symbol=r"\Delta g_{30\%}",
)

DISEASE_BURDEN_GDP_DRAG_PCT = Parameter(
    0.13,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="external",
    distribution="fixed",
    description="Fraction of GDP currently lost to disease (productivity losses + medical costs diverted "
                "from productive use). $5T productivity loss + $9.9T direct medical costs = $14.9T on $115T GDP = ~13%. "
                "As diseases are progressively cured, this drag is recovered as GDP growth. This is the "
                "missing factor that makes the treaty trajectory look like a singularity rather than "
                "a modest improvement.",
    display_name="Disease Burden as % of GDP",
    unit="percent",
    keywords=["disease", "burden", "GDP", "drag", "productivity", "medical"],
    latex_symbol=r"d_{disease}",
)

GLOBAL_POPULATION_2045_PROJECTED = Parameter(
    9_200_000_000,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_ref=ReferenceID.GLOBAL_POPULATION_8_BILLION,
    source_type="external",
    distribution="fixed",
    description="UN World Population Prospects 2022 median projection for 2045.",
    display_name="Global Population 2045 (Projected)",
    unit="of people",
    keywords=["population", "2045", "projection", "UN", "global"],
    latex_symbol=r"Pop_{2045}",
)

WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE = Parameter(
    POST_WW2_MILITARY_CUT_PCT,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Maximum physically demonstrated military reallocation share, anchored to post-WW2 US demobilization.",
    display_name="Wishonia Military Reallocation Physical Max Share",
    unit="rate",
    formula="POST_WW2_MILITARY_CUT_PCT",
    inputs=["POST_WW2_MILITARY_CUT_PCT"],
    compute=lambda ctx: ctx["POST_WW2_MILITARY_CUT_PCT"],
    keywords=["wishonia", "military", "reallocation", "physical", "max", "post-ww2"],
    latex_symbol=r"s_{mil,max}",
)

TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15 = Parameter(
    (0.01 * 3 + min(0.02, _S_ratchet) * 4 + min(0.05, _S_ratchet) * 5 + _S_ratchet * 3) / 15,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Average military-to-medicine reallocation share over 15 years under the treaty "
                "take-hold path (1% for 3 years, 2% for 4 years, 5% for 5 years, terminal ratchet "
                "share for 3 years). Binds the single ratchet knob: at "
                "TREATY_RATCHET_TERMINAL_SHARE = 0.01 this degrades to a flat 1%.",
    display_name="Treaty Effective Reallocation Share (Year 15)",
    unit="rate",
    formula="(0.01×3 + min(0.02, TREATY_RATCHET_TERMINAL_SHARE)×4 + min(0.05, TREATY_RATCHET_TERMINAL_SHARE)×5 + TREATY_RATCHET_TERMINAL_SHARE×3) / 15",
    inputs=["TREATY_RATCHET_TERMINAL_SHARE"],
    compute=lambda ctx: (
        0.01 * 3
        + min(0.02, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 4
        + min(0.05, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 5
        + ctx["TREATY_RATCHET_TERMINAL_SHARE"] * 3
    ) / 15,
    keywords=["treaty", "reallocation", "share", "15 year", "ratchet"],
    latex_symbol=r"\bar{s}_{treaty,15}",
)

TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20 = Parameter(
    (0.01 * 3 + min(0.02, _S_ratchet) * 4 + min(0.05, _S_ratchet) * 5 + _S_ratchet * 8) / 20,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Average military-to-medicine reallocation share over 20 years under the treaty "
                "take-hold path (1% for 3 years, 2% for 4 years, 5% for 5 years, terminal ratchet "
                "share for 8 years). Binds the single ratchet knob: at "
                "TREATY_RATCHET_TERMINAL_SHARE = 0.01 this degrades to a flat 1%.",
    display_name="Treaty Effective Reallocation Share (Year 20)",
    unit="rate",
    formula="(0.01×3 + min(0.02, TREATY_RATCHET_TERMINAL_SHARE)×4 + min(0.05, TREATY_RATCHET_TERMINAL_SHARE)×5 + TREATY_RATCHET_TERMINAL_SHARE×8) / 20",
    inputs=["TREATY_RATCHET_TERMINAL_SHARE"],
    compute=lambda ctx: (
        0.01 * 3
        + min(0.02, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 4
        + min(0.05, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) * 5
        + ctx["TREATY_RATCHET_TERMINAL_SHARE"] * 8
    ) / 20,
    keywords=["treaty", "reallocation", "share", "20 year", "ratchet"],
    latex_symbol=r"\bar{s}_{treaty,20}",
)

TREATY_DISEASE_CURE_FRACTION_20YR = Parameter(
    min(
        1.0,
        (
            3 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (0.01 / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
            + 4 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (min(0.02, _S_ratchet) / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
            + 5 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (min(0.05, _S_ratchet) / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
            + 8 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (_S_ratchet / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
        )
        / float(STATUS_QUO_QUEUE_CLEARANCE_YEARS),
    ),
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Fraction of currently untreatable diseases with a first effective treatment by "
                "year 20 under the treaty: queue progress integrated over the ratchet schedule, "
                "with trial capacity scaling linearly with funding up to the physical participant "
                "ceiling. Binds the single ratchet knob: at TREATY_RATCHET_TERMINAL_SHARE = 0.01 "
                "(ratchet off) this degrades to 20/36 of the queue (~56%); on the central schedule "
                "the queue clears around year 12, so the central is 100%. The ~36-year "
                "queue-clearance figure quoted elsewhere is the flat-1% case by construction.",
    display_name="Treaty Disease Cure Fraction (20yr, Ratchet Schedule)",
    unit="rate",
    formula="min(1.0, (3×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(0.01/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) + 4×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(min(0.02, TREATY_RATCHET_TERMINAL_SHARE)/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) + 5×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(min(0.05, TREATY_RATCHET_TERMINAL_SHARE)/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) + 8×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(TREATY_RATCHET_TERMINAL_SHARE/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL)) ÷ STATUS_QUO_QUEUE_CLEARANCE_YEARS)",
    inputs=["DFDA_TRIAL_CAPACITY_MULTIPLIER", "DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL",
            "TREATY_RATCHET_TERMINAL_SHARE", "STATUS_QUO_QUEUE_CLEARANCE_YEARS"],
    compute=lambda ctx: min(
        1.0,
        (
            3 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (0.01 / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
            + 4 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (min(0.02, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
            + 5 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (min(0.05, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
            + 8 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (ctx["TREATY_RATCHET_TERMINAL_SHARE"] / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
        )
        / ctx["STATUS_QUO_QUEUE_CLEARANCE_YEARS"],
    ),
    keywords=["treaty", "disease", "cure fraction", "20 year", "queue", "ratchet"],
    latex_symbol=r"f_{cure,20,treaty}",
)

TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_20 = Parameter(
    TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20 * ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT / 0.30) * (RD_SPILLOVER_MULTIPLIER / 2.0)),
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Annual GDP growth bonus by year 20 from redirecting military spending to medical research under the treaty take-hold path, "
                "including R&D spillovers.",
    display_name="Treaty Redirect GDP Growth Bonus (Year 20)",
    unit="rate",
    formula="TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20 × ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT ÷ 0.30) × (RD_SPILLOVER_MULTIPLIER ÷ 2.0))",
    inputs=["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20", "MILITARY_REDIRECT_GDP_BOOST_AT_30PCT", "RD_SPILLOVER_MULTIPLIER"],
    compute=lambda ctx: ctx["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20"] * ((ctx["MILITARY_REDIRECT_GDP_BOOST_AT_30PCT"] / 0.30) * (ctx["RD_SPILLOVER_MULTIPLIER"] / 2.0)),
    keywords=["treaty", "GDP", "growth", "redirect", "R&D", "spillover", "20 year"],
    latex_symbol=r"g_{redirect,treaty,20}",
)

TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_20 = Parameter(
    (PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / GLOBAL_GDP_2025)
    * (TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20 / TREATY_REDUCTION_PCT)
    * PEACE_DIVIDEND_CONFLICT_ELASTICITY,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Annual GDP growth bonus by year 20 from explicit avoided war-cost drag under the treaty take-hold path.",
    display_name="Treaty Peace Recovery GDP Growth Bonus (Year 20)",
    unit="rate",
    formula="(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT ÷ GLOBAL_GDP_2025) × (TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20 ÷ TREATY_REDUCTION_PCT) × PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    inputs=[
        "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
        "GLOBAL_GDP_2025",
        "TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20",
        "TREATY_REDUCTION_PCT",
        "PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    ],
    compute=lambda ctx: (
        (ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"] / ctx["GLOBAL_GDP_2025"])
        * (ctx["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20"] / ctx["TREATY_REDUCTION_PCT"])
        * ctx["PEACE_DIVIDEND_CONFLICT_ELASTICITY"]
    ),
    keywords=["treaty", "GDP", "growth", "peace dividend", "war costs", "20 year"],
    latex_symbol=r"g_{peace,treaty,20}",
)

TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_20 = Parameter(
    (GLOBAL_CYBERCRIME_COST_ANNUAL_2025 / GLOBAL_GDP_2025)
    * TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20
    * PEACE_DIVIDEND_CONFLICT_ELASTICITY,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Annual GDP growth bonus by year 20 from reducing cybercrime drag as the treaty weakens the destructive economy feedback loop.",
    display_name="Treaty Cybercrime Recovery GDP Growth Bonus (Year 20)",
    unit="rate",
    formula="(GLOBAL_CYBERCRIME_COST_ANNUAL_2025 ÷ GLOBAL_GDP_2025) × TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20 × PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    inputs=[
        "GLOBAL_CYBERCRIME_COST_ANNUAL_2025",
        "GLOBAL_GDP_2025",
        "TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20",
        "PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    ],
    compute=lambda ctx: (
        (ctx["GLOBAL_CYBERCRIME_COST_ANNUAL_2025"] / ctx["GLOBAL_GDP_2025"])
        * ctx["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_20"]
        * ctx["PEACE_DIVIDEND_CONFLICT_ELASTICITY"]
    ),
    keywords=["treaty", "GDP", "growth", "cybercrime", "destructive economy", "20 year"],
    latex_symbol=r"g_{cyber,treaty,20}",
)

TREATY_HEALTH_RECOVERY_ANNUALIZATION_YEARS = Parameter(
    20,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="definition",
    description="Annualization horizon for the treaty health recovery GDP-drag term.",
    display_name="Treaty Health Recovery Annualization Horizon",
    unit="years",
    keywords=["treaty", "GDP", "growth", "health", "annualization", "20 year"],
    latex_symbol=r"H_{health,treaty}",
    distribution="fixed",
)

TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_20 = Parameter(
    ((1 + TREATY_DISEASE_CURE_FRACTION_20YR * DISEASE_BURDEN_GDP_DRAG_PCT) ** (1 / TREATY_HEALTH_RECOVERY_ANNUALIZATION_YEARS)) - 1,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Annualized GDP growth bonus by year 20 from lower disease burden under the treaty path.",
    display_name="Treaty Health Recovery GDP Growth Bonus (Year 20)",
    unit="rate",
    formula="((1 + TREATY_DISEASE_CURE_FRACTION_20YR × DISEASE_BURDEN_GDP_DRAG_PCT)^(1 ÷ TREATY_HEALTH_RECOVERY_ANNUALIZATION_YEARS)) - 1",
    inputs=[
        "TREATY_DISEASE_CURE_FRACTION_20YR",
        "DISEASE_BURDEN_GDP_DRAG_PCT",
        "TREATY_HEALTH_RECOVERY_ANNUALIZATION_YEARS",
    ],
    compute=lambda ctx: (
        (
            1
            + ctx["TREATY_DISEASE_CURE_FRACTION_20YR"] * ctx["DISEASE_BURDEN_GDP_DRAG_PCT"]
        ) ** (1 / ctx["TREATY_HEALTH_RECOVERY_ANNUALIZATION_YEARS"])
    ) - 1,
    keywords=["treaty", "GDP", "growth", "health", "disease burden", "20 year"],
    latex_symbol=r"g_{health,treaty,20}",
)

WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL = Parameter(
    min(
        1.0,
        NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR
        * min(
            DFDA_TRIAL_CAPACITY_MULTIPLIER * (WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE / 0.01),
            DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL,
        )
        * 20
        / DISEASES_WITHOUT_EFFECTIVE_TREATMENT,
    ),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Wishonia disease-cure fraction over 20 years under full implementation. "
                "Uses full trial-capacity scaling and applies an upper bound of 100% of untreated disease classes.",
    display_name="Wishonia Disease Cure Fraction (20yr, Full Implementation)",
    unit="rate",
    formula="min(1.0, NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR × min(TRIAL_CAPACITY_MULTIPLIER × (WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE ÷ 0.01), MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) × 20 ÷ DISEASES_WITHOUT_EFFECTIVE_TREATMENT)",
    inputs=[
        "NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR",
        "DFDA_TRIAL_CAPACITY_MULTIPLIER",
        "WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE",
        "DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL",
        "DISEASES_WITHOUT_EFFECTIVE_TREATMENT",
    ],
    compute=lambda ctx: min(
        1.0,
        ctx["NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR"]
        * min(
            ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"]
            * (ctx["WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE"] / 0.01),
            ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"],
        )
        * 20
        / ctx["DISEASES_WITHOUT_EFFECTIVE_TREATMENT"],
    ),
    keywords=["wishonia", "disease", "cure fraction", "20 year", "full implementation"],
    latex_symbol=r"f_{cure,20,wish}",
    distribution="fixed",  # Saturates at 1.0 ceiling under full-implementation parameters
)

CURRENT_TRAJECTORY_GDP_YEAR_20 = Parameter(
    GLOBAL_GDP_2025 * ((1 + GDP_BASELINE_GROWTH_RATE) ** 20),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Global GDP at year 20 under status-quo current trajectory growth.",
    display_name="Current Trajectory GDP at Year 20",
    unit="USD",
    formula="GLOBAL_GDP_2025 × (1 + GDP_BASELINE_GROWTH_RATE)^20",
    keywords=["GDP", "baseline", "baseline", "year 20"],
    inputs=["GLOBAL_GDP_2025", "GDP_BASELINE_GROWTH_RATE"],
    compute=lambda ctx: ctx["GLOBAL_GDP_2025"] * ((1 + ctx["GDP_BASELINE_GROWTH_RATE"]) ** 20),
    latex_symbol=r"GDP_{base,20}",
)

CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20 = Parameter(
    CURRENT_TRAJECTORY_GDP_YEAR_20 / GLOBAL_POPULATION_2045_PROJECTED,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Average income (GDP per capita) at year 20 under current trajectory trajectory.",
    display_name="Current Trajectory Average Income at Year 20",
    unit="USD",
    formula="CURRENT_TRAJECTORY_GDP_YEAR_20 ÷ GLOBAL_POPULATION_2045_PROJECTED",
    keywords=["income", "per capita", "baseline", "year 20", "average"],
    inputs=["CURRENT_TRAJECTORY_GDP_YEAR_20", "GLOBAL_POPULATION_2045_PROJECTED"],
    compute=lambda ctx: ctx["CURRENT_TRAJECTORY_GDP_YEAR_20"] / ctx["GLOBAL_POPULATION_2045_PROJECTED"],
    latex_symbol=r"\bar{y}_{base,20}",
    distribution="fixed",  # All upstream inputs are distribution="fixed"
)


TREATY_TRAJECTORY_GDP_YEAR_20 = Parameter(
    GLOBAL_GDP_2025
    * (
        1
        + GDP_BASELINE_GROWTH_RATE
        + TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_20
        + TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_20
        + TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_20
        + TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_20
    ) ** 20,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Projected global GDP at year 20 under the optimistic treaty take-hold path. "
                "Compounds baseline growth plus explicit military redirect spillovers, peace dividend recovery, "
                "cybercrime drag recovery, and health recovery from lower disease burden.",
    display_name="Treaty Trajectory GDP at Year 20",
    unit="USD",
    formula="GLOBAL_GDP_2025 × (1 + GDP_BASELINE_GROWTH_RATE + TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_20 + TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_20 + TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_20 + TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_20)^20",
    keywords=["GDP", "treaty", "projection", "20 years", "optimistic"],
    inputs=[
        "GLOBAL_GDP_2025",
        "GDP_BASELINE_GROWTH_RATE",
        "TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_20",
        "TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_20",
        "TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_20",
        "TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_20",
    ],
    compute=lambda ctx: (
        ctx["GLOBAL_GDP_2025"]
        * (
            1
            + ctx["GDP_BASELINE_GROWTH_RATE"]
            + ctx["TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_20"]
            + ctx["TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_20"]
            + ctx["TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_20"]
            + ctx["TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_20"]
        ) ** 20
    ),
    latex_symbol=r"GDP_{treaty,20}",
)

TREATY_TRAJECTORY_CAGR_YEAR_20 = Parameter(
    (TREATY_TRAJECTORY_GDP_YEAR_20 / GLOBAL_GDP_2025) ** (1 / 20) - 1,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Compound annual growth rate implied by Treaty Trajectory GDP trajectory over 20 years.",
    display_name="Treaty Trajectory CAGR (20 Years)",
    unit="rate",
    formula="(TREATY_TRAJECTORY_GDP_YEAR_20 ÷ GLOBAL_GDP_2025)^(1/20) - 1",
    keywords=["CAGR", "GDP", "wishonia", "core", "20 years"],
    inputs=["TREATY_TRAJECTORY_GDP_YEAR_20", "GLOBAL_GDP_2025"],
    compute=lambda ctx: (ctx["TREATY_TRAJECTORY_GDP_YEAR_20"] / ctx["GLOBAL_GDP_2025"]) ** (1 / 20) - 1,
    latex_symbol=r"g_{treaty,CAGR}",
)

TREATY_TRAJECTORY_GDP_VS_CURRENT_TRAJECTORY_MULTIPLIER_YEAR_20 = Parameter(
    TREATY_TRAJECTORY_GDP_YEAR_20 / CURRENT_TRAJECTORY_GDP_YEAR_20,
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Treaty Trajectory GDP at year 20 as a multiple of current trajectory GDP at year 20.",
    display_name="Treaty Trajectory vs Current Trajectory GDP Multiplier (Year 20)",
    unit="x",
    formula="TREATY_TRAJECTORY_GDP_YEAR_20 ÷ CURRENT_TRAJECTORY_GDP_YEAR_20",
    keywords=["GDP", "wishonia", "core", "baseline", "multiplier", "year 20"],
    inputs=["TREATY_TRAJECTORY_GDP_YEAR_20", "CURRENT_TRAJECTORY_GDP_YEAR_20"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_GDP_YEAR_20"] / ctx["CURRENT_TRAJECTORY_GDP_YEAR_20"],
    latex_symbol=r"k_{treaty:base,20}",
)

TREATY_TRAJECTORY_AVG_INCOME_YEAR_20 = Parameter(
    float(TREATY_TRAJECTORY_GDP_YEAR_20) / float(GLOBAL_POPULATION_2045_PROJECTED),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Average income (GDP per capita) at year 20 under the Treaty Trajectory.",
    display_name="Treaty Trajectory Average Income at Year 20",
    unit="USD",
    formula="TREATY_TRAJECTORY_GDP_YEAR_20 / GLOBAL_POPULATION_2045_PROJECTED",
    keywords=["income", "per capita", "wishonia", "core", "year 20", "average"],
    inputs=["TREATY_TRAJECTORY_GDP_YEAR_20", "GLOBAL_POPULATION_2045_PROJECTED"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_GDP_YEAR_20"] / ctx["GLOBAL_POPULATION_2045_PROJECTED"],
    latex_symbol=r"\bar{y}_{treaty,20}",
)


WISHONIA_TRAJECTORY_GDP_YEAR_20 = Parameter(
    GLOBAL_GDP_2025
    * (
        (
            1
            + GDP_BASELINE_GROWTH_RATE
            + (0.5 * WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE)
            * ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT / 0.30) * (RD_SPILLOVER_MULTIPLIER / 2.0))
            + ((1 + WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL * DISEASE_BURDEN_GDP_DRAG_PCT) ** (1 / 20) - 1)
            + (
                (
                    1
                    + (
                        0.5
                        * (
                        (
                            POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST
                        )
                        / GLOBAL_GDP_2025
                        )
                    )
                    * (ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT / ECONOMIC_MULTIPLIER_MILITARY_SPENDING - 1)
                ) ** (1 / 20)
                - 1
            )
        ) ** 3
    )
    * (
        (
            1
            + GDP_BASELINE_GROWTH_RATE
            + WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE
            * ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT / 0.30) * (RD_SPILLOVER_MULTIPLIER / 2.0))
            + ((1 + WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL * DISEASE_BURDEN_GDP_DRAG_PCT) ** (1 / 20) - 1)
            + (
                (
                    1
                    + (
                        (
                            POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST
                        )
                        / GLOBAL_GDP_2025
                    )
                    * (ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT / ECONOMIC_MULTIPLIER_MILITARY_SPENDING - 1)
                ) ** (1 / 20)
                - 1
            )
        ) ** 17
    ),
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Projected global GDP at year 20 under the Wishonia Trajectory. "
                "Model applies all Wishonia policy channels and redirects the full Political Dysfunction Tax "
                "non-health opportunity pool to highest-marginal-value uses. Health recovery is modeled separately "
                "through disease burden removal to avoid overlap. Military and non-health reallocation effects are "
                "ramped at 50% intensity for the first 3 years, then 100% for years 4-20, reflecting implementation lag. "
                "Military reallocation uses a physically demonstrated upper bound (post-WW2 demobilization) rather than an arbitrary policy cap.",
    display_name="Wishonia Trajectory GDP at Year 20",
    unit="USD",
    formula="GLOBAL_GDP_2025 × (1 + g_ramp)^3 × (1 + g_full)^17, where years 1-3 use 50% of military and non-health reallocation intensity, and years 4-20 use 100%; both include disease-burden recovery",
    latex=r"GDP_{wish,20}=GDP_0(1+g_{ramp})^{3}(1+g_{full})^{17}",
    keywords=["GDP", "wishonia", "projection", "treaty"],
    inputs=[
        "GLOBAL_GDP_2025",
        "GDP_BASELINE_GROWTH_RATE",
        "WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE",
        "MILITARY_REDIRECT_GDP_BOOST_AT_30PCT",
        "RD_SPILLOVER_MULTIPLIER",
        "WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL",
        "DISEASE_BURDEN_GDP_DRAG_PCT",
        "POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST",
        "POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST",
        "POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST",
        "ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT",
        "ECONOMIC_MULTIPLIER_MILITARY_SPENDING",
    ],
    compute=lambda ctx: (
        ctx["GLOBAL_GDP_2025"]
        * (
            (
                1
                + ctx["GDP_BASELINE_GROWTH_RATE"]
                + (0.5 * ctx["WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE"])
                * ((ctx["MILITARY_REDIRECT_GDP_BOOST_AT_30PCT"] / 0.30) * (ctx["RD_SPILLOVER_MULTIPLIER"] / 2.0))
                + ((1 + ctx["WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL"] * ctx["DISEASE_BURDEN_GDP_DRAG_PCT"]) ** (1 / 20) - 1)
                + (
                    (
                        1
                        + (
                            0.5
                            * (
                            (
                                ctx["POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST"]
                            )
                            / ctx["GLOBAL_GDP_2025"]
                            )
                        )
                        * (ctx["ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT"] / ctx["ECONOMIC_MULTIPLIER_MILITARY_SPENDING"] - 1)
                    ) ** (1 / 20)
                    - 1
                )
            ) ** 3
        )
        * (
            (
                1
                + ctx["GDP_BASELINE_GROWTH_RATE"]
                + ctx["WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE"]
                * ((ctx["MILITARY_REDIRECT_GDP_BOOST_AT_30PCT"] / 0.30) * (ctx["RD_SPILLOVER_MULTIPLIER"] / 2.0))
                + ((1 + ctx["WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL"] * ctx["DISEASE_BURDEN_GDP_DRAG_PCT"]) ** (1 / 20) - 1)
                + (
                    (
                        1
                        + (
                            (
                                ctx["POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST"]
                            )
                            / ctx["GLOBAL_GDP_2025"]
                        )
                        * (ctx["ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT"] / ctx["ECONOMIC_MULTIPLIER_MILITARY_SPENDING"] - 1)
                    ) ** (1 / 20)
                    - 1
                )
            ) ** 17
        )
    ),
    latex_symbol=r"GDP_{wish,20}",
)

WISHONIA_TRAJECTORY_CAGR_YEAR_20 = Parameter(
    (WISHONIA_TRAJECTORY_GDP_YEAR_20 / GLOBAL_GDP_2025) ** (1 / 20) - 1,
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Compound annual growth rate implied by Wishonia Trajectory GDP trajectory over 20 years.",
    display_name="Wishonia Trajectory CAGR (20 Years)",
    unit="rate",
    formula="(WISHONIA_TRAJECTORY_GDP_YEAR_20 ÷ GLOBAL_GDP_2025)^(1/20) - 1",
    keywords=["CAGR", "GDP", "wishonia", "20 years"],
    inputs=["WISHONIA_TRAJECTORY_GDP_YEAR_20", "GLOBAL_GDP_2025"],
    compute=lambda ctx: (ctx["WISHONIA_TRAJECTORY_GDP_YEAR_20"] / ctx["GLOBAL_GDP_2025"]) ** (1 / 20) - 1,
    latex_symbol=r"g_{wish,CAGR}",
)

WISHONIA_TRAJECTORY_GDP_VS_CURRENT_TRAJECTORY_MULTIPLIER_YEAR_20 = Parameter(
    WISHONIA_TRAJECTORY_GDP_YEAR_20 / CURRENT_TRAJECTORY_GDP_YEAR_20,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Wishonia Trajectory GDP at year 20 as a multiple of current trajectory GDP at year 20.",
    display_name="Wishonia Trajectory vs Current Trajectory GDP Multiplier (Year 20)",
    unit="x",
    formula="WISHONIA_TRAJECTORY_GDP_YEAR_20 ÷ CURRENT_TRAJECTORY_GDP_YEAR_20",
    keywords=["GDP", "wishonia", "baseline", "multiplier", "year 20"],
    inputs=["WISHONIA_TRAJECTORY_GDP_YEAR_20", "CURRENT_TRAJECTORY_GDP_YEAR_20"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_GDP_YEAR_20"] / ctx["CURRENT_TRAJECTORY_GDP_YEAR_20"],
    latex_symbol=r"k_{wish:base,20}",
)

WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20 = Parameter(
    float(WISHONIA_TRAJECTORY_GDP_YEAR_20) / float(GLOBAL_POPULATION_2045_PROJECTED),
    manual_ref="knowledge/appendix/political-dysfunction-tax.qmd",
    source_type="calculated",
    description="Average income (GDP per capita) at year 20 under the Wishonia Trajectory.",
    display_name="Wishonia Trajectory Average Income at Year 20",
    unit="USD",
    formula="WISHONIA_TRAJECTORY_GDP_YEAR_20 / GLOBAL_POPULATION_2045_PROJECTED",
    keywords=["income", "per capita", "wishonia", "year 20", "average"],
    inputs=["WISHONIA_TRAJECTORY_GDP_YEAR_20", "GLOBAL_POPULATION_2045_PROJECTED"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_GDP_YEAR_20"] / ctx["GLOBAL_POPULATION_2045_PROJECTED"],
    latex_symbol=r"\bar{y}_{wish,20}",
)

WISHONIA_TRAJECTORY_VS_TREATY_TRAJECTORY_GDP_MULTIPLIER_YEAR_20 = Parameter(
    WISHONIA_TRAJECTORY_GDP_YEAR_20 / TREATY_TRAJECTORY_GDP_YEAR_20,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Year-20 GDP multiplier from adding non-health dysfunction-capital reallocation "
                "on top of the Treaty Trajectory channels.",
    display_name="Wishonia Trajectory vs Treaty Trajectory GDP Multiplier (Year 20)",
    unit="x",
    formula="WISHONIA_TRAJECTORY_GDP_YEAR_20 ÷ TREATY_TRAJECTORY_GDP_YEAR_20",
    keywords=["wishonia", "full", "core", "GDP", "multiplier", "year 20"],
    inputs=["WISHONIA_TRAJECTORY_GDP_YEAR_20", "TREATY_TRAJECTORY_GDP_YEAR_20"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_GDP_YEAR_20"] / ctx["TREATY_TRAJECTORY_GDP_YEAR_20"],
    latex_symbol=r"k_{wish,full:core,20}",
)

# ---
# YEAR 15 GDP AND HALE TRAJECTORY PARAMETERS
# ---
# Mirrors the year 20 GDP trajectory model but over a 15-year horizon
# (3-year ramp at 50% intensity + 12-year full implementation).
# Also adds HALE (healthy life expectancy) projections as a terminal general-welfare metric
# for the Earth Optimization Prize.

GLOBAL_POPULATION_2040_PROJECTED = Parameter(
    8_900_000_000,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_ref=ReferenceID.GLOBAL_POPULATION_8_BILLION,
    source_type="external",
    distribution="fixed",
    description="UN World Population Prospects 2022 median projection for 2040. "
                "Interpolated midpoint between ~8.1B (2025) and 9.2B (2045).",
    display_name="Global Population 2040 (Projected)",
    unit="of people",
    keywords=["population", "2040", "projection", "UN", "global"],
    latex_symbol=r"Pop_{2040}",
)

TREATY_DISEASE_CURE_FRACTION_15YR = Parameter(
    min(
        1.0,
        (
            3 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (0.01 / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
            + 4 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (min(0.02, _S_ratchet) / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
            + 5 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (min(0.05, _S_ratchet) / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
            + 3 * min(float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (_S_ratchet / 0.01), float(DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL))
        )
        / float(STATUS_QUO_QUEUE_CLEARANCE_YEARS),
    ),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Fraction of currently untreatable diseases with a first effective treatment by "
                "year 15 under the treaty: queue progress integrated over the ratchet schedule, "
                "with trial capacity scaling linearly with funding up to the physical participant "
                "ceiling. Binds the single ratchet knob: at TREATY_RATCHET_TERMINAL_SHARE = 0.01 "
                "(ratchet off) this degrades to 15/36 of the queue (~42%); on the central schedule "
                "the queue clears around year 12, so the central is 100%. The ~36-year "
                "queue-clearance figure quoted elsewhere is the flat-1% case by construction.",
    display_name="Treaty Disease Cure Fraction (15yr, Ratchet Schedule)",
    unit="rate",
    formula="min(1.0, (3×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(0.01/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) + 4×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(min(0.02, TREATY_RATCHET_TERMINAL_SHARE)/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) + 5×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(min(0.05, TREATY_RATCHET_TERMINAL_SHARE)/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) + 3×min(DFDA_TRIAL_CAPACITY_MULTIPLIER×(TREATY_RATCHET_TERMINAL_SHARE/0.01), DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL)) ÷ STATUS_QUO_QUEUE_CLEARANCE_YEARS)",
    inputs=["DFDA_TRIAL_CAPACITY_MULTIPLIER", "DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL",
            "TREATY_RATCHET_TERMINAL_SHARE", "STATUS_QUO_QUEUE_CLEARANCE_YEARS"],
    compute=lambda ctx: min(
        1.0,
        (
            3 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (0.01 / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
            + 4 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (min(0.02, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
            + 5 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (min(0.05, ctx["TREATY_RATCHET_TERMINAL_SHARE"]) / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
            + 3 * min(ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * (ctx["TREATY_RATCHET_TERMINAL_SHARE"] / 0.01), ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"])
        )
        / ctx["STATUS_QUO_QUEUE_CLEARANCE_YEARS"],
    ),
    keywords=["treaty", "disease", "cure fraction", "15 year", "queue", "ratchet"],
    latex_symbol=r"f_{cure,15,treaty}",
)

TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_15 = Parameter(
    TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15 * ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT / 0.30) * (RD_SPILLOVER_MULTIPLIER / 2.0)),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Annual GDP growth bonus by year 15 from redirecting military spending to medical research under the treaty take-hold path, "
                "including R&D spillovers.",
    display_name="Treaty Redirect GDP Growth Bonus (Year 15)",
    unit="rate",
    formula="TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15 × ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT ÷ 0.30) × (RD_SPILLOVER_MULTIPLIER ÷ 2.0))",
    inputs=["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15", "MILITARY_REDIRECT_GDP_BOOST_AT_30PCT", "RD_SPILLOVER_MULTIPLIER"],
    compute=lambda ctx: ctx["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15"] * ((ctx["MILITARY_REDIRECT_GDP_BOOST_AT_30PCT"] / 0.30) * (ctx["RD_SPILLOVER_MULTIPLIER"] / 2.0)),
    keywords=["treaty", "GDP", "growth", "redirect", "R&D", "spillover", "15 year"],
    latex_symbol=r"g_{redirect,treaty,15}",
)

TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_15 = Parameter(
    (PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / GLOBAL_GDP_2025)
    * (TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15 / TREATY_REDUCTION_PCT)
    * PEACE_DIVIDEND_CONFLICT_ELASTICITY,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Annual GDP growth bonus by year 15 from explicit avoided war-cost drag under the treaty take-hold path.",
    display_name="Treaty Peace Recovery GDP Growth Bonus (Year 15)",
    unit="rate",
    formula="(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT ÷ GLOBAL_GDP_2025) × (TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15 ÷ TREATY_REDUCTION_PCT) × PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    inputs=[
        "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
        "GLOBAL_GDP_2025",
        "TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15",
        "TREATY_REDUCTION_PCT",
        "PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    ],
    compute=lambda ctx: (
        (ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"] / ctx["GLOBAL_GDP_2025"])
        * (ctx["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15"] / ctx["TREATY_REDUCTION_PCT"])
        * ctx["PEACE_DIVIDEND_CONFLICT_ELASTICITY"]
    ),
    keywords=["treaty", "GDP", "growth", "peace dividend", "war costs", "15 year"],
    latex_symbol=r"g_{peace,treaty,15}",
)

TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_15 = Parameter(
    (GLOBAL_CYBERCRIME_COST_ANNUAL_2025 / GLOBAL_GDP_2025)
    * TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15
    * PEACE_DIVIDEND_CONFLICT_ELASTICITY,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Annual GDP growth bonus by year 15 from reducing cybercrime drag as the treaty weakens the destructive economy feedback loop.",
    display_name="Treaty Cybercrime Recovery GDP Growth Bonus (Year 15)",
    unit="rate",
    formula="(GLOBAL_CYBERCRIME_COST_ANNUAL_2025 ÷ GLOBAL_GDP_2025) × TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15 × PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    inputs=[
        "GLOBAL_CYBERCRIME_COST_ANNUAL_2025",
        "GLOBAL_GDP_2025",
        "TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15",
        "PEACE_DIVIDEND_CONFLICT_ELASTICITY",
    ],
    compute=lambda ctx: (
        (ctx["GLOBAL_CYBERCRIME_COST_ANNUAL_2025"] / ctx["GLOBAL_GDP_2025"])
        * ctx["TREATY_EFFECTIVE_REALLOCATION_SHARE_YEAR_15"]
        * ctx["PEACE_DIVIDEND_CONFLICT_ELASTICITY"]
    ),
    keywords=["treaty", "GDP", "growth", "cybercrime", "destructive economy", "15 year"],
    latex_symbol=r"g_{cyber,treaty,15}",
)

TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_15 = Parameter(
    ((1 + TREATY_DISEASE_CURE_FRACTION_15YR * DISEASE_BURDEN_GDP_DRAG_PCT) ** (1 / 15)) - 1,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Annualized GDP growth bonus by year 15 from lower disease burden under the treaty path. "
                "Deliberately EXCLUDES the monetized value of life-years from eliminating the existing-drug "
                "efficacy lag, matching the year-20 model and the chapter's stated accounting rule: that "
                "value belongs in health and welfare accounting, not in the output ledger. (The previous "
                "version injected the $259T cumulative mortality-valuation stock into an annual growth "
                "rate, producing a year-15 income ABOVE the year-20 income on the same trajectory.)",
    display_name="Treaty Health Recovery GDP Growth Bonus (Year 15)",
    unit="rate",
    formula="((1 + TREATY_DISEASE_CURE_FRACTION_15YR × DISEASE_BURDEN_GDP_DRAG_PCT)^(1/15)) - 1",
    inputs=[
        "TREATY_DISEASE_CURE_FRACTION_15YR",
        "DISEASE_BURDEN_GDP_DRAG_PCT",
    ],
    compute=lambda ctx: (
        (
            1
            + ctx["TREATY_DISEASE_CURE_FRACTION_15YR"] * ctx["DISEASE_BURDEN_GDP_DRAG_PCT"]
        ) ** (1 / 15)
    ) - 1,
    keywords=["treaty", "GDP", "growth", "health", "disease burden", "15 year"],
    latex_symbol=r"g_{health,treaty,15}",
)

WISHONIA_DISEASE_CURE_FRACTION_15YR = Parameter(
    min(
        1.0,
        NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR
        * min(
            DFDA_TRIAL_CAPACITY_MULTIPLIER * (WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE / 0.01),
            DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL,
        )
        * 15
        / DISEASES_WITHOUT_EFFECTIVE_TREATMENT,
    ),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Wishonia disease-cure fraction over 15 years under full implementation. "
                "Uses full trial-capacity scaling and applies an upper bound of 100% of untreated disease classes.",
    display_name="Wishonia Disease Cure Fraction (15yr, Full Implementation)",
    unit="rate",
    formula="min(1.0, NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR * min(TRIAL_CAPACITY_MULTIPLIER * (WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE / 0.01), MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL) * 15 / DISEASES_WITHOUT_EFFECTIVE_TREATMENT)",
    inputs=[
        "NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR",
        "DFDA_TRIAL_CAPACITY_MULTIPLIER",
        "WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE",
        "DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL",
        "DISEASES_WITHOUT_EFFECTIVE_TREATMENT",
    ],
    compute=lambda ctx: min(
        1.0,
        ctx["NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR"]
        * min(
            ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"]
            * (ctx["WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE"] / 0.01),
            ctx["DFDA_MAX_TRIAL_CAPACITY_MULTIPLIER_PHYSICAL"],
        )
        * 15
        / ctx["DISEASES_WITHOUT_EFFECTIVE_TREATMENT"],
    ),
    keywords=["wishonia", "disease", "cure fraction", "15 year", "full implementation"],
    latex_symbol=r"f_{cure,15,wish}",
    distribution="fixed",  # Saturates at 1.0 ceiling under full-implementation parameters
)

CURRENT_TRAJECTORY_GDP_YEAR_15 = Parameter(
    GLOBAL_GDP_2025 * ((1 + GDP_BASELINE_GROWTH_RATE) ** 15),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Global GDP at year 15 under status-quo current trajectory growth.",
    display_name="Current Trajectory GDP at Year 15",
    unit="USD",
    formula="GLOBAL_GDP_2025 * (1 + GDP_BASELINE_GROWTH_RATE)^15",
    keywords=["GDP", "baseline", "year 15"],
    inputs=["GLOBAL_GDP_2025", "GDP_BASELINE_GROWTH_RATE"],
    compute=lambda ctx: ctx["GLOBAL_GDP_2025"] * ((1 + ctx["GDP_BASELINE_GROWTH_RATE"]) ** 15),
    latex_symbol=r"GDP_{base,15}",
)

TREATY_TRAJECTORY_GDP_YEAR_15 = Parameter(
    GLOBAL_GDP_2025
    * (
        1
        + GDP_BASELINE_GROWTH_RATE
        + TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_15
        + TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_15
        + TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_15
        + TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_15
    ) ** 15,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Projected global GDP at year 15 under the optimistic treaty take-hold path. "
                "Compounds baseline growth plus explicit military redirect spillovers, peace dividend recovery, "
                "cybercrime drag recovery, and health recovery from disease cures and faster deployment.",
    display_name="Treaty Trajectory GDP at Year 15",
    unit="USD",
    formula="GLOBAL_GDP_2025 × (1 + GDP_BASELINE_GROWTH_RATE + TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_15 + TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_15 + TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_15 + TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_15)^15",
    keywords=["GDP", "treaty", "projection", "15 years", "optimistic"],
    inputs=[
        "GLOBAL_GDP_2025",
        "GDP_BASELINE_GROWTH_RATE",
        "TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_15",
        "TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_15",
        "TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_15",
        "TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_15",
    ],
    compute=lambda ctx: (
        ctx["GLOBAL_GDP_2025"]
        * (
            1
            + ctx["GDP_BASELINE_GROWTH_RATE"]
            + ctx["TREATY_REDIRECT_GDP_GROWTH_BONUS_YEAR_15"]
            + ctx["TREATY_PEACE_RECOVERY_GDP_GROWTH_BONUS_YEAR_15"]
            + ctx["TREATY_CYBERCRIME_RECOVERY_GDP_GROWTH_BONUS_YEAR_15"]
            + ctx["TREATY_HEALTH_RECOVERY_GDP_GROWTH_BONUS_YEAR_15"]
        ) ** 15
    ),
    latex_symbol=r"GDP_{treaty,15}",
)

WISHONIA_TRAJECTORY_GDP_YEAR_15 = Parameter(
    GLOBAL_GDP_2025
    * (
        (
            1
            + GDP_BASELINE_GROWTH_RATE
            + (0.5 * WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE)
            * ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT / 0.30) * (RD_SPILLOVER_MULTIPLIER / 2.0))
            + ((1 + WISHONIA_DISEASE_CURE_FRACTION_15YR * DISEASE_BURDEN_GDP_DRAG_PCT) ** (1 / 15) - 1)
            + (
                (
                    1
                    + (
                        0.5
                        * (
                        (
                            POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST
                        )
                        / GLOBAL_GDP_2025
                        )
                    )
                    * (ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT / ECONOMIC_MULTIPLIER_MILITARY_SPENDING - 1)
                ) ** (1 / 15)
                - 1
            )
        ) ** 3
    )
    * (
        (
            1
            + GDP_BASELINE_GROWTH_RATE
            + WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE
            * ((MILITARY_REDIRECT_GDP_BOOST_AT_30PCT / 0.30) * (RD_SPILLOVER_MULTIPLIER / 2.0))
            + ((1 + WISHONIA_DISEASE_CURE_FRACTION_15YR * DISEASE_BURDEN_GDP_DRAG_PCT) ** (1 / 15) - 1)
            + (
                (
                    1
                    + (
                        (
                            POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST
                            + POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST
                        )
                        / GLOBAL_GDP_2025
                    )
                    * (ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT / ECONOMIC_MULTIPLIER_MILITARY_SPENDING - 1)
                ) ** (1 / 15)
                - 1
            )
        ) ** 12
    ),
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_type="calculated",
    description="Projected global GDP at year 15 under the Wishonia Trajectory. "
                "Applies all Wishonia policy channels including military reallocation, disease-burden recovery, "
                "and Political Dysfunction Tax elimination. 3-year ramp at 50% intensity + 12 years full.",
    display_name="Wishonia Trajectory GDP at Year 15",
    unit="USD",
    formula="GLOBAL_GDP_2025 * (1 + g_ramp)^3 * (1 + g_full)^12, where years 1-3 use 50% of military and non-health reallocation intensity, and years 4-15 use 100%; both include disease-burden recovery",
    latex=r"GDP_{wish,15}=GDP_0(1+g_{ramp})^{3}(1+g_{full})^{12}",
    keywords=["GDP", "wishonia", "projection", "year 15"],
    inputs=[
        "GLOBAL_GDP_2025",
        "GDP_BASELINE_GROWTH_RATE",
        "WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE",
        "MILITARY_REDIRECT_GDP_BOOST_AT_30PCT",
        "RD_SPILLOVER_MULTIPLIER",
        "WISHONIA_DISEASE_CURE_FRACTION_15YR",
        "DISEASE_BURDEN_GDP_DRAG_PCT",
        "POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST",
        "POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST",
        "POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST",
        "ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT",
        "ECONOMIC_MULTIPLIER_MILITARY_SPENDING",
    ],
    compute=lambda ctx: (
        ctx["GLOBAL_GDP_2025"]
        * (
            (
                1
                + ctx["GDP_BASELINE_GROWTH_RATE"]
                + (0.5 * ctx["WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE"])
                * ((ctx["MILITARY_REDIRECT_GDP_BOOST_AT_30PCT"] / 0.30) * (ctx["RD_SPILLOVER_MULTIPLIER"] / 2.0))
                + ((1 + ctx["WISHONIA_DISEASE_CURE_FRACTION_15YR"] * ctx["DISEASE_BURDEN_GDP_DRAG_PCT"]) ** (1 / 15) - 1)
                + (
                    (
                        1
                        + (
                            0.5
                            * (
                            (
                                ctx["POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST"]
                            )
                            / ctx["GLOBAL_GDP_2025"]
                            )
                        )
                        * (ctx["ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT"] / ctx["ECONOMIC_MULTIPLIER_MILITARY_SPENDING"] - 1)
                    ) ** (1 / 15)
                    - 1
                )
            ) ** 3
        )
        * (
            (
                1
                + ctx["GDP_BASELINE_GROWTH_RATE"]
                + ctx["WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE"]
                * ((ctx["MILITARY_REDIRECT_GDP_BOOST_AT_30PCT"] / 0.30) * (ctx["RD_SPILLOVER_MULTIPLIER"] / 2.0))
                + ((1 + ctx["WISHONIA_DISEASE_CURE_FRACTION_15YR"] * ctx["DISEASE_BURDEN_GDP_DRAG_PCT"]) ** (1 / 15) - 1)
                + (
                    (
                        1
                        + (
                            (
                                ctx["POLITICAL_DYSFUNCTION_GLOBAL_SCIENCE_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST"]
                                + ctx["POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST"]
                            )
                            / ctx["GLOBAL_GDP_2025"]
                        )
                        * (ctx["ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT"] / ctx["ECONOMIC_MULTIPLIER_MILITARY_SPENDING"] - 1)
                    ) ** (1 / 15)
                    - 1
                )
            ) ** 12
        )
    ),
    latex_symbol=r"GDP_{wish,15}",
)

CURRENT_TRAJECTORY_AVG_INCOME_YEAR_15 = Parameter(
    CURRENT_TRAJECTORY_GDP_YEAR_15 / GLOBAL_POPULATION_2040_PROJECTED,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Average income (GDP per capita) at year 15 under current trajectory.",
    display_name="Current Trajectory Average Income at Year 15",
    unit="USD",
    formula="CURRENT_TRAJECTORY_GDP_YEAR_15 / GLOBAL_POPULATION_2040_PROJECTED",
    keywords=["income", "per capita", "baseline", "year 15", "average"],
    inputs=["CURRENT_TRAJECTORY_GDP_YEAR_15", "GLOBAL_POPULATION_2040_PROJECTED"],
    compute=lambda ctx: ctx["CURRENT_TRAJECTORY_GDP_YEAR_15"] / ctx["GLOBAL_POPULATION_2040_PROJECTED"],
    latex_symbol=r"\bar{y}_{base,15}",
    distribution="fixed",  # All upstream inputs are distribution="fixed"
)

TREATY_TRAJECTORY_AVG_INCOME_YEAR_15 = Parameter(
    float(TREATY_TRAJECTORY_GDP_YEAR_15) / float(GLOBAL_POPULATION_2040_PROJECTED),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Average income (GDP per capita) at year 15 under the Treaty Trajectory.",
    display_name="Treaty Trajectory Average Income at Year 15",
    unit="USD",
    formula="TREATY_TRAJECTORY_GDP_YEAR_15 / GLOBAL_POPULATION_2040_PROJECTED",
    keywords=["income", "per capita", "treaty", "year 15", "average"],
    inputs=["TREATY_TRAJECTORY_GDP_YEAR_15", "GLOBAL_POPULATION_2040_PROJECTED"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_GDP_YEAR_15"] / ctx["GLOBAL_POPULATION_2040_PROJECTED"],
    latex_symbol=r"\bar{y}_{treaty,15}",
)

WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_15 = Parameter(
    float(WISHONIA_TRAJECTORY_GDP_YEAR_15) / float(GLOBAL_POPULATION_2040_PROJECTED),
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_type="calculated",
    description="Average income (GDP per capita) at year 15 under the Wishonia Trajectory.",
    display_name="Wishonia Trajectory Average Income at Year 15",
    unit="USD",
    formula="WISHONIA_TRAJECTORY_GDP_YEAR_15 / GLOBAL_POPULATION_2040_PROJECTED",
    keywords=["income", "per capita", "wishonia", "year 15", "average"],
    inputs=["WISHONIA_TRAJECTORY_GDP_YEAR_15", "GLOBAL_POPULATION_2040_PROJECTED"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_GDP_YEAR_15"] / ctx["GLOBAL_POPULATION_2040_PROJECTED"],
    latex_symbol=r"\bar{y}_{wish,15}",
)

TREATY_TRAJECTORY_GDP_VS_CURRENT_TRAJECTORY_MULTIPLIER_YEAR_15 = Parameter(
    TREATY_TRAJECTORY_GDP_YEAR_15 / CURRENT_TRAJECTORY_GDP_YEAR_15,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Treaty Trajectory GDP at year 15 as a multiple of current trajectory GDP at year 15.",
    display_name="Treaty Trajectory vs Current Trajectory GDP Multiplier (Year 15)",
    unit="x",
    formula="TREATY_TRAJECTORY_GDP_YEAR_15 / CURRENT_TRAJECTORY_GDP_YEAR_15",
    keywords=["GDP", "treaty", "baseline", "multiplier", "year 15"],
    inputs=["TREATY_TRAJECTORY_GDP_YEAR_15", "CURRENT_TRAJECTORY_GDP_YEAR_15"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_GDP_YEAR_15"] / ctx["CURRENT_TRAJECTORY_GDP_YEAR_15"],
    latex_symbol=r"k_{treaty:base,15}",
)

WISHONIA_TRAJECTORY_GDP_VS_CURRENT_TRAJECTORY_MULTIPLIER_YEAR_15 = Parameter(
    WISHONIA_TRAJECTORY_GDP_YEAR_15 / CURRENT_TRAJECTORY_GDP_YEAR_15,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Wishonia Trajectory GDP at year 15 as a multiple of current trajectory GDP at year 15.",
    display_name="Wishonia Trajectory vs Current Trajectory GDP Multiplier (Year 15)",
    unit="x",
    formula="WISHONIA_TRAJECTORY_GDP_YEAR_15 / CURRENT_TRAJECTORY_GDP_YEAR_15",
    keywords=["GDP", "wishonia", "baseline", "multiplier", "year 15"],
    inputs=["WISHONIA_TRAJECTORY_GDP_YEAR_15", "CURRENT_TRAJECTORY_GDP_YEAR_15"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_GDP_YEAR_15"] / ctx["CURRENT_TRAJECTORY_GDP_YEAR_15"],
    latex_symbol=r"k_{wish:base,15}",
)

# ---
# HALE (HEALTHY LIFE EXPECTANCY) PROJECTIONS - YEAR 15
# ---
# Terminal metric for Earth Optimization Prize: median healthy life years.
# Disease burden reduces HALE by (life_expectancy - HALE) years.
# As diseases are cured, this gap closes proportionally to the cure fraction.

GLOBAL_HALE_CURRENT = Parameter(
    63.3,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    distribution="normal",
    std_error=1.5,
    description="Global healthy life expectancy at birth (HALE) from WHO Global Health Observatory, "
                "2019 data (most recent available). HALE measures years lived in full health, adjusting "
                "for years lived with disability or disease.",
    display_name="Global Healthy Life Expectancy (HALE)",
    unit="years",
    confidence="high",
    last_updated="2019",
    peer_reviewed=True,
    keywords=["HALE", "healthy life expectancy", "disability", "WHO", "global health"],
    latex_symbol=r"HALE_{0}",
)

GLOBAL_HALE_GAP = Parameter(
    float(GLOBAL_LIFE_EXPECTANCY_2024) - 63.3,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Gap between life expectancy and healthy life expectancy. Represents years lived "
                "with disability or disease that could be recovered by curing diseases.",
    display_name="Life Expectancy to HALE Gap",
    unit="years",
    formula="GLOBAL_LIFE_EXPECTANCY_2024 - GLOBAL_HALE_CURRENT",
    inputs=["GLOBAL_LIFE_EXPECTANCY_2024", "GLOBAL_HALE_CURRENT"],
    compute=lambda ctx: ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["GLOBAL_HALE_CURRENT"],
    keywords=["HALE", "gap", "disability", "disease burden", "healthy years lost"],
    latex_symbol=r"\Delta_{HALE}",
)

HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15 = Parameter(
    0.30,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="definition",
    distribution="fixed",
    description="Share of longer-run life-extension gains that have plausibly materialized into healthy years by year 15. "
                "Calibrated to the repo's conservative disease-eradication helper, which implies that only a minority "
                "of eventual longevity gains are realized within the first 15 years even under rapid research acceleration.",
    display_name="HALE Longevity Realization Share (Year 15)",
    unit="rate",
    formula="0.30",
    keywords=["HALE", "longevity", "realization", "15 year", "health span"],
    latex_symbol=r"\rho_{HALE,15}",
)

BEST_PRACTICE_LIFE_EXPECTANCY_GAIN = Parameter(
    max(float(SWITZERLAND_LIFE_EXPECTANCY), float(SINGAPORE_LIFE_EXPECTANCY)) - float(GLOBAL_LIFE_EXPECTANCY_2024),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Gap between current global life expectancy and the best life expectancy achieved by a major country today. "
                "Used as a non-arbitrary governance/public-health uplift benchmark rather than capping Wishonia at today's global average.",
    display_name="Best-Practice Life Expectancy Gain",
    unit="years",
    formula="max(SWITZERLAND_LIFE_EXPECTANCY, SINGAPORE_LIFE_EXPECTANCY) - GLOBAL_LIFE_EXPECTANCY_2024",
    inputs=["SWITZERLAND_LIFE_EXPECTANCY", "SINGAPORE_LIFE_EXPECTANCY", "GLOBAL_LIFE_EXPECTANCY_2024"],
    compute=lambda ctx: max(ctx["SWITZERLAND_LIFE_EXPECTANCY"], ctx["SINGAPORE_LIFE_EXPECTANCY"]) - ctx["GLOBAL_LIFE_EXPECTANCY_2024"],
    keywords=["life expectancy", "best practice", "governance", "benchmark", "health"],
    latex_symbol=r"\Delta LE_{best}",
)

TREATY_LONGEVITY_HALE_GAIN_YEAR_15 = Parameter(
    LIFE_EXTENSION_YEARS * HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15 * TREATY_DISEASE_CURE_FRACTION_15YR,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Additional healthy years at year 15 from partial realization of longer-run treaty longevity gains. "
                "This removes the implicit cap at today's life expectancy while keeping year-15 realization conservative.",
    display_name="Treaty Longevity HALE Gain at Year 15",
    unit="years",
    formula="LIFE_EXTENSION_YEARS × HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15 × TREATY_DISEASE_CURE_FRACTION_15YR",
    inputs=["LIFE_EXTENSION_YEARS", "HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15", "TREATY_DISEASE_CURE_FRACTION_15YR"],
    compute=lambda ctx: ctx["LIFE_EXTENSION_YEARS"] * ctx["HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15"] * ctx["TREATY_DISEASE_CURE_FRACTION_15YR"],
    keywords=["HALE", "treaty", "longevity", "healthy years", "year 15"],
    latex_symbol=r"\Delta HALE_{treaty,longevity,15}",
)

WISHONIA_EXTRA_HALE_GAIN_YEAR_15 = Parameter(
    WISHONIA_DISEASE_CURE_FRACTION_15YR * (BEST_PRACTICE_LIFE_EXPECTANCY_GAIN + LIFE_EXTENSION_YEARS * HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Additional healthy years at year 15 from optimal-governance public-health improvements plus partial realization "
                "of longer-run longevity gains. This removes the implicit cap at today's life expectancy and lets Wishonia exceed it for non-arbitrary reasons.",
    display_name="Wishonia Extra HALE Gain at Year 15",
    unit="years",
    formula="WISHONIA_DISEASE_CURE_FRACTION_15YR × (BEST_PRACTICE_LIFE_EXPECTANCY_GAIN + LIFE_EXTENSION_YEARS × HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15)",
    inputs=[
        "WISHONIA_DISEASE_CURE_FRACTION_15YR",
        "BEST_PRACTICE_LIFE_EXPECTANCY_GAIN",
        "LIFE_EXTENSION_YEARS",
        "HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15",
    ],
    compute=lambda ctx: ctx["WISHONIA_DISEASE_CURE_FRACTION_15YR"] * (
        ctx["BEST_PRACTICE_LIFE_EXPECTANCY_GAIN"]
        + ctx["LIFE_EXTENSION_YEARS"] * ctx["HALE_LONGEVITY_REALIZATION_SHARE_YEAR_15"]
    ),
    keywords=["HALE", "wishonia", "governance", "longevity", "healthy years", "year 15"],
    latex_symbol=r"\Delta HALE_{wish,extra,15}",
)

TREATY_HALE_GAIN_YEAR_15 = Parameter(
    TREATY_DISEASE_CURE_FRACTION_15YR * (float(GLOBAL_LIFE_EXPECTANCY_2024) - 63.3) + float(TREATY_LONGEVITY_HALE_GAIN_YEAR_15),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="HALE improvement at year 15 under Treaty Trajectory. It includes both closing the current "
                "HALE gap from disease/disability and a conservative partial realization of longer-run longevity gains.",
    display_name="Treaty HALE Gain at Year 15",
    unit="years",
    formula="TREATY_DISEASE_CURE_FRACTION_15YR × GLOBAL_HALE_GAP + TREATY_LONGEVITY_HALE_GAIN_YEAR_15",
    inputs=["TREATY_DISEASE_CURE_FRACTION_15YR", "GLOBAL_HALE_CURRENT", "GLOBAL_LIFE_EXPECTANCY_2024", "TREATY_LONGEVITY_HALE_GAIN_YEAR_15"],
    compute=lambda ctx: (
        ctx["TREATY_DISEASE_CURE_FRACTION_15YR"] * (ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["GLOBAL_HALE_CURRENT"])
        + ctx["TREATY_LONGEVITY_HALE_GAIN_YEAR_15"]
    ),
    keywords=["HALE", "gain", "treaty", "year 15", "healthy years"],
    latex_symbol=r"\Delta HALE_{treaty,15}",
)

WISHONIA_HALE_GAIN_YEAR_15 = Parameter(
    WISHONIA_DISEASE_CURE_FRACTION_15YR * (float(GLOBAL_LIFE_EXPECTANCY_2024) - 63.3) + float(WISHONIA_EXTRA_HALE_GAIN_YEAR_15),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="HALE improvement at year 15 under Wishonia Trajectory. It includes closing the current "
                "HALE gap, reaching today's best-practice life expectancy through optimal governance/public health, "
                "and a conservative partial realization of longer-run longevity gains.",
    display_name="Wishonia HALE Gain at Year 15",
    unit="years",
    formula="WISHONIA_DISEASE_CURE_FRACTION_15YR × GLOBAL_HALE_GAP + WISHONIA_EXTRA_HALE_GAIN_YEAR_15",
    inputs=["WISHONIA_DISEASE_CURE_FRACTION_15YR", "GLOBAL_HALE_CURRENT", "GLOBAL_LIFE_EXPECTANCY_2024", "WISHONIA_EXTRA_HALE_GAIN_YEAR_15"],
    compute=lambda ctx: (
        ctx["WISHONIA_DISEASE_CURE_FRACTION_15YR"] * (ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["GLOBAL_HALE_CURRENT"])
        + ctx["WISHONIA_EXTRA_HALE_GAIN_YEAR_15"]
    ),
    keywords=["HALE", "gain", "wishonia", "year 15", "healthy years"],
    latex_symbol=r"\Delta HALE_{wish,15}",
)

TREATY_HALE_VALUE_PER_CAPITA = Parameter(
    float(TREATY_HALE_GAIN_YEAR_15) * float(STANDARD_ECONOMIC_QALY_VALUE_USD),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Economic value of Treaty Trajectory HALE gains at year 15 using the standard QALY value.",
    display_name="Treaty HALE Value Per Capita",
    unit="USD/person",
    formula="TREATY_HALE_GAIN_YEAR_15 × STANDARD_ECONOMIC_QALY_VALUE_USD",
    inputs=["TREATY_HALE_GAIN_YEAR_15", "STANDARD_ECONOMIC_QALY_VALUE_USD"],
    compute=lambda ctx: ctx["TREATY_HALE_GAIN_YEAR_15"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    keywords=["HALE", "QALY", "value", "treaty", "per capita"],
    latex_symbol=r"Value_{HALE,treaty}",
)

WISHONIA_HALE_VALUE_PER_CAPITA = Parameter(
    float(WISHONIA_HALE_GAIN_YEAR_15) * float(STANDARD_ECONOMIC_QALY_VALUE_USD),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Economic value of Wishonia Trajectory HALE gains at year 15 using the standard QALY value.",
    display_name="Wishonia HALE Value Per Capita",
    unit="USD/person",
    formula="WISHONIA_HALE_GAIN_YEAR_15 × STANDARD_ECONOMIC_QALY_VALUE_USD",
    inputs=["WISHONIA_HALE_GAIN_YEAR_15", "STANDARD_ECONOMIC_QALY_VALUE_USD"],
    compute=lambda ctx: ctx["WISHONIA_HALE_GAIN_YEAR_15"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    keywords=["HALE", "QALY", "value", "wishonia", "per capita"],
    latex_symbol=r"Value_{HALE,wish}",
)

TREATY_PROJECTED_HALE_YEAR_15 = Parameter(
    float(GLOBAL_HALE_CURRENT) + float(TREATY_HALE_GAIN_YEAR_15),
    manual_ref="knowledge/appendix/earth-optimization-prize-protocol.qmd",
    source_type="calculated",
    description="Projected global HALE at year 15 under Treaty Trajectory. "
                "Current HALE plus the treaty-driven improvement from closing the disease gap.",
    display_name="Treaty Projected HALE at Year 15",
    unit="years",
    formula="GLOBAL_HALE_CURRENT + TREATY_HALE_GAIN_YEAR_15",
    inputs=["GLOBAL_HALE_CURRENT", "TREATY_HALE_GAIN_YEAR_15"],
    compute=lambda ctx: ctx["GLOBAL_HALE_CURRENT"] + ctx["TREATY_HALE_GAIN_YEAR_15"],
    keywords=["HALE", "projected", "treaty", "year 15", "healthy life expectancy"],
    latex_symbol=r"HALE_{treaty,15}",
)

WISHONIA_PROJECTED_HALE_YEAR_15 = Parameter(
    float(GLOBAL_HALE_CURRENT) + float(WISHONIA_HALE_GAIN_YEAR_15),
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_type="calculated",
    description="Projected global HALE at year 15 under Wishonia Trajectory. "
                "Full implementation closes the entire disease gap, pushing HALE toward life expectancy.",
    display_name="Wishonia Projected HALE at Year 15",
    unit="years",
    formula="GLOBAL_HALE_CURRENT + WISHONIA_HALE_GAIN_YEAR_15",
    inputs=["GLOBAL_HALE_CURRENT", "WISHONIA_HALE_GAIN_YEAR_15"],
    compute=lambda ctx: ctx["GLOBAL_HALE_CURRENT"] + ctx["WISHONIA_HALE_GAIN_YEAR_15"],
    keywords=["HALE", "projected", "wishonia", "year 15", "healthy life expectancy"],
    latex_symbol=r"HALE_{wish,15}",
)

# (GLOBAL_AVG_INCOME_2025 moved earlier in file for war counterfactual params)

# ---
# LIFETIME INCOME COMPARISON (Treaty Trajectory vs Current Trajectory)
# ---
# Calculates cumulative per-capita income over an average remaining lifespan.
# Treaty path uses per-capita CAGR for years 1-20, then GDP_BASELINE_GROWTH_RATE
# from the year-20 level. Conservative: assumes no further treaty acceleration beyond year 20.

GLOBAL_MEDIAN_AGE_2024 = Parameter(
    30.5,
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_ref=ReferenceID.GLOBAL_MEDIAN_AGE_UN_WPP_2024,
    source_type="external",
    description="Global median age in 2024 from UN World Population Prospects 2024 revision.",
    display_name="Global Median Age (2024)",
    unit="years",
    confidence="high",
    distribution="fixed",
    keywords=["median age", "demographics", "population", "global", "2024"],
    latex_symbol=r"Age_{median}",
)

GLOBAL_AVG_REMAINING_YEARS = Parameter(
    float(GLOBAL_LIFE_EXPECTANCY_2024) - float(GLOBAL_MEDIAN_AGE_2024),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Average remaining lifespan for the median-age person. Conservative: uses "
                "life expectancy at birth minus median age, which underestimates remaining years "
                "because survivors to age 30 have higher conditional life expectancy.",
    display_name="Average Remaining Years (Median Person)",
    unit="years",
    formula="GLOBAL_LIFE_EXPECTANCY_2024 - GLOBAL_MEDIAN_AGE_2024",
    inputs=["GLOBAL_LIFE_EXPECTANCY_2024", "GLOBAL_MEDIAN_AGE_2024"],
    compute=lambda ctx: ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["GLOBAL_MEDIAN_AGE_2024"],
    latex_symbol=r"T_{remaining}",
)


_remaining_years_0 = int(float(GLOBAL_AVG_REMAINING_YEARS))
_phase1_years_0 = min(20, _remaining_years_0)
_phase2_years_0 = _remaining_years_0 - 20
_current_pc_growth_0 = (
    float(CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20) / float(GLOBAL_AVG_INCOME_2025)
) ** (1 / 20) - 1
_treaty_pc_growth_0 = (
    float(TREATY_TRAJECTORY_AVG_INCOME_YEAR_20) / float(GLOBAL_AVG_INCOME_2025)
) ** (1 / 20) - 1
_wishonia_pc_growth_0 = (
    float(WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20) / float(GLOBAL_AVG_INCOME_2025)
) ** (1 / 20) - 1


CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME = Parameter(
    float(GLOBAL_AVG_INCOME_2025)
    * (1 + _current_pc_growth_0)
    * (((1 + _current_pc_growth_0) ** _remaining_years_0) - 1)
    / _current_pc_growth_0,
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Cumulative per-capita income over an average remaining lifespan under current trajectory "
                "baseline trajectory. Uses the implied per-capita baseline CAGR from 2025 to 2045.",
    display_name="Current Trajectory Cumulative Lifetime Income (Per Capita)",
    unit="USD",
    formula="GLOBAL_AVG_INCOME_2025 * (1+g_pc,base) * ((1+g_pc,base)^T - 1) / g_pc,base, where g_pc,base is implied by CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20",
    latex=r"Y_{cum,earth} = \bar{y}_0 \cdot \frac{(1+g_{pc,base})((1+g_{pc,base})^{T_{remaining}}-1)}{g_{pc,base}}",
    inputs=["GLOBAL_AVG_INCOME_2025", "CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20", "GLOBAL_AVG_REMAINING_YEARS"],
    compute=lambda ctx: (
        ctx["GLOBAL_AVG_INCOME_2025"]
        * (
            1
            + (
                (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                - 1
            )
        )
        * (
            (
                1
                + (
                    (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                    - 1
                )
            ) ** int(ctx["GLOBAL_AVG_REMAINING_YEARS"])
            - 1
        )
        / (
            (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
            - 1
        )
    ),
    latex_symbol=r"Y_{cum,earth}",
)

TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME = Parameter(
    (
        float(GLOBAL_AVG_INCOME_2025)
        * (1 + _treaty_pc_growth_0)
        * (((1 + _treaty_pc_growth_0) ** _phase1_years_0) - 1)
        / _treaty_pc_growth_0
    )
    + (
        float(TREATY_TRAJECTORY_AVG_INCOME_YEAR_20)
        * (1 + _current_pc_growth_0)
        * (((1 + _current_pc_growth_0) ** _phase2_years_0) - 1)
        / _current_pc_growth_0
        if _phase2_years_0 > 0
        else 0
    ),
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Cumulative per-capita income over an average remaining lifespan under Treaty Trajectory. "
                "Uses implied per-capita CAGR for years 1-20 (derived from known year-0 and year-20 "
                "per-capita incomes), then current-trajectory per-capita growth from the year-20 level. "
                "Conservative: assumes no further treaty acceleration beyond year 20.",
    display_name="Treaty Trajectory Cumulative Lifetime Income (Per Capita)",
    unit="USD",
    formula="Phase 1: y0*(1+g_pc,treaty)*((1+g_pc,treaty)^20-1)/g_pc,treaty + Phase 2: y20*(1+g_pc,base)*((1+g_pc,base)^(T-20)-1)/g_pc,base",
    latex=r"Y_{cum,treaty} = \bar{y}_0 \cdot \frac{(1+g_{pc,treaty})((1+g_{pc,treaty})^{20}-1)}{g_{pc,treaty}} + \bar{y}_{treaty,20} \cdot \frac{(1+g_{pc,base})((1+g_{pc,base})^{T_{remaining}-20}-1)}{g_{pc,base}}",
    inputs=["GLOBAL_AVG_INCOME_2025", "TREATY_TRAJECTORY_AVG_INCOME_YEAR_20", "CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20",
            "GLOBAL_AVG_REMAINING_YEARS"],
    compute=lambda ctx: (
        (
            ctx["GLOBAL_AVG_INCOME_2025"]
            * (
                ctx["TREATY_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]
            ) ** (1 / 20)
            * (
                (
                    (
                        ctx["TREATY_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]
                    ) ** (1 / 20)
                ) ** min(20, int(ctx["GLOBAL_AVG_REMAINING_YEARS"]))
                - 1
            )
            / (
                (
                    ctx["TREATY_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]
                ) ** (1 / 20)
                - 1
            )
        )
        + (
            ctx["TREATY_TRAJECTORY_AVG_INCOME_YEAR_20"]
            * (
                1
                + (
                    (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                    - 1
                )
            )
            * (
                (
                    1
                    + (
                        (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                        - 1
                    )
                ) ** (int(ctx["GLOBAL_AVG_REMAINING_YEARS"]) - 20)
                - 1
            )
            / (
                (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                - 1
            )
            if int(ctx["GLOBAL_AVG_REMAINING_YEARS"]) > 20
            else 0
        )
    ),
    latex_symbol=r"Y_{cum,treaty}",
)

TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA = Parameter(
    float(TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME) - float(CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME),
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Lifetime per-capita income gain from Treaty Trajectory vs current trajectory. "
                "Cumulative treaty income minus cumulative earth income over average remaining lifespan. "
                "Uses global averages; individual gain scales with starting income.",
    display_name="Treaty Trajectory Lifetime Income Gain (Per Capita)",
    unit="USD",
    formula="TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME - CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME",
    inputs=["TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME", "CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"] - ctx["CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    latex_symbol=r"\Delta Y_{lifetime,treaty}",
)

TREATY_TRAJECTORY_LIFETIME_INCOME_MULTIPLIER = Parameter(
    float(TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME) / float(CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME),
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Ratio of cumulative lifetime income under Treaty Trajectory vs current trajectory. "
                "Income-agnostic: applies as a multiplier to any individual's lifetime earnings.",
    display_name="Treaty Trajectory Lifetime Income Multiplier",
    unit="x",
    formula="TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME / CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME",
    inputs=["TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME", "CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"] / ctx["CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    latex_symbol=r"k_{lifetime,treaty:earth}",
)

WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME = Parameter(
    (
        float(GLOBAL_AVG_INCOME_2025)
        * (1 + _wishonia_pc_growth_0)
        * (((1 + _wishonia_pc_growth_0) ** _phase1_years_0) - 1)
        / _wishonia_pc_growth_0
    )
    + (
        float(WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20)
        * (1 + _current_pc_growth_0)
        * (((1 + _current_pc_growth_0) ** _phase2_years_0) - 1)
        / _current_pc_growth_0
        if _phase2_years_0 > 0
        else 0
    ),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Cumulative per-capita income over an average remaining lifespan under Wishonia Trajectory. "
                "Uses implied per-capita CAGR for years 1-20, then current-trajectory per-capita growth "
                "from the year-20 level. Conservative: assumes no further acceleration beyond year 20.",
    display_name="Wishonia Trajectory Cumulative Lifetime Income (Per Capita)",
    unit="USD",
    formula="Phase 1: y0*(1+g_pc,wish)*((1+g_pc,wish)^20-1)/g_pc,wish + Phase 2: y20*(1+g_pc,base)*((1+g_pc,base)^(T-20)-1)/g_pc,base",
    latex=r"Y_{cum,wish} = \bar{y}_0 \cdot \frac{(1+g_{pc,wish})((1+g_{pc,wish})^{20}-1)}{g_{pc,wish}} + \bar{y}_{wish,20} \cdot \frac{(1+g_{pc,base})((1+g_{pc,base})^{T_{remaining}-20}-1)}{g_{pc,base}}",
    inputs=["GLOBAL_AVG_INCOME_2025", "WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20", "CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20",
            "GLOBAL_AVG_REMAINING_YEARS"],
    compute=lambda ctx: (
        (
            ctx["GLOBAL_AVG_INCOME_2025"]
            * (
                ctx["WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]
            ) ** (1 / 20)
            * (
                (
                    (
                        ctx["WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]
                    ) ** (1 / 20)
                ) ** min(20, int(ctx["GLOBAL_AVG_REMAINING_YEARS"]))
                - 1
            )
            / (
                (
                    ctx["WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]
                ) ** (1 / 20)
                - 1
            )
        )
        + (
            ctx["WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20"]
            * (
                1
                + (
                    (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                    - 1
                )
            )
            * (
                (
                    1
                    + (
                        (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                        - 1
                    )
                ) ** (int(ctx["GLOBAL_AVG_REMAINING_YEARS"]) - 20)
                - 1
            )
            / (
                (ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"] / ctx["GLOBAL_AVG_INCOME_2025"]) ** (1 / 20)
                - 1
            )
            if int(ctx["GLOBAL_AVG_REMAINING_YEARS"]) > 20
            else 0
        )
    ),
    latex_symbol=r"Y_{cum,wish}",
)

WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA = Parameter(
    float(WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME) - float(CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Lifetime per-capita income gain from Wishonia Trajectory vs current trajectory. "
                "Cumulative Wishonia income minus cumulative current trajectory income over average remaining lifespan.",
    display_name="Wishonia Trajectory Lifetime Income Gain (Per Capita)",
    unit="USD",
    formula="WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME - CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME",
    inputs=["WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME", "CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"] - ctx["CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    latex_symbol=r"\Delta Y_{lifetime,wish}",
)

TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH = Parameter(
    float(TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA) + float(TREATY_HALE_VALUE_PER_CAPITA),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Personal upside under Treaty Trajectory: lifetime income gain plus valued healthy-life gains.",
    display_name="Treaty Personal Upside (Income + Health)",
    unit="USD/person",
    formula="TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA + TREATY_HALE_VALUE_PER_CAPITA",
    inputs=["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA", "TREATY_HALE_VALUE_PER_CAPITA"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"] + ctx["TREATY_HALE_VALUE_PER_CAPITA"],
    keywords=["treaty", "personal", "upside", "blended", "income", "health"],
    latex_symbol=r"Upside_{income+health,treaty}",
)

WISHONIA_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH = Parameter(
    float(WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA) + float(WISHONIA_HALE_VALUE_PER_CAPITA),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Personal upside under Wishonia Trajectory: lifetime income gain plus valued healthy-life gains.",
    display_name="Wishonia Personal Upside (Income + Health)",
    unit="USD/person",
    formula="WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA + WISHONIA_HALE_VALUE_PER_CAPITA",
    inputs=["WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA", "WISHONIA_HALE_VALUE_PER_CAPITA"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"] + ctx["WISHONIA_HALE_VALUE_PER_CAPITA"],
    keywords=["wishonia", "personal", "upside", "blended", "income", "health"],
    latex_symbol=r"Upside_{income+health,wish}",
)

WISHONIA_TRAJECTORY_LIFETIME_INCOME_MULTIPLIER = Parameter(
    float(WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME) / float(CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Ratio of cumulative lifetime income under Wishonia Trajectory vs current trajectory. "
                "Income-agnostic: applies as a multiplier to any individual's lifetime earnings.",
    display_name="Wishonia Trajectory Lifetime Income Multiplier",
    unit="x",
    formula="WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME / CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME",
    inputs=["WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME", "CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"] / ctx["CURRENT_TRAJECTORY_CUMULATIVE_LIFETIME_INCOME"],
    latex_symbol=r"k_{lifetime,wish:earth}",
)

# ---
# MEDIAN AFTER-TAX REAL INCOME TRACK (parallel to the GDP / mean-income track)
# ---
# GDP counts regrettables: pay an arsonist and then pay a firefighter and GDP rises
# while nobody is better off (Nordhaus & Tobin's 1972 Measure of Economic Welfare
# subtracted defense spending from output for exactly this reason). The median
# person's consumable income is modeled as:
#   mean income (the scenario GDP trajectories)
#   x (1 - military share of GDP)   <- the regrettables deduction. MILITARY ONLY:
#     hard SIPRI data, and literally what the book is about. Cybercrime is OUT of
#     the central model (v2): loss estimates count transfers (a stolen dollar still
#     buys bread, for the thief) and double-counted indirect costs, so subtracting
#     them 1:1 from consumable output was wrong. Crime belongs in the collapse
#     scenario and, eventually, in an endogenous crime-participation model (the
#     share of people for whom extraction pays better than legitimate work, i.e.
#     the chapter's "rational crime threshold" formalized). Documented future work.
#   x median-to-mean ratio          <- DERIVED from Gallup's measured global median
#     (the only survey of the middle human's income that exists), never chosen.
#     Anchoring to the measurement and deriving the ratio kills the circularity of
#     picking a ratio "from Gallup's range" and then claiming Gallup validates it.
#   x (1 - erosion)^t               <- best guess ZERO: the global median's share
#     of mean income ROSE 1990-2019 (between-country convergence); the US wedge is
#     the extreme, not the world. The uncertainty range covers both directions.
#   x (1 + relief x cure fraction)  <- treaty/wishonia only: cures return sick
#     wages and out-of-pocket health costs to the people who bear them, who live
#     at and below the middle (WHO: half a billion pushed into extreme poverty by
#     health costs). The one pro-median channel, WHO-anchored, honest range.
#   x (1 - effective tax rate), identical across scenarios (no thumb on the scale).
# EPISTEMOLOGY (author's rule): deliberate accuracy + deliberate uncertainty, never
# deliberate conservatism. Every input is a best guess with an honest range; a
# conservative case is a low percentile of the OUTPUT distribution, not a biased
# input. No caps, no patches, no thumbs on scales in either direction.
# NAMING NOTE: this is a WELFARE-INCOME construct (Nordhaus-Tobin style: regrettables
# subtracted from what the median's income can buy), not a household income statistic.
# A defense engineer's salary IS median income; no agency deducts the missile from the
# paycheck. Display names therefore say "consumable income".
# The collapse branch (extraction crosses the rational-crime threshold, defection
# cascades, GDP and median crater together toward the documented 70-90% extractive
# equilibria) is a SEPARATE scenario in the chapter narrative, not a deduction
# smuggled into the central path as a deterministic exponential.

GALLUP_GLOBAL_MEDIAN_INCOME_PER_CAPITA = Parameter(
    2_920,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_ref="gallup-global-median-income-2013",
    source_type="external",
    description="Global median per-capita household income as measured by the Gallup World Poll "
                "(131 countries, PPP dollars, published 2013): the only comprehensive survey-based "
                "measurement of the middle human's income that exists. The median-to-mean ratio is "
                "DERIVED from this anchor rather than chosen, so the model is calibrated to a "
                "measured human. The confidence interval covers the anchor's vintage (global "
                "medians grew after 2013, pushing the true current value above the point estimate) "
                "and PPP-vs-market-rate conversion (pushing it below).",
    display_name="Gallup Global Median Per-Capita Income (2013, PPP)",
    unit="USD",
    confidence="medium",
    distribution="normal",
    confidence_interval=(2_300, 3_700),
    keywords=["gallup", "median income", "global", "survey", "anchor", "PPP", "middle person"],
    latex_symbol=r"\tilde{y}_{gallup}",
)

GLOBAL_MILITARY_SHARE_OF_GDP = Parameter(
    float(GLOBAL_MILITARY_SPENDING_ANNUAL_2024) / float(GLOBAL_GDP_2025),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Military spending as a share of global GDP (SIPRI spending over IMF output). The "
                "regrettables deduction in the median consumable-income track: output that is made "
                "and counted but cannot be eaten. Military ONLY, by design: it is hard data and the "
                "book's actual subject. Cybercrime was removed from this deduction (v2): loss "
                "estimates count transfers and double-counted indirect costs, not uneaten output.",
    display_name="Military Share of Global GDP",
    unit="percent",
    formula="GLOBAL_MILITARY_SPENDING_ANNUAL_2024 ÷ GLOBAL_GDP_2025",
    inputs=["GLOBAL_MILITARY_SPENDING_ANNUAL_2024", "GLOBAL_GDP_2025"],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_GDP_2025"],
    keywords=["military", "share", "GDP", "regrettables", "SIPRI", "deduction"],
    latex_symbol=r"s_{mil}",
)

GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO = Parameter(
    float(GALLUP_GLOBAL_MEDIAN_INCOME_PER_CAPITA) / float(GLOBAL_AVG_INCOME_2025),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Global median-to-mean income ratio, DERIVED from the Gallup anchor against mean "
                "income (GDP per capita): the median human receives about twenty-one cents of the "
                "average dollar. Pre-tax basis on both sides. The derivation replaces a hand-chosen "
                "0.30 'from Gallup's range', which made the model's agreement with Gallup circular. "
                "This single number is why GDP per capita overstates what a typical person earns by "
                "roughly 5x.",
    display_name="Global Median-to-Mean Income Ratio",
    unit="ratio",
    formula="GALLUP_GLOBAL_MEDIAN_INCOME_PER_CAPITA ÷ GLOBAL_AVG_INCOME_2025",
    inputs=["GALLUP_GLOBAL_MEDIAN_INCOME_PER_CAPITA", "GLOBAL_AVG_INCOME_2025"],
    compute=lambda ctx: ctx["GALLUP_GLOBAL_MEDIAN_INCOME_PER_CAPITA"] / ctx["GLOBAL_AVG_INCOME_2025"],
    keywords=["median income", "mean income", "ratio", "inequality", "typical person", "gallup"],
    latex_symbol=r"\rho_{med}",
)

GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL = Parameter(
    0.0,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_ref="epi-productivity-pay-gap-2024",
    source_type="definition",
    description="Annual erosion of the median's share of mean income (positive = the middle "
                "person's slice shrinks). Best guess ZERO: the GLOBAL median-to-mean ratio ROSE "
                "1990-2019 via between-country convergence (a billion people in Asia got real "
                "jobs), so the measured global sign favors the median; the US wedge is the extreme, "
                "not the world. The range spans continued convergence (-0.5%/yr, the share keeps "
                "growing) to the US-extreme construction applied globally (+0.78%/yr; EPI: "
                "productivity +90.2% vs typical pay +33.0%, 1979-2025). Applied IDENTICALLY to the "
                "status-quo and treaty branches, so it cancels out of every treaty-vs-current "
                "multiplier; Wishonia excludes it (the wishocratic mechanism exists to stop share "
                "capture). v1 set this to 0.5%/yr shrinkage as skeptic armor; that was deliberate "
                "conservatism, replaced by deliberate accuracy plus deliberate uncertainty.",
    display_name="Median Share Erosion Rate (Annual)",
    unit="rate",
    confidence="low",
    distribution="normal",
    confidence_interval=(-0.005, 0.0078),
    keywords=["median", "erosion", "productivity pay gap", "convergence", "labor share"],
    latex_symbol=r"e_{med}",
)

GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN = Parameter(
    0.25,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="definition",
    description="Effective combined tax rate (direct plus indirect) on the global median earner. "
                "Applied IDENTICALLY across all scenarios so it shifts levels without affecting any "
                "cross-scenario comparison: there is no pro-treaty thumb on this scale. The 'after-tax' "
                "in the metric name is honesty about levels, not a modeling lever.",
    display_name="Effective Tax Rate on Median Earner",
    unit="rate",
    confidence="low",
    distribution="fixed",
    keywords=["tax", "after-tax", "median", "effective rate"],
    latex_symbol=r"\tau_{med}",
)

MEDIAN_HEALTH_BURDEN_RELIEF_SHARE = Parameter(
    0.10,
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_ref="who-health-costs-extreme-poverty-2021",
    source_type="definition",
    description="Fraction by which curing ALL currently untreatable disease would raise the median "
                "person's consumable income, beyond the mean-income effect already inside the GDP "
                "trajectories. Mechanism: out-of-pocket health spending and sick-day wage losses "
                "fall disproportionately on people at and below the median (WHO: about half a "
                "billion people pushed into extreme poverty by health costs, roughly 2 billion "
                "facing catastrophic or impoverishing health spending). Scaled by each scenario's "
                "cure fraction, so partial cures give partial relief. The range reflects genuine "
                "uncertainty about how much of that burden the queue's early cures relieve.",
    display_name="Median Income Relief from Full Disease Cure",
    unit="rate",
    confidence="low",
    distribution="normal",
    confidence_interval=(0.05, 0.15),
    keywords=["median", "health costs", "out-of-pocket", "catastrophic", "relief", "WHO", "poverty"],
    latex_symbol=r"r_{relief}",
)

# Module helpers for the median track (existing inline style; no new functions).
# Status quo: military share drifts at its measured SIPRI-vs-GDP differential.
# Treaty: by years 13+ the ratchet is redirecting the terminal share of military
# spending (TREATY_RATCHET_TERMINAL_SHARE, the single ratchet knob), so the
# year-15/20 levels use it.
_mil_share_0 = float(GLOBAL_MILITARY_SHARE_OF_GDP)
_mil_drift = (1 + float(GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR)) / (1 + float(GDP_BASELINE_GROWTH_RATE))

GLOBAL_MEDIAN_AFTER_TAX_INCOME_2025 = Parameter(
    float(GLOBAL_AVG_INCOME_2025)
    * (1 - _mil_share_0)
    * float(GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO)
    * (1 - float(GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Median after-tax consumable income today: mean income x (1 - military share) x "
                "median-to-mean ratio x (1 - tax). Because the ratio is derived from the Gallup "
                "anchor, this equals Gallup's measured median with the military slice and taxes "
                "removed. The baseline the three scenario trajectories grow from.",
    display_name="Global Median After-Tax Consumable Income (2025)",
    unit="USD",
    formula="GLOBAL_AVG_INCOME_2025 * (1 - GLOBAL_MILITARY_SHARE_OF_GDP) * GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO * (1 - GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)",
    inputs=["GLOBAL_AVG_INCOME_2025", "GLOBAL_MILITARY_SHARE_OF_GDP",
            "GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO", "GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"],
    compute=lambda ctx: ctx["GLOBAL_AVG_INCOME_2025"]
    * (1 - ctx["GLOBAL_MILITARY_SHARE_OF_GDP"])
    * ctx["GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO"]
    * (1 - ctx["GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"]),
    latex_symbol=r"\tilde{m}_{0}",
)

CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20 = Parameter(
    float(CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20)
    * (1 - _mil_share_0 * _mil_drift ** 20)
    * float(GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO)
    * (1 - float(GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)) ** 20
    * (1 - float(GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Median after-tax consumable income at year 20 under the status quo: the world more "
                "or less as trended. Mean income grows at the baseline rate, the military share "
                "drifts up at its measured SIPRI-vs-GDP differential, the median's share holds "
                "(best guess zero erosion, range covers both directions), so the median grows "
                "roughly with GDP per capita. v1's compounding destructive share and assumed "
                "erosion made the median mysteriously die against 35 years of contrary observed "
                "history; that branch is gone. The collapse scenario (extraction crosses the "
                "rational-crime threshold and GDP craters with the median) is narrated separately, "
                "not smuggled into this baseline.",
    display_name="Median After-Tax Consumable Income, Status Quo (Year 20)",
    unit="USD",
    formula="CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20 * (1 - GLOBAL_MILITARY_SHARE_OF_GDP * ((1+GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR)/(1+GDP_BASELINE_GROWTH_RATE))^20) * GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO * (1 - GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)^20 * (1 - GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)",
    inputs=["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20", "GLOBAL_MILITARY_SHARE_OF_GDP",
            "GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR", "GDP_BASELINE_GROWTH_RATE",
            "GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO", "GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL",
            "GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"],
    compute=lambda ctx: ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_20"]
    * (1 - ctx["GLOBAL_MILITARY_SHARE_OF_GDP"]
       * ((1 + ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR"]) / (1 + ctx["GDP_BASELINE_GROWTH_RATE"])) ** 20)
    * ctx["GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO"]
    * (1 - ctx["GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL"]) ** 20
    * (1 - ctx["GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"]),
    latex_symbol=r"\tilde{m}_{base,20}",
)

TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20 = Parameter(
    float(TREATY_TRAJECTORY_AVG_INCOME_YEAR_20)
    * (1 - _mil_share_0 * (1 - _S_ratchet))
    * float(GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO)
    * (1 - float(GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)) ** 20
    * (1 + float(MEDIAN_HEALTH_BURDEN_RELIEF_SHARE) * float(TREATY_DISEASE_CURE_FRACTION_20YR))
    * (1 - float(GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Median after-tax consumable income at year 20 under the Treaty Trajectory. Mean "
                "income from the treaty GDP trajectory; military share reduced by the ratchet's "
                "terminal redirect (the single ratchet knob); the same share erosion as the status "
                "quo (best guess zero) so distributional claims cancel out of the multiplier; plus "
                "the one pro-median channel: cures return out-of-pocket health costs and sick wages "
                "to the people who bear them (WHO-anchored relief share scaled by the ratchet-"
                "schedule cure fraction).",
    display_name="Median After-Tax Consumable Income, Treaty (Year 20)",
    unit="USD",
    formula="TREATY_TRAJECTORY_AVG_INCOME_YEAR_20 * (1 - GLOBAL_MILITARY_SHARE_OF_GDP * (1 - TREATY_RATCHET_TERMINAL_SHARE)) * GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO * (1 - GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)^20 * (1 + MEDIAN_HEALTH_BURDEN_RELIEF_SHARE * TREATY_DISEASE_CURE_FRACTION_20YR) * (1 - GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)",
    inputs=["TREATY_TRAJECTORY_AVG_INCOME_YEAR_20", "GLOBAL_MILITARY_SHARE_OF_GDP",
            "TREATY_RATCHET_TERMINAL_SHARE", "GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO",
            "GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL", "MEDIAN_HEALTH_BURDEN_RELIEF_SHARE",
            "TREATY_DISEASE_CURE_FRACTION_20YR", "GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_AVG_INCOME_YEAR_20"]
    * (1 - ctx["GLOBAL_MILITARY_SHARE_OF_GDP"] * (1 - ctx["TREATY_RATCHET_TERMINAL_SHARE"]))
    * ctx["GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO"]
    * (1 - ctx["GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL"]) ** 20
    * (1 + ctx["MEDIAN_HEALTH_BURDEN_RELIEF_SHARE"] * ctx["TREATY_DISEASE_CURE_FRACTION_20YR"])
    * (1 - ctx["GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"]),
    latex_symbol=r"\tilde{m}_{treaty,20}",
)

WISHONIA_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20 = Parameter(
    float(WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20)
    * (1 - _mil_share_0 * (1 - float(WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE)))
    * float(GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO)
    * (1 + float(MEDIAN_HEALTH_BURDEN_RELIEF_SHARE) * float(WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL))
    * (1 - float(GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Median after-tax consumable income at year 20 under the Wishonia Trajectory. "
                "Claims tied to mechanisms: share erosion excluded (the wishocratic one-person-one-"
                "vote mechanism exists precisely to stop the capture that drives the wedge), the "
                "military share falls by the already-parameterized physical max reallocation, and "
                "the health-burden relief channel applies at Wishonia's own full-implementation "
                "cure fraction. Deliberately UNMODELED: the wishocratic equal-per-person allocation "
                "of recovered dysfunction waste is pro-median by arithmetic, but that recovery is "
                "already inside the Wishonia GDP trajectory, so modeling its distributional bonus "
                "separately would double-count. The bonus is real and omitted; this estimate is "
                "therefore a floor.",
    display_name="Median After-Tax Consumable Income, Wishonia (Year 20)",
    unit="USD",
    formula="WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20 * (1 - GLOBAL_MILITARY_SHARE_OF_GDP*(1-WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE)) * GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO * (1 + MEDIAN_HEALTH_BURDEN_RELIEF_SHARE * WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL) * (1 - GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)",
    inputs=["WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20", "GLOBAL_MILITARY_SHARE_OF_GDP",
            "WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE", "GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO",
            "MEDIAN_HEALTH_BURDEN_RELIEF_SHARE", "WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL",
            "GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_AVG_INCOME_YEAR_20"]
    * (1 - ctx["GLOBAL_MILITARY_SHARE_OF_GDP"] * (1 - ctx["WISHONIA_MILITARY_REALLOCATION_PHYSICAL_MAX_SHARE"]))
    * ctx["GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO"]
    * (1 + ctx["MEDIAN_HEALTH_BURDEN_RELIEF_SHARE"] * ctx["WISHONIA_DISEASE_CURE_FRACTION_20YR_FULL"])
    * (1 - ctx["GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"]),
    latex_symbol=r"\tilde{m}_{wish,20}",
)

CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_15 = Parameter(
    float(CURRENT_TRAJECTORY_AVG_INCOME_YEAR_15)
    * (1 - _mil_share_0 * _mil_drift ** 15)
    * float(GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO)
    * (1 - float(GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)) ** 15
    * (1 - float(GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Median after-tax consumable income at year 15 under the status quo. Same "
                "construction as the year-20 variant: mean income x (1 - military share, drifting "
                "at its measured SIPRI-vs-GDP differential) x median-to-mean ratio x (1 - erosion, "
                "best guess zero)^15 x (1 - tax).",
    display_name="Median After-Tax Consumable Income, Status Quo (Year 15)",
    unit="USD",
    formula="CURRENT_TRAJECTORY_AVG_INCOME_YEAR_15 * (1 - GLOBAL_MILITARY_SHARE_OF_GDP * ((1+GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR)/(1+GDP_BASELINE_GROWTH_RATE))^15) * GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO * (1 - GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)^15 * (1 - GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)",
    inputs=["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_15", "GLOBAL_MILITARY_SHARE_OF_GDP",
            "GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR", "GDP_BASELINE_GROWTH_RATE",
            "GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO", "GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL",
            "GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"],
    compute=lambda ctx: ctx["CURRENT_TRAJECTORY_AVG_INCOME_YEAR_15"]
    * (1 - ctx["GLOBAL_MILITARY_SHARE_OF_GDP"]
       * ((1 + ctx["GLOBAL_MILITARY_SPENDING_REAL_CAGR_10YR"]) / (1 + ctx["GDP_BASELINE_GROWTH_RATE"])) ** 15)
    * ctx["GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO"]
    * (1 - ctx["GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL"]) ** 15
    * (1 - ctx["GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"]),
    latex_symbol=r"\tilde{m}_{base,15}",
)

TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_15 = Parameter(
    float(TREATY_TRAJECTORY_AVG_INCOME_YEAR_15)
    * (1 - _mil_share_0 * (1 - _S_ratchet))
    * float(GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO)
    * (1 - float(GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)) ** 15
    * (1 + float(MEDIAN_HEALTH_BURDEN_RELIEF_SHARE) * float(TREATY_DISEASE_CURE_FRACTION_15YR))
    * (1 - float(GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)),
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Median after-tax consumable income at year 15 under the Treaty Trajectory. Same "
                "construction as the year-20 variant: military share reduced by the ratchet's "
                "terminal redirect (the single ratchet knob), same erosion as the status quo (best "
                "guess zero) so distributional claims cancel, plus the WHO-anchored health-burden "
                "relief channel scaled by the ratchet-schedule cure fraction. Feeds the Prize "
                "settlement target.",
    display_name="Median After-Tax Consumable Income, Treaty (Year 15)",
    unit="USD",
    formula="TREATY_TRAJECTORY_AVG_INCOME_YEAR_15 * (1 - GLOBAL_MILITARY_SHARE_OF_GDP * (1 - TREATY_RATCHET_TERMINAL_SHARE)) * GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO * (1 - GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL)^15 * (1 + MEDIAN_HEALTH_BURDEN_RELIEF_SHARE * TREATY_DISEASE_CURE_FRACTION_15YR) * (1 - GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN)",
    inputs=["TREATY_TRAJECTORY_AVG_INCOME_YEAR_15", "GLOBAL_MILITARY_SHARE_OF_GDP",
            "TREATY_RATCHET_TERMINAL_SHARE", "GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO",
            "GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL", "MEDIAN_HEALTH_BURDEN_RELIEF_SHARE",
            "TREATY_DISEASE_CURE_FRACTION_15YR", "GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_AVG_INCOME_YEAR_15"]
    * (1 - ctx["GLOBAL_MILITARY_SHARE_OF_GDP"] * (1 - ctx["TREATY_RATCHET_TERMINAL_SHARE"]))
    * ctx["GLOBAL_MEDIAN_TO_MEAN_INCOME_RATIO"]
    * (1 - ctx["GLOBAL_MEDIAN_SHARE_EROSION_RATE_ANNUAL"]) ** 15
    * (1 + ctx["MEDIAN_HEALTH_BURDEN_RELIEF_SHARE"] * ctx["TREATY_DISEASE_CURE_FRACTION_15YR"])
    * (1 - ctx["GLOBAL_EFFECTIVE_TAX_RATE_MEDIAN"]),
    latex_symbol=r"\tilde{m}_{treaty,15}",
)

# ---
# PRIZE SETTLEMENT TARGETS (single source of truth for the Game's payout trigger)
# ---
# The Earth Optimization Prize settles on these two parameters and nothing else.
# Author decision 2026-06-10: targets are TREATY-trajectory year-15 values (the
# achievable floor), not Wishonia-trajectory values (the ceiling). Before this,
# the prize page and the protocol spec used treaty values while protocol-v1 had
# drifted to Wishonia values, and all three bound MEAN-income parameters under a
# "median income" label. All settlement references now bind these two params.

PRIZE_TARGET_HALE_YEAR_15 = Parameter(
    float(TREATY_PROJECTED_HALE_YEAR_15),
    manual_ref="knowledge/appendix/earth-optimization-prize-protocol.qmd",
    source_type="calculated",
    description="The Earth Optimization Prize settlement target for global HALE at year 15. "
                "Set to the Treaty-trajectory projection (the achievable floor). The terminal general-welfare metric "
                "oracle compares measured global HALE against this value.",
    display_name="Prize Settlement Target: Global HALE (Year 15)",
    unit="years",
    formula="TREATY_PROJECTED_HALE_YEAR_15",
    inputs=["TREATY_PROJECTED_HALE_YEAR_15"],
    compute=lambda ctx: ctx["TREATY_PROJECTED_HALE_YEAR_15"],
    keywords=["prize", "settlement", "target", "oracle", "HALE", "trigger"],
    latex_symbol=r"HALE^{*}_{15}",
)

PRIZE_TARGET_MEDIAN_INCOME_YEAR_15 = Parameter(
    float(TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_15),
    manual_ref="knowledge/appendix/earth-optimization-prize-protocol.qmd",
    source_type="calculated",
    description="MODEL PROJECTION that informs the Prize settlement target for global median income "
                "at year 15 (Treaty-trajectory median). NOT the binding trigger: per the Target Lock "
                "clause in the protocol spec, a pool freezes its targets as literal constants in a "
                "signed Settlement Schedule before its first deposit, denominated as a multiple of the "
                "Referee's baseline MEASURED value so target and measurement share identical units. "
                "This parameter is the rationale for the locked number, never its definition.",
    display_name="Prize Settlement Target: Median Income (Year 15)",
    unit="USD",
    formula="TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_15",
    inputs=["TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_15"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_15"],
    keywords=["prize", "settlement", "target", "oracle", "median income", "trigger"],
    latex_symbol=r"\tilde{m}^{*}_{15}",
)

TREATY_VS_CURRENT_MEDIAN_INCOME_MULTIPLIER_YEAR_20 = Parameter(
    float(TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20)
    / float(CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Median after-tax income at year 20: Treaty vs status quo. Larger than the GDP "
                "multiplier for two auditable reasons: the treaty cuts the military deduction by "
                "the ratchet's terminal redirect while the status-quo military share drifts up on "
                "its measured trend, and the WHO-anchored health-burden relief channel applies "
                "only on the treaty branch. Share erosion is identical in both branches and "
                "cancels out of this ratio by construction.",
    display_name="Treaty vs Status Quo Median Income Multiplier (Year 20)",
    unit="x",
    formula="TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20 / CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20",
    inputs=["TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20", "CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20"]
    / ctx["CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20"],
    latex_symbol=r"k_{med,treaty:base}",
)

WISHONIA_VS_CURRENT_MEDIAN_INCOME_MULTIPLIER_YEAR_20 = Parameter(
    float(WISHONIA_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20)
    / float(CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20),
    manual_ref="knowledge/economics/gdp-trajectories.qmd",
    source_type="calculated",
    description="Median after-tax income at year 20: Wishonia vs status quo.",
    display_name="Wishonia vs Status Quo Median Income Multiplier (Year 20)",
    unit="x",
    formula="WISHONIA_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20 / CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20",
    inputs=["WISHONIA_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20", "CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20"]
    / ctx["CURRENT_TRAJECTORY_MEDIAN_AFTER_TAX_INCOME_YEAR_20"],
    latex_symbol=r"k_{med,wish:base}",
)

# ---
# SHARING OPPORTUNITY COST (Downside of the Payoff Matrix)
# ---
# Quantifies the dollar cost of forwarding the message if the plan is impossible.
# Uses average (not median) hourly income, which OVERestimates the cost, making
# the payoff ratio conservative.

SHARING_TIME_MINUTES = Parameter(
    0.5,
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="definition",
    distribution="fixed",
    description="Time to copy, paste, and send the recruitment message. 30 seconds.",
    display_name="Sharing Time",
    unit="minutes",
    keywords=["sharing", "forwarding", "time", "cost", "30 seconds"],
    latex_symbol=r"t_{share}",
)

ANNUAL_WORKING_HOURS = Parameter(
    2_000,
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="definition",
    distribution="fixed",
    description="Standard annual working hours globally. Approximately 40 hours/week x 50 weeks. "
                "ILO estimates range from 1,800-2,200 across countries; 2,000 is conventional.",
    display_name="Annual Working Hours",
    unit="hours/year",
    keywords=["working hours", "annual", "labor", "employment"],
    latex_symbol=r"H_{work}",
)

GLOBAL_AVG_HOURLY_INCOME = Parameter(
    float(GLOBAL_AVG_INCOME_2025) / 2_000,
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Global average hourly income derived from GDP per capita. Uses average (not median), "
                "which overestimates the cost of sharing, making the payoff ratio conservative.",
    display_name="Global Average Hourly Income",
    unit="USD/hour",
    formula="GLOBAL_AVG_INCOME_2025 / ANNUAL_WORKING_HOURS",
    inputs=["GLOBAL_AVG_INCOME_2025", "ANNUAL_WORKING_HOURS"],
    compute=lambda ctx: ctx["GLOBAL_AVG_INCOME_2025"] / ctx["ANNUAL_WORKING_HOURS"],
    latex_symbol=r"\bar{w}_{hour}",
)

SHARING_OPPORTUNITY_COST = Parameter(
    (0.5 / 60) * float(GLOBAL_AVG_INCOME_2025) / 2_000,
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Dollar cost of 30 seconds at global average hourly income. "
                "The maximum downside of forwarding the message if the plan is impossible.",
    display_name="Sharing Opportunity Cost",
    unit="USD",
    formula="(SHARING_TIME_MINUTES / 60) * GLOBAL_AVG_HOURLY_INCOME",
    inputs=["SHARING_TIME_MINUTES", "GLOBAL_AVG_HOURLY_INCOME"],
    compute=lambda ctx: (ctx["SHARING_TIME_MINUTES"] / 60) * ctx["GLOBAL_AVG_HOURLY_INCOME"],
    latex_symbol=r"C_{share}",
)

SHARING_UPSIDE_DOWNSIDE_RATIO_TREATY = Parameter(
    float(TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA) / float(SHARING_OPPORTUNITY_COST),
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Raw ratio of upside (lifetime income gain if plan works) to downside (cost of sharing "
                "if plan is impossible). Not expected value; see SHARING_BREAKEVEN_PROBABILITY_TREATY for the "
                "probability threshold that makes forwarding rational.",
    display_name="Sharing Upside/Downside Ratio",
    unit="x",
    formula="TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA / SHARING_OPPORTUNITY_COST",
    inputs=["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA", "SHARING_OPPORTUNITY_COST"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"] / ctx["SHARING_OPPORTUNITY_COST"],
    latex_symbol=r"k_{upside:downside}",
)

SHARING_BREAKEVEN_PROBABILITY_TREATY = Parameter(
    float(SHARING_OPPORTUNITY_COST) / float(TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA),
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Minimum probability that the plan works for forwarding to have positive expected value. "
                "EV > 0 when P(works) > cost_of_sharing / gain_if_works. Below this probability, "
                "not forwarding is rational. Above it, forwarding dominates. For context, the odds of "
                "being struck by lightning are ~1 in 1.2 million.",
    display_name="Sharing Breakeven Probability",
    unit="probability",
    formula="SHARING_OPPORTUNITY_COST / TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA",
    inputs=["SHARING_OPPORTUNITY_COST", "TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"],
    compute=lambda ctx: ctx["SHARING_OPPORTUNITY_COST"] / ctx["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"],
    latex_symbol=r"P_{breakeven}",
)

SHARING_BREAKEVEN_ONE_IN_TREATY = Parameter(
    float(TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA) / float(SHARING_OPPORTUNITY_COST),
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Breakeven probability expressed as '1 in N'. Forwarding has positive expected value "
                "if you believe there is at least a 1-in-N chance the plan works. "
                "For context, lightning strike odds are ~1 in 1.2 million.",
    display_name="Sharing Breakeven (1 in N)",
    unit="ratio",
    formula="1 / SHARING_BREAKEVEN_PROBABILITY_TREATY",
    inputs=["SHARING_BREAKEVEN_PROBABILITY_TREATY"],
    compute=lambda ctx: 1 / ctx["SHARING_BREAKEVEN_PROBABILITY_TREATY"],
    latex_symbol=r"N_{breakeven}",
)

# ---
# IMPROVED PERSONAL LIFETIME WEALTH MODEL
# ---
# This section implements improvements identified in methodology review

# Constants for improved healthcare savings model
US_CHRONIC_DISEASE_SPENDING_ANNUAL = Parameter(
    4.1e12,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref="us-chronic-disease-spending",
    source_type="external",
    description="US annual chronic disease spending",
    display_name="US Annual Chronic Disease Spending",
    unit="USD/year",
    keywords=["4.1t", "yearly", "costs", "funding", "illness", "investment", "chronic"],
    distribution="lognormal",
    confidence_interval=(3.3e12, 5.0e12),  # ±20% - healthcare spending estimates vary
    latex_symbol=r"Spending_{chronic,US}",  # LaTeX symbol for equations
)  # $4.1T/year CDC estimate

US_POPULATION_2024 = Parameter(
    335e6, source_ref=ReferenceID.US_VOTER_POPULATION, source_type="external", description="US population in 2024", unit="people",
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    display_name="US Population in 2024",
    keywords=["2024", "335.0m", "people", "citizens", "individuals", "inhabitants", "persons"],
    distribution="lognormal",
    confidence_interval=(330e6, 340e6),  # ±1.5% - census estimates well-known
    latex_symbol=r"Pop_{US}",  # LaTeX symbol for equations
)

US_VOTE_DECISIVE_PROBABILITY = Parameter(
    1 / 60_000_000,
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    source_ref=ReferenceID.ODDS_OF_DECISIVE_VOTE,
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Probability of a single vote being decisive in a US presidential election. "
                "Gelman, Silver, and Edlin (2012) estimate roughly 1 in 60 million on average, "
                "varying by state from 1 in 10 million (swing states) to 1 in 1 billion (safe states).",
    display_name="Probability of Decisive Vote (US)",
    unit="probability",
    keywords=["vote", "decisive", "probability", "election", "presidential", "1 in 60 million"],
    latex_symbol=r"P_{decisive}",
)

US_FEDERAL_SPENDING_PER_CAPITA = Parameter(
    US_FEDERAL_SPENDING_2024 / US_POPULATION_2024,
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    source_type="calculated",
    confidence="high",
    description="US federal spending per capita. $6.8T total federal spending divided by 335M population.",
    display_name="US Federal Spending per Capita",
    unit="USD/person",
    formula="US_FEDERAL_SPENDING_2024 / US_POPULATION_2024",
    inputs=["US_FEDERAL_SPENDING_2024", "US_POPULATION_2024"],
    compute=lambda ctx: ctx["US_FEDERAL_SPENDING_2024"] / ctx["US_POPULATION_2024"],
    keywords=["federal", "spending", "per capita", "per person", "government"],
    latex_symbol=r"Spend_{fed,pc}",
)

US_VOTE_EXPECTED_VALUE = Parameter(
    US_VOTE_DECISIVE_PROBABILITY * US_FEDERAL_SPENDING_PER_CAPITA,
    manual_ref="knowledge/problem/unrepresentative-democracy.qmd",
    source_type="calculated",
    confidence="high",
    description="Expected monetary value of a single vote in a US presidential election. "
                "Calculated as the probability of being decisive (1 in 60M) times federal "
                "spending per capita (~$20,300). Represents the expected influence over "
                "government resource allocation from casting one vote.",
    display_name="Expected Value of a Vote (US)",
    unit="USD",
    formula="US_VOTE_DECISIVE_PROBABILITY x US_FEDERAL_SPENDING_PER_CAPITA",
    inputs=["US_VOTE_DECISIVE_PROBABILITY", "US_FEDERAL_SPENDING_PER_CAPITA"],
    compute=lambda ctx: ctx["US_VOTE_DECISIVE_PROBABILITY"] * ctx["US_FEDERAL_SPENDING_PER_CAPITA"],
    keywords=["vote", "expected value", "worth", "cost", "democracy", "influence"],
    latex_symbol=r"EV_{vote}",
)

PER_CAPITA_CHRONIC_DISEASE_COST = Parameter(
    US_CHRONIC_DISEASE_SPENDING_ANNUAL / US_POPULATION_2024,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_type="calculated",
    description="US per capita chronic disease cost",
    display_name="US Per Capita Chronic Disease Cost",
    unit="USD/person/year",
    formula="US_CHRONIC_DISEASE_SPENDING ÷ US_POPULATION",
    keywords=["chronic", "disease", "per capita", "us", "cost", "annual"],
    inputs=['US_CHRONIC_DISEASE_SPENDING_ANNUAL', 'US_POPULATION_2024'],
    compute=lambda ctx: ctx["US_CHRONIC_DISEASE_SPENDING_ANNUAL"] / ctx["US_POPULATION_2024"],
    latex_symbol=r"Cost_{chronic,pc}",  # LaTeX symbol for equations
)  # $12,239/year

# Mental health constants
US_MENTAL_HEALTH_COST_ANNUAL = Parameter(
    350e9,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref=ReferenceID.MENTAL_HEALTH_BURDEN,
    source_type="external",
    description="US mental health costs (treatment + productivity loss)",
    display_name="US Mental Health Costs",
    unit="USD/year",
    keywords=["350.0b", "yearly", "costs", "funding", "investment", "mental", "health"],
    distribution="lognormal",  # Economic cost estimates with methodological variance
    confidence_interval=(260e9, 450e9),  # ±25%: reflects treatment vs productivity cost allocation uncertainty
    latex_symbol=r"Cost_{mental,US}",  # LaTeX symbol for equations
)

PER_CAPITA_MENTAL_HEALTH_COST = Parameter(
    US_MENTAL_HEALTH_COST_ANNUAL / US_POPULATION_2024,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_type="calculated",
    description="US per capita mental health cost",
    display_name="US Per Capita Mental Health Cost",
    unit="USD/person/year",
    formula="US_MENTAL_HEALTH_COST ÷ US_POPULATION",
    keywords=["mental", "health", "per capita", "us", "cost", "annual"],
    inputs=['US_MENTAL_HEALTH_COST_ANNUAL', 'US_POPULATION_2024'],
    compute=lambda ctx: ctx["US_MENTAL_HEALTH_COST_ANNUAL"] / ctx["US_POPULATION_2024"],
    latex_symbol=r"Cost_{mental,pc}",  # LaTeX symbol for equations
)  # ~$1,045/year

MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA = Parameter(
    2000,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref=ReferenceID.MENTAL_HEALTH_BURDEN,
    source_type="external",
    description="Annual productivity loss per capita from mental health issues (beyond treatment costs)",
    display_name="Annual Productivity Loss per Capita from Mental Health Issues",
    unit="USD/year",
    keywords=["2k", "average person", "individual", "per person", "yearly", "household benefit", "per individual"],
    latex_symbol=r"Loss_{mental,pc}",  # LaTeX symbol for equations
)  # Additional productivity loss beyond treatment

# Caregiver time constants (simple model - deprecated, use detailed model below)
CAREGIVER_HOURS_PER_MONTH = Parameter(
    20,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref=ReferenceID.UNPAID_CAREGIVER_HOURS_ECONOMIC_VALUE,
    source_type="external",
    description="Average monthly hours of unpaid family caregiving in US",
    display_name="Average Monthly Hours of Unpaid Family Caregiving in US",
    unit="hours/month",
    keywords=["caregiver", "hours", "month"],
    latex_symbol=r"Hours_{care}",  # LaTeX symbol for equations
)  # Average US family provides 20 hrs/month unpaid care

CAREGIVER_VALUE_PER_HOUR_SIMPLE = Parameter(
    25,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref=ReferenceID.UNPAID_CAREGIVER_HOURS_ECONOMIC_VALUE,
    source_type="external",
    description="Estimated replacement cost per hour of caregiving",
    display_name="Estimated Replacement Cost per Hour of Caregiving",
    unit="USD/hour",
    keywords=["caregiver", "hour", "simple", "expenditure", "spending", "value", "budget"],
    latex_symbol=r"Value_{care,hr}",  # LaTeX symbol for equations
)  # Replacement cost estimate
CAREGIVER_COST_ANNUAL = Parameter(
    CAREGIVER_HOURS_PER_MONTH * MONTHS_PER_YEAR * CAREGIVER_VALUE_PER_HOUR_SIMPLE,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="definition",
    description="Annual cost of unpaid caregiving (replacement cost method)",
    display_name="Annual Cost of Unpaid Caregiving",
    unit="USD/year",
    formula="HOURS_PER_MONTH × MONTHS_PER_YEAR × VALUE_PER_HOUR",
    keywords=["caregiver", "unpaid", "annual", "expenditure", "spending", "value", "budget"],
    latex_symbol=r"Cost_{care,ann}",  # LaTeX symbol for equations
)  # $6,000/year


WORKFORCE_WITH_PRODUCTIVITY_LOSS = Parameter(
    0.28,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref="chronic-illness-workforce-productivity-loss",
    source_type="external",
    description="Percentage of workforce experiencing productivity loss from chronic illness (28%)",
    display_name="Percentage of Workforce Experiencing Productivity Loss from Chronic Illness",
    unit="rate",
    keywords=["workforce", "with", "productivity", "loss", "28%"],
    latex_symbol=r"N_{productivity,loss}",  # LaTeX symbol for equations
)  # 28% of all employees have productivity loss

CAREGIVER_ANNUAL_VALUE_TOTAL = Parameter(
    600e9,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="Total annual value of unpaid caregiving in US",
    display_name="Total Annual Value of Unpaid Caregiving in US",
    unit="USD/year",
    keywords=["600.0b", "yearly", "caregiver", "per year", "per annum", "pa", "annual"],
    latex_symbol=r"Value_{care,ann}",  # LaTeX symbol for equations
)  # $600B total

CAREGIVER_COUNT_US = Parameter(
    38e6,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="Number of unpaid caregivers in US",
    display_name="Number of Unpaid Caregivers in US",
    unit="people",
    keywords=["caregiver", "count", "38.0m"],
    latex_symbol=r"N_{care,US}",  # LaTeX symbol for equations
)  # 38 million caregivers
# Per caregiver: $600B / 38M = $15,789/year average
# But only portion is disease-related (vs aging, disability, children)
# Estimate: 40% of caregiving is for treatable disease conditions
DISEASE_RELATED_CAREGIVER_PCT = Parameter(
    0.40,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_ref="disease-related-caregiving-estimate",
    source_type="definition",
    description="Percentage of caregiving for treatable disease conditions (vs aging, disability, children)",
    display_name="Percentage of Caregiving for Treatable Disease Conditions",
    unit="rate",
    keywords=["40%", "illness", "disease", "related", "caregiver", "pct", "ailment"],
    latex_symbol=r"Pct_{care,disease}",  # LaTeX symbol for equations
)


def calculate_life_expectancy_gain_conservative_baseline(treaty_pct: float, conservative: bool = True) -> float:
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
    multiplier = calculate_trial_capacity_multiplier(treaty_pct)

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


def calculate_productivity_loss_conservative_baseline(treaty_pct: float, annual_income: float) -> float:
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
    multiplier = calculate_trial_capacity_multiplier(treaty_pct)

    # Base productivity loss for those affected: 22.6%
    BASELINE_PRODUCTIVITY_LOSS_AFFECTED = 0.226

    # Only 60% is from treatable conditions (rest is behavioral, aging, etc.)
    TREATABLE_PORTION = 0.60

    # Research impact: 115x research → recover 50% of treatable portion
    recovery_rate = min(0.70, multiplier / 165)  # 115x → 69.7% recovery

    # Expected value across population:
    # 28% of people affected × 22.6% loss × 60% treatable × 70% recovery
    net_gain_pct = (
        WORKFORCE_WITH_PRODUCTIVITY_LOSS * BASELINE_PRODUCTIVITY_LOSS_AFFECTED * TREATABLE_PORTION * recovery_rate
    )
    # = 0.28 × 0.226 × 0.60 × 0.697 = 2.65% population-wide gain

    return annual_income * net_gain_pct


def calculate_caregiver_savings_conservative_baseline(treaty_pct: float) -> float:
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
    multiplier = calculate_trial_capacity_multiplier(treaty_pct)

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
    treaty_pct: float = TREATY_REDUCTION_PCT,
    current_age: int = 30,
    baseline_life_expectancy: int = 80,
    annual_income: float = 50000,
    discount_rate: float = 0.03,
    conservative: bool = True,
    life_extension_override: float | None = None,
) -> dict[str, Any]:
    """
    Personal lifetime wealth calculation with configurable life extension

    Key components:
    1. Productivity loss: Based on IBI 2024 data (28% affected, $4,798 loss)
    2. Caregiver savings: Based on AARP data, only disease-related portion (40%)
    3. Life expectancy: Configurable via life_extension_override or model-based
    4. All parameters properly cited in ../references.qmd
    5. Mental health folded into productivity (no double-counting)
    6. Healthcare savings based on disease categories (not arbitrary divisor)

    Args:
        treaty_pct: Fraction of military spending redirected (default: 1%)
        current_age: Current age
        baseline_life_expectancy: Life expectancy without treaty (default: 80)
        annual_income: Annual income
        discount_rate: Discount rate for NPV (default: 3%)
        conservative: Use conservative estimates if True (only used if life_extension_override is None)
        life_extension_override: Direct life extension years (bypasses model calculation)

    Returns:
        Dictionary with total benefit and component breakdown
    """
    # Calculate life extension - use override if provided, otherwise use model
    if life_extension_override is not None:
        life_extension_years = life_extension_override
    else:
        life_extension_years = calculate_life_expectancy_gain_conservative_baseline(treaty_pct, conservative)
    years_remaining = baseline_life_expectancy - current_age
    total_years = years_remaining + life_extension_years

    # Medical progress multiplier
    progress_multiplier = calculate_trial_capacity_multiplier(treaty_pct)

    # GDP boost
    gdp_boost = calculate_gdp_growth_boost(treaty_pct)

    # Component 1: Peace dividend
    peace_dividend_per_capita_annual = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / GLOBAL_POPULATION_2024

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
        0.30 * 0.20 * research_effectiveness  # Treatable
        + 0.50 * 0.10 * research_effectiveness  # Manageable
        + 0.20 * 0.02 * research_effectiveness  # Incurable
    )  # = 7.9% total reduction for 115x

    healthcare_savings_annual = US_CHRONIC_COST_PER_CAPITA * weighted_reduction

    # Component 3: Productivity gains (conservative baseline, includes mental health)
    productivity_gains_annual = calculate_productivity_loss_conservative_baseline(treaty_pct, annual_income)

    # Component 4: Caregiver savings (conservative baseline, disease-portion only)
    caregiver_savings_annual = calculate_caregiver_savings_conservative_baseline(treaty_pct)

    # Component 5: Income growth from GDP boost
    # FIXED: Only calculate boost for years_remaining to avoid double-counting extended years
    # (Extended years are fully captured in the extended_earnings component)
    base_growth = 0.025
    income_with_gdp_boost = compound_sum(annual_income, years_remaining, gdp_boost, discount_rate)
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
        "total_lifetime_benefit": total_benefit,
        "annual_breakdown": {
            "peace_dividend": peace_dividend_per_capita_annual,
            "healthcare_savings": healthcare_savings_annual,
            "productivity_gains": productivity_gains_annual,
            "caregiver_savings": caregiver_savings_annual,
        },
        "npv_breakdown": {
            "peace_dividend_total": peace_dividend_total,
            "healthcare_savings_total": healthcare_savings_total,
            "productivity_gains_total": productivity_gains_total,
            "caregiver_savings_total": caregiver_savings_total,
            "gdp_boost_benefit": gdp_boost_benefit,
            "extended_earnings": extended_earnings,
        },
        "life_extension_years": life_extension_years,
        "new_life_expectancy": baseline_life_expectancy + life_extension_years,
        "gdp_growth_boost": gdp_boost - 0.025,
        "medical_progress_multiplier": progress_multiplier,
        "model_type": "conservative_baseline",
    }


# Personal lifetime wealth using simple QALY-based formula
# Life extension years valued at standard economic QALY rate
# Simple, traceable, academically standard approach
# With 20 years (median) × $150K/QALY = $3M
# Range via Monte Carlo: $750K (5yr) to $15M (100yr)
PERSONAL_LIFETIME_WEALTH = Parameter(
    float(LIFE_EXTENSION_YEARS) * float(STANDARD_ECONOMIC_QALY_VALUE_USD),
    manual_ref="knowledge/call-to-action/your-personal-benefits.qmd",
    source_type="calculated",
    description="Personal lifetime wealth from life extension valued at standard QALY rate. Simple formula: years of life gained × economic value per healthy year. Uncertainty in LIFE_EXTENSION_YEARS (5-100 year range, median 20) propagates through Monte Carlo.",
    display_name="Personal Lifetime Wealth (QALY-Based)",
    unit="USD",
    formula="LIFE_EXTENSION_YEARS × STANDARD_ECONOMIC_QALY_VALUE_USD",
    confidence="low",
    keywords=["personal", "lifetime", "wealth", "individual benefit", "qaly", "life extension", "economic value"],
    inputs=["LIFE_EXTENSION_YEARS", "STANDARD_ECONOMIC_QALY_VALUE_USD"],
    compute=lambda ctx: ctx["LIFE_EXTENSION_YEARS"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Wealth_{lifetime}",
)


# ==============================================================================
# INCENTIVE ALIGNMENT PARAMETERS
# ==============================================================================
# Parameters showing how different stakeholders benefit from your DIH/dFDA system
# Source: knowledge/solution/aligning-incentives.qmd

# ---
# PHARMACEUTICAL ECONOMICS
# ---
# Current pharma business model vs. DIH/dFDA payment reversal

PHARMA_DRUG_DEVELOPMENT_COST_CURRENT = Parameter(
    2_600_000_000,
    manual_ref="knowledge/problem/fda-is-unsafe-and-ineffective.qmd",
    source_ref=ReferenceID.DRUG_DEVELOPMENT_COST,
    source_type="external",
    description="Average cost to develop one drug in current system",
    display_name="Pharma Drug Development Cost (Current System)",
    unit="USD",
    confidence="high",
    peer_reviewed=True,
    distribution=DistributionType.LOGNORMAL,
    std_error=500_000_000,
    confidence_interval=(1_500_000_000, 4_000_000_000),
    keywords=["pharma", "drug", "development", "cost", "r&d", "current"],
    latex_symbol=r"Cost_{dev,curr}",  # LaTeX symbol for equations
)

DRUG_DEVELOPMENT_COST_1980S = Parameter(
    194_000_000,
    manual_ref="knowledge/economics/1-pct-treaty-impact.qmd",
    source_ref=ReferenceID.PRE_1962_DRUG_COSTS_TIMELINE,
    source_type="external",
    description="Drug development cost in 1980s (compounded to approval, 1990 dollars)",
    display_name="Drug Development Cost (1980s)",
    unit="USD",
    confidence="high",
    keywords=["pharma", "drug", "development", "cost", "1980s", "historical"],
    distribution="lognormal",  # Source indicates approximation (~$194M); lognormal appropriate for cost data
    confidence_interval=(145_500_000, 242_500_000),  # ±25% for measurement uncertainty (source uses "~" indicating approximation)
    latex_symbol=r"Cost_{dev,80s}",  # LaTeX symbol for equations
)

DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER = Parameter(
    PHARMA_DRUG_DEVELOPMENT_COST_CURRENT / DRUG_DEVELOPMENT_COST_1980S,
    manual_ref="knowledge/appendix/invisible-graveyard.qmd",
    source_ref=ReferenceID.PRE_1962_DRUG_COSTS_TIMELINE,
    source_type="calculated",
    description="Drug development cost increase from 1980s to current",
    display_name="Drug Cost Increase: 1980s to Current",
    unit="x",
    formula="PHARMA_DRUG_DEVELOPMENT_COST_CURRENT ÷ DRUG_DEVELOPMENT_COST_1980S",
    confidence="high",
    keywords=["cost", "increase", "multiplier", "drug", "development", "1980s", "current"],
    inputs=['DRUG_DEVELOPMENT_COST_1980S', 'PHARMA_DRUG_DEVELOPMENT_COST_CURRENT'],
    compute=lambda ctx: ctx["PHARMA_DRUG_DEVELOPMENT_COST_CURRENT"] / ctx["DRUG_DEVELOPMENT_COST_1980S"],
    latex_symbol=r"k_{cost,80s}",  # LaTeX symbol for equations
)

DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER = Parameter(
    PHARMA_DRUG_DEVELOPMENT_COST_CURRENT / PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD,
    manual_ref="knowledge/appendix/drug-development-cost-analysis.qmd",
    source_ref=ReferenceID.PRE_1962_DRUG_COSTS_BAILY_1972,
    source_type="calculated",
    description="Drug development cost increase from pre-1962 to current",
    display_name="Drug Cost Increase: Pre-1962 to Current",
    unit="x",
    formula="PHARMA_DRUG_DEVELOPMENT_COST_CURRENT ÷ PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD",
    confidence="high",
    keywords=["cost", "increase", "multiplier", "drug", "development", "1962", "regulation", "fda", "pre-1962", "current", "baily"],
    inputs=['PHARMA_DRUG_DEVELOPMENT_COST_CURRENT', 'PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD'],
    compute=lambda ctx: ctx["PHARMA_DRUG_DEVELOPMENT_COST_CURRENT"] / ctx["PRE_1962_DRUG_DEVELOPMENT_COST_2024_USD"],
    latex_symbol=r"k_{cost,pre62}",  # LaTeX symbol for equations
)  # Baily (1972): $6.5M (1980 dollars) = $24.7M (2024 dollars, CPI-adjusted 3.80×) → $2.6B = 105× increase

PHARMA_SUCCESS_RATE_CURRENT_PCT = Parameter(
    0.10,
    manual_ref="knowledge/problem/fda-is-unsafe-and-ineffective.qmd",
    source_ref=ReferenceID.DRUG_TRIAL_SUCCESS_RATE_12_PCT,
    source_type="external",
    description="Percentage of drugs that reach market in current system",
    display_name="Pharma Drug Success Rate (Current System)",
    unit="percentage",
    confidence="high",
    peer_reviewed=True,
    keywords=["pharma", "drug", "success", "rate", "approval", "current"],
    latex_symbol=r"Rate_{success,curr}",  # LaTeX symbol for equations
)

PHARMA_DRUG_REVENUE_AVERAGE_CURRENT = Parameter(
    6_700_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref="pharma-drug-revenue-average",
    source_type="external",
    description="Median lifetime revenue per successful drug (study of 361 FDA-approved drugs 1995-2014, median follow-up 13.2 years)",
    display_name="Pharma Average Drug Revenue (Current System)",
    unit="USD",
    confidence="high",
    peer_reviewed=True,
    keywords=["pharma", "drug", "revenue", "lifetime", "current"],
    latex_symbol=r"Revenue_{drug,avg}",  # LaTeX symbol for equations
)

PHARMA_ROI_CURRENT_SYSTEM_PCT = Parameter(
    0.012,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref="pharma-roi-current",
    source_type="external",
    description="ROI for pharma R&D (2022 historic low from Deloitte study of top 20 pharma companies, down from 6.8% in 2021, recovered to 5.9% in 2024)",
    display_name="Pharma ROI (Current System)",
    unit="percentage",
    confidence="high",
    peer_reviewed=True,
    keywords=["pharma", "roi", "current", "system", "barely profitable", "low returns"],
    latex_symbol=r"ROI_{pharma,curr}",  # LaTeX symbol for equations
)

# NOTE: DIH system doesn't magically increase drug efficacy success rates
# What changes: trials are MUCH cheaper (eliminate $48k/participant cost), faster trials,
# more attempts possible, rare diseases become viable
# What doesn't change: underlying biology of whether drugs work
# Main benefit: Cost elimination ($48k → ~$0 per participant) + some unknown profit margin

# ---
# DISEASE ANNUAL COSTS (FOR INSURANCE ECONOMICS)
# ---
# Annual US costs for major diseases, showing insurance company savings potential

US_DIABETES_ANNUAL_COST = Parameter(
    327_000_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref=ReferenceID.DISEASE_COST_DIABETES_1500B,
    source_type="external",
    description="Annual US cost of diabetes (direct and indirect)",
    display_name="US Diabetes Annual Cost",
    unit="USD",
    confidence="high",
    confidence_interval=(278_000_000_000, 376_000_000_000),  # ±15% on disease cost estimates
    distribution="lognormal",
    peer_reviewed=True,
    keywords=["insurance", "diabetes", "cost", "annual", "us", "disease", "burden"],
    latex_symbol=r"Cost_{diabetes,US}",  # LaTeX symbol for equations
)

US_ALZHEIMERS_ANNUAL_COST = Parameter(
    355_000_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref=ReferenceID.DISEASE_COST_ALZHEIMERS_1300B,
    source_type="external",
    description="Annual US cost of Alzheimer's disease (direct and indirect)",
    display_name="US Alzheimer's Annual Cost",
    unit="USD",
    confidence="high",
    confidence_interval=(302_000_000_000, 408_000_000_000),  # ±15% on disease cost estimates
    distribution="lognormal",
    peer_reviewed=True,
    keywords=["insurance", "alzheimer", "dementia", "cost", "annual", "us", "disease", "burden"],
    latex_symbol=r"Cost_{ALZ,US}",  # LaTeX symbol for equations
)

US_HEART_DISEASE_ANNUAL_COST = Parameter(
    363_000_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref=ReferenceID.DISEASE_COST_HEART_DISEASE_2100B,
    source_type="external",
    description="Annual US cost of heart disease and stroke (direct and indirect)",
    display_name="US Heart Disease Annual Cost",
    unit="USD",
    confidence="high",
    confidence_interval=(309_000_000_000, 417_000_000_000),  # ±15% on disease cost estimates
    distribution="lognormal",
    peer_reviewed=True,
    keywords=["insurance", "heart", "cardiovascular", "stroke", "cost", "annual", "us", "disease", "burden"],
    latex_symbol=r"Cost_{heart,US}",  # LaTeX symbol for equations
)

US_CANCER_ANNUAL_COST = Parameter(
    208_000_000_000,
    manual_ref="knowledge/solution/aligning-incentives.qmd",
    source_ref=ReferenceID.DISEASE_COST_CANCER_1800B,
    source_type="external",
    description="Annual US cost of cancer (direct and indirect)",
    display_name="US Cancer Annual Cost",
    unit="USD",
    confidence="high",
    confidence_interval=(177_000_000_000, 239_000_000_000),  # ±15% on disease cost estimates
    distribution="lognormal",
    peer_reviewed=True,
    keywords=["insurance", "cancer", "oncology", "cost", "annual", "us", "disease", "burden"],
    latex_symbol=r"Cost_{cancer,US}",  # LaTeX symbol for equations
)

US_MAJOR_DISEASES_TOTAL_ANNUAL_COST = Parameter(
    US_DIABETES_ANNUAL_COST + US_ALZHEIMERS_ANNUAL_COST + US_HEART_DISEASE_ANNUAL_COST + US_CANCER_ANNUAL_COST,
    manual_ref="knowledge/problem/cost-of-disease.qmd",
    source_type="calculated",
    description="Total annual US cost of major diseases (diabetes, Alzheimer's, heart disease, cancer)",
    display_name="US Major Diseases Total Annual Cost",
    unit="USD",
    formula="DIABETES + ALZHEIMERS + HEART + CANCER",
    confidence="high",
    keywords=["insurance", "disease", "cost", "annual", "us", "total", "burden"],
    inputs=['US_ALZHEIMERS_ANNUAL_COST', 'US_CANCER_ANNUAL_COST', 'US_DIABETES_ANNUAL_COST', 'US_HEART_DISEASE_ANNUAL_COST'],
    compute=lambda ctx: ctx["US_DIABETES_ANNUAL_COST"] + ctx["US_ALZHEIMERS_ANNUAL_COST"] + ctx["US_HEART_DISEASE_ANNUAL_COST"] + ctx["US_CANCER_ANNUAL_COST"],
    latex_symbol=r"Cost_{disease,US}",  # LaTeX symbol for equations
)

# ---
# IAB PAPER PARAMETERS
# ---
# NOTE: GLOBAL_HOUSEHOLD_WEALTH_USD is defined earlier to avoid forward-reference issues in downstream calculations

CONCENTRATED_INTEREST_SECTOR_MARKET_CAP_USD = Parameter(
    5e12,
    manual_ref="knowledge/appendix/incentive-alignment-bonds-paper.qmd",
    source_ref="",
    source_type="definition",
    description="Estimated combined market capitalization of concentrated interest opposition (defense, fossil fuel, etc.)",
    display_name="Concentrated Interest Sector Market Cap",
    unit="USD",
    keywords=["wealth", "opposition", "lobbying", "defense", "fossil fuel", "market cap"],
    latex_symbol=r"MarketCap_{defense}",  # LaTeX symbol for equations
)  # $5T

IAB_MECHANISM_ANNUAL_COST = Parameter(
    750_000_000,
    manual_ref="knowledge/appendix/incentive-alignment-bonds-paper.qmd",
    source_ref="https://iab.warondisease.org#welfare-analysis",
    source_type="definition",
    description="Estimated annual cost of the IAB mechanism (high-end estimate including regulatory defense)",
    display_name="IAB Mechanism Annual Cost (High Estimate)",
    unit="USD/year",
    confidence_interval=(160_000_000, 750_000_000),
    keywords=["iab", "cost", "overhead", "annual"],
    latex_symbol=r"Cost_{IAB,ann}",  # LaTeX symbol for equations
)  # $750M high end estimate

IAB_MECHANISM_BENEFIT_COST_RATIO = Parameter(
    TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS / IAB_MECHANISM_ANNUAL_COST,
    manual_ref="knowledge/appendix/incentive-alignment-bonds-paper.qmd",
    source_ref="https://iab.warondisease.org##welfare-analysis",
    source_type="calculated",
    description="Benefit-Cost Ratio of the IAB mechanism itself",
    display_name="IAB Mechanism Benefit-Cost Ratio",
    unit="ratio",
    formula="TREATY_PEACE_PLUS_RD_BENEFITS ÷ IAB_MECHANISM_COST",
    keywords=["bcr", "benefit cost ratio", "iab", "mechanism"],
    inputs=["TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS", "IAB_MECHANISM_ANNUAL_COST"],
    compute=lambda ctx: ctx["TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS"] / ctx["IAB_MECHANISM_ANNUAL_COST"],
    latex_symbol=r"BCR_{IAB}",  # LaTeX symbol for equations
)  # 303:1

# ============================================================================
# CHAIN REACTION MODEL: PROBABILITY OF REACHING AN IMPLEMENTER
# ============================================================================
# Models two channels of exposure over 10 years:
# 1. Direct encounters: Implementers find the idea through media, conferences, advisors
# 2. Chain reaction: Social network sharing amplifies initial audience
#
# This is a PRECURSOR to POLITICAL_SUCCESS_PROBABILITY:
#   P(success) = P(reaches implementer) x P(political success | implementer acts)
# If P(reaches) = 25%, the existing 1% implies only 4% conditional political success.
#
# Deliberately conservative: base engagement rate, narrow implementer definition, no compounding.

# --- Foundation parameters ---

CHAIN_GLOBAL_BILLIONAIRE_COUNT = Parameter(
    2_781,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_ref="forbes-billionaires-2024",
    source_type="external",
    description="Number of billionaires globally (Forbes 2024 count)",
    display_name="Global Billionaire Count",
    unit="people",
    confidence="high",
    distribution="fixed",
    peer_reviewed=False,
    keywords=["billionaire", "wealth", "forbes", "chain", "implementer"],
    latex_symbol=r"N_{billionaire}",
)

CHAIN_WORLD_LEADER_COUNT = Parameter(
    195,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_ref="",
    source_type="definition",
    description="Number of sovereign heads of state/government",
    display_name="World Leader Count",
    unit="countries",
    distribution="fixed",
    keywords=["leader", "head of state", "sovereign", "chain", "implementer"],
    latex_symbol=r"N_{leader}",
)

CHAIN_IMPLEMENTER_COUNT = Parameter(
    float(CHAIN_GLOBAL_BILLIONAIRE_COUNT) + float(CHAIN_WORLD_LEADER_COUNT),
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Total potential implementers (billionaires + world leaders)",
    display_name="Potential Implementers",
    unit="people",
    formula="CHAIN_GLOBAL_BILLIONAIRE_COUNT + CHAIN_WORLD_LEADER_COUNT",
    keywords=["implementer", "chain", "billionaire", "leader"],
    inputs=["CHAIN_GLOBAL_BILLIONAIRE_COUNT", "CHAIN_WORLD_LEADER_COUNT"],
    compute=lambda ctx: ctx["CHAIN_GLOBAL_BILLIONAIRE_COUNT"] + ctx["CHAIN_WORLD_LEADER_COUNT"],
    latex_symbol=r"N_{impl}",
)

CHAIN_INITIAL_AUDIENCE = Parameter(
    50_000,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="definition",
    description="Conservative initial audience size (readers, website visitors, conference attendees)",
    display_name="Initial Audience",
    unit="people",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(10_000, 500_000),
    conservative=True,
    keywords=["audience", "initial", "chain", "diffusion"],
    latex_symbol=r"N_0",
)

CHAIN_DISMISS_PROBABILITY = Parameter(
    0.90,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="definition",
    description="Probability someone dismisses the idea without engaging (the 'institutionalization rate')",
    display_name="Dismissal Rate",
    unit="rate",
    confidence="medium",
    distribution="beta",
    confidence_interval=(0.80, 0.97),
    conservative=True,
    keywords=["dismiss", "ignore", "chain", "engagement", "institutionalization"],
    latex_symbol=r"P_{dismiss}",
)

CHAIN_ENGAGE_PROBABILITY = Parameter(
    1.0 - float(CHAIN_DISMISS_PROBABILITY),
    manual_ref="knowledge/appendix/recruitment-and-propaganda-plan.qmd",
    source_type="calculated",
    description="Probability someone engages with the idea (1 - dismissal rate)",
    display_name="Engagement Rate",
    unit="rate",
    formula="1 - CHAIN_DISMISS_PROBABILITY",
    keywords=["engage", "chain", "diffusion"],
    inputs=["CHAIN_DISMISS_PROBABILITY"],
    compute=lambda ctx: 1.0 - ctx["CHAIN_DISMISS_PROBABILITY"],
    latex_symbol=r"P_{engage}",
)

CHAIN_HORIZON_YEARS = Parameter(
    3,
    manual_ref="knowledge/strategy/earth-optimization-protocol-v1.qmd",
    source_type="definition",
    description="Conservative upper bound for cascade propagation (social media cascades propagate in weeks; 3 years allows for slower channels and multiple cascade waves)",
    display_name="Model Horizon",
    unit="years",
    distribution="fixed",
    keywords=["horizon", "time", "chain", "years"],
    latex_symbol=r"T",
)

# --- Network propagation model (empirically grounded) ---
# Replaces flat annual encounter rate with orbit-overlap model.
#
# Key insight: you don't need to reach a billionaire directly.
# You need the content to reach anyone in their "information orbit"
# (staff, advisors, social media feeds, professional contacts).
# If ANY orbit member flags the content, the implementer encounters it.
#
# Model: P(implementer's orbit reached) = 1 - (1 - O/N)^R_total
#   O = orbit size per implementer (~1,000; Dunbar 1992 extended for info-age)
#   N = connected population (5B; hardcoded)
#   R_total = initial_audience x cascade_multiplier
#   cascade_multiplier = sum(R_eff^i) for i=0..3 (3 generations, hardcoded)
#
# Only 2 uncertain inputs; everything else is a constant or a calculation.

# Constants (not worth parameterizing: stable, well-known, low sensitivity)
_SOCIAL_NETWORK_POP = 5_000_000_000  # global connected population
_CASCADE_GENERATIONS = 3              # practical sharing depth

CHAIN_IMPLEMENTER_ORBIT_SIZE = Parameter(
    1_000,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="definition",
    description="Information-orbit size per implementer: people whose recommendation would reach them (staff, advisors, active social media feeds, professional contacts). Lower bound: Dunbar's 150; upper: corporate C-suite intake funnel.",
    display_name="Implementer Orbit Size",
    unit="people",
    confidence="medium",
    distribution="lognormal",
    confidence_interval=(150, 5_000),
    conservative=True,
    keywords=["orbit", "implementer", "dunbar", "network", "contacts", "chain"],
    latex_symbol=r"O_{impl}",
)

CHAIN_EFFECTIVE_R = Parameter(
    0.15,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="definition",
    description="Effective reproduction number per cascade generation: fraction of viewers who share (5%) x average forwards per sharer (3). CI spans pessimistic (2% x 2 = 0.04) to optimistic (10% x 8 = 0.80).",
    display_name="Effective R",
    unit="ratio",
    confidence="medium",
    distribution="lognormal",
    confidence_interval=(0.04, 0.80),
    keywords=["reproduction", "viral", "coefficient", "chain", "cascade", "sharing"],
    latex_symbol=r"R_{eff}",
)

# Shared input list for model outputs
_chain_orbit_inputs = [
    "CHAIN_IMPLEMENTER_ORBIT_SIZE", "CHAIN_EFFECTIVE_R", "CHAIN_INITIAL_AUDIENCE",
]

# --- Model outputs (variable names preserved for QMD compatibility) ---
# INFORMATION DIFFUSION ONLY. The dominant strategy proof handles "will they act?"

_R0 = float(CHAIN_EFFECTIVE_R)
_cascade_mult_0 = sum(_R0 ** i for i in range(_CASCADE_GENERATIONS + 1))
_total_reach_0 = float(CHAIN_INITIAL_AUDIENCE) * _cascade_mult_0
_p_orbit_0 = float(CHAIN_IMPLEMENTER_ORBIT_SIZE) / _SOCIAL_NETWORK_POP
_p_reach_0 = 1.0 - (1.0 - _p_orbit_0) ** _total_reach_0

CHAIN_P_ENCOUNTER_DIRECT_10YR = Parameter(
    _p_reach_0,
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Probability a given implementer's information orbit is reached by the content cascade",
    display_name="Implementer Orbit Reach Probability",
    unit="rate",
    formula="1 - (1 - CHAIN_IMPLEMENTER_ORBIT_SIZE / 5B)^(CHAIN_INITIAL_AUDIENCE x cascade_multiplier)",
    latex=r"P_{reach} = 1 - \left(1 - \frac{O_{impl}}{N}\right)^{N_0 \cdot \sum_{i=0}^{3} R_{eff}^i}",
    keywords=["encounter", "orbit", "reach", "chain", "implementer"],
    inputs=_chain_orbit_inputs,
    compute=lambda ctx: 1.0 - (
        1.0 - (ctx["CHAIN_IMPLEMENTER_ORBIT_SIZE"] / _SOCIAL_NETWORK_POP)
    ) ** (
        ctx["CHAIN_INITIAL_AUDIENCE"]
        * (
            1
            + ctx["CHAIN_EFFECTIVE_R"]
            + ctx["CHAIN_EFFECTIVE_R"] ** 2
            + ctx["CHAIN_EFFECTIVE_R"] ** 3
        )
    ),
    latex_symbol=r"P_{reach,impl}",
)

CHAIN_EXPECTED_ENGAGED_IMPLEMENTERS = Parameter(
    _p_reach_0 * float(CHAIN_ENGAGE_PROBABILITY) * float(CHAIN_IMPLEMENTER_COUNT),
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Expected number of implementers who engage (orbit reached x engagement rate x implementer count)",
    display_name="Expected Engaged Implementers",
    unit="people",
    formula="P_reach x CHAIN_ENGAGE_PROBABILITY x CHAIN_IMPLEMENTER_COUNT",
    latex=r"E[N_{engaged}] = P_{reach} \times P_{engage} \times N_{impl}",
    keywords=["engaged", "implementer", "expected", "chain"],
    inputs=_chain_orbit_inputs + ["CHAIN_ENGAGE_PROBABILITY", "CHAIN_IMPLEMENTER_COUNT"],
    compute=lambda ctx: (
        1.0
        - (
            1.0 - (ctx["CHAIN_IMPLEMENTER_ORBIT_SIZE"] / _SOCIAL_NETWORK_POP)
        ) ** (
            ctx["CHAIN_INITIAL_AUDIENCE"]
            * (
                1
                + ctx["CHAIN_EFFECTIVE_R"]
                + ctx["CHAIN_EFFECTIVE_R"] ** 2
                + ctx["CHAIN_EFFECTIVE_R"] ** 3
            )
        )
    ) * ctx["CHAIN_ENGAGE_PROBABILITY"] * ctx["CHAIN_IMPLEMENTER_COUNT"],
    latex_symbol=r"E[N_{engaged}]",
)

CHAIN_P_NO_IMPLEMENTER_ENGAGES = Parameter(
    (1.0 - _p_reach_0 * float(CHAIN_ENGAGE_PROBABILITY)) ** float(CHAIN_IMPLEMENTER_COUNT),
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Probability that NO implementer engages (all orbits missed or all dismiss)",
    display_name="P(No Implementer Engages)",
    unit="rate",
    formula="(1 - P_reach x CHAIN_ENGAGE_PROBABILITY)^CHAIN_IMPLEMENTER_COUNT",
    latex=r"P_{none} = \left(1 - P_{reach} \cdot P_{engage}\right)^{N_{impl}}",
    keywords=["no engagement", "probability", "chain", "implementer"],
    inputs=_chain_orbit_inputs + ["CHAIN_ENGAGE_PROBABILITY", "CHAIN_IMPLEMENTER_COUNT"],
    compute=lambda ctx: (
        1.0
        - (
            1.0
            - (
                1.0 - (ctx["CHAIN_IMPLEMENTER_ORBIT_SIZE"] / _SOCIAL_NETWORK_POP)
            ) ** (
                ctx["CHAIN_INITIAL_AUDIENCE"]
                * (
                    1
                    + ctx["CHAIN_EFFECTIVE_R"]
                    + ctx["CHAIN_EFFECTIVE_R"] ** 2
                    + ctx["CHAIN_EFFECTIVE_R"] ** 3
                )
            )
        ) * ctx["CHAIN_ENGAGE_PROBABILITY"]
    ) ** ctx["CHAIN_IMPLEMENTER_COUNT"],
    latex_symbol=r"P_{none}",
)

CHAIN_P_AT_LEAST_ONE_ENGAGES = Parameter(
    1.0 - float(CHAIN_P_NO_IMPLEMENTER_ENGAGES),
    manual_ref="knowledge/appendix/treaty-feasibility.qmd",
    source_type="calculated",
    description="Probability at least one implementer engages (information diffusion only; dominant strategy proof handles action)",
    display_name="P(At Least One Engages)",
    unit="percent",
    formula="1 - CHAIN_P_NO_IMPLEMENTER_ENGAGES",
    keywords=["probability", "chain", "implementer", "engagement", "headline"],
    inputs=["CHAIN_P_NO_IMPLEMENTER_ENGAGES"],
    compute=lambda ctx: 1.0 - ctx["CHAIN_P_NO_IMPLEMENTER_ENGAGES"],
    latex_symbol=r"P_{reach}",
)


# ── Individual Contribution Expected Value (per percentage point of probability shift) ──

CONTRIBUTION_EV_PER_PCT_POINT_TREATY = Parameter(
    float(TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA) * 0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Personal expected value per percentage point of implementation probability shift under Treaty Trajectory. "
                "One percent of the per-capita lifetime income gain.",
    display_name="Contribution EV per Percentage Point (Treaty)",
    unit="USD",
    formula="TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA × 0.01",
    inputs=["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"] * 0.01,
    latex_symbol=r"EV_{pp,treaty}",
)

CONTRIBUTION_EV_PER_PCT_POINT_WISHONIA = Parameter(
    float(WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA) * 0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Personal expected value per percentage point of implementation probability shift under Wishonia Trajectory. "
                "One percent of the per-capita lifetime income gain.",
    display_name="Contribution EV per Percentage Point (Wishonia)",
    unit="USD",
    formula="WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA × 0.01",
    inputs=["WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"],
    compute=lambda ctx: ctx["WISHONIA_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"] * 0.01,
    latex_symbol=r"EV_{pp,wish}",
)

CONTRIBUTION_EV_PER_PCT_POINT_TREATY_INCOME_PLUS_HEALTH = Parameter(
    float(TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH) * 0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Income-plus-health personal expected value per percentage point of implementation probability shift under Treaty Trajectory.",
    display_name="Contribution EV per Percentage Point (Treaty, Income + Health)",
    unit="USD",
    formula="TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH × 0.01",
    inputs=["TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH"],
    compute=lambda ctx: ctx["TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH"] * 0.01,
    latex_symbol=r"EV_{pp,treaty,income+health}",
)

CONTRIBUTION_EV_PER_PCT_POINT_WISHONIA_INCOME_PLUS_HEALTH = Parameter(
    float(WISHONIA_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH) * 0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Income-plus-health personal expected value per percentage point of implementation probability shift under Wishonia Trajectory.",
    display_name="Contribution EV per Percentage Point (Wishonia, Income + Health)",
    unit="USD",
    formula="WISHONIA_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH × 0.01",
    inputs=["WISHONIA_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH"],
    compute=lambda ctx: ctx["WISHONIA_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH"] * 0.01,
    latex_symbol=r"EV_{pp,wish,income+health}",
)

CONTRIBUTION_DALYS_PER_PCT_POINT = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS) * 0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="DALYs averted per percentage point of implementation probability shift. "
                "One percent of total DALYs from eliminating trial capacity bottleneck and efficacy lag.",
    display_name="DALYs Averted per Percentage Point",
    unit="DALYs",
    formula="TOTAL_TIMELINE_SHIFT_DALYS × 0.01",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"] * 0.01,
    latex_symbol=r"DALYs_{pp}",
)

CONTRIBUTION_LIVES_SAVED_PER_PCT_POINT = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED) * 0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Lives saved per percentage point of implementation probability shift. "
                "One percent of total lives saved from eliminating trial capacity bottleneck and efficacy lag.",
    display_name="Lives Saved per Percentage Point",
    unit="lives",
    formula="TOTAL_TIMELINE_SHIFT_LIVES_SAVED × 0.01",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED"] * 0.01,
    latex_symbol=r"Lives_{pp}",
)

CONTRIBUTION_SUFFERING_HOURS_PER_PCT_POINT = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS) * 0.01,
    manual_ref="knowledge/strategy/earth-optimization-prize.qmd",
    source_type="calculated",
    description="Suffering hours prevented per percentage point of implementation probability shift. "
                "One percent of total suffering hours from eliminating trial capacity bottleneck and efficacy lag.",
    display_name="Suffering Hours Prevented per Percentage Point",
    unit="hours",
    formula="TOTAL_TIMELINE_SHIFT_SUFFERING_HOURS × 0.01",
    inputs=["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS"],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS"] * 0.01,
    latex_symbol=r"Hours_{pp}",
)

# ============================================================================
# EARTH OPTIMIZATION SERVICES - DEFENSE TAKEOVER & FUND PARAMETERS
# ============================================================================

DEFENSE_PRIMES_MARKET_CAP_US = Parameter(
    836_000_000_000,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_ref=ReferenceID.STOCKANALYSIS_MILITARY_PRIME_CAPS_2026,
    source_type="external",
    description="Combined market capitalization of the 11 major US military primes at the June 2026 close: "
                "RTX $248.1B, Boeing $174.7B, Lockheed Martin $126.5B, General Dynamics $96.9B, "
                "Northrop Grumman $78.5B, L3Harris $58.2B, Leidos $15.4B, Huntington Ingalls $11.9B, "
                "CACI $11.6B, Booz Allen Hamilton $9.2B, SAIC $4.9B",
    display_name="US Military Primes Market Cap",
    unit="USD",
    keywords=["military contractor", "market cap", "US primes"],
    latex_symbol=r"MarketCap_{US}",
    distribution="fixed",
)

DEFENSE_PRIMES_MARKET_CAP_ALLIED = Parameter(
    132_000_000_000,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_ref=ReferenceID.COMPANIESMARKETCAP_EU_PRIMES_2026,
    source_type="external",
    description="Combined market capitalization of major allied European military primes "
                "(BAE Systems approx $75.8B + Thales approx $56.7B), as of June 2026",
    display_name="Allied Military Primes Market Cap",
    unit="USD",
    keywords=["military contractor", "market cap", "European primes", "BAE", "Thales"],
    latex_symbol=r"MarketCap_{allied}",
    distribution="fixed",
)

DEFENSE_TAKEOVER_CONTROL_FRACTION = Parameter(
    0.501,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="definition",
    description="Fraction of shares required for board control (50% + 1 share)",
    display_name="Control Fraction",
    unit="ratio",
    keywords=["control", "majority", "board"],
    latex_symbol=r"f_{control}",
    distribution="fixed",
)

INFLUENCE_ACTIVIST_STAKE_FRACTION = Parameter(
    0.05,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="definition",
    description="Activist equity stake assumed sufficient to win board influence when combined with index-fund votes, rather than buying outright control. Grounded in activist-investing precedent: Engine No. 1 won three ExxonMobil board seats with 0.02%, and Carl Icahn typically operates with 1-10% positions. 5% is a deliberately conservative central case; the real floor is far lower, because institutional investors hold 70-85% of every prime (the Big Three index managers alone hold roughly 20-30%, per the primes' own proxy statements) and supply the votes once shown the financial case.",
    display_name="Activist Stake Fraction",
    unit="ratio",
    confidence_interval=(0.01, 0.10),
    keywords=["activist", "engine no. 1", "icahn", "board seat", "proxy"],
    latex_symbol=r"f_{activist}",
)

DEFENSE_TAKEOVER_ACQUISITION_PREMIUM = Parameter(
    1.8,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="definition",
    description="Planning multiplier for acquisition premium, execution friction, disclosure timing, and large-position accumulation costs in a counsel-led control campaign",
    display_name="Acquisition Premium Multiplier",
    unit="x",
    confidence_interval=(1.5, 3.0),
    keywords=["acquisition premium", "execution friction", "control"],
    latex_symbol=r"m_{premium}",
)

DEFENSE_TAKEOVER_COST_TOTAL = Parameter(
    (DEFENSE_PRIMES_MARKET_CAP_US + DEFENSE_PRIMES_MARKET_CAP_ALLIED) * DEFENSE_TAKEOVER_CONTROL_FRACTION * DEFENSE_TAKEOVER_ACQUISITION_PREMIUM,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="UPPER-BOUND cost to acquire outright controlling stakes (50.1%) in all major Western military contractors, including the acquisition premium. This is the buy-it-outright ceiling, not the expected entry cost: the realistic path is an activist stake (DEFENSE_TAKEOVER_COST_ACTIVIST) plus index-fund votes, which costs far less. Headline only as a worst case.",
    display_name="Military Takeover Cost (Outright-Control Ceiling)",
    unit="USD",
    keywords=["loving takeover", "military contractor", "market cap", "acquisition", "ceiling"],
    latex_symbol=r"C_{takeover}",
    formula="(DEFENSE_PRIMES_MARKET_CAP_US + DEFENSE_PRIMES_MARKET_CAP_ALLIED) * DEFENSE_TAKEOVER_CONTROL_FRACTION * DEFENSE_TAKEOVER_ACQUISITION_PREMIUM",
    inputs=["DEFENSE_PRIMES_MARKET_CAP_US", "DEFENSE_PRIMES_MARKET_CAP_ALLIED", "DEFENSE_TAKEOVER_CONTROL_FRACTION", "DEFENSE_TAKEOVER_ACQUISITION_PREMIUM"],
    compute=lambda ctx: (ctx["DEFENSE_PRIMES_MARKET_CAP_US"] + ctx["DEFENSE_PRIMES_MARKET_CAP_ALLIED"]) * ctx["DEFENSE_TAKEOVER_CONTROL_FRACTION"] * ctx["DEFENSE_TAKEOVER_ACQUISITION_PREMIUM"],
)

DEFENSE_TAKEOVER_COST_ACTIVIST = Parameter(
    (DEFENSE_PRIMES_MARKET_CAP_US + DEFENSE_PRIMES_MARKET_CAP_ALLIED) * INFLUENCE_ACTIVIST_STAKE_FRACTION,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Realistic entry cost: capital to take an activist (non-control) equity position across all major Western military contractors, bought near market price with no control premium. Board influence comes from the financial argument plus the index-fund votes, not from outright control. This capital buys shares the fund keeps, so the true net cost is far lower than this gross figure. Contrast with the buy-outright ceiling (DEFENSE_TAKEOVER_COST_TOTAL).",
    display_name="Military Activist-Stake Cost (Realistic Entry)",
    unit="USD",
    formula="(DEFENSE_PRIMES_MARKET_CAP_US + DEFENSE_PRIMES_MARKET_CAP_ALLIED) * INFLUENCE_ACTIVIST_STAKE_FRACTION",
    inputs=["DEFENSE_PRIMES_MARKET_CAP_US", "DEFENSE_PRIMES_MARKET_CAP_ALLIED", "INFLUENCE_ACTIVIST_STAKE_FRACTION"],
    compute=lambda ctx: (ctx["DEFENSE_PRIMES_MARKET_CAP_US"] + ctx["DEFENSE_PRIMES_MARKET_CAP_ALLIED"]) * ctx["INFLUENCE_ACTIVIST_STAKE_FRACTION"],
    keywords=["loving takeover", "activist", "entry cost", "board seat", "engine no. 1"],
    latex_symbol=r"C_{activist}",
)

DEFENSE_TAKEOVER_COST_ACTIVIST_PCT_INVESTABLE_ASSETS = Parameter(
    DEFENSE_TAKEOVER_COST_ACTIVIST / GLOBAL_INVESTABLE_ASSETS,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Activist-stake entry cost across the defense primes as a share of total global investable assets. The realistic-path floor of the cost-in-context range, well below the buy-outright ceiling.",
    display_name="Military Activist-Stake Cost as Share of Global Investable Assets",
    unit="rate",
    formula="DEFENSE_TAKEOVER_COST_ACTIVIST / GLOBAL_INVESTABLE_ASSETS",
    inputs=["DEFENSE_TAKEOVER_COST_ACTIVIST", "GLOBAL_INVESTABLE_ASSETS"],
    compute=lambda ctx: ctx["DEFENSE_TAKEOVER_COST_ACTIVIST"] / ctx["GLOBAL_INVESTABLE_ASSETS"],
    keywords=["loving takeover", "activist", "cost in context", "affordability"],
    latex_symbol=r"C_{activist}/A_{investable}",
)

DEFENSE_TAKEOVER_COST_PER_HUMAN = Parameter(
    DEFENSE_TAKEOVER_COST_TOTAL / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Per-person cost of the military takeover distributed across global population",
    display_name="Military Takeover Cost per Human",
    unit="USD",
    formula="DEFENSE_TAKEOVER_COST_TOTAL / GLOBAL_POPULATION_2024",
    inputs=["DEFENSE_TAKEOVER_COST_TOTAL", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["DEFENSE_TAKEOVER_COST_TOTAL"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["loving takeover", "per person", "cost"],
    latex_symbol=r"C_{takeover,pp}",
)

DEFENSE_TAKEOVER_ROI_INCOME_ONLY = Parameter(
    TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA / DEFENSE_TAKEOVER_COST_PER_HUMAN,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Conditional return multiple on the per-human takeover contribution, counting lifetime income gains only: "
                "the treaty trajectory's per-capita lifetime income gain divided by the per-human cost of the "
                "outright-control ceiling. Conditional on campaign success; excludes the dollar value of the "
                "added healthy years (see the blend variant).",
    display_name="Loving Takeover ROI (Income Only)",
    unit="x",
    formula="TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA / DEFENSE_TAKEOVER_COST_PER_HUMAN",
    inputs=["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA", "DEFENSE_TAKEOVER_COST_PER_HUMAN"],
    compute=lambda ctx: ctx["TREATY_TRAJECTORY_LIFETIME_INCOME_GAIN_PER_CAPITA"] / ctx["DEFENSE_TAKEOVER_COST_PER_HUMAN"],
    keywords=["loving takeover", "expected value", "upside", "multiple", "roi"],
    latex_symbol=r"ROI_{takeover,income}",
)

DEFENSE_TAKEOVER_ROI_INCOME_PLUS_HEALTH = Parameter(
    TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH / DEFENSE_TAKEOVER_COST_PER_HUMAN,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Conditional return multiple on the per-human takeover contribution, counting lifetime income gains plus "
                "valued healthy-life gains (the blended personal upside) divided by the per-human cost of the "
                "outright-control ceiling. Conditional on campaign success.",
    display_name="Loving Takeover ROI (Income + Health)",
    unit="x",
    formula="TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH / DEFENSE_TAKEOVER_COST_PER_HUMAN",
    inputs=["TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH", "DEFENSE_TAKEOVER_COST_PER_HUMAN"],
    compute=lambda ctx: ctx["TREATY_PERSONAL_UPSIDE_INCOME_PLUS_HEALTH"] / ctx["DEFENSE_TAKEOVER_COST_PER_HUMAN"],
    keywords=["loving takeover", "expected value", "upside", "multiple", "health", "roi"],
    latex_symbol=r"ROI_{takeover,income+health}",
)

DEFENSE_TAKEOVER_PCT_INVESTABLE_ASSETS = Parameter(
    DEFENSE_TAKEOVER_COST_TOTAL / GLOBAL_INVESTABLE_ASSETS,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Cost to acquire controlling stakes in all major Western military contractors, expressed as a share of total global investable assets. The affordability framing: the entire takeover is a rounding error against the world's investable wealth.",
    display_name="Military Takeover Cost as Share of Global Investable Assets",
    unit="rate",
    formula="DEFENSE_TAKEOVER_COST_TOTAL / GLOBAL_INVESTABLE_ASSETS",
    inputs=["DEFENSE_TAKEOVER_COST_TOTAL", "GLOBAL_INVESTABLE_ASSETS"],
    compute=lambda ctx: ctx["DEFENSE_TAKEOVER_COST_TOTAL"] / ctx["GLOBAL_INVESTABLE_ASSETS"],
    keywords=["loving takeover", "investable assets", "cost in context", "affordability"],
    latex_symbol=r"C_{takeover}/A_{investable}",
)

DEFENSE_TAKEOVER_PCT_ANNUAL_SAVINGS = Parameter(
    DEFENSE_TAKEOVER_COST_TOTAL / GLOBAL_ANNUAL_SAVINGS,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Cost to acquire controlling stakes in all major Western military contractors, expressed as a share of one year of global saving. Roughly ten days of what humanity sets aside annually.",
    display_name="Military Takeover Cost as Share of Annual Global Saving",
    unit="rate",
    formula="DEFENSE_TAKEOVER_COST_TOTAL / GLOBAL_ANNUAL_SAVINGS",
    inputs=["DEFENSE_TAKEOVER_COST_TOTAL", "GLOBAL_ANNUAL_SAVINGS"],
    compute=lambda ctx: ctx["DEFENSE_TAKEOVER_COST_TOTAL"] / ctx["GLOBAL_ANNUAL_SAVINGS"],
    keywords=["loving takeover", "global saving", "cost in context", "affordability"],
    latex_symbol=r"C_{takeover}/S_{annual}",
)

DEFENSE_PRIMES_TRADEABLE_FLOAT = Parameter(
    880_000_000_000,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_ref=ReferenceID.STOCKANALYSIS_MILITARY_PRIME_CAPS_2026,
    source_type="external",
    confidence="medium",
    confidence_interval=(850_000_000_000, 900_000_000_000),
    description="Tradeable float of the 13 Western military primes, approx 91% of their combined "
                "market cap. Method: per-company float and shares-outstanding from stockanalysis.com "
                "statistics pages; big-5 floats verified individually (RTX 92.6%, BA 96.0%, LMT 85.7%, "
                "GD 94.2%, NOC 99.7%). Thales is the outlier at approx 45% float because the French "
                "State (26.60%) and Dassault Aviation (26.59%) stakes are locked",
    display_name="Military Primes Tradeable Float",
    unit="USD",
    keywords=["military contractor", "float", "tradeable shares", "loving takeover"],
    latex_symbol=r"Float_{primes}",
)

GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP = Parameter(
    16_710_000_000_000,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_ref=ReferenceID.OPENSECRETS_TOP_LOBBYING_INDUSTRIES_2025,
    source_type="external",
    confidence="medium",
    confidence_interval=(15_000_000_000_000, 18_000_000_000_000),
    description="Combined market capitalization of the top-5 US public lobbying spenders in each of "
                "the four other government-controlling sectors: pharmaceuticals $1.79T, technology "
                "$13.28T, insurance $0.39T, oil and gas $1.25T. Caveats: Meta (Zuckerberg 60.8% voting) "
                "and Alphabet (Page and Brin 52.3%) cannot be majority-acquired; Ellison owns 40.6% of "
                "Oracle; the largest insurance lobbyists are mutuals with no shares; trade associations "
                "(PhRMA, AHIP, SIFMA, API) are not acquirable",
    display_name="Government-Controlling Sectors Top-5 Market Cap",
    unit="USD",
    keywords=["lobbying", "market cap", "pharma", "tech", "insurance", "oil and gas", "influence"],
    latex_symbol=r"MarketCap_{sectors}",
)

FULL_INFLUENCE_COST_ACTIVIST = Parameter(
    DEFENSE_TAKEOVER_COST_TOTAL + INFLUENCE_ACTIVIST_STAKE_FRACTION * GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    confidence="medium",
    description="Ceiling cost for influence over every government-controlling industry: the buy-outright "
                "defense ceiling plus an activist stake in the top-5 lobbying firms of the other four sectors "
                "(pharma, tech, insurance, oil and gas). The other sectors use the activist tier because their "
                "largest players cannot be majority-acquired anyway (Meta, Alphabet, Oracle founder control). "
                "The activist tier follows the Engine No. 1 precedent: a 0.02% stake won three Exxon board seats, "
                "so a few percent is a loud voice at every table.",
    display_name="Full Influence Package Cost (Ceiling)",
    unit="USD",
    formula="DEFENSE_TAKEOVER_COST_TOTAL + INFLUENCE_ACTIVIST_STAKE_FRACTION * GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP",
    inputs=["DEFENSE_TAKEOVER_COST_TOTAL", "INFLUENCE_ACTIVIST_STAKE_FRACTION", "GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP"],
    compute=lambda ctx: ctx["DEFENSE_TAKEOVER_COST_TOTAL"] + ctx["INFLUENCE_ACTIVIST_STAKE_FRACTION"] * ctx["GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP"],
    keywords=["loving takeover", "activist investor", "influence", "lobbying", "acquisition"],
    latex_symbol=r"C_{influence}",
)

FULL_INFLUENCE_COST_PER_HUMAN = Parameter(
    FULL_INFLUENCE_COST_ACTIVIST / GLOBAL_POPULATION_2024,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Per-person cost of the full influence package (defense primes plus activist stakes in every other government-controlling sector) distributed across global population",
    display_name="Full Influence Package Cost per Human",
    unit="USD",
    formula="FULL_INFLUENCE_COST_ACTIVIST / GLOBAL_POPULATION_2024",
    inputs=["FULL_INFLUENCE_COST_ACTIVIST", "GLOBAL_POPULATION_2024"],
    compute=lambda ctx: ctx["FULL_INFLUENCE_COST_ACTIVIST"] / ctx["GLOBAL_POPULATION_2024"],
    keywords=["loving takeover", "influence", "per person", "cost"],
    latex_symbol=r"C_{influence,pp}",
)

FULL_INFLUENCE_PCT_INVESTABLE_ASSETS = Parameter(
    FULL_INFLUENCE_COST_ACTIVIST / GLOBAL_INVESTABLE_ASSETS,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Cost of the full influence package (every government-controlling industry, not just defense) as a share of total global investable assets. The broader takeover is still a fraction of one percent of the world's investable wealth.",
    display_name="Full Influence Cost as Share of Global Investable Assets",
    unit="rate",
    formula="FULL_INFLUENCE_COST_ACTIVIST / GLOBAL_INVESTABLE_ASSETS",
    inputs=["FULL_INFLUENCE_COST_ACTIVIST", "GLOBAL_INVESTABLE_ASSETS"],
    compute=lambda ctx: ctx["FULL_INFLUENCE_COST_ACTIVIST"] / ctx["GLOBAL_INVESTABLE_ASSETS"],
    keywords=["loving takeover", "investable assets", "cost in context", "affordability", "full influence"],
    latex_symbol=r"C_{influence}/A_{investable}",
)

FULL_INFLUENCE_PCT_ANNUAL_SAVINGS = Parameter(
    FULL_INFLUENCE_COST_ACTIVIST / GLOBAL_ANNUAL_SAVINGS,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Cost of the full influence package (every government-controlling industry, not just defense) as a share of one year of global saving.",
    display_name="Full Influence Cost as Share of Annual Global Saving",
    unit="rate",
    formula="FULL_INFLUENCE_COST_ACTIVIST / GLOBAL_ANNUAL_SAVINGS",
    inputs=["FULL_INFLUENCE_COST_ACTIVIST", "GLOBAL_ANNUAL_SAVINGS"],
    compute=lambda ctx: ctx["FULL_INFLUENCE_COST_ACTIVIST"] / ctx["GLOBAL_ANNUAL_SAVINGS"],
    keywords=["loving takeover", "global saving", "cost in context", "affordability", "full influence"],
    latex_symbol=r"C_{influence}/S_{annual}",
)

FULL_CORPORATE_TAKEOVER_COST_ACTIVIST = Parameter(
    (DEFENSE_PRIMES_MARKET_CAP_US + DEFENSE_PRIMES_MARKET_CAP_ALLIED + GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP) * INFLUENCE_ACTIVIST_STAKE_FRACTION,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Realistic cost to take an activist (non-control) stake across EVERY government-controlling industry at once: military, pharma, tech, insurance, and oil and gas. This is the symmetric activist version of the takeover. Outright majority control of all of them is not even possible (founder and mutual control of Meta, Alphabet, Oracle, and the insurance mutuals), which is exactly why the activist tier, not a 50.1% buyout, is the operative model outside the defense primes.",
    display_name="Full Corporate Activist-Stake Cost (All Sectors)",
    unit="USD",
    formula="(DEFENSE_PRIMES_MARKET_CAP_US + DEFENSE_PRIMES_MARKET_CAP_ALLIED + GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP) * INFLUENCE_ACTIVIST_STAKE_FRACTION",
    inputs=["DEFENSE_PRIMES_MARKET_CAP_US", "DEFENSE_PRIMES_MARKET_CAP_ALLIED", "GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP", "INFLUENCE_ACTIVIST_STAKE_FRACTION"],
    compute=lambda ctx: (ctx["DEFENSE_PRIMES_MARKET_CAP_US"] + ctx["DEFENSE_PRIMES_MARKET_CAP_ALLIED"] + ctx["GOV_CONTROLLING_SECTORS_TOP5_MARKET_CAP"]) * ctx["INFLUENCE_ACTIVIST_STAKE_FRACTION"],
    keywords=["loving takeover", "activist", "all sectors", "corporate takeover", "lobbying"],
    latex_symbol=r"C_{corp,activist}",
)

FULL_CORPORATE_TAKEOVER_COST_ACTIVIST_PCT_INVESTABLE_ASSETS = Parameter(
    FULL_CORPORATE_TAKEOVER_COST_ACTIVIST / GLOBAL_INVESTABLE_ASSETS,
    manual_ref="knowledge/appendix/loving-takeover.qmd",
    source_type="calculated",
    description="Activist stake across every government-controlling industry as a share of total global investable assets.",
    display_name="Full Corporate Activist-Stake Cost as Share of Global Investable Assets",
    unit="rate",
    formula="FULL_CORPORATE_TAKEOVER_COST_ACTIVIST / GLOBAL_INVESTABLE_ASSETS",
    inputs=["FULL_CORPORATE_TAKEOVER_COST_ACTIVIST", "GLOBAL_INVESTABLE_ASSETS"],
    compute=lambda ctx: ctx["FULL_CORPORATE_TAKEOVER_COST_ACTIVIST"] / ctx["GLOBAL_INVESTABLE_ASSETS"],
    keywords=["loving takeover", "activist", "cost in context", "affordability", "all sectors"],
    latex_symbol=r"C_{corp,activist}/A_{investable}",
)

# ============================================================================
# MECHANISM COST-EFFECTIVENESS RANKING
# ============================================================================
# Each mechanism has:
#   - NET COST: the money that is actually spent (gone, not recoverable).
#     Capital deployment (buying shares you keep) has near-zero net cost.
#     Bond issuance (investor capital returned with interest) has near-zero net cost.
#     Expenditure (lobbying, marketing, platform build) is real cost.
#   - P(success|funded): probability of treaty passage given full funding.
#   - EV per dollar: P(success) * annual peace dividend / net cost.
#
# The distinction between expenditure and capital deployment is critical.
# The Loving Takeover deploys ~$873B into shares the fund retains. The net cost
# is the opportunity cost: forgone return from an alternative investment.
# At market-rate returns on defense stocks, opportunity cost approaches zero.
# IABs deploy investor capital that is returned at 272%. Net cost to EOS is
# the bond administration, not the principal.
# ============================================================================

# -- Assumed opportunity cost rate for capital deployment mechanisms --
MECHANISM_OPPORTUNITY_COST_RATE = Parameter(
    0.02,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Annual opportunity cost rate for capital deployment mechanisms (forgone excess return vs market). Defense stocks historically return near-market, so excess opportunity cost is low.",
    display_name="Mechanism Opportunity Cost Rate",
    unit="ratio",
    confidence_interval=(0.0, 0.05),
    keywords=["mechanism", "opportunity cost", "capital deployment"],
    latex_symbol=r"r_{opp}",
    distribution="fixed",
)

# Use canonical cost parameters directly. Do not alias the same Parameter object
# just to fit the mechanism comparison naming pattern.

# -- LOVING TAKEOVER (capital deployment: shares retained) --
MECHANISM_LOVING_TAKEOVER_NET_COST = Parameter(
    DEFENSE_TAKEOVER_COST_TOTAL * 0.02,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Net annual cost of the Loving Takeover: opportunity cost only (capital deployed into shares is retained, not spent). At 2% annual opportunity cost rate.",
    display_name="Loving Takeover Net Cost (Annual)",
    unit="USD",
    keywords=["mechanism", "loving takeover", "net cost", "opportunity cost"],
    latex_symbol=r"C_{takeover,net}",
    formula="DEFENSE_TAKEOVER_COST_TOTAL * MECHANISM_OPPORTUNITY_COST_RATE",
    inputs=["DEFENSE_TAKEOVER_COST_TOTAL", "MECHANISM_OPPORTUNITY_COST_RATE"],
    compute=lambda ctx: ctx["DEFENSE_TAKEOVER_COST_TOTAL"] * ctx["MECHANISM_OPPORTUNITY_COST_RATE"],
)
MECHANISM_LOVING_TAKEOVER_P_SUCCESS = Parameter(
    0.95,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Probability of treaty passage given full funding of the Loving Takeover (mechanical: money buys shares, shares buy board control, board redirects lobbying)",
    display_name="P(Success | Loving Takeover Funded)",
    unit="ratio",
    confidence_interval=(0.80, 0.99),
    keywords=["mechanism", "probability", "loving takeover", "cost-effectiveness"],
    latex_symbol=r"P_{takeover}",
)

# -- TREATY CAMPAIGN (expenditure: lobbying + political spending) --
MECHANISM_TREATY_CAMPAIGN_P_SUCCESS = Parameter(
    0.40,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Probability of treaty passage given full funding of the lobbying + referendum campaign ($1B). Depends on political will after lobbying and public pressure.",
    display_name="P(Success | Treaty Campaign Funded)",
    unit="ratio",
    confidence_interval=(0.15, 0.70),
    keywords=["mechanism", "probability", "treaty campaign", "cost-effectiveness"],
    latex_symbol=r"P_{campaign}",
)

# -- SHIRT CASCADE (expenditure: seed program) --
MECHANISM_SHIRT_CASCADE_P_SUCCESS = Parameter(
    float(SHIRT_CASCADE_PROBABILITY_GIVEN_SEED),
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Probability of treaty passage given full funding of the shirt cascade seed program.",
    display_name="P(Success | Shirt Cascade Funded)",
    unit="ratio",
    formula="SHIRT_CASCADE_PROBABILITY_GIVEN_SEED",
    inputs=["SHIRT_CASCADE_PROBABILITY_GIVEN_SEED"],
    compute=lambda ctx: ctx["SHIRT_CASCADE_PROBABILITY_GIVEN_SEED"],
    confidence="low",
    keywords=["mechanism", "probability", "shirt cascade", "cost-effectiveness"],
    latex_symbol=r"P_{shirt}",
)

# -- COURT OF HUMANITY (expenditure: platform build) --
MECHANISM_COURT_OF_HUMANITY_P_SUCCESS = Parameter(
    0.10,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Probability of treaty passage given Court of Humanity operational. Lowest direct causal link: court rulings are non-binding but create political pressure.",
    display_name="P(Success | Court of Humanity Funded)",
    unit="ratio",
    confidence_interval=(0.03, 0.25),
    keywords=["mechanism", "probability", "court of humanity", "cost-effectiveness"],
    latex_symbol=r"P_{court}",
)

# -- IABs (capital deployment: investor capital returned at 272%) --
# Net cost to EOS is bond administration, estimated at 5% of principal
MECHANISM_IAB_ADMIN_RATE = Parameter(
    0.05,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Annual administrative cost of IABs as fraction of principal (legal, compliance, reporting). The principal itself is investor capital returned with interest, not EOS expenditure.",
    display_name="IAB Admin Cost Rate",
    unit="ratio",
    keywords=["mechanism", "iab", "admin cost"],
    latex_symbol=r"r_{IAB,admin}",
    distribution="fixed",
)
MECHANISM_IAB_NET_COST = Parameter(
    TREATY_CAMPAIGN_TOTAL_COST * 0.05,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Net annual cost of IABs to EOS: administration only (investor capital is returned, not spent)",
    display_name="IAB Net Cost (Annual)",
    unit="USD",
    keywords=["mechanism", "iab", "net cost"],
    latex_symbol=r"C_{IAB,net}",
    formula="TREATY_CAMPAIGN_TOTAL_COST * MECHANISM_IAB_ADMIN_RATE",
    inputs=["TREATY_CAMPAIGN_TOTAL_COST", "MECHANISM_IAB_ADMIN_RATE"],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_TOTAL_COST"] * ctx["MECHANISM_IAB_ADMIN_RATE"],
)
MECHANISM_IAB_P_SUCCESS = Parameter(
    0.60,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Probability of treaty passage given full IAB issuance. High because lobbying is a proven mechanism and IABs align politician incentives directly.",
    display_name="P(Success | IABs Funded)",
    unit="ratio",
    confidence_interval=(0.30, 0.85),
    keywords=["mechanism", "probability", "incentive alignment bonds", "cost-effectiveness"],
    latex_symbol=r"P_{IAB}",
)

# -- dFDA (expenditure: platform build + initial operations) --
MECHANISM_DFDA_NET_COST = Parameter(
    500_000_000,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Net cost to build and deploy the dFDA to operational scale (expenditure; platform generates revenue after deployment but initial build is sunk cost)",
    display_name="dFDA Deployment Net Cost",
    unit="USD",
    confidence_interval=(200_000_000, 1_000_000_000),
    keywords=["mechanism", "dfda", "deployment", "cost"],
    latex_symbol=r"C_{dFDA}",
)
MECHANISM_DFDA_P_SUCCESS = Parameter(
    0.70,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Probability that a funded dFDA produces sufficient cures to create political momentum for the treaty. High because clinical trials mechanically produce treatments; the platform reduces cost per trial.",
    display_name="P(Success | dFDA Funded)",
    unit="ratio",
    confidence_interval=(0.40, 0.90),
    keywords=["mechanism", "probability", "dfda", "cost-effectiveness"],
    latex_symbol=r"P_{dFDA}",
)

# -- GLOBAL REFERENDUM (expenditure: platform + voter acquisition) --
MECHANISM_REFERENDUM_P_SUCCESS = Parameter(
    0.30,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="definition",
    description="Probability of treaty passage given a successful global referendum demonstrating majority support. Non-binding but creates political pressure.",
    display_name="P(Success | Referendum Funded)",
    unit="ratio",
    confidence_interval=(0.10, 0.55),
    keywords=["mechanism", "probability", "referendum", "cost-effectiveness"],
    latex_symbol=r"P_{referendum}",
)

# ============================================================================
# EXPECTED SOCIAL VALUE FOR EACH MECHANISM
# ============================================================================
# EV = P(success) * annual peace dividend. No denominator.
# This is the right metric for comparing mechanisms because cost structures
# are not comparable: some mechanisms deploy capital into assets (Loving
# Takeover, IABs) and the capital is returned or appreciates. Others are
# pure expenditure (shirts, court, campaign). Dividing by "cost" produces
# a metric that penalizes capital deployment and rewards cheap long-shots,
# which is backwards. The Loving Takeover deploys capital into shares
# rather than burning it as ordinary campaign spend, has the highest
# P(success), and is mechanical. It is the best mechanism.
# The cheap expenditure mechanisms (shirts, court) are what you do while
# building toward the capital for the takeover.

MECHANISM_LOVING_TAKEOVER_EV = Parameter(
    MECHANISM_LOVING_TAKEOVER_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Expected annual social value from the Loving Takeover: P(success) * annual peace dividend. Capital is deployed into shares (retained and appreciating), not spent.",
    display_name="Loving Takeover Expected Social Value",
    unit="USD",
    keywords=["mechanism", "cost-effectiveness", "loving takeover", "ev"],
    latex_symbol=r"EV_{takeover}",
    formula="MECHANISM_LOVING_TAKEOVER_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    inputs=["MECHANISM_LOVING_TAKEOVER_P_SUCCESS", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["MECHANISM_LOVING_TAKEOVER_P_SUCCESS"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
)

MECHANISM_IAB_EV = Parameter(
    MECHANISM_IAB_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Expected annual social value from IABs: P(success) * annual peace dividend. Investor capital is returned with interest, not spent.",
    display_name="IAB Expected Social Value",
    unit="USD",
    keywords=["mechanism", "cost-effectiveness", "incentive alignment bonds", "ev"],
    latex_symbol=r"EV_{IAB}",
    formula="MECHANISM_IAB_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    inputs=["MECHANISM_IAB_P_SUCCESS", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["MECHANISM_IAB_P_SUCCESS"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
)

MECHANISM_DFDA_EV = Parameter(
    MECHANISM_DFDA_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Expected annual social value from the dFDA: P(success) * annual peace dividend. Platform build is expenditure ($500M).",
    display_name="dFDA Expected Social Value",
    unit="USD",
    keywords=["mechanism", "cost-effectiveness", "dfda", "ev"],
    latex_symbol=r"EV_{dFDA}",
    formula="MECHANISM_DFDA_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    inputs=["MECHANISM_DFDA_P_SUCCESS", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["MECHANISM_DFDA_P_SUCCESS"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
)

MECHANISM_TREATY_CAMPAIGN_EV = Parameter(
    MECHANISM_TREATY_CAMPAIGN_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Expected annual social value from the treaty campaign: P(success) * annual peace dividend. Lobbying + referendum is expenditure ($1B).",
    display_name="Treaty Campaign Expected Social Value",
    unit="USD",
    keywords=["mechanism", "cost-effectiveness", "treaty campaign", "ev"],
    latex_symbol=r"EV_{campaign}",
    formula="MECHANISM_TREATY_CAMPAIGN_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    inputs=["MECHANISM_TREATY_CAMPAIGN_P_SUCCESS", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["MECHANISM_TREATY_CAMPAIGN_P_SUCCESS"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
)

MECHANISM_REFERENDUM_EV = Parameter(
    MECHANISM_REFERENDUM_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Expected annual social value from the global referendum: P(success) * annual peace dividend. Expenditure ($250M).",
    display_name="Referendum Expected Social Value",
    unit="USD",
    keywords=["mechanism", "cost-effectiveness", "referendum", "ev"],
    latex_symbol=r"EV_{referendum}",
    formula="MECHANISM_REFERENDUM_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    inputs=["MECHANISM_REFERENDUM_P_SUCCESS", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["MECHANISM_REFERENDUM_P_SUCCESS"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
)

MECHANISM_SHIRT_CASCADE_EV = Parameter(
    MECHANISM_SHIRT_CASCADE_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Expected annual social value from the shirt cascade: P(success) * annual peace dividend. Expenditure ($50M).",
    display_name="Shirt Cascade Expected Social Value",
    unit="USD",
    keywords=["mechanism", "cost-effectiveness", "shirt cascade", "ev"],
    latex_symbol=r"EV_{shirt}",
    formula="MECHANISM_SHIRT_CASCADE_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    inputs=["MECHANISM_SHIRT_CASCADE_P_SUCCESS", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["MECHANISM_SHIRT_CASCADE_P_SUCCESS"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
)

MECHANISM_COURT_EV = Parameter(
    MECHANISM_COURT_OF_HUMANITY_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/proof/wishonias-wager.qmd",
    source_type="calculated",
    description="Expected annual social value from the Court of Humanity: P(success) * annual peace dividend. Expenditure ($30M).",
    display_name="Court of Humanity Expected Social Value",
    unit="USD",
    keywords=["mechanism", "cost-effectiveness", "court of humanity", "ev"],
    latex_symbol=r"EV_{court}",
    formula="MECHANISM_COURT_OF_HUMANITY_P_SUCCESS * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    inputs=["MECHANISM_COURT_OF_HUMANITY_P_SUCCESS", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["MECHANISM_COURT_OF_HUMANITY_P_SUCCESS"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
)

# ============================================================================
# SPECIAL EDUCATION BOT (SE_BOT) - Outbound misinformation correction
# ============================================================================
#
# The SE bot scans social media for posts containing identifiable logical
# fallacies about war, defense spending, and disease funding, then replies
# with the specific data that updates the picture. This is the outbound
# complement to Wishonia's inbound tutoring.
#
# Evidence base:
#   - Wood & Porter 2019: factual corrections rarely backfire in survey experiments.
#   - Pennycook et al. 2021: accuracy prompts can improve sharing quality.
#   - Roozenbeek et al. 2022: short prebunking videos improve manipulation recognition.
#   - Munger 2017: public bot replies can change behavior, but effects depend on source status.
#   - Vosoughi et al. 2018: false news diffuses farther and faster than true news.
#
# The persuasion and treaty-attribution values below are calibrated assumptions, not direct
# estimates from any one paper. Keep the distinction explicit in chapter text.
#
# See: knowledge/solution/special-education.qmd

SE_BOT_LLM_COST_PER_POST_USD = Parameter(
    0.006,
    manual_ref="knowledge/solution/special-education.qmd",
    source_ref="anthropic-claude-pricing-2026",
    source_type="external",
    description=(
        "Model inference cost to draft one correction reply. Central case assumes roughly "
        "1,000 input tokens plus 300 output tokens using a Sonnet-class model with some "
        "prompt caching or batch routing. The interval spans Haiku-class routing, Sonnet "
        "batch discounts, longer replies, and retries."
    ),
    display_name="SE Bot LLM Cost Per Post",
    unit="USD",
    confidence="medium",
    distribution="lognormal",
    confidence_interval=(0.002, 0.03),
    keywords=["special education", "bot", "llm", "cost", "anthropic"],
    latex_symbol=r"C_{llm}",
)

SE_BOT_PLATFORM_OVERHEAD_PER_POST_USD = Parameter(
    0.002,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="definition",
    description=(
        "Non-model marginal overhead per attempted correction: search, ranking, duplicate "
        "filtering, policy checks, posting, retries, and failed attempts. This is a planning "
        "assumption because platform access terms and rate limits vary by platform."
    ),
    display_name="SE Bot Platform Overhead Per Post",
    unit="USD",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(0.0005, 0.02),
    keywords=["special education", "bot", "platform", "api", "overhead"],
    latex_symbol=r"C_{platform}",
)

SE_BOT_COST_PER_POST_USD = Parameter(
    SE_BOT_LLM_COST_PER_POST_USD + SE_BOT_PLATFORM_OVERHEAD_PER_POST_USD,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description="Total marginal cost to generate, screen, and post one correction reply.",
    display_name="SE Bot Cost Per Post",
    unit="USD",
    formula="SE_BOT_LLM_COST_PER_POST_USD + SE_BOT_PLATFORM_OVERHEAD_PER_POST_USD",
    confidence="low",
    keywords=["special education", "bot", "cost", "api", "social media"],
    inputs=["SE_BOT_LLM_COST_PER_POST_USD", "SE_BOT_PLATFORM_OVERHEAD_PER_POST_USD"],
    compute=lambda ctx: ctx["SE_BOT_LLM_COST_PER_POST_USD"] + ctx["SE_BOT_PLATFORM_OVERHEAD_PER_POST_USD"],
    latex_symbol=r"C_{post}",
)

SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL = Parameter(
    100_000,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="definition",
    description=(
        "Correctable posts per day across all platforms globally on defense spending, "
        "war, and disease funding topics. Defined as posts from accounts with 100+ followers "
        "containing an identifiable logical fallacy (not merely mentioning the topic). "
        "This is a planning assumption, not a platform-reported count, and should be replaced "
        "with live measurement before making an operating budget."
    ),
    display_name="Relevant Posts Per Day (Global)",
    unit="posts/day",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(5_000, 1_000_000),
    keywords=["special education", "bot", "social media", "volume", "posts"],
    latex_symbol=r"V_{posts}",
)

SE_BOT_ANNUAL_OPERATIONAL_COST_USD = Parameter(
    SE_BOT_COST_PER_POST_USD * SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL * DAYS_PER_YEAR,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description="Annual cost to correct all relevant posts globally: cost_per_post * posts_per_day * days_per_year.",
    display_name="SE Bot Annual Operational Cost",
    unit="USD/year",
    formula="SE_BOT_COST_PER_POST_USD * SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL * DAYS_PER_YEAR",
    confidence="low",
    keywords=["special education", "bot", "cost", "annual", "operational"],
    inputs=["SE_BOT_COST_PER_POST_USD", "SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL"],
    compute=lambda ctx: ctx["SE_BOT_COST_PER_POST_USD"] * ctx["SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL"] * DAYS_PER_YEAR,
    latex_symbol=r"C_{annual}",
)

SE_BOT_TARGET_BELIEF_CHANGE_RATE = Parameter(
    0.02,
    manual_ref="knowledge/solution/special-education.qmd",
    source_ref="wood-porter-2019-backfire-effect",
    source_type="definition",
    description=(
        "Fraction of reply targets who durably update their stated belief after receiving "
        "a correction. Wood and Porter (2019) support the narrower claim that corrections "
        "can reduce false beliefs without routine factual backfire. This 2% value is a "
        "calibrated durable-change assumption for public social replies, reduced from lab "
        "and survey settings because the message is unsolicited and political."
    ),
    display_name="Target Belief Change Rate",
    unit="rate",
    confidence="low",
    distribution="beta",
    confidence_interval=(0.002, 0.10),
    peer_reviewed=True,
    keywords=["special education", "persuasion", "belief change", "correction", "backfire"],
    latex_symbol=r"P_{target}",
)

SE_BOT_OBSERVER_MULTIPLIER = Parameter(
    20,
    manual_ref="knowledge/solution/special-education.qmd",
    source_ref="munger-2017-tweetment-effects",
    source_type="definition",
    description=(
        "Average unique readers of a correction reply besides the target. Munger (2017) is "
        "the closest field evidence for public bot replies, while Vosoughi et al. (2018) "
        "supports the broader claim that false-news cascades can reach large audiences. "
        "Neither paper directly measures observers per correction reply, so this remains "
        "a low-confidence reach assumption."
    ),
    display_name="Observer Multiplier",
    unit="people per post",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(2, 200),
    peer_reviewed=True,
    keywords=["special education", "observer", "social media", "reach", "multiplier"],
    latex_symbol=r"M_{obs}",
)

SE_BOT_OBSERVER_BELIEF_CHANGE_RATE = Parameter(
    0.005,
    manual_ref="knowledge/solution/special-education.qmd",
    source_ref="roozenbeek-2022-inoculation-social-media",
    source_type="definition",
    description=(
        "Fraction of observers (non-target readers) who durably update their belief after "
        "reading a correction exchange. Roozenbeek et al. (2022) supports the general "
        "prebunking mechanism, and Pennycook et al. (2021) supports accuracy prompts. "
        "This parameter is lower than those intervention effects because a public reply "
        "is shorter, unsolicited, and usually viewed while skimming."
    ),
    display_name="Observer Belief Change Rate",
    unit="rate",
    confidence="low",
    distribution="beta",
    confidence_interval=(0.0005, 0.03),
    peer_reviewed=True,
    keywords=["special education", "observer", "persuasion", "inoculation", "belief change"],
    latex_symbol=r"P_{obs}",
)

SE_BOT_PEOPLE_PERSUADED_PER_POST = Parameter(
    SE_BOT_TARGET_BELIEF_CHANGE_RATE + SE_BOT_OBSERVER_MULTIPLIER * SE_BOT_OBSERVER_BELIEF_CHANGE_RATE,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Expected number of people whose belief is durably updated per correction post: "
        "(1 target * target_change_rate) + (observer_multiplier * observer_change_rate). "
        "This counts modeled belief updates, not unique humans across the whole campaign."
    ),
    display_name="People Persuaded Per Post",
    unit="people/post",
    formula="SE_BOT_TARGET_BELIEF_CHANGE_RATE + SE_BOT_OBSERVER_MULTIPLIER * SE_BOT_OBSERVER_BELIEF_CHANGE_RATE",
    confidence="low",
    keywords=["special education", "persuasion", "effectiveness", "per post"],
    inputs=["SE_BOT_TARGET_BELIEF_CHANGE_RATE", "SE_BOT_OBSERVER_MULTIPLIER", "SE_BOT_OBSERVER_BELIEF_CHANGE_RATE"],
    compute=lambda ctx: (
        ctx["SE_BOT_TARGET_BELIEF_CHANGE_RATE"]
        + ctx["SE_BOT_OBSERVER_MULTIPLIER"] * ctx["SE_BOT_OBSERVER_BELIEF_CHANGE_RATE"]
    ),
    latex_symbol=r"N_{persuaded}",
)

SE_BOT_COST_PER_BELIEF_CHANGE_USD = Parameter(
    SE_BOT_COST_PER_POST_USD / SE_BOT_PEOPLE_PERSUADED_PER_POST,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description="Cost per person whose belief is durably updated: cost_per_post / people_persuaded_per_post.",
    display_name="SE Bot Cost Per Belief Change",
    unit="USD/person",
    formula="SE_BOT_COST_PER_POST_USD / SE_BOT_PEOPLE_PERSUADED_PER_POST",
    confidence="low",
    keywords=["special education", "cost-effectiveness", "belief change", "cost per person"],
    inputs=["SE_BOT_COST_PER_POST_USD", "SE_BOT_PEOPLE_PERSUADED_PER_POST"],
    compute=lambda ctx: ctx["SE_BOT_COST_PER_POST_USD"] / ctx["SE_BOT_PEOPLE_PERSUADED_PER_POST"],
    latex_symbol=r"C_{belief}",
)

SE_BOT_ANNUAL_BELIEF_CHANGES = Parameter(
    SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL * DAYS_PER_YEAR * SE_BOT_PEOPLE_PERSUADED_PER_POST,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Modeled annual belief updates from the outbound bot before deduplicating repeat "
        "exposures across posts. This is not a count of unique people."
    ),
    display_name="SE Bot Annual Modeled Belief Changes",
    unit="people/year",
    formula="SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL * DAYS_PER_YEAR * SE_BOT_PEOPLE_PERSUADED_PER_POST",
    confidence="low",
    keywords=["special education", "belief change", "annual", "persuasion"],
    inputs=["SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL", "SE_BOT_PEOPLE_PERSUADED_PER_POST"],
    compute=lambda ctx: (
        ctx["SE_BOT_RELEVANT_POSTS_PER_DAY_GLOBAL"] * DAYS_PER_YEAR * ctx["SE_BOT_PEOPLE_PERSUADED_PER_POST"]
    ),
    latex_symbol=r"N_{belief,annual}",
)

SE_BOT_OUTCOME_ATTRIBUTION_FRACTION = Parameter(
    0.0001,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="definition",
    description=(
        "Fraction of a modeled public-policy outcome attributable to outbound Special "
        "Education running for one year. This is a scenario assumption, not an empirical estimate. The "
        "mechanical model produces modeled belief updates, but the conversion from belief "
        "updates to treaty passage depends on targeting, repeated exposure, elite pickup, "
        "platform enforcement, and whether the bot reaches marginal decision-makers."
    ),
    display_name="Special Education Outcome Attribution Fraction",
    unit="rate",
    confidence="low",
    distribution="lognormal",
    confidence_interval=(0.000001, 0.01),
    keywords=["special education", "attribution", "counterfactual", "outcome", "treaty"],
    latex_symbol=r"\alpha_{bot}",
)

SE_BOT_ANNUAL_EV_USD = Parameter(
    SE_BOT_OUTCOME_ATTRIBUTION_FRACTION * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Conservative expected annual social value from outbound Special Education: "
        "attribution_fraction x annual peace dividend. This is a treaty-only fallback, "
        "not the universal-owner portfolio case."
    ),
    display_name="Special Education Peace-Dividend Expected Value",
    unit="USD/year",
    formula="SE_BOT_OUTCOME_ATTRIBUTION_FRACTION * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
    confidence="low",
    keywords=["special education", "expected value", "bot", "ev", "cost-effectiveness"],
    inputs=["SE_BOT_OUTCOME_ATTRIBUTION_FRACTION", "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    compute=lambda ctx: ctx["SE_BOT_OUTCOME_ATTRIBUTION_FRACTION"] * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"],
    latex_symbol=r"EV_{bot}",
)

SE_BOT_ROI = Parameter(
    SE_BOT_ANNUAL_EV_USD / SE_BOT_ANNUAL_OPERATIONAL_COST_USD,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Conservative treaty-only social ROI for outbound Special Education: "
        "peace_dividend_annual_EV / annual_operational_cost. This excludes broader "
        "political dysfunction tax recovery and universal-owner portfolio gains."
    ),
    display_name="Special Education Peace-Dividend Social ROI",
    unit="ratio",
    formula="SE_BOT_ANNUAL_EV_USD / SE_BOT_ANNUAL_OPERATIONAL_COST_USD",
    confidence="low",
    keywords=["special education", "roi", "return on investment", "cost-effectiveness", "bot"],
    inputs=["SE_BOT_ANNUAL_EV_USD", "SE_BOT_ANNUAL_OPERATIONAL_COST_USD"],
    compute=lambda ctx: ctx["SE_BOT_ANNUAL_EV_USD"] / ctx["SE_BOT_ANNUAL_OPERATIONAL_COST_USD"],
    latex_symbol=r"ROI_{bot}",
)

# Trillion-dollar AUM perspective: the bot as a portfolio hedge
SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD = Parameter(
    115_000_000_000_000,
    manual_ref="knowledge/solution/special-education.qmd",
    source_ref="world-bank-market-cap-listed-companies",
    source_type="external",
    description=(
        "Approximate global market capitalization of listed domestic companies. The 2024 "
        "World Bank series is about $115 trillion; the interval allows for market movement, "
        "coverage differences, and listed-company definition differences."
    ),
    display_name="Global Listed Equity Market Capitalization",
    unit="USD",
    confidence="medium",
    distribution="lognormal",
    confidence_interval=(90_000_000_000_000, 140_000_000_000_000),
    keywords=["special education", "equity", "market cap", "world bank", "portfolio"],
    latex_symbol=r"M_{equity}",
)

SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION = Parameter(
    0.20,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="definition",
    description=(
        "Share of a large public-value gain assumed to be capitalized into listed equities "
        "through lower conflict risk, lower supply-chain risk, and higher expected real output. "
        "This is a valuation scenario, not an observed pass-through estimate."
    ),
    display_name="Equity Capture Share of Public Value",
    unit="percentage",
    confidence="low",
    distribution="beta",
    confidence_interval=(0.05, 0.40),
    keywords=["special education", "equity", "peace dividend", "portfolio", "uplift"],
    latex_symbol=r"f_{equity}",
)

SE_BOT_REFERENCE_AUM_USD = Parameter(
    1_000_000_000_000,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="definition",
    description="Reference institutional portfolio size for the trillion-dollar AUM sensitivity case.",
    display_name="Reference AUM for SE Bot Portfolio Case",
    unit="USD",
    confidence="high",
    distribution="fixed",
    keywords=["special education", "aum", "portfolio", "institutional investor"],
    latex_symbol=r"AUM_{ref}",
)

SE_BOT_AUM_1T_EXPECTED_PORTFOLIO_GAIN_USD = Parameter(
    (
        SE_BOT_OUTCOME_ATTRIBUTION_FRACTION
        * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT
        * SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION
        / SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD
        * SE_BOT_REFERENCE_AUM_USD
    ),
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Expected portfolio gain for a $1T AUM fund from one year of SE bot operation. "
        "Calculation: (attribution_fraction * peace_dividend * equity_capture_share) "
        "/ global_equity_market_cap * reference_AUM. This is a hedge value, not the "
        "social expected value."
    ),
    display_name="$1T AUM Expected Portfolio Gain from SE Bot",
    unit="USD",
    formula=(
        "SE_BOT_OUTCOME_ATTRIBUTION_FRACTION * PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT "
        "* SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION / SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD "
        "* SE_BOT_REFERENCE_AUM_USD"
    ),
    confidence="low",
    keywords=["special education", "asset management", "portfolio", "aum", "institutional investor", "roi"],
    inputs=[
        "SE_BOT_OUTCOME_ATTRIBUTION_FRACTION",
        "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
        "SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION",
        "SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD",
        "SE_BOT_REFERENCE_AUM_USD",
    ],
    compute=lambda ctx: (
        ctx["SE_BOT_OUTCOME_ATTRIBUTION_FRACTION"]
        * ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"]
        * ctx["SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION"]
        / ctx["SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD"]
        * ctx["SE_BOT_REFERENCE_AUM_USD"]
    ),
    latex_symbol=r"G_{1T}",
)

SE_BOT_AUM_1T_PORTFOLIO_ROI = Parameter(
    SE_BOT_AUM_1T_EXPECTED_PORTFOLIO_GAIN_USD / SE_BOT_ANNUAL_OPERATIONAL_COST_USD,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Portfolio-only ROI for a $1T AUM investor: expected portfolio gain divided by "
        "annual bot operating cost. Under the central case this does not include social "
        "value, donations, or reputational value."
    ),
    display_name="$1T AUM Portfolio-Only ROI from SE Bot",
    unit="ratio",
    formula="SE_BOT_AUM_1T_EXPECTED_PORTFOLIO_GAIN_USD / SE_BOT_ANNUAL_OPERATIONAL_COST_USD",
    confidence="low",
    keywords=["special education", "asset management", "portfolio", "aum", "roi", "breakeven"],
    inputs=["SE_BOT_AUM_1T_EXPECTED_PORTFOLIO_GAIN_USD", "SE_BOT_ANNUAL_OPERATIONAL_COST_USD"],
    compute=lambda ctx: ctx["SE_BOT_AUM_1T_EXPECTED_PORTFOLIO_GAIN_USD"] / ctx["SE_BOT_ANNUAL_OPERATIONAL_COST_USD"],
    latex_symbol=r"ROI_{1T}",
)

SE_BOT_AUM_1T_BREAKEVEN_ATTRIBUTION_FRACTION = Parameter(
    (
        SE_BOT_ANNUAL_OPERATIONAL_COST_USD
        * SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD
        / (
            PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT
            * SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION
            * SE_BOT_REFERENCE_AUM_USD
        )
    ),
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Treaty-attribution fraction required for a $1T AUM investor's portfolio gain "
        "to cover the annual bot operating cost, excluding social value and reputational value."
    ),
    display_name="$1T AUM Breakeven Attribution Fraction",
    unit="rate",
    formula=(
        "SE_BOT_ANNUAL_OPERATIONAL_COST_USD * SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD "
        "/ (PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT * SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION "
        "* SE_BOT_REFERENCE_AUM_USD)"
    ),
    confidence="low",
    keywords=["special education", "asset management", "portfolio", "aum", "breakeven", "attribution"],
    inputs=[
        "SE_BOT_ANNUAL_OPERATIONAL_COST_USD",
        "SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD",
        "PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT",
        "SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION",
        "SE_BOT_REFERENCE_AUM_USD",
    ],
    compute=lambda ctx: (
        ctx["SE_BOT_ANNUAL_OPERATIONAL_COST_USD"]
        * ctx["SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD"]
        / (
            ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"]
            * ctx["SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION"]
            * ctx["SE_BOT_REFERENCE_AUM_USD"]
        )
    ),
    latex_symbol=r"\alpha_{breakeven,1T}",
)

SE_BOT_POLITICAL_DYSFUNCTION_ANNUAL_EV_USD = Parameter(
    SE_BOT_OUTCOME_ATTRIBUTION_FRACTION * POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Expected annual social value from outbound Special Education under the political "
        "dysfunction tax framing: attribution_fraction x annual global opportunity cost "
        "from governance failures. This is the broad public-value case, not a direct "
        "portfolio return."
    ),
    display_name="Special Education Political Dysfunction Expected Social Value",
    unit="USD/year",
    formula="SE_BOT_OUTCOME_ATTRIBUTION_FRACTION * POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL",
    confidence="low",
    keywords=["special education", "political dysfunction tax", "expected value", "social value", "roi"],
    inputs=["SE_BOT_OUTCOME_ATTRIBUTION_FRACTION", "POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"],
    compute=lambda ctx: (
        ctx["SE_BOT_OUTCOME_ATTRIBUTION_FRACTION"]
        * ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"]
    ),
    latex_symbol=r"EV_{SE,PDT}",
)

SE_BOT_POLITICAL_DYSFUNCTION_ROI = Parameter(
    SE_BOT_POLITICAL_DYSFUNCTION_ANNUAL_EV_USD / SE_BOT_ANNUAL_OPERATIONAL_COST_USD,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Broad social ROI for outbound Special Education: political_dysfunction_annual_EV "
        "/ annual_operational_cost. This is useful as a social-value ceiling, while the "
        "universal-owner ROI estimates the investable portfolio case."
    ),
    display_name="Special Education Political Dysfunction Social ROI",
    unit="ratio",
    formula="SE_BOT_POLITICAL_DYSFUNCTION_ANNUAL_EV_USD / SE_BOT_ANNUAL_OPERATIONAL_COST_USD",
    confidence="low",
    keywords=["special education", "political dysfunction tax", "roi", "social value"],
    inputs=["SE_BOT_POLITICAL_DYSFUNCTION_ANNUAL_EV_USD", "SE_BOT_ANNUAL_OPERATIONAL_COST_USD"],
    compute=lambda ctx: (
        ctx["SE_BOT_POLITICAL_DYSFUNCTION_ANNUAL_EV_USD"]
        / ctx["SE_BOT_ANNUAL_OPERATIONAL_COST_USD"]
    ),
    latex_symbol=r"ROI_{SE,PDT}",
)

SE_BOT_AUM_1T_UNIVERSAL_OWNER_PORTFOLIO_GAIN_USD = Parameter(
    (
        SE_BOT_OUTCOME_ATTRIBUTION_FRACTION
        * POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL
        * SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION
        / SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD
        * SE_BOT_REFERENCE_AUM_USD
    ),
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Expected portfolio gain for a $1T universal-owner fund from one year of outbound "
        "Special Education. Calculation: attribution_fraction x political_dysfunction_tax "
        "x equity_capture_share / global_equity_market_cap x reference_AUM."
    ),
    display_name="$1T AUM Universal-Owner Portfolio Gain from Special Education",
    unit="USD",
    formula=(
        "SE_BOT_OUTCOME_ATTRIBUTION_FRACTION * POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL "
        "* SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION / SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD "
        "* SE_BOT_REFERENCE_AUM_USD"
    ),
    confidence="low",
    keywords=[
        "special education",
        "political dysfunction tax",
        "universal owner",
        "asset management",
        "portfolio",
        "aum",
        "roi",
    ],
    inputs=[
        "SE_BOT_OUTCOME_ATTRIBUTION_FRACTION",
        "POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL",
        "SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION",
        "SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD",
        "SE_BOT_REFERENCE_AUM_USD",
    ],
    compute=lambda ctx: (
        ctx["SE_BOT_OUTCOME_ATTRIBUTION_FRACTION"]
        * ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"]
        * ctx["SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION"]
        / ctx["SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD"]
        * ctx["SE_BOT_REFERENCE_AUM_USD"]
    ),
    latex_symbol=r"G_{UO,1T}",
)

SE_BOT_AUM_1T_UNIVERSAL_OWNER_PORTFOLIO_ROI = Parameter(
    SE_BOT_AUM_1T_UNIVERSAL_OWNER_PORTFOLIO_GAIN_USD / SE_BOT_ANNUAL_OPERATIONAL_COST_USD,
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Portfolio-only ROI for a $1T universal-owner investor: expected portfolio gain "
        "from political dysfunction tax recovery divided by annual Special Education "
        "operating cost."
    ),
    display_name="$1T AUM Universal-Owner Portfolio ROI from Special Education",
    unit="ratio",
    formula=(
        "SE_BOT_AUM_1T_UNIVERSAL_OWNER_PORTFOLIO_GAIN_USD "
        "/ SE_BOT_ANNUAL_OPERATIONAL_COST_USD"
    ),
    confidence="low",
    keywords=[
        "special education",
        "political dysfunction tax",
        "universal owner",
        "asset management",
        "portfolio",
        "aum",
        "roi",
    ],
    inputs=["SE_BOT_AUM_1T_UNIVERSAL_OWNER_PORTFOLIO_GAIN_USD", "SE_BOT_ANNUAL_OPERATIONAL_COST_USD"],
    compute=lambda ctx: (
        ctx["SE_BOT_AUM_1T_UNIVERSAL_OWNER_PORTFOLIO_GAIN_USD"]
        / ctx["SE_BOT_ANNUAL_OPERATIONAL_COST_USD"]
    ),
    latex_symbol=r"ROI_{UO,1T}",
)

SE_BOT_AUM_1T_UNIVERSAL_OWNER_BREAKEVEN_ATTRIBUTION_FRACTION = Parameter(
    (
        SE_BOT_ANNUAL_OPERATIONAL_COST_USD
        * SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD
        / (
            POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL
            * SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION
            * SE_BOT_REFERENCE_AUM_USD
        )
    ),
    manual_ref="knowledge/solution/special-education.qmd",
    source_type="calculated",
    description=(
        "Political dysfunction attribution fraction required for a $1T universal-owner "
        "investor's portfolio gain to cover annual Special Education operating cost."
    ),
    display_name="$1T AUM Universal-Owner Breakeven Attribution Fraction",
    unit="rate",
    formula=(
        "SE_BOT_ANNUAL_OPERATIONAL_COST_USD * SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD "
        "/ (POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL * SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION "
        "* SE_BOT_REFERENCE_AUM_USD)"
    ),
    confidence="low",
    keywords=[
        "special education",
        "political dysfunction tax",
        "universal owner",
        "asset management",
        "portfolio",
        "aum",
        "breakeven",
        "attribution",
    ],
    inputs=[
        "SE_BOT_ANNUAL_OPERATIONAL_COST_USD",
        "SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD",
        "POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL",
        "SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION",
        "SE_BOT_REFERENCE_AUM_USD",
    ],
    compute=lambda ctx: (
        ctx["SE_BOT_ANNUAL_OPERATIONAL_COST_USD"]
        * ctx["SE_BOT_GLOBAL_EQUITY_MARKET_CAP_USD"]
        / (
            ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"]
            * ctx["SE_BOT_EQUITY_UPLIFT_CAPTURE_FRACTION"]
            * ctx["SE_BOT_REFERENCE_AUM_USD"]
        )
    ),
    latex_symbol=r"\alpha_{breakeven,UO}",
)

# ============================================================================
# GOVERNMENT REPLACEMENT MODULE BUDGETS (comparator-anchored)
# ============================================================================
# Each module cost is anchored to the most similar system that already exists
# (card networks and blockchain rails, national digital-identity systems,
# market-scale fraud detection, frontier inference pricing) rather than to
# invented staffing plans. Inputs carry lognormal uncertainty; Monte Carlo
# propagates it. As many parameters as necessary, as few as possible.

IRS_ANNUAL_OPERATING_BUDGET = Parameter(
    12_320_000_000,
    manual_ref="knowledge/solution/automated-revenue-service.qmd",
    source_ref=ReferenceID.CRS_IRS_APPROPRIATIONS_FY2025,
    source_type="external",
    description="IRS enacted annual appropriation, FY2024 (CRS IF12647, Table 1).",
    display_name="IRS Annual Operating Budget",
    unit="USD",
    distribution="fixed",
    confidence="high",
    last_updated="2024-04",
    keywords=["irs", "internal revenue service", "budget", "appropriation", "12.3b"],
)

# --- Automated Revenue Service (replaces the IRS) ---

AUTOMATED_REVENUE_SERVICE_ANNUAL_TRANSACTION_VOLUME = Parameter(
    500_000_000_000,
    manual_ref="knowledge/solution/automated-revenue-service.qmd",
    source_type="definition",
    description="Design capacity: annual final-consumption settlements processed by the protocol, set well above current US card-network transaction volume.",
    display_name="Automated Revenue Service Annual Transaction Volume",
    unit="transactions",
    distribution="fixed",
    keywords=["automated revenue service", "transactions", "settlement volume", "capacity"],
)

AUTOMATED_REVENUE_SERVICE_ALL_IN_COST_PER_TRANSACTION = Parameter(
    0.0003,
    manual_ref="knowledge/solution/automated-revenue-service.qmd",
    source_type="definition",
    description="All-in cost per settlement (three hundredths of a cent): compute, storage, security audits, and the mostly-AI workforce, amortized per transaction. Anchored to the most similar systems that exist: card networks clear transactions for internal costs in this range, and public blockchain rails settle transfers for fractions of a cent.",
    display_name="All-In Cost per Settlement Transaction",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(0.0001, 0.001),
    keywords=["automated revenue service", "cost per transaction", "all-in", "payment rails", "blockchain"],
)

AUTOMATED_REVENUE_SERVICE_ANNUAL_OPEX = Parameter(
    AUTOMATED_REVENUE_SERVICE_ANNUAL_TRANSACTION_VOLUME * AUTOMATED_REVENUE_SERVICE_ALL_IN_COST_PER_TRANSACTION,
    manual_ref="knowledge/solution/automated-revenue-service.qmd",
    source_type="calculated",
    description="Annual operating cost of the Automated Revenue Service: design transaction volume times the all-in comparator-anchored cost per settlement. Uncertainty propagates from the component distributions via Monte Carlo.",
    display_name="Automated Revenue Service Annual Operating Cost",
    unit="USD",
    formula="TRANSACTIONS × ALL_IN_COST_PER_TRANSACTION",
    inputs=[
        "AUTOMATED_REVENUE_SERVICE_ANNUAL_TRANSACTION_VOLUME",
        "AUTOMATED_REVENUE_SERVICE_ALL_IN_COST_PER_TRANSACTION",
    ],
    compute=lambda ctx: (
        ctx["AUTOMATED_REVENUE_SERVICE_ANNUAL_TRANSACTION_VOLUME"]
        * ctx["AUTOMATED_REVENUE_SERVICE_ALL_IN_COST_PER_TRANSACTION"]
    ),
    keywords=["automated revenue service", "settlement tax", "irs replacement", "operating cost", "opex"],
)

AUTOMATED_REVENUE_SERVICE_SAVINGS_PER_AMERICAN_ANNUAL = Parameter(
    (US_GOV_WASTE_TAX_COMPLIANCE + IRS_ANNUAL_OPERATING_BUDGET - AUTOMATED_REVENUE_SERVICE_ANNUAL_OPEX)
    / US_POPULATION_2024,
    manual_ref="knowledge/solution/automated-revenue-service.qmd",
    source_type="calculated",
    description="Annual savings per American from replacing the IRS and the tax-compliance burden with the Automated Revenue Service, net of the padded replacement budget.",
    display_name="Automated Revenue Service Annual Savings per American",
    unit="USD",
    formula="(TAX_COMPLIANCE_BURDEN + IRS_BUDGET − ARS_BUDGET) / US_POPULATION",
    inputs=[
        "US_GOV_WASTE_TAX_COMPLIANCE",
        "IRS_ANNUAL_OPERATING_BUDGET",
        "AUTOMATED_REVENUE_SERVICE_ANNUAL_OPEX",
        "US_POPULATION_2024",
    ],
    compute=lambda ctx: (
        ctx["US_GOV_WASTE_TAX_COMPLIANCE"] + ctx["IRS_ANNUAL_OPERATING_BUDGET"] - ctx["AUTOMATED_REVENUE_SERVICE_ANNUAL_OPEX"]
    ) / ctx["US_POPULATION_2024"],
    keywords=["automated revenue service", "dividend", "per capita", "savings per american"],
)

# --- Universal Security Administration (replaces welfare administration) ---

UNIVERSAL_SECURITY_ADMIN_ALL_IN_COST_PER_CITIZEN_ANNUAL = Parameter(
    0.30,
    manual_ref="knowledge/solution/universal-security-administration.qmd",
    source_type="definition",
    description="All-in annual cost per citizen served: sybil-resistant identity, 365 daily deposits, and the mostly-AI workforce. Anchored to the most similar system that exists: India's national biometric identity system serves 1.4 billion people at costs in this range per person per year, and payment rails move deposits for fractions of a cent.",
    display_name="Universal Security Administration All-In Annual Cost per Citizen",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(0.10, 1.00),
    keywords=["universal security administration", "cost per citizen", "all-in", "identity", "aadhaar"],
)

UNIVERSAL_SECURITY_ADMIN_ANNUAL_OPEX = Parameter(
    US_POPULATION_2024 * UNIVERSAL_SECURITY_ADMIN_ALL_IN_COST_PER_CITIZEN_ANNUAL,
    manual_ref="knowledge/solution/universal-security-administration.qmd",
    source_type="calculated",
    description="Annual operating cost of the Universal Security Administration: population times the all-in comparator-anchored cost per citizen. Uncertainty propagates from the component distributions via Monte Carlo.",
    display_name="Universal Security Administration Annual Operating Cost",
    unit="USD",
    formula="POPULATION × ALL_IN_COST_PER_CITIZEN",
    inputs=[
        "US_POPULATION_2024",
        "UNIVERSAL_SECURITY_ADMIN_ALL_IN_COST_PER_CITIZEN_ANNUAL",
    ],
    compute=lambda ctx: (
        ctx["US_POPULATION_2024"] * ctx["UNIVERSAL_SECURITY_ADMIN_ALL_IN_COST_PER_CITIZEN_ANNUAL"]
    ),
    keywords=["universal security administration", "ubi", "welfare replacement", "operating cost", "opex"],
)

# --- Aligned Election Commission (replaces campaign finance) ---

ALIGNED_ELECTION_COMMISSION_ANNUAL_OPEX = Parameter(
    7_000_000,
    manual_ref="knowledge/solution/aligned-election-commission.qmd",
    source_type="definition",
    description="All-in annual operating cost of the Aligned Election Commission: alignment-score computation, public data pipelines, and fund routing. Sized as a small data-engineering operation; the most similar existing system is the NRA's politician scorecard, which runs on a budget that rounds to zero.",
    display_name="Aligned Election Commission Annual Operating Cost",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(2_000_000, 20_000_000),
    keywords=["aligned election commission", "alignment score", "campaign finance replacement", "operating cost", "opex"],
)

# --- Decentralized Census Bureau (the sensor array) ---

DECENTRALIZED_CENSUS_BUREAU_ANNUAL_OPEX = Parameter(
    15_000_000,
    manual_ref="knowledge/solution/decentralized-census-bureau.qmd",
    source_type="definition",
    description="All-in annual operating cost of the sensor array: continuously computing, cross-checking, and integrity-auditing the statistics the machine steers by (median after-tax income aggregates, healthy-life-expectancy estimation from dFDA outcome data, data-poisoning detection). Sized as a mid-sized analytics operation; roughly 1% of what the decennial census costs per year amortized. The citizen count itself is a free byproduct of the identity layer.",
    display_name="Decentralized Census Bureau Annual Operating Cost",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(5_000_000, 40_000_000),
    keywords=["decentralized census bureau", "sensor array", "measurement", "operating cost", "opex"],
)

# --- Algorithmic Monetary Authority (replaces the Federal Reserve) ---

ALGORITHMIC_MONETARY_AUTHORITY_ANNUAL_OPEX = Parameter(
    7_500_000,
    manual_ref="knowledge/solution/algorithmic-monetary-authority.qmd",
    source_type="definition",
    description="All-in annual operating cost of the Algorithmic Monetary Authority: basket monitoring, rule execution, continuous public verification, and the humans who hold the pager. Sized as a small monitoring operation; the rule itself is one formula and requires no committee.",
    display_name="Algorithmic Monetary Authority Annual Operating Cost",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(3_000_000, 20_000_000),
    keywords=["algorithmic monetary authority", "federal reserve replacement", "monetary policy", "operating cost", "opex"],
)

# --- Transparent Securities Commission (replaces the SEC wealth gate) ---

TRANSPARENT_SECURITIES_COMMISSION_ANNUAL_OPEX = Parameter(
    20_000_000,
    manual_ref="knowledge/solution/transparent-securities-commission.qmd",
    source_type="definition",
    description="All-in annual operating cost of the Transparent Securities Commission: standardized disclosure schema plus continuous fraud-pattern detection across every issuer on the ledger. Anchored to the most similar existing systems: the real-time fraud-detection operations card networks already run at market scale.",
    display_name="Transparent Securities Commission Annual Operating Cost",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(8_000_000, 50_000_000),
    keywords=["transparent securities commission", "sec replacement", "fraud detection", "operating cost", "opex"],
)

# --- DIH same-budget efficiency (no treaty, no new money) ---

NIH_TRIAL_PATIENTS_FUNDABLE_STATUS_QUO = Parameter(
    NIH_ANNUAL_BUDGET * NIH_CLINICAL_TRIALS_SPENDING_PCT / TRADITIONAL_PHASE3_COST_PER_PATIENT,
    manual_ref="knowledge/solution/dih.qmd",
    source_type="calculated",
    description="Trial participants the NIH's current clinical-trials allocation funds each year at traditional per-patient costs: the status quo output of the existing budget.",
    display_name="NIH Trial Patients Fundable (Status Quo)",
    unit="patients",
    formula="NIH_BUDGET × TRIALS_PCT / TRADITIONAL_COST_PER_PATIENT",
    inputs=["NIH_ANNUAL_BUDGET", "NIH_CLINICAL_TRIALS_SPENDING_PCT", "TRADITIONAL_PHASE3_COST_PER_PATIENT"],
    compute=lambda ctx: ctx["NIH_ANNUAL_BUDGET"] * ctx["NIH_CLINICAL_TRIALS_SPENDING_PCT"] / ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"],
    keywords=["nih", "trial capacity", "status quo", "patients fundable"],
)

DIH_NIH_SAME_BUDGET_PATIENTS_FUNDABLE = Parameter(
    NIH_ANNUAL_BUDGET * NIH_CLINICAL_TRIALS_SPENDING_PCT / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    manual_ref="knowledge/solution/dih.qmd",
    source_type="calculated",
    description="Trial participants the SAME NIH clinical-trials allocation funds each year at dFDA pragmatic-trial prices: identical budget, identical 3.3% split, different procurement. No treaty and no new money required.",
    display_name="DIH Same-Budget Trial Patients Fundable",
    unit="patients",
    formula="NIH_BUDGET × TRIALS_PCT / PRAGMATIC_COST_PER_PATIENT",
    inputs=["NIH_ANNUAL_BUDGET", "NIH_CLINICAL_TRIALS_SPENDING_PCT", "DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    compute=lambda ctx: ctx["NIH_ANNUAL_BUDGET"] * ctx["NIH_CLINICAL_TRIALS_SPENDING_PCT"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    keywords=["dih", "nih", "same budget", "pragmatic trials", "procurement efficiency"],
)

# --- Suite-level aggregates and per-citizen dividends ---

US_GOV_WASTE_PER_CAPITA_ANNUAL = Parameter(
    US_GOV_WASTE_TOTAL / US_POPULATION_2024,
    manual_ref="knowledge/appendix/us-efficiency-audit.qmd",
    source_type="calculated",
    description="The US efficiency gap per person per year: the audit's total governance dysfunction divided across the population. The invoice every American pays silently.",
    display_name="US Governance Dysfunction per Person per Year",
    unit="USD",
    formula="US_GOV_WASTE_TOTAL / US_POPULATION",
    inputs=["US_GOV_WASTE_TOTAL", "US_POPULATION_2024"],
    compute=lambda ctx: ctx["US_GOV_WASTE_TOTAL"] / ctx["US_POPULATION_2024"],
    keywords=["efficiency gap", "per capita", "dysfunction", "waste per person"],
)

GOV_REPLACEMENT_SUITE_ANNUAL_OPEX = Parameter(
    AUTOMATED_REVENUE_SERVICE_ANNUAL_OPEX
    + UNIVERSAL_SECURITY_ADMIN_ANNUAL_OPEX
    + ALIGNED_ELECTION_COMMISSION_ANNUAL_OPEX
    + DECENTRALIZED_CENSUS_BUREAU_ANNUAL_OPEX
    + ALGORITHMIC_MONETARY_AUTHORITY_ANNUAL_OPEX
    + TRANSPARENT_SECURITIES_COMMISSION_ANNUAL_OPEX,
    manual_ref="knowledge/solution/earth-optimization-services.qmd",
    source_type="calculated",
    description="Combined steady-state annual operating cost of the priced government-replacement modules (revenue service, security administration, election commission, census sensor array, monetary authority, securities commission). Excludes the revenue-positive and included-elsewhere modules.",
    display_name="Government Replacement Suite Annual Operating Cost",
    unit="USD",
    formula="ARS + USA + AEC + DCB + AMA + TSC operating costs",
    inputs=[
        "AUTOMATED_REVENUE_SERVICE_ANNUAL_OPEX",
        "UNIVERSAL_SECURITY_ADMIN_ANNUAL_OPEX",
        "ALIGNED_ELECTION_COMMISSION_ANNUAL_OPEX",
        "DECENTRALIZED_CENSUS_BUREAU_ANNUAL_OPEX",
        "ALGORITHMIC_MONETARY_AUTHORITY_ANNUAL_OPEX",
        "TRANSPARENT_SECURITIES_COMMISSION_ANNUAL_OPEX",
    ],
    compute=lambda ctx: (
        ctx["AUTOMATED_REVENUE_SERVICE_ANNUAL_OPEX"]
        + ctx["UNIVERSAL_SECURITY_ADMIN_ANNUAL_OPEX"]
        + ctx["ALIGNED_ELECTION_COMMISSION_ANNUAL_OPEX"]
        + ctx["DECENTRALIZED_CENSUS_BUREAU_ANNUAL_OPEX"]
        + ctx["ALGORITHMIC_MONETARY_AUTHORITY_ANNUAL_OPEX"]
        + ctx["TRANSPARENT_SECURITIES_COMMISSION_ANNUAL_OPEX"]
    ),
    keywords=["suite", "operating cost", "government replacement", "total opex"],
)

GOV_REPLACEMENT_SUITE_OPEX_PER_CITIZEN_ANNUAL = Parameter(
    GOV_REPLACEMENT_SUITE_ANNUAL_OPEX / US_POPULATION_2024,
    manual_ref="knowledge/solution/earth-optimization-services.qmd",
    source_type="calculated",
    description="The whole priced replacement suite's operating cost per citizen per year: roughly one dollar, versus five figures of dysfunction.",
    display_name="Replacement Suite Operating Cost per Citizen per Year",
    unit="USD",
    formula="SUITE_ANNUAL_OPEX / US_POPULATION",
    inputs=["GOV_REPLACEMENT_SUITE_ANNUAL_OPEX", "US_POPULATION_2024"],
    compute=lambda ctx: ctx["GOV_REPLACEMENT_SUITE_ANNUAL_OPEX"] / ctx["US_POPULATION_2024"],
    keywords=["suite", "per citizen", "operating cost", "dollar per person"],
)

DECENTRALIZED_CONGRESS_SAVINGS_PER_CITIZEN_ANNUAL = Parameter(
    (US_GOV_WASTE_TARIFFS + US_GOV_WASTE_CORPORATE_WELFARE
     + US_GOV_WASTE_AGRICULTURAL_SUBSIDIES + US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES)
    / US_POPULATION_2024,
    manual_ref="knowledge/solution/decentralized-congress.qmd",
    source_type="calculated",
    description="Annual savings per citizen from putting the zombie policies to direct evidence-attached votes: tariffs, corporate welfare, agricultural and fossil subsidies, the policies that survive only by never being asked about.",
    display_name="Decentralized Congress Savings per Citizen per Year",
    unit="USD",
    formula="(TARIFFS + CORPORATE_WELFARE + AG_SUBSIDIES + FOSSIL_SUBSIDIES) / US_POPULATION",
    inputs=[
        "US_GOV_WASTE_TARIFFS",
        "US_GOV_WASTE_CORPORATE_WELFARE",
        "US_GOV_WASTE_AGRICULTURAL_SUBSIDIES",
        "US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES",
        "US_POPULATION_2024",
    ],
    compute=lambda ctx: (
        ctx["US_GOV_WASTE_TARIFFS"] + ctx["US_GOV_WASTE_CORPORATE_WELFARE"]
        + ctx["US_GOV_WASTE_AGRICULTURAL_SUBSIDIES"] + ctx["US_GOV_WASTE_FOSSIL_FUEL_SUBSIDIES"]
    ) / ctx["US_POPULATION_2024"],
    keywords=["decentralized congress", "dividend", "per capita", "zombie tariff"],
)

DRUG_TREATMENT_ADMIN_SAVINGS_PER_CITIZEN_ANNUAL = Parameter(
    US_GOV_WASTE_DRUG_WAR / US_POPULATION_2024,
    manual_ref="knowledge/solution/drug-treatment-administration.qmd",
    source_type="calculated",
    description="Annual savings per citizen from ending the drug war and routing addiction into the treatment machinery.",
    display_name="Drug Treatment Administration Savings per Citizen per Year",
    unit="USD",
    formula="DRUG_WAR_ANNUAL_COST / US_POPULATION",
    inputs=["US_GOV_WASTE_DRUG_WAR", "US_POPULATION_2024"],
    compute=lambda ctx: ctx["US_GOV_WASTE_DRUG_WAR"] / ctx["US_POPULATION_2024"],
    keywords=["drug treatment administration", "dividend", "per capita", "drug war"],
)

DEPARTMENT_OF_PEACE_SAVINGS_PER_AMERICAN_ANNUAL = Parameter(
    US_GOV_WASTE_MILITARY_OVERSPEND / US_POPULATION_2024,
    manual_ref="knowledge/solution/department-of-peace.qmd",
    source_type="calculated",
    description="Annual savings per American from trimming military spending to the first-principles homeland-defense baseline: the audit's overspend divided across the population.",
    display_name="Department of Peace Savings per American per Year",
    unit="USD",
    formula="MILITARY_OVERSPEND / US_POPULATION",
    inputs=["US_GOV_WASTE_MILITARY_OVERSPEND", "US_POPULATION_2024"],
    compute=lambda ctx: ctx["US_GOV_WASTE_MILITARY_OVERSPEND"] / ctx["US_POPULATION_2024"],
    keywords=["department of peace", "dividend", "per capita", "military overspend"],
)

# --- Immigration Revenue Service (replaces ICE) ---

US_SMUGGLER_FEE_AVG = Parameter(
    6_937,
    manual_ref="knowledge/solution/immigration-revenue-service.qmd",
    source_ref=ReferenceID.EMIF_COYOTE_FEES_2022,
    source_type="external",
    description="Average fee Mexican migrants paid smugglers to enter the United States (EMIF Norte survey of 20,000+ migrants, second half of 2022). Reported street prices ran higher after 2023; the interval covers the range. This is the market-revealed willingness to pay for entry.",
    display_name="Average Smuggler Fee per US Border Crossing",
    unit="USD",
    distribution="lognormal",
    confidence_interval=(4_000, 14_000),
    confidence="high",
    last_updated="2023-04",
    keywords=["coyote", "smuggler fee", "immigration", "border", "revealed preference"],
)

IMMIGRATION_PRICED_ENTRY_ANNUAL_VOLUME = Parameter(
    2_000_000,
    manual_ref="knowledge/solution/immigration-revenue-service.qmd",
    source_type="definition",
    description="Modeled annual legal entries under uncapped priced entry. Anchored to the most similar thing that already happened: the 2021-2026 US immigration surge that the CBO measured ran at roughly this rate, uninvited and unpriced.",
    display_name="Priced-Entry Annual Volume",
    unit="entrants",
    distribution="lognormal",
    confidence_interval=(1_000_000, 5_000_000),
    keywords=["immigration", "priced entry", "volume", "visa sales"],
)

IMMIGRATION_ENTRY_REVENUE_ANNUAL = Parameter(
    IMMIGRATION_PRICED_ENTRY_ANNUAL_VOLUME * US_SMUGGLER_FEE_AVG,
    manual_ref="knowledge/solution/immigration-revenue-service.qmd",
    source_type="calculated",
    description="Annual entry-fee revenue under priced entry at the smuggler-revealed price: money migrants already pay, redirected from cartels to the Treasury. Excludes the ongoing surtax stream, so it is a floor.",
    display_name="Priced-Entry Annual Fee Revenue",
    unit="USD",
    formula="ENTRANTS × SMUGGLER_FEE",
    inputs=["IMMIGRATION_PRICED_ENTRY_ANNUAL_VOLUME", "US_SMUGGLER_FEE_AVG"],
    compute=lambda ctx: ctx["IMMIGRATION_PRICED_ENTRY_ANNUAL_VOLUME"] * ctx["US_SMUGGLER_FEE_AVG"],
    keywords=["immigration", "entry fees", "revenue", "smuggler market capture"],
)

CBO_IMMIGRATION_SURGE_DEFICIT_REDUCTION_2024_2034 = Parameter(
    900_000_000_000,
    manual_ref="knowledge/solution/immigration-revenue-service.qmd",
    source_ref=ReferenceID.CBO_IMMIGRATION_SURGE_2024,
    source_type="external",
    description="CBO (July 2024): the 2021-2026 immigration surge lowers federal deficits, on net, by $0.9 trillion over 2024-2034 (revenues up $1.2 trillion, spending up $0.3 trillion).",
    display_name="CBO Immigration Surge Deficit Reduction, 2024-2034",
    unit="USD",
    distribution="fixed",
    confidence="high",
    last_updated="2024-07",
    keywords=["cbo", "immigration surge", "deficit reduction", "fiscal impact"],
)

IMMIGRATION_DIVIDEND_PER_CITIZEN_ANNUAL = Parameter(
    (IMMIGRATION_ENTRY_REVENUE_ANNUAL + CBO_IMMIGRATION_SURGE_DEFICIT_REDUCTION_2024_2034 / 10)
    / US_POPULATION_2024,
    manual_ref="knowledge/solution/immigration-revenue-service.qmd",
    source_type="calculated",
    description="Annual per-citizen dividend from priced entry: entry-fee revenue redirected from smugglers to the Treasury, plus the annualized fiscal surplus the CBO measured from a surge of comparable volume. A floor: excludes the surtax stream and the retired enforcement budget.",
    display_name="Immigration Dividend per Citizen per Year",
    unit="USD",
    formula="(ENTRY_FEES + SURGE_FISCAL_SURPLUS / 10 years) / US_POPULATION",
    inputs=[
        "IMMIGRATION_ENTRY_REVENUE_ANNUAL",
        "CBO_IMMIGRATION_SURGE_DEFICIT_REDUCTION_2024_2034",
        "US_POPULATION_2024",
    ],
    compute=lambda ctx: (
        ctx["IMMIGRATION_ENTRY_REVENUE_ANNUAL"] + ctx["CBO_IMMIGRATION_SURGE_DEFICIT_REDUCTION_2024_2034"] / 10
    ) / ctx["US_POPULATION_2024"],
    keywords=["immigration", "dividend", "per capita", "citizen shareholder"],
)

# ==============================================================================
# OPTIMIZED FOOD SYSTEM (knowledge/solution/optimized-food-system.qmd)
# The animal-as-inefficient-middleware case. Planetary aggregates; each is a
# headline metric used in the chapter and citable in the parameters appendix.
# One-off supporting stats (cost curves, COVID $16T, zoonotic share) are cited
# inline in the chapter, not parameterized, per the book's parameterize/inline rule.
# ==============================================================================

FARMED_LAND_ANIMALS_SLAUGHTERED_ANNUAL = Parameter(
    83_000_000_000,  # 83 billion land animals (2022), chickens dominate
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="owid-land-animals-slaughtered",
    source_type="external",
    confidence="high",
    description="Land animals slaughtered for meat globally per year, ~83 billion in 2022 "
                "(UN FAO via Our World in Data). Chickens are the immense majority. Excludes "
                "culled male chicks and animals without data, so it undercounts total farmed "
                "deaths. Dwarfed in turn by aquatic-animal deaths (see AQUATIC_ANIMALS_KILLED_ANNUAL).",
    display_name="Land Animals Slaughtered for Food per Year",
    unit="animals",
    distribution="fixed",
    keywords=["animals", "slaughter", "meat", "livestock", "chickens", "suffering", "food"],
)

AQUATIC_ANIMALS_KILLED_ANNUAL = Parameter(
    1_100_000_000_000,  # conservative low end of the 1.1-2.2 trillion wild-caught range
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="fishcount-wild-fish",
    source_type="external",
    confidence="medium",
    description="Wild-caught fish killed globally per year, estimated at 1.1-2.2 trillion "
                "(average 2000-2019, fishcount.org.uk, derived from FAO capture tonnage and mean "
                "body weights). Value shown is the conservative low end; the range is wide because "
                "these animals are counted by weight, not headcount.",
    display_name="Wild Aquatic Animals Killed for Food per Year (low estimate)",
    unit="animals",
    distribution="fixed",
    keywords=["fish", "aquatic", "wild-caught", "fishcount", "suffering", "food"],
)

FACTORY_FARM_SHARE_US = Parameter(
    0.99,  # 99% of US farmed animals live on factory farms (Sentience Institute)
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="sentience-us-factory-farming",
    source_type="external",
    confidence="high",
    description="Share of US farmed animals living on factory farms, ~99% (Sentience Institute, "
                "using EPA CAFO definitions and USDA farm-size census; widely cited incl. by Our "
                "World in Data). Per-species: ~75% of cows, ~99% of pigs, >99.9% of meat chickens. "
                "Global share is lower for land vertebrates (~74%) and higher once fish are included (>90%).",
    display_name="Share of US Farmed Animals on Factory Farms",
    unit="percent",
    distribution="fixed",
    keywords=["factory farm", "CAFO", "intensive", "animal welfare", "sentience institute"],
)

LIVESTOCK_SHARE_OF_AGRICULTURAL_LAND = Parameter(
    0.80,  # livestock (grazing + feed cropland) = ~80% of agricultural land
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="owid-land-for-agriculture",
    source_type="external",
    confidence="high",
    description="Livestock's share of global agricultural land, combining grazing land and cropland "
                "grown for animal feed, ~80% (Our World in Data, FAOSTAT). Poore & Nemecek (2018) report "
                "~83% of farmland by a slightly different boundary. Defensible range ~77-83%. The striking "
                "point is the mismatch: this majority of farmland returns only ~18% of calories.",
    display_name="Livestock Share of Agricultural Land",
    unit="percent",
    distribution="fixed",
    keywords=["livestock", "land use", "farmland", "grazing", "feed", "agriculture"],
)

LIVESTOCK_SHARE_OF_CALORIES = Parameter(
    0.18,  # livestock provides ~18% of global calories (Poore & Nemecek 2018)
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="poore-nemecek-2018",
    source_type="external",
    confidence="high",
    description="Share of the world's calories provided by meat, aquaculture, eggs, and dairy, ~18% "
                "(Poore & Nemecek 2018, Science, meta-analysis of ~38,700 farms across 119 countries). "
                "Our World in Data reports ~17% by FAOSTAT. Pair with LIVESTOCK_SHARE_OF_AGRICULTURAL_LAND: "
                "the majority of farmland for a small share of the calories.",
    display_name="Livestock Share of Global Calories",
    unit="percent",
    distribution="fixed",
    keywords=["livestock", "calories", "protein", "poore nemecek", "food"],
)

LIVESTOCK_SHARE_OF_PROTEIN = Parameter(
    0.37,  # livestock provides ~37% of global protein (Poore & Nemecek 2018)
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="poore-nemecek-2018",
    source_type="external",
    confidence="high",
    description="Share of the world's protein provided by meat, aquaculture, eggs, and dairy, ~37% "
                "(Poore & Nemecek 2018, Science). Our World in Data reports ~38% by FAOSTAT. "
                "Delivered using ~83% of farmland and producing the majority of food's emissions.",
    display_name="Livestock Share of Global Protein",
    unit="percent",
    distribution="fixed",
    keywords=["livestock", "protein", "poore nemecek", "food"],
)

AGRICULTURE_FRESHWATER_WITHDRAWAL_PCT = Parameter(
    0.70,  # agriculture = ~70% of global freshwater withdrawals
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="owid-water-use-stress",
    source_type="external",
    confidence="medium",
    description="Agriculture's share of global freshwater withdrawals, ~70% (Our World in Data, "
                "FAO AQUASTAT / World Bank). This is the standard consensus figure but is a soft estimate; "
                "recent work argues the true irrigation share could plausibly range ~45-90%. Reported as "
                "the widely-cited ~70% with that uncertainty acknowledged.",
    display_name="Agriculture Share of Freshwater Withdrawals",
    unit="percent",
    distribution="fixed",
    keywords=["water", "freshwater", "irrigation", "agriculture", "AQUASTAT"],
)

FOOD_PRODUCTION_GHG_PCT = Parameter(
    0.26,  # food production = ~26% of global GHG (Poore & Nemecek boundary)
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="owid-environmental-impacts-food",
    source_type="external",
    confidence="high",
    description="Food production's share of global greenhouse-gas emissions, ~26% (~13.7 Gt CO2eq; "
                "Our World in Data, based on Poore & Nemecek 2018). Uses the 'food production' boundary. "
                "A wider whole-food-system boundary including retail, transport, packaging, and waste "
                "(Crippa et al. 2021, Nature Food) reaches ~34%. Present as boundary choices, not a contradiction.",
    display_name="Food Production Share of Global GHG Emissions",
    unit="percent",
    distribution="fixed",
    keywords=["emissions", "GHG", "climate", "food", "agriculture", "poore nemecek"],
)

FARMLAND_REDUCTION_POTENTIAL_PCT = Parameter(
    0.75,  # >75% of farmland freed under a full shift off animal products
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="oxford-leap-food-impacts",
    source_type="external",
    confidence="high",
    description="Reduction in global farmland if the world shifted off meat and dairy while still "
                "feeding everyone, more than 75% (~4.1 billion down to ~1 billion hectares; University of "
                "Oxford LEAP, reporting Poore & Nemecek 2018, Science). Oxford's illustrative equivalent: "
                "an area the size of the US, China, EU, and Australia combined. A hypothetical full-shift "
                "model, not a forecast.",
    display_name="Farmland Freed Under a Shift Off Animal Products",
    unit="percent",
    distribution="fixed",
    keywords=["land", "farmland", "rewilding", "reforestation", "poore nemecek", "diet"],
)

BEEF_FEED_CALORIE_EFFICIENCY_PCT = Parameter(
    0.03,  # ~3% of feed calories become beef calories (Cassidy et al. 2013)
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="cassidy-2013-nourished",
    source_type="external",
    confidence="high",
    description="Caloric conversion efficiency of beef, ~3%: only about 3 of every 100 feed calories "
                "become beef calories (Cassidy et al. 2013, Environmental Research Letters). The often-quoted "
                "'~33 feed calories per beef calorie' is the arithmetic reciprocal of this figure, not a "
                "separate measurement. System-wide, 36% of crop calories go to animal feed and only 12% return "
                "as human food.",
    display_name="Beef Caloric Conversion Efficiency",
    unit="percent",
    distribution="fixed",
    keywords=["feed conversion", "beef", "efficiency", "calories", "thermodynamics"],
)

DIETARY_RISK_DEATHS_ANNUAL = Parameter(
    11_000_000,  # ~11 million deaths/year attributable to dietary risks (GBD 2017)
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="gbd-2017-diet",
    source_type="external",
    confidence="high",
    description="Deaths per year attributable to dietary risk factors, ~11 million (95% UI 10-12 million; "
                "255 million DALYs), from the Global Burden of Disease Study 2017 (Afshin et al., The Lancet 2019). "
                "Diet-driven chronic disease is one of the human-health costs the current food system externalizes.",
    display_name="Deaths per Year from Dietary Risks",
    unit="deaths",
    confidence_interval=(10_000_000, 12_000_000),
    distribution="normal",
    keywords=["diet", "deaths", "chronic disease", "GBD", "lancet", "health"],
)

AMR_DEATHS_ATTRIBUTABLE_2019 = Parameter(
    1_270_000,  # ~1.27 million deaths directly attributable to bacterial AMR in 2019
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="murray-2022-amr",
    source_type="external",
    confidence="high",
    description="Deaths directly attributable to bacterial antimicrobial resistance in 2019, ~1.27 million "
                "(95% UI 0.91-1.71 million); ~4.95 million deaths were associated with it (Murray et al., "
                "The Lancet 2022). Attributable and associated are not additive.",
    display_name="Deaths Directly Attributable to AMR (2019)",
    unit="deaths",
    confidence_interval=(911_000, 1_710_000),
    distribution="lognormal",
    keywords=["antibiotics", "AMR", "resistance", "deaths", "lancet", "livestock"],
)

FOOD_SYSTEM_HIDDEN_COST_ANNUAL = Parameter(
    12_000_000_000_000,  # ~$12 trillion/year global hidden costs (FOLU 2019)
    manual_ref="knowledge/solution/optimized-food-system.qmd",
    source_ref="folu-growing-better-2019",
    source_type="external",
    confidence="medium",
    description="Hidden (external) costs of the global food and land-use system, ~$12 trillion/year, "
                "against a market value of ~$10 trillion (FOLU 'Growing Better' 2019; modeled by an advocacy "
                "coalition, widely cited). Comprises environmental, public-health, and poverty costs; projected "
                "to rise to $16.1 trillion by 2050 under current trends.",
    display_name="Global Food System Hidden Costs per Year",
    unit="USD",
    distribution="fixed",
    keywords=["externalities", "hidden cost", "true cost", "food system", "FOLU"],
)
