---
format: 1920x1080
duration: 2:12.1
message: "The fix is one treaty: every country moves 1% of its military budget to clinical trials at the same time, and humans have already signed treaties that asked for more."
arc: Title card (a war paper hops through the 1% and comes out medicine) → every leader drops one paper into the funnel at once, and the treaty fits on one line → the invasion objection, imagined and answered → 121 apocalypses go off instead of 122 → the treaties you signed (the landmine one goes off) → 847 folders, teal or burnt, and Earth's still smoking → the cuckoo snapped in the book → 200,000 years of flicking off the mold → the fat cat runs the greed plant
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 13, "The Solution: A 1% Treaty"
audio: index-manual.cbaf659d.mp3, 25:42.0 to 27:54.0
version: v2
---

# Part 13 storyboard: "The Solution: A 1% Treaty"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The 1%. Every scene takes one small piece off something big: one paper off the top of every leader's stack of war papers (through the color-flip funnel, where the red missile seal turns into the teal cross), one missile off each heap, one snowflake off the 122, one fourth scroll that asks for 1% fewer. In 847-civilizations, the planets that listened are the ones whose folders show the same flip.

**The leaders.** Every leader is the politician (`KIT.cast("politician")`: the toothy grin, the slick hair, the wide tie) in a plain sash with no emblem, in all four skin tones and four sash colors. The two in enemies-will-invade are two of the ring in every-leader-at-once, with the same options, so they are the same men.

**YOU.** The viewer is the busy human in the bowler from Part 1's title card, as in Parts 10 and 12 (`{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene). He walks the papers to the leaders in every-leader-at-once (the viewer does the persuading), and he is the one reader in next-page who turns to page 2.

**Running gag: the treaty is one line.** The 1% treaty is a scroll with one line of text on a lot of empty paper (`KIT.props.scroll({ text: "THE 1% TREATY", lines: ["Redirect 1% of military spending to clinical trials."], signatures: 0, wax: false })`). It unrolls over the globe in every-leader-at-once and comes back in treaties-you-signed as the fourth scroll, next to three crowded with signatures.

**Running gag: "crazy".** Each time the narrator says "crazy", a carved wooden cuckoo-clock bird pops out on a spring and cuckoos: out of the North Pole in every-leader-at-once, out of page 1 of the manual in next-page, where the reader snaps the book shut on it.

**Callbacks from Part 1.** one-twenty-one-apocalypses brings back the grid of 122 red snowflakes and its counter from nuclear-winters, and this time the 121 go off. bread-mold is the cave and the two cavemen of fire-on-fire. The burnt folder in 847-civilizations shows split-the-atom's two humans pointing their atoms at each other, as grinning skeletons. 847-civilizations uses earth-means-dirt's office with the filing cabinet (the wall screen moved right in 16:9).

**Callback from Part 12.** The Earth case file lies on Wishonia's desk in 847-civilizations where suboptimal-stamp left it, tab "~~EARTH~~ DIRT: CASE #847", stamped "MAY BE ELIGIBLE FOR OPTIMIZATION" and "SUBOPTIMAL". Earth is case 847 of the 847: on "Some didn't." its corner starts to smoke, and it stays undecided.

**Callback set up here.** In human-greed, a bond certificate (`KIT.props.bond()`, default options) slides onto the wall screen on "financial instrument". Part 17 pays it off: Wishonia slaps the same certificate on the desk in financial-instrument.

**Held frame.** 847-civilizations, from "themselves." to "The" in next-page (1.2 s): the ash settles and nothing moves. A HOLD is silent.

**Bans for this part.**
- No real people or logos. The leaders wear plain sashes, never real flags.
- No real banknotes, weapons models, treaty documents, emblems or seals; the banned weapons are silly objects (a grumpy gas canister, a germ, a plain landmine disc), the missiles are the grumpy library missile with price tags.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.

## Changes from v1

- The humans are the stereotype cast: the leaders are the politician in plain sashes, YOU walks the persuading papers, the scientist runs the lab, the weapons maker mourns the weapons humans like, the fat cat runs the greed plant; the crowd and the cavemen are everyday humans whose bodies come from their outfits.
- Money: the leaders stand on stacks of war papers (green, red missile seal), the persuading papers are plain green, and the funnel flips war papers to medicine papers (teal cross).
- Every threat pays off on screen: the imagined invasion chars each leader inside his own thought bubble, the 121 apocalypses we keep go off in the snowflake grid, the landmine treaty blows up its signer, the extinct planets are grinning skeletons, the cavemen x-ray into skeletons during 200,000 years of not noticing the mold, and the fat cat catches fire in the greed wheel and keeps running.
- every-leader-at-once slides in from the title card (the card is not the office, so there is no wall screen to zoom into).
- treaties-you-signed: the scrolls slam down on the weapons they ban; three with a twist (squash, splat, boom).
- next-page: YOU turns to page 2.
- New running gags: the one-line treaty and the "crazy" cuckoo.
- On-screen text cut to the labels that are themselves jokes (the equation "122 − 1 = 121" and the treaty years and counts are in the captions).
- Props use the shared library names; Sound lines added.

## Scene 1 · one-percent-treaty-title

- id: one-percent-treaty-title
- act: Title
- transition_in: cut (the parts are rendered on their own and joined)
- key: after "Treaty.": both lines in, the "1%" in teal, the paper bowing to the right of the "%" with its new teal cross seal
- cue: "The Solution. A one percent"
- time: 25:42.0 to 25:45.4 (3.4 s)
- voiceover: "The Solution. A one percent Treaty."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`): "THE SOLUTION" slams in, "A 1% TREATY" slides up under it, and a war paper goes through the "%" and comes out medicine.
- wishonia: not on screen
- props: titleScene, money("war"), money("med")
- status: outline

Moves: "The" → "THE" slams in. "Solution." → "SOLUTION" slams in. "A" → the second line (style small) slides up word by word on "A", "one" ("1%", in teal) and "Treaty.". "percent" → a war paper (green, red missile seal) trots in along the second line from the left. "Treaty." → it hops into the top ring of the "%", drops through the slash and pops out of the bottom ring with a teal cross seal. after "Treaty." → it bows.

Sound: a thunk on "THE", on "SOLUTION", on "1%" (the alignment puts "A" and "one" 0.02 s apart, so the pair gets one thunk) and on "TREATY"; squeaky footsteps as the paper trots; a boing as it hops in; a sparkle as it comes out teal.

On screen: "THE SOLUTION" / "A 1% TREATY". Why: the narrator reads the heading, and the paper does the whole plan in one hop.

## Scene 2 · every-leader-at-once

- id: every-leader-at-once
- act: The treaty
- transition_in: slide left (the title card is not the office)
- key: on "redirect": every leader's top paper in the air over the funnel at the same moment, the late leader a beat behind
- cue: "This is going to sound"
- time: 25:45.4 to 25:57.8 (12.4 s)
- voiceover: "This is going to sound crazy. But you're going to use those papers to persuade the leader of every country on Earth to simultaneously redirect one percent of its military budget to clinical trials. That's it. That's the treaty."
- layer: B
- scene: An engraved Earth ringed by leaders, each standing on a tall stack of war papers; YOU walks a pack of plain papers up to them; all the leaders drop their top paper into one big funnel at once, and medicine papers march out of the spout into the scientist's lab.
- wishonia: PiP, smirk-smile + body-presenting, then happy-smile + body-open-palms on "That's"
- props: earthGlobe, politician (the ring of leaders), YOU, money("plain"), money("war"), money("med"), colorFlipFunnel, lab, scientist, scroll, cuckoo
- status: outline

Moves: "crazy." → the bare globe; the cuckoo pops out of the North Pole on its spring, cuckoos once and springs back in; the PiP grins. "papers" → YOU walks in at the globe's edge with a pack of plain green papers on leashes, trotting like small dogs. "persuade" → YOU lets go of the leashes and the papers scatter all round the globe. "every country" → a leader pops up out of every country, all round the rim, each standing on a tall stack of war papers; each catches a plain paper and his eyes turn to dollar signs. "simultaneously" → every leader lifts the top paper off his stack at the same moment, like a chorus line; one leader at the back is a beat late, and the others turn their heads and glare at him. "redirect" → the top papers all fly in arcs into one big funnel over the globe, labeled "1%". "one percent" → inside the funnel's window the red missile seals flip to teal crosses. "clinical trials." → medicine papers march out of the spout to the lab bench, where the scientist holds up her bubbling flask and waves them in; the bench's round flask boils over in a puff. "That's it." → the leaders dust off their hands; each stack is one paper shorter. "That's" (second) → the treaty scroll snaps down over the globe like a window blind: one line at the top, then empty paper. "treaty." → its bottom roll keeps going and bonks the late leader on the head; stars circle it.

Sound: a boing and a squeak for the cuckoo; squeaky footsteps for the papers; a whoosh as they scatter; a pop for each leader; a cash-register ding as their eyes turn to dollars; a rising whistle as the papers lift; a whoosh into the funnel; a ding as the seals flip; squeaky marching; a pop as the flask boils over; a pat for the dusted hands; a whoosh for the scroll; a boing for the bonk.

On screen: funnel label "1%" / the scroll "THE 1% TREATY: Redirect 1% of military spending to clinical trials." No: no flags or national symbols on the sashes or the globe. Why: the whole plan in one picture, the color flip's home, and the treaty fits on one line.

## Scene 3 · enemies-will-invade

- id: enemies-will-invade
- act: The objections
- transition_in: slide left
- key: on "same time": both leaders hold one missile in the air, smiling awkwardly at each other, their thought bubbles gone
- cue: "After the craziness objection"
- time: 25:57.8 to 26:14.6 (16.7 s)
- voiceover: "After the craziness objection, the second objection every human has: "But if we cut our military budget, our enemies will invade us!". Everyone cuts one percent at the same time. Your national security actually *increases*, because everyone has one percent fewer missiles pointed at them."
- layer: B
- scene: Two of the leaders face each other over a garden fence, each behind a heap of price-tagged grumpy missiles aimed across it; each imagines the other invading, then both lift one missile off at the same moment.
- wishonia: PiP, skeptical-smile + body-arms-crossed, then smirk-smile + body-point-right on "increases"
- props: politician (two of the ring), missile, priceTag, sign, gauge, KIT.nuke (in the thought bubbles)
- status: outline

Moves: "After" → the two leaders, each behind his heap, on either side of a picket fence; every missile scowls across it. "second objection" → a sign "OBJECTION 2" springs up on the fence post. "enemies" → each leader peeks over the fence at the other and narrows his eyes. "invade" → a thought bubble puffs up over each: in it, the other leader climbs over the fence with his whole heap, and it goes off. "us!"." → in both bubbles a white flash and a little mushroom cloud; when it clears, the thinker stands in his own bubble charred black and smoking, hair straight up, blinking. The real leaders hug their heaps tighter and shake. "Everyone" → the bubbles pop; both reach for the top missile. "same time." → both lift it off together and smile awkwardly at each other. "security" → a gauge on each side, "SECURITY", with a hundred marks. "increases" → both needles tick up one mark; after "increases" → both leaders throw their arms up and cheer as if they had won the war. "fewer missiles" → they set their missiles on the fence top between them; each heap now has one gap. "pointed" → the two missiles on the fence look at each other, shrug, and shake fins.

Sound: a pop as the sign springs up; a whoosh as the bubbles puff; a boom inside the bubbles; a sizzle; a pop as the bubbles burst; one clank as both missiles lift in step; two ticks for the needles; a whistle for the cheer; a thunk as the missiles land on the fence; a squeak as they shake fins.

On screen: "OBJECTION 2" / gauges "SECURITY". Why: the objection answered by one move both sides make at once; the invasion goes off, but only in their heads.

## Scene 4 · one-twenty-one-apocalypses

- id: one-twenty-one-apocalypses
- act: The objections
- transition_in: slide left
- key: after "twenty-one": the grid counter on 121, the stray snowflake hovering clear of the grid, the tall stack running out of the top of the frame
- cue: "And if you still"
- time: 26:14.6 to 26:36.6 (22.0 s)
- voiceover: "And if you still feel like doing war, you keep the capacity for one hundred and twenty-two minus one nuclear apocalypses. Since one hundred warheads is the threshold for ending civilization and you have twelve thousand two hundred and forty-one, you are settling for one hundred and twenty-one civilizational collapses instead of one hundred and twenty-two. This should be more than sufficient."
- layer: B
- scene: The grid of 122 red snowflakes from nuclear-winters fills the left; on the right, a short stack of 100 grumpy warheads next to a tiny Earth, then the real stack of 12,241 that shoots out of the top of the frame. One snowflake leaves the grid; the other 121 go off.
- wishonia: PiP, thinking-small + body-counting, then sideeye-closed + body-arms-crossed on "collapses", then smirk-smile + body-open-palms on "sufficient."
- props: snowflakes (nuclear-winters' grid and counter), missile, earthGlobe (tiny), sign, stamp, stampMark, KIT.nuke
- status: outline

Moves: "war," → the 122-snowflake grid from nuclear-winters slides in, its counter on "122" (the bolted-on third wheel still there). "minus" → one snowflake lifts off the grid and hovers beside it, whistling. "warheads" → a short stack of 100 small grumpy missiles drops in on the right, next to a tiny Earth with one human on top. "threshold" → a ruled line across the top of the stack: "ENDS CIVILIZATION". "civilization" → the 100 lean at the tiny Earth: a white flash, a small mushroom cloud, and its human stands there charred and smoking, hair straight up, blinking. "twelve thousand" → behind it the real stack shoots up out of the top of the frame, a ruled "ENDS CIVILIZATION" line whizzing past every 100 warheads, while a counter rolls to "12,241"; the charred human looks up, and up. "twenty-one" → the grid counter flips from 122 to 121. "civilizational" → the 121 snowflakes go off row by row, faster and faster, each a white flash and a little mushroom cloud (nuclear-winters run backward). "collapses" → the last row and a big shake. "instead" → the clouds clear on a grid of 121 smoking scorch marks. "twenty-two." (second) → the stray snowflake looks back at the grid and gulps. "sufficient." → a stamp slams "MORE THAN SUFFICIENT" across the scorched grid; the thump knocks the stray snowflake off its spot, and after "sufficient." it drifts off the edge of the frame.

Sound: a whoosh as the grid slides in; a whistle as the snowflake lifts; a thunk as the 100 land; a boom for the tiny Earth; a sizzle; a rising slide whistle as the tall stack shoots up; a ding when the counter stops on 12,241; a clank as the grid counter flips; a pop per row as the grid goes off, speeding up, then a boom; a squeak for the gulp; a rubber-stamp thunk; a soft whoosh as the snowflake drifts off.

On screen: grid counter "122" → "121" / "ENDS CIVILIZATION" / "12,241" / "MORE THAN SUFFICIENT". Why: the 1% cut, counted in the units the war industry uses, and the 121 apocalypses humans keep, set off on screen.

## Scene 5 · treaties-you-signed

- id: treaties-you-signed
- act: The objections
- transition_in: slide left
- key: after "fewer": three signed scrolls in a row (the third one singed), the one-line 1% treaty unsigned with the pencil on its line, the charred leader and the weeping weapons maker
- cue: "But humans would never"
- time: 26:36.6 to 27:03.8 (27.2 s)
- voiceover: ""But humans would never agree to a treaty!" you say. You already have. Multiple times. You banned chemical weapons (nineteen ninety-three, one hundred and ninety-three countries). You banned biological weapons (nineteen seventy-five, one hundred and eighty-seven countries). You banned landmines (nineteen ninety-seven, one hundred and sixty-four countries). You've signed treaties banning weapons you actually like using. This one just asks you to buy one percent fewer of them."
- layer: B
- scene: A long signing table. A leader who says humans would never sign a treaty slams three treaty scrolls down, one by one, each on the weapon it bans; the third weapon is a landmine. The one-line 1% treaty slides in last, unsigned.
- wishonia: PiP, skeptical-closed + body-arms-crossed, then surprised-oh + body-idle on "landmines", then smirk-smile + body-point-right on "like"
- props: politician (one of the ring), scroll (four), germ, gas canister and landmine (drawn in the scene), weaponsMaker, missile (his baby), priceTag, KIT.pencil, KIT.nuke
- status: outline

Moves: "never" → a leader at a long table folds his arms and shakes his head, grinning. "already" → three rolled scrolls sit at his elbow; he looks down at them. "chemical weapons" → he unrolls scroll 1 and slams it flat on a grumpy little gas canister tiptoeing across the table; the canister is squashed and lets out a green puff, and he coughs. "biological weapons" → scroll 2 slams down on a germ scuttling the other way: splat. "landmines" → scroll 3 slams down on a landmine: a white flash, a boom, a small mushroom cloud; the leader stands there charred black and smoking, hair straight up, still grinning, only his eyes blinking; scroll 3 is singed at the edges but still legible. "like" → the weapons maker rises behind the table, cradling his grinning baby missile, a price tag on its fin. "using." → he sniffles into a hanky. "one percent fewer" → the fourth scroll, the one-line 1% treaty from every-leader-at-once, slides in at the end of the row, mostly empty paper; a pencil rolls onto its signature line. after "them." → the charred leader looks at the pencil and blinks; the weapons maker hugs the baby tighter.

Sound: a pop as the rolled scrolls appear; a slam for each scroll; a huff for the gas puff; a splat for the germ; a boom for the landmine; a sizzle; a slide whistle as the weapons maker rises; a sniffle squeak; a whoosh as scroll 4 slides in; a tick as the pencil stops on the line.

On screen: scroll titles "CHEMICAL WEAPONS BAN", "BIOLOGICAL WEAPONS BAN", "LANDMINE BAN", each crowded with tiny signatures; "THE 1% TREATY" with one line and an empty signature line. No: no real treaty documents or seals; no years or counts on screen (the captions have them). Why: humans already sign treaties against weapons they like, and the one they have not signed asks for the least.

## Scene 6 · 847-civilizations

- id: 847-civilizations
- act: Wishonia has done this before
- transition_in: zoom out of the wall screen (the wall screen starts on treaties-you-signed's last frame)
- key: after "didn't" (second): the drawer running out of frame, teal folders and burnt ones side by side, the burnt folder open on its two skeletons, Earth's file smoking on the desk
- cue: "I've done this before."
- time: 27:03.8 to 27:27.1 (23.3 s)
- voiceover: "I've done this before. I've sent versions of this manual to eight hundred and forty-seven civilizations on eight hundred and forty-seven planets. Some listened. Some didn't. I kept the data. The ones that redirected resources from killing each other to keeping each other alive stopped doing war and disease. The ones that didn't extincted themselves."
- layer: A
- scene: earth-means-dirt's office with the filing cabinet. A drawer rolls out of the cabinet, across the floor and off the edge of the frame, packed with 847 planet folders; those that listened glow teal, those that did not are burnt at the edges. Earth's case file lies on the desk, undecided.
- wishonia: big, neutral-smile + body-presenting, then happy-smile + body-open-palms on "redirected", then sad-small + body-palms-down on "extincted"
- props: office, wallScreen, cabinet, desk, mug, case-file, clipboard, colorFlipFunnel (tiny), money("war"), money("med"), KIT.nuke, skeletons
- status: outline

Moves: "I've" → the zoom out of the wall screen lands on the office; the wall screen still shows the signing table. "before." → Wishonia presents the filing cabinet, and its bottom drawer clunks open an inch. "eight hundred and forty-seven" (first) → the drawer rolls out across the floor, in front of the desk and off the edge of the frame, and keeps rolling; a counter on its front spins to "847". "planets." → a tiny planet pops up on every folder tab, each a different color and ring. "listened." → some folders light up teal. "didn't." → the rest blacken and curl at the edges, smoking; on the desk, the corner of Earth's case file starts to smoke too, and stops there. "data." → a clipboard flips up inside the drawer front: "THE DATA", two tally columns, every mark filled in. "redirected" → one teal folder springs open: on its tiny planet, war papers march into a tiny funnel and come out medicine papers, and its little aliens wave. "resources" → its seals flip. "didn't" (second) → a burnt folder creaks open: on its charred little planet two aliens still point glowing atoms at each other, as in split-the-atom, both grinning skeletons now, a mushroom cloud still rising between them. "extincted" → the burnt folder crumbles to ash. "themselves." → HOLD: nothing moves, and no sound, until "The" in next-page.

Sound: a soft whoosh for the zoom; a thunk as the drawer pops; a whirr as it rolls and rolls; ticks for the counter; a pop for the tiny planets; a sparkle for the teal; a sizzle for the burnt; a click for the clipboard; a boing as the teal folder springs open; a ding for its seals; a creak (squeak) for the burnt one; then silence.

On screen: the drawer counter "847" / folder tabs "REDIRECTED" and "DIDN'T" / Earth's tab "~~EARTH~~ DIRT: CASE #847" / clipboard "THE DATA". Why: Wishonia's track record, the one variable that decided it, and Earth's folder still undecided.

## Scene 7 · next-page

- id: next-page
- act: Wishonia has done this before
- transition_in: zoom into the wall screen (earth-means-dirt's screen box in 16:9, as pentagon does)
- key: after "page.": the row of shut books, page 2 peeking out of each, the cuckoo's head stuck out of the first one, YOU at the end of the row turning to page 2
- cue: "The only variable was"
- time: 27:27.1 to 27:33.8 (6.7 s)
- voiceover: "The only variable was the percentage of the population that decided it sounded crazy without reading the next page."
- layer: B
- scene: A row of everyday humans, each reading the manual open on page 1, "THIS IS GOING TO SOUND CRAZY"; the first one frowns and snaps his book shut, page 2 unread, and the rest follow, all but YOU.
- wishonia: PiP, sideeye-closed + body-arms-crossed
- props: manual, gauge, everyday humans, YOU, cuckoo
- status: outline

Moves: "The" → the row of readers, every body type from its outfit, YOU at the far end. "percentage" → a gauge over the row: "STOPPED AT PAGE 1"; its needle swings up near the top. "crazy" → the cuckoo pops out of the first reader's page 1 on its spring; he frowns at it. "page." → he snaps the book shut on it; the cuckoo's head sticks out of the pages, squawking, and the tab "PAGE 2" peeks out, unread. after "page." → down the row, every book snaps shut in a ripple, until YOU, who holds his open and turns to page 2; the gauge needle drops one mark.

Sound: a rising slide whistle as the needle swings; a boing for the cuckoo; a slam for the first snap and a squeak from the cuckoo; a thunk per book in the ripple; a soft whoosh as YOU turns the page.

On screen: page 1 "THIS IS GOING TO SOUND CRAZY" / gauge "STOPPED AT PAGE 1" / tab "PAGE 2". Why: the habit that decided 847 outcomes, in one human, and the viewer's way out.

## Scene 8 · bread-mold

- id: bread-mold
- act: Wishonia has done this before
- transition_in: slide left
- key: on "years": the calendar pages streaming off, the sick cavemen already skeletons, the two flickers still flicking
- cue: "That is the same reflex"
- time: 27:33.8 to 27:43.2 (9.4 s)
- voiceover: "That is the same reflex that kept you from inventing antibiotics for two hundred thousand years while bread mold sat right there on your bread."
- layer: B
- scene: The cave from fire-on-fire. Its two cavemen flick the mold (medicine teal, never money green) off slice after slice of bread for 200,000 years; the mold wears a glowing tag; behind them, sick cavemen with red chest lights x-ray into skeletons, and then the two flickers do too, still flicking.
- wishonia: PiP, eyeroll-closed + body-hands-hips
- props: fire-on-fire's cave and cavemen, bread (drawn in the scene), sign (the glowing tag), calendar, KIT.xray
- status: outline

Moves: "reflex" → caveman A flicks the teal mold off a slice with one finger and takes a bite. "antibiotics" → the flicked-off mold on the cave floor gets a glowing tag: "ANTIBIOTICS". "two hundred thousand years" → a calendar's pages tear off and stream away (the 1950s movie montage), its band reading "YEAR", toward 200,000; A and B keep flicking mold off slice after slice; behind them a line of sick cavemen with red chest lights coughs and x-rays into grinning skeletons, one after another, and then A and B x-ray too, still flicking. "mold" → push in on the pile of flicked-off mold, glowing under its tag. "bread." (second) → skeleton A tosses its last slice over its shoulder, and after "bread." it lands on a heap of moldy slices that fills the back of the cave.

Sound: a click per flick; a ding as the tag lights; a whirr as the calendar pages stream; a zap per x-ray; a sparkle on the glowing mold; a whoosh for the toss; a splat as the slice lands.

On screen: the tag "ANTIBIOTICS" / the calendar "YEAR" → "200,000". Why: what the not-reading reflex has cost before, in a picture a child gets.

## Scene 9 · human-greed

- id: human-greed
- act: Two advantages
- transition_in: zoom out of the wall screen (the wall screen starts on bread-mold's last frame)
- key: on "greed.": the plug in, the office lights flared to full, the fat cat on fire in his wheel and still running
- cue: "And you have two"
- time: 27:43.2 to 27:54.0 (10.8 s)
- voiceover: "And you have two other advantages, the internet and a new financial instrument designed specifically for harnessing the most powerful force in the universe: human greed."
- layer: A
- scene: Wishonia counts two advantages on the wall screen (a knot of cables, then a fancy bond certificate); then the screen shows a power plant labeled "HUMAN GREED", where the fat cat runs in a giant hamster wheel after a paper on a stick; Wishonia's fist lands on a plug and the office lights flare to full.
- wishonia: big, neutral-smile + body-counting, then smirk-smile + body-idle with the mug at her lips on "powerful", then excited-open + body-fist on "greed."
- props: office, wallScreen, desk, mug, bond, richHuman, money("plain"), the power plant and its hamster wheel (drawn in the scene), KIT.fireOn
- status: outline

Moves: "And" → the zoom out lands on the office; the wall screen still shows the cave and its heap of moldy bread. "two" → Wishonia holds up two fingers. "internet" → the wall screen: a knot of cables, buzzing, "1. THE INTERNET". "financial instrument" → a fancy bond certificate slides onto the wall screen, "2. A NEW FINANCIAL INSTRUMENT", and glints. "powerful" → Wishonia sips her coffee. "universe:" → the wall screen pulls back to a power plant with a glowing sign, "POWER SOURCE: HUMAN GREED"; inside, the fat cat (dollar-sign eyes) runs in a giant hamster wheel after a plain paper dangling from a stick, and the wheel hums. after "universe:" → a fat cable drops out of the bottom of the wall screen to the desk (not on "human": the alignment squeezes "human" to zero length, on top of "greed."). "greed." → Wishonia's fist slams its plug into a socket on the desk: the sunburst and the office lights flare to full; on the wall screen the wheel spins so fast the fat cat catches fire and keeps running, grinning, dollar signs and all. after "greed." → she puts the mug down slowly.

Sound: a soft whoosh for the zoom; a zap for the buzzing cables; a whoosh and a sparkle for the certificate; a hum for the power plant and a whirr for the wheel; a whoosh as the cable drops; a slam for the plug; a fire whoosh as the fat cat catches; a thunk as the mug goes down.

On screen: "1. THE INTERNET" / "2. A NEW FINANCIAL INSTRUMENT" / "POWER SOURCE: HUMAN GREED". Why: the plan runs on the force humans have the most of, and the certificate sets up Step 1.
