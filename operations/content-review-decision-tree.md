# Content Review Decision Tree

*Systematic process for reviewing archived files and deciding their fate*

## Decision Tree Flowchart

```
📁 Archived File
    ↓
🤔 Is this about dFDA implementation details?
    ↓ YES → 🗑️ DELETE (we have separate dFDA wiki)
    ↓ NO
    ↓
🤔 Does this directly support README.md narrative?
    ↓ YES → Continue to Content Mapping
    ↓ NO  
    ↓
🤔 Is this duplicated elsewhere or obsolete?
    ↓ YES → 🗑️ DELETE
    ↓ NO
    ↓
🤔 Is this essential for execution?
    ↓ YES → Continue to Content Mapping
    ↓ NO → 🗑️ DELETE

Content Mapping:
💰 Money/ROI/Financial? → economics/
🎯 Execution/Political? → strategy/
⚖️ Legal/Compliance? → legal/
👥 Team/HR/Process? → operations/
📊 Data/Studies/Citations? → reference/
```

## Step-by-Step Process

### The "Book" Mental Model: Chapters, Sections, and The Appendix

To eliminate ambiguity, use this powerful heuristic for every file:

> **Ask: "Is this part of the main story, or is it a footnote/tangent?"**

- **Chapters (Root Files like `economics.md`):** These are the main chapters of the book. They provide the high-level narrative and summarize the core arguments. They should be readable from start to finish.

- **Sections (Files in Subdirectories like `economics/`):** These are the sections and subsections that form the substance of a chapter. `economics/investment-thesis.md` is effectively "Section 3.1" of the "Economics" chapter. This is our core, first-party intellectual property.

- **The Appendix (`reference/` Directory):** This is the **one true appendix** of the book. It is for material that is supplementary to the main argument, not part of it. It's the home for external evidence, raw data, third-party studies, or deep-dive content that would interrupt the narrative flow of a chapter.

**Example Application:**
- Our analysis of NIH inefficiency (`nih-grant-efficiency-analysis.md`) is a core part of our economic argument. It belongs in the `economics/` directory as a *section* of the Economics chapter.
- A raw data file *from* the NIH or a third-party study we cite would belong in the Appendix (`reference/`).

### 1. Pre-Screening Questions

For **EVERY** archived file, ask:

**❌ IMMEDIATE DELETE if ANY of these are true:**
- Is this about dFDA technical implementation? (we have separate dFDA wiki)
- Is this a duplicate of content already in README.md?
- Is this outdated planning documentation?
- Is this a test file or template?
- Does this contradict our simplified approach?

### 2. Value Assessment

**✅ KEEP AND INTEGRATE if:**
- Contains unique data/analysis supporting README.md arguments
- Essential financial models or ROI calculations  
- Critical execution strategies not covered elsewhere
- Important legal compliance frameworks
- Key operational processes

### 3. Content Mapping (Zero Ambiguity Rules)

If keeping content, apply these **exact** rules:

| Content Type | Destination | Examples |
|--------------|-------------|----------|
| Financial models, ROI, investment thesis | `economics/` | victory-bonds-tokenomics, peace-dividend-value-capture |
| Execution plans, political strategy, how-to | `strategy/` | 1-percent-treaty, referral-rewards-system |
| Legal compliance, governance, regulations | `legal/` | multi-entity-strategy, right-to-trial-act |
| Team structure, hiring, processes | `operations/` | hiring-plan, crypto-intake-sop |
| Data, studies, citations, reference material | `reference/` | costs-of-war, recovery-trial |

### 4. Integration Methods

**A. Standalone File:** Move to appropriate directory as-is
**B. Merge Content:** Combine with existing placeholder or other files
**C. Extract Key Points:** Pull essential info into root-level narrative files

## Complete Target Structure: "The 1% Treaty: How to End War and Disease"

### Root Level: The Chapters
Following README.md's narrative flow for maximum readability:

```
/
├── README.md                           ✅ (Perfect intro - "War is incredibly stupid...")
├── problem.md                          📖 Chapter 1: The Grotesque Misallocation  
├── solution.md                         📖 Chapter 2: Legal Bribery for Peace
├── economics.md                        📖 Chapter 3: The Financial Engine  
├── strategy.md                         📖 Chapter 4: How Everyone Wins (The Bribery Strategy)
├── proof.md                           📖 Chapter 5: Why This Actually Works (Precedents & Evidence)
├── legal.md                           📖 Chapter 6: Legal Compliance & Structure
├── operations.md                       📖 Chapter 7: Building the Organization
├── FAQ.md                             📖 Chapter 8: Objections & Responses
├── roadmap.md                         📖 Chapter 9: Timeline to Global Impact
└── call-to-action.md                  📖 Chapter 10: How You Can Join
```

### Supporting Directories: The Detailed Appendices

**economics/** - Financial Models & Analysis
```
├── investment-thesis.md                     (Core investment case - unique concept)
├── peace-dividend-value-capture.md          (Economic engine explanation)  
├── dfda-cost-benefit-analysis.md            (80X efficiency ROI analysis)
├── investor-risk-analysis.md                (Risk mitigation vs. traditional VC)
├── operational-budget-model.md              (Bottom-up budget justification)
├── intervention-comparison-table.md         (Health intervention value analysis)
├── quantitative-value-medical-treatment.md  (QALY calculations)
├── dih-treasury-cash-flow-model.md          (10-year financial projections)
└── fundraising/                             (Epic folder for fundraising details)
    ├── fundraising-plan.md                  (The overview file)
    ├── fundraising-budget-breakdown.md      (The $2.5B line-item budget)
    ├── fundraising-strategy.md              (Market-driven mechanics & assurance contracts)
    ├── fundraising-pre-seed-terms.md        (SAFT structure)
    └── fundraising-whale-outreach.md        (High-net-worth targeting strategy)
```

**strategy/** - Execution Plans & Political Strategy  
```
├── 1-percent-treaty.md                      (Full treaty text & explanation)
├── dih-model.md                             (DIH structure & operation)
├── co-opting-defense-contractors.md         (KEY: How we flip the MIC)
├── coalition-building.md                    (Partner recruitment & management)
├── free-rider-solution.md                   (Preventing treaty defection)
├── executive-action-implementation.md       (DOGE model approach)
├── war-on-disease-strategy.md               (Comprehensive strategy overview)
├── historical-precedents-and-rationale.md   (Why this playbook wins)
├── messaging-value-estimation.md            (Sentiment analysis framework)
├── highest-leverage-advocacy.md             (Why every org should focus here)
└── global-referendum/                       (Epic folder for referendum details)
    ├── global-referendum-plan.md            (The overview file)
    ├── global-referendum-implementation.md  (3.5% mobilization mechanics)
    ├── global-referendum-incentives.md      (Referral rewards & VOTE points)
    ├── global-referendum-verification.md    (280M person verification & fraud prevention)
    └── global-referendum-legal-compliance.md (Multi-jurisdiction compliance)
```

**legal/** - Compliance & Governance
```
├── multi-entity-strategy.md                 (501c3/501c4/for-profit structure)
├── right-to-trial-act.md                   (FDA modernization legislation)
├── impact-securities-reform.md             (Model law for compliant financing)
├── dex-listing-policy.md                   (Token listing governance)
└── community-governance-framework.md        (DAO governance principles)
```

**operations/** - Team, Hiring & Processes
```
├── hiring-plan.md                           (Phase-based team roadmap)
├── crypto-intake-sop.md                     (Investment/donation procedures)
├── nonprofit-partnership-playbook.md        (Coalition building strategy)
├── process-index.md                         (Operational process hub)
├── pre-seed-strategy.md                     (Foundation phase execution)
├── dih-treasury-management-and-security.md  (CRITICAL: Controls for the $27B+ treasury)
└── team-incentives.md                       (Dynamic EV compensation model)
```

**reference/** - Supporting Data & Evidence
```
├── costs-of-war.md                          (Quantified direct/indirect costs)
├── recovery-trial.md                        (80X efficiency proof case)
├── global-government-medical-research-spending.md (Baseline funding analysis)
├── organizational-precedents.md             (ICBL, Global Fund, MakerDAO models)
├── historical-evidence-supporting-*.md      (Multiple evidence files)
├── existing-dct-platforms.md               (Competitive landscape)
├── impact-of-innovative-medicines-on-life-expectancy.md
├── nih-grant-efficiency-analysis.md        (Current system inefficiencies)
└── value-of-new-treatment.md               (Economic value of medical progress)
```

## Archived File Mapping Guide

**Immediate Destinations for High-Value Content:**

| Archive Source | Target Destination | Reason |
|---------------|-------------------|---------|
| `archive/economic-models/*.md` | `economics/*.md` | Direct financial model migration |
| `archive/strategy-old/1-percent-treaty/*.md` | `strategy/*.md` | Core strategy content |
| `archive/strategy-old/co-opting-defense-contractors.md` | `strategy/co-opting-defense-contractors.md` | **CRITICAL** - core strategy |
| `archive/careers/hiring-plan.md` | `operations/hiring-plan.md` | Key operational content |
| `archive/legal-old/multi-entity-strategy.md` | `legal/multi-entity-strategy.md` | Essential legal framework |
| `archive/reference-old/*.md` | `reference/*.md` | Supporting evidence |
| `archive/regulatory/*.md` | `legal/*.md` | Compliance frameworks |

**Delete Categories:**
- Most `archive/operations-old/issues/*.md` (planning artifacts)
- `archive/dfda.md` and related (separate dFDA wiki)
- `archive/features/*.md` (implementation details)
- Duplicate or obsolete planning documents

## Quick Reference Checklist

For each archived file:

1. **🔍 SCAN:** Read title and first few paragraphs
2. **❌ FILTER:** Apply pre-screening delete rules  
3. **💡 ASSESS:** Does this map to a specific target file above?
4. **📂 MAP:** Move to exact target location or integrate into chapter
5. **✅ ACT:** Move, merge, extract, or delete
6. **✨ QA:** Perform the Quality Assurance Checklist below

## Quality Assurance Checklist (Applied After Mapping & Before Moving)

For every file that is **KEPT** (moved or merged), perform this quick QA check:

**1. Link Verification:**
   - Scan for all internal relative links (e.g., `[text](./path/file.md)`).
   - Update any links pointing to files that have been moved or renamed.
   - If a link points to a now-deleted file, either remove the link or repoint it to a relevant alternative.

**2. Content Quality Triage:**
   - **Is a critical claim missing a citation?** If yes, add `<!-- TODO: Add citation for this claim. -->`
   - **Does the writing style clash with the project's voice (direct, concise)?** If yes, add `<!-- TODO: Rewrite this section to match project writing style. -->`
   - **Is a chart, image, or visual desperately needed?** If yes, add `<!-- TODO: Add a visual (chart, image) to clarify this section. -->`
   - **Is there a section that should be expanded, removed, or clarified?** If yes, add a specific TODO comment (e.g., `<!-- TODO: Expand this section to include X. -->`).

These machine-readable TODOs create an actionable list of content debt to be addressed after the structural refactor is complete.

## Priority Order for Review

**High Priority (Review First):**
1. `archive/economic-models/` → Most directly supports README.md
2. `archive/strategy-old/1-percent-treaty/` → Core solution content
3. `archive/legal-old/` → Essential compliance frameworks
4. `archive/careers/hiring-plan.md` → Key operational content

**Medium Priority:**
5. `archive/reference-old/` → Supporting data and studies
6. `archive/regulatory/` → May have legal compliance content

**Low Priority (Review Last):**
7. `archive/operations-old/issues/` → Likely delete most of these
8. `archive/features/` → Likely dFDA implementation details
9. Individual files like `archive/act.md`, `archive/dfda.md`

## Process Rules

**Golden Rules for Each File:**
1. **Always use PowerShell `Move-Item`** (not copy) - this automatically deletes the source
2. **When splitting files:** Move the original, then create additional files as needed
3. **When merging files:** Append content to target, then delete source
4. **Document each decision** in the tracking log below

## Progress Tracking

**Completed Directories:**
- `archive/economic-models/`
- `archive/strategy-old/`
- `archive/legal-old/`
- `archive/careers/` (Discovered to be empty; already processed)

**Current Directory:** `archive/reference-old/`

**Files Processed:**
- 🗑️ `all_of_us_participant_portal_adaptive_platform_for_personalized_engagement.xlsx` → **DELETED** (Per user)
- 🗑️ `canonicals.md` → **DELETED** (Obsolete navigational index)
- ✅ `costs-of-war.md` → **MOVED** to `reference/costs-of-war.md` (Quality: High, No TODOs needed)
- ✅ `data-storage-costs.md` → **MOVED** to `reference/data-storage-costs.md` (Quality: Good, No TODOs needed)
- ✅ `existing-dct-platforms.md` → **MOVED** to `reference/existing-dct-platforms.md` (Quality: High, No TODOs needed)

**Files to Process:**
- `global-government-medical-research-spending.md`
- `historical-evidence-supporting-decentralized-efficacy-trials.md`
- `historical-evidence-supporting-real-wold-efficacy-trials.md`
- `history-of-medical-regulation-and-clinical-research.md`
- `impact-of-innovative-medicines-on-life-expectancy.md`
- `nih-recover-initiative.md`
- `organizational-precedents.md`
- `otc-drugs.md`
- `pragmatic-trials.md`
- `recovery-trial.md`
- `references.md`
- `Research-and-Development-in-the-Pharmaceutical-Industry.md`
- `value-of-new-treatment.md`

**Summary:** 5/18 files processed (28% complete)

**Next Directory:** `archive/regulatory/`

**Goal:** Process all archived content systematically with zero ambiguity about decisions.
