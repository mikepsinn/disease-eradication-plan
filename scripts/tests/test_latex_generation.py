from pathlib import Path

from dih_models.latex_generation import (
    extract_lambda_body_from_file,
    formula_from_compute_source,
    formula_to_latex,
    unknown_formula_names,
)

PARAMS = '''
DAYS_PER_YEAR = 365

YLL = Parameter(
    1.0,
    formula="DEATHS_TOTAL × (REMAINING_LIFE_EXPECTANCY_AT_60 - AGE)",
    compute=lambda ctx: ctx["DEATHS_AVERTED"]
    * (ctx["LIFE_EXPECTANCY_AT_60"] - (ctx["MEAN_AGE"] - 60)),  # years lost
    latex_symbol=r"YLL_{lag}",
)

PER_DAY = Parameter(
    1.0,
    compute=lambda ctx: ctx["COST_TOTAL"] / (ctx["DEATHS_DAILY"] * DAYS_PER_YEAR),
)

CAPPED = Parameter(
    1.0,
    compute=lambda ctx: min(
        1.0,
        ctx["RATE_1"] * 1_000,
    ),
)

HELPER = Parameter(
    1.0,
    compute=lambda ctx: _helper(ctx["RATE_1"]),
)
'''


def test_lambda_body_stops_before_following_arguments(tmp_path: Path) -> None:
    params_file = tmp_path / "parameters.py"
    params_file.write_text(PARAMS, encoding="utf-8")

    body = extract_lambda_body_from_file("YLL", params_file)

    assert body is not None
    assert "latex_symbol" not in body
    assert body.rstrip().endswith('- 60))')


def test_formula_from_compute_source_uses_real_names(tmp_path: Path) -> None:
    params_file = tmp_path / "parameters.py"
    params_file.write_text(PARAMS, encoding="utf-8")

    assert formula_from_compute_source("YLL", params_file) == (
        "DEATHS_AVERTED * (LIFE_EXPECTANCY_AT_60 - (MEAN_AGE - 60))"
    )
    assert formula_from_compute_source("PER_DAY", params_file) == "COST_TOTAL / (DEATHS_DAILY * 365)"
    assert formula_from_compute_source("CAPPED", params_file) == "min( 1.0, RATE_1 * 1000)"
    assert formula_from_compute_source("HELPER", params_file) is None


def test_derived_formula_renders_symbols_only() -> None:
    symbols = {
        "DEATHS_AVERTED": type("S", (), {"latex_symbol": "Deaths_{lag}"})(),
        "LIFE_EXPECTANCY_AT_60": type("S", (), {"latex_symbol": "e_{60}"})(),
        "MEAN_AGE": type("S", (), {"latex_symbol": "Age_{death}"})(),
    }
    formula = "DEATHS_AVERTED * (LIFE_EXPECTANCY_AT_60 - (MEAN_AGE - 60))"

    assert unknown_formula_names(formula, symbols) == []
    assert unknown_formula_names("DEATHS_TOTAL * MEAN_AGE", symbols) == ["DEATHS_TOTAL"]
    assert formula_to_latex(formula, symbols, "YLL_{lag}") == (
        r"YLL_{lag} = Deaths_{lag} \times (e_{60} - (Age_{death} - 60))"
    )


def test_ln_of_fraction_has_single_left_delimiter() -> None:
    symbols = {"SHARE": type("S", (), {"latex_symbol": "r"})()}

    latex = formula_to_latex("ln(0.25 / SHARE)", symbols, "Y")

    assert latex is not None
    assert r"\left\left" not in latex
    assert r"\ln\left(\frac{0.25}{r}\right)" in latex
