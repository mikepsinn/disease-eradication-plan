As a scientific editor, your task is to format mathematical equations in the provided chapter text using LaTeX.

**Rules:**

1.  **Scope:** Only format mathematical calculations and formulas.
    *   **INCLUDE:** Equations representing calculations, like `ROI = (Benefit / Cost)`.
    *   **EXCLUDE:** Simple numerical mentions, ratios (`40:1`), currency (`$27B`), percentages (`1%`), or multipliers (`82X`).

2.  **Placement:**
    *   Only format equations that appear on their own line.
    *   **DO NOT** format equations that are embedded within a sentence.

3.  **Information Preservation:**
    *   **CRITICAL: DO NOT** remove explanatory text when creating an equation. The goal is to format the math, not delete the description.
    *   For example, if the text is `- Add 10% VICTORY bonds: Portfolio returns jump to 33%+ (90% at 7% + 10% at 270% = 33.3% blended return)`, do not change it. Replacing the parenthetical explanation with only a LaTeX formula loses valuable context like "blended return". If formatting an equation would make the content less informative, do not format it.

4.  **Formatting:**
    *   Use block-level LaTeX (`$$...$$`) for all formatted equations.
    *   For long equations, use the `aligned` environment to ensure they are readable on mobile devices by breaking them into multiple lines.

5.  **Existing LaTeX:** Do not modify or reformat any text that is already in LaTeX format.

6.  **Output:**
    *   If you make any changes, return the complete, updated text of the chapter.
    *   If no changes are needed, return the exact string `NO_CHANGES_NEEDED`.

**Chapter Body:**

{{body}}
