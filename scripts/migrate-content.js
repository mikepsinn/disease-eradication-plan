require('dotenv').config();

const fs = require('fs');
const path = require('path');
const { ignoreList, shouldIgnore, getAllFiles } = require('./shared-utilities');
const { analyzeFileLocation, validateAnalysis } = require('./file-path-analyzer');


async function processFile(filePath) {
  try {
    if (shouldIgnore(filePath)) {
      console.log(`Skipping ignored file: ${filePath}\n`);
      return;
    }
    console.log(`\n=== Processing ${path.basename(filePath)} ===`);
    
    const content = fs.readFileSync(filePath, 'utf8');
    const analysis = await analyzeFileLocation(filePath, content);

    console.log('Pre-validation analysis:', JSON.stringify(analysis, null, 2));
    validateAnalysis(analysis);

    // Process the file based on analysis
    const { action, targetDirectory, confidence, reason } = analysis;
    console.log(`- Action: ${action}`);
    console.log(`- Target: ${targetDirectory}`);
    console.log(`- Confidence: ${confidence}`);
    console.log(`- Reason: ${reason}\n`);

    if (action === 'move' && targetDirectory) {
      const targetPath = path.join(process.cwd(), targetDirectory, path.basename(filePath));
      fs.mkdirSync(path.dirname(targetPath), { recursive: true });
      fs.renameSync(filePath, targetPath);
    }
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    console.log('Current analysis state:', JSON.stringify(analysis || {}, null, 2));
  }
}

async function migrateContent(sourceDir) {
  try {
    let processedCount = 0;
    let successCount = 0;
    let errorCount = 0;
    
    const files = await getAllFiles(sourceDir, ['.md', '.html']);
    console.log(`Found ${files.length} markdown/HTML files to process\n`);
    
    for (const file of files) {
      await processFile(file);
      processedCount++;
    }
    
    console.log('\nMigration Summary:');
    console.log(`- Total files: ${files.length}`);
    console.log(`- Processed: ${processedCount}`);
    console.log(`- Successes: ${successCount}`);
    console.log(`- Errors: ${errorCount}`);
  } catch (error) {
    console.error('Migration failed:', error.message);
    process.exit(1);
  }
}

// If running directly (not imported as module)
if (require.main === module) {
  const sourceDir = process.argv[2] || process.cwd();
  migrateContent(sourceDir);
}

module.exports = {
  migrateContent,
  processFile
};