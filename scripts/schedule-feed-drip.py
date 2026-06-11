#!/usr/bin/env python3
"""
Schedule feed-date values as a strategic drip campaign.

Assigns dates starting tomorrow, one chapter per day, ordered for
maximum social media engagement:
  1. Hook phase: most provocative/shareable titles
  2. Solution reveal: now they want the answer
  3. Evidence: build credibility
  4. The plan: show them how
  5. Deep dive: for the committed

Usage:
    python scripts/schedule-feed-drip.py
    python scripts/schedule-feed-drip.py --dry-run
    python scripts/schedule-feed-drip.py --start-date 2026-03-05
"""

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # pyright: ignore[reportAttributeAccessIssue]

PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Strategic ordering: engagement-optimized drip sequence
# Each phase hooks a different audience motivation
DRIP_ORDER = [
    # --- HOOK PHASE: Most provocative, shareable titles ---
    "knowledge/problem/genetic-slavery.qmd",              # "200,000-year-old software" - irresistible click
    "knowledge/futures/moronia.qmd",                       # Dystopia fable - highly shareable fiction
    "knowledge/problem/fda-is-unsafe-and-ineffective.qmd", # Controversial, generates debate
    "knowledge/problem/cost-of-war.qmd",                   # Big numbers, emotional
    "knowledge/problem/nih-fails-2-institute-health.qmd",  # "fire dept spending 96.7% on calendars"
    "knowledge/economics/central-banks.qmd",               # "death certificate with a president's face"
    "knowledge/problem/unrepresentative-democracy.qmd",    # Princeton study, anger-inducing

    # --- SOLUTION REVEAL: Now they want the answer ---
    "knowledge/solution/1-percent-treaty.qmd",             # The core pitch
    "knowledge/futures/wishonia.qmd",                      # Utopia contrast to Moronia
    "knowledge/proof/body-as-repairable-machine.qmd",     # Optimistic: your body IS fixable
    "knowledge/solution/dih.qmd",                          # How it works
    "knowledge/solution/wishocracy.qmd",                   # Democratic innovation
    "knowledge/solution/dfda.qmd",                         # The trial platform
    "knowledge/solution/aligning-incentives.qmd",          # How to make it profitable

    # --- EVIDENCE: Build credibility ---
    "knowledge/problem.qmd",                               # Problem framing
    "knowledge/problem/cost-of-disease.qmd",               # The economic case
    "knowledge/problem/untapped-therapeutic-frontier.qmd", # 9.5M untested combos
    "knowledge/appendix/recovery-trial.qmd",               # Proof it works (Oxford)
    "knowledge/appendix/real-world-evidence-historical-success.qmd",  # Pre-1962 evidence
    "knowledge/futures.qmd",                               # The fork in the road
    "knowledge/proof.qmd",                                 # Historical precedents

    # --- THE PLAN: Now they believe, show them how ---
    "knowledge/solution.qmd",                              # Solution framing
    "knowledge/solution/incentive-alignment-bonds.qmd",    # The financial engine
    "knowledge/economics/financial-plan.qmd",              # $1B investment plan
    "knowledge/economics/peace-dividend.qmd",              # What peace pays
    "knowledge/economics/health-dividend.qmd",             # What health pays
    "knowledge/strategy/roadmap.qmd",                      # 36-month execution
    "knowledge/appendix/faq.qmd",                          # Demolish remaining objections

    # --- DEEP DIVE: For the committed ---
    "knowledge/strategy/nonprofit-coalition-strategy.qmd", # How nonprofits help
    "knowledge/legal/legal-framework.qmd",                 # Legal architecture
    "knowledge/strategy/global-referendum.qmd",            # Getting votes
    "knowledge/solution/ai-coordination-army.qmd",         # AI coordination
    "knowledge/appendix/recruitment-and-propaganda-plan.qmd",  # Growth plan
    "knowledge/economics/campaign-budget.qmd",             # Spending plan
    "knowledge/appendix/open-ecosystem-and-bounty-model.qmd",  # Developer bounties

    # --- APPENDIX: For completionists ---
    "knowledge/legal/election-law.qmd",                    # Buying politicians legally
    "knowledge/strategy/legislation-package.qmd",          # Draft laws
    "knowledge/appendix/treaty-feasibility.qmd",           # Cost analysis
    "knowledge/appendix/investor-risk-analysis.qmd",       # For investors
]


def update_feed_date(qmd_path: Path, new_date: str, dry_run: bool) -> bool:
    """Update existing feed-date in frontmatter. Returns True if modified."""
    text = qmd_path.read_text(encoding="utf-8")

    # Must have feed-date already (seeded by seed-feed-dates.py)
    if not re.search(r"^feed-date\s*:", text, re.MULTILINE):
        print(f"  [SKIP] No feed-date field: {qmd_path.name}")
        return False

    # Skip files with feed-date: false
    if re.search(r'^feed-date\s*:\s*false\s*$', text, re.MULTILINE):
        return False

    new_text = re.sub(
        r'^(feed-date\s*:\s*).*$',
        f'\\g<1>"{new_date}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )

    if new_text == text:
        return False

    if dry_run:
        print(f"  [DRY] {qmd_path.name} -> {new_date}")
    else:
        qmd_path.write_text(new_text, encoding="utf-8", newline="\n")
        print(f"  [OK]  {qmd_path.name} -> {new_date}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Schedule feed-date drip campaign")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--start-date", default=None, help="Start date (YYYY-MM-DD), defaults to tomorrow")
    args = parser.parse_args()

    if args.start_date:
        start = datetime.strptime(args.start_date, "%Y-%m-%d")
    else:
        start = datetime.now() + timedelta(days=1)

    print(f"Scheduling {len(DRIP_ORDER)} chapters starting {start.strftime('%Y-%m-%d')}")
    if args.dry_run:
        print("(dry run)\n")

    modified = 0
    for i, rel_path in enumerate(DRIP_ORDER):
        date = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        qmd_path = PROJECT_ROOT / rel_path

        if not qmd_path.exists():
            print(f"  [MISS] {rel_path}")
            continue

        phase = ""
        if i == 0: phase = "\n  --- HOOK PHASE ---"
        elif i == 7: phase = "\n  --- SOLUTION REVEAL ---"
        elif i == 14: phase = "\n  --- EVIDENCE ---"
        elif i == 21: phase = "\n  --- THE PLAN ---"
        elif i == 28: phase = "\n  --- DEEP DIVE ---"
        elif i == 35: phase = "\n  --- APPENDIX ---"
        if phase:
            print(phase)

        if update_feed_date(qmd_path, date, args.dry_run):
            modified += 1

    end_date = (start + timedelta(days=len(DRIP_ORDER) - 1)).strftime("%Y-%m-%d")
    print(f"\nDone: {modified} chapters scheduled from {start.strftime('%Y-%m-%d')} to {end_date}")


if __name__ == "__main__":
    main()
