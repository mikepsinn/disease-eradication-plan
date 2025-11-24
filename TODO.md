# TODO: economics.qmd Improvements and Parameter System Optimization

## Pending Tasks from Current Session

### Parameter Metadata Verification

- [ ] **Audit parameter source_ref values in parameters.py**
  - **Issue**: Some calculated parameters may have incorrect or missing source_ref values
  - **Example**: `CURRENT_PATIENT_PARTICIPATION_RATE` has `source_ref="clinical-trial-eligibility-rate"` but this may not exist in references.qmd or may be inappropriate for a calculated parameter
  - **Action needed**:
    - Verify all parameters marked `source_type="external"` have valid references.qmd anchor IDs
    - Verify all parameters marked `source_type="calculated"` either have no source_ref or point to methodology files (not references.qmd)
    - Fix any mismatches between source_type and source_ref
  - **Impact**: Ensures generate-variables-yml.py creates correct links and tooltips

---

## High Priority - Replace Hardcoded Values with Calculations

- [ ] **SYSTEM_PROFIT_PER_LIFE_SAVED**
  - Should be calculated from treaty benefits and lives saved
  - Current: May be hardcoded
  - Suggested formula: `TREATY_TOTAL_COMPLETE_BENEFITS_ANNUAL / DISEASE_ERADICATION_DELAY_DEATHS_ANNUAL`
  - **Impact**: Key metric showing system generates profit (not cost) per life saved

---

## Medium Priority - Optional Improvements

### Add LaTeX Equations to Key Calculated Parameters

The following calculated parameters ARE used in economics.qmd but lack LaTeX equations:

- [ ] **GLOBAL_DISEASE_ECONOMIC_BURDEN_ANNUAL**
  - Formula: `MEDICAL_COSTS + PRODUCTIVITY_LOSS + MORTALITY_VALUE`
  - Used in economics.qmd to show total disease burden ($109.1T)
  - LaTeX: `$$Burden_{annual} = \$15.0T + \$0.03T + \$94.2T = \$109.1T$$`

- [ ] **TREATY_BENEFIT_MULTIPLIER_VS_VACCINES**
  - Formula: `TREATY_CONSERVATIVE_BENEFIT ÷ CHILDHOOD_VACCINATION_BENEFIT`
  - Shows treaty is 11x larger impact than all childhood vaccination programs
  - LaTeX: `$$Multiplier = \frac{\$77.28B}{\$6.6B} = 11.7\times$$`

- [ ] **GLOBAL_ANNUAL_DEATHS_CURABLE_DISEASES**
  - Formula: `GLOBAL_DAILY_DEATHS_CURABLE_DISEASES × 365`
  - Simple but could have LaTeX for completeness
  - LaTeX: `$$Deaths_{annual} = 150,000 \times 365 = 54.75M$$`

### Parameter Count Automation

- [ ] **Line 1722: Auto-generate parameter count**
  - Current: Manually maintained "422 parameters"
  - Actual count: 407 parameters (as of last generation)
  - Solution: Add variable `{{< var total_parameter_count >}}` to automatically update
  - Implementation: Update generate-variables-yml.py to export parameter count

---

## Low Priority - Nice to Have

### Documentation Improvements

- [ ] **Add inline comments explaining which parameters should remain hardcoded**
  - Some "calculated" parameters are intentionally hardcoded estimates (e.g., DFDA_UPFRONT_BUILD)
  - Add comments like: `# Intentional estimate, not calculated from other params`
  - This prevents confusion about which parameters need formulas

- [ ] **Create parameter dependency graph**
  - Visualize which parameters depend on which others
  - Help identify circular dependencies or missing calculations
  - Could be auto-generated from parameter formulas

### Code Quality

- [ ] **Add validation that calculated parameters use formulas**
  - In generate-variables-yml.py, warn if a parameter is marked `source_type="calculated"` but has a simple numeric value
  - Exception list for intentional estimates
  - Prevents accidental hardcoding

---

## Summary Statistics

- **Pending from current session:** 1 task
  - Audit parameter metadata (source_ref verification)
- **High priority items:** 1 remaining
  - SYSTEM_PROFIT_PER_LIFE_SAVED
- **Medium priority items:** 4 (optional LaTeX equations + parameter count)
- **Low priority items:** 3 (documentation and code quality)

## Why This Matters

### For Gates Foundation Credibility

All calculated parameters should be transparently derived from component assumptions to show:

1. **Intellectual honesty**: Not pulling numbers from thin air
2. **Auditability**: Reviewers can check the math
3. **Sensitivity**: Easy to test different assumptions
4. **Consistency**: Derived values automatically match components

---

## Implementation Notes

When replacing hardcoded values with calculations:

1. **Keep existing comment with hardcoded value** for reference
2. **Add formula parameter** to show the calculation
3. **Add LaTeX parameter** for visual representation
4. **Regenerate _variables.yml** after changes
5. **Verify the calculated value matches the previous hardcoded value** (or update documentation if it differs)
