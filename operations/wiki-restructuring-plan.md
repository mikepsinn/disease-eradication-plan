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
- [ ] **User Action**: Rename the local repository directory from `dfda-wiki` to `1-percent-treaty`.
- [ ] **User Action**: Defensively register the required GitHub organizations as previously listed.
- [ ] **Task**: Perform the repository-wide search-and-replace for `VICTORY Fund` -> `1% Treaty Fund`.

**Phase B: Architectural Planning**
- [ ] **Task**: Create a new root-level `index.md` to serve as the master sitemap/table of contents for the entire wiki. This will define the target information architecture.
- [ ] **Task**: Identify and list all dFDA-specific files that are candidates for migration.

**Phase C: Content Restructuring & Re-branding**
- [ ] **Task**: Re-brand the main `README.md` and `home.md` to establish "The 1% Treaty" as the primary brand.
- [ ] **Task**: Audit and refactor all dFDA-related content (identified in Phase B) to align with the "protocol as a standard" strategy, removing all references to it being a "platform" or "product".
- [ ] **Task**: Create the new `dfda-protocol/` directory.
- [ ] **Task**: Move the now-refactored dFDA-specific files into the `dfda-protocol/` directory.

**Phase D: Link Audit & Final Polish**
- [ ] **Task**: Perform a repository-wide audit to identify and fix all broken internal links resulting from the file migration.
- [ ] **Task**: Update the master `index.md` sitemap with the final, correct file paths.
- [ ] **Task**: Perform a final polish of `README.md` and `home.md`.
