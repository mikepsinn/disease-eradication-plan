import io
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

from dih_models import chart_generators  # noqa: E402
from dih_models.plotting import chart_style  # noqa: E402

if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")


# Like dfda_trial_subsidies_annual: a spread of millions around tens of billions
BASELINE = 21_760_000_000.0
NARROW_SAMPLES = list(BASELINE + np.random.default_rng(0).normal(0, 4_000_000, 2_000))


def tight_width_ratio(qmd_path: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> float:
    """Run a generated chart and return its tight crop width over its figure width."""
    monkeypatch.setattr(chart_style, "get_figure_output_path", lambda name: tmp_path / name)
    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: None)
    match = re.search(r"```\{python\}\n(.*?)\n```", qmd_path.read_text(encoding="utf-8"), re.S)
    assert match
    exec(compile(match.group(1), str(qmd_path), "exec"), {"__name__": "__main__"})

    figure = plt.gcf()
    # Quarto crops PDF figures this way; LaTeX fails on images wider than 16,384 pt
    tight = figure.get_tightbbox()
    ratio = tight.width / figure.get_size_inches()[0]
    plt.close(figure)
    return ratio


def test_monte_carlo_chart_keeps_its_label_on_a_narrow_distribution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    samples = np.array(NARROW_SAMPLES)
    outcome = {
        "baseline": BASELINE,
        "mean": float(samples.mean()),
        "std": float(samples.std()),
        "p5": float(np.percentile(samples, 5)),
        "p50": float(np.percentile(samples, 50)),
        "p95": float(np.percentile(samples, 95)),
        "units": "USD/year",
    }
    qmd_path = chart_generators.generate_monte_carlo_distribution_chart_qmd(
        "narrow_outcome", outcome, NARROW_SAMPLES, tmp_path
    )

    # Before the fix the label sat at 1.1 x the baseline: the crop was 26 times the figure width
    assert tight_width_ratio(qmd_path, tmp_path, monkeypatch) < 1.3


def test_exceedance_chart_keeps_its_labels_on_a_narrow_distribution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    qmd_path = chart_generators.generate_cdf_chart_qmd("narrow_outcome", NARROW_SAMPLES, tmp_path)

    # Before the fix the labels sat at 1.05 x each threshold: the crop was 1.9 times the figure width
    assert tight_width_ratio(qmd_path, tmp_path, monkeypatch) < 1.3
