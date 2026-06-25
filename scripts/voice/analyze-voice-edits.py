#!/usr/bin/env python3
"""analyze-voice-edits: surface the data-driven rules hiding in the mined corpus.

Deterministic (no LLM). Reads voice-edits.jsonl and reports:
  1. Recurring short swaps  (before -> after that the author made repeatedly)
  2. Words reliably REMOVED  (present in 'before', gone in 'after', net across corpus)
  3. Words reliably ADDED
These are candidate rules for voice-check.py that the hand-written list misses.

Usage:
  python scripts/voice/analyze-voice-edits.py [--in PATH] [--top N]
"""
import argparse
import json
import re
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

WORD = re.compile(r"[a-z][a-z'\-]+")
# function words we don't care about adding/removing
STOP = set("the a an and or but of to in on for with at by from as is are was were be "
           "been being it its this that these those you your they their we our i my he "
           "she his her them then than so if not no do does did has have had will would "
           "can could should may might must just only also more most very which who what "
           "when where how why all any some each".split())


def words(s):
    return [w for w in WORD.findall(s.lower()) if w not in STOP and len(w) > 2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="scripts/voice/voice-edits.jsonl")
    ap.add_argument("--top", type=int, default=30)
    args = ap.parse_args()

    swaps = Counter()
    removed = Counter()
    added = Counter()
    cut_first = Counter()
    n = 0
    with open(args.inp, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            n += 1
            bs, as_ = r["before_span"], r["after_span"]
            # recurring short swaps: <=5 words on the 'before' side
            if r["change_type"] == "lexical_swap" and bs and as_ and len(bs.split()) <= 5:
                swaps[(bs.lower().strip(" /"), as_.lower().strip(" /"))] += 1
            # net word-level add/remove signal (swaps + tightenings)
            if r["change_type"] in ("lexical_swap", "tighten", "rewrite"):
                bw, aw = Counter(words(r["before"])), Counter(words(r["after"]))
                for w in (bw - aw):
                    removed[w] += 1
                for w in (aw - bw):
                    added[w] += 1
            # what kind of line gets cut wholesale
            if r["change_type"] == "cut":
                opener = " ".join(r["before"].split()[:4]).lower()
                if opener:
                    cut_first[opener] += 1

    def show(title, counter, top):
        print("\n" + title)
        print("-" * len(title))
        for k, c in counter.most_common(top):
            if isinstance(k, tuple):
                print("  %3d  %-32s -> %s" % (c, k[0][:32], k[1][:36]))
            else:
                print("  %3d  %s" % (c, k))

    print("corpus pairs: %d" % n)
    show("RECURRING SWAPS (author made this exact swap N times)", swaps, args.top)
    show("WORDS RELIABLY REMOVED (net, across corpus)", removed, args.top)
    show("WORDS RELIABLY ADDED (net, across corpus)", added, args.top)
    show("COMMON CUT-LINE OPENERS (sentences deleted wholesale)", cut_first, 20)


if __name__ == "__main__":
    main()
