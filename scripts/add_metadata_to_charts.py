#!/usr/bin/env python3
"""
Add PNG metadata to all chart files

This script updates all .qmd chart files to use add_png_metadata() for
proper attribution when images are shared on social media.
"""

import re
from pathlib import Path

CHART_FILES = [
    'brain/figures/healthcare-spending-vs-life-expectancy.qmd',
    'brain/figures/life-expectancy-pre-post-1962.qmd',
    'brain/figures/fda-spending-life-expectancy-drug-costs-combined.qmd',
    'brain/figures/life-expectancy-before-after-fda-line-chart.qmd',
    'brain/figures/fda-spending-life-expectancy-trend-line-chart.qmd',
    'brain/figures/fda-drug-development-cost-increase-line-chart.qmd',
    'brain/figures/current-vs-dfda-clinical-trial-cost-column-chart.qmd',
    'brain/figures/one-percent-treaty-top-country-contributions-column-chart.qmd',
    'brain/figures/congressional-committee-seat-costs-column-chart.qmd',
    'brain/figures/daily-deaths-breakdown-column-chart.qmd',
    'brain/book/appendix/peace-dividend-analysis.qmd',
    'brain/book/appendix/humanity-budget-overview.qmd',
    'brain/figures/humanity-spending-priorities-bar-chart.qmd',
    'brain/figures/war-vs-curing-diseases-column-chart.qmd',
    'brain/figures/war-vs-disease-total-costs-vs-curing-spending-column-chart.qmd',
    'brain/figures/war-hidden-direct-curing-diseases-column-chart.qmd',
    'brain/figures/war-real-hidden-costs-breakdown.qmd',
    'brain/figures/war-total-costs-breakdown-vs-curing-spending-column-chart.qmd',
    'brain/figures/self-funding-roi-comparison-column-chart.qmd',
    'brain/figures/military-vs-medical-research-spending-1-percent-treaty-column-chart.qmd',
    'brain/figures/military-vs-medical-research-spending-column-chart.qmd',
    'brain/figures/military-vs-medical-spending-ratio-bar-chart.qmd',
    'brain/figures/money-flow-diagram.qmd',
    'brain/figures/nih-budget-allocation-pie-chart.qmd',
    'brain/figures/philanthropic-cost-effectiveness-comparison-bar-chart.qmd',
    'brain/figures/public-health-interventions-economic-benefit-comparison-column-chart.qmd',
    'brain/figures/military-vs-medical-research-direct-spending-column-chart.qmd',
    'brain/figures/health-programs-vs-1-percent-treaty-societal-benefits-bar-chart.qmd',
    'brain/figures/health-interventions-roi-comparison-column-chart.qmd',
    'brain/figures/disease-war-curing-costs-column-chart.qmd',
    'brain/figures/disease-vs-war-annual-deaths-pie-chart.qmd',
    'brain/figures/disease-vs-curing-costs-column-chart.qmd',
    'brain/figures/disease-burden-war-curing-comparison.qmd',
    'brain/figures/dfda-investment-returns-bar-chart.qmd',
]


def generate_title_from_filename(filename: str) -> str:
    """Generate a title from a filename."""
    # Remove .png extension and convert hyphens to spaces
    name = filename.replace('.png', '').replace('-', ' ')
    # Capitalize each word
    return ' '.join(word.capitalize() for word in name.split())


def update_chart_file(filepath: Path) -> bool:
    """Update a single chart file with metadata. Returns True if modified."""
    content = filepath.read_text(encoding='utf-8')

    # Skip if already has add_png_metadata
    if 'add_png_metadata' in content:
        print(f'[OK] {filepath.name} - already updated')
        return False

    # Skip if no plt.savefig
    if 'plt.savefig' not in content:
        print(f'[SKIP] {filepath.name} - no plt.savefig found')
        return False

    original = content

    # 1. Add add_png_metadata to imports
    import_pattern = r'from brain\.figures\._chart_style import \(([\s\S]*?)\)'
    import_match = re.search(import_pattern, content)

    if import_match:
        imports = import_match.group(1)
        if 'add_png_metadata' not in imports:
            # Add to imports (on new line before closing paren)
            updated_imports = imports.rstrip() + ',\n    add_png_metadata'
            content = re.sub(
                import_pattern,
                f'from brain.figures._chart_style import ({updated_imports})',
                content
            )

    # 2. Find and update plt.savefig calls
    # Pattern: plt.savefig(output_dir / 'filename.png', dpi=..., ...)
    savefig_pattern = r"plt\.savefig\(output_dir / '([^']+)'(.*?)\)"

    def replace_savefig(match):
        filename = match.group(1)
        args = match.group(2)
        title = generate_title_from_filename(filename)

        return f"""output_path = output_dir / '{filename}'

# Save the figure
plt.savefig(output_path{args})

# Add metadata for attribution
add_png_metadata(output_path, title="{title}")"""

    content = re.sub(savefig_pattern, replace_savefig, content)

    # Check if we made changes
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        print(f'[UPDATED] {filepath.name}')
        return True
    else:
        print(f'[SKIP] {filepath.name} - no changes needed')
        return False


def main():
    """Process all chart files."""
    root = Path.cwd()
    print('Updating chart files with metadata...\n')

    updated_count = 0
    for file_path in CHART_FILES:
        full_path = root / file_path
        try:
            if full_path.exists():
                if update_chart_file(full_path):
                    updated_count += 1
            else:
                print(f'[ERROR] {file_path} - file not found')
        except Exception as e:
            print(f'[ERROR] {file_path} - error: {e}')

    print(f'\nDone! Updated {updated_count} files.')


if __name__ == '__main__':
    main()
