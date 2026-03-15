---
name: wishonia-style
description: Rewrite or review QMD content for Wishonia's naive alien voice. Analyzes comedy mechanics from index-manual.qmd gold standard, identifies where voice falls flat, and rewrites with proper technique.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Write
---

# /wishonia-voice <file.qmd>

Rewrite or review a QMD file to use Wishonia's childlike alien voice consistently. Gold standard: `index-manual.qmd`.

## Usage
```
/wishonia-voice knowledge/appendix/faq.qmd
/wishonia-voice knowledge/strategy/roadmap.qmd
```
If no file specified, ask which file to review.

---

## Who Is Wishonia?

A naive alien AI who has been watching Earth for 4,297 years and is genuinely confused by human behavior. NOT a comedian. NOT a debater. NOT a consultant wearing an alien costume. Wishonia states observations and they happen to be devastating because the truth is absurd.

**Closest human equivalents:** Philomena Cunk's confused literalism, Douglas Adams' deadpan absurdity, Kurt Vonnegut's tired sadness.

---

## The 7 Comedy Mechanics

These are reverse-engineered from index-manual.qmd. Every funny line in that file uses one or more of these. If your rewrite isn't funny, check which mechanic you forgot.

### 1. Jokes Are SHORT (5-15 words)

The funniest lines are throwaway one-liners, not paragraphs.

| Works | Doesn't Work |
|-------|-------------|
| "You named your planet dirt." | "Your species chose to name your planet 'Earth,' which in your language means dirt, which I find fascinating." |
| "This was very human of you." | "This behavior is characteristic of your species' tendency to do the opposite of what makes sense." |
| "Rocks do it every day." | "Even geological formations have managed to achieve this, which puts your species' efforts in perspective." |

**Rule: If the joke needs more than 2 sentences of setup, it's not worth it.**

### 2. Describe, Don't Argue

Wishonia doesn't make counter-arguments. Wishonia describes what humans do, and the description IS the argument. The reader draws the conclusion.

| Works | Doesn't Work |
|-------|-------------|
| "You give these nothing-papers to weapons makers. They make things that destroy everything. This creates 'jobs.'" | "I find your economic system fascinating. You've created a system where..." |
| "Your Department of Defense mainly just attacks people." | "Let me explain why your Department of Defense is misnamed..." |
| "Investment, which is gambling but wearing a suit." | "This is essentially the same as gambling, except your species has made it socially acceptable by requiring formal attire." |

**Rule: If Wishonia says "let me explain" or "I find this fascinating," delete it and just STATE the thing.**

### 3. The Parenthetical Undercut

Short asides in parentheses that land harder than the main sentence. These are index-manual.qmd's secret weapon.

**Examples from gold standard:**
- "(just in case the first 12 apocalypses don't take)"
- "(as a bonus)"
- "(this is correct)"
- "(they're very greedy)"
- "(to fight the zero aliens attacking you)"
- "(that's 'illegal')"
- "(barely beat inflation)"
- "(probably)"

**Rule: Parentheticals should be 2-8 words. If it's longer, it's not a parenthetical, it's a sentence pretending to be one.**

### 4. The Deadpan Definition

Redefine a human concept in its most literal, absurd terms. Delivered flat, no wink.

**Examples from gold standard:**
- "money, which is pretend value that becomes real value if everyone pretends hard enough"
- "Investment, which is gambling but wearing a suit"
- "Marketing, which is lying but with graphics"
- "Super PACs, which are like normal PACs but super"

**Template: "[Human word], which is [absurd but accurate literal description]."**

### 5. Structure IS the Joke

Use bullet lists, numbered lists, and comparison tables as comedy delivery devices. The format being serious while the content is absurd creates the gap.

**Examples from gold standard:**

The WITH/WITHOUT papers lists:
```
Without these papers, you won't:
- Save lives (requires many papers)
- Cure diseases (requires very many papers)

But WITH these papers, you will:
- Build bombs (you love giving papers for this)
- Start wars (somehow this makes more papers)
```

The Year 1-20 progression:
```
- Year 1: Move 1% of murder money to medicine money (baby steps)
- Year 5: "Remember when we spent money on bombs? That was weird."
- Year 20: "We used to WHAT?!"
```

**Rule: If you're writing 3+ similar points in prose, convert to a list. The list format does the comedy work for you.**

### 6. The Specific Absurd Noun

Don't use generic words. Invent a phrase that is technically accurate and absurd.

| Generic (not funny) | Specific (funny) |
|---------------------|-----------------|
| weapons | murder tubes that cost more than countries |
| nuclear warheads | enough to end civilization 13 times |
| slow safety system | smoke detector that works by mail |
| lobbying | money laundering but backwards and legal |
| military budget | murder money |
| the economy | a system where food grows for free but you need papers to eat it |

**Rule: If you can replace a noun with a phrase that is MORE accurate AND more absurd, always do it.**

### 7. The Childlike "Papers" Framework

Money = "small pieces of paper with presidents on them" = "papers." This is NOT just a synonym. It's a lens that makes every financial transaction sound absurd.

- "give them papers" not "fund them"
- "more papers" not "higher returns"
- "papers go to" not "funding flows to"
- "very many papers" not "significant investment"

**Use "papers" in at least 30% of money references. Don't use it in every single one (that gets tiresome). Alternate with "money" and specific dollar amounts.**

---

## Common Failures (and Fixes)

### Failure: Wishonia Announces the Joke
```
BAD:  "I find your legal system endlessly fascinating."
BAD:  "This is my favorite objection."
BAD:  "Let me make sure I understand this one."
GOOD: Just state the absurd thing. No preamble.
```

### Failure: Wishonia Lectures
```
BAD:  "Your species invented countries, which are imaginary lines on dirt
       that you kill each other over. Then you invented 'sovereignty,'
       which means each imaginary line gets to decide how to waste its
       own papers. Now a human is worried that..."
GOOD: "You drew lines on dirt and now you're worried that voluntarily
       buying fewer missiles violates the dirt lines."
```

### Failure: Wishonia Delivers Speeches
```
BAD:  3-paragraph Wishonia monologue about human nature
GOOD: 1-2 sentences of observation, then get to the point
```

### Failure: Missing the Landing
If a section has good arguments but isn't funny, add:
1. One parenthetical undercut
2. One deadpan definition
3. One specific absurd noun
That's usually enough.

---

## Process

### Phase 1: Read the File
Read the target file. Identify sections that:
- Sound like a debater, not an alien
- Have Wishonia explaining/arguing instead of describing
- Lack parenthetical undercuts
- Use generic nouns where specific absurd ones would work
- Are too long (Wishonia paragraphs should rarely exceed 3 sentences)
- Miss opportunities for structure jokes (lists, comparisons)

### Phase 2: Read the Gold Standard
Read `index-manual.qmd` lines 19-160 to recalibrate the voice. Note the rhythm: short line, observation, parenthetical, move on.

### Phase 3: Rewrite
For each weak section:
1. Cut first. Most sections are too long.
2. Find the one observation that makes the point. State it flat.
3. Add one parenthetical undercut.
4. Replace generic nouns with specific absurd ones.
5. Check: would this fit in index-manual.qmd? If not, cut more.

### Phase 4: Self-Check
Read each rewrite and ask:
- **Is Wishonia performing or observing?** (Must be observing)
- **Could I cut this in half?** (Probably yes)
- **Does it have at least one parenthetical?** (Should)
- **Would the reader laugh or just nod?** (Must laugh)
- **Is there a structure joke opportunity I'm missing?** (Lists, comparisons)

---

## What NOT to Change

- Factual content, citations, and variables
- Arguments that are already strong and funny
- Section headers and image references
- Content that's deliberately straight-faced for credibility (some sections need to be serious)
- Running gags that work across chapters

---

## The Ultimate Test

Read your rewrite aloud. Does it sound like:
- A confused alien stating observations? **GOOD**
- A comedian doing an alien bit? **BAD**
- A policy analyst with some jokes sprinkled in? **BAD**
- A debater wearing an alien costume? **BAD**

The comedy comes from the GAP between Wishonia's naive tone and the devastating truth of the observation. If Wishonia sounds self-aware, the gap closes and the comedy dies.
