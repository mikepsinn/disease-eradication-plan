---
title: "Dynamic Expected Value Incentive Policy"
description: Real-time, risk-adjusted compensation model using Expected Value calculations and prediction markets to price risk.
published: false
date: "2025-08-24T00:00:00.000Z"
tags: ["incentives", "tokenomics", "team", "algorithmic", "expected-value", "prediction-markets"]
dateCreated: "2025-08-24T00:00:00.000Z"
topic_id: team-incentives
canonical: true
status: draft
domains: ["dih"]
doc_type: policy
---

# Dynamic Expected Value (EV) Incentive Policy

This document outlines a novel incentive structure for the founding team, core contributors, and key advisors of the War on Disease initiative. It moves beyond both conventional time-based vesting and static risk multipliers to a dynamic system that rewards verifiable, high-impact work and early-stage risk. This policy for the core team is distinct from the program for external or task-based contributions, which is detailed in the [Open Ecosystem and Bounty Model](./open-ecosystem-and-bounty-model.md).

## 1. The Core Principle: Expected Value Compensation

The goal is to ensure the **Expected Value (EV)** of a contributor's at-risk compensation is always equal to the real value of the labor they are putting at risk.

The formula is: **`Expected Value = Probability of Success * Final Payout`**

This means that if a contributor performs work when the perceived chance of success is low, their potential payout upon success must be proportionally high to compensate them for the enormous risk they are taking.

## 2. The Model: How It Works

### Step 1: Valuing At-Risk Contribution

We use the "Salary + At-Risk Contribution" model to solve the "people need to eat" problem and value the work being put at risk.

- **Determine Market Rate:** Each role has a fair market salary (e.g., Senior Engineer: $200,000/year).
- **Pay a Base Cash Salary:** A portion of the market rate (e.g., 60%, or $120,000) is paid in cash/stablecoin.
- **Calculate At-Risk Contribution:** The remainder is the "at-risk" portion. (e.g., $200k - $120k = **$80,000**). This is the value the contributor is investing in the project.

### Step 2: Using a Prediction Market as a Risk Oracle

We will use a live prediction market (e.g., on Polymarket or Metaculus) to provide a real-time, decentralized measure of the project's probability of success.

- **The Market:** "Will the 1% Treaty be ratified by at least one G7 nation by 2030?"
- **The Output:** The market's live probability is our `P(success)`. For example, `P(success) = 2%`.

### Step 3: Granting "Success Grants" with a Commitment Bonus

For every dollar of at-risk work a contributor performs, they are awarded a corresponding amount of **Success Grants**. To optimally align incentives and conserve the project's cash runway, we apply a **Commitment Bonus** to the at-risk portion, making it mathematically superior to taking cash.

The formula to calculate the grant is:

**`Success Grants ($) = (At-Risk Contribution $) x (1 + Commitment Bonus) / P(success)`**

- **Commitment Bonus:** A fixed **15%** bonus that rewards contributors for forgoing cash compensation in favor of at-risk tokens.
- **Example:**
  - Our engineer performs their $80,000 of at-risk work when `P(success)` is 2%.
  - The value of their contribution is boosted by the bonus: `$80,000 * 1.15 = $92,000`.
  - `Success Grants = $92,000 / 0.02 = $4,600,000`
  - They have now earned a claim on **$4.6 million** worth of value, which has a higher expected value ($92k) than the cash they gave up ($80k).

## 3. Incentive Mechanics: Connecting Grants to Tokens

To make the Success Grants meaningful, they must map to a share of the network.

- **Success Valuation:** We define a target valuation for the project at the time of the main capital raise (Phase 2). For modeling purposes, we set this at **$5 Billion**.
- **Team Allocation Pool Value:** The 20% team allocation pool is therefore worth **$1 Billion** upon success (`$5B * 0.20`).
- **Calculating Ownership:** A contributor's ownership of the team pool is their share of the total value.
  - _Example:_ The engineer's $4.6M in Success Grants represents `$4,600,000 / $1,000,000,000 = 0.46%` of the team's token pool.

At the Token Generation Event, their accumulated Success Grants are converted into a corresponding number of VICTORY bonds.

## 4. Post-Distribution Incentives: Governance Staking

To ensure long-term alignment after tokens are distributed, we will implement a **Governance Staking** model.

- **Purpose:** To encourage active, long-term participation in the ecosystem's governance over short-term speculation.
- **Mechanism:**
  1.  **Governance Power:** Only VICTORY bonds that are "staked" (locked in a smart contract) can be used to vote on DIH funding proposals.
  2.  **Staking Yield:** To reward this commitment, stakers will receive a pro-rata share of a portion of the DIH's annual income, providing a sustainable yield for those who actively govern the treasury.

## 5. Advantages of this Model

- **Mathematically Fair:** It is the most precise method to reward risk. It algorithmically gives the highest rewards to the earliest, most courageous contributors.
- **Radically Transparent:** All inputs to the formula (market rates, hours, prediction market odds) are transparent and auditable.
- **Market-Driven:** It removes subjective decisions about what a "Risk Multiplier" should be and replaces it with a live, market-driven price of risk.
- **Optimally Aligned:** The Commitment Bonus and Staking Yield create powerful, rational incentives for contributors to prioritize the long-term success of the project at every step.
