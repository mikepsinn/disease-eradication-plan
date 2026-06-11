# The Comedy Tournament

A process for producing book-quality funny lines (taglines, hooks, joke slots, punch-ups) using parallel agent generation. It has now produced two batches the author rated as good: the President-letter slot tournament (11 upgrades applied) and the EOS tagline tournament (10 finalists, all kept). Use it when a line matters enough to spend compute on: hooks, openers, closers, taglines, shirts.

Why it works, in one line: punchlines are high-variance lotteries, so best-of-N raises the maximum; but N samples from ONE writer share one taste, so diversity must be FORCED, and the final judge must be the author's laugh.

## The recipe

0. **Fix the job spec first.** Where does the line live (masthead, section kicker, shirt, spoken pitch)? Its KPI: stop the scroll, provoke exactly one question ("wait, what?"), survive 10,000 repetitions.
1. **Separate payload from performance.** Don't compress 40 words of mechanism into 120 characters; two-deck it (tagline = feeling, deck = information). The technical substance can enter as a comedy PROP (jargon-as-glamour), not as information.
2. **Build the ingredient bank** of true facts from the book (the ratio, the apocalypse count, the lost trillions, the takeover, the ownership). Every candidate must ride one; agents may not invent facts.
3. **Define archetypes BEFORE generating.** This is the step everyone skips and the reason solo batches come out samey ("ten paint jobs, one car"). The proven archetype set for the 50s register: carnival bark, guarantee/warranty parody, jargon-as-glamour, dark understatement (Cunk), product claim, infomercial furniture, testimonial (including reviews from the diseases). For prose slots, force technique trios from STYLE_GUIDE.md's toolbox instead.
4. **Generate wide, forced-diverse.** One or two generator agents per archetype (vary the fact lens between them), ~10 candidates each, hard char/length limit, no filler to hit quota.
5. **Judge per archetype, brutally, incumbent-biased.** Kill-tests: actually funny (not merely clever)? Rides a true fact? Read-aloud test (it will be spoken)? REPETITION test (pun-twists die on the 10th hearing; attitude survives)? Provokes the right next question? Dark fact INSIDE the cheer, not adjacent? Tie goes to the incumbent; "keep-current" is a respectable verdict. Return top 3 max.
6. **Final cross-archetype judge:** shortlist of <=10, max 2 per archetype, plus an honest verdict on whether anything beats the incumbent or is better deployed as a companion (most winners are companions: section kickers, badges, shirts, pitch buttons).
7. **The author picks by laugh,** then field-test finalists on cold humans (site header, podcast outro, texts); the metric is who replies "wait, what?".

## Deployment discipline

One line, one home. Stacking winners in the same paragraph dilutes them all. Most tournament winners are not taglines; they are proof points that beat the tagline in one specific slot. Install verbatim; do not "improve" a tournament winner while installing it.

## Mechanics

Run via the Workflow tool: pipeline over archetypes (generators in parallel per archetype -> archetype judge), then one final barrier judge. Past run scripts are saved under the Claude session's workflows/scripts directory and can be resumed/adapted. Cost reference: the tagline tournament was 22 agents / ~1M tokens; the letter tournament ~28 agents / ~1.4M tokens (~120k tokens per applied joke).

## Reproducibility

Workflow agents INHERIT the session's current model unless pinned, and the session model can be changed mid-session with /model without leaving a trace in the run output. The two 2026-06 tournaments were unpinned; the session model at the time was most likely claude-sonnet-4-6 (unverifiable retroactively). Rules going forward: (1) PIN the model explicitly in every tournament/benchmark script (agent option model: 'haiku' | 'sonnet' | 'opus'); (2) record date, pinned models, agent count, and token cost in the run notes; (3) "effort" is not a separately settable agent knob; what varies quality is model choice, archetype forcing, and judge discipline.

## The comedy benchmark protocol (cross-model)

Purpose: measure which model writes the funniest lines, calibrate auto-judges against the author's taste, and re-test on each new model release.

1. **Frozen slots** (do not change between runs, so results compare): S1 a new EOS tagline (<120 chars, vs the incumbent), S2 a new memo field for the President-letter block, S3 a new disease review for "Reviews from the Competition". Same frozen ingredient bank and register rules as above.
2. **Pinned arms:** one agent per (arm x slot), each brainstorms >=10 internally, self-applies the kill-tests, returns its top 3. Self-selection is deliberate: the realistic production condition is the same model writing and editing.
3. **Blind ballot:** pool all lines per slot, sort deterministically (alphabetical; workflows cannot use Math.random), strip arm labels. The author rates: top 2 per slot plus any "genuinely funny" flags. Unblind only after ratings.
4. **Score:** points per arm (2 for a top pick, 1 for a flag). Also archive every rated line: the growing corpus of author-rated lines is the real asset, a calibration set for testing whether cheaper auto-judges agree with the author's taste.
5. **Record results in this file** (date, arms, scores) and re-run the identical protocol on new models. Cross-vendor arms (e.g., GPT via the Codex CLI) plug in the same way.

### Results log

- 2026-06-10, v1 run: arms haiku-4-5 / sonnet-4-6 / opus-4-8 (pinned), 9 agents, 27 lines, blind-rated by the author. **Survivors: 4/27** (haiku 2, sonnet 1, opus 1). Findings: (1) no model dominated; (2) the models' self-selected "top 3" had an ~85% kill rate under the author's bar, so self-judging flatters; (3) the archetype tournament with independent judges (10/10 author-approved finalists) decisively outperforms self-judged arms: **process beats model**. Surviving lines (calibration corpus): "We turned the war machine around. It's pointed at cancer now." (opus); "BENEFICIARY: everyone you know who doesn't die this Thursday" (haiku; not installed, Thursday-collision with the letter); Alzheimer's "Five stars. You forgot to fund us. Still waiting." (haiku); Malaria's "I'm leaving a review while I still can." (sonnet).
- 2026-06-10: the author paused generative comedy work; he edits for funny himself. This protocol is retained as reference for if/when that changes.
