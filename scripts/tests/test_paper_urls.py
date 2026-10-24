"""Publication links must distinguish chapter URLs from standalone site roots."""

from pathlib import Path

import pytest
import yaml

from dih_models.llms_txt_generator import extract_site_info
from dih_models.papers_qmd_generator import extract_paper_info
from dih_models.parameters_and_calculations_qmd_generator import generate_parameters_and_calculations_qmd
from dih_models.site_metadata_generator import extract_site_metadata


@pytest.mark.parametrize("site_url, expected_pdf", [
    ("https://manual.warondisease.org/knowledge/appendix/paper.html", None),
    ("https://manual.warondisease.org/knowledge/appendix/paper.html?source=apa", None),
    ("https://paper.example.org", "https://paper.example.org/paper.pdf"),
    ("https://paper.example.org/", "https://paper.example.org/paper.pdf"),
])
def test_publication_pdf_urls(tmp_path: Path, site_url: str, expected_pdf: str | None) -> None:
    config = {
        "website": {"title": "Example paper", "site-url": site_url},
        "project": {"type": "website"},
        "metadata": {"doi": "10.1234/example"},
        "format": {"pdf": {"output-file": "paper.pdf"}},
    }
    path = tmp_path / "_quarto-paper.yml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    paper = extract_paper_info(path, "paper")
    llms = extract_site_info(path, "paper")
    metadata = extract_site_metadata(path, "paper")

    assert paper is not None and llms is not None and metadata is not None
    assert paper["pdf_url"] == llms["pdf_url"] == metadata.get("pdfUrl") == expected_pdf
    assert paper["doi_url"] == "https://doi.org/10.1234/example"


@pytest.mark.parametrize("site_url", [
    "https://manual.warondisease.org/knowledge/appendix/paper.html",
    "https://manual.warondisease.org/",
])
def test_appendix_url_is_rooted_at_site(tmp_path: Path, site_url: str) -> None:
    output = tmp_path / "appendix.qmd"

    generate_parameters_and_calculations_qmd({}, output, site_url=site_url)

    content = output.read_text(encoding="utf-8")
    assert "https://manual.warondisease.org/knowledge/appendix/parameters-and-calculations.html" in content
    assert ".html/knowledge" not in content
