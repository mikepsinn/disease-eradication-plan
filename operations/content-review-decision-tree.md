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

## Quick Reference Checklist

For each archived file:

1. **🔍 SCAN:** Read title and first few paragraphs
2. **❌ FILTER:** Apply pre-screening delete rules  
3. **💡 ASSESS:** Does this add unique value to README.md narrative?
4. **📂 MAP:** Apply zero-ambiguity content mapping rules
5. **✅ ACT:** Delete, move, merge, or extract

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
