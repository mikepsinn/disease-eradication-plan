#!/usr/bin/env tsx

import * as fs from 'fs';
import * as path from 'path';

/**
 * Script to integrate updated references back into references.qmd
 * Reads from references-to-update.md and updates references.qmd
 */

const REFERENCES_FILE = path.join(process.cwd(), 'brain', 'book', 'references.qmd');
const UPDATES_FILE = path.join(process.cwd(), 'references-to-update.md');
const JSON_FILE = path.join(process.cwd(), 'references-to-update.json');
const BACKUP_FILE = path.join(process.cwd(), 'brain', 'book', 'references.qmd.backup');

interface Reference {
  id: string;
  title: string;
  quote: string;
  source: string;
  lineStart: number;
  lineEnd: number;
  rawContent: string;
}

interface UpdatedReference {
  id: string;
  newUrl: string;
  note?: string;
}

function parseUpdatesFile(): Map<string, UpdatedReference> {
  const content = fs.readFileSync(UPDATES_FILE, 'utf-8');
  const updates = new Map<string, UpdatedReference>();

  // Parse the markdown file to extract ID and NEW URL
  const sections = content.split(/^## \d+\. /m).filter(s => s.trim());

  for (const section of sections) {
    const lines = section.split('\n');

    let id = '';
    let newUrl = '';
    let note = '';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (line.startsWith('**ID:**')) {
        const idMatch = line.match(/\*\*ID:\*\*\s*`([^`]+)`/);
        if (idMatch) id = idMatch[1];
      } else if (line.startsWith('**NEW URL:**')) {
        // The URL should be on the next non-empty line
        let j = i + 1;
        while (j < lines.length && !lines[j].trim()) j++;
        if (j < lines.length) {
          newUrl = lines[j].trim();
          // Also capture any note that might follow
          j++;
          while (j < lines.length && lines[j].trim() && !lines[j].trim().startsWith('---')) {
            note += lines[j].trim() + ' ';
            j++;
          }
        }
      }
    }

    if (id && newUrl && newUrl !== '') {
      updates.set(id, { id, newUrl: newUrl.trim(), note: note.trim() });
    }
  }

  return updates;
}

function integrateUpdates(): void {
  // Load original references data
  if (!fs.existsSync(JSON_FILE)) {
    throw new Error(`JSON file not found: ${JSON_FILE}. Run extract script first.`);
  }

  const references: Reference[] = JSON.parse(fs.readFileSync(JSON_FILE, 'utf-8'));

  // Load updates from markdown file
  const updates = parseUpdatesFile();

  console.log(`Found ${updates.size} updated references with URLs`);

  if (updates.size === 0) {
    console.log('\n⚠️  No updates found. Please add URLs to references-to-update.md first.');
    return;
  }

  // Create backup of original file
  fs.copyFileSync(REFERENCES_FILE, BACKUP_FILE);
  console.log(`✓ Backup created: ${BACKUP_FILE}`);

  // Read the original file
  const content = fs.readFileSync(REFERENCES_FILE, 'utf-8');
  const lines = content.split('\n');

  // Track which references were updated
  let updatedCount = 0;
  const updatedIds: string[] = [];

  // Process updates by finding anchor tags as delimiters
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Look for anchor tags
    const anchorMatch = line.match(/<a id="([^"]+)"><\/a>/);
    if (!anchorMatch) continue;

    const id = anchorMatch[1];
    const update = updates.get(id);
    if (!update) continue;

    // Find the next line with TODO comment (should be within the next few lines)
    for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
      if (lines[j].includes('<!-- TODO: Add source URL -->')) {
        // Replace the TODO comment with the actual URL
        let newLine = lines[j].replace('<!-- TODO: Add source URL -->', update.newUrl);

        // If the newUrl doesn't start with http or [, it's probably a note
        if (!update.newUrl.startsWith('http') && !update.newUrl.startsWith('[')) {
          newLine = lines[j].replace('<!-- TODO: Add source URL -->', `<!-- ${update.newUrl} -->`);
        }

        lines[j] = newLine;
        updatedCount++;
        updatedIds.push(id);
        break;
      }
    }
  }

  // Write the updated content back
  fs.writeFileSync(REFERENCES_FILE, lines.join('\n'), 'utf-8');

  console.log(`\n✓ Updated ${updatedCount} references in references.qmd`);

  if (updatedCount > 0) {
    console.log('\n📋 Updated references:');
    updatedIds.slice(0, 10).forEach(id => console.log(`   - ${id}`));
    if (updatedIds.length > 10) {
      console.log(`   ... and ${updatedIds.length - 10} more`);
    }
  }

  console.log('\n📝 Next steps:');
  console.log('   1. Review the changes in references.qmd');
  console.log('   2. If satisfied, delete the backup file');
  console.log('   3. If not satisfied, restore from backup:');
  console.log(`      mv ${BACKUP_FILE} ${REFERENCES_FILE}`);
}

// Main execution
try {
  console.log('Integrating updated references...\n');
  integrateUpdates();
} catch (error) {
  console.error('Error:', error);
  process.exit(1);
}
