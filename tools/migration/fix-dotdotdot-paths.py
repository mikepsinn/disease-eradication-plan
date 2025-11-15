#!/usr/bin/env python3
"""Fix .../.../ paths in include directives to ../"""

from pathlib import Path

def fix_paths_in_file(file_path: Path) -> int:
    """Fix .../.../ paths in a single file. Returns number of changes made."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Replace .../../../ with ../../
        content = content.replace('.../../../', '../../')

        # Also replace .../..  with ../.. (in case there's variation)
        content = content.replace('.../..',  '../..')

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            # Count how many replacements were made
            changes = original.count('.../') - content.count('.../')
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
        changes = fix_paths_in_file(qmd_file)
        if changes > 0:
            files_fixed += 1
            total_changes += changes
            print(f"Fixed {changes} path(s) in: {qmd_file.relative_to(project_root)}")

    print(f"\nFixed {total_changes} path(s) across {files_fixed} files")

if __name__ == '__main__':
    main()
