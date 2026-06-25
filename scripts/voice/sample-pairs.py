#!/usr/bin/env python3
"""sample-pairs: pick the richest prose edit pairs for LLM distillation.

Filters out reference/metadata/table churn and over-long blocks, keeps real
sentence-level rewrites/tightenings/cuts, and writes a stratified sample as a
compact JSON array (to feed a distillation workflow as `args`).

Usage:
  python scripts/voice/sample-pairs.py [--in PATH] [--out PATH] [--n N]
"""
import argparse
import json
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

BAD = ("http", "://", "{{<", "@article", "@misc", "doi", "title:", "author:",
       "url:", "isbn", "```", "::::", "<span", "<div", "![")


def ok(r):
    b, a = r["before"], r["after"]
    blob = (b + " " + a).lower()
    if any(x in blob for x in BAD):
        return False
    if b.count("|") >= 2:               # table row
        return False
    wc = len(b.split())
    if wc < 6 or wc > 55:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="scripts/voice/voice-edits.jsonl")
    ap.add_argument("--out", default="scripts/voice/sample-pairs.json")
    ap.add_argument("--n", type=int, default=240)
    args = ap.parse_args()

    buckets = {"rewrite": [], "tighten": [], "cut": []}
    with open(args.inp, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            t = r["change_type"]
            if t in buckets and ok(r):
                buckets[t].append({"before": r["before"], "after": r["after"],
                                   "type": t, "file": r["file"].split("/")[-1]})

    random.seed(7)
    quota = {"rewrite": int(args.n * 0.45), "tighten": int(args.n * 0.30),
             "cut": int(args.n * 0.25)}
    out = []
    for t, q in quota.items():
        random.shuffle(buckets[t])
        out += buckets[t][:q]
    random.shuffle(out)

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False)
    print("available: " + ", ".join("%s=%d" % (t, len(v)) for t, v in buckets.items()))
    print("sampled:   %d  -> %s" % (len(out), args.out))


if __name__ == "__main__":
    main()
