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
