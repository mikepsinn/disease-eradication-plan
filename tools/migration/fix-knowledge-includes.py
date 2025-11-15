#!/usr/bin/env python3
"""Fix .../knowledge/ paths in include directives"""

from pathlib import Path
import re

def fix_includes_in_file(file_path: Path) -> bool:
    """Fix include paths in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Determine the relative path based on file location
        # Files in knowledge/ root should use: figures/
        # Files in knowledge/problem/ should use: ../figures/
        # Files in knowledge/economics/ should use: ../figures/

        parent_dir = file_path.parent.name

        if parent_dir == 'knowledge':
            # Root level - use figures/
            content = re.sub(r'\.\.\./knowledge/figures/', 'figures/', content)
            content = re.sub(r'\.\.\./knowledge/', '', content)
        else:
            # Subdirectory - use ../figures/
            content = re.sub(r'\.\.\./knowledge/figures/', '../figures/', content)
            content = re.sub(r'\.\.\./knowledge/', '../', content)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix include paths in all affected files."""
    project_root = Path(__file__).parent.parent.parent
    knowledge_dir = project_root / 'knowledge'

    files_to_fix = [
        knowledge_dir / 'problem.qmd',
        knowledge_dir / 'problem' / 'cost-of-war.qmd',
        knowledge_dir / 'economics' / 'economics.qmd',
    ]

    files_fixed = 0

    for qmd_file in files_to_fix:
        if qmd_file.exists():
            if fix_includes_in_file(qmd_file):
                files_fixed += 1
                print(f"Fixed: {qmd_file.relative_to(project_root)}")
        else:
            print(f"Warning: {qmd_file} does not exist")

    print(f"\nFixed {files_fixed} files")

if __name__ == '__main__':
    main()
