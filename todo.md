# DIH Book - Master Build Plan

**Strategy:** Build in layers - summaries first (reusable everywhere), then detailed chapters, then polish. Use Quarto's `{{< include >}}` system to write once, render to website/presentation/book.

**Writing Guidelines:**

- `[TODO: source - claim]` for facts needing citations
- `[STAT NEEDED: description]` for missing statistics
- Vonnegut-style dark humor throughout
- Frame NIH/FDA as central planning failures, DIH/dFDA as market solutions

---

## Phase 1: Foundation Layer (Week 1-2) 🏗️

**Goal:** Write/polish the 7 part summaries that will be reused in ALL outputs (website, presentation, book)

### Part Summaries Status

| Part | File | Status | Priority |
|------|------|--------|----------|
| I. The Problem | `brain/book/problem.qmd` | ✅ DONE | - |
| II. The Theory | `brain/book/theory.qmd` | ✅ DONE | - |
| III. The Solution | `brain/book/solution.qmd` | ✅ DONE | - |
| IV. The Money | `brain/book/economics.qmd` | 📝 Review | P1 |
| V. The Implementation | `brain/book/strategy.qmd` | 📝 Review | P1 |
| VI. The Proof | `brain/book/proof.qmd` | 📝 Review | P1 |
| VII. The Futures | `brain/book/futures.qmd` | ✅ DONE | - |

### Tasks

- [x] ~~**CREATE** `brain/book/theory.qmd` (P0 - blocks presentation)~~ ✅ DONE
  - ~~Why central planning kills (Soviet famines, FDA delays)~~
  - ~~Why markets work (price signals, distributed knowledge)~~
  - ~~Public choice theory (self-interest, not idealism)~~
  - ~~Wisdom of crowds (8B > 200 bureaucrats)~~
  - ~~Keep to 300-500 words (this is a summary)~~

- [x] ~~**CREATE** `brain/book/futures.qmd` (P0 - blocks presentation)~~ ✅ DONE
  - ~~Two paths: Idiocracy (extinction) vs Wishonia (transcendence)~~
  - ~~The Three Subs vs The Three Supers~~
  - ~~One 1% decision determines which timeline~~
  - ~~Keep to 300-500 words (this is a summary)~~

- [x] **REVIEW** `brain/book/economics.qmd` (P1) ✅ DONE
  - ~~Strengthen VICTORY Bonds pitch (40% returns)~~
  - ~~Emphasize 463:1 ROI~~
  - ~~Add coalition alignment (defense contractors, pharma, insurers)~~

- [x] **REVIEW** `brain/book/strategy.qmd` (P1) ✅ DONE
  - ~~Clarify 3-step plan (mandate → funding → treaty)~~
  - ~~Emphasize 3.5% rule~~
  - ~~Technology stack overview~~

- [x] **REVIEW** `brain/book/proof.qmd` (P1) ✅ DONE
  - ~~Lead with Oxford RECOVERY (82X efficiency)~~
  - ~~Historical precedents (Switzerland, landmine treaty)~~
  - ~~Body as machine analogy~~

**Deliverable:** 7 polished summaries that work as standalone content

---

## Phase 2: Quick Launch (Week 2-3) 🚀

**Goal:** Ship website + presentation using the summaries from Phase 1

### Website Setup

- [x] **Polish** `index.qmd` as landing page
  - ~~Use existing content (already strong)~~
  - ~~Add links to part summaries~~
  - ~~Ensure all links work~~

- [x] **Update** `_quarto.yml` for multiple outputs
  - ~~Book format (existing)~~
  - ~~Website format (existing)~~
  - ~~Presentation format (add revealjs/pptx)~~

### Presentation Build

- [x] **Finalize** `presentation.qmd` (already drafted)
  - ~~Uses `{{< include >}}` for part summaries~~
  - ~~Conditional content: bullets for slides, prose for PowerPoint~~
  - ~~Test both revealjs and pptx outputs~~

### Build & Deploy

- [ ] **Test builds**
  ```bash
  quarto render index.qmd --to html          # Website
  quarto render presentation.qmd --to revealjs  # Web slides
  quarto render presentation.qmd --to pptx      # PowerPoint
  ```

- [ ] **Deploy to GitHub Pages**
  ```bash
  quarto publish gh-pages
  ```

**Deliverable:** Live website at WarOnDisease.org + downloadable presentation

---

## Phase 3: Theory Foundation (Week 3-6) 📚

**Goal:** Write the 4 theory chapters that explain WHY markets > central planning. These will be referenced throughout other chapters.

**Why First?** These provide the intellectual framework for reframing all other content.

| Chapter | File | Topics | Words |
|---------|------|--------|-------|
| 4. Why Central Planning Kills | `brain/book/theory/central-planning-failure.qmd` | 1962 FDA centralization disaster, Soviet famines, knowledge problem, NIH inefficiency | 2,500 |
| 5. The War on Disease | `brain/book/theory/war-on-disease.qmd` | First "war" designed to win, aligned incentives, spillover effects, meta-victory | 2,000 |
| 6. Public Choice Theory | `brain/book/theory/public-choice.qmd` | Politicians maximize power, bureaucrats maximize budgets, lobbyist ROI, incentive engineering | 2,000 |
| 7. Wisdom of Crowds | `brain/book/theory/wisdom-of-crowds.qmd` | Surowiecki's ox, prediction markets, network effects, superintelligence we already have | 2,000 |

### Chapter Templates

Each chapter should follow this structure:
```markdown
---
title: "Chapter X: [Title]"
---

## The Problem (Historical Evidence)
[Soviet agriculture / FDA delays / NIH waste - pick one parallel]

## Why It Failed (Theory)
[Hayek's knowledge problem / Public choice theory / etc.]

## How Markets Solve This
[Price signals / Competition / Wisdom of crowds]

## Applied to Medical Research
[Specific examples from dFDA / DIH]

## The Proof
[Oxford RECOVERY / Pre-1962 medicine / Other examples]
```

**Deliverable:** 4 theory chapters (~8,500 words) that can be referenced in all other content

---

## Phase 4: Fill Critical Gaps (Week 6-10) 🔌

**Goal:** Complete the missing chapters needed for coherent narrative flow

### Problem Section

- [ ] **CREATE** `brain/book/problem/democracy-failure.qmd` (2,500 words)
  - Princeton study (0% public influence)
  - Rational ignorance (1 in 60M vote probability)
  - Representation illusion (750K constituents per rep)
  - Budget black box (omnibus bills)
  - Regulatory capture
  - Direct democracy failures (California)

### Economics Section

- [ ] **CREATE** `brain/book/economics/coalition.qmd` (2,500 words)
  - Defense contractors (40% returns > 8% margins)
  - Insurance companies (healthy people = profit)
  - Big Pharma (DIH = guaranteed customers)
  - Politicians (our money > their money)
  - Billionaires (reputation + returns)

- [ ] **CREATE** `brain/book/economics/legal-framework.qmd` (2,000 words)
  - Multi-jurisdiction strategy
  - Securities law navigation (VICTORY bonds as debt)
  - Election law compliance
  - Treaty framework
  - Legislation package (already drafted)

### Strategy Section

- [ ] **CREATE** `brain/book/strategy/technology-stack.qmd` (2,000 words)
  - Platform architecture (distributed ledger, smart contracts)
  - AI layer (personal health agents, treatment matching)
  - Security requirements
  - Privacy paradox solved (public science, private patients)

### Futures Section

- [ ] **CREATE** `brain/book/futures/comparison.qmd` (2,000 words)
  - Side-by-side comparison table (2030, 2035, 2040, 2045, 2050)
  - The Three Subs vs The Three Supers
  - Daily life in each timeline
  - Math that should have warned us

**Deliverable:** 5 new chapters (~11,000 words) completing the narrative skeleton

---

## Phase 5: Reframe & Enhance (Week 10-14) 🔄

**Goal:** Apply market theory framework to all existing chapters

### Part III: Solution (Apply Market Framing)

- [ ] **REFRAME** `brain/book/solution/wishocracy.qmd`
  - Add: How APPA prevents central planning
  - Add: Market discovery vs committee decisions
  - Add: Why AI twins scale better than representatives

- [ ] **REFRAME** `brain/book/solution/1-percent-treaty.qmd`
  - Add: Game theory (why countries cooperate)
  - Add: Verification mechanism (blockchain, satellites)
  - Add: Ratchet effect (1% → 2% → 5%)

- [ ] **REFRAME** `brain/book/solution/dih.qmd`
  - Add: Why subsidizing patients > funding researchers
  - Add: Capture-proof design (no committee to bribe)
  - Add: 7-step problem-solving process

- [ ] **REFRAME** `brain/book/solution/dfda.qmd`
  - Add: Amazon comparison (marketplace, not gatekeeper)
  - Add: Competition drives efficiency (82X proof)
  - Add: Network effects (each trial makes next cheaper)

### Part IV: Economics (Strengthen Arguments)

- [ ] **ENHANCE** `brain/book/economics/victory-bonds.qmd`
  - Add: Comparison to Medallion Fund
  - Add: Why defense contractors should diversify
  - Add: Use of funds transparency

- [ ] **ENHANCE** `brain/book/economics/economic-case.qmd`
  - Add: Daily holocaust of inaction (2,301 QALYs/day)
  - Add: Dominant intervention (negative ICER)
  - Add: $16.5T endgame calculation

### Part V: Implementation (Emphasize Decentralization)

- [ ] **ENHANCE** `brain/book/strategy/global-referendum.qmd`
  - Add: Viral growth strategy (3.5 multiplier)
  - Add: Network effects
  - Add: Platform details (Wishocracy app)

- [ ] **ENHANCE** `brain/book/strategy/legal-compliance-framework.qmd`
  - Add: Specific legislation package
  - Add: How to stay out of prison
  - Add: International coordination

### Part VI: Proof (Connect to Market Success)

- [ ] **ENHANCE** `brain/book/proof/historical-precedents.qmd`
  - Add: Switzerland (200-year peace dividend)
  - Add: War bonds (capitalism defeated fascism)
  - Add: 3.5% rule (we have advantages they didn't)

- [ ] **ENHANCE** `brain/book/reference/recovery-trial.qmd`
  - Add: Cost breakdown ($500 vs $41,000)
  - Add: Timeline comparison
  - Add: Why it proves decentralization works

### Part VIII: Call to Action (Final Polish)

- [ ] **POLISH** `brain/book/call-to-action.qmd`
  - Ensure clear 3-action structure
  - Personal benefits list
  - Every objection demolished

**Deliverable:** 15+ chapters enhanced with consistent market theory framing

---

## Phase 6: Research & Citations (Week 14-15) 🔬

**Goal:** Replace all placeholder citations with real sources

### Systematic Source Hunt

- [ ] **Scan all files** for citation placeholders
  ```bash
  rg "\[TODO: source" brain/book/ --type md
  rg "\[STAT NEEDED:" brain/book/ --type md
  ```

- [ ] **Create master citation list**
  - Extract all claims needing sources
  - Prioritize by importance (critical stats first)

- [ ] **Research & verify**
  - Use WebSearch tool for statistics
  - Verify all numbers are current
  - Find original sources (not secondary)

- [ ] **Build** `brain/reference/references.qmd`
  - One alphabetized list
  - Format: anchor ID, brief title, quote, source link
  - No duplicates

- [ ] **Replace placeholders** with proper links
  - Format: `[claim](./references.qmd#anchor-id)`
  - Verify all links work

**Deliverable:** Fully cited book with zero placeholders

---

## Phase 7: Visualization (Week 15-16) 📊

**Goal:** Add Python-generated charts using Quarto's computation features

### Priority Charts (Create as `.qmd` files in `brain/figures/`)

- [ ] **Military spending vs medical research** (Chapter 1)
  - Bar chart comparing $2.7T to $68B
  - Annotations showing fighter jet = rare disease budget

- [ ] **Disease costs breakdown** (Chapter 1)
  - Pie chart: direct healthcare, lost productivity, death costs
  - $109.1T total with components

- [ ] **FDA approval timeline** (Chapter 4)
  - Timeline visualization: pre-1962 vs post-1962
  - 2-3 years → 17 years, $74M → $2.6B

- [ ] **1% budget carve-out** (Chapter 9)
  - Visual showing 1% = $27B from $2.7T
  - "Still have 99% for killing"

- [ ] **VICTORY Bond returns comparison** (Chapter 11)
  - Bar chart: S&P (10%), VC (25%), Medallion (39%), VICTORY (40%)
  - Scaling potential as treaty expands

- [ ] **3.5% population map** (Chapter 16)
  - World map showing 280M = 3.5% of 8B
  - Historical examples (civil rights, suffrage)

- [ ] **Treaty progression timeline** (Chapter 9)
  - Gantt chart: Year 1 (1%), Year 2 (2%), Year 5 (5%)
  - Corresponding budget growth

- [ ] **Oxford RECOVERY cost breakdown** (Chapter 19)
  - Detailed comparison: $500 vs $41,000 per patient
  - Where the 82X savings come from

### Chart Style Standards

All charts must follow the style guide:
```python
# Use centralized theme (to be created)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'figure.dpi': 150,
})

# Watermark every chart
fig.text(0.98, 0.02, 'WarOnDisease.org',
         fontsize=8, color='gray',
         ha='right', va='bottom', alpha=0.7)
```

**Deliverable:** 8 professional charts embedded throughout book

---

## Phase 8: Polish & Launch (Week 16) 🎨

**Goal:** Final quality pass and full deployment

### Content Polish

- [ ] **Voice consistency pass**
  - Ensure Vonnegut-style dark humor throughout
  - Remove any corporate buzzwords
  - Check for euphemisms (replace with direct language)

- [ ] **Flow & transitions**
  - Ensure chapters connect logically
  - Add forward/backward references where helpful
  - Smooth narrative arc from problem → solution → action

### Technical Review

- [ ] **Verify all internal links**
  ```bash
  npm run lint:links
  ```

- [ ] **Test all Mermaid diagrams**
  - Render each one in preview
  - Ensure no syntax errors

- [ ] **Validate frontmatter**
  ```bash
  npm run validate:frontmatter --fix
  ```

- [ ] **Markdown linting**
  ```bash
  npm run lint:md:fix
  ```

### Build All Formats

- [ ] **HTML (website)**
  ```bash
  quarto render --to html
  ```

- [ ] **PDF (book)**
  ```bash
  quarto render --to pdf
  ```

- [ ] **EPUB (ebook)**
  ```bash
  quarto render --to epub
  ```

- [ ] **RevealJS (web presentation)**
  ```bash
  quarto render presentation.qmd --to revealjs
  ```

- [ ] **PowerPoint**
  ```bash
  quarto render presentation.qmd --to pptx
  ```

### Deployment

- [ ] **Deploy to GitHub Pages**
  ```bash
  quarto publish gh-pages
  ```

- [ ] **Upload presentation** to Google Drive / Dropbox
  - Share PowerPoint for offline use
  - Share RevealJS link for online viewing

- [ ] **Generate PDF/EPUB** for distribution
  - Host on website
  - Submit to ebook platforms (optional)

### Announcement

- [ ] **Launch post** on social media
- [ ] **Email list announcement**
- [ ] **Submit to relevant communities** (Reddit, HN, etc.)

**Deliverable:** Fully polished book in 5 formats (HTML, PDF, EPUB, RevealJS, PPTX)

---

## Progress Tracker

### Overall Status

| Phase | Status | Completion | Deliverable |
|-------|--------|------------|-------------|
| Phase 1: Foundation | ✅ Complete | 7/7 summaries DONE | 7 part summaries |
| Phase 2: Quick Launch | ✅ Complete | 95% (deploy when ready) | Website + Presentation |
| Phase 3: Theory | 🟢 Ready to Start | 0/4 chapters | Theory foundation |
| Phase 4: Fill Gaps | ⏸️ Waiting | 0/5 chapters | Complete skeleton |
| Phase 5: Reframe | ⏸️ Waiting | 0/15 chapters | Enhanced content |
| Phase 6: Research | ⏸️ Waiting | 0% | Full citations |
| Phase 7: Visualization | ⏸️ Waiting | 0/8 charts | Professional charts |
| Phase 8: Launch | ⏸️ Waiting | 0% | Published book |

### Files Status

**Complete:** 9/33 chapters (27%)

- ✅ Part I: Ch 1, 2 (Evolution, War+Disease)
- ✅ Part VI: Ch 20 (Body as Machine)
- ✅ Part VII: Ch 21, 22 (Dystopia, Utopia)
- ✅ 4 part summaries (problem, solution, theory, futures)

**To Create:** 9/33 chapters (27%)

- ⚠️ 4 theory chapters - **PHASE 3**
- ⚠️ 5 gap chapters - **PHASE 4**

**To Review/Enhance:** 15/33 chapters (46%)

- 📝 15 existing chapters need market framing - **PHASE 5**

---

## Key Efficiency Principles

1. **Write Once, Render Everywhere**

   - Part summaries used in website, presentation, and book
   - Detailed chapters included via `{{< include >}}`
   - Conditional content for different formats

2. **Build in Layers**

   - Summaries first (reusable foundation)
   - Theory second (framework for everything else)
   - Details last (when framework is solid)

3. **Ship Incrementally**

   - Phase 2: Website + presentation (2-3 weeks)
   - Phase 8: Full book (16 weeks)
   - Feedback improves final product

4. **Leverage Quarto Features**

   - Conditional content: `{.content-visible when-format="revealjs"}`
   - Includes: `{{< include path.qmd >}}`
   - Python charts: Executed during render
   - Multiple outputs: One command → HTML + PDF + EPUB

5. **Parallel Work Possible**

   - Theory chapters (Phase 3) can be written in parallel
   - Gap chapters (Phase 4) independent
   - Research (Phase 6) can start early

---

## Commands Reference

### Preview (Live Reload)
```bash
quarto preview                      # Preview book
quarto preview presentation.qmd     # Preview presentation
quarto preview index.qmd           # Preview website
```

### Build Specific Formats
```bash
quarto render index.qmd --to html
quarto render presentation.qmd --to revealjs
quarto render presentation.qmd --to pptx
quarto render --to pdf
quarto render --to epub
```

### Quality Checks
```bash
npm run validate:frontmatter --fix  # Fix YAML headers
npm run lint:md:fix                 # Fix markdown issues
npm run generate:index              # Update file index
```

### Deploy
```bash
quarto publish gh-pages             # Deploy to GitHub Pages
```
