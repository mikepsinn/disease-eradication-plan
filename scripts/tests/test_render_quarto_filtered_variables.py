import importlib.util
import sys
from pathlib import Path
from urllib.robotparser import RobotFileParser

import pytest

from dih_models.llms_txt_generator import generate_robots_txt

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


@pytest.mark.parametrize("site_url, sitemap_url", [
    ("https://manual.WarOnDisease.org", "https://manual.warondisease.org/sitemap.xml"),
    ("https://standalone.example.org/", "https://standalone.example.org/sitemap.xml"),
    ("https://manual.warondisease.org/knowledge/paper.html", "https://manual.warondisease.org/sitemap.xml"),
])
def test_build_preserves_declared_root_resources(tmp_path: Path, monkeypatch, site_url: str, sitemap_url: str) -> None:
    module = load_render_quarto_module()
    monkeypatch.chdir(tmp_path)
    # Resolve from the active directory just as the real build does when it
    # switches from the checkout into _build_temp/manual.
    monkeypatch.setattr(module, "_find_project_root", Path.cwd)
    (tmp_path / "_quarto-manual.yml").write_text(
        """project:
  type: book
  output-dir: _site
  resources:
    - robots.txt
    - llms.txt
    - _redirects
    - manifest.webmanifest
dih-render:
  index-source: index-manual.qmd
book:
  title: Resource check
  site-url: SITE_URL
  chapters:
    - index.qmd
format:
  html: {}
""".replace("SITE_URL", site_url), encoding="utf-8",
    )
    (tmp_path / "index-manual.qmd").write_text("# Resource check\n", encoding="utf-8")
    (tmp_path / "_variables-manual.yml").write_text("{}\n", encoding="utf-8")
    # The checkout starts with the manual's shared robots.txt even when the
    # target build will be served from a standalone paper host.
    generate_robots_txt(tmp_path, site_url="https://manual.warondisease.org")
    resources = {
        "llms.txt": "# Manual\n\n[Home](https://manual.warondisease.org/)\n",
        "_redirects": "/old /new 301\n",
        "manifest.webmanifest": '{"name": "Manual"}\n',
    }
    for name, content in resources.items():
        (tmp_path / name).write_text(content, encoding="utf-8")

    build_dir = module.prepare_build_temp("manual", verbose=False)

    assert build_dir is not None
    for name, content in resources.items():
        assert (build_dir / name).read_text(encoding="utf-8") == content
    robots = (build_dir / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *\nAllow: /" in robots
    parser = RobotFileParser()
    parser.parse(robots.splitlines())
    assert parser.can_fetch("ExampleBot", site_url)
    assert parser.site_maps() == [sitemap_url]
