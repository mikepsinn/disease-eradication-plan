#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give each page of an HTML build the reference list of its own citations.

Quarto hands _variables.yml to citeproc as metadata on every page, so each
"@key" in a *_cite variable lands in the reference list of every page. The
manual's chapters each listed about 134 sources they never cite. Quarto hides
those lists from readers, but AI tools read the hidden HTML, so the lists were
about half of all text on the site and pushed pages past fetch-size limits.

A book has a second problem: Quarto puts the whole book's bibliography on the
first page in render order that has a ::: {#refs} block. Five appendix papers
have one for their PDFs, so the bibliography went to the IAB paper, the
References page stayed empty, and every citation link pointed at the paper.

Both functions edit only the build copy in _build_temp.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List

import yaml

from dih_models.paper_bibliography_generator import extract_variables_from_qmd
from dih_models.variable_naming import CITE_VARIABLE_SUFFIX, strip_generated_variable_suffix
from dih_models.yaml_utils import yaml_safe_load

_yaml_dumper = getattr(yaml, "CSafeDumper", yaml.SafeDumper)

_RE_CITE_SHORTCODE = re.compile(r"\{\{<\s*var\s+([^\s>]+" + CITE_VARIABLE_SUFFIX + r")\s*>\}\}")
_RE_FRONTMATTER = re.compile(r"---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
# Quarto's own test for a page that holds the bibliography (containsRefs).
_RE_QUARTO_REFS_LINE = re.compile(r"^:::\s*\{#refs([\s}]|.*?\})\s*$", re.MULTILINE)
# A ::: {#refs} block with its "References" heading, if the heading comes just before it.
_RE_REFS_BLOCK = re.compile(
    r"(?:^#{1,6}[ \t]+References\b[^\n]*\n(?:[ \t]*\n)*)?^:::\s*\{#refs[^\n]*\n:::[ \t]*(?:\n|$)(?:[ \t]*\n)*",
    re.MULTILINE,
)


def _add_nocite(content: str, keys: List[str], page: str) -> str:
    """Add a nocite field that lists keys to the page frontmatter."""
    field = yaml.safe_dump({"nocite": ", ".join(f"@{key}" for key in keys)}, allow_unicode=True, width=1_000_000)
    match = _RE_FRONTMATTER.match(content)
    if match is None:
        return f"---\n{field}---\n\n{content}"
    if re.search(r"^nocite:", match.group(1), flags=re.MULTILINE):
        raise ValueError(
            f"{page} sets nocite, but the build writes each page's nocite from the "
            "parameters it uses. Cite the source in the text instead."
        )
    return content[: match.end(1)] + "\n" + field.rstrip("\n") + content[match.end(1):]


def scope_variable_citations(build_dir: Path, page_paths: Iterable[str]) -> Dict[str, int]:
    """Cite parameter sources only on the pages that show those parameters.

    1. Each page gets a nocite for the *_cite sources of the variables it uses
       (includes too), so its reference list keeps the sources of its numbers.
    2. Explicit {{< var name_cite >}} shortcodes become the literal citation,
       @{key}. The braces end the key: pandoc reads "@key/year" as the key
       "key/year".
    3. The *_cite entries leave _variables.yml, so no page cites them all.
    """
    variables_path = build_dir / "_variables.yml"
    variables = yaml_safe_load(variables_path.read_text(encoding="utf-8")) or {}
    cites = {name: str(value) for name, value in variables.items() if name.endswith(CITE_VARIABLE_SUFFIX)}
    stats = {"pages_with_nocite": 0, "inlined_shortcodes": 0, "removed_variables": len(cites)}
    if not cites:
        return stats

    # Read the sources before step 2 rewrites the shortcodes they use.
    page_keys: Dict[Path, List[str]] = {}
    for page in sorted(set(page_paths)):
        page_path = build_dir / page
        keys = {
            cites[cite_name].lstrip("@")
            for name in extract_variables_from_qmd(page_path, build_dir)
            if (cite_name := strip_generated_variable_suffix(name) + CITE_VARIABLE_SUFFIX) in cites
        }
        if keys:
            page_keys[page_path.resolve()] = sorted(keys)

    inline = {name: "@{" + value.lstrip("@") + "}" for name, value in cites.items()}
    for qmd_path in sorted(build_dir.rglob("*.qmd")):
        content = qmd_path.read_text(encoding="utf-8")
        updated, inlined = _RE_CITE_SHORTCODE.subn(lambda m: inline.get(m.group(1), m.group(0)), content)
        keys = page_keys.get(qmd_path.resolve())
        if keys:
            updated = _add_nocite(updated, keys, str(qmd_path.relative_to(build_dir)))
            stats["pages_with_nocite"] += 1
        if updated != content:
            qmd_path.write_text(updated, encoding="utf-8", newline="\n")
        stats["inlined_shortcodes"] += inlined

    kept = {name: value for name, value in variables.items() if not name.endswith(CITE_VARIABLE_SUFFIX)}
    with open(variables_path, "w", encoding="utf-8", newline="\n") as f:
        yaml.dump(
            kept, f, Dumper=_yaml_dumper, allow_unicode=True, default_flow_style=False,
            sort_keys=True, default_style='"',
        )
    return stats


def keep_one_bibliography_page(build_dir: Path, page_paths: Iterable[str], references_page: str) -> List[str]:
    """Remove ::: {#refs} blocks from every page except the references page.

    Returns the pages that lost a block. The removed "References" heading had
    nothing under it: Quarto hides the reference list on every other page.
    """
    references_path = build_dir / references_page
    if not _RE_QUARTO_REFS_LINE.search(references_path.read_text(encoding="utf-8")):
        raise ValueError(f"references-page {references_page} has no ::: {{#refs}} block")

    stripped: List[str] = []
    for page in sorted(set(page_paths) - {references_page}):
        page_path = build_dir / page
        content = page_path.read_text(encoding="utf-8")
        updated = _RE_REFS_BLOCK.sub("", content)
        if _RE_QUARTO_REFS_LINE.search(updated):
            raise ValueError(
                f"{page} still has a ::: {{#refs}} line that this build cannot remove, so Quarto "
                f"would put the book bibliography there instead of on {references_page}"
            )
        if updated != content:
            page_path.write_text(updated, encoding="utf-8", newline="\n")
            stripped.append(page)
    return stripped
