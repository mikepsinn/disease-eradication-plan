---
active: true
iteration: 1
max_iterations: 100
completion_promise: "ALL_FILES_AUDITED"
started_at: "2026-01-08T04:42:36Z"
prompt_file: "audit-hardcoded"
---

# Hardcoded Value Audit

Systematically find and replace hardcoded numeric values in QMD files with variables from `_variables.yml`.

## Your Task

1. **Find next QMD file** with hardcoded values (dollar amounts like $14M, $929, percentages, large numbers)
2. **Check _variables.yml** for matching variables
3. **Replace hardcoded values** with `{{< var variable_name >}}`
4. **Skip LaTeX blocks** - variables don't work inside `$$` blocks
5. **Move to next file** until all files are clean

## Important Rules

- Use `grep` or search tools to find hardcoded values
- Check `_variables.yml` before replacing
- If no variable exists, note it but don't create new parameters
- Track which files you've checked
- Work systematically through knowledge/ directory

## Completion

Output `<promise>ALL_FILES_AUDITED</promise>` when you have checked all QMD files and no more hardcoded values can be replaced with existing variables.
