---
title: How to Contribute
description: "The single source of truth for all contribution guidelines, style guides, and project standards for the Decentralized Institutes of Health (DIH) knowledge base."
published: true
tags: [contributing, guidelines, standards, book, knowledge-base]
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
  - [7. Visualizations and Diagrams](#7-visualizations-and-diagrams)
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

## Writing Style Guide

**The Tone: Dark Humor Meets Practical Hope**

We're writing "The Complete Idiot's Guide to Ending War and Disease" - a book that uses dark humor, absurd observations, and irrefutable facts to trick humanity into not killing itself. Think Kurt Vonnegut explaining economics to drunk people at a funeral.

**The 4 Core Checks:**

1. **Clarity:** Can I say this to my mom and have her understand?
2. **Credibility:** Would I stake my reputation on this claim?
3. **Concision:** Can I cut words without losing meaning?
4. **Directness:** Does this sound like Kurt Vonnegut wrote it?

**Essential Elements to Include:**

- **Dark humor about death and human stupidity** - We're all dying anyway, might as well laugh
- **Cynical but loving observations about humanity** - We're idiots, but we're OUR idiots
- **Simple, conversational language** - No jargon, write like you're explaining to a smart drunk friend
- **Absurd but accurate analogies** - "The FDA is like a lifeguard who checks if the life preserver is safe while you drown"
- **A sense of cosmic irony** - The universe is laughing at us, we might as well join in
- **Practical solutions presented as obvious common sense** - "What if sick people could just... try treatments?"

**Automatic Red Flags (Rewrite Immediately):**

- **Corporate Buzzwords:** "synergy," "activation," "paradigm shift," "stakeholder," "utilize," "facilitate" "world-class," "revolutionary," "unprecedented", "cutting-edge," "state-of-the-art," "best-in-class"
- **Factual Mischaracterization:** Be precise when assigning blame. For example, instead of "The FDA demands \$41,000," write "The FDA-regulated system results in trial costs of \$41,000." Attribute outcomes to the system, not just the agency, unless a source directly supports it.
- **Stylistic Redundancy:** Avoid using a string of synonyms or clichés for emphasis (e.g., "Zero. Zilch. Nada."). A single, powerful word is more effective. Let the facts be the punchline.
- **Trying to sound important:** Write like you're explaining this to a smart friend who thinks you might be crazy
- **Euphemisms for death:** Just say "die" or "death" - we're adults here
- **Academic pomposity:** If you sound like a textbook, rewrite it

**The Voice Test:** Would this make someone laugh AND think? If not, add more absurdity or more facts.

**Additional Humor Guidelines:**

- **Humor Should Enhance, Not Distract:** Jokes should make the argument more memorable, not weaker. If a joke doesn't add insight, cut it. Dark observations > cheap shots. Absurd but true > absurd but false.
- **Emulate Style, Don't Quote:** Channel Vonnegut's dark humor and cosmic irony, but don't use his actual phrases ("so it goes", "listen:", etc.). Create original observations in that style instead of borrowing catchphrases.
- **Don't Insult Unless It's Really Funny:** If you must make a joke about a group, it needs to be either: (a) So funny it's worth the risk, OR (b) About abstract "systems" not specific people/companies

**Voice and Tone: Principled, Blunt, and Credible**

**The Target and the Tone: Aim at the System, Speak to the "Us"**

The style of this project must balance two core principles: genuine outrage and radical inclusivity.

1.  **The Target of Outrage is the System, Not the People:** Our fight is with broken systems, not with the individuals trapped within them. The tone should be one of profound anger at the inefficiency, waste, and tragedy of our current institutions. It should not be a partisan or personal attack on any group. The goal is to critique a broken machine that _we_ can all work together to fix.

2.  **We're All In This Together:** The writing should always assume the reader is a potential partner and a co-owner of the project. It should use terms like "we," "us," "our" to create a sense of a massive, collective movement that includes all of humanity. The goal is to make the reader feel like they are being invited to join a powerful rebellion, not being lectured or sold to. The reader is part of the "us" from the first sentence.

- **Assume self-interest, not idealism.** Ground every argument in Public Choice Theory.
  - **Good:** "Politicians support this because we fund their campaigns and their opponents if they don't."
  - **Bad:** "World leaders will embrace this plan because it's the right thing to do."
- **Use blunt language, not euphemisms.** Call things by their real names, but maintain technical precision where it adds clarity.
  - **Good:** "How to stay out of prison," "We're bribing everyone."
  - **Bad:** "Legal compliance," "Incentive alignment."
  - **Good and Precise:** "Transparent, automated, outcome-driven institutions" is better than "computer systems" because it specifies _what kind_ of systems and _why_ they matter.

**One-Second Test:** If you hesitate before reading a sentence aloud to a skeptical audience, rewrite it.

## Development Environment Setup

### Quick Start (Automated)

1. **Run the setup script**: `.\setup.ps1`
2. **Activate the environment**: `.\venv\Scripts\Activate.ps1`
3. **Verify setup**: `.\verify-setup.ps1`
4. **Preview the book**: `quarto preview index.qmd`

### Prerequisites

- Python 3.8+
- Quarto
- PowerShell (Windows)

### Manual Setup

If the automated setup doesn't work:

1. Create virtual environment: `python -m venv .venv`
2. Activate it: `.\venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Register Jupyter kernel: `python -m ipykernel install --user --name=dih-project-kernel --display-name "DIH Project Kernel"`

### Troubleshooting

- **"ModuleNotFoundError"**: Run `.\verify-setup.ps1` to check your environment
- **"Kernel not found"**: Re-run the Jupyter kernel registration step
- **Quarto errors**: Make sure your virtual environment is activated

## Contributor Workflow

The plan _is_ the repository. We're building a book that's so clear anyone can read it.

1.  **Set up your environment:** Follow the [Development Environment Setup](#development-environment-setup) above.
2.  **Find something to improve:** Look at the `todo.md` for priorities.
3.  **If changing book structure:** Update the [Book Outline in README.md](./README.md#book-outline) first.
4.  **Make your changes:** Fork the repo and create a branch, or just edit on GitHub if you're not technical.
5.  **Follow the standards:** Use the rules in this document.
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

### 1. Information Architecture: Chapters, Sections, and The Appendix

This repo is structured like a book. Root files are "chapters." Subdirectories are "sections" with the details. `reference/` is the appendix.

**IMPORTANT:** The [Book Outline in README.md](./README.md#book-outline) is the authoritative writing checklist. Before adding new topics or changing the book architecture, update the Book Outline first. This prevents topic creep and maintains narrative flow. Remember: the outline is comprehensive for writing purposes - the final book will consolidate many items into cohesive chapters.

**Note:** Don't edit `brain/book/index.md` directly - it's auto-generated from frontmatter.

#### Epic Folders

**The Golden Rule:** If a topic is an "Epic" that needs more than one file, it gets a main summary file (`epic.md`) and a corresponding directory (`epic/`) for the details. This pattern applies at all levels.

**Book Chapter Structure:**
Each major chapter follows the epic pattern:

- **Executive Summary File:** `brain/book/problem.qmd` - Overview that links to all sections
- **Section Files:** `brain/book/problem/*.qmd` - Detailed content for each section
- **Example Structure:**

  ```
  brain/book/
    problem.qmd          # Executive summary linking to all problem sections
    problem/             # Folder with detailed sections
      cost-of-war.md
      cost-of-disease.md
      nih-funding-is-broken.md
    solution.qmd         # Executive summary linking to all solution sections
    solution/            # Folder with detailed sections
      dfda.md
      dih.qmd
      1-percent-treaty.md
  ```

**"The Book" vs. "Internal Stuff"**

- **The Book (`brain/book/`):** Main book content organized by chapters with executive summaries
- **Internal Playbook (`operations/`):** How we run things. For the core team.
- **The Appendix (`reference/`):** Data and citations that back up our claims.

| Section       | Content Type                                 | Examples                                                  |
| ------------- | -------------------------------------------- | --------------------------------------------------------- |
| `economics/`  | Financial models, ROI, investment thesis     | `investment-thesis.md`, `peace-dividend-value-capture.md` |
| `solution/`   | Core components of the proposed solution     | `1-percent-treaty.md`, `dih.md`, `dfda.md`                |
| `strategy/`   | Execution plans, political strategy, how-to  | `co-opting-defense-contractors.md`, `global-referendum.md` |
| `legal/`      | Legal compliance, governance, regulations    | `multi-entity-strategy.md`                                |
| `operations/` | Team structure, hiring, internal processes   | `hiring-plan.md`, `crypto-intake-sop.md`                  |
| `reference/`  | Data, studies, citations, reference material | `costs-of-war.md`, `recovery-trial.md`                    |

**Rules for Clean Structure:**

1. **One file, one job.** Split files that try to do too much.

2. **Unique filenames everywhere.** Add context only when needed:

   - ❌ Bad: `economics/fundraising/strategy.md` (too generic)
   - ✅ Good: `economics/fundraising/fundraising-strategy.md`
   - ✅ Also Good: `solution/1-percent-treaty.md` (already unique)

3. **Put things where they belong.** New content goes in the right section.

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

Format for new references in `references.qmd`:

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
- **Automated Formatting:** All `.qmd` files are subject to automated formatting checks based on the rules defined in [`FORMATTING_GUIDE.md`](./FORMATTING_GUIDE.md).

### 6. Naming and Linking

- **Filenames:** Use kebab-case and be descriptive (e.g., `dih-treasury-cash-flow-model.md`).
- **Internal Links:** Use standard, relative Markdown links (`./`, `../`). Do not use backticks or bare paths for links.
- **Code vs. Links:** Use backticks only for code, commands, or literals—not for navigational references.

### 7. Chapter Independence and Reusability

**IMPORTANT: QMD files must be reusable across different contexts.**

- **No "Next Chapter" sections:** Don't add "Next Chapter", "Turn the page", or similar navigation at the end of chapters
- **No hardcoded navigation:** Chapters should be self-contained without assuming a specific reading order
- **No context-specific references:** Avoid "as we saw in the previous chapter" or similar cross-references
- **Why:** These QMD files are reused in the website, presentations, and different book versions with different orderings

### 8. Visualizations and Diagrams

To make the content more engaging and easier to understand, we will use Python-generated charts and diagrams with a minimalistic and classy aesthetic. Quarto provides excellent tools for this.

- **Diagrams:** For flowcharts, sequence diagrams, etc., please use Mermaid syntax. See the [Quarto Diagrams Guide](https://quarto.org/docs/authoring/diagrams.html) for implementation details.
- **Python Charts:** For data visualizations, use Python libraries like Matplotlib or Plotly, executed within Quarto. For guidance, refer to the [Quarto Guide for Using Python](https://quarto.org/docs/computations/python.html).

**For detailed chart creation guidelines, naming conventions, and technical standards, see [DESIGN_GUIDE.md](DESIGN_GUIDE.md).**

### Where to Put Visuals: A Quick Guide

To keep our project organized, here’s where different types of visual assets should go. The golden rule is: **if you can create it with code, do it.**

1.  **Reproducible Charts (`brain/figures/`)**

    -   **What:** All new data visualizations generated from code (Python, R, etc.). This is the default location for charts.
    -   **Format:** `.qmd` files that can be included in any document.
    -   **Why:** This approach allows us to easily reuse and maintain consistent styling across the book, website, and presentations. It’s the difference between a recipe and a photo of a cake—we want the recipe.

2.  **Static Images (`assets/`)**

    -   **What:** General images that are not data visualizations, such as photos, icons, or diagrams from external sources.
    -   **Format:** `.png`, `.jpg`, `.gif`, etc.
    -   **Why:** This is the general-purpose folder for all static visual assets that aren't charts.

3.  **Static Charts (`brain/figures/`)**

    -   **What:** Pre-existing, static charts that were not generated by code in this repository (e.g., from a scientific paper).
    -   **Format:** `.png`, `.jpg`, `.svg` if possible, etc.
    -   **Why:** This is a holding area for charts we can't generate ourselves. The long-term goal is to recreate them as reproducible charts in `brain/figures/` whenever possible.

**Summary Table:**

| If you have...                               | Put it in...         | As a...          |
| -------------------------------------------- | -------------------- | ---------------- |
| A new data chart you can create with code    | `brain/figures/`      | `.qmd` file      |
| A photo, icon, or non-chart image            | `assets/`            | `.png`, `.jpg`   |
| A static chart from an external source       | `assets/figures/`     | `.png`, `.jpg`   |

## Automation and CI

- **Link Checker:** Pull requests with dead internal links will fail.
- **Frontmatter Validator:** Pull requests will fail if required frontmatter fields are missing.
