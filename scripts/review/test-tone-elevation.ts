#!/usr/bin/env node

/**
 * Demonstration script showing how tone elevation would work
 * This version applies pre-defined transformations to show the concept
 */

import { readFileWithMatter } from '../lib/file-utils';
import fs from 'fs/promises';

// Define transformation rules based on the examples from the prompt
const toneTransformations = [
  {
    find: "This isn't a protest. It's a business plan for a hostile takeover of humanity's priorities.",
    replace: "This is not a protest. It's more like when someone realizes they've been paying for the wrong subscription service for years and decides to switch providers.",
    reason: "Replaces aggressive 'hostile takeover' with mundane comparison"
  },
  {
    find: "The target is the global death industry.",
    replace: "The target is the curious human tradition of spending more money on ways to die than ways to live, which future historians will find adorable.",
    reason: "Adds philosophical distance and gentle irony"
  },
  {
    find: "The strategy is a simple, three-step algorithm to bankrupt the status quo.",
    replace: "The strategy involves three steps, much like a waltz, except instead of dancing we're suggesting humanity try not dying quite so much.",
    reason: "Uses absurdist comparison instead of aggressive language"
  },
  {
    find: "This isn't a petition; it's a political kill list.",
    replace: "This isn't a petition so much as a gentle reminder to politicians that voters exist and occasionally have opinions about not dying.",
    reason: "Transforms threat into understated observation"
  },
  {
    find: "This isn't a revolution. It's an acquisition. And you will not be outbid.",
    replace: "So it goes. Humanity might simply purchase a better future, the way one might buy a sensible coat after years of freezing in a fashionable but impractical jacket.",
    reason: "Replaces aggressive ultimatum with Vonnegut-style fatalistic optimism"
  }
];

async function demonstrateToneElevation(filePath: string) {
  console.log('🎭 TONE ELEVATION DEMONSTRATION');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  console.log('This demonstration shows how aggressive/pompous language');
  console.log('would be transformed into a more elevated, wry voice.\n');

  const { body } = await readFileWithMatter(filePath);

  console.log(`📄 Analyzing: ${filePath}\n`);

  let modifiedBody = body;
  let changesFound = 0;

  console.log('🔍 Searching for phrases to transform...\n');

  for (const transformation of toneTransformations) {
    if (body.includes(transformation.find)) {
      changesFound++;
      modifiedBody = modifiedBody.replace(transformation.find, transformation.replace);

      console.log(`✓ FOUND MATCH #${changesFound}:`);
      console.log(`  Original: "${transformation.find}"`);
      console.log(`  → New: "${transformation.replace}"`);
      console.log(`  Reason: ${transformation.reason}\n`);
    }
  }

  if (changesFound === 0) {
    console.log('ℹ️ No exact matches found from our example transformations.');
    console.log('\n📝 However, here are other phrases that would be transformed:\n');

    // Show additional examples of what would be changed
    const potentialChanges = [
      {
        original: "Weaponize Public Opinion",
        transformed: "Gently Suggest Alternative Priorities to the Public",
        reason: "Removes militaristic language"
      },
      {
        original: "Execute the Takeover",
        transformed: "Proceed with the Transition",
        reason: "Softens aggressive action verb"
      },
      {
        original: "buy the political establishment",
        transformed: "offer reasonable incentives to elected representatives",
        reason: "Reframes cynical language more neutrally"
      },
      {
        original: "makes the defense lobby look poor",
        transformed: "provides somewhat more resources than traditional lobbying groups",
        reason: "Uses understatement instead of boasting"
      }
    ];

    for (const change of potentialChanges) {
      console.log(`  • "${change.original}"`);
      console.log(`    → "${change.transformed}"`);
      console.log(`    (${change.reason})\n`);
    }
  } else {
    // Save the demonstration output
    const outputPath = filePath.replace('.qmd', '-tone-elevated-demo.qmd');
    await fs.writeFile(outputPath, modifiedBody, 'utf-8');
    console.log(`\n📝 Demonstration output saved to: ${outputPath}`);
  }

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('✨ DEMONSTRATION COMPLETE');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  if (changesFound > 0) {
    console.log(`Summary: Found and transformed ${changesFound} aggressive phrases.`);
    console.log('\nThe full implementation would use Claude Opus to identify');
    console.log('and transform ALL aggressive/pompous language throughout');
    console.log('the document, not just these specific examples.');
  } else {
    console.log('The full implementation would use Claude Opus to identify');
    console.log('similar patterns throughout the document and transform them');
    console.log('into the desired wry, philosophical voice.');
  }
}

async function main() {
  const filePath = process.argv[2] || 'brain/book/strategy-overview.qmd';

  if (!await fs.access(filePath).then(() => true).catch(() => false)) {
    console.error(`❌ Error: File not found at ${filePath}`);
    process.exit(1);
  }

  await demonstrateToneElevation(filePath);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});