---
description: "TypeScript coding standards for scripts and automation"
applyTo: "scripts/**/*.ts, src/**/*.ts"
---

# TypeScript Scripts Instructions

Standards for TypeScript scripts, automation tools, and utilities.

## Execution

**ALWAYS use `tsx` to run TypeScript files**, not `ts-node`:

✅ Correct:
```bash
npx tsx scripts/review/review.ts
```

❌ Wrong:
```bash
npx ts-node scripts/review/review.ts
```

## Code Style

### Module System

Use ES modules (as configured in `package.json`):

```typescript
// Correct
import { readFile } from 'fs/promises';
import yaml from 'js-yaml';

// Wrong - don't use require()
const fs = require('fs');
```

### TypeScript Configuration

Follow settings in `tsconfig.json`:
- **Target**: ES2022
- **Module**: ES2022
- **Strict mode**: Enabled
- **Module resolution**: bundler

### Type Safety

Always use proper types, avoid `any`:

```typescript
// Correct
interface Parameter {
  value: number;
  unit: string;
  source_type: 'external' | 'calculated' | 'definition';
}

// Wrong
let param: any = { ... };
```

## File Organization

### Script Structure

Organize scripts logically:

```
scripts/
  ├── review/          # Content review tools
  ├── images/          # Image generation/processing
  ├── chat/            # Chat and AI tools
  └── lib/             # Shared utilities
```

### Import Paths

Use relative imports for project files:

```typescript
import { loadYamlFile } from '../lib/yaml-utils.js';
```

Note: Include `.js` extension for ES modules (TypeScript resolves correctly).

## Common Patterns

### File Operations

```typescript
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';

// Use async/await
const content = await readFile(filePath, 'utf-8');
await writeFile(outputPath, content);
```

### YAML Processing

```typescript
import yaml from 'js-yaml';

const data = yaml.load(await readFile(yamlPath, 'utf-8'));
```

### Command-line Scripts

Use `yargs` for argument parsing:

```typescript
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('force', {
    alias: 'f',
    type: 'boolean',
    description: 'Force operation'
  })
  .parseSync();
```

## Error Handling

Always handle errors appropriately:

```typescript
try {
  const result = await riskyOperation();
  console.log('Success:', result);
} catch (error) {
  console.error('Error:', error.message);
  process.exit(1);
}
```

## Console Output

### Use Clear Messages

```typescript
// Good
console.log('✓ Generated variables for 42 parameters');
console.error('✗ Failed to parse YAML file');

// Avoid Unicode on Windows Python scripts, but OK in Node.js
```

### Progress Indicators

For long operations:

```typescript
console.log('Processing files...');
let processed = 0;
for (const file of files) {
  await processFile(file);
  processed++;
  console.log(`Progress: ${processed}/${files.length}`);
}
```

## Working with Parameters

### Reading Variables

```typescript
import yaml from 'js-yaml';
import { readFile } from 'fs/promises';

const variables = yaml.load(
  await readFile('_variables.yml', 'utf-8')
) as Record<string, any>;
```

### Parameter Name Conversion

Convert between Python and QMD naming:

```typescript
// Python: GLOBAL_ANNUAL_WAR_COST
// QMD: global_annual_war_cost

function toVarName(pythonName: string): string {
  return pythonName.toLowerCase();
}
```

## Quarto Integration

### Rendering

Use Python script, don't call quarto directly in TS:

```typescript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Use the Python wrapper
await execAsync('python scripts/render-quarto.py book --preview');
```

### File Paths

Always use absolute paths or proper relative paths:

```typescript
import { resolve } from 'path';

const projectRoot = process.cwd();
const qmdPath = resolve(projectRoot, 'knowledge', 'intro.qmd');
```

## Testing

### Unit Tests (Jest)

Place tests alongside code or in `__tests__`:

```typescript
// scripts/lib/__tests__/yaml-utils.test.ts
import { loadYamlFile } from '../yaml-utils.js';

describe('loadYamlFile', () => {
  it('should load valid YAML', async () => {
    const result = await loadYamlFile('test.yml');
    expect(result).toBeDefined();
  });
});
```

### Run Tests

```bash
npm test                  # Run all tests
npm run test:watch        # Watch mode
npm run test:coverage     # With coverage
```

## Dependencies

### Adding New Dependencies

1. Check if it's in the ecosystem: `npm search package-name`
2. Install: `npm install package-name`
3. Use proper imports
4. Document in code why it's needed

### Common Dependencies

- `gray-matter`: Frontmatter parsing
- `glob`: File pattern matching
- `js-yaml`: YAML processing
- `yargs`: CLI argument parsing
- `sharp`: Image processing
- `chokidar`: File watching

## Script Best Practices

1. **Single responsibility**: Each script does one thing well
2. **Reusable functions**: Extract to `lib/` if used multiple times
3. **Error messages**: Clear and actionable
4. **Documentation**: Add JSDoc comments for complex functions
5. **Dry run mode**: Add `--dry-run` flag for destructive operations

## Example Script Template

```typescript
#!/usr/bin/env node

import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

async function main() {
  const argv = yargs(hideBin(process.argv))
    .option('input', {
      alias: 'i',
      type: 'string',
      description: 'Input file path',
      demandOption: true
    })
    .option('dry-run', {
      type: 'boolean',
      description: 'Preview changes without applying',
      default: false
    })
    .parseSync();

  try {
    console.log('Starting process...');
    
    // Your logic here
    
    console.log('✓ Complete');
  } catch (error) {
    console.error('✗ Error:', error.message);
    process.exit(1);
  }
}

main();
```

## Linting and Formatting

Scripts should pass TypeScript compiler checks:

```bash
npx tsc --noEmit  # Check types without building
```

No automatic formatters are enforced, but maintain consistency with existing code style.
