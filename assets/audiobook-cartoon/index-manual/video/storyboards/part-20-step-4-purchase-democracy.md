---
format: 1920x1080
duration: 1:36.2
message: "Weapons makers spend $198 million a year buying politicians; a one-time $1 billion budget outbids them 8 to 1, and the Super PAC pays only through a scoring algorithm that rewards treaty votes."
arc: Title card, a hairy arm with a missile tattoo lifts DEMOCRACY off the card and leaves one war bill in its place → the coin-op Politician runs down beside Wishonia's lectern → the auction, where the Weapons Maker feeds him and gets a second baby missile out of him, dies of the same diseases and keeps bidding as a skeleton, and YOU's paddle presses him for free → the paddles ($198 million against $1 billion), the skeleton's tower of eight topples and the lot goes to YOU → back at the lectern, CLEARANCE and a teal tie → the race track, where the Super PAC carries the yes vote and becomes his jet pack → the same jet pack rewards the opponent and chars the no vote; the papers ride the scenic route, the senator jumps through the hoop and then rings the training bell on himself → the letter grade, the F monster, the HOLD, the carbon copy → the scroll of unpaid problems goes all the way round the planet
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 20, "Step 4: Purchase Democracy"
audio: index-manual.cbaf659d.mp3, 44:20.7 to 45:56.9
version: v3
---

# Part 20 storyboard: "Step 4: Purchase Democracy"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("democracy-auction: hold the twins longer"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The episode is a 1950s atomic-age instructional film. Layer A is the host set (`KIT.studio`): Wishonia at her lectern talking to the viewer, with a guest standing on the free wall at her right. Layer B is an illustrated plate the camera travels over (`KIT.camera`), one framing per phrase; Wishonia is not in the plates, she is the voice. Money is money green; its seal says what it buys: war papers carry the missile seal (`KIT.money("war")`), medicine papers the cross (`KIT.money("med")`). Part 2 (`../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Cast.** Drawn with these options in every scene, so each looks the same every time.
- The Politician (`KIT.cast("politician")`: lantern jaw, a grin full of teeth, slick hair, flag pin, very wide war-red tie). From "papers" in coin-op-politician on he is a coin-op machine: two coin slots on his belly under his chest light, a bill slot (a chrome plate with a long slot) and a ballot slot (a little wooden plate with a slot), each with a small red mailbox flag that stands up when it is empty, and a little vending flap at his belt buckle. From corrupt-the-corruption on: a teal tie (`tieColor: KIT.C.med`), the CLEARANCE price tag (`KIT.props.priceTag({ text: "CLEARANCE" })`) hanging from it and a medicine paper in his bill slot. Nothing on his forehead (Parts 4 and 5 put their labels there).
- The No Politician: the same options with the war-red tie, and no slots or tag. scenic-route-algorithm (charred, then flattened) and nra-letter-grade (still sooty, hair still straight up; teal tie at the end).
- The Old Politician: `KIT.cast("politician", { hairColor: "#B9B5AE", build: { hs: 1, legs: 1.08, tw: 1.1, neck: 0.5, chin: 1.25, hunch: 14 } })` (pass the whole build: a scene's `build` replaces the cast's). super-pac-rewards.
- The Lobbyist (`KIT.cast("lobbyist")`: fedora, domino mask, trench coat, gloves) is the auctioneer, with a gavel in his glove. He works for you now (Part 19): his briefcase stands at his feet with its teal cross sticker.
- The Weapons Maker (`KIT.cast("weaponsMaker")`: barrel chest, tiny head under a hard hat, cigar), cradling his grinning baby missile from Part 2; from after "both." in democracy-auction he cradles twins. Draw both babies as their own groups (the cast's baby-missile drawing), so they stay in his arms when he becomes `KIT.cast("weaponsMaker", { skeleton: true })` after "do),"; the skeleton keeps the hard hat and the cigar.
- YOU: the busy human in the bowler from Part 1's title card, as in Parts 10, 12 and 17 (`KIT.person({ tone: 2, outfit: "suit", hat: "bowler" })`). He bids at the back of the auction with a paddle on a telescoping handle and slips the carbon paper in nra-letter-grade.
- The Grim Reaper (`KIT.reaper()`) with his tally clipboard from Part 5 (navy marks in fives, a heart box and a skull box at the top) and a pencil. He stands beside YOU at the back of the auction and leans by the chalkboard in nra-letter-grade.
- The Challenger: `KIT.person({ tone: 3, hair: 1, outfit: "dress", color: 1, seed: 20, mood: "eager" })`. scenic-route-algorithm.
- The Bidders: seven everyday humans in the auction crowd, each with a paddle: `KIT.person({ tone: 0, outfit: "suit", color: 2, seed: 4, mood: "flat" })`, `{ tone: 2, hair: 1, outfit: "dress", color: 3, seed: 9, mood: "smile" }`, `{ tone: 1, outfit: "shirt", color: 0, seed: 13, mood: "flat" }`, `{ tone: 3, outfit: "suit", color: 1, seed: 21 }`, `{ tone: 0, hair: 1, outfit: "dress", color: 0, seed: 22 }`, `{ tone: 1, outfit: "suit", color: 3, seed: 23 }` and `{ tone: 2, outfit: "shirt", color: 2, seed: 24 }`.
- The Democracy Dog (`KIT.props.democracyDog({ tail: "papers", seal: "war" })`, with the tiny grinning skeletons knotted into its tail as Part 6 draws them).
- The Super PAC: Part 5's caped backpack as Part 5's storyboard and sketch module draw it (step-4-super-pac): a rust canvas backpack with a darker rust top flap, navy straps for arms, a cream "SUPER PAC" patch with an orange inner rule on its front pocket, and a war-red cape; no mask. Copy `../compositions/scenes/part-05/step-4-super-pac.html` once it is redrawn in this look, not the old file (its navy pack, domino mask and mustard cape are the old look). As a jet pack it straps onto a back and fires a flame (`KIT.flames`) and a spray of medicine papers out of its bottom.
- The tattooed arm: the hairy forearm with the little war-red missile tattoo from Part 2's pay window (`booth()` in `../compositions/scenes/part-02/money-loop.html`; Part 19 brings it back), skin `#6F4B33`, a navy cuff, drawn big. The title card.
- The paddles: a cream card with rounded corners, a navy rim and an orange inner rule, on a short wooden stick; blank until a scene writes a number on it.

**Spine.** The Politician. He runs down like a toy at the lectern until somebody pays, gets fed by the Weapons Maker on the auction block, goes to YOU under the gavel, comes back to the lectern tagged CLEARANCE with his tie gone teal, rides the Super PAC round the race track, jumps through the hoop for a poster, and then rings the training bell on himself. His double, the No Politician, takes everything the yes vote is spared: the jet pack's blast, the pancake and the F.

**Running gag: YOU's paddle.** It rises at the back on "outbid", telescopes over every head to press the Politician's nose like a vending-machine button on "not" (nothing comes out), and grows to the size of a barn door on "billion".

**The clock.** No countdown board. "The clock is running" is said once: the wall clock over the auctioneer grows legs and runs on the spot, and the Grim Reaper's tally (Part 5's count of the humans dying while time passes) runs with it.

**Callbacks.** From Part 17 (its set-ups for this part): the little NOT THE ENEMY sign on a stick over the Weapons Maker; the glass case of the capped 20% and the "$2.72 BILLION / YEAR" tag on the Super PAC's stream; the desk bell that trained the senators rings again on "train"; this time the senator jumps a hoop for it, and then rings it on himself (Part 17's senator begged for his biscuit); the comfy armchair, slippers and golf bag behind the post-office door; the title card's STEP 1 stamp is STEP 4 here. From Part 6 (its set-up): the Democracy Dog with its tail of war papers and tiny skeletons at the foot of the auction block. From Part 5: the caped Super PAC (it swallowed a river there; here it carries a runner and becomes a jet pack); the Reaper's tally. From Part 19: the Lobbyist runs the auction for you, his briefcase with its teal sticker at his feet. From Part 2: the Weapons Maker's baby missile, now twins; the pay window's hairy forearm with the missile tattoo, which takes DEMOCRACY off the title card. From Part 1 (papers-with-presidents): the flattened human, here the No Politician after the paper hops over him. From the theme song: the charred human who stands there blinking. Inside the part: the coin slots (coin-op-politician, democracy-auction, bidder-paddles, corrupt-the-corruption); the teal tie (corrupt-the-corruption, nra-letter-grade); the Reaper's tally (democracy-auction, bidder-paddles, nra-letter-grade).

**Set up here.** The Politician's teal tie: he arrives in Part 21 (wiki-voters-hammock) still wearing it, so it stays teal to the end of this part.

**Held frame.** nra-letter-grade, from "mass" until "plagiarizing". Nothing moves and nothing sounds.

**Transitions.** The title card comes up from black and goes down to black; coin-op-politician irises in on Wishonia's face. Host shot to plate and plate to host shot are cuts. bidder-paddles continues democracy-auction on the auction hall, and scenic-route-algorithm continues super-pac-rewards on the race track, with no seam: each starts on the last one's final frame and the camera keeps traveling. most-problems-scroll irises out on her face, to black, so Part 21's title card comes up from black.

**Bans for this part.**
- The words on screen are the heading, NOT THE ENEMY, EXACT CHANGE ONLY, the two paddle cards, CLEARANCE, CAPPED AT 20%, the $2.72 billion tag, SUPER PAC, the YES and NO buttons, the YES hoop, SCENIC VIEW, N.R.A., the report card and the PROBLEMS scroll. The slots, the box of gears and the armchair carry no words (the narrator names them).
- The N.R.A. is plain chalk letters, and the parties are tie colors only.
- In the new system no paper reaches a politician's hand: the slot is the old system's, fed by the Weapons Maker; the Super PAC pays for the ride, the jet pack, the armchair and the poster.

## Changes from v2

- Wishonia's office, the cream paper and her corner (PiP) are gone. She is on screen in three host shots: coin-op-politician (new) opens the part with the Politician as her guest, corrupt-the-corruption is her verdict, and most-problems-scroll ends the part with the iris. The humans act on three plates: the auction hall, the race track and the schoolroom.
- The title card is the period card and holds the italic line "It's For Sale Anyway", as Parts 15 and 17 do theirs; STEP 4 is a stamp like Part 17's STEP 1. The FOR SALE sign and the jack-in-the-box dome went with the italic line; the Politician runs down like a toy in coin-op-politician instead. Its gag is not a price label (Part 19's card ends on a SOLD tag): the tattooed arm takes DEMOCRACY and pays one war bill for it.
- The labels went with the diagram: no PAPERS and VOTES on the slots (a bill slot and a ballot slot) and no EMPTY on the flags, no YOU on the paddle, no DEMOCRACY frieze, no POST-OFFICE FELLOWSHIP sign (Part 17's armchair), no SCORING ALGORITHM sign (the narrator names the box of gears).
- The wall-screen jokes happen to the guest: the CLEARANCE tag and the teal tie land on the Politician beside her, with the seal flip in his bill slot, in place of the mug sip. The scroll of problems runs out of the bottom of the frame and comes back in from the top, all the way round the planet, in place of wrapping the Earth on the wall screen.
- The gavel comes down at the end of bidder-paddles, so the auction ends on its own plate. The marathon water cup is gone (Part 17 has it): the Super PAC carries the tired runner instead.
- The trained senator does not sit up and beg with a treat in his teeth (Part 17's pavlovian-senators does): he jumps the hoop, catches the poster, and rings the training bell on himself. The Democracy Dog stays at the auction.

## Scene 1 · step-4-purchase-democracy-title

- id: step-4-purchase-democracy-title
- act: Title
- transition_in: up from black (the head of a reel)
- key: on "Anyway" (about 0.4 s in): STEP 4 stamped on the navy card at a tilt and PURCHASE on its line; a big hairy fist with a missile tattoo on its forearm, reaching down from the top of the card, lifting DEMOCRACY off the line by its R like a plank off a shelf, the D end drooping; one war bill fluttering down into the gap it left
- cue: "Step four: Purchase Democracy"
- time: 44:20.7 to 44:25.2 (4.6 s)
- voiceover: "Step four: Purchase Democracy. *It's For Sale Anyway*"
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem with its three running war papers, the heading under it. Heading lines, 16:9: `[{ words: ["STEP", "4"], style: "stamp", cue: "four:", offset: 0.3 }, ["PURCHASE", "DEMOCRACY"], { words: ["It's", "For", "Sale", "Anyway"], style: "italic" }]`; 9:16 (`linesTall`): `[{ words: ["STEP", "4"], style: "stamp", cue: "four:", offset: 0.3 }, ["PURCHASE"], ["DEMOCRACY"], { words: ["It's", "For", "Sale", "Anyway"], style: "italic" }]`; spoken: `["Purchase", "Democracy.", "It's", "For", "Sale", "Anyway"]`. The small gag is the tattooed arm (see Cast), its fist pinned on DEMOCRACY (`c.pin("DEMOCRACY", ...)`) so the word goes where the fist goes, and one war paper (`KIT.money("war")`).
- props: title-card, money (war), tattooed-arm
- status: planned

Moves: "Step" → the card comes up from black (0.35 s), the emblem's papers running round their orbits, and the camera pushes in slowly for the whole shot. "four:" → once the card is up (0.3 s after the word starts), STEP 4 stamps onto it at a tilt, with a shake. "Purchase" → PURCHASE slams in; "Democracy." → DEMOCRACY slams in. "It's" → the italic line comes in word by word as it is read. "Sale" → a big hairy forearm with a little missile tattoo (Part 2's pay-window arm) reaches down into the card from the top edge, over the right half of DEMOCRACY, fingers open. "Anyway" → about 0.3 s in (the word's timing runs long), ka-ching: the fist closes on the R and lifts the whole word off its line like a plank off a shelf, the D end drooping, and carries it up out of the top of the card; as it goes, one war bill flutters down into the gap after PURCHASE and lies there. The card goes down to black in its last quarter second, reading PURCHASE and one bill.

Sound: the projector whirr from "Step"; a stamp thump as STEP 4 lands ("four:"); a cash-register ka-ching as the fist takes the word ("Anyway").

On screen: "STEP 4" / "PURCHASE DEMOCRACY" / "It's For Sale Anyway". No: no price tag, sticker or SOLD sign (Part 19's card ends on SOLD). Why: the narrator reads the heading and its italic line; the picture adds who is already buying it (the war money's arm) and what it costs (one bill).

## Scene 2 · coin-op-politician

- id: coin-op-politician
- act: The auction
- transition_in: iris in on her face
- key: after "jobs.": the Politician run down beside the lectern like a toy with a flat battery, folded forward at the waist, arms hanging, both red flags up beside his empty slots; Wishonia side-eyeing him
- cue: "Politicians need papers and votes"
- time: 44:25.2 to 44:28.8 (3.6 s)
- voiceover: "Politicians need papers and votes to keep their jobs."
- layer: A, host
- wishonia: big, smirk-smile + body-presenting; thinking-small + body-counting on "papers"; sideeye-closed + body-idle on "jobs."
- scene: The host's set. Her guest on the free wall at her right: the Politician (see Cast), facing her, his bill in his raised hand.
- props: studio, lectern, politician, coin-slots, flags
- status: planned

Moves: "Politicians" → the iris opens on her face while she presents her guest: the Politician at her right, grinning every tooth, waving his bill at the camera. "papers" → a bill slot pops onto his belly, a little red flag standing up beside it: empty. "votes" → a ballot slot pops on beside it, its flag up too. "keep" → his grin flickers. "jobs." → he runs down like a wind-up toy: the grin sags, the waving arm drops, and he folds forward at the waist and stops; Wishonia side-eyes him.

Sound: a pop for each slot ("papers", "votes"); a falling slide whistle as he runs down ("jobs.").

On screen: nothing but the set and the guest. No: no PAPERS or VOTES on the slots (a bill slot and a ballot slot say it). Why: the job description as a machine that stops without coins, so the next shot can feed it.

## Scene 3 · democracy-auction

- id: democracy-auction
- act: The auction
- transition_in: cut
- key: after "do),": close on the front of the crowd: the Weapons Maker a grinning skeleton under his hard hat, cigar in his teeth, the twin baby missiles in his arms looking up at him, the NOT THE ENEMY sign on its stick over his hat, the Bidders behind him with their chest lights blinking red
- cue: "Currently, weapons manufacturers provide"
- time: 44:28.8 to 44:43.1 (14.3 s)
- voiceover: "Currently, weapons manufacturers provide both. You're going to outbid them. Not because they're the enemy (they die of the same diseases you do), but because politicians do not do things for free, and the clock is running."
- layer: B, plate auction-hall
- scene: One plate: an auction hall. The back wall is Part 2's plain tan field and the floor darker tan boards; everyone at Part 2's scale. Left: the auction block, a navy plinth with orange edges and two steps, and on it the domed capitol (`KIT.props.capitol`, no label); the Politician stands on the block in front of its doors, facing the hall; the Democracy Dog runs round after its tail at the foot of the block. Middle: the Lobbyist behind a wooden rostrum, facing the crowd, his gavel in his glove and his briefcase at his feet, a round school clock on the wall above him. Right: the bidders standing in a loose crowd facing the block, each with a paddle: the Weapons Maker at the front, nearest the block; the seven Bidders behind him in two staggered rows; at the back, YOU and the Grim Reaper beside him with his tally. The camera frames one of these at a time and pulls back to the whole hall on "them.", "not" and "running.".
- props: capitol, auction-block, politician, coin-slots, democracy-dog, lobbyist, rostrum, gavel, briefcase, wall-clock, weapons-maker, missile (the baby, then the twins), money (war), ballot, human (YOU, the Bidders), paddle, sign, reaper, clipboard, pencil
- status: planned

Moves: "Currently," → cut to the block: the Politician slumped in front of the capitol where coin-op-politician left him, both flags up; at the foot of the block the dog runs round after its tail of war papers and tiny skeletons. "weapons manufacturers" → the Weapons Maker steps up out of the front of the crowd, his baby missile in one arm. "provide" → he feeds a war paper into the bill slot (it is sucked in like a bill into a change machine) and pokes a ballot into the ballot slot. "both." → both flags snap down and the Politician springs upright, grin at full power. after "both." → the flap at his belt drops open and a second baby missile slides out into the Weapons Maker's free arm, like a can out of a vending machine; he cradles the twins and walks back to the front of the crowd. "outbid" → the camera swings to the back of the crowd: YOU, in his bowler, raises his paddle. "them." → the camera pulls back to the whole hall, and every head in it turns slowly to look at him: the Bidders', the Weapons Maker's, the Lobbyist's, the dog's and, right beside him, the Reaper's skull. "enemy" → the camera pushes in on the Weapons Maker: the little NOT THE ENEMY sign on a stick from Part 17 pops up over his hard hat, and he points up at it, grinning. "die" → his chest light blinks red; he taps it like a stuck gauge. "same diseases" → the camera eases back a little: every chest light in the crowd blinks red with his. after "do)," → he x-rays into a grinning skeleton, hard hat and cigar still on, the twins still in his arms, both looking up at him. "not" (second) → the camera pulls back to the hall as YOU's paddle telescopes across it, over every head, and boops the Politician on the nose like a vending-machine button. "free," → nothing comes out: a little red flag pops up out of his ear, "EXACT CHANGE ONLY", and the paddle telescopes back. "clock" → the camera tilts up to the clock over the Lobbyist's rostrum: it sprouts two stick legs; "running." → it runs on the spot, its hands whirling, and the camera pulls back as, at the back, the Reaper's pencil goes as fast, tally marks filling his clipboard. Both keep going to the end of the scene.

Sound: two clicks as the paper and the ballot go in ("provide"); a boing as he springs up ("both."); a vending-machine thunk as the missile drops out (after "both."); a pop for the NOT THE ENEMY sign ("enemy"); an x-ray zap (after "do),"); a squeak for the nose boop ("not", second); a pop for the ear flag ("free,"); a whirr as the clock runs ("running.").

On screen: "NOT THE ENEMY" / "EXACT CHANGE ONLY". No: no money handed over by hand (it goes into the slots). Why: the politicians sell, the weapons makers keep them fed, the buyers die of the same diseases, and the clock does not wait.

## Scene 4 · bidder-paddles

- id: bidder-paddles
- act: The auction
- transition_in: same plate (no seam)
- key: on "cycle).": the tower of eight paddles toppling onto the skeleton at the front of the crowd, YOU's barn-door paddle "$1 BILLION / ONE TIME" towering at the back, the Bidders staring at their empty hands
- cue: "Your explosion manufacturers spend"
- time: 44:43.1 to 44:58.3 (15.1 s)
- voiceover: "Your explosion manufacturers spend one hundred and ninety-eight million dollars a year buying politicians. Your one-time bribery budget is one billion dollars, which is eight times their annual spend (and about twice what they spend over a full election cycle)."
- layer: B, plate auction-hall
- scene: The same plate, framed on the crowd: the skeleton's paddle against YOU's, which grows to the size of a barn door; the skeleton takes the Bidders' paddles and stacks them to match it.
- props: weapons-maker (skeleton), missile (the twins), nuke (two tiny ones), paddle, money (war), politician, coin-slots, human (YOU, the Bidders), reaper, clipboard, lobbyist, gavel, wall-clock
- status: planned

Moves: "Your" → the first frame is democracy-auction's last: the whole hall, the clock running on the spot; the camera pushes in on the front of the crowd. "explosion" → the twins each hiccup a tiny mushroom cloud, pop, pop, and their father's skull comes out of the smoke sooty black, blinking. "hundred" → he raises his paddle with a bony arm: "$198 MILLION / YEAR"; the Lobbyist points his gavel at him. "buying" → a ribbon of war papers flies off the paddle over the crowd and into the Politician's bill slot, "politicians." → and the Politician blows the skeleton a kiss. "Your" (second) → the camera swings to the back: YOU raises his paddle again, and it keeps rising on its telescoping handle; "billion" → its card flips over, "$1 BILLION / ONE TIME", and grows to the size of a barn door, and the camera pulls back as its shadow falls over the whole crowd. "eight" → the skeleton snatches the paddles off the Bidders around him (they look at their empty hands) and stacks them on top of his own, one on another, swaying; "spend" → the eighth reaches the top of YOU's card. "twice" → at the back, without looking up from his tally, the Reaper holds up two bony fingers. "full" → the tower sways one slow full circle, "cycle)." → and topples onto the skeleton with a crash. after "cycle)." → his grinning skull pops up out of the pile, hard hat on, the twins' noses poking out beside it; the Lobbyist brings his gavel down and points it at YOU: sold. YOU tips his bowler.

Sound: two pops for the hiccups ("explosion"); a ding as YOU's card flips ("billion"); three clicks as the paddles stack ("eight"); a slam as the tower falls ("cycle)."); a gavel thunk (after "cycle).").

On screen: "$198 MILLION / YEAR" / "$1 BILLION / ONE TIME". No: no ruler, scale or numbers on the stacked paddles (the narration's "eight times" does not equal $1 billion divided by $198 million, so the picture must not measure it; the eight paddles are the narrator's count, not a chart). Why: the price comparison that makes the plan affordable, and the old bidder loses the lot.

## Scene 5 · corrupt-the-corruption

- id: corrupt-the-corruption
- act: The punchline
- transition_in: cut
- key: after "corruption." (second): Wishonia smirking at the camera, hands on hips; beside her the Politician grinning the same grin in a teal tie, the CLEARANCE tag still swinging from it, a medicine paper in his bill slot
- cue: "Politicians are surprisingly affordable"
- time: 44:58.3 to 45:04.3 (6.0 s)
- voiceover: "Politicians are surprisingly affordable. It's not corruption if you corrupt the corruption."
- layer: A, host
- wishonia: big, happy-smile + body-presenting; neutral-smile + body-palms-down on "It's"; smirk-smile + body-hands-hips on "corrupt"
- scene: The host's set. Her guest on the free wall at her right: the Politician from the auction, sold, a war paper sticking out of his bill slot, his tie still war red.
- props: studio, lectern, politician, coin-slots, money (war, med), price-tag
- status: planned

Moves: "Politicians" → cut to the set: Wishonia presents her guest like a car in a showroom; the Politician beams, a war paper sticking out of his bill slot. "surprisingly" → a price tag drops in on its string from above the frame and hooks onto his wide tie: "CLEARANCE". "affordable." → he looks down at it, then up at us, his grin undimmed. "corrupt" → his tie flips from war red to medicine teal, the tag spinning round on it, and the paper in his bill slot flips its seal from the missile to the cross. "corruption." (second) → the tag swings to a stop; he grins on, and Wishonia smirks at the camera.

Sound: a pop as the tag lands ("surprisingly"); a sparkle as the tie and the seal flip ("corrupt").

On screen: "CLEARANCE". No: nothing stuck on his forehead (Parts 4 and 5 put their labels there). Why: the step's punchline: the same man, the same grin and the same slot, with the money's seal flipped.

## Scene 6 · super-pac-rewards

- id: super-pac-rewards
- act: The scoring algorithm
- transition_in: cut
- key: on "rewarded.": the Politician rocketing down the track with the caped Super PAC strapped to his back and firing like a jet pack, a flame and a spray of medicine papers behind him, grinning every tooth, the YES button still bouncing behind him
- cue: "Remember that two point seven two"
- time: 45:04.3 to 45:21.5 (17.2 s)
- voiceover: "Remember that two point seven two billion dollars a year from step one? This is where it goes. The Super PAC gives money to politicians based on how they voted on the treaty. Simple: campaign support for the ones running, post-office fellowships for the ones retiring. Vote yes on the treaty, get rewarded."
- layer: B, plate race-track
- scene: A second plate: a running track on the plain tan field, a stadium oval of rust cinder lanes with cream lane lines (bends like Part 2's road) and a starting line across the near straight; the infield is the same tan. Along the near trackside, left to right: Part 17's glass case with "CAPPED AT 20%" on its lid and a little door in its side; the Super PAC; the console of two buttons (`KIT.props.yesButton`: YES in teal, NO in war red); the starting line; and at the right end, beside the finish, a riveted slate box of gears with a row of lamps, a toaster slot on top and Part 17's desk bell beside the slot, and a paper hoop on a stand next to it. In the infield: Part 17's comfy armchair with its slippers and golf bag. Along the top of the plate, behind the far straight, a cream wooden roller coaster on rust trestles runs from a little station by the Super PAC up a climb (a little SCENIC VIEW sign at its top), down a drop, round a loop and a corkscrew, and back down at the right end into a hole in the side of the box of gears; the near-trackside framings keep it out of the picture. Everyone at Part 2's scale. The camera frames one station at a time and pulls back to the whole plate on "route" in scenic-route-algorithm.
- props: track, glass-case, money (med), price-tag, super-pac, yes-button, politician, coin-slots, sweatband, armchair, slippers, golf-bag, flames
- status: planned

Moves: "Remember" → framing on the left end of the trackside: Part 17's glass case. "two" → its little door opens and a column of medicine papers marches out along the trackside; "billion" → a tag swings on the leader's string: "$2.72 BILLION / YEAR". "goes." → the camera travels with them to the Super PAC, and they hop into its open top one after another; it swells like a balloon. "Super" → its cape snaps out and it strikes its hero pose from Part 5. "voted" → the two buttons spring up out of the trackside beside it, YES and NO. "Simple:" → the camera travels on to the starting line: the Politician (teal tie, CLEARANCE tag) crouches at it in a sweatband. "support" → he jogs off down the track, flags at the first bend and wobbles; "running," → the Super PAC swoops in under him and flies him along a foot off the track, his legs still pedalling. "post-office" → the camera crosses the infield to the armchair: the Old Politician shuffles up to it, "retiring." → sits, and sinks into the cushions until only his wide tie sticks out, waving. "yes" → back on the near straight, the Politician comes round the bend on the Super PAC and slaps the YES button in passing. "rewarded." → the Super PAC flips round onto his back, its straps snap tight and it fires like a jet pack: he rockets off down the straight in a flame and a spray of medicine papers, grinning every tooth.

Sound: a whoosh as the papers march out ("two"); a rising slide whistle as the Super PAC swells ("goes."); a thunk as the buttons spring up ("voted"); a falling slide whistle as the Old Politician sinks ("retiring."); a click as he slaps YES ("yes"); a fire whoosh as the jet pack fires ("rewarded.").

On screen: "CAPPED AT 20%" / "$2.72 BILLION / YEAR" / "SUPER PAC" / "YES" / "NO". No: no paper into a politician's hand: the Super PAC carries him, the armchair waits for the one retiring, and the jet pack is the reward. Why: where the Super PAC money goes, and the rule: yes gets rewarded.

## Scene 7 · scenic-route-algorithm

- id: scenic-route-algorithm
- act: The scoring algorithm
- transition_in: same plate (no seam)
- key: after "senator.": by the box of gears, the Politician, his new campaign poster in one hand, slapping the desk bell on the box himself and staring at its empty slot for the next one, the burst paper hoop behind him
- cue: "Vote no, watch your opponent"
- time: 45:21.5 to 45:34.0 (12.5 s)
- voiceover: "Vote no, watch your opponent get rewarded. No papers go directly to politicians. The papers take a scenic route through a scoring algorithm, which is apparently the only legal way to train a senator."
- layer: B, plate race-track
- scene: The same plate. The No Politician votes no and the jet pack rewards his opponent instead, charring him; then the papers ride the roller coaster the long way round the whole plate into the box of gears, and out comes the treat.
- props: track, yes-button, politician, human (the Challenger), super-pac, flames, money (med), roller-coaster, sign, gears, lamps, bell, hoop, poster
- status: planned

Moves: "Vote" → the first frame is super-pac-rewards' last; the camera travels back along the straight to the console: the No Politician stands at it. "no," → he slaps the NO button. "opponent" → beside him the Challenger finishes tying her shoe and stands up. "rewarded." → the jet pack zooms back down the straight, drops off the Politician (who keeps jogging on his own legs, fine) and straps onto the Challenger's back; it fires, she rockets off, and its blast hits the No Politician square on. after "rewarded." → he stands there charred black and smoking, hair straight up, only his eyes blinking. "directly" → one medicine paper walks past him along the trackside; "politicians." → he lunges for it, it hops over him, and he lands flat as a pancake, eyes blinking. "scenic" → at the trackside the papers climb into a little roller-coaster car and put their arms up; "route" → the camera pulls back to the whole plate as the car climbs past the SCENIC VIEW sign and plunges down a track that winds over everything; "through" → it corkscrews; "scoring" → the track runs down into the box of gears beside the finish, "algorithm," → and the box's lamps blink and its gears turn. "train" → the camera pushes in on the box: the desk bell on it dings by itself, and the Politician jogs up and jumps through the paper hoop on its stand, "YES", bursting it. "senator." → the box pops a campaign poster out of its slot like toast, and he catches it. after "senator." → he reaches over and slaps the desk bell himself, ding, and stares at the slot for the next one; nothing comes out (no vote, no poster).

Sound: a click as he slaps NO ("no,"); a fire whoosh and a boom as the jet pack blasts him ("rewarded."); a sizzle as the smoke clears (after "rewarded."); a boing as the paper hops over him ("politicians."); a rising slide whistle up the climb ("scenic") and a falling one down the drop ("route"); a whirr from the gears ("scoring"); the bell ("train"); a toaster pop for the poster ("senator."); a short ding as he rings it himself (after "senator.").

On screen: "NO" / "YES" (the buttons and the hoop) / "SCENIC VIEW". No: no sign on the box of gears (the narrator names it), and no sitting up to beg with a treat in his teeth (Part 17's pavlovian-senators). Why: the money never touches a politician; the algorithm does the training, so well that he rings the bell on himself.

## Scene 8 · nra-letter-grade

- id: nra-letter-grade
- act: The scoring algorithm
- transition_in: cut
- key: after "diseases.": the No Politician squeezed into the school desk hugging his report card, GUNS crossed out on its subject line and NOT DYING FROM DISEASES written in, a teal A on it, his tie gone teal; by the chalkboard the Reaper slumped over a red F stamped on his own clipboard; YOU tiptoeing off with the carbon paper
- cue: "The N.R.A. already perfected"
- time: 45:34.0 to 45:47.5 (13.5 s)
- voiceover: "The N.R.A. already perfected this technology. They give politicians a letter grade, and your senators are more afraid of a bad mark than a mass shooting. You're plagiarizing their system and replacing "guns" with "not dying from diseases.""
- layer: B, plate schoolroom
- scene: A third plate: a 1950s schoolroom. A green chalkboard in a wooden frame on a pale slate wall, a tan wood floor, and a small school desk-and-chair with the No Politician squeezed into it, knees up to his chin, still sooty from the jet pack, his hair still standing straight up. The Grim Reaper leans by the board with his tally. Everyone at Part 2's scale.
- props: chalkboard, school-desk, politician, report-card, stamp-mark, carbon-paper, human (YOU), reaper, clipboard
- status: planned

Moves: "The" → cut to the schoolroom: the No Politician in the little desk, one last wisp of smoke rising from his hair; the Reaper leaning by the board. "N.R.A." → the letters chalk themselves onto the board. "letter" → a report card slides onto his desk; "grade," → a big red F stamps onto it. "afraid" → he sweats in streams, and his wide tie flaps like a flag in a gale. "bad" → the F peels itself off the card and grows to twice his height; "mark" → it sprouts claws and fangs and looms over him, and he throws up his arms. "mass" → HOLD: everything stops, the F mid-lunge, the Politician mid-cower, his sweat drops hanging in the air. Silent. "plagiarizing" → YOU tiptoes in behind the desk and slips a sheet of carbon paper under the report card. "guns" → on the card's subject line, GUNS is crossed out; "not" → NOT DYING FROM DISEASES writes itself in; "diseases." → the F monster shrinks back down onto the card and turns into a teal A. after "diseases." → the No Politician's tie flips from war red to teal and he hugs the card; by the board the Reaper looks down at a red F stamped on his own clipboard and slumps, and YOU tiptoes off with the carbon paper.

Sound: a chalk scratch for "N.R.A."; a stamp thump as the F lands ("grade,"); a rising slide whistle as the F grows ("bad"); a yelp as he cowers ("mark"); silence for the HOLD; a marker squeak for the cross-out ("guns"); a sparkle as the A turns teal ("diseases."); a stamp thump for the Reaper's F (after "diseases.").

On screen: "N.R.A." (chalk letters only) / the report card "SUBJECT: GUNS" (crossed out) "NOT DYING FROM DISEASES" with "F", then "A" / the Reaper's "F". No: the HOLD answers "mass shooting"; the F monster stays frozen mid-lunge through it. Why: proof that grading politicians works, borrowed from a group that already does it, with the subject swapped for the one this plan grades.

## Scene 9 · most-problems-scroll

- id: most-problems-scroll
- act: The bond for everything
- transition_in: cut
- key: after "problems.": the far end of the scroll of problems dropped back in from the top of the frame onto the lectern beside the bond, its paper running up out of the frame and down the lectern's front, numbered in the thousands; Wishonia shrugging and side-eyeing the camera
- cue: "The Incentive Alignment Bond works"
- time: 45:47.5 to 45:56.9 (9.5 s)
- voiceover: "The Incentive Alignment Bond works for any problem where politicians need to do something good but haven't been paid to do it yet, which on your planet is most problems."
- layer: A, host
- wishonia: big, neutral-smile + body-presenting; smirk-smile + body-idle on "problem"; surprised-oh + body-idle on "planet"; eyeroll-smile + body-shrug on "most"; sideeye-closed + body-shrug on "problems."
- scene: The host's set, no guest. The bond (`KIT.props.bond({ text: "INCENTIVE ALIGNMENT BOND" })`) and a scroll (`KIT.props.scroll({ text: "PROBLEMS", lines: ["1. WAR", "2. DISEASE", "3. POTHOLES", ...] })`, its paper drawn as long as the gag needs) on the lectern's reading top.
- props: studio, lectern, bond, scroll
- status: planned

Moves: "The" → cut to the set: she presents. "Bond" → the bond certificate pops up on the lectern's reading top. "problem" → the scroll drops onto the lectern beside it, and its bottom roll tumbles off the front: the list unrolls down the lectern, "1. WAR", "2. DISEASE", "3. POTHOLES" and on, and the roll runs out of the bottom of the frame. "haven't" → it keeps unrolling, faster, the numbers racing up past a hundred. "planet" → the paper goes tight and stops; she looks up. "most" → the other end of the scroll drops back in from the top of the frame, numbered in the thousands, and lands on the lectern with a thunk: the list went all the way round the planet. She shrugs. "problems." → she side-eyes the camera, and after "problems." the film irises out on her face, to black.

Sound: a sparkle as the bond pops up ("Bond"); a thunk as the scroll lands and a whirr as it unrolls ("problem"); a whistle as the far end falls back in ("most") and a thunk as it lands.

On screen: "INCENTIVE ALIGNMENT BOND" / the scroll "PROBLEMS: 1. WAR 2. DISEASE 3. POTHOLES" and its far end's numbers. No: no globe; the scroll makes the trip off screen. Why: it widens the tool to every problem without a new argument, and the list is longer than the planet.
