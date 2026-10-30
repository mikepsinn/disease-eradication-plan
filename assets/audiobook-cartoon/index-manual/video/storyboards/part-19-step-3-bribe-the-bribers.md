---
format: 1920x1080
duration: 1:09.8
message: "Lobbyists have clients, not beliefs, so you hire them away: the same salary, a better legacy, and an economy 1.43 times larger."
arc: Title card, a $500,000 price tag that turns out SOLD → the Lobbyist on the therapist's couch, where one war bill comes back as 1,813 and floods the room → the spreadsheet's current job: the salary, a needle stuck by the missile, his own headstone → your offer: the same salary in medicine money, a binned cluster bomb that chars the therapist, PHILANTHROPIST, the brass plaque → close-up: the briefcase holds no beliefs, only a rolodex → two client cards: he dies in one world and lives in the other, and the Calculator does not scream
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 19, "Step 3: Bribe the Bribers"
audio: index-manual.cbaf659d.mp3, 43:10.9 to 44:20.7
version: v2
---

# Part 19 storyboard: "Step 3: Bribe the Bribers"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The Lobbyist's briefcase, with the little striped funnel on top that it had in Part 5. In briber-conversion-therapy it swallows one war bill and gushes 1,813 back until the room floods; in current-job-column it slurps the whole flood back in and stays hugged on his chest through the spreadsheet; in lobbyists-have-clients it pops open on an empty BELIEFS slot and a rolodex; in two-clients-arithmetic it goes through the color-flip funnel and comes out with a teal cross sticker, which it keeps for the rest of the episode.

**Running gag: the therapist takes every hit.** The conversion therapist is the viewer (his lapel badge says YOU). He sinks to the chest in the money flood and keeps writing, is charred black by the cluster bomb the spreadsheet throws away and keeps writing, and in two-clients-arithmetic his charred, still-smoking portrait is the new client.

**Shared drawings** (two author groups draw these, so they must match):
- **The Lobbyist.** `KIT.cast("lobbyist")`: fedora pulled low, domino mask, popped-collar trench coat, gloves. His briefcase is drawn as its own group (cast option `holdL: null`), so it can open.
- **The briefcase.** The kit's brown leather case (`#6B4A2F`, navy outline, a navy handle), drawn big: two brass latches (`KIT.C.yellow`) and a small funnel on top, striped navy and cream like the color-flip funnel's, with a bill corner peeking out of the lid. Open: the lid is lined in red velvet with one slot under a little brass label, "BELIEFS" (empty); the case is stuffed with war bills; a rolodex lies folded flat on a coil spring. From two-clients-arithmetic on, a round teal cross sticker (`KIT.moneySeal("med", ...)`) sits on its front.
- **The therapist (YOU).** An everyday human, `KIT.person({ tone: 1, outfit: "suit", color: 2, hair: 2, glasses: true, stache: true, mood: "flat" })`, with a small cream lapel badge, "YOU" in navy Oswald, drawn over the body so it survives the charring. His notebook is `KIT.props.clipboard` held at his `KIT.rig` hand. From after "bombs." in your-offer-column on, he is the same person with `charred: true`, glasses askew, smoking, his eyes blinking.
- **The CURRENT CLIENT card.** A rolodex card: cream, rounded corners, two notches in the bottom edge, a navy outline, a war-red tab at the top left, "CURRENT CLIENT" in cream Oswald, and an oval portrait of `KIT.cast("weaponsMaker")` from the chest up, grinning around his cigar, cradling his smiling missile. The NEW CLIENT card is the same card with a teal (`#1F6E68`) tab, "NEW CLIENT", and the charred therapist's portrait with his YOU badge.

**Callbacks.** The masked Lobbyist and his funnel-topped briefcase from step-3-lobbyist-funnels (Part 5). The moth that flew out of the empty wallet in without-with-papers (Part 1) flies out of the empty BELIEFS slot. The Calculator from The Math (Part 16), still cracked and missing its "=" key and one more, walks back onto a table in two-clients-arithmetic and, for once, does not scream.

**Callbacks set up here.** The brass plaque "Accidentally saved humanity while getting rich" from your-offer-column hangs on the back of the treaty cart in cure-death-by-mistake (Part 26). The briefcase's teal cross sticker is on the Lobbyist in Part 21 (panel 5).

**Bans for this part.**
- No real people or logos.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: in 16:9 nothing important below y 900; in 9:16 nothing important from y 1450 down. Keep Wishonia's corner clear (16:9 x 1600 to 1920, y 690 down; 9:16 x 740 to 1040, y 60 to 430).
- The money is always money green: war bills (red missile seals) on the current job's side, medicine bills (teal cross seals) on the offer's side.
- No real lobbying firms, clients, companies or capitols; plain signs only.
- No labels that repeat the narration ("1.43× economy", "cluster bombs", "arms dealer"): the bars, the crossed-out bomb and the missile on the dial say it.

## Changes from v1

- The humans are the stereotype cast: the Lobbyist is the masked crook, the current client the Weapons Maker, and the therapist an everyday human in a suit with a YOU badge (the viewer, who is doing the converting).
- The gags go all the way: the briefcase floods the room with 1,813 bills and buries the capitol, the gauge needle sticks next to the missile, the headstone is his own and a skeleton hand waves a bill out of it, the binned cluster bomb blows up the therapist, and the Lobbyist dies in the current client's world and comes back in the new one.
- step-3-bribe-the-bribers-title cuts in (a title card has no wall screen to zoom out of), and briber-conversion-therapy slides in from it.
- lobbyists-have-clients is a close-up of the briefcase, so the empty BELIEFS slot and the rolodex can be read.
- No countdown board in this part. Recurring props come from the shared library (`KIT.props.*`).

## Scene 1 · step-3-bribe-the-bribers-title

- id: step-3-bribe-the-bribers-title
- act: Title
- transition_in: cut (Part 18 ends on Layer B; the parts are rendered on their own and joined)
- key: both heading lines in, the "$500,000" tag swinging from the last S, a beat before it spins to SOLD
- cue: "Step 3: Bribe the Bribers"
- time: 43:10.9 to 43:14.7 (3.8 s)
- voiceover: "Step 3: Bribe the Bribers."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`) with the step number and its name; a price tag hangs off the last letter.
- wishonia: none
- props: title-card, price-tag
- status: outline

Moves: "Step" → "STEP 3" drops in as one line, small, over the heading (the alignment gives "Step" and "3" almost the same start). "Bribe" → "BRIBE" slams in, then "THE" on "the". "Bribers." → "BRIBERS" slams in. after "Bribers." → a price tag drops onto the last S on its string and swings: "$500,000", the going rate for one briber (current-job-column pays it off). A beat later the tag spins round on its string: its back says "SOLD".

Sound: a thunk on each heading word; a cash-register ding as the tag lands; a whoosh as it spins.

On screen: "STEP 3" / "BRIBE THE BRIBERS" / the tag "$500,000", then "SOLD". No: no Wishonia; the card is the heading. Why: the narrator reads the heading; the tag is the step in one gag: a briber has a price, and you pay it.

## Scene 2 · briber-conversion-therapy

- id: briber-conversion-therapy
- act: The patient
- transition_in: slide left
- key: on "thirteen": the geyser of war bills from the briefcase hitting the ceiling, "1,813" on the counter, the Lobbyist's eyes dollar signs, the therapist sunk to the chest and still writing
- cue: "Professional Briber Conversion Therapy"
- time: 43:14.7 to 43:25.7 (11.0 s)
- voiceover: "Professional Briber Conversion Therapy Military lobbyists currently get one thousand, eight hundred and thirteen dollars back per dollar invested in democracy corruption."
- layer: B
- scene: A hallway door with gold lettering on its frosted glass and a queue of identical Lobbyists; through it, a 1950s therapist's office: the Lobbyist lying on the couch hugging his briefcase, the therapist (YOU) in a wingback armchair with his notebook, a wastebasket by the chair, a side table with a lamp and a tiny domed capitol.
- wishonia: PiP, thinking-small, then surprised-oh on "thousand,", then eyeroll-closed + body-shrug on "corruption."
- props: door, lobbyist, briefcase, therapist, couch, wastebasket, papers-red, capitol, clipboard
- status: outline

Moves: "Professional" → the scene slides in on a hallway: a door with "PROFESSIONAL BRIBER CONVERSION THERAPY" in gold on its frosted glass, and three identical Lobbyists queued along the wall beside it, each hugging the same briefcase and holding a numbered ticket. "Therapy" → the door swings open on a dark doorway and the camera dives through it into the office: the Lobbyist lies on the couch hugging his funnel-topped briefcase; the therapist sits in his armchair, notebook open; on the wall, a framed diploma that is just a framed bill. "Military" → one war bill walks in on stick legs. "lobbyists" → it hops into the briefcase's funnel. "currently" → the briefcase rumbles on his chest. "one" → its latches pop and a geyser of war bills shoots out of it to the ceiling; a big counter over it starts rolling up from 1. "thousand," → the Lobbyist's eyes turn into dollar signs. "eight hundred" → the bills rain down and pile up; the therapist sinks into them to the chest, notebook held high, still writing. "thirteen" → the counter stops on "1,813" with a ding. "dollars" → the pile lifts the couch off its legs and the Lobbyist floats on it like a raft, hands behind his head. "invested" → he feeds one more bill into the funnel: a second geyser, and the counter races on to "3,626". "democracy" → the pile reaches the side table and climbs the tiny capitol. "corruption." → the capitol goes under, its pennant last. after "corruption." → one bubble pops on the surface where it was.

Sound: a door creak (squeak) on "Therapy"; tiny squeaky footsteps; a pop into the funnel; a click and a whoosh for the geyser; a yelp as the therapist goes under; a cash-register ding at 1,813; a pop and a whoosh for the second bill; a sinking slide whistle for the capitol and a pop for the bubble.

On screen: the door "PROFESSIONAL BRIBER CONVERSION THERAPY" / the counter "1,813", then "3,626". No: no "$1 in" label (the one walking bill is the dollar); no real capitol, firm or client. Why: why lobbyists lobby for war: a dollar comes back as 1,813, every time.

## Scene 3 · current-job-column

- id: current-job-column
- act: The spreadsheet
- transition_in: same form (no seam)
- key: on "orphans": the left column full (the "$500,000" stack of war bills, the needle a hair from the missile, his own headstone with a skeleton hand waving a bill out of the mound), the Lobbyist's head turning to the camera
- cue: "Show them a spreadsheet"
- time: 43:25.7 to 43:40.5 (14.8 s)
- voiceover: "Show them a spreadsheet: Current Job. The salary is five hundred thousand dollars. The moral status is somewhere between "arms dealer" and "the person who puts raisins in cookies". The legacy is "Here lies someone who made orphans"."
- layer: B
- scene: The flood goes back into the briefcase; an easel rolls in beside the couch with a ledger sheet: rows SALARY, MORAL STATUS and LEGACY under two columns. The left column, CURRENT JOB, fills in.
- wishonia: PiP, smirk-closed, then sideeye-closed + body-arms-crossed on "orphans"
- props: lobbyist, briefcase, therapist, couch, easel, spreadsheet, pencil, papers-red, gauge, missile, price-tag, cookie, headstone, skeleton
- status: outline

Moves: "Show" → the first frame is briber-conversion-therapy's last: the room flooded, the couch afloat. The Lobbyist snaps the briefcase shut and the whole flood slurps back into its funnel in one long gulp; the couch drops back onto its legs, the therapist pops back up in his chair, still writing, and the tiny capitol bobs back up, its pennant drooping. "spreadsheet:" → an easel rolls in from the right on squeaky casters and stops beside the couch: a ledger sheet with the rows SALARY, MORAL STATUS and LEGACY and two empty columns. The Lobbyist turns his head to look. "Current Job." → a pencil floats in and writes "CURRENT JOB" over the left column. "five hundred thousand" → a fat stack of war bills with a paper band, "$500,000", thumps into the salary cell. "moral status" → a small dial gauge draws into the next cell. "arms dealer" → a little missile pops up at the dial's left end, a price tag swinging from its fin; the needle swings to it. "raisins" → a raisin cookie with a frown pops up at the right end; the needle swings lazily toward it. after "cookies" → it swings back and settles a hair from the missile: technically somewhere between. "Here lies" → a headstone rises out of a dirt mound in the legacy cell, a fedora and a domino mask like his hung on its corner. "made" → a skeleton hand pokes up out of the mound, still in its glove, clutching a war bill, and waves it. "orphans" → the Lobbyist turns his head slowly from the headstone to the camera.

Sound: a click as the briefcase snaps shut and a long whoosh as the flood goes in; the easel's squeaky casters; a pencil scratch for the header; a thunk as the stack lands; a pop for the missile and a pop for the cookie; two ticks as the needle settles; a low rising slide whistle as the headstone comes up; a pop of dirt for the hand.

On screen: "SALARY" / "MORAL STATUS" / "LEGACY" / "CURRENT JOB" / the band "$500,000" / the headstone "HERE LIES SOMEONE WHO MADE ORPHANS". No: no labels at the dial's ends (the missile and the cookie are the labels). Why: the first half of the offer: what the job pays now, and what it costs him.

## Scene 4 · your-offer-column

- id: your-offer-column
- act: The spreadsheet
- transition_in: same form (no seam)
- key: on "rich": both columns full (the same stack in medicine money, the lab, PHILANTHROPIST, the brass plaque), the Lobbyist bolt upright on the couch, the therapist charred black and still writing
- cue: "Your Offer"
- time: 43:40.5 to 43:56.7 (16.2 s)
- voiceover: "Your Offer. The salary is the same, but for lobbying politicians to fund clinical trials instead of cluster bombs. The moral status is "Philanthropist" (but you get to keep the money). The legacy is "Accidentally saved humanity while getting rich"."
- layer: B
- scene: The pencil fills in the right column, YOUR OFFER, in teal, beside the left one.
- wishonia: PiP, happy-smile, then surprised-oh on "moral", then smirk-smile on "Philanthropist", then happy-smile + body-open-palms on "Accidentally"
- props: lobbyist, briefcase, therapist, couch, easel, spreadsheet, pencil, papers-red, papers-teal, lab, bomb, wastebasket, mushroom-cloud, certificate, plaque
- status: outline

Moves: "Your Offer." → the pencil writes "YOUR OFFER" over the right column in teal; the Lobbyist's head swivels back to the sheet. "same," → the left salary stack copies itself across into the right cell, and as it lands every red missile seal flips to a teal cross; the band still says "$500,000". "clinical trials" → a little lab pops up in the right column, its flask bubbling. "cluster bombs." → a little cluster bomb with a lit fuse pops up beside the lab; the pencil crosses it out, then swings like a golf club and whacks it off the sheet; it sails across the room over the couch and drops into the therapist's wastebasket. after "bombs." → the wastebasket goes off: a white flash, a shake and a small mushroom cloud; it clears on the therapist charred black and smoking, glasses askew, the YOU badge still on his lapel, only his eyes blinking. He keeps writing. "Philanthropist" → a framed certificate, "PHILANTHROPIST", with a gold seal, swings into the moral status cell; the Lobbyist puts a gloved hand on his heart. "keep the money" → he pats the briefcase twice and grins under the mask; it burps up one bill. "Accidentally" → a brass plaque screws itself into the legacy cell: "ACCIDENTALLY SAVED HUMANITY WHILE GETTING RICH". "humanity" → it gleams. "rich"." → the Lobbyist sits bolt upright on the couch, the briefcase in his lap, and looks from the headstone to the plaque.

Sound: a pencil scratch for the header; a whoosh as the stack copies across and a sparkle as its seals flip; a pop for the lab and one for the bomb; a scratch for the X; a thunk for the golf swing and a whistle as the bomb flies; a boom from the wastebasket; a bell for the certificate; pats on the briefcase; a clank for the plaque and a sparkle when it gleams; a boing as he sits up.

On screen: "YOUR OFFER" / the band "$500,000" / "PHILANTHROPIST" / the plaque "ACCIDENTALLY SAVED HUMANITY WHILE GETTING RICH". No: no "clinical trials" or "cluster bombs" labels (the lab and the crossed-out bomb are the labels). Why: the same money with a better story, and the Lobbyist sits up.

## Scene 5 · lobbyists-have-clients

- id: lobbyists-have-clients
- act: The sale
- transition_in: cut to a close-up (the briefcase in the Lobbyist's lap)
- key: after "clients.": the open briefcase, the empty BELIEFS slot with the moth flying off, the rolodex stopped on the CURRENT CLIENT card with the Weapons Maker's portrait
- cue: "They won't even need convincing"
- time: 43:56.7 to 44:02.5 (5.8 s)
- voiceover: "They won't even need convincing. Lobbyists don't have beliefs. They have clients."
- layer: B
- scene: Close on the Lobbyist's lap: his gloved hands on the briefcase's latches, his masked face above it; the therapist's charred hand and notebook at the left edge.
- wishonia: PiP, sideeye-closed, then smirk-smile + body-shrug on "clients."
- props: lobbyist, briefcase, rolodex, moth, weapons-maker, clipboard
- status: outline

Moves: "They" → cut to a close-up of the briefcase in the Lobbyist's lap, his gloved hands on the latches; at the left edge the therapist's charred hand holds the notebook open. "convincing." → the charred hand snaps the notebook shut and drops it out of frame; a puff of soot rises from below. "Lobbyists" → the Lobbyist thumbs both latches. "beliefs." → the briefcase pops open: the lid is lined in red velvet, with one slot under a little brass label, "BELIEFS"; the slot is empty, and a moth flutters out of it. The rest of the case is stuffed with war bills. "clients." → a rolodex springs up out of the case on a coil spring and spins, the cards fanning. after "clients." → it clicks to a stop on one card: the CURRENT CLIENT card, the Weapons Maker grinning in its portrait. The Lobbyist taps it with one finger.

Sound: a thunk as the notebook shuts and a huff of soot; a click as the latches pop; a boing as the rolodex springs up and a whirr as it spins; a click as it stops.

On screen: "BELIEFS" (an empty slot) / the card "CURRENT CLIENT". Why: the reason it works: lobbyists follow the client, so you only have to be the better client.

## Scene 6 · two-clients-arithmetic

- id: two-clients-arithmetic
- act: The sale
- transition_in: slide left
- key: on "arithmetic.": the two client cards on a long table, the NEW CLIENT bar 1.43 times the CURRENT CLIENT bar, the Calculator smiling calmly with "1.43" on its cracked display, the Lobbyist (alive again) with his hands over his ears
- cue: "The current client pays"
- time: 44:02.5 to 44:20.7 (18.2 s)
- voiceover: "The current client pays them to lobby for a world where they die of preventable diseases in a smaller economy. You're offering a client that pays the same salary to lobby for a world where they don't die and the economy is one point four three times larger. This is not a hard sell. It is arithmetic."
- layer: B
- scene: A long table with two giant rolodex cards standing on it, CURRENT CLIENT on the left and NEW CLIENT on the right, each with a little Earth and a money-green ECONOMY bar; the color-flip funnel stands between them; the Lobbyist stands in front.
- wishonia: PiP, neutral-smile, then sad-closed on "die", then happy-smile on "don't", then thinking-small + body-counting on "one", then smirk-smile + body-palms-down on "arithmetic."
- props: lobbyist, briefcase, rolodex-card, weapons-maker, therapist, earth-globe, papers-red, papers-teal, calculator, color-flip-funnel
- status: outline

Moves: "current client" → the scene slides in: the CURRENT CLIENT card from the rolodex, now poster size on the table, with its little Earth and its ECONOMY bar; the Lobbyist stands in front of it, briefcase in hand. "pays" → a war bill climbs out of the portrait's frame, walks down the card and hops into the briefcase's funnel. "die" → the Lobbyist's chest light starts blinking red. "diseases" → he x-rays into a grinning skeleton, fedora, mask, gloves and briefcase still on; the card's little Earth frowns. "smaller economy." → the card's ECONOMY bar shrinks. "You're offering" → the NEW CLIENT card slides in on the right: the therapist's charred portrait, still smoking, waving. "same salary" → a medicine bill climbs out of his portrait and waves at the skeleton. "don't die" → the skeleton x-rays back into the Lobbyist, chest light dark; he pats himself down, delighted. "one point four three" → the NEW CLIENT bar grows past the other one and stops at 1.43 times its length; its Earth smiles. "This" → the Calculator walks in along the table from the right, its display cracked, two gaps in its keypad, sweating. "hard" → it looks from one bar to the other, and the Lobbyist tucks the briefcase under his arm and puts his hands over his ears, braced. "sell." → its display reads "1.43". "It" → its mouth starts to open. "arithmetic." → and settles into a calm little smile: no scream. after "arithmetic." → the Lobbyist tosses his briefcase into the color-flip funnel; it shoots out of the spout with a teal cross sticker on its side; he catches it and tiptoes off toward the NEW CLIENT card. The part ends on that frame.

Sound: a pop as the bill drops into the funnel; an x-ray zap on "diseases"; a falling slide whistle as the bar shrinks; a whoosh as the new card slides in; a second zap as he comes back; a rising slide whistle as the new bar grows; squeaky footsteps for the Calculator; a clatter of keys; a ding for the calm; then a whoosh, the funnel's whirr, a pop out of the spout and a squeak of tiptoes.

On screen: "CURRENT CLIENT" / "NEW CLIENT" / "ECONOMY" under each bar / the Calculator "1.43". No: no "1×" or "1.43×" labels on the bars (the Calculator says it); no real company on either card. Why: the conversion is arithmetic, so the payoff is a calm calculator, not a speech.
