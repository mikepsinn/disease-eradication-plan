---
title: "Refactor Wiki into a Comprehensive Knowledge Base"
status: "in-progress"
priority: "high"
assignee: "@gemini"
date: '2025-08-23'
tags: [refactoring, wiki, documentation, operations]
---

## Objective

To restructure the project's wiki into a comprehensive and well-organized knowledge base that supports the mission outlined in `README.md`.

## Plan

1.  **Generate a Content Inventory:**
    *   Create a script (`scripts/generate-inventory.ts`) that scans all markdown files.
    *   The script will parse the frontmatter of each file to extract its `title` and `description`.
    *   It will output this information into a human-readable markdown file: `operations/refactoring_inventory.md`.

2.  **Define New Structure & Create Manifest:**
    *   Review the `refactoring_inventory.md` to make informed decisions about file placement.
    *   Based on the review, finalize the new directory structure.
    *   Update the `operations/refactor-manifest.json` with definitive `move`, `keep`, and `delete` actions for every file.

3.  **Execute the Refactor:**
    *   Create a script (`scripts/execute-refactor.ts`) that reads `refactor-manifest.json` and performs the file operations.
    *   The script must have a "dry run" mode for verification.
    *   Run the script to restructure the repository.

4.  **Fix Internal Links:**
    *   Create a script (`scripts/fix-internal-links.ts`) that reads the manifest and updates all internal markdown links.
    *   The script must have a "dry run" mode for verification.
    *   Run the script to repair broken links.

5.  **Final Polish:**
    *   Update the master `index.md` to serve as a sitemap for the new structure.
    *   Perform a final review of `README.md` and key landing pages.
