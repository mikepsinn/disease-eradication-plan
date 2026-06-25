#!/usr/bin/env python3
"""select-exemplars: hand-tagged before->after pairs -> voice-exemplars.jsonl.

DEPRECATED / fallback only. The exemplar bank is now produced by the quality-judge
workflow (8 judges score each pair for whether the AFTER is worth imitating, not
merely better-than-before), which is strictly better than these hardcoded indices.
Kept for reference. The indices reference an OLD sample and include weak pairs the
judge rejects.
"""
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

TAGS = {
    0: "caption_to_joke", 6: "caption_to_joke", 32: "caption_to_joke",
    44: "caption_to_joke", 71: "caption_to_joke", 169: "caption_to_joke",
    181: "caption_to_joke", 193: "caption_to_joke", 195: "caption_to_joke",
    209: "caption_to_joke", 224: "caption_to_joke",
    4: "jargon_to_plain", 48: "jargon_to_plain", 129: "jargon_to_plain",
    134: "jargon_to_plain", 191: "jargon_to_plain",
    5: "long_to_staccato", 217: "long_to_staccato", 227: "long_to_staccato",
    88: "cut_pompous_opener", 149: "cut_pompous_opener",
    12: "cut_self_aware_aside", 186: "cut_self_aware_aside",
    192: "cut_self_aware_aside", 200: "cut_self_aware_aside", 238: "cut_self_aware_aside",
    93: "cut_defensive_rigor", 97: "cut_defensive_rigor", 188: "cut_defensive_rigor",
    61: "cut_scaffolding", 79: "cut_scaffolding", 140: "cut_scaffolding",
    56: "add_absurd_closer", 78: "add_absurd_closer", 128: "add_absurd_closer",
    179: "add_absurd_closer", 182: "add_absurd_closer",
    16: "wrong_adjective", 34: "hedge_claims",
    137: "depersonalize_academic", 218: "depersonalize_academic", 232: "depersonalize_academic",
}

pairs = json.load(open("scripts/voice/sample-pairs.json", encoding="utf-8"))
out = "scripts/voice/voice-exemplars.jsonl"
n = 0
with open(out, "w", encoding="utf-8") as fh:
    for idx, tag in sorted(TAGS.items()):
        p = pairs[idx]
        fh.write(json.dumps({
            "tag": tag, "before": p["before"], "after": p["after"] or "(deleted)",
        }, ensure_ascii=False) + "\n")
        n += 1
print("wrote %d exemplars -> %s" % (n, out))
