# Open Tasks

## Week 1: Entities + first revenue (zero SEC question)

- [ ] **Form Wyoming holdco LLC + operating LLC for t-shirts.** ~$500 in fees. DIY-able. Sell t-shirts immediately.
- [ ] **Pay first 100 seed wearers from ICEWD treasury.** $50 each (~$5K total). 501(c)(3) program disbursement, not securities activity. No regulatory question.
- [ ] **Start foundation outreach for the {{< var shirt_seed_program_total_usd >}} seed ask.** Grant-making is zero regulatory question. Parallel-track to seed wearer launch.

## Weeks 2-4: Prize Fund v1 opens (low SEC risk)

- [ ] **One-hour securities-attorney conversation, $2K.** Specifically: confirm ICEWD as a 501(c)(3) can accept restricted-gift deposits with refund provisions tied to objective oracle conditions. Get an opinion letter.
- [ ] **Public dashboard build.** Page at warondisease.org showing pool size, every deposit (hashed wallet), every wire, allocation breakdown, Scoreboard distance-to-trigger, projected failure-branch refund/dollar. Backend: read-only over the custodian's API + the existing parameter system.
- [ ] **Open Prize Fund deposit window with a $5M cap.** Use ICEWD as the charitable wrapper. First deposit = host's own treasury ($100-$1000). Anchors the pool and proves the wire-to-ledger-to-dashboard loop.
- [ ] **Custodian shortlist + selection.** Mercury Treasury (USD), Anchorage Digital (multi-asset), bank trust department. Criteria: segregated client funds, audit trail export, beneficiary-designation support.

## Months 2-3: Tokens + scale (medium SEC risk, well-covered)

- [ ] **Wyoming DAO LLC for VOTE token issuance.** Use the [March 2026 SEC Interpretive Release](https://www.sec.gov/files/rules/interp/2026/33-11412.pdf) five-token taxonomy as cover: VOTE tokens are "digital tools" (utility-based, earned through verified-voter recruitment, not pre-purchased as an investment). Skip PRIZE tokens; the deposit mechanism replaces them.
- [ ] **State money-transmitter opinions.** Before accepting deposits or token activity from NY or CA residents, get a per-state opinion. State regulators are independent of Atkins and aggressive.

## Engineering

- [ ] **Treaty-cut slider widget.** Embeddable widget that lets a user set the proposed military-redirect percentage (default 1%, max 50%, min 0%) and watches every downstream number recalculate in real time. Lands on the shirt QR-code page as the primary call-to-action. See [The Funniest Joke in the Universe](knowledge/appendix/joke.qmd) for context.

## Visual Assets

- [ ] **Joke paper images.** Generate the bw-academic image set for `knowledge/appendix/joke.qmd` matching the conventions of other papers. Use `assets/images/global-referendum/global-referendum-section-qr-code-t-shirts-bw-academic.jpg` as the wearable-surface reference.
- [ ] **Joke paper favicon and OG image.** `assets/icons/joke-favicon.png` and `assets/og/joke-og-1200x630.jpg`. Subject: a T-shirt with the visible text "END WAR & DISEASE" in bold sans-serif.

## Distribution

- [ ] **Push v2 of joke paper to Zenodo.** Includes Primary Risk section, governance cross-refs, tightened title/description, em-dash fixes. Concept DOI `10.5281/zenodo.20336705` stays stable; new version DOI issued.
