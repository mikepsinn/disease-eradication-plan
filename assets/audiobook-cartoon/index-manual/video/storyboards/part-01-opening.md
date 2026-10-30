---
format: 1920x1080
duration: 4:18.5
message: "Earth may be eligible for optimization: its species only does things for paper, and it spends 604 papers on weapons for every 1 on testing which medicines work."
arc: Theme song music video → title card → eligibility check → meet the optimizer → what Wishonia noticed (the atom, dirt, the Pentagon, paper) → the 604 bar
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 1, "Opening"
audio: index-manual.cbaf659d.mp3, 00:00.0 to 04:18.5
version: v2
---

# Part 1 storyboard: "Opening"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The papers. They are introduced in papers-with-presidents, they decide everything in without-with-papers, and they stack into the 604 bar at the end. The 604 bar comes back every time the narrator says 604.

**Callback set up here.** In eligible, Wishonia stamps the Earth case file "MAY BE ELIGIBLE FOR OPTIMIZATION". The ending pays it off with "ELIGIBLE FOR OPTIMIZATION" (style bible, gag 5).

**Held frame.** loved-ones, after "diseases?". Nothing moves until "nuclear" in the next scene.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.

## Changes from v1

- "Use the existing theme song music video for the first 1:40 (cold-open and theme-titles), and switch to the drawn style at the title card." cold-open and theme-titles are now one scene, theme-music-video.

## Decided

1. **Music video.** The first 1:40 is the existing theme song music video, `assets/music-video/wishonia-theme-song-music-video.mp4`. The drawn style starts at the title card. The video sings Wishonia's full name, so no acronym card is needed.

**Transitions.** One rule for the whole part: Layer B is the footage on Wishonia's wall screen. Going from the office to Earth zooms into the wall screen; coming back zooms out of it. Earth to Earth slides left. Office to office cuts.

## Scene 1 · theme-music-video

- id: theme-music-video
- act: Theme song and title
- transition_in: the video starts
- key: the video's 15 keyframes, in order
- time: 00:00.0 to 01:40.3 (100.3 s)
- cue: the start of the MP3 (the theme song)
- layer: the existing music video, not drawn
- scene: The theme song music video: 15 clips, one per lyric line, animated from Gemini keyframes with Veo (`assets/music-video/keyframes/`, `clips/` and `music-video-manifest.json`).
- voiceover: "You're here. Your organs are failing. And your death is drawing near. But if you bribe the right politicians in the right order at the right time, you can trade the nuclear warheads for medicine. And it's not even a crime."
- props: music-video
- status: built

Moves: the video plays as made, one clip per lyric line, from the smiling planet to the curtain call.

Build: play the video muted under the episode MP3. Its sound is the same theme song (loudness correlation 1.000 at 0 ms). It is 1280 × 720 at 34 fps, so scale it to 1920 × 1080 and 30 fps. Its picture ends at 1:39.6, 0.7 s before "How", so hold its last frame until the title card. It has no lyrics on screen; the captions show the cold open's spoken lines only.

Style bible exceptions, accepted for this one video: the images are AI-made, and Wishonia is off-model in the closing curtain call (pale skin, blue dress). Any one clip can be swapped later without touching the rest. Why: the song and its video already exist, and the drawn cartoon starts where the narration does.

## Scene 2 · title-card

- id: title-card
- act: Theme song and title
- transition_in: cut on the music's last note
- key: both title lines in
- time: 01:40.3 to 01:48.8 (8.5 s)
- cue: "How"
- layer: A, title card
- scene: The book cover look fills the screen with the title.
- voiceover: "How to End War and Disease (for Busy People) A Step-by-Step Guide to Optimizing Your Terrible Civilization"
- props: title-card, office
- status: built

Moves: "How" → the title words slam in, one per spoken word. "Busy" → a tiny human sprints across the bottom of the card, checking a wristwatch. "Step-by-Step" → his skeleton, in the same bowler, strolls back the other way, still checking the watch. after "Civilization" → the half-sun on the horizon sinks a little lower, as if embarrassed.

Sound: a thunk on each title word; a quick slide whistle under the sprinting human.

On screen: "HOW TO END WAR AND DISEASE (for Busy People)" / "A Step-by-Step Guide to Optimizing Your Terrible Civilization". No: no cover photo, all drawn. Why: the narrator reads the title, so this is the one title card in the part.

## Scene 3 · loved-ones

- id: loved-ones
- act: Eligibility check
- transition_in: slide left
- key: YES ticked, the HOLD
- time: 01:48.8 to 01:57.6 (8.7 s)
- cue: "Is"
- layer: B
- scene: A 1950s mail-in form, "PLANET ELIGIBILITY CHECK", next to a framed family portrait of humans on a mantel.
- voiceover: "Is everyone you've ever loved currently being slowly tortured and or brutally murdered by horrible diseases?"
- wishonia: PiP, sad-closed
- props: eligibility-form, checkbox-tick, pencil, human
- status: built

Moves: "Is" → the form slides in and question 1 types on. "loved" → the family portrait; everyone in it is smiling. "tortured" → the chest lights in the portrait blink red, one by one, while the smiles stay. "brutally" → the Grim Reaper rises up behind the family, grinning between the last two heads. "murdered" → the family x-rays into skeletons, one by one; the skulls keep smiling. "diseases?" → the pencil ticks YES. Then HOLD. The joke is the form itself: its fine print at the bottom reads "Please allow 4 to 6 weeks for optimization."

Sound: typewriter clacks as the question types; a whoosh as the Reaper rises; an x-ray zap on "murdered"; a pencil scratch on the tick; then silence for the HOLD.

On screen: "PLANET ELIGIBILITY CHECK" / "1. Everyone you've ever loved: being slowly tortured and/or murdered by horrible diseases?" / "☐ YES ☐ NO". Why: the cheerful form against the worst question, with the horror on screen; the reason the viewer should care.

## Scene 4 · nuclear-winters

- id: nuclear-winters
- act: Eligibility check
- transition_in: same form (no seam)
- key: all 122 snowflakes in, the human frozen in his ice block
- time: 01:57.6 to 02:08.3 (10.8 s)
- cue: "Do"
- layer: B
- scene: Question 2 on the same form. One small Earth on the left; on the right, a grid of 122 red snowflakes.
- voiceover: "Do your governments waste money on enough nuclear bombs to cause one hundred and twenty-two nuclear winters despite only having the one civilization to apocalypse?"
- wishonia: PiP, thinking-closed
- props: eligibility-form, checkbox-tick, earth-globe, snowflakes
- status: built

Moves: "Do" → the first frame is loved-ones' last: the skeleton family and the Grim Reaper in the portrait, YES ticked. "nuclear" (first) → the portrait leaves, the form moves over and question 2 types on; the HOLD ends here. "bombs" → a stockpile of 122 grumpy little warheads with faces (the theme song's rocket) pops up out of the floor. "cause" → the one small Earth appears with its one human, and all 122 warheads lean at it. "one hundred and twenty-two" → row by row, faster and faster, each warhead blinks into a red snowflake in a puff; the counter runs out of digit wheels and a third wheel is bolted on. "winters" → red snow starts falling on the Earth. "despite" → the human looks up at it. "only" → he quietly puts on a scarf. "having" → a snowdrift grows on the Earth and buries him. "one civilization" → the Earth's counter reads 1. "civilization" → buried to the chin, his teeth chatter. "apocalypse?" → he freezes solid in a block of ice, scarf and all. Then the pencil comes to YES; it ticks it on Wishonia's wall screen as eligible opens (the scratch sound falls just after this scene ends).

Sound: typewriter clacks as question 2 types; a boing as the warheads pop up; a pop per row as they turn into snowflakes, speeding up; a clank as the extra wheel goes on; a whoosh of wind as the snow starts; chattering teeth from "civilization"; an ice "ding" as he freezes; a pencil scratch on YES.

On screen: "2. Enough nuclear bombs for 122 nuclear winters?" / "Nuclear winters: 122" / "Civilizations: 1". Why: the waste, as one number against one planet.

## Scene 5 · eligible

- id: eligible
- act: Eligibility check
- transition_in: zoom out of the wall screen
- key: the stamp just lifted off the case file
- time: 02:08.3 to 02:13.6 (5.3 s)
- cue: "If"
- layer: A
- scene: Wishonia at the desk stamps the Earth case file.
- voiceover: "If so, your planet may be eligible for optimization."
- wishonia: happy-smile + body-presenting, then happy-smile + body-palms-down on "eligible"
- props: office, wall-screen, eligibility-form, desk, mug, case-file, stamp
- status: built

Moves: "If" → Wishonia lifts the rubber stamp. before "eligible" → Wishonia huffs on it. "eligible" → stamp on the "EARTH: CASE #847" file: "MAY BE ELIGIBLE FOR OPTIMIZATION". after "optimization." → Wishonia blows on the wet ink and slides the file into an out-tray marked "PLANETS", on top of a stack of other planets' files: "VENUS: TOO HOT", "MARS: NOBODY HOME".

Sound: a huff; a rubber-stamp thunk; a paper slide into the tray.

No: no paperwork joke on top; the stamp is the joke. Why: the pitch, and the setup for the ending's stamp.

## Scene 6 · meet-wishonia

- id: meet-wishonia
- act: Meet Wishonia
- transition_in: cut
- key: after "years." (second): the wreck's singed card reads the same number
- time: 02:13.6 to 02:29.3 (15.7 s)
- cue: "I'm"
- layer: A
- scene: Wishonia introduces herself; a nameplate slides onto the desk; the wall screen shows the years.
- voiceover: "I'm Wishonia Love. C.E.O. and President of Universe Optimization Services. I've been upgrading civilizations for four thousand, two hundred and ninety-seven years, which in your Earth time is four thousand, two hundred and ninety-seven years."
- wishonia: happy-smile + body-hand-chest, then smirk-smile + body-open-palms on "Earth"
- props: office, wall-screen, desk, mug, nameplate, converter-dial
- status: built

Moves: "Wishonia" → the nameplate slides onto the desk. "President" → the title line appears under the name. "Universe Optimization Services" → the nameplate keeps extending off the edge of the desk to fit it all. "four thousand" (first) → "4,297 years" on the wall screen. "which" → a 1950s unit converter rises into the screen. "Earth time" → it cranks into action: dials spin, gears whirr, it shakes harder and harder, glows red and puffs steam. 1.1 s after "Earth" → it blows up: a white flash, the office shakes, a little mushroom cloud. The cloud clears on a charred, bent, smoking wreck (dented, chimney bent, a gear sprung out on its spring, the crank hanging limp); two white eyes open in the soot and blink. after "years." (second) → the wreck's bell still dings and it spits out its singed card: "IN EARTH TIME: 4,297 years". Wishonia looks at the camera; nothing moves.

Sound: the nameplate sliding (twice, longer the second time); whirring gears; a boom where the clank was; a bell ding; then silence for the look.

On screen: "WISHONIA LOVE" / "CEO and President, Universe Optimization Services" / "Upgrading civilizations: 4,297 years" / "In Earth time: 4,297 years". No: no spaceship or other planet; Wishonia stays in the office. Why: who is talking, and the first dry joke in Wishonia's voice.

## Scene 7 · split-the-atom

- id: split-the-atom
- act: What Wishonia noticed
- transition_in: zoom into the wall screen
- key: on "That's": the charred pair still aiming, smoke curling up
- time: 02:29.3 to 02:54.6 (25.2 s)
- cue: "I" ("I started watching")
- layer: B
- scene: A dictionary card for "atom" gets cut in half; then two humans each hold a glowing atom and turn to point them at each other.
- voiceover: "I started watching your planet in nineteen forty-five when you split the atom. "Atom" comes from your Greek word meaning "unable to be cut," so naturally, you cut it. This was very human of you. I assumed you were trying to unlock unlimited free energy. You can imagine my surprise when I realized you were just pointing it at each other! That's kind of like"
- wishonia: PiP, neutral-smile, then surprised-oh on "surprise"
- props: atom, dictionary-card, scissors, light-bulb, human, mushroom-cloud
- status: built

Moves: "nineteen forty-five" → "1945" stamps on. "Greek" → the dictionary card: "ATOM (Greek): unable to be cut". after "cut it." → a beat, then scissors snip the card in half. "very human of you" → a human pops up behind the two halves, proudly holding the scissors. "free energy" → a glowing atom lights a row of bulbs, and the human happily plugs in a toaster. "surprise" → Wishonia's surprised face in the corner frame. "pointing" → the bulbs go dark and two humans turn their atoms toward each other. "each" → they fire: the two atoms streak to the middle. "other!" → a white flash, the screen shakes, and a mushroom cloud rises between them; soot hides both humans. "That's" → the soot and the cloud thin away: both are standing exactly where they were, still aiming, charred black and smoking, hair straight up; only their white eyes blink. "kind" → the charred toaster pops up two slices of black toast. "like" → both blink.

Sound: a scissors snip; light-switch clicks as the bulbs light; a low hum as the atoms turn; a zap as they fire; a boom on the flash; a sizzle as the smoke clears; a toaster pop.

On screen: "1945" / "ATOM (Greek): unable to be cut". Why: first evidence that humans point every new power at each other.

## Scene 8 · fire-on-fire

- id: fire-on-fire
- act: What Wishonia noticed
- transition_in: slide left
- key: on "yourself": both cavemen on fire all over
- time: 02:54.6 to 03:00.4 (5.8 s)
- cue: "discovering"
- layer: B
- scene: A cave; a human discovers a campfire, smiles, and then the human's sleeve catches a small flame.
- voiceover: "discovering fire and then immediately using it to set yourself on fire."
- wishonia: PiP, eyeroll-closed
- props: cave, campfire, burning-stick, human
- status: built

Moves: "discovering" → two cavemen stand on either side of an unlit campfire. "fire" (first) → the campfire lights; both smile at it and warm a hand. "using" → each reaches into the fire and comes out with a burning stick; the sticks cross over the fire. "set" → they wind up, frowning at each other. "yourself" → they jab each other, one at the head and one at the belly, and both go up in flames all over: arms up, yelping, hopping and running back and forth. "fire." (last) → the flames go out in a puff of soot; it clears on two charred cavemen, hair straight up, smoking, blinking. Then they look at each other, look down at the fire, and each reaches in for a new stick. As earth-means-dirt zooms out, they pull two new burning sticks out of the fire on the wall screen.

Sound: a whoosh as the campfire lights; a second whoosh and two yelps as they catch; a sizzle as the flames go out; a small whoosh on the wall screen as the new sticks light (it plays at the start of earth-means-dirt).

Why: the same point as split-the-atom, in a picture a child gets.

## Scene 9 · earth-means-dirt

- id: earth-means-dirt
- act: What Wishonia noticed
- transition_in: zoom out of the wall screen
- key: on "want": DIRT written in, the shrug
- time: 03:00.4 to 03:11.4 (11.0 s)
- cue: "The" ("The second thing")
- layer: A
- wishonia: skeptical-closed + body-idle, then skeptical-closed + body-shrug on "want"
- scene: Wishonia crosses out "EARTH" on the case-file label and writes "DIRT".
- voiceover: "The second thing I noticed is that your planet is named "Earth," which means dirt. You named your planet.. dirt. Okay, if that's what you want..."
- props: office, cabinet, case-file, desk, mug
- status: built

Moves: "dirt." (first) → Wishonia crosses out "EARTH" on the case-file label. "dirt." (second) → writes "DIRT". "Okay," → the pen hovers. "want..." → shrug. after "want..." → Wishonia pulls the file out of the cabinet's "E" drawer and drops it into the "D" drawer.

Sound: a marker squeak on each word; a drawer slam.

On screen: the case-file label "~~EARTH~~ DIRT: CASE #847". No: no globe made of mud. Why: a breather joke between two pieces of evidence.

## Scene 10 · pentagon

- id: pentagon
- act: What Wishonia noticed
- transition_in: zoom into the wall screen
- key: all three buildings and signs in
- time: 03:11.4 to 03:22.8 (11.4 s)
- cue: "I" ("I also noticed")
- layer: B
- scene: An honest sign "WAR BUILDING" gets painted over with "THE PENTAGON" on a plain five-sided building with a missile hiding in its courtyard; beside it, a rectangle hospital and a square school with signs.
- voiceover: "I also noticed that you call your war building "The Pentagon" because it has five sides (this is like naming a hospital "Rectangle" or calling a school "Square")."
- wishonia: PiP, smirk-smile
- props: pentagon, hospital, school, sign
- status: built

Moves: "war" → an honest sign "WAR BUILDING" springs up out of the bare ground where the building will stand. "Pentagon" → the five-sided building draws on around the sign's pole, and a paint roller slaps onto the sign and rolls "THE PENTAGON" over it; the fresh paint drips. "five sides" → the sides count off, 1 to 5. after "sides" → a grumpy missile pokes up out of the courtyard, looks left, looks right, looks at us, scowls, and ducks back down on "a" ("naming a hospital"), leaving a puff of smoke. "Rectangle" → the rectangle hospital drops in with its sign. "Square" → the square school drops in with its sign. after "Square" → a fourth building drops in that nobody mentioned: a triangle doghouse with the sign "TRIANGLE". The democracy dog pokes its head out (its first appearance; it returns in Part 6).

Sound: a pop as the honest sign springs up; a pen scratch as the Pentagon draws; a splat as the roller hits the sign; a tick per side; a slide whistle down as the missile ducks; a thud per building; a small woof.

Why: names that describe the shape and hide the purpose.

## Scene 11 · papers-with-presidents

- id: papers-with-presidents
- act: The papers
- transition_in: slide left
- key: on "money": every head has turned to follow the paper
- time: 03:22.8 to 03:40.6 (17.8 s)
- cue: "However,"
- layer: B
- scene: A crowd of humans stands still, bored. One paper walks in on stick legs; every human turns and follows it.
- voiceover: "However, the most fascinating discovery about your species is that you only do things when given small pieces of paper with presidents on them. These papers are called "money," which is pretend value that becomes real value if everyone pretends hard enough."
- wishonia: PiP, thinking-small
- props: plain-paper, human, banner
- status: built

Moves: "only" → the crowd stands still, bored. "paper" → one paper walks in on stick legs. "presidents" → close-up of its oval portrait (a generic old man in a wig), who winks on "them.". "money," → every head snaps toward it but one: a bored human at the far left keeps staring at the floor. after "money," → the crowd follows the paper off in a conga line and leaves him standing alone; he lifts his head and looks after them, too late. "value" (the first) → the line comes back around the planet from the left, behind him; the paper flattens him like a pancake, only his blinking eyes showing, and the whole line walks over him. "everyone" → he peels himself off the floor, springs back up a little shorter, limps after the line with stars circling his head, and joins the back of it. "pretends" → the line squeezes its eyes shut and trembles, and the paper starts to glow. "hard" → the front human pretends so hard her head pops off and spins up; the paper glows brighter. "enough." → the paper sparkles. after "enough." → the head lands back on her neck upside down, eyes still squeezed shut.

Sound: tiny squeaky footsteps for the paper; a whoosh as the heads turn; a splat when the paper flattens the slow human; a boing as he springs back up; a pop as the head comes off; a sparkle on "enough."; a thunk as the head lands.

On screen: "MONEY: pretend value that becomes real value if everyone pretends hard enough". No: no real banknote. Why: introduces the main actor of Layer B.

## Scene 12 · without-with-papers

- id: without-with-papers
- act: The papers
- transition_in: slide left
- key: every line marked, papers on the right side
- time: 03:40.6 to 04:08.6 (28.0 s)
- cue: "Without"
- layer: B, split screen
- scene: Left, "WITHOUT PAPERS": humans sit next to a hospital, a lab and a field of free-growing food and do nothing. Right, "WITH PAPERS": red papers rush in and the humans build bombs, draw war arrows on a map and dig up the planet.
- voiceover: "Without these papers, you won't: Save lives (requires many papers). Cure diseases (requires very many papers). Feed hungry people (requires papers, even though food grows for free). But WITH these papers, you will: Build bombs (you love giving papers for this). Start wars (somehow this makes more papers). Destroy the planet (surprisingly profitable in papers)."
- wishonia: PiP, neutral-smile, then eyeroll-smile on "profitable"
- props: papers-red, hospital, lab, wheat-field, bomb, map, human, checkbox-tick
- status: built

Moves: Each line appears on its first word and gets its mark on its last word. "Save lives" → the patient by the hospital sits with a thermometer in its mouth, its check-engine light blinking red; "many papers" → the sign flips to CLOSED; after "papers)." → the patient x-rays into a skeleton and stays sitting there, grinning, thermometer in its teeth. "very many papers" → a cobweb grows between the scientist and the flask and a spider lowers itself; after "papers)." → the scientist x-rays into a skeleton, still in its lab coat, still holding the clipboard. "free" → a wheat stalk grows by itself; after "free)." → the hungry human looks at the wheat, then into an empty wallet (a moth flies out), then x-rays into a skeleton still holding up the empty wallet. "WITH" → red papers rush in from the right, and the humans there jump into frantic work. "giving papers" → two papers hop into the bomb, which swells; after "this)." → it blows up in the builder's face: a blast, a small mushroom cloud, a shake; the builder stands there charred black and smoking, hard hat on, grinning, and keeps hammering; a new bomb pops onto the bench. "Start wars" → war arrows draw on the map; after "wars" → each arrowhead turns into a tiny mushroom cloud; "more papers" → a paper flies out of each cloud. "Destroy" → the digger sweats and a crater opens in the hill; after "planet" → the dirt cracks and falls off both sides: the hill is the Earth, with a big bite out of its top, molten inside, and the clods are now sea and land. "profitable" → papers sprout from the bite like wheat. After "papers)." (last) → the sweating digger stops and looks over at the left: three grinning skeletons next to wheat taller than the hospital.

Sound: Crickets on the left; a zap on the first two x-rays; frantic hammering on "WITH"; a boom when the bomb goes off; a pop for the tiny clouds; cash-register dings for the papers from the clouds and for the paper sprouts.

On screen: "Save lives ✗ · Cure diseases ✗ · Feed hungry people ✗" / "Build bombs ✓ · Start wars ✓ · Destroy the planet ✓". Why: the rule the whole plan uses; papers decide what humans do.

## Scene 13 · 604-papers

- id: 604-papers
- act: The papers
- transition_in: slide left
- key: after "work": the camera is back down and the labels are in
- time: 04:08.6 to 04:18.5 (9.9 s)
- cue: "In" ("In fact,")
- layer: B
- scene: The 604 bar: a tall red stack of papers next to one small teal paper.
- voiceover: "In fact, your governments spend six hundred and four papers on weapons for every one paper on testing which medicines work."
- wishonia: PiP, sideeye-closed
- props: 604-bar, papers-red, papers-teal
- status: built

Moves: "six hundred and four" → the red stack rises and the camera tilts up with it, past the top of the frame, until a small airplane has to swerve around it. "one paper" → the camera falls all the way back down to the one teal paper, which waves. After "work." → "604 : 1" with the labels; the teal paper leans back and looks up at the stack; one red paper slides off the top, drifts down rocking like a leaf, then drops like an anvil and flattens the teal paper. The red paper stands on it, and the teal paper's little arm pokes out from under and waves weakly. The part ends on that frame.

Sound: A rising slide whistle as the stack climbs; an airplane whoosh; a falling slide whistle; a splat when the red paper lands; a tiny squeak from under it.

On screen: "604 : 1" / "Weapons" / "Testing which medicines work". No: no extra numbers. Why: the spine's payoff, and the number the rest of the episode fixes.
