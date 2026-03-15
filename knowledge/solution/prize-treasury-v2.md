# Prize Treasury v2: The 15-Year Yield-Bearing Refund Clause

## Status: Live Proposal — Open for Wishocratic Challenge

**Proposal type:** Treasury rule amendment to the Earth Optimization Prize  
**Amendment number:** EOP-TA-001  
**Submitted:** 2026-03-15  
**Verification clause:** Optimitron snapshot at T+15 years  
**Effect if adopted:** Strict improvement on current design (dominates current rules on all donor-facing metrics)

---

## The One-Sentence Version

Park all contributions in yield-bearing safe assets; if Optimitron verifies zero cumulative gains across all adopting jurisdictions at the 15-year mark, every contributor receives their full principal plus all accrued returns.

---

## The Problem With the Current Design

The current Earth Optimization Prize is already a dominant-strategy investment for rational selfish actors. The dominant assurance contract handles the fundraising risk: if the prize threshold is never met, contributors get their money back plus a bonus. Once the threshold is met and capital is deployed, however, the refund clause expires. From that point forward, contributors bear the tail risk that the mechanism is fully funded, runs for years, and produces nothing — a scenario the model already prices at roughly 10% probability via the parasitic-economy collapse timeline.

This is the last real "lose" case for donors. The v2 amendment eliminates it.

---

## The Three-Paragraph Rule Amendment

**Rule 1 — Yield-Bearing Escrow (effective immediately upon adoption):**  
All contributions to the Earth Optimization Prize treasury shall be held in ultra-safe, liquid, yield-bearing instruments for the duration of the holding period. Acceptable instruments: U.S. Treasury bills (3–6 month ladder), investment-grade sovereign debt from AAA-rated issuers, audited stablecoin yield protocols with ≥$5B TVL and ≥24-month track record, or a diversified low-volatility index generating real returns above CPI. The treasury's investment mandate is preservation-first, yield-second. No speculative assets, no lockups exceeding 6 months, no instruments that cannot be liquidated within 72 hours. Accrued yield is credited pro-rata to each contributor's balance daily. Yield is not distributed until the 15-year snapshot; it compounds within the treasury.

**Rule 2 — 15-Year Global Failure Refund Clause:**  
On the exact 15-year anniversary of the first deployed dollar (the "Snapshot Date"), Optimitron shall perform a mandatory one-time global snapshot of the two terminal metrics: dHealthy_med (change in median healthy life-years across all adopting jurisdictions) and gIncome_med (change in median real income across all adopting jurisdictions). If cumulative verified gains in both terminal metrics equal zero across all adopting jurisdictions — meaning the mechanism has produced no measurable improvement in either metric in any jurisdiction that adopted it — then the refund clause activates. Every original contributor receives their full principal plus all accrued safe returns, distributed proportionally within 30 days of the Snapshot Date. If any verified gains have already triggered even $1 of milestone payouts prior to the Snapshot Date, the refund clause expires permanently and the remaining treasury stays in the perpetual outcome-based pool under the existing milestone release rules.

**Rule 3 — Early Depositor Bonus:**  
Contributors who deposit prior to the first $10M in committed capital receive a 5% bonus yield enhancement, funded by the prize organizer, payable either at the time of refund (if the refund clause activates) or at the time of the first milestone payout (if the mechanism succeeds). This maintains the dominant-assurance-contract property: contributing is the correct strategy regardless of your estimate of success probability, and contributing early is strictly better than contributing late.

---

## The Optimitron Verification Clause

The 15-year global failure snapshot shall proceed as follows:

1. **Trigger:** The Snapshot Date is defined as T₀ + 15 years, where T₀ is the Unix timestamp of the first on-chain treasury deposit exceeding $1,000.

2. **Metric definition (unchanged from current scorecard):**
   - dHealthy_med = (median healthy life-years at T₁₅) − (counterfactual median healthy life-years at T₁₅ under no-treaty baseline)
   - gIncome_med = (median real income at T₁₅) − (counterfactual median real income at T₁₅ under no-treaty baseline)
   - Counterfactual baseline: the pre-existing trend line extrapolated from T₋₁₀ through T₀, with standard demographic and economic adjustments

3. **Zero-gain definition:** Both metrics register ≤0 across the population-weighted average of all jurisdictions that formally adopted any element of the plan (signed the treaty, passed Right-to-Trial equivalent legislation, or deployed IABs). A single jurisdiction showing positive gains in both metrics, with verifiable causal linkage to plan adoption, is sufficient to defeat the zero-gain finding.

4. **Verification process:** Optimitron runs its standard adversarial scoring protocol. A 90-day dispute window follows the preliminary snapshot. Any party may submit evidence of positive gains; the burden of proof for the refund clause is on the claimant (i.e., the refund activates only if nobody successfully demonstrates positive gains). After 90 days with no successful challenge, the refund clause executes automatically via smart contract. No human override is possible.

5. **Oracle stack:** Same layered stack as milestone verification (UMA optimistic oracle + Kleros appeals court + 15-of-21 trustee multisig as backstop). The refund execution itself is fully automated once the dispute window closes.

6. **Edge case — partial adoption:** If fewer than 3 jurisdictions formally adopted the plan by T₁₅, the snapshot is deferred by 5 years (to T+20) to allow for the possibility that the plan simply wasn't deployed at sufficient scale to measure. This prevents the refund clause from triggering due to non-adoption rather than mechanism failure.

---

## Expected Value Model: How Much Faster Do Capital Raises Hit?

### Baseline (current design)

Under the current dominant assurance contract, contributing is already positive EV. The key variables:

- p(success) = probability the mechanism catalyzes treaty adoption = ~3% (conservative)
- V(success) = societal value if it works = $101T/year perpetually, with ~$862,000 in personal economic value per $1 donated (at current model parameters)
- V(failure) = $0 net financial return to contributor (money is deployed, no refund)
- EV_current = (0.03 × $862,000) + (0.97 × $0) = **$25,860 per dollar donated**

Even at 0.1% success probability: EV = **$862 per dollar donated**. This already dominates every known philanthropic investment.

### v2 Design

Under the yield-bearing treasury + 15-year refund clause:

- V(failure) is no longer $0 — it becomes +4–6% annualized over 15 years = **+79–140% return on principal** in the failure branch
- The downside is now: opportunity cost only (your capital was in T-bills instead of your brokerage, earning similar returns)
- EV_v2 = (0.03 × $862,000) + (0.97 × $1.10) = **$25,861.07 per dollar donated**

The EV is almost identical because the upside already dominates. But this framing obscures the actual behavioral impact.

### Why the EV Model Undersells the v2 Effect

The relevant variable isn't EV — it's **participation rate among donors with standard risk preferences.**

Consider a donor with $10M who:
- Currently evaluates: "3% chance of enormous upside, 97% chance of losing $10M" → high risk aversion, chooses not to participate
- Under v2 evaluates: "3% chance of enormous upside, 97% chance of getting $11–14M back" → **this is now literally risk-free from their perspective**

Standard prospect theory: humans weight losses approximately 2.5× more heavily than equivalent gains. The current design asks donors to absorb a potential $10M loss. The v2 design eliminates that loss entirely. The behavioral delta between "possible total loss" and "worst case: you profit" is not marginal. It is the difference between a niche product and a mass-market product.

### Estimated Capital Raise Acceleration

| Donor segment | Current participation rate (estimated) | v2 participation rate (estimated) | Multiplier |
|---|---|---|---|
| Institutional philanthropists ($10M+) | ~0.5% | ~8% | 16× |
| HNWI ($1M–$10M) | ~2% | ~25% | 12× |
| Retail EA donors ($10K–$1M) | ~15% | ~60% | 4× |
| Small donors (<$10K) | ~30% | ~65% | 2× |

**Overall capital raise multiplier: estimated 8–20× vs. current design.**

This is consistent with the empirical literature on dominant assurance contracts (Tabarrok 1998, subsequent experimental work): eliminating downside risk in a public goods contribution problem typically increases participation by one to two orders of magnitude when the donor population includes significant risk-averse actors — which $10M+ institutional donors almost universally are.

The model already prices in a 10% baseline collapse probability (the parasitic-economy clock). Under the v2 design, the 15-year refund clause converts that collapse scenario from "donors lose their money AND civilization degrades" to "donors profit on their T-bill returns AND civilization degrades." This is not a minor tweak. It transforms the prize's risk profile from "moonshot philanthropy" into "strictly dominant financial instrument with moonshot upside" — a categorically different product that accesses a categorically different pool of capital.

---

## Why This Is Strictly Better

The v2 amendment is a Pareto improvement over the current design:

1. **Donors are strictly better off:** No financial downside in any outcome. The failure branch is now profitable.
2. **Prize integrity is preserved:** The refund only triggers if ZERO gains are verified — meaning the mechanism genuinely failed. Any partial success defeats the refund clause.
3. **Incentives are preserved:** Implementation spend still happens upfront. Real gains still trigger milestone payouts. The yield on escrowed funds is a cost to the organizer (the bonus kicker), not a drain on the prize pool.
4. **Optimitron's role is unchanged:** Same adversarial verification, same 28-metric scorecard, same causal attribution requirements. The 15-year snapshot uses the existing protocol.
5. **The self-improving property is unchanged:** If a challenger submits a better treasury design than this one, the prize funds the better design instead. This document is itself subject to the mechanism it describes.

The only cost: organizer must fund the 5% early depositor bonus, and treasury management requires marginally more operational overhead (investing in T-bills vs. holding cash). Both are trivially small relative to the prize pool and the expected capital raise acceleration.

---

## Smart Contract Upgrade Requirements

Additional fields required in `DominantAssurancePrize.sol`:

```solidity
// Treasury v2 additions
address public yieldVault;              // address of yield-bearing vault (e.g., Aave USDC, T-bill tokenizer)
uint256 public snapshotDate;            // T0 + 15 years in Unix timestamp
uint256 public earlyDepositThreshold;   // $10M in USDC (1e13 with 6 decimals)
uint256 public earlyBonusRate;          // 500 = 5%
bool public refundClauseActive;         // true until first milestone payout
bool public refundClauseTriggered;      // true after zero-gain snapshot confirmed

mapping(address => uint256) public depositTimestamp;
mapping(address => bool) public earlyDepositor;

// New functions
function investInYieldVault() external onlyTreasury;
function performSnapshotVerification() external onlyOptimitron;
function activateGlobalFailureRefund() external onlyOracleAfterDispute;
function claimYieldRefund() external onlyAfterRefundActivated;
```

The yield vault integration can use ERC-4626 (standardized vault interface) — compatible with Aave, Compound, and tokenized T-bill protocols like Ondo Finance or Superstate. This means the yield mechanism can be deployed without custom code.

---

## How to Challenge This Proposal

This is a live Wishocratic proposal. To defeat it:

1. Produce a treasury design that scores higher on the 28-metric scorecard than this amendment
2. Submit it with your projected improvement in dHealthy_med and/or gIncome_med relative to this design
3. If Optimitron verifies your design is better, the prize funds yours instead

That's it. The mechanism is working correctly if this document gets replaced by something better.

**Submit challenges to:** prize.warondisease.org (once live)  
**This proposal will remain the baseline** until a strict improvement is demonstrated.

---

*"The least-bad idea just got less bad. We expect this to happen again."*

*prize.warondisease.org*
