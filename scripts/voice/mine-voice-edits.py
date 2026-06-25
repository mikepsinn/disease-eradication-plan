#!/usr/bin/env python3
"""mine-voice-edits: extract (before -> after) prose-edit pairs from git history.

Every prose change the author made to a book .qmd is a labeled preference pair:
the removed wording is 'rejected', the replacement is 'chosen'. This walks git
history, isolates REAL prose edits (dropping parameter/var/link-URL/citation and
structural churn), extracts the tight changed span, classifies the edit, and
writes a JSONL dataset.

That dataset is the raw signal for a data-driven voice rubric + critic, i.e. the
learned version of the hand-written BANNED list in scripts/voice-check.py.

Usage:
  python scripts/voice/mine-voice-edits.py [--limit N] [--out PATH]
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

# Same banned-term knowledge the scanner has, used only to TAG which edits removed
# a violation the scanner already knows (vs. patterns it does not yet know).
_BANNED = [
    (r"\bsame mechanism\b", "whiteboard"), (r"\bsurface area\b", "whiteboard"),
    (r"\bmaximalist\b", "whiteboard"), (r"\balpha\b", "finance"),
    (r"\basymmetr\w*", "finance"), (r"\bproxy (campaign|proposal|fight|vote|battle)\b", "finance"),
    (r"\bdemand letter\b", "finance"), (r"\bbasis points\b", "finance"),
    (r"\bsynerg\w*", "corporate"), (r"\bstakeholder\w*", "corporate"),
    (r"\bparadigm\b", "corporate"), (r"\butiliz\w*", "corporate"),
    (r"\bfacilitat\w*", "corporate"), (r"\bleverage\b", "corporate"),
    (r"\bonboard\w*", "corporate"),
    (r"\bdefense\s+(contractor|industr\w*|compan\w*|sector|primes?|budget|stocks?)", "euphemism"),
    (r"\b(military|defense) primes?\b", "jargon"), (r"\blet that sink in\b", "cliche"),
    (r"\bspoiler alert\b", "cliche"), (r"\bplot twist\b", "cliche"),
    (r"\bmasterclass\b", "cliche"),
]
BANNED = [(re.compile(p, re.I), c) for p, c in _BANNED]

VAR_RE = re.compile(r"\{\{<[^>]*>\}\}")
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")   # keep link TEXT, drop URL
CITE_RE = re.compile(r"\[@[^\]]*\]")
WORD_RE = re.compile(r"[A-Za-z]{2,}")
WS_RE = re.compile(r"\s+")


def demechanize(s):
    """Strip vars / citations and collapse links to their text, so we can tell
    whether the PROSE actually changed (vs. a var/url/citation-only edit)."""
    s = VAR_RE.sub(" ", s)
    s = CITE_RE.sub(" ", s)
    s = LINK_RE.sub(r"\1", s)
    return WS_RE.sub(" ", s).strip()


def changed_spans(before, after):
    a, b = before.split(), after.split()
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    bef, aft, n_changed = [], [], 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        n_changed += (i2 - i1)
        if i2 > i1:
            bef.append(" ".join(a[i1:i2]))
        if j2 > j1:
            aft.append(" ".join(b[j1:j2]))
    return " / ".join(bef), " / ".join(aft), n_changed


def removed_terms(before, after):
    out = []
    for rx, cat in BANNED:
        m = rx.search(before)
        if m and not rx.search(after):
            out.append({"term": m.group(0).lower(), "cat": cat})
    return out


def classify(before, after, n_changed):
    if not after.strip():
        return "cut"
    if n_changed <= 3:
        return "lexical_swap"
    if len(after.split()) < len(before.split()):
        return "tighten"
    return "rewrite"


def flush(commit, date, path, removed, added):
    """Turn a hunk's removed/added line buffers into raw (before, after) pairs."""
    if not path or not path.endswith(".qmd"):
        return
    if "parameters-and-calculations" in path or "/figures/" in path:
        return
    if not removed:                      # pure additions are not 'rejections'
        return
    if added and len(removed) == len(added):
        pairs = list(zip(removed, added))
    elif not added:
        pairs = [(r, "") for r in removed]          # deletions
    else:
        pairs = [(" ".join(removed), " ".join(added))]   # block rewrite
    for before, after in pairs:
        yield commit, date, path, before, after


def iter_raw(limit):
    fmt = "\x01%H\x09%ad"
    cmd = ["git", "log", "-p", "--no-merges", "-U0", "--format=" + fmt, "--date=short"]
    if limit:
        cmd += ["-n", str(limit)]
    cmd += ["--", "knowledge"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding="utf-8", errors="replace")
    commit = date = path = None
    in_hunk = False
    removed, added = [], []
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.rstrip("\n")
        if line.startswith("\x01"):
            yield from flush(commit, date, path, removed, added)
            removed, added, in_hunk, path = [], [], False, None
            rest = line[1:]
            commit, _, date = rest.partition("\t")
            continue
        if line.startswith("diff --git"):
            yield from flush(commit, date, path, removed, added)
            removed, added, in_hunk, path = [], [], False, None
            continue
        if line.startswith("+++ b/"):
            path = line[6:]
            continue
        if line.startswith("@@"):
            yield from flush(commit, date, path, removed, added)
            removed, added, in_hunk = [], [], True
            continue
        if not in_hunk:
            continue
        if line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    yield from flush(commit, date, path, removed, added)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="max commits (0 = all)")
    ap.add_argument("--out", default="scripts/voice/voice-edits.jsonl")
    args = ap.parse_args()

    kept = 0
    types = Counter()
    term_hits = Counter()
    cat_hits = Counter()
    with_banned = 0
    seen = set()
    with open(args.out, "w", encoding="utf-8") as fh:
        for commit, date, path, before, after in iter_raw(args.limit):
            bm, am = demechanize(before), demechanize(after)
            if bm == am:                       # var / url / citation-only edit
                continue
            bspan, aspan, n_changed = changed_spans(bm, am)
            if not WORD_RE.search(bspan + " " + aspan):   # no real words changed
                continue
            key = (bspan.lower(), aspan.lower())
            if key in seen:                    # dedupe identical edits
                continue
            seen.add(key)
            rt = removed_terms(bm, am)
            ctype = classify(bm, am, n_changed)
            rec = {
                "commit": commit, "date": date, "file": path,
                "change_type": ctype, "shorter": len(am.split()) < len(bm.split()),
                "before_span": bspan[:240], "after_span": aspan[:240],
                "removed_terms": rt,
                "before": bm[:600], "after": am[:600],
            }
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
            types[ctype] += 1
            if rt:
                with_banned += 1
                for t in rt:
                    term_hits[t["term"]] += 1
                    cat_hits[t["cat"]] += 1

    print("=" * 60)
    print("VOICE-EDIT CORPUS")
    print("=" * 60)
    print("pairs kept:            %d" % kept)
    print("wrote:                 %s" % args.out)
    print()
    print("by change type:")
    for t, n in types.most_common():
        print("  %-14s %d" % (t, n))
    print()
    print("edits that removed a scanner-known banned term: %d (%.1f%%)"
          % (with_banned, 100.0 * with_banned / kept if kept else 0))
    print("  -> the other %d are voice fixes the regex scanner does NOT catch" % (kept - with_banned))
    print()
    print("top removed banned terms:")
    for term, n in term_hits.most_common(15):
        print("  %-20s %d" % (term, n))
    print()
    print("removed-term categories:")
    for cat, n in cat_hits.most_common():
        print("  %-14s %d" % (cat, n))


if __name__ == "__main__":
    main()
