import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


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
