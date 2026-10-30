---
format: 1920x1080
duration: 2:30.5
message: "Nobody has to coordinate the plan: like a pencil, a cured disease can come from millions of strangers who never meet, steered only by two numbers on a Scoreboard and the papers."
arc: Title card (YOU's hair catches fire over the manual) → beside the lectern, YOU juggles the five steps until they flatten him → the pencil nobody can make (the Weapons Maker sharpens his missile and blows up the TV) → inside a wall map, the pencil's parts fly home and strangers who would brawl pass them back → the camera pulls out of the map: it hangs in an empty central office, and a spider moves into the chair → a cash register nobody runs rings out pencils → YOU, reading his paper, is buried by a day's goods without looking up → the same story for a cure: the den again, then the chain of strangers across the map until the data kills the sea monster and a jar drops over it → millions cooperate, and the spider has died in the chair waiting for orders → two numbers and a paper beat the committee, the charity and the plan → the machine needs only its switch, and YOU's hand stops just short of it
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 23, "But You Don't Need to Understand Any of That"
audio: index-manual.cbaf659d.mp3, 48:13.0 to 50:43.5
version: v3
---

# Part 23 storyboard: "But You Don't Need to Understand Any of That"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("pencil-on-tv: a bigger boom"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The part is a 1950s atomic-age instructional film. Layer A is the host's studio set (`KIT.studio`): Wishonia large at her navy lectern in front of the mustard wall, a guest on the free wall right of the lectern when a scene needs one. Layer B is three illustrated plates the camera travels over (`KIT.camera`), one framing per phrase: the TV den, the central office with its wall map, and a quiz-show stage. Wishonia is not in the plates; she is the voice. Money is green: plain papers are wages and the Super PAC's spray, medicine papers (cross seals) are the Rich Human's. Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Spine.** Two halves on the same sets. The pencil half: the TV den (pencil-on-tv), the inside of the wall map (pencil-parts-map, pencil-strangers), the pull-back out of the map into the empty office (empty-central-office) and the cash register on its desk (price-system-pencils). The cure half runs the same way: the den with the TV patched (cured-disease-jar), the inside of the map (the two cure-chain scenes), and the same pull-back into the same office, now under dust (millions-cooperated). The audience should feel the second half click into the shape of the first.

**The office-map plate** (six scenes, three author groups; the group of pencil-parts-map draws it first as one function the others copy). Plate units are the map's. The wall map is `KIT.props.worldMap({ w: 4200 })` (no title, no markers) standing on y 0 and centered on x 0, so its inner map runs x -1869 to 1869, y -2382 to -240, and a point (u, v) of the prop's 400 x 220 land space sits at (-1869 + 9.345 u, -2382 + 9.736 v). People on the map are `KIT.person` at scale 1.5 (about 270 tall), standing on the land like the figures on a 1950s pictorial map; framings inside the map are at scale 0.7 to 1.45. The stations (land space): the forest (42, 40) on the northwest coast of the left continent, the mine (121, 138) on the southern continent, the rubber grove (328, 115) on the long island south of the right continent; the middle of the sea (162, 128), where the pencil comes together and later the disease lounges; the chain of rowboats across the south Atlantic round (176, 152); Lagos (199, 108), Brussels (196, 52), Manila (352, 121), New York (116, 62), Delhi (284, 98) and Dhaka (306, 102), so close to Delhi that its worker and the Politician stand back to back. The office around the map is drawn at 7 times a person's scale: a cream wall, a rust baseboard and a slate floor at y 825; the desk (1050 wide, its top at y 300) centered on x 250 under the map, with the phone at x -80, the order pad at x 190, the rolled blueprint at x 390 and the brass cash register on its right end at x 630; the swivel chair at x -560 at the desk's left end, turned to us; the door centered on x 2700 with "CENTRAL OFFICE" on its frosted glass; the helmet hook at (3330, -150). The whole office is in frame at about scale 0.25, centered on (650, -573). Until empty-central-office, and again from cure-chain-lagos-to-new-york until millions-cooperated, the camera stays inside the map and its frame is never in shot.

**The cast.** YOU, the busy human in the bowler from Part 1's title card (`{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene): the reader on the title card, the juggler, the man with the newspaper in billions-a-day and the hand on the switch. The Weapons Maker, the Scientist, the Lobbyist (his briefcase with Part 19's teal cross sticker), the Loud Human and the Rich Human are their `KIT.cast` selves. The old woman in the den is an everyday human, not Grandma (Grandma died in Part 17): `{ tone: 3, outfit: "dress", hair: 1, hairColor: "#DEDAD2", color: 1, seed: 31, build: { hunch: 12 } }` (white hair, a stoop), the same options in both den scenes. The No Politician is Part 20's (`KIT.cast("politician")`, his tie teal since nra-letter-grade), still sooty from its jet pack, his hair still standing straight up. The Delhi politician is `KIT.cast("politician", { hair: 1, hairStyle: "flip", tieColor: KIT.C.med })`: the lantern jaw and the grin under a flip hairdo, Part 20's teal tie. The disease is `KIT.props.diseaseBlob({ seed: 5 })` in every scene, smug until it dies. Everyone else is an everyday human.

**Running gags.**
- The Weapons Maker can only make missiles. Asked for a pencil, he sharpens his baby missile and it blows up the TV (pencil-on-tv). Asked for a cure, he reaches for the sharpener again and is sat on (cured-disease-jar).
- The only one in the central office is a spider. It moves into the chair (empty-central-office), rolls past in it (price-system-pencils), dies at the desk waiting for orders and keeps grinning as a skeleton (millions-cooperated), and is the central plan on the quiz show (two-numbers-did-it).
- The five steps. YOU juggles them and they flatten him (juggling-five-steps); bolted onto the machine at the end they need only a switch, and YOU, bandaged, is spared building it (the-switch).

**Callbacks.** From Part 22: the manual (`KIT.props.manual`) on the title card and on YOU's toolbox. From Part 17: the bond (`KIT.props.bond({ text: "INCENTIVE ALIGNMENT BOND" })`) and the "1% TREATY: YES" campaign sign it set up for this part. From Part 5: the Super PAC, a rust canvas backpack with navy strap arms, a cream "SUPER PAC" patch and a war-red cape, drawn as Part 5's storyboard (step-4-super-pac) and its sketch module draw it; copy the new `../compositions/scenes/part-05/step-4-super-pac.html` once it is redrawn in that look, not the old file. From Part 20: the No Politician, whom the Super PAC's jet pack charred for voting no, limps past in cure-chain-delhi-dhaka, still sooty. From Part 14: the Optimitron (`KIT.props.optimitron`, its defaults). From Part 2: the Weapons Maker's smiling baby missile, and the bomb that leaves everyone charred and blinking. From Part 1 (papers-with-presidents): the walking paper whose oval portrait winks.

**Set up here.** The Scoreboard in two-numbers-did-it comes back in Part 24 (game-pool-rules) with a small YRS card and a /YR card beside its numbers; draw it as Part 24 describes it (a navy board with orange edging and a row of mustard bulbs, two flip-number windows of cream cards with navy numerals, on two posts) and leave those two cards off. the-switch ends with YOU's hand just short of the knife switch; Part 24's title card opens on its click.

**Held frame.** None. No line in this part is a death toll.

**Transitions.** The title card comes up from black and goes down to black; juggling-five-steps irises in on Wishonia's face. Host shot to plate, plate to host shot and plate to plate are cuts. pencil-strangers, empty-central-office and price-system-pencils continue pencil-parts-map's plate, and cure-chain-delhi-dhaka and millions-cooperated continue cure-chain-lagos-to-new-york's, each with no seam: it starts on the last scene's final frame and the camera keeps traveling. cured-disease-jar cuts back to the den the morning after pencil-on-tv; cure-chain-lagos-to-new-york cuts back into the map. the-switch irises out on her face, to black, so Part 24's title card comes up from black.

**Bans for this part.**
- The words on screen are the heading, the props' own lettering (the bond's title, the SUPER PAC patch, the Optimitron's HEALTH and WEALTH), "25¢", "CENTRAL OFFICE", "MP" on the helmet, "PASSED", "1% TREATY: YES", "YES" and "NO", "CURED", the Scoreboard's 63.3 and $2,138, the score cards' 0 and the switch's ON and OFF. No pins, place names, dotted lines, arrows or "?" on the map; no headline on the newspaper; no names on the podiums or numbers on the gears.
- The map is the kit's made-up world, with no flags or landmarks; the speech balloons are made-up squiggles and the hats plain shapes, not real alphabets or religious symbols.
- The camera never shows the wall map's frame from inside the map; the pull-backs in empty-central-office and millions-cooperated are the only times the map is seen as a map.

## Changes from v2

- Wishonia's office, the wall screen and her corner (PiP) are gone. She is on screen in three host shots: YOU juggles the five steps beside her lectern (juggling-five-steps), YOU is buried by a day's goods while he reads the paper (billions-a-day, new: "Your species does this..." is her verdict to the viewer), and the machine with its switch stands beside her at the end (the-switch, now a host shot). Everything else happens on three plates.
- The engraved map card with its pins, place names, dotted lines and "?" is gone. The map is a pictorial wall map: the camera stays inside it, where the places are stations a long way apart and the camera whips between them on each "does not know", and pulls back out of it twice to show the empty office it hangs in.
- The labels are gone and their jokes restaged: the OBJECTION sign (YOU glances at her), "dFDA" on the laptop (a teal cross on its screen), the THE PLAN clipboard (a blueprint unrolls itself, blank), the PRICE SYSTEM hopper (a cash register nobody runs rings out pencils), the LAST TIME panel (Part 20's No Politician limps past her, still sooty), the podium names and the gear numbers.
- The disease is the map's sea monster through the cure chain. The Dhaka worker's chest light going dark is the data, the monster flops belly up, and the specimen jar drops over it: the same jar the den's TV shows in cured-disease-jar.
- The human who reads the newspaper moves out of price-system-pencils into billions-a-day, and he is YOU; YOU is also the reader on the title card, the juggler and the hand on the switch.
- The title card is the period card; the reader's hair still catches fire.

## Scene 1 · you-dont-need-to-understand-title

- id: you-dont-need-to-understand-title
- act: Title
- transition_in: up from black (the parts are rendered on their own and joined)
- key: after "That.": the heading on the navy card under the emblem, and YOU at the right end of "UNDERSTAND", charred black and smoking, hair straight up, only his eyes blinking, the manual and his bowler lying smoking at his heels
- cue: "But You Don't Need to Understand"
- time: 48:13.0 to 48:15.6 (2.6 s)
- voiceover: "But You Don't Need to Understand Any of That."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem with its three running papers, and the heading under it. Heading lines, 16:9: "BUT YOU DON'T NEED TO" (style small) / "UNDERSTAND" / "ANY OF THAT" (small); 9:16: "BUT YOU DON'T" (small) / "NEED TO" (small) / "UNDERSTAND" / "ANY OF THAT" (small). The small gag: YOU stands on the baseline of "UNDERSTAND", just past its last letter (16:9; in 9:16 under the heading, above y 1450), facing the words, his nose deep in the open manual.
- props: title-card, person (YOU), manual, flames
- status: planned

Moves: "But" → the card comes up from black with the whole heading on it, the emblem's papers running round their orbits; YOU is already there, flipping pages fast. "Understand" → steam whistles out of his ears, and his bowler pops off on the jet. "Any" → his hair catches fire; he keeps reading. "of" → he flings the manual over his shoulder. "That." → it lands behind him with a thunk beside his bowler, and his flames go out in a puff: charred black and smoking, hair straight up, only his eyes blinking. after "That." → his shoulders drop with relief; the card goes down to black in its last quarter second.

Sound: the projector whirr from "But"; a whistle as the steam shoots on "Understand"; a fire whoosh on "Any"; a thunk as the manual lands on "That.".

On screen: "BUT YOU DON'T NEED TO UNDERSTAND ANY OF THAT".

Why: the narrator reads the heading, and the human who tried to understand it all is the part's argument in one picture.

## Scene 2 · juggling-five-steps

- id: juggling-five-steps
- act: The objection
- transition_in: iris in on her face
- key: on "coordinate": the five steps wheeling high over YOU beside the lectern, the Optimitron at the top of the arc, YOU sweating, knees buckling; Wishonia thinking
- cue: "You just read five steps"
- time: 48:15.6 to 48:31.8 (16.2 s)
- voiceover: "You just read five steps involving bonds, lobbyists, Super PACs, a decentralized F.D.A., and an appliance that optimizes government policy. The obvious objection: "Nobody can coordinate all of that.". Correct."
- layer: A, host
- scene: The host's set (`KIT.studio`). YOU on the free wall right of the lectern, juggling. The five steps, one by one: the bond, the Lobbyist (fedora, mask, trench coat, briefcase and all), the SUPER PAC, a laptop (`KIT.props.laptop`, a teal cross on its screen) and the Optimitron, which is much heavier than the rest.
- wishonia: big, neutral-smile + body-counting; thinking-small + body-thinking on "objection:"; smirk-closed + body-open-palms on "Correct."
- props: studio, lectern, person (YOU), bond, lobbyist, super-pac, laptop, optimitron, money (plain)
- status: planned

Moves: "You" → the iris opens on her face; she counts on her fingers; the camera pushes in slowly for the whole shot. "steps" → YOU strides in beside the lectern, grinning, and rolls up his sleeves. "bonds," → he tosses the bond up. "lobbyists," → the Lobbyist goes up after it, tiptoeing on thin air, his briefcase leaking plain papers. "PACs," → the SUPER PAC goes up, cape flapping. "F.D.A.," → the laptop goes up. "appliance" → the Optimitron goes up; every time it comes down, his knees buckle. "optimizes" → at the top of its arc its dials spin and a policy card pops out of its slot like toast. "objection:" → he glances at Wishonia, worried, still juggling. "coordinate" → he wobbles and sweats; the five things wheel faster and higher. "Correct." → everything comes down: the Optimitron lands on his head and flattens him like a pancake, only his blinking eyes showing under the bowler; the SUPER PAC, the laptop and the bond land on top. after "Correct." → the Lobbyist lands neatly on his toes on top of the pile and tips his fedora to her.

Sound: a whoosh as the bond goes up on "bonds,"; a boing as his knees buckle on "appliance"; a toaster pop for the card on "optimizes"; a splat on "Correct."; a squeak as the Lobbyist lands, after "Correct.".

On screen: the props' own lettering (the bond's title, SUPER PAC, HEALTH and WEALTH).

No: no "dFDA" on the laptop; the teal cross on its screen says it.

Why: she opens the argument to the viewer and agrees with the objection, and the picture shows why: nobody can juggle that.

## Scene 3 · pencil-on-tv

- id: pencil-on-tv
- act: The pencil
- transition_in: cut
- key: after "pencil." (last): the den in thinning smoke, the TV's screen cracked, the economist on it charred black and smoking, still holding up his pencil; the three beside the TV charred too, only their eyes blinking, the sharpener smoking
- cue: "Nobody coordinates a pencil either"
- time: 48:31.8 to 48:41.8 (10.0 s)
- voiceover: "Nobody coordinates a pencil either. One of your economists held up a pencil on television and said: "There's not a single person in the world who could make this pencil."
- layer: B, plate tv-den
- scene: One plate: a 1950s living room, a striped tan wallpaper over a rust baseboard and a slate floor. Left of middle, a console TV (`KIT.props.tvSet`) on its splayed legs, a low coffee table in front of it. Right of the TV stand three, turned to watch it: the Scientist, the old woman and the Weapons Maker, cradling his smiling baby missile; beside him, a big crank pencil sharpener clamped to a little side table. On the screen, an economist: an everyday human in a suit and a bow tie, long face, slick hair.
- props: tvSet, pencil, person (the economist, the old woman), scientist, weaponsMaker, missile, pencil sharpener, nuke
- status: planned

Moves: "Nobody" → close on the coffee table: a single yellow pencil pops up onto its eraser end and stands there by itself. "economists" → the camera pulls back: the TV beside it clicks on, and the economist on its screen smiles out, empty-handed. "held up" → the pencil hops off the table and dives into the screen, into his hand, and he holds it up. "television" → the camera pulls back further: the three stand beside the TV, watching. "said:" → the Weapons Maker, inspired, jams his baby missile nose first into the sharpener and cranks. "single" → the Scientist shakes her head. "person" → the old woman shakes hers. "world" → he pulls out the result: the missile sharpened to a graphite point, a pink eraser on its tail, still smiling. "make" → beaming, he holds it up exactly the way the economist holds his pencil. "this" → its tail lights and it shoots out of his hands into the TV. "pencil." (last) → a white flash, a boom and a small mushroom cloud over the TV. after "pencil." → the smoke clears: the screen cracked, the economist on it charred black and smoking, hair straight up, still holding up his pencil; the three beside it charred too; only their eyes blink.

Sound: a pop as the pencil stands up on "Nobody"; a switch click as the TV comes on on "economists"; a whirr as the sharpener cranks on "said:"; a ding as he holds it up on "make"; the boom on the last "pencil.".

On screen: no text; the pencil is the picture.

No: the economist is nobody in particular, not a likeness of the real one.

Why: an object everyone has held, and the one thing a human can make all by himself turns out to be a missile.

## Scene 4 · pencil-parts-map

- id: pencil-parts-map
- act: The pencil
- transition_in: cut
- key: on "mines": on the southern continent of the map, the miner popping up out of his shaft black with graphite from cap to boots, only his eyes blinking, the bare lead sticking out of the shaft mouth beside him, the engraved sea behind
- cue: "The wood comes from"
- time: 48:41.8 to 48:53.7 (11.8 s)
- voiceover: "The wood comes from a tree in Washington. The graphite comes from mines in South America. The rubber comes from Malaya. The brass ferrule, I haven't the slightest idea where it came from."
- layer: B, plate office-map
- scene: The office-map plate (see the header), inside the map, so the map is the whole world: cream continents in halftone on an engraved sea, no pins and no names. Drawn on it at the stations: a pine forest with one stump and a lumberjack in overalls and a plaid cap; a timber mine headframe over a shaft; a grove of rubber trees with tapping cups and a tapper in a shirt with a bucket. A yellow pencil, about as long as a person is tall, hovers over the middle of the sea.
- props: worldMap, pencil, person (lumberjack, miner, tapper), mine headframe, rubber tree, tapping cup
- status: planned

Moves: "The" → framing on the middle of the sea: the pencil hovers there. "wood" → its yellow wood peels off in two halves and flies northwest, and the camera travels with them to the forest, where the lumberjack stands by his stump. "Washington." → the halves slot into the stump and it grows back into a tall pine whose trunk is still painted yellow, six-sided; the lumberjack looks up at it and scratches his head. "graphite" → the camera swings south with the bare lead as it dives into the mine shaft. "mines" → the miner pops up out of the shaft, black with graphite from cap to boots, only his eyes blinking. "rubber" → the pink eraser bounces east across the sea, boing, boing. "Malaya." → it lands, plop, in a tapping cup on a rubber tree; the tapper peers in. "ferrule," → the little brass band spins up and wanders, hovering over one continent, then another. "slightest" → it stops over the middle of the sea and turns this way and that. "from." (last) → it drops into the sea with a plop; rings spread.

Sound: a whoosh as the wood flies on "wood"; a thunk as it slots in on "Washington."; a slide whistle down as the lead dives on "graphite"; a pop for the miner on "mines"; a boing on "rubber" and on "Malaya."; a splat for the plop on the last "from.".

On screen: no text.

Why: one pencil needs the whole planet.

## Scene 5 · pencil-strangers

- id: pencil-strangers
- act: The pencil
- transition_in: same plate (no seam)
- key: after "met.": close on one rowboat in a chain of rowboats: the dust cloud of the brawl with fists, feet and stars flying out of it, the eraser shooting out of the cloud toward the pencil, the boats behind still passing
- cue: "Literally thousands of people cooperated"
- time: 48:53.7 to 49:04.5 (10.8 s)
- voiceover: "Literally thousands of people cooperated to make this pencil. People who don't speak the same language, who practice different religions, who might hate one another if they ever met."
- layer: B, plate office-map
- scene: The same plate, still inside the map. Tiny strangers line every way between the stations and the middle of the sea, over the land and across the water in a chain of rowboats.
- props: worldMap, person (strangers), rowboat, net, speech balloon, plain hats, pencil, dust cloud, stars
- status: planned

Moves: "Literally" → the first frame is pencil-parts-map's last: rings on the sea. "thousands" → the camera pulls back: strangers pop up shoulder to shoulder along every way between the places, and a chain of rowboats across the sea; the nearest boat fishes the ferrule out with a net. "cooperated" → they pass the parts hand to hand and boat to boat toward the middle of the sea. "pencil." → the wood, the lead and the ferrule meet there and snap together; the eraser is still on its way along the chain from the rubber grove. "language," → speech balloons pop up over the handovers, each in a different made-up squiggle script. "religions," → hats pop onto the strangers, every one a different plain shape: a cone, a cube, a disk, a stack of rings. "hate" → the camera pushes in on one rowboat: a stranger in a cone hat and a stranger in a cube hat glare at each other over the eraser. "met." → a cartoon brawl: a dust cloud with fists, feet and stars flying out of it, the boat rocking. after "met." → the eraser shoots out of the cloud and lands on the end of the pencil with a pop: the pencil is whole. The cloud clears on the two brawlers, black-eyed, hats bent, back in their places and passing.

Sound: a pop as the strangers pop up on "thousands"; soft pats as the parts pass on "cooperated"; a click as the parts snap together on "pencil."; a boing as the hats pop on on "religions,"; a slam and a yelp for the brawl on "met."; a pop as the eraser lands, after "met.".

On screen: only the made-up squiggles in the balloons.

No: no counter; the crowd is the number.

Why: cooperation does not need agreement or friendship.

## Scene 6 · empty-central-office

- id: empty-central-office
- act: The pencil
- transition_in: same plate (no seam)
- key: after "given.": the whole empty office under its wall map: the handset dangling off the hook over the blank order pad, the nightstick on the floor, the cobweb across the door marked CENTRAL OFFICE, the empty helmet on its hook, and the spider in the swivel chair with its feet up on the desk
- cue: "No one sitting in a central office"
- time: 49:04.5 to 49:13.0 (8.5 s)
- voiceover: "No one sitting in a central office gave orders to these thousands of people. No military police enforced the orders that were not given.""
- layer: B, plate office-map
- scene: The same plate, pulled out of the map: the office it hangs in (see the header). On the desk: a rotary phone (`KIT.props.phone`), a blank order pad, a rolled blueprint and the brass cash register; the empty swivel chair stands at its left end, turned to us. At the left, the door (`KIT.props.door`, a frosted glass panel lettered "CENTRAL OFFICE"), and a hook by it with a white military police helmet ("MP" on its band) and a nightstick. Nobody in it. On the map, the tiny strangers keep passing.
- props: worldMap, desk, swivel chair, phone, order pad, blueprint, cash register, door, helmet, nightstick, tumbleweed, spider
- status: planned

Moves: "No" (first) → the camera pulls back out of the map: it is a wall map, and the whole world of strangers is on the back wall of an empty office. "sitting" → the swivel chair turns slowly round by itself, empty. "gave" → the phone rings. "orders" → it rings itself off the hook; the handset dangles on its cord and nobody picks it up; the order pad stays blank. "thousands" → a tumbleweed rolls across the floor. "military police" → the camera travels left to the door: the helmet and the nightstick on their hook, nobody under them. "enforced" → the nightstick slips off the hook, rolls across the floor and bonks the empty chair, which spins. "not" → a spider lowers itself from the top of the frame on its thread, "given." → spins a cobweb across the doorway, climbs into the chair and puts its feet up on the desk: the only one in the office.

Sound: the phone's bell on "gave" and on "orders"; a clank as the handset drops, just after "orders"; crickets under the tumbleweed on "thousands"; a thunk as the nightstick bonks on "enforced"; a slide whistle down as the spider lowers itself on "not".

On screen: "CENTRAL OFFICE" on the door; "MP" on the helmet.

No: no "Orders given: 0" card; the blank pad is the zero.

Why: nobody is in charge, and the pencil still got made.

## Scene 7 · price-system-pencils

- id: price-system-pencils
- act: The price system
- transition_in: same plate (no seam)
- key: on "pencils.": the brass cash register on the desk's corner ringing by itself, its flags up at "25¢", its drawer shot out full of pencils spilling over the desk; the spider in the chair beside it, staring; along the bottom of the map above, strangers with dollar-sign eyes
- cue: "A pencil costs twenty-five cents"
- time: 49:13.0 to 49:29.6 (16.6 s)
- voiceover: "A pencil costs twenty-five cents. Making one requires thousands of strangers across dozens of countries. Nobody planned it. Nobody runs it. Everyone involved just wanted money, and the price system turned their selfishness into pencils."
- layer: B, plate office-map
- scene: The same plate: the office and its wall map, the camera moving between the two.
- props: worldMap, pencil, priceTag, person (strangers), blueprint, swivel chair, spider, money (plain), cash register
- status: planned

Moves: "pencil" → the camera rises back into the map to the middle of the sea: the finished pencil. "cents." → a price tag swings onto it: "25¢". "strangers" → the camera pulls back over the map: the strangers along every way, the two brawlers still black-eyed. "dozens" → more strangers pop up on every coast and island. "planned" → the camera drops out of the map to the desk: the rolled blueprint unrolls itself across it: blank. "runs" → the spider rolls past on the swivel chair, feet up. "money," → back up on the map: every stranger holds out a hand, a plain paper walks into each one, and every pair of eyes rings up dollar signs. "price system" → down to the desk's corner: the cash register, nobody at it, rings by itself, and its flags pop up: "25¢". "selfishness" → it shakes, and its keys hammer away on their own. "pencils." → ka-ching: its drawer shoots out full of pencils, which spill across the desk and onto the spider.

Sound: a ding as the tag swings on on "cents."; a pop as the strangers multiply on "dozens"; a whoosh as the blueprint unrolls on "planned"; a squeak of chair wheels on "runs"; a cash register for the dollar eyes on "money,"; a typewriter rattle for the keys on "selfishness"; the cash register on "pencils.".

On screen: "25¢" on the tag and on the register's flags.

Why: the mechanism: selfish people plus prices make useful things, and nobody has to run it.

## Scene 8 · billions-a-day

- id: billions-a-day
- act: The price system
- transition_in: cut
- key: after "noticing.": beside the lectern, a heap of pencils, loaves, shoes and pill bottles taller than the lectern, YOU buried in it, only his open newspaper sticking out of the top, a page turning; Wishonia rolling her eyes, arms crossed
- cue: "Your species does this"
- time: 49:29.6 to 49:34.4 (4.8 s)
- voiceover: "Your species does this billions of times a day without noticing."
- layer: A, host
- scene: The host's set. On the free wall right of the lectern, YOU stands reading a newspaper held wide open in front of his face (its front page squiggle columns and a picture box).
- wishonia: big, smirk-smile + body-open-palms; eyeroll-closed + body-arms-crossed on "noticing."
- props: studio, lectern, person (YOU), newspaper, pencil, bread, shoe, pillBottle
- status: planned

Moves: "Your" → back at the lectern; she opens her palms toward him; the camera pushes in slowly. "species" → he turns a page. "billions" → goods start dropping in from above the frame around him, one, two, then a rain: pencils, loaves, shoes, pill bottles; the heap climbs past his ankles, his knees, his chest. "day" → it is up to his chin; he turns a page. "noticing." → the last of it buries him; only the newspaper sticks out of the top of the heap. after "noticing." → the newspaper turns a page; she rolls her eyes at the camera.

Sound: soft pats as the goods start falling on "billions" and on "day"; a slam as the heap buries him on "noticing.".

On screen: nothing but the set and the guest.

Why: her verdict to the viewer, on the viewer: the system works so well that nobody looks up.

## Scene 9 · cured-disease-jar

- id: cured-disease-jar
- act: The cured disease
- transition_in: cut
- key: on "cure": the taped-up TV with the specimen jar on its screen, the disease belly up inside and the CURED tag on its lid; beside it, the Scientist and the old woman sitting on the Weapons Maker, his fresh missile rolling away
- cue: "Now look at this cured disease"
- time: 49:34.4 to 49:40.8 (6.4 s)
- voiceover: "Now look at this cured disease. There is not a single person in the world who could cure it."
- layer: B, plate tv-den
- scene: The den from pencil-on-tv, the morning after: tape in an X across the TV's cracked screen, a bandage on its cabinet, one rabbit ear bent; the three scrubbed clean beside it, a few sooty smudges left; the sharpener on its table. On the screen: a specimen jar on a pedestal with the disease floating belly up inside (`KIT.props.diseaseBlob({ seed: 5, mood: "dead" })`) and a tag tied to the lid.
- props: tvSet, specimen jar, diseaseBlob, priceTag, scientist, person (the old woman), weaponsMaker, missile, pencil sharpener
- status: planned

Moves: "Now" → back in the den; the taped-up TV clicks on: static, then the picture. "disease." → the camera pushes in on the screen: the jar, the disease floating belly up inside, eyes crossed out, tongue out, and the tag on the lid swings: "CURED". "single" → the camera pulls back: the Scientist shakes her head. "person" → the old woman shakes hers. "world" → the Weapons Maker grins, lifts a fresh missile and steps toward the sharpener. "cure" → the Scientist and the old woman tackle him and sit on him. "it." → his hand pokes out from under them with a thumbs-up.

Sound: a switch click as the TV comes on on "Now"; a ding as the tag swings on "disease."; a slam and a yelp for the tackle on "cure".

On screen: "CURED" on the tag.

Why: the pencil swapped for a cure, so the same argument carries over, and the one man who works alone gets sat on.

## Scene 10 · cure-chain-lagos-to-new-york

- id: cure-chain-lagos-to-new-york
- act: The cured disease
- transition_in: cut
- key: after "campaign.": in New York, the Rich Human on his hill of bonds with dollar-sign eyes, a line of medicine papers marching off the hill to the "1% TREATY: YES" sign that has just sprung up; out at sea beyond the coast, the disease lounging, smug, buffing a claw
- cue: "The researcher in Lagos"
- time: 49:40.8 to 49:58.2 (17.4 s)
- voiceover: "The researcher in Lagos who found the cheaper trial design does not know the lobbyist in Brussels who passed the directive. The lobbyist does not know the nonprofit in Manila that recruited a million voters. The voters do not know the bondholder in New York whose greed funded the campaign."
- layer: B, plate office-map
- scene: Back inside the wall map: the same world, the strangers gone home, with one new thing in the middle of the sea: the disease, lounging like the sea monster on an old map, half again a person's height, smug, its claws steepled, a few wave lines round it. Six of the cast stand at their cities, far apart (see the header): the Scientist at Lagos at a lab bench under a palm, the Lobbyist at Brussels at a little desk, the Loud Human at Manila at a card table, the Rich Human at New York on a small hill of bonds, the Politician at Delhi at a voting console, a factory worker at Dhaka on a crate.
- props: worldMap, diseaseBlob, scientist, blueprint, priceTag, scissors, lobbyist, scroll, stamp, stampMark, loudHuman, card table, clipboard, person (voters), richHuman, bond, money (med), sign
- status: planned

Moves: "researcher" → framing on Lagos, the disease out at sea behind: the Scientist holds up a trial blueprint with a price tag on a string so long it trails off across the land. "cheaper" → she snips it with scissors; the tag drops away and only a stub is left. "know" (first) → the camera whips north to Brussels; she never looks up. "Brussels" → the Lobbyist at his desk with a scroll (`KIT.props.scroll`, squiggle lines), his briefcase at his feet. "passed" → he stamps it without reading it: "PASSED". "know" (second) → the camera whips east, across the whole map, to Manila. "Manila" → the Loud Human at a card table with a clipboard. "voters." → he yells through his megaphone head, and a flood of tiny voters pours out of the megaphone and spills over the islands like confetti. "know" (third) → the camera whips all the way back west to New York. "York" → the Rich Human on his hill of bonds: top hat, monocle, cigar. "greed" → his eyes ring up dollar signs. "funded" → a line of medicine papers marches off the hill. "campaign." → where they stop, a campaign sign springs up: "1% TREATY: YES". after "campaign." → out at sea, the disease buffs a claw on its chest, still smug.

Sound: a snip on "cheaper"; a stamp thump on "passed"; a pop as the voters pour out on "voters."; a whoosh for the long whip back west on the third "know"; a cash register for the dollar eyes on "greed"; a pop as the sign springs up on "campaign.".

On screen: "PASSED" / "1% TREATY: YES".

Why: the first half of the chain of strangers: each link is a long way from the next, and none of them looks up.

## Scene 11 · cure-chain-delhi-dhaka

- id: cure-chain-delhi-dhaka
- act: The cured disease
- transition_in: same plate (no seam)
- key: on "worked.": in the middle of the sea, the disease flopped over dead, eyes crossed out, tongue out, and the specimen jar coming down over it from above, the CURED tag swinging on its lid
- cue: "The bondholder does not know"
- time: 49:58.2 to 50:15.4 (17.2 s)
- voiceover: "The bondholder does not know the politician in Delhi who voted yes because the Super PAC funded her opponent last time she voted no. The politician does not know the factory worker in Dhaka whose clinical trial enrollment generated the data that proved the treatment worked."
- layer: B, plate office-map
- scene: The same plate, inside the map: Delhi and Dhaka, then the middle of the sea. The Politician's console has two big buttons, YES and NO (`KIT.props.yesButton`). Behind her, the No Politician (see The cast) limps along the coast. The factory worker is an everyday woman in overalls, her chest light blinking red, with the laptop from juggling-five-steps on her knees.
- props: worldMap, politician (the Delhi politician, the No Politician), yesButton, person (the factory worker), laptop, pill, wristband, diseaseBlob, specimen jar, priceTag
- status: planned

Moves: "bondholder" → the first frame is cure-chain-lagos-to-new-york's last. "know" (first) → the camera whips east to Delhi. "Delhi" → the Politician at her console. "yes" → she slams YES. "because" → behind her, Part 20's No Politician limps past along the coast, still sooty from the jet pack, his hair still standing straight up, a wisp of smoke rising off it. "Super PAC" → she glances over her shoulder at him and gulps. "no." → he turns his head and blinks at her; a puff of soot falls off him. "politician" (second) → she slams YES twice more, sweating, as he limps on out of the frame. "know" (second) → the camera eases a step east to Dhaka: the factory worker sits on her crate right behind the Politician, back to back, and neither turns round. "Dhaka" → the laptop on her knees, her chest light blinking red. "enrollment" → she taps the laptop, and a trial wristband snaps onto her wrist. "data" → she swallows a pill; her chest light flickers and goes dark. "proved" → the camera whips west to the middle of the sea: the disease clutches its chest. "worked." → it flops over dead, eyes crossed out, tongue out, and a specimen jar drops over it from above with its lid on; the tag on the lid swings: "CURED".

Sound: a whoosh for the whip on the first "know"; a thunk as she slams YES on "yes"; a squeak for each limping step from "because"; a pop as the soot puffs off him on "no."; a thunk for the YES slams on the second "politician"; a click as the wristband snaps on on "enrollment"; a yelp from the disease on "proved"; a splat as it flops and a ding as the tag swings on "worked.".

On screen: "YES" / "NO" / "CURED".

No: no data dots or dotted line from the worker to the sea; her chest light going dark is the data.

Why: the second half of the chain; the cure needs every link, and no link knows the others.

## Scene 12 · millions-cooperated

- id: millions-cooperated
- act: Nobody in charge
- transition_in: same plate (no seam)
- key: after "given.": the office under thick dust and its wall map crowded with tiny people: the spider's grinning skeleton in the swivel chair with its feet still up, the handset furry with dust, a bird nesting in the helmet, a baby spider spinning a second cobweb over the first
- cue: "Literally millions of people"
- time: 50:15.4 to 50:26.4 (11.0 s)
- voiceover: "Literally millions of people cooperated to cure this disease. No one sitting in a central office gave orders. No military police enforced the orders that were not given."
- layer: B, plate office-map
- scene: The same plate: the map, then the office, which has been empty a long time: dust on everything, cobwebs on the cash register, the pencils from price-system-pencils still spilled over the desk.
- props: worldMap, person (millions), specimen jar, priceTag, desk, swivel chair, phone, cash register, door, helmet, bird, spider (skeleton), spider (baby)
- status: planned

Moves: "Literally" → the first frame is cure-chain-delhi-dhaka's last. "millions" → the camera pulls back over the whole map, and tiny people pop up everywhere until every continent is crowded and the sea is full of rowboats; the six from the chain are lost among them. "cooperated" → they pass tiny papers hand to hand; the whole map seethes. "disease." → in the middle of the sea, the jar's CURED tag swings. "sitting" → the camera keeps pulling back, out of the map, into the same office, under thick dust. "central office" → in the swivel chair: the spider, now a grinning little skeleton, its feet still up on the desk. "orders." → the handset still dangles off the hook, furry with dust. "military police" → the helmet on its hook: a bird has nested in it and pokes its head out. "given." → a baby spider lowers itself and spins a second cobweb on top of the first.

Sound: a slide whistle up as the camera pulls back on "millions"; a pop as the people multiply, just after "millions"; a ding as the tag swings on "disease."; crickets in the office on "sitting"; a squeak from the bird on "police"; a slide whistle down for the baby spider on "given.".

On screen: "CENTRAL OFFICE" on the door; "MP" on the helmet.

Why: the same line as the pencil, now for a cure, and the office has been empty a long time.

## Scene 13 · two-numbers-did-it

- id: two-numbers-did-it
- act: Nobody in charge
- transition_in: cut
- key: after "done.": the lit Scoreboard rolling up and the paper bowing beside it, facing three contestant podiums all at 0: the committee flattened under its toppled reports, the charity's coin rolling off the front, the spider skeleton's jaw on the floor
- cue: "Two numbers on a Scoreboard and"
- time: 50:26.4 to 50:35.5 (9.0 s)
- voiceover: "Two numbers on a Scoreboard and pieces of paper with presidents on them did what no committee, no charity, and no central plan has ever done."
- layer: B, plate quiz-show
- scene: A third plate: a 1950s quiz-show stage, a rust curtain over a slate floor. Left: the Scoreboard (see Set up here), its windows showing 63.3 and $2,138. Right: three contestant podiums in a row, a flip score card on the front of each: behind the first, the committee (three suits at a long table behind a tall stack of reports); behind the second, a charity collector with a tin cup holding one coin; behind the third, the central plan: the swivel chair from the office with the spider's skeleton in it, feet up.
- props: scoreboard, money (plain), podium, person (the committee, the collector), reports, tin cup, coin, swivel chair, spider (skeleton)
- status: planned

Moves: "Two" → the Scoreboard rises on its posts; "numbers" → its bulbs light, and its windows, 63.3 and $2,138, start rolling upward and keep rolling. "paper" → a plain paper walks up beside it. "them" → its oval portrait winks, as in papers-with-presidents (Part 1). "did" → it takes a bow. "committee," → the camera travels right along the podiums: the committee behind its reports. "charity," → the collector rattles the cup; the one coin rattles in it. "central plan" → the swivel chair with the spider's skeleton, feet up. "ever" → the camera pulls back to the whole stage: all three score cards flip to 0. "done." → the committee's reports topple and flatten all three suits like pancakes, eyes blinking; the lone coin rolls off the charity's podium; the spider skeleton's jaw drops off and clatters on the floor. (The scene ends 0.6 s after "done.", so the payoff starts on the word.)

Sound: a slide whistle up as the Scoreboard rises on "Two"; a switch click for the bulbs on "numbers"; a sparkle for the wink on "them"; a tick as the cards flip on "ever"; a splat as the reports flatten the committee on "done.".

On screen: "63.3" / "$2,138" / "0" on each score card.

No: no YRS or /YR cards beside the numbers (Part 24 adds them).

Why: the two things that steer the plan, against everything that never did.

## Scene 14 · the-switch

- id: the-switch
- act: The switch
- transition_in: cut
- key: on "switch.": Wishonia presenting the knife switch on the machine beside her lectern, its handle up at OFF; YOU's hand reaching up from the bottom of the frame, stopped just short of it, a wisp of smoke off its fingertip; the five dark gears behind it with the five steps on their hubs
- cue: "The five steps above are the machinery"
- time: 50:35.5 to 50:43.5 (8.0 s)
- voiceover: "The five steps above are the machinery. You do not need to build the machinery. You need to turn it on. Here is the switch."
- layer: A, host
- scene: The host's set. On the free wall right of the lectern stands a dark machine: five big meshing gears (`KIT.props.gears({ n: 5, dark: true })`, no numbers), the five steps from juggling-five-steps bolted one to each hub (the bond, the Lobbyist riding his gear, the SUPER PAC, the laptop and the Optimitron). Under the gears, a big 1950s knife switch on a slate panel, its handle up at "OFF", "ON" below.
- wishonia: big, neutral-smile + body-presenting; smirk-smile + body-palms-down on "build"; happy-smile + body-point-right on "Here"; smirk-closed + body-point-right on "switch."
- props: studio, lectern, gears, bond, lobbyist, super-pac, laptop, optimitron, person (YOU), toolbox, hand truck, manual, knife switch
- status: planned

Moves: "The" → back at the lectern: the machine stands beside her, dark and still, dust on its gears; the camera pushes in slowly. "build" → YOU, his head bandaged and a little flatter than before, wheels in a toolbox on a hand truck with the manual on top, eyeing the machine with dread. "machinery." (second) → the toolbox rolls back out of the frame by itself, and YOU faints backward out of the bottom of the frame with relief. "turn" → the gears give one small twitch and puff dust; the Lobbyist wobbles on his hub, and the Optimitron's dials flicker. "Here" → she points at the knife switch. "switch." → YOU's hand comes up from the bottom of the frame toward the handle; a spark jumps to its fingertip; it jerks back down, smoking, then comes up again and stops just short of the handle. after "switch." → the film irises out on her face, to black.

Sound: a squeak of hand-truck wheels on "build"; a whoosh as the toolbox rolls off and a thunk as YOU faints on the second "machinery."; a clank as the gears twitch on "turn"; a zap as the spark jumps on "switch.".

On screen: "OFF" and "ON" on the switch.

Why: one action for the viewer instead of five steps, and the hand that stops short hands Part 24 its opening click.
