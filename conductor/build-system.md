# Build System & Scripts

The project relies on a sophisticated set of Python scripts to manage the data-driven publishing pipeline. These scripts handle everything from parameter generation to cross-site link rewriting and validation.

## Core Scripts

### 1. Data & Parameter Generation
**Script:** `scripts/generate-everything-parameters-variables-calculations-references.py`
**Npm Command:** `npm run generate:everything`

This is the **engine** of the project. It ensures academic rigor by generating all downstream artifacts from a single source of truth.

- **Inputs:**
  - `dih_models/parameters.py` (Numeric constants & metadata)
  - `references.bib` (Single source of truth for citations)
- **Outputs:**
  - `_variables.yml`: Quarto variables with tooltips and confidence intervals.
  - `knowledge/appendix/parameters-and-calculations.qmd`: generated academic appendix.
  - `dih_models/reference_ids.py`: Python enum for type-safe citation keys.
  - `_analysis/`: Monte Carlo simulation results (`samples.json`) and sensitivity analyses.
  - `knowledge/figures/`: Generated charts (Tornado, Sensitivity, Distributions).

**Key Features:**
- Runs Monte Carlo simulations (n=10,000) to calculate confidence intervals.
- Validates that all parameters have proper sources and citations.
- Generates TypeScript definitions for the frontend apps.

### 2. Unified Renderer
**Script:** `scripts/render-quarto.py`
**Usage:** `python scripts/render-quarto.py [config_name] [options]`

A wrapper around Quarto that handles the complex multi-site architecture.

- **Configs:** `manual`, `1-pct-treaty-impact`, `us-efficiency-audit`, `wishocracy`, `iab`, `book`, `test`.
- **Key Features:**
  - **Cross-Site Link Rewriting:** Automatically converts relative links (e.g., `[Link](other-paper.qmd)`) into absolute HTTPS URLs when pointing to a different site/subdomain.
  - **Temp Build Directory:** Copies project to `_build_temp/{config}/` to isolate builds and prevent cache pollution.
  - **PDF Validation:** Checks generated PDFs for leaked Python code or frontmatter.
  - **Zenodo Integration:** Can upload final PDFs to Zenodo drafts.

### 3. Pre-Render Validation
**Script:** `scripts/pre-render-validation.py`
**Npm Command:** `npm run validate:pre-render`

Runs *before* Quarto starts to catch errors that would break the build or compromise quality.

- **Checks:**
  - **LaTeX Safety:** Detects syntax that breaks LaTeX/PDF compilation (e.g., unescaped `$`, unbalanced braces).
  - **Broken Links:** Validates all `[text](path)` links, including cross-references and anchors.
  - **Missing Images:** Ensures referenced images exist.
  - **Parameter Imports:** Verifies Python blocks import the parameters they use.
  - **Citations:** Ensures `[@citation]` keys exist in `references.bib`.

### 4. Post-Render Validation
**Script:** `scripts/post-render-validation.py`
**Npm Command:** `npm run validate:post-render`

Scans the generated HTML output to catch issues that Quarto missed.

- **Checks:**
  - **Unrendered Code:** Detects `{python}` or `{{< var >}}` literals in output (indicating render failure).
  - **Broken Internal Links:** Validates `href` and `src` attributes in the final HTML.
  - **Metadata Mismatches:** Ensures `description` and `og:description` tags match.
  - **Bibliography:** Verifies that citations include abstracts/notes (if using annotated CSL).

## Data Model: The Parameter Class

Located in `dih_models/parameters.py`, the `Parameter` class (inheriting from `float`) is the atomic unit of the project.

### Attributes
- `source_type`: `EXTERNAL`, `CALCULATED`, or `DEFINITION`.
- `distribution`: Probability distribution for Monte Carlo (e.g., `NORMAL`, `LOGNORMAL`, `BETA`, `GAMMA`).
- `inputs`: List of other parameter names used as inputs (for calculated params).
- `compute`: A lambda function `lambda ctx: ...` for calculating values and propagating uncertainty.
- `latex_symbol`: The LaTeX representation for use in auto-generated equations.

### Monte Carlo Propagation
The build system doesn't just calculate baseline values. It uses the `inputs` and `compute` metadata to run 10,000 simulations, propagating the uncertainty (defined by `distribution` and `std_error`) from raw inputs to final results. These results are then embedded back into the book as 95% confidence intervals.

## LaTeX Variable Generation

Quarto variables (e.g., `{{< var ... >}}`) **do not work inside LaTeX `$$` blocks**. 

To solve this, `variables_yml_generator.py` automatically exports a corresponding `_latex` variable for every parameter.
- **Variable:** `{{< var peace_dividend >}}` -> Renders as "$114B" with tooltip.
- **LaTeX Variable:** `{{< var peace_dividend_latex >}}` -> Renders a full `$$` block with the equation and derivation.
- **Derivation Tracking:** The generator uses recursive "expanded" LaTeX to show the full derivation chain for any calculated value, ensuring maximum transparency for peer review.

## Autonomous Perfection + Upload

### Primary Scripts
- `scripts/upload-all-zenodo-and-save-dois.py`
- `scripts/autonomous-perfect-and-upload.py`
- `scripts/autonomous-perfect-and-upload.ps1`

### Behavior
- Uses source and PDF signatures to skip papers already perfected and uploaded.
- Runs required PDF validation with LLM checks before upload.
- Uses local validation cache at `.cache/pdf-validation-upload-cache.json`.
- Uses perfected-state cache at `.cache/zenodo-perfect-upload-state.json`.
- Fails fast on the first paper with blocking validation/upload errors.
- Does not continue to later papers until the first failure is fixed.

### LLM Validation Gating
- Upload gating is controlled by explicit issue types, not mode presets.
- Default blocking set:
  - `LLM_UNRENDERED_CODE_OR_VARIABLE`
  - `LLM_PLACEHOLDER_TEXT`
  - `LLM_LEAKED_SOURCE_CODE`
  - `LLM_CORRUPTED_OR_GARBLED_TEXT`
  - `LLM_TRUNCATED_SENTENCE`
  - `LLM_BROKEN_REFERENCE_ENTRY`
  - `LLM_BROKEN_REFERENCE_LINK`
  - `LLM_OTHER_HIGH_CONFIDENCE`
- Override with:
  - `--llm-blocking-types "TYPE_A,TYPE_B,..."`
  - `--llm-warning-types "TYPE_X,TYPE_Y,..."`

### Visibility and Logs
- Upload report: `zenodo-upload-report.md` (summary, errors, warnings, action log, checklist).
- Autonomous run logs: `AUTONOMOUS-PIPELINE-LOGS/`.
- Persistent root status log: `AUTONOMOUS-PIPELINE-STATUS.md` (append-only run history).
- Persistent root live output log: `AUTONOMOUS-PIPELINE-PROGRESS.log` (streamed command output).

### No-Commit Safety
- Autonomous runner enforces no-commit behavior through:
  - explicit Codex prompt constraints (`DO NOT commit/push/branch`)
  - git HEAD guard before/after each fixer cycle.
