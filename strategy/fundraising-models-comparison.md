---
title: Fundraising Models Comparison — Selecting the Best Path for DIH
description: Comparison of fundraising options (Reg D/Reg S, Reg A+, Reg CF, token sales, grants) against our goals, with precedents and a clear recommendation.
published: true
date: '2025-01-20T00:00:00.000Z'
tags: fundraising-models, capital-raising, reg-d, reg-s, reg-a-plus, grants, public-goods, crypto, strategy
editor: markdown
dateCreated: '2025-01-20T00:00:00.000Z'
---

## Purpose

We compare viable fundraising models against the Decentralized Institutes of Health (DIH) initiative’s requirements: speed to capital, scale (\$1.2–\$2.5B), global reach, legal risk, investor inclusivity, and reputational integrity. The DIH will fund the dFDA platform and decentralized trials. We also identify proven public‑goods funding precedents and recommend a best‑fit approach.

## Evaluation Criteria

- **Speed:** months to first close
- **Capital scale:** realistic capacity in 12–24 months
- **Investor access:** accredited only vs. public (unaccredited)
- **Jurisdictional reach:** U.S. and international fit
- **Regulatory burden/risk:** upfront and ongoing
- **Cost:** legal, audit, underwriting, compliance
- **Reputation/compliance:** transparency, ethics; avoids pay‑to‑play optics

## Models Considered

### 1) Reg D 506(c) private placement (U.S. accredited)
- **Fit:** Fast, standard for high‑risk initiatives; unlimited raise from accredited investors; general solicitation allowed with accreditation verification.
- **Pros:** Speed; large checks; widely understood by VCs/FOs; pairs well with structured notes/bonds.
- **Cons:** Excludes unaccredited investors; U.S. only.

### 2) Reg S (offshore, non‑U.S. investors)
- **Fit:** Parallel track with Reg D to reach international investors without triggering SEC registration.
- **Pros:** Global capital access; can mirror terms with Reg D.
- **Cons:** Requires careful offering segregation and jurisdiction‑specific counsel.

### 3) Reg A+ (Tier 2) “mini‑IPO” (public, up to \$75M/yr)
- **Fit:** Allows unaccredited public participation once risk is reduced; SEC‑qualified offering with audited financials.
- **Pros:** Democratizes access; strong legitimacy for broad base; ongoing reporting manageable vs full IPO.
- **Cons:** Slower than Reg D/Reg S; capped at \$75M/yr; material preparation and review timeline.

### 4) Reg CF (crowdfunding) (up to ~\$5M/yr)
- **Fit:** Broad retail participation at very small caps.
- **Pros:** Inclusive; good for community alignment.
- **Cons:** Insufficient scale for our activation energy; heavy admin per dollar raised.

### 5) Public token sale/ICO (utility or governance token)
- **Fit:** Historically fast, but high enforcement and reputational risk; conflicts with election and securities constraints.
- **Pros:** Potential for rapid global participation.
- **Cons:** High likelihood of securities characterization; enforcement risk; volatile secondary markets; negative optics amid “pay‑to‑play” scrutiny.

### 6) Grant/Donation platforms (Gitcoin Grants, Optimism RetroPGF, foundation donations)
- **Fit:** Excellent for distributing funds to public goods; historically raised tens of millions, not billions.
- **Pros:** Strong alignment with public goods ethos; transparent; community‑driven.
- **Cons:** Not sized for \$1B+ activation energy; donation‑driven rather than return‑driven capital.

## Precedents in Crypto Public‑Goods Funding

- **Gitcoin:** Over **\$65M** distributed to public goods via grants, bounties, and quadratic funding.
- **Optimism RetroPGF:** More than **50 million OP tokens** allocated across rounds to impactful projects.
- **BitGive Foundation:** Early crypto philanthropy; received a **\$1M** donation from the Pineapple Fund.

## Recommendation

- **Phase 1 (Months 0–12):** Concurrent **Reg D 506(c) + Reg S** private placements to raise the initial \$250–\$400M activation energy rapidly from sophisticated U.S. and international investors.
- **Phase 2 (post‑milestones):** **Reg A+** qualified offering to include unaccredited public investors (up to \$75M/yr), after platform traction and de‑risking.
- **Distribution (ongoing):** For allocating treasury funds, adopt **Gitcoin‑style grants** and **Optimism‑style RetroPGF** mechanisms to transparently fund public‑good research at scale. Use grants for distribution, not for primary capital formation.
- **Liquidity discipline:** Defer any DEX listings until governance utility is fully live and the treasury is operational, to minimize securities risk and speculation optics.

This two‑phase path balances speed, scale, inclusivity, and compliance—suitable for a mission targeting \$27B/yr in reallocated government spend while maintaining ethical and legal integrity.

## Estimation Framework (How Much Each Channel Can Raise)

Use both top‑down caps/precedents and bottom‑up conversion funnels. Run bear/base/bull scenarios and compute expected value (EV). Update probabilities via a prediction market (e.g., Metaculus).

### 1) Reg D 506(c) (U.S. accredited)

Parameters per segment i (VC, family office, HNWI, crypto fund):
- Reachable targets: N_i; Contact rate: p_contact_i; Meeting rate: p_meet_i; Commit rate: p_commit_i; Accreditation pass: p_acc_i; Avg check: avg_check_i

Formula (12 months):
- Raise_RegD = Σ_i [N_i × p_contact_i × p_meet_i × p_commit_i × p_acc_i × avg_check_i]
- Guardrails: first close 60–120 days; typical avg_check_i ranges — VC: \$2–10M, FO: \$1–5M, HNWI: \$100–500k; subtract 15–30% KYC/ops friction.

### 2) Reg S (non‑U.S.)

By region j (EU, MEA, APAC, LATAM), apply local frictions f_law_j (0.7–0.9) and ops friction f_ops_j (0.7–0.9):
- Raise_RegS = Σ_j Σ_i [N_ij × p_contact_ij × p_meet_ij × p_commit_ij × f_law_j × f_ops_j × avg_check_ij]

### 3) Reg A+ (Tier 2)

Hard cap and funnel:
- Raise_RegA = min(\$75,000,000, months_live × T × CTR × signup × KYC_pass × invest_rate × avg_ticket)
- Benchmarks: CTR 1–3%; signup 10–20%; KYC_pass 70–90%; invest_rate 5–15%; avg_ticket \$300–\$1,500.

### 4) Reg CF

- Raise_RegCF = min(\$5,000,000, months_live × T × CTR × signup × KYC_pass × invest_rate × avg_ticket)
- Benchmarks: avg_ticket \$100–\$500; portal throughput constrains T.

### 5) Grants/Donations (Gitcoin/RetroPGF/Foundation)

- Raise_Grants = Σ_rounds (expected_midpoint × match_multiplier)
- Precedents: Gitcoin \$0.5–\$5M/round; RetroPGF 5–50M token‑equivalent over cycles; foundation gifts \$0.1–\$5M typical, rare 7–8 figures.

### 6) Portfolio, Scenarios, and EV

- Total_Base = RegD_base + RegS_base + min(\$75M, RegA_base) + min(\$5M, RegCF_base) + Grants_base
- EV_Total = Σ_channels Σ_scenarios [amount_channel,scenario × prob_channel,scenario]
- Policy/timeline adjustments: EV_adj = EV_Total × (1 − r_time) × (1 − r_policy)

Calibration starters (12 months):
- Reg D: \$250–\$400M; Reg S: \$100–\$250M; Reg A+: \$25–\$75M (6–12 months live); Reg CF: \$1–\$5M; Grants: \$2–\$10M.

---

## Source Quotes for Key Parameters

- **Gitcoin total distributed (\$65M+)**
  > “Gitcoin has distributed over \$65 million to projects through grants, bounties, and related products.”
  > — Axios, 2022, [Crypto public goods funding](mdc:https://www.axios.com/2022/08/23/crypto-public-goods-green-pill-gitcoin-advocacy-funding)

- **Optimism RetroPGF scale (50M OP)**
  > “Optimism has allocated more than 50 million OP tokens across multiple rounds of Retroactive Public Goods Funding.”
  > — Business Insider (Markets), 2024, [RetroPGF funding](mdc:https://markets.businessinsider.com/news/currencies/the-next-stage-for-public-good-funding-in-crypto-1033787594)

- **BitGive Pineapple Fund donation (\$1M)**
  > “BitGive received a \$1 million donation from the Pineapple Fund in 2017–2018.”
  > — Wikipedia, 2024, [BitGive Foundation](mdc:https://en.wikipedia.org/wiki/BitGive_Foundation)

- **Reg A+ cap (\$75M/yr)**
  > “Tier 2 of Regulation A permits eligible issuers to offer up to \$75 million in a 12‑month period, subject to SEC qualification.”
  > — SEC, 2024, [Regulation A](mdc:https://www.sec.gov/smallbusiness/exemptofferings/rega)
