# Project Outline

**Quarto Project Overview:**
- Total configs: 14
- Total QMD files: 91

---

## _quarto-1-pct-treaty-impact.yml
**Title:** The 1% Treaty: Health and Economic Impact of Redirecting 1% of Global Military Spending to Pragmatic Clinical Trials
**Type:** book
**Files:** 4 | **Words:** 88,316

#### index.qmd
**Title:** Wishocracy
**Description:** This paper introduces Wishocracy, a governance mechanism that employs Randomized Aggregated Pairwise Preference Allocation (RAPPA) to elicit and synthesize collective preferences for public resource a...
**Stats:** 6,797 words | 473 lines

- **Abstract**
- **Introduction: The Preference Aggregation Problem**
- **Theoretical Foundations**
  - **The Analytic Hierarchy Process**
  - **Quadratic Voting and Preference Intensity**
  - **Collective Intelligence and the Wisdom of Crowds**
  - **Related Work and Positioning in the Literature**
- **Mechanism Design: Randomized Aggregated Pairwise Preference Allocation**
  - **Core Mechanism**
    - Scenario: The Town Budget
  - **Formal Properties**
  - **Formal Model**
  - **Computational Complexity and Scalability**
  - **Comparative Information & Welfare Analysis**
    - **Information-Theoretic Superiority**
    - **Welfare Maximization: The "Median vs. Mean" Proof**
    - **Principal-Agent Cost Elimination**
- **Empirical Precedents and Evidence Base**
  - **Porto Alegre Participatory Budgeting**
  - **Taiwan's Digital Democracy Experiments**
  - **Stanford Participatory Budgeting Platform Research**
  - **Colorado Quadratic Voting Experiment**
  - **Reference Implementation: Wishocracy.org**
- **Addressing Potential Criticisms**
  - **Participation and Digital Divide**
  - **Manipulation and Sybil Attacks**
  - **Preference Laundering and Manufactured Consent**
  - **Complexity of Real Policy Trade-offs**
  - **Legitimacy and Accountability**
  - **Failure Modes and Robustness**
- **Conclusion**
- **Appendix A: The Service Provider Layer**
  - References {.unnumbered}

#### knowledge/appendix/parameters-and-calculations.qmd
**Title:** Methodology, Parameters, and Calculations
**Description:** Parameter definitions, formulas, uncertainty ranges, and data sources.
**Stats:** 54,274 words | 14,688 lines

  - Overview {#sec-parameters-and-calculations}
    - Quick Navigation
  - Calculated Values {#sec-calculated}
    - Additional Drug Approvals from Cost Elimination: 20 drugs/year {#sec-additional_drugs_from_cost_elimination}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs Total (US): $5.03T {#sec-bad_policy_cost_total_us}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs (% GDP): 17.5% {#sec-bad_policy_cost_total_us_pct_gdp}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs (Tier 1): $3.92T {#sec-bad_policy_cost_us_tier1_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs (Tier 2): $2T {#sec-bad_policy_cost_us_tier2_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cell Therapy Combinations: 500k combinations {#sec-cell_therapy_disease_combinations}
      - Sensitivity Analysis
    - Annual Chronic Disease Patients Treated: 982M people {#sec-chronic_disease_treated_patients_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Clinical Trial Cost Per Approved Drug: $1.20B {#sec-clinical_trial_cost_per_approved_drug}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost Per Clinical Trial Participant: $31.6K {#sec-clinical_trial_cost_per_participant_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Combination Therapy Space: 45.1B combinations {#sec-combination_therapy_disease_space}
      - Sensitivity Analysis
    - Pairwise Drug Combinations: 45.1M combinations {#sec-combination_therapy_pairs}
      - Sensitivity Analysis
    - Combined Peace and Health Dividends for ROI Calculation: $172B {#sec-combined_peace_health_dividends_annual_for_roi_calc}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Combination Therapy Exploration Time (Current): 13.7M years {#sec-current_combination_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Known Safe Exploration Time (Current): 2.88k years {#sec-current_known_safe_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Current Patient Participation Rate in Clinical Trials: 0.0792% {#sec-current_patient_participation_rate}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Exploration Time (Current): 15.6k years {#sec-current_total_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Decentralized Framework for Drug Assessment Operational Costs: $40M {#sec-dfda_annual_opex}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings: $58.6B {#sec-dfda_benefit_rd_only_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Combined Treatment Discovery Speedup Multiplier: 17.2x {#sec-dfda_combined_treatment_speedup_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Direct Funding Cost per DALY: $0.841 {#sec-dfda_direct_funding_cost_per_daly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Direct Funding NPV (Queue Clearance Period): $475B {#sec-dfda_direct_funding_queue_clearance_npv}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Direct Funding ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput: 178k:1 {#sec-dfda_direct_funding_roi_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Direct Funding Cost-Effectiveness vs Bed Nets: 106:1 {#sec-dfda_direct_funding_vs_bed_nets_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total DALYs Lost from Disease Eradication Delay: 7.94B DALYs {#sec-dfda_efficacy_lag_elimination_dalys}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Deaths from Disease Eradication Delay: 416M deaths {#sec-dfda_efficacy_lag_elimination_deaths_averted}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Loss from Disease Eradication Delay: $1.19 quadrillion {#sec-dfda_efficacy_lag_elimination_economic_value}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Years Lived with Disability During Disease Eradication Delay: 873M years {#sec-dfda_efficacy_lag_elimination_yld}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Years of Life Lost from Disease Eradication Delay: 7.07B years {#sec-dfda_efficacy_lag_elimination_yll}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA New Treatments Per Year: 185 diseases/year {#sec-dfda_first_treatments_per_year}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Known Safe Exploration Time (dFDA): 234 years {#sec-dfda_known_safe_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Annual Net Savings (R&D Only): $58.6B {#sec-dfda_net_savings_rd_only_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Total NPV Annual OPEX: $40M {#sec-dfda_npv_annual_opex_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - NPV of Decentralized Framework for Drug Assessment Benefits (R&D Only, 10-Year Discounted): $389B {#sec-dfda_npv_benefit_rd_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - NPV Net Benefit (R&D Only): $389B {#sec-dfda_npv_net_benefit_rd_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Present Value of Annual OPEX Over 10 Years: $342M {#sec-dfda_npv_pv_annual_opex}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Total NPV Cost: $611M {#sec-dfda_npv_total_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Total NPV Upfront Costs: $270M {#sec-dfda_npv_upfront_cost_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Overhead Percentage of Treaty Funding: 0.147% {#sec-dfda_opex_pct_of_treaty_funding}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Queue Clearance Time: 36 years {#sec-dfda_queue_clearance_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Daily R&D Savings from Trial Cost Reduction: $161M {#sec-dfda_rd_savings_daily}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - ROI from Decentralized Framework for Drug Assessment R&D Savings Only: 637:1 {#sec-dfda_roi_rd_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Infrastructure Cost per Patient (Annual): $8.64 {#sec-dfda_storage_cost_total_per_patient_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Infrastructure Cost per Patient (Monthly): $0.720 {#sec-dfda_storage_cost_total_per_patient_monthly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Exploration Time (dFDA): 1.27k years {#sec-dfda_total_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Maximum Trials per Year: 40.6k trials/year {#sec-dfda_trials_per_year_capacity}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - DALYs Averted from Trial Capacity Increase: 543B DALYs {#sec-dfda_trial_capacity_dalys_averted}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Economic Value from Trial Capacity Increase: $81.5 quadrillion {#sec-dfda_trial_capacity_economic_value}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Lives Saved from Trial Capacity Increase: 10.3B deaths {#sec-dfda_trial_capacity_lives_saved}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Trial Capacity Multiplier: 12.3:1 {#sec-dfda_trial_capacity_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total DALYs from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: 565B DALYs {#sec-dfda_trial_capacity_plus_efficacy_lag_dalys}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Benefit from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: $84.8 quadrillion {#sec-dfda_trial_capacity_plus_efficacy_lag_economic_value}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Lives Saved from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: 10.7B deaths {#sec-dfda_trial_capacity_plus_efficacy_lag_lives_saved}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Suffering Hours Eliminated from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: 1931T hours {#sec-dfda_trial_capacity_plus_efficacy_lag_suffering_hours}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Average Total Timeline Shift: 212 years {#sec-dfda_trial_capacity_plus_efficacy_lag_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Treatment Timeline Acceleration: 204 years {#sec-dfda_trial_capacity_treatment_acceleration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Trial Cost Reduction Factor: 44.1x {#sec-dfda_trial_cost_reduction_factor}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Trial Cost Reduction Percentage: 97.7% {#sec-dfda_trial_cost_reduction_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Valley of Death Rescue Multiplier: 1.4x {#sec-dfda_valley_of_death_rescue_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Patients Fundable Annually: 23.4M patients/year {#sec-dih_patients_fundable_annually}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Medical Research Percentage of Treaty Funding: 80% {#sec-dih_treasury_medical_research_pct}
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Funding for Pragmatic Clinical Trials: $21.8B {#sec-dih_treasury_to_medical_research_annual}
    - Annual Clinical Trial Patient Subsidies: $21.7B {#sec-dih_treasury_trial_subsidies_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Patient Trial Subsidies Percentage of Treaty Funding: 79.9% {#sec-dih_treasury_trial_subsidies_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Diseases Without Effective Treatment: 6.65k diseases {#sec-diseases_without_effective_treatment}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Annual Disease Deaths to 9/11 Terrorism Deaths: 18.4k:1 {#sec-disease_vs_terrorism_deaths_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Annual Disease Deaths to War Deaths: 225:1 {#sec-disease_vs_war_deaths_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Coverage Factor of Treaty Funding vs Decentralized Framework for Drug Assessment OPEX: 680:1 {#sec-dividend_coverage_factor}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Drugs Approved Since 1962: 3.10k drugs {#sec-drugs_approved_since_1962}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Drug Cost Increase: 1980s to Current: 13.4:1 {#sec-drug_cost_increase_1980s_to_current_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Drug Cost Increase: Pre-1962 to Current: 105:1 {#sec-drug_cost_increase_pre1962_to_current_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Possible Drug-Disease Combinations: 9.50M combinations {#sec-drug_disease_combinations_possible}
      - Sensitivity Analysis
    - Cumulative Efficacy Testing Cost (1962-2024): $4.84T {#sec-efficacy_lag_cumulative_excess_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Efficacy Lag Deaths (9/11 Equivalents): 34.1k 9/11s {#sec-efficacy_lag_deaths_911_equivalents}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treatment Delay YLD - Annual: 2.01B DALYs {#sec-efficacy_lag_treatment_delay_yld_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Emerging Modality Combinations: 42.0M combinations {#sec-emerging_modality_combinations}
      - Sensitivity Analysis
    - Epigenetic Therapy Combinations: 1.50M combinations {#sec-epigenetic_disease_combinations}
      - Sensitivity Analysis
    - Total Deaths from Historical Progress Delays: 102M deaths {#sec-existing_drugs_efficacy_lag_deaths_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Loss from Historical Progress Delays: $259T {#sec-existing_drugs_efficacy_lag_economic_loss}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Therapeutic Frontier Exploration Ratio: 0.342% {#sec-exploration_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - FDA to Oxford RECOVERY Trial Time Multiplier: 36.4:1 {#sec-fda_to_oxford_recovery_trial_time_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Gene Therapy Combinations: 20.0M combinations {#sec-gene_therapy_disease_combinations}
      - Sensitivity Analysis
    - Total Annual Conflict Deaths Globally: 245k deaths/year {#sec-global_annual_conflict_deaths_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Cost of War Worldwide: $11.4T {#sec-global_annual_direct_indirect_war_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost of Combat Deaths: $2.34T {#sec-global_annual_human_cost_active_combat}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost of State Violence Deaths: $27B {#sec-global_annual_human_cost_state_violence}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost of Terror Deaths: $83B {#sec-global_annual_human_cost_terror_attacks}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Human Life Losses from Conflict: $2.45T {#sec-global_annual_human_life_losses_conflict}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Infrastructure Destruction: $1.88T {#sec-global_annual_infrastructure_destruction_conflict}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Trade Disruption: $616B {#sec-global_annual_trade_disruption_conflict}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Direct War Costs: $7.66T {#sec-global_annual_war_direct_costs_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Indirect War Costs: $3.70T {#sec-global_annual_war_indirect_costs_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cost per Life Saved by Medical Research: $16.1K {#sec-global_cost_per_life_saved_med_research_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Burden of Disease Globally: $109T {#sec-global_disease_economic_burden_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Global Industry Spending on Clinical Trials: $55.5B {#sec-global_industry_clinical_trials_spending_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Per Capita Military Spending Globally: $340 {#sec-global_military_spending_per_capita_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Global Military Spending After 1% Treaty Reduction: $2.69T {#sec-global_military_spending_post_treaty_annual_2024}
    - Total Annual Cost of War and Disease with All Externalities: $129T {#sec-global_total_health_and_war_cost_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Healthcare vs Military Multiplier Ratio: 7.17:1 {#sec-healthcare_vs_military_multiplier_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - IAB Mechanism Benefit-Cost Ratio: 230:1 {#sec-iab_mechanism_benefit_cost_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual IAB Political Incentive Funding: $2.72B {#sec-iab_political_incentive_funding_annual}
    - Ratio of Industry to Government Clinical Trials Spending: 12.3:1 {#sec-industry_vs_government_clinical_trials_spending_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Life Expectancy Gain Rate (1883-1962): 0 years/decade {#sec-life_expectancy_gain_1883_1962_years_per_decade}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Life Expectancy Gain Rate (1962-2019): 0 years/decade {#sec-life_expectancy_gain_1962_2019_years_per_decade}
      - Sensitivity Analysis
    - Medical Research Spending as Percentage of Total Disease Burden: 0.0525% {#sec-medical_research_pct_of_disease_burden}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Military to Clinical Trials Spending: 45.3:1 {#sec-military_to_clinical_trials_spending_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Military to Government Clinical Trials Spending: 604:1 {#sec-military_to_government_clinical_trials_spending_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Military Spending to Medical Research Spending: 40.3:1 {#sec-military_vs_medical_research_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Misallocation Factor: Cost to Kill vs Cost to Save: 2.89k:1 {#sec-misallocation_factor_death_vs_saving}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - mRNA Therapeutic Combinations: 20.0M combinations {#sec-mrna_therapeutic_combinations}
      - Sensitivity Analysis
    - Annual Peace Dividend from 1% Reduction in Total War Costs: $114B {#sec-peace_dividend_annual_societal_benefit}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Conflict Reduction Benefits from 1% Less Military Spending: $86.4B {#sec-peace_dividend_conflict_reduction}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Direct War Costs: $76.6B {#sec-peace_dividend_direct_costs}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Environmental Damage: $1B {#sec-peace_dividend_environmental}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Human Casualties: $24.5B {#sec-peace_dividend_human_casualties}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Indirect War Costs: $37B {#sec-peace_dividend_indirect_costs}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Infrastructure Destruction: $18.8B {#sec-peace_dividend_infrastructure}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Lost Economic Growth: $27.2B {#sec-peace_dividend_lost_economic_growth}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Lost Human Capital: $3B {#sec-peace_dividend_lost_human_capital}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in PTSD and Mental Health Costs: $2.32B {#sec-peace_dividend_ptsd}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Refugee Support Costs: $1.50B {#sec-peace_dividend_refugee_support}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Trade Disruption: $6.16B {#sec-peace_dividend_trade_disruption}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Veteran Healthcare Costs: $2B {#sec-peace_dividend_veteran_healthcare}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Personal Lifetime Wealth (QALY-Based): $3M {#sec-personal_lifetime_wealth}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Per Capita Chronic Disease Cost: $12.2K {#sec-per_capita_chronic_disease_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Per Capita Mental Health Cost: $1.04K {#sec-per_capita_mental_health_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Lives Saved by Pharmaceuticals: 12.4M deaths {#sec-pharma_lives_saved_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Political Dysfunction Tax (Total): 20% {#sec-political_dysfunction_tax_total_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Pragmatic Trial Cost per QALY (RECOVERY): $4.00 {#sec-pragmatic_trial_cost_per_qaly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Pragmatic Trial Efficiency Multiplier vs NIH: 12.5k:1 {#sec-pragmatic_vs_nih_efficiency_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - RECOVERY Trial Cost Reduction Factor: 82x {#sec-recovery_trial_cost_reduction_factor}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - RECOVERY Trial Total QALYs Generated: 5.00M QALYs {#sec-recovery_trial_total_qalys_generated}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Status Quo Average Years to First Treatment: 222 years {#sec-status_quo_avg_years_to_first_treatment}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Status Quo Queue Clearance Time: 443 years {#sec-status_quo_queue_clearance_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide DALYs Per Event: 41.8k DALYs {#sec-thalidomide_dalys_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide Deaths Per Event: 360 deaths {#sec-thalidomide_deaths_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide Survivors Per Event: 540 cases {#sec-thalidomide_survivors_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide US Cases Prevented: 900 cases {#sec-thalidomide_us_cases_prevented}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide YLD Per Event: 13.0k years {#sec-thalidomide_yld_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide YLL Per Event: 28.8k years {#sec-thalidomide_yll_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Global Research Funding (Baseline + 1% treaty Funding): $94.7B {#sec-total_research_funding_with_treaty}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Testable Therapeutic Space: 51.5M combinations {#sec-total_testable_therapeutic_combinations}
      - Sensitivity Analysis
    - Annual Funding from 1% of Global Military Spending Redirected to DIH: $27.2B {#sec-treaty_annual_funding}
    - Treaty System Benefit Multiplier vs Childhood Vaccination Programs: 11.5:1 {#sec-treaty_benefit_multiplier_vs_vaccines}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Amortized Annual Treaty Campaign Cost: $250M {#sec-treaty_campaign_annual_cost_amortized}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total 1% Treaty Campaign Cost: $1B {#sec-treaty_campaign_total_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Target Voting Bloc Size for Campaign: 280M of people {#sec-treaty_campaign_voting_bloc_target}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cost per DALY Averted (Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput): $0.0018 {#sec-treaty_cost_per_daly_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Expected Cost per DALY (Risk-Adjusted): $0.177 {#sec-treaty_expected_cost_per_daly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Expected Treaty ROI (Risk-Adjusted): 848k:1 {#sec-treaty_expected_roi_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Expected Cost-Effectiveness vs Bed Nets Multiplier: 503:1 {#sec-treaty_expected_vs_bed_nets_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Lives Saved from 1% Reduction in Conflict Deaths: 2.45k lives/year {#sec-treaty_lives_saved_annual_global}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - 1% treaty Basic Annual Benefits (Peace + R&D Savings): $172B {#sec-treaty_peace_plus_rd_annual_benefits}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual QALYs Gained from Peace Dividend: 85.6k QALYs/year {#sec-treaty_qalys_gained_annual_global}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - 1% treaty Recurring Annual Benefits: $172B {#sec-treaty_recurring_benefits_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treaty ROI - Historical Rate (Existing Drugs): 259k:1 {#sec-treaty_roi_existing_drugs_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treaty ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput: 84.8M:1 {#sec-treaty_roi_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Treaty System Costs: $290M {#sec-treaty_total_annual_costs}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cost-Effectiveness vs Bed Nets Multiplier: 50.3k:1 {#sec-treaty_vs_bed_nets_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treaty Campaign Leverage vs Direct Funding: 475:1 {#sec-treaty_vs_direct_funding_leverage}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cumulative Trial Capacity Years Over 20 Years: 246 years {#sec-trial_capacity_cumulative_years_20yr}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Type Ii Error Cost to Type I Error Benefit: 3.07k:1 {#sec-type_ii_error_cost_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Maximum DALYs Saved by FDA Preventing Unsafe Drugs (1962-2024): 2.59M DALYs {#sec-type_i_error_benefit_dalys}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Unexplored Therapeutic Frontier: 99.7% {#sec-unexplored_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Congress Full Advocacy Cost: $5.35B {#sec-us_congress_full_advocacy_cost}
      - Sensitivity Analysis
    - US Major Diseases Total Annual Cost: $1.25T {#sec-us_major_diseases_total_annual_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Senate Treaty Advocacy Cost: $670M {#sec-us_senate_treaty_advocacy_cost}
      - Sensitivity Analysis
    - Annual VICTORY Incentive Alignment Bond Payout: $2.72B {#sec-victory_bond_annual_payout}
    - Annual Return Percentage for VICTORY Incentive Alignment Bondholders: 272% {#sec-victory_bond_annual_return_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Global Patients Willing to Participate in Clinical Trials: 1.08B people {#sec-willing_trial_participants_global}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
  - External Data Sources {#sec-external}
    - ADAPTABLE Trial Cost per Patient: $929 {#sec-adaptable_trial_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - ADAPTABLE Trial Total Cost: $14M {#sec-adaptable_trial_total_cost}
      - Uncertainty Range
      - Input Distribution
    - Antidepressant Trial Exclusion Rate: 86.1% {#sec-antidepressant_trial_exclusion_rate}
    - Average Annual Stock Market Return: 10% {#sec-average_market_return_pct}
    - Agricultural Subsidies Deadweight Loss: $75B {#sec-bad_policy_cost_us_agricultural_subsidies}
      - Uncertainty Range
      - Input Distribution
    - Defense Above Deterrence: $400B {#sec-bad_policy_cost_us_defense_above_deterrence}
      - Uncertainty Range
      - Input Distribution
    - Drug War Cost: $90B {#sec-bad_policy_cost_us_drug_war}
      - Uncertainty Range
      - Input Distribution
    - Failed Wars (Amortized): $400B {#sec-bad_policy_cost_us_failed_wars}
      - Uncertainty Range
      - Input Distribution
    - Fossil Fuel Explicit Subsidies: $50B {#sec-bad_policy_cost_us_fossil_fuel_explicit}
      - Uncertainty Range
      - Input Distribution
    - Fossil Fuel Externalities: $600B {#sec-bad_policy_cost_us_fossil_fuel_externalities}
      - Uncertainty Range
      - Input Distribution
    - Healthcare System Inefficiency: $1.20T {#sec-bad_policy_cost_us_healthcare_inefficiency}
      - Uncertainty Range
      - Input Distribution
    - Housing/Zoning Restrictions Cost: $1.40T {#sec-bad_policy_cost_us_housing_zoning}
      - Uncertainty Range
      - Input Distribution
    - Incarceration Excess Costs: $150B {#sec-bad_policy_cost_us_incarceration_excess}
      - Uncertainty Range
      - Input Distribution
    - Infrastructure Cost Disease: $150B {#sec-bad_policy_cost_us_infrastructure_disease}
      - Uncertainty Range
      - Input Distribution
    - Migration Restrictions Cost (US Share): $500B {#sec-bad_policy_cost_us_migration_restrictions}
      - Uncertainty Range
      - Input Distribution
    - Occupational Licensing Cost: $200B {#sec-bad_policy_cost_us_occupational_licensing}
      - Uncertainty Range
      - Input Distribution
    - Tariff Cost (GDP Loss): $160B {#sec-bad_policy_cost_us_tariffs}
      - Uncertainty Range
      - Input Distribution
    - Tax Compliance Cost: $546B {#sec-bad_policy_cost_us_tax_compliance}
      - Uncertainty Range
      - Input Distribution
    - Baseline Annual Lives Saved by Pharmaceuticals: 12 deaths/year {#sec-baseline_lives_saved_annual}
    - Bed Nets Cost per DALY: $89 {#sec-bed_nets_cost_per_daly}
      - Uncertainty Range
      - Input Distribution
    - Total Annual Value of Unpaid Caregiving in US: $600B {#sec-caregiver_annual_value_total}
    - Number of Unpaid Caregivers in US: 38.0M people {#sec-caregiver_count_us}
    - Average Monthly Hours of Unpaid Family Caregiving in US: 20 hours/month {#sec-caregiver_hours_per_month}
    - Estimated Replacement Cost per Hour of Caregiving: $25 {#sec-caregiver_value_per_hour_simple}
    - Estimated Annual Global Economic Benefit from Childhood Vaccination Programs: $15B {#sec-childhood_vaccination_annual_benefit}
      - Uncertainty Range
      - Input Distribution
    - Return on Investment from Childhood Vaccination Programs: 13:1 {#sec-childhood_vaccination_roi}
    - Disability Weight for Untreated Chronic Conditions: 0.35 weight {#sec-chronic_disease_disability_weight}
      - Uncertainty Range
      - Input Distribution
    - CPI Multiplier: 1980 to 2024: 3.8:1 {#sec-cpi_multiplier_1980_to_2024}
      - Uncertainty Range
      - Input Distribution
    - Crony Tax (Capture): 10% {#sec-crony_tax_pct}
      - Uncertainty Range
      - Input Distribution
    - Current Active Trials at Any Given Time: 10.0k trials {#sec-current_active_trials}
    - Current Clinical Trial Participation Rate: 0.06% {#sec-current_clinical_trial_participation_rate}
    - Global Population with Chronic Diseases: 2.40B people {#sec-current_disease_patients_global}
      - Uncertainty Range
      - Input Distribution
    - Average Annual New Drug Approvals Globally: 50 drugs/year {#sec-current_drug_approvals_per_year}
      - Uncertainty Range
      - Input Distribution
    - Current Global Clinical Trials per Year: 3.30k trials/year {#sec-current_trials_per_year}
      - Uncertainty Range
      - Input Distribution
    - Current Trial Abandonment Rate: 40% {#sec-current_trial_abandonment_rate}
    - Annual Global Clinical Trial Participants: 1.90M patients/year {#sec-current_trial_slots_available}
      - Uncertainty Range
      - Input Distribution
    - Annual Defense Industry Lobbying Spending: $127M {#sec-defense_lobbying_annual}
    - Deworming Cost per DALY: $55 {#sec-deworming_cost_per_daly}
    - dFDA Pragmatic Trial Cost per Patient: $929 {#sec-dfda_pragmatic_trial_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Drug Development Cost (1980s): $194M {#sec-drug_development_cost_1980s}
      - Uncertainty Range
      - Input Distribution
    - Drug Repurposing Success Rate: 30% {#sec-drug_repurposing_success_rate}
    - Economic Multiplier for Education Investment: 2.1:1 {#sec-economic_multiplier_education_investment}
    - Economic Multiplier for Healthcare Investment: 4.3:1 {#sec-economic_multiplier_healthcare_investment}
      - Uncertainty Range
      - Input Distribution
    - Economic Multiplier for Infrastructure Investment: 1.6:1 {#sec-economic_multiplier_infrastructure_investment}
    - Economic Multiplier for Military Spending: 0.6:1 {#sec-economic_multiplier_military_spending}
      - Uncertainty Range
      - Input Distribution
    - Regulatory Delay for Efficacy Testing Post-Safety Verification: 8.2 years {#sec-efficacy_lag_years}
      - Uncertainty Range
      - Input Distribution
    - FDA-Approved Drug Products: 20.0k products {#sec-fda_approved_products_count}
    - FDA-Approved Unique Active Ingredients: 1.65k compounds {#sec-fda_approved_unique_active_ingredients}
      - Uncertainty Range
      - Input Distribution
    - FDA GRAS Substances: 635 substances {#sec-fda_gras_substances_count}
      - Uncertainty Range
      - Input Distribution
    - FDA Phase 1 to Approval Timeline: 9.1 years {#sec-fda_phase_1_to_approval_years}
      - Uncertainty Range
      - Input Distribution
    - Givewell Average Cost per Life Saved Across Top Charities: $4.50K {#sec-givewell_cost_per_life_avg}
    - Givewell Cost per Life Saved (Maximum): $5.50K {#sec-givewell_cost_per_life_max}
    - Givewell Cost per Life Saved (Minimum): $3.50K {#sec-givewell_cost_per_life_min}
    - Annual Deaths from Active Combat Worldwide: 234k deaths/year {#sec-global_annual_conflict_deaths_active_combat}
      - Uncertainty Range
      - Input Distribution
    - Annual Deaths from State Violence: 2.70k deaths/year {#sec-global_annual_conflict_deaths_state_violence}
      - Uncertainty Range
      - Input Distribution
    - Annual Deaths from Terror Attacks Globally: 8.30k deaths/year {#sec-global_annual_conflict_deaths_terror_attacks}
      - Uncertainty Range
      - Input Distribution
    - Global Annual DALY Burden: 2.88B DALYs/year {#sec-global_annual_daly_burden}
      - Uncertainty Range
      - Input Distribution
    - Annual Deaths from All Diseases and Aging Globally: 55.0M deaths/year {#sec-global_annual_deaths_curable_diseases}
      - Uncertainty Range
      - Input Distribution
    - Annual Environmental Damage and Restoration Costs from Conflict: $100B {#sec-global_annual_environmental_damage_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Communications from Conflict: $298B {#sec-global_annual_infrastructure_damage_communications_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Education Facilities from Conflict: $234B {#sec-global_annual_infrastructure_damage_education_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Energy Systems from Conflict: $422B {#sec-global_annual_infrastructure_damage_energy_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Healthcare Facilities from Conflict: $166B {#sec-global_annual_infrastructure_damage_healthcare_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Transportation from Conflict: $487B {#sec-global_annual_infrastructure_damage_transportation_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Water Systems from Conflict: $268B {#sec-global_annual_infrastructure_damage_water_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Lives Saved by Medical Research Globally: 4.20M lives/year {#sec-global_annual_lives_saved_by_med_research}
      - Uncertainty Range
      - Input Distribution
    - Annual Lost Economic Growth from Military Spending Opportunity Cost: $2.72T {#sec-global_annual_lost_economic_growth_military_spending}
      - Uncertainty Range
      - Input Distribution
    - Annual Lost Productivity from Conflict Casualties: $300B {#sec-global_annual_lost_human_capital_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual PTSD and Mental Health Costs from Conflict: $232B {#sec-global_annual_psychological_impact_costs_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Refugee Support Costs: $150B {#sec-global_annual_refugee_support_costs}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Currency Instability: $57.4B {#sec-global_annual_trade_disruption_currency_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Energy Price Volatility: $125B {#sec-global_annual_trade_disruption_energy_price_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Shipping Disruptions: $247B {#sec-global_annual_trade_disruption_shipping_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Supply Chain Disruptions: $187B {#sec-global_annual_trade_disruption_supply_chain_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Veteran Healthcare Costs: $200B {#sec-global_annual_veteran_healthcare_costs}
      - Uncertainty Range
      - Input Distribution
    - Annual Days of Chronic Disease Therapy: 1.28T days {#sec-global_chronic_therapy_days_annual}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Spending on Clinical Trials: $60B {#sec-global_clinical_trials_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Daily Deaths from Disease and Aging: 150k deaths/day {#sec-global_disease_deaths_daily}
      - Uncertainty Range
      - Input Distribution
    - Global Annual Direct Medical Costs of Disease: $9.90T {#sec-global_disease_direct_medical_cost_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Annual Economic Value of Human Life Lost to Disease: $94.2T {#sec-global_disease_human_life_value_loss_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Annual Productivity Loss from Disease: $5T {#sec-global_disease_productivity_loss_annual}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Government Spending on Clinical Trials: $4.50B {#sec-global_government_clinical_trials_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Household Wealth: $454T {#sec-global_household_wealth_usd}
    - Global Life Expectancy (2024): 79 years {#sec-global_life_expectancy_2024}
      - Uncertainty Range
      - Input Distribution
    - Global Government Medical Research Spending: $67.5B {#sec-global_med_research_spending}
      - Uncertainty Range
      - Input Distribution
    - Global Military Spending in 2024: $2.72T {#sec-global_military_spending_annual_2024}
      - Uncertainty Range
    - Annual Global Nonprofit Spending on Clinical Trials: $3.50B {#sec-global_nonprofit_clinical_trials_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Pharmaceutical R&D Spending: $300B {#sec-global_pharma_rd_spending_annual}
    - Global Population in 2024: 8.00B of people {#sec-global_population_2024}
      - Uncertainty Range
      - Input Distribution
    - Critical Mass Threshold for Social Change: 3.5% {#sec-global_population_activism_threshold_pct}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Spending on Symptomatic Disease Treatment: $8.20T {#sec-global_symptomatic_disease_treatment_annual}
      - Uncertainty Range
      - Input Distribution
    - YLD Proportion of Total DALYs: 0.39 proportion {#sec-global_yld_proportion_of_dalys}
      - Uncertainty Range
      - Input Distribution
    - Estimated Total Economic Impact of Human Genome Project: $1T {#sec-human_genome_project_total_economic_impact}
    - Human Interactome Targeted by Drugs: 12% {#sec-human_interactome_targeted_pct}
    - ICD-10 Total Codes: 14.0k codes {#sec-icd_10_total_codes}
    - Life Extension from Treaty Research Acceleration: 20 years {#sec-life_extension_years}
      - Uncertainty Range
      - Input Distribution
    - Maximum Annual Lobbyist Salary Range: $2M {#sec-lobbyist_salary_max}
    - Minimum Annual Lobbyist Salary Range: $500K {#sec-lobbyist_salary_min_k}
    - Return on Investment from Measles Vaccination Programs: 14:1 {#sec-measles_vaccination_roi}
    - Annual Productivity Loss per Capita from Mental Health Issues: $2K {#sec-mental_health_productivity_loss_per_capita}
    - NATO Defense Spending (2024): $1.51T {#sec-nato_defense_spending_annual}
    - Diseases Getting First Treatment Per Year: 15 diseases/year {#sec-new_disease_first_treatments_per_year}
      - Uncertainty Range
      - Input Distribution
    - NIH Annual Budget: $47B {#sec-nih_annual_budget}
      - Uncertainty Range
      - Input Distribution
    - NIH Clinical Trials Spending Percentage: 3.3% {#sec-nih_clinical_trials_spending_pct}
      - Uncertainty Range
      - Input Distribution
    - NIH Standard Research Cost per QALY: $50K {#sec-nih_standard_research_cost_per_qaly}
      - Uncertainty Range
      - Input Distribution
    - Oxford RECOVERY Trial Duration: 3 months {#sec-oxford_recovery_trial_duration_months}
      - Uncertainty Range
    - Patient Willingness to Participate in Clinical Trials: 44.8% {#sec-patient_willingness_trial_participation_pct}
      - Uncertainty Range
      - Input Distribution
    - Pharma Drug Development Cost (Current System): $2.60B {#sec-pharma_drug_development_cost_current}
      - Uncertainty Range
      - Input Distribution
    - Pharma Average Drug Revenue (Current System): $6.70B {#sec-pharma_drug_revenue_average_current}
    - Annual Life-Years Saved by Pharmaceuticals: 149M life-years {#sec-pharma_life_years_saved_annual}
      - Uncertainty Range
      - Input Distribution
    - Pharma ROI (Current System): 1.2% {#sec-pharma_roi_current_system_pct}
    - Pharma Drug Success Rate (Current System): 10% {#sec-pharma_success_rate_current_pct}
    - Phase I-Passed Compounds Globally: 7.50k compounds {#sec-phase_1_passed_compounds_global}
      - Uncertainty Range
      - Input Distribution
    - Phase I Safety Trial Duration: 2.3 years {#sec-phase_1_safety_duration_years}
    - Phase 2/3 Share of Clinical Trial Costs: 69% {#sec-phase_2_3_clinical_trial_cost_pct}
      - Uncertainty Range
      - Input Distribution
    - Phase 3 Trial Total Cost (Minimum): $20M {#sec-phase_3_trial_cost_min}
    - Pragmatic Trial Median Cost per Patient (PMC Review): $97 {#sec-pmc_pragmatic_trial_median_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Return on Investment from Sustaining Polio Vaccination Assets and Integrating into Expanded Immunization Programs: 39:1 {#sec-polio_vaccination_roi}
    - Coordination Tax (Olson): 5% {#sec-political_dysfunction_tax_coordination_pct}
      - Uncertainty Range
      - Input Distribution
    - Information Tax (Hayek): 2% {#sec-political_dysfunction_tax_info_pct}
      - Uncertainty Range
      - Input Distribution
    - Time-Inconsistency Tax: 3% {#sec-political_dysfunction_tax_time_pct}
      - Uncertainty Range
      - Input Distribution
    - Political Success Probability: 1% {#sec-political_success_probability}
      - Uncertainty Range
      - Input Distribution
    - Post-Office Career Value (per politician): $10M {#sec-politician_post_office_career_value}
      - Uncertainty Range
      - Input Distribution
    - Post-1962 Drug Approval Reduction: 70% {#sec-post_1962_drug_approval_reduction_pct}
    - Percentage Military Spending Cut After WW2: 30% {#sec-post_ww2_military_cut_pct}
    - Pre-1962 Drug Development Cost (1980 Dollars): $6.50M {#sec-pre_1962_drug_development_cost_1980_usd}
      - Uncertainty Range
      - Input Distribution
    - Pre-1962 Drug Development Cost (2024 Dollars): $24.7M {#sec-pre_1962_drug_development_cost_2024_usd}
      - Uncertainty Range
      - Input Distribution
    - Pre-1962 Physician Count (Unverified): 144k physicians {#sec-pre_1962_physician_count}
    - Total Number of Rare Diseases Globally: 7.00k diseases {#sec-rare_diseases_count_global}
      - Uncertainty Range
      - Input Distribution
    - Recovery Trial Cost per Patient: $500 {#sec-recovery_trial_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - RECOVERY Trial Global Lives Saved: 1.00M lives {#sec-recovery_trial_global_lives_saved}
      - Uncertainty Range
      - Input Distribution
    - RECOVERY Trial Total Cost: $20M {#sec-recovery_trial_total_cost}
      - Uncertainty Range
      - Input Distribution
    - Mean Age of Preventable Death from Post-Safety Efficacy Delay: 62 years {#sec-regulatory_delay_mean_age_of_death}
      - Uncertainty Range
      - Input Distribution
    - Pre-Death Suffering Period During Post-Safety Efficacy Delay: 6 years {#sec-regulatory_delay_suffering_period_years}
      - Uncertainty Range
      - Input Distribution
    - September 11 Deaths: 2.98k people {#sec-sept_11_deaths}
      - Uncertainty Range
    - Singapore GDP per Capita (PPP): $105K {#sec-singapore_gdp_per_capita_ppp}
      - Uncertainty Range
    - Singapore Govt Spending (% GDP): 1500% {#sec-singapore_govt_spending_pct_gdp}
      - Uncertainty Range
    - Singapore Life Expectancy: 84.1 years {#sec-singapore_life_expectancy}
      - Uncertainty Range
    - Return on Investment from Smallpox Eradication Campaign: 280:1 {#sec-smallpox_eradication_roi}
    - Total Economic Benefit from Smallpox Eradication Campaign: $1.42B {#sec-smallpox_eradication_total_benefit}
    - Estimated Annual Global Economic Benefit from Smoking Cessation Programs: $12B {#sec-smoking_cessation_annual_benefit}
    - Standard Economic Value per QALY: $150K {#sec-standard_economic_qaly_value_usd}
      - Uncertainty Range
      - Input Distribution
    - Standard QALYs per Life Saved: 35 QALYs/life {#sec-standard_qalys_per_life_saved}
      - Uncertainty Range
      - Input Distribution
    - Annual Cost of Sugar Subsidies per Person: $10 {#sec-sugar_subsidy_cost_per_person_annual}
    - Switzerland's Defense Spending as Percentage of GDP: 0.7% {#sec-switzerland_defense_spending_pct}
    - Switzerland GDP per Capita: $93K {#sec-switzerland_gdp_per_capita_k}
    - Switzerland Govt Spending (% GDP): 3500% {#sec-switzerland_govt_spending_pct_gdp}
      - Uncertainty Range
    - Switzerland Life Expectancy: 84 years {#sec-switzerland_life_expectancy}
      - Uncertainty Range
    - Switzerland Median Income (PPP): $65K {#sec-switzerland_median_income_ppp}
      - Uncertainty Range
    - Deaths from 9/11 Terrorist Attacks: 3.00k deaths {#sec-terrorism_deaths_911}
      - Uncertainty Range
    - Thalidomide Cases Worldwide: 15.0k cases {#sec-thalidomide_cases_worldwide}
      - Uncertainty Range
      - Input Distribution
    - Thalidomide Disability Weight: 0.4:1 {#sec-thalidomide_disability_weight}
      - Uncertainty Range
      - Input Distribution
    - Thalidomide Mortality Rate: 40% {#sec-thalidomide_mortality_rate}
      - Uncertainty Range
      - Input Distribution
    - Thalidomide Survivor Lifespan: 60 years {#sec-thalidomide_survivor_lifespan}
      - Uncertainty Range
      - Input Distribution
    - US Population Share 1960: 6% {#sec-thalidomide_us_population_share_1960}
      - Uncertainty Range
      - Input Distribution
    - Phase 3 Cost per Patient: $41K {#sec-traditional_phase3_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Traditional FDA Drug Development Timeline: 17 years {#sec-treatment_acceleration_years_current}
    - Treatment Disability Reduction: 0.25 weight {#sec-treatment_disability_reduction}
      - Uncertainty Range
      - Input Distribution
    - US Alzheimer's Annual Cost: $355B {#sec-us_alzheimers_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US Cancer Annual Cost: $208B {#sec-us_cancer_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US Annual Chronic Disease Spending: $4.10T {#sec-us_chronic_disease_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - US Diabetes Annual Cost: $327B {#sec-us_diabetes_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US GDP (2024): $28.8T {#sec-us_gdp_2024}
      - Uncertainty Range
    - US Govt Spending (% GDP): 3800% {#sec-us_govt_spending_pct_gdp}
      - Uncertainty Range
    - US Heart Disease Annual Cost: $363B {#sec-us_heart_disease_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy (1880): 39.4 years {#sec-us_life_expectancy_1880}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy (1962): 70.1 years {#sec-us_life_expectancy_1962}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy (2019): 78.9 years {#sec-us_life_expectancy_2019}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy: 77.5 years {#sec-us_life_expectancy_2023}
      - Uncertainty Range
    - US Median Household Income: $80.6K {#sec-us_median_household_income_2023}
      - Uncertainty Range
    - US Mental Health Costs: $350B {#sec-us_mental_health_cost_annual}
      - Uncertainty Range
      - Input Distribution
    - US Military Spending as Percentage of GDP: 3.5% {#sec-us_military_spending_pct_gdp}
    - US Population in 2024: 335M people {#sec-us_population_2024}
      - Uncertainty Range
      - Input Distribution
    - Senators for Treaty Ratification: 67 senators {#sec-us_senators_for_treaty}
      - Uncertainty Range
    - US Federal Campaign Spending (2024): $20B {#sec-us_total_federal_campaign_spending_2024}
    - US Total Lobbying (2024): $4.40B {#sec-us_total_lobbying_annual}
    - Valley of Death Attrition Rate: 40% {#sec-valley_of_death_attrition_pct}
      - Uncertainty Range
      - Input Distribution
    - Value of Statistical Life: $10M {#sec-value_of_statistical_life}
      - Uncertainty Range
      - Input Distribution
    - Vitamin A Supplementation Cost per DALY: $37 {#sec-vitamin_a_cost_per_daly}
    - Estimated Annual Global Economic Benefit from Water Fluoridation Programs: $800M {#sec-water_fluoridation_annual_benefit}
    - Return on Investment from Water Fluoridation Programs: 23:1 {#sec-water_fluoridation_roi}
    - Cost-Effectiveness Threshold ($50,000/QALY): $50K {#sec-who_qaly_threshold_cost_effective}
    - Percentage of Workforce Experiencing Productivity Loss from Chronic Illness: 28% {#sec-workforce_with_productivity_loss}
  - Core Definitions {#sec-definitions}
    - ADAPTABLE Trial Patients Enrolled: 15.1k patients {#sec-adaptable_trial_patients}
    - Approved Drug-Disease Pairings: 1.75k pairings {#sec-approved_drug_disease_pairings}
      - Uncertainty Range
      - Input Distribution
    - Average Life Extension per Beneficiary: 12 years {#sec-avg_life_extension_per_beneficiary}
      - Uncertainty Range
      - Input Distribution
    - Overlap Discount Factor: 0.85:1 {#sec-bad_policy_us_overlap_discount}
      - Uncertainty Range
    - Celebrity and Influencer Endorsements: $15M {#sec-campaign_celebrity_endorsement}
      - Uncertainty Range
      - Input Distribution
    - Community Organizing and Ambassador Program Budget: $30M {#sec-campaign_community_organizing}
      - Uncertainty Range
      - Input Distribution
    - Contingency Fund for Unexpected Costs: $50M {#sec-campaign_contingency}
      - Uncertainty Range
      - Input Distribution
    - Defense Industry Conversion Program: $50M {#sec-campaign_defense_conversion}
      - Uncertainty Range
      - Input Distribution
    - Budget for Co-Opting Defense Industry Lobbyists: $50M {#sec-campaign_defense_lobbyist_budget}
      - Uncertainty Range
      - Input Distribution
    - Healthcare Industry Alignment and Partnerships: $35M {#sec-campaign_healthcare_alignment}
      - Uncertainty Range
      - Input Distribution
    - Campaign Operational Infrastructure: $20M {#sec-campaign_infrastructure}
      - Uncertainty Range
      - Input Distribution
    - AI-Assisted Legal Work Budget: $50M {#sec-campaign_legal_ai_budget}
      - Uncertainty Range
      - Input Distribution
    - Legal Defense Fund: $20M {#sec-campaign_legal_defense}
      - Uncertainty Range
      - Input Distribution
    - Legal Drafting and Compliance Work: $60M {#sec-campaign_legal_work}
      - Uncertainty Range
      - Input Distribution
    - EU Lobbying Campaign Budget: $40M {#sec-campaign_lobbying_eu}
      - Uncertainty Range
      - Input Distribution
    - G20 Countries Lobbying Budget: $35M {#sec-campaign_lobbying_g20_millions}
    - US Lobbying Campaign Budget: $50M {#sec-campaign_lobbying_us}
      - Uncertainty Range
      - Input Distribution
    - Maximum Mass Media Campaign Budget: $1B {#sec-campaign_media_budget_max}
      - Uncertainty Range
      - Input Distribution
    - Minimum Mass Media Campaign Budget: $500M {#sec-campaign_media_budget_min}
      - Uncertainty Range
      - Input Distribution
    - Opposition Research and Rapid Response: $25M {#sec-campaign_opposition_research}
      - Uncertainty Range
      - Input Distribution
    - Phase 1 Campaign Budget: $200M {#sec-campaign_phase1_budget}
      - Uncertainty Range
      - Input Distribution
    - Phase 2 Campaign Budget: $500M {#sec-campaign_phase2_budget}
      - Uncertainty Range
      - Input Distribution
    - Pilot Program Testing in Small Countries: $30M {#sec-campaign_pilot_programs}
      - Uncertainty Range
      - Input Distribution
    - Voting Platform and Technology Development: $35M {#sec-campaign_platform_development}
      - Uncertainty Range
      - Input Distribution
    - Regulatory Compliance and Navigation: $20M {#sec-campaign_regulatory_navigation}
      - Uncertainty Range
      - Input Distribution
    - Scaling Preparation and Blueprints: $30M {#sec-campaign_scaling_prep}
      - Uncertainty Range
      - Input Distribution
    - Campaign Core Team Staff Budget: $40M {#sec-campaign_staff_budget}
      - Uncertainty Range
      - Input Distribution
    - Super PAC Campaign Expenditures: $30M {#sec-campaign_super_pac_budget}
      - Uncertainty Range
      - Input Distribution
    - Tech Industry Partnerships and Infrastructure: $25M {#sec-campaign_tech_partnerships}
      - Uncertainty Range
      - Input Distribution
    - Post-Victory Treaty Implementation Support: $40M {#sec-campaign_treaty_implementation}
      - Uncertainty Range
      - Input Distribution
    - Viral Marketing Content Creation Budget: $40M {#sec-campaign_viral_content_budget}
      - Uncertainty Range
      - Input Distribution
    - Annual Cost of Unpaid Caregiving: $6K {#sec-caregiver_cost_annual}
    - Cell Therapy Approaches: 500 approaches {#sec-cell_therapy_approaches}
      - Uncertainty Range
      - Input Distribution
    - Childhood Vaccination Cost per DALY (Estimated): $30 {#sec-childhood_vaccination_cost_per_daly}
    - Concentrated Interest Sector Market Cap: $5T {#sec-concentrated_interest_sector_market_cap_usd}
    - Days Per Year: 365 {#sec-days_per_year}
    - Mid-Range Funding for Commercial Dct Platform: $500M {#sec-dct_platform_funding_medium}
    - Percentage of Budget Defense Sector Keeps Under 1% treaty: 99% {#sec-defense_sector_retention_pct}
    - Years to Reach Full Decentralized Framework for Drug Assessment Adoption: 5 years {#sec-dfda_npv_adoption_ramp_years}
    - Decentralized Framework for Drug Assessment Core framework Annual OPEX: $18.9M {#sec-dfda_npv_annual_opex}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Core framework Build Cost: $40M {#sec-dfda_npv_upfront_cost}
      - Uncertainty Range
      - Input Distribution
    - Stage 1 Observational Analysis Cost per Patient: $0.100 {#sec-dfda_observational_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Community Support Costs: $2M {#sec-dfda_opex_community}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Infrastructure Costs: $8M {#sec-dfda_opex_infrastructure}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Maintenance Costs: $15M {#sec-dfda_opex_platform_maintenance}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Regulatory Coordination Costs: $5M {#sec-dfda_opex_regulatory}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Staff Costs: $10M {#sec-dfda_opex_staff}
      - Uncertainty Range
      - Input Distribution
    - Backup/Redundancy Cost per Patient (Monthly): $0.200 {#sec-dfda_storage_cost_backup_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Compute/API Cost per Patient (Monthly): $0.200 {#sec-dfda_storage_cost_compute_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Database Cost per Patient (Monthly): $0.300 {#sec-dfda_storage_cost_database_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Raw Storage Cost per Patient (Monthly): $0.020 {#sec-dfda_storage_cost_raw_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Target Cost per Patient in USD: $1K {#sec-dfda_target_cost_per_patient_usd}
    - Decentralized Framework for Drug Assessment One-Time Build Cost: $40M {#sec-dfda_upfront_build}
    - Decentralized Framework for Drug Assessment One-Time Build Cost (Maximum): $46M {#sec-dfda_upfront_build_max}
    - DIH Broader Initiatives Annual OPEX: $21.1M {#sec-dih_npv_annual_opex_initiatives}
      - Uncertainty Range
      - Input Distribution
    - DIH Broader Initiatives Upfront Cost: $230M {#sec-dih_npv_upfront_cost_initiatives}
      - Uncertainty Range
      - Input Distribution
    - Percentage of Caregiving for Treatable Disease Conditions: 40% {#sec-disease_related_caregiver_pct}
    - Epigenetic Drug Targets: 1.50k targets {#sec-epigenetic_targets_count}
      - Uncertainty Range
      - Input Distribution
    - Eventually Avoidable DALY Percentage: 92.6% {#sec-eventually_avoidable_daly_pct}
      - Uncertainty Range
      - Input Distribution
    - Eventually Avoidable Death Percentage: 92.6% {#sec-eventually_avoidable_death_pct}
      - Uncertainty Range
      - Input Distribution
    - Minimum Investment for Family Offices: $5M {#sec-family_office_investment_min}
    - Fundamentally Unavoidable Death Percentage: 7.37% {#sec-fundamentally_unavoidable_death_pct}
    - Global Political Reform Investment: $125B {#sec-global_political_reform_investment}
      - Uncertainty Range
      - Input Distribution
    - Global Political Reform Investment (Maximum): $200B {#sec-global_political_reform_investment_maximum}
    - Hours Per Day: 24 {#sec-hours_per_day}
    - Hours Per Year: 8.76k {#sec-hours_per_year}
    - Human Protein-Coding Genes: 20.0k genes {#sec-human_protein_coding_genes}
      - Uncertainty Range
      - Input Distribution
    - IAB Mechanism Annual Cost (High Estimate): $750M {#sec-iab_mechanism_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - IAB Political Incentive Funding Percentage: 10% {#sec-iab_political_incentive_funding_pct}
      - Uncertainty Range
    - Minimum Investment for Institutional Investors: $10M {#sec-institutional_investor_min}
    - Maximum Bond Investment for Lobbyist Incentives: $20M {#sec-lobbyist_bond_investment_max}
    - Minutes Per Hour: 60 {#sec-minutes_per_hour}
    - Months Per Year: 12 {#sec-months_per_year}
    - NATO Political Reform Investment: $65B {#sec-nato_political_reform_investment}
    - Standard Discount Rate for NPV Analysis: 3% {#sec-npv_discount_rate_standard}
      - Uncertainty Range
    - Standard Time Horizon for NPV Analysis: 10 years {#sec-npv_time_horizon_years}
      - Uncertainty Range
    - Peace Dividend Conflict Elasticity: 1:1 {#sec-peace_dividend_conflict_elasticity}
      - Uncertainty Range
      - Input Distribution
    - Direct Fiscal Savings from 1% Military Spending Reduction: $27.2B {#sec-peace_dividend_direct_fiscal_savings}
    - Pharma Phase 2/3 Cost Barrier Per Drug: $1.56B {#sec-pharma_phase_2_3_cost_barrier}
      - Uncertainty Range
      - Input Distribution
    - Pre-1962 Validation Years: 77 years {#sec-pre_1962_validation_years}
    - QALYs per COVID Death Averted: 5 QALYs/death {#sec-qalys_per_covid_death_averted}
      - Uncertainty Range
      - Input Distribution
    - Safe Compounds Available for Testing: 9.50k compounds {#sec-safe_compounds_count}
      - Uncertainty Range
      - Input Distribution
    - Seconds Per Minute: 60 {#sec-seconds_per_minute}
    - Seconds Per Year: 31.5M {#sec-seconds_per_year}
    - Tested Drug-Disease Relationships: 32.5k relationships {#sec-tested_relationships_estimate}
      - Uncertainty Range
      - Input Distribution
    - Political Lobbying Campaign: Direct Lobbying, Super Pacs, Opposition Research, Staff, Legal/Compliance: $650M {#sec-treaty_campaign_budget_lobbying}
      - Uncertainty Range
      - Input Distribution
    - Reserve Fund / Contingency Buffer: $100M {#sec-treaty_campaign_budget_reserve}
      - Uncertainty Range
      - Input Distribution
    - Campaign Budget for Super Pacs and Political Lobbying: $800M {#sec-treaty_campaign_budget_super_pacs}
    - Treaty Campaign Duration: 4 years {#sec-treaty_campaign_duration_years}
      - Uncertainty Range
      - Input Distribution
    - Viral Referendum Budget: $250M {#sec-treaty_campaign_viral_referendum_base_case}
      - Uncertainty Range
      - Input Distribution
    - Infinite ROI from Redirected Spending: 0:1 {#sec-treaty_redirected_spending_infinite_roi}
    - 1% Reduction in Military Spending/War Costs from Treaty: 1% {#sec-treaty_reduction_pct}
      - Uncertainty Range
    - Trial-Relevant Diseases: 1.00k diseases {#sec-trial_relevant_diseases_count}
      - Uncertainty Range
      - Input Distribution
    - US Congress Members: 535 members {#sec-us_congress_member_count}
      - Uncertainty Range
    - US Dysfunction Premium vs Switzerland: 300% {#sec-us_dysfunction_premium_vs_switzerland}
      - Uncertainty Range
    - US Political Reform Investment (Total): $25B {#sec-us_political_reform_investment_total}
    - US-Singapore Spending Gap: 2300% {#sec-us_vs_singapore_spending_gap}
      - Uncertainty Range
    - Switzerland-US Life Expectancy Gap: 6.5 years {#sec-us_vs_switzerland_life_expectancy_gap}
      - Uncertainty Range
    - US-Switzerland Spending Gap: 300% {#sec-us_vs_switzerland_spending_gap}
      - Uncertainty Range
    - Percentage of Captured Dividend Funding VICTORY Incentive Alignment Bonds: 10% {#sec-victory_bond_funding_pct}
      - Uncertainty Range

#### knowledge/references.qmd
**Title:** Source Quotes and References
**Description:** Bibliography and citations for all sources cited
**Stats:** 62 words | 22 lines

#### knowledge/economics/1-pct-treaty-impact.qmd
**Title:** The 1% Treaty: Health and Economic Impact of Redirecting 1% of Global Military Spending to Pragmatic Clinical Trials
**Description:** At current trial capacity, finding first treatments for all {{< var diseases_without_effective_treatment >}} untreated diseases would take ~{{< var status_quo_queue_clearance_years >}}. Redirecting {{...
**Stats:** 27,183 words | 2,634 lines

  - Abstract
  - Interpreting the {{< var dfda_trial_capacity_plus_efficacy_lag_years >}}-Year Timeline Figure
  - Key Findings
  - How Pragmatic Trials Increase Safety
  - Introduction
    - Historical Context: When Grand Challenges Succeed
    - The Medical Research Bottleneck
    - Addressing Skepticism: Why This Differs from Failed Megaprojects
    - Contribution to Literature
  - Research Hypothesis
  - Nomenclature and Key Terms
  - Problem Statement
    - Current Resource Allocation
      - Disease treatment vs. curing disease
    - Mortality and Morbidity Burden
  - How It Works
  - A Decentralized Framework for Drug Assessment
    - Trial Cost Reduction
    - Enhanced Safety Monitoring
    - Comparative Effectiveness Rankings
      - How Comparative Effectiveness Data Is Collected
    - Outcome Labels
  - Summary of Results
    - Total Economic Value
        - Uncertainty Analysis: Total Economic Value
    - Research Acceleration
    - Treatment Timeline Acceleration
    - Suffering Reduction
    - Lives Saved
    - DALYs Averted
    - Why "Eventually Avoidable" Matters
  - Why {{< var treaty_reduction_pct >}} Is Enough
    - 1. The Peace Dividend
    - 2. The Research Efficiency Dividend
    - 3. 15–40 "NIH equivalents" of new research capacity
  - How It Increases National Security
    - What doesn't change
    - What improves
    - The De-escalation Trajectory
    - Why The Ratchet Works: The IAB Scaling Engine
  - Political Economy and Financing
    - Incentive Alignment Bonds
      - Mechanism Architecture
      - Comparative Static Analysis: Senator Smith
      - Stakeholder Alignment
      - VICTORY Incentive Alignment Bonds
      - Legal and Ethical Framework
      - Generalized Governance Application
  - Dominance Analysis
    - Quantitative Comparison
    - Why This Dominates
  - Methodology
  - Cost-Benefit Framework
    - Cost Components
    - Benefit Components
  - ROI Calculation
  - Cost-Effectiveness Analysis
    - Expected Value Under Political Uncertainty
      - Uncertainty in Risk-Adjusted Cost-Effectiveness
      - Uncertainty in Cost-Effectiveness (Conditional on Success)
    - Treaty Campaign Leverage vs Direct Funding
      - Why Billionaires Buy Lottery Tickets Instead of the Casino
      - Numerical Comparison: Treaty vs Direct Funding
      - Direct Funding Scenario
      - Treaty Campaign Advantage
    - Detailed NPV Formulas
      - NPV of Costs
      - NPV of Benefits
      - Return on Investment
      - NPV of Regulatory Delay Avoidance
  - Quality-Adjusted Life Year (QALY) Valuation
    - QALY Calculation Model
  - Economist Verification: Complete Derivation Chains
    - 1. Trial Capacity Multiplier Derivation ({{< var dfda_trial_capacity_multiplier >}})
    - 2. Timeline Shift Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_years >}})
    - 3. DALYs Averted Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_dalys >}})
    - 4. Cost per DALY Derivation ({{< var treaty_cost_per_daly_trial_capacity_plus_efficacy_lag >}})
    - 5. ROI Derivation (Conservative: {{< var dfda_roi_rd_only >}})
    - 6. ROI Derivation (Complete: {{< var treaty_roi_trial_capacity_plus_efficacy_lag >}})
    - 7. Lives Saved Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_lives_saved >}})
    - 8. Regulatory Delay Elimination Derivation
    - 9. Annual Recurring Benefits Derivation
    - Verification Summary
  - Counterfactual Baseline Specification
  - Peace Dividend Calculation Methodology
    - Economic benefits of reduced military spending
  - Research Acceleration Mechanism
    - Treatment Discovery Through Therapeutic Space Exploration
      - The Unexplored Therapeutic Frontier
      - Current Exploration Rate vs. Therapeutic Space
    - Addressing the Returns Question: Diminishing, Linear, or Compounding?
      - Why Diminishing Returns Is Unlikely (We Haven't Started Looking)
      - The Case for Compounding Returns
      - Mathematical Framework: When Would Diminishing Returns Dominate?
      - The Conservative Default: Linear Assumption
  - Data Sources and Primary Inputs
    - Military and Conflict Data
      - Clinical Trial Economics
      - Health Economics
      - Economic Parameters
  - Sensitivity Analysis Approach
  - Key Analytical Assumptions
    - Strategic Stability Assumption
    - Linear Scaling Assumption
    - Adoption Rate Assumptions
    - Cost Reduction Assumptions
      - Empirical basis
    - Historical Precedent: Pre-1962 Physician-Led Efficacy Trials
      - Historical operational model
      - Implications for generalizability
    - Political Feasibility Assumption
    - Expected Value Analysis Accounting for Political Risk
    - Time Inconsistency and Commitment Credibility
    - Technology Constancy Assumption
    - Data Quality and Availability
  - Scenario Analysis: Conservative Case
    - ROI Derivation
    - Where the Money Comes From
    - How Treaty Funding Is Allocated
    - Returns
        - Uncertainty Analysis: Combined Annual Benefits
    - Cost-Effectiveness: Cost-Saving Health Intervention
      - Incremental Cost-Effectiveness Ratio (ICER)
      - Comparative Cost-Effectiveness vs. GiveWell Top Charities
    - Self-Funding Mechanism Through Military Budget Redirection
  - Scenario Analysis: Complete Case
    - Annual Recurring Benefits Breakdown
      - Total recurring annual benefits
      - Complete Case ROI
    - Trial Capacity Scaling
  - Individual-Level Economic Impact
  - Comparative Effectiveness
    - Comprehensive Comparison
    - Linear vs. Systemic Leverage
    - The Critical Difference
      - Translation
  - Who Benefits and How
  - Adoption Dynamics: Game-Theoretic Analysis
  - Implementation Strategy
    - Step 1: Global Mandate (The Philanthropic Catalyst)
    - Step 2: Sell $1B in VICTORY [Incentive Alignment Bonds](https://iab.warondisease.org)
    - Step 3: Implment the Legislative Strategy
    - Step 4: Build the Infrastructure
    - Step 5: Eradicate Disease
    - Campaign Budget Breakdown
  - Detailed Technical References
  - Risk Analysis and Mitigation
    - The "But Politicians Won't Do It" Problem
    - Safety Concerns
    - Patient Agency and Autonomy
    - Accountability measures
  - Limitations and Uncertainties
    - Adoption Timeline Uncertainty
    - Cost Reduction Assumptions
    - Generalizability: Meta-Analysis of 108+ Trials, Not a Single Case Study
    - Diminishing Returns in Research Productivity
      - Why this critique may not apply
      - Distinction
      - The Myth of Diminishing Returns
        - Uncertainty Analysis
    - Pragmatic Trial Internal Validity and Selection Bias
      - Mitigation strategies
    - QALY Calculation Uncertainties
    - Data Limitations
    - Military Spending Data
    - Clinical Trial Market Sizing
    - QALY Valuation Thresholds
    - Generalizability Constraints
    - Political Feasibility
    - Institutional Capacity
    - Healthcare System Integration
    - Uncertainty Quantification
    - Primary Risk Factors
    - Scenario Analysis Robustness
    - General Equilibrium Effects
    - Conditional Benefits Interpretation
    - Limitations Summary
  - Policy Implications
    - National Health Budgets
    - International Development Priorities
    - Military Budget Allocation
    - Global Health Funding Mechanisms
    - Implementation Pathway
    - Bottom Line for Policymakers
  - Treaty Adoption: Political Will and Diplomatic Strategy
    - Why Simultaneous Commitment Works: Escaping the Prisoner's Dilemma
    - Historical Treaty Precedents
    - Demonstrating Feasibility
    - Adoption Pathway
  - Conclusion

---

## _quarto-cost-of-change.yml
**Title:** The Price of Political Change: A Cost-Benefit Framework for Policy Incentivization
**Type:** website
**Files:** 1 | **Words:** 3,531

#### knowledge/appendix/cost-of-change-analysis.qmd
**Title:** The Price of Political Change: A Cost-Benefit Framework for Policy Incentivization
**Description:** When critics dismiss policy proposals as "politically impossible," they implicitly claim the cost of achieving political change exceeds its benefits. This paper develops a framework for quantifying po...
**Stats:** 3,531 words | 465 lines

  - Introduction
    - The Political Impossibility Objection
    - Political Change as an Investment
    - Contribution and Roadmap
  - Literature Review
    - Public Choice and Rent-Seeking
    - Lobbying Returns and Effectiveness
    - Campaign Finance and Electoral Outcomes
    - Post-Office Career Incentives
    - Social Impact Bonds and Outcomes-Based Policy
  - Theoretical Framework
    - The Political Cost Function
    - Campaign Finance Component
    - Lobbying Component
    - Career Value Component
    - The Benefit Function
    - Breakeven Condition
  - Empirical Methodology
    - US Political System Cost Estimates
      - Campaign Finance
      - Lobbying
      - Post-Office Career Value
      - US Maximum Reform Investment Scenarios {#us-political-reform-scenarios}
    - Global Estimates {#global-estimates}
  - Case Studies
    - Case Study 1: Military-to-Health Spending Reallocation (1% Treaty)
    - Case Study 2: Carbon Pricing
    - Case Study 3: Agricultural Subsidy Reform
    - Case Study 4: Occupational Licensing Reform
    - Summary of Case Studies
  - Limitations and Counterarguments
    - Uncertainty in Cost Estimates
    - Legal and Ethical Constraints
    - Counter-Spending and Escalation
    - Political Backlash
    - Moral Objections
  - Implementation Considerations
    - The Coordination Problem
    - Assurance Contracts
    - Credible Commitment Mechanisms
    - The Wrapper Architecture
    - Governance of the Reform Coalition
  - Conclusion
  - References

---

## _quarto-dfda-impact.yml
**Title:** The Health and Economic Impact of a Global System for Pragmatic Clinical Trials
**Type:** website
**Files:** 1 | **Words:** 11,537

#### knowledge/appendix/dfda-impact-paper.qmd
**Title:** The Health and Economic Impact of a Global System for Pragmatic Clinical Trials
**Description:** Economic analysis of a decentralized framework for drug assessment (dFDA). With {{< var dih_treasury_to_medical_research_annual >}}/year in pragmatic trial funding, the framework could save {{< var df...
**Stats:** 11,537 words | 1,219 lines

  - Understanding These Figures: The Untested Treatment Backlog
  - Executive Summary
  - Protocol, Not Platform
    - What You Get
    - Key Findings
  - Vision and Capabilities
    - Core Model: An Open Coordination Protocol
    - Key Capabilities
    - Potential Impact on the Status Quo
  - Addressing Key Concerns
    - Why This Differs from Failed Megaprojects
    - Historical Validation: Pre-1962 Physician-Led Efficacy Testing
    - Why "Eventually Avoidable" Matters
    - Trial Funding Scenario
  - Framework Costs (ROM Estimates) {#dfda-framework-costs-rom-estimates}
    - Upfront Build Costs (30 Months) {#upfront-build-costs}
    - Ecosystem Participants
    - Annual Operational Costs (5M MAU Target Scale) {#annual-operational-costs}
      - Marginal Cost Analysis per User
    - Scenario Based ROM Estimates for Broader Initiative Costs
      - Interpretation
      - Summary
  - Benefit Analysis - Quantifying the Savings
    - Market Size and Impact
    - Decentralized Trial Costs Modeled on Pragmatic Trials
    - Overall Savings
    - Economic Value of Earlier Access to Treatments
    - Gross R&D Savings from Implementing a Decentralized Framework {#gross-r-and-d-savings-from-implementing-a-decentralized-framework}
      - Key Sources
    - Post-Safety Efficacy Lag Elimination {#regulatory-delay-avoidance}
      - The Efficacy Lag Problem
      - How a Decentralized Framework Eliminates the Efficacy Lag
      - Quantified Benefits (One-Time Timeline Shift)
      - Efficacy Lag Elimination - Uncertainty Analysis
    - Safety and Risk Management
      - Current System Limitations: Dangerously Blind to Real-World Harms
      - Proposed System Safety Advantages
      - Detection Timeline Comparison
      - Comparative Safety Surveillance
      - Pooled Liability Insurance
  - ROI Analysis for a Decentralized Framework {#simplified-roi-scenario}
    - Monte Carlo Distributions
  - Research Acceleration Mechanism
    - The Unexplored Therapeutic Frontier
    - Current Exploration Rate vs. Therapeutic Space
    - Addressing the Returns Question: Diminishing, Linear, or Compounding?
      - Why Diminishing Returns Is Unlikely (We Haven't Started Looking)
      - Mathematical Framework: When Would Diminishing Returns Dominate?
      - The Conservative Default: Linear Assumption
  - Data Sources and Methodological Notes
  - Conclusion
    - Disclaimer
  - Verification: Complete Derivation Chains
    - 1. Trial Capacity Multiplier Derivation ({{< var dfda_trial_capacity_multiplier >}})
    - 2. Timeline Shift Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_years >}})
    - 3. Lives Saved Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_lives_saved >}})
    - 4. Cost per DALY Derivation ({{< var dfda_direct_funding_cost_per_daly >}})
    - 5. ROI Derivation ({{< var dfda_roi_rd_only >}})
    - Verification Summary
  - Key Analytical Assumptions
    - Linear Scaling Assumption
    - Adoption Rate Assumptions
    - Cost Reduction Assumptions
    - Eventually Avoidable Mortality Assumption
    - Counterfactual Baseline Specification
    - Methodology Validation Against Accepted Benchmarks
  - Appendix Calculation Frameworks and Detailed Analysis
    - Calculation Framework - NPV Methodology {#calculation-framework---npv-methodology}
    - Financial Analysis Summary {#financial-analysis-summary}
      - Health Impact Uncertainty Analysis
      - Financial Visualizations
    - Cost-Utility Framework {#dfda-icer-analysis---cost-utility-framework}
      - QALY Benefit Streams Breakdown
      - DALY Sensitivity Analysis
    - Comparative Cost-Effectiveness - A Decentralized Framework vs Other Interventions
    - Methodology Notes
    - Data Limitations
  - Comparison to Other Major Public Investments

---

## _quarto-dfda-spec.yml
**Title:** dFDA: A Decentralized Framework for Drug Assessment Using Two-Stage Real-World Evidence Validation
**Type:** website
**Files:** 1 | **Words:** 13,613

#### knowledge/appendix/dfda-spec-paper.qmd
**Title:** dFDA: A Decentralized Framework for Drug Assessment Using Two-Stage Real-World Evidence Validation
**Description:** We present the Predictor Impact Score (PIS), a novel composite metric operationalizing Bradford Hill causality criteria for automated signal detection from aggregated N-of-1 observational studies. Com...
**Stats:** 13,613 words | 1,907 lines

  - Abstract
  - System Overview: From Methodology to Implementation {#system-overview}
    - What Patients See
    - What Companies See
    - Where This Methodology Fits
  - Introduction
    - The Human Cost of the Current System
    - The Pharmacovigilance Gap
    - The Real-World Data Opportunity
    - Our Contribution
  - Data Collection and Integration
    - Data Sources
    - Variable Ontology
    - Measurement Structure
    - Unit Standardization
  - Mathematical Framework
    - Data Structure
    - Temporal Alignment
      - Onset Delay and Duration of Action
      - Outcome Window Calculation
    - Pair Generation Strategies
      - Outcome-Based Pairing (Predictor has Filling Value)
      - Predictor-Based Pairing (No Filling Value)
    - Filling Value Logic
      - Filling Types
      - Temporal Boundaries
      - Conservative Bias
    - Baseline Definition and Outcome Estimation
      - Within-Subject Comparison
      - Outcome Means
    - Percent Change from Baseline
    - Correlation Coefficients
      - Pearson Correlation (Linear Relationships)
      - Spearman Rank Correlation (Monotonic Relationships)
      - Forward and Reverse Correlations
    - Z-Score Normalization
    - Statistical Significance
    - Hyperparameter Optimization
  - Population Aggregation
    - Individual to Population
    - Standard Error and Confidence Intervals
    - Heterogeneity Assessment
  - Data Quality Requirements
    - Minimum Thresholds
    - Variance Validation
    - Outcome Value Spread
  - Predictor Impact Score
    - What Makes the Predictor Impact Score Novel
    - User-Level Predictor Impact Score
    - Aggregate (Population-Level) Predictor Impact Score
    - Z-Score and Effect Magnitude Factor
    - Temporality Factor
    - Percent Change from Baseline
    - Statistical Significance
    - Interest Factor
    - Additional Data Quality Components
    - Bradford Hill Criteria Mapping {#bradford-hill-mapping}
    - Interpreting Predictor Impact Scores
  - Provisional Thresholds - Not Yet Validated
    - Optimal Daily Value for Precision Dosing
      - Value Predicting High Outcome
      - Value Predicting Low Outcome
      - Grouped Optimal Values
      - Precision Dosing Recommendations
      - Mathematical Relationship to Biological Gradient
      - Clinical Applications
      - Limitations
      - Confidence Intervals for Optimal Values
      - Individual vs Population Optimal Values
      - Temporal Stability and Recalculation
      - Edge Cases: Minimal Dose-Response
      - Validation of Optimal Values
    - Saturation Constant Rationale
    - Effect Following High vs Low Predictor Values
      - Average Outcome Metrics
      - Calculation
    - Predictor Baseline and Treatment Averages
    - Relationship Quality Filters
      - Filter Flags
      - Boring Relationship Definition
      - Usefulness and Causality Voting
    - Variable Valence
      - Impact on Interpretation
    - Temporal Parameter Optimization
      - Stored Optimization Data
      - Optimization Grid
      - Overfitting Protection
    - Spearman Rank Correlation
  - Outcome Label Generation
    - Predictor Analysis Reports
    - Report Structure
    - Category-Specific Analysis
    - Verification Status
    - Outcome Labels vs. FDA Drug Labels
    - Worked Example: Complete Outcome Label
  - Treatment Ranking System
    - Within-Category Rankings
    - Ranking Algorithm
    - Confidence Weighting
    - Comparative Effectiveness Display
  - Safety and Efficacy Quantification
    - Safety Signal Detection
    - Efficacy Signal Detection
    - Benefit-Risk Assessment
  - Addressing the Bradford Hill Criteria {#addressing-bradford-hill}
    - Complete Criteria Mapping
    - Quantitative Criteria Details
  - Validation and Quality Assurance
    - User Voting System
    - Automated Quality Checks
    - Flagged Study Handling
  - Stage 2: Pragmatic Trial Confirmation
    - The Two-Stage Pipeline
    - Pragmatic Trial Methodology
    - Signal-to-Trial Prioritization
    - Comparative Effectiveness Randomization
    - Feedback Loop: Trial Results Improve Observational Models
    - Output: Validated Outcome Labels
  - Limitations and How They're Addressed
    - Fundamental Limitations: Observational Stage
    - Methodological Weaknesses: Addressed by Two-Stage Design
    - Residual Limitations
    - What This Framework CAN Now Do
  - Implementation Guide
    - System Architecture
    - Core Algorithm: Pair Generation
    - Core Algorithm: Baseline Separation
    - Algorithm 3: Predictor Impact Score Calculation
    - Reference Implementation
  - Regulatory Considerations
    - Positioning Relative to RCTs
    - Evidence Hierarchy Integration
    - FDA Real-World Evidence Framework Alignment
  - Validation Framework {#sec-validation-framework}
    - The Critical Question
    - Proposed Validation Study
    - Known Limitations Requiring Validation
  - Future Directions
    - Methodological Improvements
    - Validation Priorities
    - Implementation Enhancements
  - Conclusion
  - Appendix A: Effect Size Classification
  - Appendix B: Variable Category Defaults
  - Appendix C: Glossary
  - Appendix D: Worked Example
    - Example: Calculating Predictor Impact Score for "Magnesium → Sleep Quality"
  - Appendix E: Analysis Workflow

---

## _quarto-federal-efficiency-audit.yml
**Title:** Federal Resource Allocation Efficiency Audit
**Type:** website
**Files:** 1 | **Words:** 4,249

#### knowledge/appendix/federal-efficiency-audit.qmd
**Title:** Federal Resource Allocation Efficiency Audit
**Description:** Engineering-style efficiency analysis quantifying $2.27-3.47 trillion in annual allocation losses across defense, healthcare, justice, regulatory, and subsidy subsystems, with OECD benchmark compariso...
**Stats:** 4,249 words | 555 lines

  - Executive Summary
  - Interpretation Note
  - System Specifications
    - Designed Function
    - Why Two Metrics Are Sufficient
    - Input-Output Measurement
  - Methodology
    - Engineering Loss Categories
    - Aggregate Efficiency Gap Calculation
  - Methodological Caveat: Overlap and Double-Counting
    - Valuation Standards
  - Subsystem Audit: Defense
    - Loss Category: Leakage (Audit Failure)
    - Loss Category: Conversion Inefficiency (F-35 Program)
    - Loss Category: Idle/Standby (Overseas Basing)
    - Loss Category: Parasitic (Strategic Misalignment)
    - Defense Subsystem Summary
  - Subsystem Audit: Healthcare Administration
    - Loss Category: Friction (Administrative Overhead)
    - Loss Category: Leakage (Medicare Advantage Upcoding)
    - Loss Category: Leakage (Improper Payments)
    - Healthcare Subsystem Summary
  - Subsystem Audit: Justice and Prohibition
    - Loss Category: Conversion Inefficiency (Drug Prohibition)
    - Loss Category: Negative Work (Mass Incarceration)
    - Loss Category: Leakage (Civil Asset Forfeiture)
    - Justice Subsystem Summary
  - Subsystem Audit: Regulatory and Tax Compliance
    - Loss Category: Friction (Tax Compliance)
    - Loss Category: Friction (Housing/Zoning Misallocation)
    - Loss Category: Idle (NEPA Permitting Delays)
    - Loss Category: Parasitic (Jones Act)
    - Regulatory Subsystem Summary
  - Subsystem Audit: Subsidies and Transfers
    - Loss Category: Parasitic (Fossil Fuel Subsidies)
    - Loss Category: Parasitic (Agricultural Subsidies)
    - Loss Category: Negative Work (Tariffs and Corporate Welfare)
    - Subsidies Subsystem Summary
  - Aggregate Efficiency Calculation
    - Monte Carlo Simulation Parameters
    - Simulation Results
      - Subsystem Uncertainty Distributions
  - Tax Compliance
  - Housing/Zoning
  - Healthcare
  - Drug War
    - Efficiency Rating Calculation
    - Human Cost Quantification (Economic Equivalents)
  - Reallocation Potential
    - Context Comparisons
  - Structural Factors
    - Severed Feedback Loops
    - Principal-Agent Misalignment
    - Measurement Failure
    - Monopoly Dynamics
    - Time Horizon Mismatch
  - Confidence Intervals and Limitations
    - Estimate Confidence by Subsystem
    - What This Analysis Excludes
    - Methodological Limitations
  - See Also

---

## _quarto-iab.yml
**Title:** Incentive Alignment Bonds: Making Public Goods Financially and Politically Profitable
**Type:** website
**Files:** 1 | **Words:** 16,422

#### knowledge/appendix/incentive-alignment-bonds-paper.qmd
**Title:** Incentive Alignment Bonds: Making Public Goods Financially and Politically Profitable
**Description:** Government spending is optimized for lobbying intensity, not net societal value. Programs with 100:1 benefit-cost ratios get billions while programs with negative returns get hundreds of billions. Inc...
**Stats:** 16,422 words | 1,485 lines

  - Introduction
    - The Information-Incentive Disconnect
    - Key Results
    - Reader's Guide
    - Definition
    - Why Reallocation, Not Addition
    - Political Change as an Asset Class
    - The Capital Asymmetry: Why IABs Can Outcompete Incumbent Lobbying
    - Quantifying Net Societal Value of Funding Sources
    - Relation to Existing Literature
    - Contribution
    - Roadmap
  - Why Previous Approaches Failed {#sec-literature}
    - Mechanism Design Theory
    - Public Choice Theory
    - Social Impact Bonds
    - Campaign Finance and Political Behavior
    - Credit Rating Agencies as Governance Mechanisms
  - The Math: Proving It Works {#sec-formal-model}
    - Assumptions
    - The Politician's Utility Function
    - The Utility Function Transformation
    - Numerical Calibration and Parameter Ranges
    - The Policy Choice
    - The Pre-IAB Equilibrium
    - The IAB Mechanism
    - Score-Dependent Payoffs
    - Incentive Compatibility
    - Nash Equilibrium Analysis
    - Illustrative Example: A Global Health Treaty
    - Calibration: Parameter Ranges for Incentive Compatibility
  - How IABs Work in Practice {#sec-architecture}
    - Layer A: Scoring (Data Provision)
    - Layer B: Electoral Support
    - Layer C: Post-Office Benefits
    - Why This Is Not Bribery
      - Statutory Analysis: 18 U.S.C. § 201
      - Constitutional Protections
      - Established Precedent: Decades of Legal Scorecard Operations
      - The Key Legal Distinction
    - Legal Entity Separation
    - Funding Sources and Foundation Investment
  - What Could Go Wrong {#sec-failure-modes}
    - Gaming and Metric Corruption
    - Plutocracy Objection and the "Lobbying With Extra Steps" Critique
    - Unintended Consequences
  - Where IABs Fit in Democratic Reform {#sec-governance}
    - The Four-Layer Governance Stack
    - Comparison to Alternative Governance Mechanisms
    - What IABs Do Not Solve
  - Beyond Health: Climate, Nuclear Risk, and More {#sec-generalization}
    - The General Template
    - Candidate Domains
    - Welfare Accounting of the IAB Mechanism
      - Sensitivity Analysis of Mechanism BCR
  - Conclusion
    - The Bootstrap Problem and Regulatory Resistance
  - References {.unnumbered}
  - Appendix A: Formal Proofs {.unnumbered}
    - Proof of Proposition 1 (Sufficient Condition for Incentive Compatibility)
    - Proof of Corollary 1 (Funding Threshold)
    - Proof of Proposition 2 (Multiple Equilibria Without IABs)
    - Proof of Proposition 3 (Equilibrium Selection With IABs)
  - Appendix B: Detailed Application Specifications {.unnumbered}
    - B.1 Climate Change
    - B.2 Nuclear Disarmament
    - B.3 Pandemic Preparedness
    - B.4 Comparative Analysis

---

## _quarto-invisible-graveyard.yml
**Title:** The Invisible Graveyard: Quantifying the Mortality Cost of FDA Efficacy Lag, 1962-2024
**Type:** website
**Files:** 1 | **Words:** 6,735

#### knowledge/appendix/invisible-graveyard.qmd
**Title:** The Invisible Graveyard: Quantifying the Mortality Cost of FDA Efficacy Lag, 1962-2024
**Description:** The 1962 efficacy requirement adds {{< var efficacy_lag_years >}} to drug approval after safety is proven. This study quantifies two distinct mortality costs: (1) {{< var existing_drugs_efficacy_lag_d...
**Stats:** 6,735 words | 749 lines

  - The Short Version
  - Abstract
  - Scale
  - Introduction
  - Literature Review: The Drug Lag Debate
    - Foundational Economic Analysis
    - The Current Debate
    - Empirical Case Studies: Demonstrating the Causal Mechanism
  - Methodology & Data
    - Variable Definitions {#mortality-estimates}
    - Theoretical Upper Bound: What's Eventually Preventable? {#eventually-preventable}
  - Methodological Note: Distinguishing Current vs. Theoretical Preventability
      - Disease Burden by Category
      - Why This Upper Bound? The Biological and Epidemiological Evidence
      - The {{< var fundamentally_unavoidable_death_pct >}} Floor
    - Data Sources & Parameterization
    - Uncertainty Quantification Methodology
  - Results: The Mortality Burden {#mortality-scenarios}
    - Primary Estimate
  - Methodological Caveat: Cascade Assumption
      - Sensitivity Analysis
  - Morbidity Analysis: DALYs and QALYs {#daly-calculation}
    - Years of Life Lost (YLL)
    - Years Lived with Disability (YLD)
    - Cumulative DALY Burden
    - Years Lived with Disability - Treatment Beneficiaries {#treatment-morbidity}
  - Distinction: Mortality vs. Morbidity Burden
  - Economic Valuation {#economic-valuation}
    - Contextualizing the Loss
  - Risk Analysis: The Type I vs. Type II Ratio {#risk-analysis}
  - Methodological Note: Steelmanning the FDA's Position
    - The Risk Trade-off Ratio
    - Acknowledging the Efficacy-as-Safety Argument
    - Drugs Appropriately Caught by Phase II/III Trials
  - Model Assumptions and Limitations
    - Key Assumptions
    - Sensitivity Analysis
    - Limitations
  - Policy Implications
    - The False Trade-off
    - The Bifurcated Alternative
    - Expected Impact
    - International Regulatory Comparison
  - Critical Distinction: Efficacy Assessment Reordered, Not Eliminated
  - Addressing Common Critiques
    - "The PRIMARY Estimate Is Too Speculative"
    - "The 'Eventually Preventable' Estimate Is Theoretical"
    - "Counterfactual Uncertainty - We Can't Know What Would Have Happened"
      - Natural Experiments
      - The Standard for Causal Inference
    - "Confounding Factors - Other Changes in 1962"
      - Sensitivity Analysis: What if Regulation Explains Only Part of the Decline?
    - "This Ignores Safety - Deregulation Would Flood Markets with Dangerous Drugs"
  - Conclusion

---

## _quarto-manual.yml
**Title:** How to End War and Disease
**Type:** book
**Files:** 86 | **Words:** 336,767

#### index.qmd
**Title:** Start Here
**Description:** This paper introduces Wishocracy, a governance mechanism that employs Randomized Aggregated Pairwise Preference Allocation (RAPPA) to elicit and synthesize collective preferences for public resource a...
**Stats:** 6,797 words | 473 lines

- **Abstract**
- **Introduction: The Preference Aggregation Problem**
- **Theoretical Foundations**
  - **The Analytic Hierarchy Process**
  - **Quadratic Voting and Preference Intensity**
  - **Collective Intelligence and the Wisdom of Crowds**
  - **Related Work and Positioning in the Literature**
- **Mechanism Design: Randomized Aggregated Pairwise Preference Allocation**
  - **Core Mechanism**
    - Scenario: The Town Budget
  - **Formal Properties**
  - **Formal Model**
  - **Computational Complexity and Scalability**
  - **Comparative Information & Welfare Analysis**
    - **Information-Theoretic Superiority**
    - **Welfare Maximization: The "Median vs. Mean" Proof**
    - **Principal-Agent Cost Elimination**
- **Empirical Precedents and Evidence Base**
  - **Porto Alegre Participatory Budgeting**
  - **Taiwan's Digital Democracy Experiments**
  - **Stanford Participatory Budgeting Platform Research**
  - **Colorado Quadratic Voting Experiment**
  - **Reference Implementation: Wishocracy.org**
- **Addressing Potential Criticisms**
  - **Participation and Digital Divide**
  - **Manipulation and Sybil Attacks**
  - **Preference Laundering and Manufactured Consent**
  - **Complexity of Real Policy Trade-offs**
  - **Legitimacy and Accountability**
  - **Failure Modes and Robustness**
- **Conclusion**
- **Appendix A: The Service Provider Layer**
  - References {.unnumbered}

### The Problem

#### knowledge/problem.qmd
**Title:** Problem Overview
**Description:** Humanity's spectacular failure at prioritizing not dying
**Stats:** 2,473 words | 256 lines

  - Daily Numbers
  - Where the Money Goes
  - On the Pentagon's Accounting
  - On Medical Research
  - On the FDA
  - On What War Costs
  - On What Disease Costs
  - On Democracy
  - On Regulatory Capture
  - On the Fixed Pie
  - On Your Personal Situation
  - What This Means
  - What's Next

#### knowledge/problem/the-daily-massacre.qmd
**Title:** The Bi-Monthly Holocaust
**Description:** 150,000 People Die Every Day While We Build Skynet, That's Fifty 9/11s Daily
**Stats:** 286 words | 44 lines

  - The Math Of Death

#### knowledge/problem/cost-of-war.qmd
**Title:** The Cost of War
**Description:** Quantifying Human Idiocy - A precise accounting of what humans spend to destroy themselves, with numbers that would make a statistician weep.
**Stats:** 3,369 words | 452 lines

  - The Itemized Receipt for Armageddon
    - The Shopping List (2024 Global Data)
      - Total Direct Military Spending: \$2,718.0 billion
    - The Equation of Immediate Destruction
      - Current Annual Calculation
  - Military Hardware: The World's Worst Investment
    - OFFERING MEMORANDUM
      - RETURNS
      - COSTS
      - DEPRECIATION
      - RISK FACTORS
    - The Dead Capital Problem
      - Outcome A (Unused)
      - Outcome B (Used)
    - The Price of a Ghost: Valuing Human Life
      - Annual Mortality Cost Calculation
  - Infrastructure Destruction: Breaking Things Costs Money
    - Reconstruction Cost Analysis (2023 Estimates)
      - Total Infrastructure Damage: {{< var global_annual_infrastructure_destruction_conflict >}}
  - Economic Disruption: The Ripple Effect
    - Trade Flow Disruption Matrix
      - Total Trade Disruption: {{< var global_annual_trade_disruption_conflict >}} annually
  - The Ghost in the Machine: Indirect Costs
    - Opportunity Cost Analysis: The Roads Not Taken
      - Comparative Investment Analysis (2023 Dollars)
      - The Multiplier Effect: Economic Growth We're Not Having
        - Lost GDP Growth Calculation
    - Long-term Human Costs: The Gift That Keeps on Taking
      - Veteran Healthcare Cost Projections
      - Refugee Support: The Mathematics of Displacement
        - Annual Refugee Support Cost
        - Lost Economic Productivity
    - Environmental Degradation: Poisoning the Planet Costs Money Too
      - Environmental Cost Calculation Matrix
    - The Existential Overdraft: The AI Arms Race
  - The Total Cost of Organized Violence
    - Comprehensive Cost Analysis (2024)
      - Direct Costs Summary
      - Indirect Costs Summary
      - Ultimate Total
      - Per Capita Mathematics: What War Costs You
    - Statistical Perspectives: Putting Numbers in Context
    - The Grotesque Mathematics of Misallocation
    - Hidden Costs of War

#### knowledge/problem/cost-of-disease.qmd
**Title:** The Cost of Disease
**Description:** The annual bill for our collective decision to let our bodies fall apart. Spoiler alert, it's more than all the money on Earth.
**Stats:** 1,549 words | 183 lines

  - The Actual Bill (Economist-Approved Misery Accounting)
  - How to Measure Suffering Without Feeling Feelings (The DALY)
    - What the WHO Thinks You're Worth (Spoiler: Not Much)
  - Let's Break Down This Apocalypse By Time Unit
  - What's Actually Deleting Everyone (The Greatest Hits)
  - Your Body Is Not Magic, It's Just Broken
  - What This Actually Costs
    - Your Priorities, Written in Your Budgets
    - The Future You're Paying For

#### knowledge/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd
**Title:** NIH Fails to Institute Health
**Description:** The NIH spends only 3.3% on testing if drugs actually work in humans and almost nothing on highly efficent pragmatic trials. This misallocation costs ~100 million quality-adjusted life-years annually.
**Stats:** 1,864 words | 270 lines

  - The Allocation Scandal
  - Why This Allocation Exists
  - The Efficiency Gap: A Tale of Two Trials
    - RECOVER Initiative (NIH Approach)
    - RECOVERY Trial (UK Approach)
  - The Death Toll: Opportunity Cost of Misallocation
    - Cost Per QALY (Quality-Adjusted Life Year)
    - The "Death Equivalent" of Budget Misallocation
  - The Translation Crisis: Concept Rich, Trial Poor
    - Knowledge Production: Saturated. Translation Capacity: Starved.
      - What we don't have: Cures.
  - The Public Goods vs. Club Goods Scam
  - The Patient Disconnect: Zero Correlation with Health Outcomes
    - What patients want
      - What NIH funds
  - The Track Record
  - What Would Actually Work
  - The Bottom Line

#### knowledge/problem/untapped-therapeutic-frontier.qmd
**Title:** The Untapped Therapeutic Frontier
**Description:** You've explored less than 1% of medicine. The other 99% is where the cures are.
**Stats:** 1,537 words | 177 lines

  - Your Tiny Sandbox
  - The Target List (Ways Your Body Breaks)
  - The Math You're Ignoring
    - What You've Actually Tested
    - The Scorecard
  - Is The Untested Stuff Useful?
  - The Universe is Big. You Are Small.
  - Why You Are Still Sick
  - How Long to Explore Everything?
    - Tier 1: Single Compounds (Most Conservative)
    - Tier 2: Combination Therapies (Still Defensible)
    - Tier 3: The Full Chemical Universe (Illustrative)
    - "But Won't We Run Out of Easy Discoveries?"
  - The Fix
  - The Bottom Line

#### knowledge/problem/fda-is-unsafe-and-ineffective.qmd
**Title:** The FDA Is Unsafe and Ineffective
**Description:** How blocking patient access during 8+ years of efficacy testing made clinical trials 34× more expensive per patient while making drugs demonstrably more dangerous.
**Stats:** 4,078 words | 501 lines

  - A Note on Blame
  - Confidence Levels: What We Know vs. What We Model
  - The {{< var dfda_trial_cost_reduction_factor >}}× Inefficiency Tax
    - The {{< var efficacy_lag_years >}}-Year Efficacy Lag
  - What the 1962 Efficacy Requirements Changed
  - Detailed Historical Analysis
    - The 1962 Policy Break: Measured Impact
  - Detailed Cost Analysis
    - The Modern Consequences
      - High Costs Kill Innovation, Reward Monopoly
    - Off-Patent Drugs and Rare Diseases: Mathematically Doomed
  - The Actual Death Toll of "Drug Lag"
    - The Global Body Count
    - The Morbidity Burden (DALYs)
  - How the Incentives Work
    - FDA Regulator Decision Tree
      - Approve drug that later shows problems
      - Delay drug that could save lives
    - The Math: Why Current Regulations Increase Total Harm
    - Why Bureaucrats Are Rewarded for Letting You Die
  - Clinical Trial Theater: Excluding {{< var antidepressant_trial_exclusion_rate >}} of Reality Makes Drugs More Dangerous
    - Why This Makes Drugs More Dangerous
    - No Long-Term Outcome Data
    - Pre-Specification Requirements Kill Innovation
  - The Negative Results Black Hole
  - Countries That Don't Have Our "Safety"
  - The COVID Test Fiasco
  - Small Trials Are Dangerous!
    - Why Small Trials Miss Safety Signals
    - The Adverse Event Reporting Failure
    - What Real-World Evidence Would Catch
  - The Bottom Line
  - Technical Analysis

#### knowledge/problem/unrepresentative-democracy.qmd
**Title:** Unrepresentative Democracy
**Description:** Why democracy mathematically serves money over voters, and how to exploit that bug
**Stats:** 3,692 words | 614 lines

  - Democracy
  - The Rational Ignorance Problem
  - What Democracy Should Look Like vs Reality
  - The Mathematics of Political Failure
    - Concentrated Benefits vs. Diffuse Costs
  - How Money Buys Power
    - The Lobbying ROI: 1,810:1 Returns
    - Why Nothing Ever Changes: A Mathematical Proof
  - Why Politicians Don't Care About You (With Math!)
  - The Median Voter Theorem (Or: Why Everything Sucks)
  - The Iron Law of Oligarchy
  - Your Congressman: A Prostitute with a Pension
  - Congressional Committees: Available for Purchase
  - The 4-Year Attention Span: Democracy Has ADHD
  - Why No One Can Fix This
  - The Voting Paradox
  - Special Interest Groups: Democracy's Real Winners
  - Why Your Political Tribe Is Also Worthless
  - The Solution Democracy Can't Provide
  - Public Choice Theory: The Nobel Prize for Cynicism
    - What They Actually Maximize
    - The Libertarian Paradox
  - Why This Is Actually Good News
    - Why This Is Liberating
  - Solution
  - Your Choice
  - A Brief History of Human Decision-Making (Spoiler: It's Bad)
  - Why Your Brain Can't Handle Democracy
  - How Government Actually Allocates Money (A Horror Story)
    - The Current Budget Process: Democracy Theater
      - Step 1: Lobbyists Write Checks
        - Step 2: Politicians Pretend to Think
          - Step 3: The Budget Emerges
          - Step 4: Everyone Gets Mad
  - Regulatory Capture: How Industries Write Their Own Rules
    - How to Buy a Democracy: A Practical Guide
    - The Money Machine: How Regulatory Capture Works
    - The Military-Industrial Complex: Murder Inc.
      - The Defense Budget: A Comedy in Three Acts
    - Big Pharma: Your Dealer Has a Lobbyist
    - The Incentive Structure From Hell
    - The Solution They Don't Want
    - Your Democracy: An Auction House

#### knowledge/economics/central-banks.qmd
**Title:** How Central Banks Fund Your Death
**Description:** The War Machine's ATM: How every fiat currency in history has been devalued to fund unpopular wars, and how to bypass the system.
**Stats:** 2,455 words | 487 lines

  - The Problem: Every Fiat Currency in History Has Been Devalued To Fund Unpopular Wars
    - Ancient Rome (3rd Century)
      - Revolutionary France (1790s)
      - Weimar Germany (1920s)
      - United States (1917-present)
  - 1972: When Nixon Weaponized Money Against You
    - Why He Really Did It
      - What Actually Happened
      - The Theft That Followed
  - The Cantillon Effect: Why You're Poor and Raytheon Isn't
  - The Federal Reserve: A Private Corporation That Owns You
    - What They Actually Do
  - Every War Since 1972: Funded by Destroying Your Savings
    - Vietnam War Extension (1972-1975)
      - Gulf War (1991)
      - Iraq War (2003-2011)
      - Afghanistan (2001-2021)
      - The Running Total
  - The {{< var global_pharma_rd_spending_annual >}} Annual Bank Subsidy (Your Money)
    - The Scam
      - What {{< var global_pharma_rd_spending_annual >}} Could Buy Instead
  - Why Humans Can't Reform the Fed (It's Terminal)
    - The Problem with Reform
      - The Only Solution: Bypass It Entirely
  - Why "Just Fund Medical Research More" Is a Lie
    - The Fixed Pie of Human Genius
      - The Resource Reality
    - The Inflation Shell Game (How They Steal Medical Progress)
      - Year 1
      - Year 5 (after "increasing medical research")
    - The Proof: 50 Years of Going Nowhere
      - Medical Research as % of GDP
      - What Actually Grew
    - Why Money Printing Matters: Resources Follow the Printer
      - The Brain Drain Math
  - The 1% Treaty: Redirecting the Death Printer to Life
    - The Current Money Flow
      - A 1% treaty Redirect
      - Why This Works
  - The Historical Precedent: When Markets Funded Victory
    - World War II War Bonds
      - The Difference
  - The Choice: Keep Printing Death or Start Printing Life
    - Option A: Keep the Current System
      - Option B: The 1% Redirect
      - How Tiny 1% Really Is
      - Why This Can Actually Happen
  - Your Money, Your Choice

#### knowledge/problem/genetic-slavery.qmd
**Title:** Genetic Slavery
**Description:** An exploration of how our genes use pain and pleasure to enslave us, forcing actions inconsistent with our rational ethics.
**Stats:** 2,477 words | 305 lines

  - The Selfish Gene Made You Illogical (It Was a Good Idea at the Time)
  - Part 1: Your Brain Was Optimized for a World That Doesn't Exist
    - The Scarcity Brain (Or: Why It's Hard to Stop Eating)
    - The Violence Module (Or: Why We Tend to Prefer Bombs Over Band-Aids)
    - The Tribal Brain: Why Democracy is Struggling
  - Part 2: Genetic Slavery is Literally Killing Us
    - We're Dying from Winning
    - Living in the Most Irrational Timeline
      - Problems you solved
  - Part 3: Why You Can't Just "Be Better"
    - Your Brain is Not Your Friend
    - The Pentagon's Lizard Brain
  - Part 4: The Prison We Built Ourselves
    - You Vote for Monkeys in Human-Skin Suits
    - The Military-Industrial Cortex
  - Part 5: Breaking the Chains
  - Part 6: Breaking Free from Your Programming
    - The First Step: Admitting You're Badly Designed
    - The Solution: Trick the Monkey Brain
    - The Meta-Slavery
  - The Problem With Your Brain

### The Solution

#### knowledge/solution.qmd
**Title:** Solution Overview
**Description:** How to Build Systems That Don't Suck
**Stats:** 2,702 words | 324 lines

  - A 1% treaty
    - Your decentralized institutes of health
      - What the NIH does
      - What your decentralized institutes of health do
        - On Wishocracy
        - Your decentralized framework for drug assessment
        - On Outcome Labels
        - On How Patients Pay Researchers
        - On Why Defense Contractors Should Care
        - On Why 1% Is Just The Beginning
        - On Insurance Companies
        - On the War on Disease
      - Previous Wars on Things
      - This War
        - On Aligning Everyone's Greed
        - On Why This Isn't Clinically Insane
        - On the Meta-Solution
        - On What Comes Next

#### knowledge/solution/1-percent-treaty.qmd
**Title:** A 1% treaty
**Description:** How to Redirect {{< var treaty_annual_funding >}} from War to Medicine - The complete guide to a 1% treaty, the binding global accord that redirects {{< var treaty_annual_funding >}} annually from mil...
**Stats:** 3,501 words | 423 lines

  - The Math
    - How It Works
  - This Isn't a Trade-Off.
    - You Get Two Good Things By Removing One Stupid Thing
      - Good Thing #1: You Become Safer
    - The Dead Capital Problem (Or: Why Bombs Are the Worst Investment Since Tulips)
      - A bridge
      - A missile
  - The Reallocation: How to Redirect {{< var treaty_annual_funding >}} a Year (Legally)
  - The Beautiful Mathematics of Mutual Stupidity Reduction
    - The Proof That Even Generals Can Follow
  - The Blueprint for a Saner World
    - A 1% treaty: Technical Specifications for Global Survival
      - Article 1: The Promise
      - Article 2: The Money Part
      - Article 3: The Enforcement Mechanism
      - Article 4: The Escape Clause
  - Why This Is Actually About National Security (No, Really)
    - Real Threats (That Actually Kill People)
    - Fake Threats (That Countries Spend Trillions On)
  - The Rebranding Campaign: From "Weakness" to "Strategic Genius"
    - "The Strategic Health Defense Initiative"
    - The Talking Points That Make Hawks Sound Like Doves
  - The Implementation Timeline (Or: How to Boil Humanity Slowly)
    - Phase 1: The Whisper Campaign (Months 1-6)
    - Phase 2: The Think Tank Infection (Months 6-12)
    - Phase 3: The Media Blitz (Months 12-18)
    - Phase 4: The Political Theater (Months 18-24)
    - Phase 5: The International Cascade (Months 24-36)
    - Phase 6: The Victory Lap (Month 36+)
  - The Money Flow: Where {{< var treaty_annual_funding >}} Actually Goes
    - The 1% Treaty Fund
    - Year One Projected Outcomes
      - Current System
      - With a 1% treaty + a decentralized framework for drug assessment
  - The Incentive Structure
  - What Happens If This Actually Works
    - The Endgame: Reorienting Global Priorities
    - The Ratchet Effect: How to Boil a Frog (The Frog is the War Machine)
    - The Economic Gold Rush
    - The Vision
  - The Counter-Arguments (And Why They're Stupid)
  - Summary
  - Addendum: The Actual Treaty Text (First Draft)

#### knowledge/solution/dih.qmd
**Title:** Decentralized Institutes of Health
**Description:** A thin coordination protocol that makes doing the highest-ROI thing toward disease eradication the selfish choice for every actor.
**Stats:** 3,414 words | 475 lines

  - The Objective: Total Disease Eradication
    - Why Current Systems Fail
  - The Health-Industrial Complex: Coordinating the War on Disease
    - The Olsonian Problem
    - SHAEF for the War on Disease
    - Why This Framing Matters
  - DIH: The ROI Maximization Protocol
    - Three Core Functions
  - The Core Innovation: Pay for Results
    - The Data Commons: Publish Everything
  - Governance Modules: Wishocracy + Optimocracy
    - Wishocracy: Aggregating Preferences
    - Optimocracy: Maximizing the Metric
    - Why Both Are Needed
  - The Incentive Stack: Making ROI the Selfish Choice
    - How Researchers Get Paid
    - How Politicians Get Aligned
  - How the Money Flows
    - The Architecture
    - The Fund Flow
    - How Allocation Works
    - What Gets Funded: Market Failures Only
  - What DIH Outsources (and Why)
  - How Campaigns Plug In
    - Campaign Lifecycle
    - Why This Matters
  - Anti-Capture Design
    - How DIH Resists Capture
    - The "New FDA" Risk
    - Security Architecture: Multi-Layered Defense
    - Transparent by Default
    - Beyond Medical Research
  - Summary: The Coordination Layer

#### knowledge/solution/wishocracy.qmd
**Title:** Wishocracy
**Description:** How to allocate {{< var treaty_annual_funding >}} and prevent it from getting stolen by parasitic lobbyists and special interests (as is the custom)
**Stats:** 1,291 words | 213 lines

  - How Wishocracy Allocates the 1% Treaty Fund: Decentralized Crowdfunding
    - What your [decentralized framework for drug assessment (dFDA)](dfda.qmd) handles automatically:
    - What Wishocracy Actually Decides:
      - Infrastructure Campaigns
      - Public Goods (Market Failures)
      - Service Provider Bids
    - How It Works: Pairwise Comparisons Between Campaigns
    - Why This Is Actually Needed (Not "Just 3 Parameters")
    - Why This Actually Works (Math Warning)
  - From Priorities to Projects
  - We Already Do This, Just Badly
  - Democracy's Operating System Upgrade

#### knowledge/solution/ai-coordination-army.qmd
**Title:** Building Your AI Coordination Army
**Description:** How to build and deploy autonomous AI agents that coordinate millions of people fighting the War on Disease.
**Stats:** 3,121 words | 254 lines

  - Where Your Agents Get Their Missions (Not From a Management Consultant)
  - The Secret to Success: Cross-Sector Coordination (Forces for Good)
  - Why You Need This (Humans Are Hilariously Bad at Coordination)
  - The Architecture You're Building (It's Simpler Than It Looks)
  - Step 1: Deploy Your Coordination Hub (Your Organization's Digital Slave Labor)
    - To Mobilize Support
    - To Accelerate Research
    - To Build Awareness
    - To Optimize Impact
  - Step 2: Define Each Agent's Mission (From the Task Tree, Not From Your Feelings)
  - Step 3: Enable Competition Between Agents (May the Best Robot Win)
  - How You Keep Control (Preventing the Robot Uprising)
    - AI Proposes
    - You Decide
    - AI Implements
    - You Verify
  - How You Prevent Data Silos (The Tragedy of the Nonprofit Commons)
    - Rule 1 - Share to Play

#### knowledge/solution/dfda.qmd
**Title:** A Decentralized Framework for Drug Assessment
**Description:** Increasing trial capacity {{< var dfda_trial_capacity_multiplier >}}× by giving all patients the right to effortlessly participate in global decentralized clinical trials at 80× lower cost
**Stats:** 4,242 words | 636 lines

  - The Solution: Consumer Reports for Drugs
    - How Companies Register Treatments (5 Minutes, Zero Approval Needed)
      - Net cost to company: $0
    - The Payment Flow (Or: How Everyone Profits Except Disease)
      - Example
      - Company receives
    - Why This Creates Unlimited Research Capacity
      - Traditional model (bottleneck)
  - How It Works: Just Let People Try Stuff (Carefully)
    - The Power of Real-World Evidence (Or: Spying on Sick People for a Good Cause)
    - Introducing FDA.gov 2.0: Now With 80% Less Death
    - Step 1: Type in What's Killing You
    - Step 2: See What Actually Works (Based on Reality, Not Theory)
    - Step 2.5: See the Future (With Financially-Backed Predictions)
      - Why Trust This?
    - Step 3: Join a Trial from Your Couch (While Dying Comfortably)
    - Step 4: Get Drugs Delivered Like Pizza (But More Life-Saving)
    - Step 5: Publish Results
    - Step 6: Everyone Benefits from Everyone's Suffering
  - The Partnership Approach: Building Rails, Not Trains
    - The Players Already in the Game
    - The Integration Consortium
    - Why They'll Cooperate
    - Federated, Not Centralized
  - The Money Shot: How to Save 95% on Not Killing People
    - The Itemized Receipt of Eliminated Stupidity
  - Why This Works: The Mathematical Impossibility of Committees
    - The Math That Proves Centralization Can't Work
    - Why 200 People Can't Replace 8 Billion
    - The Solution: Let 8 Billion Experts Make 8 Billion Decisions
      - Current system
  - Real Examples of This Working (While the FDA Wasn't Looking)
    - The Oxford Recovery Trial: How the British Accidentally Saved Medicine
    - Wikipedia for Whether You'll Die
      - Current Treatments Ranked by Not-Dying Score
    - Become a Scientist from Your Couch
  - Your Personal Death-Prevention Assistant: The FDAi
  - The Digital Twin Safe: Your Medical Data's Panic Room
  - Outcome Labels: Nutrition Facts for Drugs
    - Cognitive Improvements
      - Side Effects
  - The Disease Eradication Act: Making It Legal to Not Die
  - The Future: Where Death Becomes Embarrassing
    - 2027: The Beginning of the End of Dying Slowly
    - 2030: Big Pharma Pivots or Dies
    - 2035: The Great Revelation
    - 2050: Death Becomes Opt-In
    - How Your Framework Actually Works

#### knowledge/solution/war-on-disease.qmd
**Title:** The War on Disease
**Description:** Designing the First War to Win
**Stats:** 1,216 words | 157 lines

  - On How to Design a War That Actually Ends
    - On Competition Versus Monopoly
  - On The Part Where Other Problems Accidentally Get Solved
    - On the War on Drugs
      - On the War on Poverty
      - On the War on Terror
      - On the War on Crime
  - On The Real Victory
    - On Why Every Previous War Failed
      - On Why This War Will Win
      - On What Winning Looks Like
      - Year 1 Targets
      - Year 10 Targets

#### knowledge/solution/aligning-incentives.qmd
**Title:** Aligning Incentives
**Description:** How to Make the Right Choice More Profitable Than the Wrong One
**Stats:** 3,060 words | 453 lines

  - Defense Contractors: Teaching Merchants of Death to Love Life
    - Their Current Business Model (It's Actually Terrible)
    - Here's Your Better Offer: VICTORY Incentive Alignment Bonds
    - Why They'll Take the Deal
      - The Portfolio Math
      - The PR Victory
      - The Competitive Pressure
    - The Simple Pitch
    - The Implementation Playbook
  - Insurance Companies: The Accidentally Aligned Industry
    - Their Current Death Spiral
    - Your Salvation Offer
      - The Math They Can't Refuse
      - The Obvious Math
      - The Implementation
    - Why They're Your Natural Allies
  - Pharmaceutical Companies: Converting Drug Dealers to Drug Curers
    - Their Current Trap
    - The Cost Elimination
    - The Math That Converts Them
      - Current Pharma Economics
      - New System - Cost Elimination
  - How your decentralized institutes of health eliminate trial costs
    - Pharma's New Business Model: Volume Over Blockbusters
      - Current model
      - The new decentralized model
    - How to Get Them Onboard
  - Politicians: Hacking Democracy's Source Code
    - Their Current Misery
    - Your Political Welfare Program
      - The Money Pipeline
      - The Vote Harvest
      - The Jobs Program
    - The Bipartisan Beauty
  - Billionaires: The Easiest Marks
    - What They Really Want
    - Your Irresistible Package
      - The Investment
      - The Legacy
      - The Insurance
    - The Conversion Sequence
  - The Domino Effect: How This Cascade Works
    - The Sequence
    - Why This Can Work: Solving the Collective Action Problem
      - Why the cascade can happen (not "must" happen)
  - The Master Key: Greed
  - The Two-Engine System: Why You Need Both
    - Engine 1: VICTORY [Incentive Alignment Bonds](https://iab.warondisease.org) (The Initial Alignment)
    - Engine 2: [Incentive Alignment Bonds](https://iab.warondisease.org) (The Scaling Engine)
    - VICTORY Impact Alignment Bonds
    - The Endgame

#### knowledge/solution/incentive-alignment-bonds.qmd
**Title:** Incentive Alignment Bonds
**Description:** A new financial instrument for aligning political incentives with public goods
**Stats:** 8,935 words | 1,067 lines

  - A Novel Approach to Political Economy
    - The Core Problem: Good Ideas Die in Committee
    - What You Need: Legal Bribery That Isn't Technically Bribery
    - Definition: What Are Incentive Alignment Bonds?
      - How IABs Differ from Social Impact Bonds
    - How Incentive Alignment Bonds Work – The Simple Version
      - Step 1: Define a Measurable Outcome
      - Step 2: Raise Capital
      - Step 3: Fund Outcomes, Reward Politicians Indirectly
      - Step 4: Make Politicians Care (Without Paying Them)
    - 4a. The Three-Layer Architecture (How to Not Go to Prison)
      - Layer A: Outcome and Policy Scoring (Data Only)
      - Layer B: Electoral and Reputational Benefits (Separate Actors)
      - Layer C: Post-Office Career Benefits (The Goldman Sachs Board Problem)
      - Legal Entity Separation
    - 4b. A Worked Example: How Senator Smith Votes Yes on the 1% Treaty
      - The Primary Metrics We're Maximizing
      - The Politician's Utility Function
      - The Public Good Score
      - How Score Translates to Utility
      - The Setup
      - The Old Calculus (Without IABs)
      - The New Calculus (With IABs)
      - What Actually Happens
      - Post-Treaty: The Numbers
      - The Math for VICTORY Incentive Alignment Bond Investors
    - Why This Is Not Bribery (Legally Speaking)
    - Why IABs Are Not Just Social Impact Bonds
    - How This Plugs Into the 1% Treaty (The Part Where It All Comes Together)
    - 7a. The Two Engines: Financial and Political
    - Objections and Failure Modes
      - Objection 1: "Won't politicians game the metrics?"
      - Objection 2: "Isn't this just rich people buying policy?"
      - Objection 3: "What if governments take the health gains but reverse the policy later?"
      - Objection 4: "Is this realistic at a global scale?"
    - Why This Matters for Ending War and Disease
    - Summary: The Mechanism in One Sentence
    - Why 10%: The Scaling Engine {#sec-why-ten-pct-scaling-engine}
      - The Goal Isn't a 1% Treaty. The Goal Is 100%.
      - IABs Are the Political Ratchet
      - The Math Changes Everything
      - Why VICTORY Incentive Alignment Bonds Alone Won't Scale
      - The Alternative Is Stagnation
      - Bottom Line
    - Beyond the 1% Treaty: IABs as a General Governance Tool
      - Climate Change
      - Nuclear Disarmament
      - Pandemic Preparedness
      - The General Template
      - Why This Hasn't Been Done Before
      - The Bigger Picture
    - Summary: What IABs Actually Are

### The Evidence

#### knowledge/proof.qmd
**Title:** The Proof: Overview
**Description:** This Already Works - Oxford proved 82X efficiency. Switzerland proved peace pays. History proved {{< var global_population_activism_threshold_pct >}} consistently wins. War bonds proved capitalism bea...
**Stats:** 1,393 words | 212 lines

  - Oxford RECOVERY: The {{< var recovery_trial_cost_reduction_factor >}}× Proof
  - Switzerland: The 200-Year Peace Dividend
    - Result
  - War Bonds: How Capitalism Beat Fascism
  - The Landmine Treaty: Citizens Beat Armies
  - The {{< var global_population_activism_threshold_pct >}} Rule
  - The Post-WW2 Economic Miracle: History's Greatest Peace Dividend
  - You Have Advantages They Didn't
  - The Political Precedents: How to Win
    - Creating Binding International Law
    - Achieving a Political Tipping Point
  - The Financial Precedents: How to Fund It
    - Mobilizing Mass Public Capital
      - The Precedent: WWII War Bonds
    - B. Building a New Global Health Institution
    - C. Pricing the Political Risk
  - 4. The Cautionary Tales: How Not to Fail
    - A. Don't Bring a Moral Argument to a Financial Fight
    - B. Don't Have a Diffuse, Unactionable Goal
      - The Precedent: Occupy Wall Street
  - In This Section
  - Additional Evidence

#### knowledge/proof/historical-precedents.qmd
**Title:** Historical Precedents
**Description:** Why This Isn't Insane - An analysis of historical movements and financial models that prove the core mechanics of a 1% treaty are not new ideas, but rather the application of proven models for mass mo...
**Stats:** 2,259 words | 236 lines

  - Humans Doing Smart Things (Accidentally): A Collection
    - That Time Humans Banned Landmines (Yes, Really)
    - War Bonds: That Time Grandma Funded WW2
    - The Global Fund (Proof That New Health Institutions Can Exist)
    - Post-WW2: That Time America Accidentally Discovered Peace Is Profitable
    - The 1990s: When the Berlin Wall Fell and Wallets Exploded
    - Switzerland: 200 Years of Not Shooting Anyone = Being Very Rich
      - The results
    - The {{< var global_population_activism_threshold_pct >}} Rule: The Cheat Code for Democracy
      - Historical proof
  - When Good Intentions Met Reality (And Lost)
    - Eisenhower's Warning: A 5-Star General Tried to Tell You
    - The Nuclear Freeze Movement: Millions of People, Zero Results
    - Occupy Wall Street: When "We're Angry" Isn't a Strategy
  - On How Rich People Made Money Doing Crazy Things (And Why That Matters)
    - On The Time Junk Bonds Saved Capitalism
      - Michael Milken & High-Yield ("Junk") Bonds
    - On The Time George Soros Broke England
      - George Soros & The Quantum Fund
    - On When Smart People Lost All Their Money (The Cautionary Tales)
  - 4. The Ultimate Failsafe: The Worst-Case Scenario is Still a Win
    - Why?

#### knowledge/proof/body-as-repairable-machine.qmd
**Title:** You Are a Meat Robot
**Description:** Aging, disease, and death are engineering problems with engineering solutions
**Stats:** 1,462 words | 199 lines

  - Death is a Technical Problem
  - You Are a Self-Repairing Meat Robot
  - Part 2: We've Already Started Fixing the Machine
    - Exhibit A: We Can Grow New Parts
    - Exhibit B: We Can Reprogram Your Cells
    - Exhibit C: We're Debugging Your Code
  - The Car Restoration Analogy
    - Why Death is Just Deferred Maintenance
  - Part 4: The Proof That Aging is Reversible
    - Nature Already Does It
    - We've Already Reversed Aging (In Mice... and Human Cells)
    - The Hallmarks of Aging (All Fixable)
  - Part 5: Why We Haven't Fixed You Yet (It's Just Money)
    - The Manhattan Project for Not Dying
    - The Economics of Mortality
  - The Conclusion

#### knowledge/economics/1-pct-treaty-impact.qmd
**Title:** The 1% Treaty: Health and Economic Impact of Redirecting 1% of Global Military Spending to Pragmatic Clinical Trials
**Description:** At current trial capacity, finding first treatments for all {{< var diseases_without_effective_treatment >}} untreated diseases would take ~{{< var status_quo_queue_clearance_years >}}. Redirecting {{...
**Stats:** 27,183 words | 2,634 lines

  - Abstract
  - Interpreting the {{< var dfda_trial_capacity_plus_efficacy_lag_years >}}-Year Timeline Figure
  - Key Findings
  - How Pragmatic Trials Increase Safety
  - Introduction
    - Historical Context: When Grand Challenges Succeed
    - The Medical Research Bottleneck
    - Addressing Skepticism: Why This Differs from Failed Megaprojects
    - Contribution to Literature
  - Research Hypothesis
  - Nomenclature and Key Terms
  - Problem Statement
    - Current Resource Allocation
      - Disease treatment vs. curing disease
    - Mortality and Morbidity Burden
  - How It Works
  - A Decentralized Framework for Drug Assessment
    - Trial Cost Reduction
    - Enhanced Safety Monitoring
    - Comparative Effectiveness Rankings
      - How Comparative Effectiveness Data Is Collected
    - Outcome Labels
  - Summary of Results
    - Total Economic Value
        - Uncertainty Analysis: Total Economic Value
    - Research Acceleration
    - Treatment Timeline Acceleration
    - Suffering Reduction
    - Lives Saved
    - DALYs Averted
    - Why "Eventually Avoidable" Matters
  - Why {{< var treaty_reduction_pct >}} Is Enough
    - 1. The Peace Dividend
    - 2. The Research Efficiency Dividend
    - 3. 15–40 "NIH equivalents" of new research capacity
  - How It Increases National Security
    - What doesn't change
    - What improves
    - The De-escalation Trajectory
    - Why The Ratchet Works: The IAB Scaling Engine
  - Political Economy and Financing
    - Incentive Alignment Bonds
      - Mechanism Architecture
      - Comparative Static Analysis: Senator Smith
      - Stakeholder Alignment
      - VICTORY Incentive Alignment Bonds
      - Legal and Ethical Framework
      - Generalized Governance Application
  - Dominance Analysis
    - Quantitative Comparison
    - Why This Dominates
  - Methodology
  - Cost-Benefit Framework
    - Cost Components
    - Benefit Components
  - ROI Calculation
  - Cost-Effectiveness Analysis
    - Expected Value Under Political Uncertainty
      - Uncertainty in Risk-Adjusted Cost-Effectiveness
      - Uncertainty in Cost-Effectiveness (Conditional on Success)
    - Treaty Campaign Leverage vs Direct Funding
      - Why Billionaires Buy Lottery Tickets Instead of the Casino
      - Numerical Comparison: Treaty vs Direct Funding
      - Direct Funding Scenario
      - Treaty Campaign Advantage
    - Detailed NPV Formulas
      - NPV of Costs
      - NPV of Benefits
      - Return on Investment
      - NPV of Regulatory Delay Avoidance
  - Quality-Adjusted Life Year (QALY) Valuation
    - QALY Calculation Model
  - Economist Verification: Complete Derivation Chains
    - 1. Trial Capacity Multiplier Derivation ({{< var dfda_trial_capacity_multiplier >}})
    - 2. Timeline Shift Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_years >}})
    - 3. DALYs Averted Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_dalys >}})
    - 4. Cost per DALY Derivation ({{< var treaty_cost_per_daly_trial_capacity_plus_efficacy_lag >}})
    - 5. ROI Derivation (Conservative: {{< var dfda_roi_rd_only >}})
    - 6. ROI Derivation (Complete: {{< var treaty_roi_trial_capacity_plus_efficacy_lag >}})
    - 7. Lives Saved Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_lives_saved >}})
    - 8. Regulatory Delay Elimination Derivation
    - 9. Annual Recurring Benefits Derivation
    - Verification Summary
  - Counterfactual Baseline Specification
  - Peace Dividend Calculation Methodology
    - Economic benefits of reduced military spending
  - Research Acceleration Mechanism
    - Treatment Discovery Through Therapeutic Space Exploration
      - The Unexplored Therapeutic Frontier
      - Current Exploration Rate vs. Therapeutic Space
    - Addressing the Returns Question: Diminishing, Linear, or Compounding?
      - Why Diminishing Returns Is Unlikely (We Haven't Started Looking)
      - The Case for Compounding Returns
      - Mathematical Framework: When Would Diminishing Returns Dominate?
      - The Conservative Default: Linear Assumption
  - Data Sources and Primary Inputs
    - Military and Conflict Data
      - Clinical Trial Economics
      - Health Economics
      - Economic Parameters
  - Sensitivity Analysis Approach
  - Key Analytical Assumptions
    - Strategic Stability Assumption
    - Linear Scaling Assumption
    - Adoption Rate Assumptions
    - Cost Reduction Assumptions
      - Empirical basis
    - Historical Precedent: Pre-1962 Physician-Led Efficacy Trials
      - Historical operational model
      - Implications for generalizability
    - Political Feasibility Assumption
    - Expected Value Analysis Accounting for Political Risk
    - Time Inconsistency and Commitment Credibility
    - Technology Constancy Assumption
    - Data Quality and Availability
  - Scenario Analysis: Conservative Case
    - ROI Derivation
    - Where the Money Comes From
    - How Treaty Funding Is Allocated
    - Returns
        - Uncertainty Analysis: Combined Annual Benefits
    - Cost-Effectiveness: Cost-Saving Health Intervention
      - Incremental Cost-Effectiveness Ratio (ICER)
      - Comparative Cost-Effectiveness vs. GiveWell Top Charities
    - Self-Funding Mechanism Through Military Budget Redirection
  - Scenario Analysis: Complete Case
    - Annual Recurring Benefits Breakdown
      - Total recurring annual benefits
      - Complete Case ROI
    - Trial Capacity Scaling
  - Individual-Level Economic Impact
  - Comparative Effectiveness
    - Comprehensive Comparison
    - Linear vs. Systemic Leverage
    - The Critical Difference
      - Translation
  - Who Benefits and How
  - Adoption Dynamics: Game-Theoretic Analysis
  - Implementation Strategy
    - Step 1: Global Mandate (The Philanthropic Catalyst)
    - Step 2: Sell $1B in VICTORY [Incentive Alignment Bonds](https://iab.warondisease.org)
    - Step 3: Implment the Legislative Strategy
    - Step 4: Build the Infrastructure
    - Step 5: Eradicate Disease
    - Campaign Budget Breakdown
  - Detailed Technical References
  - Risk Analysis and Mitigation
    - The "But Politicians Won't Do It" Problem
    - Safety Concerns
    - Patient Agency and Autonomy
    - Accountability measures
  - Limitations and Uncertainties
    - Adoption Timeline Uncertainty
    - Cost Reduction Assumptions
    - Generalizability: Meta-Analysis of 108+ Trials, Not a Single Case Study
    - Diminishing Returns in Research Productivity
      - Why this critique may not apply
      - Distinction
      - The Myth of Diminishing Returns
        - Uncertainty Analysis
    - Pragmatic Trial Internal Validity and Selection Bias
      - Mitigation strategies
    - QALY Calculation Uncertainties
    - Data Limitations
    - Military Spending Data
    - Clinical Trial Market Sizing
    - QALY Valuation Thresholds
    - Generalizability Constraints
    - Political Feasibility
    - Institutional Capacity
    - Healthcare System Integration
    - Uncertainty Quantification
    - Primary Risk Factors
    - Scenario Analysis Robustness
    - General Equilibrium Effects
    - Conditional Benefits Interpretation
    - Limitations Summary
  - Policy Implications
    - National Health Budgets
    - International Development Priorities
    - Military Budget Allocation
    - Global Health Funding Mechanisms
    - Implementation Pathway
    - Bottom Line for Policymakers
  - Treaty Adoption: Political Will and Diplomatic Strategy
    - Why Simultaneous Commitment Works: Escaping the Prisoner's Dilemma
    - Historical Treaty Precedents
    - Demonstrating Feasibility
    - Adoption Pathway
  - Conclusion

#### knowledge/call-to-action/your-personal-benefits.qmd
**Title:** Your Personal Benefits
**Description:** What You Actually Get From This
**Stats:** 434 words | 73 lines

  - Your Actual Odds Right Now
  - What You Actually Get
  - If you're healthy (for now)
    - If you have money
      - If you have a family
    - The Math
    - Uncertainty Analysis
    - The Bottom Line

#### knowledge/futures.qmd
**Title:** The Two Futures
**Description:** Two timelines diverge from this moment. One ends in extinction, the other in transcendence. The only difference is a 1% budget reallocation.
**Stats:** 285 words | 44 lines

  - Path A: Moronia
  - Path B: Wishonia
  - The Only Variable
  - The Two Paths

#### knowledge/futures/moronia.qmd
**Title:** The Cautionary Tale of Moronia
**Description:** How a civilization decided murdered itself with machines instead of eradicating diseases and transcending their biology
**Stats:** 5,023 words | 726 lines

  - The Discovery (And Why I Regret Making It)
  - What I Tried to Tell Them
  - How They Killed Themselves: A Timeline
    - The Economics of Extinction: Why Collapse Was Inevitable
      - The Olsonian Trap
      - The Prisoners' Dilemma Arms Race
      - The Incentive Inversion Cascade
      - The Coordination Tax
    - Year Zero: Already Broken (Much Like You)
    - Year 1-2: The Cognitive Collapse (A Natural Experiment)
      - Here's how it killed their decision-making
    - Year 3: The Truth Apocalypse (When Reality Became Optional)
    - Year 5: The Arms Race (When Major Powers Built the Thing They Were Warned Not To)
      - Who built these death-maximizers
      - The budget allocation
    - Year 7: The Parasite Economy (An Incentive Structure Study)
      - Why crime pays
    - Year 8: The Gestation Collapse (Exponential Crime)
      - Human criminal gestation
      - AI criminal gestation
      - The math
    - Year 10: The Currency Collapse (When Many Become Parasites)
      - The dominoes
    - Year 15: The Gap (Peak Achievement)
      - Children born in Year Zero (now 15)
  - The Numbers (That Moronians Ignored)
    - What Moronians spent (Year Zero through Year 15)
      - What \$80T could have bought
  - The Second Law of Civilizational Thermodynamics
  - A Day in Moronian Life (Year 25)
  - The Diseases Moronia Didn't Cure
  - Moronia's Greatest Innovations
    - The Peacekeeper 3000
      - Project Guardian Angel
        - The Harmony Protocol
  - Treaties Moronia Rejected
  - Moronia's Corporate Champions
  - Victory
  - The Last Moronian Message
  - The Path Moronia Didn't Take
  - The Lesson I Learned
  - Year 25: Peak Gollum (My Precious Military Budget)
    - Final Moronian Budget
      - Final statistics
  - Moronia's Obituary
  - My Warning to You

#### knowledge/futures/wishonia.qmd
**Title:** Wishonia
**Description:** How My Planet Works and Why You Should Copy Our Homework
**Stats:** 2,015 words | 288 lines

  - How My Planet Works
  - What the Optimized World Looks Like
    - The Three Supers
    - Biology Becomes Software
  - A Day in the Optimized Life
  - The Diseases That Stopped Existing
  - The Peace Dividend Economy
    - Annual Global Redirected Funds
  - Your Corporate Heroes
  - Your New Problems
  - The Three Supers Complete
  - Your Personal Future
  - What Fixing Health Fixed
  - Reality Check
  - Message from the Future
  - What Comes After
  - Your Two Paths

#### knowledge/appendix/faq.qmd
**Title:** Frequently Asked Objections
**Description:** For the Reasonably Skeptical
**Stats:** 3,685 words | 518 lines

  - "We Need the Military Budget"
  - "Big Pharma Will Block This"
  - "You Can't Trust 8 Billion People"
  - "What About National Sovereignty?"
  - "This Is Socialism"
  - "The FDA Exists for a Reason"
  - "What If Countries Cheat?"
  - "You're Being Unfair to the NIH"
  - "This Sounds Like a Scam"
  - "You Can't Cure Aging"
  - "I'm Just One Person"
  - "Politicians Will Steal the Money"
  - "Reform the System Instead"
  - "This Is Politically Impossible"
  - "I Don't Trust Blockchain"
  - "What If the Science Is Wrong?"
  - "I'll Wait and See"
  - "I Don't Have Time"
  - "This Is Unrealistic"
  - "War Is Human Nature"
  - "All Wars on X Have Failed"
  - "This Sounds Like Bribery"
  - "This Isn't a Real Movement"
  - "It's Unenforceable"
  - "You Can't Verify 280M People"
  - "Blockchain Harms the Environment"
  - "Billionaires Will Seize Control"
  - "Why Not Just Use Philanthropy?"
  - "How Do You Prevent Waste?"
  - "Why Not Just Increase Health Funding?"
  - "What About Defense Industry Jobs?"
  - "This Disrespects Soldiers"
  - "This Violates Election Law"
  - "What If Major Powers Sabotage It?"
  - Conclusion

### The Plan

#### knowledge/strategy/roadmap.qmd
**Title:** The Roadmap to End War and Disease
**Description:** Step-by-step instructions for bootstrapping a global revolution by bribing everyone into accidentally saving humanity while getting rich.
**Stats:** 2,839 words | 265 lines

  - High-Level Strategy: The Three-Step Recipe for Not Dying
    - Step 1: Collect Papers from Rich People
    - Step 2: Pay Humans to Click YES
    - Step 3: Apply Papers to Politicians Until Treaty Happens
  - Detailed Execution: The Five-Step Cascade
    - Step 2: The Great Internet Clicking
      - Step 4: Treaty Achieves Existence
  - Tactical Implementation: The Sacred (Legal) Bribery Sequence
    - (Legal) Bribe Category #1: Rich People (The Paper Collectors)
      - The Specific Offer to Bomb Makers
      - Option A (Current Job)
      - Option B (Your Offer)
    - (Legal) Bribe Category #2: The True Believers (Early Adopters Who Want Control)
    - (Legal) Bribe Category #3: Regular People (Everyone Else)
    - (Legal) Bribe Category #4: Politicians (The Elected Paper Recipients)
      - The Package
      - The choice you give them
  - The Paper Collection Timeline: From $0 to Ending Death
  - The Legal Architecture: How to Be a Charity, a Lobbying Group, and a Hedge Fund Simultaneously
  - The Political Strategy: Co-Opt, Don't Compete
  - Your Next Steps
  - Phase 4+: The Expansion Phases (Years 4-50)
    - Why Expansion Is Built Into The System
    - Here's Why It Keeps Growing
    - The Endgame

#### knowledge/strategy/nonprofit-coalition-strategy.qmd
**Title:** Why Every Nonprofit Should Support a 1% treaty
**Description:** The strategic case for nonprofit coalition-building around a 1% treaty - escaping zero-sum competition through resource reallocation.
**Stats:** 2,164 words | 313 lines

  - The Single Highest-ROI Intervention Available
    - Why This Applies to YOUR Organization
  - "But Shouldn't Nonprofits Focus on Their Core Mission?"
  - The Zero-Sum Trap vs. The Positive-Sum Solution
  - "Why Now?" Because the Window Is Open
  - Historical Precedent: This Has Worked Before
  - "Why Not Just Run Decentralized Trials Ourselves?"
  - A 1% treaty Is a Rising Tide That Lifts Every Mission
    - Health
    - Climate
    - Poverty
    - Global Stability
    - Nonprofit Impact
  - The Moral Argument Is Simple
  - Why Nonprofits Must Prioritize a 1% treaty (Short Term)
  - The Ask Is Small, The Upside Is Massive
  - The Bottom Line

#### knowledge/legal/legal-framework.qmd
**Title:** Legal Architecture
**Description:** How to Stay Out of Prison While Revolutionizing Global Healthcare
**Stats:** 2,229 words | 391 lines

  - Entity #1: The 501(c)(3) Public Charity ("The Brain")
    - What It Does
  - Entity #2: The 501(c)(4) Social Welfare Org ("The Sword")
  - Entity #3: The Victory Corporation ("The Engine")
    - What It Does
  - Entity #4: The DIH Foundation ("The Soul")
    - What It Does
  - Why This Four-Part Structure Works
    - Legal Specialization
    - Firewall Protection
    - Risk Distribution
  - Multi-Jurisdiction Strategy (How to Not Put All Eggs in One Regulatory Basket)
  - Organizational Structure: The For-Profit Management Company
    - The General Staff (G-Staff)
  - Nonprofit Foundation Governance
  - Securities Law
  - Election Law
  - Treaty Framework
  - Risk Mitigation (When They Come For You)
    - The Legal Attack Vectors
      - Securities Fraud
      - Election Law Violations
      - Tax Evasion
      - RICO/Conspiracy
    - The Lawyer Budget
      - Budget: $100M for lawyers
      - The Strategy
  - The Escape Routes (If Everything Goes Wrong)
  - Regulatory Reform Agenda
    - HHS Policy Recommendations
      - Key Policy Objectives
      - Projected Impact
    - Priority Regulations for Modification
      - High-Priority Streamlining Targets
      - Revolutionary Exemptions for Certified Platforms

#### knowledge/legal/securities-law.qmd
**Title:** Securities Law
**Description:** How to Sell Hope Without Going to Prison
**Stats:** 1,672 words | 319 lines

  - The Core Problem: Everything Is a Security
  - The Exemptions That Save You
    - Regulation D: Your Best Friend
      - Rule 506(b): The Quiet Offering
        - Rule 506(c): The Loud Offering
    - Accredited Investors: Your Target Market
  - Structuring VICTORY Incentive Alignment Bonds: Debt Not Equity
    - Debt Advantages
    - The Structure
    - Why This Works
  - The Disclosure Documents: Covering Your Ass
    - Required Disclosures
      - Risk Factors (Make Them Terrifying)
      - Use of Funds
      - Conflicts of Interest
  - The Marketing Rules: What You Can and Can't Say
    - What You CAN Say (Under 506(c))
    - What You CAN'T Say
    - The Magic Words That Protect You
  - International Complications: Multiple Jurisdictions
    - The Swiss Foundation and US C-Corp Structure
    - The Regulatory Arbitrage
    - The Blockchain Advantage
  - The Secondary Market: Making Them Liquid
    - Alternative Trading Systems (ATS)
    - Token Wrapper Strategy
    - Market Making
  - Enforcement and Penalties: What Happens If You Screw Up
    - Civil Penalties
    - Criminal Penalties
    - How to Avoid Prison
  - The Compliance Infrastructure
    - KYC/AML Systems
    - Investment Process
    - Ongoing Compliance
  - The Endgame: Going Public
    - The IPO Option
    - The Acquisition Option
  - Conclusion
  - Implementation Resources

#### knowledge/legal/election-law.qmd
**Title:** Election Law
**Description:** How to Buy Politicians Legally
**Stats:** 1,555 words | 308 lines

  - The Legal Landscape: Money Is Speech
    - Citizens United Changed Everything
      - Super PACs (Independent Expenditure Committees)
  - The Super PAC Strategy
    - Setting Up "Cure Not Kill PAC"
      - Formation (One Day)
      - The Legal Requirements
      - What You Can Do
  - The 501(c)(4) Dark Money Machine
    - Your Action Fund (The Dark Money Vehicle)
      - The 51/49 Rule
      - How to Stay Legal
  - Campaign Finance Jujitsu
    - Making Opposition Expensive
      - The Primary Threat
      - The Bidding War
      - The Overwhelming Force Doctrine
  - State and Local Compliance
    - The Nightmare States
    - The Compliance Strategy
    - Local Elections
  - The Media Buy Strategy
    - Surgical Strikes
      - Early and Often
      - The Saturation Approach
      - Digital Micro-Targeting
  - The Ground Game
    - Paid "Volunteers"
    - The Petition Army
  - Enforcement: What Happens If You Break Rules
    - FEC Enforcement (LOL)
    - DOJ Enforcement (Rare but Real)
    - State Enforcement (Varies)
  - The Lobbying Registration Trap
    - When You Must Register
    - When You Don't
  - International Considerations
    - Foreign Nationals Ban
    - Treaty Promotion
  - The Victory Conditions
    - Phase 1: Create Fear (Months 1-6)
    - Phase 2: Offer Carrots (Months 7-12)
    - Phase 3: Ensure Victory (Months 13-18)
  - Conclusion: Democracy as Designed
  - Legal Notice

#### knowledge/legal/treaty-framework.qmd
**Title:** Treaty Framework
**Description:** How to use international law and incentive structures to make funding cures more profitable than buying weapons
**Stats:** 1,675 words | 342 lines

  - Why Treaties Matter (Sort Of)
    - What Treaties Actually Do
      - Supremacy Clause (US Constitution, Article VI)
        - International Law Principle: Pacta Sunt Servanda
      - The Ratchet Effect
  - A 1% treaty Structure
    - The Core Provisions
      - Article 1: Definitions
        - Article 2: The Obligation
          - Article 3: Enforcement
          - Article 4: Expansion
    - Key Provisions
      - The Prisoner's Dilemma Solver
      - The Political Cover
      - The Escape Clause That Isn't
  - Enforcement (The Hard Part)
    - Traditional Mechanisms (Weak)
      - Public Transparency
      - Economic Consequences
      - Legal Standing
    - The Smart Contract Approach
      - Blockchain Treaty Execution
      - The Oracle Problem
    - What Actually Works (Incentives)
  - Avoiding the Pitfalls
    - Common Treaty Killers
      - Reservation Games
      - Ratification Delays
      - Creative Accounting
      - Parliamentary Obstacles
  - The Expansion Framework
    - From 1% to More
      - Year 1-2: Proof of Concept
        - Year 3-5: Possible Expansion
          - Year 5-10: If Momentum Continues
          - Long Term: Optimistic Scenario
  - The Model Treaty Text
    - Preamble
    - Operative Clauses
  - How This Actually Works
  - Implementation Resources

#### knowledge/economics/victory-bonds.qmd
**Title:** VICTORY Incentive Alignment Bonds
**Description:** Step-by-step guide to creating perpetual bonds that fund a 1% treaty campaign
**Stats:** 3,583 words | 465 lines

  - VICTORY Incentive Alignment Bonds
  - What You're Actually Building
  - The Four Phases of Making Everyone Rich While Saving Humanity
    - Phase 1: Collect Papers From People With Too Many Papers
      - Who has that many papers
    - Phase 2: Spend the Papers Correctly
    - Phase 3: Turn On the Money Faucet
    - Phase 4: Watch Money Multiply Like Rabbits
  - Calculate Your Numbers for Investors
    - Show Them Where the Papers Come From
    - When Math Becomes Obscene
      - Even if you're extremely pessimistic
      - This isn't complicated math
    - How Returns Scale From "Obscene" to "Is This Even Legal?"
      - Why this actually happens
    - Structure the Security Package
  - What Full Success Looks Like
  - Explain the {{< var dih_treasury_medical_research_pct >}}/{{< var victory_bond_funding_pct >}}/{{< var iab_political_incentive_funding_pct >}} Split
  - Set Up the Legal Structure
    - Structure the Bond Instrument
    - Create Milestone-Based Releases
    - Address Each Risk Category
      - Project Risks
      - Investor-Specific Risks
  - What This Beats (Spoiler: Everything)
    - Show Investors This Table
  - The Expansion Flywheel
    - Explain the flywheel to investors
  - Set Minimum Investment Thresholds
    - Structure Your Minimums
    - Draft Your Term Sheet
  - When Rich People Ask Difficult Questions
    - "This sounds like a Ponzi scheme run by someone who failed math."
    - "What happens when this fails and I lose my billion dollars?"
    - "What could possibly go wrong?"
      - Project Risks
      - Investor Risks
    - "How is this different from just donating to charity?"
    - When they want detailed financials
      - Direct them
  - The One-Page Summary That Makes Calculators Weep
    - What you get
    - What could go wrong
  - Related Implementation Guides
    - For detailed execution plans
      - The core mechanism is stupid simple

#### knowledge/strategy/legislation-package.qmd
**Title:** The Legislation Package
**Description:** How to Write Laws That Actually Pass
**Stats:** 2,166 words | 365 lines

  - The Treaty Implementation Act: Making It Real
    - The Core Provisions
      - Section 1: Authorization
        - Section 2: Protection Mechanisms
          - Section 3: The Candy for Congress
    - Why Politicians Will Vote Yes
      - For Republicans
      - For Democrats
      - For Everyone
    - The Legislative Hack
  - The Authorization Act for your Decentralized Institutes of Health: Creating Your Machine
    - The Structure Designed to Resist Capture
      - Section 1: Establishment
        - Section 2: Powers
          - Section 3: Governance
    - The Trojan Horse Approach
    - The Poison Pills for Opposition
  - The Parallel Track Act: Your Regulatory Revolution
    - The Legal Architecture
      - Section 1: The Parallel Pathway
        - Section 3: The Data Revolution
    - How to Sell This to Cowards
      - The Safety Argument
      - The Freedom Argument
      - The Innovation Argument
    - The Implementation Trick
  - The Right to Try Expansion Act: Medical Freedom
    - The Provisions That Matter
      - Section 1: Absolute Right
        - Section 2: The Subsidy System
          - Section 3: The Data Exchange
    - The Emotional Blackmail Strategy
      - The Talking Points
    - The Coalition Building
  - The Budget Reallocation Act: Moving the Money
    - The Money Flow Mechanics
      - Section 1: Automatic Transfer
        - Section 2: The Protection Clauses
          - Section 3: The Growth Mechanism
    - Making It Robust
      - The Constitutional Approach
      - The Political Protection
      - The Technical Protection
    - The Incremental Implementation
  - The Legislative Strategy: Order of Operations
    - Phase 1: Build Momentum
    - Phase 2: Create Infrastructure
    - Phase 3: Fund the System
    - The Omnibus Strategy
  - Conclusion: Democracy Theater at Its Finest

#### knowledge/strategy/global-referendum.qmd
**Title:** Global Referendum Strategy
**Description:** Comprehensive strategy for implementing a secure, globally verifiable referendum to demonstrate public support for a 1% treaty, including implementation, verification, and viral marketing approaches.
**Stats:** 2,226 words | 369 lines

  - On What You're Actually Trying to Do (The Boring But Necessary Part)
    - The Goal
  - System Architecture
  - On Stopping People from Cheating (The Hard Part)
    - On Why You Need Multiple Layers of "Prove You're Human"
    - AI-Powered Fraud Detection
    - On Privacy (Or: How Not to Build a Surveillance State)
  - Viral Marketing & Growth Strategy
    - Wearable Marketing
      - QR Code T-Shirts
      - Other Wearable Items
    - Digital Marketing
      - Social Media Challenges
      - Meme Campaigns
      - Influencer Partnerships
    - Community Building
      - Local Meetups
      - University Campus Programs
      - Disease-Specific Forums
    - Cost Analysis & Optimization
      - Per-Tactic Cost Breakdown
      - ROI Optimization
  - Integration & Auditing Framework
    - Integrity and Auditing
      - Cryptographic Receipts
      - Public Audit System
      - Observer Program
    - Incentives and Referrals
      - Reward Structure
      - Education-First Approach
    - Legal Positioning
      - Consultation Framing
      - Data Protection Compliance
  - Implementation Roadmap
    - Phase 1: Foundation (Months 1-2)
    - Phase 2: Scaling (Months 3-6)
    - Phase 3: Global Launch (Months 7-12)
    - Phase 4: Optimization (Months 13+)
  - Success Metrics
  - On Putting It All Together
    - What You're Building
      - The Innovation Part
      - The Money Part
      - What Success Looks Like
    - On Why {{< var global_population_activism_threshold_pct >}} Is The Magic Number

#### knowledge/strategy/viral-marketing.qmd
**Title:** Viral Marketing Strategy
**Description:** How to Make Curing Disease More Viral Than Cat Videos
**Stats:** 1,196 words | 289 lines

  - The Message That Spreads
    - What Doesn't Go Viral
    - What Does Go Viral
  - The Viral Formula
    - Emotional Triggers
    - Personal Stake
    - Shareability
  - The Content Ladder
    - Level 1: The Hook (3 seconds)
    - Level 2: The Emotion (30 seconds)
    - Level 3: The Solution (3 minutes)
    - Level 4: The Action (immediate)
  - Platform-Specific Strategies
    - Twitter/X
    - TikTok/Reels
    - YouTube
    - Reddit
  - The Referral System
    - Individual Incentives
    - Influencer Incentives
    - Corporate Incentives
  - The Meme Arsenal
    - Economic Memes
    - Emotional Memes
    - Comparison Memes
  - The Influencer Strategy
    - Target Categories
    - The Pitch to Influencers
  - The Data That Spreads
    - Daily Updates
    - Personal Calculators
    - Comparison Tools
  - The Controversy Strategy
    - Hot Takes That Generate Engagement
    - Expected Pushback (and Responses)
  - The Metrics
    - Viral Success Indicators
    - Conversion Funnel
    - Target Ratios
  - The Timeline (Years 1-2 of the Roadmap)
    - Months 1-6: Foundation & Launch
    - Months 7-12: Acceleration
    - Months 13-18: Critical Mass
  - The Strategy

#### knowledge/strategy/co-opting-defense-contractors.qmd
**Title:** Making Friends with the Military-Industrial Complex
**Description:** Lobbyists are like pigeons. They go where the food is. This chapter teaches you how to move the food.
**Stats:** 1,421 words | 257 lines

  - The Solution
  - The Offer
  - The Math
  - Why They Take It
    - It's More Papers
    - The Treaty Doesn't Actually Hurt Them
    - Political Cover
  - How You Do This
    - Step 1: Identify Targets
    - Step 2: The Meeting
    - Step 3: The Flip
    - Step 4: Active Support
  - Budget
  - Why This Works
    - You're Using Their Own Playbook
    - It's Legal
    - It Might Work
  - What You're NOT Asking
  - The Irony
  - What They Tell Their Boards
  - Optimistic Timeline (If This Works)
  - Pessimistic Timeline (If This Doesn't Work)
  - Summary

#### knowledge/call-to-action/three-actions.qmd
**Title:** The Three Actions
**Description:** Vote, Invest, Share - That's It
**Stats:** 379 words | 50 lines

  - Action 1: VOTE (2 Minutes)
  - Action 2: INVEST (10 Minutes)
  - Action 3: RECRUIT (15 minutes)
  - That's It.

### Essential References

#### knowledge/appendix/recovery-trial.qmd
**Title:** The Oxford RECOVERY Trial
**Description:** Proof that decentralized pragmatic trials reduce costs by 82X while saving millions of lives
**Stats:** 1,440 words | 155 lines

  - Key RECOVERY Trial Statistics
    - They Used Regular Hospitals
      - They Collected Only Useful Data
      - They Integrated With Normal Care
      - They Were Flexible
      - They Prioritized Speed Over Bureaucracy
      - The Result
      - The Implications: What RECOVERY Proved
      - The Bottom Line Math
      - Sources and Key Quotes
  - Proof This Isn't Insane
    - Oxford Already Achieved {{< var recovery_trial_cost_reduction_factor >}}× Cost Reduction
    - The Oxford RECOVERY Trial
    - The Math

#### knowledge/appendix/real-world-evidence-historical-success.qmd
**Title:** Real-World Evidence Historical Success (Pre-1962)
**Description:** How decentralized physician trials from 1883-1962 achieved 4 years/decade life expectancy gains, and what happened when the 1962 regulations replaced them with industry-controlled trials
**Stats:** 1,419 words | 219 lines

  - Historical Evidence: Why Real-World Evidence Works Better
    - 10,000 Years of Dying at 30
    - 1883 – The Year You Figured It Out
    - The Result
    - 1938 – The FDA Requires Phase 1 Safety Trials
    - 1950s – Thalidomide: When Safety Regulations Actually Worked
    - 1962 – The Year You Decided to Make Everything Worse
      - What Changed
      - What Happened to Efficacy Data
      - What Happened to New Treatments
      - What Happened to Costs
      - What Happened to Drug Patents
      - Decreased Ability to Determine Comparative Efficacy
    - What Happened to Life Expectancy (The Part That Matters)
    - The "Diminishing Returns" Excuse
    - The "Correlation Is Not Causation" Excuse
    - Impact of Innovative Medicines on Life Expectancy
  - The Summary

### Implementation Strategy

#### knowledge/appendix/treaty-feasibility.qmd
**Title:** Treaty Feasibility & Cost Analysis
**Description:** Real-world evidence that getting a global treaty signed costs $90M, not billions
**Stats:** 1,985 words | 213 lines

  - What Treaties Actually Cost
    - Inflation-Adjusted to 2024 Dollars
  - Cost for a 1% Health Treaty
    - The Math
  - How to Make Governments Sign Things
    - Timeline to "Governments Can't Ignore This"
  - Conclusion
  - Political Success Probability: Economic Analysis {#sec-political-success-probability}
    - Historical Precedents for International Financial Commitments
    - Why a 1% Treaty is Harder Than Most Precedents
    - Why a 1% Treaty Might Beat the Odds
    - Probability Estimates
    - Expected Value Implications
  - Why The Treaty Won't Stop at 1%
    - The Expansion Mechanism
    - Why This Differs from Stagnant Treaties
    - The Ratchet Effect
    - Long-Term Feasibility
  - Sources

#### knowledge/appendix/nonprofit-partnership-incentives.qmd
**Title:** How to Turn Grant Applicants Into Billionaires
**Description:** On making nonprofits rich by aligning their incentives with not dying
**Stats:** 931 words | 157 lines

  - The Solution
  - On The Two-Part (Legal) Bribe
    - Part 1: Make The Organization Rich (Performance-Based Grants)
      - The Old Way
      - The New Way
      - The Offer
      - What This Does
    - Part 2: Make The Leaders Personally Rich (VOTE Points)
      - The Problem Grants Don't Solve
      - The Solution
      - The Offer
      - What This Does
  - On The Real Prize (Or: How to Stop Begging Forever)
    - The Transformation
      - How It Works
        - Who Controls These Billions?
      - The Choice
  - Earning a Stake: Tracking Contributions for Treasury Allocation
  - Conclusion: From Partners to Owners

### Policy & Regulatory

#### knowledge/appendix/right-to-trial-fda-upgrade-act.qmd
**Title:** Right to Trial & FDA Upgrade Act
**Description:** Act to modernize medical research and treatment access through an open-source FDA.gov v2, giving patients the right to participate in trials.
**Stats:** 6,849 words | 289 lines

  - TITLE I: SHORT TITLE; PURPOSE; FINDINGS; DEFINITIONS
    - SEC. 101. SHORT TITLE
    - SEC. 102. PURPOSE
    - SEC. 103. FINDINGS
    - SEC. 104. DEFINITIONS
  - TITLE II: FDA Upgrade AND CLINICAL‑TRIAL INNOVATION
    - SEC. 201. ACCELERATED ADOPTION OF ALTERNATIVE PRECLINICAL TEST METHODS
    - SEC. 202. GUIDANCE ON DECENTRALISED, ADAPTIVE, AND REAL‑WORLD‑EVIDENCE TRIALS
    - SEC. 203. PATIENT‑FOCUSED DRUG DEVELOPMENT AND GLOBAL COLLABORATION
    - SEC. 204. FDA.gov v2 DECENTRALIZED HEALTH PROTOCOL AND REFERENCE IMPLEMENTATION
    - SEC. 205. FDA-X PRIZE
  - TITLE III: UNIVERSAL TRIAL ACCESS (RIGHT‑TO‑TRIAL PROGRAM)
    - SEC. 301. UNIVERSAL ELIGIBILITY FOR INVESTIGATIONAL INTERVENTIONS
    - SEC. 302. PATIENT PROTECTIONS, CONSENT, AND LIABILITY
    - SEC. 303. FAIR ACCESS AND DISCOUNT ALGORITHMS
    - SEC. 304. PATIENT COST CONTRIBUTION FOR TRIAL PARTICIPATION
  - TITLE IV: GENERAL PROVISIONS
    - SEC. 401. COORDINATION WITH EXISTING LAW
    - SEC. 402. AUTHORIZATION OF APPROPRIATIONS AND STAGE‑GATED FUNDING
    - SEC. 403. IMPLEMENTATION TIMELINE
    - SEC. 404. STRATEGY FOR GLOBAL GOVERNANCE AND DECENTRALIZATION
    - SEC. 405. SEVERABILITY
    - SEC. 406. TRANSPARENCY IN REGULATORY ACTIONS LIMITING TREATMENT ACCESS
    - REFERENCES
      - End of Act.

#### knowledge/appendix/impact-securities-reform.qmd
**Title:** Impact Securities Reform Act
**Description:** Draft Legislation for Digital Public Goods Financing - Model law to enable high‑impact public‑good financing via impact securities, expanded investor access, and on‑chain reporting safe harbors.
**Stats:** 728 words | 95 lines

  - Section 2. Definitions
  - Section 3. Impact Securities Safe Harbor (Offering and Distribution)
  - Section 4. On‑Chain Disclosure and Reporting (Automation)
  - Section 4A. Marketing & Disclosures Safe Harbor (Plain-English, Outcome-Linked)
  - Section 5. Token Classification Safe Harbor (Governance and Utility)
  - Section 6. Outcome‑Linked Incentives (Impact‑Based Value Capture)
  - Section 9. Implementation
  - Section 10. Enforcement and Remedies
  - Commentary: Relation to dFDA/DIH and VICTORY Incentive Alignment Bonds

#### knowledge/appendix/incentive-alignment-bonds-paper.qmd
**Title:** Incentive Alignment Bonds: Making Public Goods Financially and Politically Profitable
**Description:** Government spending is optimized for lobbying intensity, not net societal value. Programs with 100:1 benefit-cost ratios get billions while programs with negative returns get hundreds of billions. Inc...
**Stats:** 16,422 words | 1,485 lines

  - Introduction
    - The Information-Incentive Disconnect
    - Key Results
    - Reader's Guide
    - Definition
    - Why Reallocation, Not Addition
    - Political Change as an Asset Class
    - The Capital Asymmetry: Why IABs Can Outcompete Incumbent Lobbying
    - Quantifying Net Societal Value of Funding Sources
    - Relation to Existing Literature
    - Contribution
    - Roadmap
  - Why Previous Approaches Failed {#sec-literature}
    - Mechanism Design Theory
    - Public Choice Theory
    - Social Impact Bonds
    - Campaign Finance and Political Behavior
    - Credit Rating Agencies as Governance Mechanisms
  - The Math: Proving It Works {#sec-formal-model}
    - Assumptions
    - The Politician's Utility Function
    - The Utility Function Transformation
    - Numerical Calibration and Parameter Ranges
    - The Policy Choice
    - The Pre-IAB Equilibrium
    - The IAB Mechanism
    - Score-Dependent Payoffs
    - Incentive Compatibility
    - Nash Equilibrium Analysis
    - Illustrative Example: A Global Health Treaty
    - Calibration: Parameter Ranges for Incentive Compatibility
  - How IABs Work in Practice {#sec-architecture}
    - Layer A: Scoring (Data Provision)
    - Layer B: Electoral Support
    - Layer C: Post-Office Benefits
    - Why This Is Not Bribery
      - Statutory Analysis: 18 U.S.C. § 201
      - Constitutional Protections
      - Established Precedent: Decades of Legal Scorecard Operations
      - The Key Legal Distinction
    - Legal Entity Separation
    - Funding Sources and Foundation Investment
  - What Could Go Wrong {#sec-failure-modes}
    - Gaming and Metric Corruption
    - Plutocracy Objection and the "Lobbying With Extra Steps" Critique
    - Unintended Consequences
  - Where IABs Fit in Democratic Reform {#sec-governance}
    - The Four-Layer Governance Stack
    - Comparison to Alternative Governance Mechanisms
    - What IABs Do Not Solve
  - Beyond Health: Climate, Nuclear Risk, and More {#sec-generalization}
    - The General Template
    - Candidate Domains
    - Welfare Accounting of the IAB Mechanism
      - Sensitivity Analysis of Mechanism BCR
  - Conclusion
    - The Bootstrap Problem and Regulatory Resistance
  - References {.unnumbered}
  - Appendix A: Formal Proofs {.unnumbered}
    - Proof of Proposition 1 (Sufficient Condition for Incentive Compatibility)
    - Proof of Corollary 1 (Funding Threshold)
    - Proof of Proposition 2 (Multiple Equilibria Without IABs)
    - Proof of Proposition 3 (Equilibrium Selection With IABs)
  - Appendix B: Detailed Application Specifications {.unnumbered}
    - B.1 Climate Change
    - B.2 Nuclear Disarmament
    - B.3 Pandemic Preparedness
    - B.4 Comparative Analysis

#### knowledge/appendix/cost-of-change-analysis.qmd
**Title:** The Price of Political Change: A Cost-Benefit Framework for Policy Incentivization
**Description:** When critics dismiss policy proposals as "politically impossible," they implicitly claim the cost of achieving political change exceeds its benefits. This paper develops a framework for quantifying po...
**Stats:** 3,531 words | 465 lines

  - Introduction
    - The Political Impossibility Objection
    - Political Change as an Investment
    - Contribution and Roadmap
  - Literature Review
    - Public Choice and Rent-Seeking
    - Lobbying Returns and Effectiveness
    - Campaign Finance and Electoral Outcomes
    - Post-Office Career Incentives
    - Social Impact Bonds and Outcomes-Based Policy
  - Theoretical Framework
    - The Political Cost Function
    - Campaign Finance Component
    - Lobbying Component
    - Career Value Component
    - The Benefit Function
    - Breakeven Condition
  - Empirical Methodology
    - US Political System Cost Estimates
      - Campaign Finance
      - Lobbying
      - Post-Office Career Value
      - US Maximum Reform Investment Scenarios {#us-political-reform-scenarios}
    - Global Estimates {#global-estimates}
  - Case Studies
    - Case Study 1: Military-to-Health Spending Reallocation (1% Treaty)
    - Case Study 2: Carbon Pricing
    - Case Study 3: Agricultural Subsidy Reform
    - Case Study 4: Occupational Licensing Reform
    - Summary of Case Studies
  - Limitations and Counterarguments
    - Uncertainty in Cost Estimates
    - Legal and Ethical Constraints
    - Counter-Spending and Escalation
    - Political Backlash
    - Moral Objections
  - Implementation Considerations
    - The Coordination Problem
    - Assurance Contracts
    - Credible Commitment Mechanisms
    - The Wrapper Architecture
    - Governance of the Reform Coalition
  - Conclusion
  - References

#### knowledge/appendix/wishocracy-paper.qmd
**Title:** Wishocracy: Solving the Democratic Principal-Agent Problem Through Pairwise Preference Aggregation
**Description:** Representative democracy suffers from an inescapable principal-agent problem where elected officials' incentives diverge from citizen welfare. Wishocracy introduces RAPPA (Randomized Aggregated Pairwi...
**Stats:** 10,548 words | 785 lines

- **Abstract**
- **Introduction: The Preference Aggregation Problem**
- **Theoretical Foundations**
  - **The Analytic Hierarchy Process**
  - **The Preference Intensity Problem**
  - **Collective Intelligence and the Wisdom of Crowds**
  - **Related Work and Positioning in the Literature**
- **Mechanism Design: Randomized Aggregated Pairwise Preference Allocation**
  - **Core Mechanism**
    - Scenario: Federal Budget Preferences
  - **Formal Properties**
  - **Formal Model**
  - **Computational Complexity and Scalability**
  - **Comparative Information & Welfare Analysis**
    - **Information-Theoretic Superiority**
    - **Welfare Maximization: The "Median vs. Mean" Proof**
    - **Principal-Agent Cost Elimination**
- **Empirical Precedents and Evidence Base**
  - **Porto Alegre Participatory Budgeting**
  - **Taiwan's Digital Democracy Experiments**
  - **Stanford Participatory Budgeting Platform Research**
  - **Reference Implementation: Wishocracy.org**
    - **Category Selection and Validation Methodology**
    - **Zero-Funding Filter Optimization**
    - **Hierarchical Category Structure**
    - **Framing Bias and Mitigation**
- **Addressing Potential Criticisms**
  - **Participation and Digital Divide**
  - **Manipulation and Sybil Attacks**
  - **Preference Laundering and Manufactured Consent**
  - **Complexity of Real Policy Trade-offs**
  - **Legitimacy and Accountability**
  - **Failure Modes and Robustness**
- **Implementation Pathway: From Information to Incentive Alignment**
  - **Why Information Alone Fails: Politicians Respond to Incentives**
  - **Three-Phase Implementation**
    - **Phase 1: Informational (Preference Gap Documentation)**
    - **Phase 2: Accountability Scoring (Politician Alignment Ratings)**
    - **Phase 3: Incentive Alignment (Integration with Incentive Alignment Bonds)**
  - **Why Federal-Scale Priorities**
  - **Evaluation Framework**
    - **Preference Aggregation Quality**
    - **Accountability System Effectiveness**
    - **Incentive Alignment Impact**
  - **Connection to Incentive Alignment Bonds**
  - **Connection to Optimocracy**
- **Conclusion**
- **Appendix A: The Service Provider Layer**
  - References {.unnumbered}

#### knowledge/appendix/optimocracy-paper.qmd
**Title:** Optimocracy: Evidence-Based Governance Through Outcome-Bound Optimization
**Description:** Political dysfunction (cronyism, short-termism, and misalignment between political incentives and citizen outcomes) costs society an estimated 20% of potential GDP (the "Political Dysfunction Tax"). O...
**Stats:** 12,861 words | 1,280 lines

  - Abstract
  - Introduction: The Political Dysfunction Problem
    - Why Information Alone Fails
    - The Political Dysfunction Tax
    - The Optimocracy Thesis
    - How It Works in Practice
    - Contributions
  - The Scale of Welfare Loss: Empirical Foundations
    - A Formal Model of the Political Dysfunction Tax
    - Documented Welfare Losses by Policy Domain
    - Alternative Estimation: Bottom-Up Policy Cost Accounting
    - Why Information Doesn't Solve the Problem
    - Implications for Mechanism Design
    - When Does Optimocracy Beat the Status Quo?
      - Formal Model
  - Theoretical Foundations
    - Lessons from Technocratic Governance Failures
      - Soviet Central Planning
      - Failed Algorithmic Governance in Finance
      - Synthesis: Boundary Conditions for Algorithmic Governance
    - Why No Perfect System Exists (And Why That's Fine)
      - Arrow and Gibbard-Satterthwaite: Metric Selection Is Political
      - Mechanism Design: Honest Answers Require Honest Incentives
      - The Comparison That Matters
    - Index Funds and Passive Allocation
    - Credible Commitment Mechanisms
  - Mechanism Design
    - Architecture Overview
    - The Constitutional Layer
    - The Verification Layer
    - The Execution Layer
  - Welfare Metrics
    - Default Implementation: Two-Metric Welfare Function {#sec-two-metric-welfare}
    - Metric Defaults
  - Scope and Limits: A Taxonomy of Governance Decisions
    - Engaging with the Counter-Literature
    - A Taxonomy of Governance Decisions
    - Defining Optimocracy's Proper Scope
  - Advantages Over Political Governance
    - Capture Resistance
    - Time Consistency
    - Transparency and Verifiability
    - Reduced Coordination Costs
    - Depolarization Through Outcome Focus
  - Challenges and Failure Modes
    - Why Goodhart's Law Doesn't Apply Here
    - Oracle Capture
    - Democratic Legitimacy
  - Testable Predictions
    - Rejection Criteria
  - The Wrapper Architecture: Integration with IABs
  - Political Economy: Making Reform Happen
    - The Coase Theorem Applied to Governance Reform
    - A Taxonomy of Affected Parties
    - IABs as the Coasean Buyout Mechanism
    - The Cost of Political Reform: Quantifying "Political Impossibility"
    - The Natural Reform Coalition
  - Implementation Pathway
    - Implementation Phases
    - Realistic Adoption Path
    - Concrete First Deployment: The GiveWell Outcome Fund
    - Why Government Adoption Isn't Required
  - Conclusion
    - What About AI?
  - Appendix A: Technical Specification Sketch
    - Verification System Specification
    - Budget and Policy Optimization: Two Complementary Frameworks
      - Budget Optimization: The Optimal Budget Generator (OBG) Framework
      - Policy Optimization: The Policy Impact Score (PIS) Framework
      - How They Work Together
    - Algorithmic Governance Threat Model
      - Known Failure Modes
      - Why "Immutable Rules" Are Insufficient
      - Realistic Security Properties
      - Defense-in-Depth Architecture
  - Acknowledgments {.unnumbered}
  - References

#### knowledge/appendix/optimal-policy-generator-spec.qmd
**Title:** Optimal Policy Generator: Evidence-Based Policy Recommendations for Jurisdictions
**Description:** The Optimal Policy Generator (OPG) produces systematic policy recommendations for jurisdictions at any level (country, state, city), generating prioritized enact/replace/repeal/maintain recommendation...
**Stats:** 13,335 words | 1,964 lines

  - Abstract {.unnumbered}
  - The Two Welfare Metrics {#sec-two-metrics}
    - Why Only Two Metrics?
    - Income Metric Definition {#sec-income-definition}
    - Outcome Translation Methodology {#sec-outcome-translation}
  - The Evidence Base: Centuries of Natural Policy Experiments {#sec-evidence-base}
    - Scale of Available Natural Experiments
    - The OPG Pipeline
    - Why This Hasn't Been Done Before
  - System Overview {#sec-opg-system-overview}
    - What Policymakers See
    - What Policy Analysts See
  - Introduction
    - Why Generic Policy Scores Are Not Enough
    - Why Policy Ranking Fails Today
    - Scale of Available Evidence
    - Contributions
    - Validation Status
  - Related Work
    - Existing Policy Evaluation Frameworks
    - This Framework's Contribution
  - Theoretical Framework
    - The Policy Optimization Problem
    - Evidence Aggregation Properties
    - Information Value
  - Core Methodology
    - Policy-Outcome Data Structure
      - Core Tables
      - Policy Types
    - Analysis Methods {#sec-analysis-methods}
      - Synthetic Control Method
      - Difference-in-Differences (DiD)
      - Regression Discontinuity Design (RDD)
      - Event Study / Interrupted Time Series
      - Confidence Weighting by Method
    - Bradford Hill Criteria Scoring Functions {#sec-bradford-hill}
      - Strength of Association
      - Consistency Across Jurisdictions
      - Temporality (Required)
      - Dose-Response Gradient
      - Experiment Quality
      - Plausibility (Mechanistic)
      - Coherence with Literature
      - Analogy to Similar Policies
      - Specificity
    - Causal Confidence Score (CCS) Calculation
  - Jurisdiction Policy Inventory
    - Tracking Current Policies by Jurisdiction
    - Data Sources for Policy Status
    - Handling Missing Data
  - Policy Gap Analysis {#sec-policy-gap}
    - Comparing Current to Optimal
    - Gap Types
    - Priority Scoring
    - Context Adjustment {#sec-context-adjustment}
  - Recommendation Generation {#sec-recommendation-generation}
    - Recommendation Types
    - Blocking Factors {#sec-blocking-factors}
    - Similar Jurisdictions {#sec-similar-jurisdictions}
      - Computing Jurisdiction Similarity
    - Recommended Tracking (for OPG Feedback)
  - Optimal Jurisdictional Level for Policy Implementation
    - The Subsidiarity Principle for Evidence Generation
    - When Higher Levels Are Necessary
    - Jurisdictional Level in Recommendations
  - Policy Impact Score (Intermediate Metric) {#sec-pis}
    - Overview
    - Jurisdiction-Level PIS Calculation
    - Always Report Both Metrics Separately
    - Effect Estimate Standardization
    - Quality Adjustment Factor
    - Confounder Adjustment
  - Global (Aggregate) PIS Calculation {#sec-global-pis}
    - Pooled Effect Estimate
    - Pooled PIS Across Jurisdictions
    - Heterogeneity Statistics
    - Evidence Grading {#sec-evidence-grading}
    - Context-Specific Confidence
  - Quality Requirements & Validation
    - Minimum Thresholds for Inclusion
    - Parallel Trends Testing (DiD)
    - Pre-Treatment Fit (Synthetic Control)
    - Placebo and Robustness Tests
  - Interpreting Recommendations
    - Priority Tiers
    - Political Feasibility Notes
    - Sequencing Guidance
  - Effect Size Benchmarks {#sec-effect-benchmarks}
  - Trial Prioritization {#sec-trial-prioritization}
    - Value of Information Calculation
    - Natural Experiment Identification
    - Recommended Pilot Jurisdictions
  - Data Sources
    - Primary Policy Databases
    - Primary Outcome Databases
    - Subnational Data
    - Jurisdiction Policy Inventory Sources
  - Limitations
    - Oracle Capture Risk
    - Confounding Severity
    - Heterogeneous Effects
    - Jurisdiction-Specific Caveats
    - Time-Varying Effects
    - Publication Bias
    - Epistemic Limitations
  - Validation Framework {#sec-validation-framework}
    - The Critical Question
    - Addressing Adoption Bias
    - Proposed Validation Study
    - Prospective Pre-Registration
    - Known Limitations Requiring Validation
    - Continuous Improvement via Adoption Feedback
  - Future Directions
    - Methodological Improvements
    - Validation Priorities
    - Data Infrastructure
    - Integration with Decision-Making
  - Conclusion
  - Acknowledgments {.unnumbered}
  - References
  - Appendix A: Worked Example - Texas Policy Recommendations {.appendix}
    - ⚠️ SYNTHETIC DATA - NOT EMPIRICAL FINDINGS
    - Overview
    - Texas Policy Inventory (Sample)
    - Step 1: Calculate Policy Impact Scores
    - Step 2: Apply Context Adjustment for Texas
    - Step 3: Generate Recommendations
  - ENACT (New Policies to Adopt)
  - REPLACE (Policies to Modify)
    - Tradeoff Demonstration
  - REPEAL (Policies to Remove)
  - MAINTAIN (No Change Needed)
    - Step 4: Summary Dashboard
    - Interpretation
  - Appendix B: OPG Analysis Workflow {.appendix}
    - Complete OPG Pipeline
    - Minimum Data Requirements Checklist
  - Appendix C: Glossary {.appendix}

#### knowledge/appendix/optimal-budget-generator-spec.qmd
**Title:** Optimal Budget Generator: Evidence-Based Budget Allocation Framework
**Description:** The Optimal Budget Generator (OBG) answers: 'How should we allocate the budget to maximize welfare?' Unlike isolated spending targets, OBG generates integrated budget recommendations that account for ...
**Stats:** 8,967 words | 1,355 lines

  - Abstract {.unnumbered}
  - System Overview {#obg-system-overview}
    - What Policymakers See
  - Example: US Federal Budget Gap Analysis
    - What Budget Analysts See
    - Where This Fits
  - Introduction
    - Why Budget Allocation Fails Today
    - The RDA Analogy: Optimal Levels, Not Just Marginal Returns
    - What This Framework Provides
  - Related Work
    - Budget Analysis Frameworks
    - Evidence-Based Policy Movement
    - Comparative Public Finance
    - How OBG Differs
  - Theoretical Framework
    - The Social Planner's Problem
    - Optimal Spending Levels Under Uncertainty
    - Budget Impact Score as Precision Weighting
    - Gap Analysis and Welfare Gains
    - Welfare Bounds Under Model Uncertainty
    - Summary of Theoretical Results
  - Core Methodology
    - Spending Category Data Structure
    - Three Methods for OBG Estimation
  - Reference Country Benchmarking
    - The Basic Approach
    - Reference Country Selection Criteria
    - Worked Example: Early Childhood Education
    - Limitations of Reference Benchmarking
  - Diminishing Returns Modeling
    - The Core Concept
    - Finding the "Knee" of the Curve
    - Estimation Methods
    - Worked Example: K-12 Education Spending
  - Worked Example: Pragmatic Clinical Trials
    - The Highest-Return Public Investment
    - Reference Country Benchmarking
    - Diminishing Returns Analysis
    - Cost-Effectiveness Calculation
    - Gap Analysis
    - Why This Category Dominates
  - Cost-Effectiveness Threshold Analysis
    - The Standard Health Economics Approach
    - Building Up from Intervention-Level Data
    - Worked Example: Vaccinations
  - Budget Impact Score (BIS) as Evidence Quality
    - Reframing BIS: Confidence in OSL, Not Allocation Driver
    - BIS Calculation
    - Evidence Grading from BIS
    - BIS Does Not Drive Allocation
  - Gap Analysis and Priority Ranking
    - Computing Gaps
    - Priority Score
    - Worked Example: Priority Ranking
  - Multi-Unit Reporting
    - The Problem with Abstract Scores
    - Reporting at Multiple Levels
    - Conversion Factors
    - Worked Example: Multi-Unit Output
  - Quality Requirements and Validation
    - Minimum Thresholds for OBG Estimation
    - Robustness Checks
  - Interpreting Results
    - Gap Ranges and Recommended Actions
    - What the Algorithm Cannot Tell You
  - Pilot Program Prioritization
    - Value of Information for Uncertain Categories
    - Recommended Pilot Designs
    - Learning Feedback Loop
  - Data Sources
    - Reference Country Databases
    - Cost-Effectiveness Databases
    - US Budget Data
  - Limitations
    - Reference Country Selection Bias
    - Diminishing Returns Uncertainty
    - Political Feasibility Not Modeled
    - Implementation Capacity
  - Validation Framework
    - Retrospective Validation
    - Prospective Validation
    - Success Metrics
    - Validation Status
  - Sensitivity Analysis
    - Parameter Sensitivity
    - Scenario Analysis
  - Future Directions
    - Methodological
    - Data Infrastructure
    - Governance Integration
  - Conclusion
  - Acknowledgments {.unnumbered}
  - References
  - Appendix A: Worked Example - Complete OBG Calculation {.appendix}
    - Example: US Military Discretionary Spending
  - Appendix B: Analysis Workflow {.appendix}
    - Complete OBG Analysis Pipeline
  - Appendix C: Glossary {.appendix}
    - Core Concepts
    - Estimation Methods
    - Evidence Quality
    - Output Concepts
  - Appendix D: Comparison to Actual US Budget {.appendix}
    - Current US Discretionary Budget vs. OSL Targets

#### knowledge/appendix/dfda-spec-paper.qmd
**Title:** dFDA: A Decentralized Framework for Drug Assessment Using Two-Stage Real-World Evidence Validation
**Description:** We present the Predictor Impact Score (PIS), a novel composite metric operationalizing Bradford Hill causality criteria for automated signal detection from aggregated N-of-1 observational studies. Com...
**Stats:** 13,613 words | 1,907 lines

  - Abstract
  - System Overview: From Methodology to Implementation {#system-overview}
    - What Patients See
    - What Companies See
    - Where This Methodology Fits
  - Introduction
    - The Human Cost of the Current System
    - The Pharmacovigilance Gap
    - The Real-World Data Opportunity
    - Our Contribution
  - Data Collection and Integration
    - Data Sources
    - Variable Ontology
    - Measurement Structure
    - Unit Standardization
  - Mathematical Framework
    - Data Structure
    - Temporal Alignment
      - Onset Delay and Duration of Action
      - Outcome Window Calculation
    - Pair Generation Strategies
      - Outcome-Based Pairing (Predictor has Filling Value)
      - Predictor-Based Pairing (No Filling Value)
    - Filling Value Logic
      - Filling Types
      - Temporal Boundaries
      - Conservative Bias
    - Baseline Definition and Outcome Estimation
      - Within-Subject Comparison
      - Outcome Means
    - Percent Change from Baseline
    - Correlation Coefficients
      - Pearson Correlation (Linear Relationships)
      - Spearman Rank Correlation (Monotonic Relationships)
      - Forward and Reverse Correlations
    - Z-Score Normalization
    - Statistical Significance
    - Hyperparameter Optimization
  - Population Aggregation
    - Individual to Population
    - Standard Error and Confidence Intervals
    - Heterogeneity Assessment
  - Data Quality Requirements
    - Minimum Thresholds
    - Variance Validation
    - Outcome Value Spread
  - Predictor Impact Score
    - What Makes the Predictor Impact Score Novel
    - User-Level Predictor Impact Score
    - Aggregate (Population-Level) Predictor Impact Score
    - Z-Score and Effect Magnitude Factor
    - Temporality Factor
    - Percent Change from Baseline
    - Statistical Significance
    - Interest Factor
    - Additional Data Quality Components
    - Bradford Hill Criteria Mapping {#bradford-hill-mapping}
    - Interpreting Predictor Impact Scores
  - Provisional Thresholds - Not Yet Validated
    - Optimal Daily Value for Precision Dosing
      - Value Predicting High Outcome
      - Value Predicting Low Outcome
      - Grouped Optimal Values
      - Precision Dosing Recommendations
      - Mathematical Relationship to Biological Gradient
      - Clinical Applications
      - Limitations
      - Confidence Intervals for Optimal Values
      - Individual vs Population Optimal Values
      - Temporal Stability and Recalculation
      - Edge Cases: Minimal Dose-Response
      - Validation of Optimal Values
    - Saturation Constant Rationale
    - Effect Following High vs Low Predictor Values
      - Average Outcome Metrics
      - Calculation
    - Predictor Baseline and Treatment Averages
    - Relationship Quality Filters
      - Filter Flags
      - Boring Relationship Definition
      - Usefulness and Causality Voting
    - Variable Valence
      - Impact on Interpretation
    - Temporal Parameter Optimization
      - Stored Optimization Data
      - Optimization Grid
      - Overfitting Protection
    - Spearman Rank Correlation
  - Outcome Label Generation
    - Predictor Analysis Reports
    - Report Structure
    - Category-Specific Analysis
    - Verification Status
    - Outcome Labels vs. FDA Drug Labels
    - Worked Example: Complete Outcome Label
  - Treatment Ranking System
    - Within-Category Rankings
    - Ranking Algorithm
    - Confidence Weighting
    - Comparative Effectiveness Display
  - Safety and Efficacy Quantification
    - Safety Signal Detection
    - Efficacy Signal Detection
    - Benefit-Risk Assessment
  - Addressing the Bradford Hill Criteria {#addressing-bradford-hill}
    - Complete Criteria Mapping
    - Quantitative Criteria Details
  - Validation and Quality Assurance
    - User Voting System
    - Automated Quality Checks
    - Flagged Study Handling
  - Stage 2: Pragmatic Trial Confirmation
    - The Two-Stage Pipeline
    - Pragmatic Trial Methodology
    - Signal-to-Trial Prioritization
    - Comparative Effectiveness Randomization
    - Feedback Loop: Trial Results Improve Observational Models
    - Output: Validated Outcome Labels
  - Limitations and How They're Addressed
    - Fundamental Limitations: Observational Stage
    - Methodological Weaknesses: Addressed by Two-Stage Design
    - Residual Limitations
    - What This Framework CAN Now Do
  - Implementation Guide
    - System Architecture
    - Core Algorithm: Pair Generation
    - Core Algorithm: Baseline Separation
    - Algorithm 3: Predictor Impact Score Calculation
    - Reference Implementation
  - Regulatory Considerations
    - Positioning Relative to RCTs
    - Evidence Hierarchy Integration
    - FDA Real-World Evidence Framework Alignment
  - Validation Framework {#sec-validation-framework}
    - The Critical Question
    - Proposed Validation Study
    - Known Limitations Requiring Validation
  - Future Directions
    - Methodological Improvements
    - Validation Priorities
    - Implementation Enhancements
  - Conclusion
  - Appendix A: Effect Size Classification
  - Appendix B: Variable Category Defaults
  - Appendix C: Glossary
  - Appendix D: Worked Example
    - Example: Calculating Predictor Impact Score for "Magnesium → Sleep Quality"
  - Appendix E: Analysis Workflow

### Economic Analysis

#### knowledge/economics/peace-dividend.qmd
**Title:** Peace Dividend
**Description:** What happens when you build 1% fewer things that explode
**Stats:** 1,323 words | 219 lines

  - How 1% Less Violence Pays For Everything
    - The Captured Money: {{< var treaty_annual_funding >}}/Year
    - The Bonus Savings: {{< var peace_dividend_annual_societal_benefit >}}/Year
    - Where the {{< var peace_dividend_annual_societal_benefit >}} Comes From
  - The Formulas
  - Military vs Disease Research: The Opportunity
  - Peace Dividend Breakdown by Category
  - Peace Dividend Composition
  - Captured vs. Societal Dividend
  - Sensitivity Analysis
    - Tornado Chart: Key Drivers of Uncertainty
    - Monte Carlo Distribution
    - Probability of Exceeding Thresholds
    - Conflict Elasticity Parameter
  - Key Findings
  - Assumptions and Limitations
    - GDP Multiplier Note
    - Causal Elasticity Assumption
    - Source Quality
    - What This Does NOT Claim
    - Conservative Interpretation

#### knowledge/economics/health-dividend.qmd
**Title:** Health Dividend
**Description:** How a {{< var dfda_annual_opex >}} framework generates {{< var dfda_benefit_rd_only_annual >}} in annual savings through 80x cost reduction
**Stats:** 961 words | 132 lines

  - The Math: From {{< var traditional_phase3_cost_per_patient >}} to {{< var recovery_trial_cost_per_patient >}} Per Patient
  - Where the {{< var dfda_benefit_rd_only_annual >}} Comes From
  - What {{< var dfda_benefit_rd_only_annual >}} Buys You
  - Daily Opportunity Cost
  - The framework Cost Breakdown
  - ROI Scenarios
  - Why This Isn't Happening Already
  - The ROI
  - Further Reading
    - Detailed Analysis
  - Impact of Innovative Medicines on Life Expectancy
      - Key Sources

#### knowledge/appendix/humanity-budget-overview.qmd
**Title:** Humanity's Budget
**Description:** The True Scale of War & Disease
**Stats:** 483 words | 83 lines

  - On The Fundamental Trade-Off (Missiles vs. Medicine)
  - On What Our Species Actually Prioritizes
    - The Part That Shouldn't Be Possible
  - On The Most Absurd Disparity in Human History
  - On Why This Is Insane
    - The Math
      - Translation

#### knowledge/appendix/global-government-medical-research-spending.qmd
**Title:** Medical Research Spending: The {{< var global_med_research_spending >}} Lie
**Description:** A comprehensive breakdown of how little humanity invests in not dying, distinguishing broad "research" from actual cures.
**Stats:** 771 words | 116 lines

  - The Broad Number vs. The Real Number
    - The Accounting Trick
    - The Real Number: {{< var global_government_clinical_trials_spending_annual >}}
  - The 604x Disparity
  - The Industry Trap
  - Broad R&D Breakdown: The Hall of Shame
    - United States: The Alleged Leader
    - China: The Rising Power
    - European Union
    - The Rest of the World
  - Conclusion: A Species-Wide Failure

#### knowledge/appendix/global-clinical-trial-spending-by-phase.qmd
**Title:** Global Clinical Trial Spending by Phase
**Description:** A comprehensive breakdown of how much governments, companies, and nonprofits spend on Phase 1, 2, 3, and 4 clinical trials globally each year.
**Stats:** 2,397 words | 469 lines

  - The Bottom Line: {{< var global_clinical_trials_spending_annual >}} Annually (2024)
    - Growth trajectory
  - How Many People Participate? The Missing Data
    - What we know
      - Regional snapshots
  - Spending by Clinical Trial Phase
    - Phase 3: The Money Pit
      - Cost per trial
      - Cost per patient
      - As percentage of total drug development
    - Phase 2: The Middle Child
      - Cost per trial
      - Cost per patient
      - As percentage of total drug development
      - Trial characteristics
    - Phase 1: The Safety Gauntlet
      - Cost per trial
      - Cost per patient
      - As percentage of total drug development
      - Trial characteristics
    - Phase 4: The Forgotten Phase
      - Key facts
      - Why it matters
  - Who's Paying: Funding Source Breakdown
    - Private Industry: The Heavy Hitter
      - Global pharmaceutical R&D
      - Top spenders (2024 R&D budgets)
      - Regional breakdown
    - Government: The Seed Investor
      - United States (NIH)
      - NIH trial distribution
      - European Union
      - China
      - Other major government funders
    - Nonprofit Foundations: The Niche Players
      - Major players (2024)
      - Gates Foundation
      - Wellcome Trust
      - Other major nonprofit funders
      - Special initiatives
  - The Brutal Economics: Cost Per Approved Drug
    - Breakdown by phase (industry average)
      - Success rates (the depressing math)
  - Regional Market Distribution
    - North America: The Dominant Player
      - United States
    - Asia-Pacific: The Rising Giant
      - China
      - Why China is winning
      - Other Asia-Pacific
    - Europe: The Steady Player
      - Market share: ~25-30% of global market
  - What This Actually Means
    - The Good News
      - The Bad News
      - The Context
  - The Efficiency Paradox
    - Current system
      - The waste
  - Summary Table
  - The Path Forward

#### knowledge/appendix/clinical-trial-participants.qmd
**Title:** The 0.06% Problem - Who Actually Gets to Try New Treatments
**Description:** Humans spend {{< var global_clinical_trials_spending_annual >}} a year on clinical trials. About 5 million people participate globally. That's 0.06% of humanity.
**Stats:** 1,502 words | 227 lines

  - Enrollment Data from ClinicalTrials.gov
    - US Trials (Cumulative)
  - The Better Method: Count Completed Trials
  - Industry Standard: IQVIA 2022
  - The Tragedy in Numbers
    - Among those who could benefit and are willing to help:
  - The Access Lottery
  - The Willingness Gap
  - The Cost Per Patient
  - Why This Matters
  - Enrollment Data by Phase
  - What a 1% Treaty Could Do
    - Today's Capacity
      - With 1% of Military Spending Redirected
      - With Your Decentralized Framework for Drug Assessment
      - The Result
  - The Bottom Line
    - The ratio: 1 in 1,263 (drug trials) or 1 in 480 (all clinical research) among disease patients.

### Detailed Calculations

#### knowledge/appendix/parameters-and-calculations.qmd
**Title:** Methodology, Parameters, and Calculations
**Description:** Parameter definitions, formulas, uncertainty ranges, and data sources.
**Stats:** 54,274 words | 14,688 lines

  - Overview {#sec-parameters-and-calculations}
    - Quick Navigation
  - Calculated Values {#sec-calculated}
    - Additional Drug Approvals from Cost Elimination: 20 drugs/year {#sec-additional_drugs_from_cost_elimination}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs Total (US): $5.03T {#sec-bad_policy_cost_total_us}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs (% GDP): 17.5% {#sec-bad_policy_cost_total_us_pct_gdp}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs (Tier 1): $3.92T {#sec-bad_policy_cost_us_tier1_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Bad Policy Costs (Tier 2): $2T {#sec-bad_policy_cost_us_tier2_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cell Therapy Combinations: 500k combinations {#sec-cell_therapy_disease_combinations}
      - Sensitivity Analysis
    - Annual Chronic Disease Patients Treated: 982M people {#sec-chronic_disease_treated_patients_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Clinical Trial Cost Per Approved Drug: $1.20B {#sec-clinical_trial_cost_per_approved_drug}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost Per Clinical Trial Participant: $31.6K {#sec-clinical_trial_cost_per_participant_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Combination Therapy Space: 45.1B combinations {#sec-combination_therapy_disease_space}
      - Sensitivity Analysis
    - Pairwise Drug Combinations: 45.1M combinations {#sec-combination_therapy_pairs}
      - Sensitivity Analysis
    - Combined Peace and Health Dividends for ROI Calculation: $172B {#sec-combined_peace_health_dividends_annual_for_roi_calc}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Combination Therapy Exploration Time (Current): 13.7M years {#sec-current_combination_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Known Safe Exploration Time (Current): 2.88k years {#sec-current_known_safe_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Current Patient Participation Rate in Clinical Trials: 0.0792% {#sec-current_patient_participation_rate}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Exploration Time (Current): 15.6k years {#sec-current_total_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Decentralized Framework for Drug Assessment Operational Costs: $40M {#sec-dfda_annual_opex}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Annual Benefit: R&D Savings: $58.6B {#sec-dfda_benefit_rd_only_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Combined Treatment Discovery Speedup Multiplier: 17.2x {#sec-dfda_combined_treatment_speedup_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Direct Funding Cost per DALY: $0.841 {#sec-dfda_direct_funding_cost_per_daly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Direct Funding NPV (Queue Clearance Period): $475B {#sec-dfda_direct_funding_queue_clearance_npv}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Direct Funding ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput: 178k:1 {#sec-dfda_direct_funding_roi_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Direct Funding Cost-Effectiveness vs Bed Nets: 106:1 {#sec-dfda_direct_funding_vs_bed_nets_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total DALYs Lost from Disease Eradication Delay: 7.94B DALYs {#sec-dfda_efficacy_lag_elimination_dalys}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Deaths from Disease Eradication Delay: 416M deaths {#sec-dfda_efficacy_lag_elimination_deaths_averted}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Loss from Disease Eradication Delay: $1.19 quadrillion {#sec-dfda_efficacy_lag_elimination_economic_value}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Years Lived with Disability During Disease Eradication Delay: 873M years {#sec-dfda_efficacy_lag_elimination_yld}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Years of Life Lost from Disease Eradication Delay: 7.07B years {#sec-dfda_efficacy_lag_elimination_yll}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA New Treatments Per Year: 185 diseases/year {#sec-dfda_first_treatments_per_year}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Known Safe Exploration Time (dFDA): 234 years {#sec-dfda_known_safe_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Annual Net Savings (R&D Only): $58.6B {#sec-dfda_net_savings_rd_only_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Total NPV Annual OPEX: $40M {#sec-dfda_npv_annual_opex_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - NPV of Decentralized Framework for Drug Assessment Benefits (R&D Only, 10-Year Discounted): $389B {#sec-dfda_npv_benefit_rd_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - NPV Net Benefit (R&D Only): $389B {#sec-dfda_npv_net_benefit_rd_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Present Value of Annual OPEX Over 10 Years: $342M {#sec-dfda_npv_pv_annual_opex}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Total NPV Cost: $611M {#sec-dfda_npv_total_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Total NPV Upfront Costs: $270M {#sec-dfda_npv_upfront_cost_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Overhead Percentage of Treaty Funding: 0.147% {#sec-dfda_opex_pct_of_treaty_funding}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Queue Clearance Time: 36 years {#sec-dfda_queue_clearance_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Daily R&D Savings from Trial Cost Reduction: $161M {#sec-dfda_rd_savings_daily}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - ROI from Decentralized Framework for Drug Assessment R&D Savings Only: 637:1 {#sec-dfda_roi_rd_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Infrastructure Cost per Patient (Annual): $8.64 {#sec-dfda_storage_cost_total_per_patient_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Infrastructure Cost per Patient (Monthly): $0.720 {#sec-dfda_storage_cost_total_per_patient_monthly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Exploration Time (dFDA): 1.27k years {#sec-dfda_total_exploration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Decentralized Framework for Drug Assessment Maximum Trials per Year: 40.6k trials/year {#sec-dfda_trials_per_year_capacity}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - DALYs Averted from Trial Capacity Increase: 543B DALYs {#sec-dfda_trial_capacity_dalys_averted}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Economic Value from Trial Capacity Increase: $81.5 quadrillion {#sec-dfda_trial_capacity_economic_value}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Lives Saved from Trial Capacity Increase: 10.3B deaths {#sec-dfda_trial_capacity_lives_saved}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Trial Capacity Multiplier: 12.3:1 {#sec-dfda_trial_capacity_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total DALYs from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: 565B DALYs {#sec-dfda_trial_capacity_plus_efficacy_lag_dalys}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Benefit from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: $84.8 quadrillion {#sec-dfda_trial_capacity_plus_efficacy_lag_economic_value}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Lives Saved from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: 10.7B deaths {#sec-dfda_trial_capacity_plus_efficacy_lag_lives_saved}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Suffering Hours Eliminated from Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Higher Trial Throughput: 1931T hours {#sec-dfda_trial_capacity_plus_efficacy_lag_suffering_hours}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Average Total Timeline Shift: 212 years {#sec-dfda_trial_capacity_plus_efficacy_lag_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Treatment Timeline Acceleration: 204 years {#sec-dfda_trial_capacity_treatment_acceleration_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Trial Cost Reduction Factor: 44.1x {#sec-dfda_trial_cost_reduction_factor}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Trial Cost Reduction Percentage: 97.7% {#sec-dfda_trial_cost_reduction_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - dFDA Valley of Death Rescue Multiplier: 1.4x {#sec-dfda_valley_of_death_rescue_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Patients Fundable Annually: 23.4M patients/year {#sec-dih_patients_fundable_annually}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Medical Research Percentage of Treaty Funding: 80% {#sec-dih_treasury_medical_research_pct}
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Funding for Pragmatic Clinical Trials: $21.8B {#sec-dih_treasury_to_medical_research_annual}
    - Annual Clinical Trial Patient Subsidies: $21.7B {#sec-dih_treasury_trial_subsidies_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Patient Trial Subsidies Percentage of Treaty Funding: 79.9% {#sec-dih_treasury_trial_subsidies_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Diseases Without Effective Treatment: 6.65k diseases {#sec-diseases_without_effective_treatment}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Annual Disease Deaths to 9/11 Terrorism Deaths: 18.4k:1 {#sec-disease_vs_terrorism_deaths_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Annual Disease Deaths to War Deaths: 225:1 {#sec-disease_vs_war_deaths_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Coverage Factor of Treaty Funding vs Decentralized Framework for Drug Assessment OPEX: 680:1 {#sec-dividend_coverage_factor}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Drugs Approved Since 1962: 3.10k drugs {#sec-drugs_approved_since_1962}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Drug Cost Increase: 1980s to Current: 13.4:1 {#sec-drug_cost_increase_1980s_to_current_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Drug Cost Increase: Pre-1962 to Current: 105:1 {#sec-drug_cost_increase_pre1962_to_current_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Possible Drug-Disease Combinations: 9.50M combinations {#sec-drug_disease_combinations_possible}
      - Sensitivity Analysis
    - Cumulative Efficacy Testing Cost (1962-2024): $4.84T {#sec-efficacy_lag_cumulative_excess_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Efficacy Lag Deaths (9/11 Equivalents): 34.1k 9/11s {#sec-efficacy_lag_deaths_911_equivalents}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treatment Delay YLD - Annual: 2.01B DALYs {#sec-efficacy_lag_treatment_delay_yld_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Emerging Modality Combinations: 42.0M combinations {#sec-emerging_modality_combinations}
      - Sensitivity Analysis
    - Epigenetic Therapy Combinations: 1.50M combinations {#sec-epigenetic_disease_combinations}
      - Sensitivity Analysis
    - Total Deaths from Historical Progress Delays: 102M deaths {#sec-existing_drugs_efficacy_lag_deaths_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Loss from Historical Progress Delays: $259T {#sec-existing_drugs_efficacy_lag_economic_loss}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Therapeutic Frontier Exploration Ratio: 0.342% {#sec-exploration_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - FDA to Oxford RECOVERY Trial Time Multiplier: 36.4:1 {#sec-fda_to_oxford_recovery_trial_time_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Gene Therapy Combinations: 20.0M combinations {#sec-gene_therapy_disease_combinations}
      - Sensitivity Analysis
    - Total Annual Conflict Deaths Globally: 245k deaths/year {#sec-global_annual_conflict_deaths_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Cost of War Worldwide: $11.4T {#sec-global_annual_direct_indirect_war_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost of Combat Deaths: $2.34T {#sec-global_annual_human_cost_active_combat}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost of State Violence Deaths: $27B {#sec-global_annual_human_cost_state_violence}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Cost of Terror Deaths: $83B {#sec-global_annual_human_cost_terror_attacks}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Human Life Losses from Conflict: $2.45T {#sec-global_annual_human_life_losses_conflict}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Infrastructure Destruction: $1.88T {#sec-global_annual_infrastructure_destruction_conflict}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Trade Disruption: $616B {#sec-global_annual_trade_disruption_conflict}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Direct War Costs: $7.66T {#sec-global_annual_war_direct_costs_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Indirect War Costs: $3.70T {#sec-global_annual_war_indirect_costs_total}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cost per Life Saved by Medical Research: $16.1K {#sec-global_cost_per_life_saved_med_research_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Economic Burden of Disease Globally: $109T {#sec-global_disease_economic_burden_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Global Industry Spending on Clinical Trials: $55.5B {#sec-global_industry_clinical_trials_spending_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Per Capita Military Spending Globally: $340 {#sec-global_military_spending_per_capita_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Global Military Spending After 1% Treaty Reduction: $2.69T {#sec-global_military_spending_post_treaty_annual_2024}
    - Total Annual Cost of War and Disease with All Externalities: $129T {#sec-global_total_health_and_war_cost_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Healthcare vs Military Multiplier Ratio: 7.17:1 {#sec-healthcare_vs_military_multiplier_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - IAB Mechanism Benefit-Cost Ratio: 230:1 {#sec-iab_mechanism_benefit_cost_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual IAB Political Incentive Funding: $2.72B {#sec-iab_political_incentive_funding_annual}
    - Ratio of Industry to Government Clinical Trials Spending: 12.3:1 {#sec-industry_vs_government_clinical_trials_spending_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Life Expectancy Gain Rate (1883-1962): 0 years/decade {#sec-life_expectancy_gain_1883_1962_years_per_decade}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Life Expectancy Gain Rate (1962-2019): 0 years/decade {#sec-life_expectancy_gain_1962_2019_years_per_decade}
      - Sensitivity Analysis
    - Medical Research Spending as Percentage of Total Disease Burden: 0.0525% {#sec-medical_research_pct_of_disease_burden}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Military to Clinical Trials Spending: 45.3:1 {#sec-military_to_clinical_trials_spending_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Military to Government Clinical Trials Spending: 604:1 {#sec-military_to_government_clinical_trials_spending_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Military Spending to Medical Research Spending: 40.3:1 {#sec-military_vs_medical_research_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Misallocation Factor: Cost to Kill vs Cost to Save: 2.89k:1 {#sec-misallocation_factor_death_vs_saving}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - mRNA Therapeutic Combinations: 20.0M combinations {#sec-mrna_therapeutic_combinations}
      - Sensitivity Analysis
    - Annual Peace Dividend from 1% Reduction in Total War Costs: $114B {#sec-peace_dividend_annual_societal_benefit}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Conflict Reduction Benefits from 1% Less Military Spending: $86.4B {#sec-peace_dividend_conflict_reduction}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Direct War Costs: $76.6B {#sec-peace_dividend_direct_costs}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Environmental Damage: $1B {#sec-peace_dividend_environmental}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Human Casualties: $24.5B {#sec-peace_dividend_human_casualties}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Indirect War Costs: $37B {#sec-peace_dividend_indirect_costs}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Infrastructure Destruction: $18.8B {#sec-peace_dividend_infrastructure}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Lost Economic Growth: $27.2B {#sec-peace_dividend_lost_economic_growth}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Lost Human Capital: $3B {#sec-peace_dividend_lost_human_capital}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in PTSD and Mental Health Costs: $2.32B {#sec-peace_dividend_ptsd}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Refugee Support Costs: $1.50B {#sec-peace_dividend_refugee_support}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Trade Disruption: $6.16B {#sec-peace_dividend_trade_disruption}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Savings from 1% Reduction in Veteran Healthcare Costs: $2B {#sec-peace_dividend_veteran_healthcare}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Personal Lifetime Wealth (QALY-Based): $3M {#sec-personal_lifetime_wealth}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Per Capita Chronic Disease Cost: $12.2K {#sec-per_capita_chronic_disease_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Per Capita Mental Health Cost: $1.04K {#sec-per_capita_mental_health_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Lives Saved by Pharmaceuticals: 12.4M deaths {#sec-pharma_lives_saved_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Political Dysfunction Tax (Total): 20% {#sec-political_dysfunction_tax_total_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Pragmatic Trial Cost per QALY (RECOVERY): $4.00 {#sec-pragmatic_trial_cost_per_qaly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Pragmatic Trial Efficiency Multiplier vs NIH: 12.5k:1 {#sec-pragmatic_vs_nih_efficiency_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - RECOVERY Trial Cost Reduction Factor: 82x {#sec-recovery_trial_cost_reduction_factor}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - RECOVERY Trial Total QALYs Generated: 5.00M QALYs {#sec-recovery_trial_total_qalys_generated}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Status Quo Average Years to First Treatment: 222 years {#sec-status_quo_avg_years_to_first_treatment}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Status Quo Queue Clearance Time: 443 years {#sec-status_quo_queue_clearance_years}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide DALYs Per Event: 41.8k DALYs {#sec-thalidomide_dalys_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide Deaths Per Event: 360 deaths {#sec-thalidomide_deaths_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide Survivors Per Event: 540 cases {#sec-thalidomide_survivors_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide US Cases Prevented: 900 cases {#sec-thalidomide_us_cases_prevented}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide YLD Per Event: 13.0k years {#sec-thalidomide_yld_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Thalidomide YLL Per Event: 28.8k years {#sec-thalidomide_yll_per_event}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Global Research Funding (Baseline + 1% treaty Funding): $94.7B {#sec-total_research_funding_with_treaty}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Testable Therapeutic Space: 51.5M combinations {#sec-total_testable_therapeutic_combinations}
      - Sensitivity Analysis
    - Annual Funding from 1% of Global Military Spending Redirected to DIH: $27.2B {#sec-treaty_annual_funding}
    - Treaty System Benefit Multiplier vs Childhood Vaccination Programs: 11.5:1 {#sec-treaty_benefit_multiplier_vs_vaccines}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Amortized Annual Treaty Campaign Cost: $250M {#sec-treaty_campaign_annual_cost_amortized}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total 1% Treaty Campaign Cost: $1B {#sec-treaty_campaign_total_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Target Voting Bloc Size for Campaign: 280M of people {#sec-treaty_campaign_voting_bloc_target}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cost per DALY Averted (Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput): $0.0018 {#sec-treaty_cost_per_daly_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Expected Cost per DALY (Risk-Adjusted): $0.177 {#sec-treaty_expected_cost_per_daly}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Expected Treaty ROI (Risk-Adjusted): 848k:1 {#sec-treaty_expected_roi_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Expected Cost-Effectiveness vs Bed Nets Multiplier: 503:1 {#sec-treaty_expected_vs_bed_nets_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual Lives Saved from 1% Reduction in Conflict Deaths: 2.45k lives/year {#sec-treaty_lives_saved_annual_global}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - 1% treaty Basic Annual Benefits (Peace + R&D Savings): $172B {#sec-treaty_peace_plus_rd_annual_benefits}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Annual QALYs Gained from Peace Dividend: 85.6k QALYs/year {#sec-treaty_qalys_gained_annual_global}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - 1% treaty Recurring Annual Benefits: $172B {#sec-treaty_recurring_benefits_annual}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treaty ROI - Historical Rate (Existing Drugs): 259k:1 {#sec-treaty_roi_existing_drugs_only}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treaty ROI - Elimination of Efficacy Lag Plus Earlier Treatment Discovery from Increased Trial Throughput: 84.8M:1 {#sec-treaty_roi_trial_capacity_plus_efficacy_lag}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Total Annual Treaty System Costs: $290M {#sec-treaty_total_annual_costs}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cost-Effectiveness vs Bed Nets Multiplier: 50.3k:1 {#sec-treaty_vs_bed_nets_multiplier}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Treaty Campaign Leverage vs Direct Funding: 475:1 {#sec-treaty_vs_direct_funding_leverage}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Cumulative Trial Capacity Years Over 20 Years: 246 years {#sec-trial_capacity_cumulative_years_20yr}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Ratio of Type Ii Error Cost to Type I Error Benefit: 3.07k:1 {#sec-type_ii_error_cost_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Maximum DALYs Saved by FDA Preventing Unsafe Drugs (1962-2024): 2.59M DALYs {#sec-type_i_error_benefit_dalys}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Unexplored Therapeutic Frontier: 99.7% {#sec-unexplored_ratio}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Congress Full Advocacy Cost: $5.35B {#sec-us_congress_full_advocacy_cost}
      - Sensitivity Analysis
    - US Major Diseases Total Annual Cost: $1.25T {#sec-us_major_diseases_total_annual_cost}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - US Senate Treaty Advocacy Cost: $670M {#sec-us_senate_treaty_advocacy_cost}
      - Sensitivity Analysis
    - Annual VICTORY Incentive Alignment Bond Payout: $2.72B {#sec-victory_bond_annual_payout}
    - Annual Return Percentage for VICTORY Incentive Alignment Bondholders: 272% {#sec-victory_bond_annual_return_pct}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
    - Global Patients Willing to Participate in Clinical Trials: 1.08B people {#sec-willing_trial_participants_global}
      - Sensitivity Analysis
      - Monte Carlo Distribution
      - Exceedance Probability
  - External Data Sources {#sec-external}
    - ADAPTABLE Trial Cost per Patient: $929 {#sec-adaptable_trial_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - ADAPTABLE Trial Total Cost: $14M {#sec-adaptable_trial_total_cost}
      - Uncertainty Range
      - Input Distribution
    - Antidepressant Trial Exclusion Rate: 86.1% {#sec-antidepressant_trial_exclusion_rate}
    - Average Annual Stock Market Return: 10% {#sec-average_market_return_pct}
    - Agricultural Subsidies Deadweight Loss: $75B {#sec-bad_policy_cost_us_agricultural_subsidies}
      - Uncertainty Range
      - Input Distribution
    - Defense Above Deterrence: $400B {#sec-bad_policy_cost_us_defense_above_deterrence}
      - Uncertainty Range
      - Input Distribution
    - Drug War Cost: $90B {#sec-bad_policy_cost_us_drug_war}
      - Uncertainty Range
      - Input Distribution
    - Failed Wars (Amortized): $400B {#sec-bad_policy_cost_us_failed_wars}
      - Uncertainty Range
      - Input Distribution
    - Fossil Fuel Explicit Subsidies: $50B {#sec-bad_policy_cost_us_fossil_fuel_explicit}
      - Uncertainty Range
      - Input Distribution
    - Fossil Fuel Externalities: $600B {#sec-bad_policy_cost_us_fossil_fuel_externalities}
      - Uncertainty Range
      - Input Distribution
    - Healthcare System Inefficiency: $1.20T {#sec-bad_policy_cost_us_healthcare_inefficiency}
      - Uncertainty Range
      - Input Distribution
    - Housing/Zoning Restrictions Cost: $1.40T {#sec-bad_policy_cost_us_housing_zoning}
      - Uncertainty Range
      - Input Distribution
    - Incarceration Excess Costs: $150B {#sec-bad_policy_cost_us_incarceration_excess}
      - Uncertainty Range
      - Input Distribution
    - Infrastructure Cost Disease: $150B {#sec-bad_policy_cost_us_infrastructure_disease}
      - Uncertainty Range
      - Input Distribution
    - Migration Restrictions Cost (US Share): $500B {#sec-bad_policy_cost_us_migration_restrictions}
      - Uncertainty Range
      - Input Distribution
    - Occupational Licensing Cost: $200B {#sec-bad_policy_cost_us_occupational_licensing}
      - Uncertainty Range
      - Input Distribution
    - Tariff Cost (GDP Loss): $160B {#sec-bad_policy_cost_us_tariffs}
      - Uncertainty Range
      - Input Distribution
    - Tax Compliance Cost: $546B {#sec-bad_policy_cost_us_tax_compliance}
      - Uncertainty Range
      - Input Distribution
    - Baseline Annual Lives Saved by Pharmaceuticals: 12 deaths/year {#sec-baseline_lives_saved_annual}
    - Bed Nets Cost per DALY: $89 {#sec-bed_nets_cost_per_daly}
      - Uncertainty Range
      - Input Distribution
    - Total Annual Value of Unpaid Caregiving in US: $600B {#sec-caregiver_annual_value_total}
    - Number of Unpaid Caregivers in US: 38.0M people {#sec-caregiver_count_us}
    - Average Monthly Hours of Unpaid Family Caregiving in US: 20 hours/month {#sec-caregiver_hours_per_month}
    - Estimated Replacement Cost per Hour of Caregiving: $25 {#sec-caregiver_value_per_hour_simple}
    - Estimated Annual Global Economic Benefit from Childhood Vaccination Programs: $15B {#sec-childhood_vaccination_annual_benefit}
      - Uncertainty Range
      - Input Distribution
    - Return on Investment from Childhood Vaccination Programs: 13:1 {#sec-childhood_vaccination_roi}
    - Disability Weight for Untreated Chronic Conditions: 0.35 weight {#sec-chronic_disease_disability_weight}
      - Uncertainty Range
      - Input Distribution
    - CPI Multiplier: 1980 to 2024: 3.8:1 {#sec-cpi_multiplier_1980_to_2024}
      - Uncertainty Range
      - Input Distribution
    - Crony Tax (Capture): 10% {#sec-crony_tax_pct}
      - Uncertainty Range
      - Input Distribution
    - Current Active Trials at Any Given Time: 10.0k trials {#sec-current_active_trials}
    - Current Clinical Trial Participation Rate: 0.06% {#sec-current_clinical_trial_participation_rate}
    - Global Population with Chronic Diseases: 2.40B people {#sec-current_disease_patients_global}
      - Uncertainty Range
      - Input Distribution
    - Average Annual New Drug Approvals Globally: 50 drugs/year {#sec-current_drug_approvals_per_year}
      - Uncertainty Range
      - Input Distribution
    - Current Global Clinical Trials per Year: 3.30k trials/year {#sec-current_trials_per_year}
      - Uncertainty Range
      - Input Distribution
    - Current Trial Abandonment Rate: 40% {#sec-current_trial_abandonment_rate}
    - Annual Global Clinical Trial Participants: 1.90M patients/year {#sec-current_trial_slots_available}
      - Uncertainty Range
      - Input Distribution
    - Annual Defense Industry Lobbying Spending: $127M {#sec-defense_lobbying_annual}
    - Deworming Cost per DALY: $55 {#sec-deworming_cost_per_daly}
    - dFDA Pragmatic Trial Cost per Patient: $929 {#sec-dfda_pragmatic_trial_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Drug Development Cost (1980s): $194M {#sec-drug_development_cost_1980s}
      - Uncertainty Range
      - Input Distribution
    - Drug Repurposing Success Rate: 30% {#sec-drug_repurposing_success_rate}
    - Economic Multiplier for Education Investment: 2.1:1 {#sec-economic_multiplier_education_investment}
    - Economic Multiplier for Healthcare Investment: 4.3:1 {#sec-economic_multiplier_healthcare_investment}
      - Uncertainty Range
      - Input Distribution
    - Economic Multiplier for Infrastructure Investment: 1.6:1 {#sec-economic_multiplier_infrastructure_investment}
    - Economic Multiplier for Military Spending: 0.6:1 {#sec-economic_multiplier_military_spending}
      - Uncertainty Range
      - Input Distribution
    - Regulatory Delay for Efficacy Testing Post-Safety Verification: 8.2 years {#sec-efficacy_lag_years}
      - Uncertainty Range
      - Input Distribution
    - FDA-Approved Drug Products: 20.0k products {#sec-fda_approved_products_count}
    - FDA-Approved Unique Active Ingredients: 1.65k compounds {#sec-fda_approved_unique_active_ingredients}
      - Uncertainty Range
      - Input Distribution
    - FDA GRAS Substances: 635 substances {#sec-fda_gras_substances_count}
      - Uncertainty Range
      - Input Distribution
    - FDA Phase 1 to Approval Timeline: 9.1 years {#sec-fda_phase_1_to_approval_years}
      - Uncertainty Range
      - Input Distribution
    - Givewell Average Cost per Life Saved Across Top Charities: $4.50K {#sec-givewell_cost_per_life_avg}
    - Givewell Cost per Life Saved (Maximum): $5.50K {#sec-givewell_cost_per_life_max}
    - Givewell Cost per Life Saved (Minimum): $3.50K {#sec-givewell_cost_per_life_min}
    - Annual Deaths from Active Combat Worldwide: 234k deaths/year {#sec-global_annual_conflict_deaths_active_combat}
      - Uncertainty Range
      - Input Distribution
    - Annual Deaths from State Violence: 2.70k deaths/year {#sec-global_annual_conflict_deaths_state_violence}
      - Uncertainty Range
      - Input Distribution
    - Annual Deaths from Terror Attacks Globally: 8.30k deaths/year {#sec-global_annual_conflict_deaths_terror_attacks}
      - Uncertainty Range
      - Input Distribution
    - Global Annual DALY Burden: 2.88B DALYs/year {#sec-global_annual_daly_burden}
      - Uncertainty Range
      - Input Distribution
    - Annual Deaths from All Diseases and Aging Globally: 55.0M deaths/year {#sec-global_annual_deaths_curable_diseases}
      - Uncertainty Range
      - Input Distribution
    - Annual Environmental Damage and Restoration Costs from Conflict: $100B {#sec-global_annual_environmental_damage_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Communications from Conflict: $298B {#sec-global_annual_infrastructure_damage_communications_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Education Facilities from Conflict: $234B {#sec-global_annual_infrastructure_damage_education_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Energy Systems from Conflict: $422B {#sec-global_annual_infrastructure_damage_energy_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Healthcare Facilities from Conflict: $166B {#sec-global_annual_infrastructure_damage_healthcare_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Transportation from Conflict: $487B {#sec-global_annual_infrastructure_damage_transportation_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Infrastructure Damage to Water Systems from Conflict: $268B {#sec-global_annual_infrastructure_damage_water_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Lives Saved by Medical Research Globally: 4.20M lives/year {#sec-global_annual_lives_saved_by_med_research}
      - Uncertainty Range
      - Input Distribution
    - Annual Lost Economic Growth from Military Spending Opportunity Cost: $2.72T {#sec-global_annual_lost_economic_growth_military_spending}
      - Uncertainty Range
      - Input Distribution
    - Annual Lost Productivity from Conflict Casualties: $300B {#sec-global_annual_lost_human_capital_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual PTSD and Mental Health Costs from Conflict: $232B {#sec-global_annual_psychological_impact_costs_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Refugee Support Costs: $150B {#sec-global_annual_refugee_support_costs}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Currency Instability: $57.4B {#sec-global_annual_trade_disruption_currency_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Energy Price Volatility: $125B {#sec-global_annual_trade_disruption_energy_price_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Shipping Disruptions: $247B {#sec-global_annual_trade_disruption_shipping_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Trade Disruption Costs from Supply Chain Disruptions: $187B {#sec-global_annual_trade_disruption_supply_chain_conflict}
      - Uncertainty Range
      - Input Distribution
    - Annual Veteran Healthcare Costs: $200B {#sec-global_annual_veteran_healthcare_costs}
      - Uncertainty Range
      - Input Distribution
    - Annual Days of Chronic Disease Therapy: 1.28T days {#sec-global_chronic_therapy_days_annual}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Spending on Clinical Trials: $60B {#sec-global_clinical_trials_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Daily Deaths from Disease and Aging: 150k deaths/day {#sec-global_disease_deaths_daily}
      - Uncertainty Range
      - Input Distribution
    - Global Annual Direct Medical Costs of Disease: $9.90T {#sec-global_disease_direct_medical_cost_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Annual Economic Value of Human Life Lost to Disease: $94.2T {#sec-global_disease_human_life_value_loss_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Annual Productivity Loss from Disease: $5T {#sec-global_disease_productivity_loss_annual}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Government Spending on Clinical Trials: $4.50B {#sec-global_government_clinical_trials_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - Global Household Wealth: $454T {#sec-global_household_wealth_usd}
    - Global Life Expectancy (2024): 79 years {#sec-global_life_expectancy_2024}
      - Uncertainty Range
      - Input Distribution
    - Global Government Medical Research Spending: $67.5B {#sec-global_med_research_spending}
      - Uncertainty Range
      - Input Distribution
    - Global Military Spending in 2024: $2.72T {#sec-global_military_spending_annual_2024}
      - Uncertainty Range
    - Annual Global Nonprofit Spending on Clinical Trials: $3.50B {#sec-global_nonprofit_clinical_trials_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Pharmaceutical R&D Spending: $300B {#sec-global_pharma_rd_spending_annual}
    - Global Population in 2024: 8.00B of people {#sec-global_population_2024}
      - Uncertainty Range
      - Input Distribution
    - Critical Mass Threshold for Social Change: 3.5% {#sec-global_population_activism_threshold_pct}
      - Uncertainty Range
      - Input Distribution
    - Annual Global Spending on Symptomatic Disease Treatment: $8.20T {#sec-global_symptomatic_disease_treatment_annual}
      - Uncertainty Range
      - Input Distribution
    - YLD Proportion of Total DALYs: 0.39 proportion {#sec-global_yld_proportion_of_dalys}
      - Uncertainty Range
      - Input Distribution
    - Estimated Total Economic Impact of Human Genome Project: $1T {#sec-human_genome_project_total_economic_impact}
    - Human Interactome Targeted by Drugs: 12% {#sec-human_interactome_targeted_pct}
    - ICD-10 Total Codes: 14.0k codes {#sec-icd_10_total_codes}
    - Life Extension from Treaty Research Acceleration: 20 years {#sec-life_extension_years}
      - Uncertainty Range
      - Input Distribution
    - Maximum Annual Lobbyist Salary Range: $2M {#sec-lobbyist_salary_max}
    - Minimum Annual Lobbyist Salary Range: $500K {#sec-lobbyist_salary_min_k}
    - Return on Investment from Measles Vaccination Programs: 14:1 {#sec-measles_vaccination_roi}
    - Annual Productivity Loss per Capita from Mental Health Issues: $2K {#sec-mental_health_productivity_loss_per_capita}
    - NATO Defense Spending (2024): $1.51T {#sec-nato_defense_spending_annual}
    - Diseases Getting First Treatment Per Year: 15 diseases/year {#sec-new_disease_first_treatments_per_year}
      - Uncertainty Range
      - Input Distribution
    - NIH Annual Budget: $47B {#sec-nih_annual_budget}
      - Uncertainty Range
      - Input Distribution
    - NIH Clinical Trials Spending Percentage: 3.3% {#sec-nih_clinical_trials_spending_pct}
      - Uncertainty Range
      - Input Distribution
    - NIH Standard Research Cost per QALY: $50K {#sec-nih_standard_research_cost_per_qaly}
      - Uncertainty Range
      - Input Distribution
    - Oxford RECOVERY Trial Duration: 3 months {#sec-oxford_recovery_trial_duration_months}
      - Uncertainty Range
    - Patient Willingness to Participate in Clinical Trials: 44.8% {#sec-patient_willingness_trial_participation_pct}
      - Uncertainty Range
      - Input Distribution
    - Pharma Drug Development Cost (Current System): $2.60B {#sec-pharma_drug_development_cost_current}
      - Uncertainty Range
      - Input Distribution
    - Pharma Average Drug Revenue (Current System): $6.70B {#sec-pharma_drug_revenue_average_current}
    - Annual Life-Years Saved by Pharmaceuticals: 149M life-years {#sec-pharma_life_years_saved_annual}
      - Uncertainty Range
      - Input Distribution
    - Pharma ROI (Current System): 1.2% {#sec-pharma_roi_current_system_pct}
    - Pharma Drug Success Rate (Current System): 10% {#sec-pharma_success_rate_current_pct}
    - Phase I-Passed Compounds Globally: 7.50k compounds {#sec-phase_1_passed_compounds_global}
      - Uncertainty Range
      - Input Distribution
    - Phase I Safety Trial Duration: 2.3 years {#sec-phase_1_safety_duration_years}
    - Phase 2/3 Share of Clinical Trial Costs: 69% {#sec-phase_2_3_clinical_trial_cost_pct}
      - Uncertainty Range
      - Input Distribution
    - Phase 3 Trial Total Cost (Minimum): $20M {#sec-phase_3_trial_cost_min}
    - Pragmatic Trial Median Cost per Patient (PMC Review): $97 {#sec-pmc_pragmatic_trial_median_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Return on Investment from Sustaining Polio Vaccination Assets and Integrating into Expanded Immunization Programs: 39:1 {#sec-polio_vaccination_roi}
    - Coordination Tax (Olson): 5% {#sec-political_dysfunction_tax_coordination_pct}
      - Uncertainty Range
      - Input Distribution
    - Information Tax (Hayek): 2% {#sec-political_dysfunction_tax_info_pct}
      - Uncertainty Range
      - Input Distribution
    - Time-Inconsistency Tax: 3% {#sec-political_dysfunction_tax_time_pct}
      - Uncertainty Range
      - Input Distribution
    - Political Success Probability: 1% {#sec-political_success_probability}
      - Uncertainty Range
      - Input Distribution
    - Post-Office Career Value (per politician): $10M {#sec-politician_post_office_career_value}
      - Uncertainty Range
      - Input Distribution
    - Post-1962 Drug Approval Reduction: 70% {#sec-post_1962_drug_approval_reduction_pct}
    - Percentage Military Spending Cut After WW2: 30% {#sec-post_ww2_military_cut_pct}
    - Pre-1962 Drug Development Cost (1980 Dollars): $6.50M {#sec-pre_1962_drug_development_cost_1980_usd}
      - Uncertainty Range
      - Input Distribution
    - Pre-1962 Drug Development Cost (2024 Dollars): $24.7M {#sec-pre_1962_drug_development_cost_2024_usd}
      - Uncertainty Range
      - Input Distribution
    - Pre-1962 Physician Count (Unverified): 144k physicians {#sec-pre_1962_physician_count}
    - Total Number of Rare Diseases Globally: 7.00k diseases {#sec-rare_diseases_count_global}
      - Uncertainty Range
      - Input Distribution
    - Recovery Trial Cost per Patient: $500 {#sec-recovery_trial_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - RECOVERY Trial Global Lives Saved: 1.00M lives {#sec-recovery_trial_global_lives_saved}
      - Uncertainty Range
      - Input Distribution
    - RECOVERY Trial Total Cost: $20M {#sec-recovery_trial_total_cost}
      - Uncertainty Range
      - Input Distribution
    - Mean Age of Preventable Death from Post-Safety Efficacy Delay: 62 years {#sec-regulatory_delay_mean_age_of_death}
      - Uncertainty Range
      - Input Distribution
    - Pre-Death Suffering Period During Post-Safety Efficacy Delay: 6 years {#sec-regulatory_delay_suffering_period_years}
      - Uncertainty Range
      - Input Distribution
    - September 11 Deaths: 2.98k people {#sec-sept_11_deaths}
      - Uncertainty Range
    - Singapore GDP per Capita (PPP): $105K {#sec-singapore_gdp_per_capita_ppp}
      - Uncertainty Range
    - Singapore Govt Spending (% GDP): 1500% {#sec-singapore_govt_spending_pct_gdp}
      - Uncertainty Range
    - Singapore Life Expectancy: 84.1 years {#sec-singapore_life_expectancy}
      - Uncertainty Range
    - Return on Investment from Smallpox Eradication Campaign: 280:1 {#sec-smallpox_eradication_roi}
    - Total Economic Benefit from Smallpox Eradication Campaign: $1.42B {#sec-smallpox_eradication_total_benefit}
    - Estimated Annual Global Economic Benefit from Smoking Cessation Programs: $12B {#sec-smoking_cessation_annual_benefit}
    - Standard Economic Value per QALY: $150K {#sec-standard_economic_qaly_value_usd}
      - Uncertainty Range
      - Input Distribution
    - Standard QALYs per Life Saved: 35 QALYs/life {#sec-standard_qalys_per_life_saved}
      - Uncertainty Range
      - Input Distribution
    - Annual Cost of Sugar Subsidies per Person: $10 {#sec-sugar_subsidy_cost_per_person_annual}
    - Switzerland's Defense Spending as Percentage of GDP: 0.7% {#sec-switzerland_defense_spending_pct}
    - Switzerland GDP per Capita: $93K {#sec-switzerland_gdp_per_capita_k}
    - Switzerland Govt Spending (% GDP): 3500% {#sec-switzerland_govt_spending_pct_gdp}
      - Uncertainty Range
    - Switzerland Life Expectancy: 84 years {#sec-switzerland_life_expectancy}
      - Uncertainty Range
    - Switzerland Median Income (PPP): $65K {#sec-switzerland_median_income_ppp}
      - Uncertainty Range
    - Deaths from 9/11 Terrorist Attacks: 3.00k deaths {#sec-terrorism_deaths_911}
      - Uncertainty Range
    - Thalidomide Cases Worldwide: 15.0k cases {#sec-thalidomide_cases_worldwide}
      - Uncertainty Range
      - Input Distribution
    - Thalidomide Disability Weight: 0.4:1 {#sec-thalidomide_disability_weight}
      - Uncertainty Range
      - Input Distribution
    - Thalidomide Mortality Rate: 40% {#sec-thalidomide_mortality_rate}
      - Uncertainty Range
      - Input Distribution
    - Thalidomide Survivor Lifespan: 60 years {#sec-thalidomide_survivor_lifespan}
      - Uncertainty Range
      - Input Distribution
    - US Population Share 1960: 6% {#sec-thalidomide_us_population_share_1960}
      - Uncertainty Range
      - Input Distribution
    - Phase 3 Cost per Patient: $41K {#sec-traditional_phase3_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Traditional FDA Drug Development Timeline: 17 years {#sec-treatment_acceleration_years_current}
    - Treatment Disability Reduction: 0.25 weight {#sec-treatment_disability_reduction}
      - Uncertainty Range
      - Input Distribution
    - US Alzheimer's Annual Cost: $355B {#sec-us_alzheimers_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US Cancer Annual Cost: $208B {#sec-us_cancer_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US Annual Chronic Disease Spending: $4.10T {#sec-us_chronic_disease_spending_annual}
      - Uncertainty Range
      - Input Distribution
    - US Diabetes Annual Cost: $327B {#sec-us_diabetes_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US GDP (2024): $28.8T {#sec-us_gdp_2024}
      - Uncertainty Range
    - US Govt Spending (% GDP): 3800% {#sec-us_govt_spending_pct_gdp}
      - Uncertainty Range
    - US Heart Disease Annual Cost: $363B {#sec-us_heart_disease_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy (1880): 39.4 years {#sec-us_life_expectancy_1880}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy (1962): 70.1 years {#sec-us_life_expectancy_1962}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy (2019): 78.9 years {#sec-us_life_expectancy_2019}
      - Uncertainty Range
      - Input Distribution
    - US Life Expectancy: 77.5 years {#sec-us_life_expectancy_2023}
      - Uncertainty Range
    - US Median Household Income: $80.6K {#sec-us_median_household_income_2023}
      - Uncertainty Range
    - US Mental Health Costs: $350B {#sec-us_mental_health_cost_annual}
      - Uncertainty Range
      - Input Distribution
    - US Military Spending as Percentage of GDP: 3.5% {#sec-us_military_spending_pct_gdp}
    - US Population in 2024: 335M people {#sec-us_population_2024}
      - Uncertainty Range
      - Input Distribution
    - Senators for Treaty Ratification: 67 senators {#sec-us_senators_for_treaty}
      - Uncertainty Range
    - US Federal Campaign Spending (2024): $20B {#sec-us_total_federal_campaign_spending_2024}
    - US Total Lobbying (2024): $4.40B {#sec-us_total_lobbying_annual}
    - Valley of Death Attrition Rate: 40% {#sec-valley_of_death_attrition_pct}
      - Uncertainty Range
      - Input Distribution
    - Value of Statistical Life: $10M {#sec-value_of_statistical_life}
      - Uncertainty Range
      - Input Distribution
    - Vitamin A Supplementation Cost per DALY: $37 {#sec-vitamin_a_cost_per_daly}
    - Estimated Annual Global Economic Benefit from Water Fluoridation Programs: $800M {#sec-water_fluoridation_annual_benefit}
    - Return on Investment from Water Fluoridation Programs: 23:1 {#sec-water_fluoridation_roi}
    - Cost-Effectiveness Threshold ($50,000/QALY): $50K {#sec-who_qaly_threshold_cost_effective}
    - Percentage of Workforce Experiencing Productivity Loss from Chronic Illness: 28% {#sec-workforce_with_productivity_loss}
  - Core Definitions {#sec-definitions}
    - ADAPTABLE Trial Patients Enrolled: 15.1k patients {#sec-adaptable_trial_patients}
    - Approved Drug-Disease Pairings: 1.75k pairings {#sec-approved_drug_disease_pairings}
      - Uncertainty Range
      - Input Distribution
    - Average Life Extension per Beneficiary: 12 years {#sec-avg_life_extension_per_beneficiary}
      - Uncertainty Range
      - Input Distribution
    - Overlap Discount Factor: 0.85:1 {#sec-bad_policy_us_overlap_discount}
      - Uncertainty Range
    - Celebrity and Influencer Endorsements: $15M {#sec-campaign_celebrity_endorsement}
      - Uncertainty Range
      - Input Distribution
    - Community Organizing and Ambassador Program Budget: $30M {#sec-campaign_community_organizing}
      - Uncertainty Range
      - Input Distribution
    - Contingency Fund for Unexpected Costs: $50M {#sec-campaign_contingency}
      - Uncertainty Range
      - Input Distribution
    - Defense Industry Conversion Program: $50M {#sec-campaign_defense_conversion}
      - Uncertainty Range
      - Input Distribution
    - Budget for Co-Opting Defense Industry Lobbyists: $50M {#sec-campaign_defense_lobbyist_budget}
      - Uncertainty Range
      - Input Distribution
    - Healthcare Industry Alignment and Partnerships: $35M {#sec-campaign_healthcare_alignment}
      - Uncertainty Range
      - Input Distribution
    - Campaign Operational Infrastructure: $20M {#sec-campaign_infrastructure}
      - Uncertainty Range
      - Input Distribution
    - AI-Assisted Legal Work Budget: $50M {#sec-campaign_legal_ai_budget}
      - Uncertainty Range
      - Input Distribution
    - Legal Defense Fund: $20M {#sec-campaign_legal_defense}
      - Uncertainty Range
      - Input Distribution
    - Legal Drafting and Compliance Work: $60M {#sec-campaign_legal_work}
      - Uncertainty Range
      - Input Distribution
    - EU Lobbying Campaign Budget: $40M {#sec-campaign_lobbying_eu}
      - Uncertainty Range
      - Input Distribution
    - G20 Countries Lobbying Budget: $35M {#sec-campaign_lobbying_g20_millions}
    - US Lobbying Campaign Budget: $50M {#sec-campaign_lobbying_us}
      - Uncertainty Range
      - Input Distribution
    - Maximum Mass Media Campaign Budget: $1B {#sec-campaign_media_budget_max}
      - Uncertainty Range
      - Input Distribution
    - Minimum Mass Media Campaign Budget: $500M {#sec-campaign_media_budget_min}
      - Uncertainty Range
      - Input Distribution
    - Opposition Research and Rapid Response: $25M {#sec-campaign_opposition_research}
      - Uncertainty Range
      - Input Distribution
    - Phase 1 Campaign Budget: $200M {#sec-campaign_phase1_budget}
      - Uncertainty Range
      - Input Distribution
    - Phase 2 Campaign Budget: $500M {#sec-campaign_phase2_budget}
      - Uncertainty Range
      - Input Distribution
    - Pilot Program Testing in Small Countries: $30M {#sec-campaign_pilot_programs}
      - Uncertainty Range
      - Input Distribution
    - Voting Platform and Technology Development: $35M {#sec-campaign_platform_development}
      - Uncertainty Range
      - Input Distribution
    - Regulatory Compliance and Navigation: $20M {#sec-campaign_regulatory_navigation}
      - Uncertainty Range
      - Input Distribution
    - Scaling Preparation and Blueprints: $30M {#sec-campaign_scaling_prep}
      - Uncertainty Range
      - Input Distribution
    - Campaign Core Team Staff Budget: $40M {#sec-campaign_staff_budget}
      - Uncertainty Range
      - Input Distribution
    - Super PAC Campaign Expenditures: $30M {#sec-campaign_super_pac_budget}
      - Uncertainty Range
      - Input Distribution
    - Tech Industry Partnerships and Infrastructure: $25M {#sec-campaign_tech_partnerships}
      - Uncertainty Range
      - Input Distribution
    - Post-Victory Treaty Implementation Support: $40M {#sec-campaign_treaty_implementation}
      - Uncertainty Range
      - Input Distribution
    - Viral Marketing Content Creation Budget: $40M {#sec-campaign_viral_content_budget}
      - Uncertainty Range
      - Input Distribution
    - Annual Cost of Unpaid Caregiving: $6K {#sec-caregiver_cost_annual}
    - Cell Therapy Approaches: 500 approaches {#sec-cell_therapy_approaches}
      - Uncertainty Range
      - Input Distribution
    - Childhood Vaccination Cost per DALY (Estimated): $30 {#sec-childhood_vaccination_cost_per_daly}
    - Concentrated Interest Sector Market Cap: $5T {#sec-concentrated_interest_sector_market_cap_usd}
    - Days Per Year: 365 {#sec-days_per_year}
    - Mid-Range Funding for Commercial Dct Platform: $500M {#sec-dct_platform_funding_medium}
    - Percentage of Budget Defense Sector Keeps Under 1% treaty: 99% {#sec-defense_sector_retention_pct}
    - Years to Reach Full Decentralized Framework for Drug Assessment Adoption: 5 years {#sec-dfda_npv_adoption_ramp_years}
    - Decentralized Framework for Drug Assessment Core framework Annual OPEX: $18.9M {#sec-dfda_npv_annual_opex}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Core framework Build Cost: $40M {#sec-dfda_npv_upfront_cost}
      - Uncertainty Range
      - Input Distribution
    - Stage 1 Observational Analysis Cost per Patient: $0.100 {#sec-dfda_observational_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Community Support Costs: $2M {#sec-dfda_opex_community}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Infrastructure Costs: $8M {#sec-dfda_opex_infrastructure}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Maintenance Costs: $15M {#sec-dfda_opex_platform_maintenance}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Regulatory Coordination Costs: $5M {#sec-dfda_opex_regulatory}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Staff Costs: $10M {#sec-dfda_opex_staff}
      - Uncertainty Range
      - Input Distribution
    - Backup/Redundancy Cost per Patient (Monthly): $0.200 {#sec-dfda_storage_cost_backup_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Compute/API Cost per Patient (Monthly): $0.200 {#sec-dfda_storage_cost_compute_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Database Cost per Patient (Monthly): $0.300 {#sec-dfda_storage_cost_database_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Raw Storage Cost per Patient (Monthly): $0.020 {#sec-dfda_storage_cost_raw_per_patient_monthly}
      - Uncertainty Range
      - Input Distribution
    - Decentralized Framework for Drug Assessment Target Cost per Patient in USD: $1K {#sec-dfda_target_cost_per_patient_usd}
    - Decentralized Framework for Drug Assessment One-Time Build Cost: $40M {#sec-dfda_upfront_build}
    - Decentralized Framework for Drug Assessment One-Time Build Cost (Maximum): $46M {#sec-dfda_upfront_build_max}
    - DIH Broader Initiatives Annual OPEX: $21.1M {#sec-dih_npv_annual_opex_initiatives}
      - Uncertainty Range
      - Input Distribution
    - DIH Broader Initiatives Upfront Cost: $230M {#sec-dih_npv_upfront_cost_initiatives}
      - Uncertainty Range
      - Input Distribution
    - Percentage of Caregiving for Treatable Disease Conditions: 40% {#sec-disease_related_caregiver_pct}
    - Epigenetic Drug Targets: 1.50k targets {#sec-epigenetic_targets_count}
      - Uncertainty Range
      - Input Distribution
    - Eventually Avoidable DALY Percentage: 92.6% {#sec-eventually_avoidable_daly_pct}
      - Uncertainty Range
      - Input Distribution
    - Eventually Avoidable Death Percentage: 92.6% {#sec-eventually_avoidable_death_pct}
      - Uncertainty Range
      - Input Distribution
    - Minimum Investment for Family Offices: $5M {#sec-family_office_investment_min}
    - Fundamentally Unavoidable Death Percentage: 7.37% {#sec-fundamentally_unavoidable_death_pct}
    - Global Political Reform Investment: $125B {#sec-global_political_reform_investment}
      - Uncertainty Range
      - Input Distribution
    - Global Political Reform Investment (Maximum): $200B {#sec-global_political_reform_investment_maximum}
    - Hours Per Day: 24 {#sec-hours_per_day}
    - Hours Per Year: 8.76k {#sec-hours_per_year}
    - Human Protein-Coding Genes: 20.0k genes {#sec-human_protein_coding_genes}
      - Uncertainty Range
      - Input Distribution
    - IAB Mechanism Annual Cost (High Estimate): $750M {#sec-iab_mechanism_annual_cost}
      - Uncertainty Range
      - Input Distribution
    - IAB Political Incentive Funding Percentage: 10% {#sec-iab_political_incentive_funding_pct}
      - Uncertainty Range
    - Minimum Investment for Institutional Investors: $10M {#sec-institutional_investor_min}
    - Maximum Bond Investment for Lobbyist Incentives: $20M {#sec-lobbyist_bond_investment_max}
    - Minutes Per Hour: 60 {#sec-minutes_per_hour}
    - Months Per Year: 12 {#sec-months_per_year}
    - NATO Political Reform Investment: $65B {#sec-nato_political_reform_investment}
    - Standard Discount Rate for NPV Analysis: 3% {#sec-npv_discount_rate_standard}
      - Uncertainty Range
    - Standard Time Horizon for NPV Analysis: 10 years {#sec-npv_time_horizon_years}
      - Uncertainty Range
    - Peace Dividend Conflict Elasticity: 1:1 {#sec-peace_dividend_conflict_elasticity}
      - Uncertainty Range
      - Input Distribution
    - Direct Fiscal Savings from 1% Military Spending Reduction: $27.2B {#sec-peace_dividend_direct_fiscal_savings}
    - Pharma Phase 2/3 Cost Barrier Per Drug: $1.56B {#sec-pharma_phase_2_3_cost_barrier}
      - Uncertainty Range
      - Input Distribution
    - Pre-1962 Validation Years: 77 years {#sec-pre_1962_validation_years}
    - QALYs per COVID Death Averted: 5 QALYs/death {#sec-qalys_per_covid_death_averted}
      - Uncertainty Range
      - Input Distribution
    - Safe Compounds Available for Testing: 9.50k compounds {#sec-safe_compounds_count}
      - Uncertainty Range
      - Input Distribution
    - Seconds Per Minute: 60 {#sec-seconds_per_minute}
    - Seconds Per Year: 31.5M {#sec-seconds_per_year}
    - Tested Drug-Disease Relationships: 32.5k relationships {#sec-tested_relationships_estimate}
      - Uncertainty Range
      - Input Distribution
    - Political Lobbying Campaign: Direct Lobbying, Super Pacs, Opposition Research, Staff, Legal/Compliance: $650M {#sec-treaty_campaign_budget_lobbying}
      - Uncertainty Range
      - Input Distribution
    - Reserve Fund / Contingency Buffer: $100M {#sec-treaty_campaign_budget_reserve}
      - Uncertainty Range
      - Input Distribution
    - Campaign Budget for Super Pacs and Political Lobbying: $800M {#sec-treaty_campaign_budget_super_pacs}
    - Treaty Campaign Duration: 4 years {#sec-treaty_campaign_duration_years}
      - Uncertainty Range
      - Input Distribution
    - Viral Referendum Budget: $250M {#sec-treaty_campaign_viral_referendum_base_case}
      - Uncertainty Range
      - Input Distribution
    - Infinite ROI from Redirected Spending: 0:1 {#sec-treaty_redirected_spending_infinite_roi}
    - 1% Reduction in Military Spending/War Costs from Treaty: 1% {#sec-treaty_reduction_pct}
      - Uncertainty Range
    - Trial-Relevant Diseases: 1.00k diseases {#sec-trial_relevant_diseases_count}
      - Uncertainty Range
      - Input Distribution
    - US Congress Members: 535 members {#sec-us_congress_member_count}
      - Uncertainty Range
    - US Dysfunction Premium vs Switzerland: 300% {#sec-us_dysfunction_premium_vs_switzerland}
      - Uncertainty Range
    - US Political Reform Investment (Total): $25B {#sec-us_political_reform_investment_total}
    - US-Singapore Spending Gap: 2300% {#sec-us_vs_singapore_spending_gap}
      - Uncertainty Range
    - Switzerland-US Life Expectancy Gap: 6.5 years {#sec-us_vs_switzerland_life_expectancy_gap}
      - Uncertainty Range
    - US-Switzerland Spending Gap: 300% {#sec-us_vs_switzerland_spending_gap}
      - Uncertainty Range
    - Percentage of Captured Dividend Funding VICTORY Incentive Alignment Bonds: 10% {#sec-victory_bond_funding_pct}
      - Uncertainty Range

#### knowledge/appendix/invisible-graveyard.qmd
**Title:** The Invisible Graveyard: Quantifying the Mortality Cost of FDA Efficacy Lag, 1962-2024
**Description:** The 1962 efficacy requirement adds {{< var efficacy_lag_years >}} to drug approval after safety is proven. This study quantifies two distinct mortality costs: (1) {{< var existing_drugs_efficacy_lag_d...
**Stats:** 6,735 words | 749 lines

  - The Short Version
  - Abstract
  - Scale
  - Introduction
  - Literature Review: The Drug Lag Debate
    - Foundational Economic Analysis
    - The Current Debate
    - Empirical Case Studies: Demonstrating the Causal Mechanism
  - Methodology & Data
    - Variable Definitions {#mortality-estimates}
    - Theoretical Upper Bound: What's Eventually Preventable? {#eventually-preventable}
  - Methodological Note: Distinguishing Current vs. Theoretical Preventability
      - Disease Burden by Category
      - Why This Upper Bound? The Biological and Epidemiological Evidence
      - The {{< var fundamentally_unavoidable_death_pct >}} Floor
    - Data Sources & Parameterization
    - Uncertainty Quantification Methodology
  - Results: The Mortality Burden {#mortality-scenarios}
    - Primary Estimate
  - Methodological Caveat: Cascade Assumption
      - Sensitivity Analysis
  - Morbidity Analysis: DALYs and QALYs {#daly-calculation}
    - Years of Life Lost (YLL)
    - Years Lived with Disability (YLD)
    - Cumulative DALY Burden
    - Years Lived with Disability - Treatment Beneficiaries {#treatment-morbidity}
  - Distinction: Mortality vs. Morbidity Burden
  - Economic Valuation {#economic-valuation}
    - Contextualizing the Loss
  - Risk Analysis: The Type I vs. Type II Ratio {#risk-analysis}
  - Methodological Note: Steelmanning the FDA's Position
    - The Risk Trade-off Ratio
    - Acknowledging the Efficacy-as-Safety Argument
    - Drugs Appropriately Caught by Phase II/III Trials
  - Model Assumptions and Limitations
    - Key Assumptions
    - Sensitivity Analysis
    - Limitations
  - Policy Implications
    - The False Trade-off
    - The Bifurcated Alternative
    - Expected Impact
    - International Regulatory Comparison
  - Critical Distinction: Efficacy Assessment Reordered, Not Eliminated
  - Addressing Common Critiques
    - "The PRIMARY Estimate Is Too Speculative"
    - "The 'Eventually Preventable' Estimate Is Theoretical"
    - "Counterfactual Uncertainty - We Can't Know What Would Have Happened"
      - Natural Experiments
      - The Standard for Causal Inference
    - "Confounding Factors - Other Changes in 1962"
      - Sensitivity Analysis: What if Regulation Explains Only Part of the Decline?
    - "This Ignores Safety - Deregulation Would Flood Markets with Dangerous Drugs"
  - Conclusion

#### knowledge/appendix/drug-development-cost-analysis.qmd
**Title:** Drug Development Cost Increase Analysis
**Description:** Rigorous analysis of the {{< var drug_cost_increase_pre1962_to_current_multiplier >}} increase in drug development costs from pre-1962 to 2024, using Baily (1972) academic study with CPI adjustments a...
**Stats:** 3,237 words | 556 lines

  - Executive Summary
  - Historical Data Sources
    - Pre-1962 Drug Development Costs
    - Current Drug Development Costs
  - Inflation-Adjusted Calculations
    - Primary Method: Baily (1972) Academic Study
    - Alternative Method: Congressional Testimony (1977)
  - Why It's Not Just Inflation
    - 1. Development Timeline Expansion
    - 2. Higher Failure Rates
    - 3. Trial Complexity
    - 4. Preclinical Requirements
  - Sensitivity Analysis
    - Uncertainty Ranges
    - Input Parameter Uncertainty
    - Alternative Scenarios
    - Independent Validation
  - Sanity Checks: Real-World Price Comparisons
    - 1. Generic vs. Brand-Name Drugs (Patent Cliff Evidence)
    - 2. Nutritional Supplements vs. Prescription Drugs (Same Molecule, Different Regulation)
    - 3. Compounding Pharmacies (Custom Manufacturing Without FDA Approval)
    - 4. Veterinary Drugs vs. Human Drugs (Same Molecule, Different Species)
    - 5. Orphan Drugs (Full Development Cost Exposure)
    - 6. Historical Price Trajectory (Penicillin: 1942 vs. 2024)
    - Cross-Validation: All Six Checks Confirm {{< var drug_cost_increase_pre1962_to_current_multiplier >}} Development Cost Increase
  - Addressing Common Objections
    - "That can't be right. It's too high!"
    - "Doesn't that include marketing costs?"
    - "What about technological improvements reducing costs?"
  - Implications for Policy
    - 1. Regulatory Reform Has Massive ROI
    - 2. Pre-1962 System Wasn't Broken
    - 3. Real-World Evidence Can Reverse This
  - Conclusion
  - References
  - Technical Parameters

#### knowledge/appendix/personal-lifetime-wealth-calc.qmd
**Title:** Personal Lifetime Wealth Calculation
**Description:** Simple QALY-based calculation showing personal benefit from 1% treaty life extension
**Stats:** 314 words | 68 lines

  - The Simple Formula
  - Why QALY Valuation?
  - Uncertainty Analysis
    - Input Distribution
    - Output Distribution
    - Sensitivity Analysis
    - Exceedance Probability
  - Bottom Line

#### knowledge/appendix/dfda-impact-paper.qmd
**Title:** The Health and Economic Impact of a Global System for Pragmatic Clinical Trials
**Description:** Economic analysis of a decentralized framework for drug assessment (dFDA). With {{< var dih_treasury_to_medical_research_annual >}}/year in pragmatic trial funding, the framework could save {{< var df...
**Stats:** 11,537 words | 1,219 lines

  - Understanding These Figures: The Untested Treatment Backlog
  - Executive Summary
  - Protocol, Not Platform
    - What You Get
    - Key Findings
  - Vision and Capabilities
    - Core Model: An Open Coordination Protocol
    - Key Capabilities
    - Potential Impact on the Status Quo
  - Addressing Key Concerns
    - Why This Differs from Failed Megaprojects
    - Historical Validation: Pre-1962 Physician-Led Efficacy Testing
    - Why "Eventually Avoidable" Matters
    - Trial Funding Scenario
  - Framework Costs (ROM Estimates) {#dfda-framework-costs-rom-estimates}
    - Upfront Build Costs (30 Months) {#upfront-build-costs}
    - Ecosystem Participants
    - Annual Operational Costs (5M MAU Target Scale) {#annual-operational-costs}
      - Marginal Cost Analysis per User
    - Scenario Based ROM Estimates for Broader Initiative Costs
      - Interpretation
      - Summary
  - Benefit Analysis - Quantifying the Savings
    - Market Size and Impact
    - Decentralized Trial Costs Modeled on Pragmatic Trials
    - Overall Savings
    - Economic Value of Earlier Access to Treatments
    - Gross R&D Savings from Implementing a Decentralized Framework {#gross-r-and-d-savings-from-implementing-a-decentralized-framework}
      - Key Sources
    - Post-Safety Efficacy Lag Elimination {#regulatory-delay-avoidance}
      - The Efficacy Lag Problem
      - How a Decentralized Framework Eliminates the Efficacy Lag
      - Quantified Benefits (One-Time Timeline Shift)
      - Efficacy Lag Elimination - Uncertainty Analysis
    - Safety and Risk Management
      - Current System Limitations: Dangerously Blind to Real-World Harms
      - Proposed System Safety Advantages
      - Detection Timeline Comparison
      - Comparative Safety Surveillance
      - Pooled Liability Insurance
  - ROI Analysis for a Decentralized Framework {#simplified-roi-scenario}
    - Monte Carlo Distributions
  - Research Acceleration Mechanism
    - The Unexplored Therapeutic Frontier
    - Current Exploration Rate vs. Therapeutic Space
    - Addressing the Returns Question: Diminishing, Linear, or Compounding?
      - Why Diminishing Returns Is Unlikely (We Haven't Started Looking)
      - Mathematical Framework: When Would Diminishing Returns Dominate?
      - The Conservative Default: Linear Assumption
  - Data Sources and Methodological Notes
  - Conclusion
    - Disclaimer
  - Verification: Complete Derivation Chains
    - 1. Trial Capacity Multiplier Derivation ({{< var dfda_trial_capacity_multiplier >}})
    - 2. Timeline Shift Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_years >}})
    - 3. Lives Saved Derivation ({{< var dfda_trial_capacity_plus_efficacy_lag_lives_saved >}})
    - 4. Cost per DALY Derivation ({{< var dfda_direct_funding_cost_per_daly >}})
    - 5. ROI Derivation ({{< var dfda_roi_rd_only >}})
    - Verification Summary
  - Key Analytical Assumptions
    - Linear Scaling Assumption
    - Adoption Rate Assumptions
    - Cost Reduction Assumptions
    - Eventually Avoidable Mortality Assumption
    - Counterfactual Baseline Specification
    - Methodology Validation Against Accepted Benchmarks
  - Appendix Calculation Frameworks and Detailed Analysis
    - Calculation Framework - NPV Methodology {#calculation-framework---npv-methodology}
    - Financial Analysis Summary {#financial-analysis-summary}
      - Health Impact Uncertainty Analysis
      - Financial Visualizations
    - Cost-Utility Framework {#dfda-icer-analysis---cost-utility-framework}
      - QALY Benefit Streams Breakdown
      - DALY Sensitivity Analysis
    - Comparative Cost-Effectiveness - A Decentralized Framework vs Other Interventions
    - Methodology Notes
    - Data Limitations
  - Comparison to Other Major Public Investments

#### knowledge/appendix/economic-value-of-accelerated-treatments.qmd
**Title:** Economic Value: Medical Progress
**Description:** Estimates the economic value of new therapies, including their market valuation and potential impact when increasing trial capacity by {{< var dfda_trial_capacity_multiplier >}}×.
**Stats:** 516 words | 66 lines

  - **Introduction**
  - **Average Economic Value of a New Therapy**
  - **Annual Value Based on Average Approvals**
  - **Impact of {{< var dfda_trial_capacity_multiplier >}}× More Trial Capacity**
  - **Considerations and Context**
  - **Conclusion**
  - **Sources**

#### knowledge/appendix/intervention-comparison-table.qmd
**Title:** High-Impact Health Interventions
**Description:** How a dFDA compares to history's best health wins
**Stats:** 486 words | 46 lines

  - Comparison Table
    - Key
  - Conclusion

#### knowledge/appendix/data-storage-costs.qmd
**Title:** Data Storage Costs for Decentralized Clinical Trials
**Description:** Why cloud storage costs less than coffee
**Stats:** 992 words | 151 lines

  - How Much Space One Patient Takes
    - What's Actually Stored
  - Cost Analysis {#cost-analysis}
    - Infrastructure Costs (Per Patient/Month)
    - Stage 1 Observational Analysis Cost
    - Comparable Real-World Systems
    - Consumer Platform Comparisons
    - Why Costs Are Lower Than Traditional Platforms
  - Additional Considerations
    - Fixed Costs
    - Cost Optimization Strategies
    - Scaling Benefits
  - Methodology and Limitations
    - True Cost by Scale
  - Conclusion

### Financial Planning

#### knowledge/economics/financial-plan.qmd
**Title:** Financial Plan: Overview
**Description:** High-level overview of how to fund, spend, and manage the financial flows required to pass a 1% treaty and operate the 1% Treaty Fund.
**Stats:** 1,547 words | 222 lines

  - The Three Financial Pillars
    - Fundraising: How To Raise {{< var treaty_campaign_total_cost >}}
      - Why This Works
    - Campaign Budget: How To Spend {{< var treaty_campaign_total_cost >}}
      - Key Innovations
    - Treasury Management: How To Manage {{< var treaty_annual_funding >}}+ Annually
      - Revenue Sources
      - Growth Scenarios (Not Predictions)
      - Expenditure Allocation
      - The Fixed Costs ({{< var victory_bond_funding_pct >}} + {{< var iab_political_incentive_funding_pct >}} = 20%)
        - Everything Else ({{< var dih_treasury_medical_research_pct >}}): Decided by Wishocracy
      - Anti-Corruption Architecture
      - Dynamic Patient Subsidies
      - How It Works
      - Why This Creates Perfect Incentives
      - Compare to Grant System
  - Risk Management
  - Related Documents
  - Summary

#### knowledge/economics/campaign-budget.qmd
**Title:** Campaign Budget: The {{< var campaign_media_budget_max >}} Legal Bribery Machine
**Stats:** 2,721 words | 417 lines

  - Why {{< var treaty_campaign_total_cost >}} Instead of $5B {#ai-assisted-lobbying-250m-25}
    - The Minimum Viable Budget
  - Where the Papers Go
    - Viral Referendum (part of {{< var treaty_campaign_viral_referendum_base_case >}} Referendum Budget)
      - Paying Humans to Click
      - Payment structure
      - Budget: Viral Referendum with Tiered Incentives {#base-case-scenario}
    - Professional (Legal) Bribery (part of {{< var treaty_campaign_budget_lobbying >}} Lobbying Budget)
    - Technology (part of {{< var treaty_campaign_viral_referendum_base_case >}} Referendum Budget)
    - Lawyers (AI-Assisted) (part of {{< var treaty_campaign_budget_lobbying >}} Lobbying Budget)
    - Co-opting the Opposition (part of {{< var treaty_campaign_budget_lobbying >}} Lobbying Budget)
    - Operations (overhead across all categories)
    - Post-Victory Transition: {{< var treaty_campaign_budget_reserve >}}
  - Timeline
  - Why This Works
  - Returns
  - Transparency
  - Adaptive Management
  - Summary

#### knowledge/appendix/investor-risk-analysis.qmd
**Title:** Investor Risk Analysis
**Description:** VICTORY Incentive Alignment Bonds vs. Traditional Venture Capital - Analysis of the unique risk profile of a 1% treaty initiative, comparing its political arbitrage model to the market-risk model of v...
**Stats:** 975 words | 79 lines

  - 1. The Core Thesis: Political Arbitrage vs. Venture Capital
  - 2. Comparative Risk Factor Analysis
  - 3. Engineered Risk Mitigation Mechanisms
    - A. The Assurance Contract (Mitigates **Fundraising Risk**)
      - B. Metaculus & Dynamic Pricing (Mitigates **Political Risk**)
      - C. Front-Loaded Payouts (Mitigates **Timeline Risk**)
      - D. First-Loss Capital (Mitigates **Financial Risk**)
  - Conclusion: Is It Less Risky Than a VC Investment?

#### knowledge/appendix/fundraising-strategy.qmd
**Title:** Fundraising Strategy
**Description:** The {{< var treaty_campaign_total_cost >}} Activation Energy - Comprehensive strategy for raising {{< var treaty_campaign_total_cost >}} through multi-phase approach targeting crypto whales, health bi...
**Stats:** 5,739 words | 862 lines

  - Fundraising Strategy: The {{< var treaty_campaign_total_cost >}} Activation Energy
    - On How to Raise {{< var treaty_campaign_total_cost >}} to Unlock {{< var treaty_annual_funding >}}/Year Forever
    - Multi-Phase Strategy
      - Phase 1: Seed Round ($250M - $400M)
      - Phase 2: Series A ($500M - $1B)
      - Phase 3: Growth Round ($500M - $1.1B)
    - Key Innovation: Nobody Gets Paid Unless It Works
    - Capital Structure: Campaign vs Implementation {#capital-structure-campaign-vs-implementation}
      - Why {{< var treaty_campaign_total_cost >}}?
      - Campaign Budget Breakdown
      - Why VICTORY [Incentive Alignment Bonds](https://iab.warondisease.org) (Not Donations)?
      - Why This Works
      - Post-Treaty Implementation ({{< var treaty_annual_funding >}}/year)
      - Legal Structure: Two Separate Entities
        - Entity 1: Nonprofit Foundation (501c3)
          - Entity 2: For-Profit Political Campaign
      - Nonprofit Compliance Checklist
    - Funding Model Comparison: What Actually Works
      - Historical Evidence: How Similar Campaigns Were Funded
      - Model A: Traditional Foundation Grants ($442M)
        - How it would work
        - Evidence
        - Pros
        - Cons
      - Model B: VICTORY [Incentive Alignment Bonds](https://iab.warondisease.org) (Traditional Securities) ($500M-$1B)
        - How it would work
        - Evidence
        - Pros
        - Cons
      - Model C: Security Token Offering / Crypto ($100M-$500M)
        - How it would work
        - Evidence
        - Pros
        - Cons
      - Model D: Litigation Finance / Contingency Model ($0 upfront)
        - How it would work
        - Evidence
        - Pros
        - Cons
      - Model E: Defense Contractor Conversion (Most Realistic?)
        - How it would work
        - Evidence
        - Calculation
        - Pros
        - Cons
      - Model F: Phased Hybrid Approach (Evidence-Based)
        - Based on what actually worked historically
          - Phase 1: Pilot ($10-20M, Years 1-2)
          - Phase 2: Campaign ($100-200M, Years 3-5)
          - Phase 3: Implementation ({{< var treaty_annual_funding >}}/year, Year 6+)
      - Recommended Strategy: Defense Contractor Pivot + Phased VICTORY Incentive Alignment Bonds
        - Year 1-2: Seed ($10-20M)
          - Year 3-4: Series A ($50-100M)
          - Year 5-6: Series B ($100-200M)
          - Year 7+: Implementation
        - Why this works
      - The Virtuous Cycle: Votes Drive Bond Sales
        - The Cycle
          - Why only bonds (not donations)?
        - Timeline milestones
    - Hybrid Communication Strategy: Simple Targets, Sophisticated Mechanics
      - The Marketing Message (The "Hook")
      - The Backend Engine (Market-Driven Pricing)
    - De-Risking with Assurance Contracts
    - Whale & Billionaire Targeting Strategy
      - Why Target Whales
        - Speed vs. Scale Trade-off
        - Unit Economics Advantage
    - Target Categories & Prospects
      - Category 1: Crypto Whales & Protocol Treasuries ($500M-1B potential)
        - Individual Crypto Billionaires
        - Protocol Treasuries (DAO-to-DAO)
      - Category 2: Health & Pharma Billionaires ($750M-1.5B potential)
        - Pharma Executives
        - Health Tech Billionaires
      - Category 3: Mission-Aligned Mega-Foundations ($500M-1B potential)
        - Health-Focused Foundations
        - Effective Altruism & Longevity
    - Outreach Templates
      - Template 1: Crypto Whales (Governance Angle)
      - Template 2: Health Billionaires (Industry Advantage)
      - Template 3: Foundations (Mission Multiplication)
    - Detailed Budget Breakdown
      - Phase 1: Seed ($250M - $400M)
      - Phase 2: Series A ($500M - $1B)
      - Phase 3: Growth Round ($500M - $1.1B)
    - Bottom-Up Budget Justification
      - Operations Budget
      - Platform Development
      - Legal & Policy Engagement
      - Public Engagement & Policy Education Initiatives
    - Legal Structures for Large Investments
      - Option 1: SAFT (Simple Agreement for Future Tokens)
      - Option 2: Convertible Note
      - Option 3: Series Seed Equity
      - Option 4: Revenue Share Agreement
    - Execution Timeline
      - Month 1-2: List Building & Warm Intros
      - Month 3-4: Direct Outreach Wave 1 (Top 25 targets)
      - Month 5-6: Closing Wave 1 ($150-300M)
      - Month 7-9: Outreach Wave 2 (Next 50 targets)
      - Month 10-12: Closing Wave 2 ($400M-1B)
    - Success Metrics
    - Risk Mitigation
      - Regulatory Risk
      - Market Risk
      - Execution Risk
    - The Economic Reality

### Governance & Organization

#### knowledge/appendix/governance.qmd
**Title:** Governance
**Description:** Governance architecture for the Decentralized Institutes of Health, including anti-capture mechanisms and security design.
**Stats:** 110 words | 29 lines

  - Content Moved

#### knowledge/appendix/organizational-precedents.qmd
**Title:** Organizational Precedents & Staffing Models
**Description:** An analysis of the organizational structures and staffing models of key precedents, The Global Fund, the ICBL, and MakerDAO, to inform the DIH's own team structure.
**Stats:** 846 words | 98 lines

  - Precedent: The Global Fund (The Financial Institution)
    - Illustrative Org Chart & Key Roles
  - Precedent: The ICBL (The Political Campaign)
    - Illustrative Org Chart & Key Roles
  - Precedent: MakerDAO (The Decentralized Protocol)
    - Illustrative "Org Chart" (Core Units)

#### knowledge/operations/careers/hiring-plan.qmd
**Title:** Hiring Plan & Team Roadmap
**Description:** Phase-based hiring plan for core team structure and scaling strategy to execute a 1% treaty and launch the DIH.
**Stats:** 1,039 words | 106 lines

    - The Philosophy: A Lean Activation Team
    - Compensation Philosophy
    - Phase 1: Seed (Core Team Headcount: ~20)
      - Leadership & Operations (5 Roles)
        - Product, Design, & Community (3 Roles)
          - Political & Growth (4 Roles)
          - Platform & Technology (7 Roles)
          - Finance & Economics (4 Roles)
    - Phase 2: Series A (Scaled Team Headcount: ~50)
      - New Roles to be Hired
    - Phase 3: Growth (Full Team Headcount: ~75-100)
      - New Roles to be Hired

#### knowledge/appendix/dih-integration-model.qmd
**Title:** DIH Healthcare Integration Model
**Description:** How the DIH functions as an insurance-like layer that seamlessly integrates with existing healthcare infrastructure
**Stats:** 698 words | 193 lines

  - 5. Why This Works Better Than Direct Payments
    - Avoids Perverse Incentives
    - Reduces Friction
    - Ensures Quality
  - Real-World Example
    - Sarah has Type 2 Diabetes
      - Old System
      - With a decentralized institutes of health integration
  - Implementation Requirements
    - Technical Infrastructure
    - Regulatory Framework
    - Who Gets What
  - Cost Structure (Realistic Numbers)
    - Per Patient Per Trial
      - Efficiency gain: 75-80% cost reduction
  - Why Doctors Will Love This
  - Why Patients Will Use This
  - The Transition Plan
    - Phase 1: Pilot Programs (Year 1)
      - Phase 2: Regional Rollout (Year 2)
        - Phase 3: National Scale (Year 3+)
  - Integration Strategy

#### knowledge/appendix/open-ecosystem-and-bounty-model.qmd
**Title:** How to Not Build Most of It
**Description:** A dFDA strategy for getting other people to build everything through open APIs and bounties, like WordPress but for not dying.
**Stats:** 1,012 words | 190 lines

  - The Core Strategy (How WordPress Beat Expensive Software)
    - The Model
    - Why This Works (Evidence Not Theory)
      - WordPress
      - Linux
      - Browser Extensions
    - Why Humans Do This For Free
  - Bounties and Prizes (Paying for Results Not Promises)
    - What Bounties Fund
    - The Difference
  - Why This Actually Works (Not Wishful Thinking)
    - 1. It's Already a Multi-Trillion-Dollar Reality
    - 2. AI Makes Building Software Radically Cheaper
    - 3. Governments Already Do This (And It Works)
  - What Has to Go Right (Success Factors)
    - 1. Critical Mass
    - 2. API Quality and Documentation
    - 3. Transparent Governance
    - 4. Clear Roadmap
  - The Result

#### knowledge/appendix/command-and-control-systems.qmd
**Title:** Command & Control Systems
**Description:** How to build a database that runs a global war (without becoming the Pentagon)
**Stats:** 2,341 words | 367 lines

  - The Architecture: Military Organization Without the Military
  - SECTION 1: G-1 (Personnel Command)
    - Table 1: `Personnel Roster` (The Master List of Who's Not Dead Yet)
      - Fields that matter
    - Table 2: `Engagements` (The Stalker's Dream Log)
      - What you track
    - Table 3: `HR & Recruitment` (Finding People Who Don't Suck)
      - The hiring pipeline
  - SECTION 2: G-2 & G-3 (Operations & Intelligence)
    - Table 4: `Organizations` (The Other Players in This Game)
      - The institutional roster
    - Table 5: `Divisions` (Your Internal Departments)
      - Your command structure
    - Table 6: `Projects & Tasks` (The Actual Work)
      - Project management for revolutionaries
  - SECTION 3: G-4 & G-5 (Strategy & Logistics)
    - Table 7: `Treasury (Financials)` (Where the Money Goes to Die)
      - The money trail
    - Table 8: `Campaigns` (The Grand Strategies)
      - Strategic initiative tracking
  - SECTION 4: G-6 (Signal & Communications)
    - Table 9: `Communiqués` (Your Propaganda Machine)
      - Message management
    - Table 10: `Media Assets` (The Propaganda Library)
      - Creative arsenal
  - SECTION 5: MISSION COMMAND (The Money Makers)
    - Table 11: `VICTORY Incentive Alignment Bonds` (The Get-Rich-Quick Scheme That's Actually Legal)
      - Investment tracking
    - Table 12: `Global Referendum` (The Democratic Facade)
      - Democracy theater
    - Table 13: `Treaty Status` (The Political Battlefield)
      - Diplomatic scorecard
  - How to Actually Build This Thing
  - The Privacy Paradox
  - The Result

### Operations & Legal

#### knowledge/appendix/recruitment-and-propaganda-plan.qmd
**Title:** Recruitment & Propaganda Plan
**Description:** How to build an army of people who don't want to die (surprisingly difficult)
**Stats:** 1,806 words | 320 lines

  - The Current Clusterfuck
  - The Three-Division Army Structure
    - Division 1: Financial Infantry (The Money People)
      - How to identify them
    - Division 2: Home Front Supporters (The Feels People)
      - How to identify them
    - Division 3: Allied Command (The Institution People)
      - How to identify them
  - The Enlistment Forms
    - Financial Infantry Enlistment Form
    - Home Front Supporter Enlistment Form
    - Allied Command Partnership Form
  - The Deployment Strategy
    - Step 1: Delete the Impossible Buttons
    - Step 2: Install the New Propaganda
    - Step 3: Create Artificial Urgency
    - Step 4: A/B Test Everything
  - The Management Protocol
    - Weekly Reviews (Monday Morning Triage)
    - Tagging System (How to Remember Who Matters)
    - Follow-Up Sequences (Automated Harassment)
  - The Communication Strategy
  - The Privacy Theater
  - The Metrics That Matter
  - The Endgame
  - Your Marching Orders

### Additional References

#### knowledge/papers.qmd
**Title:** Papers & Publications
**Description:** Academic papers and working drafts from the Disease Eradication Plan project.
**Stats:** 917 words | 106 lines

- Papers & Publications
  - Books
    - [The 1% Treaty: Health and Economic Impact of Redirecting 1% of Global Military Spending to Pragmatic Clinical Trials](https://impact.warondisease.org)
  - Working Papers
    - [Federal Resource Allocation Efficiency Audit](https://federal-efficiency-audit.warondisease.org)
    - [Incentive Alignment Bonds: Making Public Goods Financially and Politically Profitable](https://iab.warondisease.org)
    - [Optimal Budget Generator: Evidence-Based Budget Allocation Framework](https://obg.warondisease.org)
    - [Optimal Policy Generator: Evidence-Based Policy Recommendations for Jurisdictions](https://opg.warondisease.org)
    - [Optimocracy: Evidence-Based Governance Through Outcome-Bound Optimization](https://optimocracy.warondisease.org)
    - [The Health and Economic Impact of a Global System for Pragmatic Clinical Trials](https://impact.dfda.earth)
    - [The Invisible Graveyard: Quantifying the Mortality Cost of FDA Efficacy Lag, 1962-2024](https://invisible-graveyard.warondisease.org)
    - [The Political Dysfunction Tax](https://political-dysfunction-tax.warondisease.org)
    - [The Price of Political Change: A Cost-Benefit Framework for Policy Incentivization](https://cost-of-change.warondisease.org)
    - [Wishocracy: Solving the Democratic Principal-Agent Problem Through Pairwise Preference Aggregation](https://wishocracy.warondisease.org)
    - [dFDA: A Decentralized Framework for Drug Assessment Using Two-Stage Real-World Evidence Validation](https://dfda-spec.warondisease.org)

#### knowledge/appendix/lives-saved-by-drug-accessibility.qmd
**Title:** Estimated Lives Saved by Increased Drug Accessibility
**Description:** Table estimating the number of lives that could be saved annually by increasing accessibility to certain drugs
**Stats:** 644 words | 77 lines

  - **Notes on Estimates:**
  - **Additional Sources:**

#### knowledge/appendix/nuclear-weapon-cost-and-casualties.qmd
**Title:** The Cost of a Nuclear Bomb vs. The Cost of a Human Life
**Description:** A quantitative analysis of the cost per death for a modern nuclear weapon, and the potential human cost of a $2.69 trillion military budget.
**Stats:** 1,113 words | 204 lines

  - On The Price of a City-Destroying Weapon
  - On How Many People One Bomb Kills
    - The Simulation
  - On The Math That Makes You Uncomfortable
    - Translation
  - On What Happens After We Give 1% to Pragmatic Clinical Trials
    - Step 1: How many bombs?
      - Step 2: How many deaths?
      - Translation
        - Overkill capacity: 20× Earth's population
          - Twenty times.
  - On The Summary (In Case You Skipped The Math)
    - What Nuclear Weapons Cost
      - What A 1% treaty Changes
  - On Comparing Different Ways to Kill People (The Efficiency Rankings)
    - Small Arms (Rifles/Machine Guns)
    - Artillery (155mm Howitzer Shells)
    - Precision-Guided Munitions
      - Excalibur GPS-Guided Artillery
      - Air-Launched Missiles
    - Nuclear Weapons (The Winner)
    - The Leaderboard (Most to Least "Efficient")
      - The Math That Proves We're Insane
      - The Point

#### knowledge/appendix/pragmatic-vs-explanatory-trials.qmd
**Title:** Pragmatic vs Explanatory Trials: A Quantitative Analysis
**Description:** A comparison of pragmatic and explanatory trials focusing on cost, time, and real-world applicability.
**Stats:** 581 words | 125 lines

  - Key Differences at a Glance
  - Cost Analysis
    - Traditional Explanatory Trials
    - Pragmatic Trials (RECOVERY & Broader Evidence)
  - Speed and Efficiency
    - RECOVERY Trial Metrics
    - Traditional Trial Metrics
  - Clinical Impact
    - RECOVERY Trial
    - Traditional Trials
  - Advantages of Pragmatic Trials

#### knowledge/appendix/acknowledgments.qmd
**Title:** Acknowledgments
**Stats:** 316 words | 46 lines

    - Technical Contributors
    - On Standing on Shoulders

#### knowledge/references.qmd
**Title:** Source Quotes and References
**Description:** Bibliography and citations for all sources cited
**Stats:** 62 words | 22 lines

#### index-manual.qmd
**Title:** How to End War and Disease
**Stats:** 7,240 words | 790 lines

    - The Part Where I Discover Paper Makes You Do Things
    - The Gradual Stupidity Reduction Program
    - The Sacred Order of Paper Distribution
    - Why Your Leaders Pretend Not to Understand
    - The Beautiful Inefficiency of the Human Economy
    - Humanity's Adorable Death Wish
    - How This Manual Could Fix Everything
    - The Part Where Humanity Has No Choice
    - Your Two Futures
      - Future A: You Ignore This Book
      - Future B: You Follow Instructions
    - In Conclusion
  - ⚡ TL;DR
    - How You Fix This
      - Step 1: The Paper Collection Phase
      - Step 2: The Internet Clicking Ceremony
      - Step 3: The Professional Briber Redistribution
      - Step 4: The Political Awakening Ritual
      - Step 5: The Money River Redirection
    - Personalized Bribery Packages
    - The Alternative
  - The Problem
    - The Daily Deletion Event
    - The Disease Queue (Why You're Waiting to Not Die)
    - The Cost of War
    - Hilarious Security Priorities
  - The Solution
    - A 1% treaty
    - Why Decentralization Works
    - The 1% Treaty Fund
    - A Decentralized Framework for Drug Assessment (dFDA)
  - Why This Could Actually Work
    - The Evidence
  - The 5-Step Plan
    - Step 1: Collect Papers
      - What Grandma Got
      - What You're Offering
      - Potential Returns That Make Ponzi Schemes Look Conservative
    - Step 2: The Great Clicking
      - The Magic 3.5% Number
    - Step 3: Bribe the Bribers
      - Current Job
      - Your Offer
    - Step 4: Purchase Democracy
      - Incentive Alignment Bonds
    - Step 5: Enjoy
  - The Math
    - The Money Fountain
    - Where Math Breaks
      - The Reality-Breaking Equation
      - Where {{< var combined_peace_health_dividends_annual_for_roi_calc >}} Appears From
    - 2nd Best Idea in the World
  - Choose Your Own Adventure
    - Door #1: The Current Plan
    - Door #2: Try Not Dying
  - Price of Procrastination
    - The Final Math
      - Your Binary Choice Matrix

---

## _quarto-obg.yml
**Title:** Optimal Budget Generator: Evidence-Based Budget Allocation Framework
**Type:** website
**Files:** 1 | **Words:** 8,967

#### knowledge/appendix/optimal-budget-generator-spec.qmd
**Title:** Optimal Budget Generator: Evidence-Based Budget Allocation Framework
**Description:** The Optimal Budget Generator (OBG) answers: 'How should we allocate the budget to maximize welfare?' Unlike isolated spending targets, OBG generates integrated budget recommendations that account for ...
**Stats:** 8,967 words | 1,355 lines

  - Abstract {.unnumbered}
  - System Overview {#obg-system-overview}
    - What Policymakers See
  - Example: US Federal Budget Gap Analysis
    - What Budget Analysts See
    - Where This Fits
  - Introduction
    - Why Budget Allocation Fails Today
    - The RDA Analogy: Optimal Levels, Not Just Marginal Returns
    - What This Framework Provides
  - Related Work
    - Budget Analysis Frameworks
    - Evidence-Based Policy Movement
    - Comparative Public Finance
    - How OBG Differs
  - Theoretical Framework
    - The Social Planner's Problem
    - Optimal Spending Levels Under Uncertainty
    - Budget Impact Score as Precision Weighting
    - Gap Analysis and Welfare Gains
    - Welfare Bounds Under Model Uncertainty
    - Summary of Theoretical Results
  - Core Methodology
    - Spending Category Data Structure
    - Three Methods for OBG Estimation
  - Reference Country Benchmarking
    - The Basic Approach
    - Reference Country Selection Criteria
    - Worked Example: Early Childhood Education
    - Limitations of Reference Benchmarking
  - Diminishing Returns Modeling
    - The Core Concept
    - Finding the "Knee" of the Curve
    - Estimation Methods
    - Worked Example: K-12 Education Spending
  - Worked Example: Pragmatic Clinical Trials
    - The Highest-Return Public Investment
    - Reference Country Benchmarking
    - Diminishing Returns Analysis
    - Cost-Effectiveness Calculation
    - Gap Analysis
    - Why This Category Dominates
  - Cost-Effectiveness Threshold Analysis
    - The Standard Health Economics Approach
    - Building Up from Intervention-Level Data
    - Worked Example: Vaccinations
  - Budget Impact Score (BIS) as Evidence Quality
    - Reframing BIS: Confidence in OSL, Not Allocation Driver
    - BIS Calculation
    - Evidence Grading from BIS
    - BIS Does Not Drive Allocation
  - Gap Analysis and Priority Ranking
    - Computing Gaps
    - Priority Score
    - Worked Example: Priority Ranking
  - Multi-Unit Reporting
    - The Problem with Abstract Scores
    - Reporting at Multiple Levels
    - Conversion Factors
    - Worked Example: Multi-Unit Output
  - Quality Requirements and Validation
    - Minimum Thresholds for OBG Estimation
    - Robustness Checks
  - Interpreting Results
    - Gap Ranges and Recommended Actions
    - What the Algorithm Cannot Tell You
  - Pilot Program Prioritization
    - Value of Information for Uncertain Categories
    - Recommended Pilot Designs
    - Learning Feedback Loop
  - Data Sources
    - Reference Country Databases
    - Cost-Effectiveness Databases
    - US Budget Data
  - Limitations
    - Reference Country Selection Bias
    - Diminishing Returns Uncertainty
    - Political Feasibility Not Modeled
    - Implementation Capacity
  - Validation Framework
    - Retrospective Validation
    - Prospective Validation
    - Success Metrics
    - Validation Status
  - Sensitivity Analysis
    - Parameter Sensitivity
    - Scenario Analysis
  - Future Directions
    - Methodological
    - Data Infrastructure
    - Governance Integration
  - Conclusion
  - Acknowledgments {.unnumbered}
  - References
  - Appendix A: Worked Example - Complete OBG Calculation {.appendix}
    - Example: US Military Discretionary Spending
  - Appendix B: Analysis Workflow {.appendix}
    - Complete OBG Analysis Pipeline
  - Appendix C: Glossary {.appendix}
    - Core Concepts
    - Estimation Methods
    - Evidence Quality
    - Output Concepts
  - Appendix D: Comparison to Actual US Budget {.appendix}
    - Current US Discretionary Budget vs. OSL Targets

---

## _quarto-opg.yml
**Title:** Optimal Policy Generator: Evidence-Based Policy Recommendations for Jurisdictions
**Type:** website
**Files:** 1 | **Words:** 13,335

#### knowledge/appendix/optimal-policy-generator-spec.qmd
**Title:** Optimal Policy Generator: Evidence-Based Policy Recommendations for Jurisdictions
**Description:** The Optimal Policy Generator (OPG) produces systematic policy recommendations for jurisdictions at any level (country, state, city), generating prioritized enact/replace/repeal/maintain recommendation...
**Stats:** 13,335 words | 1,964 lines

  - Abstract {.unnumbered}
  - The Two Welfare Metrics {#sec-two-metrics}
    - Why Only Two Metrics?
    - Income Metric Definition {#sec-income-definition}
    - Outcome Translation Methodology {#sec-outcome-translation}
  - The Evidence Base: Centuries of Natural Policy Experiments {#sec-evidence-base}
    - Scale of Available Natural Experiments
    - The OPG Pipeline
    - Why This Hasn't Been Done Before
  - System Overview {#sec-opg-system-overview}
    - What Policymakers See
    - What Policy Analysts See
  - Introduction
    - Why Generic Policy Scores Are Not Enough
    - Why Policy Ranking Fails Today
    - Scale of Available Evidence
    - Contributions
    - Validation Status
  - Related Work
    - Existing Policy Evaluation Frameworks
    - This Framework's Contribution
  - Theoretical Framework
    - The Policy Optimization Problem
    - Evidence Aggregation Properties
    - Information Value
  - Core Methodology
    - Policy-Outcome Data Structure
      - Core Tables
      - Policy Types
    - Analysis Methods {#sec-analysis-methods}
      - Synthetic Control Method
      - Difference-in-Differences (DiD)
      - Regression Discontinuity Design (RDD)
      - Event Study / Interrupted Time Series
      - Confidence Weighting by Method
    - Bradford Hill Criteria Scoring Functions {#sec-bradford-hill}
      - Strength of Association
      - Consistency Across Jurisdictions
      - Temporality (Required)
      - Dose-Response Gradient
      - Experiment Quality
      - Plausibility (Mechanistic)
      - Coherence with Literature
      - Analogy to Similar Policies
      - Specificity
    - Causal Confidence Score (CCS) Calculation
  - Jurisdiction Policy Inventory
    - Tracking Current Policies by Jurisdiction
    - Data Sources for Policy Status
    - Handling Missing Data
  - Policy Gap Analysis {#sec-policy-gap}
    - Comparing Current to Optimal
    - Gap Types
    - Priority Scoring
    - Context Adjustment {#sec-context-adjustment}
  - Recommendation Generation {#sec-recommendation-generation}
    - Recommendation Types
    - Blocking Factors {#sec-blocking-factors}
    - Similar Jurisdictions {#sec-similar-jurisdictions}
      - Computing Jurisdiction Similarity
    - Recommended Tracking (for OPG Feedback)
  - Optimal Jurisdictional Level for Policy Implementation
    - The Subsidiarity Principle for Evidence Generation
    - When Higher Levels Are Necessary
    - Jurisdictional Level in Recommendations
  - Policy Impact Score (Intermediate Metric) {#sec-pis}
    - Overview
    - Jurisdiction-Level PIS Calculation
    - Always Report Both Metrics Separately
    - Effect Estimate Standardization
    - Quality Adjustment Factor
    - Confounder Adjustment
  - Global (Aggregate) PIS Calculation {#sec-global-pis}
    - Pooled Effect Estimate
    - Pooled PIS Across Jurisdictions
    - Heterogeneity Statistics
    - Evidence Grading {#sec-evidence-grading}
    - Context-Specific Confidence
  - Quality Requirements & Validation
    - Minimum Thresholds for Inclusion
    - Parallel Trends Testing (DiD)
    - Pre-Treatment Fit (Synthetic Control)
    - Placebo and Robustness Tests
  - Interpreting Recommendations
    - Priority Tiers
    - Political Feasibility Notes
    - Sequencing Guidance
  - Effect Size Benchmarks {#sec-effect-benchmarks}
  - Trial Prioritization {#sec-trial-prioritization}
    - Value of Information Calculation
    - Natural Experiment Identification
    - Recommended Pilot Jurisdictions
  - Data Sources
    - Primary Policy Databases
    - Primary Outcome Databases
    - Subnational Data
    - Jurisdiction Policy Inventory Sources
  - Limitations
    - Oracle Capture Risk
    - Confounding Severity
    - Heterogeneous Effects
    - Jurisdiction-Specific Caveats
    - Time-Varying Effects
    - Publication Bias
    - Epistemic Limitations
  - Validation Framework {#sec-validation-framework}
    - The Critical Question
    - Addressing Adoption Bias
    - Proposed Validation Study
    - Prospective Pre-Registration
    - Known Limitations Requiring Validation
    - Continuous Improvement via Adoption Feedback
  - Future Directions
    - Methodological Improvements
    - Validation Priorities
    - Data Infrastructure
    - Integration with Decision-Making
  - Conclusion
  - Acknowledgments {.unnumbered}
  - References
  - Appendix A: Worked Example - Texas Policy Recommendations {.appendix}
    - ⚠️ SYNTHETIC DATA - NOT EMPIRICAL FINDINGS
    - Overview
    - Texas Policy Inventory (Sample)
    - Step 1: Calculate Policy Impact Scores
    - Step 2: Apply Context Adjustment for Texas
    - Step 3: Generate Recommendations
  - ENACT (New Policies to Adopt)
  - REPLACE (Policies to Modify)
    - Tradeoff Demonstration
  - REPEAL (Policies to Remove)
  - MAINTAIN (No Change Needed)
    - Step 4: Summary Dashboard
    - Interpretation
  - Appendix B: OPG Analysis Workflow {.appendix}
    - Complete OPG Pipeline
    - Minimum Data Requirements Checklist
  - Appendix C: Glossary {.appendix}

---

## _quarto-optimocracy.yml
**Title:** Optimocracy: Evidence-Based Governance Through Outcome-Bound Optimization
**Type:** website
**Files:** 1 | **Words:** 12,861

#### knowledge/appendix/optimocracy-paper.qmd
**Title:** Optimocracy: Evidence-Based Governance Through Outcome-Bound Optimization
**Description:** Political dysfunction (cronyism, short-termism, and misalignment between political incentives and citizen outcomes) costs society an estimated 20% of potential GDP (the "Political Dysfunction Tax"). O...
**Stats:** 12,861 words | 1,280 lines

  - Abstract
  - Introduction: The Political Dysfunction Problem
    - Why Information Alone Fails
    - The Political Dysfunction Tax
    - The Optimocracy Thesis
    - How It Works in Practice
    - Contributions
  - The Scale of Welfare Loss: Empirical Foundations
    - A Formal Model of the Political Dysfunction Tax
    - Documented Welfare Losses by Policy Domain
    - Alternative Estimation: Bottom-Up Policy Cost Accounting
    - Why Information Doesn't Solve the Problem
    - Implications for Mechanism Design
    - When Does Optimocracy Beat the Status Quo?
      - Formal Model
  - Theoretical Foundations
    - Lessons from Technocratic Governance Failures
      - Soviet Central Planning
      - Failed Algorithmic Governance in Finance
      - Synthesis: Boundary Conditions for Algorithmic Governance
    - Why No Perfect System Exists (And Why That's Fine)
      - Arrow and Gibbard-Satterthwaite: Metric Selection Is Political
      - Mechanism Design: Honest Answers Require Honest Incentives
      - The Comparison That Matters
    - Index Funds and Passive Allocation
    - Credible Commitment Mechanisms
  - Mechanism Design
    - Architecture Overview
    - The Constitutional Layer
    - The Verification Layer
    - The Execution Layer
  - Welfare Metrics
    - Default Implementation: Two-Metric Welfare Function {#sec-two-metric-welfare}
    - Metric Defaults
  - Scope and Limits: A Taxonomy of Governance Decisions
    - Engaging with the Counter-Literature
    - A Taxonomy of Governance Decisions
    - Defining Optimocracy's Proper Scope
  - Advantages Over Political Governance
    - Capture Resistance
    - Time Consistency
    - Transparency and Verifiability
    - Reduced Coordination Costs
    - Depolarization Through Outcome Focus
  - Challenges and Failure Modes
    - Why Goodhart's Law Doesn't Apply Here
    - Oracle Capture
    - Democratic Legitimacy
  - Testable Predictions
    - Rejection Criteria
  - The Wrapper Architecture: Integration with IABs
  - Political Economy: Making Reform Happen
    - The Coase Theorem Applied to Governance Reform
    - A Taxonomy of Affected Parties
    - IABs as the Coasean Buyout Mechanism
    - The Cost of Political Reform: Quantifying "Political Impossibility"
    - The Natural Reform Coalition
  - Implementation Pathway
    - Implementation Phases
    - Realistic Adoption Path
    - Concrete First Deployment: The GiveWell Outcome Fund
    - Why Government Adoption Isn't Required
  - Conclusion
    - What About AI?
  - Appendix A: Technical Specification Sketch
    - Verification System Specification
    - Budget and Policy Optimization: Two Complementary Frameworks
      - Budget Optimization: The Optimal Budget Generator (OBG) Framework
      - Policy Optimization: The Policy Impact Score (PIS) Framework
      - How They Work Together
    - Algorithmic Governance Threat Model
      - Known Failure Modes
      - Why "Immutable Rules" Are Insufficient
      - Realistic Security Properties
      - Defense-in-Depth Architecture
  - Acknowledgments {.unnumbered}
  - References

---

## _quarto-political-dysfunction-tax.yml
**Title:** The Political Dysfunction Tax
**Type:** website
**Files:** 1 | **Words:** 5,447

#### knowledge/appendix/political-dysfunction-tax.qmd
**Title:** The Political Dysfunction Tax
**Description:** Quantifying the gap between current global governance and theoretical maximum welfare, estimating a 30-52% efficiency score and $101 trillion in annual opportunity costs.
**Stats:** 5,447 words | 416 lines

  - Introduction: The Mechanism Design of Civilizational Stagnation
  - Part 1: The Waste Ledger (The "Burned Capital")
    - Military Overspend: The Cost of Hegemony vs. Security
      - The Strategic Delta: Dominance vs. Denial
      - The Compounded Economic Loss
    - Administrative Bloat and the Friction Economy
      - The Healthcare Administration Tax
      - The Compliance Tax of Complexity
      - Corporate Welfare and Rent-Seeking
    - Incarceration & Prohibition: The Economics of Human Caging
      - The Direct Fiscal Cost
      - The Destruction of Human Capital
  - Part 2: The Opportunity Ledger (The "Buried Multipliers")
    - The Health Multiplier: The Trillion-Dollar Graveyard
      - The Efficiency Shift: From RCTs to PCTs
      - Valuing the "Lost Years"
    - The Science Multiplier: The ROI of the Future
      - The Fusion Gap
      - The AI Alignment Gap
    - The Human Capital Multiplier: Unleashing Cognitive Stock
      - The Lead Anchor
      - The Migration Arbitrage ("Trillion Dollar Bills")
  - Part 3: The Calculation ($E$)
    - The Variables
    - The Efficiency Score
  - Comparative Balance Sheet: Status Quo vs. Optimocracy
  - Analysis and Second-Order Insights
    - The "Parable of the Broken Window" on Steroids
    - The "Buried" Health Multiplier is the Critical Failure
    - Security Theater vs. Solvency
  - Conclusion
  - See Also
    - Works cited

---

## _quarto-test.yml
**Title:** Test Economics Document
**Type:** book
**Files:** 5 | **Words:** 8,128

#### index.qmd
**Title:** Wishocracy
**Description:** This paper introduces Wishocracy, a governance mechanism that employs Randomized Aggregated Pairwise Preference Allocation (RAPPA) to elicit and synthesize collective preferences for public resource a...
**Stats:** 6,797 words | 473 lines

- **Abstract**
- **Introduction: The Preference Aggregation Problem**
- **Theoretical Foundations**
  - **The Analytic Hierarchy Process**
  - **Quadratic Voting and Preference Intensity**
  - **Collective Intelligence and the Wisdom of Crowds**
  - **Related Work and Positioning in the Literature**
- **Mechanism Design: Randomized Aggregated Pairwise Preference Allocation**
  - **Core Mechanism**
    - Scenario: The Town Budget
  - **Formal Properties**
  - **Formal Model**
  - **Computational Complexity and Scalability**
  - **Comparative Information & Welfare Analysis**
    - **Information-Theoretic Superiority**
    - **Welfare Maximization: The "Median vs. Mean" Proof**
    - **Principal-Agent Cost Elimination**
- **Empirical Precedents and Evidence Base**
  - **Porto Alegre Participatory Budgeting**
  - **Taiwan's Digital Democracy Experiments**
  - **Stanford Participatory Budgeting Platform Research**
  - **Colorado Quadratic Voting Experiment**
  - **Reference Implementation: Wishocracy.org**
- **Addressing Potential Criticisms**
  - **Participation and Digital Divide**
  - **Manipulation and Sybil Attacks**
  - **Preference Laundering and Manufactured Consent**
  - **Complexity of Real Policy Trade-offs**
  - **Legitimacy and Accountability**
  - **Failure Modes and Robustness**
- **Conclusion**
- **Appendix A: The Service Provider Layer**
  - References {.unnumbered}

#### knowledge/test/test-parameters.qmd
**Title:** Test Parameters Document
**Description:** Minimal parameters document for testing
**Stats:** 262 words | 56 lines

- Introduction {#sec-test-parameters-intro}
  - Test Parameters
  - Simple Variable Test
  - Calculated Variable Test
  - Citation Test
  - Cross-Chapter Anchor Links Test
  - Cross-Site References

#### knowledge/appendix/parameters-and-calculations-test.qmd
**Title:** Methodology, Parameters, and Calculations
**Description:** Parameter definitions, formulas, uncertainty ranges, and data sources.
**Stats:** 669 words | 197 lines

  - Overview {#sec-parameters-and-calculations}
    - Quick Navigation
  - Calculated Values {#sec-calculated}
    - Annual Funding from 1% of Global Military Spending Redirected to DIH: $27.2B {#sec-treaty_annual_funding}
  - External Data Sources {#sec-external}
    - ADAPTABLE Trial Cost per Patient: $929 {#sec-adaptable_trial_cost_per_patient}
      - Uncertainty Range
      - Input Distribution
    - Global Military Spending in 2024: $2.72T {#sec-global_military_spending_annual_2024}
      - Uncertainty Range
  - Core Definitions {#sec-definitions}
    - 1% Reduction in Military Spending/War Costs from Treaty: 1% {#sec-treaty_reduction_pct}
      - Uncertainty Range

#### knowledge/references.qmd
**Title:** Source Quotes and References
**Description:** Bibliography and citations for all sources cited
**Stats:** 62 words | 22 lines

#### knowledge/test/test-economics.qmd
**Title:** Test Economics Document
**Description:** PAGE-LEVEL DESCRIPTION: This is the description from the QMD file frontmatter that should be used for og:description meta tag
**Stats:** 338 words | 67 lines

- Introduction
  - Link Test Cases
    - Internal Cross-References (Work in PDF)
    - External Cross-Site Links (Should Become Absolute URLs)
    - Absolute URLs (Should Remain Unchanged)
    - Anchor Links (Should Remain Unchanged)
    - Cross-Reference Format Comparison
  - Conclusion

---

## _quarto-wishocracy.yml
**Title:** Wishocracy: Solving the Democratic Principal-Agent Problem Through Pairwise Preference Aggregation
**Type:** website
**Files:** 1 | **Words:** 10,548

#### knowledge/appendix/wishocracy-paper.qmd
**Title:** Wishocracy: Solving the Democratic Principal-Agent Problem Through Pairwise Preference Aggregation
**Description:** Representative democracy suffers from an inescapable principal-agent problem where elected officials' incentives diverge from citizen welfare. Wishocracy introduces RAPPA (Randomized Aggregated Pairwi...
**Stats:** 10,548 words | 785 lines

- **Abstract**
- **Introduction: The Preference Aggregation Problem**
- **Theoretical Foundations**
  - **The Analytic Hierarchy Process**
  - **The Preference Intensity Problem**
  - **Collective Intelligence and the Wisdom of Crowds**
  - **Related Work and Positioning in the Literature**
- **Mechanism Design: Randomized Aggregated Pairwise Preference Allocation**
  - **Core Mechanism**
    - Scenario: Federal Budget Preferences
  - **Formal Properties**
  - **Formal Model**
  - **Computational Complexity and Scalability**
  - **Comparative Information & Welfare Analysis**
    - **Information-Theoretic Superiority**
    - **Welfare Maximization: The "Median vs. Mean" Proof**
    - **Principal-Agent Cost Elimination**
- **Empirical Precedents and Evidence Base**
  - **Porto Alegre Participatory Budgeting**
  - **Taiwan's Digital Democracy Experiments**
  - **Stanford Participatory Budgeting Platform Research**
  - **Reference Implementation: Wishocracy.org**
    - **Category Selection and Validation Methodology**
    - **Zero-Funding Filter Optimization**
    - **Hierarchical Category Structure**
    - **Framing Bias and Mitigation**
- **Addressing Potential Criticisms**
  - **Participation and Digital Divide**
  - **Manipulation and Sybil Attacks**
  - **Preference Laundering and Manufactured Consent**
  - **Complexity of Real Policy Trade-offs**
  - **Legitimacy and Accountability**
  - **Failure Modes and Robustness**
- **Implementation Pathway: From Information to Incentive Alignment**
  - **Why Information Alone Fails: Politicians Respond to Incentives**
  - **Three-Phase Implementation**
    - **Phase 1: Informational (Preference Gap Documentation)**
    - **Phase 2: Accountability Scoring (Politician Alignment Ratings)**
    - **Phase 3: Incentive Alignment (Integration with Incentive Alignment Bonds)**
  - **Why Federal-Scale Priorities**
  - **Evaluation Framework**
    - **Preference Aggregation Quality**
    - **Accountability System Effectiveness**
    - **Incentive Alignment Impact**
  - **Connection to Incentive Alignment Bonds**
  - **Connection to Optimocracy**
- **Conclusion**
- **Appendix A: The Service Provider Layer**
  - References {.unnumbered}

---

## ORPHANED FILES (not in any config)

*20 QMD files in knowledge/ not in any Quarto config:*

#### knowledge/appendix/military-vs-clinical-trials-funding-imbalance.qmd
- **Title:** Comparative Analysis: Global Military Spending vs. Clinical Trials Investment
- **Description:** A quantitative derivation of the 604:1 ratio between military expenditure and public clinical trials...
- **Words:** 590

#### knowledge/appendix/neuromodulation-case-study.qmd
- **Title:** Case Study: Closed-Loop Neuromodulation for Treatment-Resistant Depression
- **Description:** Quantifying the human cost of post-safety efficacy delays using breakthrough neuromodulation technol...
- **Words:** 636

#### knowledge/appendix/regulatory-mortality-analysis-for-humans.qmd
- **Title:** The Human Cost of Regulatory Latency
- **Description:** Top-down analysis estimating avoidable deaths, DALYs, and economic loss from 8.2-year efficacy lag.
- **Words:** 1,662

#### knowledge/appendix/wishocracy-implementation-guide.qmd
- **Title:** Wishocracy Implementation Guide
- **Description:** A Practical Framework for Piloting Aggregated Pairwise Preference Allocation
- **Words:** 772

#### knowledge/grant-proposal/index.qmd
- **Title:** Grant Proposal Cover Letter
- **Words:** 941

#### knowledge/legal/grant-agreement-guidance.qmd
- **Title:** Grant Agreement Guidance
- **Description:** Why we never draft the grant agreement and what to look for when they send it to us.
- **Words:** 1,013

#### knowledge/operations/ai-driven-regulatory-analysis.qmd
- **Title:** AI-Driven Regulatory Impact Analysis System
- **Description:** AI-driven system for regulatory health and economic impact analysis mandated by the Right to Trial &...
- **Words:** 567

#### knowledge/operations/careers/ai-engineer.qmd
- **Title:** AI Engineer - Patient Rights Advocacy & Civic Engagement Platform
- **Description:** Software and AI engineer wanted to help eradicate disease
- **Words:** 430

#### knowledge/operations/careers/applicant-evaluation-workflow.qmd
- **Title:** n8n Workflow for Evaluating Supreme Allied Commander Applicants
- **Description:** A detailed outline of the n8n workflow for parsing, evaluating, and ranking applications for the Sup...
- **Words:** 778

#### knowledge/operations/careers/capital-markets-lead.qmd
- **Title:** Capital Markets & Investor Relations Lead - VICTORY
- **Description:** Set up and sell VICTORY Incentive Alignment Bonds/tokens. Share clear reports. Run buybacks.
- **Words:** 215

#### knowledge/operations/careers/elections-ie-compliance-lead.qmd
- **Title:** Elections & IE Compliance Lead - US & International
- **Description:** Set up and run separate election operations by country. Keep clean walls and clear reports.
- **Words:** 201

#### knowledge/operations/careers/growth-referrals-lead.qmd
- **Title:** Growth & Referrals Lead - VOTE Points, Partners, and Growth
- **Description:** Help more people vote by running referrals, leaderboards, and partner lists.
- **Words:** 221

#### knowledge/operations/careers/peace-dividend-analytics-lead.qmd
- **Title:** Peace Dividend Analytics Lead - Value Capture & Public Dashboards
- **Description:** Show the money we save. Keep the calculators and methods clear and public.
- **Words:** 197

#### knowledge/operations/careers/security-audit-lead.qmd
- **Title:** Security & Audit Lead - 1% Treaty Fund and dFDA Infrastructure
- **Description:** Keep money and systems safe. Watch for attacks. Run fast response and audits.
- **Words:** 229

#### knowledge/operations/engagement-tracking-workflow.qmd
- **Title:** Automated Engagement Tracking Workflow
- **Description:** CRM system for automated lead capture, classification, nurturing, and conversion tracking.
- **Words:** 2,229

#### knowledge/operations/first-100-recruits-target-list.qmd
- **Title:** The First 100 Strategic Recruit Target List
- **Description:** Priority list of 100 high-leverage individuals to recruit in the first 90 days with outreach templat...
- **Words:** 2,438

#### knowledge/operations/global-referendum/public-opinion-survey.qmd
- **Title:** Global Survey on Human Values
- **Description:** Survey measuring public support for redirecting military spending to health innovation and modernizi...
- **Words:** 1,232

#### knowledge/operations/grant-application-playbook.qmd
- **Title:** Grant Application Playbook
- **Description:** How to siphon money from rich people's tax shelters to fund a global revolution.
- **Words:** 1,198

#### knowledge/operations/messaging-and-communications-strategy.qmd
- **Title:** How to Talk About Not Dying Without Sounding Insane
- **Description:** Why sentiment analysis matters and how better messaging gets you money and participants.
- **Words:** 857

#### knowledge/operations/pre-seed-strategy.qmd
- **Title:** Pre-Seed Strategy & Foundation
- **Description:** Outlines the initial steps, legal structure, pre-seed fundraising, and core team hiring required to ...
- **Words:** 614

---

## PAPER CITATIONS (for Quarto cross-references)

*Use these citation keys to reference papers in other chapters:*

| Config | Title | Citation Key | DOI |
|--------|-------|--------------|-----|
| _quarto-1-pct-treaty-impact.yml | The 1% Treaty: Health and Economic Impact of Redir... | `@1-pct-treaty-impact-paper-2025` | 10.5281/zenodo.18161561 |
| _quarto-cost-of-change.yml | The Price of Political Change: A Cost-Benefit Fram... | `@cost-of-change-paper-2025` | 10.5281/zenodo.18356216 |
| _quarto-dfda-impact.yml | The Health and Economic Impact of a Global System ... | `@dfda-impact-paper-2025` | 10.5281/zenodo.18243915 |
| _quarto-dfda-spec.yml | dFDA: A Decentralized Framework for Drug Assessmen... | `@dfda-spec-paper-2025` | 10.5281/zenodo.18203376 |
| _quarto-federal-efficiency-audit.yml | Federal Resource Allocation Efficiency Audit | `@federal-efficiency-audit-paper-2025` | - |
| _quarto-iab.yml | Incentive Alignment Bonds: Making Public Goods Fin... | `@iab-paper-2025` | 10.5281/zenodo.18203222 |
| _quarto-invisible-graveyard.yml | The Invisible Graveyard: Quantifying the Mortality... | `@invisible-graveyard-paper-2025` | 10.5281/zenodo.18356232 |
| _quarto-obg.yml | Optimal Budget Generator: Evidence-Based Budget Al... | `@obg-paper-2025` | 10.5281/zenodo.18356210 |
| _quarto-opg.yml | Optimal Policy Generator: Evidence-Based Policy Re... | `@opg-paper-2025` | 10.5281/zenodo.18356212 |
| _quarto-optimocracy.yml | Optimocracy: Evidence-Based Governance Through Out... | `@optimocracy-paper-2025` | 10.5281/zenodo.18356214 |
| _quarto-political-dysfunction-tax.yml | The Political Dysfunction Tax | `@political-dysfunction-tax-paper-2025` | - |
| _quarto-wishocracy.yml | Wishocracy: Solving the Democratic Principal-Agent... | `@wishocracy-paper-2025` | 10.5281/zenodo.18205882 |

**Usage:** `[@dfda-impact-paper-2025]` or `@dfda-impact-paper-2025`

---

## SUMMARY

- Quarto configs: 14
- Unique QMD files: 91
- Total words: 540,456
- Orphaned files: 20
- Paper configs: 12