# Project Plan: Automated Content Review & Fixing Engine

This document outlines the plan to create a suite of scripts that automate the content review and fixing process for the DIH knowledge base.

## I. Core Objectives

1.  **Automate Repetitive Tasks:** Eliminate the manual effort required for formatting, style checks, and source verification.
2.  **Improve Consistency:** Ensure every file strictly adheres to the guidelines defined in `CONTRIBUTING.md`.
3.  **Optimize Costs:** Minimize LLM API usage by only reviewing files that have been modified since their last review.
4.  **Streamline Workflow:** Create a single command that developers can run to validate and fix all staged files before committing.

## II. Frontmatter Strategy

We will adopt a granular frontmatter-based tracking system. The `lastReviewed` field will be deprecated in favor of specific, per-task timestamps.

### New Frontmatter Fields:
- `lastModified`: To be updated automatically by a script using `git` history.
- `lastFormatted`: Timestamp for when the formatting script was last run.
- `lastStyleCheck`: Timestamp for the last automated style/tone review.
- `lastFactCheck`: Timestamp for the last source and fact verification.
- `lastLinkCheck`: Timestamp for the last internal and external link validation.
- `lastFigureCheck`: Timestamp for the last check for visualization opportunities.

## III. Script Development Plan

All scripts will be developed in TypeScript and located in the `scripts/review/` directory.

### 1. `get-stale-files.ts`
- **Purpose:** Identify which files need review.
- **Logic:**
    - Use `simple-git` to get the last commit date for every `.qmd` file.
    - Parse the frontmatter of each file to get the review timestamps.
    - If `lastModified` is more recent than any of the `last...` check dates, the file is "stale" and needs review for that specific check.
- **Output:** A JSON object mapping each check type to a list of files that need processing.

### 2. `format-file.ts` (Enhancement of `check-formatting.ts`)
- **Purpose:** Automatically fix formatting issues.
- **Logic:**
    - Read a file.
    - Add missing frontmatter fields.
    - Split lines with multiple sentences.
    - Overwrite the file with the corrected content.
    - Update the `lastFormatted` timestamp in the frontmatter.

### 3. `check-style.ts`
- **Purpose:** Review the file for tone, voice, and style guide adherence.
- **Logic:**
    - Use an LLM API to analyze the text against the rules in `CONTRIBUTING.md`.
    - The prompt will instruct the LLM to identify violations of "dark humor," "Factual Mischaracterization," "Stylistic Redundancy," etc.
- **Output:** A list of suggested improvements. It will **not** auto-fix, as style is subjective.

### 4. `check-facts.ts`
- **Purpose:** Verify claims against their sources.
- **Logic:**
    - Extract all claims with inline citations.
    - For each claim, fetch the content of the cited source.
    - Use an LLM API to determine if the source material supports the claim.
- **Output:** A report of claims that may be misaligned with their sources.

### 5. `check-links.ts`
- **Purpose:** Validate all internal and external links.
- **Logic:**
    - Extract all markdown links.
    - For internal links, check if the target file exists.
    - For external links, make a HEAD request to ensure a `200 OK` response.
- **Output:** A list of broken links.

### 6. `check-figures.ts`
- **Purpose:** Identify opportunities for new visualizations.
- **Logic:**
    - Use an LLM API to read a chapter and identify sections with dense data or complex concepts.
- **Output:** Suggestions for new charts or diagrams (e.g., "A bar chart comparing X and Y would be effective here.").

### 7. `review.ts` (Master Orchestrator Script)
- **Purpose:** Run the entire review and fixing process.
- **Logic:**
    1. Run `get-stale-files.ts` to get the list of files to process.
    2. For each file needing formatting, run `format-file.ts`.
    3. For each file needing a style check, run `check-style.ts` and log the suggestions.
    4. ...and so on for all other checks.
- **Usage:** `npx ts-node scripts/review/review.ts`

## IV. Implementation Roadmap

- [ ] **Phase 1: Foundational Scripts**
    - [ ] Update `CONTRIBUTING.md` with the new frontmatter fields.
    - [ ] Develop `get-stale-files.ts` to identify target files.
    - [ ] Enhance `check-formatting.ts` into the auto-fixing `format-file.ts`.
- [ ] **Phase 2: LLM-Powered Checks**
    - [ ] Develop `check-style.ts`.
    - [ ] Develop `check-facts.ts`.
    - [ ] Develop `check-figures.ts`.
- [ ] **Phase 3: Finalization & Integration**
    - [ ] Develop `check-links.ts`.
    - [ ] Build the master `review.ts` orchestrator script.
    - [ ] Add a `pnpm` script in `package.json` (e.g., `"review": "npx ts-node scripts/review/review.ts"`).
    - [ ] (Optional) Integrate the `review` script into a pre-commit hook using `husky`.

This plan provides a clear, phased approach to building a powerful, cost-effective automated review system.
