---
format: 1920x1080
duration: 1:57.2
message: "Publishing the answers doesn't work: the returns are public (101 to 1 for vaccines, 637 to 1 for trials, less than 1 to 1 for farm subsidies) and ignored, because average citizens have almost no influence; the Evidence Machine supplies the answer, and the bonds make following it pay."
arc: Title card (the bulb over KNOWING lights and changes nothing) → Wishonia has bad news → the politician at an exam desk with the answer key behind him circles the wrong answer and the F eats him → the citizens' line on the Princeton chart is a steel rail they can't bend, and the fat cat tips the other with his cane → on the Capitol steps the politician reads the results, bins them, follows the votes and the campaign funds, and spins through the revolving door as a Lobbyist → on the Capitol lawn the bond-powered politician spins at a signpost with blank arms until the Optimitron locks on five padlocks → three things in alphabet blocks → the Optimitron toasts policy cards: WORKS comes out golden, DOESN'T comes out burnt
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 3, "Why Knowing Isn't Enough"
audio: optimocracy.27caf050.mp3, 07:38.7 to 09:35.9
version: v2
---

# Part 3 storyboard: "Why Knowing Isn't Enough"

- **Source:** `knowledge/solution/optimocracy.qmd`, "Why Knowing Isn't Enough" and the opening of "The Mechanism: Recommend, Track, Reward". The Princeton study is Gilens and Page 2014 (`gilens2014`).
- **The numbers:**
  - `childhood_vaccination_roi`: the narrator says 101 to 1 (the book cites the Copenhagen Consensus's 101:1 for vaccinating children in 80 of the poorest countries, `copenhagenconsensus2023`; the parameter `childhood_vaccination_roi` is a different, 10.9:1 figure). The screen uses "101 : 1".
  - `dfda_roi_rd_only`: the narrator says 637 to 1 for pragmatic clinical trials; `_variables.yml` now has 439. The screen uses "637 : 1".
  - Agricultural subsidies: less than 1 to 1 (spoken, not a parameter).
  - Drawn to scale on one chart, if the 1:1 line is 10 px high, 101:1 is 1,010 px (taller than the frame) and 637:1 is 6,370 px (the camera has to tilt to find its top).
  - Princeton study: 1,779 policy decisions; average citizens have "little or no independent influence" (cited, `gilens2014`, not a parameter). For the chart: the line for average citizens is flat at about 30% whatever they want; the line for economic elites rises with what they want.
- **What the viewer must leave with:** the answers are already published and ignored, because politicians are paid in votes, campaign money and jobs, not in being right; so the plan needs a true answer nobody can corrupt and a reward for following it.
- **Plates:**
  - Host scenes (host-bad-news, host-three-things, host-the-appliance): Wishonia at her console on the observation deck, Earth in the window, the Optimitron on the ledge.
  - `exam-room`: one school desk on a plain floor, a giant answer key on the wall behind it as a bar chart, "DOLLARS BACK FOR EACH DOLLAR".
  - `influence-chart`: a line chart on aged paper, "CHANCE A POLICY PASSES" up the side and "HOW MUCH THEY WANT IT" along the bottom.
  - `capitol-steps`: the Capitol on a plain field with a revolving door, a little lobbying office beside it, and a signpost on the lawn in front (nobody-can-corrupt).
- **Cast:** existing cut-outs: `politician`, `fat-cat`, `crowd` (the citizens), `capitol`, `ballot-box`, `lobbyist`, `bond`, `signpost`, `goose`. Registered, not drawn yet: `school-desk`, `report-card`, `f-monster` (Part 20's), `super-pac`, `padlock`, `optimitron` (as a cut-out), `policy-card`, `newspaper`. New: `revolving-door`, `corn` (one ear, also used in Parts 4 and 6).
- **Callbacks:**
  - Episode 1 Part 20's red F with claws and fangs eats the politician who fails the test.
  - Part 1 of this chapter: the bond's blank back ("POLICIES THAT WORK:") is filled in by the Optimitron in host-the-appliance.
  - Set up for Part 5: the five padlocks on the Optimitron in nobody-can-corrupt are the five sources.
- **New art:**
  - `revolving-door`: a brass revolving door with four glass leaves, set into the Capitol's front; a little "LOBBYING" office beside it with its own door (shared with the incentive-alignment-bonds and unrepresentative-democracy chapters).
  - `corn`: one ear of corn, raw and toasted.
- **Kit additions:**
  - A rail: a chart line drawn as a thick steel rail that does not bend, and a line that swings up about its end (the elite line).
  - A spin: a cut-out turning on the spot faster and faster (the politician at the signpost, the revolving door).
  - Host props for `KIT.props`: three brass plates (RECOMMEND, TRACK, REWARD) and three wooden alphabet blocks (SAY, LOOK, PAY), letters in code.

## Scene 1 · knowing-title

- id: knowing-title
- act: Title
- transition_in: cut
- cue: "Why Knowing Isn't Enough"
- time: 07:38.7 to 07:41.4 (2.7 s)
- voiceover: "Why Knowing Isn't Enough."
- layer: A, title card
- bit: The heading, with a light bulb that goes on and changes nothing.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Why Knowing Isn't Enough." | The heading. | The period card. A light bulb over KNOWING switches on with a ping. | It hangs there lit, and nothing else on the card moves. |

Sound: a whirr; a ping.

## Scene 2 · host-bad-news

- id: host-bad-news
- act: The answer key is public
- transition_in: iris in on her face
- cue: "If you're thinking"
- time: 07:41.4 to 07:49.1 (7.7 s)
- voiceover: "If you're thinking "just publish the results and politicians will do the right thing," I have some bad news about your species."
- layer: A, host
- wishonia: skeptical-smile + body-listening; sad-closed + body-hand-chest on "bad"
- bit: Earth hopes; she lowers the news gently.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "If you're thinking "just publish the results and politicians will do the right thing,"" | | Iris in. In the window, a tiny newspaper rises up off Earth like a flag on a pole: RESULTS PUBLISHED. Earth smiles. | |
| "I have some bad news about your species." | | She pats the case file sympathetically. In the window the newspaper droops, and a tiny politician on Earth uses it to wrap a fish. | |

Sound: a hopeful flag-raise squeak; a paper droop; a slap of a fish.

## Scene 3 · cheat-sheet

- id: cheat-sheet
- act: The answer key is public
- transition_in: cut
- cue: "The Copenhagen Consensus already publishes"
- time: 07:49.1 to 08:16.4 (27.4 s)
- voiceover: "The Copenhagen Consensus already publishes rigorous benefit-cost analyses. Childhood vaccination: one hundred and one to one returns. Pragmatic clinical trials: six hundred and thirty-seven to one. Agricultural subsidies: less than one to one. The answer key is public. It's been public for years. Your governments ignore it. You have the cheat sheet, and you're still failing the test on purpose."
- layer: B, plate exam-room
- bit: **The politician takes the test with the answer key on the wall in front of him, and picks the wrong answer anyway.** The key is a bar chart so tall the camera has to climb it; he looks right at it, circles the farm subsidy. Payoff: the F eats him.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Copenhagen Consensus already publishes rigorous benefit-cost analyses. Childhood vaccination: one hundred and one to one returns." | The answers are published; vaccines return 101 to 1. | The politician at a little school desk, pencil in his fist, an exam paper, "BUDGET". On the wall, a huge answer key: "DOLLARS BACK FOR EACH DOLLAR", with a 1:1 line along the bottom. The first bar, VACCINATION, shoots up the wall out of the frame: "101 : 1". | |
| "Pragmatic clinical trials: six hundred and thirty-seven to one." | Trials return 637 to 1. | A second bar, CLINICAL TRIALS, shoots up six times further. The camera tilts up and up along it, past the clouds, and finds "637 : 1" at the top. | A goose flies past the label. |
| "Agricultural subsidies: less than one to one." | Farm subsidies lose money. | Tilt back down to the floor: the third bar, one ear of corn, is a stub below the 1:1 line. "LESS THAN 1 : 1". | |
| "The answer key is public. It's been public for years. Your governments ignore it." | They know and ignore it. | The politician looks up at the key, nods, licks his pencil, and circles AGRICULTURAL SUBSIDIES. | |
| "You have the cheat sheet, and you're still failing the test on purpose." | | A report card slides onto his desk; a red F stamps on it. The F climbs off the card on its claws, opens its fangs and eats him, pencil and all. | It burps out his tie. |

Sound: a pencil tap; a whoosh for each bar going up and a stamp for each label; a honk; a scribble circle; a stamp; a growl, a chomp, a burp.

## Scene 4 · the-flat-line

- id: the-flat-line
- act: Why they ignore it
- transition_in: cut
- cue: "Why? Because information doesn't change"
- time: 08:16.4 to 08:35.7 (19.3 s)
- voiceover: "Why? Because information doesn't change incentives. A Princeton study analyzed one thousand seven hundred and seventy-nine policy decisions and found that average citizens have "little or no independent influence" on policy outcomes. Economic elites and organized interest groups drive policy."
- layer: B, plate influence-chart
- bit: **On the chart of what citizens want, their line is a steel rail: they jump on it and it doesn't bend, and the fat cat tips the other one with his cane.**
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Why? Because information doesn't change incentives. A Princeton study analyzed one thousand seven hundred and seventy-nine policy decisions" | 1,779 decisions studied. | The chart, "CHANCE A POLICY PASSES" against "HOW MUCH THEY WANT IT". "1,779 DECISIONS" stamps in its corner. | |
| "and found that average citizens have "little or no independent influence" on policy outcomes." | Ordinary people barely count. | The AVERAGE CITIZENS line runs flat across the chart: a steel rail. At the "WANT IT A LOT" end, a crowd of citizens climbs onto it, jumps up and down on it, swings on it. It doesn't move. | One jumps so hard he bounces off the chart. |
| "Economic elites and organized interest groups drive policy." | The rich and organized groups decide. | The fat cat strolls up to the second line, ECONOMIC ELITES, and lifts its end with his cane. It swings up steeply, and the citizens on the flat rail watch it go. | He lights his cigar off the top. |

Sound: a stamp; a dull clang per jump on the rail; a boing as one bounces off; a creak as the elite line swings up; a match strike.

## Scene 5 · votes-papers-and-a-job

- id: votes-papers-and-a-job
- act: Why they ignore it
- transition_in: cut
- cue: "You already knew this"
- time: 08:35.7 to 08:56.5 (20.8 s)
- voiceover: "You already knew this (it's covered in Unrepresentative Democracy). The point here is that publishing better data doesn't fix the problem. Your politicians already know which programs produce value. They don't act because acting doesn't maximize getting votes, getting papers, or getting a nice job afterward selling access to their replacements."
- layer: B, plate capitol-steps
- bit: **The politician knows the right answer and follows his three paydays instead, through a revolving door and back again.** He reads the results, nods, bins them, and goes where the votes and the campaign money go. Payoff: out of the revolving door as a Lobbyist, he knocks to sell access to a politician who looks exactly like him.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "You already knew this (it's covered in Unrepresentative Democracy). The point here is that publishing better data doesn't fix the problem. Your politicians already know which programs produce value." | Better data alone fails; they already know. | The politician on the Capitol steps. A newspaper of better data lands at his feet with a thump: RESULTS. He reads it, nods, folds it, and drops it over his shoulder. | |
| "They don't act because acting doesn't maximize getting votes, getting papers," | They follow votes and money. | A trail of ballots leads one way from a ballot box; he follows it, licking his lips. The Super PAC backpack swoops past with a sack labelled CAMPAIGN FUNDS; he follows that too. | |
| "or getting a nice job afterward selling access to their replacements." | Then the revolving door. | He walks into the Capitol's revolving door, spins round once and comes out the side as the Lobbyist, mask and fedora on, into the LOBBYING office. He walks straight back to the Capitol's door and knocks. It opens on a new politician with the same teeth, the same jaw and the same tie. | They shake hands. Each one recognises the other's teeth. |

Sound: a newspaper thump; a crumple; footsteps over ballots; a whoosh for the Super PAC; the door's rubber whump-whump spin; a knock; a squeak of a handshake.

## Scene 6 · nobody-can-corrupt

- id: nobody-can-corrupt
- act: Two problems
- transition_in: cut
- cue: "This is the gap between"
- time: 08:56.5 to 09:15.7 (19.3 s)
- voiceover: "This is the gap between Incentive Alignment Bonds (which solve the incentive problem) and the Evidence Machine (which solves the knowledge problem). I.A.B.s make doing the right thing profitable. But they need to know what the right thing IS. That requires a measurement system nobody can corrupt."
- layer: B, plate capitol-steps
- bit: **The bonds' Super PAC gives the politician a motive, strapped on as a jet pack, and it fires him full speed at a signpost with blank arms.** He spins on the lawn until he screws himself into the ground. Payoff: the Optimitron drops onto the post, points one way, and five padlocks snap shut on it.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "This is the gap between Incentive Alignment Bonds (which solve the incentive problem) and the Evidence Machine (which solves the knowledge problem)." | Two separate problems. | The signpost on the Capitol lawn. On its left, the INCENTIVE ALIGNMENT BOND; on its right, the Optimitron. A gap between them. | |
| "I.A.B.s make doing the right thing profitable." | The bonds make right pay. | The politician runs down the steps with the Super PAC strapped to his back as a jet pack, its patch FUNDED BY INCENTIVE ALIGNMENT BONDS. It fires, and he rockets at the signpost. | |
| "But they need to know what the right thing IS." | Which way is right? | The signpost's four arms are blank. He spins on the spot in front of it, faster and faster, until he corkscrews into the ground up to his knees. | |
| "That requires a measurement system nobody can corrupt." | The answer must be uncorruptible. | The Optimitron drops onto the top of the post, and one arm swings to point: "THIS WAY". Five padlocks snap shut round the Optimitron one after another. | The politician pulls himself out of the ground, the jet pack fires again, and he rockets off the way it points. |

Sound: a jet roar; a whirring spin, rising; a screw-in squeak; a clunk as the Optimitron lands; five padlock snaps; a fast exit whoosh.

## Scene 7 · host-three-things

- id: host-three-things
- act: The mechanism
- transition_in: iris in on her face
- cue: "The Mechanism: Recommend, Track, Reward"
- time: 09:15.7 to 09:28.9 (13.2 s)
- voiceover: "The Mechanism: Recommend, Track, Reward. The Evidence Machine does three things. That's it. Three things. Your species has difficulty with three things, so I'll use small words."
- layer: A, host
- wishonia: happy-smile + body-presenting; neutral-small + body-counting on "three"; smirk-smile + body-open-palms on "small"
- bit: The heading appears as three big words, and she swaps them for baby blocks.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Mechanism: Recommend, Track, Reward." | The heading. | Iris in. Three big brass plates drop onto the ledge one by one: RECOMMEND, TRACK, REWARD. | |
| "The Evidence Machine does three things. That's it. Three things." | | She counts them on three fingers. | |
| "Your species has difficulty with three things, so I'll use small words." | | She sweeps the plates off the ledge and sets down three wooden alphabet blocks instead: SAY, LOOK, PAY. | She stacks them carefully, then pushes them a little closer to the window. |

Sound: three clanks; a sweep and a far clatter; three wooden clonks.

## Scene 8 · host-the-appliance

- id: host-the-appliance
- act: The mechanism
- transition_in: same plate (no seam)
- cue: "On Wishonia, we just call this"
- time: 09:28.9 to 09:35.9 (7.0 s)
- voiceover: "(On Wishonia, we just call this the Optimitron. It's an appliance. You plug in policies, it tells you which ones work.)."
- layer: A, host
- wishonia: smirk-smile + body-presenting; happy-smile + body-point-right on "work."
- bit: She toasts policies like bread: the good one comes out golden, the bad one comes out black.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "(On Wishonia, we just call this the Optimitron. It's an appliance." | | She pats the Optimitron on the ledge. Its face smiles. | |
| "You plug in policies, it tells you which ones work.)." | It sorts what works. | She drops two policy cards into its slots and pushes the lever. Ding: one pops up golden, branded "WORKS". The other pops up burnt black and smoking, "DOESN'T". She writes the golden one onto the back of the bond, under POLICIES THAT WORK. | The burnt card's smoke rings drift into the window and fog Earth. |

Sound: a pat; two card slides; a lever clunk; a ding and two pops; a pen scratch.
