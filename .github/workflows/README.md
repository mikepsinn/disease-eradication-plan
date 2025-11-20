# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Decentralized Institutes of Health book project.

## Available Workflows

### 📚 Build and Download PDF Book

**File:** `build-pdf-only.yml`

**Purpose:** Manually render the complete book as a PDF and make it available for download.

**How to use:**

1. Go to the [Actions tab](https://github.com/mikepsinn/decentralized-institutes-of-health/actions)
2. Select "Build and Download PDF Book" from the workflows list on the left
3. Click the "Run workflow" button on the right
4. Select the branch you want to build from (usually `main`)
5. Click "Run workflow"

**Downloading the PDF:**

After the workflow completes successfully:

1. Click on the completed workflow run
2. Scroll down to the "Artifacts" section at the bottom
3. Download the `book-pdf` artifact (it will be a ZIP file)
4. Extract the ZIP to get the PDF file

**Notes:**

- The workflow takes approximately 15-20 minutes to complete
- PDF artifacts are retained for 30 days
- The workflow will fail if the PDF cannot be generated (errors in source files, missing dependencies, etc.)

### 🌐 Lint, Build, and Deploy Quarto site to Pages

**File:** `publish.yml`

**Purpose:** Automatically build and deploy the HTML version of the book to GitHub Pages when changes are pushed to the main branch.

**Trigger:** Automatically runs on push to `main` or `master` branch, or can be triggered manually.

### 🤖 Claude Assistant

**File:** `claude-assistant.yml`

**Purpose:** Provides GitHub Copilot integration for code assistance.

## Troubleshooting

### PDF Build Fails

If the PDF build fails, check the workflow logs for:

- **Python/LaTeX errors:** Look for error messages in the "Render Quarto Project (PDF)" step
- **Missing dependencies:** Check if all Python packages and system dependencies installed correctly
- **Source file errors:** Invalid QMD syntax, missing references, or broken code blocks

### Artifacts Not Available

If you don't see the artifact:

- Make sure the workflow completed successfully (green checkmark)
- Check that you're looking at the correct workflow run
- Verify the artifact hasn't expired (30-day retention period)
