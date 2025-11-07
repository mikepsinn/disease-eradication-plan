#!/usr/bin/env tsx

import Anthropic from '@anthropic-ai/sdk';
import {
  getBookFilesForProcessing,
  readFileWithMatter,
  updateFileWithHash,
  getBodyHash,
} from '../lib/file-utils.js';
import * as fs from 'fs';
import crypto from 'crypto';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const HASH_FIELD = 'lastToneElevationWithHumorHash';

// Priority files to process first
const PRIORITY_FILES = [
  'brain/book/strategy-overview.qmd',
  'brain/book/solution/war-on-disease.qmd',
  'brain/book/solution/1-percent-treaty.qmd',
  'brain/book/problem/fda-is-unsafe-and-ineffective.qmd',
  'brain/book/economics.qmd',
  'brain/book/theory.qmd',
  'brain/book/solution/aligning-incentives.qmd',
];

const TRANSFORMATION_PROMPT = `You are transforming aggressive/pompous language into wry/philosophical tone (Vonnegut/Deep Thoughts by Jack Handey/Philomena Cunk style) while preserving all existing humor.

CRITICAL RULES:
1. PRESERVE ALL EXISTING HUMOR - Do not touch anything that's already funny
2. ONLY transform aggressive/pompous language to elevated/wry tone
3. Keep ALL statistics, facts, technical details, links, references unchanged
4. Keep ALL code blocks and formulas unchanged
5. DO NOT add new jokes - only elevate tone of non-funny aggressive parts

TRANSFORMATION EXAMPLES:
- "hostile takeover" → "acquiring priorities through a marketplace transaction"
- "weaponize" → "align incentives"
- "political kill list" → "gentle reminder to politicians that voters exist"
- "bankrupt the status quo" → "suggesting the current arrangement might not be optimal"
- Crude language → elevated terminology unless it's really funny
- Superlatives → understatement

STYLE GUIDE:
- Write as if explaining humanity to bemused aliens
- Replace aggression with gentle irony
- Use mundane analogies for dramatic concepts
- Find the quietly ridiculous in serious matters

Return ONLY the transformed body content (no frontmatter). Do not add explanations or comments.`;

async function transformContent(body: string): Promise<string> {
  console.log('    → Sending to Claude for transformation...');

  const message = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 16000,
    messages: [
      {
        role: 'user',
        content: `${TRANSFORMATION_PROMPT}\n\nCONTENT TO TRANSFORM:\n\n${body}`,
      },
    ],
  });

  const textContent = message.content.find(block => block.type === 'text');
  if (!textContent || textContent.type !== 'text') {
    throw new Error('No text content in response');
  }

  return textContent.text.trim();
}

async function processFile(filePath: string): Promise<boolean> {
  console.log(`\n📄 Processing: ${filePath}`);

  try {
    const { frontmatter, body, originalContent } = await readFileWithMatter(filePath);

    // Calculate current hash
    const currentHash = crypto.createHash('sha256').update(body).digest('hex');
    const storedHash = frontmatter[HASH_FIELD];

    if (currentHash === storedHash) {
      console.log('  ✓ Already processed (hash matches), skipping');
      return false;
    }

    console.log('  → Hash mismatch or missing, processing...');
    console.log(`    Current:  ${currentHash.substring(0, 16)}...`);
    console.log(`    Stored:   ${storedHash?.substring(0, 16) || 'none'}...`);

    // Transform the content
    const transformedBody = await transformContent(body);

    // Update file with new content and hash
    await updateFileWithHash(filePath, transformedBody, frontmatter, HASH_FIELD);

    console.log('  ✓ Transformation complete');
    return true;
  } catch (error) {
    console.error(`  ✗ Error processing file: ${error}`);
    return false;
  }
}

async function main() {
  console.log('🎭 Tone Elevation Script - Elevating Pompous to Philosophical\n');
  console.log('═'.repeat(70));

  // Get all book files
  console.log('\n📚 Finding book files...');
  const allFiles = await getBookFilesForProcessing();

  // Filter out appendix and references
  const eligibleFiles = allFiles.filter(file => {
    const normalized = file.replace(/\\/g, '/');
    return !normalized.includes('/appendix/') && !normalized.includes('references.qmd');
  });

  console.log(`Found ${eligibleFiles.length} eligible files (excluding appendix and references)`);

  // Separate priority and non-priority files
  const priorityFiles = PRIORITY_FILES.filter(pf =>
    eligibleFiles.some(ef => ef.replace(/\\/g, '/').endsWith(pf))
  );

  const nonPriorityFiles = eligibleFiles.filter(ef =>
    !PRIORITY_FILES.some(pf => ef.replace(/\\/g, '/').endsWith(pf))
  );

  console.log(`\n🎯 Priority files: ${priorityFiles.length}`);
  console.log(`📋 Other files: ${nonPriorityFiles.length}`);

  // Resolve priority file paths
  const resolvedPriorityFiles = priorityFiles.map(pf =>
    eligibleFiles.find(ef => ef.replace(/\\/g, '/').endsWith(pf))
  ).filter(Boolean) as string[];

  // Process priority files first
  let processed = 0;
  let skipped = 0;

  console.log('\n' + '═'.repeat(70));
  console.log('🎯 PROCESSING PRIORITY FILES');
  console.log('═'.repeat(70));

  for (const file of resolvedPriorityFiles) {
    const wasProcessed = await processFile(file);
    if (wasProcessed) {
      processed++;
    } else {
      skipped++;
    }
  }

  console.log('\n' + '═'.repeat(70));
  console.log('📋 PROCESSING REMAINING FILES');
  console.log('═'.repeat(70));

  for (const file of nonPriorityFiles) {
    const wasProcessed = await processFile(file);
    if (wasProcessed) {
      processed++;
    } else {
      skipped++;
    }
  }

  console.log('\n' + '═'.repeat(70));
  console.log('📊 SUMMARY');
  console.log('═'.repeat(70));
  console.log(`Total files checked: ${eligibleFiles.length}`);
  console.log(`Files processed: ${processed}`);
  console.log(`Files skipped (already processed): ${skipped}`);
  console.log('\n✨ Tone elevation complete!');
}

main().catch(console.error);
