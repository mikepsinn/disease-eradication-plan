---
name: generate-image
description: Generate AI images using Gemini. Interactively asks for prompt and options, then generates and saves the image.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Glob
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

Before asking questions, gather context to infer likely choices:

### 1. Check Git Status (REQUIRED)

Run this first to see what the user has been working on:

```bash
git status --short
git diff --name-only HEAD~3
```

This reveals:
- Recently modified files → topic/domain
- Staged changes → current focus
- File paths → `knowledge/economics/` suggests charts, `knowledge/appendix/` suggests diagrams

### 2. Read Recent Files for Keywords

If git shows modified QMD files, read their titles/frontmatter:

```bash
# Get titles of recently modified QMD files
git diff --name-only HEAD~3 | grep "\.qmd$" | head -3
```

Then read those files to extract:
- `title:` from frontmatter
- Section headings
- Key terms that suggest image types

### 3. Check Recent Conversation

What topic is being discussed? What was just asked about?

### 4. Infer Image Type from Context

| Signal | Suggested Type |
|--------|----------------|
| Working on economics files | `chart` |
| Working on process/implementation files | `diagram` |
| Working on overview/intro files | `illustration` |
| Discussing workflows, pipelines | `diagram` |
| Discussing data, costs, comparisons | `chart` |
| Discussing concepts, vision | `illustration` |
| General/unclear | `figure` |

### 5. Infer Style from Project

| Signal | Suggested Style |
|--------|-----------------|
| `knowledge/` files | `academic` |
| Marketing/campaign content | `retro` |
| Website landing pages | `modern` |
| Default for this book | `academic` |

---

## Step 2: Get Prompt

If no prompt provided, ask with context-inferred suggestions first:

```
AskUserQuestion:
  question: "What image do you want to generate?"
  header: "Prompt"
  options:
    # Order by likelihood based on context!
    # If discussing a process → put diagram first
    # If discussing data → put chart first
    - label: "<inferred best match>"
      description: "Based on current context: [reason]"
    - label: "Diagram/flowchart"
      description: "Process flows, system architecture, decision trees"
    - label: "Data visualization"
      description: "Charts, graphs, comparisons"
    - label: "Conceptual illustration"
      description: "Abstract concepts, metaphors, themes"
    # "Other" is automatically available
```

**Context inference examples:**
- User just edited `knowledge/economics/*.qmd` → suggest "chart" showing economic data
- Discussing "treaty adoption process" → suggest "diagram" of adoption steps
- Working on landing page → suggest "illustration" for hero image

---

## Step 3: Ask Options (Context-Ordered)

Use AskUserQuestion with options ordered by inferred likelihood.

### Image Type
Reorder based on prompt content:
- Contains "flow", "process", "steps" → `diagram` first
- Contains "data", "comparison", "cost" → `chart` first
- Contains "concept", "idea", "metaphor" → `illustration` first

```
question: "What type of image?"
header: "Type"
options:
  # Put inferred best match first with "(Recommended)" suffix
  - label: "<inferred> (Recommended)"
    description: "<why this matches context>"
  - label: "figure"
    description: "General figure illustration"
  - label: "diagram"
    description: "Diagram with labeled components"
  - label: "chart"
    description: "Data visualization or chart"
  # Other always available via AskUserQuestion
```

### Aspect Ratio
Infer from intended use:
- QMD chapter content → `16:9` (standard figures)
- Social media mentioned → `1:1`
- Slides/presentations → `16:9`
- Document/PDF → `4:3`

```
question: "What aspect ratio?"
header: "Aspect"
options:
  - label: "16:9 (Recommended)"
    description: "Widescreen - inferred from [context]"
  - label: "1:1"
    description: "Square, good for social media"
  - label: "4:3"
    description: "Standard, good for documents"
```

### Visual Style
Infer from file location or topic:
- `knowledge/` files → `academic`
- Marketing content → `retro`
- Website assets → `modern`

```
question: "What visual style?"
header: "Style"
options:
  - label: "academic (Recommended)"
    description: "Clean, professional - matches book style"
  - label: "retro"
    description: "Vintage propaganda poster aesthetic"
  - label: "modern"
    description: "Contemporary minimalist design"
```

### Target File
Use git to find the most recently modified QMD file:

```bash
# Find most recently modified QMD file
git diff --name-only | grep "\.qmd$" | head -1
# Or from recent commits
git diff --name-only HEAD~3 | grep "\.qmd$" | head -1
```

Offer that file as the default:

```
question: "Insert into a file?"
header: "Insert"
options:
  - label: "Insert into <git_recent_file.qmd> (Recommended)"
    description: "Most recently modified QMD file"
  - label: "No, just generate"
    description: "I'll copy the markdown myself"
  - label: "Different file..."
    description: "Specify another QMD file"
```

---

## Step 4: Build and Run Command

Construct the command from collected options:

```bash
cd E:/code/obsidian/websites/disease-eradication-plan
npx tsx scripts/images/generate-image.ts "<prompt>" \
  --type <type> \
  --aspect <aspect> \
  --style <style> \
  [--file <qmd_path>] \
  [--alt "<alt_text>"]
```

**Examples:**

Basic generation:
```bash
npx tsx scripts/images/generate-image.ts "Treaty adoption flowchart showing nation-by-nation process" --type diagram --aspect 16:9 --style academic
```

With auto-insert:
```bash
npx tsx scripts/images/generate-image.ts "Cost comparison bar chart" --type chart --aspect 16:9 --style academic --file knowledge/economics/1-pct-treaty-impact.qmd --alt "Bar chart comparing intervention costs"
```

---

## Step 5: Report Result

After successful generation, report:

```markdown
## Image Generated

**File:** `assets/images/generated/<filename>.png`

**Markdown to insert:**
```
![<alt_text>](/<path>)
```

**Preview the image** to verify it matches expectations.
```

If `--file` was used, confirm insertion location.

---

## Context Inference Heuristics

| Context Signal | Inferred Type | Inferred Style |
|----------------|---------------|----------------|
| Editing `knowledge/*.qmd` | figure | academic |
| Editing economics content | chart | academic |
| Discussing "process", "workflow", "steps" | diagram | academic |
| Discussing "comparison", "data", "statistics" | chart | academic |
| Discussing "concept", "idea", "vision" | illustration | academic |
| Marketing/advocacy topic | figure | retro |
| Website landing page | illustration | modern |

| Prompt Keywords | Suggest Type |
|-----------------|--------------|
| flow, process, pipeline, stages | diagram |
| chart, graph, compare, data, cost, spending | chart |
| concept, metaphor, vision, idea | illustration |
| (none of above) | figure |

---

## Environment Requirements

Requires `GOOGLE_GENERATIVE_AI_API_KEY` environment variable.
Get key from: https://aistudio.google.com/app/apikey

---

## Quick Reference

| Option | Flag | Values |
|--------|------|--------|
| Type | `--type` | `figure`, `diagram`, `chart`, `illustration` |
| Aspect | `--aspect` | `16:9`, `1:1`, `4:3`, `9:16` |
| Style | `--style` | `academic`, `retro`, `modern` |
| Output | `--output` | directory path (default: `assets/images/generated`) |
| File | `--file` | QMD path to auto-insert |
| Alt | `--alt` | accessibility text |
