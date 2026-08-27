import importlib.util
import sys
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore


def load_render_quarto_module():
    module_path = Path(__file__).resolve().parents[1] / "render-quarto.py"
    spec = importlib.util.spec_from_file_location("render_quarto", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_collect_config_variables_uses_actual_index_and_filtered_appendix(
    tmp_path: Path,
) -> None:
    module = load_render_quarto_module()
    appendix_dir = tmp_path / "knowledge" / "appendix"
    appendix_dir.mkdir(parents=True)

    (tmp_path / "_quarto-sample.yml").write_text(
        """dih-render:
  index-source: paper.qmd
book:
  chapters:
    - index.qmd
    - knowledge/appendix/parameters-and-calculations.qmd
""",
        encoding="utf-8",
    )
    (tmp_path / "paper.qmd").write_text(
        "{{< var paper_value >}}\n{{< include included.qmd >}}\n",
        encoding="utf-8",
    )
    (tmp_path / "included.qmd").write_text(
        "{{< var included_value >}}\n",
        encoding="utf-8",
    )
    (appendix_dir / "parameters-and-calculations.qmd").write_text(
        "{{< var unfiltered_appendix_value >}}\n",
        encoding="utf-8",
    )
    (appendix_dir / "parameters-and-calculations-sample.qmd").write_text(
        "{{< var filtered_appendix_value >}}\n",
        encoding="utf-8",
    )

    variables = module._collect_config_variable_names(tmp_path, "sample")

    assert variables == {
        "filtered_appendix_value",
        "included_value",
        "paper_value",
    }


def test_standalone_website_pdf_renders_only_the_paper() -> None:
    module = load_render_quarto_module()

    command = module._build_quarto_render_command(
        format_override="pdf",
        quarto_args=None,
        project_type="website",
        index_source="knowledge/appendix/paper.qmd",
    )

    assert command == ["quarto", "render", "index.qmd", "--to", "pdf"]


def test_html_and_book_renders_remain_project_wide() -> None:
    module = load_render_quarto_module()

    assert module._build_quarto_render_command(
        format_override="html",
        quarto_args=["--quiet"],
        project_type="website",
        index_source="knowledge/appendix/paper.qmd",
    ) == ["quarto", "render", "--to", "html", "--quiet"]
    assert module._build_quarto_render_command(
        format_override="pdf",
        quarto_args=None,
        project_type="book",
        index_source="index-manual.qmd",
    ) == ["quarto", "render", "--to", "pdf"]


def test_strip_confidence_intervals_handles_custom_model_range_labels(
    tmp_path: Path,
) -> None:
    module = load_render_quarto_module()
    variables_path = tmp_path / "_variables.yml"
    variables_path.write_text(
        'default: "10 (95% CI: 8-12) | 95% CI: [8, 12]"\n'
        'modeled: "10 (modeled range: 4-20) | modeled range: [4, 20]"\n'
        'propagated: "10 (90% model range: 5-18) | 90% model range: [5, 18]"\n',
        encoding="utf-8",
    )

    stripped = module._strip_confidence_intervals(variables_path, verbose=False)
    result = variables_path.read_text(encoding="utf-8")

    assert stripped == 6
    assert "95% CI" not in result
    assert "modeled range" not in result
    assert "90% model range" not in result
