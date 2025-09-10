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

### The Guiding Principle: The "Platonic Ideal" Tree is Truth

Our goal is to create a clean, readable "book" based on the pre-defined target structure below. We are not simply reorganizing old files; we are writing a new book and using the archive for raw material.

**The process is TOP-DOWN, not bottom-up.** For every archived file, the primary question is:

> **"Does the essential, non-obvious, project-specific content in this file belong inside one of the pre-defined files in our ideal structure?"**

If the answer is no, the archived file is deleted. We will only add a new file to the "ideal" structure if we discover a truly critical and unforeseen gap.

### The "Book" vs. The "Internal Playbook"

To further clarify, we must distinguish between the public-facing book and our internal operational documents.

- **The Book (`/`, `economics/`, `strategy/`, `legal/`, `reference/`):** This is the public-facing content. It's the story, the argument, and the evidence. Content here should be written for an external audience.
- **The Internal Playbook (`operations/`):** This is for internal-facing strategy and standard operating procedures (SOPs). This is the "how-to" for running the organization itself. Content here is for the core team (e.g., hiring plans, fundraising SOPs, messaging frameworks). It is **not** part of the readable book.

### 1. Pre-Screening Questions

For **EVERY** archived file, ask:

**❌ IMMEDIATE DELETE if ANY of these are true:**
- Is this generic content not highly specific to our project? (e.g., "how to run a marketing campaign")
- Is this about dFDA technical implementation? (we have separate dFDA wiki)
- Is this a duplicate of content already integrated?
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
├── health-savings-sharing-model.md          (Incentive model for cures)
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

**operations/** - Team, Hiring & Processes (The Internal Playbook)
```
├── hiring-plan.md                           (Phase-based team roadmap)
├── communications-and-messaging-playbook.md (Internal framework for public narrative)
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

1. **🔍 SCAN:** Read title and first few paragraphs to understand the content.
2. **🤔 EVALUATE:** Is this content generic/obvious, or is it unique and essential to the project?
   - If generic → **DELETE**.
3. **🗺️ LOCATE:** Identify which single file in the "Platonic Ideal" structure this content belongs to.
   - If it belongs nowhere → **DELETE**.
   - If it reveals a critical gap in the ideal structure, update the structure first.
4. **✅ ACT:** **MERGE** the essential, non-obvious content into the target file, then delete the source. Or, if it's a perfect 1:1 fit, **MOVE** and **RENAME** it to match the ideal filename.
5. **✨ QA:** Perform the Quality Assurance Checklist on the *target file* that was just modified.

## Quality Assurance Checklist (Applied After Content Integration)

For every file that is **MODIFIED** (by moving or merging), perform this quick QA check:

**1. Internal Link Integrity:**
   - Scan the file for all internal relative links (e.g., `[text](./path/file.md)`).
   - **IMMEDIATELY FIX** any links that are now broken due to files being moved or renamed.
   - If a link points to a now-deleted file, either remove the link or repoint it to a relevant alternative.

**2. Content Quality Triage:**
   - **Is a critical claim missing a citation?** If yes, add `<!-- TODO: Add citation for this claim. -->`
   - **Does the writing style clash with the project's voice (direct, concise)?** If yes, add `<!-- TODO: Rewrite this section to match project writing style. -->`
   - **Is a chart, image, or visual desperately needed?** If yes, add `<!-- TODO: Add a visual (chart, image) to clarify this section. -->`
   - **Is there a section that should be expanded, removed, or clarified?** If yes, add a specific TODO comment (e.g., `<!-- TODO: Expand this section to include X. -->`).

These machine-readable TODOs create an actionable list of content debt to be addressed after the structural refactor is complete.

## Process Rules

**Golden Rules for Each File:**
1. **Always use PowerShell `Move-Item`** (not copy) - this automatically deletes the source
2. **When splitting files:** Move the original, then create additional files as needed
3. **When merging files:** Append content to target, then delete source
