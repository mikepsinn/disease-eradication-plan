require('dotenv').config();
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');
const openai = new OpenAI(process.env.OPENAI_API_KEY);

// Get configuration from environment variables
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-4'; // Default to gpt-4 if not specified

// Directory structure from reorganize.js
const newStructure = {
  docs: ['architecture', 'governance', 'api', 'getting-started', 'contributing'],
  'clinical-trials': ['protocols', 'methodologies', 'templates', 'validation', 'decentralized-methods'],
  'data-standards': ['schemas', 'ontologies', 'interoperability'],
  analytics: ['models', 'algorithms', 'validation'],
  platform: ['smart-contracts', 'security', 'integration', 'features', 'plugins'],
  regulatory: ['frameworks', 'compliance', 'legal', 'privacy'],
  'knowledge-base': ['interventions', 'conditions', 'biomarkers', 'research-database'],
  community: ['governance', 'partnerships', 'incentives', 'case-studies'],
  technical: ['infrastructure', 'deployment', 'maintenance', 'monitoring'],
  assets: ['images', 'diagrams', 'presentations', 'media'],
  'supporting-materials': ['research-papers', 'white-papers', 'presentations', 'use-cases']
};

// Files and directories to ignore
const ignoreList = [
  '.git',
  'node_modules',
  '.env',
  'package.json',
  'package-lock.json',
  '.gitignore',
  'scripts',
  '.vscode',
  '.idea'
];

// Function to check if path should be ignored
function shouldIgnore(filePath) {
  return ignoreList.some(ignored => filePath.includes(ignored));
}

// Function to get all files recursively
async function getAllFiles(dir) {
  const files = [];
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    if (shouldIgnore(fullPath)) continue;

    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      files.push(...await getAllFiles(fullPath));
    } else {
      files.push(fullPath);
    }
  }

  return files;
}

// Function to analyze file content and get suggested location
async function analyzeFile(filePath, content) {
  try {
    const prompt = `Given this file path: "${filePath}" and its content (first 1000 chars): "${content.substring(0, 1000)}..."

Please analyze where this file should be placed in the following structure and respond ONLY with a JSON object in this exact format:
{
  "targetDirectory": "main-category/sub-category",
  "reason": "Brief explanation of why this is the best location",
  "action": "move|delete|skip",
  "priority": 1-5 (1 being highest priority to move)
}

Available structure:
${JSON.stringify(newStructure, null, 2)}`;

    const completion = await openai.chat.completions.create({
      model: OPENAI_MODEL,
      messages: [{ role: "user", content: prompt }],
      temperature: 0.3,
      max_tokens: 500
    });

    return JSON.parse(completion.choices[0].message.content);
  } catch (error) {
    console.error(`Error analyzing file ${filePath}:`, error);
    return null;
  }
}

// Function to move file to new location
function moveFile(sourcePath, targetDir) {
  try {
    const fileName = path.basename(sourcePath);
    const targetPath = path.join(process.cwd(), targetDir, fileName);
    
    // Create target directory if it doesn't exist
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    
    // Move the file
    fs.renameSync(sourcePath, targetPath);
    return true;
  } catch (error) {
    console.error(`Error moving file ${sourcePath}:`, error);
    return false;
  }
}

// Main migration function
async function migrateContent() {
  try {
    // Get all files
    const files = await getAllFiles(process.cwd());
    const migrations = [];

    // Analyze each file
    for (const file of files) {
      const relativePath = path.relative(process.cwd(), file);
      console.log(`Analyzing: ${relativePath}`);
      
      const content = fs.readFileSync(file, 'utf8');
      const analysis = await analyzeFile(relativePath, content);
      
      if (analysis) {
        migrations.push({
          file: relativePath,
          ...analysis
        });
      }
    }

    // Sort migrations by priority
    migrations.sort((a, b) => a.priority - b.priority);

    // Execute migrations
    console.log('\nExecuting migrations...\n');
    for (const migration of migrations) {
      console.log(`\nProcessing: ${migration.file}`);
      console.log(`Target: ${migration.targetDirectory}`);
      console.log(`Reason: ${migration.reason}`);
      console.log(`Action: ${migration.action}`);

      switch (migration.action) {
        case 'move':
          if (moveFile(migration.file, migration.targetDirectory)) {
            console.log('✓ Moved successfully');
          }
          break;
        case 'delete':
          fs.unlinkSync(migration.file);
          console.log('✓ Deleted successfully');
          break;
        case 'skip':
          console.log('✓ Skipped');
          break;
      }
    }

    console.log('\nMigration completed!');
  } catch (error) {
    console.error('Migration failed:', error);
  }
}

// Run migration
migrateContent(); 