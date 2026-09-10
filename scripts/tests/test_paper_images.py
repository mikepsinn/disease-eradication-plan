"""Regression coverage for project-hosted images bypassing build validation."""

import importlib.util
import sys
from pathlib import Path

import pytest

from dih_models.papers_qmd_generator import extract_paper_info, generate_papers_qmd


def load_validator(filename: str):
    scripts_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location(filename.replace("-", "_"), scripts_dir / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def image_project(tmp_path: Path, monkeypatch) -> Path:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "_quarto-manual.yml").write_text(
        "book:\n  site-url: https://manual.example.org\n", encoding="utf-8"
    )
    (tmp_path / "knowledge").mkdir()
    return tmp_path


@pytest.mark.parametrize("image_url", [
    "https://manual.example.org/assets/missing.jpg",
    "http://MANUAL.EXAMPLE.ORG/assets/missing.jpg",
    "//manual.example.org/assets/missing.jpg",
    "/assets/missing.jpg",
    "../assets/missing.jpg",
])
def test_missing_project_images_fail_before_and_after_render(image_project: Path, image_url: str) -> None:
    pre = load_validator("pre-render-validation.py")
    markdown = f"[![Paper]({image_url})](https://manual.example.org/knowledge/paper.html)"
    pre.check_image_paths(markdown, "knowledge/papers.qmd", [markdown])
    assert len(pre.errors) == 1
    assert "Image file not found" in pre.errors[0].message

    post = load_validator("post-render-validation.py")
    html = f'<img src="{image_url}">'
    errors = post.check_broken_internal_links(html, image_project / "knowledge/papers.html", image_project)
    assert len(errors) == 1
    assert errors[0].error_type == "BROKEN_IMAGE"


@pytest.mark.parametrize("image_url", [
    "https://manual.example.org/assets/paper%20image.svg?v=2#preview",
    "//manual.example.org/assets/paper%20image.svg?v=2#preview",
    "../assets/paper%20image.svg?v=2#preview",
])
def test_existing_images_with_escaped_names_and_url_suffixes_pass(image_project: Path, image_url: str) -> None:
    assets = image_project / "assets"
    assets.mkdir()
    (assets / "paper image.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
    pre = load_validator("pre-render-validation.py")
    html = f'<img src="{image_url}">'
    pre.check_image_paths(html, "knowledge/papers.qmd", [html])
    assert pre.errors == []

    post = load_validator("post-render-validation.py")
    assert post.check_broken_internal_links(html, image_project / "knowledge/papers.html", image_project) == []


@pytest.mark.parametrize("image_url", [
    "https://external.example.org/assets/missing.jpg",
    "https://manual.example.org.external.example/assets/missing.jpg",
    "//external.example.org/assets/missing.jpg",
    "data:image/png;base64,AAAA",
])
def test_external_and_embedded_images_are_not_treated_as_local(image_project: Path, image_url: str) -> None:
    pre = load_validator("pre-render-validation.py")
    html = f'<img src="{image_url}">'
    pre.check_image_paths(html, "knowledge/papers.qmd", [html])
    assert pre.errors == []

    post = load_validator("post-render-validation.py")
    assert post.check_broken_internal_links(html, image_project / "knowledge/papers.html", image_project) == []


def test_post_render_requires_image_in_output_not_just_source(image_project: Path) -> None:
    (image_project / "assets").mkdir()
    (image_project / "assets/paper.svg").write_text('<svg/>', encoding="utf-8")
    output_dir = image_project / "_site"
    output_dir.mkdir()
    post = load_validator("post-render-validation.py")
    errors = post.check_broken_internal_links(
        '<img src="https://manual.example.org/assets/paper.svg">',
        output_dir / "papers.html",
        output_dir,
    )
    assert len(errors) == 1
    assert errors[0].error_type == "BROKEN_IMAGE"


@pytest.mark.parametrize(("image_url", "expected"), [
    ("https://manual.example.org/assets/paper.jpg", "../assets/paper.jpg"),
    ("https://MANUAL.EXAMPLE.ORG/assets/paper.jpg", "../assets/paper.jpg"),
    ("//manual.example.org/assets/paper.jpg", "../assets/paper.jpg"),
    ("/assets/paper.jpg", "../assets/paper.jpg"),
    ("assets/paper.jpg", "../assets/paper.jpg"),
    ("../assets/paper.jpg", "../assets/paper.jpg"),
    ("https://manual.example.org/assets/paper.svg?v=2#preview", "../assets/paper.svg?v=2#preview"),
    ("https://external.example.org/paper.jpg", "https://external.example.org/paper.jpg"),
])
def test_papers_generator_handles_chapter_site_urls(image_project: Path, image_url: str, expected: str) -> None:
    config_path = image_project / "_quarto-paper.yml"
    config_path.write_text(
        "website:\n  title: Paper\n"
        "  site-url: https://manual.example.org/knowledge/paper.html\n"
        f"metadata:\n  image: {image_url}\n",
        encoding="utf-8",
    )
    paper = extract_paper_info(config_path, "paper")
    assert paper is not None
    assert paper["og_image"] == expected


@pytest.mark.parametrize("image_field", ["", "  image: null\n", "  image: ''\n", "  image: '   '\n"])
def test_papers_index_rejects_entries_with_no_image(image_project: Path, image_field: str) -> None:
    (image_project / "_variables.yml").write_text("{}\n", encoding="utf-8")
    (image_project / "_quarto-imageless-paper.yml").write_text(
        "website:\n  title: Paper without an image\n"
        "  site-url: https://manual.example.org/knowledge/paper.html\n"
        "metadata:\n  importance: 1\n" + image_field,
        encoding="utf-8",
    )
    output = image_project / "knowledge/papers.qmd"
    output.write_text("Existing index\n", encoding="utf-8")

    with pytest.raises(ValueError, match=r"missing metadata.image.*imageless-paper"):
        generate_papers_qmd(image_project)

    assert output.read_text(encoding="utf-8") == "Existing index\n"
