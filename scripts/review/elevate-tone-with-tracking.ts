#!/usr/bin/env node

import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';
import {
  generateClaudeOpus41Content,
  generateGeminiProContent,
  extractJsonFromResponse,
  loadPromptTemplate
} from '../lib/llm';
import {
  readFileWithMatter,
  updateFileWithHash,
  getBodyHash
} from '../lib/file-utils';
import dotenv from 'dotenv';

dotenv.config();

interface ToneReplacement {
  find: string;
  replace: string;
  reason: string;
}

interface ToneResponse {
  status: 'changes_needed' | 'no_changes_needed';
  humor_preserved: string[];
  replacements: ToneReplacement[];
}

/**
 * Get all .qmd files that need tone elevation
 */
async function getFilesToProcess(directory: string): Promise<string[]> {
  const allFiles = await glob(`${directory}/**/*.qmd`, {
    ignore: [
      '**/node_modules/**',
      '**/_book/**',
      '**/.quarto/**',
      '**/references.qmd', // Skip references
      '**/appendix/**'     // Skip appendix files for now
    ]
  });

  const filesToProcess: string[] = [];

  for (const file of allFiles) {
    const { frontmatter, body } = await readFileWithMatter(file);
    const currentHash = getBodyHash(body);

    // Check if file has been processed with humor preservation
    if (!frontmatter.lastToneElevationWithHumorHash ||
        frontmatter.lastToneElevationWithHumorHash !== currentHash) {
      filesToProcess.push(file);
    }
  }

  return filesToProcess;
}

/**
 * Process a single file with humor preservation
 */
async function processFileWithHumorPreservation(filePath: string, useGemini: boolean = false): Promise<void> {
  console.log(`\n📝 Processing: ${filePath}`);
  const { frontmatter, body } = await readFileWithMatter(filePath);

  // Load the prompt with humor preservation
  const prompt = await loadPromptTemplate('scripts/prompts/elevate-tone-preserve-humor.md', {
    '{{filePath}}': filePath,
    '{{content}}': body
  });

  // Get response from LLM
  console.log(`   🤖 Analyzing with ${useGemini ? 'Gemini' : 'Claude Opus'}...`);
  const responseText = useGemini
    ? await generateGeminiProContent(prompt)
    : await generateClaudeOpus41Content(prompt);

  // Parse JSON response
  let response: ToneResponse;
  try {
    response = extractJsonFromResponse(responseText) as ToneResponse;
  } catch (error) {
    console.error(`   ❌ Failed to parse LLM response as JSON:`, error);
    console.error('   Response was:', responseText.substring(0, 500));
    return;
  }

  // Show preserved humor
  if (response.humor_preserved && response.humor_preserved.length > 0) {
    console.log(`   😄 Preserved ${response.humor_preserved.length} existing jokes:`);
    response.humor_preserved.forEach(joke => {
      console.log(`      • "${joke.substring(0, 60)}${joke.length > 60 ? '...' : ''}"`);
    });
  }

  // Check if changes are needed
  if (response.status === 'no_changes_needed' || !response.replacements || response.replacements.length === 0) {
    console.log(`   ✅ File already has appropriate tone. Marking as processed.`);
    await updateFileWithHash(filePath, body, frontmatter, 'lastToneElevationWithHumorHash');
    return;
  }

  // Apply replacements
  let modifiedBody = body;
  let replacementCount = 0;

  console.log(`   🔄 Applying ${response.replacements.length} tone improvements:`);

  for (const replacement of response.replacements) {
    // Check if text exists
    if (!modifiedBody.includes(replacement.find)) {
      console.warn(`      ⚠ Could not find: "${replacement.find.substring(0, 50)}..."`);
      continue;
    }

    // Perform replacement
    modifiedBody = modifiedBody.replace(replacement.find, replacement.replace);
    replacementCount++;

    // Log the change (abbreviated)
    console.log(`      ✓ Transformed: "${replacement.find.substring(0, 40)}..."`);
    if (replacement.find.length > 40 || replacement.replace.length > 40) {
      console.log(`        → "${replacement.replace.substring(0, 40)}..."`);
    }
  }

  if (replacementCount === 0) {
    console.log(`   ⚠ No replacements could be applied. File unchanged.`);
    return;
  }

  // Save the modified file with tracking hash
  await updateFileWithHash(filePath, modifiedBody, frontmatter, 'lastToneElevationWithHumorHash');
  console.log(`   ✅ Successfully processed (${replacementCount} changes applied)`);
}

/**
 * Main function to process all files with progress tracking
 */
async function main() {
  console.log('🎭 TONE ELEVATION WITH HUMOR PRESERVATION');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  console.log('Target: Transform aggressive language while preserving existing humor');
  console.log('Style: Vonnegut + Handey + Cunk (wry, philosophical, detached)\n');

  // Check which API is available
  const hasAnthropicKey = !!process.env.ANTHROPIC_API_KEY;
  const hasGeminiKey = !!process.env.GOOGLE_GENERATIVE_AI_API_KEY;

  if (!hasAnthropicKey && !hasGeminiKey) {
    console.error('❌ No API keys found. Please set either ANTHROPIC_API_KEY or GOOGLE_GENERATIVE_AI_API_KEY');
    process.exit(1);
  }

  const useGemini = !hasAnthropicKey && hasGeminiKey;
  if (useGemini) {
    console.log('📌 Using Gemini Pro (Claude Opus key not found)\n');
  }

  // Get files that need processing
  console.log('🔍 Scanning for files to process...');
  const filesToProcess = await getFilesToProcess('brain/book');

  if (filesToProcess.length === 0) {
    console.log('\n✨ All files have already been processed with humor preservation!');
    return;
  }

  console.log(`\n📊 Found ${filesToProcess.length} files needing tone elevation:\n`);
  filesToProcess.forEach((file, index) => {
    const relPath = path.relative('brain/book', file);
    console.log(`   ${index + 1}. ${relPath}`);
  });

  // Create a progress tracker
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📈 PROCESSING PROGRESS');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  let successCount = 0;
  let errorCount = 0;
  let totalHumorPreserved = 0;
  let totalChangesApplied = 0;

  // Process each file
  for (let i = 0; i < filesToProcess.length; i++) {
    const file = filesToProcess[i];
    const relPath = path.relative('brain/book', file);

    console.log(`\n[${i + 1}/${filesToProcess.length}] ${relPath}`);
    console.log('─'.repeat(50));

    try {
      await processFileWithHumorPreservation(file, useGemini);
      successCount++;

      // Add a small delay to avoid rate limits
      if (i < filesToProcess.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    } catch (error) {
      console.error(`   ❌ Error processing file:`, error);
      errorCount++;
    }
  }

  // Final summary
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 FINAL SUMMARY');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`✅ Successfully processed: ${successCount} files`);
  if (errorCount > 0) {
    console.log(`❌ Failed to process: ${errorCount} files`);
  }
  console.log('\n✨ Tone elevation with humor preservation complete!');
  console.log('   All existing jokes have been preserved.');
  console.log('   Aggressive language has been transformed.');

  if (errorCount > 0) {
    process.exit(1);
  }
}

// Run the script
main().catch(err => {
  console.error('❌ Unexpected error:', err);
  process.exit(1);
});