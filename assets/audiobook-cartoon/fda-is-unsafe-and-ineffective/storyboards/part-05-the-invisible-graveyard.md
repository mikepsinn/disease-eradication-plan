---
format: 1920x1080
duration: 2:15.1
message: "The 8.2-year wait after a drug is known safe adds up to 416 million avoidable deaths, and nobody photographs them because their toe tags say cancer."
arc: The economist's neat DRUG LAG label peels off the queue → the US range bar, then the globe → a column of 416 million headstones, its years deleted and its price in money → cut by ten, still off the top of the frame → the column lifts away and the two cost bars stand alone → the Non-Existent Times with an empty photo → the morgue drawers whose tags all say something else → a pigeon on the blank headline
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 5, "The Invisible Graveyard"
audio: fda-is-unsafe-and-ineffective.5d00ae46.mp3, 12:29.9 to 14:45.1
version: v2
---

# Part 5 storyboard: "The Invisible Graveyard"

- **Source:** `knowledge/problem/fda-is-unsafe-and-ineffective.qmd`, section "The Actual Death Toll of 'Drug Lag'", and `knowledge/appendix/invisible-graveyard.qmd`.
- **The numbers:**
  - Early US estimates: 21,000 to 120,000 American lives per decade (cited, `gieringer-drug-lag-estimate`, not a parameter).
  - `dfda_efficacy_lag_elimination_deaths_averted`: 416 million eventually avoidable deaths from the 8.2-year post-safety delay (`efficacy_lag_years` 8.2).
  - DALYs: the narrator says 7.94 billion; `dfda_efficacy_lag_elimination_dalys` now holds 8.77 billion. On screen, the narrator's 7.94 billion.
  - Economic cost: the narrator says $1.19 quadrillion (2024 US dollars); `dfda_efficacy_lag_elimination_economic_value` now holds $1.32 quadrillion. On screen, $1.19 quadrillion. It is 7.94 billion × `standard_economic_qaly_value_usd` $150,000 per DALY.
  - Off by a factor of ten: 41.6 million, "tens of millions".
  - `recovery_trial_cost_reduction_factor`: 82× more per patient; `fda_to_oxford_recovery_trial_time_multiplier`: 32.8× longer.
- **What the viewer must leave with:** the wait after a drug is proven safe kills on the scale of 416 million people, the cost and slowness are true whatever the death count, and nobody sees the dead because the delay never appears as a cause of death.
- **Plates:**
  - `queue-label`: a chalkboard in front of a long queue on aged paper.
  - `graveyard-column`: a bar chart on aged paper, "AVOIDABLE DEATHS FROM THE 8.2-YEAR DELAY", one column of headstones, the globe at its foot.
  - `newsstand`: a street corner on a plain field: a newsboy, a photographer, and a wall of morgue drawers behind them.
- **Cast:** existing: `economist`, `chalkboard`, `sick-human` (the queue), `patient-skeleton`, `ticket`, `approval-cabinet`, `pill-bottle`, `world-map`, `globe`, `headstone`, `cloud`, `human-ages`, `pencil` (its giant eraser end), `price-tag`, `money-hill`, `scissors`, `newspaper-man`, `photographer`, `pigeon`. New: `morgue-drawers` (a wall of steel morgue drawers; drawers slide out with a sheeted body and a toe tag).
- **Callbacks:** Part 2's cost bars ($500 and $41,000) come back, stamped 82× and 32.8×.
- **New art:**
  - the wall of morgue drawers, three drawers that slide out, sheets with feet, toe tags (text in code)
  - a column of tiny headstones drawn as one tall strip that can be cut and lifted (from `headstone`)
- **Kit additions:**
  - An erase: the giant pencil eraser rubs a strip of a figure away (years off a life).

## Scene 1 · drug-lag-label

- id: drug-lag-label
- act: The death toll
- transition_in: cut; the heading card comes up from black
- cue: "The Actual Death Toll"
- time: 12:29.9 to 12:53.8 (23.9 s)
- voiceover: "The Actual Death Toll of "Drug Lag". Economists call it "drug lag," which is a lovely, clinical way of saying "people rotting to death in a queue for drugs that have already been confirmed not to hurt them.". Early estimates: twenty-one thousand to one hundred and twenty thousand American lives per decade. But that was just the U.S."
- layer: B, plate queue-label
- bit: **The polite label peels off and the queue behind it is what it means.** Then the numbers, then the camera pulls out from America to the world.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Actual Death Toll of "Drug Lag". Economists call it "drug lag,"" | | The heading card. The economist, monocle and mutton chops, chalks "DRUG LAG" in neat copperplate on a chalkboard, and taps it with his pointer. | |
| "which is a lovely, clinical way of saying "people rotting to death in a queue for drugs that have already been confirmed not to hurt them."." | The phrase means people dying in line. | The chalkboard rolls aside. Behind it, a queue stretches to the horizon, greying as it goes: grey, then bony, then grinning skeletons, all still in line, each holding a ticket. At its head the padlocked cabinet with a "SAFE ✓" bottle. | The economist straightens his monocle. |
| "Early estimates: twenty-one thousand to one hundred and twenty thousand American lives per decade. But that was just the U.S." | 21,000 to 120,000 a decade, in one country. | Close on America on the world map; a range bar rises from it, a solid stub to "21,000" and a dotted top to "120,000", "AMERICAN LIVES PER DECADE". The camera pulls back: America is a patch on the globe. | |

Sound: chalk; a pointer tap; a trolley squeak; a creak as the queue appears; a pen squeak as the bar rises; a whoosh out.

## Scene 2 · 416-million

- id: 416-million
- act: The death toll
- transition_in: cut
- cue: "A comprehensive quantitative analysis"
- time: 12:53.8 to 14:15.3 (81.5 s)
- voiceover: "A comprehensive quantitative analysis using W.H.O. mortality data estimates the *total* cost of the eight point two years *post-safety* efficacy delay (the lag *after* drugs are known safe): four hundred and sixteen million eventually avoidable deaths. Including years lived with disability: seven point nine four billion disability-adjusted life years, or D.A.L.Y.s, of healthy human life deleted. Economic cost: one point one nine quadrillion dollars (twenty twenty-four U.S. dollars), reflecting those seven point nine four billion D.A.L.Y.s valued at one hundred and fifty thousand dollars per D.A.L.Y., the standard normative rate used in W.H.O. cost-effectiveness analyses. Even if those death estimates are off by a factor of ten, that's still tens of millions of deaths. And the inefficiency is independently verifiable: the efficacy testing process costs eighty-two times more per patient and takes thirty-two point eight times longer than proven alternatives like the Oxford RECOVERY trial. Those numbers don't depend on mortality estimates at all."
- layer: B, plate graveyard-column
- bit: **One column of headstones from the globe up past the top of the frame, then cut by ten and still too tall to see the top of; then lifted away, and the cost bars stand on their own.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "A comprehensive quantitative analysis using W.H.O. mortality data estimates the *total* cost of the eight point two years *post-safety* efficacy delay (the lag *after* drugs are known safe): four hundred and sixteen million eventually avoidable deaths." | 416 million. | On the globe, headstones pile up into one column, faster and faster; the camera tilts up after it, off the chart, past a cloud, and back down: "416,000,000". | |
| "Including years lived with disability: seven point nine four billion disability-adjusted life years, or D.A.L.Y.s, of healthy human life deleted." | 7.94 billion healthy years lost. | Beside the column, one human at six ages in a row, baby to old man. A giant pencil eraser rubs whole stretches out of the row: the toddler, the schoolboy, half the grown man. "7,940,000,000 HEALTHY YEARS". | The old man at the end looks round for the rest of himself. |
| "Economic cost: one point one nine quadrillion dollars (twenty twenty-four U.S. dollars), reflecting those seven point nine four billion D.A.L.Y.s valued at one hundred and fifty thousand dollars per D.A.L.Y., the standard normative rate used in W.H.O. cost-effectiveness analyses." | $1.19 quadrillion at $150,000 a year. | A price tag, "$150,000", hangs on each erased gap; the tags multiply into a money hill beside the column: "$1.19 QUADRILLION". | |
| "Even if those death estimates are off by a factor of ten, that's still tens of millions of deaths." | 41.6 million is still huge. | A scissor line cuts the column at a tenth of its height; the top 90% lifts away. What is left still runs off the top of the frame: "÷ 10 = 41,600,000". | |
| "And the inefficiency is independently verifiable: the efficacy testing process costs eighty-two times more per patient and takes thirty-two point eight times longer than proven alternatives like the Oxford RECOVERY trial." | 82× the cost, 32.8× the time. | Part 2's cost bars slide in, "$500" and "$41,000": "82×" stamps between them. The race lanes beside: "32.8×". | |
| "Those numbers don't depend on mortality estimates at all." | They stand without the death count. | The rest of the headstone column lifts away on wires. The two cost bars stand alone on the chart. | One headstone is left hanging, and falls with a clunk. |

Sound: a thunk per headstone, faster into a rumble; a rubbing squeak per erase; a till ding as the tags multiply; a snip; two stamps; a clunk.

## Scene 3 · non-existent-times

- id: non-existent-times
- act: The death toll
- transition_in: cut
- cue: "Here's a news story from the Non-Existent Times"
- time: 14:15.3 to 14:45.1 (29.8 s)
- voiceover: "Here's a news story from the Non-Existent Times by No One Ever, without a picture of all the people who die from lack of access to life-saving treatments that might have been. You can't photograph millions of people who died from *not* receiving a drug. There's no body with a toe tag reading "cause of death: regulatory delay." They die of cancer, heart disease, Alzheimer's. The delay that killed them is invisible, so nobody writes the headline."
- layer: B, plate newsstand
- bit: **A newspaper about nothing, a photo of nothing, and three toe tags that all blame someone else.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Here's a news story from the Non-Existent Times by No One Ever, without a picture of all the people who die from lack of access to life-saving treatments that might have been." | Nobody reports these deaths. | A newsboy waves the front page: "THE NON-EXISTENT TIMES", byline "BY NO ONE EVER", the headline blank, the photo box empty. | He shouts, and nothing comes out. |
| "You can't photograph millions of people who died from *not* receiving a drug." | They can't be seen. | A 1950s press photographer aims his flash camera at an empty field. FLASH. The print slides out: the empty field. | He shakes it, like a Polaroid. Still nothing. |
| "There's no body with a toe tag reading "cause of death: regulatory delay."" | | Behind them, a wall of morgue drawers. One slides out: a sheet, two feet, a toe tag reading "CAUSE OF DEATH: REGULATORY DELAY". The words fade off the tag. | |
| "They die of cancer, heart disease, Alzheimer's." | The death certificate names the disease. | Three drawers slide out together, one per word: "CANCER", "HEART DISEASE", "ALZHEIMER'S". | |
| "The delay that killed them is invisible, so nobody writes the headline." | | The drawers slide shut. Back on the newsboy: a pigeon lands on his blank front page and settles in. | |

Sound: a newsboy's silent shout; a flash pop; a drawer slide per tag; a coo.
