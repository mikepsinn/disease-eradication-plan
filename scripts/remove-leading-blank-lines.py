#!/usr/bin/env python3
"""
Remove leading blank lines from QMD files in brain/figures directory.
"""
import glob
import os

def remove_leading_blank_lines(content):
    """Remove leading blank lines from file content."""
    lines = content.split('\n')
    
    # Find first non-blank line
    first_non_blank = 0
    for i, line in enumerate(lines):
        if line.strip():  # Non-blank line found
            first_non_blank = i
            break
    
    # If all lines are blank, return original
    if first_non_blank == len(lines) - 1 and not lines[-1].strip():
        return content
    
    # Return content starting from first non-blank line
    return '\n'.join(lines[first_non_blank:])

def main():
    files = glob.glob('brain/figures/*.qmd')
    modified = []
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            new_content = remove_leading_blank_lines(content)
            
            if new_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                modified.append(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print(f"Removed leading blank lines from {len(modified)} files:")
    for f in modified:
        print(f"  - {f}")
    
    if not modified:
        print("No files needed modification (no leading blank lines found)")

if __name__ == '__main__':
    main()

