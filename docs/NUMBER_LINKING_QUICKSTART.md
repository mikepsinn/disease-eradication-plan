# Number Linking Quick Start

## TL;DR

**Always use this in your QMD files:**
```markdown
[`{python} parameter_name_formatted`](../appendix/source.qmd)
```

Gets you calculated values with links to sources. The value stays current, the link stays accurate.

---

## The Three Options (Best to Worst)

### Option 1: Auto-Linked (BEST) ✨

```markdown
The treaty costs [`{python} treaty_annual_funding_formatted`](../appendix/peace-dividend-calculations.qmd).
```

**Renders as:** The treaty costs [$27.2B](../appendix/peace-dividend-calculations.qmd).

**Benefits:**
- ✅ Number from parameters.py (always current)
- ✅ Link to source (in markdown)
- ✅ Minimal maintenance (just ensure link path is correct)

**How it works:** The inline `{python}` expression returns the formatted value, and the markdown link syntax creates the hyperlink. Quarto processes both correctly.

### Option 2: Calculated but Unlinked (OK)

```markdown
The treaty costs `{python} treaty_annual_funding_formatted`.
```

**Renders as:** The treaty costs $27.2B.

**Benefits:**
- ✅ Number from parameters.py (always current)
- ⚠️ No link to source
- ⚠️ Reader can't verify

**Use when:** Link isn't needed (number mentioned in passing)

### Option 3: Hardcoded with Link (LAST RESORT)

```markdown
The treaty costs [$27.2B](../appendix/peace-dividend-calculations.qmd).
```

**Problems:**
- ❌ Number can drift from calculations
- ❌ Maintenance burden
- ❌ Will break eventually

**Only use when:** Number from external source that we don't calculate

---

## Common Patterns

### Money Values

```markdown
# Best - linked to source
[`{python} treaty_annual_funding_formatted`](../appendix/peace-dividend-calculations.qmd)

# Good - no link
`{python} treaty_annual_funding_formatted`

# Bad - hardcoded
$27.2B
```

### ROI Ratios

```markdown
# Best - linked to source
[`{python} roi_dfda_savings_only_formatted`](../appendix/dfda-cost-benefit-analysis.qmd)

# Good - no link
`{python} roi_dfda_savings_only_formatted`

# Bad - hardcoded
463:1
```

### Percentages

```markdown
# Best - with context and link if needed
[`{python} treaty_reduction_pct_formatted`](../appendix/peace-dividend-calculations.qmd)

# Good - no link needed for simple values
`{python} treaty_reduction_pct_formatted`

# Bad - hardcoded
1%
```

---

## How to Check What's Available

### See all linked parameters

```python
from dih_models.parameters import PARAMETER_LINKS
print(PARAMETER_LINKS.keys())
```

### See all formatted parameters

```bash
grep "_formatted = " dih_models/parameters.py
```

### See all linked parameters

```bash
grep "_linked = " dih_models/parameters.py
```

---

## Quick Reference Table

| What You Want | How to Write It | Renders As |
|--------------|----------------|------------|
| Treaty funding (linked) | `[{python} treaty_annual_funding_formatted](../appendix/peace-dividend-calculations.qmd)` | [$27.2B](../appendix/peace-dividend-calculations.qmd) |
| Peace dividend (linked) | `[{python} peace_dividend_annual_societal_benefit_formatted](../appendix/peace-dividend-calculations.qmd)` | [$113.6B](../appendix/peace-dividend-calculations.qmd) |
| Conservative ROI (linked) | `[{python} roi_dfda_savings_only_formatted](../appendix/dfda-cost-benefit-analysis.qmd)` | [463:1](../appendix/dfda-cost-benefit-analysis.qmd) |
| Complete ROI (linked) | `[{python} roi_all_direct_benefits_formatted](../appendix/dfda-cost-benefit-analysis.qmd)` | [1,239:1](../appendix/dfda-cost-benefit-analysis.qmd) |
| Cost reduction | `[{python} f"{TRIAL_COST_REDUCTION_FACTOR}x"](../appendix/recovery-trial.qmd)` | [82x](../appendix/recovery-trial.qmd) |
| Military spending (linked) | `[{python} global_military_spending_annual_2024_formatted](../references.qmd#sipri-2024-spending)` | [$2.7T](../references.qmd#sipri-2024-spending) |

---

## Examples in Real Use

### Before (Manual linking - prone to drift)

```markdown
The 1% Treaty redirects [$27.2B annually](../appendix/peace-dividend-calculations.qmd)
to medical research, generating [463:1 returns](../appendix/dfda-cost-benefit-analysis.qmd).
```

**Problems:**
- Numbers can drift from calculations
- Have to update both number AND link manually
- Easy to make mistakes

### After (Calculated values with links)

```markdown
The 1% Treaty redirects [`{python} treaty_annual_funding_formatted` annually](../appendix/peace-dividend-calculations.qmd)
to medical research, generating [`{python} roi_dfda_savings_only_formatted` returns](../appendix/dfda-cost-benefit-analysis.qmd).
```

**Benefits:**
- Numbers always match calculations
- Links stay accurate (just need to maintain the path)
- Clear separation: Python handles values, markdown handles links

---

## Adding New Parameters

Need a new parameter? See [NUMBER_MANAGEMENT.md](./NUMBER_MANAGEMENT.md#how-to-add-new-auto-linked-parameters)

Quick version:
1. Add calculation to `parameters.py`: `NEW_PARAMETER = some_calculation()`
2. Add formatted version: `new_parameter_formatted = "$123B"`
3. (Optional) Add to `PARAMETER_LINKS` dict for documentation
4. Use in QMD: `[{python} new_parameter_formatted](../appendix/source.qmd)`

That's it! The value auto-updates, the link stays accurate.

---

## Tools

```bash
# Find unlinked numbers
python scripts/find-unlinked-numbers.py

# Find numbers that don't match parameters.py
python scripts/validate-numbers.py

# Get suggestions for reference links
python scripts/suggest-links.py
```

---

## The Golden Rule

**Never type a number that's calculated in parameters.py. Ever.**

Use `{python} parameter_name_linked` instead.
