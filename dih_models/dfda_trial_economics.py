"""
DFDA trial queue clearance economics.

Computes the funding -> capacity multiplier -> acceleration -> DALYs -> cost
pipeline that is shared across multiple chart QMD files.

All parameter values are read from dih_models.parameters at call time.

Usage (inside a QMD that already ran `from dih_models.parameters import *`):

    from dih_models.dfda_trial_economics import compute_at_funding_level
    result = compute_at_funding_level()          # uses proposed treaty funding
    result = compute_at_funding_level(50e9)      # custom funding level
"""

from __future__ import annotations

import numpy as np

from dih_models.parameters import (
    CURRENT_TRIAL_SLOTS_AVAILABLE,
    DFDA_ANNUAL_OPEX,
    DFDA_ANNUAL_TRIAL_FUNDING,
    DFDA_NPV_UPFRONT_COST_TOTAL,
    DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    EFFICACY_LAG_YEARS,
    EVENTUALLY_AVOIDABLE_DALY_PCT,
    GLOBAL_ANNUAL_DALY_BURDEN,
    NPV_DISCOUNT_RATE_STANDARD,
    STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT,
    STATUS_QUO_QUEUE_CLEARANCE_YEARS,
    _timeline_shift_discounted_years,
)


# ── Helpers to read parameters as plain floats ──────────────────────────

def _params() -> dict:
    """Load all relevant parameters as plain floats."""
    return dict(
        opex=float(DFDA_ANNUAL_OPEX),
        cost_per_patient=float(DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT),
        current_slots=float(CURRENT_TRIAL_SLOTS_AVAILABLE),
        baseline_wait=float(STATUS_QUO_AVG_YEARS_TO_FIRST_TREATMENT),
        sq_queue=float(STATUS_QUO_QUEUE_CLEARANCE_YEARS),
        efficacy_lag=float(EFFICACY_LAG_YEARS),
        annual_daly_burden=float(GLOBAL_ANNUAL_DALY_BURDEN),
        avoidable_pct=float(EVENTUALLY_AVOIDABLE_DALY_PCT),
        proposed_funding=float(DFDA_ANNUAL_TRIAL_FUNDING),
        upfront_cost=float(DFDA_NPV_UPFRONT_COST_TOTAL),
        discount_rate=float(NPV_DISCOUNT_RATE_STANDARD),
    )


# ── Core computation ────────────────────────────────────────────────────

def compute_at_funding_level(funding: float | None = None) -> dict:
    """
    Compute the full funding->DALYs->cost chain at a single funding level.

    Args:
        funding: Annual funding in USD.  Defaults to proposed funding level.

    Returns:
        dict with keys: funding, subsidy, multiplier, clearance_years,
        accel_years, total_shift, dalys_averted (undiscounted count),
        dalys_averted_discounted, total_cost (present value), cost_per_daly.
        Returns None for values that cannot be computed (funding too low).

    Cost per DALY discounts costs and DALYs at the same standard rate, matching
    DFDA_DIRECT_FUNDING_COST_PER_DALY.
    """
    p = _params()
    if funding is None:
        funding = p["proposed_funding"]

    subsidy = funding - p["opex"]
    if subsidy <= 0:
        return dict(funding=funding, subsidy=subsidy,
                    multiplier=None, clearance_years=None, accel_years=None,
                    total_shift=None, dalys_averted=None,
                    dalys_averted_discounted=None, total_cost=None,
                    cost_per_daly=None)

    patients = subsidy / p["cost_per_patient"]
    multiplier = patients / p["current_slots"]
    if multiplier <= 1:
        return dict(funding=funding, subsidy=subsidy, multiplier=multiplier,
                    clearance_years=None, accel_years=None, total_shift=None,
                    dalys_averted=None, dalys_averted_discounted=None,
                    total_cost=None, cost_per_daly=None)

    r = p["discount_rate"]
    clearance_years = p["sq_queue"] / multiplier
    accel_years = p["baseline_wait"] * (1 - 1 / multiplier)
    total_shift = accel_years + p["efficacy_lag"]
    burden = p["annual_daly_burden"] * p["avoidable_pct"]
    dalys_averted = burden * total_shift
    dalys_averted_discounted = burden * _timeline_shift_discounted_years(
        p["sq_queue"], clearance_years, p["efficacy_lag"], r)
    # Continuous spending, matching DFDA_DIRECT_FUNDING_QUEUE_CLEARANCE_NPV and the discounted DALYs
    total_cost = p["upfront_cost"] + funding * (1 - (1 + r) ** -clearance_years) / np.log(1 + r)
    cost_per_daly = total_cost / dalys_averted_discounted

    return dict(
        funding=funding,
        subsidy=subsidy,
        multiplier=multiplier,
        clearance_years=clearance_years,
        accel_years=accel_years,
        total_shift=total_shift,
        dalys_averted=dalys_averted,
        dalys_averted_discounted=dalys_averted_discounted,
        total_cost=total_cost,
        cost_per_daly=cost_per_daly,
    )


def compute_across_funding_levels(
    funding_array: np.ndarray | None = None,
) -> dict:
    """
    Vectorised computation across an array of funding levels.

    Args:
        funding_array: 1-D array of annual funding values (USD).
            Defaults to logspace from $100M to $200B (200 points).

    Returns:
        dict with keys: funding_levels, cost_per_daly, dalys_averted
        (numpy arrays; entries are NaN where funding is below threshold).
    """
    if funding_array is None:
        funding_array = np.logspace(np.log10(1e8), np.log10(2e11), 200)
    funding_levels = np.asarray(funding_array, dtype=float)

    cost_per_daly = np.full_like(funding_levels, np.nan)
    dalys_averted = np.full_like(funding_levels, np.nan)

    for i, funding in enumerate(funding_levels):
        result = compute_at_funding_level(float(funding))
        if result["cost_per_daly"] is None:
            continue
        dalys_averted[i] = result["dalys_averted"]
        cost_per_daly[i] = result["cost_per_daly"]

    return dict(
        funding_levels=funding_levels,
        cost_per_daly=cost_per_daly,
        dalys_averted=dalys_averted,
    )


# ── Asymptotic limits ───────────────────────────────────────────────────

def get_ceiling_dalys() -> float:
    """Maximum possible DALYs averted (at infinite funding).

    = annual_daly_burden * avoidable_pct * (baseline_wait + efficacy_lag)
    """
    p = _params()
    return p["annual_daly_burden"] * p["avoidable_pct"] * (p["baseline_wait"] + p["efficacy_lag"])


def get_floor_queue_cost() -> float:
    """Total cost to clear the queue at infinite speed (all spent at t=0, so no discounting).

    = sq_queue * cost_per_patient * current_slots
    This is the minimum total trial expenditure regardless of speed.
    """
    p = _params()
    return p["sq_queue"] * p["cost_per_patient"] * p["current_slots"]


def get_floor_cost_per_daly() -> float:
    """Asymptotic minimum cost/DALY at infinite funding.

    = (upfront_cost + floor_queue_cost) / discounted ceiling DALYs, where every
    first treatment arrives at t=0 and the status quo is unchanged.
    """
    p = _params()
    floor_cost = get_floor_queue_cost()
    ceiling_dalys_discounted = p["annual_daly_burden"] * p["avoidable_pct"] * _timeline_shift_discounted_years(
        p["sq_queue"], 0.0, p["efficacy_lag"], p["discount_rate"])
    return (p["upfront_cost"] + floor_cost) / ceiling_dalys_discounted


def get_efficacy_lag_dalys() -> float:
    """DALYs averted from efficacy lag elimination alone (fixed baseline).

    = annual_daly_burden * avoidable_pct * efficacy_lag
    """
    p = _params()
    return p["annual_daly_burden"] * p["avoidable_pct"] * p["efficacy_lag"]
