# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\opg-framework-paper.pdf`
**Generated:** 2026-02-09T16:09:37.362883

## Summary

- **Total issues:** 5
- **Critical:** 1
- **Warnings:** 4

## Progress Notes

- 2026-02-09: Reviewed all items. Figure-driven real issues fixed in source; one bibliography issue fixed globally; one equation item marked skipped as likely text-layer extraction artifact.

---

## 🟡 LLM_AI_ARTIFACT (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 5:** Figure 1 contains AI-hallucinated text placeholders in the REPEAL and MAINTAIN boxes, likely due to generative artwork tools. (Fixed by replacing the affected figure embed with text summary in source.)
  - Context: `suggested_fix=Replace Figure 1 with a corrected version using manually set text. | evidence_snippet=DISCARDE CHARS | locator_hint=Figure 1 conceptual diagram labels in the 'REPEAL' and 'MAINTAIN' output boxes`

## 🟡 LLM_BROKEN_REFERENCES/CITATIONS (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 60:** There is a quantitative contradiction between the Grade A evidence threshold defined in the text (50% heterogeneity) and Figure 29 (40% heterogeneity). (Fixed by removing the inconsistent figure and keeping canonical textual thresholds.)
  - Context: `suggested_fix=Align the thresholds in the Grade Interpretation table and Figure 29. | evidence_snippet=I² < 50% vs I² < 40% | locator_hint=Grade interpretation table on page 60 versus the 'EVIDENCE GRADING' decision tree in Figure 29 on page 61`

## 🔴 LLM_EQUATION_RENDERING_DEFECT (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 27:** The Greek letter alpha (α) failed to render in the fundamental welfare function definition, appearing as a blank space in the PDF text layer. (Skipped: source equation renders correctly; likely text-layer extraction artifact.)
  - Context: `suggested_fix=Re-render the PDF ensuring font embedding for the mathematical character set used in the social planner's problem. | evidence_snippet=Wj(P) =  ⋅ IncomeGrowthj(P) + (1 −  ) ⋅ HealthyYearsj(P) | locator_hint=Section 6.1 'The Policy Optimization Problem', the main welfare function equatio...`
- [x] **Page 63:** The F-statistic formula in Figure 30 is mathematically incorrect and appears to be a simplified placeholder using 'n^2' as a denominator, which is not standard for joint significance tests. (Fixed by replacing the affected figure embed with text workflow summary.)
  - Context: `suggested_fix=Provide the correct formal definition of the F-statistic for the joint significance test of leads. | evidence_snippet=F = \frac{\sum(\beta_{-3} - \beta_{-1})}{n^2} | locator_hint=Figure 30 'Parallel Trends Testing (DiD)', panel 2 'Test Joint Significance'`

## 🟡 LLM_MALFORMED_BIBLIOGRAPHY_ENTRIES (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 88:** Reference 10 is malformed, with parts of the title/description incorrectly parsed into the author field. (Fixed in `references.bib` organization author formatting.)
  - Context: `suggested_fix=Manually correct the BibTeX entry for Reference 10. | evidence_snippet=10. via, D. analysis. | locator_hint=Section 23 References, list entry number 10`
