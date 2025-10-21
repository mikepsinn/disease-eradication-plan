# Plan for Enhanced Automated Review Scripts

This document outlines the plan to upgrade the content review scripts based on user feedback. The goal is to make the scripts more actionable by moving from simple console warnings to in-file `TODO` generation and to leverage advanced LLM features for fact-checking.

## 1. Unified Issue Handling: In-File TODO Comments

All scripts that *report* issues without auto-fixing them will be modified to insert structured `<!-- TODO: ... -->` comments directly into the relevant file.

**Affected Scripts:**

- `link-check-file.ts` / `link-check-all-files.ts`
- `figure-check-file.ts` / `figure-check-all-files.ts`
- `fact-check-file.ts` / `fact-check-all-files.ts`

**TODO Comment Structure:**

The comments will follow a consistent format: `<!-- TODO: [CHECK_TYPE] - [ISSUE_DESCRIPTION] -->`

**Examples:**

- A broken link would generate: `<!-- TODO: LINK_CHECK - Broken link: ./path/to/nonexistent-file.md -->`
- A design violation would generate: `<!-- TODO: FIGURE_CHECK - Static image 'my-image.png' should be in the 'assets/' directory. -->`

## 2. Upgrading Fact-Checking with Google Search Grounding

The `factCheckFileWithLLM` function in `utils.ts` will be significantly enhanced.

**New Workflow:**

1.  **Identify Uncited Claims:** The script will first parse the file to find factual claims that do not have an existing citation link to `references.qmd`.

2.  **Find Sources via Grounded LLM:** For each uncited claim, the script will make a **second** call to the Gemini API, this time enabling the **Google Search grounding tool**. The prompt will be highly specific: "Find a credible, primary source URL that verifies the following claim: '[uncited claim text]'".

3.  **Generate Actionable TODOs:** The script will then use the LLM's response to generate a detailed `TODO` comment and insert it directly above the uncited claim in the source file.

**Example Generated TODO:**

```markdown
<!-- 
TODO: FACT_CHECK - The following claim is uncited. A potential source has been found by the LLM. Please verify the source and add it to references.qmd.

Claim: "The proven inefficiency: FDA trials are 82X more expensive than necessary."

Suggested Source: https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs

Suggested Snippet for references.qmd:

<a id="unique-anchor-id-goes-here"></a>

- **RECOVERY Trial vs. FDA Trial Costs**

  > "The RECOVERY trial, for example, cost only about $500 per patient... By contrast, the median per-patient cost of a pivotal trial for a new therapeutic is around $41,000."
  > — Oren Cass, Manhattan Institute, 2023, [Slow, Costly Clinical Trials Drag Down Biomedical Breakthroughs](https://manhattan.institute/article/slow-costly-clinical-trials-drag-down-biomedical-breakthroughs)
-->
[The proven inefficiency: FDA trials are 82X more expensive than necessary.](../references.qmd#unique-anchor-id-goes-here)
```

This enhancement will transform the `fact-check` script from a simple linter into a powerful research assistant, dramatically speeding up the citation process while maintaining manual oversight for quality control.
