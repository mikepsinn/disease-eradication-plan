---
format: 1920x1080
duration: 1:22.8
message: "A $1 billion campaign that gets treatments to patients 212 years sooner returns 7.53 million to one, at two cents per healthy year of life."
arc: Title card → the equation → the Calculator leaves the desk → the trophy shelf of not dying → still 92.1 times better at a 1% chance
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 16, "The Math"
audio: index-manual.cbaf659d.mp3, 34:20.6 to 35:43.4
version: v2
---

# Part 16 storyboard: "The Math"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the engraved Earth paper; the money is green, and its seal says what it buys (a red missile for war, a teal cross for medicine). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The Calculator (`KIT.props.calculator`), one tan desk machine with eyes and stick legs. It pops up behind the title, sits on the chalkboard ledge doing the sums in quadrillion-equation and falls apart a little more with every term (sweat, a tape of zeros, smoke, keys flying off), jumps out of the wall screen onto Wishonia's desk in calculator-scream, screams and walks off the edge, is missing from greatest-hits-trophies (it is recovering), and peeks back in at the end of one-percent-chance with its display taped up, reads "92.1×", and leaves again.

**Running gag: the Calculator loses a key every time it leaves.** It crashes off the desk and its "=" key bounces back into frame; in one-percent-chance it has a gap where the "=" key was, crashes again offscreen, and a second key bounces in.

**Second spine: the trophy shelf.** greatest-hits-trophies and one-percent-chance are one drawing: the shelf under its marquee sign, the three small cups, the giant treaty trophy on its dolly and the wooden yardstick standing beside it as a height chart. The shelf tilts in greatest-hits-trophies and stays tilted.

**Callback from Part 14.** quadrillion-equation starts from the fat "212 YEARS SOONER" arrow built in two-hundred-twelve-years-sooner.

**Callback set up here.** Part 19 (two-clients-arithmetic): the Calculator walks back onto the desk and, for once, does not scream. It can still wear the tape and the gap in its keypad.

**Bans for this part.**
- No real people or logos.
- No real banknotes or coins: the campaign money is a plain green bundle (`KIT.money("plain")`), and the 2¢ is only a price tag.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame.

## Changes from v1

- The humans are the theme song's stereotypes. The Rich Human appraises a tiny human through his monocle and gets dollar-sign eyes; the Scientist reads the 2¢ tag through her magnifying glass and pushes the treaty trophy in; the crowd and the pessimist on the gauge are everyday humans whose bodies come from their outfits.
- Every gag pays off on screen: skeletons in the crowd fill back in, the disease blobs are bowled off the globe and splat, the Calculator falls apart on the ledge and crashes off the desk, the shelf's bracket snaps, the smallpox cup squashes its germ, and the pessimist is zapped by his own raincloud.
- The title card cuts in (the parts are rendered on their own and joined), and quadrillion-equation slides in from it, as loved-ones does in Part 1.
- The Calculator jumps out of the wall screen onto the desk, so it is the same Calculator in both layers.
- New running gag: the Calculator loses a key every time it leaves.

## Scene 1 · the-math-title

- id: the-math-title
- act: Title
- transition_in: cut (the parts are rendered on their own and joined)
- key: after "Math.": "THE MATH" in, the Calculator's eyes over the top of "MATH"
- cue: "The Math."
- time: 34:20.6 to 34:22.4 (1.8 s)
- voiceover: "The Math."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`): "THE MATH" slams in, and the Calculator pops up behind the last word, reads it and ducks.
- wishonia: not on screen
- props: title-card, calculator
- status: outline

Moves: "The" → "THE" slams in. "Math." → "MATH" slams in. after "Math." → the Calculator pops up behind "MATH" like a gopher, display on "0", its eyes just over the top of the letters; it reads the heading, a bead of sweat flies off it, and it ducks back down.

Sound: a thunk on each title word; a boing as the Calculator pops up; a pop as it ducks.

On screen: "THE MATH". No: the narration gives the card 1.8 s, so one slam per word and one peek. Why: the narrator reads the heading; the peek sets up the Calculator.

## Scene 2 · quadrillion-equation

- id: quadrillion-equation
- act: The return
- transition_in: slide left
- key: on "million": the whole equation chalked up, the Calculator on the ledge buried in its own zero tape, shaking, smoking, keys flying off
- cue: "Remember the two hundred"
- time: 34:22.4 to 34:55.0 (32.6 s)
- voiceover: "Remember the two hundred and twelve years timeline shift? Treatments reaching patients that many years sooner means billions of people gain years of healthy life. Value each of those life-years at one hundred and fifty thousand dollars (the standard economic valuation), multiply across the global disease burden over the acceleration window, and you get seven point five three quadrillion dollars in total economic value. Divide that by the one billion dollars campaign cost, and you get a return of seven point five three million to one."
- layer: B
- scene: A big school chalkboard in a wooden frame with a ledge, standing on the cream paper. The equation chalks itself on term by term, and each term gets an actor on the floor in front of the board: the 212 arrow, a crowd, the Rich Human, a classroom globe under a heap of diseases, a little bundle of money. The Calculator sits on the right end of the ledge doing the sums and falls apart.
- wishonia: PiP, thinking-small + body-thinking, then excited-oh + body-excited on "quadrillion", then smirk-smile + body-point-right on "million"
- props: chalkboard, arrow-212 (from Part 14), pill-bottle, human, rich-human, price-tag, earth-globe, disease-blob, papers-plain, calculator
- status: outline

Moves: "Remember" → the board slides in, empty, the Calculator already on the right end of the ledge, display "0". "two hundred and twelve" → the fat "212 YEARS SOONER" arrow from two-hundred-twelve-years-sooner (Part 14) swoops in from the left. "twelve" → it slams onto the top left of the board. "timeline" → chalk underlines it. "Treatments" → a pill bottle with a teal cross sprints along the arrow on stick legs. "patients" → at the arrowhead it hands itself to a patient whose chest light is blinking red; the light goes out. "billions" → a crowd of tiny everyday humans pops up along the floor in front of the board, every chest light blinking red, a few of them already grinning skeletons; chalk: "→ BILLIONS OF HEALTHY YEARS". "healthy" → every light goes out, and the skeletons x-ray back into people and look at their own hands. "life." → the whole crowd hops. "Value" → the Rich Human waddles in from the left on his stub legs. "life-years" → he picks one tiny human up between finger and thumb and holds it to his monocle like a diamond. "thousand" → he ties a price tag to its wrist, "$150,000", and sets it down; chalk: "× $150,000 PER HEALTHY YEAR". "standard" → tags pop onto every human in the crowd, one after another. "valuation)," → the Rich Human's eyes turn to dollar signs. "multiply" → the crowd doubles, and doubles again, until it is packed from edge to edge. "global" → a classroom globe on a stand rolls in; chalk: "× THE GLOBAL DISEASE BURDEN". "burden" → a heap of grinning disease blobs drops onto the globe, and it sags on its stand. "acceleration" → the 212 arrow pulls back like a slingshot. "window," → it fires through a little chalk window frame and bowls the blobs off the globe; they splat flat against the board's frame and slide down it. "seven" → the Calculator's keys clatter by themselves, its eyes darting. "quadrillion" → chalk: "= $7.53 QUADRILLION"; the Calculator's display fills with zeros, and they keep coming: a paper tape of zeros spools out of the display, piles up on the ledge and spills to the floor. "value." → a bead of sweat drops off it. "Divide" → a long chalk division bar under the quadrillion. "billion" → a small strapped bundle of plain green money walks in on stick legs and stands under the bar. "campaign" → chalk: "÷ $1 BILLION CAMPAIGN". "cost," → the bundle looks up at the number on top of it and gulps. "return" → the Calculator, drenched, starts to shake. "million" → chalk: "= 7.53 MILLION : 1", the bundle standing under the 1; the Calculator shakes harder, and smoke curls out of its seams. "one." → its keys pop off one by one, and its display flickers.

Sound: a whoosh as the board slides in; a thunk as the arrow slams; a chalk squeak for each chalk line; a whistle as the bottle sprints; a pop as the light goes out; a quick run of pops as the crowd appears; a sparkle as the skeletons fill back in; a boing as they hop; tiny footsteps for the Rich Human; a ding off the monocle; a cash-register ding for the tag; pops for the tags; a ding on the dollar eyes; a run of pops as the crowd multiplies; a thunk as the blobs land; a whoosh and two splats for the slingshot; key clicks; typewriter clatter as the tape spools; a drip for the sweat; squeaky footsteps for the bundle; a hum as the Calculator shakes; a sizzle of smoke and pops as the keys fly off.

On screen: "212 YEARS SOONER" / "→ BILLIONS OF HEALTHY YEARS" / "× $150,000 PER HEALTHY YEAR" / "× THE GLOBAL DISEASE BURDEN" / "= $7.53 QUADRILLION" / "÷ $1 BILLION CAMPAIGN" / "= 7.53 MILLION : 1" / the tag "$150,000". No: no real banknotes; the bundle is plain green paper with no seal. Why: the return, built so a viewer can follow each step, while the machine doing the sums falls apart.

## Scene 3 · calculator-scream

- id: calculator-scream
- act: The return
- transition_in: zoom out of the wall screen (the screen shows quadrillion-equation's last frame)
- key: on "scream,": the Calculator at the desk's edge, "ERROR" on its display, mouth wide, shake lines
- cue: "Your calculator will display"
- time: 34:55.0 to 35:02.7 (7.7 s)
- voiceover: "Your calculator will display an error, emit a tiny electronic scream, and attempt to leave the desk. This is correct."
- layer: A
- scene: The camera pulls out of the wall screen onto the office. The Calculator jumps out of the screen onto Wishonia's desk, shows "ERROR", screams, and walks off the edge; Wishonia sips her coffee and does not look.
- wishonia: happy-smile + body-hands-hips, then happy-closed + body-hands-hips on "correct."
- props: office, wall-screen, desk, mug, calculator
- status: outline

Moves: "Your" → the camera pulls out of the wall screen, which still shows the finished board, the Calculator smoking on its ledge. "calculator" → it leaps out of the screen, trailing its zero tape, and lands on Wishonia's desk. "display" → it turns to the camera. "error," → its display reads "ERROR". "scream," → its mouth opens wide; shake lines and a tiny zigzag scream. "attempt" → it marches to the edge of the desk on its stick legs. "leave" → it looks down over the edge. "desk." → Wishonia's mug rises and she sips. "correct." → the mug goes down slowly; the Calculator steps off the edge and drops out of frame. after "correct." → a falling whistle, a crash from below, and its "=" key bounces up into frame, spins, and lands on the desk next to the mug. Wishonia does not look.

Sound: a whoosh as the camera pulls out; a boing as it leaps; a thunk as it lands; an electric zap on "ERROR"; a tiny yelp of a scream; tiny squeaky footsteps; a slurp on the sip; a soft thunk as the mug goes down; a falling slide whistle, a clank and a splat from below, and a pop as the key bounces in.

On screen: "ERROR". Why: the number is so big the machine quits, and Wishonia confirms it.

## Scene 4 · greatest-hits-trophies

- id: greatest-hits-trophies
- act: Cost-effectiveness
- transition_in: zoom into the wall screen
- key: after "cheaper.": the giant treaty trophy beside the tilted shelf, its top out of frame, the yardstick beside it flagged "9,200× CHEAPER", the three small cups piled at the low end
- cue: "Cost-effectiveness: two cents"
- time: 35:02.7 to 35:30.2 (27.5 s)
- voiceover: "Cost-effectiveness: two cents to save one year of healthy human life. Anti-malaria bed nets, the gold standard for keeping humans alive, cost one hundred and eighty-four dollars. This is nine thousand two hundred times cheaper. It beats smallpox eradication (one hundred and fifty-nine to one) and childhood vaccinations (ten point nine to one), which were humanity's previous greatest hits in the "not dying" genre."
- layer: B
- scene: A trophy shelf on the paper wall under a marquee sign, "GREATEST HITS IN NOT DYING", holding humanity's three best buys in staying alive: bed nets (a gold cup draped in a little net), smallpox eradication (a cup standing on a germ) and childhood vaccines (a cup with a syringe for a handle). A giant new trophy for the 1% Treaty rolls in and towers over the shelf.
- wishonia: PiP, happy-smile + body-presenting, then excited-ee + body-excited on "nine", then smirk-smile + body-hands-hips on "previous"
- props: trophy-shelf, trophy, sign, price-tag, scientist, germ, mosquito, dolly, yardstick
- status: outline

Moves: "Cost-effectiveness:" → the shelf, its three cups dull and its sign dark. "cents" → a price tag no bigger than a crumb flutters down onto the floor; the Scientist strides in with a magnifying glass and bends over it. "life." → the glass shows it big: "2¢ PER HEALTHY YEAR". "bed" → the bed-net cup lights and gleams. "nets," → its price tag swings out. "gold" → a gold star slaps onto it. "keeping" → a mosquito buzzes in and dive-bombs the net. "alive," → it bounces off. "eighty-four" → the bed-net tag flips: "$184 PER HEALTHY YEAR". "nine" → the floor shakes; the giant treaty trophy rolls in from the right on a dolly pushed by the Scientist, so tall its top is out of frame, "1% TREATY" on its plate and the crumb-sized 2¢ tag tied to its base. "two" → a wooden yardstick stands up beside the giant trophy and unfolds upward, click by click, from the height of the bed-net cup until it runs out of the top of the frame. "cheaper." → a flag pops out of it: "9,200× CHEAPER". after "cheaper." → the giant trophy's weight tips the floor; the shelf's bracket snaps at one end, and the three small cups slide down the tilted shelf and clink together at the low end. "smallpox" → the smallpox cup lights, its tag "159 : 1". "eradication" → it stamps down on the germ under its base: splat, the germ flat as a pancake, eyes blinking. "childhood" → the vaccine cup lights, its tag "10.9 : 1". "vaccinations" → a second germ climbs the cup and is jabbed by its syringe handle; it pops. "humanity's" → the marquee bulbs light and chase around "GREATEST HITS IN NOT DYING". "previous" → a strip slaps across the top of the sign: "PREVIOUS". after "genre." → one bulb pops and goes out.

Sound: a whoosh as the camera zooms in; a little whistle as the tag flutters down; a ding when the glass reads it; a light-switch click and a sparkle for the bed-net cup; a slap for the star; a mosquito whirr and a boing; a cash-register ding as the tag flips; a rumble and squeaking dolly wheels; a slide-up and clicks as the yardstick unfolds; a clank as the bracket snaps, a slide-down and a clink as the cups pile up; a switch for each cup that lights; a splat for the germ; a pop and a yelp for the second germ; a sparkle for the marquee; a slap for PREVIOUS; a pop for the bulb.

On screen: "GREATEST HITS IN NOT DYING" / "2¢ PER HEALTHY YEAR" / "$184 PER HEALTHY YEAR" / "1% TREATY" / "9,200× CHEAPER" / "159 : 1" / "10.9 : 1" / "PREVIOUS". Why: compares the treaty to the best buys humans already know, and demotes them.

## Scene 5 · one-percent-chance

- id: one-percent-chance
- act: Cost-effectiveness
- transition_in: same form (no seam)
- key: after "nets.": the shrunken treaty trophy, its top now in frame and still far taller than the bed-net cup, the yardstick on "92.1× BETTER", the charred pessimist on the gauge, the Calculator walking off the right edge
- cue: "Even if you assume"
- time: 35:30.2 to 35:43.4 (13.3 s)
- voiceover: "Even if you assume only a one percent probability of the treaty actually passing (because you're you), the expected return is still ninety-two point one times better than anti-malaria bed nets."
- layer: B
- scene: The same shelf. A gauge on a pole reads the chance of passing, and a gloomy human hangs on its needle to hold it at 1%. The giant treaty trophy shrinks to 1% of its size and still towers over the bed-net cup. The Calculator peeks back in, taped up, reads it, and leaves again.
- wishonia: PiP, smirk-smile + body-idle, then sideeye-closed + body-arms-crossed on "you're", then happy-smile + body-point-right on "ninety-two"
- props: trophy-shelf, trophy, gauge, human, yardstick, calculator
- status: outline

Moves: "Even" → the first frame is greatest-hits-trophies' last: the tilted shelf, PREVIOUS on the sign, the giant trophy, "9,200× CHEAPER". "one percent" → a gauge on a pole drops in beside the giant trophy, "CHANCE OF PASSING", its needle high. "probability" → a gloomy everyday human in a raincoat, under his own little raincloud, jumps up, grabs the needle and hangs on it with his whole weight until it sits on "1%". "you're" → still hanging there, he turns his head slowly and looks at the camera; in the corner, Wishonia gives the viewer the same flat look. "you)," → his raincloud zaps him: charred black and smoking, hair straight up, still hanging on the needle at 1%; only his eyes blink. "ninety-two" → the giant trophy shrinks to 1% of its size; its top comes into frame, and it is still far taller than the bed-net cup. "times" → the yardstick folds back down, click by click, to the shrunken trophy's top. "better" → its flag flips: "92.1× BETTER". "anti-malaria" → the Calculator peeks in from the right edge: a strip of tape across its cracked display, a gap in its keypad where the "=" key was. "nets." → it reads the yardstick. after "nets." → a smaller scream, the tape pops off, and it walks off the right edge again; a crash offscreen, and a second key bounces back into frame.

Sound: a clank as the gauge drops in; a slide-down as the needle is hauled to 1%; a huff as he strains; silence for the look; a zap and a sizzle as the raincloud strikes; a slide whistle down and a pop as the trophy shrinks; yardstick clicks; a ding on 92.1×; a boing as the Calculator peeks in; a small yelp, a pop for the tape, squeaky steps, a clank offscreen and a pop for the key.

On screen: "CHANCE OF PASSING: 1%" / "92.1× BETTER". Why: the worst-case answer, so a skeptic has nothing left to subtract.
