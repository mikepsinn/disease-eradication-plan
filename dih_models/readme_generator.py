#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README generator from QMD source files.

Generates README.md with a strategic structure designed to drive action:
1. Compelling hook with key statistics
2. Clear problem/solution framing
3. Call to action (vote on referendum)
4. Papers listing
5. Contributor guide
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Optional

from .variable_replacement import (
    load_variables,
    replace_variables,
    clean_for_readme,
)


def strip_confidence_intervals(text: str) -> str:
    """
    Remove (95% CI: ...) parentheticals for cleaner README prose.

    Keeps the base value but removes verbose uncertainty ranges.
    """
    # Pattern: (95% CI: anything-anything)
    text = re.sub(r'\s*\(95% CI:[^)]+\)', '', text)
    return text


def clean_value_for_prose(value: str) -> str:
    """
    Clean a variable value for use in README prose.

    Strips units and formats for readability.
    """
    # Remove common unit suffixes that make prose awkward
    value = re.sub(r'\s*deaths/day$', '', value)
    value = re.sub(r'\s*deaths$', '', value)
    value = re.sub(r'\s*lives$', '', value)
    value = re.sub(r'\s*diseases/year$', '', value)

    # Convert ratio format "604:1" to "600x" for readability
    ratio_match = re.match(r'^(\d+(?:\.\d+)?):1$', value)
    if ratio_match:
        num = float(ratio_match.group(1))
        # Round to nice number
        if num >= 100:
            value = f"{int(round(num, -1))}x"
        else:
            value = f"{num:.0f}x"

    return value


def fix_relative_paths(content: str, source_dir: str) -> str:
    """
    Fix relative paths in content for README at project root.

    Args:
        content: Markdown content with relative paths
        source_dir: Directory of the source file relative to project root

    Returns:
        Content with paths adjusted for project root
    """
    if not source_dir:
        return content

    # Fix image paths: ![...](../assets/...) -> ![...](assets/...)
    content = re.sub(
        r'\]\(\.\./assets/',
        '](assets/',
        content
    )

    # Fix markdown links from subdirectories
    content = re.sub(
        r'\]\(\.\./([^)]+\.qmd)',
        r'](\1',
        content
    )

    return content


def extract_content_after_frontmatter(content: str) -> str:
    """Extract content after YAML frontmatter."""
    lines = content.split('\n')
    in_frontmatter = False
    frontmatter_end = 0

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                frontmatter_end = i + 1
                break

    return '\n'.join(lines[frontmatter_end:])


def generate_readme(
    project_root: Path,
    variables_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Generate README.md with strategic structure for project success.

    Args:
        project_root: Root directory of the project
        variables_path: Path to _variables.yml
        output_path: Path for output README

    Returns:
        Path to the generated README.md
    """
    if variables_path is None:
        variables_path = project_root / "_variables.yml"
    if output_path is None:
        output_path = project_root / "README.md"

    # Load variables
    variables = load_variables(variables_path)
    print(f"[*] Loaded {len(variables)} variables for README generation")

    # Helper to resolve variables and clean for README prose
    def v(text: str, clean_units: bool = True) -> str:
        result = replace_variables(text, variables, highlight_missing=False)
        result = strip_confidence_intervals(result)
        if clean_units:
            result = clean_value_for_prose(result)
        return result

    # Build README content
    readme_parts = []


    papers_qmd = project_root / "knowledge" / "papers.qmd"
    if papers_qmd.exists():
        print(f"[*] Processing {papers_qmd.name}...")
        with open(papers_qmd, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract content after frontmatter
        content = extract_content_after_frontmatter(content)

        # Remove the "# Papers & Publications" header and intro paragraph
        content = re.sub(r'# Papers & Publications\s*\n', '', content)
        content = re.sub(r'This page provides an index[^\n]*\n+', '', content)
        content = re.sub(r'produced as part of[^\n]*\n+', '', content)

        # Replace variables and strip CI ranges for cleaner prose
        content = replace_variables(content, variables, highlight_missing=False)
        content = strip_confidence_intervals(content)

        # Clean Quarto-specific syntax
        content = clean_for_readme(content)

        # Fix relative paths for README at project root
        content = fix_relative_paths(content, "knowledge")

        # Strip HTML comments (e.g., submission info blocks)
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        # Clean up excess blank lines left by removed comments
        content = re.sub(r'\n{3,}', '\n\n', content)

        readme_parts.append(content)
    else:
        print(f"[WARN] {papers_qmd} not found")
        readme_parts.append("See [warondisease.org](https://warondisease.org) for full documentation.\n\n")


    # ===================
    # 6. DEVELOPER SETUP
    # ===================
    readme_parts.append("## Development\n\n")

    readme_parts.append("This is a [Quarto](https://quarto.org/) book project with Python-based parameter calculations.\n\n")

    readme_parts.append("### Quick Start\n\n")
    readme_parts.append("```bash\n")
    readme_parts.append("# Clone and setup\n")
    readme_parts.append("git clone https://github.com/wishonia/disease-eradication-plan.git\n")
    readme_parts.append("cd disease-eradication-plan\n")
    readme_parts.append("python -m venv .venv\n")
    readme_parts.append(".venv/Scripts/activate  # Windows\n")
    readme_parts.append("# source .venv/bin/activate  # macOS/Linux\n")
    readme_parts.append("pip install -r requirements.txt\n\n")
    readme_parts.append("# Generate variables and render\n")
    readme_parts.append("python scripts/generate-everything-parameters-variables-calculations-references.py\n")
    readme_parts.append("quarto render\n")
    readme_parts.append("```\n\n")

    readme_parts.append("### Key Files\n\n")
    readme_parts.append("- `dih_models/parameters.py` - All calculations and variables\n")
    readme_parts.append("- `_variables.yml` - Generated Quarto variables with tooltips\n")
    readme_parts.append("- `knowledge/` - All content organized by topic\n")
    readme_parts.append("- `CONTRIBUTING.md` - Writing standards and style guide\n\n")

    readme_parts.append("See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.\n\n")

    # Combine and write
    readme_content = ''.join(readme_parts)

    # Final cleanup
    readme_content = readme_content.replace('\r\n', '\n')
    readme_content = re.sub(r'\n{4,}', '\n\n\n', readme_content)

    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(readme_content)

    print(f"[OK] Generated {output_path.relative_to(project_root)}")
    return output_path
