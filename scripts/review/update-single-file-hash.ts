/**
 * Update the hash for a single file
 */

import { updateFileWithHash, readFileWithMatter } from '../lib/file-utils';
import { HASH_FIELDS } from '../lib/constants';

async function main() {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error('Usage: tsx update-single-file-hash.ts <file-path>');
    process.exit(1);
  }

  const { frontmatter, body } = await readFileWithMatter(filePath);
  await updateFileWithHash(filePath, body, frontmatter, HASH_FIELDS.TONE_ELEVATION_WITH_HUMOR);
  console.log(`✓ Updated hash for ${filePath}`);
}

main().catch(console.error);
