#!/usr/bin/env node

import { elevateToneWithLLM, getStaleFilesForTone } from './tone-elevation-utils';
import { parseQuartoYml } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('🎭 Starting tone elevation for all book chapters...\n');
  console.log('   Target: Transform aggressive/pompous language');
  console.log('   Style: Vonnegut + Handey + Cunk (wry, philosophical, detached)\n');

  console.log('📚 Getting main chapter files from _book.yml...');

  // Get only main chapter files from _book.yml
  const { chapters: mainChapterFiles } = await parseQuartoYml();
  console.log(`Found ${mainChapterFiles.length} main chapter files (excluding appendices)`);

  // Get stale files that need tone checking
  const allStaleFiles = await getStaleFilesForTone('brain/book');

  // Files to exclude from tone elevation:
  // - references.qmd: Reference list, not narrative content
  // - Part intro files: These are meant to introduce their sections
  // - Appendix files: These are technical/supporting content
  const excludedFiles = [
    'brain/book/references.qmd',
    'brain/book/problem.qmd',     // Part I: The Problem intro
    'brain/book/solution.qmd',    // Part II: The Solution intro
    'brain/book/proof.qmd',       // Part III: The Case intro
    'brain/book/economics.qmd',   // The Economic Case intro
    'brain/book/futures.qmd',     // Intro to Paths
    'brain/book/strategy.qmd',    // Strategy section intro
    'brain/book/appendix',        // All appendix files
  ];

  // Filter to only include main chapter files that are stale
  // Normalize paths to use forward slashes for comparison
  const staleFilesToCheck = allStaleFiles.filter(file => {
    const normalizedFile = file.replace(/\\/g, '/');

    // Check if file is in exclusion list or appendix
    if (excludedFiles.some(excluded => normalizedFile.includes(excluded))) {
      return false;
    }

    // Only process main chapter files
    return mainChapterFiles.some(chapterPath => normalizedFile.includes(chapterPath));
  });

  console.log(`\n📊 Found ${staleFilesToCheck.length} main chapter files needing tone elevation\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('✅ All main chapter files have appropriate tone!');
    return;
  }

  console.log('Files to process:');
  staleFilesToCheck.forEach((file, index) => {
    console.log(`  ${index + 1}. ${file}`);
  });
  console.log('');

  // Process each file
  let successCount = 0;
  let errorCount = 0;

  for (let i = 0; i < staleFilesToCheck.length; i++) {
    const file = staleFilesToCheck[i];
    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    console.log(`📄 Processing file ${i + 1} of ${staleFilesToCheck.length}`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);

    try {
      await elevateToneWithLLM(file);
      successCount++;
    } catch (error) {
      console.error(`❌ Failed to process ${file}:`, error);
      errorCount++;
    }
  }

  // Summary
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 TONE ELEVATION SUMMARY');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`✅ Successfully processed: ${successCount} files`);
  if (errorCount > 0) {
    console.log(`❌ Failed to process: ${errorCount} files`);
  }
  console.log('\n✨ Tone elevation process complete!');

  // Exit with error code if any files failed
  if (errorCount > 0) {
    process.exit(1);
  }
}

main().catch(err => {
  console.error('❌ An unexpected error occurred:', err);
  process.exit(1);
});