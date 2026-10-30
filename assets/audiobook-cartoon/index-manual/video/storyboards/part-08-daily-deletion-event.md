---
format: 1920x1080
duration: 1:12.6
message: "Diseases delete 150,000 humans every day, and every one of those failures is a solvable engineering problem that humans have not made a priority."
arc: Title card (an eraser rubs out a passer-by) → the Grim Reaper's deli counter, NOW SERVING 150,000, EVERY 24 HOURS, where a bribe buys nothing and a bug in the meat software is enough → the same deli's calendar sheds forty days while the queue fills in claim forms to the death, then every page is the eleventh of September and the missile goes for the oil → one reader in his armchair, his appointment waiting next door and the NOW SERVING sign coming down behind his chair → Wishonia fixes him with a wrench on her set and pops the thought that humans would make it a priority
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 8, "The Problem: The Daily Deletion Event"
audio: index-manual.cbaf659d.mp3, 14:58.0 to 16:10.6
version: v3
---

# Part 8 storyboard: "The Problem: The Daily Deletion Event"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("deletion-board: hold the sign longer"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The part is a 1950s atomic-age instructional film. Layer A is the host's studio set (`KIT.studio`): Wishonia large at her navy lectern, in front of the mustard wall and its spotlight pool. Layer B is two illustrated plates the camera travels over (`KIT.camera`), one framing per phrase: the deli (the Grim Reaper's deli counter on an open field, its queue running to the horizon) and the living room (the reader in his armchair, a doctor's office through the wall). Wishonia is not in the plates; she is the voice. Money is green, and its seal says what it buys. Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot. The shared drawings (the NOW SERVING sign, the red ticket, the beetle, the Reaper in his deli cap, the reader and his armchair, the wrench, the sprung kneecap) are in this part's sketch module, `part-08-daily-deletion-event.sketch.mjs`: copy them from there, so every scene draws them the same.

**Spine.** The NOW SERVING sign. It hangs on two chains over the Grim Reaper's deli counter. In deletion-board its flip digits stop on 150,000 and its bottom strip flips to EVERY 24 HOURS; on "software." it clicks to 150,001, and from then on it clicks up one number every 0.576 s (86,400 s a day / 150,000) whenever it is in shot, for the rest of the episode. Its corner stays in the deli's framings of the calendar through holocaust-every-40-days and fifty-nine-elevens, still counting, and on "schedule" in dissolving-on-schedule it comes down on its chains behind the reader's armchair, still counting, where he can't see it. Every human in the part holds one of its red tickets; the reader's is his bookmark.

**Callbacks.** From the theme song and Part 1 (loved-ones): the Grim Reaper (`KIT.reaper`), here in a white paper deli cap. From Part 1 (without-with-papers) and Part 2 (money-loop): the moth from the empty wallet flutters out of the disease blob's turned-out pockets. From Part 2: the Weapons Maker's smiling missile, now on a leash, and the bomb that goes off and leaves a human standing there black and blinking (oil-black this time, and delighted). From Part 2 (host-closes): the guest beside the lectern. Inside the part: the beetle from deletion-board's chest hatch crawls out of the reader's collar in meat-robot and the wrench flattens it; the deli's tear-off calendar has a twin on the doctor's office wall, which shuffles.

**Set up here.** The deli, whole, for countdown-104 (Part 26): the Reaper in his paper deli cap, the NOW SERVING sign, the TAKE A NUMBER dispenser, the DELETED door (`KIT.props.door`, label "DELETED"), the queue of ticket-holders to the horizon. Part 26 reads the sign's count off this part (150,001 on "software." at 910.02 in the MP3, then one every 0.576 s), so draw the deli from deletion-board.html. The reader (the options in the sketch module's `READER`, the manual with its red ticket bookmark, the armchair and the floor lamp) comes back in weirdly-calm (Part 9) and stop-reading (Part 17); record his options at the top of falling-apart.html. The CLAIMS clerk comes back in Part 21 (insurance-zero-claims, greed-arrow): `KIT.person({ tone: 0, outfit: "suit", hair: 2, color: 1, seed: 21 })` (the sketch module's `CLERK`), a green celluloid eyeshade over his brow (`eyeshade(H, R)`), mood "greedy" when the dollar signs ring up; record his options at the top of holocaust-every-40-days.html. The take-a-number queue, its red tickets and the NOW SERVING sign are this part's alone: later parts bring them back only as callbacks to this deli.

**Held frame.** deletion-board, from after "hours" to "bugs". holocaust-every-40-days, from after "days," to "insurance". fifty-nine-elevens, from after "day," to "invades". In each HOLD nothing moves but the NOW SERVING sign's digits (the count does not hold) and nothing sounds. falling-apart and dissolving-on-schedule are the slowest scenes in the episode: slow camera, small moves, quiet sounds.

**Transitions.** The title card comes up from black and goes down to black; deletion-board cuts in from the black on the sign. holocaust-every-40-days and fifty-nine-elevens are the same plate with no seam: the camera keeps traveling from the last framing. Cut from the deli to the living room (falling-apart); dissolving-on-schedule is the same plate with no seam. Cut from the living room to the host's set (meat-robot); thought-incorrect is the same shot with no seam, and it irises out on Wishonia's face to black, so Part 9's title card comes up from black.

**Bans for this part.**
- The narrator makes the Holocaust and 9/11 comparisons; on screen only the calendar carries them, with its pages and stamps.

## Changes from v2

- Wishonia's office, the cream paper and her corner (PiP) are gone. The deli and the living room are two plates the camera travels over, and Wishonia appears only on her set, for the meat robot and the last line.
- The NOW SERVING sign no longer flies into a screen corner: the calendar hangs on the deli's backboard under its edge, so the count keeps running in shot, and the CLAIMS booth and the oil derrick stand on the same field as the queue. The 9/11 calendar pages are "SEP 11 ×50" instead of fifty date tags under a "TODAY" heading.
- The labels went with the paper: no "MEAT SOFTWARE" printout (the beetle chews a punched tape inside a 1950s computer hatch), no "INSURANCE CLAIM" header, no "YOUR SCHEDULE" chalk (the sign comes down behind his chair, face out, where he can't see it), no blueprint tags, no starburst on the title card.
- "which part" is an itch he scratches round his body without looking up, instead of a dotted outline; the sailboat picture that turned into a doctor's office is now the office next door, through a cutaway wall.
- meat-robot is a 1950s product demonstration on the set: the reader stands beside the lectern as the model, his kneecap springs out and his chest smokes, and a wrench lowered on a string from above the frame fixes him. thought-incorrect stays on the set: his thought bubble pops on her fingertip, his kneecap springs out again, and the film irises out on her face.

## Scene 1 · daily-deletion-event-title

- id: daily-deletion-event-title
- act: Title
- transition_in: up from black (the head of a reel)
- key: on "Deletion": the whole heading on the navy card under the emblem, and the giant pencil rubbing out the little woman on top of DELETION, eraser crumbs flying, her handbag left on the letters
- cue: "The Problem. The Daily Deletion Event."
- time: 14:58.0 to 15:01.9 (3.9 s)
- voiceover: "The Problem. The Daily Deletion Event."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem at the top (its three electrons little papers running round their orbits) and the heading under it in Fraunces, cream with a navy drop shadow. Heading lines, 16:9: "THE PROBLEM" (style label) / "THE DAILY" (style small) / "DELETION EVENT"; 9:16: "THE PROBLEM" (label) / "THE DAILY" (small) / "DELETION" / "EVENT". The small gag (`gag`, pinned to the top of DELETION): a little everyday woman in a dress with a handbag on her arm strolls along the top of the word, and a giant pencil (`KIT.pencil`) rubs her out.
- props: title-card, person (a woman with a handbag), pencil, eraser crumbs
- status: planned

Moves: "The" → the card comes up from black (0.35 s) with the whole heading on it, and the camera pushes in slowly for the whole shot; the little woman strolls in along the top of DELETION from its left end, handbag swinging. "Deletion" → a giant pencil swoops down from the top left, eraser first, and rubs her out in three strokes, head to feet, leaving a little heap of eraser crumbs and her handbag on top of the word. "Event." → the pencil lifts away out of the frame, and the handbag tips over. after "Event." → the card goes down to black in its last quarter second.

Sound: a projector whirr from "The"; an eraser scratch on "Deletion"; a pop as the handbag tips over on "Event.".

On screen: "THE PROBLEM" / "THE DAILY" / "DELETION EVENT".

Why: the narrator reads the heading, and the eraser makes "deletion" literal before the number arrives.

## Scene 2 · deletion-board

- id: deletion-board
- act: The daily number
- transition_in: cut (in from the title card's black, on the sign)
- key: on "hours": the NOW SERVING sign on 150,000, its strip flipped to EVERY 24 HOURS, over the deli counter; the Reaper in his paper deli cap with a bony finger on the bell; the fat cat's grinning skeleton (top hat and monocle still on) tipping his hat at the DELETED door; the barrel man in overalls next at the counter, and the queue of ticket-holders running back to the horizon
- cue: "One hundred and fifty thousand"
- time: 15:01.9 to 15:11.4 (9.5 s)
- voiceover: "One hundred and fifty thousand humans permanently stop every twenty-four hours from diseases that are basically just bugs in your meat software."
- layer: B, plate deli
- scene: The deli plate, drawn once (holocaust-every-40-days and fifty-nine-elevens travel over the same plate). An open tan field under a cream sky, the horizon high. On the left, the Grim Reaper's deli stall: a white enamel counter with a navy kick strip, a till and a counter bell on top; behind it the Reaper (`KIT.reaper`) in a white paper deli cap, his scythe leaning on the backboard; the backboard is cream tile under a striped rust-and-cream awning, and a tear-off calendar (`KIT.props.calendar`) hangs on it right of the Reaper. Over the counter, on two chains from the awning, hangs the NOW SERVING sign: a navy enamel box with an orange rule, "NOW SERVING" across its top, six flip digits (mustard on slate tiles) and a cream strip along its bottom. At the counter's left end stands a door in its frame (`KIT.props.door`, label "DELETED"); just past its right end a red TAKE A NUMBER dispenser on a post, and beside it a smug disease blob (`KIT.props.diseaseBlob`) that tears off the tickets and passes them down the line. From the counter the queue (everyday humans facing left, each holding a red ticket) runs right and back across the field to the horizon, smaller and smaller. A little way back along it stands the CLAIMS booth; out on the field to the right, a small oil derrick. Everyone at the counter is drawn at scale 1.6.
- props: reaper, deli counter, till, bell, NOW SERVING sign, calendar, door (DELETED), ticket dispenser, diseaseBlob, ticket, richHuman, money, person (the queue, the barrel man), xray, beetle, computer hatch
- status: planned

Moves: "One" → the cut from black lands on the NOW SERVING sign filling the frame, its flip digits blurring. "One hundred and fifty thousand" → the digits clatter down column by column and clank to a stop on "thousand": 150,000. "humans" → the camera pulls back down the chains: the sign hangs over the deli counter, the Reaper stands behind it in his paper cap, the blob at the dispenser tears off a ticket and passes it down the line, and the queue runs back to the horizon. First in line is the fat cat (`KIT.cast("richHuman")`), his ticket in one hand and a wad of cash in the other. "permanently" → the camera moves in on the counter: the fat cat slides the cash across, and the Reaper rings it into the till. "stop" → then slaps the bell anyway: the fat cat x-rays into a grinning skeleton with his top hat and monocle still on, and strolls out through the DELETED door, tipping his hat; the line shuffles one step forward. "twenty-four hours" → the camera pulls back up to take in the sign: its bottom strip flips over to "EVERY 24 HOURS". HOLD from after "hours" until "bugs": nothing moves. "bugs" → the camera pushes in on the man now at the counter, a barrel of a man in overalls: his chest light blinks red and a hatch in his chest springs open like a 1950s computer panel: three blinking bulbs, two tape reels and a punched paper tape between them, and a fat beetle chewing a hole through the tape. "meat" → chomp: it bites a strip out. "software." → it swallows the strip and burps; the man x-rays into a skeleton, and the Reaper dings the bell. after "software." → the camera pulls back to the counter and the sign: the skeleton strolls out through DELETED, the line shuffles up, and the sign clicks to 150,001. From here it clicks up one number every 0.576 s.

Sound: a typewriter clatter of flip digits on "One"; a clank as they stop, just after "thousand"; a cash-register ding as the Reaper rings up the bribe, just after "permanently"; the counter bell and an x-ray zap on "stop"; a click as the strip flips on "hours"; then silence for the HOLD; a pop as the hatch springs open on "bugs"; a snip for the chomp on "meat"; an x-ray zap and the bell on "software.".

On screen: "NOW SERVING", "150,000" then "150,001", "EVERY 24 HOURS", "TAKE A NUMBER", "DELETED"; nobody's ticket number is readable.

No: no printout or label in the hatch (the beetle in the tape is the bug), and no shop names on the stall.

Why: the size of the daily loss on a sign everyone knows from the deli, with the horror on screen: the line never ends, money does not get you out of it, and one bug in the works is all it takes.

## Scene 3 · holocaust-every-40-days

- id: holocaust-every-40-days
- act: The daily number
- transition_in: same plate (no seam): the camera travels on from deletion-board's last framing
- key: after "part).": the toppled stack of forms beside the CLAIMS booth with one bony hand poking out of it, still signing; the clerk in his green eyeshade, dollar signs in his eyes and his DENIED stamp in hand, a DENIED mark on the top form; the next humans in the queue looking at the heap, tickets in hand
- cue: "That's one Holocaust every forty days"
- time: 15:11.4 to 15:23.0 (11.5 s)
- voiceover: "That's one Holocaust every forty days, except with fewer Nazis and more insurance paperwork (though some would argue the paperwork is worse; at least the Nazis were straightforward about the killing part)."
- layer: B, plate deli
- scene: The same plate. First the tear-off calendar on the backboard right of the Reaper, with the bottom corner of the NOW SERVING sign in the top of the frame, still counting. Then the CLAIMS booth a little way back along the queue: a narrow booth with "CLAIMS" on a sign on its roof and a window with a ledge, the clerk inside (an everyday human in a suit with a green celluloid eyeshade: `CLERK` and `eyeshade` in the sketch module, the drawing Part 21 copies); the queue passes its window, and the woman at that stretch of it (an everyday human in a dress, her chest light blinking red) has to fill in its forms before she can move on.
- props: calendar, reaper, stampMark (40 DAYS), CLAIMS booth, person (the clerk, the woman, the queue), claim forms, pen, xray, stamp (DENIED), stampMark (DENIED)
- status: planned

Moves: "That's" → the camera travels up and right from the counter to the calendar on the backboard; the sign's corner and its ticking digits stay in the top of the frame. "Holocaust" → the Reaper's bony hand tears off the top page, then the next, one a day, faster and faster, until the pages fly off in a stream and pile up on the counter below. "forty days," → page 40 lands on the heap, and a red rubber-stamp mark "40 DAYS" slams onto it. HOLD from after "days," until "insurance": nothing moves but the sign's digits. "insurance" → the camera travels down the queue to the CLAIMS booth: the clerk in his eyeshade, and at his window the woman, ticket in hand, chest light blinking. "paperwork" → he slaps a stack of forms on the ledge. "(though" → she starts filling them in; for every form she hands back, he slaps down two more. "paperwork" (second) → the stack beside her is taller than she is. "worse;" → she x-rays into a grinning skeleton and keeps writing. "straightforward" → the clerk stamps her top form DENIED, and dollar signs ring up in his eyes. after "part)." → the whole stack topples onto her: only a bony hand pokes out of the heap, still signing.

Sound: a flutter of tearing pages on "Holocaust"; a thunk as page 40 lands on "days,"; then silence for the HOLD; a thunk for each stack of forms ("paperwork", "argue", "paperwork" again); a pen scratch on "(though"; an x-ray zap on "worse;"; a rubber-stamp thump and a cash-register ding on "straightforward"; a splat as the stack topples, and one last pen scratch from under it, after "part).".

On screen: "40 DAYS" (the stamp mark), the calendar's dates, "CLAIMS" (the booth's sign), "DENIED" (the stamp mark).

No: no header on the forms.

Why: the daily number in the unit humans call the worst thing that ever happened, then the narrator's paperwork joke played to the end: the window kills her as surely as the counter does, and keeps her filling in forms afterwards.

## Scene 4 · fifty-nine-elevens

- id: fifty-nine-elevens
- act: The daily number
- transition_in: same plate (no seam): the camera travels on from holocaust-every-40-days' last framing
- key: after "oil.": the Weapons Maker in the foreground, oil-black and grinning in a black puddle, holding his upturned hard hat up to catch the oil raining down, the empty leash in his other hand; behind him, past the queue, the mushroom cloud over the little oil derrick and the black gusher shooting up out of it
- cue: "That's also fifty nine-elevens"
- time: 15:23.0 to 15:30.9 (8.0 s)
- voiceover: "That's also fifty nine-elevens every single day, except nobody invades anyone about it because diseases don't have oil."
- layer: B, plate deli
- scene: The same plate. The calendar again; then the front of the queue, where the Weapons Maker (`KIT.cast("weaponsMaker")`, his arms posed for the leash) walks his smiling missile (`KIT.props.missile`) on a leash like a bloodhound, past the disease blob at the TAKE A NUMBER dispenser; then the oil derrick out on the field to the right.
- props: calendar, reaper, stampMark (×50), weaponsMaker, missile, leash, diseaseBlob, moth, oil derrick, nuke, oil gusher
- status: planned

Moves: "That's" → the camera travels back up the queue to the calendar. "also" → the Reaper tears off a page: the one under it is SEP 11. "fifty" → a red stamp mark "×50" slams onto it. "every" → he tears it off: the page under it is SEP 11 ×50 too. "single" → again. "day," → and again. HOLD from after "day," until "invades": nothing moves but the sign's digits. "invades" → the camera comes down to the front of the queue: the Weapons Maker walks in from the right with his smiling missile on a leash, its nose to the ground like a bloodhound, sniffing along the line for something to invade; it gives one woof. "diseases" → it sniffs the disease blob at the dispenser all over. "don't" → the blob turns out its pockets: empty, and a moth flutters out; the missile loses interest at once, its nose swinging up and round to a little oil derrick out on the field past the queue. "have" → it yanks free of the leash and shoots off at the derrick nose first, and the camera pulls back to take in the Weapons Maker and the derrick together. "oil." → it dives into the derrick: BOOM, a white flash, the frame shakes, and a mushroom cloud stands over the derrick. after "oil." → a black gusher shoots up out of the cloud and the oil rains down on the Weapons Maker in the foreground, who stands there holding the empty leash, dripping black from hard hat to boots, only his eyes and his grin showing; he takes off his hard hat and holds it up to catch more.

Sound: a rubber-stamp thump on "fifty"; a paper rip on "every", "single" and "day,"; then silence for the HOLD; a woof from the missile just after "invades"; a sniffing huff on "diseases"; a pop as the pockets turn out on "don't"; a whistle as the missile bolts on "have"; the boom on "oil."; a splat as the oil comes down.

On screen: "SEP 11" and "×50" on the calendar, the sign's count in the corner of the calendar framing.

Why: the same number once more, and why nobody goes to war over it: the missile ignores the disease and goes for what pays.

## Scene 5 · falling-apart

- id: falling-apart
- act: One body
- transition_in: cut
- key: on "sits": the two rooms side by side, cut away like a stage set: on the left the reader in his armchair under the floor lamp, reading the manual, a red ticket for his bookmark and a lost button on the rug; on the right, through the wall, a doctor at his desk gesturing kindly at the empty patient's chair, and a calendar on the office wall
- cue: "Your body is quietly falling apart"
- time: 15:30.9 to 15:46.0 (15.1 s)
- voiceover: "Your body is quietly falling apart. Right now, as you read this sentence, something inside you is breaking. You don't know which part yet. You won't know until a doctor sits you down and says a word that rearranges the rest of your life."
- layer: B, plate living-room
- scene: The living-room plate, drawn once (dissolving-on-schedule travels the same plate). A living room cut away like a stage set, mustard wallpaper and a rust rug: an orange wingback armchair, a floor lamp with a cone shade beside it, and in the chair the reader (`READER` in the sketch module: an everyday human in a shirt and glasses), sitting facing left, reading the manual (`KIT.props.manual`), a red deli ticket for his bookmark. The room's right-hand wall is cut away, and through it is a doctor's office in pale teal: a doctor (an everyday human in a lab coat with a head mirror) behind a wooden desk, facing left, an empty wooden chair across the desk from him, and a tear-off calendar on the wall. Inside the reader's chest, drawn tiny, is the round window into his insides for dissolving-on-schedule. Everyone is drawn at scale 1.6.
- props: person (the reader, the doctor), armchair, floor lamp, manual, ticket, button, desk, chair, folded card, calendar
- status: planned

Moves: "Your" → close on the reader in his armchair under the lamp, reading; the camera starts a very slow push in. "apart." → a button pops off his shirt, drops and rolls under the chair; he does not look up. "read" → he turns a page; his bookmark is a red ticket, like the queue's. "breaking." → his chest light flickers red once; he does not notice. "which part" → still reading, he scratches his knee, then his ribs, then the back of his head. "doctor" → the camera eases back and travels right: the living room's wall is cut away, and on the other side of it is a doctor's office, a doctor at his desk and an empty chair across from him; the reader reads on next door. (9:16: the camera travels on through the wall into the office instead of holding both rooms.) "sits" → the doctor gestures kindly at the empty chair. "word" → he slides a folded card face down across the desk to the empty chair's side. "rearranges" → the calendar on the office wall shuffles its pages out of order, flapping, and settles.

Sound: a tiny tick as the button hits the floor, just after "apart."; a soft page turn on "read"; a soft scratch on "which"; a soft flutter as the calendar shuffles on "rearranges". Nothing else.

On screen: no text.

No: no fast moves; the reader never looks up and the doctor never hurries.

Why: it turns the daily number into the viewer's own body: the appointment is already waiting in the next room.

## Scene 6 · dissolving-on-schedule

- id: dissolving-on-schedule
- act: One body
- transition_in: same plate (no seam): the camera travels on from falling-apart's last framing
- key: on "schedule": the camera eased back wider than before, the reader reading in his armchair under the lamp, and on the wall behind his chair the NOW SERVING sign from the deli on its chains, clicking up past 150,080, his back to it
- cue: "Somewhere in you, right now"
- time: 15:46.0 to 15:58.0 (12.0 s)
- voiceover: "Somewhere in you, right now, cells are copying themselves wrong, proteins are misfolding, tissue is quietly scarring. You are dissolving on a schedule you can't see."
- layer: B, plate living-room
- scene: The same plate: from the office back to the reader, into his chest and out again. Inside his chest, the round window into him: pink-tan tissue, a few round cells with sleepy faces, a long ribbon of protein and a patch of tissue. The NOW SERVING sign (the deli's drawing) hangs on its chains out of shot above the reader's wall until "schedule".
- props: person (the reader), armchair, floor lamp, manual, ticket, cells, protein ribbon, scar patch, NOW SERVING sign
- status: planned

Moves: "Somewhere" → the camera travels back left through the wall and pushes in on the reader, into his chest: his shirt opens onto a round window into his insides. "cells" → one round cell splits in two, and the copy comes out lopsided and cross-eyed, and grins. "proteins" → a ribbon of protein folds and folds itself into a knot. "scarring." → a patch of tissue beside them fills in grey, dot by dot. "dissolving" → the camera eases back out of his chest to the whole room, wider than before. "schedule" → behind the armchair the NOW SERVING sign comes down on its chains from above the frame and stops with a clank, clicking up (150,080, 150,081, ...); its chains shiver at each click. He reads on with his back to it. "can't see" → he turns a page; his ticket bookmark slips, and he tucks it back in without looking.

Sound: a soft pop as the cell splits on "cells"; a small squeak as the protein knots on "proteins"; a soft scratch as the scar fills in on "scarring."; a clank as the sign stops on "schedule", then its digits ticking at the true rate, four ticks to the end of the scene.

On screen: the NOW SERVING sign, its count and its "EVERY 24 HOURS" strip.

No: no labels inside him; no fast moves.

Why: the breaking is happening now, inside, and the count from the deli is running behind his back.

## Scene 7 · meat-robot

- id: meat-robot
- act: Solvable
- transition_in: cut
- key: on "solvable": the reader beside the lectern as the demonstration model, his kneecap sprung out on a coil and a puff of black smoke over his chest, and a teal wrench just lowered on a string from above the frame, swinging over Wishonia's raised palm
- cue: "You're a meat robot"
- time: 15:58.0 to 16:04.7 (6.7 s)
- voiceover: "You're a meat robot with worn-out parts. Every one of these failures is a solvable engineering problem."
- layer: A, host
- scene: The host's set (`KIT.studio`), with a guest on the free wall right of the lectern (where host-closes puts its hungry human): the reader from the living room, standing, facing her, the manual under his arm with its ticket bookmark, his chest light red. A 1950s product demonstration: she presents him like this year's new appliance.
- wishonia: big, happy-smile + body-presenting; excited-ee + body-presenting on "solvable"; smirk-smile + body-hands-hips on "problem."
- props: studio, lectern, person (the reader), manual, ticket, kneecap on a coil, smoke puff, wrench on a string, beetle
- status: planned

Moves: "You're" → cut to the set: Wishonia presents the reader standing beside her lectern; the camera pushes in slowly (1.02 to 1.08). "meat robot" → he gives a stiff little wave, like a showroom robot. "worn-out" → his kneecap springs out on a coil, boing, and wobbles. "parts." → his chest coughs a puff of black smoke like an old jalopy, then another. "Every" → she holds her palm up. "solvable" → a teal wrench drops in on a string from above the frame, like a stagehand's prop, and bobs to a stop over her palm; she plucks it off the string and flips it across to him. "engineering" → it spins at his knee and the kneecap snaps back in; it taps his chest: the smoke stops and his chest light turns teal. "problem." → she puts her hands on her hips. after "problem." → the beetle from the deli crawls out of his collar and down his shirt; the wrench comes down on it: splat.

Sound: a boing on "worn-out"; a huff of smoke on "parts."; a falling slide whistle as the wrench drops in on "solvable"; a clank as it turns on "engineering"; a splat for the beetle after "problem.".

On screen: nothing but the set and the guest.

No: no blueprint, tags or circles; his parts show themselves breaking. The wrench is not conjured on her palm: that trick is the sandwich's in Part 2.

Why: the turn from dread to engineering: broken parts are parts, and parts get fixed.

## Scene 8 · thought-incorrect

- id: thought-incorrect
- act: Solvable
- transition_in: same shot (no seam): it starts on meat-robot's last frame
- key: on "incorrect.": Wishonia pointing, her smirk to the camera, the thought bubble over the reader bursting on her fingertip, PRIORITY 1 scattering in loose letters and the bubble's wrench falling, the reader's kneecap springing out again
- cue: "You'd think humans would prioritize"
- time: 16:04.7 to 16:10.6 (5.9 s)
- voiceover: "You'd think humans would prioritize solving these problems. That thought would be incorrect."
- layer: A, host
- scene: The same set and guest, fixed and beaming, the flattened beetle on the floor. A thought bubble rises over his head, toward her.
- wishonia: big, lookright-smile + body-idle; skeptical-closed + body-idle on "That"; smirk-closed + body-point-right on "incorrect."
- props: studio, lectern, person (the reader), thought bubble, wrench
- status: planned

Moves: "You'd" → the first frame is meat-robot's last. "think" → a thought bubble floats up from his head and drifts toward her, a teal wrench drawn in it. "prioritize" → "PRIORITY 1" writes itself into the bubble and the bubble swells. "problems." → it swells bigger and shines; he smiles up at it. "That" → Wishonia raises an eyebrow at the camera. "incorrect." → she points at the bubble and it pops on her fingertip: "PRIORITY 1" scatters into loose letters, and the wrench in it drops and clanks on the floor. after "incorrect." → the letters rain down on him, and his kneecap springs back out on its coil. Then (about half a second after "incorrect." ends) the film irises out on her face, to black.

Sound: a slide whistle up as the bubble rises on "think"; a marker squeak for "PRIORITY 1" on "prioritize"; a sparkle as it shines on "problems."; a pop on "incorrect.", a clank as the wrench lands just after it, and a boing as the kneecap springs back out.

On screen: "PRIORITY 1" in the bubble.

Why: the hinge into the next part: the fix is possible, and humans have not made it a priority.
