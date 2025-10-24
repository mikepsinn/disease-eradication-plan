#!/usr/bin/env tsx
/**
 * File Watcher for Real-time Content Reviews
 *
 * Usage: npm run watch
 *
 * Watches .qmd files and automatically runs reviews
 * when they're saved. Useful during active writing sessions.
 *
 * Press Ctrl+C to stop watching.
 */

import chokidar from 'chokidar';
import path from 'path';
import {
  styleFileWithLLM,
  factCheckFileWithLLM,
  structureCheckFileWithLLM,
  linkCheckFile,
  figureCheckFile
} from './review/utils';
import dotenv from 'dotenv';

dotenv.config();

// Debounce delay (wait this long after last change before reviewing)
const DEBOUNCE_MS = 3000;

const pendingReviews = new Map<string, NodeJS.Timeout>();

async function reviewFile(filePath: string) {
  console.log(`\n🔍 Reviewing ${filePath}...`);

  try {
    // Run checks in order of importance
    await structureCheckFileWithLLM(filePath);
    await styleFileWithLLM(filePath);
    await factCheckFileWithLLM(filePath);
    await linkCheckFile(filePath);
    await figureCheckFile(filePath);

    console.log(`✅ Review complete for ${filePath}\n`);
  } catch (error) {
    console.error(`❌ Error reviewing ${filePath}:`, error);
  }
}

function scheduleReview(filePath: string) {
  // Clear existing timer for this file
  const existing = pendingReviews.get(filePath);
  if (existing) {
    clearTimeout(existing);
  }

  // Schedule new review after debounce period
  const timer = setTimeout(() => {
    reviewFile(filePath);
    pendingReviews.delete(filePath);
  }, DEBOUNCE_MS);

  pendingReviews.set(filePath, timer);
  console.log(`⏳ Scheduled review for ${path.basename(filePath)} in ${DEBOUNCE_MS/1000}s...`);
}

console.log('👀 Watching brain/book/**/*.qmd for changes...');
console.log('💡 Save a file to trigger automated review');
console.log('⌛ Reviews run 3 seconds after you stop editing');
console.log('🛑 Press Ctrl+C to stop\n');

const watcher = chokidar.watch('brain/book/**/*.qmd', {
  ignored: /(^|[\/\\])\../, // ignore dotfiles
  persistent: true,
  ignoreInitial: true
});

watcher
  .on('change', (filePath) => {
    console.log(`📝 Detected change in ${path.basename(filePath)}`);
    scheduleReview(filePath);
  })
  .on('error', (error) => {
    console.error('❌ Watcher error:', error);
  });

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n👋 Stopping file watcher...');
  watcher.close();
  process.exit(0);
});
