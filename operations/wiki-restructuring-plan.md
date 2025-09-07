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
- [ ] **User Action**: Create the `decentralized-institutes-of-health` GitHub organization.
- [ ] **User Action**: Create the main repository as `decentralized-institutes-of-health` within the organization.
- [x] **User Action**: Defensively register the other required GitHub organizations (including `1-percent-treaty`).
- [x] **Task**: Perform the repository-wide search-and-replace for `VICTORY Fund` -> `1% Treaty Fund`, leaving the name `VICTORY Bonds` unchanged.

**Phase B: Architectural Planning**
- [x] **Task**: Create a new root-level `index.md` to serve as the master sitemap/table of contents for the entire wiki. This will define the target information architecture.
- [ ] **Task**: Identify and list all dFDA-specific files that are candidates for migration.

**Phase C: Content Restructuring & Re-branding**
- [ ] **Task**: Re-brand the main `README.md` and `home.md` to establish the "Decentralized Institutes of Health" as the primary brand and "The 1% Treaty" as its flagship initiative.
- [ ] **Task**: Audit and refactor all dFDA-related content (identified in Phase B) to align with the "protocol as a standard" strategy, removing all references to it being a "platform" or "product".
- [ ] **Task**: Create the new `dfda-protocol/` directory.
- [ ] **Task**: Move the now-refactored dFDA-specific files into the `dfda-protocol/` directory.

**Phase D: Link Audit & Final Polish**
- [ ] **Task**: Perform a repository-wide audit to identify and fix all broken internal links resulting from the file migration.
- [ ] **Task**: Update the master `index.md` sitemap with the final, correct file paths.
- [ ] **Task**: Perform a final polish of `README.md` and `home.md`.
