---
max_iterations: 50
completion_promise: ALL_ERRORS_FIXED
description: Fix all pre-render validation errors
---

# Fix Validation Errors

Run pre-render validation and fix all detected errors systematically.

## Process

1. **Run validation**:
   ```bash
   python scripts/pre-render-validation.py
   ```

2. **Parse errors** from output:
   - INVALID_VAR: Variable not found in _variables.yml
   - LATEX_VAR: Variable inside LaTeX block (won't render)
   - HTML_LINK: Link uses .html instead of .qmd
   - MISSING_CITATION: Citation key not in references.qmd

3. **Fix each error**:
   - For INVALID_VAR: Check spelling or add to parameters.py
   - For LATEX_VAR: Use _latex variable or leave hardcoded
   - For HTML_LINK: Change to .qmd extension
   - For MISSING_CITATION: Add citation to references.qmd

4. **Re-run validation** to verify fixes

5. **Repeat** until no errors remain

## Completion

Output `<promise>ALL_ERRORS_FIXED</promise>` when validation runs with zero errors.
