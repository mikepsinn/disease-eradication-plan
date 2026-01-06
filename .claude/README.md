# Claude Code Configuration for Disease Eradication Plan

This directory contains hooks, skills, and agents to enable autonomous editing and validation of the Quarto book.

## 📁 Directory Structure

```
.claude/
├── hooks/                    # Automated validation scripts
│   ├── validate-qmd-changes.py        # PostToolUse: Validate QMD edits
│   ├── auto-regenerate-variables.sh   # PostToolUse: Auto-regen variables
│   ├── check-python-errors.sh         # PostToolUse: Python linting
│   └── load-book-context.sh           # SessionStart: Load project context
├── skills/                   # Reusable multi-step workflows
│   ├── validate-and-regenerate-parameters/
│   ├── qmd-consistency-check/
│   └── verify-and-add-sources/
├── agents/                   # Autonomous specialists
│   ├── parameter-manager/
│   └── book-reviewer/
├── settings.json             # Hook configuration
└── README.md                 # This file
```

## ⚙️ Hooks (Automated Validation)

### PostToolUse Hooks
Run automatically after every file edit:

1. **validate-qmd-changes.py**
   - Checks for hardcoded values that should be variables
   - Validates variable syntax `{{< var name >}}`
   - Detects HTML links (should use `.qmd`)
   - Flags em-dashes for replacement
   - Warns about malformed variable references

2. **auto-regenerate-variables.sh**
   - Detects changes to `dih_models/parameters.py`
   - Automatically runs variable generation script
   - Updates `_variables.yml` and `_analysis/parameter-summary.md`

3. **check-python-errors.sh**
   - Runs pyright static type checking (if installed)
   - Validates Python syntax with py_compile
   - Reports errors immediately

### SessionStart Hook

4. **load-book-context.sh**
   - Shows todo.md status
   - Displays git branch and uncommitted changes
   - Checks if _variables.yml is up-to-date
   - Shows book structure and file counts

## 🛠️ Skills (Reusable Workflows)

### 1. validate-and-regenerate-parameters
**When to use:** After editing `dih_models/parameters.py`

**What it does:**
- Validates parameter syntax
- Checks for common errors (hardcoded calculated values, missing units)
- Regenerates _variables.yml
- Verifies output files

**Usage:** Automatically invoked by hooks, or call explicitly when needed

### 2. qmd-consistency-check
**When to use:** Before commits or after batch edits

**What it does:**
- Validates all variable references against `_variables.yml`
- Checks cross-file links use `.qmd` extensions
- Finds hardcoded values that should be variables
- Detects em-dashes and style issues

**Usage:** Invoke manually for comprehensive validation

### 3. verify-and-add-sources
**When to use:** When adding factual claims or statistics

**What it does:**
- Checks if claim has citation
- Searches `knowledge/references.qmd` for existing source
- If not found, searches web for authoritative source
- Adds new source to `references.qmd`
- Adds citation to text `[@reference-id]`

**Usage:** Called by book-reviewer agent automatically

## 🤖 Agents (Autonomous Specialists)

### 1. parameter-manager (Opus)
**When to use:** `"Use parameter-manager to add..."`

**Capabilities:**
- Adds new parameters to `dih_models/parameters.py`
- Updates existing parameter values
- Fixes parameter formulas and calculations
- Regenerates variables automatically
- Validates parameter naming conventions

**Key Rules:**
- ALWAYS use UPPERCASE_SNAKE_CASE for parameter names
- NEVER pre-scale values (store raw numbers, let formatter scale)
- ALWAYS use formulas for calculated parameters
- NEVER create duplicate parameters

**Example:**
```
User: "Add parameter for global billionaire count"
Agent: Adds GLOBAL_BILLIONAIRE_COUNT = Parameter(3000, ...) and regenerates
```

### 2. book-reviewer (Opus)
**When to use:** Automatically after edits, or `"Use book-reviewer to check..."`

**Capabilities:**
- Reviews changes for consistency
- Validates variable references
- Checks cross-file links
- Verifies citations and sources
- Flags style issues (em-dashes, terminology)
- Ensures completeness (figures, tables exist)

**Key Rules:**
- ALWAYS verify factual claims have citations
- Use verify-and-add-sources skill for unsourced claims
- Flag all em-dashes for replacement
- Ensure HTML links use `.qmd` instead

**Example:**
```
User edits economics.qmd
Agent: Reviews changes, finds unsourced claim "Costa Rica abolished military in 1948",
searches for source, adds to references.qmd, adds citation
```

## 🎨 CLI Tools

### generate-image.ts
**On-demand image generation for chapters**

```bash
# Generate figure and get path
npx tsx scripts/images/generate-image.ts "Flow chart showing treaty adoption"

# Generate and auto-insert into file
npx tsx scripts/images/generate-image.ts "Cost comparison bar chart" \
  --file knowledge/economics/economics.qmd \
  --alt "Bar chart comparing intervention costs"

# Generate diagram in specific style
npx tsx scripts/images/generate-image.ts "Venn diagram of stakeholder interests" \
  --type diagram --style academic --aspect 1:1
```

**Options:**
- `--file <path>`: Auto-insert image into QMD file
- `--type <type>`: figure (default), diagram, chart, illustration
- `--aspect <ratio>`: 16:9 (default), 1:1, 4:3, 9:16
- `--style <style>`: academic (default), retro, modern
- `--alt <text>`: Alt text for accessibility

## 🚀 How to Use

### Automatic Workflows (No Action Required)

After you set up this configuration, hooks run automatically:
- Edit any QMD file → validates, checks variables
- Edit `parameters.py` → regenerates variables
- Edit any Python file → runs linting
- Start session → loads project context

### Manual Invocation

**Invoke skills:**
```
"Use validate-and-regenerate-parameters skill to check parameters"
"Use qmd-consistency-check skill to validate all QMD files"
"Use verify-and-add-sources skill for this claim"
```

**Invoke agents:**
```
"Use parameter-manager to add a new parameter for X"
"Use book-reviewer to check this chapter"
```

**Generate images:**
```
"Generate an image showing X" (I'll use generate-image.ts)
```

## 📋 Configuration

All hooks configured in `settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [...],      // Run after edits
    "UserPromptSubmit": [...],  // Run before processing request
    "SessionStart": [...]       // Run at startup
  }
}
```

## 🔧 Requirements

- **Python**: `.venv` with pyright (optional) for type checking
- **Bash**: For hook scripts (Windows users: use Git Bash or WSL)
- **Node.js**: For TypeScript scripts (image generation)
- **Gemini API Key**: For image generation (`GOOGLE_GENERATIVE_AI_API_KEY` in `.env`)

## 📝 Adding New Hooks/Skills/Agents

### Add Hook
1. Create script in `.claude/hooks/`
2. Add to `.claude/settings.json`
3. Test with a file edit

### Add Skill
1. Create directory in `.claude/skills/<skill-name>/`
2. Create `SKILL.md` with frontmatter and process
3. Reference in agent's `skills` list

### Add Agent
1. Create directory in `.claude/agents/<agent-name>/`
2. Create `AGENT.md` with frontmatter, role, rules
3. Invoke with "Use <agent-name> to..."

## ✅ Best Practices

1. **Always use variables** instead of hardcoded values
2. **Always cite sources** for factual claims
3. **Always use .qmd links** not .html for cross-format compatibility
4. **Always regenerate variables** after parameter changes
5. **Always validate** before commits

## 🐛 Troubleshooting

**Hook not running?**
- Check hook path in `settings.json`
- Verify script has execute permissions (chmod +x)
- Check hook timeout settings

**Variable generation fails?**
- Run: `python -m py_compile dih_models/parameters.py`
- Check for syntax errors
- Verify all parameter names are UPPERCASE

**Image generation fails?**
- Check `GOOGLE_GENERATIVE_AI_API_KEY` in `.env`
- Verify Node.js and TypeScript installed
- Check output directory permissions

## 📚 Resources

- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks.md)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md)
- [Claude Code Agents Documentation](https://code.claude.com/docs/en/sub-agents.md)

---

**Last Updated:** 2026-01-06
**Version:** 1.0
