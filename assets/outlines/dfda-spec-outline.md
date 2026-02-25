# The Continuous Evidence Generation Protocol: Two-Stage Validation (RWE → Pragmatic Trials)

**Config:** _quarto-dfda-spec.yml
**Type:** website
**Files:** 1 | **Words:** 14,326 | **Images:** 45 | **Est. Pages:** ~80

#### knowledge/appendix/dfda-spec-paper.qmd
**Title:** The Continuous Evidence Generation Protocol: Two-Stage Validation (RWE → Pragmatic Trials)
**Description:** We present the Predictor Impact Score (PIS), a novel composite metric operationalizing Bradford Hill causality criteria for automated signal detection from aggregated N-of-1 observational studies. Combined with pragmatic trial confirmation (based on evidence from 108+ embedded trials), this two-stage framework would generate validated outcome labels at 44.1x (95% CI: 39.4x-89.1x) lower cost than traditional Phase III trials. This enables continuous, population-scale pharmacovigilance and precision dosing recommendations.
**Stats:** 14,326 words | 1,976 lines | 45 images | ~80p

  - Abstract
    ![Step 1: Let computers watch a billion people take medicine. Step 2: Test the interesting bits. You were doing Step 2 first, which is why everything costs a billion dollars.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-abstract-bw-academic.jpg)
  - System Overview: From Methodology to Implementation {#system-overview}
    ![Imagine if restaurants had to tell you which dishes actually taste good instead of just not poisoning you. This is that, but for drugs.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-system-overview-from-methodology-to-implementation-system-overview-bw-academic.jpg)
    - What Patients See
    ![Treatment rankings, like Yelp reviews, but for not dying. You could have done this decades ago. You chose not to.](../../assets/images/dfda-comparative-effectiveness-ranking-search.png)
    - What Companies See
    ![Drug companies used to spend ten years asking permission to help people. Now they just help people and write down what happens. Revolutionary.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-what-companies-see-bw-academic.jpg)
    - Where This Methodology Fits
    ![First, computers find patterns in real life. Then, humans check if the computers are hallucinating. It's like peer review, but one of the peers is a billion people.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-where-this-methodology-fits-bw-academic.jpg)
  - Introduction
    - The Human Cost of the Current System
    ![While you waited for permission to try new cancer drugs, more people died than in all of World War II. The forms were very thorough though.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-the-human-cost-of-the-current-system-bw-academic.jpg)
    - The Pharmacovigilance Gap
    ![Your three ways of checking if drugs kill people: slow and expensive, slower and more expensive, or fast but everyone lies on the survey.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-the-pharmacovigilance-gap-bw-academic.jpg)
    - The Real-World Data Opportunity
    ![People voluntarily track their sleep, heart rate, mood, and bowel movements on their phones. You could use this to cure disease. You mostly use it to sell them running shoes.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-the-real-world-data-opportunity-bw-academic.jpg)
    - Our Contribution
    ![Turns out watching people die gives you the same answer as randomly choosing who dies. Science!](../../assets/images/observational-vs-randomized-effect-sizes.png)
    ![The fancy expensive experiments get the same results as just watching what happens. You've been overpaying for decades.](../../assets/images/observational-vs-randomized-trial-effect-sizes.png)
  - Data Collection and Integration
    - Data Sources
    - Variable Ontology
    - Measurement Structure
    ![Every time you measure something, you have to write down who, what, when, and how. It's like a murder mystery, but for data points.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-measurement-structure-bw-academic.jpg)
    - Unit Standardization
  - Mathematical Framework
    ![Take pill. Wait. Feel better. Feel worse again. Take another pill. You'd think medicine would have figured out the timing by now.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-mathematical-framework-bw-academic.jpg)
    - Data Structure
    ![If you take aspirin at noon, your headache goes away around 12:30 and comes back at 5pm. Computers need Greek letters to understand this.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-mathematical-framework-bw-academic.jpg)
    - Temporal Alignment
      - Onset Delay and Duration of Action
      - Outcome Window Calculation
    - Pair Generation Strategies
      - Outcome-Based Pairing (Predictor has Filling Value)
    ![To know if the pill worked, you have to look backwards in time to see if you took it. Time travel, but boring.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-outcome-based-pairing-predictor-has-filling-value-bw-academic.jpg)
      - Predictor-Based Pairing (No Filling Value)
    ![Medicine happens. Time passes. Body does things. You measure the things. It's called 'waiting' but scientists need diagrams.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-predictor-based-pairing-no-filling-value-bw-academic.jpg)
    - Filling Value Logic
      - Filling Types
      - Temporal Boundaries
    ![Only use data from when people were actually paying attention. Ignore measurements from that week they forgot their tracking app existed.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-temporal-boundaries-bw-academic.jpg)
      - Conservative Bias
    ![When people forget to log their data, pretend they took zero pills. This makes drugs look worse than they are, which is somehow the responsible thing to do.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-conservative-bias-bw-academic.jpg)
    - Baseline Definition and Outcome Estimation
      - Within-Subject Comparison
      - Outcome Means
    - Percent Change from Baseline
    - Correlation Coefficients
      - Pearson Correlation (Linear Relationships)
      - Spearman Rank Correlation (Monotonic Relationships)
      - Forward and Reverse Correlations
    ![Does taking aspirin cure your headache, or does having a headache make you take aspirin? Computers get confused about which direction time flows.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-forward-and-reverse-correlations-bw-academic.jpg)
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
    ![Four ways to tell if a drug actually works or if you're just seeing patterns in random noise, like Jesus in toast.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-predictor-impact-score-bw-academic.jpg)
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
    ![Computers look at what dose worked best for people like you in the past. It's astrology, but with math that actually works.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-optimal-daily-value-for-precision-dosing-bw-academic.jpg)
      - Value Predicting High Outcome
      - Value Predicting Low Outcome
      - Grouped Optimal Values
    ![The computer says take 47.3mg. Your pills come in 50mg. Close enough, the computer sighs.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-grouped-optimal-values-bw-academic.jpg)
      - Precision Dosing Recommendations
    ![If more is better, take more. If more is worse, take less. You needed a flowchart for this.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-precision-dosing-recommendations-bw-academic.jpg)
      - Mathematical Relationship to Biological Gradient
      - Clinical Applications
      - Limitations
    ![What works for most people is a starting point for figuring out what works for you specifically. Personalized medicine is just trial and error with better record keeping.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-limitations-bw-academic.jpg)
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
    ![Five ways to tell if your data is too boring to bother with. Science has a spam filter now.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-boring-relationship-definition-bw-academic.jpg)
      - Usefulness and Causality Voting
    - Variable Valence
      - Impact on Interpretation
    - Temporal Parameter Optimization
      - Stored Optimization Data
      - Optimization Grid
    ![A spreadsheet where every cell represents how long to wait and how long to watch for effects. Somewhere in this grid is the truth. The computer checks every box.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-optimization-grid-bw-academic.jpg)
      - Overfitting Protection
    ![Four ways to stop the computer from seeing patterns that don't exist, like your brain does with clouds.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-overfitting-protection-bw-academic.jpg)
    - Spearman Rank Correlation
  - Outcome Label Generation
    - Predictor Analysis Reports
    ![Everything that makes your disease better or worse, ranked from most helpful to most harmful. Like a scoreboard for your organs.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-predictor-analysis-reports-bw-academic.jpg)
    - Report Structure
    - Category-Specific Analysis
    ![Five categories of things that affect your health: pills, food, habits, air, and other diseases you already have. Medicine filed everything into folders.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-category-specific-analysis-bw-academic.jpg)
    - Verification Status
    - Outcome Labels vs. FDA Drug Labels
    - Worked Example: Complete Outcome Label
    ![Outcome Labels show quantitative effect sizes, sample sizes, and confidence intervals for each treatment, like nutrition facts for drugs](../../assets/images/dfda-outcome-labels.png)
  - Treatment Ranking System
    - Within-Category Rankings
    ![Treatments ranked by: does it work (most important), are we sure (pretty important), and how many people did we watch (least important). Revolutionary prioritization.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-within-category-rankings-bw-academic.jpg)
    - Ranking Algorithm
    - Confidence Weighting
    - Comparative Effectiveness Display
  - Safety and Efficacy Quantification
    - Safety Signal Detection
    - Efficacy Signal Detection
    - Benefit-Risk Assessment
  - Addressing the Bradford Hill Criteria {#addressing-bradford-hill}
    ![Nine ways to tell if A causes B or if you're just making things up. Bradford Hill wrote them down in 1965. You've been ignoring them.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-addressing-the-bradford-hill-criteria-addressing-bradford-hill-bw-academic.jpg)
    - Complete Criteria Mapping
    - Quantitative Criteria Details
  - Validation and Quality Assurance
    - User Voting System
    - Automated Quality Checks
    ![Five checkpoints where bad data gets thrown out. It's airport security, but for numbers.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-automated-quality-checks-bw-academic.jpg)
    - Flagged Study Handling
    ![Studies can get kicked out for being terrible, then let back in if they fix their mistakes. Academic probation, but for data.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-flagged-study-handling-bw-academic.jpg)
  - Stage 2: Pragmatic Trial Confirmation
    ![Stage 1: Computers watch everyone and get suspicious about patterns. Stage 2: Humans run cheap experiments to see if the computers were right or hallucinating.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-stage-2-pragmatic-trial-confirmation-bw-academic.jpg)
    - The Two-Stage Pipeline
    - Pragmatic Trial Methodology
    - Signal-to-Trial Prioritization
    - Comparative Effectiveness Randomization
    - Feedback Loop: Trial Results Improve Observational Models
    ![A loop where real life teaches experiments what to test, and experiments teach real life what works. It's a circle, which means it never stops, which terrifies administrators.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-feedback-loop-trial-results-improve-observational-models-bw-academic.jpg)
    - Output: Validated Outcome Labels
  - Limitations and How They're Addressed
    - Fundamental Limitations: Observational Stage
    - Methodological Weaknesses: Addressed by Two-Stage Design
    - Residual Limitations
    - What This Framework CAN Now Do
    ![Watch people. Test hunches. Learn things. Watch more people. Test new hunches. Never stop. This is what learning looks like when you automate it.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-what-this-framework-can-now-do-bw-academic.jpg)
  - Implementation Guide
    - System Architecture
    ![How to turn a billion people's random health facts into useful medical knowledge: a pipeline with more steps than your morning routine.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-implementation-guide-bw-academic.jpg)
    - Core Algorithm: Pair Generation
    - Core Algorithm: Baseline Separation
    - Algorithm 3: Predictor Impact Score Calculation
    - Reference Implementation
  - Regulatory Considerations
    - Positioning Relative to RCTs
    ![RCTs are good at some things. Observational data is good at other things. Using both is called 'not being an idiot,' but it needed a diagram.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-positioning-relative-to-rcts-bw-academic.jpg)
    - Evidence Hierarchy Integration
    - FDA Real-World Evidence Framework Alignment
    ![The FDA's real-world evidence framework: a beautiful plan for using real data that they mostly ignore in favor of asking rats to get cancer.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-fda-real-world-evidence-framework-alignment-bw-academic.jpg)
  - Validation Framework {#sec-dfda-validation-framework}
    - The Critical Question
    ![If our computer predictions are good, then expensive experiments should confirm the strong predictions more often than weak ones. Shockingly, they do.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-the-critical-question-bw-academic.jpg)
    - Proposed Validation Study
    ![Looking backwards to see if computer predictions matched what actually happened in old experiments. It's backtesting, like Wall Street does before losing your money.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-proposed-validation-study-bw-academic.jpg)
    - Known Limitations Requiring Validation
    ![Three reasons the computer might be wrong: correlation confusion, tweaking the knobs changes everything, and people who track their health are weird.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-known-limitations-requiring-validation-bw-academic.jpg)
  - Future Directions
    - Methodological Improvements
    - Validation Priorities
    ![Four stages of checking if the computer is hallucinating: look at old data, run new tests, ask experts, and wiggle all the numbers to see what breaks.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-validation-priorities-bw-academic.jpg)
    - Implementation Enhancements
  - Conclusion
  - Appendix A: Effect Size Classification
  - Appendix B: Variable Category Defaults
  - Appendix C: Glossary
  - Appendix D: Worked Example
    - Example: Calculating Predictor Impact Score for "Magnesium → Sleep Quality"
  - Appendix E: Analysis Workflow
    ![Fourteen steps to turn messy human health data into clean medical insights. Step 1 is 'receive garbage.' Step 14 is 'produce knowledge.' Steps 2-13 are where the magic happens.](/assets/images/dfda-spec-paper/dfda-spec-paper-section-appendix-e-analysis-workflow-bw-academic.jpg)
