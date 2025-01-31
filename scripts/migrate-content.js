require('dotenv').config();

const fs = require('fs');
const path = require('path');
const { ignoreList, shouldIgnore, getAllFiles } = require('./shared-utilities');
const { analyzeFileLocation, validateAnalysis } = require('./file-path-analyzer');
const LLMClient = require('./llm-client');

// Get configuration from environment variables
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-4';

// Directory structure from config
const { structure } = require('./config/structure');

// Initialize LLM client
const llmClient = new LLMClient(process.env.OPENAI_API_KEY, structure);

async function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const analysis = await analyzeFileLocation(filePath, content, {
      model: OPENAI_MODEL
    });

    validateAnalysis(analysis);

    // Process the file based on analysis
    const { action, targetDirectory, confidence, reason } = analysis;
    console.log(`Processing ${filePath}:`);
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
  }
}

async function migrateContent(sourceDir) {
  try {
    const files = await getAllFiles(sourceDir);
    console.log(`Found ${files.length} files to process\n`);
    
    for (const file of files) {
      await processFile(file);
    }
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