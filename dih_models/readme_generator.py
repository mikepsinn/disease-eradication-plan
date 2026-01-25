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

    # Helper to resolve variables in text
    def v(text: str) -> str:
        return replace_variables(text, variables, highlight_missing=False)

    # Build README content
    readme_parts = []

    # Helper to resolve variables and clean for README prose
    def v(text: str, clean_units: bool = True) -> str:
        result = replace_variables(text, variables, highlight_missing=False)
        result = strip_confidence_intervals(result)
        if clean_units:
            result = clean_value_for_prose(result)
        return result

    # ===================
    # 1. HOOK / HEADER
    # ===================
    readme_parts.append("# Disease Eradication Plan\n\n")

    readme_parts.append("Hello, humans.\n\n")

    readme_parts.append("I am WISHONIA. I've been watching your species for 80 years, and I have notes.\n\n")

    readme_parts.append("Every day, **" + v("{{< var global_disease_deaths_daily >}}") + " of you permanently stop existing** from diseases that are basically just engineering problems with meat robots.\n\n")

    readme_parts.append("Meanwhile, you spend **" + v("{{< var military_to_government_clinical_trials_spending_ratio >}}") + " more** on weapons than on clinical trials to test cures. You've tested less than 1% of possible drug-disease combinations. The bottleneck isn't science. It's that you decided testing cures isn't worth funding.\n\n")

    readme_parts.append("This is like buying 600 umbrellas while your house is on fire.\n\n")

    # ===================
    # 2. THE SOLUTION
    # ===================
    readme_parts.append("## The Fix: A 1% Treaty\n\n")

    readme_parts.append("Every nation redirects **1%** of their murder budget (" + v("{{< var treaty_annual_funding >}}", clean_units=False) + "/year) to fund hyper-efficient clinical trials.\n\n")

    readme_parts.append("- Security balance unchanged (" + v("{{< var global_military_spending_post_treaty_annual_2024 >}}", clean_units=False) + " left for war stuff)\n")
    readme_parts.append("- Trial costs drop " + v("{{< var dfda_trial_cost_reduction_factor >}}") + " through automation\n")
    readme_parts.append("- " + v("{{< var dfda_efficacy_lag_elimination_deaths_averted >}}") + " humans could stop dying unnecessarily\n\n")

    readme_parts.append("You'd still have enough nuclear weapons to end civilization 20 times. If you can't do it in 19 attempts, the 20th probably wasn't going to help.\n\n")

    # ===================
    # 3. CALL TO ACTION
    # ===================
    readme_parts.append("## 🗳️ Vote Yes at [warondisease.org](https://warondisease.org)\n\n")

    readme_parts.append("When " + v("{{< var global_population_activism_threshold_pct >}}", clean_units=False) + " of humans want something, they usually get it. Click yes. Tell your friends. Stop dying from stupid things.\n\n")

    # ===================
    # 4. THE EVIDENCE (Papers)
    # ===================
    readme_parts.append("## Research & Papers\n\n")

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

        readme_parts.append(content)
    else:
        print(f"[WARN] {papers_qmd} not found")
        readme_parts.append("See [warondisease.org](https://warondisease.org) for full documentation.\n\n")

    # ===================
    # 5. HOW TO HELP
    # ===================
    readme_parts.append("\n## How to Help\n\n")

    readme_parts.append("### Spread the Word\n")
    readme_parts.append("- Share [warondisease.org](https://warondisease.org) with your network\n")
    readme_parts.append("- The key stat: **" + v("{{< var global_disease_deaths_daily >}}") + " people die daily** from curable diseases\n\n")

    readme_parts.append("### Contribute to the Project\n")
    readme_parts.append("- **Fact-checking**: Every parameter is sourced, but humans make mistakes\n")
    readme_parts.append("- **Writing**: Make content clearer, more persuasive\n")
    readme_parts.append("- **Research**: Find better sources, update statistics\n")
    readme_parts.append("- **Translation**: Help reach non-English speakers\n\n")

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

    # ===================
    # 7. FOOTER
    # ===================
    readme_parts.append("---\n\n")
    readme_parts.append("*WISHONIA*\n\n")
    readme_parts.append("*World Integrated System for High-Efficiency Optimization, Networked Intelligence, and Allocation*\n\n")
    readme_parts.append("*Still Watching. Still Concerned. Now Accepting Pull Requests.*\n\n")
    readme_parts.append("P.S. " + v("{{< var global_disease_deaths_daily >}}") + " humans died today from diseases you could cure. Tomorrow, the same. Every day until you act.\n")

    # Combine and write
    readme_content = ''.join(readme_parts)

    # Final cleanup
    readme_content = readme_content.replace('\r\n', '\n')
    readme_content = re.sub(r'\n{4,}', '\n\n\n', readme_content)

    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(readme_content)

    print(f"[OK] Generated {output_path.relative_to(project_root)}")
    return output_path
