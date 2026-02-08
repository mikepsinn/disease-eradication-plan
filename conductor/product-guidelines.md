# Product Guidelines - Disease Eradication Plan

## 1. Prose Style & Voice
The project employs a dual-voice strategy to reach different audiences while maintaining a shared core of factual integrity.

### 1.1 The "WISHONIA" Voice (The Manual)
- **Characteristics:** Bold, provocative, slightly cynical, and high-impact. It uses direct address and dark humor to highlight the absurdity of current resource allocation.
- **Key Metaphors:** "Meat robots" (humans), "Murder budget" (military spending), "Purchasing umbrellas while the house is on fire."
- **Goal:** To strip away political euphemisms and provoke a visceral realization of the opportunity cost of disease.

### 1.2 Academic Precision (Working Papers)
- **Characteristics:** Objective, formal, and rigorously structured. It follows the conventions of economic and health policy research.
- **Standards:** Prioritize clarity, statistical significance, and clear methodology.
- **Goal:** To provide "bulletproof" evidence that survives scrutiny from policy experts, economists, and skeptics.

### 1.3 Shared Core: Evidence-Based Persuasion
- **Constraint:** Regardless of the voice, every claim must be rooted in the project's data (citations, parameters, and calculations).
- **Citations:** Use Quarto's citation system (`[@citation]`) linked to `references.bib`.
- **Transparency:** All calculations should be traceable back to the `parameters-and-calculations` appendices.

## 2. Branding & Visual Identity
### 2.1 Color Palette
- **Primary:** High-contrast Black and White.
- **Rationale:** This creates a stark, serious, and "archival" aesthetic that works across both satirical and academic contexts. It emphasizes the "engineering" nature of the problem without distracting colored fluff.

### 2.2 Symbols & Imagery
- **The Skull & Prohibition Sign:** Used as a favicon/icon for the manual to represent the "War on Disease."
- **Data Visualizations:** High-quality, clean charts that focus on scale comparisons. Charts should be designed for maximum clarity in monochrome/grayscale.

## 3. Organizational Principles
- **Modularity:** Maintain the ability to render the same content in different formats (PDF, Web, EPUB) using Quarto.
- **Open Source:** All data and code used in the analysis must be publicly available and verifiable.

## 4. Parameter Standards
**CRITICAL:** Use the automated parameter/variable system for all numeric values. Never hardcode values that might change or need citations.

### 4.1 Naming Convention
Names must be self-documenting: `[SCOPE]_[METRIC]_[MODIFIERS]_[UNIT_TYPE]`

- **Scope:** `DFDA`, `TREATY`, `GLOBAL`, `PERSONAL`, `VICTORY_BOND`
- **Metric:** `ROI`, `COST`, `BENEFIT`, `DEATHS`, `DALYS`
- **Examples:** `TREATY_COMPLETE_ROI_EXPECTED_95TH_PERCENTILE`, `DFDA_ROI_RD_ONLY`

### 4.2 Unit Guidelines
Units must read naturally in prose.
- **Currency:** `unit="USD"` -> "$519M"
- **Percentages:** `unit="percent"` -> "51%"
- **Ratios:** `unit="ratio"` -> "1.5x"
- **Time:** `unit="years"` -> "10 years"
- **People:** `unit="people"`, `unit="members"`, `unit="senators"`

### 4.3 Calculated Parameters
Parameters derived from others **must** use the `compute` attribute (lambda function) and list their `inputs` explicitly. This enables automated Monte Carlo uncertainty propagation.
```python
PEACE_DIVIDEND_ANNUAL = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT,
    source_type="calculated", 
    unit="USD",
    inputs=["GLOBAL_ANNUAL_WAR_TOTAL_COST", "TREATY_REDUCTION_PCT"],
    compute=lambda ctx: ctx["GLOBAL_ANNUAL_WAR_TOTAL_COST"] * ctx["TREATY_REDUCTION_PCT"]
)
```

## 5. LaTeX & Math
- **No Variables in `$$` blocks:** Quarto variables `{{< var ... >}}` do NOT render inside display math blocks.
- **Use `_latex` Variables:** For any equation, use the auto-generated LaTeX variable: `{{< var param_name_latex >}}`.
- **Symbols:** Define `latex_symbol` in the `Parameter` class to ensure consistent symbols across auto-generated derivations.

## 6. Content Standards
- **Cross-Format Linking:** Always use `.qmd` extensions for internal links (e.g., `[Link](../path/to/file.qmd)`). Quarto handles the conversion to HTML/PDF.
- **Em-Dashes:** Do not use em-dashes (—). Replace with parenthesis, comma and space (", "), period, or semicolon.
- **Citations:** Never add citations without verification. `references.bib` is the single source of truth.
- **Python Scripts:** All Python scripts must include the UTF-8 encoding header for Windows compatibility.