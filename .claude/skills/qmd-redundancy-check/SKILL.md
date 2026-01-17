---
name: qmd-redundancy-check
description: Finds and quantifies redundant content in QMD files - repeated equations, duplicate sections, similar paragraphs, and structural redundancy.
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# QMD Redundancy Check

## Key Insight for _latex Variables

All `{{< var X >}}` variables are hyperlinks to their derivations. When removing `{{< var X_latex >}}`, just delete it - no need to add links.

---

## Phase 1: Generate and Read the Report

```bash
.venv/Scripts/python.exe scripts/redundancy-check.py <file.qmd> -v -o _analysis/redundancy-report.md
```

**The report contains:**

1. **Document Outline** - Full heading hierarchy with line numbers
2. **Summary Section Flags** - Headings containing "Summary", "Conclusion", "Key Findings" (check for overlap)
3. **Similar Heading Pairs** - Headings with >40% word overlap (may cover same content)
4. **Duplicate _latex Variables** - Sorted by redundancy cost (occurrences × lines)
5. **Duplicate Sentences** - Exact matches appearing multiple times
6. **Similar Paragraphs** - Pairs with >50% word overlap
7. **Repeated Phrases** - 5+ word n-grams appearing 3+ times

Read the report, then read the target QMD file to understand context.

---

## Phase 2: Systematic Issue Resolution

Process issues in priority order. For each issue:

### Step 1: Investigate
Read 30-50 lines around each occurrence. Understand the context.

### Step 2: Analyze
Determine which is PRIMARY (authoritative) vs SECONDARY (recap/reference):
- Primary: First introduction, methodology section, main explanation
- Secondary: Summary, conclusion, "as mentioned earlier", recap sections

### Step 3: Decide
Present findings and recommendation to user (if not obvious):

```
Issue: [Type] - [Description]
Locations: L123 (Section A), L456 (Section B)
Analysis: [Why one is primary, one is secondary]
Recommendation: [Keep X, delete/merge Y]
```

### Step 4: Execute
Make the edit. For deletions, ensure no information is lost.

### Step 5: Continue
Move to next issue. Track progress.

---

## Issue Type: Duplicate _latex Variables

**Why it matters**: Each equation expands to 20-50+ lines. 5 occurrences = 80-200 unnecessary lines.

**Rule: Keep 1-2 instances per equation, depending on document structure.**

Since all `{{< var X >}}` variables are hyperlinks to their derivations, readers can click any value to see the full equation. However, long technical documents may have intentional duplication for different audiences.

**Acceptable duplication (multi-audience design):**
- Executive summary callout + formal verification section
- Body explanation + economist verification section
- These serve different reading paths and should be kept

**What to REMOVE:**
- 3+ occurrences of the same equation (always excessive)
- Equations 6 lines apart in the same section
- Equations in narrative sections where inline value is stated
- Equations immediately after tables showing the same values

**What to KEEP:**
- At least 1 instance of each equation
- Intentional pairs serving different audiences (e.g., summary + derivation)

---

## Issue Type: Similar Headings

**From report**: Pairs with >40% word overlap flagged.

**Investigation:**
1. Read full content under both headings
2. Compare: Same points? One subset of other? Different aspects?

**Actions:**
| Finding | Action |
|---------|--------|
| Same content, different words | Merge into one section, delete other |
| One is recap of other | Delete recap, or convert to "See [Section X]" |
| Different content, confusing names | Rename one to clarify distinction |
| Intentionally different (e.g., methodology vs limitations) | Keep both, rename for clarity |

### Improving Heading Names

When sections cover related but distinct topics, **rename headings to be more descriptive** of their actual content. This prevents false positives in future scans and helps readers navigate.

**Heading naming principles:**
- Include the section's PURPOSE, not just its topic
- Add context words: "Assumptions", "Uncertainty", "Mechanism", "Comparison", "Derivation"
- Make parent-child relationships clear

**Examples of heading improvements:**

| Original (ambiguous) | Improved (descriptive) | Why |
|---------------------|------------------------|-----|
| "[Topic] Assumptions" (in Limitations) | "[Topic] Uncertainty" | Clarifies this discusses limitations, not the assumption itself |
| "[Topic]" (second occurrence) | "[Topic] Mechanism" | Distinguishes from summary section |
| "[Topic] Feasibility" (in Limitations) | "[Topic] Feasibility Constraints" | Shows this is about constraints, not general discussion |
| "Comparative [Topic]" | "Comparative [Topic] vs Alternatives" | Clarifies it's a comparison, not a feature description |
| "[Metric] Calculation" (in verification) | "[Metric] Derivation" | Shows it's a derivation, not just a result |

**Anti-patterns to fix:**
- Same heading appearing in Methodology AND Limitations sections
- Generic headings like "Results", "Analysis", "Discussion" without context
- Headings that match parent section name (e.g., "Assumptions" under "Key Analytical Assumptions")

---

## Issue Type: Summary/Recap Sections

**From report**: Sections flagged with keywords: "Summary", "Key Findings", "Conclusion", "Results", "Overview"

**Investigation:**
Compare content across all flagged sections. Do they repeat same bullets/points?

**Common pattern**: Document has "Key Findings" at top, "Summary of Results" in middle, and "Conclusion" at end - all saying the same thing.

**Actions:**
| Finding | Action |
|---------|--------|
| All repeat same points | Keep one (usually Conclusion), delete others |
| Each serves distinct purpose | Keep all, ensure they're differentiated |
| Overlap but different emphasis | Consolidate overlapping parts, keep unique parts |

---

## Issue Type: Duplicate Sentences

**From report**: Exact sentences appearing at multiple line numbers.

**Investigation:**
Read surrounding paragraphs. Which occurrence is the "home" for this sentence?

**Actions:**
- Delete the repeat, keep in primary context
- If both contexts need it, rephrase one

---

## Issue Type: Similar Paragraphs

**From report**: Paragraph pairs with >50% word overlap.

**Investigation:**
Read both paragraphs in full. Are they:
- Same point, different words?
- Different points with shared vocabulary?
- One elaborating on the other?

**Actions:**
| Finding | Action |
|---------|--------|
| Same point, different words | Merge best parts into one |
| Different points | Keep both (false positive) |
| One elaborates other | Keep detailed version, delete summary version |

---

## Issue Type: Structural Redundancy (Manual Review)

The script flags candidates, but these require human judgment:

**Multiple summary sections**
- Check if "Key Findings", "Summary", "Conclusion" repeat same bullets

**Collapsible boxes duplicating body**
- Is the "Key Metric Derivations" collapse just repeating body content?

**Tables duplicating adjacent prose**
- Are values in tables also stated in sentences before/after?

**Repetition signal phrases** (search for these):
- "As mentioned earlier..."
- "Recall that..."
- "As noted in the previous section..."
- "To reiterate..."

These often mean: content can be deleted, or replaced with a link.

---

## Phase 3: Verification

```bash
# For _latex: count remaining occurrences
grep -o "{{< var [a-z_]*_latex >}}" <file.qmd> | sort | uniq -c | sort -rn

# Re-run redundancy check
.venv/Scripts/python.exe scripts/redundancy-check.py <file.qmd>

# Validate no broken references
.venv/Scripts/python.exe scripts/pre-render-validation.py 2>&1 | grep <filename>
```

**Success criteria:**
- Every `_latex` variable has 1-2 occurrences (no 3+ duplicates)
- Similar heading pairs resolved (merged, renamed, or confirmed intentional)
- Duplicate sentences eliminated
- Total redundancy reduced while preserving multi-audience structure

---

## Quick Reference: Common Patterns

| Pattern | Solution |
|---------|----------|
| Same equation appears 3+ times | Reduce to 1-2 (keep summary + derivation) |
| Same equation 6 lines apart | Delete the repeat |
| Equation after table with same values | Delete equation (table values are links) |
| Summary callout + verification section | Keep both (multi-audience design) |
| Sentence appears in intro AND conclusion | Keep in conclusion, delete from intro |
| Paragraph in "Summary" nearly identical to "Conclusion" | Merge into Conclusion, delete Summary section |
| Similar headings in different contexts | Rename to clarify distinction |

**Heading fixes (to prevent future false positives):**

| Ambiguous | Improved |
|-----------|----------|
| "[Topic] Assumptions" (in Limitations) | "[Topic] Uncertainty" |
| "[Topic]" (appearing twice) | "[Topic] Mechanism" vs "[Topic] Summary" |
| "[Topic] Feasibility" (in Limitations) | "[Topic] Feasibility Constraints" |
| Generic "[Topic]" + Specific "[Topic] X" | Keep both (general → specific) |
