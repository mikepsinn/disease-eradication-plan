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
            source_ref="knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex",
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
        'distribution', 'inputs', 'compute'
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
# Source: brain/book/problem/cost-of-war.qmd
# Reference: references.qmd#total-military-and-war-costs-11-4t

# Direct costs
GLOBAL_MILITARY_SPENDING_ANNUAL_2024 = Parameter(
    2_718_000_000_000,
    source_ref=ReferenceID.GLOBAL_MILITARY_SPENDING,
    source_type="external",
    description="Global military spending in 2024",
    display_name="Global Military Spending in 2024",
    unit="USD",
    distribution=DistributionType.LOGNORMAL,
    std_error=271_800_000_000,  # Assumed 10% uncertainty
    confidence_interval=(2_446_000_000_000, 2_990_000_000_000),
    keywords=["2024", "2.7t", "dod", "pentagon", "national security", "army", "navy"]
)  # SIPRI 2024

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
    keywords=["10.0m", "low estimate", "cautious", "pessimistic", "worst case", "conservative", "underestimate"]
)  # US DOT uses $13.6M, we use $10M conservatively

# Conflict death breakdown (for QALY calculations)
# Source: brain/book/problem/cost-of-war.qmd#death-accounting
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
)  # Uppsala Conflict Data Program

# Total conflict deaths (calculated from breakdown)
GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS
    + GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE,
    source_ref="/knowledge/problem/cost-of-war.qmd#death-accounting",
    source_type="calculated",
    description="Total annual conflict deaths globally (sum of combat, terror, state violence)",
    display_name="Total Annual Conflict Deaths Globally",
    unit="deaths/year",
    formula="COMBAT + TERROR + STATE_VIOLENCE",
    latex=r"Deaths_{total} = 233,600 \text{ (combat)} + 8,300 \text{ (terror)} + 2,700 \text{ (state)} = 244,600",
    keywords=["worldwide", "yearly", "fatalities", "casualties", "mortality", "armed conflict", "loss of life"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT', 'GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE', 'GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT"]
    + ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS"]
    + ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE"],
)  # 244,600

# Breakdown of Human Life Loss Costs (billions USD)
GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT * VALUE_OF_STATISTICAL_LIFE,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Annual cost of combat deaths (deaths × VSL)",
    display_name="Annual Cost of Combat Deaths",
    unit="USD/year",
    formula="COMBAT_DEATHS × VSL ",
    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "mortality"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT', 'VALUE_OF_STATISTICAL_LIFE'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_ACTIVE_COMBAT"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
)  # $2,336B

GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS * VALUE_OF_STATISTICAL_LIFE,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Annual cost of terror deaths (deaths × VSL)",
    display_name="Annual Cost of Terror Deaths",
    unit="USD/year",
    formula="TERROR_DEATHS × VSL ",
    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "mortality"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS', 'VALUE_OF_STATISTICAL_LIFE'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TERROR_ATTACKS"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
)  # $83B

GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE * VALUE_OF_STATISTICAL_LIFE,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Annual cost of state violence deaths (deaths × VSL)",
    display_name="Annual Cost of State Violence Deaths",
    unit="USD/year",
    formula="STATE_DEATHS × VSL ",
    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "mortality"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE', 'VALUE_OF_STATISTICAL_LIFE'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_STATE_VIOLENCE"] * ctx["VALUE_OF_STATISTICAL_LIFE"],
)  # $27B

# Total human life losses (calculated from breakdown)
GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT = Parameter(
    GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT
    + GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS
    + GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE,
    source_ref="/knowledge/problem/cost-of-war.qmd#human-cost",
    source_type="calculated",
    description="Total annual human life losses from conflict (sum of combat, terror, state violence)",
    display_name="Total Annual Human Life Losses from Conflict",
    unit="USD/year",
    formula="COMBAT_COST + TERROR_COST + STATE_VIOLENCE_COST",
    latex=r"Cost_{human} = \$2,336B \text{ (combat)} + \$83B \text{ (terror)} + \$27B \text{ (state)} = \$2,446B",
    keywords=["worldwide", "yearly", "human", "life", "losses", "armed conflict", "military action"],
    inputs=['GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT', 'GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE', 'GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_HUMAN_COST_ACTIVE_COMBAT"]
    + ctx["GLOBAL_ANNUAL_HUMAN_COST_TERROR_ATTACKS"]
    + ctx["GLOBAL_ANNUAL_HUMAN_COST_STATE_VIOLENCE"],
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
    display_name="Total Annual Infrastructure Destruction",
    unit="USD/year",
    formula="TRANSPORT + ENERGY + COMMS + WATER + EDUCATION + HEALTHCARE",
    latex=r"Infra_{damage} = \$487B \text{ (trans)} + \$422B \text{ (nrg)} + \$298B \text{ (comms)} + \$268B \text{ (water)} + \$235B \text{ (edu)} + \$166B \text{ (hlth)} = \$1,875B",
    keywords=["worldwide", "yearly", "infrastructure", "destruction", "armed conflict", "military action", "international"],
    inputs=['GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_TRANSPORTATION_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_ENERGY_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_COMMUNICATIONS_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_WATER_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_EDUCATION_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DAMAGE_HEALTHCARE_CONFLICT"],
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
    display_name="Total Annual Trade Disruption",
    unit="USD/year",
    formula="SHIPPING + SUPPLY_CHAIN + ENERGY_PRICE + CURRENCY",
    latex=r"Trade_{disruption} = \$247B \text{ (ship)} + \$187B \text{ (supply)} + \$125B \text{ (nrg)} + \$57B \text{ (curr)} = \$616B",
    keywords=["worldwide", "yearly", "trade", "disruption", "armed conflict", "military action", "international"],
    inputs=['GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_SHIPPING_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_SUPPLY_CHAIN_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_ENERGY_PRICE_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_CURRENCY_CONFLICT"],
)  # $616B

GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024
    + GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT
    + GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT
    + GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT,
    source_ref="/knowledge/problem/cost-of-war.qmd#direct-costs",
    source_type="calculated",
    description="Total annual direct war costs (military spending + infrastructure + human life + trade disruption)",
    display_name="Total Annual Direct War Costs",
    unit="USD/year",
    formula="MILITARY + INFRASTRUCTURE + HUMAN_LIFE + TRADE",
    latex=r"DirectCosts = \$2,718B \text{ (mil)} + \$1,875B \text{ (infra)} + \$2,446B \text{ (human)} + \$616B \text{ (trade)} = \$7,655B",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "worldwide"],
    inputs=['GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT', 'GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT', 'GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT', 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"]
    + ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT"],
)  # $7,655B

# Indirect costs
GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING = Parameter(
    2_718_000_000_000,
    source_ref=ReferenceID.DISPARITY_RATIO_WEAPONS_VS_CURES,
    source_type="external",
    description="Annual lost economic growth from military spending opportunity cost",
    display_name="Annual Lost Economic Growth from Military Spending Opportunity Cost",
    unit="USD",
    keywords=["2.7t", "dod", "pentagon", "national security", "army", "navy", "armed forces"],
    distribution="lognormal",
    confidence_interval=(1_900_000_000_000, 3_800_000_000_000),  # ±30% - opportunity cost estimates vary
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
    display_name="Total Annual Indirect War Costs",
    unit="USD/year",
    formula="OPPORTUNITY + VETERANS + REFUGEES + ENVIRONMENT + MENTAL_HEALTH + LOST_CAPITAL",
    latex=r"IndirectCosts = \$2.7T \text{ (opp cost)} + \$200B \text{ (vet)} + \$150B \text{ (ref)} + \$100B \text{ (env)} + \$232B \text{ (ptsd)} + \$300B \text{ (hum cap)} = \$3.7T",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "worldwide"],
    inputs=['GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT', 'GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING', 'GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT', 'GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT', 'GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS', 'GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING"]
    + ctx["GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS"]
    + ctx["GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS"]
    + ctx["GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT"]
    + ctx["GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT"],
)  # $3,700.1B

# Grand total war costs
GLOBAL_ANNUAL_WAR_TOTAL_COST = Parameter(
    GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL + GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL,
    source_ref="/knowledge/problem/cost-of-war.qmd#total-cost",
    source_type="calculated",
    description="Total annual cost of war worldwide (direct + indirect costs)",
    display_name="Total Annual Cost of War Worldwide",
    unit="USD/year",
    formula="DIRECT_COSTS + INDIRECT_COSTS",
    latex=r"TotalWarCost = \$7,655B \text{ (direct)} + \$3,700B \text{ (indirect)} = \$11,355B",
    keywords=["worldwide", "yearly", "conflict", "costs", "funding", "investment", "war"],
    # Uncertainty derived from inputs (DIRECT + INDIRECT costs)
    validation_min=8_000_000_000_000,   # Floor: Direct costs only, conservative VSL
    validation_max=16_000_000_000_000,  # Ceiling: Including all indirect/long-term costs
    inputs=["GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL", "GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL"] + ctx["GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL"]
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
)  # Core treaty definition - the 1% is our proposal, not derived from external data

TREATY_ANNUAL_FUNDING = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * TREATY_REDUCTION_PCT,
    source_ref="",
    source_type="definition",
    description="Annual funding from 1% of global military spending redirected to DIH",
    display_name="Annual Funding from 1% of Global Military Spending Redirected to DIH",
    unit="USD/year",
    formula="MILITARY_SPENDING × 1%",
    keywords=["1%", "dod", "pentagon", "distributed research", "global research", "national security", "open science"],
    inputs=['GLOBAL_MILITARY_SPENDING_ANNUAL_2024', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] * ctx["TREATY_REDUCTION_PCT"],
)  # $27.18B

# ==============================================================================
# PEACE DIVIDEND - RECURRING ANNUAL BENEFIT ($113.55B/year perpetual)
# ==============================================================================
# A 1% treaty redirects 1% of military spending ($27.18B/year) to medical research.
# This generates recurring annual benefits from reduced conflict costs:
#   - Direct military savings
#   - Reduced infrastructure destruction
#   - Fewer casualties and refugee costs
#   - Reduced lost economic growth
# Total recurring peace dividend: $113.55B/year (happens every year forever)
# ==============================================================================

PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/appendix/peace-dividend-calculations.qmd",
    source_type="calculated",
    description="Annual peace dividend from 1% reduction in total war costs",
    display_name="Annual Peace Dividend from 1% Reduction in Total War Costs",
    unit="USD/year",
    formula="TOTAL_WAR_COST × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "yearly", "armistice", "ceasefire", "conflict"],
    # Uncertainty derived from inputs (WAR_COST × REDUCTION_PCT)
    validation_min=70_000_000_000,   # Floor: Conservative war cost estimates, 50% realization
    validation_max=180_000_000_000,  # Ceiling: Including all indirect costs, full compliance
    inputs=["GLOBAL_ANNUAL_WAR_TOTAL_COST", "TREATY_REDUCTION_PCT"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_TOTAL_COST"] * ctx["TREATY_REDUCTION_PCT"]
)  # $113.55B, rounded to $114B

# Individual peace dividend components (1% savings breakdown)
PEACE_DIVIDEND_DIRECT_COSTS = Parameter(
    GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in direct war costs",
    display_name="Annual Savings from 1% Reduction in Direct War Costs",
    unit="USD/year",
    formula="DIRECT_COSTS × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "conflict"],
    inputs=['GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_DIRECT_COSTS_TOTAL"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_INFRASTRUCTURE = Parameter(
    GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in infrastructure destruction",
    display_name="Annual Savings from 1% Reduction in Infrastructure Destruction",
    unit="USD/year",
    formula="INFRASTRUCTURE_DESTRUCTION × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_INFRASTRUCTURE_DESTRUCTION_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_HUMAN_CASUALTIES = Parameter(
    GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in human casualties",
    display_name="Annual Savings from 1% Reduction in Human Casualties",
    unit="USD/year",
    formula="HUMAN_LIFE_LOSSES × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_HUMAN_LIFE_LOSSES_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_TRADE_DISRUPTION = Parameter(
    GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in trade disruption",
    display_name="Annual Savings from 1% Reduction in Trade Disruption",
    unit="USD/year",
    formula="TRADE_DISRUPTION × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_TRADE_DISRUPTION_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_INDIRECT_COSTS = Parameter(
    GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in indirect war costs",
    display_name="Annual Savings from 1% Reduction in Indirect War Costs",
    unit="USD/year",
    formula="INDIRECT_COSTS × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "conflict"],
    inputs=['GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_INDIRECT_COSTS_TOTAL"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_LOST_ECONOMIC_GROWTH = Parameter(
    GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in lost economic growth",
    display_name="Annual Savings from 1% Reduction in Lost Economic Growth",
    unit="USD/year",
    formula="LOST_ECONOMIC_GROWTH × 1%",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict resolution"],
    inputs=['GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_LOST_ECONOMIC_GROWTH_MILITARY_SPENDING"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_VETERAN_HEALTHCARE = Parameter(
    GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in veteran healthcare costs",
    display_name="Annual Savings from 1% Reduction in Veteran Healthcare Costs",
    unit="USD/year",
    formula="VETERAN_HEALTHCARE × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_VETERAN_HEALTHCARE_COSTS"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_REFUGEE_SUPPORT = Parameter(
    GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in refugee support costs",
    display_name="Annual Savings from 1% Reduction in Refugee Support Costs",
    unit="USD/year",
    formula="REFUGEE_SUPPORT × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_REFUGEE_SUPPORT_COSTS"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_ENVIRONMENTAL = Parameter(
    GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in environmental damage",
    display_name="Annual Savings from 1% Reduction in Environmental Damage",
    unit="USD/year",
    formula="ENVIRONMENTAL_DAMAGE × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_ENVIRONMENTAL_DAMAGE_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_PTSD = Parameter(
    GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in PTSD and mental health costs",
    display_name="Annual Savings from 1% Reduction in PTSD and Mental Health Costs",
    unit="USD/year",
    formula="PTSD_COSTS × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_PSYCHOLOGICAL_IMPACT_COSTS_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
)

PEACE_DIVIDEND_LOST_HUMAN_CAPITAL = Parameter(
    GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/economics/peace-dividend.qmd",
    source_type="calculated",
    description="Annual savings from 1% reduction in lost human capital",
    display_name="Annual Savings from 1% Reduction in Lost Human Capital",
    unit="USD/year",
    formula="LOST_HUMAN_CAPITAL × 1%",
    keywords=["conflict resolution", "international agreement", "peace treaty", "armistice", "benefit", "ceasefire", "non-violence"],
    inputs=['GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_LOST_HUMAN_CAPITAL_CONFLICT"] * ctx["TREATY_REDUCTION_PCT"],
)

# Separate peace dividend into confidence levels
PEACE_DIVIDEND_DIRECT_FISCAL_SAVINGS = Parameter(
    float(TREATY_ANNUAL_FUNDING),
    source_ref=ReferenceID.SIPRI_2024_SPENDING,
    source_type="definition",  # This is a policy-derived value (1% of military spending)
    confidence="high",
    formula="TREATY_ANNUAL_FUNDING",
    latex=r"PeaceDividend_{fiscal} = \$27.18B",
    description="Direct fiscal savings from 1% military spending reduction (high confidence)",
    display_name="Direct Fiscal Savings from 1% Military Spending Reduction",
    unit="USD/year",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict resolution"],
)

PEACE_DIVIDEND_CONFLICT_REDUCTION = Parameter(
    float(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT) - float(TREATY_ANNUAL_FUNDING),
    source_ref="calculated",
    source_type="calculated",
    confidence="low",
    formula="PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT - TREATY_ANNUAL_FUNDING",
    latex=r"PeaceDividend_{conflict} = \$113.55B - \$27.18B = \$86.37B",
    description="Conflict reduction benefits from 1% less military spending (lower confidence - assumes proportional relationship)",
    display_name="Conflict Reduction Benefits from 1% Less Military Spending",
    unit="USD/year",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict resolution"],
    inputs=['PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT', 'TREATY_ANNUAL_FUNDING'],
    compute=lambda ctx: float(ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"]) - float(ctx["TREATY_ANNUAL_FUNDING"]),
)

# ---
# HEALTH DIVIDEND PARAMETERS (dFDA)
# ---

# Clinical trial market
# Source: brain/book/appendix/dfda-roi-calculations.qmd
GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL = Parameter(
    83_000_000_000,
    source_ref=ReferenceID.GLOBAL_CLINICAL_TRIALS_MARKET_2024,
    source_type="external",
    description="Annual global spending on clinical trials",
    display_name="Annual Global Spending on Clinical Trials",
    unit="USD/year",
    distribution=DistributionType.LOGNORMAL,
    std_error=12_500_000_000,  # 15% uncertainty (widened from 10%)
    confidence_interval=(70_000_000_000, 97_000_000_000),  # $70B-$97B (±15%)
    # Economist rationale: Market research varies significantly across sources:
    # GlobalData: $68B-$78B, IQVIA: $80B-$90B, Grand View Research: $85B-$95B.
    # Using $83B midpoint ±15% spans full source range. Right-skewed distribution
    # because large pharma trials (oncology, rare disease) drive high-cost tail.
    # CRITICAL: R&D savings directly proportional to market size—15% variance here
    # translates to ±$6B uncertainty in DFDA gross savings ($41.5B baseline).
    validation_min=60_000_000_000,   # Floor: Core Phase 2/3 trials only
    validation_max=110_000_000_000,  # Ceiling: Including Phase 4, observational, registries
    keywords=["83.0b", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "worldwide"]
)  # $83B spent globally on clinical trials annually

TRIAL_COST_REDUCTION_PCT = Parameter(
    0.50,
    source_ref="",
    source_type="definition",
    description="Trial cost reduction percentage (50% baseline, conservative)",
    display_name="dFDA Trial Cost Reduction Percentage",
    unit="rate",
    distribution=DistributionType.BETA,  # Beta distribution mandatory for [0,1] bounded probabilities
    confidence_interval=(0.40, 0.65),  # 40-65% reduction range (widened from 30-70%)
    # Economist rationale: Evidence-based range from published trials:
    # RECOVERY trial: 80% cost reduction (£2.70/patient vs £13.50 traditional RCT)
    # Decentralized Clinical Trials (DCTs): 30-50% reduction (NEJM, JAMA literature)
    # Pragmatic trials: 50-70% reduction (NIH Collaboratory, PCORI evidence)
    # Using 50% ±10pp (40-60%) as pragmatic midpoint across trial types.
    # CRITICAL: Beta distribution captures bounded uncertainty—can't exceed 100% or go negative.
    # Asymmetric risk: easier to underperform (regulatory resistance, adoption lag) than overperform.
    validation_min=0,    # Floor: No cost reduction (regulatory capture)
    validation_max=1,    # Ceiling: 100% reduction (theoretical maximum)
    keywords=["50%", "rct", "clinical study", "clinical trial", "low estimate", "research trial", "randomized controlled trial"]
)  # 50% baseline reduction (conservative)

TRIAL_COST_REDUCTION_FACTOR = Parameter(
    82,
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="external",
    description="Cost reduction factor demonstrated by RECOVERY trial",
    display_name="Cost Reduction Factor Demonstrated by Recovery Trial",
    unit="ratio",
    distribution=DistributionType.LOGNORMAL,
    std_error=20,  # High variance in applicability
    confidence_interval=(20, 150),
    keywords=["rct", "multiple", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research"]
)  # 82x reduction proven by RECOVERY trial

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
)  # Global clinical trials per year

CURRENT_DRUG_APPROVALS_PER_YEAR = Parameter(
    50,
    source_ref=ReferenceID.GLOBAL_NEW_DRUG_APPROVALS_50_ANNUALLY,
    source_type="external",
    description="Average annual new drug approvals globally",
    display_name="Average Annual New Drug Approvals Globally",
    unit="drugs/year",
    keywords=["worldwide", "yearly", "current", "drug", "approvals", "year", "earth"]
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
    keywords=["recovery", "covid", "trial", "timeline", "duration", "oxford", "pragmatic"]
)

FDA_PHASE_1_TO_APPROVAL_YEARS = Parameter(
    9.1,
    source_ref=ReferenceID.FDA_APPROVAL_TIMELINE_10_YEARS,
    source_type="external",
    description="FDA timeline from Phase 1 start to approval (Phase 1-3 + NDA review)",
    display_name="FDA Phase 1 to Approval Timeline",
    unit="years",
    confidence="high",
    distribution=DistributionType.GAMMA,
    std_error=2.0,  # Timeline variation
    confidence_interval=(6.0, 12.0),
    keywords=["fda", "clinical", "development", "timeline", "approval", "phase 1", "phase 2", "phase 3"]
)  # Clinical development + NDA review: ~9 years (per FDA references)

POST_1962_DRUG_APPROVAL_REDUCTION_PCT = Parameter(
    0.70,
    source_ref=ReferenceID.POST_1962_DRUG_APPROVAL_DROP,
    source_type="external",
    description="Reduction in new drug approvals after 1962 Kefauver-Harris Amendment (70% drop from 43→17 drugs/year)",
    display_name="Post-1962 Drug Approval Reduction",
    unit="percentage",
    confidence="high",
    last_updated="1962-1970",
    keywords=["kefauver", "harris", "amendment", "1962", "regulation", "fda", "approval", "drop", "decline"]
)

FDA_TO_OXFORD_RECOVERY_TRIAL_TIME_MULTIPLIER = Parameter(
    (FDA_PHASE_1_TO_APPROVAL_YEARS * MONTHS_PER_YEAR) / OXFORD_RECOVERY_TRIAL_DURATION_MONTHS,
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="calculated",
    description="FDA approval timeline vs Oxford RECOVERY trial (9.1 years ÷ 3 months = 36x slower)",
    display_name="FDA to Oxford RECOVERY Trial Time Multiplier",
    unit="ratio",
    formula="FDA_PHASE_1_TO_APPROVAL_YEARS × MONTHS_PER_YEAR ÷ OXFORD_RECOVERY_TRIAL_DURATION_MONTHS",
    latex=r"\frac{9.1 \text{ years} \times 12 \text{ months/year}}{3 \text{ months}} = 36.4",
    confidence="high",
    keywords=["recovery", "covid", "trial", "fda", "timeline", "comparison", "speed", "multiplier", "oxford"],
    inputs=['FDA_PHASE_1_TO_APPROVAL_YEARS', 'OXFORD_RECOVERY_TRIAL_DURATION_MONTHS'],
    compute=lambda ctx: (ctx["FDA_PHASE_1_TO_APPROVAL_YEARS"] * MONTHS_PER_YEAR) / ctx["OXFORD_RECOVERY_TRIAL_DURATION_MONTHS"],
)

PRE_1962_PHYSICIAN_COUNT = Parameter(
    144_000,
    source_ref=ReferenceID.PRE_1962_PHYSICIAN_TRIALS,
    source_type="external",
    description="Estimated physicians conducting real-world efficacy trials pre-1962 (unverified estimate)",
    display_name="Pre-1962 Physician Count (Unverified)",
    unit="physicians",
    confidence="low",
    keywords=["pre-1962", "physician", "doctor", "clinical", "trials", "real-world", "evidence"]
)  # Note: Specific "144,000 physicians" figure not verified in sources; AMA opposed amendments but no count documented

PRE_1962_DRUG_DEVELOPMENT_COST = Parameter(
    50_000_000,
    source_ref=ReferenceID.PRE_1962_DRUG_COSTS_TIMELINE,
    source_type="external",
    description="Pre-1962 drug development cost (documented range: $10-50M in 1950s-1960s)",
    display_name="Pre-1962 Drug Development Cost",
    unit="USD",
    confidence="medium",
    keywords=["pre-1962", "drug", "development", "cost", "historical", "fda", "regulation"],
    distribution="lognormal",  # Cost data with right skew; historical estimates vary widely
    confidence_interval=(10_000_000, 50_000_000),  # Documented range $10M-$50M
)  # Documented range was $10-50M; using upper bound

CURRENT_ACTIVE_TRIALS = Parameter(
    10000,
    source_ref=ReferenceID.CLINICALTRIALS_GOV_ENROLLMENT_DATA_2025,
    source_type="external",
    description="Current active trials at any given time (3-5 year duration)",
    display_name="Current Active Trials at Any Given Time",
    unit="trials",
    keywords=["10k", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research"]
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
    keywords=["40%", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research"]
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
    keywords=["1.9m", "rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "research", "iqvia"]
)  # 1.9M patients/year (IQVIA 2022, post-COVID normalization from 4M peak in 2021)

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
)  # GBD 2013 study

CURRENT_PATIENT_PARTICIPATION_RATE = Parameter(
    CURRENT_TRIAL_SLOTS_AVAILABLE / CURRENT_DISEASE_PATIENTS_GLOBAL,
    source_type="definition",
    description="Current patient participation rate in clinical trials (0.08% = 1.9M participants / 2.4B disease patients)",
    display_name="Current Patient Participation Rate in Clinical Trials",
    unit="rate",
    formula="CURRENT_TRIAL_SLOTS / DISEASE_PATIENTS",
    keywords=["0%", "rct", "participant", "subject", "volunteer", "enrollee", "clinical study"],
    inputs=['CURRENT_TRIAL_SLOTS_AVAILABLE', 'CURRENT_DISEASE_PATIENTS_GLOBAL'],
    compute=lambda ctx: ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"] / ctx["CURRENT_DISEASE_PATIENTS_GLOBAL"],
)  # 0.08% of disease patients participate in trials (1.9M / 2.4B, IQVIA 2022)

# Traditional Trial Economics
TRADITIONAL_PHASE3_COST_PER_PATIENT = Parameter(
    80000,
    source_ref=ReferenceID.PHASE_3_COST_PER_PATIENT_113K,
    source_type="external",
    description="Phase 3 cost per patient (median)",
    display_name="Phase 3 Cost per Patient",
    unit="USD/patient",
    keywords=["80k", "50th percentile", "confirmatory trial", "middle value", "third phase", "participant", "subject"]
)  # $40k-$120k range, using midpoint

PHASE_3_TRIAL_COST_MIN = Parameter(
    20_000_000,
    source_ref=ReferenceID.PHASE_3_COST_PER_TRIAL_RANGE,
    source_type="external",
    description="Phase 3 trial total cost (minimum)",
    display_name="Phase 3 Trial Total Cost (Minimum)",
    unit="USD/trial",
    keywords=["20.0m", "confirmatory trial", "third phase", "rct", "p3", "phase iii", "clinical study"]
)  # $20M minimum for Phase 3 trials

# (DFDA_ACTIVE_TRIALS moved to after TRIAL_CAPACITY_MULTIPLIER definition)

# dFDA Trial Economics
RECOVERY_TRIAL_COST_PER_PATIENT = Parameter(
    500,
    source_ref=ReferenceID.RECOVERY_COST_500,
    source_type="external",
    description="RECOVERY trial cost per patient",
    display_name="Recovery Trial Cost per Patient",
    unit="USD/patient",
    confidence_interval=(350, 700),  # ±30% - pragmatic trial costs can vary
    distribution="lognormal",
    keywords=["rct", "participant", "subject", "volunteer", "enrollee", "clinical study", "clinical trial"]
)  # Proven cost from Oxford RECOVERY trial

ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE = Parameter(
    0.861,
    source_ref=ReferenceID.ANTIDEPRESSANT_TRIAL_EXCLUSION_RATES,
    source_type="external",
    description="Mean exclusion rate in antidepressant trials (86.1% of real-world patients excluded)",
    display_name="Antidepressant Trial Exclusion Rate",
    unit="percentage",
    keywords=["exclusion", "trial", "antidepressant", "eligibility", "real-world", "pragmatic"]
)

PRE_1962_VALIDATION_YEARS = Parameter(
    77,
    source_ref=ReferenceID.LIFE_EXPECTANCY_INCREASE_PRE_1962,
    source_type="definition",
    description="Years of empirical validation for physician-led pragmatic trials (1883-1960)",
    display_name="Pre-1962 Validation Years",
    unit="years",
    formula="1960 - 1883",
    keywords=["pre-1962", "historical", "validation", "physician", "trials", "life expectancy"]
)

# Research Acceleration Multipliers - MOVED to after GLOBAL_MED_RESEARCH_SPENDING (line ~2971)
# See calculation block after TOTAL_RESEARCH_FUNDING_WITH_TREATY

# (DFDA_COMPLETED_TRIALS_PER_YEAR moved to after DFDA_TRIALS_PER_YEAR_CAPACITY definition)

# dFDA operational costs
DFDA_UPFRONT_BUILD = Parameter(
    40_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#build-costs",
    source_type="definition",
    description="dFDA one-time build cost (central estimate)",
    display_name="dFDA One-Time Build Cost",
    unit="USD",
    keywords=["40.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"]
)  # $40M one-time build cost

DFDA_UPFRONT_BUILD_MAX = Parameter(
    46_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#build-costs",
    source_type="definition",
    description="dFDA one-time build cost (high estimate)",
    display_name="dFDA One-Time Build Cost (Maximum)",
    unit="USD",
    keywords=["46.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"]
)  # $46M one-time build cost (high end)

# DCT Platform Funding Comparables
DCT_PLATFORM_FUNDING_MEDIUM = Parameter(
    500_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#analogous-rom",
    source_type="definition",
    description="Mid-range funding for commercial DCT platform",
    display_name="Mid-Range Funding for Commercial Dct Platform",
    unit="USD",
    keywords=["500.0m", "pragmatic trials", "real world evidence", "capital", "finance", "money", "decentralized trials"]
)  # $500M funding for commercial platforms

# Per-patient cost in dollars (not billions)
DFDA_TARGET_COST_PER_PATIENT_USD = Parameter(
    1000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#cost-per-patient",
    source_type="definition",
    description="Target cost per patient in USD (same as DFDA_TARGET_COST_PER_PATIENT but in dollars)",
    display_name="dFDA Target Cost per Patient in USD",
    unit="USD/patient",
    keywords=["1k", "pragmatic trials", "real world evidence", "participant", "subject", "volunteer", "enrollee"]
)  # $1,000 per patient

# dFDA operational cost breakdown (in billions)
DFDA_OPEX_PLATFORM_MAINTENANCE = Parameter(
    15_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="definition",
    description="dFDA maintenance costs",
    display_name="dFDA Maintenance Costs",
    unit="USD/year",
    keywords=["15.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(10_000_000, 22_000_000),  # $10M-$22M (±30%)
)  # $15M

DFDA_OPEX_STAFF = Parameter(
    10_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="definition",
    description="dFDA staff costs (minimal, AI-assisted)",
    display_name="dFDA Staff Costs",
    unit="USD/year",
    keywords=["10.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(7_000_000, 15_000_000),  # $7M-$15M (±30%)
)  # $10M - minimal, AI-assisted

DFDA_OPEX_INFRASTRUCTURE = Parameter(
    8_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="definition",
    description="dFDA infrastructure costs (cloud, security)",
    display_name="dFDA Infrastructure Costs",
    unit="USD/year",
    keywords=["8.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(5_000_000, 12_000_000),  # $5M-$12M (±30%)
)  # $8M - cloud, security

DFDA_OPEX_REGULATORY = Parameter(
    5_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="definition",
    description="dFDA regulatory coordination costs",
    display_name="dFDA Regulatory Coordination Costs",
    unit="USD/year",
    keywords=["5.0m", "pragmatic trials", "real world evidence", "approval", "authorization", "oversight", "regulation"],
    distribution="lognormal",
    confidence_interval=(3_000_000, 8_000_000),  # $3M-$8M (±30%)
)  # $5M - regulatory coordination

DFDA_OPEX_COMMUNITY = Parameter(
    2_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="definition",
    description="dFDA community support costs",
    display_name="dFDA Community Support Costs",
    unit="USD/year",
    keywords=["2.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(1_000_000, 3_000_000),  # $1M-$3M (±30%)
)  # $2M - community support

# Total annual operational costs (calculated from components)
DFDA_ANNUAL_OPEX = Parameter(
    DFDA_OPEX_PLATFORM_MAINTENANCE
    + DFDA_OPEX_STAFF
    + DFDA_OPEX_INFRASTRUCTURE
    + DFDA_OPEX_REGULATORY
    + DFDA_OPEX_COMMUNITY,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#opex-breakdown",
    source_type="calculated",
    description="Total annual dFDA operational costs (sum of all components: $15M + $10M + $8M + $5M + $2M)",
    display_name="Total Annual dFDA Operational Costs",
    unit="USD/year",
    formula="PLATFORM_MAINTENANCE + STAFF + INFRASTRUCTURE + REGULATORY + COMMUNITY",
    latex=r"OPEX_{total} = \$15M \text{ (plat)} + \$10M \text{ (staff)} + \$8M \text{ (infra)} + \$5M \text{ (reg)} + \$2M \text{ (comm)} = \$40M",
    keywords=["pragmatic trials", "real world evidence", "approval", "authorization", "oversight", "regulation", "decentralized trials"],
    # Uncertainty derived from component inputs
    validation_min=25_000_000,   # Floor: Lean MVP with minimal regulatory team
    validation_max=80_000_000,   # Ceiling: Full global compliance + 24/7 support + security audit responses
    inputs=["DFDA_OPEX_PLATFORM_MAINTENANCE", "DFDA_OPEX_STAFF", "DFDA_OPEX_INFRASTRUCTURE", "DFDA_OPEX_REGULATORY", "DFDA_OPEX_COMMUNITY"],
    compute=lambda ctx: sum([ctx["DFDA_OPEX_PLATFORM_MAINTENANCE"], ctx["DFDA_OPEX_STAFF"], ctx["DFDA_OPEX_INFRASTRUCTURE"], ctx["DFDA_OPEX_REGULATORY"], ctx["DFDA_OPEX_COMMUNITY"]])
)  # $40M annually

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
    GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL * TRIAL_COST_REDUCTION_PCT,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#cost-reduction",
    source_type="calculated",
    description="Annual dFDA benefit from R&D savings (trial cost reduction, secondary component)",
    display_name="dFDA Annual Benefit: R&D Savings",
    unit="USD/year",
    formula="TRIAL_SPENDING × COST_REDUCTION_PCT",
    keywords=["rd savings", "pragmatic trials", "real world evidence", "rct", "clinical trial"],
    # Uncertainty derived from inputs (TRIAL_SPENDING × COST_REDUCTION_PCT)
    validation_min=25_000_000_000,   # Floor: 30% cost reduction at $83B market
    validation_max=65_000_000_000,   # Ceiling: 70% cost reduction at $97B market
    inputs=["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL", "TRIAL_COST_REDUCTION_PCT"],
    compute=lambda ctx: ctx["GLOBAL_CLINICAL_TRIALS_SPENDING_ANNUAL"] * ctx["TRIAL_COST_REDUCTION_PCT"]
)  # $41.5B from automating Phase 2/3/4 trials

# Note: DFDA_BENEFIT_DISEASE_ERADICATION_DELAY_ANNUAL defined later (after DFDA_AVOIDED_DISEASE_ERADICATION_DELAY_COST_ANNUAL)

# Legacy aliases for backward compatibility (will be removed after transition)
DFDA_RD_GROSS_SAVINGS_ANNUAL = DFDA_BENEFIT_RD_ONLY_ANNUAL  # Alias
DFDA_RD_SAVINGS_DAILY = Parameter(
    DFDA_BENEFIT_RD_ONLY_ANNUAL / DAYS_PER_YEAR,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#daily-opportunity-cost-of-inaction",
    source_type="calculated",
    description="Daily R&D savings from trial cost reduction (opportunity cost of delay)",
    display_name="Daily R&D Savings from Trial Cost Reduction",
    unit="USD/day",
    formula="ANNUAL_RD_SAVINGS ÷ DAYS_PER_YEAR",
    latex=r"Savings_{daily} = \frac{\$41.5B}{365} = \$113.7M",
    keywords=["137m", "daily", "per day", "each day", "opportunity cost", "delay cost"],
    inputs=['DFDA_BENEFIT_RD_ONLY_ANNUAL'],
    compute=lambda ctx: ctx["DFDA_BENEFIT_RD_ONLY_ANNUAL"] / DAYS_PER_YEAR,
)  # $113.7M/day

DFDA_NET_SAVINGS_RD_ONLY_ANNUAL = Parameter(
    DFDA_RD_GROSS_SAVINGS_ANNUAL - DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#net-savings",
    source_type="calculated",
    description="Annual net savings from R&D cost reduction only (gross savings minus operational costs, excludes regulatory delay value)",
    display_name="dFDA Annual Net Savings (R&D Only)",
    unit="USD/year",
    formula="GROSS_SAVINGS - ANNUAL_OPEX",
    latex=r"Savings_{net} = \$41.5B - \$0.04B = \$41.46B",
    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "yearly", "conservative"],
    inputs=["DFDA_RD_GROSS_SAVINGS_ANNUAL", "DFDA_ANNUAL_OPEX"],
    compute=lambda ctx: ctx["DFDA_RD_GROSS_SAVINGS_ANNUAL"] - ctx["DFDA_ANNUAL_OPEX"]
)  # $41.46B (R&D savings only, most conservative financial estimate)

# Simple ROI (not NPV-adjusted)
DFDA_ROI_SIMPLE = Parameter(
    DFDA_RD_GROSS_SAVINGS_ANNUAL / DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#roi-simple",
    source_type="calculated",
    description="Simple ROI without NPV adjustment (gross savings / annual opex)",
    display_name="dFDA Simple ROI Without NPV Adjustment",
    unit="ratio",
    formula="GROSS_SAVINGS ÷ ANNUAL_OPEX",
    keywords=["pragmatic trials", "real world evidence", "bcr", "benefit cost ratio", "economic return", "investment return", "return on investment"],
    inputs=['DFDA_RD_GROSS_SAVINGS_ANNUAL', 'DFDA_ANNUAL_OPEX'],
    compute=lambda ctx: ctx["DFDA_RD_GROSS_SAVINGS_ANNUAL"] / ctx["DFDA_ANNUAL_OPEX"],
)  # 1,038:1
# NOTE: For NPV-adjusted ROI (463:1), use DFDA_ROI_RD_ONLY below
# The NPV-based calculation accounts for time value of money and gradual adoption

# ---
# HEALTH IMPACT PARAMETERS
# ---

# QALY valuations
# Source: brain/book/appendix/icer-full-calculation.qmd
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
    validation_max=200000   # Ceiling: US EPA upper bound ($10M VSL / 50 years)
)  # Standard economic value per QALY

WHO_QALY_THRESHOLD_COST_EFFECTIVE = Parameter(
    50000,
    source_ref=ReferenceID.WHO_COST_EFFECTIVENESS_THRESHOLD,
    source_type="external",
    description="Cost-effectiveness threshold widely used in US health economics ($50,000/QALY, from 1980s dialysis costs)",
    display_name="Cost-Effectiveness Threshold ($50,000/QALY)",
    unit="USD/QALY",
    keywords=["50k", "qaly", "cost effective", "threshold", "health economics", "dialysis", "benchmark"]
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
)  # Standard assumption (WHO life tables)

# Efficacy Lag Duration
EFFICACY_LAG_YEARS = Parameter(
    8.2,
    source_ref=ReferenceID.BIO_CLINICAL_DEVELOPMENT_2021,
    source_type="external",
    description="Regulatory delay for efficacy testing (Phase II/III) post-safety verification",
    display_name="Regulatory Delay for Efficacy Testing Post-Safety Verification",
    unit="years",
    formula="TOTAL_TIME_TO_MARKET - PHASE_1_DURATION",
    latex=r"t_{lag} = 10.5 - 2.3 = 8.2 \text{ years}",
    confidence="high",
    last_updated="2021",
    peer_reviewed=True,
    keywords=["approval lag", "drug lag", "fda delay", "bureaucratic delay", "efficacy lag", "approval", "authorization"],
    distribution="normal",  # Normal appropriate: well-measured empirical data
    std_error=1.0,  # ±1.0 years (~12% CV): Captures therapeutic area variance
                    # Economist rationale: Real variability 7.5-9.5 years across areas
                    # (oncology 9.2y, vaccines 7.3y, rare disease 10+y)
                    # Widened from ±0.5y to reflect heterogeneity beyond measurement error
                    # Justification: Pooled mean hides substantial between-indication variance
    validation_min=6.0,   # Floor: Fastest quartile (priority review, breakthrough)
    validation_max=11.0   # Ceiling: Slowest quartile (complex endpoints, rare disease)
)  # 8.2 years efficacy lag

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
    latex=r"P_{\text{unavoidable}} = \sum_{\text{categories}} (\text{disease burden} \times (1 - \text{max cure rate})) = 7.91\%",
    confidence="medium",
)  # ~7.9% unavoidable with aging_related at 0.99

EVENTUALLY_AVOIDABLE_DEATH_PCT = Parameter(
    1 - _unavoidable_pct,
    source_type="definition",
    description="Percentage of deaths that are eventually avoidable with sufficient biomedical research and technological advancement",
    display_name="Eventually Avoidable Death Percentage",
    unit="percentage",
    formula="1 - FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT",
    latex=r"P_{\text{avoidable}} = 1 - 0.0791 = 92.09\%",
    confidence="medium",
)  # ~92.1% eventually avoidable

# Disease Eradication Delay (PRIMARY ESTIMATE)
# Assumes regulatory delay shifts disease eradication timeline back by efficacy lag period
# Adjusted to exclude fundamentally unavoidable deaths (primarily accidents)
DISEASE_ERADICATION_DELAY_DEATHS_TOTAL = Parameter(
    int(GLOBAL_DISEASE_DEATHS_DAILY * EFFICACY_LAG_YEARS * DAYS_PER_YEAR * (1 - _unavoidable_pct)),
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#disease-eradication-delay",
    source_type="calculated",
    description="Total eventually avoidable deaths from delaying disease eradication by 8.2 years (PRIMARY estimate, conservative). Excludes fundamentally unavoidable deaths (primarily accidents ~7.9%).",
    display_name="Total Deaths from Disease Eradication Delay",
    unit="deaths",
    formula="ANNUAL_DEATHS × EFFICACY_LAG_YEARS × EVENTUALLY_AVOIDABLE_DEATH_PCT",
    latex=r"D_{total} = 54.75M \text{ (annual)} \times 8.2 \text{ (lag)} \times 92.1\% \text{ (avoidable)} = 413.4M",
    confidence="medium",
    keywords=["disease eradication", "regulatory delay", "efficacy lag", "primary estimate", "eventually avoidable"],
    # Uncertainty derived from inputs (DEATHS_DAILY × EFFICACY_LAG × AVOIDABILITY)
    validation_min=250_000_000,  # Floor: Pessimistic avoidability (70%), lower lag (6y)
    validation_max=600_000_000,  # Ceiling: Optimistic avoidability (98%), higher lag (10y)
    inputs=['EFFICACY_LAG_YEARS', 'GLOBAL_DISEASE_DEATHS_DAILY'],
    compute=lambda ctx: int(ctx["GLOBAL_DISEASE_DEATHS_DAILY"] * ctx["EFFICACY_LAG_YEARS"] * DAYS_PER_YEAR * (1 - _unavoidable_pct)),
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
    validation_max=75   # Ceiling: Chronic disease-dominated scenario (cancer, CVD, Alzheimer's)
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
    validation_max=85   # Ceiling: Optimistic scenario (longevity breakthroughs, developed countries)
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
    validation_max=150  # Ceiling: Accident-limited lifespan (~230 years - 80 baseline)
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
    validation_max=15   # Ceiling: Chronic-dominated scenario (Alzheimer's, Parkinson's, long cancers)
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
    validation_max=0.50   # Ceiling: Pessimistic (severe symptoms, poor healthcare access)
)

# Morbidity Analysis (DALYs) - Based on Disease Eradication Delay Model
DISEASE_ERADICATION_DELAY_YLL = Parameter(
    DISEASE_ERADICATION_DELAY_DEATHS_TOTAL * (GLOBAL_LIFE_EXPECTANCY_2024 - REGULATORY_DELAY_MEAN_AGE_OF_DEATH),
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#daly-calculation",
    source_type="calculated",
    description="Years of Life Lost from disease eradication delay deaths (PRIMARY estimate)",
    display_name="Years of Life Lost from Disease Eradication Delay",
    unit="years",
    formula="DEATHS_TOTAL × (LIFE_EXPECTANCY - MEAN_AGE_OF_DEATH)",
    latex=r"YLL = 413.4M \times 17 \text{ (years lost)} = 7.03B",
    confidence="medium",
    keywords=["disease eradication", "YLL", "years of life lost", "disease burden", "mortality burden"],
    inputs=["DISEASE_ERADICATION_DELAY_DEATHS_TOTAL", "GLOBAL_LIFE_EXPECTANCY_2024", "REGULATORY_DELAY_MEAN_AGE_OF_DEATH"],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_DELAY_DEATHS_TOTAL"] * (ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["REGULATORY_DELAY_MEAN_AGE_OF_DEATH"])
)  # 7.63B years

DISEASE_ERADICATION_DELAY_YLD = Parameter(
    DISEASE_ERADICATION_DELAY_DEATHS_TOTAL * REGULATORY_DELAY_SUFFERING_PERIOD_YEARS * CHRONIC_DISEASE_DISABILITY_WEIGHT,
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#daly-calculation",
    source_type="calculated",
    description="Years Lived with Disability during disease eradication delay (PRIMARY estimate)",
    display_name="Years Lived with Disability During Disease Eradication Delay",
    unit="years",
    formula="DEATHS_TOTAL × SUFFERING_PERIOD × DISABILITY_WEIGHT",
    confidence="medium",
    keywords=["disease eradication", "YLD", "years lived with disability", "disease burden", "morbidity"],
    inputs=["DISEASE_ERADICATION_DELAY_DEATHS_TOTAL", "REGULATORY_DELAY_SUFFERING_PERIOD_YEARS", "CHRONIC_DISEASE_DISABILITY_WEIGHT"],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_DELAY_DEATHS_TOTAL"] * ctx["REGULATORY_DELAY_SUFFERING_PERIOD_YEARS"] * ctx["CHRONIC_DISEASE_DISABILITY_WEIGHT"]
)  # 943M years

DISEASE_ERADICATION_DELAY_DALYS = Parameter(
    DISEASE_ERADICATION_DELAY_YLL + DISEASE_ERADICATION_DELAY_YLD,
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#daly-calculation",
    source_type="calculated",
    description="Total Disability-Adjusted Life Years lost from disease eradication delay (PRIMARY estimate)",
    display_name="Total DALYs Lost from Disease Eradication Delay",
    unit="DALYs",
    formula="YLL + YLD",
    latex=r"DALY_{total} = 7.03B \text{ (YLL)} + 0.87B \text{ (YLD)} = 7.90B",
    confidence="medium",
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
    inputs=["DISEASE_ERADICATION_DELAY_YLL", "DISEASE_ERADICATION_DELAY_YLD"],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_DELAY_YLL"] + ctx["DISEASE_ERADICATION_DELAY_YLD"]
)  # 7.90B DALYs

# Suffering Hours (one-time benefit from timeline shift)
SUFFERING_HOURS_ELIMINATED_TOTAL = Parameter(
    DISEASE_ERADICATION_DELAY_YLD * HOURS_PER_YEAR,  # YLD in years × hours per year
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#daly-calculation",
    source_type="calculated",
    description="Total hours of human suffering eliminated by 8.2-year disease eradication timeline shift (one-time benefit from YLD component, not annual recurring)",
    display_name="Total Suffering Hours Eliminated",
    unit="hours",
    formula="YLD × HOURS_PER_YEAR",
    latex=r"Hours = 868M \text{ (YLD)} \times 8{,}760 \text{ (hrs/yr)} = 7.60T",
    confidence="medium",
    keywords=["suffering", "disability", "pain", "morbidity", "quality of life", "one-time benefit", "disease burden"],
    inputs=['DISEASE_ERADICATION_DELAY_YLD'],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_DELAY_YLD"] * HOURS_PER_YEAR,
)  # 7.65 trillion hours total

# Economic Valuation (using standardized $150k VSLY)
DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS = Parameter(
    DISEASE_ERADICATION_DELAY_DALYS * STANDARD_ECONOMIC_QALY_VALUE_USD,
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#economic-valuation",
    source_type="calculated",
    description="Total economic loss from delaying disease eradication by 8.2 years (PRIMARY estimate, 2024 USD). Values global DALYs at standardized US/International normative rate ($150k) rather than local ability-to-pay, representing the full human capital loss.",
    display_name="Total Economic Loss from Disease Eradication Delay",
    unit="USD",
    formula="DALYS_TOTAL × VSLY",
    latex=r"Loss = 7.90B \times \$150k = \$1.185\text{ quadrillion}",
    confidence="medium",
    keywords=["disease eradication", "economic loss", "deadweight loss", "primary estimate"],
    inputs=['DISEASE_ERADICATION_DELAY_DALYS', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_DELAY_DALYS"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
)  # $1.191 Quadrillion total economic loss

# TOTAL Economic Loss Parameters (One-Time Benefits from Eliminating 8.2-Year Delay)
# These represent the complete, one-time benefit of eliminating the efficacy lag
# NOT amortized annual values that could mislead by suggesting recurring benefits

# Historical Progress - TOTAL (Conservative Floor)
HISTORICAL_PROGRESS_DEATHS_TOTAL = Parameter(
    12_000_000 * EFFICACY_LAG_YEARS,
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#historical-progress",
    source_type="calculated",
    description="Total deaths from delaying existing drugs over 8.2-year efficacy lag (CONSERVATIVE FLOOR). One-time impact of eliminating Phase 2-4 testing delay for drugs already approved 1962-2024. Based on 12M deaths/year rate × 8.2 years.",
    display_name="Total Deaths from Historical Progress Delays",
    unit="deaths",
    formula="12M × EFFICACY_LAG_YEARS",
    latex=r"D_{total} = 12M \times 8.2 = 98.4M",
    confidence="high",
    keywords=["98.4m", "conservative", "historical", "total", "one-time", "floor estimate"],
    inputs=['EFFICACY_LAG_YEARS'],
    compute=lambda ctx: 12_000_000 * ctx["EFFICACY_LAG_YEARS"],
)  # 98.4M total deaths

HISTORICAL_PROGRESS_ECONOMIC_LOSS_TOTAL = Parameter(
    HISTORICAL_PROGRESS_DEATHS_TOTAL * (GLOBAL_LIFE_EXPECTANCY_2024 - REGULATORY_DELAY_MEAN_AGE_OF_DEATH) * STANDARD_ECONOMIC_QALY_VALUE_USD,
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#historical-progress",
    source_type="calculated",
    description="Total economic loss from delaying existing drugs over 8.2-year efficacy lag (CONSERVATIVE FLOOR). One-time benefit of eliminating Phase 2-4 delay.",
    display_name="Total Economic Loss from Historical Progress Delays",
    unit="USD",
    formula="DEATHS_TOTAL × YLL × VSLY",
    latex=r"Loss_{total} = 98.4M \times 17 \times \$150k = \$251T",
    confidence="high",
    keywords=["$251t", "conservative", "historical", "total", "one-time", "floor estimate"],
    inputs=['GLOBAL_LIFE_EXPECTANCY_2024', 'HISTORICAL_PROGRESS_DEATHS_TOTAL', 'REGULATORY_DELAY_MEAN_AGE_OF_DEATH', 'STANDARD_ECONOMIC_QALY_VALUE_USD'],
    compute=lambda ctx: ctx["HISTORICAL_PROGRESS_DEATHS_TOTAL"] * (ctx["GLOBAL_LIFE_EXPECTANCY_2024"] - ctx["REGULATORY_DELAY_MEAN_AGE_OF_DEATH"]) * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"],
)  # $251T total (conservative floor)

# Disease Eradication + Acceleration - TOTAL (Optimistic Upper Bound)
DISEASE_ERADICATION_PLUS_ACCELERATION_DEATHS_TOTAL = Parameter(
    (GLOBAL_DISEASE_DEATHS_DAILY * DAYS_PER_YEAR * 2) * EFFICACY_LAG_YEARS,
    source_ref="/knowledge/references.qmd#pharmaceutical-innovation-acceleration-economics",
    source_type="calculated",
    description="Total deaths from disease eradication delay plus innovation acceleration (OPTIMISTIC UPPER BOUND). Represents additional deaths avoided beyond lag elimination through innovation cascade effects: faster development cycles, lower barriers enabling more drugs, earlier phase starts. The 2× multiplier is supported by research showing 50% timeline reductions achievable (Nature 2023) and adaptive trials generating millions of additional life-years (Woods et al. 2024). Based on (150K daily × 365 × 2) × 8.2 years.",
    display_name="Total Deaths from Disease Eradication + Innovation Acceleration",
    unit="deaths",
    formula="(ANNUAL_DEATHS × 2) × EFFICACY_LAG_YEARS",
    latex=r"D_{total} = (54.75M \times 2) \times 8.2 = 898M",
    confidence="low",
    keywords=["898m", "optimistic", "total", "one-time", "upper bound", "acceleration", "innovation"],
    inputs=['EFFICACY_LAG_YEARS', 'GLOBAL_DISEASE_DEATHS_DAILY'],
    compute=lambda ctx: (ctx["GLOBAL_DISEASE_DEATHS_DAILY"] * DAYS_PER_YEAR * 2) * ctx["EFFICACY_LAG_YEARS"],
)  # 898M total deaths (optimistic with innovation acceleration)

DISEASE_ERADICATION_PLUS_ACCELERATION_ECONOMIC_LOSS_TOTAL = Parameter(
    DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS * 2,
    source_ref="/knowledge/references.qmd#pharmaceutical-innovation-acceleration-economics",
    source_type="calculated",
    description="Total economic loss from disease eradication delay plus innovation acceleration (OPTIMISTIC UPPER BOUND). The 2× multiplier represents combined timeline and volume effects from eliminating Phase 2-4 cost barriers. Research shows: (1) Timeline acceleration of 50% achievable through AI/tech (Nature 2023), (2) Adaptive trials can reduce costs $2.6B→$2.2B, generating 3.5M additional life-years (Woods et al. 2024, Health Economics), (3) Cost barrier elimination enables more drugs to reach viability. The 2× factor conservatively represents either 2× timeline acceleration OR 1.5× timeline × 1.33× volume. Dynamic efficiency framework suggests optimal manufacturer value share ~20% maximizes long-term population health (Woods 2024).",
    display_name="Total Economic Loss from Disease Eradication + Innovation Acceleration",
    unit="USD",
    formula="PRIMARY_TOTAL × 2 (combined timeline + volume effects)",
    latex=r"Loss_{total} = \$1,286T \times 2 = \$2,572T",
    confidence="low",
    keywords=["$2572t", "optimistic", "total", "one-time", "upper bound", "acceleration", "innovation", "dynamic efficiency"],
    inputs=['DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS'],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS"] * 2,
)  # $2,572T total (optimistic upper bound with innovation acceleration)

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
    keywords=["thalidomide", "birth defects", "drug safety"]
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
    keywords=["thalidomide", "mortality", "infant deaths"]
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
    keywords=["population", "demographics"]
)

THALIDOMIDE_US_CASES_PREVENTED = Parameter(
    int(THALIDOMIDE_CASES_WORLDWIDE * THALIDOMIDE_US_POPULATION_SHARE_1960),
    source_type="calculated",
    description="Estimated US thalidomide cases prevented by FDA rejection",
    display_name="Thalidomide US Cases Prevented",
    unit="cases",
    formula="WORLDWIDE_CASES × US_POPULATION_SHARE",
    latex=r"15{,}000 \times 6\% = 900 \text{ cases}",
    confidence="medium",
    keywords=["thalidomide", "FDA", "prevention"],
    inputs=['THALIDOMIDE_CASES_WORLDWIDE', 'THALIDOMIDE_US_POPULATION_SHARE_1960'],
    compute=lambda ctx: int(ctx["THALIDOMIDE_CASES_WORLDWIDE"] * ctx["THALIDOMIDE_US_POPULATION_SHARE_1960"]),
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
    keywords=["thalidomide", "disability", "quality of life"]
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
    keywords=["thalidomide", "longevity", "life expectancy"]
)

# Calculate DALYs per "Thalidomide Event"
THALIDOMIDE_DEATHS_PER_EVENT = Parameter(
    int(THALIDOMIDE_US_CASES_PREVENTED * THALIDOMIDE_MORTALITY_RATE),
    source_type="calculated",
    description="Deaths per US-scale thalidomide event",
    display_name="Thalidomide Deaths Per Event",
    unit="deaths",
    formula="US_CASES × MORTALITY_RATE",
    latex=r"900 \text{ (cases)} \times 40\% \text{ (mortality)} = 360 \text{ deaths}",
    confidence="medium",
    keywords=["thalidomide", "mortality"],
    inputs=['THALIDOMIDE_MORTALITY_RATE', 'THALIDOMIDE_US_CASES_PREVENTED'],
    compute=lambda ctx: int(ctx["THALIDOMIDE_US_CASES_PREVENTED"] * ctx["THALIDOMIDE_MORTALITY_RATE"]),
)

THALIDOMIDE_YLL_PER_EVENT = Parameter(
    THALIDOMIDE_DEATHS_PER_EVENT * 80,  # Infant deaths, 80 years lost per death
    source_type="calculated",
    description="Years of Life Lost per thalidomide event (infant deaths)",
    display_name="Thalidomide YLL Per Event",
    unit="years",
    formula="DEATHS × 80 years",
    latex=r"360 \text{ (deaths)} \times 80 \text{ (years)} = 28{,}800 \text{ YLL}",
    confidence="medium",
    keywords=["thalidomide", "YLL", "mortality"],
    inputs=['THALIDOMIDE_DEATHS_PER_EVENT'],
    compute=lambda ctx: ctx["THALIDOMIDE_DEATHS_PER_EVENT"] * 80,
)

THALIDOMIDE_SURVIVORS_PER_EVENT = Parameter(
    int(THALIDOMIDE_US_CASES_PREVENTED * (1 - THALIDOMIDE_MORTALITY_RATE)),
    source_type="calculated",
    description="Survivors per US-scale thalidomide event",
    display_name="Thalidomide Survivors Per Event",
    unit="cases",
    formula="US_CASES × (1 - MORTALITY_RATE)",
    latex=r"900 \text{ (cases)} \times 60\% \text{ (survival)} = 540 \text{ survivors}",
    confidence="medium",
    keywords=["thalidomide", "survivors"],
    inputs=['THALIDOMIDE_MORTALITY_RATE', 'THALIDOMIDE_US_CASES_PREVENTED'],
    compute=lambda ctx: int(ctx["THALIDOMIDE_US_CASES_PREVENTED"] * (1 - ctx["THALIDOMIDE_MORTALITY_RATE"])),
)

THALIDOMIDE_YLD_PER_EVENT = Parameter(
    THALIDOMIDE_SURVIVORS_PER_EVENT * THALIDOMIDE_SURVIVOR_LIFESPAN * THALIDOMIDE_DISABILITY_WEIGHT,
    source_type="calculated",
    description="Years Lived with Disability per thalidomide event",
    display_name="Thalidomide YLD Per Event",
    unit="years",
    formula="SURVIVORS × LIFESPAN × DISABILITY_WEIGHT",
    latex=r"540 \text{ (surv)} \times 60 \text{ (yrs)} \times 0.4 \text{ (weight)} = 12{,}960 \text{ YLD}",
    confidence="medium",
    keywords=["thalidomide", "YLD", "disability"],
    inputs=['THALIDOMIDE_DISABILITY_WEIGHT', 'THALIDOMIDE_SURVIVORS_PER_EVENT', 'THALIDOMIDE_SURVIVOR_LIFESPAN'],
    compute=lambda ctx: ctx["THALIDOMIDE_SURVIVORS_PER_EVENT"] * ctx["THALIDOMIDE_SURVIVOR_LIFESPAN"] * ctx["THALIDOMIDE_DISABILITY_WEIGHT"],
)

THALIDOMIDE_DALYS_PER_EVENT = Parameter(
    THALIDOMIDE_YLL_PER_EVENT + THALIDOMIDE_YLD_PER_EVENT,
    source_type="calculated",
    description="Total DALYs per US-scale thalidomide event (YLL + YLD)",
    display_name="Thalidomide DALYs Per Event",
    unit="DALYs",
    formula="YLL + YLD",
    latex=r"28{,}800 + 12{,}960 = 41{,}760 \text{ DALYs}",
    confidence="medium",
    keywords=["thalidomide", "DALYs", "disease burden"],
    inputs=['THALIDOMIDE_YLD_PER_EVENT', 'THALIDOMIDE_YLL_PER_EVENT'],
    compute=lambda ctx: ctx["THALIDOMIDE_YLL_PER_EVENT"] + ctx["THALIDOMIDE_YLD_PER_EVENT"],
)

# Type I Error: Assuming one Thalidomide-scale disaster EVERY YEAR for 62 years (extreme overestimate)
TYPE_I_ERROR_BENEFIT_DALYS = Parameter(
    THALIDOMIDE_DALYS_PER_EVENT * 62,  # 1962-2024 period
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#risk-analysis",
    source_type="calculated",
    description="Maximum DALYs saved by FDA preventing unsafe drugs over 62-year period 1962-2024 (extreme overestimate: one Thalidomide-scale event per year)",
    display_name="Maximum DALYs Saved by FDA Preventing Unsafe Drugs (1962-2024)",
    unit="DALYs",
    formula="THALIDOMIDE_DALYS_PER_EVENT × 62 years",
    latex=r"41{,}760 \times 62 = 2.59M \text{ DALYs}",
    confidence="low",
    conservative=False,  # This is an extreme overestimate of benefits
    keywords=["Type I error", "FDA", "drug safety", "disease burden", "disability burden", "global burden of disease", "suffering", "approval", "1962-2024"],
    inputs=['THALIDOMIDE_DALYS_PER_EVENT'],
    compute=lambda ctx: ctx["THALIDOMIDE_DALYS_PER_EVENT"] * 62,
)

TYPE_II_ERROR_COST_RATIO = Parameter(
    DISEASE_ERADICATION_DELAY_DALYS / TYPE_I_ERROR_BENEFIT_DALYS,
    source_ref="/knowledge/appendix/regulatory-mortality-analysis.qmd#risk-analysis",
    source_type="calculated",
    description="Ratio of Type II error cost to Type I error benefit (harm from delay vs. harm prevented)",
    display_name="Ratio of Type Ii Error Cost to Type I Error Benefit",
    unit="ratio",
    formula="TYPE_II_COST ÷ TYPE_I_BENEFIT",
    confidence="medium",
    keywords=["approval lag", "drug lag", "fda delay", "bureaucratic delay", "efficacy lag", "approval"],
    inputs=['DISEASE_ERADICATION_DELAY_DALYS', 'TYPE_I_ERROR_BENEFIT_DALYS'],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_DELAY_DALYS"] / ctx["TYPE_I_ERROR_BENEFIT_DALYS"],
)

# Peace dividend health benefits
TREATY_LIVES_SAVED_ANNUAL_GLOBAL = Parameter(
    GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL * TREATY_REDUCTION_PCT,
    source_ref="/knowledge/appendix/parameters-and-calculations.qmd#sec-treaty_lives_saved_annual_global",
    source_type="calculated",
    description="Annual lives saved from 1% reduction in conflict deaths",
    display_name="Annual Lives Saved from 1% Reduction in Conflict Deaths",
    unit="lives/year",
    formula="TOTAL_DEATHS × REDUCTION_PCT",
    keywords=["1%", "deaths prevented", "life saving", "mortality reduction", "deaths averted", "one percent", "international agreement"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL"] * ctx["TREATY_REDUCTION_PCT"],
)  # 2,446 lives
TREATY_QALYS_GAINED_ANNUAL_GLOBAL = Parameter(
    TREATY_LIVES_SAVED_ANNUAL_GLOBAL * STANDARD_QALYS_PER_LIFE_SAVED,
    source_ref="/knowledge/appendix/parameters-and-calculations.qmd#sec-treaty_qalys_gained_annual_global",
    source_type="calculated",
    description="Annual QALYs gained from peace dividend (lives saved × QALYs/life)",
    display_name="Annual QALYs Gained from Peace Dividend",
    unit="QALYs/year",
    formula="LIVES_SAVED × QALYS_PER_LIFE",
    keywords=["1%", "cost effectiveness", "value for money", "disease burden", "cost per daly", "cost per qaly", "deaths prevented"],
    inputs=['STANDARD_QALYS_PER_LIFE_SAVED', 'TREATY_LIVES_SAVED_ANNUAL_GLOBAL'],
    compute=lambda ctx: ctx["TREATY_LIVES_SAVED_ANNUAL_GLOBAL"] * ctx["STANDARD_QALYS_PER_LIFE_SAVED"],
)  # 85,610 QALYs


# DELETED: TREATY_TOTAL_LIVES_SAVED_DAILY
# Was derived from deleted TREATY_TOTAL_LIVES_SAVED_ANNUAL (which mixed one-time + recurring)

# ---
# CAMPAIGN COSTS
# ---
# Updated to $1B VICTORY bond model: Lobbying $650M + Referendum $300M + Reserve $50M
# Tech R&D removed from campaign (post-treaty implementation funded by $27B/year)
# Legal/ops/partnerships rolled into main campaign categories

# Source: /knowledge/appendix/fundraising-strategy.qmd#capital-structure-campaign-vs-implementation
TREATY_CAMPAIGN_DURATION_YEARS = Parameter(
    4,
    source_ref="/knowledge/strategy/roadmap.qmd",
    source_type="definition",
    description="Treaty campaign duration (3-5 year range, using midpoint)",
    display_name="Treaty Campaign Duration",
    unit="years",
    keywords=["1%", "one percent", "international agreement", "peace treaty", "agreement", "pact", "duration"],
    distribution="triangular",  # Documented range with most likely midpoint
    confidence_interval=(3, 5),  # 3-5 year range as specified
)  # 3-5 year range, using midpoint

# Campaign budget breakdown - Two main categories
TREATY_CAMPAIGN_BUDGET_REFERENDUM = Parameter(
    300_000_000,
    source_ref="/knowledge/appendix/fundraising-strategy.qmd#campaign-budget-breakdown",
    source_type="definition",
    description="Global referendum campaign (get 208M votes): ads, media, partnerships, staff, legal/compliance",
    display_name="Global Referendum Campaign: Ads, Media, Partnerships, Staff, Legal/Compliance",
    unit="USD",
    confidence="medium",
    keywords=["300.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"],
    distribution="lognormal",  # Right-skewed: campaign overruns more likely than savings
    confidence_interval=(180e6, 500e6),  # 80% CI: $180M-$500M (±40% uncertainty)
    # Rationale: Digital campaigns can be lean ($180M), but traditional media + partnerships
    # could balloon to $500M. Brexit referendum ~£40M scaled globally suggests wide range.
    validation_min=100_000_000,   # Floor: Digital-only minimal campaign
    validation_max=800_000_000    # Ceiling: Full traditional media saturation
)  # $300M total referendum campaign (includes all support costs)

TREATY_CAMPAIGN_BUDGET_LOBBYING = Parameter(
    650_000_000,
    source_ref="/knowledge/appendix/fundraising-strategy.qmd#campaign-budget-breakdown",
    source_type="definition",
    description="Political lobbying campaign: direct lobbying (US/EU/G20), Super PACs, opposition research, staff, legal/compliance (exceeds pharma $300M + MIC $150M)",
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
    validation_max=2_000_000_000  # Ceiling: Full-scale opposition war chest
)  # $650M total lobbying (outspends pharma + MIC combined)

TREATY_CAMPAIGN_BUDGET_RESERVE = Parameter(
    50_000_000,
    source_ref="/knowledge/appendix/fundraising-strategy.qmd#campaign-budget-breakdown",
    source_type="definition",
    description="Reserve fund / contingency buffer",
    display_name="Reserve Fund / Contingency Buffer",
    unit="USD",
    confidence="medium",
    keywords=["50.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"],
    distribution="lognormal",
    confidence_interval=(20e6, 100e6),  # 80% CI: $20M-$100M (±60% uncertainty)
    # Rationale: Contingency by definition covers unknowns. Could be barely tapped ($20M)
    # or fully depleted + need more ($100M). Wide range reflects inherent unpredictability.
    validation_min=10_000_000,   # Floor: Minimal contingency
    validation_max=150_000_000   # Ceiling: Major unforeseen costs
)  # $50M reserve

# Total campaign cost (calculated from components)
TREATY_CAMPAIGN_TOTAL_COST = Parameter(
    TREATY_CAMPAIGN_BUDGET_REFERENDUM + TREATY_CAMPAIGN_BUDGET_LOBBYING + TREATY_CAMPAIGN_BUDGET_RESERVE,
    source_ref="/knowledge/appendix/fundraising-strategy.qmd#capital-structure-campaign-vs-implementation",
    source_type="calculated",
    description="Total treaty campaign cost (100% VICTORY Social Impact Bonds)",
    display_name="Total 1% Treaty Campaign Cost",
    unit="USD",
    formula="REFERENDUM + LOBBYING + RESERVE",
    latex=r"CampaignCost = \$300M \text{ (ref)} + \$650M \text{ (lob)} + \$50M \text{ (res)} = \$1.0B",
    confidence="high",
    keywords=["1%", "impact investing", "pay for success", "one percent", "debt instrument", "development finance", "fixed income"],
    # UNCERTAINTY: Propagates from component budgets (REFERENDUM, LOBBYING, RESERVE)
    # Expected ±50% given unprecedented scale (no manual override)
    # Comparables: Brexit campaigns ~£40M, Ottawa Treaty ~$10M (1997 dollars)
    # This is 20x larger than any treaty campaign—weak precedents justify wide uncertainty
    # Right skew expected: cost overruns more likely than savings (planning fallacy, scope creep)
    # Tornado analysis will show which budget components drive most variance
    validation_min=500_000_000,   # Floor: Bare minimum (digital-only, no paid media)
    validation_max=3_000_000_000,  # Ceiling: Full traditional + opposition response
    inputs=["TREATY_CAMPAIGN_BUDGET_REFERENDUM", "TREATY_CAMPAIGN_BUDGET_LOBBYING", "TREATY_CAMPAIGN_BUDGET_RESERVE"],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_BUDGET_REFERENDUM"] + ctx["TREATY_CAMPAIGN_BUDGET_LOBBYING"] + ctx["TREATY_CAMPAIGN_BUDGET_RESERVE"]
)  # $1B total campaign cost (all VICTORY bonds)

# Viral Referendum Scenario Budgets (Tiered Budget Calculations with Increasing Marginal Costs)
TREATY_CAMPAIGN_VIRAL_REFERENDUM_BASE_CASE = Parameter(
    140_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd#base-case-scenario",
    source_type="definition",
    description="Base case viral referendum budget (assumes flat $0.50/vote, optimistic)",
    display_name="Base Case Viral Referendum Budget",
    unit="USD",
    formula="PLATFORM + VERIFICATION + PAYMENTS_FLAT_RATE",
    confidence="medium",
    keywords=["140.0m", "1%", "high estimate", "best case", "ambitious", "overestimate", "one percent"]
)  # $140M base case (optimistic, assumes no increasing marginal costs)

TREATY_CAMPAIGN_VIRAL_REFERENDUM_WORST_CASE = Parameter(
    406_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd#worst-case-scenario",
    source_type="definition",
    description="Worst-case viral referendum budget (tiered pricing with increasing marginal costs)",
    display_name="Worst-Case Viral Referendum Budget",
    unit="USD",
    formula="PLATFORM + VERIFICATION + TIERED_PAYMENTS",
    latex=r"Budget_{worst} = \$35M_{platform} + \$59M_{verification} + \$312M_{tiered\ payments} = \$406M",
    confidence="medium",
    keywords=["406.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"]
)  # $406M worst case: 10M×$0.25 + 90M×$0.50 + 100M×$1.00 + 80M×$2.00 = $312M payments

TREATY_CAMPAIGN_VIRAL_REFERENDUM_REALISTIC = Parameter(
    220_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd#realistic-scenario",
    source_type="definition",
    description="Realistic viral referendum budget (moderate tiered pricing)",
    display_name="Realistic Viral Referendum Budget",
    unit="USD",
    formula="PLATFORM + VERIFICATION + MODERATE_TIERED_PAYMENTS",
    latex=r"Budget_{realistic} = \$35M_{platform} + \$59M_{verification} + \$126M_{tiered\ payments} = \$220M",
    confidence="high",
    keywords=["220.0m", "1%", "likely", "moderate", "probable", "one percent", "international agreement"]
)  # $220M realistic: 10M×$0.25 + 90M×$0.50 + 100M×$0.75 + 80M×$1.00 = $126M payments

TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED = Parameter(
    TREATY_CAMPAIGN_TOTAL_COST / TREATY_CAMPAIGN_DURATION_YEARS,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="calculated",
    description="Amortized annual campaign cost (total cost ÷ campaign duration)",
    display_name="Amortized Annual Treaty Campaign Cost",
    unit="USD/year",
    formula="TOTAL_COST ÷ DURATION",
    latex=r"AnnualCost = \$1B / 4 = \$0.25B",
    keywords=["1%", "one percent", "international agreement", "peace treaty", "yearly", "agreement", "costs"],
    inputs=['TREATY_CAMPAIGN_DURATION_YEARS', 'TREATY_CAMPAIGN_TOTAL_COST'],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_TOTAL_COST"] / ctx["TREATY_CAMPAIGN_DURATION_YEARS"],
)  # $250M

# Campaign phase budgets
CAMPAIGN_PHASE1_BUDGET = Parameter(
    200_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Phase 1 campaign budget (Foundation, Year 1)",
    display_name="Phase 1 Campaign Budget",
    unit="USD",
    keywords=["200.0m", "first phase", "safety trial", "p1", "phase i", "phase1", "campaign"]
)  # $200M for Phase 1

CAMPAIGN_PHASE2_BUDGET = Parameter(
    500_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Phase 2 campaign budget (Scale & Momentum, Years 2-3)",
    display_name="Phase 2 Campaign Budget",
    unit="USD",
    keywords=["500.0m", "efficacy trial", "second phase", "p2", "phase ii", "phase2", "campaign"]
)  # $500M for Phase 2

CAMPAIGN_MEDIA_BUDGET_MIN = Parameter(
    500_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Minimum mass media campaign budget",
    display_name="Minimum Mass Media Campaign Budget",
    unit="USD",
    keywords=["campaign", "media", "budget", "min", "500.0m"]
)  # $500M minimum for mass media

CAMPAIGN_MEDIA_BUDGET_MAX = Parameter(
    1_000_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Maximum mass media campaign budget",
    display_name="Maximum Mass Media Campaign Budget",
    unit="USD",
    keywords=["campaign", "media", "budget", "max", "1.0b"]
)  # $1B maximum for mass media

CAMPAIGN_STAFF_BUDGET = Parameter(
    40_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Campaign core team staff budget",
    display_name="Campaign Core Team Staff Budget",
    unit="USD",
    keywords=["campaign", "staff", "budget", "40.0m"]
)  # $40M for core team

# Detailed campaign budget line items (in millions USD)
CAMPAIGN_LEGAL_AI_BUDGET = Parameter(
    50_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="AI-assisted legal work budget",
    display_name="AI-Assisted Legal Work Budget",
    unit="USD",
    keywords=["campaign", "legal", "budget", "50.0m"]
)

CAMPAIGN_VIRAL_CONTENT_BUDGET = Parameter(
    40_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Viral marketing content creation budget",
    display_name="Viral Marketing Content Creation Budget",
    unit="USD",
    keywords=["campaign", "viral", "content", "budget", "40.0m"]
)

CAMPAIGN_COMMUNITY_ORGANIZING = Parameter(
    30_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Community organizing and ambassador program budget",
    display_name="Community Organizing and Ambassador Program Budget",
    unit="USD",
    keywords=["campaign", "community", "organizing", "30.0m"]
)

CAMPAIGN_LOBBYING_US = Parameter(
    50_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="US lobbying campaign budget",
    display_name="US Lobbying Campaign Budget",
    unit="USD",
    keywords=["campaign", "lobbying", "50.0m"]
)

CAMPAIGN_LOBBYING_EU = Parameter(
    40_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="EU lobbying campaign budget",
    display_name="EU Lobbying Campaign Budget",
    unit="USD",
    keywords=["campaign", "lobbying", "40.0m"]
)

CAMPAIGN_LOBBYING_G20_MILLIONS = Parameter(
    35_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="G20 countries lobbying budget",
    display_name="G20 Countries Lobbying Budget",
    unit="USD",
    keywords=["campaign", "lobbying", "g20", "millions", "35.0m"]
)

CAMPAIGN_DEFENSE_LOBBYIST_BUDGET = Parameter(
    50_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Budget for co-opting defense industry lobbyists",
    display_name="Budget for Co-Opting Defense Industry Lobbyists",
    unit="USD",
    keywords=["50.0m", "armed forces", "conflict", "lobbyist", "armed conflict", "military action", "warfare"]
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
    keywords=["127.0m", "armed forces", "yearly", "conflict", "costs", "funding", "investment"]
)

CAMPAIGN_SUPER_PAC_BUDGET = Parameter(
    30_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Super PAC campaign expenditures",
    display_name="Super PAC Campaign Expenditures",
    unit="USD",
    keywords=["campaign", "super", "pac", "budget", "30.0m"]
)

CAMPAIGN_OPPOSITION_RESEARCH = Parameter(
    25_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Opposition research and rapid response",
    display_name="Opposition Research and Rapid Response",
    unit="USD",
    keywords=["25.0m", "investigation", "r&d", "science", "study", "discovery", "innovation"]
)

CAMPAIGN_PILOT_PROGRAMS = Parameter(
    30_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Pilot program testing in small countries",
    display_name="Pilot Program Testing in Small Countries",
    unit="USD",
    keywords=["campaign", "pilot", "programs", "30.0m"]
)

CAMPAIGN_LEGAL_WORK = Parameter(
    60_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
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
)

CAMPAIGN_REGULATORY_NAVIGATION = Parameter(
    20_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Regulatory compliance and navigation",
    display_name="Regulatory Compliance and Navigation",
    unit="USD",
    keywords=["20.0m", "approval", "authorization", "oversight", "regulation", "compliance", "regulatory"]
)

CAMPAIGN_LEGAL_DEFENSE = Parameter(
    20_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Legal defense fund",
    display_name="Legal Defense Fund",
    unit="USD",
    keywords=["20.0m", "armed forces", "conflict", "legal", "armed conflict", "military action", "warfare"]
)

CAMPAIGN_DEFENSE_CONVERSION = Parameter(
    50_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
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
)

CAMPAIGN_HEALTHCARE_ALIGNMENT = Parameter(
    35_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Healthcare industry alignment and partnerships",
    display_name="Healthcare Industry Alignment and Partnerships",
    unit="USD",
    keywords=["campaign", "healthcare", "alignment", "35.0m"]
)

CAMPAIGN_TECH_PARTNERSHIPS = Parameter(
    25_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Tech industry partnerships and infrastructure",
    display_name="Tech Industry Partnerships and Infrastructure",
    unit="USD",
    keywords=["campaign", "tech", "partnerships", "25.0m"]
)

CAMPAIGN_CELEBRITY_ENDORSEMENT = Parameter(
    15_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Celebrity and influencer endorsements",
    display_name="Celebrity and Influencer Endorsements",
    unit="USD",
    keywords=["campaign", "celebrity", "endorsement", "15.0m"]
)

CAMPAIGN_INFRASTRUCTURE = Parameter(
    20_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Campaign operational infrastructure",
    display_name="Campaign Operational Infrastructure",
    unit="USD",
    keywords=["campaign", "infrastructure", "20.0m"]
)

CAMPAIGN_CONTINGENCY = Parameter(
    50_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
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
)

CAMPAIGN_TREATY_IMPLEMENTATION = Parameter(
    40_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
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
)

CAMPAIGN_SCALING_PREP = Parameter(
    30_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
    source_type="definition",
    description="Scaling preparation and blueprints",
    display_name="Scaling Preparation and Blueprints",
    unit="USD",
    keywords=["campaign", "scaling", "prep", "30.0m"]
)

CAMPAIGN_PLATFORM_DEVELOPMENT = Parameter(
    35_000_000,
    source_ref="/knowledge/economics/campaign-budget.qmd",
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
)

# Investment tier minimums (in millions USD or thousands USD)
INSTITUTIONAL_INVESTOR_MIN = Parameter(
    10_000_000,
    source_ref="/knowledge/economics/victory-bonds.qmd",
    source_type="definition",
    description="Minimum investment for institutional investors",
    display_name="Minimum Investment for Institutional Investors",
    unit="USD",
    keywords=["10.0m", "impact investing", "pay for success", "debt instrument", "development finance", "fixed income", "impact bond"]
)

FAMILY_OFFICE_INVESTMENT_MIN = Parameter(
    5_000_000,
    source_ref="/knowledge/economics/victory-bonds.qmd",
    source_type="definition",
    description="Minimum investment for family offices",
    display_name="Minimum Investment for Family Offices",
    unit="USD",
    keywords=["5.0m", "impact investing", "pay for success", "capital", "finance", "money", "debt instrument"]
)


# Total system costs
TREATY_TOTAL_ANNUAL_COSTS = Parameter(
    TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED + DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/parameters-and-calculations.qmd#sec-treaty_total_annual_costs",
    source_type="calculated",
    description="Total annual system costs (campaign + dFDA operations)",
    display_name="Total Annual Treaty System Costs",
    unit="USD/year",
    formula="CAMPAIGN_ANNUAL + DFDA_OPEX",
    keywords=["1%", "pragmatic trials", "real world evidence", "one percent", "decentralized trials", "drug agency", "food and drug administration"],
    inputs=['DFDA_ANNUAL_OPEX', 'TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED'],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_ANNUAL_COST_AMORTIZED"] + ctx["DFDA_ANNUAL_OPEX"],
)  # $290M ($0.29B)

# ---
# COMBINED ECONOMICS
# ---

# Basic annual benefits (peace dividend + R&D savings only, excludes regulatory delay & other benefits)
TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS = Parameter(
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + DFDA_RD_GROSS_SAVINGS_ANNUAL,
    source_ref="/knowledge/appendix/parameters-and-calculations.qmd#sec-treaty_peace_plus_rd_annual_benefits",
    source_type="calculated",
    description="Basic annual benefits: peace dividend + dFDA R&D savings only (2 of 8 benefit categories, excludes regulatory delay value)",
    display_name="1% treaty Basic Annual Benefits (Peace + R&D Savings)",
    unit="USD/year",
    formula="PEACE_DIVIDEND + DFDA_RD_SAVINGS",
    keywords=["1%", "pragmatic trials", "real world evidence", "one percent", "conflict resolution", "decentralized trials", "drug agency", "basic benefits"],
    inputs=["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT", "DFDA_RD_GROSS_SAVINGS_ANNUAL"],
    compute=lambda ctx: ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"] + ctx["DFDA_RD_GROSS_SAVINGS_ANNUAL"]
)  # $155.05B (peace + R&D only)

# ---
# FINANCIAL PARAMETERS - NPV ANALYSIS
# ---

# NPV analysis parameters
# Source: brain/book/appendix/dfda-calculation-framework.qmd
NPV_DISCOUNT_RATE_STANDARD = Parameter(
    0.03,
    source_ref="",
    source_type="definition",
    description="Standard discount rate for NPV analysis (3% annual, social discount rate)",
    display_name="Standard Discount Rate for NPV Analysis",
    unit="rate",
    latex=r"r = 0.03 \text{ (discount rate)}",
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
    validation_max=0.10   # Ceiling: High corporate rate (inappropriate for health)
)  # 3% annual social discount rate (r)

NPV_TIME_HORIZON_YEARS = Parameter(
    10, source_ref="", source_type="definition", description="Standard time horizon for NPV analysis", unit="years",
    display_name="Standard Time Horizon for NPV Analysis",
    latex=r"T = 10 \text{ (time horizon, years)}",
    keywords=["npv", "time", "horizon", "years"],
    distribution="fixed",  # Methodological choice: standard 10-year NPV analysis window
)  # Standard 10-year analysis window (T)

# ---
# FINANCIAL PARAMETERS - NPV MODEL COMPONENTS
# ---

# NPV Model - Component Costs
# Core platform and broader initiative costs (for detailed breakdowns)
DFDA_NPV_UPFRONT_COST = Parameter(
    40_000_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="definition",
    description="dFDA core platform build cost",
    display_name="dFDA Core Platform Build Cost",
    unit="USD",
    keywords=["40.0m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(25_000_000, 65_000_000),  # $25M-$65M (±40% - IT projects have high variance)
)  # $40M core platform build

DIH_NPV_UPFRONT_COST_INITIATIVES = Parameter(
    229_750_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="definition",
    description="DIH broader initiatives upfront cost (medium case)",
    display_name="DIH Broader Initiatives Upfront Cost",
    unit="USD",
    keywords=["229.8m", "pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials"],
    distribution="lognormal",
    confidence_interval=(150_000_000, 350_000_000),  # $150M-$350M (±40%)
)  # $228M medium case broader initiatives

DFDA_NPV_ANNUAL_OPEX = Parameter(
    18_950_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="definition",
    description="dFDA core platform annual opex (midpoint of $11-26.5M)",
    display_name="dFDA Core Platform Annual OPEX",
    unit="USD/year",
    keywords=["18.9m", "pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency"],
    distribution="lognormal",
    confidence_interval=(11_000_000, 26_500_000),  # $11M-$26.5M (actual range from source)
)  # $19M core platform (midpoint of $11-26.5M)

DIH_NPV_ANNUAL_OPEX_INITIATIVES = Parameter(
    21_100_000,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="definition",
    description="DIH broader initiatives annual opex (medium case)",
    display_name="DIH Broader Initiatives Annual OPEX",
    unit="USD/year",
    keywords=["21.1m", "pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials"],
    distribution="lognormal",
    confidence_interval=(14_000_000, 32_000_000),  # $14M-$32M (±30%)
)  # $21.1M medium case broader initiatives

# NPV Model - Primary Parameters (dFDA-specific)
# Total upfront costs (C0): combines core dFDA platform + broader DIH initiative setup
DFDA_NPV_UPFRONT_COST_TOTAL = Parameter(
    DFDA_NPV_UPFRONT_COST + DIH_NPV_UPFRONT_COST_INITIATIVES,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="Total NPV upfront costs (dFDA core + DIH initiatives)",
    display_name="dFDA Total NPV Upfront Costs",
    unit="USD",
    formula="DFDA_BUILD + DIH_INITIATIVES",
    latex=r"C_0 = \$0.040B + \$0.22975B = \$0.26975B \text{ (upfront cost)}",
    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials", "drug agency"],
    # Uncertainty derived from inputs (DFDA_BUILD + DIH_INITIATIVES)
    validation_min=150_000_000,  # Floor: MVP + essential initiatives only
    validation_max=800_000_000,  # Ceiling: Full scope creep + regulatory capture (raised from $500M)
    inputs=['DFDA_NPV_UPFRONT_COST', 'DIH_NPV_UPFRONT_COST_INITIATIVES'],
    compute=lambda ctx: ctx["DFDA_NPV_UPFRONT_COST"] + ctx["DIH_NPV_UPFRONT_COST_INITIATIVES"],
)  # C0 = $0.26975B

# Total annual operational costs (Cop): combines core dFDA platform + broader DIH initiative annual costs
DFDA_NPV_ANNUAL_OPEX_TOTAL = Parameter(
    DFDA_NPV_ANNUAL_OPEX + DIH_NPV_ANNUAL_OPEX_INITIATIVES,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-costs",
    source_type="calculated",
    description="Total NPV annual opex (dFDA core + DIH initiatives)",
    display_name="dFDA Total NPV Annual OPEX",
    unit="USD/year",
    formula="DFDA_OPEX + DIH_OPEX",
    latex=r"C_{op} = \$0.01895B + \$0.02110B = \$0.04005B \text{ (annual operational cost)}",
    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "decentralized trials", "drug agency"],
    inputs=['DFDA_NPV_ANNUAL_OPEX', 'DIH_NPV_ANNUAL_OPEX_INITIATIVES'],
    compute=lambda ctx: ctx["DFDA_NPV_ANNUAL_OPEX"] + ctx["DIH_NPV_ANNUAL_OPEX_INITIATIVES"],
)  # Cop = $0.04005B

# dFDA adoption curve: linear ramp from 0% to 100% over 5 years, then constant at 100%
DFDA_NPV_ADOPTION_RAMP_YEARS = Parameter(
    5,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#adoption-curve",
    source_type="definition",
    description="Years to reach full dFDA adoption",
    display_name="Years to Reach Full dFDA Adoption",
    unit="years",
    keywords=["pragmatic trials", "real world evidence", "deployment rate", "market penetration", "participation rate", "uptake", "usage rate"]
)  # Years to reach full adoption

# Calculated NPV values for dFDA
DFDA_NPV_PV_ANNUAL_OPEX = Parameter(
    DFDA_NPV_ANNUAL_OPEX_TOTAL
    * (1 - (1 + NPV_DISCOUNT_RATE_STANDARD) ** -NPV_TIME_HORIZON_YEARS)
    / NPV_DISCOUNT_RATE_STANDARD,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-calculation",
    source_type="calculated",
    description="Present value of annual opex over 10 years (NPV formula)",
    display_name="dFDA Present Value of Annual OPEX Over 10 Years",
    unit="USD",
    formula="OPEX × [(1 - (1 + r)^-T) / r]",
    latex=r"PV_{opex} = \$0.04005B \times \frac{1 - 1.08^{-10}}{0.08} \approx \$0.269B",
    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "yearly"],
    inputs=['DFDA_NPV_ANNUAL_OPEX_TOTAL', 'NPV_DISCOUNT_RATE_STANDARD', 'NPV_TIME_HORIZON_YEARS'],
    compute=lambda ctx: ctx["DFDA_NPV_ANNUAL_OPEX_TOTAL"]
    * (1 - (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** -ctx["NPV_TIME_HORIZON_YEARS"])
    / ctx["NPV_DISCOUNT_RATE_STANDARD"],
)
DFDA_NPV_TOTAL_COST = Parameter(
    DFDA_NPV_UPFRONT_COST_TOTAL + DFDA_NPV_PV_ANNUAL_OPEX,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-total-cost",
    source_type="calculated",
    description="Total NPV cost (upfront + PV of annual opex)",
    display_name="dFDA Total NPV Cost",
    unit="USD",
    formula="UPFRONT + PV_OPEX",
    latex=r"TotalCost_{NPV} = \$0.26975B + \$0.269B \approx \$0.54B",
    keywords=["pragmatic trials", "real world evidence", "decentralized trials", "drug agency", "food and drug administration", "medicines agency", "costs"],
    inputs=['DFDA_NPV_PV_ANNUAL_OPEX', 'DFDA_NPV_UPFRONT_COST_TOTAL'],
    compute=lambda ctx: ctx["DFDA_NPV_UPFRONT_COST_TOTAL"] + ctx["DFDA_NPV_PV_ANNUAL_OPEX"],
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
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-benefit",
    source_type="calculated",
    description="NPV of dFDA R&D savings only with 5-year adoption ramp (10-year horizon, most conservative financial estimate)",
    display_name="NPV of dFDA Benefits (R&D Only, 10-Year Discounted)",
    unit="USD",
    formula="Sum of discounted annual net R&D savings with linear adoption ramp",
    latex=r"PV_{benefits} = \sum_{t=1}^{10} \frac{NetSavings_{RD} \times \min(t,5)/5}{(1+r)^t} \approx \$249.3B \text{ (5-year linear adoption ramp)}",
    keywords=["pragmatic trials", "real world evidence", "deployment rate", "market penetration", "participation rate", "uptake", "usage rate", "conservative"],
    inputs=['DFDA_NET_SAVINGS_RD_ONLY_ANNUAL', 'NPV_DISCOUNT_RATE_STANDARD'],
    compute=lambda ctx: sum(
        [
            ctx["DFDA_NET_SAVINGS_RD_ONLY_ANNUAL"] * (min(year, 5) / 5) / (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** year
            for year in range(1, 11)
        ]
    ),
)  # ~$249.3B NPV of R&D savings only (conservative financial case)

DFDA_NPV_NET_BENEFIT_RD_ONLY = Parameter(
    DFDA_NPV_BENEFIT_RD_ONLY,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#npv-net-benefit",
    source_type="calculated",
    description="NPV net benefit using R&D savings only (most conservative financial estimate, excludes regulatory delay health value)",
    display_name="NPV Net Benefit (R&D Only, Conservative)",
    unit="USD",
    formula="NPV of net R&D savings with 5-year linear adoption ramp",
    latex=r"Benefit_{NPV} = \sum_{t=1}^{10} \frac{NetSavings_{RD} \times \min(t,5)/5}{(1+r)^t} \approx \$249.3B \text{ (5-year linear adoption ramp)}",
    keywords=["pragmatic trials", "real world evidence", "deployment rate", "market penetration", "participation rate", "uptake", "usage rate", "conservative"],
    inputs=['DFDA_NPV_BENEFIT_RD_ONLY'],
    compute=lambda ctx: ctx["DFDA_NPV_BENEFIT_RD_ONLY"],
)  # ~$249.3B (R&D savings only, most defensible financial case)

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
# Source: brain/book/appendix/dfda-roi-calculations.qmd NPV analysis
DFDA_ROI_RD_ONLY = Parameter(
    DFDA_NPV_BENEFIT_RD_ONLY / DFDA_NPV_TOTAL_COST,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd#roi-simple",
    source_type="calculated",
    description="ROI from dFDA R&D savings only (10-year NPV, most conservative estimate)",
    display_name="ROI from dFDA R&D Savings Only",
    unit="ratio",
    formula="NPV_BENEFIT ÷ NPV_TOTAL_COST",
    latex=r"ROI_{RD} = \frac{\$249.3B}{\$0.54B} \approx 463",
    keywords=["pragmatic trials", "real world evidence", "bcr", "benefit cost ratio", "economic return", "investment return", "low estimate"],
    inputs=["DFDA_RD_GROSS_SAVINGS_ANNUAL", "DFDA_ANNUAL_OPEX", "NPV_DISCOUNT_RATE_STANDARD", "DFDA_NPV_UPFRONT_COST_TOTAL"],
    compute=lambda ctx: (
        sum([
            (ctx["DFDA_RD_GROSS_SAVINGS_ANNUAL"] - ctx["DFDA_ANNUAL_OPEX"]) * (min(year, 5) / 5) / (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** year
            for year in range(1, 11)
        ]) / (
            ctx["DFDA_NPV_UPFRONT_COST_TOTAL"] + ctx["DFDA_ANNUAL_OPEX"] * ((1 - (1 + ctx["NPV_DISCOUNT_RATE_STANDARD"]) ** -10) / ctx["NPV_DISCOUNT_RATE_STANDARD"])
        )
    )
)  # ~463:1 - Most conservative, R&D cost savings only (NPV-adjusted)


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
# - Central (1%): Ultra-conservative - assumes 99% chance of failure
# - Floor (0.1%): Near-impossibility scenarios (gridlock, competing crises)
# - Ceiling (10%): Optimistic scenario where major crisis creates political window
POLITICAL_SUCCESS_PROBABILITY = Parameter(
    0.01,  # Central estimate: 1% - assumes 99% failure rate, yet still 7x better than bed nets
    source_ref=ReferenceID.ICBL_OTTAWA_TREATY,
    source_type="external",
    confidence="low",
    description="Estimated probability of treaty ratification and sustained implementation. "
                "Central estimate 1% is ultra-conservative. This assumes 99% chance of failure. ",
    display_name="Political Success Probability",
    unit="rate",
    distribution=DistributionType.BETA,  # Bounded [0,1], appropriate for probabilities
    confidence_interval=(0.001, 0.10),  # 0.1% floor to 10% ceiling
    std_error=0.02,  # Tighter spread around 1% central
    keywords=["probability", "political", "treaty", "ratification", "implementation", "uncertainty",
              "adoption", "success", "campaign", "voting", "referendum"],
)

# NOTE: DFDA_EXPECTED_ROI is defined later in the file (after TREATY_ROI_LAG_ELIMINATION)
# because it depends on that parameter which is calculated from other treaty parameters.

# ---
# VICTORY SOCIAL IMPACT BONDS
# ---

# VICTORY Social Impact Bonds
# Source: brain/book/economics/victory-bonds.qmd
VICTORY_BOND_FUNDING_PCT = Parameter(
    0.10,
    source_ref="",
    source_type="definition",
    description="Percentage of captured dividend funding VICTORY bonds (10%)",
    display_name="Percentage of Captured Dividend Funding Victory Bonds",
    unit="rate",
    keywords=["10%", "social impact bond", "sib", "impact investing", "pay for success", "investor return", "development impact bond"],
    distribution="fixed",  # Policy choice: bond allocation percentage is a design decision
)  # 10% of captured dividend funds bonds
VICTORY_BOND_ANNUAL_PAYOUT = Parameter(
    TREATY_ANNUAL_FUNDING * VICTORY_BOND_FUNDING_PCT,
    source_ref="",
    source_type="definition",
    description="Annual VICTORY bond payout (treaty funding × bond percentage)",
    display_name="Annual Victory Bond Payout",
    unit="USD/year",
    formula="TREATY_FUNDING × BOND_PCT",
    keywords=["social impact bond", "sib", "impact investing", "pay for success", "investor return", "development impact bond", "bcr"],
    inputs=['TREATY_ANNUAL_FUNDING', 'VICTORY_BOND_FUNDING_PCT'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] * ctx["VICTORY_BOND_FUNDING_PCT"],
)  # $2.718B
VICTORY_BOND_ANNUAL_RETURN_PCT = Parameter(
    VICTORY_BOND_ANNUAL_PAYOUT / TREATY_CAMPAIGN_TOTAL_COST,
    source_ref="",
    source_type="definition",
    description="Annual return percentage for VICTORY bondholders",
    display_name="Annual Return Percentage for Victory Bondholders",
    unit="rate",
    formula="PAYOUT ÷ CAMPAIGN_COST",
    latex=r"Return = \$2.718B / \$1B = 2.718 = 271.8\%",
    keywords=["social impact bond", "sib", "impact investing", "pay for success", "investor return", "development impact bond", "bcr"]
)  # 271.8% (reported as 270%)
DIVIDEND_COVERAGE_FACTOR = Parameter(
    TREATY_ANNUAL_FUNDING / DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/strategy/roadmap.qmd#sustainability",
    source_type="calculated",
    description="Coverage factor of treaty funding vs dFDA opex (sustainability margin)",
    display_name="Coverage Factor of Treaty Funding vs dFDA OPEX",
    unit="ratio",
    formula="TREATY_FUNDING ÷ DFDA_OPEX",
    latex=r"Coverage = \$27.18B / \$0.04B = 679x",
    keywords=["pragmatic trials", "real world evidence", "multiple", "decentralized trials", "drug agency", "food and drug administration", "international agreement"],
    inputs=['DFDA_ANNUAL_OPEX', 'TREATY_ANNUAL_FUNDING'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] / ctx["DFDA_ANNUAL_OPEX"],
)  # ~679x
DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL = Parameter(
    TREATY_ANNUAL_FUNDING - VICTORY_BOND_ANNUAL_PAYOUT,
    source_ref="",
    source_type="definition",
    description="Annual funding for medical research (treaty funding minus bond payouts)",
    display_name="DIH Annual Funding for Medical Research",
    unit="USD/year",
    formula="TREATY_FUNDING - BOND_PAYOUT",
    latex=r"ResearchFunding = \$27.18B - \$2.718B = \$24.462B",
    keywords=["impact investing", "pay for success", "distributed research", "global research", "open science", "debt instrument", "development finance"],
    inputs=['TREATY_ANNUAL_FUNDING', 'VICTORY_BOND_ANNUAL_PAYOUT'],
    compute=lambda ctx: ctx["TREATY_ANNUAL_FUNDING"] - ctx["VICTORY_BOND_ANNUAL_PAYOUT"],
)  # $24.3B/year
DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL = Parameter(
    DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL - DFDA_ANNUAL_OPEX,
    source_ref="/knowledge/economics/economics.qmd#funding-allocation",
    source_type="calculated",
    description="Annual clinical trial patient subsidies (all medical research funds after dFDA operations)",
    display_name="Annual Clinical Trial Patient Subsidies",
    unit="USD/year",
    formula="MEDICAL_RESEARCH_FUNDING - DFDA_OPEX",
    latex=r"TrialSubsidies = \$24.462B - \$0.04B = \$24.422B",
    keywords=["pragmatic trials", "real world evidence", "distributed research", "global research", "open science", "rct", "patient subsidy"],
    inputs=['DFDA_ANNUAL_OPEX', 'DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL'],
    compute=lambda ctx: ctx["DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL"] - ctx["DFDA_ANNUAL_OPEX"],
)  # $24.422B/year - ALL remaining funds go to subsidizing patient trial participation

DIH_PATIENTS_FUNDABLE_ANNUALLY = Parameter(
    DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL / RECOVERY_TRIAL_COST_PER_PATIENT,
    source_ref="/knowledge/economics/economics.qmd#funding-allocation",
    source_type="calculated",
    description="Number of patients fundable annually at RECOVERY trial cost",
    display_name="Patients Fundable Annually",
    unit="patients/year",
    formula="TRIAL_SUBSIDIES ÷ COST_PER_PATIENT",
    keywords=["trial", "participant", "enrollment", "capacity", "patient"],
    inputs=['DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL', 'RECOVERY_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL"] / ctx["RECOVERY_TRIAL_COST_PER_PATIENT"],
)  # 48.8 million patients/year

# Funding allocation percentages (calculated from absolute values)
DIH_TREASURY_MEDICAL_RESEARCH_PCT = Parameter(
    DIH_TREASURY_TO_MEDICAL_RESEARCH_ANNUAL / TREATY_ANNUAL_FUNDING,
    source_type="definition",
    source_ref="/knowledge/economics/economics.qmd#funding-allocation",
    description="Percentage of treaty funding allocated to medical research (after bond payouts)",
    display_name="Medical Research Percentage of Treaty Funding",
    unit="rate",
    formula="MEDICAL_RESEARCH_FUNDING / TREATY_FUNDING",
    latex=r"MedicalResearchPct = \$24.462B / \$27.18B = 0.90 = 90\%",
    confidence="high",
    keywords=["allocation", "percentage", "medical research", "funding"],
)  # 90%

DIH_TREASURY_TRIAL_SUBSIDIES_PCT = Parameter(
    DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL / TREATY_ANNUAL_FUNDING,
    source_type="definition",
    source_ref="/knowledge/economics/economics.qmd#funding-allocation",
    description="Percentage of treaty funding going directly to patient trial subsidies",
    display_name="Patient Trial Subsidies Percentage of Treaty Funding",
    unit="rate",
    formula="TRIAL_SUBSIDIES / TREATY_FUNDING",
    latex=r"TrialSubsidiesPct = \$24.422B / \$27.18B = 0.8986 = 89.86\%",
    confidence="high",
    keywords=["allocation", "percentage", "patient", "trial", "subsidy"],
)  # 89.86%

DFDA_OPEX_PCT_OF_TREATY_FUNDING = Parameter(
    DFDA_ANNUAL_OPEX / TREATY_ANNUAL_FUNDING,
    source_type="definition",
    source_ref="/knowledge/economics/economics.qmd#funding-allocation",
    description="Percentage of treaty funding allocated to dFDA platform overhead",
    display_name="dFDA Overhead Percentage of Treaty Funding",
    unit="rate",
    formula="DFDA_OPEX / TREATY_FUNDING",
    latex=r"DFDAOpexPct = \$0.04B / \$27.18B = 0.00147 = 0.15\%",
    confidence="high",
    keywords=["allocation", "percentage", "overhead", "platform", "opex"],
)  # 0.15%

SUGAR_SUBSIDY_COST_PER_PERSON_ANNUAL = Parameter(
    10,
    source_ref=ReferenceID.SUGAR_SUBSIDIES_COST,
    source_type="external",
    description="Annual cost of sugar subsidies per person",
    display_name="Annual Cost of Sugar Subsidies per Person",
    unit="USD/person/year",
    keywords=["average person", "yearly", "costs", "funding", "investment", "household benefit", "typical individual"]
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
)

TOTAL_RESEARCH_FUNDING_WITH_TREATY = Parameter(
    GLOBAL_MED_RESEARCH_SPENDING + TREATY_ANNUAL_FUNDING,
    source_ref="/knowledge/economics/economics.qmd",
    source_type="calculated",
    description="Total global research funding (baseline + 1% treaty funding)",
    display_name="Total Global Research Funding (Baseline + 1% treaty Funding)",
    unit="USD",
    formula="GLOBAL_MED_RESEARCH_SPENDING + TREATY_ANNUAL_FUNDING",
    keywords=["research", "funding", "total", "dih", "treaty"],
    inputs=['GLOBAL_MED_RESEARCH_SPENDING', 'TREATY_ANNUAL_FUNDING'],
    compute=lambda ctx: ctx["GLOBAL_MED_RESEARCH_SPENDING"] + ctx["TREATY_ANNUAL_FUNDING"],
)

# Trial Capacity Multiplier (Simple Economic Calculation)
# DIH funding can support 48.8M patients/year at RECOVERY trial cost ($500/patient)
# Current global trial capacity: 1.9M patients/year (IQVIA 2022)
# Capacity Multiplier = DIH capacity / Current capacity
TRIAL_CAPACITY_MULTIPLIER = Parameter(
    DIH_PATIENTS_FUNDABLE_ANNUALLY / CURRENT_TRIAL_SLOTS_AVAILABLE,
    source_type="calculated",
    description="Trial capacity multiplier from DIH funding capacity vs. current global trial participation",
    display_name="Trial Capacity Multiplier",
    unit="ratio",
    formula="DIH_PATIENTS_FUNDABLE ÷ CURRENT_TRIAL_SLOTS",
    keywords=["pragmatic trials", "real world evidence", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "multiple"],
    inputs=['CURRENT_TRIAL_SLOTS_AVAILABLE', 'DIH_PATIENTS_FUNDABLE_ANNUALLY'],
    compute=lambda ctx: ctx["DIH_PATIENTS_FUNDABLE_ANNUALLY"] / ctx["CURRENT_TRIAL_SLOTS_AVAILABLE"],
)  # 25.7x trial capacity multiplier from simple funding economics

TRIAL_CAPACITY_CUMULATIVE_YEARS_20YR = Parameter(
    int(TRIAL_CAPACITY_MULTIPLIER * 20),
    source_type="calculated",
    description="Cumulative trial-capacity-equivalent years over 20-year period",
    display_name="Cumulative Trial Capacity Years Over 20 Years",
    unit="years",
    formula="TRIAL_CAPACITY_MULTIPLIER × 20 YEARS",
    latex=r"Capacity_{20yr} = 25.7 \times 20 = 514 \text{ years}",
    keywords=["trial", "capacity", "cumulative", "20 years"],
    inputs=['TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: int(ctx["TRIAL_CAPACITY_MULTIPLIER"] * 20),
)  # ~514 trial-capacity-equivalent years (25.7x capacity × 20 years)

# dFDA System Targets (using trial capacity multiplier)
DFDA_TRIALS_PER_YEAR_CAPACITY = Parameter(
    int(CURRENT_TRIALS_PER_YEAR * TRIAL_CAPACITY_MULTIPLIER),
    source_type="calculated",
    description="Maximum trials per year possible with trial capacity multiplier",
    display_name="dFDA Maximum Trials per Year",
    unit="trials/year",
    formula="CURRENT_TRIALS × TRIAL_CAPACITY_MULTIPLIER",
    keywords=["pragmatic trials", "real world evidence", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect"],
    inputs=['CURRENT_TRIALS_PER_YEAR', 'TRIAL_CAPACITY_MULTIPLIER'],
    compute=lambda ctx: int(ctx["CURRENT_TRIALS_PER_YEAR"] * ctx["TRIAL_CAPACITY_MULTIPLIER"]),
)  # Maximum trials/year possible with trial capacity multiplier


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
    keywords=["2024", "8.0b", "people", "worldwide", "citizens", "individuals", "inhabitants"]
)  # UN World Population Prospects 2022

GLOBAL_DAILY_DEATHS_CURABLE_DISEASES = Parameter(
    150000,
    source_ref=ReferenceID.DEATHS_FROM_TREATABLE_DISEASES_15M,
    source_type="external",
    description="Daily deaths from curable diseases globally",
    display_name="Daily Deaths from Curable Diseases Globally",
    unit="deaths/day",
    keywords=["150k", "day", "each day", "per day", "worldwide", "fatalities", "casualties"],
    distribution="lognormal",
    confidence_interval=(120_000, 180_000),  # ±20% - disease mortality estimates vary by methodology
)  # Daily deaths from curable diseases

# Annual disease deaths (calculated from daily)
GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES = Parameter(
    GLOBAL_DAILY_DEATHS_CURABLE_DISEASES * DAYS_PER_YEAR,
    source_ref="/knowledge/economics/economics.qmd",
    source_type="calculated",
    description="Annual deaths from curable diseases globally",
    display_name="Annual Deaths from Curable Diseases Globally",
    unit="deaths/year",
    formula="GLOBAL_DAILY_DEATHS_CURABLE_DISEASES × DAYS_PER_YEAR",
    latex=r"Deaths_{annual} = 150{,}000 \times 365 = 54.75M",
    keywords=["day", "each day", "per day", "worldwide", "yearly", "fatalities", "casualties"],
    inputs=['GLOBAL_DAILY_DEATHS_CURABLE_DISEASES'],
    compute=lambda ctx: ctx["GLOBAL_DAILY_DEATHS_CURABLE_DISEASES"] * DAYS_PER_YEAR,
)  # 54.75 million deaths/year

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
)  # $109.1 trillion annually

GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST + GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL + GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL,
    source_ref="/knowledge/appendix/humanity-budget-overview.qmd",
    source_type="calculated",
    description="Total annual cost of war and disease with all externalities (direct + indirect costs for both)",
    display_name="Total Annual Cost of War and Disease with All Externalities",
    unit="USD/year",
    formula="WAR_TOTAL_COSTS + SYMPTOMATIC_TREATMENT + DISEASE_BURDEN",
    keywords=["deadweight loss", "economic damage", "productivity loss", "gdp loss", "worldwide", "yearly", "conflict"],
    inputs=['GLOBAL_ANNUAL_WAR_TOTAL_COST', 'GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL', 'GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL'],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_TOTAL_COST"] + ctx["GLOBAL_SYMPTOMATIC_DISEASE_TREATMENT_ANNUAL"] + ctx["GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL"],
)  # $128.6 trillion = $11.355T (war with externalities) + $8.2T + $109T

# Defense and research participation rates
DEFENSE_SECTOR_RETENTION_PCT = Parameter(
    0.99,
    source_ref="",
    source_type="definition",
    description="Percentage of budget defense sector keeps under 1% treaty",
    display_name="Percentage of Budget Defense Sector Keeps Under 1% treaty",
    unit="rate",
    keywords=["99%", "armed forces", "international agreement", "peace treaty", "conflict", "sector", "retention"]
)  # 99% retention

CURRENT_CLINICAL_TRIAL_PARTICIPATION_RATE = Parameter(
    0.0006,
    source_ref=ReferenceID.CLINICAL_TRIAL_PATIENT_PARTICIPATION_RATE,
    source_type="external",
    description="Current clinical trial participation rate (0.06% of population)",
    display_name="Current Clinical Trial Participation Rate",
    unit="rate",
    keywords=["0%", "rct", "people", "clinical study", "clinical trial", "research trial", "randomized controlled trial"]
)  # 0.06% participation

PATIENT_WILLINGNESS_TRIAL_PARTICIPATION_PCT = Parameter(
    0.448,
    source_ref=ReferenceID.PATIENT_WILLINGNESS_CLINICAL_TRIALS,
    source_type="external",
    description="Patient willingness to participate in drug trials (44.8% in surveys, 88% when actually approached)",
    display_name="Patient Willingness to Participate in Clinical Trials",
    unit="percentage",
    confidence="medium",
    keywords=["willingness", "willing", "volunteer", "interest", "clinical trial", "participation", "survey"]
)  # 44.8% willing for drug trials specifically

US_MILITARY_SPENDING_PCT_GDP = Parameter(
    0.035,
    source_ref=ReferenceID.US_MILITARY_BUDGET_3_5_PCT_GDP,
    source_type="external",
    description="US military spending as percentage of GDP (2024)",
    display_name="US Military Spending as Percentage of GDP",
    unit="rate",
    keywords=["4%", "dod", "pentagon", "national security", "army", "navy", "armed forces"]
)  # 3.5% of GDP

# Rare diseases
RARE_DISEASES_COUNT_GLOBAL = Parameter(
    7000,
    source_ref=ReferenceID.N95_PCT_DISEASES_NO_TREATMENT,
    source_type="external",
    description="Total number of rare diseases globally",
    display_name="Total Number of Rare Diseases Globally",
    unit="diseases",
    keywords=["7k", "worldwide", "illness", "rare", "diseases", "count", "international"]
)  # ~7,000 rare diseases

# Historical terrorism deaths
TERRORISM_DEATHS_911 = Parameter(
    2996,
    source_ref=ReferenceID.CHANCE_OF_DYING_FROM_TERRORISM_1_IN_30M,
    source_type="external",
    description="Deaths from 9/11 terrorist attacks",
    display_name="Deaths from 9/11 Terrorist Attacks",
    unit="deaths",
    keywords=["911", "3k", "fatalities", "casualties", "mortality", "terrorism", "loss of life"]
)  # 2,996 deaths

# Research acceleration multipliers
# Calculated ratios and comparisons
DISEASE_VS_TERRORISM_DEATHS_RATIO = Parameter(
    GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES / TERRORISM_DEATHS_911,
    source_ref="/knowledge/economics/economics.qmd",
    source_type="definition",
    description="Ratio of annual disease deaths to 9/11 terrorism deaths",
    display_name="Ratio of Annual Disease Deaths to 9/11 Terrorism Deaths",
    unit="ratio",
    formula="ANNUAL_DISEASE_DEATHS ÷ 911_DEATHS",
    latex=r"\frac{54.75\text{M disease deaths}}{3{,}000\text{ terrorism deaths}} \approx 18{,}274:1",
    keywords=["fatalities", "casualties", "illness", "mortality", "worldwide", "yearly", "disease"],
)  # ~18,274:1

DISEASE_VS_WAR_DEATHS_RATIO = Parameter(
    GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL,
    source_ref="/knowledge/economics/economics.qmd",
    source_type="definition",
    description="Ratio of annual disease deaths to war deaths",
    display_name="Ratio of Annual Disease Deaths to War Deaths",
    unit="ratio",
    formula="ANNUAL_DISEASE_DEATHS ÷ WAR_DEATHS",
    latex=r"\frac{54.75\text{M disease deaths}}{400{,}000\text{ conflict deaths}} \approx 137:1",
    keywords=["armed forces", "conflict", "fatalities", "casualties", "illness", "mortality", "worldwide"],
)  # ~137:1

# Medical research as percentage of disease burden
MEDICAL_RESEARCH_PCT_OF_DISEASE_BURDEN = Parameter(
    GLOBAL_MED_RESEARCH_SPENDING / GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL,
    source_ref="/knowledge/economics/economics.qmd",
    source_type="calculated",
    description="Medical research spending as percentage of total disease burden",
    display_name="Medical Research Spending as Percentage of Total Disease Burden",
    unit="rate",
    formula="MED_RESEARCH ÷ TOTAL_BURDEN",
    latex=r"\frac{\$67.5\text{B}}{\$128.6\text{T}} = 0.052\%",
    keywords=["deadweight loss", "economic damage", "productivity loss", "gdp loss", "investigation", "r&d", "science"],
    inputs=['GLOBAL_MED_RESEARCH_SPENDING', 'GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL'],
    compute=lambda ctx: ctx["GLOBAL_MED_RESEARCH_SPENDING"] / ctx["GLOBAL_TOTAL_HEALTH_AND_WAR_COST_ANNUAL"],
)  # 0.052%

# Per capita calculations
GLOBAL_MILITARY_SPENDING_PER_CAPITA_ANNUAL = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_POPULATION_2024,
    source_ref="/knowledge/problem/cost-of-war.qmd#per-capita",
    source_type="calculated",
    description="Per capita military spending globally",
    display_name="Per Capita Military Spending Globally",
    unit="USD/person/year",
    formula="MILITARY_SPENDING ÷ POPULATION",
    latex=r"PerCapita_{military} = \$2,718B / 8.0B = \$339.75",
    keywords=["dod", "pentagon", "average person", "national security", "army", "individual", "navy"],
    inputs=['GLOBAL_MILITARY_SPENDING_ANNUAL_2024', 'GLOBAL_POPULATION_2024'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_POPULATION_2024"],
)  # $340/person/year

# GiveWell charity comparison
# Source: brain/book/appendix/icer-full-calculation.qmd
GIVEWELL_COST_PER_LIFE_MIN = Parameter(
    3500,
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="GiveWell cost per life saved (Helen Keller International)",
    display_name="Givewell Cost per Life Saved (Minimum)",
    unit="USD/life",
    keywords=["4k", "costs", "funding", "investment", "givewell", "life", "min"]
)  # Helen Keller International Vitamin A

GIVEWELL_COST_PER_LIFE_MAX = Parameter(
    5500,
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="GiveWell cost per life saved (Against Malaria Foundation)",
    display_name="Givewell Cost per Life Saved (Maximum)",
    unit="USD/life",
    keywords=["6k", "costs", "funding", "investment", "givewell", "life", "max"]
)  # Against Malaria Foundation

GIVEWELL_COST_PER_LIFE_AVG = Parameter(
    4500,
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="GiveWell average cost per life saved across top charities",
    display_name="Givewell Average Cost per Life Saved Across Top Charities",
    unit="USD/life",
    keywords=["4k", "costs", "funding", "investment", "givewell", "life", "avg"]
)  # Midpoint of top charities

# Historical public health comparisons
SMALLPOX_ERADICATION_ROI = Parameter(
    280,
    source_ref=ReferenceID.SMALLPOX_ERADICATION_ROI,
    source_type="external",
    description="Return on investment from smallpox eradication campaign",
    display_name="Return on Investment from Smallpox Eradication Campaign",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"]
)  # 159:1 to 280:1 estimated

CHILDHOOD_VACCINATION_ROI = Parameter(
    13,
    source_ref=ReferenceID.CHILDHOOD_VACCINATION_ROI,
    source_type="external",
    description="Return on investment from childhood vaccination programs",
    display_name="Return on Investment from Childhood Vaccination Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"]
)  # 13:1

POLIO_VACCINATION_ROI = Parameter(
    39,
    source_ref=ReferenceID.POLIO_VACCINATION_ROI,
    source_type="external",
    description="Return on investment from sustaining polio vaccination assets and integrating into expanded immunization programs",
    display_name="Return on Investment from Sustaining Polio Vaccination Assets and Integrating into Expanded Immunization Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"]
)  # 39:1 (WHO 2019, 8 priority countries)

MEASLES_VACCINATION_ROI = Parameter(
    14,
    source_ref=ReferenceID.MEASLES_VACCINATION_ROI,
    source_type="external",
    description="Return on investment from measles (MMR) vaccination programs",
    display_name="Return on Investment from Measles Vaccination Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"]
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
)  # ~$15B annual benefit from preventing measles, polio, etc.

WATER_FLUORIDATION_ROI = Parameter(
    23,
    source_ref=ReferenceID.CLEAN_WATER_SANITATION_ROI,
    source_type="external",
    description="Return on investment from water fluoridation programs",
    display_name="Return on Investment from Water Fluoridation Programs",
    unit="ratio",
    keywords=["bcr", "benefit cost ratio", "economic return", "investment return", "return on investment", "benefit", "profit"]
)  # 23:1

# Historical intervention total benefits (for comparison charts)

SMALLPOX_ERADICATION_TOTAL_BENEFIT = Parameter(
    1_420_000_000,
    source_ref=ReferenceID.SMALLPOX_ERADICATION_ROI,
    source_type="external",
    description="Total economic benefit from smallpox eradication campaign",
    display_name="Total Economic Benefit from Smallpox Eradication Campaign",
    unit="USD",
    keywords=["historical", "one-time", "total benefit", "eradication", "public health"]
)  # $1.42B total benefit ($350M + $1,070M benefits, $298M cost, ~159-280:1 ROI)

HUMAN_GENOME_PROJECT_TOTAL_ECONOMIC_IMPACT = Parameter(
    1_000_000_000_000,
    source_ref=ReferenceID.HUMAN_GENOME_AND_GENETIC_EDITING,
    source_type="external",
    description="Estimated total economic impact of Human Genome Project",
    display_name="Estimated Total Economic Impact of Human Genome Project",
    unit="USD",
    keywords=["historical", "one-time", "total benefit", "genomics", "research"]
)  # ~$1T commonly cited economic impact estimate (cost ~$2.7B)

# Annual benefit parameters (used for 100-year cumulative comparisons)

WATER_FLUORIDATION_ANNUAL_BENEFIT = Parameter(
    800_000_000,
    source_ref=ReferenceID.CLEAN_WATER_SANITATION_ROI,
    source_type="external",
    description="Estimated annual global economic benefit from water fluoridation programs",
    display_name="Estimated Annual Global Economic Benefit from Water Fluoridation Programs",
    unit="USD/year",
    keywords=["yearly", "profit", "return", "worldwide", "fluoridation", "dental"]
)  # ~$800M annual benefit

SMOKING_CESSATION_ANNUAL_BENEFIT = Parameter(
    12_000_000_000,
    source_ref="life-expectancy-gains-smoking-reduction",
    source_type="external",
    description="Estimated annual global economic benefit from smoking cessation programs",
    display_name="Estimated Annual Global Economic Benefit from Smoking Cessation Programs",
    unit="USD/year",
    keywords=["yearly", "profit", "return", "worldwide", "tobacco", "smoking"]
)  # ~$12B annual benefit


# ===================================================================
# TREATY BENEFITS (RECURRING ONLY)
# ===================================================================
# Peace Dividend + R&D Savings
# Truly recurring annual benefits = $155.1B/year
# (Health benefits are one-time timeline shifts, NOT perpetual annual)
# ===================================================================

TREATY_RECURRING_BENEFITS_ANNUAL = Parameter(
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + DFDA_BENEFIT_RD_ONLY_ANNUAL,
    source_ref="/knowledge/economics/economics.qmd",
    source_type="calculated",
    description="Truly recurring annual benefits from 1% treaty: peace dividend ($113.6B/year) + R&D savings ($41.5B/year). Note: Health benefits are one-time timeline shifts, NOT included here.",
    display_name="1% treaty Recurring Annual Benefits",
    unit="USD/year",
    formula="PEACE_DIVIDEND + RD_SAVINGS",
    confidence="high",
    keywords=["recurring", "annual", "treaty benefits", "peace dividend", "rd savings", "perpetual"],
    inputs=['DFDA_BENEFIT_RD_ONLY_ANNUAL', 'PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT'],
    compute=lambda ctx: ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"] + ctx["DFDA_BENEFIT_RD_ONLY_ANNUAL"],
)  # $155.1B/year (truly recurring - peace dividend + R&D savings only)

# Backward compatibility alias for deleted parameter
# NOTE: Old parameter incorrectly included amortized one-time health benefits ($149T/year) which was nonsensical
# New parameter correctly shows only truly recurring benefits ($155.1B/year)
TREATY_TOTAL_COMPLETE_BENEFITS_ANNUAL = TREATY_RECURRING_BENEFITS_ANNUAL  # Backward compatibility alias

# Three-tier ROI analysis based on TOTAL one-time health benefits
TREATY_ROI_HISTORICAL_RATE = Parameter(
    HISTORICAL_PROGRESS_ECONOMIC_LOSS_TOTAL / TREATY_CAMPAIGN_TOTAL_COST,
    source_ref="/knowledge/figures/dfda-investment-returns-bar-chart.qmd",
    source_type="calculated",
    description="Treaty ROI based on historical rate of drug development (existing drugs only, conservative floor). Total one-time benefit from avoiding regulatory delay for drugs already in development divided by $1B campaign cost.",
    display_name="Treaty ROI - Historical Rate (Conservative Floor)",
    unit="ratio",
    formula="HISTORICAL_PROGRESS_TOTAL ÷ CAMPAIGN_COST",
    confidence="high",
    keywords=["250920", "historical", "conservative", "floor", "existing drugs", "roi"],
    inputs=['HISTORICAL_PROGRESS_ECONOMIC_LOSS_TOTAL', 'TREATY_CAMPAIGN_TOTAL_COST'],
    compute=lambda ctx: ctx["HISTORICAL_PROGRESS_ECONOMIC_LOSS_TOTAL"] / ctx["TREATY_CAMPAIGN_TOTAL_COST"],
)  # 250,920:1 ROI (conservative floor - existing drugs only)

TREATY_ROI_LAG_ELIMINATION = Parameter(
    DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS / TREATY_CAMPAIGN_TOTAL_COST,
    source_ref="/knowledge/figures/dfda-investment-returns-bar-chart.qmd",
    source_type="calculated",
    description="Treaty ROI based on eliminating the 8.2-year post-safety efficacy lag (PRIMARY METHODOLOGY). Total one-time benefit from disease eradication delay elimination divided by $1B campaign cost. This is the primary ROI estimate for total health benefits.",
    display_name="Treaty ROI - Lag Elimination (PRIMARY)",
    unit="ratio",
    formula="DISEASE_ERADICATION_DELAY_TOTAL ÷ CAMPAIGN_COST",
    latex=r"ROI_{lag\_elimination} = \frac{\$1{,}286T}{\$1.00B} = 1{,}286{,}242:1",
    confidence="medium",
    keywords=["1286242", "lag elimination", "primary", "disease eradication", "roi", "8.2 years"],
    inputs=["DISEASE_ERADICATION_DELAY_DALYS", "STANDARD_ECONOMIC_QALY_VALUE_USD", "TREATY_CAMPAIGN_TOTAL_COST"],
    compute=lambda ctx: (ctx["DISEASE_ERADICATION_DELAY_DALYS"] * ctx["STANDARD_ECONOMIC_QALY_VALUE_USD"]) / ctx["TREATY_CAMPAIGN_TOTAL_COST"]
)  # 1,286,242:1 ROI (PRIMARY - lag elimination)

TREATY_ROI_INNOVATION_ACCELERATION = Parameter(
    DISEASE_ERADICATION_PLUS_ACCELERATION_ECONOMIC_LOSS_TOTAL / TREATY_CAMPAIGN_TOTAL_COST,
    source_ref="/knowledge/figures/dfda-investment-returns-bar-chart.qmd",
    source_type="calculated",
    description="Treaty ROI based on lag elimination plus innovation acceleration effects (OPTIMISTIC UPPER BOUND). Includes cascading innovation effects from eliminating Phase 2-4 cost barriers. Research-backed 2× multiplier represents combined timeline and volume effects (Nature 2023, Woods et al. 2024).",
    display_name="Treaty ROI - Innovation Acceleration (Optimistic)",
    unit="ratio",
    formula="DISEASE_ERADICATION_PLUS_ACCELERATION_TOTAL ÷ CAMPAIGN_COST",
    confidence="low",
    keywords=["2572484", "innovation", "acceleration", "optimistic", "upper bound", "roi"],
    inputs=['DISEASE_ERADICATION_PLUS_ACCELERATION_ECONOMIC_LOSS_TOTAL', 'TREATY_CAMPAIGN_TOTAL_COST'],
    compute=lambda ctx: ctx["DISEASE_ERADICATION_PLUS_ACCELERATION_ECONOMIC_LOSS_TOTAL"] / ctx["TREATY_CAMPAIGN_TOTAL_COST"],
)  # 2,572,484:1 ROI (optimistic - innovation acceleration)

# Backward compatibility alias: TREATY_COMPLETE_ROI_ALL_BENEFITS → TREATY_ROI_LAG_ELIMINATION
# TODO: Refactor 16 files using this to use TREATY_ROI_LAG_ELIMINATION directly
TREATY_COMPLETE_ROI_ALL_BENEFITS = TREATY_ROI_LAG_ELIMINATION  # Alias to PRIMARY (lag elimination) ROI

# ---
# EXPECTED ROI WITH POLITICAL UNCERTAINTY
# ---

# Expected ROI accounting for political implementation uncertainty
# Uses the uncertain POLITICAL_SUCCESS_PROBABILITY - Monte Carlo will sample the full distribution
DFDA_EXPECTED_ROI = Parameter(
    float(TREATY_ROI_LAG_ELIMINATION) * float(POLITICAL_SUCCESS_PROBABILITY),
    source_ref="calculated",
    source_type="calculated",
    description="Expected ROI for 1% treaty accounting for political success probability uncertainty. "
                "Monte Carlo samples POLITICAL_SUCCESS_PROBABILITY from beta(5%, 50%) distribution "
                "to generate full expected value distribution. Central value uses 25% probability.",
    display_name="Expected Treaty ROI (Risk-Adjusted)",
    formula="TREATY_ROI_LAG_ELIMINATION × POLITICAL_SUCCESS_PROBABILITY",
    latex=r"E[ROI] = ROI_{conditional} \times P_{success} = 1{,}286{,}242 \times 0.25 = 321{,}561",
    confidence="low",
    keywords=["expected value", "risk-adjusted", "political risk", "bcr", "benefit cost ratio",
              "economic return", "uncertainty", "monte carlo", "321561"],
    inputs=["TREATY_ROI_LAG_ELIMINATION", "POLITICAL_SUCCESS_PROBABILITY"],
    compute=lambda ctx: ctx["TREATY_ROI_LAG_ELIMINATION"] * ctx["POLITICAL_SUCCESS_PROBABILITY"],
)

# Scale Comparison Parameters (demonstrating intervention magnitude)
# DELETED: OPPORTUNITY_COST_PER_DAY and OPPORTUNITY_COST_PER_SECOND
# Reason: These parameters were conceptually confused. They calculated the daily cost by dividing
# DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS by 8.2 years, but that $529T was itself derived from
# daily disease burden × 8.2 years, making the calculation circular. The daily disease burden
# should be calculated directly from GLOBAL_DAILY_DEATHS_CURABLE_DISEASES (150,000 deaths/day)
# rather than through this circular division.

# ---
# SCENARIO PARAMETERS
# ---

GLOBAL_MILITARY_SPENDING_POST_TREATY_ANNUAL_2024 = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * (1 - TREATY_REDUCTION_PCT),
    source_ref="/knowledge/strategy/treaty-adoption-strategy.qmd#post-treaty",
    source_type="calculated",
    description="Global military spending after 1% treaty reduction",
    display_name="Global Military Spending After 1% Treaty Reduction",
    unit="USD/year",
    formula="MILITARY_SPENDING × (1 - REDUCTION)",
    latex=r"PostTreaty_{military} = \$2,718B \times 0.99 = \$2,690.82B",
    keywords=["2024", "dod", "pentagon", "deployment rate", "market penetration", "participation rate", "national security"],
    inputs=['GLOBAL_MILITARY_SPENDING_ANNUAL_2024', 'TREATY_REDUCTION_PCT'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] * (1 - ctx["TREATY_REDUCTION_PCT"]),
)  # $2,690.82B


TREATMENT_ACCELERATION_YEARS_CURRENT = Parameter(
    17,
    source_ref=ReferenceID.FDA_APPROVAL_TIMELINE_10_YEARS,
    source_type="external",
    description="Traditional FDA drug development timeline",
    display_name="Traditional FDA Drug Development Timeline",
    unit="years",
    keywords=["drug agency", "faster development", "food and drug administration", "innovation speed", "medicines agency", "research velocity", "regulator"]
)  # 12-17 years typical

# ============================================================================
# REGULATORY MORTALITY COST PARAMETERS
# ============================================================================
# Quantitative analysis of Type II regulatory errors (delayed access)
# Based on: "The Human Capital Cost of Regulatory Latency" (2025)
# See: knowledge/appendix/regulatory-mortality-analysis.qmd

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
    keywords=["rct", "clinical study", "clinical trial", "research trial", "randomized controlled trial", "study", "discovery"]
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
    keywords=["deaths prevented", "life saving", "mortality reduction", "deaths averted", "low estimate", "yearly", "cautious"]
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
# - DFDA_ROI_RD_ONLY (463:1):
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
# - Skeptical audiences / conservative pitches: DFDA_ROI_RD_ONLY (463:1)
# - Balanced presentations / general use: DFDA_ROI_RD_PLUS_DELAY (6,489:1) **RECOMMENDED**
# - Academic/comprehensive analyses: Show full range 463:1 to 11,540:1
# - Advocacy (use cautiously): DFDA_ROI_RD_PLUS_DELAY_PLUS_INNOVATION (11,540:1)


# Cost per DALY benchmarks for comparison
BED_NETS_COST_PER_DALY = Parameter(
    89,
    source_ref=ReferenceID.GIVEWELL_COST_PER_LIFE_SAVED,
    source_type="external",
    description="GiveWell cost per DALY for bed nets (midpoint estimate, range $78-100)",
    display_name="Bed Nets Cost per DALY",
    unit="USD/DALY",
    confidence="high",
    keywords=["givewell", "bed nets", "malaria", "cost effectiveness", "benchmark", "comparison"],
    distribution="normal",  # Well-studied intervention with systematic cost tracking
    confidence_interval=(78, 100),  # Documented GiveWell range
)

DEWORMING_COST_PER_DALY = Parameter(
    55,  # Midpoint of $28-82 range from GiveWell 2011 analysis
    source_ref=ReferenceID.DEWORMING_COST_PER_DALY,
    source_type="external",
    description="Cost per DALY for deworming programs (range $28-82, midpoint estimate). GiveWell notes this 2011 estimate is outdated and their current methodology focuses on long-term income effects rather than short-term health DALYs.",
    display_name="Deworming Cost per DALY",
    unit="USD/DALY",
    confidence="low",
    keywords=["givewell", "deworming", "worms", "cost effectiveness", "benchmark", "comparison", "soil-transmitted helminths", "schistosomiasis"]
)

VITAMIN_A_COST_PER_DALY = Parameter(
    37,  # Midpoint of $23-50 India estimate (most conservative published estimate)
    source_ref=ReferenceID.VITAMIN_A_COST_PER_DALY,
    source_type="external",
    description="Cost per DALY for vitamin A supplementation programs (India: $23-50; Africa: $40-255; wide variation by region and baseline VAD prevalence). Using India midpoint as conservative estimate.",
    display_name="Vitamin A Supplementation Cost per DALY",
    unit="USD/DALY",
    confidence="medium",
    keywords=["givewell", "vitamin a", "helen keller", "cost effectiveness", "benchmark", "comparison", "supplementation", "micronutrient"]
)

CHILDHOOD_VACCINATION_COST_PER_DALY = Parameter(
    30,  # Estimated from ROI and benefit parameters; US studies use QALYs not DALYs
    source_type="definition",
    description="Estimated cost per DALY for US childhood vaccination programs. Note: US cost-effectiveness studies primarily use cost per QALY (Quality-Adjusted Life Year) rather than cost per DALY. This estimate is derived from program costs and benefits for comparison purposes only.",
    display_name="Childhood Vaccination Cost per DALY (Estimated)",
    unit="USD/DALY",
    confidence="low",
    keywords=["vaccination", "immunization", "childhood", "cost effectiveness", "benchmark", "comparison", "vaccines for children", "VFC"]
)

# Cost per DALY - Primary cost-effectiveness metric
# Note: ICER (Incremental Cost-Effectiveness Ratio) is not calculated because this is a
# cost-dominant intervention that saves money while improving health. Traditional ICER
# is designed for interventions that cost money, not those that generate net economic surplus.
# Instead, we calculate cost per DALY using only the campaign cost, which understates the
# value since it ignores the $77B/year in economic benefits (R&D savings + peace dividend).

TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT = Parameter(
    TREATY_CAMPAIGN_TOTAL_COST / DISEASE_ERADICATION_DELAY_DALYS,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd",
    source_type="calculated",
    description=f"Cost per DALY averted from one-time timeline shift (8.2 years). This is a conservative estimate that only counts campaign cost ($1B) and ignores all economic benefits ($27B/year funding unlocked + $50B/year R&D savings). For comparison: bed nets cost ${BED_NETS_COST_PER_DALY}/DALY, deworming costs $4-10/DALY. This intervention is {int(BED_NETS_COST_PER_DALY/0.127)}x more cost-effective than bed nets while also being self-funding.",
    display_name="Cost per DALY Averted (Timeline Shift)",
    unit="USD/DALY",
    formula="CAMPAIGN_COST ÷ DALYS_TIMELINE_SHIFT",
    latex=r"\text{Cost/DALY} = \frac{\$1.0B}{7.90B} = \$0.127",
    confidence="high",
    keywords=["bang for buck", "cost effectiveness", "value for money", "disease burden", "cost per daly", "gates foundation", "givewell"],
    inputs=["TREATY_CAMPAIGN_TOTAL_COST", "DISEASE_ERADICATION_DELAY_DALYS"],
    compute=lambda ctx: ctx["TREATY_CAMPAIGN_TOTAL_COST"] / ctx["DISEASE_ERADICATION_DELAY_DALYS"]
)  # $0.127 per DALY (~700x better than bed nets, while being self-funding)

# Expected cost per DALY using the unified political success probability
# The "conservative" label is retained for compatibility, but uses the unified parameter
TREATY_EXPECTED_COST_PER_DALY = Parameter(
    TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT / POLITICAL_SUCCESS_PROBABILITY,
    source_ref="/knowledge/appendix/dfda-cost-benefit-analysis.qmd",
    source_type="calculated",
    description=f"Expected cost per DALY accounting for political success probability uncertainty. "
                f"Monte Carlo samples from beta(5%, 50%) distribution. At the central 25% estimate, "
                f"this is ~{int(BED_NETS_COST_PER_DALY/0.51)}x more cost-effective than bed nets (${BED_NETS_COST_PER_DALY}/DALY).",
    display_name="Expected Cost per DALY (Risk-Adjusted)",
    unit="USD/DALY",
    formula="CONDITIONAL_COST_PER_DALY ÷ POLITICAL_SUCCESS_PROBABILITY",
    latex=r"E[\text{Cost/DALY}] = \frac{\$0.127}{0.25} = \$0.51",
    confidence="low",
    keywords=["expected value", "probability weighted", "cost effectiveness", "gates foundation", "givewell", "political risk", "uncertainty"],
    inputs=["TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT", "POLITICAL_SUCCESS_PROBABILITY"],
    compute=lambda ctx: ctx["TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT"] / ctx["POLITICAL_SUCCESS_PROBABILITY"],
)  # $0.51 per DALY at 25% probability (still ~175x better than bed nets)

# Cost-effectiveness multipliers vs. bed nets
TREATY_VS_BED_NETS_MULTIPLIER = Parameter(
    BED_NETS_COST_PER_DALY / TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT,
    source_type="calculated",
    description="How many times more cost-effective than bed nets (using $89/DALY midpoint estimate)",
    display_name="Cost-Effectiveness vs Bed Nets Multiplier",
    unit="ratio",
    formula="BED_NETS_COST_PER_DALY ÷ TREATY_COST_PER_DALY",
    latex=r"\text{Multiplier} = \frac{\$89}{\$0.127} = 701\times",
    confidence="high",
    inputs=['BED_NETS_COST_PER_DALY', 'TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT'],
    compute=lambda ctx: ctx["BED_NETS_COST_PER_DALY"] / ctx["TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT"],
)

TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER = Parameter(
    BED_NETS_COST_PER_DALY / TREATY_EXPECTED_COST_PER_DALY,
    source_type="calculated",
    description="Expected value multiplier vs bed nets (accounts for political uncertainty)",
    display_name="Expected Cost-Effectiveness vs Bed Nets Multiplier",
    unit="ratio",
    formula="BED_NETS_COST_PER_DALY ÷ TREATY_EXPECTED_COST_PER_DALY",
    latex=r"E[\text{Multiplier}] = \frac{\$89}{\$0.51} = 175\times",
    confidence="low",
    inputs=['BED_NETS_COST_PER_DALY', 'TREATY_EXPECTED_COST_PER_DALY'],
    compute=lambda ctx: ctx["BED_NETS_COST_PER_DALY"] / ctx["TREATY_EXPECTED_COST_PER_DALY"],
)

# ---
# HELPER FUNCTIONS
# ---


def format_parameter_value(param: float | int | str | Parameter, unit: str | None = None) -> str:
    """
    Universal formatter - handles Parameter objects, auto-scales based on value.

    Automatically detects unit from Parameter objects and scales appropriately.
    Works with raw numbers too.

    Args:
        param: Parameter object or raw number
        unit: Optional unit override (auto-detected if param has .unit attribute)

    Returns:
        Formatted string like "$27.18B", "50%", "184.6M deaths", etc.

    Examples:
        >>> format_parameter_value(TREATY_ANNUAL_FUNDING)  # Auto-detects USD unit
        "$27.18B"
        >>> format_parameter_value(27180000000, "USD")  # Manual unit
        "$27.18B"
        >>> format_parameter_value(0.5, "rate")  # Percentage
        "50%"
    """
    # Auto-detect unit from Parameter object
    if unit is None:
        if isinstance(param, Parameter) and param.unit:
            unit = param.unit
        else:
            unit = ""

    # Get raw numeric value
    if isinstance(param, (int, float)):
        value = float(param)
    elif hasattr(param, "__float__"):
        value = float(param)
    else:
        # Parameter object - extract numeric value
        value = float(param)

    # Detect currency parameters
    is_currency = "USD" in unit or "usd" in unit or "dollar" in unit.lower()

    # Detect percentage parameters
    is_percentage = "%" in unit or "percent" in unit.lower() or "rate" in unit.lower()

    # Check if value is already in billions, millions, thousands
    is_in_billions = "billion" in unit.lower()
    is_in_millions = "million" in unit.lower()
    is_in_thousands = "thousand" in unit.lower()

    # Helper to remove trailing zeros
    def clean_number(num_str: str) -> str:
        if "." in num_str:
            num_str = num_str.rstrip("0").rstrip(".")
        return num_str

    # Currency formatting (3 significant figures)
    if is_currency:
        abs_val = abs(value)

        if is_in_billions:
            # Value already in billions
            if abs_val >= 1000:  # Trillions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"
                else:
                    formatted = f"${scaled:.2f}T"
            elif abs_val >= 1:  # Billions
                if abs_val >= 100:
                    formatted = f"${value:.0f}B"
                elif abs_val >= 10:
                    formatted = f"${value:.1f}B"
                else:
                    formatted = f"${value:.2f}B"
            elif abs_val >= 0.001:  # Millions
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"
                else:
                    formatted = f"${scaled:.2f}M"
            else:
                formatted = f"${value*1000000:.0f}K"
        elif is_in_millions:
            # Value already in millions
            if abs_val >= 1000:  # Billions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"
                else:
                    formatted = f"${scaled:.2f}B"
            elif abs_val >= 1:  # Millions
                if abs_val >= 100:
                    formatted = f"${value:.0f}M"
                elif abs_val >= 10:
                    formatted = f"${value:.1f}M"
                else:
                    formatted = f"${value:.2f}M"
            elif abs_val >= 0.001:  # Thousands
                scaled = value * 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"
                else:
                    formatted = f"${scaled:.2f}K"
            else:
                formatted = f"${value*1000:.0f}"
        elif is_in_thousands:
            # Value already in thousands
            if abs_val >= 1000000:  # Billions
                scaled = value / 1000000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"
                else:
                    formatted = f"${scaled:.2f}B"
            elif abs_val >= 1000:  # Millions
                scaled = value / 1000
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"
                else:
                    formatted = f"${scaled:.2f}M"
            elif abs_val >= 1:  # Thousands
                if abs_val >= 100:
                    formatted = f"${value:.0f}K"
                elif abs_val >= 10:
                    formatted = f"${value:.1f}K"
                else:
                    formatted = f"${value:.2f}K"
            else:
                formatted = f"${value*1000:.0f}"
        else:
            # Value in raw dollars - auto-scale
            if abs_val >= 1e12:  # Trillions
                scaled = value / 1e12
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}T"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}T"
                else:
                    formatted = f"${scaled:.2f}T"
            elif abs_val >= 1e9:  # Billions
                scaled = value / 1e9
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}B"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}B"
                else:
                    formatted = f"${scaled:.2f}B"
            elif abs_val >= 1e6:  # Millions
                scaled = value / 1e6
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}M"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}M"
                else:
                    formatted = f"${scaled:.2f}M"
            elif abs_val >= 1e3:  # Thousands
                scaled = value / 1e3
                if abs(scaled) >= 100:
                    formatted = f"${scaled:.0f}K"
                elif abs(scaled) >= 10:
                    formatted = f"${scaled:.1f}K"
                else:
                    formatted = f"${scaled:.2f}K"
            else:
                formatted = f"${value:.0f}"

        # Clean trailing .0
        return formatted.replace(".0B", "B").replace(".0M", "M").replace(".0T", "T").replace(".0K", "K")

    # Non-currency numbers - auto-scale large numbers
    abs_val = abs(value)

    if abs_val >= 1e9:  # Billions
        scaled = value / 1e9
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}B"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}B"
        else:
            formatted_num = f"{scaled:.2f}B"
    elif abs_val >= 1e6:  # Millions
        scaled = value / 1e6
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}M"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}M"
        else:
            formatted_num = f"{scaled:.2f}M"
    elif abs_val >= 100_000:  # 100K+
        scaled = value / 1e3
        if abs(scaled) >= 100:
            formatted_num = f"{scaled:.0f}K"
        elif abs(scaled) >= 10:
            formatted_num = f"{scaled:.1f}K"
        else:
            formatted_num = f"{scaled:.2f}K"
    elif value == int(value):
        formatted_num = f"{int(value):,}"
    elif abs_val >= 1000:
        formatted_num = f"{value:,.0f}"
    elif abs_val >= 1:
        if value >= 100:
            formatted_num = f"{value:,.0f}"
        elif value >= 10:
            formatted_num = clean_number(f"{value:,.1f}")
        else:
            formatted_num = clean_number(f"{value:,.2f}")
    else:
        formatted_num = clean_number(f"{value:.3g}")

    # Clean trailing zeros
    formatted_num = formatted_num.replace(".0B", "B").replace(".0M", "M").replace(".0K", "K")

    # Percentage formatting
    if is_percentage:
        pct_value = value * 100
        if abs(pct_value) >= 100:
            pct_formatted = f"{pct_value:.0f}"
        elif abs(pct_value) >= 10:
            pct_formatted = clean_number(f"{pct_value:.1f}")
        elif abs(pct_value) >= 1:
            pct_formatted = clean_number(f"{pct_value:.2f}")
        else:
            pct_formatted = clean_number(f"{pct_value:.3g}")
        return f"{pct_formatted}%"

    return formatted_num


def format_roi(value: float) -> str:
    """Format ROI as ratio

    Args:
        value: ROI number

    Returns:
        Formatted string like "463:1"
    """
    return f"{value:,.0f}:1"


def format_percentage(value: float) -> str:
    """Format as percentage

    Args:
        value: Decimal value (e.g., 0.01 for 1%)

    Returns:
        Formatted string like "1.0%"
    """
    return f"{value*100:,.1f}%"


def format_qalys(value: float) -> str:
    """Format QALY count with commas

    Args:
        value: Number of QALYs

    Returns:
        Formatted string like "840,000"
    """
    return f"{value:,.0f}"


# --- Module Initialization ---

if __name__ == "__main__":
    # Print some key parameters when module is executed directly
    print(f"Military spending: {format_parameter_value(GLOBAL_MILITARY_SPENDING_ANNUAL_2024)}")
    print(f"Total war costs: {format_parameter_value(GLOBAL_ANNUAL_WAR_TOTAL_COST)}")
    print(f"Peace dividend: {format_parameter_value(PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT)}")
    print(f"dFDA savings: {format_parameter_value(DFDA_RD_GROSS_SAVINGS_ANNUAL)}")
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
)
GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL = Parameter(
    GLOBAL_MED_RESEARCH_SPENDING / GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH,
    source_ref="/knowledge/problem/cost-of-war.qmd#grotesque-mathematics",
    source_type="calculated",
    description="Cost per life saved by medical research",
    display_name="Cost per Life Saved by Medical Research",
    unit="USD/life",
    formula="(RESEARCH_SPENDING × 1B) ÷ LIVES_SAVED",
    latex=r"CostPerLifeSaved = \frac{\$67.5B \times 10^9}{4,200,000} \approx \$16,071",
    keywords=["worldwide", "yearly", "investigation", "r&d", "science", "study", "conflict"],
    inputs=['GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH', 'GLOBAL_MED_RESEARCH_SPENDING'],
    compute=lambda ctx: ctx["GLOBAL_MED_RESEARCH_SPENDING"] / ctx["GLOBAL_ANNUAL_LIVES_SAVED_BY_MED_RESEARCH"],
)  # ~$16,071
MISALLOCATION_FACTOR_DEATH_VS_SAVING = Parameter(
    (GLOBAL_ANNUAL_WAR_TOTAL_COST / GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL)
    / GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL,
    source_ref="/knowledge/problem/cost-of-war.qmd#grotesque-mathematics",
    source_type="calculated",
    description="Misallocation factor: cost to kill vs cost to save",
    display_name="Misallocation Factor: Cost to Kill vs Cost to Save",
    unit="ratio",
    formula="COST_PER_DEATH ÷ COST_PER_LIFE_SAVED",
    latex=r"Misallocation = \frac{\$46.4M}{\$16,071} \approx 2,889x",
    keywords=["multiple", "fatalities", "casualties", "deaths", "investigation", "r&d", "science"],
    inputs=['GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL', 'GLOBAL_ANNUAL_WAR_TOTAL_COST', 'GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL'],
    compute=lambda ctx: (ctx["GLOBAL_ANNUAL_WAR_TOTAL_COST"] / ctx["GLOBAL_ANNUAL_CONFLICT_DEATHS_TOTAL"])
    / ctx["GLOBAL_COST_PER_LIFE_SAVED_MED_RESEARCH_ANNUAL"],
)  # ~2,889x

# Opportunity Cost Parameters
ECONOMIC_MULTIPLIER_MILITARY_SPENDING = Parameter(
    0.6,
    source_ref=ReferenceID.MILITARY_SPENDING_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for military spending (0.6x ROI)",
    display_name="Economic Multiplier for Military Spending",
    unit="ratio",
    keywords=["60%", "dod", "pentagon", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect"]
)

ECONOMIC_MULTIPLIER_INFRASTRUCTURE_INVESTMENT = Parameter(
    1.6,
    source_ref=ReferenceID.INFRASTRUCTURE_INVESTMENT_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for infrastructure investment (1.6x ROI)",
    display_name="Economic Multiplier for Infrastructure Investment",
    unit="ratio",
    keywords=["economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple", "capital"]
)

ECONOMIC_MULTIPLIER_EDUCATION_INVESTMENT = Parameter(
    2.1,
    source_ref=ReferenceID.EDUCATION_INVESTMENT_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for education investment (2.1x ROI)",
    display_name="Economic Multiplier for Education Investment",
    unit="ratio",
    keywords=["economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple", "capital"]
)

ECONOMIC_MULTIPLIER_HEALTHCARE_INVESTMENT = Parameter(
    4.3,
    source_ref=ReferenceID.HEALTHCARE_INVESTMENT_ECONOMIC_MULTIPLIER,
    source_type="external",
    description="Economic multiplier for healthcare investment (4.3x ROI)",
    display_name="Economic Multiplier for Healthcare Investment",
    unit="ratio",
    keywords=["economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple", "capital"]
)

TREATY_CAMPAIGN_BUDGET_SUPER_PACS = Parameter(
    800_000_000,
    source_ref="/knowledge/strategy/roadmap.qmd#campaign-budget",
    source_type="definition",
    description="Campaign budget for Super PACs and political lobbying",
    display_name="Campaign Budget for Super Pacs and Political Lobbying",
    unit="USD",
    keywords=["800.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"]
)  # billions USD, for Super PACs/politician bribery

GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT = Parameter(
    0.035,
    source_ref=ReferenceID.N3_5_RULE,
    source_type="external",
    description="Critical mass threshold for social change (3.5% rule)",
    display_name="Critical Mass Threshold for Social Change",
    unit="rate",
    confidence_interval=(0.025, 0.045),  # Range 2.5-4.5% based on different studies
    distribution="lognormal",
    keywords=["4%", "people", "worldwide", "citizens", "individuals", "inhabitants", "persons"]
)  # 3.5% rule for social change, key tipping point

TREATY_CAMPAIGN_VOTING_BLOC_TARGET = Parameter(
    GLOBAL_POPULATION_2024 * GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT,
    source_ref="/knowledge/strategy/roadmap.qmd#voting-bloc",
    source_type="calculated",
    description="Target voting bloc size for campaign (3.5% of global population - critical mass for social change)",
    display_name="Target Voting Bloc Size for Campaign",
    unit="of people",
    formula="GLOBAL_POPULATION × 3.5%",
    keywords=["280.0m", "1%", "one percent", "international agreement", "peace treaty", "agreement", "pact"],
    inputs=['GLOBAL_POPULATION_2024', 'GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT'],
    compute=lambda ctx: ctx["GLOBAL_POPULATION_2024"] * ctx["GLOBAL_POPULATION_ACTIVISM_THRESHOLD_PCT"],
)  # 280M people = 3.5% of 8B (critical mass threshold)

# Clinical Trial Cost Examples & Comparisons
TRADITIONAL_PHASE3_COST_PER_PATIENT_EXAMPLE_48K = Parameter(
    48000,
    source_ref=ReferenceID.CLINICAL_TRIAL_COST_PER_PATIENT,
    source_type="external",
    description="Example Phase 3 trial cost per patient ($48K)",
    display_name="Example Phase 3 Trial Cost per Patient",
    unit="USD/patient",
    keywords=["48k", "confirmatory trial", "third phase", "rct", "participant", "subject", "volunteer"]
)  # USD per trial patient, specific example from text for comparison

TRADITIONAL_PHASE3_COST_PER_PATIENT_FDA_EXAMPLE_41K = Parameter(
    41000,
    source_ref=ReferenceID.TRIAL_COSTS_FDA_STUDY,
    source_type="external",
    description="FDA cited Phase 3 cost per patient ($41K)",
    display_name="FDA Cited Phase 3 Cost per Patient",
    unit="USD/patient",
    keywords=["41k", "confirmatory trial", "third phase", "rct", "participant", "subject", "volunteer"]
)  # USD per patient, cited FDA cost example for comparison

# Historical & Comparison Multipliers
MILITARY_VS_MEDICAL_RESEARCH_RATIO = Parameter(
    GLOBAL_MILITARY_SPENDING_ANNUAL_2024 / GLOBAL_MED_RESEARCH_SPENDING,
    source_ref="/knowledge/problem/cost-of-war.qmd#misallocation",
    source_type="calculated",
    description="Ratio of military spending to medical research spending",
    display_name="Ratio of Military Spending to Medical Research Spending",
    unit="ratio",
    formula="MILITARY_SPENDING ÷ MEDICAL_RESEARCH",
    latex=r"Ratio = \frac{\$2,718B}{\$67.5B} \approx 40.3:1",
    keywords=["dod", "pentagon", "national security", "army", "navy", "armed forces", "conflict"],
    inputs=['GLOBAL_MED_RESEARCH_SPENDING', 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024'],
    compute=lambda ctx: ctx["GLOBAL_MILITARY_SPENDING_ANNUAL_2024"] / ctx["GLOBAL_MED_RESEARCH_SPENDING"],
)  # Calculated ratio of military to medical research spending

POST_WW2_MILITARY_CUT_PCT = Parameter(
    0.30,
    source_ref=ReferenceID.US_POST_WWII_MILITARY_SPENDING_CUT,
    source_type="external",
    description="Percentage military spending cut after WW2 (historical precedent)",
    display_name="Percentage Military Spending Cut After WW2",
    unit="rate",
    keywords=["30%", "dod", "pentagon", "national security", "army", "navy", "armed forces"]
)  # Percentage military spending cut after WW2, historical precedent

SWITZERLAND_DEFENSE_SPENDING_PCT = Parameter(
    0.007,
    source_ref=ReferenceID.SWISS_MILITARY_BUDGET_0_7_PCT_GDP,
    source_type="external",
    description="Switzerland's defense spending as percentage of GDP (0.7%)",
    display_name="Switzerland's Defense Spending as Percentage of GDP",
    unit="rate",
    keywords=["1%", "armed forces", "international agreement", "peace treaty", "conflict", "costs", "funding"]
)  # Switzerland's defense spending as percentage of GDP

SWITZERLAND_GDP_PER_CAPITA_K = Parameter(
    93_000,
    source_ref=ReferenceID.SWISS_VS_US_GDP_PER_CAPITA,
    source_type="external",
    description="Switzerland GDP per capita",
    display_name="Switzerland GDP per Capita",
    unit="USD",
    keywords=["93k", "average person", "individual", "per person", "household benefit", "per individual", "typical individual"]
)  # Thousands USD, Switzerland GDP per capita, for comparison

AVERAGE_MARKET_RETURN_PCT = Parameter(
    0.10,
    source_ref=ReferenceID.WARREN_BUFFETT_CAREER_AVERAGE_RETURN_20_PCT,
    source_type="external",
    description="Average annual stock market return (10%)",
    display_name="Average Annual Stock Market Return",
    unit="rate",
    keywords=["10%", "benefit", "profit", "yield", "yearly", "average", "market"]
)  # Average market return percentage for portfolio comparisons

# Lobbyist compensation & incentives
LOBBYIST_BOND_INVESTMENT_MAX = Parameter(
    20_000_000,
    source_ref="/knowledge/strategy/roadmap.qmd#lobbyist-incentives",
    source_type="definition",
    description="Maximum bond investment for lobbyist incentives",
    display_name="Maximum Bond Investment for Lobbyist Incentives",
    unit="USD",
    keywords=["20.0m", "social impact bond", "sib", "impact investing", "pay for success", "capital", "finance"]
)  # Millions USD, bond investment for lobbyists (max incentive)

LOBBYIST_SALARY_MIN_K = Parameter(
    500_000,
    source_ref=ReferenceID.LOBBYIST_STATISTICS_DC,
    source_type="external",
    description="Minimum annual lobbyist salary range",
    display_name="Minimum Annual Lobbyist Salary Range",
    unit="USD",
    keywords=["500k", "yearly", "lobbyist", "min", "pa", "per annum", "per year"]
)  # $500K minimum for lobbyist salaries

LOBBYIST_SALARY_MAX = Parameter(
    2_000_000,
    source_ref=ReferenceID.LOBBYIST_STATISTICS_DC,
    source_type="external",
    description="Maximum annual lobbyist salary range",
    display_name="Maximum Annual Lobbyist Salary Range",
    unit="USD",
    keywords=["2.0m", "yearly", "lobbyist", "max", "pa", "per annum", "per year"]
)  # $2M maximum for top lobbyist salaries

# Specific benefit sum (used for the $147.1B figure in the "Where Math Breaks" section)
# This sum is distinct from TREATY_PEACE_PLUS_RD_ANNUAL_BENEFITS which uses different categories for broader calculation.
COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC = Parameter(
    PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT + DFDA_RD_GROSS_SAVINGS_ANNUAL,
    source_ref="/knowledge/appendix/peace-dividend-calculations.qmd#peace-dividend-composition",
    source_type="calculated",
    description="Combined peace and health dividends for ROI calculation",
    display_name="Combined Peace and Health Dividends for ROI Calculation",
    unit="USD/year",
    formula="PEACE_DIVIDEND + R&D_SAVINGS",
    keywords=["pragmatic trials", "real world evidence", "bcr", "benefit cost ratio", "economic return", "investment return", "return on investment"],
    inputs=["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT", "DFDA_RD_GROSS_SAVINGS_ANNUAL"],
    compute=lambda ctx: ctx["PEACE_DIVIDEND_ANNUAL_SOCIETAL_BENEFIT"] + ctx["DFDA_RD_GROSS_SAVINGS_ANNUAL"],
)

TREATY_BENEFIT_MULTIPLIER_VS_VACCINES = Parameter(
    COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC / CHILDHOOD_VACCINATION_ANNUAL_BENEFIT,
    source_ref="/knowledge/economics/economics.qmd#better-than-the-best-charities",
    source_type="calculated",
    description="Treaty system benefit multiplier vs childhood vaccination programs",
    display_name="Treaty System Benefit Multiplier vs Childhood Vaccination Programs",
    unit="ratio",
    formula="TREATY_CONSERVATIVE_BENEFIT ÷ CHILDHOOD_VACCINATION_BENEFIT",
    keywords=["1%", "economic impact", "fiscal multiplier", "gdp multiplier", "multiplier effect", "bcr", "multiple"],
    inputs=['CHILDHOOD_VACCINATION_ANNUAL_BENEFIT', 'COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC'],
    compute=lambda ctx: ctx["COMBINED_PEACE_HEALTH_DIVIDENDS_ANNUAL_FOR_ROI_CALC"] / ctx["CHILDHOOD_VACCINATION_ANNUAL_BENEFIT"],
)  # ~11:1 ratio (treaty system is 11x larger in economic impact)


# ---
# BOOK READING TIME & HOURLY RATE CALCULATIONS
# ---

# Book reading time parameters
# Source: word_count.ps1 output
TOTAL_BOOK_WORDS = Parameter(
    171121, source_ref="book-word-count", source_type="definition", description="Total words in the book", unit="words",
    display_name="Total Words in the Book",
    keywords=["total", "book", "words", "171k"]
)  # Total words in the book

BOOK_READING_SPEED_WPM = Parameter(
    200,
    source_ref="average-reading-speed",
    source_type="external",
    description="Average reading speed (conservative for non-fiction)",
    display_name="Average Reading Speed",
    unit="words/minute",
    keywords=["low estimate", "faster development", "innovation speed", "research velocity", "cautious", "pessimistic", "worst case"]
)  # Words per minute (conservative for non-fiction)

# Effective hourly rate calculation (20-year scenario, age 30, $50K income, 1% treaty)
# Using the lifetime benefit value from your-personal-benefits.qmd
EFFECTIVE_HOURLY_RATE_LIFETIME_BENEFIT = Parameter(
    4_300_000,
    source_ref="/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations.qmd",
    source_type="definition",
    description="Lifetime benefit for age 30 baseline scenario ($4.3M)",
    display_name="Lifetime Benefit for Age 30 Baseline Scenario",
    unit="USD",
    formula="Total lifetime health gains from 1% treaty",
    latex=r"Benefit = \$4,300,000",
    keywords=["4.3m", "financial benefit", "individual benefit", "monetary gain", "per capita benefit", "personal benefit", "30 year old"]
)

# Comparison benchmarks
AVERAGE_US_HOURLY_WAGE = Parameter(
    30,
    source_ref="average-us-hourly-wage",
    source_type="external",
    description="Average US hourly wage",
    display_name="Average US Hourly Wage",
    unit="USD/hour",
    keywords=["average", "hourly", "wage"]
)  # ~$30/hour average US wage

TYPICAL_CEO_HOURLY_RATE = Parameter(
    10000, source_ref="ceo-compensation", source_type="external", description="Typical CEO hourly rate", unit="USD/hour",
    display_name="Typical CEO Hourly Rate",
    keywords=["typical", "ceo", "hourly", "rate", "10k"]
)  # ~$10,000/hour typical CEO rate

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

    Uses linear scaling from the base TRIAL_CAPACITY_MULTIPLIER (25.7x at 1% treaty).

    Formula:
        Multiplier = TRIAL_CAPACITY_MULTIPLIER × (treaty_pct / 0.01)

    Examples:
    - 1% treaty: 25.7 × (0.01 / 0.01) = 25.7x
    - 2% treaty: 25.7 × (0.02 / 0.01) = 51.4x
    - 5% treaty: 25.7 × (0.05 / 0.01) = 128.5x
    - 10% treaty: 25.7 × (0.10 / 0.01) = 257x

    Args:
        treaty_pct: Fraction of military spending redirected (e.g., 0.01 for 1%)

    Returns:
        Trial capacity multiplier (e.g., 25.7 = 25.7x more trial slots available)
    """
    return float(TRIAL_CAPACITY_MULTIPLIER) * (treaty_pct / 0.01)


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
)  # $4.1T/year CDC estimate

US_POPULATION_2024 = Parameter(
    335e6, source_ref=ReferenceID.US_VOTER_POPULATION, source_type="external", description="US population in 2024", unit="people",
    display_name="US Population in 2024",
    keywords=["2024", "335.0m", "people", "citizens", "individuals", "inhabitants", "persons"],
    distribution="lognormal",
    confidence_interval=(330e6, 340e6),  # ±1.5% - census estimates well-known
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
)  # ~$1,045/year

MENTAL_HEALTH_PRODUCTIVITY_LOSS_PER_CAPITA = Parameter(
    2000,
    source_ref=ReferenceID.MENTAL_HEALTH_BURDEN,
    source_type="external",
    description="Annual productivity loss per capita from mental health issues (beyond treatment costs)",
    display_name="Annual Productivity Loss per Capita from Mental Health Issues",
    unit="USD/year",
    keywords=["2k", "average person", "individual", "per person", "yearly", "household benefit", "per individual"]
)  # Additional productivity loss beyond treatment

# Caregiver time constants (simple model - deprecated, use detailed model below)
CAREGIVER_HOURS_PER_MONTH = Parameter(
    20,
    source_ref=ReferenceID.UNPAID_CAREGIVER_HOURS_ECONOMIC_VALUE,
    source_type="external",
    description="Average monthly hours of unpaid family caregiving in US",
    display_name="Average Monthly Hours of Unpaid Family Caregiving in US",
    unit="hours/month",
    keywords=["caregiver", "hours", "month"]
)  # Average US family provides 20 hrs/month unpaid care

CAREGIVER_VALUE_PER_HOUR_SIMPLE = Parameter(
    25,
    source_ref=ReferenceID.UNPAID_CAREGIVER_HOURS_ECONOMIC_VALUE,
    source_type="external",
    description="Estimated replacement cost per hour of caregiving",
    display_name="Estimated Replacement Cost per Hour of Caregiving",
    unit="USD/hour",
    keywords=["caregiver", "hour", "simple", "expenditure", "spending", "value", "budget"]
)  # Replacement cost estimate
CAREGIVER_COST_ANNUAL = Parameter(
    CAREGIVER_HOURS_PER_MONTH * MONTHS_PER_YEAR * CAREGIVER_VALUE_PER_HOUR_SIMPLE,
    source_type="definition",
    description="Annual cost of unpaid caregiving (replacement cost method)",
    display_name="Annual Cost of Unpaid Caregiving",
    unit="USD/year",
    formula="HOURS_PER_MONTH × MONTHS_PER_YEAR × VALUE_PER_HOUR",
    keywords=["caregiver", "unpaid", "annual", "expenditure", "spending", "value", "budget"],
)  # $6,000/year


WORKFORCE_WITH_PRODUCTIVITY_LOSS = Parameter(
    0.28,
    source_ref="chronic-illness-workforce-productivity-loss",
    source_type="external",
    description="Percentage of workforce experiencing productivity loss from chronic illness (28%)",
    display_name="Percentage of Workforce Experiencing Productivity Loss from Chronic Illness",
    unit="rate",
    keywords=["workforce", "with", "productivity", "loss", "28%"]
)  # 28% of all employees have productivity loss

CAREGIVER_ANNUAL_VALUE_TOTAL = Parameter(
    600e9,
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="Total annual value of unpaid caregiving in US",
    display_name="Total Annual Value of Unpaid Caregiving in US",
    unit="USD/year",
    keywords=["600.0b", "yearly", "caregiver", "per year", "per annum", "pa", "annual"]
)  # $600B total

CAREGIVER_COUNT_US = Parameter(
    38e6,
    source_ref="unpaid-caregiver-hours-economic-value",
    source_type="external",
    description="Number of unpaid caregivers in US",
    display_name="Number of Unpaid Caregivers in US",
    unit="people",
    keywords=["caregiver", "count", "38.0m"]
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
    keywords=["40%", "illness", "disease", "related", "caregiver", "pct", "ailment"]
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


# Personal lifetime wealth with uncertainty-driven life extension
# Uses LIFE_EXTENSION_YEARS parameter which has 80% CI of 5-50 years
# NOTE: Uses fixed 3% personal discount rate (not NPV_DISCOUNT_RATE_STANDARD)
# because personal time preference is typically 2-4%, and varying discount rate
# would swamp all other factors in sensitivity analysis
PERSONAL_LIFETIME_WEALTH = Parameter(
    calculate_personal_lifetime_wealth_conservative_baseline(
        treaty_pct=0.01, current_age=30, annual_income=50000,
        life_extension_override=float(LIFE_EXTENSION_YEARS)
    )["total_lifetime_benefit"],
    source_ref="/knowledge/appendix/disease-eradication-personal-lifetime-wealth-calculations.qmd",
    source_type="calculated",
    description="Personal lifetime wealth benefit for a 30-year-old with $50K income under 1% treaty. Life extension uncertainty (5-50 years) propagates through Monte Carlo to show full range of outcomes from conservative antibiotic precedent to optimistic aging reversal scenarios.",
    display_name="Personal Lifetime Wealth (Age 30, 1% Treaty)",
    unit="usd",
    formula="NPV(peace_dividend + healthcare_savings + productivity_gains + caregiver_savings + gdp_boost + extended_earnings)",
    latex=r"\text{PLW} = \sum_{t=0}^{T + \Delta L} \frac{B_t}{(1+r)^t}",
    confidence="medium",
    keywords=["personal", "lifetime", "wealth", "individual benefit", "age 30", "npv", "life extension"],
    inputs=[
        "LIFE_EXTENSION_YEARS",  # Primary driver: 66% of benefit from extended earnings
        "TRIAL_CAPACITY_MULTIPLIER",  # Drives healthcare, productivity, GDP boost (~30%)
    ],
    compute=lambda ctx: calculate_personal_lifetime_wealth_conservative_baseline(
        treaty_pct=0.01,
        current_age=30,
        annual_income=50000,
        discount_rate=0.03,  # Fixed 3% personal discount rate
        life_extension_override=float(ctx["LIFE_EXTENSION_YEARS"]),
    )["total_lifetime_benefit"],
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
# Parameters showing how different stakeholders benefit from the DIH/dFDA system
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
    keywords=["pharma", "drug", "development", "cost", "r&d", "current"]
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
    distribution="fixed",  # Historical documented value; uncertainty is in the methodology, not measurement
)

DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER = Parameter(
    PHARMA_DRUG_DEVELOPMENT_COST_CURRENT / DRUG_DEVELOPMENT_COST_1980S,
    source_ref=ReferenceID.PRE_1962_DRUG_COSTS_TIMELINE,
    source_type="calculated",
    description="Drug development cost increase from 1980s to current ($194M → $2.6B = 13.4x)",
    display_name="Drug Cost Increase: 1980s to Current",
    unit="ratio",
    formula="PHARMA_DRUG_DEVELOPMENT_COST_CURRENT ÷ DRUG_DEVELOPMENT_COST_1980S",
    confidence="high",
    keywords=["cost", "increase", "multiplier", "drug", "development", "1980s", "current"],
    inputs=['DRUG_DEVELOPMENT_COST_1980S', 'PHARMA_DRUG_DEVELOPMENT_COST_CURRENT'],
    compute=lambda ctx: ctx["PHARMA_DRUG_DEVELOPMENT_COST_CURRENT"] / ctx["DRUG_DEVELOPMENT_COST_1980S"],
)

DRUG_COST_INCREASE_PRE1962_TO_CURRENT_MULTIPLIER = Parameter(
    PHARMA_DRUG_DEVELOPMENT_COST_CURRENT / PRE_1962_DRUG_DEVELOPMENT_COST,
    source_ref=ReferenceID.PRE_1962_DRUG_COSTS_TIMELINE,
    source_type="calculated",
    description="Drug development cost increase from pre-1962 to current ($50M → $2.6B = 52x)",
    display_name="Drug Cost Increase: Pre-1962 to Current",
    unit="ratio",
    formula="PHARMA_DRUG_DEVELOPMENT_COST_CURRENT ÷ PRE_1962_DRUG_DEVELOPMENT_COST",
    confidence="medium",
    keywords=["cost", "increase", "multiplier", "drug", "development", "1962", "regulation", "fda", "pre-1962", "current"],
    inputs=['PHARMA_DRUG_DEVELOPMENT_COST_CURRENT', 'PRE_1962_DRUG_DEVELOPMENT_COST'],
    compute=lambda ctx: ctx["PHARMA_DRUG_DEVELOPMENT_COST_CURRENT"] / ctx["PRE_1962_DRUG_DEVELOPMENT_COST"],
)  # Calculated from documented range ($10-50M pre-1962)

PHARMA_SUCCESS_RATE_CURRENT_PCT = Parameter(
    0.10,
    source_ref=ReferenceID.DRUG_TRIAL_SUCCESS_RATE_12_PCT,
    source_type="external",
    description="Percentage of drugs that reach market in current system",
    display_name="Pharma Drug Success Rate (Current System)",
    unit="percentage",
    confidence="high",
    peer_reviewed=True,
    keywords=["pharma", "drug", "success", "rate", "approval", "current"]
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
    keywords=["pharma", "drug", "revenue", "lifetime", "current"]
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
    keywords=["pharma", "roi", "current", "system", "barely profitable", "low returns"]
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
    keywords=["insurance", "diabetes", "cost", "annual", "us", "disease", "burden"]
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
    keywords=["insurance", "alzheimer", "dementia", "cost", "annual", "us", "disease", "burden"]
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
    keywords=["insurance", "heart", "cardiovascular", "stroke", "cost", "annual", "us", "disease", "burden"]
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
    keywords=["insurance", "cancer", "oncology", "cost", "annual", "us", "disease", "burden"]
)

US_MAJOR_DISEASES_TOTAL_ANNUAL_COST = Parameter(
    US_DIABETES_ANNUAL_COST + US_ALZHEIMERS_ANNUAL_COST + US_HEART_DISEASE_ANNUAL_COST + US_CANCER_ANNUAL_COST,
    source_ref="/knowledge/solution/aligning-incentives.qmd#insurance-companies",
    source_type="calculated",
    description="Total annual US cost of major diseases (diabetes, Alzheimer's, heart disease, cancer)",
    display_name="US Major Diseases Total Annual Cost",
    unit="USD",
    formula="DIABETES + ALZHEIMERS + HEART + CANCER",
    confidence="high",
    keywords=["insurance", "disease", "cost", "annual", "us", "total", "burden"],
    inputs=['US_ALZHEIMERS_ANNUAL_COST', 'US_CANCER_ANNUAL_COST', 'US_DIABETES_ANNUAL_COST', 'US_HEART_DISEASE_ANNUAL_COST'],
    compute=lambda ctx: ctx["US_DIABETES_ANNUAL_COST"] + ctx["US_ALZHEIMERS_ANNUAL_COST"] + ctx["US_HEART_DISEASE_ANNUAL_COST"] + ctx["US_CANCER_ANNUAL_COST"],
)
