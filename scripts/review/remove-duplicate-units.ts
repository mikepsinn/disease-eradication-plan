import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';

interface VariableUnitMapping {
  [variableName: string]: string;
}

interface Replacement {
  file: string;
  line: number;
  before: string;
  after: string;
}

/**
 * Escape regex special characters
 */
function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Make a word pattern that matches singular and plural
 */
function makePluralPattern(word: string): string {
  // Handle common plural patterns
  if (word.endsWith('s')) {
    return word; // Already plural, don't add optional 's'
  }
  return `${word}s?`;
}

/**
 * Create regex pattern for a variable + unit combination
 */
function createPattern(variableName: string, unit: string): RegExp {
  const varPattern = `\\{\\{< var ${escapeRegex(variableName)} >\\}\\}`;

  // Split unit into words and make each word optionally plural
  const unitWords = unit.split(/\s+/).map(word => makePluralPattern(escapeRegex(word)));
  const unitPattern = unitWords.join('\\s+');

  // Match variable, optional whitespace, then unit
  // Use word boundary to avoid matching partial words
  return new RegExp(`(${varPattern})\\s+(${unitPattern})\\b`, 'gi');
}

/**
 * Find all replacements across all files
 */
async function findReplacements(
  files: string[],
  unitMappings: VariableUnitMapping
): Promise<Replacement[]> {
  const replacements: Replacement[] = [];

  for (const file of files) {
    const content = await fs.readFile(file, 'utf-8');
    const lines = content.split('\n');

    for (const [variableName, unit] of Object.entries(unitMappings)) {
      const pattern = createPattern(variableName, unit);

      lines.forEach((line, index) => {
        const matches = line.matchAll(pattern);

        for (const match of matches) {
          const before = match[0];
          const after = match[1]; // Just the variable reference

          replacements.push({
            file,
            line: index + 1,
            before,
            after,
          });
        }
      });
    }
  }

  return replacements;
}

/**
 * Apply replacements to files
 */
async function applyReplacements(
  replacements: Replacement[],
  unitMappings: VariableUnitMapping
): Promise<void> {
  // Group replacements by file
  const fileGroups = new Map<string, Replacement[]>();
  for (const replacement of replacements) {
    if (!fileGroups.has(replacement.file)) {
      fileGroups.set(replacement.file, []);
    }
    fileGroups.get(replacement.file)!.push(replacement);
  }

  // Process each file
  for (const [file, fileReplacements] of fileGroups) {
    let content = await fs.readFile(file, 'utf-8');

    // Apply all patterns for this file
    for (const [variableName, unit] of Object.entries(unitMappings)) {
      const pattern = createPattern(variableName, unit);
      const replacement = `{{< var ${variableName} >}}`;
      content = content.replace(pattern, replacement);
    }

    await fs.writeFile(file, content, 'utf-8');
  }
}

async function main() {
  const args = process.argv.slice(2);
  const mode = args[0] || '--preview';

  if (mode !== '--preview' && mode !== '--apply') {
    console.error('Usage: npx tsx scripts/review/remove-duplicate-units.ts [--preview|--apply]');
    console.error('  --preview: Show what would be changed (default)');
    console.error('  --apply: Apply the changes');
    process.exit(1);
  }

  console.log('='.repeat(80));
  console.log('REMOVE DUPLICATE UNITS FROM VARIABLE REFERENCES');
  console.log('='.repeat(80));
  console.log(`Mode: ${mode === '--preview' ? 'PREVIEW (no changes)' : 'APPLY (will modify files)'}\n`);

  // Load variable unit mappings
  const mappingsPath = path.join(process.cwd(), 'variable-units.json');
  let unitMappings: VariableUnitMapping;

  try {
    const mappingsContent = await fs.readFile(mappingsPath, 'utf-8');
    unitMappings = JSON.parse(mappingsContent);
  } catch (error) {
    console.error('ERROR: Could not load variable-units.json');
    console.error('Please run: npx tsx scripts/review/extract-variable-units.ts');
    process.exit(1);
  }

  console.log(`Loaded ${Object.keys(unitMappings).length} variable → unit mappings\n`);

  // Get ALL QMD files (not just those in Quarto configs)
  const files = await glob('knowledge/**/*.qmd', {
    cwd: process.cwd(),
    absolute: true,
    windowsPathsNoEscape: true
  });

  // Also include root QMD files
  const rootFiles = await glob('*.qmd', {
    cwd: process.cwd(),
    absolute: true,
    windowsPathsNoEscape: true
  });

  const allFiles = [...files, ...rootFiles];
  console.log(`Scanning ${allFiles.length} QMD files...\n`);

  // Find all replacements
  const replacements = await findReplacements(allFiles, unitMappings);

  if (replacements.length === 0) {
    console.log('✓ No duplicate units found!');
    return;
  }

  // Display replacements
  console.log(`Found ${replacements.length} duplicate unit(s) to remove:\n`);

  // Group by file for display
  const fileGroups = new Map<string, Replacement[]>();
  for (const replacement of replacements) {
    if (!fileGroups.has(replacement.file)) {
      fileGroups.set(replacement.file, []);
    }
    fileGroups.get(replacement.file)!.push(replacement);
  }

  // Display grouped by file
  for (const [file, fileReplacements] of fileGroups) {
    const relativePath = path.relative(process.cwd(), file);
    console.log(`\n${relativePath} (${fileReplacements.length} change(s)):`);

    for (const replacement of fileReplacements) {
      console.log(`  Line ${replacement.line}:`);
      console.log(`    - ${replacement.before}`);
      console.log(`    + ${replacement.after}`);
    }
  }

  console.log('\n' + '='.repeat(80));

  if (mode === '--preview') {
    console.log('PREVIEW MODE - No changes made');
    console.log('To apply these changes, run:');
    console.log('  npx tsx scripts/review/remove-duplicate-units.ts --apply');
  } else {
    // Apply changes
    console.log('Applying changes...');
    await applyReplacements(replacements, unitMappings);
    console.log(`✓ Modified ${fileGroups.size} file(s)`);
    console.log('\nNext steps:');
    console.log('  1. Review changes: git diff');
    console.log('  2. Validate: npm run validate:pre-render');
    console.log('  3. Test render: quarto render knowledge/call-to-action/three-actions.qmd');
  }

  console.log('='.repeat(80));
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
