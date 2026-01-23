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

## Step 1: Read Available Options from Source Files

**REQUIRED: Read these files to get current options before asking user questions:**

1. **Read `scripts/images/generate-image.ts`** to extract:
   - Available `--type` values (from `ImageTypes` object)
   - Available `--aspect` values (from `AspectRatios` object)
   - Default values for each option

2. **Read `scripts/lib/image-prompts.ts`** to extract:
   - Available `--style` values (from `VisualStyles` object)
   - Style descriptions for each option

Present these dynamically extracted options to the user. Do NOT use hardcoded option lists.

---

## Step 2: Get Actual Numbers from QMD File

**CRITICAL for charts and data visualizations:**

If the image relates to a QMD file (especially for `chart` type), run the preview script to get actual variable values:

```bash
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file.qmd> --numbers-only
```

Or to see specific sections with resolved values:

```bash
.venv/Scripts/python.exe scripts/preview-qmd-with-variables.py <file.qmd> --line-range "1-100"
```

**Extract the actual numbers** (e.g., deaths, costs, ratios) and include them in the image prompt. The AI image generator needs concrete values to create accurate visualizations.

**Example:** If the file references `{{< var efficacy_lag_deaths_911_equivalents >}}`, run the preview to get the actual number (e.g., "5,000") and include it in the prompt.

---

## Step 3: Gather Context for Inference

Before asking questions, gather context to infer likely choices:

### Check Git Status
```bash
git status --short
git diff --name-only HEAD~3
```

This reveals:
- Recently modified files → topic/domain
- File paths → `knowledge/economics/` suggests charts, `knowledge/appendix/` suggests diagrams

### Check Recent Conversation
What topic is being discussed? What file was just edited?

### Inference Heuristics

| Signal | Suggested Type | Suggested Style |
|--------|----------------|-----------------|
| Economics files | `chart` | (default) |
| Process/implementation files | `diagram` | (default) |
| Workflows, pipelines | `diagram` | (default) |
| Data, costs, comparisons | `chart` | (default) |
| Concepts, vision | `illustration` | (default) |
| Marketing/propaganda | `figure` | retro-futuristic |
| General/unclear | `figure` | (default) |

| Prompt Keywords | Suggest Type |
|-----------------|--------------|
| flow, process, pipeline, stages | diagram |
| chart, graph, compare, data, cost | chart |
| concept, metaphor, vision, idea | illustration |

---

## Step 4: Get Prompt

If no prompt provided as argument, ask user what they want to generate.

---

## Step 5: Ask Options (Context-Ordered)

Use AskUserQuestion for each option. **Order options by inferred likelihood** based on context, putting the recommended choice first with "(Recommended)" suffix.

### Image Type
Present types extracted from `scripts/images/generate-image.ts` → `ImageTypes`

### Aspect Ratio
Present ratios extracted from `scripts/images/generate-image.ts` → `AspectRatios`

Inference hints:
- QMD chapter content → `16:9`
- Social media → `1:1`
- Slides/presentations → `16:9`

### Visual Style
Present styles extracted from `scripts/lib/image-prompts.ts` → `VisualStyles`

### Target File

Determine the target QMD file using these sources (in priority order):

1. **Explicit file reference** - If user mentions a file like `@knowledge/appendix/invisible-graveyard.qmd`
2. **Current conversation context** - What file was just being discussed or edited?
3. **Git status** - Recently modified QMD files:
   ```bash
   git diff --name-only | grep "\.qmd$" | head -1
   git diff --name-only HEAD~3 | grep "\.qmd$" | head -1
   ```
4. **Book structure** - Read `_quarto-manual.yml` to understand chapter organization and find the most relevant chapter for the image topic

**Always verify the target file exists in `_quarto-manual.yml`** - images should only be inserted into files that are part of the book.

---

## Step 6: Build and Run Command

**DO NOT use the `--file` flag** - it appends to the end of the file, which is wrong.

```bash
cd E:/code/obsidian/websites/disease-eradication-plan
npx tsx scripts/images/generate-image.ts "<prompt>" \
  --type <type> \
  --aspect <aspect> \
  --style <style> \
  --alt "<alt_text>"
```

The script outputs the generated image path. Note it for the next step.

---

## Step 7: Insert Image at Optimal Location

**CRITICAL: Insert the image where the content is discussed, NOT at the end of the file.**

### Finding the Optimal Location

1. **Read the target QMD file** to understand its structure
2. **Search for the section** that discusses the image's subject matter:
   - Look for headings (`##`, `###`) related to the image topic
   - Find paragraphs that mention the key concepts in the image
   - Identify where the data/numbers shown in the image are discussed
3. **Insert the image immediately AFTER** the relevant paragraph or section heading

### Insertion Rules

| Image Subject | Insert Location |
|---------------|-----------------|
| Data/statistics | After the paragraph that presents those numbers |
| Process/workflow | After the section heading that introduces the process |
| Comparison | After the paragraph that sets up the comparison |
| Concept illustration | After the paragraph explaining the concept |

### Example

If generating a chart about "9/11 equivalents of FDA delay deaths":
1. Search the QMD file for text mentioning "9/11" or "equivalents"
2. Find the paragraph: "The FDA's delays cause deaths equivalent to X 9/11 attacks..."
3. Insert the image markdown **immediately after** that paragraph

### Using Edit Tool

Use the Edit tool to insert the image at the correct location:

```
old_string: [the paragraph discussing the image subject]

new_string: [same paragraph]

![Alt text describing the image](../../assets/images/generated/filename.png)
```

**Compute the correct relative path** from the QMD file to the image in `assets/images/generated/`.

---

## Step 8: Report Result

After successful generation and insertion, report:
- Image file path
- Where it was inserted (section/paragraph)
- Remind user to preview the rendered output

---

## CRITICAL RULES FOR CHARTS

**NEVER use logarithmic scaling.** Always use linear scales for all axes.

When generating charts or data visualizations:

1. **Use LINEAR scaling only** - logarithmic scales obscure the dramatic differences we want to show
2. **Include actual numbers** - extract real values from the QMD file using the preview script
3. **Show scale dramatically** - if one bar is 5,000x larger than another, make that visually obvious
4. **Label clearly** - include numbers on bars/elements so the scale is unambiguous
5. **No artistic interpretation of scale** - if deaths are 15 million vs 3,000, show that exact ratio

**Bad:** Log scale that makes 15M and 3K look similar
**Good:** Linear scale where 15M tower dwarfs the 3K bar

---

## Environment Requirements

Requires `GOOGLE_GENERATIVE_AI_API_KEY` environment variable.

---

## Source Files Reference

| File | Contains |
|------|----------|
| `scripts/images/generate-image.ts` | `ImageTypes`, `AspectRatios`, CLI flags |
| `scripts/lib/image-prompts.ts` | `VisualStyles`, style prompts |
| `scripts/preview-qmd-with-variables.py` | Resolves `{{< var >}}` to actual values |
| `_quarto-manual.yml` | Book structure, chapter list, valid QMD files |
