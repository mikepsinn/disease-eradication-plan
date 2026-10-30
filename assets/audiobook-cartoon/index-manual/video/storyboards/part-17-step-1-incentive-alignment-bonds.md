---
format: 1920x1080
duration: 5:09.5
message: "Step 1 sells $1 billion of bonds whose treaty money would pay investors 272% a year, reward the politicians who vote yes, and send 80% to clinical trials, so greed keeps the treaty alive."
arc: Title card, five doors stuffed with money → the Reaper's tally while the arithmetic crawls by snail → the bond splits the treaty money 80/10/10 and the glass lid traps the Lobbyist's fingers → the fat cat bounces off the velvet rope and the Optimitron burns the useless policy like toast → Grandma's war bond, then Grandma's skeleton → YOU offer the fat cat a better deal and he becomes a lobbyist → nobody is the enemy, the Reaper pops out of the cuckoo clock → the money loop, steps 1 to 5, ending with a senator who sits up like a dog → greed runs the loop and the germs pop → an empty ring while the Reaper keeps count → the red loop prints headstones → the teal loop prints headstones for diseases → one loop grew wild, YOU planted the other
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 17, "The Five-Step Plan, Step 1: Sell Incentive Alignment Bonds"
audio: index-manual.cbaf659d.mp3, 35:43.4 to 40:53.0
version: v2
---

# Part 17 storyboard: "The Five-Step Plan, Step 1: Sell Incentive Alignment Bonds"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The 80/10/10 split. bond-splits-three-ways sets it up as one junction: a fat stream of medicine money to the lab, two thin ones through the glass box "CAPPED AT 20%". The money loop builds the same split as one big pipe plate shaped like a ring (the money loop plate, below): pipe-steps-one-two, pipe-steps-three-four, pavlovian-senators and greed-loop-runs are the same plate, the camera moving one quarter of it per step, and greed-loop-runs pulls back until the whole ring is in frame. The bond certificate starts every stage of it.

**Running gag (replaces the countdown board).** The Grim Reaper's tally (from Part 5). He keeps count of the humans that diseases kill, 150,000 a day. On the wall screen in financial-instrument he writes marks so fast his pencil smokes. In enemy-is-the-clock "the clock" is literal: a cuckoo clock, and the Reaper pops out of its door instead of a bird, adds a tally mark and snaps back, once every 0.58 seconds (86,400 seconds a day / 150,000, the true rate). The same clock hangs over the empty ring in no-opposition and keeps popping while the humans do their sum. In greed-loop-runs he waits at the hospital door and has to erase a mark.

**YOU.** The viewer is the busy human in the bowler from Part 1's title card, as in Parts 10 and 12 (`{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene). He is the empty "YOU" frame in grandmas-war-bond, hands the fat cat the bond in what-youre-offering, sells the VICTORY bonds at the counter in pipe-steps-one-two, and plants the teal loop in evolved-on-purpose.

**The cast.** The Rich Human is the fat cat (`KIT.cast("richHuman")`), with Part 5's "I PREFER LIVING" button still on his left lapel. The Politician (`KIT.cast("politician")`) has the toothy grin, the flag pin and the wide tie that flips between red and blue. The Lobbyist is the masked crook (`KIT.cast("lobbyist")`), the Weapons Maker the barrel chest with the hard hat and the baby missile (`KIT.cast("weaponsMaker")`), the Scientist the bun, glasses and flask (`KIT.cast("scientist")`), Grandma the curlers, cat-eye glasses and poster (`KIT.cast("grandma")`), the Loud Human the megaphone head (`KIT.cast("loudHuman")`). Everyone else is an everyday human whose body comes from the outfit.

**Shared drawings** (several author groups draw these, so they must match):
- **The bond certificate.** `KIT.props.bond({ text: "INCENTIVE ALIGNMENT BOND", value: "$1,000" })`, the certificate from human-greed (Part 13). The VICTORY bonds of the money loop are `KIT.props.bond({ text: "VICTORY BOND", value: "$1,000", seal: "med" })`.
- **The glass box.** A glass display case on four short navy legs, about 300 wide and 200 tall on the Earth paper: pale glass (#DCEFF0 at 0.55 opacity) with a 4 px navy outline and two white diagonal glints, a lid with a navy rim and a small brass handle, a cream plate on the lid "CAPPED AT 20%", a small brass plate on the front "FULLY TRANSPARENT". Inside, medicine money (`KIT.money("med")`) in neat rows, so every bill can be counted. bond-splits-three-ways, pipe-steps-three-four and pavlovian-senators.
- **The Super PAC.** Part 5's caped backpack: a rust canvas backpack about 120 wide and 150 tall with two navy straps, a cream patch "SUPER PAC" in Oswald capitals, a war-red cape tied at its top; it lands in a hero pose, leaning back with the cape flaring. bond-splits-three-ways, pavlovian-senators, patient-industrial-loop.
- **The cuckoo clock.** A carved 1950s cuckoo clock, about 200 wide and 260 tall: a tan house with a rust pointed roof and a carved navy trim, a cream face with navy hands, a little door above the face, two pine-cone weights on chains below, and a cream plaque under the face "150,000 / DAY". The Reaper (`KIT.reaper()` at about 0.35, his clipboard `KIT.props.clipboard` covered in navy tally marks in fives) pops out of the door on a zigzag spring, adds a mark and snaps back. enemy-is-the-clock and no-opposition (one author group).
- **The money loop plate.** One Earth-paper plate shaped like a ring, seen through four views, one per step; the money runs clockwise. The pipes are glass tubes (pale glass, 30 px wide, navy rim bands every 160 px), so the bills riding inside can be seen. Number tags "1" to "5" are Fraunces Black numerals on 90 px cream discs with a navy rim. pipe-steps-one-two, pipe-steps-three-four, pavlovian-senators and greed-loop-runs draw the same plate with the same code (copy it between the four files and change all four).
  - 16:9: the plate is 3840 × 2160; the views are top left (x 0 to 1920, y 0 to 1080), top right (x 1920 to 3840), bottom right (x 1920 to 3840, y 1080 to 2160) and bottom left (x 0 to 1920, y 1080 to 2160), each shown at scale 1. The pull-back in greed-loop-runs ends at scale 0.42 with the plate's top-left corner at screen (150, 0), which keeps the plate out of Wishonia's corner except its bottom-right tip (plate x 3450 up, y 1640 down: leave it empty).
  - Top left, step 1: tag "1" at (110, 110). The Rich Human, feet at (330, 820), facing right. YOU's counter "VICTORY BONDS", x 520 to 860, top y 560, base y 820, YOU behind it, a bond slot in its front at (600, 640). The hopper, x 900 to 1100, mouth y 420, outlet y 620, labeled "$1 BILLION". A pipe from the hopper along y 700 into the campaign office (x 1250 to 1560, y 380 to 820, "1% TREATY: YES" on its roof, a window at (1400, 560) for the Loud Human). From the office's right wall the pipe runs on along y 640 into the next view. The dividend pipe comes up the left edge at x 90 and ends in a spout over the Rich Human at (330, 320).
  - Top right, step 2: tag "2" at (2030, 110). The pipe ends at the treaty: `KIT.props.scroll({ text: "1% TREATY" })` on a stand, feet at (2150, 820). The "MURDER BUDGET" tank, x 2400 to 2800, y 200 to 820: a slate drum with a war-red band and the stencil, a level gauge on its front (`KIT.props.gauge({ mount: "dial" })` at (2600, 560)), the Weapons Maker sitting on its lid at (2600, 200) rocking his missile. Its outlet along y 760 carries a war-red valve wheel at (2900, 760) and rises into the color-flip funnel (`KIT.props.colorFlipFunnel`, base at (3200, 860)). The teal pipe leaves the spout along y 836, turns down at x 3480, and carries the tag "$27.2 BILLION / YEAR".
  - Bottom right, step 3 and the 80%: tag "3" at (2030, 1190). The teal pipe comes down x 3480 into the "VICTORY CORPORATION" valve house (a rust brick gatehouse with a cream sign, x 3050 to 3450, y 1150 to 1500). A side valve on its left wall at (3050, 1300) feeds the glass box (x 2550 to 2850, base y 1420); tag "4" at (2420, 1190). The fat 80% pipe leaves the valve house's bottom, drops to y 1620 and runs left to the lab (`KIT.props.lab`, base at (2700, 1980)) and the hospital (`KIT.props.hospital`, base at (2200, 1980)); the Grim Reaper stands by the hospital door at (2000, 1980); three or four germs (`KIT.props.germ`) cling to the two roofs.
  - Bottom left, steps 4 and 5: the glass box's top outlet (the dividend pipe) runs left along y 1120 to x 90 and up into the top-left view. Its bottom outlet runs left along y 1500 into the Super PAC (base at (1500, 1760)); tag "5" at (1760, 1500). Three senators stand with their feet on y 1960 at x 700, 900 and 1100, each with a billboard frame behind him on two posts (base y 1700); the "POST-OFFICE CAREERS" door (`KIT.props.door`) stands at (330, 1960). A dashed navy "YES" line runs from the senators up the middle of the plate to the treaty scroll, so the loop closes through their votes.
  - 9:16: the plate is 2160 × 3840 with the same four views (each 1080 × 1920) and the same stations in the same ring order, stacked top to bottom inside each view; keep each view's art out of the saucer corner (view x 740 to 1040, y 60 to 430) and above view y 1450. The pull-back ends at scale 0.5 (the whole plate); keep the bottom views' important art above view y 1100 so it clears the captions there.
- **The red loop.** The "MILITARY INDUSTRIAL COMPLEX" ring: a fat war-red arrow ring with a navy outline, dark slate gears (`KIT.props.gears({ dark: true })`) on it, and four stations: the Weapons Maker at 9 o'clock, the Politician at 12, a contract with a missile drawn on it at 3, and the contractors' factory (`KIT.props.factory`, missile chimneys) at 6. In the middle a printing press (`KIT.props.printingPress({ seal: "war" })`) prints war money and small grey headstones (`KIT.props.headstone`) onto a pile beside it. 16:9: the ring is centered at (820, 470) with an outer radius of 330, the title "MILITARY INDUSTRIAL COMPLEX" above it at y 60, the stations at (820, 140), (1150, 470), (820, 800) and (490, 470). 9:16: centered at (540, 700), the same radius, the title at y 280. military-industrial-loop draws it there at full size; patient-industrial-loop opens on that exact frame and moves it to scale 0.72 centered at (480, 470) (9:16: (540, 470)), with the mirror teal ring at scale 0.72 centered at (1180, 470) (9:16: (540, 1090)); evolved-on-purpose keeps both there. The teal ring is the same drawing in teal (`C.med`), with stations INVESTORS (9 o'clock), POLITICIANS (12), CLINICAL TRIALS (3, `KIT.props.lab`) and RETURNS (6), and a teal press (`KIT.props.printingPress({ seal: "med" })`) in its middle.

**Callback.** From Part 13 (human-greed): the bond certificate that slid onto the wall screen lands on Wishonia's desk in financial-instrument. From Part 14 (optimitron-appliance): the Optimitron prints the governments' report cards in wishocratic-allocation. From Part 5: the Super PAC backpack with the cape, the "I PREFER LIVING" button, the Grim Reaper and his tally. From Part 3: the snail from the title card carries the arithmetic across the wall screen in financial-instrument. From Part 8 (falling-apart): the reader in his armchair nods off on the pull-down chart in stop-reading. From Part 1: the moth from the empty wallet flies out of the red loop's empty blueprint drawer in evolved-on-purpose.

**Callback set up here.** The title card's five numbered doors. Door 1 bursts open here; the Step 2 to Step 5 title cards (Parts 18 to 21) can each open their own door. The Super PAC and its stream come back in super-pac-rewards (Part 20). The Lobbyist's briefcase with the funnel on top, which the fat cat picks up in what-youre-offering, is Part 19's spine.

**Held frames.** financial-instrument, after "day" (1 s). grandmas-war-bond, after "eighty-seven" (1 to 2 s). no-opposition, after "funerals" until "finish" (1 to 2 s): only the Reaper's pencil moves (it is the count, not a gag). A HOLD is silent.

**Bans for this part.**
- No real people or logos. Eisenhower is a text card only. The bond, the poster, the billboards and the Super PAC carry plain words only.
- No Nazi uniforms, symbols or flags: "Nazis" appears as words on Grandma's list only.
- No money handed to a politician in the new system: the Super PAC pays for billboards and careers. (In the red loop, the old system, the Weapons Maker does stuff the Politician's pocket.)
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: in 16:9 nothing important below y 900; in 9:16 nothing important from y 1450 down. Keep Wishonia's corner clear (16:9 x 1600 to 1920, y 690 down; 9:16 x 740 to 1040, y 60 to 430).
- Money is always money green. All treaty money is medicine money (teal cross seal) from the moment it leaves the color-flip funnel, the 10% shares included; the papers the Rich Human pays for his bonds are plain; the red loop's papers are war money.

## Changes from v1

- The countdown board is gone from the kit. Its job (150,000 people a day, while time passes) goes to the Grim Reaper's tally from Part 5: on the wall screen in financial-instrument, then popping out of a cuckoo clock at the true rate in enemy-is-the-clock and no-opposition.
- The humans are the stereotype cast, and YOU (Part 10's bowler man) is the reader wherever the narrator says "you": the empty frame against Grandma, the seller of the bonds, the gardener of the teal loop.
- The gags go all the way: money squeezes out under the title card's doors, the glass lid flattens the Lobbyist's fingers, the fat cat bounces off the velvet rope and rolls away, the Optimitron's useless policy comes out burnt and gets pocketed, Grandma x-rays into a skeleton and her headstone rises, the fat cat puts on the Lobbyist's mask, faints at 272% and lies rocking like a tipped egg, the senator sits up and begs for a biscuit, the germs pop, the Lobbyist turns into a skeleton mid-sum, a missile chimney launches and a headstone lands, the teal loop prints headstones for diseases.
- The money loop plate is a ring, so the pull-back in greed-loop-runs shows a loop, and the dividends ride back to the Rich Human who paid in.
- The title card cuts in (the parts are rendered on their own and joined, and a title card has no wall screen).
- Recurring props come from the shared library (`KIT.props.*`); every scene has a Sound line.

## Scene 1 · step-1-incentive-alignment-bonds-title

- id: step-1-incentive-alignment-bonds-title
- act: Title
- transition_in: cut (the parts are rendered on their own and joined)
- key: after "Bonds.": the heading and the italic line in, the five doors in a row, door 1 burst open with papers spilling out of it, the Step 1 line on its own row above the doors
- cue: "The Five-Step Plan."
- time: 35:43.4 to 35:53.3 (9.8 s)
- voiceover: "The Five-Step Plan. *Saving Humanity While Making Everyone Obscenely Wealthy* Step One: Sell Incentive Alignment Bonds."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`) with the heading high on the card; five numbered doors stand in a row under it. The doors are stuffed with money; door 1 bursts open and the Step 1 line rides out of it.
- wishonia: not on screen
- props: titleScene, door, money("plain")
- status: outline

Moves: "The" → "THE" slams in. "Five-Step" → "FIVE-STEP" slams in, and five doors (`KIT.props.door`, labels "1" to "5") drop into a row along the bottom of the card and land with a clank. "Plan." → "PLAN" slams in. "Saving" → the italic line slides up under the heading. "Obscenely" → green papers squeeze out from under all five doors, and the doors creak and bulge on their hinges. "Wealthy" → door 3's knob pops off and bounces away across the card. "One:" → door 1 bursts open and an avalanche of plain papers pours out across the bottom of the card. "Incentive" → the Step 1 line rides out of door 1 on top of the papers and rises to its own row above the doors. "Bonds." → it lands with a thunk. Doors 2 to 5 stay shut, still bulging.

Sound: a thunk on each heading word; a clank as the doors land; a whoosh for the italic line; door creaks as they bulge; a boing for the knob; a slam as door 1 bursts open and a whoosh for the avalanche; a rising slide whistle as the Step 1 line rises; a thunk as it lands.

On screen: "THE FIVE-STEP PLAN" / "Saving Humanity While Making Everyone Obscenely Wealthy" / "STEP 1: SELL INCENTIVE ALIGNMENT BONDS" / door numbers "1" to "5". Why: the narrator reads the heading, its italic line and the step, so one card holds all three; the doors set up Steps 2 to 5.

## Scene 2 · financial-instrument

- id: financial-instrument
- act: Why bonds
- transition_in: cut
- key: after "one.": the bond certificate just landed on the desk in front of Wishonia, its gold seal glinting, the squeezed-up timeline on the wall screen behind her
- cue: "On my planet, people"
- time: 35:53.3 to 36:16.9 (23.6 s)
- voiceover: "On my planet, people do useful things because they're useful. On Earth, you need a financial instrument. Not because anyone rationally opposes curing diseases (they don't; see above), but because one hundred and fifty thousand people die per day while the arithmetic propagates, and money is how you compress the timeline. So here's one."
- layer: A
- scene: Wishonia explains why Earth needs a money device while the wall screen shows her planet, then a human who only moves for money, an empty protest, the Grim Reaper's tally and a snail carrying the arithmetic; on "here's" the bond certificate from human-greed lands on the desk.
- wishonia: neutral-smile + body-open-palms, then sad-small + body-palms-down on "die", then happy-smile + body-wide-gesture on "compress", then smirk-smile + body-presenting on "here's"
- props: office, wallScreen, desk, mug, bond, money("plain"), sign, clipboard, reaper, snail, timeline-ribbon
- status: outline

Moves: "useful" (first) → the wall screen shows small blue Wishonians hammering a bridge together, no money anywhere. "Earth," → it switches to Earth: an everyday human asleep in a hammock. "financial" → a plain paper dangles in front of his nose on a fishing line from the top of the screen. "instrument." → he springs out of the hammock and chases it round and round the screen; the hammock flips over. "opposes" → an empty protest stand with a sign "AGAINST CURING DISEASES" and nobody behind it; crickets. "one hundred and fifty thousand" → the wall screen: the Grim Reaper at a little desk, writing tally marks on his clipboard so fast his pencil smokes; the page heading reads "150,000 DIE PER DAY". "day" → HOLD 1 s. "propagates," → the snail from Part 3's title card crawls across the bottom of the screen on a long timeline ribbon, a sum strapped to its shell; the Reaper strolls past it, still writing. "compress" → Wishonia spreads her arms, and the ribbon on the wall screen squeezes shut like an accordion. "timeline." → the snail shoots to the far end and lands with its eye stalks spinning. "here's" → the bond certificate (`KIT.props.bond`, "INCENTIVE ALIGNMENT BOND", the one from human-greed) slaps down on the desk in front of Wishonia, and the mug jumps. after "one." → its gold seal glints.

Sound: hammering for the Wishonians; a switch as the screen changes; a squeak as the paper dangles; a boing as the human springs up; crickets at the empty stand; a marker scratch for the tally; silence for the HOLD; a small squeak for the snail; a whoosh as the ribbon squeezes; a boing as the snail lands; a slam for the certificate; a sparkle on the seal.

On screen: "AGAINST CURING DISEASES" (the empty stand) / "150,000 DIE PER DAY" / "INCENTIVE ALIGNMENT BOND". No: no new countdown device; the Reaper's tally carries the number. Why: the bond exists to buy time, not to win an argument.

## Scene 3 · bond-splits-three-ways

- id: bond-splits-three-ways
- act: The split
- transition_in: zoom into the wall screen
- key: after "transparent.": three streams running (fat to the lab, thin to the Rich Human's hat, thin to the Super PAC), the glass lid down on the two thin ones, the Lobbyist's masked face pressed to the glass and his flattened fingers still under the lid
- cue: "An Incentive Alignment Bond"
- time: 36:16.9 to 36:51.4 (34.5 s)
- voiceover: "An Incentive Alignment Bond funds a policy campaign, then splits the resulting government savings three ways: eighty percent to clinical trials, ten percent to investors as a revenue share on treaty funds, and ten percent to a Super PAC that rewards politicians who voted yes (campaign support while they're running, cushy post-office careers when they're done). Investors give money, get more money back. Politicians get reelected. Eighty percent goes to curing diseases. The corruption is capped at twenty percent and fully transparent."
- layer: B
- scene: The bond certificate from the desk drops onto the paper, walks to a campaign sign, and the treaty money it wins splits at a pipe junction: a fat medicine stream to a lab, a thin one into the Rich Human's top hat, a thin one into the caped Super PAC; the glass box closes over the two thin streams.
- wishonia: PiP, happy-smile + body-presenting, then smirk-smile + body-hands-hips on "corruption"
- props: bond, sign, colorFlipFunnel, money("war"), money("med"), lab, richHuman, politician, lobbyist, scientist, germ, door, glass-box, super-pac, billboard
- status: outline

Moves: "Bond" → the certificate from financial-instrument drops onto the paper from the top. "funds" → it sprouts stick legs and walks to the left. "campaign," → a campaign sign springs up in front of it: "1% TREATY: YES". "government" → war money drops into the color-flip funnel at the top of the paper. "savings" → it comes out of the spout as medicine money, each seal flipping. "three" → the pipe under the spout splits into three with a clank. "eighty" (first) → the fat stream runs down to a lab; the Scientist in its door catches the papers. "investors" (first) → a thin stream runs to the Rich Human, who holds his top hat out upside down. "Super PAC" → the other thin stream pours into the caped Super PAC backpack, which swoops in and strikes its hero pose. "voted yes" → the Super PAC throws a billboard up behind the Politician: his grin, a "YES" button. "running," → he jogs on the spot and the Super PAC runs beside him, handing him paper cups of water like at a marathon. "post-office" → a door "POST-OFFICE CAREERS" swings open behind him on a comfy armchair and a golf bag. "back." → the top hat overflows and the Rich Human's monocle pops out. "reelected." → three "RE-ELECTED" sashes drop onto the Politician one after another. "diseases." → the lab door bangs open and a germ (`KIT.props.germ`) is booted out; it lands flat on its back, dead, tongue out. "capped" → the glass box's lid slams down over the two thin streams, right on the gloved fingers of the Lobbyist, who was tiptoeing up to them with his briefcase; he yelps. "transparent." → the glass gleams; every paper inside can be counted. after "transparent." → the Lobbyist presses his masked face to the glass and fogs a patch of it; his fingers are still flat under the lid.

Sound: a thunk as the certificate lands; a pop for the campaign sign; a sparkle as the seals flip; a clank as the pipe splits; a whoosh for the fat stream; a cash-register ding for the hat; a whoosh as the Super PAC swoops in; a thunk for the billboard; soft pats for the jogging; a door squeak; a ding and a pop for the overflowing hat and the monocle; three thunks for the sashes; a slam and a splat for the booted germ; a slam for the lid and a yelp; a sparkle on the glass; a squeak as the face presses on it.

On screen: "1% TREATY: YES" / "80% CLINICAL TRIALS" · "10% INVESTORS" · "10% SUPER PAC" / "POST-OFFICE CAREERS" / "RE-ELECTED" / "CAPPED AT 20%" · "FULLY TRANSPARENT". No: no money handed to the Politician; the Super PAC pays for the billboard, the water and the career. Why: the whole bond in one picture, and the cap is the part money cannot get past.

## Scene 4 · wishocratic-allocation

- id: wishocratic-allocation
- act: The split
- transition_in: slide left
- key: after "nothing.": the voting board lit with medicine money on every disease row, the velvet rope shut, the Rich Human rolled away, the burnt report card halfway into the Politician's pocket
- cue: "The other eighty percent"
- time: 36:51.4 to 37:08.5 (17.1 s)
- voiceover: "The other eighty percent goes directly to clinical trials through wishocratic allocation, where nobody with money gets to decide where it goes. Meanwhile, the Optimitron tells governments which of their own policies are working and which ones are expensive ways to accomplish nothing."
- layer: B
- scene: The fat medicine stream from bond-splits-three-ways reaches a big public voting board; everyday humans each set a paper on a disease row; a velvet rope keeps the Rich Human out; the Optimitron prints report cards for the Politician.
- wishonia: PiP, neutral-smile + body-point-right, then smirk-closed + body-arms-crossed on "nothing."
- props: voting-board, velvet-rope, sign, richHuman, optimitron, politician, money("med"), human
- status: outline

Moves: "eighty" → the fat medicine stream runs in from the left edge to a big public voting board with disease rows ("CANCER", "HEART DISEASE", "ALZHEIMER'S", "RARE DISEASES"). "wishocratic" → the board lights. "allocation," → a line of everyday humans each sets one medicine paper on a row, tick, tick, tick. "nobody" → the Rich Human waddles toward the board waving his fat stack of cash. "money" → a velvet rope on two brass posts clips shut in front of his belly, its sign "NO MONEY PAST THIS ROPE". "decide" → he tries to step over it; his stub legs are too short, and he bounces off it belly first. "goes." → he tips over and rolls away like an egg, out of frame. "Optimitron" → the Optimitron from optimitron-appliance (`KIT.props.optimitron`) slides in beside the board; the Politician stands at it, hands out for a card. "working" → card 1 pops up like toast: "WORKING"; the Politician beams and holds it up. "nothing." → card 2 pops up: "EXPENSIVE WAY TO ACCOMPLISH NOTHING". after "nothing." → it is burnt black and smoking like overdone toast; the Politician blows on it and quietly slides it into his pocket.

Sound: a switch as the board lights; three ticks as the papers go on; soft pats as the Rich Human waddles; a click for the rope; a boing as he bounces; a falling slide whistle as he rolls away; a whirr for the Optimitron; a toaster pop per card; a sizzle for the burnt one.

On screen: "WISHOCRATIC ALLOCATION" / the disease rows / "NO MONEY PAST THIS ROPE" / "WORKING" · "EXPENSIVE WAY TO ACCOMPLISH NOTHING". No: no real candidates, parties or agencies on the cards. Why: who decides the 80%, that money cannot buy a say, and what governments do with bad news.

## Scene 5 · grandmas-war-bond

- id: grandmas-war-bond
- act: What Grandma got
- transition_in: slide left
- key: after "eighty-seven.": all three lines ticked, Grandma a grinning skeleton in curlers still holding her poster up, her headstone "1987" in front of her, the empty "YOU" frame on the right
- cue: "Remember when your grandparents"
- time: 37:08.5 to 37:31.7 (23.2 s)
- voiceover: "Remember when your grandparents funded World War Two by buying bonds? They got four percent returns and a world without Nazis (mostly). You're proposing the same thing. What Grandma Got. Dead Nazis (admittedly good). Four percent returns (barely beat inflation). Still died of cancer in nineteen eighty-seven."
- layer: B, split screen (9:16: top and bottom)
- scene: Left half: Grandma waves her 1940s war-bond poster and her list ticks in, line by line, until the last line takes her. The right half is an empty frame labeled "YOU", waiting.
- wishonia: PiP, happy-smile + body-hand-chest, then sad-small + body-idle on "cancer"
- props: grandma, priceTag, checkbox, tick, headstone, sign
- status: outline

Moves: "grandparents" → Grandma (`KIT.cast("grandma")`) hobbles in on the left with her poster. "bonds?" → she waves it overhead: "BUY BONDS" (the cast's poster). "four" (first) → a "4%" price tag pins onto the poster. "(mostly)." → Grandma shrugs. "thing." → the right half's empty frame gets its label, stamped: "YOU". "Grandma" → the heading types on over the left half: "WHAT GRANDMA GOT". "Dead" → line 1 appears; "good)." → it ticks. "Four" (second) → line 2 appears. "inflation)." → the 4% tag sags on its string; after "inflation)." → line 2 ticks. "Still" → line 3 appears. "cancer" → it ticks, and Grandma's chest light blinks red. "nineteen" → she x-rays into a grinning skeleton, curlers and cat-eye glasses still on, poster still up. "eighty-seven." → a small headstone rises in front of her: "1987". Then HOLD 1 to 2 s; the skeleton keeps smiling.

Sound: soft pats as she hobbles in; a whoosh as the poster waves; a pop for the tag; a boing for the shrug; a stamp for "YOU"; a typewriter for the heading; a pencil scratch on each tick; a falling slide whistle as the tag sags; an x-ray zap; a thunk as the headstone rises; then silence for the HOLD.

On screen: "BUY BONDS" / "4%" / "YOU" / "WHAT GRANDMA GOT" / "Dead Nazis (admittedly good)" / "4% returns (barely beat inflation)" / "Still died of cancer in 1987" / the headstone "1987". No: no uniforms, symbols or flags; no real war poster. Why: humans already loved the bond idea, and its gap is the disease.

## Scene 6 · what-youre-offering

- id: what-youre-offering
- act: What Grandma got
- transition_in: same form (no seam)
- key: after "bonus).": both lists full, the Rich Human in the Lobbyist's mask and fedora holding the bond and the funnel briefcase, his "I PREFER LIVING" button swollen to the size of a hubcap, skeleton Grandma nodding at YOU
- cue: "What You're Offering. Dead"
- time: 37:31.7 to 38:00.7 (29.0 s)
- voiceover: "What You're Offering. Dead diseases (objectively better than dead Nazis because diseases kill more people). Two hundred and seventy-two percent annual returns (a revenue share on ten percent of treaty funds; if the treaty grows, so do their returns, which turns investors into the world's most motivated lobbyists for expanding it). Not dying from preventable meat failures (this is the big one). Also no Nazis (as a bonus)."
- layer: B, split screen (9:16: top and bottom)
- scene: The right half fills: YOU (the bowler man) hands the Rich Human a new bond, and a list ticks in line by line against Grandma's.
- wishonia: PiP, smirk-smile + body-presenting, then excited-open + body-excited on "Two", then happy-smile + body-hand-chest on "big"
- props: richHuman, bond, diseaseBlob, scroll, briefcase, checkbox, tick, grandma (skeleton), headstone
- status: outline

Moves: "What" → the first frame is grandmas-war-bond's last: skeleton Grandma, the headstone, the empty "YOU" frame. "Offering." → the right heading types on: "WHAT YOU'RE OFFERING"; YOU steps into the frame and holds out an Incentive Alignment Bond, and the Rich Human waddles in and takes it. "diseases" (first) → line 1 appears, and a disease blob in a "CANCER" sash (`KIT.props.diseaseBlob`) at the foot of the frame shrieks and keels over, dead. "people)." → line 1 ticks. "seventy-two" → line 2 appears and the Rich Human's eyes turn into dollar signs. "returns" (first) → line 2 ticks. "grows," → the treaty scroll under his arm grows longer, and his top hat grows taller to match it. "lobbyists" → he pulls the Lobbyist's domino mask on over his monocle, jams a fedora on top of the top hat, and picks up a briefcase with a funnel on top. "Not" → line 3 appears. "failures" → it ticks, and his "I PREFER LIVING" button swells. "big" → the button swells to the size of a hubcap and tips him forward. "one)." → line 3 underlines itself. "Also" → line 4 appears; "bonus)." → it ticks. after "bonus)." → on the left, skeleton Grandma gives YOU a slow nod, and her jaw clacks.

Sound: a typewriter for the heading; a shriek and a thunk as the blob keels over; a pencil scratch on each tick; a cash-register ding for the dollar eyes; a rising slide whistle as the hat grows; a snap as the mask goes on; a boing as the button swells; a marker squeak for the underline; two clacks for Grandma's jaw.

On screen: "WHAT YOU'RE OFFERING" / "Dead diseases (they kill more people)" / "272% annual returns" / "Not dying from preventable meat failures" / "Also no Nazis (bonus)" / the button "I PREFER LIVING" / the sash "CANCER". Why: the same deal as Grandma's, with the disease fixed and a bigger return, and the return makes the investor lobby for more.

## Scene 7 · enemy-is-the-clock

- id: enemy-is-the-clock
- act: The bribery machine
- transition_in: slide left
- key: after "clock.": the Reaper out of the cuckoo clock above the machine mid-mark, the three humans with their "NOT THE ENEMY" signs looking up at him, their waves frozen
- cue: "This raises the one"
- time: 38:00.7 to 38:10.0 (9.3 s)
- voiceover: "This raises the one billion dollars needed to fuel the rest of the bribery machine. Nobody in the machine is your enemy. The enemy is the clock."
- layer: B
- scene: A big 1950s machine labeled "THE BRIBERY MACHINE"; a $1 billion pile of plain papers goes into its hopper; the Lobbyist, the Politician and the Weapons Maker step out from behind it; then the cuckoo clock drops in above it and the Grim Reaper pops out of it.
- wishonia: PiP, neutral-smile + body-idle, then sad-closed + body-idle on "clock."
- props: bribery-machine, gears, money("plain"), richHuman, lobbyist, politician, weaponsMaker, sign, cuckoo-clock, reaper, clipboard
- status: outline

Moves: "billion" → the Rich Human tips his overflowing top hat into the machine's hopper and a "$1 BILLION" pile of plain papers slides in. "machine." (first) → the gears (`KIT.props.gears`, dark) start turning and the sign on top lights: "THE BRIBERY MACHINE". "Nobody" → the Lobbyist, the Politician and the Weapons Maker step out from behind the machine and wave at the camera. "enemy." (first) → a sign "NOT THE ENEMY" drops round each one's neck, pop, pop, pop; then a smaller one lands on the Weapons Maker's baby missile: "NOT THE ENEMY (PROBABLY)". "clock." → a cuckoo clock drops in on a hook above the machine; its door bangs open and the Grim Reaper pops out on a spring instead of a bird, adds a tally mark and snaps back in. after "clock." → he pops out again, and again, about twice a second (the true rate); the three humans slowly turn their heads up to look at him, their waves frozen.

Sound: a falling slide whistle as the pile slides in; a whirr and a switch as the machine starts; a pop for each sign (the missile's smaller); a thunk as the clock lands; a boing each time the Reaper pops out.

On screen: "$1 BILLION" / "THE BRIBERY MACHINE" / "NOT THE ENEMY" (three signs) / "NOT THE ENEMY (PROBABLY)" / the clock's plaque "150,000 / DAY". Why: names the real opponent, and it is time, not people.

## Scene 8 · stop-reading

- id: stop-reading
- act: The money loop
- transition_in: zoom out of the wall screen
- key: on "step:": the pull-down chart over the wall screen, its pull ring just bonked the drawn reader awake, Wishonia holding up one finger
- cue: "How the Money Loop"
- time: 38:10.0 to 38:17.6 (7.6 s)
- voiceover: "How the Money Loop Works. Here's the part where humans usually stop reading because it involves following money through more than one step:"
- layer: A
- scene: Wishonia pulls a chart down over the wall screen; on it the reader from Part 8 nods off in his armchair until the chart's pull ring bonks him awake.
- wishonia: skeptical-smile + body-point-right, then smirk-smile + body-counting on "one"
- props: office, wallScreen, desk, mug, pull-down chart, human (the reader)
- status: outline

Moves: "How" → the first frame is enemy-is-the-clock's last, small on the wall screen (`KIT.zoomView(screen).mini`): the Reaper out of the cuckoo clock. "Loop" → a pull-down chart (Earth paper cream) rolls down over the wall screen, its title "HOW THE MONEY LOOP WORKS" and under it a small drawing of the reader from falling-apart (Part 8) in his armchair, reading. "Works." → its bottom bar lands. "reading" → the drawn reader closes his book and nods off; a "Z" floats up. "one" → Wishonia holds up one finger. "step:" → the chart's pull ring swings down and bonks the reader on the head; he jolts awake with the book open again.

Sound: a whoosh as the chart rolls down; a thunk as it lands; a soft snore; a thunk and a boing for the bonk.

On screen: "HOW THE MONEY LOOP WORKS". Why: a breath before the longest chain of the part, aimed at the viewer about to tune out.

## Scene 9 · pipe-steps-one-two

- id: pipe-steps-one-two
- act: The money loop
- transition_in: zoom into the wall screen
- key: on "twenty-seven": war money pouring from the MURDER BUDGET tank into the color-flip funnel, medicine money walking out of the spout, the Weapons Maker on the tank's lid shrugging at the one-notch drop
- cue: "One. You sell one"
- time: 38:17.6 to 38:36.6 (19.0 s)
- voiceover: "One. You sell one billion dollars in VICTORY Incentive Alignment Bonds to investors. This funds the campaign. Two. The campaign succeeds. Your treaty redirects one percent of military spending: twenty-seven point two billion dollars a year flows from the murder budget to clinical trials."
- layer: B
- scene: The money loop plate, top left then top right. YOU sells VICTORY bonds over a counter to the Rich Human, his plain papers fund the campaign office, the treaty is signed, and the treaty valve sends war money through the color-flip funnel.
- wishonia: PiP, thinking-small + body-counting, then happy-smile + body-presenting on "twenty-seven"
- props: money-loop-plate, counter, bond, richHuman, money("plain"), hopper, campaign office, loudHuman, sign, scroll, tank, gauge, weaponsMaker, colorFlipFunnel, money("war"), money("med"), priceTag
- status: outline

Moves: "One." → the plate's top-left view; tag "1" drops by the counter. "sell" → YOU stands behind a little counter marked "VICTORY BONDS"; the Rich Human tips a hatful of plain papers into the hopper beside it. "VICTORY" → a VICTORY bond shoots out of the counter's slot and lands in his top hat. "investors." → he puts the hat back on, the bond sticking out of it like a feather. "campaign." → the hopper's papers slide down the glass pipe into the campaign office ("1% TREATY: YES" on its roof); the Loud Human bursts out of its window blasting "YES!". "Two." → the camera slides right to the top-right view; tag "2" drops by the treaty. "succeeds." → the 1% treaty scroll on its stand gets its signature. after "succeeds." → the valve wheel on the MURDER BUDGET tank spins open. "redirects" → war money pours out of the tank into the color-flip funnel. "spending:" → the tank's level gauge drops by one notch (1%); the Weapons Maker sitting on its lid glances down, shrugs and keeps rocking his missile. "twenty-seven" → medicine money walks out of the spout, each seal flipping with a sparkle, and a tag on the pipe reads "$27.2 BILLION / YEAR". "trials." → the camera starts to follow the teal pipe down the right side.

Sound: a thunk per tag; a whoosh as the papers go into the hopper; a pop for the bond; a cash-register ding as the hat goes back on; a whistle for the Loud Human's YES; a marker squeak for the signature; a whirr as the valve opens; a whoosh as the tank pours; a tick as the gauge drops a notch; a sparkle as the seals flip.

On screen: tag "1" / "VICTORY BONDS" / "$1 BILLION" (on the hopper) / "1% TREATY: YES" / tag "2" / "1% TREATY" / "MURDER BUDGET" / "$27.2 BILLION / YEAR". Why: steps 1 and 2, with the color flip doing the redirecting, and 1% is a notch the war industry barely notices.

## Scene 10 · pipe-steps-three-four

- id: pipe-steps-three-four
- act: The money loop
- transition_in: same form (no seam)
- key: after "not.": the Rich Human flat on his back like a tipped egg, stub legs up, the check stamped "NOT A TYPO" in his hands, "= 272% a year" chalked between it and his bond stub
- cue: "Three. The Victory Corporation"
- time: 38:36.6 to 39:01.0 (24.4 s)
- voiceover: "Three. The Victory Corporation (the company that issued the bonds) takes a twenty percent management fee on that twenty-seven point two billion dollars. Four. Half of that fee (ten percent) goes to investor dividends: two point seven two billion dollars a year on a one billion dollar investment. That's two hundred and seventy-two percent annual returns. Your investors will think it's a typo. It's not."
- layer: B
- scene: The money loop plate, bottom right, then a ride along the dividend pipe back to the top left. The VICTORY CORPORATION valve house bleeds 20% into the glass box; half of it rides back up to the Rich Human who paid in, as a check he cannot believe.
- wishonia: PiP, skeptical-smile + body-counting, then excited-open + body-excited on "That's", then smirk-smile + body-hands-hips on "not."
- props: money-loop-plate, valve house, glass-box, money("med"), check, bond, richHuman, stamp, stampMark
- status: outline

Moves: "Three." → the first frame is pipe-steps-one-two's last; the camera follows the teal pipe down to the bottom-right view; tag "3". "Corporation" → the valve house's sign lights: "VICTORY CORPORATION". "twenty" (first) → a side valve squeaks open and bleeds a fifth of the bills into the glass box (from bond-splits-three-ways), where they stack in countable rows. "Four." → tag "4". "Half" → the box's outflow splits in two with a clank. "dividends:" → one half shoots off along the dividend pipe, and the camera rides with it left and up the left edge, back to the Rich Human at the counter. after "dividends:" → a check pops out of the spout over his head and he catches it. "billion" (second) → the check fills in: "$2.72 BILLION / YEAR". "investment." → beside him, the stub of his VICTORY bond pops up: "$1 BILLION". "seventy-two" → "= 272% A YEAR" chalks on between them. "typo." → he polishes his monocle and looks again; his eyes spin into dollar signs. "not." → a rubber stamp slams "NOT A TYPO" onto the check. after "not." → he faints flat on his back, stub legs in the air, rocking like a tipped egg, still clutching the check.

Sound: a thunk per tag; a switch for the sign; a valve squeak; a clank for the split; a whoosh for the ride; a pop for the check; a typewriter as it fills in; a pop for the stub; a chalk scratch; a squeak for the monocle and a cash-register ding for the eyes; a rubber-stamp thunk; a thunk as he hits the floor.

On screen: tag "3" / "VICTORY CORPORATION · 20% FEE" / "CAPPED AT 20%" / tag "4" / check "$2.72 BILLION / YEAR" / stub "$1 BILLION" / "= 272% A YEAR" / "NOT A TYPO". Why: steps 3 and 4, and where the 272% comes from.

## Scene 11 · pavlovian-senators

- id: pavlovian-senators
- act: The money loop
- transition_in: same form (no seam)
- key: on "senators.": the three-sticker senator sitting up like a trained dog, tongue out, tie wagging, a YES-shaped dog biscuit in his teeth, the bell still trembling on the Super PAC's desk
- cue: "Five. The other half"
- time: 39:01.0 to 39:20.8 (19.8 s)
- voiceover: "Five. The other half (ten percent) goes to a Super PAC that spends two point seven two billion dollars a year getting treaty-friendly politicians elected and funding cushy post-office careers for the ones who voted yes. The more you voted for the treaty, the more support you get. It's Pavlovian conditioning, but for senators."
- layer: B
- scene: The money loop plate, bottom left. The other half of the glass box runs into the Super PAC, which puts up billboards for the senators who voted yes and opens a door to post-office careers; a bell rings and a senator sits up like a well-trained dog.
- wishonia: PiP, smirk-smile + body-idle, then smirk-ee + body-point-right on "senators."
- props: money-loop-plate, glass-box, super-pac, money("med"), politician (three senators), billboard, door, sign, bell, priceTag
- status: outline

Moves: "Five." → the first frame is pipe-steps-three-four's last; the camera drops to the bottom-left view; tag "5". "Super" → the glass box's other outlet runs into the caped Super PAC, cape flapping. "billion" → its tag fills in: "$2.72 BILLION / YEAR". "elected" → it throws a billboard up behind the first senator: his grin and a "YES" button. "post-office" → the door "POST-OFFICE CAREERS" swings open on a comfy armchair, slippers and a golf bag. "more" (first) → three senators (`KIT.cast("politician")` in three skin tones, ties red, blue, red) stand in a row, and "YES" stickers pop onto them: one, two, three. "get." → each one's billboard grows with his stickers; the three-sticker senator's runs off the top of the frame. "Pavlovian" → the Super PAC rings a desk bell. "senators." → the three-sticker senator sits up straight, tongue out, hands up like paws, his wide tie wagging like a tail; the Super PAC tosses him a dog biscuit shaped like a YES button and he catches it in his teeth; the other two sit up too.

Sound: a thunk for the tag; a whoosh as the stream pours in; a cash-register ding for the PAC's tag; a thunk for the billboard; a door squeak; a pop per sticker; a rising slide whistle as the billboards grow; a bell; a boing as he sits up; two woofs.

On screen: tag "5" / "SUPER PAC · $2.72 BILLION / YEAR" / "POST-OFFICE CAREERS" / "YES" (stickers and billboards). No: no money handed to a senator; the PAC pays for billboards, careers and one biscuit. Why: step 5, and why politicians keep voting yes.

## Scene 12 · greed-loop-runs

- id: greed-loop-runs
- act: The money loop
- transition_in: same form (no seam)
- key: after "existing.": the whole ring in frame, three "GREED" tags lit, medicine money circling, the germs popped, the Reaper at the hospital door with his eraser
- cue: "The remaining eighty percent"
- time: 39:20.8 to 39:45.2 (24.3 s)
- voiceover: "The remaining eighty percent of twenty-seven point two billion dollars goes where it's supposed to: funding clinical trials that keep humans alive. This is the entire trick. You use greed to fund the campaign, greed to pass the treaty, and greed to keep it passed. The money just circulates until diseases stop existing. None of this is overcoming opposition."
- layer: B
- scene: The camera goes to the 80% outlet, where the fat pipe pours into a lab and a hospital and the Reaper loses a customer, then pulls back to the whole money loop plate; greed lights up at three stations, the money circles, and the germs pop.
- wishonia: PiP, happy-smile + body-presenting, then excited-open + body-wide-gesture on "circulates"
- props: money-loop-plate, lab, hospital, scientist, human, reaper, clipboard, germ, sign
- status: outline

Moves: "The" → the first frame is pavlovian-senators' last. "eighty" → the camera pans right to the bottom-right view; the fat pipe out of the valve house's bottom fills. "alive." → it pours into the lab and the hospital; humans walk in with red chest lights blinking and walk out with teal ones. after "alive." → the Grim Reaper waiting at the hospital door, clipboard ready, has to erase a tally mark; he sulks. "entire" → the camera pulls back until the whole ring is in frame. "greed" (first) → the campaign office flashes a "GREED" tag. "greed" (second) → the treaty valve flashes one. "greed" (third) → the Super PAC and the senators flash one. "passed." → the senators sit up again. "circulates" → the money runs round and round the ring, faster. "stop" → the germs clinging to the hospital and the lab pop one by one like balloons. "opposition." → at the plate's edge, a lone placard "OPPOSITION" pokes up, wobbles, and falls flat on its face by itself.

Sound: a whoosh as the pipe fills; a ding as the chest lights turn teal; an eraser scrub for the Reaper; a ding per GREED tag; a woof for the senators; a whirr as the money circles; a pop per germ; a thunk for the placard.

On screen: "80% CLINICAL TRIALS" / three "GREED" tags / "OPPOSITION" (the placard). Why: the loop runs itself, so nobody has to be good.

## Scene 13 · no-opposition

- id: no-opposition
- act: The money loop
- transition_in: slide left
- key: after "finish.": the empty ring, the cuckoo clock over it with the Reaper out, the three humans in the corner doing the sum, the Lobbyist a grinning skeleton in his mask and fedora, pencil still moving
- cue: "There is no opposition."
- time: 39:45.2 to 39:55.7 (10.5 s)
- voiceover: "There is no opposition. There are only humans who haven't done the arithmetic yet, and one hundred and fifty thousand daily funerals that won't wait for them to finish."
- layer: B
- scene: An empty boxing ring labeled "OPPOSITION"; in its corner the three "NOT THE ENEMY" humans from enemy-is-the-clock work through a long sum; the cuckoo clock hangs above them and the Reaper keeps count.
- wishonia: PiP, neutral-closed + body-idle, then sad-closed + body-idle on "funerals"
- props: boxing-ring, bell, lobbyist, politician, weaponsMaker, sign, scroll, pencil, cuckoo-clock, reaper, clipboard, KIT.xray
- status: outline

Moves: "There" → an empty boxing ring with "OPPOSITION" on its apron banner. "opposition." → the ring bell dings; nobody steps in; crickets, and a tumbleweed rolls across the canvas. "humans" → in the ring's corner sit the Lobbyist, the Politician and the Weapons Maker, their "NOT THE ENEMY" signs still on, a long sum unrolled on a scroll in front of them. "arithmetic" → they work it with pencils; the Politician counts on his fingers, the Lobbyist peeks at the Weapons Maker's answer. "hundred" → the cuckoo clock from enemy-is-the-clock drops in on its hook over the ring; the Reaper pops out with his clipboard and keeps popping at the true rate. "funerals" → HOLD 1 to 2 s: only the Reaper's pencil moves. "finish." → the pencils move again; the Reaper pops out once more. after "finish." → the Lobbyist x-rays into a grinning skeleton, fedora and domino mask still on, still working the sum.

Sound: a ring bell; crickets; pencil scratches; a thunk as the clock lands and a boing as the Reaper pops out; silence for the HOLD; a boing as he pops again; an x-ray zap.

On screen: "OPPOSITION" / "NOT THE ENEMY" (three signs) / the clock's plaque "150,000 / DAY". Why: the only thing to beat is the time it takes humans to do the sum.

## Scene 14 · military-industrial-loop

- id: military-industrial-loop
- act: The complexes
- transition_in: slide left
- key: after "corpses.": the red loop closed, its gears turning with nobody touching them, the press in the middle spitting war money and headstones, a fresh headstone just landed on the pile, the smoke trail of the launched chimney
- cue: "If this sounds familiar,"
- time: 39:55.7 to 40:14.7 (19.0 s)
- voiceover: "If this sounds familiar, it should. Eisenhower warned you about the Military Industrial Complex: weapons manufacturers fund politicians, politicians fund weapons contracts, contracts fund contractors, contractors fund politicians. It's a self-sustaining loop that prints money and corpses."
- layer: B
- scene: The red loop (shared drawing) builds station by station (the Weapons Maker, the Politician, the contract, the contractors' factory) around a printing press that prints war money and small grey headstones.
- wishonia: PiP, sideeye-closed + body-arms-crossed
- props: red-loop, weaponsMaker, politician, scroll (the contract), factory, gears, printingPress, money("war"), headstone, sign
- status: outline

Moves: "If" → the empty red ring on the paper, its four stations blank. "familiar," → the Weapons Maker at 9 o'clock waves at the camera like an old friend. "Eisenhower" → a small card pins at the top: "EISENHOWER WARNED YOU". "Complex:" → the loop's title drops on: "MILITARY INDUSTRIAL COMPLEX". "manufacturers" → station 1: the Weapons Maker stuffs war money into the Politician's breast pocket at 12 o'clock. "contracts," (first) → station 2: the Politician signs a contract with a missile drawn on it at 3 o'clock. "contractors," (first) → station 3: the contract flies into the contractors' factory at 6 o'clock, missile chimneys smoking. "politicians." (last) → station 4: war money runs on round the ring past the Weapons Maker (the contractors are him) and back into the Politician's pocket; the ring closes with a clank. "self-sustaining" → the gears turn on their own; the Weapons Maker and the Politician let go and step back, and the ring keeps going. "prints" → the printing press in the middle thumps. "money" → it spits out a war paper. "corpses." → then a small grey headstone, then paper, headstone, faster; a missile chimney on the factory launches, arcs off the top of the frame, a boom off screen, and a fresh headstone thunks onto the pile.

Sound: a pop for the card; a thunk for the title; a cash-register ding for the pocket; a pen scratch for the signature; a whoosh as the contract flies; a clank as the ring closes; a whirr for the gears; a press thump; a cash-register ding for the paper; a thunk per headstone; a whistle as the chimney launches; a boom; a thunk.

On screen: "EISENHOWER WARNED YOU" / "MILITARY INDUSTRIAL COMPLEX" / station labels "WEAPONS MAKERS · POLITICIANS · CONTRACTS · CONTRACTORS". No: no portrait of Eisenhower, no real weapons models or company marks. Why: the machine that already works, shown as a loop.

## Scene 15 · patient-industrial-loop

- id: patient-industrial-loop
- act: The complexes
- transition_in: same form (no seam)
- key: after "them).": both loops turning in step, both "GREED" tags lit, the red press still spitting headstones onto its mountain, the teal press stopped beside a short row of headstones for diseases
- cue: "You're building the same"
- time: 40:14.7 to 40:38.4 (23.7 s)
- voiceover: "You're building the same machine, but pointed at diseases instead of countries. Call it the Patient Industrial Complex. Investors fund politicians, politicians fund clinical trials, trials generate returns, returns fund investors, investors fund politicians. Same loop. Same greed. Same self-sustaining mechanics. Different corpses (fewer of them)."
- layer: B
- scene: A mirror-image teal loop builds beside the red one with the same gears (investors, politicians, clinical trials, returns) around a teal printing press; its headstones are for diseases, and there are few of them.
- wishonia: PiP, happy-smile + body-presenting, then smirk-smile + body-hands-hips on "fewer"
- props: red-loop, teal loop, richHuman, super-pac, billboard, politician, scroll (the contract), lab, scientist, gears, printingPress, money("med"), headstone, diseaseBlob, earthGlobe, sign
- status: outline

Moves: "You're" → the first frame is military-industrial-loop's last. "machine," → the red loop shrinks and slides to the left half (the top half in 9:16), still turning, and an empty mirror copy of its ring appears on the right, in teal. "diseases" → each ring has a big pointer arrow on top like a weathervane; the red one points at a small Earth (`KIT.props.earthGlobe`, sign "COUNTRIES"), and the teal one swings round to a disease blob. "countries." → the blob gulps. "Complex." → the teal title drops on: "PATIENT INDUSTRIAL COMPLEX". "politicians," (first) → station 1: the Rich Human's medicine money hops into the Super PAC, which throws up a billboard behind the Politician. "trials," (first) → station 2: the Politician signs a contract with a pill drawn on it, and it flies to the lab. "returns," (first) → station 3: the lab chimney puffs out medicine money. "investors," (second) → station 4: the money runs into the Rich Human's top hat; the ring closes. "loop." → both rings' gears turn in step. "greed." → a "GREED" tag lights on both. "Different" → the red press keeps spitting headstones onto its mountain. "corpses" → the teal press spits out a headstone that reads "CANCER", then a smaller one for a germ. "fewer" → it coughs out one last tiny one and stops; its row is short next to the red mountain. after "them)." → the teal press sputters and sits still.

Sound: a whoosh as the red loop slides over; a squeak as the pointer swings; a gulp (a small yelp) from the blob; a thunk for the title; a pop as the money hops into the PAC; a pen scratch for the contract; a sparkle for the chimney's money; a cash-register ding for the hat; a whirr for the gears; a ding for GREED; a thunk per headstone; a small pop for the last one; a sputter.

On screen: "PATIENT INDUSTRIAL COMPLEX" / station labels "INVESTORS · POLITICIANS · CLINICAL TRIALS · RETURNS" / "COUNTRIES" / "GREED" (twice) / the headstones "CANCER" and a germ's / under the teal row: "CORPSES: FEWER". No: no money handed to the Politician in the teal loop; it goes through the Super PAC. Why: the same greed, pointed at diseases instead of countries, and the diseases are what die.

## Scene 16 · evolved-on-purpose

- id: evolved-on-purpose
- act: The complexes
- transition_in: same form (no seam)
- key: after "orphans.": the red loop overgrown with wild vines, the teal loop standing straight in its flower pot, both tags hung, YOU snipping the red vine that crept toward the pot
- cue: "The Military Industrial Complex wasn't"
- time: 40:38.4 to 40:53.0 (14.6 s)
- voiceover: "The Military Industrial Complex wasn't designed. It evolved, because the incentives aligned. An Incentive Alignment Bond just aligns them on purpose, toward something that doesn't require orphans."
- layer: B
- scene: The red loop grows by itself like a weed, sprouting new stations; the teal loop turns out to be planted in a neat flower pot, and YOU kneels beside it with a trowel.
- wishonia: PiP, thinking-closed + body-thinking, then smirk-closed + body-arms-crossed on "orphans."
- props: red-loop, teal loop, vines, drawer, moth, flower pot, YOU, trowel, garden shears, sign
- status: outline

Moves: "The" → the first frame is patient-industrial-loop's last. "designed." → a drawer under the red loop slides open: no blueprint inside, and the moth from Part 1's empty wallet flies out. "evolved," → the red loop sprouts wild vines, with new little stations budding on them, crawling over its headstone mountain. "aligned." → the vines snap into line behind its arrows. "purpose," → under the teal loop the ground turns out to be a neat flower pot labeled "INCENTIVE ALIGNMENT BOND", with a garden stake; YOU kneels beside it and pats the soil with a trowel. "orphans." → a tag pops onto the red loop: "REQUIRES ORPHANS"; then one onto the teal loop: "DOESN'T". after "orphans." → a red vine creeps over toward the pot, and YOU snips it off with garden shears. The part ends on that frame.

Sound: a drawer squeak; a rising slide whistle as the vines grow; a click as they snap into line; soft pats on the soil; a pop per tag; a snip.

On screen: "EVOLVED" (red) / "ON PURPOSE" (teal) / the pot "INCENTIVE ALIGNMENT BOND" / tags "REQUIRES ORPHANS" · "DOESN'T". Why: the bond builds on purpose what war built by accident, and the reader is the one who plants it.
