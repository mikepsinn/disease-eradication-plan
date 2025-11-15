#!/usr/bin/env python3
"""
Add missing imports to figure files that use get_figure_output_path
"""

import re
from pathlib import Path

def add_import_to_file(file_path: Path) -> bool:
    """Add the missing import to a file if needed."""
    content = file_path.read_text(encoding='utf-8')

    # Check if already has the import
    if 'from dih_models.plotting.chart_style import get_figure_output_path' in content:
        return False

    # Check if file uses get_figure_output_path
    if 'get_figure_output_path' not in content:
        return False

    # Find the first Python code block after the YAML frontmatter
    # Pattern: ```{python} or ```python
    pattern = r'(---\n.*?\n---\n)(```\{python\}[^\n]*\n)'

    match = re.search(pattern, content, re.DOTALL)

    if match:
        # Insert the import after the opening of the first Python block
        before = content[:match.end()]
        after = content[match.end():]

        # Add import line
        import_line = 'from dih_models.plotting.chart_style import get_figure_output_path\n'

        new_content = before + import_line + after
        file_path.write_text(new_content, encoding='utf-8')
        return True

    return False

def main():
    """Add imports to all figure files."""
    project_root = Path(__file__).parent.parent.parent
    figures_dir = project_root / 'knowledge' / 'figures'

    if not figures_dir.exists():
        print(f"Error: {figures_dir} does not exist")
        return

    files_fixed = 0
    files_processed = 0

    for qmd_file in figures_dir.glob('*.qmd'):
        files_processed += 1
        if add_import_to_file(qmd_file):
            files_fixed += 1
            print(f"Fixed: {qmd_file.name}")

    print(f"\nProcessed {files_processed} files")
    print(f"Added imports to {files_fixed} files")

if __name__ == '__main__':
    main()
