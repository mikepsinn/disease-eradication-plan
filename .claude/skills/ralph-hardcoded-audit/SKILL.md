---
name: ralph-hardcoded-audit
description: Start a Ralph Loop to systematically find and replace hardcoded numbers across all QMD files. Runs iteratively until complete.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
  - Write
---

# Ralph Loop: Hardcoded Value Audit

This skill starts a Ralph Loop session to systematically audit and replace hardcoded numbers in QMD files with variables from `_variables.yml`.

## Usage

Just run `/ralph-hardcoded-audit` to start. Optional arguments:

- `/ralph-hardcoded-audit` - Full project audit (default: 50 iterations max)
- `/ralph-hardcoded-audit economics.qmd` - Single file mode (5 iterations max)
- `/ralph-hardcoded-audit --max 100` - Custom iteration limit

## How It Works

1. Reads `_analysis/parameter-summary.md` for variable lookup
2. Gets list of QMD files to process
3. Creates tracking file `_hardcoded-audit-progress.md`
4. Processes ONE file per iteration:
   - Finds currency (`$14M`), percentages (`86%`), large numbers
   - Matches against variables using semantic context
   - Replaces with `{{< var variable_name >}}`
5. Outputs `ALL_FILES_PROCESSED` when complete

## Start Ralph Loop Now

**To begin, invoke the Ralph Loop skill with this prompt:**

```
/ralph-loop --max-iterations 50 --completion-promise "ALL_FILES_PROCESSED" Systematically find and replace all hardcoded numbers in QMD files with variables from _variables.yml.

SETUP (First Iteration):
1. Read _analysis/parameter-summary.md for variable lookup
2. Run: find knowledge -name "*.qmd" -type f | grep -v "_build_temp" | sort
3. Create _hardcoded-audit-progress.md with all files unchecked

EACH ITERATION:
1. Pick next unchecked file from _hardcoded-audit-progress.md
2. Find hardcoded values: currency ($14M), percentages (86%), large numbers (15,076)
3. SKIP lines with {{< var, years in citations, and 1% (treaty concept)
4. Search _analysis/parameter-summary.md for matching variables
5. Verify semantic context matches before replacing
6. Replace with {{< var variable_name >}} syntax
7. Mark file as checked in progress file

COMPLETION:
When all files checked, write summary to _hardcoded-audit-report.md and output: ALL_FILES_PROCESSED

RULES:
- Process ONE file per iteration
- NEVER replace 1% (treaty percentage)
- NEVER modify _build_temp/ files
- Skip references.qmd, futures/ chapters, parameters-and-calculations.qmd

LATEX EQUATIONS:
- Variables DON'T work INSIDE $$ blocks
- Check for {param_name}_latex variables in _variables.yml
- Replace ENTIRE LaTeX block with {{< var param_name_latex >}}
- Example: Replace $$ PD = $11,355B \times 0.01 $$ with {{< var peace_dividend_annual_societal_benefit_latex >}}
```

## Single File Mode

For a quick single-file audit:

```
/ralph-loop --max-iterations 5 --completion-promise "FILE_COMPLETE" Replace hardcoded numbers in knowledge/economics/economics.qmd with variables from _variables.yml. Read _analysis/parameter-summary.md first. Skip 1% and years in citations. Output FILE_COMPLETE when done.
```

## Priority Files

Process these first (most hardcoded values):

1. `knowledge/economics/economics.qmd`
2. `knowledge/problem/clinical-trials-crisis.qmd`
3. `knowledge/problem/fda-drug-lag.qmd`
4. `knowledge/solution/dfda.qmd`
5. `knowledge/economics/campaign-budget.qmd`

## LaTeX Equation Handling

**CRITICAL: Quarto variables don't work inside `$$` blocks.**

Instead of trying to replace values inside LaTeX equations, check if a `_latex` variable exists:

```bash
# Search for LaTeX variables
grep "_latex" _variables.yml | head -20
```

**Before (hardcoded LaTeX):**
```markdown
$$
PD_{annual} = \$11,355B \times 0.01 = \$113.55B
$$
```

**After (using _latex variable):**
```markdown
{{< var peace_dividend_annual_societal_benefit_latex >}}
```

Common `_latex` variables:
- `peace_dividend_annual_societal_benefit_latex`
- `treaty_annual_funding_latex`
- `dfda_trial_cost_reduction_factor_latex`
- `recovery_trial_cost_reduction_factor_latex`

## Files to Skip

The audit script automatically excludes:
- `_build_temp/` - Build artifacts
- `references.qmd` - Citation database
- `parameters-and-calculations.qmd` - Parameter definitions (source of truth)
- `futures/` - Fictional scenarios with intentional values

## Related Commands

- `/cancel-ralph` - Stop an active Ralph loop
- `/replace-hardcoded-values` - Manual single-file process
- `npm run audit-hardcoded` - Generate audit report without replacing
