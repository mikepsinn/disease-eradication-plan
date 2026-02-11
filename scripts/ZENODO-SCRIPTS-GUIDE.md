# Zenodo Scripts Guide

## Overview

All Zenodo scripts now properly handle **Concept DOIs** (stable across versions) vs **Version DOIs** (specific uploads).

## DOI Storage Format in Configs

```yaml
metadata:
  # Identifiers
  # Zenodo Concept DOI (stable across all versions - use for citations and new versions)
  doi: "10.5281/zenodo.18205881"
```

**Key Points:**
- `doi` field ALWAYS contains the **concept DOI**
- Concept DOI is stable forever, assigned once on first publish, never changes
- The upload script resolves the latest version ID via the API; no version DOI needed in config
- Block comments are preserved by YAML tools (unlike inline comments)

## Metadata Fields

### Automatically Populated Fields

All Zenodo uploads now include comprehensive metadata automatically extracted from your configs and source files:

| Field | Source | Description |
|-------|--------|-------------|
| **title** | `metadata.title` | Paper title |
| **description** | Abstract from QMD frontmatter or config | Full abstract with resolved variables, dollar sign escaping |
| **creators** | `author` field | Authors with affiliations and ORCIDs |
| **keywords** | `metadata.keywords` | Subject keywords (max 10) |
| **license** | `metadata.license` | License identifier (e.g., `cc-by-nc-4.0`) |
| **rights** | Auto-generated from license + author | Copyright statement: "© 2026 Author Name. Licensed under License" |
| **references** | `references.bib` | Only citations actually used in paper (with DOIs when available) |
| **publisher** | `metadata.zenodo.publisher` or `metadata.publisher` | Publishing organization |
| **publication_date** | Auto-generated | Current date |
| **version** | `metadata.version` | Version string |
| **related_identifiers** | `book.site-url` or `website.site-url` | Link to live website |
| **communities** | Auto-added | `decentralized-fda` community |

### Optional Fields (Add to Config)

**Grants/Funding Information:**
```yaml
metadata:
  grants:
    - title: "Open Science Grant"
      code: "OSG-2024-12345"
      funder: "National Science Foundation"
    - title: "Research Fellowship"
      code: "RF-2025-67890"
      funder: "Research Foundation"
```

**Alternate Identifiers (arXiv, SSRN, etc.):**
```yaml
metadata:
  alternate_ids:
    - scheme: "arxiv"
      identifier: "2401.12345"
    - scheme: "ssrn"
      identifier: "4567890"
    - scheme: "handle"
      identifier: "1234/5678"
```

### Reference Extraction Details

The system automatically:
1. **Scans all QMD files** for citation patterns (`@cite-key`)
2. **Parses `references.bib`** to extract full citation information
3. **Includes only cited references** (not entire bibliography)
4. **Formats with DOIs/URLs** when available in .bib entries
5. **Creates Zenodo reference objects** with proper relation metadata

Example extracted reference:
```json
{
  "raw_reference": "Smith, J. (2020). Paper Title. Journal Name, 10(2), 123-145.",
  "identifier": "10.1234/journal.2020.12345",
  "scheme": "doi",
  "relation": "cites"
}
```

## Script Reference

### Core Upload/Management Scripts

#### `upload-all-zenodo-and-save-dois.py`
**Purpose:** Upload PDFs to Zenodo with complete metadata and auto-publish

**What It Does:**
- ✅ Full PDF validation with LLM checks (blocks on errors)
- ✅ Extracts complete metadata (title, authors, abstract, references, copyright, grants)
- ✅ Reads concept DOI from `metadata.doi`
- ✅ Uses concept DOI to find existing record
- ✅ Creates new VERSION draft (not duplicate record)
- ✅ **Automatically publishes** after validation passes (default behavior)
- ✅ Saves concept DOI and version DOI back to config

**Metadata Extraction:**
- Resolves Quarto variables in abstracts and descriptions
- Escapes dollar signs to prevent LaTeX issues
- Extracts 15+ references from `references.bib` (only cited ones)
- Auto-generates copyright statement from license + author
- Includes grants and alternate IDs if present in config

**Usage:**
```bash
# Auto-publish after validation (default)
python scripts/upload-all-zenodo-and-save-dois.py

# Create drafts only (manual review required)
python scripts/upload-all-zenodo-and-save-dois.py --draft

# Specific papers
python scripts/upload-all-zenodo-and-save-dois.py wishocracy economics

# Force revalidation (ignore cached results)
python scripts/upload-all-zenodo-and-save-dois.py --force-revalidate

# Show full build/validation output
python scripts/upload-all-zenodo-and-save-dois.py --verbose
```

**Publication Modes:**
- **Default (no flag)**: Auto-publish after validation ✅ Recommended
- **`--draft` flag**: Create drafts only, manual publish required on Zenodo

Since validation is rigorous (LLM checks entire PDF, blocks on errors), auto-publish is safe and convenient.

#### `audit-zenodo.py`
**Purpose:** Check for metadata drift and issues

**Concept DOI Handling:**
- ✅ Reads concept DOI from `metadata.doi`
- ✅ Converts to record ID with `get_record_id_from_doi()`
- ✅ Fetches latest version from Zenodo API
- ✅ Compares local vs remote metadata
- ✅ Detects duplicates by concept ID

**Usage:**
```bash
python scripts/audit-zenodo.py --verbose
python scripts/audit-zenodo.py --write-todos
```

#### `sync-zenodo-metadata.py`
**Purpose:** Update Zenodo metadata to match local configs

**Concept DOI Handling:**
- ✅ Reads concept DOI from `metadata.doi`
- ✅ Fetches existing record by concept ID
- ✅ Automatically detects and deletes existing drafts (default behavior)
- ✅ Creates new version draft with updated metadata
- ✅ Preserves concept DOI relationship

**Abstract Extraction:**
- ✅ Extracts abstract from QMD file frontmatter if not in config
- ✅ Resolves Quarto variables (`{{< var name >}}`) in abstracts and descriptions
- ✅ Escapes dollar signs (`$` → `\$`) to prevent LaTeX interpretation
- ✅ Formats description as: `<p><strong>Abstract:</strong> ...</p><p><strong>Summary:</strong> ...</p>`

**Usage:**
```bash
python scripts/sync-zenodo-metadata.py --dry-run              # Preview changes
python scripts/sync-zenodo-metadata.py                        # Sync all papers (auto-replaces drafts)
python scripts/sync-zenodo-metadata.py --paper wishocracy     # Sync specific paper
python scripts/sync-zenodo-metadata.py --keep-drafts          # Skip papers with existing drafts
python scripts/sync-zenodo-metadata.py --paper wishocracy --verbose
```

**Note:** Draft replacement is now the default. Existing drafts are automatically deleted and recreated with updated metadata. Use `--keep-drafts` to preserve existing drafts (will skip those papers instead).

### Utility Scripts

#### `cleanup-zenodo-duplicates.py`
**Purpose:** One-time cleanup of incorrectly created duplicates

**Status:** ✅ Already executed successfully - created proper concept DOI structure

**What it did:**
- Deleted 11 incorrect draft deposits
- Updated all configs to use concept DOIs
- No longer needed (mission accomplished)

### Library Functions

#### `lib/zenodo_client.py`

**Key Functions:**

##### `get_record_id_from_doi(doi: str) -> Optional[int]`
- Extracts record ID from DOI string
- Works with both concept and version DOIs
- Returns concept record ID when given concept DOI

##### `save_doi_to_config(config_path, doi, url)`
- Saves concept DOI to `metadata.doi`
- Skips writing if concept DOI already matches (avoids unnecessary config changes)
- Adds explanatory block comments
- Preserves YAML formatting

##### `extract_zenodo_metadata(quarto_config, paper_key)`
- Extracts metadata for Zenodo upload
- Returns concept DOI in `_existing_doi` field
- Upload function uses this to find existing records

## How Version Creation Works

1. **Config has concept DOI**: `doi: "10.5281/zenodo.18205881"`
2. **Upload script reads it**: `existing_doi = metadata.get("doi")`
3. **Gets record ID**: `record_id = get_record_id_from_doi(doi)` → 18205881
4. **Creates new version**: `client.create_version_draft(record_id)`
5. **New draft linked**: Same concept DOI, new version DOI
6. **Saves back**: Updates config with concept DOI + latest version DOI

## Metadata Best Practices

### Ensuring Complete Metadata

**Before uploading to Zenodo:**

1. ✅ **Check `references.bib`** - All citations have DOIs when available
2. ✅ **Verify abstracts** - QMD frontmatter has complete abstract (fallback to config)
3. ✅ **Add funding info** - Include grants if your work was funded
4. ✅ **Add alternate IDs** - Include arXiv/SSRN IDs if paper is published elsewhere
5. ✅ **Review authors** - Ensure all authors have ORCIDs and affiliations

**Checking extracted metadata:**
```bash
# Test metadata extraction before upload
python -c "
import sys; sys.path.insert(0, 'scripts/lib')
from pathlib import Path
from zenodo_client import extract_zenodo_metadata
import yaml

config = yaml.safe_load(open('_quarto-yourpaper.yml'))
meta = extract_zenodo_metadata(config, 'yourpaper', Path('.'))

print(f'References: {len(meta.get(\"references\", []))}')
print(f'Rights: {meta.get(\"rights\")}')
print(f'Grants: {len(meta.get(\"grants\", []))}')
"
```

### Updating Existing Records

When you update metadata in configs (add grants, fix author info, etc.), use sync script to update Zenodo:

```bash
# Preview changes
python scripts/sync-zenodo-metadata.py --dry-run --verbose

# Apply updates (auto-deletes existing drafts)
python scripts/sync-zenodo-metadata.py

# Update specific paper
python scripts/sync-zenodo-metadata.py --paper wishocracy
```

The sync script will:
- Extract updated metadata (including new references, grants, copyright)
- Delete any existing drafts automatically
- Create new draft with complete metadata
- Show you the diff of what changed

## Workflow

### Publishing a New Version

1. Make changes to your paper
2. Run upload script:
   ```bash
   python scripts/upload-all-zenodo-and-save-dois.py
   ```
3. Script creates new version draft on Zenodo
4. Review draft at URL shown in output
5. Publish manually on Zenodo when ready

### Checking Metadata Sync

1. Run audit:
   ```bash
   python scripts/audit-zenodo.py --verbose
   ```
2. If drift detected, run sync:
   ```bash
   python scripts/sync-zenodo-metadata.py --dry-run
   python scripts/sync-zenodo-metadata.py
   ```
3. Review and publish drafts on Zenodo

## Common Issues

### Reference Extraction

**Problem:** No references extracted (count = 0)

**Causes & Fixes:**
- ✅ Check `references.bib` exists and is valid BibTeX format
- ✅ Ensure citations use correct format: `@cite-key` in QMD files
- ✅ Verify cite keys match exactly (case-sensitive)
- ✅ Install `bibtexparser`: `pip install bibtexparser`

**Debug:**
```bash
# Check what's being extracted
python -c "
import sys; sys.path.insert(0, 'scripts/lib')
from pathlib import Path
from zenodo_client import extract_cited_references
import yaml

config = yaml.safe_load(open('_quarto-yourpaper.yml'))
refs = extract_cited_references('yourpaper', config, Path('.'))
print(f'Found {len(refs)} references')
for ref in refs[:3]:
    print(f'  - {ref[\"raw_reference\"][:60]}...')
"
```

### Copyright Statement

**Problem:** Want to customize copyright statement

**Solution:** The copyright is auto-generated from:
- Author name (first creator)
- Current year
- License from config

To customize, you can add a custom rights statement to your config:
```yaml
metadata:
  zenodo:
    rights: "Custom copyright statement here"
```

If `zenodo.rights` is present, it will override the auto-generated one.

### Missing DOIs in References

**Problem:** References extracted but DOIs missing

**Solution:** Add DOIs to your `references.bib` entries:
```bibtex
@article{smith2020,
  author = {Smith, John},
  title = {Paper Title},
  journal = {Journal Name},
  year = {2020},
  doi = {10.1234/journal.2020.12345}  # <-- Add this
}
```

## Troubleshooting

### "Duplicate" deposits with different concept IDs
**Cause:** Upload script couldn't find existing record
**Fix:** Ensure `metadata.doi` contains concept DOI (not version DOI)

### Upload creates new record instead of version
**Cause:** DOI in config is version-specific, not concept
**Fix:** Check config has concept DOI with comment block

### Metadata drift warnings
**Cause:** Local config metadata differs from Zenodo
**Fix:** Run `sync-zenodo-metadata.py` to update Zenodo

## Files Modified (2026-02-09)

- ✅ `scripts/lib/zenodo_client.py` - Enhanced DOI handling
- ✅ All `_quarto-*.yml` configs - Added concept DOI comments
- ✅ `scripts/cleanup-zenodo-duplicates.py` - Cleaned up duplicates
- ✅ `scripts/sync-zenodo-metadata.py` - Created for metadata sync

## Next Steps

When you next upload:
1. Config will have concept DOI
2. Upload script will find existing record
3. Create proper new version (not duplicate)
4. Save both concept and version DOIs back to config
5. All scripts will work correctly with concept DOI system
