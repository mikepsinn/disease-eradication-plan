---
format: 1920x1080
duration: 2:39.7
message: "Old treaty campaigns cost $25 to 50 million; this one picks a fight with the weapons industry, so it budgets $1 billion, and it moves $27.2 billion a year, forever."
arc: The Fed's press cranks four old campaigns' coin columns taller → signing landmines away cost $40 million, digging them up $5 billion, and the signer strolls off through the field → a boxing ring: the treaty campaign kits up against a factory the size of its corner → back on the cost chart a $1 billion boxer towers over the old campaigns and splits into four years → in the ring, one punch and the factory coughs up 1% of the world's military budget, a slab a year, forever
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 2, "Inflation-Adjusted to 2024 Dollars"
audio: treaty-feasibility.858ed1cd.mp3, 04:05.0 to 06:44.7
version: v2
---

# Part 2 storyboard: "Inflation-Adjusted to 2024 Dollars"

- **Source:** `knowledge/appendix/treaty-feasibility.qmd` as narrated: "Inflation-Adjusted to 2024 Dollars", "Cost for a 1% Health Treaty" and "The Math". Its campaign cost table is the chapter's own (BLS CPI), not parameters.
- **The numbers:**
  - Campaign costs, then and in 2024 dollars (the chapter's table): Ottawa 1997 $15-25M → $30-50M; Cluster Munitions 2008 $15-25M → $23-38M; Arms Trade 2013 $20-30M → $27-41M; Nuclear Ban 2017 $10-20M → $13-25M. In today's money, $25-50M.
  - Landmines: about $40 million for the signatures, over $5 billion to dig them up (cited, `icbl-ottawa-treaty`). Derived: the digging bar is 125 times the signing bar.
  - `treaty_campaign_total_cost`: $1 billion. Derived: 20 to 40 times a historical campaign.
  - `treaty_campaign_annual_cost_amortized`: $250 million a year; `treaty_campaign_duration_years`: 4 years (so the $1 billion bundle splits into four).
  - `treaty_annual_funding`: $27.2 billion a year, which is `treaty_reduction_pct` 1% of `global_military_spending_annual_2024` $2.72 trillion. Derived: one year's slab is 27.2 times the campaign.
- **What the viewer must leave with:** signing is cheap but this is a fight with the weapons industry, so the campaign costs $1 billion, and it moves $27.2 billion a year from weapons to medicine, every year.
- **Plates:**
  - `campaign-chart`: a bar chart on aged paper, "CAMPAIGN COST (2024 $)", four coin columns, and the Fed's press at the left end with a hose to each column.
  - `landmine-chart`: a two-bar chart, "BANNING LANDMINES", over a field.
  - `boxing-ring`: an empty boxing ring on a plain floor; a little lab outside the ropes.
- **Cast:** existing: `fed-crank-up`, `fed-crank-down`, `coin-column`, `treaty-scroll`, `politician` (charred in code), `miner`, `factory-proud`, `aircraft-carrier`, `bundle-med`, `bundle-war`, `yes-button`, `briefcase`, `fedora`, `desk-calendar`, `lab`. From Part 1: `landmine`. New: `boxing-ring`, `boxing-gloves`.
- **Callbacks:** episode 1, Part 2's Fed press (`fed-crank-*`) is the thing that inflates prices here. The landmines are the ones the factory was planting in Part 1.
- **New art:**
  - a boxing ring with ropes and corner posts
  - boxing gloves, stick legs and a towel that fit `bundle-med` (the treaty campaign, as a boxer); a teaspoon for the miner
- **Kit additions:**
  - `grow`: a coin column that rises a few coins per crank, with a clink per coin.
  - `split`: one cut-out that splits into N copies that walk off in turn (the bundle into four years).

## Scene 1 · inflation-pump

- id: inflation-pump
- act: What it costs now
- transition_in: cut
- cue: "Inflation-Adjusted to twenty twenty-four Dollars"
- time: 04:05.0 to 04:51.8 (46.8 s)
- voiceover: "Inflation-Adjusted to twenty twenty-four Dollars. Using B.L.S. C.P.I. data: The Ottawa Treaty in nineteen ninety-seven cost between fifteen and twenty-five million dollars, which is thirty to fifty million in today's money. The Cluster Munitions Convention in two thousand and eight cost fifteen to twenty-five million, or twenty-three to thirty-eight million in twenty twenty-four dollars. The Arms Trade Treaty in twenty thirteen cost twenty to thirty million, which is twenty-seven to forty-one million today. The Nuclear Ban Treaty in twenty seventeen cost ten to twenty million, or thirteen to twenty-five million in twenty twenty-four dollars. In today's money: Treaty campaigns cost roughly twenty-five to fifty million dollars (twenty twenty-four U.S.D.)."
- layer: B, plate campaign-chart
- bit: **The Federal Reserve cranks its press, and every crank pumps the old campaigns' coin columns taller, the oldest one most.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Inflation-Adjusted to twenty twenty-four Dollars. Using B.L.S. C.P.I. data:" | Prices since then have risen. | A chart, "CAMPAIGN COST (2024 $)", four short coin columns, each with its treaty's name. At the left end the Fed's press building cranks its own wheel, smug; a hose runs from it to the foot of every column, through a little dial stamped "B.L.S. C.P.I.". | |
| "The Ottawa Treaty in nineteen ninety-seven cost between fifteen and twenty-five million dollars, which is thirty to fifty million in today's money." | $15-25M → $30-50M. | Crank, crank: OTTAWA 1997 grows from "$15-25M" to "$30-50M", twice as tall. | It is the oldest, so it gets the most cranks. |
| "The Cluster Munitions Convention in two thousand and eight cost fifteen to twenty-five million, or twenty-three to thirty-eight million in twenty twenty-four dollars. The Arms Trade Treaty in twenty thirteen cost twenty to thirty million, which is twenty-seven to forty-one million today." | $15-25M → $23-38M; $20-30M → $27-41M. | CLUSTER 2008 grows to "$23-38M"; ARMS TRADE 2013 to "$27-41M". | |
| "The Nuclear Ban Treaty in twenty seventeen cost ten to twenty million, or thirteen to twenty-five million in twenty twenty-four dollars." | $10-20M → $13-25M. | NUCLEAR BAN 2017 grows a little, to "$13-25M". The press gives one extra crank for luck, and Ottawa's top coin pops off. | |
| "In today's money: Treaty campaigns cost roughly twenty-five to fifty million dollars (twenty twenty-four U.S.D.)." | $25-50M. | A dashed band across all four: "$25-50M". | |

Sound: a crank clank per turn; a clink per coin; a ping as the top coin pops.

## Scene 2 · dig-them-up

- id: dig-them-up
- act: What it costs now
- transition_in: cut
- cue: "Banning landmines"
- time: 04:51.8 to 05:09.1 (17.3 s)
- voiceover: "Banning landmines: roughly forty million dollars to get the signatures, and over five billion dollars to actually dig them up. The paperwork is always the cheap part. The expensive part is doing the thing you wrote on the paperwork (your species often skips this part)."
- layer: B, plate landmine-chart
- bit: **Signing the landmines away is a knee-high bar; digging them up is a tower of mines into the clouds, with one man and a teaspoon at the bottom. The signer strolls off across the field.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Banning landmines: roughly forty million dollars to get the signatures," | $40M to sign. | A chart, "BANNING LANDMINES": "SIGNATURES $40M", a short bar of signed treaty scroll. | |
| "and over five billion dollars to actually dig them up." | $5B+ to dig up: 125 times as much. | "DIGGING THEM UP $5,000,000,000+": a tower of dug-up landmines, and the camera tilts up and up it into the clouds. All the way back down at its foot, the miner digs one more out with a teaspoon. | |
| "The paperwork is always the cheap part. The expensive part is doing the thing you wrote on the paperwork" | Doing is the expensive part. | He sets it on the tower, wipes his brow and goes back in with the spoon. | |
| "(your species often skips this part)." | | The Politician who signed strolls across the field behind him, whistling, hands in pockets. BOOM. The smoke clears on him charred, blinking, still whistling, still strolling. | |

Sound: a soft stamp for $40M; a long riser up the tower; a tiny scrape of the spoon; a whistled tune, a boom, and the whistle carrying on a little hoarse.

## Scene 3 · not-a-signature-campaign

- id: not-a-signature-campaign
- act: The fight
- transition_in: cut
- cue: "Cost for a one percent Health Treaty"
- time: 05:09.1 to 05:45.6 (36.6 s)
- voiceover: "Cost for a one percent Health Treaty. Historical treaty campaigns ran on pocket change. But this is not just a signature campaign. It is a referendum engine, lobbying operation, diplomatic push, and reserve fund aimed directly at military budgets, which means you are picking a fight with the most powerful industry your species has ever created. The relevant planning number is not what it costs to collect signatures. It is what it costs to win a fight with the people who build aircraft carriers."
- layer: B, plate boxing-ring
- bit: **A boxing ring. In one corner the treaty campaign, a money bundle on stick legs, kitted up one piece per word; in the other corner the weapons factory, so big it is the corner, with an aircraft carrier for a stool.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Cost for a one percent Health Treaty. Historical treaty campaigns ran on pocket change. But this is not just a signature campaign." | | An empty boxing ring. A strapped money bundle on stick legs ducks in under the ropes to the near corner and shadowboxes. | |
| "It is a referendum engine, lobbying operation, diplomatic push, and reserve fund" | Four jobs. | It kits up, one piece per word: a YES button strapped on as a shield, a briefcase, a fedora with a pen in the band, and a second bundle on its back. | |
| "aimed directly at military budgets, which means you are picking a fight with the most powerful industry your species has ever created." | The opponent is the weapons industry. | The camera swings to the far corner: the weapons factory fills it, cracking its white-gloved knuckles. Its missile chimneys swivel to aim at the bundle. | |
| "The relevant planning number is not what it costs to collect signatures. It is what it costs to win a fight with the people who build aircraft carriers." | Budget for the fight, not the signatures. | An aircraft carrier rolls out of the factory's door, and it sits down on it like a stool. The bundle pulls on its boxing gloves. | The bell rings and the bundle's knees knock. |

Sound: a bell; a click per piece of kit; knuckle cracks; a ship's horn and a creak as it sits; a boxing bell; a knee-knock rattle.

## Scene 4 · a-billion-dollars

- id: a-billion-dollars
- act: The fight
- transition_in: cut
- cue: "Historical treaty-signing benchmark"
- time: 05:45.6 to 06:17.6 (32.0 s)
- voiceover: "Historical treaty-signing benchmark: N.G.O.-led campaigns to get signatures on paper cost twenty-five to fifty million dollars in twenty twenty-four U.S. dollars. A modeled one percent Treaty campaign covering referendum, lobbying, diplomacy, legal work, and a reserve fund costs one billion dollars. The modeled annual burn is an average spend across the campaign window of two hundred and fifty million dollars per year."
- layer: B, plate campaign-chart
- bit: The boxer from the ring steps onto the cost chart, as big as a building next to the old campaigns, and splits into four years.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Historical treaty-signing benchmark: N.G.O.-led campaigns to get signatures on paper cost twenty-five to fifty million dollars in twenty twenty-four U.S. dollars." | $25-50M. | Scene 1's chart, its four knee-high columns under the "$25-50M" band. | |
| "A modeled one percent Treaty campaign covering referendum, lobbying, diplomacy, legal work, and a reserve fund costs one billion dollars." | $1 billion: 20 to 40 times as much. | The boxer bundle steps in beside them and grows, step by step, to "1% TREATY CAMPAIGN $1,000,000,000", twenty to forty times taller, still in its gloves. | The Fed's press stops cranking and stares. |
| "The modeled annual burn is an average spend across the campaign window of two hundred and fifty million dollars per year." | $250M a year over 4 years. | It splits into four bundles of "$250M", each standing on a calendar page, YEAR 1 to YEAR 4, and they walk off toward the ring in single file. | |

Sound: a grinding growth sound; a rip as it splits; four sets of footsteps.

## Scene 5 · the-lever

- id: the-lever
- act: The math
- transition_in: cut
- cue: "The Math"
- time: 06:17.6 to 06:44.7 (27.1 s)
- voiceover: "The Math. Modeled campaign cost: one billion dollars. What the treaty unlocks: twenty-seven point two billion dollars per year. Forever. Even before you count downstream health gains, this is a one-year redirection of government spending far larger than the campaign that triggered it. You are not buying signatures. You are buying leverage."
- layer: B, plate boxing-ring
- bit: **Back in the ring, the $1 billion boxer lands one punch, and the weapons factory coughs up a slab of war money 27 times the boxer's size; its seals flip to crosses and it slides out under the ropes to the lab. Then the bell rings every year and the factory coughs up another by itself, while the boxer sits on its stool.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Math. Modeled campaign cost: one billion dollars." | $1 billion. | The boxer bundle, "$1,000,000,000", knees still knocking, faces the factory across the ring. | |
| "What the treaty unlocks: twenty-seven point two billion dollars per year." | $27.2B a year (1% of military spending). | It shuts its eyes and swings one wild punch. The factory doubles over and coughs up a war-money bundle as big as a lorry, "$27,200,000,000 A YEAR"; its missile seals flip to crosses as it slides out under the ropes into the lab. | The boxer opens one eye, amazed. |
| "Forever." | Every year. | A calendar on the corner post flips a year, the bell dings, and the factory coughs up another slab without being hit. Flip, ding, slab; faster. | |
| "Even before you count downstream health gains, this is a one-year redirection of government spending far larger than the campaign that triggered it. You are not buying signatures. You are buying leverage." | One year is 27 times the campaign; one fight, a flow every year. | Hold on one slab beside the boxer: the boxer comes up to its ankle. Then it sits on its stool, towel round its neck, while the slabs keep sliding past. | The factory's chimneys droop a little lower each year. |

Sound: a thump for the punch and a cough; a click per seal; a slide and a thump into the lab; a bell ding and a cough per year, faster.
