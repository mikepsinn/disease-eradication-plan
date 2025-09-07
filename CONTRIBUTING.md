---
title: How to Contribute
description: 'The single source of truth for all contribution guidelines, style guides, and project standards for the Decentralized Institutes of Health (DIH) wiki.'
published: true
date: '2025-09-07T00:00:00.000Z'
tags: [contributing, guidelines, standards, open-source]
editor: markdown
dateCreated: '2025-02-12T16:51:44.377Z'
---
# How to Contribute to the DIH Wiki

Thank you for your interest in contributing. This document defines repo‑wide contribution rules, structure, and workflows. By participating in this project, you agree to abide by the terms outlined here and in our [**Code of Conduct**](./CODE_OF_CONDUCT.md).

## Core Principles

This wiki documents the "War on Disease," a mission to make curing people more profitable than killing them. Our communication style is a deliberate departure from standard corporate and non-profit communication. It is designed to be memorable, persuasive, and cut through the noise.

- **Primary Framing:** "Make curing people more profitable than killing them." / "Bribe our way to a better world."
- **Secondary Framing:** "Make peace more profitable than war." / "Capture the peace dividend."
- **Be Concise and Direct:** Use short sentences, simple words, and powerful language. Do not state the obvious.
- **Speak Plainly:** Avoid weak corporate euphemisms and "AI slop." Write like a human.
- **Quantify Everything:** Moral arguments are weak without data. All claims must be backed by numbers and citations.

## Contributor Workflow

1.  **Find an Issue or Propose a Change:** Start by looking at our existing [issues](https://github.com/decentralized-institutes-of-health/decentralized-institutes-of-health/issues) or proposing a new change by creating one. For major reorganizations, open a short RFC in the PR description.
2.  **Fork & Branch:** Fork the repository and create a new, descriptive branch for your contribution (e.g., `feat/add-dih-treasury-model` or `fix/correct-roadmap-dates`).
3.  **Make Your Changes:** As you work, please adhere to all standards in this document.
4.  **Submit a Pull Request:** Use the [pull request template](../.github/pull_request_template.md) to submit your changes. Ensure your PR description is clear and links to the relevant issue.

## Content and Style Standards

### 1. Information Architecture (What Goes Where)

- **Strategy:** Treaty/DIH strategy, playbooks, roadmaps -> `strategy/`
- **Features:** dFDA platform specs, technical roadmaps, treasury architecture -> `features/`
- **Economic Models:** Fundraising, tokenomics, ROI models -> `economic-models/`
- **Regulatory:** Legal analysis, compliance, model acts -> `regulatory/`
- **Reference:** Citations, datasets, appendices -> `reference/`
- **Operations:** SOPs, security, processes -> `operations/`
- **Community:** Partners, templates, outreach -> `community/`

**Rule:** Do not create deep folder trees. Keep files within one of these top-level folders and use cross-links for content that spans domains.

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

### 5. Naming, Linking, and Formatting

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Dollar Sign Escaping:** Always escape dollar signs (`\$`) in regular text to prevent rendering issues (e.g., `\$27B`). Do not escape them inside backticked code blocks.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing or if multiple canonicals exist for the same `topic_id`.

