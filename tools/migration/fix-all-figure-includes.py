#!/usr/bin/env python3
"""Fix all knowledge/figures/ paths in include directives to use relative paths"""

from pathlib import Path
import re

def fix_includes_in_file(file_path: Path, project_root: Path) -> int:
    """Fix include paths in a single file. Returns number of changes made."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Replace knowledge/figures/ with the correct relative path
        # Files in subdirectories need ../figures/
        # Files in knowledge/ root need figures/

        parent = file_path.parent
        if parent.name == 'knowledge':
            # Root level - use figures/
            content = re.sub(r'knowledge/figures/', 'figures/', content)
        else:
            # Subdirectory - use ../figures/
            content = re.sub(r'knowledge/figures/', '../figures/', content)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            # Count how many replacements were made
            changes = len(re.findall(r'knowledge/figures/', original))
            return changes
        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    """Fix include paths in all .qmd files."""
    project_root = Path(__file__).parent.parent.parent
    knowledge_dir = project_root / 'knowledge'

    if not knowledge_dir.exists():
        print(f"Error: {knowledge_dir} does not exist")
        return

    total_changes = 0
    files_fixed = 0

    for qmd_file in knowledge_dir.rglob('*.qmd'):
        changes = fix_includes_in_file(qmd_file, project_root)
        if changes > 0:
            files_fixed += 1
            total_changes += changes
            print(f"Fixed {changes} include(s) in: {qmd_file.relative_to(project_root)}")

    print(f"\nFixed {total_changes} include directive(s) across {files_fixed} files")

if __name__ == '__main__':
    main()
