from pathlib import Path

from dih_models.latex_generation import (
    extract_lambda_body_from_file,
    formula_equation,
    formula_from_compute_source,
    formula_to_latex,
    generate_auto_latex,
    infer_operation_from_compute,
    unit_constant_symbol,
)
from dih_models.latex_width import latex_display_lines, latex_line_width_pt

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
    assert formula_from_compute_source("PER_DAY", params_file) == "COST_TOTAL / (DEATHS_DAILY * DAYS_PER_YEAR)"
    assert formula_from_compute_source("CAPPED", params_file) == "min( 1.0, RATE_1 * 1000)"
    assert formula_from_compute_source("HELPER", params_file) is None


def test_derived_formula_renders_symbols_only() -> None:
    symbols = {
        "DEATHS_AVERTED": type("S", (), {"latex_symbol": "Deaths_{lag}"})(),
        "LIFE_EXPECTANCY_AT_60": type("S", (), {"latex_symbol": "e_{60}"})(),
        "MEAN_AGE": type("S", (), {"latex_symbol": "Age_{death}"})(),
    }
    formula = "DEATHS_AVERTED * (LIFE_EXPECTANCY_AT_60 - (MEAN_AGE - 60))"

    assert formula_to_latex(formula, symbols, "YLL_{lag}") == (
        r"YLL_{lag} = Deaths_{lag} \times (e_{60} - (Age_{death} - 60))"
    )


def test_ln_of_fraction_has_single_left_delimiter() -> None:
    symbols = {"SHARE": type("S", (), {"latex_symbol": "r"})()}

    latex = formula_to_latex("ln(0.25 / SHARE)", symbols, "Y")

    assert latex is not None
    assert r"\left\left" not in latex
    assert r"\ln\left(\frac{0.25}{r}\right)" in latex


def test_nested_functions_render_upright() -> None:
    symbols = {"K": type("S", (), {"latex_symbol": "k"})(), "S": type("S", (), {"latex_symbol": "s"})()}

    latex = formula_to_latex("min(1.0, (3 × min(K × min(0.02, S) ÷ 0.01, 5)) ÷ 36)", symbols, "f")

    assert latex == r"f = \min\left(1, \frac{3 \times \min\left(\frac{k \times \min\left(0.02, s\right)}{0.01}, 5\right)}{36}\right)"


def test_parenthesised_numerator_becomes_fraction() -> None:
    symbols = {name: type("S", (), {"latex_symbol": sym})() for name, sym in
               (("A_X", "a"), ("B_X", "b"), ("POP_X", "N"))}

    assert formula_to_latex("(A_X + B_X) / POP_X", symbols, "y") == r"y = \frac{a + b}{N}"


def test_unit_constant_gets_a_label() -> None:
    assert unit_constant_symbol("MONTHS_PER_YEAR", 12) == r"\underbrace{12}_{\text{months/yr}}"
    assert unit_constant_symbol("HOURS_PER_YEAR", 8760) == r"\underbrace{8760}_{\text{hours/yr}}"
    assert unit_constant_symbol("COST_TOTAL", 5) is None


def _built(*args) -> tuple[str, bool]:
    built = formula_equation(*args)
    assert built is not None
    return built


def test_formula_equation_adds_numbers_only_when_they_reproduce_the_value() -> None:
    symbols = {"COST_X": "C", "MONTHS_PER_YEAR": r"\underbrace{12}_{\text{months/yr}}"}
    numbers = {"COST_X": r"\$5", "MONTHS_PER_YEAR": "12"}
    values = {"COST_X": 5.0, "MONTHS_PER_YEAR": 12.0}

    latex, verified = _built("COST_X × MONTHS_PER_YEAR", "Y", symbols, numbers, values, 60.0, r"\$60")
    assert verified
    assert latex == r"Y = C \times \underbrace{12}_{\text{months/yr}} = \$5 \times 12 = \$60"

    latex, verified = _built("COST_X × MONTHS_PER_YEAR", "Y", symbols, numbers, values, 61.0, r"\$61")
    assert not verified
    assert latex == r"Y = C \times \underbrace{12}_{\text{months/yr}}"

    assert formula_equation("COST_X × 20 YEARS", "Y", symbols, numbers, values, 100.0, "100") is None
    assert formula_equation("COST_X × UNKNOWN_NAME", "Y", symbols, numbers, values, 100.0, "100") is None


def test_negative_numbers_are_parenthesised() -> None:
    latex, verified = _built(
        "A_X × B_X - B_X", "Y", {"A_X": "a", "B_X": "b"}, {"A_X": "2", "B_X": "-3"},
        {"A_X": 2.0, "B_X": -3.0}, -3.0, "-3")
    assert verified
    assert latex == r"Y = a \times b - b = 2 \times (-3) - (-3) = -3"


def test_round_renders_as_operator() -> None:
    latex, verified = _built(
        "BASE_X + round(ln(0.25 / SHARE_X) / ln(1 + RATE_X))", "Y",
        {"BASE_X": "Y_0", "SHARE_X": "s", "RATE_X": "g"}, {"BASE_X": "2025", "SHARE_X": "5\\%", "RATE_X": "10\\%"},
        {"BASE_X": 2025.0, "SHARE_X": 0.05, "RATE_X": 0.10}, 2042.0, "2042")
    assert verified
    assert latex.startswith(r"Y = Y_0 + \operatorname{round}\left(\frac{\ln\left(\frac{0.25}{s}\right)}{\ln\left(1 + g\right)}\right)")


def test_line_width_measure_flags_wide_lines() -> None:
    value = "$$\n\\begin{gathered}\nX \\\\\n= " + " + ".join(f"Cost_{{item{i}}}" for i in range(30)) + "\n\\end{gathered}\n$$"
    lines = latex_display_lines(value)

    assert lines[0] == "X"
    narrow, wide = latex_line_width_pt(lines[0]), latex_line_width_pt(lines[1])
    assert narrow is not None and narrow < 20
    assert wide is not None and wide > 1000
    assert latex_line_width_pt(r"a \times \underbrace{12}_{\text{months/yr}}") is not None


class _Param(float):
    """Float carrying Parameter-style attributes, enough for generate_auto_latex."""

    def __new__(cls, value: float, **attrs: object) -> "_Param":
        obj = float.__new__(cls, value)
        obj.__dict__.update(attrs)
        return obj


def test_capped_ratio_keeps_its_cap() -> None:
    # Probing min(1, A / B) with small test values looks like plain A / B
    parameters = {
        "A_X": {"value": _Param(3.0, unit="years", latex_symbol="a")},
        "B_X": {"value": _Param(2.0, unit="years", latex_symbol="b")},
    }
    capped = _Param(1.0, unit="rate", latex_symbol="f", inputs=["A_X", "B_X"], formula="min(1.0, A_X / B_X)",
                    compute=lambda ctx: min(1.0, ctx["A_X"] / ctx["B_X"]))

    latex = generate_auto_latex("CAPPED_X", capped, parameters)

    assert latex == r"f = \min\left(1, \frac{a}{b}\right) = \min\left(1, \frac{3}{2}\right) = 100\%"


def test_nonlinear_single_input_is_not_a_constant_division() -> None:
    # ((1+r)^80 - 1) / r probes to two tiny "constants" (2.7e-38, 1.4e-61) that once matched
    factor = _Param(136_000.0, unit="x", inputs=["R_X"], compute=lambda ctx: ((1 + ctx["R_X"]) ** 80 - 1) / ctx["R_X"])
    assert infer_operation_from_compute(factor, ["R_X"])[0] == "transform"

    tripled = _Param(6.0, unit="x", inputs=["R_X"], compute=lambda ctx: ctx["R_X"] * 3)
    assert infer_operation_from_compute(tripled, ["R_X"]) == ("multiply_constant", 3.0)
