#!/usr/bin/env python3
"""voice-check: fast, deterministic flag for STYLE_GUIDE voice violations.

Catches the things the LLM punch-up pass keeps re-introducing: engineer/whiteboard
jargon, finance jargon, corporate buzzwords, the "defense" euphemism, and pitch-speak.

It is ADVISORY (a few hits may be intentional, e.g. quoting a buzzword to mock it, or
literal finance "leverage"). Review each against GUIDES/STYLE_GUIDE.md. Exits non-zero
if anything is flagged, so it works as a pre-commit / CI / Claude Code hook.

Usage:
  python scripts/voice-check.py knowledge/economics/investment-thesis.qmd [more files...]
"""
import re
import sys

# (regex, category, plain-English fix)
BANNED = [
    # engineer / whiteboard jargon  (STYLE_GUIDE: "engineer-jargon as cleverness")
    (r"\bsame trade\b", "whiteboard", "say the plain thing: 'uses the same strategy'"),
    (r"\bsame play\b", "whiteboard", "say the plain thing"),
    (r"\bone level up\b", "whiteboard", "say what it actually does"),
    (r"\bsame mechanism\b", "whiteboard", "say the plain thing"),
    (r"\bsurface area\b", "whiteboard", "say the plain thing"),
    (r"\bmaximalist\b", "whiteboard", "plain word"),
    # finance jargon
    (r"(?<!\\)\balpha\b", "finance", "'the edge' / 'the profit' / plain"),  # not LaTeX \alpha
    (r"\brerate[sd]?\b", "finance", "'reprice' / 'worth more'"),
    (r"\basymmetr\w*", "finance", "'lopsided' / plain"),
    (r"\bproxy (campaign|proposal|fight|vote|battle)\b", "finance",
     "'a campaign to put your own person on the board'"),
    (r"\bdemand letter\b", "finance", "'a legal letter the board must read'"),
    (r"\bactivist stake\b", "finance", "'enough shares to win board seats'"),
    (r"\binvestable assets\b", "finance", "'money invested worldwide'"),
    (r"\bbasis points\b", "finance", "plain percent"),
    # corporate / startup buzzwords  (STYLE_GUIDE DON'T list)
    (r"\bsynerg\w*", "corporate", "cut it"),
    (r"\bstakeholder\w*", "corporate", "say who specifically"),
    (r"\bparadigm\b", "corporate", "cut it"),
    (r"\butiliz\w*", "corporate", "'use'"),
    (r"\bfacilitat\w*", "corporate", "'help' / 'let'"),
    (r"\bleverage\b", "corporate", "'use' (keep ONLY if literal finance leverage)"),
    (r"\bonboard\w*", "corporate", "plain word"),
    (r"\bworld-class\b", "corporate", "cut it"),
    (r"\bbest-in-class\b", "corporate", "cut it"),
    # euphemism  (STYLE_GUIDE: never "defense contractor")
    (r"\bdefense\s+(contractor|industr\w*|compan\w*|sector|primes?|budget|stocks?)",
     "euphemism", "'military-industrial complex' / 'military contractors'"),
    (r"\b(military|defense) primes?\b", "jargon", "'the big military contractors' (nobody knows 'prime')"),
    (r"\bprime contractor", "jargon", "'the big military contractors'"),
    # pitch-speak / tired cliche  (STYLE_GUIDE)
    (r"\blet that sink in\b", "cliche", "cut it"),
    (r"\bjoin us\b", "pitch", "you're teaching, not recruiting"),
    (r"\bour platform\b", "pitch", "'your ...'"),
    (r"\bspoiler alert\b", "cliche", "cut it"),
    (r"\bplot twist\b", "cliche", "cut it"),
    (r"\bmasterclass\b", "cliche", "cut it"),
    # adversarial stance / manufactured objections  (STYLE_GUIDE: don't preempt objections nobody raised)
    (r"\byou (might|may|could) (object|argue)\b", "stance", "don't manufacture-then-defeat the reader's objection"),
    (r"\b(some|skeptics|critics|cynics) will say\b", "stance", "don't set up a strawman objection to knock down"),
    (r"\bi know what you'?re thinking\b", "stance", "drop the mind-reading setup; just state it"),
    (r"\byou'?re probably thinking\b", "stance", "drop the mind-reading setup; just state it"),
    (r"\bwatch what you just did\b", "stance", "don't narrate the reader's move and defeat them for it"),
]

# Legit contexts that LOOK like a hit but aren't (skip the match).
DEFENSE_OK = re.compile(r"missile defense|department of defense|defense against|self-defense", re.I)


def check(path):
    hits = []
    with open(path, encoding="utf-8") as fh:
        for i, raw in enumerate(fh, 1):
            # strip {{< var foo_bar >}} so variable NAMES (e.g. defense_takeover_*) never trigger
            line = re.sub(r"\{\{<\s*var\s+[a-z0-9_]+\s*>\}\}", "", raw)
            for pat, cat, fix in BANNED:
                for m in re.finditer(pat, line, re.I):
                    if "defense" in pat or cat == "euphemism":
                        ctx = line[max(0, m.start() - 16):m.end() + 16]
                        if DEFENSE_OK.search(ctx):
                            continue
                    hits.append((i, m.group(0), cat, fix, raw.strip()[:90]))
    return hits


def main():
    total = 0
    for path in sys.argv[1:]:
        try:
            hits = check(path)
        except FileNotFoundError:
            print(f"voice-check: file not found: {path}", file=sys.stderr)
            continue
        for (ln, frag, cat, fix, ctx) in hits:
            print(f'{path}:{ln}: [{cat}] "{frag}" -> {fix}')
            total += 1
    if total:
        print(f"\n{total} voice-check flag(s). Review vs GUIDES/STYLE_GUIDE.md "
              f"(a few may be intentional, e.g. mocking a buzzword).")
        sys.exit(1)
    print("voice-check: clean")
    sys.exit(0)


if __name__ == "__main__":
    main()
