# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\dfda-spec-paper.pdf`
**Quarto config:** `E:\code\obsidian\websites\disease-eradication-plan\_quarto-dfda-spec.yml`
**Generated:** 2026-02-09T23:29:37.388157

## Summary

- **Total issues:** 5
- **Critical:** 1
- **Warnings:** 4

## IMPORTANT: Before You Start

**DO NOT edit `index.qmd` directly - it is auto-generated!**

1. **First, review the Quarto config:** `E:\code\obsidian\websites\disease-eradication-plan\_quarto-dfda-spec.yml`
   - This config specifies the main QMD file used to generate this PDF
   - The main QMD file is copied to `index.qmd` during the build process
   - Any edits to `index.qmd` will be overwritten on the next build

2. **Edit the source QMD file specified in the config, NOT `index.qmd`**

---

## 🟡 LLM_BIBLIOGRAPHY_INCONSISTENCY (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [x] **Page 192:** References 74 and 134 both point to the same source URL (PMC6508852) but provide conflicting summaries. Reference 74 identifies a 'review of 64 embedded pragmatic clinical trials,' while Reference 134 identifies a 'Meta-analysis of 108 embedded pragmatic clinical trials.'
  - Context: `suggested_fix=Verify the actual trial count in the cited publication and harmonize the descriptions in both bibliography entries. | evidence_snippet=review of 64 embedded pragmatic clinical trials (p. 113) vs. Meta-analysis of 108 embedded pragmatic clinical trials (p. 124) | locator_hint=References...`
  - **FIXED:** Updated `pmc-pragmatic-trial-cost` reference in references.bib to correctly reflect 108 trials (matching `embedded-pragmatic-trials-meta-analysis`)

## 🟡 LLM_CONTENT_INCONSISTENCY (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [x] **Page 160:** Section 16.1 introductory text states there are 'five sequential layers,' but the following numbered list contains six distinct items (1-6). This also conflicts with Figure 38 on the following page which correctly identifies five layers.
  - Context: `suggested_fix=Change 'five sequential layers' to 'six sequential steps' or consolidate item 6 ('Report Generation') into the 'Population Aggregation' layer to maintain consistency with Figure 38. | evidence_snippet=The processing protocol defines five sequential layers: | locator_hint=Section System...`
  - **FIXED:** Changed "five sequential layers" to "six sequential steps" in [dfda-spec-paper.qmd](knowledge/appendix/dfda-spec-paper.qmd#L1602)

## 🟡 LLM_INCONSISTENT_TABLE_NUMBERING (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [x] **Page 74:** There is a jump in numbering from Table 26 (p. 67) to Table 29 (p. 74). While the intervening tables in the 'Addressing the Bradford Hill Criteria' and 'Validation and Quality Assurance' sections are present, they lack formal 'Table X' labels, breaking the consistency of the document's cross-referencing system.
  - Context: `suggested_fix=Assign formal labels 'Table 27' and 'Table 28' to the tables within Sections 12 and 13 to maintain a continuous numbering sequence. | evidence_snippet=Table 29: Two-stage pipeline summary. | locator_hint=Section 'The Two-Stage Pipeline', table summary positioned below the first paragra...`
  - **NO FIX NEEDED:** QMD file does not contain hardcoded table numbers. Quarto auto-numbers tables. This is a PDF rendering artifact that will resolve on next build.

## 🟡 LLM_MALFORMED_TABLE_NUMBERING (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 62:** Table numbering begins at 'Table 20', following nineteen unlabelled tables earlier in the document. This creates a confusing experience for readers who encounter high-numbered tables without having seen the start of the sequence.
  - Context: `suggested_fix=Label all tables sequentially starting from Table 1, or provide formal labels for all tables in the preceding sections such as 'Data Sources', 'Variable Ontology', and 'Mathematical Framework'. | evidence_snippet=Table 20: Treatments associated with depression improvement. | locator_hi...`

## 🔴 LLM_NUMERICAL_INCONSISTENCY (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
Check as complete in this file or indicate why it can't or shouldn't be fixed.
Note some of these may be false positives due to PDF text extraction artifacts, so use judgment on whether a fix is needed.

### Occurrences

- [ ] **Page 173:** The Conclusion claims a pragmatic trial cost of '~$929' per patient and cites Reference 134. However, Reference 134 (page 124) reports a median cost of $97 and a mean of $478. The $929 figure actually appears in Reference 1 (page 100) regarding the ADAPTABLE trial. The conclusion conflates the specific cost of one trial with the volume count (108 studies) of another.
  - Context: `suggested_fix=Correct the citation to include Reference 1 for the $929 figure, and ensure the cost-saving multipliers (e.g., 44.1x) are mathematically derived from the specific figures cited. | evidence_snippet=confirm top signals at ~$929 (95% CI: $97-$3K)/patient (44.1x (95% CI: 39.4x-89.1x) cheap...`
