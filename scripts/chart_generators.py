#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chart generation utilities for dih_models
==========================================

Generate Quarto QMD files with embedded Python matplotlib code for:
- Tornado charts (sensitivity analysis)
- Sensitivity tables (regression coefficients)
- Input distribution charts (uncertainty visualization)
- Monte Carlo distribution charts (outcome uncertainty)
- CDF/exceedance probability charts (risk assessment)

Functions:
- generate_tornado_chart_qmd() - Tornado chart showing input parameter impacts
- generate_sensitivity_table_qmd() - Markdown table of sensitivity coefficients
- generate_input_distribution_chart_qmd() - Probability distribution for an input
- generate_monte_carlo_distribution_chart_qmd() - Histogram/CDF of MC outcomes
- generate_cdf_chart_qmd() - Standalone exceedance probability chart

Usage:
    from chart_generators import generate_tornado_chart_qmd
    from pathlib import Path

    # Generate tornado chart
    output_path = generate_tornado_chart_qmd(
        param_name="TREATY_COMPLETE_ROI",
        tornado_data={"INPUT_A": {"delta_minus": -10, "delta_plus": 15}, ...},
        output_dir=Path("knowledge/figures/"),
        baseline=100,
        units="ratio"
    )
"""

from pathlib import Path
from typing import Any, Dict

from dih_models.formatting import format_parameter_value
from dih_models.latex_generation import smart_title_case


def generate_tornado_chart_qmd(param_name: str, tornado_data: dict, output_dir: Path, param_metadata: dict = None, baseline: float = None, units: str = "") -> Path:
    """
    Generate a tornado chart QMD file for a parameter with uncertainty.

    Args:
        param_name: Parameter name (e.g., 'TREATY_DFDA_COST_PER_DALY_TIMELINE_SHIFT')
        tornado_data: Dict mapping input names to {delta_minus, delta_plus}
        output_dir: Directory to write QMD file (knowledge/figures/)
        param_metadata: Optional parameter metadata for context
        baseline: Baseline value to center chart on (instead of 0)
        units: Units for x-axis label

    Returns:
        Path to generated QMD file

    Raises:
        ValueError: If tornado_data is empty or has no meaningful drivers
    """
    # Get display name for title
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)

    # Sort by absolute impact (largest first)
    sorted_drivers = sorted(
        tornado_data.items(),
        key=lambda x: abs(x[1].get("delta_minus", 0)) + abs(x[1].get("delta_plus", 0)),
        reverse=True
    )

    # Validate: skip if no drivers or all deltas are zero
    if not sorted_drivers:
        raise ValueError(f"No tornado drivers found for {param_name}")

    # Check if all impacts are effectively zero (< 1e-10 relative to baseline)
    threshold = abs(baseline) * 1e-10 if baseline and abs(baseline) > 0 else 1e-10
    has_meaningful_impact = any(
        abs(data.get("delta_minus", 0)) > threshold or abs(data.get("delta_plus", 0)) > threshold
        for _, data in sorted_drivers
    )

    if not has_meaningful_impact:
        raise ValueError(f"All tornado impacts near zero for {param_name}")

    # Generate Python code for tornado chart
    qmd_content = f'''```{{python}}
#| echo: false

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
)
from dih_models.parameters import format_parameter_value

setup_chart_style()

# Display name for chart title

display_name = "{display_name}"

# Baseline and units

baseline = {baseline if baseline is not None else 0.0}

# Tornado data from sensitivity analysis

drivers = {[driver for driver, _ in sorted_drivers]}
impacts_low = {[data["delta_minus"] for _, data in sorted_drivers]}
impacts_high = {[data["delta_plus"] for _, data in sorted_drivers]}

# Convert deltas to absolute values (baseline + delta)

values_low = [baseline + delta for delta in impacts_low]
values_high = [baseline + delta for delta in impacts_high]

# Create tornado chart (horizontal bars showing swing range)

fig, ax = plt.subplots(figsize=(10, max(6, len(drivers) * 0.8)))

y_pos = np.arange(len(drivers))

# Plot low impact (left side)

for i, (low, high) in enumerate(zip(values_low, values_high)):
    left = min(low, high)
    width_low = baseline - left if left < baseline else 0
    width_high = max(low, high) - baseline if max(low, high) > baseline else 0

    # White bar for range below baseline

    if width_low > 0:
        ax.barh(i, width_low, left=left,
                color=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=2)

    # Black bar for range above baseline

    if width_high > 0:
        ax.barh(i, width_high, left=baseline,
                color=COLOR_BLACK, edgecolor=COLOR_BLACK, linewidth=2)

# Format axis

ax.set_yticks(y_pos)
# Simplified labels (just parameter names)

ax.set_yticklabels([d.replace('_', ' ').title() for d in drivers], fontsize=11)
ax.set_title(f'Sensitivity Analysis: {{display_name}}', fontsize=16, weight='bold', pad=20)

# X-axis label with units

units_label = "{units if units else ""}"
if units_label:
    ax.set_xlabel(f'{{display_name}} ({{units_label}})', fontsize=12)
else:
    ax.set_xlabel(f'{{display_name}}', fontsize=12)

# Add vertical line at baseline

ax.axvline(baseline, color=COLOR_BLACK, linewidth=1, linestyle='--', alpha=0.5)

# Clean spines

clean_spines(ax)

# Add watermark

add_watermark(fig)

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('tornado-{param_name.lower()}.png')
plt.savefig(output_path, dpi=200, bbox_inches=None, facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Sensitivity: {{display_name}}',
    description=f'Tornado diagram showing which input parameters have the largest impact on {{display_name}}'
)

plt.show()
```'''

    # Write QMD file
    output_file = output_dir / f'tornado-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file


def generate_sensitivity_table_qmd(param_name: str, sensitivity_data: dict, output_dir: Path, param_metadata: dict = None, parameters: Dict[str, Dict[str, Any]] = None) -> Path:
    """
    Generate a sensitivity indices table QMD file for a parameter.

    Args:
        param_name: Parameter name
        sensitivity_data: Dict mapping input names to sensitivity coefficients
        output_dir: Directory to write QMD file
        param_metadata: Optional parameter metadata for context
        parameters: Optional dict of all parameter metadata for looking up inputs

    Returns:
        Path to generated QMD file
    """
    # Get display name
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)

    # Sort by absolute sensitivity (largest first)
    sorted_indices = sorted(
        sensitivity_data.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    # Generate markdown table
    qmd_content = f'''**Sensitivity Indices for {display_name}**

Regression-based sensitivity showing which inputs explain the most variance in the output.

| Input Parameter | Sensitivity Coefficient | Interpretation |
|:----------------|------------------------:|:---------------|
'''

    for input_name, coef in sorted_indices:
        # Use parameters dict to find better display name and units
        display_input = smart_title_case(input_name)

        if parameters and input_name in parameters:
            input_val = parameters[input_name]["value"]
            if hasattr(input_val, "display_name") and input_val.display_name:
                display_input = input_val.display_name

            # Add unit if available
            if hasattr(input_val, "unit") and input_val.unit:
                # Use format_parameter_value to get a clean unit string if possible, or just append
                # For brevity in tables, just the unit name is often best
                unit_str = input_val.unit
                # Clean up unit (e.g., don't show "USD" if it's obvious, but maybe good to be explicit)
                display_input = f"{display_input} ({unit_str})"
        # Standardized coefficients range from -1 to 1
        # Use absolute value thresholds appropriate for standardized betas
        abs_coef = abs(coef)
        if abs_coef > 0.5:
            interpretation = "Strong driver"
        elif abs_coef > 0.3:
            interpretation = "Moderate driver"
        elif abs_coef > 0.1:
            interpretation = "Weak driver"
        else:
            interpretation = "Minimal effect"
        qmd_content += f'| {display_input} | {coef:.4f} | {interpretation} |\n'

    qmd_content += '''
*Interpretation*: Standardized coefficients show the change in output (in SD units) per 1 SD change in input. Values near ±1 indicate strong influence; values exceeding ±1 may occur with correlated inputs.
'''

    # Write QMD file
    output_file = output_dir / f'sensitivity-table-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file


def generate_input_distribution_chart_qmd(param_name: str, param_data: dict, output_dir: Path) -> Path:
    """
    Generate a distribution chart for an input parameter showing its uncertainty range.

    This visualizes the assumed probability distribution for external/definition parameters
    that have confidence_interval and/or distribution metadata.

    Args:
        param_name: Parameter name (e.g., 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024')
        param_data: Parameter metadata dict with 'value' key containing Parameter instance
        output_dir: Directory to write QMD file (knowledge/figures/)

    Returns:
        Path to generated QMD file

    Raises:
        ValueError: If parameter has no uncertainty metadata
    """
    value = param_data.get("value")
    if not value:
        raise ValueError(f"No value for parameter {param_name}")

    # Check for uncertainty metadata
    has_ci = hasattr(value, "confidence_interval") and value.confidence_interval
    has_dist = hasattr(value, "distribution") and value.distribution
    has_se = hasattr(value, "std_error") and value.std_error

    if not (has_ci or has_dist or has_se):
        raise ValueError(f"Parameter {param_name} has no uncertainty metadata")

    # Get display name
    if hasattr(value, "display_name") and value.display_name:
        display_name = value.display_name
    else:
        display_name = smart_title_case(param_name)

    # Get values
    central_value = float(value)
    unit = getattr(value, "unit", "")

    # Determine distribution parameters
    if has_ci:
        low, high = value.confidence_interval
    elif has_se:
        # Approximate 95% CI from standard error
        low = central_value - 1.96 * value.std_error
        high = central_value + 1.96 * value.std_error
    else:
        # Default ±20% if only distribution type specified
        low = central_value * 0.8
        high = central_value * 1.2

    # Get distribution type
    dist_type = "normal"  # default
    if has_dist:
        dist_type = value.distribution.value if hasattr(value.distribution, "value") else str(value.distribution)
        dist_type = dist_type.lower()

    # Generate Python code for the chart
    qmd_content = f'''```{{python}}
#| echo: false
#| fig-cap: "Probability Distribution: {display_name}"

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
)

setup_chart_style()

# Parameter values

central_value = {central_value}
low = {low}
high = {high}
dist_type = "{dist_type}"
display_name = "{display_name}"
unit = "{unit}"

# Calculate distribution parameters

if dist_type == "lognormal":
    # For lognormal, we need to work in log space

    # Assume low/high are 5th/95th percentiles

    if central_value > 0 and low > 0:
        mu = np.log(central_value)
        # Estimate sigma from CI width

        sigma = (np.log(high) - np.log(low)) / (2 * 1.645)  # 90% CI
        sigma = max(sigma, 0.1)  # Minimum sigma

        x = np.linspace(max(0.01, low * 0.5), high * 1.5, 500)
        y = stats.lognorm.pdf(x, s=sigma, scale=np.exp(mu))
    else:
        # Fall back to normal if values aren't positive

        dist_type = "normal"

if dist_type == "normal":
    # Estimate sigma from CI width (assuming 95% CI)

    sigma = (high - low) / (2 * 1.96)
    sigma = max(sigma, abs(central_value) * 0.01)  # Minimum 1% of value

    x = np.linspace(low - sigma, high + sigma, 500)
    y = stats.norm.pdf(x, loc=central_value, scale=sigma)

elif dist_type == "uniform":
    x = np.linspace(low * 0.9, high * 1.1, 500)
    y = np.where((x >= low) & (x <= high), 1 / (high - low), 0)

elif dist_type == "triangular":
    # Triangular with mode at central value

    x = np.linspace(low * 0.9, high * 1.1, 500)
    y = stats.triang.pdf(x, c=(central_value - low) / (high - low), loc=low, scale=high - low)

elif dist_type == "beta":
    # Beta distribution scaled to [low, high]

    # Use alpha=2, beta=2 for symmetric bell shape

    x_norm = np.linspace(0, 1, 500)
    x = low + x_norm * (high - low)
    y = stats.beta.pdf(x_norm, a=2, b=2) / (high - low)

elif dist_type == "pert":
    # PERT is a special case of beta

    # Mode = central_value, min = low, max = high

    range_val = high - low
    if range_val > 0:
        # PERT uses alpha = 1 + 4*(mode-min)/(max-min), beta = 1 + 4*(max-mode)/(max-min)

        mode_ratio = (central_value - low) / range_val
        alpha = 1 + 4 * mode_ratio
        beta_param = 1 + 4 * (1 - mode_ratio)
        x_norm = np.linspace(0, 1, 500)
        x = low + x_norm * range_val
        y = stats.beta.pdf(x_norm, a=alpha, b=beta_param) / range_val
    else:
        x = np.array([central_value])
        y = np.array([1])

# Create figure

fig, ax = plt.subplots(figsize=(10, 6))

# Plot distribution

ax.fill_between(x, y, alpha=0.3, color=COLOR_BLACK)
ax.plot(x, y, color=COLOR_BLACK, linewidth=2)

# Mark central value

ax.axvline(central_value, color=COLOR_BLACK, linestyle='--', linewidth=2,
           label=f'Central: {{central_value:,.2g}}')

# Mark confidence interval

ax.axvline(low, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7,
           label=f'95% CI Low: {{low:,.2g}}')
ax.axvline(high, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7,
           label=f'95% CI High: {{high:,.2g}}')

# Shade the CI region

ci_mask = (x >= low) & (x <= high)
ax.fill_between(x, y, where=ci_mask, alpha=0.2, color=COLOR_BLACK)

# Labels

ax.set_xlabel(f'{{display_name}} ({{unit}})' if unit else display_name, fontsize=12)
ax.set_ylabel('Probability Density', fontsize=12)
ax.set_title(f'Assumed Distribution: {{display_name}}', fontsize=14, weight='bold', pad=15)

# Legend

ax.legend(loc='upper right', fontsize=10)

# Clean up

clean_spines(ax)
ax.set_ylim(bottom=0)

# Add watermark

add_watermark(fig)

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('distribution-{param_name.lower()}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Distribution: {{display_name}}',
    description=f'Assumed probability distribution for {{display_name}} showing uncertainty range'
)

plt.show()
```

*This chart shows the assumed probability distribution for this parameter. The shaded region represents the 95% confidence interval where we expect the true value to fall.*
'''

    # Write QMD file
    output_file = output_dir / f'distribution-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file


def generate_monte_carlo_distribution_chart_qmd(
    param_name: str,
    outcome_data: dict,
    samples: list,
    output_dir: Path,
    param_metadata: dict = None
) -> Path:
    """
    Generate a Monte Carlo output distribution chart for a calculated parameter.

    Shows the histogram of simulated outcomes with percentiles and statistics.

    Args:
        param_name: Parameter name (e.g., 'TREATY_COMPLETE_ROI_ALL_BENEFITS')
        outcome_data: Dict with baseline, mean, std, p5, p50, p95, units
        samples: List of Monte Carlo samples for this outcome
        output_dir: Directory to write QMD file
        param_metadata: Optional parameter metadata

    Returns:
        Path to generated QMD file
    """
    # Get display name
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)

    baseline = outcome_data.get("baseline", 0)
    mean = outcome_data.get("mean", baseline)
    std = outcome_data.get("std", 0)
    p5 = outcome_data.get("p5", baseline)
    p50 = outcome_data.get("p50", baseline)
    p95 = outcome_data.get("p95", baseline)
    units = outcome_data.get("units", "")

    # Generate QMD with embedded Python
    qmd_content = f'''```{{python}}
#| echo: false
#| fig-cap: "Monte Carlo Distribution: {display_name} (10,000 simulations)"

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines, get_tick_formatter,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
)
from dih_models.parameters import format_parameter_value

setup_chart_style()

# Simulation results

samples = {samples[:1000] if len(samples) > 1000 else samples}  # Truncate for embedding
baseline = {baseline}
mean = {mean}
std = {std}
p5 = {p5}
p50 = {p50}
p95 = {p95}
display_name = "{display_name}"
units = "{units}"

# Create figure with two subplots

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.subplots_adjust(wspace=0.3)

# --- Left: Histogram ---

# Handle edge case where all samples are identical (zero variance)

if std == 0 or (max(samples) == min(samples)):
    n_bins = 1
else:
    n_bins = min(50, max(1, int(np.sqrt(len(samples)))))
n, bins, patches = ax1.hist(samples, bins=n_bins, color=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=1)

# Apply tick formatter for readable labels (K, M, B suffixes, $ for USD)

ax1.xaxis.set_major_formatter(get_tick_formatter(unit=units))

# Mark key statistics with formatted values in legend (use format_parameter_value for full units)

ax1.axvline(p50, color=COLOR_BLACK, linestyle='--', linewidth=2, label=f'Median: {{format_parameter_value(p50, units)}}')
ax1.axvline(p5, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7, label=f'5th %-ile: {{format_parameter_value(p5, units)}}')
ax1.axvline(p95, color=COLOR_BLACK, linestyle=':', linewidth=1.5, alpha=0.7, label=f'95th %-ile: {{format_parameter_value(p95, units)}}')
ax1.axvline(baseline, color=COLOR_BLACK, linestyle='-', linewidth=1.5, alpha=0.5, label=f'Baseline: {{format_parameter_value(baseline, units)}}')

ax1.set_xlabel(f'{{display_name}} ({{units}})' if units else display_name, fontsize=11)
ax1.set_ylabel('Frequency', fontsize=11)
ax1.set_title('Distribution of Outcomes', fontsize=12, weight='bold')
ax1.legend(loc='upper right', fontsize=9)
clean_spines(ax1)

# --- Right: CDF (Cumulative Probability) ---

sorted_samples = np.sort(samples)
cumulative = np.arange(1, len(sorted_samples) + 1) / len(sorted_samples)

ax2.plot(sorted_samples, cumulative * 100, color=COLOR_BLACK, linewidth=2)
ax2.fill_between(sorted_samples, 0, cumulative * 100, alpha=0.1, color=COLOR_BLACK)

# Apply tick formatter for readable labels (K, M, B suffixes, $ for USD)

ax2.xaxis.set_major_formatter(get_tick_formatter(unit=units))

# Mark key percentiles

ax2.axhline(50, color=COLOR_BLACK, linestyle='--', linewidth=1, alpha=0.5)
ax2.axhline(5, color=COLOR_BLACK, linestyle=':', linewidth=1, alpha=0.5)
ax2.axhline(95, color=COLOR_BLACK, linestyle=':', linewidth=1, alpha=0.5)
ax2.axvline(p50, color=COLOR_BLACK, linestyle='--', linewidth=1, alpha=0.5)

ax2.set_xlabel(f'{{display_name}} ({{units}})' if units else display_name, fontsize=11)
ax2.set_ylabel('Cumulative Probability (%)', fontsize=11)
ax2.set_title('Probability of Exceeding Value', fontsize=12, weight='bold')
ax2.set_ylim(0, 100)
clean_spines(ax2)

# Add annotation for "probability of exceeding baseline"

exceed_baseline_pct = (np.array(samples) > baseline).sum() / len(samples) * 100
ax2.annotate(f'{{exceed_baseline_pct:.0f}}% chance of\\nexceeding baseline',
             xy=(baseline, exceed_baseline_pct), xytext=(baseline * 1.1, exceed_baseline_pct + 10),
             fontsize=9, ha='left',
             arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1))

# Main title

fig.suptitle(f'Monte Carlo Analysis: {{display_name}}', fontsize=14, weight='bold', y=1.02)

# Add watermark

add_watermark(fig)

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('mc-distribution-{param_name.lower()}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Monte Carlo: {{display_name}}',
    description=f'Monte Carlo simulation results showing uncertainty distribution for {{display_name}}'
)

plt.show()
```

**Simulation Results Summary: {display_name}**

| Statistic | Value |
|:----------|------:|
| Baseline (deterministic) | {format_parameter_value(baseline, units, include_unit=False)} |
| Mean (expected value) | {format_parameter_value(mean, units, include_unit=False)} |
| Median (50th percentile) | {format_parameter_value(p50, units, include_unit=False)} |
| Standard Deviation | {format_parameter_value(std, units, include_unit=False)} |
| 90% Confidence Interval | [{format_parameter_value(p5, units, include_unit=False)}, {format_parameter_value(p95, units, include_unit=False)}] |

*The histogram shows the distribution of {display_name} across 10,000 Monte Carlo simulations. The CDF (right) shows the probability of the outcome exceeding any given value, which is useful for risk assessment.*
'''

    # Write QMD file
    output_file = output_dir / f'mc-distribution-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file


def generate_cdf_chart_qmd(
    param_name: str,
    samples: list,
    output_dir: Path,
    param_metadata: dict = None,
    thresholds: list = None
) -> Path:
    """
    Generate a standalone Cumulative Distribution Function (CDF) chart.

    This is the "probability of exceeding X" chart that funders love.

    Args:
        param_name: Parameter name
        samples: List of Monte Carlo samples
        output_dir: Directory to write QMD file
        param_metadata: Optional parameter metadata
        thresholds: Optional list of threshold values to annotate (e.g., [10, 50, 100] for ROI)

    Returns:
        Path to generated QMD file
    """
    # Get display name
    if param_metadata and hasattr(param_metadata.get("value"), "display_name"):
        display_name = param_metadata["value"].display_name
    else:
        display_name = smart_title_case(param_name)

    units = ""
    if param_metadata and hasattr(param_metadata.get("value"), "unit"):
        units = param_metadata["value"].unit or ""

    # Auto-generate thresholds if not provided
    if thresholds is None:
        sorted_s = sorted(samples)
        p10 = sorted_s[int(len(sorted_s) * 0.10)]
        p50 = sorted_s[int(len(sorted_s) * 0.50)]
        p90 = sorted_s[int(len(sorted_s) * 0.90)]
        thresholds = [p10, p50, p90]

    qmd_content = f'''```{{python}}
#| echo: false
#| fig-cap: "Probability of Exceeding Threshold: {display_name}"

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from dih_models.plotting.chart_style import (
    setup_chart_style, add_watermark, clean_spines, get_tick_formatter,
    COLOR_BLACK, COLOR_WHITE, add_png_metadata, get_figure_output_path
)
from dih_models.parameters import format_parameter_value

setup_chart_style()

# Monte Carlo samples

samples = {samples[:2000] if len(samples) > 2000 else samples}
thresholds = {thresholds}
display_name = "{display_name}"
units = "{units}"

# Calculate exceedance probabilities (1 - CDF)

sorted_samples = np.sort(samples)
exceedance = 1 - np.arange(1, len(sorted_samples) + 1) / len(sorted_samples)

# Create figure

fig, ax = plt.subplots(figsize=(10, 6))

# Plot exceedance curve

ax.plot(sorted_samples, exceedance * 100, color=COLOR_BLACK, linewidth=2.5)
ax.fill_between(sorted_samples, 0, exceedance * 100, alpha=0.1, color=COLOR_BLACK)

# Apply tick formatter for readable labels (K, M, B suffixes, $ for USD)

ax.xaxis.set_major_formatter(get_tick_formatter(unit=units))

# Annotate thresholds

for thresh in thresholds:
    exceed_pct = (np.array(samples) >= thresh).sum() / len(samples) * 100
    ax.axvline(thresh, color=COLOR_BLACK, linestyle='--', linewidth=1, alpha=0.5)
    ax.axhline(exceed_pct, color=COLOR_BLACK, linestyle=':', linewidth=1, alpha=0.3)

    # Add label with formatted threshold value (use format_parameter_value for full units)

    ax.annotate(f'{{exceed_pct:.0f}}% chance\\n≥ {{format_parameter_value(thresh, units)}}',
                xy=(thresh, exceed_pct), xytext=(thresh * 1.05, exceed_pct + 5),
                fontsize=10, ha='left', weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, alpha=0.9))

ax.set_xlabel(f'{{display_name}} ({{units}})' if units else display_name, fontsize=12)
ax.set_ylabel('Probability of Exceeding Value (%)', fontsize=12)
ax.set_title(f'Exceedance Probability: {{display_name}}', fontsize=14, weight='bold', pad=15)
ax.set_ylim(0, 100)
ax.set_xlim(left=min(sorted_samples) * 0.95)

clean_spines(ax)
add_watermark(fig)

# Save PNG to knowledge/figures/ regardless of where Quarto renders from

output_path = get_figure_output_path('exceedance-{param_name.lower()}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=COLOR_WHITE)

add_png_metadata(
    output_path,
    title=f'Exceedance: {{display_name}}',
    description=f'Probability of {{display_name}} exceeding various thresholds'
)

plt.show()
```

*This exceedance probability chart shows the likelihood that {display_name} will exceed any given threshold. Higher curves indicate more favorable outcomes with greater certainty.*
'''

    # Write QMD file
    output_file = output_dir / f'exceedance-{param_name.lower()}.qmd'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(qmd_content)

    return output_file
