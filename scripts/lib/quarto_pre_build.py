#!/usr/bin/env python3
"""
Quarto Pre-Build Processing
============================

Pre-render preparation for Quarto multi-site builds:
- Copy and activate site-specific config files (_quarto-*.yml → _quarto.yml)
- Copy and transform index files with path updates
- Rewrite cross-site links for PDF rendering (converts .qmd links to absolute URLs)
- Support for book, economics, wishocracy, and IAB sites
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


def prepare_pdf_build_temp(
    source_config: str = "_quarto-economics.yml",
    target_config: str = "_quarto-book.yml",
    target_url: str = "https://manual.WarOnDisease.org",
    verbose: bool = True
) -> Optional[Path]:
    """
    Prepare temporary build directory for PDF rendering with cross-site link rewriting.

    Creates _build_temp/, copies project files, modifies QMD links to absolute URLs.
    Caller should cd to returned path, render PDF, copy PDF back, then clean up temp folder.

    Args:
        source_config: Path to source Quarto config (e.g., "_quarto-economics.yml")
        target_config: Path to target Quarto config (default: "_quarto-book.yml")
        target_url: Base URL of the target site
        verbose: Whether to print status messages

    Returns:
        Path to temp build directory, or None if failed
    """
    try:
        project_root = _find_project_root()

        # Clean up any existing temp directory
        build_temp = project_root / "_build_temp"
        if build_temp.exists():
            if verbose:
                print(f"[*] Cleaning up existing _build_temp/", flush=True)
            shutil.rmtree(build_temp)

        # Create fresh temp directory
        build_temp.mkdir(exist_ok=True)
        if verbose:
            print(f"[*] Created temporary build directory: _build_temp/", flush=True)

        # Copy entire project to temp (excluding ignored files)
        ignore_patterns = [
            "_build_temp",
            "_site",
            "_book",
            ".quarto",
            "node_modules",
            ".git",
            "__pycache__",
            ".venv",
            "*.pyc",
            ".jupyter_cache",
            "nul"  # Windows reserved filename
        ]

        # Read .gitignore if it exists
        gitignore_path = project_root / ".gitignore"
        if gitignore_path.exists():
            try:
                with open(gitignore_path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if line and not line.startswith('#'):
                            # Remove trailing slashes from directory patterns
                            pattern = line.rstrip('/')
                            ignore_patterns.append(pattern)
                if verbose:
                    print(f"[*] Loaded {len(ignore_patterns)} ignore patterns from .gitignore", flush=True)
            except Exception as e:
                if verbose:
                    print(f"[WARNING] Failed to read .gitignore: {e}", file=sys.stderr)

        if verbose:
            print(f"[*] Copying project files to _build_temp/...", flush=True)

        def ignore_files(directory, files):
            """Return files to ignore during copy."""
            ignored = []
            for pattern in ignore_patterns:
                for file in files:
                    if pattern in file or file.startswith('.'):
                        ignored.append(file)
            return set(ignored)

        # Copy all files except ignored ones
        for item in project_root.iterdir():
            if item.name in ignore_patterns or item.name.startswith('.'):
                continue
            dest = build_temp / item.name
            try:
                if item.is_dir():
                    if verbose:
                        print(f"[*] Copying directory: {item.name}", flush=True)
                    shutil.copytree(item, dest, ignore=ignore_files, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)
            except Exception as e:
                if verbose:
                    print(f"[ERROR] Failed to copy {item.name}: {e}", file=sys.stderr)
                raise

        if verbose:
            print(f"[OK] Copied project files to _build_temp/", flush=True)

        # Get list of files from both configs
        source_yml = project_root / source_config
        target_yml = project_root / target_config

        if not source_yml.exists():
            if verbose:
                print(f"[ERROR] Source config not found: {source_config}", file=sys.stderr)
            return None

        if not target_yml.exists():
            if verbose:
                print(f"[WARNING] Target config not found: {target_config}, skipping link rewriting", file=sys.stderr)
            return build_temp

        # Parse configs
        try:
            with open(source_yml, encoding="utf-8") as f:
                source_cfg = yaml.safe_load(f)
            with open(target_yml, encoding="utf-8") as f:
                target_cfg = yaml.safe_load(f)
        except Exception as e:
            if verbose:
                print(f"[ERROR] Failed to parse config files: {e}", file=sys.stderr)
            return None

        # Extract file lists
        source_files = _extract_files_from_config(source_cfg, verbose=False)
        target_files = _extract_files_from_config(target_cfg, verbose=False)

        if verbose:
            print(f"[*] Preprocessing QMD links in _build_temp/", flush=True)
            print(f"[*] Source files: {len(source_files)}, Target files: {len(target_files)}", flush=True)

        links_rewritten = 0
        files_modified = 0

        # Process each file in the source config
        # Also process index.qmd if it exists (created by prepare_economics_index)
        files_to_process = list(source_files)
        if (build_temp / "index.qmd").exists():
            files_to_process.append("index.qmd")

        for file_path_str in files_to_process:
            qmd_file = build_temp / file_path_str

            if not qmd_file.exists():
                if verbose:
                    print(f"[WARNING] File not found: {file_path_str}", file=sys.stderr)
                continue

            try:
                with open(qmd_file, encoding="utf-8") as f:
                    content = f.read()

                modified_content = content

                # Find all markdown links: [text](path)
                def rewrite_link(match):
                    nonlocal links_rewritten

                    link_text = match.group(1)
                    link_path = match.group(2)

                    # Skip external links, anchors, mailto links
                    if link_path.startswith(("http://", "https://", "#", "mailto:")):
                        return match.group(0)

                    # Only process .qmd links (may have anchor like file.qmd#section)
                    if ".qmd" not in link_path:
                        return match.group(0)

                    # Resolve path to absolute (from project root perspective)
                    if link_path.startswith("/"):
                        # Absolute path from project root - strip leading /
                        import os
                        resolved_path = os.path.normpath(link_path[1:])
                        resolved_path = resolved_path.replace("\\", "/")
                    elif link_path.startswith("../") or link_path.startswith("./"):
                        # Relative path - resolve from file's directory
                        file_rel = qmd_file.relative_to(build_temp)
                        file_dir = file_rel.parent
                        import os
                        resolved_path = os.path.normpath(os.path.join(str(file_dir), link_path))
                        resolved_path = resolved_path.replace("\\", "/")
                    else:
                        resolved_path = link_path

                    # Split anchor from path
                    anchor = ""
                    if "#" in resolved_path:
                        resolved_path, anchor = resolved_path.split("#", 1)
                        anchor = f"#{anchor}"

                    # Remove .qmd extension for lookups
                    resolved_qmd = resolved_path

                    # Check if this link should be rewritten
                    # Rewrite if: in target but NOT in source
                    if resolved_qmd in target_files and resolved_qmd not in source_files:
                        # Convert .qmd to .html for URL
                        resolved_html = resolved_qmd.replace(".qmd", ".html")
                        new_url = f"{target_url}/{resolved_html}{anchor}"

                        if verbose:
                            print(f"[*] {file_path_str}: {link_path} -> {new_url}")

                        links_rewritten += 1
                        return f"[{link_text}]({new_url})"

                    # Otherwise leave unchanged
                    return match.group(0)

                # Replace all markdown links
                modified_content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite_link, modified_content)

                # Only write if content changed
                if modified_content != content:
                    with open(qmd_file, "w", encoding="utf-8") as f:
                        f.write(modified_content)
                    files_modified += 1

            except Exception as e:
                if verbose:
                    print(f"[WARNING] Failed to process {file_path_str}: {e}", file=sys.stderr)
                continue

        if verbose:
            if links_rewritten > 0:
                print(f"[OK] Preprocessed {files_modified} QMD files, rewrote {links_rewritten} links", flush=True)
            else:
                print(f"[*] No links needed rewriting", flush=True)

        return build_temp

    except Exception as e:
        if verbose:
            print(f"[ERROR] Failed to prepare temp build directory: {e}", file=sys.stderr)
        return None


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
                or link_path.startswith("mailto:")
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


def prepare_test_index(verbose: bool = True) -> bool:
    """
    Copy test-economics.qmd to index.qmd and update relative paths.

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    project_root = _find_project_root()

    test_qmd = project_root / "knowledge" / "test" / "test-economics.qmd"
    index_qmd = project_root / "index.qmd"

    if not test_qmd.exists():
        if verbose:
            print(f"[ERROR] Missing {test_qmd.relative_to(project_root)}", file=sys.stderr)
            print("        Unable to prepare test index.", file=sys.stderr)
        return False

    if verbose:
        print(f"[*] Copying {test_qmd.relative_to(project_root)} -> index.qmd", flush=True)

    try:
        with open(test_qmd, encoding="utf-8") as f:
            content = f.read()

        # Update relative paths when copying from knowledge/test/ to root:
        # - ../../ becomes empty (two levels up from test/ = root)
        # - ../ becomes knowledge/ (one level up from test/ = knowledge/)
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
            print(f"[ERROR] Failed to copy test-economics.qmd: {e}", file=sys.stderr)
        return False


def prepare_test(verbose: bool = True) -> bool:
    """
    Prepare everything needed for test PDF rendering:
    - Copy _quarto-test.yml to _quarto.yml
    - Copy test-economics.qmd to index.qmd with updated paths

    Args:
        verbose: Whether to print status messages

    Returns:
        True if successful, False otherwise
    """
    if not prepare_quarto_config("_quarto-test.yml", verbose):
        return False

    if not prepare_test_index(verbose):
        return False

    return True

