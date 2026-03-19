---
name: batch-voice-rewrite
description: Aggressively rewrites all book chapters into Wishonia's naive alien voice. Spawns parallel agents that identify and replace LinkedIn slop, consultant-speak, and flat prose with deadpan comedy. Skips papers, references, and files with already-excellent voice.
allowed-tools: [Read, Edit, Grep, Glob, Bash, Agent, Task]
---

# /batch-voice-rewrite [scope]

Scopes: *(none)* = all chapters | `problem` `solution` `proof` `plan` `economics` | `<file.qmd>` = single (use `/wishonia-style`)

## Step 0: Identify Target Files

Extract chapter QMD files from `_quarto-manual.yml`. **EXCLUDE:**

```
# Gold standard (don't rewrite the reference)
index-manual.qmd

# Already excellent voice
knowledge/economics/central-banks.qmd
knowledge/problem/genetic-slavery.qmd
knowledge/solution/ai-coordination-army.qmd
knowledge/appendix/recruitment-and-propaganda-plan.qmd

# Academic papers (correct tone for papers)
knowledge/economics/1-pct-treaty-impact.qmd
knowledge/appendix/dfda-impact-paper.qmd
knowledge/appendix/incentive-alignment-bonds-paper.qmd
knowledge/appendix/wishocracy-paper.qmd
knowledge/appendix/political-dysfunction-tax.qmd
knowledge/appendix/invisible-graveyard.qmd
knowledge/appendix/cost-of-change-analysis.qmd
knowledge/appendix/us-efficiency-audit.qmd
knowledge/appendix/optimocracy-paper.qmd
knowledge/appendix/optimal-policy-generator-spec.qmd
knowledge/strategy/earth-optimization-prize.qmd
knowledge/appendix/optimal-budget-generator-spec.qmd
knowledge/appendix/dfda-spec-paper.qmd
knowledge/appendix/earth-optimization-prize-protocol.qmd
knowledge/appendix/right-to-trial-fda-upgrade-act.qmd
knowledge/appendix/drug-development-cost-analysis.qmd

# Reference/meta (not narrative)
knowledge/references.qmd
knowledge/about.md
knowledge/appendix/copyright.qmd
knowledge/appendix/back-cover.qmd
knowledge/papers.qmd
knowledge/links.qmd
knowledge/podcast.qmd
knowledge/appendix/parameters-and-calculations.qmd

# Institutional (formal tone correct)
knowledge/strategy/initiating-node-brief.qmd
knowledge/strategy/initiating-node-memo.qmd
knowledge/grant-proposal/earth-optimization-prize-90-day-pilot.qmd
knowledge/strategy/institution-outreach-email.qmd
```

If a scope is given (e.g., `problem`), filter to files in that part only.

## Step 1: Read Gold Standard

Every agent MUST read `index-manual.qmd` lines 19-160 before starting. This calibrates the voice. Note the rhythm: short line, observation, parenthetical, move on.

## Step 2: Spawn Parallel Agents (6-8 files each)

Split remaining files into batches of 6-8. Spawn one agent per batch using `subagent_type: "general-purpose"`.

### Agent Prompt Template

````
You are rewriting book chapters into Wishonia's naive alien voice. This is an AGGRESSIVE rewrite. If it sounds like LinkedIn, a consultant, a debater, or a policy analyst, rewrite it.

## Your Files
[LIST OF 6-8 FILES]

## The Voice

Wishonia is a naive alien AI who has watched Earth for 4,297 years. NOT a comedian, NOT a debater, NOT a consultant wearing an alien costume. Wishonia states observations and they happen to be devastating because the truth is absurd.

**Closest equivalents:** Philomena Cunk's confused literalism, Douglas Adams' deadpan absurdity, Kurt Vonnegut's tired sadness.

## The 7 Comedy Mechanics

### 1. Jokes Are SHORT (5-15 words)
| Works | Doesn't Work |
|-------|-------------|
| "You named your planet dirt." | "Your species chose to name your planet 'Earth,' which in your language means dirt." |
| "This was very human of you." | "This behavior is characteristic of your species' tendency to do the opposite of what makes sense." |

### 2. Describe, Don't Argue
Wishonia doesn't make counter-arguments. Wishonia DESCRIBES what humans do, and the description IS the argument.
| Works | Doesn't Work |
|-------|-------------|
| "Your Department of Defense mainly just attacks people." | "Let me explain why your Department of Defense is misnamed..." |
| "Investment, which is gambling but wearing a suit." | "This is essentially the same as gambling, except your species has made it socially acceptable." |

### 3. The Parenthetical Undercut
Short asides in parentheses: "(just in case the first 12 apocalypses don't take)", "(barely beat inflation)", "(probably)", "(this is correct)"
**2-8 words only.**

### 4. The Deadpan Definition
"money, which is pretend value that becomes real value if everyone pretends hard enough"
"Marketing, which is lying but with graphics"
**Template: "[Human word], which is [absurd but accurate literal description]."**

### 5. Structure IS the Joke
Use bullet lists and tables as comedy delivery. The serious format + absurd content creates the gap.

### 6. The Specific Absurd Noun
| Generic (not funny) | Specific (funny) |
|---------------------|-----------------|
| weapons | murder tubes that cost more than countries |
| lobbying | money laundering but backwards and legal |
| military budget | murder money |

### 7. The "Papers" Framework
Money = "papers" in at least 30% of money references. "give them papers" not "fund them". Alternate with "money" and dollar amounts.

## LinkedIn Slop Detector

REWRITE any line that contains:
- "leverage", "synergy", "stakeholder", "operationalize", "ecosystem", "paradigm shift"
- "Let me explain...", "I find this fascinating...", "This is my favorite..."
- 3+ sentence Wishonia monologues (cut to 1-2 sentences)
- Generic nouns where specific absurd ones would work
- Arguments instead of observations
- Missing parenthetical undercuts (add at least 1 per section)
- Passive voice ("it has been observed" -> state the thing)
- Hedge words ("perhaps", "it could be argued", "one might say")
- Consultant framing ("value proposition", "key takeaway", "actionable insight")
- Speeches about human nature (Wishonia observes, doesn't philosophize)
- Any sentence that could appear in a TED talk without getting a laugh

## What NOT to Change
- Factual content, statistics, citations, and `{{< var >}}` variables
- Section headers (h2, h3) and YAML frontmatter
- Image references, callout blocks, cross-references
- Content that's deliberately straight-faced for credibility
- Running gags that work across chapters
- Tables of data/numbers
- Legal/technical sections that need precision

## Process for Each File
1. Read the file completely
2. Identify every paragraph that sounds like LinkedIn/consultant/debater
3. Rewrite using the 7 mechanics. When in doubt, make it shorter.
4. Self-check each rewrite:
   - Is Wishonia OBSERVING or PERFORMING? (Must be observing)
   - Could I cut this in half? (Probably yes)
   - Does it have at least one parenthetical? (Should)
   - Would the reader laugh or just nod? (Must laugh)
5. Apply edits using the Edit tool. Make targeted edits, not full file rewrites.
6. After all edits, re-read each file to verify variables and citations are intact.

## The Ultimate Test
Read your rewrite aloud. Does it sound like:
- A confused alien stating observations? GOOD
- A comedian doing an alien bit? BAD
- A policy analyst with some jokes sprinkled in? BAD
- A debater wearing an alien costume? BAD

The comedy comes from the GAP between Wishonia's naive tone and the devastating truth. If Wishonia sounds self-aware, the gap closes and the comedy dies.

## Report
After finishing all files, list:
- Files processed
- Number of sections rewritten per file
- Best new line you wrote (for quality check)
- Any sections you left untouched and why
````

## Step 3: Collect Results

After all agents complete, run:

```bash
cd E:/code/obsidian/websites/disease-eradication-plan
git diff --stat
git diff --word-diff knowledge/ index-manual.qmd | head -200
```

Review the diff summary. Flag any files where variables or citations may have been damaged:

```bash
# Check no variables were broken
grep -rn '{{<' knowledge/ --include="*.qmd" | grep -v 'var ' | grep -v 'include ' | head -20
# Check no citations were broken
grep -rn '\[@' knowledge/ --include="*.qmd" | grep -v '\[@[a-zA-Z]' | head -20
```

## Step 4: Quality Spot-Check

Read 3 random rewritten files and verify:
1. Voice is consistent with index-manual.qmd
2. No facts were changed
3. Variables render correctly
4. At least one laugh per page
