#!/usr/bin/env python3
"""
PDF Validation Script for Mass Publication Readiness

Comprehensive validator combining programmatic checks with optional LLM-powered
quality analysis.

Usage:
    python scripts/pdf-validation.py
    python scripts/pdf-validation.py --pdf assets/pdfs/my-paper.pdf
    python scripts/pdf-validation.py --skip-llm
    python scripts/pdf-validation.py --skip-url-check
    python scripts/pdf-validation.py --llm-pages 10
    python scripts/pdf-validation.py --fail-on-warning

Exit codes:
    0 - All checks passed (or only warnings)
    1 - Critical errors found
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Add lib to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    import llm  # type: ignore[import-not-found]
except ImportError:
    llm = None

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

# Detect GitHub Actions environment
IN_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
GITHUB_STEP_SUMMARY = os.environ.get("GITHUB_STEP_SUMMARY")
DEFAULT_PDF_DIR = Path(__file__).parent.parent / "assets" / "pdfs"
LLM_PAGE_CACHE_VERSION = 1
LLM_VALIDATION_PROMPT_VERSION = "2026-02-09-v1"


class PDFValidationError:
    """Represents a single validation error in a PDF."""

    SEVERITY_CRITICAL = "CRITICAL"
    SEVERITY_WARNING = "WARNING"
    SEVERITY_INFO = "INFO"

    def __init__(
        self,
        pdf_path: str,
        page_num: Optional[int],
        error_type: str,
        severity: str,
        message: str,
        context: str = "",
    ):
        self.pdf_path = pdf_path
        self.page_num = page_num
        self.error_type = error_type
        self.severity = severity
        self.message = message
        self.context = context

    def __str__(self):
        page_info = f"page {self.page_num}" if self.page_num is not None else "general"
        ctx = f" - {self.context}" if self.context else ""
        return f"{self.pdf_path}:{page_info} [{self.severity}:{self.error_type}] {self.message}{ctx}"

    def emit_annotation(self):
        """Emit GitHub Actions annotation for this error."""
        if not IN_GITHUB_ACTIONS:
            return

        # Escape special characters for GitHub Actions
        message = (
            self.message.replace("%", "%25")
            .replace("\r", "%0D")
            .replace("\n", "%0A")
        )
        if len(message) > 500:
            message = message[:497] + "..."

        level = "error" if self.severity == self.SEVERITY_CRITICAL else "warning"
        line = self.page_num if self.page_num else 1

        annotation = f"::{level} file={self.pdf_path},line={line},title={self.error_type}::{message}"
        print(annotation, flush=True)


# Content patterns to check (reused from post-render-validation.py)
CONTENT_PATTERNS = [
    {
        "regex": re.compile(r"NameError:|TypeError:|AttributeError:|ImportError:|ModuleNotFoundError:|KeyError:|ValueError:|IndexError:"),
        "error_type": "PYTHON_ERROR",
        "severity": PDFValidationError.SEVERITY_CRITICAL,
        "message": "Python exception found in PDF output",
    },
    {
        "regex": re.compile(r"\{\{<\s*var\s+[^>]+>\}\}"),
        "error_type": "UNRENDERED_VARIABLE",
        "severity": PDFValidationError.SEVERITY_CRITICAL,
        "message": "Unrendered Quarto variable shortcode",
    },
    {
        "regex": re.compile(r"\{python\}\s*\S"),
        "error_type": "UNRENDERED_PYTHON",
        "severity": PDFValidationError.SEVERITY_CRITICAL,
        "message": "Unrendered inline Python expression",
    },
    {
        "regex": re.compile(r"PosixPath\(|WindowsPath\("),
        "error_type": "POSIXPATH_LEAKED",
        "severity": PDFValidationError.SEVERITY_CRITICAL,
        "message": "Path object leaked into output",
    },
    {
        "regex": re.compile(r"\\frac\{|\\sum_|\\alpha|\\beta|\\gamma|\\int_|\\mathbf\{|\\text\{"),
        "error_type": "LATEX_SOURCE",
        "severity": PDFValidationError.SEVERITY_CRITICAL,
        "message": "Raw LaTeX source not rendered",
    },
    {
        "regex": re.compile(r'print\(f["\']'),
        "error_type": "PYTHON_CODE_LEAKED",
        "severity": PDFValidationError.SEVERITY_CRITICAL,
        "message": "Python print statement leaked into output",
    },
    {
        "regex": re.compile(r"\$undefined|\$NaN|undefined%|NaN%"),
        "error_type": "UNDEFINED_VALUE",
        "severity": PDFValidationError.SEVERITY_CRITICAL,
        "message": "Undefined or NaN value in output",
    },
    {
        "regex": re.compile(r"echo:\s*false|#\|\s+echo:", re.IGNORECASE),
        "error_type": "CELL_OPTIONS_LEAKED",
        "severity": PDFValidationError.SEVERITY_WARNING,
        "message": "Cell options leaked into output",
    },
    {
        "regex": re.compile(r"findfont:", re.IGNORECASE),
        "error_type": "MATPLOTLIB_WARNING",
        "severity": PDFValidationError.SEVERITY_WARNING,
        "message": "Matplotlib font warning in output",
    },
    {
        "regex": re.compile(
            r"lastToneElevationWithHumorHash|lastInstructionalVoiceHash|lastFormattedHash|lastFactCheckHash"
        ),
        "error_type": "FRONTMATTER_LEAKED",
        "severity": PDFValidationError.SEVERITY_WARNING,
        "message": "Frontmatter metadata leaked into output",
    },
]

# AI fix instructions for each error type
ERROR_FIX_INSTRUCTIONS = {
    "PDF_CORRUPTED": """
**Source:** The PDF file itself is corrupted or malformed.
**Fix:** Re-render the PDF using `python scripts/render-quarto.py <config-name>`.
If the problem persists, check the Quarto/LaTeX logs for errors.
""",
    "EMPTY_PDF": """
**Source:** The PDF has 0 pages - the render likely failed silently.
**Fix:** Check the Quarto build logs for errors. Ensure all QMD files compile correctly.
Run `python scripts/render-quarto.py <config-name> --verbose` to see detailed output.
""",
    "PYTHON_ERROR": """
**Source:** A Python exception (NameError, TypeError, etc.) was printed in the PDF.
**Fix:** Find the QMD file with the failing Python code block. The error message shows which
exception occurred. Common causes:
- Undefined variable (check _variables.yml)
- Missing import in the Python cell
- Incorrect function call
Run the QMD file in isolation to debug: `quarto preview <file>.qmd`
""",
    "UNRENDERED_VARIABLE": """
**Source:** A Quarto variable shortcode `{{< var name >}}` was not replaced.
**Fix:** Check that the variable exists in `_variables.yml` with the exact name (case-sensitive).
Run `grep "variable_name" _variables.yml` to verify. If it's a calculated variable,
run `python scripts/generate-everything-parameters-variables-calculations-references.py`.
""",
    "UNRENDERED_PYTHON": """
**Source:** An inline Python expression `{python} expr` was not evaluated.
**Fix:** Check the QMD file for malformed inline Python. The syntax should be:
`{python} expression` with a space after `{python}`. Also verify the Python
environment has all required packages installed.
""",
    "POSIXPATH_LEAKED": """
**Source:** A Python Path object was converted to string in output instead of its value.
**Fix:** Find the Python cell that creates a Path object and ensure you're calling
`str(path)` or accessing `.name` / reading the file contents instead of printing
the Path object directly.
""",
    "LATEX_SOURCE": """
**Source:** Raw LaTeX commands (\\frac, \\sum, etc.) appear in the PDF as text.
**Fix:** The LaTeX math was not properly delimited. Ensure math expressions use:
- Inline: `$expression$` or `\\(expression\\)`
- Display: `$$expression$$` or `\\[expression\\]`
Check for missing or mismatched delimiters in the QMD source.
""",
    "PYTHON_CODE_LEAKED": """
**Source:** Python source code (like `print(f"..."`) appears in the PDF.
**Fix:** A code cell is missing `#| echo: false` or the cell options weren't parsed.
Add `#| echo: false` to cells that should not show code, or check for YAML
formatting issues in the cell options block.
""",
    "UNDEFINED_VALUE": """
**Source:** A variable resolved to `$undefined`, `NaN`, or similar placeholder.
**Fix:** Check _variables.yml for the variable definition. If it's calculated,
verify the formula in parameters.py doesn't produce NaN (division by zero, etc.).
Run `python scripts/generate-everything-parameters-variables-calculations-references.py`.
""",
    "QMD_LINK": """
**Source:** A link to a .qmd file appears in the PDF instead of the rendered HTML/anchor.
**Fix:** Internal links should use `.qmd` extensions in source (Quarto converts them).
If this error appears, the link target may not be in the book's chapter list (_quarto-*.yml)
or the link syntax is malformed. Check the href in the source QMD.
""",
    "CELL_OPTIONS_LEAKED": """
**Source:** Cell options like `echo: false` or `#| ` appear as visible text.
**Fix:** The cell option block may have formatting issues. Ensure options use:
```
#| echo: false
#| warning: false
```
Check for invisible characters or incorrect indentation.
""",
    "MATPLOTLIB_WARNING": """
**Source:** A matplotlib font warning was printed during figure generation.
**Fix:** Add font configuration at the start of plotting cells:
```python
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'
```
Or suppress warnings: `import warnings; warnings.filterwarnings('ignore')`
""",
    "FRONTMATTER_LEAKED": """
**Source:** YAML frontmatter metadata (hash values, etc.) leaked into visible content.
**Fix:** Check the QMD file's frontmatter YAML block. Ensure it's properly delimited
with `---` at start and end. Also check for inline YAML that should be in frontmatter.
""",
    "BLANK_PAGE": """
**Source:** A page has very little text content (may be intentional for chapters).
**Fix:** If unintentional, check the source QMD for:
- Empty sections or divs
- Images that failed to render (leaving empty space)
- Page break commands in unexpected locations
If intentional (chapter starts), this warning can be ignored.
""",
    "MISSING_TOC": """
**Source:** The PDF has no table of contents.
**Fix:** Add TOC to the Quarto config in _quarto-*.yml:
```yaml
format:
  pdf:
    toc: true
    toc-depth: 3
```
""",
    "BROKEN_EXTERNAL_LINK": """
**Source:** An external URL in the PDF returns HTTP 4xx/5xx error.
**Fix:** The linked website may be down, moved, or the URL has a typo.
- Check the URL manually in a browser
- Update to the correct URL or use web.archive.org snapshot
- Consider if the link is still necessary
""",
    "UNREACHABLE_LINK": """
**Source:** An external URL could not be reached (timeout, DNS failure, etc.).
**Fix:** This may be a temporary network issue. Retry validation later.
If persistent, the domain may no longer exist - find an alternative source.
""",
    "MISSING_FIGURE_CAPTION": """
**Source:** Text references "Figure N" but no corresponding caption was found.
**Fix:** Check that figures have proper captions in the source:
```markdown
![Caption text here](image.png){#fig-label}
```
Or the reference may point to a non-existent figure number.
""",
    "MISSING_TABLE_CAPTION": """
**Source:** Text references "Table N" but no corresponding caption was found.
**Fix:** Ensure tables have captions. In Quarto:
```markdown
: Caption text here {#tbl-label}

| Col1 | Col2 |
|------|------|
| A    | B    |
```
""",
    "NO_IMAGES": """
**Source:** A long PDF has no embedded images.
**Fix:** This may be intentional for text-heavy papers. If images should exist:
- Check that image files exist at the referenced paths
- Verify image format is supported (PNG, JPG, PDF)
- Check Quarto logs for image embedding errors
""",
    "TINY_IMAGE": """
**Source:** An embedded image is unusually small (<10x10 pixels).
**Fix:** This may be a tracking pixel or malformed image. Check the source
QMD for the image reference and verify the original file dimensions.
""",
}

# Default instruction for unknown error types
DEFAULT_FIX_INSTRUCTION = """
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.
"""


def write_ai_fix_log(
    errors_by_type: dict,
    pdf_path: str,
    output_dir: Optional[str] = None
) -> Optional[str]:
    """
    Write a markdown log file with AI-actionable fix instructions.

    Returns the path to the log file, or None if no errors.
    """
    if not errors_by_type:
        return None

    # Determine output path
    if output_dir:
        log_dir = Path(output_dir)
    else:
        # Default to _build_temp in project root
        log_dir = Path(__file__).parent.parent / "_build_temp"

    log_dir.mkdir(parents=True, exist_ok=True)

    # Use PDF name in log filename
    pdf_name = Path(pdf_path).stem
    log_path = log_dir / f"pdf-validation-checklist-{pdf_name}.md"

    lines = [
        "# PDF Validation Errors - Checklist",
        "",
        f"**PDF:** `{pdf_path}`",
        f"**Generated:** {__import__('datetime').datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
    ]

    # Count by severity
    total = sum(len(errs) for errs in errors_by_type.values())
    critical = sum(
        len([e for e in errs if e.severity == PDFValidationError.SEVERITY_CRITICAL])
        for errs in errors_by_type.values()
    )
    warnings = sum(
        len([e for e in errs if e.severity == PDFValidationError.SEVERITY_WARNING])
        for errs in errors_by_type.values()
    )

    lines.append(f"- **Total issues:** {total}")
    lines.append(f"- **Critical:** {critical}")
    lines.append(f"- **Warnings:** {warnings}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by error type with fix instructions
    for error_type in sorted(errors_by_type.keys()):
        errors = errors_by_type[error_type]
        if not errors:
            continue

        severity = errors[0].severity
        severity_emoji = "🔴" if severity == "CRITICAL" else "🟡" if severity == "WARNING" else "ℹ️"

        lines.append(f"## {severity_emoji} {error_type} ({len(errors)} issue(s))")
        lines.append("")

        # Add fix instructions
        fix_instruction = ERROR_FIX_INSTRUCTIONS.get(error_type, DEFAULT_FIX_INSTRUCTION)
        lines.append("### How to Fix")
        lines.append(fix_instruction.strip())
        lines.append("")

        # List specific occurrences
        lines.append("### Occurrences")
        lines.append("")
        for error in errors:  # No truncation
            page_info = f"Page {error.page_num}" if error.page_num else "General"
            lines.append(f"- [ ] **{page_info}:** {error.message}")
            if error.context:
                # Truncate long context just for readability in the checklist, but keep it reasonably long
                ctx = error.context[:300] + "..." if len(error.context) > 300 else error.context
                lines.append(f"  - Context: `{ctx}`")
        lines.append("")

    # Write file
    log_path.write_text("\n".join(lines), encoding="utf-8")
    return str(log_path)


class Tee:
    """Duplicate output to a file and the original stream."""
    def __init__(self, name, mode, encoding='utf-8'):
        self.file = open(name, mode, encoding=encoding)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def __del__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
        self.file.flush()
        self.stdout.flush()

    def flush(self):
        self.file.flush()
        self.stdout.flush()


class PDFValidator:
    """Comprehensive PDF validator for publication readiness."""

    def __init__(
        self,
        pdf_path: str,
        skip_llm: bool = False,
        skip_url_check: bool = False,
        llm_sample_pages: int = 5,
        use_cache: bool = True,
    ):
        self.pdf_path = Path(pdf_path)
        self.skip_llm = skip_llm
        self.skip_url_check = skip_url_check
        self.llm_sample_pages = llm_sample_pages
        self.use_cache = use_cache
        self.doc = None
        self.errors: list[PDFValidationError] = []
        self.cache_dir = Path(__file__).parent.parent / ".cache"
        self.cache_file = self.cache_dir / "pdf-validation-cache.json"
        self.llm_page_cache_file = self.cache_dir / "pdf-validation-llm-pages.json"
        self.current_pdf_hash: str | None = None

    def _get_pdf_hash(self) -> str:
        """Compute SHA256 hash of the PDF file."""
        sha256_hash = hashlib.sha256()
        with open(self.pdf_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _load_cache(self) -> dict:
        """Load validation cache from file."""
        if not self.cache_file.exists():
            return {}
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self, cache_data: dict):
        """Save validation cache to file."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"[WARNING] Failed to save cache: {e}")

    def _load_llm_page_cache(self) -> dict:
        """Load LLM per-page validation cache."""
        if not self.llm_page_cache_file.exists():
            return {"version": LLM_PAGE_CACHE_VERSION, "entries": {}}
        try:
            with open(self.llm_page_cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            return {"version": LLM_PAGE_CACHE_VERSION, "entries": {}}

        if not isinstance(cache, dict) or cache.get("version") != LLM_PAGE_CACHE_VERSION:
            return {"version": LLM_PAGE_CACHE_VERSION, "entries": {}}
        entries = cache.get("entries")
        if not isinstance(entries, dict):
            return {"version": LLM_PAGE_CACHE_VERSION, "entries": {}}
        return cache

    def _save_llm_page_cache(self, cache_data: dict):
        """Save LLM per-page validation cache."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.llm_page_cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"[WARNING] Failed to save LLM page cache: {e}")

    def _normalize_text_for_hash(self, text: str) -> str:
        """Normalize extracted text before hashing for cache keying."""
        return re.sub(r"\s+", " ", text).strip()

    def _get_llm_model_id(self) -> str:
        """Resolve active model id used for LLM page validation."""
        model_id = getattr(llm, "GEMINI_FLASH_MODEL_ID", None) if llm else None
        return model_id if isinstance(model_id, str) and model_id.strip() else "gemini-flash"

    def _build_llm_page_cache_key(self, page_idx: int, text: str) -> str:
        """Build a stable cache key for a page-level LLM validation result."""
        normalized_text = self._normalize_text_for_hash(text)
        text_hash = hashlib.sha256(normalized_text.encode("utf-8", errors="replace")).hexdigest()
        pdf_hash = self.current_pdf_hash or self._get_pdf_hash()
        raw_key = (
            f"{pdf_hash}|{page_idx}|{text_hash}|{self._get_llm_model_id()}|"
            f"{LLM_VALIDATION_PROMPT_VERSION}"
        )
        return hashlib.sha256(raw_key.encode("utf-8", errors="replace")).hexdigest()

    def _record_llm_issues(self, page_idx: int, issues: list[dict[str, Any]]) -> int:
        """Convert parsed LLM issues into validation errors and return issue count."""
        for issue in issues:
            severity_map = {
                "CRITICAL": PDFValidationError.SEVERITY_CRITICAL,
                "WARNING": PDFValidationError.SEVERITY_WARNING,
                "INFO": PDFValidationError.SEVERITY_INFO,
            }
            severity = severity_map.get(
                issue.get("severity", "WARNING"),
                PDFValidationError.SEVERITY_WARNING,
            )

            issue_type = issue.get("type", "OTHER").upper().replace(" ", "_")
            self._add_error(
                page_idx + 1,
                f"LLM_{issue_type}",
                severity,
                issue.get("description", "LLM-detected issue"),
            )
        return len(issues)

    def _add_error(
        self,
        page_num: Optional[int],
        error_type: str,
        severity: str,
        message: str,
        context: str = "",
    ):
        """Add a validation error."""
        self.errors.append(
            PDFValidationError(
                str(self.pdf_path), page_num, error_type, severity, message, context
            )
        )

    def validate_structure(self) -> list[PDFValidationError]:
        """Validate PDF structural integrity."""
        import fitz  # PyMuPDF

        # Check if PDF opens
        try:
            self.doc = fitz.open(self.pdf_path)
        except Exception as e:
            self._add_error(
                None,
                "PDF_CORRUPTED",
                PDFValidationError.SEVERITY_CRITICAL,
                f"Cannot open PDF: {e}",
            )
            return self.errors

        # Check page count
        page_count = len(self.doc)
        if page_count == 0:
            self._add_error(
                None,
                "EMPTY_PDF",
                PDFValidationError.SEVERITY_CRITICAL,
                "PDF has 0 pages",
            )
            return self.errors

        if page_count > 2000:
            self._add_error(
                None,
                "EXCESSIVE_PAGES",
                PDFValidationError.SEVERITY_WARNING,
                f"PDF has {page_count} pages (>2000)",
            )

        # Check TOC
        toc = self.doc.get_toc()
        if not toc:
            self._add_error(
                None,
                "MISSING_TOC",
                PDFValidationError.SEVERITY_WARNING,
                "PDF has no table of contents",
            )

        # Check metadata
        metadata = self.doc.metadata
        if not metadata or not metadata.get("title"):
            self._add_error(
                None,
                "MISSING_METADATA",
                PDFValidationError.SEVERITY_WARNING,
                "PDF has no title metadata",
            )



        return self.errors

    def validate_content(self) -> list[PDFValidationError]:
        """Validate content patterns for rendering issues."""
        if not self.doc:
            return self.errors

        page_count = len(self.doc)
        for page_num in range(page_count):
            page = self.doc[page_num]
            text = page.get_text() or ""
            if not isinstance(text, str):
                text = str(text)

            for pattern_config in CONTENT_PATTERNS:
                matches = pattern_config["regex"].finditer(text)
                for match in matches:
                    # Get context around match
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].replace("\n", " ").strip()

                    self._add_error(
                        page_num + 1,
                        pattern_config["error_type"],
                        pattern_config["severity"],
                        pattern_config["message"],
                        f"...{context}...",
                    )

        return self.errors

    def validate_images(self) -> list[PDFValidationError]:
        """Validate images in the PDF."""
        if not self.doc:
            return self.errors

        page_count = len(self.doc)
        total_images = 0

        for page_num in range(page_count):
            page = self.doc[page_num]
            images = page.get_images()
            total_images += len(images)



        # Check if long PDF has no images
        if page_count > 10 and total_images == 0:
            self._add_error(
                None,
                "NO_IMAGES",
                PDFValidationError.SEVERITY_INFO,
                f"PDF has {page_count} pages but no images",
            )

        return self.errors

    def validate_links(self) -> list[PDFValidationError]:
        """Validate links in the PDF."""
        if not self.doc:
            return self.errors

        page_count = len(self.doc)
        external_urls = set()

        for page_num in range(page_count):
            page = self.doc[page_num]
            links = page.get_links()

            for link in links:
                uri = link.get("uri", "")

                # Check for .qmd links (critical error)
                if uri.endswith(".qmd") or ".qmd#" in uri or ".qmd?" in uri:
                    self._add_error(
                        page_num + 1,
                        "QMD_LINK",
                        PDFValidationError.SEVERITY_CRITICAL,
                        f"Link to .qmd file: {uri}",
                    )

                # Collect external URLs for validation
                if uri.startswith(("http://", "https://")):
                    external_urls.add(uri)

        # Validate external URLs (if not skipped)
        if self.skip_url_check:
            return self.errors

        if external_urls:
            try:
                import importlib

                url_checker_module = importlib.import_module("url_checker")
                url_checker_class = getattr(url_checker_module, "URLChecker")

                checker = url_checker_class(cache_ttl_hours=24, timeout_seconds=10)
                urls_to_check = list(external_urls)[:100]  # Limit to 100 URLs

                print(f"      Checking {len(urls_to_check)} external URLs...")
                results = checker.check_urls(urls_to_check)

                for result in results:
                    if not result.is_valid:
                        cache_note = " (cached)" if result.from_cache else ""
                        if result.is_http_error:
                            # 403 is usually bot-blocking, not a broken link
                            if result.status_code == 403:
                                self._add_error(
                                    None,
                                    "URL_ACCESS_DENIED",
                                    PDFValidationError.SEVERITY_WARNING,
                                    f"{result.error_message}: {result.url}{cache_note}",
                                )
                            else:
                                # 404, 500, etc. are genuinely broken
                                self._add_error(
                                    None,
                                    "BROKEN_EXTERNAL_LINK",
                                    PDFValidationError.SEVERITY_CRITICAL,
                                    f"{result.error_message}: {result.url}{cache_note}",
                                )
                        else:
                            # Timeouts and network errors are warnings
                            self._add_error(
                                None,
                                "URL_UNREACHABLE",
                                PDFValidationError.SEVERITY_WARNING,
                                f"{result.error_message}: {result.url}{cache_note}",
                            )

            except ImportError as e:
                print(f"[WARNING] URL checker not available: {e}", file=sys.stderr)

        return self.errors

    def validate_cross_references(self) -> list[PDFValidationError]:
        """Validate cross-references (figures, tables)."""
        if not self.doc:
            return self.errors

        full_text = ""
        for page_num in range(len(self.doc)):
            page_text = self.doc[page_num].get_text() or ""
            if not isinstance(page_text, str):
                page_text = str(page_text)
            full_text += page_text + "\n"

        # Check figure references
        figure_refs = re.findall(r"Figure\s+(\d+)", full_text, re.IGNORECASE)
        figure_captions = re.findall(r"Figure\s+(\d+)\s*[:\.]", full_text, re.IGNORECASE)

        # Check for figure refs without captions
        ref_numbers = set(int(n) for n in figure_refs)
        caption_numbers = set(int(n) for n in figure_captions)

        for ref_num in ref_numbers:
            if ref_num not in caption_numbers:
                self._add_error(
                    None,
                    "MISSING_FIGURE_CAPTION",
                    PDFValidationError.SEVERITY_WARNING,
                    f"Figure {ref_num} referenced but no caption found",
                )

        # Check table references
        table_refs = re.findall(r"Table\s+(\d+)", full_text, re.IGNORECASE)
        table_captions = re.findall(r"Table\s+(\d+)\s*[:\.]", full_text, re.IGNORECASE)

        ref_numbers = set(int(n) for n in table_refs)
        caption_numbers = set(int(n) for n in table_captions)

        for ref_num in ref_numbers:
            if ref_num not in caption_numbers:
                self._add_error(
                    None,
                    "MISSING_TABLE_CAPTION",
                    PDFValidationError.SEVERITY_WARNING,
                    f"Table {ref_num} referenced but no caption found",
                )

        return self.errors

    def validate_with_llm(self) -> list[PDFValidationError]:
        """Use LLM to detect quality issues."""
        if self.skip_llm or not self.doc:
            return self.errors
            
        if not llm:
            print("[WARNING] LLM library not available, skipping LLM validation", file=sys.stderr)
            return self.errors

        page_count = len(self.doc)
        llm_page_cache = self._load_llm_page_cache() if self.use_cache else {"version": LLM_PAGE_CACHE_VERSION, "entries": {}}
        llm_page_cache_entries = llm_page_cache.setdefault("entries", {})

        # Sample pages evenly distributed.
        # llm_sample_pages <= 0 means "validate all pages".
        if self.llm_sample_pages <= 0:
            sample_indices = list(range(page_count))
        elif page_count <= self.llm_sample_pages:
            sample_indices = list(range(page_count))
        else:
            step = page_count / self.llm_sample_pages
            sample_indices = [int(i * step) for i in range(self.llm_sample_pages)]

        sample_total = len(sample_indices)
        if sample_total > 0:
            print(
                f"[LLM] Validating {sample_total} page(s) with LLM (PDF has {page_count} pages)",
                flush=True,
            )

        max_llm_retries = max(1, int(os.environ.get("PDF_VALIDATION_LLM_RETRIES", "3")))

        for sample_idx, page_idx in enumerate(sample_indices, start=1):
            print(f"[LLM] Page {sample_idx}/{sample_total} (PDF page {page_idx + 1})", flush=True)
            page = self.doc[page_idx]
            text = page.get_text() or ""
            if not isinstance(text, str):
                text = str(text)

            # Skip very short pages
            if len(text.strip()) < 100:
                print(f"[LLM] Page {sample_idx}/{sample_total} skipped (low text content)", flush=True)
                continue

            # Truncate long pages
            if len(text) > 8000:
                text = text[:8000] + "\n[...truncated...]"

            cache_key = self._build_llm_page_cache_key(page_idx, text)
            if self.use_cache:
                cached = llm_page_cache_entries.get(cache_key)
                if isinstance(cached, dict):
                    cached_issues = cached.get("issues", [])
                    if isinstance(cached_issues, list):
                        issue_count = self._record_llm_issues(page_idx, cached_issues)
                        print(
                            f"[LLM] Page {sample_idx}/{sample_total} cache hit ({issue_count} issue(s))",
                            flush=True,
                        )
                        continue

            prompt = f"""Analyze this PDF page text for publication-blocking quality defects.

Bibliography/reference pages ARE IN SCOPE. Evaluate them with the same rigor.

Conservatism rule: only flag issues you are 90%+ confident are real defects.
Do NOT flag:
- Page number mismatches (common extraction artifacts)
- Minor formatting or style differences
- Normal line wrapping, hyphenation, or spacing differences
- URL encoding in references (for example %3C/%3E) unless the link itself is truly broken
- Anything uncertain or speculative

3. Allowed issue types:
- UNRENDERED_CODE_OR_VARIABLE
- PLACEHOLDER_TEXT
- LEAKED_SOURCE_CODE
- CORRUPTED_OR_GARBLED_TEXT
- BROKEN_REFERENCE
- OTHER

Issue type guidance:
1. UNRENDERED_CODE_OR_VARIABLE: literal "{{{{python}}}}", "$undefined", "NaN", "[object Object]", Python traceback text.
2. PLACEHOLDER_TEXT: TODO/FIXME/TBD/Lorem ipsum/[INSERT ...].
3. LEAKED_SOURCE_CODE: visible Python/JavaScript code that should not be in reader-facing content.
4. CORRUPTED_OR_GARBLED_TEXT: clearly unreadable/corrupted strings, not just odd punctuation.
5. BROKEN_REFERENCE: reference entry missing core bibliographic parts or malformed links.
6. OTHER: only for severe defects that do not fit above.

Page content:
---
{text}
---

Respond with JSON only. Be VERY conservative - only flag issues you're 90%+ confident are real problems:
{{
    "issues": [
        {{
        {{
            "type": "ISSUE_TYPE",
            "description": "specific, factual defect description",
            "severity": "CRITICAL|WARNING"
        }}
    ],
    "page_quality": "good|acceptable|poor"
}}

            If no clear issues, return {{"issues": [], "page_quality": "good"}}"""

            result: Optional[dict[str, Any]] = None
            last_error = None
            try:
                for attempt in range(1, max_llm_retries + 1):
                    try:
                        # Use Gemini Flash for faster/cheaper validation
                        response = llm.generate_gemini_flash_content(prompt)
                        
                        # Log LLM details for debugging
                        print(f"\n[LLM-DEBUG] Page {page_idx + 1} Prompt ({len(prompt)} chars):")
                        print(f"{prompt[:200]}...[truncated]...")
                        print(f"[LLM-DEBUG] Page {page_idx + 1} Response:")
                        print(f"{response}\n")

                        parsed = llm.extract_json_from_response(
                            response, f"LLM page {page_idx + 1}"
                        )
                        if not isinstance(parsed, dict):
                            raise ValueError("LLM response is not a JSON object")
                        result = parsed
                        last_error = None
                        break
                    except Exception as e:
                        last_error = e
                        if attempt < max_llm_retries:
                            backoff_seconds = min(8.0, 1.5 * (2 ** (attempt - 1)))
                            print(
                                f"[INFO] LLM validation retry for page {page_idx + 1} after error "
                                f"(attempt {attempt}/{max_llm_retries}): {e}",
                                file=sys.stderr,
                            )
                            time.sleep(backoff_seconds)

                if last_error is not None:
                    raise last_error

                if result is None:
                    raise ValueError("LLM response is empty")
                issues = result.get("issues", [])
                if not isinstance(issues, list):
                    raise ValueError("LLM response issues is not a list")

                issue_count = self._record_llm_issues(page_idx, issues)
                if self.use_cache:
                    llm_page_cache_entries[cache_key] = {
                        "cached_at": datetime.now().isoformat(),
                        "model_id": self._get_llm_model_id(),
                        "prompt_version": LLM_VALIDATION_PROMPT_VERSION,
                        "issues": issues,
                    }
                print(
                    f"[LLM] Page {sample_idx}/{sample_total} complete ({issue_count} issue(s))",
                    flush=True,
                )

            except Exception as e:
                print(
                    f"[WARNING] LLM validation failed for page {page_idx + 1}: {e}",
                    file=sys.stderr,
                )

        if self.use_cache:
            self._save_llm_page_cache(llm_page_cache)

        return self.errors

    def validate(self) -> list[PDFValidationError]:
        """Run all validation checks."""
        pdf_hash = self._get_pdf_hash()
        self.current_pdf_hash = pdf_hash
        cache = self._load_cache()
        
        # Check cache if enabled
        if self.use_cache and pdf_hash in cache:
            cached_result = cache[pdf_hash]
            # Ensure the cache entry has the required fields
            if "errors" in cached_result and cached_result.get("llm_pages") == self.llm_sample_pages:
                print(f"[*] Using cached validation results for {self.pdf_path.name} (hash: {pdf_hash[:8]})")
                for err_data in cached_result["errors"]:
                    self._add_error(
                        err_data.get("page_num"),
                        err_data.get("error_type"),
                        err_data.get("severity"),
                        err_data.get("message"),
                        err_data.get("context", "")
                    )
                return self.errors

        self.validate_structure()

        # Only continue if PDF opened successfully
        if self.doc:
            self.validate_content()
            self.validate_images()
            self.validate_links()
            self.validate_cross_references()
            self.validate_with_llm()

            # Close the document
            self.doc.close()

        # Save to cache
        if self.use_cache:
            cache[pdf_hash] = {
                "pdf_name": self.pdf_path.name,
                "timestamp": datetime.now().isoformat(),
                "llm_pages": self.llm_sample_pages,
                "errors": [
                    {
                        "page_num": e.page_num,
                        "error_type": e.error_type,
                        "severity": e.severity,
                        "message": e.message,
                        "context": e.context
                    } for e in self.errors
                ]
            }
            self._save_cache(cache)

        return self.errors


def find_pdf_files(output_dir: Path) -> list[Path]:
    """Find all PDF files in the output directory."""
    return list(output_dir.rglob("*.pdf"))


def write_job_summary(errors_by_type: dict, pdf_path: str):
    """Write Job Summary for GitHub Actions."""
    if not IN_GITHUB_ACTIONS or not GITHUB_STEP_SUMMARY:
        return

    total_errors = sum(len(errors) for errors in errors_by_type.values())
    critical_count = sum(
        len([e for e in errors if e.severity == PDFValidationError.SEVERITY_CRITICAL])
        for errors in errors_by_type.values()
    )

    try:
        with open(GITHUB_STEP_SUMMARY, "a", encoding="utf-8") as f:
            if critical_count > 0:
                f.write("\n## :x: PDF Validation Failed\n\n")
            else:
                f.write("\n## :warning: PDF Validation Warnings\n\n")

            f.write(f"**PDF:** `{pdf_path}`\n\n")
            f.write(f"**{total_errors} issue(s) found** ({critical_count} critical)\n\n")

            # Error summary table
            f.write("| Error Type | Severity | Count |\n")
            f.write("|------------|----------|-------|\n")

            for error_type, errors in sorted(errors_by_type.items()):
                severity = errors[0].severity if errors else "UNKNOWN"
                f.write(f"| `{error_type}` | {severity} | {len(errors)} |\n")

            # Detailed errors
            f.write("\n### Error Details\n\n")
            for error_type, errors in sorted(errors_by_type.items()):
                f.write(f"\n<details>\n<summary><b>{error_type}</b> ({len(errors)})</summary>\n\n")
                for error in errors[:10]:
                    page_info = f"page {error.page_num}" if error.page_num else "general"
                    msg = error.message[:200]
                    f.write(f"- **{page_info}** - {msg}\n")
                if len(errors) > 10:
                    f.write(f"\n*...and {len(errors) - 10} more*\n")
                f.write("\n</details>\n")

            f.write("\n---\n")
            f.write("*Run `python scripts/pdf-validation.py` locally for full details*\n")
    except Exception as e:
        print(f"[WARNING] Failed to write job summary: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Validate PDF files for publication readiness"
    )
    parser.add_argument("--pdf", help="Specific PDF file to validate")
    parser.add_argument(
        "--skip-llm", action="store_true", help="Skip LLM-powered validation"
    )
    parser.add_argument(
        "--skip-url-check", action="store_true", help="Skip external URL validation"
    )
    parser.add_argument(
        "--llm-pages",
        type=int,
        default=5,
        help="Number of pages to sample for LLM validation",
    )
    parser.add_argument(
        "--fail-on-warning", action="store_true", help="Treat warnings as errors"
    )
    parser.add_argument(
        "--no-cache", action="store_true", help="Disable validation caching"
    )
    args = parser.parse_args()

    # Determine PDF files to validate
    if args.pdf:
        pdf_files = [Path(args.pdf)]
        if not pdf_files[0].exists():
            print(f"[ERROR] PDF file not found: {args.pdf}")
            return 1
    else:
        output_dir = DEFAULT_PDF_DIR
        if not output_dir.exists():
            print(f"[ERROR] PDF directory not found: {output_dir}")
            return 1
        pdf_files = find_pdf_files(output_dir)
        if not pdf_files:
            print(f"[WARNING] No PDF files found in {output_dir}")
            return 0

    # Logging is handled by the calling script (zenodo-upload.log) via stdout capture
    # No separate log file created here to avoid clutter

    print(f"[VALIDATION] Validating {len(pdf_files)} PDF file(s)...")
    if args.skip_llm:
        print("   (LLM validation skipped)")
    if args.skip_url_check:
        print("   (URL validation skipped)")

    all_errors = []
    has_critical = False

    for pdf_file in pdf_files:
        print(f"\n   Validating: {pdf_file}")

        validator = PDFValidator(
            str(pdf_file),
            skip_llm=args.skip_llm,
            skip_url_check=args.skip_url_check,
            llm_sample_pages=args.llm_pages,
            use_cache=not args.no_cache,
        )
        errors = validator.validate()

        if errors:
            all_errors.extend(errors)

            # Check for critical errors
            for error in errors:
                if error.severity == PDFValidationError.SEVERITY_CRITICAL:
                    has_critical = True

    # Group errors by type
    errors_by_type = defaultdict(list)
    for error in all_errors:
        errors_by_type[error.error_type].append(error)

    # Print results
    if not all_errors:
        print("\n[OK] All PDF validation checks passed!")
        if IN_GITHUB_ACTIONS and GITHUB_STEP_SUMMARY:
            try:
                with open(GITHUB_STEP_SUMMARY, "a", encoding="utf-8") as f:
                    f.write("\n## :white_check_mark: PDF Validation Passed\n\n")
                    f.write(f"Validated {len(pdf_files)} PDF file(s) with no issues.\n")
            except Exception:
                pass
        return 0

    # Count by severity
    critical_count = sum(
        1 for e in all_errors if e.severity == PDFValidationError.SEVERITY_CRITICAL
    )
    warning_count = sum(
        1 for e in all_errors if e.severity == PDFValidationError.SEVERITY_WARNING
    )
    info_count = sum(
        1 for e in all_errors if e.severity == PDFValidationError.SEVERITY_INFO
    )

    print(f"\n[RESULT] Found {len(all_errors)} issue(s):")
    print(f"   CRITICAL: {critical_count}")
    print(f"   WARNING:  {warning_count}")
    print(f"   INFO:     {info_count}")

    # Emit GitHub Actions annotations
    if IN_GITHUB_ACTIONS:
        for error in all_errors:
            error.emit_annotation()

    # Print grouped errors
    print("\n[DETAILS]")
    for error_type, errors in sorted(errors_by_type.items()):
        severity = errors[0].severity if errors else "UNKNOWN"
        print(f"\n  {error_type} [{severity}]: {len(errors)} issue(s)")
        for error in errors[:10]:
            print(f"    {error}")
        if len(errors) > 10:
            print(f"    ...and {len(errors) - 10} more")

    # Write job summary
    if pdf_files:
        write_job_summary(errors_by_type, str(pdf_files[0]))

    # Write AI fix log file
    if all_errors and pdf_files:
        log_path = write_ai_fix_log(errors_by_type, str(pdf_files[0]))
        if log_path:
            print(f"\n[AI FIX LOG] Detailed fix instructions written to:")
            print(f"             {log_path}")
            print("")
            print("  To fix these issues, read this file and follow the instructions.")
            print("  Claude/AI: Use `Read` tool on this file for actionable fix guidance.")

    # Determine exit code
    if has_critical:
        return 1
    if args.fail_on_warning and warning_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
