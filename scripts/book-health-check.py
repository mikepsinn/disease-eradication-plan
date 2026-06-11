#!/usr/bin/env python3
"""
Book Health Check - Unified Quality Dashboard

Runs all quality checks on the book and generates a prioritized task list.
Integrates with existing hash tracking system to identify stale reviews.

Usage:
    python scripts/book-health-check.py                    # Full check
    python scripts/book-health-check.py --quick            # Fast checks only
    python scripts/book-health-check.py --chapter index    # Single chapter
    python scripts/book-health-check.py --changed-only     # Only recently changed files
    python scripts/book-health-check.py --with-llm         # Include LLM analysis
    python scripts/book-health-check.py --output report.md # Custom output

Output:
    _build_temp/book-health-report.md - AI-actionable task list
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')  # pyright: ignore[reportAttributeAccessIssue]

PROJECT_ROOT = Path(__file__).parent.parent
BUILD_TEMP = PROJECT_ROOT / "_build_temp"
VARIABLES_FILE = PROJECT_ROOT / "_variables.yml"
HASH_STORE_FILE = PROJECT_ROOT / ".file-hashes.json"

# Hash field names (from scripts/lib/constants.ts)
HASH_FIELDS = {
    "FORMATTED": "lastFormattedHash",
    "FACT_CHECK": "lastFactCheckHash",
    "STRUCTURE_CHECK": "lastStructureCheckHash",
    "LINK_CHECK": "lastLinkCheckHash",
    "FIGURE_CHECK": "lastFigureCheckHash",
    "LATEX_CHECK": "lastLatexCheckHash",
    "PARAM_CHECK": "lastParamCheckHash",
    "CONSISTENCY_CHECK": "lastConsistencyCheckHash",
}


class HealthIssue:
    """Represents a single health issue found in the book."""

    PRIORITY_CRITICAL = "CRITICAL"
    PRIORITY_HIGH = "HIGH"
    PRIORITY_MEDIUM = "MEDIUM"
    PRIORITY_LOW = "LOW"

    def __init__(
        self,
        file_path: str,
        category: str,
        priority: str,
        title: str,
        description: str,
        fix_instruction: str,
        line_number: Optional[int] = None,
        context: str = "",
    ):
        self.file_path = file_path
        self.category = category
        self.priority = priority
        self.title = title
        self.description = description
        self.fix_instruction = fix_instruction
        self.line_number = line_number
        self.context = context

    def to_dict(self):
        return {
            "file": self.file_path,
            "category": self.category,
            "priority": self.priority,
            "title": self.title,
            "description": self.description,
            "fix": self.fix_instruction,
            "line": self.line_number,
            "context": self.context,
        }


class BookHealthChecker:
    """Comprehensive book health checker."""

    def __init__(
        self,
        quick_mode: bool = False,
        target_chapter: Optional[str] = None,
        changed_only: bool = False,
        with_llm: bool = False,
    ):
        self.quick_mode = quick_mode
        self.target_chapter = target_chapter
        self.changed_only = changed_only
        self.with_llm = with_llm
        self.issues: list[HealthIssue] = []
        self.stats = defaultdict(int)
        self.hash_store = self._load_hash_store()

    def _load_hash_store(self) -> dict:
        """Load the hash store from .file-hashes.json."""
        if not HASH_STORE_FILE.exists():
            return {}
        try:
            return json.loads(HASH_STORE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _get_content_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        content = file_path.read_text(encoding="utf-8")
        return hashlib.md5(content.encode()).hexdigest()

    def _get_file_review_status(self, file_path: Path) -> dict:
        """Get review status for a file from hash store."""
        rel_path = str(file_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        return self.hash_store.get(rel_path, {})

    def _is_file_changed_since_review(self, file_path: Path, hash_field: str) -> bool:
        """Check if file content has changed since last review."""
        review_status = self._get_file_review_status(file_path)
        stored_hash = review_status.get(hash_field)
        if not stored_hash:
            return True  # Never reviewed
        current_hash = self._get_content_hash(file_path)
        return current_hash != stored_hash

    def get_qmd_files(self) -> list[Path]:
        """Get all QMD files to check."""
        patterns = [
            "index*.qmd",
            "knowledge/**/*.qmd",
        ]

        files = []
        for pattern in patterns:
            files.extend(PROJECT_ROOT.glob(pattern))

        # Filter to target chapter if specified
        if self.target_chapter:
            files = [f for f in files if self.target_chapter in f.stem]

        # Exclude generated files
        files = [f for f in files if "parameters-and-calculations" not in f.name]

        # Filter to changed files only if requested
        if self.changed_only:
            files = [f for f in files if self._has_any_stale_review(f)]

        return sorted(files)

    def _has_any_stale_review(self, file_path: Path) -> bool:
        """Check if any review type is stale (content changed since last review)."""
        for hash_field in HASH_FIELDS.values():
            if self._is_file_changed_since_review(file_path, hash_field):
                return True
        return False

    def check_stale_reviews(self, file_path: Path) -> list[HealthIssue]:
        """Check which reviews are stale for this file."""
        issues = []
        review_status = self._get_file_review_status(file_path)

        stale_reviews = []
        for name, hash_field in HASH_FIELDS.items():
            if self._is_file_changed_since_review(file_path, hash_field):
                stale_reviews.append(name)

        if stale_reviews:
            # Only report if more than half of reviews are stale
            if len(stale_reviews) >= len(HASH_FIELDS) // 2:
                issues.append(HealthIssue(
                    file_path=str(file_path.relative_to(PROJECT_ROOT)),
                    category="STALE_REVIEWS",
                    priority=HealthIssue.PRIORITY_LOW,
                    title=f"{len(stale_reviews)} reviews need refresh",
                    description=f"Stale: {', '.join(stale_reviews[:5])}{'...' if len(stale_reviews) > 5 else ''}",
                    fix_instruction="Run /peer-review or individual review scripts to update hashes.",
                ))

        return issues

    def check_with_llm(self, file_path: Path) -> list[HealthIssue]:
        """Use LLM to check for redundancy and language issues."""
        if self.quick_mode or not self.with_llm:
            return []

        issues = []

        try:
            # Import LLM functions
            sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "lib"))
            from llm import generate_gemini_flash_content, extract_json_from_response
        except ImportError:
            print("  [WARN] LLM library not available, skipping LLM checks")
            return []

        content = file_path.read_text(encoding="utf-8")

        # Skip very long files (token limits)
        if len(content) > 50000:
            return []

        prompt = f"""Analyze this QMD file for quality issues. Return JSON only.

FILE CONTENT:
{content[:30000]}

Check for:
1. REDUNDANCY: Repeated sentences, similar paragraphs saying the same thing
2. WORDINESS: Sentences that could be simplified (target 8th grade reading level)
3. OVERCLAIMS: Statements that are too strong without evidence

Return JSON:
{{
  "issues": [
    {{
      "type": "REDUNDANCY|WORDINESS|OVERCLAIM",
      "severity": "HIGH|MEDIUM|LOW",
      "description": "brief description",
      "location": "approximate location or quote",
      "suggestion": "how to fix"
    }}
  ],
  "summary": "1-2 sentence overall assessment"
}}

Only report significant issues. Return empty issues array if file is good.
"""

        try:
            response = generate_gemini_flash_content(prompt)
            result = extract_json_from_response(response)

            for issue in result.get("issues", []):
                severity_map = {
                    "HIGH": HealthIssue.PRIORITY_MEDIUM,
                    "MEDIUM": HealthIssue.PRIORITY_LOW,
                    "LOW": HealthIssue.PRIORITY_LOW,
                }
                issues.append(HealthIssue(
                    file_path=str(file_path.relative_to(PROJECT_ROOT)),
                    category=f"LLM_{issue.get('type', 'UNKNOWN')}",
                    priority=severity_map.get(issue.get("severity", "LOW"), HealthIssue.PRIORITY_LOW),
                    title=issue.get("description", "LLM-detected issue")[:80],
                    description=issue.get("suggestion", "Review and fix"),
                    fix_instruction="Review the flagged content and simplify/consolidate as needed.",
                    context=issue.get("location", "")[:100],
                ))

        except Exception as e:
            print(f"  [WARN] LLM check failed: {e}")

        return issues

    def check_hardcoded_values(self, file_path: Path) -> list[HealthIssue]:
        """Check for hardcoded numbers that should be variables."""
        issues = []
        content = file_path.read_text(encoding="utf-8")

        # Simpler patterns that don't use variable-width lookbehinds
        patterns = [
            # Dollar amounts (will filter out those in variables later)
            (r'\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|trillion|M|B|T))?',
             "Hardcoded dollar amount"),
            # Large numbers with commas (>1,000)
            (r'\b(\d{1,3}(?:,\d{3})+)\b',
             "Hardcoded large number"),
            # Percentages over 10%
            (r'\b(\d{2,})(?:\.\d+)?\s*%',
             "Potential hardcoded percentage"),
        ]

        lines = content.split("\n")
        in_code_block = False
        for i, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Skip cell options, comments, and lines with variables
            if line.strip().startswith("#|") or "{{< var" in line:
                continue

            for pattern, desc in patterns:
                matches = re.findall(pattern, line)
                if matches:
                    # Only flag significant values
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0]
                        # Skip small numbers and common non-variable values
                        try:
                            num = float(match.replace(",", "").replace("$", "").replace("%", ""))
                            if num < 100 and "%" not in match and "$" not in match:
                                continue
                        except ValueError:
                            pass

                        issues.append(HealthIssue(
                            file_path=str(file_path.relative_to(PROJECT_ROOT)),
                            category="HARDCODED_VALUE",
                            priority=HealthIssue.PRIORITY_MEDIUM,
                            title=f"{desc}: {match}",
                            description=f"Found '{match}' which may need to be a variable",
                            fix_instruction="Check if this value exists in _variables.yml. If not, add it to parameters.py and regenerate.",
                            line_number=i,
                            context=line.strip()[:100],
                        ))
                        break  # One issue per line

        return issues

    def check_broken_internal_links(self, file_path: Path) -> list[HealthIssue]:
        """Check for broken internal links to .qmd files."""
        issues = []
        content = file_path.read_text(encoding="utf-8")

        # Find all internal .qmd links
        link_pattern = r'\[([^\]]*)\]\(([^)]*\.qmd(?:#[^)]*)?)\)'
        matches = re.findall(link_pattern, content)

        for link_text, link_target in matches:
            # Extract just the file path (without anchor)
            file_part = link_target.split("#")[0]

            # Resolve relative path
            if file_part.startswith("/"):
                target_path = PROJECT_ROOT / file_part.lstrip("/")
            else:
                target_path = file_path.parent / file_part

            target_path = target_path.resolve()

            if not target_path.exists():
                issues.append(HealthIssue(
                    file_path=str(file_path.relative_to(PROJECT_ROOT)),
                    category="BROKEN_LINK",
                    priority=HealthIssue.PRIORITY_HIGH,
                    title=f"Broken link to: {file_part}",
                    description=f"Link target does not exist: {link_target}",
                    fix_instruction="Update the link to point to an existing file, or remove the link.",
                    context=f"[{link_text}]({link_target})",
                ))

        return issues

    def check_missing_citations(self, file_path: Path) -> list[HealthIssue]:
        """Check for citation references that don't exist in references.bib."""
        issues = []
        content = file_path.read_text(encoding="utf-8")

        # Load references.bib keys
        bib_path = PROJECT_ROOT / "references.bib"
        if not bib_path.exists():
            return issues

        bib_content = bib_path.read_text(encoding="utf-8")
        bib_keys = set(re.findall(r'@\w+\{([^,]+),', bib_content))

        # Find all citation references
        citation_pattern = r'@([a-zA-Z0-9_-]+)'
        matches = re.findall(citation_pattern, content)

        for cite_key in set(matches):
            if cite_key not in bib_keys:
                issues.append(HealthIssue(
                    file_path=str(file_path.relative_to(PROJECT_ROOT)),
                    category="MISSING_CITATION",
                    priority=HealthIssue.PRIORITY_HIGH,
                    title=f"Missing citation: @{cite_key}",
                    description=f"Citation key '{cite_key}' not found in references.bib",
                    fix_instruction="Add the citation to references.bib or fix the citation key.",
                ))

        return issues

    def check_unrendered_variables(self, file_path: Path) -> list[HealthIssue]:
        """Check for potential unrendered variable syntax."""
        issues = []
        content = file_path.read_text(encoding="utf-8")

        # Check for variables that reference non-existent keys
        if not VARIABLES_FILE.exists():
            return issues

        variables_content = VARIABLES_FILE.read_text(encoding="utf-8")

        # Find all variable references
        var_pattern = r'\{\{<\s*var\s+([a-zA-Z0-9_]+)\s*>\}\}'
        matches = re.findall(var_pattern, content)

        for var_name in set(matches):
            if f"{var_name}:" not in variables_content:
                issues.append(HealthIssue(
                    file_path=str(file_path.relative_to(PROJECT_ROOT)),
                    category="MISSING_VARIABLE",
                    priority=HealthIssue.PRIORITY_CRITICAL,
                    title=f"Missing variable: {var_name}",
                    description=f"Variable '{var_name}' referenced but not in _variables.yml",
                    fix_instruction="Add the variable to parameters.py and run generate script, or fix the variable name.",
                ))

        return issues

    def check_stale_content(self, file_path: Path) -> list[HealthIssue]:
        """Check for potentially stale content based on modification date."""
        issues = []

        # Get file modification time
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        age_days = (datetime.now() - mtime).days

        # Flag files older than 30 days that haven't been reviewed
        if age_days > 30:
            issues.append(HealthIssue(
                file_path=str(file_path.relative_to(PROJECT_ROOT)),
                category="STALE_CONTENT",
                priority=HealthIssue.PRIORITY_LOW,
                title=f"File not updated in {age_days} days",
                description=f"Last modified: {mtime.strftime('%Y-%m-%d')}",
                fix_instruction="Review this file for outdated information, statistics, or links.",
            ))

        return issues

    def check_missing_images(self, file_path: Path) -> list[HealthIssue]:
        """Check for image references that don't exist."""
        issues = []
        content = file_path.read_text(encoding="utf-8")

        # Find image references
        img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(img_pattern, content)

        for alt_text, img_path in matches:
            # Skip external URLs
            if img_path.startswith("http"):
                continue

            # Resolve path
            if img_path.startswith("/"):
                target_path = PROJECT_ROOT / img_path.lstrip("/")
            else:
                target_path = file_path.parent / img_path

            if not target_path.exists():
                issues.append(HealthIssue(
                    file_path=str(file_path.relative_to(PROJECT_ROOT)),
                    category="MISSING_IMAGE",
                    priority=HealthIssue.PRIORITY_HIGH,
                    title=f"Missing image: {img_path}",
                    description=f"Image file does not exist",
                    fix_instruction="Generate the image using /generate-image or /generate-section-images, or fix the path.",
                ))

        return issues

    def check_long_sentences(self, file_path: Path) -> list[HealthIssue]:
        """Check for overly long sentences (readability)."""
        if self.quick_mode:
            return []

        issues = []
        content = file_path.read_text(encoding="utf-8")

        # Skip code blocks and frontmatter
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'^---[\s\S]*?---', '', content)

        # Find sentences
        sentences = re.split(r'[.!?]+', content)
        long_count = 0

        for sentence in sentences:
            words = sentence.split()
            if len(words) > 40:  # Very long sentence
                long_count += 1

        if long_count > 5:
            issues.append(HealthIssue(
                file_path=str(file_path.relative_to(PROJECT_ROOT)),
                category="READABILITY",
                priority=HealthIssue.PRIORITY_LOW,
                title=f"{long_count} sentences over 40 words",
                description="Multiple very long sentences may hurt readability",
                fix_instruction="Consider breaking long sentences into shorter ones (target: 10-15 words average).",
            ))

        return issues

    def run_all_checks(self) -> list[HealthIssue]:
        """Run all health checks on the book."""
        print("[*] Starting book health check...")

        qmd_files = self.get_qmd_files()
        print(f"[*] Found {len(qmd_files)} QMD files to check")

        checks = [
            ("Hardcoded values", self.check_hardcoded_values),
            ("Broken links", self.check_broken_internal_links),
            ("Missing citations", self.check_missing_citations),
            ("Missing variables", self.check_unrendered_variables),
            ("Missing images", self.check_missing_images),
            ("Stale content", self.check_stale_content),
            ("Stale reviews", self.check_stale_reviews),
            ("Readability", self.check_long_sentences),
            ("LLM analysis", self.check_with_llm),
        ]

        for file_path in qmd_files:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            print(f"  Checking: {rel_path}")

            for check_name, check_fn in checks:
                try:
                    issues = check_fn(file_path)
                    self.issues.extend(issues)
                    self.stats[check_name] += len(issues)
                except Exception as e:
                    print(f"    [WARN] {check_name} failed: {e}")

        print(f"\n[*] Found {len(self.issues)} total issues")
        return self.issues

    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """Generate a markdown report of all issues."""
        if output_path is None:
            output_path = BUILD_TEMP / "book-health-report.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Group by priority, then by file
        by_priority = defaultdict(lambda: defaultdict(list))
        for issue in self.issues:
            by_priority[issue.priority][issue.file_path].append(issue)

        lines = [
            "# Book Health Report",
            "",
            f"**Generated:** {datetime.now().isoformat()}",
            f"**Total Issues:** {len(self.issues)}",
            "",
            "## Summary by Category",
            "",
            "| Category | Count |",
            "|----------|-------|",
        ]

        for category, count in sorted(self.stats.items(), key=lambda x: -x[1]):
            lines.append(f"| {category} | {count} |")

        lines.extend(["", "---", ""])

        priority_order = [
            HealthIssue.PRIORITY_CRITICAL,
            HealthIssue.PRIORITY_HIGH,
            HealthIssue.PRIORITY_MEDIUM,
            HealthIssue.PRIORITY_LOW,
        ]

        priority_emoji = {
            HealthIssue.PRIORITY_CRITICAL: "🔴",
            HealthIssue.PRIORITY_HIGH: "🟠",
            HealthIssue.PRIORITY_MEDIUM: "🟡",
            HealthIssue.PRIORITY_LOW: "⚪",
        }

        for priority in priority_order:
            if priority not in by_priority:
                continue

            emoji = priority_emoji.get(priority, "")
            lines.append(f"## {emoji} {priority} Priority Issues")
            lines.append("")

            for file_path, issues in sorted(by_priority[priority].items()):
                lines.append(f"### `{file_path}`")
                lines.append("")

                for issue in issues:
                    lines.append(f"- **{issue.category}**: {issue.title}")
                    if issue.line_number:
                        lines.append(f"  - Line: {issue.line_number}")
                    lines.append(f"  - {issue.description}")
                    lines.append(f"  - **Fix:** {issue.fix_instruction}")
                    if issue.context:
                        lines.append(f"  - Context: `{issue.context[:80]}...`")
                    lines.append("")

        # Add AI instructions
        lines.extend([
            "---",
            "",
            "## AI Instructions",
            "",
            "To fix these issues systematically:",
            "",
            "1. **CRITICAL issues** must be fixed before rendering",
            "2. **HIGH priority** issues affect publication quality",
            "3. **MEDIUM priority** issues improve consistency",
            "4. **LOW priority** can be addressed opportunistically",
            "",
            "For each file with issues, use the appropriate skill:",
            "- Hardcoded values: `/replace-hardcoded-values`",
            "- Missing citations: `/verify-and-add-sources`",
            "- Missing variables: `/validate-and-regenerate-parameters`",
            "- Readability: `/peer-review`",
            "",
        ])

        report = "\n".join(lines)
        output_path.write_text(report, encoding="utf-8")

        return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="Book Health Check")
    parser.add_argument("--quick", action="store_true", help="Skip slow checks")
    parser.add_argument("--chapter", help="Check single chapter by name")
    parser.add_argument("--changed-only", action="store_true", help="Only check files with stale reviews")
    parser.add_argument("--with-llm", action="store_true", help="Include LLM analysis for redundancy/language")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    checker = BookHealthChecker(
        quick_mode=args.quick,
        target_chapter=args.chapter,
        changed_only=args.changed_only,
        with_llm=args.with_llm,
    )

    issues = checker.run_all_checks()

    if args.json:
        output = {
            "generated": datetime.now().isoformat(),
            "total_issues": len(issues),
            "stats": dict(checker.stats),
            "issues": [i.to_dict() for i in issues],
        }
        print(json.dumps(output, indent=2))
    else:
        report_path = checker.generate_report(
            Path(args.output) if args.output else None
        )
        print(f"\n[OK] Report written to: {report_path}")

        # Summary
        print("\nSummary:")
        print(f"  CRITICAL: {sum(1 for i in issues if i.priority == HealthIssue.PRIORITY_CRITICAL)}")
        print(f"  HIGH:     {sum(1 for i in issues if i.priority == HealthIssue.PRIORITY_HIGH)}")
        print(f"  MEDIUM:   {sum(1 for i in issues if i.priority == HealthIssue.PRIORITY_MEDIUM)}")
        print(f"  LOW:      {sum(1 for i in issues if i.priority == HealthIssue.PRIORITY_LOW)}")

    return 0 if not any(i.priority == HealthIssue.PRIORITY_CRITICAL for i in issues) else 1


if __name__ == "__main__":
    sys.exit(main())
