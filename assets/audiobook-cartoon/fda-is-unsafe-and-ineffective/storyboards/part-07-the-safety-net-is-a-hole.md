---
format: 1920x1080
duration: 1:57.0
message: "Approving a bad drug ends a regulator's career and delaying a good one gets him promoted, so the system delays, and its safety net catches one person for every 3,070 it drops."
arc: The FDA climbs its decision tree: the approve branch is sawn off into a hearing, the delay branch has a hammock and a slide to a pharma tower → the TV says its name, so it stamps DELAYED on everything, and the complaints box stays empty → Henry Miller on a mountain of binders at the tree's foot, the building in its hammock shaking its head, and the patients waiting below → Wishonia holds a microphone to a skeleton → the DALY bars, a sliver and a tower → the net that catches one bubble-wrapped man and drops 3,070 → Wishonia's net that is just a hoop
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 7, "The Safety Net Is a Hole"
audio: fda-is-unsafe-and-ineffective.5d00ae46.mp3, 16:39.1 to 18:36.1
version: v2
---

# Part 7 storyboard: "The Safety Net Is a Hole"

- **Source:** `knowledge/problem/fda-is-unsafe-and-ineffective.qmd`, sections "How the Incentives Work" and "The Math: Why Current Regulations Increase Total Harm"; `knowledge/appendix/invisible-graveyard.qmd` for the ratio.
- **The numbers:**
  - `type_i_error_benefit_dalys`: 2.59 million DALYs prevented, crediting every drug withdrawal to the 1962 rules.
  - Delay harm: the narrator says 7.94 billion DALYs; `dfda_efficacy_lag_elimination_dalys` now holds 8.77 billion. On screen, 7.94 billion.
  - `type_ii_error_cost_ratio`: the narrator says 3,070 (7.94 billion ÷ 2.59 million = 3,066); `_variables.yml` now holds 3,389. On screen, 3,070.
  - Drawn to scale: if the 2.59 million bar is 1 px, the 7.94 billion bar is 3,070 px, nearly three frames tall.
  - Henry I. Miller and recombinant human insulin (early 1980s) are cited, not parameters.
- **What the viewer must leave with:** the person deciding is punished only for approving, never for delaying, so delay is the safe career move, and the delay harms 3,070 times more than the approvals it prevents.
- **Plates:**
  - `decision-tree`: one big engraved oak on a plain field with two branches; the Capitol at the foot of the left branch, a pharma tower at the end of a slide from the right one; room at its foot for a mountain of binders.
  - `stamp-line`: a conveyor of pill bottles running past the FDA building, a TV set on one side and a complaints box on the other.
  - `net`: a burning tower on a plain field (only its top window) and a circus safety net below it; beside it a two-bar chart, "HARM, IN HEALTHY YEARS".
  - Host scenes: Wishonia at her console.
- **Cast:** existing: `fda-sip` / `fda-scared` / `fda-folded`, `capitol`, `tv-set`, `newspaper`, `newspaper-man`, `gold-star`, `pharma-tower` (from Part 4), `pill-bottle`, `conveyor`, `skeleton`, `patient`, `patient-skeleton`, `binder`, `bubble-man`, `hoop`, `magnifier`, `thought-bubble`, `cloud`. New: `decision-tree` (the oak, its left branch that can be sawn off, a saw, a hammock on the right branch, a playground slide), `suggestion-box` (a wooden box on a post with a slot and no bottom; here "COMPLAINTS" in code, in Part 11 "F.A.E.R.S."; kneeling, praying), `henry-miller` (Dr. Henry I. Miller, caricatured, holding an insulin vial), `safety-net` (a circus net held taut by four FDA-building arms, mostly hole). The microphone is a host prop.
- **Callbacks:** Part 1's bubble-wrapped man and the balance; episode 1 Part 12's 3,389 column, beaten here by a net that is mostly hole.
- **New art:** every new cut-out in the cast.
- **Kit additions:**
  - A saw-off: a branch hinges down from its cut and drops.

## Scene 1 · decision-tree

- id: decision-tree
- act: The incentives
- transition_in: cut; the heading card comes up from black
- cue: "How the Incentives Work"
- time: 16:39.1 to 17:04.4 (25.3 s)
- voiceover: "How the Incentives Work. F.D.A. Regulator Decision Tree. Approve drug that later shows problems. Congressional hearing (televised). "F.D.A. APPROVED KILLER DRUG" headlines. Career ends. Pension threatened. Delay drug that could save lives. Nothing happens. Nobody writes a headline. Promotion on schedule. Retire to pharma job."
- layer: B, plate decision-tree
- bit: **The decision tree is a real tree, and the FDA building climbs it.** The left branch is sawn off under it into a televised hearing; the right branch holds a hammock and ends in a slide to a pharma tower.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "How the Incentives Work. F.D.A. Regulator Decision Tree." | | The heading card, then a big engraved oak; the FDA building shins up the trunk to the fork. | |
| "Approve drug that later shows problems. Congressional hearing (televised). "F.D.A. APPROVED KILLER DRUG" headlines. Career ends. Pension threatened." | Approving ends a career. | It edges out along the left branch, "APPROVE". The Capitol below, a TV camera beside it, saws the branch off. The building drops into a hearing chair under hot lights; newspapers fly at it, one headline after another, and "CAREER ENDS" stamps across it. | |
| "Delay drug that could save lives. Nothing happens. Nobody writes a headline." | Delaying costs nothing. | Rewind: the building is back at the fork, unhurt, and edges out along the right branch, "DELAY", and lies down in a hammock with its coffee. A newsboy walks underneath with a blank front page. | |
| "Promotion on schedule. Retire to pharma job." | Delaying is rewarded. | A gold star drops on its frieze. It gets up, sits on a playground slide at the end of the branch and whooshes down into a pharma tower's open door, which closes with a smile. | |

Sound: climbing scuffs; a saw; a crash and a camera flash; newspaper flaps; a stamp; a creak of the hammock; a ding for the star; a slide whoosh and a door thunk.

## Scene 2 · delay-everything

- id: delay-everything
- act: The incentives
- transition_in: cut
- cue: "To be fair, this isn't a conspiracy"
- time: 17:04.4 to 17:30.1 (25.7 s)
- voiceover: "To be fair, this isn't a conspiracy. It's just a system where the only career-ending move is letting patients access treatments. If you approve a bad drug, C.N.N. says your name. If you delay a good drug, nobody dies on television. So the rational move is to delay everything, and that's what happens, and everyone who could object is dead, which does simplify the feedback process."
- layer: B, plate stamp-line
- bit: **One TV that says its name, so it stamps DELAYED on everything; the complaints box waits for the dead.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "To be fair, this isn't a conspiracy. It's just a system where the only career-ending move is letting patients access treatments. If you approve a bad drug, C.N.N. says your name." | No plot, just rules. | The FDA building at the end of a conveyor of smiling bottles, a stamp in each hand, a TV set beside it. It stamps one "APPROVED"; on the TV a CNN anchor turns and points straight out of the screen at it: "F.D.A.!". It leaps in terror. | |
| "If you delay a good drug, nobody dies on television." | | It stamps the next "DELAYED"; the TV shows a test pattern. It relaxes. | |
| "So the rational move is to delay everything, and that's what happens," | It delays all of them. | It stamps "DELAYED" on every bottle, faster and faster, both hands, a blur; the bottles pile up off the end of the belt. | |
| "and everyone who could object is dead, which does simplify the feedback process." | The harmed can't complain. | On the other side, a complaints box on a post. A line of skeletons shuffles up to it; each tries to post a slip and its arm falls off. The box stays empty. | The building pats the empty box. |

Sound: a conveyor hum; a stamp and a TV blare; a stamp and a test-pattern tone; a stamp machine-gun; a clatter of bones per skeleton; a pat.

## Scene 3 · heads-would-roll

- id: heads-would-roll
- act: The incentives
- transition_in: cut
- cue: "Dr. Henry I. Miller ran the F.D.A. team"
- time: 17:30.1 to 17:49.6 (19.5 s)
- voiceover: "Dr. Henry I. Miller ran the F.D.A. team reviewing recombinant human insulin in the early nineteen eighties. Mountains of evidence showed it was safe and effective. His supervisor refused to approve it. If someone died from the drug, heads would roll. If people died waiting for the drug? Nothing happens."
- layer: B, plate decision-tree
- bit: **Back at the tree: a real mountain of evidence rises to the hammock, and the building in it won't take the insulin; the dying at the foot of the tree go unnoticed.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Dr. Henry I. Miller ran the F.D.A. team reviewing recombinant human insulin in the early nineteen eighties. Mountains of evidence showed it was safe and effective." | | Dr. Henry I. Miller, caricatured by name, holds up an insulin vial: "RECOMBINANT HUMAN INSULIN · 1980s". Binders pile up under him, lifting him on a mountain of evidence until he is level with the hammock: "SAFE ✓ EFFECTIVE ✓". | |
| "His supervisor refused to approve it." | | The FDA building in its hammock shakes its frieze, no. | |
| "If someone died from the drug, heads would roll." | Approving risks heads. | In a thought bubble over the building: the APPROVE branch, sawn off, and its own pediment rolling off down the trunk. It clutches its roof. | |
| "If people died waiting for the drug? Nothing happens." | Waiting risks nothing. | The bubble pops. At the foot of the tree a line of diabetic patients waits, holding empty syringes; they x-ray to skeletons one by one. The building sips. | Miller, on top, is still holding the vial up. |

Sound: a ding; binder thumps rising in pitch; a saw and a rolling rumble; a pop; x-ray zaps; a sip.

## Scene 4 · testimony

- id: testimony
- act: The incentives
- transition_in: cut
- cue: "Dead patients don't testify before Congress"
- time: 17:49.6 to 17:53.9 (4.3 s)
- voiceover: "Dead patients don't testify before Congress. I checked."
- layer: A, host
- wishonia: neutral-smile + body-presenting; skeptical-closed + body-hands-hips on "I checked."
- bit: She checked, literally.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Dead patients don't testify before Congress." | | Beside her console, one of the skeletons from the foot of the tree sits at a little hearing table with a 1950s microphone and a glass of water. | |
| "I checked." | | She taps the microphone: thump thump. She holds it closer. The skeleton's jaw falls off onto the table. | She puts the jaw back and tries again. |

Sound: two mic thumps; a clack as the jaw drops.

## Scene 5 · hole-not-a-net

- id: hole-not-a-net
- act: The math
- transition_in: cut
- cue: "The Math: Why Current Regulations"
- time: 17:53.9 to 18:32.3 (38.4 s)
- voiceover: "The Math: Why Current Regulations Increase Total Harm. Even generously crediting ALL drug withdrawals to the nineteen sixty-two changes (ignoring that Phase One safety testing already existed), the prevented harm totals approximately two point five nine million disability-adjusted life years, or D.A.L.Y.s. The delay harm totals seven point nine four billion D.A.L.Y.s. For every one unit of harm prevented, the current system creates three thousand and seventy units of harm through delay. The safety net catches one person and drops three thousand and seventy."
- layer: B, plate net
- bit: **A sliver and a tower, then the narrator's net, held up by the FDA: it catches one bubble-wrapped man and the rest pour through the hole.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Math: Why Current Regulations Increase Total Harm. Even generously crediting ALL drug withdrawals to the nineteen sixty-two changes (ignoring that Phase One safety testing already existed), the prevented harm totals approximately two point five nine million disability-adjusted life years, or D.A.L.Y.s." | 2.59 million prevented, generously. | The heading card, then a two-bar chart, "HARM, IN HEALTHY YEARS": "PREVENTED · 2.59 MILLION", a bar one hair tall. A magnifying glass finds it. | |
| "The delay harm totals seven point nine four billion D.A.L.Y.s." | 7.94 billion caused. | "CAUSED BY DELAY · 7.94 BILLION": its bar shoots up, and the camera tilts up after it for three frames. | |
| "For every one unit of harm prevented, the current system creates three thousand and seventy units of harm through delay." | 3,070 to 1. | At the top of the tower, "3,070 : 1" stamps into the sky. | |
| "The safety net catches one person and drops three thousand and seventy." | It catches one and drops 3,070. | Back down: four FDA-building arms hold a circus safety net under a burning window. One bubble-wrapped man drops and bounces in the net, thumb up. Then people pour out of the window, and every one goes straight through the middle of the net, which is one big hole, and lands below as a grinning skeleton on a growing heap. A counter by it runs to "3,070". | The bubble-wrapped man bounces higher and higher on the rim. |

Sound: a magnifier squeak; a rising whistle and a stamp; a boing; a long whoosh of falling people and a rattle of bones; a counter whirring to a stop.

## Scene 6 · just-a-hoop

- id: just-a-hoop
- act: The math
- transition_in: cut
- cue: "On Wishonia, we'd call that a hole"
- time: 18:32.3 to 18:36.1 (3.8 s)
- voiceover: "On Wishonia, we'd call that a hole, not a net."
- layer: A, host
- wishonia: smirk-smile + body-presenting; sideeye-closed + body-idle on "net."
- bit: The net, held up to the light, is a hoop.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "On Wishonia, we'd call that a hole, not a net." | It is a hole. | Wishonia holds up a hoop with one string across it, and looks at the camera through it. | Outside the window the bubble-wrapped man bounces past, up, and out of sight. |

Sound: a boing outside.
