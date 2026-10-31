---
format: 1920x1080
duration: 1:22.8
message: "A $1 billion campaign that gets treatments to patients 212 years sooner returns 7.53 million to one, at two cents per healthy year of life."
arc: Title card (the Calculator peeks over MATH) → at the console, the Calculator warms up like a prize fighter → one plate: the queue of the dead fills back in, the fat cat prices them, the blobs are bowled off the globe, a mountain of money, and dividing by a billion knocks nine zeros off the sky onto the campaign's bundle → the Calculator screams and steps off the ledge → the hall of greatest hits: the giant treaty trophy breaks the shelf → the pessimist hangs the gauge on 1%, and the shrunken trophy still towers → the Calculator peeks back, screams smaller and loses a second key
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 16, "The Math"
audio: index-manual.cbaf659d.mp3, 34:20.6 to 35:43.4
version: v3
---

# Part 16 storyboard: "The Math"

**Source:** `index-manual.qmd` "The Math"; its numbers come from `knowledge/solution/dfda.qmd` and the parameters below.

**The numbers (from `_variables.yml`):**
- `dfda_trial_capacity_plus_efficacy_lag_years` 212 years sooner (from Part 14).
- `standard_economic_qaly_value_usd` $150,000 per healthy year of life.
- `dfda_trial_capacity_plus_efficacy_lag_dalys_discounted` 50.2 billion healthy years × $150,000 = `dfda_trial_capacity_plus_efficacy_lag_economic_value` $7.53 quadrillion ($7,530,000,000,000,000).
- ÷ `treaty_campaign_total_cost` $1 billion = `treaty_roi_trial_capacity_plus_efficacy_lag` 7.53 million to 1: knock nine zeros off.
- `treaty_cost_per_daly_trial_capacity_plus_efficacy_lag` $0.02 per healthy year ($1 billion ÷ 50.2 billion years) against `bed_nets_cost_per_daly` $184: `treaty_vs_bed_nets_multiplier` 9,200×. In pennies: a stack of 2 against a tower of 18,400.
- Return per dollar: `childhood_vaccination_roi` 10.9, `smallpox_eradication_roi` 159, the treaty 7,530,000, which is 47,000 times smallpox's.
- `political_success_probability` 1%: the expected cost per healthy year is 100 times more, about $2, a stack of 200 pennies, and the tower of 18,400 is still `treaty_expected_vs_bed_nets_multiplier` 92.1 times taller.

**What the viewer must leave with:** a $1 billion campaign that gets treatments to people 212 years sooner returns 7.53 million to 1, buys a healthy year for 2 cents (9,200 times cheaper than bed nets), and still beats bed nets 92 times if it has a 1% chance.

**Plates:**
- Host scenes (host-remembers, calculator-scream, calculator-returns): Wishonia at her console on the observation deck, Earth in the window, the Calculator on the right end of the ledge.
- math-field: a field under a wide sky: a queue of patients at the front, open ground that fills with price-tagged hourglasses to the horizon, and sky for the number.
- hall-of-hits: a hall-of-fame wall with a marquee, "GREATEST HITS IN NOT DYING"; on the left a penny chart (cost of one healthy year), on the right a column chart (return per dollar) with a gold cup on each column.

**Cast:** existing: `gauge` and `needle` (the 1% meter), `scientist`, `globe`. New: `pill-bottle` (a pill bottle riding Part 14's `arrow-sign`), `patient` (chest light red, then teal), `hourglass`, `fat-cat` with a roll of `price-tag`, `money-bundle` (a strapped bundle of plain green bills on stick legs), `zero` (one big stamped digit that can fall), `penny`, `bed-net-cup` (a gold cup under a little net, a tiny human asleep in it), `mosquito`, `smallpox-cup`, `vaccine-cup` (a syringe for a handle), `treaty-column`, `germ`, `magnifier`, `pessimist` (a gloomy man in a raincoat) with his own `raincloud`, `marquee`.

**Callbacks:**
- Part 14: the 212 years (the narrator: "Remember the two hundred and twelve years") and its fat arrow sign, "212 YEARS SOONER", which a pill bottle now rides like a rocket.
- Set up here: the Calculator's cracked, taped display and the two keys it loses (Part 19, it-is-arithmetic; Part 22).

**New art:** every new cut-out in the cast list. Host props, drawn in the host style: the Calculator (`KIT.props.calculator`) with its tape, its cracked and taped display, its "=" key and a second loose key, and the coffee mug.

**Kit additions:**
- A chart move: axes and value tags on aged paper, and a flag at the top of a bar.
- A stack move: copies of a cut-out (pennies) stacked into a column that grows to a count, faster as it goes, with the camera following its top.
- A pictogram move: copies of a cut-out tiling a field row by row to the horizon, then all swapping to another cut-out (hourglass to money).
- A stamped number that types in one character per thump, and characters that fall off it one by one.
- A column that punches up through the top of the frame and through a shelf, with what stood on it sliding off.

## Scene 1 · the-math-title

- id: the-math-title
- act: Title
- transition_in: up from black (the head of a reel)
- cue: "The Math."
- time: 34:20.6 to 34:22.4 (1.8 s)
- voiceover: "The Math."
- layer: A, title card
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "The Math." | The heading. | The period title card: "THE" over "MATH" under the emblem. After "Math.", the Calculator pops up behind "MATH", only its display and eyes over the letters, display "0". | Its eyes read the heading left to right, a bead of sweat flies off, and it ducks. |

Sound: the projector whirr; a boing as it pops up; a pop as it ducks.

## Scene 2 · host-remembers

- id: host-remembers
- act: The return
- transition_in: iris in on her face
- cue: "Remember the two hundred"
- time: 34:22.4 to 34:25.6 (3.2 s)
- voiceover: "Remember the two hundred and twelve years timeline shift?"
- layer: A, host
- wishonia: big, happy-smile + body-presenting; skeptical-smile + body-hands-hips on "shift?"
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Remember the two hundred and twelve years timeline shift?" | Treatments arrive 212 years sooner (Part 14). | Wishonia at her console, the Calculator on the right end of the ledge. It punches in "212", a ripple of keys going down, then starts bouncing from foot to foot on its stick legs like a prize fighter before the bell. | A boxing bell rings twice after "shift?": round one. |

Sound: a key click on "two", "hundred" and "twelve"; the bell, twice.

## Scene 3 · quadrillion-equation

- id: quadrillion-equation
- act: The return
- transition_in: cut
- cue: "Treatments reaching patients"
- time: 34:25.6 to 34:55.0 (29.4 s)
- voiceover: "Treatments reaching patients that many years sooner means billions of people gain years of healthy life. Value each of those life-years at one hundred and fifty thousand dollars (the standard economic valuation), multiply across the global disease burden over the acceleration window, and you get seven point five three quadrillion dollars in total economic value. Divide that by the one billion dollars campaign cost, and you get a return of seven point five three million to one."
- layer: B, plate math-field
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Treatments reaching patients that many years sooner" | The 212 years, delivered. | A pill bottle roars in riding Part 14's fat arrow sign, "212 YEARS SOONER", like a rocket. It sprays bottles down a queue of patients with red chest lights; each catches one, and the lights go teal. | |
| "means billions of people gain years of healthy life." | Each cured person gets healthy years back. | Over each patient's head pops a little stack of hourglasses, one per healthy year. The camera pulls back along the queue to the horizon, hourglasses popping all the way. | |
| "Value each of those life-years at one hundred and fifty thousand dollars (the standard economic valuation)," | Each healthy year is priced at $150,000. | The fat cat waddles down the line with a fat roll of price tags, tears one off, licks it, and slaps it on the first hourglass: "$150,000". Lick, slap, lick, slap down the line. | His eyes ring up dollar signs. |
| "multiply across the global disease burden over the acceleration window," | 50.2 billion healthy years in all. | The tagged hourglasses multiply into rows that tile the whole field to the horizon, popping in like a times table. | He licks faster and faster until his tongue hangs out. |
| "and you get seven point five three quadrillion dollars in total economic value." | $7.53 quadrillion. | Every hourglass flips into a bundle of green money; the camera pulls up and back over a field of money to the horizon, and a stamp machine-guns "$7,530,000,000,000,000" into the sky, one character per thump. | The camera has to keep pulling back to fit the zeros. |
| "Divide that by the one billion dollars campaign cost," | The campaign costs $1 billion. | At the field's edge, one small bundle walks in on stick legs, tagged "$1 BILLION". It looks up, and up, at the number, and gulps. | |
| "and you get a return of seven point five three million to one." | Dividing by a billion knocks nine zeros off. | The number shakes; the "$" and then its last nine zeros drop off its end one by one, and the sky reads "7,530,000 : 1". | The falling zeros land on the little bundle and bury it; its legs kick out of the heap. |

Sound: a rocket whoosh and a crash; a run of soft pops as the lights turn; squeaky footsteps and a run of lick-slaps; a cash-register ding for the dollar eyes; a rolling patter as the field fills; a fast run of stamp thumps; a gulp; a whistle and a thunk for each falling zero; a stamp for ": 1".

## Scene 4 · calculator-scream

- id: calculator-scream
- act: The return
- transition_in: cut
- cue: "Your calculator will display"
- time: 34:55.0 to 35:02.7 (7.7 s)
- voiceover: "Your calculator will display an error, emit a tiny electronic scream, and attempt to leave the desk. This is correct."
- layer: A, host
- wishonia: big, happy-smile + body-hands-hips; smirk-closed + body-idle on "desk." (the sip); happy-closed + body-hands-hips on "correct."
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Your calculator will display an error," | The number is too big for a calculator. | Back at the console: the Calculator, drenched in sweat, smoke curling from its seams, a tape of zeros spooling out of it over the ledge. Its display flashes "ERROR". | |
| "emit a tiny electronic scream," | | Its mouth opens wide: shake lines and a tiny scream. | |
| "and attempt to leave the desk." | | It marches to the ledge's right edge, trailing its tape, and looks down. Wishonia raises her mug and sips. | |
| "This is correct." | The math is right. | She puts the mug down slowly, and the Calculator steps off the edge, its tape whipping after it. | A crash from below, and its "=" key bounces up, spins, and lands beside the mug. She does not look. |

Sound: an electric zap on "error,"; a tiny yelp of a scream; squeaky footsteps; a falling whistle, a crash and a pop as the key lands.

## Scene 5 · greatest-hits-trophies

- id: greatest-hits-trophies
- act: Cost-effectiveness
- transition_in: cut
- cue: "Cost-effectiveness: two cents"
- time: 35:02.7 to 35:30.2 (27.5 s)
- voiceover: "Cost-effectiveness: two cents to save one year of healthy human life. Anti-malaria bed nets, the gold standard for keeping humans alive, cost one hundred and eighty-four dollars. This is nine thousand two hundred times cheaper. It beats smallpox eradication (one hundred and fifty-nine to one) and childhood vaccinations (ten point nine to one), which were humanity's previous greatest hits in the "not dying" genre."
- layer: B, plate hall-of-hits
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Cost-effectiveness: two cents to save one year of healthy human life." | A healthy year costs 2 cents. | The hall's penny chart: on its baseline, a stack of just two pennies, too small to see. The Scientist bends over it with a magnifying glass; the camera pushes in through the glass: "2¢". | |
| "Anti-malaria bed nets, the gold standard for keeping humans alive," | Bed nets are the best buy known. | Beside it, on the baseline, the bed-net cup: a gold cup under a little net, a tiny human asleep in it. A gold star slaps onto it. | A mosquito dive-bombs the net and bounces off dizzy; the sleeper does not wake. |
| "cost one hundred and eighty-four dollars." | A healthy year by bed net costs $184. | A tower of pennies stacks up behind the cup, faster and faster, off the top of the wall; tag "$184". | |
| "This is nine thousand two hundred times cheaper." | 9,200×. | The camera tilts up the tower, past the marquee, to a flag at its top: "9,200×". | The tower sways; the Scientist steadies it with one finger. |
| "It beats smallpox eradication (one hundred and fifty-nine to one)" | Return per dollar: smallpox 159. | The camera travels right to the column chart: the smallpox cup on a column 159 units tall, tag "159 : 1". | The cup stamps down on a germ under it: splat, flat as a pancake, eyes blinking. |
| "and childhood vaccinations (ten point nine to one)," | Vaccines 10.9. | The vaccine cup on a column 10.9 units tall, tag "10.9 : 1". | A germ climbs its side; the syringe handle jabs it, and it pops. |
| "which were humanity's previous greatest hits in the "not dying" genre." | The treaty's 7.53 million to 1 dwarfs both. | The marquee lights up, "GREATEST HITS IN NOT DYING". Between the two cups the floor bursts and the treaty's column punches up out of the top of the frame, tagged "7,530,000 : 1"; both cups slide off their columns and clink together at its base. A strip slaps across the marquee: "PREVIOUS". | One bulb pops and goes out. |

Sound: a ding as the glass reads "2¢"; a slap for the star; a mosquito whine and a boing; a rising patter of pennies; a ding for the flag; a splat; a pop and a yelp; a sparkle for the marquee, a crash of floorboards, two clinks, a stamp slap, a pop for the bulb.

## Scene 6 · one-percent-chance

- id: one-percent-chance
- act: Cost-effectiveness
- transition_in: same plate (no seam)
- cue: "Even if you assume"
- time: 35:30.2 to 35:39.9 (9.8 s)
- voiceover: "Even if you assume only a one percent probability of the treaty actually passing (because you're you), the expected return is still ninety-two point one times better"
- layer: B, plate hall-of-hits
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "Even if you assume only a one percent probability of the treaty actually passing" | Suppose it has a 1% chance. | The camera travels back to the penny chart. The brass gauge drops in beside it, needle high. The pessimist (raincoat, his own little raincloud) trudges in, jumps, grabs the needle and hangs his whole weight on it until its window reads "1%". | His feet dangle. |
| "(because you're you)," | | He turns his head slowly and looks at the camera. | His raincloud zaps him with lightning: charred, smoking, still hanging on the needle at 1%; only his eyes blink. |
| "the expected return is still ninety-two point one times better" | A 1% chance makes each year 100 times dearer, and it is still 92.1 times cheaper. | The two-penny stack grows a hundredfold into a short column of 200 pennies. The bed-net tower still runs off the top of the frame beside it; a flag between them: "92.1×". | |

Sound: a clank as the gauge lands; a whistle down as the needle is hauled to 1%; a zap and a sizzle; a rising patter of pennies; a ding on "92.1×".

## Scene 7 · calculator-returns

- id: calculator-returns
- act: Cost-effectiveness
- transition_in: cut
- cue: "than anti-malaria bed nets."
- time: 35:39.9 to 35:43.4 (3.5 s)
- voiceover: "than anti-malaria bed nets."
- layer: A, host
- wishonia: big, smirk-smile + body-presenting; sideeye-closed + body-idle on "nets."
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "than anti-malaria bed nets." | Even the worst case is too much for a calculator. | At the console, the "=" key beside the mug. The Calculator peeks up over the ledge's right edge, a strip of tape across its cracked display, a gap where the "=" was, "92.1" on the display. It reads its own display; its mouth trembles open in a smaller scream and it drops back out of sight. Wishonia side-eyes the camera. | A crash from below, and a second key bounces up and lands beside the "=". The film irises out on her face. |

Sound: a boing as it peeks up; a small yelp; a crash and a pop as the second key lands.
