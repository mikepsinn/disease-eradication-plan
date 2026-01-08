---
name: latex-equation-audit
description: Systematically find calculated variables that have corresponding _latex equations and add them where appropriate. Uses Ralph Loop for iterative processing.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
  - Write
---

# Ralph Loop: LaTeX Equation Audit

This skill starts a Ralph Loop session to systematically find calculated variables from `_variables.yml` that have corresponding `_latex` equations, and add those equations where contextually appropriate in QMD files.

## Purpose

Many calculated parameters have auto-generated LaTeX equations (e.g., `dfda_cures_per_year` has `dfda_cures_per_year_latex`). When a calculated variable is used in text, adding the corresponding LaTeX equation nearby can help readers understand the calculation. This audit finds opportunities to add these equations.

## Usage

Just run `/latex-equation-audit` to start. Optional arguments:

- `/latex-equation-audit` - Full project audit (default: 50 iterations max)
- `/latex-equation-audit economics.qmd` - Single file mode (5 iterations max)
- `/latex-equation-audit --max 100` - Custom iteration limit

## How It Works

1. **Setup**: Extracts all `_latex` variable names from `_variables.yml`
2. **For each _latex variable**: Finds the base variable name (strip `_latex` suffix)
3. **Searches QMD files** for uses of the base variable `{{< var base_name >}}`
4. **Checks context**: Is this a good place for the equation?
   - Good: After introducing a calculated value, in "How it works" sections, near formulas
   - Bad: In lists, tables, passing mentions, already has equation nearby
5. **Adds equation**: Inserts `{{< var base_name_latex >}}` on new line after variable use
6. **Tracks progress** in `_latex-equation-audit-progress.md`

## Start Ralph Loop Now

**To begin, invoke the Ralph Loop skill with this prompt:**

```
/ralph-loop --max-iterations 50 --completion-promise "ALL_LATEX_AUDITED" Systematically find calculated variables that have _latex equations and add them where appropriate in QMD files.

SETUP (First Iteration):
1. Extract all _latex variable names: grep "_latex" _variables.yml | grep -v "^#" | cut -d'"' -f2 | sort > _latex-vars-list.txt
2. Count total: wc -l _latex-vars-list.txt
3. Create _latex-equation-audit-progress.md with all _latex vars listed as unchecked
4. Get list of QMD files: find knowledge -name "*.qmd" -type f | grep -v "_build_temp" | sort

EACH ITERATION:
1. Pick next unchecked _latex variable from progress file
2. Extract base name (e.g., dfda_cures_per_year_latex -> dfda_cures_per_year)
3. Search QMD files for {{< var base_name >}} usage
4. For each occurrence:
   a. Check if _latex version already exists within 10 lines
   b. If not, review context:
      - GOOD contexts (add equation):
        * After introducing/explaining the value
        * In methodology/calculation explanation sections
        * Where the calculation formula adds understanding
        * After prose that describes how something is calculated
      - BAD contexts (skip):
        * In bullet lists or table cells
        * Passing mentions (not explaining the calculation)
        * Already has equation within 10 lines
        * In footnotes or asides
   c. If appropriate, add {{< var base_name_latex >}} on new line after variable
5. Mark variable as checked in progress file
6. Record any additions made

COMPLETION:
When all _latex variables checked, write summary to _latex-equation-audit-report.md:
- Total _latex variables reviewed
- Number of equations added
- Files modified
- Variables with no usages found
Output: ALL_LATEX_AUDITED

RULES:
- Process ONE _latex variable per iteration
- NEVER modify _build_temp/ files
- NEVER modify parameters-and-calculations.qmd (source of truth)
- NEVER add to tables, lists, or code blocks
- Always add equation on its own line
- Leave blank line before and after equation for readability
- Skip references.qmd, futures/ chapters, vision.qmd

CONTEXT EXAMPLES:

GOOD - Add equation here:
```
The dFDA would enable {{< var dfda_cures_per_year >}} new cures annually.
This is calculated based on the acceleration multiplier applied to baseline cure rates.
```
After edit:
```
The dFDA would enable {{< var dfda_cures_per_year >}} new cures annually.
This is calculated based on the acceleration multiplier applied to baseline cure rates.

{{< var dfda_cures_per_year_latex >}}
```

BAD - Do NOT add equation here:
```
Key benefits include:
- {{< var dfda_cures_per_year >}} additional cures per year
- {{< var peace_dividend_annual >}} in savings
```
(equations don't belong in bullet lists)
```

## Single File Mode

For a quick single-file audit:

```
/ralph-loop --max-iterations 5 --completion-promise "FILE_COMPLETE" Check for _latex equation opportunities in knowledge/economics/economics.qmd. For each calculated variable used, check if _latex version exists nearby. If not and context is appropriate, add it. Output FILE_COMPLETE when done.
```

## Files to Skip

The audit automatically excludes:
- `_build_temp/` - Build artifacts
- `references.qmd` - Citation database
- `parameters-and-calculations.qmd` - Parameter definitions (source of truth)
- `futures/` - Fictional scenarios
- `vision.qmd` - Vision statement (narrative focused)

## Contextual Decision Making

### When to ADD the equation:

1. **Calculation explanations**: "This is calculated by multiplying X by Y"
2. **Methodology sections**: Explaining how values are derived
3. **After standalone value introduction**: "The total cost is {{< var X >}}."
4. **ROI/benefit discussions**: Where showing the math adds credibility

### When to SKIP:

1. **Lists/tables**: Equations break list formatting
2. **Passing mentions**: "...saving {{< var X >}} annually..."
3. **Already has equation**: Within 10 lines above or below
4. **Narrative flow**: Would interrupt storytelling
5. **Repeated values**: Only add equation on first substantive mention

## Related Commands

- `/cancel-ralph` - Stop an active Ralph loop
- `/ralph-hardcoded-audit` - Find hardcoded values to replace with variables
- `/pre-render-validate` - Validate all QMD files before render
