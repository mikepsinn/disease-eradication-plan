---
format: 1920x1080
duration: 3:56.9
message: "Earth may be eligible for optimization: its species only does things for paper, and it spends 604 papers on weapons for every 1 on testing which medicines work."
arc: Theme song music video → title card → the Reaper squeezes into the family portrait → one small Earth under 122 nuclear winters → Wishonia at her console: the stamp, her nameplate, 4,297 years → what she noticed (the atom cut, fire on fire, EARTH crossed out to DIRT, the Pentagon) → a town that moves only for papers → the 604 bar
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 1, "Opening"
audio: index-manual.7ce6b2b2.mp3, 00:00.0 to 03:56.9
version: v3
---

# Part 1 storyboard: "Opening"

- **Source:** `index-manual.qmd`, the opening, from "Is everyone you've ever loved" to the 604 line (everything before "### The Human Economy"). It links no `knowledge/` pages; its two numbers come from `knowledge/appendix/parameters-and-calculations.qmd`.
- **The numbers:**
  - `nuclear_winter_overkill_factor`: 122. It is `global_warhead_count` (12,241 warheads) over `nuclear_winter_warhead_threshold` (100 warheads, about what one nuclear winter takes). So on the chart one nuclear winter is one crate of 100 warheads, and the arsenal is 122 crates. One crate is enough; 121 are spare.
  - `military_to_government_clinical_trials_spending_ratio`: 604. It is `global_military_spending_annual_2024` ($2.72 trillion) over `global_government_clinical_trials_spending_annual` ($4.5 billion). The narrator says only "604 papers" and "one paper", so the chart shows 604 and 1, no dollars.
  - From the text, not variables: 1945 (the atom) and 4,297 years (Wishonia's career, in either unit).
- **What the viewer must leave with:** Earth qualifies for optimization because its humans only do things when handed paper, and they hand 604 papers to weapons for every 1 that tests which medicines work.
- **Plates:**
  - `family-portrait`: a Victorian studio photograph being taken: a family of four stiff on a horsehair sofa, the photographer under his black cloth.
  - `tiny-earth`: a bar chart on aged paper, "NUCLEAR WINTERS" against "CIVILIZATIONS", with one small Earth.
  - `atom-globe`: the atom on a velvet cushion, and a classroom globe that rises between Uncle Sam and the Soviet general (split-the-atom and pointing-at-each-other; as built in the approved pilot, `parts/pilot-collage.json`).
  - `cave`: a cave mouth and a campfire.
  - `four-buildings`: four lots in a row on a plain field.
  - `town-square`: paving stones and ten idle townsfolk.
  - `papers-street`: one long street the camera travels along; the left half has no papers, the right half floods with war papers.
  - `604-bar`: a two-bar chart on aged paper whose first bar is taller than the sky.
  - Host scenes (eligible, meet-wishonia, my-surprise, earth-means-dirt): Wishonia at her console on the observation deck, Earth hanging in the glass behind her (`KIT.STUDIO.earth`).
- **Cast:** existing: `atom`, `globe`, `mushroom`, `scientist` (with his giant shears), `uncle-sam`, `general`, `reaper` (`assets/art/reaper/`: `hug`, `face-grin`). New: `family`, `family-skeleton`, `photographer`, `germ`, `warhead`, `crate`, `snowflake`, `small-earth`, `frozen-man`, `light-bulbs`, `caveman`, `campfire`, `pentagon`, `paint-roller`, `grumpy-missile`, `hospital`, `schoolhouse`, `doghouse`, `democracy-dog`, `bill-plain`, `citizen`, `patient`, `lab-bench`, `spider`, `hungry-man`, `moth`, `weapons-maker`, `bomb`, `general`, `war-map`, `fat-cat`, `oil-derrick`, `bill-war`, `bill-med`, `balloon`, `you`; skeletons of the patient, the Scientist and the hungry man (`scientist` exists).
- **Callbacks:** none from earlier parts; this is the first. Later parts pay off: the case file and its DIRT tab (Parts 4, 12, 26, 27), the Reaper (Parts 5, 6, 8), the 604 chart (Parts 6, 7, 10, 25), the busy man in the fedora as YOU (Part 10 on), the Democracy Dog (Part 6), the moth (Part 2), the cavemen (Part 3).
- **New art:**
  - the Victorian family of four on the sofa (father, mother, the boy between them, the grandfather standing behind, in spectacles), and the same four as skeletons in the same clothes and poses
  - the photographer: a box camera on legs, him under its black cloth with a flash-powder tray held up
  - engraved disease germs, in the style of Victorian microscope plates (a cholera comma, a plague rod, a spiky virus)
  - a plain 1950s warhead; a wooden crate stenciled "100"; an engraved ice-blue snowflake
  - a small Earth with a little house and a picket fence on top, the little man in a scarf with a watering can, and him frozen in a block of ice
  - a row of Edison light bulbs, lit and unlit
  - two cavemen in pelts, each with a burning branch; a campfire, lit and unlit; a cave mouth
  - the Pentagon seen from above, with a sign on two posts; a paint roller; a grumpy missile (arms crossed, scowling)
  - a rectangular hospital, a square schoolhouse with a bell, a triangle doghouse, and the Democracy Dog's head
  - a dollar bill on stick legs with George Washington in the oval (his eyelid a separate piece), and the same bill blank
  - ten Victorian townsfolk with hinged heads and arms (a baker, a sweeper, a fence painter among them), and one flattened like a pancake
  - the patient in a dressing gown with a thermometer, the lab bench with a flask and a cobweb, a spider on a thread, the hungry man with an empty wallet, a moth
  - the Weapons Maker at a workbench with a bomb that swells; two generals at a war-map table with toy soldiers
  - the fat cat (top hat, monocle, cigar) at an oil derrick on a little globe, papers gushing from it
  - the war bill (green, missile seal, stick legs), the medicine bill (cross seal), and the medicine bill flattened with one arm out
  - a Victorian hot-air balloon with its balloonist
  - YOU (`you`), the busy man in a fedora with a pocket watch, and his skeleton in the same fedora
- **Kit additions:**
  - `chart`: axes, gridlines, axis labels and a title on aged paper.
  - `stack`: copies of a cut-out hop onto one another into a column, faster and faster, the camera able to tilt with it.
  - `walk`: a cut-out on stick legs walks along a path, legs flicking on twos.
  - `xray`: a cut-out flickers with its skeleton for four drawings and stays the skeleton.
  - `burn`: cut-out flames flicker on a cut-out until put out.
  - `print`: the plate becomes a developed photo print: a deckled white border, tilted, after a white flash.
  - Host props for `KIT.studio`: the case file on the console ledge, the pencil, the stamp, the PLANETS out-tray, the marker, the nameplate, the hanging card and the unit converter; Earth in the window wobbling, and swapping to a clod of dirt for a beat.

## Scene 1 · theme-music-video

- id: theme-music-video
- act: Theme song and title
- transition_in: the video starts
- cue: the start of the MP3 (the theme song)
- time: 00:00.0 to 01:40.3 (100.3 s)
- voiceover: "You're here. Your organs are failing. And your death is drawing near. But if you bribe the right politicians in the right order at the right time, you can trade the nuclear warheads for medicine. And it's not even a crime."
- layer: the existing music video, not drawn
- status: built

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "You're here. Your organs are failing. And your death is drawing near. But if you bribe the right politicians in the right order at the right time, you can trade the nuclear warheads for medicine. And it's not even a crime." | The whole plan, sung. | The existing theme song music video, as made: 15 clips, one per lyric line, scaled to 1920 × 1080. Its last frame holds the 0.7 s before "How". | The song's own. |

Sound: the theme song itself; the video plays muted under the MP3.

## Scene 2 · title-card

- id: title-card
- act: Theme song and title
- transition_in: cut on the music's last note
- cue: "How"
- time: 01:40.3 to 01:48.8 (8.5 s)
- voiceover: "How to End War and Disease (for Busy People) A Step-by-Step Guide to Optimizing Your Terrible Civilization"
- layer: A, title card
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "How to End War and Disease" | The book's title. | The period card: the atom emblem on plain navy; the heading slams in one word per spoken word. | |
| "(for Busy People)" | It is short. | "(for Busy People)" slides in under it. YOU, the busy man in a fedora, sprints across the bottom of the card, left to right, eyes on his pocket watch. | |
| "A Step-by-Step Guide to Optimizing Your Terrible Civilization" | | The subtitle pill comes in. His skeleton, in the same fedora, strolls back the other way, slowly, still checking the watch. | He was too busy to read it, and now he has all the time in the world. |

Sound: a whirr as the card comes up; a thunk on "Disease"; a quick whistle as he sprints on "Busy"; a slow tick-tock under the skeleton from "Step-by-Step".

## Scene 3 · loved-ones

- id: loved-ones
- act: Eligibility check
- transition_in: cut
- cue: "Is"
- time: 01:48.8 to 01:58.0 (9.2 s)
- voiceover: "Is everyone you've ever loved currently being slowly tortured and or brutally murdered by horrible diseases? Do your governments"
- layer: B, plate family-portrait
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Is everyone you've ever loved" | Your family. | A Victorian portrait sitting: the family of four stiff on the sofa, staring into the lens; at the right edge, the photographer under his black cloth, the flash tray up. | Nobody smiles; it is a Victorian photograph. |
| "currently being slowly tortured" | Diseases are at work in them right now. | Engraved germs crawl in from the edges, a cholera comma, a plague rod, a spiky virus, and climb into the family's collars and ears, one each. The family holds perfectly still for the exposure. | The grandfather's eye twitches. Nobody moves. |
| "and or brutally murdered" | And they kill. | The Grim Reaper rises behind the sofa between the grandfather and the mother, grinning, and puts a bony arm round each of them. | |
| "by horrible diseases?" | | He squeezes them in for the picture. After "diseases?" the flash powder goes off: a white flash and a puff of smoke. It clears on the developed print, deckled white border, tilted: the same four poses, now skeletons in the same clothes, the grandfather's spectacles still on his skull. The Reaper is the only one unchanged. | A Victorian memorial photograph, a real genre: the dead posed with the living, except here only Death is living. |
| "Do your governments" | | HOLD on the print: nothing moves and nothing sounds until nuclear-winters cuts in on "waste". | |

Sound: a scratchy whoosh as the Reaper rises on "brutally"; the flash-powder whump after "diseases?"; then silence.

## Scene 4 · nuclear-winters

- id: nuclear-winters
- act: Eligibility check
- transition_in: cut
- cue: "waste money"
- time: 01:58.0 to 02:06.9 (8.9 s)
- voiceover: "waste money on enough nuclear bombs to cause one hundred and twenty-two nuclear winters despite only having the one civilization to apocalypse?"
- layer: B, plate tiny-earth
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "waste money on enough nuclear bombs" | Governments buy warheads. | A bar chart on aged paper with two columns, "NUCLEAR WINTERS" and "CIVILIZATIONS", both empty. In front, the small Earth; the little man on top waters a flower by his door and waves. Warheads drop in from above, a price tag swinging from each nose, and clatter into a crate stenciled "100". | |
| "to cause one hundred and twenty-two nuclear winters" | 12,241 warheads; about 100 make one nuclear winter; so 122. | Each full crate frosts over into one big snowflake and hops onto the NUCLEAR WINTERS column. The snowflakes stack faster and faster, the column runs off the top of the frame, and the camera tilts up after it; "122" stamps at the top. | The crates fill so fast that one warhead misses, bounces off the rim and hops back in. |
| "despite only having the one civilization" | There is one civilization to end. | The camera drops back down. The small Earth hops onto the CIVILIZATIONS column: height 1. The little man looks up at the snowflake column towering over him and quietly puts on a scarf. | |
| "to apocalypse?" | One winter is enough. | The bottom snowflake falls on the Earth: snow buries the house, then the man to his chin, teeth chattering; he freezes solid in a block of ice, watering can in hand. The other 121 snowflakes stay stacked, with nothing left to freeze. | The next snowflake taps on his ice block, waiting its turn. |

Sound: a clank per warhead into the crate, speeding to a rattle; a crackle as each crate frosts; a thunk as "122" stamps in on "twenty-two"; wind on "despite"; chattering teeth on "civilization"; an ice ding on "apocalypse?"; a tiny tap-tap after it.

## Scene 5 · eligible

- id: eligible
- act: The verdict
- transition_in: iris in on Wishonia's face (the first time the film shows her)
- cue: "If"
- time: 02:06.9 to 02:11.1 (4.2 s)
- voiceover: "If so, your planet may be eligible for optimization."
- layer: A, host
- wishonia: happy-smile + body-presenting; happy-smile + body-palms-down on "eligible"
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "If so," | You answered yes twice. | The iris opens on Wishonia at her console, Earth in the glass behind her. On the ledge, the case file "EARTH: CASE #847"; its cover is a mail-in form, "PLANET ELIGIBILITY CHECK", two YES/NO boxes and no questions. A pencil ticks YES, YES, by itself. | The fine print: "Please allow 4 to 6 weeks for optimization." |
| "your planet may be eligible" | Earth qualifies. | The rubber stamp hops up off the ledge; she huffs on it. On "eligible" it slams down: "MAY BE ELIGIBLE FOR OPTIMIZATION", in red, across the form. | Earth in the window jolts on its string with the thump. |
| "for optimization." | | She blows on the wet ink and drops the file into the wire tray "PLANETS" at the end of the ledge, on top of "VENUS: TOO HOT" and "MARS: NOBODY HOME". | |

Sound: a pencil scratch per tick on "so,"; a huff before "eligible"; a stamp thunk on "eligible"; a whoosh into the tray after "optimization.".

## Scene 6 · meet-wishonia

- id: meet-wishonia
- act: Meet Wishonia
- transition_in: same shot (no seam)
- cue: "I'm"
- time: 02:11.1 to 02:25.8 (14.7 s)
- voiceover: "I'm Wishonia Love. C.E.O. and President of Universe Optimization Services. I've been upgrading civilizations for four thousand, two hundred and ninety-seven years, which in your Earth time is four thousand, two hundred and ninety-seven years."
- layer: A, host
- wishonia: happy-smile + body-hand-chest; smirk-smile + body-open-palms on "Earth"; smirk-closed + body-idle on "years." (second), the look at the camera
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "I'm Wishonia Love." | Who is talking. | A brass nameplate slides onto the front of the console: "WISHONIA LOVE". | |
| "C.E.O. and President" | | A second line clicks in under it: "C.E.O. AND PRESIDENT". | |
| "of Universe Optimization Services." | | A third line, "UNIVERSE OPTIMIZATION SERVICES"; the nameplate slides out sideways to fit it, past the end of the console and out of frame, sagging like a diving board. | |
| "I've been upgrading civilizations for four thousand, two hundred and ninety-seven years," | 4,297 years. | A card drops in on two strings beside her: "4,297 YEARS". | |
| "which in your Earth time" | | A brass unit converter rises onto the ledge: two dials, a crank, a bell, a card slot and a little chimney. The card feeds itself in; the dials spin, the gears whirr, it shakes and glows red. | |
| "is four thousand, two hundred and ninety-seven years." | The units are the same. | 1.1 s after "Earth" it blows up: a white flash and a little mushroom cloud on the ledge. It clears on a charred, bent wreck; two white eyes blink in the soot. After "years." its bell dings and it spits out a singed card: "4,297 YEARS". She looks at the camera. | It died converting a number into itself. |

Sound: a slide whoosh per nameplate line, a longer one on "Universe"; whirring gears on "Earth"; a boom 1.1 s after it; a bell ding after "years." (second); then silence for the look.

## Scene 7 · split-the-atom

- id: split-the-atom
- act: What Wishonia noticed
- transition_in: cut
- cue: "I started watching"
- time: 02:25.8 to 02:41.9 (16.1 s)
- voiceover: "I started watching your planet in nineteen forty-five when you split the atom. "Atom" comes from your Greek word meaning "unable to be cut," so naturally, you cut it. This was very human of you. I assumed you were trying to unlock unlimited free energy."
- layer: B, plate atom-globe
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "I started watching your planet in nineteen forty-five" | Earth got interesting in 1945. | The atom on a red velvet cushion on a pedestal, humming, its electrons whizzing. "1945" stamps in above it. | |
| "when you split the atom." | | The atom shivers. | |
| ""Atom" comes from your Greek word" | | "1945" falls away. A tag on a string pops onto the atom: "ATOMOS". | |
| "meaning "unable to be cut,"" | The word means uncuttable. | "UNABLE TO BE CUT" stamps onto the tag. | |
| "so naturally, you cut it." | So humans cut it at once. | The Victorian scientist slides in, his giant shears open round the atom. He reads the tag and looks at us. On "cut": SNIP. The atom falls apart into two glowing halves, and the tag drops. | He reads the tag first. |
| "This was very human of you." | | He bows, proud, shears up. | His pipe is still lit. |
| "I assumed you were trying to unlock" | Splitting it releases energy. | He slides off. The halves drift apart and hop. | |
| "unlimited free energy." | Enough to power everything. | A sunburst turns behind the halves, and a row of Edison bulbs along the bottom lights up one by one; "FREE ENERGY!" slams in on a card. | |

Sound: a thunk as "1945" stamps in; a rattle on "split"; a stamp thunk on "unable"; a snip on the second "cut"; a rising hum on "unlimited"; a light-switch click per bulb from "free".

## Scene 8 · my-surprise

- id: my-surprise
- act: What Wishonia noticed
- transition_in: cut
- cue: "You can imagine"
- time: 02:41.9 to 02:43.1 (1.2 s)
- voiceover: "You can imagine my surprise"
- layer: A, host
- wishonia: neutral-smile + body-open-palms; surprised-oh + body-open-palms on "surprise"
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "You can imagine" | | Wishonia at the console, polite. | |
| "my surprise" | She did not expect what came next. | A 1950s crash zoom onto her surprised face; it holds. | |

Sound: a slide whistle up on the zoom.

## Scene 9 · pointing-at-each-other

- id: pointing-at-each-other
- act: What Wishonia noticed
- transition_in: cut back to the plate on split-the-atom's last frame (same plate, no seam)
- cue: "when"
- time: 02:43.1 to 02:46.4 (3.3 s)
- voiceover: "when I realized you were just pointing it at each other! That's kind of like"
- layer: B, plate atom-globe
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "when I realized" | | The sunburst shuts. Uncle Sam slides in from the left, the Soviet general from the right, and the classroom globe rises between them; each glowing half flies into one man's raised hand. | The bulbs go out. |
| "you were just pointing it" | They made it a weapon. | Each jabs his half at the other across the top of the globe. | |
| "at each other!" | Aimed at each other. | Sparks zigzag between the halves. On "other!" a white flash, a shake, and a mushroom cloud stands on the globe; both men and the globe are charred black. | |
| "That's kind of like" | | Both blink white eyes, then fold down into two little heaps of ash, the eyes on top, blinking again. | |

Sound: a hum as they aim on "pointing"; a zap of sparks on "each"; a boom on "other!"; a sizzle as they fold to ash on "kind".

## Scene 10 · fire-on-fire

- id: fire-on-fire
- act: What Wishonia noticed
- transition_in: cut
- cue: "discovering"
- time: 02:46.4 to 02:51.6 (5.2 s)
- voiceover: "discovering fire and then immediately using it to set yourself on fire."
- layer: B, plate cave
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "discovering fire" | Humans found fire. | A cave mouth. Two cavemen crouch over a campfire as it lights; they warm their hands and grin. | |
| "and then immediately using it" | | Each pulls a burning branch out of the fire. | |
| "to set yourself on fire." | And used it on each other first. | They jab each other, one at the head, one at the belly, and both go up in flames, arms up, running in circles round the fire. On "fire." the flames go out in a puff: two charred cavemen, blinking. | After "fire." they look at each other, look at the campfire, and each reaches in for a new branch. |

Sound: a whoosh as the fire lights; a second whoosh and two yelps as they catch on "set"; a sizzle on the last "fire.".

## Scene 11 · earth-means-dirt

- id: earth-means-dirt
- act: What Wishonia noticed
- transition_in: cut
- cue: "The second thing"
- time: 02:51.6 to 03:01.7 (10.1 s)
- voiceover: "The second thing I noticed is that your planet is named "Earth," which means dirt. You named your planet.. dirt. Okay, if that's what you want..."
- layer: A, host
- wishonia: skeptical-closed + body-idle; skeptical-closed + body-shrug on "want..."
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The second thing I noticed" | | The case file hops out of the PLANETS tray onto the ledge. | |
| "is that your planet is named "Earth,"" | | The camera pushes in on its tab: "EARTH: CASE #847". | |
| "which means dirt." | The name means soil (Old English *eorþe*). | A red marker crosses out EARTH, by itself. | |
| "You named your planet.. dirt." | | It writes "DIRT" above it. | For a beat, the Earth in the window behind her is a clod of dirt, then it is the Earth again. |
| "Okay, if that's what you want..." | | She shrugs. The file hops back into the tray, and a puff of brown dust comes up out of it. | |

Sound: a marker squeak on each "dirt."; a thunk and a puff as the file lands after "want...".

## Scene 12 · pentagon

- id: pentagon
- act: What Wishonia noticed
- transition_in: cut
- cue: "I also noticed"
- time: 03:01.7 to 03:10.6 (8.9 s)
- voiceover: "I also noticed that you call your war building "The Pentagon" because it has five sides (this is like naming a hospital "Rectangle" or calling a school "Square")."
- layer: B, plate four-buildings
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "I also noticed that you call your war building" | It is the building that runs the wars. | On the first lot, an honest sign springs up: "WAR BUILDING". The Pentagon, seen from above, drops in round its posts; a grumpy missile peeks up out of the courtyard. | |
| ""The Pentagon"" | | A paint roller rolls "THE PENTAGON" over the old words; the paint drips. | |
| "because it has five sides" | It is named for its shape. | Its five walls flash, one after another. The missile looks left, right, scowls at us and ducks. | |
| "(this is like naming a hospital "Rectangle"" | | The camera travels right: a rectangular hospital drops onto the next lot, "RECTANGLE" on its cornice. | |
| "or calling a school "Square")." | | A square schoolhouse drops in: "SQUARE". After "Square" the camera pulls back on the row, and a fourth building nobody mentioned drops in: a triangle doghouse, "TRIANGLE". The Democracy Dog pokes its head out. | |

Sound: a pop as the sign springs up; a splat as the roller hits; a tick per wall; a slide whistle down as the missile ducks; a thunk per building; a small woof.

## Scene 13 · papers-with-presidents

- id: papers-with-presidents
- act: The papers
- transition_in: cut
- cue: "However,"
- time: 03:10.6 to 03:56.9 (46.3 s)
- voiceover: "However, the most fascinating discovery about your species is that you only do things when given small pieces of paper with presidents on them. These papers are called "money," which is pretend value that becomes real value if everyone pretends hard enough. Without these papers, you won't: Save lives (requires many papers). Cure diseases (requires very many papers). Feed hungry people (requires papers). But WITH these papers, you will: Build bombs (you love giving papers for this). Start wars (somehow this makes more papers). Destroy the planet (surprisingly profitable in papers). In fact, your governments spend six hundred and four papers on weapons for every one paper on testing which medicines work."
- layer: B, plate one-street
- bit: **One bill walks down a street of frozen humans, and only what it touches comes alive.** The camera walks with it, close and big: past the people it would save, without slowing, to the Weapons Maker, the war and the burning Earth. Then it climbs a tower of 604 bills and drops to the one lonely bill on the floor.
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "However, the most fascinating discovery about your species is that you only do things" | Humans act only for paper. | Baker and sweeper, big and stock-still. | A pigeon lands on the sweeper; a cobweb stretches between the two men. |
| "when given small pieces of paper with presidents on them." | | The bill struts in, huge. Whoever it passes works like mad, then stops dead. | The pigeon bolts. Washington winks on "them." |
| "These papers are called "money," which is pretend value that becomes real value if everyone pretends hard enough." | Its value is what everyone agrees it is. | The crowd's whole bodies snap toward it. The ink drains to blank paper; they squeeze their eyes shut and it inks back and glows. | The matron pretends so hard her head comes off, and lands upside down. |
| "Without these papers, you won't: Save lives (requires many papers). Cure diseases (requires very many papers)." | Saving lives costs papers. | The bill walks on without slowing. The patient, then the scientist, each lunges after it, big. | Each is a grinning skeleton behind it, still reaching. |
| "Feed hungry people (requires papers)." | Food costs papers. | The hungry man lunges after it. | Skeleton. |
| "But WITH these papers, you will: Build bombs (you love giving papers for this)." | Bombs get paid for gladly. | The frozen Weapons Maker springs to life; the bill flies onto his anvil and a bomb swells on each word. | After "this)." it goes off; he stands charred, blinking, still hammering. |
| "Start wars (somehow this makes more papers)." | War makes money. | A tank fires; the soldiers char mid-salute, blinking. A second cloud. | Bills fly out of the mushroom clouds. |
| "Destroy the planet (surprisingly profitable in papers)." | Wrecking the planet pays. | A big terrified Earth catches fire. | Bills pour out of its mouth into the Fat Cat's hat. |
| "In fact, your governments spend six hundred and four papers on weapons" | 604 papers to weapons... | The hat overflows and a stack of bills boils up beside him. The camera climbs it, past clouds and a warplane, to the top: "604". | A furious balloonist, and the same pigeon. |
| "for every one paper on testing which medicines work." | ...for every 1. | The camera drops all the way down to one medicine bill on the floor: "604 : 1". It looks up. | One war bill drifts down like a leaf, then drops like an anvil and flattens it. Its little arm pokes out and waves. |

Sound: pigeon pat; squeak for the bill; scratch and marker for the work; pop on "them."; sizzle as the ink drains, hum as they strain; pop on "hard", thunk as the head lands; crickets on "Without"; a zap per skeleton; hammer; pops as the bomb grows; booms; cash register on "profitable"; slide up and whoosh for the climb; stamp on "papers" and "one"; slide down for the drop; splat; squeak.

