---
title: Content Review Process
description: "The systematic process for reviewing and ensuring the quality of content in the DIH knowledge base."
tags: [review, process, contributing, quality-assurance]
---

# Systematic Content Review Process

This document outlines the systematic process for reviewing and ensuring the quality of all content in the DIH knowledge base.

**See also:**

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Overall contribution workflow and standards

---

To ensure every chapter meets the project's quality standards, we use a systematic audit process. Instead of a central checklist, the review status is tracked directly within each file's frontmatter using the `lastReviewed` property.

## The Audit Workflow

1.  **Find a Chapter to Review:** Identify a chapter that has no `lastReviewed` date or has one that is significantly out of date.
2.  **Perform the Audit:** Review the chapter against the 5-point checklist below.
3.  **Fix and Document:** Correct issues directly. For larger tasks (e.g., creating a new chart or sourcing a difficult claim), add a `TODO` comment in the file (e.g., `<!-- TODO: Add a chart here showing X vs. Y. -->`).
4.  **Update Frontmatter:** Once the chapter is fully audited and improved, update the `lastReviewed` date in the frontmatter to the current date (e.g., `lastReviewed: "YYYY-MM-DD"`).

## The Chapter Audit Checklist

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
- **Formatting:** Does each sentence start on a new line?
