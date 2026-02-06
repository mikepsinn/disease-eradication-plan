#!/usr/bin/env python3
"""
YAML Synchronization Utilities
================================

Functions for syncing metadata between QMD frontmatter and Quarto YAML configs.

Key features:
- Parse YAML frontmatter from QMD files
- Substitute Quarto variables with plain text values
- Update YAML configs while preserving formatting
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

# Handle import from different contexts (direct run vs imported from scripts/)
try:
    from quarto_config_utils import SKIP_CONFIG_FILES
except ModuleNotFoundError:
    # Add scripts/lib to path if not already there
    _lib_dir = Path(__file__).parent
    if str(_lib_dir) not in sys.path:
        sys.path.insert(0, str(_lib_dir))
    from quarto_config_utils import SKIP_CONFIG_FILES


def parse_qmd_frontmatter(qmd_path: Path) -> Dict[str, Any]:
    """
    Parse YAML frontmatter from QMD file.

    Args:
        qmd_path: Path to QMD file

    Returns:
        Dictionary with frontmatter fields (title, description, etc.)
    """
    if not qmd_path.exists():
        return {}

    content = qmd_path.read_text(encoding='utf-8')
    yaml_match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n', content)

    if not yaml_match:
        return {}

    try:
        frontmatter = yaml.safe_load(yaml_match.group(1))
        return frontmatter if isinstance(frontmatter, dict) else {}
    except Exception as e:
        print(f"[WARN] Failed to parse frontmatter in {qmd_path}: {e}")
        return {}


def substitute_quarto_variables(text: str, variables: Dict[str, Any]) -> str:
    """
    Replace Quarto variables {{< var name >}} with their plain text values from _variables.yml.

    Args:
        text: Text containing Quarto variable placeholders
        variables: Dictionary loaded from _variables.yml

    Returns:
        Text with variables replaced by plain text values (no HTML markup)
    """
    def extract_visible_text_from_html(html: str) -> str:
        """Extract only the visible text from HTML, stripping all tags and attributes."""
        # Remove HTML tags but keep the text content
        # First, extract text from the innermost span (the visible value)
        # Pattern matches: >visible text here</span> or >visible text here</a>

        # For parameter links, extract text between the last > and first </
        # This gets the visible value like "$21.8B" or "565B DALYs"
        text_match = re.search(r'>([^<>]+)</(?:span|a)>\s*$', html)
        if text_match:
            return text_match.group(1).strip()

        # Fallback: strip all HTML tags
        clean = re.sub(r'<[^>]+>', '', html)
        return clean.strip()

    def replace_var(match):
        var_name = match.group(1).strip()

        # Look up variable in _variables.yml
        var_data = variables.get(var_name, {})

        # Extract plain text value (without HTML tooltip)
        if isinstance(var_data, dict):
            # Try to get the plain value first
            if 'value' in var_data:
                return str(var_data['value'])
            # Otherwise try to extract from HTML string
            if 'html' in var_data:
                html = var_data['html']
                return extract_visible_text_from_html(html)
        elif isinstance(var_data, str):
            # If it's a simple string, extract visible text from HTML if present
            if '<' in var_data and '>' in var_data:
                return extract_visible_text_from_html(var_data)
            return var_data

        # Fallback: keep original placeholder
        return match.group(0)

    # Match {{< var variable_name >}}
    pattern = r'\{\{<\s*var\s+([a-zA-Z0-9_]+)\s*>\}\}'
    return re.sub(pattern, replace_var, text)


def escape_yaml_string(text: str) -> str:
    """
    Escape a string for use in YAML, using quotes if needed.

    Args:
        text: String to escape

    Returns:
        Properly quoted YAML string
    """
    # If the text contains special characters, use double quotes and escape
    if any(c in text for c in ['"', '\n', ':', '#', '<', '>']):
        # Escape double quotes and backslashes
        escaped = text.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    # If it contains single quotes, use double quotes
    elif "'" in text:
        return f'"{text}"'
    # Otherwise use single quotes for safety
    else:
        return f"'{text}'"


def normalize_abstract(abstract_text: str) -> str:
    """
    Normalize a multi-line abstract to a single line for YAML metadata.

    Strips leading/trailing whitespace, collapses multiple spaces, and joins lines.

    Args:
        abstract_text: Raw abstract text (possibly multi-line from YAML block scalar)

    Returns:
        Single-line abstract text
    """
    if not abstract_text:
        return ""
    # Replace newlines with spaces, collapse multiple spaces
    normalized = re.sub(r'\s+', ' ', abstract_text.strip())
    return normalized


def strip_confidence_intervals(text: str) -> str:
    """
    Remove inline confidence intervals from text for cleaner abstracts.

    Academically appropriate since abstracts typically omit inline CIs for readability.
    The full CIs remain in the body text where variables are rendered with tooltips.

    Args:
        text: Text potentially containing confidence interval patterns

    Returns:
        Text with CI patterns like "(95% CI: value-value)" removed
    """
    if not text:
        return ""
    # Pattern: (95% CI: value-value) or (90% CI: value-value)
    # Handles various value formats: $1.2B, 5.7k diseases, 10%, etc.
    ci_pattern = r'\s*\(\d+%\s*CI:\s*[^)]+\)'
    cleaned = re.sub(ci_pattern, '', text)
    # Clean up any double spaces left behind
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
    return cleaned.strip()


def sync_descriptions_to_yaml_configs(project_root: Path, variables_path: Path):
    """
    Sync descriptions, titles, and abstracts from QMD frontmatter to Quarto YAML configs.

    This ensures SEO metadata in YAML configs stays in sync with QMD frontmatter,
    with Quarto variables replaced by their plain text values.

    Uses text-based replacement to preserve exact YAML formatting.

    Args:
        project_root: Path to project root directory
        variables_path: Path to _variables.yml file
    """
    print("[*] Syncing descriptions and abstracts from QMD frontmatter to YAML configs...")

    # Load variables for substitution
    if not variables_path.exists():
        print(f"[WARN] {variables_path} not found - skipping description sync")
        return

    with open(variables_path, 'r', encoding='utf-8') as f:
        variables = yaml.safe_load(f) or {}

    # Find all Quarto config files (exclude _build_temp/ and non-syncable configs)
    yaml_configs = [
        f for f in project_root.glob('_quarto-*.yml')
        if '_build_temp' not in str(f) and f.name not in SKIP_CONFIG_FILES
    ]

    updated_count = 0
    skipped_count = 0

    for yaml_path in yaml_configs:
        try:
            # Read YAML content as text
            content = yaml_path.read_text(encoding='utf-8')

            # Parse to get index-source
            config = yaml.safe_load(content)
            index_source = config.get('dih-render', {}).get('index-source')
            if not index_source:
                skipped_count += 1
                continue

            qmd_path = project_root / index_source
            if not qmd_path.exists():
                print(f"[WARN] Source QMD not found: {index_source} (referenced by {yaml_path.name})")
                skipped_count += 1
                continue

            # Parse QMD frontmatter
            frontmatter = parse_qmd_frontmatter(qmd_path)
            if not frontmatter:
                skipped_count += 1
                continue

            # Extract title, description, and abstract with variable substitution
            title = frontmatter.get('title', '')
            description = frontmatter.get('description', '')
            abstract = frontmatter.get('abstract', '')

            if not title and not description and not abstract:
                skipped_count += 1
                continue

            # Substitute Quarto variables with plain text
            if title:
                title = substitute_quarto_variables(title, variables)
            if description:
                description = substitute_quarto_variables(description, variables)
                description = strip_confidence_intervals(description)
            if abstract:
                # Normalize multi-line abstract to single line and substitute variables
                abstract = normalize_abstract(abstract)
                abstract = substitute_quarto_variables(abstract, variables)
                abstract = strip_confidence_intervals(abstract)

            # Check if updates are needed
            # Note: title/description can be in 'website' or 'book' section
            # But 'abstract' is ONLY valid in 'book' section (not website)
            website_section = config.get('website', {})
            book_section = config.get('book', {})
            is_book_project = bool(book_section)

            # Get current values from the appropriate section
            current_title = website_section.get('title', '') or book_section.get('title', '')
            current_desc = website_section.get('description', '') or book_section.get('description', '')
            # Abstract only valid for book projects
            current_abstract = book_section.get('abstract', '') if is_book_project else ''

            # For website projects, don't compare/sync abstract (not a valid property)
            if not is_book_project:
                abstract = ''

            if title == current_title and description == current_desc and abstract == current_abstract:
                continue

            # Update using text replacement to preserve formatting
            updated = False
            if title and title != current_title:
                # Find and replace title line (in website or book section)
                title_pattern = r'(^  title:\s*)["\']?.*?["\']?\s*$'
                title_replacement = f'  title: {escape_yaml_string(title)}'
                new_content = re.sub(title_pattern, title_replacement, content, count=1, flags=re.MULTILINE)
                if new_content != content:
                    content = new_content
                    updated = True

            if description and description != current_desc:
                # Find and replace description line (in website or book section)
                desc_pattern = r'(^  description:\s*)["\']?.*?["\']?\s*$'
                desc_replacement = f'  description: {escape_yaml_string(description)}'
                new_content = re.sub(desc_pattern, desc_replacement, content, count=1, flags=re.MULTILINE)
                if new_content != content:
                    content = new_content
                    updated = True

            if abstract and abstract != current_abstract and is_book_project:
                # Find and replace abstract (handles both single-line and multi-line YAML blocks)
                # Pattern 1: Multi-line literal block (abstract: | or abstract: >)
                # Matches from "abstract:" through all indented continuation lines
                multiline_pattern = r'^  abstract:\s*[|>][-+]?\s*\n(?:    .+\n)*'
                multiline_match = re.search(multiline_pattern, content, flags=re.MULTILINE)

                # Pattern 2: Single-line quoted or unquoted abstract
                singleline_pattern = r'^  abstract:\s*["\']?[^|\n>][^\n]*["\']?\s*$'
                singleline_match = re.search(singleline_pattern, content, flags=re.MULTILINE)

                abstract_replacement = f'  abstract: {escape_yaml_string(abstract)}'

                if multiline_match:
                    # Replace entire multi-line block with single-line
                    content = content[:multiline_match.start()] + abstract_replacement + '\n' + content[multiline_match.end():]
                    updated = True
                elif singleline_match:
                    # Replace single-line abstract
                    content = content[:singleline_match.start()] + abstract_replacement + content[singleline_match.end():]
                    updated = True
                else:
                    # Abstract line doesn't exist yet - add it after description in book section
                    # Look for description line in the book section
                    desc_line_pattern = r'(^  description:\s*["\']?.*?["\']?\s*$)'
                    desc_match = re.search(desc_line_pattern, content, flags=re.MULTILINE)
                    if desc_match:
                        insert_pos = desc_match.end()
                        abstract_line = f'\n  abstract: {escape_yaml_string(abstract)}'
                        content = content[:insert_pos] + abstract_line + content[insert_pos:]
                        updated = True

            if updated:
                # Write back with original line endings
                yaml_path.write_text(content, encoding='utf-8')
                print(f"[OK] Updated {yaml_path.name}")
                if title and title != current_title:
                    print(f"     Title: {title[:80]}...")
                if description and description != current_desc:
                    print(f"     Description: {description[:80]}...")
                if abstract and abstract != current_abstract:
                    print(f"     Abstract: {abstract[:80]}...")
                updated_count += 1

        except Exception as e:
            print(f"[WARN] Failed to sync {yaml_path.name}: {e}")
            import traceback
            traceback.print_exc()
            skipped_count += 1
            continue

    print(f"[OK] Synced {updated_count} YAML configs, skipped {skipped_count}")
    print()
