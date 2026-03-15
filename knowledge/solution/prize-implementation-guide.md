# How to Create the Prize (Technical Implementation)

## The Three Tiers

You can launch a fork of this prize today, this week, or this quarter, depending on how decentralized you want it.

---

## Tier 1: Today (Zero Code, Existing Platforms)

A reader finishes the prize page, wants to create their own version, and can do it in under an hour using platforms that already exist:

### Option A: HeroX (herox.com)
- **What it is:** Prize challenge platform (founded by XPRIZE team). Used by NASA, DARPA, governments.
- **How:** Create a challenge → paste the 28-metric scorecard → set prize pool → invite solvers
- **Cost:** Free to launch, HeroX takes a platform fee on prizes
- **Prize pool funding:** Challenge creator funds it, or crowdfunds from supporters
- **Judging:** You appoint judges or use community voting
- **Limitation:** Centralized. No automatic refund if no winner. No assurance contract.
- **Best for:** Established organizations who want a branded challenge fast

### Option B: Gitcoin Grants (gitcoin.co)
- **What it is:** Crypto-based public goods funding with quadratic funding
- **How:** Create a grant → describe the prize → community funds it → quadratic matching multiplies small donations
- **Advantage:** Quadratic funding means 1,000 people donating $1 each gets MORE matching than 1 person donating $1,000. Rewards broad support.
- **Limitation:** Crypto-native, which limits participation. Not prize-structured (more like funding).
- **Best for:** Crypto/web3 communities, EA-adjacent groups

### Option C: GoFundMe / Kickstarter / Open Collective
- **What it is:** Standard crowdfunding
- **How:** Create campaign → "Fund the Least Bad Idea Prize" → collect pledges → hold funds in escrow
- **GoFundMe:** No all-or-nothing, funds available immediately. Good for collecting.
- **Kickstarter:** All-or-nothing (assurance-contract-like! Funds return if goal not met)
- **Open Collective:** Transparent finances, fiscal hosting, great for recurring/institutional
- **Limitation:** No built-in prize adjudication. You manage judging manually.
- **Best for:** Getting started immediately with zero technical overhead

### Option D: Manifold Markets + Metaculus
- **What it is:** Prediction markets
- **How:** Create a market: "Will the Earth Optimization Plan (or a strict improvement) be implemented by 2035?"
- **Why:** Doesn't fund the prize directly, but creates a real-time probability estimate that makes the expected-value case visible. If the market says 3% and the payoff is $101T/year, the expected value is $3T/year. That's a number people react to.
- **Best for:** Signal generation, attracting attention, complementing a funded prize

**Minimum viable fork: Create a HeroX challenge with the 28-metric scorecard, link to prize.warondisease.org as the reference implementation, and set whatever prize pool you can fund. Time: 1 hour. Cost: $0 to launch.**

---

## Tier 2: This Week (Simple Smart Contract)

For the assurance contract version — where contributors get their money back if no winner is found — you need a smart contract. But it's simpler than you'd think.

### The Assurance Contract

An assurance contract is the simplest mechanism that makes contributing safe: if the funding threshold is never reached, every contributor gets their money back. No threshold = no deployment = no risk. This is different from a donation — you are not committing anything until enough other people commit too.

Applied to the prize:
1. **Contributors pledge funds** to the prize pool (ETH, USDC, or fiat via bridge)
2. **If a winner is certified** (beats the baseline on 28 metrics) → funds go to winner
3. **If the threshold is never met** → funds returned in full to every contributor
4. **Contributing is low-risk** because the worst case is your money sat in an escrow for a while and came back

The yield-bearing treasury (see below) makes this a no-lose proposition: while your funds are in escrow awaiting threshold, they earn safe returns. Fail-to-threshold means you get back more than you put in. No organizer-funded bonus required — the T-bills provide it.

### Technical Requirements

```
Smart Contract: AssurancePrize.sol

State variables:
- scorecard: bytes32[] (hash of 28 metric definitions)
- baseline: uint256[] (current best scores from Earth Optimization Plan)
- fundingDeadline: uint256 (block timestamp — threshold must be hit by this date)
- snapshotDate: uint256 (T0 + 15 years — global failure refund trigger)
- pledges: mapping(address => uint256)
- totalPledged: uint256
- yieldVault: address (ERC-4626 compatible yield vault)
- judges: address[] (multisig or DAO)
- winner: address (zero until certified)
- refundClauseActive: bool (true until first milestone payout)

Functions:
- pledge() → deposit funds into yield vault, record contributor
- certifyWinner(address, uint256[] scores) → judges submit scores, if scores beat
  baseline on all 28 metrics, winner is set; refundClauseActive = false
- claimPrize() → winner withdraws funds
- claimRefund() → if fundingDeadline passed without hitting threshold, contributor
  gets pledge + accrued yield
- activateGlobalFailureRefund() → callable by oracle after snapshot confirms zero
  cumulative gains at snapshotDate; only if refundClauseActive = true
- claimGlobalFailureRefund() → after activateGlobalFailureRefund(), contributor
  gets pledge + 15 years of accrued yield
- challengeScores() → adversarial challenge period (30 days after certification)

Deployment cost: ~$50-200 in gas on Ethereum L2 (Base, Arbitrum, Optimism)
Development time: 1-2 weeks for a competent Solidity developer
Audit: ~$5K-20K for a basic audit (important for trust)
```

### Existing Building Blocks

- **Juicebox (juicebox.money):** Programmable treasury for crowdfunding projects on Ethereum. Already supports refund mechanics. Could be adapted for assurance contracts with minimal custom code.
- **Superfluid:** Streaming payments. Could enable continuous prize funding (pledge $1/month to the prize, automatically).
- **Kleros:** Decentralized court for dispute resolution. Could serve as the judging mechanism — adversarial, crypto-native, already handles complex disputes.
- **Snapshot:** Off-chain voting. Could handle the "certify winner" decision via token-weighted or reputation-weighted vote.
- **Safe (formerly Gnosis Safe):** Multisig wallet for holding prize funds with multiple judges required to release.

### Simplest Smart Contract Path

1. Deploy a Juicebox project with refund enabled
2. Use Snapshot for judge voting on winner certification
3. Use Kleros as appeals court for adversarial challenges
4. Prize funds held in Safe multisig controlled by judges
5. Total build time: 1-2 days using existing tools. Cost: near zero.

---

## Tier 3: This Quarter (The Prize Factory)

For "theoretically billions of decentralized prizes," you need a factory contract — a smart contract that deploys new prize instances.

### The Prize Factory

```
Contract: LeastBadIdeaPrizeFactory.sol

Anyone can call:
- createPrize(
    scorecard,      // the 28 metrics (standardized)
    baseline,       // current best scores to beat
    scope,          // "global" | "US" | "cancer" | "Alzheimers" | custom
    deadline,       // when the prize expires
    bonusRate,      // refund bonus if no winner
    judges,         // who certifies the winner
    minPledge       // minimum total before prize activates
  ) → returns new prize contract address

Each prize instance is independent but:
- Uses the same standardized scorecard (cross-comparable)
- Shares a global registry (everyone can see all active prizes)
- Winners in one prize can submit to all compatible prizes
- A solution that wins a cancer-specific prize automatically qualifies for the global prize if it covers that module
```

### What This Enables

- **A parent creates a prize:** "Cure my child's rare disease" — $500 pool, 3 metrics relevant to that disease
- **A billionaire creates a prize:** "Implement the full Earth Optimization Plan" — $100M pool, all 28 metrics
- **A university creates a prize:** "Best policy evaluation of the 1% Treaty" — $50K pool, Q_policy and Q_budget metrics
- **A government creates a prize:** "Find $1T in recoverable waste in our budget" — $10M pool, NSV_gain metric
- **A DAO creates a prize:** "Build the dFDA" — $1M pool, medical throughput metrics
- **All prizes use the same scorecard** — a team that builds a great dFDA module wins the DAO prize AND qualifies as a module for the billionaire's full-bundle prize

The prizes compose. Like Lego. Each one is independent, but they all fit together because the scorecard is standardized. A thousand small prizes, each funding one module, collectively fund the complete implementation. No central coordinator needed.

### Registry and Discovery

```
Contract: PrizeRegistry.sol

- All active prizes listed with scope, pool size, deadline
- Leaderboard of highest-funded prizes
- Challenger submissions visible across all compatible prizes
- Total pledged across all forks (the "global prize pool" number)

Frontend: prize.warondisease.org/forks
- Browse all active prize forks
- Filter by scope, size, deadline
- One-click "Create Your Fork" button
- Dashboard showing: total global prize pool, number of forks, number of challengers
```

### The Viral Loop

1. Reader reads prize.warondisease.org
2. Clicks "Create Your Fork" → deploys a prize contract in 30 seconds
3. Shares with friends → "I created a $100 prize to end war and disease. If nobody wins, I get $105 back."
4. Friends pledge → prize pool grows
5. Friends create their OWN forks → network grows
6. Total global prize pool displayed on every fork's page → social proof compounds
7. At some dollar threshold, serious teams start competing → the mechanism works

**The key insight:** You don't need one person to fund a $1B prize. You need a million people to fund a $1,000 prize each. The factory + assurance contract + standardized scorecard makes this possible. Each person's contribution is a no-lose bet (refund if threshold never met, yield-bearing treasury if deployed), so contributing is the correct decision regardless of your beliefs about success probability.

---

## Treasury Design

### Yield-Bearing Escrow

All contributions sit in ultra-safe, liquid, yield-bearing instruments from the moment they're deposited — not inert cash. Acceptable instruments: U.S. Treasury bills (3–6 month ladder), investment-grade sovereign debt from AAA-rated issuers, or audited stablecoin yield protocols with ≥$5B TVL and ≥24-month track record. The mandate is preservation-first, yield-second. No speculative assets, no lockups exceeding 6 months, no instruments that can't be liquidated within 72 hours. Accrued yield is credited pro-rata to each contributor daily and compounds within the treasury until either a milestone payout or a refund event.

This makes the assurance contract a no-lose proposition without any organizer-funded bonus: if the threshold is never met, contributors get back principal + yield. The T-bills provide the bonus.

### The 15-Year Global Failure Refund Clause

The assurance contract handles the pre-deployment risk: if the threshold is never reached, money comes back. But once the threshold is met and capital is deployed, the refund clause normally expires. This is the one remaining scenario where a contributor could lose — the mechanism is funded, runs for years, and produces nothing.

The 15-year clause closes this gap.

**Rule:** On the exact 15-year anniversary of the first deployed dollar (the "Snapshot Date"), Optimitron performs a mandatory one-time global snapshot of the two terminal metrics: dHealthy_med and gIncome_med across all adopting jurisdictions. If cumulative verified gains in both metrics equal zero — meaning the mechanism produced no measurable improvement in any jurisdiction that adopted it — then the refund clause activates: every contributor receives their full principal plus all accrued safe returns within 30 days.

**Trigger condition for refund:**
- Optimitron verifies ≤0 gains in both terminal metrics across population-weighted average of all adopting jurisdictions
- No party successfully demonstrates positive gains during the 90-day dispute window following the snapshot
- `refundClauseActive` is still `true` (no milestone payouts have occurred)

**Defeat condition (refund clause expires):**
- Any verified gains trigger even $1 of milestone payouts → `refundClauseActive = false` → remaining treasury stays in the perpetual outcome-based pool

**Edge case — insufficient adoption:** If fewer than 3 jurisdictions formally adopted the plan by T+15, the snapshot is deferred to T+20. This prevents the refund from triggering because the plan wasn't deployed at sufficient scale to measure, rather than because it failed.

**Verification process:** Same oracle stack as milestone verification — UMA optimistic oracle + 90-day dispute window + Kleros appeals court + 15-of-21 trustee multisig as backstop. Execution is fully automated once the dispute window closes. No human override.

### Why This Makes Contributing a Strictly Dominant Strategy

| Outcome | What happens to your contribution |
|---|---|
| Threshold never met | Principal + yield returned (assurance refund) |
| Threshold met, mechanism works | Prize funds the winner; you benefit from a world with less war and disease |
| Threshold met, mechanism runs 15 years, zero verified gains | Principal + 15 years of accrued yield returned (global failure refund) |

There is no outcome in which a rational contributor loses money. The downside is opportunity cost: your capital earned T-bill returns instead of whatever else you would have done with it. The upside is unchanged: the mechanism works, and 10.7 billion lives are saved.

The behavioral implication is significant. Standard prospect theory weights losses ~2.5× more heavily than equivalent gains. The current prize already has a positive expected value that dwarfs any alternative investment. The treasury design eliminates the loss branch entirely — which is the difference between "positive EV philanthropy that requires overcoming loss aversion" and "strictly dominant financial instrument that selfish actors pile into regardless of their beliefs about success probability."

---

## Recommended Path

1. **Today:** Create a HeroX challenge + Open Collective fund. Cost: $0. Time: 2 hours.
2. **This week:** Deploy a Juicebox project with refund mechanics. Get the first pledges.
3. **This month:** Build the simple smart contract (DominantAssurancePrize.sol). Audit it.
4. **This quarter:** Build the Prize Factory. Add "Create Your Fork" to prize.warondisease.org.
5. **Ongoing:** Every reader becomes a potential prize creator. The network grows without central coordination.

The prize that selects the best plan for ending war and disease should itself be the best example of decentralized coordination. If it requires a central authority to run, it has already failed its own test.

---

*"We are not sure why your civilization does not already have a machine like this."*

*Now you do. Fork it.*
