---
name: score-chapters
description: Score H2EWD manual chapters on quality, value, timeliness, standalone, and voice. Reads full files, uses calibrated anchors, writes scores to frontmatter, and regenerates the search index.
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

# /score-chapters [file-or-pattern]

Score one or more QMD chapters on 5 dimensions and write scores to frontmatter.

## Usage
```
/score-chapters knowledge/strategy/earth-optimization-prize.qmd
/score-chapters knowledge/problem/*.qmd
/score-chapters all          # score all chapters in _quarto-manual.yml
```

## Scoring Dimensions (1-10 each)

### quality
Rigor, analytical depth, and clarity. Rigor can come from EITHER empirical analysis OR mechanism design — both count equally.

**Empirical rigor** (e.g. 1-pct-treaty-impact): formal methodology, Monte Carlo, peer-reviewed sources, explicit limitations, uncertainty quantification.

**Mechanism design rigor** (e.g. earth-optimization-prize, incentive-alignment-bonds): well-specified rules, game-theoretic reasoning, worked examples with concrete numbers, failure mode analysis, comparison to alternatives, addresses objections.

- **10**: Rigorous by the standards of its genre — whether empirical paper, mechanism design, policy proposal, or investigative analysis
- **7**: Good writing and data/reasoning, well-sourced, but not groundbreaking rigor
- **4**: Thin, unsourced, presents complex problems as trivially solved

### value
Three components, scored together:

1. **Novel contribution**: Does this introduce an original framework, finding, or mechanism that doesn't exist elsewhere?
2. **Expected impact**: If this idea gets implemented, how much changes? A mechanism that could redirect $27B/year or prevent 10B deaths scores higher than a clever observation about a known problem.
3. **Actionability**: Does the reader leave with something to DO? A chapter with a worked financial model, a specific ask, or a concrete next step scores higher than analysis that ends at "this is bad."

- **10**: Novel mechanism or finding + massive expected impact + clear path to action (e.g. earth-optimization-prize: novel PRIZE/VOTE design + $27B redirect + "vote and recruit 2 people")
- **8-9**: Strong on 2 of 3 components
- **7**: Important topic, well-presented, but builds on familiar territory OR lacks actionability
- **4**: Restates common talking points, no novel contribution, nothing to do with it

### timeliness
Relevance today.
- **10**: Timeless mechanisms that will be relevant in 50 years, OR uses current 2024-2026 data
- **7**: Mostly timeless with some dated references
- **3**: Heavily dependent on current political figures, events, or data that will age

### standalone
Can a new reader landing on this page — with NO prior reading of the book — understand the argument, get value from it, and potentially use it as an entry point to the broader work?

**What standalone measures:**
- Does the piece provide enough context for its own arguments?
- Could you share this link to someone unfamiliar with H2EWD and they'd get it?
- Is it a reasonable entry point that might draw someone into the rest of the book?

**What standalone does NOT penalize:**
- Linking to other chapters (links ADD value by offering depth, they don't subtract)
- Referencing concepts from other chapters IF the piece explains them inline
- Being part of a series, as long as this installment works on its own

**What DOES indicate low standalone:**
- Opening with "You've seen the numbers" or "As we discussed" (assumes prior reading)
- Arguments that depend on concepts only explained elsewhere without inline summary
- Hub/overview pages that are just lists of links to other chapters
- Pieces that say "this book" as if the reader is already committed to reading it
- Calculator widgets or templates with no prose argument

**Scale:**
- **10**: Fully self-contained research paper (e.g. 1-pct-treaty-impact.qmd)
- **8**: Works alone, explains its own concepts, good entry point to the book
- **6**: Mostly works alone but assumes some familiarity with the project
- **4**: References "this book" or prior chapters heavily, limited cold-reader value
- **2**: Pure navigation page, template, or connective tissue

### voice
How well does the writing match the H2EWD signature style?

**The gold standard is `index-manual.qmd`**: an alien anthropologist observing human absurdity with dark humor that carries rigorous arguments. Every joke makes a point. The comedy comes from the GAP between naive tone and devastating truth.

**Key voice mechanics** (from the wishonia-style skill):
1. Jokes are SHORT (5-15 words)
2. Describe, don't argue — the description IS the argument
3. Parenthetical undercuts: "(this is correct)", "(probably)"
4. Deadpan definitions: "investment, which is gambling but wearing a suit"
5. Structure IS the joke — bullet lists and tables as comedy devices
6. Specific absurd nouns: "murder tubes" not "weapons"
7. The "papers" framework for money

**Scale:**
- **10**: Index-manual level — every section has structural humor that carries arguments (only Moronia achieves this in the chapters)
- **8**: Strong voice throughout, multiple comedy mechanics per section
- **6**: Has moments of wit but inconsistent, some flat sections
- **4**: Dry academic/spec tone (acceptable for formal papers)
- **2**: Template or boilerplate with no voice

**Note:** Academic papers (1-pct-treaty-impact, dfda-spec, invisible-graveyard) SHOULD have lower voice scores. That's correct for their format. Voice measures entertainment value, not quality.

## Anchors

Before scoring, read these calibration files:

1. **`index-manual.qmd`** — Voice=10, the gold standard style reference. Read lines 19-300.
2. **`knowledge/economics/1-pct-treaty-impact.qmd`** — Quality=10, Value=10, Timeliness=9, Standalone=10, Voice=5. Read first 300 lines.
3. **`knowledge/problem/genetic-slavery.qmd`** — Quality=7, Value=7, Timeliness=8, Standalone=7, Voice=6. Mid-tier anchor.
4. **`knowledge/solution/decentralized-census-bureau.qmd`** — Quality=4, Value=4, Timeliness=5, Standalone=5, Voice=4. Low-tier anchor.

## CRITICAL: Resolve Variables Before Scoring

QMD files contain Quarto variable shortcodes like `{{< var military_to_government_clinical_trials_spending_ratio >}}` that render as actual values (e.g., "604"). **Agents MUST read the variable-resolved version**, not the raw QMD, because:
- Numbers carry the emotional and analytical punch ("604 times more" vs opaque variable names)
- Voice/humor depends on specific numbers landing
- Files look artificially dependent on external systems when full of unresolved variables
- Quality assessment requires seeing the actual data

**To generate a preview with resolved variables:**
```bash
cd E:/code/disease-eradication-plan
python scripts/preview-qmd-with-variables.py <file.qmd>
# Or save to a temp file for agent consumption:
python scripts/preview-qmd-with-variables.py <file.qmd> -o /tmp/preview.md
```

For batch scoring, generate previews for all files into a temp directory:
```bash
mkdir -p /tmp/h2ewd-previews
for f in knowledge/problem/*.qmd knowledge/solution/*.qmd ...; do
  python scripts/preview-qmd-with-variables.py "$f" -o "/tmp/h2ewd-previews/$(echo $f | tr '/' '-')"
done
```

Then tell agents to read from `/tmp/h2ewd-previews/` instead of the raw QMD files.

**Scores are written to the ORIGINAL .qmd frontmatter**, not to the preview files.

## Process

### For a single file:
1. Read the anchor files to calibrate (use previews for anchors too)
2. Generate a variable-resolved preview: `python scripts/preview-qmd-with-variables.py <file> -o /tmp/preview.md`
3. Read the ENTIRE preview (use multiple Read calls with offset if needed for files over 300 lines)
4. Score on all 5 dimensions
5. Write scores to the `scores:` block in the ORIGINAL .qmd frontmatter using Edit
6. Regenerate the search index: `cd E:/code/disease-eradication-plan && python -c "from dih_models.search_index_generator import SearchIndexGenerator; from pathlib import Path; SearchIndexGenerator(Path('.')).generate_chat_index()"`

### For batch scoring (multiple files or "all"):
1. Generate variable-resolved previews for all target files and anchors
2. Read the anchor previews once
3. Spawn up to 3 Agent subagents in parallel, each handling a batch of files
4. **CRITICAL**: Tell agents to read ENTIRE preview files using multiple Read calls with offset/limit for files over 300 lines. Long files (400+ lines) are often the BEST content and get systematically underscored when agents only read the beginning.
5. Collect scores from agents
6. Apply scores to ORIGINAL .qmd frontmatter via a script
7. Regenerate search index once at the end

### Agent prompt template for batch scoring:
Include in every agent prompt:
- The full anchor descriptions and scores
- The full rubric for all 5 dimensions (copy from above)
- The list of preview files to score (in /tmp/h2ewd-previews/)
- "Read ENTIRE files. For files over 300 lines, use multiple Read calls with offset. DO NOT skim or stop early — long files often contain the best content in the second half."
- "Output JSON only, no justifications"

### importance
How critical is this piece to the H2EWD system actually working? This is NOT about writing quality — a dry spec that defines a critical subsystem scores higher than a beautifully written tangent.

- **10**: Core engine — nothing works without this (1% Treaty, Earth Optimization Prize, IABs, dFDA)
- **8-9**: Critical mechanism or key argument that drives adoption (Wishocracy, Optimocracy, cost-of-war, invisible-graveyard, aligning-incentives)
- **6-7**: Important supporting content (proof chapters, economic analyses, feasibility studies)
- **4-5**: Supplementary (thin governance sketches, supporting appendices)
- **2-3**: Operational artifacts (templates, email drafts)

## Frontmatter Format

```yaml
scores:
  quality: 8
  value: 9
  timeliness: 9
  standalone: 7
  voice: 9
  importance: 10
```

## After Scoring

Regenerate the search index so scores flow through to `search-index.json`:
```bash
cd E:/code/disease-eradication-plan
python -c "from dih_models.search_index_generator import SearchIndexGenerator; from pathlib import Path; SearchIndexGenerator(Path('.')).generate_chat_index()"
```

If scoring for TBN integration, also clear the eleventy-fetch cache in think-by-numbers-static:
```bash
cd E:/code/think-by-numbers-static
rm -f .cache/eleventy-fetch-*
```
