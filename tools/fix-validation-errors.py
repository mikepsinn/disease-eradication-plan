#!/usr/bin/env python3
"""
Fix common validation errors found in QMD files.

This script automatically fixes:
1. Broken links to economic_parameters.py
2. Links to .md files that should be .qmd
3. Em-dash character encoding issues
4. Placeholder links (comments them out)
5. References to non-existent strategy/economic-models files
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Track changes made
changes_made = []


def fix_economic_parameters_link(content: str, filepath: str) -> str:
    """Fix broken links to economic_parameters.py"""
    old_pattern = r'\[([^\]]+)\]\(\.\.\/economic_parameters\.py\)'
    new_link = '../../dih_models/parameters.py'

    if re.search(old_pattern, content):
        content = re.sub(old_pattern, rf'[\1]({new_link})', content)
        changes_made.append(f"{filepath}: Fixed economic_parameters.py link")

    return content


def fix_md_to_qmd_links(content: str, filepath: str) -> str:
    """Fix links to .md files that are now .qmd in careers directory"""
    careers_files = [
        'elections-ie-compliance-lead',
        'growth-referrals-lead',
        'ai-engineer',
        'capital-markets-lead',
        'peace-dividend-analytics-lead',
        'security-audit-lead',
        'hiring-plan'
    ]

    for filename in careers_files:
        old_pattern = rf'\[([^\]]+)\]\(\.\/({filename})\.md\)'
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, rf'[\1](./\2.qmd)', content)
            changes_made.append(f"{filepath}: Fixed {filename}.md → .qmd")

    return content


def fix_em_dashes(content: str, filepath: str) -> str:
    """Fix em-dash character encoding issues (� character)"""
    if '�' in content:
        # Replace � with proper em-dash
        content = content.replace('�', '—')
        changes_made.append(f"{filepath}: Fixed em-dash encoding")

    return content


def comment_placeholder_links(content: str, filepath: str) -> str:
    """Comment out placeholder links like {Record URL}"""
    lines = content.split('\n')
    modified = False

    for i, line in enumerate(lines):
        if '{Record URL}' in line:
            # Comment out the line
            if not line.strip().startswith('<!--'):
                lines[i] = f'<!-- {line} -->'
                modified = True

    if modified:
        content = '\n'.join(lines)
        changes_made.append(f"{filepath}: Commented out placeholder {{Record URL}}")

    return content


def comment_broken_strategy_links(content: str, filepath: str) -> str:
    """Comment out links to non-existent strategy/economic-models files"""
    broken_links = [
        '../strategy/1-percent-treaty/victory-bonds-tokenomics.md',
        '../economic-models/victory-bond-investment-thesis.md',
        '../strategy/legal-compliance-framework.md',
        '../strategy/referral-rewards-system.md',
        '../strategy/incentives-layer.md',
        '../economic-models/operational-budget-and-financial-model.md',
        '../reference/organizational-precedents.md',
        '../economic-models/peace-dividend-value-capture.md',
        '../strategy/1-percent-treaty/dih-org-structure.md',
        '../features/treasury/dih-treasury-architecture.md',
        './national-security-argument.md',
        '../../reference/recovery-trial-case-study.md',
        './roadmap.md',
        '../economic-models/fundraising-and-budget-plan.md',
        './open-ecosystem-and-bounty-model.md',
        './wiki-restructuring-plan.md',
        '../community/nonprofit-partnership-incentives.md'
    ]

    lines = content.split('\n')
    modified = False

    for i, line in enumerate(lines):
        for broken_link in broken_links:
            if broken_link in line and not line.strip().startswith('<!--'):
                # Comment out the line
                lines[i] = f'<!-- TODO: Fix broken link - {line.strip()} -->'
                modified = True
                break

    if modified:
        content = '\n'.join(lines)
        changes_made.append(f"{filepath}: Commented out broken strategy/economic-models links")

    return content


def process_file(filepath: Path) -> bool:
    """Process a single QMD file and apply all fixes"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply all fixes
        content = fix_economic_parameters_link(content, str(filepath))
        content = fix_md_to_qmd_links(content, str(filepath))
        content = fix_em_dashes(content, str(filepath))
        content = comment_placeholder_links(content, str(filepath))
        content = comment_broken_strategy_links(content, str(filepath))

        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def main():
    """Main function to process all QMD files"""
    project_root = Path(__file__).parent.parent
    knowledge_dir = project_root / 'knowledge'

    # Find all QMD files in knowledge directory
    qmd_files = list(knowledge_dir.rglob('*.qmd'))

    print(f"Found {len(qmd_files)} QMD files to process")

    files_modified = 0
    for qmd_file in qmd_files:
        if process_file(qmd_file):
            files_modified += 1

    print(f"\nProcessed {len(qmd_files)} files")
    print(f"Modified {files_modified} files")
    print(f"\nChanges made:")
    for change in changes_made:
        print(f"  - {change}")

    print(f"\nTotal changes: {len(changes_made)}")


if __name__ == '__main__':
    main()
