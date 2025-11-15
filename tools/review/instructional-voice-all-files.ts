import { getBookFilesForProcessing } from '../lib/file-utils';
import { fixInstructionalVoiceWithLLM } from './instructional-voice-utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('========================================');
  console.log('INSTRUCTIONAL VOICE FIX - ALL FILES');
  console.log('========================================');
  console.log('Starting at:', new Date().toISOString());
  console.log('\nGetting all book files (excluding references.qmd)...');

  const allFiles = await getBookFilesForProcessing();
  console.log('✓ File list retrieved');

  console.log(`Found ${allFiles.length} book files to process`);

  if (allFiles.length === 0) {
    console.log('No book files found!');
    return;
  }

  console.log('\nProcessing the following files:');
  allFiles.slice(0, 20).forEach(file => console.log(`  - ${file}`));
  if (allFiles.length > 20) {
    console.log(`  ... and ${allFiles.length - 20} more`);
  }

  let totalChanges = 0;
  let processedCount = 0;
  let filesChanged = 0;

  console.log('\nStarting to process files...');
  console.log('Note: Each file takes 5-20 seconds to analyze with the LLM\n');

  for (const file of allFiles) {
    processedCount++;
    const percent = Math.round((processedCount / allFiles.length) * 100);
    console.log(`\n========================================`);
    console.log(`[${processedCount}/${allFiles.length}] (${percent}%) Processing: ${file}`);
    console.log(`========================================`);

    try {
      const startTime = Date.now();
      const changes = await fixInstructionalVoiceWithLLM(file);
      const duration = ((Date.now() - startTime) / 1000).toFixed(1);

      totalChanges += changes;
      if (changes > 0) {
        filesChanged++;
        console.log(`✅ Made ${changes} changes to ${file} (${duration}s)`);
      } else {
        console.log(`✓ No changes needed for ${file} (${duration}s)`);
      }
    } catch (error) {
      console.error(`\n❌ FATAL ERROR processing ${file}:`, error);
      console.error('\nStopping script due to error.');
      console.error(`Progress: ${processedCount}/${allFiles.length} files processed`);
      console.error(`Changes made so far: ${totalChanges} across ${filesChanged} files`);
      process.exit(1);
    }
  }

  console.log(`\n✅ Instructional voice fixing complete.`);
  console.log(`Total changes made: ${totalChanges} across ${filesChanged} files`);
  console.log(`Files processed: ${processedCount}`);
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});