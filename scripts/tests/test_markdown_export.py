from pathlib import Path

from dih_models.markdown_export import load_markdown_variables


def test_markdown_variables_prefer_manual_chapter_links(tmp_path: Path) -> None:
    variables_yml = tmp_path / "_variables.yml"
    variables_yml.write_text(
        "\n".join(
            [
                'global_cybercrime_cagr: \'<a href="/knowledge/appendix/parameters-and-calculations.html#sec-global_cybercrime_cagr" class="parameter-link">15%</a>\'',
                'global_cybercrime_cagr_nounit: \'<span class="parameter-definition">15</span>\'',
            ]
        ),
        encoding="utf-8",
    )

    chapter_mapping = {
        "GLOBAL_CYBERCRIME_CAGR": [
            {
                "url": "https://manual.warondisease.org/knowledge/economics/gdp-trajectories.html",
            }
        ],
    }

    variables = load_markdown_variables(variables_yml, chapter_mapping=chapter_mapping)

    assert (
        variables["global_cybercrime_cagr"]
        == "[15%](https://manual.warondisease.org/knowledge/economics/gdp-trajectories.html)"
    )
    assert (
        variables["global_cybercrime_cagr_nounit"]
        == "[15](https://manual.warondisease.org/knowledge/economics/gdp-trajectories.html)"
    )
