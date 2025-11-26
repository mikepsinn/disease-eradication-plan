# TODO: Economics.qmd Parameterization & Cleanup

## Completed
- [x] Added SUFFERING_HOURS_ELIMINATED_TOTAL parameter (7.65T hours)
- [x] Replaced hardcoded "9.1 trillion hours" with variable
- [x] Added suffering hours to economics.qmd abstract
- [x] Fixed ">10x" research acceleration -> use research_acceleration_multiplier (25.7x)
- [x] Corrected description from "trial completion rates" -> "completed trials per year"
- [x] Replaced "35x cost increase" with drug_cost_increase_pre1962_to_current_multiplier (52x) - all 3 instances
- [x] Fixed variables inside link text (moved outside) - lines 869, 881
- [x] Replaced "144,000 physicians" with pre_1962_physician_count - all 3 instances
- [x] Removed redundant _cite variables (parameters auto-generate links)
- [x] Replaced "8 billion humans" with global_population_2024
- [x] Regenerated variables with generate-variables-yml.py
- [x] Created PRE_1962_VALIDATION_YEARS parameter (77 years) and replaced all instances
- [x] Created ANTIDEPRESSANT_TRIAL_EXCLUSION_RATE parameter (86.1%) and replaced all instances
- [x] Replaced GiveWell costs ($3,000-$5,000, $3,500) with existing parameters (givewell_cost_per_life_min/max/avg)
- [x] Added hyperlinks for RECOVERY trial details (49k patients, 185 hospitals, 33% efficacy) - kept as cited facts
- [x] Added hyperlinks for Ottawa Treaty (164 countries, 80%+) - kept as cited facts
- [x] Verified NIH 200 bureaucrats already has hyperlink - kept as cited fact

## Decision Log
**Parameterization Philosophy Applied:**
- Only created parameters for values used in **calculations** or referenced **multiple times**
- Did NOT create parameters for single-use cited facts (RECOVERY specifics, Ottawa Treaty details, NIH count)
- These are factual citations that should remain as inline references with hyperlinks

## Completed Tasks (This Session)
- [x] Created DRUG_DEVELOPMENT_COST_1980S parameter ($194M)
- [x] Created DRUG_COST_INCREASE_1980S_TO_CURRENT_MULTIPLIER parameter (13.4x)
- [x] Replaced "13-fold increase" with calculated parameter (line 889)
- [x] Reviewed sensitivity analysis ranges (50-95%, 3-8 years, 1-7%) - confirmed intentional, not parameters
- [x] Reviewed 3 Research Acceleration sections - confirmed intentional structure (summary/detail/technical)
- [x] Regenerated variables with generate-variables-yml.py

### Structure Review Results
**Research Acceleration Sections** - Intentional, well-structured:
- Line 227: Summary section (key numbers only)
- Line 693: Detailed explanation (main body)
- Line 1201: Technical details (appendix/sensitivity analysis)

These serve different audiences and detail levels - not duplicates.

## All Tasks Complete ✅

All parameterization work for economics.qmd is complete. The remaining verification steps are optional:
- Render the book to verify HTML output
- Review parameter tooltips in browser
- Commit when satisfied with changes

## Completed: Reader Hook & Impact Optimization

### Content Restructure (economics.qmd) ✅
- [x] **Fixed headline** - Changed from "150k deaths/day" (baseline rate) to actual impact:
  - Title: "How to Save 416 Million Lives for $0.13 Per DALY"
  - Description: "$1B investment generates $1.2 quadrillion in value"
  - Lead with ACTUAL IMPACT not baseline death rate
- [x] **Moved simple pitch to line 1** - "Shift 1% of military spending" immediately visible
- [x] **Created Gates Foundation comparison table** at top:
  - $0.13/DALY vs. $89/DALY bed nets (686× better)
  - 416M lives vs. 3M smallpox (138× scale)
  - Self-funding vs. perpetual fundraising
- [x] **Added comparison tables** for visual impact
- [x] **Collapsed academic abstract** into `<details>` section
- [x] **Verify research acceleration math** - Confirmed: 514 years in 20 years

### CSS Improvements (economics-overrides.css) ✅
- [x] Added `.stat-number-hero` class (5rem, elegant serif font)
- [x] Added `.stat-label-hero` class (1.5rem subtitle)
- [x] Added `.comparison-row-winner` styling (subtle cream background, accent border)
- [x] Added `.comparison-row-loser` styling (dimmed)
- [x] Added `.pull-quote` styling for emotional quotes
- [x] Added `.urgency-box` styling (subtle borders)
- [x] Added mobile responsiveness (@media queries)
- [x] **Fixed color scheme** - Replaced bright colors (red/green) with elegant book palette:
  - Uses CSS custom properties: `--book-heading`, `--book-accent`, `--book-light`, `--book-border`
  - Maintains classy black/white/cream aesthetic
  - Subtle emphasis instead of bright colors

### Key Learning
**WRONG**: "150,000 deaths per day" - that's just the baseline, not the intervention
**RIGHT**: "416 million lives saved" - that's the actual impact from 8.2-year acceleration

### Current Session TODO
- [x] Move "Mechanical Sequence" action plan section earlier (after RECOVERY proof, before Abstract)
- [x] Rename "The Mechanical Sequence" to clearer heading like "The 5-Step Implementation Plan"
- [x] Remove Gates Foundation-specific framing - make it general investor/funder pitch
- [x] Add scale comparisons (X Earths of GDP, value per human) - Created GLOBAL_GDP_ANNUAL_2024, TREATY_VALUE_VS_GLOBAL_GDP_RATIO, TREATY_VALUE_PER_PERSON parameters
- [ ] Collapse "Research Hypothesis" section (H₀/H₁ academic theater)
- [ ] Simplify "Key Findings" callout (still has number soup)

## Notes
- Many "hardcoded" numbers are actually referenced citations (good!)
- Sensitivity analysis ranges (50-95%, 3-8 years, etc.) may be intentional, not parameters
- Need to distinguish between:
  - External facts that should stay as citations (e.g., RECOVERY trial specifics)
  - Values we calculate that should be parameters
  - Intentional ranges for sensitivity analysis
