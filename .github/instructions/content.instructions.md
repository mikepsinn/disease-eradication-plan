---
description: "Writing and content standards for Quarto markdown files"
applyTo: "knowledge/**/*.qmd, *.qmd"
---

# Content Writing Instructions

These instructions apply to all Quarto Markdown (QMD) content files in the book.

## Writing Style

Follow the tone and voice established in `GUIDES/STYLE_GUIDE.md`:

- **Tone**: Dark humor meets practical hope
- **Voice**: Weary but loving parent explaining obvious solutions
- **Target**: Intelligent non-experts who need jargon explained
- **Approach**: Instructional and actionable, not sales pitches

### Key Principles

1. **Be ruthlessly concise** - every word must earn its place
2. **Use dark humor sparingly** - about death and human stupidity
3. **Write instructional content** - "Here's how you..." not "We will..."
4. **Assume self-interest** - ground arguments in concrete incentives
5. **Use "we" inclusively** - include all humanity as participants

### Avoid

- Corporate buzzwords (synergy, paradigm shift, stakeholder)
- Overused cliches (let that sink in, think about that)
- Sales language (join us, together we can, our solution will)
- Euphemisms - call things by their real names
- Jargon without explanation

## Parameter Usage (CRITICAL)

**NEVER hardcode numeric values** in content. Always use the variable system:

### Correct Usage
```markdown
The treaty would redirect {{< var peace_dividend_annual >}} annually...
```

### Wrong Usage
```markdown
The treaty would redirect $113.5 billion annually...
```

### Before Using a Variable

1. Check if it exists: `grep "keyword" _variables.yml`
2. If not, define in `dih_models/parameters.py` first
3. Run generation: `.venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py`
4. Use lowercase version: `{{< var parameter_name >}}`

### LaTeX Math Blocks

Variables **DO NOT work** inside `$$` blocks. Use LaTeX-specific variables:

```markdown
{{< var parameter_name_latex >}}
```

Never manually insert values into LaTeX equations.

## Cross-Format Linking

**ALWAYS use `.qmd` extensions** for internal links:

✅ Correct:
```markdown
[See details](../economics/roi-analysis.qmd#calculation-methods)
```

❌ Wrong:
```markdown
[See details](../economics/roi-analysis.html#calculation-methods)
```

Reason: Quarto converts `.qmd` to appropriate format (HTML/PDF/EPUB). Using `.html` breaks PDF and EPUB outputs.

## File Structure

### Frontmatter (Required)

Every QMD file needs YAML frontmatter:

```yaml
---
title: "Chapter Title"
description: "Brief description for metadata"
---
```

### Sections

- Use `#` for chapter titles (H1)
- Use `##` for main sections (H2)
- Use `###` for subsections (H3)
- Don't skip heading levels

### References

- Use Chicago-style citations: `[@citation-key]`
- Bibliography defined in `references.bib`
- Citations auto-format based on CSL file

## Figures and Images

### Creating Figures

Prefer generating figures from code when possible:

```markdown
::: {#fig-roi-analysis}
![](../assets/figures/roi-analysis.png)

Caption explaining the figure in detail
:::
```

### Figure Best Practices

1. Always include descriptive captions
2. Use labels for cross-referencing: `@fig-roi-analysis`
3. Store images in `assets/figures/` or chapter-specific folders
4. Render and review output images after modifications

## Tables

Use Quarto's markdown table syntax:

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

: Table caption {#tbl-id}
```

Reference with `@tbl-id`.

## Common Formatting

### Lists

- Use `-` for unordered lists
- Use `1.` for ordered lists (auto-numbers)
- Maintain consistent indentation

### Emphasis

- *Italic* for emphasis: `*text*`
- **Bold** for strong emphasis: `**text**`
- `Code` for technical terms: `` `text` ``

### Code Blocks

````markdown
```python
# Python code example
```
````

Specify language for syntax highlighting.

## Validation Before Committing

1. Check all variables render: `quarto preview`
2. Verify links work (especially for PDF/EPUB)
3. Run linters: `npm run lint:qmd`
4. Check for hardcoded numbers: `npm run audit-hardcoded`
5. Review rendered output for errors

## Update Related Files

When adding/removing chapters:
- Update `_quarto-book.yml` with chapter order
- Update `OUTLINE.md` to reflect structure
- Update `TODO.md` if marking tasks complete

## Content Review Checklist

Before finalizing content:
- [ ] No hardcoded numbers (use variables)
- [ ] All links use `.qmd` extensions
- [ ] Figures have descriptive captions
- [ ] References properly cited
- [ ] Tone matches style guide
- [ ] Jargon explained or avoided
- [ ] Concise and clear writing
- [ ] Actionable and instructional
