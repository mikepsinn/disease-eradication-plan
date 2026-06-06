#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-render validation script
Validates .qmd and .md files before Quarto rendering to catch errors early:
- LaTeX syntax errors (escaped dollar signs, malformed equations, etc.)
- Missing image files
- Invalid image paths
- Broken cross-reference links to .qmd files
- Broken markdown file links in .md files
- Broken anchor IDs in links (validates that #anchor-id exists in target file)
- Broken include directives ({{< include path.qmd >}})
- Missing Python imports in code blocks
- GIF files not wrapped in HTML-only or epub/pdf-exclusion blocks (prevents PDF/epub build failures)
- Unknown Quarto variables ({{< var name >}}) not defined in _variables.yml
- Missing citations ([@citation-id]) not found in references.bib
- _quarto.yml configuration (validates all chapter paths exist)
- Figure files with YAML frontmatter (knowledge/figures/*.qmd should not have frontmatter)
- Unclosed code blocks (missing closing ```) which cause code to leak into output
- Duplicate _latex variables (same equation appearing multiple times indicates redundancy)
- Figure caption LaTeX safety (prevents 'File ended while scanning use of \\@writefile' errors)
  - Double-backslash before % # & $ in captions (breaks LaTeX aux files)
  - Unbalanced braces in captions
  - Excessively long captions (>500 chars)

Runs automatically via _quarto.yml pre-render hook
"""

import argparse
import json
import logging
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

# Set UTF-8 encoding for stdout and stderr on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]

# Import shared validation library for common functions
try:
    from lib.validation_core import EM_DASH_MESSAGE
except ImportError:
    EM_DASH_MESSAGE = 'Em-dash found. Replace with parenthesis, comma and space (", "), period, or semicolon as appropriate. Prefer periods and shortened sentences where appropriate.'

# Import centralized file utilities
from lib.quarto_file_utils import find_files_by_extension
from lib.quarto_config_utils import get_all_book_qmd_files

# Use C-accelerated YAML loader when available (21x faster on _variables.yml)
try:
    import yaml
    _yaml_loader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
except ImportError:
    yaml = None  # type: ignore[assignment]
    _yaml_loader = None


def _yaml_safe_load(stream):
    """yaml.safe_load using C loader when available."""
    if yaml is None or _yaml_loader is None:
        raise RuntimeError("YAML support not available")
    return yaml.load(stream, Loader=_yaml_loader)

logger = logging.getLogger("dih.validate")

# Filler phrases that should be removed - just state the point directly
FILLER_PHRASES = [
    (re.compile(r'\*\*[Kk]ey [Ii]nsight:?\*\*:?', re.IGNORECASE), 'Filler phrase "Key insight" found. Either (1) delete it and state the point directly, or (2) replace with a specific claim like "The ratio exceeds 300:1" or "This reduces costs by 82x".'),
    (re.compile(r'\*\*[Tt]he key [Ii]nsight:?\*\*:?', re.IGNORECASE), 'Filler phrase "The key insight" found. Either (1) delete it and state the point directly, or (2) replace with a specific claim like "The ratio exceeds 300:1" or "This reduces costs by 82x".'),
]

# Pre-compiled regex patterns used across multiple check functions (avoids re._compile overhead)
_RE_HTML_COMMENT_START = re.compile(r"^\s*<!--")
_RE_PYTHON_BLOCK_START = re.compile(r"^```\{python\}")
_RE_DISPLAY_MATH = re.compile(r"\$\$")
_RE_LATEX_TEXT_BLOCK = re.compile(r"\\text\{[^}]*\}")
_RE_ESCAPED_DOLLAR = re.compile(r"\\\$")
_RE_MATH_BULLET = re.compile(r"^\s+\*\s+")
_RE_QUARTO_VAR = re.compile(r"\{\{<\s*var\s+[^>]+\s*>\}\}")
_RE_QUARTO_SHORTCODE = re.compile(r"\{\{<[^>]+>\}\}")
_RE_MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_RE_HTML_IMAGE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
_RE_EM_DASH = re.compile(r"\u2014")
_RE_INLINE_CODE_EM_DASH = re.compile(r"`[^`]*\u2014[^`]*`")
_RE_URL_EM_DASH = re.compile(r"https?://[^\s]*\u2014[^\s]*")
_RE_CROSS_REF_LINK = re.compile(r"\[([^\]]+)\]\(([^)#]+\.qmd[^)]*)\)")
_RE_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_RE_INCLUDE_DIRECTIVE = re.compile(r"\{\{<\s*include\s+([^\s>]+)\s*>\}\}")
_RE_LINK_WITH_VAR = re.compile(r"\[([^\]]*\{\{<\s*var\s+[^>]+\s*>\}\}[^\]]*)\]\([^)]+\)")
_RE_LATEX_VAR = re.compile(r"\{\{<\s*var\s+([a-z_]+_latex)\s*>\}\}")
_RE_VAR_REFERENCE = re.compile(r"\{\{<\s*var\s+([^\s>]+)\s*>\}\}")
_RE_BRACKETED_CITATION = re.compile(r'\[@([^\]]+)\]')
_RE_BARE_CITATION = re.compile(r'(?<![a-zA-Z0-9_.])@([a-zA-Z][a-zA-Z0-9_:-]*)')
_RE_CAPTION = re.compile(r'!\[([^\]]*)\]\([^)]+\)')
_RE_HTML_IMG_ALT = re.compile(r'<img[^>]+alt=["\']([^"\']*)["\']', re.IGNORECASE)
_RE_HARDCODED_PATH = re.compile(r"output_dir\s*=.*['\"]brain['\"].*['\"]figures['\"]")
_RE_MANUAL_PATH = re.compile(r"output_path\s*=\s*output_dir\s*/")
_RE_IDENTIFIER = re.compile(r"\b([A-Z][A-Z0-9_]{2,})\b")


class ValidationError:
    def __init__(self, file: str, line: int, message: str, context: str, column: Optional[int] = None):
        self.file = file
        self.line = line
        self.column = column
        self.message = message
        self.context = context


errors: List[ValidationError] = []

# Common LaTeX error patterns to check for
latex_patterns = [
    {
        "pattern": re.compile(r"\$\$\$"),
        "message": "Triple dollar sign ($$$) - should be $$ for display math or single $ for inline",
    },
    {
        "pattern": re.compile(r"\\\$\$"),
        "message": "Escaped double dollar sign (\\$$) - likely intended as single $ inside math mode",
    },
    {
        "pattern": re.compile(r"\$\$[^\n]*\\underbrace\{[^}]*\}[^\n]*\$\$"),
        "message": "Check \\underbrace syntax - ensure all braces are properly closed",
        "validator": lambda match: check_brace_balance(match),
    },
    {
        "pattern": re.compile(r"\$\$[^\n]*\\\\\]"),
        "message": "Malformed equation end (\\]) - should be ] without extra backslash",
    },
    {
        "pattern": re.compile(r"\\\}\\_\\\{"),
        "message": "Malformed subscript (}_{) - should be }_{",
    },
]


def check_brace_balance(match: str) -> bool:
    """Check if braces are balanced in a match"""
    brace_count = 0
    for char in match:
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
        if brace_count < 0:
            return False
    return brace_count == 0


def resolve_link_path(link_path: str, file_dir: str) -> str:
    """
    Resolve a link path to an absolute filesystem path.
    
    Handles:
    - Relative paths (resolved relative to file_dir)
    - Absolute paths starting with / (resolved from project root)
    
    Args:
        link_path: The path from the markdown link (may start with / for absolute)
        file_dir: The directory containing the file with the link
        
    Returns:
        Normalized absolute path to the target file
    """
    if link_path.startswith("/"):
        # Absolute path from project root - resolve from current working directory
        # Remove the leading slash and resolve from project root
        return os.path.normpath(link_path[1:])
    else:
        # Relative path - resolve from the file's directory
        return os.path.normpath(os.path.join(file_dir, link_path))


def check_math_delimiters(content: str, filename: str, lines: List[str]):
    """Check for unmatched dollar signs in math mode"""
    # Early return if no display math in file
    if "$$" not in content:
        return

    in_math_block = False
    in_code_block = False

    for line_index, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Track display math mode ($$)
        display_math_matches = _RE_DISPLAY_MATH.findall(line)
        for _ in display_math_matches:
            in_math_block = not in_math_block

        # Check for single $ in display math mode (potential error)
        # BUT ignore \$ (escaped dollar signs, which are valid in \text{} blocks)
        if in_math_block and "$" in line and "$$" not in line:
            # Remove all \$ (escaped dollar signs) and \text{...} blocks
            cleaned_line = _RE_LATEX_TEXT_BLOCK.sub("", line)  # Remove \text{...} blocks
            cleaned_line = _RE_ESCAPED_DOLLAR.sub("", cleaned_line)  # Remove escaped dollar signs

            # Now check if there are any remaining unescaped $ signs
            if "$" in cleaned_line:
                context = line.strip()[:80]
                errors.append(
                    ValidationError(
                        file=filename,
                        line=line_index + 1,
                        message="Unescaped $ inside display math mode ($$...$$)",
                        context=context,
                    )
                )

        # Check for * at the start of a line inside math block (markdown bullet interfering)
        if in_math_block and _RE_MATH_BULLET.match(line):
            context = line.strip()[:80]
            errors.append(
                ValidationError(
                    file=filename,
                    line=line_index + 1,
                    message="Markdown bullet (*) inside math block - use + for addition or \\cdot for multiplication",
                    context=context,
                )
            )

        # Check for blank lines inside math block (causes LaTeX errors)
        if in_math_block and line.strip() == "" and "$$" not in line:
            errors.append(
                ValidationError(
                    file=filename,
                    line=line_index + 1,
                    message="Blank line inside math block ($$...$$) - remove blank line or close math block first",
                    context="(blank line)",
                )
            )

        # Check for Quarto variables/shortcodes inside math blocks (they don't work there)
        if in_math_block:
            # Check for Quarto variable syntax: {{< var name >}}
            if _RE_QUARTO_VAR.search(line):
                context = line.strip()[:80]
                errors.append(
                    ValidationError(
                        file=filename,
                        line=line_index + 1,
                        message="Quarto variable ({{< var ... >}}) inside math block - variables do not work inside LaTeX. Use Python code block to print LaTeX string instead.",
                        context=context,
                    )
                )

            # Check for other Quarto shortcodes: {{< include ... >}}, {{< ... >}}
            if _RE_QUARTO_SHORTCODE.search(line):
                # But allow if it's just a variable we already caught
                if not _RE_QUARTO_VAR.search(line):
                    context = line.strip()[:80]
                    errors.append(
                        ValidationError(
                            file=filename,
                            line=line_index + 1,
                            message="Quarto shortcode ({{< ... >}}) inside math block - shortcodes do not work inside LaTeX. Process values before math block or use Python code block.",
                            context=context,
                        )
                    )


def check_image_paths(content: str, filepath: str, lines: List[str]):
    """Check for missing image files"""
    file_dir = os.path.dirname(filepath)

    for line_index, line in enumerate(lines):
        # Check markdown image syntax
        markdown_matches = _RE_MARKDOWN_IMAGE.finditer(line)
        for match in markdown_matches:
            image_path = match.group(2)
            _check_single_image_path(image_path, filepath, file_dir, line_index + 1, line)

        # Check HTML img tags
        html_matches = _RE_HTML_IMAGE.finditer(line)
        for match in html_matches:
            image_path = match.group(1)
            _check_single_image_path(image_path, filepath, file_dir, line_index + 1, line)


def _check_single_image_path(image_path: str, filepath: str, file_dir: str, line_number: int, line: str):
    """Helper function to check a single image path"""
    # Skip URLs (http://, https://, etc.)
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return

    # Resolve the image path (handles both relative and absolute /paths)
    resolved_path = resolve_link_path(image_path, file_dir)

    # Check if the path would exceed Windows MAX_PATH in the build temp directory
    if sys.platform == 'win32':
        WINDOWS_PATH_LIMIT = 250
        BUILD_TEMP_OVERHEAD = 45  # _build_temp/{longest-config-name}/
        estimated_len = len(resolved_path) + BUILD_TEMP_OVERHEAD
        if estimated_len > WINDOWS_PATH_LIMIT:
            errors.append(
                ValidationError(
                    file=filepath,
                    line=line_number,
                    message=f"Image path too long for PDF builds ({estimated_len} chars, limit {WINDOWS_PATH_LIMIT}): {os.path.basename(image_path)}",
                    context=line.strip()[:80],
                )
            )

    if not os.path.exists(resolved_path):
        errors.append(
            ValidationError(
                file=filepath,
                line=line_number,
                message=f"Image file not found: {image_path}",
                context=line.strip()[:80],
            )
        )


def check_em_dashes(content: str, filepath: str, lines: List[str]):
    """
    Check for em-dashes (\u2014) which should be replaced with comma and space or other punctuation.
    Detects ALL em-dashes except those in safe contexts (code blocks, inline code, URLs).
    """
    # Early return if no em-dashes in file
    if "\u2014" not in content:
        return

    in_code_block = False

    for line_index, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Skip if em-dash is inside inline code
        if _RE_INLINE_CODE_EM_DASH.search(line):
            continue

        # Skip if em-dash is inside a URL
        if _RE_URL_EM_DASH.search(line):
            continue

        # Find all em-dashes
        matches = list(_RE_EM_DASH.finditer(line))
        if matches:
            for match in matches:
                # Find the column position of the em-dash
                column = match.start() + 1
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        column=column,
                        message=EM_DASH_MESSAGE,
                        context=line.strip()[:80],
                    )
                )


def check_filler_phrases(content: str, filepath: str, lines: List[str]):
    """
    Check for filler phrases like "Key insight:" that should be removed.
    These phrases add no value - just state the point directly.
    """
    in_code_block = False

    for line_index, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Skip HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()) or ("<!--" in line and "-->" in line):
            continue

        # Check each filler phrase pattern (patterns are pre-compiled in FILLER_PHRASES)
        for pattern, message in FILLER_PHRASES:
            matches = list(pattern.finditer(line))
            if matches:
                for match in matches:
                    column = match.start() + 1
                    errors.append(
                        ValidationError(
                            file=filepath,
                            line=line_index + 1,
                            column=column,
                            message=message,
                            context=line.strip()[:80],
                        )
                    )


def check_cross_reference_links(content: str, filepath: str, lines: List[str]):
    """
    Check for broken cross-reference links to other .qmd files
    Matches patterns like: [text](path/to/file.qmd)
    """
    file_dir = os.path.dirname(filepath)

    for line_index, line in enumerate(lines):
        # Skip lines that are HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()):
            continue

        matches = _RE_CROSS_REF_LINK.finditer(line)
        for match in matches:
            # Skip if this match is inside an HTML comment
            # Check if there's a <!-- before the match and --> after it on the same line
            before_match = line[: match.start()]
            after_match = line[match.end() :]
            if "<!--" in before_match and "-->" in after_match:
                continue  # Link is inside HTML comment, skip it

            link_path = match.group(2).split("#")[0]  # Remove anchor if present

            # Skip URLs
            if link_path.startswith("http://") or link_path.startswith("https://"):
                continue

            # Resolve the link path (handles both relative and absolute /paths)
            resolved_path = resolve_link_path(link_path, file_dir)

            if not os.path.exists(resolved_path):
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message=f"Broken cross-reference link: {link_path} (target file not found)",
                        context=line.strip()[:80],
                    )
                )


def load_parameter_names() -> Set[str]:
    """
    Load all parameter names from dih_models/parameters.py.
    Returns a set of uppercase parameter names (e.g., 'GLOBAL_MILITARY_SPENDING_ANNUAL_2024').
    """
    parameters_file = "dih_models/parameters.py"
    parameter_names: Set[str] = set()

    if not os.path.exists(parameters_file):
        logger.debug(f"Warning: {parameters_file} not found, skipping parameter import validation")
        return parameter_names

    try:
        with open(parameters_file, encoding="utf-8") as f:
            content = f.read()

        # Pattern: PARAMETER_NAME = Parameter(
        # Match uppercase names followed by = Parameter(
        param_pattern = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=\s*Parameter\(", re.MULTILINE)
        matches = param_pattern.finditer(content)

        for match in matches:
            parameter_names.add(match.group(1))

        return parameter_names
    except Exception as e:
        logger.debug(f"Warning: Failed to parse {parameters_file}: {str(e)}")
        return parameter_names


def check_parameter_imports(content: str, filepath: str, defined_parameters: Set[str], lines: List[str]):
    """
    Check if parameters from dih_models.parameters are used but not imported.
    This catches errors like using GLOBAL_CLINICAL_TRIAL_MARKET_ANNUAL without importing it.
    """
    if not defined_parameters:
        return

    # Early return if no Python blocks
    if "```{python}" not in content:
        return

    # Check if file includes setup-parameters.qmd (which contains the import).
    # Quarto resolves includes before execution, so parameters are available.
    if "include" in content and "setup-parameters" in content:
        return

    # Skip figure files (knowledge/figures/) - they are always {{< include >}}'d
    # from parent files that already have parameter imports in an earlier block.
    if "knowledge/figures/" in filepath.replace("\\", "/"):
        return

    in_python_block = False
    current_block = []
    block_start_line = 0
    # Track whether ANY previous block imported parameters.
    # Quarto Python blocks share the same kernel session, so an import in
    # block 1 makes parameters available in all subsequent blocks.
    file_has_param_import = False

    for i, line in enumerate(lines):
        if _RE_PYTHON_BLOCK_START.match(line):
            in_python_block = True
            block_start_line = i + 1
            current_block = []
        elif in_python_block and line.strip() == "```":
            # End of Python block - check for parameter usage
            block_content = "\n".join(current_block)

            # Check if this block imports from dih_models.parameters
            if "dih_models.parameters" in block_content and "import" in block_content:
                file_has_param_import = True
                in_python_block = False
                continue

            # Skip check if a previous block already imported parameters
            if file_has_param_import:
                in_python_block = False
                continue

            # Extract all uppercase identifiers and check against parameter set
            found_identifiers = set(_RE_IDENTIFIER.findall(block_content))
            used_params = found_identifiers & defined_parameters

            # Report error for first used parameter
            if used_params:
                first_param = next(iter(used_params))
                for line_num, block_line in enumerate(current_block, block_start_line):
                    if first_param in block_line:
                        errors.append(
                            ValidationError(
                                file=filepath,
                                line=line_num,
                                message=f"Parameter '{first_param}' used but not imported from dih_models.parameters",
                                context=block_line.strip()[:80],
                            )
                        )
                        break

            in_python_block = False
        elif in_python_block:
            current_block.append(line)


def check_python_imports(content: str, filepath: str, lines: List[str]):
    """
    Check for missing imports in Python code blocks.
    Detects cases where a module is used but not imported in that specific block.
    """
    # Early return if no Python blocks
    if "```{python}" not in content:
        return

    # Common module patterns to check
    # Format: (usage_pattern, import_patterns, module_name)
    # NOTE: We only check for imports that MUST be in each block that uses them.
    # Standard library imports (pd, np, plt) are available from first block in Quarto.
    # get_figure_output_path and get_project_root are checked by check_figure_file_imports() (whole-file check).
    MODULE_CHECKS = [
        (
            r"\bnpf\.",
            [r"import\s+numpy_financial\s+as\s+npf", r"from\s+numpy_financial\s+import"],
            "numpy_financial (npf)",
        ),
    ]

    in_python_block = False
    current_block = []
    block_start_line = 0

    for i, line in enumerate(lines):
        if _RE_PYTHON_BLOCK_START.match(line):
            in_python_block = True
            block_start_line = i + 1
            current_block = []
        elif in_python_block and line.strip() == "```":
            # End of Python block - check imports
            block_content = "\n".join(current_block)

            for usage_pattern, import_patterns, module_name in MODULE_CHECKS:
                # Check if module is used
                if re.search(usage_pattern, block_content):
                    # Check if module is imported in this block (use re.DOTALL to match multi-line imports)
                    has_import = any(re.search(pattern, block_content, re.DOTALL) for pattern in import_patterns)

                    if not has_import:
                        # Find first usage line in the block
                        for line_num, block_line in enumerate(current_block, block_start_line):
                            if re.search(usage_pattern, block_line):
                                errors.append(
                                    ValidationError(
                                        file=filepath,
                                        line=line_num,
                                        message=f"Missing import in Python block: {module_name}",
                                        context=block_line.strip()[:80],
                                    )
                                )
                                break  # Only report once per module per block

            in_python_block = False
        elif in_python_block:
            current_block.append(line)


def check_graphviz_variables(content: str, filepath: str, lines: List[str]):
    """
    Check for Quarto variables ({{< var ... >}}) inside Python code blocks that generate Graphviz diagrams.
    Quarto variables don't work inside Python code blocks - use Python variables instead.
    """
    # Early return if no Graphviz or no Quarto variables in file
    if "graphviz" not in content.lower() and "Digraph" not in content and "Graph(" not in content:
        return
    if "{{<" not in content:
        return

    in_python_block = False
    current_block = []
    block_start_line = 0

    # Pattern to detect Graphviz-related code
    graphviz_patterns = [
        r"graphviz",
        r"dot\.node",
        r"dot\.edge",
        r"dot\.attr",
        r"Digraph",
        r"Graph",
    ]

    for i, line in enumerate(lines):
        if _RE_PYTHON_BLOCK_START.match(line):
            in_python_block = True
            block_start_line = i + 1
            current_block = []
        elif in_python_block and line.strip() == "```":
            # End of Python block - check if it contains Graphviz code
            block_content = "\n".join(current_block)

            # Check if this block contains Graphviz-related code
            is_graphviz_block = any(re.search(pattern, block_content) for pattern in graphviz_patterns)

            if is_graphviz_block:
                # Check for Quarto variables in this block
                for line_num, block_line in enumerate(current_block, block_start_line):
                    if _RE_QUARTO_VAR.search(block_line):
                        context = block_line.strip()[:80]
                        errors.append(
                            ValidationError(
                                file=filepath,
                                line=line_num,
                                message="Quarto variable ({{< var ... >}}) inside Graphviz Python code block - variables do not work in Python. Use Python variables from dih_models.parameters instead.",
                                context=context,
                            )
                        )

            in_python_block = False
        elif in_python_block:
            current_block.append(line)


def check_figure_file_imports(content: str, filepath: str):
    """
    For ALL files, check that get_figure_output_path and get_project_root are imported
    if they are used ANYWHERE in the file (not per-block, since Quarto shares imports across blocks).

    This is a simpler check than check_python_imports() and avoids false positives
    from imports in one block being used in another block.
    """

    # Check if get_figure_output_path is used anywhere
    uses_get_figure_output_path = "get_figure_output_path(" in content
    # Check if it's imported anywhere (in any block)
    # Support both old _chart_style and new dih_models.plotting.chart_style imports
    imports_get_figure_output_path = bool(
        re.search(
            r"from\s+(?:figures\.)?(?:_chart_style|dih_models\.plotting\.chart_style)\s+import.*get_figure_output_path",
            content,
            re.DOTALL,
        )
    )

    if uses_get_figure_output_path and not imports_get_figure_output_path:
        errors.append(
            ValidationError(
                file=filepath,
                line=1,
                message="Figure file uses get_figure_output_path() but does not import it from _chart_style",
                context="(Check all Python blocks for missing import)",
            )
        )

    # Check if get_project_root is used anywhere
    uses_get_project_root = "get_project_root(" in content
    # Check if it's imported anywhere
    # Support both old _chart_style and new dih_models.plotting.chart_style imports
    imports_get_project_root = bool(
        re.search(
            r"from\s+(?:figures\.)?(?:_chart_style|dih_models\.plotting\.chart_style)\s+import.*get_project_root",
            content,
            re.DOTALL,
        )
    )

    if uses_get_project_root and not imports_get_project_root:
        errors.append(
            ValidationError(
                file=filepath,
                line=1,
                message="Figure file uses get_project_root() but does not import it from _chart_style",
                context="(Check all Python blocks for missing import)",
            )
        )


def check_hardcoded_figure_paths(content: str, filepath: str, lines: List[str]):
    """
    Check for hardcoded figure output paths instead of using get_figure_output_path().
    Figure files should use get_figure_output_path() for consistent output location.
    """
    for line_index, line in enumerate(lines):
        if _RE_HARDCODED_PATH.search(line):
            errors.append(
                ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message="Hardcoded figure path - use get_figure_output_path('filename.png') instead",
                    context=line.strip()[:80],
                )
            )
        elif _RE_MANUAL_PATH.search(line):
            errors.append(
                ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message="Manual path construction - use get_figure_output_path('filename.png') instead",
                    context=line.strip()[:80],
                )
            )


def check_figure_caption_latex_safety(content: str, filepath: str, lines: List[str]):
    """
    Check figure captions for content that will break LaTeX aux file generation.
    These issues cause 'File ended while scanning use of \\@writefile' errors.

    Root causes include:
    - Double-backslash before special chars (\\%) becomes \\textbackslash % where % starts a comment
    - Unbalanced braces in captions
    - Very long captions that may cause buffer issues
    """

    # Problematic patterns in captions
    # Double-backslash before special chars - becomes \textbackslash + special char
    # which can break LaTeX in various ways (% starts comment, # is param char, etc.)
    # Note: To match TWO literal backslashes in regex, we need FOUR backslash chars in the pattern
    # Using non-raw strings: 8 backslashes in source = 4 backslash chars = matches 2 literal backslashes
    caption_issues = [
        ("\\\\\\\\%", 'Double-backslash percent (\\\\%) in caption - becomes \\textbackslash % which starts a LaTeX comment and truncates the rest. Use % without backslashes in captions.'),
        ("\\\\\\\\#", 'Double-backslash hash (\\\\#) in caption - may cause LaTeX issues. Use # without backslashes in captions.'),
        ("\\\\\\\\&", 'Double-backslash ampersand (\\\\&) in caption - may cause LaTeX issues. Use & without backslashes in captions.'),
        ("\\\\\\\\\\$", 'Double-backslash dollar (\\\\$) in caption - may cause LaTeX issues. Use $ without backslashes in captions.'),
    ]

    def check_caption(caption: str, line_index: int, line: str):
        """Check a single caption for issues"""
        # Check for problematic patterns
        for pattern, message in caption_issues:
            if re.search(pattern, caption):
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message=message,
                        context=line.strip()[:80],
                    )
                )

        # Check for unbalanced braces in caption
        brace_count = 0
        for char in caption:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            if brace_count < 0:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message="Unbalanced braces in figure caption - extra closing brace '}' found",
                        context=line.strip()[:80],
                    )
                )
                break
        if brace_count > 0:
            errors.append(
                ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message="Unbalanced braces in figure caption - missing closing brace '}'",
                    context=line.strip()[:80],
                )
            )

        # Check caption length (warn if very long - may cause buffer issues)
        if len(caption) > 500:
            errors.append(
                ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message=f"Figure caption is very long ({len(caption)} chars) - may cause LaTeX buffer issues. Consider shortening.",
                    context=caption[:60] + "...",
                )
            )

    for line_index, line in enumerate(lines):
        # Check markdown image captions
        matches = _RE_CAPTION.finditer(line)
        for match in matches:
            caption = match.group(1)
            check_caption(caption, line_index, line)

        # Check HTML img alt text
        html_matches = _RE_HTML_IMG_ALT.finditer(line)
        for match in html_matches:
            alt_text = match.group(1)
            check_caption(alt_text, line_index, line)


_markdown_gif_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]*\.gif[^)]*)\)", re.IGNORECASE)
_html_gif_pattern = re.compile(r'<img[^>]+src=["\']([^"\']*\.gif[^"\']*)["\']', re.IGNORECASE)


def check_gif_references(content: str, filepath: str, lines: List[str]):
    """
    Check for GIF files that aren't wrapped in format-exclusion blocks.
    GIFs must not appear in PDF/epub output. Accept either:
    (1) HTML-only: ::: {.content-visible when-format="html"} ... :::
    (2) Epub+PDF exclusion: ::: {.content-hidden when-format="epub"}
        ::: {.content-hidden when-format="pdf"}
        <img src="...gif" />
        :::
        :::
    """
    # Early return if no GIF references in file
    if ".gif" not in content.lower():
        return
    in_html_only_block = False
    html_block_depth = 0
    # Stack of opened content-hidden blocks: 'epub' and 'pdf' in open order
    epub_pdf_stack: List[str] = []

    for line_index, line in enumerate(lines):
        stripped = line.strip()

        # Track HTML-only conditional blocks
        if '{.content-visible when-format="html"}' in line:
            in_html_only_block = True
            html_block_depth = 0
        elif in_html_only_block and stripped.startswith(":::"):
            if html_block_depth == 0:
                in_html_only_block = False
            else:
                html_block_depth -= 1
        elif in_html_only_block and ":::" in line:
            html_block_depth += 1

        # Track epub/pdf exclusion blocks (content-hidden when-format="epub" then "pdf")
        if '{.content-hidden when-format="epub"}' in line and stripped.startswith(":::"):
            epub_pdf_stack.append("epub")
        elif '{.content-hidden when-format="pdf"}' in line and stripped.startswith(":::"):
            epub_pdf_stack.append("pdf")
        elif stripped == ":::" and epub_pdf_stack:
            epub_pdf_stack.pop()

        in_epub_pdf_exclusion = (
            len(epub_pdf_stack) >= 2
            and epub_pdf_stack[-2] == "epub"
            and epub_pdf_stack[-1] == "pdf"
        )
        gif_is_wrapped = in_html_only_block or in_epub_pdf_exclusion

        # Check for GIF references (markdown or HTML)
        markdown_matches = _markdown_gif_pattern.finditer(line)
        html_matches = _html_gif_pattern.finditer(line)

        # Check markdown GIF references
        for match in markdown_matches:
            if not gif_is_wrapped:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message='GIF file not wrapped in format-exclusion block - will fail in PDF/epub. Wrap in ::: {.content-visible when-format="html"} or ::: {.content-hidden when-format="epub"} + ::: {.content-hidden when-format="pdf"}',
                        context=line.strip()[:80],
                    )
                )
            else:
                # Even inside block, markdown syntax might not work - warn to use HTML
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message="GIF uses markdown syntax - use HTML <img> tag instead for better compatibility",
                        context=line.strip()[:80],
                    )
                )

        # Check HTML GIF references
        for match in html_matches:
            if not gif_is_wrapped:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message='GIF file not wrapped in format-exclusion block - will fail in PDF/epub. Wrap in ::: {.content-visible when-format="html"} or ::: {.content-hidden when-format="epub"} + ::: {.content-hidden when-format="pdf"}',
                        context=line.strip()[:80],
                    )
                )


def check_include_directives(content: str, filepath: str, lines: List[str]):
    """
    Check for broken Quarto include directives: {{< include path.qmd >}}
    Ensures that all included files exist relative to the current file.
    """
    # Early return if no include directives in file
    if "{{< include" not in content:
        return

    file_dir = os.path.dirname(filepath)

    for line_index, line in enumerate(lines):
        # Skip lines that are HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()):
            continue
        # Skip if this line contains <!-- before the include and --> after it
        if "<!--" in line and "-->" in line:
            continue

        matches = _RE_INCLUDE_DIRECTIVE.finditer(line)
        for match in matches:
            include_path = match.group(1).strip()

            # Skip URLs
            if include_path.startswith("http://") or include_path.startswith("https://"):
                continue

            # Resolve the include path (handles both relative and absolute /paths)
            resolved_path = resolve_link_path(include_path, file_dir)

            if not os.path.exists(resolved_path):
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message=f"Broken include directive: {include_path} (target file not found)",
                        context=line.strip()[:80],
                    )
                )


def check_inline_expressions(content: str, filepath: str):
    """
    Check for inline code expressions which are incompatible with Jupyter Cache.
    Inline expressions like `{python} variable` or `{r} code` cannot be used with cache: true.
    Users should use regular Python code blocks instead.
    """
    lines = content.split("\n")

    # Pattern to match inline code expressions: `{python} ...` or `{r} ...`
    # Also match variations like `python ...` without braces
    inline_expr_patterns = [
        re.compile(r"`\{python\}[^`]+`"),
        re.compile(r"`\{r\}[^`]+`"),
        re.compile(r"`python [^`]+`"),
        re.compile(r"`r [^`]+`"),
    ]

    for line_index, line in enumerate(lines):
        # Skip code blocks
        if line.strip().startswith("```"):
            continue

        for pattern in inline_expr_patterns:
            matches = pattern.finditer(line)
            for match in matches:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message="Inline code expression found - these are incompatible with Jupyter Cache (cache: true). Use a regular Python code block instead.",
                        context=line.strip()[:80],
                    )
                )


def check_figure_file_frontmatter(content: str, filepath: str, lines: List[str]):
    """
    Check that figure files (in knowledge/figures/) do not have YAML frontmatter.
    Figure files should start directly with Python code blocks, not frontmatter.
    Frontmatter is unnecessary and adds clutter to figure-generating scripts.
    """
    # Only check files in knowledge/figures/ directory
    normalized_path = os.path.normpath(filepath)
    if not ("knowledge" + os.sep + "figures" in normalized_path or "knowledge/figures" in normalized_path):
        return

    # Check if file starts with frontmatter delimiter (---)
    if lines and lines[0].strip() == "---":
        errors.append(
            ValidationError(
                file=filepath,
                line=1,
                message="Figure file should not have YAML frontmatter. Remove the frontmatter section (--- ... ---) and start directly with Python code block.",
                context="---",
            )
        )


def check_duplicate_latex_variables(content: str, filepath: str, lines: List[str]):
    """
    Check for duplicate _latex variables within the same file.
    Having the same _latex variable appear multiple times in a file indicates
    redundant LaTeX equations that should be consolidated.
    """
    # Early return if no _latex variables in file
    if "_latex" not in content:
        return

    # Track all _latex variable occurrences with line numbers
    latex_var_occurrences: Dict[str, List[int]] = {}

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()) or ("<!--" in line and "-->" in line):
            continue

        matches = _RE_LATEX_VAR.finditer(line)
        for match in matches:
            var_name = match.group(1)
            if var_name not in latex_var_occurrences:
                latex_var_occurrences[var_name] = []
            latex_var_occurrences[var_name].append(line_index + 1)

    # Report duplicates
    for var_name, line_numbers in latex_var_occurrences.items():
        if len(line_numbers) > 2:
            errors.append(
                ValidationError(
                    file=filepath,
                    line=line_numbers[0],
                    message=f"Redundant _latex variable: {{{{< var {var_name} >}}}} appears {len(line_numbers)} times (lines {', '.join(map(str, line_numbers))}). Allow maximum 2 instances (verification + summary).",
                    context=f"First occurrence on line {line_numbers[0]}, also on: {', '.join(map(str, line_numbers[1:]))}",
                )
            )


def check_unclosed_code_blocks(content: str, filepath: str, lines: List[str]):
    """
    Check for unclosed code blocks (``` without matching closing ```).
    Unclosed code blocks cause code to leak into rendered output, which can break LaTeX compilation.
    """
    in_code_block = False
    code_block_start_line = 0
    code_block_language = ""

    for line_index, line in enumerate(lines):
        stripped = line.strip()

        # Check for code block delimiter
        if stripped.startswith("```"):
            if not in_code_block:
                # Opening code block
                in_code_block = True
                code_block_start_line = line_index + 1
                # Extract language identifier (e.g., ```{python} or ```python)
                code_block_language = stripped[3:].strip() if len(stripped) > 3 else ""
            else:
                # Closing code block
                in_code_block = False
                code_block_language = ""

    # If we're still in a code block at the end of the file, it's unclosed
    if in_code_block:
        errors.append(
            ValidationError(
                file=filepath,
                line=code_block_start_line,
                message=f"Unclosed code block (missing closing ```) - code block starting with ```{code_block_language} is never closed. This causes code to leak into rendered output and breaks LaTeX compilation.",
                context=f"```{code_block_language}",
            )
        )


def check_quarto_variables_in_links(content: str, filepath: str, lines: List[str]):
    """
    Check for Quarto variables inside markdown link text.
    Quarto variables don't work inside link text: [{{< var ... >}}](url)
    They should be moved outside the link or replaced with plain text.
    """
    # Early return if no Quarto variables in file
    if "{{< var" not in content:
        return

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()) or ("<!--" in line and "-->" in line):
            continue

        matches = _RE_LINK_WITH_VAR.finditer(line)
        for match in matches:
            context = line.strip()[:80]
            errors.append(
                ValidationError(
                    file=filepath,
                    line=line_index + 1,
                    message="Quarto variable inside link text - variables do not render inside links. Remove the link brackets since variables already have their own links built-in.",
                    context=context,
                )
            )


def check_markdown_links(content: str, filepath: str, lines: List[str]):
    """
    Check all markdown links in the file for:
    - Broken file references (for local files)
    - Malformed paths with '...'
    - References to old migration directories
    """
    file_dir = os.path.dirname(filepath)

    in_code_block = False
    for line_index, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Skip HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()) or ("<!--" in line and "-->" in line):
            continue

        matches = _RE_MARKDOWN_LINK.finditer(line)
        for match in matches:
            match.group(1)
            link_path = match.group(2).strip()

            # Skip URLs
            if link_path.startswith("http://") or link_path.startswith("https://"):
                continue
            # Skip mailto links
            if link_path.startswith("mailto:"):
                continue
            # Skip anchors
            if link_path.startswith("#"):
                continue

            # Check for malformed paths with '...'
            if ".../" in link_path:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message=f'Malformed path with "...": {link_path}',
                        context=line.strip()[:80],
                    )
                )
                continue


            # For local file links, check if the file exists
            # Split off any anchor (#section)
            link_file = link_path.split("#")[0] if "#" in link_path else link_path

            if link_file:  # If there's actually a file path (not just an anchor)
                # Resolve the path (handles both relative and absolute /paths)
                resolved_path = resolve_link_path(link_file, file_dir)

                # Check if file exists as-is
                if os.path.exists(resolved_path):
                    continue  # File exists, link is valid

                # If link has .html extension but file doesn't exist, check for corresponding .qmd
                # (since .html files are generated from .qmd during rendering)
                if link_file.endswith(".html"):
                    qmd_path = resolved_path[:-5] + ".qmd"  # Replace .html with .qmd
                    if os.path.exists(qmd_path):
                        continue  # Source .qmd exists, will be rendered to .html - link is valid
                    else:
                        # Neither .html nor .qmd exists - broken link
                        errors.append(
                            ValidationError(
                                file=filepath,
                                line=line_index + 1,
                                message=f"Broken link: {link_path} (target file not found, and no corresponding .qmd file)",
                                context=line.strip()[:80],
                            )
                        )
                # If link is extensionless (format-agnostic), check for .qmd source file
                # Quarto will resolve extensionless paths appropriately for each output format
                elif not any(link_file.endswith(ext) for ext in [".html", ".qmd", ".md", ".pdf", ".epub"]):
                    # Extensionless path - check for .qmd source file
                    qmd_path = resolved_path + ".qmd"
                    if os.path.exists(qmd_path):
                        continue  # Source .qmd exists, Quarto will resolve the link - valid
                    else:
                        # No .qmd source found - broken link
                        errors.append(
                            ValidationError(
                                file=filepath,
                                line=line_index + 1,
                                message=f"Broken link: {link_path} (no corresponding .qmd source file found)",
                                context=line.strip()[:80],
                            )
                        )
                else:
                    # File with extension doesn't exist
                    errors.append(
                        ValidationError(
                            file=filepath,
                            line=line_index + 1,
                            message=f"Broken link: {link_path} (target file not found)",
                            context=line.strip()[:80],
                        )
                    )


def load_anchor_ids(filepath: str) -> Set[str]:
    """
    Load all anchor IDs from a .qmd or .md file.
    Matches patterns like:
    - HTML anchor tags: <a id="anchor-name"></a>
    - Quarto explicit anchors in headings: ## Heading {#anchor-name}
    - Quarto auto-generated anchors from headings (converted to anchor format)
    Returns a set of anchor ID names.
    """
    anchor_ids: Set[str] = set()

    if not os.path.exists(filepath):
        return anchor_ids

    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Pattern to match HTML anchor tags: <a id="anchor-name"></a>
        # Also matches variations with spaces: <a id = "anchor-name" ></a>
        html_anchor_pattern = re.compile(r'<a\s+id\s*=\s*["\']([^"\']+)["\']\s*></a>', re.IGNORECASE)
        html_matches = html_anchor_pattern.finditer(content)
        for match in html_matches:
            anchor_ids.add(match.group(1))

        # Pattern to match Quarto explicit anchors in headings: ## Heading {#anchor-name}
        # Matches: # Heading {#anchor-id} or ## Heading {#anchor-id} etc.
        quarto_anchor_pattern = re.compile(r'^(#+\s+.+)\{#([^}]+)\}', re.MULTILINE)
        headings_with_explicit_anchors: Set[str] = set()
        quarto_matches = quarto_anchor_pattern.finditer(content)
        for match in quarto_matches:
            anchor_ids.add(match.group(2))
            # Track the full heading line (without the anchor) to skip auto-generation
            headings_with_explicit_anchors.add(match.group(0))

        # Also generate auto-anchor IDs from headings (Quarto's default behavior)
        # Pattern: ## Heading Text -> heading-text
        # BUT skip headings that have explicit anchors (Quarto only uses the explicit one)
        heading_pattern = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
        heading_matches = heading_pattern.finditer(content)
        for match in heading_matches:
            full_line = match.group(0)
            # Skip if this heading has an explicit anchor
            if full_line in headings_with_explicit_anchors:
                continue
            heading_text = match.group(1).strip()
            # Convert to anchor format: lowercase, replace spaces/special chars with hyphens
            anchor_id = re.sub(r'[^\w\s-]', '', heading_text.lower())
            anchor_id = re.sub(r'[-\s]+', '-', anchor_id)
            anchor_id = anchor_id.strip('-')
            if anchor_id:  # Only add non-empty anchor IDs
                anchor_ids.add(anchor_id)

        return anchor_ids
    except Exception as e:
        logger.debug(f"Warning: Failed to load anchor IDs from {filepath}: {str(e)}")
        return anchor_ids


def _load_anchor_ids_worker(filepath: str) -> Tuple[str, Set[str]]:
    """Worker function for parallel anchor ID loading."""
    anchor_ids = load_anchor_ids(filepath)
    return (os.path.normpath(filepath), anchor_ids)


def load_all_anchor_ids() -> Dict[str, Set[str]]:
    """
    Load anchor IDs from all .qmd files in the project.
    Uses parallel processing for faster loading on multi-core systems.
    Returns a dictionary mapping file paths to sets of anchor IDs.
    """
    anchor_map: Dict[str, Set[str]] = {}

    # Find all .qmd files using centralized file utilities
    all_files = find_files_by_extension((".qmd",))

    # Load anchor IDs in parallel using ThreadPoolExecutor
    # I/O bound task, so threads work well (no GIL issues for file reading)
    with ThreadPoolExecutor(max_workers=min(32, os.cpu_count() or 4)) as executor:
        futures = {executor.submit(_load_anchor_ids_worker, f): f for f in all_files}

        for future in as_completed(futures):
            try:
                normalized_path, anchor_ids = future.result()
                if anchor_ids:
                    anchor_map[normalized_path] = anchor_ids
            except Exception:
                pass  # Skip files that fail to load

    return anchor_map


def check_anchor_ids(content: str, filepath: str, anchor_map: Dict[str, Set[str]], lines: List[str]):
    """
    Check that all anchor IDs referenced in links actually exist in the target files.
    Validates patterns like: [text](path/to/file.qmd#anchor-id)
    """
    file_dir = os.path.dirname(filepath)

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()) or ("<!--" in line and "-->" in line):
            continue

        matches = _RE_MARKDOWN_LINK.finditer(line)
        for match in matches:
            link_path = match.group(2).strip()

            # Skip URLs
            if link_path.startswith("http://") or link_path.startswith("https://"):
                continue

            # Skip anchors-only (same-page anchors)
            if link_path.startswith("#"):
                continue

            # Check if link has an anchor
            if "#" in link_path:
                link_file, anchor_id = link_path.split("#", 1)
            else:
                continue  # No anchor to validate

            # Skip if no file path (just an anchor)
            if not link_file:
                continue

            # Resolve the link path (handles both relative and absolute /paths)
            resolved_path = resolve_link_path(link_file, file_dir)

            # Check if file exists
            if not os.path.exists(resolved_path):
                continue  # File doesn't exist - will be caught by other checks

            # Look up anchor IDs for this file
            normalized_target = os.path.normpath(resolved_path)
            target_anchors = anchor_map.get(normalized_target, set())

            # Check if anchor ID exists
            if anchor_id not in target_anchors:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message=f"Broken anchor link: {link_path} (anchor ID '{anchor_id}' not found in target file)",
                        context=line.strip()[:80],
                    )
                )


def load_defined_variables() -> Tuple[Set[str], Optional[dict]]:
    """
    Load all defined variables from _variables.yml.
    Returns (set of variable names, raw parsed dict or None).
    """
    variables_file = "_variables.yml"
    defined_vars: Set[str] = set()

    if not os.path.exists(variables_file):
        logger.debug(f"Warning: {variables_file} not found, skipping variable validation")
        return defined_vars, None

    if yaml is None:
        logger.debug("Warning: PyYAML not installed, skipping variable validation")
        logger.debug("  Install with: pip install pyyaml")
        return defined_vars, None

    try:
        with open(variables_file, encoding="utf-8") as f:
            variables = _yaml_safe_load(f)

        # Variables are the top-level keys in the YAML file
        if isinstance(variables, dict):
            defined_vars = set(variables.keys())

        return defined_vars, variables
    except Exception as e:
        logger.debug(f"Warning: Failed to parse {variables_file}: {str(e)}")
        return defined_vars, None


def check_variable_link_targets(variables_data=None):
    """
    Check that href targets in _variables.yml values point to existing .qmd files.
    Generated parameter links use .html extensions; this converts them back to .qmd
    and verifies the source file exists on disk.
    """
    variables_file = "_variables.yml"

    # Reuse pre-parsed YAML data if provided (avoids re-parsing 400KB file)
    if variables_data is not None:
        variables = variables_data
    else:
        if not os.path.exists(variables_file):
            return
        try:
            with open(variables_file, encoding="utf-8") as f:
                variables = _yaml_safe_load(f)
        except Exception:
            return

    if not isinstance(variables, dict):
        return

    # Get the union of all configs' chapter lists for rendered-file checking
    all_config_qmd_files = get_all_book_qmd_files()

    href_pattern = re.compile(r'href=\\"([^"\\]+)\\"|href="([^"]+)"')
    broken_count = 0
    not_in_config_count = 0

    for var_name, value in variables.items():
        if not isinstance(value, str) or "href" not in value:
            continue

        for match in href_pattern.finditer(value):
            href = match.group(1) or match.group(2)

            # Skip external URLs and anchors-only
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue

            # Strip fragment
            path = href.split("#")[0]
            if not path:
                continue

            # Strip leading slash for absolute paths
            path = path.lstrip("/")

            # Convert .html to .qmd
            if path.endswith(".html"):
                path = path[:-5] + ".qmd"

            if not os.path.exists(path):
                broken_count += 1
                errors.append(ValidationError(
                    variables_file, 0,
                    f"Variable '{var_name}' links to missing file",
                    f"href target '{href}' -> '{path}' does not exist"
                ))
            elif path.endswith(".qmd"):
                # File exists on disk; check if it's in any config's chapter list.
                # A file not in any config won't be rendered, so links to it will be broken.
                normalized_path = path.replace("\\", "/")
                if normalized_path not in all_config_qmd_files:
                    not_in_config_count += 1
                    errors.append(ValidationError(
                        variables_file, 0,
                        f"Variable '{var_name}' links to file not in any config's chapter list",
                        f"href target '{href}' -> '{normalized_path}' exists on disk but won't be rendered"
                    ))

    if broken_count > 0:
        logger.debug(f"  Found {broken_count} broken link target(s) in _variables.yml")
    elif not_in_config_count > 0:
        logger.debug(f"  All variable link targets exist on disk, but {not_in_config_count} target(s) not in any config chapter list (may be broken in rendered output)")
    else:
        logger.debug("  All variable link targets OK")


def check_unknown_variables(content: str, filepath: str, defined_vars: Set[str], lines: List[str]):
    """
    Check for Quarto variables that are referenced but not defined in _variables.yml
    Pattern: {{< var variable_name >}}
    """
    if not defined_vars:
        return

    # Early return if no Quarto variables in file
    if "{{< var" not in content:
        return

    for line_index, line in enumerate(lines):
        # Skip HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()) or ("<!--" in line and "-->" in line):
            continue

        matches = _RE_VAR_REFERENCE.finditer(line)
        for match in matches:
            var_name = match.group(1).strip()

            # Check if variable is defined
            if var_name not in defined_vars:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message=f"Unknown Quarto variable: {{{{< var {var_name} >}}}} - not defined in _variables.yml",
                        context=line.strip()[:80],
                    )
                )


def load_citations_from_bib() -> Set[str]:
    """
    Load citation IDs from references.bib and knowledge/appendix/iab-references.bib.
    Returns set of citation keys (e.g., 'recovery-trial-82x-cost-reduction')

    Note: references.bib is the single source of truth for all citations
    """
    citation_ids = set()

    # Main bibliography file (single source of truth)
    bib_files = [
        ("references.bib", "Single source of truth for all citations"),
        ("knowledge/appendix/iab-references.bib", "IAB paper references"),
    ]

    total_citations = 0
    for bib_file, description in bib_files:
        if not os.path.exists(bib_file):
            if bib_file == "references.bib":
                logger.debug(f"Warning: {bib_file} not found")
            continue  # Skip optional files silently

        try:
            with open(bib_file, encoding="utf-8") as f:
                content = f.read()

            # Pattern to match BibTeX entry keys: @type{key,
            # e.g., @article{smith2021, or @misc{recovery-trial-82x-cost-reduction,
            entry_pattern = re.compile(r'@\w+\{([^,]+),')

            count = 0
            for match in entry_pattern.finditer(content):
                citation_id = match.group(1).strip()
                citation_ids.add(citation_id)
                count += 1

            if count > 0:
                logger.debug(f"  Loaded {count} citations from {bib_file}")
                logger.debug(f"  ({description})")
                total_citations += count

        except Exception as e:
            logger.debug(f"Warning: Failed to parse {bib_file}: {str(e)}")

    return citation_ids


_QUARTO_XREF_PREFIXES = ('sec-', 'fig-', 'tbl-', 'eq-', 'thm-', 'lst-', 'exm-', 'def-', 'nte-', 'tip-', 'wrn-', 'imp-', 'cau-', 'prp-', 'cnj-', 'lem-', 'cor-', 'exr-', 'sol-')
_RE_CITATION_SPLIT = re.compile(r'[,\s]+$')


def check_citations(content: str, filepath: str, defined_citations: Set[str], lines: List[str]):
    """
    Check for citations that are referenced but not defined in references.bib
    Pattern: [@citation-id] or @citation-id (bare citations in text/tables)
    """
    if not defined_citations:
        return

    # Early return if no @ signs in file (no possible citations)
    if "@" not in content:
        return

    in_code_block = False

    for line_index, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Skip HTML comments
        if _RE_HTML_COMMENT_START.match(line.strip()) or ("<!--" in line and "-->" in line):
            continue

        # Check bracketed citations: [@citation-id]
        matches = _RE_BRACKETED_CITATION.finditer(line)
        for match in matches:
            # Extract all citation IDs from the match (handles multiple citations like [@a; @b])
            citation_text = match.group(1)
            # Split by semicolon and @ to get individual citation IDs
            citation_ids = [c.strip() for c in re.split(r'[;@]', citation_text) if c.strip()]

            for citation_id in citation_ids:
                # Remove any trailing punctuation or spaces
                citation_id = _RE_CITATION_SPLIT.sub('', citation_id)

                # Check if citation is defined in references.bib
                if citation_id and citation_id not in defined_citations:
                    errors.append(
                        ValidationError(
                            file=filepath,
                            line=line_index + 1,
                            message=f"Missing citation: [@{citation_id}] - not found in references.bib. Search references.bib for correct ID, or add new BibTeX entry to references.bib",
                            context=line.strip()[:80],
                        )
                    )

        # Check bare citations: @citation-id (without brackets)
        bare_matches = _RE_BARE_CITATION.finditer(line)
        for match in bare_matches:
            citation_id = match.group(1)

            # Skip Quarto cross-references (@sec-xxx, @fig-xxx, etc.)
            if citation_id.startswith(_QUARTO_XREF_PREFIXES):
                continue

            # Skip if this looks like it's inside an already-matched bracketed citation
            # (the bare pattern might match the @ inside [@...])
            match_start = match.start()
            if match_start > 0 and line[match_start - 1] == '[':
                continue

            # Check if citation is defined in references.bib
            if citation_id and citation_id not in defined_citations:
                errors.append(
                    ValidationError(
                        file=filepath,
                        line=line_index + 1,
                        message=f"Missing citation: @{citation_id} - not found in references.bib. Search references.bib for correct ID, or add new BibTeX entry to references.bib",
                        context=line.strip()[:80],
                    )
                )


def validate_quarto_config():
    """
    Validate _quarto.yml configuration file.
    Checks that all referenced .qmd files in chapters and appendices exist.
    """
    config_path = "_quarto.yml"
    if not os.path.exists(config_path):
        logger.debug(f"Warning: {config_path} not found, skipping config validation")
        return

    if yaml is None:
        logger.debug("Warning: PyYAML not installed, skipping _quarto.yml validation")
        return

    try:
        with open(config_path, encoding="utf-8") as f:
            config = _yaml_safe_load(f)
    except Exception as e:
        errors.append(
            ValidationError(
                file=config_path, line=1, message=f"Failed to parse YAML: {str(e)}", context="(unable to read file)"
            )
        )
        return

    def check_file_refs(items, parent_key=""):
        """Recursively check file references in config structure"""
        if isinstance(items, dict):
            # Check for file references (chapters can be strings or dicts with 'href')
            if isinstance(items, str) and items.endswith(".qmd"):
                if not os.path.exists(items):
                    errors.append(
                        ValidationError(
                            file=config_path,
                            line=1,
                            message=f"Chapter file not found: {items}",
                            context=f"Referenced in {parent_key}" if parent_key else "book.chapters",
                        )
                    )
            # Recurse into dict values
            for key, value in items.items():
                check_file_refs(value, key)
        elif isinstance(items, list):
            # Check each item in list
            for item in items:
                if isinstance(item, str) and item.endswith(".qmd"):
                    if not os.path.exists(item):
                        errors.append(
                            ValidationError(
                                file=config_path,
                                line=1,
                                message=f"Chapter file not found: {item}",
                                context=f"Referenced in {parent_key}" if parent_key else "book.chapters",
                            )
                        )
                else:
                    check_file_refs(item, parent_key)

    # Check book chapters
    if "book" in config:
        if "chapters" in config["book"]:
            check_file_refs(config["book"]["chapters"], "book.chapters")
        if "appendices" in config["book"]:
            check_file_refs(config["book"]["appendices"], "book.appendices")


def validate_file(filepath: str, defined_vars: Set[str], defined_parameters: Set[str], anchor_map: Dict[str, Set[str]], defined_citations: Set[str]):
    """Validate a single file"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        return

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Split lines ONCE and pass to all check functions (avoids 22 redundant splits per file)
    lines = content.split("\n")

    # For .md files, only check broken links (skip citation validation - .md files often contain examples)
    if filepath.lower().endswith(".md"):
        check_cross_reference_links(content, filepath, lines)
        check_markdown_links(content, filepath, lines)
        check_anchor_ids(content, filepath, anchor_map, lines)
        return

    # For .qmd files, run all validation checks

    # Check for common LaTeX patterns
    for pattern_config in latex_patterns:
        pattern = pattern_config["pattern"]
        message = pattern_config["message"]
        validator = pattern_config.get("validator")

        for match in pattern.finditer(content):
            if validator and validator(match.group(0)):
                continue
            before_match = content[: match.start()]
            line_number = before_match.count("\n") + 1
            line = lines[line_number - 1] if line_number <= len(lines) else ""
            errors.append(ValidationError(file=filepath, line=line_number, message=message, context=line.strip()[:80]))

    check_math_delimiters(content, filepath, lines)
    check_image_paths(content, filepath, lines)
    check_figure_caption_latex_safety(content, filepath, lines)
    check_cross_reference_links(content, filepath, lines)
    check_figure_file_imports(content, filepath)
    check_python_imports(content, filepath, lines)
    check_parameter_imports(content, filepath, defined_parameters, lines)
    check_graphviz_variables(content, filepath, lines)
    check_em_dashes(content, filepath, lines)
    check_filler_phrases(content, filepath, lines)
    check_hardcoded_figure_paths(content, filepath, lines)
    check_gif_references(content, filepath, lines)
    check_include_directives(content, filepath, lines)
    check_markdown_links(content, filepath, lines)
    check_anchor_ids(content, filepath, anchor_map, lines)
    check_quarto_variables_in_links(content, filepath, lines)
    check_unknown_variables(content, filepath, defined_vars, lines)
    check_citations(content, filepath, defined_citations, lines)
    check_figure_file_frontmatter(content, filepath, lines)
    check_unclosed_code_blocks(content, filepath, lines)
    check_duplicate_latex_variables(content, filepath, lines)


def check_source_image_dpi():
    """Check source images for bad DPI metadata or oversized physical dimensions.

    Images with bad DPI (0 or 1) cause Word/EPUB to render them at hundreds of inches.
    Run 'python scripts/normalize-image-dpi.py --apply' to fix.
    """
    logger.debug("Checking source image DPI metadata...")
    image_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")
    if not os.path.isdir(image_dir):
        logger.debug("  Skipping (assets/images not found)")
        return

    try:
        from PIL import Image as PILImage
    except ImportError:
        logger.debug("  Skipping (Pillow not installed)")
        return

    supported = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}
    bad_dpi_count = 0
    MAX_INCHES = 10.0
    MIN_DPI = 72

    for root, _dirs, files in os.walk(image_dir):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in supported:
                continue
            fpath = os.path.join(root, fname)
            try:
                img = PILImage.open(fpath)
                w, h = img.size
                dpi = img.info.get("dpi", None)

                if dpi is None:
                    eff = 96
                else:
                    dx, dy = dpi
                    if dx < MIN_DPI or dy < MIN_DPI:
                        rel = os.path.relpath(fpath)
                        errors.append(ValidationError(
                            file=rel, line=0,
                            message=f"Bad DPI metadata ({dx}x{dy}). Run: python scripts/normalize-image-dpi.py --apply",
                            context=f"{w}x{h}px at {dx}x{dy} DPI"
                        ))
                        bad_dpi_count += 1
                        continue
                    eff = min(dx, dy)

                w_in = w / eff
                h_in = h / eff
                if w_in > MAX_INCHES or h_in > MAX_INCHES:
                    # Only warn for truly extreme cases (>20 inches), not the common 14-inch AI art
                    if w_in > 20 or h_in > 20:
                        rel = os.path.relpath(fpath)
                        errors.append(ValidationError(
                            file=rel, line=0,
                            message=f"Image is {w_in:.0f}x{h_in:.0f} inches at {eff:.0f} DPI. Run: python scripts/normalize-image-dpi.py --apply",
                            context=f"{w}x{h}px"
                        ))
                        bad_dpi_count += 1
            except Exception:
                pass

    if bad_dpi_count > 0:
        logger.debug(f"  Found {bad_dpi_count} images with DPI issues")
    else:
        logger.debug("  All source images OK")


def check_epub_compatibility():
    """Check source files for patterns that break EPUB/Kindle processing.

    Catches issues that epubcheck flags as FATAL or ERROR:
    - Double-dash (--) inside HTML comments (violates XML spec)
    - Backslash in URLs (Windows path separators)
    - Backslash-escaped percent in BibTeX URLs
    """
    logger.debug("Checking EPUB compatibility patterns...")
    project_root = os.path.dirname(os.path.dirname(__file__))
    issue_count = 0

    # Check QMD files for -- inside HTML comments
    _re_html_comment = re.compile(r'<!--.*?-->', re.DOTALL)
    _re_double_dash_separator = re.compile(r'---\s')  # --- used as separator line
    qmd_dir = os.path.join(project_root, "knowledge")
    if os.path.isdir(qmd_dir):
        for root, _dirs, files in os.walk(qmd_dir):
            for fname in files:
                if not fname.endswith(('.qmd', '.md')):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception:
                    continue
                for m in _re_html_comment.finditer(content):
                    comment = m.group(0)
                    # Check for --- separators inside comments (creates invalid --)
                    if _re_double_dash_separator.search(comment[4:-3]):  # Skip <!-- and -->
                        line_num = content[:m.start()].count('\n') + 1
                        rel = os.path.relpath(fpath)
                        errors.append(ValidationError(
                            file=rel, line=line_num,
                            message="HTML comment contains '---' which creates invalid '--' in XML/EPUB",
                            context="Replace --- with === inside HTML comments"
                        ))
                        issue_count += 1
                        break  # One per file is enough

    # Check references.bib for backslash in URLs
    bib_path = os.path.join(project_root, "references.bib")
    if os.path.isfile(bib_path):
        try:
            with open(bib_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip().lower().startswith('url') and '\\%' in line:
                        errors.append(ValidationError(
                            file="references.bib", line=line_num,
                            message="URL contains backslash-percent (\\%), invalid in EPUB",
                            context=line.strip()[:100]
                        ))
                        issue_count += 1
        except Exception:
            pass

    if issue_count > 0:
        logger.debug(f"  Found {issue_count} EPUB compatibility issues")
    else:
        logger.debug("  All files OK for EPUB")


def write_json_output(errors: List[ValidationError], output_path: str) -> None:
    """Write validation errors to JSON file for GitHub Actions automation."""
    json_errors = []

    for error in errors:
        json_errors.append({
            "source": "pre-render",
            "paper": "",  # Pre-render validates all files, not specific papers
            "severity": "WARNING",  # All pre-render errors are warnings
            "type": "PRE_RENDER_ERROR",
            "page": None,
            "line": error.line,
            "column": error.column,
            "message": error.message,
            "context": error.context,
            "file_path": error.file,
            "suggested_fix": "",
            "evidence_snippet": error.context,
            "locator_hint": f"Line {error.line}"
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
    """Main validation function"""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Pre-render validation for .qmd files")
    parser.add_argument(
        "--output-json", help="Write errors to JSON file (for issue automation)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose debug logging"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(message)s'
    )

    # First, regenerate _variables.yml to ensure it's current with parameters.py
    logger.debug("Regenerating _variables.yml from parameters.py...\n")
    try:
        import subprocess

        result = subprocess.run(
            [sys.executable, "scripts/generate-everything-parameters-variables-calculations-references.py"], capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"ERROR: generate-everything-parameters-variables-calculations-references.py failed with exit code {result.returncode}", file=sys.stderr)
            if result.stdout:
                print(result.stdout, file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            print("\nPre-render validation FAILED: Variable generation failed.", file=sys.stderr)
            print("Fix the issues above before rendering.\n", file=sys.stderr)
            sys.exit(1)
        else:
            # Print condensed output (just the summary lines)
            for line in result.stdout.split("\n"):
                if line.startswith("[OK]") or line.startswith("[*]"):
                    logger.debug(line)
        logger.debug("")
    except Exception as e:
        print(f"ERROR: Failed to regenerate _variables.yml: {e}\n", file=sys.stderr)
        sys.exit(1)

    logger.info("Running pre-render validation checks on .qmd files...\n")

    # Load defined variables from _variables.yml (parse once, reuse for link target check)
    logger.debug("Loading defined variables from _variables.yml...")
    defined_vars, variables_data = load_defined_variables()
    if defined_vars:
        logger.debug(f"Loaded {len(defined_vars)} defined variables")
    else:
        logger.debug("No variables loaded (PyYAML may not be installed or _variables.yml not found)")

    # Check variable link targets in _variables.yml (reuses parsed data)
    logger.debug("Checking variable link targets in _variables.yml...")
    check_variable_link_targets(variables_data)

    # Load defined parameters from dih_models/parameters.py
    logger.debug("Loading defined parameters from dih_models/parameters.py...")
    defined_parameters = load_parameter_names()
    if defined_parameters:
        logger.debug(f"Loaded {len(defined_parameters)} defined parameters")
    else:
        logger.debug("No parameters loaded (dih_models/parameters.py not found)")

    # Load anchor IDs from all files
    logger.debug("Loading anchor IDs from all .qmd and .md files...")
    anchor_map = load_all_anchor_ids()
    total_anchors = sum(len(ids) for ids in anchor_map.values())
    if anchor_map:
        logger.debug(f"Loaded {total_anchors} anchor IDs from {len(anchor_map)} files")
    else:
        logger.debug("No anchor IDs loaded")

    # Load citations from references.bib
    logger.debug("Loading citations from references.bib...")
    defined_citations = load_citations_from_bib()
    if defined_citations:
        logger.debug(f"Loaded {len(defined_citations)} citation IDs")
    else:
        logger.debug("No citations loaded")

    # Validate _quarto.yml configuration first
    validate_quarto_config()

    # Check source images for bad DPI / oversized physical dimensions
    check_source_image_dpi()

    # Check for patterns that break EPUB/Kindle
    check_epub_compatibility()

    # Find all .qmd files using centralized file utilities
    qmd_files = find_files_by_extension((".qmd",))
    # Exclude references.qmd from validation
    qmd_files = [f for f in qmd_files if not f.endswith("references.qmd")]
    # Exclude index.qmd (use index-book.qmd instead - index.qmd is for website, index-book.qmd is for book)
    qmd_files = [f for f in qmd_files if not f.endswith("index.qmd") or f.endswith("index-manual.qmd")]

    # Skip .md files - they're documentation, not part of the Quarto book
    # (anchor IDs from .md files are still loaded for cross-reference validation)
    all_files = qmd_files
    logger.info(f"Validating {len(qmd_files)} .qmd files...")

    # Validate each file
    for file in all_files:
        validate_file(file, defined_vars, defined_parameters, anchor_map, defined_citations)

    # Write JSON output if requested
    if args.output_json and len(errors) > 0:
        write_json_output(errors, args.output_json)

    # Report results
    if len(errors) == 0:
        logger.info("No pre-validation errors found!\n")
        sys.exit(0)
    else:
        print(f"Found {len(errors)} pre-validation error(s):\n", file=sys.stderr)

        # Group errors by file
        errors_by_file: Dict[str, List[ValidationError]] = {}
        for error in errors:
            if error.file not in errors_by_file:
                errors_by_file[error.file] = []
            errors_by_file[error.file].append(error)

        # Print errors grouped by file
        has_citation_errors = False
        for file, file_errors in errors_by_file.items():
            print(f"\n{file}:", file=sys.stderr)
            for error in file_errors:
                print(f"   Line {error.line}: {error.message}", file=sys.stderr)
                print(f"   Context: {error.context}", file=sys.stderr)
                if "Missing citation" in error.message:
                    has_citation_errors = True

        print("\nPlease fix the above errors before rendering.\n", file=sys.stderr)

        # Provide additional guidance for citation errors
        if has_citation_errors:
            print("TIP: To fix missing citations:", file=sys.stderr)
            print("  1. Search references.bib for the correct citation ID: grep -i 'keyword' references.bib", file=sys.stderr)
            print("  2. If not found, add a BibTeX entry to references.bib", file=sys.stderr)
            print("  3. Re-run this validation script\n", file=sys.stderr)

        sys.exit(1)


if __name__ == "__main__":
    main()
