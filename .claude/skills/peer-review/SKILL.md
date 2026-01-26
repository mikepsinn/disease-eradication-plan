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

Comprehensive peer review evaluating a paper from four perspectives:
1. **Skeptical economist** - What would a critical reviewer challenge?
2. **Lazy AI** - What gets lost with limited context windows?
3. **Calculation chain audit** - Are formulas, distributions, and uncertainty propagation optimal?
4. **Enhancement opportunities** - Missing LaTeX, charts, hardcoded values replaceable with variables

If no file specified, ask which file to review.

---

## Phase 1: Load Context

Read the full file. Then load available enhancements:
```bash
# Get _latex variables and charts
grep "_latex\":" _variables.yml | head -100
ls knowledge/figures/*.qmd | head -50
```

---

## Phase 2: Skeptical Economist Review

Read as a critical peer reviewer who is skeptical of large claims, looking for methodological weaknesses, checking if conclusions follow from evidence, and resistant to advocacy framing.

**Checklist:**

| Category | Questions |
|----------|-----------|
| **Methodology** | Causal claims justified? Counterfactual specified? CIs appropriate? Assumptions stated? |
| **Sources** | Peer-reviewed? Old sources flagged (>5y)? Over-reliance on single studies? |
| **Logic** | Conclusions follow premises? Unstated assumptions? Strongest counterargument addressed? |
| **Framing** | Neutral language? Limitations discussed? Costs AND benefits quantified? |

**Output format:**
```markdown
| Issue | Location | Severity | Suggested Fix |
|-------|----------|----------|---------------|
```

---

## Phase 3: "Lazy AI" Vulnerability Analysis

AI assistants summarizing this paper will truncate context, miss caveats stated far from claims, and lose nuance. Check for these patterns:

| Pattern | Example | Fix |
|---------|---------|-----|
| **Late Caveats** | Claim in abstract, caveat in methodology | Front-load qualification |
| **CI Collapse** | "102M (95% CI: 37M-214M)" → "102M" | Add CI inline at every mention |
| **Scope Loss** | "For approved drugs only" gets dropped | Repeat scope with each figure |
| **Conditional Loss** | "Under assumption X, Y" → "Y" | Add "(under X assumption)" inline |
| **Conservative framing loss** | "This OVERSTATES benefits" gets missed | Bold the conservative note |

**For each major claim:** What survives if AI only reads first 3 paragraphs?

---

## Phase 4: Enhancement Opportunities

### A. Hardcoded Values Check

**CRITICAL:** Find hardcoded numbers that should be variables from `_variables.yml`.

```bash
# Use the preview script to find hardcoded numbers (preferred method)
python scripts/preview-qmd-with-variables.py <file> --numbers-only

# Or manual search (fallback)
grep -E '\$[0-9]+[BMTbmt]|\$[0-9,]+|[0-9]+%|[0-9]{4,}' <file> | head -30

# Check _variables.yml for matching values
grep -i "<keyword>" _variables.yml
```

**Red flags:**
- Dollar amounts not using `{{< var ... >}}`
- Percentages that match parameter values
- Large numbers (deaths, costs) that aren't variables
- Years/durations that match known parameters
- Any number in a `$$` LaTeX block (should use `_latex` variable instead)

### B. Missing LaTeX Equations

For calculated values, check if `_latex` version exists and is displayed:
```bash
# Extract variables used
grep -o "{{< var [a-z_0-9]* >}}" <file> | sed 's/{{< var //;s/ >}}//' | sort -u
```

For key calculated values, add: `{{< var parameter_name_latex >}}`

### C. Citation Format Check

**Prefer Quarto citations over manual superscripts.**

Check if document uses proper `@citation-key` format from `references.bib`:

If we need a source for a claim see if it is in `references.bib`. If it is not, 
use the web search tool to find the best source and add it to `references.bib`.

Then use proper Quarto citations in the qmd file.


### D. Missing Charts

Check if charts exist for key variables:
```bash
ls knowledge/figures/*<variable_name>*.qmd 2>/dev/null
```

Chart types: `tornado-*.qmd` (sensitivity), `mc-distribution-*.qmd` (uncertainty), `sensitivity-table-*.qmd` (coefficients)

---

## Phase 5: Calculation Chain Audit

For every **calculated parameter**, verify the chain is academically defensible.

### Extract and Trace
```bash
# Find parameter definition
grep -B5 -A50 "^PARAMETER_NAME = Parameter" dih_models/parameters.py
```

Build dependency tree. Classify leaf inputs as: empirically grounded, theoretically grounded, or definition/assumption.

### Distribution Check

| Distribution | When to Use | Red Flag |
|--------------|-------------|----------|
| **Normal** | Symmetric, can be negative | Used for strictly positive values |
| **Lognormal** | Right-skewed, strictly positive (costs) | Used for bounded percentages |
| **Beta** | Bounded probabilities [0,1] | Used for unbounded values |
| **Fixed** | Constitutional constants | Used when uncertainty exists |

### Formula Verification

- **Additivity**: Do components overlap? (Double-counting risk)
- **Independence**: Are multiplied factors truly independent?
- **Units**: Do input units combine correctly? (`deaths = deaths/year × years` ✓)

### CI Assessment

| Width | Assessment |
|-------|------------|
| < ±20% | Overconfident for complex estimates |
| ±30-100% | Reasonable for policy estimates |
| > ±200% | Potentially uninformative |

### Source Quality

| Type | Strength |
|------|----------|
| Meta-analysis | Strong |
| Peer-reviewed study | Medium-Strong |
| Government statistics | Medium |
| Industry reports | Medium-Low |
| Made-up assumption | Must flag prominently |

---

## Phase 6: Expected Criticisms

**Common critiques to pre-empt:**

1. "The calculation is wrong" → Show formula, check units
2. "The numbers are made up" → Source everything, show CIs
3. "Correlation ≠ causation" → Explain mechanism
4. "Apples to oranges" → Verify comparison equivalence
5. "This ignores [X]" → State limitations explicitly
6. "Benefits overstated" → Show conservative estimates
7. "Who opposes this?" → Acknowledge stakeholder interests

For each major claim: Is the strongest counterargument stated and rebutted?

---

## Phase 7: Generate Report

```markdown
## Peer Review: <filename>

### Executive Summary
[1-2 sentences]

### Skeptical Economist Critique
| Issue | Severity | Location | Fix |
|-------|----------|----------|-----|

### Lazy AI Vulnerabilities
| Claim | Risk | Missing Context | Fix Strategy |
|-------|------|-----------------|--------------|

### Hardcoded Values to Replace
| Value | Location | Suggested Variable |
|-------|----------|-------------------|

### Calculation Chain Audit
| Parameter | Formula | Distribution Issues | Source Quality | Recommendation |
|-----------|---------|---------------------|----------------|----------------|

### Enhancement Opportunities
- LaTeX equations to add
- Charts to add
- Cross-references to add

### Pre-emptive Defenses Needed
| Critique | Status | Recommendation |
|----------|--------|----------------|

### Priority Actions
1. **High:** [Most important]
2. **Medium:** [Second priority]
3. **Low:** [Nice to have]
```

---

## Phase 8: Implement Fixes

Use Edit tool to implement high-priority fixes. Track with TodoWrite.

**Common edits:**
- Replace hardcoded values: `$2.6B` → `{{< var pharma_drug_development_cost_current >}}`
- Add inline CIs: `102M` → `102M (95% CI: 37M-214M)`
- Front-load qualifications
- Add charts after key figures
- Add "(lower bound)" or "(conservative)" notes inline

**Parameter fixes (in parameters.py):**
- Change distribution for costs: `normal` → `lognormal`
- Widen narrow CIs
- Add uncertainty to fixed inputs

---

## Rules

1. Read skeptically - what would a hostile reviewer attack?
2. Simulate context loss - what survives 1000-token truncation?
3. Check hardcoded values - every number should trace to `_variables.yml`
4. Prioritize fixes - focus on high-impact issues
5. Be specific - vague critiques aren't actionable
6. Propose solutions - every problem needs a recommended fix
