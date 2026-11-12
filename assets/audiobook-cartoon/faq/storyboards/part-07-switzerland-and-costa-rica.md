---
format: 1920x1080
duration: 3:10.6
message: "A failed trial is data, and 44.1 times more trials for the same money finds over four times more treatments even if 90% fail; and the countries that skipped war (Switzerland at 0.7% of GDP, Costa Rica with no army) are richer, live longer and were never invaded."
arc: YOU's placard says WRONG? → the card cabinet of 100,000 things that don't work grows into a tower, and YOU drives past the WRONG WAY sign off a cliff → under today's one flask the committee retires to hammocks, the NIH pays to prove water is wet and the FDA rejects page 847's footer; then 44.1 times the flasks, 90% go grey, and what is left is still four times today → Wishonia's falling failure chart and her collection of circles → YOU's placard says INEVITABLE → on the world map, Switzerland stirs chocolate in the middle of two world wars and outlives America; Figueres takes a sledgehammer to his barracks and it becomes a school and a hospital, and the tank turns round → three lines over twenty years with the city of tomorrow on the top one; the bomb over Japan, and the accountant still on 1944
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 7, "Switzerland and Costa Rica"
audio: faq.c12b2c60.mp3, 19:09.8 to 22:20.4
version: v2
---

# Part 7 storyboard: "Switzerland and Costa Rica"

- **Source:** `knowledge/appendix/faq.qmd`, "What If the Science Is Wrong?" and "War Is Human Nature"; `knowledge/economics/gdp-trajectories.qmd` for the 20-year paths.
- **The numbers:**
  - 100,000 trials (the objection's hypothetical); 100 trials over 17 years; page 847 (hardcoded, not parameters).
  - `dfda_trial_cost_reduction_factor`: 44.1x more trials for the same budget.
  - `pharma_success_rate_current_pct`: 10% (the narrator's "Even if ninety percent fail"). Derived: 44.1 × 10% = 4.41, "over four times more cures than today".
  - `switzerland_gdp_per_capita_k`: $93,000; `switzerland_defense_spending_pct`: 0.7%; `switzerland_life_expectancy`: 84 years; `us_vs_switzerland_life_expectancy_gap`: 6.5 years (so the US bar is 77.5).
  - Costa Rica abolished its army in 1948 (historical; José Figueres struck the Bellavista barracks wall with a sledgehammer on 1 December 1948).
  - The 20-year paths: the narrator says the Treaty Path is **16.5 times** the GDP of doing nothing; the current `treaty_trajectory_gdp_vs_current_trajectory_multiplier_year_20` is 1.71x. The Wishonia Path, `wishonia_trajectory_gdp_vs_current_trajectory_multiplier_year_20`, is 56.7x, as spoken. The screen uses the narrator's 16.5× and 56.7×, both marked PROJECTED.
- **What the viewer must leave with:** more trials means more found even when most fail, and countries that stopped preparing for war got richer and healthier without being invaded.
- **Plates:**
  - `step-four`: YOU on step four (Part 1).
  - `trial-chart`: a two-bar chart, "TRIALS, SAME BUDGET", its bars made of flasks, with the committee's table, a lab bench and the FDA building under the short TODAY bar; beside it a card cabinet, and in front a plain road with a WRONG WAY sign that runs off a cliff.
  - `world-map`: an engraved world map: Switzerland in the middle of Europe, Costa Rica in Central America, Japan at the far right, an accountant's desk at the map's edge.
  - Host scenes: Wishonia at her console on the observation deck.
- **Cast:** existing: `you`, `scientist`, `fda-sip`, `binder`, `patient-skeleton`, `skeleton`, `germ`, `tank`, `mushroom`, `flames`, `missile`, `oil-derrick`, `hospital`, `counter-sign`, `city-of-tomorrow`, `flying-car`, `calendar`, `cobweb`, `cuckoo`, `road`, `cliff-face`. From ep. 1 (not drawn yet): `filing-cabinet`, `committee`, `beard`, `hammock-palms`, `bucket`, `magnifier`, `flask`, `hamster-wheel`, `chalkboard` (Part 2's CIRCULAR SPENDING board), `schoolhouse`, `price-tag`, `citizen`, `accountant`, `world-map`. From Part 2: `cadillac`. From Part 10: `nih-building`. New: `wrong-way-sign`, `swiss-chocolatier` (with his copper pot), `jose-figueres` (with his sledgehammer), `barracks`.
- **Callbacks:** the CIRCULAR SPENDING board from Part 2 and the money machine of ep. 1 Part 2 join Wishonia's collection of circles. The Cadillac from Part 2 is YOU's car. Ep. 1 Part 4's "DAYS WITHOUT" counter sign counts Costa Rica's days without an invasion. Ep. 1 Part 2's city of tomorrow rides the top GDP line. Part 2 borrows the barracks for Pape's garden. YOU's beard is longer again.
- **New art:** a WRONG WAY road sign; a 1950s Swiss chocolatier in a white apron stirring a copper pot of chocolate; José Figueres (Costa Rica, 1948, moustache and suit) with a sledgehammer; a stone barracks with crenellations, which breaks open into two halves.
- **Kit additions:**
  - `grey`: a run of cut-outs in a bar goes grey one after another (the 90% that fail).
  - `chart`: a three-line chart whose top line can carry cut-outs along it.

## Scene 1 · science-objection

- id: science-objection
- act: The science
- transition_in: cut
- cue: ""What If the Science Is Wrong?""
- time: 19:09.8 to 19:17.0 (7.3 s)
- voiceover: "What If the Science Is Wrong? Objection: "What if we fund one hundred thousand trials and nothing gets cured?"."
- layer: B, plate step-four
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| ""What If the Science Is Wrong?"" | The heading. | The period card drops in: "WHAT IF THE SCIENCE IS WRONG?". | |
| "Objection: "What if we fund one hundred thousand trials and nothing gets cured?"" | | YOU's placard: "WRONG?". | |

Sound: a clank.

## Scene 2 · wrong-way-sign

- id: wrong-way-sign
- act: The science
- transition_in: cut
- cue: "Then you know one hundred thousand things"
- time: 19:17.0 to 19:34.5 (17.4 s)
- voiceover: "Then you know one hundred thousand things that don't work. This is called data. You've been collecting it for four hundred years. It is the only method you have that actually works. Being afraid of negative results is like being afraid of road signs that say "wrong way." The sign is helping you. Stop being angry at the sign."
- layer: B, plate trial-chart
- bit: **A failed trial is a WRONG WAY sign; YOU shakes his fist at the sign and drives off the cliff it was warning him about.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Then you know one hundred thousand things that don't work. This is called data." | Failures are knowledge. | A card cabinet: drawer after drawer of index cards slides out, each card stamped "DOESN'T WORK". The cabinet grows upward, drawer on drawer, "100,000". "DATA" on its brass plate. | |
| "You've been collecting it for four hundred years. It is the only method you have that actually works." | | The tower of drawers is now taller than the frame; the Scientist at the top files one more card. | |
| "Being afraid of negative results is like being afraid of road signs that say "wrong way."" | | The road in front of it. YOU drives up in his Cadillac. A sign stands by the road: "WRONG WAY". He brakes, gets out and shakes his fist at it. | |
| "The sign is helping you. Stop being angry at the sign." | | He gets back in, drives past it, and off the cliff. A boom down below; a puff of smoke rises. | His charred fedora floats back up and lands on the sign. |

Sound: drawer after drawer sliding; a filing thunk; an engine and a squeal of brakes; a falling whistle; a boom.

## Scene 3 · current-system

- id: current-system
- act: The science
- transition_in: same plate (no seam)
- cue: "The current system:"
- time: 19:34.5 to 20:16.4 (42.0 s)
- voiceover: "The current system: One hundred trials over seventeen years, learn nothing, many retire wealthy (with pensions). N.I.H. funding safe research confirming water is wet (it is; here is the grant). F.D.A. blocking trials because the paperwork had a typo on page eight hundred and forty-seven (this actually happens; the typo was in a footer). Your decentralized framework will run forty-four point one times more trials for the same budget. Even if ninety percent fail, you get over four times more cures than today. Failure at scale beats success at a standstill. A ninety percent failure rate is normal for the first two hundred years of any medical system."
- layer: B, plate trial-chart
- bit: **Under today's one flask, the current system retires, proves water is wet and rejects a footer; beside it rises a tower of 44 flasks, nine in ten go grey, and the four left are still four times today.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The current system: One hundred trials over seventeen years, learn nothing, many retire wealthy (with pensions)." | Slow and few. | Under the chart's TODAY bar, one bubbling flask: the committee at its table, "100 TRIALS / 17 YEARS". Their beards grow down to the floor; they get up and lie down in hammocks between two palms, each holding a pension cheque. | The table is still bare: nothing learned. |
| "N.I.H. funding safe research confirming water is wet (it is; here is the grant)." | | The Scientist dips a finger in a bucket of water, looks at it and nods: "WET ✓". The NIH building leans in and hands her a big cardboard cheque, "GRANT". | She dips the finger again to be sure, and gets a second cheque. |
| "F.D.A. blocking trials because the paperwork had a typo on page eight hundred and forty-seven (this actually happens; the typo was in a footer)." | | The FDA building turns a phone-book binder to page 847, holds a magnifying glass to the very bottom of the page, and stamps the whole binder "REJECTED". | Behind it, the line of patients waiting for that trial has turned into grinning skeletons while it squinted. |
| "Your decentralized framework will run forty-four point one times more trials for the same budget." | 44.1 times the trials. | The camera tilts up the chart: beside TODAY's one flask, "DECENTRALIZED", a tower of 44 flasks stacks up with a clink each: "44.1×". | |
| "Even if ninety percent fail, you get over four times more cures than today." | 90% fail, and over 4 times as many are found. | Nine in every ten flasks in the tall tower go grey and stop bubbling, one after another. The four still bubbling slide out and line up beside today's one flask: "4×". Germs topple X-eyed behind them. | |
| "Failure at scale beats success at a standstill. On Wishonia, we considered ninety percent failure rates normal for the first two hundred years." | | The grey flasks bow politely and walk off. | |

Sound: a whistle of beards; a hammock creak; a plink of a finger in water; a stamp; a clink per flask, faster; a fizzle per grey flask; a ding on "four"; a pop per germ.

## Scene 4 · circles

- id: circles
- act: The science
- transition_in: cut
- cue: "Then the failure rate dropped"
- time: 20:16.4 to 20:32.4 (16.0 s)
- voiceover: "Then the failure rate dropped because we had data. You don't have data because you're afraid of failure. You're afraid of failure because you don't have data. This is a circle. I keep finding circles in your systems. None of them are the good kind."
- layer: A, host
- wishonia: happy-smile + body-presenting; skeptical-smile + body-point-right on "You don't"; eyeroll-smile + body-counting on "circle."; sad-closed + body-shrug on "None of them"
- bit: Wishonia's falling line, then Earth's circle, then her collection of Earth's circles.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Then the failure rate dropped because we had data." | | On the console screen a line chart, "WISHONIA: FAILURE RATE", falls steadily. | |
| "You don't have data because you're afraid of failure. You're afraid of failure because you don't have data." | | The screen flips to YOU running in a hamster wheel. | |
| "This is a circle. I keep finding circles in your systems. None of them are the good kind." | | She lays three things on the ledge in a row: the hamster wheel, the CIRCULAR SPENDING chalkboard from Part 2, and a tiny model of ep. 1's money machine running its loop. | |

Sound: a falling tone; a squeaky wheel; three thunks on the ledge.

## Scene 5 · war-nature-objection

- id: war-nature-objection
- act: War is human nature
- transition_in: cut
- cue: ""War Is Human Nature"."
- time: 20:32.4 to 20:43.9 (11.5 s)
- voiceover: "War Is Human Nature Objection: "War is inevitable. Countries need militaries to survive.". Several countries tested this hypothesis and got different results."
- layer: B, plate step-four
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| ""War Is Human Nature"." | The heading. | The period card drops in: "WAR IS HUMAN NATURE". | |
| "Objection: "War is inevitable. Countries need militaries to survive."" | | YOU's placard: "INEVITABLE". | |
| "Several countries tested this hypothesis and got different results." | | Two test tubes drop into a rack beside YOU, labelled SWITZERLAND and COSTA RICA. | |

Sound: a clank; two glass clinks.

## Scene 6 · switzerland

- id: switzerland
- act: War is human nature
- transition_in: cut
- cue: "Switzerland:"
- time: 20:43.9 to 21:10.6 (26.7 s)
- voiceover: "Switzerland: Over two hundred years avoiding major wars. Surrounded by both World Wars (literally in the middle; made chocolate, stayed alive). G.D.P. per capita: ninety-three thousand dollars (not killing people is profitable). Military spending: zero point seven percent of G.D.P. Life expectancy: eighty-four years (six point five years longer than Americans who spend five times more on "defense")."
- layer: B, plate world-map
- bit: **Europe burns twice around one man calmly stirring chocolate, and he outlives everybody.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Switzerland: Over two hundred years avoiding major wars." | 200 years of peace. | Close on Europe on the world map, Switzerland in the middle. On it a Swiss chocolatier in a white apron stirs a copper pot. A cuckoo clock beside him pops "200 YEARS". | |
| "Surrounded by both World Wars (literally in the middle; made chocolate, stayed alive)." | | Every country around him bursts into flame: tanks, explosions, smoke, "1914". It dies down, then flares again, "1939". He keeps stirring, tastes it, and adds a pinch of sugar. | A shell lands in his pot and he stirs it in. |
| "G.D.P. per capita: ninety-three thousand dollars (not killing people is profitable). Defense spending: zero point seven percent of G.D.P." | $93,000 per person; 0.7% on the military. | Bars drop in over the map: "$93,000", a tall bar of chocolate bars; beside it a tiny bar, "0.7%", one plain missile lying on its side. | |
| "Life expectancy: eighty-four years (six point five years longer than Americans who spend five times more on "defense")." | 84 years, 6.5 longer than the US. | Two bars, "YEARS OF LIFE": SWITZERLAND "84", the chocolatier sitting on top; USA 6.5 shorter, a missile stuck in its top like a candle in a cake. | |

Sound: a cuckoo; booms and fire all around, muffled; a stir; a plop as the shell drops in; a stamp per bar.

## Scene 7 · costa-rica

- id: costa-rica
- act: War is human nature
- transition_in: same plate (no seam)
- cue: "Costa Rica:"
- time: 21:10.6 to 21:40.4 (29.7 s)
- voiceover: "Costa Rica: Abolished its army in nineteen forty-eight (said "no thank you" to the entire concept). Still sovereign seventy-five plus years later (nobody invaded the country with no oil). Redirected military budget to education and health. Life expectancy matches U.S. at a fraction of the cost. Zero invasions since (turns out nobody wants to conquer happy, educated people with good healthcare and no resentment)."
- layer: B, plate world-map
- bit: **Figueres takes a sledgehammer to his own barracks, it turns into a school and a hospital, and the tank that comes to invade turns round.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Costa Rica: Abolished its army in nineteen forty-eight (said "no thank you" to the entire concept)." | No army since 1948. | The camera crosses the Atlantic to Central America. On Costa Rica, José Figueres in his suit swings a sledgehammer at the wall of a stone barracks: "1948". A crack runs up it. | He tips his hat to it. |
| "Still sovereign seventy-five plus years later (nobody invaded the country with no oil)." | | Tanks roll past across the map toward an oil derrick in the distance and ignore Costa Rica. | |
| "Redirected military budget to education and health." | | The barracks falls open like a box: its halves are a schoolhouse and a hospital. | |
| "Life expectancy matches the U.S. at a fraction of the cost." | | Two bars, "YEARS OF LIFE", COSTA RICA and USA, the same height; under them two price tags, a little one and a huge one. | |
| "Zero invasions since (turns out nobody wants to conquer happy, educated people with good healthcare and no resentment)." | Never invaded. | A counter sign on a post: "DAYS WITHOUT AN INVASION", its digits rolling up and up. A tank rolls up to the border, looks at the waving schoolchildren and patients, and reverses away. | |

Sound: a clang and a crack; tank treads in the distance; a fall of stone and a school bell; a stamp; a digit rattle; a reversing beep.

## Scene 8 · twenty-year-paths

- id: twenty-year-paths
- act: War is human nature
- transition_in: same plate (no seam)
- cue: "Scale that up globally"
- time: 21:40.4 to 22:20.4 (40.0 s)
- voiceover: "Scale that up globally and the twenty-year model projects the treaty take-hold path producing one point seven one times the G.D.P. of doing nothing, and the Optimal Governance Trajectory producing fifty-six point seven times. Per person, the treaty path adds five hundred and eighteen thousand, eight hundred and seventy-nine dollars in lifetime income. Not murdering people is good for the economy. This should not be a surprising finding, but on your planet, it is. Nuclear weapons made territorial conquest largely obsolete in nineteen forty-five. You're still budgeting like it's nineteen forty-four. It's been eighty years. Somebody should tell the accountants."
- layer: B, plate world-map
- bit: **Over the whole world map the not-murdering lines climb, and the city of tomorrow rides the top one; at the map's edge the accountant who never noticed 1945 keeps adding until he is a skeleton.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Scale that up globally and the twenty-year model projects the Treaty Path producing sixteen point five times the G.D.P. of doing nothing," | Projected 16.5 times over 20 years. | The camera pulls back to the whole map, and a line chart is inked over it, "GDP AFTER 20 YEARS (PROJECTED)", 0 to 20 years. The "DOING NOTHING" line crawls along the bottom; the "TREATY PATH" line climbs to "16.5×". | |
| "and the Wishonia Path producing fifty-six point seven times." | 56.7 times. | The "WISHONIA PATH" line shoots past it to "56.7×"; the camera tilts up to follow. | |
| "Not murdering people is good for the economy. This should not be a surprising finding, but on your planet, it is." | | The 1950s city of tomorrow rides up the top line like a train, domes and monorail and flying car. On the bottom line, a citizen raises his eyebrows in surprise. | |
| "Nuclear weapons made territorial conquest largely obsolete in nineteen forty-five." | | The chart fades. Over Japan, at the right of the map, a mushroom cloud goes up: "1945". | |
| "You're still budgeting like it's nineteen forty-four. It's been eighty years." | | At a desk on the map's edge an accountant adds up with his pencil under a tear-off calendar stuck on "1944". He does not look up. Cobwebs spread over him; he greys, and becomes a skeleton, still adding. | |
| "Somebody should tell the accountants." | | A hand taps his shoulder; the skeleton falls into a neat heap of bones. | The calendar tears off one page: underneath, "1944". |

Sound: a drawing scratch per line; a slide whistle up; a train whistle; a single "huh"; a distant boom; a pencil scratch, on and on; a tap and a clatter of bones; a paper tear.
