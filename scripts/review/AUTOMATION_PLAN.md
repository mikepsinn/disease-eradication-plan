# Automated Review Scripts: A Proposed Plan

This document outlines a plan for new scripts to be added to the `scripts/review` directory to fully automate the content review process as defined in `CONTRIBUTING.md`.

The existing `format-` and `style-` scripts provide an excellent foundation for ensuring consistency. The following proposed scripts will complete the automated audit process by covering fact-checking, link integrity, and design/figure validation.

## 1. Fact-Checking Scripts

**Files:**

- `fact-check-all-files.ts`
- `fact-check-file.ts`

**Purpose:**

To enforce the "Sourcing & Credibility" standard from `CONTRIBUTING.md` by ensuring every claim is cited.

**Core Functionality:**

1.  **Identify Stale Files:** Use the `getStaleFiles` utility to find all files that need a fact check (i.e., where the content has changed since the last `lastFactCheck` date).
2.  **Claim Detection (LLM-Powered):** For each stale file, send the body content to an LLM (like Gemini or Claude) with a prompt asking it to identify any factual claims (e.g., sentences containing statistics, percentages, costs, or other quantifiable data) that are **not** immediately followed by a markdown citation linking to `references.qmd`.
3.  **Reporting:** The script would log any uncited claims it finds, flagging them for manual review. For a more advanced implementation, it could insert a `<!-- TODO: Add citation for this claim. -->` comment directly into the file.
4.  **Update Frontmatter:** Upon successful completion of a check (even if it finds issues to report), the script will update the `lastFactCheck` date in the file's frontmatter to the current date.

## 2. Link Integrity Scripts

**Files:**

- `link-check-all-files.ts`
- `link-check-file.ts`

**Purpose:**

To enforce the "Technical & Structural Integrity" and "Sourcing and Citation Standard" from `CONTRIBUTING.md` by ensuring all internal links are valid. While `scripts/validate-links.ts` likely performs a similar function, integrating it into the `review` workflow with the stale-file check is crucial.

**Core Functionality:**

1.  **Identify Stale Files:** Use `getStaleFiles` to find files needing a link check based on the `lastLinkCheck` date.
2.  **Parse Links:** Extract all relative markdown links from the file content.
3.  **Validate File Paths:** For each link, verify that the target file exists at the specified relative path.
4.  **Validate Anchors:** For links to `references.qmd` (e.g., `[claim](../references.qmd#anchor-id)`), verify that the corresponding anchor ID (`<a id="anchor-id"></a>`) exists within `references.qmd`.
5.  **Reporting:** Log any broken links or invalid anchors.
6.  **Update Frontmatter:** Update the `lastLinkCheck` date in the frontmatter.

## 3. Figure & Design Scripts

**Files:**

- `figure-check-all-files.ts`
- `figure-check-file.ts`

**Purpose:**

To enforce the visual standards defined in `GUIDES/DESIGN_GUIDE.md`.

**Core Functionality:**

1.  **Identify Stale Files:** Use `getStaleFiles` to find files needing a figure check based on the `lastFigureCheck` date.
2.  **Chart Linter:**
    - Scan the content of any `.qmd` files in `dih-economic-models/figures/` that are referenced in the stale file.
    - Check for violations of the `GUIDES/DESIGN_GUIDE.md`, such as:
        - The presence of `plt.tight_layout()`.
        - The absence of a call to `setup_chart_style()` or `add_watermark()`.
        - Incorrect file naming conventions.
3.  **Static Image Check:**
    - Scan the stale file for static image links (e.g., `.png`, `.jpg`).
    - Flag any images that are not located in the `assets/` directory, as these may be candidates for conversion into reproducible `.qmd` charts in `dih-economic-models/figures/`.
4.  **Reporting:** Log any design guide violations.
5.  **Update Frontmatter:** Update the `lastFigureCheck` date in the frontmatter.

## Conclusion

By implementing these three sets of scripts, you will have a comprehensive, automated review pipeline that covers formatting, style, facts, links, and figures, ensuring that every piece of content aligns with your project's high standards.
