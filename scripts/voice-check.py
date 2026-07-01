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
    (r"(?<!\\)\balpha\b(?!\s+cells?)", "finance", "'the edge' / 'the profit' / plain"),  # not LaTeX \alpha or biology "alpha cells"
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
    # only the corporate VERB "leverage X" (= use); the leverage-RATIO noun is legit finance
    (r"\bleverages?\s+(?:existing|the|a|an|its|our|their|your|this|these|those|all)\b",
     "corporate", "'use' (corporate verb 'leverage X'; the leverage-ratio noun is fine)"),
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

# "asymmetry/asymmetric" is precise finance/econ vocabulary as a compound term (information
# asymmetry, capital asymmetry, asymmetric payoffs, Olson's concentrated-vs-diffuse). Skip
# those; still flag loose rhetorical "asymmetric" in reader-facing prose.
ASYMMETRY_OK = re.compile(
    r"(information|capital|power|preference|description|payoff|risk|return|interest|"
    r"wealth|resource|lobbying|structural|temporal|cost|benefit|diffuse|concentrated)\s+asymmetr\w*"
    r"|asymmetr\w*\s+(payoffs?|information|returns?|benefits?|risks?|interests?|"
    r"advantage|upside|bets?|capital)"
    r"|asymmetr\w*\s*\(",
    re.I,
)

# "synergy/synergies/synergistic" is precise pharmacology when the line is about drugs,
# treatments, or their interactions (drug synergy = a supra-additive combination effect).
SYNERGY_OK = re.compile(
    r"drug|treatment|pharmacolog|therapeut|molecul|dose|dosing|receptor|agonist|"
    r"compound|interaction|combination effect",
    re.I,
)

# Mock-statute / mock-contract chapters written in deliberate bureaucratic register (real
# Acts of Congress and HR contracts genuinely say "utilize," "facilitate," "stakeholders,"
# "onboarding," "leverage X" -- flattening these to plain English breaks the played-dead-straight
# bit). Exempt only the bureaucratese category words below; modern pitch-deck words (synergy,
# paradigm, best-in-class, world-class, alpha, rerate) still get flagged even in these files,
# since real statutes and HR contracts never use those either.
FORMAL_REGISTER_FILES = {
    "right-to-trial-fda-upgrade-act.qmd",
    "commission-of-the-president.qmd",
    "humanity-manager-employment-agreement.qmd",
    "notice-of-termination.qmd",
    "presidential-inauguration-ceremony.qmd",
}
FORMAL_REGISTER_EXEMPT_PATTERNS = {
    r"\bstakeholder\w*",
    r"\butiliz\w*",
    r"\bfacilitat\w*",
    r"\bleverages?\s+(?:existing|the|a|an|its|our|their|your|this|these|those|all)\b",
    r"\bonboard\w*",
}


def check(path):
    hits = []
    import os
    is_formal_register = os.path.basename(path) in FORMAL_REGISTER_FILES
    with open(path, encoding="utf-8") as fh:
        for i, raw in enumerate(fh, 1):
            # strip {{< var foo_bar >}} so variable NAMES (e.g. defense_takeover_*) never trigger
            line = re.sub(r"\{\{<\s*var\s+[a-z0-9_]+\s*>\}\}", "", raw)
            # blank out markdown link/image TARGETS so paths/filenames in URLs never trigger
            # (e.g. ...section-stakeholder-alignment.jpg in an image src is not prose)
            line = re.sub(r"\]\([^)]*\)", "]()", line)
            for pat, cat, fix in BANNED:
                if is_formal_register and pat in FORMAL_REGISTER_EXEMPT_PATTERNS:
                    continue
                for m in re.finditer(pat, line, re.I):
                    frag = m.group(0)
                    if "defense" in pat or cat == "euphemism":
                        ctx = line[max(0, m.start() - 16):m.end() + 16]
                        if DEFENSE_OK.search(ctx):
                            continue
                    # precise compound use of asymmetry/asymmetric -> not a voice violation
                    if frag.lower().startswith("asymmetr"):
                        ctx = line[max(0, m.start() - 24):m.end() + 24]
                        if ASYMMETRY_OK.search(ctx):
                            continue
                    # precise pharmacology use of synergy -> not a corporate buzzword
                    if frag.lower().startswith("synerg") and SYNERGY_OK.search(line):
                        continue
                    # a buzzword in 'scare quotes' is being mocked, which the guide allows
                    if (cat in ("corporate", "finance", "whiteboard", "cliche")
                            and m.start() > 0
                            and line[m.start() - 1] in "'‘’\""):
                        continue
                    hits.append((i, frag, cat, fix, raw.strip()[:90]))
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
