# TODO: economics.qmd Improvements and Parameter System Optimization

## Recently Completed (Current Session)

### ✅ Bed Net Parameter Simplification - COMPLETED
- [x] **Simplified from 6 parameters to 3** - Reduced maintenance burden
  - ✅ Replaced `BED_NETS_COST_PER_DALY_MIN` ($78) and `_MAX` ($100) with single `BED_NETS_COST_PER_DALY` ($89 midpoint)
  - ✅ Replaced `TREATY_VS_BED_NETS_MULTIPLIER_MIN`/`_MAX` with single `TREATY_VS_BED_NETS_MULTIPLIER` (701x)
  - ✅ Replaced `TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER_MIN`/`_MAX` with single `TREATY_EXPECTED_VS_BED_NETS_MULTIPLIER` (70x)
  - ✅ Updated all 4 references in economics.qmd (abstract, key findings, decision makers box, political risk callout)
  - ✅ Regenerated _variables.yml

### ✅ LaTeX Equation Coverage - COMPLETED
- [x] **Verified all top 5 priority LaTeX equations are in place**
  - ✅ Cost per DALY with political risk (lines 543, 547)
  - ✅ Deaths avoided (line 233)
  - ✅ Research acceleration (lines 221, 223, 1202)
  - ✅ ROI breakdown (7 locations)
  - ✅ Peace dividend (line 994)
  - ✅ Total: 21 LaTeX equation placements in economics.qmd
  - ✅ Coverage: 138/234 calculated parameters have LaTeX equations (59%)

### ✅ Eventually Avoidable Death Percentage - COMPLETED
- [x] **Updated disease burden model** (from previous session)
  - ✅ Created `FUNDAMENTALLY_UNAVOIDABLE_DEATH_PCT` (7.91%) parameter
  - ✅ Created `EVENTUALLY_AVOIDABLE_DEATH_PCT` (92.09%) parameter
  - ✅ Updated `DISEASE_ERADICATION_DELAY_DEATHS_TOTAL` from 449M to 413.4M lives
  - ✅ Added "Why Eventually Avoidable Matters" callout box in economics.qmd
  - ✅ Updated aging_related research acceleration potential from 0.85 to 0.99

### ✅ Political Risk Accounting - COMPLETED
- [x] **Created expected cost per DALY parameter** (from previous session)
  - ✅ Added `POLITICAL_SUCCESS_PROBABILITY_CONSERVATIVE` (10%)
  - ✅ Created `TREATY_EXPECTED_COST_PER_DALY_CONSERVATIVE` ($1.27/DALY at 10% success)
  - ✅ Added "But What If It Doesn't Pass?" callout box with LaTeX equations
  - ✅ Updated abstract to show both conditional and expected cost-effectiveness

---

## High Priority - Replace Hardcoded Values with Calculations

### ⚠️ QUESTION: Do We Even Need Component Multipliers?

**Discovery**: The component multipliers (`RECRUITMENT_SPEED_MULTIPLIER`, `TRIAL_COMPLETION_SPEED_MULTIPLIER`, `SIMULTANEOUS_TRIALS_MULTIPLIER`) are **only used for display** - they don't drive any actual calculations.

**Current Usage**:
- ✅ Used in 2 tables in economics.qmd (lines 691-693, 1194-1196) to show breakdown
- ✅ Used to calculate `COMPLETED_TRIALS_MULTIPLIER_THEORETICAL_MAX` (560x)
- ❌ NOT used in any actual model calculations
- ❌ The model uses `RESEARCH_ACCELERATION_MULTIPLIER = 115` (hardcoded separately)
- ❌ Theoretical max (560x) is only shown for display, never used in analysis

**Options**:
1. **DELETE them** - Simplify to just "115x from multiple acceleration factors"
   - Pros: Fewer parameters to maintain, simpler model, less confusion
   - Cons: Less transparency about HOW 115x is achieved

2. **KEEP them but as display-only** - Accept they're for credibility/transparency, not calculations
   - Pros: Shows the breakdown, helps readers understand the mechanism
   - Cons: Maintenance burden for values that don't affect outcomes

3. **MAKE them drive the calculation** - Have them multiply together to get 115x
   - Pros: Single source of truth, component changes auto-update total
   - Cons: More complexity, need to justify each component value

- [ ] **DELETE component multipliers (recommended)**
  - Remove: `RECRUITMENT_SPEED_MULTIPLIER` (line 1213)
  - Remove: `TRIAL_COMPLETION_SPEED_MULTIPLIER` (line 1225)
  - Remove: `SIMULTANEOUS_TRIALS_MULTIPLIER` (line 1235)
  - Remove: `COMPLETED_TRIALS_MULTIPLIER_ACTUAL` (line 1257)
  - Remove: `COMPLETED_TRIALS_MULTIPLIER_THEORETICAL_MAX` (if it exists)
  - Remove: `COMPLETION_RATE_IMPROVEMENT_MULTIPLIER` (display-only value)

- [ ] **Update economics.qmd after deletion**
  - Simplify or remove breakdown tables (lines 689-697, 1192-1198)
  - Replace with narrative: "The 115x acceleration comes from multiple factors: faster recruitment (RECOVERY trial showed 3 weeks for 11,000 patients), faster completion (3-12 months vs. 3-5 years), more simultaneous trials (200,000 vs. 10,000), and higher completion rates (95% vs. 60%)."
  - Keep the 115x multiplier as the core metric
  - **Benefit**: Simpler model, fewer parameters, less maintenance, same outcome

---

### Research Acceleration Multipliers

**Issue**: Several key multipliers are marked as `source_type="calculated"` but use hardcoded values instead of formulas.

- [ ] **Line 1189: RESEARCH_ACCELERATION_MULTIPLIER = 115**
  - Should be: `FUNDING_MULTIPLIER × TIME_REDUCTION_MULTIPLIER`
  - Current: Hardcoded 115
  - Formula: 1.40 (funding increase) × 82 (time/cost reduction) = 115
  - Has LaTeX equation but not a calculated value
  - **Impact**: Core metric for Gates Foundation, should be transparently calculated

- [ ] **Line 1213: RECRUITMENT_SPEED_MULTIPLIER = 25** ⚠️ **MIGHT DELETE** (see above)
  - Only used for display in tables, not calculations
  - IF we keep it: Should be calculated from RECOVERY trial data (3 weeks for 11,000 patients vs. 6-18 months for 100)
  - Current: Hardcoded 25
  - Suggested formula: `(DFDA_LARGE_TRIAL_SIZE / TRADITIONAL_SMALL_TRIAL_SIZE) / (DFDA_RECRUITMENT_WEEKS / TRADITIONAL_RECRUITMENT_MONTHS_MID × 4.33)`

- [ ] **Line 1225: TRIAL_COMPLETION_SPEED_MULTIPLIER = 10** ⚠️ **MIGHT DELETE** (see above)
  - Only used for display in tables, not calculations
  - IF we keep it: Should be calculated from trial duration comparison
  - Current: Hardcoded 10
  - Suggested formula: `(TRADITIONAL_TRIAL_DURATION_YEARS × 12) / DFDA_TRIAL_DURATION_MONTHS_MAX`
  - Example: (4 years × 12) / 12 months = 4x (conservative) or (4 × 12) / 6 months = 8x (aggressive)

- [ ] **Line 1235: SIMULTANEOUS_TRIALS_MULTIPLIER = 20** ⚠️ **MIGHT DELETE** (see above)
  - Only used for display in tables, not calculations
  - IF we keep it: Should be calculated from capacity analysis
  - Current: Hardcoded 20
  - Suggested formula: `DFDA_ACTIVE_TRIALS / CURRENT_ACTIVE_TRIALS`
  - Example: 200,000 / 10,000 = 20x

- [ ] **Line 1257: COMPLETED_TRIALS_MULTIPLIER_THEORETICAL_MAX = 560** ⚠️ **MIGHT DELETE** (see above)
  - Only used for display (showing theoretical max vs. conservative 115x), never used in actual calculations
  - IF we keep it: Should be calculated from component multipliers
  - Current: Hardcoded 180 (wait, should be 560?)
  - Theoretical formula: 25 × 10 × 1.6 × 1.4 = 560x (but we use conservative 115x in practice)
  - **Note**: Check if this is actually 180 or 560 - there might be confusion here

### Cost-Effectiveness Calculations

- [ ] **Line 5664: SYSTEM_PROFIT_PER_LIFE_SAVED = 5,870,000**
  - Should be calculated from treaty benefits and lives saved
  - Current: Hardcoded $5.87M
  - Suggested formula: `TREATY_TOTAL_COMPLETE_BENEFITS_ANNUAL / DISEASE_ERADICATION_DELAY_DEATHS_ANNUAL`
  - **Impact**: Key metric showing system generates profit (not cost) per life saved

### Trial Capacity Parameters

- [ ] **Line 1056: DFDA_TRIALS_PER_YEAR_CAPACITY = 380,000**
  - Should be: `CURRENT_TRIALS_PER_YEAR × RESEARCH_ACCELERATION_MULTIPLIER`
  - Current: Hardcoded 380,000
  - Formula: 3,300 × 115 = 379,500 ≈ 380,000
  - **Impact**: Minor, but should be consistent with multiplier

- [ ] **Line 1091: DFDA_ACTIVE_TRIALS = 200,000**
  - Should be: `CURRENT_ACTIVE_TRIALS × SIMULTANEOUS_TRIALS_MULTIPLIER`
  - Current: Hardcoded 200,000
  - Formula: 10,000 × 20 = 200,000
  - **Impact**: Should derive from multiplier

### Lower Priority Hardcoded Values

Many other parameters are marked "calculated" with hardcoded values, but these are likely intentional estimates or assumptions. Examples:
- DFDA_UPFRONT_BUILD = $40M (reasonable estimate)
- CAMPAIGN_MEDIA_BUDGET_MIN = $500M (scenario planning)
- DFDA_SMALL_TRIAL_SIZE = 1,000 (design assumption)

**Recommendation**: Focus on the parameters above that are derived from other parameters, rather than estimates.

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

## Already Fixed (For Reference)

### From Previous Sessions
✅ Line 200: `9.1 trillion hours` - cited
✅ Line 213: `$50–100B` - cited
✅ Line 218: `49,000 patients`, `185 hospitals` - cited
✅ Line 486: `$3,000-10,000 per QALY` - cited
✅ Line 494: `$3,500 to save one life` - cited
✅ Line 802: `$2.6 billion` - cited
✅ Line 853: `185:1` ROI - uses variable
✅ Lines 967-976: Funding allocation percentages - use variables
✅ Line 986: Platform overhead - uses variables
✅ Line 1286: `$1,813` lobbying ROI - cited
✅ Line 1353: `200 NIH bureaucrats` - cited
✅ Line 1408: `144,000 physicians` - cited
✅ Line 1420: Bloom et al. `~5%`, `18×` - cited
✅ Line 1439: Patsopoulos `15-25%` - cited
✅ Line 1458: Publication bias `37%`, `94%`, `~$100 billion` - cited
✅ Research acceleration "2,000 years": Created parameter, actual value 2,300 years (115x × 20 years)
✅ Trial accessibility barriers: Added comprehensive geographic barriers reference
✅ 86.1% exclusion: Updated all 8 references with hyperlinks to sourced data
✅ ROI consistency: Replaced hardcoded 66:1 with variable (lines 1480, 1556)
✅ Medable valuation: Added hyperlink to existing reference
✅ 35-fold cost increase: Added hyperlinks at lines 806, 818
✅ Historical validation "77 years": Corrected from "80 years"

### Deleted as Irrelevant
✅ Historical life expectancy claim "4 years/decade" (line 1407)
✅ Defense sector employment displacement paragraph (lines 1587)
✅ Rent-seeking overhead paragraph (line 1591)
✅ DOT $13.7M comparison in peace dividend table (line 946)
✅ Economic multiplier repetition (line 615)

---

## Known Issues (Cannot Verify)

⚠️ **Line 567:** `84,000 life-years lost` - See SOURCE_CITATIONS_SUMMARY.md
⚠️ **Lines 807, 827:** `$74M` pre-1962 drug cost - See SOURCE_CITATIONS_SUMMARY.md

These claims don't have easily verifiable sources but are reasonable estimates based on historical data.

---

## Summary Statistics

- **High priority items:** 10 (hardcoded values that should be calculations)
- **Medium priority items:** 4 (optional LaTeX equations + parameter count)
- **Low priority items:** 3 (documentation and code quality)
- **Total parameters:** 407
- **Calculated parameters:** 234 (57%)
- **Calculated params WITH LaTeX:** 138 (59% of calculated)
- **Calculated params marked as calculated but hardcoded:** 93 (40%)

## Why This Matters

### For Gates Foundation Credibility

The hardcoded multipliers (RESEARCH_ACCELERATION_MULTIPLIER = 115, etc.) are **core claims** in the proposal. These should be transparently calculated from component assumptions to show:

1. **Intellectual honesty**: Not pulling numbers from thin air
2. **Auditability**: Reviewers can check the math
3. **Sensitivity**: Easy to test different assumptions
4. **Consistency**: Derived values automatically match components

### Priority Order

1. **RESEARCH_ACCELERATION_MULTIPLIER** - Most critical (headline claim)
2. **Component multipliers** (recruitment, completion, simultaneous) - Support the headline
3. **SYSTEM_PROFIT_PER_LIFE_SAVED** - Key narrative point (profit, not cost)
4. **Trial capacity** - Should derive from multipliers
5. **LaTeX equations** - Nice to have for key parameters
6. **Parameter count** - Minor QoL improvement

---

## Implementation Notes

When replacing hardcoded values with calculations:

1. **Keep existing comment with hardcoded value** for reference
2. **Add formula parameter** to show the calculation
3. **Add LaTeX parameter** for visual representation
4. **Regenerate _variables.yml** after changes
5. **Verify the calculated value matches the previous hardcoded value** (or update documentation if it differs)

Example:
```python
# OLD:
RESEARCH_ACCELERATION_MULTIPLIER = Parameter(
    115,
    source_type="calculated",
    ...
)

# NEW:
RESEARCH_ACCELERATION_MULTIPLIER = Parameter(
    FUNDING_INCREASE_MULTIPLIER * TIME_REDUCTION_MULTIPLIER,
    source_type="calculated",
    formula="FUNDING_MULTIPLIER × TIME_REDUCTION",
    latex=r"$$115\times = 1.40 \times 82$$",
    ...
)  # 115x (was hardcoded, now calculated: 1.40 × 82 = 114.8 ≈ 115)
```
