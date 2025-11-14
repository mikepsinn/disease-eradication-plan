#!/usr/bin/env python3
"""
Remove initial headings that appear immediately after Python code blocks in QMD files.
Preserves all frontmatter and content before/after the Python block.
"""
import re
import glob
import os

def remove_initial_heading(content):
    """Remove the first heading that appears immediately after the Python code block."""
    # Find the Python code block
    python_block_pattern = re.compile(
        r'```\{python\}.*?```',
        re.DOTALL
    )
    
    match = python_block_pattern.search(content)
    if not match:
        return content, False
    
    # Get the end position of the Python block
    python_end = match.end()
    
    # Look for heading immediately after Python block (with optional whitespace)
    # Match: end of Python block, optional whitespace/newlines, then heading
    after_python = content[python_end:]
    heading_pattern = re.compile(r'^(\s*\n\s*)(#+\s+.*?\n)', re.MULTILINE)
    
    heading_match = heading_pattern.match(after_python)
    if heading_match:
        # Remove the heading but keep the whitespace
        new_after_python = heading_match.group(1) + after_python[heading_match.end():]
        new_content = content[:python_end] + new_after_python
        return new_content, True
    
    return content, False

def main():
    files = glob.glob('brain/book/**/*.qmd', recursive=True)
    modified = []
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content, was_modified = remove_initial_heading(content)
            
            if was_modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                modified.append(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print(f"Removed initial heading from {len(modified)} files:")
    for f in modified[:20]:
        print(f"  - {f}")
    if len(modified) > 20:
        print(f"  ... and {len(modified) - 20} more")

if __name__ == '__main__':
    main()

