import importlib.util
import sys
from pathlib import Path

import pytest

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore


def load_render_quarto_module():
    module_path = Path(__file__).resolve().parents[1] / "render-quarto.py"
    spec = importlib.util.spec_from_file_location("render_quarto", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_papers_site(root: Path, render: str = "    - index.qmd\n    - alpha.qmd\n    - beta.qmd\n") -> None:
    """A two-paper site whose papers are owned by their own per-paper configs."""
    appendix = root / "knowledge" / "appendix"
    appendix.mkdir(parents=True)
    (root / "_quarto-site.yml").write_text(
        "project:\n  type: website\n  render:\n" + render +
        "dih-render:\n"
        "  index-page: index-site.qmd\n"
        "  papers:\n"
        "    - slug: alpha\n      config: alpha-paper\n"
        "    - slug: beta\n      config: beta-paper\n"
        "website:\n  title: Site\n  site-url: https://papers.example.org\n"
        "format:\n  html: {}\n",
        encoding="utf-8",
    )
    (root / "_quarto-alpha-paper.yml").write_text(
        "dih-render:\n  index-source: knowledge/appendix/alpha-paper.qmd\n  pdf-output-file: alpha.pdf\n"
        "metadata:\n  doi: 10.1234/alpha\n  keywords:\n    - trials\n",
        encoding="utf-8",
    )
    (root / "_quarto-beta-paper.yml").write_text(
        "dih-render:\n  index-source: knowledge/appendix/beta-paper.qmd\n",
        encoding="utf-8",
    )
    (root / "index-site.qmd").write_text("---\ntitle: Papers\n---\n", encoding="utf-8")
    (appendix / "alpha-paper.qmd").write_text(
        "---\ntitle: Alpha\n---\n\n"
        "See [Beta](beta-paper.qmd#method) and ![chart](../figures/chart.png).\n",
        encoding="utf-8",
    )
    (appendix / "beta-paper.qmd").write_text(
        "---\ntitle: Beta\ndoi: 10.9999/already-set\n---\n\nBody.\n",
        encoding="utf-8",
    )


def test_papers_site_reads_each_paper_from_its_own_config(tmp_path: Path, monkeypatch) -> None:
    module = load_render_quarto_module()
    write_papers_site(tmp_path)
    monkeypatch.setattr(module, "_find_project_root", lambda: tmp_path)

    metadata = module.get_config_metadata("site")

    assert metadata["index_source"] is None
    assert metadata["index_page"] == "index-site.qmd"
    assert [(p["slug"], p["source"], p["pdf_output_file"], p["doi"]) for p in metadata["papers"]] == [
        ("alpha", "knowledge/appendix/alpha-paper.qmd", "alpha.pdf", "10.1234/alpha"),
        ("beta", "knowledge/appendix/beta-paper.qmd", None, None),
    ]


def test_publication_image_overrides_source_only_in_generated_pages(tmp_path: Path, monkeypatch) -> None:
    module = load_render_quarto_module()
    write_papers_site(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "_find_project_root", lambda: tmp_path)
    config = tmp_path / "_quarto-alpha-paper.yml"
    config.write_text(config.read_text() + "  image: https://example.org/new.jpg\n", encoding="utf-8")
    source = tmp_path / "knowledge/appendix/alpha-paper.qmd"
    original = source.read_text().replace("title: Alpha", "title: Alpha\nimage: old.jpg")
    source.write_text(original, encoding="utf-8")

    assert module.prepare_config("site", verbose=False)
    assert "image: https://example.org/new.jpg" in (tmp_path / "alpha.qmd").read_text()
    assert source.read_text() == original
    assert module.prepare_config("alpha-paper", verbose=False)
    assert "image: https://example.org/new.jpg" in (tmp_path / "index.qmd").read_text()


@pytest.mark.parametrize("image_field", ["image: old.jpg\n", "image: >\n  old.jpg\n", ""])
def test_image_override_preserves_other_frontmatter_and_body(image_field: str) -> None:
    module = load_render_quarto_module()
    content = "---\ntitle: Original\n" + image_field + "description: Preserved\n---\n\nBody.\n"
    result = module._set_frontmatter_image(content, "https://example.org/new.jpg")
    assert module.yaml.safe_load(result.split("---")[1]) == {
        "title": "Original", "description": "Preserved", "image": "https://example.org/new.jpg"
    }
    assert result.endswith("---\n\nBody.\n")


def test_papers_are_copied_to_root_pages_with_paths_and_citation_fields_fixed(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_render_quarto_module()
    write_papers_site(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "_find_project_root", lambda: tmp_path)

    assert module.prepare_config("site", verbose=False)

    assert (tmp_path / "index.qmd").read_text(encoding="utf-8") == "---\ntitle: Papers\n---\n"
    alpha = (tmp_path / "alpha.qmd").read_text(encoding="utf-8")
    # Moved from knowledge/appendix/ to the root: parent-relative and
    # same-directory paths must still resolve.
    assert "![chart](knowledge/figures/chart.png)" in alpha
    assert "[Beta](knowledge/appendix/beta-paper.qmd#method)" in alpha
    assert "doi: 10.1234/alpha" in alpha
    assert "keywords:\n- trials" in alpha
    # A paper that sets its own DOI keeps it.
    beta = (tmp_path / "beta.qmd").read_text(encoding="utf-8")
    assert beta.count("doi:") == 1
    assert "doi: 10.9999/already-set" in beta


def test_links_between_papers_on_the_same_site_stay_internal(tmp_path: Path, monkeypatch) -> None:
    module = load_render_quarto_module()
    write_papers_site(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "_find_project_root", lambda: tmp_path)
    assert module.prepare_config("site", verbose=False)

    rewritten = module._rewrite_index_source_links(
        build_temp=tmp_path,
        source_targets={
            "knowledge/appendix/alpha-paper.qmd": "alpha.qmd",
            "knowledge/appendix/beta-paper.qmd": "beta.qmd",
        },
        files_to_process=["alpha.qmd"],
        verbose=False,
    )

    assert rewritten == 1
    assert "[Beta](/beta.qmd#method)" in (tmp_path / "alpha.qmd").read_text(encoding="utf-8")


def test_paper_missing_from_render_list_fails_loudly(tmp_path: Path, monkeypatch) -> None:
    module = load_render_quarto_module()
    write_papers_site(tmp_path, render="    - index.qmd\n    - alpha.qmd\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "_find_project_root", lambda: tmp_path)

    with pytest.raises(ValueError, match="beta.qmd is not in project.render"):
        module.prepare_config("site", verbose=False)


def test_variables_used_by_root_paper_pages_are_collected(tmp_path: Path) -> None:
    module = load_render_quarto_module()
    write_papers_site(tmp_path)
    (tmp_path / "knowledge" / "appendix" / "beta-paper.qmd").write_text(
        "---\ntitle: Beta\n---\n\n{{< var trial_cost >}}\n", encoding="utf-8"
    )
    (tmp_path / "_variables.yml").write_text('trial_cost: "$929"\n', encoding="utf-8")

    assert "trial_cost" in module._collect_config_variable_names(tmp_path, "site")
