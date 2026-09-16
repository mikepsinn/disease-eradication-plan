import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


def load_pre_render_validation_module():
    scripts_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(scripts_dir))
    module_path = scripts_dir / "pre-render-validation.py"
    spec = importlib.util.spec_from_file_location("pre_render_validation", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_manual_cross_reference_target_must_be_renderable(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = load_pre_render_validation_module()
    monkeypatch.chdir(tmp_path)
    source = Path("source.qmd")
    target = Path("orphan.qmd")
    link = "[Orphan](orphan.qmd)"
    source.write_text(link, encoding="utf-8")
    target.write_text("# Orphan", encoding="utf-8")

    module.errors.clear()
    module.check_cross_reference_links(
        link,
        str(source),
        [link],
        {"source.qmd"},
        {"source.qmd"},
        set(),
    )

    assert len(module.errors) == 1
    assert "not rendered by _quarto-manual.yml" in module.errors[0].message

    module.errors.clear()
    module.check_cross_reference_links(
        link,
        str(source),
        [link],
        {"source.qmd", "orphan.qmd"},
        {"source.qmd", "orphan.qmd"},
        set(),
    )

    assert module.errors == []

    module.check_cross_reference_links(
        link,
        str(source),
        [link],
        {"source.qmd"},
        {"source.qmd"},
        {"orphan.qmd"},
    )

    assert module.errors == []


def test_non_manual_source_and_include_directive_do_not_trigger(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = load_pre_render_validation_module()
    monkeypatch.chdir(tmp_path)
    Path("orphan.qmd").write_text("# Orphan", encoding="utf-8")

    module.errors.clear()
    link = "[Orphan](orphan.qmd)"
    module.check_cross_reference_links(
        link,
        "standalone.qmd",
        [link],
        {"manual.qmd"},
        {"manual.qmd"},
        set(),
    )
    include = "{{< include orphan.qmd >}}"
    module.check_cross_reference_links(
        include,
        "manual.qmd",
        [include],
        {"manual.qmd"},
        {"manual.qmd"},
        set(),
    )

    assert module.errors == []


def test_links_inside_manual_include_partials_are_checked(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = load_pre_render_validation_module()
    monkeypatch.chdir(tmp_path)
    Path("manual.qmd").write_text("{{< include partial.qmd >}}", encoding="utf-8")
    link = "[Orphan](orphan.qmd)"
    Path("partial.qmd").write_text(link, encoding="utf-8")
    Path("orphan.qmd").write_text("# Orphan", encoding="utf-8")
    navigation_files = {"manual.qmd"}
    source_files = module.get_qmd_include_closure(navigation_files)

    module.errors.clear()
    module.check_cross_reference_links(
        link,
        "partial.qmd",
        [link],
        source_files,
        navigation_files,
        set(),
    )

    assert source_files == {"manual.qmd", "partial.qmd"}
    assert len(module.errors) == 1
    assert "not rendered by _quarto-manual.yml" in module.errors[0].message


def test_config_helpers_include_index_source_and_cross_site_papers(tmp_path: Path) -> None:
    module = load_pre_render_validation_module()
    manual_config = tmp_path / "_quarto-manual.yml"
    manual_config.write_text(
        """book:
  chapters:
    - knowledge/manual-chapter.qmd
dih-render:
  index-source: index-manual.qmd
""",
        encoding="utf-8",
    )
    paper_config = tmp_path / "_quarto-paper.yml"
    paper_config.write_text(
        """project:
  render:
    - knowledge/paper.qmd
website:
  site-url: https://paper.example
dih-render:
  index-source: knowledge/paper.qmd
""",
        encoding="utf-8",
    )

    manual_files = module.get_qmd_files_for_config(manual_config)
    paper_files = module.get_cross_site_paper_qmd_files(tmp_path)

    assert manual_files == {"index-manual.qmd", "knowledge/manual-chapter.qmd"}
    assert paper_files == {"knowledge/paper.qmd"}


def test_select_qmd_files_filters_global_and_generated_indexes() -> None:
    module = load_pre_render_validation_module()

    selected = module.select_qmd_files(
        [
            "knowledge/chapter.qmd",
            "knowledge/references.qmd",
            "index.qmd",
            "index-manual.qmd",
            "scripts/check.py",
        ]
    )

    assert selected == ["index-manual.qmd", "knowledge/chapter.qmd"]


def test_main_always_runs_generation_before_validation(monkeypatch) -> None:
    module = load_pre_render_validation_module()
    calls = []
    completed = subprocess.CompletedProcess(args=[], returncode=1)
    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda args, **kwargs: calls.append((args, kwargs)) or completed,
    )
    monkeypatch.setattr(sys, "argv", ["pre-render-validation.py"])

    with pytest.raises(SystemExit) as exit_info:
        module.main()

    assert exit_info.value.code == 1
    assert calls == [
        (
            [
                sys.executable,
                "-u",
                "scripts/generate-everything-parameters-variables-calculations-references.py",
            ],
            {"timeout": 1800},
        )
    ]


@pytest.fixture
def manual_url_project(tmp_path: Path):
    """A small manual with the same root, paper, and shortcut routing as production."""
    paper = "knowledge/appendix/algorithmic-public-administration-paper.qmd"
    chapters = ["index.qmd", paper, "knowledge/links.qmd", "knowledge/podcast.qmd", "knowledge/papers.qmd"]
    for source in ["index-manual.qmd", *chapters[1:]]:
        path = tmp_path / source
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\ntitle: Test\n---\n", encoding="utf-8")
    manual = {
        "book": {"site-url": "https://manual.WarOnDisease.org", "chapters": chapters},
        "dih-render": {"index-source": "index-manual.qmd"},
        "project": {"resources": ["assets/"]},
    }
    (tmp_path / "_quarto-manual.yml").write_text(yaml.safe_dump(manual), encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize(
    ("target", "valid"),
    [
        ("https://manual.warondisease.org/knowledge/appendix/algorithmic-public-administration.html", False),
        ("https://manual.warondisease.org/knowledge/appendix/algorithmic-public-administration-paper.html", True),
        ("https://manual.WarOnDisease.org/knowledge/appendix/algorithmic-public-administration-paper?ref=apa#summary", True),
        ("https://manual.warondisease.org/knowledge/appendix/algorithmic-public-administration%2Dpaper.html", True),
        ("https://manual.warondisease.org/knowledge/appendix/knowledge/appendix/algorithmic-public-administration-paper.html", False),
        ("https://manual.warondisease.org/index.html", True),
        ("https://manual.warondisease.org/index-manual.html", False),
        ("https://paper.example/", True),
    ],
)
def test_manual_canonical_url_targets(manual_url_project: Path, target: str, valid: bool) -> None:
    module = load_pre_render_validation_module()
    config = {
        "website": {"site-url": target},
        "dih-render": {"redirect-from": "https://apa.warondisease.org"},
    }
    (manual_url_project / "_quarto-apa.yml").write_text(yaml.safe_dump(config), encoding="utf-8")

    module.check_manual_url_targets(manual_url_project)

    assert bool(module.errors) is not valid
    if not valid:
        assert len(module.errors) == 1
        assert module.errors[0].file == "_quarto-apa.yml"
        assert target in module.errors[0].message


def test_manual_publication_url_must_be_rendered(manual_url_project: Path) -> None:
    module = load_pre_render_validation_module()
    # Merely existing on disk is insufficient if the manual never renders it.
    (manual_url_project / "orphan.qmd").write_text("# Orphan\n", encoding="utf-8")
    config = {"metadata": {"publishing": {"own-site": {"url": "https://manual.warondisease.org/orphan.html"}}}}
    (manual_url_project / "_quarto-apa.yml").write_text(yaml.safe_dump(config), encoding="utf-8")

    module.check_manual_url_targets(manual_url_project)

    assert len(module.errors) == 1
    assert "metadata.publishing.own-site.url" in module.errors[0].context


def test_manual_shortcut_target_must_be_rendered(manual_url_project: Path) -> None:
    module = load_pre_render_validation_module()
    (manual_url_project / "knowledge/papers.qmd").unlink()

    module.check_manual_url_targets(manual_url_project)

    assert len(module.errors) == 1
    assert "papers.warondisease.org" in module.errors[0].context


@pytest.mark.parametrize("target", ["/knowledge/appendix/renamed", "/knowledge/appendix/legacy.html", "/assets/embed"])
def test_manual_aliases_output_names_and_resources(manual_url_project: Path, target: str) -> None:
    module = load_pre_render_validation_module()
    paper = manual_url_project / "knowledge/appendix/algorithmic-public-administration-paper.qmd"
    paper.write_text("---\nformat:\n  html:\n    output-file: renamed.html\naliases:\n  - /knowledge/appendix/legacy.html\n---\n", encoding="utf-8")
    assets = manual_url_project / "assets"
    assets.mkdir()
    (assets / "embed.html").write_text("<h1>Embed</h1>", encoding="utf-8")
    redirects = manual_url_project / "cloudflare/pages/manual/_redirects"
    redirects.parent.mkdir(parents=True)
    redirects.write_text(f"/old {target} 301\n", encoding="utf-8")

    module.check_manual_url_targets(manual_url_project)

    assert module.errors == []


def test_manual_pages_redirect_missing_target(manual_url_project: Path) -> None:
    module = load_pre_render_validation_module()
    redirects = manual_url_project / "cloudflare/pages/manual/_redirects"
    redirects.parent.mkdir(parents=True)
    redirects.write_text("# Legacy routes\n/old /missing 301\n", encoding="utf-8")

    module.check_manual_url_targets(manual_url_project)

    assert len(module.errors) == 1
    assert module.errors[0].file == "cloudflare/pages/manual/_redirects"
    assert module.errors[0].line == 2
