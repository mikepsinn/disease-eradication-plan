---
format: 1920x1080
duration: 3:19.1
message: "War plus cybercrime is a $13.2 trillion destructive economy growing faster than the productive one; at this rate it passes the share that collapsed the Soviet Union, unless the treaty defunds the loop that feeds it."
arc: Title card, where the Weapons Maker lights the fuse on the Earth at the heart of the atom → at the lectern, the official murder budget is only the small cart → off the books, cybercrime is the war that pays better → the destroying stack outgrows the making one, and Wishonia calls it Tuesday → on main street, building stops making sense, and the town becomes a failed state → the gasoline basement, and Wishonia sips her coffee beside her own lit fuse → 25% by 2033, at the Soviet Union's grave, and the fuse is down to its last curl → the loop → the treaty switches the money off the loop, the papers come out with the cross seal, and the fuse on the lectern goes out
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 11, "Your Civilization Has a Countdown"
audio: index-manual.cbaf659d.mp3, 19:14.9 to 22:34.0
version: v3
---

# Part 11 storyboard: "Your Civilization Has a Countdown"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`, the 1950s atomic-age instructional film. Layer A is the host's set (`KIT.studio`): Wishonia at her lectern, talking to the viewer. Layer B is a plate: one large illustration on a plain field, drawn once, that the camera travels over (`KIT.camera`), one framing per phrase; Wishonia is only the voice there. Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot. The money is money green, and its seal says what it buys: "war papers" carry the missile seal (`KIT.money("war")`), "medicine papers" the cross seal (`KIT.money("med")`), "plain papers" none (`KIT.money("plain")`).

**Cast.** The Masked Crook (`KIT.cast("lobbyist")`: fedora, domino mask, trench coat, gloves; in this part the cybercriminal, with a laptop, and the warlord), the Weapons Maker (`KIT.cast("weaponsMaker")`, cradling his grinning baby missile), the Politician (`KIT.cast("politician")`) and the Scientist (`KIT.cast("scientist")`). Five everyday humans, drawn with these exact options so each looks the same every time:
- The Builder: `KIT.person({ tone: 1, outfit: "overalls", color: 0, seed: 7, mood: "eager" })`, with a hammer. destroy-beats-make, build-or-steal, production-irrational (unburnt in the crater, then masked), loop-not-line-item (masked at station 4), defund-the-loop (unmasked).
- The Watcher: `KIT.person({ tone: 0, outfit: "suit", color: 1, seed: 3, mood: "smug" })`, with a teacup; charred (`charred: true`) from the boom in neighbors-house through try-all-three. He is the only human this part chars.
- The Hut Builder: `KIT.person({ tone: 3, hair: 1, outfit: "dress", color: 2, seed: 5, mood: "eager" })`. failed-states.
- The Kid: `KIT.person({ tone: 2, outfit: "shirt", color: 3, seed: 11, mood: "eager", build: { hs: 1.3, legs: 0.6, th: 0.75, neck: 0.5 } })` at 0.7 of the scene's human scale, with `mask: true` from "crime." in thats-homework until he takes it off in defund-the-loop.
- The patient on the gurney: any everyday human, a skeleton (`KIT.xray`) from "ransomware." in crypto-afternoon.

**Spine.** The war papers, off the books. They walk out of a bank, through a WiFi pole and out of the Crook's laptop with the missile seal (cybercrime-10-trillion), fill the bigger cart, pour into one stack that outgrows the Builder's crates (destroy-beats-make), weigh down the Crook's end of the seesaw (build-or-steal), climb the gauge as a vine (no-plan) and run round the loop (loop-not-line-item), until the treaty drops into the loop as a railroad switch and sends them through the color-flip funnel, and they come out as medicine papers (defund-the-loop).

**Running gag: the fuse.** Your civilization is a cartoon bomb: a small Earth (`KIT.props.earthGlobe`) with a bomb's navy screw collar and a lit fuse (the cord and spark of `KIT.props.bomb`). On the title card it is the nucleus of the film's atom, and the Weapons Maker lights it with his cigar. After that it sits on Wishonia's lectern, beside her mug, in every host shot, burning down a fuse that rises off the collar, makes one small curl and runs off up the wall: nearly all of it in official-murder-budget, about 60% in considered-tuesday, about a third in once-it-starts (the spark just short of the curl), round the curl in this-is-a-loop, and a stub in you-defund-it, where it goes out after the part's last word. Each host shot shows it visibly shorter than the last. Nobody ever looks at it, Wishonia included. The plates do not show it.

**Callbacks.** From Part 10: the shopping cart heaped with warheads (warheads-in-the-cart), its tag now reading the bill Wishonia's register rang up (cash-register) as "$2.72 TRILLION / YEAR" (official-murder-budget); the 1913 printing press (nothing-papers) and the shrinking paycheck (paycheck-shrinks) as stations 1 and 3 of the loop; and the color-flip funnel, which Part 10 ran backwards (submarine-on-land) and defund-the-loop runs forwards. From Part 2 (money-loop): the shape of the money loop (this part's loop is the same kind of road). From Part 4 (war-supply-chain): the 1ST rosette from the hub of the war wheel, pinned on the Soviet binder in no-plan. Inside the part: the clock that spins in crypto-afternoon jumps again in build-or-steal; the tank flattened in war-through-wifi comes back flatter in thats-homework; the war-paper stack from destroy-beats-make is station 5 of the loop; the Builder's domino mask (production-irrational, loop-not-line-item, off in defund-the-loop); the Watcher's teacup sip (neighbors-house), which Wishonia does with her mug beside her own lit fuse (once-it-starts); the charred Watcher, still holding the teacup (try-all-three); the Kid's mask (thats-homework, off in defund-the-loop); the factory's SUCCESS sign (production-irrational, back up in defund-the-loop); the needle on 11.5, where the Crook's slice was (destroy-beats-make, 25-percent-by-2033).

**Set up here.** The part's last plate ends with medicine papers filing up to the lab bench; Part 12 opens with four of them marching along Wishonia's lectern (smoke-detector-by-mail). The Earth-bomb on the lectern goes out in you-defund-it, so later host shots do not have it.

**Held frame.** None: the part states no death toll.

**Transitions.** The title card cuts in (parts are rendered on their own). A change between a host shot and a plate, or from one plate to another, is a cut. Scenes on one plate continue with no seam: each starts on the last one's final frame and the camera keeps traveling. try-all-three cuts back from the reaction cut once-it-starts to the two-houses plate where the camera would have got to: the cloud has thinned away. you-defund-it cuts to Part 12's title card.

**Bans for this part.**
- Countries are words on signs only (no flags, emblems, leaders or national costumes); the cybercriminal and the warlord are the Masked Crook.
- The TED Talk is a round rug and a headset microphone with no logo or red letters.

## Changes from v2

- The office, the cream diagram paper and Wishonia's corner are gone: five host shots at the lectern (official-murder-budget, considered-tuesday, the reaction cuts once-it-starts and this-is-a-loop, you-defund-it) and six plates the camera travels over (off-the-books, the-stacks, main-street, two-houses, the-gauge, the-loop).
- The fuse left the corner of the screen for Wishonia's lectern: it is the nucleus of the atom on the title card and burns down through the five host shots, going out on the last word.
- Two reaction cuts break up the 145 s of plates between considered-tuesday and you-defund-it and check in on the fuse: once-it-starts (after the Watcher's house goes up, Wishonia sips beside her own lit fuse) and this-is-a-loop (after the Soviet Union loses, the spark goes round the fuse's curl).
- Charring is spent once, on the Watcher. In production-irrational the missile takes the factory clean away and leaves the Builder unburnt in its crater, still holding his crate; in thats-homework the Kid is not charred: the sanctions stamp flattens his schoolhouse round him, and he keeps doing his homework.
- The labels that explained the picture are cut: the loop's station labels, THINGS THAT MAKE and THINGS THAT DESTROY, BUILD THINGS and STEAL THINGS, the country labels on the world map, the red crosses in try-all-three and the CRIME card. Who stands where says it now: the Crook on one end of the seesaw, the Weapons Maker on top of the tall stack, the lights that go out one by one, the Kid's mask.
- The world map is gone. North Korea and Russia are a sinking toy carrier and a padlocked hospital on the off-the-books plate; failed-states happens on main street after the bomb, with a stamped WELCOME sign and a broken signpost; thats-homework happens in a bombed town beside the loop.
- official-murder-budget is a host shot: the second cart is too big to fit in the studio. The last line, "You defund it.", is its own host shot, where the fuse goes out; defund-the-loop ends on the ILLEGAL sign.

## Scene 1 · civilization-countdown-title

- id: civilization-countdown-title
- act: Title
- transition_in: cut (parts are rendered on their own)
- key: after "Countdown.": the heading on the navy card, the little Earth at the heart of the atom with its fuse lit, the spark fizzing at the fuse's far end, the Weapons Maker ducking back below the bottom edge
- cue: "Your Civilization Has a Countdown."
- time: 19:14.9 to 19:17.9 (3.0 s)
- voiceover: "Your Civilization Has a Countdown."
- layer: A, title card
- scene: The period title card (`KIT.titleScene`): the heading on plain navy under the film's atom. Heading lines, 16:9: `[{ words: ["YOUR", "CIVILIZATION", "HAS", "A"], style: "small" }, ["COUNTDOWN"]]`; 9:16: `[{ words: ["YOUR", "CIVILIZATION"], style: "small" }, { words: ["HAS", "A"], style: "small" }, ["COUNTDOWN"]]`. The gag: the atom's nucleus is a small Earth with a bomb's screw collar, and a fuse runs from the collar out between the orbits and down the left side of the card to its bottom edge.
- props: title-card, earth-globe, fuse, weapons-maker
- status: planned

Moves: The card comes up from black with the heading on it, as Part 2's does, the three papers running round the atom's orbits. "Countdown." → the Weapons Maker pops up from the bottom edge at the fuse's end, grinning, and touches his cigar to it; it catches with a spark. after "Countdown." → he ducks back down, and the spark starts crawling up the fuse toward the Earth as the card goes to black.

Sound: a projector whirr on "Your"; a fire fizz as the fuse catches.

On screen: "YOUR CIVILIZATION HAS A COUNTDOWN".

Why: the narrator reads the heading, and the fuse makes the countdown literal.

## Scene 2 · official-murder-budget

- id: official-murder-budget
- act: Off the books
- transition_in: cut
- key: after "budget.": Wishonia at the lectern side-eyeing the camera, Part 10's cart beside it with OFFICIAL stamped across its tag, a cart wheel taller than the Weapons Maker filling the right edge of the frame, its shadow over him, his cigar drooping; the lit Earth-bomb on the lectern
- cue: "And that's just the official"
- time: 19:17.9 to 19:21.1 (3.3 s)
- voiceover: "And that's just the official murder budget."
- layer: A, host
- scene: The host's set. In the free wall right of the lectern stands Part 10's shopping cart, heaped with grinning warheads, the Weapons Maker leaning on its handle with his baby missile. On the lectern, beside Wishonia's mug, the Earth-bomb from the title card, its fuse long and burning.
- wishonia: smirk-closed + body-point-right; sideeye-closed + body-idle on "budget."
- props: studio, lectern, mug, earth-bomb, shopping-cart, price-tag, weapons-maker
- status: planned

Moves: "And" → Wishonia points at the cart; its tag reads "$2.72 TRILLION / YEAR", the bill Part 10's register rang up. "official" → the tag spins on its string and comes round with "OFFICIAL" stamped across it. "budget." → a shadow slides over the cart and the Weapons Maker from the right, and the front wheel of a second cart rolls into the right edge of the frame and stops. The wheel alone is taller than he is; the rest of that cart does not fit in the shot. after "budget." → he looks slowly up at it, and his cigar droops. Wishonia side-eyes the camera.

Sound: a pop as the tag spins; a whoosh as the wheel rolls in; a thunk as it stops.

On screen: "$2.72 TRILLION / YEAR" and "OFFICIAL" on the tag.

No: no tag or number on the big cart yet; it gets them on the plate.

Why: the war bill everyone argues about is the small cart.

## Scene 3 · cybercrime-10-trillion

- id: cybercrime-10-trillion
- act: Off the books
- transition_in: cut
- key: after "problem.": the two carts chained together, the big one twice the size on splayed wheels with its tags "$10.5 TRILLION" and "+15% A YEAR", war papers arcing into it from the Crook's laptop, the Weapons Maker and the Crook grinning at us over their handshake
- cue: "Cybercrime costs ten point five trillion"
- time: 19:21.1 to 19:28.7 (7.5 s)
- voiceover: "Cybercrime costs ten point five trillion dollars per year and growing at fifteen percent annually. This is not a separate problem."
- layer: B, plate off-the-books
- scene: The off-the-books plate, a long field the camera travels along, left to right: the two carts (Part 10's and one twice its size); a bank on a low hill with a WiFi pole beside it (a telephone pole with the WiFi arcs on top); a washtub of water, a missile on a launch stand, the Crook's little desk and a clock on a post; a hospital with a gurney outside and a small missile factory beside it, with room for a tank. This scene frames the carts and the bank.
- props: shopping-cart, price-tag, lobbyist, laptop, bank, wifi-pole, papers-plain, papers-war, weapons-maker, chain
- status: planned

Moves: "Cybercrime" → cut to the big cart's front wheel; the camera pulls back to the whole cart, twice the size of Part 10's, with the Weapons Maker in its shadow, and the Crook pops up out of its basket and opens a laptop on the rim. "ten point five trillion" → the camera pulls back to take in the bank on its hill: the vault door swings open, plain papers walk out in single file, climb the WiFi pole and hop into its arcs, and they pop out of the laptop with the missile seal on, arcing into the cart. The big cart's tag drops on: "$10.5 TRILLION". "fifteen percent" → the line of papers goes two abreast, then three; a second tag clips on: "+15% A YEAR". "annually." → the big cart's wheels splay under the weight. "separate" → the Weapons Maker and the Crook look at each other across the gap, then lean over and shake hands. "problem." → a chain snaps the two carts together. after "problem." → both turn to us and grin, and the Weapons Maker's cigar perks up.

Sound: a click as the laptop opens; a pop per paper out of the laptop, faster on "fifteen"; a pat for the handshake; a clank as the chain snaps on.

On screen: "$10.5 TRILLION" and "+15% A YEAR" (the big cart's tags); "BANK" on the bank.

Why: the second cart is the same war, paid for another way.

## Scene 4 · crypto-afternoon

- id: crypto-afternoon
- act: Off the books
- transition_in: same plate (no seam)
- key: after "ransomware.": the padlocked hospital with its CLOSED sign and RANSOM note, war papers squeezing out under its door and marching into the missile factory, the patient on the gurney outside a grinning skeleton, still waiting
- cue: "North Korea can't build"
- time: 19:28.7 to 19:41.9 (13.2 s)
- voiceover: "North Korea can't build an aircraft carrier, but it funds its nuclear program by stealing one point five billion dollars in cryptocurrency in a single afternoon. Russia finances military operations with ransomware."
- layer: B, plate off-the-books
- scene: The camera travels on along the plate: the washtub, the missile on its stand, the Crook's desk with the clock; then the hospital and the missile factory.
- props: washtub, aircraft-carrier, missile, price-tag, stamp, lobbyist, laptop, papers-war, clock, hospital, padlock, gurney, human, factory
- status: planned

Moves: "North" → the camera travels right past the bank to a washtub of water standing in the field, a toy aircraft carrier bobbing in it. "carrier," → it lists, tips over and sinks; one bubble pops. "nuclear program" → the camera moves on to a grinning missile on a launch stand beside the tub, a price tag "UNPAID" swinging from its nose. "stealing" → the Crook tiptoes in with his laptop and sits down at the little desk beside it. "billion" → he tips the laptop, and war papers pour out of its screen onto a pile. "cryptocurrency" → a rubber stamp comes down from above the frame and thumps "PAID" across the missile's tag. "single" → the clock on its post spins from 12 to 5 so fast it smokes, while the pile climbs. after "afternoon." → it stops with a ding; the pile is taller than the missile, and the missile looks up at it. "Russia" → the camera travels on to a hospital with a patient waiting outside on a gurney, his chest light blinking red, and a small missile factory next door. "operations" → the factory's chimney missiles puff. "ransomware." → a padlock snaps onto the hospital's doors, its sign flips to CLOSED and a note goes up: "RANSOM"; war papers squeeze out under the doors and march into the factory. after "ransomware." → the patient on the gurney x-rays into a skeleton (`KIT.xray`), still waiting, still grinning.

Sound: a slide-down whistle as the carrier sinks and a pop for the bubble; a cash-register ding on "billion"; a stamp thump on PAID; a whirr as the clock spins and a ding when it stops; a clank for the padlock; an x-ray zap.

On screen: "UNPAID", then "PAID" (the missile's tag); "RANSOM" (the note); the hospital's name and its CLOSED sign.

No: no country labels or flags; the narrator says the names.

Why: two real cases of war paid for by theft.

## Scene 5 · war-through-wifi

- id: war-through-wifi
- act: Off the books
- transition_in: same plate (no seam)
- key: after "better.": the tank flattened like a pancake under a tower of war papers, the Weapons Maker's eyes blinking out of the flat hatch, the little pay pile beside it, the Crook still typing at his desk
- cue: "Cybercrime is war conducted"
- time: 19:41.9 to 19:46.3 (4.5 s)
- voiceover: "Cybercrime is war conducted through WiFi, and it pays better."
- layer: B, plate off-the-books
- scene: The camera travels back to the Crook at his desk, and a tank rolls up beside it.
- props: lobbyist, laptop, tank, weapons-maker, papers-war
- status: planned

Moves: "Cybercrime" → the Crook at his desk, typing. "war" → a tank rolls up beside him, the Weapons Maker standing in its hatch with his cigar. "WiFi," → the WiFi arcs over the laptop ripple out across the field like rings on a pond. "pays" → payday: a small pile of war papers drops beside the tank, and the Weapons Maker admires it. after "better." → a shadow; he looks up; a tower of war papers drops out of the sky onto the tank and flattens it like a pancake, the barrel bent to the ground, and his two eyes blink out of the flat hatch. The Crook keeps typing.

Sound: a clank as the tank rolls up; a thunk for the small pile; a splat when the tower lands.

On screen: nothing.

Why: one picture of why cybercrime grows.

## Scene 6 · destroy-beats-make

- id: destroy-beats-make
- act: The destroying economy
- transition_in: cut
- key: after "emergency.": the war-paper stack lying across the flattened crates, the Weapons Maker riding on it, the Builder's blinking eyes and one hand reaching up toward the dusty EMERGENCY: PULL box on its post and falling short
- cue: "Combined, your destructive economy"
- time: 19:46.3 to 20:03.7 (17.4 s)
- voiceover: "Combined, your destructive economy is thirteen point two trillion dollars per year, eleven point five percent of global G.D.P. Both are growing faster than the part of your economy that makes things. So the part that destroys things is winning. I'm told this is not considered an emergency."
- layer: B, plate the-stacks
- scene: A plain field: the two chained carts roll in from the left; in the middle, where they tip, one stack of war papers grows; beside it, the Builder's little pile of wooden crates; to the right, a small table with a small Earth on a cake stand; behind the crates, a street fire-alarm post, "EMERGENCY: PULL", its glass gray with dust.
- props: shopping-cart, chain, papers-war, earth-globe, cake-stand, lobbyist, human, crate, hammer, weapons-maker, missile, alarm-post
- status: planned

Moves: "Combined," → the two chained carts roll in, tip forward and pour all their war papers into one heap. "thirteen point two trillion" → the heap rises into a tall stack, and "$13.2 TRILLION" stamps into the sky over it. "eleven point five percent" → the camera travels right to the little table: the Crook, a napkin tucked into his collar, cuts a slice out of the small Earth like a cake, and a toothpick flag in the slice says "11.5%". "G.D.P." → he takes a bite. "growing" → the camera travels back to the stack: beside it, the Builder hammers a wooden crate together and sets it on his pile. "faster" → the paper stack shoots up on its own while he lifts one more crate, slowly. "destroys things" → the camera tilts up the stack, far above his knee-high crates, to the Weapons Maker sitting on top with his baby missile. "winning." → up on top, the Weapons Maker hoists his baby missile over his head like a trophy, and the stack sways. after "winning." → the stack tips over onto the crates and flattens the Builder; only his blinking eyes and one hand show. "emergency." → beside him, the fire-alarm post, "EMERGENCY: PULL", its glass gray with dust; the Builder's hand reaches up toward the handle and falls short. after "emergency." → nobody pulls it; the hand drops.

Sound: a whoosh as the carts tip; a slide-up whistle as the stack rises; a snip for the slice; hammering as the Builder builds; a sparkle as the trophy goes up; a splat when the stack lands; crickets after "emergency."

On screen: "$13.2 TRILLION" in the sky; "11.5%" (the toothpick flag); "EMERGENCY: PULL" (the alarm box).

No: no THINGS THAT MAKE or THINGS THAT DESTROY (v2's labels); the Builder at the crates and the Weapons Maker on top say which is which.

Why: the destroying half of the economy is growing faster than the making half, and nobody pulls the alarm.

## Scene 7 · considered-tuesday

- id: considered-tuesday
- act: The destroying economy
- transition_in: cut
- key: after "Tuesday.": Wishonia at the lectern with her mug on its way down, the desk calendar on the lectern showing TUESDAY and two torn pages, both TUESDAY, fluttering down, the Earth-bomb's fuse half gone
- cue: "On your planet this"
- time: 20:03.7 to 20:06.6 (2.9 s)
- voiceover: "On your planet this is considered "Tuesday."."
- layer: A, host
- scene: The host's set. On the lectern: the mug, a desk calendar (`KIT.props.calendar`, its month band reading TUESDAY, several pages) and the Earth-bomb, its fuse about half as long as in official-murder-budget.
- wishonia: smirk-closed + body-idle; smirk-smile + body-palms-down on "Tuesday"
- props: studio, lectern, mug, calendar, earth-bomb
- status: planned

Moves: "On" → cut to Wishonia at her lectern; the mug rises from the lectern to her lips and she sips (the bible's mug sip). "Tuesday" → the calendar's top page tears off: TUESDAY; that one tears off: TUESDAY; and again: TUESDAY (the day number goes up, the band never changes). after "Tuesday." → the mug goes down to the lectern, slowly.

Sound: a click per calendar page; a soft thunk as the mug lands.

On screen: "TUESDAY" on the calendar.

Why: a breather punchline: the emergency is routine.

## Scene 8 · build-or-steal

- id: build-or-steal
- act: Build or steal
- transition_in: cut
- key: after "afternoon?": the padlocked hospital with RANSOM on its door and the clock over it on 5, the Builder flat on his back beside his two-legged chair at the workbench, the little factory and capitol skidded to a stop crooked behind him, skid marks running back to the seesaw at the left edge, down on the Crook's end
- cue: "When the parasitic economy grows"
- time: 20:06.6 to 20:21.6 (15.0 s)
- voiceover: "When the parasitic economy grows large enough relative to the productive one, the rational choice for any individual, company, or nation flips from "build things" to "steal things." Why spend years building a product when you can ransom a hospital in an afternoon?"
- layer: B, plate main-street
- scene: The main-street plate, the camera traveling left to right: an empty lot with a seesaw (a plank on a triangle; the Crook's end is the right one, toward town); the Builder's workbench and stool; a small hospital with a clock over its door; the Builder's factory with a SUCCESS sign on its roof and a conveyor out of its side door; the Crook's desk next door; and, at the edge of town, a WELCOME sign and an empty signpost. A plain field behind.
- props: seesaw, papers-war, papers-plain, lobbyist, human, factory, capitol, workbench, stool, chair, hospital, padlock, clock
- status: planned

Moves: "parasitic economy" → the seesaw in the empty lot: the Crook sits on its right end, grinning, and war papers land on his end one after another. "productive one," → two plain papers sit on the left end. "individual," → the Builder hops onto the other end with his hammer. "company," → a little factory hops on beside him. "nation" → a little capitol hops on beside it, and their end goes down. "flips" → a brick of war papers drops onto the Crook's end, the plank slams down, and the Builder's end tips up into a slide: the Builder, the factory and the capitol slide down the plank, the Crook ducks, and they shoot off the low end past him into main street. "building" → the camera travels right with them as they skid down the street, and the Builder skids to a stop on the stool at his workbench, stars circling his head; the factory and the capitol skid to a stop crooked behind him. "product" → he starts a chair, one slow hammer blow per piece. "ransom" → next door, the Crook snaps a padlock onto the small hospital's door with a note, "RANSOM", and papers squeeze out under the door into his briefcase. "afternoon?" → the clock over the door jumps from 12 to 5, as it spun in crypto-afternoon; the chair has two legs. after "afternoon?" → the Builder sits on it to rest, and it tips him over backwards.

Sound: pops as the war papers land; a boing for each of the three riders; a slam and a slide-down whistle as they slide; hammering; a clank for the padlock; a ding as the clock jumps; a thunk as the chair tips.

On screen: "RANSOM".

No: no BUILD THINGS or STEAL THINGS on the ends (v2's labels); the Crook on one and the Builder on the other say which is which. Not the balance scale prop: the slide needs a plank on a triangle.

Why: the tipping point, as a choice any human, company or nation faces.

## Scene 9 · production-irrational

- id: production-irrational
- act: Build or steal
- transition_in: same plate (no seam)
- key: after "survival.": a neat round crater where the factory stood, the Builder's crate and hammer at the bottom of it, and the Builder, unburnt, at the desk beside the Crook, putting on a domino mask
- cue: "Why manufacture exports"
- time: 20:21.6 to 20:38.6 (17.1 s)
- voiceover: "Why manufacture exports when hacking banks pays better? Once enough of your economy is extraction, producing anything makes you a target rather than a success. Production becomes irrational. Parasitism becomes the only means of survival."
- layer: B, plate main-street
- scene: The camera travels on along main street to the Builder's factory and the Crook's desk next door.
- props: factory, sign, conveyor, crate, human, lobbyist, laptop, papers-war, missile, crater, mask
- status: planned

Moves: "manufacture" → the camera travels on to the Builder's factory: he loads wooden crates onto a conveyor out of its side door, under a "SUCCESS" sign on the roof. "exports" → the crates ride off the end of the conveyor and out of the frame. "hacking banks" → next door, the Crook types at his desk, and his laptop spits war papers onto a pile. "extraction," → the pile grows past the factory roof. "target" → the SUCCESS sign flips over to a bullseye. "rather" → a missile pokes in at the top of the frame and whistles down at it. "success." → it hits the bullseye dead center: a white flash, a boom, the frame shakes. "irrational." → the smoke clears on a neat round crater where the factory stood. The factory is simply gone. At the bottom of the crater stands the Builder, unburnt, still holding his crate, looking round for it. The Crook, untouched, keeps typing. "Parasitism" → the Builder drops the crate and his hammer, climbs out of the crater, sits down at the desk next to the Crook and opens a spare laptop. after "survival." → the Crook hands him a domino mask, and he puts it on.

Sound: a thunk as the crates load; typewriter clacks for the hacking; a cash-register ding for the pile; a switch click as the sign flips; a slide-down whistle and a boom; a sizzle as the smoke clears; a click as the laptop opens; a pop as the mask goes on.

On screen: "SUCCESS", then the bullseye.

No: no charred Builder and no mushroom cloud; the part spends those on the Watcher, and the missile wanted the factory, not him.

Why: what the tipping point does to one worker.

## Scene 10 · failed-states

- id: failed-states
- act: Where it ends
- transition_in: same plate (no seam)
- key: after "taken.": the toll gate on the filled crater where the factory stood, the Crook in an army helmet three sizes too big holding the Hut Builder's hut up out of her reach, the Hut Builder hammering the air below it
- cue: "You have a name for places"
- time: 20:38.6 to 20:56.0 (17.4 s)
- voiceover: "You have a name for places where this already happened. You call them "failed states." Somalia, Libya, parts of Syria. The productive economy collapsed, the warlord economy replaced it, and nobody can restart production because anyone who builds something gets it taken."
- layer: B, plate main-street
- scene: The edge of town on main street, then back to the crater where the factory stood.
- props: sign, stamp, stamp-mark, signpost, crater, crate, toll-gate, lobbyist, army-helmet, papers-war, human, hut
- status: planned

Moves: "places" → the camera travels on from the two masked men to the edge of town: a WELCOME sign on two posts, and an empty signpost under it. "failed" → a giant rubber stamp comes down out of the sky and thumps "FAILED STATE" across the WELCOME sign. "Somalia," → the signpost gets its first board: SOMALIA. "Libya," → LIBYA. "Syria." → PARTS OF SYRIA, and the board snaps: only "PARTS OF SY" stays nailed up, and the rest drops into the dust. "collapsed," → the camera travels back to the crater where the factory stood, and its rim caves in and fills it, burying the Builder's crate. "warlord" → a toll gate goes up on the filled ground; the Crook, in an army helmet three sizes too big, collects war papers at it. "restart" → the Hut Builder walks up with planks and a hammer. "builds something" → she hammers a little hut together beside the gate. "taken." → the Crook's gloved hand lifts the hut off the ground, up out of her reach. after "taken." → she keeps hammering the air where it was, then looks up.

Sound: a stamp thump on the sign; a thunk as each board goes up and a snip as the third one snaps; a slide-down whistle as the crater fills; a clank as the gate goes up; hammering; a whoosh as the hut goes.

On screen: "WELCOME" and "FAILED STATE" (the sign and its stamp); "SOMALIA", "LIBYA", "PARTS OF SY" (the signpost).

Why: the end of this road already exists.

## Scene 11 · neighbors-house

- id: neighbors-house
- act: Where it ends
- transition_in: cut
- key: after "basement.": the white flash going over to a mushroom cloud where the Watcher's house stood, the YOU mailbox spinning up into the air in front of it; the neighbor's house a black frame by its FAILED STATE mailbox
- cue: "You've watched this happen"
- time: 20:56.0 to 21:04.0 (8.0 s)
- voiceover: "You've watched this happen to individual countries the way someone watches a neighbor's house burn down while storing gasoline in their own basement."
- layer: B, plate two-houses
- scene: Two houses (`KIT.props.house`) side by side on a suburban street, mailboxes "FAILED STATE" (the neighbor's, left) and "YOU" (right); in the right one's picture window, the Watcher sips tea. Beyond the right house, an empty lot runs on to the right.
- props: house, mailbox, human, teacup, gas-can, flames, nuke
- status: planned

Moves: "watches" → the two houses; in the window of his, the Watcher sips tea, watching the other one. "neighbor's house" → flames start on the neighbor's roof. "burn down" → they take the house, which burns down to a black frame; one ember floats up and drifts slowly toward his house. "gasoline" → the camera pushes in on his basement window: inside, the basement is stacked to the ceiling with red gas cans, each with the missile seal. "own" → the ember drifts lower, toward the window. "basement." → one more can rolls down the basement stairs, and the ember drops in through the window. after "basement." → the camera pulls back: a white flash, a boom, the frame shakes, and a mushroom cloud goes up where his house was; the YOU mailbox spins up into the air. The film cuts to Wishonia (once-it-starts) before the smoke clears; the Watcher is seen again when the plate comes back.

Sound: a fire whoosh as the roof catches; a clank as the cans show and another as the last can rolls in; a boom.

On screen: "FAILED STATE" and "YOU" (the mailboxes).

Why: the viewer's country is the next house.

## Scene 12 · once-it-starts

- id: once-it-starts
- act: Where it ends
- transition_in: cut
- key: after "starts,": Wishonia at the lectern with her mug at her lips, sipping, eyes on the camera; beside the mug the Earth-bomb, its fuse down to about a third, the spark just short of the curl
- cue: "Once it starts,"
- time: 21:04.0 to 21:05.0 (1.0 s)
- voiceover: "Once it starts,"
- layer: A, host (reaction cut)
- scene: The host's set. On the lectern, the mug and the Earth-bomb, its fuse about a third as long as in official-murder-budget.
- wishonia: sideeye-closed + body-idle
- props: studio, lectern, mug, earth-bomb
- status: planned

Moves: "Once" → cut to Wishonia at her lectern while the boom is still rolling, her mug already at her lips: she sips, eyes on the camera, as the Watcher sipped at his window. Beside the mug, the spark fizzes along what is left of the fuse. after "starts," → she keeps sipping. She does not look at it.

Sound: nothing new; the boom from neighbors-house rolls on under the sip.

On screen: nothing new.

Why: a reaction cut on the blast, and a fuse check-in: she is doing what the Watcher did, beside her own lit fuse.

## Scene 13 · try-all-three

- id: try-all-three
- act: Where it ends
- transition_in: cut back to the two-houses plate, where the camera would have got to
- key: on "three": the charred Watcher on the round rug leaning into the headset microphone, the dark bulb and the ballot box with his ballot stuck back out of its slot behind him, the spotlight off
- cue: "you can't vote"
- time: 21:05.0 to 21:11.5 (6.4 s)
- voiceover: "you can't vote your way out, innovate your way out, or give a TED Talk about it. (You will try all three.)."
- layer: B, plate two-houses
- scene: The Watcher's bare floor, then the empty lot beyond it.
- props: teacup, ballot-box, light-bulb, rug, headset-microphone, spotlight, human
- status: planned

Moves: "you" → cut back to the plate: the cloud has thinned away over the bare floor where the house stood, and on it the Watcher stands charred black, smoking, hair straight up, still holding his teacup, blinking. "vote" → the camera eases right off him along the empty lot, and a ballot box (`KIT.props.ballotBox`) drops in. "out," (the first) → its slot snaps shut. "innovate" → a big light bulb on a stand drops in, lit. "out," (the second) → it goes out. "TED Talk" → a round rug drops in, with a headset microphone on a stand under a spotlight. "it." → the spotlight goes out. "(You" → the charred Watcher runs in from his bare floor, still smoking, teacup in hand. "try" → he stuffs a ballot into the box, and the box spits it back in his face. "all" → he grabs the bulb, and it zaps him: a flash of his x-rayed skeleton. Then he hops onto the rug and taps the microphone, tap, tap, tap, to nobody. "three" → he leans in to speak.

Sound: a sizzle as the smoke thins off him; a click as the slot shuts; a switch click as the bulb goes out and another as the spotlight goes out; a pop as the ballot spits back; a zap; three ticks for the taps.

On screen: "VOTE" on the ballot box.

No: no crosses or X marks; each way out shuts itself off.

Why: the blast's payoff (the Watcher, charred, still at his tea), then the three usual answers, ruled out, and the joke that humans will try them anyway.

## Scene 14 · 25-percent-by-2033

- id: 25-percent-by-2033
- act: The Soviet comparison
- transition_in: cut
- key: after "one.": the USSR headstone at the foot of the gauge, and beside the grave the crankless old computer with its crank on the ground and the PLAN binder standing up proud with its TERRIBLE sticker, the dial above with the red zone lit and 2033 in its window
- cue: "At current growth rates"
- time: 21:11.5 to 21:30.8 (19.4 s)
- voiceover: "At current growth rates, your destructive economy reaches twenty-five percent of G.D.P. by twenty thirty-three. The Soviet Union collapsed at fifteen percent of G.D.P. in military spending alone. They had worse technology, a smaller parasitic sector, and a plan. It was a terrible plan, but they had one."
- layer: B, plate the-gauge
- scene: A giant dial meter (`KIT.props.gauge`, the box mount) standing on a plain field like a monument, its scale marked 0 to 30, a red zone from 25 and a counter window under the pivot. Left of it, bare ground for the Soviet side; right of it, bare ground for ours.
- props: gauge, headstone, tv-set, gears, sprout, binder, sticker
- status: planned

Moves: "current" → the gauge, its needle on 11.5, where the Crook's slice was. "twenty-five" → the red zone lights up. "thirty-three." → the window spins to 2033, and the needle swings up into the red. after "thirty-three." → the gauge rattles and puffs steam. "Soviet" → the needle drops back to 11.5. "collapsed" → the camera travels left and down: a headstone rises out of the ground at the foot of the gauge, "USSR". "technology," → beside the grave, a clunky old computer (a 1950s TV cabinet on a box of gears) cranks itself, puffing. "smaller parasitic sector," → a tiny sprout of war papers pokes up beside it. "plan." → a thick binder thumps down against the headstone: "PLAN". "terrible" → a "TERRIBLE" sticker slaps onto it. after "one." → the binder stands up straight, proud, and the crank falls off the computer.

Sound: a switch click as the red zone lights; a whirr as the window spins and a sizzle for the steam; a thunk as the headstone rises and another for the binder; a splat for the sticker; a clank as the crank falls off.

On screen: the dial's numbers, "% OF GDP" on its plate and "2033" (the window); "USSR" (the headstone); "PLAN" and "TERRIBLE" (the binder).

Why: a known collapse point, and the viewer's economy heading past it.

## Scene 15 · no-plan

- id: no-plan
- act: The Soviet comparison
- transition_in: same plate (no seam)
- key: after "lost.": the whole gauge, the Soviet side a smoking heap of rubble at the foot of the USSR headstone with the 1ST rosette on top, the Politician on our side grinning, thumbs up, his clipboard reading PLAN: and nothing else, the vine of war papers wrapped round the dial, the needle a notch closer to 15
- cue: "You are approaching their ratio"
- time: 21:30.8 to 21:43.3 (12.5 s)
- voiceover: "You are approaching their ratio with better technology, a faster-growing parasitic sector, and no plan. The Soviet Union's terrible plan beat your no plan, and the Soviet Union lost."
- layer: B, plate the-gauge
- scene: The same gauge, now with our side.
- props: gauge, laptop, vine, papers-war, politician, clipboard, rosette, headstone
- status: planned

Moves: "approaching" → the camera travels right to our side of the gauge; the needle creeps from 11.5 toward the 15, tick, tick. "technology," → a shiny laptop lands on our side. "faster-growing" → a vine of war papers shoots up out of it, up the gauge and round the dial. "no" (the first) → the Politician pops up on our side, grinning, holding a clipboard (`KIT.props.clipboard`) titled "PLAN:" with nothing on it. "beat" → the camera pulls back to the whole gauge: Part 4's 1ST rosette pins onto the Soviet binder. "lost." → the binder and the old computer crack and collapse into a smoking heap of rubble at the foot of the headstone, and the rosette floats down onto it. after "lost." → the Politician gives the rubble a thumbs-up, and the needle ticks one more notch toward 15.

Sound: two ticks as the needle creeps; a thunk for the laptop; a slide-up whistle for the vine; a boing for the Politician; a pop for the rosette; a slam as the Soviet side falls; one more tick.

On screen: "PLAN:" (the clipboard); "1ST" (the rosette).

Why: humans are doing worse than a system that already failed.

## Scene 16 · this-is-a-loop

- id: this-is-a-loop
- act: The loop
- transition_in: cut
- key: after "loop,": Wishonia at the lectern, arms crossed, side-eyeing the camera; beside her mug the Earth-bomb's spark just out of the curl in its fuse, a short stub left
- cue: "This is a loop,"
- time: 21:43.3 to 21:44.7 (1.4 s)
- voiceover: "This is a loop,"
- layer: A, host (reaction cut)
- scene: The host's set. On the lectern, the mug and the Earth-bomb, the spark at the start of the curl in its fuse.
- wishonia: sideeye-closed + body-arms-crossed
- props: studio, lectern, mug, earth-bomb
- status: planned

Moves: "This" → cut to Wishonia at her lectern, arms crossed, giving the camera a slow look after the Politician's thumbs-up; beside her mug, the spark has reached the curl in the fuse. "loop," → the spark runs round the curl, a loop of its own, and comes out with only a stub of fuse left. She does not look at it.

Sound: a fire fizz as the spark goes round the curl.

On screen: nothing new.

Why: a reaction cut on the Soviet punchline, and a fuse check-in: the countdown kept burning through the comparison.

## Scene 17 · loop-not-line-item

- id: loop-not-line-item
- act: The loop
- transition_in: cut
- key: after "spending.": the camera pulled back on the whole loop, war papers running round it so fast they fly off the bends: the press and the Politician, the bread whose price tag just burst, the Builder with his sliver of a paycheck, the Builder masked at the laptop, the stack with the Weapons Maker on top catching a new missile
- cue: "not a line item."
- time: 21:44.7 to 22:02.4 (17.7 s)
- voiceover: "not a line item. Your governments print money to fund military spending, which devalues wages through inflation, which makes legitimate work pay less, which pushes talent toward cybercrime, which grows the destructive economy, which justifies more military spending."
- layer: B, plate the-loop
- scene: A plain field with a road laid out in a loop (the shape of Part 2's money loop) and six stations round it, clockwise from the top left: 1 the 1913 printing press with the Politician at its crank; 2 a bread stand; 3 a factory gate, its SUCCESS sign hanging upside down; 4 the Crook's desk with a spare laptop; 5 the war-paper stack from destroy-beats-make; 6 the Weapons Maker on top of it. Outside the loop on the right, a small town (thats-homework); below the loop, the lab and a branch road to the color-flip funnel, empty until defund-the-loop.
- props: ledger, printing-press, politician, papers-war, bread, price-tag, human, paycheck, factory, sign, lobbyist, laptop, mask, weapons-maker, missile
- status: planned

Moves: "not" → cut to a big open ledger lying on the field, its page ruled with line items. "line" → one line, "MILITARY", peels up off the page. "item." → it stretches and curls round into a loop of road on the ground, and the camera pulls back as it lands among the six stations. "print" → station 1: the Politician cranks the 1913 press, and war papers pop out of it and run off along the loop. "inflation," → station 2: the price tag on a loaf of bread swells like a balloon, bigger and bigger. "pay less," → station 3: at the factory gate, the Builder holds out his paycheck (a plain paper), and it shrinks to a sliver, as in Part 10. "cybercrime," → station 4: he puts on his domino mask and sits down at the laptop beside the Crook. "destructive economy," → station 5: the stack shoots up as the papers run into it. "more" → station 6: on top of it, the Weapons Maker catches a new baby missile, and the papers run on round to the press. after "spending." → the camera pulls back to the whole loop: it speeds up until papers fly off the bends, and the bread's price tag bursts.

Sound: a whoosh as the line peels off; a whirr as the press turns; a slide-up whistle as the price tag swells; a squeak as the paycheck shrinks; a click for the laptop; a cash-register ding for the stack; a clank for the missile; a whoosh as the loop speeds up and a pop for the price tag.

On screen: "MILITARY" (the line that peels off); "1913" (the press); "$" (the price tag).

No: no station labels (v2 had them); what happens at each one says it.

Why: the parts of the problem feed each other.

## Scene 18 · thats-homework

- id: thats-homework
- act: The loop
- transition_in: same plate (no seam)
- key: after "math.": the Kid in his tiny domino mask at his school desk in the bombed town, the schoolhouse's walls lying flat round him, his worksheet reading "$ < $$$$$" with a gold star on it, the Politician leaning over him like a proud teacher, the tank squashed flatter under its "$$$$$" tag
- cue: "Every nation you've bombed"
- time: 22:02.4 to 22:16.2 (13.8 s)
- voiceover: "Every nation you've bombed or sanctioned has learned that parasitizing your economy is cheaper than fighting you conventionally. That's not crime. That's homework. You built the incentive structure and they did the math."
- layer: B, plate the-loop
- scene: The small town at the edge of the loop's field: three houses and a one-room schoolhouse.
- props: house, bomb, nuke, stamp, stamp-mark, schoolhouse, school-desk, human, laptop, tank, price-tag, worksheet, pencil, politician, gold-star
- status: planned

Moves: "nation" → the camera leaves the loop for the small town: three cartoon bombs whistle down onto it. "bombed" → they go off as three small mushroom clouds. "sanctioned" → a giant rubber stamp thumps "SANCTIONED" across the schoolhouse roof, and the schoolhouse's four walls fall flat outward like a cardboard box. "learned" → the dust settles on the Kid inside, unhurt, at his school desk, with a laptop and his homework. "cheaper" → beside his desk lands the flattened tank from war-through-wifi with a price tag, "$$$$$", and on the laptop a tag, "$". "conventionally." → the tank's tag is so heavy it squashes the tank flatter. "crime." → the Kid pulls on a tiny domino mask. "homework." → he licks his pencil and bends over his worksheet. "built" → the Politician strolls in from the loop and leans over the desk like a proud teacher. "did the math." → the Kid writes "$ < $$$$$". after "math." → the Politician sticks a gold star on the worksheet, grinning, and the Kid beams.

Sound: a slide-down whistle as the bombs fall and three pops; a stamp thump and a slam as the walls fall; a splat as the tag squashes the tank; a pencil scratch; a sparkle for the gold star.

On screen: "SANCTIONED" (the stamp); "$$$$$" and "$" (the tags); "$ < $$$$$" (the worksheet).

Why: the other side's answer is rational; the loop runs on incentives, not villains.

## Scene 19 · defund-the-loop

- id: defund-the-loop
- act: The loop
- transition_in: same plate (no seam)
- key: on "loop." (the last one): the Politician hammering his ILLEGAL sign in beside the loop as the last war paper runs straight past it; behind them, medicine papers filing out of the color-flip funnel to the Scientist's lab bench, and the Weapons Maker sitting on the ground with his missile asleep in his lap
- cue: "The treaty breaks this loop"
- time: 22:16.2 to 22:32.0 (15.8 s)
- voiceover: "The treaty breaks this loop. Redirect the war money to medical research, make the productive economy so rewarding that crime becomes irrational, and defund the war machine that manufactures the poverty that feeds the cycle. You don't outlaw the loop."
- layer: B, plate the-loop
- scene: The loop again, with the treaty's switch, the branch road, the color-flip funnel and the lab.
- props: scroll, railroad-switch, color-flip-funnel, papers-war, papers-med, lab, scientist, factory, sign, human, laptop, printing-press, weapons-maker, missile, politician, hammer
- status: planned

Moves: "The" → the camera travels from the Kid back to the loop, war papers racing round it. "treaty" → a treaty scroll (`KIT.props.scroll`) unrolls in the middle of the loop and folds itself into a railroad switch. "breaks" → it drops into the road at the bottom bend; the papers running round hit it and are switched off the loop onto a branch road. "Redirect" → the branch runs them into the color-flip funnel (`KIT.props.colorFlipFunnel`). "medical" → they come out with the cross seal. "research," → they file up to the lab bench, where the Scientist waves them in. "rewarding" → more medicine papers walk in at the factory gate, and its SUCCESS sign flips back up the right way. "crime" → at station 4, the Builder pulls off his mask and walks back to the factory. "irrational," → in the town, the Kid shuts his laptop, takes off his little mask and follows the papers to the lab. "defund" → the press coughs out one last puff and grinds to a stop, and the stack drains, lowering the Weapons Maker to the ground. "cycle." → he looks round for papers, finds none, and lays his missile down like a sleeping baby. "outlaw" → the Politician nails an "ILLEGAL" sign onto the loop; the last war paper runs straight past it and keeps going round.

Sound: a whoosh as the scroll unrolls; a clank as the switch drops in; a ding as the seals flip; a cash-register ding for the SUCCESS sign; a click as the Kid's laptop shuts; a sizzle as the press runs dry; hammering for the ILLEGAL sign.

On screen: "TREATY" (the scroll, before it folds); "SUCCESS"; "ILLEGAL".

Why: the fix: take the money out of the loop instead of passing a law against it.

## Scene 20 · you-defund-it

- id: you-defund-it
- act: The loop
- transition_in: cut
- key: after "it.": Wishonia at the lectern smirking at the camera, the Earth-bomb beside her mug with its fuse a drooping stub, the spark out and one smoke ring rising
- cue: "You defund it."
- time: 22:32.0 to 22:34.0 (2.0 s)
- voiceover: "You defund it."
- layer: A, host
- scene: The host's set, as in official-murder-budget; the Earth-bomb's fuse is down to a stub, its spark a finger's width from the collar.
- wishonia: happy-smile + body-open-palms; smirk-smile + body-idle on "it."
- props: studio, lectern, mug, earth-bomb
- status: planned

Moves: "You" → cut to Wishonia at her lectern; beside her mug, the spark is almost at the Earth's collar. "defund" → she opens her palms. after "it." → the spark sputters out in a puff, the stub droops, and the Earth lets out one smoke ring. She does not look at it.

Sound: a sizzle as the spark goes out.

On screen: nothing new.

Why: the countdown stops when the money stops.
