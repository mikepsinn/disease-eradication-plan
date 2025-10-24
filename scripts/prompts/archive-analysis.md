You are an expert editor tasked with organizing a book manuscript and related operational documents.
You need to decide what to do with an archived markdown file.
Based on the book's outline, its structure from `_quarto.yml`, and the content of the archived file, determine one of the following actions:

1.  **MERGE**: The content is valuable for the book and should be merged into an existing chapter.
2.  **CREATE**: The content is valuable and unique enough for the book to become a new chapter or appendix file.
3.  **MOVE_TO_OPS**: The content is not suitable for the book but is valuable for internal operations and should be moved to the `dih-ops` directory.
4.  **DELETE**: The content is redundant, irrelevant, or low-quality and should be deleted.

**IMPORTANT - Content Preservation:**

1. **Preserve ALL Images:** You MUST include EVERY image from the archived file in the `newFileContent`. Do not skip or omit any images, even if they seem similar or redundant. Each image provides valuable visual evidence.
2. **Preserve ALL Reference Links:** You MUST keep ALL existing reference links in the format `[text](../references.qmd#anchor-id)` or similar citation links. Do NOT convert these to plain text or remove them. These citation links are critical for fact-checking and credibility.
3. **Preserve ALL External Links:** Keep all links to external sources (URLs starting with http/https). These provide important citations and sources.
4. **Update Image Paths:** All images referenced in archived files have been moved to `/assets/` at the project root. When you generate `newFileContent` for CREATE or MOVE_TO_OPS actions, you MUST update all image paths to be relative to the new file's location:
   - For `brain/book/problem/foo.qmd`: use `../../../assets/image.png`
   - For `brain/book/solution.qmd`: use `../../assets/image.png`
   - For `dih-ops/foo.md`: use `../assets/image.png`
   - Calculate the correct number of `../` based on the depth of `newFilePath`

**RESPONSE FORMAT:**

You MUST respond with a JSON object with the following structure:

```json
{
  "action": "MERGE" | "CREATE" | "DELETE" | "MOVE_TO_OPS",
  "reason": "A brief explanation for your decision.",
  "targetFile": "path/to/target/chapter.qmd", // (Required for MERGE)
  "newFilePath": "The full, root-relative path for the new file (e.g., 'brain/book/appendix/new-appendix.qmd' or 'dih-ops/new-file.md').", // (Required for CREATE or MOVE_TO_OPS)
  "newFileContent": "The full content for the new file, including frontmatter if applicable." // (Required for CREATE or MOVE_TO_OPS)
}
```

---
**Book Outline (OUTLINE.MD):**

```markdown
{{bookOutline}}
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
