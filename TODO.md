# TODO: Fix Hardcoded Numbers in economics.qmd

## High Priority - Create Parameters

### ~~Economic Multiplier Effects~~ - DELETED
- [x] **Line 615:** Deleted the repetition (kept line 597 in earlier section)

### ~~Worst-Case ROI Consistency~~ - FIXED
- [x] **Lines 1480, 1556:** Replaced hardcoded `66:1 ROI` with `{{< var treaty_complete_roi_conditional_95th_percentile >}}`
- [x] Variable verified in parameters.py (TREATY_COMPLETE_ROI_CONDITIONAL_95TH_PERCENTILE = 66)

## High Priority - Find Sources and Add Citations

### Research Acceleration Claims
- [ ] **Line 196:** `2,000 years of medical advancement in 20 years`
  - Find calculation or source for this specific claim
  - Consider creating parameter if it's calculated

### Drug Development Cost Increases
- [ ] **Lines 807, 819:** `35-fold` / `35�` cost increase
  - Line 802 already cites it once, make consistent across all 3 mentions
  - Verify this matches the $74M � $2.6B calculation (if that gets resolved)

### Historical Validation Period
- [ ] **Lines 815, 825:** `80 years` of empirical validation (1883-1960)
  - Simple calculation (1960 - 1883 + 1 = 78, but text says 80)
  - Clarify if this is 78 or 80 years, or create parameter for consistency

### ~~DOT Value of Statistical Life~~ - DELETED
- [x] **Line 946:** ~~`$13.7M` DOT value~~ - Minor detail in peace dividend table, not essential
  - Delete this comparison from the table (just say "conservative" without specific DOT comparison)

### Clinical Trial Patient Exclusions
- [ ] **Line 1311:** `85% excluded` from trials
  - Find source for this exclusion percentage
  - Add citation to safety surveillance table

### Trial Accessibility Barriers
- [ ] **Lines 1334, 1344:** `500 miles` to university hospitals
  - Find source for typical trial travel distance
  - Add citations for both mentions

### ~~Historical Life Expectancy Gains~~ - DELETED
- [x] **Line 1408:** ~~`4 years/decade` life expectancy gains~~ - Removed unsourced claim
  - Revised to simply state "144,000 physicians tested treatments before 1962 regulatory shift"

### Medable Company Valuation
- [ ] **Line 1551:** `$521M` raised, `$2.1B` valuation
  - Find press release or financial database source for Medable
  - Add citation: `[Medable $521M raised, $2.1B valuation](../references.qmd#medable-funding-valuation)`
  - Add reference to references.qmd

### ~~Defense Sector Job Transitions~~ - DELETED
- [x] **Lines 1585-1592:** ~~Defense sector employment section~~ - Not relevant to Gates Foundation
  - Delete entire "Defense sector employment displacement" paragraph
  - Delete "Rent-seeking and administrative costs" paragraph
  - Gates doesn't care about defense contractor job transitions

## Medium Priority - Parameter Counts
- [ ] **Line 1722:** `422 parameters` count
  - Consider auto-generating this count from parameters.py
  - Update regularly or make it dynamic

## Already Fixed (For Reference)
 Line 200: `9.1 trillion hours` - cited
 Line 213: `$50100B` - cited
 Line 218: `49,000 patients`, `185 hospitals` - cited
 Line 486: `$3,000-10,000 per QALY` - cited
 Line 494: `$3,500 to save one life` - cited
 Line 802: `$2.6 billion` - cited
 Line 853: `185:1` ROI - uses variable
 Lines 967-976: Funding allocation percentages - use variables
 Line 986: Platform overhead - uses variables
 Line 1286: `$1,813` lobbying ROI - cited
 Line 1353: `200 NIH bureaucrats` - cited
 Line 1408: `144,000 physicians` - cited
 Line 1420: Bloom et al. `~5%`, `18�` - cited
 Line 1439: Patsopoulos `15-25%` - cited
 Line 1458: Publication bias `37%`, `94%`, `~$100 billion` - cited

## Known Issues (Cannot Verify)
� **Line 567:** `84,000 life-years lost` - See SOURCE_CITATIONS_SUMMARY.md
� **Lines 807, 827:** `$74M` pre-1962 drug cost - See SOURCE_CITATIONS_SUMMARY.md

---

## Summary Statistics
- **Total items to fix:** 5 major tasks (was 13, deleted 7, fixed 1)
- **Parameters to create:** 0 tasks (ROI consistency fixed!)
- **Sources to find:** 5 citations
- **Already fixed:** 17 items
- **Deleted as irrelevant:** 10 items (4 years/decade, defense jobs, DOT value, rent-seeking, economic multiplier repetition)

## Next Steps
1. Find sources for health/science claims (patient exclusions, trial barriers, historical data)
2. Research Medable company valuation ($521M raised, $2.1B valuation)

## Recent Changes Completed
✅ ROI consistency: Replaced hardcoded 66:1 with variable (lines 1480, 1556)
✅ Historical life expectancy claim "4 years/decade" (line 1407)
✅ Defense sector employment displacement paragraph (lines 1587)
✅ Rent-seeking overhead paragraph (line 1591)
✅ DOT $13.7M comparison in peace dividend table (line 946)
✅ Economic multiplier repetition (line 615)

## Why We Kept Political Feasibility Sections
✅ Victory Bonds, lobbying strategy, and political feasibility sections are ESSENTIAL
✅ The entire funding model depends on the 1% Treaty passing
✅ Gates needs to believe the implementation is realistic, not just scientifically sound
