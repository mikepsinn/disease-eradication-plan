import 'dotenv/config';
import * as fs from 'fs';
import * as path from 'path';
import { ignoreList, shouldIgnore, getAllFiles } from './shared-utilities';
import { analyzeFileLocation, validateAnalysis } from './file-path-analyzer';
import { updateReferences } from './reference-updater';

interface MovedFile {
  originalPath: string;
  newPath: string;
  fileName: string;
}

async function processFile(filePath: string): Promise<MovedFile | undefined> {
  let analysis: any; // Use any for compatibility with dynamic analysis structure
  try {
    if (shouldIgnore(filePath)) {
      console.log(`Skipping ignored file: ${filePath}\n`);
      return;
    }
    console.log(`\n=== Processing ${path.basename(filePath)} ===`);
    
    const content = fs.readFileSync(filePath, 'utf8');
    analysis = await analyzeFileLocation(filePath, content);

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
      
      // Track moved files for reference updating
      const movedFile: MovedFile = {
        originalPath: filePath,
        newPath: targetPath,
        fileName: path.basename(filePath)
      };
      return movedFile;
    }
  } catch (error: any) {
    console.error(`Error processing ${filePath}:`, error.message);
    console.log('Current analysis state:', JSON.stringify(analysis || {}, null, 2));
    throw error;
  }
}

async function migrateContent(sourceDir: string): Promise<void> {
  try {
    let processedCount = 0;
    let successCount = 0;
    let errorCount = 0;
    
    const files = await getAllFiles(sourceDir, ['.md', '.html']);
    console.log(`Found ${files.length} markdown/HTML files to process\n`);
    
    const movedFiles: MovedFile[] = [];
    
    for (const file of files) {
      const result = await processFile(file);
      if (result) movedFiles.push(result);
      processedCount++;
    }
    
    // Add reference updating phase
    if (movedFiles.length > 0) {
      console.log('\nUpdating file references...');
      const allContentFiles = await getAllFiles(sourceDir, ['.md', '.html', '.js', '.ts', '.json']);
      await updateReferences(movedFiles, allContentFiles);
    }
    
    console.log('\nMigration Summary:');
    console.log(`- Total files: ${files.length}`);
    console.log(`- Processed: ${processedCount}`);
    console.log(`- Successes: ${successCount}`);
    console.log(`- Errors: ${errorCount}`);
  } catch (error: any) {
    console.error('Migration failed:', error.message);
    process.exit(1);
  }
}

// If running directly (not imported as module)
if (require.main === module) {
  const sourceDir = process.argv[2] || process.cwd();
  migrateContent(sourceDir);
}

export {
  migrateContent,
  processFile
}; 