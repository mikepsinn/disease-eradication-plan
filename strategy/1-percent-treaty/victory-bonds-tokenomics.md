---
title: $VICTORY Instruments — Bonds and Tokens Tokenomics
description: Economic design for $VICTORY bonds/tokens used to bootstrap the DIH Treasury and repay contributors via 1% Treaty inflows.
published: true
date: 2025-08-12T00:00:00.000Z
tags: victory-bonds, tokenomics, treasury, fundraising, securities-compliance, roi
editor: markdown
dateCreated: 2025-08-12T00:00:00.000Z
---

## Overview

`\$VICTORY` instruments finance the initial DIH Treasury to fund patient subsidies, prizes, and platform build-out. Repayment is designed to come from sovereign contributions pledged under the [1% Treaty](./1-percent-treaty.md). This document defines the instrument types, cash flows, incentives, and guardrails.

## Instrument Options

1. **`\$VICTORY` Bonds (Debt-like)**
   - Fixed coupon with defined maturity; repayment funded by 1% Treaty flows and program cash flows.
   - Transfer-restricted until compliance checks clear (jurisdiction-dependent).
2. **`\$VICTORY` Tokens (Utility/Governance-linked)**
   - Used to fund verifiable actions (e.g., referendum referrals) and optionally confer governance rights.
   - Not designed to promise profits; avoid financial-return claims to mitigate securities risk.

## Cash Flow Model (Illustrative)

- Target raise: initial `\$50M–\$500M` program treasury.
- Coupon: 2–6% floating with performance step-down if treaty inflows exceed thresholds.
- Maturity: 5–10 years; optional amortization tied to inflow receipts.
- Seniority: Program senior; explicit waterfall published on-chain.

## Collateral and Repayment Sources

1. 1% Treaty sovereign contributions into DIH Treasury vault(s).
2. Earmarked portion of philanthropic and corporate partner inflows.
3. Optional reinsurance/guarantee facilities if available.

## Transparency and Protections

- On-chain escrow accounts; monthly proofs of reserves and liabilities.
- Public dashboards showing: inflows, coupon accruals, coverage ratio, and runway.
- Independent audits and covenant checks; breach → automated pause and governance review.

## Compliance Considerations (Non-legal summary)

- U.S. securities analysis should assume the **Howey** test may apply to bond-like or return-bearing instruments.
  - Reference: SEC v. W.J. Howey Co., 328 U.S. 293 (1946).
- Potential exemptions: **Reg CF**, **Reg A**, **Reg S** (offshore) depending on offer scope and investor base.
  - [SEC: Regulation Crowdfunding](mdc:https://www.sec.gov/resources-small-businesses/exempt-offerings/regulation-crowdfunding)
  - [SEC: Regulation A overview](mdc:https://www.sec.gov/smallbusiness/exemptofferings/rega)
  - [SEC: Regulation S resources](mdc:https://www.sec.gov/rules-regulations/1998/02/offshore-offers-sales-regulation-s-effective-date-60-days-after-publication-federal-register)
- KYC/AML: Mandatory for purchasers under most pathways.
- Jurisdictional strategy: staggered launches; geoblocking as required.

## Referral Funding Linkage

- `\$VICTORY` tokens can fund verifiable actions in the [Referral Rewards System](../referral-rewards-system.md) with anti-fraud rules and public ledgers.

## Relationship to DIH Treasury

- All terms, caps, and covenants mirrored in the [DIH Treasury Architecture](../../features/treasury/dih-treasury-architecture.md) with enforcement via on-chain modules.

---

### Source Quotes for Key Parameters

* **SEC Regulation Crowdfunding**
  > "Regulation Crowdfunding enables eligible companies to offer and sell securities through crowdfunding."  
  > — U.S. SEC, [sec.gov](mdc:https://www.sec.gov/resources-small-businesses/exempt-offerings/regulation-crowdfunding)

* **Regulation A overview**
  > "Regulation A provides an exemption from the registration requirements... for offerings of securities up to \$75 million in a 12-month period, subject to eligibility, disclosure, and reporting requirements."  
  > — U.S. SEC, [sec.gov](mdc:https://www.sec.gov/smallbusiness/exemptofferings/rega)

* **Regulation S (offshore)**
  > "The amendments are designed to stop abusive practices in connection with offerings of equity securities purportedly made in reliance on Regulation S."  
  > — U.S. SEC, [sec.gov](mdc:https://www.sec.gov/rules-regulations/1998/02/offshore-offers-sales-regulation-s-effective-date-60-days-after-publication-federal-register)


