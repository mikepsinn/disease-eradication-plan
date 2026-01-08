---
description: Run a Ralph loop from a saved prompt file
argument-hint: "<prompt-name> | --list"
---

# Ralph Prompt Runner

Run saved Ralph loop prompts from `.claude/ralph-prompts/`.

## Usage

**List available prompts:**
```bash
python .claude/ralph-prompts/run.py --list
```

**Run a prompt:**
```bash
python .claude/ralph-prompts/run.py <prompt-name>
```

## Available Prompts

Check `.claude/ralph-prompts/` for prompt files. Each `.md` file is a prompt.

## Examples

```bash
# Audit hardcoded values
python .claude/ralph-prompts/run.py audit-hardcoded

# Review current chapter
python .claude/ralph-prompts/run.py review-chapter

# Fix validation errors
python .claude/ralph-prompts/run.py fix-validation-errors
```

## Creating New Prompts

Create a `.md` file in `.claude/ralph-prompts/` with optional frontmatter:

```markdown
---
max_iterations: 50
completion_promise: TASK_DONE
description: Short description for listing
---

Your prompt instructions here...
```

## After Running

The Ralph loop will start. Work on the task. To complete:
- Reach max_iterations, OR
- Output `<promise>YOUR_COMPLETION_PROMISE</promise>`

To cancel: `/ralph-loop:cancel-ralph`
