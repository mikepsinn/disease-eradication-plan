---
name: voice-critic
description: >
  Critique book prose in the author's voice using patterns learned from his own
  git edit history (not a hand-written rubric). Use when asked to "voice-check",
  "punch up", "make this sound like me / like Vonnegut / like Cunk", or to review
  whether a passage is too pompous / cute / self-aware. Catches what the regex
  scanner (voice-check.py, ~1.4% of real edits) misses.
---

# Voice Critic

The author's voice is **semantic, not lexical** (the most-repeated swap in 34,742
mined edits occurs twice). Regexes can't capture it; exemplars can. This skill
applies the data-driven rubric + exemplar bank distilled from his real edits.

## To critique a passage or a changed file

1. Read `GUIDES/VOICE_RUBRIC.md` (the 11 edit patterns he applies, with examples).
2. Read `scripts/voice/voice-exemplars.jsonl` (quality-judged real BEFORE->AFTER
   pairs — the in-context reward model).
3. For the target prose, for each passage output: the offending span, which
   pattern (1-11) it trips, and a suggested rewrite in his voice OR `CUT` with the
   one-line reason it fails the kill-test.
4. Flag first: flat captions, pompous/announcing openers, self-aware asides,
   defensive-rigor preempts, cliches, and tidy QED bows. Keep the deadpan
   wrong-adjective and concrete-absurd lines.
5. Discipline (binding): **tie goes to the incumbent**; do not churn working lines;
   no rule-zealotry; keep the author's exact words unless you can name the reason.
   **Advisory only** — flag and suggest; never auto-apply (it ossifies past cuts).

Or run the assembled critic prompt directly:

```bash
python scripts/voice/voice-critic.py <file>          # prints the critique prompt
python scripts/voice/voice-critic.py <file> --call   # calls the API (needs key)
```

## Refreshing the model as the author keeps editing

```bash
python scripts/voice/mine-voice-edits.py    # re-mine new commits into the corpus
python scripts/voice/sample-pairs.py        # re-sample the richest pairs
# then re-judge quality and rebuild voice-exemplars.jsonl
```

The exemplar bank is **quality-judged** (a line worth imitating), not merely mined
(better-than-before). Git pairs are worse->better, and better is not good.
