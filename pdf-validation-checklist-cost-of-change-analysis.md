# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\cost-of-change-analysis.pdf`
**Quarto config:** `E:\code\obsidian\websites\disease-eradication-plan\_quarto-cost-of-change.yml`
**Generated:** 2026-02-09T16:15:43.869152

## Summary

- **Total issues:** 5
- **Critical:** 0
- **Warnings:** 5

## Progress Notes

- 2026-02-09: Reviewed all items. Marked fixed vs skipped (likely PDF text-extraction false positives).

---

## 🟡 LLM_EQUATION_RENDERING_DEFECT (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 4:** The variables 'p' are missing from within the parentheses in the equation defining when political change is rational. (Skipped: source equation is correct; likely text-layer extraction artifact.)
  - Context: `suggested_fix=Ensure the variable 'p' is rendered inside the parentheses for C(p) and B(p) to match the descriptive text below it. | evidence_snippet=Political Change is Rational if: C ( ) < B ( ) × P ( s | C ) | locator_hint=Equation in Section 1.2 Political Change as an Investment`

## 🟡 LLM_MALFORMED_BIBLIOGRAPHY_ENTRY (3 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 22:** Reference 10 has a malformed author name where 'Direct analysis' appears to have been incorrectly parsed and inverted. (Fixed in `references.bib` by converting to organization-style author.)
  - Context: `suggested_fix=Fix author name to 'ClinicalTrials.gov' or 'Direct Analysis' and remove the 'via, D.' inversion. | evidence_snippet=10. via, D. analysis. ClinicalTrials.gov cumulative enrollment data (2025). | locator_hint=Bibliography entry 10`
- [x] **Page 24:** The organization 'Think by Numbers' is incorrectly inverted as 'Numbers, T. by.' in the author field. (Fixed in `references.bib` with braced organization author.)
  - Context: `suggested_fix=Wrap organization names in double braces in BibTeX to prevent inversion. | evidence_snippet=20. Numbers, T. by. Pre-1962 drug development costs and timeline | locator_hint=Bibliography entry 20`
- [x] **Page 27:** Reference 36 contains URL-encoded characters (%3C, %3E) representing angle brackets inside the title/link text. (Fixed in `references.bib` by removing angle-bracket URL wrappers.)
  - Context: `suggested_fix=Remove the %3C and %3E encoding and use standard characters or a clean hyperlink. | evidence_snippet=War Costs $74 %3Chttps://thinkbynumbers.org/military/war/the-economic-case-for-peace-a-comprehensive-financial-analysis/%3E | locator_hint=Bibliography entry 36`

## 🟡 LLM_MISSING_TEXT/AUTHOR (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 6:** A sentence starts with a citation number (138) used as a subject, but the author's name (Olson) is missing. (Fixed in `knowledge/appendix/cost-of-change-analysis.qmd`.)
  - Context: `suggested_fix=Add the author's name: 'Olson (138) demonstrated that groups...' | evidence_snippet=responding to incentives. 138 demonstrated that groups with concentrated benefits | locator_hint=First paragraph of Section 2 Literature Review`
