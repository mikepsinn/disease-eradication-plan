# The Optimal Budget Generator: A Causal Inference Protocol for Maximizing Median Health and Wealth Through Public Goods Funding

**Config:** _quarto-obg.yml
**Type:** website
**Files:** 1 | **Words:** 8,912 | **Images:** 27 | **Est. Pages:** ~49

#### knowledge/appendix/optimal-budget-generator-spec.qmd
**Title:** The Optimal Budget Generator: A Causal Inference Protocol for Maximizing Median Health and Wealth Through Public Goods Funding
**Description:** The Optimal Budget Generator (OBG) uses causal inference, diminishing returns modeling, and cost-effectiveness evidence to determine optimal public goods funding levels that maximize two welfare metrics: real after-tax median income growth and median healthy life years. For each spending category, OBG estimates an Optimal Spending Level (OSL) and produces a gap analysis showing where current government budgets are over- or underfunded relative to evidence-based benchmarks. The Budget Impact Score (BIS) measures confidence in each recommendation based on the quality of causal evidence.
**Stats:** 8,912 words | 1,222 lines | 27 images | ~49p

  - Abstract {.unnumbered}
    ![Three ways to figure out optimal spending combine to show the gap between what you spend and what you should spend. The gap is filled with lobbyists.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-abstract-unnumbered-bw-academic.jpg)
  - System Overview {#obg-system-overview}
    - What Policymakers See
  - Illustrative Example: US Federal Budget Gap Analysis
    - What Budget Analysts See
    - Where This Fits
    ![Budget generator and policy generator both feed into constitutional rules. It's checks and balances, but the checks can do maths.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-system-overview-bw-academic.jpg)
    - Implementation Mechanism
  - Introduction
    - Why Budget Allocation Fails Today
    ![Current budgets: lobbying and 'we've always done it this way.' Result: money goes to things that don't work instead of things that do. Tradition is expensive.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-why-budget-allocation-fails-today-bw-academic.jpg)
    - The RDA Analogy: Optimal Levels, Not Just Marginal Returns
    ![Nutritionists tell you how much vitamin C you need. OSL tells governments how much education funding they need. One prevents scurvy, the other prevents stupid.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-introduction-bw-academic.jpg)
    - What This Framework Provides
    ![Five pieces: evidence-based targets, gap analysis, priority ranking, uncertainty assessment, and wishful thinking. Wait, scratch that last one.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-what-this-framework-provides-bw-academic.jpg)
    - Outcome Metrics: What We're Optimizing
  - Related Work
    - Budget Analysis Frameworks
    ![CBO scores costs. Performance budgeting measures results. Zero-based budgeting questions everything. OBG does all three and shows you the receipts.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-budget-analysis-frameworks-bw-academic.jpg)
    - Evidence-Based Policy Movement
    ![Old way: evaluate programs one at a time. New way: optimize entire budgets at once. It's like organizing your whole kitchen instead of just the spoon drawer.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-evidence-based-policy-movement-bw-academic.jpg)
    - Comparative Public Finance
    ![A conceptual model showing the methodological progression from standard OECD benchmarking to OBG’s causal identification framework and actionable spending targets.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-comparative-public-finance-bw-academic.jpg)
    - How OBG Differs
    ![Three different ways to count money, then deciding where to put it, then measuring how confident you are that you counted correctly. Like checking your restaurant bill three times because you still don't trust yourself.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-how-obg-differs-bw-academic.jpg)
  - Theoretical Framework
    ![A social planner is someone who plans society. They take evidence, weigh it (not literally), and decide how much money to spend on things. It's like meal planning but for countries.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-theoretical-framework-bw-academic.jpg)
    - The Social Planner's Problem
    - Optimal Spending Levels Under Uncertainty
    - Budget Impact Score as Precision Weighting
    ![Three ingredients that tell you how much to trust a number: how good it is, how exact it is, and how old it is. Like checking the expiration date on milk, but for statistics.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-theoretical-framework-bw-academic.jpg)
    - Gap Analysis and Welfare Gains
    - Welfare Bounds Under Model Uncertainty
    - Summary of Theoretical Results
  - Core Methodology
    - Spending Category Data Structure
    ![Boxes connected by lines. The boxes represent different kinds of information. The lines mean they're related. It's a family tree for spreadsheets.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-spending-category-data-structure-bw-academic.jpg)
    - Two Methods for OSL Estimation
  - Diminishing Returns Modeling
    - The Core Concept
    ![The first dollar you spend helps a lot. The millionth dollar helps less. The graph tells you when to stop spending money on one thing and start spending it on another thing.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-the-core-concept-bw-academic.jpg)
    - Finding the "Knee" of the Curve
    - Estimation Methods
    - Worked Example: K-12 Education Spending
  - Worked Example: Pragmatic Clinical Trials
    - The Highest-Return Public Investment
    ![Some ways of spending government money work better than others. Also, cheap trials work as well as expensive trials, but cost less. This required two charts to explain.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-the-highest-return-public-investment-bw-academic.jpg)
    - OSL Estimation
    - Diminishing Returns Analysis
    ![We spend 500 million on pragmatic trials. The graph says we should spend 50 to 100 billion. We are so far to the left of where we should be that we're practically off the chart.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-diminishing-returns-analysis-bw-academic.jpg)
    - Cost-Effectiveness Calculation
    - Gap Analysis
    - Why This Category Dominates
  - Cost-Effectiveness Threshold Analysis
    - The Standard Health Economics Approach
    - Building Up from Intervention-Level Data
    ![Four boxes with arrows between them. The boxes show how you take lots of small numbers and turn them into one big number. Addition with extra steps.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-building-up-from-intervention-level-data-bw-academic.jpg)
    - Worked Example: Vaccinations
  - Budget Impact Score (BIS)
    ![A pyramid of trustworthiness. Randomized trials sit at the top wearing a crown. Someone's opinion sits at the bottom, wondering what it did wrong.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-budget-impact-score-bis-bw-academic.jpg)
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
    ![Four ways to check if your answer is wrong. Look for weird numbers. Make sure you did the same thing every time. Check if it changes when time passes. Wiggle the inputs and see if it explodes.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-robustness-checks-bw-academic.jpg)
  - Interpreting Results
    - Gap Ranges and Recommended Actions
    - What the Algorithm Cannot Tell You
  - Pilot Program Prioritization
    - Value of Information for Uncertain Categories
    - Recommended Pilot Designs
    ![Four ways to test if your idea works before spending billions. Option 1: flip a coin. Option 2: do it slowly. Option 3: wait for something to happen and watch. Option 4: check if someone already wrote it down.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-recommended-pilot-designs-bw-academic.jpg)
    - Learning Feedback Loop
    ![A circle with four boxes in it. The boxes say: spend money, see what happened, learn from it, spend money differently. Then you go around the circle again. It's like learning from your mistakes, but on purpose.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-learning-feedback-loop-bw-academic.jpg)
  - Data Sources
    - Cross-Country Databases
    - Cost-Effectiveness Databases
    - US Budget Data
  - Limitations
    - Diminishing Returns Uncertainty
    ![The line goes up fast, then slower, then basically flat. The shaded bit means we're guessing. The dashed bit means we're really guessing and probably shouldn't be.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-diminishing-returns-uncertainty-bw-academic.jpg)
    - Implementation Capacity
    ![Money goes through two filters before it becomes results. The filters are called 'make sure you can actually do this' and 'do it slowly so you don't mess up.' Filters for money that don't involve coffee.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-implementation-capacity-bw-academic.jpg)
  - Validation Framework
    - Retrospective Validation
    ![Three steps to check if you were right. Step 1: go back in time (mathematically). Step 2: pretend you did what you should have done. Step 3: compare it to what actually happened. Like replaying a football match in your head where you win.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-retrospective-validation-bw-academic.jpg)
    - Prospective Validation
    ![How to prove you're not making things up. Write down your prediction before it happens. Tell everyone. Wait. Check if you were right. It's the scientific method for not lying to yourself.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-prospective-validation-bw-academic.jpg)
    - Success Metrics
    - Validation Status
  - Sensitivity Analysis
    - Parameter Sensitivity
    - Scenario Analysis
    ![Three answers to the same question. The pessimistic one assumes everything will go wrong. The optimistic one assumes everything will go right. The base case assumes you'll be disappointed but not surprised.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-scenario-analysis-bw-academic.jpg)
  - Conclusion
  - Acknowledgments {.unnumbered}
  - References
  - Appendix A: Analysis Workflow {.appendix}
    - Complete OBG Analysis Pipeline
  - Appendix B: Glossary {.appendix}
    - Core Concepts
    ![You put evidence and comparison data into the machine. The machine tells you two things: how much you should spend, and how sure you should be. Then you notice you're spending the wrong amount.](/assets/images/optimal-budget-generator-spec/optimal-budget-generator-spec-section-core-concepts-bw-academic.jpg)
    - Estimation Methods
    - Evidence Quality
    - Output Concepts
  - Appendix C: Illustrative Comparison to US Budget {.appendix}
    - Illustrative US Discretionary Budget vs. OSL Targets
