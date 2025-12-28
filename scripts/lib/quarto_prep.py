#!/usr/bin/env python3
"""
Quarto Preparation Utilities
============================

Shared utilities for preparing Quarto files before rendering:
- Copying and updating relative paths for economics.qmd -> index.qmd
- Copying index-book.qmd -> index.qmd for book rendering
- Copying config files (_quarto-book.yml, _quarto-economics.yml -> _quarto.yml)
- Post-processing HTML to rewrite links to book content as absolute URLs
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

        files = set()
        render_list = config.get("project", {}).get("render", [])

        for item in render_list:
            if isinstance(item, str):
                files.add(item)

        if verbose:
            print(f"[*] Found {len(files)} files in economics config", flush=True)

        return files

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

        # Extract from book.chapters
        book_config = config.get("book", {})
        if "chapters" in book_config:
            extract_chapters(book_config["chapters"])

        if verbose:
            print(f"[*] Found {len(files)} files in book config", flush=True)

        return files

    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to parse _quarto-book.yml: {e}", file=sys.stderr)
        raise


def prepare_economics_index(verbose: bool = True) -> bool:
    """
    Copy economics.qmd to index.qmd and update relative paths.

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()

    economics_qmd = project_root / "knowledge" / "economics" / "economics.qmd"
    index_qmd = project_root / "index.qmd"

    if not economics_qmd.exists():
        if verbose:
            print(f"[ERROR] Missing {economics_qmd.relative_to(project_root)}", file=sys.stderr)
            print("        Unable to prepare economics index.", file=sys.stderr)
        return False

    if verbose:
        print(f"[*] Copying {economics_qmd.relative_to(project_root)} -> index.qmd", flush=True)

    try:
        with open(economics_qmd, encoding="utf-8") as f:
            content = f.read()

        # Update relative paths when copying from knowledge/economics/ to root:
        # - ../../ becomes empty (two levels up from economics/ = root)
        # - ../ becomes knowledge/ (one level up from economics/ = knowledge/)
        # - ./filename or just filename (same directory) becomes knowledge/economics/filename
        # Must replace ../../ first to avoid double replacement

        # Replace ../../ with empty string (goes to root)
        content = re.sub(r"\.\./\.\./", "", content)
        # Replace remaining ../ with knowledge/ (goes to knowledge/)
        content = re.sub(r"\.\./", "knowledge/", content)

        # Handle same-directory links: [text](filename.qmd) or [text](./filename.qmd)
        # Pattern matches markdown links with relative paths (not starting with http, https, #, or /)
        # Root-level directories that shouldn't get knowledge/economics/ prefix
        root_level_dirs = ["assets/", "scripts/", "dih_models/", "brain/", "references.bib"]

        def replace_same_dir_link(match):
            link_text = match.group(1)
            link_path = match.group(2)
            # Skip if it's a URL, anchor, or absolute path
            if (
                link_path.startswith("http://")
                or link_path.startswith("https://")
                or link_path.startswith("#")
                or link_path.startswith("/")
                or "://" in link_path
            ):
                return match.group(0)  # Return unchanged
            # Skip if path already has knowledge/ (already processed)
            if link_path.startswith("knowledge/"):
                return match.group(0)  # Return unchanged
            # Skip if path is a root-level directory (like assets/, scripts/, etc.)
            if any(link_path.startswith(root_dir) for root_dir in root_level_dirs):
                return match.group(0)  # Return unchanged
            # Replace ./filename or just filename with knowledge/economics/filename
            if link_path.startswith("./"):
                new_path = "knowledge/economics/" + link_path[2:]
            else:
                # Just a filename (same directory)
                new_path = "knowledge/economics/" + link_path
            return f"[{link_text}]({new_path})"

        # Match markdown links: [text](path)
        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_same_dir_link, content)

        with open(index_qmd, "w", encoding="utf-8") as f:
            f.write(content)

        return True
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to copy economics.qmd: {e}", file=sys.stderr)
        return False


def prepare_book_index(verbose: bool = True) -> bool:
    """
    Copy index-book.qmd to index.qmd for book rendering.

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()

    index_book_qmd = project_root / "index-book.qmd"
    index_qmd = project_root / "index.qmd"

    if not index_book_qmd.exists():
        if verbose:
            print(f"[ERROR] Missing {index_book_qmd.relative_to(project_root)}", file=sys.stderr)
            print("        Unable to prepare book index.", file=sys.stderr)
        return False

    if verbose:
        print(f"[*] Copying {index_book_qmd.relative_to(project_root)} -> index.qmd", flush=True)

    try:
        shutil.copy2(index_book_qmd, index_qmd)
        return True
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to copy index-book.qmd: {e}", file=sys.stderr)
        return False


def prepare_quarto_config(config_name: str, verbose: bool = True) -> bool:
    """
    Copy a Quarto config file to _quarto.yml.

    Args:
        config_name: Name of config file (e.g., '_quarto-book.yml', '_quarto-economics.yml')
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()

    config_file = project_root / config_name
    quarto_yml = project_root / "_quarto.yml"

    if not config_file.exists():
        if verbose:
            print(f"[ERROR] Missing {config_file.relative_to(project_root)}", file=sys.stderr)
        return False

    if verbose:
        print(f"[*] Copying {config_file.name} -> _quarto.yml", flush=True)

    try:
        shutil.copy2(config_file, quarto_yml)
        return True
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to copy config: {e}", file=sys.stderr)
        return False


def prepare_economics(verbose: bool = True) -> bool:
    """
    Prepare everything needed for economics rendering:
    - Copy _quarto-economics.yml to _quarto.yml
    - Copy economics.qmd to index.qmd with updated paths

    NOTE: Link rewriting is now done AFTER render via postprocess_economics_html()

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    if not prepare_quarto_config("_quarto-economics.yml", verbose):
        return False

    if not prepare_economics_index(verbose):
        return False

    return True


def prepare_book(verbose: bool = True) -> bool:
    """
    Prepare everything needed for book rendering:
    - Copy _quarto-book.yml to _quarto.yml
    - Copy index-book.qmd to index.qmd

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    if not prepare_quarto_config("_quarto-book.yml", verbose):
        return False

    if not prepare_book_index(verbose):
        return False

    return True


def prepare_paper_index(paper_path: str, verbose: bool = True) -> bool:
    """
    Copy a paper QMD file to index.qmd and update relative paths.

    For papers in knowledge/appendix/, when copying to root:
    - ../ becomes knowledge/ (one level up from appendix/ = knowledge/)
    - ../../ becomes empty string (two levels up from appendix/ = root)

    Args:
        paper_path: Relative path to paper from project root (e.g., 'knowledge/appendix/wishocracy-paper.qmd')
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()

    paper_qmd = project_root / paper_path
    index_qmd = project_root / "index.qmd"

    if not paper_qmd.exists():
        if verbose:
            print(f"[ERROR] Missing {paper_qmd.relative_to(project_root)}", file=sys.stderr)
            print("        Unable to prepare paper index.", file=sys.stderr)
        return False

    if verbose:
        print(f"[*] Copying {paper_qmd.relative_to(project_root)} -> index.qmd", flush=True)

    try:
        with open(paper_qmd, encoding="utf-8") as f:
            content = f.read()

        # Update relative paths when copying from knowledge/appendix/ to root:
        # - ../../ becomes empty (two levels up from appendix/ = root)
        # - ../ becomes knowledge/ (one level up from appendix/ = knowledge/)
        # Must replace ../../ first to avoid double replacement

        # Replace ../../ with empty string (goes to root)
        content = re.sub(r"\.\./\.\./", "", content)
        # Replace remaining ../ with knowledge/ (goes to knowledge/)
        content = re.sub(r"\.\./", "knowledge/", content)

        with open(index_qmd, "w", encoding="utf-8") as f:
            f.write(content)

        return True
    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to copy paper: {e}", file=sys.stderr)
        return False


def prepare_wishocracy(verbose: bool = True) -> bool:
    """
    Prepare everything needed for wishocracy paper rendering:
    - Copy _quarto-wishocracy.yml to _quarto.yml
    - Copy wishocracy-paper.qmd to index.qmd

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    if not prepare_quarto_config("_quarto-wishocracy.yml", verbose):
        return False

    if not prepare_paper_index("knowledge/appendix/wishocracy-paper.qmd", verbose):
        return False

    return True


def prepare_iab(verbose: bool = True) -> bool:
    """
    Prepare everything needed for IAB paper rendering:
    - Copy _quarto-iab.yml to _quarto.yml
    - Copy incentive-alignment-bonds-paper.qmd to index.qmd

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    if not prepare_quarto_config("_quarto-iab.yml", verbose):
        return False

    if not prepare_paper_index("knowledge/appendix/incentive-alignment-bonds-paper.qmd", verbose):
        return False

    return True


def postprocess_economics_html(
    build_dir: str = "_site/economics",
    book_url: str = "https://manual.WarOnDisease.org",
    verbose: bool = True
) -> bool:
    """
    Post-process rendered HTML files to rewrite links to book content as absolute URLs.

    This runs AFTER quarto render completes, so source .qmd files remain untouched.
    Only rewrites links to files that are in the book but NOT in economics.

    Args:
        build_dir: Path to rendered HTML output directory (relative to project root)
        book_url: Base URL of the book site
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

        # Get list of files in economics and book
        economics_files = _extract_economics_files(verbose=False)
        book_files = _extract_book_files(verbose=False)

        # Convert to .html paths
        economics_html = {f.replace(".qmd", ".html") for f in economics_files}
        book_html = {f.replace(".qmd", ".html") for f in book_files}

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

                    # Convert to .html for book lookups
                    resolved_html = resolved_qmd.replace(".qmd", ".html")

                    # Check if this link should be rewritten
                    # Rewrite if: in book but NOT in economics
                    if resolved_qmd in book_files and resolved_qmd not in economics_files:
                        new_url = f"{book_url}/{resolved_html}{anchor}"
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
                print(f"[OK] Post-processed {files_modified} HTML files, rewrote {links_rewritten} links to book")
            else:
                print(f"[*] No links needed rewriting in economics HTML")

        return True

    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to post-process HTML: {e}", file=sys.stderr)
        return False
