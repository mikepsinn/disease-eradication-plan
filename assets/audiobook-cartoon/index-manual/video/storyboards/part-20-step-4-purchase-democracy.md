---
format: 1920x1080
duration: 1:36.2
message: "Weapons makers spend $198 million a year buying politicians; a one-time $1 billion budget outbids them 8 to 1, and the Super PAC pays only through a scoring algorithm that rewards treaty votes."
arc: Title card, where DEMOCRACY gets a PRE-OWNED sticker → the auction, where the Politician is a coin-op machine the Weapons Maker keeps fed, until he dies of the same diseases and keeps bidding as a skeleton → the paddles ($198 million against $1 billion), the skeleton's tower of eight topples → the price tag and the teal tie in the office → the Super PAC jet pack rewards the yes vote → the same jet pack rewards the opponent and chars the no vote; the papers ride the scenic route and the senator jumps through the hoop → the letter grade, the F monster and the HOLD → the scroll of unpaid problems wraps the Earth
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 20, "Step 4: Purchase Democracy"
audio: index-manual.cbaf659d.mp3, 44:20.7 to 45:56.9
version: v2
---

# Part 20 storyboard: "Step 4: Purchase Democracy"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys: "war papers" carry the red missile seal (`KIT.money("war")`), "medicine papers" the teal cross seal (`KIT.money("med")`), "plain papers" no seal (`KIT.money("plain")`). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Cast.** Drawn with these exact options in every scene, so each looks the same every time.
- The Politician (`KIT.cast("politician")`: lantern jaw, a grin full of teeth, slick hair, flag pin, very wide tie). The spine. His tie is war red until corrupt-the-corruption, then teal (`tieColor: KIT.C.med`) with the CLEARANCE price tag (`KIT.props.priceTag`) hanging from it for the rest of the part. Two coin slots sit on his shirt front from democracy-auction on: PAPERS and VOTES.
- The No Politician: the same `KIT.cast("politician")`, war-red tie, no tag, no slots. scenic-route-algorithm (charred), nra-letter-grade (cleaned up, then teal).
- The Old Politician: `KIT.cast("politician", { hairColor: "#B9B5AE", build: { hs: 1, legs: 1.08, tw: 1.1, neck: 0.5, chin: 1.25, hunch: 14 } })` (pass the whole build: a scene's `build` replaces the cast's). super-pac-rewards.
- The Lobbyist (`KIT.cast("lobbyist")`: fedora, domino mask, trench coat, gloves) is the auctioneer, with a gavel. His briefcase stands at his feet with the teal sticker it got in Part 19 (two-clients-arithmetic).
- The Weapons Maker (`KIT.cast("weaponsMaker")`: barrel chest, tiny head under a hard hat, cigar), cradling his baby missile; from democracy-auction on he cradles twins. Draw the twins as their own groups (`KIT.props.missile` at about 0.3, lying in his arms), not as a held prop, so they stay in his arms when he turns into `KIT.cast("weaponsMaker", { skeleton: true })` (the skeleton keeps the hard hat and the cigar).
- YOU: the busy human in the bowler from Part 1's title card, as in Parts 10 and 12 (`KIT.person({ tone: 2, outfit: "suit", hat: "bowler" })`). He bids at the back of the auction with a telescoping paddle and slips the carbon paper in nra-letter-grade.
- The Grim Reaper (`KIT.reaper()` with `KIT.props.clipboard` covered in navy tally marks in fives, as in Part 5) sits in the back row of the auction and leans by the chalkboard in nra-letter-grade.
- The Challenger: `KIT.person({ tone: 3, hair: 1, outfit: "dress", color: 1, seed: 20, mood: "eager" })` (an hourglass in a slate dress). scenic-route-algorithm.
- The Bidders: three everyday humans in the auction rows, `KIT.person({ tone: 0, outfit: "suit", color: 2, seed: 4, mood: "flat" })`, `KIT.person({ tone: 2, hair: 1, outfit: "dress", color: 3, seed: 9, mood: "smile" })` and `KIT.person({ tone: 1, outfit: "shirt", color: 0, seed: 13, mood: "flat" })`, each with a paddle on its lap.
- The Democracy Dog (`KIT.props.democracyDog({ tail: "papers", seal: "war" })`, the dog and tail of Part 6).
- The Super PAC backpack: Part 5's backpack with a cape, labeled SUPER PAC (also in Parts 17 and 23). Not in the props library: draw it the way Part 5 does.

**Spine.** The Politician. He pops out of the dome of DEMOCRACY on the auction block as a coin-op machine (two coin slots, PAPERS and VOTES), gets a CLEARANCE price tag and a teal tie when the gavel comes down, runs his race with the Super PAC as his jet pack, and jumps through the hoop for a poster.

**Running gag: YOU's paddle.** It rises at the back on "outbid", telescopes across the hall to press the Politician's nose like a vending-machine button on "free," (nothing comes out), and grows to the size of a barn door on "one billion".

**No countdown board.** This part never used it. "The clock is running" is said once: the clock over the auctioneer grows legs and runs, and the Grim Reaper's tally (Part 5's running gag for people dying while time passes) runs with it.

**Callbacks.** From the title card: the PRE-OWNED sticker stays on the dome in democracy-auction. From Part 19 (two-clients-arithmetic): the Lobbyist's briefcase with its teal sticker; the Lobbyist works for you now and runs the auction. From Part 17 (enemy-is-the-clock): the little NOT THE ENEMY sign on a stick over the Weapons Maker; (pavlovian-senators) the bell that trains senators rings again on "train", and this time the senator jumps a hoop and begs. From Part 6 (democracy-dog-loop): the Democracy Dog with its tail of war papers at the foot of the block, as Part 6 set up; it begs beside the Politician on "senator.". From Part 5 (step-4-super-pac): the caped Super PAC backpack; in Part 5 it fired posters, here it is a jet pack. From Part 1 (papers-with-presidents): the flattened human peeling up off the floor (the paper hops over the charred No Politician and flattens him). Inside the part: the coin slots (democracy-auction, scenic-route-algorithm), the teal tie (corrupt-the-corruption, nra-letter-grade), the Reaper's tally (democracy-auction, bidder-paddles, nra-letter-grade).

**Held frame.** nra-letter-grade, from "mass" to "plagiarizing". A HOLD is silent.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.
- The N.R.A. is plain typed letters only: no logo, no eagle, no gun on screen. "Mass shooting" gets the HOLD and nothing drawn for it.
- No real legislature: the domed building is the generic `KIT.props.capitol`, labeled DEMOCRACY.
- No real party names or colors beyond the tie colors (war red, teal).

## Changes from v1

- The humans are the stereotype cast: the auctioneer is the Lobbyist (in Part 19 he switched sides), the bidders are the Weapons Maker and YOU (the bowler man of Parts 10 and 12), the retiring senator is an old Politician, the opponent is an everyday human. The Grim Reaper sits in the back row with his tally.
- The Politician's hat is gone: he is a coin-op machine with two coin slots, PAPERS and VOTES, that the Weapons Maker keeps fed, and he dispenses a second baby missile.
- Every threat pays off on screen: the Weapons Maker dies of the same diseases (x-ray to a grinning skeleton) and keeps bidding; his tower of eight paddles topples on him; the Super PAC jet pack chars the No Politician; the bad mark becomes an F monster; the scroll of unpaid problems wraps the whole Earth.
- super-pac-rewards and scenic-route-algorithm are one race: "running" is a running track, campaign support is a marathon water cup, the reward is the Super PAC as a jet pack, and the same reward goes to the opponent on a no vote.
- The paddles are not drawn to scale against each other (see the note in bidder-paddles).
- The title card cuts in (the parts are rendered on their own and joined), and democracy-auction slides in from it, as loved-ones does in Part 1.
- Every scene has a Sound line, and the part file places each sound on its word.

## Scene 1 · step-4-purchase-democracy-title

- id: step-4-purchase-democracy-title
- act: Title
- transition_in: cut (the chapter card)
- key: on "Democracy.": both lines in, the PRE-OWNED sticker just clicked onto DEMOCRACY
- cue: "Step four: Purchase Democracy"
- time: 44:20.7 to 44:23.4 (2.8 s)
- voiceover: "Step four: Purchase Democracy."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`): "STEP 4" over "PURCHASE DEMOCRACY"; a 1950s supermarket price gun clicks a sticker onto the last word.
- wishonia: not on screen
- props: title-card, price-gun, sticker
- status: planned

Moves: "Step" → "STEP 4" drops in (the small line, whole). "Purchase" → PURCHASE slams in. "Democracy." → DEMOCRACY slams in, and a chunky 1950s price gun pokes in from the right edge, aims, and clicks a round sticker onto the D: "PRE-OWNED". The gun withdraws.

Sound: a thunk on STEP 4, PURCHASE and DEMOCRACY; a click as the gun fires; a pop as the sticker lands.

On screen: "STEP 4" / "PURCHASE DEMOCRACY" / the sticker "PRE-OWNED". Why: the narrator reads the heading; the sticker says somebody already bought it.

## Scene 2 · democracy-auction

- id: democracy-auction
- act: The auction
- transition_in: slide left (from the card, as loved-ones does in Part 1)
- key: after "do),": the Weapons Maker a grinning skeleton in the front row with the twins in his arms, the coin-op Politician on the block, YOU's paddle up at the back, the Reaper adding a mark
- cue: "It's For Sale Anyway"
- time: 44:23.4 to 44:43.1 (19.7 s)
- voiceover: "*It's For Sale Anyway* Politicians need papers and votes to keep their jobs. Currently, weapons manufacturers provide both. You're going to outbid them. Not because they're the enemy (they die of the same diseases you do), but because politicians do not do things for free, and the clock is running."
- layer: B
- scene: An auction hall drawn on the paper: the domed DEMOCRACY building (`KIT.props.capitol`, label "DEMOCRACY") on an auction block, the PRE-OWNED sticker on its dome, the Democracy Dog at its foot; the Lobbyist at a podium under a wall clock; rows of folding chairs with the Weapons Maker in front, the Bidders in the middle, YOU and the Grim Reaper at the back.
- wishonia: PiP, neutral-smile + idle, then smirk-smile + point-right on "outbid", sad-closed + idle on "die", eyeroll-closed + shrug on "free,"
- props: capitol, sign, auction-block, podium, gavel, wall-clock, politician, coin-slots, lobbyist, briefcase, weapons-maker, missile, human (YOU, the Bidders), paddle, reaper, clipboard, democracy-dog, papers-war, ballot
- status: planned

Moves: "It's" → the hall slides in: the dome wears the PRE-OWNED sticker from the title card, the dog chases its tail of war papers round the foot of the block, the Lobbyist taps his gavel, the wall clock ticks. "Sale" → a FOR SALE sign (`KIT.props.sign`, one pole) drops on a string and hooks onto the dome's pennant pole, swinging. "Anyway" → the dog completes one more lap of its tail, unbothered. "Politicians" → the dome lifts like a lid and the Politician pops up out of the building like a jack-in-the-box, grinning every tooth, and steps onto the block. "papers" → a coin slot pops onto his shirt front, "PAPERS", with a little red flag up: "EMPTY". "votes" → a second slot pops on beside it, "VOTES", flag up. "jobs." → his grin sags and he slumps like a toy with a flat battery. "Currently," → the Weapons Maker stands up in the front row, baby missile in the crook of one arm. "provide" → he feeds a war paper into PAPERS (it is sucked in like a bill into a change machine) and pokes a ballot into VOTES. "both." → both EMPTY flags snap down, the Politician springs upright, grin at full power; after "both." → a little flap at his belt drops open and a second baby missile slides out into the Weapons Maker's free arm. He cradles the twins. "outbid" → at the back, YOU raises a paddle: "YOU". "them." → every head in the hall turns slowly to look at it, the Reaper's skull and the dog's too. "enemy" → the little NOT THE ENEMY sign from Part 17 pops up on a stick over the Weapons Maker's hard hat; he points up at it, grinning. "die" → his chest light blinks red; he taps it like a stuck gauge. "same diseases" → every chest light in the hall blinks red, the Politician's and the Lobbyist's too; in the back row the Reaper licks his pencil. after "do)," → the Weapons Maker x-rays into a grinning skeleton, hard hat and cigar still on, the twins still in his arms, both looking up at him; he sits back down. The Reaper adds one mark to his tally. "not" (the second) → YOU's paddle telescopes across the whole hall and boops the Politician's nose like a vending-machine button. "free," → nothing comes out; a little flag pops up out of his ear: "EXACT CHANGE ONLY". The paddle telescopes back. "clock" → the wall clock over the podium sprouts two stick legs; "running." → it runs in place, its hands whirling, and in the back row the Reaper's pencil goes as fast as the hands, tally marks filling his clipboard. It keeps running to the end of the scene.

Sound: a clank as the sign hooks on; a boing as the Politician pops out; a pop for each coin slot; a falling slide whistle as he runs down; two clicks as the paper and the ballot go in; a boing as he springs up; a vending-machine thunk as the missile drops out; a rising slide whistle for YOU's paddle; a whoosh as the heads turn; a pop for the NOT THE ENEMY sign; two ticks as he taps his light; a zap for the x-ray; a pencil scratch for the tally mark; a squeak for the nose boop; a pop for the flag; four ticks from the clock; a whirr as it runs; two pencil scratches for the tally.

On screen: "DEMOCRACY" (the frieze) / "PRE-OWNED" / "FOR SALE" / the slots "PAPERS" and "VOTES" with their "EMPTY" flags / the paddle "YOU" / "NOT THE ENEMY" / "EXACT CHANGE ONLY". No: no real legislature or flag; no money handed to anyone by hand except into the slots. Why: politicians sell, the weapons makers keep them fed, the buyers die of the same diseases, and the clock does not wait.

## Scene 3 · bidder-paddles

- id: bidder-paddles
- act: The auction
- transition_in: same form (no seam)
- key: on "cycle).": the tower of eight paddles toppling onto the skeleton, under YOU's barn-door paddle
- cue: "Your explosion manufacturers spend"
- time: 44:43.1 to 44:58.3 (15.1 s)
- voiceover: "Your explosion manufacturers spend one hundred and ninety-eight million dollars a year buying politicians. Your one-time bribery budget is one billion dollars, which is eight times their annual spend (and about twice what they spend over a full election cycle)."
- layer: B
- scene: The same hall, closer on the front: the skeleton's paddle against YOU's, which grows to the size of a barn door; the skeleton steals the Bidders' paddles and stacks them to match it.
- wishonia: PiP, smirk-smile + idle, then excited-closed + wide-gesture on "billion", smirk-closed + arms-crossed on "cycle)."
- props: weapons-maker (skeleton), missile, paddle, politician, coin-slots, lobbyist, gavel, human (YOU, the Bidders), reaper, clipboard, wall-clock, papers-war
- status: planned

Moves: "Your" → the first frame is democracy-auction's last: the skeleton in the front row with the twins, the clock running in place, the Reaper scribbling; the camera starts a slow push in on the front row. "explosion" → the twins each hiccup a tiny puff of black smoke. "hundred" → the skeleton raises his paddle with a bony arm: "$198 MILLION / YEAR". The Lobbyist points the gavel at him. "buying" → a ribbon of war papers flies off the paddle and into the Politician's PAPERS slot; "politicians." → the Politician blows the skeleton a kiss. "Your" (the second) → YOU raises his paddle again, and it keeps rising on its telescoping handle; "billion" → its card flips: "$1 BILLION, ONE TIME", and the card grows to the size of a barn door, shading the whole front row. "eight" → the skeleton climbs up on his chair, snatches the paddles off the Bidders' laps around him (they look at their empty hands) and stacks them on top of his own, one, two, three, a click each, swaying; "spend" → the eighth one reaches the top of YOU's card. "twice" → in the back row, without looking up from his tally, the Reaper holds up two bony fingers. "full" → the tower of paddles sways one slow full circle, like a clock hand. "cycle)." → it topples onto the skeleton with a crash. after "cycle)." → his grinning skull pops up out of the pile, hard hat on, the twins' noses poking out beside it; the Lobbyist's gavel hangs in the air, waiting.

Sound: two little pops for the hiccups; a whoosh as the skeleton's paddle goes up; two squeaks for the ribbon of papers; a pop for the kiss; a rising slide whistle for YOU's paddle; a ding as the card flips; eight clicks as the paddles stack; a whoosh as the tower sways; a slam as it falls; a boing as the skull pops up.

On screen: "$198 MILLION / YEAR" / "$1 BILLION, ONE TIME". No: no ruler, scale or numbers on the eight stacked paddles (the narration's "eight times" does not equal $1 billion divided by $198 million, so the picture must not measure it; the eight paddles are the narrator's count, not a chart). Why: the price comparison that makes the plan affordable.

## Scene 4 · corrupt-the-corruption

- id: corrupt-the-corruption
- act: The punchline
- transition_in: zoom out of the wall screen
- key: after "corruption." (second): the mug coming down, the smirk at the camera, the teal tie with its CLEARANCE tag on the wall screen
- cue: "Politicians are surprisingly affordable"
- time: 44:58.3 to 45:04.3 (6.0 s)
- voiceover: "Politicians are surprisingly affordable. It's not corruption if you corrupt the corruption."
- layer: A
- scene: Wishonia at the desk; the wall screen still shows the auction: the gavel comes down, the Politician gets a price tag, and his tie turns teal while she sips.
- wishonia: big, smirk-closed + body-idle, then smirk-smile + body-hands-hips on "corrupt"
- props: office, desk, mug, wall-screen, politician, price-tag, lobbyist, gavel
- status: planned

Moves: "Politicians" → the zoom out starts on bidder-paddles' last frame inside the wall screen: the toppled paddles, the grinning skull, the gavel in the air. "surprisingly" → on the wall screen the gavel comes down, and a price tag (`KIT.props.priceTag`) flips onto the Politician's wide tie: "CLEARANCE". "affordable." → Wishonia's mug rises from the desk and she sips, eyes on the camera. "corrupt" → on the wall screen the Politician's tie flips from war red to medicine teal, the price tag spinning round with it. "corruption." (second) → Wishonia sets the mug down slowly and smirks at the camera.

Sound: a gavel thunk; a pop as the tag flips on; a sparkle as the tie turns teal; a soft click as the mug touches the desk.

On screen: the price tag "CLEARANCE". Why: the step's punchline, played to the camera, with the mug sip before it (style bible, gag 3).

## Scene 5 · super-pac-rewards

- id: super-pac-rewards
- act: The scoring algorithm
- transition_in: zoom into the wall screen
- key: on "rewarded.": the Politician rocketing down the track with the Super PAC backpack firing on his back
- cue: "Remember that two point seven two"
- time: 45:04.3 to 45:21.5 (17.2 s)
- voiceover: "Remember that two point seven two billion dollars a year from step one? This is where it goes. The Super PAC gives money to politicians based on how they voted on the treaty. Simple: campaign support for the ones running, post-office fellowships for the ones retiring. Vote yes on the treaty, get rewarded."
- layer: B
- scene: A running track drawn round the paper. The teal stream from Step 1 pours into the caped Super PAC backpack at the trackside, by two console buttons, YES and NO; the Politician runs the race, an old Politician retires into an armchair.
- wishonia: PiP, thinking-small + thinking, then happy-smile + point-right on "goes.", smirk-smile + hands-hips on "rewarded."
- props: track, pipe, papers-teal, price-tag, backpack, yes-button, politician, coin-slots, armchair, sign, paper-cup
- status: planned

Moves: "Remember" → a running track, lanes and all, drawn on the paper; at the left edge the glass pipe from Step 1 (Part 17's capped 10%). "two" → the stream of medicine papers flows in through it; "billion" → its tag swings into view: "$2.72 BILLION / YEAR". "goes." → the stream pours into the Super PAC backpack at the trackside, which swells like a balloon. "Super" → its cape snaps out and it strikes the hero pose from Part 5. "voted" → two console buttons spring up out of the trackside: a teal YES (`KIT.props.yesButton`) and a red NO (the same prop, `label: "NO"`, color war red). "Simple:" → a starting line draws itself across the track, and the Politician (teal tie, CLEARANCE tag) crouches at it in a sweatband. "support" → he jogs off down the track; the backpack runs beside him on its strap legs like a trainer. "running," → it hands him a paper cup full of medicine papers and he throws it in his own face, as runners do. "post-office" → off the track, the Old Politician shuffles to a huge plush armchair under a sign (`KIT.props.sign`): "POST-OFFICE FELLOWSHIP"; "retiring." → he sits and sinks into the cushions until only his wide tie sticks out of them, waving. "yes" → the Politician comes round the bend and slaps the YES button in passing. "rewarded." → the backpack jumps onto his back, its straps snap tight, and it fires like a jet pack: he rockets off round the track in a teal exhaust of confetti papers, grinning all his teeth.

Sound: a whoosh as the stream flows in; a pop as the tag swings in; a rising slide whistle as the backpack swells; a whoosh as the cape snaps; a thunk as the buttons spring up; a pop as the starting line draws; running pats as he jogs; a splat as the cup hits his face; a whoosh as the armchair slides in; a falling slide whistle as the Old Politician sinks; a squeak as the tie waves; a click as he slaps YES; a clank as the straps snap; a fire whoosh and a whoosh as the jet pack fires.

On screen: "$2.72 BILLION / YEAR" / "SUPER PAC" / "YES" / "NO" / "POST-OFFICE FELLOWSHIP". No: no money handed to a politician; the PAC pays the race and the armchair. Why: where the Super PAC money goes, and the rule: yes gets rewarded.

## Scene 6 · scenic-route-algorithm

- id: scenic-route-algorithm
- act: The scoring algorithm
- transition_in: same form (no seam)
- key: after "senator.": the Politician sitting up and begging with a poster in his teeth beside the begging Democracy Dog, the papers' roller coaster winding through SCORING ALGORITHM, the charred No Politician blinking
- cue: "Vote no, watch your opponent"
- time: 45:21.5 to 45:34.0 (12.5 s)
- voiceover: "Vote no, watch your opponent get rewarded. No papers go directly to politicians. The papers take a scenic route through a scoring algorithm, which is apparently the only legal way to train a senator."
- layer: B
- scene: The same track. The No Politician votes no; the jet pack leaves the Politician and rockets the Challenger off instead, charring him. Then the papers board a roller coaster that winds over the whole paper and through a box of gears, SCORING ALGORITHM, and out comes the treat.
- wishonia: PiP, smirk-closed + idle, then happy-smile + wide-gesture on "scenic", skeptical-smile + arms-crossed on "train"
- props: track, yes-button, politician, coin-slots, price-tag, human (the Challenger), backpack, papers-teal, roller-coaster, sign, gears, hoop, bell, poster, democracy-dog
- status: planned

Moves: "Vote" → the first frame is super-pac-rewards' last: the Politician rocketing round the far bend. At the starting line stands the No Politician, the same in every way except his war-red tie, no tag and no slots. "no," → he slaps the red NO button. "opponent" → beside him the Challenger finishes tying her shoe and stands up. "rewarded." → the jet pack zooms back, drops off the Politician (who keeps running on his own legs, fine) and straps onto the Challenger's back; it fires, she rockets off, and its blast hits the No Politician square on. after "rewarded." → he stands there charred black and smoking, hair straight up, only his eyes blinking. "directly" → a single medicine paper walks past the Politician as he jogs by; he flips open his PAPERS slot hopefully; the paper side-steps it. "politicians." → the charred No Politician lunges for it; it hops over him and he lands flat as a pancake, eyes blinking. "scenic" → the papers climb into a little roller-coaster car; "route" → it plunges down a long winding track that loops over the whole paper, past a little sign, "SCENIC VIEW" (`KIT.props.sign`), every paper's arms up; "through" → it corkscrews; "scoring" → the track runs into a riveted box of gears (`KIT.props.gears`) labeled "SCORING ALGORITHM"; "algorithm," → its lamps blink and the gears turn. "train" → the bell from Part 17's pavlovian-senators rings, and the Politician jumps through a hoop on a stand: "YES ON THE TREATY". "senator." → the box pops a campaign poster out of its slot like toast, and he catches it in his teeth. after "senator." → he sits up and begs, poster in his teeth, tie wagging; the Democracy Dog trots in from the auction and sits up and begs beside him, exactly in time.

Sound: a click as he slaps NO; a squeak as she tightens the shoe; a clank, a fire whoosh and a boom as the jet pack switches and fires; a sizzle as the smoke clears; a squeak as the paper side-steps; a boing as it hops over him; a rising slide whistle up the first climb and a falling one down the drop; a yelp from the papers in the corkscrew; a whirr from the gears; a ding from the lamps; the bell; a toaster pop for the poster; a woof from the dog.

On screen: "SCENIC VIEW" / "SCORING ALGORITHM" / the hoop "YES ON THE TREATY". No: no paper ever touches a politician's hand. Why: the money never touches a politician; the algorithm does the training.

## Scene 7 · nra-letter-grade

- id: nra-letter-grade
- act: The scoring algorithm
- transition_in: slide left
- key: after "diseases.": the teal A on the report card, the No Politician's tie gone teal as he hugs it, the Reaper slumped over the F stamped on his own clipboard
- cue: "The N.R.A. already perfected"
- time: 45:34.0 to 45:47.5 (13.5 s)
- voiceover: "The N.R.A. already perfected this technology. They give politicians a letter grade, and your senators are more afraid of a bad mark than a mass shooting. You're plagiarizing their system and replacing "guns" with "not dying from diseases.""
- layer: B
- scene: A 1950s schoolroom drawn on the paper: a chalkboard and a small school desk with the No Politician squeezed into it. A report card with an F turns into a monster; YOU slips carbon paper under it and the subject is rewritten; the Reaper flunks.
- wishonia: PiP, skeptical-closed + arms-crossed, then sad-closed + idle on "mass", smirk-smile + point-right on "plagiarizing"
- props: chalkboard, school-desk, politician, report-card, plain-paper, carbon-paper, human (YOU), reaper, clipboard, stamp-mark
- status: planned

Moves: "The" → the schoolroom slides in: the No Politician (the soot brushed off, one last wisp of smoke rising from his hair) squeezed into a small school desk, the Reaper leaning by the chalkboard with his tally. "N.R.A." → the letters type onto a plain card pinned to the chalkboard. "letter" → a report card slides onto his desk; "grade," → a big red F stamps onto it. "afraid" → he sweats in streams; his wide tie flaps like a flag in a gale. "bad" → the F peels itself off the card and grows to twice his height; "mark" → it sprouts claws and fangs and looms over him; he throws up his arms. "mass" → HOLD: everything stops, the F in mid-lunge, the Politician mid-cower, his sweat drops hanging in the air. Silent. "plagiarizing" → YOU tiptoes in behind the desk and slips a sheet of carbon paper under the report card. "guns" → on the card's subject line, GUNS is crossed out. "not" → NOT DYING FROM DISEASES writes itself in; "diseases." → the F monster shrinks back down onto the card and turns into a teal A. after "diseases." → the No Politician's tie flips from war red to teal and he hugs the card; by the chalkboard, the Reaper finds a red F stamped on his own clipboard (`KIT.props.stampMark`) and slumps.

Sound: typewriter clacks for N.R.A.; a slam as the F stamps on; a whoosh as the tie flaps; a rising slide whistle as the F grows; a yelp as he cowers; silence for the HOLD; a whoosh as the carbon paper slides in; a marker squeak for the cross-out; two marker squeaks as the new subject writes in; a sparkle as the A turns teal; a rubber-stamp thunk for the Reaper's F; a falling slide whistle as he slumps.

On screen: "N.R.A." (typed, text only) / the report card "SUBJECT: ~~GUNS~~ NOT DYING FROM DISEASES" with "F", then "A" / the Reaper's "F". No: no N.R.A. logo, no gun and nothing drawn for "mass shooting": the HOLD is the only answer to that line. Why: proof that grading politicians works, borrowed from a group that already does it.

## Scene 8 · most-problems-scroll

- id: most-problems-scroll
- act: The bond for everything
- transition_in: zoom out of the wall screen
- key: after "problems.": the scroll wrapped round and round the Earth on the wall screen, the Earth's worried eyes peeking out, Wishonia mid-shrug
- cue: "The Incentive Alignment Bond works"
- time: 45:47.5 to 45:56.9 (9.5 s)
- voiceover: "The Incentive Alignment Bond works for any problem where politicians need to do something good but haven't been paid to do it yet, which on your planet is most problems."
- layer: A
- scene: Wishonia at the desk holds up the bond while a scroll of problems drops off the desk, unrolls across the tiled floor and out of the frame; on the wall screen it comes down from space and wraps the whole Earth like a parcel.
- wishonia: big, neutral-smile + body-presenting, then lookright-smile + body-idle on "yet,", eyeroll-smile + body-shrug on "most"
- props: office, desk, wall-screen, bond, scroll, earth-globe
- status: planned

Moves: "The" → the zoom out starts on nra-letter-grade's last frame inside the wall screen. "Bond" → the bond certificate (`KIT.props.bond`, text "INCENTIVE ALIGNMENT BOND") rises from behind the desk and Wishonia presents it. "problem" → a scroll (`KIT.props.scroll`, title "PROBLEMS") drops off the end of the desk, bounces once, and starts to unroll across the tiled floor toward the wall screen: "1. WAR", "2. DISEASE", "3. POTHOLES", and on. "haven't" → it keeps unrolling, faster, under the wall screen. "yet," → Wishonia glances after it. "planet" → it rolls out of the frame, and the wall screen clicks over to the Earth (`KIT.props.earthGlobe`, face "worried"). "most" → Wishonia shrugs. "problems." → on the wall screen the end of the scroll comes down from space and wraps round and round the Earth like a parcel. after "problems." → the Earth's worried eyes peek out between two turns. The part ends on that frame.

Sound: a sparkle as the bond rises; a thunk as the scroll hits the floor; a whirr as it unrolls, and another as it speeds up; a switch click as the wall screen changes; a whoosh as the scroll comes down; soft pats as it wraps the Earth.

On screen: "INCENTIVE ALIGNMENT BOND" / the scroll "PROBLEMS: 1. WAR 2. DISEASE 3. POTHOLES". Why: widens the tool to every problem without a new argument, and the list is longer than the planet.
