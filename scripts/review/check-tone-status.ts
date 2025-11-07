#!/usr/bin/env node

import { glob } from 'glob';
import { readFileWithMatter, getBodyHash } from '../lib/file-utils';
import path from 'path';

interface FileStatus {
  path: string;
  hasOldToneCheck: boolean;
  hasHumorPreservedCheck: boolean;
  needsProcessing: boolean;
  lastModified?: string;
}

async function checkToneStatus(): Promise<void> {
  console.log('\n🎭 TONE ELEVATION STATUS REPORT');
  console.log('━'.repeat(60) + '\n');

  // Get all .qmd files
  const allFiles = await glob('brain/book/**/*.qmd', {
    ignore: [
      '**/node_modules/**',
      '**/_book/**',
      '**/.quarto/**'
    ]
  });

  const fileStatuses: FileStatus[] = [];
  const categorized = {
    fullyProcessed: [] as string[],
    oldMethodOnly: [] as string[],
    unprocessed: [] as string[],
    references: [] as string[],
    appendix: [] as string[]
  };

  // Check each file
  for (const file of allFiles) {
    const relPath = path.relative('brain/book', file).replace(/\\/g, '/');

    // Categorize special files
    if (relPath.includes('references.qmd')) {
      categorized.references.push(relPath);
      continue;
    }
    if (relPath.startsWith('appendix/')) {
      categorized.appendix.push(relPath);
      continue;
    }

    const { frontmatter, body } = await readFileWithMatter(file);
    const currentHash = getBodyHash(body);

    const status: FileStatus = {
      path: relPath,
      hasOldToneCheck: !!frontmatter.lastToneElevationHash,
      hasHumorPreservedCheck: frontmatter.lastToneElevationWithHumorHash === currentHash,
      needsProcessing: frontmatter.lastToneElevationWithHumorHash !== currentHash,
      lastModified: frontmatter.lastInstructionalVoiceHash ? '✓' : undefined
    };

    fileStatuses.push(status);

    // Categorize by processing status
    if (status.hasHumorPreservedCheck) {
      categorized.fullyProcessed.push(relPath);
    } else if (status.hasOldToneCheck) {
      categorized.oldMethodOnly.push(relPath);
    } else {
      categorized.unprocessed.push(relPath);
    }
  }

  // Display results
  console.log(`✅ FULLY PROCESSED (with humor preservation): ${categorized.fullyProcessed.length} files`);
  if (categorized.fullyProcessed.length > 0) {
    categorized.fullyProcessed.forEach(f => console.log(`   • ${f}`));
  }

  if (categorized.oldMethodOnly.length > 0) {
    console.log(`\n⚠️  PROCESSED (old method, no humor check): ${categorized.oldMethodOnly.length} files`);
    categorized.oldMethodOnly.forEach(f => console.log(`   • ${f}`));
  }

  if (categorized.unprocessed.length > 0) {
    console.log(`\n❌ UNPROCESSED: ${categorized.unprocessed.length} files`);
    categorized.unprocessed.forEach(f => console.log(`   • ${f}`));
  }

  // Show special categories
  if (categorized.appendix.length > 0) {
    console.log(`\n📎 APPENDIX FILES (skipped): ${categorized.appendix.length} files`);
    console.log(`   These technical files typically don't need tone adjustment`);
  }

  if (categorized.references.length > 0) {
    console.log(`\n📚 REFERENCES (skipped): ${categorized.references.length} files`);
  }

  // Summary statistics
  console.log('\n' + '━'.repeat(60));
  console.log('📊 SUMMARY');
  console.log('━'.repeat(60));

  const total = categorized.fullyProcessed.length + categorized.oldMethodOnly.length + categorized.unprocessed.length;
  const percentComplete = Math.round((categorized.fullyProcessed.length / total) * 100);

  console.log(`Total main content files: ${total}`);
  console.log(`Fully processed: ${categorized.fullyProcessed.length} (${percentComplete}%)`);
  console.log(`Needs humor-preserved processing: ${categorized.oldMethodOnly.length + categorized.unprocessed.length}`);

  // Recommendation
  console.log('\n💡 RECOMMENDATION:');
  if (categorized.unprocessed.length > 0 || categorized.oldMethodOnly.length > 0) {
    console.log('Run: npx tsx scripts/review/elevate-tone-with-tracking.ts');
    console.log('This will process remaining files while preserving existing humor.');
  } else {
    console.log('All files have been processed with humor preservation! 🎉');
  }
}

// Run the status check
checkToneStatus().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});