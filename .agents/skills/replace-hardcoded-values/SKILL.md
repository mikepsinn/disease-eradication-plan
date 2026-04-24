---
name: replace-hardcoded-values
description: Systematically finds and replaces hardcoded numbers in QMD files with variables from _variables.yml. Use when auditing book for consistency.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
---

# Replace Hardcoded Values with Variables

## Purpose

Systematically audit QMD files for hardcoded numbers that should be replaced with `{{< var variable_name >}}` references.

## When to Use

- After batch adding new parameters to `parameters.py`
- Before major commits or releases
- When auditing specific chapters for variable consistency
- After noticing hardcoded values in a file

## Process

### Phase 1: Load Variable Lookup

Read the compact variable reference (no HTML noise, one line per variable):

```bash
cat _analysis/variable-lookup-compact.txt
```

Format: `var_name: display_value  [has _nounit]`

This file contains all ~471 variables stripped of HTML tooltips. If it doesn't exist, regenerate it (see Regeneration section below).

### Phase 2: Find Hardcoded Values

For each target QMD file, run the numbers-only preview:

```bash
python scripts/preview-qmd-with-variables.py FILE --numbers-only
```

This flags hardcoded DOLLAR AMOUNTS, LARGE NUMBERS, and PERCENTAGES with line numbers and context. Use this as your primary discovery tool.

### Phase 3: Semantic Matching (Critical)

For each hardcoded value found, use **semantic judgment**, not exact matching:

- Hardcoded `$2.7 trillion` may match variable showing `$2.72T`
- Hardcoded `55 million` may match variable showing `55.0 million`
- Hardcoded `3,000 years` may match variable showing `2.88 thousand years`
- Hardcoded `0.4%` may match variable showing `0.342%` (text rounds up)

**Ask: "Is this number representing the same concept as the variable?"**

If unsure, search the compact lookup:
```bash
grep -i "keyword" _analysis/variable-lookup-compact.txt
```

### Phase 4: Apply Replacements

Use the Edit tool. For variables with text units (deaths, years, people), use `_nounit` variant when prose supplies its own unit word:

```
Old: 55 million annual deaths
New: {{< var global_annual_deaths_curable_diseases_nounit >}} annual deaths
```

Without `_nounit`, the rendered output would show "55.0 million deaths annual deaths" (doubled unit).

For variables with format-inherent units (USD `$`, `%`, ratios, multipliers), use the base variable directly:

```
Old: costs $89
New: costs {{< var bed_nets_cost_per_daly >}}
```

### Phase 5: Report

After completing, report changes and skips with reasoning.

## What to Skip

| Category | Example | Why |
|----------|---------|-----|
| YAML frontmatter | `title:`, `description:` | `{{< var >}}` doesn't render in YAML |
| Image alt text | `![280 million people...](img)` | Variables render as ugly HTML tooltips |
| LaTeX blocks | `$$ x = 42 $$` | Variables don't work inside `$...$` |
| Cited statistics | `$247 billion [@source]` | One-off facts tied to specific citations |
| Historical facts | `in 1948`, `200,000 people killed` | Fixed historical data, not model params |
| Jokes/illustrations | `line 4,582 of your DNA` | Rhetorical/comedic numbers |
| Fictional narrative | Moronia/Wishonia story numbers | World-building, not real-world data |
| "1% treaty" as name | `the 1% treaty` | Brand identity, not a parameterizable value |
| Treaty expansion tiers | `$5.44B`, `$13.6B` (5%, 10% tiers) | Tier-specific derived values with no individual variables |

## What to Replace

| Category | Example |
|----------|---------|
| Model parameters used in 2+ files | `$27.2B`, `3.5%`, `280 million` |
| Real-world stats matching variables | `55 million deaths`, `8 billion people` |
| Bond split percentages (80/10/10) | `80%` to trials, `10%` to investors |
| Trial/drug statistics | `~50 approvals`, `>20,000 drugs` |
| Cost comparisons | `$89` bed nets, `$500K` lobbyist salary |
| Numbers already used as variables elsewhere in the same file | Consistency within a file |

## Regenerating the Compact Lookup

If `_analysis/variable-lookup-compact.txt` is missing or stale:

```bash
python -c "
import sys, re, yaml
sys.stdout.reconfigure(encoding='utf-8')
with open('_variables.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
for key, val in sorted(data.items()):
    if key.endswith('_latex') or key.endswith('_cite') or key.endswith('_nounit'): continue
    s = str(val)
    m = re.search(r'>([^<]+)</(?:a|span)>', s)
    if m:
        display = m.group(1).strip()
        display = re.sub(r'\s*\(95% CI:.*', '', display).strip()
    else:
        display = re.sub(r'<[^>]*>', '', s).strip()
        display = re.sub(r'\s*\(95% CI:.*', '', display).strip()
    if not display: continue
    has_nounit = f'{key}_nounit' in data
    suffix = '  [has _nounit]' if has_nounit else ''
    print(f'{key}: {display}{suffix}')
" > _analysis/variable-lookup-compact.txt
```

## Related Tools

- `npm run generate:everything` - Regenerate `_variables.yml` from `parameters.py`
- `/validate-and-regenerate-parameters` - After adding new parameters
- `/qmd-consistency-check` - Full book validation
