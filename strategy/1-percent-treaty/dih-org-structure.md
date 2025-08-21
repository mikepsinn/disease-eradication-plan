---
title: Decentralized Institutes of Health — Org Structure
description: Org chart connecting the Joint Strategic Command, DIH (treasury), dFDA platform, decentralized sub-institutes (including Aging), and mirrors of legacy agencies to align communities behind the 1% Treaty referendum.
published: true
date: '2025-08-15T00:00:00.000Z'
tags: dih, dfda, war-on-disease, organizational-design, governance
editor: markdown
---

## Org chart

```mermaid
graph TD
    JSC["Joint Strategic Command<br/>War on Disease"] --> DIH["Decentralized Institutes of Health (DIH)<br/>(Treasury & Coordination)"]
    DIH --> dFDA["dFDA Platform<br/>(Autonomous Trials & RWE)"]

    %% Disease/vertical institutes
    DIH --> DIH_Aging["DIH–Aging"]
    DIH --> DIH_Cancer["DIH–Cancer"]
    DIH --> DIH_Neuro["DIH–Neuroscience"]
    DIH --> DIH_Metabolic["DIH–Metabolic"]
    DIH --> DIH_Infectious["DIH–Infectious Disease"]
    DIH --> DIH_Mental["DIH–Mental Health"]
    DIH --> DIH_Rare["DIH–Rare Disease"]
    DIH --> DIH_Womens["DIH–Women’s Health"]
    DIH --> DIH_Child["DIH–Child Health"]

    %% Cross-cutting institutes
    DIH -. cross-cutting .-> Data["Data & Interop Standards (ONC mirror)"]
    DIH -. cross-cutting .-> Safety["Safety & Pharmacovigilance (BARDA/FDA mirror)"]
    DIH -. cross-cutting .-> Policy["Policy & Regulatory (AHRQ/Policy mirror)"]
    DIH -. cross-cutting .-> Treasury["Treasury & Grants (Payment & CMS savings)"]
    DIH -. cross-cutting .-> Advocacy["Patient Advocacy & Ethics"]
    DIH -. cross-cutting .-> AI["AI & Methods (Trial Automation)"]

    %% External mirrors / alignment
    NIH[("NIH Institutes")] -->|mirror programs| DIH
    CDC[("CDC")] -->|surveillance alignment| DIH_Infectious
    BARDA[("BARDA")] -->|risk & safety| Safety
    CMS[("CMS")] -->|value-based savings| Treasury
    ONC[("ONC")] -->|interoperability| Data
    AHRQ[("AHRQ")] -->|outcomes research| Policy

    %% Platform flows
    dFDA --> Trials["Decentralized Trials"]
    dFDA --> Registries["Longitudinal Registries"]
    Trials --> Evidence["Treatment Outcome Rankings"]
    Registries --> Evidence
    Evidence --> Policy
```

## Purpose

- Align thousands of orgs/communities behind the 1% Treaty referendum with clear homes and earned, criteria-based recognition.
- Create a lightweight mirror of legacy agencies to collaborate without implying government authority.

## Titles framework (earned recognition with guardrails)

- Institute Chair (volunteer, term-limited)
- Scientific Council Member
- Founding Fellow / Fellow
- Ambassador (regional or domain)
- Affiliate Partner (org-level)

Appointments are transparent, criteria-based, and revocable; all appointees sign code of conduct, conflict-of-interest, and brand-use policy. Public directory lists affiliations and disclosures.

## Minimal governance

- Automated-by-default. Human roles act as emergency custodians with explicit sunset/hand-off to contracts.
- Each institute uses a one-page charter and auto-generated OKRs/dashboards from oracles; no quarterly reports.
- Cross-cutting institutes provide shared services (standards, safety, ethics, treasury, AI) as APIs/contracts.

## Success metrics

- Orgs endorsed to the 1% Treaty, active projects funded, volunteer hours, trial participants subsidized, and referendum signatures attributed to institutes.


## Decentralization and automation blueprint

- On-chain treasury modules for grants, quadratic funding, patient subsidies, outcome bounties, and $VICTORY bonds
- Verifiable oracles for evidence, safety, identity/COI, and healthcare-savings estimates
- AI agents for trial design, monitoring, fraud detection, and funding triage
- Tokenless-first governance (reputation/credentials), merge-to-earn bounties, public proposals with on-chain execution
- Interop standards: HL7 FHIR/OMOP, DID/VC, EIP-712, IPFS/Arweave

See [DIH On-Chain and AI Architecture](../../architecture/dih-onchain-architecture.md) for technical details and [Incentives Layer](../incentives-layer.md) for social/economic incentives.




