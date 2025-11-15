#!/usr/bin/env python3
"""
Script to estimate page counts for each file in _quarto.yml and add comments
"""

import re
import os
import yaml
from pathlib import Path


def estimate_pages(file_path: str) -> int:
    """
    Estimate the number of pages a file will contribute to the PDF
    
    Uses:
    - ~275 words per page (standard for academic books)
    - Accounts for code blocks, tables, and equations taking more space
    """
    if not os.path.exists(file_path):
        return 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove YAML frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # Count code blocks (they take more space)
        code_blocks = len(re.findall(r'```[^`]*?```', content, re.DOTALL))
        code_lines = sum(len(block.split('\n')) for block in re.findall(r'```[^`]*?```', content, re.DOTALL))
        
        # Remove code blocks for word counting
        content = re.sub(r'```[^`]*?```', '', content, flags=re.DOTALL)
        
        # Count math equations (they take more space)
        math_equations = len(re.findall(r'\$\$.*?\$\$', content, re.DOTALL))
        inline_math = len(re.findall(r'\$[^$]+\$', content))
        
        # Count tables (they take more space)
        tables = len(re.findall(r'^\|.*\|', content, re.MULTILINE))
        
        # Count words in prose
        words = len(re.findall(r'\b\w+\b', content))
        
        # Base estimate: 275 words per page
        base_pages = max(1, words / 275)
        
        # Add space for code blocks (roughly 40 lines per page)
        code_pages = code_lines / 40 if code_lines > 0 else 0
        
        # Add space for math equations (each equation block ~0.3 pages)
        math_pages = (math_equations * 0.3) + (inline_math * 0.05)
        
        # Add space for tables (each table ~0.2 pages)
        table_pages = tables * 0.2
        
        # Total estimate
        total_pages = base_pages + code_pages + math_pages + table_pages
        
        return max(1, int(round(total_pages)))
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return 0


def extract_file_paths(yaml_content: str) -> list:
    """Extract all .qmd file paths from the YAML content"""
    file_paths = []
    
    # Pattern to match file paths (handles both string and list formats)
    patterns = [
        r'^\s*-\s+([\w/\.-]+\.qmd)',  # List item with file
        r'href:\s*([\w/\.-]+\.qmd)',   # href: file.qmd
        r'^\s*([\w/\.-]+\.qmd)',       # Direct file reference
    ]
    
    for line in yaml_content.split('\n'):
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                file_path = match.group(1)
                if file_path not in file_paths:
                    file_paths.append(file_path)
    
    return file_paths


def add_page_comments(yaml_file: str):
    """Add page estimate comments to _quarto.yml"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # First pass: estimate pages for all files
    file_estimates = {}
    for line in lines:
        # Match file references
        for pattern in [
            r'^\s*-\s+([\w/\.-]+\.qmd)',
            r'href:\s*([\w/\.-]+\.qmd)',
            r'^\s*([\w/\.-]+\.qmd)',
        ]:
            match = re.search(pattern, line)
            if match:
                file_path = match.group(1)
                if file_path not in file_estimates:
                    pages = estimate_pages(file_path)
                    file_estimates[file_path] = pages
                    print(f"Estimated {pages} pages for {file_path}")
    
    # Second pass: add comments
    new_lines = []
    for line in lines:
        new_line = line.rstrip('\n')
        
        # Skip if line already has a page estimate comment
        if re.search(r'#\s*~?\d+\s*pages?', new_line, re.IGNORECASE):
            new_lines.append(new_line + '\n')
            continue
        
        # Check if this line contains a file reference
        for pattern in [
            (r'^\s*-\s+([\w/\.-]+\.qmd)', r'^\s*-\s+([\w/\.-]+\.qmd)'),
            (r'href:\s*([\w/\.-]+\.qmd)', r'href:\s*([\w/\.-]+\.qmd)'),
            (r'^\s*([\w/\.-]+\.qmd)', r'^\s*([\w/\.-]+\.qmd)'),
        ]:
            match = re.search(pattern[0], new_line)
            if match:
                file_path = match.group(1)
                if file_path in file_estimates:
                    pages = file_estimates[file_path]
                    # Add page estimate comment, preserving existing comments
                    if '#' in new_line:
                        # Append to existing comment
                        new_line = f"{new_line} ~{pages}p"
                    else:
                        # Add new comment
                        new_line = f"{new_line}  # ~{pages}p"
                    break
        
        new_lines.append(new_line + '\n')
    
    # Write back
    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    # Print summary
    total_pages = sum(file_estimates.values())
    print(f"\nTotal estimated pages: {total_pages}")
    print(f"Files processed: {len(file_estimates)}")


if __name__ == '__main__':
    import sys
    
    yaml_file = '_quarto.yml'
    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
    
    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Estimating pages for files in {yaml_file}...\n")
    add_page_comments(yaml_file)
    print(f"\nDone! Updated {yaml_file} with page estimates.")

