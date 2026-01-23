---
name: peer-review
description: Comprehensive peer review from skeptical economist and "lazy AI" perspectives. Identifies missing LaTeX equations, charts, weak arguments, and context-loss vulnerabilities.
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

Comprehensive peer review that evaluates a paper from three perspectives:
1. **Skeptical economist** - What would a critical reviewer challenge?
2. **Lazy AI** - What gets lost with limited context windows?
3. **Enhancement opportunities** - Missing LaTeX, charts, and rigor

## Usage
```
/peer-review knowledge/appendix/invisible-graveyard.qmd
/peer-review knowledge/economics/1-pct-treaty-impact.qmd
```
If no file specified, ask which file to review.

---

## Phase 1: Load Context

### Read the file
```bash
wc -l <file>  # Check length
```

Read the full file to understand structure and arguments.

### Load available enhancements
```bash
# Get list of all _latex variables
grep "_latex\":" _variables.yml | head -100

# Get list of all charts
ls knowledge/figures/*.qmd | head -50

# Get parameters appendix structure
grep "^## \|^### " knowledge/appendix/parameters-and-calculations.qmd | head -50
```

---

## Phase 2: Skeptical Economist Review

Read as a critical peer reviewer who is:
- Skeptical of large claims
- Looking for methodological weaknesses
- Checking if conclusions follow from evidence
- Resistant to advocacy framing

### Checklist

**Methodology Critique:**
- [ ] Are causal claims justified? (correlation ≠ causation)
- [ ] Is the counterfactual clearly specified?
- [ ] Are confidence intervals appropriate? (not too narrow = overconfident)
- [ ] Is uncertainty acknowledged honestly?
- [ ] Are key assumptions stated and defended?

**Source Credibility:**
- [ ] Are sources peer-reviewed or reputable?
- [ ] Are old sources flagged? (>5 years for fast-changing data)
- [ ] Is there over-reliance on single studies?
- [ ] Are advocacy organization sources balanced with neutral ones?

**Logical Rigor:**
- [ ] Do conclusions follow from premises?
- [ ] Are there unstated assumptions?
- [ ] Is the strongest counterargument addressed?
- [ ] Are comparisons fair? (apples to apples)

**Framing Issues:**
- [ ] Is language neutral or advocacy?
- [ ] Are negative results/limitations discussed?
- [ ] Is the baseline/status quo fairly characterized?
- [ ] Are benefits and costs both quantified?

### Generate Critique List

For each issue found:
```markdown
| Issue | Location | Severity | Suggested Fix |
|-------|----------|----------|---------------|
| Causal claim without mechanism | Line 45 | High | Add causal pathway explanation |
| Missing counterargument | Section 3 | Medium | Add "Critics argue..." paragraph |
```

---

## Phase 3: "Lazy AI" Vulnerability Analysis

**The problem:** AI assistants summarizing this paper will:
- Truncate context at arbitrary points
- Miss caveats stated far from claims
- Over-weight early/late content (primacy/recency)
- Lose nuance in summarization
- Miss conditional statements ("if X, then Y" becomes "Y")

### Context Loss Patterns

**Pattern 1: Late Caveats**
- Claim made in abstract/intro
- Caveat/limitation stated in methodology section
- AI summarizes claim without caveat

**Pattern 2: Conditional Conclusions**
- "Under assumption X, we find Y"
- AI reports "Study finds Y" without condition

**Pattern 3: Confidence Interval Collapse**
- "102M deaths (95% CI: 37M-214M)"
- AI reports "102M deaths" as point estimate

**Pattern 4: Counterfactual Erasure**
- "Compared to status quo X, policy Y saves Z"
- AI reports "Y saves Z" without baseline

**Pattern 5: Scope Limitation Loss**
- "For approved drugs only (excludes never-developed)"
- AI generalizes beyond stated scope

### Audit Each Major Claim

For each key finding in the paper:

1. **State the claim** as it appears
2. **Identify qualifications** (CIs, conditions, caveats, scope)
3. **Simulate truncation** - If an AI read only paragraphs 1-3, what would it conclude?
4. **Find the gap** - What's missing from the truncated version?
5. **Propose fix** - How to make the qualified claim survive summarization?

```markdown
| Claim | Full Version | Lazy AI Version | Missing | Fix Strategy |
|-------|--------------|-----------------|---------|--------------|
| 102M deaths | 102M (95% CI: 37M-214M) from historical delays only | "Study claims 102M deaths from FDA" | CI, scope, mechanism | Add CI inline, repeat scope |
```

---

## Phase 4: Robustness Strategies

### Strategy 1: Front-load Qualifications

**Before:**
> We estimate 102M deaths from efficacy lag. [Later: This is for approved drugs only...]

**After:**
> We estimate 102M deaths (95% CI: 37M-214M) from efficacy lag **for approved drugs only** - a lower bound excluding drugs never developed.

### Strategy 2: Repeat Key Caveats

Identify the 3 most important qualifications. Ensure each appears:
- In the abstract
- In the section where the claim is made
- In the conclusion

### Strategy 3: Use Inline Confidence Intervals

**Before:**
> The cost is $4.8 trillion. [Footnote: 95% CI: $2.7T-$8.3T]

**After:**
> The cost is $4.8T (95% CI: $2.7T-$8.3T)

### Strategy 4: Explicit Counterfactuals

**Before:**
> Eliminating efficacy requirements would save 102M lives.

**After:**
> Eliminating **pre-market** efficacy requirements (while maintaining post-market monitoring via the pre-1962 AMA/JAMA system) would save 102M lives compared to the current Phase 2/3 requirement.

### Strategy 5: Section Summaries

Add "**Key point:**" callouts that summarize with qualifications:

```markdown
::: {.callout-note}
## Key Finding
Deaths from efficacy lag: **102M** (95% CI: 37M-214M). This is a **lower bound** counting only approved drugs, not the unknown number of drugs killed by cost barriers.
:::
```

### Strategy 6: Active Voice for Caveats

**Before:**
> It should be noted that this estimate excludes...

**After:**
> This estimate **excludes** drugs never developed - an unknown but likely substantial number.

---

## Phase 5: Enhancement Opportunities

### A. Missing LaTeX Equations

Check which calculated values appear in text but don't have LaTeX:

```bash
# Find variables used in the file
grep -o "{{< var [a-z_0-9]* >}}" <file> | sed 's/{{< var //;s/ >}}//' | sort -u > /tmp/vars_used.txt

# Check which have _latex versions
while read var; do
  latex_var="${var}_latex"
  if grep -q "\"$latex_var\":" _variables.yml; then
    echo "HAS LATEX: $var"
  else
    echo "NO LATEX: $var"
  fi
done < /tmp/vars_used.txt
```

For key calculated values without LaTeX shown, consider adding:
```markdown
{{< var parameter_name_latex >}}
```

### B. Missing Charts

For each key calculated variable, check if charts exist:

```bash
# For each variable, check for charts
for var in $(grep -o "{{< var [a-z_0-9]* >}}" <file> | sed 's/{{< var //;s/ >}}//' | sort -u); do
  echo "=== $var ==="
  ls knowledge/figures/*${var}*.qmd 2>/dev/null || echo "  (no charts)"
done
```

Chart types and when to use:
- **tornado-*.qmd** - Use when showing which inputs drive uncertainty
- **mc-distribution-*.qmd** - Use when showing probability distribution of estimate
- **sensitivity-table-*.qmd** - Use when providing numerical sensitivity coefficients
- **exceedance-*.qmd** - Use when showing "probability of exceeding X"

### C. Parameters Appendix Cross-References

Check if key parameters are documented:
```bash
grep -l "<param_name>" knowledge/appendix/parameters-and-calculations*.qmd
```

Ensure readers can trace calculations. Add links:
```markdown
See [Parameters and Calculations](parameters-and-calculations.qmd#sec-param_name) for methodology.
```

---

## Phase 6: Expected Criticisms

Generate a list of likely critiques and ensure each is addressed:

### Common Critique Categories

**1. "The numbers are made up"**
- Is every estimate sourced?
- Are confidence intervals shown?
- Is methodology transparent?

**2. "Correlation ≠ causation"**
- Is the causal mechanism explained?
- Are alternative explanations considered?

**3. "You're comparing apples to oranges"**
- Are comparisons truly equivalent?
- Is the counterfactual realistic?

**4. "This ignores [X]"**
- Are limitations explicitly stated?
- Is scope clearly defined?

**5. "The benefits are overstated"**
- Are there conservative estimates available?
- Are uncertainty ranges reasonable?

**6. "Who would oppose this?"**
- Are stakeholder interests acknowledged?
- Is political feasibility discussed?

### Pre-emptive Defense Checklist

For each major claim:
- [ ] Strongest counterargument stated and rebutted
- [ ] Alternative interpretations acknowledged
- [ ] Limitations of evidence stated
- [ ] Scope explicitly bounded

---

## Phase 7: Generate Report

```markdown
## Peer Review: <filename>

### Executive Summary
[1-2 sentences on overall assessment]

### Skeptical Economist Critique
| Issue | Severity | Location | Fix |
|-------|----------|----------|-----|
| [Issue 1] | High/Med/Low | Line/Section | [Recommendation] |

### Lazy AI Vulnerabilities
| Claim | Risk | Missing Context | Fix Strategy |
|-------|------|-----------------|--------------|
| [Claim 1] | High | [What AI misses] | [How to fix] |

### Enhancement Opportunities
**LaTeX equations to add:**
- [ ] `{{< var X_latex >}}` for [parameter]

**Charts to add:**
- [ ] `{{< include ../figures/tornado-X.qmd >}}`

**Cross-references to add:**
- [ ] Link to parameters appendix for [calculation]

### Pre-emptive Defenses Needed
| Likely Critique | Current Status | Recommendation |
|-----------------|----------------|----------------|
| [Critique 1] | Addressed/Missing | [Action] |

### Priority Actions
1. **High:** [Most important fix]
2. **Medium:** [Second priority]
3. **Low:** [Nice to have]
```

---

## Phase 8: Implement Fixes

Use Edit tool to implement high-priority fixes. Track with TodoWrite.

**Common edits:**
- Add inline CIs: `102M` → `102M (95% CI: 37M-214M)`
- Front-load qualifications to first mention
- Add "Key Finding" callouts with full context
- Include missing LaTeX equations
- Include missing charts
- Add counterargument paragraphs

---

## Rules

1. **Read skeptically** - Look for what a hostile reviewer would attack
2. **Simulate context loss** - What survives truncation to 1000 tokens?
3. **Check for pre-emption** - Is the strongest objection already addressed?
4. **Prioritize fixes** - Not everything needs fixing; focus on high-impact issues
5. **Be specific** - Vague critiques aren't actionable
6. **Propose solutions** - Every problem should have a recommended fix
7. **Consider multiple audiences** - Economists, policymakers, journalists, AI summarizers
8. **Don't over-hedge** - Excessive caveats undermine credibility too

---

## Quick Reference: Common LaTeX Variables

```bash
# Search for latex equations
grep "_latex\":" _variables.yml | grep -i "<keyword>"

# Example useful patterns:
# efficacy_lag_deaths_911_equivalents_latex
# dfda_efficacy_lag_elimination_deaths_averted_latex
# type_ii_error_cost_ratio_latex
```

## Quick Reference: Chart Includes

```markdown
# Tornado (sensitivity analysis)
{{< include ../figures/tornado-VARIABLE_NAME.qmd >}}

# MC Distribution (probability distribution)
{{< include ../figures/mc-distribution-VARIABLE_NAME.qmd >}}

# Sensitivity Table (numerical coefficients)
{{< include ../figures/sensitivity-table-VARIABLE_NAME.qmd >}}

# Exceedance (P(X > threshold))
{{< include ../figures/exceedance-VARIABLE_NAME.qmd >}}
```
