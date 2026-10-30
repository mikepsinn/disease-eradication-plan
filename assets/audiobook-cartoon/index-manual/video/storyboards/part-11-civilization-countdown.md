---
format: 1920x1080
duration: 3:19.1
message: "War plus cybercrime is a $13.2 trillion destructive economy growing faster than the productive one; at this rate it passes the share that collapsed the Soviet Union, unless the treaty defunds the loop that feeds it."
arc: Title card, where the Weapons Maker lights the fuse on the Earth → the official budget is only the small cart → cybercrime, the war that pays better → the destroying economy outgrows the making one ("Tuesday") → building stops making sense → failed states and the gasoline basement → 25% by 2033 and the Soviet Union's terrible plan → the loop → the treaty switches the money off the loop, the papers come out teal and the fuse goes out
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 11, "Your Civilization Has a Countdown"
audio: index-manual.cbaf659d.mp3, 19:14.9 to 22:34.0
version: v2
---

# Part 11 storyboard: "Your Civilization Has a Countdown"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys: "war papers" carry the red missile seal (`KIT.money("war")`), "medicine papers" the teal cross seal (`KIT.money("med")`), "plain papers" no seal (`KIT.money("plain")`). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Cast.** The Masked Crook (`KIT.cast("lobbyist")`: fedora, domino mask, popped-collar trench coat, gloves; in this part he is the cybercriminal, with a laptop in place of his briefcase), the Weapons Maker (`KIT.cast("weaponsMaker")`: barrel chest, tiny head under a hard hat, cigar, cradling a grinning baby missile), the Politician (`KIT.cast("politician")`: lantern jaw, a grin full of teeth, flag pin, very wide tie) and the Scientist (`KIT.cast("scientist")`). Four everyday humans come back from scene to scene, drawn with these exact options so each looks the same every time:
- The Builder: `KIT.person({ tone: 1, outfit: "overalls", color: 0, seed: 7, mood: "eager" })` (an orange barrel), with a hammer in the right hand. destroy-beats-make, build-or-steal, production-irrational (charred, then masked), loop-not-line-item (masked at station 4), defund-the-loop (unmasked).
- The Watcher: `KIT.person({ tone: 0, outfit: "suit", color: 1, seed: 3, mood: "smug" })` (a refrigerator-box businessman), with a teacup; the same options plus `charred: true` from the boom in neighbors-house through try-all-three.
- The Hut Builder: `KIT.person({ tone: 3, hair: 1, outfit: "dress", color: 2, seed: 5, mood: "eager" })` (an hourglass). failed-states.
- The Kid: `KIT.person({ tone: 2, outfit: "shirt", color: 3, seed: 11, mood: "eager", mask: true, build: { hs: 1.3, legs: 0.6, th: 0.75, neck: 0.5 } })` at 0.7 of the scene's human scale: a small human in a tiny domino mask. thats-homework, defund-the-loop (`mask: false` once he takes it off).

**Spine.** The war papers, off the books. In this part they stop being only the government's: they walk out of a bank through the WiFi and come out with the red missile seal (cybercrime-10-trillion), fill the bigger cart, tip into the THINGS THAT DESTROY stack (destroy-beats-make), weigh down the STEAL end of the seesaw (build-or-steal), climb the gauge as a vine (no-plan) and run round the ledger loop (loop-not-line-item), until the treaty switches them off the loop into the color-flip funnel and they come out as medicine papers (defund-the-loop).

**Running gag: the fuse.** It replaces the countdown board (the board is no longer in the kit) and says what the board said: the countdown is running, and it is the viewer's civilization on the end of it. The civilization is a cartoon bomb: a small Earth (`KIT.props.earthGlobe`) with a bomb's navy screw collar on top and a lit fuse. The Weapons Maker lights it with his cigar on the title card; it hops into the top-left corner and burns there, a little shorter in every Layer B scene, for the whole part. Its spark flares on "emergency" (destroy-beats-make) and on "no plan" (no-plan). On the part's last words it goes out: after "it." in defund-the-loop the spark sputters out in a puff, the stub droops and the Earth lets out one smoke ring. Nobody ever looks at it, which is the joke.

Build: the fuse burns by part time, so it is continuous across scenes. t = `KIT.scene(ID).start` plus the scene's own time.
- 16:9: the Earth centered at (112, 116), radius 58; the collar a navy 32 × 14 box at (96, 46) with an orange edge; the fuse path `M112,52 Q118,30 150,32 L780,32` (677 px), drawn from the collar outward; visible length L(t) = 640 - 2.6 t.
- 9:16: the Earth at (110, 150), radius 56; the collar at (94, 80); the fuse path `M110,86 Q116,64 148,66 L690,66` (589 px); L(t) = 560 - 2.2 t.
- The cord is a navy stroke 9 px wide under a tan (`KIT.C.tan`) stroke 5 px wide, both with `stroke-dasharray` "L 3000"; the spark sits at `getPointAtLength(L)`: a mustard `KIT.star` (r 14) over an orange one (r 8), flickering in scale 0.8 to 1.2 (finite repeats), with a thin grey smoke wisp. About 125 px are left at "defund it".
- It lives in its own layer above the scene camera and under the grain, so a slide left does not move it. In the one zoom into the wall screen (build-or-steal) it goes inside the camera, and in the office (considered-tuesday) it appears only inside the wall screen's mini frame.
- Scene art keeps out of its corner: in 16:9 x 0 to 200, y 0 to 190 and the strip y 0 to 60 out to x 800; in 9:16 x 0 to 190, y 0 to 220 and the strip y 0 to 95 out to x 700.

**Callbacks.** From Part 10 (murder-shopping-cart, warheads-in-the-cart, cart-gadgets): the shopping cart (`KIT.props.shoppingCart`) comes back with its contents (the warhead heap, the frowning robot, the crank box) in official-murder-budget. From Part 10 (nothing-papers, paycheck-shrinks): the 1913 printing press and the shrinking paycheck are stations 1 and 3 of the loop. From Part 10 (submarine-on-land): Part 10 flipped medicine papers red in the funnel; defund-the-loop flips them back. From Part 1 (without-with-papers): the cobweb and the spider, now on the EMERGENCY box. Inside the part: the wall clock (crypto-afternoon, build-or-steal), the tank (war-through-wifi, thats-homework), the factory and its SUCCESS sign (production-irrational, defund-the-loop), the Builder's domino mask (production-irrational, loop-not-line-item, defund-the-loop), the Kid (thats-homework, defund-the-loop), the Watcher (neighbors-house, try-all-three), the 11.5% slice (destroy-beats-make; the gauge needle starts on it in 25-percent-by-2033). Set up for Part 12: the part ends with medicine papers walking into the lab; Part 12's smoke-detector-by-mail opens on medicine papers walking in.

**Held frame.** None: the part states no death toll.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.
- Countries are plain text labels on the world map; no flags, emblems, leaders or national costumes. The cybercriminal and the warlord are the Masked Crook, never a national stereotype.
- No real conference stage or logo in try-all-three; the stage is a plain round rug with a headset microphone.
- No real weapons, banks or company marks: the tank, the missiles and the bank are plain engraved objects.

## Changes from v1

- The countdown board is gone from the kit; the fuse on the Earth replaces it (running gag above).
- The humans are the stereotype cast: the hacker is the Masked Crook, the cart pusher the Weapons Maker, the human with the empty clipboard the Politician; the Builder, the Watcher, the Hut Builder and the Kid are everyday humans with fixed options.
- Money is money green with seals: "red papers" are now war papers. The stolen money walks out of the bank plain and gets its red missile seal as it passes through the WiFi.
- Every threat pays off on screen (style bible, Comedy 6): the cybercrime payday flattens the tank, the ransomed patient turns into a grinning skeleton, the destroy stack topples onto the Builder, the seesaw catapults him, a missile chars him and his SUCCESS factory, the gasoline basement goes up and chars the Watcher, the bulb x-rays him, and the Soviet side crumbles under its WINNER ribbon.
- defund-the-loop: the treaty no longer snips the loop with scissors (Part 6's redirect-math already snips its loop); it drops in like a railroad switch and sends the papers off the loop into the funnel. The loop is a strip of ledger paper, not Part 6's ring.
- civilization-countdown-title cuts in (parts are rendered on their own), and official-murder-budget slides in from the card, as loved-ones does in Part 1.
- Every scene has a Sound line, and the part file places each sound on its word.

## Scene 1 · civilization-countdown-title

- id: civilization-countdown-title
- act: Title
- transition_in: cut (the chapter card)
- key: after "Countdown.": the heading in, the lit Earth on its way to the top-left corner, the Weapons Maker ducking out of sight
- cue: "Your Civilization Has a Countdown."
- time: 19:14.9 to 19:17.9 (3.0 s)
- voiceover: "Your Civilization Has a Countdown."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`) with the part's heading; a small Earth with a bomb's collar and fuse drops in under it, and the Weapons Maker lights the fuse.
- wishonia: not on screen
- props: title-card, earth-globe, fuse, weapons-maker
- status: planned

Moves: "Your" → the heading slams in, one word per spoken word: YOUR CIVILIZATION / HAS A COUNTDOWN. "Civilization" → a small Earth with a bomb's screw collar and a fuse on top drops in under the heading and bounces once. "Countdown." → the Weapons Maker pops up from the bottom edge, grinning, touches his cigar to the fuse, and it catches with a fizz; he ducks back down. after "Countdown." → the lit Earth hops into the top-left corner, where it stays for the rest of the part.

Sound: a thunk on YOUR, CIVILIZATION, HAS and COUNTDOWN; a boing as the Earth bounces; a fire fizz as the fuse catches; a whoosh as the Earth hops into the corner.

On screen: "YOUR CIVILIZATION HAS A COUNTDOWN". Why: the narrator reads the heading, and the fuse makes the countdown literal.

## Scene 2 · official-murder-budget

- id: official-murder-budget
- act: Off the books
- transition_in: slide left
- key: after "budget.": the tagged cart in the shadow of the bigger, untagged cart, the Weapons Maker looking up at it with his cigar drooping
- cue: "And that's just the official"
- time: 19:17.9 to 19:21.1 (3.3 s)
- voiceover: "And that's just the official murder budget."
- layer: B
- scene: The shopping cart from Part 10, heaped with warheads, the frowning robot and the crank box, with the Weapons Maker at its handle; it gets a new tag, and a cart twice its size rolls up behind it out of the shadow.
- wishonia: PiP, smirk-closed + point-right
- props: shopping-cart, price-tag, bomb, robot, weapons-maker, fuse
- status: planned

Moves: "And" → the cart from Part 10 stands parked, the Weapons Maker leaning on its handle and cradling his missile. "official" → the cart's price tag flips over to "OFFICIAL MURDER BUDGET". "budget." → a shadow slides over the cart and the man from the right, and a second cart twice the size, with no tag, rolls up behind it. after "budget." → the Weapons Maker looks slowly up at it; his cigar droops.

Sound: a pop as the tag flips; a whoosh as the big cart rolls in; a thunk as it stops.

On screen: "OFFICIAL MURDER BUDGET". Why: the war bill was the smaller cart.

## Scene 3 · cybercrime-10-trillion

- id: cybercrime-10-trillion
- act: Off the books
- transition_in: same form (no seam)
- key: after "problem.": the chain between the two carts, the Weapons Maker and the Masked Crook grinning over their handshake, war papers streaming from the bank through the WiFi into the big cart
- cue: "Cybercrime costs ten point five trillion"
- time: 19:21.1 to 19:28.7 (7.5 s)
- voiceover: "Cybercrime costs ten point five trillion dollars per year and growing at fifteen percent annually. This is not a separate problem."
- layer: B
- scene: The Masked Crook opens a laptop on the rim of the big cart; plain papers walk out of a bank, through a WiFi symbol, and come out of his laptop with the red missile seal, into the cart; then the two carts are chained together.
- wishonia: PiP, thinking-closed + thinking
- props: shopping-cart, price-tag, lobbyist, laptop, bank, wifi-symbol, papers-plain, papers-war, weapons-maker, fuse
- status: planned

Moves: "Cybercrime" → the first frame is official-murder-budget's last; the Masked Crook pops up on the rim of the big cart and opens a laptop. "ten point five trillion" → a bank stands at the right edge; plain papers walk out of its door in single file, hop into a WiFi symbol on a pole and pop out of the laptop with the red missile seal on, into the big cart, whose tag drops on: "CYBERCRIME: $10.5 TRILLION / YEAR". "fifteen percent" → the line of papers goes two abreast, then three; the tag gets a second line: "+15% / YEAR". "annually." → the big cart's wheels splay out under the weight. "separate" → the Weapons Maker and the Crook look at each other across the gap, then lean over and shake hands. "problem." → a chain snaps the two carts together. after "problem." → both grin at us.

Sound: a click as the laptop opens; squeaky paper footsteps and a pop per paper out of the laptop, faster on "fifteen"; a pat on the handshake; a clank as the chain snaps on.

On screen: "CYBERCRIME: $10.5 TRILLION / YEAR" / "+15% / YEAR". Why: the second cart is the same war, paid another way.

## Scene 4 · crypto-afternoon

- id: crypto-afternoon
- act: Off the books
- transition_in: slide left
- key: after "ransomware.": the $1.5 BILLION pile taller than the map, the missile's tag stamped PAID, the padlocked hospital's papers marching into the missile factory, the grinning skeleton on the gurney
- cue: "North Korea can't build"
- time: 19:28.7 to 19:41.9 (13.2 s)
- voiceover: "North Korea can't build an aircraft carrier, but it funds its nuclear program by stealing one point five billion dollars in cryptocurrency in a single afternoon. Russia finances military operations with ransomware."
- layer: B
- scene: On the world map, a toy aircraft carrier sinks in a washtub while the Masked Crook's laptop pours war papers onto a pile in one afternoon and pays for a missile; then a hospital is padlocked and its papers march into a missile factory.
- wishonia: PiP, neutral-smile + idle, then surprised-oh + open-palms on "single"
- props: world-map, washtub, aircraft-carrier, missile, price-tag, stamp, lobbyist, laptop, papers-war, wall-clock, factory, hospital, padlock, human, fuse
- status: planned

Moves: "North" → the label "NORTH KOREA" lands on the map. "aircraft" → a toy aircraft carrier bobs in a washtub by the label. "carrier," → it tips over and sinks; one bubble pops. "nuclear program" → a grinning missile on a stand, with a price tag: "UNPAID". "stealing" → the Masked Crook tiptoes in with his laptop. "billion" → the laptop pours war papers onto a pile: "$1.5 BILLION". "cryptocurrency" → a rubber stamp thumps "PAID" over the missile's tag. "single" → a round wall clock spins from 12 to 5 so fast it smokes. after "afternoon." → it stops with a ding; the pile is taller than the map. "Russia" → the label "RUSSIA" lands. "operations" → a small factory with missile-shaped chimneys drops in by it. "ransomware." → a padlock snaps onto the door of a hospital next to it, with a note: "RANSOM"; war papers squeeze out under the door and march into the factory, whose chimneys puff. after "ransomware." → a patient on a gurney outside the locked door x-rays into a skeleton (`KIT.xray`), still waiting, still grinning.

Sound: a thunk as each label lands; a slide-down whistle as the carrier sinks and a pop for the bubble; a cash-register ding on "billion"; a stamp thump on PAID; a whirr as the clock spins and a ding when it stops; a clank for the padlock; an x-ray zap.

On screen: "NORTH KOREA" / "UNPAID", then "PAID" / "$1.5 BILLION" / "RUSSIA" / "RANSOM". Why: two real examples of war paid for by theft.

## Scene 5 · war-through-wifi

- id: war-through-wifi
- act: Off the books
- transition_in: slide left
- key: after "better.": the tank flattened under the laptop's tower of pay, the Weapons Maker's eyes blinking out of the flat hatch, the Crook still typing
- cue: "Cybercrime is war conducted"
- time: 19:41.9 to 19:46.3 (4.5 s)
- voiceover: "Cybercrime is war conducted through WiFi, and it pays better."
- layer: B
- scene: A tank with the Weapons Maker in its hatch rolls up beside the Masked Crook's laptop; the laptop's WiFi arcs fly out as war arrows; payday drops a small pile by the tank and a tall one onto it.
- wishonia: PiP, smirk-smile + point-right
- props: tank, weapons-maker, lobbyist, laptop, wifi-symbol, papers-war, fuse
- status: planned

Moves: "Cybercrime" → the Masked Crook sits at his laptop. "war" → a tank rolls up beside him, the Weapons Maker standing in its hatch with his cigar. "WiFi," → the laptop's WiFi arcs fly out across the paper as red war arrows. "pays" → payday: a small pile of war papers drops beside the tank. after "better." → a tower of war papers drops out of the sky onto the tank and flattens it like a pancake; the Weapons Maker's eyes blink out of the flat hatch.

Sound: a click as the laptop wakes; a clank as the tank rolls up; a zap for the arrows; a thunk for the small pile; a splat when the tower lands.

On screen: nothing (the captions say it). Why: one picture for why cybercrime grows.

## Scene 6 · destroy-beats-make

- id: destroy-beats-make
- act: The destroying economy
- transition_in: slide left
- key: after "emergency.": the ribboned THINGS THAT DESTROY stack lying across the flattened crates, the Builder's hand reaching up toward the cobwebbed EMERGENCY box, the fuse spark flaring above it
- cue: "Combined, your destructive economy"
- time: 19:46.3 to 20:03.7 (17.4 s)
- voiceover: "Combined, your destructive economy is thirteen point two trillion dollars per year, eleven point five percent of global G.D.P. Both are growing faster than the part of your economy that makes things. So the part that destroys things is winning. I'm told this is not considered an emergency."
- layer: B
- scene: The two chained carts tip their war papers into one tall stack; the Masked Crook cuts an 11.5% slice out of a small Earth; the Builder stacks crates by hand beside the stack, which grows faster, wins a ribbon and falls on him; on the wall, an EMERGENCY box nobody pulls.
- wishonia: PiP, neutral-smile + idle, then sideeye-closed + arms-crossed on "emergency."
- props: shopping-cart, papers-war, earth-globe, lobbyist, human, crate, ribbon, alarm-box, fuse
- status: planned

Moves: "Combined," → the two chained carts from cybercrime-10-trillion roll in and tip all their war papers into one stack. "thirteen point two trillion" → the stack rises: "$13.2 TRILLION / YEAR". "eleven point five percent" → a small Earth beside it; the Masked Crook cuts a slice out of it like a pie, and the slice shows red inside: "11.5% OF GLOBAL GDP". "G.D.P." → he takes a bite. "growing" → beside the stack, the Builder stacks wooden crates by hand. "faster" → the paper stack grows on its own, much faster. "makes things." → the crate stack gets its label: "THINGS THAT MAKE". "destroys things" → the paper stack gets its label: "THINGS THAT DESTROY". "winning." → a winner's ribbon pins onto the paper stack. after "winning." → the stack tips over onto the crates and flattens the Builder; only his blinking eyes and one hand show. "emergency." → on the wall above, a box "EMERGENCY: PULL" under a cobweb, the spider from without-with-papers hanging off it; the Builder's hand reaches up and falls short; the fuse's spark flares right over the box. after "emergency." → nobody pulls it.

Sound: a whoosh as the carts tip; a slide-up whistle as the stack rises; a snip for the slice; a pop for the bite; hammering as the Builder stacks; a pop as the ribbon pins on; a splat when the stack lands; crickets after "emergency."

On screen: "$13.2 TRILLION / YEAR" / "11.5% OF GLOBAL GDP" / "THINGS THAT MAKE" / "THINGS THAT DESTROY" / "EMERGENCY: PULL". Why: the destroying half of the economy is growing faster than the making half.

## Scene 7 · considered-tuesday

- id: considered-tuesday
- act: The destroying economy
- transition_in: zoom out of the wall screen
- key: after "Tuesday.": the desk calendar riffled to TUESDAY, the mug on its way down, the toppled stack and the burning fuse on the wall screen
- cue: "On your planet this"
- time: 20:03.7 to 20:06.6 (2.9 s)
- voiceover: "On your planet this is considered "Tuesday."."
- layer: A
- scene: Wishonia sips coffee at the desk while the desk calendar flips to Tuesday, and flips again, and every page is Tuesday.
- wishonia: big, smirk-closed + body-idle while sipping, then smirk-smile + body-palms-down on "Tuesday"
- props: office, wall-screen, desk, mug, calendar
- status: planned

Moves: "On" → the zoom out starts on destroy-beats-make's last frame inside the wall screen (the toppled stack, the cobwebbed box, the fuse). "planet" → Wishonia lifts her mug and sips. "Tuesday" → the desk calendar (`KIT.props.calendar`) flips to "TUESDAY", then riffles on through the next pages: TUESDAY, TUESDAY. after "Tuesday." → Wishonia puts the mug down slowly.

Sound: a click per calendar page; a soft thunk as the mug lands.

On screen: "TUESDAY". Why: a breather punchline: the emergency is routine.

## Scene 8 · build-or-steal

- id: build-or-steal
- act: Build or steal
- transition_in: zoom into the wall screen
- key: after "afternoon?": the seesaw down on STEAL THINGS under the war papers and the grinning Crook, the padlocked hospital, the clock on 5, the Builder flat on his back beside his two-legged chair, the factory and the capitol upside down behind him
- cue: "When the parasitic economy grows"
- time: 20:06.6 to 20:21.6 (15.0 s)
- voiceover: "When the parasitic economy grows large enough relative to the productive one, the rational choice for any individual, company, or nation flips from "build things" to "steal things." Why spend years building a product when you can ransom a hospital in an afternoon?"
- layer: B
- scene: A seesaw, "BUILD THINGS" on one end and "STEAL THINGS" on the other; the Masked Crook sits on STEAL while war papers pile onto it; the Builder, a little factory and a little capitol hop onto BUILD and get catapulted; the Builder starts a chair while the Crook ransoms a hospital in one afternoon.
- wishonia: PiP, annoyed-closed + hands-hips
- props: seesaw, papers-war, papers-plain, lobbyist, human, factory, capitol, hospital, padlock, wall-clock, chair, fuse
- status: planned

Moves: "parasitic economy" → war papers start landing on the "STEAL THINGS" end, where the Masked Crook sits, grinning. "productive one," → a few plain papers sit on the "BUILD THINGS" end. "individual," → the Builder hops onto the BUILD end. "company," → a little factory hops on beside him. "nation" → a little capitol hops on beside it. "flips" → the war papers pile higher until the seesaw slams down on STEAL and catapults the Builder, the factory and the capitol off the top of the frame. "building" → the Builder drops back in, stars circling his head, onto a stool at a workbench; the factory and the capitol land behind him upside down. "product" → he starts a chair, slowly. "ransom" → the Crook snaps a padlock onto a small hospital's door, with a note: "RANSOM"; papers squeeze out under the door into his briefcase. "afternoon?" → the wall clock from crypto-afternoon jumps from 12 to 5; the chair has two legs. after "afternoon?" → the Builder sits on the chair to rest, and it tips him over backwards.

Sound: pops as the war papers land; a boing for each of the three riders; a slam and a slide-up whistle on the catapult; a thunk as the Builder lands; hammering; a clank for the padlock; a ding as the clock jumps; a thunk as the chair tips.

On screen: "BUILD THINGS" / "STEAL THINGS" / "RANSOM". No: not the balance scale prop; the catapult needs a seesaw (a plank on a triangle). Why: the tipping point, as a choice any human, company or nation faces.

## Scene 9 · production-irrational

- id: production-irrational
- act: Build or steal
- transition_in: slide left
- key: after "survival.": the charred Builder at a laptop beside the Crook, putting on a domino mask, the charred factory behind them with its bullseye
- cue: "Why manufacture exports"
- time: 20:21.6 to 20:38.6 (17.1 s)
- voiceover: "Why manufacture exports when hacking banks pays better? Once enough of your economy is extraction, producing anything makes you a target rather than a success. Production becomes irrational. Parasitism becomes the only means of survival."
- layer: B
- scene: The Builder loads EXPORTS crates onto a conveyor outside a small factory with a SUCCESS sign on its roof, while next door the Crook's laptop piles up more papers; the sign turns into a bullseye, a missile hits it, and the charred Builder sits down at a laptop and puts on a mask.
- wishonia: PiP, annoyed-closed + arms-crossed, then sad-small + idle on "survival."
- props: factory, sign, conveyor, crate, human, lobbyist, laptop, papers-war, missile, fuse
- status: planned

Moves: "manufacture" → the Builder loads crates onto a conveyor outside a small factory with a "SUCCESS" sign on its roof. "exports" → the crates get their stencil: "EXPORTS". "hacking banks" → next door, the Masked Crook types at his laptop, and it spits war papers into a pile. "extraction," → the Crook's pile grows past the factory roof. "target" → the "SUCCESS" sign flips over to a bullseye. "rather" → a missile appears at the top of the frame and whistles down at it. "success." → it hits the bullseye: a white flash, a boom, a mushroom cloud, the frame shakes. "irrational." → the smoke clears on the factory charred and bent and the Builder charred black, smoking, hair straight up, still holding a crate, blinking. "Parasitism" → he drops the crate and the hammer, sits down next to the Crook and opens a laptop. after "survival." → the Crook hands him a domino mask, and he puts it on.

Sound: a thunk as the crates load; typewriter clacks for the hacking; a cash-register ding for the pile; a switch click as the sign flips; a slide-down whistle and a boom; a sizzle as the smoke clears; a thunk as the crate drops and a click as the laptop opens; a pop as the mask goes on.

On screen: "SUCCESS" / "EXPORTS". Why: what the tipping point does to one worker.

## Scene 10 · failed-states

- id: failed-states
- act: Where it ends
- transition_in: slide left
- key: after "taken.": the toll gate where the factory stood, the Crook in his oversized helmet holding the hut up out of reach, the Hut Builder hammering the air
- cue: "You have a name for places"
- time: 20:38.6 to 20:56.0 (17.4 s)
- voiceover: "You have a name for places where this already happened. You call them "failed states." Somalia, Libya, parts of Syria. The productive economy collapsed, the warlord economy replaced it, and nobody can restart production because anyone who builds something gets it taken."
- layer: B
- scene: The world map with three plain labels; a factory on it folds flat, a toll gate goes up in its place, and the hut a human builds is lifted away.
- wishonia: PiP, sad-closed + idle
- props: world-map, stamp-mark, factory, toll-gate, lobbyist, papers-war, human, hut, fuse
- status: planned

Moves: "places" → the world map. "failed" → a heading stamps on over the map: "FAILED STATES". "Somalia," → the label "SOMALIA" lands. "Libya," → "LIBYA". "Syria." → "PARTS OF SYRIA" lands, tears, and only part of it stays stuck. "collapsed," → a factory on the map folds flat. "warlord" → a toll gate goes up where it stood; the Masked Crook, in an army helmet three sizes too big, collects war papers at it. "restart" → the Hut Builder walks up with planks and a hammer. "builds something" → she builds a small hut beside the gate. "taken." → the Crook's gloved hand lifts the hut off the map. after "taken." → she keeps hammering the air where it was, then looks up.

Sound: a stamp thump on the heading; a thunk as each label lands and a snip as the third one tears; a slide-down whistle as the factory folds; a clank as the gate goes up; hammering; a whoosh as the hut goes.

On screen: "FAILED STATES" / "SOMALIA" / "LIBYA" / "PARTS OF SYRIA". No: no flags, emblems or local costumes; the warlord is the Crook. Why: the end of this road already exists, on a map.

## Scene 11 · neighbors-house

- id: neighbors-house
- act: Where it ends
- transition_in: slide left
- key: after "basement.": the Watcher's house gone, the Watcher on the bare floor, charred black, smoking, hair straight up, teacup in hand, blinking; the neighbor's house a black frame
- cue: "You've watched this happen"
- time: 20:56.0 to 21:04.0 (8.0 s)
- voiceover: "You've watched this happen to individual countries the way someone watches a neighbor's house burn down while storing gasoline in their own basement."
- layer: B
- scene: Two houses side by side; the neighbor's burns down; one ember drifts over to the Watcher's house, whose basement (in a cutaway) is full of gasoline cans with the war seal.
- wishonia: PiP, sideeye-closed + arms-crossed
- props: house, human, teacup, mailbox, gas-can, fuse
- status: planned

Moves: "watches" → two houses (`KIT.props.house`) side by side, mailboxes "FAILED STATE" and "YOU"; in the window of the right one, the Watcher sips tea. "neighbor's house" → small flames start on the neighbor's roof. "burn down" → the flames grow and the neighbor's house burns down to a black frame; one ember floats up and drifts slowly toward the Watcher's house. "gasoline" → the cutaway opens: the Watcher's basement is full of red gasoline cans, each with the missile seal. "own" → the ember drifts lower, toward the basement window. "basement." → one more can rolls in, and the ember drops in through the window. A beat later: a white flash, a boom, and the house is gone; the Watcher stands on the bare floor, charred black, smoking, hair straight up, still holding the teacup, blinking.

Sound: a fire whoosh as the roof catches and a bigger one as it burns; a clank as the cutaway shows the cans and another as the last can rolls in; a boom; a sizzle as the Watcher smokes.

On screen: "FAILED STATE" / "YOU" on the mailboxes. Why: the viewer's country is the next house.

## Scene 12 · try-all-three

- id: try-all-three
- act: Where it ends
- transition_in: slide left
- key: at the end: all three crossed out, the charred Watcher on the rug, leaning into the headset microphone
- cue: "Once it starts, you can't"
- time: 21:04.0 to 21:11.5 (7.4 s)
- voiceover: "Once it starts, you can't vote your way out, innovate your way out, or give a TED Talk about it. (You will try all three.)."
- layer: B
- scene: A ballot box, a light bulb and a round rug with a headset microphone each get a red ✗; then the charred Watcher from neighbors-house runs to all three anyway.
- wishonia: PiP, neutral-smile + counting, then eyeroll-smile + shrug on "try"
- props: ballot-box, light-bulb, stage, human, fuse
- status: planned

Moves: "vote" → a ballot box (`KIT.props.ballotBox`) drops in. "out," (first) → a red ✗ slashes across it. "innovate" → a light bulb drops in. "out," (second) → ✗. "TED Talk" → a plain round rug with a headset microphone on a stand drops in. "it." → ✗. "(You" → the charred Watcher from neighbors-house runs in, still smoking. "try" → he stuffs a ballot into the box, and the box spits it back in his face. "all" → he runs to the bulb and grabs it; it zaps him: a flash of his x-rayed skeleton; then he hops onto the rug and taps the microphone, tap, tap, tap, to nobody. "three" → he leans in to speak.

Sound: a thunk as each thing drops in; a marker squeak on each ✗; a pop as the ballot spits back; a whistle as he runs; a zap; three taps.

On screen: three red ✗ marks (drawn as SVG), no words. Why: the three usual answers, ruled out, with the joke that humans will try them anyway.

## Scene 13 · 25-percent-by-2033

- id: 25-percent-by-2033
- act: The Soviet comparison
- transition_in: slide left
- key: after "one.": the needle back on 11.5%, the lit red zone at 25% with 2033 in the year window, the SOVIET UNION: COLLAPSED mark at 15% with its MILITARY ONLY tag, the crank computer missing its crank, the PLAN binder with its TERRIBLE sticker
- cue: "At current growth rates"
- time: 21:11.5 to 21:30.8 (19.4 s)
- voiceover: "At current growth rates, your destructive economy reaches twenty-five percent of G.D.P. by twenty thirty-three. The Soviet Union collapsed at fifteen percent of G.D.P. in military spending alone. They had worse technology, a smaller parasitic sector, and a plan. It was a terrible plan, but they had one."
- layer: B
- scene: A big gauge (`KIT.props.gauge`) with a needle and a year window; the needle swings to 25% by 2033 and back; a mark at 15% reads "SOVIET UNION: COLLAPSED", with a crank computer and a thick binder labeled "PLAN" beside it.
- wishonia: PiP, thinking-closed + thinking, then smirk-closed + point-right on "terrible"
- props: gauge, tv-set, gears, plan-binder, sticker, fuse
- status: planned

Moves: "current" → a big gauge, "% OF GDP", its needle on 11.5% (the slice from destroy-beats-make). "twenty-five" → a red zone at 25% lights up. "thirty-three." → the year window spins to "2033" and the needle swings up into the red zone. after "thirty-three." → the gauge rattles and puffs steam. "Soviet" → the needle drops back to 11.5%, and a mark drops in at 15%: "SOVIET UNION: COLLAPSED". "alone." → the mark gets a tag: "MILITARY ONLY". "technology," → beside the mark, a clunky old computer (a 1950s TV cabinet on a box of gears) cranks itself, puffing. "smaller parasitic sector," → a tiny red sprout pokes up beside it. "plan." → a thick binder lands next to it: "PLAN". "terrible" → a "TERRIBLE" sticker slaps onto the binder. after "one." → the binder stands up straight, proud, and the crank falls off the old computer.

Sound: a switch click as the red zone lights; a whirr as the year window spins and a sizzle for the steam; a thunk as the mark drops in; a pop for the tag; a thunk for the binder; a splat for the sticker; a clank as the crank falls off.

On screen: "% OF GDP" / "25%" / "2033" / "SOVIET UNION: COLLAPSED" at 15% / "MILITARY ONLY" / "PLAN" / "TERRIBLE". Why: a known collapse point, and the viewer's economy heading past it.

## Scene 14 · no-plan

- id: no-plan
- act: The Soviet comparison
- transition_in: same form (no seam)
- key: after "lost.": the Soviet side a smoking heap of rubble under the 15% mark with the WINNER ribbon on top, the Politician grinning beside it with his empty clipboard and a thumbs-up, the red vine round the gauge, the needle one notch higher
- cue: "You are approaching their ratio"
- time: 21:30.8 to 21:43.3 (12.5 s)
- voiceover: "You are approaching their ratio with better technology, a faster-growing parasitic sector, and no plan. The Soviet Union's terrible plan beat your no plan, and the Soviet Union lost."
- layer: B
- scene: The same gauge; on the "YOU" side a shiny laptop, a fast red vine of war papers and the Politician with an empty clipboard; the terrible plan wins a ribbon, then the whole Soviet side crumbles.
- wishonia: PiP, smirk-closed + idle, then eyeroll-closed + shrug on "lost."
- props: gauge, laptop, vine, papers-war, politician, clipboard, ribbon, plan-binder, tv-set, fuse
- status: planned

Moves: "You" → the first frame is 25-percent-by-2033's last. "approaching" → a "YOU" sign goes up on the other side of the gauge; the needle creeps from 11.5% toward the 15% mark, tick, tick. "technology," → a shiny laptop lands on the YOU side. "faster-growing" → a red vine of war papers shoots up the gauge and wraps round it. "no" (first) → the Politician pops up on the YOU side, grinning, holding a clipboard: "PLAN:" and nothing after it; the fuse's spark flares. "beat" → a ribbon pins onto the Soviet binder: "WINNER". "lost." → the Soviet side crumbles: the binder and the crank computer collapse into a smoking heap of rubble under the 15% mark, and the WINNER ribbon floats down and lands on top. after "lost." → the Politician gives the rubble a thumbs-up, and the needle ticks up one more notch.

Sound: two ticks as the needle creeps; a thunk for the laptop; a slide-up whistle for the vine; a boing for the Politician; a pop for the ribbon; a slide-down whistle and a slam as the Soviet side falls; one more tick.

On screen: "YOU" / "PLAN:" / "WINNER". Why: the punchline: humans are doing worse than a system that already failed.

## Scene 15 · loop-not-line-item

- id: loop-not-line-item
- act: The loop
- transition_in: slide left
- key: after "spending.": all six stations lit, war papers running the ledger loop so fast they fly off the bends, the PRICES balloon just popped
- cue: "This is a loop, not"
- time: 21:43.3 to 22:02.4 (19.1 s)
- voiceover: "This is a loop, not a line item. Your governments print money to fund military spending, which devalues wages through inflation, which makes legitimate work pay less, which pushes talent toward cybercrime, which grows the destructive economy, which justifies more military spending."
- layer: B
- scene: One line of a ledger page peels off and curls into a ring with six stations; war papers run round it as each station lights up, and the loop speeds up.
- wishonia: PiP, thinking-closed + presenting
- props: ledger-loop, printing-press, politician, balloon, human, papers-plain, laptop, papers-war, weapons-maker, missile, fuse
- status: planned

Moves: "line" → a ledger page; one line, "MILITARY", peels off. "item." → it curls into a big ring standing on the paper, with six empty stations round it. "print" → station 1: the 1913 printing press from Part 10; the Politician turns its crank, and war papers pop out and start running clockwise round the ring. "inflation," → station 2: a balloon marked "PRICES" inflates, bigger and bigger. "pay less," → station 3: the Builder holds out his paycheck (a plain paper), and it shrinks to a sliver, as in Part 10's paycheck-shrinks. "cybercrime," → station 4: the Builder puts on his domino mask and sits at a laptop. "destructive economy," → station 5: the THINGS THAT DESTROY stack grows. "more" → station 6: the Weapons Maker cradles a new missile; the papers run back to the press. after "spending." → the loop speeds up until papers fly off the bends, and the PRICES balloon pops.

Sound: a whoosh as the line peels off; a whirr as the press turns; a slide-up whistle as the balloon inflates; a squeak as the paycheck shrinks; a click for the laptop; a cash-register ding for the stack; a clank for the missile; a whoosh as the loop speeds up; a pop for the balloon.

On screen: the six station labels "PRINT MONEY" / "INFLATION" / "WORK PAYS LESS" / "TALENT TO CYBERCRIME" / "DESTRUCTIVE ECONOMY GROWS" / "MORE MILITARY SPENDING". Why: the parts of the problem feed each other.

## Scene 16 · thats-homework

- id: thats-homework
- act: The loop
- transition_in: slide left
- key: after "math.": the Kid in his tiny domino mask at the school desk, the worksheet "HACK < FIGHT" with its gold star, the Politician at the chalkboard grinning
- cue: "Every nation you've bombed"
- time: 22:02.4 to 22:16.2 (13.8 s)
- voiceover: "Every nation you've bombed or sanctioned has learned that parasitizing your economy is cheaper than fighting you conventionally. That's not crime. That's homework. You built the incentive structure and they did the math."
- layer: B
- scene: Bombs and a SANCTIONED stamp land on the world map; two price tags compare fighting with hacking; then a small kid in a tiny domino mask does the sum at a school desk while the Politician, as the teacher, has the lesson on the chalkboard.
- wishonia: PiP, sideeye-closed + hands-hips
- props: world-map, bomb, stamp, stamp-mark, price-tag, tank, laptop, human, school-desk, chalkboard, politician, pencil, fuse
- status: planned

Moves: "nation" → the world map; three cartoon bombs whistle down onto it. "bombed" → they go off as three tiny mushroom clouds. "sanctioned" → a giant rubber stamp thumps "SANCTIONED" across a country. "cheaper" → two price tags: "FIGHT: $$$$$" hangs on the flattened tank from war-through-wifi, and "HACK: $" on a laptop. "conventionally." → the FIGHT tag is so heavy it squashes the flat tank flatter. "crime." → a "CRIME" label slides in; after "crime." → a red line crosses it out. "homework." → a small school desk drops in; at it, the Kid, in his tiny domino mask, opens the laptop next to a worksheet: "HOMEWORK". "built" → behind him, the Politician, as the teacher, chalks the two prices on a chalkboard: "FIGHT: $$$$$ / HACK: $". "did the math." → the Kid writes "HACK < FIGHT". after "math." → the Politician sticks a gold star on the worksheet, grinning; the Kid beams.

Sound: a slide-down whistle as the bombs fall and three pops; a stamp thump; a splat as the tag squashes the tank; a marker squeak for the cross-out; a thunk as the desk lands; a pencil scratch; a sparkle for the gold star.

On screen: "SANCTIONED" / "FIGHT: $$$$$" / "HACK: $" / "CRIME" crossed out / "HOMEWORK" / "HACK < FIGHT". Why: the other side's response is rational; the loop runs on incentives, not villains.

## Scene 17 · defund-the-loop

- id: defund-the-loop
- act: The loop
- transition_in: slide left
- key: after "it.": the empty ledger loop lying on its side, medicine papers filing into the lab, the factory clean with its SUCCESS sign, the Weapons Maker's missile asleep on the ground, the fuse out and smoking in the corner
- cue: "The treaty breaks this loop"
- time: 22:16.2 to 22:34.0 (17.8 s)
- voiceover: "The treaty breaks this loop. Redirect the war money to medical research, make the productive economy so rewarding that crime becomes irrational, and defund the war machine that manufactures the poverty that feeds the cycle. You don't outlaw the loop. You defund it."
- layer: B
- scene: The loop from loop-not-line-item, still spinning; the treaty drops into it like a railroad switch and sends the war papers off the ring into the color-flip funnel; they come out as medicine papers and walk to a lab; the factory gets its SUCCESS sign back, the Builder and the Kid take off their masks, the missile factory's chimneys go out, and the empty loop rolls over and stops; the fuse goes out.
- wishonia: PiP, happy-smile + presenting, then skeptical-smile + arms-crossed on "outlaw", then happy-smile + excited on "defund" (the second)
- props: ledger-loop, scroll, color-flip-funnel, papers-war, papers-med, lab, scientist, factory, sign, human, laptop, weapons-maker, missile, politician, fuse
- status: planned

Moves: "The" → the loop as loop-not-line-item left it, spinning, war papers running round it. "treaty" → a treaty scroll (`KIT.props.scroll`) unrolls and folds itself into a railroad switch. "breaks" → it drops into the ring; the papers running round hit it and are sent off the ring. "Redirect" → they run down a chute into the color-flip funnel (`KIT.props.colorFlipFunnel`). "medical" → they come out with the teal cross seal. "research," → they walk into a lab, where the Scientist holds the door and waves them in. "productive economy so rewarding" → more medicine papers walk into the factory from production-irrational, which is clean again, and its "SUCCESS" sign flips back up. "crime" → the Builder pulls off his domino mask and walks back to the factory. "irrational," → the Kid from thats-homework shuts his laptop, takes off his little mask and follows the papers to the lab. "defund" (first) → the missile factory's missile-shaped chimneys go out one by one. "cycle." → the Weapons Maker looks round for papers, finds none, and lays his missile down like a sleeping baby. "outlaw" → the Politician nails an "ILLEGAL" sign onto the ring; the last war paper runs straight past it, still going round. "defund" (second) → that paper hits the switch, goes down the funnel and comes out teal. after "it." → the empty loop wobbles, rolls over like a dropped hoop and lies still; in the corner, the fuse's spark sputters out in a puff, the stub droops, and the Earth lets out one smoke ring.

Sound: a whoosh as the scroll unrolls; a clank as the switch drops in; a ding as the seals flip; a cash-register ding for the SUCCESS sign; a click as the Kid's laptop shuts; a sizzle as the chimneys go out; hammering for the ILLEGAL sign; a ding for the last flip; a clank as the loop falls over; a sizzle as the fuse goes out.

On screen: "ILLEGAL". Why: the fix: take the money out of the loop instead of passing a law against it.
