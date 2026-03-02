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
import argparse
import hashlib
import shutil
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
from lib.retry import retry_with_backoff, RateLimiter

# Configuration
OUTPUT_DIR = NARRATION_DIR

MAX_CHUNK_CHARS = 3_000

# LLM parallelization
LLM_PARALLEL_WORKERS = 4
llm_rate_limiter = RateLimiter(max_requests=15, window_seconds=60)


# ---------------------------------------------------------------------------
# Programmatic stripping (deterministic, easy stuff)
# ---------------------------------------------------------------------------

def strip_qmd_markup(content: str) -> str:
    """
    Strip Quarto/Markdown markup that has no business in an audiobook.
    Keeps prose, tables, lists, and headers as-is for the LLM to handle.
    """
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
    # 1. Resolve variables while syntax is still intact
    text = replace_variables(raw_qmd, variables, highlight_missing=False)
    # Remove any remaining unresolved variable syntax
    text = re.sub(r'\{\{<\s*var\s+\w+\s*>\}\}', '', text)
    # 2. Strip all markup
    text = strip_qmd_markup(text)
    # 3. Split very long lines at sentence boundaries for better TTS prosody
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


def rewrite_for_audiobook(text: str, title: str, output_path: Path) -> str:
    """
    Send pre-processed text to LLM for narration rewrite.
    Saves each chunk to disk as it completes so we can resume after crashes.
    Uses parallel workers for uncached chunks.
    """
    from lib.llm import generate_gemini_flash_content

    chunks = chunk_text(text)
    # Chunks go in the adjacent narration-txt-chunks/ dir, not nested under narration-txt-chapters/
    chunk_dir = output_path.parent.parent / "narration-txt-chunks" / output_path.stem
    chunk_dir.mkdir(parents=True, exist_ok=True)

    total = len(chunks)
    # results[i] holds the rewritten text for chunk i
    results: list[str | None] = [None] * total

    # Collect cached results and build work items for uncached chunks
    work_items = []
    for i, chunk in enumerate(chunks):
        chunk_file = chunk_dir / f"chunk-{i+1:02d}-of-{total:02d}.txt"
        if chunk_file.exists():
            print(f"    [CACHED] chunk {i + 1}/{total} ({chunk_file.stat().st_size:,} bytes)")
            results[i] = chunk_file.read_text(encoding='utf-8')
        else:
            work_items.append((i, chunk, chunk_file))

    if work_items:
        def _rewrite_one(item):
            i, chunk, chunk_file = item
            label = f"chunk {i + 1}/{total}"
            if total > 1:
                context = f"\n\nThis is part {i + 1} of {total} of the chapter \"{title}\". Continue from where the previous part left off."
            else:
                context = f"\n\nThis is the chapter \"{title}\"."
            prompt = AUDIOBOOK_REWRITE_PROMPT + context + "\n\n---\n\nCONTENT TO CONVERT:\n\n" + chunk

            print(f"    [{label}] Calling LLM ({len(chunk):,} chars)...")
            llm_rate_limiter.acquire()
            # Capture prompt in default arg to avoid closure issues
            result = retry_with_backoff(
                lambda p=prompt: generate_gemini_flash_content(p).strip(),
                label=f"{label} ",
            )
            chunk_file.write_text(result, encoding='utf-8')
            print(f"    [{label}] Saved -> {chunk_file.name}")
            return i, result

        workers = min(LLM_PARALLEL_WORKERS, len(work_items))
        print(f"    Rewriting {len(work_items)} chunks ({workers} parallel workers)...")
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_rewrite_one, item): item for item in work_items}
            for future in as_completed(futures):
                i, result = future.result()
                results[i] = result

    return '\n\n'.join(r for r in results if r is not None)


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
) -> dict | None:
    """Generate audiobook text for a single chapter."""
    qmd_path = PROJECT_ROOT / chapter['path']
    if not qmd_path.exists():
        print(f"  [SKIP] File not found: {qmd_path}")
        return None

    title = chapter['title'] or extract_title_from_qmd(qmd_path)

    slug = chapter_slug(chapter)
    output_path = OUTPUT_DIR / f"{slug}.prepared.txt"

    raw_qmd = qmd_path.read_text(encoding='utf-8')

    # Check if source QMD has changed since last generation
    source_hash = hashlib.sha256(raw_qmd.encode('utf-8')).hexdigest()[:16]
    source_hash_file = OUTPUT_DIR / f"{slug}.source_hash"
    if output_path.exists() and not force:
        old_source_hash = source_hash_file.read_text(encoding='utf-8').strip() if source_hash_file.exists() else ''
        if old_source_hash == source_hash:
            print(f"  [SKIP] Source unchanged: {output_path.name}")
            return {
                'index': chapter['index'], 'title': title, 'part': chapter['part'],
                'path': chapter['path'], 'text_file': str(output_path.relative_to(PROJECT_ROOT)),
                'status': 'cached',
            }
        print(f"  [STALE] Source QMD changed (was {old_source_hash or 'unknown'}, now {source_hash}), regenerating")
    original_vars = len(re.findall(r'\{\{<\s*var\s+\w+\s*>\}\}', raw_qmd))

    prepared = prepare_for_narration(raw_qmd, variables)

    # Prepend title and description as spoken episode intro
    intro_parts = []
    if title:
        intro_parts.append(title)
    description = chapter.get('description', '')
    if description:
        intro_parts.append(description)
    if intro_parts:
        prepared = '\n\n'.join(intro_parts) + '\n\n' + prepared

    if not prepared or len(prepared) < 50:
        print(f"  [SKIP] Insufficient content in {qmd_path.name}")
        return None

    remaining_vars = len(re.findall(r'\{\{<\s*var\s+\w+\s*>\}\}', prepared))
    print(f"  Content: {len(raw_qmd):,} -> {len(prepared):,} chars, {original_vars} vars ({original_vars - remaining_vars} resolved)")

    if dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prepared, encoding='utf-8')
        source_hash_file.write_text(source_hash, encoding='utf-8')
        print(f"  [DRY RUN] Prepared text saved to: {output_path.name}")
        return {
            'index': chapter['index'], 'title': title, 'part': chapter['part'],
            'path': chapter['path'], 'text_file': str(output_path.relative_to(PROJECT_ROOT)),
            'status': 'dry_run',
        }

    # Invalidate chunk cache if prepared text has changed
    chunk_dir = output_path.parent.parent / "narration-txt-chunks" / output_path.stem
    hash_file = chunk_dir / ".prepared_hash"
    prepared_hash = hashlib.sha256(prepared.encode('utf-8')).hexdigest()[:16]
    if chunk_dir.exists():
        if force:
            print(f"  [CACHE] Force flag set, clearing chunk cache")
            shutil.rmtree(chunk_dir)
        else:
            old_hash = hash_file.read_text(encoding='utf-8').strip() if hash_file.exists() else ''
            if old_hash != prepared_hash:
                print(f"  [CACHE] Source text changed (was {old_hash or 'unknown'}, now {prepared_hash}), clearing chunk cache")
                shutil.rmtree(chunk_dir)
            else:
                print(f"  [CACHE] Source text unchanged ({prepared_hash}), reusing chunk cache")

    print(f"  Rewriting for audiobook...")
    rewritten = rewrite_for_audiobook(prepared, title, output_path)

    # Save hash for future cache validation
    chunk_dir.mkdir(parents=True, exist_ok=True)
    hash_file.write_text(prepared_hash, encoding='utf-8')

    if not rewritten or len(rewritten) < 50:
        print(f"  [ERROR] LLM returned insufficient content")
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rewritten, encoding='utf-8')
    source_hash_file.write_text(source_hash, encoding='utf-8')
    print(f"  [OK] {output_path.name} ({len(rewritten):,} chars)")

    return {
        'index': chapter['index'], 'title': title, 'part': chapter['part'],
        'path': chapter['path'], 'text_file': str(output_path.relative_to(PROJECT_ROOT)),
        'chars': len(rewritten), 'status': 'generated',
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

def main():
    parser = argparse.ArgumentParser(description="Generate audiobook-friendly text from Quarto book chapters")
    parser.add_argument("--config", "-cfg", default=str(DEFAULT_CONFIG_PATH), help=f"Quarto config YAML (default: {DEFAULT_CONFIG_PATH.name})")
    parser.add_argument("--chapter", "-c", type=int, help="Generate only specific chapter number")
    parser.add_argument("--start", type=int, help="Start from chapter number (inclusive)")
    parser.add_argument("--end", type=int, help="End at chapter number (inclusive)")
    parser.add_argument("--list", "-l", action="store_true", help="List all chapters and exit")
    parser.add_argument("--force", "-f", action="store_true", help="Regenerate text even if files exist")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Run programmatic strip only, skip LLM (saves prepared text for review)")
    parser.add_argument("--variables-yml", default=str(VARIABLES_YML), help=f"Path to variables YAML (default: {VARIABLES_YML.name})")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    cfg_name = config_name_from_path(config_path)
    paths = get_paths(cfg_name)

    # Point module-level OUTPUT_DIR at config-specific text dir
    global OUTPUT_DIR
    OUTPUT_DIR = paths.narration_txt

    print(f"Loading config: {config_path.name} (output: assets/audiobook/{cfg_name}/)")
    config = load_quarto_config(config_path)
    chapters = extract_chapters(config)
    print(f"Found {len(chapters)} chapters")

    variables_path = Path(args.variables_yml)
    if not variables_path.is_absolute():
        variables_path = PROJECT_ROOT / variables_path
    print(f"Loading variables: {variables_path.name}")
    variables = load_variables(variables_path)
    print(f"Loaded {len(variables)} variables")

    if args.list:
        list_chapters(chapters)
        return

    if args.chapter:
        chapters = [ch for ch in chapters if ch['index'] == args.chapter]
        if not chapters:
            print(f"Error: Chapter {args.chapter} not found")
            sys.exit(1)
    elif args.start or args.end:
        start = args.start or 1
        end = args.end or max(ch['index'] for ch in chapters)
        chapters = [ch for ch in chapters if start <= ch['index'] <= end]

    mode = "DRY RUN (strip only)" if args.dry_run else "GENERATE"
    print(f"\n[{mode}] Processing {len(chapters)} chapter(s)...")
    print(f"Output: {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")
    print()

    results = []
    for chapter in chapters:
        qmd_path = PROJECT_ROOT / chapter['path']
        title = chapter['title'] or (extract_title_from_qmd(qmd_path) if qmd_path.exists() else chapter['path'])
        print(f"\n[{chapter['index']}/{chapters[-1]['index']}] {title}")
        result = generate_chapter_text(chapter, variables, force=args.force, dry_run=args.dry_run)
        if result:
            results.append(result)

    generated = sum(1 for r in results if r['status'] == 'generated')
    cached = sum(1 for r in results if r['status'] == 'cached')
    dry_runs = sum(1 for r in results if r['status'] == 'dry_run')

    print(f"\n{'=' * 60}")
    print(f"Results: {generated} generated, {cached} cached, {dry_runs} dry-run")

    if results and not args.dry_run:
        save_text_results(results, paths=paths)

    print("\nDone!")


if __name__ == "__main__":
    main()
