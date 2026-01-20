# Ralph Loop Prompt: Systematic Hardcoded Value Replacement

**Copy-paste this into Ralph Loop with the command:**

```bash
/ralph-loop --max-iterations 50 --completion-promise "ALL_FILES_PROCESSED" <paste prompt below>
```

---

## Prompt

Systematically find and replace all hardcoded numbers in QMD files with variables from `_variables.yml`. Work through files one at a time until complete.

### Setup Phase (First Iteration)

1. Read `_analysis/parameter-summary.md` to build your variable lookup reference
2. Get list of all QMD files to process:
   ```bash
   find knowledge -name "*.qmd" -type f | grep -v "_build_temp" | sort
   ```
3. Create a tracking file `_hardcoded-audit-progress.md` with all files listed as unchecked

### Processing Loop (Each Iteration)

For each unchecked file in `_hardcoded-audit-progress.md`:

1. **Read the file** and identify hardcoded values:
   - Currency: `$14M`, `$929`, `$2.6B`, etc.
   - Percentages: `86%`, `92%`, `10%` (SKIP `1%` - treaty concept)
   - Large numbers: `15,076`, `184,600,000`, etc.
   - **SKIP** lines already containing `{{< var`
   - **SKIP** years in citations (`@source-2024`)

2. **For each hardcoded value found:**
   - Search `_analysis/parameter-summary.md` for matching values
   - Verify the semantic context matches (e.g., `$14M` for ADAPTABLE trial vs other `$14M`)
   - If match found: Replace with `{{< var variable_name >}}`
   - If no match: Note in report as "needs new parameter"

3. **After processing file:**
   - Mark file as checked in `_hardcoded-audit-progress.md`
   - Log replacements made
   - Log values without matches

4. **Move to next unchecked file**

### Completion Criteria

When ALL files in `_hardcoded-audit-progress.md` are marked as checked:
- Write final summary to `_hardcoded-audit-report.md`
- Output: `ALL_FILES_PROCESSED`

### Important Rules

- Process ONE file per iteration to avoid context overflow
- NEVER replace `1%` (treaty percentage is conceptual)
- NEVER modify `_build_temp/` files
- ALWAYS verify semantic context before replacing
- If uncertain about a match, add to "review needed" section
- Skip `references.qmd`, `futures/` chapters, `_analysis/` files

### Variable Lookup Tips

Common patterns in `_analysis/parameter-summary.md`:
```
ADAPTABLE_TRIAL_TOTAL_COST: $14M
ADAPTABLE_TRIAL_PATIENTS: 15.1k patients
TREATY_ANNUAL_FUNDING: $27.2B
ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE: 86.1%
REGULATORY_DELAY_DEATHS_GLOBAL_HISTORICAL_30YR: 184.6M
```

### Output Format Per File

```
## knowledge/path/to/file.qmd [DONE]

### Replacements Made
- Line 45: `$14M` -> `{{< var adaptable_trial_total_cost >}}`
- Line 89: `15,076 patients` -> `{{< var adaptable_trial_patients >}}`

### No Variable Match (Needs Review)
- Line 123: `$5.2B` - Context: "annual pharma revenue"

### Skipped (Intentional)
- Line 67: `1%` - Treaty percentage
```

---

## Alternative: Simpler Single-File Processing

For processing a single file interactively:

```bash
/ralph-loop --max-iterations 5 Replace all hardcoded numbers in knowledge/economics/1-pct-treaty-impact.qmd with variables from _variables.yml. Read _analysis/parameter-summary.md first to find matching variables. Skip 1% (treaty concept) and years in citations.
```

---

## Quick Reference: High-Value Files to Process First

These files likely have the most hardcoded values:

1. `knowledge/economics/1-pct-treaty-impact.qmd` - Budget and cost figures
2. `knowledge/problem/clinical-trials-crisis.qmd` - Trial statistics
3. `knowledge/problem/fda-drug-lag.qmd` - Regulatory delay numbers
4. `knowledge/solution/dfda.qmd` - dFDA cost comparisons
5. `knowledge/economics/campaign-budget.qmd` - Campaign cost breakdowns
