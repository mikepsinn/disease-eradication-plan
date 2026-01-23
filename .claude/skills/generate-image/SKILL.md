---
name: generate-image
description: Generate AI images using Gemini. Interactively asks for prompt and options, then generates and saves the image.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Glob
  - Edit
---

# /generate-image [prompt]

Generate AI images using Gemini with interactive option selection.

## Usage
```
/generate-image
/generate-image "A diagram showing the treaty adoption process"
```

---

## Step 1: Gather Context

**Read source files for available options:**
- `scripts/images/generate-image.ts` → `ImageTypes`, `AspectRatios`
- `scripts/lib/image-prompts.ts` → `VisualStyles`

**Determine target QMD file** (priority order):
1. Explicit file reference (e.g., `@knowledge/appendix/file.qmd`)
2. Current conversation context
3. Git status: `git diff --name-only HEAD~3 | grep "\.qmd$" | head -1`

**Derive output folder from QMD filename:**
- `knowledge/problem/regulatory-capture.qmd` → `assets/images/regulatory-capture/`
- `knowledge/appendix/invisible-graveyard.qmd` → `assets/images/invisible-graveyard/`
- No target file → `assets/images/generated/` (fallback)

**For charts**, get actual numbers:
```bash
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file.qmd> --numbers-only
```

**IMPORTANT: Include confidence intervals when available.** The preview output shows values with 95% CIs in format `X (95% CI: Y-Z)`. Always include these uncertainty ranges in chart prompts - request error bars or uncertainty visualization.

---

## Step 2: Ask User for Options

Use AskUserQuestion. Order options by inferred likelihood, putting recommended choice first with "(Recommended)" suffix.

**Inference heuristics:**

| Context Signal | Suggested Type |
|----------------|----------------|
| Economics files, data, costs, comparisons | `chart` |
| Process, workflow, pipeline, stages | `diagram` |
| Concepts, vision, metaphor | `illustration` |
| Marketing, propaganda | `figure` + retro-futuristic style |
| General/unclear | `figure` |

**Aspect ratio hints:** QMD chapters → `16:9`, Social media → `1:1`

---

## Step 3: Build Prompt and Confirm

**Extract comprehensive context from the QMD file** (with variables resolved). Include enough surrounding text for the image generator to understand the full concept.

**Do NOT prescribe specific layouts** (e.g., "left bar should be X, right bar should be Y"). Provide the content and let the generator be creative.

**Minimum context to include:**
1. **Title/topic** of the section or chapter
2. **The specific data/comparison** being illustrated (with actual numbers)
3. **The key insight or takeaway** (why this matters)
4. **Surrounding context** that helps explain the significance

**Run preview script with broad line range** (e.g., 30-50 lines) to capture full context:
```bash
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file.qmd> --line-range "X-Y"
```

For charts:
- Append "Linear scale." to the prompt
- **Include error bars** if confidence intervals are available (e.g., "Show error bars for 95% confidence intervals: X ranges from Y to Z")

### Confirmation (MANDATORY)

**NEVER generate without showing the prompt and getting explicit user confirmation.** This applies to initial generation AND regeneration/edits.

Present the full prompt in a code block:
```
Prompt: [full prompt text]
Type: [type]
Aspect: [aspect]
Style: [style]
Alt text: [alt]
```

Use AskUserQuestion to confirm: "Generate with this prompt?" with options:
- "Yes, generate"
- "Edit prompt"
- "Cancel"

**Do NOT proceed to Step 4 until user confirms.**

---

## Step 4: Run Generation

After user confirms:
```bash
npx tsx scripts/images/generate-image.ts '<prompt>' \
  --type <type> --aspect <aspect> --style <style> --alt '<alt_text>' \
  --output 'assets/images/<qmd-basename>/'
```

**Examples:**
- Target: `regulatory-capture.qmd` → `--output 'assets/images/regulatory-capture/'`
- Target: `invisible-graveyard.qmd` → `--output 'assets/images/invisible-graveyard/'`
- No target → `--output 'assets/images/generated/'`

**IMPORTANT: Use single quotes** around prompt and alt text to prevent bash from interpreting `$` as variable expansion (e.g., `$8 trillion` would break with double quotes).

---

## Step 5: Insert at Optimal Location

**Insert where the content is discussed, NOT at the end.**

1. Search QMD file for the section discussing the image's subject
2. Insert image markdown immediately AFTER the relevant paragraph

| Image Subject | Insert After |
|---------------|--------------|
| Data/statistics | Paragraph presenting those numbers |
| Process/workflow | Section heading introducing the process |
| Comparison | Paragraph setting up the comparison |

**Use Edit tool** with correct relative path from QMD to `assets/images/<qmd-basename>/`.

---

## Step 6: Report Result

Report: image file path, where inserted, remind user to preview.

---

## Environment

Requires `GOOGLE_GENERATIVE_AI_API_KEY` environment variable.
