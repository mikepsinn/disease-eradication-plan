# Zenodo Publishing Guide

This document explains how to automatically upload your Quarto papers to Zenodo for permanent archival and DOI assignment.

## What is Zenodo?

[Zenodo](https://zenodo.org) is an open-access repository operated by CERN that:
- Assigns DOIs (Digital Object Identifiers) to your papers
- Provides permanent archival of research outputs
- Integrates with ORCID and other academic systems
- Supports versioning (new DOI versions for updates)

## Workflow

**CI uploads drafts → You review → You publish manually on Zenodo**

This approach:
- Automates the tedious work (building PDFs, uploading, setting metadata)
- Gives you control over when to actually publish
- Lets you review/edit metadata before making it permanent
- Avoids DOI pollution from every commit

## Setup

### 1. Create Zenodo Account

1. Go to https://zenodo.org and sign up (or use GitHub/ORCID login)
2. Optionally, use https://sandbox.zenodo.org for testing first

### 2. Generate API Tokens

**Production token:**
1. Go to https://zenodo.org/account/settings/applications/
2. Click "New token"
3. Name it (e.g., "GitHub Actions - Disease Eradication Plan")
4. Select scopes: `deposit:write` and `deposit:actions`
5. Copy the token (you won't see it again!)

**Sandbox token (for testing):**
1. Go to https://sandbox.zenodo.org/account/settings/applications/
2. Follow same steps as above

### 3. Add Tokens to GitHub Secrets

1. Go to your repo's Settings > Secrets and variables > Actions
2. Add these secrets:
   - `ZENODO_TOKEN`: Your production Zenodo API token
   - `ZENODO_SANDBOX_TOKEN`: Your sandbox Zenodo API token (optional)

## Usage

### Upload via GitHub Actions

1. Go to Actions > "Upload Papers to Zenodo"
2. Click "Run workflow"
3. Options:
   - **Paper**: Select specific paper or leave empty for all
   - **Use sandbox**: Test with sandbox.zenodo.org first

### Automatic Upload on Releases

When you create a GitHub Release, all papers are automatically uploaded as drafts to Zenodo.

### Publish on Zenodo

After CI uploads your drafts:
1. Go to https://zenodo.org/me/uploads
2. Review the draft(s) - check title, description, authors
3. Edit metadata if needed
4. Click "Publish" when ready

### Local Testing

```bash
# Set environment variable (Windows)
set ZENODO_SANDBOX_TOKEN=your-sandbox-token

# Set environment variable (Linux/Mac)
export ZENODO_SANDBOX_TOKEN="your-sandbox-token"

# Dry run (shows what would be uploaded)
python scripts/publish-zenodo.py --sandbox --dry-run

# Upload draft to sandbox (recommended first step)
python scripts/publish-zenodo.py --sandbox --draft --paper iab

# Then go to https://sandbox.zenodo.org/me/uploads to review and publish
```

## How It Works

### Metadata Extraction

The script reads metadata from your `_quarto-*.yml` files:

| Quarto Field | Zenodo Field |
|--------------|--------------|
| `website.title` / `book.title` | Title |
| `website.description` | Description |
| `metadata.human-author` | Creators |
| `metadata.keywords` | Keywords |
| `metadata.license` | License |
| `website.site-url` | Related identifiers |

### Versioning

- First publish creates a new deposit with a unique DOI
- Subsequent publishes create new versions under the same "concept DOI"
- The `zenodo-deposits.json` file tracks deposit IDs for versioning

### DOI Structure

Zenodo creates two DOIs:
- **Version DOI**: Specific to this version (e.g., `10.5281/zenodo.12345`)
- **Concept DOI**: Always resolves to latest version (e.g., `10.5281/zenodo.12344`)

Use the Concept DOI in citations if you want readers to always get the latest version.

## Paper Configuration

Papers are configured in `scripts/publish-zenodo.py`:

```python
PAPERS = {
    "iab": {
        "quarto_config": "_quarto-iab.yml",
        "pdf_path": "_build_temp/iab/_site/iab/incentive-alignment-bonds-paper.pdf",
        "resource_type": "publication-workingpaper",
    },
    # ... more papers
}
```

### Resource Types

Available resource types:
- `publication-workingpaper` (default)
- `publication-preprint`
- `publication-article`
- `publication-report`
- `publication-technicalnote`

## Recommended Workflow

1. **First time**: Use sandbox + dry-run to verify metadata extraction
2. **Test**: Upload draft to sandbox, review on Zenodo, publish there
3. **Production**: Run workflow for production, review drafts at zenodo.org/me/uploads
4. **Updates**: Create GitHub Release to auto-upload new versions as drafts
5. **Publish**: Manually publish on Zenodo when you're ready for a new DOI version

## Adding ORCID

Add your ORCID to `_quarto-*.yml` files:

```yaml
metadata:
  human-author: "Mike P. Sinn"
  orcid: "0000-0000-0000-0000"  # Add this line
```

## Troubleshooting

### "ZENODO_TOKEN environment variable not set"
Add the token to GitHub Secrets or set it locally.

### "PDF not found"
Build the paper first: `python scripts/render-quarto.py iab`

### "Validation error" from Zenodo
Check that all required metadata fields are present in your `_quarto-*.yml`.

### Rate Limits
Zenodo has rate limits. If you hit them, wait a few minutes and retry.

## References

- [Zenodo REST API Documentation](https://developers.zenodo.org/)
- [Zenodo Deposit Metadata](https://developers.zenodo.org/#representation)
- [GitHub Zenodo Integration](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content)
