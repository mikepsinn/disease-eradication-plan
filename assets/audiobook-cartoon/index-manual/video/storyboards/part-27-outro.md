---
format: 1920x1080
duration: 0:59.8
message: "Too busy to end war and disease? Share the episode, leave a good review, or take 15 seconds to vote at warondisease.org."
arc: Wishonia files Earth and thanks a viewer who falls asleep → his glowing rectangle hands the job to a friend in a deckchair under a sprinkler → six stars carry the pro-war robot off over the horizon like a rug and find Grandma, who has had spare time since 1987 → the review clerk stamps anything without looking → charred YOU drags the money from the bomb to the lab → one YES button gets him a WANTED poster → the address, a wink, and the iris closes the film
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 27, "Outro"
audio: index-manual.cbaf659d.mp3, 56:53.5 to 57:53.3
version: v3
---

# Part 27 storyboard: "Outro"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The film look of Part 2 (`../compositions/scenes/part-02/`): Layer A is the host at her lectern (`KIT.studio`), Layer B is an illustrated plate the camera travels over (`KIT.camera`), one framing per phrase, and the period film runs over every shot. Wishonia is on screen only at her lectern; in the plate she is the voice. Money is green: the bills that feed the bomb have missile seals, and the ones that come out of the color-flip funnel have cross seals. The narrator reads no heading here, so the part has no title card.

**Spine.** "Too busy", three times, and each time the ask gets smaller: YOU's glowing rectangle shrinks a size with a slide whistle, from a tray he holds in both hands to a phone to a matchbox, and on "And vote!" to nothing. Meanwhile YOU gets busier: asleep (and thanked anyway), buried in calendar pages, running on the spot, on fire, charred. Each smaller ask gets a bigger payoff on the field: one free afternoon ends war and disease from a deckchair; six stars carry the pro-war robot off over the horizon like a rug; one slider walks the money from the bomb to the lab; one YES button puts YOU on a WANTED poster.

**YOU.** The viewer is the busy human in the bowler from Part 1's title card (`{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene, so he is the same man), with his wristwatch. Since Part 26's countdown-104 his legs are bone from the waist down, and they stay bone to the end of the film: they clatter when he runs. He stands beside the gift where Part 26 leaves him and sinks into an armchair to sleep in thank-you, works the field in the four plate scenes, and runs back into the studio, still charred and smoking, in love-you-bye. From "least" in wishocratic-slider to the end of the film he is charred black above the waist, hair straight up, smoking, only his eyes blinking (`charred: true`), and his bowler rides on top of the spikes; his bone legs come out of the fire bone white, and the rectangle in his hand comes through untouched.

**The cast.** The friend is an everyday woman in a dress (`{ tone: 3, outfit: "dress", hair: 1, color: 2 }`). The review clerk is an everyday human in a shirt (`{ tone: 0, outfit: "shirt", color: 1 }`). The pro-war robot is `KIT.props.robot` in war red with an army helmet on its box head and a little missile painted on its chest. The grumpy missile is `KIT.props.missile`, the disease is `KIT.props.diseaseBlob`, Grandma is `KIT.cast("grandma", { skeleton: true })` with her poster, and the 2.6 humans are everyday humans whose builds come from their outfits.

**Shared drawings** (the group named draws each one first as a function the others copy, so they match):
- **The glowing rectangle.** A slate slab with rounded corners, two little 1950s TV knobs under the screen and a pale cyan screen that lights what is in front of it. Three sizes: a tray held in both hands (about 70 x 50 person units), a phone (36 x 26), a matchbox (16 x 12). Its screens: a cream SHARE button with a drawn share mark; five empty stars; the address page "warondisease.org". Drawn first by the share-and-review group.
- **The busy-field plate** (see glowing-rectangle-share's scene line), drawn first by the share-and-review group (glowing-rectangle-share, really-good-review); the slider-and-vote group (wishocratic-slider, personally-to-blame) copies its drawing code and its views. The friend's lawn, deckchair and sprinkler are on it (`lawn`, `deckchair`, `sprinkler` in the sketch module).
- **YOU's bone legs.** Part 26's `bonyYou`: the person clipped above the hips over the skeleton's legs, with knobbly knees. `part-27-outro.sketch.mjs` (`bonyYOU`) draws them in any leg pose, seated and running too.
- **Charred YOU.** `KIT.person` with `charred: true` drops the hat and blows the hair straight up, so draw the bowler (kit.js `hatSvg` "bowler") on top of the spikes, at about (5, -107) in person units, tipped a few degrees; below the waist the bone legs stay bone white. `part-27-outro.sketch.mjs` (`charredYOU`) draws it.
- **Grandma's poster.** The skeleton drops her held props, so draw the poster in her raised hand: the kit's "poster" card, BUY BONDS on the front, a teal cross and TRIALS on the back (`poster` in the sketch module).
- **YOU's armchair**: the rust wingback of Part 8's reader, as `../compositions/scenes/part-08/dissolving-on-schedule.html` draws it (`chairBack`, `chairFront`, the seated `legPose`).
- **The lectern as Part 26 leaves it**: the case file, its stamp and the mug (part-26's sketch module: `caseFile(H, 3)`, `mug`), and the gift-wrapped Earth on its pedestal (eligible-final-stamp). **The PLANETS out-tray** with "VENUS: TOO HOT" and "MARS: NOBODY HOME", as Part 1's eligible draws it.

**Callbacks.** From Part 26 (eligible-final-stamp): its last frame, the case file "~~EARTH~~ DIRT: CASE #847" stamped "~~MAY BE~~ ELIGIBLE FOR OPTIMIZATION" on the lectern (style bible, gag 4), the mug, and YOU on his bone legs beside the gift-wrapped Earth; the file hops into the PLANETS out-tray from eligible (Part 1), on top of VENUS: TOO HOT and MARS: NOBODY HOME, and the gift rolls away unclaimed. From Part 26 (countdown-104): YOU's bone legs, and "2.6 lives" and "468,000 hours" from the Reaper's refund receipt. From Part 1's title card: the busy runner in the bowler, eyes on his wristwatch, who runs to the address at the end. From Part 8: the reader's rust wingback armchair, now with YOU asleep in it under the open manual. From Part 17 (grandmas-war-bond): Grandma's grinning skeleton, her BUY BONDS poster and her headstone "1987"; she still died of cancer, so she has had nothing but spare time. From Part 25 (dont-know-what-to-tell-you): the YES button, now the size of a fire hydrant. From Part 1 (split-the-atom) and the Optimitron: things pop out like toast (the slider, the treaty). The seal flip in the color-flip funnel (style bible, gag 2). The iris (style bible, gag 6): the film closes on her face.

**Set up here.** Nothing: this is the last part.

**Held frame.** None. No death toll is spoken in this part.

**Transitions.** thank-you starts on Part 26's eligible-final-stamp last frame (a cut, since the parts are rendered on their own and joined). Cuts between host shots and the plate. really-good-review continues glowing-rectangle-share's plate, and personally-to-blame continues wishocratic-slider's, each with no seam (it starts on the last scene's final frame). wishocratic-slider cuts back to the plate at YOU. love-you-bye irises out on her face to black: the end of the film.

**Bans for this part.**
- The glowing rectangle, its share mark, its stars and its address page are drawn, not a real phone, app or store screen.
- YOU's options, his bone legs and the rectangle's sizes match in every scene.

## Changes from v2

- The office, the wall screen and Wishonia's corner are gone. She is on screen in three host shots: thanking YOU while he sleeps beside her lectern (thank-you), the REVIEW CHECKING booth (they-dont-check) and the goodbye (love-you-bye). Everything YOU does happens on one plate, busy-field, where the camera travels from his desk to a deckchair on a lawn, the horizon and Grandma's headstone, and back.
- thank-you opens on Part 26's last frame: the file hops from the lectern into the PLANETS tray, the gift Earth rolls away, and YOU sinks into his armchair on the bone legs Part 26 gave him, which he keeps to the end.
- The glowing rectangle is in YOU's hands, not on the wall screen, and still shrinks on each "too busy". The GLOWING RECTANGLE museum label and its arrow are gone: its light turns his face cyan and his eyes go to spirals instead.
- The juggling became running on the spot, so the fire has a cause: his bone feet smoke, he burns, he is charred. The rectangle comes through the fire untouched, and his wristwatch melts off his wrist.
- The stars hop out of the rectangle on stick legs, and the pro-war robot sits on them like a park bench before they carry it off over the horizon like a rug; its ALGORITHM stencil became an army helmet and a missile on its chest. The REVIEW CHECKING booth moved into a host shot, where the joke is told to the camera, and it is open: its clerk stamps CHECKED on every review without looking.
- The slider has no words on it: a bomb on a pile of war money at one end, a lab at the other, the color-flip funnel between, and Grandma's skeleton running the trials. The rectangle's last shrink leaves nothing, and the vote is a YES button as big as a fire hydrant.
- The end card on the wall screen became a WARONDISEASE.ORG sign that drops into the studio on its wires, and the film ends on the iris closing on her wink.

## Scene 1 · thank-you

- id: thank-you
- act: The asks
- transition_in: cut (the parts are rendered on their own and joined); the first frame is Part 26's eligible-final-stamp last frame: Wishonia side-eyeing the camera, the stamp just lifted off the case file on the lectern, the mug, and on the free wall YOU on his bone legs, chin in hand, beside the gift-wrapped Earth on its pedestal, a puff of saucer exhaust over them
- key: after "time": Wishonia beams and presents, with both hands, YOU asleep on his bone legs in his rust wingback armchair beside the lectern, the open manual over his face lifted on a snore; the stamped case file on top of VENUS and MARS in the PLANETS tray, the gift's pedestal empty
- cue: "Thank you so much"
- time: 56:53.5 to 57:01.3 (7.8 s)
- voiceover: "Thank you so much for taking the time to end war and disease, but if at any point you decide you're too busy,"
- layer: A, host
- scene: The host's set as Part 26's eligible-final-stamp leaves it: on the lectern the case file "~~EARTH~~ DIRT: CASE #847" (SUBOPTIMAL and "~~MAY BE~~ ELIGIBLE FOR OPTIMIZATION" on it), its rubber stamp and the mug; on the free wall right of the lectern the gift-wrapped Earth on its pedestal (the bow, the TO: HUMANS tag) and YOU on his bone legs, chin in hand. Part 1's wire out-tray "PLANETS", with "VENUS: TOO HOT" and "MARS: NOBODY HOME" in it, comes onto the lectern's far end (screen left), and YOU's armchair (Part 8's reader's rust wingback, on casters) rolls in from the right.
- wishonia: big, happy-open + body-wide-gesture; happy-smile + body-presenting on "time"; skeptical-smile + body-hands-hips on "busy,"
- props: studio, lectern, case-file, stamp, mug, out-tray, pedestal, earth-globe, gift-bow, price-tag, armchair, manual, YOU (bone legs)
- status: planned

Moves: "Thank" → she puts the stamp down, turns from the side-eye to a beam and spreads her arms wide; the saucer's puff of exhaust drifts off, and the camera pushes in slowly for the whole shot. "so" → the case file hops up off the lectern; "much" → the PLANETS tray slides in under it, and it drops flat into the tray on top of VENUS and MARS. "taking" → the gift Earth rolls off its pedestal, bounces once and trundles out of the frame, its TO: HUMANS tag flapping; nobody looks. "time" → YOU, still lost in thought, sits back on nothing; his armchair rolls in under him from the right just in time, with the manual riding on its arm, and he lands in it with a clatter of bone; the manual flops open over his face, and he is asleep. She presents him with both hands, proud. "end" → a snore lifts the manual off his face and it flops back, and a snore bubble swells out of his nose under it. after "disease," → a bigger snore: the manual flaps like a bird and settles. "decide" → he jolts awake, the manual flies up, and he checks his wristwatch. "busy," → he sprints off the set to the right, out of the chair so fast his bowler hangs in the air for a beat, his bone legs clattering; after "busy," a hand reaches back into the frame and grabs it. She puts her hands on her hips.

Sound: a whoosh as the file drops into the tray ("much"); a thunk as the Earth hits the floor ("taking"); a squeak of casters as the chair rolls in ("time"); a huff for the snore ("end"); a boing as he jolts awake ("decide"); a whistle and a clatter of bone as he sprints off ("busy,").

On screen: "PLANETS" / "VENUS: TOO HOT" / "MARS: NOBODY HOME" / "~~EARTH~~ DIRT: CASE #847" / "ELIGIBLE FOR OPTIMIZATION" (on the file) / "TO: HUMANS" (the tag, as the gift rolls off).

No: no easel; the file goes from the lectern straight into the tray.

Why: she thanks the viewer for his time while he sleeps through it, the gift nobody takes rolls away on "taking", and the first "too busy" sends him running.

## Scene 2 · glowing-rectangle-share

- id: glowing-rectangle-share
- act: The asks
- transition_in: cut
- key: on "war": the friend springs up out of her deckchair on the lawn, beside the FREE AFTERNOON sign, and karate-chops the grumpy missile in half, her lemonade level in her other hand, both halves dropping, surprised, into the sprinkler's spray, the disease blob creeping up behind the deckchair
- cue: "please press the share button"
- time: 57:01.3 to 57:08.6 (7.3 s)
- voiceover: "please press the share button on your glowing rectangle in case one of your friends have a free afternoon to end war and disease instead."
- layer: B, plate busy-field
- scene: One plate, a wide open field: a cream sky over plain tan ground, the horizon high (plate y -520), the near ground where everyone stands at y 0, everyone drawn at scale 1.5. Left (x -900): YOU's desk, a slate 1950s office desk standing alone in the field, with a big tear-off calendar (`KIT.props.calendar`) and an in-tray piled with paper on it; YOU's spot is just right of it (x -700). Middle (x -500 to 600): open ground, where the stars line up in really-good-review and the slider lands in wishocratic-slider. Right (x 1400): a round patch of green lawn on the tan ground, a striped canvas deckchair on it, the friend lounging in it with a tall glass of lemonade and her own little rectangle in her lap, an oscillating lawn sprinkler beside her ticking a fan of water back and forth over her, and a little garden sign on a stake in the lawn, "FREE AFTERNOON". Far right (x 2100, mid-ground): a small headstone, "1987", with Grandma's skeleton sitting on it. The camera starts at the desk and chases the share across to the lawn.
- props: desk, calendar, glowing-rectangle, YOU, lawn, deckchair, sprinkler, sign, person (the friend), lemonade, missile, diseaseBlob
- status: planned

Moves: "please" → framing on the desk: YOU skids in from the left to his spot beside it. "press" → the calendar's pages tear themselves off, faster and faster, a blizzard that buries him to the chin by "button". "share" → his glowing rectangle (the tray size) pops up out of the pile in both hands, a SHARE button on its screen. after "rectangle" → the camera pushes in on his face: the rectangle's light turns it cyan, his eyes go to spirals and his mouth hangs open. "friends" → his thumb presses SHARE: a zigzag bolt shoots out of the rectangle to the right, and the camera chases it across the field. "afternoon" → it lands on the lawn: the friend's own little rectangle dings in her lap, the sprinkler's spray ticking over her. "end" → a grumpy missile flies in from the right, nose first, on its flame. "war" → she springs up out of the deckchair and karate-chops it in half, holding her lemonade level in the other hand; both halves drop, surprised, and the sprinkler's spray sweeps over them and puts their flames out. "disease" → a disease blob creeping up behind the deckchair: she stomps it flat as a rug. "instead." → she flops back into the deckchair, which folds up on her like a clam; her hand comes out between the slats with the lemonade still level, and she sips.

Sound: a whoosh of pages on "press"; a pop as the rectangle comes up on "share"; a zap as the share shoots out on "friends"; a ding from her rectangle on "afternoon"; a whistle as the missile flies in on "end"; a clank as it is chopped on "war"; a splat on "disease"; a thunk as the deckchair folds up on "instead.".

On screen: "SHARE" (the button) / "FREE AFTERNOON" (the garden sign).

Why: the first and biggest ask, and one free afternoon is enough to end war and disease.

## Scene 3 · really-good-review

- id: really-good-review
- act: The asks
- transition_in: same plate (no seam)
- key: after "suppression": the six stars standing up together under the tin robot and carrying it off on their little legs like a rug, scurrying right, YOU running on the spot behind them with his phone-sized rectangle held out
- cue: "And if you're too busy"
- time: 57:08.6 to 57:21.2 (12.6 s)
- voiceover: "And if you're too busy to even do that, please leave a really, really, really good rating and review so we overcome the pro -war algorithmic suppression and find someone with more spare time for ending wars and diseases."
- layer: B, plate busy-field
- scene: The busy-field plate as glowing-rectangle-share left it: YOU buried to the chin in calendar pages at his desk, the friend folded up in her deckchair on the lawn. The robot comes in from the right; the stars come out of the rectangle; Grandma waits on her headstone at the far right.
- props: glowing-rectangle, YOU, calendar pages, stars on legs, robot, nuke, headstone, grandma (skeleton), sign (her poster)
- status: planned

Moves: "And" → the camera travels back left from the lawn to YOU, still buried to the chin, glazed. "busy" → his rectangle shrinks a size, to a phone, and its screen flips to five empty stars. "that," → he bursts up out of the page pile and starts running on the spot, his bone legs a blur wheel, the rectangle held out in front of him, checking his wristwatch every few steps. "really," (first) → a fat mustard star pops up out of the rectangle and lands on the ground in front of him on stick legs, cheering. "really," (second) → a second. "really" (third) → a third. "good" → a fourth and a fifth together. "rating" → a sixth star elbows into the row and shoves the others along. "overcome" → the camera pulls back a little: the tin robot stomps in from the right in its army helmet, the missile on its chest. "pro-war" → it plonks down on the row of stars like a park bench. "algorithmic" → the stars go dim and flat under it, legs kicking; it folds its arms, smug. after "suppression" → the six stars flare, stand up together under it and carry it off on their little legs like a rug, scurrying right, the robot flailing on its back. "find" → the camera pulls back and pans right after them as they scurry off across the field toward the horizon. "someone" → far beyond the lawn they tip it off over the horizon: a white flash and a little mushroom cloud, and the stars scatter. The camera keeps traveling right along the field, past the friend's folded deckchair, the sprinkler still ticking over it, to "spare time" → Grandma's grinning skeleton sitting on her headstone, "1987", in her curlers and cat-eye glasses, legs crossed, her BUY BONDS poster in her lap, a cobweb from her elbow to the stone. "ending wars" → she flips her poster over: the back reads TRIALS, with a cross. "diseases." → she hops down and marches off to the left, poster high.

Sound: a slide whistle down as the rectangle shrinks on "busy"; a clatter of running bone feet on "that,"; a pop per star (the fourth and fifth share one), a squeak for the sixth on "rating"; a clank as the robot stomps in on "overcome"; a slam as it sits on "pro-war"; a patter of little feet as the stars carry it off, after "suppression"; a boom where it lands on "someone"; a whoosh as the poster flips on "ending".

On screen: the stars (drawn) / "1987" / "BUY BONDS", then "TRIALS".

No: no app-store page and no word on the robot; the helmet and the missile on its chest say whose side it is on. No catapult or fling: the stars carry it off on foot (Part 12's 3389-to-1 has the one fling out of the top of the frame).

Why: the second, smaller ask; the review beats the pro-war algorithm and reaches someone with time on her hands.

## Scene 4 · they-dont-check

- id: they-dont-check
- act: The asks
- transition_in: cut
- key: on "check.": Wishonia side-eyes the camera; beside the lectern the REVIEW CHECKING booth stands open, its clerk turned away on the telephone, laughing, his arm reaching back out of the window and his stamp lifting off a review card with so many stars they run off both ends: CHECKED, on top of two more CHECKED cards
- cue: "The good review doesn't have to be true"
- time: 57:21.2 to 57:24.0 (2.7 s)
- voiceover: "The good review doesn't have to be true, they don't check."
- layer: A, host
- scene: The host's set, the PLANETS tray on the lectern's far end (the case file "~~EARTH~~ DIRT: CASE #847" filed in it, as thank-you left it) and the mug on its near end. On the free wall right of the lectern, a little 1950s booth (a cream box with a rust roof and a counter window), "REVIEW CHECKING" over the window, its shutter rolled up. Inside, the clerk sits turned away from the window, chatting on a desk telephone (`KIT.props.phone`), his back arm reaching out over the ledge with a rubber stamp (`KIT.props.stamp`, "CHECKED"). On the ledge, review cards (cream cards with a row of mustard stars) slide in under his stamp one at a time.
- wishonia: big, smirk-smile + body-palms-down; sideeye-closed + body-palms-down on "check."
- props: studio, lectern, out-tray, mug, booth, person (the clerk), phone, stamp, stampMark, review cards
- status: planned

Moves: "The" → cut to the lectern: she stands palms down, smirking; beside her the booth is open, its clerk on the phone, turned away from the window, a review card sliding onto the ledge under his stamp. "true," → she leans in to the camera; without turning round, the clerk thumps CHECKED onto the card, and the next slides in. "they" → thump: CHECKED. "check." → the third card has so many stars they run off both ends of it: thump, CHECKED. She side-eyes the camera; the clerk laughs into the phone.

Sound: a rubber-stamp thunk on "true,", on "they" and on "check.".

On screen: "REVIEW CHECKING" / the stars on the cards / "CHECKED".

No: no push and no iris; it is a short cut.

Why: a joke told to the viewer, so it is hers to tell; the booth is open, and its clerk stamps anything put under his hand, even a review that cannot be true.

## Scene 5 · wishocratic-slider

- id: wishocratic-slider
- act: The asks
- transition_in: cut (back to the busy-field plate, at YOU)
- key: the scene's last frame, just after "trials.": the whole slider across the field, charred YOU at its knob dragged right, medicine-seal bills piled at the lab bench with Grandma's skeleton waving TRIALS beside it, the empty bomb at the left end with a little BANG flag poking out, the flattened robot's antenna bulb blinking under the track's end
- cue: "But if you're too busy"
- time: 57:24.0 to 57:39.4 (15.4 s)
- voiceover: "But if you're too busy to even do that, the absolute least you could do is take 15 seconds to go to WarOnDisease.org and make your wishocratic allocation, telling us what fraction of humanity's resources should go to explosions versus clinical trials."
- layer: B, plate busy-field
- scene: The busy-field plate: YOU at his desk, running on the spot (the stars have scattered after the robot). The slider, when it lands, lies across the middle ground from x -560 to 450, just in front of the people line: a long cream track on two short feet with a navy knob at its left end, at a standing person's hand height; under the left end a pile of war-seal bills with a lit bomb (`KIT.props.bomb`) on top; the color-flip funnel (`KIT.props.colorFlipFunnel`) behind its middle; a lab bench (`KIT.props.lab`, x 760) past its right end, where the medicine bills pile up.
- props: glowing-rectangle, YOU (charred), flames, wristwatch, slider, money (war, med), bomb, colorFlipFunnel, lab, grandma (skeleton), robot (charred)
- status: planned

Moves: "But" → back on the field: YOU running on the spot at his desk. "busy" → his rectangle shrinks again, to a matchbox. "even" → his bone feet start to smoke. "do" (first) → he bursts into flames all over and runs in circles, still holding the rectangle out, still checking his watch. "least" → the flames go out in a puff: he stands still, charred black, hair straight up, smoking, only his eyes blinking, on bone legs still bone white; the matchbox rectangle in his hand is untouched and still glows. "15 seconds" → he checks his wristwatch: it has melted and droops off his wrist. "WarOnDisease.org" → the camera pushes all the way in on the tiny rectangle until it fills the frame, and "warondisease.org" types onto its screen. "wishocratic" → a slider pops up out of it like toast, and the camera pulls back after it as it spins up. "allocation," → it lands across the field in front of him with a thunk, and its right end comes down on the tin robot, charred and smoking, limping back in from the horizon: flattened, only its antenna bulb poking out, blinking. "humanity's" → framing on the left end: the war bills hop up into the bomb one after another. "resources" → it swells, and its fuse fizzes. "explosions" → YOU's charred hand grabs the knob. "versus" → the camera pulls back to the whole slider as he drags the knob right, walking along behind it, all the way to the lab end. "clinical" → the bills march back out of the bomb and through the funnel, coming out with crosses where the missiles were, and the bomb shrinks as they leave. "trials." → they pile up at the lab bench, the flask bubbles over, and Grandma's skeleton marches in beside the bench and waves her TRIALS poster overhead; a quarter second later, before the cut, the empty bomb sputters and a little BANG flag pokes out of it on a stick.

Sound: a slide whistle down for the shrink on "busy"; a whoosh of fire on "do"; a yelp as he runs in circles on "that,"; a sizzle as the fire goes out on "least"; typewriter clacks for the address on "WarOnDisease.org"; a toaster pop on "wishocratic"; a thunk as the slider lands on "allocation,"; a fizz-tick from the fuse on "resources"; a slide whistle up as he drags on "versus"; a cash-register ding as the medicine pile lands on "trials."; a pop for the BANG flag 0.3 s into "trials." (after "trials." would fall past the cut).

On screen: "warondisease.org" (on the rectangle) / "BANG" (the flag) / "TRIALS" (Grandma's poster).

No: no words on the slider and no percentages; the bomb and the lab are its ends.

Why: the smallest ask is 15 seconds, and the episode's seal flip done by the viewer's own charred hand.

## Scene 6 · personally-to-blame

- id: personally-to-blame
- act: The vote
- transition_in: same plate (no seam)
- key: after "468,000": in the spotlight, charred YOU beside the giant YES button, the stamped treaty on it, under a WANTED poster with his charred mugshot, "2.6 LIVES" and "468,000 HOURS" on it, and two whole humans and a third only 60% drawn waving from behind the medicine pile at the lab
- cue: "And vote"
- time: 57:39.4 to 57:49.2 (9.8 s)
- voiceover: "And vote! If the 1% treaty passes, your vote will be personally to blame for saving 2.6 lives and preventing 468,000 hours of suffering."
- layer: B, plate busy-field
- scene: The busy-field plate as wishocratic-slider left it, at the slider's lab end: YOU at the knob, the medicine pile and the lab bench to his right. The YES button (`KIT.props.yesButton`, "YES", at the size of a fire hydrant) comes up out of the ground just right of him; the WANTED poster unrolls out of the sky behind him.
- props: glowing-rectangle, YOU (charred), yesButton, scroll, stamp, stampMark, spotlight, wanted-poster, person (the 2.6 humans), pencil
- status: planned

Moves: "And" → the camera pushes back in on YOU at the knob, and the matchbox rectangle shrinks to a speck and vanishes with a pop. "vote!" → a YES button the size of a fire hydrant pops up out of the ground beside him; he pokes it with one charred finger and its cap clunks down. "treaty" → a little scroll, "1% TREATY", pops up out of the button like toast. "passes," → a rubber stamp drops in from above the frame and thumps PASSED onto it in teal. "personally" → the field goes dark, and a police spotlight snaps on and swings onto YOU. "blame" → the camera pulls back as a WANTED poster unrolls down out of the sky behind him: WANTED, over his charred mugshot (hair straight up, the bowler riding on top, smoking) against a height chart. "2.6 lives" → "2.6 LIVES" types onto the poster under the mugshot, and three humans pop up from behind the medicine pile and wave: two whole ones and a third who is only 60% drawn, inked from the shoes to the chest and the rest a dashed pencil outline, the pencil still hovering beside him. "468,000 hours" → "468,000 HOURS" types on under it. "suffering." → the mugshot winks; under it, YOU blinks.

Sound: a slide whistle down and a pop as the rectangle vanishes on "And"; a click as he presses YES on "vote!"; a toaster pop on "treaty"; a rubber-stamp thunk on "passes,"; a switch for the spotlight on "personally"; a slam as the poster unrolls on "blame"; three pops for the humans on "2.6", the third at 60% volume; typewriter clacks on "468,000"; a ding on the wink on "suffering.".

On screen: "YES" / "1% TREATY" / "PASSED" / "WANTED" / "2.6 LIVES" / "468,000 HOURS".

No: no police badge or agency seal, and no more words on the poster than these.

Why: the vote, framed as a crime the viewer gets blamed for, and 2.6 lives drawn as 2.6 people.

## Scene 7 · love-you-bye

- id: love-you-bye
- act: Goodbye
- transition_in: cut
- key: on "Love": Wishonia winks with her arms wide; on the wall beside the lectern the WARONDISEASE.ORG sign hangs on its wires, and charred YOU stands under it tipping his bowler, smoke curling off him
- cue: "Go to WarOnDisease.org right now"
- time: 57:49.2 to 57:53.3 (4.1 s)
- voiceover: "Go to WarOnDisease.org right now. Love you, bye!"
- layer: A, host
- scene: The host's set, the PLANETS tray on the lectern's far end (the case file "~~EARTH~~ DIRT: CASE #847" filed in it) and the mug on its near end. A period sign (navy, a cream rule round its edge, the address in big cream Fraunces) drops in on two wires onto the free wall right of the lectern.
- wishonia: big, happy-smile + body-counting; blink-smile + body-wide-gesture on "Love"
- props: studio, lectern, out-tray, mug, sign, YOU (charred, bone legs)
- status: planned

Moves: "Go" → back at the lectern; the sign drops in on its wires and bounces to a stop: "WARONDISEASE.ORG". She raises one finger. "now." → charred YOU sprints in from the left behind the lectern, bone legs clattering, eyes on his melted watch, the runner from Part 1's title card, skids to a stop under the sign and tips his bowler; smoke curls off him. "Love" → she winks and spreads her arms. "bye!" → the iris closes on her face, to black: the end of the film.

Sound: a thunk as the sign lands on "Go"; a whistle and a clatter of bone under the runner on "now."; a sparkle on "bye!".

On screen: "WARONDISEASE.ORG".

No: no credits on the set (only half a second of audio follows "bye!"; an end card after the iris is the edit's call).

Why: the address one last time, and the film closes on her face as it opened on it.
