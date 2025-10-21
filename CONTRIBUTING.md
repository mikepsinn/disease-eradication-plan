---
title: How to Contribute
description: "The single source of truth for all contribution guidelines, style guides, and project standards for the Decentralized Institutes of Health (DIH) knowledge base."
published: true
tags: [contributing, guidelines, standards, book, knowledge-base]
---

# How to Contribute to the DIH Knowledge Base

This document provides a central overview of the contribution process. For detailed standards, please refer to our specialized guides:

- **[Writing Style Guide](./GUIDES/STYLE_GUIDE.md)**: Tone, voice, and prose style.
- **[Design Guide](./GUIDES/DESIGN_GUIDE.md)**: Visual standards for charts and diagrams.
- **[Technical Guide](./GUIDES/TECHNICAL_GUIDE.md)**: Development setup and technical standards.

**Table of Contents**

- [Core Principles](#core-principles)
- [Contributor Workflow](#contributor-workflow)
- [Content and Style Standards](#content-and-style-standards)
- [Automation and CI](#automation-and-ci)

## Core Principles

This repository documents "The Complete Idiot's Guide to Ending War and Disease," a book about getting every nation to sign the **1% Treaty** to redirect 1% of military spending to cure diseases instead of cause them. The plan involves creating a **Wishocratically governed** (using randomized pairwise preference allocations where everyone divides budget allocations between random pairs of priorities) global **Decentralized Institutes of Health (DIH)** that subsidizes patient participation in **80X more efficient decentralized pragmatic clinical trials**. All data flows through the **Decentralized FDA (dFDA)** which provides **Outcome Labels** for every food and drug, plus personalized treatment effectiveness rankings for all diseases.

- **Primary Focus:** The unnecessary suffering and death from war (14M deaths/year) and disease (55M deaths/year). Every year we lose 69 million lives that could be saved.
- **The Problem:** We spend $119 trillion annually on war and disease while investing just 0.06% of that on finding cures. Children die of rare diseases while we build nuclear submarines.
- **The Solution:** Redirect just 1% of military spending to medical research through systems that are 80X more efficient than current approaches.
- **The Mission:** Save millions of lives by making curing people more profitable than killing them
- **Core Benefits to Emphasize:** The DIH delivers **80X more efficient medical research** (proven by Oxford RECOVERY trial: $500/patient vs $41,000), tests **1,000X more treatments** with the same budget, uses **economic analysis to minimize DALYs/maximize QALYs**, provides **complete data transparency** (no hidden failures), and enables **100% patient participation** (vs 15% in traditional trials). Focus on OUTCOMES (more cures, faster, cheaper), not mechanisms (patient control, DAOs).
- **Healthcare Integration Model:** The DIH functions as a **clinical trial insurance provider** that works WITHIN existing healthcare infrastructure. Patients pay small copays ($20-50), doctors recommend trials like any treatment, pharmacies dispense trial meds like regular prescriptions. We're NOT "paying patients directly" - we're covering their costs like insurance. This maintains medical ethics while removing financial barriers.
- **Anchor in Public Choice Theory:** All strategic arguments must be framed through the lens of public choice theory. Assume that all actors (politicians, corporate leaders, voters) act in their own rational self-interest. Avoid arguments based on abstract "national interests" and instead focus on the specific, concrete incentives that drive individual decision-makers.
- **Be Specific About the Goal:** Avoid generic phrases like "saving the world." Our objective is specific and measurable: to redirect 1% of global military spending toward curing disease. Frame the mission in these concrete terms, as the first step toward the complete eradication of war and disease. If you need shorthand for the goal say "End War and Disease" instead of "Save the World" or such nonsense
- **Identify the Incentive Gaps:** Frame the _problem_ not as a moral failure, but as a system with flawed incentives. The status quo is a rational response by individuals to a system that rewards rent-seeking and concentrates benefits for a few while diffusing costs to the many.
- **Engineer a Better Deal:** Frame the _solution_ as an exercise in incentive engineering. The goal is to create a new system with a superior set of **concentrated benefits** for a broader coalition of key actors. Always answer the question: "What's in it for them, personally and professionally?"
- **Co-Opt, Control:** Acknowledge that powerful interest groups exist. The strategy is not to destroy them but to make it more profitable for them to support our goals than to oppose them. This is "politics as exchange."
- **Use History Wisely:** Central planning has a documented history of causing unnecessary death (Soviet famines, Great Leap Forward, etc.). Use these examples as evidence that committee-based systems fail in complex domains - but present them as historical lessons, not ideological attacks. Walk readers logically from "committees failed at agriculture" to "committees are failing at medical research." Both Democrats and Republicans can agree that some problems need distributed solutions.
- **Be Concise and Direct:** Use short sentences, simple words, and powerful language.
- **Speak Plainly:** Avoid weak corporate euphemisms. Write like a human.
- **Quantify Everything:** All claims must be backed by data and citations.
- **Tell a Compelling Story:** This is not just a plan; it's a movement. Use the "chapters" to build a powerful narrative:
  - `problem.md` should graphically and emotionally depict the human cost of war and disease. It must build urgency.
  - `solution.md` should paint a vivid, hopeful picture of the future we are building—a world without war and disease. It must inspire.

## Contributor Workflow

The plan _is_ the repository. We're building a book that's so clear anyone can read it.

1.  **Set up your environment:** Follow the [Development Environment Setup](./GUIDES/TECHNICAL_GUIDE.md#development-environment-setup) above.
2.  **Find something to improve:** Look at the `todo.md` for priorities.
3.  **If changing book structure:** Update the [Book Outline in README.md](./README.md#book-outline) first.
4.  **Make your changes:** Fork the repo and create a branch, or just edit on GitHub if you're not technical.
5.  **Follow the standards:** Use the rules in this document and the specialized guides.
6.  **Submit a pull request:** Explain how your change makes things better.

### Understanding the Book Outline

The Book Outline in README.md is the **complete skeleton of the book** showing the final narrative structure. It defines:

- **Parts:** Major thematic sections (8 total)
- **Chapters:** Main arguments within each part (16 total)
- **Sections:** Key points within chapters (numbered like 1.1, 1.2)
- **Subsections:** Supporting details (numbered like 1.1.1, 1.1.2)

**Format Rules:**

- Every item follows "[Core Concept]: [Dark Humor Description]"
  - Good: "FDA Gatekeeping: Killing You Safely Since 1962"
  - Bad: "The FDA approval process and its problems"

**Content Guardrails:**

- **Anti-Central-Planning:** Every solution must emphasize decentralization/markets/competition over committees
- **Public Choice Focus:** Frame problems through self-interest, not idealism
- **Dark Humor Required:** If it's not funny, make it funny

## Systematic Content Review Process

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
- **Formatting:** Does each sentence start on a new line? 

## Content and Style Standards

For detailed standards, please refer to the specialized guides linked at the top of this document. This section provides a high-level overview.

### 1. Information Architecture: Chapters, Sections, and The Appendix

This repo is structured like a book. Root files are "chapters." Subdirectories are "sections" with the details. `reference/` is the appendix.

**IMPORTANT:** The [Book Outline in README.md](./README.md#book-outline) is the authoritative writing checklist. Before adding new topics or changing the book architecture, update the Book Outline first. This prevents topic creep and maintains narrative flow. Remember: the outline is comprehensive for writing purposes - the final book will consolidate many items into cohesive chapters.

**Note:** Don't edit `brain/book/index.md` directly - it's auto-generated from frontmatter.

### 2. Quality Assurance and Actionable TODOs

To ensure all unfinished work is tracked and easily searchable, please add a `TODO` comment directly in the file at the location where work is needed. This allows any contributor to find actionable tasks by simply searching the entire project for "TODO".

- **Where:** Put `TODO`s where the problem is. Document-wide TODOs go at the bottom of the file. Never at the top.
- **Format:** Use comments so we can find them all later:
  - `<!-- TODO: Add citation for this claim. -->`
  - `<!-- TODO: Rewrite this section. -->`
  - `<!-- TODO: Add a chart here. -->`
  - `<!-- TODO: Expand this section. -->`

**Internal Link Integrity:** Before submitting, you **MUST FIX** any broken links in your changed files. Scan for all internal relative links (e.g., `[text](./path/file.md)`). If a link points to a deleted file, either remove the link or repoint it to a relevant alternative. This is a critical pre-submission check, not a task to be marked with a `TODO`.

### 3. Frontmatter Requirements

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

### 4. Sourcing and Citation Standard (CRITICAL)

**Every claim needs a source.** All source quotes go in `brain/book/references.qmd`.

1. Check if your source is already there
2. If yes, link to it: `[your claim](./references.qmd#anchor-id)`
3. If no, add it using the format you see in that file

Example in-text: `[The world spends 40x more on war](./references.qmd#sipri-2024) than on [curing disease](./references.qmd#med-research-funding).`

### 5. Naming and Linking

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.

### 6. Chapter Independence and Reusability

**IMPORTANT: QMD files must be reusable across different contexts.**

- **No "Next Chapter" sections:** Don't add "Next Chapter", "Turn the page", or similar navigation at the end of chapters
- **No hardcoded navigation:** Chapters should be self-contained without assuming a specific reading order
- **No context-specific references:** Avoid "as we saw in the previous chapter" or similar cross-references
- **Why:** These QMD files are reused in the website, presentations, and different book versions with different orderings

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing.
