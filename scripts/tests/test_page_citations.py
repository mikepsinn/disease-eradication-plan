import importlib.util
from pathlib import Path

import pytest
import yaml


def load_page_citations_module():
    module_path = Path(__file__).resolve().parents[1] / "lib" / "page_citations.py"
    spec = importlib.util.spec_from_file_location("page_citations", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_variables(build_dir: Path, variables: dict) -> None:
    (build_dir / "_variables.yml").write_text(yaml.safe_dump(variables), encoding="utf-8")


def test_each_page_cites_only_the_sources_of_its_own_parameters(tmp_path: Path) -> None:
    module = load_page_citations_module()
    write_variables(
        tmp_path,
        {
            "deaths": "55 million",
            "deaths_cite": "@who-2024",
            "spending": "$2.7T",
            "spending_nounit": "2.7T",
            "spending_cite": "@sipri-2024",
            "lobbying": "$4B",
            "lobbying_cite": "@opensecrets-2024",
            "ratio": "12x",
        },
    )
    (tmp_path / "war.qmd").write_text(
        "---\ntitle: War\n---\n\n{{< var deaths >}} died. {{< include parts/money.qmd >}}\n",
        encoding="utf-8",
    )
    (tmp_path / "parts").mkdir()
    (tmp_path / "parts" / "money.qmd").write_text("It cost {{< var spending_nounit >}}.\n", encoding="utf-8")
    (tmp_path / "lobby.qmd").write_text(
        "Lobbyists spend {{< var lobbying >}} {{< var lobbying_cite >}}/year.\n", encoding="utf-8"
    )
    (tmp_path / "plain.qmd").write_text("---\ntitle: Plain\n---\n\n{{< var ratio >}}\n", encoding="utf-8")

    stats = module.scope_variable_citations(tmp_path, ["war.qmd", "lobby.qmd", "plain.qmd"])

    assert stats == {"pages_with_nocite": 2, "inlined_shortcodes": 1, "removed_variables": 3}
    war = (tmp_path / "war.qmd").read_text(encoding="utf-8")
    assert war.startswith("---\ntitle: War\nnocite: '@sipri-2024, @who-2024'\n---\n")
    # Braces end the key: a bare "@opensecrets-2024/year" is the key "opensecrets-2024/year".
    lobby = (tmp_path / "lobby.qmd").read_text(encoding="utf-8")
    assert lobby == "---\nnocite: '@opensecrets-2024'\n---\n\nLobbyists spend {{< var lobbying >}} @{opensecrets-2024}/year.\n"
    assert (tmp_path / "plain.qmd").read_text(encoding="utf-8") == "---\ntitle: Plain\n---\n\n{{< var ratio >}}\n"
    # The included file is not a page: it needs no frontmatter of its own.
    assert (tmp_path / "parts" / "money.qmd").read_text(encoding="utf-8") == "It cost {{< var spending_nounit >}}.\n"

    variables = yaml.safe_load((tmp_path / "_variables.yml").read_text(encoding="utf-8"))
    assert variables == {"deaths": "55 million", "spending": "$2.7T", "spending_nounit": "2.7T", "lobbying": "$4B", "ratio": "12x"}


def test_a_hand_written_nocite_fails_loudly(tmp_path: Path) -> None:
    module = load_page_citations_module()
    write_variables(tmp_path, {"deaths": "55 million", "deaths_cite": "@who-2024"})
    (tmp_path / "page.qmd").write_text("---\nnocite: '@other'\n---\n\n{{< var deaths >}}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="page.qmd sets nocite"):
        module.scope_variable_citations(tmp_path, ["page.qmd"])


PAPER_WITH_REFS = """# A Paper

Text [@a].

## Acknowledgments {.unnumbered}

Thanks.

## References {.unnumbered}

::: {#refs}
:::

## Appendix A {.appendix}

More text.
"""


def test_only_the_references_page_keeps_a_refs_block(tmp_path: Path) -> None:
    module = load_page_citations_module()
    (tmp_path / "paper.qmd").write_text(PAPER_WITH_REFS, encoding="utf-8")
    (tmp_path / "chapter.qmd").write_text("# Chapter\n\nText [@b].\n", encoding="utf-8")
    references = "---\ntitle: References\n---\n\n::: {#refs}\n:::\n"
    (tmp_path / "references.qmd").write_text(references, encoding="utf-8")

    stripped = module.keep_one_bibliography_page(
        tmp_path, ["paper.qmd", "chapter.qmd", "references.qmd"], "references.qmd"
    )

    assert stripped == ["paper.qmd"]
    assert (tmp_path / "paper.qmd").read_text(encoding="utf-8") == (
        "# A Paper\n\nText [@a].\n\n## Acknowledgments {.unnumbered}\n\nThanks.\n\n"
        "## Appendix A {.appendix}\n\nMore text.\n"
    )
    assert (tmp_path / "references.qmd").read_text(encoding="utf-8") == references


def test_the_references_page_must_have_a_refs_block(tmp_path: Path) -> None:
    module = load_page_citations_module()
    (tmp_path / "references.qmd").write_text("# References\n", encoding="utf-8")

    with pytest.raises(ValueError, match="has no ::: \\{#refs\\} block"):
        module.keep_one_bibliography_page(tmp_path, ["references.qmd"], "references.qmd")


def test_a_refs_block_the_build_cannot_remove_fails_loudly(tmp_path: Path) -> None:
    module = load_page_citations_module()
    (tmp_path / "references.qmd").write_text("::: {#refs}\n:::\n", encoding="utf-8")
    (tmp_path / "paper.qmd").write_text("::: {#refs}\nA note inside the block.\n:::\n", encoding="utf-8")

    with pytest.raises(ValueError, match="paper.qmd still has a ::: \\{#refs\\} line"):
        module.keep_one_bibliography_page(tmp_path, ["paper.qmd", "references.qmd"], "references.qmd")
