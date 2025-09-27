# DIH Book Launch - Master To-Do List

This is the master checklist for completing and launching the book, website, and presentation. The tasks are ordered to ensure foundational work is completed first, followed by content creation and final polishing.

---

## Phase 1: Foundation & Setup

- [x] **Project Configuration:**
    - [x] Review and finalize `_quarto.yml` to ensure all book, website, and presentation settings are correct.
    - [x] Confirm Python virtual environment (`dih-project-kernel`) is correctly configured and documented.
- [ ] **Standards & Guidelines:**
    - [x] Review `CONTRIBUTING.md` to ensure all guidelines are up-to-date and clear for all contributors.
    - [ ] Review `brain/book/references.md` for formatting consistency and sort all entries alphabetically.
- [ ] **Asset Management:**
    - [ ] Create a central directory for Python visualization scripts (e.g., `scripts/charts/`).
    - [ ] Establish a consistent, minimalistic, and classy aesthetic/theme for all Python-generated visuals.

---

## Phase 1.5: Content Consolidation from Orphaned Files

This phase consolidates ~45 orphaned files from brain/book/ that contain valuable content not in the current table of contents. Files will be processed, valuable content merged, and originals moved to archive/.

### High-Priority Economic Content
- [ ] **Merge ROI and Financial Models:**
    - [ ] Extract 463:1 dFDA ROI calculation from `economics/dfda-cost-benefit-analysis.md` → merge into `victory-bonds.qmd`
    - [ ] Extract intervention comparison data from `economics/intervention-comparison-table.md` → merge into `economic-impact-summary.md`
    - [ ] Extract peace dividend calculations from `economics/1-percent-treaty-peace-dividend-analysis.md` → merge into relevant chapters
    - [ ] Extract QALY framework from `economics/quantitative-value-medical-treatment.md` → merge into `economic-impact-summary.md`
    - [ ] Extract accelerated treatment value from `economics/economic-value-of-accelerated-treatments.md` → merge into `dfda.md`

### Fundraising Strategy Integration
- [ ] **Create new fundraising section in Chapter 4:**
    - [ ] Extract $1.2B-$2.5B phase-by-phase plan from `economics/fundraising/fundraising-plan.md`
    - [ ] Extract whale outreach strategy from `economics/fundraising/fundraising-whale-outreach.md`
    - [ ] Extract pre-seed terms from `economics/fundraising/fundraising-pre-seed-terms.md`
    - [ ] Extract budget breakdown from `economics/fundraising/fundraising-budget-breakdown.md`
    - [ ] Create new file: `brain/book/strategy/fundraising-strategy.md` with consolidated content

### Legal and Governance Framework
- [ ] **Enhance legal compliance chapter:**
    - [ ] Extract multi-entity structure from `legal/multi-entity-strategy.md` → merge into `legal-compliance-framework.md`
    - [ ] Extract Right to Trial Act from `legal/right-to-trial-act.md` → create new section in Chapter 4
    - [ ] Extract HHS recommendations from `legal/hhs-policy-recommendations.md` → merge into relevant strategy files
    - [ ] Extract regulatory modifications from `legal/regulations-to-modify-or-rescind.md` → merge into legal framework
    - [ ] Extract impact securities from `legal/impact-securities-reform.md` → merge into VICTORY bonds section

### Strategy and Implementation
- [ ] **Consolidate global referendum details:**
    - [ ] Extract implementation plan from `strategy/global-referendum/global-referendum-implementation.md`
    - [ ] Extract verification protocols from `strategy/global-referendum/global-referendum-verification.md`
    - [ ] Extract viral marketing from `strategy/global-referendum/global-referendum-viral-marketing.md`
    - [ ] Merge all into existing `global-referendum.md`
- [ ] **Add endgame strategy:**
    - [ ] Extract 100-200 year vision from `strategy/the-endgame-phasing-out-war.md` → merge into `utopia-health-and-happiness.md`
- [ ] **Add coalition and advocacy:**
    - [ ] Extract coalition building from `strategy/coalition-building.md` → merge into `co-opt-dont-compete.md`
    - [ ] Extract advocacy strategies from `strategy/highest-leverage-advocacy.md` → merge into relevant strategy files

### Operations and FAQ
- [ ] **Create FAQ chapter:**
    - [ ] Extract Q&A from `FAQ.md` and create new Chapter 8 or appendix
    - [ ] Include common objections and responses
- [ ] **Create operations appendix:**
    - [ ] Extract operational content from `operations.md`
    - [ ] Extract roadmap from `roadmap.md`
    - [ ] Create `brain/book/reference/operations-roadmap.md`

### Vision and Meta Content
- [ ] **Integrate vision content:**
    - [ ] Extract vision from `vision.md` → merge into introduction or futures chapter
    - [ ] Archive section overview files (`problem.md`, `solution.md`, `proof.md`, etc.)

### Final Cleanup
- [ ] **Move all processed files to archive:**
    - [ ] Create archive log documenting what was extracted from each file
    - [ ] Move processed files to `brain/book/archive/`
    - [ ] Update any broken internal links
- [ ] **Generate consolidation report:**
    - [ ] List all content merges performed
    - [ ] Document any content that was archived without merging
    - [ ] Identify any remaining gaps or duplications

---

## Phase 2: Content Perfection (Chapter by Chapter)

This phase involves a thorough review of every document listed in the official Table of Contents. Each file must be reviewed for three core requirements: humor, sourcing, and visual engagement.

### Chapter 1: The Problem: A $119 Trillion Mistake

- **1.0 Why We're Like This: The Evolutionary Trap (`/brain/book/problem/the-evolutionary-trap.md`)**
    - [ ] Create the file and write content about the selfish gene, evolutionary psychology, and how our brains evolved for scarcity
    - [ ] Explain how tendencies toward gluttony and violence were survival advantages but are now leading to extinction
    - [ ] Add humor while maintaining scientific accuracy
    - [ ] Source all evolutionary biology and psychology claims to `references.md`
    - [ ] Create visual showing evolution from scarcity-optimized brain to modern abundance problems
- **1.1 The Cost of War: Humanity's Most Expensive Hobby (`/brain/book/problem/cost-of-war.md`)**
    - [ ] Review for tone and humor (dark humor about human stupidity, absurd analogies).
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Identify opportunities for and create Python-generated visuals (e.g., chart comparing military spending to other sectors).
- **1.2 The Cost of Disease: A Slow-Motion Apocalypse (`/brain/book/problem/cost-of-disease.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Identify opportunities for and create Python-generated visuals (e.g., chart showing disease cost vs. research spending).
- **1.3 The System is Broken: Why We Don't Have Cures (`/brain/book/problem/why-the-system-is-broken.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a summary diagram (Mermaid) illustrating the core bottlenecks.
- **1.3.1 Why NIH is Terrible at Funding Research (`/brain/book/problem/nih-funding-is-broken.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a chart showing NIH grant success rates over time.
- **1.3.2 Why the FDA is Unsafe and Ineffective (`/brain/book/problem/fda-approvals-are-broken.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a visual timeline of the 17-year drug approval process.
- **1.3.3 Why Representative Democracy is Unrepresentative (`/brain/book/problem/democracy-is-broken.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a diagram illustrating the flow of lobbying money to policy outcomes.

### Chapter 2: The Solution: A Better Deal

- **2.1 The 1% Treaty (`/brain/book/solution/1-percent-treaty.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a simple visual showing 1% being carved out of the total military budget.
- **2.2 The Decentralized Institutes of Health (DIH) (`/brain/book/solution/dih.qmd`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Ensure all diagrams (like the money flow chart) are clear and follow the project's aesthetic.
- **2.3 The Decentralized FDA (dFDA) (`/brain/book/solution/dfda.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Add a visual comparing the cost-per-patient in traditional vs. dFDA trials.
- **2.4 Wishocracy (`/brain/book/solution/wishocracy.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a simplified diagram of the Aggregated Pairwise Preference Allocation (APPA) voting process.

### Chapter 3: Economics

- **3.1 VICTORY Bonds (`/brain/book/economics/victory-bonds.qmd`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a chart projecting investor returns vs. traditional investments (e.g., S&P 500).
- **3.2 Societal Impact Analysis (`/brain/book/economics/economic-impact-summary.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a summary visual of the total economic benefit (Peace Dividend).

### Chapter 4: The Strategy

- **4.1 The Core Strategy: Co-opt, Don't Compete (`/brain/book/strategy/co-opt-dont-compete.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a diagram showing the incentive alignment for different actors (politicians, MIC, etc.).
- **4.2 Global Referendum (`/brain/book/strategy/global-referendum.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a map or visual showing the 3.5% target population by region.
- **4.3 Legal Compliance (`/brain/book/strategy/legal-compliance-framework.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create a diagram showing the legal structure (Super PACs, etc.).

### Chapter 5: The Proof

- **5.1 Precedent 1: The 80X Efficiency Gain (`/brain/book/reference/recovery-trial.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Ensure data on the RECOVERY trial is presented visually.
- **5.2 Precedent 2: Historical Precedents (`/brain/book/proof/historical-precedents.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
- **5.3 Precedent 3: Historical Evidence for Decentralized Trials (`/brain/reference/historical-evidence-supporting-decentralized-efficacy-trials.md`)**
    - [ ] Review for tone and humor.
    - [ ] Verify all claims are sourced to `references.md`.
- **5.4 The Biological Truth: Your Body is a Machine That Can Be Fixed (`/brain/book/proof/body-as-repairable-machine.md`)**
    - [ ] Create the file with irrefutable scientific evidence about biological repair mechanisms
    - [ ] Use the 50-year-old car restoration analogy throughout
    - [ ] Include evidence from regenerative medicine, stem cells, tissue engineering, etc.
    - [ ] Add humor while maintaining scientific rigor
    - [ ] Source all scientific claims to `references.md`
    - [ ] Create visual comparing car maintenance/restoration to human body repair

### Chapter 6: The Futures

- **6.1 The Dystopia: What Happens When We Keep Building Skynet (`/brain/book/futures/dystopia-skynet-wins.md`)**
    - [ ] Review for tone and dark humor balance.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create timeline visualization showing military AI development vs disease deaths.
    - [ ] Add chart comparing military spending to potential medical breakthroughs.
- **6.2 The Utopia: The World After We Choose Life Over Death (`/brain/book/futures/utopia-health-and-happiness.md`)**
    - [ ] Review for tone and inspirational quality.
    - [ ] Verify all claims are sourced to `references.md`.
    - [ ] Create visualization showing the treaty progression (1% to 50% over time).
    - [ ] Add chart showing life expectancy and quality of life improvements.
    - [ ] Create economic model visualization of the peace dividend growth.

### Chapter 7: Join the War on Disease

- **7.1 How You Can Help (`/brain/book/call-to-action.md`)**
    - [ ] Review for clarity and tone.
    - [ ] Ensure all links are correct and actionable.

---

## Phase 3: Finalization & Launch

- [ ] **Content Finalization:**
    - [ ] **Master Overview (`index.qmd`):** Perform a final review to ensure it's punchy, hilarious, and perfectly sets the stage for the detailed chapters.
    - [ ] **Full Manuscript Proofread:** Read the entire book from start to finish to check for flow, consistency, and any remaining typos or errors.
- [ ] **Build & Test All Formats:**
    - [ ] **Website:** Run `quarto render` and thoroughly test the generated website on multiple browsers. Check all links, images, and interactive elements.
    - [ ] **PDF:** Generate the PDF output and review it for any formatting issues, page breaks, or rendering errors.
    - [ ] **Presentation (`presentation.qmd`):**
        - [ ] Create the content for the slide presentation, summarizing the key points of the book.
        - [ ] Generate the presentation slides and ensure they are visually appealing and functional.
- [ ] **Launch:**
    - [ ] Deploy the website to the target host (e.g., GitHub Pages).
    - [ ] Prepare the PDF and presentation files for distribution.
    - [ ] Announce the launch!
