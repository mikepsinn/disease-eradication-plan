---
format: 1920x1080
duration: 1:26.8
message: "Once the treaty passes, the $27.2 billion a year pays every group that profited from war, so nobody has to become a better person."
arc: Title card (the emblem's papers stop running and lie back; the Reaper's jaw drops at "Nobody Dies") → at the lectern, money carries the treaty onto the scale, and the Moral Human, who weighs nothing, floats off it like a balloon → the money volcano erupts over a road, and the camera travels it stop by stop as each group gets paid: the Weapons Maker heaved up into the money cloud, the Scientist's turnstile turned round so patients queue to get in, the insurer bubble-wrapping YOU, the Rich Human's hill marching off, the Lobbyist's tan line, the Politician buried in ballots, waving his teal tie, YOU in the hammock while the Reaper's coconut comes back on him → the Moral Human comes down on the lectern → YOU swings the GREED arrow off the brawl onto the diseases
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 21, "Step 5: Enjoy"
audio: index-manual.cbaf659d.mp3, 45:56.9 to 47:23.7
version: v3
---

# Part 21 storyboard: "Step 5: Enjoy"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("insurance-zero-claims: hold the NO SALE flag longer"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The part is a 1950s atomic-age instructional film. Layer A is the host's studio set (`KIT.studio`): Wishonia large at her navy lectern, in front of the mustard wall and its spotlight pool. Layer B is two illustrated plates the camera travels over (`KIT.camera`), one framing per phrase: the volcano-road (the money volcano and the road of paydays at its foot) and the greed-field (the GREED arrow); Wishonia is not in them, she is the voice. Money is green, and its seal says what it buys: the money that carries the treaty is plain (`KIT.money("plain")`), the Weapons Maker's pile is war money, and everything the volcano pays out is medicine money (`KIT.money("med")`). Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Spine.** The money volcano and the road at its foot. It erupts medicine money in money-volcano; the bills pop little parachutes and hang over the whole road as a money cloud, and the paydays drop out of it. The camera travels right along the road, one stop per group, and every stop ends with its group paid: the factory (money-volcano), the lab (pharma-per-patient), the insurer's desk (insurance-zero-claims), the Rich Human's hill (investor-lobby-force), then the Lobbyist's encyclopedia page, the polling place and the hammock (wiki-voters-hammock). It is Part 2's road, straight this time: the money no longer goes round in a loop.

**Build (volcano-road).** One plate shared by five scenes in two author groups, so both draw to these numbers. Plate units: the road's back edge is y 0, and the road runs from y 0 to 170 across the whole plate in Part 2's colors with its dashed center line; the tan field runs back to a horizon at y -760, with a cream sky above. Everyone stands on the road at scale 1.5, feet at y 90. The volcano is centered on x 0, its base from x -950 to 950 just behind the road, its crater rim at y -1100. The stops are about 1250 apart (centers): the factory 1800, the lab 3050, the insurer 4300, the hill 5550, the encyclopedia page 6800, the polling place 8000, the palms 9200; the plate ends at x 10000. The money cloud: medicine bills under little cream parachutes, spread from x 400 to the end between y -1500 and -1150, each bobbing ±6 on a 2 s cycle of part time (`KIT.scene(ID).start` plus scene time), so it does not jump between scenes.

**Running gag: the Grim Reaper is the one who does not get paid.** `KIT.reaper()`, with Part 5's tally clipboard under his arm; in this part he never adds a mark. On the title card he reads "Nobody Dies" and his jaw drops off; from then on it is jammed back on crooked. In insurance-zero-claims he wheels a headstone up to the insurer and is sent away with it. In wiki-voters-hammock his coconut bounces off YOU's helmet back onto his skull, and he collapses into a heap of bones.

**Running gag: the Moral Human, not required.** A beanpole in a mustard shirt with a gold halo, hands clasped, eyes up (`KIT.person({ tone: 1, outfit: "shirt", kind: "twig", color: 3, mood: "smile" })`, the halo a gold ring drawn at `<!--head-end-->`). He stands on the scale beside the lectern in money-defeats-morality and weighs nothing: when the money slams the other pan down on "defeats", he floats up off his pan like a balloon and out of the top of the picture, and his halo stays behind; he drifts across the sky over the eruption in money-volcano, still rising; he comes back down onto the lectern in evolve-morally, without his halo.

**YOU.** The viewer is the busy human in the bowler from Part 1's title card, as in Parts 10, 12 and 13 (`{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene). He is the healthy customer whom the insurer bubble-wraps in insurance-zero-claims (from then on: clear bubble wrap over him from neck to shoes, and a mustard crash helmet strapped on over his bowler), the man in the hammock in wiki-voters-hammock, and the one who swings the GREED arrow in greed-arrow.

**The insurance clerk.** Part 8's CLAIMS clerk (fifty-nine-elevens), the man who stamped DENIED on a skeleton: the same options as Part 8's storyboard records for him (its sketch draws him as `{ tone: 0, outfit: "suit", hair: 2, color: 1, seed: 21 }`) and his green eyeshade. insurance-zero-claims, then the brawl in greed-arrow. The joke of his stop is the turn: the clerk who denied the dying now bubble-wraps the healthy.

**Callbacks.** From Part 2: the emblem's papers, which have run round their orbits since Part 2, stop on the title card; the war factory with its grinning missile chimneys and the Weapons Maker's baby missile (money-volcano); the road with its dashed line. From Part 5: the Reaper's tally clipboard and the Rich Human's "I PREFER LIVING" button. From Part 6 (better-loop): the halo that will not stay on a human, here a stack of old halos on the scale's post. From Part 20 (corrupt-the-corruption): the Politician's teal tie, which he arrives in. From the style bible (gag 2): the color-flip funnel takes one bill out of the Weapons Maker's pile. From Part 8 (fifty-nine-elevens): the CLAIMS clerk in his green eyeshade. From Part 17 (grandmas-war-bond): Grandma's grinning skeleton with her BUY BONDS poster (she died in 1987). From Part 19 (two-clients): the Lobbyist's briefcase with its teal cross sticker. From Parts 10, 12 and 13: YOU.

**Set up here.** The GREED arrow from greed-arrow comes back as the game board's spinner in greed-handles-it (Part 24): a long mustard arrow (`KIT.C.yellow`) with a navy outline and an orange edge, "GREED" in Oswald capitals on its shaft, pivoting at its middle on a riveted slate post. Draw it the same way there.

**Held frame.** None: the part states no death toll.

**Transitions.** The title card comes up from black and goes down to black; money-defeats-morality irises in on Wishonia's face. Cut from the set to the volcano road on "The". The five road scenes run on with no seam, the camera traveling. Cut to the set for evolve-morally, then to the greed-field; greed-arrow irises out on YOU's face to black, so Part 22's title card comes up from black.

**Bans for this part.**
- The words on screen are "TREATY" on the scroll, "$27.2 BILLION" / "A YEAR", the tags "99%", "$41,000", "PRICELESS" and "$0", the register's "NO SALE" flag, the flag "272%", the dial's window, the button, the picket sign, "CONTROVERSIES", Grandma's poster and "GREED". The road is a run of paydays the narrator names one by one, so no stop gets a caption or sign naming its group (the factory is `label: ""`).
- Wikipedia is said, never shown: the encyclopedia page is generic (no logo, globe or wordmark; squiggles for its text).

## Changes from v2

- Wishonia's office, the cream paper and her corner (PiP) are gone. She hosts from her lectern in two host shots: money-defeats-morality (the scale stands beside her lectern) and evolve-morally (new: the Moral Human comes back down onto her lectern on "morally.").
- The seven-panel comic strip, its caption boxes and number discs are gone. The money volcano stands at the end of a road, and the camera travels along it from stop to stop under one cloud of parachuting medicine money.
- Labels went with the strip, and their jokes are restaged as pictures: the banner is the title card's italic line, the "AS IS TRADITION" plaques are a stack of old halos on the scale's post, the CLAIMS and PREMIUMS trays are a paper spike and a cash register whose flag says "NO SALE", the rosette is a plain prize rosette, the "RE-ELECTED" banner is a glint off the Politician's teeth, and the evolution chart and "MORAL HUMAN: NOT REQUIRED" are the Moral Human landing on the lectern.
- The title card is the period card: the emblem's papers stop running for the first time and lie back on their orbits with cross seals, and the Reaper's jaw drops there, on "Nobody Dies".
- The Weapons Maker is heaved up into the money cloud instead of through a panel border; the hammock hangs between two palm trees, which is where the coconut comes from.

## Scene 1 · step-5-enjoy-title

- id: step-5-enjoy-title
- act: Title
- transition_in: up from black (the head of a reel)
- key: on "Dies*": "STEP 5" / "ENJOY" / the italic line on the navy card, the emblem's three papers lying back on their orbits with cross seals, the Grim Reaper beside the end of "Nobody Dies", his fingers on the "s", his jaw falling away
- cue: "Step five: Enjoy"
- time: 45:56.9 to 46:02.7 (5.8 s)
- voiceover: "Step five: Enjoy. *Everyone Gets Rich and Nobody Dies*"
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem with its three running war papers, and the heading under it. Heading lines, 16:9: "STEP 5" (style small) / "ENJOY" / "Everyone Gets Rich and Nobody Dies" (style italic, cue "Everyone"); 9:16: "STEP 5" (small) / "ENJOY" / "Everyone Gets Rich" / "and Nobody Dies" (both italic, cue "Everyone"). Spoken: "Step", "five:" (shows "5"), "Enjoy.". Two small gags (`gag`): the emblem's papers retire, and the Grim Reaper (`KIT.reaper()`) reads the italic line.
- props: title-card, money (war, then med), reaper, clipboard
- status: planned

Moves: "Step" → the card comes up from black, the emblem's papers running round their orbits as in every part since Part 2; "STEP" and "5" come in on their words. "Enjoy." → "ENJOY" slams in. after "Enjoy." → the three papers stop running for the first time in the film: their missile seals flip to crosses, and each sits down on its orbit, leans back and crosses its stick legs. "Everyone" → the italic line comes in under the heading. "Nobody" → the Grim Reaper rises up beside the right end of the line (pinned to "Dies"), scythe over his shoulder, and rests his bony fingers on the "s" to read it. "Dies*" → his jaw drops off and falls out of the bottom of the picture; a clatter from below, and he stares at the camera with no jaw until the card goes to black.

Sound: a projector whirr from "Step"; a sparkle as the seals flip, after "Enjoy."; a clank from below as the jaw lands, 0.6 s into "Dies*" (before the card goes to black).

On screen: "STEP 5" / "ENJOY" / "Everyone Gets Rich and Nobody Dies". Why: the narrator reads the heading and the subheading; the money stops running in circles at last, and the one creature the subheading is bad news for reads it first.

## Scene 2 · money-defeats-morality

- id: money-defeats-morality
- act: The treaty passes
- transition_in: iris in on her face
- key: after "morality,": the left pan slammed down under the plain bills and the treaty scroll, the right pan up and empty, the Moral Human's dangling feet drifting out of the top of the picture like a lost balloon, his halo left hanging in the air below them, the stack of old halos on the scale's post; Wishonia smirking beside it
- cue: "Your treaty passes because"
- time: 46:02.7 to 46:07.9 (5.2 s)
- voiceover: "Your treaty passes because money defeats morality, as is tradition."
- layer: A, host
- scene: The host's set (`KIT.studio`). On the free wall right of the lectern stands a tall brass balance scale (`KIT.props.balanceScale`, its pans about as high as the lectern's top). On its right pan stands the Moral Human, so light the beam stays level; its left pan is empty. Round the scale's center post, a stack of identical gold halos lies ringed like quoits, from the floor up: it is there from the first frame.
- wishonia: big, smirk-smile + body-presenting; smirk-closed + body-shrug on "tradition."
- props: studio, lectern, balance-scale, moral-human, halo, money (plain), scroll
- status: planned

Moves: "Your" → the iris opens on her face; she presents the scale, and the camera pushes in slowly for the whole shot. "treaty passes" → a line of plain bills marches in from the right edge carrying the rolled treaty scroll (`KIT.props.scroll`) over their heads, like ants with a leaf. "money" → they hop up onto the left pan one after another, the scroll on top. "defeats" → the left pan slams down and the right pan swings up; the Moral Human, who weighs nothing, lifts gently off it and floats up like a balloon, hands still clasped, eyes still up. "morality," → he drifts out of the top of the picture, and his halo, the only thing on him with any weight, stays hanging in the air where his head was. "as" → it drops, wobbling down like a coin. "tradition." → it rings onto the scale's post with a clink, on top of the stack of halos; Wishonia shrugs.

Sound: marching pats on "treaty"; a pop per bill onto the pan on "money"; a slam and a slow slide whistle up on "defeats"; a ding as the halo rings onto the post, on "tradition.".

On screen: "TREATY" on the scroll. No: no plaque on the halos (the stack says "as is tradition"). Why: the treaty passes the way everything passes, by the weight of the money, and the stack of halos says it happens every time.

## Scene 3 · money-volcano

- id: money-volcano
- act: The money volcano
- transition_in: cut
- key: after "returns.": the Weapons Maker heaved up into the money cloud on top of his tower of money (war bills below, medicine bills on top), his hard hat bonked into the parachuting bills, kissing his baby missile
- cue: "The twenty-seven point two billion"
- time: 46:07.9 to 46:20.5 (12.6 s)
- voiceover: "The twenty-seven point two billion dollars a year money volcano erupts: Military Contractors keep ninety-nine percent of their murder budget PLUS get two hundred and seventy-two percent returns."
- layer: B, plate volcano-road
- scene: The left end of the volcano road: the money volcano, a big faceted cone of rust and tan with a navy outline, smoke curling from its crater, the road running along in front of it and off to the right. The first stop: the Weapons Maker's factory (`KIT.props.factory`, no sign, its chimneys grinning missiles), the Weapons Maker (`KIT.cast("weaponsMaker")`) sitting on a tall pile of war money in front of its door, cradling his baby missile, and a color-flip funnel (`KIT.props.colorFlipFunnel`, no label) beside the pile.
- props: money-volcano, money (med, war), parachute, stamped number, factory, weapons-maker, missile, color-flip-funnel, price-tag, moral-human
- status: planned

Moves: "The" → cut to the plate, wide on the volcano rumbling quietly at the end of the road. "billion" → "$27.2 BILLION" stamps into the sky over it, and "A YEAR" under it on "year". "volcano" → it rumbles: smoke puffs from the crater and the ground shakes. "erupts:" → BOOM: a geyser of medicine bills shoots out of the crater, legs kicking; high up, each pops a little cream parachute, and the camera pulls back and tilts up as they spread across the sky to the right, a cloud of money drifting over the whole road. High over it all, the Moral Human drifts across the sky like a lost balloon, still rising. "Military Contractors" → the camera travels right along the road under the cloud to the factory: the Weapons Maker on his pile of war money, grinning round his cigar, rocking his baby missile. "ninety-nine percent" → a tag swings out on the pile, "99%"; one bill hops off the top and drops into the funnel, and he waves it goodbye with his cigar. "budget" → it walks out of the spout a medicine bill and strolls off along the road toward the next stop. "PLUS" → parachuting medicine bills land on top of his pile: splat, splat, splat. "two hundred" → more come down, and the medicine heap on top grows in three jumps, lifting him; the camera tilts up with him. "returns." → it heaves him up into the cloud: his hard hat bonks into the parachuting bills, and he sits up there among them, kissing his baby missile.

Sound: a stamp thump on "billion" and on "year"; a low hum on "volcano"; the boom on "erupts:" and a whoosh as the bills fly; a squeak as the bill hops off on "ninety-nine"; a clank as the funnel flips it on "budget"; two splats on "PLUS"; a slide whistle up on "hundred"; a thunk as the hat bonks the cloud on "returns.".

On screen: "$27.2 BILLION" / "A YEAR" / the tag "99%". Why: the biggest objector gets paid first, so it stops objecting, and it keeps almost everything.

## Scene 4 · pharma-per-patient

- id: pharma-per-patient
- act: The money volcano
- transition_in: same plate (no seam)
- key: on "joins": passers-by turning off the road on their own and queuing at the reversed turnstile, a medicine bill popping out of it into the Scientist's hand, dollar signs in her eyes, two patients already spinning into the lab
- cue: "Instead of paying forty-one thousand"
- time: 46:20.5 to 46:29.7 (9.2 s)
- voiceover: "Instead of paying forty-one thousand dollars for phase two and three trials, the treaty pays Big Pharma for each patient that joins their trials."
- layer: B, plate volcano-road
- scene: The second stop: the Scientist (`KIT.cast("scientist")`) behind her lab bench (`KIT.props.lab`), a turnstile at the front of her patch facing the road, and one patient (an everyday human in a cardigan) waiting at it.
- props: scientist, lab, turnstile, price-tag, wheelbarrow, money (plain, med), parachute, human (patients, passers-by), clipboard
- status: planned

Moves: "Instead" → the camera comes down out of the cloud and travels on with the strolling medicine bill to the lab. "forty-one thousand" → a price tag swings on the turnstile: "$41,000". "dollars" → the Scientist wheels up a barrow heaped with plain money and tips the lot into the turnstile's coin slot. "trials," → it clicks once and the one patient walks through; the barrow is empty, and she mops her brow. "treaty" → a parachuting medicine bill drops in from the cloud and knocks the tag off. "pays" → the turnstile spins round with a boing and now faces the other way. "each patient" → the next patient clicks through, and the turnstile spits a medicine bill into her hand; her eyes ring up dollar signs. "joins" → the camera pulls back to take in the road: passers-by see the bills popping out, turn off the road on their own and line up at the turnstile, faster and faster, a bill popping out per click into her hand, a tick on her clipboard per patient. "trials." → the turnstile spins so fast it smokes, and the patients come out the other side spinning like tops, into the lab.

Sound: a tick as the tag swings on "forty-one"; a pat as the money is tipped in on "dollars"; a click as the patient goes through on "trials,"; a whoosh as the bill knocks the tag off on "treaty"; a boing as the turnstile turns round on "pays"; a cash-register ding on "each"; three clicks on "joins"; a whirr as it spins up, from "their".

On screen: the tag "$41,000". No: nobody drags the patients in (the reversed turnstile is the whole incentive). Why: drug makers make money from every patient in a trial, so they go out and find them.

## Scene 5 · insurance-zero-claims

- id: insurance-zero-claims
- act: The money volcano
- transition_in: same plate (no seam)
- key: on "problem).": the clerk vaulting his desk to bubble-wrap YOU, the easel chart's line run off the bottom and down its leg, the Grim Reaper wheeling the rosetted headstone away on his hand truck, "NO SALE" still up on the register
- cue: "Insurance Companies find"
- time: 46:29.7 to 46:43.2 (13.5 s)
- voiceover: "Insurance Companies find that healthy people file fewer claims than dead people (dead people file zero claims, which is the ideal customer except they also pay zero premiums, creating a revenue problem)."
- layer: B, plate volcano-road
- scene: The third stop: the insurance clerk (Part 8's CLAIMS clerk, see the cast note) at a desk standing out on the field, a paper spike at its left end and a 1950s cash register at its right, and behind him an easel chart with a line rising across it. YOU is first in line.
- props: human (the clerk, YOU), desk, paper-spike, claim-form, cash-register, easel-chart, money (plain), reaper, clipboard, hand-truck, headstone, rosette, bubble-wrap, crash-helmet
- status: planned

Moves: "Insurance" → the camera travels on to the insurer's desk. "healthy people" → YOU steps up, healthy, chest light dark. "fewer claims" → he spikes one thin claim form and feeds a fat bill into the register: ka-ching; the clerk beams. "dead people" (first) → the Grim Reaper, his jaw jammed back on crooked, wheels the next customer up on a hand truck: a headstone (`KIT.props.headstone`); YOU steps aside. "zero claims," → nothing goes on the spike; the clerk leans over the desk, delighted. "ideal customer" → he pins a big prize rosette on the headstone. "zero premiums," → he rings it up: the register's drawer slides open empty, and its flag pops up, "NO SALE"; his smile slides off his face. "creating" → he shoves the hand truck back at the Reaper, who wheels his customer away, rosette and all. "revenue" → the line on the chart dives, runs off the bottom of the chart and down the easel's leg into the grass. "problem)." → the clerk vaults the desk and bubble-wraps YOU from neck to shoes. after "problem)." → he straps a crash helmet on over YOU's bowler and pats it.

Sound: a pat as the claim goes on the spike on "fewer" and a cash-register ding for the bill on "claims"; squeaky hand-truck wheels on "dead"; crickets on "zero"; a sparkle for the rosette on "ideal"; a thunk as "NO SALE" pops up on "premiums,"; a slide whistle down as the line dives on "revenue"; a whoosh as he vaults and bubble-wrap pops on "problem).".

On screen: "NO SALE" on the register's flag. No: no words on the rosette, and no DENIED stamp at this desk (he denies nobody here). Why: an insurer earns from the living, so the clerk who stamped DENIED on the dying in Part 8 joins the side of health, starting with YOU.

## Scene 6 · investor-lobby-force

- id: investor-lobby-force
- act: The money volcano
- transition_in: same plate (no seam)
- key: on "expected": the Rich Human riding his hill of medicine bills as it marches along the road on hundreds of little legs, megaphone in one hand and picket sign in the other, his monocle popped out and dangling, the folded missile drooping behind
- cue: "Investors receive two hundred"
- time: 46:43.2 to 46:58.6 (15.4 s)
- voiceover: "Investors receive two hundred and seventy-two percent returns that scale with every treaty expansion, turning them into the world's most aggressive pro-health and anti-war lobbying force, not a sentence anyone expected to write."
- layer: B, plate volcano-road
- scene: The fourth stop: the Rich Human (`KIT.cast("richHuman")`) sitting on a small hill of medicine bills, hugging a stack, his "I PREFER LIVING" button from Part 5 on his lapel; beside the hill, a treaty dial on a post (`KIT.props.gauge`, its window "1%").
- props: rich-human, button, money (med), flag, gauge, megaphone, picket-sign, germ, missile
- status: planned

Moves: "Investors" → the camera travels on to the hill. "seventy-two" → a little flag pops up on top of the hill: "272%". "every treaty expansion," → the dial clicks 1%, 2%, 3% in its window, and with each click the hill doubles under him and lifts him higher; the camera pulls back and tilts up with him. "aggressive" → he spits out his cigar, rolls up his sleeves and snatches up a megaphone and a picket sign: "MORE TRIALS, FEWER WARS". "pro-health" → a germ (`KIT.props.germ`) creeps up the hill; one blast of the megaphone blows it spinning out of the picture. "anti-war" → a grinning missile (`KIT.props.missile`) noses in; he whacks it with the sign, and it folds into a pretzel and droops. "lobbying" → the hill stands up on hundreds of little legs (it was bills all the way down) and marches off along the road in step, each bill with a tiny picket sign, carrying him on top; the camera travels with it. "expected" → he glances down at his button, then up at his own sign, and his monocle pops out and dangles on its string.

Sound: a pop for the flag on "seventy-two"; a click per dial step on "every", "treaty" and "expansion," and a slide whistle up as the hill grows; a pop as the cigar flies on "aggressive"; a whoosh for the megaphone blast and a yelp from the germ on "pro-health"; a thunk for the whack and a squeak as the missile folds on "anti-war"; marching pats on "lobbying"; a boing as the monocle pops out on "expected".

On screen: the flag "272%" / the dial's window "1%", "2%", "3%" / the button "I PREFER LIVING" / the sign "MORE TRIALS, FEWER WARS". Why: the investors become the loudest lobby for the treaty, which surprises them most of all.

## Scene 7 · wiki-voters-hammock

- id: wiki-voters-hammock
- act: The money volcano
- transition_in: same plate (no seam)
- key: after "free).": YOU in his bubble wrap and crash helmet in the hammock between the palms, drink in hand, the tag flipped to "$0", the Grim Reaper a heap of bones at the foot of the palm, his skull on top blinking
- cue: "Lobbyists keep the same job"
- time: 46:58.6 to 47:16.5 (17.9 s)
- voiceover: "Lobbyists keep the same job and salary, but their Wikipedia page no longer needs a "Controversies" section. Politicians get reelected by living voters (a revolutionary strategy). Regular humans enjoy not dying from stupid things (priceless, but also free)."
- layer: B, plate volcano-road
- scene: The last three stops. The Lobbyist's stop: open ground where a giant encyclopedia page will unfold like a billboard. The polling place: the Politician (`KIT.cast("politician")`) at a little podium beside a ballot box (`KIT.props.ballotBox`), in the teal tie Part 20 gave him (`tieColor: KIT.C.med`). The end of the road: a hammock slung between two palm trees, and YOU in it.
- props: lobbyist, briefcase, sticker, envelope, parachute, encyclopedia-page, pencil, politician, podium, ballot-box, ballots, grandma (skeleton), poster, human (voters, YOU), hammock, palm trees, drink, coconut, reaper, clipboard, bubble-wrap, crash-helmet, price-tag
- status: planned

Moves: "Lobbyists" → the camera travels on as the marching hill passes out of the picture: the Lobbyist (`KIT.cast("lobbyist")`) tiptoes along the road, his briefcase wearing its teal cross sticker from Part 19 and leaking medicine bills. "salary," → a pay envelope parachutes down out of the cloud into his glove; he sniffs it. "Wikipedia page" → a giant encyclopedia page unfolds behind him like a billboard: his mugshot in his mask at the top, columns of squiggles under it. "Controversies" → a section headed "CONTROVERSIES" scrolls down the page, runs off its bottom and piles up on the ground; he takes a giant pencil and erases it in big strokes, eraser crumbs flying. "section." → the page is clean; he peels off his domino mask, and underneath is a pale, mask-shaped tan line; he smiles. "Politicians" → the camera travels on to the polling place. "reelected" → the Politician grins, and a glint pings off his teeth. "living voters" → a line of living voters files up and drops ballots into the box, chest lights dark; at the back of the line, Grandma's skeleton from Part 17 (`KIT.cast("grandma", { skeleton: true })`, curlers, cat-eye glasses and apron still on) waves her BUY BONDS poster. after "voters" → she reaches the box last, and its slot snaps shut on her ballot (living voters only); she shrugs, and her jaw clacks. "revolutionary" → the box overflows; ballots fountain out of it and bury the Politician, grin and all. "strategy)." → his teal tie springs up out of the pile and waves, like a hand out of a snowdrift. "Regular humans" → the camera travels on to the end of the road: YOU, still bubble-wrapped and helmeted, lies in a hammock between two palm trees. "enjoy" → he sips a drink with a paper umbrella. "not dying" → the Grim Reaper shins up the palm above him, a coconut in his bony hands. "stupid things" → he drops it; it bounces off YOU's helmet and flies straight back up into the Reaper's skull, and the Reaper drops out of the palm into a heap of bones at its foot, hood and scythe on top. "(priceless," → a price tag swings out from the hammock: "PRICELESS". "free)." → it flips over: "$0". after "free)." → the skull on top of the bone pile blinks.

Sound: a cash-register ding for the envelope on "salary,"; a whoosh as the page unfolds on "Wikipedia"; a slide whistle down as the section unrolls on "Controversies", then two eraser scratches; a pop as the mask comes off on "section."; a sparkle off his teeth on "reelected"; ticks as the ballots drop in on "living"; a click as the slot snaps shut on Grandma (after "voters"); a whoosh for the fountain on "revolutionary"; a boing as the tie springs up on "strategy)."; a slide whistle down as the coconut falls on "stupid"; a boing off the helmet, a thunk on the skull and a clatter of bones on "things"; a squeak as the tag swings out; a ding as it flips on "free).".

On screen: "CONTROVERSIES" / "BUY BONDS" on Grandma's poster / the tag "PRICELESS", then "$0". No: no tie flip (his tie has been teal since Part 20). Why: everyone left gets paid, the viewer included, and the only one out of work is the Reaper.

## Scene 8 · evolve-morally

- id: evolve-morally
- act: The turn
- transition_in: cut
- key: on "morally.": the Moral Human sprawled on his back across the lectern's reading top, arms and legs dangling, a ring of dizzy stars circling his head where his halo used to be; Wishonia side-eyeing the camera over him
- cue: "Nobody has to evolve morally"
- time: 47:16.5 to 47:18.9 (2.4 s)
- voiceover: "Nobody has to evolve morally."
- layer: A, host
- scene: The host's set, nothing on the lectern. The Moral Human, who floated off the scale in money-defeats-morality, is on his way back down.
- wishonia: big, smirk-smile + body-hands-hips; sideeye-closed + body-idle on "morally."
- props: studio, lectern, moral-human, dizzy-stars
- status: planned

Moves: "Nobody" → back at the lectern, hands on hips; a falling whistle from above the picture. "evolve" → the Moral Human drops into the picture and lands flat on his back across the lectern's reading top, splat, arms and legs dangling over its edges, no halo. "morally." → a ring of little dizzy stars starts circling his head where his halo used to be; Wishonia side-eyes the camera and does not look down.

Sound: a falling slide whistle on "Nobody"; a splat on "evolve"; a sparkle as the stars start on "morally.".

On screen: nothing but the set. Why: the verdict in one picture: the Moral Human was never required, and he comes back down to prove it.

## Scene 9 · greed-arrow

- id: greed-arrow
- act: The turn
- transition_in: cut
- key: after "other.": the GREED arrow pointing at the disease blobs flattened like rugs, the cast standing on them grinning, YOU in his bubble wrap at the arrow's tail
- cue: "You just point everyone's greed"
- time: 47:18.9 to 47:23.7 (4.8 s)
- voiceover: "You just point everyone's greed at diseases instead of each other."
- layer: B, plate greed-field
- scene: A second plate: a plain tan field under a cream sky. In the middle, the GREED arrow on its riveted slate post (see Set up here). On the left, the cast of the road in one brawling dust cloud (the Rich Human, the Weapons Maker, the Scientist, the clerk, the Lobbyist, the Politician): fists and shoes poke out of it. On the right, three smug disease blobs (`KIT.props.diseaseBlob`, different seeds and colors). YOU, bubble-wrapped and helmeted, beside the arrow's tail.
- props: greed-arrow, post, dust-cloud, rich-human, weapons-maker, scientist, human (the clerk, YOU), lobbyist, politician, disease-blob, bubble-wrap, crash-helmet
- status: planned

Moves: "You" → cut to the field: the arrow points left at the brawl. "point" → YOU waddles up in his bubble wrap and puts his shoulder to the arrow's tail. "greed" → a top hat, a hard hat, a fedora and a flask fly up out of the brawl. "diseases" → he swings the arrow round to the blobs, and it clanks into place; the camera pans right with its tip; the blobs' grins falter. "instead" → the brawl cloud rolls across the field along the arrow and onto the blobs. "each other." → the dust clears: the blobs lie flat as rugs, x-eyed, and the cast stands on them, grinning, dollar signs in their eyes, chest lights calm. after "other." → the camera pulls back to take in the arrow, YOU and the flattened blobs, and the film irises out on YOU's face, to black.

Sound: brawl hammering from "You"; a huff as YOU pushes on "point"; a whoosh and a clank as the arrow swings on "diseases"; hammering again as the cloud rolls on "instead"; two splats as the blobs go flat on "each".

On screen: "GREED" on the arrow. Why: the five steps in one move: aim the greed, skip the sermon.
