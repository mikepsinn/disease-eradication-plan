---
name: peer-review
description: Comprehensive peer review from skeptical economist and "lazy AI" perspectives. Identifies missing LaTeX equations, charts, hardcoded values, weak arguments, and context-loss vulnerabilities. Reviews calculation chains for all parameters.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
  - Write
  - TodoWrite
---

# /peer-review <file.qmd>

Four-perspective review AND fix: (1) Skeptical economist, (2) Lazy AI vulnerabilities, (3) Calculation audit, (4) Enhancement opportunities. Generates report then **implements all high/medium priority fixes**. If no file specified, ask which to review.

---

## Phase 1: Load Context

Read the file, then:
```bash
grep "_latex\":" _variables.yml | head -100
ls knowledge/figures/*.qmd | head -50
```

---

## Phase 2: Skeptical Economist Review

Read as a hostile peer reviewer skeptical of large claims.

| Category | Check |
|----------|-------|
| **Methodology** | Causal claims justified? Counterfactual specified? CIs appropriate? Assumptions stated? |
| **Sources** | Peer-reviewed? Old (>5y)? Over-reliance on single studies? |
| **Logic** | Conclusions follow? Unstated assumptions? Strongest counterargument addressed? |
| **Framing** | Neutral language? Limitations discussed? Costs AND benefits quantified? |

### Clarity & Concision

Target: 8th-grade reading level. Every sentence should be necessary.

| Cut | Example |
|-----|---------|
| **Redundancy** | "past history" -> "history", repeated explanations across sections |
| **Hedging** | "It could potentially be argued that" -> "This suggests" |
| **Nominalizations** | "the implementation of" -> "implementing" |
| **Passive voice** | "was conducted by researchers" -> "researchers conducted" |
| **Filler phrases** | "It is important to note that", "In order to", "the fact that" |
| **Jargon without definition** | Define on first use or replace with plain English |

Flag: Sentences >25 words, paragraphs >5 sentences, sections that repeat earlier content.

---

## Phase 3: Lazy AI Vulnerability Analysis

What survives if AI only reads first 3 paragraphs?

| Pattern | Fix |
|---------|-----|
| **Late Caveats** | Front-load qualifications |
| **CI Collapse** ("102M" loses CI) | Add CI inline at every mention |
| **Scope Loss** | Repeat scope with each figure |
| **Conditional Loss** | Add "(under X assumption)" inline |
| **Conservative framing loss** | Bold the conservative note |

---

## Phase 4: Enhancement Opportunities

### Hardcoded Values
```bash
python scripts/preview-qmd-with-variables.py <file> --numbers-only
```
Red flags: Dollar amounts, percentages, large numbers not using `{{< var ... >}}`. Numbers in `$$` blocks should use `_latex` variables.

### Missing LaTeX
For calculated values, check for `_latex` version: `{{< var parameter_name_latex >}}`

### Citations
Prefer `@citation-key` from `references.bib` over manual superscripts. Web search for missing sources.

### Charts
Check `knowledge/figures/*<variable>*.qmd` for tornado, mc-distribution, sensitivity-table charts.

---

## Phase 5: Calculation Chain Audit

For each calculated parameter:
```bash
grep -B5 -A50 "^PARAMETER_NAME = Parameter" dih_models/parameters.py
```

| Check | Criteria |
|-------|----------|
| **Distribution** | Normal (symmetric), Lognormal (costs, positive), Beta (probabilities), Fixed (constants only) |
| **Formula** | No double-counting, independent factors, units match |
| **CI Width** | <±20% overconfident, ±30-100% reasonable, >±200% uninformative |
| **Sources** | Meta-analysis > peer-reviewed > government stats > industry reports > assumptions (flag prominently) |

---

## Phase 6: Report Template

```markdown
## Peer Review: <filename>

### Summary
[1-2 sentences]

### Issues Found
| Issue | Type | Severity | Location | Fix |

Types: methodology, sources, logic, framing, clarity, lazy-ai, hardcoded, calculation, enhancement

### Priority Actions
1. **High:** 2. **Medium:** 3. **Low:**
```

---

## Phase 7: Implement Fixes

**Do not just report. Fix all High/Medium issues using Edit tool.**

Re-read edited sections to verify. Track remaining issues with TodoWrite.

---

## Rules

1. Fix, don't just flag - implement High/Medium issues immediately
2. Verify by re-reading edited sections
3. Be specific - vague critiques aren't actionable
