---
title: How to Contribute
description: "The single source of truth for all contribution guidelines, style guides, and project standards for the Decentralized Institutes of Health (DIH) knowledge base."
published: true
date: "2025-09-09T00:00:00.000Z"
tags: [contributing, guidelines, standards, book, knowledge-base]
editor: markdown
dateCreated: "2025-09-09T00:00:00.000Z"
---

# How to Contribute to the DIH Knowledge Base

## Table of Contents
- [Core Principles](#core-principles)
- [Writing Style Guide](#writing-style-guide)
- [Contributor Workflow](#contributor-workflow)
- [Content and Style Standards](#content-and-style-standards)
  - [1. Information Architecture: Chapters, Sections, and The Appendix](#1-information-architecture-chapters-sections-and-the-appendix)
  - [2. Quality Assurance and Actionable TODOs](#2-quality-assurance-and-actionable-todos)
  - [3. Frontmatter Requirements](#3-frontmatter-requirements)
  - [4. Sourcing and Citation Standard (CRITICAL)](#4-sourcing-and-citation-standard-critical)
  - [5. Technical Standards](#5-technical-standards)
  - [6. Naming, Linking, and Formatting](#6-naming-linking-and-formatting)
- [Automation and CI](#automation-and-ci)

Thank you for your interest in contributing to a plan that could save millions of lives. This document defines the contribution rules, structure, and workflows for this knowledge base. 

We're here because humanity spends 40X more on weapons than on curing diseases. While millions die from preventable illnesses, we waste trillions on the capacity to kill each other. This is not a normal business plan—it's an attempt to fix the most grotesque misallocation of resources in human history.

By participating, you agree to abide by the terms outlined here.

## Core Principles

This repository documents the "War on Disease," a mission to make curing people more profitable than killing them. It is structured as a book that can be read from start to finish. Our communication style is designed to be memorable, persuasive, and cut through the noise.

- **Primary Framing:** "Make curing people more profitable than killing them." / "Bribe our way to a better world."
- **Secondary Framing:** "Make peace more profitable than war." / "Capture the peace dividend."
- **Anchor in Public Choice Theory:** All strategic arguments must be framed through the lens of public choice theory. Assume that all actors (politicians, corporate leaders, voters) act in their own rational self-interest. Avoid arguments based on abstract "national interests" and instead focus on the specific, concrete incentives that drive individual decision-makers.
- **Be Specific About the Goal:** Avoid generic phrases like "saving the world." Our objective is specific and measurable: to redirect 1% of global military spending toward curing disease. Frame the mission in these concrete terms, as the first step toward the complete eradication of war and disease. If you need shorthand for the goal say "End War and Disease" instead of "Save the World" or such nonsense
- **Identify the Incentive Gaps:** Frame the _problem_ not as a moral failure, but as a system with flawed incentives. The status quo is a rational response by individuals to a system that rewards rent-seeking and concentrates benefits for a few while diffusing costs to the many.
- **Engineer a Better Deal:** Frame the _solution_ as an exercise in incentive engineering. The goal is to create a new system with a superior set of **concentrated benefits** for a broader coalition of key actors. Always answer the question: "What's in it for them, personally and professionally?"
- **Co-Opt, Don't Fight:** Acknowledge that powerful interest groups exist. The strategy is not to destroy them but to make it more profitable for them to support our goals than to oppose them. This is "politics as exchange."
- **Be Concise and Direct:** Use short sentences, simple words, and powerful language.
- **Speak Plainly:** Avoid weak corporate euphemisms. Write like a human.
- **Quantify Everything:** All claims must be backed by data and citations.
- **Tell a Compelling Story:** This is not just a plan; it's a movement. Use the "chapters" to build a powerful narrative:
  - `problem.md` should graphically and emotionally depict the human cost of war and disease. It must build urgency.
  - `solution.md` should paint a vivid, hopeful picture of the future we are building—a world without war and disease. It must inspire.

## Writing Style Guide

**The 4 Core Checks:**
1. **Clarity:** Can I say this to my mom and have her understand?
2. **Credibility:** Would I stake my reputation on this claim?
3. **Concision:** Can I cut words without losing meaning?
4. **Humanity:** Does this sound like Kurt Vonnegut wrote it?

**Automatic Red Flags (Rewrite Immediately):**
- **Superlatives:** "world-class," "revolutionary," "unprecedented"
- **Buzzwords:** "synergy," "activation," "paradigm shift", "stakeholder"
- **Trying to sound important:** Write like you're explaining this to a smart friend who thinks you might be crazy

**Gold Standard Test:** Would Warren Buffett write this sentence?
- Clear enough for anyone
- Backed by facts
- No salesy drama
- Respectful of reader's intelligence

**Voice and Tone: Principled, Blunt, and Credible**

**The Target and the Tone: Aim at the System, Speak to the "Us"**

The style of this project must balance two core principles: genuine outrage and radical inclusivity.

1.  **The Target of Outrage is the System, Not the People:** Our fight is with broken systems, not with the individuals trapped within them. The tone should be one of profound anger at the inefficiency, waste, and tragedy of our current institutions. It should not be a partisan or personal attack on any group. The goal is to critique a broken machine that *we* can all work together to fix.

2.  **The Tone is Radically Inclusive:** The writing should always assume the reader is a potential partner and a co-owner of the project. It should use inclusive language ("we," "us," "our") to create a sense of a massive, collective movement that includes all of humanity. The goal is to make the reader feel like they are being invited to join a powerful rebellion, not being lectured or sold to. The reader is part of the "us" from the first sentence.

- **Write from a place of genuine outrage.** If you're not angry that we waste trillions on weapons while millions die from preventable diseases, you shouldn't be writing this.
  - **Good:** "The Pentagon loses more money in accounting errors than we spend trying to cure cancer. This is insane."
  - **Bad:** "We're revolutionizing the paradigm to create world-class solutions for the unprecedented global health crisis."
- **Assume self-interest, not idealism.** Ground every argument in Public Choice Theory.
  - **Good:** "Politicians support this because we fund their campaigns and their opponents if they don't."
  - **Bad:** "World leaders will embrace this plan because it's the right thing to do."
- **Use blunt language, not euphemisms.** Call things by their real names, but maintain technical precision where it adds clarity.
  - **Good:** "How to stay out of prison," "We're bribing everyone."
  - **Bad:** "Legal compliance," "Incentive alignment."
  - **Good and Precise:** "Transparent, automated, outcome-driven institutions" is better than "computer systems" because it specifies *what kind* of systems and *why* they matter.

**One-Second Test:** If you hesitate before reading a sentence aloud to a skeptical audience, rewrite it.

## Contributor Workflow

The plan _is_ the repository. Our goal is to create a single source of truth that is so clear it can be read like a book.

1.  **Identify an Area for Improvement:** Find a "chapter" (a file in the root directory like `problem.md`) or an "appendix" (a file in a subdirectory) that is incomplete, unclear, or could be improved. The highest-priority areas are outlined in the main `roadmap.md`.
2.  **Suggest an Edit (Propose a Change):** This project uses a standard Git workflow.
    - **For Git Users:** Fork the repository and create a new, descriptive branch for your contribution (e.g., `update-financial-model` or `clarify-legal-framework`).
    - **For Non-Technical Users:** You can edit files directly through the GitHub web interface, which will handle the process of creating a fork and proposing a change for you.
3.  **Make Your Changes:** As you work, please adhere to all standards in this document. Your goal is to add clarity, detail, and evidence to the "book."
4.  **Submit Your Change for Review:** Propose your changes by opening a "Pull Request." Ensure your description is clear and explains how your change improves the overall narrative.

## Content and Style Standards

### 1. Information Architecture: Chapters, Sections, and The Appendix

This repository is structured as a book. The root directory contains the "Chapters," which tell the core narrative. The subdirectories are "Sections" that provide detailed evidence, models, and plans for their parent chapter. `reference/` is the one true "Appendix" for external, evidentiary material.

**Note:** The file `brain/book/index.md` is automatically generated from the frontmatter of all files in the brain/book directory. Do not edit it directly - instead, update the frontmatter in the individual chapter and section files.

#### Epic Folders

**The Golden Rule:** If a topic is an "Epic" that needs more than one file, it gets a main summary file (`epic.md`) and a corresponding directory (`epic/`) for the details. This pattern applies at all levels.

**"The Book" vs. "The Internal Playbook"**

- **The Book (`/`, `economics/`, `strategy/`, `legal/`):** This is the public-facing content. It's the story, the argument, and the evidence. Content here should be written for an external audience.
- **The Internal Playbook (`operations/`):** This is for internal-facing strategy and standard operating procedures (SOPs). This is the "how-to" for running the organization itself. Content here is for the core team.
- **The Appendix (`reference/`):** This is for supporting data, studies, citations, and other third-party reference material that back up claims made in "The Book."

| Section       | Content Type                                 | Examples                                                  |
| ------------- | -------------------------------------------- | --------------------------------------------------------- |
| `economics/`  | Financial models, ROI, investment thesis     | `investment-thesis.md`, `peace-dividend-value-capture.md` |
| `solution/`   | Core components of the proposed solution     | `1-percent-treaty.md`, `dih.md`, `dfda.md`                |
| `strategy/`   | Execution plans, political strategy, how-to  | `co-opting-defense-contractors.md`, `global-referendum.md` |
| `legal/`      | Legal compliance, governance, regulations    | `multi-entity-strategy.md`, `right-to-trial-act.md`       |
| `operations/` | Team structure, hiring, internal processes   | `hiring-plan.md`, `crypto-intake-sop.md`                  |
| `reference/`  | Data, studies, citations, reference material | `costs-of-war.md`, `recovery-trial.md`                    |

**Rules for Maintainable Structure:**

1. **Single Responsibility Principle:** One file should do one job and do it well. If a file covers multiple distinct topics, it must be split. When in doubt, split files rather than merge them.

2. **Globally Unique Filenames:** Every filename in the repository must be unique and descriptive. Add context prefixes only when the base filename could realistically exist in multiple directories:
   - ❌ Bad: `economics/fundraising/strategy.md` (too generic)
   - ✅ Good: `economics/fundraising/fundraising-strategy.md` (context needed)
   - ✅ Also Good: `solution/1-percent-treaty.md` (inherently unique concept)

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
date: "YYYY-MM-DDTHH:MM:SS.sssZ" # The publication or last significant update date
tags: [keyword1, keyword2] # A list of relevant tags/keywords
editor: markdown # Should always be markdown
dateCreated: "YYYY-MM-DDTHH:MM:SS.sssZ" # The date the file was first created
---
```

### 4. Sourcing and Citation Standard (CRITICAL)

**MANDATORY**: ALL factual claims, statistics, and figures **MUST** be cited with hyperlinks to authoritative sources using the centralized reference system described below.

#### Central References File

All references are consolidated in `brain/book/references.md` to avoid duplication and maintain consistency across the knowledge base.

1.  **Find a High-Quality Source:** Use reputable sources like academic journals, government reports, or major news outlets.

2.  **Check for Existing References:** Before adding a new reference, search `brain/book/references.md` to see if it already exists. If it does, use the existing anchor ID.

3.  **Link Claims Directly to References:** In your content, hyperlink the relevant text directly to the specific reference in the central file.
    - **Example:** `...global military spending reached [$2.443 trillion](./references.md#global-spending-2023)...`
    - **Example:** `[The world spends 40 times more on military force](./references.md#sipri-2024-spending) than on [medical research](./references.md#global-gov-med-research-spending).`

4.  **Add New References (If Needed):** If your source doesn't exist in the central file, add it following this format:

      ```markdown
      <a id="unique-anchor-id"></a>

      - **Brief descriptive title**

        > "Direct quote from the source with key statistics or claims..."
        > — Source Name, Date, [Link Title](URL)
      ```

5.  **Use Descriptive Anchor IDs:** Create meaningful anchor IDs that describe the content (e.g., `sipri-2024-spending`, `recovery-cost-500`, `fossil-fuel-subsidies`).

#### Maintainability

-   **Use a Single, Alphabetized List:** To ensure `references.md` is easy to navigate and free of duplicates, all reference items **MUST** be in a single, flat list sorted alphabetically by their descriptive title. **Do not use subsections or headings.** To avoid clutter, you may group closely related statistics (e.g., multiple years of the same report) under a single alphabetized item.

#### What NOT to Do

- **Do not create local "Source Quotes" sections** in individual files
- **Do not duplicate references** that already exist in the central file  
- **Do not use generic link text** like "(Source)" - hyperlink the actual claim text
- **Do not create internal anchor links** within individual files for citations

This centralized approach prevents link rot, eliminates duplicate references, and creates a single source of truth for all factual claims across the knowledge base.

### 5. Technical Standards

- **Tooling and Server-Side Code:** Any new tooling or server-side components for the project (e.g., MCP servers, automation scripts) **MUST** be written in TypeScript.
- **Dependencies:** Use `npm` for package management. All projects must include a `package.json` file with clearly defined dependencies.
- **Execution:** To avoid committing compiled code, run TypeScript files directly using a runtime like `ts-node` or `tsx`. Compiled JavaScript files (`.js`) are disallowed in the repository and should be added to the project's `.gitignore` file.

### 6. Naming, Linking, and Formatting

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Dollar Sign Escaping:** Always escape dollar signs (`\$`) in regular text to prevent rendering issues (e.g., `\$27B`). Do not escape them inside backticked code blocks.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.
- **Sentence Structure:** Each sentence must start on a new line. This makes diffs cleaner, editing easier, and git blame more useful. Break after every period, question mark, or exclamation point.

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing.
