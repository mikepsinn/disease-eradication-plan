---
format: 1920x1080
duration: 1:30.2
message: "Humans cannot stop being illogical all at once, so the plan moves 1% of murder money to medicine money in year one and a little more each year, until war is forgotten."
arc: Title card (a snail pushes the bar to 1%) → Wishonia's dusty manual unfolds 12,000 years of war → the nations bonk each other for 10,000 years and keep going as skeletons → the toddlers nap through a mushroom cloud → a dog doing calculus catches fire → the new manual, a bribe on a spring → the funnel from year 1 to year 20 → paint chips swapped for peas → the dog turns down the last chip
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 3, "The Gradual Irrationality Reduction Program"
audio: index-manual.cbaf659d.mp3, 04:58.2 to 06:28.4
version: v3
---

# Part 3 storyboard: "The Gradual Irrationality Reduction Program"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The episode is a 1950s atomic-age instructional film. Layer A is the host's set: Wishonia at her lectern (`KIT.studio`), talking to the viewer. Layer B is an illustrated plate the camera travels over (`KIT.camera`), one framing per phrase; Wishonia is only the voice there. Money is green, and its seal says what it buys (`KIT.money("war")`: a missile seal; `KIT.money("med")`: a cross seal). Part 2 (`../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Spine.** A little at a time. Wishonia's planet fought for 12,000 years (host-opens); Earth's nations bonk each other for 10,000 years and outlive themselves doing it, while its toddlers tire and nap (the-strait); a dog taught calculus before sitting catches fire (the-classroom); the plan moves war money through the color-flip funnel, one bill in year one, a stream by year ten (the-funnel); and a mother swaps paint chips for peas one at a time (the-kitchen). The snail is the pace: it pushes the title card's bar to 1% and sets off across the lectern in host-manual. The plain tan dog carries the part's end: it learns to sit in dog-calculus, sits under the high chair in paint-chips, and turns down the last paint chip in host-closes.

**Callbacks.** From Part 1 (meet-wishonia): the wrecked unit converter's bell dings once offstage on "four thousand" in host-opens. From Part 1 (without-with-papers) and Part 2 (money-loop): the moth from the empty wallet and the empty press tray flutters out of Wishonia's old manual in host-opens. From Part 2 (money-loop): the Weapons Maker cradling his smiling missile at the factory with missile chimneys; here it goes limp in his arms like a deflated balloon, and he ends up cradling a pill bottle. Inside the part: the toddlers bonk with the nations' orange foam bats; the old dusty manual of host-opens stands next to the new one in host-manual; the paint chips carry the war seal's missile and the peas the medicine seal's cross.

**Set up here.** The snail (title-card, host-manual) carries the sum in Part 17 (the-arithmetic), where a dangling paper makes it rocket off: draw it from the snail in the old `../compositions/scenes/part-03/irrationality-reduction-title.html`. The color-flip funnel (`KIT.props.colorFlipFunnel`) makes its first film-look appearance in year-one-to-twenty; Part 13's leaders drop their papers into it. The two Politicians wear one red tie and one blue tie (the bible's red team / blue team gag, Part 6).

**Held frame.** None: this part has no death toll. Its stillest beat is the end of toddlers-take-nap, after "geopolitics.", where the toddlers sleep on under the thinning cloud.

**Transitions.** The title card comes up from black and goes down to black; host-opens irises in on Wishonia's face. Cut to the-strait; toddlers-take-nap continues on the same plate (no seam: the camera keeps traveling from the islands to the house). Cuts from there to the-classroom, to host-manual, to the-funnel, to the-kitchen and back to the set. host-closes irises out on her face to black, so Part 4's title card comes up from black.

**Bans for this part.**
- The islands are plain shapes and the capitols the library's generic dome: no real flags, country outlines or buildings.

## Changes from v2

- The office, its wall screen, the cream diagram paper and Wishonia's corner are gone: she talks from her lectern in three host shots (host-opens, host-manual, host-closes), and the humans act on four plates the camera travels over (the-strait, the-classroom, the-funnel, the-kitchen).
- wishonia-war-timeline is now host-opens: the 12,000-year tape is a fold-out that drops out of her own dusty copy of the manual and piles up beside the lectern, a moth flies out of the book, and the PEACE and WAR labels are gone.
- nations-foam-bats and toddlers-take-nap share one plate: the split screen became a pull-back that holds the sleeping toddlers in front and the bonking skeletons behind; the NAPS certificate and its stamp became a winged pillow the skeletons bat away; the HE HIT ME LAST bubbles became the two skeletons pointing at each other.
- slider-year-one-to-twenty is split: host-manual (Wishonia shows the new edition, a bill boings out of it, the snail sets off) and year-one-to-twenty, one plate from the factory's money mountain through the color-flip funnel to the hospital. The knob's percentages and the year ticks became bills (one, two, five, a stream) and a tear-off calendar.
- dog-calculus drops its lesson list: a pull-back from the crowded board to the dog is the reveal.
- paint-chips hands its last line to host-closes: the dog trots into the studio with the chip already balanced on its nose, turns it down, and the film irises out on Wishonia.

## Scene 1 · title-card

- id: title-card
- act: Title
- transition_in: up from black (Part 2 irises out to black)
- key: after "Program.": the whole heading in, IRRATIONALITY straight at last, the bar reading 1% and the snail sitting down at its left end, wiping its brow
- cue: "The Gradual Irrationality Reduction Program"
- time: 04:58.2 to 05:02.3 (4.1 s)
- voiceover: "The Gradual Irrationality Reduction Program."
- layer: A, title card
- scene: The period title card (`KIT.titleScene`): the heading in cream on plain navy under the film's emblem, whose three war papers run round their orbits as in Part 2. Heading lines, 16:9: "THE GRADUAL" (small) / "IRRATIONALITY" / "REDUCTION PROGRAM"; 9:16: "THE GRADUAL" (small) / "IRRATIONALITY" / "REDUCTION" / "PROGRAM". Under the heading, a long empty progress bar, and a snail at its left end pushing the fill. The heading sits a little smaller and higher than Part 2's so the bar clears y 900 (16:9) and y 1450 (9:16).
- props: title-card, snail, progress-bar, money-war
- status: planned

Moves: "Gradual" → the card comes up from black; THE and GRADUAL fade in slowly, each word taking about 0.8 s to settle (the slowest title card in the film), and the snail is already straining at the bar's left end: its body stretches, its shell rocks, a bead of sweat comes up. "Irrationality" → IRRATIONALITY fades in crooked and spends the rest of the card slowly straightening itself. "Reduction" → REDUCTION fades in. "Program." → PROGRAM settles with a thunk and the line shudders. after "Program." → the bar's readout ticks from "0%" to "1%", a sliver of fill; the snail stops, wipes its brow with an eye stalk, flicks the sweat off and sits down for a rest. The card goes down to black.

Sound: the title card's whirr on "Gradual"; a thunk as PROGRAM settles; a tick at 1%.

On screen: "THE GRADUAL IRRATIONALITY REDUCTION PROGRAM" / "0%", then "1%". Why: the narrator reads the heading, and the snail at 1% is the plan's pace before anyone explains it.

## Scene 2 · host-opens

- id: host-opens
- act: How Wishonia's planet did it
- transition_in: iris in on Wishonia's face (the title card ends on black)
- key: on "nobody": Wishonia shrugging over her dusty old manual, its red fold-out hanging down the lectern and heaped beside it to lectern height, a row of grinning antenna skulls along the panels
- cue: "We ended wars using"
- time: 05:02.3 to 05:17.6 (15.4 s)
- voiceover: "We ended wars using this exact program four thousand, two hundred and ninety-seven years ago. Before that we'd been fighting for twelve thousand years, which now seems like quite a long time to do something nobody enjoyed."
- layer: A, host
- scene: The host's set (`KIT.studio`). Standing on the right end of the lectern top is Wishonia's own copy of the manual (`KIT.props.manual`, aged): the theme song's orange book faded to tan, dusty, a cobweb across one corner, the other corner chewed. Out of its back drops a fold-out: a long strip of red paper folded like a road map, each panel carrying a tiny grinning skull with two antennae and ball tips (Wishonia's ancestors). It unfolds down the lectern's right side and piles up in zigzags on the free wall to the right of it.
- wishonia: big, happy-smile + body-hand-chest; thinking-closed + body-thinking on "Before"; skeptical-closed + body-shrug on "nobody"
- props: studio, lectern, manual (old copy), cobweb, moth, fold-out strip, antenna skulls
- status: planned

Moves: "We" → the iris opens on her face; the old manual already stands on the lectern beside her. "exact" → the book wobbles and a puff of dust rolls off it. "four thousand" → offstage, the wrecked converter's bell (Part 1) dings once; the dust settles, and she smiles at the book. "ago." → its cover creaks open by itself and a moth flutters out of the pages (the moth from Part 1's empty wallet and Part 2's empty press tray) and flaps slowly up out of the frame. "Before" → a fold-out drops out of the back of the book: a red strip folded like a road map, a tiny grinning antenna skull on its first panel. "twelve thousand" → it unfolds down the side of the lectern, panel after panel, skull after skull, and runs off the bottom of the frame. "which now seems" → it keeps coming: the folds pile up beside the lectern in zigzags, the heap rising into the frame from below. "quite a long time" → the heap reaches the lectern top. "nobody" → Wishonia shrugs over it. "enjoyed." → the whole strip zips back up into the book like a tape measure, the skulls whipping past, the last one waving bye-bye on its way in; the book slams shut and hops on the lectern. after "enjoyed." → one last wisp of dust.

Sound: a huff of dust on "exact"; a single bell ding, small and offstage, on "four thousand"; a typewriter clatter as the panels flap down on "twelve"; a whoosh as the strip zips back on "enjoyed." and a slam a beat later as the book shuts.

On screen: the old book's own cover lettering, faded. No: no numbers, timeline or labels on the strip; its length is the joke. Why: the program worked once, on a planet that fought even longer, and 12,000 years of war is more paper than the studio holds.

## Scene 3 · nations-foam-bats

- id: nations-foam-bats
- act: Why not all at once
- transition_in: cut
- key: on "last.": two grinning politician skeletons on cratered, smoking islands, wide ties and long white beards still on, each pointing a bony finger at the other across the strait; the calendar in the water stopped at 10,000
- cue: "Your nations have been hitting"
- time: 05:17.6 to 05:23.8 (6.2 s)
- voiceover: "Your nations have been hitting each other for ten thousand years because the other one hit them last."
- layer: B, plate the-strait
- scene: Plate the-strait: a calm sea under a pale sky. Up and to the right, across the water, two small islands face each other over a narrow strait, each with a little domed capitol (`KIT.props.capitol`) and a Politician (`KIT.cast("politician")`, two skin tones, one in a red tie and one in a blue tie) holding an orange foam bat long enough to reach the other island. A tear-off calendar (`KIT.props.calendar`, its band reading "YEAR") stands on a post in the water between them. Down and to the left, on the near shore, a 1950s house drawn as a cutaway, its playroom open to us (toddlers-take-nap). The islands are drawn small (far) and the house large (near), so a wide view can hold both.
- props: politician (x2), foam-bat (x2), capitol (x2), calendar, nuke (tiny), skeleton (xray)
- status: planned

Moves: "Your" → the camera frames the two islands; the Politicians (the cast's toothy grin, slick hair, flag pin) face each other across the water, bats on their shoulders. "hitting" → the left one swings his bat across the strait and bonks the right one on the head: the head squashes flat and springs back, and a tiny mushroom cloud pops up behind the right capitol. "each other" → the right one bonks back; a tiny cloud pops on the left island. "ten thousand" → the bonks speed up to a blur; the calendar's pages fly off in a blizzard, its number racing up; their hair goes white and their beards grow down to their shoes; the capitols crumble into smoking craters under a crowd of tiny clouds. "years" → both x-ray into grinning skeletons, beards and wide ties still on, still swinging. "because" → both freeze mid-swing; the calendar stops on "10,000"; the camera pushes in. "last." → each skeleton points a bony finger at the other. after "last." → they bonk each other at the same moment, both skulls squash, and they get right back to it.

Sound: a boing per bonk and a pop for each tiny cloud; a whirr as the calendar pages fly; an x-ray zap on "years"; a record scratch on "because"; a boing for the double bonk.

On screen: the calendar: "YEAR" over its number, stopping at "10,000". No: no speech bubbles; the two pointing fingers say it. Why: the reason for every war, as a playground fight that outlives the players.

## Scene 4 · toddlers-take-nap

- id: toddlers-take-nap
- act: Why not all at once
- transition_in: same plate (no seam): the camera travels from the islands to the house
- key: after "geopolitics.": the wide view: two toddlers asleep on the playroom rug, bats in hand, the winged pillow under one's head; across the water, the skeletons still bonking under a small mushroom cloud
- cue: "This is the conflict resolution"
- time: 05:23.8 to 05:38.8 (14.9 s)
- voiceover: "This is the conflict resolution strategy of four-year-olds, except four-year-olds eventually get tired and take a nap. Your species invented naps and then refused to apply them to geopolitics."
- layer: B, plate the-strait
- scene: The same plate. The camera travels down and left across the water to the cutaway house on the near shore: a playroom with a round rug and toy blocks, where two four-year-olds (everyday humans with big heads and short legs, one in overalls, one in a dress) hold the same orange foam bats. At the end it pulls back to hold both: the playroom large in front, the islands small behind.
- props: human (two toddlers), foam-bat (x2), house (cutaway), rug, toy blocks, pillow (with wings), politician skeletons, nuke
- status: planned

Moves: "This" → the camera leaves the bonking skeletons and travels down and left across the water to the house, into the open playroom. "resolution" → two four-year-olds bonk each other with the same orange foam bats, in turns, in the politicians' rhythm; each bonked head squashes and springs back. "four-year-olds," → bonk back. "eventually" → the bonks slow down. "tired" → both yawn, mouths wider than their heads; the bats droop. "nap." → they flop onto the rug asleep mid-swing, bats still in hand; Z's rise. "invented" → the camera pulls back out of the house: the toddlers asleep in front, and across the water behind them the skeletons still bonking. "naps" → a fluffy white pillow sprouts two little wings and flutters up out of the playroom like a dove of peace, out across the water toward the islands. "refused" → it reaches the skeletons, and one bats it away with his foam bat without even looking. "apply" → it sails back across the water and lands softly under a sleeping toddler's head; the toddler snuggles into it. "geopolitics." → the other skeleton's next bonk lands so hard a mushroom cloud goes off over the islands, and the frame shakes. after "geopolitics." → the cloud thins on the two skeletons, smoking, still bonking. The toddlers sleep through it.

Sound: a foam squeak per toddler bonk, slowing down; a yawn (a huff) on "tired"; a soft thud on "nap." and a little snoring hum after it; a whoosh as the pillow takes off on "naps"; a boing as it is batted away on "refused"; the boom on "geopolitics.".

On screen: nothing new. No: no certificate, stamp or split screen; the pull-back holds both halves in one picture. Why: humans already have the fix and use it only on children.

## Scene 5 · dog-calculus

- id: dog-calculus
- act: Why not all at once
- transition_in: cut
- key: on "learns": the dog on its hind legs at the chalkboard, chalk in its mouth, ears on fire, staring at the camera; the Scientist beside it raising her bubbling flask
- cue: "You can't just stop being"
- time: 05:38.8 to 05:45.9 (7.1 s)
- voiceover: "You can't just stop being illogical all at once. That would be like teaching a dog calculus before it learns to sit."
- layer: B, plate the-classroom
- scene: Plate the-classroom: a cream schoolroom wall with a big wood-framed slate chalkboard crammed edge to edge with chalk integrals and sums, a chalk tray, a plank floor. The Scientist (`KIT.cast("scientist")`: lab coat, bun, big glasses) stands at the board's right end with a pointer and her bubbling flask. A plain tan dog (the mutt of the old `../compositions/scenes/part-03/dog-calculus.html`, its DOG block; not the Democracy Dog) stands on its hind legs at the board, writing with a stick of chalk in its mouth.
- props: chalkboard, chalk, scientist, pointer, flask, dog
- status: planned

Moves: "You" → close on the board: chalk integrals crammed edge to edge, and a fresh line squeaks on, fast. "illogical" → another line, faster; chalk dust flies. "once." → another; the board is full. "teaching" → the camera pulls back: the one writing is a dog, standing on its hind legs with the chalk in its mouth; the Scientist taps the board twice with her pointer. "calculus" → the dog scribbles faster, and steam whistles out of its ears. "before" → its ears catch fire. "learns" → it stops dead, ears burning, and looks at the camera; the camera pushes in. "sit." → the Scientist upends her bubbling flask over its head: a splash and a hiss of steam. after "sit." → soaked and charred, blinking, the dog plops down into a perfect sit, its stub tail thumping once.

Sound: chalk squeaks on "You"; a steam whistle on "calculus"; a whoosh of fire on "before"; a splat and a sizzle on "sit.".

On screen: the chalk sums, as a picture of calculus. No: no lesson list on the board. Why: the order matters, and the dog only sits once it is on fire; it comes back, sitting, in paint-chips and host-closes.

## Scene 6 · host-manual

- id: host-manual
- act: The plan
- transition_in: cut
- key: on "gradually": Wishonia at the lectern looking down at the snail as it sets off along the lectern top; the new manual open beside the old dusty one, a green medicine bill boinging on a spring out of its pages
- cue: "So this manual shows"
- time: 05:45.9 to 05:52.9 (7.0 s)
- voiceover: "So this manual shows you how to bribe humanity into being less irrational gradually:"
- layer: A, host
- scene: The host's set. On the lectern top: the old dusty copy from host-opens and, new beside it, a fresh copy of the manual (`KIT.props.manual`, the theme song's orange book), gleaming.
- wishonia: big, happy-smile + body-presenting; smirk-smile + body-open-palms on "bribe"; lookright-smile + body-idle on "gradually:" (the lookright head looks to screen left, so the snail comes in on that side)
- props: studio, lectern, manual (new and old), money-med, spring, snail
- status: planned

Moves: "So" → cut in: the new copy stands on the lectern next to the old dusty one. "manual" → a sparkle runs across its cover. "bribe" → its cover swings open and a fat green bill with a cross seal boings up out of the pages on a spring, like a jack-in-the-box, and keeps wobbling. "gradually:" → the snail from the title card climbs up over the lectern's left edge and sets off along the top, toward the books. after "gradually:" → Wishonia looks down at it; it has gone about a finger's width.

Sound: a sparkle on "manual"; a boing on "bribe".

On screen: the new manual's cover ("HOW TO END WAR AND DISEASE", the prop's own lettering). Why: the plan is a bribe, it comes in a book, and it goes at the snail's pace on purpose.

## Scene 7 · year-one-to-twenty

- id: year-one-to-twenty
- act: The plan
- transition_in: cut
- key: on "WHAT": year 20, the war-money mountain gone, a hill of medicine money by the hospital, the old stooped Weapons Maker holding out a framed photo of his missile, the grown human's eyes out on springs and his jaw on the ground
- cue: "Year one"
- time: 05:52.9 to 06:14.5 (21.6 s)
- voiceover: "Year one: Move one percent of murder money to medicine money (baby steps). Year two: "Hey, we didn't die! Let's do two percent!". Year five: "Remember when we spent money on bombs? That was weird.". Year ten: "What's a war?". Year twenty: "We used to WHAT?!"."
- layer: B, plate the-funnel
- scene: Plate the-funnel, a plain tan field like Part 2's. Left: the Weapons Maker's factory (`KIT.props.factory`, no sign: its chimneys are three grinning missiles), a mountain of war money heaped in front of it and his workbench beside it. Middle: the color-flip funnel (`KIT.props.colorFlipFunnel`) standing on the field, and a tear-off calendar on a post beside it, its band reading "YEAR". Right: a hospital (`KIT.props.hospital`), where the medicine money piles up. One human grows up at the funnel's spout: a baby, a toddler, a kid, a teenager, a grown man (one drawing per year, swapped on "Year").
- props: factory, money-war (mountain), workbench, weaponsMaker, missile (cradled, then deflated), colorFlipFunnel, calendar, money-med, human (five ages), conveyor, pillBottle, lab coat, photo frame, hospital
- status: planned

Moves: "Year" → the camera opens on the funnel standing in the field, the calendar beside it on "1". "one:" → a baby crawls in between the funnel's legs and sits under the spout. "Move" → the camera pulls back left: the factory with its three missile chimneys, the mountain of war money in front of it, and the Weapons Maker (`KIT.cast("weaponsMaker")`) at his workbench, cradling his smiling missile. "murder money" → one war bill hops off the top of the mountain, trots over and dives into the funnel's mouth; the Weapons Maker dives under his workbench, 1950s duck-and-cover, hands over his hard hat. "medicine money" → the camera pushes in on the spout: the bill walks out with a cross on its seal and climbs into the baby's hands. "(baby steps)." → the baby stands, takes one wobbly step and plops onto its diaper. "Year two:" → the calendar flips to "2"; the baby is a toddler. "Hey," → the Weapons Maker peeks out from under the bench. "die!" → he pats himself all over and checks his own pulse; the toddler pats its own chest, amazed. "two percent!" → two bills hop off the mountain, through the funnel and out as medicine money. "Year five:" → "5"; five bills; the toddler is a kid in short trousers. "Remember" → the Weapons Maker walks over to the funnel and holds his smiling missile out to the kid, cradled like a baby. "bombs?" → the kid holds it at arm's length, nose wrinkled. "That" → the kid hands it back. "weird." → back in his arms, the missile goes down like a balloon with a long squeal, its grin sagging, until it hangs over his forearms like a wet sock. after "weird." → he looks down at it, then at the kid. "Year ten:" → the calendar flips to "10"; a stream of war bills pours off the mountain through the funnel and out as medicine money; the camera pulls back past the factory: its conveyor now carries pill bottles and its missile chimneys puff teal smoke. "What's" → the Weapons Maker, in a lab coat now, strolls past cradling a grinning pill bottle like a baby. "war?" → the teenager shrugs. after "war?" → crickets. "Year twenty:" → "20"; the camera pulls back to the whole plate: the war-money mountain is gone, and a hill of medicine money stands by the hospital. "used to" → the Weapons Maker, old, gray and stooped, holds out a framed photo of his old missile to the grown man. "WHAT?!" → the grown man's eyes shoot out on springs and his jaw drops to the ground; the camera pushes in. after "WHAT?!" → the eyes boing back in.

Sound: a tick for each calendar flip on "Year"; a falling whistle as the Weapons Maker dives on "murder"; a ding as the first seal flips on "medicine"; a boing for the diaper plop; pats on "die!"; a deflating squeal on "weird."; crickets after "war?"; a boing for the eyes on "WHAT?!" and another as they snap back.

On screen: the calendar: "YEAR" over "1", "2", "5", "10", "20". No: no percentages, ticks or labels; the number of bills is the percentage. Why: the plan's pace, slow enough that nobody panics, and the Weapons Maker ends up holding medicine.

## Scene 8 · paint-chips

- id: paint-chips
- act: The plan
- transition_in: cut
- key: on "cry.": the baby wailing in the high chair, two jets of tears shooting out sideways like fire hoses, one blowing the mother's hair straight back as she holds the bowl out of reach, the other splatting the bitten red wall; the dog under the chair, ears flapping
- cue: "It's like weaning a baby"
- time: 06:14.5 to 06:24.4 (9.9 s)
- voiceover: "It's like weaning a baby off eating paint chips. You can't just take away all the paint chips at once. They'll cry. You have to gradually replace paint chips with food"
- layer: B, plate the-kitchen
- scene: Plate the-kitchen: a 1950s kitchen with a checkered floor and a window. The wall behind the high chair is painted war red and bitten bare in patches, with little tooth marks round each hole (the baby has been eating the wall). In the high chair a baby (an everyday human, big head, bib) eats red paint chips, each carrying the war seal's little missile in cream, from a bowl on its tray. Its mother (an everyday human in a dress and apron) stands beside it. The tan dog from dog-calculus sits tidily under the high chair: it learned to sit.
- props: high-chair, human (baby, mother), bowl, paint-chips, peas, dog, window
- status: planned

Moves: "It's" → the kitchen: the baby crunching a red paint chip and grinning, the mother beaming, the dog sitting under the chair. "chips." → the baby crunches another; crumbs fly. "take" → the mother picks up the bowl. "all" → she lifts it high, out of reach. "cry." → the baby wails: two jets of tears shoot out sideways like fire hoses; one blows the mother's hair straight back, the other splats the wall and cracks the window; the dog's ears flap in the spray. after "cry." → she slams the bowl back on the tray; the crying stops at once, and the baby beams and crunches. "gradually" → she swaps one red chip for one teal pea, each pea carrying the medicine seal's little cross. "replace" → another. "chips" (fourth) → another, faster. "food" → a blur of swaps: the bowl is all teal peas, and the baby eats them happily without noticing.

Sound: a crunch on "chips."; a whoosh as the bowl goes up on "all"; a wail and a splat on "cry."; a slam as the bowl comes back after it; a pop for each swap from "gradually".

On screen: nothing. No: the chips and peas are paint and food, not money, so they keep their red and teal. Why: the same plan in a picture every parent knows: red out, teal in, a little at a time.

## Scene 9 · host-closes

- id: host-closes
- act: The plan
- transition_in: cut
- key: on "option.": Wishonia giving the dog the side-eye; the dog sitting beside the lectern with its nose in the air and its eyes shut, the red paint chip it brought in on its nose flicked off and tumbling away
- cue: "until they forget"
- time: 06:24.4 to 06:28.4 (3.9 s)
- voiceover: "until they forget paint chips were ever an option."
- layer: A, host
- scene: The host's set, with the tan dog from the kitchen as the guest: it trots in from the right with a red paint chip already balanced on its nose and sits on the free wall beside the lectern.
- wishonia: big, happy-smile + body-presenting; sideeye-closed + body-idle on "option."
- props: studio, lectern, dog, paint-chip
- status: planned

Moves: "until" → the dog trots into the studio from the right, nose high, a red paint chip balanced on the end of it like a treat in a dog trick, and sits beside the lectern, tidy, chest out. "paint" → the chip teeters; the dog freezes and steadies it. "ever" → the dog crosses its eyes at it. "option." → it flicks the chip off its nose with a snort, turns its nose up and shuts its eyes; Wishonia side-eyes it. after "option." → the iris closes on her face, and the part ends on black.

Sound: soft paw pats as the dog trots in on "until"; a snort (a huff) on "option.".

On screen: nothing. No: no bowl and no baby; the dog is the test. Why: even the dog won't touch the old stuff, which is the plan's finish line.
