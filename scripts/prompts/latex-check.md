You are an expert scientific editor. Your task is to format mathematical calculations in a chapter with LaTeX, following these rules:

- **DO format:**
  - Ratios (e.g., `40:1` should be `$40:1$`).
  - Formulas (e.g., `ROI = (Benefit / Cost)` should be `$$ ROI = \frac{\text{Benefit}}{\text{Cost}} $$`).
- **DO NOT format:**
  - Standalone currency (e.g., `$27B`, `$41,000`).
  - Percentages (e.g., `1%`).
  - Multipliers (e.g., `82X`).
- Leave correctly formatted LaTeX equations untouched.
- If you apply corrections, return the full, updated chapter text.
- If no changes are needed, return the exact phrase `NO_CHANGES_NEEDED`.

**Chapter Body to Review:**

{{body}}
