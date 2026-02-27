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

import math
import warnings
from enum import Enum
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
        display_name: Optional override for parameter title in documentation (e.g., "dFDA Active Trials")
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
        'source_ref', 'source_type', 'description', 'unit', 'formula', 'latex',
        'confidence', 'last_updated', 'peer_reviewed', 'conservative',
        'sensitivity', 'display_value', 'display_name', 'keywords',
        'validation_min', 'validation_max', 'confidence_interval', 'std_error',
        'distribution', 'inputs', 'compute', 'latex_symbol', 'hide_ci'
    )

    # Type annotations for Pylance/Pyright
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
    keywords: "list[str]"
    validation_min: "float | None"
    validation_max: "float | None"
    confidence_interval: "tuple[float, float] | None"
    std_error: "float | None"
    distribution: "DistributionType | None"
    inputs: "list[str]"
    compute: "Callable[[ComputeContext], float] | None"
    latex_symbol: "str | None"  # LaTeX symbol for this parameter in equations, e.g. "Cost_{DFDA}"
    hide_ci: bool  # Suppress confidence interval display in _variables.yml

    def __new__(
        cls,
        value: float,
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
        keywords: Optional[List[str]] = None,
        validation_min: Optional[float] = None,
        validation_max: Optional[float] = None,
        confidence_interval: Optional[Tuple[float, float]] = None,
        std_error: Optional[float] = None,
        distribution: Union[DistributionType, str, None] = None,
        inputs: Optional[List[str]] = None,
        compute: Optional[Callable[[ComputeContext], float]] = None,
        latex_symbol: Optional[str] = None,  # LaTeX symbol for equations, e.g. "Cost_{DFDA}"
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

        instance = super().__new__(cls, value)
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
        instance.keywords = keywords or []
        instance.validation_min = validation_min
        instance.validation_max = validation_max
        instance.confidence_interval = confidence_interval
        instance.std_error = std_error
        instance.distribution = distribution
        instance.inputs = inputs or []
        instance.compute = compute
        instance.latex_symbol = latex_symbol  # LaTeX symbol for equations, e.g. "Cost_{DFDA}"
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
    source_ref=ReferenceID.GLOBAL_MILITARY_SPENDING,
    source_type="external",
    description="Global military spending in 2024",
    display_name="Global Military Spending in 2024",
    unit="USD",
    distribution="fixed",  # Using point estimate for clean presentation throughout book
    keywords=["2024", "2.7t", "dod", "pentagon", "national security", "army", "navy"],
    latex_symbol=r"Spending_{mil}",  # LaTeX symbol for equations
)  # SIPRI 2024 (rounded to 3 sig figs for clarity)

# Value of Statistical Life (VSL)
VALUE_OF_STATISTICAL_LIFE = Parameter(
    10_000_000,
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

# Total conflict deaths (calculated from breakdown)
GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE,
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

# Individual peace dividend components (1% savings breakdown)
PEACE_DIVIDEND_DIRECT_COSTS = Parameter(
    GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL * TREATY_REDUCTION_PCT,
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

NIH_CLINICAL_TRIALS_SPENDING_PCT = Parameter(
    0.033,
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

GLOBAL_INDUSTRY_CLINICAL_TRIALS_SPENDING_ANNUAL = Parameter(
    GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL - GLOBAL_GOVERNMENT_CLINICAL_TRIALS_SPENDING_ANNUAL,
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
    source_ref=ReferenceID.GLOBAL_NEW_DRUG_APPROVALS_50_ANNUALLY,
    source_type="external",
    description="Average annual new drug approvals globally",
    display_name="Average Annual New Drug Approvals Globally",
    unit="drugs/year",
    keywords=["worldwide", "yearly", "current", "drug", "approvals", "year", "earth"],
    distribution="lognormal",  # Count data with right skew
    confidence_interval=(45, 60),  # FDA approval rate varies 45-60/year
    latex_symbol=r"Drugs_{ann,curr}",  # LaTeX symbol for equations
)  # FDA ~50-55/year

# Historical FDA/Drug Development Parameters
OXFORD_RECOVERY_TRIAL_DURATION_MONTHS = Parameter(
    3,
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


FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER = Parameter(
    (FDA_PHASE_1_TO_APPROVAL_YEARS * MONTHS_PER_YEAR) / OXFORD_RECOVERY_TRIAL_DURATION_MONTHS,
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="calculated",
    description="FDA approval timeline vs Oxford RECOVERY trial (10.5 years ÷ 3 months = 42x slower)",
    display_name="FDA to Oxford RECOVERY Trial Time Multiplier",
    unit="multiplier",
    formula="FDA_PHASE_1_TO_APPROVAL_YEARS × MONTHS_PER_YEAR ÷ OXFORD_RECOVERY_TRIAL_DURATION_MONTHS",
    latex=r"""\begin{aligned}
\text{Multiplier}_{RD} &= \frac{Y_{FDA} \times 12}{M_{RECOVERY}} \\
&= \frac{10.5 \times 12}{3} = 42
\end{aligned}""",
    confidence="high",
    keywords=["recovery", "covid", "trial", "fda", "timeline", "comparison", "speed", "multiplier", "oxford"],
    inputs=['FDA_PHASE_1_TO_APPROVAL_YEARS', 'OXFORD_RECOVERY_TRIAL_DURATION_MONTHS'],
    compute=lambda ctx: (ctx["FDA_PHASE_1_TO_APPROVAL_YEARS"] * MONTHS_PER_YEAR) / ctx["OXFORD_RECOVERY_TRIAL_DURATION_MONTHS"],
    latex_symbol=r"k_{FDA:RECOVERY}",  # LaTeX symbol for equations
)

PRE_1962_PHYSICIAN_COUNT = Parameter(
    144_000,
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
    source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
    source_type="external",
    description="dFDA pragmatic trial cost per patient. Uses ADAPTABLE trial ($929) as DELIBERATELY CONSERVATIVE central estimate. Ramsberg & Platt (2018) reviewed 108 embedded pragmatic trials; 64 with cost data had median of only $97/patient - our estimate may overstate costs by 10x. Confidence interval spans meta-analysis median to complex chronic disease trials.",
    display_name="dFDA Pragmatic Trial Cost per Patient",
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

# dFDA Pragmatic Trial Cost Reduction (forward-looking projection)
DFDA_TRIAL_COST_REDUCTION_FACTOR = Parameter(
    TRADITIONAL_PHASE3_COST_PER_PATIENT / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    source_type="calculated",
    description="Cost reduction factor projected for dFDA pragmatic trials (traditional Phase 3 cost / dFDA pragmatic cost per patient)",
    display_name="dFDA Trial Cost Reduction Factor",
    unit="multiplier",
    formula="TRADITIONAL_PHASE3_COST / DFDA_PRAGMATIC_COST",    keywords=["dfda", "pragmatic", "rct", "clinical trial", "cost reduction", "projected"],
    inputs=['TRADITIONAL_PHASE3_COST_PER_PATIENT', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    latex_symbol=r"k_{reduce}",  # LaTeX symbol for equations
)

# dFDA Trial Cost Reduction as Percentage (derived from factor)
DFDA_TRIAL_COST_REDUCTION_PCT = Parameter(
    1 - (DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT / TRADITIONAL_PHASE3_COST_PER_PATIENT),
    source_type="calculated",
    description="Trial cost reduction percentage: 1 - (dFDA pragmatic cost / traditional Phase 3 cost)",
    display_name="dFDA Trial Cost Reduction Percentage",
    unit="percentage",
    formula="1 - (DFDA_COST / TRADITIONAL_COST)",
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
    0,  # Placeholder, computed below
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
    compute=lambda ctx: round((ctx["US_LIFE_EXPECTANCY_1962"] - ctx["US_LIFE_EXPECTANCY_1880"]) / 7.9, 2),
    latex_symbol=r"\Delta LE_{pre62}",  # LaTeX symbol for equations
)

LIFE_EXPECTANCY_GAIN_1962_2019_YEARS_PER_DECADE = Parameter(
    0,  # Placeholder, computed below
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
    compute=lambda ctx: round((ctx["US_LIFE_EXPECTANCY_2019"] - ctx["US_LIFE_EXPECTANCY_1962"]) / 5.7, 2),
    latex_symbol=r"\Delta LE_{post62}",  # LaTeX symbol for equations
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
    source_type="calculated",
    description="Unique pairwise drug combinations from known safe compounds (n choose 2)",
    display_name="Pairwise Drug Combinations",
    unit="combinations",
    formula="SAFE_COMPOUNDS × (SAFE_COMPOUNDS - 1) ÷ 2",
    keywords=["combination", "pairwise", "polypharmacy", "multi-drug", "synergy"],
    inputs=["SAFE_COMPOUNDS_COUNT"],
    compute=lambda ctx: ctx["SAFE_COMPOUNDS_COUNT"] * (ctx["SAFE_COMPOUNDS_COUNT"] - 1) / 2,
    latex_symbol=r"N_{combo}",  # LaTeX symbol for equations
)

COMBINATION_THERAPY_DISEASE_SPACE = Parameter(
    float(COMBINATION_THERAPY_PAIRS) * float(TRIAL_RELEVANT_DISEASES_COUNT),
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
    source_ref=ReferenceID.CLINICAL_TRIALS_PUZZLE_INTERACTOME,
    source_type="external",
    description="Percentage of human interactome (protein-protein interactions) targeted by drugs",
    display_name="Human Interactome Targeted by Drugs",
    unit="percentage",
    keywords=["interactome", "targets", "proteins", "biology", "drug discovery", "untapped"],
    latex_symbol=r"Pct_{interactome}",  # LaTeX symbol for equations
)

# dFDA operational costs
DFDA_UPFRONT_BUILD = Parameter(
    40_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment one-time build cost (central estimate)",
    display_name="Decentralized Framework for Drug Assessment One-Time Build Cost",
    unit="USD",
    keywords=["40.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    latex_symbol=r"Cost_{build}",  # LaTeX symbol for equations
)  # $40M one-time build cost

DFDA_UPFRONT_BUILD_MAX = Parameter(
    46_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment one-time build cost (high estimate)",
    display_name="Decentralized Framework for Drug Assessment One-Time Build Cost (Maximum)",
    unit="USD",
    keywords=["46.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    latex_symbol=r"Cost_{build,max}",  # LaTeX symbol for equations
)  # $46M one-time build cost (high end)

# DCT Platform Funding Comparables
DCT_PLATFORM_FUNDING_MEDIUM = Parameter(
    500_000_000,
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
    source_type="definition",
    description="Target cost per patient in USD (same as DFDA_TARGET_COST_PER_PATIENT but in dollars)",
    display_name="Decentralized Framework for Drug Assessment Target Cost per Patient in USD",
    unit="USD/patient",
    keywords=["1k", "pragmatic trials", "real world evidence", "participant", "subject", "volunteer", "enrollee"],
    latex_symbol=r"Cost_{target,pt}",  # LaTeX symbol for equations
)  # $1,000 per patient

# dFDA operational cost breakdown (in billions)
DFDA_OPEX_PLATFORM_MAINTENANCE = Parameter(
    15_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment maintenance costs",
    display_name="Decentralized Framework for Drug Assessment Maintenance Costs",
    unit="USD/year",
    keywords=["15.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(10_000_000, 22_000_000),  # $10M-$22M (±30%)
    latex_symbol=r"Cost_{platform}",  # LaTeX symbol for equations
)  # $15M

DFDA_OPEX_STAFF = Parameter(
    10_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment staff costs (minimal, AI-assisted)",
    display_name="Decentralized Framework for Drug Assessment Staff Costs",
    unit="USD/year",
    keywords=["10.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(7_000_000, 15_000_000),  # $7M-$15M (±30%)
    latex_symbol=r"Cost_{staff}",  # LaTeX symbol for equations
)  # $10M - minimal, AI-assisted

DFDA_OPEX_INFRASTRUCTURE = Parameter(
    8_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment infrastructure costs (cloud, security)",
    display_name="Decentralized Framework for Drug Assessment Infrastructure Costs",
    unit="USD/year",
    keywords=["8.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(5_000_000, 12_000_000),  # $5M-$12M (±30%)
    latex_symbol=r"Cost_{infra}",  # LaTeX symbol for equations
)  # $8M - cloud, security

DFDA_OPEX_REGULATORY = Parameter(
    5_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment regulatory coordination costs",
    display_name="Decentralized Framework for Drug Assessment Regulatory Coordination Costs",
    unit="USD/year",
    keywords=["5.0m", "pragmatic trials", "real world evidence", "approval", "authorization", "oversight", "regulation"],
    distribution="lognormal",
    confidence_interval=(3_000_000, 8_000_000),  # $3M-$8M (±30%)
    latex_symbol=r"Cost_{regulatory}",  # LaTeX symbol for equations
)  # $5M - regulatory coordination

DFDA_OPEX_COMMUNITY = Parameter(
    2_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment community support costs",
    display_name="Decentralized Framework for Drug Assessment Community Support Costs",
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
    source_type="calculated",
    description="Total annual Decentralized Framework for Drug Assessment operational costs (sum of all components: platform + staff + infra + regulatory + community)",
    display_name="Total Annual Decentralized Framework for Drug Assessment Operational Costs",
    unit="USD/year",
    formula="PLATFORM_MAINTENANCE + STAFF + INFRASTRUCTURE + REGULATORY + COMMUNITY",    keywords=["pragmatic trials", "real world evidence", "approval", "authorization", "oversight", "regulation", "decentralized trials"],
    # Uncertainty derived from component inputs
    validation_min=25_000_000,   # Floor: Lean MVP with minimal regulatory team
    validation_max=80_000_000,   # Ceiling: Full global compliance + 24/7 support + security audit responses
    inputs=["DFDA_OPEX_PLATFORM_MAINTENANCE", "DFDA_OPEX_STAFF", "DFDA_OPEX_INFRASTRUCTURE", "DFDA_OPEX_REGULATORY", "DFDA_OPEX_COMMUNITY"],
    latex_symbol=r"OPEX_{dFDA}",  # LaTeX symbol for equations
    compute=lambda ctx: sum([ctx["DFDA_OPEX_PLATFORM_MAINTENANCE"], ctx["DFDA_OPEX_STAFF"], ctx["DFDA_OPEX_INFRASTRUCTURE"], ctx["DFDA_OPEX_REGULATORY"], ctx["DFDA_OPEX_COMMUNITY"]])
)

# ===================================================================
# STANDALONE dFDA FUNDING CHAIN (source-agnostic)
# ===================================================================
# These parameters represent dFDA's assumed annual funding level WITHOUT
# specifying the source (treaty, philanthropy, government, etc.).
# The treaty-derived chain (DIH_TREASURY_*) is kept separately for
# the treaty impact paper.

DFDA_ANNUAL_TRIAL_FUNDING = Parameter(
    21_800_000_000,
    source_type="definition",
    distribution="fixed",
    description="Assumed annual funding for dFDA pragmatic clinical trials (~$21.8B/year). Source-agnostic: could come from military reallocation, philanthropy, or government appropriation.",
    display_name="dFDA Annual Trial Funding",
    unit="USD/year",
    keywords=["funding", "annual", "trials", "dfda", "pragmatic trials"],
    latex_symbol=r"Funding_{dFDA,ann}",
)  # $21.8B/year (source-agnostic)

DFDA_TRIAL_SUBSIDIES_ANNUAL = Parameter(
    DFDA_ANNUAL_TRIAL_FUNDING - DFDA_ANNUAL_OPEX,
    source_type="calculated",
    description="Annual clinical trial patient subsidies from dFDA funding (total funding minus operational costs)",
    display_name="dFDA Annual Trial Subsidies",
    unit="USD/year",
    formula="DFDA_ANNUAL_TRIAL_FUNDING - DFDA_ANNUAL_OPEX",
    keywords=["subsidy", "trial", "patient", "funding", "dfda"],
    inputs=["DFDA_ANNUAL_TRIAL_FUNDING", "DFDA_ANNUAL_OPEX"],
    compute=lambda ctx: ctx["DFDA_ANNUAL_TRIAL_FUNDING"] - ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"Subsidies_{dFDA,ann}",
)  # $21.76B/year

DFDA_PATIENTS_FUNDABLE_ANNUALLY = Parameter(
    DFDA_TRIAL_SUBSIDIES_ANNUAL / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    source_type="calculated",
    description="Number of patients fundable annually from dFDA funding at pragmatic trial cost. Source-agnostic counterpart of DIH_PATIENTS_FUNDABLE_ANNUALLY.",
    display_name="dFDA Patients Fundable Annually",
    unit="patients/year",
    formula="DFDA_TRIAL_SUBSIDIES_ANNUAL / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT",
    keywords=["patients", "fundable", "trial", "capacity", "dfda"],
    inputs=["DFDA_TRIAL_SUBSIDIES_ANNUAL", "DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    compute=lambda ctx: ctx["DFDA_TRIAL_SUBSIDIES_ANNUAL"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    latex_symbol=r"N_{fundable,dFDA}",
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
    source_type="calculated",
    description="Annual Decentralized Framework for Drug Assessment benefit from R&D savings (trial cost reduction, secondary component)",
    display_name="Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings",
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
    source_type="calculated",
    description="Annual net savings from R&D cost reduction only (gross savings minus operational costs, excludes regulatory delay value)",
    display_name="Decentralized Framework for Drug Assessment Annual Net Savings (R&D Only)",
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

WHO_QALY_THRESHOLD_COST_EFFECTIVE = Parameter(
    50000,
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

# ============================================================================
# GLOBAL DALY BURDEN (WHO Global Burden of Disease)
# ============================================================================
# Used for calculating DALYs averted from accelerating cures

GLOBAL_ANNUAL_DALY_BURDEN = Parameter(
    2_880_000_000,  # 2.88 billion DALYs/year
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
    # Critique: Assumes regulatory delay affects all age groups equally—may overweight elderly
    validation_min=50,  # Floor: Infectious disease-dominated scenario (HIV, TB, malaria)
    validation_max=75,  # Ceiling: Chronic disease-dominated scenario (cancer, CVD, Alzheimer's)
    latex_symbol=r"Age_{death,delay}",  # LaTeX symbol for equations
)

GLOBAL_LIFE_EXPECTANCY_2024 = Parameter(
    79,
    source_ref=ReferenceID.WHO_GLOBAL_HEALTH_ESTIMATES_2024,
    source_type="external",
    description="Global life expectancy (2024)",
    display_name="Global Life Expectancy (2024)",
    unit="years",
    confidence="high",
    last_updated="2024",
    peer_reviewed=True,
    keywords=["life expectancy", "longevity", "lifespan", "actuarial", "demographics"],
    distribution="normal",  # Normal appropriate: tight empirical data, slow-changing
    std_error=2,  # ±2 years (2.5% CV): Captures measurement + projection uncertainty
    # Economist justification: WHO reports 73.4 (global), with regional variance:
    #   - High-income: 80.3 years (Japan 84, US 77)
    #   - Low-income: 63.7 years (Chad 54, Nigeria 55)
    # Using 79 assumes developed-country treatment access (optimistic for global model)
    # CRITICAL: If dFDA benefits accrue mainly to high-income countries, use 80+
    #           If global access, weight toward lower 73-75 range
    # Tight ±2 years appropriate: actuarial tables very stable, no sudden shifts expected
    validation_min=70,  # Floor: Pessimistic scenario (global conflicts, pandemics)
    validation_max=85,  # Ceiling: Optimistic scenario (longevity breakthroughs, developed countries)
    latex_symbol=r"LE_{global}",  # LaTeX symbol for equations
)

# Expected life extension from 1% treaty research acceleration (25x trial capacity)
# Bounds are physically constrained: 0 (failure) to accident-limited lifespan - current
# Distribution encodes beliefs about where in that range we'll land
LIFE_EXTENSION_YEARS = Parameter(
    20,  # Conservative median: meaningful progress without assuming miracles
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
    DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED * (GLOBAL_LIFE_EXPECTANCY_2024 - REGULATORY_DELAY_MEAN_AGE_OF_DEATH),
    source_type="calculated",
    description="Years of Life Lost from disease eradication delay deaths (PRIMARY estimate)",
    display_name="Years of Life Lost from Disease Eradication Delay",
    unit="years",
    formula="DEATHS_TOTAL × (LIFE_EXPECTANCY - MEAN_AGE_OF_DEATH)",
    confidence="medium",
    keywords=["disease eradication", "YLL", "years of life lost", "disease burden", "mortality burden"],
    inputs=["DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED", "GLOBAL_LIFE_EXPECTANCY_2024", "REGULATORY_DELAY_MEAN_AGE_OF_DEATH"],
    compute=lambda ctx: ctx["DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED"] * (ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["REGULATORY_DELAY_MEAN_AGE_OF_DEATH"]),
    latex_symbol=r"YLL_{lag}",  # LaTeX symbol for equations
)  # 7.63B years

DFDA_EFFICACY_LAG_ELIMINATION_YLD = Parameter(
    DFDA_EFFICACY_LAG_ELIMINATION_DEATHS_AVERTED * REGULATORY_DELAY_SUFFERING_PERIOD_YEARS * CHRONIC_DISEASE_DISABILITY_WEIGHT,
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
    EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL * (GLOBAL_LIFE_EXPECTANCY_2024 - REGULATORY_DELAY_MEAN_AGE_OF_DEATH) * STANDARD_ECONOMIC_QALY_VALUE_USD,
    source_type="calculated",
    description="Total economic loss from delaying existing drugs over 8.2-year efficacy lag. One-time benefit of eliminating Phase 2-4 delay. Excludes innovation acceleration effects.",
    display_name="Total Economic Loss from Historical Progress Delays",
    unit="USD",
    formula="DEATHS_TOTAL × YLL × VSLY",
    confidence="medium",  # Inherited from PHARMA_LIVES_SAVED_ANNUAL uncertainty
    keywords=["$251t", "historical", "total", "one-time", "existing drugs"],
    inputs=['GLOBAL_LIFE_EXPECTANCY_2024', 'EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL', 'REGULATORY_DELAY_MEAN_AGE_OF_DEATH', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["EXISTING_DRUGS_EFFICACY_LAG_DEATHS_TOTAL"] * (ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["REGULATORY_DELAY_MEAN_AGE_OF_DEATH"]) * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Loss_{lag}",  # LaTeX symbol for equations
)  # $251T total (existing drugs only)

# DELETED: EFFICACY_LAG_WITH_INNOVATION_CASCADE_DEATHS_TOTAL and EFFICACY_LAG_WITH_INNOVATION_CASCADE_ECONOMIC_LOSS
# Reason: These used an arbitrary 2× "innovation cascade" multiplier. Replaced by the more rigorous
# queue-based model: TRIAL_CAPACITY_PLUS_EFFICACY_LAG_* parameters which use the empirically-derived
# trial capacity multiplier to calculate cure acceleration.

# Type I vs Type II Error Ratio - Thalidomide Baseline

# Thalidomide disaster parameters (1957-1962)
THALIDOMIDE_CASES_WORLDWIDE = Parameter(
    15_000,  # Conservative midpoint of 10,000-20,000 estimate
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

# Source: /knowledge/appendix/fundraising-strategy.qmd#capital-structure-campaign-vs-implementation
TREATY_CAMPAIGN_DURATION_YEARS = Parameter(
    4,
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
    source_type="calculated",
    description="Total treaty campaign cost (100% VICTORY Incentive Alignment Bonds)",
    display_name="Total 1% Treaty Campaign Cost",
    unit="USD",
    formula="REFERENDUM + LOBBYING + RESERVE",    confidence="high",
    keywords=["1%", "impact investing", "pay for success", "one percent", "debt instrument", "development finance", "fixed income"],
    # UNCERTAINTY: Propagates from component budgets (REFERENDUM, LOBBYING, RESERVE)
    # Expected ±50% given unprecedented scale (no manual override)
    # Comparables: Brexit campaigns ~£40M, Ottawa Treaty ~$10M (1997 dollars)
    # This is 20x larger than any treaty campaign—weak precedents justify wide uncertainty
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
    source_type="definition",
    description="G20 countries lobbying budget",
    display_name="G20 Countries Lobbying Budget",
    unit="USD",
    keywords=["campaign", "lobbying", "g20", "millions", "35.0m"],
    latex_symbol=r"Budget_{lobby,G20}",  # LaTeX symbol for equations
)

CAMPAIGN_DEFENSE_LOBBYIST_BUDGET = Parameter(
    50_000_000,
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
    127_000_000,
    source_ref=ReferenceID.LOBBYING_SPEND_DEFENSE,
    source_type="external",
    confidence="high",
    description="Annual defense industry lobbying spending",
    display_name="Annual Defense Industry Lobbying Spending",
    unit="USD/year",
    peer_reviewed=True,
    last_updated="2024",
    keywords=["127.0m", "armed forces", "yearly", "conflict", "costs", "funding", "investment"],
    latex_symbol=r"Lobby_{def,ann}",  # LaTeX symbol for equations
)

CAMPAIGN_SUPER_PAC_BUDGET = Parameter(
    30_000_000,
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
    # CRITICAL: Legal disputes (pharma, defense contractors) could escalate costs 2-3x.
    validation_min=40_000_000,   # Floor: Lean legal team, minimal dispute resolution
    validation_max=120_000_000,  # Ceiling: Protracted legal challenges from industry groups
    latex_symbol=r"Budget_{legal}",  # LaTeX symbol for equations
)

CAMPAIGN_REGULATORY_NAVIGATION = Parameter(
    20_000_000,
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
    # CRITICAL: Lockheed, Raytheon lobbying power—conversion could require 2-3x budget if contested.
    validation_min=30_000_000,   # Floor: Minimal outreach, focus on willing partners
    validation_max=100_000_000,  # Ceiling: Full industry engagement + job retraining programs
    latex_symbol=r"Budget_{conversion}",  # LaTeX symbol for equations
)

CAMPAIGN_HEALTHCARE_ALIGNMENT = Parameter(
    35_000_000,
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
    source_type="definition",
    description="Contingency fund for unexpected costs",
    display_name="Contingency Fund for Unexpected Costs",
    unit="USD",
    keywords=["50.0m", "contingency", "most likely", "campaign", "base case", "central", "expenditure"],
    distribution="uniform",  # Uniform by definition—contingency is for unknown unknowns
    confidence_interval=(30_000_000, 80_000_000),  # $30M-$80M (wide for true contingency)
    # Economist rationale: Contingency should be 10-20% of total project cost ($1B × 10-20% = $100M-$200M).
    # Using $50M as baseline (5% of $1B) is conservative. Uniform distribution reflects epistemic uncertainty—
    # we don't know what we don't know. Historical precedent: mega-projects require 15-30% contingency.
    # CRITICAL: This is NOT lognormal—contingency spending is bounded and uniform by construction.
    validation_min=20_000_000,   # Floor: Minimal buffer (2% of $1B)
    validation_max=150_000_000,  # Ceiling: Full 15% contingency for mega-project risk
    latex_symbol=r"Budget_{contingency}",  # LaTeX symbol for equations
)

CAMPAIGN_TREATY_IMPLEMENTATION = Parameter(
    40_000_000,
    source_type="definition",
    description="Post-victory treaty implementation support",
    display_name="Post-Victory Treaty Implementation Support",
    unit="USD",
    keywords=["40.0m", "1%", "impact investing", "pay for success", "one percent", "development finance", "impact bond"],
    distribution="lognormal",
    confidence_interval=(30_000_000, 55_000_000),  # $30M-$55M (±30%)
    # Economist rationale: Post-treaty implementation varies with compliance enforcement needs.
    # Ottawa Treaty implementation: $20M/year for 10 years ($200M total). Paris Climate: $100M/year ongoing.
    # Our $40M is 1-year support (campaign phase)—ongoing DIH funding covers long-term implementation.
    # Right-skewed: compliance failures (e.g., Syria violating Ottawa Treaty) require surge funding.
    validation_min=25_000_000,   # Floor: Lean monitoring team, voluntary compliance
    validation_max=80_000_000,   # Ceiling: Full enforcement mechanism + dispute resolution
    latex_symbol=r"Budget_{impl}",  # LaTeX symbol for equations
)

CAMPAIGN_SCALING_PREP = Parameter(
    30_000_000,
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
    source_type="definition",
    description="Minimum investment for institutional investors",
    display_name="Minimum Investment for Institutional Investors",
    unit="USD",
    keywords=["10.0m", "impact investing", "pay for success", "debt instrument", "development finance", "fixed income", "impact bond"],
    latex_symbol=r"Invest_{inst,min}",  # LaTeX symbol for equations
)

FAMILY_OFFICE_INVESTMENT_MIN = Parameter(
    5_000_000,
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
    source_type="calculated",
    description="Total annual system costs (campaign + Decentralized Framework for Drug Assessment operations)",
    display_name="Total Annual Treaty System Costs",
    unit="USD/year",
    formula="CAMPAIGN_ANNUAL + DFDA_OPEX",
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
    source_type="calculated",
    description="Basic annual benefits: peace dividend + Decentralized Framework for Drug Assessment R&D savings only (2 of 8 benefit categories, excludes regulatory delay value)",
    display_name="1% treaty Basic Annual Benefits (Peace + R&D Savings)",
    unit="USD/year",
    formula="PEACE_DIVIDEND + DFDA_RD_SAVINGS",
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
    display_name="Standard Time Horizon for NPV Analysis",
    keywords=["npv", "time", "horizon", "years"],
    distribution="fixed",  # Methodological choice: standard 10-year NPV analysis window
    latex_symbol=r"T_{horizon}",  # LaTeX symbol for equations
)  # Standard 10-year analysis window (T)

# ---
# FINANCIAL PARAMETERS - NPV MODEL COMPONENTS
# ---

# NPV Model - Component Costs
# Core framework and broader initiative costs (for detailed breakdowns)
DFDA_NPV_UPFRONT_COST = Parameter(
    40_000_000,
    source_type="definition",
    description="Decentralized Framework for Drug Assessment Core framework build cost",
    display_name="Decentralized Framework for Drug Assessment Core framework Build Cost",
    unit="USD",
    keywords=["40.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(25_000_000, 65_000_000),  # $25M-$65M (±40% - IT projects have high variance)
    latex_symbol=r"Cost_{upfront}",  # LaTeX symbol for equations
)  # $40M Core framework build

DIH_NPV_UPFRONT_COST_INITIATIVES = Parameter(
    229_750_000,
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
    source_type="definition",
    description="Decentralized Framework for Drug Assessment Core framework annual opex (midpoint of $11-26.5M)",
    display_name="Decentralized Framework for Drug Assessment Core framework Annual OPEX",
    unit="USD/year",
    keywords=["18.9m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(11_000_000, 26_500_000),  # $11M-$26.5M (actual range from source)
    latex_symbol=r"OPEX_{ann}",  # LaTeX symbol for equations
)  # $19M Core framework (midpoint of $11-26.5M)

DIH_NPV_ANNUAL_OPEX_INITIATIVES = Parameter(
    21_100_000,
    source_type="definition",
    description="DIH broader initiatives annual opex (medium case)",
    display_name="DIH Broader Initiatives Annual OPEX",
    unit="USD/year",
    keywords=["21.1m", "pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials"],
    distribution="lognormal",
    confidence_interval=(14_000_000, 32_000_000),  # $14M-$32M (±30%)
    latex_symbol=r"OPEX_{DIH,ann}",  # LaTeX symbol for equations
)  # $21.1M medium case broader initiatives

# NPV Model - Primary Parameters (dFDA-specific)
# Total upfront costs (C0): combines core dFDA framework + broader DIH initiative setup
DFDA_NPV_UPFRONT_COST_TOTAL = Parameter(
    DFDA_NPV_UPFRONT_COST + DIH_NPV_UPFRONT_COST_INITIATIVES,
    source_type="calculated",
    description="Total NPV upfront costs (Decentralized Framework for Drug Assessment core + DIH initiatives)",
    display_name="Decentralized Framework for Drug Assessment Total NPV Upfront Costs",
    unit="USD",
    formula="DFDA_BUILD + DIH_INITIATIVES",    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials", "drug agency"],
    # Uncertainty derived from inputs (DFDA_BUILD + DIH_INITIATIVES)
    validation_min=150_000_000,  # Floor: MVP + essential initiatives only
    validation_max=800_000_000,  # Ceiling: Full scope creep + regulatory capture (raised from $500M)
    inputs=['DFDA_NPV_UPFRONT_COST', 'DIH_NPV_UPFRONT_COST_INITIATIVES'],
    compute=lambda ctx: ctx["DFDA_NPV_UPFRONT_COST"] + ctx["DIH_NPV_UPFRONT_COST_INITIATIVES"],
    latex_symbol=r"Cost_{upfront,total}",  # LaTeX symbol for equations
)  # C0 = $0.26975B

# Total annual operational costs (Cop): combines core dFDA framework + broader DIH initiative annual costs
DFDA_NPV_ANNUAL_OPEX_TOTAL = Parameter(
    DFDA_NPV_ANNUAL_OPEX + DIH_NPV_ANNUAL_OPEX_INITIATIVES,
    source_type="calculated",
    description="Total NPV annual opex (Decentralized Framework for Drug Assessment core + DIH initiatives)",
    display_name="Decentralized Framework for Drug Assessment Total NPV Annual OPEX",
    unit="USD/year",
    formula="DFDA_OPEX + DIH_OPEX",    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials", "drug agency"],
    inputs=['DFDA_NPV_ANNUAL_OPEX', 'DIH_NPV_ANNUAL_OPEX_INITIATIVES'],
    compute=lambda ctx: ctx["DFDA_NPV_ANNUAL_OPEX"] + ctx["DIH_NPV_ANNUAL_OPEX_INITIATIVES"],
    latex_symbol=r"OPEX_{total}",  # LaTeX symbol for equations
)  # Cop = $0.04005B

# dFDA adoption curve: linear ramp from 0% to 100% over 5 years, then constant at 100%
DFDA_NPV_ADOPTION_RAMP_YEARS = Parameter(
    5,
    source_type="definition",
    description="Years to reach full Decentralized Framework for Drug Assessment adoption",
    display_name="Years to Reach Full Decentralized Framework for Drug Assessment Adoption",
    unit="years",
    keywords=["pragmatic trials", "real world evidence", "deployment rate", "market penetration", "participation rate", "uptake", "usage rate"],
    latex_symbol=r"T_{ramp}",  # LaTeX symbol for equations
)  # Years to reach full adoption

# Calculated NPV values for dFDA
DFDA_NPV_PV_ANNUAL_OPEX = Parameter(
    DFDA_NPV_ANNUAL_OPEX_TOTAL
    * (1 - (1 + NPV_DISCOUNT_RATE_STANDARD) ** -NPV_TIME_HORIZON_YEARS)
    / NPV_DISCOUNT_RATE_STANDARD,
    source_type="calculated",
    description="Present value of annual opex over 10 years (NPV formula)",
    display_name="Decentralized Framework for Drug Assessment Present Value of Annual OPEX Over 10 Years",
    unit="USD",
    formula="OPEX × [(1 - (1 + r)^-T) / r]",
    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "yearly"],
    inputs=['DFDA_NPV_ANNUAL_OPEX_TOTAL', 'NPV_DISCOUNT_RATE_STANDARD', 'NPV_TIME_HORIZON_YEARS'],
    compute=lambda ctx: ctx["DFDA_NPV_ANNUAL_OPEX_TOTAL"]
    * (1 - (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** -ctx["NPV_TIME_HORIZON_YEARS"])
    / ctx["NPV_DISCOUNT_RATE_STANDARD"],
    latex_symbol=r"PV_{OPEX}",  # LaTeX symbol for equations
    latex=r"PV_{OPEX} = OPEX_{ann} \times \frac{1 - (1+r)^{-T}}{r}",
)
DFDA_NPV_TOTAL_COST = Parameter(
    DFDA_NPV_UPFRONT_COST_TOTAL + DFDA_NPV_PV_ANNUAL_OPEX,
    source_type="calculated",
    description="Total NPV cost (upfront + PV of annual opex)",
    display_name="Decentralized Framework for Drug Assessment Total NPV Cost",
    unit="USD",
    formula="UPFRONT + PV_OPEX",    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "costs"],
    inputs=['DFDA_NPV_PV_ANNUAL_OPEX', 'DFDA_NPV_UPFRONT_COST_TOTAL'],
    compute=lambda ctx: ctx["DFDA_NPV_UPFRONT_COST_TOTAL"] + ctx["DFDA_NPV_PV_ANNUAL_OPEX"],
    latex_symbol=r"Cost_{dFDA,total}",  # LaTeX symbol for equations
)  # ~$0.54B

# NPV of dFDA benefits with 5-year linear adoption ramp
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
    source_type="calculated",
    description="NPV of Decentralized Framework for Drug Assessment R&D savings only with 5-year adoption ramp (10-year horizon, most conservative financial estimate)",
    display_name="NPV of Decentralized Framework for Drug Assessment Benefits (R&D Only, 10-Year Discounted)",
    unit="USD",
    formula="SUM[Savings × adoption(t) / (1+r)^t] for t=1..10",
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
    latex=r"NPV_{RD} = \sum_{t=1}^{10} \frac{Savings_{RD,ann} \times \frac{\min(t,5)}{5}}{(1+r)^t}",
)  # ~$249.3B NPV of R&D savings only (conservative financial case)

DFDA_NPV_NET_BENEFIT_RD_ONLY = Parameter(
    DFDA_NPV_BENEFIT_RD_ONLY - DFDA_NPV_TOTAL_COST,
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

# Tier 1: Conservative - dFDA R&D savings only (10-year NPV)
# Source: knowledge/appendix/dfda-roi-calculations.qmd NPV analysis
DFDA_ROI_RD_ONLY = Parameter(
    DFDA_NPV_BENEFIT_RD_ONLY / DFDA_NPV_TOTAL_COST,
    source_type="calculated",
    description="ROI from Decentralized Framework for Drug Assessment R&D savings only (10-year NPV, most conservative estimate)",
    display_name="ROI from Decentralized Framework for Drug Assessment R&D Savings Only",
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

# Global GDP (2025) - needed for global opportunity cost calculations
GLOBAL_GDP_2025 = Parameter(
    115_000_000_000_000,  # $115 trillion (2025 estimate from Political Dysfunction Tax paper)
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

# US GDP (2024) - needed for US waste percentage calculations
US_GDP_2024 = Parameter(
    28_780_000_000_000,  # $28.78 trillion (2024 estimate)
    source_ref="worldbank-gdp",
    source_type="external",
    confidence="high",
    distribution="fixed",  # Official statistic
    description="US GDP in 2024 dollars for calculating policy costs as percentage of GDP.",
    display_name="US GDP (2024)",
    unit="USD",
    keywords=["GDP", "US", "economy", "2024"],
)


# =============================================================================
# PART 1: WASTE LEDGER (GLOBAL)
# =============================================================================
# Global-scope waste figures

POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES = Parameter(
    1_300_000_000_000,  # $1.3T annually
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
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="low",
    description="Annual opportunity cost from underfunding high-ROI science (fusion, AI safety). "
                "Human Genome Project: $3.8B cost, $796B-1T impact (141:1 ROI). "
                "Fusion DEMO plant: $5-10B could solve energy/climate permanently. "
                "AI safety: <5% of capabilities spending despite existential stakes. "
                "Reallocating $200B from military waste at 20x multiplier = $4T foregone growth.",
    display_name="Global Science Opportunity Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(2_000_000_000_000, 10_000_000_000_000),
    std_error=2_000_000_000_000,
    keywords=["science", "R&D", "opportunity cost", "global", "fusion", "AI safety"],
    latex_symbol=r"O_{science}",
)

POLITICAL_DYSFUNCTION_GLOBAL_LEAD_OPPORTUNITY_COST = Parameter(
    6_000_000_000_000,  # $6T annually
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

POLITICAL_DYSFUNCTION_GLOBAL_MIGRATION_OPPORTUNITY_COST = Parameter(
    57_000_000_000_000,  # $57T annually (conservative lower bound)
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="low",
    description="Unrealized output from migration restrictions. Clemens (2011) calculated "
                "eliminating labor mobility barriers could increase global GDP by 50-150%. "
                "At $115T global GDP, lower bound = $57T; upper bound = $170T. "
                "Even 5% workforce mobility would generate trillions, exceeding all foreign aid ever given. "
                "This is the largest single distortion in the global economy.",
    display_name="Global Migration Opportunity Cost",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    confidence_interval=(57_000_000_000_000, 170_000_000_000_000),
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
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="calculated",
    confidence="low",
    description="Total global opportunity cost from governance failures: "
                "health innovation delays ($34T), underfunded science ($4T), "
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

# Global opportunity cost as percentage of global GDP
POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_PCT_GDP = Parameter(
    POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL / GLOBAL_GDP_2025,
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
)

# ==============================================================================
# CATEGORY 1: DIRECT FEDERAL SPENDING WASTE (~$1.01T)
# Components representing actual federal budget allocations that could be
# redirected. Solution: Budget reallocation.
# ==============================================================================

# Component 1.1: Military overspend ($615B) [CATEGORY 1: Direct Spending]
US_GOV_WASTE_MILITARY_OVERSPEND = Parameter(
    615_000_000_000,  # $615B annually
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="external",
    confidence="medium",
    description="US military spending above 'Strict Deterrence' baseline. Current budget "
                "~$900B supports global power projection (750+ bases). Strict Deterrence "
                "(nuclear triad $95B, Coast Guard $14B, National Guard $33B, Missile Defense "
                "$28B, Cyber $15B, defensive Navy/Air Force $100B) = ~$285B. "
                "Delta: $900B - $285B = $615B 'Hegemony Tax'. [CATEGORY 1: Direct Spending]",
    display_name="Military Overspend",
    unit="USD",
    distribution=DistributionType.NORMAL,
    confidence_interval=(500_000_000_000, 750_000_000_000),
    std_error=75_000_000_000,
    keywords=["military", "defense", "overspend", "hegemony", "pentagon", "category_1_direct_spending"],
    latex_symbol=r"W_{military}",
)

# Component 1.2: Corporate welfare ($181B) [CATEGORY 1: Direct Spending]
US_GOV_WASTE_CORPORATE_WELFARE = Parameter(
    181_000_000_000,  # $181B annually
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
)

# Cat 1 direct waste as percentage of discretionary spending
US_FED_DISCRETIONARY_WASTE_PCT = Parameter(
    US_GOV_WASTE_CATEGORY_1_DIRECT_SPENDING / US_FED_DISCRETIONARY_SPENDING_2024,
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

POLITICAL_DYSFUNCTION_GLOBAL_EFFICIENCY_SCORE = Parameter(
    (GLOBAL_GDP_2025 - US_GOV_WASTE_TOTAL - POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES) /
    (GLOBAL_GDP_2025 - US_GOV_WASTE_TOTAL - POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES +
     POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL),
    source_ref=ReferenceID.POLITICAL_DYSFUNCTION_TAX_PAPER_2025,
    source_type="calculated",
    confidence="low",
    unit="percent",
    description="Global Governance Efficiency Score from Political Dysfunction Tax paper. "
                "E = Adjusted W_real / W_max, where W_real = GDP - waste, W_max = W_real + opportunity cost. "
                "Paper calculates 30-52% efficiency (using $110.9T adjusted / $211.9T maximum). "
                "This means civilization operates at roughly half its technological potential.",
    display_name="Global Governance Efficiency Score",
    formula="(GDP - WASTE) / (GDP - WASTE + OPPORTUNITY)",
    latex=r"E = \frac{W_{real}}{W_{max}} = \frac{GDP - W_{waste}}{GDP - W_{waste} + O_{total}}",
    inputs=[
        "GLOBAL_GDP_2025",
        "US_GOV_WASTE_TOTAL",
        "POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES",
        "POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL",
    ],
    compute=lambda ctx: (
        (ctx["GLOBAL_GDP_2025"] - ctx["US_GOV_WASTE_TOTAL"] -
         ctx["POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES"]) /
        (ctx["GLOBAL_GDP_2025"] - ctx["US_GOV_WASTE_TOTAL"] -
         ctx["POLITICAL_DYSFUNCTION_GLOBAL_FOSSIL_FUEL_SUBSIDIES"] +
         ctx["POLITICAL_DYSFUNCTION_GLOBAL_OPPORTUNITY_COST_TOTAL"])
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
    source_ref="oecd-govt-spending",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US total government spending as percentage of GDP (federal + state + local). "
                "OECD average is ~40%, but US gets worse outcomes for similar spending.",
    display_name="US Govt Spending (% GDP)",
    unit="percent",
    keywords=["government", "spending", "GDP", "US"],
)

US_LIFE_EXPECTANCY_2023 = Parameter(
    77.5,
    source_ref="cdc-life-expectancy",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US life expectancy at birth (2023). Lowest among high-income OECD countries "
                "despite highest healthcare spending.",
    display_name="US Life Expectancy",
    unit="years",
    keywords=["life expectancy", "US", "health", "outcomes"],
)

US_MEDIAN_HOUSEHOLD_INCOME_2023 = Parameter(
    80_610,  # $80,610 median household income 2023
    source_ref="census-income-2023",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="US median household income (2023). High in absolute terms but adjusted for "
                "healthcare costs and inequality, purchasing power is lower than peers.",
    display_name="US Median Household Income",
    unit="USD",
    keywords=["income", "median", "household", "US"],
)

# SWITZERLAND - Lower spending, better outcomes
SWITZERLAND_GOVT_SPENDING_PCT_GDP = Parameter(
    35.0,  # ~35% of GDP
    source_ref="oecd-govt-spending",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Switzerland government spending as percentage of GDP. 3 percentage points LOWER "
                "than US (35% vs 38%) yet achieves dramatically better outcomes.",
    display_name="Switzerland Govt Spending (% GDP)",
    unit="percent",
    keywords=["government", "spending", "GDP", "Switzerland"],
)

SWITZERLAND_LIFE_EXPECTANCY = Parameter(
    84.0,
    source_ref="who-life-expectancy",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Switzerland life expectancy at birth. 6.5 years LONGER than US (84.0 vs 77.5) "
                "despite lower government spending as % of GDP.",
    display_name="Switzerland Life Expectancy",
    unit="years",
    keywords=["life expectancy", "Switzerland", "health", "outcomes"],
)

SWITZERLAND_MEDIAN_INCOME_PPP = Parameter(
    65_000,  # ~$65K median income PPP
    source_ref="oecd-median-income",
    source_type="external",
    confidence="medium",
    distribution="fixed",
    description="Switzerland median household income (PPP-adjusted). Higher than US when "
                "adjusted for cost of healthcare and other expenses.",
    display_name="Switzerland Median Income (PPP)",
    unit="USD",
    keywords=["income", "median", "Switzerland"],
)

# SINGAPORE - Much lower spending, excellent outcomes
SINGAPORE_GOVT_SPENDING_PCT_GDP = Parameter(
    15.0,  # ~15% of GDP - very lean government
    source_ref="imf-singapore-spending",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Singapore government spending as percentage of GDP. Less than HALF the US rate "
                "(15% vs 38%) yet achieves excellent outcomes through efficiency.",
    display_name="Singapore Govt Spending (% GDP)",
    unit="percent",
    keywords=["government", "spending", "GDP", "Singapore"],
)

SINGAPORE_LIFE_EXPECTANCY = Parameter(
    84.1,
    source_ref="who-life-expectancy",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Singapore life expectancy at birth. 6.6 years LONGER than US (84.1 vs 77.5) "
                "despite government spending at less than half the rate.",
    display_name="Singapore Life Expectancy",
    unit="years",
    keywords=["life expectancy", "Singapore", "health", "outcomes"],
)

SINGAPORE_GDP_PER_CAPITA_PPP = Parameter(
    105_000,  # ~$105K GDP per capita PPP
    source_ref="worldbank-singapore-gdp",
    source_type="external",
    confidence="high",
    distribution="fixed",
    description="Singapore GDP per capita (PPP-adjusted). Among highest in world, "
                "demonstrating that lean government can coexist with prosperity.",
    display_name="Singapore GDP per Capita (PPP)",
    unit="USD",
    keywords=["GDP", "per capita", "Singapore"],
)

# Comparison metrics: US vs international benchmarks
# These are definitions based on fixed government statistics (no uncertainty propagation needed)
US_VS_SWITZERLAND_LIFE_EXPECTANCY_GAP = Parameter(
    6.5,  # 84.0 - 77.5 = 6.5 years
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
)

US_VS_SWITZERLAND_SPENDING_GAP = Parameter(
    3.0,  # 38.0 - 35.0 = 3.0%
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
)

US_VS_SINGAPORE_SPENDING_GAP = Parameter(
    23.0,  # 38.0 - 15.0 = 23.0%
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
)

# Implied dysfunction premium: US spends more but gets worse outcomes
# If US achieved Swiss efficiency, same spending would yield better outcomes
# If US achieved Singapore efficiency, same outcomes could be achieved with 60% less spending
US_DYSFUNCTION_PREMIUM_VS_SWITZERLAND = Parameter(
    3.0,  # 3% of GDP more spending for worse outcomes (38% - 35%)
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
    source_type="calculated",
    description="Total upper-bound investment for US political reform: (campaign spending + 2 years lobbying) × effort multiplier + Congress career advocacy. Represents cost to achieve democratic parity with incumbent interests.",
    display_name="US Political Reform Investment (Total)",
    unit="USD",
    formula="(CAMPAIGN + LOBBYING×2) × EFFORT_MULTIPLIER + CONGRESS_CAREER",
    confidence="low",
    keywords=["political reform", "advocacy", "investment", "democratic parity", "us"],
    inputs=["US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024", "US_TOTAL_LOBBYING_ANNUAL", "US_POLITICAL_EFFORT_MULTIPLIER", "US_CONGRESS_FULL_ADVOCACY_COST"],
    compute=lambda ctx: (ctx["US_TOTAL_FEDERAL_CAMPAIGN_SPENDING_2024"] + ctx["US_TOTAL_LOBBYING_ANNUAL"] * 2) * ctx["US_POLITICAL_EFFORT_MULTIPLIER"] + ctx["US_CONGRESS_FULL_ADVOCACY_COST"],
    latex_symbol=r"Cost_{US,total}",
    latex=r"Cost_{US,total} = (Cost_{campaign} + Cost_{lobby} \times 2) \times \mu_{effort} + Cost_{career}",
)

# Global Political Costs
NATO_DEFENSE_SPENDING_ANNUAL = Parameter(
    1_506_000_000_000,  # $1.506T NATO defense spending 2024
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
# FUNDING ALLOCATION (Updated to include IAB)
# ---

DIVIDEND_COVERAGE_FACTOR = Parameter(
    TREATY_ANNUAL_FUNDING / DFDA_ANNUAL_OPEX,
    source_type="calculated",
    description="Coverage factor of treaty funding vs Decentralized Framework for Drug Assessment opex (sustainability margin)",
    display_name="Coverage Factor of Treaty Funding vs Decentralized Framework for Drug Assessment OPEX",
    unit="ratio",
    formula="TREATY_FUNDING ÷ DFDA_OPEX",    keywords=["pragmatic trials", "real world evidence", "multiple", "decentralized trials", "drug agency", "food and drug administration", "international agreement"],
    inputs=['DFDA_ANNUAL_OPEX', 'TREATY_ANNUAL_FUNDING'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] / ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"k_{coverage}",  # LaTeX symbol for equations
)  # ~679x
DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL = Parameter(
    TREATY_ANNUAL_FUNDING - VICTORY_BOND_ANNUAL_PAYOUT - IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL,
    source_ref="",
    source_type="calculated",  # Derived from treaty funding minus bond and IAB allocations
    description="Annual funding for pragmatic clinical trials (treaty funding minus VICTORY Incentive Alignment Bond payouts and IAB political incentive mechanism)",
    display_name="Annual Funding for Pragmatic Clinical Trials",
    unit="USD/year",
    formula="TREATY_FUNDING - BOND_PAYOUT - IAB_POLITICAL_INCENTIVE_FUNDING",
    keywords=["impact investing", "pay for success", "distributed research", "global research", "open science", "debt instrument", "development finance"],
    inputs=['TREATY_ANNUAL_FUNDING', 'VICTORY_BOND_ANNUAL_PAYOUT', 'IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] - ctx["VICTORY_BOND_ANNUAL_PAYOUT"] - ctx["IAB_POLITICAL_INCENTIVE_FUNDING_ANNUAL"],
    latex_symbol=r"Treasury_{RD,ann}",  # LaTeX symbol for equations
)  # $21.744B/year (80% of treaty funding)
DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL = Parameter(
    DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL - DFDA_ANNUAL_OPEX,
    source_type="calculated",
    description="Annual clinical trial patient subsidies (all medical research funds after Decentralized Framework for Drug Assessment operations)",
    display_name="Annual Clinical Trial Patient Subsidies",
    unit="USD/year",
    formula="MEDICAL_RESEARCH_FUNDING - DFDA_OPEX",    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "rct", "patient subsidy"],
    inputs=['DFDA_ANNUAL_OPEX', 'DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL'],
    compute=lambda ctx: ctx["DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL"] - ctx["DFDA_ANNUAL_OPEX"],
    latex_symbol=r"Subsidies_{trial,ann}",  # LaTeX symbol for equations
)  # $24.422B/year - ALL remaining funds go to subsidizing patient trial participation

DIH_PATIENTS_FUNDABLE_ANNUALLY = Parameter(
    DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    source_type="calculated",
    description="Number of patients fundable annually at dFDA pragmatic trial cost. Based on empirical pragmatic trial costs (RECOVERY to PCORnet range).",
    display_name="Patients Fundable Annually",
    unit="patients/year",
    formula="TRIAL_SUBSIDIES ÷ DFDA_COST_PER_PATIENT",    keywords=["trial", "participant", "enrollment", "capacity", "patient"],
    inputs=['DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
    latex_symbol=r"N_{fundable,ann}",  # LaTeX symbol for equations
)

# Funding allocation percentages (calculated from absolute values)
DIH_TREASURY_MEDICAL_RESEARCH_PCT = Parameter(
    DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL / TREATY_ANNUAL_FUNDING,
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
    source_type="calculated",
    description="Percentage of treaty funding allocated to Decentralized Framework for Drug Assessment framework overhead",
    display_name="Decentralized Framework for Drug Assessment Overhead Percentage of Treaty Funding",
    unit="rate",
    formula="DFDA_OPEX / TREATY_FUNDING",
    confidence="high",
    keywords=["allocation", "percentage", "overhead", "platform", "opex"],
    inputs=["DFDA_ANNUAL_OPEX", "TREATY_ANNUAL_FUNDING"],
    compute=lambda ctx: ctx["DFDA_ANNUAL_OPEX"] / ctx["TREATY_ANNUAL_FUNDING"],
    latex_symbol=r"OPEX_{pct}",  # LaTeX symbol for equations
)  # 0.15%

SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL = Parameter(
    10,
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
# dFDA funding can support ~23.4M patients/year at pragmatic trial cost ($929/patient)
# Current global trial capacity: 1.9M patients/year (IQVIA 2022)
# Capacity Multiplier = dFDA capacity / Current capacity
DFDA_TRIAL_CAPACITY_MULTIPLIER = Parameter(
    DFDA_PATIENTS_FUNDABLE_ANNUALLY / CURRENT_TRIAL_SLOTS_AVAILABLE,
    source_type="calculated",
    description="Trial capacity multiplier from dFDA funding capacity vs. current global trial participation",
    display_name="Trial Capacity Multiplier",
    unit="x",
    formula="DFDA_PATIENTS_FUNDABLE_ANNUALLY ÷ CURRENT_TRIAL_SLOTS",
    keywords=["pragmatic trials", "real world evidence", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "multiple"],
    inputs=['CURRENT_TRIAL_SLOTS_AVAILABLE', 'DFDA_PATIENTS_FUNDABLE_ANNUALLY'],
    compute=lambda ctx: ctx["DFDA_PATIENTS_FUNDABLE_ANNUALLY"] / ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"],
    latex_symbol=r"k_{capacity}",  # LaTeX symbol for equations
)  # Trial capacity multiplier from simple funding economics (dFDA patients fundable / current trial slots)

TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR = Parameter(
    float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * 20,
    source_type="calculated",
    description="Cumulative trial-capacity-equivalent years over 20-year period",
    display_name="Cumulative Trial Capacity Years Over 20 Years",
    unit="years",
    formula="DFDA_TRIAL_CAPACITY_MULTIPLIER × 20 YEARS",
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
    source_type="calculated",
    description="Factor increase in drugs entering development when dFDA eliminates Phase 2/3 cost barrier. Valley-of-death attrition (40%) becomes new drugs, so 1 + 0.40 = 1.4× more drugs.",
    display_name="dFDA Valley of Death Rescue Multiplier",
    unit="multiplier",
    formula="1 + VALLEY_OF_DEATH_ATTRITION_PCT",    confidence="medium",
    keywords=["dfda", "valley of death", "rescue", "multiplier", "cost barrier"],
    inputs=['VALLEY_OF_DEATH_ATTRITION_PCT'],
    compute=lambda ctx: 1 + ctx["VALLEY_OF_DEATH_ATTRITION_PCT"],
    latex_symbol=r"k_{rescue}",  # LaTeX symbol for equations
)  # 1.4× more drugs when dFDA eliminates cost barrier

# Combined treatment discovery speedup from dFDA implementation
# Trial capacity multiplier × valley of death rescue multiplier
DFDA_COMBINED_TREATMENT_SPEEDUP_MULTIPLIER = Parameter(
    float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * float(DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER),
    source_type="calculated",
    description="Combined speedup factor for treatment discovery from dFDA. Trial capacity multiplier times valley of death rescue multiplier. Diseases that would take T years to get first treatment now take T/speedup years.",
    display_name="dFDA Combined Treatment Discovery Speedup Multiplier",
    unit="multiplier",
    formula="DFDA_TRIAL_CAPACITY_MULTIPLIER × DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER",
    confidence="medium",
    keywords=["dfda", "treatment", "speedup", "combined", "multiplier"],
    inputs=['DFDA_TRIAL_CAPACITY_MULTIPLIER', 'DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"] * ctx["DFDA_VALLEY_OF_DEATH_RESCUE_MULTIPLIER"],
    latex_symbol=r"k_{speedup}",  # LaTeX symbol for equations
)  # Auto-generated LaTeX from calculated value

# Rare diseases (moved here to enable calculated parameters below)
RARE_DISEASES_COUNT_GLOBAL = Parameter(
    7000,
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

# Treatment timeline acceleration from dFDA implementation (trial capacity only)
# Calculated as: Status Quo Baseline × (1 - 1/Speedup)
# Uses only trial capacity multiplier, not combined with valley of death rescue,
# because valley of death rescue adds more drug candidates but doesn't directly speed therapeutic space exploration
DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS = Parameter(
    float(STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT) * (1 - 1 / float(DFDA_TRIAL_CAPACITY_MULTIPLIER)),
    source_type="calculated",
    description="Years earlier the average first treatment arrives due to dFDA's trial capacity increase. Calculated as the status quo timeline reduced by the inverse of the capacity multiplier. Uses only trial capacity multiplier (not combined with valley of death rescue) because additional candidates don't directly speed therapeutic space exploration.",
    display_name="dFDA Treatment Timeline Acceleration",
    unit="years",
    formula="STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT × (1 - 1/DFDA_TRIAL_CAPACITY_MULTIPLIER)",
    confidence="low",
    keywords=["dfda", "acceleration", "first treatment", "timeline", "years"],
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
    source_type="calculated",
    description="Total eventually avoidable deaths from trial capacity increase alone. Represents first treatments arriving earlier due to faster therapeutic space exploration from increased trial capacity.",
    display_name="Lives Saved from Trial Capacity Increase",
    unit="deaths",
    formula="ANNUAL_DEATHS × DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS × AVOIDABLE_PCT",
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
    source_type="calculated",
    description="Total economic value from trial capacity increase alone. DALYs valued at standard economic rate.",
    display_name="Economic Value from Trial Capacity Increase",
    unit="USD",
    formula="DFDA_TRIAL_CAPACITY_DALYS_AVERTED × STANDARD_QALY_VALUE",
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
    source_type="calculated",
    description="Average years earlier patients receive treatments due to dFDA. Combines treatment timeline acceleration from increased trial capacity with efficacy lag elimination for treatments already discovered.",
    display_name="dFDA Average Total Timeline Shift",
    unit="years",
    formula="DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS + EFFICACY_LAG_YEARS",
    confidence="low",
    keywords=["dfda", "total", "timeline", "shift", "acceleration", "efficacy lag", "years", "average"],
    inputs=['DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS', 'EFFICACY_LAG_YEARS'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_TREATMENT_ACCELERATION_YEARS"] + ctx["EFFICACY_LAG_YEARS"],
    latex_symbol=r"T_{accel,max}",  # LaTeX symbol for equations
)  # ~207 years average total timeline shift from dFDA

# dFDA treatment rate (diseases getting first treatment per year)
DFDA_FIRST_TREATMENTS_PER_YEAR = Parameter(
    float(NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR) * float(DFDA_TRIAL_CAPACITY_MULTIPLIER),
    source_type="calculated",
    description="Diseases per year receiving their first effective treatment with dFDA. Scales proportionally with trial capacity multiplier.",
    display_name="dFDA New Treatments Per Year",
    unit="diseases/year",
    formula="NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR × DFDA_TRIAL_CAPACITY_MULTIPLIER",
    confidence="low",
    keywords=["dfda", "cures", "diseases", "per year", "rate", "first treatment"],
    inputs=['NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR', 'DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["NEW_DISEASE_FIRST_TREATMENTS_PER_YEAR"] * ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"],
    latex_symbol=r"Treatments_{dFDA,ann}",  # LaTeX symbol for equations
)

# Time to explore entire therapeutic space with dFDA
DFDA_QUEUE_CLEARANCE_YEARS = Parameter(
    float(STATUS_QUO_QUEUE_CLEARANCE_YEARS) / float(DFDA_TRIAL_CAPACITY_MULTIPLIER),
    source_type="calculated",
    description="Years to explore the entire therapeutic search space with dFDA implementation. At increased discovery rate, finding first treatments for all currently untreatable diseases takes ~36 years instead of ~443.",
    display_name="dFDA Therapeutic Space Exploration Time",
    unit="years",
    formula="STATUS_QUO_QUEUE_CLEARANCE_YEARS ÷ DFDA_TRIAL_CAPACITY_MULTIPLIER",
    confidence="low",
    keywords=["dfda", "queue", "clearance", "all diseases", "cure all", "years"],
    inputs=['STATUS_QUO_QUEUE_CLEARANCE_YEARS', 'DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["STATUS_QUO_QUEUE_CLEARANCE_YEARS"] / ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"],
    latex_symbol=r"T_{queue,dFDA}",  # LaTeX symbol for equations
)

# ============================================================================
# TOTAL LIVES SAVED FROM COMBINED TIMELINE SHIFT
# ============================================================================
# These parameters use the combined timeline shift from both cure acceleration
# and efficacy lag elimination.

DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED = Parameter(
    float(GLOBAL_DISEASE_DEATHS_DAILY) * float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS) * DAYS_PER_YEAR * (1 - _unavoidable_pct),
    source_type="calculated",
    description="Total eventually avoidable deaths from the combined dFDA timeline shift. Represents deaths prevented when cures arrive earlier due to both increased trial capacity and eliminated efficacy lag.",
    display_name="Total Lives Saved from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
    unit="deaths",
    formula="ANNUAL_DEATHS × DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS × AVOIDABLE_PCT",
    confidence="low",
    keywords=["total", "lives saved", "timeline shift", "cure acceleration", "efficacy lag", "average"],
    inputs=['GLOBAL_DISEASE_DEATHS_DAILY', 'DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS'],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DEATHS_DAILY"] * ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS"] * DAYS_PER_YEAR * (1 - _unavoidable_pct),
    latex_symbol=r"Lives_{max}",  # LaTeX symbol for equations
)

DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS = Parameter(
    float(GLOBAL_ANNUAL_DALY_BURDEN) * float(EVENTUALLY_AVOIDABLE_DALY_PCT) * float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_YEARS),
    source_type="calculated",
    description="Total DALYs averted from the combined dFDA timeline shift. Calculated as annual global DALY burden × eventually avoidable percentage × timeline shift years. Includes both fatal and non-fatal diseases (WHO GBD methodology).",
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
    source_type="calculated",
    description="Total economic value from the combined dFDA timeline shift. DALYs valued at standard economic rate.",
    display_name="Total Economic Benefit from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
    unit="USD",
    formula="DALYS × STANDARD_QALY_VALUE",
    confidence="low",
    keywords=["total", "economic", "value", "timeline shift", "USD"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
    latex_symbol=r"Value_{max}",  # LaTeX symbol for equations
)

DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS) * float(GLOBAL_YLD_PROPORTION_OF_DALYS) * HOURS_PER_YEAR,
    source_type="calculated",
    description="Hours of suffering eliminated from the combined dFDA timeline shift. Calculated from YLD component of DALYs (39% of total DALYs × hours per year). One-time benefit, not annual recurring.",
    display_name="Suffering Hours Eliminated from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput",
    unit="hours",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS × GLOBAL_YLD_PROPORTION × HOURS_PER_YEAR",
    confidence="low",
    keywords=["suffering", "disability", "pain", "morbidity", "quality of life", "one-time benefit", "disease burden", "trial capacity", "efficacy lag", "YLD", "hours"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS', 'GLOBAL_YLD_PROPORTION_OF_DALYS'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS"] * ctx["GLOBAL_YLD_PROPORTION_OF_DALYS"] * HOURS_PER_YEAR,
    latex_symbol=r"Hours_{suffer,max}",  # LaTeX symbol for equations
)  # ~1,875 trillion hours from full timeline shift (vs old 193T - now based on WHO YLD proportion)

# dFDA System Targets (using trial capacity multiplier)
DFDA_TRIALS_PER_YEAR_CAPACITY = Parameter(
    float(CURRENT_TRIALS_PER_YEAR) * float(DFDA_TRIAL_CAPACITY_MULTIPLIER),
    source_type="calculated",
    description="Maximum trials per year possible with trial capacity multiplier",
    display_name="Decentralized Framework for Drug Assessment Maximum Trials per Year",
    unit="trials/year",
    formula="CURRENT_TRIALS × DFDA_TRIAL_CAPACITY_MULTIPLIER",
    keywords=["pragmatic trials", "real world evidence", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect"],
    inputs=['CURRENT_TRIALS_PER_YEAR', 'DFDA_TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: ctx["CURRENT_TRIALS_PER_YEAR"] * ctx["DFDA_TRIAL_CAPACITY_MULTIPLIER"],
    latex_symbol=r"Capacity_{trials}",  # LaTeX symbol for equations
)  # Maximum trials/year possible with trial capacity multiplier

# =============================================================================
# THERAPEUTIC SPACE EXPLORATION TIMELINES
# =============================================================================
# How long to systematically test all therapeutic combinations at current vs dFDA capacity

CURRENT_KNOWN_SAFE_EXPLORATION_YEARS = Parameter(
    float(DRUG_DISEASE_COMBINATIONS_POSSIBLE) / float(CURRENT_TRIALS_PER_YEAR),
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
    source_type="calculated",
    description="Years to test all known safe drug-disease combinations with dFDA trial capacity",
    display_name="Known Safe Exploration Time (dFDA)",
    unit="years",
    formula="DRUG_DISEASE_COMBINATIONS ÷ DFDA_TRIALS_PER_YEAR",
    keywords=["exploration", "therapeutic frontier", "timeline", "dfda", "accelerated", "known safe", "years"],
    inputs=["DRUG_DISEASE_COMBINATIONS_POSSIBLE", "DFDA_TRIALS_PER_YEAR_CAPACITY"],
    compute=lambda ctx: ctx["DRUG_DISEASE_COMBINATIONS_POSSIBLE"] / ctx["DFDA_TRIALS_PER_YEAR_CAPACITY"],
    latex_symbol=r"T_{safe,dFDA}",  # LaTeX symbol for equations
)

CURRENT_TOTAL_EXPLORATION_YEARS = Parameter(
    float(TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS) / float(CURRENT_TRIALS_PER_YEAR),
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
    source_type="calculated",
    description="Years to test all therapeutic combinations (known safe + emerging modalities) with dFDA capacity",
    display_name="Total Exploration Time (dFDA)",
    unit="years",
    formula="TOTAL_COMBINATIONS ÷ DFDA_TRIALS_PER_YEAR",
    keywords=["exploration", "total", "all modalities", "timeline", "dfda", "accelerated", "years"],
    inputs=["TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS", "DFDA_TRIALS_PER_YEAR_CAPACITY"],
    compute=lambda ctx: ctx["TOTAL_TESTABLE_THERAPEUTIC_COMBINATIONS"] / ctx["DFDA_TRIALS_PER_YEAR_CAPACITY"],
    latex_symbol=r"T_{explore,dFDA}",  # LaTeX symbol for equations
)

# Combination therapy exploration (pairwise drug combinations - standard in modern medicine)
CURRENT_COMBINATION_EXPLORATION_YEARS = Parameter(
    float(COMBINATION_THERAPY_DISEASE_SPACE) / float(CURRENT_TRIALS_PER_YEAR),
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

# Population
GLOBAL_POPULATION_2024 = Parameter(
    8_000_000_000,
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

# NOTE: Daily deaths (150k/day) defined above as GLOBAL_DISEASE_DEATHS_DAILY (line ~1903)
# Annual disease deaths (from WHO global health estimates)
GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES = Parameter(
    55_000_000,
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

# Disease economic burden
GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL = Parameter(
    8_200_000_000_000,
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

# Disease cost breakdown components
GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL = Parameter(
    9_900_000_000_000,
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="external",
    description="Direct medical costs of disease globally (treatment, hospitalization, medication)",
    display_name="Global Annual Direct Medical Costs of Disease",
    unit="USD/year",
    keywords=["9.9t", "medical", "healthcare", "treatment", "hospitalization"],
    distribution="lognormal",
    confidence_interval=(7_000_000_000_000, 14_000_000_000_000),  # ±30% - global healthcare cost estimates vary widely
    latex_symbol=r"Cost_{medical,direct}",  # LaTeX symbol for equations
)  # $9.9 trillion annually

GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL = Parameter(
    5_000_000_000_000,
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="external",
    description="Annual productivity loss from disease globally (absenteeism, reduced output)",
    display_name="Global Annual Productivity Loss from Disease",
    unit="USD/year",
    keywords=["5.0t", "productivity", "lost work", "economic loss", "absenteeism"],
    distribution="lognormal",
    confidence_interval=(3_500_000_000_000, 7_000_000_000_000),  # ±30%
    latex_symbol=r"Loss_{productivity}",  # LaTeX symbol for equations
)  # $5 trillion annually

GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL = Parameter(
    94_200_000_000_000,
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="external",
    description="Economic value of human life lost to disease annually (mortality valuation)",
    display_name="Global Annual Economic Value of Human Life Lost to Disease",
    unit="USD/year",
    keywords=["94.2t", "human life", "mortality", "deaths", "dalys", "life value"],
    distribution="lognormal",
    confidence_interval=(66_000_000_000_000, 132_000_000_000_000),  # ±30%
    latex_symbol=r"Loss_{life,disease}",  # LaTeX symbol for equations
)  # $94.2 trillion annually

GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL = Parameter(
    GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL + GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL + GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL,
    source_ref=ReferenceID.DISEASE_ECONOMIC_BURDEN_109T,
    source_type="calculated",
    description="Total economic burden of disease globally (medical + productivity + mortality)",
    display_name="Total Economic Burden of Disease Globally",
    unit="USD/year",
    formula="MEDICAL_COSTS + PRODUCTIVITY_LOSS + MORTALITY_VALUE",
    keywords=["109.0t", "109.1t", "deadweight loss", "economic damage", "productivity loss", "gdp loss", "worldwide", "yearly"],
    inputs=['GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL', 'GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL', 'GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL'],
    compute=lambda ctx: ctx["GLOBAL_DISEASE_DIRECT_MEDICAL_COST_ANNUAL"] + ctx["GLOBAL_DISEASE_PRODUCTIVITY_LOSS_ANNUAL"] + ctx["GLOBAL_DISEASE_HUMAN_LIFE_VALUE_LOSS_ANNUAL"],
    latex_symbol=r"Burden_{disease}",  # LaTeX symbol for equations
)  # $109.1 trillion annually

GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL = Parameter(
    GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST + GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL + GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL,
    source_type="calculated",
    description="Total annual cost of war and disease with all externalities (direct + indirect costs for both)",
    display_name="Total Annual Cost of War and Disease with All Externalities",
    unit="USD/year",
    formula="WAR_TOTAL_COSTS + SYMPTOMATIC_TREATMENT + DISEASE_BURDEN",
    keywords=["deadweight loss", "economic damage", "productivity loss", "gdp loss", "worldwide", "yearly", "conflict"],
    inputs=['GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST', 'GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL', 'GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_DIRECT_INDIRECT_WAR_COST"] + ctx["GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL"] + ctx["GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL"],
    latex_symbol=r"Cost_{health+war}",  # LaTeX symbol for equations
)  # $128.6 trillion = $11.355T (war with externalities) + $8.2T + $109T

# Defense and research participation rates
DEFENSE_SECTOR_RETENTION_PCT = Parameter(
    0.99,
    source_ref="",
    source_type="definition",
    description="Percentage of budget defense sector keeps under 1% treaty",
    display_name="Percentage of Budget Defense Sector Keeps Under 1% treaty",
    unit="rate",
    keywords=["99%", "armed forces", "international agreement", "peace treaty", "conflict", "sector", "retention"],
    latex_symbol=r"Retain_{def}",  # LaTeX symbol for equations
)  # 99% retention

CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE = Parameter(
    0.0006,
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


US_MILITARY_SPENDING_PCT_GDP = Parameter(
    0.035,
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
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="GiveWell average cost per life saved across top charities",
    display_name="Givewell Average Cost per Life Saved Across Top Charities",
    unit="USD/life",
    keywords=["4k", "costs", "funding", "investment", "givewell", "life", "avg"],
    latex_symbol=r"Cost_{GW,avg}",  # LaTeX symbol for equations
)  # Midpoint of top charities

# Historical public health comparisons
SMALLPOX_ERADICATION_ROI = Parameter(
    280,
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
    source_type="calculated",
    description="Treaty ROI from elimination of efficacy lag plus earlier treatment discovery from increased trial throughput. Total one-time benefit divided by campaign cost. This is the primary ROI estimate for total health benefits.",
    display_name="Treaty ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput",
    unit="ratio",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_ECONOMIC_VALUE ÷ CAMPAIGN_COST",
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

PRAGMATIC_VS_NIH_EFFICIENCY_MULTIPLIER = Parameter(
    NIH_STANDARD_RESEARCH_COST_PER_QALY / PRAGMATIC_TRIAL_COST_PER_QALY,
    source_type="calculated",
    description="How many times more cost-effective pragmatic trials are vs standard NIH research. "
                "Calculated using global impact methodology (NIH cost per QALY / pragmatic cost per QALY). "
                "Shows orders-of-magnitude efficiency gap between discovery-focused pragmatic trials and standard research.",
    display_name="Pragmatic Trial Efficiency Multiplier vs NIH",
    unit="x",
    formula="NIH_COST_PER_QALY ÷ PRAGMATIC_COST_PER_QALY",
    confidence="medium",
    keywords=["efficiency", "multiplier", "pragmatic", "nih", "comparison", "cost effectiveness"],
    inputs=["NIH_STANDARD_RESEARCH_COST_PER_QALY", "PRAGMATIC_TRIAL_COST_PER_QALY"],
    compute=lambda ctx: ctx["NIH_STANDARD_RESEARCH_COST_PER_QALY"] / ctx["PRAGMATIC_TRIAL_COST_PER_QALY"],
    latex_symbol=r"k_{pragmatic:NIH}",  # LaTeX symbol for equations
)  # ~12,500x more efficient (global impact methodology)

# Cost per DALY - Primary cost-effectiveness metric
# Note: ICER (Incremental Cost-Effectiveness Ratio) is not calculated because this is a
# cost-dominant intervention that saves money while improving health. Traditional ICER
# is designed for interventions that cost money, not those that generate net economic surplus.
# Instead, we calculate cost per DALY using only the campaign cost, which understates the
# value since it ignores the $77B/year in economic benefits (R&D savings + peace dividend).

TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG = Parameter(
    TREATY_CAMPAIGN_TOTAL_COST / DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS,
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
    source_type="calculated",  # NPV calculation from funding, discount rate, and time horizon
    description="NPV of annual direct funding for the therapeutic space exploration period. Funding period equals exploration time (queue clearance years at given capacity multiplier). After exploration completes, the full timeline shift benefit is realized.",
    display_name="dFDA Direct Funding NPV (Exploration Period)",
    unit="USD",
    formula="ANNUAL_FUNDING × [(1 - (1 + r)^-T) / r] where T = exploration time",
    keywords=["philanthropy", "direct funding", "alternative", "npv", "exploration"],
    inputs=['DFDA_ANNUAL_TRIAL_FUNDING', 'NPV_DISCOUNT_RATE_STANDARD', 'DFDA_QUEUE_CLEARANCE_YEARS'],
    compute=lambda ctx: ctx["DFDA_ANNUAL_TRIAL_FUNDING"]
        * (1 - (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** -ctx["DFDA_QUEUE_CLEARANCE_YEARS"])
        / ctx["NPV_DISCOUNT_RATE_STANDARD"],
    latex_symbol=r"NPV_{direct}",  # LaTeX symbol for equations
    latex=r"NPV_{direct} = Funding_{ann} \times \frac{1 - (1+r)^{-T}}{r}",  # PV of annuity formula
)  # ~$541.9B NPV

# Cost per DALY for direct funding scenario
DFDA_DIRECT_FUNDING_COST_PER_DALY = Parameter(
    DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV / DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_DALYS,
    source_type="calculated",  # Derived from NPV and DALYs
    description="Cost per DALY at direct funding level for the therapeutic space exploration period. Still highly cost-effective vs bed nets.",
    display_name="dFDA Direct Funding Cost per DALY",
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

# Treaty campaign leverage vs direct funding
TREATY_VS_DIRECT_FUNDING_LEVERAGE = Parameter(
    DFDA_DIRECT_FUNDING_COST_PER_DALY / TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
    source_type="calculated",  # Ratio of cost per DALY metrics
    description="How many times more cost-effective the treaty campaign is vs direct funding. Treaty campaign unlocks government funding at scale, avoiding need for philanthropists/NIH to directly commit equivalent amounts. Both approaches achieve same DALY timeline shift benefit. Treaty spreads cost across governments while building sustainable public funding infrastructure.",
    display_name="Treaty Campaign Leverage vs Direct Funding",
    unit="x",
    formula="DFDA_DIRECT_FUNDING_COST_PER_DALY ÷ TREATY_COST_PER_DALY",    confidence="high",
    keywords=["leverage", "campaign effectiveness", "treaty advantage", "cost comparison", "therapeutic space"],
    inputs=['DFDA_DIRECT_FUNDING_COST_PER_DALY', 'TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG'],
    compute=lambda ctx: ctx["DFDA_DIRECT_FUNDING_COST_PER_DALY"] / ctx["TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG"],
    latex_symbol=r"Leverage_{treaty}",  # LaTeX symbol for equations
)  # ~542× - treaty campaign achieves massive leverage

# Cost-effectiveness multipliers vs. bed nets
TREATY_VS_BED_NETS_MULTIPLIER = Parameter(
    BED_NETS_COST_PER_DALY / TREATY_COST_PER_DALY_TRIAL_CAPACITY_PLUS_EFFICACY_LAG,
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

GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT = Parameter(
    0.035,
    source_ref=ReferenceID.N3_5_RULE,
    source_type="external",
    description="Critical mass threshold for social change (3.5% rule)",
    display_name="Critical Mass Threshold for Social Change",
    unit="rate",
    hide_ci=True,  
    confidence_interval=(0.025, 0.045),  # Range 2.5-4.5% based on different studies
    distribution="lognormal",
    keywords=["4%", "people", "worldwide", "citizens", "individuals", "inhabitants", "persons"],
    latex_symbol=r"Threshold_{activism}",  # LaTeX symbol for equations
)  # 3.5% rule for social change, key tipping point

TREATY_CAMPAIGN_VOTING_BLOC_TARGET = Parameter(
    GLOBAL_POPULATION_2024 * GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT,
    source_type="calculated",
    description="Target voting bloc size for campaign (3.5% of global population - critical mass for social change)",
    display_name="Target Voting Bloc Size for Campaign",
    unit="of people",
    formula="GLOBAL_POPULATION × 3.5%",
    keywords=["280.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"],
    inputs=['GLOBAL_POPULATION_2024', 'GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT'],
    compute=lambda ctx: ctx["GLOBAL_POPULATION_2024"] * ctx["GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT"],
    latex_symbol=r"N_{voters,target}",  # LaTeX symbol for equations
    hide_ci=True,  # CI clutters display for this target figure
)  # 280M people = 3.5% of 8B (critical mass threshold)

# Per-voter impact (total impact ÷ voting bloc target)
# Used in podcast outro CTA and campaign materials
VOTER_LIVES_SAVED = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED) / float(TREATY_CAMPAIGN_VOTING_BLOC_TARGET),
    source_type="calculated",
    description="Lives saved attributable to each voter if the treaty passes (total lives saved ÷ 3.5% voting bloc target)",
    display_name="Lives Saved per Voter",
    unit="lives",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED ÷ TREATY_CAMPAIGN_VOTING_BLOC_TARGET",
    keywords=["per voter", "individual impact", "lives saved", "CTA", "campaign"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED', 'TREATY_CAMPAIGN_VOTING_BLOC_TARGET'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_LIVES_SAVED"] / ctx["TREATY_CAMPAIGN_VOTING_BLOC_TARGET"],
    latex_symbol=r"Lives_{voter}",
)

VOTER_SUFFERING_HOURS_PREVENTED = Parameter(
    float(DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS) / float(TREATY_CAMPAIGN_VOTING_BLOC_TARGET),
    source_type="calculated",
    description="Hours of suffering prevented attributable to each voter if the treaty passes (total suffering hours ÷ 3.5% voting bloc target)",
    display_name="Suffering Hours Prevented per Voter",
    unit="hours",
    formula="DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS ÷ TREATY_CAMPAIGN_VOTING_BLOC_TARGET",
    keywords=["per voter", "individual impact", "suffering", "CTA", "campaign"],
    inputs=['DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS', 'TREATY_CAMPAIGN_VOTING_BLOC_TARGET'],
    compute=lambda ctx: ctx["DFDA_TRIAL_CAPACITY_PLUS_EFFICACY_LAG_SUFFERING_HOURS"] / ctx["TREATY_CAMPAIGN_VOTING_BLOC_TARGET"],
    latex_symbol=r"Hours_{suffer,voter}",
)

# Historical & Comparison Multipliers
MILITARY_VS_MEDICAL_RESEARCH_RATIO = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_MED_RESEARCH_SPENDING,
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

POST_WW2_MILITARY_CUT_PCT = Parameter(
    0.30,
    source_ref=ReferenceID.US_POST_WWII_MILITARY_SPENDING_CUT,
    source_type="external",
    description="Percentage military spending cut after WW2 (historical precedent)",
    display_name="Percentage Military Spending Cut After WW2",
    unit="rate",
    keywords=["30%", "dod", "pentagon", "national security", "army", "navy", "armed forces"],
    latex_symbol=r"Cut_{WW2}",  # LaTeX symbol for equations
)  # Percentage military spending cut after WW2, historical precedent

SWITZERLAND_DEFENSE_SPENDING_PCT = Parameter(
    0.007,
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
    source_type="definition",
    description="Maximum bond investment for lobbyist incentives",
    display_name="Maximum Bond Investment for Lobbyist Incentives",
    unit="USD",
    keywords=["20.0m", "social impact bond", "sib", "impact investing", "pay for success", "capital", "finance"],
    latex_symbol=r"Invest_{lobby,max}",  # LaTeX symbol for equations
)  # Millions USD, bond investment for lobbyists (max incentive)

LOBBYIST_SALARY_MIN_K = Parameter(
    500_000,
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
    Calculate GDP growth boost from military spending redirection

    Historical evidence:
    - Post-WW2: 30% military cut → 8% annual GDP growth for a decade (vs 2-3% normal)
    - Post-Cold War: 3% military cut → 1990s boom with 2.5% productivity surge

    Model: Each 1% reduction in military spending → ~0.25% GDP growth boost
    This is conservative given historical evidence shows larger effects.

    Formula:
        GDP_{growth} = GDP_{base} + treaty_{pct} \times multiplier

    LaTeX:
        GDP_{growth} = 0.025 + treaty_{pct} \times 0.25

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)

    Returns:
        Total annual GDP growth rate (baseline + boost)
    """
    BASE_GDP_GROWTH = 0.025  # 2.5% baseline global growth
    MULTIPLIER_EFFECT = 0.25  # Conservative: 1% military cut → 0.25% GDP boost

    boost = treaty_pct * MULTIPLIER_EFFECT
    return BASE_GDP_GROWTH + boost


def calculate_trial_capacity_multiplier(treaty_pct: float) -> float:
    """
    Calculate trial capacity multiplier for a given treaty percentage.

    Uses linear scaling from the base DFDA_TRIAL_CAPACITY_MULTIPLIER at 1% treaty.

    Formula:
        Multiplier = DFDA_TRIAL_CAPACITY_MULTIPLIER × (treaty_pct / 0.01)

    Examples (assuming base multiplier of 9.53x):
    - 1% treaty: 9.53 × (0.01 / 0.01) = 9.53x
    - 2% treaty: 9.53 × (0.02 / 0.01) = 19.1x
    - 5% treaty: 9.53 × (0.05 / 0.01) = 47.7x
    - 10% treaty: 9.53 × (0.10 / 0.01) = 95.3x

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)

    Returns:
        Trial capacity multiplier (scales with treaty percentage)
    """
    return float(DFDA_TRIAL_CAPACITY_MULTIPLIER) * (treaty_pct / 0.01)


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
# IMPROVED PERSONAL LIFETIME WEALTH MODEL
# ---
# This section implements improvements identified in methodology review

# Constants for improved healthcare savings model
US_CHRONIC_DISEASE_SPENDING_ANNUAL = Parameter(
    4.1e12,
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
    display_name="US Population in 2024",
    keywords=["2024", "335.0m", "people", "citizens", "individuals", "inhabitants", "persons"],
    distribution="lognormal",
    confidence_interval=(330e6, 340e6),  # ±1.5% - census estimates well-known
    latex_symbol=r"Pop_{US}",  # LaTeX symbol for equations
)

PER_CAPITA_CHRONIC_DISEASE_COST = Parameter(
    US_CHRONIC_DISEASE_SPENDING_ANNUAL / US_POPULATION_2024,
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
    latex=r"Wealth_{lifetime} = T_{extend} \times Value_{QALY}",
)


# Years of life lost per death by category
# Source: Cancer YLL studies, cardiovascular burden research
YEARS_LOST_PER_DEATH = {
    "cardiovascular": 12.0,  # Similar to cancer
    "cancer": 13.5,  # Average 14.9 women, 12.7 men
    "respiratory": 8.0,  # Older age deaths
    "neurodegenerative": 6.0,  # Very old age deaths
    "metabolic": 10.0,  # Middle age deaths
    "infectious": 15.0,  # Can affect all ages
    "accidents": 35.0,  # Often young people
    "aging_related": 3.0,  # Very old age, natural limits
    "other": 10.0,  # Mixed
}


def calculate_cumulative_research_years(treaty_pct: float, years_elapsed: float) -> float:
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
    multiplier = calculate_trial_capacity_multiplier(treaty_pct)
    return multiplier * years_elapsed


def calculate_disease_eradication_rate(category: str, cumulative_research_years: float, conservative: bool = False) -> float:
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


def calculate_life_extension_from_eradication(treaty_pct: float, years_elapsed: float, conservative: bool = False) -> dict[str, Any]:
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
        new_cure_rate = calculate_disease_eradication_rate(category, cumulative_research, conservative)

        # Improvement in cure rate
        cure_rate_improvement = new_cure_rate - current_cure_rate

        # Life extension from this category
        # If we cure X% more of a disease that causes Y% of deaths
        # and each death loses Z years, we gain: X * Y * Z years
        category_life_extension = cure_rate_improvement * burden_pct * years_lost_per_death

        total_life_extension += category_life_extension

        disease_details[category] = {
            "burden_pct": burden_pct,
            "current_cure_rate": current_cure_rate,
            "new_cure_rate": new_cure_rate,
            "improvement": cure_rate_improvement,
            "years_lost_per_death": years_lost_per_death,
            "life_extension_contribution": category_life_extension,
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
        "total_life_extension": total_life_extension,
        "disease_life_extension": total_life_extension - aging_reversal_bonus,
        "aging_reversal_bonus": aging_reversal_bonus,
        "cumulative_research_years": cumulative_research,
        "years_elapsed": years_elapsed,
        "disease_details": disease_details,
        "model_type": "disease_eradication",
        "conservative": conservative,
    }


def calculate_personal_lifetime_wealth_disease_eradication(
    treaty_pct: float = TREATY_REDUCTION_PCT,
    current_age: int = 30,
    baseline_life_expectancy: int = 80,
    annual_income: float = 50000,
    discount_rate: float = 0.03,
    years_elapsed: float = 5,
    conservative: bool = False,
) -> dict[str, Any]:
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
    eradication_result = calculate_life_extension_from_eradication(treaty_pct, years_elapsed, conservative)
    life_extension_years = eradication_result["total_life_extension"]

    # Medical progress multiplier for other calculations
    progress_multiplier = calculate_trial_capacity_multiplier(treaty_pct)

    # Peace dividend (same as other models)
    peace_dividend_per_capita_annual = PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT / GLOBAL_POPULATION_2024
    years_remaining = baseline_life_expectancy - current_age
    total_years = years_remaining + life_extension_years

    # GDP boost for compounding calculations
    gdp_boost = calculate_gdp_growth_boost(treaty_pct)

    # Healthcare savings (disease eradication approach)
    # As diseases are eradicated, healthcare costs drop
    # Average reduction proportional to cure rate improvement across all categories
    avg_cure_improvement = sum(
        detail["improvement"] * detail["burden_pct"] for detail in eradication_result["disease_details"].values()
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
    # FIXED: Only calculate boost for years_remaining to avoid double-counting extended years
    # (Extended years are fully captured in the extended_earnings component)
    baseline_growth = 0.025  # Baseline economic growth without treaty

    # Calculate incremental benefit from faster growth over baseline lifespan only
    gdp_boost_benefit = 0
    for t in range(1, int(years_remaining) + 1):
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
        "cumulative_research_years": eradication_result["cumulative_research_years"],
        "gdp_growth_boost": gdp_boost - 0.025,
        "medical_progress_multiplier": progress_multiplier,
        "eradication_details": eradication_result["disease_details"],
        "model_type": "disease_eradication",
        "years_elapsed": years_elapsed,
        "conservative": conservative,
    }


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

GLOBAL_HOUSEHOLD_WEALTH_USD = Parameter(
    454e12,
    source_ref=ReferenceID.CS_GLOBAL_WEALTH_REPORT_2023,
    source_type="external",
    description="Total global household wealth (2022/2023 estimate)",
    display_name="Global Household Wealth",
    unit="USD",
    keywords=["wealth", "household", "global", "assets", "capital"],
    latex_symbol=r"Wealth_{household}",  # LaTeX symbol for equations
)  # $454T

CONCENTRATED_INTEREST_SECTOR_MARKET_CAP_USD = Parameter(
    5e12,
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

