# TODO: Replace Hard-Coded Numbers with Variables

This checklist tracks replacement of hard-coded numbers in `knowledge/economics/economics.qmd` with variables from `_variables.yml` or new parameters in `dih_models/parameters.py`.

## ⚠️ Important Notes

### Outdated Numbers
**Some numbers in `economics.qmd` may be outdated and need verification against current values in `dih_models/parameters.py`.**

When replacing hard-coded numbers:
1. **First verify** the number matches the current parameter value in `dih_models/parameters.py`
2. If the number is **different**, update the parameter in `parameters.py` with the correct value
3. If the number is **correct**, proceed with replacement
4. If the number is **intentionally different** (e.g., historical reference), document why

### LaTeX Equations
**All LaTeX equations should use `_latex` variables from `_variables.yml` when available.**

This ensures:
- Consistency across documents
- Automatic updates when parameters change
- Proper formatting and citation links

## Workflow

**⚠️ IMPORTANT: Use the systematic process in `SYSTEMATIC_REPLACEMENT_PROCESS.md`**

The systematic process uses semantic search to find appropriate parameters and decision criteria to determine when to create new parameters.

### Quick Workflow

1. **Extract** hard-coded number with context (3-5 lines before/after)
2. **Categorize** by type, context, unit, scope
3. **Search** semantically for existing parameters using:
   - `codebase_search()` for concept-based search
   - `grep` for value-based search
   - Parameter `keywords` fields for discovery
4. **Verify** value, context, unit match
5. **Decide** using decision tree:
   - ✅ Use existing parameter (value and context match)
   - 🔄 Update parameter value (value outdated)
   - ⚠️ Create new parameter (different context/calculation)
   - ✅ Keep as literal (example, threshold, historical reference)
6. **Replace** in economics.qmd with `{{< var parameter_name >}}`
7. **Regenerate** `_variables.yml` if parameter was created/updated: `python scripts/generate-variables-yml.py`
8. **Verify** rendering with `quarto preview`

### Automated Help

Run `python scripts/find-parameter-matches.py` to get suggestions for parameter matches (demonstration script).

## Priority 1: High-Impact Numbers (ROI, Key Metrics)

### ROI and Investment Returns
- [ ] Line 87: `$100B` - "NPV benefit exceeds $100B" → **CREATE**: `npv_benefit_threshold_billion`
- [ ] Line 479: `$1` - "You spend $1" → **CREATE**: `roi_example_dollar_amount` or use literal (example)
- [ ] Line 485: `$1 billion` - "You spend $1 billion once" → **CREATE**: `roi_example_billion_investment` or use literal (example)
- [ ] Line 716: `1:1` - "ROI > 1:1" → Use literal (threshold)
- [ ] Line 1451: `230:1` and `620:1` - Diminishing returns ROI → **CREATE**: `roi_with_diminishing_returns_conservative`, `roi_with_diminishing_returns_complete`


### Peace Dividend
(All items completed - see "Recently Completed" section)

## Priority 2: Research Acceleration and Trial Metrics

### Research Acceleration Multipliers
- [ ] Line 89: `>10×` - ">10× increase in trial completion rates" → **CREATE**: `research_acceleration_minimum_multiplier`
- [ ] Line 632-636: Table multipliers `25×`, `10×`, `20×`, `1.6×`, `1.4×` → **CREATE**: `research_acceleration_recruitment_multiplier`, `research_acceleration_completion_speed_multiplier`, `research_acceleration_simultaneous_trials_multiplier`, `research_acceleration_completion_rate_multiplier`, `research_acceleration_funding_multiplier`
- [ ] Line 638: `25 × 10 × 1.6 × 1.4 = 560×` - "Theoretical maximum" → **CREATE**: `research_acceleration_theoretical_maximum`
- [ ] Line 1123: `10-20×` - "10-20× more discoveries" → **CREATE**: `research_acceleration_discoveries_multiplier_range`
- [ ] Line 1153-1157: Table multipliers (duplicate of 632-636) → Same variables as above
- [ ] Line 1162: `25 × 10 × 1.6 × 1.4 = 560` - in formula → Same as line 638
- [ ] Line 1174: `20-40x` - "20-40x" → **CREATE**: `drug_approvals_multiplier_range`
- [ ] Line 1175: `82x` - "82x cost reduction" → Check: `trial_cost_reduction_factor`
- [ ] Line 1611: `115×` - "Increasing trial demand by 115×" → Check: `research_acceleration_multiplier`
- [ ] Line 1611: `82×` - "82× cheaper via automation" → Check: `trial_cost_reduction_factor`
- [ ] Line 1615: `115×` - "115× more trials" → Check: `research_acceleration_multiplier`

### Trial Costs and Economics
- [ ] Line 497: `$3,000-10,000` - "Most successful health programs cost $3,000-10,000 per QALY" → **CREATE**: `standard_qaly_cost_range_usd`
- [ ] Line 505: `$3,500` - "Please donate $3,500 to save one life" → **CREATE**: `givewell_cost_per_life_saved_usd` (check if exists)
- [ ] Line 1175: `$41,000` - "From [$41,000 cost per patient]" → Check: `traditional_phase3_cost_per_patient_fda_example_41k`
- [ ] Line 1198-1199: `$3,000-$5,000` - GiveWell costs → Check: `givewell_cost_per_life_min`, `givewell_cost_per_life_max`
- [ ] Line 1611: `$41,000` and `$500` - Trial cost comparison → Check: `traditional_phase3_cost_per_patient_fda_example_41k`, `recovery_trial_cost_per_patient`

### RECOVERY Trial Data
- [ ] Line 225: `49,000` - "enrolled 49,000 patients" → **CREATE**: `recovery_trial_patients_enrolled`
- [ ] Line 225: `185` - "across 185 hospitals" → **CREATE**: `recovery_trial_hospitals_count`
- [ ] Line 225: `33%` - "reducing COVID deaths 33%" → **CREATE**: `recovery_trial_dexamethasone_mortality_reduction_pct`
- [ ] Line 252: `<10` - "RECOVERY collected <10 core outcomes" → **CREATE**: `recovery_trial_core_outcomes_count`
- [ ] Line 1331: `6` and `47,000` and `3 months` - "tested 6 treatments on 47,000 patients in 3 months" → **CREATE**: `recovery_trial_treatments_tested`, `recovery_trial_patients_total`, `recovery_trial_duration_months` (check if exists)

## Priority 3: Time Periods and Delays

### Regulatory Delays
- [ ] Line 1319: `8 years` - "wait 8 years to prove aspirin helps headaches" → Check: `efficacy_lag_years`

### Historical Periods
- [ ] Line 150: `50 years` - "Diseases eradicated in past 50 years" → **CREATE**: `disease_eradication_lookback_years`
- [ ] Line 155: `1961` - Eisenhower quote year → Use literal (historical reference)
- [ ] Line 202: `2,000 years` and `20 years` - "2,000 years of medical advancement in 20 years" → **CREATE**: `research_acceleration_equivalent_years`, `research_acceleration_actual_years`
- [ ] Line 876: `2024` - "As of 2024" → Use literal (current year reference)
- [ ] Line 90: `year 3` - "by year 3 of implementation" → **CREATE**: `self_funding_threshold_year`

### Trial Durations
- [ ] Line 632: `6-18 months` and `3 weeks` - Recruitment speed → **CREATE**: `traditional_trial_recruitment_duration_months`, `pragmatic_trial_recruitment_duration_weeks`
- [ ] Line 633: `3-5 years` and `3-12 months` - Trial completion speed → **CREATE**: `traditional_trial_completion_duration_years`, `pragmatic_trial_completion_duration_months`
- [ ] Line 1135: `3-5 year` - "3-5 year duration" → Same as above
- [ ] Line 1138: `6-18 months` and `100 patients` - "6-18 months to recruit 100 patients" → Same as above
- [ ] Line 1144: `3-12 month` - "3-12 month duration" → Same as above
- [ ] Line 1147: `3 weeks` - "3 weeks to recruit" → Same as above
- [ ] Line 1153-1154: Duplicate of above → Same variables
- [ ] Line 1333: `40+ years` and `2-3 years` - Safety detection → **CREATE**: `traditional_safety_detection_years`, `pragmatic_safety_detection_years`
- [ ] Line 1359: `6 months` - "wait 6 months" → **CREATE**: `traditional_trial_wait_time_months`
- [ ] Line 1717: `36 months` - "Timeline: [36 months]" → **CREATE**: `treaty_implementation_timeline_months`

### Adoption and Implementation
- [ ] Line 709: `3-8 years` - "adoption timeline (3-8 years)" → Check: `dfda_npv_adoption_ramp_years`
- [ ] Line 738: `10` - in formula "sum from t=1 to 10" → Check: `npv_time_horizon_years`

## Priority 4: Economic Multipliers and Percentages

### Economic Multipliers
- [ ] Line 457: `0.5-1.0×` - "economic multiplier effects of 0.5-1.0×" → **CREATE**: `military_spending_multiplier_range`
- [ ] Line 457: `2.0-3.0×` - "multiplier effects of 2.0-3.0×" → **CREATE**: `medical_research_multiplier_range`
- [ ] Line 457: `50 cents to a dollar` - "you get 50 cents to a dollar" → **CREATE**: `military_spending_multiplier_min`, `military_spending_multiplier_max`
- [ ] Line 457: `$2-3` - "you get $2-3 of economic value" → **CREATE**: `medical_research_multiplier_min`, `medical_research_multiplier_max`
- [ ] Line 459: `0.5×` and `2.0×` - "Moving money from 0.5× returns to 2.0× returns" → Use variables from above
- [ ] Line 592: `0.5-1.0×` and `2.0-3.0×` - multiplier effects → Same as above
- [ ] Line 610: `2.0-3.0×` and `0.5-1.0×` - multiplier effects → Same as above

### Cost Reduction Percentages
- [ ] Line 104: `50-95%` - "Reduces per-patient costs by 50-95%" → **CREATE**: `trial_cost_reduction_pct_range`
- [ ] Line 709: `50-95%` - "Cost reduction (50-95%)" → Same as above
- [ ] Line 1414: `50-70%` - "Conservative estimate uses 50-70% cost reduction" → **CREATE**: `trial_cost_reduction_pct_conservative_range`
- [ ] Line 824: `50-95%` and `97%+` - cost reduction estimates → Check: `trial_cost_reduction_pct`, create `trial_cost_reduction_pct_historical_max`
- [ ] Line 1457: `15-25%` - "pragmatic trials often find 15-25% smaller effect sizes" → **CREATE**: `pragmatic_trial_effect_size_reduction_pct_range`

### Other Percentages
- [ ] Line 88: `$0` - "ICER < $0/QALY" → Use literal (threshold)
- [ ] Line 142: `0.053%` - "That's 0.053% of the disease burden" → **CREATE**: `disease_burden_research_funding_pct`
- [ ] Line 145: `0.053%` - in formula → Same as above
- [ ] Line 572: `17%` - "baseline: 17% of total" → **CREATE**: `qaly_gain_prevention_care_pct`
- [ ] Line 580: `60%` - "baseline: 60% of total" → **CREATE**: `qaly_gain_rare_diseases_pct`
- [ ] Line 622: `$0` - "$0 to {{< var peace_dividend_conflict_reduction >}}" → Use literal
- [ ] Line 624: `0%` and `>1%` - "A 1% spending reduction may yield anywhere from 0% to >1%" → Use literals (range description)
- [ ] Line 730: `1%` - discount rate → Check: `roi_discount_1pct` (if exists)
- [ ] Line 732: `3%` - "3% (baseline)" → Check: `npv_discount_rate_standard`
- [ ] Line 733: `5%` - discount rate → Check: `roi_discount_5pct` (if exists)
- [ ] Line 734: `7%` - discount rate → Check: `roi_discount_7pct` (if exists)
- [ ] Line 709: `1-7%` - "discount rate (1-7%)" → **CREATE**: `discount_rate_sensitivity_range_pct`
- [ ] Line 709: `5-60%` - "political success probability (5-60%)" → **CREATE**: `political_success_probability_range_pct`
- [ ] Line 709: `0.7-1.3×` - "QALY gains (0.7-1.3× baseline)" → **CREATE**: `qaly_gains_sensitivity_range`
- [ ] Line 713: `95%` - "95% of simulations" → Use literal (statistical threshold)
- [ ] Line 714: `95%` - "95% of simulations" → Use literal (statistical threshold)
- [ ] Line 716: `10,000` - "All 10,000 simulations" → **CREATE**: `monte_carlo_simulation_count`
- [ ] Line 970: `~$24.4B` - "patient subsidies (~$24.4B)" → Check: `dih_treasury_trial_subsidies_annual`
- [ ] Line 972: `89.8%` - "Patient Trial Subsidies (89.8%)" → **CREATE**: `treaty_funding_patient_subsidies_pct`
- [ ] Line 977: `10%` - "Victory Bond Payouts (10%)" → **CREATE**: `treaty_funding_victory_bonds_pct`
- [ ] Line 979: `0.15%` - "Coordination Platform (0.15%)" → **CREATE**: `treaty_funding_platform_pct`
- [ ] Line 989: `90%` - "90% of treaty funding" → **CREATE**: `treaty_funding_direct_to_patients_pct`
- [ ] Line 1134: `60%` - "60% completion rate" → Check: `current_trial_abandonment_rate` (inverse)
- [ ] Line 1143: `95%` - "95% completion rate" → Check: `dfda_trial_completion_rate`
- [ ] Line 1156: `60%` and `95%` - in table → Same as above
- [ ] Line 1326: `85%` - "85% excluded" → **CREATE**: `traditional_trial_exclusion_rate_pct`
- [ ] Line 1328: `37%` and `100%` - Publication rates → **CREATE**: `traditional_trial_negative_publication_rate_pct`, `pragmatic_trial_publication_rate_pct`
- [ ] Line 1351: `85%` - "Trials exclude 85% of actual patients" → Same as line 1326
- [ ] Line 1451: `50%` - "Even applying 50% diminishing returns" → Use literal (example)
- [ ] Line 1476: `37%` and `94%` - Publication bias → Same as line 1328
- [ ] Line 1609: `10-20%` - "suggests 10-20% overhead" → **CREATE**: `funding_program_overhead_pct_range`

## Priority 5: Dollar Amounts and Financial Values

### Large Dollar Amounts
- [ ] Line 220: `$50–100B` - "$50–100B saved per year" → **CREATE**: `annual_savings_range_billion`
- [ ] Line 402: `$1B` - "A $1B invested here" → Use literal (example)
- [ ] Line 411: `$1B` - "any other known use of $1B" → Use literal (example)
- [ ] Line 876: `$100B` - "$100B annual climate finance pledge" → Use literal (reference to external commitment)
- [ ] Line 989: `$40M` and `$24.4B` - "$40M) compared to patient subsidies ($24.4B)" → Check: `dfda_annual_opex`, `dih_treasury_trial_subsidies_annual`
- [ ] Line 1195: `$1.1M` - "$1.1M profit" → Check: `treaty_dfda_net_benefit_per_life_saved`
- [ ] Line 1301: `$1,813` and `$1` - "Defense lobbyists currently get $1,813 back for every $1 spent" → **CREATE**: `defense_lobbying_roi_ratio`
- [ ] Line 1605: `$600k` - "assuming $600k cost per job" → **CREATE**: `defense_sector_job_cost_usd`
- [ ] Line 1605: `$2-4B` - "Transition costs estimated at $2-4B annually" → **CREATE**: `defense_sector_transition_cost_annual_billion`
- [ ] Line 1613: `$27.2B` - "Does $27.2B in new medical research" → Check: `treaty_annual_funding`

### Historical Drug Costs
- [ ] Line 798: `$74 million` - "Pre-1962 system: [$74 million per drug]" → **CREATE**: `pre_1962_drug_development_cost_usd`
- [ ] Line 799: `$2.6 billion` and `35×` - "Post-1962 system: $2.6 billion per drug average, a **35× cost increase**" → **CREATE**: `post_1962_drug_development_cost_usd`, `drug_cost_increase_multiplier`
- [ ] Line 824: `$74M` and `$2.6B` - cost reduction estimates → Same as above
- [ ] Line 949: `$13.7M` - "conservative vs. DOT $13.7M" → **CREATE**: `dot_value_of_statistical_life_usd`
- [ ] Line 953: `$1,384` - "108.4M displaced persons × $1,384/year" → **CREATE**: `refugee_support_cost_per_person_annual_usd`
- [ ] Line 1476: `~$100 billion` - "~$100 billion annually wasted" → **CREATE**: `wasted_spending_failed_experiments_annual_billion`

### Small Dollar Amounts (Examples/Analogies)
- [ ] Line 153: `$40` and `$1` - "spending $40 on gasoline for a fire and $1 on a fire extinguisher" → Use literal (analogy)
- [ ] Line 145: `$68\text{B}` and `$128.6\text{T}` - in formula → Check: `global_med_research_spending`, `global_disease_economic_burden_annual`

## Priority 6: Counts and Quantities

### Patient and Trial Counts
- [ ] Line 632: `100 patients` - "6-18 months for 100 patients" → **CREATE**: `traditional_trial_recruitment_target_patients`
- [ ] Line 1138: `100 patients` - "6-18 months to recruit 100 patients" → Same as above
- [ ] Line 1153: `100 patients` - in table → Same as above
- [ ] Line 1155: `10,000` and `200,000` - "10,000 active trials | 200,000 active trials" → Check: `current_active_trials`, `dfda_active_trials`
- [ ] Line 1325: `100-300` - "Sample size | 100-300 patients" → **CREATE**: `traditional_trial_sample_size_range`
- [ ] Line 1325: `10,000-100,000+` - "10,000-100,000+ patients" → **CREATE**: `pragmatic_trial_sample_size_range`
- [ ] Line 1362: `240 times` - "240 times more willing participants" → **CREATE**: `pragmatic_trial_participation_multiplier`

### Other Counts
- [ ] Line 150: `Zero` - "Diseases eradicated in past 50 years: **Zero**" → Use literal (factual statement)
- [ ] Line 189: `Phase 2/3/4` - "Phase 2/3/4 trials" → Use literal (trial phase names)
- [ ] Line 206: `9.1 trillion` - "9.1 trillion hours of human suffering" → **CREATE**: `annual_suffering_hours_eliminated_trillion`
- [ ] Line 258: `15–40` - "15–40 'NIH equivalents'" → **CREATE**: `nih_equivalents_research_capacity_range`
- [ ] Line 275: `19 times` and `20` - "can still end civilization 19 times instead of 20" → Use literal (analogy)
- [ ] Line 876: `196` - "196 parties ratified" → Use literal (historical fact)
- [ ] Line 953: `108.4M` - "108.4M displaced persons" → Check if exists in references
- [ ] Line 1174: `50` and `1,000` - "From 50 drug approvals/year → 1,000-{{< var dfda_drug_approvals_per_year_high >}}" → **CREATE**: `baseline_drug_approvals_per_year`
- [ ] Line 1368: `200` and `8 billion` - "200 NIH bureaucrats decide what 8 billion humans" → **CREATE**: `nih_decision_makers_count`, use literal for `8 billion` (global population)

## Priority 7: Ratios and Comparisons

### Death Ratios
- [ ] Line 172: `54.75\text{M}` and `3{,}000` and `18{,}274:1` - in formula → Check: `global_annual_deaths_curable_diseases`, **CREATE**: `annual_terrorism_deaths`, `disease_vs_terrorism_deaths_ratio`
- [ ] Line 178: `54.75\text{M}` and `400{,}000` and `137:1` - in formula → Check: `global_annual_deaths_curable_diseases`, `global_annual_conflict_deaths_total`, **CREATE**: `disease_vs_conflict_deaths_ratio`

## Priority 8: Sensitivity Analysis Parameters

- [ ] Line 709: All sensitivity ranges already covered above
- [ ] Line 713-714: Monte Carlo results already covered above
- [ ] Line 716: `2.7:1` - "5th percentile expected ROI of 2.7:1" → Already covered above

## Priority 9: LaTeX Equation Replacements

Replace hard-coded LaTeX equations with `{{< var variable_name_latex >}}` from `_variables.yml`.


### NPV Equations
- [ ] Line 517: `\text{NPV}(\text{Costs}) = C_{0} + \sum_{t=1}^{T} \frac{C_{\text{op}}(t)}{(1 + r)^t}` → **CREATE**: `npv_costs_formula_latex`
- [ ] Line 533: `\text{NPV}(\text{Benefits}) = \sum_{t=1}^{T} \frac{S(t)}{(1 + r)^t}` → **CREATE**: `npv_benefits_formula_latex`
- [ ] Line 539: `\text{ROI} = \frac{\text{NPV}(\text{Benefits})}{\text{NPV}(\text{Costs})}` → Check: `dfda_roi_rd_only_latex` or use general formula
- [ ] Line 738: `\text{NPV} = \sum_{t=1}^{10} \frac{B_t - C_t}{(1 + r)^t}` → **CREATE**: `npv_general_formula_latex` (verify `10` matches `npv_time_horizon_years`)

### Expected Value Equations
- [ ] Line 839: `E[\text{ROI}] = P(\text{success}) \times \text{ROI}_{\text{if successful}}` → **CREATE**: `expected_roi_formula_latex`

### Disease Burden and Ratios
(All items completed - see "Recently Completed" section)

### QALY and Lives Saved Equations
(All items completed - see "Recently Completed" section)

### Notes on LaTeX Replacement
- Always verify that hard-coded numbers in LaTeX match current parameter values
- If numbers differ, update the parameter first, then replace the equation
- Use `{{< var variable_name_latex >}}` to insert the entire LaTeX block
- Some equations may need to be split into multiple variables if they're used in different contexts

## Notes

### Variables That Already Exist (from grep)
- `treaty_reduction_pct` - Use for all `1%` instances
- `dfda_roi_rd_only` - ROI conservative case
- `treaty_complete_roi_all_benefits` - ROI complete case
- `research_acceleration_multiplier` - Research acceleration
- `peace_dividend_annual_societal_benefit` - Peace dividend
- `recovery_trial_cost_per_patient` - RECOVERY trial cost
- `global_military_spending_annual_2024` - Military spending
- `trial_cost_reduction_factor` - Cost reduction multiplier
- `efficacy_lag_years` - Regulatory delay
- `npv_time_horizon_years` - NPV time horizon
- `npv_discount_rate_standard` - Discount rate
- `current_active_trials`, `dfda_active_trials` - Trial counts
- `dih_treasury_trial_subsidies_annual` - Patient subsidies
- `dfda_annual_opex` - Platform costs

### Literals to Keep (Not Variables)
- Historical years (1961, 1980, 2024) - Contextual references
- Example amounts in analogies ($40, $1 for fire extinguisher)
- Statistical thresholds (95% confidence, 1:1 ROI threshold)
- Trial phase names (Phase 2/3/4)
- Factual statements ("Zero" diseases eradicated)

### Implementation Steps

1. **Create new parameters** in `dih_models/parameters.py`:
   - Follow existing Parameter() structure
   - Include source_ref, description, unit, confidence
   - Add to appropriate section (Peace Dividend, Research Acceleration, etc.)

2. **Regenerate variables**:
   ```powershell
   python scripts/generate-variables-yml.py
   ```

3. **Replace in QMD**:
   - Search for hard-coded number
   - Replace with `{{< var parameter_name >}}`
   - Test rendering with `quarto preview`

4. **Verify**:
   - Check that numbers match
   - Verify citations appear correctly
   - Ensure formatting is correct

## Progress Tracking

- **Total items**: ~200+
- **Already have variables**: ~30
- **Need new parameters**: ~170
- **Should remain literal**: ~20
- **LaTeX equations to replace**: ~15

**Status**: [x] In Progress | [ ] Complete

## Recently Completed (2025-01-23)

### NPV and Formula LaTeX Variables
Fixed economics.qmd to use correct existing parameter LaTeX variables:
- `npv_costs_formula_latex` → `dfda_npv_total_cost_latex`
- `npv_benefits_formula_latex` → `dfda_npv_benefit_rd_only_latex`
- `npv_general_formula_latex` → `dfda_npv_net_benefit_rd_only_latex`
- `expected_roi_formula_latex` → `dfda_expected_roi_10pct_political_success_latex`

### NPV of Regulatory Delay Avoidance
Added new parameters for calculating NPV of the 8-year timeline shift:
- `REGULATORY_DELAY_AVOIDANCE_FAR_FUTURE_YEARS` (100 years)
- `DFDA_NPV_BENEFIT_DELAY_AVOIDANCE` ($386.6B NPV)
- Clarified distinction between one-time timeline shift benefits and recurring annual benefits (R&D savings + peace dividend)

### ROI and Investment Returns
- Line 355: `$270+` → `victory_bond_annual_return_pct`
- Line 686: `66:1` → `treaty_conservative_scenario_roi`
- Line 713-714: Monte Carlo ROI values → `treaty_complete_roi_conditional_*` and `treaty_complete_roi_expected_*` variables

### Peace Dividend
- Line 620: `$7.7T` and `$3.7T` → `global_annual_war_direct_costs_total` and `global_annual_war_indirect_costs_total`
- Line 1106: `$1.2 trillion` → `treaty_total_complete_benefits_annual`

### LaTeX Equations
- Line 145: Disease burden ratio → `medical_research_pct_of_disease_burden_latex`
- Line 172: Disease vs terrorism deaths → `disease_vs_terrorism_deaths_ratio_latex`
- Line 178: Disease vs war deaths → `disease_vs_war_deaths_ratio_latex` (fixed calculation error)
- Line 1073: QALYs to lives conversion → `treaty_total_lives_saved_annual_latex` (using existing parameter)

### Link Fixes
Fixed Quarto variables inside link text (variables don't work as link text):
- Lines 1144-1147: Moved multiplier variables outside links in research acceleration table
- Line 1164: Moved cost variables outside links in trial cost comparison
- Line 1237: Moved research acceleration variable outside link

## Verification Checklist

Before marking items complete, verify:

- [ ] All numbers match current values in `dih_models/parameters.py`
- [ ] All LaTeX equations use `_latex` variables where available
- [ ] All citations appear correctly after replacement
- [ ] Document renders correctly with `quarto preview`
- [ ] No broken variable references
- [ ] Formatting is consistent (currency, percentages, etc.)

