---
format: 1920x1080
duration: 0:49.5
message: "Humanity knows war is illogical (it makes movies, books and prizes against it) and keeps paying for war anyway, like a game where the objective is to lose."
arc: Title card (a falling star that is a missile) → Wishonia: your species KNOWS (a tourist taps his temple with a hammer and bonks himself) → the tourist tours the Museum of Knowing Better, agrees with every exhibit and is wrecked by each one's opposite → humanity's board game, objective lose, ends in a mushroom cloud and a reset → Wishonia defines "digress" while war papers march across her lectern and keep going, even after the iris should have stopped them
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 7, "Humanity's Death Wish"
audio: index-manual.cbaf659d.mp3, 14:08.5 to 14:58.0
version: v3
---

# Part 7 storyboard: "Humanity's Death Wish"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The episode is a 1950s atomic-age instructional film. Layer A is Wishonia at her lectern talking to the viewer (`KIT.studio`); Layer B is an illustrated plate the camera travels over (`KIT.camera`), one framing per phrase, and there she is only the voice. The money is green, and its seal says what it buys (a missile for war, a cross for medicine). Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Cast.** The tourist, an everyday human (`{ tone: 1, outfit: "shirt", color: 3, seed: 7 }`: a mustard shirt, a camera on a rust strap at his chest and an audio-guide handset on an orange lanyard), in host-knows, museum-of-knowing and, as his skeleton, lose-elaborately: draw him with these options in all three. The Weapons Maker (`KIT.cast("weaponsMaker")`, with his smiling baby missile), the Politician (`KIT.cast("politician")`) and the Scientist (`KIT.cast("scientist")`). The prize winner is an everyday woman.

**Spine.** The tourist who knows. In host-knows he stands beside Wishonia's lectern, taps his temple knowingly with a hammer and bonks himself with it. Then he tours the Museum of Knowing Better, agrees with every exhibit (he sobs at the anti-war film, buys the peace book, applauds the peace prize) and is wrecked by each one's opposite: a bump, then charred, then a stripe shaved through his hair, then a grinning skeleton. His skeleton sits down at humanity's board game in lose-elaborately, and it is the one that sets the board up again after the bomb.

**Callbacks.**
- From Part 1 (pentagon): the plain five-sided building and its grumpy courtyard missile are the DEPARTMENT OF DEFENSE exhibit, and the sign's paint peels back to WAR, as the honest WAR BUILDING sign was painted over.
- From Part 1 (604-papers): a paper flattens someone and a little hand waves weakly from underneath (the prize winner under the giant check).
- From Part 2 (money-loop): the Weapons Maker's smiling baby missile, and the charred look (black, smoking, hair straight up, only the eyes blink).
- The seal flip, run backwards: a TAX rubber stamp turns the tourist's plain paper into war money.
- Style bible gag 3: Wishonia's mug sip before the last punchline, the mug down slowly after it. Gag 6: the iris opens on her face after the title card and closes on it at the end.

**Set up here.** lose-elaborately's board game is the episode's first 1950s board game. In Part 24's game-box the new lid, THE EARTH OPTIMIZATION GAME, lifts off this one's OBJECTIVE: LOSE lid: the same box, now played to win. So draw this box the way Part 24 draws its own: an orange box round a cream board, a track of squares in orange, mustard, slate blue and rust, START on a mustard square at the front left, and a lid the size of the box.

**Held frame.** None. No line in this part is a death toll.

**Transitions.** The title card comes up from black and goes to black (`KIT.titleScene`); host-knows irises in on Wishonia's face. Host to plate, plate to plate and plate to host are cuts. museum-of-knowing is one plate: the camera travels along it from exhibit to exhibit with no seam. host-digress irises out on her face at the end of the part (Part 8's title card comes up from black).

**Bans for this part.**
- The camera frames one exhibit at a time, and an exhibit's own sign is its only text.
- The exhibits are generic and drawn: no real film, book cover, medal or seal; the five-sided building is Part 1's plain drawing of it.
- host-digress's war papers march in a line; they never stack up (a tall stack of war money is the 604 bar of Parts 1 and 6).

## Changes from v2

- The new look: Wishonia leaves her office and her corner. She talks to the viewer at her lectern in host-knows and host-digress; the museum and the living room are plates the camera travels over, with her as the voice.
- host-knows is new: "What's most endearing ... illogical:" moves from the museum's entrance to a host shot, and the tourist's knowing wink becomes a hammer he taps his temple with and then bonks himself with.
- Labels out: the exhibits keep only their own signs (the TV film loses WAR IS BAD, the stage loses its PEACE PRIZE banner), and the TAX funnel becomes a TAX rubber stamp.
- digress-dictionary becomes host-digress: the dictionary card on the wall screen is gone (it wrote the narration out). War papers now march across her lectern and will not stop: one wades through her mug, and the last one wedges the closing iris open.
- lose-elaborately keeps "But I digress." (the cut to Wishonia moves to "That's"), so its button has time to play: the players charred, the skeleton setting the tiny Earth back on START. The chain reaction is one long run of dominoes round the room instead of five kinds of contraption.
- The title card is the period card: the falling star that turns into a missile now crosses the navy card behind the heading, without the wisher.

## Scene 1 · death-wish-title

- id: death-wish-title
- act: Title
- transition_in: up from black (a cut from Part 6's last frame)
- key: after "Wish.": the heading on the navy card, and the falling star turned into a smiling missile, trailing the star's sparkles, nosing down behind WISH
- cue: "Humanity's Death Wish"
- time: 14:08.5 to 14:10.8 (2.3 s)
- voiceover: "Humanity's Death Wish."
- layer: A, title card
- scene: The period title card (`KIT.titleScene`, look "atomic"): the heading in the cover font on plain navy under the film's emblem, whose electrons are running war papers. 16:9 lines: `[{ words: ["HUMANITY'S"], style: "small" }, ["DEATH", "WISH"]]`; 9:16 (`linesTall`): `[{ words: ["HUMANITY'S"], style: "small" }, ["DEATH"], ["WISH"]]`. The heading is on the card as it comes up from black (no `spoken`, as in Part 2). The small gag goes in the `gag` hook.
- props: title-card, star, missile, mushroom-cloud
- status: planned

Moves: "Humanity's" → the card comes up from black with the heading on it. High on the left, a mustard star (the theme song's kind) comes loose from the navy and starts to fall toward the heading, trailing sparkles. "Wish." → as it falls it grows fins, a nose cone and a grin: a smiling baby missile. 0.6 s after "Wish." starts → it noses down behind WISH, a small mushroom cloud (`KIT.nuke`, small, in `ctx.back`) puffs up behind the word, and the card shakes once before it goes to black.

Sound: a whirr under the card; a falling slide whistle as the missile dives; a small boom as the cloud puffs up.

On screen: "HUMANITY'S DEATH WISH".

No: no wisher; the star falls on its own.

Why: the narrator reads the heading, and a wish on a falling star that turns out to be a missile is the part in one picture.

## Scene 2 · host-knows

- id: host-knows
- act: It knows
- transition_in: iris in on her face
- key: after "illogical:": the tourist beside the lectern grinning, a bump swelling out of his hair with three stars circling it, the hammer in one hand and a thumbs-up in the other; Wishonia shrugging with a smirk
- cue: "What's most endearing about"
- time: 14:10.8 to 14:16.2 (5.4 s)
- voiceover: "What's most endearing about your species is it KNOWS it's being illogical:"
- layer: A, host
- scene: The host's set (`KIT.studio`): Wishonia at the lectern, and in the free wall at her right (`KIT.STUDIO.right`) the tourist, standing as big as the hungry man in Part 2's host-closes, facing her, a claw hammer in his hand.
- wishonia: happy-smile + body-hand-chest; excited-ee + body-point-right on "KNOWS"; smirk-smile + body-shrug on "illogical:"
- props: studio, human, hammer
- status: planned

Moves: "What's" → the iris opens on Wishonia's face, her hand on her chest, and the camera pushes in slowly as in Part 2's host-opens. The tourist is already there, looking up at her and nodding along. "endearing" → he beams at us and gives a little wave. "KNOWS" → Wishonia points at him; he taps his temple with the hammer's head, tap, tap, and winks at us: he knows. "illogical:" → 0.3 s in, he swings it: BONK, on top of his own head. 0.25 s later → a bump swells up out of his hair and three little stars circle it; he keeps grinning and gives us a thumbs-up. The bump stays on him through the museum.

Sound: a thunk for the bonk; a boing as the bump swells.

On screen: nothing written.

No: no thought bubble and no "I KNOW" sign; the hammer says it.

Why: the species knows and does it anyway, shown once by the human who is about to tour the proof.

## Scene 3 · museum-of-knowing

- id: museum-of-knowing
- act: It knows
- transition_in: cut
- key: after "manufacturers).": on the prize stage the giant check lies flat where the winner stood, her hand poking out from under it with a dove on one finger, waving weakly; the Weapons Maker grinning over it with his hands still up; the charred tourist at the left applauding, soot puffing off his hands
- cue: "You have movies"
- time: 14:16.2 to 14:43.1 (26.8 s)
- voiceover: "You have movies about how wars are bad (which you watch between wars). You have books about peace (that you tax to buy bombs). You give prizes to people who promote peace (funded by weapons manufacturers). You have a "Department of Defense" (that mainly just attacks people). You have a "Department of Health" (that apparently makes coronaviruses and has not yet produced any observable health)."
- layer: B, plate museum
- scene: One long gallery: a plain wall over a parquet floor, five exhibits in a row in the order the narrator lists them: 1 a TV set on a plinth beside a tall window, under the museum's banner; 2 a gift-shop counter piled with PEACE books; 3 a small prize stage with a velvet curtain; 4 a scale model of the five-sided building on a plinth; 5 a glass display case, with a gauge on the wall beside it. The camera travels right along it with the tourist, one exhibit per sentence, and pushes in for each payoff.
- props: museum-gallery, banner, tv-set, window, curtain, human, book, money, stamp, bomb, mushroom-cloud, stage, medal, dove, weapons-maker, giant-check, pram, missile, pentagon, sign, glass-case, scientist, germ, gauge
- status: planned

Moves:
- The film. "You" → cut in, a little wide, on the first exhibit: the banner "MUSEUM OF KNOWING BETTER" on the wall over a 1950s TV set on a plinth (`KIT.props.tvSet`), and beside it a tall gallery window with curtains and a sunny sky outside. The tourist (the bump still on his head) stands at the TV, the audio guide at his ear. "movies" → the camera pushes in on him and the TV; the TV clicks on: a sad war film, an empty soldier's helmet on a rifle in the rain. "bad" → he bursts into tears, two arcs of water spurting from his eyes, and honks into a hanky. "between" → through the window, a smiling missile streaks past. "wars)." (second) → a mushroom cloud rises on the horizon in the window, the window flashes white, and 0.4 s later, without taking his eyes off the TV, he reaches over, yanks the curtain shut and keeps sobbing.
- The book. "books" → the camera travels right with him to a gift-shop counter piled with big books, PEACE on every cover. He hugs one to his chest, "peace" (first) → and slaps a plain paper (`KIT.money("plain")`) on the counter to pay. "tax" → a rubber stamp marked TAX (`KIT.props.stamp`) thumps down on the paper; it comes up with a missile seal: war money (the seal flip, run backwards). "buy" → the war paper hops off the counter onto a round black bomb (`KIT.props.bomb`) waiting below it; the fuse lights itself and the bomb rolls to his feet. "bombs)." → it goes off: a white flash, a small mushroom cloud, the gallery shakes. after "bombs)." → the smoke clears on him charred black and smoking, hair straight up, still hugging PEACE; only his eyes blink. He opens the book and the page crumbles to ash.
- The prize. "prizes" → the camera travels right; he follows, leaving sooty footprints, to a small stage with a velvet curtain behind a podium, a gold medal gleaming on a cushion. "promote" → the winner (an everyday woman in a dress, a white dove on her finger) steps up onto the podium and the medal is hung round her neck. "funded" → the curtain behind her drops: the Weapons Maker grins round his cigar, holding up a giant check (money green, missile seal) that reads "PAY TO: PEACE"; his baby missile watches from a pram, in a bonnet. "weapons" → he hoists the check high over her head. "manufacturers)." → he lets go: it falls flat like an anvil and flattens her. after "manufacturers)." → her hand pokes out from under it, the dove on one finger, and gives a weak little wave; the baby missile winks; the charred tourist applauds, soot puffing off his hands.
- The first department. "Department" (first) → the camera travels right to a plinth with a scale model of the plain five-sided building from Part 1 and a sign on a stick: "DEPARTMENT OF DEFENSE". "mainly" → the grumpy courtyard missile pokes up, looks left, looks right. "attacks" → it ducks, and tiny missiles shoot out of all five sides at once, punching holes through the gallery walls; daylight beams in through the holes, and one tiny missile shaves a stripe through the tourist's upright hair. "people)." (second) → the sign's paint peels off in one curl: under DEFENSE it says WAR.
- The other department. "Department" (second) → the camera travels right to a glass case under the sign "DEPARTMENT OF HEALTH": the Scientist stands in it like a diorama figure, beaming, holding up her bubbling flask; on the wall beside it, a big gauge (`KIT.props.gauge`) marked OBSERVABLE HEALTH, its needle on 0. "makes" → she gives the flask a proud shake. "coronaviruses" → the bubbles rising out of it are little spiky grinning germs (`KIT.props.germ`); they pop out through the top of the case and bounce round the gallery, off the walls and off the tourist's head. "and" → one settles on his shoulder, and his check-engine light starts blinking red. "not" → he turns to the gauge. "observable" → he taps its glass, tap, tap, tap; the needle twitches up and falls back to 0. "health)." (second) → he x-rays into a grinning skeleton (`KIT.xray`), still tapping. after "health)." → the camera pulls back a little: the skeleton gives the glass one more tap, and the needle drops off its pivot onto the floor.

Sound: a whoosh as the missile passes the window and a distant boom; a rubber-stamp thump on "tax"; a boom on "bombs"; a splat as the check lands and applause pats after it; pops as the tiny missiles fire and a paint scratch as the sign peels; a boing for the germs; three ticks on the gauge glass; an x-ray zap.

On screen: "MUSEUM OF KNOWING BETTER" (the banner) / "PEACE" (the books) / "TAX" (the stamp) / "PAY TO: PEACE" (the check) / "DEPARTMENT OF DEFENSE", then "DEPARTMENT OF WAR" / "DEPARTMENT OF HEALTH" / "OBSERVABLE HEALTH" and 0 (the gauge).

Why: five proofs that humans know better, in the order the narrator lists them, each one paid for by the same human.

## Scene 4 · lose-elaborately

- id: lose-elaborately
- act: The game
- transition_in: cut
- key: on "elaborately": the living room from the back of the camera's pull, a long line of dominoes fallen off the card table, across the floor and up a propped book onto the sofa, where the front is tipping; the baby missile hanging on its string from the lamp right over the tiny Earth, a lit candle and its fuse waiting at the table's far end, the three players cheering, the lid "OBJECTIVE: LOSE" propped against a table leg
- cue: "It's like humanity is playing"
- time: 14:43.1 to 14:52.3 (9.2 s)
- voiceover: "It's like humanity is playing a game where the objective is to lose, but it is trying to lose as elaborately as possible. But I digress."
- layer: B, plate living-room
- scene: A 1950s living room: a card table under a hanging lamp in the middle, a sofa, a mantel and a bookcase round the walls. At the table, humanity: the Politician, the Weapons Maker (cradling his baby missile) and the tourist's skeleton, the audio guide still round its neck. They play a board game whose lid says the objective is to lose, and they lose it with one run of dominoes that goes all the way round the room.
- props: living-room, card-table, lamp, board-game, earth-globe, politician, weapons-maker, missile, human, dominoes, candle, fuse, mushroom-cloud
- status: planned

Moves: "It's" → cut in close on the card table; the three sit down. "game" → the Politician opens the box and the board flops out (a cream board with a track of colored squares); the players' one piece, a tiny Earth with a worried face (`KIT.props.earthGlobe`, small), hops onto START. "objective" → he holds the lid up to us, "OBJECTIVE: LOSE", and nods, grinning; the camera pushes in on it. "lose," → all three cheer, arms up; the skeleton's jaw clacks. "trying" → the camera eases back; the Weapons Maker kisses his baby missile and hangs it on a string from the lamp, nose down, right over the tiny Earth. "lose" (second) → the skeleton flicks the first domino at the table's edge. "elaborately" → the camera pulls back fast and chases the falling dominoes: off the table, across the rug, up over the sofa, along the mantel, up and down the bookcase and back onto the table, where the last one knocks a lit candle onto a fuse, and the flame runs up the fuse, wound round the lamp's cord, to the missile's string. "possible." → the string burns through and the missile drops onto the tiny Earth: a white flash, a mushroom cloud fills the room, the room shakes. "But" → the smoke clears, the camera back at the table: the Politician and the Weapons Maker sit charred black and smoking, hair straight up, blinking; the tiny Earth is charred too, and blinks; the skeleton, already bones, is fine. "digress." → the skeleton sets the tiny Earth back on START, and the charred Weapons Maker pulls a new baby missile out of the box.

Sound: a thunk as the board flops out; a party whistle on the cheer; a domino clatter on the run; a boom; a pop as the new missile comes out of the box.

On screen: "OBJECTIVE: LOSE" (the lid) and "START" (the board).

No: one kind of contraption: no marbles, seesaws or mousetraps on top of the dominoes, just a very long line of them (the candle and its fuse are the line's last link).

Why: the whole death wish as one picture, and the button is the humans setting it up again.

## Scene 5 · host-digress

- id: host-digress
- act: But I digress
- transition_in: cut
- key: at the very end: the iris closed almost to nothing on Wishonia's side-eye, and the last war paper wedged sideways in the little circle, stick legs braced on one edge and arms on the other, holding it open
- cue: "That's an Earth word"
- time: 14:52.3 to 14:58.0 (5.7 s)
- voiceover: "That's an Earth word I learned. It means continuing after you should have stopped. Like your military spending."
- layer: A, host
- scene: The host's set. Wishonia at the lectern, her coffee mug near the right end of its reading top (a cream diner mug, drawn in the scene). Nothing else on the set: the war papers walk in from off the right edge of the frame.
- wishonia: happy-smile + body-hand-chest; neutral-smile + body-point-right on "continuing"; smirk-closed + body-idle on "stopped." (the sip); sideeye-closed + body-idle on "military"; sideeye-closed + body-palms-down on "spending." (the mug goes down)
- props: studio, mug, money
- status: planned

Moves: "That's" → cut to Wishonia at the lectern, hand on her chest, proud of her Earth word. "continuing" → she points off to the right: war papers (green, missile seals) march in on their stick legs from the right edge of the frame, hop up onto the lectern's reading top and march across it in single file, round her mug and off its left end. "stopped." → the line keeps coming; she lifts her mug and sips. "military" → her eyes slide down to the line over the mug; it speeds up to a jog. "spending." → she sets the mug down slowly, and the next paper marches straight into it, plop, and climbs out the other side dripping coffee and marches on. after "spending." → the film irises out on her face while the papers keep marching across the lectern under it; the last paper jumps up into the closing circle, turns sideways and braces itself across it, legs on one edge and arms on the other, and holds the iris open a crack on her side-eye. The part cuts to black on that.

Sound: a pop as the first paper hops onto the lectern; a patter of little feet as the line speeds up; a small splat as the paper lands in the mug; a squeak as the iris jams on the paper.

On screen: nothing written.

No: no dictionary card; the papers that will not stop are the definition.

Why: the part's last joke lands on the thing the plan fixes: spending that keeps going after it should have stopped, right through the end of the shot.
