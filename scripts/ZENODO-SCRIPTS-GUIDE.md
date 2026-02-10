# Zenodo Scripts Guide

## Overview

All Zenodo scripts now properly handle **Concept DOIs** (stable across versions) vs **Version DOIs** (specific uploads).

## DOI Storage Format in Configs

```yaml
metadata:
  # Identifiers
  # Zenodo Concept DOI (stable across all versions - use for citations and new versions)
  doi: "10.5281/zenodo.18205881"
  zenodo_version_doi: "10.5281/zenodo.18480097"  # Latest published version (optional)
```

**Key Points:**
- `doi` field ALWAYS contains the **concept DOI**
- Concept DOI is stable forever - use for citations and creating new versions
- `zenodo_version_doi` tracks the latest published version (auto-updated by upload script)
- Block comments are preserved by YAML tools (unlike inline comments)

## Script Reference

### Core Upload/Management Scripts

#### `upload-all-zenodo-and-save-dois.py`
**Purpose:** Upload PDFs to Zenodo with metadata

**Concept DOI Handling:**
- ✅ Reads concept DOI from `metadata.doi`
- ✅ Uses concept DOI to find existing record
- ✅ Creates new VERSION draft (not duplicate record)
- ✅ Saves concept DOI back to config with `save_doi_to_config()`
- ✅ Also saves version DOI to `zenodo_version_doi` field

**Usage:**
```bash
python scripts/upload-all-zenodo-and-save-dois.py
python scripts/upload-all-zenodo-and-save-dois.py --paper wishocracy
```

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

##### `save_doi_to_config(config_path, doi, url, version_doi=None)`
- Saves concept DOI to `metadata.doi`
- Optionally saves version DOI to `metadata.zenodo_version_doi`
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
