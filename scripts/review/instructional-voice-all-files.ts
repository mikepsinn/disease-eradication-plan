import { getBookFilesForProcessing } from '../lib/file-utils';
import { fixInstructionalVoiceWithLLM } from './instructional-voice-utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Getting all book files (excluding references.qmd)...');

  const allFiles = await getBookFilesForProcessing();

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

  for (const file of allFiles) {
    processedCount++;
    console.log(`\n[${processedCount}/${allFiles.length}] Processing ${file}...`);

    try {
      const changes = await fixInstructionalVoiceWithLLM(file);
      totalChanges += changes;
      if (changes > 0) {
        filesChanged++;
        console.log(`✅ Made ${changes} changes to ${file}`);
      } else {
        console.log(`✓ No changes needed for ${file}`);
      }
    } catch (error) {
      console.error(`Error processing ${file}:`, error);
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