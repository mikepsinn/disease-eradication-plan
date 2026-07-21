from pathlib import Path

from dih_models.reference_parser import parse_references_bib
from dih_models.typescript_generator import _convert_to_csl_json


def test_csl_conversion_splits_bibtex_author_lists() -> None:
    citation = _convert_to_csl_json(
        "paper",
        {
            "author": "Cassidy, Emily S. and West, Paul C.",
            "title": "Paper",
            "type": "article",
        },
    )

    assert citation is not None
    assert citation["author"] == [
        {"family": "Cassidy", "given": "Emily S."},
        {"family": "West", "given": "Paul C."},
    ]


def test_csl_conversion_preserves_braced_corporate_authors(tmp_path: Path) -> None:
    bib_path = tmp_path / "references.bib"
    bib_path.write_text(
        """@misc{org,
  title = {Report},
  author = {{University of Oxford, LEAP}},
}
""",
        encoding="utf-8",
    )

    reference = parse_references_bib(bib_path)["org"]
    citation = _convert_to_csl_json("org", reference)

    assert citation is not None
    assert citation["author"] == [{"literal": "University of Oxford, LEAP"}]
