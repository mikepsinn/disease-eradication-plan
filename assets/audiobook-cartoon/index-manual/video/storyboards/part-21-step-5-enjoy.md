---
format: 1920x1080
duration: 1:26.8
message: "Once the treaty passes, the $27.2 billion a year pays every group that profited from war, so nobody has to become a better person."
arc: Title card → money beats morality → the money volcano → seven groups get paid, one comic panel each → the greed arrow turns around
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 21, "Step 5: Enjoy"
audio: index-manual.cbaf659d.mp3, 45:56.9 to 47:23.7
version: v2
---

# Part 21 storyboard: "Step 5: Enjoy"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The money volcano and its seven-panel comic strip. One long Earth plate: the volcano at its start, then seven comic panels in a row (in 9:16, in a column), one per group that gets paid. The volcano erupts medicine money in money-volcano; the bills pop little parachutes and hang over the whole strip as a money cloud, and a few drift down into each panel as it opens. The camera moves along the strip one panel at a time: panel 1 in money-volcano, 2 in pharma-per-patient, 3 in insurance-zero-claims, 4 in investor-lobby-force, and 5, 6 and 7 in wiki-voters-hammock. Each panel's caption box names its group on the narrator's word, and every panel ends with its group paid.

Build: the strip is one drawing shared by five scenes in two author groups, so both draw it to these numbers.
- 16:9: a cream plate (`KIT.paper`) 7400 wide in a strip group that the camera moves; Wishonia's corner and the grain sit outside it. The volcano: base x 60 to 780 on the ground at y 880, crater rim at y 330 around x 420, its label banner on the flank at (420, 620). Panel k (1 to 7): left edge x 840 + 820(k - 1), 760 wide, y 120 to 800, a navy 6 px frame with an orange inner rule, cream inside, a caption box across the top (y 120 to 190, Oswald capitals, navy), a mustard number disc at its top left, the panel's floor at y 760. The money cloud: parachuting medicine bills along y 10 to 100 from x 300 to the end, each bobbing ±6 px with a 2 s period of part time (`KIT.scene(ID).start` plus scene time), so it is continuous across scenes.
- 16:9 camera: the wide shot is scale 1 at x 0. "On panel k" is scale 1.2 with panel k's center (x0 + 380, 460) at screen (820, 480): the panel fills x 364 to 1276, y 72 to 888, the neighbors' edges show at both sides, and Wishonia's corner stays clear. Every move to the next panel is 0.6 s, power2.inOut, on the scene's first word (on "Military" in money-volcano).
- 9:16: the plate is 1080 wide and runs down. The volcano at the top: base x 80 to 1000 on y 1300, crater rim at y 760 around x 540, label at (540, 1060). Panel k: top y 1400 + 880(k - 1), x 70 to 1010, 820 tall, caption box 80 tall. "On panel k" is scale 1 with the panel at screen y 550 to 1370 (clear of the saucer and above the captions); the camera tilts down to the next panel. The bills drift down into each panel from the top of the frame.

**Running gag: the Grim Reaper is the one who does not get paid.** `KIT.reaper()`, with Part 5's tally clipboard under his arm; in this part he never adds a mark. In money-defeats-morality he reads "NOBODY DIES" on the banner and his jaw drops off. In insurance-zero-claims he wheels a dead customer up to the insurer on a hand truck and is sent away with it. In wiki-voters-hammock he drops a coconut on YOU, it bounces off the helmet back onto his skull, and he collapses into a heap of bones.

**Running gag: the Moral Human, not required.** A beanpole in a mustard shirt with a gold halo, hands clasped, eyes up (`KIT.person({ tone: 1, outfit: "shirt", kind: "twig", color: 3, mood: "smile" })`, the halo a gold ring drawn at `<!--head-end-->`). He stands on the MORALITY pan in money-defeats-morality, weighs nothing, and is catapulted out of the top of the frame on "defeats". He comes back down in the last second of the part, into the empty MORAL HUMAN box of greed-arrow.

**YOU.** The viewer is the busy human in the bowler from Part 1's title card, as in Parts 10 and 12 (`{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene, so he is the same man). He is the healthy customer whom the insurer bubble-wraps in insurance-zero-claims, the man in the hammock in wiki-voters-hammock (still wrapped, a crash helmet strapped over his bowler), and the one who swings the GREED arrow in greed-arrow (still wrapped).

**Recurring human: the insurance clerk.** A bald, box-shaped man in a suit and glasses with a green eyeshade (`{ tone: 1, outfit: "suit", kind: "box", hair: 2, glasses: true, color: 1 }`, the eyeshade drawn at `<!--head-end-->`). Panel 3, then the crowd in greed-arrow.

**Callbacks.** From Part 1 (title-card): the half-sun that sank in embarrassment rises a notch and puts on sunglasses on this title card. From Part 1 and the style bible (gag 2): the color-flip funnel takes the 1% out of the Weapons Maker's murder budget (panel 1). From Part 6 (red-blue-ties): the Politician's tie flips red, blue, then a new third color, teal (panel 6). From Part 17 (what-youre-offering): the Rich Human's "I PREFER LIVING" button (panel 4); Grandma and her BUY BONDS poster (panel 6). From Part 19 (two-clients-arithmetic): the Lobbyist's briefcase with its teal sticker (panel 5). From Part 5: the Reaper's tally clipboard. From Parts 10 and 12: YOU.

**Callback set up here.** The GREED arrow from greed-arrow swings back in greed-handles-it (Part 24): a long mustard arrow (`KIT.C.yellow`) with a navy outline and an orange edge, "GREED" in Oswald capitals on its shaft, pivoting at its middle on a riveted slate post. Draw it the same way there.

**Held frame.** None: the part states no death toll.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.
- Wikipedia is said, never shown: the encyclopedia page is generic, with no logo, globe or wordmark.
- Red team and blue team are tie colors only (`KIT.C.war` and `KIT.C.peri`, then `KIT.C.med`): no party names, animals or logos. The lab, the insurer and the factory have plain signs and no company names.

## Changes from v1

- The humans are the theme song's stereotypes: the Politician passes the treaty and gets buried in ballots, the Weapons Maker keeps his pile, the Scientist works the turnstile for Big Pharma, a box-shaped clerk runs the insurer, the Rich Human leads the lobby, the masked Lobbyist erases his page, Grandma votes, and YOU is the healthy customer, the man in the hammock and the man who swings the arrow.
- Every threat pays off on screen: the Moral Human is catapulted off the scale and lands at the end; the Reaper's jaw drops off, his customer is turned away and a coconut collapses him into bones; the Weapons Maker's pile heaves him through the top of his panel; the turnstile smokes; the germ is blown away and the missile folded; the ballots bury the Politician; the brawl flattens the diseases.
- New running gags: the Grim Reaper (the one who does not get paid) and the Moral Human (not required).
- The 1% that leaves the murder budget goes through the color-flip funnel (panel 1), and the war bills appear only in the Weapons Maker's pile; everything the volcano pays out is medicine money.
- The title card cuts in (the parts are rendered separately), and money-defeats-morality slides in from it, as loved-ones does in Part 1.
- wiki-voters-hammock shows its three panels one at a time, like the rest of the strip, so each can be read.

## Scene 1 · step-5-enjoy-title

- id: step-5-enjoy-title
- act: Title
- transition_in: cut (the parts are rendered on their own and joined)
- key: after "Enjoy.": all three words in, the streamers in the air, the sun in its sunglasses
- cue: "Step five: Enjoy"
- time: 45:56.9 to 46:00.0 (3.0 s)
- voiceover: "Step five: Enjoy."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`) with the step number and its name; the sun is in a better mood than in Part 1.
- wishonia: not on screen
- props: title-card, papers-teal, party-popper, sunglasses
- status: outline

Moves: "Step" → "STEP" slams in. "five:" → "5" slams in beside it. "Enjoy." → "ENJOY" slams in big under them, and a party popper on its last letter fires paper streamers and a burst of tiny medicine bills. after "Enjoy." → the half-sun on the horizon, which sank in embarrassment on Part 1's title card, rises a notch and slips on a pair of sunglasses.

Sound: a thunk on each heading word; a pop for the party popper; a sparkle as the sunglasses go on.

On screen: "STEP 5" / "ENJOY". Why: the narrator reads the heading; the sun has finally seen something it likes.

## Scene 2 · money-defeats-morality

- id: money-defeats-morality
- act: The treaty passes
- transition_in: slide left
- key: on "morality,": the money pan slammed down, the Moral Human gone through the top of the frame, his halo hanging in the air over the empty pan
- cue: "Everyone Gets Rich and Nobody Dies"
- time: 46:00.0 to 46:07.9 (8.0 s)
- voiceover: "*Everyone Gets Rich and Nobody Dies* Your treaty passes because money defeats morality, as is tradition."
- layer: B
- scene: A banner over a brass balance scale on a tall pedestal. On the right pan stands the Moral Human, so light the scale stays level. The Politician stands at a little desk on the left with the treaty; the Grim Reaper leans in from the right.
- wishonia: PiP, smirk-smile + body-presenting, then smirk-closed + body-shrug on "tradition."
- props: banner, balance-scale, moral-human, halo, politician, scroll, stamp, stamp-mark, papers-teal, reaper, plaque
- status: outline

Moves: "Everyone" → the banner unrolls across the top: "EVERYONE GETS RICH AND NOBODY DIES". "Nobody Dies" → the Grim Reaper leans in under the banner's right end, tally clipboard under his arm, reads it, and his jaw drops off and clatters on the floor. "treaty passes" → the Politician (`KIT.cast("politician")`), grinning with every tooth, slams a rubber stamp onto the treaty scroll: "PASSED". The Reaper picks up his jaw, jams it back on crooked and slinks out. "money" → a line of medicine bills marches up a little ramp and hops onto the left pan, one after another. "defeats" → the left pan slams down onto the pedestal; the right pan whips up and catapults the Moral Human straight out of the top of the frame. "morality," → his halo hangs in the air where his head was, for a beat, then drops onto the empty pan, which is tagged "MORALITY", with a clink. "as" → a brass plaque screws itself onto the pedestal: "AS IS TRADITION". "tradition." → the camera tilts down the pedestal: it is covered from top to bottom in identical plaques, "AS IS TRADITION", each one older and greener than the last, running out of the frame.

Sound: a whoosh as the banner unrolls; a clank as the jaw hits the floor; a rubber-stamp thunk on "passes"; squeaky paper footsteps and a pop per bill onto the pan; a slam on "defeats" with a rising slide whistle as the Moral Human flies; a small ding as the halo lands; three ticks as the plaque screws on.

On screen: "EVERYONE GETS RICH AND NOBODY DIES" / "TREATY" / "PASSED" / the pan tag "MORALITY" / the plaques "AS IS TRADITION". No: the Reaper's jaw is a plain bone piece, no blood; he only looks embarrassed. Why: the treaty passes the way everything passes, by money, and morality goes flying.

## Scene 3 · money-volcano

- id: money-volcano
- act: The money volcano
- transition_in: slide left
- key: after "returns.": the Weapons Maker heaved through the top of panel 1 on his medicine pile, kissing his baby missile; the money cloud over the strip
- cue: "The twenty-seven point two billion"
- time: 46:07.9 to 46:20.5 (12.6 s)
- voiceover: "The twenty-seven point two billion dollars a year money volcano erupts: Military Contractors keep ninety-nine percent of their murder budget PLUS get two hundred and seventy-two percent returns."
- layer: B
- scene: The left end of the strip: a faceted volcano and, beside it, panel 1, empty. The volcano erupts medicine money; the camera moves onto panel 1, where the Weapons Maker sits on his pile of war money in front of his factory.
- wishonia: PiP, excited-open + body-wide-gesture, then smirk-smile + body-point-right on "Military"
- props: money-volcano, comic-strip, papers-teal, papers-red, parachute, weapons-maker, factory, color-flip-funnel, price-tag
- status: outline

Moves: "The" → the plate slides in, wide: the volcano, panel 1 with a blank caption box, and the rest of the strip trailing off to the right. "twenty-seven point two billion" → a banner unfurls across the volcano's flank: "$27.2 BILLION / YEAR". "volcano" → it rumbles; smoke curls out of the crater and the paper shakes. "erupts:" → it blows: a geyser of medicine bills shoots out of the crater, legs kicking; high up, each one pops a tiny cream parachute, and they spread across the top of the whole strip as a money cloud. "Military Contractors" → the camera moves onto panel 1 and its caption box fills: "MILITARY CONTRACTORS". The Weapons Maker (`KIT.cast("weaponsMaker")`) sits on top of a tall pile of war money in front of his factory (`KIT.props.factory`, the missile chimneys puffing), cradling his grinning baby missile. "ninety-nine percent" → one bill hops off the top of the pile and marches into a color-flip funnel at the panel's edge; the Weapons Maker waves it goodbye with his cigar, and a tag on the pile reads "99%". "budget" → it walks out of the spout a medicine bill and strolls off toward panel 2. "PLUS" → parachuting medicine bills land on top of his pile: splat, splat, splat. "two hundred and seventy-two percent" → the medicine heap on top grows in three jumps. "returns." → it heaves him up through the top border of the panel: his hard hat punches through the frame, and he kisses his baby missile.

Sound: a thunk as the label lands; a low hum for the rumble; a boom on "erupts:" and a whoosh as the bills fly; a whoosh as the camera moves; squeaky footsteps for the leaving bill and a clank as the funnel flips it; a pop as it walks out; three splats on "PLUS"; a rising slide whistle as the heap grows; a thunk as the hat breaks through; a cash-register ding.

On screen: "$27.2 BILLION / YEAR" / "MILITARY CONTRACTORS" / the pile tag "99%". No: the factory sign is plain ("WEAPONS"), no company name. Why: the biggest objector gets paid first, so it stops objecting.

## Scene 4 · pharma-per-patient

- id: pharma-per-patient
- act: The money volcano
- transition_in: same form (no seam)
- key: on "joins": the Scientist with dollar-sign eyes hooking passers-by through the turnstile, a medicine bill popping out per click
- cue: "Instead of paying forty-one thousand"
- time: 46:20.5 to 46:29.7 (9.2 s)
- voiceover: "Instead of paying forty-one thousand dollars for phase two and three trials, the treaty pays Big Pharma for each patient that joins their trials."
- layer: B
- scene: Panel 2: the Scientist at her lab bench in a little lab with a turnstile at its door and a patient waiting at it. The turnstile costs the lab a barrow of money per patient, until the treaty turns it around.
- wishonia: PiP, neutral-smile + body-idle, then happy-smile + body-counting on "each"
- props: comic-strip, scientist, lab, turnstile, price-tag, wheelbarrow, papers-plain, papers-teal, parachute, human, cane-hook, clipboard
- status: outline

Moves: "Instead" → the camera moves onto panel 2: the Scientist (`KIT.cast("scientist")`) at her lab bench (`KIT.props.lab`) behind a shop window, a turnstile at the lab door, and one patient waiting at it (an everyday human in a cardigan). "forty-one thousand" → a price tag swings on the turnstile: "$41,000 PER PATIENT". "dollars" → the Scientist wheels up a barrow heaped with money and shovels the lot into the turnstile's coin slot. "trials," → the turnstile clicks once and the one patient walks through; the barrow is empty, and she mops her brow. "treaty" → a parachuting medicine bill drops in from the cloud and knocks the price tag off. "pays" → the turnstile spins around with a boing and now faces the other way. "Big Pharma" → the caption box fills: "BIG PHARMA". "each patient" → the next patient clicks through, and the turnstile spits a medicine bill into the Scientist's hand. Her eyes turn to dollar signs. "joins" → she grabs a vaudeville cane hook and hooks passers-by in off the street, faster and faster, a bill popping out per click, a tick on her clipboard per patient. "trials." → the turnstile spins so fast it smokes, and the patients come out the other side spinning like tops, into the lab.

Sound: a tick as the tag swings; a pat as the money is dumped; a click as the patient goes through and a huff as she mops her brow; a whoosh as the bill parachutes in; a boing as the turnstile turns around; a click and a cash-register ding per patient, faster on "joins"; a whirr as the turnstile spins.

On screen: "BIG PHARMA" / the tag "$41,000 PER PATIENT". No: the lab is a generic building, no company name; the patients are dizzy, never hurt. Why: drug makers make money from more patients in trials, so they go looking for them.

## Scene 5 · insurance-zero-claims

- id: insurance-zero-claims
- act: The money volcano
- transition_in: same form (no seam)
- key: on "problem).": the clerk bubble-wrapping YOU over the desk, the chart's line run off the bottom, the ribboned headstone being wheeled out
- cue: "Insurance Companies find"
- time: 46:29.7 to 46:43.2 (13.5 s)
- voiceover: "Insurance Companies find that healthy people file fewer claims than dead people (dead people file zero claims, which is the ideal customer except they also pay zero premiums, creating a revenue problem)."
- layer: B
- scene: Panel 3: the insurance clerk at a desk with two trays, CLAIMS and PREMIUMS, and a wall chart behind him. YOU is first in line; the Grim Reaper brings the next customer.
- wishonia: PiP, thinking-closed + body-thinking, then eyeroll-smile + body-hands-hips on "premiums,"
- props: comic-strip, human, desk, in-tray, chart, claim-form, papers-plain, reaper, hand-truck, headstone, rosette, bubble-wrap, crash-helmet
- status: outline

Moves: "Insurance" → the camera moves onto panel 3 and its caption box fills: "INSURANCE COMPANIES". The clerk sits at his desk with the two trays, CLAIMS and PREMIUMS, and a wall chart with a rising line. "healthy people" → YOU steps up first, healthy, chest light dark. "fewer claims" → he drops one thin claim form into CLAIMS and a fat bill into PREMIUMS; the clerk beams. "dead people" (first) → the Grim Reaper wheels the next customer up on a hand truck: a headstone (`KIT.props.headstone`). "zero claims," → the headstone drops nothing into CLAIMS; the clerk leans over the desk, delighted. "ideal customer" → he pins a rosette on it: "IDEAL CUSTOMER". "zero premiums," → he holds out the PREMIUMS tray; nothing; his smile drops off his face. "creating" → he shoves the hand truck back at the Reaper, who wheels his customer out of the panel, ribbon and all. "revenue" → the line on the wall chart dives and runs off the bottom of the chart. "problem)." → the clerk vaults the desk and bubble-wraps YOU from head to toe, then straps a crash helmet over his bowler.

Sound: a whoosh as the camera moves; a pat as the claim lands and a cash-register ding for the premium; squeaky hand-truck wheels; crickets when the headstone files nothing; a sparkle for the rosette; crickets again for the premium; squeaks as the hand truck leaves; a falling slide whistle as the chart dives; a whoosh as the clerk vaults; bubble-wrap pops.

On screen: "INSURANCE COMPANIES" / the trays "CLAIMS" and "PREMIUMS" / the rosette "IDEAL CUSTOMER". No: the insurer has no company name or logo. Why: insurers want living customers, so they join the side of health.

## Scene 6 · investor-lobby-force

- id: investor-lobby-force
- act: The money volcano
- transition_in: same form (no seam)
- key: after "lobbying": the Rich Human on top with the megaphone and the sign, the hill of bills on its feet and marching
- cue: "Investors receive two hundred"
- time: 46:43.2 to 46:58.6 (15.4 s)
- voiceover: "Investors receive two hundred and seventy-two percent returns that scale with every treaty expansion, turning them into the world's most aggressive pro-health and anti-war lobbying force, not a sentence anyone expected to write."
- layer: B
- scene: Panel 4: the Rich Human on a hill of medicine bills, wearing his "I PREFER LIVING" button, next to a treaty dial. The hill grows with the dial, then stands up and marches.
- wishonia: PiP, happy-smile + body-idle, then surprised-oh + body-open-palms on "expected"
- props: comic-strip, rich-human, papers-teal, parachute, flag, gauge, megaphone, protest-sign, germ, missile, button
- status: outline

Moves: "Investors" → the camera moves onto panel 4 and its caption box fills: "INVESTORS". The Rich Human (`KIT.cast("richHuman")`) sits on a small hill of medicine bills, hugging a stack, his "I PREFER LIVING" button from Part 17 on his chest. "two hundred and seventy-two percent" → a flag pops up on the hill: "272%". "every treaty expansion," → beside the hill a treaty dial (`KIT.props.gauge`) clicks 1%, 2%, 3%; with each click the hill doubles and lifts him higher. "aggressive" → he spits out his cigar, rolls up his sleeves and snatches a megaphone and a picket sign: "MORE TRIALS, FEWER WARS". "pro-health" → a germ (`KIT.props.germ`) creeps into the panel; one blast of the megaphone blows it out of the panel, spinning. "anti-war" → a grinning missile (`KIT.props.missile`) noses in; he whacks it with the picket sign, and it folds into a pretzel and droops. "lobbying" (the timings join "force" to the next word) → the hill stands up on hundreds of little legs: it was all bills, and they march behind him in step, each with a tiny picket sign. "expected" → he glances down at his button, then up at his own sign, and his monocle pops out and dangles on its string. Wishonia's eyebrows go up in her corner.

Sound: a whoosh as the camera moves; a pop for the flag; a click per dial step and a rising slide whistle as the hill grows; a pop as the cigar flies; a whoosh for the megaphone blast and a yelp from the germ; a thunk for the whack and a squeak as the missile folds; marching pats; a boing as the monocle pops out.

On screen: "INVESTORS" / the flag "272%" / the dial "1% 2% 3%" / the button "I PREFER LIVING" / the sign "MORE TRIALS, FEWER WARS". Why: the investors become the loudest lobby for the treaty, which surprises them most of all.

## Scene 7 · wiki-voters-hammock

- id: wiki-voters-hammock
- act: The money volcano
- transition_in: same form (no seam)
- key: after "free).": panel 7, YOU in the hammock, the tag flipped to "$0", the Reaper a heap of bones beside it
- cue: "Lobbyists keep the same job"
- time: 46:58.6 to 47:16.5 (17.9 s)
- voiceover: "Lobbyists keep the same job and salary, but their Wikipedia page no longer needs a "Controversies" section. Politicians get reelected by living voters (a revolutionary strategy). Regular humans enjoy not dying from stupid things (priceless, but also free)."
- layer: B
- scene: The last three panels, one after another: the Lobbyist with his encyclopedia page, the Politician with a line of living voters at a ballot box, and YOU in a hammock.
- wishonia: PiP, smirk-smile + body-idle, then happy-smile + body-hand-chest on "Regular"
- props: comic-strip, lobbyist, briefcase, sticker, envelope, encyclopedia-page, pencil, politician, ballot-box, banner, grandma, human, hammock, drink, reaper, coconut, bubble-wrap, crash-helmet, price-tag
- status: outline

Moves: "Lobbyists" → the camera moves onto panel 5 and its caption box fills: "LOBBYISTS". The Lobbyist (`KIT.cast("lobbyist")`) tiptoes in; his briefcase wears its teal sticker from Part 19 and leaks medicine bills. "salary," → a pay envelope parachutes into his glove; he sniffs it. "Wikipedia page" → a giant encyclopedia page unfolds beside him: "THE LOBBYIST", a mugshot of him in his mask, and a section headed "CONTROVERSIES". "Controversies" → the section is so long it unrolls off the bottom of the page and piles up on the floor; he takes a giant pencil and erases it in big strokes, eraser crumbs flying. "section." → the page is clean; he peels off his domino mask, and underneath is a pale, mask-shaped tan line. He smiles. "Politicians" → the camera moves onto panel 6 and its caption box fills: "POLITICIANS". The Politician stands at a podium beside a ballot box (`KIT.props.ballotBox`), his wide tie red. "reelected" → a "RE-ELECTED" banner drops over him. "living voters" → a line of living voters files up and drops ballots into the box, chest lights dark (healthy), Grandma (`KIT.cast("grandma")`) at the front in her curlers, waving her BUY BONDS poster. "revolutionary" → the box overflows; ballots fountain out and bury the Politician up to his teeth. "strategy)." → his tie, sticking up out of the pile, flips red, then blue, then teal, and stays teal. "Regular humans" → the camera moves onto panel 7 and its caption box fills: "REGULAR HUMANS". YOU, still bubble-wrapped and helmeted from panel 3, lies in a hammock tied to the panel's two side borders. "enjoy" → he sips a drink with a paper umbrella. "not dying" → the Grim Reaper climbs the panel's border above him, a coconut in his bony hands. "stupid things" → he drops it; it bounces off YOU's helmet and flies straight back up into the Reaper's skull. The Reaper collapses into a heap of bones, hood and scythe on top. "priceless," → a price tag swings from the hammock: "PRICELESS". "free)." → it flips over: "$0". The skull on top of the bone pile blinks.

Sound: a whoosh as the camera moves (three times); a cash-register ding for the envelope; a whoosh as the page unfolds; a falling slide whistle as the section unrolls, then two eraser scratches; a pop as the mask comes off; a thunk as the banner drops; ticks as the ballots drop in; a whoosh for the ballot fountain; two switch clicks and a ding as the tie flips; a whistle as the coconut falls, a boing off the helmet, a thunk on the skull and a clatter of bones; a squeak as the tag swings; a ding as it flips.

On screen: "LOBBYISTS" / "THE LOBBYIST" / "CONTROVERSIES" / "POLITICIANS" / "RE-ELECTED" / "VOTE" / "REGULAR HUMANS" / the tag "PRICELESS", then "$0". No: the encyclopedia page is generic, no logo; nobody bleeds, the Reaper just falls apart. Why: everyone left gets paid, including the viewer, and the only one out of work is the Reaper.

## Scene 8 · greed-arrow

- id: greed-arrow
- act: The turn
- transition_in: slide left
- key: on "each other.": the diseases flattened under the cast, the GREED arrow pointing at them, YOU at its tail, the MORAL HUMAN box still empty
- cue: "Nobody has to evolve morally"
- time: 47:16.5 to 47:23.7 (7.2 s)
- voiceover: "Nobody has to evolve morally. You just point everyone's greed at diseases instead of each other."
- layer: B
- scene: Across the top, a little evolution chart of four boxes. Below it, the big GREED arrow on its pivot post, the whole cast of the strip in a crowd on the left, grinning disease blobs on the right.
- wishonia: PiP, smirk-smile + body-idle, then happy-smile + body-point-right on "diseases"
- props: evolution-chart, greed-arrow, rich-human, weapons-maker, scientist, human, lobbyist, politician, disease-blob, dust-cloud, moral-human, halo
- status: outline

Moves: "Nobody" → the plate slides in: the chart, the arrow pointing at nobody, the crowd (the Rich Human, the Weapons Maker, the Scientist, the insurance clerk, the Lobbyist with his tan line, the Politician with his teal tie) and three disease blobs (`KIT.props.diseaseBlob`, different seeds and colors). "evolve" → the chart walks: a fish flops out of its box, becomes an ape, becomes a human. "morally." → the fourth box stays empty, and its label slams on: "MORAL HUMAN: NOT REQUIRED". "point" → the GREED arrow swings onto the crowd: every human gets dollar-sign eyes and turns on the one next to it. "greed" → they pile into a brawl: a dust cloud with fists, a top hat, a hard hat, a fedora and a flask flying out of it. "diseases" → YOU, still in his bubble wrap, waddles in and swings the arrow round to the disease blobs; it clanks into place. "instead" → the brawl cloud rolls along the arrow, across the floor and onto the blobs; their grins drop. "each other." → the dust clears: the blobs lie flat as rugs, x-eyed (`mood: "dead"`), and the cast stands on them, grinning, chest lights calm. after "other." → the Moral Human from money-defeats-morality falls out of the sky into the empty fourth box with a whistle and a splat, halo bent. The part ends on that frame.

Sound: three pops as the chart's creatures change; a rubber-stamp thunk for the label; a whoosh as the arrow swings and a cash-register ding for the dollar eyes; brawl hammering and a yelp; a whoosh and a clank as YOU swings the arrow; more brawl hammering as the cloud rolls; two splats as the blobs go flat; a falling slide whistle, a splat and a small ding for the Moral Human.

On screen: "MORAL HUMAN: NOT REQUIRED" / "GREED". No: the diseases are flattened, never torn apart. Why: the one-line summary of the five steps: aim the greed, skip the sermon.
