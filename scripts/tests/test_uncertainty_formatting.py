# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from types import SimpleNamespace

from dih_models.chart_generators import (
    generate_cdf_chart_qmd,
    generate_monte_carlo_distribution_chart_qmd,
)
from dih_models.parameters import Parameter
from dih_models.quarto_formatting import generate_uncertainty_section


if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore


def test_custom_lognormal_range_is_described_as_clipped_model_bounds() -> None:
    parameter = Parameter(
        65_000_000,
        confidence_interval=(25_000_000, 200_000_000),
        distribution="lognormal",
        interval_label="modeled range",
        manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
        unit="USD",
    )

    section = "\n".join(generate_uncertainty_section(parameter, "USD"))

    assert "clips draws to the modeled bounds" in section
    assert "statistical confidence interval" in section
    assert "±" not in section


def test_custom_chart_label_reports_embedded_and_summary_draw_counts(tmp_path: Path) -> None:
    parameter = SimpleNamespace(
        chart_label="Disability-equivalent years prevented",
        display_name="Long modeled outcome name",
        unit="years",
    )
    output_path = generate_monte_carlo_distribution_chart_qmd(
        "MODELED_OUTCOME",
        {
            "baseline": 50,
            "mean": 55,
            "std": 10,
            "p5": 35,
            "p50": 54,
            "p95": 75,
            "units": "years",
        },
        list(range(10_000)),
        tmp_path,
        {"value": parameter},
    )

    chart = output_path.read_text(encoding="utf-8")
    assert "1,000 plotted draws; 10,000 summary draws" in chart
    assert "Cumulative Probability" in chart
    assert "10,000 simulations" not in chart


def test_cost_exceedance_chart_marks_lower_curves_as_favorable(tmp_path: Path) -> None:
    parameter = SimpleNamespace(
        chart_label="Cost per life saved",
        display_name="Launch Cost per Life Saved",
        unit="USD/life",
    )
    output_path = generate_cdf_chart_qmd(
        "LAUNCH_COST_PER_LIFE",
        list(range(1, 101)),
        tmp_path,
        {"value": parameter},
    )

    chart = output_path.read_text(encoding="utf-8")
    assert "Probability of Exceeding Threshold: Cost per life saved" in chart
    assert "lower curves indicate more favorable results" in chart
