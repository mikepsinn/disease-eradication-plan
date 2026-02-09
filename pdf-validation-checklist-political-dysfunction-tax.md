# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\political-dysfunction-tax.pdf`
**Generated:** 2026-02-09T16:12:19.934449

## Summary

- **Total issues:** 9
- **Critical:** 4
- **Warnings:** 5

## Progress Notes

- 2026-02-09: Reviewed all items. Marked as skipped where evidence points to PDF extraction/OCR artifacts rather than source defects.

---

## 🔴 LLM_EQUATION_RENDERING_DEFECT (6 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 1:** The variable symbol for Political Dysfunction Tax (Tpd) is missing, leaving an empty set of parentheses in the abstract. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Ensure LaTeX math fonts are correctly embedded in the PDF export. | evidence_snippet=Political Dysfunction Tax (      ): | locator_hint=Abstract, first sentence`
- [x] **Page 1:** The variable symbol for the Efficiency Score (E) is missing in the Table of Contents for Part 3 and Section 4. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Verify that variable symbols render correctly in the ToC generation process. | evidence_snippet=4 Part 3: The Calculation (  ) 34 | locator_hint=Table of Contents, Section 4`
- [x] **Page 5:** The variable symbol Tpd is again missing in the body text introducing the Shadow Budget. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Re-render math symbols for consistency across the document. | evidence_snippet=Political Dysfunction Tax (      ). | locator_hint=First paragraph after Figure 2`
- [x] **Page 6:** Missing variable 'E' in the definition of Global Governance Efficiency Score. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Embed math symbols correctly in text blocks. | evidence_snippet=Global Governance Efficiency Score (  ). | locator_hint=Paragraph immediately preceding Section 2`
- [x] **Page 34:** Major rendering failure in Section 4.1 where variables W_real and W_max are blank in list headers and formulas. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Ensure all subscripted variables render properly in the calculation sections. | evidence_snippet=1. Current Realized Welfare (          ) | locator_hint=Section 4.1, list items 1 and 2`
- [x] **Page 35:** Missing variable W_max in the sensitivity analysis bullet point. (Skipped: likely text-layer extraction artifact.)
  - Context: `suggested_fix=Check math rendering in bulleted lists. | evidence_snippet=• High-End         : | locator_hint=Sensitivity Analysis section, third bullet point`

## 🟡 LLM_MALFORMED_BIBLIOGRAPHY_ENTRIES (2 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 41:** Broken URL in citation 20: an unintended space exists within the URL string ('% 20'), which will cause link failure. (Skipped: likely line-wrap extraction artifact in PDF text layer.)
  - Context: `suggested_fix=Remove the space between '%' and '20' in the URL. | evidence_snippet=Reform_Sept% 2024.pdf | locator_hint=Works cited, entry 20`
- [x] **Page 55:** Citation 66 contains a Unicode replacement character (), indicating a failed character mapping for a math symbol (likely '=' or '≈'). (Skipped: extraction artifact; source contains valid symbols.)
  - Context: `suggested_fix=Replace the replacement character with the intended mathematical symbol. | evidence_snippet=($41,000 ÷ $500  82×) | locator_hint=Works cited, entry 66`

## 🟡 LLM_UNREADABLE_FIGURES/TABLES (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [x] **Page 5:** Poor page break placement; a sentence ends abruptly with 'denoted as', with the following term 'Optimocracy' appearing on page 6. (Skipped: layout preference, not a correctness defect.)
  - Context: `suggested_fix=Adjust page geometry or add a page break hint to keep the definition on one page. | evidence_snippet=theoretical maximum denoted as | locator_hint=Last line of page 5`
