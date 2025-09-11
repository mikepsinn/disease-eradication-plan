---
title: Fundraising Models Comparison — Selecting the Best Path for DIH
description: 'Comparison of fundraising options (Reg D/Reg S, Reg A+, Reg CF, token sales, grants) against our goals, with precedents and a clear recommendation.'
published: true
date: '2025-01-20T00:00:00.000Z'
tags: [fundraising-models, capital-raising, reg-d, reg-s, reg-a-plus, grants, public-goods, crypto, strategy]
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

### 5) Public token sale / ICO / Fair launch (Gnosis Auction, LBP)

- **Fit:** Token distribution through public sale or auction mechanisms (e.g., Gnosis Auction batched Dutch auctions; Balancer Liquidity Bootstrapping Pools).
- **Pros:** Potential for rapid global participation; transparent price discovery in auctions; mitigates sniping/whale dominance vs. fixed‑price ICOs.
- **Cons:** High likelihood of securities characterization; election‑law/optics risk; secondary‑market volatility; requires mature utility case to justify listing.

### 6) Juicebox DAO campaign (ConstitutionDAO‑style)

- **Fit:** Time‑boxed, on‑chain treasury raise via Juicebox with NFT receipts/perks; mainly donation‑based (no profit promises).
- **Pros:** Very fast setup; strong memetic energy; public transparency; low legal risk if structured as pure donations with no ROI claims.
- **Cons:** Donation caps; operational limits; not sized for \$1B+ activation energy; requires strict firewalling from U.S. election work.

### 7) Grant/Donation platforms (Gitcoin Grants, Optimism RetroPGF, foundation donations)

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

### 5) Juicebox DAO campaign

- Raise_Juicebox = campaign_days × daily_uniques × conv_rate × avg_donation × match_multiplier
- Benchmarks: ConstitutionDAO \$60M in weeks; but donation‑only; set conv_rate 0.2–1.0%, avg_donation \$50–\$500.

### 6) Public token sale / Auction (Gnosis Auction, LBP)

- Raise_Auction = min(demand_curve_at_clearing_price, compliance_haircut × ops_cap)
- Notes: model with pre‑registration soft commits; apply large haircuts for securities/election‑law risk until counsel greenlights.

### 7) Grants/Donations (Gitcoin/RetroPGF/Foundation)

- Raise_Grants = Σ_rounds (expected_midpoint × match_multiplier)
- Precedents: Gitcoin \$0.5–\$5M/round; RetroPGF 5–50M token‑equivalent over cycles; foundation gifts \$0.1–\$5M typical, rare 7–8 figures.

### 8) Portfolio, Scenarios, and EV

- Total_Base = RegD_base + RegS_base + min(\$75M, RegA_base) + min(\$5M, RegCF_base) + Juicebox_base + Auction_base + Grants_base
- EV_Total = Σ_channels Σ_scenarios [amount_channel,scenario × prob_channel,scenario]
- Policy/timeline adjustments: EV_adj = EV_Total × (1 − r_time) × (1 − r_policy)

Calibration starters (12 months):
- Reg D: \$250–\$400M; Reg S: \$100–\$250M; Reg A+: \$25–\$75M (6–12 months live); Reg CF: \$1–\$5M; Juicebox: \$2–\$20M sprint; Auction (if ever used): monitor only until compliance greenlight; Grants: \$2–\$10M.

## Semiquantitative Scoring (Criteria Weights and Scores)

Weights (sum = 1.0): Speed 0.20; Scale 0.25; Compliance 0.20; Global reach 0.10; Inclusivity 0.10; Cost 0.05; Optics 0.10.

Scores are 1 (poor) to 5 (excellent). Weighted score = Σ(weight × score).

| Option | Speed | Scale | Compliance | Global | Inclusivity | Cost | Optics | Weighted Score |
| --- | ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---:|
| Reg D 506(c) | 5 | 4 | 4 | 2 | 1 | 4 | 4 | 0.20×5 + 0.25×4 + 0.20×4 + 0.10×2 + 0.10×1 + 0.05×4 + 0.10×4 = **3.65** |
| Reg S | 4 | 3 | 3 | 5 | 2 | 3 | 4 | 0.20×4 + 0.25×3 + 0.20×3 + 0.10×5 + 0.10×2 + 0.05×3 + 0.10×4 = **3.30** |
| Reg A+ | 2 | 3 | 5 | 3 | 5 | 3 | 5 | 0.20×2 + 0.25×3 + 0.20×5 + 0.10×3 + 0.10×5 + 0.05×3 + 0.10×5 = **3.85** |
| Reg CF | 3 | 1 | 5 | 2 | 5 | 4 | 5 | 0.20×3 + 0.25×1 + 0.20×5 + 0.10×2 + 0.10×5 + 0.05×4 + 0.10×5 = **3.15** |
| Public token sale/ICO/Auction (Gnosis/LBP) | 5 | 4 | 1 | 5 | 5 | 4 | 2 | 0.20×5 + 0.25×4 + 0.20×1 + 0.10×5 + 0.10×5 + 0.05×4 + 0.10×2 = **3.25** |
| Juicebox DAO campaign | 5 | 2 | 4 | 4 | 5 | 5 | 4 | 0.20×5 + 0.25×2 + 0.20×4 + 0.10×4 + 0.10×5 + 0.05×5 + 0.10×4 = **3.95** |
| Grants/Donations | 3 | 2 | 5 | 4 | 5 | 5 | 5 | 0.20×3 + 0.25×2 + 0.20×5 + 0.10×4 + 0.10×5 + 0.05×5 + 0.10×5 = **3.85** |

Notes:
- Auction mechanisms improve fairness vs. fixed‑price ICOs but do not eliminate securities/optics risks without mature utility and counsel sign‑off.
- Juicebox scores high on speed/inclusivity/optics for donation‑only sprints; not a substitute for institutional activation capital.

## Downside, Reversibility, and “Try & See” Costs

- **Reg D 506(c):** If under‑raises, sunk legal/placement \$0.5–\$1.5M; time cost 2–4 months. Reversible; neutral optics if framed as pilot.
- **Reg S:** Sunk multi‑jurisdiction counsel \$0.3–\$1.0M; time 2–4 months; reversible with minimal optics risk.
- **Reg A+:** If not qualified or under‑subscribed, sunk legal/audit \$0.8–\$2.0M; time 6–12 months. Still useful for reputation and future rounds.
- **Reg CF:** Sunk \$50–\$200k; time 2–3 months; reputationally positive signal even if small.
- **Public token sale/ICO/Auction:** High downside—enforcement, potential personal liability, reputational damage; not easily reversible. Use only as a monitored scenario with counsel.
- **Juicebox DAO campaign:** Low financial downside; time‑boxed; reputationally positive if donation‑only with clear use‑of‑funds; firewall U.S. election operations.
- **Grants/Donations:** Low financial downside; time‑boxed campaigns can be run in parallel; reputationally positive.

## Portfolio and Parallelization Plan

- **Run in parallel (low conflict):** Reg D + Reg S + Grants/Donations + Juicebox campaign; prep Reg A+ in background (audits, offering circular).
- **Gate to public:** Launch Reg A+ only after milestone de‑risking (platform live, pilot referendums, anchor investors).
- **Community sprints:** Time‑boxed donation/NFT campaigns (no profit promises) to galvanize support and fund discrete goals; publish on‑chain dashboards/leaderboards.
- **Monitor high‑risk paths:** Track regulatory shifts for token‑sale/auction viability; do not deploy without counsel and clear green lights.

---

## Source Quotes for Key Parameters

- **Gitcoin total distributed (\$65M+)**
  > “Gitcoin has distributed over \$65 million to projects through grants, bounties, and related products.”
  > — Axios, 2022, [Crypto public goods funding](https://www.axios.com/2022/08/23/crypto-public-goods-green-pill-gitcoin-advocacy-funding)

- **Optimism RetroPGF scale (50M OP)**
  > “Optimism has allocated more than 50 million OP tokens across multiple rounds of Retroactive Public Goods Funding.”
  > — Business Insider (Markets), 2024, [RetroPGF funding](https://markets.businessinsider.com/news/currencies/the-next-stage-for-public-good-funding-in-crypto-1033787594)

- **BitGive Pineapple Fund donation (\$1M)**
  > “BitGive received a \$1 million donation from the Pineapple Fund in 2017–2018.”
  > — Wikipedia, 2024, [BitGive Foundation](https://en.wikipedia.org/wiki/BitGive_Foundation)

- **Reg A+ cap (\$75M/yr)**
  > “Tier 2 of Regulation A permits eligible issuers to offer up to \$75 million in a 12‑month period, subject to SEC qualification.”
  > — SEC, 2024, [Regulation A](https://www.sec.gov/smallbusiness/exemptofferings/rega)
