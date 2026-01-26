<!-- AI INSTRUCTIONS: Keep all additions to this file concise, information-dense, and general.
     Avoid verbose explanations. Use tables for rules. One example per concept max. -->

## Project Overview

This is a Quarto-based book project: "How to End War and Disease" - a guide to getting nations to sign a 1% treaty, redirecting military spending to the Decentralized Institutes of Health and decentralized framework for drug assessment to automate ubiquitous clinical trials.

**Key Navigation:**

- **`todo.md`**: Master task list and current priorities for book completion
- **`OUTLINE.md`**: Complete book outline (comprehensive writing checklist)
- **`index.qmd`**: Book introduction and overview (landing page)
- **`_book.yml`**: Book configuration, chapter order, and output formats
- **`package.json`**: Node.js dependencies and npm scripts

**Important:** Use `tsx` (not ts-node) to run TypeScript files. Example: `npx tsx scripts/review/review.ts`

### Applying Global Changes to All QMD Files

For batch changes across all chapters (style fixes, term replacements, formatting updates):

```bash
npx tsx scripts/review/apply-instruction-all-files.ts "Replace all instances of 'utilise' with 'use'"
```

Loops through all book QMD files, sends each to Gemini Pro, shows preview before processing.

### Python Scripts on Windows

**CRITICAL:** Add UTF-8 encoding header to all Python scripts:
```python
#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

Avoid Unicode characters in print statements. Use ASCII: `->`, `WARNING:`, `[OK]`.

## Code Quality and Verification Standards

### Commit Rules

**NEVER commit unless:**
1. User has **explicitly requested** a commit
2. You have **reviewed EVERY CHANGE** for errors
3. All parameter names match `_variables.yml` (lowercase format)
4. Validation checks pass with no regressions

### Error Handling

**NEVER add try/catch blocks** unless absolutely necessary. Let errors propagate and crash loudly.

## Parameter and Variable System

**CRITICAL: Use the automated parameter/variable system for all numeric values.**

Before hardcoding ANY value, check `_variables.yml` first: `grep "keyword" _variables.yml`

### Workflow

1. **Define** in `dih_models/parameters.py`:
   ```python
   FOUNDATION_FUNDING_REALISTIC = Parameter(
       519_000_000, unit="USD",
       source_ref="/knowledge/appendix/fundraising-strategy.qmd#...",
       description="Nonprofit foundation funding in realistic scenario"
   )
   ```

2. **Generate**: `.venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py`

3. **Use**: `{{< var foundation_funding_realistic >}}` -> renders as "$519M" with tooltip

**Lookup**: `grep "PARAM_NAME" _analysis/parameter-summary.md`

### Parameter Naming Rules

**Names must be SELF-DOCUMENTING: `[SCOPE]_[METRIC]_[MODIFIERS]_[UNIT_TYPE]`**

| Component | Examples |
|-----------|----------|
| SCOPE | DFDA, TREATY, GLOBAL, PERSONAL, VICTORY_BOND |
| METRIC | ROI, COST, BENEFIT, DEATHS, DALYS |
| MODIFIERS | scenario, timeframe, calculation method |
| UNIT_TYPE | ANNUAL, PCT, RATIO (optional) |

Good: `TREATY_COMPLETE_ROI_EXPECTED_95TH_PERCENTILE`, `DFDA_ROI_RD_ONLY`
Bad: `PROBABILISTIC_ROI_EXPECTED_UPPER_BOUND` (ROI of what?), `TOTAL_COST` (of what?)

**Rules:**

| Rule | Correct | Wrong |
|------|---------|-------|
| Store raw values | `Parameter(519_000_000, unit="USD")` | `Parameter(519, unit="millions USD")` |
| No scale in name | `REGULATORY_DELAY_DEATHS` | `REGULATORY_DELAY_DEATHS_MILLIONS` |
| No manual formatting | `{{< var param >}}` | `${{< var param >}}M` |
| Include scope prefix | `TREATY_ROI_CONSERVATIVE` | `CONSERVATIVE_ROI` |

The formatter auto-scales: `unit="USD"` -> $519M, $1.02B; large numbers -> M/B/K; percentages -> "51%".

### Unit Guidelines

**Units must read naturally in prose.** The unit is appended as a suffix to the formatted value.

| Type | Unit | Renders as | Notes |
|------|------|------------|-------|
| Currency | `unit="USD"` | "$519M" | Auto-scales with $ prefix |
| Percentages | `unit="percent"` | "51%" | Auto-adds % suffix |
| Ratios | `unit="ratio"` | "1.5x" | Dimensionless multipliers |
| Time | `unit="years"` | "10 years" | Use plural form |
| People (general) | `unit="people"` | "335M people" | For populations |
| People (specific) | `unit="members"`, `unit="senators"` | "535 members", "67 senators" | Use descriptive nouns |
| Dimensionless | `unit=""` | "42" | Empty string = no suffix |

**Never use `unit="count"`** - it renders awkwardly ("535 count"). Instead:
- Use a descriptive noun: `unit="members"`, `unit="senators"`, `unit="trials"`, `unit="drugs"`
- Or use empty string if context is clear: `unit=""`

### Constitutional Constants

For values with zero uncertainty (constitutional requirements, mathematical constants):
```python
US_SENATORS_FOR_TREATY = Parameter(
    67,
    unit="senators",  # Reads naturally: "67 senators"
    distribution="fixed",  # No Monte Carlo sampling - this is a constitutional constant
    confidence="high",
)
```

### Calculated Parameters

**Parameters with `source_type="calculated"` MUST use formulas, not hardcoded values:**

```python
# Correct: formula-based
PEACE_DIVIDEND_ANNUAL = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT,
    source_type="calculated", unit="USD", formula="GLOBAL_WAR_COST x 1%"
)

# Wrong: hardcoded result breaks traceability
PEACE_DIVIDEND_ANNUAL = Parameter(113_550_000_000, source_type="calculated", ...)
```

**source_type values:** `"external"` (WHO, SIPRI), `"calculated"` (formulas), `"definition"` (fixed assumptions)

### LaTeX Math Block Variables

**CRITICAL: Quarto variables do NOT work inside `$$` blocks.**

Use pre-built LaTeX variables instead: `{{< var peace_dividend_annual_societal_benefit_latex >}}`

**Hardcoded value audits:**
- Never replace values inside `$$` blocks - check for `_latex` suffixed variables instead
- Replace entire LaTeX blocks with latex variables when available
- Remove hyperlinks around variables - they have built-in source links

Use `/latex-equation-audit` for systematic LaTeX equation additions.

### Why This Matters

- **Single source of truth**: Change once in parameters.py, updates everywhere
- **Automatic tooltips**: Hover shows source, confidence, formula
- **Academic rigor**: Auto-generates parameters-and-calculations.qmd appendix

## Cross-Format Linking (HTML, PDF, EPUB)

**CRITICAL: Always use `.qmd` extensions for internal links.**

Quarto converts `.qmd` -> `.html` (web) or internal references (PDF/EPUB).

Correct: `[Link](../path/to/file.qmd#section-id)`
Wrong: `[Link](../path/to/file.html)` (breaks PDF/EPUB)

Links only work if target is in `_quarto-manual.yml`. External URLs use full paths.

## Content Standards

**See `CONTRIBUTING.md` for complete writing guidelines.**

**Do not use em-dashes (—).** Replace with parenthesis, comma and space (", "), period, or semicolon as appropriate. Prefer periods and shortened sentences where appropriate.

Render and critically review output images whenever you modify figure-generating files.

## Automation Architecture

See `scripts/README.md` for complete documentation.

### Quick Commands

| Task | Command |
|------|---------|
| Find param usages | `npx tsx scripts/parameter-audit.ts PARAM_NAME` |
| Find unused params | `npm run param:unused` |
| Run review checks | `npm run review:run -- file.qmd --checks fact,link` |
| Validate before render | `npm run validate:pre-render` |
| Regenerate variables | `npm run generate:everything` |

### Hash Tracking System

Files are tracked using content hashes to avoid reprocessing unchanged files. Hash fields are defined in `scripts/lib/constants.ts`.

**Python integration:** Use `scripts/lib/hash_store.py` for Python scripts to read/write the same hash store.

### Review Framework

Single entry point for all checks:
```bash
npx tsx scripts/review/run-checks.ts knowledge/file.qmd --checks fact,link,structure
npx tsx scripts/review/run-checks.ts --all --checks fact --limit 5
```

Available checks: `fact`, `link`, `figure`, `structure`, `param`, `latex`, `format`, `nonprofit`

### Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `quick-validate.py` | PostToolUse | Validates QMD edits for broken variables/links |
| `check-pending-work.py` | SessionStart | Shows pending tasks |
