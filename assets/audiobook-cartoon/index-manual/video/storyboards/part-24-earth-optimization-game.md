---
format: 1920x1080
duration: 0:47.6
message: "The switch is a game: a pool of money goes to Earth Optimization Points holders if the Scoreboard's two numbers (how long people live, how much they earn) go up by 2040, depositors get it back pro rata if they don't, points come from getting friends to play, and the players' greed pulls in the people who know how to cure diseases."
arc: Title card (the emblem's nucleus becomes a spinner) → Wishonia presents the game box: its new lid lifts off Part 7's old OBJECTIVE: LOSE lid, and medicine money pushes the old one up → the board: the Scoreboard, 2040, the holders cannonball into the pool, the film rewinds, the pool pours into the fat cat's piggy bank and YOU's retirement piggy keels over → YOU hauls two friends onto START, and the one human who won't play is x-rayed into a skeleton on his crate → beside the lectern, the five steps sprout legs and walk off into the game box on their own, and YOU shrugs, presses YES and gets a gold star → 4 billion dollar-eyed players burst the box, a magnet pulls in lobbyists, scientists and walking buildings, the GREED arrow nukes the WAR corner out of habit, the stampede drags it round to the diseases, and the hospital flattens the last one
audience: busy humans on YouTube who have not read the book
mode: collaborative
part: 24, "The Earth Optimization Game"
audio: index-manual.cbaf659d.mp3, 50:43.5 to 51:31.0
version: v3
---

# Part 24 storyboard: "The Earth Optimization Game"

Times are MP3 times. They come from each scene's cue word in `../../word-timings.json`, so do not edit them by hand; if the audio changes, rebuild the timings and the scenes follow. Each scene runs until the next one starts. Inside a scene, every move starts on the quoted word.

Scenes are named, not numbered. Use the name in feedback ("friends-to-play: make the crate bigger"). The number in each heading is only the order.

Look, characters and rules: `../../cartoon-style-bible.md`. The film look of Part 2 (`../compositions/scenes/part-02/`): Layer A is the host at her lectern (`KIT.studio`), Layer B is an illustrated plate the camera travels over (`KIT.camera`), one framing per phrase, and the period film runs over every shot. Wishonia is on screen only at her lectern; on the board she is the voice. Money is green: the pool and everything paid out of it is medicine money (cross seal); the crate man's bill and the lobbyists' leaking cash are plain.

**Spine.** One plate, game-board: THE EARTH OPTIMIZATION GAME, a made-up 1950s board game the size of a field, drawn from above like Part 2's loop road, with everything on it standing up. Plate units, the humans at scale 1.5 as in Part 2:
- The box: orange walls round a cream board (the board from x -1200 to 1200, y -700 to 700), mustard stars on the walls. The front wall faces the camera as a standing band (y 720 to 830) and carries a mustard starburst roundel, "FOR 2 TO 4,000,000,000 PLAYERS".
- The track: a ring of squares 240 deep round the board's edge in orange, mustard, slate blue and rust. Corner squares: START at the front left (mustard, lettered "START"), WAR at the back left (rust, a smiling missile painted on it), DISEASES at the back right (slate, three smug disease blobs sitting on it from the start, `KIT.props.diseaseBlob` with three seeds and colors), a mustard star at the front right.
- The pool: a 1950s kidney-shaped swimming pool in the middle (about 1070 x 460, centered near x 40), a cream rim, filled to the brim with medicine money instead of water, a diving board at its left end and a chrome ladder at its right.
- Behind the back wall: the Scoreboard (below), 820 wide, its two posts standing on y -770 at x 0, and a big tear-off calendar on a post at x -760, its pages years.
- On the pool's back rim: the three point holders (a woman in a dress, a worker in overalls, a beanpole in a shirt).
- On the front edge, left to right: YOU's retirement piggy at x -460, Grandma's piggy at x 40, the fat cat's piggy at x 380.
- Outside the box, on the plain tan field: the crate man on his upturned crate left of the left wall (about x -1700, his feet on y 420), and the weapons factory (`KIT.props.factory`, no sign, its chimneys smiling missiles) beyond the back left corner (about x -1650, y -760), the Weapons Maker at its door.
- In greed-handles-it only: the GREED arrow's riveted post drops in at x 200, standing on y -480, about 240 tall, between the WAR and DISEASES corners.

Three scenes travel over it: game-pool-rules and friends-to-play with no seam, and greed-handles-it after the host shot your-job.

**Shared drawings** (several author groups draw these, so they must match). The sketch module (`part-24-earth-optimization-game.sketch.mjs`) has a first version of each in the production art: `chip`, `scoreboard`, `calendar`, `board`, `frontWall`, `roundel`, `pool`, `piggy` and `greedArrow`. The game-pool-rules group draws the plate's versions first; greed-handles-it and the host shots copy them:
- **YOU.** The busy human in the bowler from Part 1's title card, as in Parts 10, 12, 17 and 21: `{ tone: 2, outfit: "suit", hat: "bowler" }`, the same options in every scene. From friends-to-play on, two point chips sit stacked on his bowler.
- **The point chip.** An Earth Optimization Point: a mustard game chip with a notched cream rim and a navy star (`KIT.star`) in the middle, about a hand across. The same chip everywhere: the holders hold it up, two land on YOU's bowler, every player in the crowd holds one.
- **The Scoreboard.** The one in Part 23's two-numbers-did-it: a 1950s ballpark scoreboard, a navy board with orange edging and a row of mustard bulbs along its top, on two posts, two flip-number windows side by side (cream cards, navy Fraunces numerals). The left window reads "63.3" with a small "YRS" card, the right "$2,138" with a small "/YR" card (the book's global_hale_current and global_median_after_tax_income_2025). No other lettering on it.
- **The piggy banks.** 1950s piggy banks in the film's colors (no pink), a coin slot on top, stub legs, a snout and a curly tail, each dressed as its owner: the fat cat's is huge, navy with orange edges, in his top hat, monocle and cigar (`KIT.cast("richHuman")`'s tells); Grandma's is small and cream, in her curlers and cat-eye glasses (`KIT.cast("grandma")`'s); YOU's retirement piggy is skinny and tan, in YOU's bowler.
- **The GREED arrow.** Part 21's (greed-arrow): a long mustard arrow (`KIT.C.yellow`) with a navy outline and an orange edge, "GREED" in Oswald capitals on its shaft, pivoting at its middle on a riveted slate post.
- **The YES console.** Part 18's: `KIT.props.yesButton({ label: "YES", sub: "TREATY" })`.

**Callbacks.** From Part 7 (lose-elaborately): humanity's board game, whose lid said "OBJECTIVE: LOSE"; in game-box the new game's lid lifts off that old lid, still on the box. From Part 23: its last scene offers a knife switch, and this part's title card comes up on a switch click; the Scoreboard of two-numbers-did-it comes back with its YRS and /YR cards; the five steps that flattened YOU in juggling-five-steps walk off by themselves in your-job. From Part 21 (greed-arrow): the GREED arrow, which YOU swung at the diseases there; here it swings back to WAR by habit until the players' stampede drags it round. From Part 18: the YES console. From Part 2: the weapons factory, its smiling missile chimneys and the Weapons Maker; the bomb that leaves the humans charred black and blinking. The cast: the fat cat and Grandma (as piggy banks), the Lobbyist, the Scientist, the Weapons Maker, YOU.

**Set up here.** The roundel "FOR 2 TO 4,000,000,000 PLAYERS" on the game box (game-box) pays off when 4 billion players burst the box's front wall in greed-handles-it. Part 26's doubling-starts grows from your-job's two jobs: YOU votes on the YES console and gets two friends to play.

**Held frame.** None: no line in this part is a death toll. The part's last image (the flat blob under the hospital's foot) holds from "before." to the end, about 1.4 s.

**Transitions.** The title card comes up from black on a switch click and goes down to black; game-box irises in on Wishonia's face, quicker than Part 2's (the shot is 1.5 s). Cut to the plate on "Two"; friends-to-play continues it with no seam (it starts on game-pool-rules' final frame). Cut to the set for your-job, and back to the plate for greed-handles-it. The part ends on the plate's held last frame; Part 25's title card comes up from black.

**Bans for this part.**
- Text is the heading, the box's name and roundel, the old lid's "OBJECTIVE: LOSE", START on its square, the Scoreboard's numbers, the calendar's years, YES on the console, GREED on the arrow and the binders' spine numbers. No signs on the corners (the painted missile and the blobs say it), no share tags on the piggies (their sizes and the streams say it), no arrows over the Scoreboard (the rolling digits say it), no sign on the retirement piggy (YOU's bowler says whose it is).
- The Scoreboard shows only the book's two current numbers. When they go up they roll and keep rolling; they never land on a forecast.
- The board game is made up: no real game's box, board, track or tokens.

## Changes from v2

- The office, the wall screen and Wishonia's corner (PiP) are gone. She is on screen in two host shots: game-box, where she presents the game on "A pool of money", and your-job, where YOU stands beside her lectern. Everything else is one plate, the game board, which the camera travels over in three scenes.
- The title card is the period card; its small gag is the emblem's nucleus turning into a spinner. The box lid moved to game-box, where it lifts a crack on "pool" and three medicine bills peek out; its roundel is also on the box's front wall on the plate, so the crowd bursts it.
- The labels went: the Scoreboard's HEALTHY YEARS and MEDIAN YEARLY PAY plates (its numbers carry their units), the up arrows, the 90% and 10% tags, the YOUR RETIREMENT ACCOUNT sign and the spinner's WAR and DISEASES sectors. The GREED arrow now points at real corners of the board: WAR, with a smiling missile painted on it, and DISEASES, with the blobs sitting on it.
- your-job-card is now your-job: the index card on the wall screen became five fat binders in YOU's arms beside the lectern. They sprout stick legs and walk off into the game box on their own (Part 23 already burnt and flattened him over the five steps), he shrugs and presses Part 18's YES console, which springs out of the lectern, and the gold star slaps onto his forehead.
- The board is drawn from above like Part 2's loop road. The film itself rewinds for "If they didn't", the retirement piggy gets nothing and keels over, and the crate man sits on the tan field outside the box instead of on a table.
- In greed-handles-it the players' stampede drags the arrow round to DISEASES, instead of a hand from the top (in Part 21 YOU swung it; here nobody has to), and the hospital's splat lands on "before." so the last frame holds.

## Scene 1 · earth-optimization-game-title

- id: earth-optimization-game-title
- act: Title
- transition_in: up from black on a switch click (the parts are rendered on their own and joined)
- key: after "Game.": the heading under the atom, a little mustard spinner arrow on the orange nucleus pointing at one running paper, which has jumped
- cue: "The Earth Optimization Game"
- time: 50:43.5 to 50:46.1 (2.6 s)
- voiceover: "The Earth Optimization Game."
- layer: A, title card
- scene: `KIT.titleScene`'s period card (look "atomic"): plain navy, the film's emblem at the top and the heading under it. Heading lines, 16:9: `[{ words: ["THE", "EARTH", "OPTIMIZATION"], style: "small" }, ["GAME"]]`; 9:16: `[{ words: ["THE", "EARTH"], style: "small" }, { words: ["OPTIMIZATION"], style: "small" }, ["GAME"]]`. The small gag (`gag`): a mustard spinner arrow, Part 21's GREED arrow in miniature without its lettering, drops onto the nucleus.
- props: title-card, money (war), greed-arrow (small)
- status: planned

Moves: "The" → a switch click, and the card snaps up from black (Part 23's switch has been thrown) with the whole heading on it; the three papers run round their orbits, and the camera pushes in slowly for the whole shot. "Game." → a little mustard arrow drops onto the orange nucleus with a bounce, pivoting at its middle. after "Game." → it spins like a board-game spinner, clicking, slows, and stops pointing at a paper running past, which jumps. The card goes down to black in its last quarter second.

Sound: a switch click on "The"; a whirr under the running papers; ticks as the arrow spins.

On screen: "THE EARTH OPTIMIZATION GAME". Why: the narrator reads the heading, and the emblem turns into a game before anyone says it is one; the arrow comes back as the board's spinner.

## Scene 2 · game-box

- id: game-box
- act: The game
- transition_in: iris in on her face (quick)
- key: after "money.": Wishonia pointing at the game box on its side table: its new lid lifted clean off and hanging tilted above it; under it, still on the box, Part 7's old orange lid, "OBJECTIVE: LOSE", pushed up a crack at the front by three medicine bills peeking out from under it, pale green light spilling out
- cue: "A pool of money"
- time: 50:46.1 to 50:47.6 (1.5 s)
- voiceover: "A pool of money."
- layer: A, host
- scene: The host's set (`KIT.studio`). On the free wall right of the lectern, a 1950s boomerang-shaped side table on tapered legs, and on it the game box seen from a little above: an orange base, a cream lid with a navy and orange double border and mustard stars, "THE EARTH OPTIMIZATION GAME" across it in Fraunces, and a mustard roundel on its top right corner, "FOR 2 TO 4,000,000,000 PLAYERS". Under the new lid, still on the box, is the old lid of humanity's board game from Part 7 (lose-elaborately), drawn as Part 7 draws it: orange, a cream inner border, "OBJECTIVE:" in navy and "LOSE" in war red. The new game came in the old game's box.
- wishonia: big, happy-smile + body-point-right; smirk-smile + body-point-right on "money."
- props: studio, lectern, side table, game box, old lid (OBJECTIVE: LOSE), money (med)
- status: planned

Moves: "A" → the iris opens on her face (in about 0.4 s) and she points at the box. "pool" → the new lid lifts clean off by itself and hangs tilted above the box: under it, still on the box, is the old orange lid, "OBJECTIVE: LOSE". "money." → the old lid's front edge lifts a crack like a treasure chest, pale green light spills out onto the table, and three medicine bills peek out from under it, one after another, bobbing; she smirks at the camera.

Sound: a squeak as the new lid lifts on "pool"; a second squeak as the old lid lifts and a sparkle as the bills peek out on "money.".

On screen: "THE EARTH OPTIMIZATION GAME" and the roundel "FOR 2 TO 4,000,000,000 PLAYERS" on the new lid, "OBJECTIVE: LOSE" on the old one. No: no price on the box. Why: the host sells the product like a 1950s game show: it is humanity's old losing game with a new lid and money inside, and the roundel promises the crowd that bursts the box at the end.

## Scene 3 · game-pool-rules

- id: game-pool-rules
- act: The rules
- transition_in: cut
- key: after "pool.": the pool of money cut into three slices like a pie, a holder waist-deep in each slice in a crown of flying bills, grinning, arms up, a point chip held high; the three smug blobs on their corner behind
- cue: "Two numbers on a Scoreboard"
- time: 50:47.6 to 51:02.2 (14.6 s)
- voiceover: "Two numbers on a Scoreboard: how long people live, how much they earn. By twenty forty, if the numbers went up, Earth Optimization Points holders split the pool. If they didn't, depositors divide it pro rata (still beats your retirement account)."
- layer: B, plate game-board
- scene: The game board (the spine), first seen whole from high above: the box open, the pool of money in the middle, the Scoreboard dark behind the back wall. The camera travels the back of the board (the Scoreboard, the calendar, the holders on the pool's rim), then the front edge (the piggy banks), right to left, toward START.
- props: game-board, scoreboard, calendar, pool, money (med), point-chip, human, piggy-bank (fat cat, Grandma, YOU)
- status: planned

Moves: "Two" → the whole board from high above. "numbers" → the camera pushes up to the dark Scoreboard. "Scoreboard:" → its row of bulbs lights with a click. "how long" → the camera pushes in on the left window: its cards flip through digits and land on 63.3 on "live,". "how much" → it slides to the right window, which flips and lands on $2,138 on "earn.". "twenty" → the camera swings left to the calendar, and its pages tear themselves off in a 1950s movie flurry, 2026, 2027, 2028 and on. "forty," → it stops on 2040. "went up," → the camera pulls back over the Scoreboard and the pool's back rim: both windows roll upward and keep rolling, the digits a blur that never lands; on "up," the three holders on the rim throw their arms up. "Points holders" → the camera tilts down to them: each holds up a point chip, grinning. "split" → a dashed cut line draws itself across the pool and divides it into three slices like a pie. "pool." → each holder cannonballs into a slice. after "pool." → three crowns of bills splash up, and the holders bob up waist-deep in their slices, grinning, chips held high. "If" → the film rewinds: flickering scratches run down the picture, the holders fly backward out of their splashes onto the rim, the slices close up, and the windows roll back down to 63.3 and $2,138. "depositors" → the camera tilts down to the front edge: the fat cat's huge piggy in his top hat, monocle and cigar, and Grandma's small one in her curlers and cat-eye glasses. "pro rata" → the pool tips forward like a bathtub and pours out in two streams as wide as the piggies: a fire hose into the top hat's coin slot, a trickle into the curlers'; both swell up and burp. "retirement" → the camera moves left along the front edge to a skinny tan piggy in YOU's bowler: it gets nothing, and stands there with its slot open, waiting. after "account)." → it keels over, legs up, X eyes, and the bowler rolls off onto START.

Sound: a switch click as the bulbs light; flip ticks for each number; a whoosh of pages on "twenty" and a ding on 2040; a slide whistle up as the numbers roll; a snip for the cut line; a splat for the cannonballs; a record scratch for the rewind; a whoosh for the pour and a pop for the burps; crickets for the retirement piggy; a boing as it keels over.

On screen: "63.3 YRS" / "$2,138 /YR" / the calendar's years, 2026 to "2040". No: no forecast numbers (the windows roll, they never land on new values); no rule text on the board and no share tags (the sizes say the shares). Why: the whole game on one board: two numbers, one date, two outcomes, and neither outcome loses the money; the only loser is the account you already have.

## Scene 4 · friends-to-play

- id: friends-to-play
- act: The rules
- transition_in: same plate (no seam)
- key: after "playing.": outside the box's left wall, the crate man a grinning skeleton on his crate with his arms still crossed, the disease blob grinning beside him; over the wall, the board's players each holding a medicine bill
- cue: "You earn Earth Optimization Points"
- time: 51:02.2 to 51:09.5 (7.3 s)
- voiceover: "You earn Earth Optimization Points by getting friends to play. Nobody loses. The only losing move is not playing."
- layer: B, plate game-board
- scene: YOU plays: he takes his bowler back at START, hauls two friends onto the board and scores; then the camera finds the one human sitting outside the box.
- props: game-board, you, human, point-chip, money (med, plain), piggy-bank, crate, disease-blob, xray
- status: planned

Moves: "You" → the first frame is game-pool-rules' last. YOU steps over the box's left wall onto START, picks his bowler up off the board and puts it on. "getting" → he reaches over the front wall and hauls up two friends by their collars (a woman in a dress and a barrel-shaped worker), legs dangling. "friends" → he plonks them down on START, one, two. "play." → two point chips pop up over his head and land stacked on his bowler. "Nobody" → the camera pulls back to the whole board: a medicine bill hops into every player's hand and every piggy's coin slot. "loses." → the keeled-over retirement piggy gets one too, and sits up. "The only" → the camera swings left over the box's left wall to the tan field outside, where a refrigerator-box businessman sits on an upturned crate, arms crossed, smug. "losing move" → his plain bill climbs out of his breast pocket, salutes him, and hops over the wall into the game. "not" → his chest light blinks red, and behind him a disease blob rises, claws steepled. "playing." → it pounces: an x-ray zap, and he is a grinning skeleton, arms still crossed, still sitting on his crate. after "playing." → the blob grins at the camera.

Sound: a whoosh as he hauls the friends up; two boings as they land; two dings for the chips; a quick run of pops as the bills hop in, then a cash register; a squeak as the bill salutes; two ticks for the chest light; an x-ray zap.

On screen: "START". No: no text for the points; the chips on the bowler and the skeleton say it. Why: how a player scores (friends), why nobody on the board loses, and the one way to lose.

## Scene 5 · your-job

- id: your-job
- act: Your job
- transition_in: cut
- key: after "play.": beside the lectern, YOU, his two chips on his bowler and a gold star stuck on his forehead, two fingers up, one finger on the YES console that has sprung out of the lectern top; at the right end of the wall the game box on its side table, its lid shut on the last binder's kicking stick legs; Wishonia smiling, counting on her fingers
- cue: "Your job was never to understand"
- time: 51:09.5 to 51:16.3 (6.8 s)
- voiceover: "Your job was never to understand the five steps. Your job is to vote and get two friends to play."
- layer: A, host
- scene: The host's set, with YOU as the guest on the free wall right of the lectern (as host-closes' guest in Part 2, about scale 3.3, feet at the frame's bottom), his two point chips on his bowler. He carries a stack of five fat ring binders, spines numbered 1 to 5, up to his chin. At the right end of the free wall, the game box from game-box on its side table, its lid shut (in 9:16 it can stand at the frame's right edge, half out of shot). Part 18's YES console waits inside the lectern.
- wishonia: big, neutral-smile + body-palms-down; smirk-smile + body-open-palms on "never"; sideeye-closed + body-idle on "steps."; happy-smile + body-counting on "vote"
- props: studio, lectern, you, point-chip, binders, side table, game box, yes-button, gold star
- status: planned

Moves: "Your" → cut to the set: YOU staggers beside the lectern under the five binders, knees knocking. "never" → each binder sprouts a pair of stick legs with pointed shoes, pop, pop, pop, pop, pop. "understand" → they hop down out of his arms one after another and march off in a line to the game box, up onto its table and in under its lid. "steps." → the lid drops shut on the last one, its legs still kicking out from under it; YOU stands with his arms still held out, empty, blinking; she side-eyes him. after "steps." → he looks down at his empty arms, then at the camera, and shrugs. "vote" → the YES console springs up out of the lectern top on a coil spring beside her hand, and he leans over and presses it: ding. She counts on her fingers. "two" → he holds up two fingers. after "play." → a gold star sticker flies in and slaps onto his forehead.

Sound: pops as the legs sprout on "never"; a patter of little feet on "understand"; a thunk as the lid drops on "steps."; a boing as the console springs up and a ding as he presses it; a rubber-stamp thunk and a sparkle for the star.

On screen: "1" to "5" on the binders' spines, the box's name and roundel, "YES" / "TREATY" on the console. Why: shrinks the viewer's part to two actions: the five steps leave his arms and go into the game, which does them for him (in Part 23 he tried to handle them himself and was flattened).

## Scene 6 · greed-handles-it

- id: greed-handles-it
- act: Greed does the rest
- transition_in: cut
- key: after "before.": the back right of the board, the GREED arrow pointing at the DISEASES corner with a player still dangling from it, legs running, the dollar-eyed crowd stampeding onto the corner in a cloud of dust, the walking hospital's foot down on the last blob, flat as a pancake and x-eyed
- cue: "Four billion humans whose payout"
- time: 51:16.3 to 51:31.0 (14.7 s)
- voiceover: "Four billion humans whose payout depends on curing diseases will attract the lobbyists, researchers, and institutions who know how to do the rest. The greed handles it. It always has. You just never pointed it at anything useful before."
- layer: B, plate game-board
- scene: The same board, overfull: 4 billion players, a magnet rising out of the pool, the cast pulled in, and Part 21's GREED arrow dropped in on its post at the back of the board, between the WAR and DISEASES corners (its post at x 200, standing on y -480). The crate man's skeleton still sits on his crate outside the left wall.
- props: game-board, human (crowd), point-chip, magnet, lobbyist, scientist, hospital, bank, capitol, greed-arrow, factory, weapons-maker, missile, nuke, disease-blob
- status: planned

Moves: "Four billion" → cut to the whole board from high above: players pour onto it from the top of the frame like rain, a few, then hundreds, then a solid crowd, each holding a point chip. "humans" → the crowd spills over the track, and the box's front wall bursts off with a boing, its roundel spinning away. "payout" → the camera pushes in on the crowd: every face turns toward the back right corner, and every pair of eyes becomes dollar signs. "diseases" → the camera travels to the DISEASES corner: the three blobs sit there, smug, steepling their claws. "attract" → the camera pulls back over the pool: a giant red horseshoe magnet rises out of the money, poles up, bills sliding off it. "lobbyists," → three masked crooks skid in from the left on their heels, leaning back, briefcases leaking money, and clank onto the left pole. "researchers," → three scientists skid in from the right, flasks sloshing, and clank onto the right pole. "institutions" → a hospital, a bank and a legislature on little stick legs stomp in over the back wall, one, two, three. "rest." → the magnet sinks back into the money and lets go; everyone it pulled in turns toward the DISEASES corner, and the blobs stop smirking and gulp. "greed" → the camera travels to the back of the board: the GREED arrow drops in on its post between the WAR and DISEASES corners with a clank. "handles" → it spins by itself, clicking. "always" → it slows and stops pointing left, at the WAR corner. "has." → beyond the back left corner, the factory's middle chimney, a smiling missile, lifts off while the Weapons Maker waves his hard hat at the door. after "has." → it comes down on the WAR corner: a white flash, the frame shakes, a mushroom cloud stands over the corner, and the players on it stand charred black and smoking, hair straight up, only their eyes blinking, still holding up their chips. "pointed" → the camera slides right to the arrow as the whole crowd breaks into a stampede for the DISEASES corner; the front runners grab the arrowhead on their way past and drag it round with them, a few of them dangling from it, legs still running. "anything" → it clanks down pointing right, at the DISEASES corner. "useful" → the camera pushes in toward the DISEASES corner as the stampede pours onto it in a cloud of dust, the walking hospital in front; the blobs scream, and two of them run off the board. "before." → the hospital steps on the last blob: splat, flat as a pancake, x-eyed. Hold on that to the end.

Sound: a whoosh as the players pour in; a boing as the wall bursts; a cash register for the dollar eyes; a magnetic hum; a clank for each group that hits a pole; three thunks for the stomping buildings; a squeak as the blobs gulp; a clank as the arrow drops onto its post; spinner ticks; a slide whistle down as the missile falls and the boom; hammering footsteps from "pointed" and a squeak as the arrow drags round; a ding on DISEASES; more hammering as the stampede pours onto the corner; a splat.

On screen: "GREED" on the arrow, "FOR 2 TO 4,000,000,000 PLAYERS" on the bursting wall. No: no counter of 4,000,000,000 (the crowd and the burst box carry it) and no sector labels (the arrow points at the corners). Why: the players do not need to know how; their payout pulls in the people who do, and the same greed that always picked war gets dragged round to diseases by the crowd itself: nobody has to point it.
