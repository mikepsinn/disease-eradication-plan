---
name: replace-hardcoded-values
description: Systematically finds and replaces hardcoded numbers in QMD files with variables from _variables.yml. Use when auditing book for consistency.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
---

# Replace Hardcoded Values with Variables

## Purpose

Systematically audit all QMD files for hardcoded numbers that should be replaced with `{{< var variable_name >}}` references from `_variables.yml`.

## When to Use

- After batch adding new parameters to `parameters.py`
- Before major commits or releases
- When auditing specific chapters for variable consistency
- After noticing hardcoded values in a file

## Process

### Phase 1: Build Variable Lookup Map

First, load the parameter summary for quick lookups:

```bash
# Get all variable names and their display values
head -200 _analysis/parameter-summary.md
```

Key patterns to match:
- **Currency**: `$14M`, `$929`, `$27.2B`, `$113.55B`
- **Percentages**: `86.1%`, `10%`, `92%` (skip `1%` - treaty concept)
- **Counts with units**: `15,076 patients`, `184.6M deaths`, `4.83B DALYs`
- **Years**: `1948`, `2024` (skip years in citations `@source-2024`)

### Phase 2: Find Hardcoded Values

For each QMD file in `knowledge/` (excluding `_build_temp/`):

```bash
# Find currency values
grep -rn '\$[0-9,]\+\(\.[0-9]\+\)\?[KMB]\?' --include="*.qmd" knowledge/ | grep -v "_build_temp" | grep -v "{{< var"

# Find percentages (excluding 1%)
grep -rn '[0-9]\+\(\.[0-9]\+\)\?%' --include="*.qmd" knowledge/ | grep -v "_build_temp" | grep -v "{{< var" | grep -v "1%"

# Find large numbers with commas
grep -rn '[0-9]\{1,3\}\(,[0-9]\{3\}\)\+' --include="*.qmd" knowledge/ | grep -v "_build_temp" | grep -v "{{< var"
```

### Phase 3: Match Against Variables

For each hardcoded value found:

1. **Normalize the value**: Remove commas, standardize format
2. **Search parameter summary**: Look for matching values
   ```bash
   grep -i "14M\|14,000,000\|14000000" _analysis/parameter-summary.md
   ```
3. **Verify semantic match**: Ensure variable meaning matches context
4. **Document if no match**: Create list for potential new parameters

### Phase 4: Replace Values

For each confirmed match:

```
Old: The ADAPTABLE trial cost $14M and enrolled 15,076 patients
New: The ADAPTABLE trial cost {{< var adaptable_trial_total_cost >}} and enrolled {{< var adaptable_trial_patients >}}
```

Use the Edit tool to make replacements, preserving surrounding context.

### Phase 5: Validation

After replacements:

```bash
# Verify all variable references are valid
npx tsx scripts/validate-variable-refs.ts

# Render to check for errors
quarto render knowledge/path/to/file.qmd --to html
```

## Common Replacements Reference

| Hardcoded Pattern | Variable Name | Display Value |
|------------------|---------------|---------------|
| `$14M` (ADAPTABLE cost) | `adaptable_trial_cost_per_patient` | $929 |
| `15,076` (patients) | `adaptable_trial_patients` | 15.1k patients |
| `$27B` (treaty funding) | `treaty_annual_funding` | $27.2B |
| `92%` (exclusion) | `antidepressant_trial_exclusion_rate` | 86.1% |
| `$2.6B` (drug dev cost) | `fda_phase_2_3_cost` | $2.6B |
| `184.6M` (deaths) | `regulatory_delay_deaths_global_historical_30yr` | 184.6M |

## Output Format

After completing audit, report:

```markdown
## Hardcoded Value Audit Report

### Replacements Made
- file.qmd:123 - Replaced `$14M` with `{{< var adaptable_trial_total_cost >}}`
- file.qmd:456 - Replaced `92%` with `{{< var trial_exclusion_rate >}}`

### Values Without Variable Match
- file.qmd:789 - `$5.2B` - Context: "annual research budget"
  - Recommendation: Create ANNUAL_RESEARCH_BUDGET parameter

### Skipped (Intentional Hardcoding)
- file.qmd:101 - `1%` - Treaty percentage (conceptual, not a variable)
- file.qmd:202 - `2024` - Year in citation
```

## Important Rules

1. **NEVER replace `1%`** - This is the treaty concept, not a variable
2. **Skip years in citations** - `@source-2024` should keep the year
3. **Verify semantic context** - A `$14M` budget is different from `$14M` trial cost
4. **One file at a time** - Process, validate, then move to next
5. **Create new params if needed** - If value should be a variable but doesn't exist, note it for parameter creation

## Related Tools

- `npm run review-hardcoded <file.qmd>` - Generate detailed review for single file
- `/validate-and-regenerate-parameters` - After adding new parameters
- `/qmd-consistency-check` - Full book validation
