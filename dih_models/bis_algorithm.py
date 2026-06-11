"""
Budget Impact Score (BIS) Algorithm

Implementation of the meta-analytic budget allocation algorithm specified in
optimocracy-paper.qmd. Computes optimal budget allocations from econometric
literature estimates using quality-weighted meta-analysis.

Usage:
    from dih_models.bis_algorithm import calculate_allocations
    from dih_models.bis_literature_data import EFFECT_ESTIMATES

    results = calculate_allocations(EFFECT_ESTIMATES, total_budget=1_000_000_000_000)
    print(results.to_markdown())
"""

from dataclasses import dataclass
from datetime import datetime
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dih_models.bis_literature_data import EffectEstimate

# Import quality weights from data module
from dih_models.bis_literature_data import QUALITY_WEIGHTS, CATEGORIES


# =============================================================================
# ALGORITHM PARAMETERS
# =============================================================================

# Recency decay parameter (lambda in the paper)
# Half-life = ln(2) / lambda ≈ 23 years at lambda = 0.03
RECENCY_DECAY_RATE = 0.03

# Calibration constant for confidence score
# Higher K = requires more evidence for full confidence
CONFIDENCE_CALIBRATION_K = 100

# Minimum confidence threshold for allocation
# Categories below this get $0 from main budget (but may get exploration funds)
MIN_CONFIDENCE_THRESHOLD = 0.30

# Exploration reserve fraction
# This fraction of budget funds RCTs on uncertain interventions
EXPLORATION_RESERVE_FRACTION = 0.10

# Current year for recency calculations
CURRENT_YEAR = datetime.now().year


# =============================================================================
# CATEGORY FLOOR PRESETS
# =============================================================================
# Minimum allocations based on international norms or expert consensus

# NATO standard: 2% of GDP for defense (~$560B for US with $28T GDP)
# Using 3% as more realistic US floor given alliance commitments
FLOORS_NATO_STANDARD = {
    "military_discretionary": 200_000_000_000,  # $200B (scaled to $1T budget = 20%)
}

# OECD average allocation pattern (% of total government spending)
# Source: Government at a Glance 2025
FLOORS_OECD_AVERAGE = {
    "military_discretionary": 30_000_000_000,  # ~3% (OECD average defense)
}

# US historical minimum (post-Cold War low ~3% of GDP)
FLOORS_US_HISTORICAL = {
    "military_discretionary": 300_000_000_000,  # $300B (~3% of GDP scaled)
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CategoryScore:
    """Computed scores for a single spending category."""
    category: str
    description: str
    n_studies: int
    weighted_beta: float  # Meta-analytic effect estimate
    confidence: float  # Evidence quality/quantity score
    bis: float  # Budget Impact Score
    allocation: float  # Dollar allocation
    allocation_pct: float  # Percentage of budget
    is_exploration: bool  # True if funded via exploration reserve


@dataclass
class AllocationResult:
    """Complete allocation results."""
    total_budget: float
    main_budget: float
    exploration_budget: float
    categories: list[CategoryScore]

    def to_markdown(self) -> str:
        """Format results as markdown table."""
        lines = [
            f"**Total Budget:** ${self.total_budget / 1e9:.0f}B",
            f"**Main Allocation:** ${self.main_budget / 1e9:.0f}B",
            f"**Exploration Reserve:** ${self.exploration_budget / 1e9:.0f}B",
            "",
            "| Category | Studies | Effect | Confidence | BIS | Allocation |",
            "|----------|---------|--------|------------|-----|------------|",
        ]

        for cat in sorted(self.categories, key=lambda x: -x.allocation):
            # Show all categories, including those with $0 allocation
            if cat.allocation > 0:
                alloc_str = f"${cat.allocation / 1e9:.0f}B ({cat.allocation_pct:.1%})"
                if cat.is_exploration:
                    alloc_str += " *"
            else:
                alloc_str = "$0"

            # Use short category name
            short_name = cat.category.replace("_", " ").title()
            lines.append(
                f"| {short_name} | {cat.n_studies} | "
                f"{cat.weighted_beta:.2f} | {cat.confidence:.2f} | "
                f"{cat.bis:.2f} | {alloc_str} |"
            )

        lines.append("")
        lines.append("*\\* Exploration funding for high-uncertainty categories*")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "total_budget": self.total_budget,
            "main_budget": self.main_budget,
            "exploration_budget": self.exploration_budget,
            "categories": [
                {
                    "category": c.category,
                    "description": c.description,
                    "n_studies": c.n_studies,
                    "weighted_beta": c.weighted_beta,
                    "confidence": c.confidence,
                    "bis": c.bis,
                    "allocation": c.allocation,
                    "allocation_pct": c.allocation_pct,
                    "is_exploration": c.is_exploration,
                }
                for c in self.categories
            ],
        }


# =============================================================================
# CORE ALGORITHM
# =============================================================================

def compute_quality_weight(method: str) -> float:
    """Step 2: Quality weight based on identification strategy."""
    return QUALITY_WEIGHTS.get(method, 0.25)


def compute_precision_weight(se: float | None, n: int | None) -> float:
    """Step 3: Precision weight based on standard error or sample size."""
    if se is not None and se > 0:
        # Inverse variance weighting
        return 1.0 / (se ** 2)
    elif n is not None and n > 0:
        # Approximate with square root of sample size
        return math.sqrt(n)
    else:
        # Default weight if no precision info available
        return 1.0


def compute_recency_weight(year: int) -> float:
    """Step 4: Recency weight with exponential decay."""
    years_ago = CURRENT_YEAR - year
    return math.exp(-RECENCY_DECAY_RATE * years_ago)


def compute_weighted_beta(estimates: list["EffectEstimate"]) -> tuple[float, float]:
    """
    Step 5: Compute weighted effect estimate for a category.

    Returns:
        (weighted_beta, total_weight) tuple
    """
    if not estimates:
        return 0.0, 0.0

    numerator = 0.0
    denominator = 0.0

    for est in estimates:
        w_q = compute_quality_weight(est.method)
        w_p = compute_precision_weight(est.se, est.n)
        w_r = compute_recency_weight(est.year)

        total_weight = w_q * w_p * w_r
        numerator += total_weight * est.beta
        denominator += total_weight

    if denominator == 0:
        return 0.0, 0.0

    return numerator / denominator, denominator


def compute_confidence(estimates: list["EffectEstimate"]) -> float:
    """
    Step 6: Compute confidence score based on evidence quantity and quality.
    """
    if not estimates:
        return 0.0

    total_quality_precision = 0.0
    for est in estimates:
        w_q = compute_quality_weight(est.method)
        w_p = compute_precision_weight(est.se, est.n)
        total_quality_precision += w_q * w_p

    # Normalize by calibration constant, cap at 1.0
    return min(1.0, total_quality_precision / CONFIDENCE_CALIBRATION_K)


def compute_variance(estimates: list["EffectEstimate"], weighted_beta: float) -> float:
    """Compute variance of estimates for exploration allocation."""
    if len(estimates) < 2:
        return 1.0  # High variance assumed for sparse evidence

    squared_diffs = [(e.beta - weighted_beta) ** 2 for e in estimates]
    return sum(squared_diffs) / len(squared_diffs)


def calculate_allocations(
    estimates: list["EffectEstimate"],
    total_budget: float = 1_000_000_000_000,  # $1T default
    exploration_fraction: float = EXPLORATION_RESERVE_FRACTION,
    min_confidence: float = MIN_CONFIDENCE_THRESHOLD,
    category_floors: dict[str, float] | None = None,  # Min allocation per category
) -> AllocationResult:
    """
    Main BIS algorithm: compute budget allocations from literature estimates.

    Args:
        estimates: List of EffectEstimate objects from literature
        total_budget: Total budget to allocate in dollars
        exploration_fraction: Fraction reserved for uncertain interventions
        min_confidence: Minimum confidence for main budget allocation

    Returns:
        AllocationResult with category scores and allocations
    """
    # Group estimates by category
    categories_data: dict[str, list["EffectEstimate"]] = {}
    for est in estimates:
        if est.category not in categories_data:
            categories_data[est.category] = []
        categories_data[est.category].append(est)

    # Compute scores for each category
    category_scores: list[CategoryScore] = []

    for category, cat_estimates in categories_data.items():
        weighted_beta, total_weight = compute_weighted_beta(cat_estimates)
        confidence = compute_confidence(cat_estimates)

        # Step 7: BIS = max(beta, 0) * confidence
        bis = max(weighted_beta, 0) * confidence

        category_scores.append(CategoryScore(
            category=category,
            description=CATEGORIES.get(category, category),
            n_studies=len(cat_estimates),
            weighted_beta=weighted_beta,
            confidence=confidence,
            bis=bis,
            allocation=0.0,  # Will be computed below
            allocation_pct=0.0,
            is_exploration=False,
        ))

    # Split budget into main and exploration
    exploration_budget = total_budget * exploration_fraction
    main_budget = total_budget - exploration_budget

    # Apply category floors (e.g., minimum defense spending)
    floor_total = 0.0
    if category_floors:
        for cat in category_scores:
            if cat.category in category_floors:
                floor = category_floors[cat.category]
                cat.allocation = floor
                cat.allocation_pct = floor / total_budget
                floor_total += floor

    # Budget available after floors
    available_budget = main_budget - floor_total

    # Step 8: Allocate remaining budget in proportion to BIS
    # Only categories with confidence >= min_confidence and not already floored
    floored_cats = set(category_floors.keys()) if category_floors else set()
    eligible_categories = [
        c for c in category_scores
        if c.confidence >= min_confidence and c.category not in floored_cats
    ]
    total_bis = sum(c.bis for c in eligible_categories)

    if total_bis > 0 and available_budget > 0:
        for cat in eligible_categories:
            cat.allocation = (cat.bis / total_bis) * available_budget
            cat.allocation_pct = cat.allocation / total_budget

    # Step 9: Allocate exploration budget to low-confidence categories
    low_confidence_categories = [c for c in category_scores if c.confidence < min_confidence]

    if low_confidence_categories:
        # Weight by variance (higher variance = more exploration value)
        variances = {}
        for cat in low_confidence_categories:
            cat_estimates = categories_data[cat.category]
            variances[cat.category] = compute_variance(cat_estimates, cat.weighted_beta)

        total_variance = sum(variances.values())

        if total_variance > 0:
            for cat in low_confidence_categories:
                cat.allocation = (variances[cat.category] / total_variance) * exploration_budget
                cat.allocation_pct = cat.allocation / total_budget
                cat.is_exploration = True

    return AllocationResult(
        total_budget=total_budget,
        main_budget=main_budget,
        exploration_budget=exploration_budget,
        categories=category_scores,
    )


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def format_allocation_table(result: AllocationResult) -> str:
    """Format allocation results as a simple table for display."""
    return result.to_markdown()


def run_example():
    """Run the BIS algorithm with the curated literature data."""
    from dih_models.bis_literature_data import EFFECT_ESTIMATES

    result = calculate_allocations(EFFECT_ESTIMATES, total_budget=1_000_000_000_000)
    print(result.to_markdown())
    return result


# =============================================================================
# SENSITIVITY ANALYSIS AND ROBUSTNESS CHECKS
# =============================================================================

# Approximate US federal discretionary budget allocation (FY2024, $B)
# Source: Congressional Budget Office, OMB, Bureau of Justice Statistics
US_ACTUAL_ALLOCATION = {
    "military_discretionary": 886,  # Total DoD discretionary (~$886B FY2024)
    "k12_education": 80,
    "basic_research": 50,  # NIH + NSF + DOE science
    "infrastructure": 90,
    "preventive_health": 40,  # CDC + preventive programs
    "early_childhood": 12,  # Head Start + child care
    "vaccinations": 8,
    "maternal_health": 6,
    "nutrition": 120,  # SNAP, WIC, school meals
    "pragmatic_trials": 2,  # PCORI + CMS innovation
    "agricultural_subsidies": 30,
    "incarceration_nonviolent": 40,  # ~50% of $81B total corrections (non-violent share)
    "drug_enforcement": 35,  # DEA + state/local drug enforcement
}


def compare_to_actual(result: AllocationResult) -> str:
    """
    Compare BIS allocations to actual US federal discretionary spending.
    Returns markdown table showing the delta.
    """
    lines = [
        "| Category | Actual ($B) | BIS ($B) | Delta ($B) | Change |",
        "|----------|-------------|----------|------------|--------|",
    ]

    total_actual = sum(US_ACTUAL_ALLOCATION.values())
    total_bis = result.total_budget / 1e9

    for cat in sorted(result.categories, key=lambda x: -x.allocation):
        actual = US_ACTUAL_ALLOCATION.get(cat.category, 0)
        bis = cat.allocation / 1e9
        delta = bis - actual

        if actual > 0:
            pct_change = (delta / actual) * 100
            change_str = f"{pct_change:+.0f}%"
        else:
            change_str = "New"

        sign = "+" if delta >= 0 else ""
        lines.append(
            f"| {cat.category.replace('_', ' ').title()} | "
            f"${actual:.0f}B | ${bis:.0f}B | {sign}${delta:.0f}B | {change_str} |"
        )

    lines.append("")
    lines.append(f"BIS reallocates ${sum(US_ACTUAL_ALLOCATION.values()) - total_actual:.0f}B "
                 f"from low-return to high-return categories.")

    return "\n".join(lines)


def sensitivity_analysis(
    estimates: list["EffectEstimate"],
    total_budget: float = 1_000_000_000_000,
) -> str:
    """
    Run sensitivity analysis varying key parameters.
    Returns markdown table showing how allocations change.
    """
    from dih_models.bis_literature_data import EFFECT_ESTIMATES

    scenarios = [
        ("Baseline", {"exploration_fraction": 0.10, "min_confidence": 0.30}),
        ("No exploration reserve", {"exploration_fraction": 0.00, "min_confidence": 0.30}),
        ("20% exploration reserve", {"exploration_fraction": 0.20, "min_confidence": 0.30}),
        ("Higher confidence threshold", {"exploration_fraction": 0.10, "min_confidence": 0.50}),
        ("Lower confidence threshold", {"exploration_fraction": 0.10, "min_confidence": 0.20}),
    ]

    # Get categories from baseline
    baseline = calculate_allocations(estimates, total_budget)
    categories = [c.category for c in sorted(baseline.categories, key=lambda x: -x.allocation)[:6]]

    # Build header
    header = "| Scenario | " + " | ".join(c.replace("_", " ").title()[:12] for c in categories) + " |"
    separator = "|" + "|".join(["----------"] * (len(categories) + 1)) + "|"
    lines = [header, separator]

    for name, params in scenarios:
        result = calculate_allocations(
            estimates,
            total_budget,
            exploration_fraction=params["exploration_fraction"],
            min_confidence=params["min_confidence"],
        )
        allocs = {c.category: c.allocation_pct for c in result.categories}
        row = f"| {name} | " + " | ".join(f"{allocs.get(c, 0):.1%}" for c in categories) + " |"
        lines.append(row)

    return "\n".join(lines)


def robustness_check_drop_rcts(estimates: list["EffectEstimate"]) -> str:
    """
    Check robustness by dropping all RCT studies.
    Shows how much allocations depend on gold-standard evidence.
    """
    non_rct = [e for e in estimates if e.method != "rct"]
    rct_only = [e for e in estimates if e.method == "rct"]

    full = calculate_allocations(estimates)
    no_rcts = calculate_allocations(non_rct) if non_rct else None

    lines = [
        f"**RCT sensitivity check:**",
        f"- Full dataset: {len(estimates)} studies ({len(rct_only)} RCTs)",
        f"- Without RCTs: {len(non_rct)} studies",
        "",
    ]

    if no_rcts:
        lines.append("| Category | With RCTs | Without RCTs | Difference |")
        lines.append("|----------|-----------|--------------|------------|")

        full_allocs = {c.category: c.allocation_pct for c in full.categories}
        no_rct_allocs = {c.category: c.allocation_pct for c in no_rcts.categories}

        for cat in sorted(full_allocs.keys()):
            full_pct = full_allocs.get(cat, 0)
            no_rct_pct = no_rct_allocs.get(cat, 0)
            diff = no_rct_pct - full_pct
            sign = "+" if diff >= 0 else ""
            lines.append(
                f"| {cat.replace('_', ' ').title()} | "
                f"{full_pct:.1%} | {no_rct_pct:.1%} | {sign}{diff:.1%} |"
            )

    return "\n".join(lines)


def bootstrap_confidence_intervals(
    estimates: list["EffectEstimate"],
    n_bootstrap: int = 1000,
    total_budget: float = 1_000_000_000_000,
) -> str:
    """
    Bootstrap the allocation algorithm to compute 95% confidence intervals.
    """
    import random

    # Run bootstrap
    bootstrap_allocations: dict[str, list[float]] = {}

    for _ in range(n_bootstrap):
        # Resample estimates with replacement
        resampled = random.choices(estimates, k=len(estimates))
        result = calculate_allocations(resampled, total_budget)

        for cat in result.categories:
            if cat.category not in bootstrap_allocations:
                bootstrap_allocations[cat.category] = []
            bootstrap_allocations[cat.category].append(cat.allocation_pct)

    # Compute percentiles
    lines = [
        "| Category | Point Est. | 95% CI |",
        "|----------|------------|--------|",
    ]

    baseline = calculate_allocations(estimates, total_budget)
    baseline_allocs = {c.category: c.allocation_pct for c in baseline.categories}

    for cat in sorted(baseline_allocs.keys(), key=lambda x: -baseline_allocs.get(x, 0)):
        if cat in bootstrap_allocations:
            vals = sorted(bootstrap_allocations[cat])
            p5 = vals[int(0.025 * len(vals))]
            p95 = vals[int(0.975 * len(vals))]
            point = baseline_allocs[cat]
            lines.append(
                f"| {cat.replace('_', ' ').title()} | "
                f"{point:.1%} | [{p5:.1%}, {p95:.1%}] |"
            )

    return "\n".join(lines)


if __name__ == "__main__":
    run_example()
