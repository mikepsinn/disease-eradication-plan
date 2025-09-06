---
title: "Operational Plan: Phase 0 & 1 - Bootstrap & Foundation"
description: "The detailed, task-level operational plan for the initial pre-seed and foundation phases of the project."
published: true
date: '2025-08-22T00:00:00.000Z'
tags: operations, roadmap, tasks, pre-seed, strategy
editor: markdown
dateCreated: '2025-08-22T00:00:00.000Z'
topic_id: operational-plan-phase-0-1
canonical: true
status: active
domains: [ops]
doc_type: ops
---

# Operational Plan: Phase 0 & 1

This document provides the detailed, granular task list for the initial phases of the project, as outlined in the [Canonical Roadmap](../strategy/roadmap.md). This serves as the tactical execution plan for the strategic goals of Phase 0 and Phase 1.

## Wiki Restructuring To-Do

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

---

## Phase 0: Pre-Seed & Foundation (Months 0-3)

**Goal:** Establish the core legal and financial structure and hire the "activation team" required to execute the main capital raise and global campaign.

| Task | Owner | Dependencies | Timeline | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Stream 1: Pitch & Pre-Seed Funding** | | | | |
| Draft core pitch deck summarizing the "ask" | Founder | [Landing Page Content](../strategy/warondisease-landing.md) | 1 Week | `Done` |
| Finalize [Pre-Seed SAFT terms](../economic-models/pre-seed-terms.md) | Founder | Pitch Deck | 3 Days | `Done` |
| Approve & Adopt [Team Incentive Policy](../strategy/team-incentives.md) | Founder | Pitch Deck | 1 Day | `Done` |
| Build & deploy landing page (v1) | Founder | Pitch Deck | 1-2 Weeks | `Not Started` |
| Build target list of angel & pre-seed investors | Founder | Pitch Deck | 1 Week | `Not Started` |
| Begin investor outreach & hold pitch meetings | Founder | Landing Page Live | 8 Weeks | `Not Started` |
| Secure pre-seed funding ($1M-$3M) | Founder | Pitch Meetings | 4 Weeks | `Not Started` |
| **Stream 2: Founding Team Recruitment** | | | | |
| Draft Job Description: [Capital Markets Lead](../careers/capital-markets-lead.md) | Founder | *(None)* | 2 Days | `Not Started` |
| Draft Job Description: [Elections & IE Compliance Lead](../careers/elections-ie-compliance-lead.md) | Founder | *(None)* | 2 Days | `Not Started` |
| Draft Job Description: [Growth & Referrals Lead](../careers/growth-referrals-lead.md) | Founder | *(None)* | 2 Days | `Not Started` |
| Begin recruitment for core leads | Founder | Funding Secured | Ongoing | `Not Started` |

---

## Phase 1: Foundation & Legal Framework (Months 1-12)

**Goal:** With a core team and seed funding in place, build the full legal, financial, and technical infrastructure required for the global campaign.

| Task | Owner | Dependencies | Timeline | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Stream 1: Strategy & Narrative** | | | | |
| Final review & sign-off on `warondisease-landing.md` | Program Lead | *(None)* | | `Done` |
| Add "Too Good to Be True?" sections to key docs | Program Lead | `warondisease-landing.md` | 1 Week | `Not Started` |
| **Stream 2: Team Expansion** | | | | |
| Draft Job Descriptions for Leads | Program Lead | [Hiring Plan](../careers/hiring-plan.md) | | `Done` |
| Begin recruitment outreach for Design Lead | Program Lead | JDs | 4 Weeks | `Not Started` |
| Begin recruitment outreach for Engineering Lead | Program Lead | JDs | 4 Weeks | `Not Started` |
| Begin recruitment outreach for Policy Lead | Program Lead | JDs | 4 Weeks | `Not Started` |
| **Stream 3: Website & Public Presence** | | | | |
| Develop core brand assets (logo, style guide, messaging framework) | Design Lead | Strategy & Narrative | 2 Weeks | `Not Started` |
| Create wireframes & final visual design | Design Lead | `warondisease-landing.md`, Brand Assets | 2 Weeks | `Not Started` |
| Develop website frontend | Engineering Lead | Visual Design | 3 Weeks | `Not Started` |
| Develop referral engine backend | Engineering Lead | | 4 Weeks | `Not Started` |
| Develop Peace Dividend calculator | Engineering Lead | | 2 Weeks | `Not Started` |
| Deploy public website V1 | Engineering Lead | Frontend/Backend Dev | 1 Week | `Not Started` |
| Launch v1 of the Bounty Program | Program Lead | [Bounty Model Doc](../strategy/open-ecosystem-and-bounty-model.md) | 1 Week | `Not Started` |
| **Stream 4: Legal & Financial Infrastructure** | | | | |
| Select jurisdiction & file for legal entity incorporation | Legal/Policy Lead | [Multi-Entity Strategy](../legal/multi-entity-strategy.md) | 2 Weeks | `Not Started` |
| Draft initial version of Impact Securities Reform Act | Legal/Policy Lead | | 6 Weeks | `Not Started` |
| Stand up core treasury vaults & dashboards | On-Chain/Treasury Lead | [DIH On-Chain Architecture](../architecture/dih-onchain-architecture.md) | 3 Weeks | `Not Started` |
| Finalize tokenomics & investment thesis documents | Capital Markets Lead | [Investment Thesis](../economic-models/victory-bond-investment-thesis.md) | 2 Weeks | `Not Started` |

---
*Note: The task "Approve & Adopt Team Incentive Policy" requires the creation of a `team-incentives.md` document in the `strategy` directory.*
