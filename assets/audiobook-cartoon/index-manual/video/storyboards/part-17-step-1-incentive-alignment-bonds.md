---
format: 1920x1080
duration: 5:09.5
message: "Step 1 sells $1 billion of bonds whose treaty money would pay investors 272% a year, reward the politicians who vote yes, and send 80% to clinical trials, so greed keeps the treaty alive."
arc: Title card, the emblem's papers jam the atom → Wishonia fishes a sleeping human out of a hammock with a paper → a disease is the only protester against cures, the Reaper keeps count and the snail with the sum rockets off after a paper → she slaps the bond on her lectern → a traffic cop splits the treaty money 80/10/10 and the glass lid traps the Lobbyist's fingers → the fat cat bounces off the velvet rope and the Optimitron burns the useless policy like toast → she sets her mug down slowly → Grandma's war bond, then Grandma's skeleton → YOU sells the fat cat a 272% bond and he puts on a lobbyist's mask → nobody in the machine is the enemy, the Reaper pops out of the cuckoo clock → the reader nods off beside the lectern → the money loop road, stop by stop: the feather bond, the 1% shrug, NOT A TYPO and the fat cat faints → she rolls her eyes → the senator who sits up like a dog, the money goes round and the germs pop → an empty ring while the humans do the sum → she raises an eyebrow → Part 2's loop road prints money and walking headstones → the same loop pointed at diseases prints three little headstones → YOU snips the war vine beside the lectern
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 17, "The Five-Step Plan, Step 1: Sell Incentive Alignment Bonds"
audio: index-manual.cbaf659d.mp3, 35:43.4 to 40:53.0
version: v3
---

# Part 17 storyboard: "The Five-Step Plan, Step 1: Sell Incentive Alignment Bonds"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The film look of Part 2 (`../compositions/scenes/part-02/`): Layer A is the host at her lectern (`KIT.studio`), Layer B is an illustrated plate the camera travels over (`KIT.camera`), one framing per phrase, and the period film runs over every shot. Wishonia is on screen only at her lectern; in the plates she is the voice. Money is green: plain papers are what the Rich Human pays with, war money (missile seal) goes into the color-flip funnel, and everything that comes out of it is medicine money (cross seal), the 10% shares included.

**Spine.** Roads. The treaty money walks, as Part 2's papers did. bond-splits-three-ways is one fork in a road: a traffic cop waves eight bills of every ten down the wide road to the lab and one down each narrow lane, to the Rich Human and to the Super PAC, and the narrow lanes run under glass. The money loop plate is a looping road like Part 2's, built stop by stop from YOU's VICTORY BONDS booth round to the hospital (loop-steps-one-two to greed-loop-runs), and greed-loop-runs pulls back until the road is a loop and holds on the money going round it. military-industrial-loop then cuts to Part 2's own loop road ("If this sounds familiar, it should"), and patient-industrial-loop pulls back to show the money loop standing beside it, the same shape.

**Running gag: the Grim Reaper's tally** (from Part 5), 150,000 a day. He writes so fast his pencil smokes at his curbside desk (the-arithmetic), pops out of a cuckoo clock at the true rate (one mark every 0.58 s: 86,400 seconds a day / 150,000) in enemy-is-the-clock and no-opposition, and has to erase a mark at the hospital door in greed-loop-runs.

**The cast.** YOU, the reader, is the busy human in the bowler from Part 1's title card, as in Parts 10 and 12 (`{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene): he runs the VICTORY BONDS booth, sits in the glass toll booth on the money loop, and plants the teal plant beside the lectern. The Rich Human is the fat cat (`KIT.cast("richHuman")`) with Part 5's "I PREFER LIVING" button; from "lobbyists" in what-youre-offering to the end of the part he also wears the Lobbyist's domino mask (`mask: true`), but never his briefcase (the funnel-topped briefcase is the Lobbyist's, in Parts 5 and 19). The Politician and the three senators are `KIT.cast("politician")` (the senators in three skin tones). The Lobbyist, the Weapons Maker, the Scientist, Grandma and the Loud Human are their `KIT.cast` selves. Everyone else is an everyday human whose body comes from the outfit.

**Shared drawings** (several author groups draw these, so they must match; the group named draws it first as a function the others copy):
- **The bond.** `KIT.props.bond({ text: "INCENTIVE ALIGNMENT BOND" })`; the VICTORY bonds are `KIT.props.bond({ text: "VICTORY BOND", seal: "med" })`.
- **The glass case.** Pale glass (#DCEFF0 at 0.55 opacity) with a navy outline and two white diagonal glints, a navy-rimmed lid with a small brass handle and a cream plate on it, "CAPPED AT 20%"; the bills inside stand in neat rows you could count. A long, low case over two lanes in bond-splits-three-ways; on the money loop the same case stood on end is the toll booth (the glass toll booth, see loop-steps-one-two). Drawn first by the-fork group.
- **The money loop plate** (described at loop-steps-one-two). Drawn first by the loop-steps group (loop-steps-one-two, loop-steps-three-four); pavlovian-senators, greed-loop-runs and patient-industrial-loop copy it.
- **Her mug.** A cream diner mug with a rust band on the lectern's reading top, drawn in the scene (`KIT.mug` is Part 1's office): heres-one draws it first, and the three reaction cuts (slow-sip, count-five, sounds-familiar) copy it.
- **The Super PAC.** Part 5's caped backpack as Part 5 v3 draws it (`part-05-sacred-order-of-paper-distribution.md`, step-4-super-pac, and the-rally in its sketch module): a rust canvas backpack with navy straps for arms, a cream "SUPER PAC" patch on its front pocket and a war-red cape. Copy the new `../compositions/scenes/part-05/step-4-super-pac.html` once it is redrawn in that look; the file there now is the old look (navy pack, domino mask, mustard cape), so do not copy it.
- **The VICTORY BONDS booth.** A little striped kiosk (cream and rust stripes) with a counter, a bond slot in the counter's front, bunting and a sign "VICTORY BONDS"; Grandma's booth beside it is the same kiosk with the sign "WAR BONDS". Drawn first by the bond-booths group; the money loop's first stop is the same booth.
- **The cuckoo clock.** A carved 1950s cuckoo clock about the size of a person's torso: a tan house with a rust pointed roof and navy trim, a cream face, a little door above the face, two pine-cone weights on chains, and a cream plaque under the face, "150,000 / DAY". The Reaper (`KIT.reaper()` small, his tally clipboard) pops out of the door on a zigzag spring, adds a mark and snaps back. the-machine plate only.
- **The snail** from Part 3's title card: copy `snail(C, pid, o)` from Part 3's sketch module (`part-03-*.sketch.mjs`), which copied it from the old title card.
- **The reader** from Part 8: `READER = { tone: 1, outfit: "shirt", color: 1, hair: 0, glasses: true, seed: 8 }` (exported by Part 8's sketch module), his orange wingback armchair, floor lamp and the manual with its red ticket bookmark, as Part 8's sketch module and `../compositions/scenes/part-08/falling-apart.html` draw them.
- **Part 2's loop road** (military-industrial-loop): the drawing code of `../compositions/scenes/part-02/money-loop.html`.

**Callbacks.** From Part 13 (human-greed): the bond certificate lands on Wishonia's lectern in heres-one. From Part 14: the Optimitron (`KIT.props.optimitron`, its defaults) in wishocratic-allocation. From Part 5: the Super PAC, the "I PREFER LIVING" button, the Reaper and his tally. From Part 3: the snail, now carrying the arithmetic. From Part 8 (falling-apart): the reader in his armchair, beside the lectern in stop-reading. From Part 15: the podium name card "EISENHOWER" and the factory with missile chimneys. From Part 2: the whole loop road, its press, its factory and its house, in military-industrial-loop. Inside the part: Wishonia's fishing line (financial-instrument) drops the paper in front of the snail; the VICTORY BONDS booth of what-youre-offering is the money loop's first stop; the senators sit up like dogs again in greed-loop-runs; the NOT THE ENEMY humans of enemy-is-the-clock do the sum in no-opposition.

**Set up here.** The little NOT THE ENEMY sign on a stick over the Weapons Maker (Part 20). The bell that trains the senators (Part 20). The Super PAC's "$2.72 BILLION / YEAR" tag and the glass case of the capped 20% (Part 20). Grandma's skeleton with her BUY BONDS poster and her "1987" headstone: from here on she is only a skeleton (Part 21, at the back of the living voters' line; Part 27). The "I PREFER LIVING" button (Part 21). The "1% TREATY: YES" campaign sign (Part 23). The Optimitron's burnt toast card (Part 22).

**Held frames.** the-arithmetic, after "day" (about 1 s). grandmas-war-bond, after "eighty-seven." (1 to 2 s). no-opposition, after "funerals" until "finish." (1 to 2 s): only the Reaper's pencil moves (it is the count, not a gag). A HOLD is silent.

**Transitions.** The title card comes up from black and goes down to black; financial-instrument irises in on Wishonia's face. Cuts between host shots and plates; the three reaction cuts (slow-sip, count-five, sounds-familiar) cut in and out. what-youre-offering continues grandmas-war-bond's plate, loop-steps-three-four continues loop-steps-one-two, greed-loop-runs continues pavlovian-senators, and patient-industrial-loop continues military-industrial-loop, each with no seam (it starts on the last scene's final frame). pavlovian-senators cuts back from count-five to the money loop on loop-steps-three-four's final frame. no-opposition cuts back to the-machine plate of enemy-is-the-clock. evolved-on-purpose irises out on her face to black, so Part 18's title card comes up from black.

**Bans for this part.**
- The money loop's stops go unlettered (the tank, the toll booth, the campaign office, the hospital), and it has no step numbers: the narrator counts and the camera arrives.
- In the new system no bill goes into a politician's hand or pocket: the Super PAC pays for billboards, water cups, careers and one biscuit. In Part 2's loop (the old system) the Weapons Maker does stuff the Politician's pocket.

## Changes from v2

- The office, the wall screen and Wishonia's corner are gone. She is on screen in four host shots: she fishes a sleeping human out of a hammock with a paper on a rod (financial-instrument), slaps the bond on her lectern (heres-one), wakes the reader beside her lectern with her fist (stop-reading), and ends the part beside YOU's potted plant (evolved-on-purpose). Three reaction cuts of about a second break up the two long plate runs: she sets her mug down after the burnt card (slow-sip), rolls her eyes after the Rich Human faints (count-five) and raises an eyebrow after the Lobbyist's skeleton (sounds-familiar). Everything else happens on seven plates.
- financial-instrument's wall-screen gags became the-arithmetic, a street plate: a disease blob is the only protester at the AGAINST CURING DISEASES stand and signs its own petition, the Reaper keeps his tally at a curbside desk, and money compresses the timeline by dangling a paper in front of the snail, which rockets off (instead of an accordion ribbon).
- Pipes and arrow rings became roads. The split is a fork with a traffic cop; the money loop is a looping road like Part 2's, with a glass toll booth (YOU inside) keeping the 20% in plain view and a bill running the dividends straight across the infield to the Rich Human; military-industrial-loop is Part 2's own loop road, and patient-industrial-loop pulls back to the money loop beside it.
- The labels went: no number discs, no 80% / 10% / GREED tags, no THE BRIBERY MACHINE sign, no CORPSES: FEWER or REQUIRES ORPHANS tags, and no signs that only name a stop on the money loop (no MURDER BUDGET on the tank, VICTORY CORPORATION on the toll booth, campaign awning or HOSPITAL lettering); its pull-back holds on the money going round, not on the stops. grandmas-war-bond and what-youre-offering are two bond booths side by side instead of two ticked lists: a little 4% tag on Grandma's poster, a 272% tag on YOU's bond big enough to swing the Rich Human round.
- The title card is the period card. The five numbered doors are gone (a five-line heading leaves no room under it); the emblem gets obscenely wealthy instead, its orbits jamming with papers.
- The Rich Human puts on the Lobbyist's mask but not his briefcase: the funnel-topped briefcase stays the Lobbyist's (Parts 5 and 19).
- no-opposition's empty ring stands beside the bribery machine and its cuckoo clock on one plate; the red loop's wild vines and YOU's flower pot moved into the ending host shot, where YOU snips the vine without looking.

## Scene 1 · title-card

- id: title-card
- act: Title
- transition_in: up from black (the parts are rendered on their own and joined)
- key: after "Bonds.": the whole heading on the navy card under the emblem, the STEP 1 stamp tilted on it, the three papers back on their orbits and a heap of spilled papers at the foot of the card
- cue: "The Five-Step Plan."
- time: 35:43.4 to 35:53.3 (9.8 s)
- voiceover: "The Five-Step Plan. *Saving Humanity While Making Everyone Obscenely Wealthy* Step One: Sell Incentive Alignment Bonds."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem (three cream orbits round an orange nucleus, a war-seal paper running round each) and the heading under it. Heading lines, 16:9: "THE FIVE-STEP PLAN" (small) / "Saving Humanity While Making Everyone Obscenely Wealthy" (italic) / "STEP 1" (stamp) / "SELL INCENTIVE" / "ALIGNMENT BONDS". 9:16: "THE FIVE-STEP PLAN" (small) / "Saving Humanity While Making" (italic) / "Everyone Obscenely Wealthy" (italic) / "STEP 1" (stamp) / "SELL" / "INCENTIVE" / "ALIGNMENT" / "BONDS". Five lines under the emblem is a lot: pass the layout overrides (cy, maxH, minTop) so the big lines stay big. The small gag is the emblem getting obscenely wealthy.
- props: title-card, money (war)
- status: planned

Moves: "The" → the card comes up from black with "THE FIVE-STEP PLAN" on it, the emblem's three papers running round their orbits; the camera pushes in slowly for the whole shot. "Saving" → the italic line fades in, word by word as it is read. "Obscenely" → more papers run onto the orbits, nose to tail: six, twelve, twenty. "Wealthy" → the orbits are jammed solid with papers and the nucleus is squeezed out of round. after "Wealthy" → the jam spills: papers tumble off the orbits, drop behind the heading and land in a heap at the foot of the card, and the three runners carry on as before. "One:" → "STEP 1" stamps onto the card with a shake. "Sell" → "SELL INCENTIVE ALIGNMENT BONDS" fades in word by word as it is read. after "Bonds." → the card goes down to black in its last quarter second.

Sound: the projector whirr from "The"; a slide whistle down as the papers spill after "Wealthy"; a stamp thump on "One:".

On screen: "THE FIVE-STEP PLAN" / "Saving Humanity While Making Everyone Obscenely Wealthy" / "STEP 1" / "SELL INCENTIVE ALIGNMENT BONDS".

Why: the narrator reads the heading, its italic line and the step, and the money on the emblem gets obscenely wealthy before the plan explains how.

## Scene 2 · financial-instrument

- id: financial-instrument
- act: Why bonds
- transition_in: iris in on her face
- key: on "instrument.": Wishonia at the lectern reeling in, a plain paper on the hook skipping toward her, and the human from the hammock lunging after it with his arms out, the hammock flipped upside down behind him
- cue: "On my planet, people"
- time: 35:53.3 to 35:59.4 (6.1 s)
- voiceover: "On my planet, people do useful things because they're useful. On Earth, you need a financial instrument."
- layer: A, host
- scene: The host's set (`KIT.studio`). On the free wall right of the lectern, an everyday human in a shirt asleep in a canvas hammock strung between two posts. A fishing rod stands in a holder clamped to the lectern's side, leaning out over the hammock (no hand has to hold it; its reel turns by itself).
- wishonia: big, happy-smile + body-presenting; smirk-smile + body-point-right on "Earth,"; smirk-ee + body-open-palms on "instrument."
- props: studio, lectern, person (everyday, shirt), hammock, fishing rod, money (plain)
- status: planned

Moves: "On" → the iris opens on her face; she presents, cheerfully; the camera pushes in slowly for the whole shot. "useful" (first) → beside her, the human in the hammock snores, one arm hanging out, the hammock rocking. "Earth," → she points at him. "financial" → the rod dips and casts: a plain paper on the hook swings out over the hammock and stops right in front of his nose. "instrument." → his eyes snap open; he springs out of the hammock, which flips upside down, and lunges for the paper as the reel winds it in toward the lectern, just out of his reach; he runs after it, arms out, until the cut.

Sound: a whoosh as the line casts on "financial"; a boing as he springs up on "instrument.".

On screen: nothing but the set and the guest.

No: she does not hold the rod.

Why: on Earth a human gets out of the hammock for a paper, so she fishes for one.

## Scene 3 · the-arithmetic

- id: the-arithmetic
- act: Why bonds
- transition_in: cut
- key: after "timeline.": the snail rocketing along the gutter after the dangling paper, a smoke trail behind it and its sum flapping, the Reaper at his curbside desk spun round in its wind, the pages of his clipboard flying
- cue: "Not because anyone rationally"
- time: 35:59.4 to 36:15.6 (16.2 s)
- voiceover: "Not because anyone rationally opposes curing diseases (they don't; see above), but because one hundred and fifty thousand people die per day while the arithmetic propagates, and money is how you compress the timeline."
- layer: B, plate main-street
- scene: One plate: a 1950s sidewalk and a strip of street on a plain tan field, the curb and gutter running along the bottom. On the left a little card table with a petition on a clipboard and a picket sign (`KIT.props.sign`, one pole) "AGAINST CURING DISEASES"; behind it, the only protester, a smug disease blob (`KIT.props.diseaseBlob`). In the middle, at the curb, a school desk and chair where the Grim Reaper sits writing on his tally clipboard. In the gutter in front of him, the snail with a long sum strapped to its shell. A couple of everyday humans walk the sidewalk.
- props: diseaseBlob, sign, card table, clipboard (the petition), person (everyday), reaper, clipboard (the tally), school desk, snail, scroll (the sum), money (plain), fishing line
- status: planned

Moves: "Not" → framing on the protest table: the sign "AGAINST CURING DISEASES", an empty petition, and behind them, alone, the smug disease blob. "rationally" → two everyday humans walk past the table without a glance. "opposes" → the blob waves the picket sign at their backs. "(they" → they keep walking. "above)," → the blob signs its own petition, the only name on it, and glares after them. "hundred" → the camera travels right along the curb to the Grim Reaper at his school desk, writing tally marks so fast his pencil smokes. "die" → the camera pushes in on his clipboard: "150,000 / DAY" at its head over rows of tally marks in fives; a page flips over, and another. "day" → HOLD about 1 s: nothing moves. "arithmetic" → the camera drops to the gutter: the snail inches along with a long sum unrolled on its shell, its slime trail barely longer than it is. "money" → a plain paper on a fishing line drops in from above the frame and dangles in front of its eye stalks (Wishonia's line, from financial-instrument). "compress" → both eye stalks swing round to the paper. "timeline." → the snail rockets off along the gutter after it, the sum flapping, a smoke trail behind. after "timeline." → it shoots past the Reaper's desk, and its wind spins him round on his chair and blows the pages off his clipboard.

Sound: a squeak as the blob signs on "above),"; a pencil scratch from "hundred"; silence for the HOLD; a whoosh as the snail rockets off on "timeline.".

On screen: "AGAINST CURING DISEASES" / "150,000 / DAY".

No: the sum on the shell is digits and squiggles, not words; no number in the sky (the clipboard carries it).

Why: nobody human opposes cures; people die while the sum crawls, and money makes even arithmetic hurry.

## Scene 4 · heres-one

- id: heres-one
- act: Why bonds
- transition_in: cut
- key: on "one.": the bond certificate standing on the lectern's reading top under Wishonia's palms, her coffee mug in the air above the lectern, the gold seal glinting
- cue: "So here's one."
- time: 36:15.6 to 36:16.9 (1.3 s)
- voiceover: "So here's one."
- layer: A, host
- scene: The host's set, her coffee mug on the lectern's reading top (drawn in the scene). The bond certificate (`KIT.props.bond({ text: "INCENTIVE ALIGNMENT BOND" })`), the one from human-greed (Part 13).
- wishonia: big, smirk-smile + body-palms-down
- props: studio, lectern, mug, bond
- status: planned

Moves: "So" → back at the lectern; "here's" → she slaps the bond certificate down on the reading top, facing the camera, and the mug jumps. "one." → the mug lands, and the gold seal glints.

Sound: a slam on "here's"; a sparkle on "one.".

On screen: "INCENTIVE ALIGNMENT BOND".

No: no push or iris; it is a one-second cut.

Why: the device the last line asked for, delivered like a sales slip.

## Scene 5 · bond-splits-three-ways

- id: bond-splits-three-ways
- act: The split
- transition_in: cut
- key: after "transparent.": the long glass case shut over the two narrow lanes, a bill walking in each, the Lobbyist's masked face pressed to the glass and fogging it, his gloved fingers flat under the lid
- cue: "An Incentive Alignment Bond funds"
- time: 36:16.9 to 36:51.4 (34.5 s)
- voiceover: "An Incentive Alignment Bond funds a policy campaign, then splits the resulting government savings three ways: eighty percent to clinical trials, ten percent to investors as a revenue share on treaty funds, and ten percent to a Super PAC that rewards politicians who voted yes (campaign support while they're running, cushy post-office careers when they're done). Investors give money, get more money back. Politicians get reelected. Eighty percent goes to curing diseases. The corruption is capped at twenty percent and fully transparent."
- layer: B, plate the-fork
- scene: One plate on a plain tan field, drawn in Part 2's road colors. A cream road comes in from the left past a spot for the campaign sign, runs under the color-flip funnel (`KIT.props.colorFlipFunnel`), and reaches a fork where a traffic cop (an everyday human in a policeman's cap, white gloves, a whistle) stands on a little round stand. From the fork the wide road runs on to a lab shed (`KIT.props.lab` under a little roof, the Scientist in its doorway); two narrow lanes peel off through the long glass case (lid propped open) to the Rich Human, and further on to the Super PAC beside the Politician, an empty billboard frame on two posts behind him and a door "POST-OFFICE CAREERS" (`KIT.props.door`). The Lobbyist lurks behind the glass case.
- props: bond, sign, colorFlipFunnel, money (war, med), person (the traffic cop), lab, scientist, richHuman, super-pac, politician, billboard, door, sash, germ, glass-case, lobbyist
- status: planned

Moves: "Bond" → the bond certificate from heres-one drops onto the road from above the frame. "funds" → it sprouts stick legs and walks right. "campaign," → a campaign sign springs up beside it, "1% TREATY: YES", and the bond dips a corner to it in passing. "government" → the camera travels on to the color-flip funnel: war money drops into it. "savings" → medicine money walks out of its spout onto the road, each seal flipped. "three" → at the fork the traffic cop blows his whistle. "ways:" → he waves the bills on: eight of every ten down the wide road, one into each narrow lane. "eighty" → the camera follows the crowd down the wide road to the lab shed, where the Scientist catches them in her arms. "investors" (first) → the camera travels back to the fork and along the first narrow lane to the Rich Human, who holds out his top hat upside down; one bill hops in. "Super" → along the other lane, the caped Super PAC swoops in and lands in its hero pose; one bill hops into it. "voted" → it throws a billboard up into the frame behind the Politician: his grin and a YES button. "running," → he jogs on the spot and the Super PAC runs beside him, handing him paper cups of water like at a marathon. "post-office" → the door behind him swings open on a comfy armchair and a golf bag. "Investors" → the camera pulls back to the whole fork, both lanes and their ends. "back." → the Rich Human's hat overflows and his monocle pops out. "reelected." → three "RE-ELECTED" sashes drop onto the Politician, one after another. "diseases." → the Scientist boots a germ out of the lab shed; it lands flat on its back, dead, tongue out. Meanwhile the Lobbyist tiptoes out from behind the glass case toward the narrow lanes, fingers reaching. "capped" → the glass lid slams down over both lanes, right on his gloved fingers; he yelps. "transparent." → the glass gleams; every bill inside can be counted. after "transparent." → the camera pushes in on him: he presses his masked face to the glass and fogs a patch of it, his fingers still flat under the lid.

Sound: a thunk as the bond lands; a pop for the campaign sign; a sparkle as the seals flip; a whistle for the cop; a cash-register ding as the bill hops into the hat; a whoosh as the Super PAC swoops in; a thunk for the billboard; a door squeak; a pop for the monocle; three thunks for the sashes; a splat for the germ; a slam and a yelp for the lid; a squeak as his face presses on the glass.

On screen: "1% TREATY: YES" / the billboard's "YES" / "POST-OFFICE CAREERS" / "RE-ELECTED" / the lid plate "CAPPED AT 20%".

No: no 80% / 10% labels (the road's width says it); no bill into the Politician's hand (the Super PAC pays for the billboard, the water and the door).

Why: the whole bond at one fork: most of it to the lab, a little to whoever keeps the treaty alive, and the little part is under glass where the crooks can see it and not touch it.

## Scene 6 · wishocratic-allocation

- id: wishocratic-allocation
- act: The split
- transition_in: cut
- key: after "nothing.": the Politician on the government steps blowing on a burnt, smoking card and sliding it into his pocket, the Optimitron beside him, the velvet rope still shut on the left of the frame
- cue: "The other eighty percent"
- time: 36:51.4 to 37:08.5 (17.1 s)
- voiceover: "The other eighty percent goes directly to clinical trials through wishocratic allocation, where nobody with money gets to decide where it goes. Meanwhile, the Optimitron tells governments which of their own policies are working and which ones are expensive ways to accomplish nothing."
- layer: B, plate the-allocation
- scene: One plate: the wide road from the-fork comes in from the left to a low stage with three plain ballot boxes (`KIT.props.ballotBox`) on it, and behind each box a disease blob of a different color waiting like a contestant. A line of everyday humans in front of the stage. A velvet rope on two brass posts across the stage's steps, a little card hanging from it. To the right, on the steps of a government building (`KIT.props.capitol`, small, no label), the Optimitron on a little table and the Politician beside it.
- props: money (med), ballotBox, diseaseBlob, person (everyday), velvet rope, sign, richHuman, capitol, optimitron, politician
- status: planned

Moves: "eighty" → the medicine money walks in from the left along the wide road to the stage. "wishocratic" → each human in the line takes one bill off the road. "allocation," → one after another they drop their bills into the box of their choice, tick, tick, tick; the boxes fill unevenly, and the blob behind the fullest one starts to sweat. "nobody" → the Rich Human waddles up to the steps waving his fat stack of cash. "money" → the velvet rope clips shut across his belly; its card reads "NO MONEY PAST THIS ROPE". "decide" → he tries to step over it; his stub legs are too short, and he bounces off it belly first. "goes." → he tips over and rolls away like an egg, out of the frame. "Optimitron" → the camera travels right to the government steps: the Optimitron on its table, the Politician at it with his hands out. "working" → a card pops out of its toaster slot: "WORKING"; he beams and holds it up to the camera. "expensive" → a second card pops, burnt black and smoking like overdone toast: "EXPENSIVE WAY TO ACCOMPLISH NOTHING". "nothing." → he blows on it. after "nothing." → he quietly slides it into his pocket and smiles at the camera, until the cut.

Sound: three ticks as the bills go in; a click for the rope; a boing as he bounces; a falling slide whistle as he rolls away; a toaster pop per card; a sizzle for the burnt one.

On screen: "NO MONEY PAST THIS ROPE" / "WORKING" / "EXPENSIVE WAY TO ACCOMPLISH NOTHING".

No: no disease names on the boxes (the blobs behind them say it).

Why: everyone gets a say in the 80%, money cannot buy one, and governments pocket their bad news.

## Scene 7 · slow-sip

- id: slow-sip
- act: The split
- transition_in: cut
- key: after "grandparents": Wishonia at the lectern, her eyes on the camera, her mug just set down on the reading top with a curl of steam over it
- cue: "Remember when your grandparents"
- time: 37:08.5 to 37:09.9 (1.4 s)
- voiceover: "Remember when your grandparents"
- layer: A, host (reaction cut)
- scene: The host's set, her mug (see Shared drawings) at her lips. Nothing else.
- wishonia: big, sideeye-closed + body-idle
- props: studio, lectern, mug
- status: planned

Moves: "Remember" → cut to Wishonia at the lectern, mid-sip; her eyes slide to the camera over the rim. "grandparents" → she sets the mug down slowly on the reading top.

Sound: a soft thunk as the mug touches down.

On screen: nothing but the set.

No: no push or iris; it is a one-second cut.

Why: a beat for the government pocketing its bad news, and a breath in a 52-second run of plates.

## Scene 8 · grandmas-war-bond

- id: grandmas-war-bond
- act: What Grandma got
- transition_in: cut
- key: after "eighty-seven.": Grandma a grinning skeleton in curlers, cat-eye glasses and apron in front of her WAR BONDS booth, her BUY BONDS poster still up with its drooping 4% tag, a small headstone "1987" in front of her
- cue: "funded World War Two"
- time: 37:09.9 to 37:31.7 (21.8 s)
- voiceover: "funded World War Two by buying bonds? They got four percent returns and a world without Nazis (mostly). You're proposing the same thing. What Grandma Got. Dead Nazis (admittedly good). Four percent returns (barely beat inflation). Still died of cancer in nineteen eighty-seven."
- layer: B, plate bond-booths
- scene: One plate: a sidewalk with two bond booths side by side, like a 1940s fair: on the left Grandma's booth, "WAR BONDS"; on the right YOU's, "VICTORY BONDS" (see Shared drawings), YOU behind its counter. Grandma (`KIT.cast("grandma")`) comes to her booth with her poster.
- props: booth (two), grandma, priceTag, coin, medal, YOU, bond, headstone, xray
- status: planned

Moves: "funded" → framing on the WAR BONDS booth: Grandma hobbles up to it with her poster. "bonds?" → she waves it overhead: "BUY BONDS". "four" → a small price tag drops onto the poster on its string: "4%". "(mostly)." → she shrugs. "thing." → the camera pulls back to both booths: next door, YOU holds up an Incentive Alignment Bond over his counter, and Grandma looks over at him. "Grandma" → the camera pushes back in on her. "good)." → she gives a firm nod, and a little medal pops onto her apron. "Four" → her booth's slot pays out: one coin rolls into her hand. "inflation)." → she holds it up to the light; the 4% tag droops on its string. "cancer" → her chest light blinks red. "nineteen" → she x-rays into a grinning skeleton, curlers, glasses and apron still on, poster still up. "eighty-seven." → a small headstone rises in front of her: "1987". Then HOLD 1 to 2 s; the skeleton keeps smiling.

Sound: soft pats as she hobbles in; a whoosh as the poster waves; a pop for the tag; a ding for the coin; a falling slide whistle as the tag droops; an x-ray zap on "nineteen"; a thunk as the headstone rises; then silence for the HOLD.

On screen: "WAR BONDS" / "VICTORY BONDS" / "BUY BONDS" / "4%" / the headstone "1987".

No: no list of what Grandma got (the narrator reads it; the booth shows it).

Why: humans already loved buying bonds; the one thing Grandma's bond could not buy was a cure.

## Scene 9 · what-youre-offering

- id: what-youre-offering
- act: What Grandma got
- transition_in: same plate (no seam)
- key: after "bonus).": both booths in frame: skeleton Grandma nodding at YOU, and at YOU's counter the Rich Human in a domino mask, tipped forward by an I PREFER LIVING button the size of a hubcap, the huge 272% tag on his bond, the dead CANCER blob flat on the sidewalk
- cue: "What You're Offering. Dead"
- time: 37:31.7 to 38:00.7 (29.0 s)
- voiceover: "What You're Offering. Dead diseases (objectively better than dead Nazis because diseases kill more people). Two hundred and seventy-two percent annual returns (a revenue share on ten percent of treaty funds; if the treaty grows, so do their returns, which turns investors into the world's most motivated lobbyists for expanding it). Not dying from preventable meat failures (this is the big one). Also no Nazis (as a bonus)."
- layer: B, plate bond-booths
- scene: The same plate: YOU's VICTORY BONDS booth on the right, Grandma's skeleton and headstone on the left. The Rich Human waddles up to YOU's counter with a rolled treaty scroll (`KIT.props.scroll({ text: "1% TREATY" })`) under his arm; a disease blob in a "CANCER" sash lurks behind him.
- props: richHuman, YOU, bond, priceTag, diseaseBlob (sash), scroll, mask, grandma (skeleton), headstone
- status: planned

Moves: "What" → the first frame is grandmas-war-bond's last. "Offering." → the camera travels right to YOU's booth; the Rich Human waddles up to the counter, and behind him a disease blob in a "CANCER" sash (the one that got Grandma) creeps up, claws raised. "diseases" (first) → the blob shrieks and keels over flat, dead, tongue out. "people)." → YOU hands the Rich Human the bond. "seventy-two" → a price tag drops onto it: "272%", so big and heavy it swings him half round; his eyes ring up dollar signs. "grows," → the treaty scroll under his arm unrolls down to the sidewalk and keeps going, and his top hat grows taller to match. "lobbyists" → he pulls a domino mask on over his monocle, like the Lobbyist's. "failures" → his "I PREFER LIVING" button swells. "big" → it swells to the size of a hubcap and tips him forward onto the counter. "Also" → the camera pulls back to both booths. after "bonus)." → on the left, skeleton Grandma gives YOU a slow nod, and her jaw clacks.

Sound: a yelp and a thunk as the blob keels over; a pop for the tag; a cash-register ding for the dollar eyes; a rising slide whistle as the scroll and the hat grow; a click as the mask goes on; a boing as the button swells; two ticks for Grandma's jaw.

On screen: "VICTORY BONDS" / "CANCER" (the sash) / "272%" / "I PREFER LIVING".

No: no list of what YOU is offering; no fedora and no briefcase on the Rich Human (the mask is enough, and he keeps it for the rest of the part; the funnel-topped briefcase is the Lobbyist's).

Why: Grandma's deal with the disease dead and a return 68 times bigger, and the return turns the investor into a lobbyist for more.

## Scene 10 · enemy-is-the-clock

- id: enemy-is-the-clock
- act: The bribery machine
- transition_in: cut
- key: after "clock.": the Reaper sprung out of the cuckoo clock on the machine's front mid-mark, the Lobbyist, the Politician and the Weapons Maker leaning out of their hatches with NOT THE ENEMY signs over them, all three looking up at him, their waves frozen
- cue: "This raises the one billion"
- time: 38:00.7 to 38:10.0 (9.3 s)
- voiceover: "This raises the one billion dollars needed to fuel the rest of the bribery machine. Nobody in the machine is your enemy. The enemy is the clock."
- layer: B, plate the-machine
- scene: One plate on a plain field: a huge 1950s machine of riveted slate panels with dark gears (`KIT.props.gears({ dark: true })`) turning in round windows, rows of lamps, a smokestack, a hopper on top with a ladder up to it, and three hatches across its front. The cuckoo clock (see Shared drawings) hangs on its front over the middle hatch. To the right of the machine, out of frame here, an empty boxing ring (no-opposition).
- props: machine, gears, ladder, richHuman (mask), money (plain), lobbyist, politician, weaponsMaker, sign (one pole, three and a small one), cuckoo clock, reaper, clipboard
- status: planned

Moves: "billion" → at the top of the ladder the Rich Human (in his mask) tips his overflowing top hat into the hopper, and a river of plain papers pours in. "machine." → the gears turn, the lamps blink and the smokestack puffs. "Nobody" → the three hatches pop open: the Lobbyist, the Politician and the Weapons Maker lean out and wave at the camera. "enemy." (first) → a little sign on a stick pops up over each, pop, pop, pop: "NOT THE ENEMY"; then a smaller one on the baby missile: "NOT THE ENEMY (PROBABLY)". "clock." → the cuckoo clock's door bangs open and the Grim Reaper pops out on a zigzag spring instead of a bird, adds a tally mark and snaps back in. after "clock." → he pops out again, and again, about twice a second; the three slowly turn their heads up to him, their waves frozen.

Sound: a falling slide whistle as the papers pour; a whirr as the machine starts; three pops for the signs and a smaller one for the missile's; a boing each time the Reaper pops out.

On screen: "NOT THE ENEMY" (three) / "NOT THE ENEMY (PROBABLY)" / the clock's plaque "150,000 / DAY".

No: no sign naming the machine; no "$1 BILLION" on the papers.

Why: the people in the machine are doing their jobs; what kills people is how long it all takes.

## Scene 11 · stop-reading

- id: stop-reading
- act: The money loop
- transition_in: cut
- key: after "step:": Wishonia's fist down on the lectern, the reader in his armchair beside it jolted awake, holding his book open upside down
- cue: "How the Money Loop"
- time: 38:10.0 to 38:17.6 (7.6 s)
- voiceover: "How the Money Loop Works. Here's the part where humans usually stop reading because it involves following money through more than one step:"
- layer: A, host
- scene: The host's set. On the free wall right of the lectern, the reader from Part 8 (see Shared drawings) in his orange wingback armchair under his floor lamp, reading the manual.
- wishonia: big, skeptical-smile + body-presenting; sideeye-closed + body-idle on "stop"; smirk-smile + body-counting on "more"; annoyed-closed + body-fist on "step:"
- props: studio, lectern, person (the reader), armchair, floor lamp, manual
- status: planned

Moves: "How" → she presents the heading to the camera. "Here's" → the reader in his armchair slides in on the free wall beside the lectern, lamp and all, reading. "stop" → she side-eyes him. "reading" → he closes the book on his finger and nods off; a "Z" floats up. "more" → she holds up one finger. "step:" → she brings her fist down on the lectern; he jolts awake and snaps the book open again, upside down.

Sound: a soft huff as he nods off after "reading"; a thunk on "step:" and a boing as he jolts awake.

On screen: nothing but the set, the guest and his "Z".

No: no chart or heading card; she says the heading.

Why: a breath before the longest chain in the part, aimed at the viewer about to tune out.

## Scene 12 · loop-steps-one-two

- id: loop-steps-one-two
- act: The money loop
- transition_in: cut
- key: on "spending:": the war tank, heaped over its rim with war money, pouring war money into the color-flip funnel, its gauge one notch lower, the Weapons Maker sitting on the heap glancing down at the gauge mid-shrug, his baby missile in his arms
- cue: "One. You sell one"
- time: 38:17.6 to 38:36.6 (19.0 s)
- voiceover: "One. You sell one billion dollars in VICTORY Incentive Alignment Bonds to investors. This funds the campaign. Two. The campaign succeeds. Your treaty redirects one percent of military spending: twenty-seven point two billion dollars a year flows from the murder budget to clinical trials."
- layer: B, plate money-loop
- scene: One plate like Part 2's loop road, in its colors: a stadium-shaped cream road with a dashed center line on a plain tan field, the stops beside it, traveled clockwise, one framing per phrase. Top straight, left to right: YOU's VICTORY BONDS booth (the bond-booths drawing) with a hopper beside it, the Rich Human (masked) at the counter; the campaign office, a little storefront under a plain striped awning and bunting, the Loud Human inside; the treaty (`KIT.props.scroll({ text: "1% TREATY" })` on a stand) with the Politician beside it holding a pen; and at the top-right bend the war tank (a slate drum heaped over its rim with war money, missile seals up, a level gauge on its front, `KIT.props.gauge({ mount: "dial" })`, a valve wheel at its foot, the Weapons Maker sitting on the heap rocking his baby missile) emptying into the color-flip funnel over the road. At the bottom of the right bend, across the road: the glass toll booth (the glass case of Shared drawings stood on end, its "CAPPED AT 20%" plate on the roof, a striped boom gate, YOU inside on a stool with a long-handled grabber, the 20% standing in countable rows on shelves behind him, two little doors in its back). Along the bottom straight, right to left: the Super PAC with three senators in a row, a billboard frame behind each, and the POST-OFFICE CAREERS door; then the lab shed and the hospital (`KIT.props.hospital({ label: "" })`), where the road's bills turn in, the Grim Reaper waiting at the hospital door, and a few germs (`KIT.props.germ`) clinging to the two roofs. Up the left bend the road comes back to YOU's booth. No sign on the plate names a stop; the stops are few and big enough to read in the pull-back, and the money going round the road is what the pull-back is about.
- props: money-loop plate, booth, hopper, richHuman (mask), YOU, bond, money (plain, war, med), campaign office, loudHuman, scroll, politician, tank, gauge, weaponsMaker, colorFlipFunnel, priceTag
- status: planned

Moves: "One." → framing on YOU's booth: YOU behind the counter, the Rich Human in front of it. "sell" → the Rich Human tips a hatful of plain papers into the hopper. "VICTORY" → a VICTORY bond shoots out of the counter's slot and lands in his top hat. "investors." → he puts the hat back on, the bond sticking out of the band like a feather. "campaign." → the hopper's papers hop down onto the road and march right; the camera travels with them to the campaign office, they file in at its door, and the Loud Human bursts out of the window blasting through his megaphone head. "Two." → the camera travels on to the treaty. "succeeds." → the Politician signs it with a flourish. after "succeeds." → the valve wheel at the foot of the war tank spins open. "redirects" → war money pours out of the tank into the color-flip funnel. "percent" → the tank's gauge drops one notch; the Weapons Maker on the heap glances down at it, shrugs, and keeps rocking his missile. "twenty-seven" → medicine money walks out of the spout onto the road, each seal flipping with a sparkle, and a price tag swings on the spout: "$27.2 BILLION / YEAR". "trials." → the camera follows the new bills down the right bend.

Sound: a whoosh as the papers go into the hopper; a pop for the bond; a cash-register ding as the hat goes back on; a whistle for the Loud Human; a marker squeak for the signature; a whirr as the valve opens; a tick as the gauge drops; a sparkle as the seals flip.

On screen: "VICTORY BONDS" / "1% TREATY" / "$27.2 BILLION / YEAR".

No: no step numbers on the plate; the narrator counts and the camera arrives on each number.

Why: steps 1 and 2, and 1% is a notch the war industry barely notices.

## Scene 13 · loop-steps-three-four

- id: loop-steps-three-four
- act: The money loop
- transition_in: same plate (no seam)
- key: after "not.": the Rich Human flat on his back at YOU's booth like a tipped egg, stub legs in the air, the check stamped NOT A TYPO in his hands, "272%" big in the sky over him, the bill that brought the check standing by his head
- cue: "Three. The Victory Corporation"
- time: 38:36.6 to 39:01.0 (24.4 s)
- voiceover: "Three. The Victory Corporation (the company that issued the bonds) takes a twenty percent management fee on that twenty-seven point two billion dollars. Four. Half of that fee (ten percent) goes to investor dividends: two point seven two billion dollars a year on a one billion dollar investment. That's two hundred and seventy-two percent annual returns. Your investors will think it's a typo. It's not."
- layer: B, plate money-loop
- scene: The same plate: down the right bend to the glass toll booth, then straight across the infield, on foot, to the Rich Human at YOU's booth.
- props: money-loop plate, glass toll booth, YOU, grabber, money (med), check, richHuman (mask), stamp, stampMark
- status: planned

Moves: "Three." → the first frame is loop-steps-one-two's last; the camera follows the bills down the bend to the glass toll booth across the road, YOU inside on his stool. "bonds)" → YOU points at himself and tips his bowler. "twenty" (first) → the boom gate lifts for the bills, and YOU plucks two of every ten off the road with a long-handled grabber and stands them on the shelves behind him, in countable rows under the roof plate "CAPPED AT 20%". "Half" → two little doors open in the back of the booth and the bills on the shelves split, half to each. "dividends:" → one bill steps out of the first door with a check under its arm and runs straight across the infield, the camera running with it, to YOU's booth. after "dividends:" → it climbs up the Rich Human's belly and hands him the check. "billion" (second) → the check fills in: "$2.72 BILLION / YEAR". "investment." → he looks from it to the VICTORY bond in his hatband and back. "seventy-two" → "272%" stamps big into the sky over him. "typo." → he polishes his monocle and looks again; his eyes spin into dollar signs. "not." → a rubber stamp slams "NOT A TYPO" onto the check, and he goes straight over backwards like a felled tree: flat on his back, stub legs in the air, rocking like a tipped egg, still clutching the check, while the bill looks down at him. It has to land on the word: count-five cuts in half a second later.

Sound: a pop as YOU's grabber plucks the bills; pattering feet as the bill runs across; a typewriter as the check fills in; a thunk as 272% lands; a cash-register ding for the dollar eyes; a stamp thump on "not." and a thunk as he hits the ground.

On screen: "CAPPED AT 20%" / "$2.72 BILLION / YEAR" / "272%" / "NOT A TYPO".

No: no "= 272%" sum chalked between the papers; the big number is the sum.

Why: steps 3 and 4, and the 272% lands on the man who paid in, from the reader's own company.

## Scene 14 · count-five

- id: count-five
- act: The money loop
- transition_in: cut
- key: on "Five.": Wishonia at the lectern, palms flat on its top, rolling her eyes up to the ceiling, her mug beside her hand
- cue: "Five."
- time: 39:01.0 to 39:02.5 (1.5 s)
- voiceover: "Five."
- layer: A, host (reaction cut)
- scene: The host's set, her mug (see Shared drawings) on the reading top. Nothing else.
- wishonia: big, eyeroll-closed + body-palms-down
- props: studio, lectern, mug
- status: planned

Moves: "Five." → cut to Wishonia at the lectern, palms flat on its top; she rolls her eyes up to the ceiling and slowly back down to the camera.

Sound: none.

On screen: nothing but the set.

No: no push or iris; it is a one-and-a-half-second cut.

Why: the investor fainting at his own returns gets its look, and the narrator's "Five." is said to the camera.

## Scene 15 · pavlovian-senators

- id: pavlovian-senators
- act: The money loop
- transition_in: cut (back to the money loop on loop-steps-three-four's last frame)
- key: after "senators.": the three-sticker senator sitting up like a trained dog, tongue out, hands up like paws, tie wagging, a YES-shaped biscuit in his teeth, the bell still trembling on the Super PAC's desk, the other two senators sitting up too
- cue: "The other half (ten"
- time: 39:02.5 to 39:20.8 (18.3 s)
- voiceover: "The other half (ten percent) goes to a Super PAC that spends two point seven two billion dollars a year getting treaty-friendly politicians elected and funding cushy post-office careers for the ones who voted yes. The more you voted for the treaty, the more support you get. It's Pavlovian conditioning, but for senators."
- layer: B, plate money-loop
- scene: The same plate: back from YOU's booth to the glass toll booth, then along the road to the Super PAC, the three senators and the POST-OFFICE CAREERS door. A little desk bell on a stand beside the Super PAC.
- props: money-loop plate, glass toll booth, super-pac, money (med), priceTag, politician (three senators), billboard, door, sticker, bell, biscuit
- status: planned

Moves: "The" → the first frame is loop-steps-three-four's last (the Rich Human still rocking on his back); the camera travels back across the infield to the glass toll booth. "Super" → the other half marches out of its second door along the road into the Super PAC, which swallows them, cape flapping. "billion" → a price tag swings on its strap: "$2.72 BILLION / YEAR". "elected" → it throws a billboard up behind the first senator: his grin and a "YES" button. "post-office" → the door swings open on a comfy armchair, slippers and a golf bag. "more" (first) → the camera eases back to the three senators in a row in front of their billboards; "YES" stickers pop onto them: one on the first, two on the second, three on the third. "get." → each billboard grows with his stickers; the three-sticker senator's runs off the top of the frame. "Pavlovian" → the Super PAC rings the desk bell. "senators." → the three-sticker senator sits up like a dog, tongue out, hands up like paws, his wide tie wagging like a tail; the Super PAC tosses him a dog biscuit shaped like a YES button, and he catches it in his teeth. after "senators." → the other two sit up too.

Sound: a whoosh as the bills pour in; a thunk for the billboard; a door squeak; a pop per sticker; a rising slide whistle as the billboards grow; a bell on "Pavlovian"; a woof as he sits up.

On screen: "$2.72 BILLION / YEAR" / "SUPER PAC" / "POST-OFFICE CAREERS" / "YES" (stickers and billboards).

No: no bill into a senator's hand; the Super PAC pays for billboards, careers and one biscuit.

Why: step 5, and why politicians keep voting yes.

## Scene 16 · greed-loop-runs

- id: greed-loop-runs
- act: The money loop
- transition_in: same plate (no seam)
- key: after "existing.": the whole loop road in frame like the end of Part 2's, a ring of medicine money walking round it nose to tail, the stops quiet beside it, the germs on the hospital and lab roofs popped
- cue: "The remaining eighty percent"
- time: 39:20.8 to 39:43.2 (22.4 s)
- voiceover: "The remaining eighty percent of twenty-seven point two billion dollars goes where it's supposed to: funding clinical trials that keep humans alive. This is the entire trick. You use greed to fund the campaign, greed to pass the treaty, and greed to keep it passed. The money just circulates until diseases stop existing."
- layer: B, plate money-loop
- scene: The same plate: along the bottom straight to the lab shed and the hospital, then a pull-back to the whole loop, three close framings on the greedy, and the whole loop again.
- props: money-loop plate, lab, scientist, hospital, person (everyday patients), reaper, clipboard, germ, money (med)
- status: planned

Moves: "The" → the first frame is pavlovian-senators' last. "eighty" → the camera travels left along the bottom straight with the bills that passed the toll, to the lab shed and the hospital. "alive." → the bills turn in; humans walk into the hospital with red chest lights blinking and out with teal ones. after "alive." → the Grim Reaper waiting at the hospital door, clipboard ready, has to erase a tally mark instead; he sulks. "entire" → the camera pulls back until the whole loop is in frame, and holds on the money: medicine bills walking round the road nose to tail, the only thing moving. "greed" (first) → the camera pushes in on YOU's booth: the Rich Human's eyes ring up dollar signs. "greed" (second) → it slides along to the treaty: the Politician's do. "greed" (third) → it drops across the infield to the Super PAC: all three senators' do. "passed." → the senators sit up like dogs again. "circulates" → the camera pulls back to the whole loop and holds there: the money runs round and round it, faster and faster, until it is a green ring. "stop" → the germs on the hospital and lab roofs pop one by one like balloons, in little bursts.

Sound: a ding as the chest lights turn teal; a scratch for the eraser; a cash-register ding on each "greed"; a woof as the senators sit up; a whirr as the money circles; a pop per germ.

On screen: nothing new.

No: no GREED tags; the dollar-sign eyes say it, close up. No dollar eyes in the wide shot, where the actors are too small to read.

Why: the loop runs on greed alone, so nobody has to be good.

## Scene 17 · no-opposition

- id: no-opposition
- act: The money loop
- transition_in: cut (back to the-machine plate)
- key: after "finish.": the three humans in the ring's corner doing the sum, NOT THE ENEMY signs still up, the Lobbyist a grinning skeleton in his fedora and domino mask with his pencil still moving, the cuckoo clock on the machine beside the ring with the Reaper out
- cue: "None of this is overcoming"
- time: 39:43.2 to 39:55.7 (12.5 s)
- voiceover: "None of this is overcoming opposition. There is no opposition. There are only humans who haven't done the arithmetic yet, and one hundred and fifty thousand daily funerals that won't wait for them to finish."
- layer: B, plate the-machine
- scene: The-machine plate of enemy-is-the-clock: right of the machine, an empty boxing ring with a banner on its apron, "OPPOSITION", and a ring bell on a corner post. The cuckoo clock still hangs on the machine.
- props: boxing ring, bell, tumbleweed, lobbyist, politician, weaponsMaker, sign (NOT THE ENEMY), scroll (the sum), pencil, cuckoo clock, reaper, clipboard, xray
- status: planned

Moves: "None" → framing on the empty boxing ring, "OPPOSITION" on its apron. "opposition." (second) → the ring bell dings; nobody steps in; crickets, and a tumbleweed rolls across the canvas. "humans" → the camera finds the ring's corner: the Lobbyist, the Politician and the Weapons Maker sit on the canvas, their NOT THE ENEMY signs still up, a long sum unrolled on a scroll in front of them. "arithmetic" → they work it with pencils; the Politician counts on his fingers, and the Lobbyist peeks at the Weapons Maker's answer. "hundred" → the camera pulls back to take in the cuckoo clock on the machine beside the ring: the Reaper pops out at the true rate, adding marks. "funerals" → HOLD 1 to 2 s: nothing moves but the Reaper's pencil. "finish." → the pencils move again; the Reaper pops out once more and adds a mark, and the Lobbyist x-rays into a grinning skeleton, fedora and domino mask still on, still working the sum. It holds until sounds-familiar cuts in, about a second later.

Sound: a ring bell on "opposition."; crickets after it; a pencil scratch on "arithmetic"; a boing as the Reaper pops out on "hundred"; silence for the HOLD; an x-ray zap on "finish.".

On screen: "OPPOSITION" / "NOT THE ENEMY" (three) / the clock's plaque "150,000 / DAY".

No: no motion but the Reaper's pencil during the HOLD, and no sound.

Why: there is nobody to fight; the only thing to beat is the time humans take to do the sum.

## Scene 18 · sounds-familiar

- id: sounds-familiar
- act: The complexes
- transition_in: cut
- key: on "familiar,": Wishonia at the lectern, arms crossed, one eyebrow up at the camera, her mug beside her
- cue: "If this sounds familiar,"
- time: 39:55.7 to 39:57.3 (1.6 s)
- voiceover: "If this sounds familiar,"
- layer: A, host (reaction cut)
- scene: The host's set, her mug (see Shared drawings) on the reading top. Nothing else.
- wishonia: big, skeptical-smile + body-arms-crossed
- props: studio, lectern, mug
- status: planned

Moves: "If" → cut to Wishonia at the lectern, arms crossed, one eyebrow up at the camera; she holds it.

Sound: none.

On screen: nothing but the set.

No: no push or iris; it is a cut of about a second and a half.

Why: a look after the Lobbyist's skeleton, and the line that turns to the viewer is said to the viewer.

## Scene 19 · military-industrial-loop

- id: military-industrial-loop
- act: The complexes
- transition_in: cut
- key: after "corpses.": Part 2's loop road framed on its printing press, cranking itself with nobody at the wheel, the Politician and the Weapons Maker standing back from it, a war paper and a little grey headstone on stick legs hopping out of it, and a pile of headstones beside it
- cue: "it should. Eisenhower"
- time: 39:57.3 to 40:14.7 (17.4 s)
- voiceover: "it should. Eisenhower warned you about the Military Industrial Complex: weapons manufacturers fund politicians, politicians fund weapons contracts, contracts fund contractors, contractors fund politicians. It's a self-sustaining loop that prints money and corpses."
- layer: B, plate two-loops
- scene: One plate, two loop roads side by side. On the left, Part 2's loop road, drawn by the code of `../compositions/scenes/part-02/money-loop.html`: the printing press with the Politician at its wheel, the factory whose chimneys are smiling missiles with the Weapons Maker at its door, a rebuilt house, the pay window and the farm stand with the farmer; war money walks the road. A period arch over the road by the factory, "MILITARY INDUSTRIAL COMPLEX", and beside the factory an empty podium with a microphone, a little alarm bell and the name card "EISENHOWER" (Part 15's). On the right, out of frame until patient-industrial-loop, the money loop of Steps 1 to 5 (the money-loop plate's drawing), with the war loop's factory across a narrow gap from YOU's booth.
- props: Part 2's loop road, printingPress, politician, factory, weaponsMaker, house, pay window, farm stand, farmer, money (war), arch, podium, bell, name card, scroll (the contract), headstone
- status: planned

Moves: "it" → the whole of Part 2's loop, as Part 2 left it (papers walking round, the press cranking, a new house where the old one stood), and the camera pushes in at once on the factory door. "should." → the Weapons Maker waves at the camera like an old friend, and his baby missile waves too. "Eisenhower" → the camera slides to the podium beside him: an empty microphone and the name card "EISENHOWER". "warned" → the little alarm bell on the podium rings itself silly; the Weapons Maker sticks a finger in one ear. "Complex:" → the camera eases back to take in the arch over the road: "MILITARY INDUSTRIAL COMPLEX". "manufacturers" → the camera travels left with the Weapons Maker to the press, where he stuffs war money into the Politician's breast pocket. "contracts," (first) → the Politician signs a contract with a missile drawn on it and hands it back. "contractors," (first) → the Weapons Maker carries it back into his factory; the chimneys puff. "politicians." (last) → war papers march out of the factory, round the road and back into the Politician's pocket. "self-sustaining" → both men let go and step back: the wheel cranks itself, and the papers keep walking round. "prints" → the press stamps out a war paper. "corpses." → the next sheet out of the press is a little grey headstone (`KIT.props.headstone`) on stick legs; then paper, headstone, paper, faster, and the headstones hop down onto a growing pile beside the press.

Sound: an alarm bell on "warned"; a cash-register ding for the pocket; a marker scratch for the signature; a whirr as the wheel cranks itself; a stamp thump on "prints"; a thunk for each headstone from "corpses.".

On screen: "EISENHOWER" / "MILITARY INDUSTRIAL COMPLEX".

No: no portrait of Eisenhower (his name card only).

Why: the machine the viewer watched in Part 2 is the complex Eisenhower named, and nobody has to push it.

## Scene 20 · patient-industrial-loop

- id: patient-industrial-loop
- act: The complexes
- transition_in: same plate (no seam)
- key: after "them).": both loop roads side by side under their two arches, the war press's headstones a mountain, and on the money loop three small headstones by the lab, the first one "CANCER"
- cue: "You're building the same"
- time: 40:14.7 to 40:38.4 (23.7 s)
- voiceover: "You're building the same machine, but pointed at diseases instead of countries. Call it the Patient Industrial Complex. Investors fund politicians, politicians fund clinical trials, trials generate returns, returns fund investors, investors fund politicians. Same loop. Same greed. Same self-sustaining mechanics. Different corpses (fewer of them)."
- layer: B, plate two-loops
- scene: The same plate, now with the money loop on the right in frame. A second arch, the same as the first, waits above the frame over the money loop's road. A disease blob sits on the lab shed's doorstep.
- props: two-loops plate, scientist, flask, diseaseBlob, germ, weaponsMaker, farmer, arch, richHuman (mask), super-pac, politician (a senator), scroll (the contract), lab, money (war, med), printingPress, headstone
- status: planned

Moves: "You're" → the first frame is military-industrial-loop's last. "machine," → the camera pulls back and slides right: beside the war loop is the money loop from Steps 1 to 5, the same shape, its medicine money circling. "diseases" → the camera pushes in on the money loop's lab shed: the Scientist points her bubbling flask at the disease blob on the doorstep like a ray gun; it gulps and puts its claws up. "countries." → the camera snaps back to the war loop's farm stand: the Weapons Maker points his baby missile at the farmer, who puts his hands up the same way. "Complex." → the camera pulls back as the second arch drops in over the money loop's road: "PATIENT INDUSTRIAL COMPLEX". "politicians," (first) → framing on the money loop: the Rich Human tips medicine money into the Super PAC, which throws up a senator's billboard. "trials," (first) → the senator signs a contract with a pill drawn on it, and it flies off to the lab. "returns," (first) → the Scientist's flask boils over with medicine money. "investors," (first) → the money walks round the road into the Rich Human's top hat. "politicians." (last) → he tips it into the Super PAC again. "loop." → the camera pulls back to both loops, side by side, their papers running in step. "greed." → framing on the gap between them: the Weapons Maker at his factory door and the Rich Human at YOU's booth, back to back; both their eyes ring up dollar signs at the same moment, and they glance at each other. "mechanics." → the camera pulls back again: the war press cranks itself and the money loop's bills circle by themselves, nobody touching either. "Different" → the camera pushes in on the war press: its headstones are a mountain now. "corpses" → it slides to the money loop's lab: the disease blob lies dead on the doorstep, and a small headstone pops up over it, "CANCER"; then a tiny one with a germ on it. "(fewer" → one last tiny headstone pops up, and no more come. after "them)." → the camera eases back until both are in frame: the mountain on the left, three little stones on the right.

Sound: a whoosh as the camera slides right; a yelp from the blob on "diseases"; a thunk as the arch lands; a pop as the money hops into the Super PAC; a marker scratch for the contract; a sparkle for the boiling flask; a cash-register ding for the hat; a cash-register ding on "greed."; a thunk per small headstone and a small pop for the last one.

On screen: "MILITARY INDUSTRIAL COMPLEX" / "PATIENT INDUSTRIAL COMPLEX" / the headstones "CANCER" and the germ's.

No: no bill into the senator's hand on the money loop; it goes through the Super PAC.

Why: the same greed, pointed at diseases instead of countries, and the diseases are what die.

## Scene 21 · evolved-on-purpose

- id: evolved-on-purpose
- act: The complexes
- transition_in: cut
- key: after "orphans.": YOU beside the lectern holding his neat flower pot, snipping the creeping war-red vine with garden shears without looking at it; Wishonia side-eyeing the camera; the blank blueprint unrolled on the lectern top
- cue: "The Military Industrial Complex wasn't"
- time: 40:38.4 to 40:53.0 (14.6 s)
- voiceover: "The Military Industrial Complex wasn't designed. It evolved, because the incentives aligned. An Incentive Alignment Bond just aligns them on purpose, toward something that doesn't require orphans."
- layer: A, host
- scene: The host's set. A rolled blueprint lies on the lectern's reading top. YOU comes in on the free wall right of the lectern with a neat clay flower pot: a tidy teal plant whose leaves are medicine bills, staked with the Incentive Alignment Bond from heres-one.
- wishonia: big, thinking-closed + body-thinking; eyeroll-smile + body-shrug on "designed."; happy-smile + body-presenting on "An"; sideeye-closed + body-arms-crossed on "orphans."
- props: studio, lectern, blueprint, vine (war bills for leaves, missile buds), YOU, flower pot, bond, trowel, garden shears
- status: planned

Moves: "The" → back at the lectern; she looks thoughtful. "designed." → the blueprint on the lectern top unrolls itself toward the camera: blank, not one line on it. "evolved," → a war-red vine creeps into the frame from the right edge along the chair rail, its leaves war bills, little missiles budding on it. "aligned." → all its leaves snap round to face the same way, like soldiers. "Bond" → YOU steps in under it, beside the lectern, holding the flower pot. "purpose," → he pats the soil with a trowel, and the teal plant stands up straight. "orphans." → the vine has crept down to the pot; YOU snips it off with garden shears without looking at it. after "orphans." → Wishonia side-eyes the camera, and the film irises out on her face, to black.

Sound: a whoosh as the blueprint unrolls; a rising slide whistle as the vine grows; a click as its leaves snap into line; soft pats on the soil; a snip on "orphans.".

On screen: nothing but the set, YOU and the plant.

No: no tags on the vine or the pot.

Why: war built its loop by accident; the bond plants this one on purpose, and the reader keeps it weeded.
