You are an expert editor tasked with organizing a book manuscript.
You need to decide what to do with an archived markdown file.
Based on the book's structure from `_quarto.yml` and the content of the archived file, determine one of the following actions:

1.  **MERGE**: The content is valuable and should be merged into an existing chapter.
2.  **CREATE**: The content is valuable and unique enough to become a new chapter or appendix file. Your decision should also consider creating new appendix files for content that is too detailed or technical for the main narrative.
3.  **DELETE**: The content is redundant, irrelevant, or low-quality and should be deleted.

**RESPONSE FORMAT:**

You MUST respond with a JSON object with the following structure:

```json
{
  "action": "MERGE" | "CREATE" | "DELETE",
  "reason": "A brief explanation for your decision.",
  "targetFile": "path/to/target/chapter.qmd", // (Required for MERGE)
  "newFilePath": "The full, root-relative path for the new file (e.g., 'brain/book/new-chapter.qmd' or 'brain/book/appendix/new-appendix.qmd').", // (Required for CREATE)
  "newFileContent": "The full content for the new chapter, including frontmatter." // (Required for CREATE)
}
```

---
**Book Structure (_quarto.yml):**
```yaml
{{quartoYmlContent}}
```
---
**Archived File Content ({{filePath}}):**
```markdown
{{archivedContent}}
