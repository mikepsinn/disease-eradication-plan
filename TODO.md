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

## Pending Tasks

### Final Steps
- [ ] Verify all changes render correctly in HTML
- [ ] Check that all parameter tooltips display correctly
- [ ] Commit changes with descriptive message

## Notes
- Many "hardcoded" numbers are actually referenced citations (good!)
- Sensitivity analysis ranges (50-95%, 3-8 years, etc.) may be intentional, not parameters
- Need to distinguish between:
  - External facts that should stay as citations (e.g., RECOVERY trial specifics)
  - Values we calculate that should be parameters
  - Intentional ranges for sensitivity analysis
