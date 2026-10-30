---
format: 1920x1080
duration: 0:39.7
message: "The human economy prints papers from nothing, hands them to weapons makers, and has killed 310 million people in wars along the way."
arc: Title card (the emblem's papers run in circles) → Wishonia promises something magnificent → the camera travels the money loop stop by stop, and the bomb chars the family the loop then pays and feeds → the family turns to skeletons in a field of headstones under 310,000,000 (HOLD) → Wishonia conjures a sandwich straight into a hungry human's hands
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 2, "The Human Economy"
audio: index-manual.cbaf659d.mp3, 04:18.5 to 04:58.2
version: v3
---

# Part 2 storyboard: "The Human Economy"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("money-loop: hold the tray longer"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The part is a 1950s atomic-age instructional film. Layer A is the host's studio set (`KIT.studio`): Wishonia large at her navy lectern, in front of the mustard wall and its spotlight pool. Layer B is the illustrated plates the camera travels over (`KIT.camera`), one framing per phrase; Wishonia is not in them, she is the voice. Money is green, and its seal says what it buys: every paper in this part has a missile seal (war money). Part 2 is built (`../parts/part-02.json`, `../compositions/scenes/part-02/`) and is the reference for every kind of shot, so this storyboard describes its five scenes as they are.

**Spine.** The war papers going round. They run round the title card's orbits, pop out of a press with an empty tray, march into the weapons factory, come back out of a pay window in the rubble, buy bread, and walk back round the road toward the press. The road is a loop, and on "economy" the camera pulls back to show it whole. The family that lives on the loop carries the story from the bomb to the toll: they wave at the missile, stand there charred, get paid, buy bread, and in the-toll turn into skeletons still holding the loaves.

**Callbacks.** From Part 1 (without-with-papers): the moth from the hungry human's empty wallet flutters up out of the press's empty paper tray; the wheat that grows by itself shoots up beside the farm stand, and this time a price tag drops onto it; the hungry human with nothing is host-closes's guest, his pockets turned out. From the theme song: the bomb goes off and the humans stand there charred black, hair straight up, blinking. The iris (style bible, gag 6): host-opens irises in on Wishonia's face and host-closes irises out on it.

**Set up here.** The hungry human and his club sandwich with one bite gone: he walks into Part 4's less-crazy-goal still eating it, and debug-37-trillion-cells dives into him, so draw both from host-closes.html (`MAN`: `{ kind: "shirt", head: "long", hairStyle: "short", tone: 2, color: 2, build: { tw: 0.72, legs: 1.18, th: 1.12, neck: 1.6, hs: 0.95, nose: 1.5 } }`, pockets turned out; `sandwich()`). The Politician cranking the printing press with the empty tray (`KIT.props.printingPress({ seal: "war", tray: 0 })`) comes back as the 1913 press in nothing-papers (Part 10) and as a station of Part 11's loop (loop-not-line-item). The Weapons Maker's smiling baby missile and the factory whose chimneys are smiling missiles (`KIT.props.factory`) come back wherever weapons get made. The loop road with stops on it comes back as Part 6's loop (democracy-dog-loop) and Part 11's (loop-not-line-item).

**Held frame.** the-toll, from after "million" (the number has landed and the pull-back has settled) until the cut to host-closes on "On". Nothing moves and nothing sounds while the narrator finishes "of you in your assorted wars."

**Transitions.** The title card comes up from black and goes down to black; host-opens irises in on Wishonia's face. Cuts from host-opens to the plate, from the plate to the-toll, and from the-toll back to the set. host-closes irises out on her face to black, so Part 3's title card comes up from black.

**Bans for this part.**
- The factory has no sign (`label: ""`, though the prop draws one by default) and the pay window none. The only text in the plates is the price tag's "$", the dollar signs in the Weapons Maker's eyes and "310,000,000".
- Every paper in the part is war money; no medicine money and no seal flip yet.

## Changes from v2

- Wishonia's office, the cream paper diagrams and her corner (PiP) are gone. She hosts from her lectern in two host shots, host-opens and host-closes, and the money loop is one illustrated plate, a looping road the camera travels round.
- A new host shot, host-opens, takes "Humanity has created something magnificent" to the camera, so the loop starts on "You print".
- The labels went with the diagram: no 1ST PRIZE rosette, no MONETARY POLICY plaque (the Politician grins at us instead), no JOBS sign with air quotes (the pay window pops up out of the rubble), no THE ECONOMY banner (the pull-back that shows the road is a loop is the joke).
- The title card is the period card: the economy's first picture is the emblem's three papers running round their orbits, going nowhere, instead of a hamster-wheel O.
- The death toll is its own plate: the charred family from the loop x-rays into skeletons in a field whose headstones rise row after row to the horizon, instead of a gray circle with headstone dashes.
- The sandwich is a conjuring trick: it appears on Wishonia's palm and hops straight into the hungry human's hands on the set. No wall screen, no skulls turning to stare, no mug sip; the part ends on an iris out.

## Scene 1 · title-card

- id: title-card
- act: Title
- transition_in: up from black (the head of a reel)
- key: the whole heading on the navy card under the emblem, its three war-seal papers running round their orbits
- cue: "The Human Economy"
- time: 04:18.5 to 04:20.8 (2.3 s)
- voiceover: "The Human Economy."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem at the top (three cream orbits round an orange nucleus) and the heading under it in Fraunces, cream with a navy drop shadow. Heading lines, 16:9: "THE HUMAN" (style small) / "ECONOMY"; 9:16: the same two lines. The small gag is the emblem: its three electrons are little war-seal papers running round their orbits on stick legs, going nowhere.
- props: title-card, money (war)
- status: planned

Moves: "The" → the card comes up from black (0.35 s) with the whole heading already on it, and the camera pushes in slowly (to 1.045) for the whole shot. "Human" → the three papers run round their orbits, legs flicking, at different points round the atom, and keep running. after "Economy." → the card goes down to black in its last quarter second.

Sound: a whirr under the running papers, from "Human".

On screen: "THE HUMAN ECONOMY". Why: the narrator reads the heading, and the emblem shows the economy before anyone explains it: money running in circles, going nowhere.

## Scene 2 · host-opens

- id: host-opens
- act: The economy
- transition_in: iris in on her face
- key: on "magnificent:": Wishonia throws her arms wide at the lectern, excited, and the spotlight pool behind her swells a notch
- cue: "Humanity has created something magnificent"
- time: 04:20.8 to 04:24.2 (3.4 s)
- voiceover: "Humanity has created something magnificent:"
- layer: A, host
- scene: The host's set (`KIT.studio`): the mustard studio wall with its spotlight pool, a rust chair rail over the tan dado, and Wishonia large behind the navy lectern with the cream atom on its front. Nothing on the lectern.
- wishonia: big, happy-smile + body-presenting; excited-ee + body-wide-gesture on "magnificent:"
- props: studio, lectern
- status: planned

Moves: "Humanity" → the iris opens on her face (in the first 0.7 s) while she presents, and the camera pushes in slowly on her face for the whole shot (1 to 1.07). "magnificent:" → she throws her arms wide and the studio light comes up a notch: the spotlight pool swells behind her with a springy overshoot, a showroom reveal. The reveal is the cut: the magnificent creation turns out to be a man cranking a press with an empty tray.

Sound: none; her voice carries it.

On screen: nothing but the set. No: no props on the lectern and no guest. Why: the host sells the set-up to the viewer herself, and the light oversells it for the cut.

## Scene 3 · money-loop

- id: money-loop
- act: The economy
- transition_in: cut
- key: after "everything.": the house flat, the mushroom cloud standing over the rubble, and the family in front of it on the road, charred black and smoking, hair straight up, only their eyes blinking
- cue: "You print papers from nothing"
- time: 04:24.2 to 04:44.3 (20.1 s)
- voiceover: "You print papers from nothing (called "monetary policy"). You give these nothing-papers to weapons makers. They make things that destroy everything. This creates "jobs" which give people papers. People use papers to buy food (which grows for free). This is called "the economy"."
- layer: B, plate loop-road
- scene: One plate: a stadium-shaped cream road with a dashed center line on a plain tan field (straights from x -850 to 850 at y -640 and 640, bends of radius 640; everyone drawn at scale 1.5). Behind the top straight, left: the printing press (`KIT.props.printingPress`, war seal, empty tray, mirrored so its crank wheel faces left) with the Politician at the wheel; right: the Weapons Maker's factory (`KIT.props.factory`, no sign; its three chimneys are smiling missiles) with the Weapons Maker standing at its door cradling his smiling baby missile. Inside the loop behind the bottom straight, right: a little house (`KIT.props.house`, variant 2) with the family of three on the road in front of it (a father in a shirt, a mother in a dress, a small kid); left: the farm stand (a striped rust-and-cream awning on two posts over a plank counter piled with loaves), a farmer in overalls, a straw hat and a mustache behind it, and a bare patch of field to its left where the wheat will grow. The papers (`KIT.money("war")`) walk the road. The camera travels clockwise round the loop, one framing per phrase, and ends on all of it.
- props: money (war), printingPress, politician, moth, factory, weaponsMaker, missile, house, nuke, pay window, farm stand, farmer, bread, wheat, priceTag
- status: planned

Moves: "print" → framing on the press: the Politician cranks the wheel, the press's plate stamps down once a turn, and three papers pop out one after another on "print papers from", hop down onto the road and wait in line, jogging on the spot. "nothing" → the camera pushes into the press's paper tray: it is empty, and a moth flutters slowly up out of it in a lazy zigzag; no paper comes out while we look. "policy" → the camera swings to the Politician: still cranking, he turns his head to us and grins, all teeth, until "makers"; three more papers pop out behind him. "give" → the six papers march off right along the road, and the camera travels with them past the press to the factory, where they file in through the door one by one, rising and fading into it. "makers." → a close-up on the Weapons Maker's face: his eyes ring up dollar signs. "make" → the camera pulls back to him at his door, and he lets his baby missile go: it hops up out of his arms, points its nose up and flies off in a big arc trailing puffs of smoke, and the camera chases it round the bend. "destroy" → it comes down on the little house, and the family on the road in front of it waves at it. "everything." → BOOM: a white flash, the frame shakes, and a mushroom cloud stands over the house. after "everything." → the house is flat rubble, and the family stands in front of it charred black and smoking, hair straight up, only their eyes blinking; the cloud holds over them until "This", then thins away. "This" → the camera moves along to the rubble. "jobs" → a pay window (a little yellow booth with a rust roof) pops up out of the rubble beside them, and its shutter rolls up. "give" (second) → a hairy forearm with a missile tattoo reaches out of the window holding a fan of three papers, and each of the family takes one and holds it up. after "papers." → the arm pulls back in, and the family marches left along the road to the farm stand, the camera with them. "buy" → each one hands its paper up onto the counter and a loaf hops back into its hands; they munch. "grows" → the camera leaves the stand for the bare patch of field beside it, and the wheat shoots up by itself, stalk after stalk, with a springy overshoot. after "free)." → a price tag with a "$" on it drops in on its string from above the frame, lands on the middle stalk with a little bounce and swings. "This" (second) → the camera pulls back, and back. "economy". → the whole picture: the road is a loop. The papers the family paid hop down off the counter and walk off round the bend toward the press, and the press's next batch heads off to the factory. after "economy". → the factory's middle chimney, a smiling missile, lifts off on a flame: the next one.

Sound: a stamp thump on "print"; a cash-register ding on "makers."; a slide whistle down as the missile comes down, just after "that"; the boom on "everything."; a service bell as the pay window pops up on "jobs"; a pop as the papers land in the family's hands ("papers."); a slide whistle up as the wheat grows; a ding as the price tag lands; a whistle as the next missile lifts off after "economy".

On screen: the "$" on the price tag and the dollar signs in the Weapons Maker's eyes; nothing else. Why: the whole money loop as one road the camera travels, one stop per phrase, so later parts can come back to any stop on it.

## Scene 4 · the-toll

- id: the-toll
- act: The economy
- transition_in: cut
- key: during the HOLD: three grinning skeletons holding their loaves in a gray field of headstones that runs to the horizon, "310,000,000" in the sky, only the bread in color
- cue: "One downside of this system"
- time: 04:44.3 to 04:50.8 (6.6 s)
- voiceover: "One downside of this system is that it has killed three hundred and ten million of you in your assorted wars."
- layer: B, plate headstone-field
- scene: A second plate: an empty field (tan ground, a cream sky, the horizon high in the frame) with the charred family from the loop, at the loop's scale, close in the middle, each holding its loaf. Rows of headstones lie hidden in the field, receding toward a vanishing point on the horizon. The number stands in the sky, fixed to the screen, not to the plate.
- props: person (charred, skeleton), xray, bread, headstones
- status: planned

Moves: "One" → close on the charred family on the empty field, munching their loaves. "downside" → they stop chewing. "killed" → one after another they x-ray into skeletons that keep their grins and their loaves, and the field and the sky drain to gray; only the bread keeps its color. "three" → the camera pulls back while rows of headstones rise out of the field behind them, row after row from the front to the horizon. "million" → "310,000,000" stamps into the sky. Then HOLD: nothing moves from after "million" until the cut on "On".

Sound: an x-ray zap on "killed"; a thunk as the number lands on "million"; then silence for the HOLD.

On screen: "310,000,000". No: no words under the number. Why: the cost of the loop as one number, on the people we just watched it pay and feed, and the one thing that came through fine is the bread.

## Scene 5 · host-closes

- id: host-closes
- act: On my planet
- transition_in: cut
- key: after "probably": the hungry human takes an enormous bite out of the club sandwich beside the lectern while Wishonia smirks
- cue: "On my planet"
- time: 04:50.8 to 04:58.2 (7.4 s)
- voiceover: "On my planet, we skip the mass murder step and just give people food directly, but that's probably too advanced for you."
- layer: A, host
- scene: The host's set again (the same code as host-opens), with a guest on the free wall right of the lectern: a skinny hungry human with his pockets turned out (no papers, so never in the loop), facing her. A tall 1950s club sandwich (three slices of bread, ham and cheese, tomato and lettuce, a toothpick with an olive on top).
- wishonia: big, smirk-smile + body-open-palms; happy-smile + body-presenting on "give"; smirk-closed + body-idle on "but"; sideeye-closed + body-idle on "you."
- props: studio, lectern, person (the hungry human), sandwich
- status: planned

Moves: "On" → back on the set, palms open; the camera pushes in slowly on her face (1.02 to 1.08). "skip" → the hungry human walks in from the right, legs swinging, and stops beside the lectern facing her, worried, hands at his turned-out pockets. "give" → she presents her palm, and a club sandwich pops into being on it like a conjuring trick; he holds his hands out. "directly," → it hops straight across into his hands in one spinning arc. "but" → he turns it over and back, looking for the price tag; there is none; he looks at us, brows up. "probably" → he takes an enormous bite out of its side and chews, smiling, bobbing. "you." → she side-eyes the camera; after "you." the film irises out on her face, to black.

Sound: a sparkle as the sandwich appears on "give"; a pop as it lands in his hands on "directly,".

On screen: nothing but the set and the guest. No: no price tag on the sandwich; its missing is the joke. Why: the alternative in one action: the food goes straight from the one who has it to the one who needs it, and the mass murder step was optional all along.
