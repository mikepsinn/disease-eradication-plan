# Handoff: episode 1 cartoon (2026-10-31)

Working folder: this worktree (`E:/eos/manual/.claude/worktrees/cartoon-storyboard`, branch `feature/index-manual-cartoon`). Everything since commit `b99c5717b` is uncommitted. Commit only when Mike asks.

## Where things stand

- **The look** (Mike chose it):
  - Plates are Gilliam-style cut-out collage: Victorian engraving cut-outs on aged paper, animated with `KIT.collage`.
  - Host shots show Wishonia at a painted console on an observation deck, with Earth hanging in space beside her (`KIT.studio`, art in `video/assets/art/console/` and `deck/`).
  - The backdrop stays still; things move only for a gag.
- **Built in collage:**
  - `pilot-collage` (Part 1's atom sequence): `assets/audiobook/cartoon/pilot-collage-v2.mp4`.
  - `short-soviet-plan`: built by Sonnet from the old storyboard. Its imagery (gauge, plant) was wrong, which led to the beat-sheet rewrite below. Rebuild it from Part 11's storyboard.
- **Storyboards:** all 27 are beat sheets (`video/storyboards/FORMAT.md`), written from the chapter and its numbers. For each spoken line they give the claim, the visual and the gag.
  - Charts carry numbers and trends.
  - Mechanisms are shown literally.
- **Lists the build reads:**
  - `video/storyboards/ART.md`: every cut-out, under one name each.
  - `video/storyboards/KIT-TODO.md`: the collage moves to build, most-used first.
  - `video/storyboards/DECISIONS.md`: Mike's open questions.
- **Older work:** Parts 1 to 14 have scenes in the flat 1950s look, and Parts 1 and 3 are rendered. They get rebuilt in collage. The code-drawn people and props kit goes once nothing uses it.

## Next

1. Mike answers DECISIONS.md and reviews the beat sheets, starting with the shorts (listed in `video/storyboards/README.md`).
2. Build the KIT-TODO moves, most-used first (chart first).
3. Generate the recurring cut-outs in ART.md in batches with `video/tools/art-gen.sh`, passing an existing collage sheet as the reference.
4. Build the 13 shorts, then the parts. The strong model writes the specs from the approved beat sheet; Sonnet can build the routine scenes.
