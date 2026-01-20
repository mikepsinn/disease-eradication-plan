# PDF Link Preprocessing Tests

This directory contains tests to verify that PDF link preprocessing works correctly.

## Overview

The PDF rendering process uses a temp folder approach to rewrite cross-site links without modifying source files. These tests verify that:

1. **Internal links** (to files in the same config) remain as `.qmd` paths
2. **Cross-site links** (to files in book config but not current config) become absolute URLs to `https://manual.WarOnDisease.org`
3. **External URLs** remain unchanged
4. **Anchor-only links** remain unchanged

## Quick Start

### Windows
```cmd
scripts\test-pdf-links.bat
```

### Linux/Mac
```bash
bash scripts/test-pdf-links.sh
```

### Manual
```bash
python scripts/render-test-pdf.py --verify
```

## Test Files

- **`_quarto-test.yml`** - Minimal test configuration with only test files
- **`knowledge/test/test-economics.qmd`** - Test document with various link types
- **`knowledge/test/test-parameters.qmd`** - Test parameters document with cross-references
- **`scripts/render-test-pdf.py`** - Test render script
- **`scripts/test/verify-pdf-links.py`** - Verification script

## How It Works

1. **Prepare** - Copy test config and index files
2. **Create temp** - Copy all files to `_build_temp/` and rewrite cross-site links
3. **Render** - Generate PDF from temp folder
4. **Verify** - Check that links were rewritten correctly
5. **Cleanup** - Remove temp folder

## Expected Output

```
==========================================
CREATING TEMPORARY BUILD DIRECTORY
==========================================
[*] Created temporary build directory: _build_temp/
[*] Copying project files to _build_temp/...
[OK] Copied project files to _build_temp/
[*] Preprocessing QMD links in _build_temp/
[*] Source files: 3, Target files: 45
[*] knowledge/test/test-economics.qmd: ../appendix/drug-development-cost-analysis.qmd -> https://manual.WarOnDisease.org/knowledge/appendix/drug-development-cost-analysis.html
[*] knowledge/test/test-economics.qmd: ../appendix/regulatory-mortality-analysis.qmd -> https://manual.WarOnDisease.org/knowledge/appendix/regulatory-mortality-analysis.html
...
[OK] Preprocessed 2 QMD files, rewrote 5 links

==========================================
RENDERING TEST PDF FROM TEMP DIRECTORY
==========================================
[OK] Test PDF render complete!
[OK] PDF copied to test-links.pdf

==========================================
RUNNING VERIFICATION TESTS
==========================================

Checking index.qmd (test-economics.qmd)...
--------------------------------------------------------------------------------
[PASS] Internal link to parameters remains .qmd
[PASS] Internal link with anchor remains .qmd
[PASS] Cross-site link becomes absolute URL
[PASS] Cross-site regulatory link becomes absolute URL
...
[PASS] Anchor link to section unchanged

Checking test-parameters.qmd...
--------------------------------------------------------------------------------
[PASS] Internal link back to test-economics remains .qmd
[PASS] Cross-site DFDA link becomes absolute URL
[PASS] DFDA link should NOT have .qmd extension

================================================================================
VERIFICATION SUMMARY: 16 passed, 0 failed
================================================================================
```

## Troubleshooting

### PDF not generated
- Make sure Quarto is installed and in your PATH
- Check that all test files exist in `knowledge/test/`

### Links not rewritten
- Verify that `_quarto-manual.yml` exists and contains the target files
- Check that the target files are NOT in `_quarto-test.yml`

### Verification fails
- Review the preprocessed files in `_build_temp/` (before cleanup)
- Check the exact link syntax in test files
- Ensure link paths match what's expected in verification script

## Adding New Tests

To add new link types to test:

1. Add test case to `knowledge/test/test-economics.qmd`
2. Add corresponding verification in `scripts/test/verify-pdf-links.py`
3. Run tests to verify

## Integration with CI/CD

You can add this to GitHub Actions:

```yaml
- name: Test PDF link preprocessing
  run: python scripts/render-test-pdf.py --verify
```
