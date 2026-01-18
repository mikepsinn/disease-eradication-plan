# GitHub Copilot Instructions

This directory contains custom instructions for GitHub Copilot to provide better, more context-aware code suggestions for this repository.

## Files

### Repository-wide Instructions

- **`../copilot-instructions.md`**: Main instructions that apply to all files in the repository
  - Tech stack overview
  - Key files and navigation
  - Critical rules (parameters, linking, etc.)
  - Build and development commands
  - Code quality standards

### Path-specific Instructions

These files target specific parts of the codebase using YAML frontmatter with `applyTo` patterns:

- **`parameters.instructions.md`**: Rules for `dih_models/**/*.py`
  - Parameter naming conventions
  - Value storage requirements
  - Calculated parameter rules
  - Generation workflow

- **`content.instructions.md`**: Standards for `knowledge/**/*.qmd, *.qmd`
  - Writing style guidelines
  - Variable usage (no hardcoded numbers)
  - Cross-format linking
  - Content structure requirements

- **`typescript.instructions.md`**: Standards for `scripts/**/*.ts, src/**/*.ts`
  - TypeScript execution (tsx, not ts-node)
  - Module system (ES modules)
  - Common patterns and best practices
  - Testing guidelines

## How It Works

GitHub Copilot automatically reads these instruction files when you work in the repository:

1. **Repository-wide instructions** are always included in Copilot's context
2. **Path-specific instructions** are added when you work on matching files
3. Instructions guide Copilot to suggest code that follows project conventions

## Best Practices

When modifying these files:

1. **Keep instructions concise** - Copilot works best with clear, direct rules
2. **Use examples** - Show correct vs. incorrect patterns
3. **Focus on project-specific conventions** - Don't repeat general programming knowledge
4. **Test changes** - Verify Copilot suggestions improve after updates
5. **Organize by topic** - Use sections and bullet points for clarity

## Documentation

For more information about GitHub Copilot custom instructions:

- [GitHub Docs: Configure custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions)
- [GitHub Blog: Copilot code review instructions](https://github.blog/ai-and-ml/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files/)

## Maintenance

These instructions should be updated when:

- Project conventions change
- New critical rules are established
- Common mistakes are identified
- Tech stack or tooling updates occur

Keep instructions synchronized with:
- `CONTRIBUTING.md`
- `GUIDES/TECHNICAL_GUIDE.md`
- `GUIDES/STYLE_GUIDE.md`
- `CLAUDE.md` (Claude-specific instructions)
