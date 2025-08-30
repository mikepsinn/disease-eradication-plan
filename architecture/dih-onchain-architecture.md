---
title: DIH On-Chain and AI Architecture
description: Modular blueprint to replace centralized bureaucracy with AI agents and smart contracts across treasury, trials, and evidence-to-funding automation.
published: true
date: '2025-08-15T00:00:00.000Z'
tags: architecture, smart-contracts, ai, governance, oracle, dfda, dih
editor: markdown
---

## Why on-chain + AI

Replace manual, political, and opaque processes with verifiable automation: programmatic funding, open evidence, transparent governance, and cryptographic attestations.

## High-level architecture

```mermaid
graph TD
  subgraph Platform
    dFDA[dFDA Evidence Engine]
    Agents[AI Agents (Design, Monitor, Fraud, Triage)]
  end

  subgraph OnChain
    Treasury[DIH Treasury]
    QF[Quadratic Funding Rounds]
    Bounties[Outcome Bounties/Prizes]
    Subsidies[Patient Subsidy Module]
    Savings["VICTORY Bonds & Savings-Sharing"]
    Registry[Identity & Attestation Registry]
    Pause[Safety Pause/Kill-switch]
  end

  Oracles[Verifiable Oracles (Evidence, Safety, Identity, Savings)]

  dFDA -->|ranked outcomes, trial status| Oracles
  Agents -->|trial design, monitoring signals| dFDA
  Oracles --> Treasury
  Treasury --> QF
  Treasury --> Bounties
  Treasury --> Subsidies
  Treasury --> Savings
  Registry --> QF
  Registry --> Bounties
  Registry --> Subsidies
  Agents --> Pause
  Pause --> Treasury
```

## Core modules

- Treasury (modular vault): role-gated modules, streamed disbursements, clawbacks, emergency pause
- Quadratic Funding: round factory, matching pool rules, sybil-resistance hooks (Passport/Proof-of-Humanity pluggable)
- Outcome Bounties/Prizes: milestone contracts linked to evidence oracle; partial payouts; dispute window
- Patient Subsidies: per-participant vouchers; eligibility rules; post-trial reconciliation
- VICTORY Bonds & Savings-Sharing: bond issuance; vesting tied to measured savings; slippage caps; redemption windows
- Identity & Attestations: DID/VC registry; EIP-712 signed reports; role-bound credentials (Chair, Fellow, Ambassador)
- Safety Pause: circuit-breaker triggered by incident signals; progressive unpause policy tied to remediation

## Oracles (minimal trust, verifiable data)

- Evidence Oracle: consumes dFDA outputs (ranked outcomes, enrollment, adverse events); hashes data packages; posts proofs
- Savings Oracle: posts healthcare-savings estimates with confidence intervals; references public models and datasets
- Identity Oracle: verifies affiliations and conflicts; binds to roles via credentials
- Safety Oracle: emits incident severity scores; triggers automatic holds on affected payouts

## AI agent responsibilities

- Design Agent: trial templates, power/budget estimates, adaptive designs
- Monitor Agent: enrollment, adherence, data quality, interim looks
- Fraud Agent: anomaly detection, duplication, collusion, sybil detection
- Triage Agent: prioritizes funding by expected social value; explains decisions with citations

## Governance pattern (tokenless-first)

- Reputation- and credential-based participation; one-person safeguards via sybil-resistance
- Public proposals; off-chain signaling (e.g., Snapshot) with on-chain execution via safe modules
- Merge-to-earn: GitHub merges release bounty payouts via attestation hooks

## Interoperability standards

- Health: HL7 FHIR R4; OMOP CDM mapping; open measurement catalogs
- Identity: W3C DID/VC; EIP-712 signatures; selective disclosure
- Data packaging: IPFS/Arweave content addressing; cryptographic hashes in-chain

## Risk controls

- Emergency pause on safety incidents; payout holds for affected interventions
- Clawbacks for data falsification or trial misconduct
- Auditability: immutable logs, reproducible pipelines, open models/code

## Migration path (mirror → replacement)

1) Mirror: run parallel programs with transparent automation and faster cycles
2) Co-govern: accept third-party funds and match with DIH treasury under shared rules
3) Replace: program becomes de facto standard; agencies integrate or become data providers

## KPIs

- Cost per trial, time-to-launch, participants subsidized, evidence generated, ROI of subsidies, verified savings redeemed, incident rate and time-to-mitigation

Link: see [DIH Org Structure](../strategy/1-percent-treaty/dih-org-structure.md) for the org view and [Institute Charter Template](../strategy/1-percent-treaty/institute-charter-template.md) for institute‑level governance.


