---
name: critique-calculation
description: Critically analyze a calculated parameter for academic rigor. Checks methodology, identifies weaknesses, suggests improvements for economist audiences.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - TodoWrite
---

# /critique-calculation <PARAMETER_NAME>

Critically analyze a calculated parameter for academic defensibility. Identifies methodological weaknesses and suggests improvements that would make the calculation more persuasive to economists.

## Usage
```
/critique-calculation POLITICAL_DYSFUNCTION_TAX_TOTAL_PCT
/critique-calculation TREATY_COMPLETE_ROI_EXPECTED
/critique-calculation DFDA_NET_BENEFIT_ANNUAL
```

If no parameter specified, list calculated parameters and ask which to review.

---

## Phase 1: Identify the Calculation

Find the parameter definition:
```bash
grep -B5 -A50 "^<PARAM_NAME> = Parameter" dih_models/parameters.py
```

Extract:
- **Formula/compute function**: How is it calculated?
- **Inputs**: What parameters feed into it?
- **Source type**: calculated, external, definition?
- **Confidence interval**: Is uncertainty properly propagated?

---

## Phase 2: Trace Input Dependencies

For each input parameter:
```bash
grep -B5 -A30 "^<INPUT_NAME> = Parameter" dih_models/parameters.py
```

Build dependency tree:
```
TARGET_PARAM
├── INPUT_1 (source: external, ref: study2023)
├── INPUT_2 (source: calculated)
│   ├── INPUT_2a (source: external, ref: who2024)
│   └── INPUT_2b (source: definition)
└── INPUT_3 (source: definition)
```

Classify each leaf input:
- **Empirically grounded**: Has peer-reviewed source with specific estimate
- **Theoretically grounded**: Based on theory but no empirical estimate
- **Definition/assumption**: Policy parameter or modeling choice

---

## Phase 3: Methodological Critique

### A. Additivity/Independence Check

**If formula uses addition** (A + B + C):
- Do components overlap? (Double-counting risk)
- Would multiplicative model be more appropriate?
  - Additive: τ_total = τ_1 + τ_2 + τ_3
  - Multiplicative: τ_total = 1 - (1-τ_1)(1-τ_2)(1-τ_3)
- Is there theoretical justification for additivity?

**If formula uses multiplication** (A × B × C):
- Are factors truly independent?
- Could there be interaction effects?

### B. Empirical Backing Assessment

Rate each input:
| Input | Source Type | Empirical Strength |
|-------|-------------|-------------------|
| INPUT_1 | Meta-analysis | **Strong** |
| INPUT_2 | Single study | Medium |
| INPUT_3 | Theoretical | Weak |
| INPUT_4 | Assumption | None |

**Red flags:**
- Key inputs with no empirical backing
- Large uncertainty on dominant inputs
- Sources from advocacy organizations vs peer review
- Old data (>10 years) for fast-changing metrics

### C. Uncertainty Propagation Check

```bash
# Check if inputs have uncertainty metadata
grep -E "confidence_interval|distribution|std_error" dih_models/parameters.py | grep -i "<input_names>"
```

Verify:
- All leaf inputs have uncertainty (CI, distribution, or std_error)
- Calculated parameter derives uncertainty from Monte Carlo
- CI width is plausible (not too narrow = overconfident, not too wide = useless)

### D. Sensitivity Analysis

Check if tornado/sensitivity charts exist:
```bash
ls knowledge/figures/tornado-<param_name>*.qmd
ls _analysis/tornado_<PARAM_NAME>.json
```

Review sensitivity results:
- Which inputs dominate the output variance?
- Are the dominant inputs well-grounded empirically?
- Would reducing uncertainty on key inputs substantially tighten the estimate?

---

## Phase 4: Identify Improvements

Categorize potential improvements by effort/impact:

### Low Effort, High Impact
- Fix additivity with multiplicative model
- Add confidence intervals to inputs missing them
- Cite better sources for key inputs
- Acknowledge overlap explicitly in text

### Medium Effort, Medium Impact
- Find empirical estimates for theoretically-grounded inputs
- Add sensitivity analysis if missing
- Split aggregate parameters into measurable components

### High Effort (Note for Future)
- Commission original research to fill gaps
- Build more sophisticated interaction models
- Conduct meta-analysis of existing estimates

---

## Phase 5: Generate Report

```markdown
## Calculation Critique: <PARAMETER_NAME>

### Summary
- **Central estimate:** X (95% CI: Y-Z)
- **Formula:** [describe calculation]
- **Academic defensibility:** Strong / Medium / Weak

### Dependency Tree
[ASCII tree of inputs]

### Empirical Grounding
| Component | Backing | Strength | Key Source |
|-----------|---------|----------|------------|

### Methodological Issues
1. **[Issue]:** [Description]
   - **Impact:** [How it affects credibility]
   - **Fix:** [Recommended solution]

### Recommended Improvements
**Quick wins:**
- [ ] [Improvement 1]
- [ ] [Improvement 2]

**Consider for future:**
- [ ] [Improvement 3]

### What Economists Would Ask
1. [Likely challenge and how to respond]
2. [Likely challenge and how to respond]
```

---

## Common Patterns

### Pattern: Additive Components That Overlap
**Problem:** Sum of parts > whole due to double-counting
**Fix:** Use multiplicative model: 1 - Π(1-τ_i)
**Example:** Political dysfunction tax components

### Pattern: Theoretical Decomposition Without Empirical Parts
**Problem:** Elegant theory, but component estimates are guesses
**Fix:** Either find empirical estimates OR present as conceptual framework, not precise calculation
**Example:** Time-inconsistency, information, coordination taxes

### Pattern: Single Study Anchor
**Problem:** Entire calculation depends on one study's estimate
**Fix:** Cite meta-analysis if available, OR widen confidence interval, OR conduct sensitivity to source
**Example:** Del Rosal (2011) rent-seeking survey

### Pattern: Stale Data
**Problem:** Key inputs from 5+ years ago for rapidly changing metrics
**Fix:** Update with recent data, OR note vintage and direction of likely bias
**Example:** GDP, spending, population figures

### Pattern: Missing Counterfactual
**Problem:** Benefit calculated vs. status quo, but status quo is changing
**Fix:** Specify baseline scenario, consider alternative counterfactuals
**Example:** DFDA benefits vs. current FDA (but FDA is evolving)

---

## Rules

1. **Be honest about weaknesses** - Credibility comes from acknowledging limits
2. **Propose fixes, not just critiques** - Every issue should have a recommendation
3. **Distinguish fatal flaws from minor issues** - Not everything needs fixing
4. **Consider the audience** - What would a skeptical economist ask?
5. **Check if fixes already exist** - Maybe the issue is presentation, not calculation
