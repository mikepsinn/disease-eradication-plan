---
name: work-todo
description: Pick a task from TODO.md, plan implementation, complete it, and update TODO.md
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
  - Task
  - AskUserQuestion
---

# /work-todo

Pick a task from TODO.md, plan its implementation, complete it, and update TODO.md.

---

## Step 1: Read and Select Task

Read `TODO.md`:

```bash
cat TODO.md
```

Present tasks to the user using AskUserQuestion:
- List each task with a number
- Let user pick which to work on

---

## Step 2: Analyze and Plan

Once a task is selected:

1. **Read OUTLINE.md** to understand project structure
2. **Read mentioned files** thoroughly
3. **Identify all affected files** that need changes
4. **Create implementation plan** with concrete steps

Present plan using AskUserQuestion:
```
Task: [Selected task]

Analysis: [Your understanding]

Files to modify:
- file1.qmd - [reason]
- file2.qmd - [reason]

Plan:
1. [Step 1]
2. [Step 2]

Proceed?
```

---

## Step 3: Implement

Execute the plan:

1. Read each file before editing
2. Make focused, minimal changes
3. Validate with pre-render check:
```bash
npm run validate:pre-render
```

---

## Step 4: Update TODO.md

After implementation:

| Status | Action |
|--------|--------|
| **Complete** | Remove the task line |
| **Partial** | Add `(NOTE: progress details)` suffix |
| **Blocked** | Add `(BLOCKED: reason)` suffix |

Edit TODO.md with the appropriate update.

---

## Step 5: Summary

Report:
- What was done
- Files changed
- TODO.md status
- Any follow-up needed

---

## Guidelines

- **Don't commit** unless asked
- **Validate changes** before finishing
- **Ask before major changes**
- **Be accurate** about completion status
