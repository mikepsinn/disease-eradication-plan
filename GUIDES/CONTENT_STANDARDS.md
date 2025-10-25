---
title: Content and Formatting Standards
description: "Unified content, structural, and formatting standards for the Complete Idiot's Guide to Ending War and Disease."
tags: [standards, contributing, content, style, review, process, quality-assurance, formatting]
---

# Content and Formatting Standards

**See also:**

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Overall contribution workflow and standards

---

## 1. Information Architecture: Chapters, Sections, and The Appendix

This repo is structured like a book. Root files are "chapters." Subdirectories are "sections" with the details. `reference/` is the appendix.

**IMPORTANT:** The [Book Outline in README.md](../README.md#book-outline) is the authoritative writing checklist. Before adding new topics or changing the book architecture, update the Book Outline first. This prevents topic creep and maintains narrative flow. Remember: the outline is comprehensive for writing purposes - the final book will consolidate many items into cohesive chapters.

**Note:** Don't edit `brain/book/index.md` directly - it's auto-generated from frontmatter.

## 2. Quality Assurance and Actionable TODOs

To ensure all unfinished work is tracked and easily searchable, please add a `TODO` comment directly in the file at the location where work is needed. This allows any contributor to find actionable tasks by simply searching the entire project for "TODO".

- **Where:** Put `TODO`s where the problem is. Document-wide TODOs go at the bottom of the file. Never at the top.
- **Format:** Use comments so we can find them all later:
  - `<!-- TODO: Add citation for this claim. -->`
  - `<!-- TODO: Rewrite this section. -->`
  - `<!-- TODO: Add a chart here. -->`
  - `<!-- TODO: Expand this section. -->`

**Internal Link Integrity:** Before submitting, you **MUST FIX** any broken links in your changed files. Scan for all internal relative links (e.g., `[text](./path/file.md)`). If a link points to a deleted file, either remove the link or repoint it to a relevant alternative. This is a critical pre-submission check, not a task to be marked with a `TODO`.

## 3. Frontmatter Requirements

Every markdown file needs this header. These fields are essential for our automated review and maintenance scripts.

```yaml
---
title: "A Clear and Descriptive Title"
description: "One sentence summary (max 140 chars)"
published: true # false for drafts
date: "YYYY-MM-DDTHH:MM:SS.sssZ" # Last modified date, managed by script
tags: [keyword1, keyword2]
lastFormatted: "YYYY-MM-DD"
lastStyleCheck: "YYYY-MM-DD"
lastFactCheck: "YYYY-MM-DD"
lastLinkCheck: "YYYY-MM-DD"
lastFigureCheck: "YYYY-MM-DD"
---
```

## 4. Sourcing and Citation Standard (CRITICAL)

**Every claim needs a source.** All source quotes go in `brain/book/references.qmd`.

1. Check if your source is already there
2. If yes, link to it: `[your claim](./references.qmd#anchor-id)`
3. If no, add it using the format you see in that file

Example in-text: `[The world spends 40x more on war](./references.qmd#sipri-2024) than on [curing disease](./references.qmd#med-research-funding).`

## 5. Naming and Linking

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.

## 6. Chapter Independence and Reusability

**IMPORTANT: QMD files must be reusable across different contexts.**

- **No "Next Chapter" sections:** Don't add "Next Chapter", "Turn the page", or similar navigation at the end of chapters
- **No hardcoded navigation:** Chapters should be self-contained without assuming a specific reading order
- **No context-specific references:** Avoid "as we saw in the previous chapter" or similar cross-references
- **Why:** These QMD files are reused in the website, presentations, and different book versions with different orderings

## 7. Chapter Heading Standard

**IMPORTANT: Chapters must not start with a redundant heading.**

- **No "Introduction" Headings:** Do not start a chapter with `## Introduction` or similar variations. The chapter's content should begin immediately after the frontmatter.
- **No Title Repetition:** Do not repeat the chapter's title (from the frontmatter `title:` field) as the first heading in the document. The title and description are automatically displayed by the publishing system.
- **Why:** The title and description are displayed prominently above the chapter's content. Adding a heading that repeats this information is redundant and creates a poor reading experience.

**Correct Example:**
```markdown
---
title: "The Peace Dividend"
description: "How redirecting military spending can generate a massive societal return."
---

The 1% Treaty proposes redirecting a small fraction of global military expenditure...
```

**Incorrect Example:**
```markdown
---
title: "The Peace Dividend"
description: "How redirecting military spending can generate a massive societal return."
---

## Introduction

The 1% Treaty proposes redirecting a small fraction of global military expenditure...
```

## 8. Automated Formatting Standards

The following objective formatting rules are enforced by an automated script. While you should strive to follow them, the script will automatically correct any deviations.

1.  **Sentence Structure:** Each sentence must start on a new line.
2.  **Blank Line After Bold Text:** Bold text (e.g., `**Bold text**`) at the end of a line MUST be followed by a blank line to ensure proper paragraph separation in rendered output.
3.  **Blank Line After Quoted Text:** Quoted text (e.g., `"Quote"`) at the end of a line MUST be followed by a blank line to ensure proper rendering.
4.  **List Spacing:** Ensure all markdown lists are preceded by a blank line.
5.  **Math Formatting:** Enclose all inline mathematical formulas in single dollar signs (`$...$`) and block-level formulas in double dollar signs (`$$...$$`) for proper LaTeX rendering.
6.  **Preserve Quarto Syntax:** All Quarto syntax must be preserved *exactly*. This includes:
    *   Code blocks with curly braces: ````{python}`
    *   Special comments: `#| label: my-label`
    *   Shortcodes: `{{< include ... >}}`
7.  **Preserve Markdown:** All standard markdown (headers, tables, etc.) must be preserved.

## 9. Systematic Content Review Process

To ensure every chapter meets the project's quality standards, we use a systematic audit process. Instead of a central checklist, the review status is tracked directly within each file's frontmatter using the `lastReviewed` property.

### The Audit Workflow

1.  **Find a Chapter to Review:** Identify a chapter that has no `lastReviewed` date or has one that is significantly out of date.
2.  **Perform the Audit:** Review the chapter against the 5-point checklist below.
3.  **Fix and Document:** Correct issues directly. For larger tasks (e.g., creating a new chart or sourcing a difficult claim), add a `TODO` comment in the file (e.g., `<!-- TODO: Add a chart here showing X vs. Y. -->`).
4.  **Update Frontmatter:** Once the chapter is fully audited and improved, update the `lastReviewed` date in the frontmatter to the current date (e.g., `lastReviewed: "YYYY-MM-DD"`).

### The Chapter Audit Checklist

Use these five checks to audit every chapter file.

**1. Content & Narrative Flow:**

- **Completeness:** Does the chapter deliver on its promise from the master `OUTLINE.MD`? Is any critical information missing?
- **Conciseness:** Is there redundant content already covered elsewhere? Can anything be cut to make the argument stronger?
- **Independence:** Does the chapter avoid phrases like "in the previous chapter," ensuring it can be reused in different contexts?

**2. Tone & Voice (per `STYLE_GUIDE.md`):**

- **Instructional Tone:** Does it read like a DIY manual ("Here's how you...") rather than a sales pitch ("Our solution will...")?
- **Voice Consistency:** Does it maintain the "dark humor meets practical hope" tone?
- **Word Choice:** Does it avoid corporate buzzwords, academic jargon, and euphemisms?

**3. Sourcing & Credibility:**

- **Universal Citation:** Is every claim, number, and statistic backed by an inline citation to `brain/book/references.qmd`?
- **Source Verification:** Have you personally checked that the source exists, is valid, and actually supports the claim being made?

**4. Visuals & Data (per `DESIGN_GUIDE.md`):**

- **Opportunity:** Could the argument be made stronger with a chart, diagram, or illustration?
- **Clarity:** Is data presented in the most effective, honest, and minimalist way possible?

**5. Technical & Structural Integrity:**

- **Frontmatter:** Does the file have a complete and accurate YAML frontmatter block?
- **Link Integrity:** Are all internal links (`[link](./path/to/file.md)`) valid and pointing to existing files?
- **Formatting:** Does the file adhere to the automated formatting standards?
- **Heading Standard:** Does the chapter avoid starting with a redundant "Introduction" or title-like heading?
