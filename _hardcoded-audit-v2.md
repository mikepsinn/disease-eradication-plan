# Hardcoded Value Audit Report

Generated: 2026-01-08T03:46:31.351Z

## Summary

- **Total hardcoded values found**: 82
- **High confidence matches**: 5 (safe to replace)
- **Medium confidence matches**: 9 (review context)
- **Low confidence matches**: 29 (likely wrong match)
- **No match found**: 39 (may need new param)
- **On lines with existing variables**: 14

## High Confidence Replacements

*These matches have strong context alignment and are safe to replace.*

### knowledge\proof.qmd

- [ ] **Line 38**: `$93K` → `{{< var switzerland_gdp_per_capita_k >}}`
  > - [25% richer than Americans ($93K vs $76K GDP per capita)](references.qmd#swiss-vs-us-gdp-per-capita)...

### knowledge\problem.qmd

- [ ] **Line 75**: `$20 million` → `{{< var recovery_trial_total_cost >}}` [MIXED]
  > Meanwhile, the UK's RECOVERY trial spent $20 million over six months, enrolled 48,000 patients, found multiple effective...
- [ ] **Line 91**: `40,000` → `{{< var traditional_phase3_cost_per_patient >}}` [MIXED]
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for {{< var recovery_trial_cost_per_patient ...
- [ ] **Line 174**: `$93,000` → `{{< var switzerland_gdp_per_capita_k >}}` [MIXED]
  > Switzerland spends 0.7% of GDP on military and has $93,000 GDP per capita. America spends {{< var us_military_spending_p...
- [ ] **Line 174**: `93,000` → `{{< var switzerland_gdp_per_capita_k >}}` [MIXED]
  > Switzerland spends 0.7% of GDP on military and has $93,000 GDP per capita. America spends {{< var us_military_spending_p...

## Medium Confidence (Review Context)

*These have partial context match. Verify the semantic meaning before replacing.*

### knowledge\solution.qmd

- [ ] **Line 52**: `$1,000` → `{{< var dfda_target_cost_per_patient_usd >}}` | Also: trial_relevant_diseases_count, per_capita_mental_health_cost
  > - Or 27 million patients in trials at $1,000 each...
- [ ] **Line 52**: `1,000` → `{{< var dfda_target_cost_per_patient_usd >}}` | Also: trial_relevant_diseases_count, per_capita_mental_health_cost
  > - Or 27 million patients in trials at $1,000 each...
- [ ] **Line 212**: `10%` → `{{< var pharma_success_rate_current_pct >}}` | Also: average_market_return_pct, iab_political_incentive_funding_pct, victory_bond_funding_pct
  > That's the meta-strategy: Use 1% to prove the model works, then use the built-in expansion mechanism to capture 2%, 5%, ...

### knowledge\problem.qmd

- [ ] **Line 75**: `48,000` → `{{< var who_qaly_threshold_cost_effective >}}` [MIXED] | Also: nih_standard_research_cost_per_qaly
  > Meanwhile, the UK's RECOVERY trial spent $20 million over six months, enrolled 48,000 patients, found multiple effective...
- [ ] **Line 89**: `$2.6 billion` → `{{< var pharma_drug_development_cost_current >}}` [MIXED] | Also: iab_political_incentive_funding_annual, victory_bond_annual_payout
  > It takes {{< var treatment_acceleration_years_current >}} and $2.6 billion to get a drug through FDA approval. {{< var t...
- [ ] **Line 91**: `$10` → `{{< var sugar_subsidy_cost_per_person_annual >}}` [MIXED] | Also: npv_time_horizon_years
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for {{< var recovery_trial_cost_per_patient ...
- [ ] **Line 162**: `$2.6 billion` → `{{< var pharma_drug_development_cost_current >}}` | Also: iab_political_incentive_funding_annual, victory_bond_annual_payout
  > This is why the FDA's rules mysteriously benefit large pharmaceutical companies who can afford $2.6 billion approval pro...
- [ ] **Line 172**: `$150,000` → `{{< var global_disease_deaths_daily >}}` | Also: pre_1962_physician_count, standard_economic_qaly_value_usd
  > The brain drain is real: Raytheon pays $150,000 to design bombs, the NIH pays $55,000 to cure diseases. Guess where the ...
- [ ] **Line 172**: `150,000` → `{{< var global_disease_deaths_daily >}}` | Also: pre_1962_physician_count, standard_economic_qaly_value_usd
  > The brain drain is real: Raytheon pays $150,000 to design bombs, the NIH pays $55,000 to cure diseases. Guess where the ...

## Low Confidence (Likely Wrong Match)

*Value matches but context does not. These are probably false positives.*

### knowledge\solution.qmd

- [ ] **Line 51**: `$500,000` ≈ `cell_therapy_disease_combinations` | Also: lobbyist_salary_min_k, personal_lifetime_wealth ⚠️
  > - 54,000 pragmatic clinical trials at $500,000 each (the cheap way)...
- [ ] **Line 51**: `500,000` ≈ `cell_therapy_disease_combinations` | Also: lobbyist_salary_min_k, personal_lifetime_wealth ⚠️
  > - 54,000 pragmatic clinical trials at $500,000 each (the cheap way)...
- [ ] **Line 147**: `$50` ≈ `current_drug_approvals_per_year` ⚠️
  > - Costs $50/month...
- [ ] **Line 152**: `12%` ≈ `human_interactome_targeted_pct` ⚠️
  > Every food, every drug, every supplement: Outcome label. "Increases diabetes risk 12%." "Does nothing." "Actually works,...
- [ ] **Line 160**: `$48,000` ≈ `nih_standard_research_cost_per_qaly` | Also: who_qaly_threshold_cost_effective ⚠️
  > Currently: Pharma companies pay $48,000 per trial patient...
- [ ] **Line 160**: `48,000` ≈ `nih_standard_research_cost_per_qaly` | Also: who_qaly_threshold_cost_effective ⚠️
  > Currently: Pharma companies pay $48,000 per trial patient...
- [ ] **Line 201**: `$2.7B` ≈ `iab_political_incentive_funding_annual` | Also: pharma_drug_development_cost_current, victory_bond_annual_payout ⚠️
  > | 1% | $2.7B/year | Passage pressure |...
- [ ] **Line 203**: `$27B` ≈ `global_annual_human_cost_state_violence` | Also: peace_dividend_direct_fiscal_savings, peace_dividend_lost_economic_growth, treaty_annual_funding ⚠️
  > | 10% | $27B/year | Defense industry pivot |...
- [ ] **Line 203**: `10%` ≈ `average_market_return_pct` | Also: iab_political_incentive_funding_pct, pharma_success_rate_current_pct, victory_bond_funding_pct ⚠️
  > | 10% | $27B/year | Defense industry pivot |...

### knowledge\proof.qmd

- [ ] **Line 49**: `$4 trillion` ≈ `us_chronic_disease_spending_annual` ⚠️
  > WWII cost [$4 trillion (today's dollars)](references.qmd#wwii-cost-4-trillion-today)....

### knowledge\problem.qmd

- [ ] **Line 49**: `$2,700` ≈ `global_annual_conflict_deaths_state_violence` ⚠️
  > For comparison, imagine if you spent $2,700 on guns and $68 on food. Your neighbors would stage an intervention (or call...
- [ ] **Line 49**: `$68` ≈ `us_life_expectancy_1962` ⚠️
  > For comparison, imagine if you spent $2,700 on guns and $68 on food. Your neighbors would stage an intervention (or call...
- [ ] **Line 49**: `2,700` ≈ `global_annual_conflict_deaths_state_violence` ⚠️
  > For comparison, imagine if you spent $2,700 on guns and $68 on food. Your neighbors would stage an intervention (or call...
- [ ] **Line 53**: `$2.5 trillion` ≈ `global_annual_human_life_losses_conflict` ⚠️
  > The Pentagon has lost $2.5 trillion. Not spent. Lost. Like car keys, except the car keys could cure cancer several hundr...
- [ ] **Line 55**: `$20,` ≈ `additional_drugs_from_cost_elimination` | Also: caregiver_hours_per_month, life_extension_years ⚠️
  > When normal people lose $20, they search the couch cushions. When the Pentagon loses $2,500,000,000,000, they ask for mo...
- [ ] **Line 55**: `$2,500,000,000,000,` ≈ `global_annual_human_life_losses_conflict` ⚠️
  > When normal people lose $20, they search the couch cushions. When the Pentagon loses $2,500,000,000,000, they ask for mo...
- [ ] **Line 55**: `2,500,000,000,000,` ≈ `global_annual_human_life_losses_conflict` ⚠️
  > When normal people lose $20, they search the couch cushions. When the Pentagon loses $2,500,000,000,000, they ask for mo...
- [ ] **Line 63**: `$1 trillion` ≈ `human_genome_project_total_economic_impact` ⚠️
  > Since 1970, the National Institutes of Health has spent over $1 trillion studying diseases....
- [ ] **Line 120**: `$8.2 trillion` ≈ `global_symptomatic_disease_treatment_annual` ⚠️
  > - $8.2 trillion on healthcare (treating symptoms because cures are bad for business)...
- [ ] **Line 124**: `$5 trillion` ≈ `concentrated_interest_sector_market_cap_usd` | Also: global_disease_productivity_loss_annual ⚠️
  > - 1 billion depressed humans (costing $5 trillion in lost "wanting to exist")...
- [ ] **Line 143**: `$100 billion` ≈ `global_annual_environmental_damage_conflict` ⚠️
  > This is because of something called "concentrated benefits versus diffuse costs." When military contractors want $100 bi...
- [ ] **Line 143**: `$55 million` ≈ `global_annual_deaths_curable_diseases` ⚠️
  > This is because of something called "concentrated benefits versus diffuse costs." When military contractors want $100 bi...
- [ ] **Line 143**: `1,813` ≈ `approved_drug_disease_pairings` ⚠️
  > This is because of something called "concentrated benefits versus diffuse costs." When military contractors want $100 bi...
- [ ] **Line 162**: `$1,800` ≈ `approved_drug_disease_pairings` ⚠️
  > This is why the FDA's rules mysteriously benefit large pharmaceutical companies who can afford $2.6 billion approval pro...
- [ ] **Line 162**: `1,800` ≈ `approved_drug_disease_pairings` ⚠️
  > This is why the FDA's rules mysteriously benefit large pharmaceutical companies who can afford $2.6 billion approval pro...
- [ ] **Line 203**: `$2.5 trillion` ≈ `global_annual_human_life_losses_conflict` ⚠️
  > - $2.5 trillion lost by Pentagon (whoops)...
- [ ] **Line 223**: `$1 trillion` ≈ `human_genome_project_total_economic_impact` ⚠️
  > - Why the NIH spent $1 trillion curing nothing...

### knowledge\test\test-parameters.qmd

- [ ] **Line 16**: `$1,000,000` ≈ `recovery_trial_global_lives_saved` ⚠️
  > - Sample value: $1,000,000...
- [ ] **Line 16**: `1,000,000` ≈ `recovery_trial_global_lives_saved` ⚠️
  > - Sample value: $1,000,000...

## No Variable Match

*These values have no matching variable. Consider creating new parameters.*

### `100%` (2 occurrences)

- knowledge\solution.qmd:187
  > Here's the thing they don't tell you: The goal isn't 1%. The goal is 100%....
- knowledge\test\test-parameters.qmd:15
  > - Test metric: 100%...

### `1847` (2 occurrences)

- knowledge\proof.qmd:40
  > - Haven't had a [war death since 1847](references.qmd#switzerland-last-war-death...
- knowledge\proof.qmd:40
  > - Haven't had a [war death since 1847](references.qmd#switzerland-last-war-death...

### `97%` (2 occurrences)

- knowledge\problem.qmd:69
  > Here's where it gets interesting. The NIH has a $51 billion annual budget. Of th...
- knowledge\problem.qmd:71
  > It's like if you spent 97% of your grocery budget on cookbooks and 3% on food, t...

### `54,000` (1 occurrences)

- knowledge\solution.qmd:51
  > - 54,000 pragmatic clinical trials at $500,000 each (the cheap way)...

### `73%` (1 occurrences)

- knowledge\solution.qmd:132
  > You report outcomes through your phone. The AI analyzes millions of data points....

### `45%` (1 occurrences)

- knowledge\solution.qmd:132
  > You report outcomes through your phone. The AI analyzes millions of data points....

### `35%` (1 occurrences)

- knowledge\solution.qmd:144
  > - Improves memory 35%...

### `60%` (1 occurrences)

- knowledge\solution.qmd:145
  > - Reduces symptoms 60%...

### `$5.4B` (1 occurrences)

- knowledge\solution.qmd:195
  > The {{< var iab_political_incentive_funding_pct >}} going to [Incentive Alignmen...

### `$13.5B` (1 occurrences)

- knowledge\solution.qmd:202
  > | 5% | $13.5B/year | Overwhelming lobbying |...

### `$135B` (1 occurrences)

- knowledge\solution.qmd:204
  > | 50%+ | $135B+/year | War becomes economically obsolete |...

### `50%` (1 occurrences)

- knowledge\solution.qmd:204
  > | 50%+ | $135B+/year | War becomes economically obsolete |...

### `$76K` (1 occurrences)

- knowledge\proof.qmd:38
  > - [25% richer than Americans ($93K vs $76K GDP per capita)](references.qmd#swiss...

### `25%` (1 occurrences)

- knowledge\proof.qmd:38
  > - [25% richer than Americans ($93K vs $76K GDP per capita)](references.qmd#swiss...

### `37%` (1 occurrences)

- knowledge\proof.qmd:93
  > 1945: US military spending [37% of GDP](references.qmd#us-post-wwii-military-spe...

### `271%` (1 occurrences)

- knowledge\proof.qmd:152
  > **The Lesson:** **[VICTORY Incentive Alignment Bonds](economics/economics.qmd)**...

### `$2 trillion` (1 occurrences)

- knowledge\problem.qmd:34
  > After the first 9/11, America invaded two countries and spent $2 trillion. After...

### `$51 billion` (1 occurrences)

- knowledge\problem.qmd:69
  > Here's where it gets interesting. The NIH has a $51 billion annual budget. Of th...

### `$1.665 billion` (1 occurrences)

- knowledge\problem.qmd:73
  > But it gets worse. The NIH RECOVER Initiative spent $1.665 billion over four yea...

### `$55,500` (1 occurrences)

- knowledge\problem.qmd:73
  > But it gets worse. The NIH RECOVER Initiative spent $1.665 billion over four yea...

### `55,500` (1 occurrences)

- knowledge\problem.qmd:73
  > But it gets worse. The NIH RECOVER Initiative spent $1.665 billion over four yea...

### `$820,` (1 occurrences)

- knowledge\problem.qmd:91
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for ...

### `$820` (1 occurrences)

- knowledge\problem.qmd:91
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for ...

### `820,` (1 occurrences)

- knowledge\problem.qmd:91
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for ...

### `$74,259` (1 occurrences)

- knowledge\problem.qmd:110
  > Your personal lifetime contribution to the murder budget is $74,259. You could h...

### `74,259` (1 occurrences)

- knowledge\problem.qmd:110
  > Your personal lifetime contribution to the murder budget is $74,259. You could h...

### `$100.9 trillion` (1 occurrences)

- knowledge\problem.qmd:121
  > - $100.9 trillion in economic losses (dead people are notoriously unproductive)...

### `95%` (1 occurrences)

- knowledge\problem.qmd:125
  > - 95% of rare diseases with zero treatments (too rare to profit from, sorry)...

### `99.8%` (1 occurrences)

- knowledge\problem.qmd:129
  > Out of {{< var current_disease_patients_global >}} people suffering from chronic...

### `99.6%` (1 occurrences)

- knowledge\problem.qmd:131
  > Half of humanity would volunteer if asked. You're turning away 99.6% of willing ...
