#!/usr/bin/env node

import { elevateToneWithLLM } from './tone-elevation-utils';
import fs from 'fs';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error('❌ Please provide a file path as an argument.');
    console.error('Usage: npx tsx scripts/review/elevate-tone-file.ts <file-path>');
    process.exit(1);
  }

  if (!fs.existsSync(filePath)) {
    console.error(`❌ Error: File not found at ${filePath}`);
    process.exit(1);
  }

  if (!filePath.endsWith('.qmd')) {
    console.error(`❌ Error: File must be a .qmd file`);
    process.exit(1);
  }

  try {
    console.log('🎭 Starting tone elevation process...');
    console.log('   Target: Transform aggressive/pompous language');
    console.log('   Style: Vonnegut + Handey + Cunk (wry, philosophical, detached)\n');

    await elevateToneWithLLM(filePath);

    console.log('\n✨ Tone elevation complete!');
  } catch (error) {
    console.error('❌ An error occurred during the tone elevation process:', error);
    process.exit(1);
  }
}

main();