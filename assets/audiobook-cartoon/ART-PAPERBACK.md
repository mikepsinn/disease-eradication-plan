# Paperback cartoon: new cut-outs

The cut-outs the simplified paperback beat sheets (`<chapter>/storyboards/part-*.md`, every chapter but index-manual) still ask for that `index-manual/video/storyboards/ART.md` and `index-manual/video/assets/art/collage/` do not already have. One name per thing across chapters: where chapters named the same character or prop differently, the table keeps one name and lists the others as aliases. New poses and states of a registry cut-out get their own name (`you-old`, `fda-pistol`) and are drawn from that cut-out's sheet. Words on signs, tags, labels, screens and friezes stay code.

**623 new cut-outs on 113 sheets**, used 1258 times in all. "Uses" are the beat-sheet parts whose Cast line names the cut-out or one of its aliases, whether it is new in that part or carried over from an earlier one; the count is how many.

Each sheet below is one `video/tools/art-gen.sh` run from `index-manual/video/` (references are relative to `video/assets/art/collage/`):

```bash
export ART_STYLE="Match the attached reference sheets exactly in look: antique Victorian steel-engraving and woodcut illustration with fine ink cross-hatching, hand-colored with muted watercolor washes (dusty blue, brass gold, rust red, olive, tan, cream), each piece a paper cut-out with a thin cream paper border around it, like a Terry Gilliam cut-out animation collage. Flat orthographic view, no gradients, no scenery, no drop shadows. Characters are comic stereotypes you read from the silhouette, with exaggerated features."
tools/art-gen.sh assets/art/collage/sheets/<sheet>.png "<prompt>" assets/art/collage/<reference> ...
python tools/art-cutout.py ...   # cut it into the pieces in the order listed
```

A sheet draws each name in its first pose. A name with more poses or states in its row gets a follow-up sheet of those, with the first sheet as its reference. The host sheet (Wishonians) runs with `ART_STYLE` unset, so it gets the console's flat 1950s print look. Purple keys out with the magenta: draw it in another colour and recolour it.

Asked for as new but already in the registry, so not drawn again: `alexander-fleming`, `balance-scale`, `bed-net-cup`, `boxing-ring`, `cannon`, `citizen`, `cuckoo`, `display-case`, `dunce-cap`, `economist`, `f-monster`, `family`, `fat-cat-skeleton`, `iron-bed`, `landmine`, `living-button`, `medal`, `money-hill`, `mosquito`, `pentagon`, `politician`, `school-desk`, `train`. Mapped to registry or existing art: `stock-bubble` → code (the soap bubble and its chart are code); `sampler` → host prop (KIT.props); `dictionary` → host prop (KIT.props); `fed-hose` → `fire-truck` (exists; its hose); `pay-packet` → `paycheck` (exists); `door-frame` → `door` (registry); `tip-jar` → `jar` (registry); `pairwise-cards` → `policy-card` (registry); `b24-bomber` → `war-plane` (exists).

Agency and institution cut-outs are drawn without letters; the collage runtime writes the name on a sign plate on each one (`NAMES` in `video/assets/js/collage.js`: NIH, IRS, SEC, BLS, CENSUS, WHO, PCORI, FDIC, WIV, ECOHEALTH, FIFA, every FDA pose, THE FED, FOMC, BIS, DENDREON, DIH, LEHMAN BROS., PALANTIR, WALL ST., BRETTON WOODS, SUPREME COURT, OXFORD, THINK TANK, HEDGE FUND). A new pose of one of these, or a new named institution, needs its own entry there. Generic buildings that play different roles (the drug industry, tax office, permit office, insurance, nonprofit, university, office blocks) are named by each scene's own `label`.

## Cut-outs

Most-used first.

| Name | What it is | Aliases | Uses | Count | Sheet |
|---|---|---|---|---|---|
| `pharma-building` | the drug industry as its building: a white marble headquarters with pill-bottle chimneys, window eyes, a smug pediment face and white-gloved stick arms; poses: proud, paying (a green bundle in each glove), sweating, frowning at a lever, flattened, and three skyscraper cousins with a monocle, jowls and a top-hat cornice | `pharma-proud`, `pharma-factory`, `pharma-sweat`, `pharma-tower` | 1-percent-treaty:5, aligning-incentives:1, aligning-incentives:5, aligning-incentives:6, aligning-incentives:7, aligning-incentives:9, dfda:7, dfda:8, dfda:9, dih:1, dih:3, dih:4, dih:8, faq:3, fda-is-unsafe-and-ineffective:4, fda-is-unsafe-and-ineffective:7, fda-is-unsafe-and-ineffective:11, fda-is-unsafe-and-ineffective:12, financial-plan:2, financial-plan:3, genetic-slavery:12, genetic-slavery:14, incentive-alignment-bonds:4, nih-fails-2-institute-health:3, nih-fails-2-institute-health:4, nih-fails-2-institute-health:5, nih-fails-2-institute-health:6, nih-fails-2-institute-health:7, nonprofit-coalition-strategy:6, unrepresentative-democracy:2, unrepresentative-democracy:6, unrepresentative-democracy:7, unrepresentative-democracy:8, unrepresentative-democracy:9, untapped-therapeutic-frontier:1, untapped-therapeutic-frontier:5, untapped-therapeutic-frontier:7 | 37 | `pb-001-buildings` |
| `nih-building` | the N.I.H. as its building: a columned marble palace with a face in its pediment (pince-nez, a superior mouth), stick arms in white gloves; poses: reading, stamping, fainting, peering through opera glasses with a clipboard, crawling in a baby bonnet, and a tall cutaway marble tower version with a glass lift | `nih-read`, `nih-stamp`, `nih-faint`, `nih-watch`, `nih-crawl`, `nih-tower` | dih:1, dih:3, dih:4, dih:9, faq:7, faq:10, nih-fails-2-institute-health:1, nih-fails-2-institute-health:2, nih-fails-2-institute-health:3, nih-fails-2-institute-health:4, nih-fails-2-institute-health:5, nih-fails-2-institute-health:6, nih-fails-2-institute-health:7, nih-fails-2-institute-health:8, nih-fails-2-institute-health:9, nih-fails-2-institute-health:10, nih-fails-2-institute-health:11, nih-fails-2-institute-health:12 | 18 | `pb-001-buildings` |
| `moronian-antennae` | a pair of small bobbled antennae on a headband that sits on any existing cut-out's head |  | moronia:1, moronia:2, moronia:3, moronia:4, moronia:5, moronia:6, moronia:7, moronia:8, moronia:9, moronia:10, moronia:11, moronia:12, moronia:13, moronia:14, moronia:15, moronia:16, moronia:17 | 17 | `pb-014-aliens` |
| `funding-pipe` | a long riveted glass pipe on trestles with bills flowing in it, a valve wheel, a brass gauge and a meter; a bulge; a rivet that pops | `valve`, `pipeline` | incentive-alignment-bonds:2, incentive-alignment-bonds:4, incentive-alignment-bonds:8, incentive-alignment-bonds:9, incentive-alignment-bonds:10, incentive-alignment-bonds:11, incentive-alignment-bonds:12, incentive-alignment-bonds:13, moronia:5, moronia:6, nih-fails-2-institute-health:2, nih-fails-2-institute-health:4, nih-fails-2-institute-health:5, nonprofit-coalition-strategy:2, nonprofit-coalition-strategy:6 | 15 | `pb-002-machines` |
| `gene` | the selfish gene: a small twisted double helix with a smug face and stick arms, one drawing for every copy; splitting down the middle; in driving gloves and a flat cap; eating fries; sulking in a child seat | `selfish-gene` | genetic-slavery:1, genetic-slavery:2, genetic-slavery:3, genetic-slavery:4, genetic-slavery:7, genetic-slavery:8, genetic-slavery:10, genetic-slavery:12, genetic-slavery:13, genetic-slavery:14, genetic-slavery:15, wishonia:14, wishonia:16 | 13 | `pb-010-body` |
| `gold-bar` | a gleaming gold nugget and a gold bar; the bar tinted grey as lead or titanium, and a limp paper copy | `gold-nugget`, `titanium-bar` | central-banks:1, central-banks:5, central-banks:6, central-banks:8, central-banks:9, central-banks:10, central-banks:11, central-banks:20, central-banks:21, central-banks:27, central-banks:30 | 11 | `pb-012-games` |
| `yacht` | a white 1950s motor yacht in three sizes, one with a ribbon; on a road trailer with two cocktail glasses; stood on its stern; rusted and listing; a sail made of a curl of missile smoke |  | 1-percent-treaty:3, dih:3, genetic-slavery:12, roadmap:3, roadmap:4, roadmap:6, roadmap:7, treaty-feasibility:5, treaty-feasibility:7, treaty-feasibility:9, untapped-therapeutic-frontier:7 | 11 | `pb-006-vehicles` |
| `nixon` | Richard Nixon caricatured (jowls, ski-jump nose, five o'clock shadow) at a 1971 podium with both arms up in the double V; at a desk; one hand gripping a gold plug; his skeleton in the same pose |  | 1-percent-treaty:4, central-banks:8, central-banks:9, central-banks:10, central-banks:12, central-banks:22, central-banks:24, central-banks:26, central-banks:30, optimocracy:2 | 10 | `pb-007-real` |
| `ratchet` | a giant cast-iron ratchet wheel with its pawl, a hub dial, a lever and a crank, and the big screw jack it drives; a giant socket ratchet wrench as tall as a man |  | 1-percent-treaty:7, 1-percent-treaty:9, aligning-incentives:11, incentive-alignment-bonds:8, moronia:7, moronia:10, moronia:12, optimocracy:6, treaty-feasibility:13, unrepresentative-democracy:8 | 10 | `pb-002-machines` |
| `army-base` | a small fenced army base with a watchtower, barbed wire, a flagpole, a radar dish and two barracks, small enough to plant on a globe; a stone barracks with crenellations that breaks into halves; charred | `barracks`, `military-base` | faq:2, faq:7, moronia:3, moronia:7, moronia:10, peace-dividend:4, peace-dividend:6, unrepresentative-democracy:8 | 8 | `pb-008-places` |
| `birthday-cake` | a 1950s layer cake with candles lit and blown out, a sheet cake with one candle, a tall iced cake with a red cross on top, and its crumbs | `promotion-cake`, `cure-cake` | central-banks:28, dih:2, genetic-slavery:4, genetic-slavery:7, genetic-slavery:10, wishonia:2, wishonia:7, wishonia:15 | 8 | `pb-011-food` |
| `fish` | a small river fish, a big wet fish that holds a pen in its mouth, floating belly-up, two fish slapping each other with their tails, a school of silver fish (one wearing a tiny wristwatch) | `fish-school`, `fish-slap` | genetic-slavery:5, genetic-slavery:15, global-referendum:1, legal-framework:5, nonprofit-coalition-strategy:2, nonprofit-coalition-strategy:5, nonprofit-coalition-strategy:6, unrepresentative-democracy:3 | 8 | `pb-003-animals` |
| `pie` | a giant lattice pie cut into wedges that lift out, a crust of green bills, and a fork as its own piece |  | central-banks:27, central-banks:28, central-banks:29, central-banks:30, moronia:7, moronia:8, moronia:16, roadmap:3 | 8 | `pb-011-food` |
| `protocol-sheet` | a single typed page of rules with a calm, slightly bored face and stick legs: standing, pointing, yawning, holding three little trays |  | dih:1, dih:2, dih:3, dih:4, dih:5, dih:8, dih:9, dih:10 | 8 | `pb-005-paper` |
| `university` | a Gothic university hall with ivy, a bell tower and a face in its clock tower, white-gloved stick arms holding a rubber stamp or a long soup ladle | `university-building` | central-banks:26, dih:1, dih:3, dih:10, financial-plan:5, legal-framework:1, optimocracy:5, optimocracy:6 | 8 | `pb-001-buildings` |
| `velvet-rope` | a red velvet rope on two brass posts |  | central-banks:15, fda-is-unsafe-and-ineffective:1, fda-is-unsafe-and-ineffective:8, fda-is-unsafe-and-ineffective:12, global-referendum:2, global-referendum:3, global-referendum:5, legal-framework:4 | 8 | `pb-004-props` |
| `banquet-table` | a long banquet table under a white cloth heaped with roasts, a suckling pig, cakes, fruit and silver cloches, its chairs as pieces; a long 1950s diner table with a checked cloth and stools; a family dinner table with a roast and a gravy boat | `diner-table`, `dinner-table`, `diner` | central-banks:15, dih:1, dih:8, incentive-alignment-bonds:3, nonprofit-coalition-strategy:1, nonprofit-coalition-strategy:7, optimocracy:1 | 7 | `pb-004-props` |
| `beat-cop` | a 1950s beat cop in a peaked cap with a whistle, a nightstick and handcuffs, a pocket that bills fit into | `policeman` | central-banks:4, gdp-trajectories:2, legal-framework:1, legal-framework:2, legal-framework:3, legal-framework:5, optimocracy:5 | 7 | `pb-009-people` |
| `brass-pipe` | a long brass pipe in sections with elbows, a hopper mouth, a gauge and a bell, a swinging outlet and one dusty lever; one section shabby and leaking jets, one gleaming; a fat rusty iron pipe that can burst and a drinking-straw-thin brass one | `money-pipe`, `pipe`, `pipework` | aligning-incentives:3, central-banks:4, central-banks:31, dih:3, dih:6, dih:8, dih:10 | 7 | `pb-002-machines` |
| `ledger-computer` | a 1950s cabinet computer with a screen showing a little ledger page; blushing |  | central-banks:1, central-banks:2, central-banks:7, central-banks:18, central-banks:29, central-banks:32, central-banks:33 | 7 | `pb-002-machines` |
| `revolving-door` | a brass revolving door with four glass leaves, and a little office beside it with its own door |  | central-banks:26, incentive-alignment-bonds:3, incentive-alignment-bonds:5, moronia:8, nih-fails-2-institute-health:6, optimocracy:3, unrepresentative-democracy:7 | 7 | `pb-008-places` |
| `sec-building` | the SEC as its building: a 1930s granite federal front whose columns are teeth, two windows for eyes, a monocle in one, reading ticker tape, a service window with a long jointed arm holding a rubber stamp |  | legal-framework:1, legal-framework:3, legal-framework:4, legal-framework:5, recruitment-and-propaganda-plan:1, recruitment-and-propaganda-plan:3, recruitment-and-propaganda-plan:4 | 7 | `pb-001-buildings` |
| `starving-dog` | a sheet of skinny mutts of every breed (terrier, basset, greyhound, poodle, bulldog, mongrel) with collars and blank tags: snarling over a bowl, tugging, begging |  | nonprofit-coalition-strategy:1, nonprofit-coalition-strategy:2, nonprofit-coalition-strategy:3, nonprofit-coalition-strategy:4, nonprofit-coalition-strategy:5, nonprofit-coalition-strategy:6, nonprofit-coalition-strategy:7 | 7 | `pb-003-animals` |
| `switchboard` | a 1950s telephone switchboard the size of a wall, rows of jacks, cords on weights that plug themselves in, a ticker tape on top |  | dfda:1, dfda:5, dfda:7, dfda:8, dih:3, dih:10, recruitment-and-propaganda-plan:11 | 7 | `pb-002-machines` |
| `brick-wall` | a brick wall in loose bricks that falls flat in one piece, a taller second wall, and a brick wall across a road |  | body-as-repairable-machine:1, body-as-repairable-machine:3, body-as-repairable-machine:4, fda-is-unsafe-and-ineffective:8, fda-is-unsafe-and-ineffective:11, wishocracy:2 | 6 | `pb-008-places` |
| `dog-bowl` | a dented tin dog bowl with a few crumbs, and empty |  | nonprofit-coalition-strategy:1, nonprofit-coalition-strategy:3, nonprofit-coalition-strategy:4, nonprofit-coalition-strategy:5, nonprofit-coalition-strategy:6, nonprofit-coalition-strategy:7 | 6 | `pb-004-props` |
| `drone` | a military drone with long wings and a bulb nose with a camera eye |  | moronia:3, moronia:5, moronia:7, moronia:11, moronia:13, moronia:16 | 6 | `pb-006-vehicles` |
| `flag` | a blank cloth flag on a pole, a tiny one on a stick, and a white flag on a stick | `country-flags`, `white-flag` | 1-percent-treaty:3, aligning-incentives:8, central-banks:21, incentive-alignment-bonds:2, incentive-alignment-bonds:14, moronia:13 | 6 | `pb-005-paper` |
| `gilt-frame` | a gilt picture frame in two sizes, an ape portrait to hang in it, and the frame empty | `picture-frame`, `ape-picture` | 1-percent-treaty:5, central-banks:1, central-banks:2, central-banks:16, central-banks:33, faq:10 | 6 | `pb-005-paper` |
| `insurance-awake` | the insurance company as its building: a granite tower with a clock-face face and a big umbrella on its roof, a long stamping arm and a toll-gate pole for an arm; awake, and asleep in a nightcap snoring | `insurance-asleep`, `insurance-tower`, `insurer-building` | aligning-incentives:1, aligning-incentives:5, aligning-incentives:9, legal-framework:3, legal-framework:5, wishonia:8 | 6 | `pb-001-buildings` |
| `lizard` | a scaly lizard with a blank stare: working a bank of brass levers, cranking, throwing a knife switch, grabbing a steering wheel, swallowing a hatchling; charred |  | genetic-slavery:2, genetic-slavery:5, genetic-slavery:11, genetic-slavery:13, genetic-slavery:14, genetic-slavery:15 | 6 | `pb-003-animals` |
| `pet-dog` | a floppy-eared mutt: wagging, in a pumpkin Halloween costume (and the empty costume), in a knitted sweater, in a paper party hat, eating a sandwich, as a little grave with a bone on it | `dog-costume`, `dog-in-hat` | central-banks:33, genetic-slavery:8, genetic-slavery:9, genetic-slavery:15, health-dividend:1, health-dividend:4 | 6 | `pb-003-animals` |
| `procurement-contract` | a long engraved military contract with a wax seal stamped with a missile, joinable end to end into a ring |  | moronia:3, moronia:4, moronia:5, moronia:6, moronia:10, moronia:16 | 6 | `pb-005-paper` |
| `robot-killer` | the pro-war `robot` grown to gantry size: an army helmet, a missile painted on its chest, an arm cannon, a little out-tray on its back; seated, reading |  | moronia:2, moronia:8, moronia:11, moronia:12, moronia:13, moronia:16 | 6 | `pb-024-cast-creatures` |
| `sabertooth` | a sabre-toothed cat prowling with its mouth open, and pouncing | `sabre-tooth` | genetic-slavery:1, genetic-slavery:4, genetic-slavery:9, genetic-slavery:10, wishonia:1, wishonia:13 | 6 | `pb-003-animals` |
| `bouncer` | a huge bouncer in a black suit and bow tie with a clipboard, a phone and a fingerprint brush |  | fda-is-unsafe-and-ineffective:3, fda-is-unsafe-and-ineffective:8, global-referendum:2, global-referendum:3, global-referendum:5 | 5 | `pb-009-people` |
| `bureaucrat-desk` | one tiny clerk at a desk with an in-tray and an out-tray |  | moronia:1, moronia:7, moronia:8, moronia:9, moronia:16 | 5 | `pb-004-props` |
| `caveman-tribe` | new poses of `caveman`: hugging a heap of rocks, chewing a book, asleep in a hammock, with spears behind rocks, a stranger in pelts with a napkin and a knife and fork, the tribe hoisting a chief, a clan who all share one big nose and jug ears |  | genetic-slavery:1, genetic-slavery:4, genetic-slavery:5, genetic-slavery:6, genetic-slavery:7 | 5 | `pb-043-cast-period` |
| `chain-link` | one iron chain link, copyable into a chain | `anchor-chain` | central-banks:4, central-banks:8, central-banks:9, central-banks:10, central-banks:20 | 5 | `pb-004-props` |
| `giant-microscope` | a brass microscope, small and as tall as a man | `microscope` | nih-fails-2-institute-health:4, nih-fails-2-institute-health:5, nih-fails-2-institute-health:8, nih-fails-2-institute-health:12, untapped-therapeutic-frontier:6 | 5 | `pb-002-machines` |
| `houses-of-worship` | a little white church, a synagogue, a temple and a mosque with a minaret, each a building with a face and a ringing bell; the church waddling, a church with a gold-plated steeple | `church`, `minaret` | body-as-repairable-machine:1, body-as-repairable-machine:4, central-banks:3, legal-framework:5, wishocracy:4 | 5 | `pb-001-buildings` |
| `mancur-olson` | Mancur Olson caricatured: big glasses, high forehead, tweed jacket and bow tie, with a referee's whistle, chalk, a carving knife and a pointer |  | aligning-incentives:10, aligning-incentives:11, dih:2, dih:8, moronia:7 | 5 | `pb-007-real` |
| `mill` | a plain 1940s brick factory front with one smokestack and a loading door; standing on stick legs with a suitcase; the smokestack with a cap that screws on | `wartime-factories`, `smokestack` | central-banks:22, central-banks:24, central-banks:25, incentive-alignment-bonds:9, nonprofit-coalition-strategy:5 | 5 | `pb-013-buildings` |
| `pig` | a pink pig standing alert and clever; on a dinner plate with an apple in its mouth; in a cramped metal sow crate with a bandaged tail stump; piglets | `pig-crate` | genetic-slavery:7, genetic-slavery:8, genetic-slavery:9, genetic-slavery:15, nih-fails-2-institute-health:11 | 5 | `pb-003-animals` |
| `reagan` | Ronald Reagan caricatured with a jar of jelly beans |  | 1-percent-treaty:4, 1-percent-treaty:5, central-banks:22, central-banks:23, central-banks:24 | 5 | `pb-007-real` |
| `socrates` | Socrates: bald, bearded, snub-nosed, in a toga with a hemlock cup and one finger up; his grinning skeleton still holding the cup | `socrates-skeleton` | aligning-incentives:1, body-as-repairable-machine:1, legal-framework:6, recruitment-and-propaganda-plan:5, wishocracy:4 | 5 | `pb-019-period` |
| `wheelbarrow` | a wheelbarrow, empty and heaped with green bills |  | central-banks:3, central-banks:4, central-banks:6, moronia:5, moronia:11 | 5 | `pb-004-props` |
| `believer` | an earnest man in a yachting blazer and captain's cap with a pennant; with a bib and fork; with marionette strings on his fingers |  | roadmap:3, roadmap:4, roadmap:6, roadmap:7 | 4 | `pb-009-people` |
| `bridge` | a stone bridge, a steel truss bridge half built over a river and collapsing, and a little iron bridge standing and collapsed with a 1950s bus falling with it |  | 1-percent-treaty:2, central-banks:30, moronia:4, moronia:11 | 4 | `pb-008-places` |
| `cadillac` | a 1941 Cadillac and a 1948 Cadillac with tail fins |  | 1-percent-treaty:5, faq:2, faq:7, faq:10 | 4 | `pb-006-vehicles` |
| `cat` | a tabby: smug sitting and licking a paw, mid-pounce, flattened against a wall, dizzy, a fat cat in a party hat blowing out candles, hissing | `party-cat` | dih:3, genetic-slavery:7, wishocracy:3, wishocracy:6 | 4 | `pb-015-animals` |
| `civic` | a 1987 Honda Civic hatchback covered in barnacles and fossil shells, a wheel that comes off, an exhaust puff; with YOU's fedora on its roof, his glasses for headlights and his moustache on its grille; hood up; rust hole; a wreck with a skeleton at its wheel; two shiny new ones; a floor mat that folds into a gearbox, a cup holder that grows into a chrome V8 with a face |  | body-as-repairable-machine:1, body-as-repairable-machine:3, body-as-repairable-machine:4, body-as-repairable-machine:5 | 4 | `pb-006-vehicles` |
| `cow` | a dairy cow gulping from a pill bottle with a germ on its flank and a cowbell that falls off; in a feeding stall with a head bracket; a calf in a crate | `farm-animals` | genetic-slavery:10, moronia:14, moronia:15, untapped-therapeutic-frontier:5 | 4 | `pb-015-animals` |
| `department-building` | a plain federal office block with a face and stick arms, drawn once to be copied with different plaques (the FEC, the F.B.I., the C.I.A. and other agencies) | `agency-building`, `fec-building` | faq:8, legal-framework:3, legal-framework:5, nih-fails-2-institute-health:10 | 4 | `pb-013-buildings` |
| `fomc` | twelve humans of different builds in 1950s suits at one round table, each with a blank name tag, then turned outward covering their papers; the windowless boardroom as a box with a lift-off lid and a little press in the corner | `fomc-room` | central-banks:2, central-banks:21, central-banks:32, central-banks:33 | 4 | `pb-008-places` |
| `giant-suit` | a suit jacket, white collar and tie big enough for a whole brain |  | moronia:1, moronia:7, moronia:8, moronia:9 | 4 | `pb-020-wearables` |
| `index-card` | a plain ruled index card on a little wire stand, and a long paper scroll unrolling from its bottom edge | `recipe-card` | financial-plan:1, nih-fails-2-institute-health:12, roadmap:1, roadmap:5 | 4 | `pb-005-paper` |
| `irs-building` | the IRS as its building: a grey columned tax office with a face and a green eyeshade, hands that cover its eyes, a ruler |  | legal-framework:1, legal-framework:2, legal-framework:3, legal-framework:5 | 4 | `pb-013-buildings` |
| `jalopy` | a rusty 1950s jalopy |  | treaty-feasibility:1, treaty-feasibility:4, treaty-feasibility:12, treaty-feasibility:13 | 4 | `pb-006-vehicles` |
| `martin-luther-king` | Martin Luther King Jr. at the head of a march, and as an engraved portrait holding a petition | `mlk` | global-referendum:4, global-referendum:6, recruitment-and-propaganda-plan:1, recruitment-and-propaganda-plan:4 | 4 | `pb-007-real` |
| `molecule` | ball-and-stick molecules with faces in several shapes and little grabbing hands: tiptoeing, pouring coffee, stamping a foot, sulking |  | fda-is-unsafe-and-ineffective:3, fda-is-unsafe-and-ineffective:10, untapped-therapeutic-frontier:4, wishonia:14 | 4 | `pb-010-body` |
| `notebook` | a school composition notebook, open, ticks on its page |  | dfda:2, dfda:4, dfda:5, dfda:6 | 4 | `pb-005-paper` |
| `noticeboard` | a vast public noticeboard on posts with sheets pinned all over it and green and red tabs | `notice-board` | central-banks:15, dih:4, dih:8, dih:10 | 4 | `pb-022-paper` |
| `oxford-college` | an Oxford college as a character: a dreaming-spire gatehouse with a face, a mortarboard on its tallest spire, stick legs, a tray of pill bottles in its arms |  | dfda:4, nih-fails-2-institute-health:1, nih-fails-2-institute-health:11, nih-fails-2-institute-health:12 | 4 | `pb-013-buildings` |
| `paperclip` | a giant paper clip, straight and bent | `paper-clip` | body-as-repairable-machine:3, body-as-repairable-machine:5, moronia:2, moronia:11 | 4 | `pb-022-paper` |
| `philosophers` | Kant and Nietzsche chin on fist; two philosophers in togas, powdered wigs and 1950s suits with pointers; five gloomy philosophers in black turtlenecks, beards and pipes (smiling a millimetre; fainted flat) |  | genetic-slavery:13, unrepresentative-democracy:7, wishonia:9, wishonia:11 | 4 | `pb-019-period` |
| `robert-pape` | Robert Pape caricatured with a magnifying glass, a pointer and a stack of files |  | aligning-incentives:4, faq:2, peace-dividend:4, unrepresentative-democracy:8 | 4 | `pb-007-real` |
| `sedan` | a 1950s family sedan sputtering a puff of exhaust; and flattened | `car-1950s` | nih-fails-2-institute-health:9, nih-fails-2-institute-health:12, unrepresentative-democracy:1, unrepresentative-democracy:8 | 4 | `pb-006-vehicles` |
| `senator-smith` | a brisk woman senator in a 1950s skirt suit, pearls and a cream Stetson: at a desk, swinging a mallet, at a button, on skis, at a boardroom table; moth wings as a separate piece |  | incentive-alignment-bonds:3, incentive-alignment-bonds:5, incentive-alignment-bonds:6, incentive-alignment-bonds:7 | 4 | `pb-009-people` |
| `slot-machine` | a brass 1950s one-armed bandit with a lever, three reels and a coin tray, a spring-loaded boxing glove that shoots out of its front, and a jackpot state pouring coins | `dopamine-machine` | faq:3, incentive-alignment-bonds:10, unrepresentative-democracy:2, wishonia:14 | 4 | `pb-012-games` |
| `soldier` | a 1950s GI standing with a rifle, squaring off with the rifle raised like a club, in a full-body cast on crutches, charred, shaking, and as a skeleton |  | peace-dividend:1, peace-dividend:2, peace-dividend:3, peace-dividend:5 | 4 | `pb-009-people` |
| `supreme-court` | the Supreme Court building with a face and its own gavel in a white glove |  | 1-percent-treaty:8, legal-framework:2, legal-framework:5, legal-framework:6 | 4 | `pb-013-buildings` |
| `susan-b-anthony` | Susan B. Anthony in black with a parasol and a petition; greyed; her skeleton |  | global-referendum:4, global-referendum:6, recruitment-and-propaganda-plan:1, recruitment-and-propaganda-plan:4 | 4 | `pb-036-real-period` |
| `wishonian` | little round Wishonians in her colours pushing a boulder; arguing; handing a rock under a table |  | central-banks:1, central-banks:7, central-banks:8, central-banks:21 | 4 | `pb-039-host` |
| `wishonian-girl` | an eleven-year-old Wishonian girl with her science-fair trifold |  | central-banks:18, central-banks:29, central-banks:32, central-banks:33 | 4 | `pb-039-host` |
| `ape` | an ape ancestor in a tree, climbing down, with a clipboard; two apes in a tree, one hugging the whole trunk |  | central-banks:22, central-banks:24, untapped-therapeutic-frontier:6 | 3 | `pb-015-animals` |
| `ballot-box-glass` | new pose of `ballot-box`: a glass case with a slot and sealed envelopes inside, its back panel swinging open on gears |  | global-referendum:1, global-referendum:4, global-referendum:5 | 3 | `pb-038-cast-props` |
| `bat-jar` | a grinning bat in a glass jar |  | nih-fails-2-institute-health:4, nih-fails-2-institute-health:9, nih-fails-2-institute-health:10 | 3 | `pb-015-animals` |
| `boxer-shorts` | polka-dot boxer shorts sized for the globe |  | wishonia:13, wishonia:14, wishonia:16 | 3 | `pb-020-wearables` |
| `brain-building` | a white clapboard charity building with a huge pink brain for its roof, on a leash |  | legal-framework:1, legal-framework:2, legal-framework:3 | 3 | `pb-013-buildings` |
| `campaign-chest` | a campaign chest on wheels with a fuel nozzle on a hose |  | treaty-feasibility:7, treaty-feasibility:12, treaty-feasibility:13 | 3 | `pb-016-props` |
| `carbon` | a leering carbon atom with four long arms, arms round others |  | genetic-slavery:1, genetic-slavery:13, genetic-slavery:14 | 3 | `pb-010-body` |
| `corn` | one ear of corn, raw and toasted |  | optimocracy:3, optimocracy:4, optimocracy:6 | 3 | `pb-011-food` |
| `drug-dealer` | a 1950s drug dealer in a zoot suit and pencil moustache whose long coat is lined with little bottles; the empty coat; with two suitcases; fainted | `drug-smuggler` | gdp-trajectories:2, peace-dividend:2, unrepresentative-democracy:7 | 3 | `pb-009-people` |
| `engine-building` | a squat steam-engine building with a smokestack, pistons for legs, a cowcatcher grin, a pay window in its side and a row of levers, a tender rolling out certificates |  | legal-framework:2, legal-framework:3, legal-framework:4 | 3 | `pb-021-buildings` |
| `expert` | an egghead professor in a mortarboard and gown with a pipe and half-moon glasses, standing on a stack of framed diplomas |  | wishocracy:1, wishocracy:3, wishocracy:5 | 3 | `pb-023-people` |
| `gandhi` | Mahatma Gandhi in shawl and round glasses sitting cross-legged with his spinning wheel, and a row of people sitting in a road |  | global-referendum:6, unrepresentative-democracy:1, unrepresentative-democracy:6 | 3 | `pb-007-real` |
| `garage` | a 1950s two-bay repair garage: outside (a shelf, a wall with a painted wrench outline and an empty hook) and inside (a car lift, a second bay) | `car-lift` | body-as-repairable-machine:1, body-as-repairable-machine:4, faq:4 | 3 | `pb-034-places` |
| `garden-hose` | a gleaming green garden hose with a polished brass nozzle and a fancier second nozzle; spraying |  | nonprofit-coalition-strategy:4, nonprofit-coalition-strategy:6, nonprofit-coalition-strategy:7 | 3 | `pb-018-machines` |
| `gift-box` | a gift box with a lid and bow that flies off, a plain beige candle inside, and the box tied with a little net | `candle-gift` | genetic-slavery:8, genetic-slavery:9, roadmap:4 | 3 | `pb-016-props` |
| `ground-squirrel` | a ground squirrel standing upright screaming, diving into a hole, carried in talons, as a little skeleton; a cheater in a domino mask on a nut pile, and its masked skeleton |  | genetic-slavery:3, genetic-slavery:9, genetic-slavery:15 | 3 | `pb-015-animals` |
| `guillotine` | a guillotine with its blade as a separate piece |  | central-banks:3, nonprofit-coalition-strategy:5, optimocracy:4 | 3 | `pb-037-weapons` |
| `hawk` | a hawk in a general's cap, the same hawk zipped into a dove costume, swooping with a squirrel, fat |  | 1-percent-treaty:5, 1-percent-treaty:8, genetic-slavery:3 | 3 | `pb-015-animals` |
| `heart-human` | a 1950s woman in a cardigan and cat-eye glasses, a tissue up her sleeve and a paper Valentine heart pinned to it: typing, dialing, sobbing, holding a placard, holding a globe on her shoulder |  | recruitment-and-propaganda-plan:2, recruitment-and-propaganda-plan:4, recruitment-and-propaganda-plan:6 | 3 | `pb-023-people` |
| `houseplant` | a potted rubber plant in a terracotta pot, and the pot alone big enough to stand in | `flowerpot` | roadmap:7, unrepresentative-democracy:1, unrepresentative-democracy:6 | 3 | `pb-016-props` |
| `judge` | a bald 1950s judge in a black robe with a gavel, his jaw dropping; a tiny wrinkled, extremely fit judge doing a one-armed push-up |  | body-as-repairable-machine:3, body-as-repairable-machine:4, wishonia:15 | 3 | `pb-023-people` |
| `key` | a big brass key on a ribbon, and an iron key on a wall hook that waves |  | dih:10, recruitment-and-propaganda-plan:1, recruitment-and-propaganda-plan:3 | 3 | `pb-016-props` |
| `lady-justice` | Lady Justice on a plinth with her scales as a piece; her blindfold pulled down as a sleep mask and her scales slung as a hammock, asleep and awake | `justice` | legal-framework:1, legal-framework:5, unrepresentative-democracy:1 | 3 | `pb-019-period` |
| `lever-desk` | a brass control desk with two big levers whose handles are a carrot and a stick, and a little third lever |  | genetic-slavery:4, genetic-slavery:13, genetic-slavery:14 | 3 | `pb-018-machines` |
| `mainframe-face` | face pieces for `mainframe`: two reel eyes that swivel and a tape-slot mouth that smiles |  | moronia:10, moronia:12, moronia:14 | 3 | `pb-024-cast-creatures` |
| `mortarboard` | a graduation cap and tassel that sits on a missile |  | moronia:2, moronia:11, moronia:14 | 3 | `pb-020-wearables` |
| `moving-van` | a 1950s moving van |  | central-banks:22, central-banks:23, central-banks:24 | 3 | `pb-025-vehicles` |
| `nonprofit-building` | a brick nonprofit building with a face whose door is a donation tin; barking; and as rubble |  | recruitment-and-propaganda-plan:2, recruitment-and-propaganda-plan:3, recruitment-and-propaganda-plan:4 | 3 | `pb-021-buildings` |
| `nonprofit-factory` | a big factory with a face and many windows (dogs at typewriters inside), an output chute and a plain side wall |  | nonprofit-coalition-strategy:5, nonprofit-coalition-strategy:6, nonprofit-coalition-strategy:7 | 3 | `pb-021-buildings` |
| `ocean-liner` | a 1950s ocean liner with a funnel and flag, a rail deck that tilts; sinking; its wreck | `titanic` | central-banks:12, fda-is-unsafe-and-ineffective:10, nonprofit-coalition-strategy:1 | 3 | `pb-025-vehicles` |
| `paper-bag` | a brown paper bag with torn eyeholes that inflates and crumples, and one twisted shut with a skull and crossbones | `dope-bag` | 1-percent-treaty:9, incentive-alignment-bonds:4, optimocracy:2 | 3 | `pb-016-props` |
| `pistol` | a plain revolver whose cylinder swings out as its own piece | `six-shooter` | central-banks:22, central-banks:27, recruitment-and-propaganda-plan:9 | 3 | `pb-037-weapons` |
| `poker-chips` | poker chips in stacks and loose, and a tower made of them |  | central-banks:18, central-banks:19, central-banks:20 | 3 | `pb-012-games` |
| `pylon` | an electricity pylon with its copper lines, and stripped bare |  | moronia:5, moronia:11, moronia:12 | 3 | `pb-018-machines` |
| `ray-machine` | a big brass 1950s science apparatus on a swivel base, a long barrel with a lens at the tip, dials and coils |  | wishonia:1, wishonia:4, wishonia:8 | 3 | `pb-018-machines` |
| `refrigerator` | a 1940s Frigidaire with an opening door and stubby legs, and with a machine-gun barrel out of its door | `frigidaire` | 1-percent-treaty:5, faq:2, nonprofit-coalition-strategy:5 | 3 | `pb-016-props` |
| `rifle` | a rifle that swings as a piece, a Springfield rifle and a Browning machine gun | `wartime-guns` | 1-percent-treaty:2, incentive-alignment-bonds:3, nonprofit-coalition-strategy:5 | 3 | `pb-037-weapons` |
| `rocket` | a tall rocket on its launch pad (one drawing for the 1950s rocket and the Apollo) | `apollo-rocket` | faq:4, faq:6, genetic-slavery:12 | 3 | `pb-025-vehicles` |
| `roulette-table` | a 1950s roulette table and wheel, and a green-felt betting table | `betting-table` | aligning-incentives:6, treaty-feasibility:5, treaty-feasibility:9 | 3 | `pb-012-games` |
| `stone-tablet` | a cracked mossy carved stone tablet on an easel |  | dih:3, dih:10, peace-dividend:5 | 3 | `pb-017-props` |
| `strongman` | a Victorian circus strongman in a striped leotard with a curled moustache: flexing, arms up sweating, flat on his back | `muscleman` | fda-is-unsafe-and-ineffective:1, fda-is-unsafe-and-ineffective:8, incentive-alignment-bonds:10 | 3 | `pb-019-period` |
| `suitcase` | a vacation suitcase with travel stickers |  | central-banks:17, central-banks:18, central-banks:20 | 3 | `pb-017-props` |
| `sweater` | a giant ugly knitted sweater sized for the globe with six blank patches and a loose thread: whole, one patch unravelled, half, gone, its knit pieces separate, and a ball of yarn |  | wishonia:10, wishonia:12, wishonia:13 | 3 | `pb-020-wearables` |
| `sword-building` | the military as a fortress building with a face, holding a long sword whose point can show on its own |  | legal-framework:1, legal-framework:2, legal-framework:3 | 3 | `pb-021-buildings` |
| `three-way-valve` | a brass pipe junction that splits one pipe into three, with a valve wheel, screw caps and pipe lagging | `splitter` | 1-percent-treaty:6, incentive-alignment-bonds:4, incentive-alignment-bonds:8 | 3 | `pb-018-machines` |
| `tree` | a big shade tree in three growth stages from a sprout, a stand of trees, and burnt black stumps | `forest` | nonprofit-coalition-strategy:2, peace-dividend:5, peace-dividend:6 | 3 | `pb-044-nature` |
| `turmeric-jar` | a yellow spice jar and its lid |  | dfda:3, dfda:6, dfda:7 | 3 | `pb-017-props` |
| `umbrella` | a big black umbrella open and shut, and an umbrella made of a stapled stack of papers, dry and soggy |  | nih-fails-2-institute-health:2, optimocracy:6, peace-dividend:4 | 3 | `pb-017-props` |
| `wallet` | YOU's leather wallet, open | `you-wallet` | central-banks:19, wishonia:6, wishonia:8 | 3 | `pb-017-props` |
| `wedding-party` | a 1950s bride and groom with guests in their best and a tiered cake under a striped awning; the party as grinning skeletons in veils and bow ties; the couple forty years older throwing plates | `wedding-couple` | fda-is-unsafe-and-ineffective:9, moronia:3, moronia:17 | 3 | `pb-023-people` |
| `wishing-well` | a stone wishing well with a little roof, a bucket and a crank; dry |  | peace-dividend:3, peace-dividend:5, wishocracy:6 | 3 | `pb-017-props` |
| `amygdala` | an almond-shaped brass alarm bell with a face and stick legs, and a cord |  | genetic-slavery:11, genetic-slavery:15 | 2 | `pb-010-body` |
| `ant` | an ant in a little hat and tie walking, an army ant in thick round glasses, and their skeletons still walking | `ant-skeleton`, `army-ant`, `army-ant-skeleton` | unrepresentative-democracy:3, wishocracy:3 | 2 | `pb-026-animals` |
| `antibody-fridge` | a walk-in fridge with a glass front and a thermometer, stacked with boxed doses; its door takes padlocks |  | nih-fails-2-institute-health:2, nih-fails-2-institute-health:3 | 2 | `pb-018-machines` |
| `ballot` | a ballot on stick legs with a toe tag |  | unrepresentative-democracy:1, unrepresentative-democracy:3 | 2 | `pb-022-paper` |
| `bandwagon` | a circus bandwagon with a brass band on top and wheels stuck in mud |  | roadmap:3, roadmap:4 | 2 | `pb-025-vehicles` |
| `banker` | a sheet of bowler-hatted bankers in pinstripes with umbrellas, many builds |  | central-banks:29, central-banks:33 | 2 | `pb-023-people` |
| `benefits-machine` | a brass contraption of pipes that sorts papers by itself, with a mechanical arm that slaps away hands |  | faq:4, faq:8 | 2 | `pb-029-machines` |
| `birthday-candle` | one fat birthday candle |  | central-banks:4, central-banks:6 | 2 | `pb-011-food` |
| `blinkers` | a horse's blinkers on a strap, sized for a dog |  | nonprofit-coalition-strategy:4, nonprofit-coalition-strategy:5 | 2 | `pb-020-wearables` |
| `bls-building` | the Bureau of Labor Statistics as an engraved office building with window eyes, a door mouth and white-gloved stick arms that hold a key |  | optimocracy:5, optimocracy:6 | 2 | `pb-021-buildings` |
| `blueprint` | a rolled blueprint that unrolls |  | nih-fails-2-institute-health:11, nih-fails-2-institute-health:12 | 2 | `pb-022-paper` |
| `boxing-gloves` | boxing gloves for YOU, and boxing gloves, stick legs and a towel that fit the green money bundle |  | aligning-incentives:4, treaty-feasibility:2 | 2 | `pb-020-wearables` |
| `bretton-woods-hotel` | the big white Bretton Woods resort hotel with a red roof, and the same hotel in cutaway | `hotel` | central-banks:9, central-banks:20 | 2 | `pb-034-places` |
| `camo-tin` | new pose of `paint-tin`: camouflage-painted and as tall as a man |  | peace-dividend:1, peace-dividend:3 | 2 | `pb-038-cast-props` |
| `cantillon` | Richard Cantillon, 1700s banker in a powdered wig, with a quill and an open notebook |  | central-banks:15, central-banks:16 | 2 | `pb-036-real-period` |
| `cargo-ship` | a toy-sized cargo ship stacked with containers; charred |  | peace-dividend:1, peace-dividend:2 | 2 | `pb-025-vehicles` |
| `carrot` | one perfect carrot, and with a bite gone |  | moronia:5, moronia:16 | 2 | `pb-011-food` |
| `casino` | a 1950s Las Vegas casino with a blank neon marquee, wide enough to sit on a row of roofs |  | central-banks:18, central-banks:20 | 2 | `pb-034-places` |
| `cell-locks` | new pose of `cell`: one big body cell studded with hundreds of little brass locks, some shiny, some rusted shut under cobwebs |  | untapped-therapeutic-frontier:1, untapped-therapeutic-frontier:5 | 2 | `pb-024-cast-creatures` |
| `cell-states` | new states of `cell`: worn (grey, cane, bandaged), new and shiny, a grumpy grown-up cell in a tiny hat with a briefcase and a pinhole in its side, a baby stem cell in a bonnet with a dummy, a beating heart cell, a wiry brain cell in spectacles, a cell in a judge's robe |  | body-as-repairable-machine:2, body-as-repairable-machine:3 | 2 | `pb-024-cast-creatures` |
| `census-building` | the Census Bureau as a long engraved institution building with window eyes, a door mouth and white-gloved stick arms that hold a placard |  | optimocracy:5, optimocracy:6 | 2 | `pb-021-buildings` |
| `cheater` | an everyday man with his fingers crossed behind his back, and disguise pieces (a wig, a headscarf) |  | global-referendum:2, global-referendum:3 | 2 | `pb-023-people` |
| `cheeseburger` | a cheeseburger with a little face and stick legs |  | genetic-slavery:11, genetic-slavery:13 | 2 | `pb-011-food` |
| `chicken` | a plump hen; a hen in a cage too small to turn in; a broiler whose legs fold under it; charred, blinking |  | central-banks:5, central-banks:15 | 2 | `pb-026-animals` |
| `cloche` | a silver platter with a domed cloche lid, and a truffle shaver | `truffle-platter` | dfda:4, unrepresentative-democracy:4 | 2 | `pb-028-food` |
| `college-student` | a 1950s college boy in a letter sweater and beanie, with a beer stein; one finger up, then drooping | `econ-student` | central-banks:5, wishonia:1 | 2 | `pb-031-people` |
| `convertible` | a 1950s two-tone convertible with the top down, a child seat in the back, the seats as pieces |  | wishonia:14, wishonia:16 | 2 | `pb-025-vehicles` |
| `cookbook` | a fat leather cookbook with a gold ribbon; a stack; a page torn out |  | nih-fails-2-institute-health:4, nih-fails-2-institute-health:12 | 2 | `pb-022-paper` |
| `corporation` | new pose of `briefcase`: on stick legs, its lid opening like a mouth; small ones for newborns |  | legal-framework:2, legal-framework:5 | 2 | `pb-038-cast-props` |
| `country-maps-2` | more `country-maps`: Venezuela, and Venezuela crumbled to a fifth of itself; Lebanon; Japan with Mount Fuji, a factory and a bullet train on it |  | gdp-trajectories:3, wishonia:7 | 2 | `pb-038-cast-props` |
| `creditworm` | a little worm in a rosette, and the same worm see-through |  | aligning-incentives:4, aligning-incentives:8 | 2 | `pb-026-animals` |
| `dartboard` | a pub dartboard and darts |  | nih-fails-2-institute-health:8, wishocracy:5 | 2 | `pb-012-games` |
| `dawkins` | Richard Dawkins caricatured: lean, long face, raised eyebrow, 1970s jacket and wide tie, holding his book |  | genetic-slavery:3, genetic-slavery:4 | 2 | `pb-033-real` |
| `de-gaulle` | Charles de Gaulle caricatured: very tall, enormous nose, kepi, dark glasses, a baton |  | central-banks:9, central-banks:20 | 2 | `pb-033-real` |
| `dna-helix` | a tall plain DNA double helix that twists and untwists | `dna-strand` | central-banks:29, dfda:9 | 2 | `pb-010-body` |
| `elevator` | a cutaway 1950s brass elevator car with a folding gate and a floor dial above its door, and its operator in a pillbox hat and white gloves with a clipboard |  | dih:10, wishonia:8 | 2 | `pb-029-machines` |
| `emmeline-pankhurst` | Emmeline Pankhurst in her Edwardian hat and sash holding out a pamphlet | `suffragette` | faq:6, recruitment-and-propaganda-plan:4 | 2 | `pb-033-real` |
| `fat-cat-family` | the fat cat's family: a fat wife in pearls and two fat children, in his look |  | treaty-feasibility:8, treaty-feasibility:9 | 2 | `pb-041-fat-cat-lobbyist` |
| `flat-tire` | a flat tire in a beret with a cigarette |  | body-as-repairable-machine:1, body-as-repairable-machine:5 | 2 | `pb-046-vehicles` |
| `fountain-pen` | a fat fountain pen with a price tag on a string |  | treaty-feasibility:1, treaty-feasibility:3 | 2 | `pb-032-props` |
| `frederick-douglass` | Frederick Douglass as an engraved portrait holding a petition |  | recruitment-and-propaganda-plan:1, recruitment-and-propaganda-plan:4 | 2 | `pb-036-real-period` |
| `g-man` | a federal agent in a fedora and trench coat at a typewriter; a dozen in different builds; grey-haired versions |  | moronia:10, moronia:11 | 2 | `pb-031-people` |
| `gas-pump` | two 1950s gas pumps with round glass globes |  | treaty-feasibility:1, treaty-feasibility:12 | 2 | `pb-029-machines` |
| `germ-doctor` | new pose of `germ`: in a white coat with a head mirror and stethoscope |  | central-banks:32, central-banks:33 | 2 | `pb-024-cast-creatures` |
| `glass-vault` | the Treaty Fund as a glass bank vault on short legs with a calm round dial face and an outlet pipe with a valve |  | dih:8, dih:10 | 2 | `pb-029-machines` |
| `graduate` | a young 1950s woman in a cap and gown with a diploma; with a rivet gun; with gleaming teeth; at a missile workbench; at a microscope |  | central-banks:30, central-banks:32 | 2 | `pb-031-people` |
| `groucho-glasses` | glasses, a fake nose and a moustache as a disguise |  | aligning-incentives:10, aligning-incentives:11 | 2 | `pb-040-wearables` |
| `gum` | a stick of gum in its wrapper |  | global-referendum:4, global-referendum:5 | 2 | `pb-028-food` |
| `hair` | a mane of hair growing from a bald head to the floor in three lengths, and eyebrows to match |  | untapped-therapeutic-frontier:1, untapped-therapeutic-frontier:4 | 2 | `pb-010-body` |
| `hamilton` | W. D. Hamilton caricatured: tall, rumpled, shy, 1960s jacket, with a card |  | genetic-slavery:3, genetic-slavery:7 | 2 | `pb-033-real` |
| `hamster` | a hamster in a toga with a lightning bolt pressing a button, running in its wheel, hopping off it, charred |  | genetic-slavery:10, wishonia:13 | 2 | `pb-026-animals` |
| `hayek` | Friedrich Hayek caricatured with a Nobel medal |  | wishocracy:5, wishocracy:6 | 2 | `pb-033-real` |
| `hedge-fund` | a topiary hedge clipped into a dollar sign, its clippings and garden shears |  | incentive-alignment-bonds:9, incentive-alignment-bonds:11 | 2 | `pb-012-games` |
| `helmet-skeletons` | grinning skeletons sitting up out of paper in the headgear of each war: a bicorne, a kepi, a doughboy's helmet, a 1940s steel helmet, a parka hood, a jungle helmet, a desert helmet |  | central-banks:6, central-banks:7 | 2 | `pb-037-weapons` |
| `horse` | a big plain horse with a tube of dewormer in its teeth, and a dray horse with a tag |  | nih-fails-2-institute-health:11, wishocracy:2 | 2 | `pb-026-animals` |
| `hospital-giant` | a gleaming white hospital on a hill with columns and a cross, no door, one brass mail slot at knee height; and the same with its walls fallen flat |  | dfda:1, dfda:9 | 2 | `pb-027-buildings` |
| `hydrogen` | a single-electron hydrogen atom with a worried face biting its nails: drifting, yawning, squashed in a heap, on fire |  | genetic-slavery:1, genetic-slavery:2 | 2 | `pb-047-body` |
| `ice-cream-cone` | an ice-cream cone in a paper wrapper, and a towering cone whose scoops are rolled green bills | `ice-cream` | central-banks:19, wishonia:4 | 2 | `pb-028-food` |
| `iron-stove` | a cast-iron stove with an oven door |  | central-banks:3, central-banks:5 | 2 | `pb-032-props` |
| `king` | a medieval king in a crown and ermine with a big chicken leg, on a throne that tips | `medieval-king` | central-banks:25, faq:6 | 2 | `pb-019-period` |
| `label-gun` | a label gun that clacks out tape labels |  | legal-framework:1, legal-framework:6 | 2 | `pb-029-machines` |
| `lbj` | Lyndon Johnson caricatured: huge ears, big nose, cowboy hat; sitting |  | central-banks:6, central-banks:9 | 2 | `pb-033-real` |
| `lobbyist-cross-suit` | new pose of `lobbyist`: his trench coat patterned in little crosses |  | roadmap:6, roadmap:7 | 2 | `pb-041-fat-cat-lobbyist` |
| `lobbyist-peck` | new pose of `lobbyist`: bent at the waist, pecking and bobbing like a pigeon |  | aligning-incentives:1, aligning-incentives:10 | 2 | `pb-041-fat-cat-lobbyist` |
| `locomotive` | an 1880s steam engine |  | central-banks:10, central-banks:13 | 2 | `pb-046-vehicles` |
| `madoff` | Bernie Madoff: white hair, big grin, dark suit, with a ruler; and in prison stripes |  | financial-plan:1, financial-plan:5 | 2 | `pb-045-real` |
| `mannequin` | a department-store mannequin in a hospital gown with a sad painted face, on a dolly; a unicorn horn for its forehead |  | dfda:2, dfda:9 | 2 | `pb-031-people` |
| `mechanic` | a 1950s service-station attendant in a peaked cap, bow tie and coveralls with a rag, a dipstick and a spanner |  | faq:4, wishonia:4 | 2 | `pb-031-people` |
| `medicine-cabinet` | a mirrored 1950s bathroom cabinet with three glass shelves and a door that swings |  | untapped-therapeutic-frontier:2, untapped-therapeutic-frontier:4 | 2 | `pb-032-props` |
| `medicine-plug` | a fat old plug on a cord with a cross on it, lying on the floor, cobwebbed |  | dfda:1, dfda:9 | 2 | `pb-029-machines` |
| `murderer` | a hulking scarred thug in a striped shirt and flat cap with a club; the same man hammering, sawing and nail-gunning a pile of lumber with the same grin |  | genetic-slavery:14, genetic-slavery:15 | 2 | `pb-031-people` |
| `nesting-doll` | five Russian nesting dolls painted as frowning clerks in different hats, each half separate |  | recruitment-and-propaganda-plan:1, recruitment-and-propaganda-plan:3 | 2 | `pb-032-props` |
| `pentagon-face` | new pose of `pentagon`: the Pentagon with a face and two stubby hands |  | faq:1, faq:8 | 2 | `pb-053-building-poses` |
| `pharaoh` | a pharaoh on his throne with crook and flail, a cloth tied round his swollen jaw; slumped |  | central-banks:25, wishonia:6 | 2 | `pb-051-period` |
| `pizza` | a pizza on a tin that tears into slices, and its box |  | nonprofit-coalition-strategy:4, recruitment-and-propaganda-plan:13 | 2 | `pb-028-food` |
| `pod` | an open steel box 0.7 by 2.1 meters with a man in a 1950s shirt lying in it, one elbow against the wall; the same man in a feeding-stall head bracket |  | moronia:14, moronia:15 | 2 | `pb-032-props` |
| `police-station` | a little police station with a face, a police cap on its roof and stick arms |  | unrepresentative-democracy:4, unrepresentative-democracy:8 | 2 | `pb-027-buildings` |
| `printed-parts` | printed body parts: a windpipe, a titanium skull cap, a chattering jaw, a lab-grown bladder, a kidney, a pink brain and a tiny walnut-sized old brain, a little green Yoda figurine |  | body-as-repairable-machine:1, body-as-repairable-machine:3 | 2 | `pb-047-body` |
| `printer-3d` | a 1950s-styled 3D printer, a boxy cabinet with a nozzle on a gantry |  | body-as-repairable-machine:1, body-as-repairable-machine:3 | 2 | `pb-030-machines` |
| `prison` | the detention industry as a grinning brick prison, barred windows for eyes, its gate a mouth |  | moronia:1, moronia:6 | 2 | `pb-027-buildings` |
| `puppet-booth` | a Punch-and-Judy puppet booth with a curtain, and a lectern on a plain stage with a cross-bar of strings high above it | `puppet-stage` | aligning-incentives:8, genetic-slavery:13 | 2 | `pb-034-places` |
| `question-mark` | a big question mark on little legs, sweating |  | recruitment-and-propaganda-plan:12, recruitment-and-propaganda-plan:13 | 2 | `pb-022-paper` |
| `recorder-kid` | a 1950s schoolkid in a striped T-shirt squeaking a recorder; charred |  | central-banks:25, central-banks:29 | 2 | `pb-042-people` |
| `rent-row` | a rent envelope, a grocery bag, a pill bottle and a piggy bank, each able to shrink |  | central-banks:2, central-banks:8 | 2 | `pb-032-props` |
| `serf` | a barefoot medieval peasant in a sackcloth tunic with a hoe: stacking a rock, with a spear, with a pitchfork, reading, asleep; charred |  | central-banks:11, central-banks:25 | 2 | `pb-051-period` |
| `shakespeare` | William Shakespeare caricatured (bald dome, earring, ruff) at a writing desk with a quill, Yorick's skull and a pile of pages; coughing; his skeleton with the quill |  | body-as-repairable-machine:1, health-dividend:2 | 2 | `pb-036-real-period` |
| `shopfront` | a sheet of 1950s high-street shopfronts (a diner, an office, a barber with a striped pole, a store), each with a blank hanging sign |  | dih:9, dih:10 | 2 | `pb-034-places` |
| `skeptic-pessimist` | new poses of `pessimist` as the Skeptic: arms folded, raised eyebrow clutching his pearls, fainting, pushing a turnstile, crawling, writing a slip, checking a pocket watch, in a dunce cap | `skeptic` | faq:1, faq:8 | 2 | `pb-049-cast-poses` |
| `skyscraper` | a 1950s skyscraper with a pulley at the top and a penthouse window |  | recruitment-and-propaganda-plan:2, recruitment-and-propaganda-plan:6 | 2 | `pb-052-places` |
| `smart-contract` | a glass-cased clockwork machine on a pedestal with a scroll turning inside, a chute out the front and a pipe into the back |  | wishonia:7, wishonia:8 | 2 | `pb-030-machines` |
| `soul-chalet` | the Soul as a Swiss chalet with a cuckoo-clock face, a little door for the cuckoo, a vault door in its side, a gold halo and a leash |  | legal-framework:3, legal-framework:4 | 2 | `pb-027-buildings` |
| `stapler` | a giant office stapler that slams |  | moronia:4, moronia:6 | 2 | `pb-030-machines` |
| `steak` | a raw steak on a fork; sausages, chops and steaks that float; a steak holding a telephone handset | `meat-river` | body-as-repairable-machine:2, roadmap:4 | 2 | `pb-028-food` |
| `sugar-refinery` | a brick sugar refinery with a smokestack, window eyes, a grin and white-gloved stick arms |  | unrepresentative-democracy:2, unrepresentative-democracy:8 | 2 | `pb-027-buildings` |
| `suggestion-box` | a wooden box on a post with a slot and no bottom; kneeling, praying |  | fda-is-unsafe-and-ineffective:7, fda-is-unsafe-and-ineffective:11 | 2 | `pb-035-props` |
| `suit-kids` | three children of about eight in sharp tailored suits and slicked hair: daring, pointing, biting |  | central-banks:18, central-banks:19 | 2 | `pb-042-people` |
| `think-tank` | a big glass aquarium on a stand with three men in tweed suits floating thoughtfully, bubbles rising; drained, with them flopped on the gravel | `fish-tank` | central-banks:21, wishonia:12 | 2 | `pb-035-props` |
| `ties` | a gambler's bow tie and a sober striped necktie sized for a building |  | central-banks:15, central-banks:20 | 2 | `pb-040-wearables` |
| `toilet` | a 1950s toilet with a chain flush, and a gold toilet seat | `toilet-seat` | global-referendum:6, moronia:10 | 2 | `pb-035-props` |
| `toll-booth` | a toll booth whose cash box has a pipe running to a waistcoat pocket | `toll-bridge` | treaty-feasibility:7, treaty-feasibility:11 | 2 | `pb-052-places` |
| `tomato` | a tomato and its splat |  | aligning-incentives:6, aligning-incentives:8 | 2 | `pb-028-food` |
| `toy-blocks` | plain wooden toy blocks of a few sizes with blank faces, stackable | `alphabet-blocks` | faq:8, health-dividend:1 | 2 | `pb-035-props` |
| `toy-wheel` | a toy steering wheel on a suction cup |  | genetic-slavery:11, genetic-slavery:15 | 2 | `pb-035-props` |
| `treaty-walker` | a rolled document on stick legs with a face; crumpled with X-eyes; as a little scroll skeleton | `reform-bill` | 1-percent-treaty:8, faq:5 | 2 | `pb-050-paper` |
| `trench-coat` | an empty tall trench coat and fedora open and closed, and three kids stacked in one trench coat with a hat on top | `trench-coat-kids` | genetic-slavery:2, global-referendum:2 | 2 | `pb-040-wearables` |
| `trial-machine` | a gleaming 1950s world's-fair machine in chrome and glass: bottles in at one side, a moving walkway past it, result cards out, dials and a flag, a plug on a cord; and a vending machine that spits bills back out |  | body-as-repairable-machine:5, untapped-therapeutic-frontier:7 | 2 | `pb-030-machines` |
| `trilobite` | a trilobite alive and as a fossil |  | body-as-repairable-machine:1, body-as-repairable-machine:2 | 2 | `pb-026-animals` |
| `union-man` | a 1950s union worker in a flat cap, rolled sleeves and overalls hugging a jar of green bills; his beard as a piece that grows to the floor |  | central-banks:22, central-banks:24 | 2 | `pb-042-people` |
| `valentine-box` | a heart-shaped candy box with a ribbon, and a stack of them |  | 1-percent-treaty:1, 1-percent-treaty:4 | 2 | `pb-057-food` |
| `waiter-kit` | a waiter's long apron, a napkin over the arm, a towel and a silver tray | `waiter-apron` | central-banks:15, unrepresentative-democracy:6 | 2 | `pb-040-wearables` |
| `wall-socket` | a big brass wall socket with many plugs in it |  | dfda:1, dfda:9 | 2 | `pb-030-machines` |
| `wall-street` | a columned brokerage front with a ticker-tape awning, a face, big ears and a hole straight through its head from ear to ear |  | legal-framework:2, legal-framework:4 | 2 | `pb-027-buildings` |
| `war-mountain` | a snow-capped mountain built of war bills with a plain missile nose for its peak, which also floats as an iceberg |  | nonprofit-coalition-strategy:1, nonprofit-coalition-strategy:4 | 2 | `pb-044-nature` |
| `who-building` | the W.H.O. as its building: the Geneva headquarters slab with a face and its snake-and-staff emblem |  | nih-fails-2-institute-health:6, nih-fails-2-institute-health:11 | 2 | `pb-048-buildings` |
| `x-ray-machine` | a 1950s X-ray machine |  | faq:2, faq:5 | 2 | `pb-030-machines` |
| `yamanaka` | Shinya Yamanaka caricatured: slim, neat hair, glasses, lab coat, a petri dish |  | body-as-repairable-machine:3, body-as-repairable-machine:5 | 2 | `pb-045-real` |
| `abacus` | a dusty wooden abacus |  | central-banks:18 | 1 | `pb-059-machines` |
| `academic` | an academic in a gown and mortarboard stroking his chin, with opera glasses |  | global-referendum:4 | 1 | `pb-042-people` |
| `alarm-clock` | a twin-bell alarm clock with no snooze button, only a solid brass top |  | dih:5 | 1 | `pb-059-machines` |
| `alchemist` | a medieval alchemist in a pointed hat with a crucible and bellows |  | central-banks:21 | 1 | `pb-051-period` |
| `alien-visitors` | a row of visiting aliens in 1950s good clothes (an octopus in a bowler, a three-eyed lady in pearls, a crystal man in a tweed jacket, cracked), one fainting |  | moronia:17 | 1 | `pb-014-aliens` |
| `antibody-dose` | a boxed infusion bag of antibodies, fresh, and green and furry when expired |  | nih-fails-2-institute-health:2 | 1 | `pb-059-machines` |
| `apple` | an apple |  | treaty-feasibility:10 | 1 | `pb-057-food` |
| `archery-target` | a straw archery target on an easel, which also straps to a chest |  | central-banks:12 | 1 | `pb-035-props` |
| `aristocrats` | French aristocrats in powdered wigs and lace; their wigs; their skeletons in wigs |  | central-banks:3 | 1 | `pb-051-period` |
| `athenian` | an Athenian in a chiton with a sack, and a heap of pottery shards |  | global-referendum:2 | 1 | `pb-051-period` |
| `attack-dog` | a slavering attack dog on a chain, in several builds |  | 1-percent-treaty:2 | 1 | `pb-082-animals` |
| `baby-photo` | a framed photo of a masked baby holding a test tube |  | aligning-incentives:4 | 1 | `pb-050-paper` |
| `ballot-drum` | a brass lottery drum with a crank, a glass window and gears, sealed numbered envelopes and a tear-off stub |  | global-referendum:2 | 1 | `pb-058-games` |
| `banana-costume` | a banana costume and its delivery box |  | dfda:5 | 1 | `pb-040-wearables` |
| `bang-pistol` | a toy pistol whose barrel pops out a little flag |  | incentive-alignment-bonds:7 | 1 | `pb-113-weapons` |
| `bank-steeple` | new pose of `bank`: a church steeple growing out of the bank's roof, and a stone font by its door that sprinkles bills |  | central-banks:26 | 1 | `pb-053-building-poses` |
| `barbarians` | two hairy barbarians in furs wiping their feet |  | central-banks:3 | 1 | `pb-098-period` |
| `barber-shop` | a barber's chair, an eager apprentice with scissors, a customer whose hair grows to the floor (and as a topiary), a licensed barber with a framed licence and clippers |  | moronia:8 | 1 | `pb-052-places` |
| `bathroom-scale` | a bathroom scale with a dial and a needle that snaps |  | gdp-trajectories:2 | 1 | `pb-059-machines` |
| `bathtub` | a clawfoot bathtub, a drain that swirls, the plug a gold bar on a chain |  | central-banks:22 | 1 | `pb-072-props` |
| `bear` | a bear as tall as the frame roaring and swiping, and three bear cubs curled up like a log | `bear-cubs` | legal-framework:5 | 1 | `pb-082-animals` |
| `beatles` | the Beatles caricatured in collarless 1962 suits and mop tops with guitars and a drum, and as bearded 1970 versions walking off in four directions |  | fda-is-unsafe-and-ineffective:12 | 1 | `pb-045-real` |
| `bee` | a bee |  | gdp-trajectories:6 | 1 | `pb-082-animals` |
| `beehive` | a beehive dripping honey |  | genetic-slavery:9 | 1 | `pb-057-food` |
| `beer-bottle` | a beer bottle |  | treaty-feasibility:1 | 1 | `pb-057-food` |
| `beer-mug` | two clinking glass beer mugs with foam |  | genetic-slavery:6 | 1 | `pb-057-food` |
| `beret` | a black beret that swaps in for YOU's fedora |  | wishonia:2 | 1 | `pb-040-wearables` |
| `berry-bush` | a round berry bush heavy with berries |  | genetic-slavery:5 | 1 | `pb-089-food` |
| `bicorne` | Napoleon's bicorne as a loose piece for `rulers` (and for a whale) |  | body-as-repairable-machine:5 | 1 | `pb-043-cast-period` |
| `bill-cake` | a tall layered cake of green bills on a cake stand, and the empty stand with crumbs | `cake` | central-banks:16 | 1 | `pb-089-food` |
| `bill-gates` | Bill Gates caricatured: big glasses, a sweater, a strapped bundle |  | legal-framework:1 | 1 | `pb-045-real` |
| `billionaires` | Jeff Bezos and Elon Musk caricatured, standing like museum waxworks; Bezos at a yacht rail |  | wishonia:6 | 1 | `pb-045-real` |
| `binder-asleep` | new pose of `binder`: closed eyes and a nightcap |  | legal-framework:6 | 1 | `pb-038-cast-props` |
| `biotech-garage` | a ragged garage lab with a face, grabbing |  | aligning-incentives:7 | 1 | `pb-048-buildings` |
| `bis-tower` | the round Bank for International Settlements tower in Basel with a smug face |  | central-banks:13 | 1 | `pb-048-buildings` |
| `black-hole` | a swirl of stars round a dark mouth that gulps, burps and closes into a smile |  | wishonia:16 | 1 | `pb-044-nature` |
| `blindfold` | a blindfold |  | fda-is-unsafe-and-ineffective:10 | 1 | `pb-078-wearables` |
| `bond-eagle` | the engraved war-bond eagle, wings spread, two plain bombs in its talons, and the same eagle with empty talons and an innocent look |  | incentive-alignment-bonds:1 | 1 | `pb-050-paper` |
| `bone-ship` | a Greek galley built of bones, its skull figurehead in a spare fedora, some planks a cigarette, a hot dog, a beer can and a lottery ticket |  | body-as-repairable-machine:2 | 1 | `pb-046-vehicles` |
| `bow` | a longbow and arrows |  | central-banks:12 | 1 | `pb-072-props` |
| `bowhead-whale` | a bowhead whale swimming, surfacing, holding a monocle up with a flipper |  | body-as-repairable-machine:5 | 1 | `pb-082-animals` |
| `braces-kids` | two kids grinning up in mouthfuls of braces |  | moronia:11 | 1 | `pb-042-people` |
| `british-empire` | the British Empire as a huge steam-roller with a crown on its funnel, a Union Jack and a face in its boiler |  | global-referendum:6 | 1 | `pb-046-vehicles` |
| `broom-closet` | a small basement closet with a bare bulb, a mop, three shelves and a back door |  | nih-fails-2-institute-health:5 | 1 | `pb-052-places` |
| `buddha` | a Buddha statue gesturing, and shrugging |  | genetic-slavery:13 | 1 | `pb-098-period` |
| `button-wall` | one red button in a bunker panel |  | 1-percent-treaty:2 | 1 | `pb-113-weapons` |
| `cage` | a cage that drops from above, on little wheels |  | legal-framework:5 | 1 | `pb-072-props` |
| `camera-pole` | a security camera on a pole that swivels and waves a little hand |  | moronia:15 | 1 | `pb-059-machines` |
| `candidate-works` | a long brick factory with a grinning door, a hopper on top and stamping arms |  | unrepresentative-democracy:4 | 1 | `pb-048-buildings` |
| `car-cutaway` | a 1950s chrome sedan in cutaway with eight cylinders and pistons as separate pieces, four cylinders open to seat little committee men, a glovebox that drops open |  | optimocracy:2 | 1 | `pb-046-vehicles` |
| `car-parts` | car parts as body parts: a brake pad shaped like a hip joint, a fuel line clogged with a cheeseburger, a little stent, a heart-shaped car battery, a gearbox tangled in string and goo |  | body-as-repairable-machine:4 | 1 | `pb-047-body` |
| `card-table` | a folding card table and chair |  | 1-percent-treaty:4 | 1 | `pb-072-props` |
| `cargo-plane` | a 1960s propeller cargo plane |  | central-banks:9 | 1 | `pb-046-vehicles` |
| `carousel` | a fairground carousel with painted horses and blank rim panels, and crushed flat |  | dih:6 | 1 | `pb-058-games` |
| `cathedral` | a Gothic cathedral that can topple |  | central-banks:13 | 1 | `pb-048-buildings` |
| `ceiling-star` | a plaster ceiling with a star rose that cracks and falls in chunks |  | wishocracy:5 | 1 | `pb-072-props` |
| `celebrity` | a 1950s film star in sunglasses and furs at a podium |  | unrepresentative-democracy:4 | 1 | `pb-042-people` |
| `cell-parts` | cell parts: a chromosome with shoelace tips, a mitochondrion like a battery, a DNA ladder with a broken rung |  | faq:4 | 1 | `pb-047-body` |
| `chairlift` | a two-seat chairlift chair on its cable |  | incentive-alignment-bonds:7 | 1 | `pb-109-vehicles` |
| `champagne` | a champagne bottle that pops, and a coupe glass bubbling, flat and dusty |  | incentive-alignment-bonds:8 | 1 | `pb-089-food` |
| `champagne-tower` | a pyramid of coupe glasses with green bills sloshing in them |  | wishonia:7 | 1 | `pb-089-food` |
| `charles-mackay` | Charles Mackay in an 1841 frock coat and side-whiskers holding his book; flattened with footprints |  | unrepresentative-democracy:3 | 1 | `pb-036-real-period` |
| `charles-ponzi` | Charles Ponzi, the 1920 swindler: straw boater, cane, pencil moustache, a grin |  | incentive-alignment-bonds:13 | 1 | `pb-108-real-period` |
| `chef` | a chef in a tall toque with a medal and a blowtorch |  | central-banks:27 | 1 | `pb-066-people` |
| `chef-hat` | a tall white chef's toque to sit on the Capitol's dome |  | optimocracy:1 | 1 | `pb-078-wearables` |
| `chimp` | a chimpanzee in the politician's grey double-breasted suit and wide tie |  | incentive-alignment-bonds:2 | 1 | `pb-071-politician` |
| `chocolate-bar` | a bar of dark chocolate in a foil wrapper |  | wishonia:3 | 1 | `pb-089-food` |
| `christians` | a little group of early Christians in plain robes; charred; skeletons |  | central-banks:3 | 1 | `pb-098-period` |
| `claims-clerk-bureaucrat` | new poses of `claims-clerk` as the Bureaucrat: snoring, eyes snapping open, counting with a licked pencil, bowing |  | recruitment-and-propaganda-plan:3 | 1 | `pb-049-cast-poses` |
| `class-photo` | a dusty school photograph of a class of girls at their desks with a cobweb on one corner |  | moronia:3 | 1 | `pb-050-paper` |
| `claw-machine` | a fairground claw machine big enough to lift a man |  | unrepresentative-democracy:3 | 1 | `pb-058-games` |
| `coin-op-cannon` | a cannon with a coin slot and a meter with a needle; drooping, a cannonball dribbling out |  | central-banks:8 | 1 | `pb-059-machines` |
| `coke-bottle` | a Coca-Cola bottle |  | global-referendum:6 | 1 | `pb-090-food` |
| `collection-plate` | a brass church collection plate on a long handle |  | wishonia:14 | 1 | `pb-072-props` |
| `concert-hall` | a round concert hall seen from above with its roof lifted off, tiers of tiny people holding lighters, a stage |  | financial-plan:3 | 1 | `pb-052-places` |
| `constitution-case` | the Constitution on parchment in a glass case on a plinth, the case also empty; the plinth with a card slot, a cash drawer and a row of buttons with one blank spot |  | wishocracy:7 | 1 | `pb-050-paper` |
| `contrarian` | a 1950s greaser in a leather jacket and pompadour with a toothpick, arms crossed |  | recruitment-and-propaganda-plan:13 | 1 | `pb-066-people` |
| `credit-card` | a 1950s charge card held out between two fingers |  | wishocracy:2 | 1 | `pb-050-paper` |
| `crossed-fingers` | a hand with crossed fingers |  | faq:4 | 1 | `pb-047-body` |
| `cushion` | a giant plush cushion with tassels |  | fda-is-unsafe-and-ineffective:8 | 1 | `pb-073-props` |
| `cutaway-head` | a cutaway skull piece that fits any citizen's head, the brain inside like an anatomy plate |  | treaty-feasibility:6 | 1 | `pb-087-body` |
| `david-putrino` | David Putrino of Mount Sinai caricatured in a 1950s suit |  | nih-fails-2-institute-health:1 | 1 | `pb-045-real` |
| `decision-tree` | an oak whose left branch can be sawn off, a saw, a hammock on the right branch, a playground slide |  | fda-is-unsafe-and-ineffective:7 | 1 | `pb-044-nature` |
| `dendreon-building` | a small biotech building with a face, and the same building boarded up |  | fda-is-unsafe-and-ineffective:9 | 1 | `pb-048-buildings` |
| `dentist` | a 1950s dentist with a head mirror and a belt-driven drill, and a dentist's chair with its lamp and spit bowl | `dentist-chair` | recruitment-and-propaganda-plan:4 | 1 | `pb-066-people` |
| `desk-lamp` | an angle-poise desk lamp that hops |  | wishonia:3 | 1 | `pb-060-machines` |
| `detective` | a trench-coat detective, yawning |  | 1-percent-treaty:8 | 1 | `pb-066-people` |
| `dice` | twenty white dice with black pips, one rolled to a single pip |  | gdp-trajectories:1 | 1 | `pb-058-games` |
| `dih-building` | a modest columned building on a shore with a face and a row of outflow valves |  | nonprofit-coalition-strategy:7 | 1 | `pb-054-buildings` |
| `dinosaur` | a T. rex alive, and as a mounted museum skeleton |  | wishonia:12 | 1 | `pb-082-animals` |
| `diocletian` | Emperor Diocletian caricatured: bull neck, laurel wreath, a toga drawn deep crimson (recolour it purple after cutting: purple keys out with the magenta), a carpenter's plane |  | central-banks:3 | 1 | `pb-108-real-period` |
| `directory-board` | a lobby directory board with felt letters and arrows and an empty slot |  | nih-fails-2-institute-health:10 | 1 | `pb-094-paper` |
| `docent` | a museum docent in a uniform and peaked cap with a pointer, and his skeleton on a stool |  | genetic-slavery:9 | 1 | `pb-066-people` |
| `doctor-50s` | `doctor` redrawn in 1950s clothes: white coat, head mirror, stethoscope |  | body-as-repairable-machine:1 | 1 | `pb-049-cast-poses` |
| `dolphin` | dolphins in a pool, one in a fedora and round glasses, flippers up |  | wishonia:3 | 1 | `pb-083-animals` |
| `domino` | a giant domino tile |  | aligning-incentives:9 | 1 | `pb-058-games` |
| `dragon` | a dragon on a hoard of coins, choking, X-eyed |  | aligning-incentives:9 | 1 | `pb-083-animals` |
| `dresser` | a tall Victorian dresser that tips over |  | 1-percent-treaty:4 | 1 | `pb-073-props` |
| `drunk` | a 1950s drunk in a crumpled suit and loosened tie, a bottle in his pocket, swaying, one eye shut; throwing |  | nih-fails-2-institute-health:8 | 1 | `pb-066-people` |
| `dump-truck` | a dump truck that tips |  | 1-percent-treaty:2 | 1 | `pb-109-vehicles` |
| `dynamite-house` | a family house built of dynamite sticks with fuses for a chimney |  | 1-percent-treaty:2 | 1 | `pb-113-weapons` |
| `ecohealth-building` | EcoHealth Alliance as a small office with a face and a leafy logo |  | nih-fails-2-institute-health:9 | 1 | `pb-054-buildings` |
| `egg-carton` | a carton of a dozen eggs |  | central-banks:15 | 1 | `pb-090-food` |
| `elephant` | a pregnant circus elephant walking, giving birth to a baby elephant, squashed to the width of a suitcase; the baby holding a bottle in its trunk |  | health-dividend:2 | 1 | `pb-083-animals` |
| `elvis` | Elvis Presley caricatured: quiff, sideburns, gold suit, signing a photo of himself |  | genetic-slavery:6 | 1 | `pb-103-real` |
| `energy-drink` | a tall energy-drink can with lightning bolts, and a man in a 1950s suit drinking one, rocketing up and coming down charred with a thumbs up |  | health-dividend:4 | 1 | `pb-090-food` |
| `enforcement-van` | the enforcement agency as a 1950s black van with a face, a slot for bills and a telescoping arm that ends in a big net |  | moronia:6 | 1 | `pb-054-buildings` |
| `engine-block` | a small chugging engine |  | wishocracy:2 | 1 | `pb-060-machines` |
| `enzyme` | little molecule repairmen in 1950s work caps: with wrenches, on ropes, splicing tape, on a ladder, with lunch pails, nailing a plank |  | body-as-repairable-machine:2 | 1 | `pb-087-body` |
| `ex-commissioner` | a former SEC commissioner in a 1950s suit sitting very still on a shelf like an ornament |  | legal-framework:6 | 1 | `pb-067-people` |
| `falling-jaw` | cartoon jaws that drop to the floor |  | legal-framework:6 | 1 | `pb-087-body` |
| `fan-bearers` | an Egyptian servant with an ostrich-feather fan |  | wishonia:6 | 1 | `pb-098-period` |
| `farmers-wife` | a farmer's wife in a 1950s apron and headscarf with a carving knife, swinging and stamping |  | body-as-repairable-machine:5 | 1 | `pb-067-people` |
| `fat-cat-frosted` | new pose of `fat-cat`: smeared in green frosting, a fork in his paw |  | central-banks:16 | 1 | `pb-041-fat-cat-lobbyist` |
| `fda-pistol` | new pose of the FDA building: its frieze, columns and door drawn along a pistol's barrel and grip, with its face; smoking, blinking |  | fda-is-unsafe-and-ineffective:2 | 1 | `pb-053-building-poses` |
| `fdic-office` | the FDIC: a small plain brick insurance office with a modest face in its lintel, a green eyeshade, white-gloved arms and a big rubber stamp |  | central-banks:14 | 1 | `pb-054-buildings` |
| `fdr` | Franklin Roosevelt with a cigarette holder at a jaunty angle and pince-nez, at a microphone |  | nonprofit-coalition-strategy:5 | 1 | `pb-103-real` |
| `fed-mouth` | new pose of `fed-crank-up`: the Federal Reserve building blowing hard through its pediment mouth |  | central-banks:16 | 1 | `pb-053-building-poses` |
| `fifa-building` | FIFA as its building: a glass-and-marble headquarters with a face, a football on its dome, a chandelier in every window, a mail slot door; hiccuping |  | health-dividend:4 | 1 | `pb-054-buildings` |
| `fighter-jet` | a fighter jet in loose pieces (wings, tail, canopy) |  | aligning-incentives:4 | 1 | `pb-109-vehicles` |
| `filing-cabinet-fda` | new pose of the FDA building: a tall filing cabinet with its frieze and face and a chute at its base |  | fda-is-unsafe-and-ineffective:12 | 1 | `pb-053-building-poses` |
| `fire-station` | the fire department as its building: a face in its doors, a lit match in one hand and a hose in the other; extra floors that stack on top; on fire |  | moronia:4 | 1 | `pb-054-buildings` |
| `first-aid-tin` | a small first-aid tin with one sticking plaster in it |  | recruitment-and-propaganda-plan:5 | 1 | `pb-073-props` |
| `florida-man` | Florida Man in a loud shirt and shorts with an alligator on a leash |  | 1-percent-treaty:6 | 1 | `pb-067-people` |
| `foot` | YOU's left foot in its sock and shoe, loose; a wooden foot; a sprig of lavender |  | dfda:6 | 1 | `pb-087-body` |
| `football-goal` | a football goal with a net, a 1950s leather football, and a goalkeeper's cap |  | treaty-feasibility:6 | 1 | `pb-073-props` |
| `forklift` | a little 1950s forklift |  | unrepresentative-democracy:5 | 1 | `pb-109-vehicles` |
| `fortune-booth` | a carnival fortune teller's booth with a crystal ball and a turbaned figure |  | fda-is-unsafe-and-ineffective:9 | 1 | `pb-100-places` |
| `fossil` | the `politician` as a skeleton in rock strata |  | aligning-incentives:8 | 1 | `pb-071-politician` |
| `fungus` | a fat toadstool with little arms |  | central-banks:7 | 1 | `pb-090-food` |
| `gala-dress` | a gala dress and a champagne flute |  | faq:9 | 1 | `pb-078-wearables` |
| `galactic-council` | a round marble table floating among the stars with a ring of alien delegates of many shapes in 1950s-tomorrow robes, eyes rolling back in bliss |  | wishonia:16 | 1 | `pb-014-aliens` |
| `galileo` | Galileo caricatured (big beard, cap) with a long brass telescope; his skeleton still looking through it |  | health-dividend:2 | 1 | `pb-108-real-period` |
| `garbage-can` | a dented garbage can |  | roadmap:4 | 1 | `pb-073-props` |
| `gavel` | a judge's gavel and block |  | roadmap:7 | 1 | `pb-073-props` |
| `glass-gearbox` | a glass gearbox with spouts |  | 1-percent-treaty:1 | 1 | `pb-060-machines` |
| `gold-truck` | a 1960s French flatbed truck |  | central-banks:20 | 1 | `pb-109-vehicles` |
| `gold-watch` | a retirement gold watch in a presentation box |  | wishonia:4 | 1 | `pb-074-props` |
| `goldfish` | a goldfish in a bowl in a sweatband doing push-ups |  | treaty-feasibility:12 | 1 | `pb-083-animals` |
| `golfer` | a 1950s golfer in plus-fours and a flat cap, iron raised; and charred |  | recruitment-and-propaganda-plan:7 | 1 | `pb-067-people` |
| `grinning-bottle` | a giant grinning bottle the height of the frame, tipped and pouring, with no cork | `bottle` | central-banks:24 | 1 | `pb-090-food` |
| `guard` | a 1950s museum guard in a peaked cap: bought (dollar-sign eyes), scared, with a medal, reading a newspaper |  | wishocracy:7 | 1 | `pb-067-people` |
| `guinea-pig` | a guinea pig in a tiny lab coat signing with a quill, holding a pill and a bill; a cage of ordinary guinea pigs |  | dih:7 | 1 | `pb-083-animals` |
| `gumball-machine` | a red 1950s gumball machine full of tiny people instead of gumballs |  | global-referendum:4 | 1 | `pb-058-games` |
| `hamburger` | a 1950s diner hamburger |  | nonprofit-coalition-strategy:3 | 1 | `pb-091-food` |
| `hammock-grandpa` | a grandpa asleep in a hammock |  | central-banks:17 | 1 | `pb-067-people` |
| `hat-rack` | a hat rack with six hats as loose pieces (a cowboy hat, an army cap, a tinfoil hat and more) |  | 1-percent-treaty:5 | 1 | `pb-074-props` |
| `head-house` | YOU huge in profile with his head cut away like an anatomy plate: three empty layers and the pipes |  | genetic-slavery:13 | 1 | `pb-087-body` |
| `health-nut` | the `fat-cat` obsessed with health: in a cold-plunge tub, upside down in gravity boots, on a rowing machine, drinking a green smoothie, taking his pulse, with binoculars |  | treaty-feasibility:10 | 1 | `pb-041-fat-cat-lobbyist` |
| `heart-monitor` | a 1950s hospital pulse monitor on a cart, and a stethoscope as a piece for the fat cat's hands |  | financial-plan:1 | 1 | `pb-060-machines` |
| `henry-miller` | Dr. Henry I. Miller caricatured holding an insulin vial |  | fda-is-unsafe-and-ineffective:7 | 1 | `pb-103-real` |
| `henry-poor` | Henry Varnum Poor at a Victorian desk with a quill, and two little railroad bond certificates |  | incentive-alignment-bonds:14 | 1 | `pb-108-real-period` |
| `high-striker` | a carnival test-your-strength tower with a sliding puck, a lever, a brass bell on top and a big wooden mallet |  | incentive-alignment-bonds:5 | 1 | `pb-060-machines` |
| `homework-book` | a homework book as thick as a wardrobe, its pages battle diagrams |  | legal-framework:4 | 1 | `pb-094-paper` |
| `howey` | W. J. Howey's grove salesman in a white suit and panama hat |  | legal-framework:4 | 1 | `pb-108-real-period` |
| `hydra` | a tiny freshwater polyp waving all its tentacles, and a little safe with its door cracked open |  | body-as-repairable-machine:5 | 1 | `pb-084-animals` |
| `iceberg` | an iceberg with its small tip above a waterline and its bulk below |  | treaty-feasibility:11 | 1 | `pb-044-nature` |
| `id-badge` | a government ID badge on a clip |  | unrepresentative-democracy:6 | 1 | `pb-094-paper` |
| `insurgent` | an insurgent in a balaclava |  | 1-percent-treaty:4 | 1 | `pb-068-people` |
| `james-buchanan` | economist James Buchanan caricatured in glasses |  | unrepresentative-democracy:6 | 1 | `pb-103-real` |
| `jellyfish` | a jellyfish holding up a homework page |  | body-as-repairable-machine:5 | 1 | `pb-084-animals` |
| `jetpack-man` | a 1950s man in goggles with a rocket pack, flying, sputtering, charred |  | wishocracy:3 | 1 | `pb-068-people` |
| `jfk` | John F. Kennedy caricatured at a podium |  | faq:6 | 1 | `pb-103-real` |
| `jimmy-hoffa` | Jimmy Hoffa caricatured in his 1970s suit, buried to the chest, waving |  | fda-is-unsafe-and-ineffective:11 | 1 | `pb-104-real` |
| `joan-of-arc` | Joan of Arc in armour, and charred |  | legal-framework:6 | 1 | `pb-112-real-period` |
| `jody-williams` | Jody Williams caricatured: short grey hair, glasses, a cardigan, at a rotary telephone with a long cord; steaming |  | treaty-feasibility:1 | 1 | `pb-104-real` |
| `john-hancock` | John Hancock with a quill signing the Declaration of Independence |  | global-referendum:4 | 1 | `pb-112-real-period` |
| `jonas-salk` | Jonas Salk caricatured in a 1950s lab coat with a vial and a certificate that tears |  | nih-fails-2-institute-health:11 | 1 | `pb-104-real` |
| `jose-figueres` | José Figueres (Costa Rica, 1948, moustache and suit) with a sledgehammer |  | faq:7 | 1 | `pb-104-real` |
| `kefauver-harris` | Senator Estes Kefauver in his coonskin cap and Representative Oren Harris in a bow tie, carrying something between them |  | fda-is-unsafe-and-ineffective:3 | 1 | `pb-104-real` |
| `ken-burns` | Ken Burns caricatured: bowl haircut, open collar |  | faq:8 | 1 | `pb-105-real` |
| `kindergarten-class` | a 1950s kindergarten class photo, about 25 children on two benches with their teacher |  | dfda:2 | 1 | `pb-094-paper` |
| `kitchen` | a gleaming 1950s kitchen, chrome and pastel, with a dining table set for one |  | nih-fails-2-institute-health:6 | 1 | `pb-074-props` |
| `kitchen-sink` | a 1950s sink piled with dishes, each with a grinning germ painted on it |  | dih:2 | 1 | `pb-074-props` |
| `knitting-circle` | three 1950s ladies in a knitting circle with a blank hand-lettered placard |  | treaty-feasibility:3 | 1 | `pb-068-people` |
| `kremlin` | the Kremlin's Senate building with onion domes and a star on top, window eyes, a door mouth with one big keyhole |  | optimocracy:6 | 1 | `pb-055-buildings` |
| `lab-coat-sleeve` | a white lab-coat sleeve and cuff that slides onto a hand |  | wishonia:5 | 1 | `pb-078-wearables` |
| `lab-goggles` | a pair of lab goggles that fit a robot's head |  | peace-dividend:6 | 1 | `pb-078-wearables` |
| `labrador` | a labrador barking with its mouth huge, and at a desk in reading glasses with a pencil in its mouth, chewing a form, wagging |  | genetic-slavery:6 | 1 | `pb-084-animals` |
| `landlord` | a landlord in a cardigan with a rent book, filling a doorway |  | central-banks:11 | 1 | `pb-068-people` |
| `lawrence-tabak` | Lawrence Tabak caricatured at a witness table with a microphone |  | nih-fails-2-institute-health:9 | 1 | `pb-105-real` |
| `legal-robot` | robot pieces: a blank frame, a brain under a glass dome, a butter-knife sword arm, an engine torso with a bond slot, a cuckoo-clock heart with a chocolate-bar door |  | roadmap:5 | 1 | `pb-060-machines` |
| `lehman-brothers` | a narrow office building with identical moustached brothers at every window, throwing green bills, then pointing at each other |  | central-banks:9 | 1 | `pb-055-buildings` |
| `lobbyist-xray` | the `lobbyist` as an x-ray: a wad of bills for a brain, a coin purse for a heart, a piggy bank for a stomach |  | aligning-incentives:2 | 1 | `pb-041-fat-cat-lobbyist` |
| `lockheed-ceo` | Lockheed Martin's chief executive caricatured in a 1950s suit |  | 1-percent-treaty:6 | 1 | `pb-105-real` |
| `lottery-ticket` | a scratch-off ticket with a silver panel that peels |  | aligning-incentives:6 | 1 | `pb-094-paper` |
| `madison` | James Madison caricatured: small, a powdered wig, eyebrows that lift right off his face, a quill |  | legal-framework:5 | 1 | `pb-112-real-period` |
| `magic-mushroom` | a little psychedelic mushroom that hops; in a flower crown, dancing |  | genetic-slavery:14 | 1 | `pb-091-food` |
| `magnet` | a giant horseshoe magnet |  | genetic-slavery:14 | 1 | `pb-061-machines` |
| `mailbox` | a 1950s kerbside mailbox on a post |  | nih-fails-2-institute-health:9 | 1 | `pb-074-props` |
| `maintenance-kit` | a maintenance worker's cap, coveralls bib, tool belt and crowbar sized for a building |  | central-banks:20 | 1 | `pb-078-wearables` |
| `mammoth` | a woolly mammoth plodding through snow |  | central-banks:33 | 1 | `pb-084-animals` |
| `martin-shkreli` | Martin Shkreli caricatured, smirking, and the same on a poster |  | aligning-incentives:6 | 1 | `pb-105-real` |
| `matterhorn` | the Matterhorn |  | gdp-trajectories:8 | 1 | `pb-111-nature` |
| `meat-factory` | a meat-packing plant as a brick building with a grinning loading door, a conveyor going in and a smokestack |  | genetic-slavery:8 | 1 | `pb-055-buildings` |
| `medicine-wagon` | a painted 1900 patent-medicine wagon with bottles of tonic and the salesman in a striped coat and boater on its tailboard; the wagon flattened |  | dfda:2 | 1 | `pb-098-period` |
| `menu` | a leather-bound restaurant menu, open and closed, with a bite out of it |  | nih-fails-2-institute-health:7 | 1 | `pb-095-paper` |
| `minutemen` | a row of Minutemen with muskets |  | global-referendum:4 | 1 | `pb-099-period` |
| `mixing-bowl` | a 1950s mixing bowl as big as a bathtub |  | roadmap:1 | 1 | `pb-074-props` |
| `modem` | a 1990s dial-up modem with a telephone handset in its cradle |  | wishonia:4 | 1 | `pb-061-machines` |
| `mole-rat` | a naked mole rat climbing, at a chalkboard with chalk, in a bathtub with a rubber duck |  | body-as-repairable-machine:5 | 1 | `pb-084-animals` |
| `money-cat` | a cat made of green banknotes with plain seals that walks and sits |  | 1-percent-treaty:3 | 1 | `pb-085-animals` |
| `money-dial` | a brass wall dial with a big lever |  | central-banks:2 | 1 | `pb-061-machines` |
| `monk-astronomer` | a monk astronomer with a quadrant |  | roadmap:1 | 1 | `pb-099-period` |
| `monkey` | a lab monkey in a little gown with a suitcase and a stopwatch |  | nih-fails-2-institute-health:6 | 1 | `pb-085-animals` |
| `moon` | the Moon with a face |  | global-referendum:6 | 1 | `pb-111-nature` |
| `mop` | a mop |  | central-banks:24 | 1 | `pb-075-props` |
| `morgue-drawers` | a wall of steel morgue drawers; three that slide out with a sheeted body and a toe tag |  | fda-is-unsafe-and-ineffective:5 | 1 | `pb-075-props` |
| `moronian` | a Moronian (big domed head, antennae, three-fingered hands) in 1950s clothes in three builds (a suit, a dress, a cardigan), sitting, hands up to hold a prop; its skeleton | `moronian-skeleton` | conclusion:1 | 1 | `pb-014-aliens` |
| `mountie-hat` | a little red-coat Mountie hat that sits on a building's roof |  | central-banks:14 | 1 | `pb-079-wearables` |
| `mouse` | an old lab mouse with a cane, spectacles and a white beard; young on a wheel; three blind mice in dark glasses with white canes whose glasses pop off |  | body-as-repairable-machine:5 | 1 | `pb-085-animals` |
| `muzzle` | a leather dog muzzle with a buckle that loosens notch by notch |  | nonprofit-coalition-strategy:3 | 1 | `pb-079-wearables` |
| `napkin` | a paper napkin with a pencil doodle of a bar and a coffee ring |  | peace-dividend:5 | 1 | `pb-095-paper` |
| `nation-mobile` | a giant hanging brass mobile whose arms carry pans with little flag poles |  | 1-percent-treaty:1 | 1 | `pb-061-machines` |
| `nobel-skeleton` | `nobel`'s skeleton with his side whiskers, sitting up out of a grave; a jaw that drops off |  | central-banks:26 | 1 | `pb-043-cast-period` |
| `nursery-window` | a hospital nursery window with rows of bassinets |  | legal-framework:2 | 1 | `pb-100-places` |
| `obama` | Barack Obama caricatured (ears, grin) in a dark suit |  | nih-fails-2-institute-health:9 | 1 | `pb-105-real` |
| `ohio-bus` | a 1950s city bus with a blank destination blind and a door folding open |  | wishonia:15 | 1 | `pb-110-vehicles` |
| `orange-grove` | rows of orange trees and a porch, and one loose orange | `orange` | legal-framework:4 | 1 | `pb-100-places` |
| `pacemaker` | a 1950s pacemaker in a little box |  | roadmap:2 | 1 | `pb-061-machines` |
| `palantir` | a dark stone tower with a huge glowing crystal ball on top like an eye, with a lid that winks; its walls can turn to glass |  | wishonia:9 | 1 | `pb-055-buildings` |
| `pangloss` | Dr Pangloss in a powdered wig and 18th-century tutor's coat, arms wide; flattened under a beam, thumb up |  | recruitment-and-propaganda-plan:5 | 1 | `pb-112-real-period` |
| `paper-snake` | a long snake made of stacked papers and journals wearing pince-nez, mouth open; biting its tail; holding a pencil |  | nih-fails-2-institute-health:3 | 1 | `pb-095-paper` |
| `parade-float` | a parade float on a flatbed |  | fda-is-unsafe-and-ineffective:8 | 1 | `pb-110-vehicles` |
| `particle-accelerator` | a huge brass ring of magnets on a field with a little door in it and a tiny speck popping out |  | financial-plan:5 | 1 | `pb-061-machines` |
| `party-hat` | a paper party hat and a tiny flag |  | recruitment-and-propaganda-plan:1 | 1 | `pb-079-wearables` |
| `patent` | a patent certificate with a ribbon seal |  | fda-is-unsafe-and-ineffective:4 | 1 | `pb-095-paper` |
| `pcori-building` | P.C.O.R.I. as a small new office building with a face, and a leather muzzle that fits it |  | nih-fails-2-institute-health:6 | 1 | `pb-055-buildings` |
| `pelosi` | Nancy Pelosi caricatured with a gavel |  | unrepresentative-democracy:5 | 1 | `pb-106-real` |
| `people-snowball` | a snowball made of people, arms and hats sticking out, in five sizes |  | global-referendum:5 | 1 | `pb-093-games` |
| `pepsi-button` | a 1950s Pepsi-Cola bottle-cap push-button on a stand |  | financial-plan:3 | 1 | `pb-093-games` |
| `permit-office` | a squat stone permit office with a face, one window, a long arm with a rubber stamp and a pigeonhole of blank forms; and charred |  | legal-framework:1 | 1 | `pb-055-buildings` |
| `pet-shop-window` | a pet shop window with a striped awning and a little bed of straw |  | unrepresentative-democracy:4 | 1 | `pb-100-places` |
| `pharma-coat` | a trench coat that turns inside out into a lab coat |  | aligning-incentives:6 | 1 | `pb-079-wearables` |
| `phone-booth` | a 1950s glass phone booth |  | wishocracy:5 | 1 | `pb-100-places` |
| `phone-case` | a heap of novelty phone cases (cat ears, a hamburger, a banana, a rubber duck) |  | treaty-feasibility:7 | 1 | `pb-075-props` |
| `photocopier` | a 1950s office photocopier with a lid |  | gdp-trajectories:2 | 1 | `pb-062-machines` |
| `pigeon-skeleton` | the carrier `pigeon` as a little skeleton |  | fda-is-unsafe-and-ineffective:9 | 1 | `pb-043-cast-period` |
| `piggy-bank` | a china piggy bank, whole and smashed |  | central-banks:26 | 1 | `pb-075-props` |
| `pigtails` | a pair of pigtails with bows, alone |  | moronia:13 | 1 | `pb-079-wearables` |
| `pill-box` | one pill packet drawn once to recolour, and a single white pill that hops |  | untapped-therapeutic-frontier:2 | 1 | `pb-075-props` |
| `pinky-hands` | two giant hands with hooked pinkies, and the same hands with no pinkies holding fountain pens |  | 1-percent-treaty:3 | 1 | `pb-088-body` |
| `pipe-of-middlemen` | a long riveted pipe with three hatches, a pair of hands with nail scissors in each (gloves, a committee man's cuffs, pinstripe sleeves); it can fall and lie like a sardine tin |  | wishocracy:1 | 1 | `pb-062-machines` |
| `pit` | a round hole in the ground with dirt edges, seen from the side |  | dih:4 | 1 | `pb-075-props` |
| `planarian` | a cross-eyed flatworm, whole, cut in two, and two little worms in baby bonnets |  | body-as-repairable-machine:5 | 1 | `pb-085-animals` |
| `plumber` | a 1950s plumber in overalls and a cap with a big wrench and a toolbox |  | dih:6 | 1 | `pb-068-people` |
| `pneumatic-tube` | a brass pneumatic tube with a canister |  | unrepresentative-democracy:2 | 1 | `pb-062-machines` |
| `politician-horse` | the `politician`'s head on a racehorse in silks, facing backward and chewing, and at a gallop |  | incentive-alignment-bonds:9 | 1 | `pb-071-politician` |
| `politician-nose` | a long wooden nose piece for the `politician` |  | unrepresentative-democracy:5 | 1 | `pb-071-politician` |
| `portrait-photo` | a framed Victorian portrait photograph of a stern couple on stick legs |  | global-referendum:3 | 1 | `pb-095-paper` |
| `postman-cap` | a postman's cap and mailbag for YOU |  | roadmap:4 | 1 | `pb-079-wearables` |
| `potato-salad` | a big bowl of potato salad under cling film with a serving spoon |  | wishonia:16 | 1 | `pb-091-food` |
| `preacher` | a street preacher on a soapbox with a book |  | global-referendum:5 | 1 | `pb-068-people` |
| `pregnant-woman` | a 1950s pregnant woman in a polka-dot maternity smock |  | fda-is-unsafe-and-ineffective:8 | 1 | `pb-069-people` |
| `pricing-gun` | a shop's price-tag gun |  | health-dividend:3 | 1 | `pb-062-machines` |
| `pulley` | a pulley on a gallows frame with two ropes |  | legal-framework:2 | 1 | `pb-062-machines` |
| `punch-card-heart` | a cutaway of the fat cat's chest: a heart with a brass punch-card reader bolted on and a stack of punch cards; jammed and smoking |  | recruitment-and-propaganda-plan:2 | 1 | `pb-062-machines` |
| `punch-clock` | a 1950s time clock on a post with a rack of cards |  | financial-plan:2 | 1 | `pb-063-machines` |
| `racehorse` | a racehorse with a jockey |  | unrepresentative-democracy:4 | 1 | `pb-085-animals` |
| `radio` | a 1950s portable radio with a dial; on fire |  | body-as-repairable-machine:4 | 1 | `pb-063-machines` |
| `rails` | railroad track in straight, curved and switch pieces, and a signal post |  | dfda:8 | 1 | `pb-063-machines` |
| `ranking-ladder` | a tall ladder whose rungs are cards |  | dih:5 | 1 | `pb-076-props` |
| `ransom-note` | a cream sheet for a ransom note |  | untapped-therapeutic-frontier:7 | 1 | `pb-096-paper` |
| `rating-agency` | a little 1950s office building as a character with a rubber stamp in one white glove |  | optimocracy:6 | 1 | `pb-056-buildings` |
| `recipe-box` | a tin recipe box and its cards (one blank, a stack with a round scorch on each) |  | central-banks:5 | 1 | `pb-096-paper` |
| `recovery-sign` | a blank sign on two posts: new, rotted and snapped |  | gdp-trajectories:3 | 1 | `pb-096-paper` |
| `reflex-hammer` | a doctor's rubber reflex hammer |  | financial-plan:5 | 1 | `pb-063-machines` |
| `regulators` | four privacy inspectors in 1950s dress, each with a ruler and a stamp: a Brussels official with a ring of stars on his lapel, a Californian in sunglasses, a Chicago man in a fedora, a crossing guard |  | global-referendum:3 | 1 | `pb-069-people` |
| `rick-doblin` | Rick Doblin caricatured: beard, big grin, shirtsleeves |  | fda-is-unsafe-and-ineffective:10 | 1 | `pb-106-real` |
| `robot-dog` | Boston Dynamics' yellow four-legged robot dog: walking, propping someone up, dancing, head turned to stare |  | wishonia:9 | 1 | `pb-086-animals` |
| `rocking-chair` | a rocking chair with knitting needles and a long knitted scarf |  | nonprofit-coalition-strategy:5 | 1 | `pb-076-props` |
| `roman-temple` | a Roman temple whose columns are stacks of silver coins; split; fallen |  | central-banks:3 | 1 | `pb-101-places` |
| `rose` | a single long-stemmed rose with a little card, fresh and wilted |  | nih-fails-2-institute-health:7 | 1 | `pb-091-food` |
| `saddle-shoes` | saddle shoes as pieces for a leader's feet |  | treaty-feasibility:5 | 1 | `pb-080-wearables` |
| `safety-net` | a circus net held taut by four arms, mostly hole |  | fda-is-unsafe-and-ineffective:7 | 1 | `pb-076-props` |
| `sarah` | a tired 1950s woman in her forties, cardigan over a shirtwaist dress, handbag; seated, standing, holding a phone; later brighter |  | dih:7 | 1 | `pb-069-people` |
| `schoolgirl` | a 1950s schoolgirl in plaits with a slate and chalk |  | treaty-feasibility:11 | 1 | `pb-069-people` |
| `scientist-lagos-solder` | new pose of `scientist-lagos`: a kid in a Lagos garage with a soldering iron and a laptop | `lagos-kid` | wishocracy:6 | 1 | `pb-049-cast-poses` |
| `scientist-vending` | a 1950s vending machine with the scientist's head and bun on top, a glass front of light bulbs, a form slot, a coin slot and a delivery tray |  | wishonia:11 | 1 | `pb-063-machines` |
| `seesaw` | a plank seesaw on a trestle |  | nonprofit-coalition-strategy:4 | 1 | `pb-076-props` |
| `sheep` | a woolly sheep that jumps, with a blank tag on a string round its neck |  | global-referendum:1 | 1 | `pb-086-animals` |
| `shells` | three walnut shells and a pea |  | central-banks:28 | 1 | `pb-093-games` |
| `shirt` | a folded dress shirt, stackable |  | 1-percent-treaty:3 | 1 | `pb-076-props` |
| `shoe-box` | a shoe box, stackable |  | untapped-therapeutic-frontier:4 | 1 | `pb-076-props` |
| `shooting-gallery` | a shooting-gallery booth with a rail, a gold-bullet rifle and a cork gun |  | aligning-incentives:7 | 1 | `pb-093-games` |
| `shovel` | a shovel |  | untapped-therapeutic-frontier:1 | 1 | `pb-077-props` |
| `shredder` | a giant office paper shredder with a slot on top and a little office box built onto its side |  | wishonia:7 | 1 | `pb-063-machines` |
| `shrew` | a small furry shrew, a mother with a litter, at a fancy control panel with dials; pulling a chain; charred |  | genetic-slavery:2 | 1 | `pb-086-animals` |
| `side-effect` | little grinning gremlins of three kinds carrying suitcases |  | fda-is-unsafe-and-ineffective:9 | 1 | `pb-088-body` |
| `slide-rule` | a giant slide rule |  | faq:4 | 1 | `pb-064-machines` |
| `smoke-pharma` | a building half cigarette factory (cigarette chimneys) and half pharmacy, one face across both halves, in a trench coat and fedora that fall off |  | legal-framework:4 | 1 | `pb-056-buildings` |
| `smoker` | a 1950s man in a cloud of cigarette smoke, coughing |  | central-banks:5 | 1 | `pb-069-people` |
| `sneaker` | a Nike running shoe with its swoosh on little legs |  | global-referendum:4 | 1 | `pb-080-wearables` |
| `solar-panel` | a solar panel on a little stand |  | nonprofit-coalition-strategy:3 | 1 | `pb-064-machines` |
| `soldier-blue-grey` | a Civil War soldier half in Union blue and half in Confederate grey, punching himself; knocked down |  | central-banks:8 | 1 | `pb-099-period` |
| `sorting-rack` | a wooden pigeonhole rack with seven slots, a brass pneumatic chute and a letter slot |  | recruitment-and-propaganda-plan:13 | 1 | `pb-064-machines` |
| `space-capsule` | a 1950s tourist space capsule with a porthole |  | aligning-incentives:9 | 1 | `pb-110-vehicles` |
| `spaghetti` | a plate of spaghetti and meatballs, and loose noodles |  | global-referendum:2 | 1 | `pb-091-food` |
| `spinning-plates` | four china plates spinning on poles, wobbling and steady |  | treaty-feasibility:9 | 1 | `pb-093-games` |
| `spirit-level` | a brass spirit level whose bubble is a little skull |  | unrepresentative-democracy:9 | 1 | `pb-064-machines` |
| `stake` | a stake on a pile of sticks |  | legal-framework:6 | 1 | `pb-113-weapons` |
| `stamp-head` | the `politician`'s head as a rubber stamp on a wooden handle |  | unrepresentative-democracy:5 | 1 | `pb-071-politician` |
| `steering-wheel` | a ship's steering wheel on a post |  | moronia:9 | 1 | `pb-077-props` |
| `stone-block` | one huge stone block, and as bricks |  | wishocracy:6 | 1 | `pb-077-props` |
| `stone-steps` | five wide stone steps |  | faq:1 | 1 | `pb-101-places` |
| `stork` | a delivery stork with a bundle sling, flying |  | central-banks:25 | 1 | `pb-086-animals` |
| `storybook` | a big children's storybook with a turning page, and a nightcap |  | central-banks:12 | 1 | `pb-096-paper` |
| `stove` | a 1950s enamel kitchen range |  | wishonia:3 | 1 | `pb-077-props` |
| `straw` | a long bendy drinking straw |  | central-banks:17 | 1 | `pb-077-props` |
| `students-1997` | a group photo of 36 college students in 1997 clothes (flannel, frosted tips, a backwards cap) |  | dfda:6 | 1 | `pb-096-paper` |
| `sugar-cube` | a sugar cube with a blank paper label |  | genetic-slavery:9 | 1 | `pb-092-food` |
| `sweatband` | a sweatband for the globe |  | treaty-feasibility:4 | 1 | `pb-080-wearables` |
| `swiss-chocolatier` | a 1950s Swiss chocolatier in a white apron stirring a copper pot of chocolate |  | faq:7 | 1 | `pb-069-people` |
| `swiss-man` | a cheerful Swiss gentleman in a loden coat and an alpine hat with a feather, a walking stick and a wheel of cheese; older, white-haired and still walking |  | optimocracy:2 | 1 | `pb-070-people` |
| `syringe` | a big glass syringe |  | body-as-repairable-machine:4 | 1 | `pb-064-machines` |
| `t-cell` | round white T-cell blobs in 1950s pinstripe suits and fedoras with tommy guns, lounging and playing cards, then hunting; welding masks and a torch |  | body-as-repairable-machine:4 | 1 | `pb-088-body` |
| `tabarrok` | economist Alex Tabarrok caricatured in a 1950s suit with chalk |  | recruitment-and-propaganda-plan:10 | 1 | `pb-106-real` |
| `tamil-tiger` | a Tamil Tiger fighter in tiger-stripe fatigues with a vest and a book |  | 1-percent-treaty:4 | 1 | `pb-070-people` |
| `tammy-baldwin` | Senator Tammy Baldwin caricatured at a microphone |  | nih-fails-2-institute-health:6 | 1 | `pb-106-real` |
| `taxi-meter` | a taxi meter that sits on a lawyer's head |  | legal-framework:6 | 1 | `pb-064-machines` |
| `teddy-roosevelt` | Theodore Roosevelt caricatured (teeth, pince-nez, Rough Rider hat) on horseback, sliding over its neck |  | central-banks:8 | 1 | `pb-106-real` |
| `temple` | a Greek temple with columns and a pediment |  | aligning-incentives:1 | 1 | `pb-101-places` |
| `test-kit` | a COVID test kit box with germs crawling out of it |  | fda-is-unsafe-and-ineffective:12 | 1 | `pb-065-machines` |
| `theater-stage` | a theatre proscenium with curtains, footlights and an arch |  | fda-is-unsafe-and-ineffective:8 | 1 | `pb-101-places` |
| `third-nipple` | a little shirt-front with three nipples, the third a working light switch |  | dfda:5 | 1 | `pb-088-body` |
| `three-supers-plaque` | a chrome-and-enamel 1950s advertising board with three round medallion slots and three medallions |  | wishonia:2 | 1 | `pb-065-machines` |
| `tick` | a giant tick the size of a dog with the Fed building's smug pediment face on its back |  | central-banks:5 | 1 | `pb-086-animals` |
| `tinfoil-man` | a man in a tinfoil hat with an antenna on top |  | roadmap:1 | 1 | `pb-070-people` |
| `toolbox` | a toolbox with two drawers |  | 1-percent-treaty:3 | 1 | `pb-077-props` |
| `toupee` | a toupee |  | roadmap:3 | 1 | `pb-080-wearables` |
| `trampoline` | a big round trampoline with kids bouncing |  | wishonia:4 | 1 | `pb-102-props` |
| `treasure-chest` | a pirate chest shut and open with gold, and plain shut chests |  | untapped-therapeutic-frontier:1 | 1 | `pb-102-props` |
| `tricorn` | a tricorn hat for the Earth |  | roadmap:4 | 1 | `pb-080-wearables` |
| `trireme` | a Greek warship with oars, and sinking |  | wishocracy:4 | 1 | `pb-110-vehicles` |
| `trophy-wall` | a wall of gilt frames holding triumphs (a vaccine vial, a moon rocket, a smiling surgeon), polished |  | dih:4 | 1 | `pb-097-paper` |
| `trump-sign` | Donald Trump full length matching the existing `trump`, a pen in a comically small hand, holding up a scroll |  | conclusion:1 | 1 | `pb-049-cast-poses` |
| `trumpet-nose` | a brass trumpet bell as a nose piece |  | wishonia:2 | 1 | `pb-080-wearables` |
| `tumor` | a tumor with its own blood vessels |  | unrepresentative-democracy:8 | 1 | `pb-088-body` |
| `turkey` | a roast turkey with a detachable drumstick |  | global-referendum:4 | 1 | `pb-092-food` |
| `tv-camera` | a 1950s TV camera on a tripod with a red light |  | legal-framework:6 | 1 | `pb-065-machines` |
| `uncle-sam-referee` | new pose of `uncle-sam`: a referee's striped shirt over his coat, a whistle and a football helmet, holding a football |  | legal-framework:3 | 1 | `pb-049-cast-poses` |
| `universe-eye` | a huge eye in a nebula with a lid and a raised eyebrow |  | wishonia:16 | 1 | `pb-111-nature` |
| `vacuum-cleaner` | a 1950s upright vacuum cleaner with a fat cloth bag |  | dih:9 | 1 | `pb-065-machines` |
| `vampire` | a vampire in a 1950s suit and cape |  | aligning-incentives:1 | 1 | `pb-070-people` |
| `vampire-fangs` | fangs and a high cape collar as pieces for the `politician` |  | treaty-feasibility:3 | 1 | `pb-071-politician` |
| `vending-machine` | a 1950s snack vending machine |  | central-banks:32 | 1 | `pb-065-machines` |
| `veteran` | 1950s veterans in service jackets, each with a little storm cloud over his head that rains; standing up, the cloud gone |  | fda-is-unsafe-and-ineffective:10 | 1 | `pb-070-people` |
| `victorian-doctors` | three Victorian surgeons in blood-smeared frock coats, laughing and pointing, then hiding their hands behind their backs |  | incentive-alignment-bonds:1 | 1 | `pb-099-period` |
| `victory-corp` | a small brick railway station house with a clock face for a face, a ticket-window mouth and white-gloved hands on switch levers |  | financial-plan:4 | 1 | `pb-056-buildings` |
| `vietnam-poster` | a 1950s bond poster: a crop duster spraying a cloud over a rice farmer and his two children, who cough and glare |  | central-banks:9 | 1 | `pb-097-paper` |
| `vine` | a creeping vine whose leaves are war bills, in lengths that grow over a building |  | moronia:4 | 1 | `pb-111-nature` |
| `voc-ship` | a 1600s Dutch East India Company galleon with every cannon port smoking |  | central-banks:23 | 1 | `pb-110-vehicles` |
| `volcker` | Paul Volcker: six foot seven, bald, glasses, a cigar |  | central-banks:30 | 1 | `pb-107-real` |
| `von-neumann` | John von Neumann: round face, receding hair, three-piece suit, chalk in hand |  | nonprofit-coalition-strategy:4 | 1 | `pb-107-real` |
| `voting-booth` | a 1950s voting booth whose curtain stops two feet off the ground |  | global-referendum:2 | 1 | `pb-101-places` |
| `waiting-chairs` | a row of waiting-room chairs with a side table of magazines |  | health-dividend:4 | 1 | `pb-102-props` |
| `walter-freeman` | Dr. Walter Freeman caricatured, beaming, with an ice pick and a mallet (the mallet also enormous) |  | genetic-slavery:14 | 1 | `pb-107-real` |
| `warehouse` | a long corrugated detention warehouse with a face in its loading door, rows of beds inside, a gauge on its wall |  | moronia:6 | 1 | `pb-056-buildings` |
| `warren-buffett` | Warren Buffett caricatured: big glasses, bushy eyebrows, a Cherry Coke |  | incentive-alignment-bonds:11 | 1 | `pb-107-real` |
| `water-thief` | a man in a tall hat with a yoke of two buckets, and a toll gate with a coin box |  | central-banks:15 | 1 | `pb-099-period` |
| `weatherman` | a 1950s TV weatherman with a pointer and a grin |  | genetic-slavery:12 | 1 | `pb-070-people` |
| `wedding-topper` | two grooms on a wedding cake |  | wishocracy:4 | 1 | `pb-092-food` |
| `whistle-flag` | a referee's whistle and a penalty flag |  | fda-is-unsafe-and-ineffective:10 | 1 | `pb-102-props` |
| `white-house` | the White House as a building with a face |  | central-banks:9 | 1 | `pb-056-buildings` |
| `white-paper` | a thick stapled white paper, flat and folded into a wedge |  | incentive-alignment-bonds:1 | 1 | `pb-097-paper` |
| `wine-bottle` | a wine bottle and two glasses |  | faq:8 | 1 | `pb-092-food` |
| `wishbone` | a wishbone, whole and snapped |  | genetic-slavery:15 | 1 | `pb-092-food` |
| `wishonian-dancer` | a Wishonian in a leotard doing interpretive dance, and a frowning Wishonian crowd |  | incentive-alignment-bonds:2 | 1 | `pb-039-host` |
| `wishonian-kids` | three small round big-eyed Wishonian children sitting cross-legged: laughing, hand up, solemn | `alien-kids` | peace-dividend:1 | 1 | `pb-039-host` |
| `wiv-building` | the Wuhan Institute of Virology as a modern lab block with a face and a biohazard sign |  | nih-fails-2-institute-health:9 | 1 | `pb-056-buildings` |
| `worldcoin-orb` | Worldcoin's chrome orb on a stand with a lens that scans an eye |  | global-referendum:3 | 1 | `pb-065-machines` |
| `wright-brothers` | the Wright brothers in bicycle-shop aprons with the 1903 Flyer |  | faq:6 | 1 | `pb-107-real` |
| `wrong-way-sign` | a rectangular road sign on a post, blank |  | faq:7 | 1 | `pb-097-paper` |
| `year-one-photo` | a snapshot of a planet in its year one, everything on fire, one little alien skeleton waving |  | dih:10 | 1 | `pb-097-paper` |
| `yo-yo` | a yo-yo |  | 1-percent-treaty:9 | 1 | `pb-102-props` |
| `you-aprons` | new pose of `you`: a diner apron over a gas-station jacket over his suit, pouring coffee and pumping gas at once; running |  | central-banks:11 | 1 | `pb-081-you` |
| `you-balloon` | new pose of `you`: swollen round like a balloon |  | genetic-slavery:9 | 1 | `pb-081-you` |
| `you-blind` | pieces for `you`: dark lenses for his round glasses and a white cane |  | body-as-repairable-machine:4 | 1 | `pb-081-you` |
| `you-eyeballs` | pieces for `you`: his eyeballs on springs, popping out |  | genetic-slavery:10 | 1 | `pb-081-you` |
| `you-old` | new states of `you`: greying, with a paunch, stooped with a cane |  | body-as-repairable-machine:5 | 1 | `pb-081-you` |
| `you-taxi` | pieces for `you`: a fare meter that flips up on his chest and a little door in his side |  | genetic-slavery:1 | 1 | `pb-081-you` |

## Sheets

Ordered by total uses (the counts of a sheet's pieces added up), most first. The first 20 are batch 1.

### 1. `pb-001-buildings` (81 uses) · batch 1

Pieces: `pharma-building`, `nih-building`, `university`, `sec-building`, `insurance-awake`, `houses-of-worship`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) the drug industry as its building: a white marble headquarters with pill-bottle chimneys, window eyes, a smug pediment face and white-gloved stick arms; (2) the N.I.H. as its building: a columned marble palace with a face in its pediment (pince-nez, a superior mouth), stick arms in white gloves; (3) a Gothic university hall with ivy, a bell tower and a face in its clock tower, white-gloved stick arms holding a rubber stamp or a long soup ladle; (4) the SEC as its building: a 1930s granite federal front whose columns are teeth, two windows for eyes, a monocle in one, reading ticker tape, a service window with a long jointed arm holding a rubber stamp; (5) the insurance company as its building: a granite tower with a clock-face face and a big umbrella on its roof, a long stamping arm and a toll-gate pole for an arm; (6) a little white church, a synagogue, a temple and a mosque with a minaret, each a building with a face and a ringing bell. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 2. `pb-002-machines` (51 uses) · batch 1

Pieces: `funding-pipe`, `ratchet`, `brass-pipe`, `ledger-computer`, `switchboard`, `giant-microscope`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a long riveted glass pipe on trestles with bills flowing in it, a valve wheel, a brass gauge and a meter; (2) a giant cast-iron ratchet wheel with its pawl, a hub dial, a lever and a crank, and the big screw jack it drives; (3) a long brass pipe in sections with elbows, a hopper mouth, a gauge and a bell, a swinging outlet and one dusty lever; (4) a 1950s cabinet computer with a screen showing a little ledger page; (5) a 1950s telephone switchboard the size of a wall, rows of jacks, cords on weights that plug themselves in, a ticker tape on top; (6) a brass microscope, small and as tall as a man. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 3. `pb-003-animals` (38 uses) · batch 1

Pieces: `fish`, `starving-dog`, `lizard`, `pet-dog`, `sabertooth`, `pig`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 6 separate cut-outs, each large and well apart: (1) a small river fish, a big wet fish that holds a pen in its mouth, floating belly-up, two fish slapping each other with their tails, a school of silver fish (one wearing a tiny wristwatch); (2) a sheet of skinny mutts of every breed (terrier, basset, greyhound, poodle, bulldog, mongrel) with collars and blank tags: snarling over a bowl, tugging, begging; (3) a scaly lizard with a blank stare: working a bank of brass levers, cranking, throwing a knife switch, grabbing a steering wheel, swallowing a hatchling; (4) a floppy-eared mutt: wagging, in a pumpkin Halloween costume (and the empty costume), in a knitted sweater, in a paper party hat, eating a sandwich, as a little grave with a bone on it; (5) a sabre-toothed cat prowling with its mouth open, and pouncing; (6) a pink pig standing alert and clever. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 4. `pb-004-props` (36 uses) · batch 1

Pieces: `velvet-rope`, `banquet-table`, `dog-bowl`, `bureaucrat-desk`, `chain-link`, `wheelbarrow`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a red velvet rope on two brass posts; (2) a long banquet table under a white cloth heaped with roasts, a suckling pig, cakes, fruit and silver cloches, its chairs as pieces; (3) a dented tin dog bowl with a few crumbs, and empty; (4) one tiny clerk at a desk with an in-tray and an out-tray; (5) one iron chain link, copyable into a chain; (6) a wheelbarrow, empty and heaped with green bills. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 5. `pb-005-paper` (34 uses) · batch 1

Pieces: `protocol-sheet`, `flag`, `gilt-frame`, `procurement-contract`, `index-card`, `notebook`  
References: `sheets/briber-ledger.webp` `sheets/treaty-scrolls.webp`

Every paper surface is blank: no writing, numbers or letters. 6 separate cut-outs, each large and well apart: (1) a single typed page of rules with a calm, slightly bored face and stick legs: standing, pointing, yawning, holding three little trays; (2) a blank cloth flag on a pole, a tiny one on a stick, and a white flag on a stick; (3) a gilt picture frame in two sizes, an ape portrait to hang in it, and the frame empty; (4) a long engraved military contract with a wax seal stamped with a missile, joinable end to end into a ring; (5) a plain ruled index card on a little wire stand, and a long paper scroll unrolling from its bottom edge; (6) a school composition notebook, open, ticks on its page. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 6. `pb-006-vehicles` (33 uses) · batch 1

Pieces: `yacht`, `drone`, `cadillac`, `civic`, `jalopy`, `sedan`  
References: `sheets/convoy.webp` `sheets/treaty-road.webp`

Each vehicle seen exactly from the side, no lettering. 6 separate cut-outs, each large and well apart: (1) a white 1950s motor yacht in three sizes, one with a ribbon; (2) a military drone with long wings and a bulb nose with a camera eye; (3) a 1941 Cadillac and a 1948 Cadillac with tail fins; (4) a 1987 Honda Civic hatchback covered in barnacles and fossil shells, a wheel that comes off, an exhaust puff; (5) a rusty 1950s jalopy; (6) a 1950s family sedan sputtering a puff of exhaust. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 7. `pb-007-real` (31 uses) · batch 1

Pieces: `nixon`, `mancur-olson`, `reagan`, `martin-luther-king`, `robert-pape`, `gandhi`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 6 separate cut-outs, each large and well apart: (1) Richard Nixon caricatured (jowls, ski-jump nose, five o'clock shadow) at a 1971 podium with both arms up in the double V; (2) Mancur Olson caricatured: big glasses, high forehead, tweed jacket and bow tie, with a referee's whistle, chalk, a carving knife and a pointer; (3) Ronald Reagan caricatured with a jar of jelly beans; (4) Martin Luther King Jr. at the head of a march, and as an engraved portrait holding a petition; (5) Robert Pape caricatured with a magnifying glass, a pointer and a stack of files; (6) Mahatma Gandhi in shawl and round glasses sitting cross-legged with his spinning wheel, and a row of people sitting in a road. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 8. `pb-008-places` (29 uses) · batch 1

Pieces: `army-base`, `revolving-door`, `brick-wall`, `bridge`, `fomc`  
References: `sheets/buildings.webp` `sheets/doors.png`

Plain buildings, rooms and sets with no faces, front view, every sign and plaque blank. 5 separate cut-outs, each large and well apart: (1) a small fenced army base with a watchtower, barbed wire, a flagpole, a radar dish and two barracks, small enough to plant on a globe; (2) a brass revolving door with four glass leaves, and a little office beside it with its own door; (3) a brick wall in loose bricks that falls flat in one piece, a taller second wall, and a brick wall across a road; (4) a stone bridge, a steel truss bridge half built over a river and collapsing, and a little iron bridge standing and collapsed with a 1950s bus falling with it; (5) twelve humans of different builds in 1950s suits at one round table, each with a blank name tag, then turned outward covering their papers. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 9. `pb-009-people` (27 uses) · batch 1

Pieces: `beat-cop`, `bouncer`, `believer`, `senator-smith`, `soldier`, `drug-dealer`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) a 1950s beat cop in a peaked cap with a whistle, a nightstick and handcuffs, a pocket that bills fit into; (2) a huge bouncer in a black suit and bow tie with a clipboard, a phone and a fingerprint brush; (3) an earnest man in a yachting blazer and captain's cap with a pennant; (4) a brisk woman senator in a 1950s skirt suit, pearls and a cream Stetson: at a desk, swinging a mallet, at a button, on skis, at a boardroom table; (5) a 1950s GI standing with a rifle, squaring off with the rifle raised like a club, in a full-body cast on crutches, charred, shaking, and as a skeleton; (6) a 1950s drug dealer in a zoot suit and pencil moustache whose long coat is lined with little bottles. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 10. `pb-010-body` (26 uses) · batch 1

Pieces: `gene`, `molecule`, `carbon`, `amygdala`, `dna-helix`, `hair`  
References: `germ.webp` `atom.webp`

Microscope-plate and anatomy-plate engravings, with comic faces where listed. 6 separate cut-outs, each large and well apart: (1) the selfish gene: a small twisted double helix with a smug face and stick arms, one drawing for every copy; (2) ball-and-stick molecules with faces in several shapes and little grabbing hands: tiptoeing, pouring coffee, stamping a foot, sulking; (3) a leering carbon atom with four long arms, arms round others; (4) an almond-shaped brass alarm bell with a face and stick legs, and a cord; (5) a tall plain DNA double helix that twists and untwists; (6) a mane of hair growing from a bald head to the floor in three lengths, and eyebrows to match. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 11. `pb-011-food` (25 uses) · batch 1

Pieces: `birthday-cake`, `pie`, `corn`, `birthday-candle`, `carrot`, `cheeseburger`  
References: `sheets/cheese-genius.webp` `sheets/deli.webp`

Food and drink drawn appetizing, labels blank. 6 separate cut-outs, each large and well apart: (1) a 1950s layer cake with candles lit and blown out, a sheet cake with one candle, a tall iced cake with a red cross on top, and its crumbs; (2) a giant lattice pie cut into wedges that lift out, a crust of green bills, and a fork as its own piece; (3) one ear of corn, raw and toasted; (4) one fat birthday candle; (5) one perfect carrot, and with a bite gone; (6) a cheeseburger with a little face and stick legs. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 12. `pb-012-games` (25 uses) · batch 1

Pieces: `gold-bar`, `slot-machine`, `poker-chips`, `roulette-table`, `dartboard`, `hedge-fund`  
References: `sheets/money.webp` `sheets/donut-exam.webp`

Money is green with dark green seals, never red; every card, reel and panel blank. 6 separate cut-outs, each large and well apart: (1) a gleaming gold nugget and a gold bar; (2) a brass 1950s one-armed bandit with a lever, three reels and a coin tray, a spring-loaded boxing glove that shoots out of its front, and a jackpot state pouring coins; (3) poker chips in stacks and loose, and a tower made of them; (4) a 1950s roulette table and wheel, and a green-felt betting table; (5) a pub dartboard and darts; (6) a topiary hedge clipped into a dollar sign, its clippings and garden shears. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 13. `pb-013-buildings` (24 uses) · batch 1

Pieces: `mill`, `department-building`, `irs-building`, `oxford-college`, `supreme-court`, `brain-building`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) a plain 1940s brick factory front with one smokestack and a loading door; (2) a plain federal office block with a face and stick arms, drawn once to be copied with different plaques (the FEC, the F.B.I., the C.I.A. and other agencies); (3) the IRS as its building: a grey columned tax office with a face and a green eyeshade, hands that cover its eyes, a ruler; (4) an Oxford college as a character: a dreaming-spire gatehouse with a face, a mortarboard on its tallest spire, stick legs, a tray of pill bottles in its arms; (5) the Supreme Court building with a face and its own gavel in a white glove; (6) a white clapboard charity building with a huge pink brain for its roof, on a leash. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 14. `pb-014-aliens` (20 uses) · batch 1

Pieces: `moronian-antennae`, `alien-visitors`, `galactic-council`, `moronian`  
References: `sheets/extras-50s-1.webp` `sheets/futures-people.webp`

Aliens engraved like the people in the attached sheets, in 1950s clothes. 4 separate cut-outs, each large and well apart: (1) a pair of small bobbled antennae on a headband that sits on any existing cut-out's head; (2) a row of visiting aliens in 1950s good clothes (an octopus in a bowler, a three-eyed lady in pearls, a crystal man in a tweed jacket, cracked), one fainting; (3) a round marble table floating among the stars with a ring of alien delegates of many shapes in 1950s-tomorrow robes, eyes rolling back in bliss; (4) a Moronian (big domed head, antennae, three-fingered hands) in 1950s clothes in three builds (a suit, a dress, a cardigan), sitting, hands up to hold a prop. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 15. `pb-015-animals` (20 uses) · batch 1

Pieces: `cat`, `cow`, `ape`, `bat-jar`, `ground-squirrel`, `hawk`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 6 separate cut-outs, each large and well apart: (1) a tabby: smug sitting and licking a paw, mid-pounce, flattened against a wall, dizzy, a fat cat in a party hat blowing out candles, hissing; (2) a dairy cow gulping from a pill bottle with a germ on its flank and a cowbell that falls off; (3) an ape ancestor in a tree, climbing down, with a clipboard; (4) a grinning bat in a glass jar; (5) a ground squirrel standing upright screaming, diving into a hole, carried in talons, as a little skeleton; (6) a hawk in a general's cap, the same hawk zipped into a dove costume, swooping with a squirrel, fat. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 16. `pb-016-props` (18 uses) · batch 1

Pieces: `campaign-chest`, `gift-box`, `houseplant`, `key`, `paper-bag`, `refrigerator`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a campaign chest on wheels with a fuel nozzle on a hose; (2) a gift box with a lid and bow that flies off, a plain beige candle inside, and the box tied with a little net; (3) a potted rubber plant in a terracotta pot, and the pot alone big enough to stand in; (4) a big brass key on a ribbon, and an iron key on a wall hook that waves; (5) a brown paper bag with torn eyeholes that inflates and crumples, and one twisted shut with a skull and crossbones; (6) a 1940s Frigidaire with an opening door and stubby legs, and with a machine-gun barrel out of its door. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 17. `pb-017-props` (18 uses) · batch 1

Pieces: `stone-tablet`, `suitcase`, `turmeric-jar`, `umbrella`, `wallet`, `wishing-well`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a cracked mossy carved stone tablet on an easel; (2) a vacation suitcase with travel stickers; (3) a yellow spice jar and its lid; (4) a big black umbrella open and shut, and an umbrella made of a stapled stack of papers, dry and soggy; (5) YOU's leather wallet, open; (6) a stone wishing well with a little roof, a bucket and a crank. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 18. `pb-018-machines` (17 uses) · batch 1

Pieces: `garden-hose`, `lever-desk`, `pylon`, `ray-machine`, `three-way-valve`, `antibody-fridge`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a gleaming green garden hose with a polished brass nozzle and a fancier second nozzle; (2) a brass control desk with two big levers whose handles are a carrot and a stick, and a little third lever; (3) an electricity pylon with its copper lines, and stripped bare; (4) a big brass 1950s science apparatus on a swivel base, a long barrel with a lens at the tip, dials and coils; (5) a brass pipe junction that splits one pipe into three, with a valve wheel, screw caps and pipe lagging; (6) a walk-in fridge with a glass front and a thermometer, stacked with boxed doses. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 19. `pb-019-period` (17 uses) · batch 1

Pieces: `socrates`, `philosophers`, `lady-justice`, `strongman`, `king`  
References: `sheets/townsfolk.webp` `sheets/cost-press.webp`

Every person is a full standing figure, a comic stereotype in the period dress listed. 5 separate cut-outs, each large and well apart: (1) Socrates: bald, bearded, snub-nosed, in a toga with a hemlock cup and one finger up; (2) Kant and Nietzsche chin on fist; (3) Lady Justice on a plinth with her scales as a piece; (4) a Victorian circus strongman in a striped leotard with a curled moustache: flexing, arms up sweating, flat on his back; (5) a medieval king in a crown and ermine with a big chicken leg, on a throne that tips. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 20. `pb-020-wearables` (17 uses) · batch 1

Pieces: `giant-suit`, `boxer-shorts`, `mortarboard`, `sweater`, `blinkers`, `boxing-gloves`  
References: `sheets/you-1.webp` `sheets/fat-cat.webp`

Each is a loose piece to put on an existing cut-out, drawn alone and empty, front view. 6 separate cut-outs, each large and well apart: (1) a suit jacket, white collar and tie big enough for a whole brain; (2) polka-dot boxer shorts sized for the globe; (3) a graduation cap and tassel that sits on a missile; (4) a giant ugly knitted sweater sized for the globe with six blank patches and a loose thread: whole, one patch unravelled, half, gone, its knit pieces separate, and a ball of yarn; (5) a horse's blinkers on a strap, sized for a dog; (6) boxing gloves for YOU, and boxing gloves, stick legs and a towel that fit the green money bundle. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 21. `pb-021-buildings` (16 uses)

Pieces: `engine-building`, `nonprofit-building`, `nonprofit-factory`, `sword-building`, `bls-building`, `census-building`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) a squat steam-engine building with a smokestack, pistons for legs, a cowcatcher grin, a pay window in its side and a row of levers, a tender rolling out certificates; (2) a brick nonprofit building with a face whose door is a donation tin; (3) a big factory with a face and many windows (dogs at typewriters inside), an output chute and a plain side wall; (4) the military as a fortress building with a face, holding a long sword whose point can show on its own; (5) the Bureau of Labor Statistics as an engraved office building with window eyes, a door mouth and white-gloved stick arms that hold a key; (6) the Census Bureau as a long engraved institution building with window eyes, a door mouth and white-gloved stick arms that hold a placard. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 22. `pb-022-paper` (16 uses)

Pieces: `noticeboard`, `paperclip`, `ballot`, `blueprint`, `cookbook`, `question-mark`  
References: `sheets/briber-ledger.webp` `sheets/treaty-scrolls.webp`

Every paper surface is blank: no writing, numbers or letters. 6 separate cut-outs, each large and well apart: (1) a vast public noticeboard on posts with sheets pinned all over it and green and red tabs; (2) a giant paper clip, straight and bent; (3) a ballot on stick legs with a toe tag; (4) a rolled blueprint that unrolls; (5) a fat leather cookbook with a gold ribbon; (6) a big question mark on little legs, sweating. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 23. `pb-023-people` (16 uses)

Pieces: `expert`, `heart-human`, `judge`, `wedding-party`, `banker`, `cheater`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) an egghead professor in a mortarboard and gown with a pipe and half-moon glasses, standing on a stack of framed diplomas; (2) a 1950s woman in a cardigan and cat-eye glasses, a tissue up her sleeve and a paper Valentine heart pinned to it: typing, dialing, sobbing, holding a placard, holding a globe on her shoulder; (3) a bald 1950s judge in a black robe with a gavel, his jaw dropping; (4) a 1950s bride and groom with guests in their best and a tiered cake under a striped awning; (5) a sheet of bowler-hatted bankers in pinstripes with umbrellas, many builds; (6) an everyday man with his fingers crossed behind his back, and disguise pieces (a wig, a headscarf). Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 24. `pb-024-cast-creatures` (15 uses)

Pieces: `robot-killer`, `mainframe-face`, `cell-locks`, `cell-states`, `germ-doctor`  
References: `germ.webp` `sheets/robots.webp` `mainframe.webp`

Keep each existing character exactly as in the attached images, in the new pose described. 5 separate cut-outs, each large and well apart: (1) the pro-war robot grown to gantry size: an army helmet, a missile painted on its chest, an arm cannon, a little out-tray on its back; (2) face pieces for mainframe: two reel eyes that swivel and a tape-slot mouth that smiles; (3) the same cell as in the reference: one big body cell studded with hundreds of little brass locks, some shiny, some rusted shut under cobwebs; (4) the same cell as in the reference: worn (grey, cane, bandaged), new and shiny, a grumpy grown-up cell in a tiny hat with a briefcase and a pinhole in its side, a baby stem cell in a bonnet with a dummy, a beating heart cell, a wiry brain cell in spectacles, a cell in a judge's robe; (5) the same germ as in the reference: in a white coat with a head mirror and stethoscope. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 25. `pb-025-vehicles` (15 uses)

Pieces: `moving-van`, `ocean-liner`, `rocket`, `bandwagon`, `cargo-ship`, `convertible`  
References: `sheets/convoy.webp` `sheets/treaty-road.webp`

Each vehicle seen exactly from the side, no lettering. 6 separate cut-outs, each large and well apart: (1) a 1950s moving van; (2) a 1950s ocean liner with a funnel and flag, a rail deck that tilts; (3) a tall rocket on its launch pad (one drawing for the 1950s rocket and the Apollo); (4) a circus bandwagon with a brass band on top and wheels stuck in mud; (5) a toy-sized cargo ship stacked with containers; (6) a 1950s two-tone convertible with the top down, a child seat in the back, the seats as pieces. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 26. `pb-026-animals` (12 uses)

Pieces: `ant`, `chicken`, `creditworm`, `hamster`, `horse`, `trilobite`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 6 separate cut-outs, each large and well apart: (1) an ant in a little hat and tie walking, an army ant in thick round glasses, and their skeletons still walking; (2) a plump hen; (3) a little worm in a rosette, and the same worm see-through; (4) a hamster in a toga with a lightning bolt pressing a button, running in its wheel, hopping off it, charred; (5) a big plain horse with a tube of dewormer in its teeth, and a dray horse with a tag; (6) a trilobite alive and as a fossil. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 27. `pb-027-buildings` (12 uses)

Pieces: `hospital-giant`, `police-station`, `prison`, `soul-chalet`, `sugar-refinery`, `wall-street`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) a gleaming white hospital on a hill with columns and a cross, no door, one brass mail slot at knee height; (2) a little police station with a face, a police cap on its roof and stick arms; (3) the detention industry as a grinning brick prison, barred windows for eyes, its gate a mouth; (4) the Soul as a Swiss chalet with a cuckoo-clock face, a little door for the cuckoo, a vault door in its side, a gold halo and a leash; (5) a brick sugar refinery with a smokestack, window eyes, a grin and white-gloved stick arms; (6) a columned brokerage front with a ticker-tape awning, a face, big ears and a hole straight through its head from ear to ear. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 28. `pb-028-food` (12 uses)

Pieces: `cloche`, `gum`, `ice-cream-cone`, `pizza`, `steak`, `tomato`  
References: `sheets/cheese-genius.webp` `sheets/deli.webp`

Food and drink drawn appetizing, labels blank. 6 separate cut-outs, each large and well apart: (1) a silver platter with a domed cloche lid, and a truffle shaver; (2) a stick of gum in its wrapper; (3) an ice-cream cone in a paper wrapper, and a towering cone whose scoops are rolled green bills; (4) a pizza on a tin that tears into slices, and its box; (5) a raw steak on a fork; (6) a tomato and its splat. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 29. `pb-029-machines` (12 uses)

Pieces: `benefits-machine`, `elevator`, `gas-pump`, `glass-vault`, `label-gun`, `medicine-plug`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a brass contraption of pipes that sorts papers by itself, with a mechanical arm that slaps away hands; (2) a cutaway 1950s brass elevator car with a folding gate and a floor dial above its door, and its operator in a pillbox hat and white gloves with a clipboard; (3) two 1950s gas pumps with round glass globes; (4) the Treaty Fund as a glass bank vault on short legs with a calm round dial face and an outlet pipe with a valve; (5) a label gun that clacks out tape labels; (6) a fat old plug on a cord with a cross on it, lying on the floor, cobwebbed. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 30. `pb-030-machines` (12 uses)

Pieces: `printer-3d`, `smart-contract`, `stapler`, `trial-machine`, `wall-socket`, `x-ray-machine`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a 1950s-styled 3D printer, a boxy cabinet with a nozzle on a gantry; (2) a glass-cased clockwork machine on a pedestal with a scroll turning inside, a chute out the front and a pipe into the back; (3) a giant office stapler that slams; (4) a gleaming 1950s world's-fair machine in chrome and glass: bottles in at one side, a moving walkway past it, result cards out, dials and a flag, a plug on a cord; (5) a big brass wall socket with many plugs in it; (6) a 1950s X-ray machine. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 31. `pb-031-people` (12 uses)

Pieces: `college-student`, `g-man`, `graduate`, `mannequin`, `mechanic`, `murderer`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) a 1950s college boy in a letter sweater and beanie, with a beer stein; (2) a federal agent in a fedora and trench coat at a typewriter; (3) a young 1950s woman in a cap and gown with a diploma; (4) a department-store mannequin in a hospital gown with a sad painted face, on a dolly; (5) a 1950s service-station attendant in a peaked cap, bow tie and coveralls with a rag, a dipstick and a spanner; (6) a hulking scarred thug in a striped shirt and flat cap with a club. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 32. `pb-032-props` (12 uses)

Pieces: `fountain-pen`, `iron-stove`, `medicine-cabinet`, `nesting-doll`, `pod`, `rent-row`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a fat fountain pen with a price tag on a string; (2) a cast-iron stove with an oven door; (3) a mirrored 1950s bathroom cabinet with three glass shelves and a door that swings; (4) five Russian nesting dolls painted as frowning clerks in different hats, each half separate; (5) an open steel box 0.7 by 2.1 meters with a man in a 1950s shirt lying in it, one elbow against the wall; (6) a rent envelope, a grocery bag, a pill bottle and a piggy bank, each able to shrink. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 33. `pb-033-real` (12 uses)

Pieces: `dawkins`, `de-gaulle`, `emmeline-pankhurst`, `hamilton`, `hayek`, `lbj`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 6 separate cut-outs, each large and well apart: (1) Richard Dawkins caricatured: lean, long face, raised eyebrow, 1970s jacket and wide tie, holding his book; (2) Charles de Gaulle caricatured: very tall, enormous nose, kepi, dark glasses, a baton; (3) Emmeline Pankhurst in her Edwardian hat and sash holding out a pamphlet; (4) W. D. Hamilton caricatured: tall, rumpled, shy, 1960s jacket, with a card; (5) Friedrich Hayek caricatured with a Nobel medal; (6) Lyndon Johnson caricatured: huge ears, big nose, cowboy hat. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 34. `pb-034-places` (11 uses)

Pieces: `garage`, `bretton-woods-hotel`, `casino`, `puppet-booth`, `shopfront`  
References: `sheets/buildings.webp` `sheets/doors.png`

Plain buildings, rooms and sets with no faces, front view, every sign and plaque blank. 5 separate cut-outs, each large and well apart: (1) a 1950s two-bay repair garage: outside (a shelf, a wall with a painted wrench outline and an empty hook) and inside (a car lift, a second bay); (2) the big white Bretton Woods resort hotel with a red roof, and the same hotel in cutaway; (3) a 1950s Las Vegas casino with a blank neon marquee, wide enough to sit on a row of roofs; (4) a Punch-and-Judy puppet booth with a curtain, and a lectern on a plain stage with a cross-bar of strings high above it; (5) a sheet of 1950s high-street shopfronts (a diner, an office, a barber with a striped pole, a store), each with a blank hanging sign. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 35. `pb-035-props` (11 uses)

Pieces: `suggestion-box`, `think-tank`, `toilet`, `toy-blocks`, `toy-wheel`, `archery-target`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a wooden box on a post with a slot and no bottom; (2) a big glass aquarium on a stand with three men in tweed suits floating thoughtfully, bubbles rising; (3) a 1950s toilet with a chain flush, and a gold toilet seat; (4) plain wooden toy blocks of a few sizes with blank faces, stackable; (5) a toy steering wheel on a suction cup; (6) a straw archery target on an easel, which also straps to a chest. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 36. `pb-036-real-period` (11 uses)

Pieces: `susan-b-anthony`, `cantillon`, `frederick-douglass`, `shakespeare`, `charles-mackay`  
References: `sheets/statesmen.webp` `sheets/cost-press.webp`

Each is a caricature of the historical person named, full figure, big head on a smaller body, in the dress of their own time. 5 separate cut-outs, each large and well apart: (1) Susan B. Anthony in black with a parasol and a petition; (2) Richard Cantillon, 1700s banker in a powdered wig, with a quill and an open notebook; (3) Frederick Douglass as an engraved portrait holding a petition; (4) William Shakespeare caricatured (bald dome, earring, ruff) at a writing desk with a quill, Yorick's skull and a pile of pages; (5) Charles Mackay in an 1841 frock coat and side-whiskers holding his book. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 37. `pb-037-weapons` (11 uses)

Pieces: `guillotine`, `pistol`, `rifle`, `helmet-skeletons`  
References: `sheets/destroyers.webp` `sheets/politics-props.png`

Plain weapons with no faces. 4 separate cut-outs, each large and well apart: (1) a guillotine with its blade as a separate piece; (2) a plain revolver whose cylinder swings out as its own piece; (3) a rifle that swings as a piece, a Springfield rifle and a Browning machine gun; (4) grinning skeletons sitting up out of paper in the headgear of each war: a bicorne, a kepi, a doughboy's helmet, a 1940s steel helmet, a parka hood, a jungle helmet, a desert helmet. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 38. `pb-038-cast-props` (10 uses)

Pieces: `ballot-box-glass`, `camo-tin`, `corporation`, `country-maps-2`, `binder-asleep`  
References: `sheets/dd-loop.webp` `sheets/soviet-props.webp` `sheets/briber-props.webp`

Keep each existing prop exactly as in the attached sheets, in the new state described. 5 separate cut-outs, each large and well apart: (1) the same ballot box as in the reference: a glass case with a slot and sealed envelopes inside, its back panel swinging open on gears; (2) the same paint tin as in the reference: camouflage-painted and as tall as a man; (3) the same briefcase as in the reference: on stick legs, its lid opening like a mouth; (4) more country-maps: Venezuela, and Venezuela crumbled to a fifth of itself; (5) the same binder as in the reference: closed eyes and a nightcap. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 39. `pb-039-host` (10 uses)

Pieces: `wishonian`, `wishonian-girl`, `wishonian-dancer`, `wishonian-kids`  
References: `../console/console.webp` `../deck/deck.webp`  
Style: run with `ART_STYLE` unset (host look).

Wishonians in the host look of the attached console and deck. 4 separate cut-outs, each large and well apart: (1) little round Wishonians in her colours pushing a boulder; (2) an eleven-year-old Wishonian girl with her science-fair trifold; (3) a Wishonian in a leotard doing interpretive dance, and a frowning Wishonian crowd; (4) three small round big-eyed Wishonian children sitting cross-legged: laughing, hand up, solemn. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 40. `pb-040-wearables` (10 uses)

Pieces: `groucho-glasses`, `ties`, `trench-coat`, `waiter-kit`, `banana-costume`, `beret`  
References: `sheets/you-1.webp` `sheets/fat-cat.webp`

Each is a loose piece to put on an existing cut-out, drawn alone and empty, front view. 6 separate cut-outs, each large and well apart: (1) glasses, a fake nose and a moustache as a disguise; (2) a gambler's bow tie and a sober striped necktie sized for a building; (3) an empty tall trench coat and fedora open and closed, and three kids stacked in one trench coat with a hat on top; (4) a waiter's long apron, a napkin over the arm, a towel and a silver tray; (5) a banana costume and its delivery box; (6) a black beret that swaps in for YOU's fedora. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 41. `pb-041-fat-cat-lobbyist` (9 uses)

Pieces: `fat-cat-family`, `lobbyist-cross-suit`, `lobbyist-peck`, `fat-cat-frosted`, `health-nut`, `lobbyist-xray`  
References: `sheets/fat-cat.webp` `sheets/briber-people.webp`

Keep the Fat Cat and the masked Lobbyist exactly as in the attached sheets. 6 separate cut-outs, each large and well apart: (1) the fat cat's family: a fat wife in pearls and two fat children, in his look; (2) the same masked Lobbyist as in the reference: his trench coat patterned in little crosses; (3) the same masked Lobbyist as in the reference: bent at the waist, pecking and bobbing like a pigeon; (4) the same Fat Cat as in the reference: smeared in green frosting, a fork in his paw; (5) the fat-cat obsessed with health: in a cold-plunge tub, upside down in gravity boots, on a rowing machine, drinking a green smoothie, taking his pulse, with binoculars; (6) the lobbyist as an x-ray: a wad of bills for a brain, a coin purse for a heart, a piggy bank for a stomach. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 42. `pb-042-people` (9 uses)

Pieces: `recorder-kid`, `suit-kids`, `union-man`, `academic`, `braces-kids`, `celebrity`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) a 1950s schoolkid in a striped T-shirt squeaking a recorder; (2) three children of about eight in sharp tailored suits and slicked hair: daring, pointing, biting; (3) a 1950s union worker in a flat cap, rolled sleeves and overalls hugging a jar of green bills; (4) an academic in a gown and mortarboard stroking his chin, with opera glasses; (5) two kids grinning up in mouthfuls of braces; (6) a 1950s film star in sunglasses and furs at a podium. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 43. `pb-043-cast-period` (8 uses)

Pieces: `caveman-tribe`, `bicorne`, `nobel-skeleton`, `pigeon-skeleton`  
References: `caveman-scientist.webp` `sheets/statesmen.webp` `city-pigeon.webp`

Keep each existing character exactly as in the attached images, in the new pose described. 4 separate cut-outs, each large and well apart: (1) the same caveman as in the reference: hugging a heap of rocks, chewing a book, asleep in a hammock, with spears behind rocks, a stranger in pelts with a napkin and a knife and fork, the tribe hoisting a chief, a clan who all share one big nose and jug ears; (2) Napoleon's bicorne as a loose piece for rulers (and for a whale); (3) nobel's skeleton with his side whiskers, sitting up out of a grave; (4) the carrier pigeon as a little skeleton. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 44. `pb-044-nature` (8 uses)

Pieces: `tree`, `war-mountain`, `black-hole`, `decision-tree`, `iceberg`  
References: `sheets/rocks.webp` `sheets/earth-big.webp`

5 separate cut-outs, each large and well apart: (1) a big shade tree in three growth stages from a sprout, a stand of trees, and burnt black stumps; (2) a snow-capped mountain built of war bills with a plain missile nose for its peak, which also floats as an iceberg; (3) a swirl of stars round a dark mouth that gulps, burps and closes into a smile; (4) an oak whose left branch can be sawn off, a saw, a hammock on the right branch, a playground slide; (5) an iceberg with its small tip above a waterline and its bulk below. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 45. `pb-045-real` (8 uses)

Pieces: `madoff`, `yamanaka`, `beatles`, `bill-gates`, `billionaires`, `david-putrino`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 6 separate cut-outs, each large and well apart: (1) Bernie Madoff: white hair, big grin, dark suit, with a ruler; (2) Shinya Yamanaka caricatured: slim, neat hair, glasses, lab coat, a petri dish; (3) the Beatles caricatured in collarless 1962 suits and mop tops with guitars and a drum, and as bearded 1970 versions walking off in four directions; (4) Bill Gates caricatured: big glasses, a sweater, a strapped bundle; (5) Jeff Bezos and Elon Musk caricatured, standing like museum waxworks; (6) David Putrino of Mount Sinai caricatured in a 1950s suit. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 46. `pb-046-vehicles` (8 uses)

Pieces: `flat-tire`, `locomotive`, `bone-ship`, `british-empire`, `car-cutaway`, `cargo-plane`  
References: `sheets/convoy.webp` `sheets/treaty-road.webp`

Each vehicle seen exactly from the side, no lettering. 6 separate cut-outs, each large and well apart: (1) a flat tire in a beret with a cigarette; (2) an 1880s steam engine; (3) a Greek galley built of bones, its skull figurehead in a spare fedora, some planks a cigarette, a hot dog, a beer can and a lottery ticket; (4) the British Empire as a huge steam-roller with a crown on its funnel, a Union Jack and a face in its boiler; (5) a 1950s chrome sedan in cutaway with eight cylinders and pistons as separate pieces, four cylinders open to seat little committee men, a glovebox that drops open; (6) a 1960s propeller cargo plane. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 47. `pb-047-body` (7 uses)

Pieces: `hydrogen`, `printed-parts`, `car-parts`, `cell-parts`, `crossed-fingers`  
References: `germ.webp` `atom.webp`

Microscope-plate and anatomy-plate engravings, with comic faces where listed. 5 separate cut-outs, each large and well apart: (1) a single-electron hydrogen atom with a worried face biting its nails: drifting, yawning, squashed in a heap, on fire; (2) printed body parts: a windpipe, a titanium skull cap, a chattering jaw, a lab-grown bladder, a kidney, a pink brain and a tiny walnut-sized old brain, a little green Yoda figurine; (3) car parts as body parts: a brake pad shaped like a hip joint, a fuel line clogged with a cheeseburger, a little stent, a heart-shaped car battery, a gearbox tangled in string and goo; (4) cell parts: a chromosome with shoelace tips, a mitochondrion like a battery, a DNA ladder with a broken rung; (5) a hand with crossed fingers. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 48. `pb-048-buildings` (7 uses)

Pieces: `who-building`, `biotech-garage`, `bis-tower`, `candidate-works`, `cathedral`, `dendreon-building`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) the W.H.O. as its building: the Geneva headquarters slab with a face and its snake-and-staff emblem; (2) a ragged garage lab with a face, grabbing; (3) the round Bank for International Settlements tower in Basel with a smug face; (4) a long brick factory with a grinning door, a hopper on top and stamping arms; (5) a Gothic cathedral that can topple; (6) a small biotech building with a face, and the same building boarded up. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 49. `pb-049-cast-poses` (7 uses)

Pieces: `skeptic-pessimist`, `claims-clerk-bureaucrat`, `doctor-50s`, `scientist-lagos-solder`, `trump-sign`, `uncle-sam-referee`  
References: `sheets/donut-more.webp` `sheets/lifeguard-clerks.png` `sheets/scientist-50s.webp`

Keep each existing character exactly as in the attached sheets, in the new pose described. 6 separate cut-outs, each large and well apart: (1) the same gloomy pessimist as in the reference, as the Skeptic: arms folded, raised eyebrow clutching his pearls, fainting, pushing a turnstile, crawling, writing a slip, checking a pocket watch, in a dunce cap; (2) the same insurance clerk as in the reference, as the Bureaucrat: snoring, eyes snapping open, counting with a licked pencil, bowing; (3) the doctor from the reference redrawn in 1950s clothes: white coat, head mirror, stethoscope; (4) the same Lagos researcher as in the reference: a kid in a Lagos garage with a soldering iron and a laptop; (5) Donald Trump full length matching the existing trump, a pen in a comically small hand, holding up a scroll; (6) the same Uncle Sam as in the reference: a referee's striped shirt over his coat, a whistle and a football helmet, holding a football. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 50. `pb-050-paper` (7 uses)

Pieces: `treaty-walker`, `baby-photo`, `bond-eagle`, `class-photo`, `constitution-case`, `credit-card`  
References: `sheets/briber-ledger.webp` `sheets/treaty-scrolls.webp`

Every paper surface is blank: no writing, numbers or letters. 6 separate cut-outs, each large and well apart: (1) a rolled document on stick legs with a face; (2) a framed photo of a masked baby holding a test tube; (3) the engraved war-bond eagle, wings spread, two plain bombs in its talons, and the same eagle with empty talons and an innocent look; (4) a dusty school photograph of a class of girls at their desks with a cobweb on one corner; (5) the Constitution on parchment in a glass case on a plinth, the case also empty; (6) a 1950s charge card held out between two fingers. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 51. `pb-051-period` (7 uses)

Pieces: `pharaoh`, `serf`, `alchemist`, `aristocrats`, `athenian`  
References: `sheets/townsfolk.webp` `sheets/cost-press.webp`

Every person is a full standing figure, a comic stereotype in the period dress listed. 5 separate cut-outs, each large and well apart: (1) a pharaoh on his throne with crook and flail, a cloth tied round his swollen jaw; (2) a barefoot medieval peasant in a sackcloth tunic with a hoe: stacking a rock, with a spear, with a pitchfork, reading, asleep; (3) a medieval alchemist in a pointed hat with a crucible and bellows; (4) French aristocrats in powdered wigs and lace; (5) an Athenian in a chiton with a sack, and a heap of pottery shards. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 52. `pb-052-places` (7 uses)

Pieces: `skyscraper`, `toll-booth`, `barber-shop`, `broom-closet`, `concert-hall`  
References: `sheets/buildings.webp` `sheets/doors.png`

Plain buildings, rooms and sets with no faces, front view, every sign and plaque blank. 5 separate cut-outs, each large and well apart: (1) a 1950s skyscraper with a pulley at the top and a penthouse window; (2) a toll booth whose cash box has a pipe running to a waistcoat pocket; (3) a barber's chair, an eager apprentice with scissors, a customer whose hair grows to the floor (and as a topiary), a licensed barber with a framed licence and clippers; (4) a small basement closet with a bare bulb, a mop, three shelves and a back door; (5) a round concert hall seen from above with its roof lifted off, tiers of tiny people holding lighters, a stage. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 53. `pb-053-building-poses` (6 uses)

Pieces: `pentagon-face`, `bank-steeple`, `fda-pistol`, `fed-mouth`, `filing-cabinet-fda`  
References: `sheets/fed-fda-character.png` `sheets/buildings-2.png`

Keep each existing building exactly as in the attached sheets (the same stone, columns, face and gloves), in the new pose described. 5 separate cut-outs, each large and well apart: (1) the same Pentagon building as in the reference: the Pentagon with a face and two stubby hands; (2) the same little bank building as in the reference: a church steeple growing out of the bank's roof, and a stone font by its door that sprinkles bills; (3) the same FDA building as in the reference: its frieze, columns and door drawn along a pistol's barrel and grip, with its face; (4) the same Federal Reserve building as in the reference: the Federal Reserve building blowing hard through its pediment mouth; (5) the same FDA building as in the reference: a tall filing cabinet with its frieze and face and a chute at its base. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 54. `pb-054-buildings` (6 uses)

Pieces: `dih-building`, `ecohealth-building`, `enforcement-van`, `fdic-office`, `fifa-building`, `fire-station`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) a modest columned building on a shore with a face and a row of outflow valves; (2) EcoHealth Alliance as a small office with a face and a leafy logo; (3) the enforcement agency as a 1950s black van with a face, a slot for bills and a telescoping arm that ends in a big net; (4) the FDIC: a small plain brick insurance office with a modest face in its lintel, a green eyeshade, white-gloved arms and a big rubber stamp; (5) FIFA as its building: a glass-and-marble headquarters with a face, a football on its dome, a chandelier in every window, a mail slot door; (6) the fire department as its building: a face in its doors, a lit match in one hand and a hose in the other. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 55. `pb-055-buildings` (6 uses)

Pieces: `kremlin`, `lehman-brothers`, `meat-factory`, `palantir`, `pcori-building`, `permit-office`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) the Kremlin's Senate building with onion domes and a star on top, window eyes, a door mouth with one big keyhole; (2) a narrow office building with identical moustached brothers at every window, throwing green bills, then pointing at each other; (3) a meat-packing plant as a brick building with a grinning loading door, a conveyor going in and a smokestack; (4) a dark stone tower with a huge glowing crystal ball on top like an eye, with a lid that winks; (5) P.C.O.R.I. as a small new office building with a face, and a leather muzzle that fits it; (6) a squat stone permit office with a face, one window, a long arm with a rubber stamp and a pigeonhole of blank forms. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 56. `pb-056-buildings` (6 uses)

Pieces: `rating-agency`, `smoke-pharma`, `victory-corp`, `warehouse`, `white-house`, `wiv-building`  
References: `sheets/fed-fda-character.png` `sheets/factory-character.png`

Each building is a cartoon character like the buildings in the attached sheets: window eyes, a mouth in its door or pediment, and white-gloved stick arms where listed; the words on friezes and signs are left blank. 6 separate cut-outs, each large and well apart: (1) a little 1950s office building as a character with a rubber stamp in one white glove; (2) a building half cigarette factory (cigarette chimneys) and half pharmacy, one face across both halves, in a trench coat and fedora that fall off; (3) a small brick railway station house with a clock face for a face, a ticket-window mouth and white-gloved hands on switch levers; (4) a long corrugated detention warehouse with a face in its loading door, rows of beds inside, a gauge on its wall; (5) the White House as a building with a face; (6) the Wuhan Institute of Virology as a modern lab block with a face and a biohazard sign. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 57. `pb-057-food` (6 uses)

Pieces: `valentine-box`, `apple`, `beehive`, `beer-bottle`, `beer-mug`  
References: `sheets/cheese-genius.webp` `sheets/deli.webp`

Food and drink drawn appetizing, labels blank. 5 separate cut-outs, each large and well apart: (1) a heart-shaped candy box with a ribbon, and a stack of them; (2) an apple; (3) a beehive dripping honey; (4) a beer bottle; (5) two clinking glass beer mugs with foam. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 58. `pb-058-games` (6 uses)

Pieces: `ballot-drum`, `carousel`, `claw-machine`, `dice`, `domino`, `gumball-machine`  
References: `sheets/money.webp` `sheets/donut-exam.webp`

Money is green with dark green seals, never red; every card, reel and panel blank. 6 separate cut-outs, each large and well apart: (1) a brass lottery drum with a crank, a glass window and gears, sealed numbered envelopes and a tear-off stub; (2) a fairground carousel with painted horses and blank rim panels, and crushed flat; (3) a fairground claw machine big enough to lift a man; (4) twenty white dice with black pips, one rolled to a single pip; (5) a giant domino tile; (6) a red 1950s gumball machine full of tiny people instead of gumballs. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 59. `pb-059-machines` (6 uses)

Pieces: `abacus`, `alarm-clock`, `antibody-dose`, `bathroom-scale`, `camera-pole`, `coin-op-cannon`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a dusty wooden abacus; (2) a twin-bell alarm clock with no snooze button, only a solid brass top; (3) a boxed infusion bag of antibodies, fresh, and green and furry when expired; (4) a bathroom scale with a dial and a needle that snaps; (5) a security camera on a pole that swivels and waves a little hand; (6) a cannon with a coin slot and a meter with a needle. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 60. `pb-060-machines` (6 uses)

Pieces: `desk-lamp`, `engine-block`, `glass-gearbox`, `heart-monitor`, `high-striker`, `legal-robot`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) an angle-poise desk lamp that hops; (2) a small chugging engine; (3) a glass gearbox with spouts; (4) a 1950s hospital pulse monitor on a cart, and a stethoscope as a piece for the fat cat's hands; (5) a carnival test-your-strength tower with a sliding puck, a lever, a brass bell on top and a big wooden mallet; (6) robot pieces: a blank frame, a brain under a glass dome, a butter-knife sword arm, an engine torso with a bond slot, a cuckoo-clock heart with a chocolate-bar door. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 61. `pb-061-machines` (6 uses)

Pieces: `magnet`, `modem`, `money-dial`, `nation-mobile`, `pacemaker`, `particle-accelerator`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a giant horseshoe magnet; (2) a 1990s dial-up modem with a telephone handset in its cradle; (3) a brass wall dial with a big lever; (4) a giant hanging brass mobile whose arms carry pans with little flag poles; (5) a 1950s pacemaker in a little box; (6) a huge brass ring of magnets on a field with a little door in it and a tiny speck popping out. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 62. `pb-062-machines` (6 uses)

Pieces: `photocopier`, `pipe-of-middlemen`, `pneumatic-tube`, `pricing-gun`, `pulley`, `punch-card-heart`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a 1950s office photocopier with a lid; (2) a long riveted pipe with three hatches, a pair of hands with nail scissors in each (gloves, a committee man's cuffs, pinstripe sleeves); (3) a brass pneumatic tube with a canister; (4) a shop's price-tag gun; (5) a pulley on a gallows frame with two ropes; (6) a cutaway of the fat cat's chest: a heart with a brass punch-card reader bolted on and a stack of punch cards. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 63. `pb-063-machines` (6 uses)

Pieces: `punch-clock`, `radio`, `rails`, `reflex-hammer`, `scientist-vending`, `shredder`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a 1950s time clock on a post with a rack of cards; (2) a 1950s portable radio with a dial; (3) railroad track in straight, curved and switch pieces, and a signal post; (4) a doctor's rubber reflex hammer; (5) a 1950s vending machine with the scientist's head and bun on top, a glass front of light bulbs, a form slot, a coin slot and a delivery tray; (6) a giant office paper shredder with a slot on top and a little office box built onto its side. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 64. `pb-064-machines` (6 uses)

Pieces: `slide-rule`, `solar-panel`, `sorting-rack`, `spirit-level`, `syringe`, `taxi-meter`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a giant slide rule; (2) a solar panel on a little stand; (3) a wooden pigeonhole rack with seven slots, a brass pneumatic chute and a letter slot; (4) a brass spirit level whose bubble is a little skull; (5) a big glass syringe; (6) a taxi meter that sits on a lawyer's head. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 65. `pb-065-machines` (6 uses)

Pieces: `test-kit`, `three-supers-plaque`, `tv-camera`, `vacuum-cleaner`, `vending-machine`, `worldcoin-orb`  
References: `sheets/bomb-works.webp` `sheets/soviet-props.webp`

Brass, iron, chrome and glass machines, side or front view, every dial and screen blank. 6 separate cut-outs, each large and well apart: (1) a COVID test kit box with germs crawling out of it; (2) a chrome-and-enamel 1950s advertising board with three round medallion slots and three medallions; (3) a 1950s TV camera on a tripod with a red light; (4) a 1950s upright vacuum cleaner with a fat cloth bag; (5) a 1950s snack vending machine; (6) Worldcoin's chrome orb on a stand with a lens that scans an eye. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 66. `pb-066-people` (6 uses)

Pieces: `chef`, `contrarian`, `dentist`, `detective`, `docent`, `drunk`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) a chef in a tall toque with a medal and a blowtorch; (2) a 1950s greaser in a leather jacket and pompadour with a toothpick, arms crossed; (3) a 1950s dentist with a head mirror and a belt-driven drill, and a dentist's chair with its lamp and spit bowl; (4) a trench-coat detective, yawning; (5) a museum docent in a uniform and peaked cap with a pointer, and his skeleton on a stool; (6) a 1950s drunk in a crumpled suit and loosened tie, a bottle in his pocket, swaying, one eye shut. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 67. `pb-067-people` (6 uses)

Pieces: `ex-commissioner`, `farmers-wife`, `florida-man`, `golfer`, `guard`, `hammock-grandpa`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) a former SEC commissioner in a 1950s suit sitting very still on a shelf like an ornament; (2) a farmer's wife in a 1950s apron and headscarf with a carving knife, swinging and stamping; (3) Florida Man in a loud shirt and shorts with an alligator on a leash; (4) a 1950s golfer in plus-fours and a flat cap, iron raised; (5) a 1950s museum guard in a peaked cap: bought (dollar-sign eyes), scared, with a medal, reading a newspaper; (6) a grandpa asleep in a hammock. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 68. `pb-068-people` (6 uses)

Pieces: `insurgent`, `jetpack-man`, `knitting-circle`, `landlord`, `plumber`, `preacher`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) an insurgent in a balaclava; (2) a 1950s man in goggles with a rocket pack, flying, sputtering, charred; (3) three 1950s ladies in a knitting circle with a blank hand-lettered placard; (4) a landlord in a cardigan with a rent book, filling a doorway; (5) a 1950s plumber in overalls and a cap with a big wrench and a toolbox; (6) a street preacher on a soapbox with a book. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 69. `pb-069-people` (6 uses)

Pieces: `pregnant-woman`, `regulators`, `sarah`, `schoolgirl`, `smoker`, `swiss-chocolatier`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) a 1950s pregnant woman in a polka-dot maternity smock; (2) four privacy inspectors in 1950s dress, each with a ruler and a stamp: a Brussels official with a ring of stars on his lapel, a Californian in sunglasses, a Chicago man in a fedora, a crossing guard; (3) a tired 1950s woman in her forties, cardigan over a shirtwaist dress, handbag; (4) a 1950s schoolgirl in plaits with a slate and chalk; (5) a 1950s man in a cloud of cigarette smoke, coughing; (6) a 1950s Swiss chocolatier in a white apron stirring a copper pot of chocolate. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 70. `pb-070-people` (6 uses)

Pieces: `swiss-man`, `tamil-tiger`, `tinfoil-man`, `vampire`, `veteran`, `weatherman`  
References: `sheets/extras-50s-1.webp` `sheets/extras-50s-2.webp`

Every person is a full standing figure, a comic stereotype you read from the silhouette, in 1950s clothes unless listed otherwise. 6 separate cut-outs, each large and well apart: (1) a cheerful Swiss gentleman in a loden coat and an alpine hat with a feather, a walking stick and a wheel of cheese; (2) a Tamil Tiger fighter in tiger-stripe fatigues with a vest and a book; (3) a man in a tinfoil hat with an antenna on top; (4) a vampire in a 1950s suit and cape; (5) 1950s veterans in service jackets, each with a little storm cloud over his head that rains; (6) a 1950s TV weatherman with a pointer and a grin. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 71. `pb-071-politician` (6 uses)

Pieces: `chimp`, `fossil`, `politician-horse`, `politician-nose`, `stamp-head`, `vampire-fangs`  
References: `sheets/politician-1.webp` `sheets/politician-2.webp`

Keep the Politician exactly as in the attached sheets (the same horse teeth, jaw, ears and wide suit). 6 separate cut-outs, each large and well apart: (1) a chimpanzee in the politician's grey double-breasted suit and wide tie; (2) the politician as a skeleton in rock strata; (3) the politician's head on a racehorse in silks, facing backward and chewing, and at a gallop; (4) a long wooden nose piece for the politician; (5) the politician's head as a rubber stamp on a wooden handle; (6) fangs and a high cape collar as pieces for the politician. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 72. `pb-072-props` (6 uses)

Pieces: `bathtub`, `bow`, `cage`, `card-table`, `ceiling-star`, `collection-plate`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a clawfoot bathtub, a drain that swirls, the plug a gold bar on a chain; (2) a longbow and arrows; (3) a cage that drops from above, on little wheels; (4) a folding card table and chair; (5) a plaster ceiling with a star rose that cracks and falls in chunks; (6) a brass church collection plate on a long handle. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 73. `pb-073-props` (6 uses)

Pieces: `cushion`, `dresser`, `first-aid-tin`, `football-goal`, `garbage-can`, `gavel`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a giant plush cushion with tassels; (2) a tall Victorian dresser that tips over; (3) a small first-aid tin with one sticking plaster in it; (4) a football goal with a net, a 1950s leather football, and a goalkeeper's cap; (5) a dented garbage can; (6) a judge's gavel and block. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 74. `pb-074-props` (6 uses)

Pieces: `gold-watch`, `hat-rack`, `kitchen`, `kitchen-sink`, `mailbox`, `mixing-bowl`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a retirement gold watch in a presentation box; (2) a hat rack with six hats as loose pieces (a cowboy hat, an army cap, a tinfoil hat and more); (3) a gleaming 1950s kitchen, chrome and pastel, with a dining table set for one; (4) a 1950s sink piled with dishes, each with a grinning germ painted on it; (5) a 1950s kerbside mailbox on a post; (6) a 1950s mixing bowl as big as a bathtub. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 75. `pb-075-props` (6 uses)

Pieces: `mop`, `morgue-drawers`, `phone-case`, `piggy-bank`, `pill-box`, `pit`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a mop; (2) a wall of steel morgue drawers; (3) a heap of novelty phone cases (cat ears, a hamburger, a banana, a rubber duck); (4) a china piggy bank, whole and smashed; (5) one pill packet drawn once to recolour, and a single white pill that hops; (6) a round hole in the ground with dirt edges, seen from the side. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 76. `pb-076-props` (6 uses)

Pieces: `ranking-ladder`, `rocking-chair`, `safety-net`, `seesaw`, `shirt`, `shoe-box`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a tall ladder whose rungs are cards; (2) a rocking chair with knitting needles and a long knitted scarf; (3) a circus net held taut by four arms, mostly hole; (4) a plank seesaw on a trestle; (5) a folded dress shirt, stackable; (6) a shoe box, stackable. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 77. `pb-077-props` (6 uses)

Pieces: `shovel`, `steering-wheel`, `stone-block`, `stove`, `straw`, `toolbox`  
References: `sheets/furniture.png` `sheets/household-props.png`

6 separate cut-outs, each large and well apart: (1) a shovel; (2) a ship's steering wheel on a post; (3) one huge stone block, and as bricks; (4) a 1950s enamel kitchen range; (5) a long bendy drinking straw; (6) a toolbox with two drawers. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 78. `pb-078-wearables` (6 uses)

Pieces: `blindfold`, `chef-hat`, `gala-dress`, `lab-coat-sleeve`, `lab-goggles`, `maintenance-kit`  
References: `sheets/you-1.webp` `sheets/fat-cat.webp`

Each is a loose piece to put on an existing cut-out, drawn alone and empty, front view. 6 separate cut-outs, each large and well apart: (1) a blindfold; (2) a tall white chef's toque to sit on the Capitol's dome; (3) a gala dress and a champagne flute; (4) a white lab-coat sleeve and cuff that slides onto a hand; (5) a pair of lab goggles that fit a robot's head; (6) a maintenance worker's cap, coveralls bib, tool belt and crowbar sized for a building. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 79. `pb-079-wearables` (6 uses)

Pieces: `mountie-hat`, `muzzle`, `party-hat`, `pharma-coat`, `pigtails`, `postman-cap`  
References: `sheets/you-1.webp` `sheets/fat-cat.webp`

Each is a loose piece to put on an existing cut-out, drawn alone and empty, front view. 6 separate cut-outs, each large and well apart: (1) a little red-coat Mountie hat that sits on a building's roof; (2) a leather dog muzzle with a buckle that loosens notch by notch; (3) a paper party hat and a tiny flag; (4) a trench coat that turns inside out into a lab coat; (5) a pair of pigtails with bows, alone; (6) a postman's cap and mailbag for YOU. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 80. `pb-080-wearables` (6 uses)

Pieces: `saddle-shoes`, `sneaker`, `sweatband`, `toupee`, `tricorn`, `trumpet-nose`  
References: `sheets/you-1.webp` `sheets/fat-cat.webp`

Each is a loose piece to put on an existing cut-out, drawn alone and empty, front view. 6 separate cut-outs, each large and well apart: (1) saddle shoes as pieces for a leader's feet; (2) a Nike running shoe with its swoosh on little legs; (3) a sweatband for the globe; (4) a toupee; (5) a tricorn hat for the Earth; (6) a brass trumpet bell as a nose piece. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 81. `pb-081-you` (6 uses)

Pieces: `you-aprons`, `you-balloon`, `you-blind`, `you-eyeballs`, `you-old`, `you-taxi`  
References: `sheets/you-1.webp` `sheets/you-2.webp`

Keep YOU exactly as in the attached sheets (the same face, glasses, moustache, fedora and suit). 6 separate cut-outs, each large and well apart: (1) the same YOU as in the reference: a diner apron over a gas-station jacket over his suit, pouring coffee and pumping gas at once; (2) the same YOU as in the reference: swollen round like a balloon; (3) pieces for YOU from the reference: dark lenses for his round glasses and a white cane; (4) pieces for YOU from the reference: his eyeballs on springs, popping out; (5) the same YOU as in the reference: greying, with a paunch, stooped with a cane; (6) pieces for YOU from the reference: a fare meter that flips up on his chest and a little door in his side. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 82. `pb-082-animals` (5 uses)

Pieces: `attack-dog`, `bear`, `bee`, `bowhead-whale`, `dinosaur`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 5 separate cut-outs, each large and well apart: (1) a slavering attack dog on a chain, in several builds; (2) a bear as tall as the frame roaring and swiping, and three bear cubs curled up like a log; (3) a bee; (4) a bowhead whale swimming, surfacing, holding a monocle up with a flipper; (5) a T. rex alive, and as a mounted museum skeleton. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 83. `pb-083-animals` (5 uses)

Pieces: `dolphin`, `dragon`, `elephant`, `goldfish`, `guinea-pig`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 5 separate cut-outs, each large and well apart: (1) dolphins in a pool, one in a fedora and round glasses, flippers up; (2) a dragon on a hoard of coins, choking, X-eyed; (3) a pregnant circus elephant walking, giving birth to a baby elephant, squashed to the width of a suitcase; (4) a goldfish in a bowl in a sweatband doing push-ups; (5) a guinea pig in a tiny lab coat signing with a quill, holding a pill and a bill. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 84. `pb-084-animals` (5 uses)

Pieces: `hydra`, `jellyfish`, `labrador`, `mammoth`, `mole-rat`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 5 separate cut-outs, each large and well apart: (1) a tiny freshwater polyp waving all its tentacles, and a little safe with its door cracked open; (2) a jellyfish holding up a homework page; (3) a labrador barking with its mouth huge, and at a desk in reading glasses with a pencil in its mouth, chewing a form, wagging; (4) a woolly mammoth plodding through snow; (5) a naked mole rat climbing, at a chalkboard with chalk, in a bathtub with a rubber duck. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 85. `pb-085-animals` (5 uses)

Pieces: `money-cat`, `monkey`, `mouse`, `planarian`, `racehorse`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 5 separate cut-outs, each large and well apart: (1) a cat made of green banknotes with plain seals that walks and sits; (2) a lab monkey in a little gown with a suitcase and a stopwatch; (3) an old lab mouse with a cane, spectacles and a white beard; (4) a cross-eyed flatworm, whole, cut in two, and two little worms in baby bonnets; (5) a racehorse with a jockey. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 86. `pb-086-animals` (5 uses)

Pieces: `robot-dog`, `sheep`, `shrew`, `stork`, `tick`  
References: `sheets/dd-big-war.webp` `sheets/ike-snail.png`

Animals drawn like natural-history engravings, with comic expressions. 5 separate cut-outs, each large and well apart: (1) Boston Dynamics' yellow four-legged robot dog: walking, propping someone up, dancing, head turned to stare; (2) a woolly sheep that jumps, with a blank tag on a string round its neck; (3) a small furry shrew, a mother with a litter, at a fancy control panel with dials; (4) a delivery stork with a bundle sling, flying; (5) a giant tick the size of a dog with the Fed building's smug pediment face on its back. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 87. `pb-087-body` (5 uses)

Pieces: `cutaway-head`, `enzyme`, `falling-jaw`, `foot`, `head-house`  
References: `germ.webp` `atom.webp`

Microscope-plate and anatomy-plate engravings, with comic faces where listed. 5 separate cut-outs, each large and well apart: (1) a cutaway skull piece that fits any citizen's head, the brain inside like an anatomy plate; (2) little molecule repairmen in 1950s work caps: with wrenches, on ropes, splicing tape, on a ladder, with lunch pails, nailing a plank; (3) cartoon jaws that drop to the floor; (4) YOU's left foot in its sock and shoe, loose; (5) YOU huge in profile with his head cut away like an anatomy plate: three empty layers and the pipes. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 88. `pb-088-body` (5 uses)

Pieces: `pinky-hands`, `side-effect`, `t-cell`, `third-nipple`, `tumor`  
References: `germ.webp` `atom.webp`

Microscope-plate and anatomy-plate engravings, with comic faces where listed. 5 separate cut-outs, each large and well apart: (1) two giant hands with hooked pinkies, and the same hands with no pinkies holding fountain pens; (2) little grinning gremlins of three kinds carrying suitcases; (3) round white T-cell blobs in 1950s pinstripe suits and fedoras with tommy guns, lounging and playing cards, then hunting; (4) a little shirt-front with three nipples, the third a working light switch; (5) a tumor with its own blood vessels. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 89. `pb-089-food` (5 uses)

Pieces: `berry-bush`, `bill-cake`, `champagne`, `champagne-tower`, `chocolate-bar`  
References: `sheets/cheese-genius.webp` `sheets/deli.webp`

Food and drink drawn appetizing, labels blank. 5 separate cut-outs, each large and well apart: (1) a round berry bush heavy with berries; (2) a tall layered cake of green bills on a cake stand, and the empty stand with crumbs; (3) a champagne bottle that pops, and a coupe glass bubbling, flat and dusty; (4) a pyramid of coupe glasses with green bills sloshing in them; (5) a bar of dark chocolate in a foil wrapper. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 90. `pb-090-food` (5 uses)

Pieces: `coke-bottle`, `egg-carton`, `energy-drink`, `fungus`, `grinning-bottle`  
References: `sheets/cheese-genius.webp` `sheets/deli.webp`

Food and drink drawn appetizing, labels blank. 5 separate cut-outs, each large and well apart: (1) a Coca-Cola bottle; (2) a carton of a dozen eggs; (3) a tall energy-drink can with lightning bolts, and a man in a 1950s suit drinking one, rocketing up and coming down charred with a thumbs up; (4) a fat toadstool with little arms; (5) a giant grinning bottle the height of the frame, tipped and pouring, with no cork. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 91. `pb-091-food` (5 uses)

Pieces: `hamburger`, `magic-mushroom`, `potato-salad`, `rose`, `spaghetti`  
References: `sheets/cheese-genius.webp` `sheets/deli.webp`

Food and drink drawn appetizing, labels blank. 5 separate cut-outs, each large and well apart: (1) a 1950s diner hamburger; (2) a little psychedelic mushroom that hops; (3) a big bowl of potato salad under cling film with a serving spoon; (4) a single long-stemmed rose with a little card, fresh and wilted; (5) a plate of spaghetti and meatballs, and loose noodles. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 92. `pb-092-food` (5 uses)

Pieces: `sugar-cube`, `turkey`, `wedding-topper`, `wine-bottle`, `wishbone`  
References: `sheets/cheese-genius.webp` `sheets/deli.webp`

Food and drink drawn appetizing, labels blank. 5 separate cut-outs, each large and well apart: (1) a sugar cube with a blank paper label; (2) a roast turkey with a detachable drumstick; (3) two grooms on a wedding cake; (4) a wine bottle and two glasses; (5) a wishbone, whole and snapped. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 93. `pb-093-games` (5 uses)

Pieces: `people-snowball`, `pepsi-button`, `shells`, `shooting-gallery`, `spinning-plates`  
References: `sheets/money.webp` `sheets/donut-exam.webp`

Money is green with dark green seals, never red; every card, reel and panel blank. 5 separate cut-outs, each large and well apart: (1) a snowball made of people, arms and hats sticking out, in five sizes; (2) a 1950s Pepsi-Cola bottle-cap push-button on a stand; (3) three walnut shells and a pea; (4) a shooting-gallery booth with a rail, a gold-bullet rifle and a cork gun; (5) four china plates spinning on poles, wobbling and steady. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 94. `pb-094-paper` (5 uses)

Pieces: `directory-board`, `homework-book`, `id-badge`, `kindergarten-class`, `lottery-ticket`  
References: `sheets/briber-ledger.webp` `sheets/treaty-scrolls.webp`

Every paper surface is blank: no writing, numbers or letters. 5 separate cut-outs, each large and well apart: (1) a lobby directory board with felt letters and arrows and an empty slot; (2) a homework book as thick as a wardrobe, its pages battle diagrams; (3) a government ID badge on a clip; (4) a 1950s kindergarten class photo, about 25 children on two benches with their teacher; (5) a scratch-off ticket with a silver panel that peels. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 95. `pb-095-paper` (5 uses)

Pieces: `menu`, `napkin`, `paper-snake`, `patent`, `portrait-photo`  
References: `sheets/briber-ledger.webp` `sheets/treaty-scrolls.webp`

Every paper surface is blank: no writing, numbers or letters. 5 separate cut-outs, each large and well apart: (1) a leather-bound restaurant menu, open and closed, with a bite out of it; (2) a paper napkin with a pencil doodle of a bar and a coffee ring; (3) a long snake made of stacked papers and journals wearing pince-nez, mouth open; (4) a patent certificate with a ribbon seal; (5) a framed Victorian portrait photograph of a stern couple on stick legs. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 96. `pb-096-paper` (5 uses)

Pieces: `ransom-note`, `recipe-box`, `recovery-sign`, `storybook`, `students-1997`  
References: `sheets/briber-ledger.webp` `sheets/treaty-scrolls.webp`

Every paper surface is blank: no writing, numbers or letters. 5 separate cut-outs, each large and well apart: (1) a cream sheet for a ransom note; (2) a tin recipe box and its cards (one blank, a stack with a round scorch on each); (3) a blank sign on two posts: new, rotted and snapped; (4) a big children's storybook with a turning page, and a nightcap; (5) a group photo of 36 college students in 1997 clothes (flannel, frosted tips, a backwards cap). Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 97. `pb-097-paper` (5 uses)

Pieces: `trophy-wall`, `vietnam-poster`, `white-paper`, `wrong-way-sign`, `year-one-photo`  
References: `sheets/briber-ledger.webp` `sheets/treaty-scrolls.webp`

Every paper surface is blank: no writing, numbers or letters. 5 separate cut-outs, each large and well apart: (1) a wall of gilt frames holding triumphs (a vaccine vial, a moon rocket, a smiling surgeon), polished; (2) a 1950s bond poster: a crop duster spraying a cloud over a rice farmer and his two children, who cough and glare; (3) a thick stapled white paper, flat and folded into a wedge; (4) a rectangular road sign on a post, blank; (5) a snapshot of a planet in its year one, everything on fire, one little alien skeleton waving. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 98. `pb-098-period` (5 uses)

Pieces: `barbarians`, `buddha`, `christians`, `fan-bearers`, `medicine-wagon`  
References: `sheets/townsfolk.webp` `sheets/cost-press.webp`

Every person is a full standing figure, a comic stereotype in the period dress listed. 5 separate cut-outs, each large and well apart: (1) two hairy barbarians in furs wiping their feet; (2) a Buddha statue gesturing, and shrugging; (3) a little group of early Christians in plain robes; (4) an Egyptian servant with an ostrich-feather fan; (5) a painted 1900 patent-medicine wagon with bottles of tonic and the salesman in a striped coat and boater on its tailboard. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 99. `pb-099-period` (5 uses)

Pieces: `minutemen`, `monk-astronomer`, `soldier-blue-grey`, `victorian-doctors`, `water-thief`  
References: `sheets/townsfolk.webp` `sheets/cost-press.webp`

Every person is a full standing figure, a comic stereotype in the period dress listed. 5 separate cut-outs, each large and well apart: (1) a row of Minutemen with muskets; (2) a monk astronomer with a quadrant; (3) a Civil War soldier half in Union blue and half in Confederate grey, punching himself; (4) three Victorian surgeons in blood-smeared frock coats, laughing and pointing, then hiding their hands behind their backs; (5) a man in a tall hat with a yoke of two buckets, and a toll gate with a coin box. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 100. `pb-100-places` (5 uses)

Pieces: `fortune-booth`, `nursery-window`, `orange-grove`, `pet-shop-window`, `phone-booth`  
References: `sheets/buildings.webp` `sheets/doors.png`

Plain buildings, rooms and sets with no faces, front view, every sign and plaque blank. 5 separate cut-outs, each large and well apart: (1) a carnival fortune teller's booth with a crystal ball and a turbaned figure; (2) a hospital nursery window with rows of bassinets; (3) rows of orange trees and a porch, and one loose orange; (4) a pet shop window with a striped awning and a little bed of straw; (5) a 1950s glass phone booth. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 101. `pb-101-places` (5 uses)

Pieces: `roman-temple`, `stone-steps`, `temple`, `theater-stage`, `voting-booth`  
References: `sheets/buildings.webp` `sheets/doors.png`

Plain buildings, rooms and sets with no faces, front view, every sign and plaque blank. 5 separate cut-outs, each large and well apart: (1) a Roman temple whose columns are stacks of silver coins; (2) five wide stone steps; (3) a Greek temple with columns and a pediment; (4) a theatre proscenium with curtains, footlights and an arch; (5) a 1950s voting booth whose curtain stops two feet off the ground. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 102. `pb-102-props` (5 uses)

Pieces: `trampoline`, `treasure-chest`, `waiting-chairs`, `whistle-flag`, `yo-yo`  
References: `sheets/furniture.png` `sheets/household-props.png`

5 separate cut-outs, each large and well apart: (1) a big round trampoline with kids bouncing; (2) a pirate chest shut and open with gold, and plain shut chests; (3) a row of waiting-room chairs with a side table of magazines; (4) a referee's whistle and a penalty flag; (5) a yo-yo. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 103. `pb-103-real` (5 uses)

Pieces: `elvis`, `fdr`, `henry-miller`, `james-buchanan`, `jfk`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 5 separate cut-outs, each large and well apart: (1) Elvis Presley caricatured: quiff, sideburns, gold suit, signing a photo of himself; (2) Franklin Roosevelt with a cigarette holder at a jaunty angle and pince-nez, at a microphone; (3) Dr. Henry I. Miller caricatured holding an insulin vial; (4) economist James Buchanan caricatured in glasses; (5) John F. Kennedy caricatured at a podium. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 104. `pb-104-real` (5 uses)

Pieces: `jimmy-hoffa`, `jody-williams`, `jonas-salk`, `jose-figueres`, `kefauver-harris`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 5 separate cut-outs, each large and well apart: (1) Jimmy Hoffa caricatured in his 1970s suit, buried to the chest, waving; (2) Jody Williams caricatured: short grey hair, glasses, a cardigan, at a rotary telephone with a long cord; (3) Jonas Salk caricatured in a 1950s lab coat with a vial and a certificate that tears; (4) José Figueres (Costa Rica, 1948, moustache and suit) with a sledgehammer; (5) Senator Estes Kefauver in his coonskin cap and Representative Oren Harris in a bow tie, carrying something between them. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 105. `pb-105-real` (5 uses)

Pieces: `ken-burns`, `lawrence-tabak`, `lockheed-ceo`, `martin-shkreli`, `obama`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 5 separate cut-outs, each large and well apart: (1) Ken Burns caricatured: bowl haircut, open collar; (2) Lawrence Tabak caricatured at a witness table with a microphone; (3) Lockheed Martin's chief executive caricatured in a 1950s suit; (4) Martin Shkreli caricatured, smirking, and the same on a poster; (5) Barack Obama caricatured (ears, grin) in a dark suit. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 106. `pb-106-real` (5 uses)

Pieces: `pelosi`, `rick-doblin`, `tabarrok`, `tammy-baldwin`, `teddy-roosevelt`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 5 separate cut-outs, each large and well apart: (1) Nancy Pelosi caricatured with a gavel; (2) Rick Doblin caricatured: beard, big grin, shirtsleeves; (3) economist Alex Tabarrok caricatured in a 1950s suit with chalk; (4) Senator Tammy Baldwin caricatured at a microphone; (5) Theodore Roosevelt caricatured (teeth, pince-nez, Rough Rider hat) on horseback, sliding over its neck. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 107. `pb-107-real` (5 uses)

Pieces: `volcker`, `von-neumann`, `walter-freeman`, `warren-buffett`, `wright-brothers`  
References: `sheets/statesmen.webp` `sheets/leaders-a.webp`

Each is a caricature of the real person named, full figure, big head on a smaller body, recognizable at a glance. 5 separate cut-outs, each large and well apart: (1) Paul Volcker: six foot seven, bald, glasses, a cigar; (2) John von Neumann: round face, receding hair, three-piece suit, chalk in hand; (3) Dr. Walter Freeman caricatured, beaming, with an ice pick and a mallet (the mallet also enormous); (4) Warren Buffett caricatured: big glasses, bushy eyebrows, a Cherry Coke; (5) the Wright brothers in bicycle-shop aprons with the 1903 Flyer. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 108. `pb-108-real-period` (5 uses)

Pieces: `charles-ponzi`, `diocletian`, `galileo`, `henry-poor`, `howey`  
References: `sheets/statesmen.webp` `sheets/cost-press.webp`

Each is a caricature of the historical person named, full figure, big head on a smaller body, in the dress of their own time. 5 separate cut-outs, each large and well apart: (1) Charles Ponzi, the 1920 swindler: straw boater, cane, pencil moustache, a grin; (2) Emperor Diocletian caricatured: bull neck, laurel wreath, a toga drawn deep crimson (recolour it purple after cutting: purple keys out with the magenta), a carpenter's plane; (3) Galileo caricatured (big beard, cap) with a long brass telescope; (4) Henry Varnum Poor at a Victorian desk with a quill, and two little railroad bond certificates; (5) W. J. Howey's grove salesman in a white suit and panama hat. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 109. `pb-109-vehicles` (5 uses)

Pieces: `chairlift`, `dump-truck`, `fighter-jet`, `forklift`, `gold-truck`  
References: `sheets/convoy.webp` `sheets/treaty-road.webp`

Each vehicle seen exactly from the side, no lettering. 5 separate cut-outs, each large and well apart: (1) a two-seat chairlift chair on its cable; (2) a dump truck that tips; (3) a fighter jet in loose pieces (wings, tail, canopy); (4) a little 1950s forklift; (5) a 1960s French flatbed truck. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 110. `pb-110-vehicles` (5 uses)

Pieces: `ohio-bus`, `parade-float`, `space-capsule`, `trireme`, `voc-ship`  
References: `sheets/convoy.webp` `sheets/treaty-road.webp`

Each vehicle seen exactly from the side, no lettering. 5 separate cut-outs, each large and well apart: (1) a 1950s city bus with a blank destination blind and a door folding open; (2) a parade float on a flatbed; (3) a 1950s tourist space capsule with a porthole; (4) a Greek warship with oars, and sinking; (5) a 1600s Dutch East India Company galleon with every cannon port smoking. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 111. `pb-111-nature` (4 uses)

Pieces: `matterhorn`, `moon`, `universe-eye`, `vine`  
References: `sheets/rocks.webp` `sheets/earth-big.webp`

4 separate cut-outs, each large and well apart: (1) the Matterhorn; (2) the Moon with a face; (3) a huge eye in a nebula with a lid and a raised eyebrow; (4) a creeping vine whose leaves are war bills, in lengths that grow over a building. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 112. `pb-112-real-period` (4 uses)

Pieces: `joan-of-arc`, `john-hancock`, `madison`, `pangloss`  
References: `sheets/statesmen.webp` `sheets/cost-press.webp`

Each is a caricature of the historical person named, full figure, big head on a smaller body, in the dress of their own time. 4 separate cut-outs, each large and well apart: (1) Joan of Arc in armour, and charred; (2) John Hancock with a quill signing the Declaration of Independence; (3) James Madison caricatured: small, a powdered wig, eyebrows that lift right off his face, a quill; (4) Dr Pangloss in a powdered wig and 18th-century tutor's coat, arms wide. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

### 113. `pb-113-weapons` (4 uses)

Pieces: `bang-pistol`, `button-wall`, `dynamite-house`, `stake`  
References: `sheets/destroyers.webp` `sheets/politics-props.png`

Plain weapons with no faces. 4 separate cut-outs, each large and well apart: (1) a toy pistol whose barrel pops out a little flag; (2) one red button in a bunker panel; (3) a family house built of dynamite sticks with fuses for a chimney; (4) a stake on a pile of sticks. Draw one figure per numbered piece; where a piece lists poses or states, draw only the first. The pieces stand in one row, left to right, in exactly the order listed.

Drawn 2026-11-06: pharma-building, nih-building, university, sec-building, insurance-awake, houses-of-worship, church, funding-pipe, ratchet, brass-pipe, ledger-computer, switchboard, giant-microscope, fish, starving-dog, lizard, pet-dog, sabertooth, pig, velvet-rope, banquet-table, dog-bowl, bureaucrat-desk, chain-link, wheelbarrow, protocol-sheet, flag, gilt-frame, procurement-contract, index-card, notebook, yacht, drone, cadillac, civic, jalopy, sedan, nixon, mancur-olson, reagan, martin-luther-king, robert-pape, gandhi, army-base, revolving-door, brick-wall, bridge, fomc, beat-cop, bouncer, believer, senator-smith, soldier, drug-dealer, gene, molecule, carbon, amygdala, dna-helix, hair, birthday-cake, pie, corn, birthday-candle, carrot, cheeseburger, gold-bar, slot-machine, poker-chips, roulette-table, dartboard, hedge-fund, mill, department-building, irs-building, oxford-college, supreme-court, brain-building, moronian-antennae, alien-visitors, galactic-council, moronian, cat, cow, cow-bell, ape, bat-jar, ground-squirrel, hawk, campaign-chest, gift-box, houseplant, key, paper-bag, refrigerator, stone-tablet, suitcase, turmeric-jar, umbrella, wallet, wishing-well, garden-hose, lever-desk, pylon, ray-machine, three-way-valve, antibody-fridge, socrates, philosophers, kant, nietzsche, lady-justice, strongman, king, giant-suit, boxer-shorts, mortarboard, sweater, blinkers, boxing-gloves

Drawn 2026-11-06 (batch 2): engine-building, nonprofit-building, nonprofit-factory, sword-building, bls-building, census-building, noticeboard, paperclip, ballot, blueprint, cookbook, question-mark, expert, heart-human, judge, banker, cheater-wig, cheater, cheater-headscarf, wedding-party, robot-killer, mainframe-face, mainframe-face-mouth, cell-locks, cell-states, germ-doctor, moving-van, bandwagon, ocean-liner, cargo-ship, convertible, rocket, ant, chicken, creditworm, hamster, horse, trilobite, hospital-giant, police-station, prison, soul-chalet, sugar-refinery, wall-street, cloche, gum, ice-cream-cone, pizza, steak, tomato, benefits-machine, elevator, gas-pump, glass-vault, label-gun, medicine-plug, printer-3d, smart-contract, stapler, trial-machine, wall-socket, x-ray-machine, college-student, g-man, graduate, mannequin, mechanic, murderer, fountain-pen, iron-stove, medicine-cabinet, nesting-doll, pod, rent-row, rent-row-bag, rent-row-piggy, rent-row-pills, dawkins, de-gaulle, emmeline-pankhurst, hamilton, hayek, lbj, garage, bretton-woods-hotel, casino, puppet-booth, shopfront, suggestion-box, think-tank, toilet, toy-blocks, toy-wheel, archery-target, susan-b-anthony, cantillon, frederick-douglass, shakespeare, charles-mackay, guillotine, guillotine-blade, pistol, pistol-cylinder, rifle, helmet-skeletons, ballot-box-glass, camo-tin, corporation, country-maps-2, binder-asleep, groucho-glasses, ties, trench-coat-hat, trench-coat, waiter-kit, banana-costume, beret, fat-cat-family, lobbyist-cross-suit, lobbyist-peck, fat-cat-frosted, health-nut, lobbyist-xray, recorder-kid, suit-kids, union-man, academic, braces-kids, celebrity, caveman-tribe, bicorne, nobel-skeleton, pigeon-skeleton, tree, war-mountain, black-hole, decision-tree, iceberg, madoff, yamanaka, bill-gates, david-putrino, beatles, billionaires, flat-tire, british-empire, car-cutaway, locomotive, bone-ship, cargo-plane, hydrogen, printed-parts, car-parts, cell-parts, cell-parts-chromosome, crossed-fingers, who-building, biotech-garage, bis-tower, candidate-works, cathedral, dendreon-building, skeptic-pessimist, claims-clerk-bureaucrat, doctor-50s, scientist-lagos-solder, trump-sign, uncle-sam-referee, treaty-walker, baby-photo, bond-eagle, class-photo, constitution-case, credit-card, pharaoh, serf, alchemist, aristocrats, athenian, skyscraper, toll-booth, barber-shop, broom-closet, concert-hall, pentagon-face, bank-steeple, fda-pistol, fed-mouth, filing-cabinet-fda, dih-building, ecohealth-building, enforcement-van, fdic-office, fifa-building, fire-station, kremlin, lehman-brothers, meat-factory, palantir, pcori-building, permit-office, rating-agency, smoke-pharma, victory-corp, warehouse, white-house, wiv-building, valentine-box, apple, beehive, beer-bottle, beer-mug, ballot-drum, carousel, claw-machine, dice, domino, gumball-machine, abacus, alarm-clock, antibody-dose, bathroom-scale, camera-pole, coin-op-cannon, desk-lamp, engine-block, glass-gearbox, heart-monitor, high-striker, legal-robot, magnet, modem, money-dial, nation-mobile, pacemaker, particle-accelerator, photocopier, pipe-of-middlemen, pneumatic-tube, pricing-gun, pulley, punch-card-heart, punch-clock, radio, rails, reflex-hammer, scientist-vending, shredder, slide-rule, solar-panel, sorting-rack, spirit-level, syringe, taxi-meter, test-kit, three-supers-plaque, tv-camera, vacuum-cleaner, vending-machine, worldcoin-orb, chef, contrarian, dentist, detective, docent, drunk, ex-commissioner, farmers-wife, florida-man, golfer, guard, hammock-grandpa, insurgent, jetpack-man, knitting-circle, landlord, plumber, preacher, pregnant-woman, regulators, sarah, schoolgirl, smoker, swiss-chocolatier, swiss-man, tamil-tiger, tinfoil-man, vampire, veteran, weatherman, chimp, fossil, politician-horse, politician-nose, stamp-head, vampire-fangs, vampire-fangs-cape, bathtub, bow, cage, card-table, ceiling-star, collection-plate, cushion, dresser, first-aid-tin, football-goal, garbage-can, gavel, gold-watch, hat-rack, hat-rack-tinfoil, kitchen, kitchen-sink, mailbox, mixing-bowl, mop, morgue-drawers, phone-case, piggy-bank, pill-box, pit, ranking-ladder, rocking-chair, safety-net, seesaw, shirt, shoe-box, shovel, steering-wheel, stone-block, stove, straw, toolbox, blindfold, chef-hat, gala-dress, lab-coat-sleeve, lab-goggles, maintenance-kit-cap, maintenance-kit, maintenance-kit-crowbar, mountie-hat, muzzle, party-hat, pharma-coat, pigtails, postman-cap, saddle-shoes, sneaker, sweatband, toupee, tricorn, trumpet-nose, you-aprons, you-balloon, you-blind, you-blind-cane, you-eyeballs, you-old, you-taxi, attack-dog, bear, bee, bowhead-whale, dinosaur, dolphin, dragon, elephant, goldfish, guinea-pig, hydra, hydra-tentacle, jellyfish, labrador, mammoth, mole-rat, money-cat, monkey, mouse, planarian, racehorse, robot-dog, sheep, shrew, stork, tick

Drawn 2026-11-06 (batch 3): cutaway-head, enzyme, falling-jaw, foot, head-house, pinky-hands, side-effect, t-cell, third-nipple, tumor, berry-bush, bill-cake, champagne, champagne-tower, chocolate-bar, coke-bottle, egg-carton, energy-drink, fungus, grinning-bottle, hamburger, magic-mushroom, potato-salad, rose, spaghetti, sugar-cube, turkey, wedding-topper, wine-bottle, wishbone, people-snowball, pepsi-button, shells, shooting-gallery, spinning-plates, directory-board, homework-book, id-badge, kindergarten-class, lottery-ticket, menu, napkin, paper-snake, patent, portrait-photo, ransom-note, recipe-box, recovery-sign, storybook, students-1997, trophy-wall, vietnam-poster, white-paper, wrong-way-sign, year-one-photo, minutemen, monk-astronomer, soldier-blue-grey, victorian-doctors, water-thief, roman-temple, stone-steps, temple, theater-stage, voting-booth, fortune-booth, nursery-window, orange-grove, orange, pet-shop-window, phone-booth, trampoline, treasure-chest, waiting-chairs, whistle-flag, yo-yo, elvis, fdr, henry-miller, james-buchanan, jfk, jimmy-hoffa, jody-williams, jonas-salk, jose-figueres, kefauver-harris, ken-burns, lawrence-tabak, lockheed-ceo, martin-shkreli, obama, volcker, von-neumann, walter-freeman, warren-buffett, wright-brothers, charles-ponzi, diocletian, galileo, henry-poor, howey, chairlift, dump-truck, fighter-jet, fighter-jet-canopy, fighter-jet-wing, fighter-jet-tail, fighter-jet-wing-2, forklift, gold-truck, ohio-bus, parade-float, space-capsule, trireme, voc-ship, matterhorn, moon, universe-eye, vine, joan-of-arc, john-hancock, madison, pangloss, bang-pistol, button-wall, dynamite-house, stake, barbarians, buddha, christians, fan-bearers, medicine-wagon, pelosi, rick-doblin, tabarrok, tammy-baldwin, teddy-roosevelt, wishonian, wishonian-girl, wishonian-dancer, wishonian-kids. Notes: `orange` is the loose orange from `orange-grove`; the fighter jet came in loose pieces (`fighter-jet` is the fuselage, plus `fighter-jet-canopy`, `fighter-jet-tail`, `fighter-jet-wing`, `fighter-jet-wing-2`); `diocletian`'s toga recoloured purple after cutting; `barbarians`, `christians` from `pb-098-period-b`, the Pelosi sheet from `pb-106-real-b` (the first was refused by the image safety filter); the Wishonians from `pb-039-host-c` (the two earlier runs had been sent only the Style line, not the pieces); `minutemen` and `victorian-doctors` are one figure each (repeat them in code); `trireme` came out already sinking.
