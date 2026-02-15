#!/usr/bin/env python3
"""
Validate Quarto Render Output

This script checks rendered HTML files for common issues:
1. Unrendered inline Python expressions (literal `{python}` in output)
2. Blacklisted patterns (findfont warnings, echo: false leaks, Python errors, frontmatter leaks, PosixPath objects)
3. Links to .qmd files (should be .html in rendered output)
4. Broken internal links (relative paths that don't exist)
5. Other rendering failures

Usage:
    python scripts/post-render-validation.py [--output-dir _manual/warondisease]

Exit codes:
    0 - All checks passed
    1 - Validation errors found
"""

import argparse
import json
import os
import re
import sys
import yaml
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, unquote

from lib.yaml_sync_utils import strip_confidence_intervals

# Set UTF-8 encoding for stdout
if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

# Detect GitHub Actions environment
IN_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
GITHUB_STEP_SUMMARY = os.environ.get("GITHUB_STEP_SUMMARY")


class ValidationError:
    def __init__(self, file_path, line_num, error_type, context):
        self.file_path = file_path
        self.line_num = line_num
        self.error_type = error_type
        self.context = context

    def __str__(self):
        return f"{self.file_path}:{self.line_num} [{self.error_type}] {self.context}"

    def get_source_file(self, output_dir: Path) -> str:
        """
        Convert HTML file path back to source QMD file path for annotations.
        Example: _manual/warondisease/knowledge/appendix/invisible-graveyard.html
              -> knowledge/appendix/invisible-graveyard.qmd
        """
        try:
            # Get path relative to output directory
            rel_path = Path(self.file_path).relative_to(output_dir)
            # Convert .html to .qmd
            qmd_path = rel_path.with_suffix('.qmd')
            return str(qmd_path)
        except ValueError:
            # If not relative to output_dir, just convert extension
            return str(Path(self.file_path).with_suffix('.qmd'))

    def emit_annotation(self, output_dir: Path):
        """Emit GitHub Actions annotation for this error."""
        if not IN_GITHUB_ACTIONS:
            return

        source_file = self.get_source_file(output_dir)
        # Escape special characters in message for GitHub Actions
        message = self.context.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
        # Truncate message if too long (GitHub has limits)
        if len(message) > 500:
            message = message[:497] + "..."

        # Format: ::error file={name},line={line},title={title}::{message}
        annotation = f"::error file={source_file},line={self.line_num},title={self.error_type}::{message}"
        print(annotation, flush=True)


BLACKLISTED_PATTERNS = [
    {
        "regex": re.compile(r"<pre><code>[^<]*\$[^<]*(\\_|\\[a-zA-Z]|\{|_\{)[^<]*</code></pre>", re.DOTALL),
        "error_type": "LATEX_IN_CODE_BLOCK",
        "message": "LaTeX math with commands found in <pre><code> block - should be rendered as math, not code",
        "skip_in_comments": True,
        "skip_in_scripts": False,
    },
    {
        "regex": re.compile(r"<pre><code>[^<]*\$\$[^<]*</code></pre>", re.DOTALL),
        "error_type": "LATEX_DISPLAY_MATH_IN_CODE",
        "message": "LaTeX display math ($$) found in <pre><code> block - should be rendered as math, not code",
        "skip_in_comments": True,
        "skip_in_scripts": False,
    },
    {
        "regex": re.compile(r"<pre><code>[^<]*(\\mathbf|\\text\{|\\alpha|\\beta|\\gamma|\\sum|\\int|\\frac)[^<]*</code></pre>", re.DOTALL),
        "error_type": "LATEX_COMMANDS_IN_CODE",
        "message": "LaTeX commands found in <pre><code> block - math should be rendered, not shown as code",
        "skip_in_comments": True,
        "skip_in_scripts": False,
    },
    {
        "regex": re.compile(r"findfont:", re.IGNORECASE),
        "error_type": "FINDFONT_WARNING",
        "message": "Matplotlib font warning in output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r"echo:\s*false", re.IGNORECASE),
        "error_type": "ECHO_FALSE_LEAK",
        "message": "Cell option 'echo: false' leaked into output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
        "skip_if": lambda line: line.strip().startswith("<!--") or "href=" in line or "class=" in line,
    },
    {
        "regex": re.compile(r"NameError:|AttributeError:|ImportError:|ModuleNotFoundError:|KeyError:|TypeError:"),
        "error_type": "PYTHON_ERROR",
        "message": "Python error in output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r"SyntaxWarning:"),
        "error_type": "PYTHON_SYNTAX_WARNING",
        "message": "Python SyntaxWarning in output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(
            r"lastToneElevationWithHumorHash|lastInstructionalVoiceHash|lastFormattedHash|lastFactCheckHash|lastStyleCheckHash|lastStructureCheckHash|lastLatexCheckHash|lastParamCheckHash"
        ),
        "error_type": "FRONTMATTER_LEAK",
        "message": "Frontmatter metadata leaked into output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r"<span[^>]*>[^<]*quarto-shortcode[^<]*</span>", re.IGNORECASE),
        "error_type": "QUARTO_SHORTCODE_TEXT",
        "message": "Quarto shortcode rendered as literal span text",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r"PosixPath\("),
        "error_type": "POSIXPATH_IN_OUTPUT",
        "message": "PosixPath object leaked into rendered output (should be converted to string)",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
    {
        "regex": re.compile(r"Try using xlabels", re.IGNORECASE),
        "error_type": "MATPLOTLIB_XLABELS_WARNING",
        "message": "Matplotlib xlabels warning in output",
        "skip_in_comments": True,
        "skip_in_scripts": True,
    },
]


def find_html_files(output_dir):
    """Find all HTML files in the output directory"""
    html_files = []
    for path in Path(output_dir).rglob("*.html"):
        # Skip site_libs and other infrastructure
        if "site_libs" not in str(path):
            html_files.append(path)
    return html_files


def check_unrendered_inline_python(content, file_path):
    """Check for literal `{python} ...` expressions in HTML output"""
    errors = []

    # Pattern: <code>{python} something</code>
    # This indicates inline Python didn't evaluate
    pattern = r"<code>\{python\}\s+([^<]+)</code>"

    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        matches = re.finditer(pattern, line)
        for match in matches:
            var_name = match.group(1).strip()
            context = f"Unrendered inline expression: `{{python}} {var_name}`"
            errors.append(ValidationError(file_path, i, "UNRENDERED_PYTHON", context))

    return errors


def check_dollar_python_pattern(content, file_path):
    """Check for literal `{python} ...` patterns in HTML output"""
    errors = []

    # Pattern: {python} something - this is the inline Python syntax that should be rendered
    # If it appears literally in the HTML, it means Quarto didn't evaluate it
    # Look for {python} followed by content (variable name or expression)
    # Pattern matches: {python} followed by word characters, dots, spaces, or simple expressions
    pattern = r"\{python\}\s*[^\s<}]+"

    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        # Skip HTML comments and script tags
        if "<!--" in line:
            continue
        if "<script" in line.lower():
            continue

        # Only skip if it's in a <pre><code> documentation block (multi-line code examples)
        # Don't skip standalone <code> tags - those are where unrendered inline Python appears!
        if "<pre" in line.lower() and "<code" in line.lower():
            # This is likely a code example showing syntax - skip it
            python_pos = line.find("{python}")
            if python_pos != -1:
                pre_start = line.lower().find("<pre")
                pre_end = line.lower().find("</pre>")
                if pre_start != -1 and pre_end != -1 and pre_start < python_pos < pre_end:
                    continue  # It's in a documentation code block, skip it

        matches = re.finditer(pattern, line)
        for match in matches:
            matched_text = match.group(0)
            # Extract context (first 100 chars)
            context_text = matched_text[:100].strip()
            # Get surrounding context (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(line), match.end() + 50)
            context = f"Unrendered {{python}} pattern: `{context_text}` (context: ...{line[start:end]}...)"
            errors.append(ValidationError(file_path, i, "UNRENDERED_PYTHON_INLINE", context))

    return errors


def check_blacklisted_strings(content, file_path):
    """Check for generic blacklisted string patterns in rendered output"""
    errors = []
    lines = content.split("\n")

    for pattern_config in BLACKLISTED_PATTERNS:
        regex = pattern_config["regex"]
        skip_in_comments = pattern_config.get("skip_in_comments", False)
        skip_in_scripts = pattern_config.get("skip_in_scripts", False)
        skip_if = pattern_config.get("skip_if", None)

        for i, line in enumerate(lines, 1):
            # Apply skip conditions
            if skip_in_comments and "<!--" in line:
                continue
            if skip_in_scripts and "<script" in line.lower():
                continue
            if skip_if and skip_if(line):
                continue

            # Check for pattern match
            match = regex.search(line)
            if match:
                # Get surrounding context (50 chars before and after match)
                start = max(0, match.start() - 50)
                end = min(len(line), match.end() + 50)
                snippet = line[start:end].strip()
                context = f"{pattern_config['message']}: ...{snippet}..."
                errors.append(ValidationError(file_path, i, pattern_config["error_type"], context))

    return errors


def check_qmd_file_links(content, file_path):
    """Check for links pointing to .qmd files (should be .html in rendered output)"""
    errors = []
    lines = content.split("\n")

    # Pattern to match href attributes that end with .qmd
    # Matches: href="something.qmd" or href='something.qmd' or href=something.qmd
    pattern = r'href\s*=\s*["\']?([^"\'>\s]+\.qmd(?:\?[^"\'>\s]*)?(?:#[^"\'>\s]*)?)["\']?'

    for i, line in enumerate(lines, 1):
        # Skip HTML comments and script tags
        if "<!--" in line:
            continue
        if "<script" in line.lower():
            continue

        matches = re.finditer(pattern, line, re.IGNORECASE)
        for match in matches:
            href_value = match.group(1)
            # Get surrounding context
            start = max(0, match.start() - 50)
            end = min(len(line), match.end() + 50)
            context = f"Link to .qmd file: `{href_value}` (context: ...{line[start:end]}...)"
            errors.append(ValidationError(file_path, i, "QMD_FILE_LINK", context))

    return errors


def check_broken_internal_links(content, file_path, output_dir):
    """Check for broken internal links (relative paths that don't exist)"""
    errors = []
    lines = content.split("\n")

    # Pattern to match href attributes and img src attributes
    # Matches: href="path" or href='path' or src="path" or src='path'
    href_pattern = r'href\s*=\s*["\']([^"\']+)["\']'
    img_pattern = r'src\s*=\s*["\']([^"\']+)["\']'

    # Get the directory containing the current HTML file
    file_dir = file_path.parent

    for i, line in enumerate(lines, 1):
        # Skip HTML comments and script tags
        if "<!--" in line:
            continue
        if "<script" in line.lower():
            continue

        # Check both href and img src attributes
        all_matches = []
        all_matches.extend([(match, 'href') for match in re.finditer(href_pattern, line)])
        all_matches.extend([(match, 'src') for match in re.finditer(img_pattern, line)])

        for match, attr_type in all_matches:
            href_value = match.group(1)

            # Skip external links (http, https, mailto, etc.)
            parsed = urlparse(href_value)
            if parsed.scheme in ('http', 'https', 'mailto', 'ftp', 'tel'):
                continue

            # Skip anchor-only links (fragments)
            if href_value.startswith('#'):
                continue

            # Skip data URIs and javascript: links
            if href_value.startswith('data:') or href_value.startswith('javascript:'):
                continue

            # This is an internal link - check if it exists
            # Decode URL encoding
            decoded_href = unquote(href_value)

            # Remove fragment if present
            if '#' in decoded_href:
                decoded_href = decoded_href.split('#')[0]

            # Resolve relative to current file's directory
            if decoded_href.startswith('/'):
                # Absolute path from output_dir root
                target_path = output_dir / decoded_href.lstrip('/')
            else:
                # Relative path from current file
                target_path = (file_dir / decoded_href).resolve()

            # Normalize the path (handle .. and .)
            try:
                target_path = target_path.resolve()
            except (OSError, ValueError):
                # Invalid path
                error_type = "BROKEN_IMAGE" if attr_type == 'src' else "BROKEN_LINK"
                context = f"Invalid {'image' if attr_type == 'src' else 'link'} path: `{href_value}` (context: ...{line[max(0, match.start()-50):min(len(line), match.end()+50)]}...)"
                errors.append(ValidationError(file_path, i, error_type, context))
                continue

            # Check if file exists
            # First check if it's a direct file path
            if target_path.exists():
                # Path exists, check if it's a directory
                if target_path.is_dir():
                    # Directory link - check for index.html (only for href, not img src)
                    if attr_type == 'href':
                        index_path = target_path / "index.html"
                        if not index_path.exists():
                            context = f"Broken link to directory (no index.html): `{href_value}` -> {target_path} (context: ...{line[max(0, match.start()-50):min(len(line), match.end()+50)]}...)"
                            errors.append(ValidationError(file_path, i, "BROKEN_LINK", context))
                # If it's a file, it exists - no error
            else:
                # File doesn't exist - check if it's within the output directory
                try:
                    target_path.relative_to(output_dir)
                except ValueError:
                    # Link points outside output directory - might be intentional, skip
                    continue

                # Check if it's a file without extension and .html version exists (only for href)
                if attr_type == 'href':
                    html_path = target_path.with_suffix('.html')
                    if html_path.exists():
                        # The .html version exists, so the link should work
                        continue

                # File doesn't exist and no .html version found
                error_type = "BROKEN_IMAGE" if attr_type == 'src' else "BROKEN_LINK"
                resource_type = "image" if attr_type == 'src' else "internal link"
                context = f"Broken {resource_type}: `{href_value}` -> {target_path} (context: ...{line[max(0, match.start()-50):min(len(line), match.end()+50)]}...)"
                errors.append(ValidationError(file_path, i, error_type, context))

    return errors


def check_bibliography_annotations(content, file_path):
    """Check that bibliography note/abstract fields are being rendered (not stripped by CSL)"""
    errors = []

    # Look for references section
    # Quarto generates: <section id="references" ...> or <div id="refs" ...>
    refs_pattern = r'<(?:section|div)[^>]*(?:id=["\'](?:references|refs)["\']|class=["\'][^"\']*references[^"\']*["\'])[^>]*>'
    refs_match = re.search(refs_pattern, content, re.IGNORECASE)

    if not refs_match:
        # No references section found - that's OK for pages without citations
        return errors

    # Find the references section content
    refs_start = refs_match.end()
    # Find closing tag (simplified - look for next major section or end)
    refs_section_pattern = r'<(?:section|div)[^>]*(?:id=["\'](?:references|refs)["\'])[^>]*>(.*?)</(?:section|div)>'
    refs_section_match = re.search(refs_section_pattern, content, re.IGNORECASE | re.DOTALL)

    if not refs_section_match:
        # Can't find complete references section
        return errors

    refs_content = refs_section_match.group(1)

    # Count citation entries (csl-entry class)
    citation_entries = re.findall(r'<div[^>]*class=["\'][^"\']*csl-entry[^"\']*["\']', refs_content)
    num_citations = len(citation_entries)

    if num_citations == 0:
        # No citations found in references section
        return errors

    # Check for rendered abstracts/notes
    # nature-annotated.csl renders abstracts in quotes or with specific formatting
    # Look for patterns indicating abstract content is present:
    # 1. Quoted text (abstracts often rendered in quotes)
    # 2. Long text blocks within citation entries
    # 3. Specific CSL annotation classes

    # Pattern for quoted abstracts (nature-annotated style)
    quoted_abstracts = re.findall(r'["\u201c][^"\u201d]{100,}["\u201d]', refs_content)

    # Pattern for annotation divs (some CSL styles use these)
    annotation_divs = re.findall(r'<div[^>]*class=["\'][^"\']*(?:csl-block|annotation|abstract|note)[^"\']*["\']', refs_content, re.IGNORECASE)

    # Check if we have any indication of rendered annotations
    has_annotations = len(quoted_abstracts) > 0 or len(annotation_divs) > 0

    # If we have many citations but no visible annotations, that's suspicious
    # (assuming the bib file has abstracts - we can't check that here)
    if num_citations >= 3 and not has_annotations:
        # This is a warning, not an error - the bib might not have abstracts
        # Only flag if the refs section is suspiciously short for the citation count
        avg_chars_per_citation = len(refs_content) / num_citations

        # A citation with abstract should be at least 500+ chars typically
        # Basic citation (author, title, journal, year) is ~200-300 chars
        if avg_chars_per_citation < 400:
            context = f"References section has {num_citations} citations but may be missing abstracts/notes (avg {int(avg_chars_per_citation)} chars/citation). Check that nature-annotated.csl is being used and .bib has abstract fields."
            errors.append(ValidationError(file_path, 0, "BIBLIOGRAPHY_MISSING_ANNOTATIONS", context))

    return errors


def normalize_description_for_comparison(text: str) -> str:
    """
    Normalize description text for comparison.

    Strips confidence intervals and normalizes whitespace so that:
    - "6.65k diseases (95% CI: 5.70k-8.24k) diseases..."
    - "6.65k diseases diseases..."
    Both normalize to the same string.

    This allows intentional CI differences between:
    - Page descriptions (Quarto-rendered with CIs)
    - Book/website descriptions (clean for SEO)
    """
    if not text:
        return ""
    # Strip confidence intervals using shared function
    normalized = strip_confidence_intervals(text)
    # Normalize whitespace
    normalized = re.sub(r'\s{2,}', ' ', normalized)
    return normalized.strip()


def check_meta_description_match(content, file_path):
    """Check that og:description and name="description" meta tags have matching values"""
    errors = []
    
    # Pattern to match meta description tags
    # Matches: <meta name="description" content="...">
    # Matches: <meta property="og:description" content="...">
    name_desc_pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
    og_desc_pattern = r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']'
    
    name_desc_match = re.search(name_desc_pattern, content, re.IGNORECASE)
    og_desc_match = re.search(og_desc_pattern, content, re.IGNORECASE)
    
    # If neither exists, that's fine (some pages might not have descriptions)
    if not name_desc_match and not og_desc_match:
        return errors
    
    # If only one exists, that's an error
    if name_desc_match and not og_desc_match:
        context = f"Has <meta name=\"description\"> but missing <meta property=\"og:description\">"
        errors.append(ValidationError(file_path, 0, "MISSING_OG_DESCRIPTION", context))
        return errors
    
    if og_desc_match and not name_desc_match:
        context = f"Has <meta property=\"og:description\"> but missing <meta name=\"description\">"
        errors.append(ValidationError(file_path, 0, "MISSING_META_DESCRIPTION", context))
        return errors
    
    # Both exist - normalize and check if they match
    name_desc_value = name_desc_match.group(1)
    og_desc_value = og_desc_match.group(1)

    # Normalize both descriptions (strip CIs, normalize whitespace)
    # This allows intentional CI differences between page and book descriptions
    name_normalized = normalize_description_for_comparison(name_desc_value)
    og_normalized = normalize_description_for_comparison(og_desc_value)

    if name_normalized != og_normalized:
        # Some non-index pages intentionally use page-specific SEO descriptions while
        # inheriting a shared Open Graph description. Treat this as acceptable.
        if Path(file_path).name != "index.html":
            return errors
        context = (
            f"Description mismatch after normalization:\n"
            f"  name=\"description\" = \"{name_desc_value[:80]}...\"\n"
            f"  og:description = \"{og_desc_value[:80]}...\"\n"
            f"  (normalized: \"{name_normalized[:60]}...\" vs \"{og_normalized[:60]}...\")"
        )
        errors.append(ValidationError(file_path, 0, "DESCRIPTION_MISMATCH", context))

    return errors


def check_quarto_config_resources(output_dir):
    """Check that resources referenced in _quarto.yml exist in output directory"""
    errors = []

    # Look for _quarto.yml in project root (parent of output dir)
    project_root = output_dir.parent.parent if "/_" in str(output_dir) or "\\_" in str(output_dir) else output_dir.parent
    quarto_config = project_root / "_quarto.yml"

    if not quarto_config.exists():
        # No _quarto.yml found, skip this check
        return errors

    try:
        with open(quarto_config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        errors.append(ValidationError(quarto_config, 0, "YAML_PARSE_ERROR", f"Failed to parse _quarto.yml: {e}"))
        return errors

    # Check PDF output file if specified
    if 'format' in config and 'pdf' in config['format']:
        pdf_config = config['format']['pdf']
        if 'output-file' in pdf_config:
            pdf_filename = pdf_config['output-file']
            pdf_path = output_dir / pdf_filename

            if not pdf_path.exists():
                context = f"PDF file referenced in config not found: {pdf_filename}"
                errors.append(ValidationError(quarto_config, 0, "MISSING_PDF", context))

    # Check navbar/sidebar PDF links
    def check_pdf_links(obj, path=""):
        """Recursively check for PDF links in config structure"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if key == 'href' and isinstance(value, str) and value.endswith('.pdf'):
                    # Found a PDF link, check if it exists
                    # Remove leading slash for local files
                    pdf_file = value.lstrip('/')
                    pdf_path = output_dir / pdf_file
                    if not pdf_path.exists():
                        context = f"PDF linked in config not found: {value} (checked: {pdf_path})"
                        errors.append(ValidationError(quarto_config, 0, "MISSING_PDF_LINK", context))
                else:
                    check_pdf_links(value, new_path)
        elif isinstance(obj, list):
            for item in obj:
                check_pdf_links(item, path)

    if 'book' in config:
        check_pdf_links(config['book'])
    if 'website' in config:
        check_pdf_links(config['website'])

    return errors


def validate_file(file_path, output_dir):
    """Run all validation checks on a single HTML file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [ValidationError(file_path, 0, "READ_ERROR", f"Failed to read file: {e}")]

    errors = []
    errors.extend(check_unrendered_inline_python(content, file_path))
    errors.extend(check_dollar_python_pattern(content, file_path))
    errors.extend(check_blacklisted_strings(content, file_path))
    errors.extend(check_qmd_file_links(content, file_path))
    errors.extend(check_broken_internal_links(content, file_path, output_dir))
    errors.extend(check_meta_description_match(content, file_path))
    errors.extend(check_bibliography_annotations(content, file_path))

    return errors


def write_job_summary(errors_by_type: dict, output_dir: Path):
    """Write a Job Summary to $GITHUB_STEP_SUMMARY for prominent display in GitHub Actions UI."""
    if not IN_GITHUB_ACTIONS or not GITHUB_STEP_SUMMARY:
        return

    total_errors = sum(len(errors) for errors in errors_by_type.values())

    try:
        with open(GITHUB_STEP_SUMMARY, "a", encoding="utf-8") as f:
            f.write("\n## :x: Post-Render Validation Failed\n\n")
            f.write(f"**{total_errors} validation error(s) found**\n\n")

            # Error summary table
            f.write("| Error Type | Count | Description |\n")
            f.write("|------------|-------|-------------|\n")

            error_descriptions = {
                "QMD_FILE_LINK": "Links to .qmd files in rendered HTML (should be .html)",
                "BROKEN_LINK": "Internal links to non-existent files",
                "BROKEN_IMAGE": "Image references to non-existent files",
                "UNRENDERED_PYTHON": "Inline Python expressions that didn't evaluate",
                "UNRENDERED_PYTHON_INLINE": "Raw {python} patterns in output",
                "PYTHON_ERROR": "Python exceptions in rendered output",
                "ECHO_FALSE_LEAK": "Cell options leaked into output",
                "FRONTMATTER_LEAK": "YAML frontmatter leaked into output",
                "FINDFONT_WARNING": "Matplotlib font warnings in output",
                "LATEX_IN_CODE_BLOCK": "LaTeX math rendered as code instead of math",
                "POSIXPATH_IN_OUTPUT": "Python path objects not converted to strings",
                "MISSING_PDF": "Expected PDF file not found",
                "MISSING_PDF_LINK": "PDF linked in config not found",
                "DESCRIPTION_MISMATCH": "Meta description tags have different values",
                "BIBLIOGRAPHY_MISSING_ANNOTATIONS": "References may be missing abstracts",
            }

            for error_type, errors in sorted(errors_by_type.items()):
                desc = error_descriptions.get(error_type, "Validation error")
                f.write(f"| `{error_type}` | {len(errors)} | {desc} |\n")

            # Detailed errors (first 10 per type)
            f.write("\n### Error Details\n\n")
            for error_type, errors in sorted(errors_by_type.items()):
                f.write(f"\n<details>\n<summary><b>{error_type}</b> ({len(errors)} errors)</summary>\n\n")
                for error in errors[:10]:
                    source_file = error.get_source_file(output_dir)
                    # Escape backticks in context for markdown
                    context = error.context.replace('`', '\\`')[:200]
                    f.write(f"- **{source_file}:{error.line_num}** - {context}\n")
                if len(errors) > 10:
                    f.write(f"\n*...and {len(errors) - 10} more*\n")
                f.write("\n</details>\n")

            f.write("\n---\n")
            f.write("*Run `python scripts/post-render-validation.py` locally to see full details*\n")
    except Exception as e:
        print(f"[WARNING] Failed to write job summary: {e}", file=sys.stderr)


def write_json_output(errors: list, output_path: str) -> None:
    """Write validation errors to JSON file for GitHub Actions automation."""
    json_errors = []

    for error in errors:
        json_errors.append({
            "source": "post-render",
            "paper": "",  # Post-render validates all files, not specific papers
            "severity": "WARNING",  # All post-render errors are warnings
            "type": error.error_type,
            "page": None,
            "line": error.line_num,
            "message": error.error_type,
            "context": error.context,
            "file_path": error.file_path,
            "suggested_fix": "",
            "evidence_snippet": error.context,
            "locator_hint": f"Line {error.line_num}"
        })

    output = {
        "timestamp": datetime.now().isoformat(),
        "totalErrors": len(errors),
        "errors": json_errors
    }

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n[JSON OUTPUT] Written to: {output_path}")
    except Exception as e:
        print(f"[WARNING] Failed to write JSON output: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Validate Quarto render output for common issues")
    parser.add_argument("--output-dir", default="_manual/warondisease", help="Directory containing rendered HTML files")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Treat warnings as errors")
    parser.add_argument(
        "--output-json", help="Write errors to JSON file (for issue automation)"
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    if not output_dir.exists():
        print(f"[ERROR] Output directory not found: {output_dir}")
        return 1

    print(f"[VALIDATION] Validating rendered HTML in {output_dir}...")

    html_files = find_html_files(output_dir)
    print(f"   Found {len(html_files)} HTML files to check")

    all_errors = []
    errors_by_type = defaultdict(list)

    for file_path in html_files:
        errors = validate_file(file_path, output_dir)
        if errors:
            all_errors.extend(errors)
            for error in errors:
                errors_by_type[error.error_type].append(error)

    # Check Quarto config resources (PDFs, etc.)
    print("   Checking Quarto config resources...")
    config_errors = check_quarto_config_resources(output_dir)
    if config_errors:
        all_errors.extend(config_errors)
        for error in config_errors:
            errors_by_type[error.error_type].append(error)

    # Print results
    if not all_errors:
        print("[OK] All validation checks passed!")
        # Write success to job summary
        if IN_GITHUB_ACTIONS and GITHUB_STEP_SUMMARY:
            try:
                with open(GITHUB_STEP_SUMMARY, "a", encoding="utf-8") as f:
                    f.write("\n## :white_check_mark: Post-Render Validation Passed\n\n")
                    f.write(f"Validated {len(html_files)} HTML files with no errors.\n")
            except Exception:
                pass
        return 0

    print(f"\n[ERROR] Found {len(all_errors)} validation error(s):\n")

    # Emit GitHub Actions annotations (before printing, so they appear at top)
    if IN_GITHUB_ACTIONS:
        for error in all_errors:
            error.emit_annotation(output_dir)

    # Group errors by type for better readability
    for error_type, errors in sorted(errors_by_type.items()):
        print(f"  {error_type}: {len(errors)} error(s)")
        for error in errors:  # Show all errors
            print(f"    {error}")
        print()

    # Write Job Summary for GitHub Actions UI
    write_job_summary(errors_by_type, output_dir)

    # Provide suggestions
    print("[SUGGESTIONS]")
    if "UNRENDERED_PYTHON" in errors_by_type:
        print("   - Unrendered inline Python: This happens when Quarto uses cached")
        print("     computations. Clear freeze directories: rm -rf _freeze .quarto/_freeze")
        print("   - Or render with: quarto render --execute-daemon restart")
        print("   - Check that variables are defined before use")
    if "UNRENDERED_PYTHON_INLINE" in errors_by_type:
        print("   - Unrendered `{python}` pattern: Inline Python expressions didn't evaluate")
        print("     Clear freeze directories: rm -rf _freeze .quarto/_freeze")
        print("   - Or render with: quarto render --execute-daemon restart")
        print("   - Ensure Python code blocks execute before inline expressions")
        print("   - Check that variables referenced in `{python}` are defined")
    if "ECHO_FALSE_LEAK" in errors_by_type:
        print("   - 'echo: false' in output: Use cell option format: #| echo: false")
        print("     (with #| prefix, not as YAML)")
    if "PYTHON_ERROR" in errors_by_type:
        print("   - Python errors: Check Python code cells for exceptions")
    if "FRONTMATTER_LEAK" in errors_by_type:
        print("   - Frontmatter leakage: YAML frontmatter from included files is appearing in output")
        print("     This usually means {{< include >}} is not properly stripping frontmatter")
        print("     Check that included files have properly formatted YAML (--- at start and end)")
        print("     Or remove frontmatter from files that are only meant to be included")
    if "FINDFONT_WARNING" in errors_by_type:
        print("   - Matplotlib findfont warnings: Ensure the required fonts are installed")
        print("     or configure Matplotlib to use bundled fonts to avoid runtime warnings")
    if "QMD_FILE_LINK" in errors_by_type:
        print("   - Links to .qmd files: rendered HTML should only contain .html links")
        print("     Update the SOURCE .qmd file to link to another .qmd (Quarto converts)")
        print("     Ensure the target .qmd exists and is listed in the book config")
    if "BROKEN_LINK" in errors_by_type:
        print("   - Broken internal links: Some links point to files that don't exist")
        print("     Check that all referenced files were rendered")
        print("     Verify that relative paths are correct")
        print("     Ensure that directory links have an index.html file")
    if "BROKEN_IMAGE" in errors_by_type:
        print("   - Broken images: Some img src paths point to files that don't exist")
        print("     Check that image files were generated/copied during render")
        print("     Verify that relative image paths are correct")
        print("     For Quarto-generated figures, ensure _files/ directories are included in output")
    if "POSIXPATH_IN_OUTPUT" in errors_by_type:
        print("   - PosixPath in output: A pathlib.PosixPath object was not converted to string")
    if "MISSING_PDF" in errors_by_type:
        print("   - Missing PDF: PDF file specified in _quarto.yml output-file not found in output directory")
        print("     Check that PDF format is being rendered (format: pdf: section in config)")
        print("     Verify the PDF was successfully generated during render")
    if "MISSING_PDF_LINK" in errors_by_type:
        print("   - Missing PDF link: PDF file linked in navbar/sidebar not found in output directory")
        print("     Ensure the PDF file exists or is generated during render")
        print("     Check that the href path in config matches the actual file location")
    if "DESCRIPTION_MISMATCH" in errors_by_type:
        print("   - Description mismatch: <meta name=\"description\"> and <meta property=\"og:description\">")
        print("     have different values even after normalizing (stripping CIs, whitespace).")
        print("     This indicates the descriptions have fundamentally different content.")
        print("     Note: Confidence interval differences are allowed and normalized during comparison.")
    if "MISSING_OG_DESCRIPTION" in errors_by_type:
        print("   - Missing og:description: Page has <meta name=\"description\"> but no <meta property=\"og:description\">")
        print("     Ensure open-graph: true is set in metadata section of _quarto.yml")
    if "MISSING_META_DESCRIPTION" in errors_by_type:
        print("   - Missing meta description: Page has <meta property=\"og:description\"> but no <meta name=\"description\">")
        print("     This is unusual - both should be present. Check Quarto configuration.")
    if "BIBLIOGRAPHY_MISSING_ANNOTATIONS" in errors_by_type:
        print("   - Bibliography missing annotations: References section appears to lack abstract/note content")
        print("     Ensure nature-annotated.csl (or similar annotated CSL) is specified in _quarto*.yml")
        print("     Verify .bib files have 'abstract' and 'note' fields populated")
        print("     Check that bibliography: and csl: are correctly configured")

    # Write JSON output if requested
    if args.output_json and all_errors:
        write_json_output(all_errors, args.output_json)

    return 1


if __name__ == "__main__":
    sys.exit(main())
