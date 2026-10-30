---
format: 1920x1080
duration: 1:30.2
message: "Humans cannot stop being illogical all at once, so the plan moves 1% of murder money to medicine money in year one and a little more each year, until war is forgotten."
arc: Title card (a snail pushes the bar to 1%) → Wishonia's planet ended a 12,000-year war → humans bonk each other for 10,000 years and keep going as skeletons → toddlers nap, nations don't → a dog doing calculus catches fire → the slider from year 1 to year 20 → paint chips swapped for peas, until even the dog won't touch them
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 3, "The Gradual Irrationality Reduction Program"
audio: index-manual.cbaf659d.mp3, 04:58.2 to 06:28.4
version: v2
---

# Part 3 storyboard: "The Gradual Irrationality Reduction Program"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the Earth paper; the money is green, and its seal says what it buys (`KIT.money("war")`: a red missile seal; `KIT.money("med")`: a teal cross seal). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** A little at a time. The foam bats show why it can't happen at once (nations-foam-bats, toddlers-take-nap), the slider shows the plan (war money through the color-flip funnel, a bit more each year), and paint-chips repeats it on a high chair: chips with the war seal's missile swapped for peas with the medicine seal's cross, one at a time.

**Running gags.** The snail on the title card pushes a progress bar to 1%; it rides the slider's knob in slider-year-one-to-twenty. The year counter is a tear-off calendar (`KIT.props.calendar`) in nations-foam-bats; there is no countdown board in this part.

**Callbacks.** From Part 1 (meet-wishonia): the 4,297 years and the converter's bell come back on the teal bar in wishonia-war-timeline. The two politicians from nations-foam-bats come back as skeletons, still bonking, in toddlers-take-nap. The dog from dog-calculus, which finally learned to sit, sits under the high chair in paint-chips. The manual Wishonia opens in wishonia-war-timeline is the manual the narrator holds up in slider-year-one-to-twenty (old edition, new edition). The Weapons Maker's cradled missile becomes a cradled pill bottle.

**Transitions.** Part 2 ends in the office (food-directly), so the title card cuts in. Office to office cuts; the office zooms into the wall screen for nations-foam-bats; Earth to Earth slides left. Part 4's title zooms out of the wall screen, so paint-chips ends on a settled frame.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.
- No real flags or country outlines; the two nations are plain islands.
- No speech text that repeats the narration: the captions carry the year lines in slider-year-one-to-twenty.

## Changes from v1

- The humans are the stereotype cast: the nations are two Politicians, the teacher is the Scientist, the slider has the Weapons Maker, and everyday humans (the toddlers, the growing human, the mother) get their bodies from their outfits.
- The money is green with seals; "red papers" became war money and "teal papers" medicine money.
- Every gag now pays off on screen: the bonks set off tiny mushroom clouds and outlive the politicians, the toddlers sleep through a nuke, the dog's ears catch fire, the Weapons Maker's missile goes off in his arms, the baby's cry floods the kitchen.
- The year counter in nations-foam-bats is a tear-off calendar; the title card got a snail and a 1% bar.
- slider-year-one-to-twenty no longer prints the year lines on screen.
- Every scene has a Sound line, placed in `parts/part-03.json`.

## Scene 1 · irrationality-reduction-title

- id: irrationality-reduction-title
- act: Title
- transition_in: cut (Part 2 ends in the office)
- key: after "Program.": all four words in, the snail sitting down at 1% on the progress bar
- cue: "The Gradual Irrationality Reduction Program"
- time: 04:58.2 to 05:02.3 (4.1 s)
- voiceover: "The Gradual Irrationality Reduction Program."
- layer: A, title card
- scene: The title card (`KIT.titleScene`) with the part's heading; under it, an empty progress bar that a snail pushes.
- props: title-card, snail, progress-bar
- status: outline

Moves: "Gradual" → "THE GRADUAL" drifts in slowly (each word takes about 0.8 s to settle instead of slamming: the slowest title card in the episode), and a snail starts along the horizon, pushing the fill of an empty progress bar under the heading. "Irrationality" → the word drifts in crooked and slowly straightens itself. "Reduction" → drifts in. "Program." → drifts in and settles with a thunk. after "Program." → the bar ticks to "1%"; the snail stops, wipes its brow with an eye stalk and sits down for a rest.

Sound: a soft whoosh under each drifting word; a thunk as the last word settles; a tick as the bar reaches 1%.

On screen: "THE GRADUAL IRRATIONALITY REDUCTION PROGRAM" / "1%". Why: the narrator reads the heading; the snail at 1% is the plan's pace before anyone explains it.

## Scene 2 · wishonia-war-timeline

- id: wishonia-war-timeline
- act: How Wishonia's planet did it
- transition_in: cut
- key: on "nobody": the red tape looped across the office floor with its row of grinning antenna skulls, Wishonia shrugging over the open manual
- cue: "We ended wars using"
- time: 05:02.3 to 05:17.6 (15.4 s)
- voiceover: "We ended wars using this exact program four thousand, two hundred and ninety-seven years ago. Before that we'd been fighting for twelve thousand years, which now seems like quite a long time to do something nobody enjoyed."
- layer: A
- scene: Wishonia's battered old copy of the manual lands on the desk and falls open; the wall screen draws her planet's timeline: a short teal peace bar, then a red war bar so long it prints out of the screen as a paper tape and piles up on the office floor.
- wishonia: big, happy-smile + body-hand-chest, then thinking-closed + body-thinking on "Before", then skeptical-closed + body-shrug on "nobody"
- props: office, desk, mug, wall-screen, manual, timeline-tape, politician, foam-bat, capitol
- status: outline

Moves: "We" → the blank wall screen is off; an old, dusty copy of the manual (`KIT.props.manual`) drops onto the desk; its cover reads "GRADUAL IRRATIONALITY REDUCTION PROGRAM". "ended" → it flops open by itself in a puff of dust. "program" → the wall screen clicks on: a timeline axis. "four thousand" → a short teal bar draws on at the right end, labeled with the number from meet-wishonia: "PEACE: 4,297 years". "years" (first) → the label dings like the converter's bell in meet-wishonia. "twelve thousand" → a red bar grows out to the left of the teal one, almost three times as long, hits the screen's left bezel and keeps going: it prints out through the bezel as a long red paper tape, "WAR: 12,000 years". Along the tape runs a row of tiny grinning skulls, each with two antennae and ball tips: Wishonia's ancestors. "which now seems" → the tape spills down the wall and loops onto the floor. "quite a long time" → the loops pile up as high as the desk. "nobody" → Wishonia shrugs. "enjoyed." → the tape zips back into the screen like a tape measure, the last skull waving on the way in; the screen wobbles on its mount and settles. after "enjoyed." → the screen clicks over to Earth: two islands, a politician on each, foam bats raised (nations-foam-bats' first frame).

Sound: a thunk as the manual lands; a huff of dust; a switch click as the screen comes on; a marker squeak for the teal bar; the converter's bell on "years"; a typewriter clatter as the tape prints; a whirr as it spills; a whoosh and a slam as it zips back; a switch click to Earth.

On screen: "GRADUAL IRRATIONALITY REDUCTION PROGRAM" (the manual's cover) / "PEACE: 4,297 years" / "WAR: 12,000 years". No: no drawn aliens beyond the antenna skulls; no mug sip (Part 2 just ended on one). Why: it worked once, on a planet that fought even longer, and the tape shows how long 12,000 years is.

## Scene 3 · nations-foam-bats

- id: nations-foam-bats
- act: Why not all at once
- transition_in: zoom into the wall screen
- key: on "last": two politician skeletons on cratered islands pointing at each other, "HE HIT ME LAST" over both skulls, the calendar at YEAR 10,000
- cue: "Your nations have been hitting"
- time: 05:17.6 to 05:23.8 (6.2 s)
- voiceover: "Your nations have been hitting each other for ten thousand years because the other one hit them last."
- layer: B
- scene: Two plain islands across a strait, each with a little capitol and a Politician holding a big orange foam bat. They take turns bonking each other, and every bonk pops a tiny mushroom cloud on the other island. A tear-off calendar on a post in the strait runs the years.
- wishonia: PiP, neutral-smile + body-point-right, then eyeroll-closed + body-arms-crossed on "last."
- props: politician, foam-bat, capitol, calendar, mushroom-cloud
- status: outline

Moves: "Your" → the zoom lands on the two islands; each Politician (the cast's toothy grin, slick hair, flag pin and wide tie, in two skin tones) grips a foam bat. "hitting" → the left one bonks the right one on the head: the head squashes flat and springs back, and a tiny mushroom cloud pops up beside his capitol. "each other" → the right one bonks back; a tiny cloud pops on the left island. "ten thousand" → the calendar's pages rip off in a blur; the bonks speed up; their hair goes white and their beards grow down to their shoes; the capitols crumble into smoking craters. "years" → both x-ray into skeletons, still grinning, still swinging, wide ties still on. "because" → both freeze mid-swing. "last." → both skeletons point at each other, and a speech bubble pops over each: "HE HIT ME LAST". after "last." → they bonk each other at the same moment and get right back to it.

Sound: a boing per bonk and a pop for each tiny cloud; a whirr as the calendar pages fly; faster boings; an x-ray zap on "years"; a record scratch on "because"; a pop for the bubbles; a boing for the last double bonk.

On screen: "YEAR 10,000" (the calendar) / "HE HIT ME LAST" (both bubbles). No: no real flags or country outlines; the islands are plain shapes. Why: the reason for every war, as a playground fight that outlives the players.

## Scene 4 · toddlers-take-nap

- id: toddlers-take-nap
- act: Why not all at once
- transition_in: slide left
- key: after "geopolitics": the toddlers asleep on the rug under the stamped certificate; on the right, the skeletons still bonking under a small mushroom cloud
- cue: "This is the conflict resolution"
- time: 05:23.8 to 05:38.8 (14.9 s)
- voiceover: "This is the conflict resolution strategy of four-year-olds, except four-year-olds eventually get tired and take a nap. Your species invented naps and then refused to apply them to geopolitics."
- layer: B
- scene: A playroom rug: two four-year-olds bonk each other with the same foam bats, get tired and fall asleep under a certificate on the wall; then the frame splits and the politician skeletons from nations-foam-bats are still at it.
- wishonia: PiP, smirk-smile + body-idle, then happy-closed + body-hand-chest on "nap.", then annoyed-frown + body-hands-hips on "refused"
- props: human, foam-bat, rug, certificate, stamp, pillow, politician, mushroom-cloud
- status: outline

Moves: "conflict" → two four-year-olds (one in overalls, one in a dress) bonk each other with the same foam bats, in turns, in the politicians' rhythm. "resolution" → bonk back. "eventually" → the bonks slow down. "tired" → both yawn, mouths wider than their heads; the bats droop. "nap." → they flop onto the rug and fall asleep mid-swing, bats still in hand; Z's rise. "invented" → a framed certificate drops onto the wall above the rug and pins itself up: "NAPS: INVENTED". "naps" → a gold star sticks itself on. "refused" → the frame splits: on the right, the two politician skeletons from nations-foam-bats, beards and wide ties, still bonking, wide awake. "apply" → a fluffy pillow floats down between them; one skeleton bonks it away, and it sails over the split and lands under a sleeping toddler's head. "geopolitics" → a rubber stamp (`KIT.props.stamp`) slams the certificate's second line: "APPLIED TO GEOPOLITICS: NEVER". Then a bonk lands so hard that a small mushroom cloud goes off on the right; the right half shakes; the cloud thins on the skeletons, smoking, still bonking. The toddlers sleep through it.

Sound: a foam squeak per toddler bonk, slowing down; a yawn; a soft thud as they flop; a low snoring hum; a whoosh and a click as the certificate pins up; a sparkle for the star; a whoosh for the split and a boing as the skeletons bonk; the stamp; a boom under the stamp's tail.

On screen: "NAPS: INVENTED" / "APPLIED TO GEOPOLITICS: NEVER". No: nothing hits the toddlers. Why: humans already have the fix, and use it only on children.

## Scene 5 · dog-calculus

- id: dog-calculus
- act: Why not all at once
- transition_in: slide left
- key: on "sit": the dog at the chalkboard, chalk in its mouth, ears on fire, looking at the camera
- cue: "You can't just stop being"
- time: 05:38.8 to 05:45.9 (7.1 s)
- voiceover: "You can't just stop being illogical all at once. That would be like teaching a dog calculus before it learns to sit."
- layer: B
- scene: A plain dog stands on its hind legs at a chalkboard covered in integrals, chalk in its mouth; the Scientist teaches with a pointer; the lesson list in the board's corner has the order wrong.
- wishonia: PiP, thinking-small + body-thinking, then sideeye-closed + body-arms-crossed on "dog"
- props: dog, chalkboard, scientist, flask
- status: outline

Moves: "illogical" → the board is already full of integrals; the dog scribbles another line with the chalk in its mouth. "once." → the Scientist (lab coat, bun, big glasses) taps the board twice with her pointer. "calculus" → the dog adds one more squiggle, and steam whistles out of its ears. "before" → its ears catch fire. "sit" → the dog stops, still standing, ears burning, and looks at the camera. after "sit." → the Scientist empties her bubbling flask over its head: a hiss of steam; the dog, soaked and charred, plops down into a sit.

Sound: chalk scratching; two pointer taps; a steam whistle; a whoosh of fire; a splat of flask water and a sizzle; a thump as it sits.

On screen: "LESSON 1: CALCULUS" / "LESSON 2: SIT" (the board's top corner). No: the dog is a plain dog, not the Democracy Dog of Part 6. Why: the order matters and small steps come first; the dog only sits once it is on fire, and it comes back, sitting, in paint-chips.

## Scene 6 · slider-year-one-to-twenty

- id: slider-year-one-to-twenty
- act: The plan
- transition_in: slide left
- key: after "WHAT": the knob far toward MEDICINE MONEY, the grown human's eyes out on springs, the old Weapons Maker holding up the photo of his missile
- cue: "So this manual shows"
- time: 05:45.9 to 06:14.5 (28.6 s)
- voiceover: "So this manual shows you how to bribe humanity into being less irrational gradually: Year one: Move one percent of murder money to medicine money (baby steps). Year two: "Hey, we didn't die! Let's do two percent!". Year five: "Remember when we spent money on bombs? That was weird.". Year ten: "What's a war?". Year twenty: "We used to WHAT?!"."
- layer: B
- scene: The manual opens into a pop-up slider from "MURDER MONEY" (the Weapons Maker's factory and a pile of war money) to "MEDICINE MONEY" (a hospital), with the color-flip funnel on its knob. Each year war money hops into the funnel and comes out medicine money, the knob moves right, and one human, standing under the funnel's spout, grows a little older.
- wishonia: PiP, happy-smile + body-presenting, then happy-smile + body-counting on "Year" (one), then excited-open + body-excited on "WHAT"
- props: manual, slider-bar, color-flip-funnel, money-war, money-med, sign, factory, conveyor, hospital, weapons-maker, human, missile, mushroom-cloud, pill-bottle, snail
- status: outline

Moves: "manual" → a fresh copy of the manual from wishonia-war-timeline drops onto the paper and flops open. "shows" → the slider pops up out of its pages like a pop-up book: "MURDER MONEY" on the left with the Weapons Maker at his factory (missile chimneys, a conveyor of grinning missiles) and a pile of war money; "MEDICINE MONEY" on the right with a hospital. The knob sits at the murder end. "bribe" → the color-flip funnel drops onto the knob with a clank. "gradually" → the snail from the title card climbs onto the funnel's rim and stays there all scene. "Year one" → a "YEAR 1" tick pops up on the bar; a baby human crawls in under the funnel's spout. "murder money" → one war bill hops off the pile into the funnel, and the Weapons Maker dives under his bench, 1950s duck-and-cover, hands on his hard hat. "medicine money" → the bill pops out of the spout as medicine money (the seal flips from the red missile to the teal cross) into the baby's hands; the knob clicks to "1%". "(baby steps)" → the baby stands, takes one wobbly step and plops onto its diaper. "Year two" → "YEAR 2"; the baby is a toddler. "Hey" → the Weapons Maker peeks out from under the bench. "die" → the toddler pats its own chest, amazed; the Weapons Maker pats himself all over and checks his own pulse. "two percent" → two bills flip; the knob clicks to "2%". "Year five" → "YEAR 5"; five bills flip and the knob slides on; the human is a kid. "Remember" → the Weapons Maker comes over and holds out his old grinning missile, cradled like a baby. "bombs?" → the kid holds it at arm's length, nose wrinkled. "weird." → the kid hands it back. after "weird." → it goes off in the Weapons Maker's arms: a white flash, a mushroom cloud, a shake; he stands there charred black and smoking, hard hat on, hair straight up, still grinning, blinking. "Year ten" → "YEAR 10"; a stream of war bills pours through the funnel and comes out medicine money; the factory's conveyor now carries pill bottles, and its chimneys puff teal smoke; the Weapons Maker, clean again, in a lab coat over his overalls, cradles a grinning pill bottle like a baby. "war?" → the teenager shrugs. "Year twenty" → "YEAR 20"; the knob is far toward teal; the war-money pile is gone and a hill of medicine money stands by the hospital. "used to" → the old Weapons Maker, gray and stooped, holds up a framed photo of his old missile. "WHAT" → the grown human's eyes pop out on springs and his jaw drops to the floor. after "WHAT" → the eyes boing back in.

Sound: a thunk as the manual lands; a rising whistle as the slider pops up; a clank as the funnel lands; a pop for each year's tick; a falling whistle as the Weapons Maker dives; a pop as the bill comes out; a click for each percent; a boing for the diaper plop; pats; pops for the flipping bills; a boom and the whirr of the stream; crickets after "war?"; a rising whistle as the knob slides; two boings and a thunk for the eyes and the jaw.

On screen: "MURDER MONEY" / "MEDICINE MONEY" / "YEAR 1", "YEAR 2", "YEAR 5", "YEAR 10", "YEAR 20" (ticks on the bar) / "1%" / "2%". No: the knob shows only the percentages the narrator says (1% and 2%); later years have no number. No speech bubbles with the year lines (the captions carry them). Why: the plan's pace, slow enough that nobody panics, and the Weapons Maker ends up holding medicine.

## Scene 7 · paint-chips

- id: paint-chips
- act: The plan
- transition_in: slide left
- key: after "option": a bowl of teal peas, the baby smug, the dog under the high chair nosing the last red chip away
- cue: "It's like weaning a baby"
- time: 06:14.5 to 06:28.4 (13.9 s)
- voiceover: "It's like weaning a baby off eating paint chips. You can't just take away all the paint chips at once. They'll cry. You have to gradually replace paint chips with food until they forget paint chips were ever an option."
- layer: B
- scene: A 1950s kitchen. The baby from slider-year-one-to-twenty sits in a high chair eating red paint chips (each with the war seal's little white missile) from a bowl; its mother swaps them for teal peas (each with the medicine seal's little white cross), one at a time. The wall behind has bite-shaped holes where the paint used to be. The dog from dog-calculus sits under the high chair.
- wishonia: PiP, neutral-smile + body-listening, then smirk-smile + body-hands-hips on "option."
- props: human, high-chair, paint-chips, peas, dog
- status: outline

Moves: "It's" → the kitchen: the baby in the high chair, the mother (a 1950s housewife in a dress) beaming beside it, the dog sitting tidily underneath (it learned to sit). "paint chips" (first) → the baby crunches a chip and grins. "all the paint chips" → the mother grabs the whole bowl. "cry." → the baby wails: two jets of tears shoot out sideways like fire hoses, blow the mother's hair straight back and splat the wall; the window cracks; the dog's ears flap. after "cry." → she slams the bowl back; the crying stops at once; the baby beams and crunches. "gradually" → she swaps one red chip for one teal pea. "replace" → another. "food" → faster and faster, a blur. "forget" → the bowl is all teal peas and the baby eats them; a thought bubble over its head shows one red chip, which fades away. "ever" → one red chip is left on the tray; the baby eyes it with suspicion, brows down. "option." → the baby flicks it off the tray with one finger. after "option." → it lands in front of the dog; the dog sniffs it and pushes it away with its nose. The part ends on that frame.

Sound: a crunch; a whoosh as the bowl is grabbed; a wail and a splat; a thunk as the bowl comes back; a pop per swap, speeding up; a whoosh for the thought bubble; a flick; a sniff and a small woof.

On screen: nothing. Why: the same plan in a picture every parent knows: red out, teal in, a little at a time, until even the dog won't touch the old stuff.
