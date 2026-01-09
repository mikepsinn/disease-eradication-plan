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

Links only work if target is in `_quarto-book.yml`. External URLs use full paths.

## Content Standards

**See `CONTRIBUTING.md` for complete writing guidelines.**

Render and critically review output images whenever you modify figure-generating files.
