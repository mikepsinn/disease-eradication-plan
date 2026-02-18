#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render Quarto Config
====================

Unified script to render or preview any Quarto configuration. Configuration is
data-driven from dih-render sections in _quarto-*.yml files.

Features:
- Automatic cross-site link rewriting (QMD links to book chapters become absolute URLs)
- Build monitoring with timeout detection (prevents hung CI builds)
- Real-time progress tracking and profiling
- PDF validation for Python code leakage
- Live preview mode with hot reload

Usage:
    python render-quarto.py economics                # Render economics (all formats)
    python render-quarto.py wishocracy               # Render wishocracy (all formats)
    python render-quarto.py iab                      # Render IAB (all formats)
    python render-quarto.py test --verify            # Render test config with verification
    python render-quarto.py economics --to pdf       # Render only PDF format
    python render-quarto.py economics --to html      # Render only HTML format
    python render-quarto.py book --timeout 1800      # Custom timeout (30 min)
    python render-quarto.py book --kill-existing     # Kill stale Quarto processes first
    python render-quarto.py economics --preview      # Preview with live reload
    python render-quarto.py book --preview --port 4200  # Preview on custom port
"""

import argparse
import gc
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Set, Dict, Any

from dih_models.yaml_utils import load_quarto_config

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

# Force line buffering for GitHub Actions
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore[union-attr]
    sys.stderr.reconfigure(line_buffering=True)  # type: ignore[union-attr]

# Add project root and scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from build_logger import BuildLogger  # type: ignore[import-not-found]
from python_utils import load_project_dotenv  # type: ignore[import-not-found]
from render_utils import (  # type: ignore[import-not-found]
    BuildMonitor,
    create_latex_parser,
    ensure_jupyter_kernel,
    kill_existing_quarto_processes,
    print_latex_errors,
    run_pre_validation,
    run_post_validation,
    run_pdf_validation,
    validate_pdf_for_python_code
)


# =============================================================================
# epubcheck auto-download
# =============================================================================

EPUBCHECK_VERSION = "5.1.0"
EPUBCHECK_URL = f"https://github.com/w3c/epubcheck/releases/download/v{EPUBCHECK_VERSION}/epubcheck-{EPUBCHECK_VERSION}.zip"


def ensure_epubcheck(project_root: Path) -> Optional[Path]:
    """Download epubcheck if not present. Returns path to jar or None on failure."""
    jar = project_root / "tools" / f"epubcheck-{EPUBCHECK_VERSION}" / "epubcheck.jar"
    if jar.exists():
        return jar

    tools_dir = project_root / "tools"
    tools_dir.mkdir(exist_ok=True)
    zip_path = tools_dir / f"epubcheck-{EPUBCHECK_VERSION}.zip"

    print(f"[*] Downloading epubcheck {EPUBCHECK_VERSION}...")
    try:
        urllib.request.urlretrieve(EPUBCHECK_URL, str(zip_path))
    except Exception as e:
        print(f"[WARN] Failed to download epubcheck: {e}", file=sys.stderr)
        return None

    print(f"[*] Extracting epubcheck...")
    try:
        with zipfile.ZipFile(str(zip_path), "r") as zf:
            zf.extractall(str(tools_dir))
    except Exception as e:
        print(f"[WARN] Failed to extract epubcheck: {e}", file=sys.stderr)
        return None
    finally:
        zip_path.unlink(missing_ok=True)

    if jar.exists():
        print(f"[OK] epubcheck installed at {jar}")
        return jar

    print(f"[WARN] epubcheck jar not found after extraction", file=sys.stderr)
    return None


# =============================================================================
# GitHub Actions Log Grouping
# =============================================================================

# Detect if running in GitHub Actions
IN_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"


def gh_group_start(title: str) -> None:
    """Start a collapsible group in GitHub Actions logs."""
    if IN_GITHUB_ACTIONS:
        print(f"::group::{title}", flush=True)
    print("=" * 80, flush=True)
    print(title, flush=True)
    print("=" * 80, flush=True)


def gh_group_end() -> None:
    """End a collapsible group in GitHub Actions logs."""
    if IN_GITHUB_ACTIONS:
        print("::endgroup::", flush=True)
    print(flush=True)


# =============================================================================
# Pre-Build Functions (formerly in quarto_pre_build.py)
# =============================================================================

def rmtree_with_retry(path: Path, max_retries: int = 5, delay: float = 1.0, verbose: bool = True) -> bool:
    """
    Remove a directory tree with retries for Windows file locking issues.

    Tries multiple strategies:
    1. Simple rmtree with retries and delays
    2. Force garbage collection to release file handles
    3. Kill any Python/Quarto processes that might be locking files
    4. On Windows, use robocopy for directories with very long paths
    """
    if not path.exists():
        return True

    # On Windows, try robocopy trick for long paths first
    # robocopy /MIR with an empty dir effectively deletes everything
    if sys.platform == 'win32':
        try:
            import tempfile
            with tempfile.TemporaryDirectory() as empty_dir:
                result = subprocess.run(
                    ['robocopy', empty_dir, str(path), '/MIR', '/R:0', '/W:0'],
                    capture_output=True,
                    timeout=60
                )
                # robocopy returns 0-7 for success, 8+ for errors
                if result.returncode < 8:
                    # Now remove the empty directory
                    try:
                        path.rmdir()
                    except Exception:
                        pass
                    if not path.exists():
                        return True
        except Exception:
            pass  # Fall through to normal rmtree

    for attempt in range(max_retries):
        try:
            # Force garbage collection to release any file handles
            gc.collect()
            shutil.rmtree(path)
            return True
        except (PermissionError, OSError) as e:
            if attempt < max_retries - 1:
                if verbose:
                    print(f"[WARN] Directory removal issue (attempt {attempt + 1}/{max_retries}), retrying in {delay}s...", flush=True)

                # On Windows, try to kill processes that might be locking the directory
                if sys.platform == 'win32' and attempt >= 2:
                    if verbose:
                        print("[*] Attempting to kill locking processes...", flush=True)
                    try:
                        # Kill any stale Python/Quarto processes, but never kill
                        # the current process or its direct parent (e.g. batch uploader).
                        our_pid = os.getpid()
                        parent_pid = os.getppid()
                        protected_pids = {our_pid}
                        if parent_pid:
                            protected_pids.add(parent_pid)
                        protected_expr = ",".join(str(pid) for pid in sorted(protected_pids))
                        result = subprocess.run(
                            ['powershell', '-Command',
                             f'$protected=@({protected_expr}); '
                             f'Get-Process python*, quarto* -ErrorAction SilentlyContinue | '
                             f'Where-Object {{ $protected -notcontains $_.Id }} | '
                             f'Stop-Process -Force -ErrorAction SilentlyContinue'],
                            capture_output=True,
                            timeout=10
                        )
                    except Exception:
                        pass  # Ignore errors from process killing

                time.sleep(delay)
                delay *= 1.5  # Exponential backoff
            else:
                if verbose:
                    print(f"[WARN] Failed to fully remove {path}, continuing anyway: {e}", flush=True)
                # Don't raise - just continue, the directory might be partially cleaned
                return False
    return False


def _find_project_root(start_path: Optional[Path] = None) -> Path:
    """Find the project root by looking for package.json or _quarto-manual.yml."""
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path).resolve()
    markers = ["package.json", "_quarto-manual.yml", "_quarto-1-pct-treaty-impact.yml"]

    for path in [current] + list(current.parents):
        for marker in markers:
            if (path / marker).exists():
                return path

    return current


def _extract_files_from_config(config: dict) -> Set[str]:
    """Extract list of QMD files from a Quarto config dictionary."""
    files: Set[str] = set()

    def extract_chapters(items: Any) -> None:
        if not isinstance(items, list):
            return
        for item in items:
            if isinstance(item, str):
                files.add(item)
            elif isinstance(item, dict):
                if "href" in item:
                    files.add(item["href"])
                if "chapters" in item:
                    extract_chapters(item["chapters"])
                if "contents" in item:
                    extract_chapters(item["contents"])

    # Book format
    if "chapters" in config.get("book", {}):
        extract_chapters(config["book"]["chapters"])

    # Website format
    for item in config.get("project", {}).get("render", []):
        if isinstance(item, str):
            files.add(item)

    return files


def _build_paper_url_mapping(project_root: Path) -> Dict[str, str]:
    """
    Build mapping from standalone paper QMD paths to their deployed HTTPS URLs.

    Reads all _quarto-*.yml configs and extracts:
    - dih-render.index-source -> the QMD file path
    - website.site-url -> the deployed URL

    Returns:
        Dict mapping QMD path (e.g., 'knowledge/appendix/optimocracy-paper.qmd')
        to site URL (e.g., 'https://optimocracy.warondisease.org')
    """
    # Skip these config types (not standalone papers)
    skip_configs = {"manual", "book", "test", "base", "shared-defaults"}

    mapping = {}

    for config_path in project_root.glob("_quarto-*.yml"):
        if "_build_temp" in str(config_path):
            continue

        key = config_path.stem.replace("_quarto-", "")
        if key in skip_configs or not key:
            continue

        try:
            config = load_quarto_config(config_path)
        except Exception:
            continue

        if not config:
            continue

        # Get index-source from dih-render
        dih_render = config.get("dih-render", {})
        index_source = dih_render.get("index-source")
        if not index_source:
            continue

        # Get site-url from website section
        site_url = config.get("website", {}).get("site-url")
        if not site_url:
            site_url = config.get("book", {}).get("site-url")

        if not site_url:
            continue

        # Normalize: remove trailing slash from URL
        site_url = site_url.rstrip("/")
        mapping[index_source] = site_url

    return mapping


def _rewrite_paper_links(
    build_temp: Path,
    project_root: Path,
    current_config_source: Optional[str],
    files_to_process: List[str],
    verbose: bool = True
) -> int:
    """
    Rewrite links to standalone paper QMD files with their deployed HTTPS URLs.

    Args:
        build_temp: Path to the temp build directory
        project_root: Path to the project root
        current_config_source: The index-source of the current config (to avoid self-links)
        files_to_process: List of QMD files to process
        verbose: Whether to print status messages

    Returns:
        Number of links rewritten
    """
    mapping = _build_paper_url_mapping(project_root)
    if not mapping:
        return 0

    # Remove self-reference from mapping (a paper shouldn't link to its own URL)
    if current_config_source and current_config_source in mapping:
        mapping = {k: v for k, v in mapping.items() if k != current_config_source}

    if not mapping:
        return 0

    links_rewritten = 0

    for file_path_str in files_to_process:
        qmd_file = build_temp / file_path_str
        if not qmd_file.exists():
            continue

        with open(qmd_file, encoding="utf-8") as f:
            content = f.read()

        original = content

        def rewrite_paper_link(match: re.Match[str]) -> str:
            nonlocal links_rewritten
            text, full_path = match.group(1), match.group(2)

            # Skip external links
            if full_path.startswith(("http://", "https://", "#", "mailto:")):
                return match.group(0)

            # Skip non-QMD links
            if ".qmd" not in full_path:
                return match.group(0)

            # Split path and anchor
            if "#" in full_path:
                path_part, anchor = full_path.split("#", 1)
                anchor = "#" + anchor
            else:
                path_part = full_path
                anchor = ""

            # Normalize path
            path_normalized = path_part.replace("\\", "/")

            # Try to match against our mapping
            for qmd_path, site_url in mapping.items():
                qmd_filename = Path(qmd_path).name

                # Match if:
                # 1. Full path matches exactly
                # 2. Path ends with the QMD path
                # 3. Just the filename matches (for same-directory links)
                if (path_normalized == qmd_path or
                    path_normalized.endswith("/" + qmd_path) or
                    path_normalized.endswith(qmd_filename) or
                    Path(path_normalized).name == qmd_filename):

                    new_url = site_url + "/" + anchor if anchor else site_url
                    if verbose:
                        print(f"    {file_path_str}: {full_path} -> {new_url}")
                    links_rewritten += 1
                    return f"[{text}]({new_url})"

            return match.group(0)

        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite_paper_link, content)

        if content != original:
            with open(qmd_file, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)

    return links_rewritten


def get_config_metadata(config_name: str) -> Dict[str, Any]:
    """
    Read build configuration from dih-render section of a Quarto config file.

    Args:
        config_name: Name of configuration (economics, wishocracy, iab, test, book)

    Returns:
        Dictionary with: config_file, index_source, target_url, description, output_dir,
                        pdf_output_file, epub_output_file
    """
    project_root = _find_project_root()
    config_file = f"_quarto-{config_name}.yml"
    config_path = project_root / config_file

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    config = load_quarto_config(config_path)

    dih_render = config.get("dih-render", {})
    pdf_output_file = dih_render.get("pdf-output-file")
    epub_output_file = dih_render.get("epub-output-file")

    # Fallback to format output-file when dih-render doesn't provide names.
    if not pdf_output_file:
        pdf_output_file = config.get("format", {}).get("pdf", {}).get("output-file")
    if not epub_output_file:
        epub_output_file = config.get("format", {}).get("epub", {}).get("output-file")

    return {
        "config_file": config_file,
        "index_source": dih_render.get("index-source"),
        "target_url": dih_render.get("fallback-404-redirect-domain"),
        "description": (
            config.get("book", {}).get("title") or
            config.get("website", {}).get("title") or
            config_name.title()
        ),
        "output_dir": config.get("project", {}).get("output-dir", f"_site/{config_name}"),
        # Read desired output filenames from dih-render, then format.* fallback.
        "pdf_output_file": pdf_output_file,
        "epub_output_file": epub_output_file,
        # Whether to show "(95% CI: ...)" in variable display values (default: True)
        "show_confidence_intervals": dih_render.get("show-confidence-intervals", True),
        # How to handle <a> links on parameter values (default: "html" = keep raw tags)
        # Options: "html" (keep raw <a> tags), "markdown" (convert to [text](path.qmd)),
        #          "none" (strip to plain text)
        "parameter_link_format": dih_render.get("parameter-link-format", "html"),
    }


def prepare_config(config_name: str, verbose: bool = True) -> bool:
    """
    Prepare for rendering: copy config to _quarto.yml, copy/transform index.qmd.

    Args:
        config_name: Name of configuration (economics, wishocracy, iab, test, book)
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()

    try:
        metadata = get_config_metadata(config_name)
    except FileNotFoundError as e:
        if verbose:
            print(f"[ERROR] {e}", file=sys.stderr)
        return False

    # Copy config file to _quarto.yml
    config_src = project_root / metadata["config_file"]
    config_dst = project_root / "_quarto.yml"

    if verbose:
        print(f"[*] Copying {metadata['config_file']} -> _quarto.yml", flush=True)

    shutil.copy2(config_src, config_dst)

    # Copy and transform index file if specified
    index_source = metadata["index_source"]
    if not index_source:
        return True

    source_path = project_root / index_source
    target_path = project_root / "index.qmd"

    if not source_path.exists():
        if verbose:
            print(f"[ERROR] Missing {index_source}", file=sys.stderr)
        return False

    if verbose:
        print(f"[*] Copying {index_source} -> index.qmd", flush=True)

    with open(source_path, encoding="utf-8") as f:
        content = f.read()

    # Calculate path depth for transformation
    source_parts = Path(index_source).parts
    depth = len(source_parts) - 1  # Exclude filename
    source_dir = ""

    if depth > 0:
        source_dir = "/".join(source_parts[:-1])

        # Replace relative paths from deepest to shallowest
        for i in range(depth, 0, -1):
            pattern = "../" * i
            replacement = "" if i == depth else "/".join(source_parts[:depth - i]) + "/"
            content = content.replace(pattern, replacement)

    # Use per-paper filtered bibliography if available (fixes all-refs-in-PDF issue)
    # This ensures standalone paper PDFs only include cited references.
    # The filtered bib now includes citations from both:
    # 1. Direct [@key] citations in the QMD
    # 2. Citations embedded in used variable values (data-source-ref attributes)
    filtered_bib = project_root / f"references-{config_name}.bib"
    if filtered_bib.exists() and config_name != "book":
        # Replace bibliography path in frontmatter with filtered version
        # Matches: bibliography:\n  - path or bibliography: path
        bib_pattern = r'(bibliography:\s*\n\s*-\s*)[^\n]+'
        content = re.sub(bib_pattern, f'\\1references-{config_name}.bib', content)
        if verbose:
            print(f"[*] Using filtered bibliography: references-{config_name}.bib", flush=True)
        # Transform same-directory links
        root_dirs = ["assets/", "scripts/", "dih_models/", "brain/", "references.bib"]

        def fix_same_dir_link(match: re.Match[str]) -> str:
            text, path = match.group(1), match.group(2)

            # Skip URLs, anchors, absolute paths, already-transformed paths
            if (path.startswith(("http://", "https://", "mailto:", "#", "/")) or
                "://" in path or
                ("/" in path and not path.startswith("./")) or
                any(path.startswith(d) for d in root_dirs)):
                return match.group(0)

            # Add source directory prefix
            new_path = source_dir + "/" + (path[2:] if path.startswith("./") else path)
            return f"[{text}]({new_path})"

        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", fix_same_dir_link, content)
    elif verbose:
        print(f"[*] Using full references.bib (book config or no filtered file)", flush=True)

    with open(target_path, "w", encoding="utf-8", newline='\n') as f:
        f.write(content)

    return True


def _strip_confidence_intervals(variables_path: Path, verbose: bool = True) -> int:
    """
    Strip "(95% CI: ...)" text from variable display values in _variables.yml.

    Removes CI ranges from both display text and title/tooltip attributes so
    general-audience builds (book, EPUB) show clean numbers without uncertainty
    ranges. Academic paper builds keep CIs by not calling this function.

    Args:
        variables_path: Path to _variables.yml in the build temp directory.
        verbose: Whether to print status messages.

    Returns:
        Number of CI occurrences stripped.
    """
    if not variables_path.exists():
        return 0

    with open(variables_path, encoding="utf-8") as f:
        content = f.read()

    original = content
    stripped = 0

    # Strip CI from display text: " (95% CI: $10.5M-$19.5M)" or " (95% CI: 8 years-18 years)"
    # Pattern: space, open paren, "95% CI: ", content up to closing paren
    content, n = re.subn(r' \(95% CI: [^)]+\)', '', content)
    stripped += n

    # Strip CI from title attributes: "| 95% CI: [$78, $100] |" or "| 95% CI: [8 years, 18 years] |"
    # Keep the surrounding pipes clean (remove leading pipe + CI + trailing pipe, leave one pipe)
    content, n = re.subn(r' \| 95% CI: \[[^\]]*\]', '', content)
    stripped += n

    if content != original:
        with open(variables_path, "w", encoding="utf-8", newline='\n') as f:
            f.write(content)

    if verbose:
        if stripped > 0:
            print(f"[OK] Stripped {stripped} confidence intervals from _variables.yml", flush=True)
        else:
            print("[*] No confidence intervals found to strip", flush=True)

    return stripped


def _convert_parameter_links(variables_path: Path, mode: str = "markdown", verbose: bool = True) -> int:
    """
    Convert or strip parameter link HTML in _variables.yml.

    Modes:
        "markdown": Convert <a class="parameter-link"> tags to markdown links
                    with .qmd extensions so Quarto resolves them per-format.
                    Strips <span> wrappers to plain text (no link to convert).
        "none":     Strip all HTML wrappers to plain display text.

    Examples (markdown mode):
        <a href="/path.html#sec-x" class="parameter-link" ...>$89</a>
            → [$89](/path.qmd#sec-x)
        <span class="parameter-definition" ...>1,750</span>
            → 1,750

    Args:
        variables_path: Path to _variables.yml in the build temp directory.
        mode: "markdown" to convert links, "none" to strip entirely.
        verbose: Whether to print status messages.

    Returns:
        Number of tags converted/stripped.
    """
    if not variables_path.exists():
        return 0

    with open(variables_path, encoding="utf-8") as f:
        content = f.read()

    original = content
    n = 0

    if mode == "markdown":
        # Convert <a class="parameter-link" href="...">text</a> → [text](path.qmd#sec-...)
        # In raw YAML, double-quoted strings escape internal quotes as \" (backslash + quote)
        def _a_to_markdown(match: re.Match[str]) -> str:
            tag = match.group(0)
            text = match.group(1)
            href_match = re.search(r'href=\\"([^"\\]+)\\"', tag)
            if href_match:
                href = href_match.group(1).replace('.html', '.qmd')
                return f'[{text}]({href})'
            return text

        content, n1 = re.subn(
            r'<a\s[^>]*class=\\"parameter-link\\"[^>]*>(.*?)</a>',
            _a_to_markdown,
            content
        )
        n += n1
    else:
        # mode == "none": strip <a> tags to plain text
        content, n1 = re.subn(
            r'<a\s[^>]*class=\\"parameter-link\\"[^>]*>(.*?)</a>',
            r'\1',
            content
        )
        n += n1

    # Strip <span class="parameter-definition" ...>text</span> → text (no link to convert)
    content, n2 = re.subn(
        r'<span\s[^>]*class=\\"parameter-definition\\"[^>]*>(.*?)</span>',
        r'\1',
        content
    )
    n += n2

    # Strip <span class="parameter-link" ...>text</span> → text (constants like DAYS_PER_YEAR)
    content, n3 = re.subn(
        r'<span\s[^>]*class=\\"parameter-link\\"[^>]*>(.*?)</span>',
        r'\1',
        content
    )
    n += n3

    if content != original:
        with open(variables_path, "w", encoding="utf-8", newline='\n') as f:
            f.write(content)

    if verbose:
        action = "Converted" if mode == "markdown" else "Stripped"
        if n > 0:
            print(f"[OK] {action} {n} parameter links in _variables.yml", flush=True)
        else:
            print("[*] No parameter links found to process", flush=True)

    return n


def prepare_build_temp(config_name: str, verbose: bool = True) -> Optional[Path]:
    """
    Create temp build directory with cross-site link rewriting.

    Copies project to _build_temp/{config_name}/, rewrites links to book chapters
    as absolute URLs. Config-specific subfolders enable parallel builds.

    Args:
        config_name: Name of configuration (economics, wishocracy, iab, test, book)
        verbose: Whether to print status messages

    Returns:
        Path to temp build directory, or None if failed
    """
    project_root = _find_project_root()

    try:
        metadata = get_config_metadata(config_name)
    except FileNotFoundError as e:
        if verbose:
            print(f"[ERROR] {e}", file=sys.stderr)
        return None

    # Create config-specific temp directory (enables parallel builds)
    build_temp_root = project_root / "_build_temp"
    build_temp = build_temp_root / config_name

    # Clean up existing config-specific directory only (with retry for Windows locking)
    if build_temp.exists():
        if verbose:
            print(f"[*] Cleaning up existing _build_temp/{config_name}/", flush=True)
        success = rmtree_with_retry(build_temp, verbose=verbose)
        # Verify directory was actually deleted - crash if not
        if build_temp.exists():
            print(f"[ERROR] Failed to delete _build_temp/{config_name}/ - directory still exists", file=sys.stderr)
            print(f"        Try manually deleting: rm -rf _build_temp/{config_name}", file=sys.stderr)
            return None

    build_temp.mkdir(parents=True)
    if verbose:
        print(f"[*] Created build directory: _build_temp/{config_name}/", flush=True)

    # Whitelist approach: only copy what's needed for Quarto builds
    # This prevents cache pollution and ensures clean builds
    required_dirs = {"assets", "knowledge", "dih_models"}
    required_file_patterns = {
        "_quarto",      # _quarto*.yml configs
        "_variables",   # _variables*.yml
        "references",   # references*.bib
        "index",        # index*.qmd
    }
    required_extensions = {".css", ".tex", ".csl", ".png", ".ico", ".toml"}
    required_files = {"dfda-logo.png", "favicon.ico", "pyproject.toml", "netlify.toml"}

    # Ignore patterns for subdirectories (e.g., __pycache__ inside dih_models)
    subdir_ignore = {"__pycache__", ".git", "node_modules", ".venv"}

    # LaTeX build artifacts that should never be copied into the build temp directory.
    # Root-level .tex files (LaTeX templates) are still copied via the required_extensions path.
    build_artifact_extensions = {".tex", ".log", ".aux", ".out", ".toc", ".fls", ".fdb_latexmk", ".synctex.gz"}

    # On Windows, skip files with paths that would exceed MAX_PATH (260 chars)
    extra_path_len = len(str(build_temp)) - len(str(project_root))
    max_path_len = (250 - extra_path_len) if sys.platform == 'win32' else 4096

    def should_ignore(directory: str, files: List[str]) -> Set[str]:
        ignored = set()
        for f in files:
            if f in subdir_ignore or f.startswith('.'):
                ignored.add(f)
            elif os.path.splitext(f)[1] in build_artifact_extensions:
                ignored.add(f)
            elif len(os.path.join(directory, f)) > max_path_len:
                ignored.add(f)
        return ignored

    if verbose:
        print(f"[*] Copying project files to _build_temp/{config_name}/...", flush=True)

    copied_count = 0
    for item in project_root.iterdir():
        dest = build_temp / item.name

        # Copy required directories
        if item.is_dir() and item.name in required_dirs:
            shutil.copytree(item, dest, ignore=should_ignore)
            copied_count += 1
            continue

        # Skip other directories and hidden files
        if item.is_dir() or item.name.startswith('.'):
            continue

        # Copy files matching patterns (e.g., _quarto-manual.yml, references-economics.bib)
        if any(item.name.startswith(pat) for pat in required_file_patterns):
            shutil.copy2(item, dest)
            copied_count += 1
            continue

        # Copy files with required extensions
        if item.suffix in required_extensions or item.name in required_files:
            shutil.copy2(item, dest)
            copied_count += 1

    if verbose:
        print(f"[OK] Copied {copied_count} items to _build_temp/{config_name}/", flush=True)

    # Use per-paper filtered _variables.yml if available (generated by paper_bibliography_generator)
    # This ensures citeproc only sees citations embedded in variables that are actually used.
    # Falls back to empty _variables.yml if no filtered file exists.
    filtered_vars = project_root / f"_variables-{config_name}.yml"
    if config_name != "book":
        if filtered_vars.exists():
            # Copy filtered variables file to build directory
            target_vars = build_temp / "_variables.yml"
            shutil.copy2(filtered_vars, target_vars)
            if verbose:
                print(f"[*] Using filtered variables: _variables-{config_name}.yml", flush=True)
        else:
            # Fallback: use the main _variables.yml (all variables available)
            main_vars = project_root / "_variables.yml"
            target_vars = build_temp / "_variables.yml"
            if main_vars.exists():
                shutil.copy2(main_vars, target_vars)
                if verbose:
                    print(f"[*] Using main _variables.yml (no filtered file found)", flush=True)
            else:
                raise FileNotFoundError(
                    f"No _variables.yml found. Run: python scripts/generate-everything-parameters-variables-calculations-references.py"
                )

    # Strip confidence intervals from _variables.yml if config says so
    if not metadata.get("show_confidence_intervals", True):
        target_vars = build_temp / "_variables.yml"
        _strip_confidence_intervals(target_vars, verbose=verbose)

    # Convert or strip <a> wrappers from parameter values based on config
    link_format = metadata.get("parameter_link_format", "html")
    if link_format != "html":
        target_vars = build_temp / "_variables.yml"
        _convert_parameter_links(target_vars, mode=link_format, verbose=verbose)

    # Use per-paper filtered parameters-and-calculations.qmd if available
    # This ensures the appendix only includes parameters used by this paper.
    # Renamed to canonical name so links from _variables.yml work correctly.
    # Config files reference the canonical name (parameters-and-calculations.qmd),
    # and this copy ensures the filtered content is used instead of the full master file.
    filtered_params = project_root / "knowledge" / "appendix" / f"parameters-and-calculations-{config_name}.qmd"
    if config_name != "book" and filtered_params.exists():
        target_params = build_temp / "knowledge" / "appendix" / "parameters-and-calculations.qmd"
        shutil.copy2(filtered_params, target_params)
        if verbose:
            print(f"[*] Using filtered parameters: parameters-and-calculations-{config_name}.qmd", flush=True)

    # Copy Lua filters referenced in configs (scripts/ dir is not in required_dirs whitelist)
    filters_src = project_root / "scripts" / "filters"
    if filters_src.is_dir():
        filters_dst = build_temp / "scripts" / "filters"
        filters_dst.mkdir(parents=True, exist_ok=True)
        for lua_file in filters_src.glob("*.lua"):
            shutil.copy2(lua_file, filters_dst / lua_file.name)

    # Prepare config and index in temp directory
    original_cwd = os.getcwd()
    os.chdir(build_temp)
    try:
        if not prepare_config(config_name, verbose=verbose):
            return None
    finally:
        os.chdir(original_cwd)

    # Rewrite links to standalone papers with their deployed HTTPS URLs
    # This runs for all configs (not just manual) to fix "Unable to resolve link target" warnings
    current_cfg = load_quarto_config(project_root / metadata["config_file"])
    current_files = _extract_files_from_config(current_cfg)
    paper_files_to_process = list(current_files)
    if (build_temp / "index.qmd").exists():
        paper_files_to_process.append("index.qmd")

    if verbose:
        print(f"[*] Rewriting links to standalone papers with HTTPS URLs...", flush=True)

    paper_links_rewritten = _rewrite_paper_links(
        build_temp=build_temp,
        project_root=project_root,
        current_config_source=metadata.get("index_source"),
        files_to_process=paper_files_to_process,
        verbose=verbose
    )

    if paper_links_rewritten > 0 and verbose:
        print(f"[OK] Rewrote {paper_links_rewritten} paper links to HTTPS URLs", flush=True)

    # Cross-site link rewriting
    target_url = metadata.get("target_url")
    if not target_url:
        if verbose:
            print("[*] No fallback-404-redirect-domain, skipping cross-site link rewriting", flush=True)
        return build_temp

    target_yml = project_root / "_quarto-manual.yml"
    if not target_yml.exists():
        if verbose:
            print("[WARNING] _quarto-manual.yml not found, skipping link rewriting", file=sys.stderr)
        return build_temp

    # Parse configs to get file lists
    source_cfg = load_quarto_config(project_root / metadata["config_file"])
    target_cfg = load_quarto_config(target_yml)

    source_files = _extract_files_from_config(source_cfg)
    target_files = _extract_files_from_config(target_cfg)

    if verbose:
        print(f"[*] Preprocessing QMD links in _build_temp/{config_name}/", flush=True)

    links_rewritten = 0
    files_modified = 0

    # Process source files + index.qmd
    files_to_process = list(source_files)
    if (build_temp / "index.qmd").exists():
        files_to_process.append("index.qmd")

    for file_path_str in files_to_process:
        qmd_file = build_temp / file_path_str
        if not qmd_file.exists():
            continue

        with open(qmd_file, encoding="utf-8") as f:
            content = f.read()

        original = content

        def rewrite_link(match: re.Match[str]) -> str:
            nonlocal links_rewritten
            text, path = match.group(1), match.group(2)

            # Skip external/anchor links
            if path.startswith(("http://", "https://", "#", "mailto:")) or ".qmd" not in path:
                return match.group(0)

            # Resolve relative path
            if path.startswith("/"):
                resolved = os.path.normpath(path[1:]).replace("\\", "/")
            elif path.startswith(("../", "./")):
                file_dir = qmd_file.relative_to(build_temp).parent
                resolved = os.path.normpath(os.path.join(str(file_dir), path)).replace("\\", "/")
            else:
                resolved = path

            # Handle anchors
            anchor = ""
            if "#" in resolved:
                resolved, anchor = resolved.split("#", 1)
                anchor = f"#{anchor}"

            # Rewrite if in target but not in source
            if resolved in target_files and resolved not in source_files:
                new_url = f"{target_url}/{resolved.replace('.qmd', '.html')}{anchor}"
                if verbose:
                    print(f"[*] {file_path_str}: {path} -> {new_url}")
                links_rewritten += 1
                return f"[{text}]({new_url})"

            return match.group(0)

        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite_link, content)

        if content != original:
            with open(qmd_file, "w", encoding="utf-8", newline='\n') as f:
                f.write(content)
            files_modified += 1

    if verbose:
        if links_rewritten > 0:
            print(f"[OK] Preprocessed {files_modified} files, rewrote {links_rewritten} links", flush=True)
        else:
            print("[*] No links needed rewriting", flush=True)

    return build_temp


# =============================================================================
# Main Render Functions
# =============================================================================

def get_available_configs() -> List[str]:
    """Discover available configs from _quarto-*.yml files."""
    project_root = Path(__file__).parent.parent
    configs = []
    for yml in project_root.glob("_quarto-*.yml"):
        name = yml.stem.replace("_quarto-", "")
        configs.append(name)
    return sorted(configs)


def render_quarto(
    config_name: str,
    format_override: Optional[str] = None,
    verify: bool = False,
    quarto_args: Optional[list] = None,
    timeout: int = 900,
    log_file: Optional[str] = None,
    fail_on_warnings: bool = True,
    kill_existing: bool = False,
    preview: bool = False,
    port: Optional[int] = None,
    host: Optional[str] = None,
    no_browser: bool = False,
    skip_validation: bool = False
) -> int:
    """
    Render or preview Quarto configuration.

    Args:
        config_name: Name of configuration (economics, wishocracy, iab, test, book)
        format_override: Override format (pdf, html, or None for all formats in config)
        verify: Run verification tests after rendering (test config only)
        quarto_args: Additional arguments to pass to quarto render/preview
        timeout: Seconds with no output before killing build (default: 900 = 15min)
        log_file: Path to log file (default: build-{config}.log)
        fail_on_warnings: Whether to fail build on warnings (default: True)
        kill_existing: Kill existing Quarto/LaTeX processes before starting
        preview: Run in preview mode with live reload instead of rendering
        port: Port for preview server (preview mode only)
        host: Host for preview server (preview mode only)
        no_browser: Do not open browser automatically (preview mode only)
        skip_validation: Skip PDF validation steps (Python code check and LLM validation)

    Returns:
        Exit code (0 for success, non-zero for failure)

    Note:
        If Quarto fails but HTML was generated, validation and deployment will
        proceed. The job will still fail at the end with the original exit code.
    """
    project_root = Path(__file__).parent.parent.absolute()
    original_cwd = os.getcwd()

    # Get config metadata from YAML
    try:
        metadata = get_config_metadata(config_name)
    except FileNotFoundError:
        print(f"[ERROR] Unknown config: {config_name}", file=sys.stderr)
        print(f"        Available: {', '.join(get_available_configs())}", file=sys.stderr)
        return 1

    description = metadata["description"]

    # Create logger that writes to both console and log file
    log_file_name = log_file or f"build-{config_name}.log"
    logger = BuildLogger(log_file_name)

    # Write build metadata to log
    if logger.log_handle:
        logger.log_handle.write(f"Config: {config_name}\n")
        logger.log_handle.write(f"Format: {format_override or 'all'}\n")
        logger.log_handle.write("=" * 80 + "\n\n")
        logger.log_handle.flush()

    exit_code = 0
    build_temp = None
    monitor = None
    quarto_exit_code = 0  # Track original Quarto exit code
    html_can_deploy = False  # Track if HTML deployment should proceed despite PDF failure

    try:
        # Start capturing ALL stdout/stderr to log file
        logger.start_capture()

        # Determine if we're rendering PDF (affects timeout and LaTeX parser)
        rendering_pdf = format_override == "pdf" or format_override is None

        os.chdir(project_root)

        # 0. Kill existing processes if requested
        if kill_existing:
            gh_group_start("KILLING EXISTING QUARTO/LaTeX PROCESSES")
            killed = kill_existing_quarto_processes(include_latex=rendering_pdf)
            print(f"[OK] Killed {killed} process(es)" if killed else "[*] No processes found")
            gh_group_end()

        # 1. Ensure Jupyter kernel exists
        gh_group_start("SETUP: JUPYTER KERNEL")
        if not ensure_jupyter_kernel("dih-project-kernel", "DIH Project"):
            print("[WARNING] Jupyter kernel setup failed, continuing anyway...")
        gh_group_end()

        # 2. Run pre-validation
        gh_group_start("VALIDATION: PRE-RENDER")
        validation_exit = run_pre_validation()
        if validation_exit != 0:
            print("[ERROR] Pre-validation failed, aborting render", file=sys.stderr)
            gh_group_end()
            return validation_exit
        gh_group_end()

        # 3. Prepare build directory (always use temp directory for clean builds)
        gh_group_start(f"SETUP: PREPARING {description.upper()}")

        build_temp = prepare_build_temp(config_name, verbose=True)
        if build_temp is None:
            print("[ERROR] Failed to create temp build directory", file=sys.stderr)
            gh_group_end()
            return 1
        os.chdir(build_temp)
        print(f"[*] Changed to temp directory: {build_temp}")

        # Strip chart includes for EPUB/DOCX builds.
        # Quarto processes {{< include >}} shortcodes before content-visible
        # filters, so charts hidden by unless-format divs still get rendered.
        if format_override in ("epub", "docx"):
            params_qmd = build_temp / "knowledge" / "appendix" / "parameters-and-calculations.qmd"
            if params_qmd.exists():
                text = params_qmd.read_text(encoding="utf-8")
                text = re.sub(r'\{\{< include \.\./figures/.*?\.qmd >\}\}\n?', '', text)
                params_qmd.write_text(text, encoding="utf-8", newline='\n')
                print(f"[*] Stripped chart includes from parameters page ({format_override.upper()})")

        gh_group_end()

        # 4. Run Quarto render or preview
        render_title = f"PREVIEWING {description.upper()}" if preview else f"RENDERING {description.upper()} ({format_override or 'all formats'})"
        gh_group_start(render_title)

        if preview:
            # Preview mode - run quarto preview directly
            cmd = ["quarto", "preview"]
            if port:
                cmd.extend(["--port", str(port)])
            if host:
                cmd.extend(["--host", host])
            if no_browser:
                cmd.append("--no-browser")
            if quarto_args:
                cmd.extend(quarto_args)

            print(f"[*] Command: {' '.join(cmd)}")
            print()

            try:
                subprocess.run(cmd, check=True)
                exit_code = 0
            except KeyboardInterrupt:
                print("\n[*] Preview server stopped")
                exit_code = 0
            except subprocess.CalledProcessError as e:
                exit_code = e.returncode
            gh_group_end()
        else:
            # Render mode - use build monitor
            cmd = ["quarto", "render"]
            if format_override:
                cmd.extend(["--to", format_override])
            if quarto_args:
                cmd.extend(quarto_args)

            # Stop capture before BuildMonitor (it has its own logging)
            logger.stop_capture()

            # Create build monitor (appends to existing log file)
            effective_timeout = max(timeout, 900) if rendering_pdf else timeout
            monitor = BuildMonitor(
                timeout_seconds=effective_timeout,
                fail_on_warnings=fail_on_warnings,
                log_file=str(logger.log_path)
            )

            custom_parsers = [create_latex_parser()] if rendering_pdf else []
            build_type = f"{description} ({format_override or 'all formats'})"
            quarto_exit_code = monitor.run_build(cmd, build_type=build_type, custom_parsers=custom_parsers)
            exit_code = quarto_exit_code

            # Resume capture for post-build output
            logger.start_capture()

            if exit_code != 0:
                print(f"[ERROR] {description} render failed with exit code {exit_code}", file=sys.stderr)
                # Extract and display LaTeX errors from log files
                if build_temp and rendering_pdf:
                    gh_group_start("LATEX ERROR DETAILS")
                    print_latex_errors(str(build_temp))
                    gh_group_end()

                # Check if HTML exists despite Quarto failure - deploy HTML anyway
                if build_temp:
                    html_index = build_temp / metadata["output_dir"] / "index.html"
                    if html_index.exists():
                        print(f"[WARN] Quarto failed but HTML exists at {html_index}", file=sys.stderr)
                        print(f"[WARN] Continuing with HTML validation and deployment...", file=sys.stderr)
                        html_can_deploy = True
                        exit_code = 0  # Temporarily allow validation/deployment to proceed
            else:
                print(f"[OK] {description} render complete!")
            gh_group_end()

        # 5. Post-validation for HTML builds (skip in preview mode)
        # Runs when HTML is rendered (either all formats or html-only)
        if not preview and (format_override is None or format_override == "html") and exit_code == 0:
            gh_group_start("VALIDATION: POST-RENDER (HTML)")
            output_dir = metadata["output_dir"]
            validation_exit = run_post_validation(output_dir=output_dir)
            if validation_exit != 0:
                print("[ERROR] Post-validation failed", file=sys.stderr)
                exit_code = validation_exit
            gh_group_end()

        # 6. Validate and verify outputs in temp directory (skip in preview mode)
        # Skip if build already failed - no point validating broken/missing outputs
        if not preview and build_temp and exit_code == 0:
            gh_group_start("VALIDATING BUILD OUTPUTS")

            # Determine output directory in temp build folder
            temp_output_dir = build_temp / metadata["output_dir"]

            # Rename PDFs in temp folder to match config output-file
            expected_pdf = metadata.get("pdf_output_file")
            if expected_pdf:
                for pdf_file in temp_output_dir.glob("*.pdf"):
                    if pdf_file.name != expected_pdf:
                        new_path = pdf_file.parent / expected_pdf
                        print(f"[*] Renaming {pdf_file.name} -> {expected_pdf}")
                        pdf_file.rename(new_path)

            # Rename EPUBs in temp folder to match config output-file
            expected_epub = metadata.get("epub_output_file")
            if expected_epub:
                for epub_file in temp_output_dir.glob("*.epub"):
                    if epub_file.name != expected_epub:
                        new_path = epub_file.parent / expected_epub
                        print(f"[*] Renaming {epub_file.name} -> {expected_epub}")
                        epub_file.rename(new_path)
            gh_group_end()  # End VALIDATING BUILD OUTPUTS

            # Validate PDFs for Python code leakage
            for pdf_file in temp_output_dir.glob("*.pdf"):
                size_mb = pdf_file.stat().st_size / (1024 * 1024)
                print(f"[*] PDF: {pdf_file} ({size_mb:.2f} MB)")

                if skip_validation:
                    print("[SKIP] PDF Python code check (--skip-validation)")
                else:
                    gh_group_start("VALIDATION: PDF PYTHON CODE CHECK")
                    found_issues, issues = validate_pdf_for_python_code(str(pdf_file))
                    if found_issues:
                        print("[ERROR] PDF validation failed: Python code detected!", file=sys.stderr)
                        for issue in issues[:5]:
                            safe = issue.encode("ascii", errors="replace").decode("ascii")
                            print(f"  {safe}", file=sys.stderr)
                        if len(issues) > 5:
                            print(f"  ... and {len(issues) - 5} more", file=sys.stderr)
                        exit_code = 1
                    else:
                        print("[OK] PDF validation passed")
                    gh_group_end()

            # Log EPUB files
            for epub_file in temp_output_dir.glob("*.epub"):
                size_mb = epub_file.stat().st_size / (1024 * 1024)
                print(f"[*] EPUB: {epub_file} ({size_mb:.2f} MB)")

            # Verify expected outputs exist
            gh_group_start("VERIFICATION: EXPECTED OUTPUTS")

            # Check PDF if expected
            if expected_pdf and (format_override is None or format_override == "pdf"):
                pdf_path = temp_output_dir / expected_pdf
                if pdf_path.exists():
                    size_mb = pdf_path.stat().st_size / (1024 * 1024)
                    print(f"[OK] PDF exists: {pdf_path} ({size_mb:.2f} MB)")

                    # Copy PDF to assets/pdfs for distribution
                    assets_pdfs_dir = project_root / "assets" / "pdfs"
                    assets_pdfs_dir.mkdir(parents=True, exist_ok=True)
                    dest_pdf_path = assets_pdfs_dir / expected_pdf
                    shutil.copy2(pdf_path, dest_pdf_path)
                    print(f"[OK] Copied PDF to: {dest_pdf_path.relative_to(project_root)}")

                    # Run comprehensive PDF validation (LLM if GEMINI key available)
                    if skip_validation:
                        print("[SKIP] Comprehensive PDF validation (--skip-validation)")
                    else:
                        gh_group_start("VALIDATION: COMPREHENSIVE PDF CHECK")
                        pdf_validation_exit = run_pdf_validation(
                            str(dest_pdf_path),
                            skip_url_check=True,  # URLs already checked in post-validation
                        )
                        if pdf_validation_exit != 0:
                            print("[ERROR] Comprehensive PDF validation failed", file=sys.stderr)
                            exit_code = pdf_validation_exit
                        gh_group_end()
                else:
                    print(f"[ERROR] Expected PDF not found: {expected_pdf}", file=sys.stderr)
                    print(f"        Expected at: {pdf_path}", file=sys.stderr)
                    exit_code = 1

            # Check EPUB if expected
            if expected_epub and (format_override is None or format_override == "epub"):
                epub_path = temp_output_dir / expected_epub
                if epub_path.exists():
                    size_mb = epub_path.stat().st_size / (1024 * 1024)
                    print(f"[OK] EPUB exists: {epub_path} ({size_mb:.2f} MB)")

                    # Post-process EPUB for e-reader compatibility
                    validate_epub_script = project_root / "scripts" / "validate-epub.py"
                    if validate_epub_script.exists():
                        print(f"[*] Post-processing EPUB for e-reader compatibility...")
                        fix_result = subprocess.run(
                            [sys.executable, "-u", str(validate_epub_script), "--fix", str(epub_path)],
                            cwd=str(project_root),
                        )
                        if fix_result.returncode != 0:
                            print(f"[WARN] EPUB validation found issues (exit code {fix_result.returncode})", file=sys.stderr)

                    # Copy EPUB to assets/epubs for distribution
                    assets_epubs_dir = project_root / "assets" / "epubs"
                    assets_epubs_dir.mkdir(parents=True, exist_ok=True)
                    dest_epub_path = assets_epubs_dir / expected_epub
                    shutil.copy2(epub_path, dest_epub_path)
                    print(f"[OK] Copied EPUB to: {dest_epub_path.relative_to(project_root)}")

                    # Fix EPUB for Kindle compatibility (resize oversized images, fix DPI, compress)
                    fix_kindle_script = project_root / "scripts" / "fix-epub-kindle.py"
                    kindle_epub_name = expected_epub.replace(".epub", "-kindle.epub")
                    dest_kindle_path = assets_epubs_dir / kindle_epub_name
                    if fix_kindle_script.exists():
                        print(f"[*] Generating Kindle-compatible EPUB...")
                        kindle_result = subprocess.run(
                            [sys.executable, "-u", str(fix_kindle_script), str(dest_epub_path), "-o", str(dest_kindle_path)],
                            cwd=str(project_root),
                        )
                        if kindle_result.returncode != 0:
                            print(f"[WARN] Kindle EPUB fix encountered issues (exit code {kindle_result.returncode})", file=sys.stderr)
                        elif dest_kindle_path.exists():
                            kindle_mb = dest_kindle_path.stat().st_size / (1024 * 1024)
                            print(f"[OK] Kindle EPUB: {dest_kindle_path.relative_to(project_root)} ({kindle_mb:.2f} MB)")

                    # Validate Kindle compatibility
                    validate_kindle_script = project_root / "scripts" / "validate-kindle-compat.py"
                    kindle_target = dest_kindle_path if dest_kindle_path.exists() else dest_epub_path
                    if validate_kindle_script.exists():
                        print(f"[*] Validating Kindle compatibility...")
                        validate_result = subprocess.run(
                            [sys.executable, "-u", str(validate_kindle_script), str(kindle_target)],
                            cwd=str(project_root),
                            capture_output=True, text=True,
                        )
                        if validate_result.returncode != 0:
                            # Extract just the error lines for concise output
                            for line in validate_result.stdout.splitlines():
                                if "[ERROR]" in line:
                                    print(f"  {line.strip()}", file=sys.stderr)
                            print(f"[WARN] Kindle validation found {validate_result.stdout.count('[ERROR]')} error(s)", file=sys.stderr)
                        else:
                            print(f"[OK] Kindle validation passed")

                    # Run epubcheck for EPUB spec compliance (catches issues KDP rejects)
                    epubcheck_jar = ensure_epubcheck(project_root)
                    if epubcheck_jar:
                        epubcheck_target = dest_kindle_path if dest_kindle_path.exists() else dest_epub_path
                        print(f"[*] Running epubcheck on {epubcheck_target.name}...")
                        epubcheck_result = subprocess.run(
                            ["java", "-jar", str(epubcheck_jar), str(epubcheck_target)],
                            capture_output=True, text=True, encoding="utf-8",
                        )
                        # Count fatals and errors from stderr (epubcheck outputs there)
                        output = epubcheck_result.stderr or epubcheck_result.stdout or ""
                        fatal_count = output.count("FATAL(")
                        error_count = output.count("ERROR(")
                        warning_count = output.count("WARNING(")
                        if fatal_count > 0 or error_count > 0:
                            print(f"[WARN] epubcheck: {fatal_count} fatal, {error_count} errors, {warning_count} warnings", file=sys.stderr)
                            for line in output.splitlines():
                                if line.startswith("FATAL(") or line.startswith("ERROR("):
                                    print(f"  {line.strip()[:150]}", file=sys.stderr)
                        else:
                            print(f"[OK] epubcheck passed ({warning_count} warnings)")
                else:
                    print(f"[ERROR] Expected EPUB not found: {expected_epub}", file=sys.stderr)
                    print(f"        Expected at: {epub_path}", file=sys.stderr)
                    exit_code = 1

            # Check DOCX if it exists (no expected_docx config field, just look for .docx files)
            if format_override is None or format_override == "docx":
                # Look for DOCX files in output directory
                docx_files = list(temp_output_dir.glob("*.docx"))
                if docx_files:
                    for docx_path in docx_files:
                        size_mb = docx_path.stat().st_size / (1024 * 1024)
                        print(f"[OK] DOCX exists: {docx_path} ({size_mb:.2f} MB)")

                        # Copy DOCX to assets/docx for distribution
                        assets_docx_dir = project_root / "assets" / "docx"
                        assets_docx_dir.mkdir(parents=True, exist_ok=True)
                        dest_docx_path = assets_docx_dir / docx_path.name
                        shutil.copy2(docx_path, dest_docx_path)
                        print(f"[OK] Copied DOCX to: {dest_docx_path.relative_to(project_root)}")

                        # Validate DOCX images (check for oversized images that break Word)
                        analyze_docx_script = project_root / "scripts" / "analyze-docx-images.py"
                        if analyze_docx_script.exists():
                            print(f"[*] Validating DOCX images...")
                            result = subprocess.run(
                                [sys.executable, str(analyze_docx_script), str(dest_docx_path)],
                                capture_output=True, text=True, encoding="utf-8"
                            )
                            if result.returncode != 0:
                                print(f"[WARNING] DOCX has oversized images (may cause Word 22-inch limit errors)")
                                print(f"          Run: npm run images:normalize-dpi:apply")
                                print(f"          Then re-render to fix")
                                # Print just the summary lines
                                for line in result.stdout.splitlines():
                                    if "ISSUES FOUND" in line or "WORD_OVERSIZE" in line:
                                        print(f"          {line.strip()}")
                            else:
                                print(f"[OK] DOCX image validation passed")

            # Check HTML output directory if expected
            if format_override is None or format_override == "html":
                html_index = temp_output_dir / "index.html"
                if html_index.exists():
                    print(f"[OK] HTML exists: {html_index}")
                else:
                    print(f"[ERROR] Expected HTML not found: index.html", file=sys.stderr)
                    print(f"        Expected at: {html_index}", file=sys.stderr)
                    exit_code = 1
            gh_group_end()  # End VERIFICATION: EXPECTED OUTPUTS

            # Print deployment path for GitHub Actions
            gh_group_start("DEPLOYMENT INFO")
            print(f"[*] Deploy from: {temp_output_dir}")
            print(f"[*] Example: publish-dir: '{temp_output_dir.relative_to(project_root)}'")
            gh_group_end()

        # 7. Run verification tests (test config only, skip in preview mode)
        if not preview and verify and config_name == "test" and exit_code == 0:
            gh_group_start("VERIFICATION: PDF LINK TESTS")
            verify_script = project_root / "scripts" / "test" / "verify-pdf-links.py"
            if verify_script.exists() and build_temp:
                os.chdir(project_root)
                result = subprocess.run([sys.executable, str(verify_script), str(build_temp)], check=False)
                if result.returncode != 0:
                    print("[ERROR] Verification tests failed", file=sys.stderr)
                    exit_code = result.returncode
            else:
                print("[WARNING] Verification script not found", file=sys.stderr)
            gh_group_end()

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Subprocess failed: {e.returncode}", file=sys.stderr)
        exit_code = e.returncode
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {e}", file=sys.stderr)
        print("        Make sure Quarto is installed and in your PATH", file=sys.stderr)
        exit_code = 1
    except KeyboardInterrupt:
        print("\n[*] Build interrupted by user", file=sys.stderr)
        exit_code = 130
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        exit_code = 1
    finally:
        os.chdir(original_cwd)

        # Note: Temp directory (_build_temp/) is NOT cleaned up automatically
        # - In CI: GitHub Actions runner is destroyed after job completes
        # - Locally: Run `git clean -fdx _build_temp/` to clean up manually

        # Close BuildMonitor's log handle
        if monitor and hasattr(monitor, 'log_handle') and monitor.log_handle:
            try:
                monitor.log_handle.close()
            except Exception:
                pass

        # Stop capture and close logger (writes footer automatically)
        logger.stop_capture()
        logger.close(exit_code)

    # Restore original exit code if PDF/EPUB failed but HTML was deployed
    if html_can_deploy and quarto_exit_code != 0:
        print(f"[ERROR] PDF/EPUB generation failed (exit code {quarto_exit_code}) - job will report failure", file=sys.stderr)
        print(f"[INFO] HTML was successfully deployed to Netlify", file=sys.stderr)
        exit_code = quarto_exit_code

    return exit_code


def main():
    available = get_available_configs()

    parser = argparse.ArgumentParser(
        description="Render Quarto configuration with build monitoring and validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "config",
        choices=available,
        help=f"Configuration to render: {', '.join(available)}"
    )
    parser.add_argument(
        "--to",
        choices=["pdf", "html", "epub", "docx", "all"],
        default=None,
        help="Format to render (default: all formats in config)"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run verification tests after rendering (test config only)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Seconds with no output before killing build (default: 900)"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Log file path (default: build-{config}.log)"
    )
    parser.add_argument(
        "--no-fail-on-warnings",
        action="store_true",
        help="Do not fail build on warnings"
    )
    parser.add_argument(
        "--kill-existing",
        action="store_true",
        help="Kill existing Quarto/LaTeX processes before starting"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Run in preview mode with live reload instead of rendering"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port for preview server (preview mode only)"
    )
    parser.add_argument(
        "--host",
        type=str,
        help="Host for preview server (preview mode only)"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open browser automatically (preview mode only)"
    )
    parser.add_argument(
        "quarto_args",
        nargs="*",
        help="Additional arguments to pass to quarto render/preview"
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip PDF validation steps (Python code check and comprehensive LLM validation)"
    )

    # Zenodo publishing options
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Upload PDF to Zenodo after rendering (as draft by default)"
    )
    parser.add_argument(
        "--publish-live",
        action="store_true",
        help="Upload and publish to Zenodo (assigns DOI immediately)"
    )

    args = parser.parse_args()

    # Force-selecting PDF output is disabled because several multi-file website
    # configs can fail with Quarto output-file path validation in this mode.
    if args.to == "pdf":
        print(
            "[ERROR] '--to pdf' is disabled for render-quarto.py. "
            "Render with config defaults (omit --to) instead.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Run the render
    exit_code = render_quarto(
        config_name=args.config,
        format_override=None if args.to == "all" else args.to,
        verify=args.verify,
        quarto_args=args.quarto_args,
        timeout=args.timeout,
        log_file=args.log_file,
        fail_on_warnings=not args.no_fail_on_warnings,
        kill_existing=args.kill_existing,
        preview=args.preview,
        port=args.port,
        host=args.host,
        no_browser=args.no_browser,
        skip_validation=args.skip_validation
    )

    # Publish to Zenodo if requested and render succeeded
    if (args.publish or args.publish_live) and exit_code == 0 and not args.preview:
        exit_code = _publish_to_zenodo(
            config_name=args.config,
            draft=not args.publish_live
        )

    sys.exit(exit_code)


def _publish_to_zenodo(config_name: str, draft: bool = True) -> int:
    """
    Upload rendered PDF to Zenodo.

    Returns exit code (0 for success, 1 for failure).
    """
    from lib.zenodo_client import (
        ZenodoClient,
        get_zenodo_token,
        load_quarto_config,
        upload_paper,
    )

    print()
    gh_group_start("ZENODO UPLOAD")

    # Skip test and book configs
    if config_name in ("test", "book"):
        print(f"[--] Skipping Zenodo upload for '{config_name}' config")
        gh_group_end()
        return 0

    # Load .env file if present
    project_root = _find_project_root()
    load_project_dotenv(project_root)

    # Get token
    token = get_zenodo_token()
    if not token:
        print("ERROR: ZENODO_TOKEN environment variable not set", file=sys.stderr)
        print("  Get token at: https://zenodo.org/account/settings/applications/")
        gh_group_end()
        return 1

    # Find project root and config
    project_root = _find_project_root()
    config_file = project_root / f"_quarto-{config_name}.yml"

    if not config_file.exists():
        print(f"ERROR: Config file not found: {config_file}", file=sys.stderr)
        gh_group_end()
        return 1

    # Load config and find PDF path
    quarto_config = load_quarto_config(config_file)
    dih_render = quarto_config.get("dih-render", {})

    # Get PDF filename
    pdf_filename = dih_render.get("pdf-output-file")
    if not pdf_filename:
        format_config = quarto_config.get("format", {})
        pdf_config = format_config.get("pdf", {})
        pdf_filename = pdf_config.get("output-file", f"{config_name}-paper.pdf")

    # Build PDF path
    pdf_path = project_root / f"_build_temp/{config_name}/_site/{config_name}/{pdf_filename}"

    if not pdf_path.exists():
        print(f"ERROR: PDF not found at {pdf_path}", file=sys.stderr)
        print("  Build may have failed or PDF output is disabled", file=sys.stderr)
        gh_group_end()
        return 1

    # Create client and upload
    print("[*] Zenodo Environment: PRODUCTION")

    client = ZenodoClient(token)
    result = upload_paper(
        client=client,
        paper_key=config_name,
        quarto_config=quarto_config,
        pdf_path=pdf_path,
        draft=draft,
        verbose=True
    )

    gh_group_end()
    if result:
        print()
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()
