#!/usr/bin/env python3
"""voice-critic: the learned-from-your-edits version of the punch-up pass.

Assembles a critic prompt from the data-driven rubric (GUIDES/VOICE_RUBRIC.md) +
the tagged exemplar bank (voice-exemplars.jsonl) + the target prose, asking a model
to predict which edits the author would make and to suggest them in his voice.

This is the inference-time-alignment / best-of-N reward signal described in
AI-Polish (arxiv 2504.07532): the exemplars ARE the reward model, in-context.

By default it prints the ready-to-run prompt (zero dependencies; paste into any
model, or pipe to the Claude CLI). With ANTHROPIC_API_KEY set and the `anthropic`
package installed, pass --call to run it directly.

Usage:
  python scripts/voice/voice-critic.py knowledge/proof/wishonias-wager.qmd
  python scripts/voice/voice-critic.py path.qmd --call          # calls the API
"""
import argparse
import json
import os
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUBRIC = os.path.join(ROOT, "GUIDES", "VOICE_RUBRIC.md")
EXEMPLARS = os.path.join(ROOT, "scripts", "voice", "voice-exemplars.jsonl")

INSTRUCTION = """\
You are the author's voice-critic for the book "How to End War and Disease". Your
job is to predict which edits the AUTHOR would make to the TARGET prose below, in
his voice (Vonnegut / Philomena Cunk: flat, deadpan, concrete, short; never
pompous, never self-aware, never defensive).

You have two inputs: (1) the data-driven RUBRIC of the 11 edit patterns he applies,
mined from 34,742 of his real edits, and (2) a bank of real BEFORE->AFTER EXEMPLARS.
Learn his taste from the exemplars, not from generic "good writing".

For the TARGET, output ONLY real issues as a short list. For each: the offending
span, which pattern it trips (1-11), and a suggested rewrite in his voice (or
"CUT" with the one-line reason it fails the kill-test). Discipline: tie goes to the
incumbent; do not churn working lines; flag pompous openers, self-aware asides,
defensive-rigor preempts, flat captions, and clever-wrapping-nothing first. If a
passage is already as good as it gets, say so and move on. Be concise."""


def load_exemplars(k):
    rows = [json.loads(l) for l in open(EXEMPLARS, encoding="utf-8")]
    random.seed(13)
    # one per tag first (diversity), then fill to k
    by_tag, rest = {}, []
    random.shuffle(rows)
    for r in rows:
        (by_tag.setdefault(r["tag"], r) if r["tag"] not in by_tag else rest.append(r))
    picked = list(by_tag.values()) + rest
    return picked[:k]


def build_prompt(target_text, k):
    rubric = open(RUBRIC, encoding="utf-8").read()
    ex = load_exemplars(k)
    ex_block = "\n".join(
        '- [%s]\n    BEFORE: %s\n    AFTER : %s' % (e["tag"], e["before"], e["after"])
        for e in ex)
    return (INSTRUCTION + "\n\n=== RUBRIC ===\n" + rubric
            + "\n\n=== EXEMPLARS (his real edits) ===\n" + ex_block
            + "\n\n=== TARGET ===\n" + target_text + "\n\n=== CRITIQUE ===\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="path to a .qmd (or - for stdin)")
    ap.add_argument("--k", type=int, default=16, help="exemplars to include")
    ap.add_argument("--call", action="store_true", help="call the Anthropic API")
    args = ap.parse_args()

    text = sys.stdin.read() if args.target == "-" else open(args.target, encoding="utf-8").read()
    prompt = build_prompt(text, args.k)

    if not args.call:
        print(prompt)
        return
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=os.environ.get("VOICE_CRITIC_MODEL", "claude-opus-4-8"),
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    print("".join(b.text for b in msg.content if b.type == "text"))


if __name__ == "__main__":
    main()
