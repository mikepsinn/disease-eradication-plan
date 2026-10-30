---
format: 1920x1080
duration: 2:38.6
message: "Humans call moving 1% of murder money to medicine crazy, but war is the largest coordinated effort your species undertakes, and ending it only requires not doing it."
arc: Title card → the sign-holder gets netted → curing disease is the real hard job → sane / insane → the diagnostic criteria → the padded cell: what you tell the orderly → the war supply chain → the chain goes dark (HOLD) → rocks manage peace → the real obstacle is one billionaire and a PDF
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 4, "What to Do When They Try to Institutionalize You"
audio: index-manual.cbaf659d.mp3, 06:28.4 to 09:07.0
version: v2
---

# Part 4 storyboard: "What to Do When They Try to Institutionalize You"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's office; Layer B is the printed Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The patient. One everyday human, the same in every scene (`KIT.person({ tone: 1, outfit: "shirt", color: 3 })`: a mustard shirt, slick hair, a plain build), carries the part. He holds up the 1% sign in butterfly-net and the Orderly nets him; he is the straitjacketed contestant who drops through the trapdoor in sane-insane-buzzer; he lands in the padded cell in orderly-door-slot, works one arm free, draws the war supply chain on the padded wall in war-supply-chain, and switches it all off in chain-goes-dark.

**Running gag.** The Orderly's long neck (his cast tell, `KIT.cast("orderly")`). It rises behind a hedge like a periscope in butterfly-net, lifts his eyes into the door window in orderly-door-slot, follows the chain box to box in war-supply-chain, pushes his whole head through the window on "largest", and ducks under the door frame in chain-goes-dark.

**The thrown rock.** centrifuge-vs-rocks ends with a human hurling the rust rock off the right edge; it flies into billionaire-pdf and dents the STOP sign.

**Callbacks.** From Part 2 (food-directly): the walking human in debug-37-trillion-cells eats Wishonia's sandwich (one bite already gone) the whole time. From Part 1 (eligible, earth-means-dirt): the case file in diagnostic-criteria is the same folder, "~~EARTH~~ DIRT: CASE #847" with the "MAY BE ELIGIBLE FOR OPTIMIZATION" stamp on its cover. From Part 1 (title-card): the half-sun sinks again in diagnostic-criteria, this time because the office pulls away from Earth. Set up for Part 5: the Rich Human who lights his cigar with the PDF in billionaire-pdf, the UNREALISTIC sticker still on his forehead, is the one Step 1 asks for papers.

**Held frames.** diagnostic-criteria, from "nailed" to "So": the file closes slowly, nothing else moves, no sound. chain-goes-dark, from "NOT": nothing moves until "Building" in centrifuge-vs-rocks.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.
- The last human who suggested universal love and peace is text only on a file page; never drawn, no cross, no wood.
- Money is always money green (`KIT.money`); war money carries the red missile seal, medicine money the teal cross seal.

## Changes from v1

- The humans are the theme song's stereotypes: the Orderly nets the sign-holder, the Weapons Maker reads the news, the Politician hosts the game show, the Scientist is the tiny technician, the Loud Human runs the propaganda box, the Rich Human is the fat cat.
- The sign-holder is THE PATIENT, with fixed options so he looks the same everywhere. He drops through the game-show trapdoor into the padded cell, in a straitjacket.
- Gags pushed to the end: the missile on the "laws of nature" chart goes off; the liver simulation catches fire; the germ eats the treatment; the other humans in the supply chain are blown up and keep waving; the bomb cascade vanishes with its foreman; a human throws a rock and resets the peace counter; the Rich Human lights his cigar with the PDF.
- The chain of boxes is a Ferris wheel whose rim is a paper-doll chain of humans holding hands; it turns on "forever" and stops dead on "NOT".
- The title card cuts in (Part 3 ends on Layer B paper), and butterfly-net slides in after it, as in Part 1.
- Text cards the captions already say are cut ("ANNUALLY, FOREVER", the banner, the BUILDING / NOT BUILDING card).
- Sound lines added.

**Transitions.** Layer B is the footage on Wishonia's wall screen. Office to Earth zooms into the wall screen; Earth to office zooms out of it. Earth to Earth slides left. A scene that continues the last one ("same form (no seam)") starts on its last frame.

## Scene 1 · institutionalize-title

- id: institutionalize-title
- act: Title
- transition_in: cut (Part 3 ends on Layer B paper; the parts join on this cut)
- key: after "You.": all nine words in, INSTITUTIONALIZE buckled into its straitjacket straps
- cue: "What to Do When They"
- time: 06:28.4 to 06:32.2 (3.8 s)
- voiceover: "What to Do When They Try to Institutionalize You."
- layer: A, title card
- scene: The title card (`KIT.titleScene`): the navy wall, the rising sun and the stars, with the part's heading in the cover font.
- props: title-card
- status: outline

Moves: "What" → the heading slams in, one word per spoken word. "Institutionalize" → the long word lands too wide for the card; two canvas straps with buckles whip around it and cinch until the letters squash together and fit. after "You." → two pupils appear in the O of YOU and dart left, then right.

Sound: a thunk on each slammed word (What, Do, They, Try, Institutionalize, You); a squeak as the straps cinch and a click as the buckles shut.

On screen: "WHAT TO DO WHEN THEY TRY TO INSTITUTIONALIZE YOU". Why: the narrator reads the heading aloud.

## Scene 2 · butterfly-net

- id: butterfly-net
- act: They call you crazy
- transition_in: slide left
- key: after "weather.": the missile on the TV chart has gone off, the tiny human charred and blinking, the crowd nodding; the Orderly's head up over the hedge behind the patient
- cue: "When you suggest moving"
- time: 06:32.2 to 06:49.9 (17.7 s)
- voiceover: "When you suggest moving one percent of murder money to medicine money, other humans will have you committed. Most humans have been programmed by their news boxes to believe war is a law of nature, like gravity or weather. They will assume your brain is malfunctioning."
- layer: B
- scene: A street corner. Left, the patient holds up a hand-lettered 1% sign, with a hedge behind him. Right, a crowd of everyday humans on a sofa stares at a TV set whose news anchor is the Weapons Maker in a necktie, cradling his missile. Behind the hedge, the Orderly waits with a butterfly net.
- wishonia: PiP, neutral-smile + body-idle, then skeptical-closed + body-arms-crossed on "malfunctioning"
- props: human, protest-sign (`KIT.props.sign`), color-flip-funnel, money (war, med), orderly, butterfly-net, tv-set, weapons-maker, missile, sofa
- status: outline

Moves: "suggest" → the patient raises the sign: "1%" over a little war-seal bill, the color-flip funnel and an empty spot. "murder" → the little bill hops into the funnel; "money," (second) → it pops out with a teal cross seal. "committed." → behind the hedge, the Orderly's head rises on his long neck like a periscope, and his long arms lift a butterfly net. "programmed" → wires spring out of the back of the TV and plug into the backs of the crowd's heads, one after another; their eyes go flat. "news boxes" → the TV switches on: the Weapons Maker, in a necktie over his barrel chest, reads the news with his missile in his arms, grinning around the cigar. "war" → the TV shows a chart, "LAWS OF NATURE", in three panels; panel 1, "WAR": a missile hangs over a tiny human. "gravity" → panel 2: an apple drops on a tiny human's head. "weather." → panel 3: a rain cloud rains on a tiny human. after "weather." → back in panel 1 the missile drops: a white flash fills the TV, a little mushroom cloud, and the tiny human stands charred black and smoking, hair straight up, blinking. The crowd nods along, satisfied, wires bobbing. "assume" → every head on the sofa turns slowly, wires and all, to the patient. "brain" → the patient's chest light blinks red. "malfunctioning." → the whole crowd points; the Orderly tiptoes out from the hedge and swings the net down over the patient. after "malfunctioning." → the Orderly carries him off in the net like a prize butterfly, the 1% sign sticking out of the mesh.

Sound: a pop as the sign goes up; a boing as the bill hops in and a sparkle as it comes out teal; a squeak as the Orderly's neck rises; a click per wire; a TV switch; a whoosh as the chart slides in; a boing on the apple; a boom when the missile goes off; a whoosh as the heads turn; a dashboard ding for the chest light; a whoosh and a pop for the net; a whistle as he is carried off.

On screen: "1%" (the sign) / "LAWS OF NATURE" / "WAR" / "GRAVITY" / "WEATHER" (the chart). Why: the first reaction to the plan, so the viewer is ready for it; the second joke is who reads the news.

## Scene 3 · debug-37-trillion-cells

- id: debug-37-trillion-cells
- act: The real crazy goal
- transition_in: slide left
- key: on "once.": inside the body, every chest light red at once, the tiny Scientist spinning round with her wrench, her to-do list unrolled off the frame, the laptop still burning by the liver
- cue: "Here's what's funny about"
- time: 06:49.9 to 07:20.0 (30.1 s)
- voiceover: "Here's what's funny about this: these same humans think curing disease is the less crazy goal. That's thirty-seven trillion cells per human, breaking in seven thousand different ways, involving chemistry you don't fully understand, inside organs you can't fully simulate, fighting pathogens that evolve faster than your treatments. You're trying to debug all of it. At once. While your meat is walking around using itself."
- layer: B
- scene: A human strolls across the paper eating Wishonia's sandwich. The camera dives through his chest light into his cells, pulls back to his organs, and finally pulls all the way out. Inside, every cell has its own little check-engine light, germs outgrow the pills, a laptop fails to simulate the liver, and the Scientist, tiny, climbs in with a wrench to fix all of it.
- wishonia: PiP, thinking-small + body-idle, then smirk-smile + body-hands-hips on "walking"
- props: human, sandwich, price-tag, germ, disease-blob, pill-bottle, laptop, scientist, clipboard, wrench
- status: outline

Moves: "Here's" → the walking human strolls in, chewing the sandwich; the ground scrolls under him. "less" → a tag on a string (`KIT.props.priceTag`) drops onto his shoulder: "LESS CRAZY GOAL: cure disease". He does not notice. "thirty-seven" → the camera dives through his chest light: cells fill the frame, each with its own little check-engine light, and a label runs "37,000,000,000,000 cells" with zeros that keep coming. "thousand" → the cells' lights blink red one after another, faster and faster, each with a tiny red tag. "chemistry" → inside the cells, molecule chains tie themselves in knots, then in a bow. "organs" → the camera pulls back to the organs, flat printed outlines (heart, lungs, liver, stomach); a sandwich bite drops into the stomach. "simulate," → a tiny laptop by the liver shows "LIVER SIMULATION 3%"; it shakes and smokes, and after "simulate," it bursts into flames and keeps burning. "pathogens" → germs (`KIT.props.germ`) race through the bloodstream between the organs. "evolve" → a pill bottle fires a pill at the lead germ; the germ grows a new spike and the pill bounces off. "treatments." → the second pill: the germ eats it, swells into a big grinning disease blob, and after "treatments." burps out the bottle cap. "debug" → the Scientist, tiny, rappels in on a rope with a wrench and her clipboard. "all" → her clipboard to-do list unrolls, and unrolls, out of the bottom of the frame. "once." → every chest light in the body goes red at the same moment; she spins round, wrench up. "While" → THUMP: the whole inside lurches with a footstep; organs, blob and Scientist all bounce, and she falls on her back. "walking" → the camera pulls all the way out: the human is still strolling, still chewing, the tag still on his shoulder. "using" → he takes another big bite. after "itself." → a tiny yelp comes out of his chest; he pats his chest, shrugs, and keeps eating.

Sound: a boing as the tag drops; a whoosh on the dive; pops as the lights go red, speeding up; a squeak as the molecules knot; a whoosh on the pull-back; a straining whirr from the laptop, then fire; a pop and a boing as the pill bounces off; a splat as the germ eats the pill and a huff for the burp; a clank for the wrench; a slide whistle down as the list unrolls; an alarm bell on "once."; a slam for the footstep; a whoosh on the pull-out; a tiny yelp.

On screen: "LESS CRAZY GOAL: cure disease" (the tag) / "37,000,000,000,000 cells" / "LIVER SIMULATION 3%". No: no counter for the 7,000 (the lights are the count). Why: the goal humans call sane is the hard one; it makes the next scene's verdict absurd.

## Scene 4 · sane-insane-buzzer

- id: sane-insane-buzzer
- act: The real crazy goal
- transition_in: slide left
- key: after "insane.": INSANE flashing red, the host's hand on the buzzer, the trapdoor hanging open under the empty contestant podium
- cue: "That: sane."
- time: 07:20.0 to 07:27.8 (7.7 s)
- voiceover: "That: sane. "Give one percent fewer papers to people who build murder machines": insane."
- layer: B
- scene: A 1950s game show, "SANE OR INSANE?". The Politician hosts at a board with two face-down cards and a big red buzzer. The patient, in a straitjacket, stands at the contestant podium. The Weapons Maker sits in the front row of the studio audience with his missile.
- wishonia: PiP, eyeroll-closed + body-hands-hips
- props: game-show-board, buzzer, trapdoor, politician, human, weapons-maker, missile, money (war)
- status: outline

Moves: "That:" → the host flips card 1: "DEBUG ALL OF HUMAN BIOLOGY AT ONCE". "sane." → a teal SANE light flashes, confetti falls, and the audience claps. "Give" → the host flips card 2: "GIVE 1% FEWER PAPERS TO MURDER-MACHINE BUILDERS", with a picture of a pile of war-seal bills and one bill leaving it. "murder" → in the front row, the Weapons Maker clutches his missile tighter. "insane." → the host slaps the red buzzer: INSANE flashes red, the trapdoor under the contestant podium drops open, and the patient falls through, straitjacket and all. The host keeps grinning; the audience cheers.

Sound: a whoosh for each card flip; a ding and a sparkle for SANE; the buzzer (zap) for INSANE; a clank as the trapdoor drops and a slide whistle down as he falls.

On screen: "SANE OR INSANE?" / the two cards / "SANE" / "INSANE". Why: the planet's verdict, side by side, delivered by its own politician.

## Scene 5 · diagnostic-criteria

- id: diagnostic-criteria
- act: The diagnostic criteria
- transition_in: zoom out of the wall screen
- key: on "light-years": the mug set down, Wishonia pointing at the gauge, its needle on SEVERAL LIGHT-YEARS; the wall screen still flashing INSANE
- cue: "This is your planet's diagnostic"
- time: 07:27.8 to 07:43.5 (15.8 s)
- voiceover: "This is your planet's diagnostic criteria. I looked up the last person on your planet who went around suggesting universal love and peace. You nailed him to a piece of wood. So I consider it quite fortunate that I'm making this suggestion from several light-years away."
- layer: A
- scene: The office. The wall screen shows the end of the game show. Wishonia reads a page in the Earth case file, closes it slowly, sips from the mug, and points at a gauge on the wall that reads several light-years; then the office moves further away.
- wishonia: big, neutral-closed + body-idle, then sad-closed + body-hand-chest on "nailed", then smirk-closed + body-point-right on "light-years"
- props: office, wall-screen, desk, mug, case-file, stamp-mark, gauge
- status: outline

Moves: "This" → the camera pulls out of the wall screen, which still shows the game show: INSANE flashing, the trapdoor open. "diagnostic" → the case file on the desk ("~~EARTH~~ DIRT: CASE #847", the MAY BE ELIGIBLE stamp on its cover) flips open to a page headed "EARTH: DIAGNOSTIC CRITERIA". "last" → the page turns: "LAST HUMAN TO SUGGEST UNIVERSAL LOVE AND PEACE:", with a typed line under it. "nailed" → the file closes slowly. HOLD: nothing else moves, no sound, until "So". "So" → the mug rises to Wishonia's mouth: a long sip. "light-years" → the mug comes down slowly, and she points at a gauge on the wall to her right: "DISTANCE FROM EARTH", its needle on "SEVERAL LIGHT-YEARS". after "away." → the office lurches: the needle swings on to "MORE LIGHT-YEARS", the mug skids across the desk, the half-sun on the horizon sinks lower as the office pulls away from Earth, and the wall screen flicks to static.

Sound: a soft whoosh as the file opens and as the page turns; silence for the HOLD; a thunk as the mug comes down and a tick from the needle; a whoosh as the office lurches, a squeak as the mug skids, a crackle of static.

On screen: "EARTH: DIAGNOSTIC CRITERIA" / "LAST HUMAN TO SUGGEST UNIVERSAL LOVE AND PEACE: nailed to a piece of wood" / "DISTANCE FROM EARTH: SEVERAL LIGHT-YEARS" then "MORE LIGHT-YEARS". No: no drawing of that human, no cross, no wood. Why: what happens to people who suggest peace, and why Wishonia is glad to be far away (and then further).

## Scene 6 · orderly-door-slot

- id: orderly-door-slot
- act: What you tell the orderly
- transition_in: zoom into the wall screen
- key: after "bomb.": the BUILT BY ACCIDENT birdhouse on the padded wall, the aircraft carrier and the bomb crossed out, the patient with one arm free and the pencil, the Orderly's eyes in the door window
- cue: "Anyway, here's what you tell"
- time: 07:43.5 to 07:55.2 (11.7 s)
- voiceover: "Anyway, here's what you tell the orderly when he slides your medication through the door slot: Nobody accidentally builds an aircraft carrier or a nuclear bomb."
- layer: B
- scene: A padded cell: cream quilted walls with halftone tufts, a steel door with a small window and a slot. The patient drops in from the game show's trapdoor; the Orderly slides his medication in on an impossibly long arm; the patient works an arm free of the straitjacket and starts drawing on the padded wall.
- wishonia: PiP, neutral-smile + body-idle, then smirk-smile + body-point-right on "Nobody"
- props: padded-room, door, orderly, human, straitjacket, cup, pencil, bomb
- status: outline

Moves: "Anyway," → zoom into the wall screen out of the static: the padded cell. A hatch in the ceiling opens and the patient drops in, straitjacket and all, bounces twice on the padded floor and sits up, stars circling his head. "orderly" → the Orderly's eyes appear in the door window; then his head rises higher on his long neck. "slides" → the slot flap opens and a paper cup slides through on the Orderly's arm, which keeps coming, snaking across the whole floor to the patient. "medication" → the cup stops at the patient's feet, a red pill and a teal pill rattling in it; after "medication" the arm zips back out through the slot. "Nobody" → the patient wriggles one arm out of the straitjacket (the empty sleeve flaps), pushes the cup aside, picks up a fat pencil and turns to the wall. "accidentally" → he draws a little human tripping over a toolbox; the drawing comes alive: the tools fly up and clatter down, by pure accident, as a lopsided birdhouse. "builds" → he writes "BUILT BY ACCIDENT" over it. "carrier" → next to it he draws an aircraft carrier; "bomb." → and a nuclear bomb. after "bomb." → he crosses both out with one big X; the little drawn human looks at the birdhouse and shrugs.

Sound: two padded boings as he lands; a squeak as the Orderly's head rises; a click for the slot flap; ticks as the pills rattle; a quick whistle as the arm zips back; a boing as the arm pops free; a marker scratch for the drawing, a clank as the tools fly, a little hammering as the birdhouse builds itself; a marker for the bomb; a scratch for the big X.

On screen: "BUILT BY ACCIDENT" over the birdhouse. Why: the setup for the chain; big weapons are never an accident. The cold open of the tell-the-orderly short.

## Scene 7 · war-supply-chain

- id: war-supply-chain
- act: What you tell the orderly
- transition_in: same form (no seam)
- key: after "largest": the war wheel turning, all eight boxes lit, war-seal bills running the rim, the calendar shedding years, the first-place rosette on the hub, the Orderly's head through the door window, jaw dropped
- cue: "War requires you to get"
- time: 07:55.2 to 08:30.1 (34.9 s)
- voiceover: "War requires you to get millions of humans to work together to mine metal from the ground, refine it into alloys, build factories to shape the alloys into weapons, train millions of humans to operate the weapons, feed and clothe those humans, build ships and planes and trucks to move the weapons to where the other humans are, convince your population the other humans deserve it, and then vote to pay for all of this, annually, forever. It is the single largest coordinated effort your species undertakes."
- layer: B
- scene: On the padded wall, the patient draws a Ferris wheel whose rim is a paper-doll chain of humans holding hands; eight boxes hang from it like gondolas, from a mine to a ballot box. Each box lights up (fills with color, a red glow behind it) and comes alive as it is read. The patient bounces off the padded floor to reach the high boxes. The Orderly's eyes in the door window follow him box to box.
- wishonia: PiP, thinking-closed + body-counting, then sideeye-closed + body-arms-crossed on "largest"
- props: padded-room, door, orderly, human, pencil, factory, missile, conveyor, weapons-maker, house, loud-human, sign, ballot-box, politician, money (war), calendar, ribbon
- status: outline

Moves: "War" → the first frame is orderly-door-slot's last; the patient steps right to the big blank stretch of wall. "millions" → he draws a paper-doll chain of tiny humans holding hands, bent round into a big circle: the wheel's rim. "together" → they all lift their joined hands. "mine" → box 1 hangs from the rim and lights: a miner in overalls swings a pickaxe; ore pops out. "refine" → box 2: a furnace pours glowing alloy into ingots. "factories" → box 3: a factory (`KIT.props.factory`) whose chimneys are missiles; on "weapons," missiles roll out on a conveyor into the arms of the Weapons Maker, who cradles each one. "train" → box 4: rows of humans salute in unison; one salutes with the wrong hand. "feed" → box 5: a soup pot ladles soup; "clothe" → uniforms drop onto the humans. "ships" → box 6: a ship, then on "planes" a plane, then on "trucks" a truck, each loaded with missiles, head for a little village of other humans (`KIT.props.house`), who wave hello. after "are," → the missiles land: a white flash, a little mushroom cloud, and the other humans stand charred black and smoking, still waving. "convince" → box 7: the Loud Human shouts through his megaphone head at a crowd, in front of a poster (`KIT.props.sign`) of the charred other humans drawn with horns and fangs: "THEY DESERVE IT". "deserve" → the crowd nods and cheers. "vote" → box 8: the crowd drops ballots into a ballot box beside the grinning Politician; "pay" → war-seal bills pour out of the box's bottom and run along the rim back to box 1, where the miner swings faster. "annually," → a wall calendar (`KIT.props.calendar`) tears off a year; the bills run another lap. "forever." → the last arrow closes the loop and the whole wheel starts turning, gondolas swinging, the calendar shedding years in a blizzard. "largest" → the Orderly's head pushes in through the door window on his long neck, jaw dropping; a big first-place rosette pins itself to the hub: "LARGEST COORDINATED EFFORT".

Sound: a marker scratch as each piece is drawn; a pop as the paper dolls raise their hands; a clank on the pickaxe; a sizzle as the alloy pours; a toaster pop as the missiles come out; an airplane on "planes"; a boom as the missiles land; a cash register as the bills pour out; a tear as the calendar sheds a year; a whirr as the wheel starts turning; a squeak as the Orderly's neck stretches and a pop as the rosette pins on.

On screen: the eight boxes' pictures, with one short label each only where the picture needs it ("THEY DESERVE IT" on the poster) / "LARGEST COORDINATED EFFORT" (the rosette). No: no list of box titles, no "ANNUALLY, FOREVER" stamp, no banner (the captions say them). Why: war is work; every box is a thing humans choose to do, every year.

## Scene 8 · chain-goes-dark

- id: chain-goes-dark
- act: What you tell the orderly
- transition_in: same form (no seam)
- key: after "NOT": every box dark and still, the wheel stopped, the bills frozen mid-stride, the switch on OFF, the Orderly frozen half through the doorway with a fresh cup
- cue: "Ending war simply requires"
- time: 08:30.1 to 08:34.6 (4.5 s)
- voiceover: "Ending war simply requires NOT doing any of that stuff."
- layer: B
- scene: The patient draws a light switch next to the turning wheel and flicks it off; every box goes dark at once, and the Orderly, who has just opened the door, stops.
- wishonia: PiP, smirk-closed + body-palms-down
- props: padded-room, door, orderly, human, pencil, light-switch
- status: outline

Moves: "Ending" → the first frame is war-supply-chain's last; the door swings open and the Orderly ducks in under the frame, long neck bent, a fresh cup in hand; the patient sketches a light switch on the wall beside the wheel, set to ON. "NOT" → he flicks it to OFF with one finger: every box goes dark at once (back to flat pencil, no glow), every actor stops mid-motion, the wheel stops, the bills freeze mid-stride, the calendar stops shedding, and the Orderly freezes mid-step. Then HOLD: nothing moves for about 2.8 s, to the end of the scene.

Sound: a door creak (squeak) as the Orderly comes in; a marker scratch for the switch; the light-switch click on "NOT"; then silence.

No: no new text; the dark wall is the line. Why: the punchline; ending war is a list of things to stop doing.

## Scene 9 · centrifuge-vs-rocks

- id: centrifuge-vs-rocks
- act: Rocks do it every day
- transition_in: slide left
- key: on "thousands": the two rocks side by side, mossy, a bird nesting on the gray one, the sun streaking over again and again, the DAYS OF PEACE counter spinning; the Weapons Maker's hard hat still lying where the cascade stood
- cue: "Building a nuclear bomb requires"
- time: 08:34.6 to 08:54.7 (20.1 s)
- voiceover: "Building a nuclear bomb requires mass spectrometers, centrifuge cascades, and some of the most precise engineering your species has ever attempted. Not building a nuclear bomb requires nothing. Rocks do it every day. In fact, rocks have managed to live peacefully alongside different colored rocks for thousands of years."
- layer: B
- scene: A huge printed centrifuge cascade with branching pipes, run by an engineer and supervised by the Weapons Maker, vanishes in one pop. A gray rock rolls into the empty space next to a 1950s factory-floor counter, "DAYS OF PEACE", and a rust rock joins it for thousands of years, until a human picks one up and throws it.
- wishonia: PiP, thinking-closed + body-thinking, then happy-smile + body-hand-chest on "peacefully", then annoyed-closed + body-arms-crossed on "years."
- props: blueprint, spectrometer, centrifuge, pipes, weapons-maker, missile, human, rocks, sign (DAYS OF PEACE counter), sun
- status: outline

Moves: "Building" → slide left: a blueprint unrolls across the paper, "NUCLEAR BOMB (some assembly required)", and the Weapons Maker strides in, cradling his missile, grinning around his cigar. "spectrometers," → a spectrometer (a cabinet of dials) draws on and spits out a paper readout. "cascades," → rows of tall centrifuges spin up, pipes branching across the whole frame, everything humming. "precise" → an engineer (an everyday human in a lab coat) squints through a loupe at a tiny dial, tweezers trembling, sweat flying. "attempted." → the dial clicks into place, every centrifuge whines up to speed, and the Weapons Maker kisses his missile. "Not" → everything stops dead, mid-spin. "nothing." → the whole cascade vanishes in one pop, engineer and all, leaving empty paper and the Weapons Maker alone with his missile; he looks left, looks right, and vanishes too with a smaller pop; his hard hat drops and rolls to a stop. A cricket chirps. "Rocks" → a gray rock rolls in and stops where the cascade stood, beside a factory-floor counter on a post: "DAYS OF PEACE: 0". "day." → the sun arcs over once and the counter ticks to 1. "colored" → a second, rust-colored rock rolls up beside the first; a tiny heart floats up between them. "thousands" → the sun arcs over again and again, faster and faster; the counter spins up into the hundreds of thousands; moss and little flowers grow on both rocks and a bird nests on the gray one. "years." → an everyday human strolls in, picks up the rust rock, and hurls it off the right edge; the heart pops; after "years." the counter flips back to 0. The gray rock sits alone.

Sound: a whoosh as the blueprint unrolls; a typewriter chatter from the spectrometer; a hum as the cascade spins up; a click and a rising whirr as the dial sets; a pop for the cascade and a smaller pop for the Weapons Maker; crickets; a thunk as each rock stops; a tick per day, speeding up; a whoosh as the rock is thrown; a click as the counter resets.

On screen: "NUCLEAR BOMB (some assembly required)" (the blueprint) / "DAYS OF PEACE" (the counter). No: no BUILDING / NOT BUILDING text card. Why: stopping costs nothing, and rocks prove it daily, until a human picks one up.

## Scene 10 · billionaire-pdf

- id: billionaire-pdf
- act: The real obstacle
- transition_in: slide left
- key: after "is.": the Rich Human puffing the burning PDF like a second cigar, the UNREALISTIC sticker on his forehead, the dented STOP sign behind
- cue: "But somehow stop is"
- time: 08:54.7 to 09:07.0 (12.3 s)
- voiceover: "But somehow "stop" is the unrealistic part. Improvement is physically possible. "Stop" isn't the unrealistic part. Getting one billionaire to read a P.D.F. is."
- layer: B
- scene: A STOP sign on a post wears an "UNREALISTIC" sticker. The sticker peels off and flutters right, to the Rich Human (the fat cat) at a huge desk, scrolling a phone, while a one-page PDF slides up to him.
- wishonia: PiP, skeptical-closed + body-hands-hips, then eyeroll-closed + body-hands-hips on "billionaire", then sideeye-closed + body-arms-crossed on "is."
- props: sign (STOP), rocks, stamp, stamp-mark, rich-human, desk, phone, pdf, flames
- status: outline

Moves: "But" → slide left: a STOP sign on a post; the rust rock from centrifuge-vs-rocks flies in from the left and clangs off it, leaving a dent; the sign wobbles. "stop" (first) → an "UNREALISTIC" sticker slaps onto the sign. "physically" → a rubber stamp (`KIT.props.stamp`) slams onto the post: "PHYSICALLY POSSIBLE" with a teal tick (`KIT.props.stampMark`). "isn't" → the sticker peels off the sign and flutters right; the camera follows it. "billionaire" → the camera lands on the Rich Human in a huge leather chair at a huge desk, scrolling a phone (`KIT.props.phone`); a one-page PDF slides across the desk to him. "read" → he picks it up between two fingers; his monocle pops out. "P.D.F." → he rolls it into a tube and lights it off his cigar. "is." (last) → the sticker flutters down and lands on his forehead: UNREALISTIC. after "is." → he puffs the burning PDF like a second cigar and blows a smoke ring. The part ends on that frame.

Sound: a clank as the rock hits the sign and a boing as it wobbles; a splat as the sticker slaps on; a rubber-stamp thunk; a whoosh as the sticker flutters off; a whoosh as the PDF slides up; a pop as the monocle pops out; a flare as the PDF lights; a splat as the sticker lands; a huff for the smoke ring.

On screen: "STOP" / "UNREALISTIC" (the sticker) / "PHYSICALLY POSSIBLE" (the stamp) / "PDF". Why: the real obstacle is one reader, not physics; Part 5 pays that reader.
