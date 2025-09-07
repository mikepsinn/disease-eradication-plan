---
title: "Project Plan: Wiki Restructuring"
description: "The detailed, task-level project plan for the comprehensive refactoring and re-branding of the 1% Treaty Wiki."
published: true
date: '2025-08-22T00:00:00.000Z'
tags: operations, project-plan, wiki, refactoring
editor: markdown
dateCreated: '2025-08-22T00:00:00.000Z'
---

# Wiki Restructuring To-Do

This section tracks the high-level tasks for the current wiki refactoring project. This process is broken down into phases to ensure a methodical and organized restructuring.

**Phase A: Foundational Setup & Renaming**
- [x] **User Action**: Create the `decentralized-institutes-of-health` GitHub organization.
- [x] **User Action**: Create the main repository as `decentralized-institutes-of-health` within the organization.
- [x] **User Action**: Defensively register the other required GitHub organizations (including `1-percent-treaty`).
- [x] **Task**: Perform the repository-wide search-and-replace for `VICTORY Fund` -> `1% Treaty Fund`, leaving the name `VICTORY Bonds` unchanged.

**Phase A.5: Pre-Refactoring Cleanup**
- [x] **Task**: Create a `scripts/cleanup_unused_images.py` script to find and optionally delete unreferenced image files. The script MUST include a "dry run" mode.
- [ ] **Task**: Run the script in "dry run" mode to generate a list of orphaned images.
- [ ] **Task**: Review the list of orphaned images and execute the script in "delete" mode.

**Phase B: Architectural Planning & Scripting**
- [ ] **Task**: Create an `scripts/generate_manifest.py` script that generates a `refactor-manifest.md` file listing all files and directories.
- [ ] **Task**: Run the inventory script and collaboratively curate the `refactor-manifest.md` to define the action for each file (MOVE, DELETE, KEEP).
- [ ] **Task**: Create an `execute-refactor.py` script that reads the manifest and performs the file operations. This script MUST include a "dry run" mode.

**Phase C: Execution & Re-branding**
- [ ] **Task**: Perform a final review of the manifest and the script's "dry run" output.
- [ ] **Task**: Execute the `execute-refactor.js` script to perform the full file migration.
- [ ] **Task**: Re-brand the main `README.md` and `home.md` to establish the "Decentralized Institutes of Health" as the primary brand.
- [ ] **Task**: Audit and refactor all dFDA-related content (now in `dFDA-protocol/`) to align with the "protocol as a standard" strategy.

**Phase D: Link Audit & Final Polish**
- [ ] **Task**: Perform a repository-wide audit to identify and fix all broken internal links resulting from the migration.
- [ ] **Task**: Update the master `index.md` sitemap with the final, correct file paths.
- [ ] **Task**: Perform a final polish of `README.md` and `home.md`.
