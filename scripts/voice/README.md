# Voice pipeline: learning the author's taste from git history

The hooks and `voice-check.py` are a hand-written regex rubric. They catch ~1.4% of
the voice-editing the author actually does. This pipeline learns the rest from the
edit history itself: every prose diff is a labeled (rejected -> chosen) pair. This
is the approach in EditPrefs and AI-Polish (arxiv 2504.07532): edits become a
reward signal used at inference time, no model fine-tuning.

## Pipeline

```
git history
   |  mine-voice-edits.py        extract before->after prose pairs (drop param/link/ref churn)
   v
voice-edits.jsonl                34,742 labeled pairs
   |  analyze-voice-edits.py     recurring swaps + reliably-cut words (deterministic)
   |  sample-pairs.py            stratified sample of the richest pairs
   v
sample-pairs.json / candidates   studied -> the 11 patterns (GUIDES/VOICE_RUBRIC.md)
   |  quality-judge workflow      8 judges score each pair for AFTER-quality (a line
   |  (calibrated by author veto)  worth imitating, NOT merely "better"); kept 83/400.
   v
voice-exemplars.jsonl (51)       quality-vetted few-shot exemplars (the reward model)
   |  voice-critic.py            assemble rubric + exemplars + target -> critique prompt
   v
a critique in the author's voice
```

## Use the critic

```bash
# print the ready-to-run critic prompt for a file (zero deps; paste into any model)
python scripts/voice/voice-critic.py knowledge/proof/wishonias-wager.qmd

# or, as a Claude Code subagent: tell an agent to Read VOICE_RUBRIC.md +
# voice-exemplars.jsonl, then critique the passage. (See the demo in chat history.)

# or call the API directly (needs ANTHROPIC_API_KEY + `pip install anthropic`)
python scripts/voice/voice-critic.py path.qmd --call
```

## Refresh as the corpus grows

Every new edit you make is more training signal. Periodically:

```bash
python scripts/voice/mine-voice-edits.py        # re-mine (picks up new commits)
python scripts/voice/sample-pairs.py --n 400 --out scripts/voice/candidates.json
# split candidates.json into scripts/voice/cand/batch-*.json, then run the
# quality-judge workflow (scripts/voice/voice-exemplar-quality-judge): 8 judges keep
# only lines worth imitating; synthesis balances the bank -> voice-exemplars.jsonl.
# (select-exemplars.py is the older hand-indexed path, superseded by the judge.)
```

That is the flywheel: the critic improves as you keep editing, with no GPUs.

## What it does and does not do

- **Captures the reliable 80%** (pompous openers, self-aware asides, defensive-rigor
  preempts, flat captions, jargon, length, cliches) very well. The demo critic
  reproduced an unseen taste judgment from exemplars alone.
- **The creative 20%** (is this joke actually funny; is this the right dark beat) is
  sparse in the data and stays with you. The critic is a filter that removes your
  reliable dislikes so your tokens go only to the 20% that needs you.
- **Keep it advisory, never auto-apply.** Auto-applying ossifies "what was cut
  before" into rules that kill good new lines. Flag and suggest; you decide. (This
  is why the style guide's "tie goes to the incumbent / no rule-zealotry" matters.)

## Wiring options (not yet done)

- Reference `GUIDES/VOICE_RUBRIC.md` from `CLAUDE.md` so it loads into context.
- Upgrade `.claude/hooks/voice-punchup-review.py` to also surface the rubric + run
  `voice-critic.py` on the changed files.
- Add a `voice-critic` Claude Code skill that critiques the current diff on demand.
