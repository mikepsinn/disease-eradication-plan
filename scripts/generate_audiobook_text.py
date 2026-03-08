#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audiobook Text Generator

Loops through chapters in a Quarto config, programmatically strips Quarto/Markdown
markup and resolves variables, then sends to an LLM for audiobook narration rewrite.

Programmatic (deterministic): strip frontmatter, code blocks, shortcodes, LaTeX,
    HTML, citations, footnotes, cross-refs, div blocks, image paths, link URLs,
    resolve {{< var >}} to actual values.

LLM (creative): convert numbers/money to spoken words, tables to prose, lists to
    flowing sentences, section transitions, overall narration flow.

Pipeline: QMD -> programmatic strip -> resolve variables -> LLM rewrite -> text -> TTS

Usage:
    python scripts/generate_audiobook_text.py                          # All chapters
    python scripts/generate_audiobook_text.py --chapter 5              # Single chapter
    python scripts/generate_audiobook_text.py --start 3 --end 10      # Range
    python scripts/generate_audiobook_text.py --config _quarto-manual-paperback.yml
    python scripts/generate_audiobook_text.py --list                   # List chapters
    python scripts/generate_audiobook_text.py --force                  # Regenerate all
    python scripts/generate_audiobook_text.py --dry-run                # Preview without calling LLM
"""
import io
import sys
import re
import os
import random
import argparse
import hashlib
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import cast

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    cast(io.TextIOWrapper, sys.stdout).reconfigure(encoding='utf-8')

# Add scripts directory and project root to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from dih_models.yaml_utils import load_quarto_config
from dih_models.variable_replacement import load_variables, replace_variables
from lib.audiobook_common import (
    PROJECT_ROOT, NARRATION_DIR, VARIABLES_YML, DEFAULT_CONFIG_PATH,
    extract_chapters, extract_title_from_qmd, safe_filename, chapter_slug,
    config_name_from_path, get_paths,
)
from lib.audiobook_manifest import save_text_results
from lib.build_logger import BuildLogger, SingleLineProgress
from lib.retry import RateLimiter

# Configuration
OUTPUT_DIR = NARRATION_DIR
LOGGER: BuildLogger | None = None

MAX_CHUNK_CHARS = 3_000

# LLM parallelization
def _env_int(name: str, default: int, minimum: int = 1) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return max(minimum, int(raw))
    except ValueError:
        return default


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


# Higher default worker count can improve throughput for long-latency calls.
# The sliding-window limiter below still caps request rate.
LLM_PARALLEL_WORKERS = _env_int("AUDIOBOOK_LLM_WORKERS", 6)
LLM_REQUESTS_PER_MINUTE = _env_int("AUDIOBOOK_LLM_REQUESTS_PER_MINUTE", 15)
LLM_MAX_ATTEMPTS = _env_int("AUDIOBOOK_LLM_MAX_ATTEMPTS", 6)
# Single-line progress display for narration chunk generation.
LLM_SINGLE_LINE_PROGRESS = _env_flag("AUDIOBOOK_LLM_SINGLE_LINE_PROGRESS", True)
llm_rate_limiter = RateLimiter(max_requests=LLM_REQUESTS_PER_MINUTE, window_seconds=60)


def _log_info(message: str) -> None:
    if LOGGER:
        LOGGER.info(message)
    else:
        print(f"[*] {message}")


def _log_ok(message: str) -> None:
    if LOGGER:
        LOGGER.ok(message)
    else:
        print(f"[OK] {message}")


def _log_error(message: str) -> None:
    if LOGGER:
        LOGGER.error(message)
    else:
        print(f"[ERROR] {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Programmatic stripping (deterministic, easy stuff)
# ---------------------------------------------------------------------------

def strip_qmd_markup(content: str) -> str:
    """
    Strip Quarto/Markdown markup that has no business in an audiobook.
    Keeps prose, tables, lists, and headers as-is for the LLM to handle.
    """
    # Remove .no-narration blocks entirely (content + markers).
    # Use ::: {.no-narration} in QMD to exclude tables, charts, etc. from audiobook.
    # Must run before general div stripping.
    def _strip_no_narration(content: str) -> str:
        """Remove ::: {.no-narration} blocks, handling nested ::: divs."""
        result = []
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            if re.match(r'^:+\s*\{\.no-narration\}', lines[i]):
                # Count nesting depth to find the matching closer
                depth = 1
                i += 1
                while i < len(lines) and depth > 0:
                    if re.match(r'^:+\s*\{', lines[i]):
                        depth += 1
                    elif re.match(r'^:+\s*$', lines[i]):
                        depth -= 1
                    i += 1
            else:
                result.append(lines[i])
                i += 1
        return '\n'.join(result)
    content = _strip_no_narration(content)

    # Remove YAML frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Remove fenced code blocks
    content = re.sub(r'```[\s\S]*?```', '', content)

    # Remove Quarto executable code blocks
    content = re.sub(r'\{[#]?(?:python|r|julia|bash|sql)[\s\S]*?\}[\s\S]*?(?=\n\n|\n#|\Z)', '', content)

    # Remove Quarto shortcodes except var (include, video, embed, etc.)
    content = re.sub(r'\{\{<\s*(?!var\s)\w+\s+[^>]*>\}\}', '', content)

    # Remove LaTeX display math blocks
    content = re.sub(r'\$\$[\s\S]*?\$\$', '', content)

    # Remove inline LaTeX math (but NOT dollar amounts like $100 or $1.5B)
    # LaTeX inline math: $x = y$ or $\text{foo}$ -- contains letters/backslashes, not just digits
    content = re.sub(r'(?<!\w)\$(?!\d)([^$\n]+)\$(?!\d)', '', content)

    # Remove confidence intervals: (95% CI: $X-$Y), (95% CI: X-Y), 95% CI [X, Y]
    content = re.sub(r'\s*\(95% CI:[^)]+\)', '', content)
    content = re.sub(r',?\s*95% CI\s*\*?\*?\[[^\]]+\]\*?\*?', '', content)

    # Remove HTML comments
    content = re.sub(r'<!--[\s\S]*?-->', '', content)

    # Remove HTML tags (keep content)
    content = re.sub(r'<[^>]+>', '', content)

    # Remove Quarto div openers/closers (callouts, panel-tabset, figure divs)
    content = re.sub(r'^:::\s*\{[^}]+\}\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^:::\s*$', '', content, flags=re.MULTILINE)

    # Remove citations: [@key], [@key1; @key2]
    content = re.sub(r'\s*\[@[^\]]+\]', '', content)

    # Remove cross-references: @fig-label, @tbl-label, @sec-label
    content = re.sub(r'@(?:fig|tbl|sec)-[a-zA-Z0-9_-]+', '', content)

    # Remove footnote markers and definitions
    content = re.sub(r'\[\^[^\]]+\]', '', content)
    content = re.sub(r'^\[\^[^\]]+\]:.*$', '', content, flags=re.MULTILINE)

    # Remove section header ID attributes {#some-id}
    content = re.sub(r'\s*\{#[a-zA-Z0-9_-]+\}', '', content)

    # Remove image attribute blocks {width=50% #fig-id .class}
    content = re.sub(r'\{[^}]*(?:width|height|#fig|\.)[^}]*\}', '', content)

    # Images: drop entirely (alt text often has partial numbers/formatting that garbles)
    # The LLM prompt says to remove image captions anyway
    content = re.sub(r'!\[[^\]]*\]\([^)]+\)(?:\{[^}]*\})?', '', content)

    # Links: keep full markdown syntax so the LLM can see what was a link
    # and decide whether link text is spoken prose vs. a navigation label to drop.
    # Only strip reference-style link definitions (not useful for the LLM).
    content = re.sub(r'^\[[^\]]+\]:\s+.*$', '', content, flags=re.MULTILINE)

    # Remove horizontal rules
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*\*+$', '', content, flags=re.MULTILINE)

    # Add periods to lines that don't end with punctuation (helps TTS prosody)
    content = re.sub(r'([a-zA-Z0-9\)\]"\'])$', r'\1.', content, flags=re.MULTILINE)

    # Clean up excessive whitespace
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def split_long_lines(text: str, max_chars: int = 300) -> str:
    """Split lines longer than max_chars at sentence boundaries for better TTS prosody."""
    lines = text.split('\n')
    result = []
    for line in lines:
        if len(line) <= max_chars:
            result.append(line)
            continue
        # Split at sentence boundaries (. ! ?) followed by a space
        sentences = re.split(r'(?<=[.!?])\s+', line)
        current = ''
        for sentence in sentences:
            if current and len(current) + len(sentence) + 1 > max_chars:
                result.append(current)
                current = sentence
            else:
                current = current + ' ' + sentence if current else sentence
        if current:
            result.append(current)
    return '\n'.join(result)


def prepare_for_narration(raw_qmd: str, variables: dict) -> str:
    """
    Programmatic pipeline: resolve variables first, then strip markup.
    Variables must be resolved before HTML stripping (which would eat the
    {{< var >}} angle brackets).
    """
    # 1. Strip _cite variable references before resolving (they produce citation
    #    text that should not be spoken in the audiobook narration)
    text = re.sub(r'\{\{<\s*var\s+\w+_cite\s*>\}\}', '', raw_qmd)
    # 2. Resolve remaining variables while syntax is still intact
    text = replace_variables(text, variables, highlight_missing=False)
    # Remove any remaining unresolved variable syntax
    text = re.sub(r'\{\{<\s*var\s+\w+\s*>\}\}', '', text)
    # 3. Strip all markup
    text = strip_qmd_markup(text)
    # 4. Split very long lines at sentence boundaries for better TTS prosody
    text = split_long_lines(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ---------------------------------------------------------------------------
# LLM narration rewrite (creative stuff)
# ---------------------------------------------------------------------------

AUDIOBOOK_REWRITE_PROMPT = """Convert this book chapter to an audiobook narration script.

Your job is MINIMAL: only change what would sound obviously wrong or excruciatingly boring spoken aloud. Leave everything else EXACTLY as written.

CONVERT (only these):
- ALL numbers to spoken words. Never leave bare digits in the output: "50" -> "fifty", "$8.2T" -> "eight point two trillion dollars", "5%" -> "five percent". For k/K suffixes compute the full number: "3.07k" -> "three thousand and seventy" (not "three point zero seven thousand"). Years: use natural English pronunciation. Years 2010+ split as "twenty XX" ("2024" -> "twenty twenty-four"). Years 2000-2009 use "two thousand and X" ("2003" -> "two thousand and three", NOT "twenty oh-three"). Years before 2000 use standard form ("1993" -> "nineteen ninety-three", "1975" -> "nineteen seventy-five").
- Alphanumeric abbreviations: "WW2" -> "World War Two", "WW1" -> "World War One", "G7" -> "G Seven", "G20" -> "G Twenty"
- Tables: convert rows into short spoken sentences
- Bullet lists: one sentence per bullet, keep them as separate paragraphs
- Condense/improve extremely boring sentences with too many dense numbers or weird units: condense or round or use different unit framings when a run of numbers would sound excruciatingly boring or extremely weird spoken aloud. When in doubt, leave as-is.
- Acronyms: spell out with dots ("GDP" -> "G.D.P.", "FDA" -> "F.D.A.") EXCEPT acronyms pronounced as words ("PAC", "NATO" stay as-is). 
- Unfamiliar acronyms: expand acronyms that the average person would not know on first use (for example, "DALYs" -> "disability-adjusted life years, or D.A.L.Y.s"). BUT if the text already expands an acronym (e.g., "DALYs (Disability-Adjusted Life Years)"), do NOT expand it again; just add dots to the acronym part.
- Well-known acronyms (GDP, FDA, NIH, NATO): just add dots, don't expand. "dFDA" always becomes "D.F.D.A." (a decentralized FDA).
- Strip markdown formatting characters (**, ##, -, etc.)

KEEP for TTS:
- PRESERVE ALL-CAPS words or italics where they would help the TTS engine speak with emphasis.
- PRESERVE Quote marks around dialogue: "Hey, we didn't die!" -- helps TTS shift into speaking prosody
- PRESERVE Contractions (don't, can't, it's stay as-is)
- PRESERVE Parenthetical asides IN PARENTHESES -- they're the comedic delivery. TTS handles parentheses well.
  NEVER convert "(they're very vain)" to ", they're very vain" or "as they're very vain" or "which is very vain".
  NEVER convert "(requires many papers)" to ", which requires many papers".
  Keep the literal ( ) characters exactly as written.

Section headers (## lines): keep the text as a standalone paragraph (strip ## markers), then add a blank line after. They're often jokes or punchy phrases that work as natural pauses.

REMOVE:
- remove or edit text only if would sound extremly weird to be spoken in an audiobook. 

RULES:
- DO NOT remove or rephrase parenthetical asides. "(they're very vain)" must stay as "(they're very vain)", not become ", they're very vain"
- DO NOT collapse paragraphs together. Keep the original paragraph breaks. Short punchy lines should stay short and punchy.
- DO NOT add transition phrases like "Regarding...", "As for...", "Now let's consider..."
- DO NOT rewrite, rephrase, or "improve" any sentence that already reads naturally
- DO NOT add chapter headers or narrator instructions

Return ONLY the narration text."""


def _fmt_elapsed_short(seconds: float) -> str:
    """Format elapsed seconds as M:SS or H:MM:SS."""
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _is_likely_rate_limit_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(
        token in msg
        for token in (
            "429",
            "rate limit",
            "too many requests",
            "resource_exhausted",
            "quota",
            "quota exceeded",
        )
    )


def _llm_call_with_retries(prompt: str, label: str) -> str:
    """Call Gemini Flash with adaptive backoff for rate-limit/transient failures."""
    from lib.llm import generate_gemini_flash_content

    transient_backoff = (5.0, 10.0, 20.0, 30.0, 45.0)
    for attempt in range(1, LLM_MAX_ATTEMPTS + 1):
        try:
            llm_rate_limiter.acquire()
            return generate_gemini_flash_content(prompt).strip()
        except Exception as e:
            if attempt >= LLM_MAX_ATTEMPTS:
                raise

            if _is_likely_rate_limit_error(e):
                # Exponential backoff with jitter to reduce synchronized retries.
                wait = min(120.0, 5.0 * (2 ** (attempt - 1))) + random.uniform(0.0, 2.0)
                print(
                    f"    [LLM RATE LIMIT] {label}attempt {attempt}/{LLM_MAX_ATTEMPTS} failed: {e}"
                )
            else:
                wait = transient_backoff[min(attempt - 1, len(transient_backoff) - 1)]
                print(
                    f"    [LLM RETRY] {label}attempt {attempt}/{LLM_MAX_ATTEMPTS} failed: {e}"
                )

            print(f"    [LLM RETRY] Waiting {wait:.1f}s...", flush=True)
            time.sleep(wait)

    raise RuntimeError(f"LLM request failed unexpectedly for {label}")


def rewrite_for_audiobook(
    text: str,
    title: str,
    output_path: Path,
    intro_text: str = "",
    debug_chunks: bool = False,
    progress_interval_s: float = 5.0,
) -> tuple[str, dict[str, int | float]]:
    """
    Send pre-processed text to LLM for narration rewrite.
    Saves each chunk to disk as it completes so we can resume after crashes.
    Uses parallel workers for uncached chunks and emits periodic progress.
    """
    from lib.llm import generate_gemini_flash_content

    rewrite_start = time.monotonic()
    chunks = chunk_text(text)
    # Insert intro (title + description) as a dedicated first chunk
    # so TTS generates it separately (combining with content degrades quality)
    if intro_text:
        chunks.insert(0, intro_text)
    # Chunks go in the adjacent narration-txt-chunks/ dir, not nested under narration-txt-chapters/
    chunk_dir = output_path.parent.parent / "narration-txt-chunks" / output_path.stem
    chunk_dir.mkdir(parents=True, exist_ok=True)

    total = len(chunks)
    # results[i] holds the rewritten text for chunk i
    results: list[str | None] = [None] * total

    # Collect cached results and build work items for uncached chunks
    cached_chunks = 0
    work_items = []
    for i, chunk in enumerate(chunks):
        chunk_file = chunk_dir / f"chunk-{i+1:02d}-of-{total:02d}.txt"
        if chunk_file.exists():
            cached_chunks += 1
            if debug_chunks:
                print(f"    [CACHED] chunk {i + 1}/{total} ({chunk_file.stat().st_size:,} bytes)")
            results[i] = chunk_file.read_text(encoding='utf-8')
        else:
            work_items.append((i, chunk, chunk_file))

    generated_chunks = len(work_items)
    workers = min(LLM_PARALLEL_WORKERS, generated_chunks) if generated_chunks else 0
    print(
        f"    [LLM NARRATION PLAN] chunks total={total}, cached={cached_chunks}, "
        f"to-generate={generated_chunks}, workers={workers}"
    )
    if generated_chunks:
        print(
            "    [LLM NARRATION START] Sending prepared text chunks to Gemini Flash "
            "to generate audiobook narration text"
        )

    generated_chars = 0
    if work_items:
        def _rewrite_one(item):
            i, chunk, chunk_file = item
            label = f"chunk {i + 1}/{total}"
            if total > 1:
                context = f"\n\nThis is part {i + 1} of {total} of the chapter \"{title}\". Continue from where the previous part left off."
            else:
                context = f"\n\nThis is the chapter \"{title}\"."
            prompt = AUDIOBOOK_REWRITE_PROMPT + context + "\n\n---\n\nCONTENT TO CONVERT:\n\n" + chunk

            start = time.monotonic()
            result = _llm_call_with_retries(prompt, label=f"{label} ")
            chunk_file.write_text(result, encoding='utf-8')
            elapsed = time.monotonic() - start
            return i, result, len(chunk), elapsed, chunk_file.name

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_rewrite_one, item): item for item in work_items}
            completed = 0
            recent_done: list[int] = []
            generation_start = time.monotonic()
            last_progress = generation_start
            progress = SingleLineProgress(enabled=LLM_SINGLE_LINE_PROGRESS)

            for future in as_completed(futures):
                item = futures[future]
                try:
                    i, result, chunk_chars, chunk_elapsed, chunk_filename = future.result()
                except Exception as e:
                    chunk_idx = item[0] + 1
                    progress.clear()
                    raise RuntimeError(
                        f"LLM narration generation failed for chunk {chunk_idx}/{total}: {e}"
                    ) from e
                results[i] = result
                completed += 1
                generated_chars += chunk_chars
                recent_done.append(i + 1)
                if len(recent_done) > 3:
                    recent_done.pop(0)

                if debug_chunks:
                    progress.clear()
                    print(
                        f"    [LLM CHUNK DONE] {i + 1:02d}/{total:02d} "
                        f"chars={chunk_chars:,} elapsed={chunk_elapsed:.1f}s file={chunk_filename}"
                    )

                now = time.monotonic()
                if (
                    now - last_progress >= progress_interval_s
                    or completed == generated_chunks
                ):
                    elapsed = now - generation_start
                    rate = completed / elapsed if elapsed > 0 else 0.0
                    remaining = generated_chunks - completed
                    eta = remaining / rate if rate > 0 else 0.0
                    pct = (completed / generated_chunks * 100) if generated_chunks else 100.0
                    chapter_ready = cached_chunks + completed
                    chunks_per_min = rate * 60.0
                    avg_chunk_s = (elapsed / completed) if completed > 0 else 0.0
                    recent = ",".join(f"{n:02d}" for n in recent_done) if recent_done else "-"
                    progress.update(
                        f"    [LLM NARRATION PROGRESS] chunks done={completed}/{generated_chunks} "
                        f"({pct:.0f}%) chapter-ready={chapter_ready}/{total} "
                        f"elapsed={_fmt_elapsed_short(elapsed)} "
                        f"eta={_fmt_elapsed_short(eta)} "
                        f"throughput={chunks_per_min:.1f}/min avg={avg_chunk_s:.1f}s/chunk "
                        f"recent={recent}",
                        final=(completed == generated_chunks),
                    )
                    last_progress = now

            progress.clear()

    rewritten = '\n\n'.join(r for r in results if r is not None)
    rewrite_elapsed = time.monotonic() - rewrite_start
    print(
        f"    [LLM NARRATION DONE] chunks total={total}, cached={cached_chunks}, "
        f"generated={generated_chunks}, elapsed={_fmt_elapsed_short(rewrite_elapsed)}"
    )
    stats: dict[str, int | float] = {
        "chunks_total": total,
        "chunks_cached": cached_chunks,
        "chunks_generated": generated_chunks,
        "generated_chars": generated_chars,
        "rewrite_elapsed_s": rewrite_elapsed,
    }
    return rewritten, stats


def chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """Split text into chunks at paragraph boundaries."""
    paragraphs = text.split('\n\n')
    chunks = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para) + 2
        if current_len + para_len > max_chars and current:
            chunks.append('\n\n'.join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append('\n\n'.join(current))

    return chunks


# ---------------------------------------------------------------------------
# Per-chapter generation
# ---------------------------------------------------------------------------

def generate_chapter_text(
    chapter: dict,
    variables: dict,
    force: bool = False,
    dry_run: bool = False,
    debug_chunks: bool = False,
    seq: int | None = None,
    total: int | None = None,
) -> dict | None:
    """Generate audiobook text for a single chapter."""
    chapter_start = time.monotonic()
    qmd_path = PROJECT_ROOT / chapter['path']
    if not qmd_path.exists():
        print(f"  [SKIP] File not found: {qmd_path}")
        return None

    title = chapter['title'] or extract_title_from_qmd(qmd_path)

    slug = chapter_slug(chapter)
    output_path = OUTPUT_DIR / f"{slug}.prepared.txt"
    chapter_header = None
    if seq is not None and total is not None:
        chapter_header = (
            f"\n[CHAPTER START] {seq:02d}/{total:02d} "
            f"idx={chapter['index']:02d} title={title}"
        )
    start_printed = False

    def _print_start_once() -> None:
        nonlocal start_printed
        if start_printed:
            return
        if chapter_header:
            print(chapter_header)
        start_printed = True

    raw_qmd = qmd_path.read_text(encoding='utf-8')

    # Hash QMD with variables resolved. Title and description come from
    # QMD frontmatter (inside raw_qmd), so no need to append separately.
    hash_input = replace_variables(raw_qmd, variables, highlight_missing=False)
    source_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]
    source_hash_file = OUTPUT_DIR / f"{slug}.source_hash"
    source_state = "new"
    if output_path.exists() and not force:
        old_source_hash = source_hash_file.read_text(encoding='utf-8').strip() if source_hash_file.exists() else ''
        if old_source_hash == source_hash:
            return {
                'index': chapter['index'], 'title': title, 'part': chapter['part'],
                'path': chapter['path'], 'text_file': str(output_path.relative_to(PROJECT_ROOT)),
                'status': 'cached',
                'slug': slug,
                'source_state': 'unchanged',
                'raw_chars': len(raw_qmd),
                'elapsed_s': time.monotonic() - chapter_start,
            }
        source_state = "stale"
        if debug_chunks:
            print(f"  [STALE] Source QMD changed (was {old_source_hash or 'unknown'}, now {source_hash}), regenerating")
    elif force:
        source_state = "forced"
    _print_start_once()
    original_vars = len(re.findall(r'\{\{<\s*var\s+\w+\s*>\}\}', raw_qmd))

    prepared = prepare_for_narration(raw_qmd, variables)

    # Build title and description as separate intro text
    # (generated as its own TTS chunk to avoid quality degradation)
    intro_parts = []
    if title:
        intro_parts.append(title)
    description = chapter.get('description', '')
    if description:
        intro_parts.append(description)
    intro_text = '\n\n'.join(intro_parts) if intro_parts else ''

    if not prepared or len(prepared) < 50:
        print(f"  [SKIP] Insufficient content in {qmd_path.name}")
        return None

    remaining_vars = len(re.findall(r'\{\{<\s*var\s+\w+\s*>\}\}', prepared))
    if debug_chunks:
        print(f"  Content: {len(raw_qmd):,} -> {len(prepared):,} chars, {original_vars} vars ({original_vars - remaining_vars} resolved)")

    if dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prepared, encoding='utf-8')
        source_hash_file.write_text(source_hash, encoding='utf-8')
        return {
            'index': chapter['index'], 'title': title, 'part': chapter['part'],
            'path': chapter['path'], 'text_file': str(output_path.relative_to(PROJECT_ROOT)),
            'status': 'dry_run',
            'slug': slug,
            'source_state': source_state,
            'raw_chars': len(raw_qmd),
            'prepared_chars': len(prepared),
            'vars_total': original_vars,
            'vars_resolved': original_vars - remaining_vars,
            'elapsed_s': time.monotonic() - chapter_start,
        }

    # Invalidate chunk cache if prepared text has changed
    chunk_dir = output_path.parent.parent / "narration-txt-chunks" / output_path.stem
    hash_file = chunk_dir / ".prepared_hash"
    hash_content = (intro_text + '\n\n' + prepared) if intro_text else prepared
    prepared_hash = hashlib.sha256(hash_content.encode('utf-8')).hexdigest()[:16]
    if chunk_dir.exists():
        if force:
            if debug_chunks:
                print(f"  [CACHE] Force flag set, clearing chunk cache")
            shutil.rmtree(chunk_dir)
        else:
            old_hash = hash_file.read_text(encoding='utf-8').strip() if hash_file.exists() else ''
            if old_hash != prepared_hash:
                if debug_chunks:
                    print(f"  [CACHE] Source text changed (was {old_hash or 'unknown'}, now {prepared_hash}), clearing chunk cache")
                shutil.rmtree(chunk_dir)
            elif debug_chunks:
                print(f"  [CACHE] Source text unchanged ({prepared_hash}), reusing chunk cache")

    rewritten, rewrite_stats = rewrite_for_audiobook(
        prepared,
        title,
        output_path,
        intro_text=intro_text,
        debug_chunks=debug_chunks,
    )

    # Save hash for future cache validation
    chunk_dir.mkdir(parents=True, exist_ok=True)
    hash_file.write_text(prepared_hash, encoding='utf-8')

    if not rewritten or len(rewritten) < 50:
        print(f"  [ERROR] LLM returned insufficient content")
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rewritten, encoding='utf-8')
    source_hash_file.write_text(source_hash, encoding='utf-8')

    return {
        'index': chapter['index'], 'title': title, 'part': chapter['part'],
        'path': chapter['path'], 'text_file': str(output_path.relative_to(PROJECT_ROOT)),
        'chars': len(rewritten), 'status': 'generated',
        'slug': slug,
        'source_state': source_state,
        'raw_chars': len(raw_qmd),
        'prepared_chars': len(prepared),
        'vars_total': original_vars,
        'vars_resolved': original_vars - remaining_vars,
        'elapsed_s': time.monotonic() - chapter_start,
        **rewrite_stats,
    }


# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------

def list_chapters(chapters: list[dict]):
    print("\nBook Chapters:")
    print("=" * 90)
    current_part = None
    for ch in chapters:
        if ch['part'] != current_part:
            current_part = ch['part']
            if current_part:
                print(f"\n  [{current_part}]")
        qmd_path = PROJECT_ROOT / ch['path']
        title = ch['title']
        if not title and qmd_path.exists():
            title = extract_title_from_qmd(qmd_path)
        title = title or ch['path']
        slug = chapter_slug(ch)
        text_file = OUTPUT_DIR / f"{slug}.prepared.txt"
        if text_file.exists():
            status = f"[x] ({text_file.stat().st_size:,} bytes)"
        else:
            status = "[ ]"
        print(f"  {status} {ch['index']:3d}. {title}")
    print("=" * 90)
    print(f"Total: {len(chapters)} chapters")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _chapter_summary_line(result: dict, seq: int, total: int) -> str:
    """Build a dense, one-line chapter status summary."""
    status = result.get("status", "unknown")
    idx = int(result.get("index", seq))
    slug = result.get("slug") or Path(result.get("path", "")).stem or f"chapter-{idx}"
    elapsed_s = float(result.get("elapsed_s", 0.0))
    source_state = result.get("source_state", "-")

    if status == "generated":
        chunks_total = int(result.get("chunks_total", 0))
        chunks_cached = int(result.get("chunks_cached", 0))
        chunks_generated = int(result.get("chunks_generated", 0))
        raw_chars = int(result.get("raw_chars", 0))
        prepared_chars = int(result.get("prepared_chars", 0))
        out_chars = int(result.get("chars", 0))
        return (
            f"[CHAPTER] {seq:02d}/{total:02d} idx={idx:02d} slug={slug} "
            f"status=generated src={source_state} chunks={chunks_total} "
            f"(cache={chunks_cached}, new={chunks_generated}) "
            f"chars={raw_chars:,}->{prepared_chars:,}->{out_chars:,} "
            f"time={_fmt_elapsed_short(elapsed_s)}"
        )
    if status == "cached":
        raw_chars = int(result.get("raw_chars", 0))
        return (
            f"[CHAPTER] {seq:02d}/{total:02d} idx={idx:02d} slug={slug} "
            f"status=cached src={source_state} chars={raw_chars:,} "
            f"time={_fmt_elapsed_short(elapsed_s)}"
        )
    if status == "dry_run":
        raw_chars = int(result.get("raw_chars", 0))
        prepared_chars = int(result.get("prepared_chars", 0))
        return (
            f"[CHAPTER] {seq:02d}/{total:02d} idx={idx:02d} slug={slug} "
            f"status=dry_run src={source_state} "
            f"chars={raw_chars:,}->{prepared_chars:,} time={_fmt_elapsed_short(elapsed_s)}"
        )
    return (
        f"[CHAPTER] {seq:02d}/{total:02d} idx={idx:02d} slug={slug} "
        f"status={status} src={source_state} time={_fmt_elapsed_short(elapsed_s)}"
    )


def _print_timing_summary(step_times: dict[str, float], total_elapsed_s: float) -> None:
    """Print a compact end-of-run timing summary."""
    shown = [(label, secs) for label, secs in step_times.items() if secs > 0.05]
    if not shown:
        return

    print(f"\n{'=' * 60}")
    print("Timing summary")
    print(f"{'=' * 60}")
    width = max(len(label) for label, _ in shown)
    for label, secs in shown:
        print(f"  {label:<{width}}  {_fmt_elapsed_short(secs):>8} ({secs:.1f}s)")
    print(f"  {'-' * (width + 21)}")
    print(f"  {'TOTAL':<{width}}  {_fmt_elapsed_short(total_elapsed_s):>8} ({total_elapsed_s:.1f}s)")


def main() -> int:
    global LLM_PARALLEL_WORKERS, LLM_REQUESTS_PER_MINUTE, LLM_MAX_ATTEMPTS, llm_rate_limiter
    parser = argparse.ArgumentParser(description="Generate audiobook-friendly text from Quarto book chapters")
    parser.add_argument("--config", "-cfg", default=str(DEFAULT_CONFIG_PATH), help=f"Quarto config YAML (default: {DEFAULT_CONFIG_PATH.name})")
    parser.add_argument("--chapter", "-c", type=int, help="Generate only specific chapter number")
    parser.add_argument("--start", type=int, help="Start from chapter number (inclusive)")
    parser.add_argument("--end", type=int, help="End at chapter number (inclusive)")
    parser.add_argument("--list", "-l", action="store_true", help="List all chapters and exit")
    parser.add_argument("--force", "-f", action="store_true", help="Regenerate text even if files exist")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Run programmatic strip only, skip LLM (saves prepared text for review)")
    parser.add_argument("--debug-chunks", action="store_true", help="Verbose per-chunk logs (default is compact chapter summaries)")
    parser.add_argument(
        "--llm-workers",
        type=int,
        default=LLM_PARALLEL_WORKERS,
        help=f"Parallel LLM chunk workers (default: {LLM_PARALLEL_WORKERS})",
    )
    parser.add_argument(
        "--llm-rpm",
        type=int,
        default=LLM_REQUESTS_PER_MINUTE,
        help=f"LLM request cap per minute across all workers (default: {LLM_REQUESTS_PER_MINUTE})",
    )
    parser.add_argument(
        "--llm-max-attempts",
        type=int,
        default=LLM_MAX_ATTEMPTS,
        help=f"Max retries per LLM chunk request (default: {LLM_MAX_ATTEMPTS})",
    )
    parser.add_argument("--variables-yml", default=str(VARIABLES_YML), help=f"Path to variables YAML (default: {VARIABLES_YML.name})")
    args = parser.parse_args()
    pipeline_start = time.monotonic()
    step_times: dict[str, float] = {
        "Load config": 0.0,
        "Load variables": 0.0,
        "Chapter processing": 0.0,
        "Save manifest": 0.0,
    }

    # Apply runtime concurrency/rate settings from CLI.
    LLM_PARALLEL_WORKERS = max(1, args.llm_workers)
    LLM_REQUESTS_PER_MINUTE = max(1, args.llm_rpm)
    LLM_MAX_ATTEMPTS = max(1, args.llm_max_attempts)
    llm_rate_limiter = RateLimiter(max_requests=LLM_REQUESTS_PER_MINUTE, window_seconds=60)

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

    # Point module-level OUTPUT_DIR at config-specific text dir
    global OUTPUT_DIR
    OUTPUT_DIR = paths.narration_txt

    t_sub = time.monotonic()
    _log_info(f"Loading config: {config_path.name} (output: assets/audiobook/{cfg_name}/)")
    config = load_quarto_config(config_path)
    chapters = extract_chapters(config)
    _log_info(f"Found {len(chapters)} chapters")
    step_times["Load config"] = time.monotonic() - t_sub

    variables_path = Path(args.variables_yml)
    if not variables_path.is_absolute():
        variables_path = PROJECT_ROOT / variables_path
    t_sub = time.monotonic()
    _log_info(f"Loading variables: {variables_path.name}")
    variables = load_variables(variables_path)
    _log_info(f"Loaded {len(variables)} variables")
    step_times["Load variables"] = time.monotonic() - t_sub

    if args.list:
        list_chapters(chapters)
        return 0

    if args.chapter:
        chapters = [ch for ch in chapters if ch['index'] == args.chapter]
        if not chapters:
            _log_error(f"Chapter {args.chapter} not found")
            return 1
    elif args.start or args.end:
        start = args.start or 1
        end = args.end or max(ch['index'] for ch in chapters)
        chapters = [ch for ch in chapters if start <= ch['index'] <= end]

    mode = "DRY RUN (strip only)" if args.dry_run else "GENERATE"
    _log_info(f"[{mode}] Processing {len(chapters)} chapter(s)...")
    _log_info(f"Output: {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")
    if not args.dry_run:
        _log_info(
            f"LLM settings: workers={LLM_PARALLEL_WORKERS}, "
            f"rate-cap={LLM_REQUESTS_PER_MINUTE}/min, retries={LLM_MAX_ATTEMPTS}"
        )
    if args.debug_chunks:
        _log_info("Chunk logs: verbose")
    else:
        _log_info("Chunk logs: compact (use --debug-chunks for per-chunk detail)")
    print()

    results = []
    manifest_fields = {"index", "title", "part", "path", "text_file", "chars", "status"}
    total_selected = len(chapters)
    t_sub = time.monotonic()
    for seq, chapter in enumerate(chapters, start=1):
        result = generate_chapter_text(
            chapter,
            variables,
            force=args.force,
            dry_run=args.dry_run,
            debug_chunks=args.debug_chunks,
            seq=seq,
            total=total_selected,
        )
        if result:
            print(_chapter_summary_line(result, seq=seq, total=total_selected))
            results.append({k: v for k, v in result.items() if k in manifest_fields})
    step_times["Chapter processing"] = time.monotonic() - t_sub

    generated = sum(1 for r in results if r['status'] == 'generated')
    cached = sum(1 for r in results if r['status'] == 'cached')
    dry_runs = sum(1 for r in results if r['status'] == 'dry_run')

    _log_info(f"{'=' * 60}")
    _log_info(f"Results: {generated} generated, {cached} cached, {dry_runs} dry-run")

    if results and not args.dry_run:
        t_sub = time.monotonic()
        save_text_results(results, paths=paths)
        step_times["Save manifest"] = time.monotonic() - t_sub

    total_elapsed = time.monotonic() - pipeline_start
    _print_timing_summary(step_times, total_elapsed)
    _log_ok("Done!")
    return 0


if __name__ == "__main__":
    logger = BuildLogger("generate-audiobook-text.log")
    LOGGER = logger
    logger.start_capture()
    exit_code = 0
    try:
        exit_code = main()
    except SystemExit as e:
        if isinstance(e.code, int):
            exit_code = e.code
        elif e.code is None:
            exit_code = 0
        else:
            exit_code = 1
        raise
    except Exception:
        exit_code = 1
        raise
    finally:
        logger.stop_capture()
        logger.close(exit_code)
    sys.exit(exit_code)
