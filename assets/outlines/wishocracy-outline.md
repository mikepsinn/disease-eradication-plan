# Wishocracy: Solving the Democratic Principal-Agent Problem Through Pairwise Preference Aggregation

**Config:** _quarto-wishocracy.yml
**Type:** website
**Files:** 1 | **Words:** 10,527 | **Images:** 35 | **Est. Pages:** ~60

#### knowledge/appendix/wishocracy-paper.qmd
**Title:** Wishocracy: Solving the Democratic Principal-Agent Problem Through Pairwise Preference Aggregation
**Description:** Representative democracy suffers from an inescapable principal-agent problem where elected officials' incentives diverge from citizen welfare. Wishocracy introduces RAPPA (Randomized Aggregated Pairwise Preference Allocation), which aggregates citizen preferences through cognitively tractable pairwise comparisons and creates accountability via Citizen Alignment Scores that channel electoral resources toward politicians who actually represent what citizens want.
**Stats:** 10,527 words | 785 lines | 35 images | ~60p

- **Abstract**
    ![You compare things in pairs, math adds it up, politicians get scored on whether they do what you wanted, and bonds reward the ones who listen.](/assets/images/wishocracy-paper/wishocracy-paper-section-abstract-bw-academic.jpg)
- **Introduction: The Preference Aggregation Problem**
    ![Four ways to run a country: elect someone to decide (traditional), decide everything yourself (exhausting), let experts decide (undemocratic), or compare pairs and let math decide (new).](/assets/images/wishocracy-paper/wishocracy-paper-section-introduction-the-preference-aggregation-problem-bw-academic.jpg)
- **Theoretical Foundations**
  - **The Analytic Hierarchy Process**
  - **The Preference Intensity Problem**
    ![90/10 means you really care. 55/45 means you barely care. Democracy currently can't tell the difference, like a thermostat that only has two settings: off and inferno.](/assets/images/wishocracy-paper/wishocracy-paper-section-the-preference-intensity-problem-bw-academic.jpg)
  - **Collective Intelligence and the Wisdom of Crowds**
    ![A conceptual diagram illustrating Surowiecki’s four conditions for collective intelligence and a visualization of Page’s diversity prediction theorem showing how diversity reduces collective error.](/assets/images/wishocracy-paper/wishocracy-paper-section-collective-intelligence-and-the-wisdom-of-crowds-bw-academic.jpg)
  - **Related Work and Positioning in the Literature**
    ![Five ways to let people decide things, rated by how hard they are to use, how well they capture what you want, and whether they work at scale. RAPPA wins at not melting your brain.](/assets/images/wishocracy-paper/wishocracy-paper-section-related-work-and-positioning-in-the-literature-bw-academic.jpg)
- **Mechanism Design: Randomized Aggregated Pairwise Preference Allocation**
  - **Core Mechanism**
    ![List problems, compare them in pairs, convert to ratios, aggregate everyone's ratios, allocate budget. It's like democracy but with less screaming and more math.](/assets/images/wishocracy-paper/wishocracy-paper-section-core-mechanism-bw-academic.jpg)
    - Scenario: Federal Budget Preferences
  - **Formal Properties**
    ![More options means more work for voters. Some systems scale gently. Others require a PhD in combinatorics. RAPPA stays manageable, like a reasonable person.](/assets/images/wishocracy-paper/wishocracy-paper-section-formal-properties-bw-academic.jpg)
  - **Formal Model**
    ![Your preferences become ratios, ratios become matrices, matrices get aggregated, aggregation becomes budget. It's democracy digestion, where math is the stomach.](/assets/images/wishocracy-paper/wishocracy-paper-section-formal-model-bw-academic.jpg)
  - **Computational Complexity and Scalability**
    ![RAPPA works for small towns, big cities, and entire nations. The computer does more work, but you don't. It's like having a calculator that scales to government size.](/assets/images/wishocracy-paper/wishocracy-paper-section-computational-complexity-and-scalability-bw-academic.jpg)
  - **Comparative Information & Welfare Analysis**
    ![Governance is trying to match what people want with what government does. Representative democracy fails at this. RAPPA optimizes it, like Google Maps but for democracy.](/assets/images/wishocracy-paper/wishocracy-paper-section-comparative-information-welfare-analysis-bw-academic.jpg)
    - **Information-Theoretic Superiority**
    ![The flatline of democracy: Public support (0 percent to 100 percent) has near-zero impact on the probability of policy adoption (flat at ~30 percent), whereas elite support strongly correlates with adoption. Data from @gilens2014.](../../assets/images/bill-public-support-vs-chance-of-adoption-what-actually-happens.png)
    - **Welfare Maximization: The "Median vs. Mean" Proof**
    - **Principal-Agent Cost Elimination**
    ![Representative democracy: your preferences go to a politician who ignores them. Wishocracy: your preferences go into an algorithm that implements them. One has a middleman, the other has middleware.](/assets/images/wishocracy-paper/wishocracy-paper-section-principal-agent-cost-elimination-bw-academic.jpg)
- **Empirical Precedents and Evidence Base**
  - **Porto Alegre Participatory Budgeting**
    ![When Porto Alegre let citizens decide the budget, participation increased 20x and services multiplied. Turns out people care more when they get to choose where money goes.](/assets/images/wishocracy-paper/wishocracy-paper-section-porto-alegre-participatory-budgeting-bw-academic.jpg)
  - **Taiwan's Digital Democracy Experiments**
    ![Taiwan used pairwise comparisons to find consensus on Uber regulation. It worked. Democracy upgraded from shouting match to intelligent conversation.](/assets/images/wishocracy-paper/wishocracy-paper-section-taiwan-s-digital-democracy-experiments-bw-academic.jpg)
  - **Stanford Participatory Budgeting Platform Research**
  - **Reference Implementation: Wishocracy.org**
    ![Theory says RAPPA works. Wishocracy.org tests whether theory is lying. Interface, algorithms, identity verification: all the boring parts that make democracy not collapse.](/assets/images/wishocracy-paper/wishocracy-paper-section-reference-implementation-wishocracy-org-bw-academic.jpg)
    - **Category Selection and Validation Methodology**
    ![Some spending returns $125 per dollar. Other spending loses money. We fund both equally because democracy doesn't check receipts.](/assets/images/wishocracy-paper/wishocracy-paper-section-category-selection-and-validation-methodology-bw-academic.jpg)
    - **Zero-Funding Filter Optimization**
    ![Remove things you don't care about, cut your work in half. It's like a multiple choice test where you can delete the stupid questions.](/assets/images/wishocracy-paper/wishocracy-paper-section-zero-funding-filter-optimization-bw-academic.jpg)
    - **Hierarchical Category Structure**
    ![Decide big categories first, drill into details if you care, let math combine everything. Like a restaurant menu where you must choose protein but sides are optional.](/assets/images/wishocracy-paper/wishocracy-paper-section-hierarchical-category-structure-bw-academic.jpg)
    - **Framing Bias and Mitigation**
    ![How to avoid biasing the questions: find the bias, have enemies review it, test it in parallel, document everything. Democracy with peer review.](/assets/images/wishocracy-paper/wishocracy-paper-section-framing-bias-and-mitigation-bw-academic.jpg)
- **Addressing Potential Criticisms**
  - **Participation and Digital Divide**
  - **Manipulation and Sybil Attacks**
    ![Fake voters get random comparisons, so their fraud gets diluted across thousands of pairs. It's like trying to poison a lake with a eyedropper.](/assets/images/wishocracy-paper/wishocracy-paper-section-manipulation-and-sybil-attacks-bw-academic.jpg)
  - **Preference Laundering and Manufactured Consent**
  - **Complexity of Real Policy Trade-offs**
    ![Citizens say what they want. Experts figure out how to do it. Division of labor, like how you tell the chef you want pasta but don't invade the kitchen.](/assets/images/wishocracy-paper/wishocracy-paper-section-complexity-of-real-policy-trade-offs-bw-academic.jpg)
  - **Legitimacy and Accountability**
    ![Preferences go into algorithm, algorithm makes recommendations, elected officials oversee it. Everyone watches everyone else, like a Mexican standoff but with spreadsheets.](/assets/images/wishocracy-paper/wishocracy-paper-section-legitimacy-and-accountability-bw-academic.jpg)
  - **Failure Modes and Robustness**
    ![Three ways RAPPA breaks: nobody participates, comparisons are too sparse, or attackers coordinate. Three layers of defense against each. Belt, suspenders, and duct tape.](/assets/images/wishocracy-paper/wishocracy-paper-section-failure-modes-and-robustness-bw-academic.jpg)
- **Implementation Pathway: From Information to Incentive Alignment**
    ![The military gets $886 billion. Medical research gets crumbs. Fossil fuels get subsidies. The drug war gets enforcement. We fund what we love: fighting.](/assets/images/wishocracy-paper/wishocracy-paper-section-implementation-pathway-from-information-to-incentive-alignment-bw-academic.jpg)
  - **Why Information Alone Fails: Politicians Respond to Incentives**
    ![E-government returns $125 per dollar. Vaccines return $101. Military expansion loses 30 cents per dollar. We prefer the 30 cent loss.](/assets/images/wishocracy-paper/wishocracy-paper-section-why-information-alone-fails-politicians-respond-to-incentives-bw-academic.jpg)
  - **Three-Phase Implementation**
    - **Phase 1: Informational (Preference Gap Documentation)**
    ![What citizens want versus what government funds. The gap is enormous, like the difference between ordering salad and receiving a flamethrower.](/assets/images/wishocracy-paper/wishocracy-paper-section-phase-1-informational-preference-gap-documentation-bw-academic.jpg)
    - **Phase 2: Accountability Scoring (Politician Alignment Ratings)**
    ![Track how Congress votes, compare to what citizens want, calculate alignment score. It's a report card for democracy, currently showing lots of Fs.](/assets/images/wishocracy-paper/wishocracy-paper-section-phase-2-accountability-scoring-politician-alignment-ratings-bw-academic.jpg)
    - **Phase 3: Incentive Alignment (Integration with Incentive Alignment Bonds)**
    ![Households have $454 trillion. Special interests have $5 trillion. We're letting the 5 outspend the 454. Incentive Alignment Bonds fix this by mobilizing the 454.](/assets/images/wishocracy-paper/wishocracy-paper-phase-3-incentive-alignment-integration-with-incentive-alignment-bonds-bw-academic.jpg)
    ![City budgets: $10 million. Federal budget: $500 billion. The difference is 50,000x, like comparing a lemonade stand to Amazon.](/assets/images/wishocracy-paper/wishocracy-paper-section-why-federal-first-beats-municipal-pilots-bw-academic.jpg)
  - **Why Federal-Scale Priorities**
    ![Citizens want things, government spends money, RAPPA measures the gap and creates financial instruments to close it. Democracy with accounting.](/assets/images/wishocracy-paper/wishocracy-paper-section-why-federal-scale-priorities-bw-academic.jpg)
  - **Evaluation Framework**
    - **Preference Aggregation Quality**
    - **Accountability System Effectiveness**
    - **Incentive Alignment Impact**
  - **Connection to Incentive Alignment Bonds**
    ![You ask people what they want, then pay politicians to do it. Like parenting, but with money instead of guilt.](/assets/images/wishocracy-paper/wishocracy-paper-section-connection-to-incentive-alignment-bonds-bw-academic.jpg)
  - **Connection to Optimocracy**
    ![Democracy asks what you want. Optimocracy does the math. It's like finally hiring an accountant after years of guessing.](/assets/images/wishocracy-paper/wishocracy-paper-section-connection-to-optimocracy-bw-academic.jpg)
- **Conclusion**
    ![How to make representatives represent people: give them a score, then attach money to it. Like training a very expensive dog.](/assets/images/wishocracy-paper/wishocracy-paper-section-conclusion-bw-academic.jpg)
- **Appendix A: The Service Provider Layer**
    ![Layer 1: people say what they want. Layer 2: nerds figure out how. You invented management consulting but made it work.](/assets/images/wishocracy-paper/wishocracy-paper-section-appendix-a-the-service-provider-layer-bw-academic.jpg)
  - References {.unnumbered}
