<!-- AI: CLAUDE.md edits must be minimal. Tables > prose. No examples unless essential. -->

## Project Overview

Quarto book: "How to End War and Disease" - getting nations to sign a 1% treaty redirecting military spending to clinical trials.

**Navigation:** `todo.md` (priorities), `OUTLINE.md` (structure), `index.qmd` (intro), `_book.yml` (config), `package.json` (scripts)

**Run TypeScript with `tsx`**, not ts-node. Batch changes: `npx tsx scripts/review/apply-instruction-all-files.ts "instruction"`

**Python on Windows:** All scripts need UTF-8 header: `sys.stdout.reconfigure(encoding='utf-8')`. Use ASCII only in print statements.

## Code Standards

- **Never commit** unless explicitly requested, all changes reviewed, param names match `_variables.yml`
- **No try/catch** unless absolutely necessary. Let errors crash loudly.
- **No em-dashes.** Use parentheses, commas, periods, or semicolons.
- **Links:** Always `.qmd` extensions (not `.html`). Target must be in `_quarto-manual.yml`.
- **Decision quality:** Evaluate trade-offs, state confidence. Don't mirror; hold position when evidence supports it.

## Citations (references.bib)

**Never add without verification:** WebSearch -> WebFetch -> extract quote -> add BibTeX with verified URL + `urldate`.

## Parameter System

**All numeric values use `dih_models/parameters.py` -> `_variables.yml` -> `{{< var name >}}`**

Check existing: `grep "keyword" _variables.yml`. Never duplicate. Generate: `npm run generate:everything`

**Naming:** `[SCOPE]_[METRIC]_[MODIFIERS]` - e.g., `TREATY_ROI_CONSERVATIVE`, not `CONSERVATIVE_ROI`

| Rule | Do | Don't |
|------|----|-------|
| Raw values | `Parameter(519_000_000, unit="USD")` | `Parameter(519, unit="millions USD")` |
| Formatting | `{{< var param >}}` | `${{< var param >}}M` |
| Unit-free | `{{< var param_nounit >}} people` | `{{< var param >}} people` (duplicates unit) |
| Calculated | Use formulas: `A * B` | Hardcode result: `Parameter(113_550_000_000)` |
| Units | `"USD"`, `"percent"`, `"senators"`, `""` | `"count"`, `"millions USD"` |
| Constants | `distribution="fixed"` | Monte Carlo on constitutional values |
| LaTeX | `{{< var name_latex >}}` | Variables inside `$$` blocks |

**Auto-generated (don't hardcode):** `latex=` formulas, confidence intervals, `_latex` variables, `_nounit` variants. **Do add:** `latex_symbol=r"W_{total}"`

**`_nounit` variants:** Auto-generated for params with visible text units (deaths, years, people, etc.). Use `{{< var param_nounit >}}` when prose supplies its own unit word. Not generated for format-inherent units (USD, %, ratio, x). Analyze: `python scripts/analyze-unit-duplication.py`

**source_type:** `"external"` (WHO, SIPRI), `"calculated"` (formulas), `"definition"` (assumptions)

| Parameterize | Leave Hardcoded |
|-------------|-----------------|
| Used in calculations or 2+ files | One-off cited statistics with inline citations |
| Aggregate metrics, Monte Carlo values | Historical facts, one-time context comparisons |

## Content Rules

**Voice:** Wishonia (naive alien observing Earth, Philomena Cunk deadpan). Never consultant, crypto bro, or salesman.

**Financial architecture:** Corruption capped at 20% (transparent), 80% untouchable via wishocracy. Money and influence are disentangled. This is the core selling point vs current government.

| Rule | Do | Don't |
|------|----|-------|
| Investors | Money in, more money out (revenue share) | Board seats, governance, influence, "control the fund" |
| Nonprofits | Mission funded + direct referral bonuses | "Seat at the table", governance stake, tokens, VOTE points |
| Politicians | Campaign funding + votes + post-office careers | Personal bond investments, direct payments |
| Regular people | Referral bonuses + diseases get cured | Tokens, ownership, crypto anything |
| Confidence | "probably irresistible", "the math suggests" | "unstoppable", "inevitable", "guaranteed" |
| Comparisons | Like with like (margins to margins) | 8% operating margin vs 272% bond return |
| Treaty durability | Billionaire bondholders have pre-existing influence + motive to keep/expand | "if the treaty holds" without explaining why it will |
| Cross-chapter | Each chapter gets its own joke version | Same joke verbatim in 2+ chapters |
| Bond terms | Securities, revenue share, perpetual bonds | Utility tokens, DAO governance |
| Jargon | Alien voice: "you give them money, they stop dying" | "leverage", "synergy", "stakeholder", "operationalize" |

## Quick Commands

| Task | Command |
|------|---------|
| Regenerate everything | `npm run generate:everything` |
| Validate before render | `npm run validate:pre-render` |
| Review checks | `npx tsx scripts/review/run-checks.ts file.qmd --checks fact,link,structure` |
| Find param usages | `npx tsx scripts/parameter-audit.ts PARAM_NAME` |
| Unused params | `npm run param:unused` |
| Outline | `python scripts/generate-outline.py` |

Available checks: `fact`, `link`, `figure`, `structure`, `param`, `latex`, `format`, `nonprofit`

## AI Agent Startup

1. Read `todo.md` for priorities
2. Read `OUTLINE.md` for structure
3. Check `_analysis/parameter-summary.md` for param reference
