---
title: How to Contribute
description: 'The single source of truth for all contribution guidelines, style guides, and project standards for the Decentralized Institutes of Health (DIH) knowledge base.'
published: true
date: '2025-09-09T00:00:00.000Z'
tags: [contributing, guidelines, standards, book, knowledge-base]
editor: markdown
dateCreated: '2025-09-09T00:00:00.000Z'
---
# How to Contribute to the DIH Knowledge Base

Thank you for your interest in contributing. This document defines the contribution rules, structure, and workflows for this knowledge base. By participating, you agree to abide by the terms outlined here.

## Core Principles

This repository documents the "War on Disease," a mission to make curing people more profitable than killing them. It is structured as a book that can be read from start to finish. Our communication style is designed to be memorable, persuasive, and cut through the noise.

- **Primary Framing:** "Make curing people more profitable than killing them." / "Bribe our way to a better world."
- **Secondary Framing:** "Make peace more profitable than war." / "Capture the peace dividend."
- **Be Concise and Direct:** Use short sentences, simple words, and powerful language.
- **Speak Plainly:** Avoid weak corporate euphemisms. Write like a human.
- **Quantify Everything:** All claims must be backed by data and citations.

## Contributor Workflow

The plan *is* the repository. Our goal is to create a single source of truth that is so clear it can be read like a book.

1.  **Identify an Area for Improvement:** Find a "chapter" (a file in the root directory like `problem.md`) or an "appendix" (a file in a subdirectory) that is incomplete, unclear, or could be improved. The highest-priority areas are outlined in the main `roadmap.md`.
2.  **Suggest an Edit (Propose a Change):** This project uses a standard Git workflow.
    *   **For Git Users:** Fork the repository and create a new, descriptive branch for your contribution (e.g., `update-financial-model` or `clarify-legal-framework`).
    *   **For Non-Technical Users:** You can edit files directly through the GitHub web interface, which will handle the process of creating a fork and proposing a change for you.
3.  **Make Your Changes:** As you work, please adhere to all standards in this document. Your goal is to add clarity, detail, and evidence to the "book."
4.  **Submit Your Change for Review:** Propose your changes by opening a "Pull Request." Ensure your description is clear and explains how your change improves the overall narrative.

## Content and Style Standards

### 1. Information Architecture: The "Book & Appendices" Model

This repository is structured as a book. The root directory contains the "Chapters," which tell the core narrative. The subdirectories are the "Appendices," which provide the detailed evidence, models, and plans.

**The Golden Rule:** If a topic is an "Epic" that needs more than one file, it gets a main summary file (`epic.md`) and a corresponding directory (`epic/`) for the details. This pattern applies at all levels.

- **Root Chapters:** `problem.md`, `solution.md`, `economics.md`, `strategy.md`, etc. These are narrative summaries that should be kept concise and link to the appendices for details.
- **`economics/`:** The appendix for all financial models, ROI calculations, and investment theses.
- **`strategy/`:** The appendix for all external-facing execution plans (e.g., how we win the referendum).
- **`legal/`:** The appendix for all binding rules, compliance frameworks, and governance models.
- **`operations/`:** The appendix for all internal-facing processes for running the organization (e.g., hiring, SOPs).
- **`reference/`:** The appendix for all supporting data, studies, and third-party evidence.

**Rule:** Place new content in the appropriate appendix. Only modify root-level chapters to summarize and link to new detailed content in the appendices.

### 2. Frontmatter Requirements

All Markdown files **MUST** begin with a YAML frontmatter block. Our frontmatter is designed for compatibility with [Wiki.js](https://js.wiki/). Please adhere to the following structure:

```yaml
---
title: "A Clear and Descriptive Title for the Page"
description: "A brief, one-sentence summary of the page's content. Used in search results. (Max 140 characters)"
published: true # Set to 'false' for drafts
date: 'YYYY-MM-DDTHH:MM:SS.sssZ' # The publication or last significant update date
tags: [keyword1, keyword2] # A list of relevant tags/keywords
editor: markdown # Should always be markdown
dateCreated: 'YYYY-MM-DDTHH:MM:SS.sssZ' # The date the file was first created
---
```

### 3. Sourcing and Citation Standard (CRITICAL)

**MANDATORY**: ALL factual claims, statistics, and figures **MUST** be cited with hyperlinks to authoritative sources using the anchor-based method described below.

1.  **Find a High-Quality Source:** Use reputable sources like academic journals, government reports, or major news outlets.
2.  **Create an Anchor Link in the Text:** In the body of the text, link your claim to a unique anchor ID.
    -   **Example:** `...global military spending reached [$2.443 trillion](#global-spending-2023)...`
3.  **Add a Source Quote Section:** At the end of the file, create a section titled `## Source Quotes` if one does not exist.
4.  **Add the Full Citation:** In the source section, create the anchor and add the full quote and link.
    -   **Example:**
        ```markdown
        <a id="global-spending-2023"></a>
        * **Global military spending reached $2.443 trillion**
          > "World military expenditure reached an all-time high of $2443 billion in 2023..."
          > — SIPRI, April 2024, [URL](https://www.sipri.org/media/press-release/2024/world-military-expenditure-surges-amid-war-rising-tensions-and-insecurity)
        ```

This pattern is mandatory to prevent link rot, provide immediate context, and keep readers on-page.

### 4. Technical Standards

- **Tooling and Server-Side Code:** Any new tooling or server-side components for the project (e.g., MCP servers, automation scripts) **MUST** be written in TypeScript.
- **Dependencies:** Use `npm` for package management. All projects must include a `package.json` file with clearly defined dependencies.
- **Execution:** To avoid committing compiled code, run TypeScript files directly using a runtime like `ts-node` or `tsx`. Compiled JavaScript files (`.js`) are disallowed in the repository and should be added to the project's `.gitignore` file.

### 5. Naming, Linking, and Formatting

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Dollar Sign Escaping:** Always escape dollar signs (`\$`) in regular text to prevent rendering issues (e.g., `\$27B`). Do not escape them inside backticked code blocks.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing.

