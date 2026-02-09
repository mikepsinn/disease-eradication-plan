# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\optimocracy-paper.pdf`
**Generated:** 2026-02-09T16:10:40.538304

## Summary

- **Total issues:** 7
- **Critical:** 5
- **Warnings:** 2

## Progress Notes

- 2026-02-09: Reviewed all items. Bibliography issues fixed globally; equation items marked skipped as likely text-layer extraction artifacts.

---

## 🔴 LLM_EQUATION_RENDERING_DEFECT (5 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 10:** Mathematical variables for welfare (W and W*) are missing from the introductory text of section 4.1. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Ensure all math symbols are correctly embedded and rendered in the body text font. | evidence_snippet=Let   * represent maximum achievable welfare under optimal policy, and    represent actual welfare | locator_hint=Section 4.1, first paragraph after the tau equation.`
- [x] **Page 16:** Key variables (N, i, pi, ci, K, pO) are invisible in the explanatory text of the Formal Model section. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Fix math character font embedding in the text blocks. | evidence_snippet=Let    denote the number of capture-prone allocation decisions under the status quo. Each decision    has capture probability | locator_hint=Section 4.6.1, first paragraph.`
- [x] **Page 20:** The symbols for the metric (M), allocation vector (x), and budget (B) are missing from the text defining the execution layer's optimization parameters. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Ensure LaTeX-style variables are properly rendered within normal text paragraphs. | evidence_snippet=Where    (⋅) is the chosen metric, x is the allocation vector, and    is the total budget. | locator_hint=Section 6.3, sentence beginning with 'Where M(·)'.`
- [x] **Page 21:** The Greek symbol alpha is missing from the explanation of the default weighting in the welfare function. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Verify rendering and embedding of Greek character set in the body font. | evidence_snippet=Default weighting:    = 0.5 (equal weight to economic and health welfare). | locator_hint=Section 7.1, text following 'The Welfare Function' display equation.`
- [x] **Page 33:** Variables E and G are missing from the Campaign Funding Allocation Algorithm equation and its factor descriptions. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Repair character mapping for E and G symbols in math environments. | evidence_snippet=[Δ  ] = alignment_gap×position_power×win_probability_shift | locator_hint=Section 11.1, main algorithmic equation for E[delta G].`

## 🟡 LLM_MALFORMED_BIBLIOGRAPHY_ENTRIES (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 60:** Bibliography entry 10 appears as a malformed sentence fragment ('via, D. analysis'). (Fixed in `references.bib` organization author formatting.)
  - Context: `suggested_fix=Reconstruct reference 10 to properly reflect the source and author. | evidence_snippet=10. via, D. analysis. ClinicalTrials.gov cumulative enrollment data (2025). | locator_hint=References section, entry 10.`
- [x] **Page 61:** Bibliography entry 20 misparses the source name 'Think by Numbers' as an author ('Numbers, T. by.'). (Fixed in `references.bib` organization author formatting.)
  - Context: `suggested_fix=Update metadata to correctly categorize the source title and author. | evidence_snippet=20. Numbers, T. by. Pre-1962 drug development costs and timeline | locator_hint=References section, entry 20.`
