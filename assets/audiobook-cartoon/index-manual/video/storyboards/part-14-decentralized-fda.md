---
format: 1920x1080
duration: 4:45.4
message: "Spend the treaty money on patients instead of committees, and treatments reach people 212 years sooner, which prevents 10.7 billion deaths."
arc: Title card (the FDA scatters to the edges of the card) → Wishonia's ticker-tape parade and the dictionary with no word for it → the FDA official sitting on SAFE bottles like a hen → the paper reflex at the lectern → the money follows the patient and tramples the grants office → out of the terrarium → the protocol stamp flattens the lifeguard and jackets fly to 23.4 million → one lands on Wishonia's mug → 443 years squeezed to 36 → the approval cabinet opens, 212 years sooner → 10.7 billion rise out of the field with plans for Tuesday → the live detector lands on the one that works by mail → the coin on its edge → the doctor's prize wheel → grape soda → the ranking board crushes the wheel → the 40-page insert buries the patient → the meadow human dies mid-skip and keeps skipping → the doctor Googles in the hall → the outcome label buries the lawyer → louder wins, and both are charred → the Optimitron's card knocks the trophy away
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 14, "Your Decentralized FDA"
audio: index-manual.cbaf659d.mp3, 27:54.0 to 32:39.5
version: v3
---

# Part 14 storyboard: "Your Decentralized FDA"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. This part is the 1950s atomic-age instructional film. Layer A is the host's set (`KIT.studio`): Wishonia at her navy lectern in front of the mustard studio wall, the coffee mug on the lectern, a guest standing at the free wall on her right when a scene needs one. Layer B is an illustrated plate on a plain field that the camera travels over (`KIT.camera`), one framing per phrase; Wishonia is not in the plates, she is the voice. The period film (`KIT.film`) runs over every shot. Money is money green; a cross seal is medicine money, a missile seal war money, no seal plain money. Part 2 (`parts/part-02.json`, `compositions/scenes/part-02/`) is the reference for every kind of shot.

**Spine.** One patient. She is an everyday human, `KIT.person({ tone: 2, outfit: "dress", hair: 1, color: 1, light: "red", mood: "worried" })` (the same options in every scene, so she is the same woman), with a mustard-and-orange striped scarf at her neck (drawn at `KIT.rig(o).neck`) and her chest light blinking red. She dives after Wishonia's paper in small-pieces-of-paper, gets a medicine paper for a puppy and goes through a trial door in subsidy-follows-patient, is flicked out of the terrarium and walks into a real hospital, catches a life jacket, moves up the squeezed queue and catches the SAFE bottle out of the approval cabinet in two-hundred-twelve-years-sooner. That bottle is hers from then on (`KIT.props.pillBottle({ face: "smile", label: "SAFE" })`): it lights up with side effects in smoke-detector-live, matches row 1 of the ranking board, and gets the outcome label in outcome-label, where she takes the pill and her chest light turns teal. In the old-system scenes (decision-wheel, forty-page-insert, meadow-ad, ask-your-doctor) her light is still red.

**The everyday humans who come back.** The doctor, `KIT.person({ tone: 1, outfit: "labcoat", color: 1 })`, with a head mirror and a stethoscope: small-pieces-of-paper, decision-wheel, ranked-treatments, forty-page-insert, ask-your-doctor. The lawyer, `KIT.person({ tone: 3, outfit: "suit", color: 1, holdR: "briefcase" })`: smoke-detector-live, forty-page-insert, outcome-label. Same options in every scene. In the props lines, "patient", "doctor" and "lawyer" mean these three.

**Running gag: the replacement lands on the old thing.** Each new piece of the system arrives on top of the piece it replaces and flattens it: the stampede of medicine papers runs over the grants officer and a giant red ✗ drops on the grant committee (subsidy-follows-patient), the protocol stamp flattens the lifeguard into his chair (life-jackets-handed-out), the live smoke detector slams onto the one that works by mail (smoke-detector-live), the ranking board drops onto the prize wheel (ranked-treatments), the lawyer's own 40-page insert buries him (outcome-label). The last one flies: the Optimitron's policy card shoots across the set and knocks the trophy out of the charred winner's hands (optimitron-appliance).

**Callbacks.** From Part 12: the smoke detector from smoke-detector-by-mail, still charred, its letter still up and its mailbox flag; the approval cabinet from committee-8-years with its hourglass on "8.2 YEARS", the SAFE bottle, the life preserver the lifeguard locked in it (lifeguard-cabinet), the handprint and YOU's skeleton (bowler on) slumped against the glass; the beach from lifeguard-cabinet with the lifeguard and his binder, the two jackets on the hook and the line of swimmers and grinning skulls; the bearded committee from committee-8-years; the FDA official, drawn with Part 12's options exactly (`KIT.person({ tone: 0, outfit: "suit", color: 1, hair: 2, glasses: true, hat: null, seed: 12 })`: bald, in glasses, a small "FDA" badge on his lapel; without `hat: null` the kit gives his suit a hat, and the bowler is YOU's). "The dead keep waiting" pays off: the skulls get their jackets late, and the cabinet skeleton reaches for the bottle eight years late. From Part 9: the roped queue from queue-to-not-die (each human walking his disease on a leash, the back of the line grey and bearded, then skeletons) under the wait sign from untested-warehouse on "443 YEARS", and its shelf with the dusty "NEVER TESTED FOR THIS" bottle; "waiting ages you" runs backwards as the beards zip back up. From Part 1: the paper reflex from papers-with-presidents (every head snaps to a paper). From Part 2: the-toll's rows of headstones rising to the horizon come back the other way round in plans-for-tuesday, as rows of living humans.

**Set up here.** The Optimitron (`KIT.props.optimitron` with its defaults, so it is the same appliance) comes back in Step 1 (Part 17, wishocratic-allocation). The fat "212 YEARS SOONER" arrow sign comes back in Part 16 (quadrillion-equation), where a pill bottle rides it like a rocket on "acceleration"; the 212 years are also the Calculator's first sum there (host-remembers).

**Held frame.** plans-for-tuesday, after "deaths." until "individual" (about 1.5 s): the number in the sky over the empty field. A HOLD is silent.

**Transitions.** The title card comes up from black and goes down to black (`KIT.titleScene`); home-planet irises in on Wishonia's face. Host to plate and plate to host are cuts; so are plate to plate. Consecutive scenes on one plate continue with no seam (accordion-timeline into two-hundred-twelve-years-sooner; forty-page-insert through louder-wins on the living room). ranked-treatments cuts back to the exam room exactly as decision-wheel left it. life-jackets-handed-out cuts to the one-for-the-mug reaction cut on "million.", which cuts to accordion-timeline on "This". optimitron-appliance irises out on her face; Part 15's title card comes up from black.

**Bans for this part.**
- The cereal box, the cigarette pack, the soda can and the search box are plain. "Vioxx" is said, not drawn.
- The TV ad's crawl and end card sit inside the TV screen, above the keep-out.
- The two panelists in louder-wins are both the cast's politician; the winner's charred tie flickers red and blue, so neither team wins.

## Changes from v2

- Wishonia's office, its wall screen and her corner (PiP) are gone. She is on screen only at her lectern (home-planet, small-pieces-of-paper, they-make-you-guess, grape-soda, optimitron-appliance); every Earth scene is a plate the camera travels over, one framing per phrase.
- Labels that explained the picture are cut: the section banners, "CLINICAL TERRARIUM", "RANKED BY WHAT HAPPENED", the numbered arrow slots and "BUDGETS / LAWS / KEEP / THROW AWAY". What stays is text that is the joke or the fact.
- The wall-screen jokes moved: the live board is a ticker-tape parade at the lectern; the dictionary's "see EARTH" cuts to a new plate of the FDA official sitting on SAFE bottles like a hen; the paper reflex happens at the lectern with the patient, the doctor and the scientist as guests; the Optimitron's card knocks the trophy out of the charred winner, who stands at her lectern.
- The living room and its front hall are one plate: the 40-page insert, the meadow ad, the doctor's house call, the outcome label and the panel show all happen round the same couch and the same TV, and the camera travels between them.
- The 212 arrow is a wooden arrow sign (two signs slam into one, then a stamp); 10.7 billion stands in the sky over a field where rows of living humans rise like Part 2's headstones.
- Two new host shots break up the run of plates: the one-for-the-mug reaction cut in the middle of it, and they-make-you-guess (the coin lands on its edge on the lectern) at its end; the old home-planet-board is now two host shots round a 3-second plate.

## Scene 1 · decentralized-fda-title

- id: decentralized-fda-title
- act: Title
- transition_in: cut (the parts are rendered on their own and joined); up from black
- key: 1.2 s into "F.D.A.": a dozen little FDAs perched round the edges of the navy card, the big stamp coming down on the empty middle
- cue: "Your decentralized F.D.A."
- time: 27:54.0 to 27:57.4 (3.4 s)
- voiceover: "Your decentralized F.D.A."
- layer: A, title card
- scene: The period title card (`KIT.titleScene`): the heading on plain navy under the film's emblem. 16:9 lines: `[{ words: ["YOUR", "DECENTRALIZED"], style: "small" }, ["FDA"]]`; 9:16 lines: `[{ words: ["YOUR"], style: "small" }, { words: ["DECENTRALIZED"], style: "small" }, ["FDA"]]`; spoken: `["Your", "decentralized", { cue: "F.D.A.", show: "FDA" }]`. Gag: the FDA decentralizes.
- props: titleScene, stamp
- status: planned

Moves: "Your" → "YOUR" fades in under the emblem. "decentralized" → "DECENTRALIZED" beside it. "F.D.A." → "FDA" lands under them. A beat into "F.D.A." → the FDA cracks into a dozen little "FDA"s that hop off to every edge and corner of the card and perch there like pigeons; the emblem's papers keep running. A beat later → a big rubber stamp comes down on the empty middle where the FDA was, thumps, and lifts: nothing under it, nothing left to approve.

Sound: the projector whirr on "Your"; pops as the little FDAs hop off; a rubber-stamp thunk on the empty middle.

On screen: "YOUR DECENTRALIZED FDA".

No: no APPROVED mark under the stamp (there is nothing to approve).

Why: the narrator reads the heading; the scattering is "decentralized" as a picture.

## Scene 2 · home-planet

- id: home-planet
- act: Wishonia's version
- transition_in: iris in on her face (the title card ends on black)
- key: on "participate.": ticker tape and confetti raining down over the set, the little ticker under its glass dome on the lectern still chattering, a streamer hanging off one antenna, Wishonia carrying on
- cue: "We built ours with"
- time: 27:57.4 to 28:13.8 (16.4 s)
- voiceover: "We built ours with the funding from our version of the treaty, three thousand years ago. Every treatment is tracked in real time. Every outcome is published. Every patient can participate. We don't have a word for "unapproved medicine" because we don't have a bureaucracy that"
- layer: A, host
- scene: The host's set. On the lectern's reading top sits a small brass ticker-tape machine under a glass dome, the kind that prints prices, and a small Wishonian dictionary lies closed beside the mug. She tells us about home; the ticker shows it; then the dictionary shows the word Earth has and her planet does not.
- wishonia: happy-smile + body-presenting on "We", then smirk-smile + body-hand-chest on "three", then happy-smile + body-counting on "Every", then happy-closed + body-wide-gesture on "participate.", then thinking-small + body-thinking on "We" (the second), then skeptical-smile + body-presenting on "bureaucracy"
- props: studio, lectern, mug, ticker (drawn: brass, under a glass dome), dictionary (drawn)
- status: planned

Moves: "We" → the iris opens on her face at the lectern; the camera's slow push begins. "three thousand years ago." → she leans over and blows the dust off the ticker's dome: a big grey puff (it is three thousand years old and still running). "tracked" → the ticker starts chattering and a curl of tape climbs out of it. "published." → it chatters faster, and the tape curls higher out of the dome. "participate." → ticker tape and confetti rain down over the whole set from above the frame, a ticker-tape parade; she keeps talking, a streamer hanging off one antenna. "word" → she flips the dictionary open and holds it up to us; the camera pushes in until the page fills the frame. "medicine" → on the page, "UNAPPETIZING" and right under it "UNARMED", with an empty gap between them; a cricket chirps in the gap. "bureaucracy" → her thumb riffles the pages to B: one entry, "BUREAUCRACY: see EARTH".

Sound: a huff for the dust; the ticker's typewriter chatter on "tracked"; a sparkle as the parade starts; a pat as the book opens; crickets in the gap; a ding on "see EARTH".

On screen: "UNAPPETIZING · UNARMED" / "BUREAUCRACY: see EARTH" (the dictionary page).

Why: she opens the part with the finished system, and the dictionary sets up what Earth has instead.

## Scene 3 · hen-on-safe-bottles

- id: hen-on-safe-bottles
- act: Wishonia's version
- transition_in: cut
- key: after "die.": the FDA official on his heap of SAFE bottles like a hen on eggs, the line in front of him grinning skeletons, still reaching, a bottle rolling out from under him
- cue: "sits on safe treatments"
- time: 28:13.8 to 28:16.7 (2.9 s)
- voiceover: "sits on safe treatments while people die."
- layer: B, plate hen
- scene: One framing on a bare field: a heap of smiling SAFE pill bottles, the FDA official from Part 12 sitting on top of it like a hen on eggs, elbows out like wings, and a short line of patients in front of the heap, chest lights red, reaching for the bottles.
- props: pillBottle, the FDA official (Part 12's), human, KIT.xray
- status: planned

Moves: "sits" → the cut lands on the heap; the official wiggles down onto the bottles and settles, elbows flapping once. "safe" → the camera pushes slowly in. "die." → the line x-rays into grinning skeletons, still in line, still reaching. after "die." → a bottle squeezes out from under him and rolls down the heap; he hooks it back under himself with his shoe and settles again.

Sound: an x-ray zap on "die."; a pop as the bottle squeezes out.

On screen: "SAFE" on the bottles; "FDA" on his badge.

No: no word "BUREAUCRACY" on the plate (the dictionary just said it).

Why: "see EARTH", answered: what Earth's bureaucracy does with safe treatments, in one held image.

## Scene 4 · small-pieces-of-paper

- id: small-pieces-of-paper
- act: Wishonia's version
- transition_in: cut
- key: on "anything.": Wishonia holding one plain paper out at arm's length by a corner, its legs kicking, and the patient, the doctor and the scientist crowded in at her right, every head turned up to the paper
- cue: "You'd call our system"
- time: 28:16.7 to 28:26.8 (10.1 s)
- voiceover: "You'd call our system a decentralized F.D.A. Here's what yours would look like, adjusted for the fact that you require small pieces of paper before you'll do anything."
- layer: A, host
- scene: The host's set, the ticker still chattering quietly, the streamer still on her antenna. Three humans come in as guests at the free wall on her right: the paper reflex.
- wishonia: eyeroll-smile + body-shrug on "You'd", then smirk-smile + body-presenting on "Here's", then skeptical-smile + body-point-right on "small", then smirk-smile + body-point-right on "anything."
- props: studio, lectern, mug, money("plain"), patient, doctor, scientist
- status: planned

Moves: "You'd" → back at the lectern; she shrugs. "Here's" → she reaches under the lectern. "small pieces of paper" → she holds up one plain paper (no seal) by a corner at arm's length, like a dead mouse; its little legs kick. "anything." → the patient, the doctor and the scientist pop up into frame at her right, every head snapping to the paper; she moves it left and three heads follow it; right, and they follow it back. after "anything." → she flicks it off the right edge of the frame; all three dive after it and out of frame; a crash off screen. She picks up her mug.

Sound: a squeak as the paper's legs kick; a whoosh as they dive; a slam for the crash.

On screen: nothing new.

Why: Earth's version has to run on paper, and the heads following it prove it; it also brings the patient, the doctor and the scientist into the part.

## Scene 5 · subsidy-follows-patient

- id: subsidy-follows-patient
- act: Paying patients
- transition_in: cut
- key: on "follow": the patient walking past the trial doors with her medicine-paper puppy trotting at her heel, its "$929" collar tag swinging; behind them, the popped $41,000 bag and the flattened grants officer
- cue: "Eighty percent of the"
- time: 28:26.8 to 28:53.4 (26.7 s)
- voiceover: "Eighty percent of the twenty-seven point two billion dollars will go directly to subsidizing patient participation in pragmatic trials at nine hundred and twenty-nine dollars per patient instead of the usual forty-one thousand dollars. Patients will choose which trials to join; their subsidy will follow them. Treatment developers and providers will get paid for each participant. No grant committees deciding which diseases are fashionable this year."
- layer: B, plate trial-hall
- scene: One long hallway seen side-on, left to right: a mountain of medicine money at the far left; the hallway's mouth, where the patient and a few more patients wait; a desk under a "GRANTS OFFICE" sign in the middle of the floor; a row of trial doors, a germ on each door's sign and a tally under it, a doctor leaning in each doorway and the scientist in one; at the far right, the grant committee's long table. The camera travels with the money from left to right.
- props: money("med"), money("plain"), priceTag, door, sign, germ, scientist, patient, human, moneybag (drawn), ✗ (drawn)
- status: planned

Moves: "Eighty" → the mountain of medicine money (cross seals) at the hallway's left end, a tag on a string, "$27.2 BILLION"; the plain paper Wishonia flicked flutters down from the top of the frame and lands on its peak like the star on a tree. "percent" → most of the pile (four papers in five) stands up on stick legs; the lead paper waves a little flag, "80%". "directly" → the herd stampedes right and the camera travels with it: the grants officer at his desk holds up his palm, is trampled flat with a trail of tiny footprints across him, and blinks. "subsidizing" → at the hallway's mouth, one paper peels off the herd and sits at the patient's feet like a puppy, a back leg kicking. "nine hundred and twenty-nine" → the camera pushes in: the tag on its collar swings round, "$929". "forty-one thousand" → a bloated money bag waddles in beside it on stub legs, tagged "$41,000", wheezing. "dollars." (the last) → the bag pops like a balloon: 44 puppy papers spill out and scamper off down the hall, one to each of 44 more patients. "choose" → the patient walks along the doors, looking at each germ, and picks one. "follow them." → her puppy trots at her heel. "Treatment developers" → in her door stands the scientist (cast), clipboard out. "paid" → the puppy jumps up into the scientist's hand. "participant." → the tally under her door ticks up, and so does every other door's as the other puppies arrive; the patient goes in and the door shuts. "No grant committees" → the camera travels on to the far end: the committee from committee-8-years (Part 12) at its long table under a "GRANT COMMITTEE" sign, turning pages; a giant red ✗ drops on the table like an anvil and flattens them. "fashionable" → from under the ✗, one flattened arm pokes up holding a germ by a strap like a handbag, and strikes a pose. after "year." → the germ blows a kiss.

Sound: a pop as the herd stands up; little pat footsteps for the stampede and a splat for the grants officer; a boing as the puppy sits; a pop as the bag bursts; a cash-register ding as the puppy pays; a falling slide whistle and a slam for the ✗; a sparkle on the germ; a squeak for the kiss.

On screen: "$27.2 BILLION" / "80%" / "GRANTS OFFICE" / "$929" / "$41,000" / "GRANT COMMITTEE".

Why: the money goes where the patient goes, not where a committee points, and the burst bag shows the same money paying for 44 patients (it sets up the 44.1 in life-jackets-handed-out).

## Scene 6 · clinical-terrarium

- id: clinical-terrarium
- act: Paying patients
- transition_in: cut
- key: on "pharmaceutical": the fat cat holding the patient up in his tweezers, looking at her red chest light, the identical tidy humans smiling behind the glass of the lizard tank
- cue: "Instead of testing drugs"
- time: 28:53.4 to 29:05.1 (11.7 s)
- voiceover: "Instead of testing drugs on two hundred humans selected by pharmaceutical companies in clinical terrariums, you'll test on real patients in real hospitals. Where the diseases are."
- layer: B, plate terrarium
- scene: A lab bench on a plain floor holding a glass tank set up like a lizard terrarium (a heat lamp, a water dish, a plastic plant), full of identical tidy little humans; to its right, a row of three real hospitals. The camera starts on the tank and travels along the hospitals.
- props: lab, hospital, diseaseBlob, richHuman, patient, KIT.person({ plain: true }) (the tidy humans)
- status: planned

Moves: "Instead" → the tank on the bench: tidy little humans who are all the same (the plain build, the same gown, the same smile, every chest light off) sitting under the heat lamp. "two hundred humans" → a pet-shop price sticker on the glass: "200". "selected" → the fat cat (cast) leans in over the bench with long tweezers and drops in one more tidy human. "pharmaceutical" → the patient (scarf, chest light blinking red) has climbed up the bench leg; he plucks her up with the tweezers, holds her to his monocle, sees her chest light, and flicks her away; she sails out of frame and lands in a heap. "real patients" → the glass lifts off; he gapes. "real hospitals." → the tidy humans file off the bench and into the hospitals; the patient picks herself up and walks in with them. "Where" → the camera travels along the hospital windows. "diseases are." → in every window a disease blob looms smugly over a bed; each one turns to see the testers walking in, and goes from smug to scared. after "are." → one blob climbs out of a back window and runs.

Sound: a snip of the tweezers on "selected"; a whistle as she is flicked and a boing as she lands; a rising slide whistle as the glass lifts; a yelp from the blobs.

On screen: "200" (the sticker); "HOSPITAL" on the buildings.

Why: trials move to where the sick people are, and the tweezers show who they used to leave out.

## Scene 7 · life-jackets-handed-out

- id: life-jackets-handed-out
- act: Paying patients
- transition_in: cut
- key: on "hand out": life jackets flying off the conveyor down the whole line, the swimmers bobbing up like corks, the patient catching hers, the lifeguard flat in his chair under the stamp mark
- cue: "The whole thing will"
- time: 29:05.1 to 29:26.5 (21.4 s)
- voiceover: "The whole thing will use your new decentralized F.D.A. protocol, reducing trial costs by forty-four point one times and funding twenty-three point four million patients per year (versus the current one point nine million patients per year). Remember that billion patients drowning in line for two life jackets? Your decentralized F.D.A. will hand out twenty-three point four"
- layer: B, plate beach
- scene: Part 12's beach from lifeguard-cabinet: the lifeguard on his tall chair at the waterline, a post with a hook holding two life jackets, and the line of swimmers in the water running out to the horizon, grinning skulls bobbing among them. The protocol stamp flattens the lifeguard, and a conveyor of life jackets runs out along the whole line. (The approval cabinet is not on the beach in this part: it opens in two-hundred-twelve-years-sooner.)
- props: stamp, stampMark, priceTag, conveyor, patient, human, life-jacket (drawn), KIT.person skeleton (the skulls)
- status: planned

Moves: "The whole thing" → the beach as Part 12 left it: the lifeguard (a beanpole in a striped tank top, zinc on his nose, sunglasses, a whistle) up on his chair flipping his binder; the two jackets on the hook, a price tag "$41,000" hanging from one. "protocol," → a giant rubber stamp drops out of the sky onto the chair and flattens him into the seat; when it lifts, he is printed over with a red "DECENTRALIZED FDA PROTOCOL" mark, blinking. "forty-four point one" → the camera pushes in on the tag: it deflates with a squeal to a tiny tag, "$929". "twenty-three point four million" (the first) → the camera pulls back: a conveyor rolls out from the hook along the waterline, stacked with life jackets, a counter on its side rolling up to "23.4 MILLION". "one point nine million" → the hook's old little counter, "1.9 MILLION", shrinks beside it. "Remember" → the camera travels along the line of swimmers: the near ones drawn humans with their hats and hairdos, the far ones dots, grinning skulls bobbing politely among them. "drowning" → down the line, heads bob under and back up. "jackets?" → the nearest swimmer strains for the hook. "hand out" → the conveyor runs: life jackets fly off it down the whole line, one per head, and every swimmer pops up high in the water like a cork; the patient (scarf) catches hers mid-air. "four" (the last) → the jackets keep flying to the horizon; the skulls get jackets too, a little late, and bob along, still grinning; one jacket sails on over the horizon (it lands in one-for-the-mug).

Sound: a rubber-stamp thunk and a splat for the lifeguard; a falling slide whistle as the tag deflates; the conveyor's whirr as it rolls out; a pop and a boing as the jackets fly and the swimmers bob up.

On screen: "$41,000" → "$929" / "DECENTRALIZED FDA PROTOCOL" (the stamp mark) / "23.4 MILLION" / "1.9 MILLION".

No: no 44.1× on screen; the deflating tag is the 44.1.

Why: pays off Part 12's lifeguard with the new number.

## Scene 8 · one-for-the-mug

- id: one-for-the-mug
- act: Paying patients
- transition_in: cut
- key: after "million.": a life jacket sitting snug round Wishonia's coffee mug on the lectern, her hand patting it, her eyes on the camera
- cue: "million. This"
- time: 29:26.5 to 29:28.1 (1.6 s)
- voiceover: "million."
- layer: A, host (reaction cut)
- scene: The host's set, the mug on the lectern. One of the jackets from the beach flies all the way to the studio.
- wishonia: happy-smile + body-palms-down
- props: studio, lectern, mug, life jacket (drawn as in life-jackets-handed-out)
- status: planned

Moves: "million." → cut to the lectern: a life jacket sails in from the left edge of the frame and drops neatly round her coffee mug. after "million." → she pats it and looks at the camera, pleased.

Sound: a whoosh as the jacket flies in; a pat after "million.".

On screen: nothing lettered.

Why: breaks up the long run of plates with a one-second reaction, and 23.4 million is enough jackets to reach the studio.

## Scene 9 · accordion-timeline

- id: accordion-timeline
- act: Faster treatments
- transition_in: cut
- key: on "thirty-six": the line squeezed up to the window, the beards gone, the wait sign's wheels clanking to "36 YEARS"
- cue: "This will increase the"
- time: 29:28.1 to 29:37.4 (9.2 s)
- voiceover: "This will increase the treatment discovery rate twelve point three times, compressing that about four hundred and forty-three years wait to about thirty-six years."
- layer: B, plate queue
- scene: Part 9's ticket window in its long wall, the wait sign over it on "443 YEARS", and the roped queue zigzagging away between brass posts. Further along the same wall stand Part 9's warehouse shelf (left of the window) and the approval cabinet from Part 12 (right of it), for two-hundred-twelve-years-sooner.
- props: sign (the wait sign), pillBottle, germ, patient, human, KIT.person skeleton
- status: planned

Moves: "This" → the window, the sign on "443 YEARS", and the queue: humans walking their diseases on leashes, chest lights red, the back of the line grey and bearded, then grinning skeletons still holding their leashes. The patient is a third of the way back, ticket in hand. "twelve point three" → the window's shutter flies up and down so fast it blurs, spitting teal bottles to the front of the line; a tag on it flips to "12.3×". "compressing" → the brass posts slam together like an accordion and the zigzag folds up toward the window; the grey humans' beards zip back up into their chins like tape measures, and the skeletons at the back are squeezed forward too, rattling. "forty-three" → the wait sign shakes on 443. "thirty-six" → its digit wheels spin down and clank to "36 YEARS"; the patient is near the front now.

Sound: the shutter's whirr; a huff as the line squeezes; a clank as the wheels stop.

On screen: "12.3×" / "443 YEARS" → "36 YEARS".

No: no timeline bar; the line is the timeline.

Why: the speed-up as a line that gets shorter.

## Scene 10 · two-hundred-twelve-years-sooner

- id: two-hundred-twelve-years-sooner
- act: Faster treatments
- transition_in: continues on the plate (no seam)
- key: on "two hundred and twelve": the two arrow signs slammed into one fat arrow sign stamped "212 YEARS SOONER", the approval cabinet standing open behind it, the patient hugging her SAFE bottle
- cue: "Two things will save"
- time: 29:37.4 to 30:02.7 (25.3 s)
- voiceover: "Two things will save lives. First, finding treatments faster: treatments that would have sat undiscovered for centuries will get found two hundred and four years sooner on average. Second, eliminating the eight point two years bureaucratic delay between proving a drug is safe and letting dying humans take it. Combined, treatments will reach patients two hundred and twelve years sooner on average."
- layer: B, plate queue
- scene: The same plate, squeezed. Two wooden arrow signs spring up by the window. The camera travels left to the warehouse shelf, where a dusty bottle is found, then right to the approval cabinet, which bursts open, then pulls back while the two signs become one.
- props: sign (two arrow signs, then one fat one), stamp, pillBottle, padlock, glass cabinet and hourglass (as Part 12 draws them), KIT.person skeleton, patient, human
- status: planned

Moves: "Two" → the first frame is accordion-timeline's last. "things" → two blank wooden arrow signs spring up out of the ground by the window, both pointing at the front of the line. "First," → the camera travels left along the wall to Part 9's warehouse shelf: a dusty bottle in a cobweb, wearing its "NEVER TESTED FOR THIS" tag, a spider hanging over it. "centuries" → the spider, which has grown a long white beard, yawns. "found" → a flashlight beam lands on the bottle; it shakes off its dust, the tag flips to a teal tick, and it hops off the shelf and runs for the front of the line. "two hundred and four" → the camera travels back with it: arrow sign 1 gets its lettering, "204 YEARS SOONER". "Second," → the camera travels on, past the window, to the approval cabinet from committee-8-years: the hourglass on top on "8.2 YEARS", the padlock on the hasp, the SAFE bottle on the top shelf, the life preserver on the bottom shelf, the handprint on the glass, and YOU's skeleton (bowler on) slumped against it, palm on the glass. "eliminating" → the hourglass bursts and sprays sand, the padlock pops off, and the glass door swings open. "dying" → the SAFE bottle hops out and runs for the line, past the slumped skeleton, which lifts a bony hand for it eight years late. "take it." → the patient catches the bottle and hugs it; arrow sign 2 gets its lettering, "8.2 YEARS SOONER". "Combined," → the camera pulls back over the whole line; the two arrow signs slam together into one fat arrow sign. "two hundred and twelve" → a rubber stamp comes down on it: "212 YEARS SOONER". after "average." (the last) → the whole line cheers and throws its hats in the air; one skeleton throws its skull by mistake and catches it.

Sound: a pop as the signs spring up; a huff of dust and a sparkle as the tag flips; a clank as the padlock pops; a boing as the bottle hops; a rubber-stamp thunk on "twelve"; a pop as the hats go up.

On screen: "NEVER TESTED FOR THIS" (the tag) / "204 YEARS SOONER" / "8.2 YEARS" / "8.2 YEARS SOONER" / "212 YEARS SOONER".

No: no plus sign or sum written out; the signs slamming together are the sum.

Why: the two gains added up, so the 212 is earned on screen.

## Scene 11 · plans-for-tuesday

- id: plans-for-tuesday
- act: Faster treatments
- transition_in: cut
- key: after "Tuesday.": the front row holding up their desk calendars with ticked sticky notes, the crowd behind them to the horizon, the dentist man groaning, "10,700,000,000" in the sky
- cue: "That timeline shift will"
- time: 30:02.7 to 30:12.3 (9.5 s)
- voiceover: "That timeline shift will prevent ten point seven billion deaths. Those are individual humans who currently have plans for next Tuesday."
- layer: B, plate tuesday-field
- scene: The-toll's field from Part 2, the other way round: a plain field under a cream sky, the horizon low. The number stamps into the sky; then, where Part 2 grew headstones, rows of living humans rise out of the ground to the horizon, each holding up a desk calendar.
- props: calendar, grandma, pillBottle, patient, human
- status: planned

Moves: "That" → the empty field, the camera low and close. "billion" → "10,700,000,000" stamps into the sky. "deaths." → HOLD: nothing moves until "individual". "individual" → row after row, from the front to the horizon, humans rise out of the field (the near ones drawn humans of every build and hat, the far ones dots), every one holding up a desk calendar open on "TUE"; the camera pulls back as they rise. "plans" → the camera pushes in on the front row: a sticky note lands on each calendar: the patient (scarf, her SAFE bottle under one arm) "KID'S RECITAL", grandma (cast) "BINGO", a barrel-shaped man in a cardigan "FISHING", a box-shaped man in a suit "DENTIST". "Tuesday." → each note gets a small teal tick. after "Tuesday." → the dentist man reads his note and groans; everyone else beams.

Sound: a thunk as the number lands; then silence for the HOLD; a pop as the rows rise; a pat as the notes land; a sparkle for the ticks; a huff for the groan.

On screen: "10,700,000,000" / "TUE" / "KID'S RECITAL" · "BINGO" · "FISHING" · "DENTIST".

Why: turns the biggest number in the part back into people, and the dentist is the proof they are alive.

## Scene 12 · smoke-detector-live

- id: smoke-detector-live
- act: Real-time safety monitoring
- transition_in: cut
- key: on "BEFORE": the patient reading her bottle's lit side panel with the cap still on; above her on the kitchen wall, the live detector, the old one flattened under it with only its mailbox flag sticking out
- cue: "Real-Time Safety Monitoring."
- time: 30:12.3 to 30:30.7 (18.4 s)
- voiceover: "Real-Time Safety Monitoring. Remember Vioxx and the smoke detector that works by mail? Your new system will collect every side effect automatically in real time. You'll know "twelve percent got headaches, three percent were severe" BEFORE you take the pill, not after the class action lawsuit."
- layer: B, plate kitchen
- scene: The patient's 1950s kitchen, side-on: a wall with the old smoke detector up near the ceiling, a counter under it, a window, the back door on the right. The camera starts on the detector and tilts down to the counter.
- props: pillBottle, sign, smoke-detector (as Part 12 draws it), lawyer, patient
- status: planned

Moves: "Real-Time" → the kitchen wall: Part 12's smoke detector, still charred black, holding up its singed letter; it starts writing another with a little pen. "mail?" → its mailbox flag pops up. "automatically" → a new detector with a little live screen slams onto the wall on top of it and flattens it; only the mailbox flag sticks out from under, then droops. "real time." → the screen blinks on and a wavy reading line starts scrolling across it. "twelve percent" → the camera tilts down to the counter: the patient (scarf, chest light red) holds up her SAFE bottle; a panel on its side lights up, "HEADACHES 12%". "three percent" → under it, "SEVERE 3%". "BEFORE" → she reads it with the cap still on, rubs her temple at the 12%, and nods. "class" → the lawyer bursts in through the back door waving an "INJURED?" sign; nobody is. "lawsuit." → he reads the panel over her shoulder, and his "INJURED?" sign wilts on its stick like a dead flower.

Sound: a pen scratch as the detector writes; a squeak as the flag goes up; a slam as the live detector lands; a switch as its screen blinks on; a ding for each number; pat footsteps for the lawyer; a falling slide whistle as his sign wilts.

On screen: "HEADACHES 12%" · "SEVERE 3%" / "INJURED?".

Why: fixes the detector that works by mail, and puts the numbers on the bottle before the pill.

## Scene 13 · they-make-you-guess

- id: they-make-you-guess
- act: Real-time safety monitoring
- transition_in: cut
- key: after "guess.": the coin standing on its edge on the lectern next to the FDA bottle with its blank panel, Wishonia side-eyeing the camera
- cue: "The F.D.A. doesn't publish"
- time: 30:30.7 to 30:35.0 (4.3 s)
- voiceover: "The F.D.A. doesn't publish these numbers at all. They make you guess."
- layer: A, host
- scene: The host's set. Wishonia holds up the FDA's own bottle: a plain bottle labeled "FDA" with a blank side panel. Then she flips a coin for it.
- wishonia: skeptical-smile + body-presenting on "The", then smirk-closed + body-palms-down on "They", then sideeye-closed + body-idle on "guess."
- props: studio, lectern, mug, pillBottle (label "FDA", a blank panel), coin (drawn)
- status: planned

Moves: "The" → cut to the lectern: she holds up the FDA bottle. "numbers" → she taps its side panel: blank. "They" → she sets it down and flips a coin over it. "guess." → the coin lands on its edge on the lectern and stays standing. after "guess." → she looks from the coin to the camera, side-eye.

Sound: a ding as the coin flips; a tick as it lands on its edge.

On screen: "FDA" (the bottle's label).

Why: a verdict told to the camera, and a guess that cannot even come down heads or tails.

## Scene 14 · decision-wheel

- id: decision-wheel
- act: Treatment rankings
- transition_in: cut
- key: after "vibes.": the wheel clicked to a stop on DONUTS, the doctor handing the patient a donut, the lobbyist and the fat cat at the edges
- cue: "Treatment Rankings. Currently,"
- time: 30:35.0 to 30:49.4 (14.4 s)
- voiceover: "Treatment Rankings. Currently, your doctor picks treatments based on: that drug rep who brought good donuts in two thousand and three, something they half-remember from medical school, whatever the insurance company allows, and vibes."
- layer: B, plate exam-room
- scene: A doctor's exam room, side-on: the exam table with the patient on it in a paper gown, a window behind, and a carnival prize wheel on a stand with four dark slices. The camera starts wide and pushes in on each slice as it lights.
- props: stamp, lobbyist, richHuman, doctor, patient, prize-wheel (drawn), donut box (drawn)
- status: planned

Moves: "Treatment" → the exam room: the patient on the exam table, scarf on, chest light blinking red; the doctor (head mirror, stethoscope) steps up to the prize wheel. "donuts" → slice 1 lights up, "DONUTS (2003)"; the lobbyist (cast) tiptoes in behind the doctor and slips a box of donuts under his arm. "half-remember" → slice 2, "HALF-REMEMBERED LECTURE"; a thought bubble over the doctor shows a chalkboard, half erased. "insurance company" → slice 3, "WHAT INSURANCE ALLOWS"; the fat cat (cast) leans in through the window and thumps a "DENIED" stamp onto the patient's chart. "vibes." → slice 4, "VIBES"; the camera pulls back; the doctor licks a finger, holds it up to the wind, and spins the wheel. after "vibes." → it clicks to a stop on DONUTS; he hands the patient a donut and writes her a prescription.

Sound: a ding as each of the first two slices lights; a rubber-stamp thunk for DENIED; the wheel's whirr; a click as it stops.

On screen: "DONUTS (2003)" · "HALF-REMEMBERED LECTURE" · "WHAT INSURANCE ALLOWS" · "VIBES" / "DENIED".

Why: how treatments get picked today, as a game of chance.

## Scene 15 · grape-soda

- id: grape-soda
- act: Treatment rankings
- transition_in: cut
- key: after "grape." (the last): the grape sticker fluttering into Wishonia's mug, the can's label under it reading "0% GRAPE"
- cue: "This is called evidence-based"
- time: 30:49.4 to 30:57.1 (7.7 s)
- voiceover: "This is called "evidence-based medicine," which contains the word "evidence" the same way "grape soda" contains the word "grape."."
- layer: A, host
- scene: The host's set. Wishonia holds up the doctor's donut (with its prescription tag tied on), then a can of grape soda with one very small, clearly fake grape on the label.
- wishonia: skeptical-smile + body-presenting on "This", then smirk-smile + body-presenting on "soda", then smirk-closed + body-hands-hips on "word" (the second)
- props: studio, lectern, mug, donut with a prescription tag (drawn), soda can (drawn)
- status: planned

Moves: "This" → cut to the lectern: she holds up the doctor's donut, a prescription tag tied to it with string. "evidence" → she sets the donut down. "soda" → she lifts a plain can, "GRAPE SODA", with one very small, clearly fake grape on its label. "grape." (the last) → the camera pushes in on the grape. after "grape." → it is a sticker: it peels off and flutters into her coffee mug; under it the label reads "0% GRAPE".

Sound: a pop as the can comes up; a squeak as the sticker peels and a small splat in the mug.

On screen: "GRAPE SODA" / "0% GRAPE".

Why: a dry joke told to the camera, with the donut from decision-wheel as its exhibit.

## Scene 16 · ranked-treatments

- id: ranked-treatments
- act: Treatment rankings
- transition_in: cut back to the plate as decision-wheel left it
- key: on "it:": the flip board standing on the flattened prize wheel, three bottles in order with their rows of tiny humans, the patient dropping her donut and holding her SAFE bottle up to row 1
- cue: "Your decentralized F.D.A. will rank"
- time: 30:57.1 to 31:03.9 (6.8 s)
- voiceover: "Your decentralized F.D.A. will rank every treatment by what actually happened to real humans who took it:"
- layer: B, plate exam-room
- scene: Back in the exam room. A tall flip board, like a train-station departures board, drops onto the prize wheel and crushes it; pill bottles clack into order by what happened to the humans who took them, best on top.
- props: pillBottle, ranking board (drawn), patient, doctor, human, KIT.person skeleton
- status: planned

Moves: "Your" → the exam room as decision-wheel left it: the wheel stopped on DONUTS, the patient on the exam table holding her donut. "rank" → a tall flip board drops from the top of the frame onto the prize wheel and crushes it flat; one slice spins away across the floor. Its flaps clack, and three pill bottles shuffle into order, best on top. "actually happened" → beside each bottle, a row of tiny humans who took it pops up: row 1 standing and cheering, row 3 mostly grinning skeletons. "it:" → the patient drops the donut, pulls her SAFE bottle out of her gown pocket and holds it up to row 1: the same bottle.

Sound: a slam as the board lands and the typewriter clack of its flaps; a tick as the rows pop up; a ding as she holds her bottle up.

On screen: "1 · 2 · 3" (the rows).

No: no figures on the board; the tiny humans are the ranking.

Why: what replaces the prize wheel.

## Scene 17 · forty-page-insert

- id: forty-page-insert
- act: Outcome labels
- transition_in: cut
- key: on "doctor.": the patient buried to the chin on the couch, the insert running across the floor and through the doorway, the doctor in the doorway wiping his shoes on it like a doormat, and the lawyer at the hall table still writing its far end
- cue: "Outcome Labels. Food has"
- time: 31:03.9 to 31:16.2 (12.3 s)
- voiceover: "Outcome Labels. Food has nutrition labels. Cigarettes have warning labels. Drugs have forty-page inserts written by lawyers having seizures, which nobody reads, including your doctor."
- layer: B, plate living-room
- scene: The patient's living room and front hall, side-on, left to right: a window over the couch, a coffee table in front of it, a console TV with rabbit ears, a doorway into the front hall, a telephone table with a rotary phone, and the front door. The insert unfolds from the coffee table, across the floor, through the doorway and up onto the telephone table, where the lawyer is still writing it. This plate carries the rest of the part's plates, through louder-wins.
- props: tvSet, phone, door, pillBottle, lawyer, doctor, patient, cereal box and cigarette pack (drawn, plain), insert (drawn)
- status: planned

Moves: "Outcome" → the coffee table: a plain cereal box, a plain cigarette pack by an ashtray and a plain pill box; the patient on the couch behind them, scarf on, chest light red. "nutrition" → the cereal box turns to show its side, "NUTRITION FACTS". "warning" → the cigarette pack turns, "WARNING", with a small skull. "forty-page" → she opens the pill box: the insert unfolds, and unfolds, and unfolds, off the table, up over her and across the floor, until only her head and scarf stick out of the heap; its top fold reads "PAGE 1 OF 40". "lawyers" → the camera travels along the insert through the doorway into the front hall: its far end climbs the telephone table and runs under the pen of the lawyer, standing at the table, still writing it in tiny scribbles. "seizures," → his pen hand jitters so hard the scribbles turn into zigzags and the table rattles. "nobody reads," → the camera pulls back to take in the whole insert, couch to table. "doctor." → the doctor, his bag in hand, stops in the doorway, wipes his shoes on the insert like a doormat without looking down, checks his watch, and goes back out of the front door.

Sound: a click as each box turns; a whoosh and a pat of paper as the insert unfolds; a pen scratch for the lawyer and the typewriter rattle as he jitters; a pat as the doctor wipes his feet.

On screen: "NUTRITION FACTS" / "WARNING" / "PAGE 1 OF 40".

Why: the problem, told with things in the viewer's own living room.

## Scene 18 · meadow-ad

- id: meadow-ad
- act: Outcome labels
- transition_in: continues on the plate (no seam)
- key: on "death,": the TV screen filling the frame, "DEATH" crawling past along its bottom the same size as everything else, the meadow woman mid-skip as a grinning skeleton in her sun hat, daisies still in hand
- cue: "Your television advertisements show"
- time: 31:16.2 to 31:36.4 (20.2 s)
- voiceover: "Your television advertisements show a smiling human frolicking through a meadow while a voiceover lists ways the drug might kill you at auctioneer speed. The meadow human does not react to the word "stroke." Side effects include "death," listed between "constipation" and "mild rash," as if your organs failing is roughly as inconvenient as dry skin."
- layer: B, plate living-room
- scene: The same living room. The TV is on: a drug ad, a smiling woman skipping through a meadow while small fast text crawls along the bottom of the screen; on "death" she turns into a grinning skeleton and keeps skipping. The camera pushes into the TV and comes back out.
- props: tvSet, KIT.xray, patient, human
- status: planned

Moves: "Your" → the camera travels back from the hall to the TV, the patient still buried to the chin on the couch, watching. On the screen: a smiling hourglass woman in a sundress and a sun hat, holding daisies, in a meadow. "frolicking" → the camera pushes into the TV screen; she skips through the meadow, smile fixed. "voiceover" → a crawl of small text starts along the bottom of the screen. "auctioneer" → the crawl speeds up to a blur and the rabbit ears wiggle into the top of the frame. "stroke." → STROKE crawls past; her smile does not move. "death," → DEATH crawls past, the same small size as everything else; she x-rays into a grinning skeleton mid-skip, sun hat and daisies and all, and keeps skipping. "constipation" → CONSTIPATION crawls past just ahead of it. "mild" → MILD RASH: red spots pop out on the skeleton. "skin." → the skeleton scratches its elbow bone and keeps skipping. after "skin." → the camera pulls back out of the TV: on the couch, the patient's head, sticking out of the insert, turns slowly to the camera.

Sound: a boing per skip (two); the typewriter clack as the crawl starts and again at auctioneer speed; crickets after "stroke."; an x-ray zap on "death,"; a pop for the rash; a scratch for the elbow.

On screen: the crawl, "may cause: stroke · constipation · death · mild rash · dry skin".

Why: today's label, the way viewers actually see it, with the horror the ad leaves out.

## Scene 19 · ask-your-doctor

- id: ask-your-doctor
- act: Outcome labels
- transition_in: continues on the plate (no seam)
- key: after "hallway.": the doctor on roller skates at the hall telephone table, its little screen showing a grinning skull, rolling slowly backwards out of the front door, the egg timer on "7 MIN"
- cue: "The label says individual"
- time: 31:36.4 to 31:51.1 (14.7 s)
- voiceover: "The label says "individual results may vary," meaning outcomes range from "cured" to "deceased" (both technically qualifying). It also says "ask your doctor," but your doctor has seven minutes per appointment and just Googled your condition in the hallway."
- layer: B, plate living-room
- scene: The same living room. The ad's end card on the TV, then the doctor's house call in the front hall.
- props: tvSet, gauge, stampMark, phone, door, doctor, patient, KIT.person skeleton, egg timer (drawn), roller skates (drawn)
- status: planned

Moves: "The" → the first frame is meadow-ad's last: the patient looking at the camera from the heap. The TV cuts to the ad's end card: "INDIVIDUAL RESULTS MAY VARY". "individual" → the camera pushes into the TV. "cured" → a dial (gauge, mount "dial") on the card runs from "CURED" to "DECEASED"; its needle swings to CURED, and a tick appears there. "deceased" → the needle swings to DECEASED, and a tick appears there too. "qualifying)." → "QUALIFIES" stamps onto both; the skeleton from the ad skips back in, gives a bony thumbs-up, and skips off. "ask" → the camera pulls out of the TV and travels to the front hall: the doctor zips in through the front door on roller skates, a stopwatch in his hand. "seven minutes" → he slaps a kitchen egg timer onto the telephone table: "7 MIN"; it starts ticking. "Googled" → he types on the rotary phone, which has a little screen: a plain search box, "RED CHEST LIGHT". "hallway." → the result is a grinning skull; he goes pale, looks through the doorway at the patient on the couch, and rolls slowly backwards out of the front door.

Sound: a click as the end card comes up; a ding at each end of the dial; a rubber-stamp thunk for QUALIFIES; a whoosh as the camera pulls out; a tick as the egg timer goes down; the typewriter clack as he types; a falling slide whistle as he rolls back.

On screen: "INDIVIDUAL RESULTS MAY VARY" / "CURED" · "DECEASED" · "QUALIFIES" / "7 MIN" / "RED CHEST LIGHT".

Why: why "ask your doctor" does not fix the label.

## Scene 20 · outcome-label

- id: outcome-label
- act: Outcome labels
- transition_in: continues on the plate (no seam)
- key: after "happens." (the last): the label flat on the patient's SAFE bottle on the coffee table, her chest light just turned teal, the loud human gagged by his own sticker at the window, the lawyer buried under his insert with only his briefcase sticking out
- cue: "Your new system will produce"
- time: 31:51.1 to 32:04.5 (13.4 s)
- voiceover: "Your new system will produce Outcome Labels that tell you what actually happens when real humans take a drug. Not what a marketing department hopes happens. Not what a lawyer is comfortable admitting happens. What happens."
- layer: B, plate living-room
- scene: The same living room. A clean label, laid out like a nutrition label, slides onto the patient's SAFE bottle; the loud human and the lawyer each try to cover it with their own and get it back in the face. She reads it, takes the pill, and gets better.
- props: pillBottle, loudHuman, lawyer, patient, outcome label (drawn), insert (drawn)
- status: planned

Moves: "Your" → the camera travels back from the hall to the couch: the patient digs her SAFE bottle out of the heap and stands it on the coffee table; its side panel from smoke-detector-live is still lit. "Labels" → a clean label, laid out like a nutrition label, slides in and stops over the bottle: "OUTCOME LABEL". "humans" → its three bars fill with tiny humans: "GOT BETTER", "NO CHANGE", "SIDE EFFECTS". "department" → the loud human (cast: a megaphone for a head) leans in through the window and slaps a "MIRACLE!" sticker over the label. "hopes" → the sticker peels itself off and slaps over the mouth of his megaphone; he can only squeak. "lawyer" → the lawyer comes in from the hall and tapes his 40-page insert over the label. "admitting" → the tape lets go; the insert unfolds off the bottle onto him and buries him; only his briefcase sticks out. "What" (the last) → the label snaps flat onto the bottle. "happens." (the last) → the patient reads it, pops the cap and takes the pill. after "happens." → her chest light flips from red to teal; she smiles, loosens her scarf, and kicks off the rest of the insert.

Sound: a whoosh as the label slides in; a pop as the bars fill; a splat for the sticker; a squeak from the gagged megaphone; a snip as the tape lets go and a pat of paper as the insert buries the lawyer; a thunk as the label snaps flat; a sparkle as her light turns teal.

On screen: "OUTCOME LABEL" / "GOT BETTER" · "NO CHANGE" · "SIDE EFFECTS" / "HEADACHES 12%" · "SEVERE 3%" / "MIRACLE!".

No: no invented numbers on the label; the bars carry tiny humans, not figures.

Why: the fix, as something the viewer can read, and the patient's story ends in the teal light.

## Scene 21 · louder-wins

- id: louder-wins
- act: The Optimitron
- transition_in: continues on the plate (no seam)
- key: after "louder.": the TV screen filling the frame, both panelists charred black and smoking, hair straight up, still shouting into megaphones; the trophy in one's hands, his tie flickering red and blue
- cue: "Your decentralized D.F.D.A. figures"
- time: 32:04.5 to 32:19.8 (15.3 s)
- voiceover: "Your decentralized D.F.D.A. figures out which treatments work. But your governments also need to know which *policies* work, how much to spend on what, which laws to keep, which to throw away. Your current method is to argue about it on television until someone wins by being louder."
- layer: B, plate living-room
- scene: The same living room, the patient well. Then the TV: a panel show, two politicians shouting across a desk piled with papers, a loudness meter between them; the meter pins and blows up, and the louder one gets the trophy anyway.
- props: tvSet, gauge, politician, KIT.nuke, KIT.boom, trophy (drawn), megaphone (drawn), patient, pillBottle
- status: planned

Moves: "Your" → the patient on the couch, chest light teal, scarf loose, her labeled SAFE bottle on the coffee table. "work." → she pats the bottle and it smiles back. "policies" → the TV clicks over to a panel show and the camera pushes into it until the screen fills the frame: two politicians (cast) at a long desk piled with papers, one in a red tie and one in a blue tie. "keep," → one pulls a paper to his chest. "away." → the other tosses one over his shoulder. "argue" → both grab megaphones and shout across the desk; a loudness meter (gauge) stands between them. "television" → the rabbit ears shake into the top of the frame. "wins" → the needle swings back and forth, harder and harder. "louder." → it pins and bursts: a white flash, a boom and a small mushroom cloud over the desk. after "louder." → the smoke clears on both panelists charred black and smoking, hair straight up, still shouting into their megaphones; a trophy, "WINNER (LOUDEST)", drops into one's hands; his charred tie flickers red, blue, red.

Sound: a switch as the TV clicks over; two yelps as they shout; the needle's whirr; a boom; a bell for the trophy.

On screen: "WINNER (LOUDEST)".

No: no party names or flags; the ties are the teams.

Why: the current method, so the Optimitron has something to replace.

## Scene 22 · optimitron-appliance

- id: optimitron-appliance
- act: The Optimitron
- transition_in: cut
- key: on "laws.": card 2 shooting out of the Optimitron across the set into the charred winner's trophy, card 1 standing in the slot, both dials up, the mug down
- cue: "Back home, the Optimitron"
- time: 32:19.8 to 32:39.5 (19.7 s)
- voiceover: "Back home, the Optimitron handles this. It's an appliance. You plug in what ten thousand jurisdictions tried, it tells you which policies actually made people richer or less dead. Its Optimal Budget Generator does budgets; its Optimal Policy Generator does laws."
- layer: A, host
- scene: The host's set. The Optimitron sits on the lectern like a toaster. At the free wall on her right stands the charred winner from louder-wins, still shouting silently into his megaphone, the trophy under his arm. A card stack goes into the Optimitron's slot, two policy cards pop out like toast, and the second one flies.
- wishonia: happy-smile + body-presenting on "Back", then smirk-closed + body-idle on "handles" (the mug at her lips), then smirk-smile + body-presenting on "appliance.", then happy-smile + body-counting on "richer", then excited-oh + body-excited on "Policy", then smirk-smile + body-hands-hips on "laws."
- props: studio, lectern, mug, optimitron, politician (charred), trophy (drawn), megaphone (drawn), card stack (drawn)
- status: planned

Moves: "Back" → cut to the lectern; at her right the charred winner shouts into his megaphone, no sound coming out, the trophy under his arm. "Optimitron" → the Optimitron sits on the lectern like a toaster, two big dials, HEALTH and WEALTH; she pats it. "handles" → she sips her coffee. "appliance." → she puts the mug down slowly; the Optimitron's window glows and its face smiles. "jurisdictions" → a fat stack of cards banded "10,000 JURISDICTIONS" drops into its toaster slot. "tried," → it rumbles and shakes on the lectern. "richer" → the WEALTH dial turns up. "dead." → the HEALTH dial turns up. "Budget" → card 1 pops up like toast, "OPTIMAL BUDGET". "Policy" → card 2 pops up beside it, "OPTIMAL POLICY". "laws." → card 2 shoots out of the slot across the set and knocks the trophy out of the charred winner's hands; he stops shouting and stares at the card. after "laws." → the iris closes on her face.

Sound: a pat on the Optimitron; a thunk as the mug goes down and a hum as the window glows; a thunk as the stack drops in; a whirr as it rumbles; a click for each dial; a toaster pop for each card; a whistle as card 2 flies and a clank as the trophy falls.

On screen: "OPTIMITRON" / dials "HEALTH" · "WEALTH" / "10,000 JURISDICTIONS" / "OPTIMAL BUDGET" / "OPTIMAL POLICY".

Why: introduces the Optimitron, which comes back in Step 1, and lands the part's running gag one last time, at the lectern.
