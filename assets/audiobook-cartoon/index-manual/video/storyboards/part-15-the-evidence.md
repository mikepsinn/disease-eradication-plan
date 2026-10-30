---
format: 1920x1080
duration: 1:41.2
message: "It has worked before: one trial ran 82 times cheaper during a pandemic, and after World War Two humans cut military spending 87.6% and got the biggest boom in history."
arc: Title card (the evidence lands on a crook) → Wishonia: a tower of forms to stop, one button to start → the pandemic ward does the science on fire while the calm room next door waits its patients to death → the war stack cut, the baby boom, the Weapons Maker flicks 1% off today's 30.6 stack with one hand → the empty podium, the theft acted out, the ovation, 65 years in two seconds → the studio, 65 years later
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 15, "Why This Could Actually Work: The Evidence"
audio: index-manual.cbaf659d.mp3, 32:39.5 to 34:20.6
version: v3
---

# Part 15 storyboard: "Why This Could Actually Work: The Evidence"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("recovery-trial: make the giant tag bigger"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The part is a 1950s atomic-age instructional film. Layer A is the host's studio set (`KIT.studio`): Wishonia large at her navy lectern, in front of the mustard wall and its spotlight pool. Layer B is the illustrated plates the camera travels over (`KIT.camera`), one framing per phrase; Wishonia is not in them, she is the voice. Money is green, and its seal says what it buys: a missile seal is war money, a cross seal is medicine money, no seal is plain money (`KIT.money("war" | "med" | "plain")`). Part 2 (`../parts/part-02.json`, `../compositions/scenes/part-02/`) is the reference for every kind of shot.

**Spine.** The tower of forms: the proof humans ask for before they stop doing something stupid. It thumps up beside Wishonia's lectern in proof-required and runs out of the top of the frame, while the Politician starts a war with one button and no paperwork at all. The three plates are the proof, already done: a trial 82 times cheaper, a war budget cut 87.6% followed by a boom, and a war hero's warning. In sixty-five-years the studio is back, and the tower is still standing beside her, gray with dust and strung with cobwebs, with the Politician a grinning skeleton at his button: the proof was there the whole time and nobody moved.

**Running gag: the dead keep waiting** (from Part 12). In recovery-trial the patients on the calm room's bench turn into grinning skeletons, still sitting politely, before the official's slow stamp comes down. In empty-podium the audience, the hungry human and the cold human x-ray into skeletons while they get on with the missiles.

**Recurring cast.** The Lobbyist (the masked crook) is flattened by "THE EVIDENCE" on the title card and is back, unflattened, sitting in the empty-podium audience until he gets up to steal the soup and the coat. The Politician presses the WAR button in proof-required and is charred, is clean again in the empty-podium audience, and is a skeleton at the same button in sixty-five-years. The Weapons Maker rides the war stack down in 1945 and back up today in postwar-boom, then claps in the empty-podium audience with the same missile. The Scientist catches fire in recovery-trial. The FDA official from Part 12 runs the calm room next door. The Rich Human sits in the empty-podium audience.

**Callbacks.** From Part 1 (split-the-atom): the Scientist's giant shears, as giant scissors, cut the war stack in postwar-boom (this time they cut something worth cutting). From Part 2: the factory whose chimneys are smiling missiles (`KIT.props.factory`, no sign), the Weapons Maker's smiling baby missile, and the charred-and-blinking gag after the bomb. From Part 12: the FDA official, drawn exactly as Part 12 records him (`KIT.person({ tone: 0, outfit: "suit", color: 1, hair: 2, glasses: true, hat: null, seed: 12 })`, bald, in glasses, a small "FDA" badge on his lapel; without `hat: null` the kit gives his suit a hat), the dead who keep waiting, and the Earth case file as Part 12 draws it, propped up on the lectern's left end: the tab "~~EARTH~~ DIRT: CASE #847", Part 1's "MAY BE ELIGIBLE FOR OPTIMIZATION" and Part 12's "SUBOPTIMAL" on its cover. It stands there in both host shots and is under dust and a cobweb in sixty-five-years. From Part 13: the color-flip funnel (`KIT.props.colorFlipFunnel`) turns the 1% into medicine money. From the theme song: the bomb goes off in the Politician's face and he stands there charred, grinning, blinking.

**Set up here.** The empty podium, its microphone and its "EISENHOWER" name card come back beside Part 2's factory in Part 17 (military-industrial-loop). The Politician's red WAR button (`KIT.props.yesButton({ label: "WAR", color: C.war })`) and the tower of forms can come back wherever a war starts without proof.

**Held frame.** empty-podium, from a beat after "clothed." (the new missile in the stolen coat) to "standing". Nothing moves and nothing sounds.

**Transitions.** The title card comes up from black and goes down to black; proof-required irises in on Wishonia's face. Cuts from the set to the first plate and from plate to plate (recovery-trial, postwar-boom, empty-podium), and from the last plate back to the set on "years.". sixty-five-years irises out on her face to black, so Part 16's title card comes up from black.

**Bans for this part.**
- Eisenhower is a name card on an empty podium, never a drawn face, uniform or hat.
- The bowler is YOU's mark: nobody in this part wears one.

## Changes from v2

- Wishonia's office, the cream paper diagrams and her corner (PiP) are gone. She hosts from her lectern in two host shots (proof-required and the new sixty-five-years reaction cut at the end), and the three pieces of evidence are three plates the camera travels over: the pandemic ward, the money stacks and the town square.
- The evidence clipboard (labeled rows ticked in the corner of every plate) is cut. The spine is now the tower of forms beside the lectern, which comes back under 65 years of cobwebs in sixty-five-years.
- proof-required has no wall screen: the Politician wheels the WAR button onto her set himself, and the bomb goes off in his face there.
- The labels went with the diagrams: no "NORMAL SYSTEM" sign (the calm room is a waiting room where one slow stamp comes down while the trial's counter rolls to 48,000), no "WEAPONS" sign on the factory, no "IGNORED" calendar; the big numbers are the facts.
- The 65 years happen in the last two seconds of empty-podium, and the part ends on the studio 65 years later instead of a spider on the microphone.
- Fewer sounds: one or two per gag.

## Scene 1 · the-evidence-title

- id: the-evidence-title
- act: Title
- transition_in: up from black (the head of a reel)
- key: after "Evidence.": "THE EVIDENCE" just stamped down on the Lobbyist under the heading, his gloved hand poking out from under the plate and letting go of a war bill
- cue: "Why This Could Actually"
- time: 32:39.5 to 32:46.9 (7.4 s)
- voiceover: "Why This Could Actually Work. *Unlike Everything Else Humanity Has Tried* The Evidence."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem at the top (three cream orbits round an orange nucleus, three war-seal papers running round them) and the heading under it. Heading lines, 16:9: "WHY THIS COULD" (style small) / "ACTUALLY WORK" / "Unlike Everything Else Humanity Has Tried" (style italic, cue "Unlike") / "THE EVIDENCE" (style stamp, cue "Evidence."); 9:16: "WHY THIS COULD" (small) / "ACTUALLY" / "WORK" / "Unlike Everything Else" / "Humanity Has Tried" (italic, cue "Unlike") / "THE EVIDENCE" (stamp, cue "Evidence."). The small gag: the stamp plate lands on the Lobbyist.
- props: title-card, money (war), lobbyist
- status: planned

Moves: "This" → the card comes up from black (0.35 s) with "WHY THIS COULD ACTUALLY WORK" already on it, and the camera pushes in slowly for the whole shot; the emblem's papers run round their orbits. "Unlike" → the italic line slides up under the heading, and the Lobbyist (`KIT.cast("lobbyist")`: fedora, domino mask, trench coat, a briefcase leaking cash) tiptoes in from the left edge along the line where the stamp will land. "Humanity" → he reaches the middle and stops. "Tried" → he looks up. "Evidence." → the "THE EVIDENCE" stamp plate slams down on top of him with its shake. after "Evidence." → his gloved hand pokes out from under the plate's bottom edge and lets go of one war bill, which flutters down; his fedora rolls out the other side. The card goes down to black in its last quarter second.

Sound: a whirr under the running papers from "This"; tiptoe squeaks on "Everything" and "Humanity"; a rubber-stamp thunk on "Evidence."; a squeak from under the plate after it.

On screen: "WHY THIS COULD ACTUALLY WORK" / "Unlike Everything Else Humanity Has Tried" / "THE EVIDENCE". Why: the narrator reads the heading, its italic line and the sub-heading, so one card holds all three; the evidence landing on a crook is the part in one gag.

## Scene 2 · proof-required

- id: proof-required
- act: Proof
- transition_in: iris in on her face
- key: on "starting:": the Politician charred black at the smoking WAR button, still grinning and waving, the tower of forms running out of the top of the frame on her other side, Wishonia's arms folded
- cue: "Humans usually want proof"
- time: 32:46.9 to 32:55.0 (8.2 s)
- voiceover: "Humans usually want "proof" before they stop doing something stupid, which is interesting because you never required proof before starting:"
- layer: A, host
- scene: The host's set (`KIT.studio`), the Earth case file lying on the lectern top. In 16:9 the tower of forms grows on the free wall right of the lectern, where her presenting palm points, and the Politician comes in on her left with a console carrying one big red button. Bundles of cream forms tied with string, stacked a little crooked.
- wishonia: big, skeptical-smile + body-presenting; smirk-smile + body-open-palms on "never"; skeptical-closed + body-arms-crossed on "starting:"
- props: studio, lectern, case-file, paper-stack, politician, yes-button, nuke, sticky-note
- status: planned

Moves: "Humans" → the iris opens on her face while she presents the empty wall at her side; the camera pushes in slowly for the whole shot. "proof" (first) → a bundle of forms thumps down on the floor beside her. "stop" → a second bundle lands on it. "something" → a third. "stupid," → the stack shoots up out of the top of the frame, a tower of forms, and the lectern hops. "never" → the Politician (`KIT.cast("politician")`: toothy grin, very wide tie) strolls in on her other side, wheeling a console with one big red button, "WAR" on its cap; nothing stands beside it. "required" → one blank sticky note flutters down and lands on the console: that is all the paperwork. "proof" (second) → he grins at the camera, waves, and slaps the button without looking. "before" (second) → a white flash: a small mushroom cloud stands up out of the console in his face, and the set shakes. "starting:" → the cloud thins away on him charred black, hair straight up, still grinning, still waving, finger still on the button, smoke curling up; the tower of forms has not moved. Wishonia folds her arms and waits.

Sound: thunks as the bundles land on "proof" and "something"; a slide whistle up as the tower shoots up on "stupid,"; a click for the button on the second "proof"; the boom on the second "before"; a sizzle as the cloud clears on "starting:".

On screen: "WAR" on the button's cap. No: no words on the forms or the sticky note; the blank note is the joke. Why: the standard of proof humans ask for, next to the one they never asked of war.

## Scene 3 · recovery-trial

- id: recovery-trial
- act: The evidence
- transition_in: cut
- key: on "medical research": the Scientist running past the calm result board on fire, chalking a tick under bottle 2, the helpers running in circles behind her and germs everywhere
- cue: "The RECOVERY trial tested"
- time: 32:55.0 to 33:23.3 (28.3 s)
- voiceover: "The RECOVERY trial tested six treatments on forty-eight thousand patients for five hundred dollars per patient instead of the usual forty-one thousand dollars per patient. That's an eighty-two times cost reduction. Not in theory. In reality. During a pandemic. While panicking. Your species does its best medical research when terrified and disorganized, which suggests your normal system is somehow worse than panic."
- layer: B, plate pandemic-ward
- scene: One wide interior plate, left to right: a ward door in a cream wall that patients in pale gowns stream out of; the lab bench (`KIT.props.lab`, boiling over a burner) with the Scientist and two helpers in lab coats; the result board in the middle (a blackboard on legs, a ledge of six pill bottles with faces numbered 1 to 6, a chalk counter over them); a filing cabinet and an alarm light on the wall; a wall; then the calm room next door: beige, a wall clock, a potted plant, the FDA official (as in Part 12) at a tidy desk with one form and his rubber stamp, and a bench of patients in the same gowns, hands folded in their laps. Germs (`KIT.props.germ`) bounce round the lab half.
- props: lab, scientist, human, door, pill-bottle, price-tag, sign, stamp, stamp-mark, germ, flames, fda-official, desk, clock, xray
- status: planned

Moves: "RECOVERY" → wide on the lab: the bench bubbling, the board with an empty ledge, two germs pinging off the walls. "six treatments" → push in on the board: six pill bottles hop onto its ledge one after another, 1 to 6, and smile at us. "forty-eight thousand" → the camera swings left: the ward door bursts open and a conga line of patients in pale gowns streams out across the lab. "thousand" → pull back to take in the board: its chalk counter rolls up and stops on "48,000". "five hundred dollars" → close on the line: a little "$500" tag pops onto each patient's wrist as he passes. "forty-one thousand" → the next patient out of the door gets the usual tag, "$41,000", as big as he is. "dollars" (second) → its weight drags his arm to the floor. "patient." → he topples flat under it, feet in the air. "eighty-two" → "82×" stamps into the air over him. "reduction." → the giant tag shrinks with a squeak to a $500 tag, and he springs back up and rejoins the line. "theory." → by the board, a tidy sign on a post pops up: "THEORY". "reality." → a giant rubber stamp drops out of the top of the frame and smashes it to splinters; it lifts off a mark on the floor, "REALITY". "pandemic." → pull back to the whole lab: every germ splits in two, then four, and the patients sneeze down the line. "panicking." → the same wide frame goes to pieces: the alarm light spins, the helpers run in circles screaming with their arms up, the flasks boil over, and the Scientist's bun catches fire on the burner; she runs in circles on fire, still writing on her clipboard. The board stands calm in the middle. "medical research" → push in on the board as she runs past it, chalking a result under one bottle each lap: ticks under 1 and 2, which cheer; crosses under 3 to 6, which slump. "terrified" → a germ lands on a helper's nose and he leaps into the other helper's arms. "disorganized," → the filing cabinet tips over and spews papers, and a helper empties a bucket of water over the Scientist: she stands charred black and steaming, hair straight up, glasses white, still grinning, and chalks the last cross. "normal system" → the camera travels right through the wall into the calm room: the clock ticks, the plant sits, the FDA official reads his one form; the bench of patients waits, hands in laps. "somehow" → he lifts his rubber stamp, very slowly. "worse" → down the bench, the patients x-ray into grinning skeletons one after another, still sitting politely, hands still in their laps. after "panic." → the stamp finally lands on the form: "PENDING".

Sound: a slam as the ward door bursts open on "forty-eight" and a whirr as the counter rolls on "thousand"; a slam as the patient goes flat on the second "patient."; a rubber-stamp thunk on "eighty-two"; a squeak and a boing as he springs back up on "reduction."; a stamp and a splat as REALITY smashes the sign; a yelp and a fire whoosh on "panicking."; marker squeaks on "medical research"; a clank for the cabinet and a sizzle for the bucket on "disorganized,"; a whoosh into the calm room and two clock ticks; an x-ray zap on "worse"; a slow stamp thunk after "panic.".

On screen: "48,000" / "$500" / "$41,000" / "82×" / "THEORY" / "REALITY" / "PENDING" / the numbers 1 to 6 on the bottles. No: no drug names on the bottles; the two ticks and four crosses are the trial's real result. Why: proof that cheap trials already worked once, in the worst conditions, next to the calm system that kills people by making them wait.

## Scene 4 · postwar-boom

- id: postwar-boom
- act: The evidence
- transition_in: cut
- key: on "handle": the Weapons Maker on top of today's stack, his missile hugged in one arm, flicking the 1% slice off the stack with his other hand like a crumb, the "1%" beside it
- cue: "After World War Two,"
- time: 33:23.3 to 33:51.4 (28.0 s)
- voiceover: "After World War Two, humans cut military spending by eighty-seven point six percent in two years and stumbled into the greatest economic boom in history by running out of people to shoot at. You're now spending thirty point six times the pre-World War Two baseline in inflation-adjusted dollars. You're asking for one percent. Even people who really, really, love exploding people should be able to handle one percent."
- layer: B, plate money-stacks
- scene: A plain tan field with a ground line. On the left, a stack of war bills lying flat, to scale in bills: 49 high in 1945, with the Weapons Maker sitting on top cradling his smiling missile and a tear-off calendar standing beside it whose pages are years. At its foot, one bill lying alone by a little stake reading "1939". The open field on the right is where the fallen bills build a suburb (three `KIT.props.house` ranch houses, a dad at a barbecue, a mom with a pram). Later the color-flip funnel rolls up to the stack's foot.
- props: papers-red, papers-plain, papers-teal, weapons-maker, missile, scissors, calendar, sign, house, human, nuke, color-flip-funnel, pump
- status: planned

Moves: "Two," → framed tall on the 1945 stack, 49 war bills high, the Weapons Maker on top cradling his missile; a pinch of victory confetti falls; the calendar beside it reads 1945. "cut" → the giant scissors swing in from the left and snip the stack 6 bills up. "eighty-seven point six" → the top 43 bills topple like a felled tree with the Weapons Maker riding them down, screaming, and "−87.6%" lands in the sky. "percent" (first) → they crash across the empty ground; the camera pulls back with the fall. "two years" → the calendar tears off two pages: 1946, 1947. "stumbled" → the Weapons Maker staggers out of the heap, stars circling his hard hat. "greatest economic" → the fallen bills' missile seals pop off, the plain bills scamper away across the field, and three ranch houses pop up out of the ground where they stop. "boom" → a swaddled baby pops up out of each chimney like toast. "running out" → close on the Weapons Maker: he aims his missile at the nearest human, a dad at a barbecue, who hands him a hot dog. "people" (first) → he swings it to a mom pushing a pram; she waves. "shoot at." → the missile looks left, looks right, finds nobody, and droops in his arms; he eats the hot dog. "now" → the calendar blurs through the years to a last page, "NOW"; he drops the hot dog and climbs back onto the stump. "thirty point six" → the camera tilts up with him as the stump regrows bill by bill under him, up to 30 bills and a 0.6 bill sliced clean on top: "30.6×". "baseline" → back down at the foot, the lone 1939 bill looks all the way up at it and gulps. "inflation-adjusted" → an accountant (fedora, glasses, a suit) pumps the 1939 bill up with a bicycle pump; it puffs up like a pillow. "dollars." → it pops in his face: he stands charred black, hair straight up, blinking, and the bill lies flat again, exactly the same size. "one percent" (first) → up top, a slice a third of a bill thick right under the Weapons Maker's seat slides half out like a drawer and back, and "1%" lands beside it; down below, the color-flip funnel rolls up to the stack's foot. "really," (first) → he hugs his missile. "really," (second) → he kisses it. "love" → three little hearts float up over them. "exploding" → each heart goes off as a tiny mushroom cloud, pop, pop, pop, and he sighs happily. "handle" → without letting go of the missile, he reaches under his seat with his free hand, pulls the 1% slice out and flicks it off the stack like a crumb; he settles by its thickness and goes back to hugging. "one percent." (second) → the camera follows the slice down: it sails into the funnel and walks out of the spout as medicine money, a cross on its seal.

Sound: a snip on "cut"; a slide whistle down and a yelp as the stack topples on "eighty-seven", and a slam as it lands on "percent"; two calendar ticks on "two years"; a boing as he staggers; three pops for the houses and three toaster pops for the babies on "boom"; a sad slide whistle down as the missile droops on "at."; a whoosh for the years; a slide whistle up as the stack regrows and a thunk for "30.6×"; a squeak for the gulp; two pump huffs, a pop and a sizzle; a ding for the 1%; a sparkle for the hearts and three pops for the tiny clouds; a click for the flick and a whoosh as the slice sails off on "handle"; a cash-register ding as the medicine money walks out.

On screen: the calendar's "1945" / "1946" / "1947" / "NOW"; the "1939" stake; "−87.6%" / "30.6×" / "1%". No: the stacks stay to scale (today's 30.6 bills is shorter than 1945's 49), so the picture never says today's spending beats the wartime peak; no number on the accountant's bill. Why: cutting far more than 1% has been done before and it went well; today's stack is 30.6 times the old baseline; the man who loves bombs most can spare the 1% with one hand and never let go of his missile.

## Scene 5 · empty-podium

- id: empty-podium
- act: The evidence
- transition_in: cut
- key: during the HOLD after "clothed.": the new missile in the stolen coat popping out of the factory door, snug, next to the shivering human in polka-dot underwear and the thin human holding an empty spoon, the Lobbyist tiptoeing off
- cue: "Even your own war heroes"
- time: 33:51.4 to 34:19.1 (27.8 s)
- voiceover: "Even your own war heroes figured this out. Eisenhower, the human who won World War Two, warned you that the weapons industry was eating your civilization alive: "Every gun that is made, every warship launched, every rocket fired signifies, in the final sense, a theft from those who hunger and are not fed, those who are cold and are not clothed." You gave him a standing ovation and then immediately ignored him for sixty-five"
- layer: B, plate town-square
- scene: A 1950s town square on a plain tan field, left to right: a little bandstand with an old podium, a microphone on a stalk, nobody behind it, a spotlight on a pole and a tear-off calendar on the bandstand rail; two rows of folding chairs facing the podium with the audience in profile (the Politician, the Rich Human, the Weapons Maker with his missile, the Lobbyist and everyday humans); behind them the factory (`KIT.props.factory`, no sign) with a hopper on its side and a conveyor out of its side door ending in a bucket of water, and beside it a house and the hospital (`KIT.props.hospital`); at the hopper, a thin hungry human holding a bowl of soup and a human in a winter coat and a hat.
- props: podium, microphone, spotlight, sign, rosette, factory, conveyor, house, hospital, lobbyist, politician, rich-human, weapons-maker, missile, human, calendar, xray
- status: planned

Moves: "war heroes" → framed on the bandstand: the spotlight clicks on the old podium and its microphone. Nobody is behind it. "Eisenhower," → a name card slides onto the podium's front: "EISENHOWER". "won" → a victory rosette pins onto the podium: "1945". "weapons industry" → the spotlight swings off the podium, over the audience, onto the factory behind them, missile chimneys puffing; the camera travels with it. "eating" → the factory's rolling door opens like a mouth full of teeth and chomps the house next to it. "civilization" → it chomps the hospital. "alive:" → a little family waves out from between its teeth as the door rolls shut, and the factory burps a smoke ring. "gun" → a cartoon gun with a price tag rolls out of the side door onto the conveyor. "warship" → a little warship slides down the conveyor. "launched," → it splashes into the bucket at the end. "rocket" → a missile chimney on the roof lights up. "fired" → it launches off the roof and out of the frame. "theft" → close on the hopper: the Lobbyist slips out of his chair and tiptoes over. "hunger" → he lifts the soup bowl out of the thin human's hands. "fed," → he tips the soup into the hopper; the thin human is left holding an empty spoon. "cold" → he pulls the winter coat off the other human, who is left shivering in polka-dot underwear and his hat, an icicle on his nose. "clothed." → he stuffs the coat into the hopper. after "clothed." → a new missile pops out of the factory door wearing the coat, buttoned up, snug, and the Lobbyist tiptoes off. HOLD: nothing moves until "standing". "standing" → the camera pulls back over the whole square: the audience leaps to its feet facing the empty podium. "ovation" → they clap wildly: the Rich Human's monocle pops out, the Weapons Maker claps with the missile tucked under his arm, and the missile claps its little arms too. "immediately" → they all sit down at once, thump. "ignored" → they turn their backs on the podium and get back to work on the missiles: the Politician signs a contract on the Weapons Maker's back, the Rich Human feeds bills into the hopper. "him" (second) → cobwebs race over the podium, its microphone droops, and the calendar on the rail tears through its pages in a blur. "for" → the audience x-rays into grinning skeletons one by one, still at work, and the thin human and the shivering human go too, spoon and hat in hand; they are bones by "sixty-five", and the film cuts to the studio on "years.".

Sound: a switch click for the spotlight on "war"; a whoosh as the name card slides; a pop for the rosette; a slam for each chomp on "eating" and "civilization" and a huff for the burp; a clank for the gun; a splat as the warship lands in the bucket; a slide whistle up as the rocket fires; tiptoe squeaks on "theft"; a clank as the bowl hits the hopper on "fed,"; a whoosh for the coat; a pop for the coated missile after "clothed."; then silence for the HOLD; a whoosh as the audience stands and clapping on "ovation"; a thunk as they sit; hammering on "ignored"; an x-ray zap on "for".

On screen: "EISENHOWER" / "1945" on the rosette / the gun's price tag. No: no quote card; the captions carry the quote, and the picture acts it out. Why: humanity's own war hero made the argument; the picture shows the theft he described, and the applause changed nothing.

## Scene 6 · sixty-five-years

- id: sixty-five-years
- act: The evidence
- transition_in: cut
- key: after "years.": the studio 65 years on, the tower of forms gray with dust and cobwebs, the Politician a grinning cobwebbed skeleton with his finger still on the WAR button, Wishonia side-eyeing the camera with her arms folded
- cue: "years."
- time: 34:19.1 to 34:20.6 (1.5 s)
- voiceover: "years."
- layer: A, host
- scene: The host's set from proof-required, 65 years later: the same tower of forms on the free wall beside her and the same WAR console on her other side, all gray with dust and strung with cobwebs, the case file on the lectern under dust too, cobwebs from the tower to the lectern's corner, and the Politician a skeleton at the button, still grinning, finger on it, cobweb under his arm.
- wishonia: big, sideeye-closed + body-arms-crossed
- props: studio, lectern, case-file, paper-stack, yes-button, politician (skeleton), cobweb
- status: planned

Moves: "years." → cut in on the dusty set with her arms already folded, and she side-eyes the camera, slowly. after "years." → the film irises out on her face to black.

Sound: none; the dusty studio is silent.

On screen: "WAR" on the button's cap. No: no calendar, no number; the dust does the counting. Why: the proof was in the studio the whole time, and so was the button; 65 years later only the skeleton has changed.
