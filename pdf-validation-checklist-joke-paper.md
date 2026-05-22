# PDF Validation Errors - Checklist

**PDF:** `E:\code\disease-eradication-plan\assets\pdfs\joke-paper.pdf`
**Quarto config:** `E:\code\disease-eradication-plan\_quarto-joke.yml`
**Generated:** 2026-05-21T20:18:40.017994

## Summary

- **Total issues:** 1
- **Critical:** 0
- **Warnings:** 0

## IMPORTANT: Before You Start

**DO NOT edit `index.qmd` directly - it is auto-generated!**

1. **First, review the Quarto config:** `E:\code\disease-eradication-plan\_quarto-joke.yml`
   - This config specifies the main QMD file used to generate this PDF
   - The main QMD file is copied to `index.qmd` during the build process
   - Any edits to `index.qmd` will be overwritten on the next build

2. **Edit the source QMD file specified in the config, NOT `index.qmd`**

---

## ℹ️ NO_IMAGES (1 issue(s))

### How to Fix
**Source:** A long PDF has no embedded images.
**Fix:** This may be intentional for text-heavy papers. If images should exist:
- Check that image files exist at the referenced paths
- Verify image format is supported (PNG, JPG, PDF)
- Check Quarto logs for image embedding errors

### Occurrences

- [ ] **General:** PDF has 37 pages but no images
