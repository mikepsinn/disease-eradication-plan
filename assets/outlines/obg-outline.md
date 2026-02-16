# The Optimal Budget Generator: A Causal Inference Protocol for Maximizing Median Health and Wealth Through Public Goods Funding

**Config:** _quarto-obg.yml
**Type:** website
**Files:** 1 | **Words:** 8,912

#### knowledge/appendix/optimal-budget-generator-spec.qmd
**Title:** The Optimal Budget Generator: A Causal Inference Protocol for Maximizing Median Health and Wealth Through Public Goods Funding
**Description:** The Optimal Budget Generator (OBG) uses causal inference, diminishing returns modeling, and cost-effectiveness evidence to determine optimal public goods funding levels that maximize two welfare metrics: real after-tax median income growth and median healthy life years. For each spending category, OBG estimates an Optimal Spending Level (OSL) and produces a gap analysis showing where current government budgets are over- or underfunded relative to evidence-based benchmarks. The Budget Impact Score (BIS) measures confidence in each recommendation based on the quality of causal evidence.
**Stats:** 8,912 words | 1,223 lines

  - Abstract {.unnumbered}
  - System Overview {#obg-system-overview}
    - What Policymakers See
  - Illustrative Example: US Federal Budget Gap Analysis
    - What Budget Analysts See
    - Where This Fits
    - Implementation Mechanism
  - Introduction
    - Why Budget Allocation Fails Today
    - The RDA Analogy: Optimal Levels, Not Just Marginal Returns
    - What This Framework Provides
    - Outcome Metrics: What We're Optimizing
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
    - Two Methods for OSL Estimation
  - Diminishing Returns Modeling
    - The Core Concept
    - Finding the "Knee" of the Curve
    - Estimation Methods
    - Worked Example: K-12 Education Spending
  - Worked Example: Pragmatic Clinical Trials
    - The Highest-Return Public Investment
    - OSL Estimation
    - Diminishing Returns Analysis
    - Cost-Effectiveness Calculation
    - Gap Analysis
    - Why This Category Dominates
  - Cost-Effectiveness Threshold Analysis
    - The Standard Health Economics Approach
    - Building Up from Intervention-Level Data
    - Worked Example: Vaccinations
  - Budget Impact Score (BIS)
    - BIS Calculation
    - Evidence Grading from BIS
  - Gap Analysis and Priority Ranking
    - Computing Gaps
    - Priority Score
    - Illustrative Example: Priority Ranking
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
    - Cross-Country Databases
    - Cost-Effectiveness Databases
    - US Budget Data
  - Limitations
    - Diminishing Returns Uncertainty
    - Implementation Capacity
  - Validation Framework
    - Retrospective Validation
    - Prospective Validation
    - Success Metrics
    - Validation Status
  - Sensitivity Analysis
    - Parameter Sensitivity
    - Scenario Analysis
  - Conclusion
  - Acknowledgments {.unnumbered}
  - References
  - Appendix A: Analysis Workflow {.appendix}
    - Complete OBG Analysis Pipeline
  - Appendix B: Glossary {.appendix}
    - Core Concepts
    - Estimation Methods
    - Evidence Quality
    - Output Concepts
  - Appendix C: Illustrative Comparison to US Budget {.appendix}
    - Illustrative US Discretionary Budget vs. OSL Targets
