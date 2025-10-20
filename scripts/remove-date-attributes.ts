#!/usr/bin/env node
/**
 * Remove date-related attributes from frontmatter in all .qmd files
 */

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { glob } from 'glob';

interface Change {
  file: string;
  removedFields: string[];
}

// Date-related fields to remove
const DATE_FIELDS = [
  'date',
  'dateCreated',
  'dateModified',
  'dateUpdated',
  'lastModified',
  'created',
  'updated',
  'modified',
];

// Extract frontmatter from a .qmd file
function extractFrontmatter(content: string): { frontmatter: any; rest: string } | null {
  // Normalize line endings to \n
  const normalizedContent = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // Try to match frontmatter with various patterns
  const match = normalizedContent.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    // Try without trailing content requirement
    const simpleMatch = normalizedContent.match(/^---\n([\s\S]*?)\n---/);
    if (!simpleMatch) return null;

    try {
      const frontmatter = yaml.load(simpleMatch[1]);
      const rest = normalizedContent.substring(simpleMatch[0].length);
      return { frontmatter, rest };
    } catch (e) {
      return null;
    }
  }

  try {
    const frontmatter = yaml.load(match[1]);
    return { frontmatter, rest: match[2] };
  } catch (e) {
    return null;
  }
}

// Update frontmatter in file content
function updateFrontmatter(content: string, newFrontmatter: any): string {
  // Normalize line endings
  const normalizedContent = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  const match = normalizedContent.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    // Try simpler match
    const simpleMatch = normalizedContent.match(/^---\n[\s\S]*?\n---/);
    if (!simpleMatch) return content;

    const rest = normalizedContent.substring(simpleMatch[0].length);
    const newYaml = yaml.dump(newFrontmatter, { lineWidth: -1 });
    return `---\n${newYaml}---${rest}`;
  }

  const newYaml = yaml.dump(newFrontmatter, { lineWidth: -1 });
  return `---\n${newYaml}---\n${match[2]}`;
}

// Main function
async function main() {
  const rootDir = process.cwd();

  console.log('🔍 Finding all .qmd files...\n');

  // Find all .qmd files
  const files = await glob('**/*.qmd', {
    cwd: rootDir,
    ignore: ['node_modules/**', '_book/**', '.quarto/**'],
  });

  console.log(`Found ${files.length} .qmd files\n`);

  const changes: Change[] = [];
  const skipped: string[] = [];
  const errors: string[] = [];

  // Analyze all files
  for (const file of files) {
    const filePath = path.join(rootDir, file);

    if (!fs.existsSync(filePath)) {
      errors.push(`File not found: ${file}`);
      continue;
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const parsed = extractFrontmatter(content);

    if (!parsed) {
      // No frontmatter, skip
      continue;
    }

    const { frontmatter } = parsed;

    // Check if any date fields exist
    const removedFields: string[] = [];
    for (const field of DATE_FIELDS) {
      if (field in frontmatter) {
        removedFields.push(field);
      }
    }

    if (removedFields.length === 0) {
      skipped.push(file);
      continue;
    }

    changes.push({
      file,
      removedFields,
    });
  }

  // Display preview
  console.log('📝 Preview of changes:\n');
  console.log('='.repeat(80));

  for (const change of changes) {
    console.log(`\n${change.file}`);
    console.log(`  Removing: ${change.removedFields.join(', ')}`);
  }

  if (skipped.length > 0) {
    console.log(`\n\n✅ No date fields found (${skipped.length} files skipped)`);
  }

  if (errors.length > 0) {
    console.log('\n\n⚠️  Errors:');
    for (const error of errors) {
      console.log(`  • ${error}`);
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log(`\n📊 Summary:`);
  console.log(`  • ${changes.length} files to update`);
  console.log(`  • ${skipped.length} files without date fields`);
  console.log(`  • ${errors.length} errors\n`);

  // Ask for confirmation
  const answer = await new Promise<string>((resolve) => {
    process.stdout.write('Apply these changes? (y/n): ');
    process.stdin.once('data', (data) => {
      resolve(data.toString().trim());
    });
  });

  if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
    // Apply changes
    for (const change of changes) {
      const filePath = path.join(rootDir, change.file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const parsed = extractFrontmatter(content);

      if (parsed) {
        // Remove date fields
        for (const field of change.removedFields) {
          delete parsed.frontmatter[field];
        }

        const newContent = updateFrontmatter(content, parsed.frontmatter);
        fs.writeFileSync(filePath, newContent, 'utf-8');
      }
    }

    console.log(`\n✅ Updated ${changes.length} files!`);
  } else {
    console.log('\n❌ Cancelled. No files were modified.');
  }

  process.exit(0);
}

main().catch(console.error);
