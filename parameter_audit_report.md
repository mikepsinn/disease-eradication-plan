# Parameter Usage Audit Report

**Search Terms:** `RECOVERY_TRIAL_COST_PER_PATIENT`, `ADAPTABLE_TRIAL_COST_PER_PATIENT`, `DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`, `TRADITIONAL_PHASE3_COST_PER_PATIENT`, `recovery trial cost`, `adaptable trial cost`, `cost per patient`

## GUIDES/MISSION_AND_PRINCIPLES.md

- **Line 17** (matched '`cost per patient`')
  ```
  This repository documents "How to End War and Disease," a book about getting every nation to sign the **1% treaty** to redirect 1% of military spending to cure diseases instead of cause them. 

The plan involves creating a **Wishocratically governed** (using randomized pairwise preference allocations where everyone divides budget allocations between random pairs of priorities) global **Decentralized Institutes of Health (DIH)** that subsidizes patient participation in **decentralized pragmatic clinical trials with 80X lower cost per patient** (RECOVERY trial: $500/patient vs $41K traditional). 

All data flows through the **decentralized framework for drug assessment (dFDA)** which provides **Outcome Labels** for every food and drug, plus personalized treatment effectiveness rankings for all diseases.
  ```
  - [ ] Reviewed

- **Line 25** (matched '`cost per patient`')
  ```
  - **Primary Focus:** The unnecessary suffering and death from war (14M deaths/year) and disease (55M deaths/year). Every year we lose 69 million lives that could be saved.
- **The Problem:** Humans spend $119 trillion annually on war and disease while investing just 0.06% of that on finding cures. Children die of rare diseases while we build nuclear submarines.
- **The Solution:** Redirect just 1% of military spending to medical research through proven decentralized trial methods with 80X lower cost per patient (RECOVERY trial: $500/patient vs $41K traditional).
- **The Mission:** Save millions of lives by making curing people more profitable than killing them
- **Core Benefits to Emphasize:** The DIH delivers **80X lower cost per patient** (proven by Oxford RECOVERY trial: $500/patient vs $41,000), enabling **22.8X more trial capacity** to test treatments simultaneously. Uses **economic analysis to minimize DALYs/maximize QALYs**, provides **complete data transparency** (no hidden failures), and enables **100% patient participation** (vs 15% in traditional trials). Focus on OUTCOMES (more cures, faster, cheaper), not mechanisms (patient control, DAOs).
  ```
  - [ ] Reviewed

- **Line 27** (matched '`cost per patient`')
  ```
  - **The Solution:** Redirect just 1% of military spending to medical research through proven decentralized trial methods with 80X lower cost per patient (RECOVERY trial: $500/patient vs $41K traditional).
- **The Mission:** Save millions of lives by making curing people more profitable than killing them
- **Core Benefits to Emphasize:** The DIH delivers **80X lower cost per patient** (proven by Oxford RECOVERY trial: $500/patient vs $41,000), enabling **22.8X more trial capacity** to test treatments simultaneously. Uses **economic analysis to minimize DALYs/maximize QALYs**, provides **complete data transparency** (no hidden failures), and enables **100% patient participation** (vs 15% in traditional trials). Focus on OUTCOMES (more cures, faster, cheaper), not mechanisms (patient control, DAOs).
- **Healthcare Integration Model:** The DIH functions as a **clinical trial insurance provider** that works WITHIN existing healthcare infrastructure. Patients pay small copays ($20-50), doctors recommend trials like any treatment, pharmacies dispense trial meds like regular prescriptions. We're NOT "paying patients directly" - we're covering their costs like insurance. This maintains medical ethics while removing financial barriers.
- **Anchor in Public Choice Theory:** All strategic arguments must be framed through the lens of public choice theory. Assume that all actors (politicians, corporate leaders, voters) act in their own rational self-interest. Avoid arguments based on abstract "national interests" and instead focus on the specific, concrete incentives that drive individual decision-makers.
  ```
  - [ ] Reviewed

## _hardcoded-audit-v2.md

- **Line 27** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  - [ ] **Line 75**: '$20 million' → '{{< var recovery_trial_total_cost >}}' [MIXED]
  > Meanwhile, the UK's RECOVERY trial spent $20 million over six months, enrolled 48,000 patients, found multiple effective...
- [ ] **Line 91**: '40,000' → '{{< var traditional_phase3_cost_per_patient >}}' [MIXED]
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for {{< var recovery_trial_cost_per_patient ...
- [ ] **Line 174**: '$93,000' → '{{< var switzerland_gdp_per_capita_k >}}' [MIXED]
  ```
  - [ ] Reviewed

- **Line 28** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  > Meanwhile, the UK's RECOVERY trial spent $20 million over six months, enrolled 48,000 patients, found multiple effective...
- [ ] **Line 91**: '40,000' → '{{< var traditional_phase3_cost_per_patient >}}' [MIXED]
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for {{< var recovery_trial_cost_per_patient ...
- [ ] **Line 174**: '$93,000' → '{{< var switzerland_gdp_per_capita_k >}}' [MIXED]
  > Switzerland spends 0.7% of GDP on military and has $93,000 GDP per capita. America spends {{< var us_military_spending_p...
  ```
  - [ ] Reviewed

- **Line 54** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  > It takes {{< var treatment_acceleration_years_current >}} and $2.6 billion to get a drug through FDA approval. {{< var t...
- [ ] **Line 91**: '$10' → '{{< var sugar_subsidy_cost_per_person_annual >}}' [MIXED] | Also: npv_time_horizon_years
  > During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for {{< var recovery_trial_cost_per_patient ...
- [ ] **Line 162**: '$2.6 billion' → '{{< var pharma_drug_development_cost_current >}}' | Also: iab_political_incentive_funding_annual, victory_bond_annual_payout
  > This is why the FDA's rules mysteriously benefit large pharmaceutical companies who can afford $2.6 billion approval pro...
  ```
  - [ ] Reviewed

## _variables-dfda-spec.yml

- **Line 10** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  | Unit: USD/trial | Click to view details, calculation & sources">$20M</a>'
phase_3_trial_cost_min_cite: '@phase-3-cost-per-trial-range'
recovery_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-recovery_trial_cost_per_patient"
  class="parameter-link" data-source-ref="recovery-cost-500" data-source-type="external"
  data-confidence="high" title="RECOVERY trial cost per patient. Note: RECOVERY was
  ```
  - [ ] Reviewed

- **Line 12** (matched '`recovery trial cost`')
  ```
  recovery_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-recovery_trial_cost_per_patient"
  class="parameter-link" data-source-ref="recovery-cost-500" data-source-type="external"
  data-confidence="high" title="RECOVERY trial cost per patient. Note: RECOVERY was
  an outlier - hospital-based during COVID emergency, minimal extra procedures, existing
  NHS infrastructure, streamlined consent. Replicating this globally will be harder.
  ```
  - [ ] Reviewed

- **Line 17** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  | ✓ High confidence | 95% CI: [$400, $2.50K] | Dist: Lognormal | Unit: USD/patient
  | Click to view details, calculation & sources">$500 (95% CI: $400-$2.50K)</a>'
recovery_trial_cost_per_patient_cite: '@recovery-cost-500'
recovery_trial_cost_reduction_factor: '<a href="/knowledge/appendix/parameters-and-calculations#sec-recovery_trial_cost_reduction_factor"
  class="parameter-link" data-source-ref="recovery-trial-82x-cost-reduction" data-source-type="calculated"
  ```
  - [ ] Reviewed

- **Line 39** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  & sources">1.00M lives (95% CI: 500k lives-2.00M lives)</a>'
recovery_trial_global_lives_saved_cite: '@recovery-trial-1m-lives-saved'
traditional_phase3_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-traditional_phase3_cost_per_patient"
  class="parameter-link" data-source-ref="trial-costs-fda-study" data-source-type="external"
  data-confidence="high" title="Phase 3 cost per patient (median from FDA study) |
  ```
  - [ ] Reviewed

- **Line 41** (matched '`cost per patient`')
  ```
  traditional_phase3_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-traditional_phase3_cost_per_patient"
  class="parameter-link" data-source-ref="trial-costs-fda-study" data-source-type="external"
  data-confidence="high" title="Phase 3 cost per patient (median from FDA study) |
  ✓ High confidence | 95% CI: [$20K, $120K] | Dist: Lognormal | Unit: USD/patient
  | Click to view details, calculation & sources">$41K (95% CI: $20K-$120K)</a>'
  ```
  - [ ] Reviewed

- **Line 44** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  ✓ High confidence | 95% CI: [$20K, $120K] | Dist: Lognormal | Unit: USD/patient
  | Click to view details, calculation & sources">$41K (95% CI: $20K-$120K)</a>'
traditional_phase3_cost_per_patient_cite: '@trial-costs-fda-study'
  ```
  - [ ] Reviewed

## _variables-economics.yml

- **Line 5** (matched '`ADAPTABLE_TRIAL_COST_PER_PATIENT`')
  ```
  # Re-generate with: python scripts/generate-everything-parameters-variables-calculations-references.py

adaptable_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-adaptable_trial_cost_per_patient"
  class="parameter-link" data-source-ref="pragmatic-trials-cost-advantage" data-source-type="external"
  data-confidence="medium" title="Cost per patient in ADAPTABLE trial ($14M PCORI
  ```
  - [ ] Reviewed

- **Line 7** (matched '`cost per patient`')
  ```
  adaptable_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-adaptable_trial_cost_per_patient"
  class="parameter-link" data-source-ref="pragmatic-trials-cost-advantage" data-source-type="external"
  data-confidence="medium" title="Cost per patient in ADAPTABLE trial ($14M PCORI
  grant / 15,076 patients). Note: This is the direct grant cost; true cost including
  in-kind may be 10-40% higher. | ~ Medium confidence | 95% CI: [$929, $1.40K] | Dist:
  ```
  - [ ] Reviewed

- **Line 12** (matched '`ADAPTABLE_TRIAL_COST_PER_PATIENT`')
  ```
  Lognormal | Unit: USD/patient | Click to view details, calculation & sources">$929
  (95% CI: $929-$1.40K)</a>'
adaptable_trial_cost_per_patient_cite: '@pragmatic-trials-cost-advantage'
adaptable_trial_patients: '<a href="/knowledge/appendix/parameters-and-calculations#sec-adaptable_trial_patients"
  class="parameter-link" data-source-ref="pragmatic-trials-cost-advantage" data-source-type="definition"
  ```
  - [ ] Reviewed

- **Line 854** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  $$'
dfda_pragmatic_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-dfda_pragmatic_trial_cost_per_patient"
  class="parameter-link" data-source-ref="pragmatic-trials-cost-advantage" data-source-type="external"
  data-confidence="medium" title="dFDA pragmatic trial cost per patient. Uses ADAPTABLE
  ```
  - [ ] Reviewed

- **Line 856** (matched '`cost per patient`')
  ```
  dfda_pragmatic_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-dfda_pragmatic_trial_cost_per_patient"
  class="parameter-link" data-source-ref="pragmatic-trials-cost-advantage" data-source-type="external"
  data-confidence="medium" title="dFDA pragmatic trial cost per patient. Uses ADAPTABLE
  trial ($929) as DELIBERATELY CONSERVATIVE central estimate. Harvard meta-analysis
  of 108 trials found median of only $97/patient - our estimate may overstate costs
  ```
  - [ ] Reviewed

- **Line 862** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  trials. | ~ Medium confidence | 95% CI: [$97, $3K] | Dist: Lognormal | Unit: USD/patient
  | Click to view details, calculation & sources">$929 (95% CI: $97-$3K)</a>'
dfda_pragmatic_trial_cost_per_patient_cite: '@pragmatic-trials-cost-advantage'
dfda_queue_clearance_years: '<a href="/knowledge/appendix/parameters-and-calculations#sec-dfda_queue_clearance_years"
  class="parameter-link" data-source-ref="" data-source-type="calculated" data-confidence="low"
  ```
  - [ ] Reviewed

- **Line 2784** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  diseases)</a>'
rare_diseases_count_global_cite: '@95-pct-diseases-no-treatment'
recovery_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-recovery_trial_cost_per_patient"
  class="parameter-link" data-source-ref="recovery-cost-500" data-source-type="external"
  data-confidence="high" title="RECOVERY trial cost per patient. Note: RECOVERY was
  ```
  - [ ] Reviewed

- **Line 2786** (matched '`recovery trial cost`')
  ```
  recovery_trial_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-recovery_trial_cost_per_patient"
  class="parameter-link" data-source-ref="recovery-cost-500" data-source-type="external"
  data-confidence="high" title="RECOVERY trial cost per patient. Note: RECOVERY was
  an outlier - hospital-based during COVID emergency, minimal extra procedures, existing
  NHS infrastructure, streamlined consent. Replicating this globally will be harder.
  ```
  - [ ] Reviewed

- **Line 2791** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  | ✓ High confidence | 95% CI: [$400, $2.50K] | Dist: Lognormal | Unit: USD/patient
  | Click to view details, calculation & sources">$500 (95% CI: $400-$2.50K)</a>'
recovery_trial_cost_per_patient_cite: '@recovery-cost-500'
recovery_trial_cost_reduction_factor: '<a href="/knowledge/appendix/parameters-and-calculations#sec-recovery_trial_cost_reduction_factor"
  class="parameter-link" data-source-ref="recovery-trial-82x-cost-reduction" data-source-type="calculated"
  ```
  - [ ] Reviewed

- **Line 2892** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  relationships] | Dist: Lognormal | Unit: relationships | Click to view details,
  calculation & sources">32.5k relationships (95% CI: 15.0k relationships-50.0k relationships)</a>'
traditional_phase3_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-traditional_phase3_cost_per_patient"
  class="parameter-link" data-source-ref="trial-costs-fda-study" data-source-type="external"
  data-confidence="high" title="Phase 3 cost per patient (median from FDA study) |
  ```
  - [ ] Reviewed

- **Line 2894** (matched '`cost per patient`')
  ```
  traditional_phase3_cost_per_patient: '<a href="/knowledge/appendix/parameters-and-calculations#sec-traditional_phase3_cost_per_patient"
  class="parameter-link" data-source-ref="trial-costs-fda-study" data-source-type="external"
  data-confidence="high" title="Phase 3 cost per patient (median from FDA study) |
  ✓ High confidence | 95% CI: [$20K, $120K] | Dist: Lognormal | Unit: USD/patient
  | Click to view details, calculation & sources">$41K (95% CI: $20K-$120K)</a>'
  ```
  - [ ] Reviewed

- **Line 2897** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  ✓ High confidence | 95% CI: [$20K, $120K] | Dist: Lognormal | Unit: USD/patient
  | Click to view details, calculation & sources">$41K (95% CI: $20K-$120K)</a>'
traditional_phase3_cost_per_patient_cite: '@trial-costs-fda-study'
treatment_acceleration_years_current: '<a href="/knowledge/appendix/parameters-and-calculations#sec-treatment_acceleration_years_current"
  class="parameter-link" data-source-ref="fda-approval-timeline-10-years" data-source-type="external"
  ```
  - [ ] Reviewed

## assets/IMAGE-GUIDE.md

- **Line 63** (matched '`cost per patient`')
  ```
  **Size:** 153.4 KB | **Format:** PNG | **Dimensions:** 795x819

**Description:** The image visualizes the high costs associated with developing a single drug and conducting clinical trials. It presents data on the estimated development cost of a single drug ($2.6 billion), the cost per patient in a trial ($36,500), trial costs by medical indication (e.g., pain/anesthesia, ophthalmology), and a pie chart breaking down the costs within a clinical trial (e.g., staff & admin, site monitoring). A stethoscope is present in the upper right.

**Keywords:** Drug development, clinical trials, research costs, healthcare spending, medical research, pharmaceutical industry, cost analysis, clinical trial costs, pain/anesthesia, oncology
  ```
  - [ ] Reviewed

## brainstorm.md

- **Line 273** (matched '`cost per patient`')
  ```
  Key facts:

* Cost per patient ≈ **$500** vs typical pharma trials ≈ **$40,000 per patient** (≈80× cheaper).
* Trial cost ≈ **£2.1M (~$2.7M)** for the dexamethasone question.
* Dexamethasone result estimated to have saved **~1 million lives globally in the first 9 months**.
  ```
  - [ ] Reviewed

## dih_models/parameters.py

- **Line 1342** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  # dFDA Trial Economics
RECOVERY_TRIAL_COST_PER_PATIENT = Parameter(
    500,
    source_ref=ReferenceID.RECOVERY_COST_500,
  ```
  - [ ] Reviewed

- **Line 1346** (matched '`recovery trial cost`')
  ```
  source_ref=ReferenceID.RECOVERY_COST_500,
    source_type="external",
    description="RECOVERY trial cost per patient. Note: RECOVERY was an outlier - hospital-based during COVID emergency, minimal extra procedures, existing NHS infrastructure, streamlined consent. Replicating this globally will be harder.",
    display_name="Recovery Trial Cost per Patient",
    unit="USD/patient",
  ```
  - [ ] Reviewed

- **Line 1347** (matched '`recovery trial cost`')
  ```
  source_type="external",
    description="RECOVERY trial cost per patient. Note: RECOVERY was an outlier - hospital-based during COVID emergency, minimal extra procedures, existing NHS infrastructure, streamlined consent. Replicating this globally will be harder.",
    display_name="Recovery Trial Cost per Patient",
    unit="USD/patient",
    confidence_interval=(400, 2500),  # Widened to reflect implementation challenges:
  ```
  - [ ] Reviewed

- **Line 1385** (matched '`ADAPTABLE_TRIAL_COST_PER_PATIENT`')
  ```
  )

ADAPTABLE_TRIAL_COST_PER_PATIENT = Parameter(
    929,  # $14M / 15,076 patients = $929/patient
    source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
  ```
  - [ ] Reviewed

- **Line 1389** (matched '`cost per patient`')
  ```
  source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
    source_type="external",
    description="Cost per patient in ADAPTABLE trial ($14M PCORI grant / 15,076 patients). Note: This is the direct grant cost; true cost including in-kind may be 10-40% higher.",
    display_name="ADAPTABLE Trial Cost per Patient",
    unit="USD/patient",
  ```
  - [ ] Reviewed

- **Line 1390** (matched '`adaptable trial cost`')
  ```
  source_type="external",
    description="Cost per patient in ADAPTABLE trial ($14M PCORI grant / 15,076 patients). Note: This is the direct grant cost; true cost including in-kind may be 10-40% higher.",
    display_name="ADAPTABLE Trial Cost per Patient",
    unit="USD/patient",
    confidence="medium",
  ```
  - [ ] Reviewed

- **Line 1395** (matched '`cost per patient`')
  ```
  confidence_interval=(929, 1400),  # Grant cost to estimated true cost with in-kind
    distribution="lognormal",
    keywords=["adaptable", "pcornet", "cost per patient", "pragmatic"],
)  # $929/patient from PCORI grant; up to ~$1,400 with in-kind
  ```
  - [ ] Reviewed

- **Line 1405** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  # Meta-analysis shows median is only $97 - we use the HIGHER value for credibility
# This means our projections likely UNDERSTATE the true potential by ~10x
DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT = Parameter(
    929,  # ADAPTABLE trial empirical cost - CONSERVATIVE choice
    source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
  ```
  - [ ] Reviewed

- **Line 1409** (matched '`cost per patient`')
  ```
  source_ref=ReferenceID.PRAGMATIC_TRIALS_COST_ADVANTAGE,
    source_type="external",
    description="dFDA pragmatic trial cost per patient. Uses ADAPTABLE trial ($929) as DELIBERATELY CONSERVATIVE central estimate. Harvard meta-analysis of 108 trials found median of only $97/patient - our estimate may overstate costs by 10x. Confidence interval spans meta-analysis median to complex chronic disease trials.",
    display_name="dFDA Pragmatic Trial Cost per Patient",
    unit="USD/patient",
  ```
  - [ ] Reviewed

- **Line 1410** (matched '`cost per patient`')
  ```
  source_type="external",
    description="dFDA pragmatic trial cost per patient. Uses ADAPTABLE trial ($929) as DELIBERATELY CONSERVATIVE central estimate. Harvard meta-analysis of 108 trials found median of only $97/patient - our estimate may overstate costs by 10x. Confidence interval spans meta-analysis median to complex chronic disease trials.",
    display_name="dFDA Pragmatic Trial Cost per Patient",
    unit="USD/patient",
    confidence="medium",
  ```
  - [ ] Reviewed

- **Line 1422** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  # Traditional Phase 3 Cost (baseline for comparison)
TRADITIONAL_PHASE3_COST_PER_PATIENT = Parameter(
    41000,
    source_ref=ReferenceID.TRIAL_COSTS_FDA_STUDY,
  ```
  - [ ] Reviewed

- **Line 1426** (matched '`cost per patient`')
  ```
  source_ref=ReferenceID.TRIAL_COSTS_FDA_STUDY,
    source_type="external",
    description="Phase 3 cost per patient (median from FDA study)",
    display_name="Phase 3 Cost per Patient",
    unit="USD/patient",
  ```
  - [ ] Reviewed

- **Line 1427** (matched '`cost per patient`')
  ```
  source_type="external",
    description="Phase 3 cost per patient (median from FDA study)",
    display_name="Phase 3 Cost per Patient",
    unit="USD/patient",
    distribution=DistributionType.LOGNORMAL,  # Right-skewed: simple trials ~$20K, complex ~$120K+
  ```
  - [ ] Reviewed

- **Line 1432** (matched '`cost per patient`')
  ```
  confidence_interval=(20000, 120000),  # Range from Moore et al. 2020 FDA study
    keywords=["41k", "confirmatory trial", "third phase", "rct", "participant", "subject", "volunteer", "median"]
)  # Median cost per patient from FDA/JAMA study (Moore et al. 2020)

# Trial Cost Reduction Factors (calculated from cost per patient comparisons)
  ```
  - [ ] Reviewed

- **Line 1434** (matched '`cost per patient`')
  ```
  )  # Median cost per patient from FDA/JAMA study (Moore et al. 2020)

# Trial Cost Reduction Factors (calculated from cost per patient comparisons)

# RECOVERY Trial Cost Reduction (historical evidence)
  ```
  - [ ] Reviewed

- **Line 1436** (matched '`recovery trial cost`')
  ```
  # Trial Cost Reduction Factors (calculated from cost per patient comparisons)

# RECOVERY Trial Cost Reduction (historical evidence)
# $41,000 traditional / $500 RECOVERY = 82x
RECOVERY_TRIAL_COST_REDUCTION_FACTOR = Parameter(
  ```
  - [ ] Reviewed

- **Line 1439** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  # $41,000 traditional / $500 RECOVERY = 82x
RECOVERY_TRIAL_COST_REDUCTION_FACTOR = Parameter(
    TRADITIONAL_PHASE3_COST_PER_PATIENT / RECOVERY_TRIAL_COST_PER_PATIENT,
    source_ref=ReferenceID.RECOVERY_TRIAL_82X_COST_REDUCTION,
    source_type="calculated",
  ```
  - [ ] Reviewed

- **Line 1443** (matched '`recovery trial cost`')
  ```
  source_type="calculated",
    description="Cost reduction factor demonstrated by RECOVERY trial ($41K traditional / $500 RECOVERY = 82x)",
    display_name="RECOVERY Trial Cost Reduction Factor",
    unit="multiplier",
    formula="TRADITIONAL_PHASE3_COST / RECOVERY_COST",    keywords=["oxford", "recovery", "82x", "rct", "clinical trial", "cost reduction", "historical"],
  ```
  - [ ] Reviewed

- **Line 1446** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  unit="multiplier",
    formula="TRADITIONAL_PHASE3_COST / RECOVERY_COST",    keywords=["oxford", "recovery", "82x", "rct", "clinical trial", "cost reduction", "historical"],
    inputs=['TRADITIONAL_PHASE3_COST_PER_PATIENT', 'RECOVERY_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"] / ctx["RECOVERY_TRIAL_COST_PER_PATIENT"],
)  # 82x reduction proven by RECOVERY trial ($41K / $500)
  ```
  - [ ] Reviewed

- **Line 1447** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  formula="TRADITIONAL_PHASE3_COST / RECOVERY_COST",    keywords=["oxford", "recovery", "82x", "rct", "clinical trial", "cost reduction", "historical"],
    inputs=['TRADITIONAL_PHASE3_COST_PER_PATIENT', 'RECOVERY_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"] / ctx["RECOVERY_TRIAL_COST_PER_PATIENT"],
)  # 82x reduction proven by RECOVERY trial ($41K / $500)
  ```
  - [ ] Reviewed

- **Line 1453** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  # $41,000 traditional / $1,200 dFDA pragmatic = 34.17x
DFDA_TRIAL_COST_REDUCTION_FACTOR = Parameter(
    TRADITIONAL_PHASE3_COST_PER_PATIENT / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    source_ref="/knowledge/appendix/dfda-impact-paper.qmd#cost-reduction",
    source_type="calculated",
  ```
  - [ ] Reviewed

- **Line 1460** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  unit="multiplier",
    formula="TRADITIONAL_PHASE3_COST / DFDA_PRAGMATIC_COST",    keywords=["dfda", "pragmatic", "34x", "rct", "clinical trial", "cost reduction", "projected"],
    inputs=['TRADITIONAL_PHASE3_COST_PER_PATIENT', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
)  # 34x reduction projected for dFDA ($41K / $1,200)
  ```
  - [ ] Reviewed

- **Line 1461** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  formula="TRADITIONAL_PHASE3_COST / DFDA_PRAGMATIC_COST",    keywords=["dfda", "pragmatic", "34x", "rct", "clinical trial", "cost reduction", "projected"],
    inputs=['TRADITIONAL_PHASE3_COST_PER_PATIENT', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
)  # 34x reduction projected for dFDA ($41K / $1,200)
  ```
  - [ ] Reviewed

- **Line 1466** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  # dFDA Trial Cost Reduction as Percentage (derived from factor)
DFDA_TRIAL_COST_REDUCTION_PCT = Parameter(
    1 - (DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT / TRADITIONAL_PHASE3_COST_PER_PATIENT),
    source_ref="/knowledge/appendix/dfda-impact-paper.qmd#cost-reduction",
    source_type="calculated",
  ```
  - [ ] Reviewed

- **Line 1474** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  formula="1 - (DFDA_COST / TRADITIONAL_COST)",
    latex=r"R_{pct} = 1 - \frac{\$1{,}200}{\$41{,}000} = 97.07\%",
    # Derived from: DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT ($1,200) vs TRADITIONAL_PHASE3_COST_PER_PATIENT ($41,000)
    # This matches DFDA_TRIAL_COST_REDUCTION_FACTOR = 34× (which is the inverse: $41K / $1.2K)
    # RECOVERY trial achieved 82× (98.8%), so 97% is conservative relative to historical evidence
  ```
  - [ ] Reviewed

- **Line 1479** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  validation_min=0.90,   # Floor: 90% reduction (minimum based on RECOVERY-like efficiency)
    validation_max=0.99,   # Ceiling: 99% reduction (approaching theoretical maximum)
    inputs=["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT", "TRADITIONAL_PHASE3_COST_PER_PATIENT"],
    compute=lambda ctx: 1 - (ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"] / ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"]),
    keywords=["97%", "rct", "clinical study", "clinical trial", "cost reduction", "research trial", "randomized controlled trial"]
  ```
  - [ ] Reviewed

- **Line 1480** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  validation_max=0.99,   # Ceiling: 99% reduction (approaching theoretical maximum)
    inputs=["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT", "TRADITIONAL_PHASE3_COST_PER_PATIENT"],
    compute=lambda ctx: 1 - (ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"] / ctx["TRADITIONAL_PHASE3_COST_PER_PATIENT"]),
    keywords=["97%", "rct", "clinical study", "clinical trial", "cost reduction", "research trial", "randomized controlled trial"]
)  # 97% reduction = 34× cost reduction factor
  ```
  - [ ] Reviewed

- **Line 1960** (matched '`cost per patient`')
  ```
  source_ref="/knowledge/appendix/dfda-impact-paper.qmd#cost-per-patient",
    source_type="definition",
    description="Target cost per patient in USD (same as DFDA_TARGET_COST_PER_PATIENT but in dollars)",
    display_name="Decentralized Framework for Drug Assessment Target Cost per Patient in USD",
    unit="USD/patient",
  ```
  - [ ] Reviewed

- **Line 1961** (matched '`cost per patient`')
  ```
  source_type="definition",
    description="Target cost per patient in USD (same as DFDA_TARGET_COST_PER_PATIENT but in dollars)",
    display_name="Decentralized Framework for Drug Assessment Target Cost per Patient in USD",
    unit="USD/patient",
    keywords=["1k", "pragmatic trials", "real world evidence", "participant", "subject", "volunteer", "enrollee"]
  ```
  - [ ] Reviewed

- **Line 3726** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  DIH_PATIENTS_FUNDABLE_ANNUALLY = Parameter(
    DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL / DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT,
    source_ref="/knowledge/economics/economics.qmd#funding-allocation",
    source_type="calculated",
  ```
  - [ ] Reviewed

- **Line 3733** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  unit="patients/year",
    formula="TRIAL_SUBSIDIES ÷ DFDA_COST_PER_PATIENT",    keywords=["trial", "participant", "enrollment", "capacity", "patient"],
    inputs=['DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
)  # ~20.4M patients/year at $1,200/patient
  ```
  - [ ] Reviewed

- **Line 3734** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  formula="TRIAL_SUBSIDIES ÷ DFDA_COST_PER_PATIENT",    keywords=["trial", "participant", "enrollment", "capacity", "patient"],
    inputs=['DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL', 'DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT'],
    compute=lambda ctx: ctx["DIH_TREASURY_TRIAL_SUBSIDIES_ANNUAL"] / ctx["DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT"],
)  # ~20.4M patients/year at $1,200/patient
  ```
  - [ ] Reviewed

- **Line 3816** (matched '`recovery trial cost`')
  ```
  # Trial Capacity Multiplier (Simple Economic Calculation)
# DIH funding can support 48.8M patients/year at RECOVERY trial cost ($500/patient)
# Current global trial capacity: 1.9M patients/year (IQVIA 2022)
# Capacity Multiplier = DIH capacity / Current capacity
  ```
  - [ ] Reviewed

## index-book.qmd

- **Line 394** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  ### The Evidence

- **Oxford Already Did It**: [The RECOVERY trial](knowledge/appendix/recovery-trial.qmd) tested 6 treatments on 47,000 patients across 186 hospitals for {{< var recovery_trial_cost_per_patient >}}/patient (vs standard FDA phase 3 cost of {{< var traditional_phase3_cost_per_patient >}}), demonstrating a {{< var recovery_trial_cost_reduction_factor >}} cost reduction at scale. Not in theory. In reality. With actual dying people who became not-dying people.
- **You've Done This Before**: [After WW2, humans cut military spending by 30.0%](knowledge/proof/historical-precedents.qmd) and inadvertently created the greatest economic boom in history. You're only asking for 1.0%.
  ```
  - [ ] Reviewed

- **Line 563** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  **Insurance Companies**: "Healthy people file zero claims. Sick people file all the claims. We'll let you do the math since you love math.

**Big Pharma**: "Instead of paying {{< var traditional_phase3_cost_per_patient >}} per trial patient, they pay YOU. It's like if your costs became revenue. We call it 'reverse expenses' or 'profit.'"

**Politicians**: "{{< var treaty_campaign_voting_bloc_target >}} million voters want this. Your opponent supports it. You can either agree or explain why you prefer bombs to grandma's cancer treatment. Your choice."
  ```
  - [ ] Reviewed

## knowledge/appendix/clinical-trial-participants.qmd

- **Line 125** (matched '`cost per patient`')
  ```
  **We're turning away 99.82% of willing participants** (using drug trials), or 99.5% if counting all clinical research.

## The Cost Per Patient

Using IQVIA's {{< var current_trial_slots_available >}} drug trial participants:
  ```
  - [ ] Reviewed

- **Line 171** (matched '`cost per patient`')
  ```
  | Phase 4 | 5,790 | 2,718,541 | 90 | $6,437 |

(Cost per patient calculated from [phase spending estimates](global-clinical-trial-spending-by-phase.qmd) divided by participant counts)

## What a 1% Treaty Could Do
  ```
  - [ ] Reviewed

- **Line 193** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  - Patients report outcomes via smartphone
- Trials run continuously instead of in isolated batches
- Cost per participant drops to **{{< var dfda_pragmatic_trial_cost_per_patient >}}** (pragmatic trial cost, based on RECOVERY trial benchmarks)

#### The Result
  ```
  - [ ] Reviewed

- **Line 197** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  #### The Result

- {{< var dih_treasury_trial_subsidies_annual >}} ÷ {{< var dfda_pragmatic_trial_cost_per_patient >}} = **{{< var dih_patients_fundable_annually >}}/year**
- Current: {{< var current_trial_slots_available >}}/year (IQVIA 2022)
- **{{< var dfda_trial_capacity_multiplier >}}× more trial capacity** means testing {{< var dfda_trial_capacity_multiplier >}}× more treatments simultaneously
  ```
  - [ ] Reviewed

## knowledge/appendix/dfda-impact-paper.qmd

- **Line 34** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  ### What You Get

- **Cost Cuts:** Clinical trials cost [50-95% less](#gross-r-and-d-savings-from-dfda-implementation). The UK's [RECOVERY trial](recovery-trial.qmd) proved you can cut costs {{< var recovery_trial_cost_reduction_factor >}} without killing anyone extra. Our projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on the [ADAPTABLE trial](https://pcornet.org/clinical-research/pcornet-clinical-trials-demonstrations/adaptable/). Apply that globally to the {{< var global_clinical_trials_spending_annual >}} spent annually on trials, save [tens of billions](#roi-analysis).
- **More Drugs Faster:** Cheaper trials mean testing rare diseases and treatments that don't make billionaires richer. Drugs reach dying people before they finish dying.
- **Fewer Dead People:** The framework generates {{< var dfda_trial_capacity_plus_efficacy_lag_dalys >}} extra life-years through the {{< var dfda_trial_capacity_plus_efficacy_lag_years >}}-year timeline shift (from {{< var dfda_trial_capacity_multiplier >}}× trial capacity + efficacy lag elimination), plus faster access, better prevention data, and drugs for diseases companies currently ignore.
  ```
  - [ ] Reviewed

- **Line 83** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  #### Cost Reduction Assumptions

- Decentralized trial costs drop closer to the [Oxford RECOVERY model](#decentralized-trial-costs-modeled-on-oxford-recovery): from {{< var traditional_phase3_cost_per_patient >}} per patient to roughly **{{< var dfda_pragmatic_trial_cost_per_patient >}} per patient**.
- Regulatory oversight is streamlined through continuous data auditing, reducing administrative overhead.
  ```
  - [ ] Reviewed

- **Line 406** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  - Phase III: \$100 - {{< var dct_platform_funding_medium >}}/trial (large patient populations).

- **Per-Patient Phase III Costs**: Often {{< var traditional_phase3_cost_per_patient >}} per patient (site fees, overhead, staff, monitoring, data management).

### Decentralized Trial Costs Modeled on Pragmatic Trials
  ```
  - [ ] Reviewed

- **Line 410** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  ### Decentralized Trial Costs Modeled on Pragmatic Trials

- **Oxford RECOVERY**: Achieved **~{{< var recovery_trial_cost_per_patient >}} per patient**. Key strategies included:
  1. Embedding trial protocols within routine hospital care.
  2. Minimizing overhead by leveraging existing staff/resources and electronic data capture.
  ```
  - [ ] Reviewed

- **Line 417** (matched '`ADAPTABLE_TRIAL_COST_PER_PATIENT`')
  ```
  *Important caveat*: RECOVERY's exceptional cost efficiency benefited from NHS infrastructure integration and COVID-19 emergency conditions that may not be replicable globally.

- **ADAPTABLE Trial (PCORnet)**: The US-based [ADAPTABLE trial](https://pcornet.org/clinical-research/pcornet-clinical-trials-demonstrations/adaptable/) ({{< var adaptable_trial_total_cost >}} / {{< var adaptable_trial_patients >}} = **{{< var adaptable_trial_cost_per_patient >}}/patient**) provides a more representative benchmark for pragmatic trial costs in typical healthcare settings without emergency conditions.

- **dFDA Cost Projection**: Our projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on ADAPTABLE. Confidence interval ($500-$3,000) captures range from RECOVERY-like efficiency to complex chronic disease trials.
  ```
  - [ ] Reviewed

- **Line 419** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  - **ADAPTABLE Trial (PCORnet)**: The US-based [ADAPTABLE trial](https://pcornet.org/clinical-research/pcornet-clinical-trials-demonstrations/adaptable/) ({{< var adaptable_trial_total_cost >}} / {{< var adaptable_trial_patients >}} = **{{< var adaptable_trial_cost_per_patient >}}/patient**) provides a more representative benchmark for pragmatic trial costs in typical healthcare settings without emergency conditions.

- **dFDA Cost Projection**: Our projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on ADAPTABLE. Confidence interval ($500-$3,000) captures range from RECOVERY-like efficiency to complex chronic disease trials.

- **Extrapolation to New System**:
  ```
  - [ ] Reviewed

- **Line 422** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  - **Extrapolation to New System**:
  - A well-integrated global framework could achieve {{< var dfda_pragmatic_trial_cost_per_patient >}} per patient in many cases, especially for pragmatic or observational designs.
  - Up to **~{{< var dfda_trial_cost_reduction_factor >}}× cost reduction** is achievable by comparing pragmatic trial costs ({{< var dfda_pragmatic_trial_cost_per_patient >}}) against traditional costs of {{< var traditional_phase3_cost_per_patient >}}.
  ```
  - [ ] Reviewed

- **Line 423** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  - **Extrapolation to New System**:
  - A well-integrated global framework could achieve {{< var dfda_pragmatic_trial_cost_per_patient >}} per patient in many cases, especially for pragmatic or observational designs.
  - Up to **~{{< var dfda_trial_cost_reduction_factor >}}× cost reduction** is achievable by comparing pragmatic trial costs ({{< var dfda_pragmatic_trial_cost_per_patient >}}) against traditional costs of {{< var traditional_phase3_cost_per_patient >}}.

  The cost reduction factor can be formalized as:
  ```
  - [ ] Reviewed

- **Line 432** (matched '`cost per patient`')
  ```
  Where:
  - $c_t$ is the traditional cost per patient
  - $c_d$ is the decentralized cost per patient
  ```
  - [ ] Reviewed

- **Line 433** (matched '`cost per patient`')
  ```
  Where:
  - $c_t$ is the traditional cost per patient
  - $c_d$ is the decentralized cost per patient

  The percentage reduction is:
  ```
  - [ ] Reviewed

- **Line 445** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  1. **By Reducing Per-Patient Costs**

   - If a trial with 5,000 participants costs {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient, total cost is ~\$6 million, versus \$200 - \$600 million under traditional models.
   - This magnitude of savings can drastically reduce the total cost of clinical development.
  ```
  - [ ] Reviewed

- **Line 455** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  Where:
   - $c_t$ is the traditional cost per patient ({{< var traditional_phase3_cost_per_patient >}})
   - $c_d$ is the decentralized cost per patient ({{< var dfda_pragmatic_trial_cost_per_patient >}})
  ```
  - [ ] Reviewed

- **Line 456** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  Where:
   - $c_t$ is the traditional cost per patient ({{< var traditional_phase3_cost_per_patient >}})
   - $c_d$ is the decentralized cost per patient ({{< var dfda_pragmatic_trial_cost_per_patient >}})

   For a trial with $x = 5,000$ participants, savings are approximately:
  ```
  - [ ] Reviewed

- **Line 583** (matched '`ADAPTABLE_TRIAL_COST_PER_PATIENT`')
  ```
  - **Source/Rationale**:
  - [Decentralized Clinical Trials (DCTs) have demonstrated potential for significant cost reductions](../references.qmd#dct-cost-reductions-evidence) (20-50.0% or more) through reduced site management, travel, and streamlined data collection.
  - The [UK RECOVERY trial achieved cost reductions of ~80-98% per patient](../references.qmd#recovery-trial-cost-reduction) compared to traditional trials. The US-based [ADAPTABLE trial](https://pcornet.org/clinical-research/pcornet-clinical-trials-demonstrations/adaptable/) ({{< var adaptable_trial_cost_per_patient >}}/patient) demonstrates similar efficiencies are achievable outside NHS infrastructure and emergency conditions.
  - _Note on R&D Savings Estimates_: While specific trials like RECOVERY showcase transformative cost-saving potential (>95%), these results benefited from NHS infrastructure and COVID-19 emergency conditions. ADAPTABLE provides a more typical benchmark (~98% savings vs. traditional trials). The average quantifiable cost reduction across the full spectrum of decentralized trials is an area of ongoing research and varies significantly based on trial complexity, therapeutic area, and the extent of decentralization. The scenarios below therefore present a range, with the "Transformative" scenario reflecting exceptional, RECOVERY-like outcomes.
  ```
  - [ ] Reviewed

- **Line 617** (matched '`recovery trial cost`')
  ```
  - [DCT Cost Reductions Evidence](../references.qmd#dct-cost-reductions-evidence)
- [Clinical Trial Market Size](../references.qmd#clinical-trial-market-size)
- [RECOVERY Trial Cost Reduction](../references.qmd#recovery-trial-cost-reduction)

## ROI Analysis for a Decentralized Framework
  ```
  - [ ] Reviewed

- **Line 780** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - Tufts Center for the Study of Drug Development often cited for \$1.0 - \$2.6 billion/drug.
   - Journal articles and industry reports (IQVIA, Deloitte) also highlight \$2+ billion figures.
   - Oxford RECOVERY trial: {{< var recovery_trial_cost_per_patient >}}/patient (exceptional NHS/COVID conditions). ADAPTABLE trial: {{< var adaptable_trial_cost_per_patient >}}/patient (typical US pragmatic trial). Our projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on ADAPTABLE; confidence interval captures uncertainty.

2. **ROI Calculation Method**:
  ```
  - [ ] Reviewed

- **Line 883** (matched '`cost per patient`')
  ```
  - Let $x$ be the number of patients in a given trial.
   - **Traditional cost per patient**: $c_{t}$.
   - **Decentralized cost per patient**: $c_{d}$, where $c_{d} \ll c_{t}$.
  ```
  - [ ] Reviewed

- **Line 884** (matched '`cost per patient`')
  ```
  - Let $x$ be the number of patients in a given trial.
   - **Traditional cost per patient**: $c_{t}$.
   - **Decentralized cost per patient**: $c_{d}$, where $c_{d} \ll c_{t}$.

   Therefore, the total cost for a single trial of size $x$ is:
  ```
  - [ ] Reviewed

- **Line 1327** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  | **Generic Drug Substitution**          |       **+**<a href="#ref_dominant">³</a>       | **Dominant** (Cost-Saving)                              | **Dominant**                     | By definition cost-saving when therapeutic equivalence is maintained, with typical savings of 30-80% versus brand-name drugs. ([WHO, 2015](../references.qmd#who-generic-drug-policy))                                                        |
| **Statins / Polypill**                 |         **67+**<a href="#ref_dominant">³</a>         | Cost-Saving to **~$15,000**                             | Dominant / Highly Cost-Effective | Cost-saving in high-risk populations. ICERs range from dominant to $15k/QALY in lower-risk groups. ([eClinicalMedicine, 2022](../references.qmd#eclinicalmedicine-statins-polypill))                                               |
| **Pragmatic Trials (RECOVERY model)** | **~250,000** | **{{< var pragmatic_trial_cost_per_qaly >}}/QALY** | Highly Cost-Effective | UK RECOVERY trial: {{< var recovery_trial_total_cost >}} spent, saving {{< var recovery_trial_global_lives_saved >}} globally via dexamethasone discovery. {{< var pragmatic_vs_nih_efficiency_multiplier >}} more efficient than standard research. (Note: RECOVERY's {{< var recovery_trial_cost_per_patient >}}/patient benefited from NHS infrastructure; ADAPTABLE achieved {{< var adaptable_trial_cost_per_patient >}}/patient in US settings.) |
| **NIH Standard Research Portfolio** | **~20** | **{{< var nih_standard_research_cost_per_qaly >}}/QALY** | Inefficient Baseline | Standard NIH-funded research. Represents current status quo efficiency. {{< var nih_standard_research_cost_per_qaly_cite >}} |
  ```
  - [ ] Reviewed

## knowledge/appendix/dfda-spec-paper.qmd

- **Line 51** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **Stage 1 (Signal Detection)**: Aggregated N-of-1 observational analysis [@duan-2013-n-of-1; @lillie-2011-n-of-1] integrates data from millions of individual longitudinal natural experiments. The methodology applies temporal precedence analysis with automated hyperparameter optimization, addresses six of nine Bradford Hill causality criteria through a composite Predictor Impact Score (PIS), and produces ranked treatment-outcome hypotheses at ~$0.10 per patient.

**Stage 2 (Causal Confirmation)**: High-priority signals (top 0.1-1% by PIS) proceed to pragmatic randomized trials following the RECOVERY/ADAPTABLE model [@recovery-trial-efficiency; @pragmatic-trials-cost-advantage]. Simple randomization embedded in routine care confirms causation at ~{{< var recovery_trial_cost_per_patient >}} per patient ({{< var recovery_trial_cost_reduction_factor >}} cheaper than traditional Phase III trials) while eliminating confounding concerns inherent in observational data.

The complete methodology includes: (1) data collection from heterogeneous sources; (2) temporal alignment with onset delay optimization; (3) within-subject baseline/follow-up comparison; (4) Predictor Impact Score calculation operationalizing Bradford Hill criteria; (5) Trial Priority Score for signal-to-trial prioritization; (6) pragmatic trial protocols for causal confirmation; and (7) validated outcome label generation with evidence grades.
  ```
  - [ ] Reviewed

- **Line 1322** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  |-------|--------|------|---------|--------|
| **Stage 1: Signal Detection** | Aggregated N-of-1 observational analysis | ~$0.10/patient | Hypothesis generation | Ranked PIS signals |
| **Stage 2: Causal Confirmation** | Pragmatic randomized trials | ~{{< var recovery_trial_cost_per_patient >}}/patient | Causation proof | Validated effect sizes |

This design leverages the complementary strengths of each approach:
  ```
  - [ ] Reviewed

- **Line 1335** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  | Dimension | Traditional Phase III | Pragmatic Trial (RECOVERY Model) |
|-----------|----------------------|----------------------------------|
| **Cost per patient** | {{< var traditional_phase3_cost_per_patient >}} | {{< var recovery_trial_cost_per_patient >}} |
| **Time to results** | 3-7 years | 3-6 months |
| **Patient population** | Homogeneous (strict exclusion) | Real-world (minimal exclusion) |
  ```
  - [ ] Reviewed

- **Line 1377** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  Data collection: Baseline characteristics (EHR), outcome at 90 days (patient-reported or EHR)
Sample size: 2,000 patients (1,000 per arm)
Cost: ~$1M total ({{< var recovery_trial_cost_per_patient >}}/patient)

Timeline: 6-12 months
  ```
  - [ ] Reviewed

- **Line 2008** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  1. **Stage 1: Scalable signal detection**: Aggregated N-of-1 observational analysis processes millions of treatment-outcome pairs at ~$0.10/patient, generating ranked hypotheses through the Predictor Impact Score
2. **Stage 2: Causal confirmation**: Pragmatic randomized trials following the RECOVERY/ADAPTABLE model confirm top signals at ~{{< var recovery_trial_cost_per_patient >}}/patient ({{< var recovery_trial_cost_reduction_factor >}} cheaper than traditional trials) while eliminating confounding
3. **Bradford Hill operationalization**: Six of nine causality criteria quantified in composite scoring system
4. **Trial Priority Score**: Principled prioritization of which signals warrant experimental confirmation
  ```
  - [ ] Reviewed

## knowledge/appendix/dih-integration-model.qmd

- **Line 135** (matched '`cost per patient`')
  ```
  - Data collection: $10/month (automated)

**Total trial fund cost per patient:** $310-2,510/month (decentralized model eliminates travel costs)
**Traditional trial cost per patient:** [$6,800-13,600/month](../references.qmd#trial-costs-fda-study)
  ```
  - [ ] Reviewed

- **Line 136** (matched '`cost per patient`')
  ```
  **Total trial fund cost per patient:** $310-2,510/month (decentralized model eliminates travel costs)
**Traditional trial cost per patient:** [$6,800-13,600/month](../references.qmd#trial-costs-fda-study)

#### Efficiency gain: 75-80% cost reduction
  ```
  - [ ] Reviewed

## knowledge/appendix/drug-development-cost-analysis.qmd

- **Line 133** (matched '`cost per patient`')
  ```
  - Hospital-integrated data collection
- Minimal regulatory burden
- Cost per patient: ~$50

**Post-1962 (typical FDA Phase III):**
  ```
  - [ ] Reviewed

- **Line 140** (matched '`cost per patient`')
  ```
  - Separate CRO infrastructure
- Extensive monitoring and auditing
- Cost per patient: ~$4,100

See [Regulatory Mortality Analysis](../appendix/regulatory-mortality-analysis.qmd) for full derivation.
  ```
  - [ ] Reviewed

- **Line 375** (matched '`cost per patient`')
  ```
  **Orphan drugs reveal the full {{< var drug_cost_increase_pre1962_to_current_multiplier >}} cost burden** because small patient populations (~200,000 or fewer in the US) mean development costs cannot be spread across many sales:

| Drug | Annual Cost per Patient | Comparable Non-Orphan Alternative | Ratio |
|------|------------------------|-----------------------------------|-------|
| **Zolgensma** (spinal muscular atrophy) | $'{python} f"{zolgensma_price:,.0f}"' (one-time) | Supportive care: $'{python} f"{zolgensma_supportive_care_low:,.0f}"'-'{python} f"{zolgensma_supportive_care_high:,.0f}"'/year | **'{python} f"{zolgensma_ratio_low:.0f}"'-'{python} f"{zolgensma_ratio_high:.0f}"'×** |
  ```
  - [ ] Reviewed

- **Line 515** (matched '`cost per patient`')
  ```
  The [RECOVERY trial](../appendix/recovery-trial.qmd) demonstrated that **simple randomization** can:

- Reduce cost per patient by **{{< var recovery_trial_cost_reduction_factor >}}×**
- Maintain scientific rigor
- Accelerate results (6 months vs. 5+ years)
  ```
  - [ ] Reviewed

## knowledge/appendix/economic-value-of-accelerated-treatments.qmd

- **Line 55** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  ## **Conclusion**

Increasing trial capacity by {{< var dfda_trial_capacity_multiplier >}}× through lower-cost decentralized trials (RECOVERY: {{< var recovery_trial_cost_per_patient >}}/patient vs {{< var traditional_phase3_cost_per_patient >}} traditional) enables testing far more treatments simultaneously. While market dynamics and system capacities are important considerations, the potential economic and societal impacts underscore the transformative value of advancing medical innovation.

## **Sources**
  ```
  - [ ] Reviewed

## knowledge/appendix/faq.qmd

- **Line 15** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **Objection**: "Nice idea, but it likely won't happen."

**Response**: The Oxford RECOVERY trial tested 7 treatments in 6 months, saved 1 million lives, and cost {{< var recovery_trial_cost_per_patient >}} per patient. The FDA's equivalent costs {{< var traditional_phase3_cost_per_patient >}} per patient, which is approximately the price of a luxury car per question about whether aspirin works.

The trial used existing hospital systems. Hospitals, it turns out, already contain sick people.
  ```
  - [ ] Reviewed

- **Line 447** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **Objection**: "How do you ensure money helps patients instead of funding bureaucracy?"

**Response**: The [decentralized framework for drug assessment](../solution/dfda.qmd) model achieves [80× lower cost per patient](../references.qmd#recovery-trial-82x-cost-reduction). Pragmatic trials cost {{< var recovery_trial_cost_per_patient >}} [per patient](../references.qmd#recovery-cost-500) versus {{< var traditional_phase3_cost_per_patient >}} in [traditional trials](../references.qmd#trial-cost-41k).

The NIH's RECOVER initiative spent $1.6B for zero completed trials in 4 years. With that budget, this model could run 2,800 trials for 2.8 million patients. Evidence is strong.
  ```
  - [ ] Reviewed

## knowledge/appendix/fundraising-strategy.qmd

- **Line 576** (matched '`cost per patient`')
  ```
  "The initiative advocates for the creation of a 1% Treaty Fund (a {{< var treaty_annual_funding >}} annually decentralized treasury) using proven DAO models from MakerDAO/Uniswap. We advocate for a governance model where future government-issued VICTORY Incentive Alignment Bond holders, alongside public health experts, provide input on the allocation of this treasury across pragmatic clinical trials and other global health initiatives.

This isn't just an investment - it's a chance to influence the direction of more capital than the NIH budget toward curing diseases through [80X lower cost per patient](../references.qmd#recovery-trial-82x-cost-reduction) decentralized trials."

#### Template 2: Health Billionaires (Industry Advantage)
  ```
  - [ ] Reviewed

## knowledge/appendix/global-clinical-trial-spending-by-phase.qmd

- **Line 87** (matched '`cost per patient`')
  ```
  - Range by therapeutic area: [$11.5M (dermatology) to $52.9M (pain/anesthesia)](../references.qmd#phase-3-therapeutic-area-costs)

#### Cost per patient

- Traditional Phase 3: {{< var traditional_phase3_cost_per_patient >}} per patient
  ```
  - [ ] Reviewed

- **Line 89** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  #### Cost per patient

- Traditional Phase 3: {{< var traditional_phase3_cost_per_patient >}} per patient
- Average: [$113,000 per patient](../references.qmd#phase-3-cost-per-patient-113k)
  ```
  - [ ] Reviewed

- **Line 105** (matched '`cost per patient`')
  ```
  - Range by therapeutic area: [$7.0M (cardiovascular) to $19.6M (hematology)](../references.qmd#phase-2-therapeutic-area-costs)

#### Cost per patient

- Average: [$130,000 per patient](../references.qmd#phase-2-cost-per-patient-130k)
  ```
  - [ ] Reviewed

- **Line 127** (matched '`cost per patient`')
  ```
  - Typical: [$25 million](../references.qmd#phase-1-cost-typical) per trial

#### Cost per patient

- Average: [$137,000 per patient](../references.qmd#phase-1-cost-per-patient-137k) (highest per-patient cost!)
  ```
  - [ ] Reviewed

- **Line 376** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - [Industry spending grew 44% (2012-2022)](../references.qmd#industry-rd-growth-2012-2022)
- More trials running globally than ever
- Technology enabling cheaper trials (see: RECOVERY trial at {{< var recovery_trial_cost_per_patient >}}/patient)

#### The Bad News
  ```
  - [ ] Reviewed

- **Line 404** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **What the same money could buy (with a decentralized framework for drug assessment):**

- At {{< var recovery_trial_cost_per_patient >}}/patient (RECOVERY model): **120 million patient-participants**
- At $2 million per efficient trial: **30,000 trials annually**
- Instead of 50 drugs: **Hundreds or thousands of treatments tested**
  ```
  - [ ] Reviewed

- **Line 411** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  #### The waste

- Traditional Phase 3: {{< var traditional_phase3_cost_per_patient >}} per patient
- RECOVERY achieved: {{< var recovery_trial_cost_per_patient >}} per patient
- **That's an 80-240× markup for bureaucracy**
  ```
  - [ ] Reviewed

- **Line 412** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - Traditional Phase 3: {{< var traditional_phase3_cost_per_patient >}} per patient
- RECOVERY achieved: {{< var recovery_trial_cost_per_patient >}} per patient
- **That's an 80-240× markup for bureaucracy**
  ```
  - [ ] Reviewed

## knowledge/appendix/legal-compliance-framework.qmd

- **Line 346** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  #### Projected Impact

- Support 61+ million participants annually (\$30.6B ÷ {{< var recovery_trial_cost_per_patient >}} per participant)
- Potential for 160+ million participants with Medicare/Medicaid integration
- Trillions in global healthcare savings
  ```
  - [ ] Reviewed

## knowledge/appendix/recovery-trial.qmd

- **Line 19** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  The Oxford RECOVERY trial isn't theory, it's proof. In 2020, while [traditional trials](../references.qmd#trial-cost-41k) cost {{< var traditional_phase3_cost_per_patient >}} per patient, Oxford spent {{< var recovery_trial_cost_per_patient >}} per patient and [saved over 1 million lives globally](../references.qmd#recovery-trial-1m-lives-saved). This {{< var recovery_trial_cost_reduction_factor >}}× efficiency gain demonstrates that decentralized, pragmatic trials aren't just possible, they're already superior to centralized FDA approaches.

**Speed to Launch:** [9 days from conception to first patient enrolled](../references.qmd#landray-recovery-trial-quote). FDA average: [6-12 months](../references.qmd#fda-trial-launch-timeline).
  ```
  - [ ] Reviewed

- **Line 32** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  | Participating Hospitals            | 186                                                                                                                               | [RECOVERY Trial Website](https://www.recoverytrial.net/)                                                                                                                                |
| Total Trial Cost                   | £2.1M (~$2.7M)                                                                                                                    | [UKRI Impact Report](https://www.ukri.org/who-we-are/how-we-are-doing/research-outcomes-and-impact/mrc/recovery-trial-identifies-covid-19-treatments/)                                  |
| Cost per Patient                   | ~{{< var recovery_trial_cost_per_patient >}} ([Manhattan Institute](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)) | [Manhattan Institute](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)                                                               | 
| Traditional Trial Cost per Patient | ~{{< var traditional_phase3_cost_per_patient >}}                                                                                                                          | [NCBI](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7295430/)                                                                                                                           |
| Treatments Evaluated               | 12                                                                                                                                | [RECOVERY Results](https://www.recoverytrial.net/results)                                                                                                                               |
  ```
  - [ ] Reviewed

- **Line 33** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  | Total Trial Cost                   | £2.1M (~$2.7M)                                                                                                                    | [UKRI Impact Report](https://www.ukri.org/who-we-are/how-we-are-doing/research-outcomes-and-impact/mrc/recovery-trial-identifies-covid-19-treatments/)                                  |
| Cost per Patient                   | ~{{< var recovery_trial_cost_per_patient >}} ([Manhattan Institute](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)) | [Manhattan Institute](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)                                                               | 
| Traditional Trial Cost per Patient | ~{{< var traditional_phase3_cost_per_patient >}}                                                                                                                          | [NCBI](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7295430/)                                                                                                                           |
| Treatments Evaluated               | 12                                                                                                                                | [RECOVERY Results](https://www.recoverytrial.net/results)                                                                                                                               |
| Cost per Intervention              | ~£175,000 (~$223,000)                                                                                                             | Calculated (£2.1M ÷ 12 treatments)                                                                                                                                                      |
  ```
  - [ ] Reviewed

- **Line 77** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  #### The Result

{{< var recovery_trial_cost_per_patient >}} per patient ([Manhattan Institute](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)) vs FDA's {{< var traditional_phase3_cost_per_patient >}} per patient ([NCBI](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7295430/)).

That's an {{< var recovery_trial_cost_reduction_factor >}}× efficiency gain achieved by doing the obvious things in obvious ways.
  ```
  - [ ] Reviewed

- **Line 124** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  4. **Cost Efficiency**
   The actual cost of £2.1M (~$2.7M) for the entire trial represents an even more dramatic efficiency than previously estimated. While a simple division yields approximately £43 (~$55) per patient, authoritative sources cite ~{{< var recovery_trial_cost_per_patient >}} per patient as a more realistic figure ([Manhattan Institute](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)). This is nearly 80 times more cost-efficient than traditional clinical trials ([NCBI](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7295430/): {{< var traditional_phase3_cost_per_patient >}} per patient). This extraordinary cost-effectiveness, combined with the rapid delivery of results (three major findings within 100 days) and estimated global impact of over 1 million lives saved, demonstrates the revolutionary nature of the RECOVERY trial model.

## Proof This Isn't Insane
  ```
  - [ ] Reviewed

- **Line 136** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  ### The Oxford RECOVERY Trial

**{{< var recovery_trial_cost_per_patient >}} vs FDA's {{< var traditional_phase3_cost_per_patient >}} Per Patient**

The UK spent {{< var recovery_trial_cost_per_patient >}} per patient testing COVID treatments. Saved a million lives.
  ```
  - [ ] Reviewed

- **Line 138** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **{{< var recovery_trial_cost_per_patient >}} vs FDA's {{< var traditional_phase3_cost_per_patient >}} Per Patient**

The UK spent {{< var recovery_trial_cost_per_patient >}} per patient testing COVID treatments. Saved a million lives.

The U.S. equivalent often costs {{< var traditional_phase3_cost_per_patient >}} per patient, with a significant portion dedicated to extensive regulatory paperwork.
  ```
  - [ ] Reviewed

- **Line 140** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  The UK spent {{< var recovery_trial_cost_per_patient >}} per patient testing COVID treatments. Saved a million lives.

The U.S. equivalent often costs {{< var traditional_phase3_cost_per_patient >}} per patient, with a significant portion dedicated to extensive regulatory paperwork.

### The Math
  ```
  - [ ] Reviewed

## knowledge/appendix/right-to-trial-fda-upgrade-act.qmd

- **Line 46** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  1. New, effective treatments take an average of **17 years** to transition from scientific discovery to clinical practice, a delay during which millions of patients suffer without access to potential cures.
2. The current clinical trial paradigm is profoundly inefficient and exclusionary.
   (A) Median per‑patient cost for a phase‑3 drug trial in 2024 exceeded **{{< var traditional_phase3_cost_per_patient >}}**\[2], inflating drug prices and limiting R‑&‑D on unpatentable therapies.
   (B) Up to **86.1 percent of patients** are excluded from participating in pivotal trials, limiting the generalizability of findings to real-world patient populations.
   (C) The failure to publish negative results leads to redundant research, while rigid trial designs that cannot adapt to incoming data stifle innovation.
  ```
  - [ ] Reviewed

- **Line 52** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  3. As a consequence of these systemic failures, an estimated **95 percent of rare diseases lack a single FDA-approved treatment**, and effective therapies for common conditions remain undiscovered or inaccessible.
4. The U.K. **RECOVERY** pragmatic trial enrolled 49,000 patients in 100 days at roughly **{{< var recovery_trial_cost_per_patient >}} per patient**\[3], demonstrating that a decentralized, adaptive model can reduce the non-biologic operational costs of clinical research by over **90 percent** through automation of data management, monitoring, and administrative functions.
5. The strategic application of artificial intelligence in healthcare has the potential to yield substantial economic benefits, with studies indicating that AI could reduce national healthcare spending by 5 to 10 percent annually by optimizing diagnostics, personalizing treatments, and improving the efficiency of health-related research and development.
6. Publicly financed, algorithm-targeted discounts on patient-borne trial participation costs, aimed at maximizing **quality‑adjusted life‑years (QALYs) per federal dollar**, can enhance access to trials, with patients covering the net costs of their participation. Funding for these subsidies can be sourced through innovative mechanisms like [a decentralized institutes of health (DIH)](../solution/dih.qmd), a global treasury that raises capital by issuing bonds and is repaid by nations participating in a global health treaty.
  ```
  - [ ] Reviewed

## knowledge/economics/economics.qmd

- **Line 85** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  :::

**How the {{< var dfda_trial_capacity_multiplier >}}× capacity increase works:** Redirecting {{< var treaty_annual_funding >}}/year at {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient (based on ADAPTABLE trial; RECOVERY achieved {{< var recovery_trial_cost_per_patient >}}/patient under exceptional NHS/COVID conditions) enables {{< var dih_patients_fundable_annually >}} annual trial participants vs. current {{< var current_trial_slots_available >}}, increasing trial completion rate from {{< var new_disease_first_treatments_per_year >}} to {{< var dfda_first_treatments_per_year >}} diseases/year. This removes the primary bottleneck to medical progress: currently less than {{< var current_clinical_trial_participation_rate >}} of willing patients can access trials, and over {{< var safe_compounds_count >}} proven-safe compounds (FDA-approved drugs + GRAS substances) remain untested for most conditions they could improve.

**Robustness**: Even at {{< var political_success_probability >}} probability of adoption, risk-adjusted cost-effectiveness ({{< var treaty_expected_cost_per_daly >}}/DALY) remains {{< var treaty_expected_vs_bed_nets_multiplier >}}× better than bed nets. Monte Carlo simulation across 10,000 trials indicates the intervention remains cost-saving across the sensitivity ranges explored here.
  ```
  - [ ] Reviewed

- **Line 141** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  | **Trial participation rate** | {{< var current_clinical_trial_participation_rate >}} of willing patients | Massive unmet research capacity [@clinical-trial-patient-participation-rate] |
| **Untested safe compounds** | {{< var safe_compounds_count >}} proven-safe (FDA-approved drugs + GRAS) | {{< var exploration_ratio >}} of drug-disease space explored [@drug-repurposing-rate] |
| **Traditional trial cost** | {{< var traditional_phase3_cost_per_patient >}}/patient | Makes comprehensive testing economically infeasible {{< var traditional_phase3_cost_per_patient_cite >}} |
| **Pragmatic trial cost** | {{< var recovery_trial_cost_per_patient >}}/patient (RECOVERY) | {{< var recovery_trial_cost_reduction_factor >}}× cost reduction enables systematic exploration {{< var recovery_trial_cost_per_patient_cite >}} |
  ```
  - [ ] Reviewed

- **Line 142** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  | **Untested safe compounds** | {{< var safe_compounds_count >}} proven-safe (FDA-approved drugs + GRAS) | {{< var exploration_ratio >}} of drug-disease space explored [@drug-repurposing-rate] |
| **Traditional trial cost** | {{< var traditional_phase3_cost_per_patient >}}/patient | Makes comprehensive testing economically infeasible {{< var traditional_phase3_cost_per_patient_cite >}} |
| **Pragmatic trial cost** | {{< var recovery_trial_cost_per_patient >}}/patient (RECOVERY) | {{< var recovery_trial_cost_reduction_factor >}}× cost reduction enables systematic exploration {{< var recovery_trial_cost_per_patient_cite >}} |

The Oxford RECOVERY trial demonstrated that pragmatic trial design can maintain scientific rigor while delivering results in <100 days [@recovery-trial-82x-cost-reduction]. This {{< var recovery_trial_cost_reduction_factor >}}× cost reduction transforms the economics of medical research: what was previously too expensive to test becomes systematically explorable.
  ```
  - [ ] Reviewed

- **Line 153** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  1. **Empirical grounding**: Cost estimates based on demonstrated pragmatic trial results, not theoretical projections. Our projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on the ADAPTABLE trial. (RECOVERY achieved {{< var recovery_trial_cost_per_patient >}}/patient under exceptional NHS/COVID conditions; confidence interval captures this range.)

2. **Decentralized execution**: Unlike centralized megaprojects vulnerable to corruption and bureaucratic failure, pragmatic trials distribute decision-making across thousands of physicians and millions of patients. No single point of failure.
  ```
  - [ ] Reviewed

- **Line 246** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  The bottleneck isn't basic research or laboratory science. It's **clinical trials**. We've tested {{< var exploration_ratio >}} of [possible drug-disease combinations](../problem/untapped-therapeutic-frontier.qmd) using existing safe compounds. Not because the science is impossible, but because traditional trials cost {{< var traditional_phase3_cost_per_patient >}} per patient while pragmatic trials like Oxford RECOVERY run for {{< var recovery_trial_cost_per_patient >}} per patient. At current funding levels, testing the remaining {{< var unexplored_ratio >}} of therapeutic space would take millennia. Meanwhile, military budgets dwarf the funding needed to automate ubiquitous clinical trials and systematically explore what actually helps people.

{{< include ../figures/military-vs-medical-research-spending-column-chart.qmd >}}
  ```
  - [ ] Reviewed

- **Line 286** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  The mechanism is financial, not bureaucratic:

1. **Patient subsidies**: Most treaty funding ({{< var dih_treasury_trial_subsidies_annual >}}) goes directly to subsidizing patient participation in trials at ~{{< var dfda_pragmatic_trial_cost_per_patient >}} {{< var dfda_pragmatic_trial_cost_per_patient_cite >}} per patient, similar to how insurance covers medical procedures
2. **Providers get paid**: Treatment providers can charge for patient participation in trials, making trials profitable rather than costly
3. **Easy enrollment**: A decentralized framework for drug assessment infrastructure (costing just {{< var dfda_annual_opex >}}) makes it easy for anyone to create or join Phase 2/3/4 trials globally
  ```
  - [ ] Reviewed

- **Line 301** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  ### Trial Cost Reduction

Traditional FDA Phase 3 trials cost {{< var traditional_phase3_cost_per_patient >}} {{< var traditional_phase3_cost_per_patient_cite >}} per patient because they require dedicated infrastructure: specialized research sites, dedicated research coordinators, custom data collection systems, patient travel reimbursement, and extensive monitoring visits. This overhead exists independent of the actual treatment being tested.

The Oxford RECOVERY trial demonstrated an alternative: leverage existing hospital infrastructure, collect only incremental data beyond standard medical records, and integrate evidence generation into routine clinical care. Cost: {{< var recovery_trial_cost_per_patient >}} {{< var recovery_trial_cost_per_patient_cite >}} per patient. While RECOVERY's exceptional efficiency benefited from NHS infrastructure and COVID emergency conditions, a review of 64 embedded pragmatic clinical trials found a median cost of **$97 per patient** [@programs-barriers-pragmatic-embedded-trials-pmc], confirming that order-of-magnitude cost reductions are replicable. (Our conservative dFDA projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on the ADAPTABLE trial.) Same quality evidence. {{< var recovery_trial_cost_reduction_factor >}} lower cost.
  ```
  - [ ] Reviewed

- **Line 303** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  Traditional FDA Phase 3 trials cost {{< var traditional_phase3_cost_per_patient >}} {{< var traditional_phase3_cost_per_patient_cite >}} per patient because they require dedicated infrastructure: specialized research sites, dedicated research coordinators, custom data collection systems, patient travel reimbursement, and extensive monitoring visits. This overhead exists independent of the actual treatment being tested.

The Oxford RECOVERY trial demonstrated an alternative: leverage existing hospital infrastructure, collect only incremental data beyond standard medical records, and integrate evidence generation into routine clinical care. Cost: {{< var recovery_trial_cost_per_patient >}} {{< var recovery_trial_cost_per_patient_cite >}} per patient. While RECOVERY's exceptional efficiency benefited from NHS infrastructure and COVID emergency conditions, a review of 64 embedded pragmatic clinical trials found a median cost of **$97 per patient** [@programs-barriers-pragmatic-embedded-trials-pmc], confirming that order-of-magnitude cost reductions are replicable. (Our conservative dFDA projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on the ADAPTABLE trial.) Same quality evidence. {{< var recovery_trial_cost_reduction_factor >}} lower cost.

**Concrete example**: A hospital already tracks patient lab results, symptoms, and outcomes in electronic health records. Traditional trials build a parallel research infrastructure to collect the same information again. Pragmatic trials simply flag which patients are enrolled and automatically extract relevant data from existing systems. No duplicate infrastructure, no dedicated research staff per trial.
  ```
  - [ ] Reviewed

- **Line 611** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  **Insurance Companies**: Healthier populations generate higher lifetime premium revenue. Patients living longer with better health outcomes produce better actuarial performance than the current mortality-driven model.

**Pharmaceutical Companies**: Trial costs convert to revenue streams. Instead of paying {{< var traditional_phase3_cost_per_patient >}} {{< var traditional_phase3_cost_per_patient_cite >}} per trial patient, companies collect {{< var dfda_pragmatic_trial_cost_per_patient >}} {{< var dfda_pragmatic_trial_cost_per_patient_cite >}} subsidies when patients enroll. This transforms trials from cost centers to profit centers.

**Politicians**: {{< var treaty_campaign_voting_bloc_target >}} million voters represent a significant electoral constituency. Politicians supporting the treaty gain reputation benefits, campaign support, and reduced opposition funding. Those opposing it face well-funded challengers and organized voter blocs.
  ```
  - [ ] Reviewed

- **Line 737** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **2. Trial cost reduction through infrastructure efficiency**

Traditional FDA Phase 3 trials cost {{< var traditional_phase3_cost_per_patient >}} {{< var traditional_phase3_cost_per_patient_cite >}} per patient due to site setup costs, dedicated research staff, patient travel reimbursement, custom case report forms, and extensive monitoring requirements. The Oxford RECOVERY trial cost {{< var recovery_trial_cost_per_patient >}} {{< var recovery_trial_cost_per_patient_cite >}} per patient by using existing hospital infrastructure, minimal additional data collection beyond standard care, and simplified consent processes.

This represents an {{< var recovery_trial_cost_reduction_factor >}}× cost reduction achieved by eliminating duplicative overhead and leveraging existing healthcare infrastructure.
  ```
  - [ ] Reviewed

- **Line 973** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - Treaty redirects {{< var treaty_annual_funding >}}/year
- Trial subsidies allocation: {{< var dih_treasury_trial_subsidies_annual >}} (after IAB and political allocations)
- Pragmatic trial cost: {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient (ADAPTABLE basis; RECOVERY achieved {{< var recovery_trial_cost_per_patient >}})

**Step 2: Compare to current capacity**
  ```
  - [ ] Reviewed

- **Line 1477** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  #### Empirical basis

- Oxford RECOVERY trial: {{< var recovery_trial_cost_reduction_factor >}}× cost reduction ({{< var recovery_trial_cost_per_patient >}} per patient vs. {{< var traditional_phase3_cost_per_patient >}} traditional). Note: RECOVERY benefited from NHS infrastructure and COVID emergency conditions.
- ADAPTABLE trial: {{< var adaptable_trial_total_cost >}} / {{< var adaptable_trial_patients >}} = {{< var adaptable_trial_cost_per_patient >}}/patient using PCORnet pragmatic design, more representative of typical pragmatic trial costs.
- Our dFDA projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on ADAPTABLE. Confidence interval ($500-$3,000) captures range from RECOVERY-like efficiency to complex chronic disease trials.
  ```
  - [ ] Reviewed

- **Line 1478** (matched '`ADAPTABLE_TRIAL_COST_PER_PATIENT`')
  ```
  - Oxford RECOVERY trial: {{< var recovery_trial_cost_reduction_factor >}}× cost reduction ({{< var recovery_trial_cost_per_patient >}} per patient vs. {{< var traditional_phase3_cost_per_patient >}} traditional). Note: RECOVERY benefited from NHS infrastructure and COVID emergency conditions.
- ADAPTABLE trial: {{< var adaptable_trial_total_cost >}} / {{< var adaptable_trial_patients >}} = {{< var adaptable_trial_cost_per_patient >}}/patient using PCORnet pragmatic design, more representative of typical pragmatic trial costs.
- Our dFDA projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on ADAPTABLE. Confidence interval ($500-$3,000) captures range from RECOVERY-like efficiency to complex chronic disease trials.
- Literature on pragmatic trials consistently shows 50-95% cost reductions
  ```
  - [ ] Reviewed

- **Line 1479** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  - Oxford RECOVERY trial: {{< var recovery_trial_cost_reduction_factor >}}× cost reduction ({{< var recovery_trial_cost_per_patient >}} per patient vs. {{< var traditional_phase3_cost_per_patient >}} traditional). Note: RECOVERY benefited from NHS infrastructure and COVID emergency conditions.
- ADAPTABLE trial: {{< var adaptable_trial_total_cost >}} / {{< var adaptable_trial_patients >}} = {{< var adaptable_trial_cost_per_patient >}}/patient using PCORnet pragmatic design, more representative of typical pragmatic trial costs.
- Our dFDA projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on ADAPTABLE. Confidence interval ($500-$3,000) captures range from RECOVERY-like efficiency to complex chronic disease trials.
- Literature on pragmatic trials consistently shows 50-95% cost reductions
  ```
  - [ ] Reviewed

- **Line 1510** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  #### Implications for generalizability

The RECOVERY trial ({{< var recovery_trial_cost_per_patient >}} {{< var recovery_trial_cost_per_patient_cite >}} per patient) demonstrates that modern infrastructure enables even greater efficiency than the pre-1962 system. (Our dFDA projections use {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on the ADAPTABLE trial.) However, the fundamental approach, physicians testing treatments on real patients in clinical practice settings, has {{< var pre_1962_validation_years >}} of empirical validation (1883-1960), not merely one case study.

The cost reduction estimates are conservative relative to historical costs. 1980s drugs cost approximately {{< var drug_development_cost_1980s >}} [(compounded, 1990 dollars)](../references.qmd#pre-1962-drug-costs-timeline) compared to modern {{< var pharma_drug_development_cost_current >}} [costs](../references.qmd#pre-1962-drug-costs-timeline), representing a {{< var drug_cost_increase_1980s_to_current_multiplier >}}-fold increase. Modern technology (EHRs, wearables, automated data collection) suggests efficiency gains could exceed historical precedent while maintaining the safety protections that successfully prevented disasters like thalidomide.
  ```
  - [ ] Reviewed

- **Line 1672** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  1. **Patient Trial Subsidies** ({{< var dih_treasury_trial_subsidies_pct >}}): {{< var dih_treasury_trial_subsidies_annual >}}/year
   - Subsidizes {{< var dih_patients_fundable_annually >}} patients annually at {{< var dfda_pragmatic_trial_cost_per_patient >}} {{< var dfda_pragmatic_trial_cost_per_patient_cite >}} per patient
   - Patients bring subsidies to trials; providers collect payment when patients enroll
   - Makes trial participation profitable for providers instead of costly
  ```
  - [ ] Reviewed

- **Line 1746** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - **Standard NIH Portfolio:** {{< var nih_standard_research_cost_per_qaly >}}/QALY {{< var nih_standard_research_cost_per_qaly_cite >}}. Current research spending efficiency.
- **Pragmatic Trials:** {{< var pragmatic_trial_cost_per_qaly >}}/QALY. Calculated from RECOVERY trial's exceptional global impact ({{< var recovery_trial_total_cost >}} spent, {{< var recovery_trial_global_lives_saved >}} saved). Note: RECOVERY was an outlier with exceptional NHS infrastructure and COVID emergency conditions. Critics note this may not be representative of typical pragmatic trials. For operational cost projections, we use the more conservative {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient (2.4× higher than RECOVERY's {{< var recovery_trial_cost_per_patient >}}).

**Efficiency gap:** {{< var pragmatic_vs_nih_efficiency_multiplier >}}. Even using RECOVERY's exceptional results, the gap demonstrates pragmatic trials' transformative potential.
  ```
  - [ ] Reviewed

- **Line 1793** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  1. **Patient Trial Subsidies**: {{< var dih_treasury_trial_subsidies_annual >}}/year subsidizing patient participation in clinical trials
   - At {{< var dfda_pragmatic_trial_cost_per_patient >}} {{< var dfda_pragmatic_trial_cost_per_patient_cite >}} per patient ([pragmatic trial cost](../appendix/recovery-trial.qmd)), this funds {{< var dih_patients_fundable_annually >}} patients annually
   - Patients choose which trials to join; trials that attract patients get funded
   - **ALL remaining funds go to patient subsidies** - no separate bureaucracy or overhead budget
  ```
  - [ ] Reviewed

- **Line 1882** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  **How the {{< var dfda_trial_capacity_multiplier >}}× Multiplier Works**:

The acceleration comes from simple economics: The 1% Treaty Fund can fund {{< var dih_patients_fundable_annually >}} patients/year at [pragmatic trial cost](../references.qmd#pragmatic-trials-cost-advantage) ({{< var dfda_pragmatic_trial_cost_per_patient >}}/patient based on ADAPTABLE trial), compared to [current global trial participation](../references.qmd#global-trial-participant-capacity) of {{< var current_trial_slots_available >}} patients/year (IQVIA 2022).

{{< var dfda_trial_capacity_multiplier_latex >}}
  ```
  - [ ] Reviewed

- **Line 1892** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - {{< var dfda_trial_capacity_multiplier >}}× more completed trials/year
- From [50 drug approvals/year](../references.qmd#global-new-drug-approvals-50-annually) → proportionally more approvals
- From {{< var traditional_phase3_cost_per_patient >}} [cost per patient](../appendix/recovery-trial.qmd) → {{< var dfda_pragmatic_trial_cost_per_patient >}} cost per patient (using conservative ADAPTABLE-based estimate; RECOVERY achieved {{< var recovery_trial_cost_per_patient >}} under exceptional conditions)
  ```
  - [ ] Reviewed

- **Line 2223** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **What RECOVERY demonstrates vs. what the base estimate assumes:**

The RECOVERY trial proves two things: (1) pragmatic trials can cost {{< var recovery_trial_cost_per_patient >}}/patient instead of {{< var traditional_phase3_cost_per_patient >}}, and (2) this approach can accelerate research dramatically (47,000 patients in 3 months).

Critically, **the base ROI estimate ({{< var dfda_roi_rd_only >}}) uses only the cost reduction**, not the acceleration effect. It assumes we run the same number of trials at lower cost, not 22× more trials. The 22× acceleration multiplier is excluded from conservative estimates precisely because it requires extrapolating RECOVERY's recruitment success across all disease areas. This provides substantial margin of safety against overgeneralization.
  ```
  - [ ] Reviewed

- **Line 2243** (matched '`cost per patient`')
  ```
  #### Why this critique may not apply

This intervention targets a different margin than traditional research scaling. Bloom et al. measure **idea productivity** (breakthroughs per researcher-year). Our intervention targets **trial execution efficiency** (cost per patient enrolled, completion rates, recruitment speed).

#### Distinction
  ```
  - [ ] Reviewed

- **Line 2254** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  The argument that medical research faces diminishing returns rests on a false premise: that we have already picked the "low-hanging fruit." In reality, we haven't picked the fruit because we can't afford the ladder.

High trial costs (median {{< var traditional_phase3_cost_per_patient >}} per patient) force researchers to bet only on "sure things," leaving the vast majority of the therapeutic map blank.

**1. The Immediate Opportunity (Existing Safe Drugs)**
  ```
  - [ ] Reviewed

- **Line 2432** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  1. **Data infrastructure scaling costs**: Decentralized trial infrastructure uses automated software (federated queries, not centralized databases), scaling through technology rather than labor. Unlike traditional research that faces researcher supply constraints, the system leverages existing EHR systems (Epic, Cerner) and adds coordination protocols. Marginal scaling costs are low relative to traditional models.

2. **Clinical trial market price effects**: Increasing trial demand by {{< var dfda_trial_capacity_multiplier >}}× could affect equilibrium prices for clinical research services. However, the pragmatic trial approach *reduces* per-trial costs ({{< var recovery_trial_cost_reduction_factor >}}× cheaper via automation), suggesting supply constraints may not bind. Traditional trials cost {{< var traditional_phase3_cost_per_patient >}} per patient; decentralized trials target {{< var dfda_pragmatic_trial_cost_per_patient >}} per patient by eliminating overhead, not by increasing demand for scarce inputs.

3. **Crowding out effects**: Do billions in new pragmatic clinical trials displace existing research funding, or does it add incrementally? Conservative assumption: fully additive. If partially substitutive (e.g., governments reduce NIH funding in response), net research increase would be lower than modeled.
  ```
  - [ ] Reviewed

- **Line 2542** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  - Technological breakthroughs

It requires only a 1% reallocation from the least cost-effective government spending (military) to the most cost-effective health intervention (pragmatic trials at {{< var dfda_pragmatic_trial_cost_per_patient >}}/patient).

The political challenge isn't economic: the ROI speaks for itself. The challenge is overcoming entrenched interests in military-industrial spending. The solution: [Incentive Alignment Bonds](../appendix/incentive-alignment-bonds-paper.qmd) that make supporting the treaty more profitable for politicians than opposing it.
  ```
  - [ ] Reviewed

- **Line 2578** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  While the treaty itself requires simultaneous adoption, individual nations or sub-national jurisdictions could demonstrate pragmatic trial feasibility:

- Oxford RECOVERY trial already proved {{< var recovery_trial_cost_per_patient >}}/patient cost ({{< var recovery_trial_cost_reduction_factor >}}× reduction) is achievable
- Nations could pilot expanded pragmatic trial systems domestically to demonstrate health and economic benefits
- This builds empirical evidence for treaty negotiations but is not a prerequisite
  ```
  - [ ] Reviewed

## knowledge/economics/health-dividend.qmd

- **Line 31** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  Here's the breakdown.

## The Math: From {{< var traditional_phase3_cost_per_patient >}} to {{< var recovery_trial_cost_per_patient >}} Per Patient

Traditional Phase III trials cost **{{< var traditional_phase3_cost_per_patient >}} per patient**. That's more than a Tesla per person to find out if a pill works. The pill costs 37 cents to make. The paperwork weighs more than the patient.
  ```
  - [ ] Reviewed

- **Line 33** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  ## The Math: From {{< var traditional_phase3_cost_per_patient >}} to {{< var recovery_trial_cost_per_patient >}} Per Patient

Traditional Phase III trials cost **{{< var traditional_phase3_cost_per_patient >}} per patient**. That's more than a Tesla per person to find out if a pill works. The pill costs 37 cents to make. The paperwork weighs more than the patient.

The Oxford RECOVERY trial proved humans can do the same thing for **{{< var recovery_trial_cost_per_patient >}} per patient**. They tested COVID treatments on 40,000+ patients by:
  ```
  - [ ] Reviewed

- **Line 35** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  Traditional Phase III trials cost **{{< var traditional_phase3_cost_per_patient >}} per patient**. That's more than a Tesla per person to find out if a pill works. The pill costs 37 cents to make. The paperwork weighs more than the patient.

The Oxford RECOVERY trial proved humans can do the same thing for **{{< var recovery_trial_cost_per_patient >}} per patient**. They tested COVID treatments on 40,000+ patients by:

- Using existing hospital staff (revolutionary concept: doctors treating patients)
  ```
  - [ ] Reviewed

- **Line 119** (matched '`recovery trial cost`')
  ```
  #### Key Sources

- [RECOVERY Trial Cost Reduction](../references.qmd#recovery-trial-cost-reduction)
- [Clinical Trial Market Size](../references.qmd#clinical-trial-market-size)
- [DCT Cost Reductions Evidence](../references.qmd#dct-cost-reductions-evidence)
  ```
  - [ ] Reviewed

## knowledge/figures/core-economic-formulas.qmd

- **Line 36** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  TRADITIONAL_TRIAL_COST_PER_PATIENT = 80_000  # $80K average
RECOVERY_TRIAL_COST_PER_PATIENT = 500  # $500
DFDA_TARGET_COST_PER_PATIENT = 1_000  # $1K
'''
  ```
  - [ ] Reviewed

## knowledge/figures/fda-vs-dfda-efficiency-comparison-diagram.qmd

- **Line 6** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  |--------|-------------------|-------------------|-------------|
| **Approach** | 📋 Central Planning | 🛒 Open Platform | Market-based |
| **Cost per Patient** | {{< var traditional_phase3_cost_per_patient >}} | {{< var recovery_trial_cost_per_patient >}} | **{{< var dfda_trial_cost_reduction_factor >}} cheaper** |
| **Time to Results** | {{< var treatment_acceleration_years_current >}} | {{< var phase_1_safety_duration_years >}} | **{{< var fda_to_oxford_recovery_trial_time_multiplier >}} faster** |
| **Patient Access** | {{< var current_patient_participation_rate >}} | 100% | **{{< var dfda_trial_capacity_multiplier >}} more access** |
  ```
  - [ ] Reviewed

## knowledge/operations/messaging-and-communications-strategy.qmd

- **Line 97** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  This is where the real money is.

- **Lower recruiting costs:** Clinical trial participant acquisition costs {{< var recovery_trial_cost_per_patient >}} to $7,500 each. A 15-20% reduction from better messaging = massive savings
- **Faster recruiting:** Trial delays cost $600K-$8M per day. Recruit faster = save millions, get treatments to market sooner
  ```
  - [ ] Reviewed

## knowledge/problem.qmd

- **Line 73** (matched '`cost per patient`')
  ```
  It's like if you spent 97% of your grocery budget on cookbooks and 3% on food, then wondered why you're starving.

But it gets worse. The NIH RECOVER Initiative spent $1.665 billion over four years testing COVID treatments. Trials completed: zero. Cost per patient: $55,500.

Meanwhile, the UK's RECOVERY trial spent {{< var recovery_trial_total_cost >}} over six months, enrolled 48,000 patients, found multiple effective treatments, and saved over 1 million lives. Cost per patient: {{< var recovery_trial_cost_per_patient >}}.
  ```
  - [ ] Reviewed

- **Line 75** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  But it gets worse. The NIH RECOVER Initiative spent $1.665 billion over four years testing COVID treatments. Trials completed: zero. Cost per patient: $55,500.

Meanwhile, the UK's RECOVERY trial spent {{< var recovery_trial_total_cost >}} over six months, enrolled 48,000 patients, found multiple effective treatments, and saved over 1 million lives. Cost per patient: {{< var recovery_trial_cost_per_patient >}}.

The NIH spent 133 times more per patient to achieve infinitely less (dividing by zero is still infinity, even in government accounting).
  ```
  - [ ] Reviewed

- **Line 91** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  It takes {{< var treatment_acceleration_years_current >}} and {{< var pharma_drug_development_cost_current >}} to get a drug through FDA approval. {{< var treatment_acceleration_years_current >}}. That's longer than it took to build the pyramids, and those involved moving rocks the size of houses without machinery (also the pharaohs didn't have to file quarterly progress reports in triplicate).

During the Oxford RECOVERY trial, they tested treatments on 40,000 patients for {{< var recovery_trial_cost_per_patient >}} per person. The FDA's process costs {{< var traditional_phase3_cost_per_patient >}} per patient. That's {{< var recovery_trial_cost_reduction_factor >}} times more expensive for the same result, except slower. It's like if you could get a haircut for $10 or $820, but the $820 haircut takes {{< var treatment_acceleration_years_current >}} and you might be bald by then anyway.

Ninety-five percent of diseases have zero approved treatments. This is because the FDA is very good at preventing bad drugs from reaching people, and also pretty good at preventing good drugs from reaching people, and absolutely excellent at preventing any drugs from reaching people.
  ```
  - [ ] Reviewed

## knowledge/problem/fda-is-unsafe-and-ineffective.qmd

- **Line 50** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **Irrefutable Facts** (direct empirical data):

- {{< var recovery_trial_cost_reduction_factor >}}× cost differential: Oxford trial ({{< var recovery_trial_cost_per_patient >}}) vs. standard Phase III ({{< var traditional_phase3_cost_per_patient >}})
- {{< var post_1962_drug_approval_reduction_pct >}} drug approval reduction: Immediate drop from [46/year (1960) to 13/year (1963)](../references.qmd#post-1962-drug-approval-drop)
- Beta-blocker deaths: [100,000 Americans died](../references.qmd#beta-blocker-drug-lag-deaths) during decade-long delay
  ```
  - [ ] Reviewed

- **Line 75** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  Compare two real-world systems for testing drugs:

1.  **The Oxford RECOVERY Trial:** Tested COVID treatments on 47,000 patients for **{{< var recovery_trial_cost_per_patient >}} per patient**. Found a life-saving treatment in 3 months.
2.  **The Post-1962 System:** Averages **{{< var traditional_phase3_cost_per_patient >}} per patient** for clinical trials. Takes **[9.1 years](../references.qmd#drug-development-timeline-17-years)** to approve a new drug.
  ```
  - [ ] Reviewed

- **Line 76** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  1.  **The Oxford RECOVERY Trial:** Tested COVID treatments on 47,000 patients for **{{< var recovery_trial_cost_per_patient >}} per patient**. Found a life-saving treatment in 3 months.
2.  **The Post-1962 System:** Averages **{{< var traditional_phase3_cost_per_patient >}} per patient** for clinical trials. Takes **[9.1 years](../references.qmd#drug-development-timeline-17-years)** to approve a new drug.

The current system costs **{{< var dfda_trial_cost_reduction_factor >}}× more** and takes **{{< var fda_to_oxford_recovery_trial_time_multiplier >}} longer**. Not a small difference - the difference between functional and designed-to-fail.
  ```
  - [ ] Reviewed

- **Line 127** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  | **New Approvals** | [46/year (1960)](../references.qmd#post-1962-drug-approval-drop) | [13/year (1963)](../references.qmd#post-1962-drug-approval-drop) | {{< var post_1962_drug_approval_reduction_pct >}} decline |
| **Life Expectancy Growth** | [3.82 years/decade](../references.qmd#life-expectancy-increase-pre-1962) | [1.54 years/decade](../references.qmd#post-1962-life-expectancy-slowdown) | [60% reduction](../references.qmd#post-1962-life-expectancy-slowdown) |
| **Trial Cost** | {{< var dfda_pragmatic_trial_cost_per_patient >}} (pragmatic) | {{< var traditional_phase3_cost_per_patient >}} | {{< var dfda_trial_cost_reduction_factor >}}× increase |
| **Time to Approval** | 2-3 years | {{< var fda_phase_1_to_approval_years >}} | 5-8× slower |
  ```
  - [ ] Reviewed

## knowledge/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd

- **Line 58** (matched '`cost per patient`')
  ```
  **Patients enrolled:** [~30,000](../references.qmd#recover-initiative-patient-enrollment)
**Trials completed:** [Zero](../references.qmd#nih-recover-inefficiency)
**Cost per patient:** \$55,500

### RECOVERY Trial (UK Approach)
  ```
  - [ ] Reviewed

- **Line 66** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  **Patients enrolled:** [48,000](../references.qmd#recovery-trial-82x-cost-reduction)
**Treatments found:** [Multiple, including dexamethasone](../references.qmd#recovery-trial-summary-quote) (saved over 1 million lives)
**Cost per patient:** {{< var recovery_trial_cost_per_patient >}}

The NIH RECOVER Initiative spent **133X more per patient** to achieve **infinitely less** (dividing by zero trials completed).
  ```
  - [ ] Reviewed

- **Line 224** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  ## What Would Actually Work

The UK RECOVERY trial proved the alternative: {{< var recovery_trial_cost_per_patient >}} per patient instead of {{< var traditional_phase3_cost_per_patient >}}, 100 days instead of years, and over 1 million lives saved.

What it requires:
  ```
  - [ ] Reviewed

## knowledge/problem/untapped-therapeutic-frontier.qmd

- **Line 102** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  It's not because science is hard. It's because:

1. **Trials Cost Too Much:** A typical Phase II-III RCT costs **$30-$100M** (Median cost per patient {{< var traditional_phase3_cost_per_patient >}}). At that price, you only test "sure things." You test the equivalent of betting your house that the sun will rise. Safe bets. Boring bets. Bets that don't cure cancer.

2. **Herd Mentality:** Trials overwhelmingly test the same few biological targets due to [preferential attachment dynamics](../references.qmd#preferential-target-attachment). Everyone studies what everyone else is studying because that's how you get grants. It's like if every explorer only went to France because France already had good reviews on TripAdvisor.
  ```
  - [ ] Reviewed

- **Line 150** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  ## The Fix

The Oxford RECOVERY Trial (COVID-19) proved that large-scale pragmatic trials can run for ~{{< var recovery_trial_cost_per_patient >}} per patient and deliver results in [<100 days](../references.qmd#recovery-trial-100-days-to-cure).

{{< var recovery_trial_cost_per_patient >}} vs {{< var traditional_phase3_cost_per_patient >}}.
  ```
  - [ ] Reviewed

- **Line 152** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  The Oxford RECOVERY Trial (COVID-19) proved that large-scale pragmatic trials can run for ~{{< var recovery_trial_cost_per_patient >}} per patient and deliver results in [<100 days](../references.qmd#recovery-trial-100-days-to-cure).

{{< var recovery_trial_cost_per_patient >}} vs {{< var traditional_phase3_cost_per_patient >}}.

With a [decentralized framework for drug assessment](../solution/dfda.qmd), trial capacity increases by {{< var dfda_trial_capacity_multiplier >}}:
  ```
  - [ ] Reviewed

## knowledge/proof.qmd

- **Line 24** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  2020: In less than 100 days, British doctors prevented over a million COVID deaths with a drug from 1961.
Cost: **{{< var recovery_trial_cost_per_patient >}} per patient**.

The model exists.
  ```
  - [ ] Reviewed

## knowledge/references.qmd

- **Line 658** (matched '`cost per patient`')
  ```
  > "Research productivity is falling sharply everywhere we look. Averaging across industries, research productivity declines at a rate that averages about 5% per year. For example, the number of researchers required to achieve a constant level of Moore's Law has risen by a factor of 18 since 1971."
> — Bloom, Nicholas, Charles I. Jones, John Van Reenen, and Michael Webb, 2020, [Are Ideas Getting Harder to Find?](https://www.aeaweb.org/articles?id=10.1257/aer.20180338) American Economic Review 110 (4): 1104–44 | Originally NBER Working Paper 23782 (2017)
> Note: This finding reflects innovation productivity in traditional research models; dFDA targets trial execution efficiency (cost per patient), not fundamental idea generation

---
  ```
  - [ ] Reviewed

- **Line 1428** (matched '`cost per patient`')
  ```
  > Median clinical trial cost: $19.0 million (range: $12.2M - $33.1M)
> Cost per patient varies by phase: Phase 1: ~$137K, Phase 2: ~$130K, Phase 3: ~$113K
> — [JAMA Internal Medicine: Clinical Trial Costs Study](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2702287)
> Note: Based on analysis of 138 clinical trials. Actual costs can vary significantly based on disease area, trial complexity, and patient population
  ```
  - [ ] Reviewed

- **Line 1436** (matched '`cost per patient`')
  ```
  <a id="clinical-trial-cost-per-patient"></a>

title: Clinical trial cost per patient (traditional Phase III)

type: article
  ```
  - [ ] Reviewed

- **Line 1445** (matched '`cost per patient`')
  ```
  > Traditional Phase III trials cost $40,000-120,000 per patient including site fees, overhead, staff, monitoring, and data management.
> — ProRelix Research, [Phase-by-Phase Clinical Trial Costs](https://prorelixresearch.com/phase-by-phase-clinical-trial-costs-what-every-sponsor-needs-to-know/) | WithPower, [Clinical Trial Cost Per Patient](https://www.withpower.com/guides/clinical-trial-cost-per-patient) | JAMA, [Cost of Bringing a New Drug](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2702287)

---
  ```
  - [ ] Reviewed

- **Line 8557** (matched '`cost per patient`')
  ```
  <a id="phase-1-cost-per-patient-137k"></a>

title: Phase 1 cost per patient

type: article
  ```
  - [ ] Reviewed

- **Line 8680** (matched '`cost per patient`')
  ```
  <a id="phase-2-cost-per-patient-130k"></a>

title: Phase 2 cost per patient

type: article
  ```
  - [ ] Reviewed

- **Line 8773** (matched '`cost per patient`')
  ```
  <a id="phase-3-cost-per-patient-113k"></a>

title: Phase 3 cost per patient

type: article
  ```
  - [ ] Reviewed

- **Line 9505** (matched '`recovery trial cost`')
  ```
  <a id="recovery-cost-500"></a>

title: RECOVERY Trial Cost per Patient

type: article
  ```
  - [ ] Reviewed

- **Line 9576** (matched '`recovery trial cost`')
  ```
  <a id="recovery-trial-cost-reduction"></a>

title: RECOVERY trial cost reduction

type: article
  ```
  - [ ] Reviewed

- **Line 9616** (matched '`recovery trial cost`')
  ```
  url: https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs

> "At a cost of $20 million for 48,000 patients, the RECOVERY trial cost about $500 per patient... that is about $50 per patient per answer."
> — Professor Martin Landray (co-chief investigator), quoted in Oren Cass, Manhattan Institute, 2023, [Slow, Costly Clinical Trials Drag Down Biomedical Breakthroughs](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)
  ```
  - [ ] Reviewed

- **Line 10706** (matched '`cost per patient`')
  ```
  <a id="trial-cost-41k"></a>

title: Traditional Trial Cost per Patient

type: article
  ```
  - [ ] Reviewed

- **Line 10714** (matched '`cost per patient`')
  ```
  url: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7295430/

> "The median cost of a pivotal trial was estimated to be \$19 million... the median cost per patient was \$41,413."
> — Moore, T. J., Zhang, H., Anderson, G., & Alexander, G. C. (2020). Estimated Costs of Pivotal Trials for Novel Therapeutic Agents Approved by the US Food and Drug Administration, 2015-2017. _JAMA Internal Medicine_. [Link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7295430/)
  ```
  - [ ] Reviewed

- **Line 12632** (matched '`recovery trial cost`')
  ```
  <a id="recovery-trial-roi"></a>

title: RECOVERY Trial Cost-Effectiveness (~$4/QALY, Global Impact Methodology)

type: article
  ```
  - [ ] Reviewed

- **Line 12685** (matched '`adaptable trial cost`')
  ```
  url: https://commonfund.nih.gov/hcscollaboratory

> The NIH Pragmatic Trials Collaboratory funds trials at **$500K for planning phase, $1M/year for implementation**—a tiny fraction of NIH's budget. The ADAPTABLE trial cost **$14 million** for **15,076 patients** (= **$929/patient**) versus **$420 million** for a similar traditional RCT (30x cheaper), yet pragmatic trials remain severely underfunded. PCORnet infrastructure enables real-world trials embedded in healthcare systems, but receives minimal support compared to basic research funding.
> — [NIH Common Fund: HCS Research Collaboratory](https://commonfund.nih.gov/hcscollaboratory) | [PCORnet ADAPTABLE Summary](https://pcornet.org/wp-content/uploads/2025/08/ADAPTABLE_Lay_Summary_21JUL2025.pdf) | [PMC: Pragmatic Clinical Trials in Healthcare Systems](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5604499/)
  ```
  - [ ] Reviewed

- **Line 12704** (matched '`cost per patient`')
  ```
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC6508852/

> **Meta-analysis of 108 embedded pragmatic clinical trials** (2006-2016). The median cost per patient was **$97** (mean $478) across all trials reviewed. 25% of studies cost less than $19 per patient. US studies had higher median costs ($187 vs $27 non-US). Registry-based trials were less expensive than EHR-based trials. Traditional RCT comparison: **$16,600/patient** (Berndt & Cockburn 2014). The 108 trials had median enrollment of 5,540 patients with broad eligibility criteria. 81% used cluster randomization. Trials spanned 15 countries, infectious diseases (25%), cardiovascular (18%), diabetes (12%).
> — [Harvard Medical School/Harvard Pilgrim Health Care Institute, Learning Health Systems 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6508852/)
  ```
  - [ ] Reviewed

## knowledge/solution.qmd

- **Line 130** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  3. **Publishes outcome labels** (truth about every treatment)

Instead of waiting {{< var treatment_acceleration_years_current >}} for FDA approval while you die, you join a trial. The trial costs {{< var dfda_pragmatic_trial_cost_per_patient >}} per patient instead of {{< var traditional_phase3_cost_per_patient >}} because it turns out you don't need {{< var treatment_acceleration_years_current >}} layers of paperwork to figure out if aspirin works.

You report outcomes through your phone. The AI analyzes millions of data points. The framework publishes rankings: "For your condition, this works 73% of the time, this works 45%, this does nothing but costs less."
  ```
  - [ ] Reviewed

## knowledge/solution/1-percent-treaty.qmd

- **Line 279** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  #### Current System

- Pivotal trials: {{< var traditional_phase3_cost_per_patient >}} per patient
- Only 5M participants per year globally
- 99.8% of willing participants turned away
  ```
  - [ ] Reviewed

- **Line 287** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  - $110B total funding ({{< var global_clinical_trials_spending_annual >}} existing + {{< var treaty_annual_funding >}} from treaty)
- Pragmatic trials: {{< var dfda_pragmatic_trial_cost_per_patient >}} per patient ({{< var dfda_trial_cost_reduction_factor >}}× cheaper)
- 220M participants per year (44x acceleration)
- Still only using 18% of available willing participants
  ```
  - [ ] Reviewed

## knowledge/solution/dfda.qmd

- **Line 26** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  [Half of humanity would volunteer](../references.qmd#patient-willingness-clinical-trials) if they could. We have **240 times more willing participants** than we're using.

This isn't because people don't want to help find cures. It's because the current system can't scale. Trials cost {{< var traditional_phase3_cost_per_patient >}} per patient, require traveling to major medical centers, and have exclusion criteria that reject {{< var antidepressant_trial_exclusion_rate >}} [of actual patients](../references.qmd#antidepressant-trial-exclusion-rates).

**We're not facing a recruitment problem. We're facing a capacity problem.**
  ```
  - [ ] Reviewed

- **Line 49** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  - Patients pay for treatment (covers manufacturing/delivery)
- Patients provide data (eliminates data collection cost ~{{< var traditional_phase3_cost_per_patient >}}/patient)
- Platform handles analysis (eliminates analysis cost)
- Insurance is built-in (eliminates liability cost)
  ```
  - [ ] Reviewed

- **Line 76** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  - Manufacturing cost: $20/month
- Profit: $80/month per patient
- Plus: Free clinical trial data worth {{< var traditional_phase3_cost_per_patient >}}/patient in traditional system

### Why This Creates Unlimited Research Capacity
  ```
  - [ ] Reviewed

- **Line 452** (matched '`cost per patient`')
  ```
  During COVID, while America was filling out forms, Oxford University did something crazy: they just tested drugs on dying people to see if they stopped dying.

Cost per patient:

- Normal clinical trials: {{< var traditional_phase3_cost_per_patient >}}
  ```
  - [ ] Reviewed

- **Line 454** (matched '`TRADITIONAL_PHASE3_COST_PER_PATIENT`')
  ```
  Cost per patient:

- Normal clinical trials: {{< var traditional_phase3_cost_per_patient >}}
- Oxford pragmatic trials: {{< var recovery_trial_cost_per_patient >}}
  ```
  - [ ] Reviewed

- **Line 455** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - Normal clinical trials: {{< var traditional_phase3_cost_per_patient >}}
- Oxford pragmatic trials: {{< var recovery_trial_cost_per_patient >}}

That's not a typo. Five hundred dollars. The cost of a nice dinner in Manhattan to save a human life.
  ```
  - [ ] Reviewed

- **Line 619** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  Your decentralized framework for drug assessment achieves **{{< var dfda_trial_cost_reduction_factor >}}× More Efficiency** through:

- **Cost per patient**: {{< var dfda_pragmatic_trial_cost_per_patient >}} vs the current {{< var traditional_phase3_cost_per_patient >}}
- **Time to results**: 2 years vs the current 17 years
- **Patient access**: Universal access vs {{< var antidepressant_trial_exclusion_rate >}} excluded currently
  ```
  - [ ] Reviewed

## knowledge/solution/war-on-disease.qmd

- **Line 132** (matched '`RECOVERY_TRIAL_COST_PER_PATIENT`')
  ```
  - 1,000+ active trials launched (versus current 50/year)
- 100,000+ patients enrolled (versus current 5,000)
- A 50.0% reduction in trial costs demonstrated (from {{< var traditional_phase3_cost_per_patient >}} to {{< var recovery_trial_cost_per_patient >}} per patient)

#### Year 10 Targets
  ```
  - [ ] Reviewed

## knowledge/test/test-parameters.qmd

- **Line 14** (matched '`ADAPTABLE_TRIAL_COST_PER_PATIENT`')
  ```
  Testing if using ANY variable from _variables.yml triggers citation warnings for ALL embedded citations:

- ADAPTABLE trial cost per patient: {{< var adaptable_trial_cost_per_patient >}}
- Test metric: 100%
- Sample value: $1,000,000
  ```
  - [ ] Reviewed

## scripts/find-parameter-usages.ts

- **Line 8** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  * Usage:
 *   npx tsx scripts/find-parameter-usages.ts PARAMETER_NAME
 *   npx tsx scripts/find-parameter-usages.ts DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT
 *   npx tsx scripts/find-parameter-usages.ts --all  # List all parameters
 */
  ```
  - [ ] Reviewed

- **Line 376** (matched '`DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT`')
  ```
  console.log('       npx tsx scripts/find-parameter-usages.ts --all');
    console.log('\nExample:');
    console.log('  npx tsx scripts/find-parameter-usages.ts DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT');
    process.exit(1);
  }
  ```
  - [ ] Reviewed

