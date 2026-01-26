---
name: suggest-automations
description: Analyzes recent git history and Claude Code features to suggest new hooks, skills, agents, or plugins that could automate repetitive work.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Task
---

# /suggest-automations

Reviews your recent work patterns and Claude Code capabilities to suggest automation opportunities. Run periodically (weekly/monthly) to continuously improve your workflow.

---

## Step 1: Analyze Recent Git History

Get the last 50 commits with file changes:

```bash
git log --oneline --stat -50 | head -200
```

Look for patterns:
- **Repetitive file edits** (same files touched multiple times)
- **Batch operations** (many similar changes in one commit)
- **Manual fixes** (commits mentioning "fix", "update", "correct")
- **Review cycles** (multiple review/refinement commits)

---

## Step 2: Categorize Work Patterns

Group commits into categories:

| Category | Automation Potential |
|----------|---------------------|
| Content editing (wording, tone) | Medium - LLM review skills |
| Parameter/variable updates | High - Automated validation |
| Image management | High - Generation scripts |
| Link/reference fixes | High - Validation hooks |
| Structural changes | Low - Needs human judgment |
| Publication workflow | High - CI/CD automation |

---

## Step 3: Review Existing Automation

Check what's already automated:

```bash
# List existing skills
ls -la .claude/skills/*/SKILL.md

# List hooks
cat .claude/settings.json

# List scripts
ls scripts/*.py scripts/*.ts | head -30
```

Identify gaps between work patterns and existing automation.

---

## Step 4: Research Claude Code Features

Search for new Claude Code features that could help:

Use WebSearch to find:
- "Claude Code hooks 2026 new features"
- "Claude Code plugins marketplace"
- "Claude Code MCP servers"
- "Claude Code background tasks automation"

Check official docs:
- https://docs.anthropic.com/claude-code/hooks
- https://docs.anthropic.com/claude-code/plugins
- https://docs.anthropic.com/claude-code/agents

---

## Step 5: Generate Recommendations

For each work pattern, suggest specific automations:

### Hook Opportunities

| Trigger | Pattern to Match | Action |
|---------|------------------|--------|
| PostToolUse | Edit\|Write on *.qmd | Run pre-render validation |
| PostToolUse | Edit on parameters.py | Regenerate _variables.yml |
| PreToolUse | Write to sensitive files | Require confirmation |

### Skill Opportunities

| Skill Name | Purpose | When to Use |
|------------|---------|-------------|
| `/batch-fix-X` | Fix all instances of pattern X | Weekly maintenance |
| `/chapter-polish` | Full review of single chapter | Before publication |
| `/sync-configs` | Update all _quarto-*.yml files | After metadata changes |

### Agent Opportunities

| Agent | Tools | Purpose |
|-------|-------|---------|
| citation-finder | WebSearch, Read, Edit | Find and add missing citations |
| image-auditor | Read, Glob, Bash | Check image quality/metadata |
| link-checker | Read, WebFetch | Validate all external links |

### MCP Server Opportunities

| Server | Capability | Use Case |
|--------|------------|----------|
| Reference manager | Query Zotero/Mendeley | Auto-import citations |
| Image generator | Direct API access | Generate images without scripts |
| Task queue | Persistent task list | Cross-session work tracking |

---

## Step 6: Prioritize Recommendations

Rank by:
1. **Frequency** - How often does this work happen?
2. **Time savings** - How much time would automation save?
3. **Error reduction** - Would automation prevent mistakes?
4. **Implementation effort** - How hard is it to build?

Focus on high-frequency, high-savings, low-effort automations first.

---

## Step 7: Create Implementation Plan

For top 3 recommendations, provide:

1. **What**: Specific hook/skill/agent to create
2. **Why**: Work pattern it addresses
3. **How**: Implementation steps
4. **Code**: Draft implementation

---

## Output Format

Generate a report:

```markdown
# Automation Recommendations

## Work Pattern Analysis
[Summary of recent git activity]

## Current Automation Coverage
[List of existing skills/hooks and what they cover]

## Gaps Identified
[Work patterns not covered by automation]

## Recommendations

### 1. [Highest Priority]
- **Type**: Hook/Skill/Agent/MCP
- **Pattern**: [What work it automates]
- **Savings**: [Estimated time/effort saved]
- **Implementation**: [Steps to build]

### 2. [Second Priority]
...

### 3. [Third Priority]
...

## Next Steps
[Actionable items to implement recommendations]
```

---

## Example Findings

From analyzing a typical book project:

**High-value automations found:**
1. **PostToolUse hook for QMD edits** - Auto-run pre-render validation after every edit
2. **Citation finder agent** - When writing claims, auto-search for supporting sources
3. **Image metadata skill** - Batch update alt text and metadata for accessibility
4. **Stale content alert** - Weekly report of files not updated in 30+ days

**Already well-automated:**
- Parameter generation
- PDF validation
- Section image generation

**Needs human judgment:**
- Chapter restructuring
- Tone/voice decisions
- Strategic content choices
