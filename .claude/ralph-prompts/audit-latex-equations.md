# Ralph Prompt: Audit LaTeX Equations

Systematically find calculated variables that have `_latex` equations and add them where appropriate in QMD files.

## Invocation

```
/ralph-prompt audit-latex-equations
```

Or manually with Ralph Loop:

```
/ralph-loop --max-iterations 50 --completion-promise "ALL_LATEX_AUDITED"
```

## Prompt

```
Systematically find calculated variables that have _latex equations and add them where appropriate in QMD files.

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
```

## Decision Guide

### Add Equation When:
- Introducing a calculated value with explanation
- In methodology/calculation sections
- After prose describing how value is derived
- Where formula adds credibility (ROI discussions)

### Skip When:
- In bullet lists or tables
- Passing mentions in narrative
- Equation already nearby (within 10 lines)
- Would interrupt narrative flow
- Value appears multiple times (only add on first substantive mention)

## Example Transformation

**Before:**
```markdown
The dFDA platform would enable {{< var dfda_cures_per_year >}} new cures per year
through its acceleration of clinical trials and expanded therapeutic exploration.
```

**After:**
```markdown
The dFDA platform would enable {{< var dfda_cures_per_year >}} new cures per year
through its acceleration of clinical trials and expanded therapeutic exploration.

{{< var dfda_cures_per_year_latex >}}
```

## Related

- `/ralph-hardcoded-audit` - Replace hardcoded values with variables
- `/latex-equation-audit` - This skill (shortcut)
