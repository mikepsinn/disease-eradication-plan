---
title: Incentives Layer for DIH/dFDA
description: Social and economic incentive mechanisms that drive growth, engagement, and funding for the 1% Treaty and decentralized trials, wired to on-chain modules, credentials, and public dashboards.
published: true
date: '2025-08-15T00:00:00.000Z'
tags: incentives, referrals, bounties, hypercerts, credentials, leaderboards, dfda, dih
editor: markdown
---

## Goals

- Maximize growth (pledges, funding, trials, outcomes) with verifiable, fraud-resistant incentives
- Reward real impact, not bureaucracy; minimize human discretion via rules and oracles
- Keep costs low (target ≤ $0.50 per verified action; best-case $0.20–$0.30)

## Components

- Referral engine
  - Performance awards + weekly leaderboards for top referrers (default denomination: VOTE points representing earned shares of [peace dividend value](../economic-models/peace-dividend-value-capture.md) pre‑treaty; cash-only pilots must follow [Legal Compliance Framework](./legal-compliance-framework.md))
  - Optional tree revenue-share with hard caps and anti-fraud rules (sharing real value creation stakes)
  - Verification tiers: email/phone → device fingerprint → eID as jurisdiction requires
  - KPIs: CPA, K-factor, verified-pledge velocity

- Reputation and credentials
  - Verifiable credentials (DID/VC) for roles and contributions (Fellows, Ambassadors, Reviewers)
  - Impact certificates/Hypercerts for referrals, merges, trial milestones; public explorer
  - Reputation boosts matching rates, bounty priority, and listing prominence
  - Slashing/blacklisting for fraud or COI violations

- Bounties, prizes, and merge-to-earn
  - Outcome bounties for evidence-producing milestones (pre‑treaty payouts in VOTE points representing earned shares of [peace dividend value](../economic-models/peace-dividend-value-capture.md); post‑treaty governed by VICTORY DAO per [DIH](./1-percent-treaty/decentralized-institutes-of-health.md))
  - Security/bug bounties; feature bounties with pay-on-merge (earning real value creation stakes)
  - Major prizes for critical platform capabilities that unlock the $16.5T annual peace dividend

- Quests and streaks
  - Weekly missions: recruit partners, publish translations, onboard sites, report outcomes
  - Streak multipliers; completion proofs via attestations

- Leaderboards and recognition
  - Individual, org, institute, and regional leaderboards
  - Recognition is earned, criteria-based, revocable; public directory with COI

- Ambassador performance pools
  - Regional/institute matching pools unlocked by meeting verified KPIs (pledges, enrollments, outcomes); default payouts in VOTE points representing earned ownership of [peace dividend value](../economic-models/peace-dividend-value-capture.md) created through successful advocacy

> Canonical references: [Legal Compliance Framework](./legal-compliance-framework.md), [VICTORY Bonds — Incentive Mechanics](./1-percent-treaty/victory-bonds-tokenomics.md), [Decentralized Institutes of Health](./1-percent-treaty/decentralized-institutes-of-health.md)
  - Transparent formulas; funds flow programmatically

## On-chain and oracle wiring

- Modules: Treasury (grants/QF, bounties, subsidies, VICTORY), Reputation, Subsidy vouchers
- Oracles: Identity/COI, Activity (referrals, merges, quests), Evidence (ranked outcomes), Safety (incidents)
- Credentials: EIP-712-signed attestations, W3C VC; role-bound actions require valid creds
- Dashboards: Auto-computed OKRs and KPIs; immutable logs replace reports

## Anti-fraud controls

- Sybil resistance: multi-factor, velocity caps, anomaly detection
- Manual review queue for flagged actions; whistleblower bounties
- Clawbacks for falsification; payout pauses on safety incidents

## KPIs

- Growth: CPA, K-factor, weekly active referrers, org/region activation
- Execution: bounties closed, merges, trial participants subsidized
- Impact: evidence generated, savings redeemed, incident rate/time-to-mitigation

## Privacy and compliance

- Minimize PII; selective disclosure; regional compliance (GDPR/CCPA)
- Public proofs without doxxing; aggregate stats by default

## Links

- [Referral engine and 3.5% rule](./referral-rewards-system.md)
- [Open ecosystem and bounty model](./open-ecosystem-and-bounty-model.md)
- [DIH On-Chain and AI Architecture](../architecture/dih-onchain-architecture.md)
- [DIH Treasury Architecture](../features/treasury/dih-treasury-architecture.md)
- [VICTORY Bonds — Bonds and Tokens Incentive Mechanics](./1-percent-treaty/victory-bonds-tokenomics.md)
- [DIH Org Structure](./1-percent-treaty/dih-org-structure.md)


