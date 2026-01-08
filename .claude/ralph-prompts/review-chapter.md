---
max_iterations: 20
completion_promise: CHAPTER_REVIEWED
description: Review and improve a single chapter
---

# Chapter Review

Review the currently open QMD file for quality, consistency, and correctness.

## Review Checklist

1. **Variable Usage**
   - Are there hardcoded values that should use variables?
   - Are variable references correctly formatted?

2. **Links**
   - Do internal links use `.qmd` extension (not `.html`)?
   - Are external links valid?

3. **Citations**
   - Are claims properly cited with `@citation-key`?
   - Do citation keys exist in references.qmd?

4. **Writing Quality**
   - Is the content clear and concise?
   - Are there grammatical errors?
   - Is the tone appropriate?

5. **Structure**
   - Are headings properly nested?
   - Is content well-organized?

## Your Task

1. Read the file
2. Check each item above
3. Fix issues you find
4. Report what you fixed

## Completion

Output `<promise>CHAPTER_REVIEWED</promise>` when you have reviewed all aspects and made necessary improvements.
