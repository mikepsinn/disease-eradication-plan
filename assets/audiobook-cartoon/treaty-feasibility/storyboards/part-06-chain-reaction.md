---
format: 1920x1080
duration: 3:06.4
message: "90% of humans throw the idea out, but 2,980 billionaires and heads of state each have a small chance of finding it every year, so about 14.5 of them are expected to take it up within ten years."
arc: The idea goes into ten heads, and in nine the white cells tape it up and throw it out → the grid of 2,980 top hats and crowns, and the ways the idea finds them, penicillin-style → Wishonia's Calculator does the four sums, gets 100% and checks itself → the goalie in front of the grid stops nine shots in ten and 14.5 go in → three ways the Economist keeps the count low
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 6, "The Chain Reaction Model"
audio: treaty-feasibility.858ed1cd.mp3, 16:22.3 to 19:28.7
version: v2
---

# Part 6 storyboard: "The Chain Reaction Model"

- **Source:** `knowledge/appendix/treaty-feasibility.qmd` as narrated: "The Chain Reaction Model: Why This Idea Cannot Stay Contained", "Direct Encounters" and "The Mathematics".
- **The numbers** (the narrator's, from an earlier model run; where `_variables.yml` now differs, its value is given and the narrator's is used on screen):
  - `chain_dismiss_probability`: 90% dismiss it (so `chain_engage_probability` 10% engage).
  - `chain_implementer_count`: narrated 2,980 (`_variables.yml` now 2,976) = `chain_global_billionaire_count` narrated 2,780 (now 2,781) + `chain_world_leader_count` 195.
  - Annual chance each one stumbles on the idea: 0.5% (narration; no current parameter). Derived: about 15 of the grid a year.
  - `chain_horizon_years`: narrated 10 years (now 3).
  - `chain_p_encounter_direct_10yr`: narrated 4.89% (now 1.17%). Derived: about 146 of the 2,980.
  - Per implementer, encountering and not dismissing: 4.89% × 10% = 0.489% (derived).
  - `chain_expected_engaged_implementers`: narrated 14.5 (now 3.48).
  - `chain_p_at_least_one_engages`: narrated 100% (now 96.9%).
  - Personal recommendations convert about 3 times better (narration, not a parameter).
- **What the viewer must leave with:** most people dismiss the idea, but so many powerful people can stumble on it that about 14 or 15 of them are expected to take it up within ten years.
- **Plates:**
  - `ten-heads`: ten citizens in a row on a plain field, their heads cut away like an anatomy plate.
  - `the-grid`: a pictogram of 2,980 tiny top hats and crowns on aged paper, a fence round it, and a football goal in front of it.
  - Host (the-sums): Wishonia at her console on the observation deck, the Calculator on the ledge.
- **Cast:** existing: `orderly` (the brain's white cells, tiny; the goalkeeper), `bill-war`, `bill-med`, `tape`, `desk-mug`, `fat-cat` and `fat-cat-catch` (tiny, the grid), `politician` (tiny, with a sash, for heads of state), `google-phone`, `lobbyist` (the advisor who whispers), `manual`, `calculator` (host prop), `doctor` (the W.H.O. official), `matron` (the foundation head), `auditor` (the fund manager), `rope`, `pdf` (the newspapers), `tarp`. New: `cutaway-head`, `alexander-fleming`, `football-goal`. Shared: `citizen` (Part 3), `economist` (Part 1).
- **Callbacks:**
  - Episode 1, Part 4: the orderlies and the SANE / INSANE game show; here the brain's white cells are orderlies.
  - Episode 1, Part 5: the grid of 2,800 tiny fat cats, now 2,780 of them plus 195 heads of state.
  - Episode 1, Part 16: the Calculator, who screams at big numbers; here it checks its own display.
  - Set up for Part 7: the 14.5 engaged (fourteen tiny fat cats and half of one).
- **New art:**
  - a cutaway skull piece that fits any `citizen`'s head, the brain inside like an anatomy plate
  - Alexander Fleming, caricatured, lifting the lid of a mouldy petri dish
  - a football goal with a net, a 1950s leather football, and a goalkeeper's cap for the `orderly`
- **Kit additions:**
  - `pass-through`: a cut-out that travels in one ear and out the other of a cutaway head.
  - `grid-light`: a pictogram grid where a counted number light up per beat (as `pictogram` in Part 3, with two cut-out types).

## Scene 1 · cognitive-immune-system

- id: cognitive-immune-system
- act: The immune system
- transition_in: cut
- cue: "The Chain Reaction Model"
- time: 16:22.3 to 16:54.5 (32.2 s)
- voiceover: "The Chain Reaction Model: Why This Idea Cannot Stay Contained. Your species has a cognitive immune system. When someone suggests redirecting one percent of murder money to medicine money, approximately ninety percent of humans will dismiss it without engaging. This is the institutionalization rate: the probability that a human's brain classifies "stop funding murder" as crazier than "continue funding murder." On Earth, this is called "being realistic.""
- layer: B, plate ten-heads
- bit: **The idea is a war bill whose seal flips to a cross. It walks into ten heads; in nine of them white cells in orderlies' scrubs tape it up and throw it out the other ear.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Chain Reaction Model: Why This Idea Cannot Stay Contained. Your species has a cognitive immune system. When someone suggests redirecting one percent of murder money to medicine money," | Brains reject the idea. | Close on one cutaway head: inside the skull, tiny white cells in orderlies' scrubs patrol the brain. A war bill walks up to the ear; its missile seal flips to a cross; it steps inside. | |
| "approximately ninety percent of humans will dismiss it without engaging." | 90% throw it out. | The white cells swarm it, tape its arms to its sides and pitch it out of the other ear. Pull back: ten heads in a row; the bill goes through nine of them the same way. In the tenth it sits down and is handed a mug of tea. "90%" stamps over the nine. | |
| "This is the institutionalization rate: the probability that a human's brain classifies "stop funding murder" as crazier than "continue funding murder."" | They file it as crazy. | Inside one head, a white cell stamps two cards: "STOP FUNDING MURDER", CRAZY; "CONTINUE FUNDING MURDER", SANE. | |
| "On Earth, this is called "being realistic."" | | The nine pat themselves on the head, pleased. | |

Sound: a siren-like whistle from the cells; a struggle and a boing out of each ear, nine times; a mug's clink; two stamps; nine contented pats.

## Scene 2 · the-grid

- id: the-grid
- act: Direct encounters
- transition_in: cut
- cue: "The question is whether a ninety percent"
- time: 16:54.5 to 17:50.0 (55.6 s)
- voiceover: "The question is whether a ninety percent dismissal rate prevents the idea from reaching someone who can act on it. This section answers whether reaching such people is overwhelmingly likely. (The next section addresses what happens once they understand the incentive structure.) Direct Encounters. On your planet, important humans find ideas through news, conferences, advisors whispering in their ears, or occasionally by accident while searching for something else (this is how most of your scientific breakthroughs happen, and also how you discovered penicillin). Each of two thousand nine hundred and eighty potential implementers (two thousand seven hundred and eighty billionaires plus one hundred and ninety-five heads of state) has an annual probability zero point five percent of stumbling across this idea. That is a very small number per person. But there are a lot of persons."
- layer: B, plate the-grid
- bit: **The camera finds three of the grid's people finding the idea, one way each, then pulls back to all 2,980 of them.** The last finds it in his own top hat, next to Fleming finding penicillin.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The question is whether a ninety percent dismissal rate prevents the idea from reaching someone who can act on it. This section answers whether reaching such people is overwhelmingly likely. (The next section addresses what happens once they understand the incentive structure.)" | The question: does it reach anyone who can act? | Close on one tiny fat cat in his square of the grid. The bill from scene 1, still taped up, wriggles free and floats overhead. | |
| "Direct Encounters. On your planet, important humans find ideas through news, conferences, advisors whispering in their ears," | The usual ways. | The camera hops from square to square: one fat cat reads the news on his glowing rectangle; one has an advisor whispering into his ear. | |
| "or occasionally by accident while searching for something else (this is how most of your scientific breakthroughs happen, and also how you discovered penicillin)." | And by accident. | One fat cat takes off his top hat looking for his cufflink and finds the manual in it. In the next square, Alexander Fleming lifts the lid of a mouldy petri dish and finds penicillin. They look at each other. | |
| "Each of two thousand nine hundred and eighty potential implementers (two thousand seven hundred and eighty billionaires plus one hundred and ninety-five heads of state) has an annual probability zero point five percent of stumbling across this idea." | 2,980: 2,780 billionaires and 195 heads of state; 0.5% a year each. | The camera pulls back fast: the whole grid, top hats and, at one end, a block of heads of state in sashes. "2,780", "195", "2,980". The medicine bill drifts over it; each year about 15 squares light up where it passes, "0.5% A YEAR". | |
| "That is a very small number per person. But there are a lot of persons." | Many people. | The camera pulls back further; the grid fills the frame edge to edge, and the lit squares twinkle across it. | |

Sound: a phone ping; a whisper; a hat's pop and a gasp, twice; a whoosh as the camera pulls back; a soft ping per lit square.

## Scene 3 · the-sums

- id: the-sums
- act: The math
- transition_in: cut
- cue: "The Mathematics"
- time: 17:50.0 to 18:12.4 (22.4 s)
- voiceover: "The Mathematics. The probability that a given implementer encounters the idea within ten years: The per-implementer probability of engaging (encountering AND not dismissing): The expected number of implementers who engage: The probability that at least one engages: one hundred percent. That is not a typo."
- layer: A, host
- wishonia: neutral-smile + body-presenting; happy-smile + body-point-right on "one hundred percent."; sideeye-closed + body-arms-crossed on "typo."
- bit: Wishonia's Calculator does four sums, gets 100%, and can't believe it.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Mathematics. The probability that a given implementer encounters the idea within ten years:" | 4.89% in ten years. | Wishonia at her console. The Calculator on the ledge chews its tape and prints line 1 on the glass: "MEETS THE IDEA IN 10 YEARS: 4.89%". | |
| "The per-implementer probability of engaging (encountering AND not dismissing): The expected number of implementers who engage:" | 0.489%; 14.5. | Line 2: "MEETS IT AND DOESN'T THROW IT OUT: 0.489%". Line 3: "EXPECTED TO TAKE IT UP: 14.5". | |
| "The probability that at least one engages: one hundred percent." | 100%. | Line 4: "AT LEAST ONE: 100%". The Calculator's display reads 100. | |
| "That is not a typo." | | It rubs its eyes, shakes itself so its keys rattle, and looks again: 100. It bangs its own side. Still 100. Wishonia folds her arms. | |

Sound: a tape chatter per line; a rattle of keys; a bang and a little "ow".

## Scene 4 · shots-on-goal

- id: shots-on-goal
- act: The math
- transition_in: cut
- cue: "With two thousand nine hundred and eighty"
- time: 18:12.4 to 18:41.1 (28.7 s)
- voiceover: "With two thousand nine hundred and eighty potential implementers and a four point eight nine percent per-implementer encounter probability over ten years, the model expects approximately fourteen point five implementers to engage with this idea. Not guaranteed in the mathematical sense. But in planning terms, this is the kind of number you treat as near-inevitable unless your diffusion assumptions are wrong. The dismissal rate stops mattering once enough shots are on goal."
- layer: B, plate the-grid
- bit: **A white cell from scene 1 keeps goal in front of the grid and saves nine shots in ten, but 146 shots come at it, and 14 and a half go in.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "With two thousand nine hundred and eighty potential implementers and a four point eight nine percent per-implementer encounter probability over ten years," | 146 of 2,980 meet it. | A football goal in front of the grid. A white cell in a goalkeeper's cap and its scrubs bounces on its toes. From the grid, 146 of the squares (4.89%) step forward, each with a ball. | |
| "the model expects approximately fourteen point five implementers to engage with this idea." | About 14.5 take it up. | They shoot, one after another. The cell saves nine in ten, diving left and right; the net bulges at every tenth shot. The tally: "14.5". The last ball goes in halfway and stops on the line. | Half a goal. |
| "Not guaranteed in the mathematical sense. But in planning terms, this is the kind of number you treat as near-inevitable unless your diffusion assumptions are wrong." | Not certain, but plan on it. | The cell stands up, mud-covered, and squints at the tally. | |
| "The dismissal rate stops mattering once enough shots are on goal." | Enough shots and some go in. | Another ball goes in behind it. It collapses flat on its back, cap over its face. | |

Sound: a whistle; thuds of kicks in a rising rhythm; a dive and a whump per save; a net's swish on each goal; a crowd's "ooh" for the half ball; a long exhausted sigh.

## Scene 5 · three-ways-conservative

- id: three-ways-conservative
- act: The math
- transition_in: same plate (the camera rises over the goal to the grid)
- cue: "This model answers only"
- time: 18:41.1 to 19:28.7 (47.6 s)
- voiceover: "This model answers only: "Is it overwhelmingly likely to reach someone who matters?" The answer is yes. The next section asks: "What happens once it does?" This model is deliberately conservative in three ways: Base engagement rate: Uses the same engagement rate for personal recommendations as for passive exposure (personal recommendations convert at approximately three times higher rates). Narrow implementer definition: Counts only billionaires and heads of state (excludes foundation heads, W.H.O. officials, major fund managers, et cetera). No compounding: Ignores the feedback loop where media coverage of early adoption increases subsequent encounter rates, and ignores network amplification (people sharing the idea with others)."
- layer: B, plate the-grid
- bit: **The Economist keeps the count low on purpose, three ways:** he turns a whisper's triple glow down to one, keeps three eager outsiders behind a rope, and holds a tarp over the grid so the newspapers can't land.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "This model answers only: "Is it overwhelmingly likely to reach someone who matters?" The answer is yes. The next section asks: "What happens once it does?"" | It reaches them. | The grid, the 14.5 lit squares glowing. A big tick drops over it. | |
| "This model is deliberately conservative in three ways: Base engagement rate: Uses the same engagement rate for personal recommendations as for passive exposure (personal recommendations convert at approximately three times higher rates)." | 1: recommendations count once, not 3 times. | The Economist walks onto the grid. A friend whispers to one fat cat, who lights up three times as bright; the Economist reaches over and turns him down to normal with a knob on his back. | |
| "Narrow implementer definition: Counts only billionaires and heads of state (excludes foundation heads, W.H.O. officials, major fund managers, et cetera)." | 2: only billionaires and heads of state count. | At the grid's fence, a rope: a foundation head, a W.H.O. official in a white coat and a fund manager trailing ticker tape wave the manual from outside it. The Economist unhooks the rope, looks at them, and hooks it back. | |
| "No compounding: Ignores the feedback loop where media coverage of early adoption increases subsequent encounter rates, and ignores network amplification (people sharing the idea with others)." | 3: no news coverage, no sharing. | Newspapers rain down over the grid, "BILLIONAIRE FUNDS TREATY", and the lit squares start passing the manual to their neighbours. The Economist stretches a tarp over the grid; the papers bounce off it, and he slaps the passing hands apart. | |

Sound: a tick; a whisper and a triple ping turned down to one; a rope hook's click, twice; a patter of newspapers on canvas; two slaps.
