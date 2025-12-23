# GitHub Actions Deployment Setup

This repository uses GitHub Actions to automatically build and deploy multiple sites to Netlify.

## Sites Deployed

| Site | URL | Netlify Secret | Output Directory |
|------|-----|----------------|------------------|
| **Main Book** | https://manual.WarOnDisease.org | `NETLIFY_MAIN_SITE_ID` | `_book/warondisease` |
| **Economics** | https://impact.dih.earth | `NETLIFY_ECONOMICS_SITE_ID` | `_site/economics` |
| **Wishocracy Paper** | https://paper.wishocracy.org | `NETLIFY_WISHOCRACY_SITE_ID` | `_site/wishocracy` |
| **IAB Paper** | https://iab.warondisease.org | `NETLIFY_IAB_SITE_ID` | `_site/iab` |

## Required GitHub Secrets

Add these secrets in **Settings → Secrets and variables → Actions → Repository secrets**:

### 1. NETLIFY_AUTH_TOKEN
Your Netlify authentication token (shared across all sites).

**How to get it:**
1. Log in to Netlify
2. Go to User Settings → Applications
3. Create a new Personal Access Token
4. Copy the token

### 2. NETLIFY_MAIN_SITE_ID
The Netlify site ID for WarOnDisease.org

**How to get it:**
1. Go to your site in Netlify (WarOnDisease.org)
2. Site Settings → General → Site information
3. Copy the **Site ID** (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### 3. NETLIFY_ECONOMICS_SITE_ID
The Netlify site ID for impact.dih.earth

### 4. NETLIFY_WISHOCRACY_SITE_ID ⚠️ **NEW - Required**
The Netlify site ID for paper.wishocracy.org

**Setup steps:**
1. Create a new site in Netlify
2. Configure custom domain: `paper.wishocracy.org`
3. Copy the Site ID
4. Add as GitHub secret: `NETLIFY_WISHOCRACY_SITE_ID`

### 5. NETLIFY_IAB_SITE_ID ⚠️ **NEW - Required**
The Netlify site ID for iab.warondisease.org

**Setup steps:**
1. Create a new site in Netlify
2. Configure custom domain: `iab.warondisease.org`
3. Copy the Site ID
4. Add as GitHub secret: `NETLIFY_IAB_SITE_ID`

## Workflow Overview

The GitHub Actions workflow (`.github/workflows/publish.yml`) performs these steps:

### Build Phase (Job: `build-html`)
1. **Setup environment** - Install Quarto, Python, Graphviz, dependencies
2. **Render main book** - Full book to `_book/warondisease/`
3. **Deploy main site** - Upload to Netlify (WarOnDisease.org)
4. **Render economics** - Economics site to `_site/economics/`
5. **Deploy economics** - Upload to Netlify (impact.dih.earth)
6. **Render Wishocracy paper** - Paper to `_site/wishocracy/`
7. **Deploy Wishocracy** - Upload to Netlify (paper.wishocracy.org)
8. **Render IAB paper** - Paper to `_site/iab/`
9. **Deploy IAB** - Upload to Netlify (iab.warondisease.org)
10. **Generate PDFs** - Create book PDF and EPUB versions

### Deploy Phase (Jobs: `deploy-main`, `deploy-economics`, `deploy-wishocracy`, `deploy-iab`)
These jobs run in parallel after the build completes, each downloading their respective artifacts and deploying to Netlify.

## Triggering Deployments

Deployments trigger automatically on:
- **Push to master branch** - Full production deployment
- **Manual workflow dispatch** - Run workflow manually from GitHub Actions tab

## Render Times (Approximate)

| Task | Timeout | Typical Duration |
|------|---------|------------------|
| Main book (85 files) | 25 min | ~8-10 min |
| Economics (71 files) | 25 min | ~6-8 min |
| Wishocracy paper (1 file) | 10 min | ~30 sec |
| IAB paper (1 file) | 10 min | ~30 sec |
| Book PDF | 20 min | ~10-15 min |
| Book EPUB | 30 min | ~15-20 min |

## Local Testing

Before pushing, test the renders locally:

```bash
# Main book
python scripts/render-book-website.py

# Economics site
python scripts/render-economics-website.py

# Wishocracy paper
python scripts/render-wishocracy.py

# IAB paper
python scripts/render-iab.py
```

## Troubleshooting

### "Context access might be invalid" warnings
These are expected if the secrets haven't been added to GitHub yet. Add the missing secrets to fix.

### Deployment failures
1. Check that the Netlify site exists and the Site ID is correct
2. Verify `NETLIFY_AUTH_TOKEN` is valid and has permissions
3. Check Netlify site settings for custom domain configuration

### Build timeouts
If builds timeout, check:
- Quarto freeze cache (may need clearing)
- Python dependencies (check for version conflicts)
- Graphviz installation (required for diagrams)

## Artifacts

The workflow creates these artifacts (retained for 1-30 days):

| Artifact | Retention | Content |
|----------|-----------|---------|
| `main-site` | 1 day | Built main book HTML |
| `economics-site` | 1 day | Built economics site HTML |
| `wishocracy-site` | 1 day | Built wishocracy paper HTML |
| `iab-site` | 1 day | Built IAB paper HTML |
| `book-pdf` | 30 days | PDF version of book |
| `book-epub` | 30 days | EPUB version of book |

You can download these from the Actions run page.
