---
name: edit-image
description: Edit images using AI (Gemini). Fix text, change colors, remove elements, or make other modifications while preserving the original style.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Glob
---

# /edit-image <image-path> "<instructions>"

Edit an existing image using Gemini AI while preserving its overall style.

## Usage
```
/edit-image assets/images/chart.jpg "Change the title to 'Updated Chart'"
/edit-image assets/images/diagram.png "Make the background white"
/edit-image @assets/images/poster.jpg "Remove the watermark"
```

---

## Step 1: Determine Target Image

**Priority order:**
1. Explicit file path argument (e.g., `assets/images/chart.jpg`)
2. File reference in conversation (e.g., `@assets/images/file.png`)
3. Recent git changes: `git diff --name-only HEAD~3 | grep -E "\.(jpg|jpeg|png|webp)$" | head -1`

If no image found, ask user to specify.

**Verify image exists:**
```bash
ls -la "<image-path>"
```

---

## Step 2: Get Edit Instructions

If not provided in the command, use AskUserQuestion to ask what changes to make:

**Common edit types:**
- Text changes: "Change 'X' to 'Y'", "Fix the typo", "Update the title"
- Color changes: "Make the background white", "Change blue to green"
- Element removal: "Remove the watermark", "Delete the red circle"
- Style adjustments: "Make it darker", "Increase contrast"

---

## Step 3: Confirm Edit

**Show preview of what will happen:**
```
Image: <image-path>
Edit: <instructions>
Backup: Yes (original saved as <image>.backup)
```

Use AskUserQuestion to confirm:
- "Yes, edit" (Recommended)
- "Edit with different output path"
- "Cancel"

---

## Step 4: Run Edit

After user confirms:
```bash
npx tsx scripts/images/edit-image.ts '<image-path>' '<edit-instructions>'
```

**Options:**
- `--output <path>` - Save to different location instead of overwriting
- `--no-backup` - Don't create backup of original
- `--no-transcript` - Skip transcript extraction after edit

**Examples:**
```bash
# Basic edit (overwrites original, creates .backup)
npx tsx scripts/images/edit-image.ts 'assets/images/chart.jpg' 'Change title to New Title'

# Save to new file
npx tsx scripts/images/edit-image.ts 'assets/images/old.png' 'Remove watermark' --output 'assets/images/new.png'

# No backup
npx tsx scripts/images/edit-image.ts 'assets/images/temp.jpg' 'Fix typo' --no-backup
```

**IMPORTANT: Use single quotes** around paths and instructions to prevent bash interpretation.

---

## Step 5: Report Result

Report:
- Whether edit succeeded
- Output file path
- Backup location (if created)
- Remind user to preview the edited image

---

## Batch Text Fixes

For fixing the same text across multiple images, use the fix-image-text script:

```bash
# Search for images with specific text
npx tsx scripts/images/fix-image-text.ts --search "oldtext"

# Edit all matching images
npx tsx scripts/images/fix-image-text.ts --search "oldtext" --replace "newtext" --edit

# Remove text from all matching images
npx tsx scripts/images/fix-image-text.ts --search "watermark" --remove --edit
```

---

## Environment

Requires `GOOGLE_GENERATIVE_AI_API_KEY` environment variable.

---

## Troubleshooting

**Edit doesn't change what you wanted:**
- Be more specific in instructions
- Try describing the exact location ("the title at the top", "the text in the bottom-left corner")

**Image quality degrades:**
- AI editing may introduce artifacts
- Consider regenerating the image instead with a corrected prompt

**"No edited image returned":**
- Gemini may refuse certain edits
- Try rephrasing the instructions
- Check if the edit request is within content policy
