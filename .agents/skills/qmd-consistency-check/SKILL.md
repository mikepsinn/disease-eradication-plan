---
name: qmd-consistency-check
description: Checks QMD files for consistency, variable references, and cross-format links. Use after batch editing multiple files or before commits.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# QMD Consistency Checker

## What This Does

Validates entire book for:
- Variable references (all `{{< var ... >}}` are valid)
- Cross-file links use `.qmd` extensions
- Referenced files exist in `_quarto.yml`
- No hardcoded values that should be variables
- Consistent formatting and style
- No em-dashes (should be periods, commas, or parentheses)

## Process

### 1. Find all QMD files

```bash
find knowledge -name "*.qmd" -type f
```

### 2. Check all variable references

```bash
grep -r "{{< var" --include="*.qmd" knowledge/
```

Compare against `_variables.yml` to verify all variables exist.

### 3. Check cross-file links

```bash
grep -r "\](.*\.html" --include="*.qmd" knowledge/
```

All links should use `.qmd` not `.html` for cross-format compatibility.

### 4. Find hardcoded values

```bash
grep -rE '\$[0-9,]+(\.[0-9]+)?[MBK]?' --include="*.qmd" knowledge/
```

Check if these values exist as variables in `_variables.yml`.

### 5. Check for em-dashes

```bash
grep -r "—" --include="*.qmd" knowledge/
```

Linter requires replacing em-dashes with periods, commas, or parentheses.

## Expected Outcome

After running this skill:
- All variable references are valid
- All links use cross-format compatible `.qmd` extensions
- No broken cross-file references
- Hardcoded values are flagged for review
- Style issues are identified
