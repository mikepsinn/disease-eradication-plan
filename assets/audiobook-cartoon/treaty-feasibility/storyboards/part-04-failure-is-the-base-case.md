---
format: 1920x1080
duration: 3:27.0
message: "Even at a 1% chance of working, the treaty buys a healthy year for $0.177, 503 times cheaper than bed nets; and the depressing table shows countries keep under a quarter of what they sign."
arc: A prize wheel that is 99% LOSE, and Wishonia would never spin it, and the fat cat spins a hundred of them for a living → 18 pennies against a tower of 8,900, and the pessimist's raincloud rains on the pessimist → beside it the Economist's whiskers poke through the ceiling → the depressing table: every bar is a crowd of signers, and they leave → the globe joins a gym in front of the chart: January, February, March
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 4, "Political Success Probability"
audio: treaty-feasibility.858ed1cd.mp3, 09:06.4 to 12:33.4
version: v2
---

# Part 4 storyboard: "Political Success Probability"

- **Source:** `knowledge/appendix/treaty-feasibility.qmd` as narrated: "Political Success Probability: Economic Analysis" and "Historical Precedents (The Depressing Table)".
- **The numbers** (the narrator's, from an earlier model run; where `_variables.yml` now differs, its value is given and the narrator's is used on screen):
  - `political_success_probability`: 1% (95% CI 0.1% to 10%). The 25% optimistic ceiling is the chapter's scenario, not a parameter.
  - `treaty_expected_cost_per_daly`: narrated $0.177 (95% CI $0.029 to $3.20); `_variables.yml` now has $1.99.
  - `treaty_expected_vs_bed_nets_multiplier`: narrated 503× (95% CI 30× to 3,000×); now 92.1×.
  - `bed_nets_cost_per_daly`: narrated $89 (95% CI $78 to $100); now $184.
  - Derived, in pennies: the treaty's healthy year is a stack of about 18 pennies; the bed nets' is a tower of 8,900.
  - The depressing table (the chapter's, not parameters): 0.7% ODA, about 20% complied over 50+ years (Scandinavia and Germany); Kyoto, about 55% at first, then collapse, 1997 to 2012, the US never ratified and Canada withdrew; Paris, 15 to 25% on track since 2015, 195 signed and maybe 40 meant it; NATO 2%, 72% in 2024 against 32% from 2014 until the war in Ukraine; EU Stability Pact (3% deficit, 60% debt), routinely broken since 1997, France and Germany included. The pattern: under 25%.
- **What the viewer must leave with:** the model assumes the treaty fails 99 times in 100 and it is still 503 times better value than bed nets; most treaties are signed and not kept.
- **Plates:**
  - `prize-wheel`: a carnival prize wheel on a plain field, one hair-thin WIN slice.
  - Host (on-wishonia-vc): Wishonia at her console on the observation deck, Earth in the glass.
  - `penny-chart`: a penny chart on aged paper, "COST OF ONE HEALTHY YEAR", with the bed-net cup on the baseline, and the Economist's chalkboard beside it.
  - `promise-chart`: a bar chart on aged paper, "COUNTRIES THAT DID WHAT THEY SIGNED", five bars, a dashed line at 25%.
- **Cast:** existing: `prize-wheel`, `wheel-stand`, `fat-cat-chair`, `coin` (copper pennies), `newspaper-man` (the pessimist, in his trench coat), `cloud`, `rosette`, `rank-board`, `uncle-sam`, `tank`, `treaty-scroll`, `globe`, `cobweb`, `paycheck` (the membership card). New: `bed-net-cup`, `sweatband`. Shared: `economist` (Part 1), `citizen` (Part 3; the signers, with flags and national hats), `jalopy` (Part 1).
- **Callbacks:**
  - Episode 1, Part 16's bed-net cup, the penny chart and the pessimist with his raincloud (its numbers there are $0.02 and $184; here they are the narrator's $0.177 and $89).
  - Part 1's jalopies: the KYOTO and 0.7% AID wrecks are parked at the foot of their bars.
  - Set up for Part 12: the promise chart comes back ("You saw the depressing table").
- **New art:** the bed-net cup (a tiny human asleep under a net in a paper cup), unless episode 1, Part 16 draws it first; a sweatband for the `globe`.
- **Kit additions:**
  - `whiskers`: a dot with an error bar that draws out from the dot to both ends (and can run off its board).
  - `leave`: pictogram figures that walk out of a bar one by one, so the bar shrinks.

## Scene 1 · ninety-nine-percent-lose

- id: ninety-nine-percent-lose
- act: Failure is the base case
- transition_in: cut
- cue: "Political Success Probability"
- time: 09:06.4 to 09:23.7 (17.3 s)
- voiceover: "Political Success Probability: Economic Analysis. This section documents the rationale for the one percent central estimate (and a twenty-five percent optimistic scenario ceiling). The model assumes failure is the base case. It's still a good bet."
- layer: B, plate prize-wheel
- bit: **A prize wheel that is all LOSE except one hair of WIN, and it's a good bet.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Political Success Probability: Economic Analysis. This section documents the rationale for the one percent central estimate" | 1%. | Big: a carnival prize wheel. 99% of it is one slice, "LOSE"; one hair-thin slice, "WIN 1%". | |
| "(and a twenty-five percent optimistic scenario ceiling)." | Up to 25%. | A dotted quarter of the wheel flickers on, "25%", and off again. | |
| "The model assumes failure is the base case." | It probably fails. | The wheel spins and stops on LOSE. | |
| "It's still a good bet." | What you lose is small; what you can win is enormous. | The camera pushes into the hair of WIN until it fills the frame: written along it, in letters that now fill the screen, "CURE MOST DISEASES". Pull back out: the huge LOSE slice says, small, "$1 BILLION". | The pointer, stopped on LOSE, shrugs. |

Sound: a ratcheting spin and a clunk on LOSE; a sad trombone note that turns up at the end as the camera pushes in.

## Scene 2 · on-wishonia-vc

- id: on-wishonia-vc
- act: Failure is the base case
- transition_in: cut
- cue: "On Wishonia, we would not invest"
- time: 09:23.7 to 09:34.4 (10.6 s)
- voiceover: "On Wishonia, we would not invest in something where failure is the base case. On Earth, this is called "venture capital" and your richest humans do it professionally."
- layer: A, host
- wishonia: sad-closed + body-palms-down; smirk-smile + body-point-right on "venture"; sideeye-closed + body-idle on "professionally."
- bit: Wishonia wouldn't spin it once; the fat cat spins a wall of them for a living.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "On Wishonia, we would not invest in something where failure is the base case." | | Wishonia at her console, palms down, shaking her head at a tiny copy of the wheel on the ledge. | |
| "On Earth, this is called "venture capital"" | Rich humans make such bets all the time. | She points: the fat cat rolls onto the deck in his chair, a phone at his ear, in front of a wall of a hundred little prize wheels, all LOSE but a sliver. | |
| "and your richest humans do it professionally." | | He flicks them all spinning with one hand without looking, and lights his cigar. | One stops on WIN; he doesn't notice. |

Sound: a hundred wheels ratcheting at once; a ding nobody hears.

## Scene 3 · eighteen-pennies

- id: eighteen-pennies
- act: Failure is the base case
- transition_in: cut
- cue: "Even at one percent probability"
- time: 09:34.4 to 10:05.3 (30.9 s)
- voiceover: "Even at one percent probability of success, this intervention's expected cost per disability-adjusted life years, or D.A.L.Y.s ($0.177) is still five hundred and three times more cost-effective than malaria bed nets ($89 per D.A.L.Y.). Bed nets are the gold standard of global health interventions. This beats the gold standard while assuming it will almost certainly fail. The math doesn't care about your pessimism."
- layer: B, plate penny-chart
- bit: **Eighteen pennies against a tower of 8,900, and the pessimist's own raincloud rains on him instead.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Even at one percent probability of success, this intervention's expected cost per disability-adjusted life years, or D.A.L.Y.s ($0.177)" | $0.177 a healthy year at 1%. | A penny chart, "COST OF ONE HEALTHY YEAR". The treaty's stack: 18 pennies, ankle-high, "$0.177". | |
| "is still five hundred and three times more cost-effective than malaria bed nets ($89 per D.A.L.Y.)." | Bed nets: $89; 503×. | Beside it, the bed-net cup, a tiny human asleep under its net. Behind it a tower of 8,900 pennies stacks up, faster and faster, and the camera tilts up it off the top: "$89". "503×" stamps between them. | |
| "Bed nets are the gold standard of global health interventions. This beats the gold standard while assuming it will almost certainly fail." | | A gold rosette pins onto the cup. Then a bigger one onto the 18 pennies. | |
| "The math doesn't care about your pessimism." | | The pessimist in his trench coat holds his raincloud over the 18 pennies. It rains on him instead. The stack stays exactly 18 high. | |

Sound: 18 clinks; a long run of clinks up the tower; a stamp; two pins; rain, and a sniff.

## Scene 4 · whiskers

- id: whiskers
- act: Failure is the base case
- transition_in: same plate (the camera travels to the chalkboard)
- cue: "The political success probability point estimate"
- time: 10:05.3 to 10:49.4 (44.1 s)
- voiceover: "The political success probability point estimate is one percent, with a ninety-five percent confidence interval of zero point one percent to ten percent. The expected cost per D.A.L.Y. point estimate is zero point one seven seven dollars, with a ninety-five percent confidence interval of zero point zero two nine dollars to three dollars and twenty cents. The cost-effectiveness versus bed nets point estimate is five hundred and three times, with a ninety-five percent confidence interval of thirty times to three thousand times. The bed net cost per D.A.L.Y. point estimate is eighty-nine dollars, with a ninety-five percent confidence interval of seventy-eight dollars to one hundred dollars."
- layer: B, plate penny-chart
- bit: **The Economist chalks four dots and draws their whiskers; the third whisker is so long it goes through the ceiling, and even its bottom end beats bed nets.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The political success probability point estimate is one percent, with a ninety-five percent confidence interval of zero point one percent to ten percent." | 1% (0.1% to 10%). | The Economist at the chalkboard beside the penny chart chalks a dot, "1%", and draws its whiskers out to "0.1%" and "10%". | |
| "The expected cost per D.A.L.Y. point estimate is zero point one seven seven dollars, with a ninety-five percent confidence interval of zero point zero two nine dollars to three dollars and twenty cents." | $0.177 ($0.029 to $3.20). | Second row: "$0.177", whiskers to "$0.029" and "$3.20". | |
| "The cost-effectiveness versus bed nets point estimate is five hundred and three times, with a ninety-five percent confidence interval of thirty times to three thousand times." | 503× (30× to 3,000×). | Third row: "503×". He draws the whisker up to "3,000×": it runs off the board, up the wall and through the ceiling. Plaster drops on his head. The bottom end stops at "30×", still well above a dashed line, "BED NETS = 1×". | |
| "The bed net cost per D.A.L.Y. point estimate is eighty-nine dollars, with a ninety-five percent confidence interval of seventy-eight dollars to one hundred dollars." | $89 ($78 to $100). | Fourth row, plaster on his head: "$89", a neat short whisker, "$78" to "$100". He dusts himself off. | |

Sound: chalk taps; a chalk squeal up the wall, a crunch through the ceiling, and a plaster patter; a neat little tick for the last.

## Scene 5 · depressing-table

- id: depressing-table
- act: The depressing table
- transition_in: cut
- cue: "Historical Precedents (The Depressing Table)"
- time: 10:49.4 to 12:08.7 (79.3 s)
- voiceover: "Historical Precedents (The Depressing Table). For the zero point seven percent O.D.A., or Official Development Assistance, target of zero point seven percent of gross national income, or G.N.I., to foreign aid, only about twenty percent of countries complied over fifty plus years, which was basically just Scandinavia and Germany. The Kyoto Protocol set binding emissions targets that about fifty-five percent of countries initially followed before a collapse between nineteen ninety-seven and twenty twelve, noting the U.S. never ratified and Canada withdrew. The Paris Agreement for non-binding pledges has about fifteen to twenty-five percent of countries on track since twenty fifteen, where one hundred and ninety-five countries signed but maybe forty meant it. The NATO two percent G.D.P. defense spending target is met by about seventy-two percent of members as of twenty twenty-four, whereas only thirty-two percent complied from twenty fourteen until an actual land war in Europe motivated spending. The E.U. Stability Pact of a three percent deficit and sixty percent debt has been routinely violated since nineteen ninety-seven, with France and Germany breaking their own rule."
- layer: B, plate promise-chart
- bit: **A bar chart of countries that did what they signed, where every bar is a crowd of signers with flags, and the crowds walk out.** The only bar that grows is the one a tank drives past.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Historical Precedents (The Depressing Table). For the zero point seven percent O.D.A., or Official Development Assistance, target of zero point seven percent of gross national income, or G.N.I., to foreign aid, only about twenty percent of countries complied over fifty plus years, which was basically just Scandinavia and Germany." | 0.7% aid: about 20%, 50 years. | A chart, "COUNTRIES THAT DID WHAT THEY SIGNED". The first bar, "0.7% AID", is a full column of little signers with flags. Fifty years flick by; the column wanders off until only a few Scandinavians and one German are left, "20%". The 0.7% AID jalopy from Part 1 is parked at its foot. | The Scandinavians wave. |
| "The Kyoto Protocol set binding emissions targets that about fifty-five percent of countries initially followed before a collapse between nineteen ninety-seven and twenty twelve, noting the U.S. never ratified and Canada withdrew." | Kyoto: 55%, then collapse. | "KYOTO" rises to 55% and slumps into a heap like a sandcastle, 1997 to 2012. Uncle Sam stands outside it, arms folded, the whole time; a signer in a Mountie hat climbs out of the heap and leaves. | |
| "The Paris Agreement for non-binding pledges has about fifteen to twenty-five percent of countries on track since twenty fifteen, where one hundred and ninety-five countries signed but maybe forty meant it." | Paris: 195 signed, about 40 meant it. | 195 signers pile into "PARIS" and it towers; on "maybe forty" all but 40 tiptoe out, and it sinks to about 20%. | |
| "The NATO two percent G.D.P. defense spending target is met by about seventy-two percent of members as of twenty twenty-four, whereas only thirty-two percent complied from twenty fourteen until an actual land war in Europe motivated spending." | NATO: 32%, then 72% after a war. | "NATO 2%" sits at 32%. A tank rolls along behind the chart, and the bar jumps to 72% in one go. | The one bar that grew needed a war. |
| "The E.U. Stability Pact of a three percent deficit and sixty percent debt has been routinely violated since nineteen ninety-seven, with France and Germany breaking their own rule." | The EU breaks its own rule. | "EU STABILITY PACT": a pinned scroll, "3% DEFICIT · 60% DEBT". A signer in a beret and one in a Tyrolean hat take an end each and tear it in half together. | |

Sound: footsteps as the signers leave; a slump; a crowd stampede and tiptoes; a tank's clank and a boing as the bar jumps; a paper tear.

## Scene 6 · new-years-resolution

- id: new-years-resolution
- act: The depressing table
- transition_in: same plate (no seam)
- cue: "Pattern: International financial commitments"
- time: 12:08.7 to 12:33.4 (24.7 s)
- voiceover: "Pattern: International financial commitments achieve less than twenty-five percent meaningful compliance. Your species signs things and then doesn't do them. It's like a New Year's resolution, but for geopolitics. The gym membership analogy is overused but accurate: purchased with enthusiasm in January, abandoned by February, cited in arguments about personal growth throughout March."
- layer: B, plate promise-chart
- bit: **The whole planet buys a gym membership, in front of the chart that proves it won't use it.** The globe jogs in January, is a cobweb in February, and in March lectures the Scandinavians about it.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Pattern: International financial commitments achieve less than twenty-five percent meaningful compliance. Your species signs things and then doesn't do them." | Under 25%. | A dashed line draws across the chart at 25%, "MEANINGFUL COMPLIANCE"; every bar but NATO's is under it, and NATO's has a tank parked next to it. | |
| "It's like a New Year's resolution, but for geopolitics. The gym membership analogy is overused but accurate: purchased with enthusiasm in January," | January. | The globe hops off its stand in front of the chart, in a sweatband, waving a membership card, "GYM · 1 YEAR". JANUARY: it jogs on the spot, sweating, grinning. | |
| "abandoned by February," | February. | FEBRUARY: the spot is empty but for a cobweb; the globe is back on its stand. | |
| "cited in arguments about personal growth throughout March." | March. | MARCH: the globe waves the membership card at the little Scandinavians at the foot of the 0.7% AID bar, mid-lecture. Their eyes glaze over. | The only ones who did it are the ones being lectured. |

Sound: a pen ruling the line; jogging thuds and panting; silence and a single creak; a smug lecturing murmur.
