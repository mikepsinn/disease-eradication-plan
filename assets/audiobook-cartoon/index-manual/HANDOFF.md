# Handoff: episode 1 cartoon (2026-11-02)

Working folder: this worktree (`E:/eos/manual/.claude/worktrees/cartoon-storyboard`, branch `feature/index-manual-cartoon`). The 13 shorts (below) are uncommitted. Commit only when Mike asks.

## Where things stand

- **The look** (Mike chose it):
  - Plates are Gilliam-style cut-out collage: engraved cut-outs in 1950s clothes on aged paper, animated with `KIT.collage`.
  - Host shots show Wishonia at a painted console on an observation deck, with Earth hanging in space beside her (`KIT.studio`, art in `video/assets/art/console/` and `deck/`).
  - The backdrop stays still; things move only for a gag.
- **Built in collage:**
  - `pilot-collage` (Part 1's atom sequence): `assets/audiobook/cartoon/pilot-collage-v2.mp4`.
  - **All 13 shorts** (`video/storyboards/shorts.json`): `parts/short-<name>.json` and `compositions/scenes/short-<name>/`, rendered in both shapes to `assets/audiobook/cartoon/short-<name>-v2-16x9.mp4` and `-9x16.mp4` (soviet-plan as `short-soviet-plan-v4-*`), with small `-preview` copies. Mike rejected the first build, which illustrated every line. the-human-economy was rebuilt by hand as one escalating bit, he approved it, and the other 12 followed, one agent per short from a `bit:` line. The highest version of each short is the current one, and all 13 were re-rendered after the redraw of about 50 people into engraved 1950s clothes, with no chest lights and a suited Weapons Maker. Worker extras (baker, miner, sweeper, lamplighter) and period roles were left as they were. Renders with no version are the rejected first build. Open questions are in `DECISIONS.md`.
  - The kit grew for them: `chart`, `rule`, `chain`, `bar`, `wash`, `flatten`, host shots in collage (`host: true`), cast labels and stamps on cut-outs, and generated art sizes (`assets/js/art-sizes.js`). What the agents still had to fake is listed at the end of `KIT-TODO.md`.
- **Storyboards:** all 27 are beat sheets (`video/storyboards/FORMAT.md`), written from the chapter and its numbers. For each spoken line they give the claim, the visual and the gag.
  - Charts carry numbers and trends.
  - Mechanisms are shown literally.
- **Lists the build reads:**
  - `video/storyboards/ART.md`: every cut-out, under one name each.
  - `video/storyboards/KIT-TODO.md`: the collage moves to build, most-used first.
  - `video/storyboards/DECISIONS.md`: Mike's open questions.
- **Older work:** Parts 1 to 14 have scenes in the flat 1950s look, and Parts 1 and 3 are rendered. They get rebuilt in collage. The code-drawn people and props kit goes once nothing uses it.

## Audio (2026-11-06)

- All timings follow `index-manual.7ce6b2b2.mp3` (57:06). Six chunks differ from the published take (02, 06, 08, 10, 15, 18): the food line cut to "we skip the mass murder step", the two-mistakes and 10.7 billion passages condensed, "five times" fixed, and the 2040 line about AI evading tax collection cut (chunk 18, so Part 25 lost the tax office, the auditor and the `audit-side-eye` host cut).
- **It is not published.** The feed still serves `cbaf659d`, so `build-part.mjs` only works where `assets/audiobook/cartoon/index-manual.7ce6b2b2.mp3` exists locally. A fresh checkout gets a 404 until it is uploaded.
- The takes are in `assets/audiobook/cartoon/audio-7ce6b2b2/` (git-ignored): the six chunks and their hashes, the prepared text, alignment, subtitles and the MP3. To publish: merge develop into this branch, copy them into the main checkout's `assets/audiobook/manual-paperback/`, update `index-manual.source_hash` so text prep doesn't rewrite and re-voice the chapter, then sync. Running text prep without that re-voices all 19 chunks.
- This branch is behind develop: its `index-manual.qmd` lacks the restored Nazi line, which the audio has.
- `two-mistakes` is rebuilt on the condensed passage as v4: the cabinet pops onto his desk (12.4 MILLION A YEAR, 8.2 YEARS), the column climbs to 102,000,000, the Thalidomide plates and Kelsey come before the ratio, and the second climb ends on 3,389 : 1. `hyperframes check` flags the REJECTED stamp over the plates, which is intended.
- Other old renders still stand on the old take with the same words: `604-to-1`, `you-bought-the-other-thing`, `donut-doctor`. `the-human-economy` is re-cut as v9 (a new art sheet, `sheets/tomorrow.png`): on "skip" the murder drops out of the same machine, the bills' seals flip from missiles to crosses, the city of tomorrow rises where the bones were, the money goes straight to the family and "23.2× RICHER" replaces THE ECONOMY; she closes the punchline at the console.
- Her mouth (2026-11-05): `build-part.mjs` gives a fast word the most open shape among its letters instead of dropping every shape, and `kit.js` makes a smirk, side-eye or eye-roll wait for a pause while she speaks with her last face that can. Every part's data carries this; renders made earlier don't. Part 2's flat `host-closes` is that plain host shot until its collage rebuild; its beat sheet has the clean machine.

## Next

1. Mike watches the shorts and answers DECISIONS.md.
2. Build the KIT-TODO moves, most-used first (chart first).
3. Generate the recurring cut-outs in ART.md in batches with `video/tools/art-gen.sh`, passing an existing collage sheet as the reference.
4. Build the parts the same way: write each scene's `bit:` line first, build one by hand, and judge the frames for whether they land, not only whether they fit.
