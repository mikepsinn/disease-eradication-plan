#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Install Windows-compatible Ralph Loop plugin scripts.

This script copies the Python versions of the ralph-loop plugin scripts
to the Claude Code plugin cache, replacing the Bash scripts that don't
work on Windows.

Usage:
    python .claude/plugins/ralph-loop/install-windows-fix.py
"""

import os
import sys
import shutil
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

def get_plugin_locations():
    """Get all ralph-loop plugin cache locations."""
    home = Path.home()
    claude_dir = home / '.claude' / 'plugins'

    locations = []

    # Check cache directories
    cache_dir = claude_dir / 'cache' / 'claude-plugins-official' / 'ralph-loop'
    if cache_dir.exists():
        for subdir in cache_dir.iterdir():
            if subdir.is_dir():
                locations.append(subdir)

    # Check marketplaces directory
    marketplace_dir = claude_dir / 'marketplaces' / 'claude-plugins-official' / 'plugins' / 'ralph-loop'
    if marketplace_dir.exists():
        locations.append(marketplace_dir)

    return locations


def install_to_location(src_dir: Path, dest_dir: Path):
    """Install Python scripts to a plugin location."""
    print(f"  Installing to: {dest_dir}")

    # Copy scripts
    scripts_dir = dest_dir / 'scripts'
    scripts_dir.mkdir(exist_ok=True)
    shutil.copy(src_dir / 'setup-ralph-loop.py', scripts_dir / 'setup-ralph-loop.py')

    # Copy hooks
    hooks_dir = dest_dir / 'hooks'
    hooks_dir.mkdir(exist_ok=True)
    shutil.copy(src_dir / 'stop-hook.py', hooks_dir / 'stop-hook.py')
    shutil.copy(src_dir / 'hooks.json', hooks_dir / 'hooks.json')

    # Copy command
    commands_dir = dest_dir / 'commands'
    commands_dir.mkdir(exist_ok=True)
    shutil.copy(src_dir / 'ralph-loop.md', commands_dir / 'ralph-loop.md')

    print(f"    [OK] Installed Python scripts")


def main():
    print("Ralph Loop Windows Fix Installer")
    print("=" * 40)
    print("")

    # Find source directory (where this script is located)
    src_dir = Path(__file__).parent

    # Get all plugin locations
    locations = get_plugin_locations()

    if not locations:
        print("ERROR: No ralph-loop plugin locations found.")
        print("Make sure the plugin is installed:")
        print("  /plugin install ralph-loop@claude-plugins-official")
        sys.exit(1)

    print(f"Found {len(locations)} plugin location(s):")
    print("")

    for loc in locations:
        install_to_location(src_dir, loc)

    print("")
    print("=" * 40)
    print("[OK] Installation complete!")
    print("")
    print("Restart Claude Code for changes to take effect.")


if __name__ == '__main__':
    main()
