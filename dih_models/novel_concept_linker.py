#!/usr/bin/env python3
"""
Novel Concept Linker
====================

Normalizes mentions of project-specific concepts in QMD sources by:
1. Linking the first eligible mention in each file to the canonical target
2. Appending the owning paper citation if it is missing

Concept definitions live in paper configs under `dih-render.concept-terms`, e.g.:

    dih-render:
      concept-terms:
        - term: Wishocracy
          aliases: [RAPPA]
          manual-target: knowledge/solution/wishocracy.qmd

The linker derives the cite key and site URL from the owning `_quarto-*.yml`
paper config, and it suppresses self-citation when processing that paper's
own `dih-render.index-source`.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, List, Sequence, Set, Tuple

from dih_models.quarto_references_generator import extract_paper_citation_info
from dih_models.yaml_utils import load_quarto_config

logger = logging.getLogger("dih.novel_concept_linker")

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
BARE_URL_RE = re.compile(r"https?://\S+")

SKIP_FILE_PATTERNS = (
    "knowledge/papers.qmd",
    "knowledge/references.qmd",
    "knowledge/appendix/parameters-and-calculations.qmd",
    "knowledge/appendix/parameters-and-calculations-*.qmd",
)

SKIP_LINE_PREFIXES = ("#", "|", "![", "<", ":::", "```")


@dataclass(frozen=True)
class ConceptRule:
    key: str
    owner_config_name: str
    owner_source_path: Path | None
    target: str
    citation_keys: Tuple[str, ...]
    patterns: Tuple[re.Pattern[str], ...]

    @property
    def citation_suffix(self) -> str:
        if not self.citation_keys:
            return ""
        joined = "; ".join(f"@{key}" for key in self.citation_keys)
        return f" [{joined}]"

    def has_citation(self, text: str) -> bool:
        return any(f"@{key}" in text for key in self.citation_keys)


@dataclass
class LinkerStats:
    files_scanned: int = 0
    files_changed: int = 0
    links_added: int = 0
    citations_added: int = 0
    concepts_normalized: int = 0


def _collect_qmd_paths(node: Any, results: Set[str]) -> None:
    """Recursively collect .qmd paths from Quarto config structures."""
    if isinstance(node, str):
        if node.endswith(".qmd"):
            results.add(node)
        return

    if isinstance(node, list):
        for item in node:
            _collect_qmd_paths(item, results)
        return

    if not isinstance(node, dict):
        return

    href = node.get("href")
    if isinstance(href, str) and href.endswith(".qmd"):
        results.add(href)

    for key in ("chapters", "contents", "appendices"):
        if key in node:
            _collect_qmd_paths(node[key], results)


def _get_config_qmd_files(project_root: Path, config_name: str = "manual") -> List[Path]:
    config_path = project_root / f"_quarto-{config_name}.yml"
    config = load_quarto_config(config_path)

    qmd_paths: Set[str] = set()

    book = config.get("book", {}) if isinstance(config, dict) else {}
    _collect_qmd_paths(book.get("chapters", []), qmd_paths)
    _collect_qmd_paths(book.get("appendices", []), qmd_paths)

    project_cfg = config.get("project", {}) if isinstance(config, dict) else {}
    _collect_qmd_paths(project_cfg.get("render", []), qmd_paths)

    dih_render = config.get("dih-render", {}) if isinstance(config, dict) else {}
    index_source = dih_render.get("index-source")
    if isinstance(index_source, str) and index_source.endswith(".qmd"):
        qmd_paths.add(index_source)
        # Standalone paper renders often copy the source to root index.qmd.
        # Prefer the actual source file for normalization.
        qmd_paths.discard("index.qmd")

    resolved: List[Path] = []
    for rel_path in sorted(qmd_paths):
        file_path = (project_root / rel_path).resolve()
        if file_path.exists():
            resolved.append(file_path)
    return resolved


def _should_skip_file(project_root: Path, file_path: Path) -> bool:
    try:
        rel_path = file_path.resolve().relative_to(project_root.resolve())
    except ValueError:
        return False
    rel = PurePosixPath(rel_path.as_posix())
    return any(rel.match(pattern) for pattern in SKIP_FILE_PATTERNS)


def _relative_target(project_root: Path, current_file: Path, target: str) -> str:
    if target.startswith(("http://", "https://")):
        return target
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = project_root / target_path
    rel = os.path.relpath(target_path, start=current_file.parent)
    return rel.replace("\\", "/")


def _protect_spans(line: str) -> List[Tuple[int, int]]:
    spans: List[Tuple[int, int]] = []
    for regex in (MARKDOWN_LINK_RE, IMAGE_LINK_RE, INLINE_CODE_RE, BARE_URL_RE):
        for match in regex.finditer(line):
            spans.append((match.start(), match.end()))
    spans.sort()
    return spans


def _span_overlaps(spans: Sequence[Tuple[int, int]], start: int, end: int) -> bool:
    return any(start < span_end and end > span_start for span_start, span_end in spans)


def _line_is_skippable(line: str) -> bool:
    stripped = line.lstrip()
    return not stripped or stripped.startswith(SKIP_LINE_PREFIXES)


def _compile_term_pattern(term: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w/]){re.escape(term)}(?![\w-])", re.IGNORECASE)


def _slugify_term(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _normalize_aliases(raw_aliases: Any) -> List[str]:
    if isinstance(raw_aliases, str):
        alias = raw_aliases.strip()
        return [alias] if alias else []
    if isinstance(raw_aliases, list):
        aliases: List[str] = []
        for alias in raw_aliases:
            alias_text = str(alias).strip()
            if alias_text:
                aliases.append(alias_text)
        return aliases
    return []


def _normalize_citation_keys(raw_entry: Any, default_keys: Tuple[str, ...]) -> Tuple[str, ...]:
    if isinstance(raw_entry, str):
        cite_key = raw_entry.strip()
        return (cite_key,) if cite_key else default_keys
    if isinstance(raw_entry, list):
        keys = tuple(str(item).strip() for item in raw_entry if str(item).strip())
        return keys or default_keys
    return default_keys


def _load_concept_rules(project_root: Path) -> Tuple[ConceptRule, ...]:
    rules: List[ConceptRule] = []

    for config_path in sorted(project_root.glob("_quarto-*.yml")):
        match = re.match(r"_quarto-(.+)\.yml", config_path.name)
        if not match:
            continue

        config_name = match.group(1)
        config = load_quarto_config(config_path)
        dih_render = config.get("dih-render", {}) if isinstance(config, dict) else {}
        if not isinstance(dih_render, dict):
            continue

        raw_concepts = dih_render.get("concept-terms", [])
        if not raw_concepts:
            continue

        if isinstance(raw_concepts, (str, dict)):
            raw_concepts = [raw_concepts]
        if not isinstance(raw_concepts, list):
            continue

        citation_info = extract_paper_citation_info(config_path, config_name) or {}
        default_citation_keys: Tuple[str, ...] = ()
        cite_key = citation_info.get("citation_key")
        if isinstance(cite_key, str) and cite_key.strip():
            default_citation_keys = (cite_key.strip(),)

        default_target = str(citation_info.get("url", "") or "").strip()
        owner_source_path = None
        index_source = dih_render.get("index-source")
        if isinstance(index_source, str) and index_source.endswith(".qmd"):
            owner_source_path = (project_root / index_source).resolve()

        for raw_concept in raw_concepts:
            if isinstance(raw_concept, str):
                concept_entry = {"term": raw_concept}
            elif isinstance(raw_concept, dict):
                concept_entry = raw_concept
            else:
                continue

            term = str(concept_entry.get("term", "") or "").strip()
            if not term:
                continue

            aliases = _normalize_aliases(concept_entry.get("aliases", []))
            citation_keys = _normalize_citation_keys(
                concept_entry.get("citation-keys", concept_entry.get("citation-key")),
                default_citation_keys,
            )
            target = str(
                concept_entry.get("manual-target")
                or concept_entry.get("target")
                or default_target
                or ""
            ).strip()

            if not target:
                logger.warning(
                    "Skipping concept term '%s' in %s: no target available",
                    term,
                    config_path.name,
                )
                continue

            terms = [term, *aliases]
            patterns = tuple(_compile_term_pattern(candidate) for candidate in terms if candidate)
            if not patterns:
                continue

            rules.append(
                ConceptRule(
                    key=f"{config_name}:{_slugify_term(term) or 'concept'}",
                    owner_config_name=config_name,
                    owner_source_path=owner_source_path,
                    target=target,
                    citation_keys=citation_keys,
                    patterns=patterns,
                )
            )

    return tuple(rules)


def _append_citation_to_existing_link(line: str, rule: ConceptRule) -> Tuple[str, bool, bool, bool]:
    """
    Returns: (updated_line, changed, handled, citation_added)

    handled=True means this file already has a suitable first mention for the concept,
    whether or not any rewrite was needed.
    """
    for match in MARKDOWN_LINK_RE.finditer(line):
        link_text = match.group(1)
        if not any(pattern.search(link_text) for pattern in rule.patterns):
            continue

        link_target = match.group(2)
        normalized_link = f"[{link_text}]({link_target.replace('\\', '/')})"
        updated = f"{line[:match.start()]}{normalized_link}{line[match.end():]}"
        changed = updated != line

        if rule.has_citation(updated):
            return updated, changed, True, False

        if not rule.citation_keys:
            return updated, changed, True, False

        insert_at = match.start() + len(normalized_link)
        updated = f"{updated[:insert_at]}{rule.citation_suffix}{updated[insert_at:]}"
        return updated, True, True, True

    return line, False, False, False


def _replace_first_plain_mention(project_root: Path, line: str, rule: ConceptRule, file_path: Path) -> Tuple[str, bool, bool]:
    protected = _protect_spans(line)
    for pattern in rule.patterns:
        for match in pattern.finditer(line):
            if _span_overlaps(protected, match.start(), match.end()):
                continue

            matched_text = match.group(0)
            link_target = _relative_target(project_root, file_path, rule.target)
            replacement = f"[{matched_text}]({link_target})"
            citation_added = False
            if rule.citation_keys and not rule.has_citation(line):
                replacement += rule.citation_suffix
                citation_added = True

            updated = f"{line[:match.start()]}{replacement}{line[match.end():]}"
            return updated, True, citation_added

    return line, False, False


def _normalize_file(project_root: Path, file_path: Path, rules: Sequence[ConceptRule]) -> dict[str, int]:
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    if not lines:
        return {"links_added": 0, "citations_added": 0, "concepts_normalized": 0, "changed": 0}

    file_owner_configs = {
        rule.owner_config_name
        for rule in rules
        if rule.owner_source_path is not None and rule.owner_source_path == file_path.resolve()
    }
    try:
        display_path = file_path.resolve().relative_to(project_root.resolve())
    except ValueError:
        display_path = file_path

    concept_done = {
        rule.key: (
            rule.owner_config_name in file_owner_configs
            or (
                not rule.target.startswith(("http://", "https://"))
                and (project_root / rule.target).resolve() == file_path.resolve()
            )
        )
        for rule in rules
    }

    changed = False
    links_added = 0
    citations_added = 0
    concepts_normalized = 0

    in_frontmatter = bool(lines and lines[0].strip() == "---")
    frontmatter_seen = 0
    in_code_fence = False

    for idx, line in enumerate(lines):
        stripped = line.strip()

        if in_frontmatter:
            if stripped == "---":
                frontmatter_seen += 1
                if frontmatter_seen >= 2:
                    in_frontmatter = False
            continue

        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue

        if in_code_fence or _line_is_skippable(line):
            continue

        updated_line = line
        line_changed = False

        for rule in rules:
            if concept_done[rule.key]:
                continue

            existing_link_line, link_changed, handled, citation_added = _append_citation_to_existing_link(updated_line, rule)
            if handled:
                if citation_added:
                    citations_added += 1
                if link_changed or citation_added:
                    updated_line = existing_link_line
                    line_changed = True
                concept_done[rule.key] = True
                concepts_normalized += 1
                continue

            replaced_line, replaced, citation_added = _replace_first_plain_mention(project_root, updated_line, rule, file_path)
            if replaced:
                link_target = _relative_target(project_root, file_path, rule.target)
                updated_line = replaced_line
                line_changed = True
                links_added += 1
                if citation_added:
                    citations_added += 1
                concept_done[rule.key] = True
                concepts_normalized += 1
                logger.debug(
                    "[%s] Linked %s in %s -> %s",
                    rule.key,
                    file_path.name,
                    display_path,
                    link_target,
                )

        if line_changed:
            lines[idx] = updated_line
            changed = True

    if changed:
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    return {
        "links_added": links_added,
        "citations_added": citations_added,
        "concepts_normalized": concepts_normalized,
        "changed": int(changed),
    }


def normalize_config_concept_links(project_root: Path, config_name: str = "manual") -> LinkerStats:
    """
    Normalize concept links/citations for files referenced by a Quarto config.

    Args:
        project_root: Repository root
        config_name: Quarto config stem, e.g. "manual" for _quarto-manual.yml

    Returns:
        LinkerStats summary
    """
    stats = LinkerStats()
    rules = _load_concept_rules(project_root)
    qmd_files = _get_config_qmd_files(project_root, config_name=config_name)

    if not rules:
        logger.info("[*] No concept rules configured in _quarto-*.yml files")
        return stats

    for file_path in qmd_files:
        if _should_skip_file(project_root, file_path):
            continue

        stats.files_scanned += 1
        result = _normalize_file(project_root, file_path, rules)
        stats.links_added += result["links_added"]
        stats.citations_added += result["citations_added"]
        stats.concepts_normalized += result["concepts_normalized"]
        stats.files_changed += result["changed"]

    logger.info(
        "[OK] Normalized novel concept links in %d file(s): %d changed, %d link(s) added, %d citation(s) added",
        stats.files_scanned,
        stats.files_changed,
        stats.links_added,
        stats.citations_added,
    )
    return stats


def normalize_manual_concept_links(project_root: Path, config_name: str = "manual") -> LinkerStats:
    """Backward-compatible wrapper for the manual book config."""
    return normalize_config_concept_links(project_root, config_name=config_name)
