#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate outline from all headings in .qmd files listed in _quarto-book.yml

Extracts headings (h1-h6) from each chapter file and generates a hierarchical
outline showing the complete document structure.

Usage:
    python scripts/generate-outline.py [--output OUTLINE.MD]
    
If --output is not specified, prints to stdout.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Set UTF-8 encoding for stdout and stderr on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def extract_headings_from_file(filepath: Path) -> List[Tuple[int, str]]:
    """
    Extract all headings from a .qmd file, ignoring code blocks.
    
    Returns list of tuples: (level, heading_text)
    where level is 1-6 (h1-h6)
    """
    if not filepath.exists():
        return []
    
    headings = []
    in_code_block = False
    code_block_delimiter = None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Track code blocks - handle both ``` and ```{language} formats
                stripped = line.strip()
                if stripped.startswith('```'):
                    # Toggle code block state - any ``` opens/closes
                    in_code_block = not in_code_block
                    continue
                
                # Skip lines inside code blocks
                if in_code_block:
                    continue
                
                # Match markdown headings: # through ######
                # Must have text after the # symbols
                match = re.match(r'^(#{1,6})\s+(.+)$', line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2).strip()
                    # Only add if there's actual text content
                    if text:
                        headings.append((level, text))
    
    except Exception as e:
        print(f"Warning: Error reading {filepath}: {e}", file=sys.stderr)
        return []
    
    return headings


def format_heading(level: int, text: str) -> str:
    """Format a heading for the outline with appropriate indentation."""
    indent = "  " * (level - 1)
    return f"{indent}{'#' * level} {text}"


def extract_chapter_files(book_config: Dict) -> List[Tuple[str, str]]:
    """
    Extract all chapter file paths from the book configuration.
    
    Returns list of tuples: (part_name, file_path)
    where part_name is None for chapters not in a part.
    """
    chapters = []
    
    def process_chapters(chapter_list: List, current_part: Optional[str] = None):
        """Recursively process chapters and parts."""
        for item in chapter_list:
            if isinstance(item, dict):
                if 'part' in item:
                    # This is a part
                    part_name = item['part']
                    if 'chapters' in item:
                        process_chapters(item['chapters'], part_name)
                elif 'href' in item:
                    # This is a chapter with href
                    chapters.append((current_part, item['href']))
                elif isinstance(item, str):
                    # This is a chapter path (string)
                    chapters.append((current_part, item))
            elif isinstance(item, str):
                # Direct chapter path
                chapters.append((current_part, item))
    
    # Process main chapters
    if 'book' in book_config and 'chapters' in book_config['book']:
        process_chapters(book_config['book']['chapters'])
    
    # Process appendices
    if 'book' in book_config and 'appendices' in book_config['book']:
        process_chapters(book_config['book']['appendices'])
    
    return chapters


def generate_outline(book_config_path: Path, project_root: Path) -> str:
    """
    Generate outline from all headings in chapter files.
    
    Returns the outline as a string.
    """
    # Load book configuration
    try:
        with open(book_config_path, 'r', encoding='utf-8') as f:
            book_config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Could not read {book_config_path}: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Extract chapter files
    chapter_files = extract_chapter_files(book_config)
    
    # Get book title
    book_title = book_config.get('book', {}).get('title', 'Book Outline')
    
    # Build outline
    outline_lines = [f"# {book_title}", ""]
    
    current_part = None
    files_with_headings = 0
    files_without_headings = 0
    files_not_found = 0
    total_headings = 0
    
    for part_name, file_path in chapter_files:
        # Skip auto-generated parameters file
        if file_path == "knowledge/appendix/parameters-and-calculations.qmd":
            continue
        
        # Add part header if it changed
        if part_name and part_name != current_part:
            outline_lines.append(f"## {part_name}")
            outline_lines.append("")
            current_part = part_name
        
        # Get full file path
        full_path = project_root / file_path
        
        # Extract headings
        headings = extract_headings_from_file(full_path)
        
        if headings:
            # Add file reference
            outline_lines.append(f"### {file_path}")
            outline_lines.append("")
            
            # Add all headings
            for level, text in headings:
                outline_lines.append(format_heading(level, text))
            
            outline_lines.append("")
            files_with_headings += 1
            total_headings += len(headings)
        else:
            # File exists but has no headings (or file doesn't exist)
            if full_path.exists():
                outline_lines.append(f"### {file_path} (no headings found)")
                files_without_headings += 1
            else:
                outline_lines.append(f"### {file_path} (file not found)")
                files_not_found += 1
            outline_lines.append("")
    
    # Add summary
    outline_lines.append("---")
    outline_lines.append("")
    outline_lines.append(f"**Summary:**")
    outline_lines.append(f"- Files processed: {len(chapter_files)}")
    outline_lines.append(f"- Files with headings: {files_with_headings}")
    outline_lines.append(f"- Files without headings: {files_without_headings}")
    outline_lines.append(f"- Files not found: {files_not_found}")
    outline_lines.append(f"- Total headings extracted: {total_headings}")
    
    return "\n".join(outline_lines)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate outline from headings in _quarto-book.yml chapter files"
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '--book-config',
        type=str,
        default='_quarto-book.yml',
        help='Path to book configuration file (default: _quarto-book.yml)'
    )
    
    args = parser.parse_args()
    
    # Get project root (directory containing _quarto-book.yml)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    book_config_path = project_root / args.book_config
    
    if not book_config_path.exists():
        print(f"Error: Book configuration file not found: {book_config_path}", file=sys.stderr)
        sys.exit(1)
    
    # Generate outline
    outline = generate_outline(book_config_path, project_root)
    
    # Output
    if args.output:
        output_path = project_root / args.output
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(outline)
            print(f"Outline written to {output_path}", file=sys.stderr)
        except Exception as e:
            print(f"Error: Could not write to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(outline)


if __name__ == '__main__':
    main()
