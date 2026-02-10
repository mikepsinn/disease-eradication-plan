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

try:
    from quarto_config_utils import discover_paper_configs  # type: ignore[import-not-found]
except ImportError:
    discover_paper_configs = None

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

# Detect GitHub Actions environment
IN_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
GITHUB_STEP_SUMMARY = os.environ.get("GITHUB_STEP_SUMMARY")
DEFAULT_PDF_DIR = Path(__file__).parent.parent / "assets" / "pdfs"
LLM_FULL_PDF_PROMPT_VERSION = "2026-02-09-v2"

LLM_FULL_PDF_PROMPT_TEXT = """Review this full PDF for publication-blocking defects.

Focus on:
- equation rendering defects
- unreadable figures/tables
- broken references/citations
- leaked source/code
- malformed bibliography entries

Be conservative: only include issues you are highly confident are true defects.
Treat PDF text extraction artifacts as non-issues unless you have strong visual evidence of an actual rendering defect.
If the PDF appears fine, return an empty errors list instead of speculative findings.
Return JSON only with this schema:
{
  "summary": "one paragraph",
  "errors": [
    {
      "severity": "CRITICAL|WARNING",
      "type": "string",
      "page": "page number or range",
      "description": "specific defect",
      "suggested_fix": "actionable fix",
      "evidence_snippet": "short exact text snippet copied from the PDF near the defect",
      "locator_hint": "how to find this in source docs using only document-visible clues (section heading, figure/table label, citation text, unique phrase)"
    }
  ],
  "high_value_improvements": ["string"]
}

Important constraints:
- You do NOT have access to source qmd/bib files. Do not invent filenames or keys.
- "locator_hint" must rely only on clues visible in the PDF.
- Keep snippets short and exact.
- `errors` may be an empty list when no clear defects are present.
- Do NOT flag extraction-layer artifacts as defects:
  - spaces/newlines inserted inside URLs (for example "https: //")
  - missing Greek/math symbols in copied text when layout appears intact
  - line-wrap hyphenation artifacts in bibliography entries
  - markdown tokens visible only in extracted text layer
  - orphan punctuation that may be extraction noise
- Only flag equation defects when mathematical meaning is actually broken in rendered layout.
- Only flag broken references/citations when a link/reference is clearly malformed in the rendered document itself.
- Do not invent issues to satisfy category coverage. If uncertain, omit the issue.
- The "errors" list MUST be sorted by page in ascending order."""


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


def find_quarto_config_for_pdf(pdf_path: str) -> Optional[str]:
    """
    Find the _quarto-*.yml config that renders the given PDF.

    Matches by `format.pdf.output-file` and fallback `dih-render.pdf-output-file`.
    Returns absolute config path string, or None when no unique match is found.
    """
    project_root = Path(__file__).parent.parent
    pdf_name = Path(pdf_path).name
    # Prefer shared config discovery logic so filename parsing stays centralized.
    if discover_paper_configs is not None:
        try:
            papers = discover_paper_configs(project_root=project_root, include_disabled=True)
            matches = []
            for _, info in papers.items():
                config_path = info.get("config_path")
                pdf_filename = info.get("pdf_filename")
                if config_path and pdf_filename and Path(str(pdf_filename)).name == pdf_name:
                    matches.append(Path(config_path))
            if len(matches) == 1:
                return str(matches[0].resolve())
        except Exception:
            pass

    # Fallback: direct scan for environments where shared lib import fails.
    candidate_configs = sorted(project_root.glob("_quarto-*.yml"))
    matches: list[Path] = []
    for config_path in candidate_configs:
        try:
            text = config_path.read_text(encoding="utf-8")
        except Exception:
            continue

        output_file_match = re.search(r'output-file:\s*"?([^"\n]+\.pdf)"?', text, flags=re.IGNORECASE)
        if output_file_match and Path(output_file_match.group(1).strip()).name == pdf_name:
            matches.append(config_path)
            continue

        fallback_match = re.search(r'pdf-output-file:\s*"?([^"\n]+\.pdf)"?', text, flags=re.IGNORECASE)
        if fallback_match and Path(fallback_match.group(1).strip()).name == pdf_name:
            matches.append(config_path)

    if len(matches) == 1:
        return str(matches[0].resolve())
    return None


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
        # Default to project root so checklists are easy to find
        log_dir = Path(__file__).parent.parent

    log_dir.mkdir(parents=True, exist_ok=True)

    # Use PDF name in log filename
    pdf_name = Path(pdf_path).stem
    log_path = log_dir / f"pdf-validation-checklist-{pdf_name}.md"
    config_path = find_quarto_config_for_pdf(pdf_path)

    lines = [
        "# PDF Validation Errors - Checklist",
        "",
        f"**PDF:** `{pdf_path}`",
        f"**Quarto config:** `{config_path}`" if config_path else "**Quarto config:** `(not auto-detected)`",
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
        use_cache: bool = True,
    ):
        self.pdf_path = Path(pdf_path)
        self.skip_llm = skip_llm
        self.skip_url_check = skip_url_check
        self.use_cache = use_cache
        self.doc = None
        self.errors: list[PDFValidationError] = []
        self.cache_dir = Path(__file__).parent.parent / ".cache"
        self.cache_file = self.cache_dir / "pdf-validation-cache.json"
        self.full_pdf_llm_cache_file = self.cache_dir / "pdf-full-review-cache.json"
        self.current_pdf_hash: str | None = None
        self.llm_requests_made = 0
        self.llm_input_tokens_est = 0.0
        self.llm_output_tokens_est = 0.0
        self.llm_cost_est_usd = 0.0

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

    def _log_cache_paths(self) -> None:
        """Log cache locations and whether files currently exist."""
        cache_dir_display = str(self.cache_dir.resolve())
        pdf_cache_display = str(self.cache_file.resolve())
        full_pdf_llm_cache_display = str(self.full_pdf_llm_cache_file.resolve())
        print(f"[CACHE] Base cache directory: {cache_dir_display}", flush=True)
        print(
            "[CACHE] Cache directory is outside _build_temp, so it is not deleted by rebuilds.",
            flush=True,
        )
        print(
            f"[CACHE] PDF cache file: {pdf_cache_display} "
            f"(exists={'yes' if self.cache_file.exists() else 'no'})",
            flush=True,
        )
        print(
            f"[CACHE] Full-PDF LLM cache file: {full_pdf_llm_cache_display} "
            f"(exists={'yes' if self.full_pdf_llm_cache_file.exists() else 'no'})",
            flush=True,
        )

    def _log_cache_inventory(
        self,
        pdf_cache: dict | None = None,
    ) -> None:
        """Log cache entry counts and file sizes for quick diagnostics."""
        if pdf_cache is not None:
            try:
                pdf_cache_entries = len(pdf_cache) if isinstance(pdf_cache, dict) else 0
                print(f"[CACHE] PDF cache entries: {pdf_cache_entries}", flush=True)
            except Exception:
                print("[CACHE] PDF cache entries: unknown (failed to count)", flush=True)

        if pdf_cache is not None and self.cache_file.exists():
            try:
                print(f"[CACHE] PDF cache file size: {self.cache_file.stat().st_size} bytes", flush=True)
            except Exception:
                print("[CACHE] PDF cache file size: unknown", flush=True)

        if self.full_pdf_llm_cache_file.exists():
            try:
                full_pdf_cache = json.loads(self.full_pdf_llm_cache_file.read_text(encoding="utf-8"))
                entries = full_pdf_cache.get("entries", {}) if isinstance(full_pdf_cache, dict) else {}
                entry_count = len(entries) if isinstance(entries, dict) else 0
                print(f"[CACHE] Full-PDF LLM cache entries: {entry_count}", flush=True)
                print(
                    f"[CACHE] Full-PDF LLM cache file size: {self.full_pdf_llm_cache_file.stat().st_size} bytes",
                    flush=True,
                )
            except Exception:
                print("[CACHE] Full-PDF LLM cache inventory: unknown", flush=True)

    def _get_llm_model_id(self) -> str:
        """Resolve active model id used for LLM page validation."""
        model_id = getattr(llm, "GEMINI_FLASH_MODEL_ID", None) if llm else None
        return model_id if isinstance(model_id, str) and model_id.strip() else "gemini-flash"


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
                total_external_urls = len(external_urls)
                urls_to_check = list(external_urls)
                print(f"      Found {total_external_urls} external URLs; validating all.")
                results = checker.check_urls(urls_to_check)

                valid_count = 0
                invalid_count = 0
                cached_count = 0
                broken_count = 0
                access_denied_count = 0
                unreachable_count = 0

                for result in results:
                    if result.from_cache:
                        cached_count += 1
                    if not result.is_valid:
                        invalid_count += 1
                        cache_note = " (cached)" if result.from_cache else ""
                        if result.is_http_error:
                            # 403 is usually bot-blocking, not a broken link
                            if result.status_code == 403:
                                access_denied_count += 1
                                # User requested to ignore 403 errors (often bot protection)
                                print(f"      [INFO] Ignoring 403 Access Denied: {result.url}{cache_note}")
                            else:
                                # 404, 500, etc. are genuinely broken
                                broken_count += 1
                                self._add_error(
                                    None,
                                    "BROKEN_EXTERNAL_LINK",
                                    PDFValidationError.SEVERITY_CRITICAL,
                                    f"{result.error_message}: {result.url}{cache_note}",
                                )
                        else:
                            # Timeouts and network errors are warnings
                            unreachable_count += 1
                            self._add_error(
                                None,
                                "URL_UNREACHABLE",
                                PDFValidationError.SEVERITY_WARNING,
                                f"{result.error_message}: {result.url}{cache_note}",
                            )
                    else:
                        valid_count += 1

                checked_count = len(results)
                fresh_count = checked_count - cached_count
                print(
                    f"      URL check summary: checked={checked_count}, valid={valid_count}, invalid={invalid_count}, "
                    f"cached={cached_count}, fresh={fresh_count}"
                )
                if invalid_count > 0:
                    print(
                        f"      Invalid breakdown: broken={broken_count}, access_denied={access_denied_count}, "
                        f"unreachable={unreachable_count}"
                    )

            except ImportError as e:
                print(f"[WARNING] URL checker not available: {e}", file=sys.stderr)

        return self.errors

    def validate_cross_references(self) -> list[PDFValidationError]:
        """Validate cross-references (figures, tables).

        Missing figure/table caption heuristics are intentionally disabled because
        they produce frequent false positives with Quarto-generated layouts.
        """
        return self.errors

    def _parse_page_value(self, page_value: Any) -> Optional[int]:
        """Parse first integer from page label/range."""
        if page_value is None:
            return None
        matches = re.findall(r"\d+", str(page_value))
        if not matches:
            return None
        try:
            return int(matches[0])
        except ValueError:
            return None

    def _validate_chunked_pdf(
        self,
        model_id: str,
        prompt: str,
        input_rate: float,
        output_rate: float,
    ) -> tuple[list[Any], dict[str, float]]:
        """
        Split large PDF into chunks and validate each with LLM.
        Returns (all_issues, combined_usage_stats).
        """
        import fitz
        import tempfile

        chunk_size_limit = 12 * 1024 * 1024  # 12MB target (safe under 17MB limit)
        all_issues = []
        combined_usage = {
            "prompt_token_count": 0.0,
            "candidates_token_count": 0.0,
            "total_token_count": 0.0,
        }

        doc_len = len(self.doc)
        print(f"[LLM] PDF is large (>15MB). Splitting {doc_len} pages into chunks...", flush=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            chunk_files: list[tuple[Path, int]] = []

            # Split PDF into size-limited chunks
            current_chunk = fitz.open()
            current_start_page = 0
            
            # Helper to finalize current chunk
            def save_chunk(doc_chunk, start_p):
                if doc_chunk.page_count > 0:
                    c_path = temp_path / f"chunk_{len(chunk_files)}.pdf"
                    doc_chunk.save(c_path)
                    chunk_files.append((c_path, start_p))

            for i in range(doc_len):
                current_chunk.insert_pdf(self.doc, from_page=i, to_page=i)
                
                # Check size periodically (every 10 pages) or on last page
                if (i - current_start_page + 1) % 10 == 0 or i == doc_len - 1:
                    data = current_chunk.tobytes()
                    if len(data) > chunk_size_limit:
                        # If more than 1 page, backtrack one to be safe
                        if current_chunk.page_count > 1:
                            current_chunk.delete_page(-1)
                            save_chunk(current_chunk, current_start_page)
                            
                            # Start new chunk with the page we just removed
                            current_chunk = fitz.open()
                            current_chunk.insert_pdf(self.doc, from_page=i, to_page=i)
                            current_start_page = i
                        else:
                            # Single huge page, just save it
                            save_chunk(current_chunk, current_start_page)
                            current_chunk = fitz.open()
                            current_start_page = i + 1
            
            # Save any remaining pages
            save_chunk(current_chunk, current_start_page)
            
            print(f"[LLM] Split into {len(chunk_files)} chunks.", flush=True)

            # Validate each chunk
            for i, (chunk_path, start_page) in enumerate(chunk_files):
                chunk_prompt = f"Context: This is part {i+1}/{len(chunk_files)} of the document, starting at page {start_page+1}.\n\n" + prompt

                print(f"[LLM] Validating chunk {i+1}/{len(chunk_files)} (pages {start_page+1}+)...", flush=True)
                
                try:
                    response, usage = llm.generate_gemini_flash_content_with_pdf_and_usage(
                        prompt=chunk_prompt,
                        pdf_path=str(chunk_path),
                    )
                    
                    # Accumulate usage
                    for k, v in usage.items():
                        combined_usage[k] = combined_usage.get(k, 0.0) + float(v)

                    parsed = llm.extract_json_from_response(response, f"chunk {i+1}")
                    issues = parsed.get("errors", [])
                    if not isinstance(issues, list):
                        issues = parsed.get("top_issues", [])
                    if not isinstance(issues, list):
                        issues = []

                    # Adjust page numbers
                    for issue in issues:
                        page_val = issue.get("page")
                        # Try to parse integer
                        page_int = self._parse_page_value(page_val)
                        if page_int is not None:
                            # The LLM sees the chunk as starting at page 1.
                            # We need to add start_page offset.
                            issue["page"] = page_int + start_page
                        
                    all_issues.extend(issues)

                except Exception as e:
                    print(f"[LLM] Error validating chunk {i+1}: {e}", file=sys.stderr)
                    # Continue with other chunks

        return all_issues, combined_usage

    def _record_full_pdf_issues(self, issues: list[dict[str, Any]]) -> int:
        """Convert full-PDF LLM issues to validation errors."""
        for issue in issues:
            severity = str(issue.get("severity", "WARNING")).upper()
            if severity not in {
                PDFValidationError.SEVERITY_CRITICAL,
                PDFValidationError.SEVERITY_WARNING,
                PDFValidationError.SEVERITY_INFO,
            }:
                severity = PDFValidationError.SEVERITY_WARNING

            issue_type = str(issue.get("type", "OTHER")).upper().replace(" ", "_")
            page_num = self._parse_page_value(issue.get("page"))
            message = str(issue.get("description", "LLM full-PDF issue detected")).strip()
            suggested_fix = str(issue.get("suggested_fix", "")).strip()
            evidence_snippet = str(issue.get("evidence_snippet", "")).strip()
            locator_hint = str(issue.get("locator_hint", "")).strip()
            context_parts: list[str] = []
            if suggested_fix:
                context_parts.append(f"suggested_fix={suggested_fix}")
            if evidence_snippet:
                context_parts.append(f"evidence_snippet={evidence_snippet}")
            if locator_hint:
                context_parts.append(f"locator_hint={locator_hint}")
            context = " | ".join(context_parts)
            self._add_error(page_num, f"LLM_{issue_type}", severity, message, context)
        return len(issues)

    def validate_with_llm(self) -> list[PDFValidationError]:
        """Use full-PDF upload + Gemini review with cache-first behavior."""
        if self.skip_llm or not self.doc:
            return self.errors
        if not llm:
            print("[WARNING] LLM library not available, skipping LLM validation", file=sys.stderr)
            return self.errors

        model_id = self._get_llm_model_id()
        pricing = llm.get_cost_rates_per_1m(model_id=model_id)
        input_rate, output_rate, pricing_source = pricing
        print(
            f"[LLM] Full-PDF review model: {model_id}; estimated pricing USD/1M tokens "
            f"(input={input_rate}, output={output_rate}, source={pricing_source})",
            flush=True,
        )

        pdf_hash = self.current_pdf_hash or self._get_pdf_hash()
        cache_key = hashlib.sha256(
            f"{pdf_hash}|{model_id}|{LLM_FULL_PDF_PROMPT_VERSION}".encode("utf-8", errors="replace")
        ).hexdigest()
        full_pdf_cache: dict[str, Any] = {"version": 1, "entries": {}}
        if self.use_cache and self.full_pdf_llm_cache_file.exists():
            try:
                loaded = json.loads(self.full_pdf_llm_cache_file.read_text(encoding="utf-8"))
                if isinstance(loaded, dict) and isinstance(loaded.get("entries"), dict):
                    full_pdf_cache = loaded
            except Exception:
                pass
        entries = full_pdf_cache.setdefault("entries", {})

        cached = entries.get(cache_key) if self.use_cache else None
        if isinstance(cached, dict):
            cached_response = cached.get("response", {})
            cached_issues: Any = []
            if isinstance(cached_response, dict):
                cached_issues = cached_response.get("errors", [])
                if not isinstance(cached_issues, list):
                    cached_issues = cached_response.get("top_issues", [])
            if isinstance(cached_issues, list):
                issue_count = self._record_full_pdf_issues(cached_issues)
                print(
                    f"[LLM] Full-PDF cache hit key={cache_key[:12]} ({issue_count} issue(s))",
                    flush=True,
                )
                return self.errors

        prompt = LLM_FULL_PDF_PROMPT_TEXT

        # Pre-call token/cost logging
        prompt_tokens_est = llm.estimate_tokens(prompt)
        input_only_cost_est = (prompt_tokens_est / 1_000_000.0) * input_rate
        
        # Check if PDF is large enough to require splitting (e.g. >15MB)
        file_size = self.pdf_path.stat().st_size
        use_chunking = file_size > 15 * 1024 * 1024  # 15MB
        
        if not use_chunking:
            # Standard single-call path
            try:
                projected_output_tokens = max(
                    0.0,
                    float(os.getenv("PDF_VALIDATION_LLM_PROJECTED_OUTPUT_TOKENS", "1500")),
                )
            except ValueError:
                projected_output_tokens = 1500.0
            projected_total_cost_est = (
                input_only_cost_est + (projected_output_tokens / 1_000_000.0) * output_rate
            )
            print(
                f"[LLM] Preflight estimate: model={model_id}, input_tokens_est={prompt_tokens_est:.0f}, "
                f"input_cost_est_usd=${input_only_cost_est:.6f}, "
                f"projected_output_tokens={projected_output_tokens:.0f}, "
                f"projected_total_cost_est_usd=${projected_total_cost_est:.6f} "
                "(prompt-only estimate; excludes PDF document tokens)",
                flush=True,
            )

            response, usage = llm.generate_gemini_flash_content_with_pdf_and_usage(
                prompt=prompt,
                pdf_path=str(self.pdf_path),
            )
            parsed = llm.extract_json_from_response(response, f"full-pdf-review {self.pdf_path.name}")
            if not isinstance(parsed, dict):
                raise RuntimeError("Full-PDF LLM response is not a JSON object")
            issues: Any = parsed.get("errors", [])
            if not isinstance(issues, list):
                issues = parsed.get("top_issues", [])
            if not isinstance(issues, list):
                issues = []
                
        else:
            # Chunked path
            issues, usage = self._validate_chunked_pdf(model_id, prompt, input_rate, output_rate)
            # Create synthetic response for caching/cost
            parsed = {"summary": "Aggregated from chunks", "errors": issues}
            response = json.dumps(parsed)

        # Common cost accounting
        actual_input_tokens = usage.get("prompt_token_count")
        actual_output_tokens = usage.get("candidates_token_count")
        if actual_input_tokens is not None and actual_output_tokens is not None:
            cost = llm.estimate_request_cost_usd_from_tokens(
                model_id=model_id,
                input_tokens=float(actual_input_tokens),
                output_tokens=float(actual_output_tokens),
                token_source="actual",
            )
        else:
            cost = llm.estimate_request_cost_usd(
                model_id=model_id,
                prompt_text=prompt,
                response_text=response or "",
            )
        input_tokens_est = float(cost["input_tokens_est"])
        output_tokens_est = float(cost["output_tokens_est"])
        request_cost_est = float(cost["request_cost_est_usd"])
        token_source = str(cost.get("token_source", "estimated"))
        self.llm_requests_made += 1
        self.llm_input_tokens_est += input_tokens_est
        self.llm_output_tokens_est += output_tokens_est
        self.llm_cost_est_usd += request_cost_est
        print(
            f"[LLM] Full-PDF API request (total): model={model_id}, input_tokens_est={input_tokens_est:.0f}, "
            f"output_tokens_est={output_tokens_est:.0f}, token_source={token_source}, "
            f"request_cost_est_usd=${request_cost_est:.6f}",
            flush=True,
        )
        issue_count = self._record_full_pdf_issues(issues)
        print(f"[LLM] Full-PDF review complete ({issue_count} issue(s))", flush=True)

        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            response_to_cache = dict(parsed)
            if "errors" not in response_to_cache and isinstance(response_to_cache.get("top_issues"), list):
                response_to_cache["errors"] = response_to_cache["top_issues"]
            entries[cache_key] = {
                "cached_at": datetime.now().isoformat(),
                "pdf_path": str(self.pdf_path),
                "pdf_hash": pdf_hash,
                "model_id": model_id,
                "prompt_version": LLM_FULL_PDF_PROMPT_VERSION,
                "response": response_to_cache,
            }
            self.full_pdf_llm_cache_file.write_text(
                json.dumps(full_pdf_cache, indent=2),
                encoding="utf-8",
            )
            print(
                f"[LLM] Full-PDF cache saved key={cache_key[:12]} file={self.full_pdf_llm_cache_file}",
                flush=True,
            )

        return self.errors

    def validate(self) -> list[PDFValidationError]:
        """Run all validation checks."""
        pdf_hash = self._get_pdf_hash()
        self.current_pdf_hash = pdf_hash
        cache = self._load_cache()
        if self.use_cache:
            self._log_cache_paths()
            self._log_cache_inventory(pdf_cache=cache)
        else:
            print("[CACHE] Validation cache disabled (--no-cache)", flush=True)
        if self.use_cache:
            print(
                f"[*] PDF cache lookup: hash={pdf_hash[:8]}, cache_file={self.cache_file}",
                flush=True,
            )

        # Check cache if enabled
        if self.use_cache:
            cached_result = cache.get(pdf_hash)
            if cached_result is None:
                print(f"[*] PDF cache miss for {self.pdf_path.name}: no matching hash entry", flush=True)
            elif "errors" not in cached_result:
                print(
                    f"[*] PDF cache miss for {self.pdf_path.name}: malformed entry (missing errors)",
                    flush=True,
                )
            elif cached_result.get("llm_mode") != "full_pdf":
                print(
                    f"[*] PDF cache miss for {self.pdf_path.name}: llm_mode mismatch "
                    f"(cached={cached_result.get('llm_mode')}, requested=full_pdf)",
                    flush=True,
                )
            else:
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
                "llm_mode": "full_pdf",
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
