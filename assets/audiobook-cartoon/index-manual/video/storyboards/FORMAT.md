# Storyboard format (the beat sheet)

Each part has one storyboard, `part-NN-*.md`. It says what each spoken line claims, the picture that shows it, and the gag. Mike approves it before any art or animation. The build details (positions, moves, timing) live in the collage scene specs, not here. The worked example is Part 2's money-loop (rebuilt 2026-10-31).

## The part header

Keep the YAML front matter as it is. Under the `#` title, write these:

- **Source:** the `index-manual.qmd` section, plus the `knowledge/` pages it links to for its numbers.
- **The numbers:** each one with its `_variables.yml` name and its value, plus anything derived from it that a picture will use (for example, "crosses 15% in about 2028").
- **What the viewer must leave with:** one sentence.
- **Plates:** one line each. A plate is one picture on aged paper that the camera travels over. Host scenes are Wishonia at her console on the observation deck.
- **Cast:** the cut-outs used, by their names in `assets/art/collage/` (existing or new).
- **Callbacks:** only gags from other parts that this part really pays off.
- **New art:** what Codex has to make.
- **Kit additions:** collage moves the scenes need that `KIT.collage` lacks.

## Each scene

```
## Scene N · scene-id

- id: scene-id
- act: …
- transition_in: cut | same plate (no seam) | …
- cue: "first words"
- time: (filled by tools/storyboard-times.mjs)
- voiceover: "the exact spoken words"
- layer: A, host | B, plate <name>
- wishonia: expression-mouth + body-pose   (layer A only)
- bit: one sentence: the single image the scene (or the run of scenes on one plate) is, how it escalates, and its payoff
- status: planned

| Line | Claim | Visual | Gag |
|---|---|---|---|
| "spoken words" | what it asserts (blank if it continues the row above) | what is on screen, and what leaves | the joke, if any |

Sound: what makes a sound, and on which word.
```

## The bit comes first

Before the table, write the **bit**: one image that carries the whole run of lines and gets worse until it pays off (Part 2: the economy is one machine for getting a loaf of bread, and it stands on the dead). The table then lists only the 3 to 6 moments where the bit changes; lines that change nothing share a row. Illustrating every line, each with its own small picture, is the failure this replaces: it turns into an animated slide deck.

- **Big:** the one or two things on screen fill half to all of the frame height. The camera travels between them rather than showing everything small.
- **Few words:** words on screen only where the narrator's word or number is the joke (MONETARY POLICY, JOBS, 310,000,000).
- **Funny is the check:** before rendering, look at the frames and ask whether each moment lands, not only whether it fits.

## Choosing visuals

- **Numbers and trends** are charts: a line for a trajectory, bars for a comparison, inked on aged paper. The gag happens on the chart.
- **A chart is titled with what it measures**, in the narrator's words, and its marks show every part of it.
- **Mechanisms** are shown literally, as the chapter describes them, never as a metaphor. Growing cybercrime is replicating AI agents, not a plant.
- **One idea per frame:** a thing leaves when its joke is done.
- **Real people** are caricatured by name (Gorbachev, not "a Soviet general").
- **Gags go all the way:** the bomb goes off, people get charred, the dead turn into skeletons.
