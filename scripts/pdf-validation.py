#!/usr/bin/env python3
"""
PDF Validation Script for Mass Publication Readiness

Comprehensive validator combining programmatic checks with optional LLM-powered
quality analysis.

Usage:
    python scripts/pdf-validation.py
    python scripts/pdf-validation.py --pdf assets/pdfs/my-paper.pdf
    python scripts/pdf-validation.py --skip-llm --skip-url-check
    python scripts/pdf-validation.py --llm-pages 10
    python scripts/pdf-validation.py --fail-on-warning

Exit codes:
    0 - All checks passed (or only warnings)
    1 - Critical errors found
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

# Detect GitHub Actions environment
IN_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
GITHUB_STEP_SUMMARY = os.environ.get("GITHUB_STEP_SUMMARY")


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


class PDFValidator:
    """Comprehensive PDF validator for publication readiness."""

    def __init__(
        self,
        pdf_path: str,
        skip_llm: bool = False,
        skip_url_check: bool = False,
        llm_sample_pages: int = 5,
    ):
        self.pdf_path = pdf_path
        self.skip_llm = skip_llm
        self.skip_url_check = skip_url_check
        self.llm_sample_pages = llm_sample_pages
        self.doc = None
        self.errors: list[PDFValidationError] = []

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
                self.pdf_path, page_num, error_type, severity, message, context
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

        # Check for blank pages
        for page_num in range(page_count):
            page = self.doc[page_num]
            text = page.get_text()
            if len(text.strip()) < 50:
                self._add_error(
                    page_num + 1,  # 1-indexed for human readability
                    "BLANK_PAGE",
                    PDFValidationError.SEVERITY_WARNING,
                    f"Page {page_num + 1} appears blank or has very little content",
                    f"Text length: {len(text.strip())} chars",
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

        # Check file size
        file_size = os.path.getsize(self.pdf_path)
        if file_size < 100 * 1024:  # < 100KB
            self._add_error(
                None,
                "SMALL_FILE",
                PDFValidationError.SEVERITY_WARNING,
                f"PDF file is suspiciously small ({file_size / 1024:.1f}KB)",
            )
        elif file_size > 500 * 1024 * 1024:  # > 500MB
            self._add_error(
                None,
                "LARGE_FILE",
                PDFValidationError.SEVERITY_WARNING,
                f"PDF file is very large ({file_size / (1024 * 1024):.1f}MB)",
            )

        return self.errors

    def validate_content(self) -> list[PDFValidationError]:
        """Validate content patterns for rendering issues."""
        if not self.doc:
            return self.errors

        page_count = len(self.doc)
        for page_num in range(page_count):
            page = self.doc[page_num]
            text = page.get_text()

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

            for img_index, img in enumerate(images):
                xref = img[0]
                try:
                    img_data = self.doc.extract_image(xref)
                    width = img_data.get("width", 0)
                    height = img_data.get("height", 0)

                    if width < 10 or height < 10:
                        self._add_error(
                            page_num + 1,
                            "TINY_IMAGE",
                            PDFValidationError.SEVERITY_WARNING,
                            f"Tiny image found ({width}x{height}px)",
                        )
                except Exception:
                    # Image extraction failed - might be a format issue
                    pass

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

        import urllib.request
        from urllib.error import HTTPError, URLError

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
        if not self.skip_url_check:
            for url in list(external_urls)[:50]:  # Limit to 50 URLs
                try:
                    req = urllib.request.Request(
                        url, method="HEAD", headers={"User-Agent": "PDF-Validator/1.0"}
                    )
                    urllib.request.urlopen(req, timeout=5)
                except HTTPError as e:
                    if e.code >= 400:
                        self._add_error(
                            None,
                            "BROKEN_EXTERNAL_LINK",
                            PDFValidationError.SEVERITY_CRITICAL,
                            f"HTTP {e.code} for URL: {url}",
                        )
                except URLError:
                    self._add_error(
                        None,
                        "BROKEN_EXTERNAL_LINK",
                        PDFValidationError.SEVERITY_CRITICAL,
                        f"Cannot reach URL: {url}",
                    )
                except Exception:
                    pass  # Timeout or other issues - don't flag

        return self.errors

    def validate_cross_references(self) -> list[PDFValidationError]:
        """Validate cross-references (figures, tables)."""
        if not self.doc:
            return self.errors

        full_text = ""
        for page_num in range(len(self.doc)):
            full_text += self.doc[page_num].get_text() + "\n"

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

        try:
            # Import LLM functions - need to handle encoding conflict
            sys.path.insert(0, str(Path(__file__).parent / "lib"))

            # Temporarily restore original stdout/stderr for llm.py import
            # (it tries to reconfigure encoding which conflicts with codecs wrapper)
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            if hasattr(sys, '__stdout__') and sys.__stdout__:
                sys.stdout = sys.__stdout__
            if hasattr(sys, '__stderr__') and sys.__stderr__:
                sys.stderr = sys.__stderr__

            try:
                from llm import generate_gemini_flash_content, extract_json_from_response
            finally:
                sys.stdout = original_stdout
                sys.stderr = original_stderr

        except ImportError as e:
            print(f"[WARNING] LLM validation skipped: {e}", file=sys.stderr)
            return self.errors
        except (ValueError, AttributeError) as e:
            # API key not set or encoding conflict
            print(f"[WARNING] LLM validation skipped: {e}", file=sys.stderr)
            return self.errors

        page_count = len(self.doc)

        # Sample pages evenly distributed
        if page_count <= self.llm_sample_pages:
            sample_indices = list(range(page_count))
        else:
            step = page_count / self.llm_sample_pages
            sample_indices = [int(i * step) for i in range(self.llm_sample_pages)]

        for page_idx in sample_indices:
            page = self.doc[page_idx]
            text = page.get_text()

            # Skip very short pages
            if len(text.strip()) < 100:
                continue

            # Truncate long pages
            if len(text) > 8000:
                text = text[:8000] + "\n[...truncated...]"

            prompt = f"""Analyze this PDF page content for quality issues. Check for:
1. Rendering artifacts or garbled text
2. Sentences cut off mid-word
3. Malformed tables (misaligned columns)
4. Figure/table captions without corresponding content
5. Placeholder text (TODO, FIXME, Lorem ipsum, TBD)
6. Obviously wrong values ($undefined, NaN, None, [object Object])
7. Code or error messages that shouldn't be visible

Page {page_idx + 1} content:
---
{text}
---

Respond with JSON only:
{{
    "issues": [
        {{"type": "string", "description": "string", "severity": "CRITICAL|WARNING|INFO"}}
    ],
    "page_quality": "good|acceptable|poor"
}}

If no issues found, return {{"issues": [], "page_quality": "good"}}"""

            try:
                response = generate_gemini_flash_content(prompt)
                result = extract_json_from_response(response, f"LLM page {page_idx + 1}")

                for issue in result.get("issues", []):
                    severity_map = {
                        "CRITICAL": PDFValidationError.SEVERITY_CRITICAL,
                        "WARNING": PDFValidationError.SEVERITY_WARNING,
                        "INFO": PDFValidationError.SEVERITY_INFO,
                    }
                    severity = severity_map.get(
                        issue.get("severity", "WARNING"),
                        PDFValidationError.SEVERITY_WARNING,
                    )

                    self._add_error(
                        page_idx + 1,
                        f"LLM_{issue.get('type', 'UNKNOWN').upper().replace(' ', '_')}",
                        severity,
                        issue.get("description", "LLM-detected issue"),
                    )

            except Exception as e:
                print(
                    f"[WARNING] LLM validation failed for page {page_idx + 1}: {e}",
                    file=sys.stderr,
                )

        return self.errors

    def validate(self) -> list[PDFValidationError]:
        """Run all validation checks."""
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
    parser.add_argument(
        "--output-dir",
        default="_manual/warondisease",
        help="Directory to search for PDF files",
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
    args = parser.parse_args()

    # Determine PDF files to validate
    if args.pdf:
        pdf_files = [Path(args.pdf)]
        if not pdf_files[0].exists():
            print(f"[ERROR] PDF file not found: {args.pdf}")
            return 1
    else:
        output_dir = Path(args.output_dir)
        if not output_dir.exists():
            print(f"[ERROR] Output directory not found: {output_dir}")
            return 1
        pdf_files = find_pdf_files(output_dir)
        if not pdf_files:
            print(f"[WARNING] No PDF files found in {output_dir}")
            return 0

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

    # Determine exit code
    if has_critical:
        return 1
    if args.fail_on_warning and warning_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
