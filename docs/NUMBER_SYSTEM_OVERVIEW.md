# Complete Number Management System

## Overview

This project has a comprehensive system for ensuring all numbers are accurate, up-to-date, and properly sourced.

## The Four Components

### 1. Single Source of Truth (`dih_models/parameters.py`)

**All calculations live here.**

```python
# Raw values (for calculations)
TREATY_ANNUAL_FUNDING = 27.18e9

# Formatted values (for display)
treaty_annual_funding_formatted = "$27.2B"

# Auto-linked values (for documents)
treaty_annual_funding_linked = param_link('treaty_annual_funding', treaty_annual_funding_formatted)
# Returns: "[$27.2B](../appendix/peace-dividend-calculations.qmd)"
```

**Key features:**
- All economic parameters defined here
- Calculations derived from base values
- Formatted versions for display
- Auto-linked versions combining value + source

### 2. Parameter Linking Registry

**Maps each parameter to its source documentation.**

```python
PARAMETER_LINKS = {
    'treaty_annual_funding': '../appendix/peace-dividend-calculations.qmd',
    'roi_conservative': '../appendix/dfda-cost-benefit-analysis.qmd',
    'global_military_spending': '../references.qmd#sipri-2024-spending',
    # ... etc
}
```

**Helper function:**
```python
param_link('treaty_annual_funding')
# Returns: "[$27.2B](../appendix/peace-dividend-calculations.qmd)"
```

### 3. Validation Scripts

**Ensure numbers stay in sync with calculations.**

#### `scripts/find-unlinked-numbers.py`
Scans QMD files for numbers without links or Python references.

```bash
python scripts/find-unlinked-numbers.py
# Finds: $27.2B (unlinked), 463:1 (unlinked), etc.
```

**Output:**
```
📄 knowledge/economics/economics.qmd
   12 unlinked number(s)

   Line  142 | money        | $27.2B
              Context: The treaty redirects $27.2B annually
```

#### `scripts/validate-numbers.py`
Checks hardcoded numbers against calculated values in parameters.py.

```bash
python scripts/validate-numbers.py
```

**Output:**
```
📄 knowledge/economics/peace-dividend.qmd
   5 number(s) that match parameters.py

   Line  23: $27.2B
              Matches: TREATY_ANNUAL_FUNDING
              Suggest: {python} treaty_annual_funding_linked
```

#### `scripts/suggest-links.py`
Suggests appropriate reference links based on context.

```bash
python scripts/suggest-links.py
```

**Output:**
```
📄 knowledge/economics/economics.qmd

   Line  67: $2.7T
              Reference: SIPRI 2024 Military Spending
              Replace with: [$2.7T](../references.qmd#sipri-2024-spending)
```

### 4. Documentation

- **[NUMBER_MANAGEMENT.md](./NUMBER_MANAGEMENT.md)** - Complete best practices guide
- **[NUMBER_LINKING_QUICKSTART.md](./NUMBER_LINKING_QUICKSTART.md)** - Quick reference
- **This file** - System overview

---

## How It All Works Together

### The Workflow

```
1. Define in parameters.py
   ↓
2. Add to PARAMETER_LINKS
   ↓
3. Create _linked version
   ↓
4. Use {python} in QMD files
   ↓
5. Run validation before commit
```

### Example End-to-End

**1. Add to parameters.py:**
```python
# Calculation
NEW_METRIC = old_value * multiplier  # = 456.78

# Format for display
new_metric_formatted = "$456.8B"

# Add to links registry
PARAMETER_LINKS['new_metric'] = '../appendix/analysis.qmd'

# Create linked version
new_metric_linked = param_link('new_metric', new_metric_formatted)
```

**2. Use in QMD:**
```markdown
Our new metric is `{python} new_metric_linked`.
```

**3. Renders as:**
```markdown
Our new metric is [$456.8B](../appendix/analysis.qmd).
```

**4. Validate:**
```bash
python scripts/validate-numbers.py
# ✅ All numbers match calculations
```

---

## Benefits

### Before This System

```markdown
❌ The treaty costs $27.2B annually.
   - Could drift from calculation
   - No source link
   - Manual maintenance

❌ The treaty costs [$27.2B](../appendix/peace-dividend.qmd) annually.
   - Still could drift from calculation
   - Link could break
   - Manual maintenance

❌ The treaty costs `{python} f"${TREATY_ANNUAL_FUNDING/1e9:.1f}B"` annually.
   - Correct value
   - No source link
   - Calculation in template
```

### After This System

```markdown
✅ The treaty costs `{python} treaty_annual_funding_linked` annually.
   - Always matches calculation
   - Automatically linked to source
   - Single source of truth
   - Zero maintenance
```

---

## Usage Patterns

### Simple Number (No Link Needed)

```markdown
The cost is `{python} cost_formatted`.
```

### Number with Auto-Link

```markdown
The cost is `{python} cost_linked`.
```

### Custom Format with Link

```markdown
The cost is `{python} param_link('cost', f"${COST/1e9:.2f}B")}`.
```

### External Source (Not Calculated)

```markdown
SIPRI reports [$2.7T annual spending](../references.qmd#sipri-2024-spending).
```

---

## Maintenance

### Daily (Automated in CI)

```yaml
# In .github/workflows/validate.yml
- name: Validate numbers
  run: python scripts/validate-numbers.py --strict
```

### Before Each Commit

```bash
# Find unlinked numbers in new content
python scripts/find-unlinked-numbers.py
```

### Weekly

```bash
# Full validation report
python scripts/validate-numbers.py --report weekly-report.json
```

### When Parameters Change

```bash
# Rebuild all QMD files (numbers auto-update)
quarto render
```

---

## Migration Guide

### Current State

You have ~21 QMD files in `_quarto-economics.yml` with mix of:
- Hardcoded numbers
- Partially linked numbers
- Some inline Python

### Migration Steps

**Phase 1: Add missing parameters** (30 min)
```bash
# Find numbers that should be parameterized
python scripts/find-unlinked-numbers.py > unlinked.txt

# Add to parameters.py + PARAMETER_LINKS
# Create _linked versions
```

**Phase 2: Update QMD files** (2 hours)
```bash
# Replace hardcoded numbers with {python} references
# Use validate-numbers.py to find candidates

# Old: $27.2B
# New: `{python} treaty_annual_funding_linked`
```

**Phase 3: Validate** (15 min)
```bash
python scripts/validate-numbers.py
# Should show zero discrepancies
```

**Phase 4: Enable pre-render validation** (5 min)
```yaml
# In _quarto-economics.yml
project:
  pre-render:
    - python scripts/validate-numbers.py --strict
```

---

## Advanced Usage

### Dynamic Links

```python
# In parameters.py
def param_link_custom(name, value, source, anchor=None):
    """Create custom linked parameter."""
    link = f"{source}#{anchor}" if anchor else source
    return f"[{value}]({link})"

# Usage
special_metric_linked = param_link_custom(
    'special_metric',
    '$123.4B',
    '../appendix/analysis.qmd',
    anchor='detailed-calculation'
)
```

### Conditional Linking

```python
# Only link if detailed analysis exists
def param_link_conditional(name, value):
    if name in PARAMETER_LINKS:
        return f"[{value}]({PARAMETER_LINKS[name]})"
    return value
```

### Link Collections

```python
# Create related parameter groups
PEACE_DIVIDEND_PARAMS = [
    'treaty_annual_funding',
    'peace_dividend_annual',
    'global_war_total_cost'
]

# All link to same source
for param in PEACE_DIVIDEND_PARAMS:
    PARAMETER_LINKS[param] = '../appendix/peace-dividend-calculations.qmd'
```

---

## Quick Commands

```bash
# Find issues
python scripts/find-unlinked-numbers.py
python scripts/validate-numbers.py
python scripts/suggest-links.py

# Generate reports
python scripts/validate-numbers.py --report report.json
python scripts/find-unlinked-numbers.py --format json > unlinked.json

# Test specific file
python scripts/validate-numbers.py --file knowledge/economics/economics.qmd
```

---

## The Golden Rules

1. **Never hardcode a calculated number**
   - Always use `{python} parameter_name`

2. **Always link calculated numbers to sources**
   - Use `_linked` versions: `{python} parameter_name_linked`

3. **Keep parameters.py comprehensive**
   - Every economic figure should have a calculated value
   - Every calculated value should have a formatted version
   - Every formatted version should have a linked version

4. **Validate before publishing**
   - Run validation scripts
   - Fix discrepancies immediately
   - Never ignore warnings

---

## Support

- Questions: See [NUMBER_MANAGEMENT.md](./NUMBER_MANAGEMENT.md)
- Quick reference: See [NUMBER_LINKING_QUICKSTART.md](./NUMBER_LINKING_QUICKSTART.md)
- Add new parameters: See [How to Add section](./NUMBER_MANAGEMENT.md#how-to-add-new-auto-linked-parameters)
