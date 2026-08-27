# -*- coding: utf-8 -*-
import sys

from dih_models.chart_generators import (
    generate_cdf_chart_qmd,
    generate_monte_carlo_distribution_chart_qmd,
)
from dih_models.parameters import Parameter


if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore


def _parameter() -> Parameter:
    return Parameter(
        50,
        manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
        source_type="definition",
        description="Synthetic parameter used to verify generated chart labels.",
        display_name="A deliberately long parameter name for prose and metadata",
        chart_label="Concise outcome",
        unit="years",
    )


def test_monte_carlo_chart_uses_concise_axis_label(tmp_path) -> None:
    output = generate_monte_carlo_distribution_chart_qmd(
        "TEST_OUTCOME",
        {
            "baseline": 50,
            "mean": 55,
            "std": 10,
            "p5": 35,
            "p50": 54,
            "p95": 75,
            "units": "years",
        },
        list(range(100)),
        tmp_path,
        {"value": _parameter()},
    ).read_text(encoding="utf-8")

    assert "ax1.set_xlabel('Concise outcome (years)'" in output
    assert "ax2.set_xlabel('Concise outcome (years)'" in output
    assert "Simulation Results Summary: A deliberately long parameter name" in output


def test_exceedance_chart_uses_concise_caption_axis_and_title(tmp_path) -> None:
    output = generate_cdf_chart_qmd(
        "TEST_OUTCOME",
        list(range(1, 101)),
        tmp_path,
        {"value": _parameter()},
    ).read_text(encoding="utf-8")

    assert 'fig-cap: "Probability of Exceeding Threshold: Concise outcome"' in output
    assert "chart_label = \"Concise outcome\"" in output
    assert "Exceedance Probability: {chart_label}" in output
