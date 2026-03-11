"""
Quarto Config Synchronization
=============================

Syncs shared settings from _quarto-shared-defaults.yml to all paper/site configs.

Uses text-based insertion to PRESERVE all original formatting.
Only ADDS missing keys - never modifies existing content.

Usage:
    from dih_models.quarto_config_sync import sync_shared_config_settings
    sync_shared_config_settings(project_root)
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Set
import re
import sys

logger = logging.getLogger("dih.quarto_config_sync")

from dih_models.yaml_utils import load_quarto_config

# Import shared config skip list from scripts/lib
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))
from quarto_config_utils import SKIP_CONFIG_FILES


# Metadata keys that should be synced (nested under "metadata")
# Only ADD these if missing - never overwrite existing values
SYNC_METADATA_KEYS = {
    # Author identification
    "creator",
    "orcid",
    "orcid-url",
    "primary-author",
    "byline",
    "human-author",
    # Contact
    "author-email",
    "author-url",
    "author-website",
    "contact",
    # Academic profiles
    "github-profile",
    "google-scholar",
    # Social profiles
    "linkedin",
    # Language
    "language",
    # Legal (these are universal)
    "copyright",
    "copyright-year",
    "license",
    "license-url",
    "rights",
    # Publisher (universal)
    "publisher",
    "publisher-url",
    "publisher-name",
    "publisher-email",
    # Social (universal)
    "twitter-site",
    "twitter-creator",
    # Open Graph (base setting)
    "open-graph",
    # Academic statements (universal)
    "funding",
    "data-availability",
    "coi-statement",
    "ethics-statement",
}

# Metadata keys to SKIP - these are intentionally site-specific
SKIP_METADATA_KEYS = {
    "version",
    "edition",
    "audience",
    "genre",
    "format",  # Site-specific: "Website", "Working Paper", etc.
    "type",    # Site-specific: "Economic Analysis", "Policy Framework", etc.
    "medium",
    "subject",
    "category",
    "keywords",  # Site-specific
    "image",     # Site-specific OG image
    "doi",       # Site-specific DOI
    "publishing",  # Site-specific publication tracking
    "geographic-coverage",
    "repo-url",
    "issue-url",
    "source-url",
}

# Format HTML keys that should be synced (ADD only if missing)
SYNC_FORMAT_HTML_KEYS = {
    "theme",              # Consistent theme across all papers (cosmo)
    "filters",            # Shared paper rendering filters
    "link-citations",     # Make citations clickable
    "citation-hover",     # Show citation preview on hover
    "smooth-scroll",      # Smooth scrolling for anchor links
    "code-fold",          # Collapsible code blocks
    "code-tools",         # Code copy button and source view
}

# Format PDF keys that should be synced (ADD only if missing)
SYNC_FORMAT_PDF_KEYS = {
    "filters",            # Shared paper rendering filters
}

# Note: SKIP_CONFIG_FILES is imported from quarto_config_utils
# Contains: _quarto.yml, _quarto-manual.yml, _quarto-test.yml, _quarto-shared-defaults.yml


def load_yaml_for_check(path: Path) -> Dict[str, Any]:
    """Load YAML for checking what keys exist (read-only)."""
    return load_quarto_config(path)


def find_section_end(lines: List[str], section_pattern: str, indent: int) -> int:
    """
    Find the line number where a section ends.
    A section ends when we hit a line with less or equal indentation (non-comment, non-blank).
    """
    section_started = False
    section_indent = 0

    for i, line in enumerate(lines):
        # Check if this is the section start
        if re.match(section_pattern, line):
            section_started = True
            section_indent = len(line) - len(line.lstrip())
            continue

        if section_started:
            stripped = line.rstrip()
            if not stripped or stripped.startswith('#'):
                continue  # Skip blank lines and comments

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= section_indent:
                # Found a line with same or less indentation - section ended
                return i

    return len(lines)  # Section goes to end of file


def format_yaml_value(value: Any) -> str:
    """Format a value for YAML output."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "[" + ", ".join(format_yaml_value(item) for item in value) + "]"
    if isinstance(value, str):
        # Check if value needs quoting
        if any(c in value for c in ":#{}[]|>&*!?,\n") or value.startswith(("@", "`", '"', "'")):
            # Use double quotes and escape internal quotes
            return f'"{value}"'
        return value
    return str(value)


def insert_metadata_keys(
    content: str,
    defaults_meta: Dict[str, Any],
    existing_meta: Dict[str, Any]
) -> tuple[str, List[str]]:
    """
    Insert missing metadata keys into the config content.
    Returns (updated_content, list_of_changes)
    """
    changes = []
    lines = content.split('\n')

    # Find metadata section
    metadata_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^metadata:\s*$', line):
            metadata_idx = i
            break

    if metadata_idx == -1:
        return content, changes

    # Find where to insert (end of metadata section or before subsections like 'publishing:')
    # We want to insert after existing top-level metadata keys
    insert_idx = metadata_idx + 1
    in_subsection = False
    subsection_indent = 0

    for i in range(metadata_idx + 1, len(lines)):
        line = lines[i]
        stripped = line.rstrip()

        if not stripped or stripped.startswith('#'):
            insert_idx = i
            continue

        current_indent = len(line) - len(line.lstrip())

        # Check if we've exited metadata section
        if current_indent == 0 and not stripped.startswith(' '):
            break

        # Track subsections (like 'publishing:')
        if current_indent == 2 and stripped.endswith(':'):
            in_subsection = True
            subsection_indent = current_indent
            continue

        # If we're in a subsection with more indent, keep going
        if in_subsection and current_indent > subsection_indent:
            continue

        # If we hit something at indent 2 that's a key-value, record it
        if current_indent == 2 and not in_subsection:
            insert_idx = i + 1
            in_subsection = False

    # Build keys to insert
    keys_to_add = []
    for key in sorted(SYNC_METADATA_KEYS):
        if key in SKIP_METADATA_KEYS:
            continue
        if key not in existing_meta and key in defaults_meta:
            value = format_yaml_value(defaults_meta[key])
            keys_to_add.append(f'  {key}: {value}')
            changes.append(f"Added metadata.{key}")

    if keys_to_add:
        # Find a good insertion point - before any subsections
        for i in range(metadata_idx + 1, len(lines)):
            line = lines[i]
            stripped = line.rstrip()
            if not stripped:
                continue
            current_indent = len(line) - len(line.lstrip())
            # If we hit a subsection (like 'publishing:' with nested content), insert before it
            if current_indent == 2 and stripped.endswith(':') and i + 1 < len(lines):
                next_line = lines[i + 1]
                next_indent = len(next_line) - len(next_line.lstrip()) if next_line.strip() else 0
                if next_indent > 2:
                    insert_idx = i
                    break
            # If we've exited metadata section
            if current_indent == 0 and stripped and not stripped.startswith('#'):
                insert_idx = i
                break

        # Insert the new keys
        for key_line in reversed(keys_to_add):
            lines.insert(insert_idx, key_line)

    return '\n'.join(lines), changes


def insert_html_format_keys(
    content: str,
    defaults_html: Dict[str, Any],
    existing_html: Dict[str, Any]
) -> tuple[str, List[str]]:
    """
    Insert missing format.html keys into the config content.
    Returns (updated_content, list_of_changes)
    """
    changes = []
    lines = content.split('\n')

    # Find format: section, then html: subsection
    format_idx = -1
    html_idx = -1

    for i, line in enumerate(lines):
        if re.match(r'^format:\s*$', line):
            format_idx = i
        elif format_idx >= 0 and re.match(r'^  html:\s*$', line):
            html_idx = i
            break

    if html_idx == -1:
        return content, changes

    # Find end of html section (where indent goes back to 2 or less)
    insert_idx = html_idx + 1
    for i in range(html_idx + 1, len(lines)):
        line = lines[i]
        stripped = line.rstrip()

        if not stripped or stripped.startswith('#'):
            continue

        current_indent = len(line) - len(line.lstrip())

        # If indent is 2 or less (but not 0 if it's a blank), we've exited html section
        if current_indent <= 2:
            insert_idx = i
            break

        # Track the last valid position to insert
        insert_idx = i + 1

    # Build keys to insert
    keys_to_add = []
    for key in sorted(SYNC_FORMAT_HTML_KEYS):
        if key not in existing_html and key in defaults_html:
            value = format_yaml_value(defaults_html[key])
            keys_to_add.append(f'    {key}: {value}')
            changes.append(f"Added format.html.{key}")

    if keys_to_add:
        # Insert before the line where html section ends
        for key_line in reversed(keys_to_add):
            lines.insert(insert_idx, key_line)

    return '\n'.join(lines), changes


def insert_pdf_format_keys(
    content: str,
    defaults_pdf: Dict[str, Any],
    existing_pdf: Dict[str, Any]
) -> tuple[str, List[str]]:
    """
    Insert missing format.pdf keys into the config content.
    Returns (updated_content, list_of_changes)
    """
    changes = []
    lines = content.split('\n')

    # Find format: section, then pdf: subsection
    format_idx = -1
    pdf_idx = -1

    for i, line in enumerate(lines):
        if re.match(r'^format:\s*$', line):
            format_idx = i
        elif format_idx >= 0 and re.match(r'^  pdf:\s*$', line):
            pdf_idx = i
            break

    if pdf_idx == -1:
        return content, changes

    # Find end of pdf section (where indent goes back to 2 or less)
    insert_idx = pdf_idx + 1
    for i in range(pdf_idx + 1, len(lines)):
        line = lines[i]
        stripped = line.rstrip()

        if not stripped or stripped.startswith('#'):
            continue

        current_indent = len(line) - len(line.lstrip())

        if current_indent <= 2:
            insert_idx = i
            break

        insert_idx = i + 1

    # Build keys to insert
    keys_to_add = []
    for key in sorted(SYNC_FORMAT_PDF_KEYS):
        if key not in existing_pdf and key in defaults_pdf:
            value = format_yaml_value(defaults_pdf[key])
            keys_to_add.append(f'    {key}: {value}')
            changes.append(f"Added format.pdf.{key}")

    if keys_to_add:
        for key_line in reversed(keys_to_add):
            lines.insert(insert_idx, key_line)

    return '\n'.join(lines), changes


def sync_config_file(
    config_path: Path,
    defaults: Dict[str, Any],
    dry_run: bool = False
) -> List[str]:
    """
    Sync a single config file with shared defaults.
    Uses text insertion to preserve formatting.
    Returns list of changes made.
    """
    config = load_yaml_for_check(config_path)
    all_changes = []

    # Read file content
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert missing metadata keys
    if "metadata" in defaults:
        existing_meta = config.get("metadata", {})
        content, meta_changes = insert_metadata_keys(
            content, defaults["metadata"], existing_meta
        )
        all_changes.extend(meta_changes)

    # Insert missing format.html keys
    if "format" in defaults and "html" in defaults["format"]:
        existing_html = config.get("format", {}).get("html", {})
        content, html_changes = insert_html_format_keys(
            content, defaults["format"]["html"], existing_html
        )
        all_changes.extend(html_changes)

    # Insert missing format.pdf keys
    if "format" in defaults and "pdf" in defaults["format"]:
        existing_pdf = config.get("format", {}).get("pdf", {})
        content, pdf_changes = insert_pdf_format_keys(
            content, defaults["format"]["pdf"], existing_pdf
        )
        all_changes.extend(pdf_changes)

    # Write back if changes were made
    if all_changes and not dry_run:
        with open(config_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

    return all_changes


def sync_shared_config_settings(project_root: Path, dry_run: bool = False) -> Dict[str, List[str]]:
    """
    Sync shared settings from _quarto-shared-defaults.yml to all paper configs.

    ONLY adds missing keys using text insertion.
    Preserves all original formatting, comments, and structure.

    Args:
        project_root: Path to the project root
        dry_run: If True, only report what would change without writing

    Returns:
        Dict mapping config filename to list of changes made
    """
    defaults_path = project_root / "_quarto-shared-defaults.yml"
    if not defaults_path.exists():
        logger.warning("Shared defaults file not found: %s", defaults_path)
        return {}

    defaults = load_yaml_for_check(defaults_path)
    results = {}

    # Find all _quarto-*.yml files in root
    for config_path in sorted(project_root.glob("_quarto-*.yml")):
        if config_path.name in SKIP_CONFIG_FILES:
            continue

        changes = sync_config_file(config_path, defaults, dry_run)

        if changes:
            results[config_path.name] = changes

    return results


def report_config_drift(project_root: Path) -> Dict[str, List[str]]:
    """
    Report differences between configs and shared defaults.
    Useful for auditing which configs have drifted from the standard.
    """
    defaults_path = project_root / "_quarto-shared-defaults.yml"
    if not defaults_path.exists():
        return {}

    defaults = load_yaml_for_check(defaults_path)
    drift = {}

    for config_path in sorted(project_root.glob("_quarto-*.yml")):
        if config_path.name in SKIP_CONFIG_FILES:
            continue

        config = load_yaml_for_check(config_path)
        differences = []

        # Check metadata keys
        if "metadata" in defaults:
            config_meta = config.get("metadata", {})
            for key in sorted(SYNC_METADATA_KEYS):
                if key in SKIP_METADATA_KEYS:
                    continue
                if key in defaults["metadata"] and key not in config_meta:
                    differences.append(f"Missing: metadata.{key}")

        # Check format.html keys
        if "format" in defaults and "html" in defaults.get("format", {}):
            config_html = config.get("format", {}).get("html", {})
            for key in sorted(SYNC_FORMAT_HTML_KEYS):
                if key in defaults["format"]["html"] and key not in config_html:
                    differences.append(f"Missing: format.html.{key}")

        if "format" in defaults and "pdf" in defaults.get("format", {}):
            config_pdf = config.get("format", {}).get("pdf", {})
            for key in sorted(SYNC_FORMAT_PDF_KEYS):
                if key in defaults["format"]["pdf"] and key not in config_pdf:
                    differences.append(f"Missing: format.pdf.{key}")

        if differences:
            drift[config_path.name] = differences

    return drift


if __name__ == "__main__":
    import sys

    project_root = Path(__file__).parent.parent

    if "--dry-run" in sys.argv:
        logger.debug("DRY RUN: Checking what would be synced...")
        results = sync_shared_config_settings(project_root, dry_run=True)
    elif "--report" in sys.argv:
        logger.debug("Reporting config drift from shared defaults...")
        results = report_config_drift(project_root)
    else:
        logger.debug("Syncing shared config settings...")
        results = sync_shared_config_settings(project_root)

    if results:
        for config_name, changes in results.items():
            logger.debug("\n%s:", config_name)
            for change in changes:
                logger.debug("  - %s", change)
        logger.debug("%d configs updated", len(results))
    else:
        logger.debug("All configs are in sync with shared defaults")
