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

**Table of Contents**

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
4. **Directness:** Does this sound like Kurt Vonnegut wrote it?

**Automatic Red Flags (Rewrite Immediately):**
- **Corporate Buzzwords:** "synergy," "activation," "paradigm shift," "stakeholder,"  "utilize," "facilitate" "world-class," "revolutionary," "unprecedented",  "world-class," "revolutionary," "unprecedented," "cutting-edge," "state-of-the-art," "best-in-class"
- **Trying to sound important:** Write like you're explaining this to a smart friend who thinks you might be crazy

**The Warren Buffett test:** Clear, factual, no drama, treats readers like adults.

**Voice and Tone: Principled, Blunt, and Credible**

**The Target and the Tone: Aim at the System, Speak to the "Us"**

The style of this project must balance two core principles: genuine outrage and radical inclusivity.

1.  **The Target of Outrage is the System, Not the People:** Our fight is with broken systems, not with the individuals trapped within them. The tone should be one of profound anger at the inefficiency, waste, and tragedy of our current institutions. It should not be a partisan or personal attack on any group. The goal is to critique a broken machine that *we* can all work together to fix.

2.  **We're All In This Together:** The writing should always assume the reader is a potential partner and a co-owner of the project. It should use terms like "we," "us," "our" to create a sense of a massive, collective movement that includes all of humanity. The goal is to make the reader feel like they are being invited to join a powerful rebellion, not being lectured or sold to. The reader is part of the "us" from the first sentence.

- **Assume self-interest, not idealism.** Ground every argument in Public Choice Theory.
  - **Good:** "Politicians support this because we fund their campaigns and their opponents if they don't."
  - **Bad:** "World leaders will embrace this plan because it's the right thing to do."
- **Use blunt language, not euphemisms.** Call things by their real names, but maintain technical precision where it adds clarity.
  - **Good:** "How to stay out of prison," "We're bribing everyone."
  - **Bad:** "Legal compliance," "Incentive alignment."
  - **Good and Precise:** "Transparent, automated, outcome-driven institutions" is better than "computer systems" because it specifies *what kind* of systems and *why* they matter.

**One-Second Test:** If you hesitate before reading a sentence aloud to a skeptical audience, rewrite it.

## Contributor Workflow

The plan _is_ the repository. We're building a book that's so clear anyone can read it.

1.  **Find something to improve:** Look at the `roadmap.md` for priorities.
2.  **If changing book structure:** Update the [Table of Contents in README.md](./README.md#table-of-contents) first.
3.  **Make your changes:** Fork the repo and create a branch, or just edit on GitHub if you're not technical.
4.  **Follow the standards:** Use the rules in this document.
5.  **Submit a pull request:** Explain how your change makes things better.

## Content and Style Standards

### 1. Information Architecture: Chapters, Sections, and The Appendix

This repo is structured like a book. Root files are "chapters." Subdirectories are "sections" with the details. `reference/` is the appendix.

**IMPORTANT:** The [Table of Contents in README.md](./README.md#table-of-contents) is the authoritative book structure. Before adding new chapters, sections, or changing the book architecture, update that Table of Contents first. This prevents topic creep and maintains narrative flow.

**Note:** Don't edit `brain/book/index.md` directly - it's auto-generated from frontmatter.

#### Epic Folders

**The Golden Rule:** If a topic is an "Epic" that needs more than one file, it gets a main summary file (`epic.md`) and a corresponding directory (`epic/`) for the details. This pattern applies at all levels.

**"The Book" vs. "Internal Stuff"**

- **The Book (`/`, `economics/`, `strategy/`, `legal/`):** Public content. The story and evidence.
- **Internal Playbook (`operations/`):** How we run things. For the core team.
- **The Appendix (`reference/`):** Data and citations that back up our claims.

| Section       | Content Type                                 | Examples                                                  |
| ------------- | -------------------------------------------- | --------------------------------------------------------- |
| `economics/`  | Financial models, ROI, investment thesis     | `investment-thesis.md`, `peace-dividend-value-capture.md` |
| `solution/`   | Core components of the proposed solution     | `1-percent-treaty.md`, `dih.md`, `dfda.md`                |
| `strategy/`   | Execution plans, political strategy, how-to  | `co-opting-defense-contractors.md`, `global-referendum.md` |
| `legal/`      | Legal compliance, governance, regulations    | `multi-entity-strategy.md`, `right-to-trial-act.md`       |
| `operations/` | Team structure, hiring, internal processes   | `hiring-plan.md`, `crypto-intake-sop.md`                  |
| `reference/`  | Data, studies, citations, reference material | `costs-of-war.md`, `recovery-trial.md`                    |

**Rules for Clean Structure:**

1. **One file, one job.** Split files that try to do too much.

2. **Unique filenames everywhere.** Add context only when needed:
   - ❌ Bad: `economics/fundraising/strategy.md` (too generic)
   - ✅ Good: `economics/fundraising/fundraising-strategy.md`
   - ✅ Also Good: `solution/1-percent-treaty.md` (already unique)

3. **Put things where they belong.** New content goes in the right section.

### 2. How to Mark What Needs Work

If something's broken, mark it with a `TODO` comment so we can fix it later.

**1. Internal Link Integrity:**

- Before submitting, scan the file for all internal relative links (e.g., `[text](./path/file.md)`).
- **You MUST FIX** any links that are broken.
- If a link points to a deleted file, either remove the link or repoint it to a relevant alternative.

**2. Marking What Needs Work:**

- **Where:** Put `TODO`s where the problem is. Document-wide TODOs go at the bottom. Never at the top.
- **Format:** Use comments so we can find them all later:
  - `<!-- TODO: Add citation for this claim. -->`
  - `<!-- TODO: Rewrite this section. -->`
  - `<!-- TODO: Add a chart here. -->`
  - `<!-- TODO: Expand this section. -->`

### 3. Frontmatter Requirements

Every markdown file needs this header:

```yaml
---
title: "A Clear and Descriptive Title"
description: "One sentence summary (max 140 chars)"
published: true # false for drafts
date: "YYYY-MM-DDTHH:MM:SS.sssZ"
tags: [keyword1, keyword2]
editor: markdown
dateCreated: "YYYY-MM-DDTHH:MM:SS.sssZ"
---
```

### 4. Sourcing and Citation Standard (CRITICAL)

**Every claim needs a source.** All sources go in `brain/book/references.md`.

1. Check if your source is already there
2. If yes, link to it: `[your claim](./references.md#anchor-id)`
3. If no, add it using the format you see in that file
4. Use good sources (not random blogs)

Example: `[The world spends 40x more on war](./references.md#sipri-2024) than on [curing disease](./references.md#med-research-funding).`

Format for new references:
```markdown
<a id="unique-anchor-id"></a>

- **Brief descriptive title**

  > "Direct quote with key stats..."
  > — Source Name, Date, [Link Title](URL)
```

#### How to Keep This Organized

-   **One alphabetized list:** Sort references by title. No subsections. Group related stats (like multiple years of the same report) under one item.

#### What NOT to Do

- Don't create "Sources" sections in individual files
- Don't duplicate references that already exist
- Don't use generic link text like "(Source)" - link the actual claim
- Don't create anchor links within individual files

This keeps everything in one place and prevents broken links.

### 5. Technical Standards

- **Code:** Write new tools in TypeScript
- **Dependencies:** Use `npm` and include a `package.json`
- **Execution:** Run TypeScript directly with `ts-node` or `tsx`. No compiled `.js` files in the repo.

### 6. Naming, Linking, and Formatting

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Dollar Sign Escaping:** Always escape dollar signs (`\$`) in regular text to prevent rendering issues (e.g., `\$27B`). Do not escape them inside backticked code blocks.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.
- **Sentence Structure:** Each sentence must start on a new line. This makes diffs cleaner, editing easier, and git blame more useful. Break after every period, question mark, or exclamation point.

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing.
