---
active: true
iteration: 1
max_iterations: 50
completion_promise: "ALL_FILES_PROCESSED"
started_at: "2026-01-08T04:02:19Z"
---

# Ralph Loop: Systematic Hardcoded Value Replacement

## Task
Replace hardcoded numbers in QMD files with `{{< var variable_name >}}` references from `_variables.yml`.

## Systematic Process

### Step 1: Run Audit (Each Session Start)
```bash
npx tsx scripts/audit-hardcoded-all.ts --output _hardcoded-audit-latest.md
```
This generates a report with HIGH/MEDIUM/LOW confidence matches.

### Step 2: Process HIGH Confidence Matches Only
The audit report has sections:
- **High Confidence Replacements** - SAFE to fix, strong context match
- **Medium Confidence** - Review needed, may be wrong
- **Low Confidence** - Likely false positives, SKIP

**ONLY fix HIGH confidence matches.**

### Step 3: Work Through Files Systematically

For each file in the High Confidence section:

1. **Read the file** to understand context
2. **Make replacements** using Edit tool:
   - `$27.2B` → `{{< var treaty_annual_funding >}}`
   - `$2.6 billion` → `{{< var pharma_drug_development_cost_current >}}`
   - etc.
3. **Verify semantic match** - same number can mean different things!
4. **Move to next file**

### Step 4: Track Progress

After fixing a batch of files, re-run audit:
```bash
npx tsx scripts/audit-hardcoded-all.ts --output _hardcoded-audit-latest.md
```

Report remaining count. When high-confidence = 0, output: `ALL_FILES_PROCESSED`

## Critical Rules

1. **NEVER replace `1%`** - Treaty concept, not a variable
2. **SKIP years in citations** - `@source-2024` keeps the year
3. **SKIP Medium/Low confidence** - They need human review
4. **Verify context** - `$27B` for treaty funding ≠ `$27B` for something else
5. **One concept at a time** - Don't batch unrelated replacements

## Common Variable Mappings

| Hardcoded | Variable | Context Keywords |
|-----------|----------|------------------|
| `$27.2B`, `$27B` | `treaty_annual_funding` | treaty, funding, 1% |
| `$2.6B`, `$2.6 billion` | `pharma_drug_development_cost_current` | FDA, drug, approval, pharma |
| `$93K`, `$93,000` | `switzerland_gdp_per_capita_k` | Switzerland, GDP, per capita |
| `$20M`, `$20 million` | `recovery_trial_total_cost` | RECOVERY trial, Oxford |
| `10%` | `victory_bond_funding_pct` OR `iab_political_incentive_funding_pct` | bonds, investors OR political, IAB |
| `80%` | `dih_treasury_medical_research_pct` | medical research, treasury, cures |
| `86.1%` | `antidepressant_trial_exclusion_rate` | exclusion, trial, patients |
| `$1B`, `$1.0B` | `treaty_campaign_total_cost` | campaign, budget, raise |
| `0.7%` | `switzerland_defense_spending_pct` | Switzerland, military, defense |
| `$41K`, `$41,000` | `traditional_phase3_cost_per_patient` | phase 3, traditional, per patient |

## File Priority Order

1. `knowledge/strategy/` - High visibility
2. `knowledge/solution/` - Core content
3. `knowledge/economics/` - Numbers-heavy
4. `knowledge/problem/` - Supporting content
5. `knowledge/appendix/` - Reference material
6. Everything else

## Completion Criteria

When `npx tsx scripts/audit-hardcoded-all.ts` shows:
- **High confidence matches: 0**

Output: `ALL_FILES_PROCESSED`
