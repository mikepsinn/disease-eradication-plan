#!/usr/bin/env python3
"""Fix ../../figures/ paths to ../figures/ in subdirectories"""

from pathlib import Path

def fix_paths_in_file(file_path: Path, project_root: Path) -> int:
    """Fix ../../figures/ to ../figures/ if file is in a subdirectory of knowledge/."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Only fix if file is in a subdirectory of knowledge/
        # (not in knowledge/ root)
        parent_dir = file_path.parent
        if parent_dir.name != 'knowledge':
            # Replace ../../figures/ with ../figures/
            content = content.replace('../../figures/', '../figures/')

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            changes = original.count('../../figures/') - content.count('../../figures/')
            return changes
        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    """Fix paths in all .qmd files."""
    project_root = Path(__file__).parent.parent.parent
    knowledge_dir = project_root / 'knowledge'

    if not knowledge_dir.exists():
        print(f"Error: {knowledge_dir} does not exist")
        return

    total_changes = 0
    files_fixed = 0

    for qmd_file in knowledge_dir.rglob('*.qmd'):
        changes = fix_paths_in_file(qmd_file, project_root)
        if changes > 0:
            files_fixed += 1
            total_changes += changes
            print(f"Fixed {changes} path(s) in: {qmd_file.relative_to(project_root)}")

    print(f"\nFixed {total_changes} path(s) across {files_fixed} files")

if __name__ == '__main__':
    main()
