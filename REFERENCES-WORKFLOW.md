---
title: References URL Update Workflow
description: Systematic workflow for adding source URLs to 400+ references in the book using extraction and integration scripts.
---

# References URL Update Workflow

This document explains the workflow for adding URLs to references in the book.

## Overview

The [references.qmd](brain/book/references.qmd) file contains 400+ references that are missing URLs (marked with `<!-- TODO: Add source URL -->`). This workflow helps you systematically add URLs to these references.

## Files Involved

- **[brain/book/references.qmd](brain/book/references.qmd)** - Main references file
- **references-to-update.md** - Generated file with references needing URLs (human-readable)
- **references-to-update.json** - Generated file with reference metadata (for integration script)
- **[scripts/extract-references-without-urls.ts](scripts/extract-references-without-urls.ts)** - Extraction script
- **[scripts/integrate-references.ts](scripts/integrate-references.ts)** - Integration script

## Workflow

### Step 1: Extract References Without URLs

Run the extraction script to generate a list of all references that need URLs:

```bash
npm run extract-references
```

This creates two files:

- `references-to-update.md` - Edit this file to add URLs
- `references-to-update.json` - Metadata for the integration script (don't edit)

### Step 2: Add URLs

Open `references-to-update.md` and add URLs for each reference. For each entry:

1. Find the appropriate source URL
2. Add it after the `**NEW URL:**` line
3. Format options:
   - Direct URL: `https://example.com/source`
   - Markdown link: `[Source Title](https://example.com)`
   - Note if no URL available: `No URL available - original source`

Example:

```markdown
## 1. 21st Century Cures Act (2016)

**ID:** `21st-century-cures-act-2016`

**Quote:**

> 21st Century Cures Act (2016)

**Current Source:**

> <!-- TODO: Add source URL -->

**NEW URL:** https://www.congress.gov/bill/114th-congress/house-bill/34

---
```

### Step 3: Integrate URLs Back

Once you've added URLs, run the integration script:

```bash
npm run integrate-references
```

This script will:

1. Create a backup of `references.qmd` at `brain/book/references.qmd.backup`
2. Update all references with the new URLs
3. Show a summary of updated references

### Step 4: Review Changes

1. Review the changes in [references.qmd](brain/book/references.qmd)
2. If satisfied:
   - Delete the backup file: `rm brain/book/references.qmd.backup`
   - Delete the update files: `rm references-to-update.md references-to-update.json`
   - Commit the changes
3. If not satisfied:
   - Restore from backup: `mv brain/book/references.qmd.backup brain/book/references.qmd`
   - Fix issues in `references-to-update.md`
   - Run integration script again

## Tips

- **Work in batches**: Add URLs for 10-20 references at a time, then integrate and review
- **Use Claude Code**: Ask Claude to help find URLs for references
- **Document missing URLs**: If you can't find a URL, add a note explaining why
- **Verify URLs**: Make sure URLs are working before integrating

## Reference Format

Each reference in `references.qmd` follows this format:

```markdown
<a id="reference-id"></a>
- **Reference Title**
  > "Quote or content from the source"
  > — [Source Name](https://url) or <!-- TODO: Add source URL -->
```

The scripts use the anchor tags (`<a id="...">`) as delimiters to identify and update individual references.

## Troubleshooting

### No references found

If the extraction script finds 0 references, check:

- Are there TODOs in [references.qmd](brain/book/references.qmd)?
- Run: `grep -c "TODO: Add source URL" brain/book/references.qmd`

### Integration failed

If integration fails:

- Check that `references-to-update.json` exists
- Verify you added URLs in `references-to-update.md`
- Ensure URLs are on the line after `**NEW URL:**`

### Want to start over

```bash
# Restore from backup if it exists
mv brain/book/references.qmd.backup brain/book/references.qmd

# Delete update files
rm references-to-update.md references-to-update.json

# Extract again
npm run extract-references
```
