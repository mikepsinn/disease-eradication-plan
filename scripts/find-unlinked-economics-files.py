#!/usr/bin/env python3
"""
Find files in _quarto-economics.yml that are not linked from economics.qmd.

This helps identify orphaned content that might need to be removed or
content that should be added to the main economics page.
"""
import re
import sys
from pathlib import Path
import yaml


def extract_qmd_files_from_config(config_path: Path) -> set[str]:
    """Extract all .qmd files from the quarto config's render list."""
    with open(config_path) as f:
        config = yaml.safe_load(f)

    render_list = config.get('project', {}).get('render', [])
    qmd_files = set()

    for item in render_list:
        # Skip comments and index.qmd (that's the economics.qmd copy)
        if isinstance(item, str) and item.endswith('.qmd') and item != 'index.qmd':
            qmd_files.add(item)

    return qmd_files


def extract_links_from_markdown(md_path: Path, repo_root: Path) -> set[str]:
    """Extract all .qmd file links from a markdown file and resolve relative paths."""
    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    # Pattern to match markdown links and href attributes to .qmd files
    # Matches: [text](path.qmd), href="path.qmd", href='path.qmd'
    patterns = [
        r'\[([^\]]+)\]\(([^)]+\.qmd(?:#[^)]*)?)\)',  # Markdown links
        r'href=["\']([^"\']+\.qmd(?:#[^"\']*)?)["\']',  # HTML href
    ]

    linked_files = set()
    for pattern in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            # Get the path (different group depending on pattern)
            path = match.group(2) if len(match.groups()) > 1 else match.group(1)
            # Remove fragment if present
            if '#' in path:
                path = path.split('#')[0]
            # Remove leading slash if present
            path = path.lstrip('/')

            # Resolve relative paths (e.g., ../appendix/file.qmd)
            if path.startswith('../') or path.startswith('./'):
                # Get the directory containing the markdown file
                md_dir = md_path.parent
                # Resolve the relative path
                resolved = (md_dir / path).resolve()
                # Make it relative to repo root
                try:
                    path = str(resolved.relative_to(repo_root)).replace('\\', '/')
                except ValueError:
                    # If path is outside repo, keep original
                    pass

            linked_files.add(path)

    return linked_files


def main():
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / '_quarto-economics.yml'
    economics_path = repo_root / 'knowledge' / 'economics' / 'economics.qmd'

    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        return 1

    if not economics_path.exists():
        print(f"Error: Economics file not found: {economics_path}")
        return 1

    print("=" * 80)
    print("ECONOMICS CONFIG ORPHAN ANALYSIS")
    print("=" * 80)
    print()

    # Get files from config
    config_files = extract_qmd_files_from_config(config_path)
    print(f"Files in _quarto-economics.yml: {len(config_files)}")

    # Get links from economics.qmd
    linked_files = extract_links_from_markdown(economics_path, repo_root)
    print(f"Files linked from economics.qmd: {len(linked_files)}")
    print()

    # Find unlinked files
    unlinked = config_files - linked_files

    if not unlinked:
        print("[OK] All files in config are linked from economics.qmd!")
        return 0

    print(f"Found {len(unlinked)} file(s) in config NOT linked from economics.qmd:")
    print()

    # Group by directory for better readability
    by_dir = {}
    for file in sorted(unlinked):
        dir_name = str(Path(file).parent)
        if dir_name not in by_dir:
            by_dir[dir_name] = []
        by_dir[dir_name].append(file)

    for dir_name, files in sorted(by_dir.items()):
        print(f"  {dir_name}/")
        for file in sorted(files):
            filename = Path(file).name
            print(f"    - {filename}")
        print()

    print("=" * 80)
    print("SUGGESTIONS:")
    print("=" * 80)
    print()
    print("These files are in the economics config but not linked from economics.qmd.")
    print("You may want to:")
    print("  1. Add links to these files in economics.qmd if they're important")
    print("  2. Remove them from _quarto-economics.yml if they're not needed")
    print("  3. Keep them if they're accessed via sidebar/navbar only")
    print()

    # Also show files that ARE linked (for completeness)
    linked_in_both = config_files & linked_files
    if linked_in_both:
        print(f"[OK] {len(linked_in_both)} file(s) are linked from economics.qmd:")
        for file in sorted(linked_in_both):
            print(f"    {file}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
