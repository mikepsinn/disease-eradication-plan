---
format: 1920x1080
duration: 2:15.6
message: "Papers move politics in a fixed order (rich humans, loud humans, lobbyists, politicians' friends), and the treaty pays everyone back from $27.2 billion a year, 80% of it for clinical trials."
arc: Title card, papers in procession → Wishonia pulls down the five steps → Step 1, a billion papers from a fat cat who ticks the living box → 2,800 top hats, one prefers living → Step 2, loud humans blast your thing → Step 3, the long way to the Politician's pocket, stamped LEGAL → Step 4, the Super PAC swallows a river → Step 5, the treaty flips $27.2 billion teal and splits it 80/10/10, and forever survives the Grim Reaper
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 5, "The Sacred Order of Paper Distribution"
audio: index-manual.cbaf659d.mp3, 09:07.0 to 11:22.6
version: v2
---

# Part 5 storyboard: "The Sacred Order of Paper Distribution"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The scroll, the hill and one stream of papers. The five steps glow on Wishonia's pull-down scroll in sacred-scroll, and every step scene opens on its numbered card, a strip of that scroll. One stream of plain papers leaves the Rich Human's hill in Step 1 and walks in from the left edge in Steps 2, 3 and 4; in Step 5 the treaty's war money goes through the color-flip funnel and comes out medicine money, and a tenth of it climbs back up the same hill.

**Running gag (replaces the countdown board).** The Grim Reaper and his tally clipboard. He keeps count of the humans that diseases kill, adding marks as fast as he can write. In step-1-dice-in-a-suit he offers the Rich Human a pencil for box 2; in 2800-top-hats he leans on a headstone, adding a mark; in step-5-treaty-split he comes for the Rich Human, gets him for a moment, and loses him to the lab.

**Shared drawings** (several author groups draw these, so they must match):
- **The step card.** A strip of the sacred scroll (`KIT.props.scroll`): cream paper with rolled ends and a navy outline, "STEP N" in Fraunces Black and the heading in Oswald SemiBold capitals. 16:9: across the top, x 120 to 1500, y 40 to 170. 9:16: x 40 to 720, y 70 to 330, the heading in three lines (the saucer is at the top right). It unrolls on "Step" (0.5 s), stays while the heading is read, then rolls up into a small "STEP N" tab in the top-left corner (16:9 x 40 to 260, y 30 to 100) for the rest of the scene.
- **The Rich Human's hill.** A mound of plain bills (`KIT.money("plain")`) packed in rows, with Part 4's navy swivel chair at the top (the cream "UNREALISTIC" sticker still on its back) and `KIT.cast("richHuman")` sitting in it. 16:9: the right half, x 1000 to 1520, y 330 to 860, clear of Wishonia's corner.
- **The stream.** Plain bills on stick legs walking in single file, entering from the left edge.
- **The "I PREFER LIVING" button** (from 2800-top-hats on): a round cream pin with a navy rim and teal text, on the Rich Human's left lapel above his chest light.
- **The LEGAL stamp** (from step-3-lobbyist-funnels on): `KIT.props.stampMark("LEGAL")`, tilted, on the Politician's forehead in Steps 3, 4 and 5.
- **The Grim Reaper.** `KIT.reaper()` with `KIT.props.clipboard` under one arm or in hand; the clipboard is covered in navy tally marks in fives.

**Callback.** From Part 4 (billionaire-pdf): the Rich Human who turned his chair away from the PDF sits in the same chair, sticker and all, on the hill in step-1-dice-in-a-suit. From Part 1 (split-the-atom): the wall screen's calendar in sacred-scroll starts on 1945, the year Wishonia started watching. From Part 1 (loved-ones): the Grim Reaper and the mail-in form look. Set up for later parts: the "I PREFER LIVING" button stays on the Rich Human (style bible, the Rich Human); the Reaper's tally can stand in for the countdown board in the parts that used it (8, 11, 17, 26); Part 6's redirect-math reuses the $27.2 billion teal stream into the lab.

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: in 16:9 nothing important below y 900; in 9:16 nothing important from y 1450 down. Keep Wishonia's corner clear (16:9 x 1600 to 1920, y 690 down; 9:16 x 740 to 1040, y 60 to 430).
- The money is always money green. Steps 1 to 4 use plain bills (no seal); war seals and medicine seals start with the treaty in Step 5.
- No real lobbying firms, Super PACs, campaigns, platforms, treaties or banks; plain signs only.
- No labels that repeat what the narrator just said ("investment: gambling, but wearing a suit"); the dice, the pie chart and the washing machine say it.

## Changes from v1

- The humans are the stereotype cast: the Rich Human is the fat cat, the Lobbyist the masked crook, the Politician the lantern jaw with the toothy grin; the Loud Humans get everyday builds.
- The countdown board is gone from the kit. Its job in step-5-treaty-split (diseases kill people while time passes) goes to the Grim Reaper's tally clipboard, set up in Step 1 and 2800-top-hats.
- The gags go all the way: the dice roll themselves, the ILLEGAL sign flattens the paper, the route runs backwards, the plain PAC bursts, the Politician bonks the top of the frame, and the Rich Human grows a beard, turns into a skeleton and is brought back by the lab.
- sacred-order-title cuts in (a title card has no wall screen to zoom out of, as in Part 1); the scroll in sacred-scroll is a pull-down chart over the wall screen, so the steps sit above the bottom of the frame.
- Recurring props come from the shared library (`KIT.props.*`).

## Scene 1 · sacred-order-title

- id: sacred-order-title
- act: Title
- transition_in: cut
- key: the heading in, the procession of hooded papers halfway into the top hat
- cue: "The Sacred Order of Paper"
- time: 09:07.0 to 09:10.7 (3.8 s)
- voiceover: "The Sacred Order of Paper Distribution."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`) with the part's heading in the cover font; along the bottom, a solemn procession of plain papers marches into a top hat.
- props: title-card, plain-paper, top-hat
- status: outline

Moves: "Sacred" → the heading slams in, one word per spoken word, with soft mustard rays behind "SACRED". "Order" → along the bottom of the card, a single file of plain papers in tiny monk hoods walks in from the left, the leader swinging a little censer on a chain. "Distribution." → the line reaches an upturned top hat on the right and marches into it, one paper at a time. after "Distribution." → the hat burps.

Sound: a thunk on each title word; a sparkle under the rays; tiny squeaky footsteps for the procession; a pop as the hat burps.

On screen: "THE SACRED ORDER OF PAPER DISTRIBUTION". No: no Wishonia; the card is the heading. Why: the narrator reads the heading aloud, and the procession sets up where the papers end up.

## Scene 2 · sacred-scroll

- id: sacred-scroll
- act: The five steps
- transition_in: cut
- key: the scroll pulled down over the wall screen, all five steps glowing, its tail rolling away across the floor
- cue: "After eighty years of observation"
- time: 09:10.7 to 09:18.2 (7.5 s)
- voiceover: "After eighty years of observation, I've decoded the paper-giving sequence. This manual will teach you the precise order:"
- layer: A
- scene: Wishonia at her desk. The wall screen's calendar runs from 1945 to 2025; then a long scroll drops over the screen like a 1950s classroom pull-down chart, its tail unrolls across the floor and out of the office, and five steps glow on it.
- wishonia: big, happy-smile + body-presenting, then happy-smile + body-counting on "precise"
- props: office, desk, mug, wall-screen, calendar, scroll
- status: outline

Moves: "eighty years" → on the wall screen, a desk calendar starts on 1945 (the year she started watching, Part 1) and tears off its pages in a blur. "observation," → it stops on 2025. "decoded" → a long scroll drops over the wall screen like a pull-down chart, its pull ring swinging; the five steps are printed on it in faint ink. "paper-giving" → its tail keeps unrolling past the bottom of the screen, onto the floor, and rolls away out of the office on the left. "precise" → the five steps glow, one every 0.25 s; step 5, "(FOREVER)", glows last and brightest. "order:" (1.15 s in) → the scroll snaps back up into its roller, spinning, and the tail whips back in across the floor; the mug spins on the desk. The wall screen behind it now shows the Earth paper: the Rich Human's hill with the swivel chair at the top, turned away, and the step 1 card still rolled up (step-1-dice-in-a-suit's first frame).

Sound: a flutter of calendar pages; a ding at 2025; a whoosh as the scroll drops; a whirr as its tail rolls away; a ding per step, a sparkle on step 5; a rising slide whistle as it snaps back up.

On screen: "1945" to "2025" (the calendar) / "1. Rich humans" / "2. Loud humans" / "3. Lobbyists" / "4. Politicians' friends" / "5. Back to the rich humans (forever)". No: no new characters in the office. Why: the map of the part, so each step has a place to land; the calendar is the 80 years.

## Scene 3 · step-1-dice-in-a-suit

- id: step-1-dice-in-a-suit
- act: Step 1
- transition_in: zoom into the wall screen
- key: on "suit": the dice in a business suit straightening its tie in front of the hill, the Rich Human above it with dollar-sign eyes, reaching for the dotted LATER stack
- cue: "Step one: Get Many Papers"
- time: 09:18.2 to 09:40.8 (22.6 s)
- voiceover: "Step one: Get Many Papers from Rich Humans You convince rich humans to give you papers (at least one billion to be exact) by promising them even more papers later. This is called "investment," which is gambling but wearing a suit. You really only need one human with a billion papers who prefers not dying of horrible diseases to dying of horrible diseases."
- layer: B
- scene: The Rich Human (the fat cat) sits in Part 4's swivel chair on a hill of plain papers; a billion of them slide off toward the viewer, a pair of dice in a tiny business suit strolls past and rolls itself, and a two-box form asks the Rich Human a question while the Grim Reaper offers him a pencil.
- wishonia: PiP, neutral-smile, then smirk-smile on "suit", then sideeye-closed + body-arms-crossed on "to" (as the Reaper rises)
- props: step-card, scroll, rich-human, plain-paper, swivel-chair, dice-in-suit, two-box-form, checkbox-tick, pencil, reaper, clipboard
- status: outline

Moves: "Step one" → the step 1 card unrolls across the top. after "Humans" (first) → it rolls up into its tab. "convince" → the swivel chair at the top of the hill spins round: the Rich Human in top hat and monocle, cigar in his teeth, hugging his stack of cash; the UNREALISTIC sticker is still on the chair's back. "one billion" → a big stack of plain papers slides off the hill toward the viewer, labeled "1,000,000,000". "exact)" → one more paper hops on top and the label clicks to "1,000,000,001". "later." → a bigger stack, drawn in dotted lines and labeled "LATER", floats above the hill. after "later." → the Rich Human's eyes turn into dollar signs and he reaches up for it. "investment," → a pair of dice in a tiny pinstripe suit and bowler strolls in along the front, swinging a briefcase. "gambling" → it trips and rolls itself across the ground, clattering. "but" → it lands on snake eyes. "suit." → it stands up, dusts itself off, straightens its tie as if nothing happened, and strolls on. "one human" → a two-box mail-in form slides up beside the hill, in the Part 1 form look: "RICH HUMAN PREFERENCE CHECK". "not dying" → box 1 types on: "Not dying of horrible diseases". "to" (the long one before the second "dying") → the Grim Reaper rises from behind the hill, his tally clipboard under his arm. "dying" (second) → box 2 types on, "Dying of horrible diseases", and the Reaper leans over, helpfully holding out a pencil at box 2. "diseases." (last) → the Rich Human snatches the pencil and ticks box 1. after "diseases." → the Reaper sinks back behind the hill, sulking, and makes a note on his clipboard.

Sound: a whoosh as the card unrolls; a chair squeak as it spins; a falling slide whistle as the stack slides; a pop for the extra paper; a sparkle for the LATER stack; a cash-register ding for the dollar eyes; soft pats for the dice's footsteps; a clatter as they roll; a thunk on snake eyes; a squeak as the tie is straightened; a typewriter as the form types; a whoosh as the Reaper rises; a pencil scratch on the tick; a falling slide whistle as the Reaper sinks.

On screen: "STEP 1: GET MANY PAPERS FROM RICH HUMANS" / "1,000,000,000" then "1,000,000,001" / "LATER" / "RICH HUMAN PREFERENCE CHECK" / "☐ Not dying of horrible diseases ☐ Dying of horrible diseases" / the form's fine print: "Not reading this form counts as box 2." No: no "INVESTMENT" label (the dice are the joke); no real banknotes. Why: Step 1 needs one rich human to pick the obvious box, and the Reaper shows what the other box means.

## Scene 4 · 2800-top-hats

- id: 2800-top-hats
- act: Step 1
- transition_in: same form (no seam)
- key: on "living": the spotlight on our Rich Human, his top hat lit, the button on his lapel
- cue: "There are approximately two thousand"
- time: 09:40.8 to 09:48.5 (7.6 s)
- voiceover: "There are approximately two thousand eight hundred of these humans on your planet. Statistically, at least one of them prefers living."
- layer: B
- scene: The camera pulls back from the Rich Human's hat to a grid of 2,800 fat cats on hills of papers; a spotlight sweeps the grid and stops three times: a headstone, a sleeper, and our man.
- wishonia: PiP, neutral-smile, then happy-smile + body-open-palms on "living."
- props: rich-human, plain-paper, headstone, top-hat, reaper, clipboard, spotlight
- status: outline

Moves: "There" → the first frame is step-1-dice-in-a-suit's last: the Rich Human with box 1 ticked, the Reaper's hood sinking behind the hill. "two thousand eight hundred" → the camera pulls back fast: his top hat becomes one in a grid of 2,800 tiny top hats on 2,800 tiny hills, and a counter runs up to "About 2,800 humans with 1,000,000,000 papers". "Statistically," → a spotlight clunks on and sweeps the grid; it stops on a headstone wearing a top hat, a monocle hanging off it, the Grim Reaper leaning on it and adding a tally mark (that one ticked box 2). "least" → it jumps to a fat cat asleep face down on his money, snoring. "one" → it swings back toward the hill we came from. "living." → it lands on our Rich Human: his top hat lights up and he waves the ticked form. after "living." → a button pops onto his lapel, "I PREFER LIVING", and a second counter line appears: "You need: 1", with a teal check.

Sound: a rising slide whistle as the camera pulls back; ticks as the counter runs; a switch as the spotlight comes on; a pencil scratch for the Reaper's mark; a snore; a ding as the hat lights; a pop for the button.

On screen: "About 2,800 humans with 1,000,000,000 papers" / "You need: 1" / "I PREFER LIVING" (the button). Why: the odds; the plan needs one yes out of 2,800, and the three stops are the three kinds.

## Scene 5 · step-2-loud-humans

- id: step-2-loud-humans
- act: Step 2
- transition_in: slide left
- key: on "thing": every megaphone turned to the camera mid-blast, the bubbles turning into teal pill bottles
- cue: "Step two: Give Some"
- time: 09:48.5 to 10:04.3 (15.8 s)
- voiceover: "Step two: Give Some of the Papers to Loud Humans Some humans are very loud on the internet. If you give them papers, they become loud about your thing instead of other things. This is called "marketing" which is lying but with graphics."
- layer: B
- scene: A row of Loud Humans (megaphones for heads) shout at each other over laptops; the stream of plain papers marches in and hops into the megaphones; every megaphone swings to the camera and blasts; then a pie chart in sunglasses struts past.
- wishonia: PiP, smirk-smile, then surprised-oh on "thing", then smirk-smile on "marketing"
- props: step-card, scroll, loud-human, laptop, plain-paper, pill-bottle, human, pie-chart
- status: outline

Moves: "Step two" → the step 2 card unrolls. after "Humans" (first) → it rolls up into its tab. "loud" (second) → four Loud Humans, each with a different everyday build (a barrel, a beanpole, an hourglass, a refrigerator box), stand behind laptops on little stands and shout at each other; scribbled speech bubbles cross between them (a cat, a sandwich, an angry squiggle). "internet." → the bubbles pile up and tangle. "If" → the stream of plain papers walks in from the left. "papers," → one paper hops into each megaphone, gulp. "your" → every megaphone swings round to the camera. "thing" → they all blast at once: every bubble becomes a teal pill bottle and the frame shakes. "other things." → the old scribbled bubbles blow off the left edge like leaves, and a passing everyday human is blown clean out of his shoes and off the frame; the shoes stay, smoking. "marketing" → a pie chart wearing sunglasses struts in along the front. "lying" → its three slices read 60%, 60% and 60%. after "graphics." → it lowers its sunglasses at the camera and winks; a sparkle on the lens.

Sound: a whoosh as the card unrolls; a megaphone squawk; a scribble scratch as the bubbles tangle; pops as the papers hop in; a whoosh as the megaphones swing; a boom for the blast; a whoosh as the bubbles blow away; a boing as the human leaves his shoes; soft pats for the strut; a sparkle on the wink.

On screen: "STEP 2: GIVE SOME OF THE PAPERS TO LOUD HUMANS" / "60%" "60%" "60%" (the slices). No: no real platforms, logos or faces on the laptops; scribbles only. Why: Step 2 buys attention, and the chart shows what the attention is made of.

## Scene 6 · step-3-lobbyist-funnels

- id: step-3-lobbyist-funnels
- act: Step 3
- transition_in: slide left
- key: on "legal": the LEGAL stamp lifting off the Politician's forehead, the paper back in his pocket, his grin unbothered
- cue: "Step three: Give Some"
- time: 10:04.3 to 10:24.5 (20.2 s)
- voiceover: "Step three: Give Some of the Papers to the Humans Who Give Papers to Politicians Politicians don't take papers directly (that's "illegal"). Instead, you give papers to people called "lobbyists." The lobbyists give papers to "campaigns." The campaigns give papers to politicians. It's like money laundering but backwards and legal."
- layer: B
- scene: A paper the Politician will not touch goes the long way round: flattened by an ILLEGAL sign, into the masked Lobbyist's briefcase, along a conveyor into a washing machine labeled CAMPAIGN, and into the Politician's pocket; then the route runs backwards and forwards again, and a stamp says LEGAL.
- wishonia: PiP, smirk-smile, then eyeroll-smile + body-shrug on "legal"
- props: step-card, scroll, politician, lobbyist, plain-paper, sign, conveyor, washing-machine, stamp, stamp-mark
- status: outline

Moves: "Step three" → the step 3 card unrolls. after "Politicians" (first) → it rolls up into its tab. "take" → a paper from the stream walks up to the Politician (lantern jaw, toothy grin, wide tie, flag pin) and holds itself up to be taken. "directly" → he jumps back with both palms up, horrified, still grinning. "illegal" → a sign marked "ILLEGAL" drops in on a rope and flattens the paper. "Instead," → the paper peels itself off the floor, springs back into shape and turns away. "lobbyists." (first) → the Lobbyist (fedora low, domino mask, trench coat, gloves) tiptoes in from the left and clicks his briefcase open; it has a funnel on top. "lobbyists" (second) → the paper hops into the funnel; the Lobbyist tiptoes to a conveyor, the briefcase leaking other papers behind him. "campaigns." (first) → the paper drops out onto the conveyor and rides along it. "campaigns" (second) → it drops into a 1950s washing machine labeled "CAMPAIGN", which sloshes. "politicians." (last) → the machine spits it straight into the Politician's breast pocket. after "politicians." → he looks away, whistling. "laundering" → the washing machine starts to spin. "backwards" → the whole route runs in rewind at speed: the paper flies back out of the pocket, back through the machine, back along the conveyor, out of the briefcase and back in front of the Politician; the ILLEGAL sign rises back up its rope. "and" → then it all runs forward again at triple speed, and the paper lands back in his pocket. "legal." → a rubber stamp slams "LEGAL" onto the Politician's forehead; he keeps grinning. The stamp mark stays on him for the rest of the part.

Sound: a whoosh as the card unrolls; a squeak of tiny footsteps; a gasp as he jumps back; a slam and a splat as the sign lands; a boing as the paper peels up; a click as the briefcase opens; a pop as the paper hops in; a thunk into the washing machine; a cash-register ding into the pocket; whistling; a whirr as the machine spins; a rising slide whistle for the rewind; a whoosh forward; a rubber-stamp thunk.

On screen: "STEP 3: GIVE SOME OF THE PAPERS TO THE HUMANS WHO GIVE PAPERS TO POLITICIANS" / "ILLEGAL" / "CAMPAIGN" / "LEGAL". No: no real lobbying firms or campaigns; plain signs only; no "money laundering" label (the washing machine is the label). Why: the same paper reaches the same pocket; only the route makes it legal.

## Scene 7 · step-4-super-pac

- id: step-4-super-pac
- act: Step 4
- transition_in: slide left
- key: on "else": the Lobbyist's glove patting the SUPER PAC label down over BRIBERY, the river pouring in, the burst PAC beside it, the Politician high on his poster podium
- cue: "Step four: Give Some"
- time: 10:24.5 to 10:47.7 (23.2 s)
- voiceover: "Step four: Give Some of the Papers to the Politicians' Friends Politicians have friends called "Super PACs" which are like normal PACs but super. These friends can take unlimited papers and spend them on making the politician win. This isn't bribery because you called it something else. (This is part of the six hundred and fifty million dollar lobbying budget.)."
- layer: B
- scene: A plain backpack labeled PAC sits next to a caped backpack labeled SUPER PAC, which swallows a river of papers without filling and fires the Politician's posters until his podium hits the top of the frame.
- wishonia: PiP, neutral-smile, then smirk-closed on "else"
- props: step-card, scroll, backpack, plain-paper, politician, stamp-mark, poster, podium, lobbyist, price-tag
- status: outline

Moves: "Step four" → the step 4 card unrolls. after "Friends" (first) → it rolls up into its tab. "Super PACs" → a backpack with a cape swoops in and lands, labeled "SUPER PAC". "normal PACs" → a plain backpack labeled "PAC" sits beside it and looks up at it. "super." (last) → the cape flaps and the Super PAC strikes a hero pose. "unlimited" → the stream arrives as a river of plain papers from the left and pours into the Super PAC, which never fills; a few papers spill into the plain PAC. "papers" (second) → the plain PAC bursts at the seams: five papers was its limit. "win." → the Super PAC fires campaign posters like a machine gun (each poster is the Politician's grin, LEGAL still on his forehead) and they plaster the background; the Politician rises on a podium of stacked posters, up and up. after "win." → his head bonks the top of the frame; stars circle it. "bribery" → the SUPER PAC label lifts at one corner, showing the old word underneath: "BRIBERY". "else." → the Lobbyist's gloved hand reaches in from the edge and pats the label back down. "six hundred and fifty million" → a price tag drops onto the river on a string: "PART OF THE $650 MILLION LOBBYING BUDGET".

Sound: a whoosh as the card unrolls; a whoosh as the Super PAC swoops in; a sparkle on the hero pose; a pop as the plain PAC bursts; pops as the posters fire; a rising slide whistle as the podium rises; a thunk on the bonk; a scratch as the label peels; soft pats as the glove smooths it; a cash-register ding for the tag.

On screen: "STEP 4: GIVE SOME OF THE PAPERS TO THE POLITICIANS' FRIENDS" / "PAC" / "SUPER PAC" / "BRIBERY" (under the label) / "PART OF THE $650 MILLION LOBBYING BUDGET". No: no real Super PACs or campaigns; the posters carry the grin and no name. Why: Super PACs take unlimited papers, and the plan budgets for them.

## Scene 8 · step-5-treaty-split

- id: step-5-treaty-split
- act: Step 5
- transition_in: slide left
- key: on "works": the three teal streams flowing, the infinity sign looping over the hill, the bearded Rich Human giving a thumbs-up, the Reaper's pencil about to snap
- cue: "Step five: Give Papers"
- time: 10:47.7 to 11:22.6 (34.9 s)
- voiceover: "Step five: Give Papers You Get Back From The Government Back to the Rich Humans (Forever) Your treaty passes, redirecting twenty-seven point two billion dollars in papers annually. Eighty percent funds clinical trials (the point). Ten percent goes to a fund that rewards politicians who voted yes. Ten percent goes back to the rich humans as returns, forever. This is a good deal because forever is a long time. Unless you die from preventable diseases. Which you're fixing, so it works out."
- layer: B
- scene: The treaty passes; a river of war money from the missile factory goes through the color-flip funnel and comes out medicine money, then splits three ways: 80% into a lab and a hospital, 10% to a fund that rewards yes votes, and 10% back up the Rich Human's hill, forever. Forever is long enough for a beard, a skeleton and a rescue from the lab.
- wishonia: PiP, happy-smile, then happy-smile + body-point-right on "Eighty", then surprised-oh on "die", then smirk-smile on "works"
- props: step-card, scroll, politician, stamp, stamp-mark, factory, papers-red, color-flip-funnel, papers-teal, lab, hospital, scientist, sign, bank, yes-button, ribbon, rich-human, infinity-sign, calendar, reaper, clipboard
- status: outline

Moves: "Step five" → the step 5 card unrolls. "(Forever)" → it keeps unrolling past the right edge of the frame and on out of sight. after "(Forever)" → it whips back and rolls up into its tab. "treaty" → the Politician (LEGAL still on his forehead) signs a treaty scroll with a huge flourish. "passes," → a stamp slams "PASSED" on it. "redirecting" → the missile factory's door opens and a river of war money (green, red missile seals) marches out and up into the color-flip funnel. "twenty-seven point two billion" → a counter on the funnel spins up: "$27.2 billion / year". "dollars" → out of the spout come the same bills with teal cross seals, each seal flipping with a sparkle. "Eighty percent" → most of the teal papers march down into a lab and a hospital; the scientist in the lab catches them and her flask bubbles over. "point)." → a sign springs up on the lab's roof: "THE POINT", with an arrow pointing down at the lab. "Ten percent" (first) → a tenth march into a small bank labeled "YES-VOTE FUND". "voted yes." → the Politician slaps a big YES button on its front. after "yes." → the bank pins a ribbon on his chest and dumps a shower of teal papers on his head; his grin grows more teeth. "Ten percent" (second) → a tenth climb back up the Rich Human's hill into his arms. "returns," → his eyes turn into dollar signs. "forever." → an infinity sign lights up over the hill like neon. "forever" (third) → the sign keeps looping and the papers keep climbing. "long time." → a calendar beside the hill sheds its pages in a blizzard, and his walrus mustache grows into a long white beard that pours down the hill. before "Unless" → the Grim Reaper rises behind the hill, scribbling tally marks as fast as he can, and taps the Rich Human on the shoulder; the chest light blinks red. "die" → the Rich Human x-rays into a grinning skeleton (top hat, monocle and beard still on), still catching his returns; the papers keep climbing into its arms. "preventable" → the Reaper adds one more mark. "diseases." → the lab door bursts open and the scientist sprints up the hill with her bubbling teal flask, trailing dust. "fixing," → she dumps the flask over the skeleton, which flickers back into the Rich Human (the x-ray in reverse), beard and all; his chest light turns teal. "works" → he gives the camera a thumbs-up; the "I PREFER LIVING" button glints. after "out." → the Reaper's pencil snaps in half; he looks at the camera and sinks back behind the hill. The part ends on that frame.

Sound: a whoosh as the card unrolls; a whirr as it keeps going; a pen scratch for the signature; a rubber-stamp thunk; a hum from the funnel; a sparkle as the seals flip; a pop for THE POINT sign; a click for the YES button; a cash-register ding for the ribbon and the shower; a switch as the neon lights; a whoosh for the calendar blizzard; a falling slide whistle as the beard pours down; a whoosh as the Reaper rises; a zap for the x-ray; a pencil scratch for the tally; a slam as the lab door bursts open; a splat for the flask; a zap as the x-ray reverses; a ding for the thumbs-up; a snip as the pencil snaps; a falling slide whistle as the Reaper sinks.

On screen: "STEP 5: GIVE PAPERS YOU GET BACK FROM THE GOVERNMENT BACK TO THE RICH HUMANS (FOREVER)" / "PASSED" / "$27.2 billion / year" / "80% clinical trials" / "THE POINT" / "10% YES-VOTE FUND" / "10% rich humans, forever" / the infinity sign (drawn, not a font glyph). No: no real treaty, flags or banks; the medicine comes out of the lab the papers just funded, never off a shelf where it was waiting. Why: the payoff that makes Steps 1 to 4 worth paying for, the color flip at full size, and the Reaper shows what "unless you die" means before the lab takes the Rich Human back.
