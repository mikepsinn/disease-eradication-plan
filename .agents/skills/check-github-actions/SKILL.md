---
name: check-github-actions
description: Check GitHub Actions workflow status, diagnose failures, fetch logs, and fix common build issues. Use when builds fail, deploys break, or you need to investigate CI/CD problems.
---

# GitHub Actions Diagnostics

Check the most recent completed workflow run and fix any failures.

## Process

1. Run `gh run list --limit 5` to find recent runs
2. Identify the most recent completed run
3. If failed, run `gh run view RUN_ID` to see which jobs failed and their error annotations
4. Read the error messages to understand what broke
5. Search the codebase for the failing code/file mentioned in the error
6. Fix the root cause
7. Report what was broken and what you fixed

## Output

```
GitHub Actions Status
--------------------
Run #[ID] ([time] ago): [X]/13 jobs passed

Failed Jobs:
- [Job Name]: [Brief error description]
  Fix: [What you changed]

Status: [Fixed/Needs commit/Other action needed]
```

Focus on fixing, not explaining. Keep output concise.
