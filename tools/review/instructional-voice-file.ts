import { fixInstructionalVoiceWithLLM } from './instructional-voice-utils';
import fs from 'fs';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Please provide a file path as an argument.');
    console.error('Usage: npx tsx scripts/review/instructional-voice-file.ts <file-path>');
    process.exit(1);
  }

  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found at ${filePath}`);
    process.exit(1);
  }

  try {
    console.log(`\n🔍 Checking instructional voice in: ${filePath}\n`);
    const changesMade = await fixInstructionalVoiceWithLLM(filePath);

    if (changesMade === 0) {
      console.log('\n✅ File already uses proper instructional voice!');
    } else {
      console.log(`\n✅ Successfully fixed ${changesMade} instructional voice issues.`);
    }
  } catch (error) {
    console.error('An error occurred:', error);
    process.exit(1);
  }
}

main();