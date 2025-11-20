# GitHub Actions Workflows

## Render Book PDF

**File:** `render-book-pdf.yml`

**Purpose:** Manually trigger a book PDF render and download the result.

**How to use:**

1. Go to the [Actions tab](../../actions/workflows/render-book-pdf.yml) in GitHub
2. Click "Run workflow" button
3. Select the branch you want to render from
4. Click the green "Run workflow" button
5. Wait for the workflow to complete (~10-20 minutes)
6. Download the PDF from the "Artifacts" section at the bottom of the workflow run page

**What it does:**

- Sets up Python 3.11 and all dependencies (uv, Graphviz, Jupyter kernel)
- Installs Quarto and TinyTeX (LaTeX)
- Runs `python scripts/render-book-pdf.py` to generate the PDF
- Uploads the PDF as a downloadable artifact named `war-on-disease-book-pdf`
- Artifact is kept for 30 days

**Output:**

- Artifact name: `war-on-disease-book-pdf`
- Contains: `*.pdf` files from `_book/warondisease/` directory

## Other Workflows

### `publish.yml`
Main publishing workflow for deploying to GitHub Pages.

### `build-pdf-only.yml`
Low-level PDF build for local testing with `act`.

### `claude-assistant.yml`
Claude Code automation workflow.
