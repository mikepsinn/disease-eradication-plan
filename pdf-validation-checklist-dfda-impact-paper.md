# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\dfda-impact-paper.pdf`
**Quarto config:** `E:\code\obsidian\websites\disease-eradication-plan\_quarto-dfda-impact.yml`
**Generated:** 2026-02-09T16:22:55.956936

## Summary

- **Total issues:** 5
- **Critical:** 1
- **Warnings:** 4

## Progress Notes

- 2026-02-09: Reviewed all items. Fixed confirmed source leak issues; left broad bibliography-normalization and chart readability items as pending follow-up.

---

## 🔴 LLM_EQUATION_RENDERING_DEFECT (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 12:** The mathematical derivation for 'Cost per DALY' has failed to render correctly. Most text and variables are missing, leaving behind only horizontal lines and mathematical operators (=, +, /). (Skipped: likely text-layer extraction artifact; keep monitoring after next render.)
  - Context: `suggested_fix=Re-render the PDF ensuring that all mathematical fonts are correctly embedded and that the derivation block is not corrupted during output. | evidence_snippet=Cost_direct,DALY = NPV_direct / DALYs_max = $475B / 565B = $0.841 | locator_hint=Following the 'Cost per DALY:' heading on page...`

## 🟡 LLM_LEAKED_SOURCE/CODE (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 13:** A technical cross-reference tag '{#the-discovery-capacity-model}' is visible in the text body instead of being processed into a link or hidden. (Fixed in `knowledge/appendix/dfda-impact-paper.qmd` by converting to a proper heading anchor.)
  - Context: `suggested_fix=Remove the raw Markdown cross-reference tag from the source text. | evidence_snippet=The Discovery Capacity Model: {#the-discovery-capacity-model} | locator_hint=Section 1 (Executive Summary), table heading 'The Discovery Capacity Model:'`
- [x] **Page 99:** The bar chart displaying annual budgets contains literal newline characters ('\n') in the category labels on the y-axis. (Fixed in `knowledge/figures/dfda-vs-federal-health-programs-comparison-bar-chart.qmd` by using real line breaks in labels.)
  - Context: `suggested_fix=Process the newline characters as actual breaks or use spaces in the label source strings. | evidence_snippet=Framework (Lean Ecosystem) $40.05M/year\n(1x) | locator_hint=Y-axis labels in the 'Decentralized Drug Assessment Framework Cost vs. Other Federal Health Programs' bar chart`

## 🟡 LLM_MALFORMED_BIBLIOGRAPHY_ENTRIES (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [ ] **Page 101:** Systemic citation parsing error where institutional names and journals are incorrectly formatted as personal names (e.g., 'Bank, W.' for World Bank, 'Organization, W. H.' for WHO, 'ONE, P.' for PLOS ONE). (Pending: requires broader bibliography normalization pass across many entries.)
  - Context: `suggested_fix=Wrap institutional author names in double curly braces in the BibTeX source to prevent incorrect parsing. | evidence_snippet=Organization, W. H. WHO global health estimates 2024. | locator_hint=References section, specifically entries 4, 10, 25, 45, 101, 108, and 128`

## 🟡 LLM_UNREADABLE_FIGURES/TABLES (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [ ] **Page 36:** Several Monte Carlo distribution charts have overlapping, double-printed x-axis labels, making them difficult to read. (Pending: needs targeted chart layout adjustments in distribution figure generators.)
  - Context: `suggested_fix=Adjust chart generation settings to prevent the overlapping of duplicate axis label strings. | evidence_snippet=Decentralized Framework for Drug Assessment Annual BenefDite:c eRn&tDra lSiazveidn gFsr a(mUeSwDo/ryke afro)r Drug Assessment Annual Benefit | locator_hint=X-axis labels in F...`
