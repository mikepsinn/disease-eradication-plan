---
name: check-duplicate-references
enabled: true
event: file
conditions:
  - field: file_path
    operator: ends_with
    pattern: references.bib
---

⚠️ **Editing references.bib - Check for duplicates first!**

Before adding a new reference, search the existing bibliography:

1. **Search for similar entries:**
   - Search by author name: `grep -i "author_surname" references.bib`
   - Search by title keywords: `grep -i "keyword" references.bib`
   - Search by year: `grep "year = {2024}" references.bib`

2. **Common duplicate patterns:**
   - Same source cited with different keys (e.g., `smith2024` vs `smith2024a`)
   - Different editions of the same work
   - Preprint vs published version

3. **If a similar reference exists:**
   - Use the existing citation key
   - Update the existing entry if needed (add DOI, page numbers, etc.)
   - Don't add a duplicate

4. **If adding a new reference:**
   - Follow consistent key naming: `{author}{year}{keyword}`
   - Ensure all required fields are present
   - Verify no existing entry covers this source

**Run this first:** `grep -i "AUTHOR_NAME_OR_KEYWORD" references.bib`
