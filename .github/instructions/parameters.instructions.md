---
description: "Rules for the parameter and variable system in dih_models/"
applyTo: "dih_models/**/*.py"
---

# Parameter System Instructions

This file provides specific rules for working with the parameter system in `dih_models/parameters.py`.

## Critical Rules for Parameters

### Parameter Definition Structure

Every parameter MUST follow this structure:

```python
PARAMETER_NAME = Parameter(
    value,                    # Raw numeric value (not scaled)
    unit="USD",              # Unit type (USD, years, people, etc.)
    source_type="external",  # One of: external, calculated, definition
    source_ref="/path/to/source.qmd#section",  # Reference to source
    description="Clear description of what this represents",
    formula="PARAM1 x PARAM2"  # Required for calculated parameters
)
```

### Naming Convention (MANDATORY)

**Format:** `[SCOPE]_[METRIC]_[MODIFIERS]_[UNIT_TYPE]`

- **SCOPE**: TREATY, DFDA, GLOBAL, PERSONAL, VICTORY_BOND, etc.
- **METRIC**: ROI, COST, BENEFIT, DEATHS, DALYS, etc.
- **MODIFIERS**: Scenario, timeframe, calculation method
- **UNIT_TYPE**: ANNUAL, PCT, RATIO (optional)

**Examples:**
- ✅ `TREATY_COMPLETE_ROI_EXPECTED_95TH_PERCENTILE`
- ✅ `DFDA_ROI_RD_ONLY`
- ✅ `GLOBAL_ANNUAL_WAR_TOTAL_COST`
- ❌ `CONSERVATIVE_ROI` (missing scope)
- ❌ `TOTAL_COST` (missing scope and context)

### Value Storage Rules

| Rule | Correct | Wrong |
|------|---------|-------|
| Store raw values | `Parameter(519_000_000, unit="USD")` | `Parameter(519, unit="millions USD")` |
| No scale in name | `REGULATORY_DELAY_DEATHS` | `REGULATORY_DELAY_DEATHS_MILLIONS` |
| No manual formatting | Value only | `$519M` in value field |
| Include scope | `TREATY_ROI_CONSERVATIVE` | `CONSERVATIVE_ROI` |

### Calculated Parameters

Parameters with `source_type="calculated"` MUST:
1. Use formulas with other parameters (not hardcoded results)
2. Include a clear `formula` field describing the calculation
3. Reference the parameters used in the calculation

**Correct:**
```python
PEACE_DIVIDEND_ANNUAL = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT,
    source_type="calculated",
    unit="USD",
    formula="GLOBAL_WAR_COST × 1%",
    description="Annual peace dividend from 1% treaty"
)
```

**Wrong:**
```python
# Hardcoded result breaks traceability
PEACE_DIVIDEND_ANNUAL = Parameter(
    113_550_000_000,  # This should be a formula!
    source_type="calculated",
    unit="USD"
)
```

### Source Types

- **`"external"`**: Data from external sources (WHO, SIPRI, academic papers)
  - Requires `source_ref` to documentation
- **`"calculated"`**: Derived from other parameters via formula
  - Requires `formula` field and formula in value
- **`"definition"`**: Fixed assumptions or definitions
  - Requires explanation in description

### After Modifying Parameters

**ALWAYS run the generation script:**
```bash
.venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py
```

This regenerates:
- `_variables.yml` (lowercase variable names for QMD files)
- `_analysis/parameter-summary.md` (documentation)
- LaTeX variables for math blocks

### Validation

Before committing parameter changes:
1. Run generation script
2. Check `_variables.yml` has lowercase versions
3. Verify parameters appear in `_analysis/parameter-summary.md`
4. Test in QMD files: `{{< var parameter_name >}}`
5. Check tooltips render correctly in preview

## Common Mistakes to Avoid

1. **Don't scale values in the parameter definition** - store 519000000, not 519
2. **Don't include units in parameter names** - use `COST` not `COST_MILLIONS`
3. **Don't hardcode calculated values** - use formulas
4. **Don't forget scope prefix** - every parameter needs context
5. **Don't skip the generation script** - variables won't update otherwise

## Variable Usage in QMD Files

After defining a parameter `PARAMETER_NAME` in Python:
- Auto-generated as `{{< var parameter_name >}}` (lowercase)
- Renders with automatic formatting and tooltip
- For LaTeX: `{{< var parameter_name_latex >}}`

Never manually format variables in QMD files - the system handles it.
