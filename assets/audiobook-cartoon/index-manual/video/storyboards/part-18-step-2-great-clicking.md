---
format: 1920x1080
duration: 2:17.9
message: "Nearly everyone already wants less war and disease; a yes vote by 3.5% of humanity (280 million people) proves it, and paid referral bonuses get it there."
arc: Title card, door 2 springs out the YES button → one click stops the Reaper's scythe, the needle barely moves, 1 bill in 100 comes out teal → everyone already agrees (except the Weapons Maker) → nobody opens their bubble first → the galaxy's longest game of you-go-first, with headstones → every bubble pops open and the missile chimneys go up as fireworks → the lone weird human presses the button and the stadium lights up → the shelf of history, FAILURES: 0 → the cheat code filed under LATER → 280 million open bubbles beside a field of twerking TV sets → the referral pyramid of Loud Humans bumps the Reaper off the top
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 18, "Step 2: The Great Clicking"
audio: index-manual.cbaf659d.mp3, 40:53.0 to 43:10.9
version: v2
---

# Part 18 storyboard: "Step 2: The Great Clicking"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The closed thought bubbles. Every human in the crowd carries one with the YES button inside. They stay shut in proving-it and pluralistic-ignorance (cracked open for a peek, then snapped shut), all pop open at once in everyone-realizes, the stadium in you-are-everyone shows what was in them (every seat holds the same sign), and the 280 million dots in 280-million are those open bubbles.

**Running gag: the Grim Reaper waits.** Part 5's Reaper, with his tally clipboard, is waiting for humanity to miss 3.5%. In click-to-not-die one click stops his scythe, but the needle barely moves, so he sits down on the console and checks his wristwatch. In you-go-first he holds the REFERENDUM door open like a doorman and taps his watch while the line bows. In referral-pyramid the pyramid of Loud Humans grows up his hill, and the sign at its top pokes him off.

**Shared drawings** (several author groups draw these, so they must match):
- **The YES console.** `KIT.props.yesButton({ label: "YES", sub: "TREATY" })` with a sign beside it, `KIT.props.sign({ text: "PUSH TO\nNOT DIE" })` and a navy arrow at the button. It springs out of door 2 in step-2-great-clicking-title, the clerk presses it in click-to-not-die, and it rises out of the stage in you-are-everyone. Draw it at the same size relative to the clerk every time (the cap at his hand height).
- **The 3.5% dial.** `KIT.props.gauge({ mount: "dial", label: "VOTING YES", value: 0, zones: [], marks: [[0.035, "3.5%", KIT.C.war]] })` (the bare dial, 120 across, pivot "0 -62"): the needed mark sits barely off zero, which is the joke. It stands on a short post beside the console in click-to-not-die and rolls back in on a little cart in chenoweth-shelf, its needle still a hair off zero.
- **The clerk.** One everyday human in a shirt with a beanpole build, the same options everywhere: `KIT.person({ outfit: "shirt", kind: "twig", tone: 2, color: 1, mood: "worried" })` (rig it with the same options). He presses the button in click-to-not-die, stands second in line in you-go-first, and is the lone human in you-are-everyone.
- **Grandma.** `KIT.cast("grandma")` (curlers, cat-eye glasses, apron), her arms posed and her poster left out. She peeks first in pluralistic-ignorance and stands first in line in you-go-first.
- **The thought bubble.** A cream cloud (8 to 10 sharp facets, thin navy outline, three trailing puffs down to the head) with a lid seam across its middle. Shut, it is plain cream with halftone dots; cracked or open, a tiny YES console (a teal cap on a slate box) glows inside. The crowd's bubbles in proving-it, pluralistic-ignorance and everyone-realizes, and the dots of 280-million.
- **The crowd.** About 24 everyday humans of every build (shirts, dresses, suits, overalls; `seed` picks each one) packed into a town square in front of a street of three war factories (`KIT.props.factory`, missile chimneys puffing) with a blank wall at the left end, Grandma in the front row, the Weapons Maker (`KIT.cast("weaponsMaker")`, hard hat, cigar, cradling his smiling missile) in the middle. The same humans in the same places in proving-it, pluralistic-ignorance and everyone-realizes; from proving-it's end on, the Weapons Maker drips cream paint, and from pluralistic-ignorance's end on, the old human beside Grandma is a skeleton.
- **The Grim Reaper.** `KIT.reaper()` with `KIT.props.clipboard` (navy tally marks in fives, as in Part 5) and a wristwatch drawn on his wrist bone (a cream face, a navy strap).

**Callback.** From Part 17's title card: the five numbered doors; door 1 is already open, and door 2 opens here (Steps 3 to 5 can open doors 3 to 5). From Part 5: the Grim Reaper and his tally clipboard; the Loud Humans (megaphones for heads) in referral-pyramid. From Part 1: the color flip (style bible, gag 2) in click-to-not-die; the dictionary card in pluralistic-ignorance has split-the-atom's look.

**Bans for this part.**
- No real people or logos. Erica Chenoweth is a name on a bookend, never a face. TikTok is a word on a placard, never its logo, an app or a phone screen.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: in 16:9 nothing important below y 900; in 9:16 nothing important from y 1450 down. Keep Wishonia's corner clear (16:9 x 1600 to 1920, y 690 down; 9:16 x 740 to 1040, y 60 to 430).
- The money is always money green: war seals on the parade in click-to-not-die, a medicine seal on the one bill that comes out of the funnel, plain bills (no seal) for the lifetime income and the referral bonuses.

## Changes from v1

- The humans are the stereotype cast: the Weapons Maker and his missile are the one holdout in the crowd; Grandma peeks into her bubble first; the clerk who presses the button is the lone human in the stadium; the scientist catches the medicine bill; every sharer in referral-pyramid becomes a Loud Human.
- Part 5's Grim Reaper comes back as a running gag: he waits for humanity to miss 3.5%, and the referral pyramid bumps him off its top.
- The gags go all the way: the scythe stops an inch from the clerk's neck, a paint bucket lands on the Weapons Maker, a waiting human turns into a skeleton with its hand still half up, the other planets die with their lines still bowing, the missile chimneys launch and burst as fireworks, the lone human is crowd-surfed, the history books spill marchers, a cannon and a crown, and a field of TV sets twerks the ground into a quake.
- step-2-great-clicking-title cuts in (a title card has no wall screen to zoom out of, as in Part 1), and click-to-not-die slides in from it, as Part 1's loved-ones does.
- The referral bonuses and the lifetime income are plain bills, not medicine money: they pay people, they do not buy trials.
- The labels that repeated the narration are gone ("MAKE HUMANS CLICK A BUTTON TO NOT DIE", "3.5%?", "Needed: 3.5% of humanity"); the dictionary card says "see illustration".
- The phones in 280-million are 1950s TV sets (`KIT.props.tvSet`), so nothing looks like a real app.
- Recurring props come from the shared library (`KIT.props.*`).

## Scene 1 · step-2-great-clicking-title

- id: step-2-great-clicking-title
- act: Title
- transition_in: cut
- key: both title lines in, door 2 just swung open, the YES console bobbing on its spring in the doorway
- cue: "Step 2: The Great Clicking"
- time: 40:53.0 to 40:56.1 (3.1 s)
- voiceover: "Step 2: The Great Clicking."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`) with the step number and its name; under the heading, Part 17's five numbered doors stand in a row on the horizon.
- wishonia: none
- props: title-card, door, yes-button
- status: outline

Moves: "Step" → "STEP 2" drops in. "2:" → the five numbered doors (`KIT.props.door`, labels "1" to "5") drop into their row, door 1 still ajar from Step 1. "Great" → "THE GREAT" slams in. "Clicking." → "CLICKING" slams in, and a big white cursor arrow with a navy outline glides in from the right edge. 0.3 s after "Clicking." starts → the cursor clicks door 2's knob; door 2 swings open and the YES console springs out of the doorway on a coil spring, bobbing.

Sound: a thunk on each title word; a slam as the doors land; a click from the cursor; a boing for the spring.

On screen: "STEP 2" / "THE GREAT CLICKING" / the doors' numbers. No: no Wishonia (a title card). Why: the narrator reads the heading, and door 2 hands the step its one prop.

## Scene 2 · click-to-not-die

- id: click-to-not-die
- act: The button
- transition_in: slide left
- key: on "Die": the scythe stopped an inch from the clerk's neck, the button just popped back up
- cue: "Make Humans Click a Button"
- time: 40:56.1 to 41:08.7 (12.7 s)
- voiceover: "Make Humans Click a Button to Not Die You need three point five percent of humanity to vote yes on: "Should your country redirect one percent of military spending to fund clinical trials?"."
- layer: B
- scene: The YES console on the left of the Earth paper, the clerk at it and the Grim Reaper behind him; then the camera slides right to a parade of war money marching into the war factory, the color-flip funnel over the line and the scientist at her lab bench. A ballot card with the question hangs across the top, outside the camera move.
- wishonia: PiP, happy-smile + body-presenting, then smirk-smile on "Die", then happy-smile + body-open-palms on "trials?"
- props: yes-button, sign, gauge, human (the clerk), reaper, clipboard, papers-red, papers-teal, color-flip-funnel, factory, lab, scientist, pill-bottle
- status: outline

Moves: "Make" → the YES console rises out of the floor, its "PUSH TO NOT DIE" sign and the dial beside it. "Humans" → the clerk shuffles up to it. "Click" → he presses it with one finger: it clicks down and pops back. "Button" → behind him, the Grim Reaper rises, scythe raised over the clerk's neck. "Not" → the scythe swings. "Die" → it stops an inch from the clerk's neck; the Reaper checks his tally clipboard, scowls and rubs out one mark. "five" → the dial beside the console: the clerk's one click nudges the needle a hair off zero, and the red 3.5% mark lights up, barely past it and still far away. "humanity" → the Reaper sees the needle, grins, sits down on the console, crosses his legs and checks his wristwatch. "vote" → the clerk presses again, harder, twice; the needle does not budge. "yes" → the Reaper taps his watch. "Should" → a ballot card drops in across the top and its question types on with the voice. "redirect" → the camera slides right: a parade of war money (green bills, red missile seals) marches toward the war factory (`KIT.props.factory`), and the color-flip funnel swings down over the line. "one" → it snatches exactly one bill; the other 99 march on into the factory door, and its missile chimneys puff smugly without noticing. "percent" (second) → the funnel's box rattles. "fund" → out of the spout walks the same bill with a teal cross seal. "trials?" → it hops onto the scientist's lab bench (`KIT.cast("scientist")` at `KIT.props.lab`); every flask boils over at once and a pill bottle pops up out of the beaker like toast.

Sound: a rising slide whistle as the console rises; a click for the press; a whoosh as the scythe swings; a record scratch as it stops; a tick as the needle twitches and a ding for the 3.5% mark; a huff as the Reaper sits; a click as the clerk presses again; a tick from the watch; typewriter clacks for the question; a whoosh for the camera; a pop as the funnel snatches its bill; a whirr as the box rattles; a sparkle as the seal flips; a toaster pop at the lab.

On screen: "PUSH TO NOT DIE" (the sign) / "TREATY" (the button's plate) / "VOTING YES" and "3.5%" (the dial) / the ballot card: "Should your country redirect 1% of military spending to fund clinical trials?" / "WEAPONS" (the factory sign). No: no heading banner and no "Needed: 3.5%" label; the dial says it. Why: the whole step is one button and one question; one click saves one human for a moment, 3.5% saves everyone, and the color flip shows how little of the war money it asks for.

## Scene 3 · proving-it

- id: proving-it
- act: Everyone already agrees
- transition_in: slide left
- key: on "supports": the whole crowd mid-nod, hats in the air, the Weapons Maker and his missile shaking their heads, the tally board nearly full
- cue: "You are not creating"
- time: 41:08.7 to 41:22.4 (13.6 s)
- voiceover: "You are not creating support for not dying of horrible diseases and not mass murdering each other. Nearly everyone already supports not dying of horrible diseases and not mass murdering each other. You are proving it."
- layer: B
- scene: The crowd in its town square, each human under a closed thought bubble, the war factories puffing behind them; a painter on a ladder at the blank wall on the left; a pollster's tally board on an easel on the right.
- wishonia: PiP, neutral-smile, then smirk-smile + body-point-right on "proving"
- props: human, thought-bubble, weapons-maker, missile, painter (human in overalls), ladder, paint bucket, banner, tally board, clipboard, checkbox-tick
- status: outline

Moves: "You" → the crowd, every bubble shut. "creating" → the painter (an everyday human in overalls, a barrel build) climbs his ladder and starts painting a giant banner on the wall, "SUPP", in big drippy letters. "support" → "SUPPORT". after "other." (first) → he stops, brush in the air, and looks down at the crowd. "everyone" (first) → the tally board fills itself, tick after tick, almost every box in both rows. "supports" → every human nods once, all together, so hard that every hat hops up and lands again; in the middle, the Weapons Maker shakes his head, and the missile in his arms shakes its head too. "murdering" (second) → the board's last box gets a red cross, and the missile crosses its arms and scowls. "proving" → the painter swaps his brush for a clipboard; the paint bucket tips off the ladder and lands upside down on the Weapons Maker's head, splat, paint dripping down him and the missile. "it." → the painter climbs down and starts counting heads with his pencil, tap, tap, tap.

Sound: a marker scrub for the painting; a record scratch as he stops; pencil ticks as the board fills; a thunk for the nod and pats as the hats land; a boing as the Weapons Maker shakes his head; a squeak as the missile crosses its arms; a splat for the bucket.

On screen: "SUPPORT" (the banner) / the tally board: "NOT DYING OF HORRIBLE DISEASES" and "NOT MASS MURDERING EACH OTHER", two rows of ticks with one red cross. No: no percentages; the ticks are the count. Why: the vote does not change minds; it counts minds already made up, and the only holdout is the one holding the missile.

## Scene 4 · pluralistic-ignorance

- id: pluralistic-ignorance
- act: Everyone already agrees
- transition_in: same form (no seam)
- key: on "permission": every hand half raised, cobwebs between them, the skeleton beside Grandma with its hand still up
- cue: "Everyone thinks this is crazy"
- time: 41:22.4 to 41:35.8 (13.4 s)
- voiceover: "Everyone thinks this is crazy because everyone else thinks this is crazy. Your economists call it pluralistic ignorance, which is the polite term for eight billion people waiting for permission to want what they already want."
- layer: B
- scene: The same square and crowd. Grandma peeks into her bubble, glances at her neighbors and snaps it shut; then everybody does the same.
- wishonia: PiP, thinking-closed + body-thinking, then eyeroll-closed + body-shrug on "waiting"
- props: human, grandma, thought-bubble, yes-button (inside the bubbles), dictionary-card, earth-globe, weapons-maker
- status: outline

Moves: "Everyone" → the first frame is proving-it's last: the painter counting heads, the Weapons Maker dripping paint. "crazy" (first) → Grandma, in the front row, cracks her bubble open: the YES button glows inside. "else" → her eyes slide left, then right: every other bubble is shut. after "else" → she snaps hers shut and whistles at the sky. "crazy." (second) → every bubble in the crowd cracks open at once, every head glances left and right, and they all snap shut again in a ripple across the square. "pluralistic" → a dictionary card slides in over the top. "ignorance," → it lands: "PLURALISTIC IGNORANCE (n.): see illustration", with an arrow down at the crowd. "eight billion" → the camera pulls back and back until the crowd covers a whole small Earth (`KIT.props.earthGlobe`), a shut bubble over every head, and a counter clicks up to "8,000,000,000". "waiting" → the camera drops back into the front row: every human raises a hand halfway and waits. "permission" → cobwebs string between the raised hands, and the old human beside Grandma x-rays into a grinning skeleton, hand still half up. "already" → every bubble flickers open for one frame, all showing the YES button, the skeleton's too. after "want." (second) → they snap shut.

Sound: a squeak as Grandma's bubble cracks; a pop as she snaps it shut; an innocent whistle; a ripple of pops for the crowd; a whoosh as the card slides and a thunk as it lands; a whoosh for the pull-back; crickets while they wait; a zap for the x-ray; a sparkle for the flicker; a pop as the bubbles shut.

On screen: "PLURALISTIC IGNORANCE (n.): see illustration" / "8,000,000,000". No: the card does not repeat the narration's definition; the crowd is the definition. Why: names the real obstacle, which is silence, not disagreement.

## Scene 5 · you-go-first

- id: you-go-first
- act: Everyone already agrees
- transition_in: slide left
- key: on "finish": the other planets dark under their tiny headstones, their tiny lines now skeletons still bowing, Earth's line still bowing at its door
- cue: "It is the galaxy's longest"
- time: 41:35.8 to 41:44.2 (8.4 s)
- voiceover: "It is the galaxy's longest game of you-go-first. Most species that start playing it don't finish playing it."
- layer: B
- scene: A door marked REFERENDUM on a little hill, the Grim Reaper holding it open like a doorman, and a line of humans in front of it, each bowing the next one ahead; then the camera pulls back to an engraved star chart of planets, each with its own door and its own line.
- wishonia: PiP, sideeye-closed + body-arms-crossed
- props: door, reaper, grandma, human (the clerk), earth-globe, headstone, star chart
- status: outline

Moves: "galaxy's" → the door (`KIT.props.door({ label: "REFERENDUM" })`) on a little hill; the Grim Reaper holds it open, bowing like a doorman. "longest" → the line fills in: Grandma first, then the clerk, then everyday humans out to the edge of the frame. "you-go-first." → every human bows and waves the one behind it ahead, all at once, so nobody moves. A beat later → the Reaper taps his wristwatch. "Most" → the camera pulls back: the hill is a small Earth on an engraved star chart, among five other planets, each with a tiny door and a tiny bowing line. "finish" → the other planets go dark one by one, a tiny headstone (`KIT.props.headstone`) popping up on each; their tiny lines are skeletons now, still bowing. after "it." (last) → only Earth is lit, its line still bowing; its tiny Reaper looks up at the camera and taps his watch.

Sound: a thunk as the door lands; soft pats for the bows; a tick from the watch; a whoosh for the pull-back; a light switch as each planet goes dark and a thunk for each headstone; a last tick.

On screen: "REFERENDUM" on the door. Why: the price of nobody going first, as a dark joke.

## Scene 6 · everyone-realizes

- id: everyone-realizes
- act: The moment they find out
- transition_in: slide left
- key: after "unrecognizable.": every bubble open with its smiling Earth and its stack of bills, the missile chimneys bursting into fireworks over new hospitals and labs, the Weapons Maker cuddling a pill bottle
- cue: "If every human realized"
- time: 41:44.2 to 41:59.9 (15.8 s)
- voiceover: "If every human realized that nearly every other human would like a world without war and disease and an extra five hundred and eighteen thousand, eight hundred and seventy-nine dollars in lifetime income, it would be done tomorrow and the world would be unrecognizable."
- layer: B
- scene: The same square and crowd, every bubble shut, with a street of war factories behind them; every bubble pops open at the same moment.
- wishonia: PiP, happy-smile, then excited-open + body-excited on "tomorrow", then happy-smile + body-wide-gesture on "unrecognizable."
- props: human, thought-bubble, weapons-maker, missile, earth-globe, plain-paper, price-tag, calendar, stamp-mark, factory, hospital, lab, pill-bottle
- status: outline

Moves: "If" → the square again, every bubble shut (Grandma, the paint-spattered Weapons Maker and the skeleton too); behind them, a street of three war factories, missile chimneys puffing. "realized" → every bubble pops open at once, with a bang that blows every hat off. "human" (second) → every head turns slowly to its neighbors' bubbles: the same YES button in every one; jaws drop. "without" → every YES button turns into a tiny smiling Earth (`KIT.props.earthGlobe({ face: "smile" })`) with no smoke on it. "thousand," → a fat stack of plain green bills thumps into every bubble. "dollars" → a price tag swings out from the front bubble's stack: "+$518,879". "done" → a tear-off desk calendar beside the crowd (`KIT.props.calendar`) tears off its page. "tomorrow" → a stamp mark slams onto the next page: "DONE". "world" (second) → the missile chimneys on every factory blast off into the sky. "unrecognizable." → the factories fold flat and pop back up as hospitals and labs, and the missile in the Weapons Maker's arms turns into a pill bottle. after "unrecognizable." → the missiles burst high overhead as fireworks; the Weapons Maker looks down at his pill bottle, shrugs, and cuddles it anyway.

Sound: pops as the bubbles burst open and a boing for the hats; a falling slide whistle as the jaws drop; a sparkle for the little Earths; a thunk for the stacks; a cash-register ding for the tag; a rubber-stamp thunk on DONE; an airplane roar as the missiles launch; a whirr as the street redraws; pops and a sparkle for the fireworks.

On screen: "+$518,879" (the tag) / "DONE" (the stamp) / the factory signs "WEAPONS", then "HOSPITAL". Why: what happens when everyone learns what everyone else wants, and where the missiles go.

## Scene 7 · you-are-everyone

- id: you-are-everyone
- act: The moment they find out
- transition_in: slide left
- key: on "everyone.": the stadium lights just banged on, every seat holding the same sign, the WEIRD? cap flying off the clerk
- cue: "Right now every human"
- time: 41:59.9 to 42:10.7 (10.7 s)
- voiceover: "Right now every human who wants less war and disease assumes they are the weird one. The referendum is the moment they find out they are everyone."
- layer: B
- scene: The clerk alone in a spotlight on a dark stage holds a small sign; the YES console rises beside him; he presses it, and the lights of a huge stadium come on around him.
- wishonia: PiP, neutral-smile, then excited-open + body-fist on "everyone."
- props: human (the clerk), sign, yes-button, stage, spotlight, stadium crowd
- status: outline

Moves: "Right" → a dark stage; a spotlight clunks on over the clerk, alone, holding up a small sign: "LESS WAR AND DISEASE". "assumes" → he peers out into the dark, sweating. "weird" → a "WEIRD?" label floats down. after "one." → it lands on his head like a dunce cap; he hides the sign behind his back. "referendum" → the YES console rises out of the stage beside him. "moment" → he looks at it and gulps. "find" → he presses it. "everyone." → the stadium lights bang on, bank after bank: every seat in a huge stadium holds a human with the same sign, and the WEIRD? cap blows off his head. after "everyone." → the crowd pours down, lifts him overhead and crowd-surfs him away, sign up.

Sound: a light switch and a low hum for the spotlight; crickets in the dark; a falling slide whistle for the label and a thunk as it lands; a rising slide whistle for the console; a click for the press; slams for the light banks and a low boom of a roar; a whistle as he goes up.

On screen: "LESS WAR AND DISEASE" (on every sign) / "WEIRD?". Why: the turn of the step; the vote shows people they are not alone.

## Scene 8 · chenoweth-shelf

- id: chenoweth-shelf
- act: Why 3.5%
- transition_in: slide left
- key: on "one.": a long row of teal bars at the line, the counter landing on "FAILURES: 0"
- cue: "Why three point five percent?"
- time: 42:10.7 to 42:34.6 (23.9 s)
- voiceover: "Why three point five percent? A political scientist named Erica Chenoweth studied every major political movement of the last century and found that none had ever failed after achieving three point five percent active participation. Not one. Every civil rights movement, every revolution, every regime change. Hit three point five percent and you win."
- layer: B
- scene: A long shelf of history books, each with a small bar gauge on its spine and a line at 3.5%, ending in a brass bookend with a nameplate.
- wishonia: PiP, thinking-closed + body-thinking, then smirk-smile + body-counting on "Not", then happy-smile + body-fist on "win."
- props: gauge, shelf, books, bookend, counter, bell, tiny marchers, tiny cannon, crown, rich-human (tiny), confetti
- status: outline

Moves: "Why" → the 3.5% dial from click-to-not-die rolls in on a little cart, its needle still a hair off zero, and a big question mark springs out of its top on a coil spring. "Chenoweth" → a brass bookend slides onto the end of a long shelf of history books and lands; its nameplate reads "ERICA CHENOWETH". "studied" → the camera tracks along the shelf, book after book; each spine has a year and a small bar gauge with a line at 3.5%. "three" (second) → down the shelf, each bar that reaches the line turns teal, one after another. "Not one." → a counter on the bookend spins and lands: "FAILURES: 0". "rights" → one book tips forward and a tiny crowd marches out of it with tiny signs, along the shelf. "revolution," → the next book tips and a tiny cannon rolls out and fires a confetti ball. "regime" → the next book tips and a tiny crown rolls out. "change." → a tiny fat cat (`KIT.cast("richHuman")`, small) chases the crown off the edge of the shelf. after "change." → splat, somewhere below. "win." → a boxing bell over the shelf rings, confetti falls, and the dial's question mark flips into an exclamation mark.

Sound: a boing for the question mark; a thunk as the bookend lands; dings as the bars turn teal; a tick and a thunk for the counter; thunks as the books tip; a pop for the confetti cannon; a falling slide whistle as the fat cat goes over and a splat below; a bell and a sparkle on "win".

On screen: "ERICA CHENOWETH" (the nameplate) / the spines' years / "FAILURES: 0". No: the researcher is a name only, never a drawn face; no "3.5%?" card (the question mark is on the dial). Why: the evidence that 3.5% is enough.

## Scene 9 · cheat-code

- id: cheat-code
- act: Why 3.5%
- transition_in: same form (no seam)
- key: on "purpose.": the drawer marked LATER under dust and a cobweb, the spider moving in, a tumbleweed rolling past
- cue: "Humanity discovered the cheat code"
- time: 42:34.6 to 42:40.9 (6.4 s)
- voiceover: "Humanity discovered the cheat code for changing its own civilization and then never used it on purpose."
- layer: B
- scene: A card slides out of the last book on the shelf; an everyday human reads it, files it in a drawer marked LATER, and time passes.
- wishonia: PiP, eyeroll-closed + body-arms-crossed
- props: shelf, books, card, drawer, human, spider, cobweb, tumbleweed
- status: outline

Moves: "Humanity" → the first frame is chenoweth-shelf's last: the confetti still falling. "discovered" → the last book before the bookend glows. "cheat" → a card slides out of it. "code" → it stands up with a game-show ding: "CHEAT CODE: 3.5% = YOU WIN". "civilization" → an everyday human in a suit (a refrigerator box) picks it up, reads it and nods, impressed. "never" → he files it in a drawer under the shelf marked "LATER" and slams it. "purpose." → time passes in one beat: dust piles on the drawer, a spider strings a cobweb across it and moves in, and a tumbleweed rolls past.

Sound: a whoosh as the card slides out; a game-show ding; a slam for the drawer; a whoosh of wind and crickets.

On screen: "CHEAT CODE: 3.5% = YOU WIN" / "LATER". Why: the punchline on the evidence; humans had the answer and never used it on purpose.

## Scene 10 · 280-million

- id: 280-million
- act: 280 million
- transition_in: slide left
- key: after "twerk.": the small field of open bubbles bouncing beside the field ten times bigger of wiggling TV sets, the ground shaking
- cue: "That's two hundred and eighty million"
- time: 42:40.9 to 42:56.5 (15.5 s)
- voiceover: "That's two hundred and eighty million humans. Sounds like a lot until you remember that more than ten times as many of you downloaded TikTok to watch people twerk. You can get two hundred and eighty million to vote yes or no on the treaty."
- layer: B
- scene: A dense field of tiny open thought bubbles, each with its YES button, for 280 million people; then a field ten times bigger beside it, each dot a tiny 1950s TV set with a wiggling human on its screen.
- wishonia: PiP, smirk-smile, then sideeye-closed + body-hands-hips on "twerk.", then happy-smile + body-presenting on "vote"
- props: thought-bubble (tiny), tv-set, sign (the placard), ballots (tiny), checkbox-tick
- status: outline

Moves: "two" (first) → the field fills in, row by row: tiny open bubbles from everyone-realizes, each with its YES button. "humans." → a counter under it lands on "280,000,000". "Sounds" → the camera pulls back until the field is a small patch. "ten" → a field ten times bigger draws in beside it: tiny 1950s TV sets (`KIT.props.tvSet`) on splayed legs, rabbit ears up. "TikTok" → a placard on a post (`KIT.props.sign`) types on beside it: "DOWNLOADED TIKTOK". "twerk." → every TV shows the same tiny human wiggling its hips, and the whole field of TVs wiggles with it, in step, so hard the ground quakes, the rabbit ears flap and the small field's bubbles bounce. "vote" → the small field's bubbles turn into tiny ballots. "yes" → a wave of ticks runs across the ballots. after "treaty." → the TVs stop; one at the front topples over, still wiggling.

Sound: pops as the field fills; a ding as the counter lands; a rising slide whistle as the big field draws in; typewriter clacks for the placard; a boing and a low boom for the quake; a pop as the ballots appear; pencil ticks for the wave; a thunk for the toppled TV.

On screen: "280,000,000" / "DOWNLOADED TIKTOK" (the placard). No: TikTok is a word on a placard, no logo, no app and no phones. Why: makes 280 million feel small.

## Scene 11 · referral-pyramid

- id: referral-pyramid
- act: 280 million
- transition_in: slide left
- key: on "diseases.": the pyramid of Loud Humans blasting, the sign at its top, the Reaper tumbling down the far side
- cue: "Two hundred and fifty million dollars"
- time: 42:56.5 to 43:10.9 (14.4 s)
- voiceover: "Two hundred and fifty million dollars of the campaign budget goes to paid referral bonuses that make sharing their link to vote financially attractive. It's a pyramid scheme where the thing at the top of the pyramid is not dying from preventable diseases."
- layer: B
- scene: A pile of plain bills pays every human who passes the vote link on; each one who shares turns into a Loud Human, and they stack into a human pyramid up the hill where the Grim Reaper sits waiting.
- wishonia: PiP, smirk-smile + body-presenting, then smirk-smile + body-wide-gesture on "pyramid", then happy-smile + body-open-palms on "diseases."
- props: plain-paper, sign, human, loud-human, link card, reaper, clipboard
- status: outline

Moves: "Two" → a pile of plain green bills thumps down on the left, with a sign on it: "REFERRAL BONUSES". On a hilltop on the right, the Grim Reaper sits on a rock, checking his watch. "dollars" → the pile settles with a ding. "referral" → bills hop off the pile and walk toward a row of everyday humans. "sharing" → the first human passes a small ticket marked "VOTE" (the link) to the next; a bill hops into the giver's hand, and the giver's head turns into a megaphone, blasting (`prop: "megaphone"`, as Part 5's Loud Humans). "link" → the next one passes it on: another bill, another megaphone; it runs down the row faster and faster. "attractive." → the Loud Humans climb onto each other's shoulders. "pyramid" (first) → they stack into a human pyramid at the foot of the Reaper's hill, every megaphone blasting. "top" → the pyramid grows up the hill and lifts the Reaper off his rock; the camera tilts up after him. "not" → the top Loud Human plants a sign: "NOT DYING FROM PREVENTABLE DISEASES", and its post pokes the Reaper off the top. "dying" → he tips over the edge. "from" → he tumbles down the far side, scythe and clipboard flying. 0.4 s after "diseases." starts → he lands at the bottom, splat. after "diseases." → his clipboard flutters down and lands on his skull.

Sound: a thunk for the pile and a cash-register ding; a pop as each head turns into a megaphone; soft pats as they climb; thunks as the pyramid stacks; a yelp as the Reaper is lifted and another as he is poked off; a falling slide whistle for the tumble; a splat at the bottom; a thunk for the clipboard.

On screen: "REFERRAL BONUSES" (the pile's sign) / "VOTE" (the link ticket) / "NOT DYING FROM PREVENTABLE DISEASES" (the sign at the top). Why: how the 280 million get there; sharing pays, so everyone becomes the Loud Human, and the thing at the top of this pyramid knocks the Reaper off it.
