#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autonomous Fix and PR Creator

Orchestrates the auto-fix workflow:
1. Fetch issue details from GitHub
2. Parse validation errors from issue body
3. Route to appropriate fix tier (deterministic → WISHONIA → complex LLM)
4. Apply fixes with validation gates
5. Create PR if all validations pass
6. Rollback on failure

Usage:
    python scripts/autonomous-fix-and-pr.py --issue 123
    python scripts/autonomous-fix-and-pr.py --issue 123 --budget 5.0 --dry-run

Safety:
    - Pre-fix validation: Verify error exists
    - Post-fix validation: Re-run validators
    - Budget limits: $5/run, $0.50/paper, $0.25/fix
    - Git rollback on any failure
    - Always creates PR (never auto-merges)
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set UTF-8 for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "AUTONOMOUS-FIX-LOGS"
RESULT_FILE = PROJECT_ROOT / "auto-fix-result.json"


class AutoFixOrchestrator:
    def __init__(
        self,
        issue_number: int,
        budget_total: float = 5.0,
        budget_per_paper: float = 0.50,
        budget_per_fix: float = 0.25,
        dry_run: bool = False
    ):
        self.issue_number = issue_number
        self.budget_total = budget_total
        self.budget_per_paper = budget_per_paper
        self.budget_per_fix = budget_per_fix
        self.dry_run = dry_run

        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = LOG_DIR / self.run_id
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.cost_tracker = {
            "tier1": 0.0,
            "tier2": 0.0,
            "tier3": 0.0,
            "total": 0.0
        }

        print(f"[ORCHESTRATOR] Initialized for issue #{issue_number}")
        print(f"[ORCHESTRATOR] Budget: ${budget_total} total, ${budget_per_fix}/fix")
        print(f"[ORCHESTRATOR] Log directory: {self.log_dir}")
        if dry_run:
            print("[ORCHESTRATOR] DRY RUN MODE - no changes will be made")

    def fetch_issue(self) -> Dict:
        """Fetch issue details from GitHub using gh CLI"""
        print(f"\n[STEP 1] Fetching issue #{self.issue_number}...")

        try:
            result = subprocess.run(
                ["gh", "issue", "view", str(self.issue_number), "--json",
                 "title,body,labels,state"],
                capture_output=True,
                text=True,
                check=True
            )

            issue = json.loads(result.stdout)
            print(f"[ISSUE] Title: {issue['title']}")
            print(f"[ISSUE] State: {issue['state']}")
            print(f"[ISSUE] Labels: {', '.join(l['name'] for l in issue['labels'])}")

            # Save issue to log
            with open(self.log_dir / "issue.json", "w", encoding="utf-8") as f:
                json.dump(issue, f, indent=2)

            return issue

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to fetch issue: {e.stderr}", file=sys.stderr)
            raise
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse issue JSON: {e}", file=sys.stderr)
            raise

    def parse_errors_from_issue(self, issue: Dict) -> List[Dict]:
        """Parse validation errors from issue body"""
        print("\n[STEP 2] Parsing errors from issue body...")

        body = issue.get("body", "")

        # For now, use a simple extraction from the structured issue body
        # In production, this would parse the markdown structure more robustly
        errors = []

        # Extract paper, error type from title
        # Format: "[Validation] paper-name: ERROR_TYPE (N occurrences)"
        title = issue.get("title", "")
        import re
        match = re.match(r'\[Validation\]\s+([^:]+):\s+([^\(]+)', title)

        if match:
            paper = match.group(1).strip()
            error_type = match.group(2).strip()

            # Create error object from issue metadata
            error = {
                "source": self._extract_source_from_labels(issue.get("labels", [])),
                "paper": paper,
                "type": error_type,
                "severity": self._extract_severity_from_labels(issue.get("labels", [])),
                "message": f"Validation error: {error_type}",
                "issue_body": body
            }

            errors.append(error)
            print(f"[PARSED] {len(errors)} error(s) from issue")
        else:
            print("[WARNING] Could not parse error from issue title")

        # Save errors to log
        with open(self.log_dir / "errors.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, indent=2)

        return errors

    def _extract_source_from_labels(self, labels: List[Dict]) -> str:
        """Extract validation source from labels"""
        for label in labels:
            name = label.get("name", "")
            if name.startswith("validation:"):
                source = name.replace("validation:", "")
                if source in ["pdf", "pre-render", "post-render", "build"]:
                    return source
        return "unknown"

    def _extract_severity_from_labels(self, labels: List[Dict]) -> str:
        """Extract severity from labels"""
        for label in labels:
            name = label.get("name", "")
            if name in ["validation:critical", "validation:warning", "validation:info"]:
                return name.replace("validation:", "").upper()
        return "WARNING"

    def classify_and_route(self, errors: List[Dict]) -> Dict:
        """Classify errors and route to appropriate fix tier"""
        print("\n[STEP 3] Classifying errors and routing to fix tiers...")

        # Call TypeScript error router via npx tsx
        errors_json = json.dumps(errors)

        try:
            result = subprocess.run(
                ["npx", "tsx", "scripts/agents/sub-agents/error-router.ts"],
                input=errors_json,
                capture_output=True,
                text=True,
                check=True,
                cwd=PROJECT_ROOT
            )

            classification = json.loads(result.stdout)

            print(f"[ROUTING] Tier 1 (deterministic): {len(classification.get('tier1', []))}")
            print(f"[ROUTING] Tier 2 (WISHONIA): {len(classification.get('tier2', []))}")
            print(f"[ROUTING] Tier 3 (complex LLM): {len(classification.get('tier3', []))}")
            print(f"[ROUTING] Manual review: {len(classification.get('manual', []))}")
            print(f"[ROUTING] Estimated cost: ${classification.get('totalEstimatedCost', 0):.2f}")

            # Check budget
            if classification.get("totalEstimatedCost", 0) > self.budget_total:
                print(f"[ERROR] Estimated cost exceeds budget: ${classification['totalEstimatedCost']:.2f} > ${self.budget_total}", file=sys.stderr)
                raise RuntimeError("Budget exceeded")

            # Save classification
            with open(self.log_dir / "classification.json", "w", encoding="utf-8") as f:
                json.dump(classification, f, indent=2)

            return classification

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Classification failed: {e.stderr}", file=sys.stderr)
            raise
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse classification JSON: {e}", file=sys.stderr)
            raise

    def apply_fixes(self, classification: Dict) -> Dict:
        """Apply fixes using appropriate tier agents"""
        print("\n[STEP 4] Applying fixes...")

        if self.dry_run:
            print("[DRY RUN] Skipping actual fix application")
            return {
                "success": True,
                "tier1_fixed": len(classification.get("tier1", [])),
                "tier2_fixed": 0,
                "tier3_fixed": 0,
                "files_modified": []
            }

        # TODO: Call TypeScript auto-fix workflow
        # For now, just stub the interface
        print("[TODO] Auto-fix workflow not yet implemented")
        print("[INFO] In production, this would:")
        print("  1. Create git feature branch")
        print("  2. Apply Tier 1 fixes (deterministic)")
        print("  3. Apply Tier 2 fixes (WISHONIA agents)")
        print("  4. Apply Tier 3 fixes (complex LLM)")
        print("  5. Validate all changes")
        print("  6. Commit incrementally")

        return {
            "success": False,
            "message": "Auto-fix workflow not yet implemented",
            "files_modified": []
        }

    def create_pr(self, fix_result: Dict) -> Optional[str]:
        """Create pull request with fixes"""
        print("\n[STEP 5] Creating pull request...")

        if self.dry_run:
            print("[DRY RUN] Skipping PR creation")
            return "https://github.com/example/repo/pull/999"

        if not fix_result.get("success"):
            print("[SKIP] No fixes applied - skipping PR creation")
            return None

        # TODO: Implement PR creation via git-operations.ts
        print("[TODO] PR creation not yet implemented")

        return None

    def run(self) -> Dict:
        """Main orchestration flow"""
        start_time = datetime.now()

        try:
            # Step 1: Fetch issue
            issue = self.fetch_issue()

            # Step 2: Parse errors
            errors = self.parse_errors_from_issue(issue)

            if not errors:
                return {
                    "success": False,
                    "message": "No errors found in issue",
                    "issue_number": self.issue_number
                }

            # Step 3: Classify and route
            classification = self.classify_and_route(errors)

            # Step 4: Apply fixes
            fix_result = self.apply_fixes(classification)

            # Step 5: Create PR
            pr_url = self.create_pr(fix_result)

            # Calculate duration and cost
            duration = (datetime.now() - start_time).total_seconds()

            result = {
                "success": fix_result.get("success", False),
                "issue_number": self.issue_number,
                "pr_url": pr_url,
                "errors_processed": len(errors),
                "files_modified": fix_result.get("files_modified", []),
                "cost": self.cost_tracker,
                "duration_seconds": duration,
                "log_dir": str(self.log_dir)
            }

            # Save result
            with open(RESULT_FILE, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            with open(self.log_dir / "result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            print(f"\n[COMPLETE] Auto-fix run finished in {duration:.1f}s")
            print(f"[RESULT] Success: {result['success']}")
            if pr_url:
                print(f"[RESULT] PR created: {pr_url}")

            return result

        except Exception as e:
            print(f"\n[ERROR] Auto-fix failed: {e}", file=sys.stderr)

            result = {
                "success": False,
                "issue_number": self.issue_number,
                "error": str(e),
                "log_dir": str(self.log_dir)
            }

            with open(RESULT_FILE, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            return result


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous validation error fixer with PR creation"
    )
    parser.add_argument(
        "--issue",
        type=int,
        required=True,
        help="GitHub issue number to fix"
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=5.0,
        help="Total budget for LLM API calls (USD)"
    )
    parser.add_argument(
        "--budget-per-fix",
        type=float,
        default=0.25,
        help="Budget per fix (USD)"
    )
    parser.add_argument(
        "--budget-per-paper",
        type=float,
        default=0.50,
        help="Budget per paper (USD)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without making any changes"
    )

    args = parser.parse_args()

    # Ensure log directory exists
    LOG_DIR.mkdir(exist_ok=True)

    # Create orchestrator and run
    orchestrator = AutoFixOrchestrator(
        issue_number=args.issue,
        budget_total=args.budget,
        budget_per_paper=args.budget_per_paper,
        budget_per_fix=args.budget_per_fix,
        dry_run=args.dry_run
    )

    result = orchestrator.run()

    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
