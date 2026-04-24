---
name: fix-github-issues
description: Check all open GitHub issues and fix whatever you can. Mark issues complete when fixed, or comment on why they can't be auto-fixed. Use to autonomously work through the issue backlog.
---

# Fix GitHub Issues

Go through all open issues and fix whatever can be fixed automatically.

## Process

1. **List issues**: `gh issue list --state open --json number,title,labels,body --limit 50`
2. **For each issue**:
   - Read issue details
   - Determine if auto-fixable
   - If YES: Fix it, commit, close issue with comment
   - If NO: Add comment explaining why, add label `needs-manual-fix`
3. **Commit all fixes**: One commit with all changes, list issues fixed in commit message
4. **Report summary**: Show what was fixed and what needs manual work

## Types of Issues to Auto-Fix

✅ **Validation errors** - LaTeX, links, citations, etc.
✅ **Simple bugs** - Typos, formatting, broken references
✅ **Documentation** - Missing docs, outdated info
✅ **Code quality** - Linting errors, deprecated syntax

❌ **Can't auto-fix**:
- Design decisions (need user input)
- Breaking changes (need approval)
- Complex refactors (need planning)
- Features without specs

## Actions by Issue Type

**Validation errors** (labels: `validation`, `validation:*`):
- Fix triple dollar signs, broken links, LaTeX errors
- Run validation to confirm fix
- Close issue with: "✅ Fixed in commit [hash]"

**Simple fixes** (labels: `bug`, `documentation`):
- Read file, fix issue, test if possible
- Close with: "✅ Fixed: [brief description]"

**Complex issues** (labels: `enhancement`, `refactor`):
- Comment: "⚠️ Needs manual review: [reason]"
- Add label: `needs-manual-fix`
- Don't close

## Output Format

```
GitHub Issues Auto-Fix
---------------------
Checked: [count] open issues

✅ Fixed ([count]):
  #123 - [title]: [what was changed]
  #124 - [title]: [what was changed]

⚠️ Needs Manual Fix ([count]):
  #125 - [title]: [reason can't auto-fix]
  #126 - [title]: [reason can't auto-fix]

Commit: [hash]
Changes: [file count] files modified
```

## Important

- Batch all fixes into ONE commit (don't spam commits)
- Always test/validate before closing issues
- Be conservative - if unsure, mark as needs-manual-fix
- Close issues only when 100% confident the fix is correct
