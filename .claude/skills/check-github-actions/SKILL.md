---
name: check-github-actions
description: Check GitHub Actions workflow status, diagnose failures, fetch logs, and fix common build issues. Use when builds fail, deploys break, or you need to investigate CI/CD problems.
---

# GitHub Actions Diagnostics Skill

Your task is to diagnose and fix GitHub Actions workflow failures for the mikepsinn/disease-eradication-plan Quarto-based multi-site publishing project.

## Diagnostic Process

Follow these steps systematically:

## Repository

Repo: `mikepsinn/disease-eradication-plan`

All `gh` commands should use: `gh --repo mikepsinn/disease-eradication-plan`

## Workflows

### 1. `publish.yml` - Main Build & Deploy

Triggers: push to master, manual dispatch

13 parallel jobs, each building one paper/site and deploying to Netlify:

| Job | Config | Netlify Site |
|-----|--------|-------------|
| build-manual | `_quarto-manual.yml` | manual.warondisease.org |
| build-1-pct-treaty | `_quarto-1-pct-treaty-impact.yml` | impact.warondisease.org |
| build-iab | `_quarto-iab.yml` | iab.warondisease.org |
| build-wishocracy | `_quarto-wishocracy.yml` | wishocracy.warondisease.org |
| build-dfda-spec | `_quarto-dfda-spec.yml` | dfda-spec.warondisease.org |
| build-dfda-impact | `_quarto-dfda-impact.yml` | dfda-impact.warondisease.org |
| build-obg | `_quarto-obg.yml` | obg.warondisease.org |
| build-opg | `_quarto-opg.yml` | opg.warondisease.org |
| build-optimocracy | `_quarto-optimocracy.yml` | optimocracy.warondisease.org |
| build-cost-of-change | `_quarto-cost-of-change.yml` | cost-of-change.warondisease.org |
| build-political-dysfunction-tax | `_quarto-political-dysfunction-tax.yml` | political-dysfunction-tax.warondisease.org |
| build-federal-efficiency-audit | `_quarto-federal-efficiency-audit.yml` | federal-efficiency-audit.warondisease.org |
| build-invisible-graveyard | `_quarto-invisible-graveyard.yml` | invisible-graveyard.warondisease.org |

Each job:
1. Checkout repo
2. Cache Quarto freeze directory
3. Setup Quarto, Python 3.12, uv
4. Install graphviz, Python deps, dih_models, Jupyter kernel
5. Cache + install TinyTeX (for PDF)
6. Render HTML + PDF via `scripts/render-quarto.py`
7. Upload LaTeX logs as artifact on failure
8. Deploy to Netlify

### 2. `domain-status-check.yml` - Domain Health

Triggers: weekly cron (Mondays 9am UTC), manual dispatch

Checks all site domains are healthy, creates/updates GitHub issues for unhealthy ones.

## Diagnostic Workflow

### Step 1: Get Current Status

```bash
# List recent workflow runs (last 10)
gh run list --repo mikepsinn/disease-eradication-plan --limit 10

# Check a specific workflow
gh run list --repo mikepsinn/disease-eradication-plan --workflow publish.yml --limit 5
```

### Step 2: Investigate Failures

```bash
# View a specific run (replace RUN_ID)
gh run view RUN_ID --repo mikepsinn/disease-eradication-plan

# List failed jobs in a run
gh run view RUN_ID --repo mikepsinn/disease-eradication-plan --json jobs --jq '.jobs[] | select(.conclusion == "failure") | {name, conclusion}'

# Get logs for a failed job
gh run view RUN_ID --repo mikepsinn/disease-eradication-plan --log-failed
```

If `--log-failed` output is too large, narrow to a specific job:

```bash
# Get job IDs
gh run view RUN_ID --repo mikepsinn/disease-eradication-plan --json jobs --jq '.jobs[] | select(.conclusion == "failure") | {databaseId, name}'

# Get logs for specific job
gh api repos/mikepsinn/disease-eradication-plan/actions/jobs/JOB_ID/logs
```

### Step 3: Download Artifacts (LaTeX logs)

Failed PDF builds upload LaTeX logs as artifacts:

```bash
# List artifacts for a run
gh run view RUN_ID --repo mikepsinn/disease-eradication-plan --json artifacts

# Download LaTeX log artifact
gh run download RUN_ID --repo mikepsinn/disease-eradication-plan --name latex-logs-JOBNAME --dir /tmp/latex-logs
```

### Step 4: Diagnose Common Issues

#### LaTeX / PDF Errors

**Symptoms**: Job fails at "Render" step, LaTeX log artifact uploaded
**Common causes**:
- Missing LaTeX package: Check log for `! LaTeX Error: File 'package.sty' not found`
  - Fix: Add package to TinyTeX install step in `publish.yml` or the `_extensions/` config
- Undefined control sequence: `! Undefined control sequence` in log
  - Fix: Check the QMD file for broken LaTeX macros, mismatched `$$` blocks
- Unicode errors: Characters that LaTeX can't render
  - Fix: Replace special characters or add appropriate LaTeX packages
- Overfull/underfull boxes: Usually warnings, not fatal

**Where to look**: Download LaTeX logs artifact, search for lines starting with `!`

#### Python / Jupyter Errors

**Symptoms**: Job fails during render, Python traceback in logs
**Common causes**:
- Import error: Missing package in `requirements.txt` or `pyproject.toml`
- Variable not defined: Parameter referenced in code cell but not in `dih_models/parameters.py`
- Encoding errors on Windows vs Linux: Scripts missing UTF-8 encoding header
  - Fix: Add `sys.stdout.reconfigure(encoding='utf-8')` header

**Where to look**: Search logs for `Traceback`, `ImportError`, `NameError`

#### Quarto Render Errors

**Symptoms**: Render step fails before PDF generation
**Common causes**:
- Missing QMD file: File referenced in `_quarto-*.yml` render list but doesn't exist
- Broken cross-references: `@ref` or `{{< var >}}` pointing to nonexistent targets
- YAML parse error: Malformed frontmatter in QMD or config file
- Missing bibliography entry: `@citation_key` not in `references.bib`

**Where to look**: Search logs for `ERROR`, `Warning`, `undefined reference`

#### Netlify Deploy Errors

**Symptoms**: Render succeeds but deploy step fails
**Common causes**:
- Missing `NETLIFY_AUTH_TOKEN` secret
- Missing `NETLIFY_SITE_ID_*` secret for specific site
- Site not configured in Netlify dashboard
- Deploy directory doesn't exist (render produced no output)

**Where to look**: Search logs for `Netlify`, `deploy`, `404`, `401`

#### Dependency / Setup Errors

**Symptoms**: Job fails early (before render)
**Common causes**:
- `uv pip install` failure: Package version conflict or unavailable
- Quarto version mismatch: Feature used that requires newer Quarto
- TinyTeX cache corruption: Clear cache by re-running with fresh checkout
- Graphviz not installed: Mermaid/diagram rendering fails

**Where to look**: Search logs for the specific setup step that failed

### Step 5: Fix and Verify

After identifying the issue:

1. **Fix locally** - Make the code/config change
2. **Test locally if possible**:
   ```bash
   # Render a specific project locally
   python scripts/render-quarto.py <project-key> --to html
   python scripts/render-quarto.py <project-key> --to pdf
   ```
3. **Commit and push** - The push triggers a new build
4. **Monitor** - Watch the new run:
   ```bash
   gh run list --repo mikepsinn/disease-eradication-plan --limit 3
   gh run watch RUN_ID --repo mikepsinn/disease-eradication-plan
   ```

### Step 6: Re-run Failed Jobs

If a failure was transient (network issue, flaky dependency):

```bash
# Re-run only failed jobs
gh run rerun RUN_ID --repo mikepsinn/disease-eradication-plan --failed

# Re-run entire workflow
gh run rerun RUN_ID --repo mikepsinn/disease-eradication-plan
```

## Quick Status Report

When user asks "check builds" or similar, provide a concise report:

```
GitHub Actions Status
---------------------
Last run: #123 (2h ago) - 11/13 jobs passed

Failed jobs:
  build-wishocracy: LaTeX error (missing package)
  build-dfda-spec: Python ImportError

Passing jobs: build-manual, build-1-pct-treaty, build-iab, ...

Recent runs:
  #123 (2h ago)  - 11/13 passed
  #122 (1d ago)  - 13/13 passed
  #121 (2d ago)  - 13/13 passed
```

## Manual Trigger

To trigger a build without pushing:

```bash
gh workflow run publish.yml --repo mikepsinn/disease-eradication-plan
```

## Secrets Reference

Required repository secrets for `publish.yml`:

| Secret | Purpose |
|--------|---------|
| `NETLIFY_AUTH_TOKEN` | Netlify API authentication |
| `NETLIFY_SITE_ID_MANUAL` | Site ID for manual.warondisease.org |
| `NETLIFY_SITE_ID_1_PCT_TREATY` | Site ID for impact.warondisease.org |
| `NETLIFY_SITE_ID_IAB` | Site ID for iab.warondisease.org |
| ... (one per site) | Each job uses its own site ID secret |
| `ZENODO_TOKEN` | Zenodo API token (for publish step) |
