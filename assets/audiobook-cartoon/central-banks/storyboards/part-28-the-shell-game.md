---
format: 1920x1080
duration: 2:29.8
message: "Raising medical funding 50% while printing 50% more money for everything leaves the 604-to-1 ratio untouched, which is why medical research has shrunk as a share of the economy for fifty years while finance and billing grew."
arc: Title card: three shells, and the press shuffling them → today, a pill bottle against a tower of $2.72 trillion: 604 to 1; five years later, flashbulbs, a giant +50% check and patted backs, while the press prints 50% more of everything, both bars grow, and the scientist's bigger check buys the same one flask → fifty years along a line that goes nowhere, a tiny hop at the end, and YOU's skeleton holding the promotion cake → what grew: finance, missiles in disguise, and billing; the pie gets bigger, the scientist gets crumbs, and a flag says PROGRESS
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 28, "The Shell Game"
audio: central-banks.a2bae1b9.mp3, 80:32.7 to 83:02.5
version: v2
---

# Part 28 storyboard: "The Shell Game"

- **Source:** `knowledge/economics/central-banks.qmd`, "The Shell Game (How Inflation Steals Medical Progress)", "The Proof: 50 Years of Going Nowhere" and "What Actually Grew". The narration is `central-banks.prepared.txt`.
- **The numbers:**
  - `global_government_clinical_trials_spending_annual`: $4.5 billion a year.
  - `global_military_spending_annual_2024`: $2.72 trillion a year.
  - `military_to_government_clinical_trials_spending_ratio`: 604 (to 1).
  - Five years later, both up 50%: about $6.75 billion against about $4.08 trillion; still 604 to 1 (derived).
  - Hardcoded in the chapter, not parameters: medical research as a % of GDP, 1975 0.08%, 1985 0.07%, 1995 0.07%, 2005 0.06%, 2015 0.06%, 2025 0.065%; absolute dollars up 10 times.
  - What grew (hardcoded): financial sector 3% to 8% of GDP (the narrator's figure; the chapter text now says 4% to 8%, and Part 30's narration says "about four percent"); military-industrial 3% to 3.4% (official); healthcare 7% to 18%.
- **What the viewer must leave with:** a raise for medicine means nothing if the printer raises everything else by the same amount; the share that goes to research has fallen for fifty years.
- **Plates:**
  - `ratio-chart`: a two-bar chart on aged paper, CLINICAL TRIALS and MILITARY, its axis in dollars; a shop counter to its right.
  - `fifty-years`: one long sheet of chart paper, 1975 to 2025: on the left a line chart, MEDICAL RESEARCH AS A % OF GDP; on the right three pairs of bars, 1975 and now, and the pie on a table.
- **Cast:** existing: `fed-crank-up` / `fed-crank-down`, `pill-bottle`, `missile` (stacked into the tower, and in disguise with a `fedora` and a `moustache`), `politician`, `scientist`, `scientist-flask`, `paycheck` (the giant check), `cash-register`, `you`, `you-skeleton`, `germ`, `till-receipt` (the stack of invoices), `cobweb`. From earlier parts: `bank` (Part 5). From Part 27: `pie`. New: `shells`, `promotion-cake`.
- **Callbacks:** the 604-missile tower and the pill bottle from Part 27. Part 27's pie comes back bigger. The PROGRESS flag goes round the loop in Part 31.
- **New art:**
  - `shells`: three walnut shells and a pea.
  - `promotion-cake`: a sheet cake with a candle on it.
  - In code: the headlines, the +50% on the check, the price tags, the health-insurance card and its confetti, the DENIED stamp, the PROGRESS flag.
- **Kit additions:**
  - `rescale`: a chart's axis relabels while its bars grow, so the picture does not change (both bars up 50%).
  - `walk-line`: a cut-out walking along a chart's line, rising and falling with it.

## Scene 1 · shell-game-title

- id: shell-game-title
- act: Title
- transition_in: up from black
- cue: "The Shell Game"
- time: 80:32.7 to 80:40.9 (8.3 s)
- voiceover: "The Shell Game (How Inflation Steals Medical Progress). This is the trick. Watch the money:"
- layer: A, title card
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Shell Game (How Inflation Steals Medical Progress)." | The heading. | The period card, THE SHELL GAME. The Federal Reserve press's crank-arm reaches into the card, sets out three walnut shells and puts a medicine bill under one. | |
| "This is the trick. Watch the money:" | | It shuffles the shells, faster and faster. | It lifts all three: all empty. |

Sound: a carnival organ; shells clattering; a ta-da on the empty lift.

## Scene 2 · six-hundred-and-four-to-one

- id: six-hundred-and-four-to-one
- act: The shell game
- transition_in: cut
- cue: "Today"
- time: 80:40.9 to 81:32.2 (51.2 s)
- voiceover: "Today. Government clinical trials cost four point five billion dollars. Global military spending is two point seventy-two trillion dollars. The ratio is six hundred and four to one for killing over curing. Five Years Later (after "increasing medical research funding"). Clinical trial funding is up fifty percent! Headlines are written. Backs are patted. A politician poses with a scientist. Meanwhile, military spending also went up fifty percent, because central banks printed fifty percent more money, so the real allocation of brains, factories, and hours is exactly the same. The ratio is still six hundred and four to one. You gave the medical department a raise and then raised the price of everything they need to buy."
- layer: B, plate ratio-chart
- bit: **Two bars on a chart: everyone celebrates when the small one grows, and nobody notices the big one grew by the same half.** The ratio card never moves, and the scientist's raise buys the same one flask.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Today. Government clinical trials cost four point five billion dollars. Global military spending is two point seventy-two trillion dollars." | $4.5 billion against $2.72 trillion. | TODAY on a card. The CLINICAL TRIALS bar: one small pill bottle, $4.5 BILLION. The MILITARY bar: the missile tower from Part 27 drops in beside it and runs out of the frame, $2.72 TRILLION. | |
| "The ratio is six hundred and four to one for killing over curing." | 604 to 1. | A card slams down between them: 604 : 1. | The pill bottle shuffles a little further from the tower. |
| "Five Years Later (after "increasing medical research funding"). Clinical trial funding is up fifty percent! Headlines are written. Backs are patted. A politician poses with a scientist." | Medicine gets +50%. | FIVE YEARS LATER. The pill bottle grows half again. Headlines spin in: +50%! Hands pat backs from all sides. The Politician grins beside the scientist, who holds a giant check, +50% FOR MEDICAL RESEARCH; a flashbulb goes off. | The flash leaves both of them sooty for a beat. |
| "Meanwhile, military spending also went up fifty percent, because central banks printed fifty percent more money, so the real allocation of brains, factories, and hours is exactly the same. The ratio is still six hundred and four to one." | Printing raised everything 50%. | Behind them, the Federal Reserve press cranks: the missile tower grows half again too, and the axis relabels itself so the picture looks the same as before. The 604 : 1 card has not moved. | A cobweb on it. |
| "You gave the medical department a raise and then raised the price of everything they need to buy." | A raise eaten by prices. | The scientist takes her bigger check to the shop counter. Every price tag on the flasks puffs up by half as she reaches it. | She walks away with the same one flask. |

Sound: a pop for the bottle; a long clatter for the tower; a slam on "one"; a newspaper spin; pats; a flash pop; a press thump per crank; a balloon squeak for each price tag; a till ding.

## Scene 3 · going-nowhere

- id: going-nowhere
- act: The proof
- transition_in: cut
- cue: "The Proof"
- time: 81:32.2 to 82:19.1 (46.9 s)
- voiceover: "The Proof: Fifty Years of Going Nowhere. Medical Research as a percentage of G.D.P. In nineteen seventy-five, it was zero point zero eight percent. In nineteen eighty-five, it was zero point zero seven percent. In nineteen ninety-five, it was zero point zero seven percent. In two thousand and five, it was zero point zero six percent. In twenty fifteen, it was zero point zero six percent. In twenty twenty-five, it was zero point zero six five percent. Absolute dollars increased ten times. Share of actual resources: decreased. You got ten times "richer" and spent a smaller fraction of it on not dying. This is like getting a promotion and canceling your health insurance to celebrate."
- layer: B, plate fifty-years
- bit: **The scientist walks fifty years along the line and ends lower than she started, then YOU celebrates his own promotion to death.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Proof: Fifty Years of Going Nowhere. Medical Research as a percentage of G.D.P." | | A line chart, MEDICAL RESEARCH AS A % OF GDP, 1975 to 2025, empty. The scientist stands at 1975 with her flask. | |
| "In nineteen seventy-five, it was zero point zero eight percent. In nineteen eighty-five, it was zero point zero seven percent. In nineteen ninety-five, it was zero point zero seven percent. In two thousand and five, it was zero point zero six percent. In twenty fifteen, it was zero point zero six percent." | 0.08% down to 0.06%. | Each year the narrator says, a point inks in and the line draws to it: 0.08, 0.07, 0.07, 0.06, 0.06. The scientist walks along it, a step down each decade, greying as she goes. | |
| "In twenty twenty-five, it was zero point zero six five percent." | A sliver back up. | The last point, 0.065, is a tiny step up. She hops onto it and throws both arms up. | It is still below where she started. |
| "Absolute dollars increased ten times. Share of actual resources: decreased." | More money, smaller share. | Two bars rise beside the line: DOLLARS climbs ten times; SHARE shrinks. | |
| "You got ten times "richer" and spent a smaller fraction of it on not dying. This is like getting a promotion and canceling your health insurance to celebrate." | | YOU gets a promotion cake with a candle. He tears up his health-insurance card and throws it as confetti. A germ walks in under the confetti, and YOU x-rays into a skeleton. | The skeleton still holds the cake, and blows out the candle. |

Sound: a pen squeak per point; footsteps down; a small boing for the hop; a party horn; a rip and confetti; an x-ray zap; a candle puff.

## Scene 4 · what-grew

- id: what-grew
- act: What grew
- transition_in: same plate (the camera travels right along the sheet)
- cue: "What Actually Grew"
- time: 82:19.1 to 83:02.5 (43.4 s)
- voiceover: "What Actually Grew. The financial sector grew from three percent to eight percent of G.D.P. The military-industrial sector grew from three percent to three point four percent of G.D.P. (the official number; the rest enters your budget wearing other costumes). Healthcare spending grew from seven percent to eighteen percent of G.D.P. (most of that growth is billing, not healing). The part that actually keeps you alive (the actual research into why your cells stop working) is a shrinking fraction of a growing economy. You baked a bigger pie and gave the science department fewer crumbs. Then you named the pie "progress.""
- layer: B, plate fifty-years
- bit: Same sheet: everything beside the scientist's line grew, and the pie that grew gives her crumbs.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "What Actually Grew. The financial sector grew from three percent to eight percent of G.D.P." | 3% to 8%. | Three pairs of bars, then and now. FINANCE: a bank stands on its bar, which stretches from 3% to 8%. | |
| "The military-industrial sector grew from three percent to three point four percent of G.D.P. (the official number; the rest enters your budget wearing other costumes)." | Most military money is hidden elsewhere. | MILITARY: a missile's bar barely grows, 3% to 3.4%. Then missiles in fedoras and false moustaches tiptoe out of it and stand inside the other bars. | One of them tips its fedora. |
| "Healthcare spending grew from seven percent to eighteen percent of G.D.P. (most of that growth is billing, not healing)." | 7% to 18%, mostly paperwork. | HEALTHCARE: the bar rises 7% to 18%, and it is a stack of invoices. A rubber stamp thumps DENIED down the whole stack. | |
| "The part that actually keeps you alive (the actual research into why your cells stop working) is a shrinking fraction of a growing economy." | | The pie from Part 27 on a table, growing bigger. Its RESEARCH slice gets thinner as the pie grows. | |
| "You baked a bigger pie and gave the science department fewer crumbs. Then you named the pie "progress."" | | The scientist holds out her plate; a few crumbs land on it. A flag is stuck in the middle of the giant pie: PROGRESS. | She eats one crumb. |

Sound: a stretch for each bar; tiptoe footsteps; a stamp per DENIED; an oven ding as the pie grows; a flag thunk on "progress."
