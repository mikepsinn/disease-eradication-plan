# Testing GitHub Actions Locally with ACT

## Overview

The `test-economics-pdf.yml` workflow is a standalone test workflow for debugging the economics PDF generation process locally before deploying to GitHub Actions.

## Prerequisites

1. **Docker Desktop** must be installed and running
   - Download: https://www.docker.com/products/docker-desktop

2. **ACT** must be installed
   - **Windows**: `choco install act-cli`
   - **macOS**: `brew install act`
   - **Linux**: `curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash`
   - Or download from: https://github.com/nektos/act/releases

## Quick Start

### Option 1: Run Test Script (Recommended)

**Windows (PowerShell):**
```powershell
cd e:\code\obsidian\websites\disease-eradication-plan
.\scripts\test-economics-local.ps1
```

**macOS/Linux (Bash):**
```bash
cd /path/to/disease-eradication-plan
bash scripts/test-economics-local.sh
```

### Option 2: Run ACT Directly

```bash
# From project root
act workflow_dispatch \
    -W .github/workflows/test-economics-pdf.yml \
    -j test-economics \
    --artifact-server-path ./act-artifacts \
    --verbose
```

## What the Test Does

1. ✅ Sets up Python 3.10, Quarto, and dependencies
2. ✅ Installs LaTeX (TinyTeX) for PDF generation
3. ✅ Runs `python scripts/render-economics-website.py`
4. ✅ Validates PDF exists at `_site/economics/dih-economic-models.pdf`
5. ✅ Uploads artifacts to `./act-artifacts/`
6. ⏭️ Skips Netlify deployment (requires secrets)

## Expected Output

If successful, you'll see:
```
✅ PDF found in correct location: _site/economics/dih-economic-models.pdf
-rw-r--r-- 1 user user 32M Jan 15 10:30 _site/economics/dih-economic-models.pdf
```

The PDF will be available in: `act-artifacts/economics-site-test/dih-economic-models.pdf`

## Troubleshooting

### PDF Not Generated

If the build succeeds but PDF is missing:

1. **Check LaTeX output** in the ACT logs:
   ```
   Rendering PDF
   running lualatex - 1
   running lualatex - 2
   running lualatex - 3
   ```

2. **Check for errors** in Python cell execution (434 cells in parameters-and-calculations.qmd)

3. **Verify post-processing ran**:
   ```
   POST-PROCESSING ECONOMICS PDF
   [*] Found PDF in wrong location: The-1%-Treaty-...pdf
   [*] Moving to: _site/economics/dih-economic-models.pdf
   [OK] PDF moved successfully
   ```

### Docker Issues

**"Docker is not running"**
- Start Docker Desktop and wait for it to fully initialize

**"Cannot connect to Docker daemon"**
- On Windows: Make sure Docker Desktop is set to run Linux containers (not Windows containers)
- On Linux: Make sure your user is in the `docker` group: `sudo usermod -aG docker $USER`

### ACT Issues

**"act: command not found"**
- ACT is not installed or not in PATH. Follow installation instructions above.

**"Image pull failed"**
- ACT needs to download a ~2GB Docker image on first run. Ensure good internet connection.
- If stuck, try: `docker pull catthehacker/ubuntu:act-latest`

**"Permission denied" errors**
- On Linux/macOS: Use `sudo` or fix Docker permissions
- On Windows: Run PowerShell as Administrator

## Comparing with Main Book Workflow

The test workflow mirrors the `build-economics` job in `publish.yml` but:
- ✅ Runs independently (no parallel jobs)
- ✅ Uploads artifacts for inspection
- ✅ Has explicit PDF validation step
- ⏭️ Skips Netlify deployment by default
- 🐛 Includes verbose logging for debugging

## Running on GitHub Actions

To test on actual GitHub infrastructure:

1. Push to GitHub:
   ```bash
   git add .github/workflows/test-economics-pdf.yml
   git commit -m "test: Add economics PDF test workflow"
   git push
   ```

2. Go to: https://github.com/YOUR_USERNAME/disease-eradication-plan/actions
3. Select "Test Economics PDF Build" workflow
4. Click "Run workflow"
5. Download artifacts after completion

## Next Steps After Successful Test

Once the PDF generates correctly in ACT:

1. ✅ Verify PDF quality (check file size, page count, figures)
2. ✅ Compare with book PDF generation (should be similar)
3. ✅ Update main `publish.yml` workflow if needed
4. ✅ Delete or disable test workflow once satisfied

## Files

- `.github/workflows/test-economics-pdf.yml` - Test workflow
- `.actrc` - ACT configuration
- `scripts/test-economics-local.ps1` - Windows test script
- `scripts/test-economics-local.sh` - Linux/macOS test script
- `act-artifacts/` - Local test artifacts (gitignored)
