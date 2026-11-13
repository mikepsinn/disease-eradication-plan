---
format: 1920x1080
duration: 2:48.8
message: "A trial of 3,000 can't see a one-in-10,000 reaction, the monitoring afterward is a voluntary suggestion box that let Vioxx kill up to 55,000 Americans, and companies may bury the trials that failed."
arc: A block of 3,000 where nobody reacts, then millions where people pop into flames like popcorn → the suggestion box with no bottom and the Vioxx pile behind it → YOU arrives grey after 8.2 years and posts his slip straight through → across the road, the world-of-tomorrow machine that catches the flare at once, against the fax and the box praying under a slipping halo → the published-results bars and the black hole on the desk → the deli's grade card and the sandwich's blue ribbon → WE TESTED THIS DRUG! → the tower digs past Jimmy Hoffa, and the next towers walk into the same dead end → the casino reports its losers
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 11, "The Suggestion Box"
audio: fda-is-unsafe-and-ineffective.5d00ae46.mp3, 27:38.3 to 30:27.2
version: v2
---

# Part 11 storyboard: "The Suggestion Box"

- **Source:** `knowledge/problem/fda-is-unsafe-and-ineffective.qmd`, sections "Small Trials Are Dangerous" and "The Negative Results Black Hole".
- **The numbers:**
  - Phase 3 trials test 1,000 to 3,000 patients; a one-in-10,000 reaction is invisible in 3,000 (in 3,000 the expected count is 0.3).
  - FAERS captures less than 10% of adverse events (`adverse-event-underreporting`).
  - Vioxx killed an estimated 38,000 to 55,000 Americans (`vioxx-deaths`); more than the Korean War's US dead (about 36,000; bar height only).
  - `efficacy_lag_years`: 8.2 years.
  - A decentralized FDA with 10 million participants: 1,000 expected cases of a one-in-10,000 reaction (the narrator's 10 million; the system is the reader's to build, not an existing one).
  - Published: 37% of negative results, 94% of positive (`publication-bias-clinical-trials`); about $100 billion a year wasted repeating failed experiments (cited, not a parameter).
- **What the viewer must leave with:** trials are too small to see rare harms, the check after approval is a voluntary box that misses nine in ten, and failed trials can be hidden, so the same mistakes are paid for again.
- **Plates:**
  - `popcorn-field`: a pictogram field on aged paper: a block of 3,000 tiny people, then the field spreading to millions.
  - `suggestion-box`: a road on aged paper, 8.2 years long, from the approval cabinet to a wooden suggestion box on a post, a headstone pile behind it; across the road, a gleaming world-of-tomorrow machine room.
  - `black-hole-street`: a desk on a street with a swirling black hole in its blotter, a bar chart behind it; a deli counter across the street; an alley beside it that ends in a brick wall under a DEAD END sign.
- **Cast:** existing: `citizen` (pictogram size), `skeleton`, `flames`, `magnifier`, `fax-machine`, `pill-bottle` (VIOXX, and a chemotherapy bottle with a blank label), `doctor`, `patient`, `headstone`, `approval-cabinet`, `you`, `beard`, `mainframe`, `robot`, `extinguisher`, `halo`, `pharma-tower` (from Part 4, with its shovel), `fda-sip`, `speech-bubbles`, `deli-counter`, `sandwich`, `rosette`, `hamster-wheel`, `scientist`, `flask`, `bill-plain`, `brick-wall` (from Part 8), `signpost`, `scoreboard`, `suggestion-box` (from Part 7, here "F.A.E.R.S. · REPORT IF YOU FEEL LIKE IT"). New: `jimmy-hoffa` (Jimmy Hoffa caricatured, buried in his 1970s suit, waving).
- **Callbacks:** episode 1 Part 12's fax machine and smoke detector by mail; Part 4's three towers; Part 1's YOU with the committee beards; Part 7's complaints box, the same box.
- **New art:** Jimmy Hoffa.
- **Kit additions:**
  - Popcorn: random tiny figures across a pictogram field flare and swap to skeletons (seeded `KIT.rng`).
  - The black hole on the desk is an effect in code: a spiral that pulls cut-outs in, shrinking and spinning them.

## Scene 1 · popcorn

- id: popcorn
- act: Small trials
- transition_in: cut; the heading card comes up from black
- cue: "Small Trials Are Dangerous"
- time: 27:38.3 to 27:54.0 (15.7 s)
- voiceover: "Small Trials Are Dangerous. Phase three trials test one thousand to three thousand patients. A one-in-ten-thousand adverse event is mathematically invisible in a trial of three thousand. Then the drug goes to millions."
- layer: B, plate popcorn-field
- bit: **A block of 3,000 where nothing happens, then the field spreads to millions and people start popping into flames like popcorn.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Small Trials Are Dangerous. Phase three trials test one thousand to three thousand patients." | 1,000 to 3,000. | The heading card, then a block of tiny people on aged paper, "3,000", each taking a pill. | |
| "A one-in-ten-thousand adverse event is mathematically invisible in a trial of three thousand." | Too small to see it. | Nothing happens. A magnifying glass sweeps the block. Nothing. A tick: "SAFE". | |
| "Then the drug goes to millions." | Millions take it. | The block spreads out to the edges of the frame and keeps going as the camera pulls back: millions. Here, then there, a tiny person bursts into flames and pops into a skeleton, pop, pop, pop-pop-pop, faster, like a pan of popcorn. | |

Sound: a soft pill swallow; a magnifier squeak and a tick; a crackle that builds into popcorn.

## Scene 2 · suggestion-box

- id: suggestion-box
- act: The monitoring
- transition_in: cut
- cue: "After approval, the F.D.A. monitors safety"
- time: 27:54.0 to 29:06.2 (72.1 s)
- voiceover: "After approval, the F.D.A. monitors safety using the F.D.A. Adverse Event Reporting System, or F.A.E.R.S., a system where doctors voluntarily report problems if they feel like it. It captures less than ten percent of actual adverse events. Vioxx killed an estimated thirty-eight thousand to fifty-five thousand Americans before this honor system noticed. That's more people than died in the entire Korean War, detected by a system that relies on doctors filling out optional paperwork. I want to be clear: the eight point two years delay is supposed to be for safety. And then the safety monitoring after approval is a suggestion box. You waited eight point two years to get to the suggestion box. A decentralized F.D.A. with ten million participants catches one in ten thousand reactions, includes real populations, tracks long-term outcomes, and provides automated surveillance instead of voluntary paperwork. You have a fax machine and a suggestion box. One of these is a safety system. The other is a prayer with an eight point two years waiting period."
- layer: B, plate suggestion-box
- bit: **The whole safety system after approval is one wooden box with no bottom; YOU walks 8.2 years to reach it.** Across the road, the machine that would catch every flare at once; on this side, the fax and the box kneel and pray.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "After approval, the F.D.A. monitors safety using the F.D.A. Adverse Event Reporting System, or F.A.E.R.S., a system where doctors voluntarily report problems if they feel like it. It captures less than ten percent of actual adverse events." | Reporting is voluntary; under 10%. | A wooden suggestion box on a post: "F.A.E.R.S. · REPORT IF YOU FEEL LIKE IT". Ten doctors stroll past it, whistling; one stops and drops in a slip. | |
| "Vioxx killed an estimated thirty-eight thousand to fifty-five thousand Americans before this honor system noticed. That's more people than died in the entire Korean War, detected by a system that relies on doctors filling out optional paperwork." | 38,000 to 55,000; more than the Korean War. | Behind the box the smiling VIOXX bottle hops along a line of patients; headstones pile up behind it into a heap, "38,000–55,000". Beside the heap, a shorter pile, "KOREAN WAR". | |
| "I want to be clear: the eight point two years delay is supposed to be for safety. And then the safety monitoring after approval is a suggestion box. You waited eight point two years to get to the suggestion box." | The 8.2-year wait ends at the box. | The camera pulls back along the road: the box is at the end of an 8.2-year road that starts at the approval cabinet. YOU arrives at the box, grey, bent, his committee-length beard trailing behind him, and posts a slip. It falls straight out of the bottom onto his shoe. | |
| "A decentralized F.D.A. with ten million participants catches one in ten thousand reactions, includes real populations, tracks long-term outcomes, and provides automated surveillance instead of voluntary paperwork." | 10 million, watched live. | Across the road: a gleaming world-of-tomorrow machine room, its wall a map of ten million pinpoint lights (old, young, pregnant, sick). One light flares red; a tin robot whips out an extinguisher and puts out the tiny person: "1 IN 10,000 ✓". | |
| "You have a fax machine and a suggestion box." | | Back on this side: a stool with a fax machine and the suggestion box on it. | The fax screeches once. |
| "One of these is a safety system. The other is a prayer with an eight point two years waiting period." | | The fax and the box kneel on the stool, hands together. A halo lowers onto the box and slides off; it puts it back; it slides off. | |

Sound: whistling feet; one slip in; a hop and a thunk per headstone; a long shuffle; a slip that lands on a shoe; a hum and a bleep; a fizz of the extinguisher; a fax screech; an organ chord; the halo's clink, twice.

## Scene 3 · black-hole

- id: black-hole
- act: The black hole
- transition_in: cut; the heading card comes up from black
- cue: "The Negative Results Black Hole"
- time: 29:06.2 to 29:48.8 (42.7 s)
- voiceover: "The Negative Results Black Hole. Here's something that would be illegal if anybody important cared: Thirty-seven percent of negative trial results are published. Ninety-four percent of positive trial results are published. Approximately one hundred billion dollars is wasted annually repeating failed experiments. Companies are allowed to hide when drugs don't work. Restaurants can't hide when they fail a health inspection. I checked this twice because I thought I was wrong, but I wasn't. A sandwich has more regulatory transparency than chemotherapy. I don't know what to do with that information but I've had it for three days now and it won't go away."
- layer: B, plate black-hole-street
- bit: **A black hole in a desk eats the failed trials; across the street the deli has to post its grade.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Negative Results Black Hole. Here's something that would be illegal if anybody important cared:" | | The heading card, then a desk with a black hole swirling in the blotter. | |
| "Thirty-seven percent of negative trial results are published. Ninety-four percent of positive trial results are published." | 37% against 94%. | A bar chart behind it, "TRIAL RESULTS PUBLISHED": "NEGATIVE · 37%", "POSITIVE · 94%". Result papers float in: the "FAILED" ones spiral into the hole, the "WORKED" ones land neatly on the bars. | |
| "Approximately one hundred billion dollars is wasted annually repeating failed experiments." | $100 billion a year. | Beside the desk, a scientist in a hamster wheel runs the same experiment: her flask blows up, she runs round, it blows up again: "$100,000,000,000 A YEAR". | |
| "Companies are allowed to hide when drugs don't work." | | A pharma tower slides its "FAILED" card into the hole and whistles. | |
| "Restaurants can't hide when they fail a health inspection. I checked this twice because I thought I was wrong, but I wasn't." | | Across the street, a deli counter with a grade card on its glass: "C". | |
| "A sandwich has more regulatory transparency than chemotherapy. I don't know what to do with that information but I've had it for three days now and it won't go away." | A sandwich discloses more than chemotherapy. | A club sandwich with a label listing everything in it gets a blue rosette; a chemotherapy bottle beside it has a blank label. The camera tries to leave; the sandwich follows it to the edge of the frame. | It is still there in the corner of the next shot. |

Sound: a low swirling hum; paper sucked in with a slurp; a boom per flask; a whistle; a ding for the rosette.

## Scene 4 · deeper-than-hoffa

- id: deeper-than-hoffa
- act: The black hole
- transition_in: same plate (no seam)
- cue: "Company: We tested this drug"
- time: 29:48.8 to 30:27.2 (38.3 s)
- voiceover: "Company: "We tested this drug!". Regulator: "Did it work?". Company: "...We tested this drug!". Pharmaceutical companies bury negative results deeper than Jimmy Hoffa. Other companies waste billions testing the same dead ends. Your insurance premiums fund this magnificent inefficiency. It's like casinos only having to report when people win. Actually, I think casinos DO have to report when people win. So drugs get less honesty than gambling. I keep finding these comparisons and they keep getting worse."
- layer: B, plate black-hole-street
- bit: **The tower digs a grave for its results deeper than Jimmy Hoffa's; the other towers walk into the same dead end, on YOU's money.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Company: "We tested this drug!". Regulator: "Did it work?". Company: "...We tested this drug!"." | They dodge the question. | A pharma tower and the FDA building face to face by the desk, speech bubbles: "WE TESTED THIS DRUG!" / "DID IT WORK?" / "...WE TESTED THIS DRUG!". | The tower grins harder. |
| "Pharmaceutical companies bury negative results deeper than Jimmy Hoffa." | | The tower digs. Its shovel passes Jimmy Hoffa in his 1970s suit, buried, who waves; it digs on, deeper, drops the "FAILED" folder in, and fills the hole. | Hoffa gives a thumbs up from above it. |
| "Other companies waste billions testing the same dead ends." | | Up the alley, the other two towers walk one after another into the brick wall under the "DEAD END" sign, bonk, bonk, back up, and bonk again. | |
| "Your insurance premiums fund this magnificent inefficiency." | You pay for it. | YOU feeds a plain bill into a slot in the wall, "PREMIUMS", and the towers back up for another bonk. | |
| "It's like casinos only having to report when people win. Actually, I think casinos DO have to report when people win." | Casinos report more. | A casino's lit Scoreboard, "WINNERS"; beside it a second board flicks on, "LOSERS", with a long list. | |
| "So drugs get less honesty than gambling. I keep finding these comparisons and they keep getting worse." | | Back at the desk, the towers' own board: "WINNERS", and nothing beside it. | |

Sound: speech-bubble pops; shovel scrapes; a muffled hello; three bonks; a coin-slot clunk; a slot-machine jingle; silence.
