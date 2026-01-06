---
name: validate-and-regenerate-parameters
description: Validates parameters.py, checks for errors, and regenerates _variables.yml. Use when editing parameters, adding new values, or ensuring variable consistency.
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - Grep
---

# Parameter Validation & Regeneration

## When to Use

Use this skill when you:
- Add or modify parameters in `dih_models/parameters.py`
- Edit parameter formulas or calculations
- Need to verify variables are up-to-date
- Update parameter descriptions or confidence levels
- See "variables out of date" warnings

## Process

### 1. Validate parameters.py syntax

```bash
cd e:\code\obsidian\websites\disease-eradication-plan
python -m py_compile dih_models/parameters.py
```

### 2. Check for common errors

- Hardcoded values marked as "calculated" (should use formulas)
- Missing unit specifications
- Parameter names that aren't self-documenting
- Non-uppercase naming violations
- Duplicate parameter definitions

### 3. Regenerate variables

```bash
.venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py
```

### 4. Verify output

- Check `_variables.yml` updated successfully
- Verify `_analysis/parameter-summary.md` generated
- Spot-check formatting of values (currency, percentages, DALYs)

### 5. Report changes

- List new/modified/deleted variables
- Show updated parameter counts
- Flag any warnings from generation script

## Expected Outcome

After running this skill:
- parameters.py compiles without errors
- _variables.yml is up-to-date
- All variable references in QMD files are valid
- Parameter summary shows correct values
