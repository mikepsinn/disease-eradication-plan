/**
 * CLI script to render and view QMD file content
 * Uses the same content cleaning function as image generation
 *
 * Usage:
 *   npx tsx scripts/qmd-render.ts <path-to-qmd-file>
 *   npx tsx scripts/qmd-render.ts knowledge/futures.qmd
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { getCleanedContentForLLM } from './lib/file-utils';

// Load environment variables
dotenv.config();

async function main() {
  // Get file path from command line argument
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('ERROR: No file path provided');
    console.error('');
    console.error('Usage: npx tsx scripts/qmd-render.ts <path-to-qmd-file>');
    console.error('');
    console.error('Examples:');
    console.error('  npx tsx scripts/qmd-render.ts knowledge/futures.qmd');
    console.error('  npx tsx scripts/qmd-render.ts knowledge/problem/fda-is-unsafe-and-ineffective.qmd');
    process.exit(1);
  }

  const fileArg = args[0];
  const filePath = path.join(process.cwd(), fileArg);

  // Check if file exists
  try {
    await fs.access(filePath);
  } catch {
    console.error(`ERROR: File not found: ${filePath}`);
    process.exit(1);
  }

  console.log(`\n📄 Reading rendered content from: ${fileArg}\n`);
  console.log('='.repeat(80));

  try {
    // Get cleaned/rendered content (variables replaced, markup stripped)
    const content = await getCleanedContentForLLM(filePath);

    // Output the content
    console.log(content);
    console.log('='.repeat(80));
    console.log(`\n📊 Statistics:`);
    console.log(`   Characters: ${content.length.toLocaleString()}`);
    console.log(`   Lines: ${content.split('\n').length.toLocaleString()}`);
    console.log(`   Words (approx): ${content.split(/\s+/).length.toLocaleString()}`);
  } catch (error) {
    console.error('\nERROR: Failed to render content:', error);
    process.exit(1);
  }
}

main().catch(console.error);
