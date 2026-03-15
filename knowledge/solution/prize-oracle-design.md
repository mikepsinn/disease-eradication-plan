# Prize Oracle Design: Who Decides Who Won?

## The Problem

You have a smart contract holding potentially billions of dollars. Someone claims they've implemented the Earth Optimization Plan. Who verifies? Who releases the funds? Every design choice here is a trade-off between three things:

1. **Accuracy** — did the claimant actually win?
2. **Theft resistance** — can bad actors steal the funds?
3. **Speed** — how fast can a legitimate winner get paid?

Pick two. Then engineer the third back in.

There's a prior question most prize designs skip: **why are you using human judges at all when you've already built a machine that scores proposals against 28 metrics?** The answer is: you shouldn't be. Optimitron is the primary evaluator. Everything else is either input verification (did this real-world event happen?) or governance (what should the scorecard measure?). Those are different problems with different tools.

---

## The Three Problems, Clearly Separated

### Problem 1: Scoring — Did the claimant beat the baseline?
**Tool: Optimitron**

This is what Optimitron exists to do. It takes a submitted plan, runs it against the 28-metric scorecard, compares it to the current baseline, and outputs a score. There is no reason a human judge panel or token-staked jurors should be doing this. They are not better at it. They are worse at it and corruptible.

Optimitron's scoring is:
- Deterministic given the same inputs (auditable)
- Adversarially challengeable (anyone can submit counter-evidence that changes the inputs)
- Transparent (all inputs, weights, and outputs published on-chain)
- Self-improving (the scorecard and baseline are themselves subject to Wishocracy governance — see Problem 3)

### Problem 2: Factual verification — Did the claimed real-world events actually happen?
**Tool: Optimistic oracle + Kleros for disputes**

Optimitron scores plans. It does not verify that a law was actually passed, that a trial was actually run, or that bond dividends were actually paid. Those are factual claims about the real world. This is where the optimistic oracle + Kleros stack earns its place — not for evaluating whether a plan is good, but for verifying that claimed events occurred.

### Problem 3: Governance — Who decides the rules?
**Tool: Wishocracy**

What counts as the 28 metrics? How should the baseline be updated? Who are the trustees? What happens when Optimitron's model itself is challenged? These are value-laden collective decisions. Wishocracy is the correct mechanism: pairwise preference aggregation across all stakeholders, no concentrated veto, no appointed committees.

---

## Why Previous Approaches Fall Short

**Judge panels:** Capturable at scale. For a prize large enough to matter, the financial incentive to corrupt 5 of 7 judges exceeds the reputational cost. Works for small prizes ($10K–$1M). Fails precisely when it needs to work most.

**Kleros for scoring:** Kleros is excellent at adversarial factual disputes. It is not equipped to evaluate 28 interconnected policy metrics. Random token-staked jurors are not better scorers than Optimitron. They're slower, more expensive, and more manipulable. Kleros belongs in the factual verification layer, not the scoring layer.

**Prediction markets as signal:** Prediction markets aggregate speculative price signals — what are traders betting on? Wishocracy aggregates actual stakeholder preferences — what do participants want? For a system that's building Wishocracy, the signal layer should be Wishocracy polls, not Polymarket. This also turns every signal query into a running Wishocracy experiment on real infrastructure.

**UMA Optimistic Oracle for outcome scoring:** UMA is excellent at verifying factual claims optimistically. It is not a policy evaluation engine. For Milestone 7 (full implementation, all 28 metrics), UMA alone is the wrong tool. Optimitron scores; UMA verifies the inputs Optimitron scored against.

---

## The Recommended Stack

```
Layer 1: SMART CONTRACT (holds funds, enforces milestones)
  - Juicebox or custom Solidity contract
  - Time-locked releases (7-day delay after oracle confirms)
  - Emergency pause (Wishocracy-elected trustees can freeze if fraud detected)
  - Yield vault integration (ERC-4626) — funds earn returns while held

Layer 2: SCORING (did the claimant beat the baseline?)
  - Optimitron runs the 28-metric scorecard against submitted plan
  - All inputs, weights, and outputs published on-chain
  - 90-day adversarial window: anyone may submit counter-evidence
  - If counter-evidence changes any input → Optimitron rescores
  - Score is deterministic given inputs; disputes are about inputs, not the model

Layer 3: FACTUAL VERIFICATION (did the claimed events happen?)
  - Milestones 1, 5: On-chain data (vote counter, bond payments — no oracle needed)
  - Milestones 2, 3, 6: UMA Optimistic Oracle (submit proof + 30-day dispute window)
  - Milestones 4, 7: UMA + Optimitron scoring of trial/implementation results
  - Kleros decentralized court for disputed factual claims only
    (Did this legislation pass? Was this trial published? Did these payments occur?)

Layer 4: GOVERNANCE (who decides the rules?)
  - Wishocracy governs: scorecard updates, baseline revisions, trustee election,
    rule amendments, fork certification, scope disputes
  - Pairwise preference voting across all registered stakeholders
  - No appointed committees, no founding-team veto
  - The prize rules themselves are subject to Wishocracy —
    if a majority of stakeholders prefer a different rule, it wins
  - Wishocracy results are published on-chain before taking effect;
    30-day implementation delay for transparency

Layer 5: WATCHDOG INCENTIVES (everyone is watching)
  - 5% of each milestone's funds reserved as dispute bounty
  - Anyone who successfully challenges a false factual claim gets the bounty
  - Anyone who submits valid counter-evidence that changes an Optimitron score
    gets a bounty proportional to the scoring delta
  - Result: for every milestone, thousands of people are economically incentivized
    to verify inputs and catch fraud

Layer 6: SIGNAL LAYER (real-time probability estimates)
  - Wishocracy polls embedded on prize.warondisease.org for each milestone
  - Shows real-time stakeholder preferences (not speculative price signals)
  - Does NOT trigger fund release
  - Doubles as live Wishocracy experiment: results are the data
  - Early warning: sudden preference shift triggers watchdog investigation
```

---

## The Milestone Ladder

```
Milestone 1: REFERENDUM THRESHOLD (5% of funds)
  Trigger: warondisease.org vote counter reaches 280M verified votes
  Verification: On-chain counter (smart contract reads directly)
  Scoring: N/A — binary event
  Theft risk: Very low — you'd have to fake 280M votes

Milestone 2: FIRST LEGISLATION (10% of funds)
  Trigger: Right-to-Trial or equivalent legislation passes in any jurisdiction
  Verification: UMA Optimistic Oracle (submit proof + 30-day dispute window)
  Evidence: Government gazette, official legal database
  Scoring: N/A — binary event
  Theft risk: Low — legislation is public record

Milestone 3: FIRST COUNTRY SIGNS (15% of funds)
  Trigger: First country commits to 1% reallocation (binding treaty or law)
  Verification: UMA + Kleros on dispute
  Evidence: UN treaty database, government records
  Scoring: N/A — binary event
  Theft risk: Low — treaty signatures are the most publicly verifiable events on Earth

Milestone 4: FIRST TRIAL FUNDED (15% of funds)
  Trigger: First pragmatic trial funded by treaty-redirected money produces results
  Verification: UMA (trial published in peer-reviewed journal)
  Scoring: Optimitron scores trial results against dHealthy_med contribution
  Theft risk: Medium — Optimitron scoring is adversarially challengeable

Milestone 5: BOND RETURNS VERIFIED (15% of funds)
  Trigger: Incentive Alignment Bond investors receive first dividend
  Verification: On-chain (if tokenized) or audited financial statement via UMA
  Scoring: N/A — binary event
  Theft risk: Low — financial flows are auditable

Milestone 6: FIVE COUNTRIES SIGN (15% of funds)
  Trigger: Five countries commit to treaty
  Verification: Same as Milestone 3 (UMA + Kleros on dispute)
  Scoring: N/A — binary event
  Theft risk: Very low

Milestone 7: FULL IMPLEMENTATION (25% of funds)
  Trigger: All 28 scorecard metrics meet or exceed baseline
  Verification: UMA (real-world events submitted as evidence)
  Scoring: Optimitron full scorecard run; 90-day adversarial window
  Wishocracy: Any disputed metric weights resolved via stakeholder vote
  Theft risk: Lowest — requires faking implementation across 28 dimensions
    AND surviving Optimitron scoring AND 90 days of adversarial challenge
```

---

## Anti-Theft Properties

| Attack | Defense |
|---|---|
| Bribe the judges | No judge panel for scoring. Optimitron scores; inputs are on-chain and adversarially challengeable. |
| Corrupt Optimitron's scoring | Inputs are public. Anyone who catches a wrong input gets a bounty. Scoring is deterministic — change the inputs, the score changes automatically. |
| Fake a milestone | 30-day dispute window + watchdog bounties. Factual claims are public record. |
| Manipulate the signal layer | Wishocracy polls don't trigger fund release. Manipulation is visible and self-defeating. |
| Steal via smart contract exploit | Time-locked releases. Emergency pause. Audited contract. |
| Social engineer the trustees | Trustees are Wishocracy-elected, not appointed. Replacing them requires winning a preference vote, not corrupting individuals. |
| Submit false legislation proof | Legislation is public record. 30-day dispute window for anyone on Earth to challenge. |
| Drain funds gradually | On-chain transparency. Every movement visible. Watchdog bounties for unauthorized transfers. |
| Capture the governance layer | Wishocracy requires majority preference, not majority stake. One person one vote, not one dollar one vote. Capturing it requires genuinely persuading the majority. |
| Challenge Optimitron's model | Valid — this is a feature. Better model = better scores = better outcomes. Governance upgrades via Wishocracy. |

**The meta-property:** The mechanism that makes the prize work (distributed self-interest > concentrated self-interest) also makes it theft-resistant. Optimitron's transparency means more eyes on every score. Wishocracy's governance means no single actor controls the rules. Watchdog bounties mean prize size and defender count scale together. Theft resistance increases with prize size.

---

## What To Build First

1. **Today:** Describe the Optimitron scoring layer and Wishocracy governance on prize.warondisease.org
2. **This month:** Deploy simple contract with Milestone 1 (vote counter) + Wishocracy-elected trustee multisig
3. **This quarter:** Integrate UMA optimistic oracle for Milestones 2–3; launch Wishocracy polls as signal layer
4. **When needed:** Full Optimitron scoring integration for Milestones 4, 7; Kleros for factual disputes

Start simple. The Optimitron + Wishocracy architecture scales from a $10K prize to a $1B prize without changing the fundamental design. The tools that work at small scale are the same tools that work at large scale — which is how you know you've picked the right tools.

---

*The oracle problem is the last refuge of "this can't work." Optimitron scores. Wishocracy governs. Now it can.*
