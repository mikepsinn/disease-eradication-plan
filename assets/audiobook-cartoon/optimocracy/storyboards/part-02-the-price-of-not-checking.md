---
format: 1920x1080
duration: 2:52.0
message: "Not checking is expensive: America spends more than Switzerland and dies 6.5 years sooner, governance runs at half power, and the War on Drugs got 18 times worse while its budget went up; meanwhile 10,000 places have already run the experiments."
arc: Title card (its price tag spins up) → Uncle Sam and the Swiss walk the road of life, and Uncle Sam falls in his grave 6.5 years early while the debate panel grows beards → the civilization car on the same road runs on half its cylinders, the other half a committee arguing about forward, until the glovebox drops two audits on it → Nixon's tank fires at a bag of dope and the overdose line climbs in headstones from 6,000 to 100,000 while the budget is piled higher → the map of 10,000 experiments: Kansas's school falls flat, fifty wage tags, Portugal's deckchair and Singapore's prison jacket, and YOU watches the twerking video → the drug machine and the Optimitron at the map's foot, same question, a mountain more dead
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 2, "The Price of Not Checking"
audio: optimocracy.27caf050.mp3, 04:46.7 to 07:38.7
version: v2
---

# Part 2 storyboard: "The Price of Not Checking"

- **Source:** `knowledge/solution/optimocracy.qmd`, "The Price of Not Checking" and "The Answer Key You Already Have"; `knowledge/appendix/political-dysfunction-tax.qmd` and `knowledge/appendix/us-efficiency-audit.qmd` for the waste numbers.
- **The numbers:**
  - The spending gap: the narrator says "three hundred percentage points more of G.D.P."; that is a units bug in the audio. `us_vs_switzerland_spending_gap` is 3 percentage points (`us_govt_spending_pct_gdp` and `switzerland_govt_spending_pct_gdp` print as 3800% and 3500% in `_variables.yml`, the same bug: 38% and 35% of GDP). The spending bars carry no number on screen.
  - `us_vs_switzerland_life_expectancy_gap` 6.5 years more life in Switzerland (`switzerland_life_expectancy` 84 years).
  - `us_gov_waste_total`: the narrator says $4.9 trillion; `_variables.yml` now has $4.98 trillion. `us_gov_waste_pct_gdp`: the narrator says 17%; now 17.3%. The screen uses "$4.9 TRILLION".
  - `political_dysfunction_global_opportunity_cost_total` $101 trillion; `political_dysfunction_global_opportunity_cost_pct_gdp` 87.8% of GDP.
  - `political_dysfunction_global_efficiency_score`: the narrator says 51.9%; `_variables.yml` now has 51.8%. The gauge reads "51.9%".
  - `us_gov_waste_drug_war` $90 billion a year on the War on Drugs.
  - Spoken, cited, not parameters: about 6,000 overdose deaths a year in 1971 (`cdc-overdose-1980`), over 100,000 after fifty years (`cdc-overdose-2023`); over a trillion dollars spent; "eighteen times worse" (100,000 ÷ 6,000 is about 17, the narrator's round figure). For the chart: the line of headstones starts at 6,000 in 1971 and ends above 100,000 in 2023; the spending bars under it rise every decade.
  - Spoken, not parameters: fifty years of debate; ten thousand jurisdictions; fifty states and thirty years of minimum wages.
- **What the viewer must leave with:** nobody checks whether policies work, so America pays more to die sooner and the War on Drugs is funded harder as it fails, while the answers are already sitting in 10,000 natural experiments.
- **Plates:**
  - `the-road`: a long plain road on aged paper. For pay-more-die-sooner it is marked in years of life, with two "GOVERNMENT SPENDING" bars at its start, two graves along it and a debate table at its side; for half-the-cylinders the civilization car stands on it.
  - `war-on-drugs-chart`: a line chart on aged paper, "OVERDOSE DEATHS A YEAR", 1971 to 2023; under it, bars of "WAR ON DRUGS SPENDING". Nixon's podium at the left end.
  - `experiment-map`: the engraved world map, covered in 10,000 tiny pins; the camera dives to pairs of pins on it. At its foot, the Optimitron and the decentralized FDA's laptop (same-question).
- **Cast:** existing cut-outs: `uncle-sam`, `headstone`, `skeleton`, `politician-red`, `politician-blue`, `calendar`, `binder`, `gauge`, `bill-plain`, `bill-war`, `bundle-war`, `tank`, `cobweb`, `spider`, `idler` (Portugal), `inmate-jacket` (Singapore), `you`, `google-phone`, `laptop`, `pill-bottle`, `capitol`. Registered, not drawn yet: `committee`, `beard`, `optimitron` (as a cut-out), `world-map`, `pins-and-string`, `schoolhouse`, `price-tag`, `flask`, `twerker`. New: `swiss-man`, `car-cutaway`, `nixon`, `dope-bag`.
- **Callbacks:**
  - Episode 1 Part 17's Optimitron chart of the War on Drugs: here the chart's line is built of headstones, and the Optimitron sits in the corner, unplugged and cobwebbed.
  - Part 1's phone and its twerking video: YOU watches it while the experiments go off behind him.
  - The decentralized FDA's laptop (episode 1 Part 14's) stands beside the Optimitron in same-question.
- **New art:**
  - `swiss-man`: a cheerful Swiss gentleman in a 1950s loden coat and an alpine hat with a feather, walking stick, a wheel of cheese under one arm; older, white-haired and still walking.
  - `car-cutaway`: a 1950s chrome sedan with tail fins in cutaway, eight cylinders as separate pieces with pistons; four of the cylinders open at the top to seat little committee men; a glovebox that drops open.
  - `nixon`: Richard Nixon caricatured: ski-jump nose, jowls, five o'clock shadow, both arms up in V signs; at a 1971 podium (shared with the central-banks and 1-percent-treaty chapters).
  - `dope-bag`: a little brown paper bag twisted shut at the top, a skull and crossbones on it (the street drugs; the medicine `pill-bottle` stays out of the drug war).
- **Kit additions:**
  - `chain` along a chart line (the headstones up the overdose line), as in episode 1 Part 2.

## Scene 1 · price-title

- id: price-title
- act: Title
- transition_in: cut
- cue: "The Price of Not Checking"
- time: 04:46.7 to 04:49.5 (2.9 s)
- voiceover: "The Price of Not Checking."
- layer: A, title card
- bit: The title card has a price tag, and it spins.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Price of Not Checking." | The heading. | The period card. A price tag on a string hangs from the corner of the words; its digits spin up like a petrol pump and run off the edge of the tag. | |

Sound: a whirr; a fast pump-meter tick.

## Scene 2 · pay-more-die-sooner

- id: pay-more-die-sooner
- act: Paying more, dying sooner
- transition_in: cut
- cue: "The United States spends"
- time: 04:49.5 to 05:18.8 (29.3 s)
- voiceover: "The United States spends three hundred percentage points more of G.D.P. than Switzerland on government. Switzerland gets six point five more years of life expectancy. One of these countries is doing it wrong. On Wishonia, we would check which one. On Earth, you have a debate about it. The debate has been going on for fifty years. The Swiss are still winning. You're paying more and dying sooner, and your response is to have opinions about it."
- layer: B, plate the-road
- bit: **Uncle Sam pays more for the walk of life and falls into his grave first.** Two bars become two walkers on a road marked in years; Uncle Sam drops into a hole 6.5 years short while the Swiss strolls on, and the debaters at the roadside grow beards for fifty years. Payoff: Uncle Sam's skeleton climbs out and joins the debate.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The United States spends three hundred percentage points more of G.D.P. than Switzerland on government." | America spends more. | Two bars, "GOVERNMENT SPENDING": Uncle Sam stands on the taller one, the Swiss gentleman on the shorter. Both hop down onto the long road, "YEARS OF LIFE". | |
| "Switzerland gets six point five more years of life expectancy." | The Swiss live 6.5 years longer. | They walk side by side. Uncle Sam steps into an open grave and drops out of sight. The Swiss walks on, the camera with him, and "+6.5 YEARS" stretches between the grave and his feet. | Uncle Sam's hat lands on the headstone a second later. |
| "One of these countries is doing it wrong. On Wishonia, we would check which one. On Earth, you have a debate about it." | Nobody checks; they debate. | At the roadside, a debate table: the red-tie and the blue-tie politicians point at the grave and argue, scribbles flying. | |
| "The debate has been going on for fifty years. The Swiss are still winning." | | A calendar on the table sheds fifty years of pages. The debaters grow long white beards down to the floor. Far down the road, the Swiss gentleman, white-haired now, is still strolling. | He tips his hat to them. |
| "You're paying more and dying sooner, and your response is to have opinions about it." | | Uncle Sam's skeleton climbs out of the grave in his top hat, sits at the table and starts arguing too. | |

Sound: two thumps as they hop down; footsteps; a slide whistle down into the grave and a hat plop; a babble of argument; a calendar riffle; a yodel far off.

## Scene 3 · half-the-cylinders

- id: half-the-cylinders
- act: Running at half power
- transition_in: cut
- cue: "Documented U.S. governance waste"
- time: 05:18.8 to 06:03.6 (44.7 s)
- voiceover: "Documented U.S. governance waste totals four point nine trillion dollars (seventeen percent of G.D.P.). Globally, the opportunity cost of suboptimal policy reaches one hundred and one trillion dollars (eighty-seven point eight percent of G.D.P.), putting your civilization's governance efficiency at fifty-one point nine percent. Your species is running at roughly half its technological potential. Imagine building a car, then only turning on half the cylinders because the other half are controlled by a committee that meets once a year and disagrees about what "forward" means. (For the full accounting, see the Political Dysfunction Tax and U.S. Efficiency Audit.)"
- layer: B, plate the-road
- bit: **Civilization is a gleaming car running on four of its eight cylinders, because a committee sits in the other four.** Money blows out of the exhaust, the gauge reads 51.9%, and the car drives in a circle while the committee points every way but forward. Payoff: the glovebox drops the two audits on the committee, and two cylinders start firing.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Documented U.S. governance waste totals four point nine trillion dollars (seventeen percent of G.D.P.). Globally, the opportunity cost of suboptimal policy reaches one hundred and one trillion dollars (eighty-seven point eight percent of G.D.P.)," | America wastes $4.9 trillion a year; the world loses $101 trillion. | The big chrome sedan in cutaway on the road, engine open. It coughs: plain bills blow out of the exhaust in a cloud. "$4.9 TRILLION" stamps in the cloud. The camera pulls back as the cloud grows to fill the sky: "$101 TRILLION". | |
| "putting your civilization's governance efficiency at fifty-one point nine percent. Your species is running at roughly half its technological potential." | Civilization runs at about half power. | Push in on the dashboard gauge, "GOVERNANCE EFFICIENCY". The needle wobbles and settles on 51.9%. | |
| "Imagine building a car, then only turning on half the cylinders because the other half are controlled by a committee that meets once a year and disagrees about what "forward" means." | Half the machine is run by a committee. | Into the engine: four cylinders pump away. In each of the other four sits a committee man, each pointing a different way: up, down, back, at another committee man. A calendar on the dashboard flips once, and they all switch directions. The car drives in a slow circle. | One points straight down, and the car sinks a foot into the road. |
| "(For the full accounting, see the Political Dysfunction Tax and U.S. Efficiency Audit.)" | | The glovebox pops open. Two fat binders, POLITICAL DYSFUNCTION TAX and U.S. EFFICIENCY AUDIT, drop out and flatten two committee men in their cylinders. | Two cylinders start firing. The needle twitches up one notch. |

Sound: a cough and a flutter of bills; two stamps; a needle wobble; the chug of four cylinders; a committee babble; a sinking crunch; two book thuds and two new chugs.

## Scene 4 · war-on-drugs

- id: war-on-drugs
- act: Not checking
- transition_in: cut
- cue: "Or consider the War on Drugs"
- time: 06:03.6 to 06:43.5 (39.9 s)
- voiceover: "Or consider the War on Drugs. Your species spends ninety billion dollars per year on it. When Nixon declared it in nineteen seventy-one, about six thousand Americans died annually from drug overdoses. After fifty years and over a trillion dollars, that number exceeded one hundred thousand. At no point did anyone check whether the policy was working. At no point did anyone stop funding it because it wasn't. On Wishonia, if you spend a trillion dollars on something and the problem gets eighteen times worse, you stop doing it. On Earth, you increase the budget."
- layer: B, plate war-on-drugs-chart
- bit: **Nixon's tank fires at a bag of dope, and after every shot there are more bags and more headstones.** The overdose line climbs as a chain of headstones from 6,000 to 100,000, the spending bars feed the tank, and the Optimitron sits unplugged in the corner. Payoff: the budget gets piled higher, the tank grows, and the recoil knocks Nixon off his podium.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Or consider the War on Drugs. Your species spends ninety billion dollars per year on it." | $90 billion a year. | The chart, "OVERDOSE DEATHS A YEAR", empty. Under it a bar of war bills, "$90 BILLION A YEAR", stands beside a tank. | |
| "When Nixon declared it in nineteen seventy-one, about six thousand Americans died annually from drug overdoses." | It began in 1971 at 6,000 deaths a year. | Nixon at a 1971 podium throws up both V signs. The tank fires at a little paper bag of dope on the chart, a skull and crossbones on it. The smoke clears: the bag is fine, and there are two of them. A small stack of headstones at 1971: "6,000". | |
| "After fifty years and over a trillion dollars, that number exceeded one hundred thousand. At no point did anyone check whether the policy was working. At no point did anyone stop funding it because it wasn't." | 50 years and a trillion dollars later, 100,000; nobody checked or stopped. | War bills march into the tank; it fires again and again across the decades. After every shot there are more bags, and a chain of headstones climbs the chart behind them, steeper and steeper, to "100,000" at 2023. In the bottom corner, the Optimitron sits with its plug on the floor, cobwebbed, a spider asleep on its dial. | Its eyes follow the line up. |
| "On Wishonia, if you spend a trillion dollars on something and the problem gets eighteen times worse, you stop doing it." | It got 18 times worse. | A bracket from the 6,000 stack to the 100,000 stack: "×18". | |
| "On Earth, you increase the budget." | | Three fat bundles of war bills thump onto the spending bar, and it grows with each. The tank gets bigger with each one. It fires; the chart line breaks out through the top of the frame. | The recoil knocks Nixon off his podium, still giving the V signs. |

Sound: a tank boom per shot, faster; a pop per new bag; a thunk per headstone; a soft snore from the spider; a stamp for ×18; three bundle thumps; a huge boom.

## Scene 5 · answer-key-title

- id: answer-key-title
- act: The answer key
- transition_in: cut
- cue: "The Answer Key You Already Have"
- time: 06:43.5 to 06:46.1 (2.7 s)
- voiceover: "The Answer Key You Already Have."
- layer: A, title card
- bit: The heading, with the answers written on the back of the card.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Answer Key You Already Have." | The heading. | The period card. It flips over: the back is a printed answer sheet, every bubble filled in. | |

Sound: a whirr; a card flip.

## Scene 6 · ten-thousand-experiments

- id: ten-thousand-experiments
- act: The answer key
- transition_in: cut
- cue: "Your planet has roughly ten thousand"
- time: 06:46.1 to 07:18.7 (32.6 s)
- voiceover: "Your planet has roughly ten thousand jurisdictions making different policy choices. Kansas cut education funding; Minnesota increased it. Fifty states adopted different minimum wages over thirty years. Portugal decriminalized drugs; Singapore didn't. These are natural experiments, and the math can now figure out which policy caused which result, without needing anyone's permission to run an experiment. The experiment already happened. You just weren't paying attention."
- layer: B, plate experiment-map
- bit: **The whole map is a lab, and every experiment has already gone off.** The camera dives to pairs of pins that chose differently and shows what happened to each; then every pin is a bubbling flask. Payoff: YOU, in front of the map, is watching the twerking video while the flasks pop behind him.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Your planet has roughly ten thousand jurisdictions making different policy choices." | 10,000 places choose differently. | The world map fills the frame, covered in tiny pins, "10,000" in the corner. | |
| "Kansas cut education funding; Minnesota increased it. Fifty states adopted different minimum wages over thirty years." | | Dive to two pins in the middle of America, KANSAS and MINNESOTA, each with its schoolhouse. Scissors snip Kansas's budget ribbon and its walls fall flat round the kids at their desks; Minnesota's bell rings. Pull out a little: fifty pins across America, each with a wage tag on a string, spin to fifty different numbers. | The Kansas kids keep sitting at their desks in the open air. |
| "Portugal decriminalized drugs; Singapore didn't." | | Two pins side by side. On PORTUGAL, a man with his feet up in a deckchair. On SINGAPORE, a man in a prison jacket. | |
| "These are natural experiments, and the math can now figure out which policy caused which result, without needing anyone's permission to run an experiment." | The differences are experiments, readable without permission. | Pull right out: every pin on the map is now a little flask, bubbling. The Optimitron's cord drops onto the map, plugs in, and a stream of result cards runs up the cord into it. | |
| "The experiment already happened. You just weren't paying attention." | It's done; nobody looked. | In front of the map, YOU stands with his back to it, staring at his phone and its twerking lady. Behind him, the flasks pop one after another like fireworks. | He chuckles at the phone. |

Sound: a soft field of pin clicks; a snip and a wall-flat slam; a school bell; spinning tags; bubbling; a plug click and a card-shuffle stream; pops, and the phone's tinny music.

## Scene 7 · same-question

- id: same-question
- act: The answer key
- transition_in: same plate (no seam)
- cue: "Same logic as your decentralized"
- time: 07:18.7 to 07:38.7 (19.9 s)
- voiceover: "Same logic as your decentralized F.D.A.: watch what actually happens, then analyze the data. Your decentralized F.D.A. applies this to medicine. The Evidence Machine applies it to governance. Instead of "which drug works?" you're asking "which policy works?" Same question, higher body count."
- layer: B, plate experiment-map
- bit: **Two machines ask the same question, and the policy one faces a much bigger pile of dead.** At the foot of the map, the drug machine in front of a heap of skeletons and the Optimitron in front of a mountain of them, a tank on top. Payoff: the Optimitron looks up, and up, and gulps.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Same logic as your decentralized F.D.A.: watch what actually happens, then analyze the data. Your decentralized F.D.A. applies this to medicine. The Evidence Machine applies it to governance." | Watch, then analyze; one for medicine, one for government. | At the foot of the map, two machines side by side: the decentralized FDA's laptop on the left, the Optimitron on the right. Each prints a chart. The laptop pops a card with a pill bottle on it; the Optimitron pops a card with the Capitol on it. | |
| "Instead of "which drug works?" you're asking "which policy works?"" | Same question. | Over each, a card: WHICH DRUG WORKS? and WHICH POLICY WORKS? The word DRUG flips to POLICY. Otherwise the cards match. | |
| "Same question, higher body count." | More die of bad policy. | Behind each machine, the dead it is there to stop rise up out of the ground: behind the laptop, a heap of skeletons, waist high; behind the Optimitron, a mountain of skeletons that shoots up out of the frame, a tank parked on the summit and the drug war's headstones down one slope. | The Optimitron looks up, and up, and gulps. |

Sound: two printer chatters; two pops; a card flip; a rumble and a clatter of bones rising; a gulp.
