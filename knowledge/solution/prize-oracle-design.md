# Prize Oracle Design: Who Decides Who Won?

## The Problem

You have a smart contract holding potentially billions of dollars. Someone claims they've implemented the Earth Optimization Plan. Who verifies? Who releases the funds? Every design choice here is a trade-off between three things:

1. **Accuracy** — did the claimant actually win?
2. **Theft resistance** — can bad actors steal the funds?
3. **Speed** — how fast can a legitimate winner get paid?

Pick two. Then engineer the third back in.

---

## Option 1: Single Prediction Market

**How it works:** Create a market on Polymarket/Manifold: "Has the Earth Optimization Plan (or strict improvement) been verifiably implemented by [date]?" When the market resolves YES, funds release.

**Failure modes:**
- ❌ **Market manipulation.** Someone with $100M could temporarily push the market to YES and trigger payout to a confederate. The prize pool IS the incentive to manipulate.
- ❌ **Binary resolution.** A prediction market says IF something happened, not WHO caused it. You need to pay a specific winner.
- ❌ **Resolution oracle.** Who resolves the prediction market? You've just moved the oracle problem one level up.

**Verdict:** Useful as a SIGNAL (shows real-time probability), terrible as a TRIGGER. Use prediction markets alongside the prize, not as the oracle.

---

## Option 2: Judge Panel (Multisig)

**How it works:** 7 respected judges. 5-of-7 must sign to release funds to a winner.

**Failure modes:**
- ❌ **Collusion.** 5 judges agree to split the prize pool among themselves via a fake "winner."
- ❌ **Bribery.** Cheaper to bribe 5 judges than to actually end war and disease.
- ❌ **Capture.** Judges become the concentrated interest that the prize is designed to overcome.
- ⚠️ **Single point of failure.** All 7 judges die/disappear/become unreachable → funds locked forever.

**Mitigation:** Make judges high-profile enough that collusion destroys their reputation. Nobel laureates, heads of major foundations, etc. Reputational cost of collusion must exceed the prize pool share.

**Verdict:** Works for small prizes ($10K-$1M) where the reputational cost of cheating exceeds the financial gain. Does NOT work for large prizes where the financial incentive overwhelms reputation.

---

## Option 3: Kleros (Decentralized Court)

**How it works:** Random jurors selected from a pool of staked participants. Adversarial process — anyone can challenge a ruling. Multiple rounds of appeal, each with more jurors, make manipulation exponentially more expensive.

**How Kleros works specifically:**
1. Winner submits claim + evidence to Kleros court
2. Random jurors (staked PNK tokens) are selected
3. Jurors review evidence against the 28-metric scorecard
4. Ruling issued. 30-day appeal window.
5. If appealed: double the jurors, re-review. Can appeal multiple times.
6. Each appeal round costs the loser more (disincentivizes frivolous appeals)
7. Jurors who vote with the majority keep their stake; minority jurors lose theirs (Schelling point mechanism)

**Failure modes:**
- ⚠️ **Whale attack.** Someone buys enough PNK to dominate jury selection. Mitigation: Kleros has stake-weighted selection that makes this very expensive for high-value cases.
- ⚠️ **Complexity.** Evaluating 28 metrics requires expertise. Random jurors may not understand the scorecard. Mitigation: specialized Kleros courts for technical disputes.
- ✅ **Multiple appeals** make manipulation exponentially expensive. To steal a $1B prize via Kleros, you'd need to corrupt jurors across 5+ appeal rounds, each with double the jurors.

**Verdict:** Best existing decentralized option. Good for the appeals/dispute layer. Not ideal as the primary oracle for complex multi-metric evaluation.

---

## Option 4: UMA Optimistic Oracle

**How it works:**
1. Winner submits claim: "I have implemented functions X, Y, Z with scores A, B, C"
2. Claim is published. 30-day dispute window.
3. If nobody disputes → claim is accepted, funds release.
4. If disputed → goes to UMA's Data Verification Mechanism (token holders vote on truth)
5. Disputant must post a bond (skin in the game)

**Why "optimistic":** It assumes claims are true unless someone proves otherwise. This works because the incentive to dispute a false claim (you get the disputant bond + a share of the prize) is strong enough to guarantee that false claims get caught.

**Failure modes:**
- ⚠️ **Apathy attack.** If nobody is watching, a false claim goes through unchallenged. Mitigation: multiple watchdog bounties — anyone who successfully disputes a false claim gets a reward.
- ⚠️ **Slow.** 30-day windows + potential disputes = months to finalize. But this is a feature for a prize this large — speed is less important than accuracy.
- ✅ **Very hard to steal.** You'd need to submit a false claim AND ensure nobody on the entire internet disputes it for 30 days. For a prize worth millions+, that's effectively impossible.

**Verdict:** Excellent primary oracle. The "optimistic" assumption + economic incentive to dispute = very robust.

---

## Option 5: Milestone-Based Release (RECOMMENDED)

**The key insight: Don't release all funds at once.**

Instead of one giant prize, break it into milestones. Each milestone has its own verification, its own oracle, and releases a fraction of the funds. This means:

- At any given time, only a fraction of funds are at risk
- Each milestone is easier to verify than the whole plan
- Early milestones can use simpler oracles (on-chain data)
- Later milestones can use more complex oracles (as the system matures)
- A thief would have to fake EVERY milestone, not just one

### The Milestone Ladder

```
Milestone 1: REFERENDUM THRESHOLD (5% of funds)
  Trigger: warondisease.org vote counter reaches 280M verified votes
  Oracle: On-chain counter (objective, no judge needed)
  Verification: Smart contract reads the counter directly
  Theft risk: Very low — you'd have to fake 280M votes

Milestone 2: FIRST LEGISLATION (10% of funds)
  Trigger: Right-to-Trial or equivalent legislation passes in any jurisdiction
  Oracle: Optimistic oracle (UMA) — submit proof of legislation + 30-day dispute window
  Verification: Link to government gazette / official legal database
  Theft risk: Low — legislation is public record

Milestone 3: FIRST COUNTRY SIGNS (15% of funds)
  Trigger: First country commits to 1% reallocation (binding treaty or law)
  Oracle: Optimistic oracle + Kleros appeals court
  Verification: UN treaty database, government records
  Theft risk: Low — treaty signatures are the most publicly verifiable events on Earth

Milestone 4: FIRST TRIAL FUNDED (15% of funds)
  Trigger: First pragmatic trial funded by treaty-redirected money produces results
  Oracle: Optimistic oracle + expert panel review
  Verification: Published trial results in peer-reviewed journal
  Theft risk: Medium — need expert evaluation of trial quality

Milestone 5: BOND RETURNS VERIFIED (15% of funds)
  Trigger: Incentive Alignment Bond investors receive first dividend
  Oracle: On-chain verification (if bonds are tokenized) or audited financial statement
  Verification: Auditable financial flows
  Theft risk: Low — financial flows are auditable

Milestone 6: FIVE COUNTRIES SIGN (15% of funds)
  Trigger: Five countries commit to treaty
  Oracle: Same as Milestone 3
  Verification: UN records
  Theft risk: Very low

Milestone 7: FULL IMPLEMENTATION (25% of funds)
  Trigger: All 28 scorecard metrics meet or exceed baseline
  Oracle: Full Kleros court + UMA optimistic oracle + expert panel
  Verification: Comprehensive audit against scorecard
  Theft risk: Lowest — requires faking implementation across 28 dimensions
```

### Why This Is Theft-Resistant

1. **No single point of failure.** Stealing requires compromising 7 different oracles.
2. **Graduated risk.** Early milestones release small amounts with simple oracles. Large amounts require complex verification.
3. **Real-world anchoring.** Most milestones are anchored to events that are publicly verifiable (legislation, treaties, published trials). You can't fake a UN treaty signing.
4. **Time distribution.** Milestones are spread over years. A thief would need to maintain a fraud across multiple verification events over a long period.
5. **Watchdog incentives.** Anyone who catches a false milestone claim gets a bounty from the disputed funds.

---

## The Recommended Stack

```
Layer 1: SMART CONTRACT (holds funds, enforces milestones)
  - Juicebox or custom Solidity contract
  - Time-locked releases (7-day delay after oracle confirms)
  - Emergency pause (multisig can freeze if fraud detected)

Layer 2: PRIMARY ORACLE (verifies milestones)
  - Milestones 1, 5: On-chain data (no human oracle needed)
  - Milestones 2, 3, 6: UMA Optimistic Oracle (30-day dispute window)
  - Milestones 4, 7: UMA + Expert panel review

Layer 3: DISPUTE RESOLUTION (appeals court)
  - Kleros decentralized court for all disputed claims
  - Multiple appeal rounds, each more expensive to manipulate
  - Final backstop: 15-of-21 multisig of high-profile trustees

Layer 4: WATCHDOG INCENTIVES (everyone is watching)
  - 5% of each milestone's funds reserved as dispute bounty
  - Anyone who successfully challenges a false claim gets the bounty
  - This means: for every milestone, thousands of people are economically incentivized to verify it

Layer 5: PREDICTION MARKET (signal, not trigger)
  - Polymarket/Manifold market for each milestone
  - Shows real-time probability estimates
  - Does NOT trigger fund release (avoids manipulation)
  - Serves as early warning: if market suddenly spikes, watchdogs investigate

Layer 6: TRANSPARENCY (deterrence)
  - All fund movements on-chain and publicly visible
  - Dashboard showing: total funds, milestone status, oracle decisions, disputes
  - Prize page displays everything in real-time
  - Theft requires stealing in public, from thousands of watchers, across multiple verification events
```

---

## The Anti-Theft Properties (Summary)

| Attack | Defense |
|---|---|
| Bribe the judges | No single judge panel. Milestones use different oracles. |
| Fake a milestone | 30-day dispute window + thousands of watchdogs incentivized to catch you |
| Manipulate prediction market | Market is signal only, not trigger. Can't release funds by moving a market. |
| Steal via smart contract exploit | Time-locked releases (7-day delay). Emergency pause multisig. Audited contract. |
| Collude with oracle | Different oracles for different milestones. Would need to compromise UMA + Kleros + expert panel + multisig. |
| Submit false legislation proof | Legislation is public record. 30-day window for anyone on Earth to dispute. |
| Drain funds gradually | On-chain transparency. Every movement visible. Watchdog bounties for catching unauthorized transfers. |
| 51% attack on Kleros | Exponentially expensive across multiple appeal rounds. For a $1B prize, would cost more than the prize. |
| Social engineering the multisig | 15-of-21 threshold. Signers are public figures. Would need to compromise 15 separate people without any of the other 6 noticing. |

**The meta-property:** The same design principle that makes the prize work (stronger self-interest = stronger mechanism) makes it theft-resistant. The watchdog bounties mean that the more money in the prize, the more people are watching, the harder it is to steal. Theft resistance scales with prize size. This is the opposite of most financial systems, where larger pools attract more sophisticated attackers. Here, larger pools attract more sophisticated defenders.

---

## What To Build First

1. **Today:** Describe the milestone structure on prize.warondisease.org
2. **This month:** Deploy simple contract with Milestone 1 (vote counter) + multisig backstop
3. **This quarter:** Integrate UMA optimistic oracle for Milestones 2-3
4. **When needed:** Add Kleros court, expert panels, full stack

Start simple. Add complexity as the prize pool grows. A $10K prize doesn't need Kleros. A $10M prize does. A $1B prize needs all six layers. The architecture scales with the stakes.

---

*The oracle problem is the last refuge of "this can't work." Now it can. Fork it.*
