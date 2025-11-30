"""
Uncertainty and Sensitivity Utilities
=====================================

This module provides Monte Carlo sampling and simple sensitivity analysis
for `Parameter` instances defined in `dih_models/parameters.py`.

Design goals:
- Zero-coupling: do not modify existing Parameter class to work.
- Use available metadata: `distribution`, `std_error`, `confidence_interval`,
  `validation_min/max`, and `formula` for calculated values.
- Deterministic seeds for reproducibility when requested.

Exports:
- sample_parameter(param, n, seed=None): numpy array of samples
- simulate(parameters: dict, n: int = 10000, seed: int | None = None):
    Returns dict of sampled arrays for each parameter name.
- one_at_a_time_sensitivity(parameters: dict, target_name: str, n: int = 1000):
    Varies each input parameter ±1 std and measures effect on target.

Note: We avoid heavy external deps. If numpy is unavailable, we fallback
to Python's random and basic math with reduced performance.
"""

from __future__ import annotations

import math
import random
from typing import Dict, Any, Tuple, Sequence, cast, Callable, List, Optional

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    np = None  # Fallback handled below

try:
    # Import Parameter and DistributionType without causing side effects
    from .parameters import Parameter, DistributionType
except Exception:  # pragma: no cover
    Parameter = Any  # type: ignore
    DistributionType = Any  # type: ignore


def _rng(seed: int | None):
    if np is not None:
        return np.random.default_rng(seed)
    random.seed(seed or 0)
    return None


def _bounded(value: float, bounds: Tuple[float | None, float | None]):
    lo, hi = bounds
    if lo is not None:
        value = max(value, lo)
    if hi is not None:
        value = min(value, hi)
    return value


def _get_bounds(param: Parameter) -> Tuple[float | None, float | None]:
    lo = getattr(param, "validation_min", None)
    hi = getattr(param, "validation_max", None)
    # If CI available, use it as soft bounds when validation_* missing
    ci = getattr(param, "confidence_interval", None)
    if ci and (lo is None or hi is None):
        if isinstance(ci, Sequence) and len(ci) == 2:
            lo = ci[0] if lo is None else lo
            hi = ci[1] if hi is None else hi
    return lo, hi


def sample_parameter(param: Parameter, n: int = 10000, seed: int | None = None):
    """Sample from a Parameter's uncertainty distribution.

    Strategy:
    - Normal: mean=param, sd=std_error if provided, else inferred from CI
    - Lognormal: infer mu/sigma from mean and std_error or CI
    - Gamma: shape/scale from mean and std_error
    - If no distribution metadata: return constant array of param value
    - Respect validation_min/max and clip
    """

    mean = float(param)
    dist = getattr(param, "distribution", None)
    std = getattr(param, "std_error", None)
    ci = getattr(param, "confidence_interval", None)
    bounds = _get_bounds(param)

    rng = _rng(seed)

    def infer_std_from_ci(ci_tuple):
        if not ci_tuple or len(ci_tuple) != 2:
            return None
        # assume 95% CI ~ mean ± 1.96*sd for Normal
        lo, hi = ci_tuple
        return (hi - lo) / (2 * 1.96)

    if std is None:
        std = infer_std_from_ci(ci)

    # Fallback constant if no variability
    if dist is None or std is None or std == 0:
        if np is not None:
            return np.full(n, _bounded(mean, bounds))
        return [_bounded(mean, bounds) for _ in range(n)]

    # Sampling per distribution
    if dist == getattr(DistributionType, "NORMAL", "NORMAL"):
        if np is not None:
            samples = rng.normal(loc=mean, scale=std, size=n)
            return np.clip(samples, bounds[0] if bounds[0] is not None else -np.inf,
                           bounds[1] if bounds[1] is not None else np.inf)
        # Python fallback
        s = [_bounded(random.gauss(mean, std), bounds) for _ in range(n)]
        return s

    if dist == getattr(DistributionType, "LOGNORMAL", "LOGNORMAL"):
        # Convert mean/std to log-space params
        # For lognormal: mean = exp(mu + 0.5*sigma^2), var = (exp(sigma^2)-1)exp(2mu+sigma^2)
        if std <= 0:
            if np is not None:
                return np.full(n, _bounded(mean, bounds))
            return [_bounded(mean, bounds) for _ in range(n)]
        variance = std ** 2
        sigma2 = math.log(1 + variance / (mean ** 2))
        sigma = math.sqrt(sigma2)
        mu = math.log(mean) - 0.5 * sigma2
        if np is not None:
            samples = rng.lognormal(mean=mu, sigma=sigma, size=n)
            return np.clip(samples, bounds[0] if bounds[0] is not None else -np.inf,
                           bounds[1] if bounds[1] is not None else np.inf)
        s = [_bounded(math.exp(random.gauss(mu, sigma)), bounds) for _ in range(n)]
        return s

    if dist == getattr(DistributionType, "GAMMA", "GAMMA"):
        # shape k, scale theta with mean = k*theta, var = k*theta^2
        if std <= 0 or mean <= 0:
            if np is not None:
                return np.full(n, _bounded(mean, bounds))
            return [_bounded(mean, bounds) for _ in range(n)]
        var = std ** 2
        theta = var / mean
        k = mean / theta
        if np is not None:
            samples = rng.gamma(shape=k, scale=theta, size=n)
            return np.clip(samples, bounds[0] if bounds[0] is not None else -np.inf,
                           bounds[1] if bounds[1] is not None else np.inf)
        # Python fallback: approximate via sum of exponentials for integer k
        k_int = max(1, int(round(k)))
        s = []
        for _ in range(n):
            total = sum(random.expovariate(1/theta) for _ in range(k_int))
            s.append(_bounded(total, bounds))
        return s

    # Default fallback: constant
    if np is not None:
        return np.full(n, _bounded(mean, bounds))
    return [_bounded(mean, bounds) for _ in range(n)]


def simulate(parameters: Dict[str, Dict[str, Any]], n: int = 10000, seed: int | None = None):
    """Sample all Parameter values.

    `parameters` is the dict produced by parse_parameters_file(), where each
    value may hold a `Parameter` instance under `metadata['value']`.
    Returns a dict: name -> samples (numpy array or list).
    """
    results = {}
    for name, meta in parameters.items():
        val = meta.get("value")
        if isinstance(val, Parameter):
            results[name] = sample_parameter(val, n=n, seed=seed)
        else:
            # Plain numeric
            try:
                v = float(val)
            except Exception:
                continue
            if np is not None:
                results[name] = np.full(n, v)
            else:
                results[name] = [v for _ in range(n)]
    return results


def one_at_a_time_sensitivity(parameters: Dict[str, Dict[str, Any]], target_name: str, n: int = 1000):
    """Compute simple One-At-A-Time sensitivity on calculated `target_name`.

    Assumes `parameters[target_name]['value']` is a Parameter derived via
    arithmetic of other Parameters (sum/products). Since formulas are not
    executable here, we approximate by varying each input's samples ±1 std
    and recomputing algebra if possible (sum/product detection).

    Returns dict: input_name -> { 'delta_mean': float, 'delta_pct': float }
    """
    target_meta = parameters.get(target_name)
    if not target_meta:
        raise KeyError(f"Target parameter '{target_name}' not found")
    target_val = target_meta.get("value")

    # Heuristic: try to parse a simple formula string
    formula = getattr(target_val, "formula", None)
    inputs: Sequence[str] = []
    if isinstance(formula, str):
        # Extract tokens that look like uppercase parameter names
        tokens = [t for t in formula.replace("+", " ").replace("*", " ").replace("-", " ").split()
                  if t.isupper() and t in parameters]
        inputs = tokens

    # Fallback: sensitivity to all other Parameter inputs would be too large; limit
    inputs = inputs[:12]

    if not inputs:
        return {}

    # Baseline samples
    sims = simulate({name: parameters[name] for name in inputs}, n=n)
    if np is None:
        # Compute baseline sum/product based on formula hints
        baseline = 0.0
        if isinstance(formula, str) and "+" in formula and "*" not in formula:
            baseline = sum(sum(sims[name]) / n for name in inputs)
        elif isinstance(formula, str) and "*" in formula and "+" not in formula:
            prod_vals = [sum(sims[name]) / n for name in inputs]
            baseline = math.prod(prod_vals)
        else:
            baseline = sum(sum(sims[name]) / n for name in inputs)
    else:
        means = [float(np.mean(np.asarray(cast(Any, sims[name])))) for name in inputs]
        if isinstance(formula, str) and "+" in formula and "*" not in formula:
            baseline = float(sum(means))
        elif isinstance(formula, str) and "*" in formula and "+" not in formula:
            baseline = float(np.prod(means))
        else:
            baseline = float(sum(means))

    out: Dict[str, Dict[str, float]] = {}
    for name in inputs:
        meta = parameters[name]
        val = meta.get("value")
        if not isinstance(val, Parameter):
            continue
        std = getattr(val, "std_error", None)
        if std in (None, 0):
            continue
        # Perturb up and down
        mean_v = float(val)
        up = mean_v + std
        down = mean_v - std

        # Recompute baseline with perturbed input
        if np is None:
            if isinstance(formula, str) and "+" in formula and "*" not in formula:
                new_mean_up = baseline - (sum(sims[name]) / n) + up
                new_mean_down = baseline - (sum(sims[name]) / n) + down
            else:
                # Simplified: treat as sum-style
                new_mean_up = baseline - (sum(sims[name]) / n) + up
                new_mean_down = baseline - (sum(sims[name]) / n) + down
        else:
            means = {i: float(np.mean(np.asarray(cast(Any, sims[i])))) for i in inputs}
            if isinstance(formula, str) and "+" in formula and "*" not in formula:
                new_mean_up = sum((means[i] if i != name else up) for i in inputs)
                new_mean_down = sum((means[i] if i != name else down) for i in inputs)
            elif isinstance(formula, str) and "*" in formula and "+" not in formula:
                vec_up = [ (means[i] if i != name else up) for i in inputs ]
                vec_down = [ (means[i] if i != name else down) for i in inputs ]
                new_mean_up = float(np.prod(vec_up))
                new_mean_down = float(np.prod(vec_down))
            else:
                new_mean_up = sum( (means[i] if i != name else up) for i in inputs )
                new_mean_down = sum( (means[i] if i != name else down) for i in inputs )

        delta = (new_mean_up - new_mean_down) / 2.0
        pct = (delta / baseline) * 100.0 if baseline != 0 else 0.0
        out[name] = {"delta_mean": float(delta), "delta_pct": float(pct)}

    return out


# ---
# Outcome wrapper for rigorous sensitivity on derived metrics
# ---

class Outcome:
    """Represents a derived analysis metric (e.g., ROI, ICER).

    Provide `name`, `inputs` (parameter names), and a pure `compute(context)`
    callable that returns the outcome given a dict of parameter values.
    """

    def __init__(
        self,
        name: str,
        inputs: List[str],
        compute: Callable[[Dict[str, float]], float],
        units: Optional[str] = None,
    ) -> None:
        self.name = name
        self.inputs = inputs
        self.compute = compute
        self.units = units or ""


def get_fundamental_inputs(parameters: Dict[str, Dict[str, Any]], param_name: str, visited: Optional[set] = None) -> set:
    """
    Recursively find all fundamental (leaf) parameters that a calculated parameter depends on.
    
    A fundamental parameter is one that either:
    - Has no inputs (is a constant/measured value)
    - Has uncertainty (distribution, confidence_interval, or std_error)
    
    Args:
        parameters: Full parameters dictionary
        param_name: Name of parameter to analyze
        visited: Set of already-visited params (for cycle detection)
    
    Returns:
        Set of fundamental parameter names
    """
    if visited is None:
        visited = set()
    
    if param_name in visited:
        return set()  # Avoid cycles
    
    visited.add(param_name)
    
    meta = parameters.get(param_name, {})
    val = meta.get("value")
    
    # Check if this parameter has uncertainty (is fundamental)
    has_uncertainty = (
        hasattr(val, "distribution") and val.distribution or
        hasattr(val, "confidence_interval") and val.confidence_interval or
        hasattr(val, "std_error") and val.std_error
    )
    
    # Check if this parameter has inputs (is calculated)
    has_inputs = hasattr(val, "inputs") and val.inputs
    
    # If no inputs, it's fundamental (leaf node)
    if not has_inputs:
        if has_uncertainty:
            return {param_name}
        else:
            return set()  # Constant with no uncertainty
    
    # If has uncertainty AND inputs, this is a calculated parameter with its own uncertainty
    # We could either:
    # 1. Treat it as fundamental (stop here)
    # 2. Expand it to show component uncertainties
    # Let's expand to show more detail
    
    # Recursively expand all inputs
    fundamental = set()
    for inp in val.inputs:
        fundamental.update(get_fundamental_inputs(parameters, inp, visited))
    
    return fundamental


def tornado_deltas(parameters: Dict[str, Dict[str, Any]], outcome: Outcome, expand_inputs: bool = True) -> Dict[str, Dict[str, float]]:
    """Deterministic sensitivity (tornado) using low/high per input.

    Uses each input's `std_error` or `confidence_interval` to derive low/high.
    Returns mapping: input -> {delta_minus, delta_plus} relative to baseline.
    
    Args:
        parameters: Full parameters dictionary
        outcome: Outcome with compute function and inputs
        expand_inputs: If True, recursively expand calculated inputs to fundamental parameters
    """
    # Decide which inputs to analyze
    if expand_inputs:
        # Recursively find all fundamental inputs
        all_fundamental = set()
        for direct_input in outcome.inputs:
            all_fundamental.update(get_fundamental_inputs(parameters, direct_input))
        inputs_to_analyze = sorted(all_fundamental)  # Sort for deterministic order
    else:
        # Use only direct inputs (old behavior)
        inputs_to_analyze = outcome.inputs
    
    # Build baseline context (need ALL inputs for compute, not just fundamental)
    ctx = {}
    for name in outcome.inputs:
        meta = parameters.get(name, {})
        val = meta.get("value")
        ctx[name] = float(val) if val is not None else 0.0
    baseline = outcome.compute(cast(Dict[str, float], ctx))

    def low_high(v: Any) -> Tuple[float, float]:
        m = float(v)
        std = getattr(v, "std_error", None)
        ci = getattr(v, "confidence_interval", None)
        if ci and isinstance(ci, Sequence) and len(cast(Sequence[Any], ci)) == 2:
            return float(cast(Sequence[Any], ci)[0]), float(cast(Sequence[Any], ci)[1])
        if std and std > 0:
            return m - std, m + std
        return m, m
    
    def evaluate_param(param_name: str, overrides: Dict[str, float]) -> float:
        """Evaluate a parameter with overrides propagated through dependencies."""
        meta = parameters.get(param_name, {})
        val = meta.get("value")
        
        # If overridden directly, use that
        if param_name in overrides:
            return overrides[param_name]
        
        # If has compute function, recursively evaluate inputs
        if hasattr(val, "compute") and val.compute and hasattr(val, "inputs") and val.inputs:
            sub_ctx = {}
            for inp in val.inputs:
                sub_ctx[inp] = evaluate_param(inp, overrides)
            return val.compute(sub_ctx)
        
        # Otherwise use base value
        return float(val) if val is not None else 0.0

    deltas: Dict[str, Dict[str, float]] = {}
    for name in inputs_to_analyze:
        meta = parameters.get(name, {})
        val = meta.get("value")
        lo, hi = low_high(val)
        
        # Skip if no uncertainty
        if lo == hi:
            continue
        
        # Evaluate outcome with fundamental input varied (propagates through calc chain)
        # minus
        overrides_minus = {name: lo}
        ctx_minus = {}
        for direct_inp in outcome.inputs:
            ctx_minus[direct_inp] = evaluate_param(direct_inp, overrides_minus)
        y_minus = outcome.compute(ctx_minus)
        
        # plus
        overrides_plus = {name: hi}
        ctx_plus = {}
        for direct_inp in outcome.inputs:
            ctx_plus[direct_inp] = evaluate_param(direct_inp, overrides_plus)
        y_plus = outcome.compute(ctx_plus)
        
        deltas[name] = {
            "delta_minus": float(y_minus - baseline),
            "delta_plus": float(y_plus - baseline),
        }
    
    # Sort by max abs delta for presentation (caller may sort again)
    return dict(sorted(deltas.items(), key=lambda kv: max(abs(kv[1]["delta_minus"]), abs(kv[1]["delta_plus"])), reverse=True))


def regression_sensitivity(samples: Dict[str, Any], outcome_samples: Sequence[float]) -> Dict[str, float]:
    """Compute standardized regression coefficients as sensitivity indices.

    `samples`: name -> array-like of sampled input values
    `outcome_samples`: array-like of outcome values per simulation
    Returns: name -> standardized beta coefficient
    """
    if np is None:
        # Fallback: simple correlation coefficient per input
        vals = list(outcome_samples)
        def corr(x: Sequence[float]) -> float:
            xm = sum(x)/len(x)
            ym = sum(vals)/len(vals)
            cov = sum((xi - xm)*(yi - ym) for xi, yi in zip(x, vals)) / len(x)
            vx = sum((xi - xm)**2 for xi in x)/len(x)
            vy = sum((yi - ym)**2 for yi in vals)/len(vals)
            denom = (vx * vy) ** 0.5 if vx > 0 and vy > 0 else 1.0
            return cov / denom if denom != 0 else 0.0
        return {name: corr(list(arr)) for name, arr in samples.items()}

    # Standardize inputs
    X_list: List[Any] = []
    names = list(samples.keys())
    for name in names:
        a = np.asarray(samples[name], dtype=float)
        mu = np.mean(a)
        sd = np.std(a)
        X_list.append((a - mu) / (sd if sd != 0 else 1))
    X = np.vstack(X_list).T  # shape (n, p)
    y = np.asarray(outcome_samples, dtype=float)
    # OLS beta = (X'X)^(-1) X'y
    XtX = X.T @ X
    try:
        beta = np.linalg.solve(XtX, X.T @ y)
    except Exception:
        beta = np.linalg.pinv(XtX) @ (X.T @ y)
    return {name: float(b) for name, b in zip(names, beta)}
