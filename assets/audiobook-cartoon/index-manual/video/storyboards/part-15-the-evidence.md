---
format: 1920x1080
duration: 1:41.2
message: "It has worked before: one trial ran 82 times cheaper during a pandemic, and after World War Two humans cut military spending 87.6% and got the biggest boom in history."
arc: Title card (the evidence lands on a crook) → proof was never required to start → the RECOVERY trial in a burning lab beats the calm system → the war stack cut, the baby boom, today's 30.6 stack loses 1% like a tablecloth → the empty podium, the theft acted out, the ovation, 65 years of cobwebs
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 15, "Why This Could Actually Work: The Evidence"
audio: index-manual.cbaf659d.mp3, 32:39.5 to 34:20.6
version: v2
---

# Part 15 storyboard: "Why This Could Actually Work: The Evidence"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("loved-ones: make the form smaller"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. Layer A is Wishonia's sunburst office; Layer B is the Earth paper; the money is green, and its seal says what it buys (`KIT.money("war")`: a red missile seal; `KIT.money("med")`: a teal cross seal; `KIT.money("plain")`: no seal). "PiP" means Wishonia in her Layer B corner: standing in the bottom right corner in 16:9 (cut off by the frame's bottom edge), in her flying saucer at the top right in 9:16, with her gesture body showing.

**Spine.** The evidence clipboard (`KIT.props.clipboard`). In proof-required it stands on Wishonia's desk, page 1, "PROOF REQUIRED", with two rows, "TO STOP" (a tower of forms lands beside it) and "TO START" (nothing does). When recovery-trial's zoom lands, page 1 flips over the clip and page 2 reads "THE EVIDENCE" (the title card's stamp) with three empty rows; the clipboard hangs in the top corner of every Layer B scene from then on, outside the camera, so it never slides or zooms. Each piece of evidence pops it forward to the middle of the frame, writes its row and ticks it in teal: "82× CHEAPER" after "reality." in recovery-trial, "CUT 87.6%: BOOM" after "at." in postwar-boom, "WAR HERO SAID SO" after "out." in empty-podium. The rows stay that short so they read on a clipboard. The twist on the third: on "sixty-five years" the humans ignore the finished proof too, and a cobweb grows across the clipboard.

**Running gag: the dead keep waiting** (from Part 12). In recovery-trial the calm "normal system" room has a bench of waiting patients who turn into grinning skeletons, tickets still in hand, before the official's stamp comes down. In empty-podium the hungry and the cold humans wait 65 years and end the same way.

**Recurring cast.** The Lobbyist (the masked crook) gets flattened by "THE EVIDENCE" on the title card and is back, unflattened, stealing the soup and the coat in empty-podium. The Politician presses the WAR button on the wall screen in proof-required, charred, and is clean again in the empty-podium audience. The Weapons Maker rides the war stack down in 1945 and back up today in postwar-boom, then sits in the empty-podium audience with the same missile. The Scientist catches fire in recovery-trial.

**Callbacks.** From Part 1: the giant scissors from split-the-atom cut the war stack in postwar-boom (this time they cut something worth cutting), and the stacks are drawn like 604-papers' stack (green bills, red seals). From Part 12: the FDA official (suit, bowler, glasses, an "FDA" badge) is the calm official in recovery-trial's normal-system room, and the dead keep waiting. From Part 13: the 1% goes through the color-flip funnel (its home) in postwar-boom. From Part 14: the Optimitron can stay on Wishonia's desk in proof-required, its two cards still up.

**Callback set up here.** The podium's "EISENHOWER" name card is the card Part 17 pins up ("EISENHOWER WARNED YOU"), and the WEAPONS factory with missile chimneys is the one Part 17's loop feeds.

**Transitions.** Part 14 ends in the office (optimitron-appliance) and the parts are rendered on their own, so the title card cuts in. Title to office cuts. proof-required's wall screen ends on recovery-trial's first frame, so the zoom into the wall screen starts on the picture it lands on. Earth to Earth slides left. Part 16's title follows empty-podium, so empty-podium ends on a settled frame.

**Held frame.** empty-podium, from a beat after "clothed." (the missile in the stolen coat) to "standing". A HOLD is silent.

**Bans for this part.**
- No real people or logos. Eisenhower appears as text only: a name card on an empty podium, never a drawn face, uniform or hat.
- No slideshow (a new text card every scene) and no screensaver (motion that says nothing). Every Layer B scene has an actor that moves on the words.
- Captions keep-out: nothing important in the bottom 17% of the frame (16:9: below y 900; 9:16: y 1470 to 1700).
- No drug names, no real trial logo: the RECOVERY trial is a plain board with six numbered bottles.
- No quote card: the captions carry the Eisenhower quote; the picture acts it out.
- No countdown board in this part.

## Changes from v1

- The humans are the stereotype cast: the Lobbyist under the title card's stamp, the Politician at the WAR button, the Scientist on fire, the Weapons Maker on the war stack, the whole cast in the empty-podium audience. Everyday humans (the lab helpers, the patients, the suburb, the accountant, the hungry and the cold) get their bodies from their outfits.
- The money is green with seals: the war stack is war money, the bills that fall off in 1945 lose their seals and become plain money that builds the suburb, and the 1% comes out of the funnel as medicine money.
- Every gag pays off on screen: the WAR button's mushroom cloud chars the Politician, the Scientist burns and is doused, the waiting patients become skeletons, the 1939 bill pops in the accountant's face, the Weapons Maker's love hearts go off like little nukes, the factory eats a town, the audience ages into skeletons at the missile bench.
- The clipboard is now the spine across all four evidence scenes and gets cobwebs at the end.
- The postwar stacks are drawn to scale in bills: 1939 is one bill, 1945 is 49, 1947 is 6, today is 30.6 (the parameters behind 87.6% and 30.6×), so today's peacetime stack is honestly shorter than the wartime peak and still 30.6 times the baseline.
- empty-podium no longer types the quote on a card.
- Every scene has a Sound line, placed in `parts/part-15.json`.

## Scene 1 · the-evidence-title

- id: the-evidence-title
- act: Title
- transition_in: cut (the parts are rendered on their own and joined)
- key: on "Evidence.": "THE EVIDENCE" just stamped down on the crook, his gloved hand poking out from under it
- cue: "Why This Could Actually"
- time: 32:39.5 to 32:46.9 (7.4 s)
- voiceover: "Why This Could Actually Work. *Unlike Everything Else Humanity Has Tried* The Evidence."
- layer: A, title card
- scene: The sunburst title card (`KIT.titleScene`): the heading in five slams, the italic line under it, then "THE EVIDENCE" as a red rubber-stamp plate, which lands on a crook sneaking along the horizon.
- wishonia: none (title card)
- props: title-card, lobbyist, stamp
- status: outline

Moves: "This" → "WHY" (the scene's first frame; the word itself falls in Part 14's audio) and "THIS" slam in. "Could" → "COULD". "Actually" → "ACTUALLY". "Work." → "WORK". "Unlike" → the italic line "Unlike Everything Else Humanity Has Tried" slides up under the heading, and the Lobbyist (fedora, domino mask, trench coat, briefcase leaking cash) tiptoes in along the horizon from the left. "Humanity" → he reaches the middle, right where the stamp line will land, and stops. "Tried" → he looks up. "Evidence." → the "THE EVIDENCE" stamp plate slams down on top of him with a shake. after "Evidence." → his gloved hand pokes out from under the plate's bottom edge and drops one war-money bill, which flutters down.

Sound: a thunk on each heading word; a whoosh as the italic line slides up; tiny tiptoe squeaks; a rubber-stamp thunk and a splat on "Evidence."; a squeak from under the plate.

On screen: "WHY THIS COULD ACTUALLY WORK" / "Unlike Everything Else Humanity Has Tried" / "THE EVIDENCE". Why: the narrator reads the heading, its italic line and the sub-heading, so one card holds all three; the evidence landing on a crook is the part in one gag.

## Scene 2 · proof-required

- id: proof-required
- act: Proof
- transition_in: cut
- key: after "starting:": the tower of forms on the desk, nothing on row 2, the mushroom cloud filling the wall screen, Wishonia's arms folded
- cue: "Humans usually want proof"
- time: 32:46.9 to 32:55.0 (8.2 s)
- voiceover: "Humans usually want "proof" before they stop doing something stupid, which is interesting because you never required proof before starting:"
- layer: A
- scene: The office. The evidence clipboard stands on the desk, page 1: "PROOF REQUIRED", two rows. To stop something stupid, a tower of forms lands on the desk; to start, nothing at all, while the Politician on the wall screen presses a big red WAR button without looking.
- wishonia: skeptical-smile + body-presenting, then skeptical-closed + body-arms-crossed on "starting:"
- props: office, desk, mug, wall-screen, clipboard, paper-stack, politician, yes-button, nuke
- status: outline

Moves: "Humans" → Wishonia presents the clipboard, propped on the desk at her side: "PROOF REQUIRED". "proof" (first) → row 1 writes itself: "TO STOP". "stop" → a stack of forms thumps onto the desk beside it. "something" → a second stack lands on it. "stupid," → a third lands, the tower runs out of the top of the frame, the desk sags and the mug hops. "never" → row 2 writes itself: "TO START". "required" → beside row 2, where its tower would go, one blank sticky note flutters down. "proof" (second) → on the wall screen, the Politician (lantern jaw, toothy grin, wide tie) strolls up to a console with a big red button: "WAR" on the cap, "START" on the plate. "before" (second) → he slaps it without looking, grinning and waving at the camera. "starting:" → a white flash on the wall screen and a mushroom cloud fills it; the office shakes, the form tower wobbles, Wishonia folds her arms and waits. Then the cloud clears on the Politician charred black, hair straight up, still grinning, still waving, finger still on the button, smoking. Just before the scene ends, the wall screen clicks over to the RECOVERY lab (recovery-trial's first frame).

Sound: a marker squeak as each row writes; three thunks for the stacks, the last one a slam; a soft falling whistle for the sticky note; a click for the button; a boom on "starting:"; a sizzle as the cloud clears; a click as the screen changes channel.

On screen: "PROOF REQUIRED" / "TO STOP" / "TO START" / the button "WAR" · "START". No: no words on the sticky note; its blankness is the joke. Why: sets the standard of proof humans ask for, and shows they never asked it of war.

## Scene 3 · recovery-trial

- id: recovery-trial
- act: The evidence
- transition_in: zoom into the wall screen
- key: on "panicking.": the lab in chaos, the Scientist running in circles on fire, the result board clean in the middle
- cue: "The RECOVERY trial tested"
- time: 32:55.0 to 33:23.3 (28.3 s)
- voiceover: "The RECOVERY trial tested six treatments on forty-eight thousand patients for five hundred dollars per patient instead of the usual forty-one thousand dollars per patient. That's an eighty-two times cost reduction. Not in theory. In reality. During a pandemic. While panicking. Your species does its best medical research when terrified and disorganized, which suggests your normal system is somehow worse than panic."
- layer: B
- scene: A pandemic lab: the lab bench of bubbling glassware with the Scientist and two helpers in lab coats, a calm result board in the middle ("RECOVERY TRIAL", six numbered pill bottles, a patient counter), and a WARD door on the right that patients in gowns stream out of. Germs ping around the room. At the end the camera pans right through the wall into the calm room next door: "NORMAL SYSTEM".
- wishonia: PiP, thinking-small, then surprised-oh + body-open-palms on "eighty-two", then smirk-smile + body-hands-hips on "panic."
- props: lab, scientist, human, result-board, pill-bottle, door, price-tag, sign, stamp, stamp-mark, germ, flames, clipboard, desk
- status: outline

Moves: "RECOVERY" → the zoom lands on the lab; page 1 of the clipboard flips over the clip and page 2, "THE EVIDENCE", hangs in the top corner; a few germs ping off the walls. "six treatments" → six plain pill bottles with faces, numbered 1 to 6, hop onto the board's rows one after another. "forty-eight thousand" → the WARD door bursts open and a conga line of patients in pale gowns streams out across the lab; "thousand" → the board's counter rolls up and stops at "48,000". "five hundred dollars" → each patient in the line gets a little price tag on the wrist: "$500". "forty-one thousand" → the next patient out of the door gets the usual tag, "$41,000", as big as he is; "dollars" (second) → its weight drags his arm to the floor; "patient." → he topples flat under it. "eighty-two" → a rubber stamp slams "82× CHEAPER" across the giant tag. "reduction." → the giant tag shrinks to a $500 tag with a squeak, and he springs back up and rejoins the line. "theory." → a tidy sign on a post pops up by the board: "THEORY". "reality." → a rubber stamp "REALITY" slams down on the sign and smashes it to splinters. after "reality." → the clipboard pops forward and ticks row 1: "82× CHEAPER". "pandemic." → every germ splits into two, then four; the window fogs; the patients sneeze. "panicking." → full chaos: an alarm light spins, the helpers run in circles screaming, a coffee cup flies and splashes the papers, the flasks boil over, and the Scientist's bun catches fire on the burner; she runs in circles on fire, still writing on her clipboard. The result board stays calm and clean in the middle. "medical research" → each time she runs past the board she chalks a result: rows 1 and 2 get ticks and their bottles cheer; rows 3 to 6 get crosses and their bottles slump. "terrified" → a germ lands on a helper's nose and he leaps into the other helper's arms. "disorganized," → the filing cabinet tips over and spews papers; a helper empties a bucket of water over the Scientist: she stands charred black and steaming, hair straight up, glasses white, still grinning, and chalks the last cross. "normal system" → the camera pans right through the wall into the calm room next door, "NORMAL SYSTEM": beige walls, a ticking wall clock, a potted plant, the FDA official (suit, bowler, glasses, "FDA" badge) at a perfectly tidy desk with one form, and a bench of patients in the same gowns holding numbered tickets. "somehow" → the official lifts his rubber stamp, very slowly. "worse" → down the bench, the waiting patients x-ray into grinning skeletons one after another, tickets still in hand, still sitting politely. after "panic." → the stamp finally lands on the form: "PENDING".

Sound: a thunk as the board lands; six pops for the bottles; a slam for the ward door and a whirr as the counter rolls; pops for the small tags; a whoosh as the giant tag drops and a slam as the patient goes flat; a rubber-stamp thunk on "eighty-two"; a squeak and a boing as the tag shrinks and he springs up; a pop for the THEORY sign; a stamp and a pencil scratch for REALITY and the tick; boings for the germs; yelps, a fire whoosh and a splat in the panic; marker squeaks for the results; a yelp on "terrified"; a clank for the cabinet and a sizzle for the bucket; a whoosh for the pan, a ticking clock; an x-ray zap on "worse"; a slow rubber-stamp thunk for PENDING.

On screen: "RECOVERY TRIAL" / "PATIENTS 48,000" / "$500" / "$41,000" / "82× CHEAPER" / "THEORY" / "REALITY" / "NORMAL SYSTEM" / "PENDING" / clipboard "82× CHEAPER" ticked. No: no drug names on the bottles (numbers only); the two ticks and four crosses are the trial's real result. Why: proof that cheap trials already worked once, in the worst conditions, next to the calm system that kills people by waiting.

## Scene 4 · postwar-boom

- id: postwar-boom
- act: The evidence
- transition_in: slide left
- key: on "handle": the 1% slice whipped out from under the Weapons Maker like a tablecloth, him still sitting on the stack, unbothered
- cue: "After World War Two,"
- time: 33:23.3 to 33:51.4 (28.0 s)
- voiceover: "After World War Two, humans cut military spending by eighty-seven point six percent in two years and stumbled into the greatest economic boom in history by running out of people to shoot at. You're now spending thirty point six times the pre-World War Two baseline in inflation-adjusted dollars. You're asking for one percent. Even people who really, really, love exploding people should be able to handle one percent."
- layer: B
- scene: Stacks of war money on a ground line, to scale in bills (one bill lying flat per unit): 1939 is a single bill, the 1945 stack is 49 bills tall with the Weapons Maker sitting on top hugging his missile. The scissors cut it to 6 bills; the 43 that fall become plain money and build a 1950s suburb; then the stump regrows to today's 30.6 bills and loses its top 1% into the color-flip funnel.
- wishonia: PiP, thinking-small, then happy-smile + body-open-palms on "boom", then thinking-closed + body-counting on "asking", then sideeye-closed + body-hands-hips on "exploding"
- props: papers-red, papers-plain, papers-teal, weapons-maker, scissors, calendar, house, human, color-flip-funnel, nuke, clipboard
- status: outline

Moves: "Two," → the 1945 stack, 49 war bills tall, with the Weapons Maker on top cradling his grinning missile; a pinch of victory confetti falls; at its foot, one bill lying alone: "1939"; the tear-off calendar in the corner reads 1945. "cut" → the giant scissors from split-the-atom swing in from the left and snip the stack 6 bills up. "eighty-seven point six" → the top 43 bills topple over like a felled tree, the Weapons Maker riding them down, screaming: "−87.6%". "percent" (first) → they crash across the empty ground. "two years" → the calendar tears off two pages: 1946, 1947. "stumbled" → the Weapons Maker staggers out of the heap, stars circling his hard hat. "greatest economic" → the fallen bills' red seals pop off, the plain bills scamper away, and three ranch houses pop up out of the ground where they ran, TV antennas and all. "boom" → a swaddled baby pops up out of each chimney like toast. "running out" → the Weapons Maker aims his missile at the nearest human, a dad at a barbecue, who hands him a hot dog. "people" (first) → he swings to a mom pushing a pram; she waves. "shoot at." → the missile looks left, looks right, finds nobody, and droops in his arms; he eats the hot dog. after "at." → the clipboard pops forward and ticks row 2: "CUT 87.6%: BOOM". "now" → the calendar blurs through the years to a last page: "NOW"; the Weapons Maker drops the hot dog and climbs back onto the stump. "thirty point six" → the stump regrows bill by bill under him, up to 30 bills and a 0.6 bill sliced clean on top, with him riding it up, grinning: "30.6×". "baseline" → back at the foot, the lone 1939 bill looks all the way up at it and gulps. "inflation-adjusted" → an accountant (bowler, glasses, a suit) pumps the 1939 bill up with a bicycle pump; it puffs up like a pillow. "dollars." → it pops in his face: he stands charred black, hair straight up, blinking, and the bill lies flat again, exactly the same size. "one percent" (first) → at the top of the stack, a slice one hundredth of the stack thick, right under the Weapons Maker's seat, outlines teal: "1%"; the color-flip funnel stands at the stack's foot. "really," (first) → the Weapons Maker hugs his missile. "really," (second) → he kisses it. "love" → three little hearts float up over them. "exploding" → each heart goes off as a tiny mushroom cloud, pop, pop, pop, and he sighs happily. "handle" → zip: the 1% slice is whipped out from under him like a tablecloth; he and the missile drop the slice's thickness and keep hugging, unbothered; only the missile's eyes look down. "one percent." (second) → the slice flutters down into the funnel and walks out of the spout as medicine money, teal cross seal.

Sound: a pop for the confetti; a snip for the scissors; a falling whistle and a yelp as the stack topples and a slam as it crashes; two calendar ticks; a boing as he staggers; three pops as the houses come up; three toaster pops for the babies; a sad falling whistle as the missile droops; a pencil scratch for the tick; a whoosh as the calendar blurs; a rising slide whistle as the stack regrows and a thunk for "30.6×"; a squeak for the gulp; three huffs of the pump, a pop and a sizzle; a ding for the teal slice; a sparkle for the hearts and three pops for the tiny clouds; a whoosh for the tablecloth yank; a cash-register ding as the medicine money walks out.

On screen: "1939" / "1945" / "1947" / "NOW" (calendar) / "−87.6%" / "30.6×" / "1%" / clipboard "CUT 87.6%: BOOM" ticked. No: the stacks stay to scale (today's 30.6 bills is shorter than 1945's 49), so the picture never says today's spending beats the wartime peak; no number on the accountant's bill. Why: cutting far more than 1% has been done before and it went well; today's stack is 30.6 times the old baseline; the 1% comes out from under the man who loves bombs most and he does not even notice.

## Scene 5 · empty-podium

- id: empty-podium
- act: The evidence
- transition_in: slide left
- key: after "years.": the cobwebbed empty podium, the audience grinning skeletons still at the missile bench, the calendar on 65, a spider tapping the microphone
- cue: "Even your own war heroes"
- time: 33:51.4 to 34:20.6 (29.3 s)
- voiceover: "Even your own war heroes figured this out. Eisenhower, the human who won World War Two, warned you that the weapons industry was eating your civilization alive: "Every gun that is made, every warship launched, every rocket fired signifies, in the final sense, a theft from those who hunger and are not fed, those who are cold and are not clothed." You gave him a standing ovation and then immediately ignored him for sixty-five years."
- layer: B
- scene: A 1950s hall. On a small stage at the left, an old podium with a microphone and nobody behind it. In the middle, the WEAPONS factory (missile chimneys) with a conveyor out of its door and a hopper on its side, beside a little town. In front, two rows of theater seats: the audience (the Politician, the Rich Human, the Weapons Maker, the Lobbyist and everyday humans). At the side, a thin hungry human with a soup bowl and a human in a winter coat.
- wishonia: PiP, neutral-smile, then sad-closed on "hunger", then eyeroll-closed + body-arms-crossed on "ignored"
- props: podium, sign, factory, conveyor, house, hospital, lobbyist, human, politician, rich-human, weapons-maker, missile, calendar, clipboard
- status: outline

Moves: "war heroes" → a spotlight clicks on: the empty podium, its microphone, nobody behind it. after "out." → the clipboard pops forward and ticks row 3: "WAR HERO SAID SO". "Eisenhower," → a name card slides onto the podium: "EISENHOWER". "won" → a 1945 victory ribbon pins onto the podium. "weapons industry" → the spotlight swings across the audience to the factory behind them, missile chimneys puffing. "eating" → its loading door opens like a mouth full of teeth and chomps the house next to it. "civilization" → it chomps the hospital. "alive:" → a little family waves out from between its teeth as the door rolls shut; the factory burps a smoke ring. "gun" → a gun rolls out of the door onto the conveyor. "warship" → a warship slides down the conveyor; "launched," → it splashes into a bucket at the end. "rocket" → a missile chimney lights up; "fired" → it launches off the roof. "theft" → the Lobbyist tiptoes in. "hunger" → he lifts the soup bowl out of the thin human's hands; "fed," → he tips the soup into the factory's hopper; the thin human is left holding an empty spoon. "cold" → he pulls the winter coat off the other human, who is left shivering in polka-dot underwear and a hat, an icicle on his nose; "clothed." → he stuffs the coat into the hopper. after "clothed." → a new missile pops out of the factory door wearing the coat, snug. HOLD: nothing moves until "standing". "standing" → the whole audience leaps to its feet. "ovation" → they clap wildly: the Rich Human's monocle pops out, the Weapons Maker claps with the missile tucked under his arm, and the missile claps its little arms too. "immediately" → they all sit down at once, thump. "ignored" → they all turn their backs on the podium and get back to work on the missiles: the Politician signs a contract on the Weapons Maker's back, the Rich Human feeds bills into the hopper. "sixty-five years." → the calendar tears through its pages, "IGNORED" 1 to 65; cobwebs grow over the podium and the microphone droops; the audience x-rays into grinning skeletons one by one, still at work; the thin human and the shivering human x-ray into skeletons too, spoon and hat still in hand; a cobweb stretches across the clipboard. after "years." → a spider lowers itself onto the microphone and taps it twice.

Sound: a switch click for the spotlight; a pencil scratch for the tick; a whoosh as the name card slides; a pop for the ribbon; a hum as the spotlight swings; two slams for the chomps, a yelp from the family and a huff for the burp; a clank for the gun; a whoosh and a splat for the warship; a whistle and a rising slide whistle for the rocket; tiptoe squeaks for the crook; whooshes for the bowl and the coat, a clank for the bowl in the hopper; a pop for the coated missile; then silence for the HOLD; a whoosh as the audience stands and clapping; a thunk as they sit; hammering; calendar ticks; an x-ray zap; two clicks as the spider taps the microphone.

On screen: "EISENHOWER" / "1945" (the ribbon) / "WEAPONS" (the factory) / calendar "IGNORED 65" / clipboard "WAR HERO SAID SO" ticked. No: no drawn Eisenhower (no face, uniform or hat; the empty podium is the joke); no quote card; no gag during the HOLD. Why: humanity's own war hero made the argument; the picture shows the theft he described, and the applause changed nothing for 65 years.
