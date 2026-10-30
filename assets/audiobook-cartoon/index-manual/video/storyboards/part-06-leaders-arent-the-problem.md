---
format: 1920x1080
duration: 2:45.9
message: "Your leaders are not monsters: a loop that pays politicians to buy weapons is the psychopath, it hurts even the people running it, and the plan keeps the loop but pays it to cure diseases."
arc: Title card (PROBLEM lands on a Politician) → Wishonia and one guest with every ailment at once → the monster at the desk is a Politician in a costume, sipping tea, beside the 604 bar → the loop road, stop by stop, and the Democracy Dog → the loop grows a face and runs with its plug pulled, and only Wishonia looks round at the bomb → the Weapons Maker's family gets sick, the Reaper steps out of their portrait, and his house shrinks → the snip, and what he loses and gains → Wishonia's verdict, the Weapons Maker's arithmetic → red tie, blue tie, same strings → wallpaper in a burning room → the halo, the rebuilt loop → the same dog with a tail of pills, reelected
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 6, "Why Your Leaders Aren't the Problem"
audio: index-manual.cbaf659d.mp3, 11:22.6 to 14:08.5
version: v3
---

# Part 6 storyboard: "Why Your Leaders Aren't the Problem"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The episode is a 1950s atomic-age instructional film. Layer A is the host set (`KIT.studio`): Wishonia at her lectern talking to the viewer, sometimes with a guest standing on the free wall at her right. Layer B is an illustrated plate the camera travels over (`KIT.camera`), one framing per phrase; Wishonia is not in the plates, she is the voice. Money is money green; its seal says what it buys: war papers carry the missile seal (`KIT.money("war")`), medicine papers the cross (`KIT.money("med")`). Part 2 (`compositions/scenes/part-02/`) is the reference for every kind of shot.

**Cast.** The Politician (`KIT.cast("politician")`: lantern jaw, a grin full of teeth, slick hair, flag pin, very wide tie), his replacement and the blue-tie Politician (the same options, only `tieColor` changed), the Weapons Maker (`KIT.cast("weaponsMaker")`: barrel chest, tiny head under a hard hat, cigar, cradling his grinning baby missile), the Scientist (`KIT.cast("scientist")`), the Grim Reaper (`KIT.reaper`), the Democracy Dog (`KIT.props.democracyDog`), and everyday humans whose bodies come from their outfits: the sick guest, the three voters (one of them dives into the ballot box and papers the burning room), and the Weapons Maker's wife and two children (in tiny hard hats). The same human looks the same in every scene: the first scene that draws an everyday human records its options in a comment, and the others copy them.

**Spine.** The loop plate, `the-loop`. A ring road on a plain field (Part 2's money-loop field and road), with four stops round it: the Weapons Maker's factory at the top (12 o'clock, its chimneys grinning missiles), the Politician's desk on the left (9 o'clock, the 604 bar beside it), the ballot box and the voters at the bottom (6 o'clock) and the capitol on the right (3 o'clock, `KIT.props.capitol`). The papers and the dog go round it counterclockwise, the way the Democracy Dog faces. A lane leaves the ring at 2 o'clock, between the capitol and the factory (the color-flip funnel stands at that corner), and runs up the plate past the factory to the Weapons Maker's street: his house, and across the lane the lab. Seven scenes travel over this one drawing: the desk opens on it (politician-drinks-tea), the stops start up and the dog runs round it (democracy-dog-loop) and it grows a face (loop-is-evil); after the side-eye cut (loop-side-eye) the camera follows the Weapons Maker home up the lane (weapons-maker-gets-sick) and the scissors snip it (redirect-math); the film cuts back to it for the ballot box (red-blue-ties) and the rebuild (better-loop).

**Running gags inside the part.**
- The horns. They pop off the Politician's monster costume in politician-drinks-tea, stick in the field either side of the factory in democracy-dog-loop, so the ring reads as a horned head, frame the ring's angry face in loop-is-evil, and pop off in better-loop.
- The tail bite. The dog catches its tail of war papers and corpses and yelps (democracy-dog-loop); at the end it catches its tail of pills, swallows one and runs faster (better-loop-teal-tail).
- The Grim Reaper climbs out of the family portrait and waits by the Weapons Maker's door (weapons-maker-gets-sick); on "not being dead" he crosses him off his clipboard and slouches off (redirect-math).
- The house squeezes the family (weapons-maker-gets-sick) and grows back 1.43 times bigger (redirect-math).
- The same voter: he squeezes through the ballot slot in red-blue-ties and papers the burning room in wallpaper-burning-building.

**Callbacks.** From Part 1 (604-papers): the 604 bar rises beside the desk on "six hundred and four", and at its foot the one medicine paper is still flattened under the war paper that landed on it. From Part 1 (pentagon): the Democracy Dog is the dog from the doghouse. From Part 1 (loved-ones): the flash bulb's print, the family as grinning skeletons on their sofa with the Reaper grinning between the heads, in its white deckled border, hangs framed on the Weapons Maker's wall, and the Reaper climbs out of it. From Part 2 (money-loop): the road on its plain field, the factory with missile chimneys and the Weapons Maker's baby missile. From Part 5 (step-5-treaty-split): the same $27.2 billion medicine stream, with its tag, marches into the lab in redirect-math.

**Set up here.** The dog with its tail of war papers and tiny skeletons sits on the auction block in Part 20 (democracy-auction); the dog with its tail of teal pills and knocked-out diseases runs inside the compounding loop in Part 25 (future-b-2040). Draw both tails the same way there (`KIT.props.democracyDog({ tail: "papers", seal: "war" })` and `{ tail: "pills" }`, with the skeletons or the diseases knotted in). The tie flip (red, blue) comes back in Part 21 with a third color, teal. Part 11 (defund-the-loop) leans on redirect-math's snip and does not repeat it.

**Held frame.** None: the part says no death toll. The skeletons here are gags, and they keep moving.

**Transitions.** The title card comes up from black and goes down to black; two-billion-sick irises in on Wishonia's face. Host shot to plate and plate to host shot are cuts. Scenes on one plate run on with no seam: each starts on the last one's final frame and the camera keeps traveling. A return to the loop plate after another shot (weapons-maker-gets-sick after the reaction cut loop-side-eye, red-blue-ties, better-loop) is a cut. The part ends with the iris closing on her face after "it." in better-loop-teal-tail.

**Bans for this part.**
- Red team and blue team are tie colors only (the Politician's `tieColor`: `KIT.C.war` and `KIT.C.peri`); the factory's sign is a plain WEAPONS; the capitol has no label.
- The words on screen: the heading, the factory's WEAPONS sign, the dog's DEMOCRACY tag, ×1.43, the $27.2 billion tag and the REELECTED rosette. The papers walking the road carry the story.
- The loop has four stops, but the camera frames one at a time and pulls back to the whole ring only on "system", "circular", "individual", "machine" and "builds".

## Changes from v2

- Wishonia is on screen only at her lectern. Three host shots replace her corner: two-billion-sick opens the part, no-rational-beneficiary is her verdict, and better-loop-teal-tail ends it, with the dog as her guest; the plates are her voice. A reaction cut, loop-side-eye, breaks the run of plates after loop-is-evil's bomb.
- The paper diagrams are one plate, the-loop: a ring road with four stops (the factory, the Politician's desk, the ballot box, and the capitol in place of the POWER tap) and the Weapons Maker's street up the lane. Seven scenes travel over it, one stop per phrase.
- Labels are gone: no station names, no two-box card (the trapdoor and the replacement are the choice), no pie (he loses one paper from a stack of a hundred), no ECONOMY sign, no RED TEAM / BLUE TEAM badges, no case-file page.
- Jokes restaged as one held image each: the sick crowd is one guest at Wishonia's side with every ailment at once (Part 8 owns the take-a-ticket queue); the wall-screen magnifier and stamp become the Weapons Maker doing the arithmetic as her guest; the ring's leash becomes marionette strings held by one giant war paper; the halo chars the Politician at his desk on the loop; the teal tail and the REELECTED rosette happen on the host set.
- The portrait on the Weapons Maker's wall is already Part 1's skeleton print; the new beat is the Reaper climbing out of it to wait by the door.
- politician-drinks-tea loses its gear machine and conveyor: the "system" is the loop road behind his desk, and the reward is a paper in his pocket and a gold star on his forehead.

## Scene 1 · leaders-title

- id: leaders-title
- act: Title
- transition_in: cut (up from black, the head of the reel)
- key: after "Problem.": PROBLEM sitting where the Politician stood, his hand poking out from under it, still waving his bill
- cue: "Why Your Leaders Aren't the"
- time: 11:22.6 to 11:25.6 (3.0 s)
- voiceover: "Why Your Leaders Aren't the Problem."
- layer: A, title card
- scene: The period title card (`KIT.titleScene`): the heading on plain navy under the film's atom, whose electrons are three running war papers. 16:9 lines: WHY YOUR LEADERS AREN'T THE (style small) / PROBLEM. 9:16 lines: WHY YOUR LEADERS (small) / AREN'T THE (small) / PROBLEM. The words come in on the narration (`spoken`), PROBLEM with the "drop" entrance. The gag: a small Politician on the card, standing on the spot where PROBLEM lands.
- props: title-card, politician
- status: planned

Moves: "Why" → the card comes up from black, and WHY YOUR LEADERS AREN'T THE come in word by word on the narration. "Leaders" → a small Politician pops up on the empty spot under the first line, where PROBLEM will land, grinning at the camera and waving a bill; a shadow grows round his feet. "Problem." → PROBLEM drops out of the top of the card and lands on him with a splat; the word bounces once and settles. after "Problem." → his hand pokes out from under the P, still holding the bill, and waves weakly. Then the card goes down to black.

Sound: a projector whirr on "Why"; a splat as PROBLEM lands; a tiny squeak from under it.

On screen: "WHY YOUR LEADERS AREN'T THE PROBLEM". Why: the narrator reads the heading, and the card argues with it before the part does.

## Scene 2 · two-billion-sick

- id: two-billion-sick
- act: Not monsters
- transition_in: iris in on her face
- key: on "suffering": Wishonia at the lectern, and at her right one guest with every ailment at once: a thermometer in his mouth, an ice pack on his head, his jaw bandaged, leaning on a crutch, his chest light blinking red
- cue: "With over two billion humans"
- time: 11:25.6 to 11:29.6 (4.0 s)
- voiceover: "With over two billion humans suffering from disease, you'd have to be a complete"
- layer: A, host
- wishonia: big, sad-closed + body-hand-chest; skeptical-closed + body-palms-down on "you'd"
- scene: The host set. On the free wall at her right stands one everyday human with all four ailments at once: a thermometer in his mouth, an ice pack on his head, his jaw bandaged with a knot on top, a crutch under one arm, his chest light blinking red.
- props: studio, human (the sick guest), thermometer, ice-pack, crutch, bandage
- status: planned

Moves: "With" → the iris opens on her face; the guest is already there, waiting patiently. "two billion" → his chest light blinks faster. "suffering" → the crutch wobbles, and the thermometer climbs into the red. after "disease," → he sneezes: the thermometer shoots out like a cork, the ice pack flies off, the crutch skids away, and he topples over backwards, stiff as a plank, out of the bottom of the frame; only his shoes stay in the shot, sticking up, his chest light still blinking from the floor. "you'd" → Wishonia looks at the camera.

Sound: a huff for the sneeze after "disease,"; a thunk as he lands, half a second later.

On screen: nothing. No: no counter for the two billion. Why: the part opens on the people the money is not spent on, all of their troubles on one man.

## Scene 3 · politician-drinks-tea

- id: politician-drinks-tea
- act: Not monsters
- transition_in: cut
- key: after "monsters.": the horns, the fangs and the tail drifting up off him, and under them the Politician at his desk, pinky out, sipping tea, the 604 bar beside the desk
- cue: "psychopath to make the conscious"
- time: 11:29.6 to 11:43.3 (13.7 s)
- voiceover: "psychopath to make the conscious decision to spend six hundred and four times more on weapons than on helping them. But your leaders aren't monsters. They're just operating in a system that rewards the wrong things."
- layer: B, plate the-loop
- scene: The left stop of the loop plate: the Politician's office desk at the roadside, a big red button on it and a teacup, the 604 bar standing beside it. It opens tight on the desk and pulls back on "system" to show the road behind it.
- props: ring-road, desk, politician, red-button, money("war") (the 604 bar), money("med"), white-flag, teacup, horns, fangs, tail, gold-star
- status: planned

Moves: "psychopath" → tight on a desk in shadow: a monster sits at it, all horns, glowing red eyes, fangs and a pointed tail, one claw hovering over a big red button. "decision" → the claw comes down on the button. "six hundred and four" → beside the desk the 604 bar shoots up, a tall stack of war papers, out through the top of the frame, and the desk jumps. "helping them." → the camera dips to the foot of the stack: the one medicine paper from Part 1 still lies flattened under the bottom war paper, and its little arm pokes out and waves a tiny white flag. "monsters." → back on the desk: the horns, the fangs and the tail pop off one, two, three, like a cheap costume, and drift up out of the frame, and the light comes up: under them is the Politician, pinky out, sipping a cup of tea, looking quite normal. "operating" → he gives the camera a friendly little wave with the cup. "system" → the camera pulls back: the desk stands at the side of a looping road, and war papers march past behind it on their stick legs. "rewards" → one marching paper hops up and tucks itself into his breast pocket, and a gold star slaps onto his forehead. after "things." → he takes another sip, the star twinkles, and the papers march on.

Sound: a thunk as the button goes down; a rising slide whistle as the stack shoots up; a tiny squeak with the flag; three pops as the costume comes off; a ding as the star goes on.

On screen: nothing. No: no counter; the stack going out of the frame is the number. Why: the numbers look like a monster's work, so the part clears the man and shows the road he works on.

## Scene 4 · democracy-dog-loop

- id: democracy-dog-loop
- act: The loop
- transition_in: same plate (no seam)
- key: after "corpses.": close on the dog on the road with its own tail in its teeth, war papers and tiny grinning skeletons strung along the tail
- cue: "Your civilization's incentive structure"
- time: 11:43.3 to 12:12.0 (28.7 s)
- voiceover: "Your civilization's incentive structure is the psychopath: Weapons manufacturers give politicians papers. Politicians use the papers to get people to vote for them. Voting for them gives them the power to give more papers to weapons manufacturers. Weapons manufacturers give them more papers. It's circular, like a dog chasing its tail, except the dog is democracy and the tail is made of money and corpses."
- layer: B, plate the-loop
- scene: The whole loop plate, stop by stop. Each stop starts up as it is read, the war papers walk the road counterclockwise from stop to stop, and then the Democracy Dog runs round it chasing its tail.
- props: ring-road, factory, weapons-maker, missile (his baby), politician, desk, money("war"), human (three voters), ballot-box, capitol, democracy-dog, skeleton, horns
- status: planned

Moves: "Your" → the camera keeps pulling back from the desk to the whole loop: the ring road on its field with its four stops. "psychopath:" → the costume's horns drift back down into the picture and stick in the field at the top of the ring, either side of the factory, so the whole ring reads as a head with horns. "Weapons manufacturers" → the camera travels up to the factory; the Weapons Maker steps out of its door, baby missile in one arm, "give politicians papers." → and lobs a brick of war papers down the road; the camera travels with it round the bend to the desk, where the Politician catches it, grinning, and stuffs it in his jacket. "Politicians use the papers" → he walks on down the road to the bottom stop, fanning papers out ahead of him; "vote" → each of three voters catches one, dollar signs light up in their eyes, and they drop their ballots in the box. "Voting" → the ballots march out of the box on little legs, lift the Politician up on top of them and carry him along the road to the capitol, like a crowd; "power" → they set him down on the top step and the capitol's dome lifts like a lid, "give more papers to weapons manufacturers." → and a fountain of war papers spouts out of it and rains down along the road to the factory. "Weapons manufacturers give them more papers." → the factory belches back a brick twice the size; it sails over and lands on the Politician and buries him; after "papers." → his grinning face pops out of the pile and he hugs it. "circular," → the camera pulls back to the whole ring: the papers march round it by themselves, faster and faster. "dog" → the Democracy Dog runs onto the road and round it after its own tail. "democracy" → its collar tag swings round into view: DEMOCRACY. "money" → the camera runs with the dog and pushes in on its tail: a chain of war papers, "corpses." → knotted with tiny grinning skeletons that rattle like tin cans. after "corpses." → the dog catches its tail, chomps, yelps, and keeps running, faster.

Sound: a whoosh as the horns drift in; a cash-register ka-ching as the Politician pockets the brick; two pops as the ballots drop; a clank as the dome lifts; a whoosh as the papers fountain out; a thunk as the bigger brick buries him and a boing as his face pops out; a whirr as the ring speeds up; a woof; a ding on the collar tag; bone rattles (typewriter) on "corpses."; a yelp on the bite.

On screen: "WEAPONS" (the factory sign) / "DEMOCRACY" (the collar tag). Why: the real psychopath, drawn as a road anyone can follow.

## Scene 5 · loop-is-evil

- id: loop-is-evil
- act: The loop
- transition_in: same plate (no seam)
- key: after "automatically.": the whole ring with its horns and angry face, missiles marching off the left edge, a voter holding up the pulled plug, a mushroom cloud rising far off to the left, nobody looking round
- cue: "No individual human in"
- time: 12:12.0 to 12:31.6 (19.6 s)
- voiceover: "No individual human in this loop is evil. The loop is evil. Every politician in it is making the locally rational choice: take the papers or lose your job to someone who will. It's a machine that converts good intentions into missiles, and it runs automatically."
- layer: B, plate the-loop
- scene: The same plate. The camera pulls back from the dog to the whole ring; everyone on it shrugs; the ring grows an angry face; at the capitol the Politician picks the papers over the trapdoor; the ring turns hearts into missiles and keeps running with its plug pulled.
- props: ring-road, horns, politician (and his replacement), weapons-maker, human (voters), ballot-box, capitol, factory, democracy-dog, money("war"), trapdoor, hearts, missile, plug, mushroom-cloud
- status: planned

Moves: "No" → the first frame is democracy-dog-loop's last: the dog with its tail in its teeth. "individual" → the camera pulls back to the whole ring. "evil." (first) → every human on it shrugs at once: the Weapons Maker at the factory door, the Politician in his pile at the capitol, the voters at the ballot box; the baby missile shrugs too. "evil." (second) → the ring grows a face: two angry eyebrows and narrow eyes in the field inside it, and a fanged grin along the inside of its bottom bend, under the horns. "politician" → the camera travels to the capitol: the Politician, dug out of his pile, stands on the top step. "take" → a war paper hops up into his hand and he pockets it at once. "lose" → he takes it out again and holds it out to give it back, and a trapdoor under his feet creaks open a crack. "someone who will." → behind him, in the capitol doors, stands his replacement: another Politician with the same toothy grin, his hand already out. after "will." → he snatches the paper back, the trapdoor snaps shut, and the replacement steps back into the doorway to wait. "machine" → the camera pulls back to the whole ring again. "good intentions" → at the bottom stop the voters drop little red hearts into the ballot box; "missiles," → at the top, grinning missiles pop out of the factory chimneys like toast and roll off along the road. "runs" → a voter pulls the ring's power cord out of its socket by the road and holds up the plug; the ring keeps turning, the papers keep marching, the dog keeps running, and the missiles march off the left edge of the plate. "automatically." → far off to the left, where the missiles went, a white flash. after "automatically." → a mushroom cloud rises there. Nobody looks round; the ring keeps turning.

Sound: a boing on the shrug; a slam as the face snaps on; a squeak as the trapdoor creaks; a slam as it shuts; two soft pops as the hearts drop in; a toaster pop as the missiles come out; a click as the plug comes out; a distant boom on "automatically.".

On screen: nothing. No: no card with the two choices written on it; the trapdoor and the replacement are the choice. Why: each choice is reasonable, and the sum is a missile factory; nobody on the plate looks round at the bomb, so the next shot is the one who does.

## Scene 6 · loop-side-eye

- id: loop-side-eye
- act: The loop
- transition_in: cut
- key: on "This": Wishonia at her lectern, arms crossed, side-eyeing the camera, nobody else in the shot
- cue: "This loop does not even"
- time: 12:31.6 to 12:33.1 (1.5 s)
- voiceover: "This loop does not even"
- layer: A, host (reaction cut)
- scene: A reaction cut to the host set, about a second and a half, nobody on the free wall.
- wishonia: big, sideeye-closed + body-arms-crossed
- props: studio, lectern
- status: planned

Moves: "This" → cut to Wishonia at her lectern, arms crossed, side-eyeing the camera while it pushes in a little on her face: she is the one who looked round. The plate comes back on "benefit".

Sound: none.

On screen: nothing. Why: the reaction to the bomb nobody on the plate turned round for, and a break in the run of plates between politician-drinks-tea and no-rational-beneficiary.

## Scene 7 · weapons-maker-gets-sick

- id: weapons-maker-gets-sick
- act: Nobody wins
- transition_in: cut (back to the plate as loop-is-evil left it)
- key: after "shrinking.": the squeezed little house with the family pressed against its picture window, his hard hat down over his eyes, the skeleton portrait on the wall behind them with a Reaper-shaped blank in it, the Reaper outside tapping his watch
- cue: "benefit the humans inside"
- time: 12:33.1 to 12:46.8 (13.8 s)
- voiceover: "benefit the humans inside it. The weapons manufacturers get diseases. Their children get diseases. Everyone they love gets diseases. They live in the same economy that the loop is shrinking."
- layer: B, plate the-loop
- scene: The same plate, up the lane past the factory: the Weapons Maker's street. His ranch house (`KIT.props.house`) with a big picture window you can see the living room through (or the front wall cut away); across the lane the lab, dark and shut. Inside: his wife, two children in tiny hard hats, and on the wall Part 1's skeleton print, framed.
- props: ring-road, weapons-maker, missile (his baby), house, human (his wife and children), portrait (Part 1's skeleton print), cigar, reaper, clipboard, lab
- status: planned

Moves: "benefit" → cut back to the wide as loop-is-evil left it, the mushroom cloud still standing far off on the left; the Weapons Maker walks off the ring and up the lane past the factory, cradling his baby missile, and the camera travels with him to his street; "inside it." → he goes in his front door and it slams. The camera settles on the picture window: his wife and two children in tiny hard hats inside. "weapons manufacturers get diseases." → his chest light blinks red; he coughs so hard his cigar shoots out of his mouth and across the room. "children" → both children's chest lights blink red. "Everyone they love" → the camera pushes in on the family portrait on the living-room wall: Part 1's print (loved-ones), the family already grinning skeletons on their sofa, the Grim Reaper grinning between the heads with his arms round them, in its white deckled border. "gets" → the Reaper in the print turns his head and looks out at the room. "diseases." (third) → he climbs out of the frame, leaving a Reaper-shaped blank in the print, steps down past the family, lets himself out of the front door and leans beside it outside with his clipboard. "same economy" → the camera pulls back to the whole house. "shrinking." → the house shrinks round them: the walls squeeze in, the roof pushes his hard hat down over his eyes, and the family ends up crammed inside, faces squashed against the window glass. after "shrinking." → outside, the Reaper taps his watch.

Sound: the door slam; a click as his chest light comes on and a pop as the cigar shoots out; a click for the children's lights; a pop as the Reaper steps out of the print; a falling slide whistle as the house shrinks; a squeak as it squashes them.

On screen: nothing. No: no ECONOMY sign; the narration says it. Why: the people running the loop live inside its damage, and the Reaper has already moved in.

## Scene 8 · redirect-math

- id: redirect-math
- act: Nobody wins
- transition_in: same plate (no seam)
- key: after "dead.": the Weapons Maker in front of his house, now 1.43 times bigger with a second floor and a new wing, his chest light out, holding a share certificate up next to his baby missile; the Reaper slouching off with his clipboard
- cue: "If the loop breaks"
- time: 12:46.8 to 13:08.6 (21.8 s)
- voiceover: "If the loop breaks and the redirect happens, they lose one percent of their doomsday-device revenue and gain a one point four three times larger economy to sell into, plus the ability to invest in the biotech sector that absorbs the redirected twenty-seven point two billion dollars a year, plus not being dead."
- layer: B, plate the-loop
- scene: The same plate: the camera looks back down the lane to the ring, where the scissors snip it and the color-flip funnel stands at the roadside, then comes back up to the street, where the lab across from his house lights up.
- props: ring-road, scissors, democracy-dog, money("war"), money("med"), colorFlipFunnel, weapons-maker, missile (his baby), hanky, house, human (customers), shoppingCart, lab, bond (the share), priceTag (the stream's tag), reaper, clipboard
- status: planned

Moves: "If" → the first frame is weapons-maker-gets-sick's last. "loop" → the camera travels back down the lane to where it meets the ring. "breaks" → a giant pair of scissors snips the ring road open there with a twang; the cut ends spring apart, and the dog skids to a stop at the gap, its tail flopping. "redirect" → one war paper hops off the cut end into the color-flip funnel at the roadside, "happens," → and walks out of its spout a medicine paper, the missile on its seal flipping to a cross; it sets off up the lane. "lose" → the camera follows it up to the Weapons Maker, standing outside his squeezed house hugging a stack of a hundred war papers; "one percent" → there is one gap at the top of the stack where a paper was, and he sobs into a hanky. "one point four three" → his house pops back up and keeps growing to 1.43 times its old size, a second floor and a new wing, and the family unsquashes and stretches; ×1.43 stamps onto the new wing. "sell into," → a queue of new customers with shopping carts full of money lines up at his door, and the shop bell rings. "invest" → across the lane the lab lights up; he slides a paper through its little share window, "biotech" → and gets a share certificate back; he holds it up next to his baby missile, comparing them. "twenty-seven point two billion" → Part 5's medicine stream marches up the lane into the lab, and its tag swings into view. "not being dead." → his chest light stops blinking. after "dead." → the Reaper by the door checks his clipboard, crosses the Weapons Maker's name off, and slouches away out of the frame.

Sound: a snip as the ring opens; a sparkle as the seal flips; a falling slide whistle with the sob; a rising slide whistle as the house grows; a shop bell; a cash-register ka-ching for the share; a whoosh as the tag swings in; a marker squeak as the Reaper crosses him off.

On screen: "×1.43" (on the new wing) / "$27.2 billion / year" (the stream's tag, as in Part 5). No: no pie. Why: the deal, from the side of the man who fears it most.

## Scene 9 · no-rational-beneficiary

- id: no-rational-beneficiary
- act: Nobody wins
- transition_in: cut
- key: after "arithmetic.": Wishonia at the lectern looking at the camera; beside her the Weapons Maker counting on his fingers, steam jetting from where his hard hat was, the hard hat in the air
- cue: "This is not a case"
- time: 13:08.6 to 13:24.1 (15.5 s)
- voiceover: "This is not a case where an entrenched industry rationally profits at the public's expense. There is no rational beneficiary of the current arrangement. Everyone in the loop is worse off, including the people running it. They just haven't done the arithmetic."
- layer: A, host
- wishonia: big, skeptical-closed + body-thinking; annoyed-closed + body-palms-down on "beneficiary"; smirk-smile + body-presenting on "haven't"
- scene: The host set. The Weapons Maker is her guest on the free wall at her right, baby missile in the crook of one arm, cigar in his teeth, chest light blinking red.
- props: studio, weapons-maker, missile (his baby), steam
- status: planned

Moves: "This" → cut to the host set: the Weapons Maker stands at her right, grinning, his chest light blinking red. "entrenched" → he puffs out his chest and pats his baby missile; "profits" → his eyes ring up dollar signs. "beneficiary" → the dollar signs roll over like a slot machine and come up blank; he blinks. "worse off," → he coughs, and the ash drops off his cigar. "haven't done" → he counts on his fingers, runs out of fingers, starts on the baby missile's fins, and steam whistles out of his ears. "arithmetic." → his hard hat shoots off like a cork on a jet of steam. after "arithmetic." → Wishonia looks at the camera.

Sound: a cash-register ka-ching as his eyes ring up; a click as they come up blank; a kettle whistle from his ears; a cork pop for the hard hat and a hiss of steam.

On screen: nothing. No: no sum written out; his fingers are the arithmetic. Why: the verdict, delivered to the face of the man it is about.

## Scene 10 · red-blue-ties

- id: red-blue-ties
- act: Same loop, any party
- transition_in: cut
- key: on "ties.": the red-tie and the blue-tie Politician lifted off the road by their ties spinning like propellers, marionette strings running from their wrists up to one wooden cross held by a giant war paper
- cue: "There's literally no voting"
- time: 13:24.1 to 13:43.8 (19.7 s)
- voiceover: "There's literally no voting your way out of this. It doesn't matter which political party is in power. Your "red team" and "blue team" argue about everything except the loop, because they're both inside it. They are all slaves to the same incentive structure, wearing different colored ties."
- layer: B, plate the-loop
- scene: Back on the loop plate, at the bottom stop: a voter at the ballot box, the papers marching past behind him, the dog running round. Then two Politicians, the same man except for the tie, standing on the road by the box, and over them a war paper as tall as the capitol, working them like puppets.
- props: ring-road, human (the voter), ballot-box, money("war"), democracy-dog, politician (red tie and blue tie), speech-bubbles, marionette-strings, puppet-cross, giant war paper
- status: planned

Moves: "There's" → cut to the ballot box at the bottom of the ring: a voter in front of it, the papers marching past behind him, the dog running round. This frame opens the democracy-dog short, so it stands on its own. "voting" → he drops his ballot in the box; the papers keep marching. "way out" → he tries it literally: he squeezes head first into the ballot slot, legs kicking, and disappears; "this." → he pops out of the back of the box onto the road and is swept along with the marching papers, running to keep up, the dog behind him. "party" → the box pops out a Politician like toast. "red team" → his wide tie flashes war red. "blue team" → the box pops out a second Politician, the same in every way except a blue tie. "argue" → they shout nose to nose, scribbles filling their speech bubbles faster and faster. "except" → the camera pulls back a little: they are standing on the road; "inside it." → the dog runs round under their feet and they both hop over it without looking, still shouting. "slaves" → marionette strings snap taut from both men's wrists up out of the frame; "same incentive structure," → the camera tilts up the strings: they run to one wooden puppet cross, held in the stick hands of a giant war paper standing over the ring; it tips the cross and both men's arms jerk up together. "ties." → both ties flip red, blue, red, blue, faster and faster, until they spin like propellers and lift both men off their feet, and the paper yanks the strings and slams them back down on the road.

Sound: a thunk as the ballot drops; a squeak as he squeezes into the slot; a pop as he comes out; a toaster pop for each Politician; a marker scribble in the bubbles; a boing as they hop the dog; a clank as the strings snap tight; a propeller whirr; a slam as they land.

On screen: nothing. No: no party names, animals or badges; the tie is the only difference. Why: voting changes the tie, not the loop, and the same paper pulls both strings.

## Scene 11 · wallpaper-burning-building

- id: wallpaper-burning-building
- act: Same loop, any party
- transition_in: cut
- key: after "building.": the voter on fire all over, still smiling, pasting a red-striped strip back over the new blue stripes, the curtains in flames
- cue: "Switching parties is like"
- time: 13:43.8 to 13:48.2 (4.4 s)
- voiceover: "Switching parties is like changing the wallpaper in a burning building."
- layer: B, plate living-room
- scene: A 1950s living room, flames already licking the curtains and smoke rolling along the ceiling: the voter from red-blue-ties, with a paste brush and a roll, papering blue stripes over red-striped wallpaper, right over the fire extinguisher on the wall.
- props: human (the voter), wallpaper, paste-brush, flames, fire-extinguisher
- status: planned

Moves: "Switching" → he pastes a blue-striped strip over the red stripes and smooths it down. "wallpaper" → the last strip goes up over the fire extinguisher; he steps back, pleased, and pats it. "burning" → the flames jump from the curtains onto the new wallpaper and up his trouser leg. "building." → he is on fire all over, hair burning straight up, still smiling. after "building." → he unrolls a fresh roll of red stripes and starts pasting it over the blue.

Sound: two pats as he smooths the strips; a whoosh of fire as the flames jump; a bigger one as he goes up; a pat as he starts on the red roll.

On screen: nothing. Why: the same point as red-blue-ties in one picture, and the button is the human doing it again.

## Scene 12 · better-loop

- id: better-loop
- act: A better loop
- transition_in: cut
- key: on "thing.": the charred Politician at his desk, smoking, hair straight up, dollar signs in his eyes, hugging an armful of medicine papers, the manual open on the desk
- cue: "This manual doesn't ask politicians"
- time: 13:48.2 to 14:00.5 (12.3 s)
- voiceover: "This manual doesn't ask politicians to become better people (that's clearly out of the question). It builds a better loop. You give them MORE papers to do the OPPOSITE thing."
- layer: B, plate the-loop
- scene: Back on the loop plate at the Politician's desk, the 604 bar beside it. The halo; then the camera pulls back while the loop is rebuilt (the factory becomes a lab, the ring's face smiles, the horns come off) and pushes back in for the papers.
- props: ring-road, manual, desk, politician, halo, string, factory, lab, scientist, horns, money("war"), money("med")
- status: planned

Moves: "manual" → the manual drops onto his desk with a thunk. "better people" → a halo is lowered on a string onto his slick hair; it slides right off. "clearly" → it is lowered again and he grins his widest; the halo shorts out with a zap, and he stands there charred black and smoking, hair straight up, still grinning. "question)." → the halo drops off and rolls away down the road. "builds" → the manual flips open, and the camera pulls back to the whole ring: the factory at the top folds flat and a lab springs up in its place, the Scientist in its door holding up a bubbling flask. "better loop." → the ring's angry face flips to a smile, and its horns pop off. "MORE papers" → the camera pushes back in on the desk: a column of war papers twice as long as before marches up into the charred Politician's arms. "OPPOSITE" → every seal in his arms flips from the missile to the cross. "thing." → dollar signs light up in his charred eyes, and he hugs the medicine papers.

Sound: a thunk as the manual lands; a falling slide whistle as the halo slides off; a zap as it shorts out and a sizzle; a pop as the lab springs up; a sparkle as the seals flip; a cash-register ka-ching as his eyes light up.

On screen: nothing (the WEAPONS sign goes down with the factory). No: no "better loop" sign; the smile and the lab say it. Why: the plan in one picture; it changes what the loop pays for, not the people in it.

## Scene 13 · better-loop-teal-tail

- id: better-loop-teal-tail
- act: A better loop
- transition_in: cut
- key: on "reelected": the Democracy Dog at Wishonia's right, chasing its tail of teal pills and knocked-out diseases, a REELECTED rosette landing on its collar, confetti falling, Wishonia smirking
- cue: "Same dog, same tail"
- time: 14:00.5 to 14:08.5 (8.0 s)
- voiceover: "Same dog, same tail, but now the tail is made of cured diseases and the dog gets reelected for chasing it."
- layer: A, host
- wishonia: big, happy-smile + body-presenting; smirk-smile + body-idle on "reelected"; sideeye-closed + body-idle on "it."
- scene: The host set. The Democracy Dog is her guest: it runs in on the free wall at her right and chases its tail round in a circle there.
- props: studio, democracy-dog, skeleton, pills, disease-blob, rosette, confetti
- status: planned

Moves: "Same dog," → the Democracy Dog runs in from the right and round in a circle at her right, chasing its tail; "same tail," → the same tail of war papers and tiny grinning skeletons. "now" → poof: a puff of smoke round the tail, "cured diseases" → and out of it comes a chain of teal pills, knotted with tiny disease blobs knocked out cold, X-eyed. "reelected" → a REELECTED rosette drops from above onto its collar, and confetti falls. "chasing" → the dog catches its tail and chomps a pill. after "it." → it swallows, sparkles, and runs faster, wagging; Wishonia side-eyes the camera, and the film irises out on her face.

Sound: a woof; a pop as the tail goes poof; a bell as the rosette lands; a pop on the chomp; a sparkle as it swallows.

On screen: "REELECTED" (the rosette). Why: the plan's payoff as one gag, and the part ends on the host who told it.
