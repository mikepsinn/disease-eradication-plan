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
- **Tell a Compelling Story:** This is not just a plan; it's a movement. Use the "chapters" to build a powerful narrative:
    -   `problem.md` should graphically and emotionally depict the human cost of war and disease. It must build urgency.
    -   `solution.md` should paint a vivid, hopeful picture of the future we are building—a world without war and disease. It must inspire.

## Contributor Workflow

The plan *is* the repository. Our goal is to create a single source of truth that is so clear it can be read like a book.

1.  **Identify an Area for Improvement:** Find a "chapter" (a file in the root directory like `problem.md`) or an "appendix" (a file in a subdirectory) that is incomplete, unclear, or could be improved. The highest-priority areas are outlined in the main `roadmap.md`.
2.  **Suggest an Edit (Propose a Change):** This project uses a standard Git workflow.
    *   **For Git Users:** Fork the repository and create a new, descriptive branch for your contribution (e.g., `update-financial-model` or `clarify-legal-framework`).
    *   **For Non-Technical Users:** You can edit files directly through the GitHub web interface, which will handle the process of creating a fork and proposing a change for you.
3.  **Make Your Changes:** As you work, please adhere to all standards in this document. Your goal is to add clarity, detail, and evidence to the "book."
4.  **Submit Your Change for Review:** Propose your changes by opening a "Pull Request." Ensure your description is clear and explains how your change improves the overall narrative.

## Content and Style Standards

### 1. Information Architecture: Chapters, Sections, and The Appendix

This repository is structured as a book. The root directory contains the "Chapters," which tell the core narrative. The subdirectories are "Sections" that provide detailed evidence, models, and plans for their parent chapter. `reference/` is the one true "Appendix" for external, evidentiary material.

**The Golden Rule:** If a topic is an "Epic" that needs more than one file, it gets a main summary file (`epic.md`) and a corresponding directory (`epic/`) for the details. This pattern applies at all levels.

**"The Book" vs. "The Internal Playbook"**

- **The Book (`/`, `economics/`, `strategy/`, `legal/`):** This is the public-facing content. It's the story, the argument, and the evidence. Content here should be written for an external audience.
- **The Internal Playbook (`operations/`):** This is for internal-facing strategy and standard operating procedures (SOPs). This is the "how-to" for running the organization itself. Content here is for the core team.
- **The Appendix (`reference/`):** This is for supporting data, studies, citations, and other third-party reference material that back up claims made in "The Book."

| Section | Content Type | Examples |
|---|---|---|
| `economics/` | Financial models, ROI, investment thesis | `investment-thesis.md`, `peace-dividend-value-capture.md` |
| `strategy/` | Execution plans, political strategy, how-to | `1-percent-treaty.md`, `co-opting-defense-contractors.md` |
| `legal/` | Legal compliance, governance, regulations | `multi-entity-strategy.md`, `right-to-trial-act.md` |
| `operations/` | Team structure, hiring, internal processes | `hiring-plan.md`, `crypto-intake-sop.md` |
| `reference/` | Data, studies, citations, reference material | `costs-of-war.md`, `recovery-trial.md` |

**Rules for Maintainable Structure:**

1. **Single Responsibility Principle:** One file should do one job and do it well. If a file covers multiple distinct topics, it must be split. When in doubt, split files rather than merge them.

2. **Globally Unique Filenames:** Every filename in the repository must be unique and descriptive. Add context prefixes only when the base filename could realistically exist in multiple directories:
   - ❌ Bad: `economics/fundraising/strategy.md` (too generic)
   - ✅ Good: `economics/fundraising/fundraising-strategy.md` (context needed)
   - ✅ Also Good: `strategy/1-percent-treaty.md` (inherently unique concept)
   
   This ensures every file can be unambiguously referenced with `@filename` while keeping names as simple as possible.

3. **Place new content in the appropriate section.** Only modify root-level chapters to summarize and link to new detailed content.

### 2. Quality Assurance and Actionable TODOs

To maintain a clean and actionable list of improvements, all contributions must be checked against the following standards. We use a specific format for `TODO` comments to flag content that needs citations, stylistic rewrites, clarification, or visual aids.

**1. Internal Link Integrity:**
   - Before submitting, scan the file for all internal relative links (e.g., `[text](./path/file.md)`).
   - **You MUST FIX** any links that are broken.
   - If a link points to a deleted file, either remove the link or repoint it to a relevant alternative.

**2. Content Quality Triage (TODOs):**
   - **Placement:** Place `TODO`s in the most relevant location **inside the body of the text**. If a `TODO` applies to the entire document, place it at the **very bottom**. NEVER place `TODO`s at the top of a file or in the frontmatter.
   - **Formatting:** Use machine-readable comments so they can be easily aggregated into a project-wide "content debt" list.
     - `<!-- TODO: Add citation for this claim. -->`
     - `<!-- TODO: Rewrite this section to match project writing style. -->`
     - `<!-- TODO: Add a visual (chart, image) to clarify this section. -->`
     - `<!-- TODO: Expand this section to include X. -->`

### 3. Frontmatter Requirements

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

### 4. Sourcing and Citation Standard (CRITICAL)

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

### 5. Technical Standards

- **Tooling and Server-Side Code:** Any new tooling or server-side components for the project (e.g., MCP servers, automation scripts) **MUST** be written in TypeScript.
- **Dependencies:** Use `npm` for package management. All projects must include a `package.json` file with clearly defined dependencies.
- **Execution:** To avoid committing compiled code, run TypeScript files directly using a runtime like `ts-node` or `tsx`. Compiled JavaScript files (`.js`) are disallowed in the repository and should be added to the project's `.gitignore` file.

### 6. Naming, Linking, and Formatting

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Dollar Sign Escaping:** Always escape dollar signs (`\$`) in regular text to prevent rendering issues (e.g., `\$27B`). Do not escape them inside backticked code blocks.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing.

