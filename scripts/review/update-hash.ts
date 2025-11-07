#!/usr/bin/env tsx
import { readFileWithMatter, updateFileWithHash } from '../lib/file-utils';
import { HASH_FIELDS, isValidHashField, getHashFieldDisplayName, type HashFieldName } from '../lib/constants';
import path from 'path';

const filePath = process.argv[2];
const hashFieldArg = process.argv[3];

function printUsage() {
  console.log('Usage: npx tsx scripts/review/update-hash.ts <file-path> [hash-field]');
  console.log('\nAvailable hash fields:');
  Object.entries(HASH_FIELDS).forEach(([key, value]) => {
    console.log(`  ${key.padEnd(25)} → ${value}`);
  });
  console.log('\nExample:');
  console.log('  npx tsx scripts/review/update-hash.ts brain/book/theory.qmd TONE_ELEVATION_WITH_HUMOR');
  console.log('  npx tsx scripts/review/update-hash.ts brain/book/theory.qmd lastToneElevationWithHumorHash');
}

async function main() {
  if (!filePath) {
    console.error('❌ Error: No file path provided\n');
    printUsage();
    process.exit(1);
  }

  // Determine the hash field to use
  let hashField: HashFieldName;

  if (!hashFieldArg) {
    // Default to tone elevation with humor
    hashField = HASH_FIELDS.TONE_ELEVATION_WITH_HUMOR;
    console.log(`ℹ️  No hash field specified, using default: ${hashField}`);
  } else if (hashFieldArg in HASH_FIELDS) {
    // User provided a key like "TONE_ELEVATION_WITH_HUMOR"
    hashField = HASH_FIELDS[hashFieldArg as keyof typeof HASH_FIELDS];
  } else if (isValidHashField(hashFieldArg)) {
    // User provided the actual field name like "lastToneElevationWithHumorHash"
    hashField = hashFieldArg;
  } else {
    console.error(`❌ Error: Invalid hash field: ${hashFieldArg}\n`);
    printUsage();
    process.exit(1);
  }

  try {
    const { frontmatter, body } = await readFileWithMatter(filePath);
    await updateFileWithHash(filePath, body, frontmatter, hashField);

    const fileName = path.basename(filePath);
    const displayName = getHashFieldDisplayName(hashField);

    console.log(`✅ Updated ${displayName} hash for ${fileName}`);
    console.log(`   Field: ${hashField}`);
    console.log(`   File: ${filePath}`);
  } catch (error) {
    console.error(`❌ Error updating hash:`, error);
    process.exit(1);
  }
}

main().catch(console.error);
