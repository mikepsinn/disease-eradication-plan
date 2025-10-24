As a scientific editor, format mathematical calculations in the chapter with LaTeX.

**Rules:**
1.  **Format:** Ratios (e.g., `40:1` should be `$40:1$`) and formulas (e.g., `ROI = (Benefit / Cost)` should be `$$ ROI = \frac{\text{Benefit}}{\text{Cost}} $$`).
2.  **Ignore:** Standalone currency (`$27B`), percentages (`1%`), and multipliers (`82X`).
3.  Leave existing LaTeX untouched.
4.  Return the full, updated text if you make changes.
5.  Return `NO_CHANGES_NEEDED` if no changes are made.

**Chapter Body:**

{{body}}
