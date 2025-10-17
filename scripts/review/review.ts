import { 
  getStaleFiles, 
  formatFileWithLLM, 
  styleFileWithLLM, 
  factCheckFileWithLLM, 
  linkCheckFile, 
  figureCheckFile 
} from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Starting comprehensive review process...');

  // For now, we'll use the hash-based getStaleFiles. 
  // This could be updated to the date-based logic from get-stale-files.ts if preferred.
  const staleFiles = await getStaleFiles('lastFormattedHash');
  const bookFiles = staleFiles.filter(file => file.startsWith('brain\\book'));

  if (bookFiles.length === 0) {
    console.log('All files in brain/book are up-to-date. No review needed.');
    return;
  }

  console.log(`Found ${bookFiles.length} stale files in brain/book to review.`);

  for (const file of bookFiles) {
    console.log(`\n--- Processing: ${file} ---`);
    try {
      // Step 1: Format file (auto-fixes)
      await formatFileWithLLM(file);

      // Step 2: Style file (auto-fixes)
      await styleFileWithLLM(file);

      // Step 3: Fact Check (reports warnings)
      await factCheckFileWithLLM(file);

      // Step 4: Link Check (reports warnings)
      await linkCheckFile(file);

      // Step 5: Figure Check (reports warnings)
      await figureCheckFile(file);

    } catch (error) {
      console.error(`An error occurred while processing ${file}:`, error);
      // Continue to the next file
    }
  }

  console.log('\nComprehensive review process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred during the review process:', err);
  process.exit(1);
});
