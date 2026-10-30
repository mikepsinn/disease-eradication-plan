---
format: 1920x1080
duration: 2:45.9
message: "Your leaders are not monsters: a loop that pays politicians to buy weapons is the psychopath, it hurts even the people running it, and the plan keeps the loop but pays it to cure diseases."
arc: Title card → 2 billion sick and the 604 bar, yet the Politician is normal → the Democracy Dog loop → the loop is evil, not the people → the loop makes the Weapons Maker's family sick too → what he loses and gains if it breaks → no rational beneficiary → red team, blue team, same loop → wallpaper in a burning building → the same dog with a teal tail, reelected
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 6, "Why Your Leaders Aren't the Problem"
audio: index-manual.cbaf659d.mp3, 11:22.6 to 14:08.5
version: v2
---

# Part 6 storyboard: "Why Your Leaders Aren't the Problem"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys: "war papers" carry the red missile seal (`KIT.money("war")`), "medicine papers" the teal cross seal (`KIT.money("med")`). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Cast.** The Politician (`KIT.cast("politician")`: lantern jaw, a grin full of teeth, slick hair, flag pin, very wide tie), the Weapons Maker (`KIT.cast("weaponsMaker")`: barrel chest, tiny head under a hard hat, cigar, cradling a grinning baby missile), the Grim Reaper (`KIT.reaper`), and everyday humans (voters, the sick crowd, the Weapons Maker's wife and children), whose body types come from their outfits. The same human looks the same in every scene.

**Spine.** The loop. A ring drawn on the paper with four stations around it (WEAPONS MAKERS at the top, POLITICIANS on the left, VOTES at the bottom, POWER on the right; the papers and the dog go round counterclockwise, the way the Democracy Dog faces) and the Democracy Dog (`KIT.props.democracyDog`) running round it, chasing its tail. It is built in democracy-dog-loop, grows the monster's horns and a face in loop-is-evil, is snipped open in redirect-math, is searched on the wall screen in no-rational-beneficiary, carries both politicians in red-blue-ties, and is redrawn in better-loop-teal-tail, where the same dog chases a tail of teal pills and gets reelected.

**Running gags inside the part.**
- The horns. The psychopath's horns, fangs and tail pop off the Politician in politician-drinks-tea, settle on the empty ring in democracy-dog-loop, become the loop's angry face in loop-is-evil, and fall off when the arrows turn teal in better-loop-teal-tail.
- The tail bite. The dog catches its tail of war papers and corpses and yelps (democracy-dog-loop); at the end it catches its tail of pills, swallows one and runs faster (better-loop-teal-tail).
- The Grim Reaper. He rises behind the Weapons Maker's family portrait in weapons-maker-gets-sick and waits outside the house; in redirect-math, on "not being dead", he crosses the Weapons Maker's name off his clipboard and slouches off.
- The house is the economy. It squeezes the family in weapons-maker-gets-sick and grows back 1.43 times bigger in redirect-math.

**Callbacks.** From Part 1 (604-papers): the 604 bar rises in politician-drinks-tea on "six hundred and four", and at its foot the one medicine paper is still flattened under the war paper that landed on it. From Part 1 (pentagon): the Democracy Dog is the dog from the triangle doghouse. From Part 1 (loved-ones): a family portrait with blinking chest lights and the Reaper grinning between the heads, now on the Weapons Maker's mantel. From Part 1 (eligible): Wishonia huffs on her rubber stamp before it lands. From Part 5 (step-5-treaty-split): the same $27.2 billion medicine stream, with its tag, flows into the lab in redirect-math. Set up for later: the dog with its tail of war papers sits on the auction block in Part 20 (democracy-auction); the dog with its tail of teal pills runs inside the compounding loop in Part 25 (future-b-2040). Draw both tails the same way there.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.
- Red team and blue team are tie colors only (the Politician's `tieColor`: `KIT.C.war` and `KIT.C.peri`): no real party names, animals or logos.
- No real weapons companies; the Weapons Maker's factory has a plain sign.

## Changes from v1

- The humans are the stereotype cast (`KIT.cast`); the voters, the sick crowd and the Weapons Maker's family are everyday humans with body types from their outfits.
- Money is money green with seals: "red papers" are now war papers (green, red missile seal) and "teal papers" medicine papers.
- Every threat pays off on screen (style bible, Comedy 6): the conveyor missile chars the sick crowd, the loop's missiles go off on the horizon, the portrait x-rays into skeletons, the halo chars the Politician, the wallpaper human catches fire and keeps pasting.
- weapons-maker-gets-sick and redirect-math: the shrinking rug is now the house itself (`KIT.props.house`), squeezing the family and then growing back 1.43 times bigger; the Reaper waits outside and leaves on "not being dead".
- leaders-title cuts in (parts are rendered on their own), and politician-drinks-tea slides in from the card, as loved-ones does in Part 1.
- The counters in politician-drinks-tea and on the lab door are gone (the captions say the numbers); the $27.2 billion tag is the Part 5 stream's own tag.

## Scene 1 · leaders-title

- id: leaders-title
- act: Title
- transition_in: cut (the chapter card)
- key: after "Problem.": the heading in, PROBLEM sitting on the flattened Politician, his hand waving from under it
- cue: "Why Your Leaders Aren't the"
- time: 11:22.6 to 11:25.6 (3.0 s)
- voiceover: "Why Your Leaders Aren't the Problem."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`) with the part's heading in the cover font, and a small Politician standing where the last word will land.
- props: title-card, politician
- status: outline

Moves: "Why" → the heading slams in, one word per spoken word: WHY YOUR LEADERS / AREN'T THE PROBLEM. "Leaders" → a small Politician pops up in the empty slot at the end of the second line, grinning and waving. "Problem." → PROBLEM drops out of the sky onto him and flattens him like a pancake; only his grin shows under the word. after "Problem." → his hand pokes out from under PROBLEM and waves weakly (the 604-papers squash, now on a leader).

Sound: a thunk on WHY, LEADERS and AREN'T; a pop as the Politician pops up; a splat as PROBLEM lands; a small squeak from under it.

On screen: "WHY YOUR LEADERS AREN'T THE PROBLEM". Why: the narrator reads the heading aloud, and the card already argues with it.

## Scene 2 · politician-drinks-tea

- id: politician-drinks-tea
- act: Not monsters
- transition_in: slide left
- key: after "things.": the Politician sipping tea with a gold star on his forehead, his desk on the machine's gear, the 604 bar beside him, the front row of the sick crowd charred and blinking
- cue: "With over two billion humans"
- time: 11:25.6 to 11:43.3 (17.7 s)
- voiceover: "With over two billion humans suffering from disease, you'd have to be a complete psychopath to make the conscious decision to spend six hundred and four times more on weapons than on helping them. But your leaders aren't monsters. They're just operating in a system that rewards the wrong things."
- layer: B
- scene: A crowd of sick humans fills the back; a horned monster sketched at a desk turns out to be the Politician in a costume, drinking tea and looking quite normal, next to the 604 bar; his desk is one gear of a machine that pays him and ships missiles.
- wishonia: PiP, sad-closed, then neutral-smile + open-palms on "monsters.", then sideeye-closed + arms-crossed on "wrong"
- props: human, politician, 604-bar, papers-red, papers-teal, gears, conveyor, missile, mushroom-cloud
- status: outline

Moves: "two billion" → a crowd of everyday humans fills the back of the paper, every chest light blinking red: thermometers in mouths, ice packs on heads, one on crutches. after "disease," → the background gag starts and runs to the end of the scene: one at a time, a sick human in the back row x-rays into a grinning skeleton and stays standing in line (the sick do not wait). "psychopath" → in front, a pen sketches a monster at a desk in quick scratchy lines: horns, fangs, a pointed tail, a finger on a big red button. "six hundred and four" → beside the desk the 604 bar shoots up: a tall stack of war papers, out through the top of the frame. "helping them." → at the bar's foot, the one medicine paper is still flattened under the war paper from Part 1; its little arm pokes out and waves a tiny white flag. "monsters." → the horns, the fangs and the tail pop off him one, two, three, like a cheap costume, and drift up out of the frame: under them is the Politician, pinky out, sipping tea, looking quite normal. "operating" → he gives the camera a friendly wave with the teacup hand. "system" → the camera pulls back: his desk is bolted onto a big gear in a huge machine, with a conveyor running out of its far end toward the sick crowd. "rewards" → the gear turns one notch, and a mechanical arm sticks a gold star on his forehead and tucks a war paper into his breast pocket; he keeps sipping. "wrong" → at the far end of the machine a grinning little missile drops onto the conveyor and trundles toward the crowd. after "things." → it reaches them: a white flash, a small mushroom cloud, and the front row stands there charred black and smoking, hair straight up, only their eyes blinking. The Politician sips.

Sound: a zap on the first background x-ray; a pen scratch as the monster is sketched; a rising slide whistle as the 604 bar shoots up; a tiny squeak with the white flag; three pops as the costume comes off; a machine whirr as the camera pulls back; a ding as the gold star goes on; a thunk as the missile drops onto the conveyor; a boom.

On screen: "604 : 1" / "Weapons" / "Helping them" (the 604 bar's labels). No: no counter for the two billion; the captions say it. Why: the numbers look like a monster's work, so the part starts by clearing the person and showing the machine.

## Scene 3 · democracy-dog-loop

- id: democracy-dog-loop
- act: The loop
- transition_in: slide left
- key: after "corpses.": the close-up on the dog with its own tail in its teeth, war papers and tiny grinning skeletons strung along it
- cue: "Your civilization's incentive structure"
- time: 11:43.3 to 12:12.0 (28.7 s)
- voiceover: "Your civilization's incentive structure is the psychopath: Weapons manufacturers give politicians papers. Politicians use the papers to get people to vote for them. Voting for them gives them the power to give more papers to weapons manufacturers. Weapons manufacturers give them more papers. It's circular, like a dog chasing its tail, except the dog is democracy and the tail is made of money and corpses."
- layer: B
- scene: Four stations around a ring light up as each is read (the Weapons Maker at his factory, the Politician, the voters at the ballot box, the POWER tap), the war papers run round it, and the Democracy Dog runs round the ring chasing its tail.
- wishonia: PiP, thinking-closed + point-right, then eyeroll-closed + arms-crossed on "corpses."
- props: loop-diagram, weapons-maker, politician, human, papers-red, factory, ballot-box, democracy-dog
- status: outline

Moves: "psychopath:" → the horns from politician-drinks-tea float in from the left and settle on top of an empty ring drawn on the paper. "Weapons manufacturers give politicians papers." → station 1 lights at the top: the Weapons Maker steps out of his factory (its chimneys are missiles), baby missile in one arm, and lobs a brick of war papers round the ring to station 2, where the Politician catches it, grinning, and pockets it ("papers."). "Politicians use the papers" → the Politician fans papers down the ring to station 3; "vote" → each voter catches one, dollar signs light in their eyes, and they drop ballots in the ballot box. "power" → station 4: the ballots shoot out of the box round the ring into a big brass tap marked POWER, which spins open. "give more papers to weapons manufacturers." → the tap gushes war papers up the ring into the factory. "Weapons manufacturers give them more papers." → the factory belches back a bigger brick; it lands on the Politician and buries him; after "papers." → his grinning face pops out of the pile and he hugs it. "circular," → the four stations join into one turning ring, and the war papers march round it by themselves, faster and faster. "dog" → the Democracy Dog (the dog from Part 1's triangle doghouse) runs in and chases its tail round the ring. "democracy" → its collar tag swings into view: DEMOCRACY. "money" → the camera pushes in on the tail: a chain of war papers, "corpses." → knotted with tiny grinning skeletons that rattle like tin cans. after "corpses." → the dog catches its tail, chomps, yelps, and keeps running, faster.

Sound: a whoosh as the horns float in; a cash-register ka-ching as the Politician pockets the brick; two pops as the ballots drop; a clank as the POWER tap spins open; a whoosh as the papers gush into the factory; a thunk as the bigger brick buries him; a boing as his face pops out; a machine whirr as the ring starts turning; a woof; a jingle ding on the collar tag; bone rattles on "corpses."; a yelp on the bite.

On screen: "WEAPONS MAKERS" / "POLITICIANS" / "VOTES" / "POWER" (the stations) / "DEMOCRACY" (the collar tag). Why: the real psychopath, drawn as a machine anyone can follow.

## Scene 4 · loop-is-evil

- id: loop-is-evil
- act: The loop
- transition_in: same form (no seam)
- key: the ring with the horns and an angry face, hearts dropping into the ballot box, grinning missiles rolling out of the factory chimneys, the unplugged cord held up
- cue: "No individual human in"
- time: 12:12.0 to 12:31.6 (19.6 s)
- voiceover: "No individual human in this loop is evil. The loop is evil. Every politician in it is making the locally rational choice: take the papers or lose your job to someone who will. It's a machine that converts good intentions into missiles, and it runs automatically."
- layer: B
- scene: The camera pulls back from the dog to the whole loop; every human in it shrugs, the ring grows a face under its horns, the Politician picks the only box that keeps him off the trapdoor, and the loop turns hearts into missiles with its plug pulled.
- wishonia: PiP, thinking-small + thinking, then sideeye-closed + arms-crossed on "automatically."
- props: loop-diagram, politician, weapons-maker, human, democracy-dog, checkbox-tick, missile, ballot-box, factory, mushroom-cloud
- status: outline

Moves: "No" → the first frame is democracy-dog-loop's last: the close-up of the dog with its tail in its teeth. "individual" → the camera pulls back to the whole loop. "evil." (first) → every human in the loop shrugs at once, the Weapons Maker's baby missile too. "evil." (second) → the ring grows a face under its horns: angry eyebrows and narrow eyes in its middle, a fanged grin along its bottom arc, its arrows glowing war red. "locally rational" → a two-box card drops on a string in front of the Politician. "take" → he ticks the first box at once. "lose" → he peeks at the second box, and a trapdoor under his feet creaks open a crack. "someone who will." → behind him stands his replacement, another Politician with the same toothy grin, hand already out; after "will." → the trapdoor snaps shut and the replacement steps back to wait. "machine" → small red hearts drop into the ballot box, "missiles," → and grinning missiles pop out of the factory's missile chimneys like toast and line up on the ring. "runs" → the humans step back, hands up; a voter pulls the loop's plug and holds it up; the loop keeps turning, the dog keeps running, the missiles march off the edge of the paper. after "automatically." → far behind the loop, where the missiles went, a white flash and a mushroom cloud on the horizon. Nobody looks round.

Sound: a whoosh as the camera pulls back; a boing on the shrug; a slam as the face snaps on; a pencil scratch on the tick; a creak (squeak) as the trapdoor opens; a slam as it shuts; two soft pops as the hearts drop in; a toaster pop as the missiles come out; a click as the plug comes out; a distant boom.

On screen: "Take the papers" / "Lose your job to someone who will" (the card, with two drawn boxes). Why: each choice is reasonable, and the sum is a missile factory.

## Scene 5 · weapons-maker-gets-sick

- id: weapons-maker-gets-sick
- act: Nobody wins
- transition_in: slide left
- key: after "shrinking.": the shrunken house with the family squashed against its windows, the skeleton portrait on the mantel, the Reaper outside tapping his watch
- cue: "This loop does not even"
- time: 12:31.6 to 12:46.8 (15.2 s)
- voiceover: "This loop does not even benefit the humans inside it. The weapons manufacturers get diseases. Their children get diseases. Everyone they love gets diseases. They live in the same economy that the loop is shrinking."
- layer: B
- scene: The Weapons Maker goes home to a cutaway house; his chest light, his children's, and the ones in the family portrait blink red, the Reaper rises behind the portrait, and the house, marked ECONOMY, shrinks around the family.
- wishonia: PiP, sad-closed, then sad-frown + hand-chest on "Everyone"
- props: weapons-maker, human, house, family-portrait, reaper, sign, clipboard
- status: outline

Moves: "benefit" → the Weapons Maker walks home from the loop, cradling his baby missile, into a cutaway house where his wife and two children (in tiny hard hats) wait; "it." → the door shuts behind him. "weapons manufacturers get diseases." → his chest light blinks red; he coughs so hard his cigar shoots out of his mouth. "children" → his two children's chest lights blink red. "Everyone they love" → the framed family portrait on the mantel (grandparents, aunts, cousins, all smiling); its chest lights blink red, one by one. "gets" → the Grim Reaper rises up behind the portrait, grinning between the last two heads. "diseases." (last) → the portrait x-rays into skeletons, one by one; the skulls keep smiling. The Reaper steps out of the frame and through the wall, and leans outside the front door with a clipboard, waiting. "same economy" → a sign drops onto the roof: ECONOMY. "shrinking." → the house shrinks around them: the walls squeeze in, the ceiling pushes the hard hat down over his eyes, and the family ends up crammed inside, faces squashed against the windows. Outside, the Reaper taps his watch.

Sound: footsteps (pat); the door slam; a click as his chest light comes on; a pop as the cigar shoots out; a click for the children's lights; a whoosh as the Reaper rises; an x-ray zap on the portrait; a falling slide whistle as the house shrinks; a squeak as it squashes them.

On screen: "ECONOMY" (the sign on the roof). Why: the people running the loop are inside its damage.

## Scene 6 · redirect-math

- id: redirect-math
- act: Nobody wins
- transition_in: slide left
- key: after "dead.": the house 1.43 times bigger with a new wing, the medicine stream into the lab, the Weapons Maker holding his share and his baby missile, the Reaper slouching off with his clipboard
- cue: "If the loop breaks"
- time: 12:46.8 to 13:08.6 (21.8 s)
- voiceover: "If the loop breaks and the redirect happens, they lose one percent of their doomsday-device revenue and gain a one point four three times larger economy to sell into, plus the ability to invest in the biotech sector that absorbs the redirected twenty-seven point two billion dollars a year, plus not being dead."
- layer: B
- scene: The loop is snipped open; one war paper in a hundred goes through the color-flip funnel and comes out a medicine paper, and the Weapons Maker loses a sliver of pie, gets his house back bigger, buys a share in the lab, and is crossed off the Reaper's list.
- wishonia: PiP, thinking-closed + counting, then happy-smile + open-palms on "dead."
- props: loop-diagram, democracy-dog, weapons-maker, papers-red, papers-teal, color-flip-funnel, pie-chart, house, shopping-cart, lab, bond, price-tag, reaper, clipboard
- status: outline

Moves: "breaks" → scissors snip the ring of war papers open with a twang; the dog skids to a stop at the gap, its tail flopping. "redirect" → one war paper in a hundred hops off the cut end into the color-flip funnel; "happens," → it comes out a medicine paper, the seal flipping from the red missile to the teal cross. "lose" → the Weapons Maker holds up his revenue pie, labelled DOOMSDAY-DEVICE REVENUE; "one percent" → a thin slice drops off it onto his toe, and he hops on one foot, still holding the pie and the baby missile. "one point four three" → his squashed house from weapons-maker-gets-sick pops back up and keeps growing to 1.43 times its old size: a second floor, a new wing; the family unsquashes and stretches. The Reaper is still leaning by the door. "sell into," → a line of new customers with shopping carts queues at his door, and the shop bell rings. "invest" → he slides a paper through the share window of a lab, "biotech" → and gets a share certificate back; he holds it up next to the baby missile, comparing them. "twenty-seven point two billion" → the medicine stream from Part 5 flows into the lab, and its tag swings into view. "not being dead." → his chest light stops blinking. after "dead." → the Reaper checks his clipboard, crosses the Weapons Maker's name off, and slouches away out of the frame.

Sound: a snip as the ring opens; a boing as the paper hops in; a sparkle as its seal flips; a thunk as the slice lands on his toe; a yelp; a rising slide whistle as the house grows; a shop bell; a squeak as the share window slides; a cash-register ka-ching for the share; a whoosh as the tag swings in; a marker squeak as the Reaper crosses him off; a falling slide whistle as the Reaper slouches off.

On screen: "DOOMSDAY-DEVICE REVENUE" (the pie) / "−1%" (the slice) / "×1.43" (the house) / "$27.2 billion a year" (the stream's tag). Why: the deal, from the side of the person who fears it most.

## Scene 7 · no-rational-beneficiary

- id: no-rational-beneficiary
- act: Nobody wins
- transition_in: zoom out of the wall screen
- key: after "arithmetic.": the stamped page on the desk, Wishonia holding the sum up to the wall screen, the Weapons Maker on the screen with steam jetting where his hard hat was
- cue: "This is not a case"
- time: 13:08.6 to 13:24.1 (15.5 s)
- voiceover: "This is not a case where an entrenched industry rationally profits at the public's expense. There is no rational beneficiary of the current arrangement. Everyone in the loop is worse off, including the people running it. They just haven't done the arithmetic."
- layer: A
- scene: Wishonia switches the wall screen back to the loop as it is now, searches it with a magnifying glass, finds nobody who gains, stamps a page in the Earth case file, and holds up the arithmetic, which the Weapons Maker on the screen tries to do on his fingers.
- wishonia: big, skeptical-closed + body-thinking, then annoyed-closed + body-palms-down on "beneficiary", then smirk-smile + body-presenting on "arithmetic."
- props: office, wall-screen, loop-diagram, magnifier, case-file, stamp, desk, plain-paper, pencil
- status: outline

Moves: "This" → the zoom out starts on redirect-math's last frame on the wall screen. "not" → the screen clicks over, like a television channel, to the loop as it is now: the war loop turning, the dog chasing its tail. "entrenched" → Wishonia holds a magnifying glass up to the screen and slides it along the loop: under the glass each human is big, and each one is coughing, blinking red, or charred. before "beneficiary" → she huffs on her rubber stamp. "beneficiary" → she stamps the open case-file page BENEFICIARIES OF THE LOOP: NONE FOUND. "worse off," → on the wall screen every face in the loop frowns, the Weapons Maker's and the Politician's too; even the dog's ears droop. "including" → Wishonia writes a sum on a plain paper. "They" → she holds it up to the wall screen. "haven't done" → on the screen the Weapons Maker squints at it and counts on his fingers, runs out of fingers, and steam starts whistling out of his ears. "arithmetic." → his hard hat shoots off like a cork on a jet of steam. Wishonia looks at the camera.

Sound: a television click; a whoosh as the magnifier comes up; a huff on the stamp; a rubber-stamp thunk; a falling slide whistle as the faces droop; a marker squeak as she writes; a kettle whistle from his ears; a cork pop for the hard hat; a hiss of steam (huff).

On screen: "BENEFICIARIES OF THE LOOP" (the case-file page) / "NONE FOUND" (the stamp) / "−1% + 1.43× + not dead" (the paper). Why: the verdict; even the people running the loop lose from it.

## Scene 8 · red-blue-ties

- id: red-blue-ties
- act: Same loop, any party
- transition_in: zoom into the wall screen
- key: on "ties.": both politicians on the top of the loop, leashed to it by strings at the wrists, their ties spinning into propellers
- cue: "There's literally no voting"
- time: 13:24.1 to 13:43.8 (19.7 s)
- voiceover: "There's literally no voting your way out of this. It doesn't matter which political party is in power. Your "red team" and "blue team" argue about everything except the loop, because they're both inside it. They are all slaves to the same incentive structure, wearing different colored ties."
- layer: B
- scene: A voter tries to vote his way out, literally, and comes out on the loop; the ballot box pops out a red-tie Politician and a blue-tie Politician, who argue standing on the same loop, leashed to it by strings, while their ties flip color faster and faster.
- wishonia: PiP, eyeroll-closed + arms-crossed, then skeptical-smile + shrug on "slaves"
- props: loop-diagram, human, ballot-box, politician, democracy-dog, papers-red
- status: outline

Moves: "There's" → the first frame stands on its own (it opens the democracy-dog short): a voter at a ballot box, the war loop turning behind it, the dog chasing its tail. "voting" → he drops a ballot in the box; the loop keeps turning. "way out" → he tries it literally: he squeezes into the ballot box slot head first, legs kicking, and disappears; "this." → he pops out of the back of the box onto the loop and gets carried round with the papers, running to keep up beside the dog. "party" → the box pops out a Politician like toast. "red team" → his wide tie flashes war red. "blue team" → the box pops out a second Politician, the same in every way except a blue tie. "argue" → they shout nose to nose, scribbles in their speech bubbles; "everything" → the bubbles fill faster and faster, until a tiny anvil drops out of one. "except" → the camera pulls back: both stand on the top of the Democracy Dog's loop, and the dog runs round under their feet; "inside it." → as it passes they both hop over it without looking, still shouting. "slaves" → strings snap tight from the ring to both of their wrists, like leashes; "same incentive structure," → the ring turns a notch and both their arms jerk up together. "ties." → both ties flip red, blue, red, blue, faster and faster, until they spin like propellers and lift both politicians off their feet, until the strings snap them back down onto the loop.

Sound: a thunk as the ballot drops; a squeak as he squeezes into the slot; a pop as he comes out on the loop; a toaster pop for each Politician; a ding as the red tie flashes; marker scribbles in the bubbles; a thunk as the anvil drops; a whoosh as the camera pulls back; a boing as they hop the dog; a clank as the strings snap tight; a click (switch) as their arms jerk; a propeller whirr; a slam as they land.

On screen: "RED TEAM" / "BLUE TEAM" (badges on their lapels). Why: voting changes the tie, not the loop.

## Scene 9 · wallpaper-burning-building

- id: wallpaper-burning-building
- act: Same loop, any party
- transition_in: slide left
- key: after "building.": the human on fire all over, smiling, pasting a red-striped strip back over the new blue stripes
- cue: "Switching parties is like"
- time: 13:43.8 to 13:48.2 (4.4 s)
- voiceover: "Switching parties is like changing the wallpaper in a burning building."
- layer: B
- scene: In a living room with flames on the curtains, a voter calmly pastes blue-striped wallpaper over red-striped wallpaper, catches fire, and starts switching back.
- wishonia: PiP, sideeye-closed + hands-hips
- props: human, wallpaper, flames
- status: outline

Moves: "Switching" → in a living room with flames licking the curtains, a voter pastes a blue-striped strip over the red stripes and smooths it down. "wallpaper" → the last strip goes up; he steps back, pleased, and pats it. "burning" → the flames jump from the curtains onto the new wallpaper and up his trouser leg. "building." → he is on fire all over, hair burning straight up, still smiling. after "building." → he unrolls a fresh roll of red-striped wallpaper and starts pasting it over the blue.

Sound: two pats as he smooths the strips; a whoosh of fire as the flames jump; a bigger one as he goes up; a pat as he starts on the red roll.

Why: the same point as red-blue-ties, in one picture; the button is the human doing it again.

## Scene 10 · better-loop-teal-tail

- id: better-loop-teal-tail
- act: A better loop
- transition_in: slide left
- key: on "reelected": the redrawn loop with teal arrows and a lab station, the dog chasing its tail of teal pills and knocked-out diseases, the REELECTED ribbon landing on its collar
- cue: "This manual doesn't ask politicians"
- time: 13:48.2 to 14:08.5 (20.3 s)
- voiceover: "This manual doesn't ask politicians to become better people (that's clearly out of the question). It builds a better loop. You give them MORE papers to do the OPPOSITE thing. Same dog, same tail, but now the tail is made of cured diseases and the dog gets reelected for chasing it."
- layer: B
- scene: A halo will not stay on the Politician and finally chars him, so the manual redraws the loop: more war papers go through the color-flip funnel and come out medicine papers, the arrows turn teal, the horns fall off, and the same Democracy Dog chases a tail of teal pills and gets reelected.
- wishonia: PiP, happy-smile + presenting, then smirk-smile + point-right on "reelected"
- props: loop-diagram, manual, politician, halo, democracy-dog, papers-red, papers-teal, color-flip-funnel, lab, scientist, pills, disease-blob, ribbon, human
- status: outline

Moves: "manual" → the manual drops onto the paper beside the war loop, next to the Politician at his station. "better people" → a halo is lowered on a string onto his slick hair; it slides right off. "clearly" → it is lowered again and he grins his widest; the halo shorts out with a zap: he stands there charred black and smoking, hair straight up, still grinning. "question)." → the halo drops off and rolls away out of the frame. "builds" → the manual flips open and its pencil redraws the ring; "better loop." → the factory station pops up as a lab, the Scientist in its door with a bubbling flask. "MORE papers" → a bigger stream of war papers runs through the color-flip funnel and comes out medicine papers, the seals flipping, into the charred Politician's hands; dollar signs light in his eyes. "OPPOSITE" → the arrows round the ring flip from war red to medicine teal, the angry face on the ring flips to a smile, "thing." → and the horns fall off it. "Same dog," → the Democracy Dog runs in again, "same tail," → chasing the same tail, "cured diseases" → but now its tail is a chain of teal pills knotted with tiny knocked-out disease blobs, X-eyed (the corpses tail, the other way round). "reelected" → mid-run, a REELECTED ribbon lands on its collar, and the voters at the bottom station throw confetti. "chasing" → the dog catches its tail and chomps a pill; after "it." → it swallows, sparkles, and runs faster, wagging. The part ends on that frame.

Sound: a thunk as the manual lands; a falling slide whistle as the halo slides off; a zap as it shorts out; a sizzle; a marker squeak as the ring is redrawn; a pop as the lab comes up; a cash-register ka-ching on MORE; a sparkle as the seals flip; a click (switch) as the arrows flip; a pop as the horns fall; a woof; two pops as the pills appear; a bell as the ribbon lands; a pop on the chomp; a sparkle as the dog swallows.

On screen: "REELECTED" (the ribbon). No: no "Same dog. Same tail." card; the captions say it. Why: the plan in one picture; it changes what the loop pays for, not the people in it.
