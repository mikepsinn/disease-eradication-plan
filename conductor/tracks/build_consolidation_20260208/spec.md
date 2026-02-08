# Specification: Consolidate and Verify Build Scripts

## Goal
To ensure the reliability and efficiency of the document generation pipeline for the "Disease Eradication Plan" project. This involves verifying all primary Quarto render paths and confirming that validation scripts provide comprehensive coverage across the book and all academic papers.

## Scope
- **Primary Documents:** Manual, 1% Treaty Impact Paper, Federal Efficiency Audit, Wishocracy, Optimocracy.
- **Validation Suite:** `validate:all`, `lint:md`, `lint:qmd`, and LaTeX validation scripts.
- **Automation:** Ensuring `npm run generate:everything` correctly prepares all parameters and variables before rendering.

## Acceptance Criteria
- All primary documents render to PDF and HTML without errors.
- `npm run validate:all` passes for the entire repository.
- A single "smoke test" command is identified or created to verify the entire build chain.
