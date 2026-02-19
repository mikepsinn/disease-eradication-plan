# The Optimal Policy Generator: A Causal Inference Protocol for Maximizing Median Health and Wealth Through Public Policy

**Config:** _quarto-opg.yml
**Type:** website
**Files:** 1 | **Words:** 12,861 | **Images:** 34 | **Est. Pages:** ~68

#### knowledge/appendix/optimal-policy-generator-spec.qmd
**Title:** The Optimal Policy Generator: A Causal Inference Protocol for Maximizing Median Health and Wealth Through Public Policy
**Description:** The Optimal Policy Generator (OPG) produces systematic public policy recommendations for jurisdictions at any level (country, state, city), generating prioritized enact/replace/repeal/maintain recommendations to maximize real after-tax median income growth and median healthy life years, based on quasi-experimental evidence from centuries of policy variation data.
**Stats:** 12,861 words | 1,878 lines | 34 images | ~68p

  - Abstract {.unnumbered}
  - The Two Welfare Metrics {#sec-two-metrics}
    ![The two things that matter: having money and being alive to spend it. You'd think this would be obvious, but governments often forget the second bit.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-the-two-welfare-metrics-sec-two-metrics-bw-academic.jpg)
    - Why Only Two Metrics?
    - Income Metric Definition {#sec-income-definition}
    - Outcome Translation Methodology {#sec-outcome-translation}
  - The Evidence Base: Centuries of Natural Policy Experiments {#sec-evidence-base}
    - Scale of Available Natural Experiments
    ![US states give you 3,500 policy-years of data. Cities worldwide give you millions. It's like comparing a cookbook to the entire history of food.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-scale-of-available-natural-experiments-bw-academic.jpg)
    - The OPG Pipeline
    ![Data goes in, gets organized, analyzed, scored, then spits out recommendations. It's a sausage factory, but for telling politicians what works instead of what kills you.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-the-opg-pipeline-bw-academic.jpg)
    - Why This Hasn't Been Done Before
    ![Four reasons this was impossible before: scattered data, slow computers, bad methods, nobody cared. Now: fast computers, good methods, some people care. Progress is three steps forward, four barriers removed.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-why-this-hasn-t-been-done-before-bw-academic.jpg)
  - System Overview {#sec-opg-system-overview}
    - What Policymakers See
    - What Policy Analysts See
    ![Eight different types of data combine to tell you if a policy actually works. Like ingredients in a recipe, except this one tells you which recipes poison people.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-what-policy-analysts-see-bw-academic.jpg)
  - Introduction
    - Why Policy Ranking Fails Today
    ![Evidence says policy X works. But lobbying, fear of change, and shiny distractions filter it out. It's like having the cure but drinking the poison because the bottle is prettier.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-why-policy-ranking-fails-today-bw-academic.jpg)
    - Scale of Available Evidence
    ![Current system: decide based on feelings, maybe 10 examples. New system: decide based on millions of examples. It's the difference between astrology and astronomy, but for governance.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-scale-of-available-evidence-bw-academic.jpg)
    - Contributions
    ![Evidence becomes a score. Score tells you: do this new thing, swap that old thing, stop doing that terrible thing, or keep doing that good thing. It's like Marie Kondo, but for laws.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-contributions-bw-academic.jpg)
    - Validation Status
  - Related Work
    - Existing Policy Evaluation Frameworks
    - This Framework's Contribution
    ![How OPG is different from traditional evaluation: it's personalized, comprehensive, and uses actual data instead of vibes.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-this-framework-s-contribution-bw-academic.jpg)
  - Theoretical Framework
    - The Policy Optimization Problem
    ![Two circles: what you do now, what you should do. The bits that don't overlap are where people are dying unnecessarily. Venn diagrams finally do something useful.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-the-policy-optimization-problem-bw-academic.jpg)
    - Evidence Aggregation Properties
    - Information Value
  - Core Methodology
    - Policy-Outcome Data Structure
    ![How the database connects policies to outcomes. It's plumbing, but for knowledge instead of waste. Although some policies are also waste.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-policy-outcome-data-structure-bw-academic.jpg)
      - Core Tables
      - Policy Types
    - Analysis Methods {#sec-analysis-methods}
    ![Different ways to figure out if policies work when you can't run proper experiments because ethics committees get upset about randomly killing control groups.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-analysis-methods-sec-analysis-methods-bw-academic.jpg)
      - Synthetic Control Method
      - Difference-in-Differences (DiD)
    ![Two lines run parallel, then one gets the policy and diverges. The gap between them is how much the policy helped or hurt. It's like twins, but one gets vegetables.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-difference-in-differences-did-bw-academic.jpg)
      - Regression Discontinuity Design (RDD)
    ![Dots on either side of a line, big jump at the cutoff. People just above the line do better. It's like being born one day later and getting free healthcare.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-regression-discontinuity-design-rdd-bw-academic.jpg)
      - Event Study / Interrupted Time Series
    ![Nothing happens, nothing happens, nothing happens, policy hits, then things change. It's like a heart rate monitor, but for legislation instead of life.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-event-study-interrupted-time-series-bw-academic.jpg)
      - Confidence Weighting by Method
    - Bradford Hill Criteria Scoring Functions {#sec-bradford-hill}
    ![Take nine different ways to check if something causes something else, squish them into numbers between 0 and 1. Science loves turning confidence into decimals.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-bradford-hill-criteria-sco-bw-academic.jpg)
      - Strength of Association
      - Consistency Across Jurisdictions
      - Temporality (Required)
      - Dose-Response Gradient
      - Experiment Quality
      - Plausibility (Mechanistic)
      - Coherence with Literature
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
    ![How to find good examples to copy: find places like you, who did the thing, and didn't collapse. It's like plagiarism, but encouraged.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-similar-jurisdictions-sec-similar-jurisdictions-bw-academic.jpg)
      - Computing Jurisdiction Similarity
    - Recommended Tracking (for OPG Feedback)
    ![OPG suggests thing, place does thing, place reports how it went, OPG learns. It's a feedback loop, except it actually uses the feedback instead of filing it.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-recommended-tracking-for-opg-feedback-bw-academic.jpg)
  - Optimal Jurisdictional Level for Policy Implementation
    - The Subsidiarity Principle for Evidence Generation
    ![Federal level: little data, big risk. County level: lots of data, small risk. It's safer to experiment in Shropshire than with the entire country.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-the-subsidiarity-principle-for-evidence-generation-bw-academic.jpg)
    - When Higher Levels Are Necessary
    - Jurisdictional Level in Recommendations
  - Policy Impact Score (Intermediate Metric) {#sec-pis}
    - Overview
    - Jurisdiction-Level PIS Calculation
    ![How to calculate if a policy works: add up how big the effect is, how sure we are, and how good the data is, for both money and health. Then argue about the number.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-jurisdiction-level-pis-calculation-bw-academic.jpg)
    - Always Report Both Metrics Separately
    - Effect Estimate Standardization
    - Quality Adjustment Factor
    - Confounder Adjustment
    ![Policy causes outcome, but other things also cause outcome. We control for the things we know about. The things we don't know about are called 'oops.'](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-confounder-adjustment-bw-academic.jpg)
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
    ![How to check if your fake control group is good enough: measure error, try fake treatments, reject if it's rubbish. Quality control for imaginary things.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-pre-treatment-fit-synthetic-control-bw-academic.jpg)
    - Placebo and Robustness Tests
  - Interpreting Recommendations
    - Priority Tiers
    - Political Feasibility Notes
    - Sequencing Guidance
    ![Start with easy wins, build momentum, bundle things together, hit critical mass. It's like a diet plan, but for governance and with better success rates.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-sequencing-guidance-bw-academic.jpg)
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
    ![Same policy, different places, different results. Turns out context matters. Who knew, apart from everyone who's ever tried anything anywhere.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-heterogeneous-effects-bw-academic.jpg)
    - Jurisdiction-Specific Caveats
    - Time-Varying Effects
    ![Immediate effect, people adapt, effect drifts, long-run effect settles. Policies age like milk, not wine.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-time-varying-effects-bw-academic.jpg)
    - Publication Bias
    ![Studies that find nothing don't get published, so we think everything works. Funnel plots fish the failures out of the file drawer. Science learns to count its zeros.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-publication-bias-bw-academic.jpg)
    - Epistemic Limitations
  - Validation Framework {#sec-opg-validation-framework}
    - The Critical Question
    - Addressing Adoption Bias
    - Proposed Validation Study
    ![Check if the system would have been right in the past: compute old data, identify policies, compare predictions to reality, grade yourself. It's like marking your own homework, but honest.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-proposed-validation-study-bw-academic.jpg)
    - Prospective Pre-Registration
    ![Promise what you'll measure before you measure it, then stick to the promise. Prevents 'we meant to test that all along' syndrome.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-prospective-pre-registration-bw-academic.jpg)
    - Known Limitations Requiring Validation
    - Continuous Improvement via Adoption Feedback
    ![Recommend policy, place tries it, place reports results, analysis updates, better recommendations. It's machine learning, but for government instead of cat pictures.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-continuous-improvement-via-adoption-feedback-bw-academic.jpg)
  - Future Directions
    - Validation Priorities
    ![Ways to check if predictions work, ranked by importance: retrospective studies, prospective trials, cross-validation, expert review. Trust in descending order.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-validation-priorities-bw-academic.jpg)
    - Data Infrastructure
    ![Collect laws, teach computers to read them, standardize the results, give researchers access. It's a library, but the books are alive and the librarian is an algorithm.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-data-infrastructure-bw-academic.jpg)
    - Integration with Decision-Making
    ![Show data, admit uncertainty, model scenarios, get feedback, repeat. It's like being honest about not knowing things, which is why it's revolutionary.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-integration-with-decision-making-bw-academic.jpg)
  - Conclusion
  - Acknowledgments {.unnumbered}
  - References
  - Appendix A: Worked Example - Texas Policy Recommendations {.appendix}
    - Warning SYNTHETIC DATA - NOT EMPIRICAL FINDINGS
    - Overview
    - Texas Policy Inventory (Sample)
    - Step 1: Calculate Policy Impact Scores
    - Step 2: Apply Context Adjustment for Texas
    - Step 3: Generate Recommendations
  - ENACT (New Policies to Adopt)
  - REPLACE (Policies to Modify)
  - REPEAL (Policies to Remove)
  - MAINTAIN (No Change Needed)
    - Step 4: Summary Dashboard
    - Interpretation
    ![How policies affect money versus how they affect not dying. Ideally, both go up. Often, you have to pick one.](/assets/images/optimal-policy-generator-spec/optimal-policy-generator-spec-section-interpretation-bw-academic.jpg)
  - Appendix B: OPG Analysis Workflow {.appendix}
    - Complete OPG Pipeline
    - Minimum Data Requirements Checklist
  - Appendix C: Glossary {.appendix}
