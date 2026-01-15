---
name: review
description: Comprehensive single-file review. Generates preview with variables replaced, finds and replaces hardcoded values, adds _latex equations, validates consistency.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
  - Write
  - TodoWrite
---

# Comprehensive File Review

## Purpose

One command to thoroughly review and improve a QMD file:
1. Generate human-readable preview with variables replaced
2. Find and replace hardcoded numbers with Quarto variables
3. Add `_latex` equations where appropriate
4. Validate consistency and fix issues

## Usage

```
/review <file.qmd>
/review knowledge/appendix/incentive-alignment-bonds-paper.qmd
/review economics.qmd
```

If no file is specified, ask the user which file to review.

## Process

### Phase 1: Setup and Preview Generation

**1.1 Locate the file:**
```bash
# If relative path, search in knowledge/
find knowledge -name "<filename>" -type f 2>/dev/null | head -5
```

**1.2 Generate preview with variables replaced:**
```bash
cd E:/code/obsidian/websites/disease-eradication-plan
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file.qmd> -o _analysis/<basename>-preview.md
```

**1.3 Read preview to understand current state:**
- Skim the preview to see actual rendered values
- Note any obvious inconsistencies (e.g., "$2.4T" in one place, "$2.72T" in another)

### Phase 2: Find Hardcoded Numbers

**2.1 Run hardcoded number detection:**
```bash
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file.qmd> --numbers-only
```

**2.2 Categorize findings:**

| Category | Action | Examples |
|----------|--------|----------|
| **REPLACE** | Use variable | Treaty funding, military spending, DALYs |
| **REPLACE with _latex** | Use equation variable | `$$` blocks with calculations |
| **KEEP hardcoded** | Leave as-is | Citation data, examples, `1%` treaty |

### Phase 3: Match Values to Variables

**3.1 Search for matching variables:**
```bash
# Quick keyword search
grep -i "military\|spending\|treaty" _analysis/parameter-summary.md | head -20

# Search by value pattern
grep "\$27.2B\|27200000000" _variables.yml
```

**3.2 Key variable patterns:**

| Value Pattern | Variable Name Pattern | Example |
|--------------|----------------------|---------|
| Military spending | `global_military_spending_*` | `$2.72T` |
| Treaty funding | `treaty_annual_funding` | `$27.2B` |
| War costs | `global_annual_*_conflict` | `$11.4T` |
| DALY burden | `global_annual_daly_burden` | `2.88B` |
| Household wealth | `global_household_wealth_usd` | `$454T` |
| IAB metrics | `iab_mechanism_*` | BCR, costs |
| Peace dividend | `peace_dividend_*` | Annual/NPV |

### Phase 4: Replace Hardcoded Values

**4.1 Use TodoWrite to track replacements:**
Create a todo item for each replacement to ensure nothing is missed.

**4.2 Make replacements systematically:**

```markdown
# Simple value replacement
Old: Global military expenditure exceeds \$2.4 trillion annually
New: Global military expenditure exceeds {{< var global_military_spending_annual_2024 >}} annually

# With citation (use _cite variable)
Old: ...exceeds $2.72T annually [@sipri2024]
New: ...exceeds {{< var global_military_spending_annual_2024 >}} {{< var global_military_spending_annual_2024_cite >}}

# LaTeX block replacement
Old: $$\text{BCR} = \frac{\$227B}{\$0.75B} \approx 303:1$$
New: {{< var iab_mechanism_benefit_cost_ratio_latex >}}
```

### Phase 5: Add LaTeX Equations

**5.1 Find calculated variables used in file:**
```bash
grep -o "{{< var [a-z_]* >}}" <file.qmd> | sort -u
```

**5.2 Check which have _latex versions:**
```bash
# For each variable, check if _latex exists
grep "peace_dividend_annual_societal_benefit_latex" _variables.yml
```

**5.3 Add equations where appropriate:**

**GOOD contexts (add equation):**
- After introducing/explaining a calculated value
- In methodology sections
- Where showing the math adds credibility

**BAD contexts (skip):**
- In bullet lists or tables
- Passing mentions
- Already has equation within 10 lines

**Example addition:**
```markdown
The peace dividend would be {{< var peace_dividend_annual_societal_benefit >}} annually.

{{< var peace_dividend_annual_societal_benefit_latex >}}
```

### Phase 6: Validate Changes

**6.1 Run pre-render validation:**
```bash
.venv/Scripts/python.exe scripts/pre-render-validation.py <file.qmd>
```

**6.2 Regenerate preview to verify consistency:**
```bash
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file.qmd> --line-range "1-50"
```

**6.3 Check for any remaining issues:**
- All values consistent throughout file
- No `[MISSING: variable_name]` in preview
- No validation errors

### Phase 7: Generate Report

Summarize the review:

```markdown
## Review Complete: <filename>

### Preview
Generated: `_analysis/<basename>-preview.md`

### Replacements Made
| Line | Old Value | New Variable | Rendered |
|------|-----------|--------------|----------|
| 797 | `$2.4T` | `global_military_spending_annual_2024` | `$2.72T` |

### LaTeX Equations Added
- Line 1340: Added `iab_mechanism_benefit_cost_ratio_latex`

### Kept Hardcoded (Intentional)
- Copenhagen Consensus BCRs (citation-specific)
- `1%` treaty concept

### Validation
- Pre-render: PASSED
- All variables valid: YES
- Internal consistency: YES
```

## Important Rules

1. **ALWAYS generate preview first** - Understand before editing
2. **Use TodoWrite** - Track each replacement
3. **Verify semantic match** - Same number can mean different things
4. **Check `_latex` availability** - Don't leave outdated `$$` blocks
5. **Preserve citations** - Use `_cite` variables
6. **Run validation after** - Ensure no broken references
7. **NEVER replace `1%`** - Treaty concept, not a variable
8. **Skip citation-specific data** - Copenhagen BCRs, study figures stay hardcoded

## Quick Reference: Common Variables

```
# Core metrics
{{< var treaty_annual_funding >}}                    # $27.2B
{{< var global_military_spending_annual_2024 >}}    # $2.72T
{{< var global_annual_daly_burden >}}               # 2.88B DALYs
{{< var global_annual_direct_indirect_war_cost >}}  # $11.4T
{{< var global_household_wealth_usd >}}             # $454T

# IAB mechanism
{{< var iab_mechanism_benefit_cost_ratio >}}        # 230:1
{{< var iab_mechanism_annual_cost >}}               # $750M
{{< var iab_bootstrap_campaign_cost >}}             # $100M
{{< var victory_bond_annual_payout >}}              # $2.72B
{{< var iab_political_incentive_funding_annual >}}  # $2.72B

# With _latex suffix for equations
{{< var iab_mechanism_benefit_cost_ratio_latex >}}
{{< var treaty_peace_plus_rd_annual_benefits_latex >}}
```

## Related Commands

- `/pre-render-validate` - Validate all files before render
- `/validate-and-regenerate-parameters` - After editing parameters.py
