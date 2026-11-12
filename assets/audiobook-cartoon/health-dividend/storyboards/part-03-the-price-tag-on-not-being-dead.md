---
format: 1920x1080
duration: 3:15.3
message: "150,000 people die of disease every day, 92.6% of it fixable in principle; 212 years sooner prevents 10.7 billion deaths, and at the government's own $150,000 a year of life that is $84.8 quadrillion."
arc: Title card (the counter clicks 1.7 times a second) → headstones pile up behind YOU's armchair while he reads, 92.6% of them redraw in dotted lines, the ladder man keeps getting hit, and the old man bonks the theoretical ceiling → 10.7 billion against everyone alive, and the house-sized cup comes down over the economist's OBJECTION → the price tag on DEAD → the Capitol prices everyone in the footnote of HUMAN LIFE IS PRICELESS* → one bar of lost years becomes money and copies itself 212 times onto the receipt → the GDP register rings up toast and says NO SALE to being alive → Earth sneezes on the window → the dice man rolls the 212 bars into a blur, rolls himself to pieces, and they settle back on 212
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 3, "The Price Tag on Not Being Dead"
audio: health-dividend.77700cce.mp3, 06:26.9 to 09:42.1
version: v2
---

# Part 3 storyboard: "The Price Tag on Not Being Dead"

- **Source:** `knowledge/economics/health-dividend.qmd`, "The Body Count" and "The Price Tag on Not Being Dead"; it links `knowledge/appendix/dfda-impact-paper.qmd` (the derivation and the Monte Carlo) and cites `ihme-gbd-2021` for the disease burden.
- **The numbers:**
  - `global_disease_deaths_daily` 150,000 deaths a day. Derived: about 104 a minute, 1.7 a second. The narrator's "approximately three hundred" during the previous section is about 3 minutes of it (spoken, not a parameter).
  - `eventually_avoidable_death_pct` 92.6% eventually avoidable; the other 7.4% (derived) are accidents. Of the headstones behind the armchair, 92.6% redraw dotted and 7.4% stay solid.
  - `dfda_trial_capacity_plus_efficacy_lag_years` 212 years (its 90% range is 124 to 398 years; not spoken, so the sign shows only 212).
  - `dfda_trial_capacity_plus_efficacy_lag_lives_saved` 10.7 billion deaths. Against `global_population_2024` 8 billion: 107 figures at 100 million each beside 80. The 8 billion is not spoken, so its bar carries a label and no number.
  - `dfda_trial_capacity_plus_efficacy_lag_dalys` 565 billion healthy years; `dfda_trial_capacity_plus_efficacy_lag_suffering_hours` 1.93 quadrillion hours of suffering.
  - `standard_economic_qaly_value_usd` $150,000 a year of healthy life.
  - `global_annual_daly_burden` 2.88 billion healthy years lost a year; `eventually_avoidable_daly_pct` 92.6%; so `global_disease_economic_burden_annual` $400 trillion a year.
  - $400 trillion × 212 = the narrator's $84.8 quadrillion. The variable `dfda_trial_capacity_plus_efficacy_lag_economic_value` now reads $7.53 quadrillion (discounted); on screen, 84.8, the narrator's.
  - `global_gdp_2025` $115 trillion. Derived: the $400 trillion a year is about 3.5 times it.
- **What the viewer must leave with:** 150,000 people die of disease every day and 92.6% of that is fixable in principle; 212 years sooner prevents 10.7 billion deaths, and priced at the government's own $150,000 a year of life it is worth $84.8 quadrillion.
- **Plates:**
  - `the-parlour`: YOU's wingback armchair on a plain field, a counter on a post beside it, open ground behind it for rows of headstones, a tall ladder at the right edge.
  - `the-cups`: a bar chart, "DEATHS PREVENTED", beside a trophy plinth with the smallpox cup and an empty plinth with room for a cup the size of a house.
  - `the-field`: a long field on aged paper with a year ruler. At the left, a row of citizens under a huge billboard, "HUMAN LIFE IS PRICELESS*"; then one bar of hourglasses with room for 212 copies of it to the horizon and for the receipt to unroll along the front; a brass cash register, "GDP", at the foot of the first bar; Part 2's arrow sign at the far end.
  - host: Wishonia at her console on the observation deck, Earth in the glass, the receipt still printing.
- **Cast:** existing: `you` (reading in the armchair), `armchair`, `manual`, `year-counter`, `headstone`, `skeleton`, `ladder`, `motorcar`, `motorist`, `human-ages` (the old man on a cane), `scientist`, `flask`, `hot-water-bottle`, `smallpox-cup` (and a house-sized copy), `germ`, `economist`, `sign-board` (the OBJECTION placard), `banner` (the PRICELESS billboard), `capitol-legs`, `citizen`, `price-tag`, `patient`, `iron-bed`, `hourglass`, `money-bundle`, `receipt`, `cash-register`, `goods`, `family`, `calculator` (host prop), `arrow-sign`, `dice-suit`. New: `pricing-gun`.
- **Callbacks:** Part 1's receipt (it prints the $84.8 quadrillion line in times-two-twelve); Part 1's economist, who checked the number and now objects to it; Part 2's arrow signs (the 212 sign in monte-carlo).
- **New art:**
  - `pricing-gun`: a shop's price-tag gun, for the Capitol's hand.
- **Kit additions:**
  - A dotted swap: a cut-out redraws as a dotted outline of itself, run along a row (the headstones, the hourglasses).
  - A copy-march: one bar copied along a ruler N times, faster and faster to the horizon, and back.

## Scene 1 · body-count-title

- id: body-count-title
- act: Title
- transition_in: cut
- cue: "The Body Count."
- time: 06:26.9 to 06:29.1 (2.2 s)
- voiceover: "The Body Count."
- layer: A, title card
- bit: The counter on the card runs at the real rate.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Body Count." | The heading. | The period card: "THE BODY COUNT", a brass tally counter in its corner clicking 1.7 times a second, the real rate. Under the words a small headstone pops up per click. | The headstones push the words up off the card. |

Sound: a whirr; the counter's click, 1.7 a second; a thunk per headstone.

## Scene 2 · while-you-were-reading

- id: while-you-were-reading
- act: The body count
- transition_in: cut
- cue: "One hundred and fifty thousand"
- time: 06:29.1 to 07:15.3 (46.2 s)
- voiceover: "One hundred and fifty thousand deaths per day die from disease every day. While you were reading the previous section, approximately three hundred of them did. They are not coming back to find out how the math turned out. Not all of those deaths are currently preventable, but ninety-two point six percent are eventually avoidable with sufficient biomedical research. "Eventually avoidable" does not mean "currently preventable." It means: given enough research, these diseases have biological solutions. The only category excluded is accidents (falling off things, being hit by things). Every disease, including aging, is a biological process, and biological processes are, in principle, fixable. This is the theoretical ceiling, not a near-term promise."
- layer: B, plate the-parlour
- bit: **The dead pile up behind YOU's armchair while he reads, and he never looks round.** Their skeletons leave; the empty graves redraw in dotted lines (fixable, not fixed), all but the accidents, where one man keeps getting hit by cars. Payoff: an old man is steered into the dotted rows and bonks his head on the ceiling.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "One hundred and fifty thousand deaths per day die from disease every day. While you were reading the previous section, approximately three hundred of them did." | 150,000 a day, 1.7 a second; about 300 in three minutes. | Close: YOU in a wingback armchair, reading the manual. The counter on its post beside him clicks; a headstone pops up behind his chair on each click. The camera pulls back: rows of headstones fill the ground behind him to the edge of the paper. Counter: "300". He turns a page. | |
| "They are not coming back to find out how the math turned out." | | The skeletons climb out of their graves and walk off the edge of the paper in single file. The last one stops, reads over YOU's shoulder, shrugs and follows them. | YOU licks a finger and turns the page. |
| "Not all of those deaths are currently preventable, but ninety-two point six percent are eventually avoidable with sufficient biomedical research. "Eventually avoidable" does not mean "currently preventable." It means: given enough research, these diseases have biological solutions." | 92.6% are fixable in principle; not yet, and research finds the fixes. | The headstones redraw in dotted lines, row by row: "EVENTUALLY AVOIDABLE · 92.6%". A rubber stamp thumps across them: "NOT YET". The Scientist walks along in front with her bubbling flask held up. | The last dotted headstone is cut through the middle: six tenths dotted. |
| "The only category excluded is accidents (falling off things, being hit by things)." | 7.4% are accidents. | At the right, the solid 7.4%: a man on a tall ladder falls off it, lands, sits up dazed, and a motorcar hits him. Tag: "ACCIDENTS · 7.4%". | He sits up again, and a second motorcar hits him. |
| "Every disease, including aging, is a biological process, and biological processes are, in principle, fixable." | Aging counts, in principle. | An old man on a cane totters toward the accidents. The Scientist takes his elbow and steers him into the dotted rows, and he redraws dotted, cane and all. | He looks at his dotted hands, delighted. |
| "This is the theoretical ceiling, not a near-term promise." | It is the upper limit. | A dashed line drops in over the dotted rows: "THEORETICAL CEILING". | The old man stands up straight and bonks his head on it. |

Sound: the counter click; a thunk per headstone; a page turn; a rattle of bones walking away; a dotted pen tick per row; a stamp; a fall, a thud and a car horn, twice; a dotted tick for the old man; a bonk.

## Scene 3 · more-than-everyone

- id: more-than-everyone
- act: The body count
- transition_in: cut
- cue: "Over a two hundred and"
- time: 07:15.3 to 07:55.4 (40.2 s)
- voiceover: "Over a two hundred and twelve-year timeline shift, the cumulative toll: ten point seven billion deaths. That is five hundred and sixty-five billion disability-adjusted life years, or D.A.L.Y.s, of healthy life, and one point nine three quadrillion hours of suffering eliminated. These are cumulative, one-time benefits from permanently accelerating the discovery pipeline, the same methodology used to value smallpox eradication. Nobody objected to the methodology when it was used for smallpox. They will object now because the number is larger, which is a strange reason to object to saving more people."
- layer: B, plate the-cups
- bit: **The people the shift saves outnumber everyone alive, and their cup is so big the economist objects to it.** He applauds the same method on the small smallpox cup. Payoff: the big one comes down over him.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Over a two hundred and twelve-year timeline shift, the cumulative toll: ten point seven billion deaths." | 10.7 billion, more than the 8 billion alive. | A bar chart, "DEATHS PREVENTED": a pictogram bar of 107 people, "10.7 BILLION", beside a bar of 80, "EVERYONE ALIVE TODAY". | The top person on the shorter bar looks up at the taller one and takes off his hat. |
| "That is five hundred and sixty-five billion disability-adjusted life years, or D.A.L.Y.s, of healthy life, and one point nine three quadrillion hours of suffering eliminated." | 565 billion healthy years; 1.93 quadrillion hours. | A counter rolls to "565,000,000,000 YEARS". Every one of the 107 has been holding something that hurts (a back, a jaw, a hot-water bottle on the head); a second counter rolls to "1,930,000,000,000,000 HOURS", and they all let go and straighten up. | |
| "These are cumulative, one-time benefits from permanently accelerating the discovery pipeline, the same methodology used to value smallpox eradication. Nobody objected to the methodology when it was used for smallpox." | Counted once, for a permanent speed-up, by the smallpox method. | The camera travels to the trophy plinth: the gold smallpox cup, a germ flattened under its foot, a card on the plinth: "METHOD". The same card hangs on an empty plinth beside it. The economist strolls up to the smallpox cup and applauds, monocle in. | |
| "They will object now because the number is larger," | | On the empty plinth a second cup of the same shape rises and rises, as big as a house: "10.7 BILLION". His monocle pops out, and he thrusts up a placard: "OBJECTION". | |
| "which is a strange reason to object to saving more people." | | The 107 people from the chart walk past him into the big cup's shade. The cup wobbles and comes down over him. | Only the placard sticks out from under the rim. |

Sound: a pop per row; the counters' rolling clicks; a long sigh of relief; a squish under the smallpox cup; polite applause; a rising creak as the big cup grows; a monocle ping; a deep clang.

## Scene 4 · price-tag-title

- id: price-tag-title
- act: Title
- transition_in: cut
- cue: "The Price Tag on Not"
- time: 07:55.4 to 07:58.4 (3.0 s)
- voiceover: "The Price Tag on Not Being Dead."
- layer: A, title card
- bit: The price tag hangs off the word DEAD.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Price Tag on Not Being Dead." | The heading. | The period card: "THE PRICE TAG ON / NOT BEING DEAD", a price tag on a string hanging off DEAD. It turns over: "$150,000". | A skeleton walks across the bottom of the card and bumps it, and it swings. |

Sound: a whirr; a tag flip; a soft clack of bones.

## Scene 5 · priceless-footnote

- id: priceless-footnote
- act: The price tag
- transition_in: cut
- cue: "Your governments already put"
- time: 07:58.4 to 08:22.5 (24.0 s)
- voiceover: "Your governments already put a price on human life when deciding whether to approve drugs, build highways, or regulate pollution. The standard rate: one hundred and fifty thousand dollars per quality-adjusted life year. Your species finds this uncomfortable to discuss but does it constantly. You just prefer to do it in footnotes, where the dying can't see."
- layer: B, plate the-field
- bit: **The Capitol walks down a row of people pricing each one with a tag gun, and the whole row turns out to be a footnote.** The camera pulls back to the billboard it sits under: "HUMAN LIFE IS PRICELESS*".
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Your governments already put a price on human life when deciding whether to approve drugs, build highways, or regulate pollution. The standard rate: one hundred and fifty thousand dollars per quality-adjusted life year." | Governments price life to decide drugs, roads and pollution: $150,000 a year of healthy life. | Close: the Capitol on its legs walks along a row of citizens with a price-tag gun, clacking a tag onto each: one holding a pill bottle, one at the wheel of a motorcar, one coughing. Close on a tag: "$150,000 PER YEAR OF LIFE". | |
| "Your species finds this uncomfortable to discuss but does it constantly." | | The citizens read their tags and squirm. The Capitol whistles and keeps clacking. | |
| "You just prefer to do it in footnotes, where the dying can't see." | It is in the small print. | The camera pulls back and back: the row is the tiny footnote under a huge billboard over the field, "HUMAN LIFE IS PRICELESS*", and the footnote reads "*$150,000 a year". A patient in an iron bed under the billboard squints up at the headline and cannot find the asterisk. | |

Sound: a clack per tag; a whistle; a long whoosh back; a squint creak.

## Scene 6 · times-two-twelve

- id: times-two-twelve
- act: The price tag
- transition_in: same plate (the camera travels right along the field)
- cue: "The world loses two point"
- time: 08:22.5 to 08:54.0 (31.5 s)
- voiceover: "The world loses two point eight eight billion D.A.L.Y.s per year. Ninety-two point six percent are eventually avoidable with sufficient research. At one hundred and fifty thousand dollars per quality-adjusted life year, or Q.A.L.Y., that is four hundred trillion dollars per year in welfare losses. Multiply by the two hundred and twelve-year timeline shift and you get the total economic value of the health dividend: eighty-four point eight quadrillion dollars."
- layer: B, plate the-field
- bit: **One bar of lost years turns into money and copies itself 212 times to the horizon, and the receipt prints the total.** The multiplication is shown, not told.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The world loses two point eight eight billion D.A.L.Y.s per year. Ninety-two point six percent are eventually avoidable with sufficient research." | 2.88 billion healthy years a year, 92.6% avoidable. | A bar of stacked hourglasses on the field: "HEALTHY YEARS LOST A YEAR · 2.88 BILLION". All but the bottom sliver redraws dotted, like the headstones. | |
| "At one hundred and fifty thousand dollars per quality-adjusted life year, or Q.A.L.Y., that is four hundred trillion dollars per year in welfare losses." | × $150,000 = $400 trillion a year. | The Capitol's tag gun clacks a "$150,000" tag onto every dotted hourglass, and each tagged hourglass flips into a strapped bundle of green bills; the bar is money: "$400 TRILLION A YEAR". | |
| "Multiply by the two hundred and twelve-year timeline shift" | × 212. | The bar copies itself along the year ruler, one per year, faster and faster, 212 bars to the horizon. | |
| "and you get the total economic value of the health dividend: eighty-four point eight quadrillion dollars." | = $84.8 quadrillion. | Part 1's receipt unrolls across the front of the field and prints its line: "HEALTH DIVIDEND ..... $84,800,000,000,000,000". | The camera has to travel the length of the field to reach the end of the zeros. |

Sound: a clink per hourglass; a dotted tick; a clack per tag; a flip per bundle; a run of thumps, faster and faster, as the bars copy; a printer chatter.

## Scene 7 · no-sale

- id: no-sale
- act: The price tag
- transition_in: same plate (no seam)
- cue: "But that is more than"
- time: 08:54.0 to 09:13.7 (19.7 s)
- voiceover: ""But that is more than global G.D.P.!" Yes. G.D.P. (one hundred and fifteen trillion dollars) measures market transactions. It does not measure the value of not being dead, not being in pain, and not watching your children die of treatable diseases."
- layer: B, plate the-field
- bit: **The GDP register rings up toast and shoes, and says NO SALE to staying alive.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| ""But that is more than global G.D.P.!" Yes." | It is bigger than GDP. | The economist bursts in, a plaster on his head, and points: at the foot of the first "$400 TRILLION A YEAR" bar stands a brass register, "GDP", with its own bar, "$115 TRILLION", 3.5 times shorter. | |
| "G.D.P. (one hundred and fifteen trillion dollars) measures market transactions." | GDP counts sales. | A loaf, a toaster and a pair of shoes are rung up: ding, ding, ding. | |
| "It does not measure the value of not being dead, not being in pain," | | A man steps up to the counter and simply stands there, alive, breathing: the register's flag pops up, "NO SALE". A man who has just stopped holding his back does a little jig: "NO SALE". | |
| "and not watching your children die of treatable diseases." | | The family steps up together, all three alive, the boy holding his father's hand. "NO SALE". | The economist rings them up himself. The drawer opens on "$0.00". |

Sound: three dings; three flat clunks for NO SALE; a drawer slide.

## Scene 8 · host-not-my-fault

- id: host-not-my-fault
- act: The price tag
- transition_in: cut
- cue: "The one hundred and fifty"
- time: 09:13.7 to 09:27.2 (13.4 s)
- voiceover: "The one hundred and fifty thousand dollars per quality-adjusted life year, or Q.A.L.Y. figure is not something I invented. I just multiplied it by the number of sick people, which is also not my fault."
- layer: A, host
- wishonia: neutral-smile + body-open-palms; smirk-smile + body-point-right on "sick"; sideeye-closed + body-shrug on "fault."
- bit: The sick people are Earth, and Earth sneezes on her window.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The one hundred and fifty thousand dollars per quality-adjusted life year, or Q.A.L.Y. figure is not something I invented." | It is the governments' number. | Wishonia at the console, palms open. The "$150,000" tag from the footnote hangs off the ledge. The receipt keeps printing. | |
| "I just multiplied it by the number of sick people," | | She points at Earth in the window. Earth coughs; little germs puff off it. | |
| "which is also not my fault." | | She shrugs and side-eyes the camera. | Earth sneezes on the glass. She does not look round. |

Sound: the printer chatter; a cough; a big wet sneeze and a splat on glass.

## Scene 9 · monte-carlo

- id: monte-carlo
- act: The price tag
- transition_in: cut back to the-field
- cue: "The only debatable input is"
- time: 09:27.2 to 09:42.1 (15.0 s)
- voiceover: "The only debatable input is whether the timeline shift is really approximately two hundred and twelve years. See the full derivation for how that number is calculated, and the Monte Carlo simulations for what happens when every input varies."
- layer: B, plate the-field
- bit: **Monte Carlo is a man made of dice rolling along the 212 bars, and every roll changes how many there are, until he rolls himself to pieces and they settle back on 212.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The only debatable input is whether the timeline shift is really approximately two hundred and twelve years." | The weak spot is the 212. | At the far end of the 212 bars, Part 2's wooden arrow sign on a post: "212 YEARS SOONER". The economist, plaster on his head, taps it with his pointer and squints. | |
| "See the full derivation for how that number is calculated," | | The sign's face flips to the sum, "204 + 8.2", and back. | |
| "and the Monte Carlo simulations for what happens when every input varies." | Every input is varied at random, over and over. | The dice-suit businessman rolls himself along the field; with each roll the sign's digits spin like a slot machine and the row of bars stretches or shrinks to match, faster and faster until the digits are a blur. | He rolls himself apart: dice loose, suit empty. The digits click back to "212", the bars with them. The economist pockets one die. |

Sound: a tap; a flip and a flip back; a rattle and a slot-machine whirr per roll, faster; a clatter as he comes apart; three clicks as the sign settles.
