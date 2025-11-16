# Number Management Best Practices

## The Problem

Hard-coded numbers in documentation become stale, create maintenance burden, and break trust when they don't match calculations.

## The Solution: Auto-Linked Parameters ✨

**Best of both worlds**: Numbers calculated from `parameters.py` that are AUTOMATICALLY linked to their source documentation.

### The Ideal Approach (NEW!)

Use `param_link()` to get both calculated values AND source links:

```markdown
The 1% Treaty redirects `{python} treaty_annual_funding_linked` annually.
This generates `{python} roi_conservative_linked` returns.
Military spending totals `{python} global_military_spending_linked`.
```

**This renders as:**
- The 1% Treaty redirects [$27.2B](../appendix/peace-dividend-calculations.qmd) annually.
- This generates [463:1](../appendix/dfda-cost-benefit-analysis.qmd) returns.
- Military spending totals [$2.7T](../references.qmd#sipri-2024-spending).

**Pros:**
- ✅ Always up-to-date (from parameters.py calculations)
- ✅ Automatically linked to detailed source
- ✅ Single source of truth
- ✅ No manual linking maintenance
- ✅ Can't drift from calculations

**How it works:**
1. `parameters.py` has `PARAMETER_LINKS` registry mapping params to sources
2. `param_link()` function combines formatted value + link
3. Pre-computed `_linked` versions for common params

**When to use:** ALWAYS, for any calculated number

### Tier 2: Linked Numbers (ACCEPTABLE) ⚠️

Hard-coded number with link to source/calculation:

```markdown
The 1% Treaty redirects [$27.2B annually](../appendix/peace-dividend-calculations.qmd)
to the Decentralized Institutes of Health.
```

**Pros:**
- Shows source
- Allows readers to verify
- Easy to spot-check

**Cons:**
- Can drift from source
- Maintenance burden
- Link rot

**When to use:** Numbers from external sources (SIPRI, WHO, etc.) that we reference but don't calculate

### Tier 3: Bare Numbers (AVOID) ❌

Hard-coded number with no link:

```markdown
The 1% Treaty redirects $27.2B annually.
```

**Why to avoid:**
- No way to verify
- No way to update systematically
- Breaks when calculations change
- Destroys credibility when wrong

**Only acceptable for:**
- Round numbers used for illustration ("imagine you had $100...")
- Numbers that are part of the narrative setup, not facts

## How to Add New Auto-Linked Parameters

### Step 1: Add calculation to parameters.py

```python
# In dih_models/parameters.py

# Raw value (for calculations)
NEW_PARAMETER = some_calculation()  # e.g., 123.45

# Formatted version (for display)
new_parameter_formatted = "$123.5B"  # or "123:1" or "45%" etc.
```

### Step 2: Add to PARAMETER_LINKS registry

```python
# In dih_models/parameters.py, in the PARAMETER_LINKS dict:

PARAMETER_LINKS = {
    # ... existing entries ...
    'new_parameter': '../appendix/detailed-analysis.qmd',  # or '../references.qmd#anchor'
}
```

### Step 3: Create linked version (optional, for common use)

```python
# In dih_models/parameters.py, after param_link() function:

new_parameter_linked = param_link('new_parameter', new_parameter_formatted)
```

### Step 4: Use in QMD files

```markdown
Our new metric is `{python} new_parameter_linked`.
```

**Renders as:** Our new metric is [$123.5B](../appendix/detailed-analysis.qmd).

---

## Migration Strategy

### Step 1: Expand parameters.py (DONE ✅)

The linking system is now in place! Just add to `PARAMETER_LINKS` dict.

### Step 2: Use Scripts to Find Issues

```bash
# Find all unlinked numbers
python scripts/find-unlinked-numbers.py

# Find numbers that don't match parameters.py
python scripts/validate-numbers.py

# Get suggestions for inline code
python scripts/validate-numbers.py --suggest
```

### Step 3: Convert Numbers to Inline Code

**Before:**
```markdown
The 1% Treaty generates [$113.6B annually](../appendix/peace-dividend-calculations.qmd).
```

**After:**
```markdown
The 1% Treaty generates [`{python} peace_dividend_annual_formatted`](../appendix/peace-dividend-calculations.qmd) annually.
```

Now you get:
- Auto-updating from calculations
- Still linked to detailed source
- Best of both worlds

## Number Types & Conventions

### Money

```python
# parameters.py
TREATY_ANNUAL_FUNDING = 27.18e9  # Store as raw number
treaty_annual_funding_formatted = "$27.2B"  # For display
treaty_annual_funding_billions = 27.2  # For charts

# In QMD
`{python} treaty_annual_funding_formatted`
```

### Percentages

```python
# parameters.py
TREATY_REDUCTION_PCT = 0.01  # Store as decimal
treaty_reduction_pct_formatted = "1%"  # For display

# In QMD
`{python} treaty_reduction_pct_formatted`
```

### Ratios

```python
# parameters.py
ROI_CONSERVATIVE = 463
roi_conservative_ratio = "463:1"  # For display

# In QMD
`{python} roi_conservative_ratio`
```

### Multipliers

```python
# parameters.py
TRIAL_COST_REDUCTION_FACTOR = 82
trial_cost_reduction_formatted = "82x"  # For display

# In QMD
`{python} trial_cost_reduction_formatted`
```

## Pre-Render Validation

Enable in `_quarto.yml`:

```yaml
project:
  pre-render:
    - python scripts/validate-numbers.py --strict
```

This will:
1. Check all hardcoded numbers against parameters.py
2. Fail the build if discrepancies found
3. Force you to fix before publishing

## Reference Link Patterns

### When to Link

| Number Type | Link To | Example |
|-------------|---------|---------|
| Our calculations | Detailed analysis | `[$27.2B](../appendix/peace-dividend-calculations.qmd)` |
| External data | references.qmd | `[$2.7T](../references.qmd#sipri-2024-spending)` |
| Derived values | Calculation source | `[463:1](../appendix/dfda-cost-benefit-analysis.qmd)` |

### Link Format

```markdown
[{python} value_formatted](source.qmd#anchor)
```

Benefits:
- Number auto-updates from parameters.py
- Link remains stable
- Reader can verify calculation

## Common Patterns

### Economic Figures

```markdown
# BAD
The peace dividend is $113.6B.

# GOOD
The peace dividend is `{python} peace_dividend_annual_formatted`.

# BETTER
The peace dividend is [`{python} peace_dividend_annual_formatted`](../appendix/peace-dividend-calculations.qmd).
```

### ROI Ratios

```markdown
# BAD
This generates 463:1 returns.

# GOOD
This generates `{python} roi_conservative_ratio` returns.

# BETTER
This generates [`{python} roi_conservative_ratio`](../appendix/dfda-cost-benefit-analysis.qmd) returns.
```

### Source Citations

```markdown
# GOOD - External source
SIPRI reports [`$2.7T` annual military spending](../references.qmd#sipri-2024-spending).

# EVEN BETTER - Use parameter
SIPRI reports [`{python} global_military_spending_annual_formatted`](../references.qmd#sipri-2024-spending).
```

## Testing Your Numbers

### Unit Test

```python
def test_treaty_funding_matches_calculation():
    """Verify treaty funding equals 1% of military spending."""
    assert TREATY_ANNUAL_FUNDING == GLOBAL_MILITARY_SPENDING_ANNUAL_2024 * 0.01
```

### Integration Test

```bash
# Render one file and check output
quarto render knowledge/economics/peace-dividend.qmd
grep -o '\$[0-9.]*B' _site/economics/peace-dividend.html
```

## Maintenance Schedule

- **Weekly**: Run `find-unlinked-numbers.py` on new content
- **Before releases**: Run full `validate-numbers.py`
- **After parameter updates**: Rebuild all documents
- **Quarterly**: Review external source numbers for updates

## Quick Reference

```bash
# Find unlinked numbers
python scripts/find-unlinked-numbers.py

# Validate against parameters.py
python scripts/validate-numbers.py

# Generate replacement suggestions
python scripts/validate-numbers.py --suggest

# Check specific file
python scripts/validate-numbers.py --file knowledge/economics/economics.qmd

# Export report
python scripts/validate-numbers.py --report issues.json
```

## The Golden Rule

**If a number is calculated anywhere in the codebase, use inline Python to reference it.**

Never duplicate a calculation as a hard-coded number. Ever.
