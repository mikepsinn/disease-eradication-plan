import importlib.util
import shutil
from pathlib import Path

import pytest


def load_markdown_twins_module():
    module_path = Path(__file__).resolve().parents[1] / "lib" / "markdown_twins.py"
    spec = importlib.util.spec_from_file_location("markdown_twins", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


QUARTO_PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>The Cost of War</title></head>
<body>
<nav id="quarto-sidebar" class="sidebar"><a href="other.html">Another chapter</a></nav>
<main class="content" id="quarto-document-content">
<div id="calc-loader" style="display: none;">Please wait, this takes like 47 seconds.</div>
<div id="platform-bar" class="platform-bar"><span class="platform-label">Listen</span></div>
<header id="title-block-header" class="quarto-title-block default">
<nav class="quarto-page-breadcrumbs"><a href="problem.html">Failure Analysis</a></nav>
<h1 class="title">The Cost of War</h1>
<div class="keywords"><div class="block-title">Keywords</div><p>war-on-disease</p></div>
</header>
<p>Spending was <a href="appendix/parameters.html#sec-spending" title="Cumulative military spending. Built from SIPRI data.">$170 trillion</a>
and the formula is <span class="math inline">\\(C = M + I\\)</span>.</p>
<p><span class="math display">\\[ E = mc^2 \\]</span></p>
<p>Author <a href="https://orcid.org/0000"><img src="data:image/png;base64,AAAA"></a></p>
<script>var tracking = true;</script>
</main>
</body></html>
"""


def test_main_document_keeps_content_and_drops_page_furniture() -> None:
    module = load_markdown_twins_module()

    document = module._main_document(QUARTO_PAGE.encode("utf-8"))

    assert document is not None
    assert "$170 trillion" in document and "The Cost of War" in document
    for furniture in ("47 seconds", "platform-label", "Failure Analysis", "Keywords", "Another chapter", "tracking"):
        assert furniture not in document
    assert module._main_document(b"<html><head></head><body><p>Not a Quarto page</p></body></html>") is None


def test_alternate_link_is_added_once(tmp_path: Path) -> None:
    module = load_markdown_twins_module()
    page = tmp_path / "cost-of-war.html"
    page.write_text(QUARTO_PAGE, encoding="utf-8")

    module._add_alternate_link(page)
    module._add_alternate_link(page)

    link = '<link rel="alternate" type="text/markdown" href="cost-of-war.llms.md">'
    assert page.read_text(encoding="utf-8").count(link) == 1


def test_llms_txt_links_only_pages_that_have_a_twin(tmp_path: Path) -> None:
    module = load_markdown_twins_module()
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "index.llms.md").write_text("# Home\n", encoding="utf-8")
    (tmp_path / "knowledge" / "war.llms.md").write_text("# War\n", encoding="utf-8")
    (tmp_path / "llms.txt").write_text(
        "- [Home](https://manual.WarOnDisease.org): the book\n"
        "- [War](https://manual.warondisease.org/knowledge/war.html): a chapter\n"
        "- [No twin](https://manual.warondisease.org/knowledge/print.html): a resource\n"
        "- [Paper](https://papers.acceleratedmedicine.org/dfda-impact.html): another site\n",
        encoding="utf-8",
    )

    linked = module._link_llms_txt_to_twins(tmp_path, "https://manual.WarOnDisease.org")

    assert linked == 2
    assert (tmp_path / "llms.txt").read_text(encoding="utf-8") == (
        "- [Home](https://manual.WarOnDisease.org/index.llms.md): the book\n"
        "- [War](https://manual.warondisease.org/knowledge/war.llms.md): a chapter\n"
        "- [No twin](https://manual.warondisease.org/knowledge/print.html): a resource\n"
        "- [Paper](https://papers.acceleratedmedicine.org/dfda-impact.html): another site\n"
    )


@pytest.mark.skipif(shutil.which("quarto") is None, reason="needs Quarto 1.9 or later on PATH")
def test_twin_has_real_math_and_no_tooltips(tmp_path: Path) -> None:
    module = load_markdown_twins_module()
    (tmp_path / "knowledge").mkdir()
    page = tmp_path / "knowledge" / "cost-of-war.html"
    page.write_text(QUARTO_PAGE, encoding="utf-8")
    (tmp_path / "404.html").write_text(QUARTO_PAGE, encoding="utf-8")

    counts = module.write_markdown_twins(tmp_path, site_url="https://manual.warondisease.org")

    assert counts == {"twins": 1, "llms_txt_links": 0}
    assert not (tmp_path / "404.llms.md").exists()
    twin = (tmp_path / "knowledge" / "cost-of-war.llms.md").read_text(encoding="utf-8")
    assert "# The Cost of War" in twin
    assert "[\\$170 trillion](appendix/parameters.llms.md#sec-spending)" in twin
    assert "$C = M + I$" in twin
    assert "$$ E = mc^2 $$" in twin
    assert "SIPRI" not in twin
    assert "data:image" not in twin and "orcid" not in twin
