---
title: File Organization Guidelines for the dFDA Wiki
description: 'Where new pages belong, naming and linking conventions, and how to keep the wiki coherent at scale.'
published: true
date: '2025-01-20T00:00:00.000Z'
tags: [authoring, style, structure, file-placement, naming, links]
editor: markdown
dateCreated: '2025-01-20T00:00:00.000Z'
---

## Purpose

This wiki is the source of truth. These guidelines define where new content belongs, how to name files, and how to link—so readers can reliably find things and contributors don’t second‑guess placement.

## Core Placement Map (what goes where)

- `features/` — Product and technical components of the dFDA system (UIs, APIs, analytics, plugins, treasury infra). The primary technical roadmap for the dFDA platform itself should be at the root of this folder (e.g., `features/dfda-roadmap.md`), while roadmaps for specific sub-features can be nested.
- `problems/` — Issues in the current medical research system (e.g., cost, speed, bias), with evidence
- `benefits/` — Advantages of the dFDA approach (cost/time/QALY gains, access), with quantified claims
- `regulatory/` — Legal and compliance analysis, recommendations, and policy proposals
- `economic-models/` — Quantitative models, ROI analyses, budgets, market sizing, investor theses
- `strategy/` — Strategic plans, playbooks, fundraising models, governance strategy, roadmaps
- `proposals/` — Concrete initiatives (X‑Prizes, policy proposals, referendums), specs and drafts
- `clinical-trials/` — Trial methodologies, protocols, pragmatic vs explanatory, case studies
- `community/` — Governance, contribution guides, partners, researchers, funding sources, templates
- `architecture/` — High‑level system and on‑chain/off‑chain architectural docs
- `interventions/`, `conditions/`, `reference/`, `wiki/` — Reference pages as already organized

## New operational docs (SOPs, policies)

Avoid creating a generic `docs/` folder—the entire repo is documentation. Place operational content as follows:
- Compliance, fundraising, liquidity policies: in `strategy/` (or `regulatory/` if primarily legal)
- Day‑to‑day SOPs (e.g., intake, incident response): use `operations/` (new top‑level) or the closest domain folder if narrowly scoped

When in doubt, place the doc where its primary decision‑maker would look (legal → `regulatory/`; capital raising → `strategy/`; engineering → `features/`/`architecture/`).

## Naming & structure

- Use kebab‑case filenames: `victory-bond-investment-thesis.md`
- One clear purpose per page; split if a page grows beyond a single concern
- Start every `.md` with YAML frontmatter (title, description < 250 chars, published, date, tags, editor, dateCreated)

## Linking & anchors

- Use page‑relative markdown links (./, ../), not repo‑root or backticked paths
- Examples (from a file in `strategy/`):
  - Same folder: `[Fundraising Models Comparison](./fundraising-models-comparison.md)`
  - Parent folder: `[Legal Compliance Framework](../regulatory/legal-compliance-framework.md)`
  - Sibling domain: `[Victory Bond Investment Thesis](../economic-models/victory-bond-investment-thesis.md)`
- Link to sections with `#heading-slug` anchors when helpful

## Sourcing & citations (for quantified claims)

- Inline link the claim to a high‑quality source
- Add a “Source Quotes for Key Parameters” section with verbatim quotes and links
- Escape dollar signs (\$) in body text to avoid unintended LaTeX rendering

## Decision tree (where does this page go?)

1) Is it primarily about product/tech behavior? → `features/` (UI/API/analytics) or `architecture/` (system diagrams)
2) Is it a legal analysis, rule, or policy? → `regulatory/`
3) Is it a capital strategy, funding model, or governance playbook? → `strategy/`
4) Is it a quantitative model, ROI/budget, or investor thesis? → `economic-models/`
5) Is it a public‑facing proposal or program spec? → `proposals/`
6) Is it an SOP or operational runbook? → `operations/` (or the closest domain)
7) Is it background evidence or definitions? → `reference/` (or the relevant domain subfolder)

## Examples

- Investor thesis: `economic-models/victory-bond-investment-thesis.md`
- Legal fundraising strategy: `strategy/legal-compliance-framework.md`
- Fundraising option comparison & EV modeling: `strategy/fundraising-models-comparison.md`
- Token liquidity policy (could live in strategy or operations): `strategy/dex-listing-policy.md` (or `operations/dex-listing-policy.md`)
- Crypto intake SOP (ops‑facing): `operations/crypto-intake-sop.md`

## Migration note (deprecating docs/)

The `docs/` folder has been deprecated and removed. New files should follow the map above. All previous contents of `docs/` have been moved to their appropriate locations in `strategy/`, `regulatory/`, `operations/`, `reference/`, `architecture/`, and `features/`.

## Pull request checklist

- [ ] File placed per map/decision tree
- [ ] Kebab‑case filename; YAML frontmatter present
- [ ] Page‑relative links only; no backticked paths for navigation
- [ ] Dollar signs escaped; sources linked and quoted where claims are quantitative
- [ ] Cross‑linked from relevant hub pages (e.g., landing, strategy index)
