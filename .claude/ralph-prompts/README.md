# Ralph Loop Prompts

Drop prompt files here to create reusable Ralph loops.

## File Format

Each `.md` file becomes a Ralph loop prompt. The filename becomes the command name.

**Example: `audit-hardcoded.md`**
```markdown
---
max_iterations: 50
completion_promise: ALL_HARDCODED_VALUES_REPLACED
---

Find and replace all hardcoded values in QMD files with variables from _variables.yml.

1. Search for hardcoded dollar amounts ($X, $XM, $XB)
2. Check if a matching variable exists in _variables.yml
3. Replace with {{< var variable_name >}}
4. Move to next file

Work systematically through all files until complete.
```

## Usage

```bash
# List available prompts
python .claude/ralph-prompts/run.py --list

# Run a prompt as Ralph loop
python .claude/ralph-prompts/run.py audit-hardcoded

# Run with custom max iterations
python .claude/ralph-prompts/run.py audit-hardcoded --max-iterations 20
```

## Frontmatter Options

| Field | Default | Description |
|-------|---------|-------------|
| `max_iterations` | 0 (unlimited) | Stop after N iterations |
| `completion_promise` | null | Phrase to signal completion |
| `description` | filename | Short description for listing |
