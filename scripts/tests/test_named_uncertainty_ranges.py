# -*- coding: utf-8 -*-
import importlib.util
import sys
from pathlib import Path

from dih_models.chart_generators import generate_input_distribution_chart_qmd
from dih_models.parameters import Parameter
from dih_models.parameters_and_calculations_qmd_generator import (
    generate_parameters_and_calculations_qmd,
)
from dih_models.quarto_formatting import generate_uncertainty_section
from dih_models.typescript_generator import generate_typescript_parameters
from dih_models.variables_yml_generator import _format_ci_display


if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore


def _modeled_parameter() -> Parameter:
    return Parameter(
        65_000_000,
        manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
        source_type="definition",
        description="Synthetic cost assumption used to verify named ranges.",
        display_name="Synthetic modeled launch cost",
        unit="USD",
        confidence_interval=(25_000_000, 200_000_000),
        distribution="lognormal",
        interval_label="modeled range",
    )


def test_named_range_is_used_in_variable_display() -> None:
    display = _format_ci_display(
        65_000_000,
        "USD",
        25_000_000,
        200_000_000,
        interval_label="modeled range",
    )

    assert "(modeled range:" in display
    assert "95% CI" not in display


def test_lognormal_range_is_described_as_modeled_bounds() -> None:
    section = "\n".join(generate_uncertainty_section(_modeled_parameter(), "USD"))

    assert "modeled range:" in section
    assert "clips draws to the modeled bounds" in section
    assert "not a statistical confidence interval" in section
    assert "±" not in section


def test_input_distribution_chart_uses_named_range(tmp_path) -> None:
    output = generate_input_distribution_chart_qmd(
        "SYNTHETIC_MODELED_COST",
        {"value": _modeled_parameter()},
        tmp_path,
    ).read_text(encoding="utf-8")

    assert "modeled range low" in output
    assert "modeled range high" in output
    assert "shaded region marks the modeled range" in output


def test_typescript_export_preserves_interval_label(tmp_path) -> None:
    output_path = tmp_path / "parameters.ts"
    generate_typescript_parameters(
        {"SYNTHETIC_MODELED_COST": {"value": _modeled_parameter(), "comment": ""}},
        output_path,
    )
    output = output_path.read_text(encoding="utf-8")

    assert "intervalLabel?: string" in output
    assert 'intervalLabel: "modeled range"' in output


def test_public_export_uses_samples_for_explicitly_named_range() -> None:
    script_path = (
        Path(__file__).resolve().parents[1]
        / "generate-everything-parameters-variables-calculations-references.py"
    )
    spec = importlib.util.spec_from_file_location("generate_everything", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    parameter = Parameter(
        50,
        manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
        source_type="calculated",
        description="Synthetic calculated outcome used to verify public exports.",
        unit="years",
        formula="BASE * 2",
        latex=r"x = 2b",
        inputs=["BASE"],
        compute=lambda context: context["BASE"] * 2,
        interval_label="90% model range",
    )
    entry = module._public_parameter_entry(
        "SYNTHETIC_OUTCOME",
        {"value": parameter, "comment": ""},
        {"SYNTHETIC_OUTCOME": {"value": parameter, "comment": ""}},
        Path("dih_models/parameters.py"),
        {},
        {},
        {"SYNTHETIC_OUTCOME": {"p5": 35, "p95": 75}},
    )

    assert entry is not None
    assert entry["confidenceInterval"] == [35.0, 75.0]
    assert entry["intervalLabel"] == "90% model range"


def test_calculation_appendix_preserves_input_interval_label(tmp_path) -> None:
    modeled_input = _modeled_parameter()
    calculated = Parameter(
        130_000_000,
        manual_ref="knowledge/appendix/state-right-to-trial-impact.qmd",
        source_type="calculated",
        description="Synthetic calculation using the modeled input.",
        unit="USD",
        formula="SYNTHETIC_MODELED_COST * 2",
        latex=r"y = 2x",
        inputs=["SYNTHETIC_MODELED_COST"],
        compute=lambda context: context["SYNTHETIC_MODELED_COST"] * 2,
    )
    output_path = tmp_path / "parameters-and-calculations-test.qmd"
    generate_parameters_and_calculations_qmd(
        {
            "SYNTHETIC_MODELED_COST": {"value": modeled_input, "comment": ""},
            "SYNTHETIC_CALCULATION": {"value": calculated, "comment": ""},
        },
        output_path,
        citation_data={},
    )
    output = output_path.read_text(encoding="utf-8")

    assert "(modeled range:" in output
