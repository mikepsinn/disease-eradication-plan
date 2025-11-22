# WISHONIA Agent System

WISHONIA (WISdom and Health Optimization Network Intelligence Agent) is a superintelligent AI economist agent that systematically perfects the book by finding issues, validating content, and maintaining a comprehensive todo list.

## Overview

WISHONIA uses a supervisor agent that coordinates 5 specialized subagents:

1. **Parameter Checker** - Finds hardcoded numbers and suggests parameters
2. **Math Validator** - Validates equations and calculations
3. **Claim Validator** - Identifies unsupported claims needing references
4. **Reference Linker** - Ensures all numbers/claims link to sources
5. **Consistency Checker** - Checks cross-file consistency

## Quick Start

### Prerequisites

- Node.js and npm/pnpm installed
- Google Generative AI API key in `.env` file:
  ```
  GOOGLE_GENERATIVE_AI_API_KEY=your-key-here
  ```

### Basic Usage

```bash
# Process stale files (files that have changed)
npm run wishonia

# Process all files
npm run wishonia:full

# Process a specific file
npm run wishonia:file --file=knowledge/problem/intro.qmd

# Export todo list
npm run wishonia:todo

# Show status
npm run wishonia:status
```

## How It Works

1. **File Detection**: WISHONIA checks frontmatter hash fields to identify files that need review
2. **Parallel Processing**: All 5 subagents check files simultaneously for efficiency
3. **Issue Tracking**: Issues are stored in `.voltagent/wishonia-todo.json`
4. **Hash Updates**: After processing, frontmatter hash fields are updated
5. **Git Staging**: Changes are staged (not committed) for your review

## Todo Management

Todos are stored in `.voltagent/wishonia-todo.json` and can be exported to:
- JSON: `.wishonia-todos.json`
- YAML: `.wishonia-todos.yaml`
- Markdown: `.wishonia-todos.md`

Each todo includes:
- Type (parameter, math, claim, reference, consistency)
- Priority (critical, high, medium, low)
- File path and line number
- Issue description
- Suggested fix
- Confidence level
- Status (pending, in_progress, fixed, reviewed, rejected)

## Hash Fields

WISHONIA tracks review status using frontmatter hash fields:
- `lastParameterCheckHash`
- `lastMathValidationHash`
- `lastClaimValidationHash`
- `lastReferenceLinkingHash`
- `lastConsistencyCheckHash`
- `lastWishoniaFullReviewHash`

## Integration with Git

WISHONIA stages changes but never commits. Review staged changes with:
```bash
git diff --staged
```

## Configuration

The system uses VoltAgent with:
- **Model**: Google Gemini 2.5 Pro
- **Embedding**: Google `models/text-embedding-004`
- **Memory**: LibSQL (SQLite) for persistence
- **Server**: Hono server on port 3141

## Troubleshooting

**No issues found**: This is normal if files are already perfect or recently reviewed.

**API errors**: Make sure `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env`.

**TypeScript errors**: Run `npm install` to ensure all dependencies are installed.

## Advanced Usage

### Custom Workflow

You can create custom workflows by importing the components:

```typescript
import { WishoniaVoltAgent } from "./wishonia-voltagent";
import { EnhancedTodoManager } from "./todo-manager-enhanced";

const wishonia = new WishoniaVoltAgent();
await wishonia.init();
await wishonia.processFile("path/to/file.qmd");
```

### Programmatic Todo Access

```typescript
import { EnhancedTodoManager } from "./todo-manager-enhanced";

const manager = new EnhancedTodoManager();
await manager.loadFromFile();
const todos = manager.getAllTodos();
const criticalTodos = todos.filter(t => t.priority === "critical");
```

## Architecture

```
wishonia-voltagent.ts (Main CLI)
├── Supervisor Agent (coordinates subagents)
├── 5 Subagents (specialized checkers)
├── File Review Workflow (parallel processing)
├── Enhanced Todo Manager (issue tracking)
└── Hash Utilities (stale file detection)
```

## See Also

- [VoltAgent Documentation](https://docs.voltagent.ai) - Framework details

