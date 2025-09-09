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
├── victory-bonds-investment-thesis.md       (Core investment case)
├── peace-dividend-value-capture.md          (Economic engine explanation)  
├── fundraising-and-budget-plan.md           (The $2.5B activation energy)
├── dih-treasury-cash-flow-model.md          (10-year financial projections)
├── dfda-cost-benefit-analysis.md            (80X efficiency ROI analysis)
├── investor-risk-analysis.md                (Risk mitigation vs. traditional VC)
├── pre-seed-terms.md                        (SAFT structure)
├── operational-budget-and-financial-model.md (Bottom-up budget justification)
├── intervention-comparison-table.md         (Health intervention value analysis)
└── quantitative-value-medical-treatment.md  (QALY calculations)
```

**strategy/** - Execution Plans & Political Strategy  
```
├── 1-percent-treaty.md                      (Full treaty text & explanation)
├── decentralized-institutes-of-health.md    (DIH structure & operation)
├── co-opting-defense-contractors.md         (KEY: How we flip the MIC)
├── referral-rewards-system.md               (Viral growth mechanics)
├── legal-compliance-framework.md            (Multi-jurisdiction compliance)
├── verification-and-fraud-prevention.md     (280M person verification)
├── free-rider-solution.md                   (Preventing treaty defection)
├── whale-billionaire-outreach-strategy.md   (High-net-worth targeting)
├── global-referendum-implementation.md      (3.5% mobilization mechanics)
├── executive-action-implementation.md       (DOGE model approach)
├── war-on-disease-strategy.md               (Comprehensive strategy overview)
├── historical-precedents-and-rationale.md   (Why this playbook wins)
├── messaging-value-estimation.md            (Sentiment analysis framework)
└── highest-leverage-advocacy.md             (Why every org should focus here)
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

## Outcome Tracking

Keep a simple log:
- **📁 Files Reviewed:** X/Y
- **🗑️ Deleted:** Count  
- **📂 Moved:** Count
- **🔄 Merged:** Count
- **⏭️ Deferred:** Count

**Goal:** Process all archived content systematically with zero ambiguity about decisions.
