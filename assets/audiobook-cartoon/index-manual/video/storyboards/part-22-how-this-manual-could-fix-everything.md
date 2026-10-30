---
format: 1920x1080
duration: 0:49.3
message: "The manual is built for humans as they are: pictures, simple math, exact amounts and the order to pay them, legal names for bribes, an appliance that rates policies, and templates for tricking politicians into saving lives."
arc: Title card (the wrench fixes EVERYTHING, crooked) → at the lectern the manual lands and opens like a tackle box → inside it, one plate up a stair of trays: the patient dies reading the fine print and his skeleton enjoys the picture book, the Calculator screams at a ×, the Lobbyist's fingers get flattened, the order tray blows up → down the bottom drawer: the Lobbyist labeled NOT A BRIBE, the Optimitron spits out MORE WAR and pops CURE IT into a sobbing chin, the Politician trapped into being a hero → the dysfunction engine: the treadmill pays the Rich Human a paper a turn into his upturned top hat, so he sprints, and he burns PLEASE BE GOOD for his cigar → back at the lectern: the self-help book onto a heap of its copies, the manual slammed shut, one paper held up like a treat, the Reaper's scythe wilts
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 22, "How This Manual Could Fix Everything"
audio: index-manual.cbaf659d.mp3, 47:23.7 to 48:13.0
version: v3
---

# Part 22 storyboard: "How This Manual Could Fix Everything"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("manual-toolbox: hold the skeleton longer"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The part is a 1950s atomic-age instructional film. Layer A is the host's studio set (`KIT.studio`): Wishonia large at her navy lectern, her coffee mug on the left end of its reading top (drawn as Part 16 draws it). Layer B is two illustrated plates the camera travels over (`KIT.camera`), one framing per phrase: tackle-box (the inside of the manual) and dysfunction-engine; Wishonia is not in them, she is the voice. Money is green: every paper in this part is medicine money (`KIT.money("med")`, a cross seal), except the plain papers leaking from the Lobbyist's briefcase (`KIT.money("plain")`). Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Spine.** The manual as a tackle box. In manual-contains the book (`KIT.props.manual`, the theme song's orange cover) drops onto the right end of the lectern and springs open on a little stair of trays. The cut on "Pictures" goes inside it: on the tackle-box plate the manual is a building-sized box on a plain field, its four trays climbing out of it in a stair up to the right, one item per tray, and in not-a-bribe-label-maker its bottom drawer shoots out along the ground under them, long as a shelf, with the last three tools. In bribe-humanity it is back on the lectern, small, with the drawer's cast hanging out of its pages, and it slams shut.

**Build: the tackle-box plate** (manual-toolbox and not-a-bribe-label-maker, two author groups, so both draw it to these numbers). Plate units; the ground at y 0; every person at scale 1.5, feet on its floor.
- The field: a cream sky (`#EFE6C8`) over a tan ground (`#C8B07B`) from y 0 down.
- The manual: `KIT.props.manual({ size: 7 })` standing at (-1200, 0), about 690 wide and 870 tall, its cover swung back past the spine (`.manual-cover` at scaleX -0.35 about (-42, -59), its title text hidden, since the inside of a cover is plain orange) and a few lines of print on its first page; the trays climb out of the top of the page block. The small manual on the lectern opens the same way.
- Tray k (1 to 4): an open tray 760 wide, its left edge at x -820 + 800(k - 1), its floor at y -520 - 200(k - 1): an orange front panel 90 tall (the cover's orange, a navy outline, a cream rule along its top edge) in front of a cream back wall 150 tall. Actors stand on the floor behind the front panel, seen from the knees up, and can duck and pop up. A pair of slate folding arms (a scissor X) joins tray 1's left end to the manual's page block and each tray's right end to the next tray's left end.
- The bottom drawer: built like a tray, 3500 long, its floor on the ground. Shut, it is a slot in the manual's base; in not-a-bribe-label-maker it slides out to the right to x 2600. Its stations: the label maker at x -350, the Optimitron at x 700, the templates at x 1600.
- 16:9: a tray or a station is framed at about scale 1.8, its actors' heads near the middle of the frame; the whole box is about scale 0.4. 9:16 frames tighter on each phrase's actor, above y 1450.

**Callbacks.**
- The Calculator (The Math, Part 16; Bribe the Bribers, Part 19): its cracked, taped display and its two missing keys, as Part 16 left it. It does addition happily and screams at the ×, as it screamed in Part 16 and did not in Part 19.
- The order cards in tray 4 are Part 5's five steps of paper distribution, numbered in their sacred order (Part 5 opens on that order as a money double helix longer than the room, in sacred-scroll).
- The Lobbyist's briefcase keeps its teal cross sticker (two-clients, Part 19; wiki-voters-hammock, Part 21). Its fingers get caught again (Part 17's glass lid), this time in a mousetrap, and stay flat for the rest of the part.
- The Optimitron (optimitron-appliance, Part 14; Part 17) pops cards like toast; MORE WAR comes back burnt, like Part 17's useless policy card.
- The Rich Human wears the "I PREFER LIVING" button (Part 5 on) and burns something to light his cigar, as he puffed the burning PDF in billionaire-pdf (Part 4). In Part 13 (human-greed) his hamster wheel ran him after a paper he never reached; this treadmill pays him, one paper a turn, into his own top hat.
- The Grim Reaper and his tally clipboard (Part 5; Part 21, where he never gets paid) wait beside the lectern in bribe-humanity, and get no customers.
- The iris (style bible, gag 6): manual-contains irises in on her face, and bribe-humanity irises out on it.

**Set up here.** The manual's look (the orange cover on `KIT.props.manual`) for the reader with the manual on Part 23's title card. The NOT A BRIBE strip across the Lobbyist's mask, if it turns up again later in the episode.

**Held frame.** None: there is no death toll in this part.

**Transitions.** The title card comes up from black and goes down to black; manual-contains irises in on Wishonia's face. The cut on "Pictures" goes into the manual, onto tray 1 of the plate. not-a-bribe-label-maker continues manual-toolbox's plate with no seam: it starts on its last frame (the whole open box) and the camera keeps traveling. Cuts from the plate to dysfunction-engine and from there back to the set. bribe-humanity irises out on her face to black, so Part 23's title card comes up from black.

**Bans for this part.**
- The text on screen is the jokes: the price tags, the Calculator's display, the numerals on the order cards, the three printed labels, the MORE WAR and CURE IT cards, "Dear Senator ____,", HERO, 1% TREATY, PLEASE BE GOOD, BE A BETTER HUMAN, I PREFER LIVING, and the manual's own cover. The hospital prop takes `label: ""`.

## Changes from v2

- Wishonia's office, the wall screen and her corner (PiP) are gone. She is on screen only at her lectern: manual-contains (new, 1.6 s: the manual lands on the lectern and opens on its trays) and bribe-humanity (the ending).
- The tackle box is a plate: the cut goes inside the manual, a building-sized box on a plain field, and the camera climbs its stair of four trays, one item per tray, then drops to the bottom drawer for the last three tools. The trays stay out (they no longer fold back in), so not-a-bribe-label-maker starts on the pull-back to the whole box.
- The dysfunction engine is its own plate (dysfunction-engine, new) instead of a blueprint on the wall screen. The patients' chest lights now go out when the pill bottles reach them, and the Reaper moves from the hospital door to the set.
- Jokes that needed the office: the self-help book that fell to Earth from the office in space now lands in a wastebasket beside the lectern already heaped with copies of itself; the tray lid that flattened the Lobbyist's fingers is a mousetrap under the Scientist's stack; the order cards get faces and legs, so they can stand there charred and blink.
- The title card is the period card with the whole heading on it from the start: the wrench's twist leaves EVERYTHING crooked (no word-by-word slam, no fallen G).

## Scene 1 · how-this-manual-could-fix-everything-title

- id: how-this-manual-could-fix-everything-title
- act: Title
- transition_in: up from black (the head of a reel)
- key: after "Everything.": the heading on the navy card under the emblem, EVERYTHING tilted crooked, the chrome wrench swinging away and a loose bolt bouncing off the bottom of the card
- cue: "How This Manual Could Fix Everything"
- time: 47:23.7 to 47:27.2 (3.5 s)
- voiceover: "How This Manual Could Fix Everything."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem with its three running papers, and the heading under it. Heading lines, 16:9: "HOW THIS MANUAL COULD FIX" (style small) / "EVERYTHING"; 9:16: "HOW THIS MANUAL" (small) / "COULD FIX" (small) / "EVERYTHING". The small gag: a big chrome wrench (drawn in the gag, pinned to the right end of EVERYTHING) tightens the word until it is crooked.
- props: title-card, wrench, bolt
- status: planned

Moves: "How" → the card comes up from black with the whole heading on it, the emblem's papers running round their orbits, and the camera pushes in slowly. "Fix" → a big chrome wrench swings in from the right edge of the card and clamps onto the end of EVERYTHING. "Everything." → it cranks twice, and the word tips a few degrees with each crank. after "Everything." → the wrench lets go and swings back out: EVERYTHING stays crooked, and a bolt drops out from under it, bounces twice on the bottom of the card and rolls away. The card goes down to black in its last quarter second.

Sound: a projector whirr from "How"; two ratchet clicks on "Everything."; a clank as the bolt drops.

On screen: "HOW THIS MANUAL COULD FIX EVERYTHING". Why: the narrator reads the heading, and the first thing the manual fixes, it fixes crooked.

## Scene 2 · manual-contains

- id: manual-contains
- act: What is in the manual
- transition_in: iris in on her face
- key: after "contains:": the manual open on the right end of the lectern, four little trays on folding arms climbing out of it in a stair up to the right past her antennae, the mug still rocking, Wishonia looking over at them
- cue: "This manual contains"
- time: 47:27.2 to 47:28.9 (1.6 s)
- voiceover: "This manual contains:"
- layer: A, host
- scene: The host's set (`KIT.studio`), her mug on the left end of the lectern's reading top. The manual (`KIT.props.manual({ size: 1.6 })`, standing at about (935, 790) in 16:9, the same place on the right end in 9:16) drops in from above.
- wishonia: big, happy-smile + body-presenting; lookright-oh + body-presenting on "contains:"
- props: studio, lectern, mug, manual, tray
- status: planned

Moves: "This" → the iris opens on her face while the manual drops out of the top of the frame onto the right end of the lectern with a thump; the mug jumps and rocks. "contains:" → the manual's cover springs open and four little trays clatter out of it on folding arms, stair-stepping up to the right over the free wall, the top one higher than her antennae; she turns her head and looks at them. after "contains:" → the last arm overextends with a wobble. The cut on "Pictures" goes into the first tray.

Sound: a slam on "This"; a clank and four clicks as the trays climb out on "contains:".

On screen: the manual's cover. Why: she opens the list to the viewer, and the book turns out to be a tackle box bigger than the lectern.

## Scene 3 · manual-toolbox

- id: manual-toolbox
- act: What is in the manual
- transition_in: cut (into the manual: tray 1)
- key: after "important).": tray 4 under a mushroom cloud, the five cards standing there charred black and smoking, only their white eyes blinking, cards 4 and 3 still out of order
- cue: "Pictures (because reading"
- time: 47:28.9 to 47:45.6 (16.8 s)
- voiceover: "Pictures (because reading is hard when you're diseased and dying). Simple math (addition mostly, some multiplication). Exact amounts of papers to give to specific humans. The order in which to give them (very important)."
- layer: B, plate tackle-box
- scene: The tackle-box plate (Build, above): the open manual standing on the plain field, its four trays climbing out of it in a stair up to the right. Tray 1: a fat picture book and, beside it, a 1950s iron hospital bed with a patient (an everyday human) sitting up in it. Tray 2: a big plus sign and the Calculator. Tray 3: three stacks of medicine papers, tallest on the left, and behind them the Scientist, the Politician and the Lobbyist, ducked out of sight; a mousetrap under the tallest stack. Tray 4: five cream cards on stick legs, numbered 1 to 5, with faces. The camera climbs the stair, one tray per item, and pulls back at the end to the whole box.
- props: manual, tray, picture book, hospital bed, human (the patient, then his skeleton), xray, calculator, plus sign, money (med), price-tag, scientist, politician, lobbyist, briefcase, mousetrap, numbered cards, nuke
- status: planned

Moves: "Pictures" → close on tray 1: a fat picture book pops up out of it and falls open on one big crayon drawing, a smiling pill bottle. "reading" → the camera slides along the tray to the bed beside it: the patient sits up holding a page of dense fine print up to his nose. "hard" → his eyes cross. "diseased" → his chest light blinks red. "dying)." → he x-rays into a grinning skeleton, still holding the page. after "dying)." → the skeleton tosses the page over its shoulder, reaches across, takes the picture book and flips through it, delighted, its jaw bobbing. "Simple" → the camera climbs the folding arms to tray 2: a big plus sign pops up, and the Calculator climbs up over the rim beside it. "(addition" → it taps its own keys; its display reads "1+1". "mostly," → it reads "2", and the Calculator beams and bounces. "multiplication)." → a small × sign peeks up from behind the plus. The Calculator sees it: its display flips to "ERROR", it screams and dives into the tray. after "multiplication)." → only its eyes show over the rim, trembling. "Exact" → up to tray 3: three stacks of medicine papers pop up in a row, each with a price tag to the cent: "$2,712,000.00", "$486,300.00", "$12.50". "specific humans." → the Scientist pops up behind the tallest, the Politician behind the middle one and the Lobbyist behind the $12.50, its briefcase under its arm. after "humans." → the Lobbyist's glove creeps over to the Scientist's stack, and the mousetrap under it snaps shut on its fingers: they come out flat. "order" → up to tray 4, the top of the stair: the five cards stand in a row, 1 to 5, smiling. "(very" → cards 3 and 4 quietly swap places. "important)." → tray 4 blows up: a white flash, the frame shakes, and a mushroom cloud stands over the tray. after "important)." → the five cards stand there charred black and smoking, only their white eyes blinking; 4 and 3 shuffle back into order, and the camera pulls back and back to the whole open manual, the cloud thinning over the top of the stair.

Sound: a pop for the picture book; a boing as his eyes cross; an x-ray zap on "dying)."; key clicks on "(addition" and a ding on "mostly,"; a yelp for the scream; pops for the three stacks; a slam and a yelp for the mousetrap; a squeak as the cards swap; the boom on "important)."; a sizzle as the cards smoke.

On screen: the tags "$2,712,000.00" / "$486,300.00" / "$12.50"; the Calculator's display "1+1", "2", "ERROR"; the cards "1" to "5". No: the picture book and the fine print have no titles. Why: tools for a reader who is busy, sick and dying, one per tray; the explosion is why the order is very important.

## Scene 4 · not-a-bribe-label-maker

- id: not-a-bribe-label-maker
- act: What is in the manual
- transition_in: same plate (no seam)
- key: after "governing).": the Politician hugging the Optimitron from behind and sobbing two fountains, the CURE IT card popped up into his chin, both dials swung to the top, its face perfectly flat, the burnt MORE WAR card smoking on the drawer's rim
- cue: "Legal ways to call bribes"
- time: 47:45.6 to 48:01.2 (15.5 s)
- voiceover: "Legal ways to call bribes other things. An appliance that tells your governments which policies work (it doesn't have feelings, which is why it's better at governing). Templates for tricking politicians into saving lives."
- layer: B, plate tackle-box
- scene: The same plate. The bottom drawer shoots out of the manual's base to the right along the ground under the stair of trays, and its three stations come out of it in turn: a 1950s pistol-grip label maker (no brand), the Optimitron on a little lift, and a fan of fill-in-the-blank letters. The camera travels along the drawer, left to right.
- props: manual, drawer, label maker, lobbyist, briefcase, money (plain), optimitron, politician, cards, letters, pencil, money (med), sash, medal, scroll, human (three tiny cheering humans)
- status: planned

Moves: "Legal" → the first frame is manual-toolbox's last, the whole open box. The bottom drawer shoots out of its base to the right along the ground, and the camera drops to the drawer's near end, where the label maker hops up. "call" → the Lobbyist tiptoes in along the drawer from the left (it has climbed down from tray 3), its fingers still flat, its briefcase leaking plain papers. "bribes" → the label maker chatters out a strip of red tape and slaps it on the briefcase: "CAMPAIGN CONTRIBUTION". "other" → a second strip slaps onto a leaking paper: "SPEAKING FEE". "things." → a third slaps across the Lobbyist's domino mask: "NOT A BRIBE". after "things." → the Lobbyist straightens its fedora and folds its flat fingers, very pleased. "appliance" → the camera travels along the drawer to the Optimitron, rising out of it on a little lift, its HEALTH and WEALTH dials halfway. "governments" → the Politician pops up behind it, grinning, holding up a card: "MORE WAR". "policies" → he feeds it into the toaster slot. "work" → both dials drop to the bottom, the Optimitron shudders, and it spits the card back out over the rim, burnt black and smoking. "feelings," → the camera pushes in: the Politician bursts into tears, two fountains, and hugs the Optimitron from behind; its face stays perfectly flat and its dials do not move. after "governing)." → it pops a card up like toast, "CURE IT", straight into his chin, and both dials swing up to the top. "Templates" → the camera travels on along the drawer: a fan of letters slides out across it, "Dear Senator ____,". "tricking" → the top letter folds itself into a box and props itself up on a pencil, with one medicine paper under it for bait. "politicians" → the Politician stops crying at once and tiptoes in from the left toward the bait, grinning. "saving" → he grabs it, and the box slams down on him. "lives." → the box lifts: he stands there in a HERO sash with a medal on, holding a signed 1% TREATY scroll, and three tiny humans pop up out of the drawer and cheer. after "lives." → he looks at the camera, confused; then he grins and waves.

Sound: a clank as the drawer shoots out; typewriter chatter on "bribes" and a thunk for each label; a whirr as the Optimitron rises; a slide whistle down as the dials fall and a pop and a sizzle for the burnt card; a huff for the sobs; a toaster pop and a ding for CURE IT; a slam for the box; a slide whistle up as it lifts and a ding for the medal.

On screen: the labels "CAMPAIGN CONTRIBUTION" / "SPEAKING FEE" / "NOT A BRIBE"; the cards "MORE WAR" (red) and "CURE IT"; the dials "HEALTH" and "WEALTH"; "Dear Senator ____,"; the sash "HERO"; the scroll "1% TREATY". No: nothing is labeled but what the label maker prints. Why: the tools for the parts of the plan that touch politicians: rename the bribes, let the appliance judge, and trick them into the right thing.

## Scene 5 · dysfunction-engine

- id: dysfunction-engine
- act: With human dysfunction
- transition_in: cut
- key: after "it.": close on the Rich Human sprinting on his treadmill with dollar signs in his eyes, holding his own top hat out upside down under the payout slot, heaped with medicine papers and one more dropping in, his cigar freshly lit, the burning PLEASE BE GOOD sign tumbling away over his shoulder
- cue: "Everything is designed to work"
- time: 48:01.2 to 48:05.5 (4.4 s)
- voiceover: "Everything is designed to work WITH human dysfunction, not against it."
- layer: B, plate dysfunction-engine
- scene: One wide plate on the same plain field (cream sky, tan ground). Left: the Rich Human (`KIT.cast("richHuman")`, his "I PREFER LIVING" button on) on a 1950s treadmill (a slate frame, a cream belt, and on its front post a slate payout box with a slot), his top hat off and held out upside down under the slot: each turn of the belt pushes one medicine paper out of the slot into the hat. A drive belt runs from the treadmill's roller to a chain of three gears (`KIT.props.gears`), which turn a conveyor (`KIT.props.conveyor`) that runs right, carrying smiling pill bottles (`KIT.props.pillBottle`) to three patients (everyday humans) waiting in line at the door of a hospital (`KIT.props.hospital`, `label: ""`), their chest lights blinking red. The camera starts on the whole machine and pushes in on the Rich Human.
- props: rich-human, treadmill, payout slot, top hat, money (med), gears, conveyor, pill-bottle, human (three patients), hospital, sign, flames
- status: planned

Moves: "Everything" → the whole machine, standing still, the Rich Human on the treadmill holding his empty top hat out upside down under the slot. "WITH" → he takes a step; the belt turns once and the gears creak round. "human" → the turn pays: a medicine paper pops out of the slot and drops into his hat, and his eyes ring up dollar signs. "dysfunction," → he sprints, stub legs a blur, and the faster he runs the faster it pays: papers drop into the hat one per turn until they heap up over the brim. The gears whirl, and smiling pill bottles hop onto the conveyor one after another and ride it to the patients, who each catch one: their chest lights stop blinking, one, two, three. "not" → the camera pushes in on the Rich Human. "against" → a sign on a post springs up out of the treadmill belt in his path: "PLEASE BE GOOD". after "it." → without breaking stride he plucks it with his free hand, it bursts into flame, he lights his cigar off it and tosses it over his shoulder, still running, the slot still paying.

Sound: a whirr as the engine starts on "WITH"; a cash-register ding as the first paper drops into his hat on "human"; three pops as the bottles land in the patients' hands; a thunk for the sign; a fire whoosh after "it.".

On screen: the sign "PLEASE BE GOOD" and the button "I PREFER LIVING". Why: the method in one picture: the machine pays greed by the turn, so greed runs flat out, the gears it turns deliver the medicine, and the request to be good is fuel.

## Scene 6 · bribe-humanity

- id: bribe-humanity
- act: With human dysfunction
- transition_in: cut
- key: after "dying.": Wishonia side-eyeing the camera at her lectern, the manual slammed shut with a glove and the end of the HERO sash sticking out of it and one medicine paper standing on top like a treat; beside the lectern the wastebasket heaped with BE A BETTER HUMAN books; on the right the Reaper looking at his blank tally clipboard, his scythe's blade wilted like a dead flower
- cue: "I'm not asking humans"
- time: 48:05.5 to 48:13.0 (7.5 s)
- voiceover: "I'm not asking humans to be better humans. I'm showing you how to bribe humanity into not dying."
- layer: A, host
- scene: The host's set again (the same code as manual-contains), with the mug on the left end of the lectern and the manual standing open on the right end, its trays folded away, a flat glove and the end of the HERO sash hanging out of its pages. On the floor right of the lectern a tin wastebasket heaped high with identical fat books, "BE A BETTER HUMAN". Further right on the free wall, the guest: the Grim Reaper (`KIT.reaper()`), leaning on his scythe, his tally clipboard under his arm, waiting.
- wishonia: big, neutral-smile + body-presenting; eyeroll-closed + body-presenting on "better"; smirk-ee + body-palms-down on "bribe"; smirk-smile + body-presenting on "humanity"; sideeye-closed + body-idle on "dying."
- props: studio, lectern, mug, manual, self-help book, wastebasket, money (med), reaper, clipboard
- status: planned

Moves: "I'm" → back on the set; the camera pushes in slowly on her face for the whole shot. "asking" → a fat self-help book, "BE A BETTER HUMAN", pops onto her presenting palm. "better humans." → she tips it off her palm over the edge of the lectern: it drops into the wastebasket with a thunk on top of the heap of identical copies, and a puff of dust comes up. "bribe" → she slaps the manual shut; the glove and the sash end get squashed and still stick out. A single medicine paper hops up onto the closed manual and stands there like a treat. "humanity" → she presents it to the camera. "not" → the paper takes a small bow. "dying." → the Reaper looks down at his tally clipboard: still blank. after "dying." → his scythe's blade wilts like a dead flower; crickets; she side-eyes the camera, and the film irises out on her face, to black.

Sound: a thunk as the book lands; a slam on "bribe" and a sparkle as the paper hops up; a squeak for the bow; crickets after "dying.".

On screen: the book "BE A BETTER HUMAN" (on every copy in the heap). Why: the method in one line: bribe people as they are; the better-human approach has been tried, and its copies fill the bin.
