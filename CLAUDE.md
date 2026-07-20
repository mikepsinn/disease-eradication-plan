<!-- AI: CLAUDE.md edits must be minimal. Shared instructions belong in AGENTS.md. -->

@AGENTS.md

## Claude Code

- Before promoting content into the book, use the Optimitron `searchManual` tool with `llms.txt` to confirm the argument is not already written.
- When the user gives a generalizable correction, save it as a `feedback` memory. If it is mechanically checkable, add it to `.claude/hooks/voice-punchup-review.py`. Capture durable rules, not one-offs.
