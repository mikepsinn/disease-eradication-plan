---
name: batch-review-qmd
description: Spawns parallel agents to review all paperback QMD files. Reads variable-resolved previews, flags judgment-required issues with REVIEW comments.
allowed-tools: [Read, Edit, Grep, Glob, Bash, Task]
---

# /batch-review-qmd [scope]

Scopes: *(none)* = all | `problem` `solution` `economics` `appendix` | `<file.qmd>` = single (use `/review-qmd`)

## Step 1: Generate Previews

```bash
cd E:/code/obsidian/websites/disease-eradication-plan
INDEX=$(grep "index-source:" _quarto-manual-paperback.yml | sed 's/.*: //')
CHAPTERS=$(grep -E "^\s+- knowledge/.*\.qmd" _quarto-manual-paperback.yml | sed 's/^\s*- //' | grep -v "references\.qmd" | grep -v "copyright\.qmd")
for f in $INDEX $CHAPTERS; do
  bn=$(echo "$f" | sed 's|.*/||;s|\.qmd$||')
  .venv/Scripts/python.exe scripts/preview-qmd-with-variables.py "$f" -o "_analysis/${bn}-preview.md"
done
```

## Step 2: Spawn Agents (4-5 files each, `subagent_type: "general-purpose"`)

### Agent Prompt

````
Review book chapters via variable-resolved previews. Flag ONLY judgment-required issues. Skip everything pre-render-validation.py handles (links, vars, em-dashes, images, citations, LaTeX, filler phrases).

**PROTECT THE JOKES.** This book uses deadpan, sarcastic humor to deliver serious policy arguments. The tone is a feature. Never flag humor as unprofessional. Fix errors while preserving the voice: "update the punchline" not "replace with neutral statement."

## Files: [LIST: file.qmd -> _analysis/basename-preview.md]

## Process
1. Read preview (rendered text) -> 2. Read raw QMD -> 3. Add `<!-- REVIEW: CATEGORY description + fix -->` ABOVE problematic lines

## Error Categories

| Category | Flag when... |
|----------|-------------|
| WRONG_VALUE | Rendered number contradicts prose (approx OK; order-of-magnitude mismatch not OK) |
| UNIT_DUPLICATION | Variable includes unit + prose repeats: "$27.2B dollars", "55M deaths deaths" |
| MISSING_NOUNIT | Variable unit clashes with prose: "55.0 million of deaths annual deaths" |
| MATH_ERROR | Arithmetic wrong, percentages don't sum, stated ratio doesn't match numbers |
| CONTRADICTION | File says X here, not-X there |
| GARBLED_TEXT | Nonsensical after variable substitution |
| LOGIC_ERROR | Argument doesn't follow, false equivalence, single case proves universal claim |
| FACTUAL_ERROR | Verifiably wrong (only when confident) |
| WEAK_CLAIM | Smart audiobook listener would think "that's obviously wrong/naive/easily refuted" |
| STALE_COMPARISON | Reference point no longer matches variable value |
| REDUNDANT | Same point twice in different words, same stat in two sections (callbacks/running gags are fine) |

## Quality Flags (sparingly, clear wins only)

| Category | Flag when... |
|----------|-------------|
| PACING | Number dump without breather; listener would zone out |
| BURIED_LEDE | Strongest claim buried mid-paragraph instead of leading |
| UNEARNED_CONCLUSION | "Therefore" not supported by preceding evidence |
| MISSING_STEELMAN | Obvious counterargument unaddressed; skeptics will notice |

## DO NOT flag
- Pre-render-validation.py territory (links, vars, em-dashes, citations, LaTeX, bad contexts)
- Approximate values, YAML frontmatter, image alt text, hardcoded cited stats
- The sarcastic tone, deliberate hyperbole ("your species", "longer than the universe")
- Style preferences

## Report: files reviewed, comments per file, serious issues.
````

## Step 3: Collect

```bash
grep -rn "<!-- REVIEW:" --include="*.qmd" knowledge/ index-manual.qmd | wc -l
grep -rn "<!-- REVIEW:" --include="*.qmd" knowledge/ index-manual.qmd | sed 's/.*REVIEW: \([A-Z_]*\).*/\1/' | sort | uniq -c | sort -rn
```

## Step 4: Fix Phase (Optional)

Spawn agents to fix each `<!-- REVIEW: -->` and remove it. **Fix the error, keep the joke.**
