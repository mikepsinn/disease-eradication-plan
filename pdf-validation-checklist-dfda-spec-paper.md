# PDF Validation Errors - Checklist

**PDF:** `E:\code\obsidian\websites\disease-eradication-plan\assets\pdfs\dfda-spec-paper.pdf`
**Quarto config:** `E:\code\obsidian\websites\disease-eradication-plan\_quarto-dfda-spec.yml`
**Generated:** 2026-02-09T16:26:39.464715

## Summary

- **Total issues:** 1
- **Critical:** 1
- **Warnings:** 0

---

## 🔴 LLM_EQUATION_RENDERING_DEFECT (1 issue(s))

### How to Fix
**Fix:** Review the error context and check the corresponding QMD source file.
If the error persists, check Quarto documentation or run with `--verbose` flag.

### Occurrences

- [ ] **Page 24:** In the caption for Figure 13, the parentheses intended to contain the mathematical symbols for onset delay (δ) and duration of action (τ) are empty, leaving only spaces like '( )'.
  - Context: `suggested_fix=Update the figure caption to ensure the symbols δ and τ are correctly rendered within the parentheses. | evidence_snippet=defined by onset delay ( ) and duration of action ( ). | locator_hint=Found in the caption for Figure 13, titled 'Temporal alignment diagram...'`
