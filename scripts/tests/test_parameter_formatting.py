from dih_models.formatting import format_parameter_value
from dih_models.latex_generation import format_latex_value, round_to_n_sigfigs


def test_probability_values_format_as_one_in_odds() -> None:
    assert format_parameter_value(1 / 60_000_000, "probability") == "1 in 60 million"
    assert format_parameter_value(1.72e-8, "probability") == "1 in 58.1 million"


def test_latex_probability_values_do_not_round_to_zero() -> None:
    assert format_latex_value(1 / 60_000_000, "probability") == r"1\text{ in }60M"
    assert format_latex_value(1.72e-8, "probability") == r"1\text{ in }58.1M"


def test_latex_sigfig_rounding_preserves_tiny_nonzero_values() -> None:
    assert round_to_n_sigfigs(1.72e-8, 3) == r"1.72 \times 10^{-8}"


def test_latex_sigfig_rounding_keeps_plain_thousands() -> None:
    assert round_to_n_sigfigs(1000, 3) == "1000"
