---
description: Add citations and references to claims
---

Review the current chapter and add proper citations for any unsupported claims.

## Process

1. **Identify unsupported claims**: Look for factual statements lacking citations
2. **Check existing references**: Review `brain/book/references.qmd` for matching citations
3. **Add reference links**: Use format `[see reference](#ref-id)`
4. **Create new references**: If needed, add to `references.qmd` with:
   ```markdown
   <a id="ref-id"></a>
   - **Title of Source**
     > Quote or data point
     > — Source URL or citation
   ```

## Citation Style

- Use relative path from chapter to references: `references.qmd#ref-id`
- Format: Claims with citations look like this [see reference](references.qmd#economic-burden-disease)
- Reference IDs should be kebab-case and descriptive

## Existing References

Load and review all references in `brain/book/references.qmd` before creating new ones to avoid duplicates.

## Guidelines

- **DO** cite specific numbers, statistics, and data
- **DO** cite controversial or surprising claims
- **DON'T** over-cite common knowledge
- **DON'T** break narrative flow with excessive citations

Update `lastFactCheckHash` in frontmatter when done.
