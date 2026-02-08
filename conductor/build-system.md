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

- **Configs:** `manual`, `1-pct-treaty-impact`, `federal-efficiency-audit`, `wishocracy`, `iab`, `book`, `test`.
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

### 5. CI/CD Workflow Generator
**Script:** `scripts/lib/workflow_generator.py`

Automates GitHub Actions configuration.

- **Function:** Scans all `_quarto-*.yml` files and auto-generates `.github/workflows/publish.yml`.
- **Benefit:** Adding a new paper/site only requires creating a `_quarto-new-paper.yml` file; the CI pipeline is updated automatically.

## Validation Strategy

The project uses a "defense in depth" validation strategy:

1.  **Static Analysis (`pre-render`):** Fast checks on source files.
2.  **Build Monitor (`render-quarto`):** Real-time monitoring of the Quarto process (timeout detection, log parsing).
3.  **Output Verification (`post-render`):** Inspection of final artifacts.
