---
format: 1920x1080
duration: 2:17.9
message: "Nearly everyone already wants less war and disease; a yes vote by 3.5% of humanity (280 million people) proves it, and paid referral bonuses get it there."
arc: Title card, a finger rings the atom and one running paper turns into medicine money → at the lectern, one click stops the Reaper's scythe and the dial barely twitches → the funnel takes one war bill to the lab and the rest march into the factory → the whole town already agrees, except the Weapons Maker, who gets the paint bucket → nobody opens their bubble first, and an old woman's husband dies beside her with his hand half up → the galaxy's longest game of you-go-first, with headstones → every bubble pops open, the missile chimneys go up as fireworks, and the Weapons Maker's baby goes with them, leaving him its empty bonnet → the lone weird human presses the button and the stadium lights up → the dial asks why → the shelf of history, FAILURES: 0, and the cheat code filed under LATER → 280 million open bubbles beside a field of twerking TV sets → the twerker votes with his hip → the pyramid of Loud Humans blasts the Reaper off the top, and his clipboard lands on the lectern
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 18, "Step 2: The Great Clicking"
audio: index-manual.cbaf659d.mp3, 40:53.0 to 43:10.9
version: v3
---

# Part 18 storyboard: "Step 2: The Great Clicking"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("proving-it: hold the bucket longer"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The part is a 1950s atomic-age instructional film. Layer A is the host's studio set (`KIT.studio`): Wishonia large at her navy lectern, in front of the mustard wall and its spotlight pool. Layer B is six illustrated plates the camera travels over (`KIT.camera`), one framing per phrase: the town-square (four scenes), the planets, the stadium, the history-shelf, the tv-field and the pyramid-hill. Wishonia is not in them; she is the voice. Money is green, and its seal says what it buys: war seals on the parade into the factory, a cross seal on the one bill that comes out of the funnel, plain bills (no seal) for the lifetime income and the referral bonuses. Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Spine.** The shut thought bubbles. Every human in the town square carries one over its head, with the YES button inside. They stay shut in proving-it and pluralistic-ignorance (cracked open for a peek, then snapped shut), all pop open at once in everyone-realizes, the stadium in you-are-everyone shows what was in them (every seat holds the same YES sign), and the 280 million in 280-million are those open bubbles.

**Running gag: the Grim Reaper waits.** Part 5's Reaper, with his tally clipboard, waits for humanity to miss 3.5%. In click-to-not-die his scythe stops an inch from the clerk's neck, but the dial barely twitches, so he leans on his scythe and checks his wristwatch. In you-go-first he holds the VOTE door open like a doorman and taps his watch while the line bows. In referral-pyramid he sits on top of the hill until the pyramid of Loud Humans blasts him off it, and in pyramid-ends his clipboard lands on Wishonia's lectern.

**Shared drawings** (several author groups draw these, so they must match):
- **The YES console.** `KIT.props.yesButton({ label: "YES", sub: "TREATY" })`, drawn at the same scale as the person pressing it (its cap at hand height). click-to-not-die (beside the lectern), you-are-everyone (it rises out of the stage), you-can-get (on the TV screen), and tiny inside every bubble.
- **The 3.5% dial.** `KIT.props.gauge({ mount: "dial", label: "", value: 0, zones: [], marks: [[0.035, "3.5%"]] })` standing on the right end of the lectern's reading top, needle at zero. Its one mark sits barely off zero, which is the joke. click-to-not-die (the needle twitches a hair), why-three-point-five (a question mark springs out of its top on a coil spring), you-can-get and pyramid-ends (the spring holds an exclamation mark).
- **The clerk.** One everyday human, the same options everywhere: `KIT.person({ outfit: "shirt", kind: "twig", tone: 2, color: 1, mood: "worried" })` (rig him with the same options). He presses the button in click-to-not-die, stands second in line in you-go-first, and is the lone human in you-are-everyone.
- **The old woman.** An everyday human, not the cast's Grandma (Grandma died in Part 17 and is a skeleton from then on): `KIT.person({ outfit: "dress", kind: "hourglass", hair: 1, hairStyle: "bun", hairColor: "#E8E4DA", tone: 3, color: 0, mood: "smile", build: { hunch: 10, legs: 0.82 } })`, a white bun, no curlers, no cat-eye glasses, no apron and no poster. Front row of the town square beside her husband; first in line in you-go-first.
- **The thought bubble.** A cream cloud (8 to 10 sharp facets, thin navy outline, three trailing puffs down to the head) with a lid seam across its middle. Shut, it is plain cream with halftone dots; cracked or open, its top half flips up like a lid and a tiny YES console glows inside. The town square's bubbles, the old woman's, the economist's and the dots of 280-million.
- **The Grim Reaper.** `KIT.reaper()` with `KIT.props.clipboard` (navy tally marks in fives, as in Part 5) and a wristwatch drawn on his wrist bone (a cream face, a navy strap).
- **The baby's bonnet.** In this part the Weapons Maker's smiling missile wears a frilly cream baby bonnet over its nose cone, tied with an orange ribbon. It stays on the missile through proving-it (paint and all) and is all he has left in everyone-realizes.

**The town-square plate** (the-question, proving-it, pluralistic-ignorance, everyone-realizes; a plain tan field under a cream sky). Two levels:
- The back street, its cobbles at the top of the plate: three war factories side by side (`KIT.props.factory({ label: "" })`, missile chimneys puffing), their loading doors on the street, the right-hand factory's door rolled open. The color-flip funnel (`KIT.props.colorFlipFunnel`) stands at the back edge of the street just left of that door. Past the last factory, the Scientist (`KIT.cast("scientist")`) at her lab bench (`KIT.props.lab`).
- The square in front of the street: the crowd, about 24 everyday humans of every build (shirts, dresses, suits, overalls; `seed` picks each one) in three rows facing the camera, each under a shut bubble. the old woman (Shared drawings) in the front row left of center with her husband (a bald everyday human with glasses) beside her; the Weapons Maker (`KIT.cast("weaponsMaker")`, hard hat, cigar, cradling his smiling missile in its bonnet) in the back row, right of center, where his barrel chest shows over the rows in front; the economist (an everyday human in a suit with a bow tie, horn-rims and a pipe, a magnifying glass and a clipboard) at the right end of the front row. At the right edge of the square, a blank brick wall as tall as a factory, the painter's tall ladder leaning on it with a paint bucket on its top step.
- Continuity: from proving-it's end on, "SUPP" is painted across the wall, the ladder lies across the square and the Weapons Maker wears the bucket and drips orange paint; from pluralistic-ignorance's end on, the old woman's husband is a skeleton.

**Callbacks.** From Part 5: the Grim Reaper and his tally clipboard; the Loud Humans (megaphones for heads) in referral-pyramid. From Part 2 (money-loop): the war factory with its grinning missile chimneys, and the war money marching into its door. From Part 1: the seal flip (style bible, gag 2) on the title card and at the funnel; the skeleton x-ray. Inside the part: the dial's question mark in why-three-point-five is an exclamation mark from you-can-get on, the tiny bubbles of 280-million are the open bubbles of everyone-realizes, and the TV set on the lectern in you-can-get comes from the tv-field.

**Set up here.** The YES console is the button the later parts come back to: in Part 24 (your-job) it springs up out of the lectern for YOU to press; in Part 25 (dont-know-what-to-tell-you) it stands on its console beside the lectern while busy humans walk past it; in Part 27 (personally-to-blame) it is the size of a fire hydrant. Draw it from click-to-not-die.

**Held frame.** None: this part states no death toll.

**Transitions.** The title card comes up from black and goes down to black; click-to-not-die irises in on Wishonia's face. Cuts between the set and the plates. proving-it and pluralistic-ignorance continue the-question's plate with no seam, the camera still traveling; everyone-realizes cuts back to the same plate. pyramid-ends irises out on her face to black, so Part 19's title card comes up from black.

**Bans for this part.**
- The ballot question is never written out, on any card, sign or screen: the funnel in the-question shows it.
- Erica Chenoweth is a name on a nameplate, never a face; the app is never shown or named (the TV sets carry the joke).
- Draw each framing large: one station fills the frame, with the ground and the cast big, except where the Moves say the camera pulls back.

## Changes from v2

- Wishonia's office, the engraved paper and her corner (PiP) are gone. She is on screen at her lectern in four host shots: click-to-not-die (the step's first line, with the clerk and the Reaper as her guests), why-three-point-five (new), you-can-get (new) and pyramid-ends (new; the part ends on an iris out). Everything else is six plates.
- The labels that explained the picture are cut and their jokes restaged: no ballot card (the funnel shows the question), no tally board rows (the painter gets as far as "SUPP" and counts heads instead), no dictionary card and arrow (the economist who names the effect hides his own bubble), no WEIRD? label (a dunce cap), no app placard (the TV screens show the twerk), no REFERRAL BONUSES sign (a price tag), no NOT DYING sign (the megaphones blast the Reaper off the top).
- The title card is the period card. Its gag: a finger rings the atom's nucleus like a doorbell and one of its running papers flips to a cross seal. Part 17's five doors are not used.
- The 3.5% dial is a lectern prop that carries through the part: a twitch at the clerk's click, a question mark on "Why", an exclamation mark after the shelf.
- "Eight billion" no longer pulls back onto a small Earth (you-go-first keeps that move): heads under shut bubbles pop up in every window and on every roof of the square. cheat-code is now the end of chenoweth-shelf, one travel along the same shelf.
- New jokes: the ladder falls across the crowd like a felled tree, the skeleton's jaw drops off when the bubbles open, the stamp hops down the shelf stamping WON, the tiny twerker votes YES with his hip.

## Scene 1 · step-2-great-clicking-title

- id: step-2-great-clicking-title
- act: Title
- transition_in: up from black (the head of a reel)
- key: a beat after "Clicking.": the whole heading on the navy card, a finger from the top edge pressing the atom's nucleus, one of the three running papers stopped at the top of its orbit, looking down at the new cross on its seal
- cue: "Step 2: The Great Clicking"
- time: 40:53.0 to 40:56.1 (3.1 s)
- voiceover: "Step 2: The Great Clicking."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem with its three running war-seal papers, the heading under it. Heading lines, 16:9: "STEP 2:" (style small) / "THE GREAT CLICKING"; 9:16: "STEP 2:" (style small) / "THE GREAT" / "CLICKING". Each heading word fades in on its spoken word. The small gag: a human finger in a shirt cuff pokes down from the top edge and rings the orange nucleus like a doorbell.
- props: title-card, money (war, med), hand
- status: planned

Moves: "Step" → the card comes up from black, the emblem's papers already running; "STEP 2:" fades in on "Step" and "2:". "The" → "THE GREAT" fades in on its words. "Great" → a finger in a shirt cuff pokes down from the top edge toward the nucleus. "Clicking." → "CLICKING" fades in, and the finger presses the nucleus: it clicks in and pops back out, and the finger pulls back up out of the frame. A beat later → the paper passing the top of its orbit flips its missile seal to a cross, skids to a stop, looks down at itself, and runs on after the other two. The card goes down to black in its last quarter second.

Sound: a projector whirr from "Step"; a click as the finger presses on "Clicking."; a sparkle as the seal flips, a beat later.

On screen: "STEP 2: THE GREAT CLICKING". Why: the narrator reads the heading, and a click that turns a running war paper into medicine money is the step in one picture.

## Scene 2 · click-to-not-die

- id: click-to-not-die
- act: The button
- transition_in: iris in on her face
- key: on "Die": beside the lectern, the Grim Reaper's scythe stopped an inch from the clerk's neck, the YES button's cap just popped back up under the clerk's finger, Wishonia smirking at the camera
- cue: "Make Humans Click a Button"
- time: 40:56.1 to 41:03.5 (7.4 s)
- voiceover: "Make Humans Click a Button to Not Die You need three point five percent of humanity to vote yes on:"
- layer: A, host
- scene: The host's set (`KIT.studio`). The 3.5% dial stands on the right end of the lectern's reading top, needle at zero. On the free wall right of the lectern, the guests: the YES console standing on the floor beside the lectern, and the clerk at it, facing left toward it and her. The Grim Reaper waits out of sight below the frame behind the clerk, his clipboard under his arm.
- wishonia: big, happy-smile + body-presenting; smirk-smile + body-idle on "Die"; lookright-smile + body-point-right on "five"; skeptical-smile + body-hands-hips on "yes"
- props: studio, lectern, gauge (dial), yes-button, human (the clerk), reaper, clipboard, wristwatch
- status: planned

Moves: "Make" → the iris opens on her face while she presents (in the first 0.7 s), and the camera pushes in slowly for the whole shot, keeping the guests in frame (1 to 1.04). "Click" → the clerk presses the button with one finger: it clicks down and pops back. "Button" → behind him, the Grim Reaper rises up into the shot, scythe raised over the clerk's neck. "Not" → the scythe swings. "Die" → it stops an inch from his neck. after "Die" → the Reaper checks his clipboard, scowls and rubs out one tally mark; the clerk never notices. "five" → Wishonia points at the dial on her lectern: its needle twitches a hair off zero, and its 3.5% mark is barely past that. "humanity" → the Reaper sees the dial, grins, plants his scythe, leans on it and checks his wristwatch. "vote" → the clerk presses again, harder, twice; the needle does not budge. "yes" → the Reaper taps his watch at the camera.

Sound: a click on "Click"; a whoosh as the scythe swings on "Not"; a record scratch as it stops on "Die"; a tick as the needle twitches on "five"; a click on "vote"; a tick from the watch on "yes".

On screen: "YES" and "TREATY" (the button), "3.5%" (the dial's one mark). No: no heading banner, no "Needed: 3.5%" label; the dial says it. Why: she opens the step to the viewer: one click saves one human for a moment, and 3.5% of humanity is a mark barely off zero that one click cannot reach.

## Scene 3 · the-question

- id: the-question
- act: The button
- transition_in: cut
- key: after "trials?": the one medicine bill standing on the Scientist's bench, every flask boiling over, a pill bottle popped up out of the beaker like toast; beside it the line of war money still filing into the factory door
- cue: "Should your country redirect"
- time: 41:03.5 to 41:08.7 (5.3 s)
- voiceover: ""Should your country redirect one percent of military spending to fund clinical trials?"."
- layer: B, plate town-square
- scene: The town-square plate's back street: a long line of war money (`KIT.money("war")`) marching left to right along the cobbles into the open door of the right-hand factory, the color-flip funnel standing beside the line just before the door, and the Scientist at her lab bench past the last factory.
- props: money (war, med), factory, color-flip-funnel, lab, scientist, pill-bottle
- status: planned

Moves: "Should" → on the back street: the line of war bills marching along the cobbles, out of the left of the frame and into the factory door on the right, the missile chimneys puffing. "redirect" → the camera pushes in on the funnel: its mouth turns toward the line. "one" → it sucks exactly one bill up out of the line, fwoop, legs kicking. "percent" → the other bills march on into the factory without looking up, and its chimneys give a smug puff. "spending" → the funnel's box rattles. "fund" → out of its spout walks the same bill with a cross seal; the camera travels right with it, past the factory door the others are filing into, to the lab bench. "trials?" → it hops onto the bench beside the Scientist (`KIT.cast("scientist")` at `KIT.props.lab`): every flask boils over at once, and a pill bottle (`KIT.props.pillBottle`) pops up out of the beaker like toast.

Sound: a whoosh as the funnel sucks up the bill on "one"; a whirr as the box rattles on "spending"; a sparkle as the seal comes out flipped on "fund"; a toaster pop at the lab on "trials?".

On screen: nothing but the money, the funnel and the lab. No: no ballot card and no question written out; the factory has no sign. Why: the whole referendum in one move: one bill in the line goes to the lab, and the rest of the war money does not even notice.

## Scene 4 · proving-it

- id: proving-it
- act: Everyone already agrees
- transition_in: same plate (no seam)
- key: on "supports": the whole crowd mid-nod, every hat in the air, the Weapons Maker and his missile shaking their heads, "SUPP" painted on the wall at the right and the painter stopped on his ladder, brush in the air
- cue: "You are not creating"
- time: 41:08.7 to 41:22.4 (13.6 s)
- voiceover: "You are not creating support for not dying of horrible diseases and not mass murdering each other. Nearly everyone already supports not dying of horrible diseases and not mass murdering each other. You are proving it."
- layer: B, plate town-square
- scene: The same plate, down in the square: the crowd under its shut bubbles, the wall at the right with the painter (an everyday human in overalls, a barrel build) up his ladder.
- props: human (crowd, painter), thought-bubble, weapons-maker, missile, bonnet, ladder, paint bucket, clipboard
- status: planned

Moves: "You" → the camera leaves the lab and drops down into the square: the crowd, every bubble shut, the Weapons Maker in the back row cradling his missile in its bonnet. "creating" → the camera moves to the wall: the painter up his ladder paints big drippy letters across it, "S", "U", "P", "P". after "other." (first) → he stops, brush in the air, and looks down over his shoulder at the crowd. "Nearly" → the camera pulls back to take in the crowd and the wall. "supports" → every human nods once, all together, so hard that every hat hops up and lands again; in the middle, the Weapons Maker shakes his head, and the missile in his arms shakes its head too. "murdering" (second) → the missile crosses its arms and scowls. "proving" → the painter drops his brush, pulls a clipboard out of his overalls and climbs down; the ladder tips away from the wall and falls across the crowd like a felled tree, everyone ducking. "it." → the bucket from its top step lands upside down on the Weapons Maker's head: splat, orange paint running down him and his missile. after "it." → the painter walks along the front row counting heads with his pencil, tap, tap, tap.

Sound: a marker scrub as he paints on "creating"; a record scratch as he stops, after "other."; a thunk on the nod and pats as the hats land on "supports"; a squeak as the missile crosses its arms; a whoosh as the ladder falls on "proving"; a splat on "it.".

On screen: "SUPP" on the wall. No: no percentages and no tally board; the nod is the count. Why: the vote does not change minds; it counts minds already made up, and the only holdout is the one holding the missile.

## Scene 5 · pluralistic-ignorance

- id: pluralistic-ignorance
- act: Everyone already agrees
- transition_in: same plate (no seam)
- key: on "permission": the front row with every hand half raised, cobwebs strung between them, the old woman's husband beside her a grinning skeleton with his hand still half up, every bubble shut
- cue: "Everyone thinks this is crazy"
- time: 41:22.4 to 41:35.8 (13.4 s)
- voiceover: "Everyone thinks this is crazy because everyone else thinks this is crazy. Your economists call it pluralistic ignorance, which is the polite term for eight billion people waiting for permission to want what they already want."
- layer: B, plate town-square
- scene: The same square and crowd. The old woman peeks into her bubble, glances at her neighbors and snaps it shut; then everybody does the same, the economist who names it included.
- props: human (crowd, economist, the old woman, her husband), thought-bubble, yes-button (inside the bubbles), magnifier, xray, cobweb, stamped number
- status: planned

Moves: "Everyone" → the first frame is proving-it's last: the painter counting heads, the ladder across the square, the Weapons Maker dripping paint under his bucket. "crazy" (first) → close on the old woman in the front row: she cracks her bubble's lid open, and the YES button glows inside. "else" → her eyes slide left, then right: every other bubble is shut. after "else" → she snaps hers shut and whistles at the sky. "crazy." (second) → the camera pulls back on the rows: every bubble cracks open at once, every head glances left and right, and they all snap shut again in a ripple across the square. "economists" → the camera travels to the right end of the front row: the economist studies the crowd through his magnifying glass, nodding, and notes it on his clipboard. "polite" → he tips his hat to the camera. "term" → then he cracks his own bubble open, glances left and right, and snaps it shut too. "eight billion" → the camera pulls back over the whole plate while heads under shut bubbles pop up everywhere: in every factory window, on every roof, astride the missile chimneys, out of the funnel's mouth, until the square is packed to its edges, and "8,000,000,000" stamps into the sky. "waiting" → the extra heads duck back out of sight, and the camera drops into the front row: every human raises a hand halfway and waits, like a class waiting to be called on. "permission" → cobwebs string between the raised hands, and her husband beside her x-rays into a grinning skeleton, hand still half up. "already" → every bubble flickers open for one frame, every one with the YES button inside, the skeleton's too. after "want." (second) → they snap shut.

Sound: a squeak as the old woman's lid cracks on "crazy" and a pop as she snaps it shut, after "else"; a ripple of pops on "crazy."; a pop as the economist snaps his shut on "term"; pops as the heads pop up and a stamp thump as the number lands on "billion"; crickets while they wait on "waiting"; a zap for the x-ray on "permission"; a sparkle for the flicker on "already".

On screen: "8,000,000,000". No: no definition written anywhere; the crowd is the definition. Why: names the real obstacle, which is silence, not disagreement, and the expert who names it is doing it too.

## Scene 6 · you-go-first

- id: you-go-first
- act: Everyone already agrees
- transition_in: cut
- key: on "finish": the five other planets dark, a tiny headstone on each, their tiny lines skeletons still bowing; Earth still lit in the middle, its line still bowing at its door
- cue: "It is the galaxy's longest"
- time: 41:35.8 to 41:44.2 (8.4 s)
- voiceover: "It is the galaxy's longest game of you-go-first. Most species that start playing it don't finish playing it."
- layer: B, plate planets
- scene: A plate of navy night sky with mustard stars. In the middle, a small Earth (`KIT.props.earthGlobe`), with a little grassy hill on its top and a door on the hill (`KIT.props.door({ label: "VOTE" })`), the Grim Reaper holding it open like a doorman, and a line of humans winding down the hill in front of it: the old woman first, the clerk second, everyday humans behind. Around it in the sky, five other small planets in the palette's colors (rust, slate, tan, orange, mustard), each with its own tiny door and its own tiny line.
- props: door, reaper, wristwatch, human (the old woman, the clerk, the line), earth-globe, planets, headstone, skeleton
- status: planned

Moves: "galaxy's" → close on the door on its hill; the Reaper holds it open, bowing like a doorman. "longest" → the line fills in down the hill: the old woman first, then the clerk, then everyday humans out of the frame. "you-go-first." → every human bows and waves the one behind it ahead, all at once, so nobody moves. A beat later → the Reaper taps his wristwatch. "Most" → the camera pulls back: the hill is the top of a small Earth hanging in the night sky among five other little planets, each with a tiny door and a tiny bowing line. "finish" → the other planets go dark one by one, a tiny headstone (`KIT.props.headstone`) popping up on each; their tiny lines are skeletons now, still bowing. after "it." (last) → only Earth is lit, its line still bowing; its tiny Reaper looks up at the camera and taps his watch.

Sound: soft pats for the bows on "you-go-first."; a tick from the watch a beat later; a whoosh for the pull-back on "Most"; a switch as the planets go dark and a thunk for the headstones on "finish"; a last tick, after "it.".

On screen: "VOTE" on the door. Why: the price of nobody going first, as a dark joke: the other players are already dead.

## Scene 7 · everyone-realizes

- id: everyone-realizes
- act: The moment they find out
- transition_in: cut
- key: after "unrecognizable.": every bubble open with its tiny smiling Earth and its stack of plain bills, the missiles bursting into fireworks over the hospitals where the factories stood, his own orange-spattered one among them, and the paint-spattered Weapons Maker under his "+$518,879" tag holding its empty bonnet
- cue: "If every human realized"
- time: 41:44.2 to 41:59.9 (15.8 s)
- voiceover: "If every human realized that nearly every other human would like a world without war and disease and an extra five hundred and eighteen thousand, eight hundred and seventy-nine dollars in lifetime income, it would be done tomorrow and the world would be unrecognizable."
- layer: B, plate town-square
- scene: Back on the town-square plate, as pluralistic-ignorance left it: every bubble shut, the husband's skeleton beside the old woman, the Weapons Maker under his bucket cradling his bonneted missile, "SUPP" on the wall, the factories behind. A tear-off desk calendar (`KIT.props.calendar`) hangs on a nail on the wall above "SUPP".
- props: human (crowd), thought-bubble, weapons-maker, missile, bonnet, earth-globe, money (plain), price-tag, calendar, stamp-mark, factory, hospital, fireworks
- status: planned

Moves: "If" → the square again, every bubble shut. "realized" → every bubble pops open at once, with a bang that blows every hat off. "human" (second) → every head turns slowly to its neighbors' bubbles: the same YES button in every one; jaws drop, and the skeleton's jaw drops clean off. "without" → every YES button turns into a tiny smiling Earth (`KIT.props.earthGlobe({ face: "smile" })`). "thousand," → a fat stack of plain green bills thumps into every bubble beside its Earth. "dollars" → a price tag swings out from the Weapons Maker's own stack: "+$518,879"; under his bucket, his eyes go wide. "done" → on the wall, the calendar's page tears off by itself. "tomorrow" → a stamp mark slams onto the next page: "DONE". "world" (second) → the missile chimneys on every factory blast off into the sky, and the baby missile in the Weapons Maker's arms wriggles out of its bonnet and blasts off after them, trailing orange paint drips. "unrecognizable." → the factories fold flat and pop back up as hospitals (`KIT.props.hospital`). after "unrecognizable." → the missiles burst high overhead as fireworks, his among them in an orange-spattered burst; he looks down at the empty bonnet in his arms, then up at the sky, and waves the bonnet after it like a hankie.

Sound: pops as the bubbles burst open on "realized"; a falling slide whistle as the jaws drop; a thunk for the stacks on "thousand,"; a cash-register ding for the tag on "dollars"; a stamp thump on "tomorrow"; an airplane roar as the missiles launch on "world"; pops and a sparkle for the fireworks, after "unrecognizable.".

On screen: "+$518,879" (the tag) / "DONE" (the stamp). No: no signs on the factories or the hospitals. Why: what happens when everyone learns what everyone else wants, and where the missiles go.

## Scene 8 · you-are-everyone

- id: you-are-everyone
- act: The moment they find out
- transition_in: cut
- key: on "everyone.": the floodlights just banged on, every seat in the huge stadium holding up the same YES sign, the dunce cap blowing off the clerk's head beside the YES console
- cue: "Right now every human"
- time: 41:59.9 to 42:10.7 (10.7 s)
- voiceover: "Right now every human who wants less war and disease assumes they are the weird one. The referendum is the moment they find out they are everyone."
- layer: B, plate stadium
- scene: A huge stadium seen from its stage: a plain slate stage at the bottom middle, tier after tier of seats rising to the top of the frame, banks of floodlights on towers along the rim. Every seat holds an everyday human with a small YES sign on a stick, all unseen in the dark until the lights come on.
- props: human (the clerk, the crowd), sign, yes-button, spotlight, floodlights, dunce cap
- status: planned

Moves: "Right" → a dark stage; a spotlight clunks on over the clerk, alone, holding up a small sign on a stick: "YES". "assumes" → he peers out into the dark, sweating. "weird" → a dunce cap drops out of the dark onto his head. after "one." → he lowers the sign and hides it behind his back. "referendum" → the YES console rises out of the stage beside him. "moment" → he looks at it and gulps. "find" → he presses it. "everyone." → the floodlights bang on, bank after bank: every seat in the huge stadium holds a human with the same YES sign, and the dunce cap blows off his head. after "everyone." → the crowd pours down onto the stage, lifts him overhead and crowd-surfs him away, sign up.

Sound: a switch and a low hum for the spotlight on "Right"; crickets in the dark on "assumes"; a falling slide whistle for the dunce cap on "weird"; a rising slide whistle for the console on "referendum"; a click on "find"; a slam for the light banks and a boom for the roar on "everyone."; a whistle as he goes up, after "everyone.".

On screen: "YES" on every sign. Why: the turn of the step; the vote shows people they are not alone.

## Scene 9 · why-three-point-five

- id: why-three-point-five
- act: Why 3.5%
- transition_in: cut
- key: after "percent?": a question mark sprung out of the top of the dial on a coil spring, still bobbing, Wishonia raising a brow at the camera
- cue: "Why three point five percent?"
- time: 42:10.7 to 42:13.1 (2.4 s)
- voiceover: "Why three point five percent?"
- layer: A, host
- scene: The host's set, the 3.5% dial on the right end of the lectern, its needle still a hair off zero from click-to-not-die.
- wishonia: big, thinking-closed + body-thinking; lookright-smile + body-point-right on "five"; skeptical-smile + body-hands-hips on "percent?"
- props: studio, lectern, gauge (dial), question mark on a spring
- status: planned

Moves: "Why" → back at the lectern; the camera pushes in slowly. "five" → she looks over at the dial and points at it. "percent?" → a question mark springs out of the top of the dial on a coil spring, boing, and bobs; she turns back and raises a brow at the camera.

Sound: a boing on "percent?".

On screen: "3.5%" on the dial, and the question mark. Why: she asks the viewer the question the dial has been asking since the clerk's click.

## Scene 10 · chenoweth-shelf

- id: chenoweth-shelf
- act: Why 3.5%
- transition_in: cut
- key: after "purpose.": the drawer marked LATER under the end of the shelf under a drift of dust, its label yellowed and curling, a tumbleweed rolling past on the floor; above it the brass bookend, "ERICA CHENOWETH" on its nameplate and "FAILURES: 0" in its counter
- cue: "A political scientist named"
- time: 42:13.1 to 42:40.9 (27.9 s)
- voiceover: "A political scientist named Erica Chenoweth studied every major political movement of the last century and found that none had ever failed after achieving three point five percent active participation. Not one. Every civil rights movement, every revolution, every regime change. Hit three point five percent and you win. Humanity discovered the cheat code for changing its own civilization and then never used it on purpose."
- layer: B, plate history-shelf
- scene: One long plate: a wooden shelf on brackets runs left to right across a mustard library wall for several frames, packed with history books whose spines are rust, navy, slate, tan and orange, each with a year in Oswald, 1900s at the left to 2000s at the right. At its right end stands a brass bookend with a nameplate and a counter window under it. Under the last stretch of shelf, a small wooden card drawer with an empty label holder. A plank floor below, for the splat and the tumbleweed.
- props: shelf, books, bookend, counter, stamp, stamp-mark, tiny marchers, tiny cannon, crown, rich-human (tiny), bell, confetti, card, drawer, human (suit), tumbleweed
- status: planned

Moves: "political" → on the shelf's right end, empty. "Chenoweth" → a brass bookend slides in along the shelf and lands at its end; its nameplate reads "ERICA CHENOWETH". "studied" → the camera travels left along the shelf, past book after book, each spine with its year. "found" → a rubber stamp (`KIT.props.stamp`) hops up onto the books at the left. "failed" → it hops back along the shelf from book to book, stamping every spine as it goes, thump, thump, thump, faster and faster: "WON". "participation." → it reaches the bookend and stops, out of books. "Not one." → the camera pushes in on the bookend's counter: it clicks round and lands on "FAILURES: 0". "rights" → the camera pulls back: one book tips forward, and a tiny crowd marches out of it along the shelf with tiny signs. "revolution," → the next book tips, and a tiny cannon rolls out and fires a confetti ball. "regime" → the next book tips, and a tiny crown rolls out. "change." → a tiny fat cat (`KIT.cast("richHuman")`, small) chases the crown off the edge of the shelf. after "change." → splat, somewhere below. "win." → a boxing bell over the shelf rings, and confetti falls. "Humanity" → the camera travels back to the last book before the bookend. "discovered" → it glows. "cheat" → a card slides up out of its pages. "code" → it stands up with a game-show ding: "3.5%". "civilization" → an everyday human in a suit (a refrigerator box) walks in under the shelf, plucks the card, reads it and nods, impressed. "never" → he files it in the drawer under the shelf, slides a "LATER" label into its holder, slams it and walks off. "purpose." → time passes in one beat: dust piles on the drawer, its LATER label yellows and curls, and a tumbleweed rolls past on the floor.

Sound: a thunk as the bookend lands on "Chenoweth"; stamp thumps as the stamp hops on "failed"; a tick as the counter lands on "Not"; a pop for the confetti cannon on "revolution,"; a falling slide whistle as the fat cat goes over on "change." and a splat after it; a bell on "win."; a ding on "code"; a slam for the drawer on "never"; crickets on "purpose.".

On screen: the years on the spines / "ERICA CHENOWETH" / "WON" / "FAILURES: 0" / "3.5%" (the card) / "LATER". No: the researcher is a name only, never a drawn face; no "3.5%?" card. Why: the evidence that 3.5% is enough, and the punchline on it: humans had the answer and filed it.

## Scene 11 · 280-million

- id: 280-million
- act: 280 million
- transition_in: cut
- key: on "twerk.": the small field of open bubbles bouncing beside the field ten times bigger of wiggling TV sets, every screen showing the same tiny wiggling human, the ground shaking, "280,000,000" in the sky
- cue: "That's two hundred and eighty million"
- time: 42:40.9 to 42:52.0 (11.0 s)
- voiceover: "That's two hundred and eighty million humans. Sounds like a lot until you remember that more than ten times as many of you downloaded TikTok to watch people twerk."
- layer: B, plate tv-field
- scene: A plain tan field under a cream sky, flat to a low horizon. On the left, a square patch packed with tiny open thought bubbles, each with its tiny YES button. On the right, beside it, a field ten times bigger packed with tiny 1950s TV sets (`KIT.props.tvSet`) on splayed legs, rabbit ears up, in rows back to the horizon. The number stands in the sky, fixed to the screen.
- props: thought-bubble (tiny), yes-button (tiny), tv-set, stamped number
- status: planned

Moves: "two" (first) → the small field fills in, row by row from the front: tiny open bubbles from everyone-realizes, each with its YES button. "humans." → "280,000,000" stamps into the sky over it. "Sounds" → the camera pulls back until the field is a small patch on the plain. "ten" → a field ten times bigger draws in beside it, rows of tiny TV sets back to the horizon. "downloaded" → every screen flickers on. "people" → every screen shows the same tiny human wiggling its hips. "twerk." → the whole field of TVs wiggles with it, in step, so hard the ground quakes, the rabbit ears flap and the small field's bubbles bounce; a TV at the front topples over, still wiggling.

Sound: pops as the field fills on "two"; a stamp thump on "humans."; a slide whistle up as the big field draws in on "ten"; a switch as the screens come on on "downloaded"; a boing and a boom for the quake on "twerk.".

On screen: "280,000,000". No: the app is never named or drawn: no logo, no phones, no placard. Why: makes 280 million feel small.

## Scene 12 · you-can-get

- id: you-can-get
- act: 280 million
- transition_in: cut
- key: on "yes": on the little TV set on the lectern, the tiny twerker bumping the YES button with his hip, its cap pressed down; Wishonia presenting it with open palms, the dial's exclamation mark on its spring
- cue: "You can get two hundred"
- time: 42:52.0 to 42:56.5 (4.5 s)
- voiceover: "You can get two hundred and eighty million to vote yes or no on the treaty."
- layer: A, host
- scene: The host's set: one TV set from the tv-field stands on the left end of the lectern, its tiny human still wiggling on the screen; the dial on the right end, an exclamation mark on its spring now where the question mark was.
- wishonia: big, smirk-smile + body-presenting; happy-smile + body-open-palms on "vote"; smirk-closed + body-idle on "treaty."
- props: studio, lectern, tv-set, yes-button (on the screen), gauge (dial), exclamation mark on a spring
- status: planned

Moves: "You" → back at the lectern: the little TV on its left end, its tiny human still wiggling his hips. "get" → she presents it to the camera. "vote" → its picture flips like a channel change, and the YES console now stands on the screen beside the tiny human, who keeps wiggling. "yes" → his hip bumps the button: click, its cap goes down. "treaty." → the TV's rabbit ears shoot straight up; she smirks at the camera.

Sound: a switch for the channel change on "vote"; a click on "yes"; a boing for the rabbit ears on "treaty.".

On screen: "YES" on the button. Why: the verdict to the viewer: the same humans, doing the same thing, can vote.

## Scene 13 · referral-pyramid

- id: referral-pyramid
- act: 280 million
- transition_in: cut
- key: on "dying": the pyramid of Loud Humans stacked up the hill, every megaphone blasting at the top, the Grim Reaper blown off his rock, scythe and clipboard flying
- cue: "Two hundred and fifty million dollars"
- time: 42:56.5 to 43:08.8 (12.3 s)
- voiceover: "Two hundred and fifty million dollars of the campaign budget goes to paid referral bonuses that make sharing their link to vote financially attractive. It's a pyramid scheme where the thing at the top of the pyramid is not dying from"
- layer: B, plate pyramid-hill
- scene: A tan field under a cream sky. On the left, open ground where a pile of plain bills lands, and a row of everyday humans standing in line toward the right. On the right, a steep rust-and-tan hill rising high above the field, a rock on its top where the Grim Reaper sits, its far side dropping away out of the right of the plate.
- props: money (plain), price-tag, human (the row), loud-human, ticket, reaper, clipboard, wristwatch
- status: planned

Moves: "Two" → a pile of plain green bills thumps down on the left; high on the hill, the Grim Reaper sits on his rock, checking his watch. "dollars" → a price tag swings out of the pile: "$250,000,000". "referral" → bills hop off the pile and walk to the row of humans. "sharing" → the first human hands a small ticket marked "VOTE" (the link) to the next; a bill hops into the giver's hand, and the giver's head turns into a megaphone, blasting (`KIT.cast("loudHuman")`, as Part 5's Loud Humans). "link" → the next one passes it on: another bill, another megaphone; it runs down the row faster and faster. "attractive." → the Loud Humans climb onto each other's shoulders. "pyramid" (first) → they stack into a human pyramid at the foot of the hill, every megaphone blasting. "top" → the pyramid grows up the hill, and the camera tilts up after it until its top Loud Human is nose to skull with the Reaper. "pyramid" (second) → the Reaper looks down at it and taps his watch. "not" → every megaphone in the pyramid turns to the Reaper and blasts at once. "dying" → the blast blows him off his rock. "from" → he tumbles down the far side and out of the picture, scythe and clipboard flying.

Sound: a thunk for the pile on "Two"; a cash-register ding for the tag on "dollars"; a pop as the first head turns into a megaphone on "sharing" and another on "link"; pats as they climb on "attractive."; a yelp as he is blown off on "dying"; a falling slide whistle for the tumble on "from".

On screen: "$250,000,000" (the tag) / "VOTE" (the ticket). No: no sign on the pile or at the top of the pyramid. Why: how the 280 million get there: sharing pays, so everyone becomes the Loud Human, and the thing at the top of this pyramid is the one who knocked the Reaper off it.

## Scene 14 · pyramid-ends

- id: pyramid-ends
- act: 280 million
- transition_in: cut
- key: on "diseases.": the Reaper's tally clipboard just landed face up on the lectern in front of Wishonia, a loose tally mark still fluttering down, Wishonia smirking at the camera
- cue: "preventable diseases."
- time: 43:08.8 to 43:10.9 (2.1 s)
- voiceover: "preventable diseases."
- layer: A, host
- scene: The host's set: the TV set on the left end of the lectern, its ears still up, the dial with its exclamation mark on the right end, and the middle of the reading top clear.
- wishonia: big, happy-smile + body-presenting; smirk-smile + body-idle on "diseases."
- props: studio, lectern, tv-set, gauge (dial), clipboard
- status: planned

Moves: "preventable" → back at the lectern, she presents to the camera; from below the frame, a distant splat: the Reaper has landed. "diseases." → his tally clipboard flutters down from the top of the frame and lands face up on the lectern in front of her; she smirks at the camera. after "diseases." → the film irises out on her face, to black.

Sound: a splat a beat after "preventable" starts; a falling slide whistle as the clipboard falls and a thunk as it lands on "diseases.".

On screen: the tally marks on the clipboard. Why: the part ends on the host, holding the Reaper's count.
