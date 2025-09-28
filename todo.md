# DIH Book Launch - Master To-Do List

This is the master checklist for completing and launching the book, website, and presentation. 

**UPDATED STRATEGY (2025-09-27):** Write first, research later. Focus on getting all content written with placeholder citations, then do a systematic research pass.

## Phase 0.5: DIH as Free Market Alternative to NIH Central Planning (IN PROGRESS)

### Core Conceptual Reframing: NIH = Communism, DIH = Capitalism

**NEW FRAMING:** Position DIH as the free market/capitalist alternative to NIH's Soviet-style central planning. Leverage:
- **Hayek's Information Theory**: Markets as superior information aggregation mechanisms
- **Wisdom of Crowds**: Distributed decision-making beats expert committees
- **Market Mechanisms**: Price signals, competition, and incentives vs bureaucracy
- **Blockchain Question**: Evaluate if necessary for transparency/anti-corruption

### Files to Update with Market-Based Framing:

- [ ] **Core DIH Positioning:**
    - [ ] `brain/book/solution/dih.qmd` - Reframe as market-based research funding system
    - [ ] `brain/book/solution/dfda.md` - Emphasize market competition in trials
    - [ ] `brain/book/solution/wishocracy.md` - Position as inequality-addressing mechanism within capitalist framework
    - [ ] `brain/book/solution/1-percent-treaty.md` - Show transition from central planning to markets

- [ ] **Problem Diagnosis (New Angle):**
    - [ ] Chapter 1.3.1 "Why NIH is Terrible" - Frame as failure of central planning
    - [ ] Add comparison: NIH grant committees = Soviet planning bureaus
    - [ ] Show information bottlenecks and misallocated resources

- [ ] **Economic Arguments:**
    - [ ] `brain/book/economics/victory-bonds.qmd` - Markets pricing future health gains
    - [ ] `brain/book/economics/economic-impact-summary.md` - Market efficiency vs bureaucratic waste

### Key Conceptual Shifts:

1. **NIH = Central Planning Problems:**
   - Information bottlenecks (committees can't know all science)
   - Political capture and bureaucratic incentives
   - Slow adaptation to new information
   - Winner-picking by committees vs market discovery

2. **DIH = Market Solutions:**
   - Distributed knowledge aggregation (Hayek)
   - Competition between research approaches
   - Price signals for research value
   - Rapid iteration and failure tolerance

3. **Wishocracy = Addressing Market Failures:**
   - Democratic input for public goods
   - Equity considerations in pure capitalism
   - Collective wisdom for research priorities
   - Balance between efficiency and fairness

4. **Insurance Model Reconsideration:**
   - May keep as implementation detail
   - Or pivot to direct market mechanisms
   - Focus on incentives and information flow

### New Theoretical Foundations to Incorporate:

- [ ] **Hayekian Knowledge Problem**: Why NIH can't efficiently allocate $48B
- [ ] **Prediction Markets**: Could DIH use them for research prioritization?
- [ ] **Wisdom of Crowds**: James Surowiecki's principles applied to research
- [ ] **Public Choice Theory**: Why NIH serves bureaucrats, not patients
- [ ] **Mechanism Design**: Optimal incentives for medical innovation
- [ ] **Blockchain/Transparency**: Necessary or nice-to-have for anti-corruption?

### Writing Tasks:

- [ ] Draft new introduction comparing NIH to Gosplan (Soviet planning committee)
- [ ] Create comparison table: Central Planning vs Market Mechanisms in Research
- [ ] Write section on Hayek's "Use of Knowledge in Society" applied to medical research
- [ ] Develop concrete examples of market mechanisms in DIH operations
- [ ] Address "but healthcare isn't a normal market" objections

---

## Phase 0: Core Improvements (COMPLETED)

- [x] **Clarify Core Benefits Focus:**
    - [x] Updated CONTRIBUTING.md to emphasize focusing on OUTCOMES (80X efficiency, speed, scale) over mechanisms (patient control, DAOs)
    - [x] Revised DIH chapter to lead with concrete benefits: 80X cost efficiency, 10X speed, 1,000X treatments tested
    - [x] Updated index.qmd to emphasize measurable outcomes in the 6-step process
    - [x] Added emphasis on econometric optimization to minimize DALYs/maximize QALYs

---

## Phase 1: Foundation & Setup ✅

- [x] **Project Configuration:**
    - [x] Review and finalize `_quarto.yml` to ensure all book, website, and presentation settings are correct.
    - [x] Confirm Python virtual environment (`dih-project-kernel`) is correctly configured and documented.
- [x] **Standards & Guidelines:**
    - [x] Review `CONTRIBUTING.md` to ensure all guidelines are up-to-date and clear for all contributors.

---

## Phase 1.5: Clean brain/book/ Folder Completely (IN PROGRESS)

### STRATEGY: Extract ONLY valuable sources and unique ideas, then DELETE

**The orphaned files have terrible writing. We're ONLY keeping:**
1. **Sources/citations** → Add to `brain/book/references.md`
2. **Unique data/calculations** → Note for use in real chapters
3. **Ideas not yet covered** → Note for incorporation

**Everything else gets deleted. The writing style sucks and needs complete rewrite per CONTRIBUTING.md.**

#### Files to Process (60 total):

**⚠️ STRUCTURAL CONSIDERATION:**
Part IV: 4.2 "The ROI" is getting too much content. Consider splitting into:
- 4.2a: **Treaty Peace Dividend** ($24B redirect, $92B savings from 1% less war)
- 4.2b: **dFDA Efficiency Gains** (463:1 ROI from 80X cheaper trials)
- 4.2c: **DIH Market Allocation** (Better funding via markets vs committees)
- 4.2d: **Combined Impact** (How all three multiply together)

**Economics (18 files) - COMPLETE ACTION PLAN:**

- [ ] **`1-percent-treaty-peace-dividend-analysis.md`**
  - Content: $24.43B redirect, $91.97B savings breakdown
  - Action: Create `brain/charts/treaty-peace-dividend-waterfall.qmd`
  - Delete after extraction

- [ ] **`dfda-cost-benefit-analysis.md`** (CRITICAL - 33K tokens!)
  - Content: 463:1 ROI, platform costs, 840K QALYs/year
  - Action: Extract to multiple reusable charts:
    - `brain/charts/dfda-roi-waterfall.qmd` (463:1 from trial efficiency)
    - `brain/charts/dfda-qaly-impact.qmd` (840K QALYs/year)
    - `brain/charts/dfda-platform-costs.qmd` (build & operational costs)
  - **CREATE NEW SECTION:** Part IV: 4.2b "dFDA Efficiency Returns"
  - Delete after extraction

- [ ] **`intervention-comparison-table.md`**
  - Content: Compares dFDA to smallpox eradication, vaccines, etc.
  - Action: Create `brain/charts/health-intervention-roi-comparison.qmd`
  - Delete after extraction

- [ ] **`quantitative-value-medical-treatment.md`**
  - Content: QALY framework explanation
  - Action: Extract to Part III: 3.3 (Incentive Alignment) or new theory chapter
  - Delete after extraction

- [ ] **`economic-value-of-accelerated-treatments.md`**
  - Content: Value of faster drug development
  - Action: Extract key data to Part II: 2.2 (dFDA benefits)
  - Delete after extraction

- [ ] **`financial-model.md`**
  - Action: Check for unique data → Part IV: 4.5 Timeline/Budget
  - Delete after extraction

- [ ] **`health-savings-sharing-model.md`**
  - Action: Check for unique content → Part IV: 4.3 Business Model
  - Delete after extraction

- [ ] **`investor-risk-analysis.md`**
  - Action: Extract to Part IV: 4.1 VICTORY Bonds
  - Delete after extraction

- [ ] **`operational-budget-model.md`**
  - Content: 36-month implementation budget
  - Action: Extract to Part IV: 4.5 Timeline
  - Delete after extraction

- [ ] **`value-of-automating-research.md`**
  - Action: Extract automation benefits to Part II: 2.2 dFDA
  - Delete after extraction

- [ ] **Files already in TOC (keep):**
  - `economic-impact-summary.md` → Part IV: 4.2 ✓
  - `victory-bonds.qmd` → Part IV: 4.1 ✓

- [ ] **Likely duplicates (delete):**
  - `dfda-cost-benefit.qmd` (check vs .md)
  - `economic-summary.qmd` (check vs economic-impact-summary.md)
  - `humanity-budget-overview.qmd` (check for unique visuals)
  - `peace-dividend-analysis.qmd` (check vs 1-percent-treaty version)
  - `victory-bonds.html` (generated file)
  - `economic_models.ipynb` (check for unique calculations)

**Governance (3 files):**

- [ ] **`governance/dih-onchain-architecture.md`**
  - Content: Blockchain/DAO governance details
  - Action: Extract to Part IV: 4.4 Infrastructure (blockchain discussion)
  - Delete after extraction

- [ ] **`governance/organizational-structure.md`**
  - Content: DIH organizational design
  - Action: Extract to Part II: 2.1 DIH market structure
  - Delete after extraction

- [ ] **`governance.md`**
  - Action: Section overview file → Delete
**Legal (3 files):**

- [ ] **`legal/community-governance-framework.md`**
  - Action: Extract to Part II: 2.4 Wishocracy
  - Delete after extraction

- [ ] **`legal/impact-securities-reform.md`**
  - Content: Legal framework for VICTORY bonds
  - Action: Extract to Part IV: 4.1 VICTORY Bonds
  - Delete after extraction

- [ ] **`legal.md`**
  - Action: Section overview file → Delete

**Partners (1 file):**

- [ ] **`partners/incentives.md`**
  - Content: Stakeholder incentive alignment
  - Action: Extract to Part III: 3.3 Incentive Alignment
  - Delete after extraction

**Problem (7 files):**

- [ ] **Files already in TOC (keep):**
  - `problem/the-evolutionary-trap.md` → Part I: 1.1 ✓
  - `problem/cost-of-war.md` → Part I: 1.2 ✓
  - `problem/cost-of-disease.md` → Part I: 1.3 ✓
  - `problem/nih-funding-is-broken.md` → Part I: 1.4 ✓
  - `problem/fda-approvals-are-broken.md` → Part I: 1.5 ✓

- [ ] **`problem/why-the-system-is-broken.md`**
  - Action: Extract unique points to Part I: 1.6-1.8 (Regulatory Capture, Democracy, Failed Reforms)
  - Delete after extraction

- [ ] **`problem.md`**
  - Action: Section overview file → Delete

**Proof (3 files):**

- [ ] **Files already in TOC (keep):**
  - `proof/body-as-repairable-machine.md` → Part III: 3.4 ✓
  - `proof/historical-precedents.md` → Part VI: 6.2 ✓

- [ ] **`proof.md`**
  - Action: Section overview file → Delete

**Solution (7 files):**

- [ ] **Files already in TOC (keep):**
  - `solution/dih.qmd` → Part II: 2.1 ✓
  - `solution/dfda.md` → Part II: 2.2 ✓
  - `solution/1-percent-treaty.md` → Part II: 2.3 ✓
  - `solution/wishocracy.md` → Part II: 2.4 ✓
  - `solution/dih-integration-model.md` → Part IV: 4.3 ✓

- [ ] **`solution/dih-core-benefits.md`**
  - Content: Additional DIH benefits
  - Action: Extract to Part II: 2.1
  - Delete after extraction

- [ ] **`solution.md`**
  - Action: Section overview file → Delete

**Strategy (12 files):**

- [ ] **Files already in TOC (keep):**
  - `strategy/co-opt-dont-compete.md` → Part V: 5.1 ✓
  - `strategy/global-referendum.md` → Part V: 5.2 ✓
  - `strategy/legal-compliance-framework.md` → Part V: 5.3 ✓
  - `strategy/fundraising-strategy.md` → Part V: 5.4 ✓

- [ ] **`strategy/1-percent-treaty.md`**
  - Action: Check if duplicate of solution version → Likely delete

- [ ] **`strategy/coalition-building.md`**
  - Content: Partnership strategy
  - Action: Extract to Part V: 5.1
  - Delete after extraction

- [ ] **`strategy/dfda-implementation-via-executive-action.md`**
  - Content: Executive order path
  - Action: Extract to Part V: 5.3 Legal
  - Delete after extraction

- [ ] **`strategy/free-rider-solution.md`**
  - Content: Treaty enforcement mechanism
  - Action: Extract to Part II: 2.6 Treaty Enforcement
  - Delete after extraction

- [ ] **`strategy/hhs-dFDA-policy-recommendations.md`**
  - Content: HHS policy specifics
  - Action: Extract to Part V: 5.3 Legal
  - Delete after extraction

- [ ] **`strategy/highest-leverage-advocacy.md`**
  - Content: Lobbying ROI ($1:$1,813)
  - Action: Extract data to Part V: 5.1
  - Delete after extraction

- [ ] **`strategy/open-ecosystem-and-bounty-model.md`**
  - Content: Open source strategy
  - Action: Extract to Part IV: 4.4 Infrastructure
  - Delete after extraction

- [ ] **`strategy.md`**
  - Action: Section overview file → Delete

**Other Files (8 in root/subdirs):**

- [ ] **`call-to-action.md`** → Part VIII (already in TOC) ✓
- [ ] **`futures/dystopia-skynet-wins.md`** → Part VII: 7.1 ✓
- [ ] **`futures/utopia-health-and-happiness.md`** → Part VII: 7.2 ✓
- [ ] **`reference/faq.md`** → Appendix A.1 ✓
- [ ] **`reference/operations-roadmap.md`** → Appendix A.2 ✓
- [ ] **`references.md`** → Keep for bibliography ✓
- [ ] **`vision.md`** → Extract inspiring content to Introduction, then delete
- [ ] **`economics.md`** → Section overview file → Delete

**Legal (3 files):**
- [ ] `legal/community-governance-framework.md` → Extract to Part II: 2.4 Wishocracy
- [ ] `legal/impact-securities-reform.md` → Extract to Part IV: 4.1 VICTORY
- [ ] `legal.md` → Archive

**Partners (1 file):**
- [ ] `partners/incentives.md` → Extract to Part III: 3.3 Incentive Alignment

**Problem (7 files):**
- [ ] `problem/cost-of-disease.md` → Already in TOC Part I: 1.3, skip
- [ ] `problem/cost-of-war.md` → Already in TOC Part I: 1.2, skip
- [ ] `problem/fda-approvals-are-broken.md` → Already in TOC Part I: 1.5, skip
- [ ] `problem/nih-funding-is-broken.md` → Already in TOC Part I: 1.4, skip
- [ ] `problem/the-evolutionary-trap.md` → Already in TOC Part I: 1.1, skip
- [ ] `problem/why-the-system-is-broken.md` → Extract key points to new chapters
- [ ] `problem.md` → Archive

**Proof (3 files):**
- [ ] `proof/body-as-repairable-machine.md` → Already in TOC Part III: 3.4, skip
- [ ] `proof/historical-precedents.md` → Already in TOC Part VI: 6.2, skip
- [ ] `proof.md` → Archive

**Solution (7 files):**
- [ ] `solution/1-percent-treaty.md` → Already in TOC Part II: 2.3, skip
- [ ] `solution/dfda.md` → Already in TOC Part II: 2.2, skip
- [ ] `solution/dih.qmd` → Already in TOC Part II: 2.1, skip
- [ ] `solution/dih-core-benefits.md` → Extract to Part II: 2.1
- [ ] `solution/dih-integration-model.md` → Already in TOC Part IV: 4.3, skip
- [ ] `solution/wishocracy.md` → Already in TOC Part II: 2.4, skip
- [ ] `solution.md` → Archive

**Strategy (12 files):**
- [ ] `strategy/1-percent-treaty.md` → Check if duplicate, likely archive
- [ ] `strategy/coalition-building.md` → Extract to Part V: 5.1
- [ ] `strategy/co-opt-dont-compete.md` → Already in TOC Part V: 5.1, skip
- [ ] `strategy/dfda-implementation-via-executive-action.md` → Extract to Part V: 5.3
- [ ] `strategy/free-rider-solution.md` → Extract to Part II: 2.6
- [ ] `strategy/fundraising-strategy.md` → Already in TOC Part V: 5.4, skip
- [ ] `strategy/global-referendum.md` → Already in TOC Part V: 5.2, skip
- [ ] `strategy/hhs-dFDA-policy-recommendations.md` → Extract to Part V: 5.3
- [ ] `strategy/highest-leverage-advocacy.md` → Extract to Part V: 5.1
- [ ] `strategy/legal-compliance-framework.md` → Already in TOC Part V: 5.3, skip
- [ ] `strategy/open-ecosystem-and-bounty-model.md` → Extract to Part IV: 4.4
- [ ] `strategy.md` → Archive

**Root & Other (8 files):**
- [ ] `call-to-action.md` → Already in TOC Part VIII, skip
- [ ] `futures/dystopia-skynet-wins.md` → Already in TOC Part VII: 7.1, skip
- [ ] `futures/utopia-health-and-happiness.md` → Already in TOC Part VII: 7.2, skip
- [ ] `reference/faq.md` → Already in TOC Appendix A.1, skip
- [ ] `reference/operations-roadmap.md` → Already in TOC Appendix A.2, skip
- [ ] `references.md` → Keep for bibliography
- [ ] `vision.md` → Extract to introduction
- [ ] `economics.md`, `governance.md`, `legal.md`, `problem.md`, `proof.md`, `solution.md`, `strategy.md` → All archive

### Phase 1.6: Convert All Files to .qmd Format

**WHEN:** After Phase 1.5 cleanup is complete
**WHY:** Quarto needs .qmd for interactive features, Python integration, better rendering

#### Conversion Strategy:
1. **Batch rename** all .md files to .qmd in brain/book/
2. **Update all internal links** to point to .qmd files
3. **Update _quarto.yml** chapter references
4. **Update README.md** TOC links
5. **Test build** to ensure no broken references

**Script needed:** Create rename-to-qmd.js utility script

---

## Phase 2: Content Creation (Write First, Research Later)

### 📝 WRITING PHASE (Current Priority)

**Instructions:** Write engaging content with placeholder citations. Use these markers:
- `[TODO: source - claim about X]` for facts needing citations
- `[STAT NEEDED: specific number about Y]` for statistics
- `[CITATION: existing reference ID]` for claims we know are already in references.md
- Focus on narrative flow and dark humor
- Frame NIH as central planning failure, DIH as market solution

### Part I: The $119 Trillion Central Planning Disaster

- **1.1 Evolution Trapped Us in Violence** ✅ WRITTEN
- **1.2 The Cost of War: Humanity's Most Expensive Hobby** ✅ WRITTEN
- **1.3 The Cost of Disease: A Slow-Motion Apocalypse** ✅ WRITTEN
- **1.4 The NIH: How Soviet-Style Science Wastes $48B/Year** ⚠️ NEEDS CREATION
    - [ ] Frame as central planning failure
    - [ ] Compare to Soviet economic planning
- **1.5 The FDA: Central Planning's Body Count** ⚠️ NEEDS CREATION
    - [ ] Show deaths from delayed approvals
    - [ ] Regulatory capture examples
- **1.6 Regulatory Capture: How Pharma Bought the Refs** ⚠️ NEEDS CREATION
- **1.7 Democracy's Failure: Why Voters Can't Fix This** ⚠️ NEEDS CREATION
- **1.8 Why Nobody Fixed This Yet: A Century of Failed Reforms** ⚠️ NEEDS CREATION

### Part II: Markets > Committees (The Solution)

- **2.1 The DIH: Prediction Markets for Medical Research** 📝 NEEDS REVIEW
    - [ ] Reframe as market-based alternative
    - [ ] Emphasize Hayekian knowledge aggregation
- **2.2 The dFDA: Competition Beats Regulation** 📝 NEEDS REVIEW
- **2.3 The 1% Treaty: Redirecting Resources to What Works** 📝 NEEDS REVIEW
- **2.4 Wishocracy: Democratic Markets for Public Goods** 📝 NEEDS REVIEW
- **2.5 The Transition Plan: From Soviet Science to Free Markets** ⚠️ NEEDS CREATION
- **2.6 International Coordination: Making Treaties Stick** ⚠️ NEEDS CREATION

### Part III: Why Markets Win (The Theory) ⚠️ ALL NEW

- **3.1 Hayek Was Right: The Knowledge Problem in Medicine** ⚠️ NEEDS CREATION
- **3.2 Wisdom of Crowds: 280 Million Brains > 200 NIH Reviewers** ⚠️ NEEDS CREATION
- **3.3 Incentive Alignment: Why Everyone Wins** ⚠️ NEEDS CREATION
- **3.4 Your Body is Just a Machine (And Markets Fix Machines)** ✅ WRITTEN
- **3.5 Other Industries That Escaped Central Planning** ⚠️ NEEDS CREATION
- **3.6 Network Effects: Why This Gets Better at Scale** ⚠️ NEEDS CREATION
- **3.7 Information Theory: Why Transparency Beats Secrecy** ⚠️ NEEDS CREATION

### Part IV: The Money (Making It Real)

- **4.1 VICTORY Bonds: War Profiteering for Peace** 📝 NEEDS REVIEW
- **4.2 The ROI: $27B → $16.5T Annual Returns** 📝 NEEDS REVIEW
- **4.3 The Business Model: Insurance, Not Charity** 📝 EXISTS, NEEDS REVIEW
- **4.4 The Infrastructure: Tech Stack for Distributed Trials** ⚠️ NEEDS CREATION
- **4.5 Implementation Timeline: 36 Months to Launch** ⚠️ NEEDS CREATION

### Part V: The Heist (Strategy)

- **5.1 We're Not Fighting, We're Buying** 📝 NEEDS REVIEW
- **5.2 The Global Referendum: 280M Signatures = Unstoppable** 📝 NEEDS REVIEW
- **5.3 Legal CYA: How Not to Go to Prison** 📝 NEEDS REVIEW
- **5.4 The $2.5B Bribe Fund** ⚠️ NEEDS CREATION (fundraising-strategy.md)

### Part VI: Proof This Works

- **6.1 RECOVERY Trial: Markets Already Won (80X Efficiency)** 📝 NEEDS REVIEW
- **6.2 Historical Wins: When Decentralization Crushed Central Planning** 📝 NEEDS REVIEW
- **6.3 Pre-1962: When Doctors > Bureaucrats** 📝 NEEDS REVIEW
- **6.4 Case Studies: Cancer, Alzheimer's, Rare Diseases** ⚠️ NEEDS CREATION
- **6.5 Why Other Reforms Failed (And We Won't)** ⚠️ NEEDS CREATION

### Part VII: Pick Your Future

- **7.1 Option A: Skynet + Cancer (Status Quo)** ✅ WRITTEN
- **7.2 Option B: Markets Cure Everything** ✅ WRITTEN

### Part VIII: Join or Die (Literally)

- **8.1-8.3 Call to Action sections** 📝 NEEDS REVIEW

### Part IX: Yes, We've Heard Your Concerns ⚠️ ALL NEW

- **9.1-9.5 Objection Handling chapters** ⚠️ ALL NEED CREATION

---

## Phase 3: Research & Citation (After Writing)

### 🔬 RESEARCH PHASE (Do After All Chapters Written)

- [ ] **Systematic Source Verification:**
    - [ ] Go through each chapter and list all [TODO: source] placeholders
    - [ ] Use web_search to find real quotes and statistics
    - [ ] Build a clean references.md with verified sources only
    - [ ] Replace all placeholders with proper links to references.md
- [ ] **Fact Checking:**
    - [ ] Verify all statistics are current and accurate
    - [ ] Ensure all quotes are real and properly attributed
    - [ ] Check that all claims can be substantiated

---

## Phase 4: Visualization & Polish

### 📊 VISUALIZATION PHASE

- [ ] **Create Data Visualizations:**
    - [ ] Military spending vs medical research (Chapter 1.1)
    - [ ] Disease costs breakdown (Chapter 1.2)
    - [ ] NIH grant success rates over time (Chapter 1.3.1)
    - [ ] FDA approval timeline (Chapter 1.3.2)
    - [ ] 1% budget carve-out (Chapter 2.1)
    - [ ] VICTORY Bond returns comparison (Chapter 3.1)
    - [ ] 3.5% population map (Chapter 4.2)
    - [ ] Treaty progression timeline (Chapter 6.2)

### 🎨 POLISH PHASE

- [ ] **Content Polish:**
    - [ ] Final tone and humor pass
    - [ ] Ensure consistent voice throughout
    - [ ] Check chapter transitions and flow
- [ ] **Technical Review:**
    - [ ] Verify all internal links work
    - [ ] Test all Mermaid diagrams render correctly
    - [ ] Ensure frontmatter is consistent

---

## Phase 5: Build & Launch

- [ ] **Build All Formats:**
    - [ ] Generate and test website (`quarto render`)
    - [ ] Generate and review PDF
    - [ ] Create presentation slides
- [ ] **Launch:**
    - [ ] Deploy to GitHub Pages
    - [ ] Announce the launch
    - [ ] Prepare distribution materials

---

## 🎯 IMMEDIATE PRIORITIES (REVISED ORDER):

### Priority 1: Clean brain/book/ folder (Phase 1.5) ✅ IN PROGRESS
**ACTION:** Process all 60 orphaned files, extract value, archive originals

### Priority 2: Write Theory Foundation FIRST (Part III)
**WHY:** These chapters explain WHY markets > central planning - needed before writing other chapters
- [ ] 3.1 Hayek Was Right: The Knowledge Problem in Medicine
- [ ] 3.2 Wisdom of Crowds: 280 Million Brains > 200 NIH Reviewers
- [ ] 3.3 Incentive Alignment: Why Everyone Wins
- [ ] 3.5 Other Industries That Escaped Central Planning
- [ ] 3.6 Network Effects: Why This Gets Better at Scale
- [ ] 3.7 Information Theory: Why Transparency Beats Secrecy

### Priority 3: Reframe Existing Chapters with Market Theory
**UPDATE:** Apply theory to existing content
- [ ] Part II: All DIH/dFDA chapters - reframe with market mechanisms
- [ ] Part I: NIH/FDA chapters - frame as central planning failures

### Priority 4: Create New Problem/Strategy Chapters
**CREATE:** Fill gaps with market framing
- [ ] Part I: Regulatory Capture, Failed Reforms chapters
- [ ] Part II: Transition Plan, Treaty Enforcement
- [ ] Part V: Fundraising strategy chapter

---

## Progress Tracking

**Chapters Complete:** 5/~45 (11%)
- ✅ Part I: 1.1, 1.2, 1.3 (Evolution, War, Disease)
- ✅ Part III: 3.4 (Body as Machine)
- ✅ Part VII: 7.1, 7.2 (Dystopia, Utopia)

**Chapters Needing Creation:** ~25/45 (56%)
- ⚠️ Part I: 5 chapters (NIH, FDA, Regulatory Capture, Democracy, Failed Reforms)
- ⚠️ Part II: 2 chapters (Transition, Treaty Enforcement)
- ⚠️ Part III: 6 chapters (Theory - Hayek, Crowds, Incentives, etc.)
- ⚠️ Part IV: 2 chapters (Infrastructure, Timeline)
- ⚠️ Part V: 1 chapter (Fundraising)
- ⚠️ Part VI: 2 chapters (Case Studies, Why Others Failed)
- ⚠️ Part IX: 5 chapters (All objection handling)

**Chapters Needing Review/Reframing:** ~15/45 (33%)
- 📝 Most of Parts II, IV, V, VI need market-based reframing
