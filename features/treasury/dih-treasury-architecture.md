---
title: DIH Treasury Architecture
description: Technical and governance architecture for the Decentralized Institutes of Health (DIH) Treasury, targeting Bitcoin-level decentralization via multi-sig and threshold signatures.
published: true
date: 2025-08-12T00:00:00.000Z
tags: dih, treasury, multisig, threshold-signatures, governance, security, transparency
editor: markdown
dateCreated: 2025-08-12T00:00:00.000Z
fontawesomeIcon: fa-vault
---

## Purpose

The Decentralized Institutes of Health (DIH) operates a global treasury to subsidize decentralized clinical trials, fund open-source infrastructure, and manage prizes and bounties. To earn durable trust, the treasury must be credibly neutral, censorship-resistant, and resilient—approaching "Bitcoin-level" decentralization in practice. This page specifies the treasury architecture: custody, controls, governance hooks, auditing, and incident response.

## Design Goals

- **Security first**: Defense-in-depth across keys, approvals, and execution.
- **Geographic and institutional diversity**: Signers distributed across jurisdictions and sectors.
- **Minimize single points of failure**: Multiple clients, infra, and operational providers.
- **Transparency by default**: On-chain policies, open reporting, real-time dashboards.
- **Progressive decentralization**: Clear milestones to reduce admin key powers over time.

## Chain and Asset Strategy

- **Settlement layer**: Ethereum mainnet or a high-security L2 with mature tooling and decentralization guarantees.
- **Stable unit-of-account**: Diversified basket of reputable, fully-backed stablecoins and short-duration treasuries via tokenized T-bills; explicit counterparty risk limits.
- **Segregated wallets**: Distinct vaults for operating budget, subsidies, bounties, and reserves.

## Custody: Multi-Sig and Threshold Signatures

- **Primary control**: A battle-tested multi-signature safe with configurable modules and spending limits (e.g., Gnosis Safe).
  - Documentation: [Gnosis Safe](mdc:https://docs.safe.global/)
- **Threshold signing (advanced)**: Adopt a standard threshold signature scheme (e.g., FROST) for key ceremonies where appropriate.
  - Reference: [IETF CFRG draft: FROST](mdc:https://datatracker.ietf.org/doc/draft-irtf-cfrg-frost/)

### Signer Set and Policies

- **n-of-m policy**: Start with 6-of-11; minimum 1 signer per region across at least 4 regions; maximum 2 signers per entity.
- **Rotation**: Quarterly key rotation window; slashing/expulsion policy for inactivity or policy breaches.
- **Conflict-of-interest disclosures**: Public registry for all signers.

### Safeguards

- **Timelocks**: Mandatory 24–72h delay for large transfers above policy thresholds.
- **Guardians**: Independent guardian module to pause non-critical modules under narrowly defined conditions.
- **Spending limits**: Daily/weekly caps per vault; autonomous micro-spend module for low-risk bounties.

## Governance Interfaces

- **Proposal lifecycle**: On-chain proposals referencing signed, hash-committed budgets and vendor terms. Quorum and approval thresholds defined in the DAO constitution.
- **Module separation**: Upgrades gated by higher quorum; no emergency upgrade authority without two-tier approvals and time delay.
- **Moving beyond coin-voting**: Explore identity- and contribution-weighted voting to mitigate plutocracy risks ([Buterin, 2021](mdc:https://vitalik.ca/general/2021/08/16/voting3.html)).

## Auditing and Transparency

- **Open accounting**: All treasury addresses published; standardized tags for disbursements; hash-committed invoices.
- **Dashboards**: Real-time inflow/outflow, runway, subsidy allocation, and grant milestones.
- **Independent reviews**: Annual smart contract audits and semiannual operational audits with published reports.

## Incident Response

- **Runbooks**: Public emergency procedures for key compromise, oracle failure, or exploit.
- **Compensation fund**: Capped reserve for remediation with predefined governance path.

## Relationship to the 1% Treaty and $VICTORY Instruments

- **Funding path**: Initial capitalization via `\$VICTORY` bond/token issuance; long-term repayment and sustainability via 1% Treaty contributions.
- **Cross-references**: See [Victory Bonds Tokenomics](../../strategy/1-percent-treaty/victory-bonds-tokenomics.md) and [The 1% Treaty](../../strategy/1-percent-treaty/1-percent-treaty.md).

## Key External Benchmarks

- **Global military expenditure**: \$2.443 trillion (2023) and \$2.718 trillion (2024), per [SIPRI](mdc:https://www.sipri.org/media/press-release/2024/global-military-spending-surges-amid-war-rising-tensions-and-insecurity) and [SIPRI 2025 press release](mdc:https://www.sipri.org/media/press-release/2025/unprecedented-rise-global-military-expenditure-european-and-middle-east-spending-surges).

---

### Source Quotes for Key Parameters

* **SIPRI global military expenditure (2023)**
  > "Total global military expenditure reached \$2443 billion in 2023, an increase of 6.8 per cent in real terms from 2022."  
  > — SIPRI, Apr 2024, [Press release](mdc:https://www.sipri.org/media/press-release/2024/global-military-spending-surges-amid-war-rising-tensions-and-insecurity)

* **SIPRI global military expenditure (2024)**
  > "World military expenditure reached \$2718 billion in 2024, an increase of 9.4 per cent in real terms from 2023..."  
  > — SIPRI, Apr 2025, [Press release](mdc:https://www.sipri.org/media/press-release/2025/unprecedented-rise-global-military-expenditure-european-and-middle-east-spending-surges)

* **Gnosis Safe**
  > "Safe is a smart account infrastructure enabling secure and flexible management of digital assets on Ethereum and EVM-compatible networks."  
  > — Safe Docs, [docs.safe.global](mdc:https://docs.safe.global/)

* **FROST threshold signatures**
  > "FROST is a flexible round-optimal Schnorr threshold signature scheme, designed for practical deployment with support for key refresh and signer aggregation."  
  > — IETF CFRG Draft, [datatracker.ietf.org](mdc:https://datatracker.ietf.org/doc/draft-irtf-cfrg-frost/)

* **Beyond coin voting**
  > "We need to move beyond coin voting as it exists in its present form."  
  > — Vitalik Buterin, 2021, [vitalik.ca](mdc:https://vitalik.ca/general/2021/08/16/voting3.html)


