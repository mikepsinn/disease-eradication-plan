# Book Completion TODO List


## Phase 1: Content Generation (Expand Placeholder Chapters)

### Priority 1: Core Economic/Legal Chapters
- [x] ~~Expand `brain/book/economics/financial-plan.qmd`~~ - RESTRUCTURED: Now high-level overview linking to detailed files
- [x] ~~Create `brain/book/economics/campaign-budget.qmd`~~ - COMPLETED: Detailed budget breakdown
- [ ] Expand `brain/book/economics/central-banks.qmd` (full chapter placeholder)
- [ ] Expand `brain/book/legal/legal-framework.qmd` (full chapter placeholder)

### Priority 2: Strategy Chapters
- [ ] Expand `brain/book/strategy/co-opting-defense-contractors.qmd` (full chapter placeholder)

### Priority 3: Reference/Appendix Chapters
- [ ] Expand `brain/book/reference/global-government-medical-research-spending.qmd` (full chapter placeholder)

### Priority 4: Rewrite for Style Consistency
- [ ] Rewrite `brain/book/economics/health-savings-sharing-model.qmd` to match formal, direct tone (remove marketing language and emojis)

## Phase 2: Fact-Checking & Sourcing

### Files with Internal Link TODOs
- [ ] `brain/book/strategy/1-percent-treaty.qmd`
  - [ ] Add link to dih-technical-architecture.md (decide if needed)
  - [ ] Link to detailed tokenomics file (decide if needed)
  - [ ] Review sections on Cost of War/Disease and ROI (decide if they belong here or should be moved/summarized)

## Phase 3: Visuals & Illustrations

### Requested Visualizations

### Figures from OUTLINE.MD to Create
(Scan OUTLINE.MD for all `[FIGURE:` markers and add them here as we process chapters)
- [ ] The $119 Trillion Waste (Problem section)
- [ ] Humanity's Budget Pie Chart (Problem section)
- [ ] Your Democracy Score: 0% (Problem section)
- [ ] How Wishocracy Works (Solution section)
- [ ] The 1% Treaty Visualization (Solution section)
- [ ] dFDA vs FDA Comparison (Solution section)
- [ ] 463:1 ROI Comparison (Money section)
- [ ] The DIH Feedback Loop (Money section)
- [ ] Death Toll Counter (Money section)
- [ ] The Two Timelines - Dystopian Path (Futures section)
- [ ] The Two Timelines - Wishonia Path (Futures section)

## Phase 4: Tone & Style Polish

### Chapters Needing Humor/Style Pass
- [ ] All completed chapters need a final pass for:
  - [ ] Consistent tone (irreverent, funny, but serious about data)
  - [ ] Punch lines land properly
  - [ ] Complex ideas simplified without dumbing down
  - [ ] Smooth transitions between sections
  - [ ] Consistent voice throughout

### Specific Style Issues Identified
- [ ] `brain/book/economics/health-savings-sharing-model.qmd` - remove marketing language and emojis

## Phase 5: Technical & Structural

### Rendering & Link Verification
- [ ] Run `quarto render` and verify no broken links
- [ ] Verify all cross-references work correctly
- [ ] Check all anchor links in references.qmd

### Final Review
- [ ] Ensure OUTLINE.MD and _quarto.yml remain in sync
- [ ] Verify all appendices are properly categorized
- [ ] Check that all chapter titles match between files and _quarto.yml

---

## Notes on Workflow

**Phase Order**: Complete each phase sequentially for best results
1. Generate all content first (so we know what needs sourcing)
2. Fact-check and source everything (so we know the facts are solid)
3. Add visuals (to enhance the verified content)
4. Polish tone (final creative pass on completed, verified content)

**Automation Opportunities**:
- AI-assisted drafting of placeholder chapters based on OUTLINE.MD
- Automated web search for sources
- Automated insertion of source links
- Batch processing of style checks

**Quality Standards**:
- Every numerical claim must have a source in references.qmd
- Every placeholder `TODO` must be resolved before moving to next phase
- Every figure mentioned in text must either exist or have a detailed creation spec
