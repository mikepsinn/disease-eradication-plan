---
name: review-qmd
description: Comprehensive single-file review. Generates preview with variables replaced, finds and replaces hardcoded values, adds _latex equations, validates consistency.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
  - Write
  - TodoWrite
---

# /review-qmd <file.qmd>

Comprehensive single-file review covering: variable consistency, content quality, and reader engagement.

## Usage
```
/review-qmd knowledge/appendix/incentive-alignment-bonds-paper.qmd
/review-qmd economics.qmd
```
If no file specified, ask which file to review.

---

## Phase 1: Generate Preview

```bash
cd E:/code/obsidian/websites/disease-eradication-plan
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file> -o _analysis/<basename>-preview.md
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file> --numbers-only
```

Read preview to understand rendered state. Note inconsistencies (e.g., "$2.4T" vs "$2.72T").

---

## Phase 2: Variable Audit

**REPLACE with variables:**
- Core metrics: military spending, treaty funding, DALYs, household wealth, war costs
- Calculated values: BCR, mechanism costs/benefits, peace dividend
- Any value appearing multiple times

**KEEP hardcoded:**
- Citation-specific data (Copenhagen Consensus BCRs, study figures)
- Illustrative examples, calibration parameters
- `1%` treaty concept, years in citations

**Variable lookup:**
```bash
grep -i "keyword" _analysis/parameter-summary.md
grep "value_pattern" _variables.yml
```

**Key variables:**
| Pattern | Variable | Value |
|---------|----------|-------|
| Military spending | `global_military_spending_annual_2024` | $2.72T |
| Treaty funding | `treaty_annual_funding` | $27.2B |
| War costs | `global_annual_direct_indirect_war_cost` | $11.4T |
| DALYs | `global_annual_daly_burden` | 2.88B |
| Household wealth | `global_household_wealth_usd` | $454T |
| IAB BCR | `iab_mechanism_benefit_cost_ratio` | 230:1 |

**Replace with _latex versions** for `$$` blocks containing calculations.

**Check for useful auto-generated charts:**
```bash
# List variables used in file
grep -o "{{< var [a-z_]* >}}" <file> | sed 's/{{< var //;s/ >}}//' | sort -u

# For each variable, check if charts exist in knowledge/figures/
ls knowledge/figures/*<variable_name>*.qmd
```

Charts available per calculated variable:
- `tornado-<var>.qmd` - Sensitivity analysis (which inputs matter most)
- `mc-distribution-<var>.qmd` - Monte Carlo probability distribution
- `exceedance-<var>.qmd` - Probability of exceeding thresholds
- `sensitivity-table-<var>.qmd` - Regression coefficients

**Add charts where they enhance understanding** - especially for key metrics like ROI, BCR, costs. Include with:
```markdown
{{< include ../figures/tornado-<variable_name>.qmd >}}
```

---

## Phase 3: Content Quality Review

Read through the preview and evaluate:

### Clarity & Accessibility
- [ ] **Plain English summaries** at section starts for non-technical readers
- [ ] **Jargon explained** on first use (define mechanism design, Nash equilibrium, BCR, etc.)
- [ ] **Concrete examples** before abstract formulas
- [ ] **Visual aids** referenced where helpful (figures, tables, infographics)

### Engagement & Persuasion
- [ ] **Strong opening hook** - Does the intro grab attention? Lead with the problem/stakes
- [ ] **Emotional resonance** - Connect to human impact (lives saved, suffering prevented)
- [ ] **Vivid comparisons** - Make abstract numbers concrete ("enough to fund X hospitals")
- [ ] **Call to action** - Clear next steps for different audiences (investors, policymakers, researchers)

### Rigor & Credibility
- [ ] **Claims have citations** - Every factual claim backed by source
- [ ] **Uncertainty acknowledged** - Confidence intervals, limitations stated
- [ ] **Counterarguments addressed** - Steel-man objections, then refute
- [ ] **Math checks out** - Calculations internally consistent

### Flow & Structure
- [ ] **Logical progression** - Each section builds on previous
- [ ] **Transitions** - Clear connections between ideas
- [ ] **Scannable** - Headers, bullets, bold key points for skimmers

### Cut the Garbage
- [ ] **Redundancy** - Same point made multiple times? Consolidate (pre-render validation detects duplicate `_latex` vars automatically)
- [ ] **Filler phrases** - "It is important to note that..." → delete
- [ ] **Weak qualifiers** - "somewhat", "fairly", "quite" → remove or strengthen
- [ ] **Orphaned content** - Sections that don't connect to main argument
- [ ] **Over-explanation** - Reader got it the first time
- [ ] **Defensive hedging** - Excessive caveats that undermine confidence

### Tone
- [ ] **Confident but not arrogant** - State conclusions clearly, acknowledge limits
- [ ] **Urgent but not alarmist** - Convey stakes without hyperbole
- [ ] **Technical but accessible** - Expert credibility with lay readability
- [ ] **No "consultantly" language** - Avoid buzzwords, empty phrases

### Publication Readiness
- [ ] **No implementation code** - Python/SQL → pseudocode or math notation, link to repo
- [ ] **Math notation** - `forward_pearson_correlation_coefficient` → $r_{forward}$
- [ ] **Proper tables** - No ASCII art (`═══`, `───`) - use markdown tables
- [ ] **Appendix placement** - Move detailed algorithms/schemas to appendix or supplementary

---

## Phase 4: Make Improvements

Use Edit tool to fix identified issues. Track changes with TodoWrite.

**Common fixes:**
- Add "**The short version:**" summaries to dense sections
- Replace jargon: "mechanism design" → "mechanism design (designing rules so selfish choices create good outcomes)"
- Add concrete examples before formulas
- Strengthen weak openings with stakes
- **CUT**: redundant paragraphs, filler phrases, weak hedging, over-explanation
- Add missing citations with `{{< var variable_cite >}}`
- Replace `$$` blocks with `{{< var variable_latex >}}`

---

## Phase 5: Validate

Run pre-render validation to catch automated issues:

```bash
.venv/Scripts/python.exe scripts/pre-render-validation.py 2>&1 | grep -A2 "<filename>"
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file> --line-range "1-50"
```

**Automated checks include:**
- `[MISSING: variable]` - undefined variables
- Duplicate `_latex` variables (redundant equations)
- Broken links and anchor IDs
- Missing citations and imports
- Unclosed code blocks
- Em-dashes (should be commas/periods)

**If duplicate _latex variables found:**
1. Review both occurrences - are they truly redundant?
2. If redundant, remove the duplicate (keep the one in better context)
3. If both needed, consider if they're explaining different aspects

---

## Phase 6: Report

```markdown
## Review Complete: <filename>

### Preview: `_analysis/<basename>-preview.md`

### Variable Replacements
| Line | Old | New Variable |
|------|-----|--------------|

### Content Improvements
- [x] Added plain English summary to Section X
- [x] Fixed weak opening in intro
- [x] Added concrete example for BCR concept

### Kept Hardcoded (Intentional)
- Copenhagen Consensus data, calibration params, 1% treaty

### Validation: PASSED
```

---

## Rules

1. Generate preview FIRST - understand before editing
2. Track changes with TodoWrite
3. Semantic match required - same number can mean different things
4. NEVER replace `1%` treaty concept
5. Skip citation-specific data
6. Run validation AFTER changes
7. Improve engagement, not just accuracy
