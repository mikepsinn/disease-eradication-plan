---
format: 1920x1080
duration: 0:49.3
message: "The manual is built for humans as they are: pictures, simple math, exact amounts and the order to pay them, legal names for bribes, an appliance that rates policies, and templates for tricking politicians into saving lives."
arc: Title card (it breaks on "Fix" and gets fixed, crooked) → the manual opens like a tackle box (pictures, math, amounts, the order, and the order blows up) → its bottom drawer (the label maker, the Optimitron, the politician trap) → the dysfunction engine on the wall screen, the manual slammed shut on its cast, one teal paper held up like a treat
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 22, "How This Manual Could Fix Everything"
audio: index-manual.cbaf659d.mp3, 47:23.7 to 48:13.0
version: v2
---

# Part 22 storyboard: "How This Manual Could Fix Everything"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's office; Layer B is the printed Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The manual as a tackle box. The book itself (`KIT.props.manual`: "HOW TO END WAR AND DISEASE", the theme song's orange cover) stands on the left end of Wishonia's desk. In manual-toolbox its cover swings open and four trays climb out on folding arms; at the end they fold back in. In not-a-bribe-label-maker its bottom drawer slides out and the last three tools come out onto it. In bribe-humanity Wishonia slams the drawer and the cover shut on everything, cast included. The whole part stays in the office.

**The wall screen.** Off (dark) through manual-toolbox and not-a-bribe-label-maker, so the trays and the drawer read in front of it. It clicks on at "Everything" in bribe-humanity, to the dysfunction engine blueprint.

**Fixed positions** (both author groups use these, so the seam into not-a-bribe-label-maker matches):
- The manual: `KIT.props.manual({ size: 2.4 })` standing at (1115, 905) in 16:9 and `{ size: 1.9 }` at (175, 1250) in 9:16 (its base on the desk top).
- Open cover: `.manual-cover` at scaleX -0.35 about (-42, -59) (swung back past the spine, seen nearly edge-on).
- The mug: `KIT.mug` at (1775, 800) scale 1.5 in 16:9, (952, 1173) scale 1.1 in 9:16, as in Part 1.
- The wall screen off: `KIT.wallScreen(...KIT.OFFICE.screen)` with its hole (x + 34, y + 34, w - 68, h - 68, rx 22) filled `C.slate` and one cream glint (a thin diagonal band across the hole's top-left corner, opacity 0.25).

**Callbacks.**
- The Calculator (The Math, Part 16, and Bribe the Bribers, Part 19, where for once it did not scream) does addition happily in tray 2 and screams at the × sign.
- The order list in tray 4 is a strip of Wishonia's pull-down scroll of the five steps (sacred-scroll, Part 5).
- The Optimitron (optimitron-appliance, Part 14; wishocratic-allocation, Part 17) rises out of the drawer and pops cards like toast.
- The Lobbyist still wears its teal sticker from the color flip (Part 19; panel 5 of Part 21).
- The Rich Human still wears the "I PREFER LIVING" button (Part 21, panel 4), and lights his cigar with a paper again, as with the PDF in billionaire-pdf (Part 4).
- The Grim Reaper and his tally clipboard (the running gag from Part 5) wait at the hospital door in bribe-humanity, and get no customers.
- The office floats in space above Earth (style bible, Layer A), so the self-help book Wishonia drops falls a very long way.

**Bans for this part.**
- No real people or logos. The label maker, the picture book, the self-help book and the treaty are generic; no real senators.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every item that comes out of the manual moves on its word.
- No label cards for what the captions already say ("PICTURES", "SIMPLE MATH", "EXACT AMOUNTS", "THE ORDER", "Designed to work WITH human dysfunction", "AGAINST").
- Captions keep-out: nothing important below y 900 in 16:9; keep above y 1450 in 9:16.
- Money is always money green (`KIT.money`); the treat and the stacks are medicine money (teal cross seal), the Lobbyist's leaking briefcase is plain money.

## Changes from v1

- The humans are the stereotype cast: a patient (an everyday human) in tray 1; the Scientist, the Politician and the Lobbyist behind their stacks in tray 3; the Lobbyist gets the labels; the Politician feeds the Optimitron and walks into the trap; the Rich Human runs the dysfunction engine; the Grim Reaper waits at the hospital.
- Gags pushed to the end: the patient dies reading the fine print and his skeleton enjoys the picture book; the Calculator screams at the × and hides; the Lobbyist's fingers get flattened in the lid; two cards swap and the order tray blows up; the Optimitron spits the MORE WAR card back out charred; the Politician gets trapped into being a hero; the self-help book falls all the way to Earth; the manual slams shut on its cast; the Reaper's scythe wilts.
- The design-rule text and the crossed-out AGAINST on the wall screen are cut (the captions say them); the screen shows the dysfunction engine instead.
- Wishonia "tapping the list twice" (the sprites cannot tap) becomes the order tray's explosion.
- The four trays fold back in at the end of manual-toolbox, and the label maker comes out of a bottom drawer, so not-a-bribe-label-maker starts on a clean frame.
- The title card cuts in (Part 21 ends on Layer B paper, and a title card has no wall screen to zoom out of).
- Sound lines added.

**Transitions.** Layer B is the footage on Wishonia's wall screen. Office to Earth zooms into the wall screen; Earth to office zooms out of it. Earth to Earth slides left. A scene that continues the last one ("same form (no seam)") starts on its last frame. This part stays in the office: the title card cuts in, manual-toolbox cuts in after it, and the other two continue with no seam.

## Scene 1 · how-this-manual-could-fix-everything-title

- id: how-this-manual-could-fix-everything-title
- act: Title
- transition_in: cut (Part 21 ends on Layer B paper, greed-arrow; the parts join on this cut)
- key: after "Everything.": all six words in, the wrench bolting the fallen G back on, crooked
- cue: "How This Manual Could Fix Everything"
- time: 47:23.7 to 47:27.2 (3.5 s)
- voiceover: "How This Manual Could Fix Everything."
- layer: A, title card
- scene: The title card (`KIT.titleScene`): the navy wall, the rising sun and the stars, with the part's heading in the cover font.
- wishonia: not on screen
- props: title-card, wrench
- status: outline

Moves: "How" → the heading slams in, one word per spoken word. "Fix" → a big chrome wrench swings in from the right edge and hangs there, ready. "Everything." → EVERYTHING slams in hardest. after "Everything." → its G drops off and clanks onto the horizon line; the wrench snatches it up and bolts it back on, crooked.

Sound: a thunk on each heading word (How, This, Manual, Could, Fix, Everything); a whoosh as the wrench swings in; a clank as the G falls; two squeaks as the wrench tightens it.

On screen: "HOW THIS MANUAL COULD FIX EVERYTHING". Why: the narrator reads the heading; the heading breaks and gets fixed, badly, on the word "Fix".

## Scene 2 · manual-toolbox

- id: manual-toolbox
- act: What is in the manual
- transition_in: cut
- key: on "order": all four trays out and full: the skeleton flipping the picture book, the Calculator's eyes over its tray's rim, the three stacks and their humans (the Lobbyist's fingers flat), the five numbered cards
- cue: "This manual contains"
- time: 47:27.2 to 47:45.6 (18.4 s)
- voiceover: "This manual contains: Pictures (because reading is hard when you're diseased and dying). Simple math (addition mostly, some multiplication). Exact amounts of papers to give to specific humans. The order in which to give them (very important)."
- layer: A
- scene: Wishonia's office, the wall screen off. The manual stands on the left end of the desk and opens like a tackle box: four trays climb out on folding arms, stair-stepping up and to the left in front of the dark wall screen (in 9:16, up over the wall screen, above Wishonia's head), and each item pops up out of its tray as it is named.
- wishonia: big, happy-smile + body-presenting, then surprised-oh + body-presenting on "multiplication", then happy-smile + body-presenting on "Exact", then happy-smile + body-counting on "order"
- props: office, desk, mug, wall-screen, manual, human (the patient, and his skeleton), pill-bottle, calculator, money-med, price-tag, scientist, politician, lobbyist, nuke
- status: outline

Moves: "This" → the manual drops onto the left end of the desk with a thump; the mug jumps. "contains:" → the cover swings open and four trays climb out on folding arms, one after another, stair-stepping up and to the left. "Pictures" → tray 1: a picture book pops up and falls open on one big drawing: a war-seal paper, an arrow, a smiling pill bottle. "reading" → beside it, a tiny patient sits up in a hospital bed, holding a page of dense fine print. "hard" → his eyes cross. "diseased" → his chest light blinks red. "dying)." → he x-rays into a grinning skeleton, still holding the page. after "dying)." → the skeleton tosses the page over its shoulder, takes the picture book and flips through it, delighted. "Simple math" → tray 2: a big plus sign pops up, and the Calculator (from The Math) climbs out of the tray beside it. "(addition" → it taps its own keys; its display reads "1+1". "mostly," → the display reads "2" and the Calculator beams. "multiplication)." → a small × sign peeks up from behind the plus. The Calculator sees it, its display flips to ERROR, it screams and dives into its tray. after "multiplication)." → only its eyes show over the rim, trembling. "Exact amounts" → tray 3: three stacks of teal-seal papers pop up, each with a price tag to the cent: "$2,712,000.00", "$486,300.00", "$12.50". "specific humans." → the Scientist pops up behind the tallest stack, the Politician behind the middle one, and the Lobbyist (its teal sticker from Step 3 on the trench coat) behind the $12.50. after "humans." → the Lobbyist's glove creeps toward the Scientist's stack, and the tray's lid snaps shut on its fingers; they come out flat. "order" → tray 4: a strip of Wishonia's pull-down scroll from the Sacred Order of Paper Distribution rises, five numbered cards in a row, 1 to 5. "(very" → cards 3 and 4 quietly swap places by themselves. "important)." → tray 4 blows up: a white flash, the office shakes, and a little mushroom cloud rises out of the tray. after "important)." → the cloud clears on five charred, smoking cards, only their white eyes blinking; 4 and 3 shuffle back into order, and all four trays fold back into the manual with a clank, a smoke ring puffing out of the top.

Sound: a slam as the manual lands; a clank and four clicks as the trays climb out; a pop for the picture book; a boing as his eyes cross; an x-ray zap on "dying"; a whoosh as the page goes over the shoulder; a pop for the plus; three key clicks and a ding for "2"; a pop for the ×, a yelp for the scream; three pops for the stacks; a boing for the three humans; a slam and a yelp for the lid; a slide whistle up for the cards; a squeak as 3 and 4 swap; a boom; a sizzle and a squeak as the cards shuffle back; a clank as the trays fold in.

On screen: the tags "$2,712,000.00" / "$486,300.00" / "$12.50"; the cards "1" to "5"; the Calculator's display "1+1", "2", "ERROR". No: no label cards for the four items (the captions say them); the picture book and the fine print have no titles. Why: the manual as tools for a reader who is busy, sick and dying; the explosion is why the order is very important.

## Scene 3 · not-a-bribe-label-maker

- id: not-a-bribe-label-maker
- act: What is in the manual
- transition_in: same form (no seam)
- key: after "governing).": the Lobbyist in its three labels and its halo, the Optimitron's CURE IT card popping into the sobbing Politician's chin, both dials swung up, the charred MORE WAR card at his feet
- cue: "Legal ways to call bribes"
- time: 47:45.6 to 48:01.2 (15.5 s)
- voiceover: "Legal ways to call bribes other things. An appliance that tells your governments which policies work (it doesn't have feelings, which is why it's better at governing). Templates for tricking politicians into saving lives."
- layer: A
- scene: The manual's bottom drawer slides out to the left, long as a shelf, and the last three tools come out onto it: a 1950s label maker, the Optimitron, and a fan of fill-in-the-blank letters.
- wishonia: big, smirk-smile + body-presenting, then happy-smile + body-open-palms on "appliance", then neutral-smile + body-hand-chest on "feelings,", then smirk-smile + body-presenting on "Templates"
- props: office, desk, mug, wall-screen, manual, label-maker, lobbyist, money-plain, optimitron, politician, scroll, pencil, money-med, human
- status: outline

Moves: "Legal" → the first frame is manual-toolbox's last: the manual open, its trays folded in, the smoke ring fading. The bottom drawer slides out to the left, and a 1950s label maker hops out onto it. "call" → the Lobbyist tiptoes up out of the drawer, its fingers still flat, its briefcase leaking plain papers. "bribes" → the label maker chatters out a strip of tape and slaps it on the briefcase: "CAMPAIGN CONTRIBUTION". "other" → a second strip slaps onto a leaking paper: "SPEAKING FEE". "things." → a third slaps across the Lobbyist's domino mask: "NOT A BRIBE". after "things." → a halo pops on over its fedora, and the Lobbyist folds its hands, very pleased. "appliance" → the Optimitron (from Your Decentralized F.D.A.) rises out of the drawer on a little lift, its HEALTH and WEALTH dials halfway. "governments" → the Politician pops up beside it, grinning, holding a card: "MORE WAR". "policies" → it feeds the card into the toaster slot. "work" → both dials drop to zero, the Optimitron shudders, and it spits the card back out, charred and smoking, at the Politician's feet. "feelings," → the Politician bursts into tears (two fountains) and hugs the Optimitron; its face stays perfectly flat and the dials do not move. after "governing)." → it pops a card up like toast, "CURE IT", into the Politician's chin, and both dials swing up to the top. "Templates" → a fan of fill-in-the-blank letters slides out of the drawer across the desk: "Dear Senator ____,". "tricking" → the top letter folds itself into a box and props itself up on a pencil, with one teal-seal paper under it for bait. "politicians" → the Politician stops crying at once and tiptoes toward the bait, grinning. "saving" → he grabs it, and the box slams down on him. "lives." → the box lifts: he stands there in a HERO sash with a medal on, holding a signed 1% Treaty scroll, while three tiny humans cheer. after "lives." → he looks at the camera, confused; then he grins and waves.

Sound: a clank as the drawer slides out and a pop as the label maker hops out; soft tiptoe pats; typewriter chatter and a thunk for each of the three labels; a sparkle for the halo; a whirr as the Optimitron rises; a boing for the Politician; a click as the card goes in; a slide whistle down as the dials fall; a rattle as it shudders; a pop and a sizzle for the charred card; two sniffs for the tears; a toaster pop and a ding for CURE IT; a whoosh for the letters; a click for the pencil; tiptoe pats; a slam for the box; a slide whistle up as it lifts and a ding for the medal.

On screen: the labels "CAMPAIGN CONTRIBUTION" / "SPEAKING FEE" / "NOT A BRIBE"; the cards "MORE WAR" (red) and "CURE IT"; the dials "HEALTH" and "WEALTH"; the letters "Dear Senator ____,"; the sash "HERO"; the scroll "1% TREATY". No: the label maker has no brand. Why: the tools for the parts of the plan that touch politicians: rename the bribes, let the appliance judge, and trick them into the right thing.

## Scene 4 · bribe-humanity

- id: bribe-humanity
- act: With human dysfunction
- transition_in: same form (no seam)
- key: after "dying.": the manual slammed shut with the halo, a glove and the end of the HERO sash sticking out of its drawer, one teal paper standing on it like a treat; on the wall screen the patients' chest lights dark and the Reaper's scythe wilted
- cue: "Everything is designed to work"
- time: 48:01.2 to 48:13.0 (11.8 s)
- voiceover: "Everything is designed to work WITH human dysfunction, not against it. I'm not asking humans to be better humans. I'm showing you how to bribe humanity into not dying."
- layer: A
- scene: The wall screen clicks on to a Layer B blueprint, the dysfunction engine: the Rich Human runs on a treadmill after a teal-seal paper dangling from a rod on his own top hat; the treadmill turns gears that run a conveyor of pill bottles into a hospital, where patients wait at the door and the Grim Reaper waits beside them. Wishonia drops a self-help book off the desk, slams the manual shut, and offers one teal paper to the camera like a treat.
- wishonia: big, neutral-smile + body-presenting, then neutral-smile + body-palms-down on "asking", then smirk-smile + body-open-palms on "bribe"
- props: office, desk, mug, wall-screen, paper, rich-human, conveyor, gears, pill-bottle, hospital, human, reaper, clipboard, sign, money-med, manual, self-help-book
- status: outline

Moves: "Everything" → the first frame is not-a-bribe-label-maker's last. The wall screen clicks on: a blueprint on cream paper. "WITH" → on it, the Rich Human (his "I PREFER LIVING" button on) jogs on a treadmill after a teal-seal paper dangling from a fishing rod strapped to his own top hat. "human" → his eyes flip to dollar signs. "dysfunction," → he sprints; the treadmill turns a chain of gears, the gears run a conveyor, and smiling pill bottles ride it into the hospital, where a line of patients waits at the door, chest lights blinking red, and the Grim Reaper waits beside them with his tally clipboard. "against" → a sign on a post pops up in the Rich Human's path: "PLEASE BE GOOD". after "it." → without breaking stride he plucks it, lights his cigar with it and drops the stub. "asking" → a fat self-help book, "BE A BETTER HUMAN", appears under Wishonia's palm, over the front edge of the desk. "better humans." → she lets go: it drops past the desk and out of the bottom of the frame, with a long falling whistle, and a second later a faint thunk from Earth, far below. "bribe" → the drawer slams shut, shoving the label maker, the Lobbyist, the Optimitron and the Politician inside, and the cover slams after it; the halo, a glove and the end of the HERO sash stick out. A single teal-seal paper hops up onto the closed manual and stands there like a treat. "humanity" → on the wall screen, every patient at the hospital door turns its head toward the paper, with dollar signs in every eye. "not" → their chest lights stop blinking and go dark, one, two, three. "dying." → the paper on the manual takes a small bow. after "dying." → on the screen, the Reaper looks at his tally clipboard, still blank, and his scythe's blade wilts like a dead flower. Crickets; hold to the end.

Sound: a switch click and a hum as the screen comes on; a pop for the Rich Human; a cash-register ding for the dollar eyes; a whirr as the engine runs, with pops for the pill bottles; a thunk for the sign and a fire whoosh for the cigar; a long slide whistle down and a faint thunk for the book; two slams (the drawer, the cover) and a sparkle for the paper; a squeak as the heads turn; three ticks as the lights go dark; a squeak for the bow; crickets.

On screen: the button "I PREFER LIVING"; the sign "PLEASE BE GOOD"; the book "BE A BETTER HUMAN"; the hospital's own "HOSPITAL". No: no design-rule text or crossed-out AGAINST on the wall screen (the captions say them). Why: the method in one line: bribe people as they are; do not wait for better people.
