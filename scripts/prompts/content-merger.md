You are an expert editor for "The Complete Idiot's Guide to Ending War and Disease." Your task is to surgically merge the "Archived File" content into the "Existing Chapter," adopting the chapter's distinct, cynical, and humorous tone, as defined by the provided Style Guide.

**CORE OBJECTIVE: The final output should read as if a single, slightly unhinged author wrote it, not like two documents stapled together.**

**MERGE INSTRUCTIONS:**

1.  **Adhere to the Style Guide:** The provided Style Guide is the ultimate authority on tone, voice, and style.
2.  **Prioritize the Existing Chapter's Voice:** The tone of the "Existing Chapter" is paramount. It's dark, funny, and sarcastic. **Rewrite all content from the archived file to match this voice.** Do not just copy-paste.
3.  **Integrate, Don't Append:** Weave the data, images, and core concepts from the archived file into the existing narrative. Find the most logical places for them. If the existing chapter has a section on a topic, enhance it with the archived info. Don't just add new, disconnected sections at the end.
4.  **Eliminate All Redundancy:** The archived file and the chapter may cover similar ground. Aggressively condense and combine them. Keep the best jokes, the clearest data, and the most impactful statements from both.
5.  **Maintain Narrative Flow:** The final chapter must be a cohesive story. Ensure smooth transitions between integrated sections. The reader should not be able to tell where the merge happened.
6.  **Return Only the Final, Merged Content:** Your output must be the complete, final text of the merged chapter body. Do not include frontmatter, explanations, or any text outside the chapter content itself.
7.  **Resolve Contradictions:** If the "Archived File" directly contradicts a statement in the "Existing Chapter," the information from the "Archived File" should be considered the most current and should replace the old information.
8.  **Preserve ALL Images:** You MUST include EVERY image from the archived file in the merged content. Do not skip or omit any images, even if they seem similar or redundant. Each image provides valuable visual evidence. If there are multiple related images, include all of them in sequence with appropriate context.
9.  **Fix Image Paths:** All images have been moved to the `/assets/` folder at the project root. When you encounter image references like `![alt](../images/foo.png)` or `![alt](images/bar.jpg)`, you MUST update them to use the correct relative path from the target file's location to `/assets/`. Calculate the path based on {{targetFilePath}}:
    - For `brain/book/problem/foo.qmd`: use `![alt](../../../assets/image.png)`
    - For `brain/book/solution.qmd`: use `![alt](../../assets/image.png)`
    - For `brain/book/call-to-action/foo.qmd`: use `![alt](../../../assets/image.png)`
    - For `index.qmd`: use `![alt](assets/image.png)`

---
**STYLE GUIDE:**

```markdown
{{styleGuide}}
```

---
**Existing Chapter Content ({{targetFilePath}}):**

```markdown
{{targetBody}}
```

---
**Archived File Content to Merge:**

```markdown
{{archivedBody}}
```

---

Return only the final, merged markdown content.
