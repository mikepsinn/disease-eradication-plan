#!/usr/bin/env python3
"""Fix asset paths that have .../../assets/ instead of ../../assets/"""

from pathlib import Path

def fix_asset_paths_in_file(file_path: Path) -> bool:
    """Fix asset paths in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Fix the pattern .../../assets/ to ../../assets/
        content = content.replace('.../../assets/', '../../assets/')

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix asset paths in all .qmd files."""
    project_root = Path(__file__).parent.parent.parent
    knowledge_dir = project_root / 'knowledge'

    if not knowledge_dir.exists():
        print(f"Error: {knowledge_dir} does not exist")
        return

    files_fixed = 0
    files_processed = 0

    for qmd_file in knowledge_dir.rglob('*.qmd'):
        files_processed += 1
        if fix_asset_paths_in_file(qmd_file):
            files_fixed += 1
            print(f"Fixed: {qmd_file.relative_to(project_root)}")

    print(f"\nProcessed {files_processed} files")
    print(f"Fixed {files_fixed} files")

if __name__ == '__main__':
    main()
