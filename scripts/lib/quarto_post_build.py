#!/usr/bin/env python3
"""
Quarto Post-Build Processing
=============================

Post-render processing for Quarto multi-site builds:
- Fix PDF locations (move misplaced PDFs to correct directories)
- Rewrite HTML links (economics → book as absolute URLs)
- Clean up and validate rendered output
"""

import re
import shutil
import sys
import yaml
from pathlib import Path
from typing import Optional, Set


def _find_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find the project root by looking for package.json or _quarto-book.yml.

    Args:
        start_path: Path to start searching from (default: current working directory)

    Returns:
        Path to project root

    Raises:
        FileNotFoundError: If project root cannot be found
    """
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path).resolve()

    # Look for project root markers
    markers = ["package.json", "_quarto-book.yml", "_quarto-economics.yml"]

    # Walk up the directory tree
    for path in [current] + list(current.parents):
        for marker in markers:
            if (path / marker).exists():
                return path

    # If we can't find markers, assume we're already at root
    return current


def _extract_files_from_config(config: dict, verbose: bool = False) -> Set[str]:
    """
    Extract list of files from a Quarto config dictionary.

    Args:
        config: Parsed YAML config dictionary
        verbose: Whether to print status messages

    Returns:
        Set of file paths in the config
    """
    files = set()

    def extract_chapters(items):
        """Recursively extract chapter files from nested structure."""
        if not isinstance(items, list):
            return

        for item in items:
            if isinstance(item, str):
                files.add(item)
            elif isinstance(item, dict):
                # Handle 'href' key (direct file reference)
                if "href" in item:
                    files.add(item["href"])
                # Handle 'chapters' key (nested chapters)
                if "chapters" in item:
                    extract_chapters(item["chapters"])
                # Handle 'contents' key (sidebar contents)
                if "contents" in item:
                    extract_chapters(item["contents"])

    # Try book.chapters first (book format)
    book_config = config.get("book", {})
    if "chapters" in book_config:
        extract_chapters(book_config["chapters"])

    # Try project.render (other formats)
    render_list = config.get("project", {}).get("render", [])
    for item in render_list:
        if isinstance(item, str):
            files.add(item)

    if verbose:
        print(f"[*] Found {len(files)} files in config", flush=True)

    return files


def _extract_economics_files(verbose: bool = False) -> Set[str]:
    """
    Extract list of files from _quarto-economics.yml.

    Args:
        verbose: Whether to print status messages

    Returns:
        Set of file paths (relative to project root) in economics render

    Raises:
        FileNotFoundError: If _quarto-economics.yml not found
    """
    project_root = _find_project_root()
    economics_yml = project_root / "_quarto-economics.yml"

    if not economics_yml.exists():
        raise FileNotFoundError(f"Missing {economics_yml}")

    try:
        with open(economics_yml, encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return _extract_files_from_config(config, verbose)
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to parse _quarto-economics.yml: {e}", file=sys.stderr)
        raise


def _extract_book_files(verbose: bool = False) -> Set[str]:
    """
    Extract list of files from _quarto-book.yml.

    Args:
        verbose: Whether to print status messages

    Returns:
        Set of file paths (relative to project root) in book render

    Raises:
        FileNotFoundError: If _quarto-book.yml not found
    """
    project_root = _find_project_root()
    book_yml = project_root / "_quarto-book.yml"

    if not book_yml.exists():
        raise FileNotFoundError(f"Missing {book_yml}")

    try:
        with open(book_yml, encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return _extract_files_from_config(config, verbose)
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to parse _quarto-book.yml: {e}", file=sys.stderr)
        raise


def postprocess_html_links(
    build_dir: str,
    source_config: str,
    target_config: str = "_quarto-book.yml",
    target_url: str = "https://manual.WarOnDisease.org",
    verbose: bool = True
) -> bool:
    """
    Post-process rendered HTML files to rewrite cross-site links as absolute URLs.

    This runs AFTER quarto render completes, so source .qmd files remain untouched.
    Rewrites links to files that are in target config but NOT in source config.

    Args:
        build_dir: Path to rendered HTML output directory (relative to project root)
        source_config: Path to source Quarto config (e.g., "_quarto-economics.yml")
        target_config: Path to target Quarto config (default: "_quarto-book.yml")
        target_url: Base URL of the target site
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    try:
        project_root = _find_project_root()
        build_path = project_root / build_dir

        if not build_path.exists():
            if verbose:
                print(f"[ERROR] Build directory not found: {build_dir}", file=sys.stderr)
            return False

        # Get list of files from both configs
        source_yml = project_root / source_config
        target_yml = project_root / target_config

        if not source_yml.exists():
            if verbose:
                print(f"[ERROR] Source config not found: {source_config}", file=sys.stderr)
            return False

        if not target_yml.exists():
            if verbose:
                print(f"[WARNING] Target config not found: {target_config}, skipping link rewriting", file=sys.stderr)
            return True

        # Extract file lists from configs
        try:
            with open(source_yml, encoding="utf-8") as f:
                source_cfg = yaml.safe_load(f)
            with open(target_yml, encoding="utf-8") as f:
                target_cfg = yaml.safe_load(f)
        except Exception as e:
            if verbose:
                print(f"[ERROR] Failed to parse config files: {e}", file=sys.stderr)
            return False

        # Extract files from both configs using existing helper
        source_files = _extract_files_from_config(source_cfg, verbose=False)
        target_files = _extract_files_from_config(target_cfg, verbose=False)

        # Convert to .html paths
        source_html = {f.replace(".qmd", ".html") for f in source_files}
        target_html = {f.replace(".qmd", ".html") for f in target_files}

        # Find all HTML files in build directory
        html_files = list(build_path.rglob("*.html"))

        links_rewritten = 0
        files_modified = 0

        for html_file in html_files:
            try:
                with open(html_file, encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                # Find all <a href="..."> tags
                def rewrite_link(match):
                    nonlocal links_rewritten

                    full_match = match.group(0)
                    href = match.group(1)

                    # Skip external links and anchors
                    if href.startswith(("http://", "https://", "#", "mailto:")):
                        return full_match

                    # Only process .qmd links (may have anchor like file.qmd#section)
                    if ".qmd" not in href:
                        return full_match

                    # Resolve relative path to absolute (from build root perspective)
                    if href.startswith("../") or href.startswith("./"):
                        # Get this HTML file's path relative to build directory
                        html_rel = html_file.relative_to(build_path)
                        html_dir = html_rel.parent
                        # Resolve the link relative to this file's directory
                        resolved_qmd = (html_dir / href).as_posix()
                        # Normalize path (resolve ..)
                        from pathlib import PurePosixPath
                        resolved_qmd = str(PurePosixPath(resolved_qmd))
                    else:
                        resolved_qmd = href

                    # Remove .qmd extension and any anchor
                    anchor = ""
                    if "#" in resolved_qmd:
                        resolved_qmd, anchor = resolved_qmd.split("#", 1)
                        anchor = f"#{anchor}"

                    # Convert to .html for target lookups
                    resolved_html = resolved_qmd.replace(".qmd", ".html")

                    # Check if this link should be rewritten
                    # Rewrite if: in target but NOT in source
                    if resolved_qmd in target_files and resolved_qmd not in source_files:
                        new_url = f"{target_url}/{resolved_html}{anchor}"
                        if verbose:
                            print(f"[*] Rewriting: {href} -> {new_url}")
                        links_rewritten += 1
                        return f'<a href="{new_url}"'

                    # Otherwise, convert .qmd to .html (keep as relative link)
                    new_href = resolved_html + anchor
                    if new_href != href:
                        links_rewritten += 1
                        return f'<a href="{new_href}"'

                    return full_match

                # Replace all <a href="..."> tags
                content = re.sub(r'<a href="([^"]+)"', rewrite_link, content)

                # Only write if content changed
                if content != original_content:
                    with open(html_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    files_modified += 1

            except Exception as e:
                if verbose:
                    print(f"[WARNING] Failed to process {html_file.name}: {e}", file=sys.stderr)
                continue

        if verbose:
            if links_rewritten > 0:
                print(f"[OK] Post-processed {files_modified} HTML files, rewrote {links_rewritten} links")
            else:
                print(f"[*] No links needed rewriting")

        return True

    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to post-process HTML: {e}", file=sys.stderr)
        return False


def postprocess_pdf(
    build_dir: str,
    config_file: Optional[str] = None,
    expected_pdf: Optional[str] = None,
    search_patterns: Optional[list] = None,
    verbose: bool = True
) -> bool:
    """
    Post-process PDF generation to ensure PDF is in the correct location.

    Quarto book type sometimes places PDFs in the project root with title-based names.
    This function finds the PDF and moves it to the correct location.

    Args:
        build_dir: Path to rendered output directory (relative to project root)
        config_file: Path to Quarto config file (auto-detects PDF filename if not provided)
        expected_pdf: Expected PDF filename (overrides config detection)
        search_patterns: List of glob patterns to search for PDF (default: ["The*.pdf", "*.pdf"])
        verbose: Whether to print status messages

    Returns:
        True if PDF exists in correct location, False otherwise
    """
    try:
        project_root = _find_project_root()
        build_path = project_root / build_dir

        # Auto-detect PDF filename from config if not provided
        if expected_pdf is None and config_file:
            config_path = project_root / config_file
            if config_path.exists():
                try:
                    with open(config_path, encoding="utf-8") as f:
                        config = yaml.safe_load(f)
                    # Extract output-file from format.pdf
                    pdf_config = config.get("format", {}).get("pdf", {})
                    expected_pdf = pdf_config.get("output-file")
                    if expected_pdf and verbose:
                        print(f"[*] Detected PDF filename from config: {expected_pdf}")
                except Exception as e:
                    if verbose:
                        print(f"[WARNING] Failed to parse config for PDF filename: {e}", file=sys.stderr)

        # If still no PDF filename, cannot proceed
        if expected_pdf is None:
            if verbose:
                print(f"[ERROR] No PDF filename specified or detected from config", file=sys.stderr)
            return False

        target_pdf = build_path / expected_pdf

        # Check if PDF already in correct location
        if target_pdf.exists():
            if verbose:
                print(f"[OK] PDF found in correct location: {build_dir}/{expected_pdf}")
            return True

        # Default search patterns - try to match common Quarto PDF naming
        if search_patterns is None:
            # Use broad patterns by default - will find most PDFs
            search_patterns = ["The*.pdf", "*.pdf"]
        
        patterns = search_patterns
        
        found_pdfs = []
        
        # Helper to find PDFs
        def find_pdfs_in_dir(directory):
            pdfs = []
            for pattern in patterns:
                pdfs.extend(list(directory.glob(pattern)))
            return pdfs

        # First check build directory
        if build_path.exists():
            found_pdfs = find_pdfs_in_dir(build_path)
            
            # Filter out the expected PDF itself if it exists (though we checked that above)
            found_pdfs = [p for p in found_pdfs if p.name != expected_pdf]
            
            if found_pdfs:
                source_pdf = found_pdfs[0]  # Take the first match
                if verbose:
                    print(f"[*] Found PDF in build dir with name: {source_pdf.name}")
                    print(f"[*] Renaming to: {expected_pdf}")

                # Rename PDF to correct name
                shutil.move(str(source_pdf), str(target_pdf))

                if verbose:
                    print(f"[OK] PDF renamed successfully")
                return True

        # Then check project root
        found_pdfs = find_pdfs_in_dir(project_root)
        
        if found_pdfs:
            source_pdf = found_pdfs[0]
            if verbose:
                print(f"[*] Found PDF in wrong location: {source_pdf.name}")
                print(f"[*] Moving to: {build_dir}/{expected_pdf}")

            # Ensure target directory exists
            build_path.mkdir(parents=True, exist_ok=True)

            # Move PDF to correct location
            shutil.move(str(source_pdf), str(target_pdf))

            if verbose:
                print(f"[OK] PDF moved successfully")
            return True

        # PDF not found anywhere
        if verbose:
            print(f"[ERROR] PDF not found in expected locations", file=sys.stderr)
            print(f"        Expected: {target_pdf}", file=sys.stderr)
            print(f"        Searched for patterns: {', '.join(patterns)}", file=sys.stderr)
        return False

    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to post-process PDF: {e}", file=sys.stderr)
        return False


# Backwards-compatible wrapper functions
def postprocess_economics_html(
    build_dir: str = "_site/economics",
    book_url: str = "https://manual.WarOnDisease.org",
    verbose: bool = True
) -> bool:
    """
    Post-process economics HTML (backwards-compatible wrapper).

    Args:
        build_dir: Path to rendered HTML output directory
        book_url: Base URL of the book site
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    return postprocess_html_links(
        build_dir=build_dir,
        source_config="_quarto-economics.yml",
        target_config="_quarto-book.yml",
        target_url=book_url,
        verbose=verbose
    )


def postprocess_economics_pdf(
    build_dir: str = "_site/economics",
    expected_pdf: str = "dih-economic-models.pdf",
    verbose: bool = True
) -> bool:
    """
    Post-process economics PDF (backwards-compatible wrapper).

    Args:
        build_dir: Path to rendered output directory
        expected_pdf: Expected PDF filename
        verbose: Whether to print status messages

    Returns:
        True if PDF exists in correct location, False otherwise
    """
    return postprocess_pdf(
        build_dir=build_dir,
        config_file="_quarto-economics.yml",
        expected_pdf=expected_pdf,
        search_patterns=["The*.pdf", "the*.pdf"],
        verbose=verbose
    )


def postprocess_book_pdf(
    build_dir: str = "_book/warondisease",
    verbose: bool = True
) -> bool:
    """
    Post-process book PDF (auto-detects filename from config).

    Args:
        build_dir: Path to rendered output directory
        verbose: Whether to print status messages

    Returns:
        True if PDF exists in correct location, False otherwise
    """
    return postprocess_pdf(
        build_dir=build_dir,
        config_file="_quarto-book.yml",
        expected_pdf=None,  # Auto-detect from config
        verbose=verbose
    )


def postprocess_wishocracy_pdf(
    build_dir: str = "_site/wishocracy",
    verbose: bool = True
) -> bool:
    """
    Post-process wishocracy PDF (auto-detects filename from config).

    Args:
        build_dir: Path to rendered output directory
        verbose: Whether to print status messages

    Returns:
        True if PDF exists in correct location, False otherwise
    """
    return postprocess_pdf(
        build_dir=build_dir,
        config_file="_quarto-wishocracy.yml",
        expected_pdf=None,  # Auto-detect from config
        verbose=verbose
    )


def postprocess_iab_pdf(
    build_dir: str = "_site/iab",
    verbose: bool = True
) -> bool:
    """
    Post-process IAB PDF (auto-detects filename from config).

    Args:
        build_dir: Path to rendered output directory
        verbose: Whether to print status messages

    Returns:
        True if PDF exists in correct location, False otherwise
    """
    return postprocess_pdf(
        build_dir=build_dir,
        config_file="_quarto-iab.yml",
        expected_pdf=None,  # Auto-detect from config
        verbose=verbose
    )

