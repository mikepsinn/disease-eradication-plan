---
format: 1920x1080
duration: 4:45.4
message: "Spend the treaty money on patients instead of committees, and treatments reach people 212 years sooner, which prevents 10.7 billion deaths."
arc: Title card (the FDA scatters to every corner) → Wishonia's live board and the paper reflex → the money follows the patient and tramples the grants office → out of the terrarium → the protocol stamp flattens the lifeguard and jackets fly to 23.4 million → 443 years squeezed to 36 → the approval cabinet opens, 212 years sooner → plans for Tuesday → the live detector lands on the one that works by mail → the doctor's prize wheel → grape soda → the ranking board crushes the wheel → the 40-page insert buries the patient → the meadow human dies mid-skip and keeps skipping → ask your doctor → the outcome label buries the lawyer → louder wins, and both are charred → the Optimitron
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 14, "Your Decentralized FDA"
audio: index-manual.cbaf659d.mp3, 27:54.0 to 32:39.5
version: v2
---

# Part 14 storyboard: "Your Decentralized FDA"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** One patient. She is an everyday human, `KIT.person({ tone: 2, outfit: "dress", hair: 1, color: 1, light: "red", mood: "worried" })` (an hourglass in a slate-blue dress with a flip hairdo; the same options in every scene, so she is the same woman), with a mustard-and-orange striped scarf at her neck (drawn at `KIT.rig(o).neck`) and her chest light blinking red. Her subsidy is one medicine paper that trots at her heel like a puppy in subsidy-follows-patient, until it jumps into the hand of the scientist at her trial door. She then walks through every Layer B scene of the new system: into a real hospital, a life jacket, the queue that squeezes, the SAFE bottle out of the approval cabinet (her bottle from then on: `KIT.props.pillBottle({ face: "smile", label: "SAFE" })`), the live side-effect panel on that bottle, row 1 of the ranking board, and the outcome label, where she takes the pill and her chest light turns teal. In the old-system scenes (decision-wheel, forty-page-insert, meadow-ad, ask-your-doctor) she waits on the side, scarf and all, chest light still red.

**The everyday humans who come back.** The doctor, `KIT.person({ tone: 1, outfit: "labcoat", color: 1 })` (a lab-coat build with a lantern jaw and a bald head), with a head mirror and a stethoscope: decision-wheel, ranked-treatments, forty-page-insert, ask-your-doctor. The lawyer, `KIT.person({ tone: 3, outfit: "suit", color: 1, holdR: "briefcase" })` (a box-shaped man with jowls and a bald head): smoke-detector-live, forty-page-insert, outcome-label. Use the same options in every scene, so each is the same man. In the props lines, "patient", "doctor" and "lawyer" mean these three.

**Running gag: the replacement lands on the old thing.** Each new piece of the system arrives on top of the piece it replaces and flattens it, so every flattening says what replaces what: the stampede of medicine papers runs over the grants officer and a giant red ✗ drops on the grant committee (subsidy-follows-patient), the protocol stamp flattens the lifeguard into his chair (life-jackets-handed-out), the live smoke detector slams onto the one that works by mail (smoke-detector-live), the ranking board drops onto the prize wheel (ranked-treatments), the lawyer's own 40-page insert buries him (outcome-label). The last one flies: the Optimitron's policy card shoots into the wall screen and knocks the trophy out of the loudest panelist's hands (optimitron-appliance).

**Callbacks from Part 12.** life-jackets-handed-out returns to lifeguard-cabinet's beach: the lifeguard, the line of swimmers and grinning skulls in the water, the two jackets on the hook. two-hundred-twelve-years-sooner opens the approval cabinet from committee-8-years, with its hourglass on "8.2 YEARS", the SAFE bottle and life preserver inside, the handprint on the glass, and the patient's skeleton still slumped against it. smoke-detector-live brings back the detector from smoke-detector-by-mail, still charred black, letter and mailbox flag still up. The bearded grant committee in subsidy-follows-patient is committee-8-years' committee. "The dead keep waiting" (Part 12) pays off: the skulls in the water get their jackets late, and the cabinet skeleton reaches for the bottle eight years late.

**Callbacks from Part 9.** accordion-timeline squeezes the roped queue from queue-to-not-die (humans holding germ tickets, the back of the line grey and bearded, then skeletons still holding their tickets) under the wait sign from untested-warehouse, still on "443 YEARS". Part 9's running gag "waiting ages you" runs backwards: the beards zip back up into the chins. The dusty bottle with the cobweb from untested-warehouse rides arrow 1 in two-hundred-twelve-years-sooner.

**Callbacks from Part 1.** The paper reflex from papers-with-presidents: on "small pieces of paper" every head on the wall screen snaps to Wishonia's paper (home-planet-board). The moth from the empty wallet in without-with-papers flies out of the class-action lawyer's briefcase (smoke-detector-live). The skeletons keep smiling: the meadow human dies mid-skip and keeps skipping (meadow-ad).

**Callback set up here.** The Optimitron comes back in Step 1 (Part 17). Draw it with `KIT.props.optimitron` and its defaults, so it is the same appliance.

**Held frame.** plans-for-tuesday, after "deaths.": the 10.7 billion counter holds still for 1 s, until "individual". A HOLD is silent.

**Bans for this part.**
- No real people or logos. No real drug brands or packaging, no real cereal or cigarette brands (plain boxes), no search-engine logo (the doctor's screen is a plain search box). "Vioxx" is spoken only; nothing is drawn for it.
- The two panelists in louder-wins are generic politicians; the winner's tie flickers red and blue, so neither team wins.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame. The TV ad's crawl text sits inside the TV, above the keep-out.
- No countdown board (it was removed from the kit); this part never used one.

## Changes from v1

- The humans are the stereotype cast: the scientist takes the subsidy at the trial door, the fat cat picks the terrarium humans with tweezers (and flicks the sick patient away) and stamps "DENIED" for the insurance company, the lobbyist is the drug rep with the donuts, the loud human is marketing, and the two panelists in louder-wins are politicians, red tie and blue tie. The patient, the doctor and the lawyer are everyday humans with fixed options, so they look the same in every scene.
- New running gag: the replacement lands on the old thing (above).
- Every threat pays off on screen: the grants officer is trampled flat, the committee is flattened under a red ✗, the lifeguard is stamped into his chair, the old detector is squashed, the prize wheel is crushed, the insert buries the patient and then the lawyer, the meadow human x-rays into a skeleton mid-skip, the loudness meter blows up and chars both panelists.
- The $41,000 bag in subsidy-follows-patient pops into 44 puppy papers ($41,000 ÷ $929 = 44.1), which sets up the 44.1× in life-jackets-handed-out.
- The puppy paper pays the scientist at the trial door; it does not follow the patient through the whole part. Her SAFE bottle is the object that travels instead.
- Money is green with seals: the subsidy, the stampede and the puppies are medicine papers (teal cross seal); Wishonia's paper in home-planet-board is plain.
- Props use the shared library names; every scene has a Sound line, and the sounds are placed in `parts/part-14.json`.

## Scene 1 · decentralized-fda-title

- id: decentralized-fda-title
- act: Title
- transition_in: cut (the parts are rendered on their own and joined)
- key: 1.6 s into "F.D.A.": a dozen little FDAs sitting in every corner of the card, the big stamp thumping the empty middle
- cue: "Your decentralized F.D.A."
- time: 27:54.0 to 27:57.4 (3.4 s)
- voiceover: "Your decentralized F.D.A."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`): "YOUR DECENTRALIZED" over "FDA". Then the FDA decentralizes.
- wishonia: not on screen
- props: titleScene, stamp, stampMark
- status: outline

Moves: "Your" → "YOUR" slams in. "decentralized" → "DECENTRALIZED" slides in beside it. "F.D.A." → "FDA" stamps down under them. 0.8 s into "F.D.A." → the FDA cracks into a dozen little "FDA"s that hop off to every corner and edge of the card and sit there. 1.6 s into "F.D.A." → a big rubber stamp comes down on the middle where the FDA was, thumps the empty card, and lifts: nothing left to approve.

Sound: a thunk on "Your" and "decentralized"; a rubber-stamp thunk on "F.D.A."; four quick pops as the little FDAs hop off; a second stamp thunk on the empty middle.

On screen: "YOUR DECENTRALIZED FDA". No: no APPROVED mark (there is nothing under the stamp). Why: the narrator reads the heading; the scattering is the word "decentralized" as a picture.

## Scene 2 · home-planet-board

- id: home-planet-board
- act: Wishonia's version
- transition_in: cut
- key: on "anything.": Wishonia holding a plain paper at arm's length; on the wall screen, the patient and two doctors squashed flat against the inside of the glass, reaching for it
- cue: "We built ours with"
- time: 27:57.4 to 28:26.8 (29.3 s)
- voiceover: "We built ours with the funding from our version of the treaty, three thousand years ago. Every treatment is tracked in real time. Every outcome is published. Every patient can participate. We don't have a word for "unapproved medicine" because we don't have a bureaucracy that sits on safe treatments while people die. You'd call our system a decentralized F.D.A. Here's what yours would look like, adjusted for the fact that you require small pieces of paper before you'll do anything."
- layer: A
- scene: The wall screen shows Wishonia's home planet's live board, rows of treatments and outcomes that tick in real time; Wishonia looks up "unapproved medicine" in a small Wishonian dictionary and finds only a cross-reference to Earth. Then the screen switches to Earth's version, and the Earth humans on it react to a paper the way they always do.
- wishonia: happy-smile + body-point-right, then thinking-small + body-point-right on "unapproved", then smirk-smile + body-presenting on "bureaucracy", then skeptical-smile + body-open-palms on "small"
- props: office, wallScreen, desk, mug, dictionary (drawn), money("plain"), door, scientist, patient, human
- status: outline

Moves: "three thousand years" → the wall screen lights up on Wishonia's home planet: a live board under "WISHONIA · 3,000 YEARS", rows of treatments with outcome columns. "tracked" → the rows start ticking, digits rolling. "published." → each row's outcome column fills with teal ticks. "participate." → small blue Wishonians with ball-tipped antennae hop onto the rows, one per row, and wave. "unapproved" → a little Wishonian dictionary flips open at Wishonia's pointing hand; her finger runs down the U page: "UNAPPETIZING" is followed straight by "UNARMED", with a gap between. "bureaucracy" → the pages riffle to B, which has one entry: "BUREAUCRACY: see EARTH", over a small engraving of a committee member sitting on a heap of SAFE bottles like a hen on eggs, a line of patients waiting in front of him. "die." → the patients in the engraving drop into grinning skeletons, still in line. after "die." → the dictionary snaps shut. "decentralized F.D.A." → the board's header retypes itself: "DECENTRALIZED FDA (your word)". "Here's" → the wall screen flips from the live board to Earth's cream paper: a long hallway of trial doors, a doctor leaning in each doorway (the scientist at the nearest one), and the patient at its start, chest light blinking red, looking lost. "small pieces of paper" → Wishonia holds up one plain paper between two fingers at arm's length, like a dead mouse; its little legs wriggle. "anything." → every head on the wall screen snaps toward the paper; the patient and two doctors run at it and squash their faces flat on the inside of the screen glass. after "anything." → they slide down the glass and drop back to their places in the hallway, heads still turned up toward the paper.

Sound: a switch as the board lights; four ticks as the rows start; typewriter clacks as the outcomes fill; three pops as the Wishonians hop on; a riffle of pages; crickets on the empty gap; a riffle and a ding on "see EARTH"; a small x-ray zap on "die."; a slam as the dictionary shuts; typewriter clacks as the header retypes; a whoosh as the screen flips; a squeak from the wriggling paper; a whoosh as the heads snap, a splat on the glass, and a falling slide whistle as they slide down.

On screen: "WISHONIA · 3,000 YEARS" / the dictionary's "UNAPPETIZING · UNARMED" and "BUREAUCRACY: see EARTH" / "DECENTRALIZED FDA (your word)". Why: shows the finished system first, so Earth's version has something to copy, and the paper reflex sets up the next scene: Earth's version has to run on paper.

## Scene 3 · subsidy-follows-patient

- id: subsidy-follows-patient
- act: Paying patients
- transition_in: zoom into the wall screen
- key: on "follow": the patient walking to her trial door with the medicine-paper puppy at her heel, its "$929" collar tag swinging; behind them the popped $41,000 bag and the trampled grants officer
- cue: "Eighty percent of the"
- time: 28:26.8 to 28:53.4 (26.7 s)
- voiceover: "Eighty percent of the twenty-seven point two billion dollars will go directly to subsidizing patient participation in pragmatic trials at nine hundred and twenty-nine dollars per patient instead of the usual forty-one thousand dollars. Patients will choose which trials to join; their subsidy will follow them. Treatment developers and providers will get paid for each participant. No grant committees deciding which diseases are fashionable this year."
- layer: B
- scene: The hallway of trial doors from the wall screen. A mountain of medicine papers stampedes straight to the patients over the grants office; one paper becomes the patient's puppy; the old $41,000 bag pops into 44 puppies; the patient picks a door, and the puppy pays the scientist standing in it. In the corner, the grant committee is flattened.
- wishonia: PiP, happy-smile + body-presenting, then smirk-smile + body-hands-hips on "fashionable"
- props: money("med"), priceTag, door, sign, germ, scientist, patient, human, moneybag (drawn)
- status: outline

Moves: "Eighty" → the first frame is the wall screen's last: the hallway of trial doors, every head turned up to the top right; they turn back. A mountain of medicine papers (green, teal cross seals) slides in from the left, tagged "$27.2 BILLION / YEAR". "percent" → 80% of it stands up on its little legs. "directly" → the 80% stampedes straight at the patients waiting at the hallway's mouth; a grants officer at a desk in its way, "GRANTS OFFICE", palm out, is trampled flat, a trail of tiny footprints across him; he blinks. "subsidizing" → one paper peels off the stampede and sits at the patient's feet, back legs kicking like a puppy. "nine hundred and twenty-nine" → a price tag on its collar swings round: "$929 / PATIENT". "forty-one thousand" → a huge bloated money bag waddles in beside it on stub legs, tagged "$41,000". "dollars." (last) → the bag pops like a balloon: 44 puppy papers spill out and scamper off down the hallway, one to each of 44 more patients. "choose" → the patient walks along the hallway past the trial doors, each with a different germ on its sign, and picks one. "follow them." → her puppy trots at her heel. "Treatment developers" → in her door stands the scientist (cast), clipboard out; everyday doctors stand in the others. "paid" → the puppy jumps up into the scientist's hand. "participant." → the tally on her door ticks to 1, and the other doors' tallies tick as the other puppies arrive; the patient goes in. "No grant committees" → in the corner, the bearded grant committee from committee-8-years (Part 12) sits at its table under "GRANT COMMITTEE", turning pages; a giant red ✗ drops on the table like an anvil and flattens them. "fashionable" → from under the ✗, one flattened arm pokes up holding a germ by a strap, like a handbag, posing. after "year." → the germ blows a kiss.

Sound: a whoosh for the zoom; a pop as the 80% stands up; tiny squeaky footsteps for the stampede and a splat for the grants officer; a boing as the puppy sits; a squeak as the tag swings; a squeak for the waddling bag; a pop as it bursts and squeaky footsteps as the 44 scatter; a squeak per step down the hallway; a cash-register ding as the puppy pays; three ticks for the tallies; a falling slide whistle and a slam for the ✗; a sparkle on the germ; a kiss squeak.

On screen: "$27.2 BILLION / YEAR" / "80%" / "GRANTS OFFICE" / "$929 / PATIENT" / "$41,000" / "GRANT COMMITTEE". No: no "Patients choose. The money follows." card (the captions say it). Why: the money goes where the patient goes, not where a committee points, and the burst bag shows the same money paying for 44 patients.

## Scene 4 · clinical-terrarium

- id: clinical-terrarium
- act: Paying patients
- transition_in: slide left
- key: on "real hospitals": the glass lifted, the tidy humans filing out along the bench into the hospitals, the patient picking herself up to walk in with them
- cue: "Instead of testing drugs"
- time: 28:53.4 to 29:05.1 (11.7 s)
- voiceover: "Instead of testing drugs on two hundred humans selected by pharmaceutical companies in clinical terrariums, you'll test on real patients in real hospitals. Where the diseases are."
- layer: B
- scene: A glass terrarium on a lab bench holds 200 identical, healthy little humans; the fat cat picks them with tweezers and flicks the sick patient away. The glass lifts, and they all walk into a row of real hospitals, where the diseases are.
- wishonia: PiP, smirk-smile + body-idle, then happy-smile + body-point-right on "Where"
- props: lab, hospital, diseaseBlob, sign, richHuman, patient, KIT.person({ plain: true }) (the tidy humans)
- status: outline

Moves: "Instead" → a glass terrarium on a lab bench, full of tidy little humans who are all the same: the plain build, the same gown, the same smile, every chest light off. "two hundred humans" → a counter on the glass: "200". "selected" → the fat cat (cast) leans over the bench with a pair of tweezers and sets one more tidy human inside. "pharmaceutical" → the patient (scarf, chest light blinking red) climbs up the bench leg to get in; the fat cat picks her up with the tweezers, looks at her chest light, and flicks her off the bench; she sails out of frame and lands in a heap. "terrariums," → a label on the glass: "CLINICAL TERRARIUM". "real patients" → the glass lifts off. "real hospitals." → the tidy humans file out along the bench and down into a row of real hospitals; the patient picks herself up and walks in with them, scarf flapping. "Where" → the camera pans along the hospitals. "diseases are." → in every window a disease blob looms smugly over a bed; each one turns to see the testers walking in, and its grin turns scared. after "are." → one blob climbs out of a back window.

Sound: a thunk as the terrarium lands; a pop for the counter; a click of the tweezers; a whistle as the patient is flicked and a boing as she lands; a tick for the label; a rising slide whistle as the glass lifts; squeaky footsteps into the hospitals; a yelp from the blobs.

On screen: "200" / "CLINICAL TERRARIUM". Why: trials move to where the sick people are, and the terrarium shows who they used to leave out.

## Scene 5 · life-jackets-handed-out

- id: life-jackets-handed-out
- act: Paying patients
- transition_in: slide left
- key: on "hand out": life jackets flying off the conveyor down the whole line, the swimmers bobbing up like corks, the patient catching hers, the lifeguard flat in his chair under the stamp mark
- cue: "The whole thing will"
- time: 29:05.1 to 29:28.1 (23.0 s)
- voiceover: "The whole thing will use your new decentralized F.D.A. protocol, reducing trial costs by forty-four point one times and funding twenty-three point four million patients per year (versus the current one point nine million patients per year). Remember that billion patients drowning in line for two life jackets? Your decentralized F.D.A. will hand out twenty-three point four million."
- layer: B
- scene: The beach from lifeguard-cabinet (Part 12): the lifeguard on his tall chair, the line of swimmers and grinning skulls out to the horizon, the two jackets on the hook. The protocol stamp flattens the lifeguard, and a conveyor of life jackets runs out to the whole line.
- wishonia: PiP, happy-smile + body-presenting, then excited-ee + body-excited on "hand"
- props: stamp, stampMark, priceTag, conveyor, patient, human, life-jacket (drawn), KIT.person skeleton (the skulls)
- status: outline

Moves: "The whole thing" → the beach as lifeguard-cabinet left it: the lifeguard (a beanpole in a striped tank top, zinc on his nose, sunglasses, a whistle) up on his chair flipping his "BUOYANCY STUDY: 8.2 YEARS" clipboard; the two jackets on the hook, a price tag "$41,000 / PATIENT" hanging from one. "protocol," → a giant rubber stamp drops out of the sky onto the lifeguard's chair and flattens him into the seat; when it lifts, he is printed over with a red "DECENTRALIZED FDA PROTOCOL" mark, blinking. "forty-four point one" → the price tag shrinks with a deflating squeal to a tiny tag: "$929". "twenty-three point four million" (first) → a conveyor rolls out from the hook along the waterline, stacked with life jackets, a counter on its side: "23.4 MILLION / YEAR". "one point nine million" → the hook's old counter, "TODAY: 1.9 MILLION", shrinks beside it. "Remember" → the camera pans along the line of swimmers from Part 12, heads and waving arms (the near ones drawn humans with their hats and hairdos, the far ones dots), grinning skulls bobbing politely among them. "drowning" → down the line, heads bob under and back up. "jackets?" → the first swimmer reaches for the two jackets on the hook. "hand out" → the conveyor starts: life jackets fly off it down the whole line, one per head, and every swimmer pops up high in the water like a cork; the patient (scarf) catches hers mid-air. "million." (last) → the jackets keep flying to the horizon; the grinning skulls get jackets too, a little late, and bob along, still grinning. after "million." → the lifeguard peels himself off his chair like a sticker and blows his whistle at nobody.

Sound: a rubber-stamp thunk and a splat for the lifeguard; a falling slide whistle as the tag deflates; the conveyor's whirr as it rolls out; a tick for the old counter; a whoosh for the pan; three bubble pops; a squeak for the reach; the conveyor's whirr and four pops as the jackets fly; a boing as the swimmers bob up; a whistle after "million.".

On screen: "DECENTRALIZED FDA PROTOCOL" (the stamp mark) / "$41,000 / PATIENT" → "$929" / "23.4 MILLION / YEAR" / "TODAY: 1.9 MILLION". Why: pays off Part 12's lifeguard with the new number.

## Scene 6 · accordion-timeline

- id: accordion-timeline
- act: Faster treatments
- transition_in: slide left
- key: on "thirty-six": the line squeezed up to the window, the beards gone, the wait sign's wheels clanking to "36 YEARS"
- cue: "This will increase the"
- time: 29:28.1 to 29:37.4 (9.2 s)
- voiceover: "This will increase the treatment discovery rate twelve point three times, compressing that about four hundred and forty-three years wait to about thirty-six years."
- layer: B
- scene: The ticket window and roped queue from queue-to-not-die (Part 9), under the wait sign from untested-warehouse on "443 YEARS". The shutter speeds up, and the line squeezes like an accordion until the sign reads 36 years.
- wishonia: PiP, thinking-small + body-thinking, then happy-smile + body-fist on "thirty-six"
- props: sign (the wait sign), pillBottle, germ, patient, human, KIT.person skeleton
- status: outline

Moves: "This" → the ticket window in its long wall, the wait sign over it on "WAIT TIME FROM HERE: 443 YEARS", and the roped queue zigzagging away between brass posts: humans holding germ tickets, chest lights red, the back of the line grey and bearded, then grinning skeletons still holding their tickets. The patient is a third of the way back, ticket in hand. "twelve point three" → the window's shutter starts flying up and down so fast it blurs, spitting out teal bottles one after another; a tag on it spins up to "12.3×". "compressing" → the brass posts slam together like an accordion and the zigzag folds up toward the window; the grey humans' beards zip back up into their chins like tape measures, and the skeletons at the back are squeezed forward too, rattling. "four hundred and forty-three" → the wait sign shakes on "443 YEARS". "thirty-six" → its digit wheels spin down and clank to "36 YEARS"; the patient is near the front now.

Sound: a whirr as the shutter blurs and three pops for the bottles; a huff and a squeak as the line squeezes; a low clank as the sign shakes; four ticks as the wheels spin down and a clank as they stop.

On screen: "12.3×" / "443 YEARS" → "36 YEARS". Why: the speed-up as a line that gets shorter.

## Scene 7 · two-hundred-twelve-years-sooner

- id: two-hundred-twelve-years-sooner
- act: Faster treatments
- transition_in: same form (no seam)
- key: on "two hundred and twelve": the two arrows merged into one fat arrow stamped "212 YEARS SOONER", the approval cabinet standing open, the patient hugging her SAFE bottle
- cue: "Two things will save"
- time: 29:37.4 to 30:02.7 (25.3 s)
- voiceover: "Two things will save lives. First, finding treatments faster: treatments that would have sat undiscovered for centuries will get found two hundred and four years sooner on average. Second, eliminating the eight point two years bureaucratic delay between proving a drug is safe and letting dying humans take it. Combined, treatments will reach patients two hundred and twelve years sooner on average."
- layer: B
- scene: Over the squeezed line, two arrow slots fill: first a dusty bottle from untested-warehouse found 204 years sooner, then the approval cabinet from committee-8-years bursts open and the SAFE bottle runs past its old skeleton to the patient. The two arrows merge into one big arrow.
- wishonia: PiP, neutral-smile + body-counting, then happy-smile + body-presenting on "Combined,"
- props: pillBottle, padlock, stampMark, sign, glass-cabinet (drawn as in Part 12), hourglass (drawn as in Part 12), KIT.person skeleton, patient, human
- status: outline

Moves: "Two" → the first frame is accordion-timeline's last. "things" → two empty arrow slots open over the line, "1" and "2". "First," → arrow 1 slides into slot 1. "centuries" → a dusty bottle from untested-warehouse's shelf rides in on it, in a cobweb, wearing its "NEVER TESTED FOR THIS" tag; the spider lowers itself. "found" → the tag flips to a teal tick and the bottle shakes off its dust. "two hundred and four" → arrow 1's label lands: "FOUND 204 YEARS SOONER". "Second," → the approval cabinet from committee-8-years slides into slot 2: the hourglass on top on "8.2 YEARS", the SAFE bottle on the top shelf, the life preserver on the bottom shelf, the handprint on the glass, and Part 12's patient skeleton still slumped against it, palm on the glass. "eliminating" → the hourglass bursts and sprays sand, the padlock pops off, and the glass door swings open. "dying" → the SAFE bottle hops out and runs down to the line, past the slumped skeleton, which lifts a bony hand for it eight years late. "take it." → the patient takes the bottle and hugs it; it is her bottle from now on. "Combined," → the two arrows merge into one fat arrow. "two hundred and twelve" → it stamps: "212 YEARS SOONER". after "average." (last) → the line cheers, and the near humans throw their hats in the air.

Sound: two pops for the slots; a whoosh for arrow 1; a huff of dust; a sparkle as the tag flips; a ding as the label lands; a whoosh as the cabinet slides in; a pop as the hourglass bursts, a clank for the padlock and a squeak for the door; a boing as the bottle hops; a pop as she takes it; a whoosh as the arrows merge; a rubber-stamp thunk; three pops for the hats.

On screen: "1" / "2" / "FOUND 204 YEARS SOONER" / "8.2 YEARS" / "212 YEARS SOONER". No: no "No 8.2-year delay" card (the burst hourglass says it). Why: the two gains, added up, so the 212 is earned on screen.

## Scene 8 · plans-for-tuesday

- id: plans-for-tuesday
- act: Faster treatments
- transition_in: slide left
- key: after "Tuesday.": the crowd to the horizon holding up calendars, every sticky note ticked, the dentist man groaning
- cue: "That timeline shift will"
- time: 30:02.7 to 30:12.3 (9.5 s)
- voiceover: "That timeline shift will prevent ten point seven billion deaths. Those are individual humans who currently have plans for next Tuesday."
- layer: B
- scene: A counter rolls to 10.7 billion and holds; then its digits crack apart into a crowd of humans to the horizon, each holding up a desk calendar with a sticky note for next Tuesday.
- wishonia: PiP, sad-small + body-idle, then happy-small + body-hand-chest on "Tuesday."
- props: calendar, sign, grandma, pillBottle, patient, human
- status: outline

Moves: "ten point seven billion" → a counter rolls up to "10.7 BILLION DEATHS PREVENTED". "deaths." → HOLD 1 s, until "individual". "individual" → the counter's digits crack apart, and out of each crack steps a human, then more, until the crowd runs to the horizon (the near ones drawn humans of every build and hat, the far ones dots), every one holding up a desk calendar open on "TUE". "plans" → a sticky note lands on each calendar; in front: the patient (scarf, her SAFE bottle under one arm) "KID'S RECITAL", grandma (cast) "BINGO", a barrel-shaped man in a cardigan "FISHING", a box-shaped man in a suit "DENTIST". "Tuesday." → each note gets a small teal tick. after "Tuesday." → the dentist man reads his note and groans; everyone else beams.

Sound: four ticks as the counter rolls and a soft ding as it stops; then silence for the HOLD; four pops as the crowd steps out; a pat as the notes land; a sparkle for the ticks; a huff for the groan.

On screen: "10.7 BILLION DEATHS PREVENTED" / "TUE" / "KID'S RECITAL" · "BINGO" · "FISHING" · "DENTIST". Why: turns the biggest number in the part back into people, and the dentist is the proof they are alive.

## Scene 9 · smoke-detector-live

- id: smoke-detector-live
- act: Real-time safety monitoring
- transition_in: slide left
- key: on "BEFORE": the patient reading her bottle's lit panel with the cap still on; above her, the live detector on the wall, the old one flattened under it with only its mailbox flag sticking out
- cue: "Real-Time Safety Monitoring."
- time: 30:12.3 to 30:35.0 (22.7 s)
- voiceover: "Real-Time Safety Monitoring. Remember Vioxx and the smoke detector that works by mail? Your new system will collect every side effect automatically in real time. You'll know "twelve percent got headaches, three percent were severe" BEFORE you take the pill, not after the class action lawsuit. The F.D.A. doesn't publish these numbers at all. They make you guess."
- layer: B
- scene: Under a banner, the patient's kitchen wall holds the charred smoke detector from smoke-detector-by-mail (Part 12); a live detector slams onto it. The patient's SAFE bottle lights up with side-effect numbers before the cap comes off. A class-action lawyer finds nobody to sue; the FDA's own bottle has no numbers, so she flips a coin.
- wishonia: PiP, smirk-smile + body-idle, then sideeye-closed + body-arms-crossed on "guess."
- props: pillBottle, sign, smoke-detector (drawn as in Part 12), lawyer, patient, coin (drawn)
- status: outline

Moves: "Monitoring." → a banner unrolls: "REAL-TIME SAFETY MONITORING". "smoke" → on the kitchen wall, the smoke detector from smoke-detector-by-mail, still charred black, the singed "RE: SMOKE" letter still held up; it starts writing another letter. "mail?" → its mailbox flag pops up. "automatically" → a new detector with a live screen slams onto the wall on top of it and flattens it; only the mailbox flag sticks out from under, then droops. "real time." → the live screen blinks on and a line of readings starts scrolling across it. "twelve percent" → below it, the patient (scarf, chest light red) holds up her SAFE bottle; its side panel lights up: "HEADACHES 12%". "three percent" → "SEVERE 3%". "BEFORE" → she reads it with the cap still on, rubs her temple at the 12%, and nods. "class" → a class-action lawyer (a box-shaped man with jowls in a suit) rushes in waving a sign, "INJURED?"; nobody is. "lawsuit." → he snaps open his briefcase, and a moth flies out. "F.D.A." → beside her bottle stands the FDA's own bottle, a plain bottle labeled "FDA" with a blank panel. "guess." → she flips a coin over it; the coin lands on its edge and stays standing.

Sound: a whoosh as the banner unrolls; a pen scratch as the detector writes; a squeak as the flag goes up; a slam and a splat as the live detector lands; a switch as its screen blinks on; a ding for each number; squeaky footsteps for the lawyer and a click as the briefcase opens; a ding as the coin flips and a tick as it lands on its edge.

On screen: "REAL-TIME SAFETY MONITORING" / "RE: SMOKE" / "HEADACHES 12%" · "SEVERE 3%" / "INJURED?" / "FDA". Why: fixes the detector that works by mail, and puts the numbers on the bottle before the pill.

## Scene 10 · decision-wheel

- id: decision-wheel
- act: Treatment rankings
- transition_in: slide left
- key: after "vibes.": the wheel clicking to a stop on DONUTS, the patient on the exam table, the lobbyist and the fat cat at the edges
- cue: "Treatment Rankings. Currently,"
- time: 30:35.0 to 30:49.4 (14.4 s)
- voiceover: "Treatment Rankings. Currently, your doctor picks treatments based on: that drug rep who brought good donuts in two thousand and three, something they half-remember from medical school, whatever the insurance company allows, and vibes."
- layer: B
- scene: Under a banner, a doctor's office: the patient waits on the exam table while the doctor steps up to a carnival prize wheel with four slices. The drug rep, a half-erased lecture and the insurance company each light a slice; the doctor spins.
- wishonia: PiP, eyeroll-smile + body-idle, then eyeroll-closed + body-shrug on "vibes."
- props: sign, stamp, lobbyist, richHuman, doctor, patient, prize-wheel (drawn), donut-box (drawn)
- status: outline

Moves: "Rankings." → a banner unrolls: "TREATMENT RANKINGS". "Currently," → a doctor's office: the patient sits on the exam table in a paper gown, scarf on, chest light blinking red; the doctor (a lab-coat build with a lantern jaw and a bald head, a head mirror and a stethoscope) steps up to a prize wheel on a stand with four slices. "donuts" → slice 1 lights: "DONUTS (2003)"; the lobbyist (cast: fedora, domino mask, trench coat) tiptoes in behind the doctor and slips a box of donuts under his arm. "half-remember" → slice 2 lights: "HALF-REMEMBERED LECTURE"; a thought bubble over the doctor shows a chalkboard, half erased. "insurance company" → slice 3 lights: "WHAT INSURANCE ALLOWS"; the fat cat (cast) leans in through the window and thumps a "DENIED" stamp on the patient's chart. "vibes." → slice 4 lights: "VIBES"; the doctor licks a finger, holds it up to the wind, and spins the wheel. after "vibes." → it clicks to a stop on DONUTS. (On grape-soda's wall screen, the doctor then hands the patient a donut.)

Sound: a whoosh as the banner unrolls; a squeak as the doctor steps up; a ding as each slice lights and a tiptoe squeak for the lobbyist; a rubber-stamp thunk for DENIED; the wheel's whirr; three slowing ticks and a click as it stops.

On screen: "TREATMENT RANKINGS" / "DONUTS (2003)" · "HALF-REMEMBERED LECTURE" · "WHAT INSURANCE ALLOWS" · "VIBES" / "DENIED". Why: how treatments get picked today.

## Scene 11 · grape-soda

- id: grape-soda
- act: Treatment rankings
- transition_in: zoom out of the wall screen
- key: after "grape." (last): the grape sticker fluttering into Wishonia's mug, the can's label under it reading "0% GRAPE"
- cue: "This is called evidence-based"
- time: 30:49.4 to 30:57.1 (7.7 s)
- voiceover: "This is called "evidence-based medicine," which contains the word "evidence" the same way "grape soda" contains the word "grape."."
- layer: A
- scene: The wall screen still shows the doctor's office; a framed sign "EVIDENCE-BASED MEDICINE" drops over it. Wishonia holds up a can of grape soda with one very small, clearly fake grape on the label.
- wishonia: skeptical-smile + body-point-right, then smirk-smile + body-presenting on "soda", then smirk-closed + body-hands-hips on "word" (just before the last "grape")
- props: office, wallScreen, desk, mug, sign, soda-can (drawn)
- status: outline

Moves: "This" → zoom out of the wall screen, which still shows decision-wheel's last frame: the wheel stopped on DONUTS. On the screen, the doctor hands the patient a donut and writes the prescription; she looks at the donut. "medicine," → a framed sign drops over the wall screen picture: "EVIDENCE-BASED MEDICINE". "contains" (first) → Wishonia underlines "EVIDENCE" with her pointing finger. "soda" → she lifts a plain can, "GRAPE SODA", with one very small, clearly fake grape on its label. "grape." (last) → the camera pushes in on the grape. after "grape." → it is a sticker: it peels off and flutters into her coffee mug; under it the label reads "0% GRAPE".

Sound: a whoosh for the zoom; a thunk as the sign drops; a marker squeak for the underline; a pop as the can comes up; a tick for the push-in; a squeak as the sticker peels and a small splat in the mug.

On screen: "EVIDENCE-BASED MEDICINE" / "GRAPE SODA" / "0% GRAPE". Why: a dry joke gets Wishonia's face and the office.

## Scene 12 · ranked-treatments

- id: ranked-treatments
- act: Treatment rankings
- transition_in: zoom into the wall screen
- key: on "took it:": the flip board standing on the flattened prize wheel, bottles in order, the patient dropping her donut and pointing at row 1
- cue: "Your decentralized F.D.A. will rank"
- time: 30:57.1 to 31:03.9 (6.8 s)
- voiceover: "Your decentralized F.D.A. will rank every treatment by what actually happened to real humans who took it:"
- layer: B
- scene: Back in the doctor's office on the wall screen. A tall flip board, like a train-station departures board, drops onto the prize wheel and crushes it; pill bottles clack into order by what happened to the humans who took them, best on top.
- wishonia: PiP, happy-smile + body-point-right
- props: pillBottle, sign, ranking-board (drawn), patient, doctor
- status: outline

Moves: "Your" → zoom into the wall screen: the doctor's office, the prize wheel on DONUTS, the patient on the exam table holding her donut. "rank" → a tall flip board drops from the top of the frame onto the prize wheel and crushes it flat; one slice spins away across the floor. The board clacks, and pill bottles shuffle into order, best on top: "TREATMENT A · B · C". "actually happened" → each row gets a tally of tiny humans who took it, and its "GOT BETTER" bar fills. "it:" → the patient drops the donut, looks up and points at row 1; its bottle is the twin of her SAFE bottle.

Sound: a whoosh for the zoom; a slam and a splat as the board crushes the wheel; typewriter clacks as the rows flip; three ticks as the tallies fill; a ding as she points.

On screen: "RANKED BY WHAT HAPPENED" / "TREATMENT A · B · C" / "GOT BETTER". No: no real drug names, and no figures on the bars. Why: what replaces the prize wheel.

## Scene 13 · forty-page-insert

- id: forty-page-insert
- act: Outcome labels
- transition_in: slide left
- key: on "doctor.": the patient buried to the chin in unfolded insert, the doctor wiping his shoes on it, the lawyer scribbling at the far end
- cue: "Outcome Labels. Food has"
- time: 31:03.9 to 31:16.2 (12.3 s)
- voiceover: "Outcome Labels. Food has nutrition labels. Cigarettes have warning labels. Drugs have forty-page inserts written by lawyers having seizures, which nobody reads, including your doctor."
- layer: B
- scene: Under a banner, a kitchen counter: a plain cereal box shows its nutrition label and a plain cigarette pack its warning; then the patient opens a pill box and a 40-page insert unfolds, and keeps unfolding, until it buries her.
- wishonia: PiP, neutral-smile + body-idle, then eyeroll-closed + body-shrug on "including"
- props: sign, pillBottle, lawyer, doctor, patient, human, drug-insert (drawn)
- status: outline

Moves: "Labels." (first) → a banner unrolls: "OUTCOME LABELS". "nutrition" → on a kitchen counter, a plain cereal box turns to show its label: "NUTRITION FACTS". "warning" → a plain cigarette pack turns to show its label: "WARNING", with a small skull. "forty-page" → the patient opens a pill box; the insert unfolds, and unfolds, and unfolds, off the counter and across the floor, and piles up over her until only her head and scarf stick out. "lawyers" → at the far end of the insert, the lawyer from smoke-detector-live sits at a desk writing it; its text is tiny scribbles. "seizures," → his pen hand jitters so hard the scribbles turn into zigzags and the desk rattles. "nobody reads," → humans walk across the insert without looking down. "doctor." → the doctor from decision-wheel walks in, wipes his shoes on the insert like a doormat, and steps over the patient.

Sound: a whoosh as the banner unrolls; a click as each box turns; a whoosh and three paper pats as the insert unfolds; a pen scratch for the lawyer and a rattle as he jitters; squeaky footsteps across the paper; a pat as the doctor wipes his feet.

On screen: "OUTCOME LABELS" / "NUTRITION FACTS" / "WARNING" / the insert's "PAGE 1 OF 40". No: no real brand on the boxes. Why: the problem, told with things in the viewer's kitchen.

## Scene 14 · meadow-ad

- id: meadow-ad
- act: Outcome labels
- transition_in: slide left
- key: on "death,": "DEATH" crawling past, the meadow human mid-skip as a grinning skeleton in her sun hat, the patient on the couch
- cue: "Your television advertisements show"
- time: 31:16.2 to 31:36.4 (20.2 s)
- voiceover: "Your television advertisements show a smiling human frolicking through a meadow while a voiceover lists ways the drug might kill you at auctioneer speed. The meadow human does not react to the word "stroke." Side effects include "death," listed between "constipation" and "mild rash," as if your organs failing is roughly as inconvenient as dry skin."
- layer: B
- scene: A living room: the patient on the couch in front of an old TV set. On the screen, an ad: a smiling human skips through a meadow while small fast text crawls along the bottom of the screen; on "death" she turns into a grinning skeleton and keeps skipping.
- wishonia: PiP, sideeye-closed + body-idle, then annoyed-closed + body-arms-crossed on "organs"
- props: tvSet, KIT.xray, patient, human
- status: outline

Moves: "Your" → a living room: the patient on the couch, scarf on, chest light blinking red, in front of an old TV set (rabbit ears). On the screen, an ad: a smiling hourglass woman in a sundress and a sun hat, holding daisies, in a meadow. "frolicking" → she skips through the meadow, her smile fixed. "voiceover" → a crawl of small text starts along the bottom of the TV screen. "auctioneer" → the crawl speeds up to a blur and the rabbit ears wiggle. "stroke." → "STROKE" crawls past; her smile does not move. "death," → "DEATH" crawls past, the same small size as everything else; she x-rays into a grinning skeleton mid-skip, sun hat and daisies and all, and keeps skipping. "constipation" → "CONSTIPATION" crawls past just ahead of it. "mild" → "MILD RASH": red spots pop out on the skeleton. "dry skin." → the skeleton scratches its elbow bone and keeps skipping. after "skin." → on the couch, the patient turns her head slowly to the camera.

Sound: a boing per skip (three); typewriter clacks as the crawl starts and faster ones at auctioneer speed; crickets after "stroke."; an x-ray zap on "death,"; three pops for the rash; a scratch for the elbow.

On screen: the crawl "may cause: stroke · constipation · death · mild rash · dry skin". Why: today's label, the way viewers actually see it, with the horror the ad leaves out.

## Scene 15 · ask-your-doctor

- id: ask-your-doctor
- act: Outcome labels
- transition_in: same form (no seam)
- key: after "hallway.": the doctor stepping back from the patient, his phone's search box lit; the "APPOINTMENT: 7 MIN" sign over them, the TV on the waiting-room wall
- cue: "The label says individual"
- time: 31:36.4 to 31:51.1 (14.7 s)
- voiceover: "The label says "individual results may vary," meaning outcomes range from "cured" to "deceased" (both technically qualifying). It also says "ask your doctor," but your doctor has seven minutes per appointment and just Googled your condition in the hallway."
- layer: B
- scene: The ad's end card shows a dial from "CURED" to "DECEASED", and both ends qualify; then the camera pulls out of the TV into a hospital hallway, where the doctor skates past and looks up the patient's condition on his phone.
- wishonia: PiP, skeptical-smile + body-idle, then eyeroll-smile + body-shrug on "Googled"
- props: tvSet, gauge, stampMark, sign, phone, hospital, doctor, patient, KIT.person skeleton
- status: outline

Moves: "The" → the first frame is meadow-ad's last: the skeleton skipping on the TV, the patient looking at the camera. "individual" → the ad's end card: "INDIVIDUAL RESULTS MAY VARY". "cured" → a dial (gauge, mount "dial") on the card runs from "CURED" to "DECEASED"; its needle swings to CURED, and it gets a tick. "deceased" → the needle swings to DECEASED, and that gets a tick too. "qualifying)." → both ticks stamp "QUALIFIES"; the skeleton from the ad skips back into the end card, gives a bony thumbs-up, and skips off. "ask" → the camera pulls out of the TV: it hangs on the waiting-room wall of a hospital hallway, and the patient waits in a plastic chair under it. "seven minutes" → a sign over the hallway: "APPOINTMENT: 7 MIN"; the doctor (from decision-wheel) zips past on roller skates, a stopwatch in his hand. "Googled" → he skids to a stop and types on a rotary phone with a small screen, its cord trailing: a plain search box with the patient's condition typed in. "hallway." → he reads the result, goes pale, looks at the patient, and takes one slow step back.

Sound: a click as the end card comes up; a tick and a ding for each end of the dial; two rubber-stamp thunks; a whoosh as the camera pulls out; a whistle and a squeak as he skates past; typewriter clacks as he types; a falling slide whistle as he steps back.

On screen: "INDIVIDUAL RESULTS MAY VARY" / "CURED ✓ · DECEASED ✓ · QUALIFIES" / "APPOINTMENT: 7 MIN". No: no search-engine logo. Why: why "ask your doctor" does not fix the label.

## Scene 16 · outcome-label

- id: outcome-label
- act: Outcome labels
- transition_in: slide left
- key: after "happens." (last): the label flat on the patient's SAFE bottle, her chest light just turned teal, the loud human's megaphone gagged by his own sticker, the lawyer buried under his insert
- cue: "Your new system will produce"
- time: 31:51.1 to 32:04.5 (13.4 s)
- voiceover: "Your new system will produce Outcome Labels that tell you what actually happens when real humans take a drug. Not what a marketing department hopes happens. Not what a lawyer is comfortable admitting happens. What happens."
- layer: B
- scene: A clean outcome label, laid out like a nutrition label, slides onto the patient's SAFE bottle; the loud human and the lawyer each try to cover it with their own and get it back in the face. She reads it, takes the pill, and gets better.
- wishonia: PiP, happy-smile + body-presenting, then eyeroll-closed + body-arms-crossed on "comfortable", then smirk-closed + body-hands-hips on "What" (last)
- props: pillBottle, sign, loudHuman, lawyer, patient, outcome-label (drawn), drug-insert (drawn)
- status: outline

Moves: "Your" → the patient at her kitchen table with her SAFE bottle, its side panel from smoke-detector-live still lit. "Labels" → a clean label, laid out like a nutrition label, slides in and stops over the bottle: "OUTCOME LABEL (EXAMPLE)". "humans" → its bars fill with tiny humans: "GOT BETTER", "NO CHANGE", "SIDE EFFECTS", over the panel's "HEADACHES 12% · SEVERE 3%". "department" → the loud human (cast: a megaphone for a head) leans in and slaps a "MIRACLE!" sticker over the label. "hopes" → the sticker peels itself off and slaps over the mouth of his megaphone; he can only squeak now. "lawyer" → the lawyer from forty-page-insert tapes his 40-page insert over the label. "admitting" → the tape lets go; the insert unfolds off the bottle onto him and buries him; only his briefcase sticks out. "What" (last) → the label snaps flat onto the bottle. "happens." (last) → the patient reads it, pops the cap and takes the pill. after "happens." → her chest light flips from red to teal; she smiles and loosens her scarf.

Sound: a whoosh as the label slides in; three pops as the bars fill; a splat for the sticker; a squeak from the gagged megaphone; a tape rip; a whoosh and a paper pat as the insert buries the lawyer; a thunk as the label snaps flat; a sparkle as her light turns teal.

On screen: "OUTCOME LABEL (EXAMPLE)" / "What happened to real humans who took it" / bars "GOT BETTER" · "NO CHANGE" · "SIDE EFFECTS" / "HEADACHES 12% · SEVERE 3%" / "MIRACLE!". No: no invented numbers on the label; the bars carry no figures. Why: the fix, as something the viewer can read, and the patient's story ends in the teal light.

## Scene 17 · louder-wins

- id: louder-wins
- act: The Optimitron
- transition_in: slide left
- key: after "louder.": both panelists charred black and smoking, hair straight up, still shouting into megaphones; the trophy in one's hands, the BUDGETS and LAWS in his lap, his tie flickering red and blue
- cue: "Your decentralized D.F.D.A. figures"
- time: 32:04.5 to 32:19.8 (15.3 s)
- voiceover: "Your decentralized D.F.D.A. figures out which treatments work. But your governments also need to know which *policies* work, how much to spend on what, which laws to keep, which to throw away. Your current method is to argue about it on television until someone wins by being louder."
- layer: B
- scene: The ranking board shrinks into the corner. A TV panel show: two politicians with megaphones shout across a desk piled with budgets and laws, a loudness meter between them; the meter pins and blows up, and the louder one gets the trophy anyway.
- wishonia: PiP, annoyed-closed + body-arms-crossed, then eyeroll-closed + body-hands-hips on "louder."
- props: tvSet, gauge, sign, politician, KIT.nuke, KIT.boom, ranking-board (drawn), trophy (drawn), megaphone (drawn)
- status: outline

Moves: "Your" → the ranking board from ranked-treatments shrinks into the top-left corner. "work." → it gets a teal tick. "policies" → a big TV set fills the frame: a panel show with a long desk, and a pile of papers thumps onto it: "BUDGETS" and "LAWS". "keep," → a tray at one end: "KEEP". "away." → a trash can at the other end: "THROW AWAY". "argue" → two politicians (cast), one in a red tie and one in a blue tie, each with a megaphone, face off across the desk and shout; a loudness meter (gauge) stands between them, "LOUDNESS". "television" → the TV's rabbit ears shake. "wins" → the meter's needle swings back and forth, harder and harder. "louder." → it pins and bursts: a white flash and a boom. after "louder." → the smoke clears on both panelists charred black and smoking, hair straight up, still shouting into their megaphones; a trophy, "WINNER (LOUDEST)", drops into one's hands, and the BUDGETS and LAWS slide into his lap; his charred tie flickers red, blue, red.

Sound: a falling slide whistle as the board shrinks and a ding for its tick; a thunk as the pile lands and another for the tray; a clank for the trash can; two yelps as they shout; a switch as the ears shake; the needle's whirr; a boom; a bell for the trophy and a sizzle as the smoke clears.

On screen: "BUDGETS" · "LAWS" / "KEEP" · "THROW AWAY" / "LOUDNESS" / "WINNER (LOUDEST)". No: no "WHICH POLICIES WORK?" card (the captions say it); no party names or flags. Why: the current method, so the Optimitron has something to replace.

## Scene 18 · optimitron-appliance

- id: optimitron-appliance
- act: The Optimitron
- transition_in: zoom out of the wall screen
- key: on "laws.": card 2 shooting out of the Optimitron into the wall screen, card 1 standing in the slot, both dials up, the mug down
- cue: "Back home, the Optimitron"
- time: 32:19.8 to 32:39.5 (19.7 s)
- voiceover: "Back home, the Optimitron handles this. It's an appliance. You plug in what ten thousand jurisdictions tried, it tells you which policies actually made people richer or less dead. Its Optimal Budget Generator does budgets; its Optimal Policy Generator does laws."
- layer: A
- scene: The Optimitron sits on Wishonia's desk like a toaster; a fat card stack goes into its slot and two policy cards pop out like toast. The second one flies into the wall screen and ends the panel show.
- wishonia: happy-smile + body-point-right, then smirk-closed + body-idle on "handles" (the mug at her lips), then smirk-smile + body-presenting on "appliance.", then excited-oh + body-excited on "Policy"
- props: office, wallScreen, desk, mug, optimitron, sign
- status: outline

Moves: "Back" → zoom out of the wall screen, which still shows louder-wins' last frame: the charred panelists shouting, the trophy, the flickering tie. "Optimitron" → the Optimitron sits on Wishonia's desk like a toaster: two big dials, HEALTH and WEALTH; Wishonia pats it. "handles" → Wishonia sips her coffee. "appliance." → the mug goes down slowly; the Optimitron's window glows and its face smiles. "jurisdictions" → a fat stack of cards banded "10,000 JURISDICTIONS" drops into its toaster slot. "tried," → it rumbles and shakes on the desk. "richer" → the WEALTH dial turns up. "dead." → the HEALTH dial turns up. "Budget" → card 1 pops up like toast: "OPTIMAL BUDGET". "Policy" → card 2 pops up beside it: "OPTIMAL POLICY". "laws." → card 2 shoots out of the slot and flies into the wall screen. 0.5 s into "laws." → it knocks the trophy out of the charred winner's hands; both panelists stop shouting and stare at it. The part ends on that frame.

Sound: a whoosh for the zoom; a pat on the Optimitron; a thunk as the mug goes down and a hum as the window glows; a thunk as the stack drops in; a whirr as it rumbles; a click for each dial; a toaster pop for each card; a whistle as card 2 flies and a clank as the trophy falls.

On screen: "OPTIMITRON" / dials "HEALTH" · "WEALTH" / "10,000 JURISDICTIONS" / "OPTIMAL BUDGET" / "OPTIMAL POLICY". Why: introduces the Optimitron, which comes back in Step 1, and lands the part's running gag one last time.
