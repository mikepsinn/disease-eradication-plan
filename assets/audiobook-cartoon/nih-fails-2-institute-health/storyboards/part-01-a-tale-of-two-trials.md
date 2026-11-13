---
format: 1920x1080
duration: 5:14.2
message: "During COVID, Oxford gave 48,000 patients the drugs for $500 each and saved a million lives; the N.I.H. got $1.665 billion for long COVID, watched its patients, and completed zero trials."
arc: Title card (the N.I.H. puts HEALTH in a specimen jar) → Wishonia opens the case file → the scoreboard, 1,000,000 against 0 → one long hospital ward split down the middle by a chalk line → left, the Oxford college gives each bed a pill and the patients get up and walk out → right, the N.I.H. building watches its beds through opera glasses, takes roll call over the dead, and buries the sick under their own paperwork → the scoreboard again, and the waiting room grows beards
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 1, "A Tale of Two Trials"
audio: nih-fails-2-institute-health.dc5afcd8.mp3, 00:00.0 to 05:14.2
version: v1
---

# Part 1 storyboard: "A Tale of Two Trials"

- **Source:** `knowledge/problem/nih-fails-2-institute-health.qmd`, the description, "A Tale of Two Trials", "RECOVERY Trial (UK Approach)" and "RECOVER Initiative (NIH Approach)". The narration script is `nih-fails-2-institute-health.prepared.txt`, from the chapter title to "a system that tests patience."
- **The numbers:**
  - `nih_clinical_trials_spending_pct`: 3.3% of the N.I.H. budget on trials.
  - `recovery_trial_cost_per_patient`: $500 per patient.
  - `recovery_trial_total_cost`: $20 million (the narrator: "twenty million dollars over six months").
  - `recovery_trial_global_lives_saved`: 1 million lives.
  - "One hundred days" to the first result (the narrator; the parameter `oxford_recovery_trial_duration_months` is 3 months).
  - RECOVERY enrolled 48,000 patients; dexamethasone, on sale since 1957, cut COVID deaths by one third (cited, not parameters).
  - RECOVER: "nearly six hundred" candidate treatments; $1.665 billion received (the summary line rounds it to "one point six billion"); 5,500 patients per trial at $500 is $2.75 million a trial, so $1.665 billion buys about 600 trials; zero completed in four years; 15% of the budget to trials; 11% of patients in interventional trials, 89% observational; $504,500 per interventional patient (all cited, not parameters).
- **What the viewer must leave with:** Oxford tested drugs on patients for $500 each and saved a million lives in a hundred days; the N.I.H. spent $1.665 billion watching patients and completed zero trials.
- **Plates:**
  - `the-score`: a ballpark scoreboard on a plain field, two rows, OXFORD and N.I.H.
  - `two-wards`: one long hospital ward on aged paper, a chalk line down the middle, U.K. on the left and U.S. on the right, a row of iron beds going off to the horizon on each side. The Oxford college stands at the head of the left row, the N.I.H. building at the head of the right. The camera travels down one side, then the other.
  - Host: Wishonia at her console on the observation deck, Earth in the glass.
- **Cast:** existing: `patient`, `patient-skeleton`, `hospital-bed`, `pill-bottle`, `scoreboard`, `zero`, `specimen-jar`, `germ` (the spiky virus), `calendar`, `money-bundle`, `bill-med`, `house`, `price-tag`, `committee`, `shelf`, `scientist`, `wastebasket`, `cobweb`, `beard`, `skeleton`, `sheets` (the paper that buries the beds), `rope` (the velvet rope). Shared with other chapters' new art (not yet in ART.md): `nih-building` (with `nih-read`, `nih-stamp`), `oxford-college`. New: `nih-watch`, `david-putrino`.
- **Callbacks:** none from episode 1. Set up for this chapter: the two-wards plate comes back in Part 11 ("The RECOVERY trial already proved it"); the N.I.H.'s opera glasses (in `nih-watch`'s hand) are how it observes all chapter; the dexamethasone bottle that waves comes back in Part 11 ("It's waving at you").
- **New art:**
  - `nih-watch`: the N.I.H. building (a columned marble palace with a face in its pediment and pince-nez, N.I.H. on its frieze, stick arms in white gloves) holding a pair of opera glasses to its window eyes, a clipboard under one arm.
  - `david-putrino`: David Putrino of Mount Sinai, caricatured, in a 1950s suit.
  - The `two-wards` plate.
- **Kit additions:**
  - `chart`: a pie with a lit wedge, and a counter that runs up.
  - `row`: copies of a cut-out along a line to the horizon (the beds), each one changeable on its own (a patient sits up, a patient becomes a skeleton).

## Scene 1 · nih-fails-title

- id: nih-fails-title
- act: Title
- transition_in: up from black (the head of a reel)
- cue: "N.I.H. Fails to Institute Health"
- time: 00:00.0 to 01:43.5 (103.5 s)
- voiceover: "You're here. Your organs are failing. And your death is drawing near. But if you bribe the right politicians in the right order at the right time, you can trade the nuclear warheads for medicine. And it's not even a crime. N.I.H. Fails to Institute Health"
- layer: A, title card
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "N.I.H. Fails to Institute Health" | The heading. | The period card comes up from black: N.I.H. FAILS TO INSTITUTE HEALTH. A white-gloved hand reaches in from the edge of the card, lifts the word HEALTH off it, turns it over, and drops it into a specimen jar. The lid screws shut. A tag swings on the jar: UNDER STUDY. | The card now reads N.I.H. FAILS TO INSTITUTE, and the jar sits where HEALTH was. |

Sound: a projector whirr; a cork squeak as the lid turns; a tiny clink.

## Scene 2 · host-root-cause

- id: host-root-cause
- act: The summary
- transition_in: iris in on her face
- cue: "A root cause failure analysis"
- time: 01:43.5 to 01:59.6 (16.1 s)
- voiceover: "A root cause failure analysis to show why the world's largest medical research institution only allocates three point three percent of its budget to testing which of the thousands of known-safe treatments actually work in humans."
- layer: A, host
- wishonia: smirk-smile + body-presenting; lookright-smile + body-point-right on "three"; skeptical-smile + body-idle on "humans."
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "A root cause failure analysis to show why the world's largest medical research institution" | | Wishonia opens a fresh case file on the console: N.I.H. | |
| "only allocates three point three percent of its budget to testing" | 3.3% goes to trials. | A pie on her screen, its 3.3% wedge a sliver so thin she has to lean in to point at it. | |
| "which of the thousands of known-safe treatments actually work in humans." | Thousands of safe drugs are untested. | A row of little pill bottles along the console's ledge, every one tagged SAFE, every one waving. | Nobody picks one up. |

Sound: a paper flap as the file opens; a soft click for the wedge; squeaks as the bottles wave.

## Scene 3 · the-score

- id: the-score
- act: The summary
- transition_in: cut
- cue: "Oxford tested COVID treatments"
- time: 01:59.6 to 02:15.9 (16.3 s)
- voiceover: "Oxford tested COVID treatments for five hundred dollars per patient and saved a million lives in one hundred days. The N.I.H. spent one point six billion dollars and completed zero trials in four years."
- layer: B, plate the-score
- bit: **The whole chapter as one scoreboard.** One row fills with a million; the other row's money runs up and its zero falls off the board.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Oxford tested COVID treatments for five hundred dollars per patient" | $500 a patient. | The scoreboard fills the frame. OXFORD's row: COST PER PATIENT clicks to $500. | |
| "and saved a million lives in one hundred days." | 1 million lives, 100 days. | LIVES SAVED spins up to 1,000,000; DAYS reads 100. A firework pops over the row. | |
| "The N.I.H. spent one point six billion dollars" | $1.6 billion spent. | N.I.H.'s row: SPENT spins up and up to $1,600,000,000, the digits crowding to the edge. | |
| "and completed zero trials in four years." | Zero trials. | TRIALS COMPLETED: one big stamped 0 slots into its window. YEARS: 4. | The 0 wobbles, drops out of the board, rolls off across the field, and keeps rolling out of the frame. |

Sound: scoreboard clicks; a pop for the firework; a ratchet as the dollars spin; a clunk and a long rolling rumble for the 0.

## Scene 4 · tale-of-two-trials

- id: tale-of-two-trials
- act: Two trials
- transition_in: cut (a period card, then the plate)
- cue: "A Tale of Two Trials."
- time: 02:15.9 to 03:04.6 (48.7 s)
- voiceover: "A Tale of Two Trials. The difference between efficient and inefficient trial design isn't theoretical. Your species accidentally ran a controlled experiment on itself during COVID. Two countries. Same disease. One spent like it was trying to cure death. The other actually did. RECOVERY Trial (U.K. Approach). The British spent twenty million dollars over six months. Enrolled forty-eight thousand patients. Found multiple effective treatments, including dexamethasone, a steroid that had been available since nineteen fifty-seven. It reduced COVID deaths by one-third and saved over one million lives. Cost per patient: five hundred dollars."
- layer: B, plate two-wards
- bit: **One ward, two halves, the same disease in every bed.** The left half gives the beds medicine; the right half watches them. Over Scenes 4 to 7 the left beds empty as patients walk out, and the right beds fill with paper and skeletons.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "A Tale of Two Trials. The difference between efficient and inefficient trial design isn't theoretical. Your species accidentally ran a controlled experiment on itself during COVID." | COVID was a real experiment. | The period card, A TALE OF TWO TRIALS, wipes off to the ward: wide, the long ward, a chalk line down its middle, U.K. on the left, U.S. on the right. | |
| "Two countries. Same disease. One spent like it was trying to cure death. The other actually did." | One spent big; one got results. | A grinning spiky virus hops onto the pillow of every bed on both sides. The Oxford college walks to the head of the left row with a small strapped bundle of bills; the N.I.H. building walks to the head of the right row towing a bundle the size of a bus, which flattens the chalk line. | The same virus, in the same pose, in every bed. |
| "RECOVERY Trial (U.K. Approach). The British spent twenty million dollars over six months. Enrolled forty-eight thousand patients." | $20 million, six months, 48,000 patients. | The camera travels down the left row under a sign, RECOVERY. A counter at the head of the row runs to 48,000 as beds slide in, row after row, to the horizon. | |
| "Found multiple effective treatments, including dexamethasone, a steroid that had been available since nineteen fifty-seven." | An old, cheap drug worked. | The college pulls a dusty pill bottle off a shelf, cobweb and all, tagged DEXAMETHASONE · 1957, blows the dust off, and pours a pill into each bed's cup down the row. | |
| "It reduced COVID deaths by one-third and saved over one million lives." | Deaths cut by a third; 1 million lives. | Down the whole row, every third patient sits up, gets out of bed and walks out of the ward, still in pyjamas. The counter: 1,000,000 SAVED. | The viruses on their pillows look round, confused, and are left alone in the empty beds. |
| "Cost per patient: five hundred dollars." | $500 each. | A price tag swings from one walker's toe: $500. | |

Sound: a whirr for the card; a pop per virus, fast; a heavy rumble for the bus-sized bundle; a ticking counter; a puff of dust; a pill rattle down the row; a crowd of slippers shuffling out.

## Scene 5 · recover-initiative

- id: recover-initiative
- act: Two trials
- transition_in: same plate (no seam)
- cue: "RECOVER Initiative (N.I.H. Approach)."
- time: 03:04.6 to 03:34.6 (30.0 s)
- voiceover: "RECOVER Initiative (N.I.H. Approach). Nearly six hundred potential treatments for Long COVID have been identified. At RECOVERY trial efficiency (five hundred dollars per patient, five thousand five hundred patients per treatment), one point six six five billion dollars buys six hundred completed trials. The N.I.H. received one point six six five billion dollars. Over four years, they completed zero."
- layer: B, plate two-wards
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "RECOVER Initiative (N.I.H. Approach). Nearly six hundred potential treatments for Long COVID have been identified." | 600 candidates. | The camera crosses the chalk line to the right row. A sign over it: RECOVER. Behind the N.I.H. building, a shelf runs off into the distance: 600 bottles, each tagged LONG COVID? | |
| "At RECOVERY trial efficiency (five hundred dollars per patient, five thousand five hundred patients per treatment), one point six six five billion dollars buys six hundred completed trials." | $1.665 billion is enough for 600 trials. | The bus-sized bundle splits itself into 600 little bundles, and each little bundle hops up beside one bottle. | It fits exactly. |
| "The N.I.H. received one point six six five billion dollars." | | The little bundles hop back together into the bus-sized one and climb in through the N.I.H.'s front door. | |
| "Over four years, they completed zero." | Zero trials. | A calendar on its door tears off four years. The 600 bottles are still on the shelf, untouched, gathering cobwebs. Over the row: TRIALS COMPLETED: 0. | |

Sound: a hop per bundle, a hundred tiny pops; a door slam; four calendar rips, each slower than the last.

## Scene 6 · attendance-at-a-funeral

- id: attendance-at-a-funeral
- act: Two trials
- transition_in: same plate (no seam)
- cue: "Only fifteen percent of the budget"
- time: 03:34.6 to 04:26.5 (51.9 s)
- voiceover: "Only fifteen percent of the budget went to clinical trials; the rest funded observational studies, data management, and administration. Of those enrolled, roughly eleven percent were in interventional trials that actually tested treatments. The other eighty-nine percent were in observational studies, which is the medical equivalent of taking attendance at a funeral. Cost per interventional patient: five hundred and four thousand, five hundred dollars, the price of a house. Nobody got a house and nobody got cured. They got observed. Expensively. The observation was very thorough. It has been peer-reviewed. The peers also observed the patients. The patients are still sick, but they are the most well-documented sick people in the history of sickness."
- layer: B, plate two-wards
- bit: The right half watches its patients through opera glasses, takes the roll over the dead, and buries the rest in their own paperwork.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Only fifteen percent of the budget went to clinical trials; the rest funded observational studies, data management, and administration. Of those enrolled, roughly eleven percent were in interventional trials that actually tested treatments." | 15% to trials; 11% got tested. | The N.I.H. building comes out of its door holding opera glasses to its window eyes, a clipboard under its arm. Down the right row, about one bed in nine gets a pill. | |
| "The other eighty-nine percent were in observational studies, which is the medical equivalent of taking attendance at a funeral." | 89% only watched. | The building walks the rest of the row peering at each patient through its opera glasses. One by one the watched patients turn into grinning skeletons, and at each bed it ticks its clipboard: PRESENT. | The skeletons raise a bony hand for the roll call. |
| "Cost per interventional patient: five hundred and four thousand, five hundred dollars, the price of a house. Nobody got a house and nobody got cured. They got observed. Expensively." | $504,500 a tested patient, spent on watching. | Close on one of the few tested patients. A price tag drops onto his bed: $504,500. A little house slides in next to the bed and the tag swings over to it; it fits. The house slides away again, and the building goes on peering at him. | |
| "The observation was very thorough. It has been peer-reviewed. The peers also observed the patients." | | The committee files in round the bed, and all of them peer at him together. | He pulls his blanket up to his chin. |
| "The patients are still sick, but they are the most well-documented sick people in the history of sickness." | Records, not recovery. | Paper drifts down onto every bed down the row, sheaf by sheaf, until the patients are buried in drifts to the ceiling, only their thermometers sticking out. | |

Sound: a lens squeak per peer; a pencil tick per bed; a soft x-ray zap per skeleton; a church bell tolls once at "funeral."; a price-tag thunk; a creak as the house slides in and out; a long hiss of paper falling.

## Scene 7 · truly-absurd

- id: truly-absurd
- act: Two trials
- transition_in: same plate (no seam)
- cue: "It gets worse."
- time: 04:26.5 to 05:02.7 (36.2 s)
- voiceover: "It gets worse. The treatments RECOVER eventually selected were called "truly absurd" by patient advocates. Low-dose naltrexone, the number one patient-requested treatment (generic, cheap, already showing results in independent studies), was excluded for over two years before finally being added in round two. David Putrino, director of rehabilitation innovation at Mount Sinai, called the spending "largely wasted". Researchers outside RECOVER had lists of drugs to test. The system ignored them."
- layer: B, plate two-wards
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "It gets worse. The treatments RECOVER eventually selected were called "truly absurd" by patient advocates." | Patients called the picks absurd. | The building picks a few bottles off its shelf. A hand pokes up out of a paper heap holding a card: TRULY ABSURD. | |
| "Low-dose naltrexone, the number one patient-requested treatment (generic, cheap, already showing results in independent studies), was excluded for over two years before finally being added in round two." | The drug patients asked for most waited two years. | Every paper heap down the row raises a hand holding up the same small bottle: LOW-DOSE NALTREXONE, #1 REQUESTED. The building plants a velvet rope in front of it. A calendar tears off two years. Then it lifts the rope and lets the bottle in: ROUND TWO. | |
| "David Putrino, director of rehabilitation innovation at Mount Sinai, called the spending "largely wasted"." | | David Putrino steps up beside the row and holds up a card: LARGELY WASTED. | Behind him the bus-sized bundle at the N.I.H.'s door goes down like a punctured tyre, with a long raspberry. |
| "Researchers outside RECOVER had lists of drugs to test. The system ignored them." | Outside lists were ignored. | Three scientists push long lists under the N.I.H.'s door. Each list slides straight out through a flap at the back of the building into a wastebasket. | |

Sound: a rustle as the hands come up; a velvet-rope clink; two calendar rips; paper slides and three soft pats into the basket.

## Scene 8 · tests-patience

- id: tests-patience
- act: Two trials
- transition_in: cut back to the-score
- cue: "Six hundred trials were possible"
- time: 05:02.7 to 05:14.2 (11.5 s)
- voiceover: "Six hundred trials were possible with that money. Zero were completed. That is the difference between a system that tests treatments and a system that tests patience."
- layer: B, plate the-score
- bit: Payoff: back to the scoreboard; its zero has come home, and the waiting room grows beards.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Six hundred trials were possible with that money." | 600 possible. | The scoreboard, a new row under N.I.H.: POSSIBLE 600. | |
| "Zero were completed." | 0 done. | The big 0 rolls back in from the edge of the frame and climbs into the COMPLETED window. | It is dusty from its trip. |
| "That is the difference between a system that tests treatments and a system that tests patience." | The N.I.H. tests how long patients wait. | The camera drops below the scoreboard to a waiting-room bench of long COVID patients holding numbered tickets. On "patience." long white beards shoot down to their knees, and the patient at the end of the bench is a skeleton with a beard, still holding his ticket. | |

Sound: a scoreboard click; the 0's rumble coming back and a clunk; a rising whistle as the beards grow.
