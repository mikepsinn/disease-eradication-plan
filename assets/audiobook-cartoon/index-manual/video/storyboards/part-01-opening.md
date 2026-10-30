---
format: 1920x1080
duration: 4:18.5
message: "Earth may be eligible for optimization: its species only does things for paper, and it spends 604 papers on weapons for every 1 on testing which medicines work."
arc: Theme song music video → title card → the eligibility check (a family portrait, one small planet under 122 nuclear winters) → Wishonia at her lectern: the stamp, her name, 4,297 years → what she noticed (the atom, fire, dirt, the Pentagon) → the papers → the 604 bar
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 1, "Opening"
audio: index-manual.cbaf659d.mp3, 00:00.0 to 04:18.5
version: v3
---

# Part 1 storyboard: "Opening"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the sofa smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Part 1 is now the 1950s atomic-age film of Part 2 (`compositions/scenes/part-02/` is the reference for every kind of shot). Layer A is Wishonia at her lectern in the studio (`KIT.studio`); Layer B is the illustrated plates the camera travels over (`KIT.camera`), where Wishonia is the voice and is not on screen. The money is green, and its seal says what it buys (a missile for war, a cross for medicine). The theme song music video stays as made.

**Spine.** The papers. One plain paper walks into papers-with-presidents and the whole crowd follows it; in without-with-papers the left of the street has none and nothing gets done, and war-seal papers flood the right; at the end they stack into the 604 bar. The 604 bar comes back every time the narrator says 604.

**Callbacks.** This is the first part, so the callbacks are inside it: the case file stamped in eligible is the one corrected in earth-means-dirt; the 4,297 YEARS card in meet-wishonia comes back as the wrecked converter's singed card; the two halves of the atom go to the two neighbors who blow each other up with them; the toaster that free energy lights in split-the-atom pops black toast in pointing-at-each-other.

**Set up here.** For later parts, draw these so they can come back:
- The case file "EARTH: CASE #847" with "MAY BE ELIGIBLE FOR OPTIMIZATION" across its cover and "~~EARTH~~ DIRT" on its tab (Parts 4 and 12, and the final stamp in Parts 26 and 27, style bible gag 4); Wishonia's huff on the stamp (Part 26); the PLANETS out-tray with VENUS and MARS (Part 27).
- The family portrait: the living-room sitting (on YOU's mantel in Part 12) and the print the flash develops, the family as smiling skeletons with the Grim Reaper grinning between the heads (on the Weapons Maker's wall in Part 6). The Reaper himself comes back in Parts 5, 6 and 8.
- The 122 red snowflakes (Parts 10 and 13); 4,297 years and the converter's bell, which dings once offstage in Part 3's host-opens.
- The five-sided building with the grumpy missile in its courtyard and the honest WAR BUILDING sign under the paint (Part 7); the Democracy Dog in the triangle doghouse (Part 6).
- The neighbors who point the atom halves at each other and the cave of fire-on-fire (Part 13); the giant shears (Part 15); the toaster on the fence post (Part 25).
- The flattened human from papers-with-presidents (Parts 12 and 20); the moth from the empty wallet (Part 2 on); the wheat that grows by itself (Part 2); the cobweb and the spider (Part 9).
- The 604 bar, with the medicine paper flattened under the war paper and its little arm waving weakly (Parts 6, 7, 10 and 25).
- The busy human in the bowler and his skeleton in the same bowler, `{ tone: 2, outfit: "suit", hat: "bowler" }`: YOU, the viewer, from Part 10 on.

**Held frame.** loved-ones, from the flash after "diseases?": the developed print holds, with no motion and no sound, until nuclear-winters cuts in on "waste".

**Transitions.** The title card cuts in on the music's last note. Plates and host shots cut to each other. eligible irises in on Wishonia's face, the first time the film shows her (style bible gag 6); meet-wishonia is the same shot with no seam. pointing-at-each-other cuts back to the plate where the camera would have got to during the reaction cut. The part ends on the 604 plate and cuts to Part 2's title card.

**Bans for this part.**
- The eligibility form survives only as the case file's cover sheet: two YES/NO boxes and no question text, never a plate of its own.

## Decided

1. **Music video.** The first 1:40 is the existing theme song music video, `assets/music-video/wishonia-theme-song-music-video.mp4`. The drawn style starts at the title card. The video sings Wishonia's full name, so no acronym card is needed.

## Changes from v2

- The office, the wall screen, the cream paper diagrams and Wishonia's corner are gone: Layer A is Wishonia at her lectern in the studio, Layer B is illustrated plates the camera travels over, and every shot runs under the period film.
- Wishonia is on screen only in eligible (where the film first irises in on her face), meet-wishonia, the reaction cut my-surprise and earth-means-dirt. Every other scene is a plate she narrates.
- Labels, arrows and written-out narration are cut: the form's question text, the MONEY banner, the WITHOUT/WITH headings and their tick-and-cross lists, the 604 bar's labels, and the dictionary card (the atom now wears a "DO NOT CUT" tag). The eligibility form survives as the case file's cover sheet, with only its boxes.
- without-with-papers is one long street the camera travels along, one station per line, instead of a split screen; split-the-atom is two scenes on one plate on either side of the reaction cut.
- The humans are the stereotype cast (the Scientist snips the atom, the Weapons Maker builds the bomb), everyday humans get their bodies from their outfits, and the money is green with seals.
- The title card is the period card; the half-sun that sank on it went with the office.

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
- key: the whole heading in, the busy human mid-sprint along the bottom of the card, checking his watch
- cue: "How"
- time: 01:40.3 to 01:48.8 (8.5 s)
- voiceover: "How to End War and Disease (for Busy People) A Step-by-Step Guide to Optimizing Your Terrible Civilization"
- layer: A, title card
- scene: KIT.titleScene's period card: the film's atom emblem on plain navy, and under it the book's title as it is read. Lines in 16:9: "HOW TO END" / "WAR AND DISEASE" / "(for Busy People)" (label style). Lines in 9:16: "HOW TO END" / "WAR AND" / "DISEASE" / "(for Busy People)". The pill under the heading: "A Step-by-Step Guide to Optimizing Your Terrible Civilization".
- props: title-card, human
- status: planned

Moves: "How" → the heading words slam in, one per spoken word ("How", "to", "End", "War", "and", "Disease"). "(for" → "(for Busy People)" slides in under them. "Busy" → a busy human in a suit and bowler (`{ tone: 2, outfit: "suit", hat: "bowler" }`) sprints across the bottom of the card, left to right, eyes on his wristwatch. "A" → the subtitle pill comes in. "Step-by-Step" → his skeleton, in the same bowler, strolls back the other way, slowly, still checking the watch, until the card ends.

Sound: a whirr as the card comes up; a thunk on "Disease"; a quick whistle under the sprinting human.

On screen: "HOW TO END WAR AND DISEASE" / "(for Busy People)" / "A Step-by-Step Guide to Optimizing Your Terrible Civilization".

Why: the narrator reads the title, so this is the one title card in the part. The busy man is the viewer; from Part 10 on he and his skeleton are YOU.

## Scene 3 · loved-ones

- id: loved-ones
- act: Eligibility check
- transition_in: cut
- key: just after the flash: the developed print, the family on the sofa as grinning skeletons, the Grim Reaper grinning between the heads with his arms round them, inside a white photo border (the HOLD)
- cue: "Is"
- time: 01:48.8 to 01:58.4 (9.5 s)
- voiceover: "Is everyone you've ever loved currently being slowly tortured and or brutally murdered by horrible diseases? Do your governments"
- layer: B, plate family-portrait
- scene: A 1950s living room seen straight on, like a portrait sitting: patterned wallpaper, a fringed floor lamp, a mantel clock, a long sofa. An everyday family of four poses on and behind it for a portrait, smiling at us (we are the camera): the father and the mother on the sofa, the boy between them, the grandfather standing behind.
- props: human, reaper, sofa, lamp, flash
- status: planned

Moves: "Is" → the family poses, the camera wide enough for the lamp. "loved" → they all lean in together and smile harder for the picture. "slowly" → the camera starts a slow push in. "tortured" → their chest lights blink red one by one, left to right; the smiles stay, and a bead of sweat runs down the father's temple. "brutally" → the Grim Reaper rises up behind the sofa between the grandfather and the mother, grinning, and puts a bony arm round each of them for the photo. "murdered" → he squeezes them in tight for the picture; every smile goes stiff and stays. "diseases?" → everyone holds still for the picture. after "diseases?" → a flash bulb goes off: a white flash, and the picture is a print, inside a white border with a deckled edge, tilted a little. As the white fades, the print develops: the same poses and the same smiles, but the family are skeletons now (the grandfather's glasses still on his skull), and the Reaper is the only one who looks the same. HOLD: nothing moves until "waste".

Sound: a whoosh as the Reaper rises; a flash-bulb pop after "diseases?"; then silence for the HOLD.

On screen: nothing written.

No: the family stays alive and smiling until the flash; the print, not an x-ray, shows the skeletons (Part 2's the-toll x-rays its family one by one).

Why: the reason the viewer should care, as the family's own portrait: everyone keeps smiling for the picture while the diseases take them.

## Scene 4 · nuclear-winters

- id: nuclear-winters
- act: Eligibility check
- transition_in: cut
- key: the little Earth under a sky full of red snowflakes, "122" among them, the one human on top frozen solid in his block of ice, scarf and all
- cue: "waste money"
- time: 01:58.4 to 02:08.3 (10.0 s)
- voiceover: "waste money on enough nuclear bombs to cause one hundred and twenty-two nuclear winters despite only having the one civilization to apocalypse?"
- layer: B, plate tiny-earth
- scene: The theme song's night sky, navy with mustard stars. One small Earth floats in it (`KIT.props.earthGlobe`), so small that the one human standing on top of it is half its height, with his little house and a picket fence beside him.
- props: earth-globe, missile, price-tag, snowflakes, human, ice-block
- status: planned

Moves: "waste" → the human stands on top of his little Earth, watering a flower by his front door, and waves at us. "nuclear" → a grumpy missile (`KIT.props.missile`, arms crossed) pops up out of the ground beside him, a price tag swinging from its nose. "bombs" → another pops up, and another. "one hundred and twenty-two" → the camera pulls back to the whole planet as missiles pop up row by row, faster and faster, until the little Earth bristles with them like a pincushion and the human stands in the one clear patch on top. "winters" → missile by missile, each blinks into a big red snowflake in a puff of smoke and floats up into the sky; "122" stamps in among them. "despite" → red snow starts falling; the human looks up at it. "only" → he quietly puts on a scarf. "having" → a snowdrift grows over the planet, over his roof, up to his chest. "civilization" → buried to the chin, his teeth chatter. "apocalypse?" → he freezes solid in a block of ice, scarf and all, the watering can still in his hand.

Sound: a boing as the first missile pops up; a pop on "hundred" and on "twenty-two" as the rows speed up; a thunk as "122" stamps in; a whoosh of wind as the snow starts; chattering teeth from "civilization"; an ice ding on "apocalypse?".

On screen: "122".

No: no counter ticking up to 122; the missiles popping up are the count.

Why: the waste, as one number against one planet.

## Scene 5 · eligible

- id: eligible
- act: The verdict
- transition_in: iris in on Wishonia's face (the first time the film shows her)
- key: the stamp just lifted off the case file: "MAY BE ELIGIBLE FOR OPTIMIZATION" in red across the form on its cover, both YES boxes ticked
- cue: "If"
- time: 02:08.3 to 02:13.6 (5.3 s)
- voiceover: "If so, your planet may be eligible for optimization."
- layer: A, host
- scene: The studio. To Wishonia's left (screen right), on a little studio easel beside the lectern, the Earth case file faces us: a manila folder with a tab "EARTH: CASE #847", whose cover sheet is the 1950s mail-in form "PLANET ELIGIBILITY CHECK" with two YES/NO boxes (no question text; fine print "Please allow 4 to 6 weeks for optimization."). The rubber stamp (`KIT.props.stamp`) waits on the easel's ledge. On the lectern's far end (screen left), a wire out-tray "PLANETS" holds two other files: "VENUS: TOO HOT" and "MARS: NOBODY HOME". The file is on the easel, not the lectern, so her face stays clear.
- wishonia: happy-smile + body-presenting; happy-smile + body-palms-down on "eligible"
- props: studio, lectern, easel, case-file, eligibility-form, pencil, stamp, stamp-mark, out-tray
- status: planned

Moves: "If" → the iris opens on her face. "so," → a pencil ticks YES in box 1, then in box 2, by itself. before "eligible" → the stamp hops up into the air and she huffs on it. "eligible" → it slams down on the case file: "MAY BE ELIGIBLE FOR OPTIMIZATION", in red, across the form; the lectern shakes. after "optimization." → she blows on the wet ink, and the file flies off the easel, across in front of her, into the PLANETS tray, on top of VENUS and MARS.

Sound: a pencil scratch per tick; a huff before "eligible"; a stamp thunk on "eligible"; a whoosh as the file slides into the tray.

On screen: "EARTH: CASE #847", "PLANET ELIGIBILITY CHECK" with YES and NO, "MAY BE ELIGIBLE FOR OPTIMIZATION", "PLANETS", "VENUS: TOO HOT", "MARS: NOBODY HOME".

No: the form has no question text; the narrator asked the questions.

Why: the pitch, and the setup for the ending's stamp.

## Scene 6 · meet-wishonia

- id: meet-wishonia
- act: Meet Wishonia
- transition_in: same shot (no seam)
- key: after "years." (second): the charred converter's singed card reads 4,297 YEARS under the studio card that reads the same, and Wishonia looks at the camera
- cue: "I'm"
- time: 02:13.6 to 02:29.3 (15.7 s)
- voiceover: "I'm Wishonia Love. C.E.O. and President of Universe Optimization Services. I've been upgrading civilizations for four thousand, two hundred and ninety-seven years, which in your Earth time is four thousand, two hundred and ninety-seven years."
- layer: A, host
- scene: The same shot. The empty easel slides away, and a brass desk nameplate slides onto the front edge of the lectern and grows; on the free wall to her right a studio card drops in, and a 1950s unit converter rises in under it and blows up.
- wishonia: happy-smile + body-hand-chest; smirk-smile + body-open-palms on "Earth"; smirk-closed + body-idle on "years." (second), the look at the camera
- props: studio, lectern, nameplate, studio-card, converter, nuke
- status: planned

Moves: "I'm" → the empty easel slides off to the right. "Wishonia" → a brass nameplate slides onto the lectern's front edge: "WISHONIA LOVE". "C.E.O." → a second line clicks in under the name: "C.E.O. AND PRESIDENT". "Universe" → a third line, "UNIVERSE OPTIMIZATION SERVICES", and the nameplate keeps sliding out sideways to fit it, past the end of the lectern and out of the left of the frame, sagging under its own length like a diving board. "four thousand" (first) → a studio card drops in on two strings on the wall to her right: "4,297 YEARS". "which" → a 1950s unit converter rises into the picture under the card: a cabinet with two dials, a crank, a bell, a card slot and a little chimney. "Earth time" → it cranks into action: the dials spin, the gears whirr, it shakes harder and harder, glows red and puffs steam. 1.1 s after "Earth" → it blows up: a white flash, the studio shakes, and a little mushroom cloud stands where it was. The cloud clears on a charred, bent, smoking wreck (dented, chimney bent, a gear sprung out on its spring, the crank hanging limp); two white eyes open in the soot and blink. after "years." (second) → the wreck's bell still dings and it spits out its singed card (above y 900 in 16:9): "4,297 YEARS". Wishonia looks at the camera; nothing moves.

Sound: a slide whoosh as the nameplate comes in, and a longer one on "Universe"; whirring gears on "Earth"; a boom 1.1 s after it; a bell ding after "years." (second); then silence for the look.

On screen: "WISHONIA LOVE" / "C.E.O. AND PRESIDENT" / "UNIVERSE OPTIMIZATION SERVICES" / "4,297 YEARS" (the studio card) / "4,297 YEARS" (the singed card).

No: the mushroom cloud stays over the converter and never reaches her.

Why: who is talking, and the first dry joke in her voice.

## Scene 7 · split-the-atom

- id: split-the-atom
- act: What Wishonia noticed
- transition_in: cut
- key: after "it.": the shears have snipped the atom in two; its halves fall off the cushion, the "DO NOT CUT" tag flutters down between them and the Scientist grins
- cue: "I started watching"
- time: 02:29.3 to 02:47.2 (17.9 s)
- voiceover: "I started watching your planet in nineteen forty-five when you split the atom. "Atom" comes from your Greek word meaning "unable to be cut," so naturally, you cut it. This was very human of you. I assumed you were trying to unlock unlimited free energy."
- layer: B, plate atom-street
- scene: One long plate on a plain field under a cream sky. On the left, a pedestal with a red velvet cushion, and on it a big glowing atom (the film's emblem: three electrons whizzing round an orange nucleus) wearing a tag on a string, like a mattress tag: "DO NOT CUT". On the right, a 1950s street: two little ranch houses (`KIT.props.house`) side by side, a picket fence between their front yards, a string of light bulbs from porch to porch, and a toaster on the fence post.
- props: atom, tag, shears, scientist, house, fence, bulbs, toaster, human
- status: planned

Moves: "watching" → the camera on the atom on its cushion, humming and glowing, the tag hanging off it. "nineteen forty-five" → "1945" stamps into the sky above it. "split" → the Scientist (`KIT.cast("scientist")`) tiptoes in behind the pedestal with a giant pair of shears. "Greek" → the camera pushes in on the tag: "DO NOT CUT". "cut," → the shears open round the atom; she reads the tag and looks at us. "naturally," → she grins. after "it." → SNIP: the atom falls apart into two glowing halves that drop off the cushion, and the tag flutters down. "very human" → she holds up the shears, proud. "assumed" → the two halves roll off to the right, and the camera travels with them down the street, one into each front yard, where two neighbors (everyday humans, one in shirtsleeves, one in a cardigan) pick them up. "unlock" → each plugs his half into his house on a long cord. "free energy" → the string of bulbs lights up from porch to porch and the windows glow; one neighbor drops two slices of bread into the toaster on the fence post, and they pop up golden. The neighbors wave to each other over the fence.

Sound: a thunk as "1945" stamps in; a snip after "it."; light-switch clicks on "free"; a toaster pop as the toast comes up.

On screen: "1945" and the tag "DO NOT CUT".

No: no dictionary card; the tag says it.

Why: the setup: a thing named for not being cuttable, cut at once, and a new power that starts out lighting porches.

## Scene 8 · my-surprise

- id: my-surprise
- act: What Wishonia noticed
- transition_in: cut
- key: on "surprise": the crash zoom in on her surprised face
- cue: "You can imagine"
- time: 02:47.2 to 02:49.2 (1.9 s)
- voiceover: "You can imagine my surprise"
- layer: A, host
- scene: A reaction cut to Wishonia at her lectern (the PLANETS tray at its end, the case file in it, as eligible left it; no easel).
- wishonia: neutral-smile + body-open-palms; surprised-oh + body-open-palms on "surprise"
- props: studio, lectern, out-tray
- status: planned

Moves: "You" → Wishonia at the lectern, polite. "surprise" → the camera snaps in on her face, a 1950s crash zoom, and holds there, surprised. The plate comes back on "when".

Sound: a slide whistle up on the crash zoom.

On screen: nothing new.

No: no plate in this shot; it is her own reaction to her own line.

Why: a reaction cut on the big turn; the plate's payoff comes on the next words.

## Scene 9 · pointing-at-each-other

- id: pointing-at-each-other
- act: What Wishonia noticed
- transition_in: cut back to the plate, where the camera would have got to
- key: on "That's": the cloud thinned away: both neighbors charred black and smoking, still aiming at each other over the fence, hair straight up, only their eyes white
- cue: "when"
- time: 02:49.2 to 02:54.6 (5.4 s)
- voiceover: "when I realized you were just pointing it at each other! That's kind of like"
- layer: B, plate atom-street
- scene: The same street, the camera on the two neighbors at the fence.
- props: house, fence, bulbs, toaster, human, nuke
- status: planned

Moves: "when" → the bulbs go out, one after another; the neighbors stop waving. "realized" → each unplugs his glowing half. "pointing" → they turn and point the halves at each other over the fence, scowling. "each" → they fire: the two halves streak to the middle. "other!" → a white flash, the frame shakes, and a mushroom cloud stands over the fence. "That's" → the cloud thins away: both stand exactly where they were, still aiming, charred black and smoking, hair straight up, only their eyes white; the houses are charred too. "kind" → the charred toaster on the fence post pops up two slices of black toast. "like" → both blink.

Sound: a switch click as the bulbs go out; a low hum as they turn; a zap as they fire; a boom on the flash; a sizzle as the smoke clears; a toaster pop on "kind".

On screen: nothing written.

Why: first evidence that humans point every new power at each other.

## Scene 10 · fire-on-fire

- id: fire-on-fire
- act: What Wishonia noticed
- transition_in: cut
- key: on "yourself": both cavemen on fire all over, arms up, running in circles round the campfire
- cue: "discovering"
- time: 02:54.6 to 03:00.4 (5.8 s)
- voiceover: "discovering fire and then immediately using it to set yourself on fire."
- layer: B, plate cave
- scene: The mouth of a cave in a plain hillside, flat stone shapes. Two cavemen (everyday humans in spotted tan pelts, bare feet, wild hair) stand on either side of an unlit campfire.
- props: cave, campfire, burning-stick, human, flames
- status: planned

Moves: "discovering" → the two cavemen look down at the unlit campfire. "fire" (first) → it lights; both smile and warm their hands. "using" → each reaches into the fire and comes out with a burning stick; the sticks cross over the flames. "set" → they wind up, frowning at each other. "yourself" → they jab each other, one at the head and one at the belly, and both go up in flames all over: arms up, yelping, running in circles round the fire. "fire." (last) → the flames go out in a puff of soot; it clears on two charred cavemen, hair straight up, smoking, blinking. after "fire." (last) → they look at each other, look down at the campfire, and each reaches in for a new stick.

Sound: a whoosh of fire as the campfire lights; another and two yelps as they catch; a sizzle as the flames go out.

On screen: nothing written.

Why: the same point as the atom, in a picture a child gets.

## Scene 11 · earth-means-dirt

- id: earth-means-dirt
- act: What Wishonia noticed
- transition_in: cut
- key: on "want...": the shrug, the marker hovering by the case file's tab on the easel, "EARTH" crossed out and "DIRT" written over it
- cue: "The second thing"
- time: 03:00.4 to 03:11.4 (11.0 s)
- voiceover: "The second thing I noticed is that your planet is named "Earth," which means dirt. You named your planet.. dirt. Okay, if that's what you want..."
- layer: A, host
- scene: The studio, as in eligible: the easel to her left, the PLANETS tray on the lectern's far end.
- wishonia: skeptical-closed + body-idle; skeptical-closed + body-shrug on "want..."
- props: studio, lectern, easel, case-file, marker, out-tray
- status: planned

Moves: "The" → the easel slides back in from the right, and the case file hops out of the PLANETS tray onto it, "MAY BE ELIGIBLE FOR OPTIMIZATION" across its cover. "Earth," → the camera pushes in a little, so the tab reads: "EARTH: CASE #847". "dirt." (first) → a fat red marker crosses out EARTH, by itself. "dirt." (second) → it writes "DIRT" above it. "Okay," → the marker hovers. "want..." → she shrugs. after "want..." → the file hops back into the PLANETS tray, onto VENUS and MARS, and a puff of brown dust comes up out of it.

Sound: a marker squeak on each "dirt."; a thunk and a puff as it lands in the tray.

On screen: the tab "~~EARTH~~ DIRT: CASE #847".

No: no globe made of mud; the file is the joke.

Why: a breather joke between two pieces of evidence.

## Scene 12 · pentagon

- id: pentagon
- act: What Wishonia noticed
- transition_in: cut
- key: after "Square": the pull back on all four buildings in a row with their signs, the dog's head out of the triangle doghouse
- cue: "I also noticed"
- time: 03:11.4 to 03:22.8 (11.4 s)
- voiceover: "I also noticed that you call your war building "The Pentagon" because it has five sides (this is like naming a hospital "Rectangle" or calling a school "Square")."
- layer: B, plate four-buildings
- scene: A plain field under a cream sky, four lots along it from left to right: bare ground where the war building will stand, then room for a hospital, a school and one more.
- props: pentagon, sign, paint-roller, missile, hospital, school, doghouse, democracy-dog
- status: planned

Moves: "war" → an honest sign springs up out of the bare ground: "WAR BUILDING". "Pentagon" → a plain five-sided building with a courtyard (seen from a little above) draws itself on around the sign's posts, and a paint roller slaps onto the sign and rolls "THE PENTAGON" over the old words; the fresh paint drips. "five sides" → its five walls flash one after another. after "sides" → a grumpy missile pokes up out of the courtyard, looks left, looks right, looks at us, scowls, and ducks back down on "a" ("naming a hospital"), leaving a puff of smoke. "Rectangle" → the camera travels right as a plain rectangle hospital drops onto the next lot, its name on its cornice: "RECTANGLE". "Square" → a square school drops in next to it, a bell on its roof: "SQUARE". after "Square" → the camera pulls back on the row, and a fourth building drops in that nobody mentioned: a triangle doghouse with its sign, "TRIANGLE". The Democracy Dog pokes its head out (its first appearance; it comes back in Part 6).

Sound: a pop as the honest sign springs up; a splat as the roller hits it; a tick per wall; a slide whistle down as the missile ducks; a thunk per building; a small woof.

On screen: "WAR BUILDING" (under the paint), "THE PENTAGON", "RECTANGLE", "SQUARE", "TRIANGLE".

Why: names that describe the shape and hide the purpose.

## Scene 13 · papers-with-presidents

- id: papers-with-presidents
- act: The papers
- transition_in: cut
- key: on "money,": every head in the crowd snapped toward the little paper, all but one bored human at the far left still staring at the ground
- cue: "However,"
- time: 03:22.8 to 03:40.6 (17.8 s)
- voiceover: "However, the most fascinating discovery about your species is that you only do things when given small pieces of paper with presidents on them. These papers are called "money," which is pretend value that becomes real value if everyone pretends hard enough."
- layer: B, plate town-square
- scene: A plain town square: paving stones, a lamppost, a bench. A crowd of ten everyday humans stands about, doing nothing.
- props: plain-paper, human, lamppost, bench
- status: planned

Moves: "However," → the camera travels slowly along the crowd: they stand still, bored; one yawns, one studies a thread on his sleeve. "fascinating" → a fly lands on somebody's nose; nobody moves. "paper" → one paper (plain, no seal) walks in from the right on its stick legs. "presidents" → the camera pushes in on its oval portrait (a generic old man in a wig), who winks on "them.". "money," → every head snaps toward it, all but one: a bored human at the far left keeps staring at the ground. after "money," → the crowd follows the paper off in a conga line and leaves him standing alone; he lifts his head and looks after them, too late. "value" (first) → the line comes back round from the left behind him; the paper walks straight over him and flattens him like a pancake, only his blinking eyes showing, and the whole line walks over him. "everyone" → he peels himself off the paving, springs back up a little shorter, limps after the line with stars circling his head, and joins the back of it. "pretends" → the whole line squeezes its eyes shut and trembles, and the paper starts to glow. "hard" → the woman at the front pretends so hard that her head pops off and spins up into the air; the paper glows brighter. "enough." → the paper sparkles. after "enough." → the head lands back on her neck upside down, eyes still squeezed shut.

Sound: tiny squeaky footsteps for the paper; a whoosh as the heads turn; a splat when the paper flattens the slow human; a boing as he springs back up; a pop as the head comes off; a sparkle on "enough."; a thunk as the head lands.

On screen: nothing written.

No: no MONEY banner; the narrator defines it.

Why: introduces the main actor of Layer B, and the most fascinating species in the universe standing about doing nothing.

## Scene 14 · without-with-papers

- id: without-with-papers
- act: The papers
- transition_in: cut
- key: after "this).": the bomb has gone off in the Weapons Maker's face; he stands charred and smoking, hard hat on, still grinning and hammering, a little mushroom cloud rising behind him, war papers round his boots and a new bomb popping onto the bench
- cue: "Without"
- time: 03:40.6 to 04:08.6 (28.0 s)
- voiceover: "Without these papers, you won't: Save lives (requires many papers). Cure diseases (requires very many papers). Feed hungry people (requires papers, even though food grows for free). But WITH these papers, you will: Build bombs (you love giving papers for this). Start wars (somehow this makes more papers). Destroy the planet (surprisingly profitable in papers)."
- layer: B, plate papers-street
- scene: One long street on a plain field, and the camera travels along it left to right, one station per line. The left half has no papers at all: a hospital (`KIT.props.hospital`), a lab bench (`KIT.props.lab`) and a bare field. The right half fills with war-seal papers: a workbench where the Weapons Maker builds a bomb (`KIT.props.bomb`), a war table with a world map (`KIT.props.worldMap`) and two generals, and a hill with a digger on it.
- props: hospital, lab, scientist, wheat, wallet, moth, cobweb, spider, papers-war, bomb, weapons-maker, world-map, nuke, earth-globe, human, skeleton
- status: planned

Moves: "Without" → the camera on the hospital: a patient in a dressing gown sits on the bench outside, a thermometer in his mouth, his chest light blinking red. "Save lives" → he looks hopefully at the door. "many papers" → the sign on the door flips to CLOSED. after "papers)." → he x-rays into a skeleton and stays sitting there, grinning, thermometer in his teeth. "Cure diseases" → the camera travels right to the lab bench, where the Scientist stands by her bubbling flask with her clipboard. "very many papers" → a cobweb grows between her and the flask, a spider lowers itself on its thread, and the flask stops bubbling. after "papers)." → she x-rays into a skeleton, still in her lab coat, still holding the clipboard. "Feed hungry people" → the camera travels on to a bare field and a thin, hungry human, his belly growling. "grows" → a wheat stalk grows up out of the ground by itself, right in front of him. "free)." → he looks at the wheat, then into his wallet: a moth flies out. after "free)." → he x-rays into a skeleton, still holding the empty wallet open. "WITH" → a flood of war papers runs in from the right on their stick legs, and the camera travels with them into the busy half. "Build bombs" → the Weapons Maker hammers away at a bomb on his workbench. "giving papers" → two papers hop into a slot in the bomb, which swells. after "this)." → it blows up in his face: a blast, a little mushroom cloud, a shake; he stands there charred black and smoking, hard hat on, still grinning, and keeps hammering, and a new bomb pops onto the bench. "Start wars" → the camera travels on to the war table, where two generals (everyday humans in olive suits with medals) push toy missiles across the map at each other. after "wars" → each toy turns into a tiny mushroom cloud on the map. "more papers" → a paper pops out of each little cloud like popcorn and lands in the generals' hands. "Destroy" → the camera travels to the hill, where a sweating digger in overalls shovels a crater into its top. after "planet" → the dirt cracks and falls off both sides: the hill is the Earth, with a big bite out of its top, molten inside. "profitable" → papers sprout from the bite like wheat, and the digger grins. after "papers)." (last) → the camera whips back left along the whole street to the start: the three skeletons still sit there grinning, and the wheat has grown taller than the hospital.

Sound: crickets on "Without"; a click as the door sign flips; an x-ray zap after each of the three "papers)." lines' x-rays (the patient, the Scientist, the hungry human); frantic hammering on "WITH"; a boom when the bomb goes off; a pop for the tiny clouds; a cash-register ding for the papers from the clouds and for the papers sprouting from the Earth; a whoosh on the whip back.

On screen: the hospital's own sign and its door sign "CLOSED".

No: no WITHOUT/WITH headings, no ticks or crosses, and no war arrows; the toy missiles and the tiny clouds do it.

Why: the rule the whole plan uses: papers decide what humans do.

## Scene 15 · 604-papers

- id: 604-papers
- act: The papers
- transition_in: cut
- key: after "work.": the war paper standing on the flattened medicine paper at the foot of the stack, its little arm poking out and waving weakly, "604 : 1" in the sky
- cue: "In fact,"
- time: 04:08.6 to 04:18.5 (9.9 s)
- voiceover: "In fact, your governments spend six hundred and four papers on weapons for every one paper on testing which medicines work."
- layer: B, plate 604-bar
- scene: A plain field under an open cream sky. One medicine paper stands on it; a stack of war papers rises beside it, far past the top of the frame.
- props: papers-war, papers-med, airplane, clouds
- status: planned

Moves: "In" → the medicine paper (cross seal) stands alone on the field, small and cheerful. "six hundred and four" → war papers (missile seals) march in from the left and hop up onto each other into a stack beside it, faster and faster, and the camera tilts up with the stack, up past the clouds. "weapons" → a small airplane has to swerve round the top of the stack. "for every" → the camera falls all the way back down. "one paper" → it lands on the one medicine paper, which waves; "604 : 1" stamps into the sky. "testing" → the medicine paper leans back and looks up at the stack. "medicines" → far above, one war paper slides off the top and drifts down, rocking like a leaf. after "work." → it drops like an anvil and flattens the medicine paper. The war paper stands on it; the medicine paper's little arm pokes out from under and waves weakly. The part ends on that frame.

Sound: a rising slide whistle as the stack climbs; an airplane whoosh; a falling slide whistle; a thunk as "604 : 1" stamps in; a splat when the war paper lands; a tiny squeak from under it.

On screen: "604 : 1".

No: no number but "604 : 1".

Why: the spine's payoff, and the number the rest of the episode fixes.
