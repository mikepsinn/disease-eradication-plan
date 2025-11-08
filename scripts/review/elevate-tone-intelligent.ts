#!/usr/bin/env tsx

import {
  readFileWithMatter,
  updateFileWithHash,
  getBookContentFiles,
  getBodyHash
} from '../lib/file-utils';
import { HASH_FIELDS } from '../lib/constants';
import path from 'path';
import fs from 'fs/promises';

/**
 * Process a single file with intelligent tone elevation
 * This creates a temporary file for the agent to edit
 */
async function processFileIntelligently(filePath: string): Promise<boolean> {
  const { frontmatter, body } = await readFileWithMatter(filePath);
  const currentHash = getBodyHash(body);

  // Check if already processed
  if (frontmatter[HASH_FIELDS.TONE_ELEVATION_WITH_HUMOR] === currentHash) {
    return false; // Already processed
  }

  // Create a temporary file for the agent to work with
  const tempPath = filePath.replace('.qmd', '.tone-temp.qmd');
  await fs.writeFile(tempPath, body);

  return true; // Needs processing
}

/**
 * Get files that need tone elevation
 */
async function getFilesNeedingToneElevation(): Promise<string[]> {
  const allFiles = await getBookContentFiles({
    includeAppendix: true,
    includeReferences: false, // Skip references as they don't need tone changes
    includePartIntros: true
  });

  const needsProcessing: string[] = [];

  for (const file of allFiles) {
    const { frontmatter, body } = await readFileWithMatter(file);
    const currentHash = getBodyHash(body);

    // Check if file needs processing
    if (frontmatter[HASH_FIELDS.TONE_ELEVATION_WITH_HUMOR] !== currentHash) {
      needsProcessing.push(file);
    }
  }

  return needsProcessing;
}

/**
 * Main function to coordinate intelligent tone elevation
 */
async function main() {
  console.log('🎭 TONE REVIEW: ANTHROPOLOGIST FROM MARS');
  console.log('━'.repeat(60));
  console.log('Transform earnest declarations into bemused observations.');
  console.log('Voice: Vonnegut meets Handey meets Cunk.\n');

  // Get files needing processing
  console.log('🔍 Scanning for files to process...');
  const filesToProcess = await getFilesNeedingToneElevation();

  if (filesToProcess.length === 0) {
    console.log('\n✨ All files have already been processed!');
    return;
  }

  console.log(`\n📊 Found ${filesToProcess.length} files needing tone elevation:\n`);

  // Group files by directory for better organization
  const filesByDir = new Map<string, string[]>();

  for (const file of filesToProcess) {
    const relPath = path.relative('brain/book', file).replace(/\\/g, '/');
    const dir = path.dirname(relPath);

    if (!filesByDir.has(dir)) {
      filesByDir.set(dir, []);
    }
    filesByDir.get(dir)!.push(path.basename(relPath));
  }

  // Display organized list
  let fileIndex = 1;
  for (const [dir, files] of filesByDir) {
    console.log(`\n📁 ${dir === '.' ? 'Root' : dir}/`);
    for (const file of files) {
      console.log(`   ${fileIndex}. ${file}`);
      fileIndex++;
    }
  }

  console.log('\n' + '━'.repeat(60));
  console.log('📋 PROCESSING APPROACH\n');
  console.log('Transform earnest/pompous declarations by:');
  console.log('1. Adding philosophical distance (Vonnegut\'s "So it goes")');
  console.log('2. Using absurdist comparisons (Handey\'s mundane metaphors)');
  console.log('3. Expressing deadpan confusion (Cunk\'s puzzlement)');
  console.log('4. Preserving ALL existing humor and wordplay');
  console.log('5. Keeping factual information unchanged');
  console.log('6. Making readers discover absurdity themselves');

  console.log('\n' + '━'.repeat(60));
  console.log('🚀 FILES READY FOR AGENT PROCESSING\n');

  // Write the file list to a temporary file for the agent
  const fileListPath = 'brain/book/tone-elevation-files.txt';
  const fileListContent = filesToProcess
    .map(f => path.relative('brain/book', f).replace(/\\/g, '/'))
    .join('\n');

  await fs.writeFile(fileListPath, fileListContent);
  console.log(`✅ File list written to: ${fileListPath}`);
  console.log(`   The agent should process these ${filesToProcess.length} files.`);

  console.log('\n💡 Next step: Launch agent with scripts/prompts/tone-guide.md');
  console.log('   Transform earnest claims → bemused observations');
  console.log('   Keep all humor, change only pompous/earnest language\n');

  return filesToProcess;
}

// Export for use by other scripts
export { getFilesNeedingToneElevation, processFileIntelligently };

// Run if called directly
main().catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});