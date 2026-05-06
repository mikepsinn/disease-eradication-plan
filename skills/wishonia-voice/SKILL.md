---
name: wishonia-voice
description: Review and improve QMD chapter writing quality by replacing boring/consultant text with Wishonia's deadpan alien voice, consolidating redundancy, and reducing word count. Use when asked to fix voice, make content funnier, remove jargon, or enforce the book's writing style.
---

# Wishonia Voice Enforcement & Writing Quality

## What This Skill Does

Reviews QMD chapters in the disease eradication plan Quarto book and improves writing quality by:
1. Replacing boring text with funnier text that conveys the same information in fewer words
2. Eliminating redundancy and duplication
3. Fixing consultant/jargon language
4. Injecting Wishonia humor where it's missing

**The net word count should stay flat or decrease.** Never just add text. If you add a funny opening, find existing dry text that says the same thing worse and delete or compress it.

## The Voice

Wishonia is a naive alien observing Earth's self-destructive choices with genuine confusion. Think Philomena Cunk's deadpan, Jack Handey's one-liners, Kurt Vonnegut's brevity. The humor comes from stating obvious absurdities as simple observations.

**Good examples from the book:**

- "Courts with armies are called 'governments,' and governments are the defendants." (court-of-humanity.qmd, voice: 10)
- "'checks and balances,' which contains the word 'checks' the same way 'grape soda' contains the word 'grape'" (court-of-humanity.qmd, voice: 10)
- "which suggests either innumeracy or enthusiasm" (humanity-v-government.qmd, voice: 9)
- "On Wishonia, when we found a way to audit everything for free in real time, we stopped paying 3,400 people to audit some things slowly for $803 million. We did this on the same day. It did not require a committee." (decentralized-accountability-office.qmd — book chapter, "On Wishonia" OK here)

**Good examples for papers (no "On Wishonia"):**

- "Any engineer looking at a machine that converts inputs to outputs at 3.7% efficiency would replace the machine. Your species instead feeds the machine more money." (us-efficiency-audit.qmd)
- "Your species has known for decades which government programs save the most lives per dollar. You have ranked them." (incentive-alignment-bonds-paper.qmd)
- "Your species is sitting on a combinatorial goldmine of potential cures and has chosen to explore it with a teaspoon." (dfda-impact-paper.qmd)

**Never:** consultant, crypto bro, salesman, "leverage" (non-financial), "synergy" (non-satirical), "stakeholder" (non-satirical), "operationalize", "comprehensive" (consultant sense).

## "On Wishonia" References

**Remove "On Wishonia" from punchlines.** When it's just framing a joke ("On Wishonia, we have a word for this"), the joke is funnier without it. "There is a word for this" lands harder and works as a standalone paper, tweet, or pitch deck.

**Keep "On Wishonia" for counterfactual world-building.** When Wishonia is describing what it actually did as a civilization ("On Wishonia, we eliminated disease 4,000 years ago," "On Wishonia, we fixed this 4,297 years ago," "On Wishonia, we built a system that asks everyone"), the reader needs to know WHO did it. Without "On Wishonia," the "we" is orphaned and the counterfactual loses its power.

**The test:** Does the sentence describe something that happened on the planet (built, eliminated, fixed, tried, discovered)? Keep "On Wishonia." Is it just a setup for a punchline (we have a word for this, we call this X, we find this remarkable)? Remove it.

**Never use the same replacement pattern twice in one file.** Repetition kills humor. Rotate through these:

| Pattern | Example | Best for |
|---------|---------|----------|
| Just state it | "The gate costs more than what is behind it. Removing it is arithmetic." | When the fact is already absurd enough |
| Professional observer | "An engineer would call this a system." / "Accountants call this..." | Technical absurdities |
| "Your species..." | "Your species optimized for maximum death per dollar" | Big-picture observations |
| "No sane X would..." | "No sane audit process lets the defendant grade their own exam." | Institutional absurdities |
| "There is a word for this." | "There is a word for this. The word is 'cancer.'" | Punchline delivery |
| "A rational civilization..." | "In a rational civilization, this would be performance art." | Contrast jokes (use ONCE per file max) |
| Reframe the contrast | "On Earth, you call it X" → "Your species calls it X" | When the Earth/Wishonia contrast was the joke |
| Kill the setup | Cut "On Wishonia we do X" entirely, keep only the punchline | When the punchline doesn't need a setup |

**The funniest option is usually the shortest.** If you can cut the framing entirely and just state the obvious absurdity, do that. Vonnegut never needed a narrator to tell you something was insane. He just described it.

## Descriptions and Subtitles

Frontmatter `description:` and `subtitle:` fields show up in search results, social cards, and RSS feeds. They are often the only thing someone reads before deciding to click.

**Rule: descriptions and subtitles must contain actual information.** A reader should learn what the chapter argues, covers, or proposes just from the description. Humor is welcome but not at the expense of content.

- **Bad:** "90 Days to Make the Thing Real" (tagline, conveys nothing)
- **Good:** "A 90-day pilot to launch the first public Earth Optimization Prize without creating a single point of failure" (tells you what it is)
- **Also good:** "The US spends $886 billion per year on military hegemony. The only quantifiable benefit is $20-200 billion in dollar privilege." (funny because the facts are absurd, but still informative)

If a description is already funny AND informative, leave it alone. If it's funny but says nothing, rewrite it to say something.

## Process

1. Read `_quarto-manual.yml` to get the full chapter list
2. For each chapter, read frontmatter to check `scores.voice`
3. Focus on files with voice <= 5
4. Read enough content to assess
5. Make edits that are net-negative or net-neutral on word count
6. Preserve all `{{< var ... >}}` parameter references, `[@citation-key]` references, and `.qmd` cross-links exactly

## What To Replace vs. Skip

### Replace
- Dry academic openings → Wishonia observation that covers the same ground
- Redundant paragraphs that say the same thing twice → One paragraph that says it once, better
- "This paper introduces X, a mechanism design approach to Y" → What X actually does, in plain language
- "The remainder proceeds as follows: Section 2..." → Delete entirely
- "Contribution and Roadmap" → "What This Paper Does" (or just cut)
- Bloated explanations → Same information, fewer words

### Skip
- Legislative text (Right to Trial Act) — deliberately formal
- Chapters with voice 7+ — already good unless you find actual jargon
- Technical specs/protocols — brief contextual opening only, not humor throughout
- Grant proposals — fix jargon subtitles only, leave formal structure
- Mathematical definitions and proofs — keep dry
- Citations, parameter references, cross-links — never touch

## Quality Check

BEFORE: "This specification describes the Optimal Policy Generator (OPG), a framework for producing jurisdiction-specific policy recommendations from quasi-experimental evidence."

AFTER: "Thousands of jurisdictions have been running different policies for centuries. Some got richer. Some got healthier. Nobody has systematically checked which ones worked. This is like having centuries of clinical trial data in a filing cabinet and never opening the cabinet."

Same information. More memorable. The reader now understands what OPG does and why it matters, instead of just what category of academic exercise it belongs to.

## Reference Files

- Voice exemplars: `knowledge/appendix/humanity-v-government.qmd` (voice: 9), `knowledge/solution/court-of-humanity.qmd` (voice: 10)
- Style guide: `index-manual.qmd`
- Project rules: `CLAUDE.md`
- Parameter system: `_variables.yml`
