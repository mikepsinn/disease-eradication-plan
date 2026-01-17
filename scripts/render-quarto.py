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
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Set, Dict, Any

import yaml
from dotenv import load_dotenv

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

# Force line buffering for GitHub Actions
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore[union-attr]
    sys.stderr.reconfigure(line_buffering=True)  # type: ignore[union-attr]

# Add scripts/lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from build_logger import BuildLogger  # type: ignore[import-not-found]
from render_utils import (  # type: ignore[import-not-found]
    BuildMonitor,
    create_latex_parser,
    ensure_jupyter_kernel,
    kill_existing_quarto_processes,
    run_pre_validation,
    run_post_validation,
    validate_pdf_for_python_code
)


# =============================================================================
# Pre-Build Functions (formerly in quarto_pre_build.py)
# =============================================================================

def _find_project_root(start_path: Optional[Path] = None) -> Path:
    """Find the project root by looking for package.json or _quarto-book.yml."""
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path).resolve()
    markers = ["package.json", "_quarto-book.yml", "_quarto-economics.yml"]

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

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    dih_render = config.get("dih-render", {})

    return {
        "config_file": config_file,
        "index_source": dih_render.get("index-source"),
        "target_url": dih_render.get("target-url"),
        "description": (
            config.get("book", {}).get("title") or
            config.get("website", {}).get("title") or
            config_name.title()
        ),
        "output_dir": config.get("project", {}).get("output-dir", f"_site/{config_name}"),
        # Read desired output filenames from dih-render section (renamed after build)
        "pdf_output_file": dih_render.get("pdf-output-file"),
        "epub_output_file": dih_render.get("epub-output-file"),
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

    # Clean up existing config-specific directory only
    if build_temp.exists():
        if verbose:
            print(f"[*] Cleaning up existing _build_temp/{config_name}/", flush=True)
        shutil.rmtree(build_temp)

    build_temp.mkdir(parents=True)
    if verbose:
        print(f"[*] Created build directory: _build_temp/{config_name}/", flush=True)

    # Copy project files
    ignore_patterns = {
        "_build_temp", "_site", "_book", ".quarto", "node_modules",
        ".git", "__pycache__", ".venv", ".jupyter_cache",
        # Windows reserved device names
        "nul", "con", "prn", "aux", "com1", "lpt1"
    }

    if verbose:
        print(f"[*] Copying project files to _build_temp/{config_name}/...", flush=True)

    for item in project_root.iterdir():
        if item.name in ignore_patterns or item.name.startswith('.'):
            continue

        dest = build_temp / item.name
        if item.is_dir():
            shutil.copytree(
                item, dest,
                ignore=lambda d, f: {x for x in f if x in ignore_patterns or x.startswith('.')}
            )
        else:
            shutil.copy2(item, dest)

    if verbose:
        print(f"[OK] Copied project files to _build_temp/{config_name}/", flush=True)

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
            # Fallback: create empty _variables.yml
            empty_vars = build_temp / "_variables.yml"
            empty_vars.write_text("# Empty variables for standalone paper build\n", encoding="utf-8")
            if verbose:
                print(f"[*] Created empty _variables.yml (no filtered file found)", flush=True)

    # Use per-paper filtered parameters-and-calculations.qmd if available
    # This ensures the appendix only includes parameters used by this paper.
    # Renamed to canonical name so links from _variables.yml work correctly.
    filtered_params = project_root / "knowledge" / "appendix" / f"parameters-and-calculations-{config_name}.qmd"
    if config_name != "book" and filtered_params.exists():
        target_params = build_temp / "knowledge" / "appendix" / "parameters-and-calculations.qmd"
        shutil.copy2(filtered_params, target_params)
        if verbose:
            print(f"[*] Using filtered parameters: parameters-and-calculations-{config_name}.qmd", flush=True)

    # Prepare config and index in temp directory
    original_cwd = os.getcwd()
    os.chdir(build_temp)
    try:
        if not prepare_config(config_name, verbose=verbose):
            return None
    finally:
        os.chdir(original_cwd)

    # Cross-site link rewriting
    target_url = metadata.get("target_url")
    if not target_url:
        if verbose:
            print("[*] No target-url, skipping cross-site link rewriting", flush=True)
        return build_temp

    target_yml = project_root / "_quarto-book.yml"
    if not target_yml.exists():
        if verbose:
            print("[WARNING] _quarto-book.yml not found, skipping link rewriting", file=sys.stderr)
        return build_temp

    # Parse configs to get file lists
    with open(project_root / metadata["config_file"], encoding="utf-8") as f:
        source_cfg = yaml.safe_load(f)
    with open(target_yml, encoding="utf-8") as f:
        target_cfg = yaml.safe_load(f)

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
    no_browser: bool = False
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

    Returns:
        Exit code (0 for success, non-zero for failure)
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

    try:
        # Start capturing ALL stdout/stderr to log file
        logger.start_capture()

        # Determine if we're rendering PDF (affects timeout and LaTeX parser)
        rendering_pdf = format_override == "pdf" or format_override is None

        os.chdir(project_root)

        # 0. Kill existing processes if requested
        if kill_existing:
            print("=" * 80)
            print("KILLING EXISTING QUARTO/LaTeX PROCESSES")
            print("=" * 80)
            killed = kill_existing_quarto_processes(include_latex=rendering_pdf)
            print(f"[OK] Killed {killed} process(es)" if killed else "[*] No processes found")
            print()

        # 1. Ensure Jupyter kernel exists
        print("=" * 80)
        print("SETUP: JUPYTER KERNEL")
        print("=" * 80)
        if not ensure_jupyter_kernel("dih-project-kernel", "DIH Project"):
            print("[WARNING] Jupyter kernel setup failed, continuing anyway...")
        print()

        # 2. Run pre-validation
        print("=" * 80)
        print("VALIDATION: PRE-RENDER")
        print("=" * 80)
        validation_exit = run_pre_validation()
        if validation_exit != 0:
            print("[ERROR] Pre-validation failed, aborting render", file=sys.stderr)
            return validation_exit
        print()

        # 3. Prepare build directory (always use temp directory for clean builds)
        print("=" * 80)
        print(f"SETUP: PREPARING {description.upper()}")
        print("=" * 80)

        build_temp = prepare_build_temp(config_name, verbose=True)
        if build_temp is None:
            print("[ERROR] Failed to create temp build directory", file=sys.stderr)
            return 1
        os.chdir(build_temp)
        print(f"[*] Changed to temp directory: {build_temp}")
        print()

        # 4. Run Quarto render or preview
        print("=" * 80)
        if preview:
            print(f"PREVIEWING {description.upper()}")
        else:
            print(f"RENDERING {description.upper()}")
        print("=" * 80)

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
            exit_code = monitor.run_build(cmd, build_type=build_type, custom_parsers=custom_parsers)

            # Resume capture for post-build output
            logger.start_capture()

            if exit_code != 0:
                print(f"[ERROR] {description} render failed with exit code {exit_code}", file=sys.stderr)
            else:
                print(f"[OK] {description} render complete!")

        # 5. Post-validation for HTML builds (skip in preview mode)
        # Runs when HTML is rendered (either all formats or html-only)
        if not preview and (format_override is None or format_override == "html") and exit_code == 0:
            print("=" * 80)
            print("VALIDATION: POST-RENDER (HTML)")
            print("=" * 80)
            output_dir = metadata["output_dir"]
            validation_exit = run_post_validation(output_dir=output_dir)
            if validation_exit != 0:
                print("[ERROR] Post-validation failed", file=sys.stderr)
                exit_code = validation_exit
            print()

        # 6. Validate and verify outputs in temp directory (skip in preview mode)
        if not preview and build_temp:
            print("=" * 80)
            print("VALIDATING BUILD OUTPUTS")
            print("=" * 80)

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

            # Validate PDFs for Python code leakage
            for pdf_file in temp_output_dir.glob("*.pdf"):
                size_mb = pdf_file.stat().st_size / (1024 * 1024)
                print(f"[*] PDF: {pdf_file} ({size_mb:.2f} MB)")

                print("=" * 80)
                print("VALIDATION: PDF PYTHON CODE CHECK")
                print("=" * 80)
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

            # Log EPUB files
            for epub_file in temp_output_dir.glob("*.epub"):
                size_mb = epub_file.stat().st_size / (1024 * 1024)
                print(f"[*] EPUB: {epub_file} ({size_mb:.2f} MB)")

            # Verify expected outputs exist
            print("=" * 80)
            print("VERIFICATION: EXPECTED OUTPUTS")
            print("=" * 80)

            # Check PDF if expected
            if expected_pdf and (format_override is None or format_override == "pdf"):
                pdf_path = temp_output_dir / expected_pdf
                if pdf_path.exists():
                    size_mb = pdf_path.stat().st_size / (1024 * 1024)
                    print(f"[OK] PDF exists: {pdf_path} ({size_mb:.2f} MB)")
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
                else:
                    print(f"[ERROR] Expected EPUB not found: {expected_epub}", file=sys.stderr)
                    print(f"        Expected at: {epub_path}", file=sys.stderr)
                    exit_code = 1

            # Check HTML output directory if expected
            if format_override is None or format_override == "html":
                html_index = temp_output_dir / "index.html"
                if html_index.exists():
                    print(f"[OK] HTML exists: {html_index}")
                else:
                    print(f"[ERROR] Expected HTML not found: index.html", file=sys.stderr)
                    print(f"        Expected at: {html_index}", file=sys.stderr)
                    exit_code = 1

            # Print deployment path for GitHub Actions
            print("=" * 80)
            print("DEPLOYMENT INFO")
            print("=" * 80)
            print(f"[*] Deploy from: {temp_output_dir}")
            print(f"[*] Example: publish-dir: '{temp_output_dir.relative_to(project_root)}'")
            print()

        # 7. Run verification tests (test config only, skip in preview mode)
        if not preview and verify and config_name == "test" and exit_code == 0:
            print("=" * 80)
            print("VERIFICATION: PDF LINK TESTS")
            print("=" * 80)
            verify_script = project_root / "scripts" / "test" / "verify-pdf-links.py"
            if verify_script.exists() and build_temp:
                os.chdir(project_root)
                result = subprocess.run([sys.executable, str(verify_script), str(build_temp)], check=False)
                if result.returncode != 0:
                    print("[ERROR] Verification tests failed", file=sys.stderr)
                    exit_code = result.returncode
            else:
                print("[WARNING] Verification script not found", file=sys.stderr)
            print()

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
        choices=["pdf", "html", "epub", "all"],
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
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo sandbox for testing (with --publish)"
    )

    args = parser.parse_args()

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
        no_browser=args.no_browser
    )

    # Publish to Zenodo if requested and render succeeded
    if (args.publish or args.publish_live) and exit_code == 0 and not args.preview:
        exit_code = _publish_to_zenodo(
            config_name=args.config,
            sandbox=args.sandbox,
            draft=not args.publish_live
        )

    sys.exit(exit_code)


def _publish_to_zenodo(config_name: str, sandbox: bool = False, draft: bool = True) -> int:
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
    print("=" * 80)
    print("ZENODO UPLOAD")
    print("=" * 80)

    # Skip test and book configs
    if config_name in ("test", "book"):
        print(f"[--] Skipping Zenodo upload for '{config_name}' config")
        return 0

    # Load .env file if present
    project_root = _find_project_root()
    load_dotenv(project_root / ".env")

    # Get token
    token = get_zenodo_token(sandbox=sandbox)
    if not token:
        env_var = "ZENODO_SANDBOX_TOKEN" if sandbox else "ZENODO_TOKEN"
        print(f"ERROR: {env_var} environment variable not set", file=sys.stderr)
        print(f"  Get token at: https://{'sandbox.' if sandbox else ''}zenodo.org/account/settings/applications/")
        return 1

    # Find project root and config
    project_root = _find_project_root()
    config_file = project_root / f"_quarto-{config_name}.yml"

    if not config_file.exists():
        print(f"ERROR: Config file not found: {config_file}", file=sys.stderr)
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
        return 1

    # Create client and upload
    env_name = "SANDBOX" if sandbox else "PRODUCTION"
    print(f"[*] Zenodo Environment: {env_name}")

    client = ZenodoClient(token, sandbox=sandbox)
    result = upload_paper(
        client=client,
        paper_key=config_name,
        quarto_config=quarto_config,
        pdf_path=pdf_path,
        draft=draft,
        verbose=True
    )

    if result:
        print()
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()
