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

When the user requests a change that should be applied to all QMD chapter/appendix files (e.g., "replace all instances of X with Y", "fix all occurrences of...", "update formatting for..."), use the automated batch processing script:

```bash
npx tsx scripts/review/apply-instruction-all-files.ts "Your instruction here"
```

**Examples:**
```bash
# Style/formatting changes
npx tsx scripts/review/apply-instruction-all-files.ts "Replace all instances of 'utilise' with 'use'"

# Consistency fixes
npx tsx scripts/review/apply-instruction-all-files.ts "Ensure all section headers use sentence case, not title case"

# Content updates
npx tsx scripts/review/apply-instruction-all-files.ts "Replace references to 'FDA approval timeline' with 'regulatory approval timeline'"
```

**How it works:**
- Loops through all book QMD files (excludes references.qmd, vision.qmd, futures chapters)
- Sends each file to Gemini Pro with your instruction
- Shows 5-second preview with file list before processing
- Tracks statistics (modified/unchanged/errors)
- Continues processing if individual files fail

### Python Scripts on Windows

**CRITICAL: All Python scripts must handle Windows console encoding.**

Add this header to every Python script:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

**Avoid Unicode characters in print statements** that may fail on Windows console (arrows, emojis, checkmarks). Use ASCII alternatives: `->`, `WARNING:`, `[OK]`.

## Code Quality and Verification Standards

**CRITICAL: These rules exist to prevent careless errors that have caused significant problems in the past.**

### Commit Rules

**NEVER commit changes unless:**
1. The user has **explicitly requested** a commit
2. You have **reviewed EVERY SINGLE CHANGE** for errors
3. You have **verified all parameter names** match `_variables.yml` (lowercase format)
4. You have **run validation checks** to ensure no regressions

## Parameter and Variable System

**CRITICAL: Use the automated parameter/variable system for all numeric values.**

**Before hardcoding ANY value in QMD files, check `_variables.yml` first.** All available variables are listed there in lowercase format (e.g., `global_military_spending_annual_2024`, `treaty_annual_funding`).

### When Editing QMD Files

**ALWAYS check for hardcoded numbers that should be variables:**
- When you edit a QMD file, scan for hardcoded numbers like `$14M`, `$929`, `15,076`, etc.
- Search `_variables.yml` for existing variables: `grep "keyword" _variables.yml`
- If a variable exists, use `{{< var variable_name >}}` instead of the hardcoded value
- If no variable exists but should, create it in `dih_models/parameters.py` first

**Common hardcoded values to replace:**
- Trial costs: Use `{{< var adaptable_trial_cost_per_patient >}}`, `{{< var recovery_trial_cost_per_patient >}}`
- Patient counts: Use `{{< var adaptable_trial_patients >}}`, `{{< var recovery_trial_patients >}}`
- Cost reductions: Use `{{< var dfda_trial_cost_reduction_factor >}}`

### How It Works

1. **Define parameters** in `dih_models/parameters.py`:
   ```python
   FOUNDATION_FUNDING_REALISTIC = Parameter(
       519_000_000,  # Use underscores for readability
       unit="USD",   # Formatter auto-scales to "$519M"
       source_ref="/knowledge/appendix/fundraising-strategy.qmd#...",
       description="Nonprofit foundation funding in realistic scenario",
       confidence="high"
   )
   ```

2. **Generate variables** by running:
   ```bash
   .venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py
   ```

3. **Use in QMD files** (formatter handles all formatting):
   ```markdown
   Foundation funding: {{< var foundation_funding_realistic >}}
   ```
   Output: "Foundation funding: $519M" (with HTML tooltip and source link)

### Quick Parameter Lookup

**Use `_analysis/parameter-summary.md` to quickly get calculated values** (auto-generated, one parameter per line):

```bash
grep "TREATY_ANNUAL_FUNDING" _analysis/parameter-summary.md
# -> TREATY_ANNUAL_FUNDING: $27.2B (95% CI: $27.2B-$27.2B)
```

### Parameter Naming Rules

**CRITICAL: Parameter names must be SELF-DOCUMENTING. A reader should know EXACTLY what is being measured without looking at the description.**

**Naming Structure: `[SCOPE]_[METRIC]_[MODIFIERS]_[UNIT_TYPE]`**

- **SCOPE**: What entity? (DFDA, TREATY, GLOBAL, PERSONAL, VICTORY_BOND, etc.)
- **METRIC**: What's being measured? (ROI, COST, BENEFIT, DEATHS, DALYS, etc.)
- **MODIFIERS**: Scenario, timeframe, calculation method
- **UNIT_TYPE**: Optional for clarity (ANNUAL, PCT, RATIO, etc.)

**Good names (self-documenting):**
- `TREATY_COMPLETE_ROI_EXPECTED_95TH_PERCENTILE` - Clear: Treaty, complete benefits, expected value, 95th percentile
- `DFDA_ROI_RD_ONLY` - Clear: dFDA, R&D savings only
- `PERSONAL_LIFE_EXTENSION_YEARS_AGE_30` - Clear: Personal benefit, life extension, for age 30

**Bad names (ambiguous):**
- `PROBABILISTIC_ROI_EXPECTED_UPPER_BOUND` - ROI of WHAT?
- `ANNUAL_BENEFIT` - Benefit of WHAT? Which scenario?
- `TOTAL_COST` - Total cost of WHAT?

**Rules:**

| Rule | Correct | Wrong |
|------|---------|-------|
| Parameter name format | `FOUNDATION_FUNDING_REALISTIC` (uppercase) | - |
| Variable name format | `foundation_funding_realistic` (lowercase, auto-generated) | - |
| Store raw values | `Parameter(519_000_000, unit="USD")` | `Parameter(519, unit="millions USD")` |
| No scale in name | `REGULATORY_DELAY_DEATHS` | `REGULATORY_DELAY_DEATHS_MILLIONS` |
| No manual formatting in QMD | `{{< var foundation_funding_realistic >}}` | `${{< var foundation_funding_realistic >}}M` |
| Include scope prefix | `TREATY_COMPLETE_ROI_CONSERVATIVE` | `CONSERVATIVE_ROI` |

**Why**: The formatter automatically determines appropriate scale ($519M, 184.6M, $113.55B). Pre-scaled values break the auto-scaling logic, and scale suffixes in names are redundant.

### Formatter Capabilities

The `format_parameter_value()` function automatically:
- **Currency**: `unit="USD"` -> auto-scales to $519M, $1.02B, $50K, $483T
- **Large numbers**: Auto-scales deaths/DALYs/years to M/B/K (>=100K)
- **Percentages**: `unit="percentage"` -> "51%"
- **Small numbers**: Uses commas (1,000-99,999) or raw values (<1,000)
- **3 significant figures** precision for all scaled values

### Calculated Parameters

**CRITICAL: Parameters marked as `source_type="calculated"` MUST use formulas, not hardcoded values.**

Correct (calculated using inline formulas):
```python
PEACE_DIVIDEND_ANNUAL = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT,
    source_type="calculated",
    description="Annual peace dividend from 1% treaty",
    unit="USD",
    formula="GLOBAL_WAR_COST x 1%"
)
```

Wrong (hardcoded value marked as calculated):
```python
PEACE_DIVIDEND_ANNUAL = Parameter(
    113_550_000_000,  # Hardcoded result - breaks traceability
    source_type="calculated",
    ...
)
```

**When to use each source_type:**
- `source_type="external"`: Data from external sources (WHO, SIPRI, papers)
- `source_type="calculated"`: Derived using formulas from other parameters
- `source_type="definition"`: Fixed values, core assumptions, legacy compatibility values

### LaTeX Math Block Variables

**CRITICAL: Quarto variables do NOT work inside `$$` LaTeX blocks.**

The `generate-variables-yml.py` script exports LaTeX equations as `{param_name}_latex` variables. Use these instead of hardcoding LaTeX or trying to embed variables in math blocks.

Correct (use pre-built LaTeX variable):
```markdown
{{< var peace_dividend_annual_societal_benefit_latex >}}
```

Wrong (variables don't render inside $$):
```markdown
$$
\${{< var global_annual_war_total_cost >}} \times {{< var treaty_reduction_pct >}}
$$
```

**When auditing for hardcoded values:**
1. Never try to replace values inside LaTeX `$$` blocks
2. Check `_variables.yml` for `_latex` suffixed variables
3. Replace the entire LaTeX block with the latex variable if one exists
4. Leave LaTeX hardcoded values as-is if no suitable `_latex` variable exists
5. Remove hyperlinks from around variables - they have built-in source links
   - Wrong: `[{{< var cost >}}](../economics/victory-bonds.qmd)`
   - Right: `{{< var cost >}}`

**Systematic LaTeX Equation Audit:** Use `/latex-equation-audit` to find calculated variables and add their `_latex` equations where appropriate.

### Why This Matters

- **Single source of truth**: All values come from parameters.py
- **Automatic tooltips**: Hover shows source, confidence, formula
- **Consistency**: Same value displayed identically everywhere
- **Zero maintenance**: Change parameter once, regenerates everywhere
- **Academic rigor**: Auto-generates parameters-and-calculations.qmd appendix

## Cross-Format Linking (HTML, PDF, EPUB)

**CRITICAL: Always use `.qmd` extensions for internal links in source files.**

Quarto automatically converts `.qmd` links to the appropriate format:
- **HTML output**: `.qmd` -> `.html`
- **PDF/EPUB output**: `.qmd` -> internal references

Correct: `[Link Text](../path/to/file.qmd)` or `[Link with Anchor](../path/to/file.qmd#section-id)`

Wrong: `[Link Text](../path/to/file.html)` (breaks PDF/EPUB)

**IMPORTANT**: Links only work if the target file is listed in `_quarto-book.yml` chapters. If post-validation reports `QMD_FILE_LINK` errors:

1. Check if target `.qmd` file exists
2. Add it to `_quarto-book.yml` in the appropriate section
3. Re-render - Quarto will handle format conversion

**External URLs** (outside the book) should use full URLs: `[External Link](https://example.com/page.html)`

## Content Standards

**See `CONTRIBUTING.md` for complete writing guidelines, style requirements, and content standards.**

Please render and critically review output images of quarto files whenever you modify figure-generating files.
