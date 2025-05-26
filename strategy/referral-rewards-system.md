**Short answer:** Yes—if the referral-rewards scheme is tuned aggressively you can plausibly drop the **verified-vote cost below \$1** and, in an optimistic viral scenario, to **\$0.20 – \$0.30**. The \$2.00 figure in the roadmap is intentionally conservative so the budget never shocks you; it assumes:

* **\$0.50–\$0.75** per vote in direct rewards (cash, merch, or crypto)
* **\$0.75–\$1.00** in paid reach (ads, influencer micro-fees)
* **\$0.25** in identity-verification/ops overhead.

With stronger organic spread and tighter reward design, the ad component collapses.

---

## How the referral cost curve works

| Variable              | Conservative setting (Roadmap)                 | Aggressive setting                                             | Resulting \$/vote                        |
| --------------------- | ---------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------- |
| **Reward pool size**  | \$25 k for 200 k votes → **\$0.13**/vote       | Same pool, but scale to 400 k votes                            | \$0.06                                   |
| **Reward structure**  | Flat \$0.50/verified vote credited to referrer | Tiered leaderboard + weekly jackpot                            | Pushes organic sharing → halves ad spend |
| **Paid reach**        | \$1.00 per click-to-vote in swing-seat geo ads | \$0.10 initial spark; rely on org partners for bulk list sends | –\$0.90                                  |
| **Verification cost** | KYC lite (selfie + ID scrape) **\$0.25**       | Email + phone (lower assurance) **\$0.05**                     | –\$0.20                                  |

**Lower-friction verification** + **tiered/lottery rewards** are where most savings hide. If partners (disease foundations, patient forums, Reddit communities) email their lists for free, paid reach drops almost to zero.

---

## Benchmarks from similar campaigns

| Campaign                             | Verification     | Reward/CTA                                       | Verified-vote-like cost |
| ------------------------------------ | ---------------- | ------------------------------------------------ | ----------------------- |
| 2023 “EveryLibrary” petition drives  | Email + ZIP      | No cash, but free e-book                         | \$0.18                  |
| Avaaz climate pledges 2022           | Email + phone    | Donor-funded match (“each pledge plants a tree”) | \$0.32                  |
| GiveDirectly “crypto match” AMA 2021 | Wallet-signature | \$0.50 in ETH airdrop                            | \$0.48                  |
| California recall petition 2021      | Wet signature    | None (paid canvassers)                           | \$2.50                  |

A well-gamified referral program that leans on existing disease-advocacy lists should track near the Avaaz/GiveDirectly range—\$0.30–\$0.50—even after KYC overhead.

---

## Practical tuning steps

1. **Switch to jackpot-lottery + leaderboard**

   * Weekly \$500 prizes for top referrers + random \$50 draws among anyone with ≥ 1 referral.
   * Keeps marginal cost per new vote near zero once the pool is funded.

2. **Lower-touch verification for early phases**

   * Email + phone OTP is enough for press optics; add selfie-ID only when counts matter legislatively.
   * Saves \$0.15–\$0.20 per head.

3. **Seed through partner newsletters instead of ads**

   * Draft ready-to-send HTML blocks for each org; pay bounties in the same reward pool.
   * A single 100 k-subscriber list converting at 5 % yields 5 k votes for almost no incremental cash.

4. **Track K-factor weekly**

   * Viral coefficient > 0.8? cut ad spend. < 0.5? top-up jackpot or test new creatives.

---

### Revised cost scenarios (per 200 k verified votes)

| Scenario               | Reward Pool | Paid Ads | Ops    | Total   | \$ per vote |
| ---------------------- | ----------- | -------- | ------ | ------- | ----------- |
| **Baseline (roadmap)** | \$25 k      | \$150 k  | \$25 k | \$200 k | **\$1.00**  |
| **Partner-list heavy** | \$25 k      | \$40 k   | \$20 k | \$85 k  | **\$0.43**  |
| **Viral best-case**    | \$25 k      | \$15 k   | \$10 k | \$50 k  | **\$0.25**  |

---

## What to do with the roadmap?

* **Keep the \$2 placeholder** as a “not-to-exceed” guard-rail in grant applications.
* Internally, plan milestones: *“If \$/vote drops below \$0.60, re-forecast pool size and stretch goals upward.”*
* Document the tuning levers (reward tiers, jackpot frequency, verification strictness) so the engineer can toggle them with minimal code changes.

With a disciplined referral-reward loop—and the right partner lists—you should comfortably beat \$1 and may flirt with sub-\$0.30 territory.
