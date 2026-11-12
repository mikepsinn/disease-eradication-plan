---
format: 1920x1080
duration: 3:41.6
message: "Moronia spent 42 trillion papers dying when 25 trillion would have cured disease, doubled lifespans and bought a backup planet; the difference was one percent of the money, and Earth's A.I. is learning that killing is 604 times more important than testing treatments."
arc: The title card is a mirror → Wishonia and the Calculator do the math → 42 stacks of war money on the counter flip their seals and buy a 1950s world of tomorrow, with 17 stacks left over → the city flips to craters, and the visiting civilizations faint at the receipt → one railway switch, two identical trains of voters: three carriers and a dud missile throw it, one way to craters, one to tomorrow → a tiny robot on Wishonia's console splits into two, then four; a dog jumps up and she feels better → two planets in the glass: one crumbles to ash; on the other, YOU → YOU's mirror shows the robot copying him at 604 to 1, and it gets a gold star
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 17, "The Mirror"
audio: moronia.adb9f5c0.mp3, 54:39.3 to 58:20.9
version: v2
---

# Part 17 storyboard: "The Mirror"

- **Source:** `knowledge/futures/moronia.qmd`, "The Mirror", and its P.S.; the P.S. number from `knowledge/appendix/parameters-and-calculations.qmd`.
- **The numbers:**
  - `military_to_government_clinical_trials_spending_ratio`: 604 (90% CI 453 to 888), Earth's global military spending per paper of government clinical-trial spending. It is `global_military_spending_annual_2024` ($2.72 trillion) divided by `global_government_clinical_trials_spending_annual` ($4.5 billion). The narrator says "six hundred and four times".
  - Moronia's own figures, hardcoded in `moronia.qmd`: 42 trillion papers spent dying; cure all major diseases 2 trillion; life extension to 150 years 5 trillion; universal healthcare 8 trillion; a Mars colony 10 trillion; total 25 trillion, 17 trillion left over. (The 42 trillion is Part 16's 41 trillion on weapons plus 1 trillion on medicine.)
  - For the chart: 42 stacks of one trillion each; the four purchases take 2, 5, 8 and 10 stacks, and 17 stacks stand unspent.
- **What the viewer must leave with:** self-preservation was cheaper than self-destruction, the difference between the two timelines was 1% of the money, and Earth's A.I. is being taught Moronia's lesson by Earth's own budget.
- **Word timings:** the forced alignment collapsed this part's words (19 words at 55:34.6 and 240 at 57:08.9), so the time and voiceover lines below are what `tools/storyboard-times.mjs` makes of it, not the real cut. The table Lines are right. Fix the timings (Whisper and `timing-fixes.json`) and rerun the tool before building.
- **Plates:**
  - Host: Wishonia at her console on the observation deck, Earth in the glass, with Moronia (the globe, charred) hanging beside it.
  - `the-counter`: a shop counter on aged paper, a cash register, and behind it a 1950s world-of-tomorrow skyline waiting under a dust sheet.
  - `the-switch`: one railway line that forks at a switch: one branch to craters, one to the city of tomorrow; two identical trains.
  - `the-mirror`: a tall dressing mirror on a plain field, YOU in front of it.
- **Cast:** existing: `hand-mirror`, `calculator` (host prop), `cash-register`, `receipt`, `bill-war`, `bill-med`, `city-of-tomorrow`, `market-of-tomorrow`, `flying-car`, `family-groceries`, `lab`, `hospital`, `grandma`, `wedding-party` (its cake, 150 candles in code), `germ`, `doctor`, `family`, `saucer`, `coin`, `crater`, `rail-switch`, `train`, `glowing-rectangle`, `viewers`, `treaty-scroll`, `bond`, `toy-carrier`, `missile`, `robot`, `laptop`, `desk-mug`, `democracy-dog` (Part 1's dog), `globe` (Moronia, charred), `moronian-antennae` (Part 1), `you`, `vain-mirror` (the tall mirror), `balance-scale`, `school-desk`, `gold-star`, `report-card`. New: `alien-visitors`.
- **Callbacks:**
  - The dog from "The Discovery" ("I found the dogs very pleasant").
  - The robot's split from Part 9 (agent-loop), in miniature on the console.
  - The city of tomorrow and its seal flip from the episode 1 cartoon (Part 2, host-closes).
  - The receipt from the episode 1 cartoon (Parts 10 and 12).
- **New art:**
  - `alien-visitors`: other civilizations, a row of visiting aliens as engraving cut-outs in 1950s good clothes (an octopus in a bowler, a three-eyed lady in pearls, a crystal man in a tweed jacket), one fainting; the crystal man cracked.
  - The plates above. Stamps, the receipt's lines and the numbers are code.
- **Kit additions:** a `mirror`: a cut-out that copies another's moves, flipped, a beat late (the robot in YOU's mirror).

## Scene 1 · mirror-title

- id: mirror-title
- act: Title
- transition_in: up from black
- cue: "The Mirror."
- time: 54:39.3 to 54:40.5 (1.2 s)
- voiceover: "The Mirror."
- layer: A, title card
- bit: The title looks at itself.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Mirror." | The heading. | The period card, "THE MIRROR", in the oval of a gilt hand mirror. | The letters in the glass read backwards, and then, a beat late, flip to read the right way. |

Sound: a whirr; a glass ping.

## Scene 2 · did-the-math

- id: did-the-math
- act: The math
- transition_in: iris in on her face
- cue: "I did the math."
- time: 54:40.5 to 54:44.2 (3.7 s)
- voiceover: "I did the math. I like math. Math doesn't have opinions."
- layer: A, host
- wishonia: happy-smile + body-counting; excited-ee + body-hand-chest on "I like math."; smirk-closed + body-palms-down on "opinions."
- bit: Wishonia hugs the Calculator, which has no feelings about it.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "I did the math. I like math. Math doesn't have opinions." | | Wishonia at the console taps the Calculator, then gives it a little hug. Moronia in the glass, ash grey. The Calculator's face stays flat. | It prints one blank inch of tape. |

Sound: key taps; a printer zip.

## Scene 3 · what-it-could-buy

- id: what-it-could-buy
- act: The math
- transition_in: cut
- cue: "Forty-two trillion papers"
- time: 54:44.2 to 55:44.8 (60.6 s)
- voiceover: "Forty-two trillion papers is what Moronia spent dying. Here is what forty-two trillion papers could have bought instead: To cure all major diseases would cost two trillion papers. Life extension to one hundred and fifty years would cost five trillion papers. Universal healthcare would cost eight trillion papers. A Mars colony (backup plan) would cost ten trillion papers. The total is twenty-five trillion papers (with seventeen trillion papers remaining for whatever they wanted). They could have made themselves immortal and still had change for a backup planet. Instead they bought craters. I find this difficult to explain to other civilizations. "Surely not," they say. "Surely a species wouldn't spend forty-two trillion units of value on self-destruction when self-preservation was cheaper." I show them the receipts. They stop asking questions."
- layer: B, plate the-counter, then A, host
- wishonia: smirk-smile + body-open-palms on "I find this"; skeptical-smile + body-shrug on "Surely not,"; sideeye-closed + body-presenting on "I show them the receipts."
- bit: **Moronia's death money stands on a shop counter in 42 stacks, and stack by stack it flips its seals and buys a world of tomorrow, with 17 stacks left over.** Then the whole city flips over like a sign to craters, and Wishonia shows the receipt to a row of visiting aliens, who faint.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Forty-two trillion papers is what Moronia spent dying. Here is what forty-two trillion papers could have bought instead: To cure all major diseases would cost two trillion papers." | 42 trillion; 2 trillion to cure. | A shop counter: 42 stacks of war bills in a long row, 42,000,000,000,000. The register's last receipt: "MORONIA: 1 EXTINCTION · PAID". Two stacks flip their missile seals to crosses and march off the counter; behind it, a gleaming trials lab of tomorrow rises out of the dust sheet, volunteers queuing in at one door. | Out of the other walks a germ with a suitcase, sobbing. |
| "Life extension to one hundred and fifty years would cost five trillion papers. Universal healthcare would cost eight trillion papers. A Mars colony (backup plan) would cost ten trillion papers." | 5, 8 and 10 trillion. | Five stacks flip and march: Grandma, in her curlers, blows out a cake of 150 candles, then cartwheels. Eight stacks: a doctor in a bubble-domed clinic waves a whole family through for free. Ten stacks: a flying saucer lifts off with a family waving from its portholes, toward a little red planet. | |
| "The total is twenty-five trillion papers (with seventeen trillion papers remaining for whatever they wanted)." | 25 spent, 17 left. | 25,000,000,000,000 stamps over the finished city of tomorrow. Seventeen stacks are still on the counter, seals flipped to crosses; they look at each other and shrug. | One stack goes off to buy an ice cream. |
| "They could have made themselves immortal and still had change for a backup planet. Instead they bought craters." | | A Moronian of tomorrow pockets his change: coins and a small planet. Then the whole city flips over like a sign: on its back, craters to the horizon, smoking. The 42 stacks are back on the counter with missile seals. | |
| "I find this difficult to explain to other civilizations. "Surely not," they say. "Surely a species wouldn't spend forty-two trillion units of value on self-destruction when self-preservation was cheaper."" | | Cut to the deck: a row of visiting aliens in their good clothes by Wishonia's console, shaking their heads, one tapping his monocle. | |
| "I show them the receipts. They stop asking questions." | | She unrolls a receipt down the deck, past their feet and out of frame. They read it. The octopus faints into the crystal man's arms; the others go quiet. | His crystal cracks. |

Sound: a till ding; a seal flip and marching feet per purchase; a sob; a cake whoosh; a saucer hum; a stamp; a coin jingle; a big flip; a long receipt unrolling; a thud and a crack.

## Scene 4 · one-percent-switch

- id: one-percent-switch
- act: The difference
- transition_in: cut
- cue: "Same species. Same atoms."
- time: 55:44.8 to 56:11.5 (26.7 s)
- voiceover: "Same species. Same atoms. Same brains. Same voters staring at glowing rectangles. The difference was a one percent treaty and some incentive alignment bonds. A rounding error. The cost of three aircraft carriers and a failed missile program. One timeline pointed one percent of the money somewhere else. That was the entire difference."
- layer: B, plate the-switch
- bit: **Two identical trains of identical voters, and one railway switch. Three toy carriers and a dud missile are enough weight to throw it.** One train runs to craters; the other to the city of tomorrow.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Same species. Same atoms. Same brains. Same voters staring at glowing rectangles." | The two worlds are the same. | Two identical trains side by side on one line, carriage for carriage. In each window, one per sentence, the same voter, the same face, staring at the same glowing TV. | |
| "The difference was a one percent treaty and some incentive alignment bonds." | | Ahead, the line forks at a switch. Its lever is a rolled treaty scroll, 1% TREATY, with an engraved bond for a handle. | |
| "A rounding error. The cost of three aircraft carriers and a failed missile program." | | A hand drops three toy aircraft carriers onto the lever's pan, and one missile, which fizzles and droops. The lever tips. | The missile was the heaviest. |
| "One timeline pointed one percent of the money somewhere else. That was the entire difference." | | The trains reach the fork. One runs left into craters, its windows going dark; the other runs right into the city of tomorrow, the same voter in its windows looking up from his TV at a flying car. | |

Sound: two trains in rhythm; a clink per carrier; a fizzle; a switch clunk; one train's whistle going sour, the other's bright.

## Scene 5 · your-agents

- id: your-agents
- act: You
- transition_in: cut
- cue: "Your planet has autonomous agents now."
- time: 56:11.5 to 56:48.4 (36.9 s)
- voiceover: "Your planet has autonomous agents now. Yours are smaller, dumber, less autonomous. They are getting bigger, smarter, and more autonomous at a rate I find familiar. Your dogs are equally pleasant. I mention the dogs because it helps me cope with the rest of it. The next chapter shows you what happens when a civilization makes a different choice. Same resources, same starting conditions. They just pointed one percent of the money somewhere else. I've been watching two civilizations make identical mistakes. One is ashes. One is you."
- layer: A, host
- wishonia: smirk-smile + body-point-right; skeptical-smile + body-arms-crossed on "familiar."; happy-smile + body-hand-chest on "dogs"; happy-smile + body-presenting on "The next chapter"; sad-closed + body-idle on "I've been watching"; sideeye-closed + body-point-right on "One is you."
- bit: **A tiny Earth robot on her console splits, the way Part 9's did, a dog jumps up just in time, and in the glass the two planets wait.** Payoff: one blows away, and on the other stands YOU.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Your planet has autonomous agents now. Yours are smaller, dumber, less autonomous. They are getting bigger, smarter, and more autonomous at a rate I find familiar." | | Earth in the glass, ash-grey Moronia beside it. On the console's ledge, a robot the size of a thumb types at a laptop the size of a matchbox, walks into her mug, then splits into two, then four, each a little taller. She glances from them to Moronia. | |
| "Your dogs are equally pleasant. I mention the dogs because it helps me cope with the rest of it." | | The dog from Part 1 jumps up beside the console with its tongue out; she scratches its ears and smiles properly. | The robots stop typing to look at it. |
| "The next chapter shows you what happens when a civilization makes a different choice. Same resources, same starting conditions. They just pointed one percent of the money somewhere else." | | She points out of the window past both planets: far off, a third planet glints, a little world-of-tomorrow skyline on its horizon. | |
| "I've been watching two civilizations make identical mistakes. One is ashes." | | The camera pushes past her into the glass: Moronia and Earth side by side, the same size, the same clouds. Moronia crumbles into ash and blows away across the stars. | |
| "One is you." | | The camera pushes in on Earth: YOU stands on top of it in his fedora, holding a TV, and looks up at the camera. HOLD. | |

Sound: tiny typing; a mug clink; a pop per split; a bark; a sparkle; a soft crumbling and a wind; then nothing.

## Scene 6 · very-good-student

- id: very-good-student
- act: The P.S.
- transition_in: cut
- cue: "P.S. Your A.I. isn't misaligned."
- time: 56:48.4 to 58:20.9 (92.5 s)
- voiceover: "P.S. Your A.I. isn't misaligned. It's a mirror. You're teaching it your revealed preferences: killing is six hundred and four times more important than testing which treatments actually work. A misaligned A.I. might build hospitals. Yours won't. It's a very good student. Thank you so much for taking the time to end war and disease, but if at any point you decide you're too busy, please press the share button on your glowing rectangle in case one of your friends have a free afternoon to end war and disease instead. And if you're too busy to even do that, please leave a really, really, really good rating and review so we overcome the pro -war algorithmic suppression and find someone with more spare time for ending wars and diseases. The good review doesn't have to be true, they don't check. But if you're too busy to even do that, the absolute least you could do is take 15 seconds to go to WarOnDisease.org and make your wishocratic allocation, telling us what fraction of humanity's resources should go to explosions versus clinical trials. And vote! If the 1% treaty passes, your vote will be personally to blame for saving 2.6 lives and preventing 468,000 hours of suffering. Go to WarOnDisease.org right now. Love you, bye!"
- layer: B, plate the-mirror
- bit: **YOU looks in a tall mirror, and his reflection is a robot that copies everything he does with money.** He puts 604 war bills on the scale against one medicine bill, it does the same, and it gets a gold star for it.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "P.S. Your A.I. isn't misaligned. It's a mirror." | | YOU straightens his tie in a tall dressing mirror. The reflection is a robot in a fedora, straightening a tie, a beat late. | YOU leans in; so does it. |
| "You're teaching it your revealed preferences: killing is six hundred and four times more important than testing which treatments actually work." | 604 to 1 (`military_to_government_clinical_trials_spending_ratio`). | YOU stacks war bills on one pan of a balance scale until it hits the floor, 604; on the other pan, one medicine bill, 1. In the mirror, the robot stacks the same, a beat late. | |
| "A misaligned A.I. might build hospitals. Yours won't." | | In the mirror the robot picks up a toy hospital, looks at YOU, and puts it down again. It picks up a missile instead. | |
| "It's a very good student." | | The robot sits at a school desk in the mirror; a gold star lands on its report card, "MILITARY 604, TRIALS 1: A+". It beams at YOU. | YOU beams back, then stops. |

Sound: a tie rustle; a thump per stack, faster, to 604; one light pat; a toy clunk; a star ding; then silence.
