const fs = require('fs').promises;
const path = require('path');
const LLMClient = require('../llm-client');
const {
  FrontmatterGenerator,
  findMarkdownFiles,
} = require('../fix_frontmatter_metadata');

describe('Frontmatter Metadata Integration Tests', () => {
  let generator;
  const testDir = path.resolve(__dirname, '../../fdai');

  beforeAll(async () => {
    // Use real LLM client
    const llmClient = new LLMClient();
    generator = new FrontmatterGenerator(llmClient);
  });

  test('should find markdown files in fdai directory', async () => {
    const files = await findMarkdownFiles(testDir);
    expect(files.length).toBeGreaterThan(0);
    console.log('Found files:', files);
  });

  test('should process a single file with real LLM client', async () => {
    // Get first markdown file from fdai directory
    const files = await findMarkdownFiles(testDir);
    expect(files.length).toBeGreaterThan(0);

    const testFile = files[0];
    console.log('Testing with file:', testFile);

    // Make a backup of the file
    const content = await fs.readFile(testFile, 'utf8');
    const backupPath = `${testFile}.backup`;
    await fs.writeFile(backupPath, content);

    try {
      // Process the file with real LLM client
      const result = await generator.processFile(testFile);
      console.log('Process result:', result);

      // Read the processed file
      const processedContent = await fs.readFile(testFile, 'utf8');
      console.log('Processed content:', processedContent);

      // Verify the result
      expect(result).toBeDefined();
      if (result.error) {
        console.error('Processing error:', result.error);
      }
      
    } finally {
      // Restore the backup
      await fs.copyFile(backupPath, testFile);
      await fs.unlink(backupPath);
    }
  });

  test('should process all files in fdai directory', async () => {
    const files = await findMarkdownFiles(testDir);
    expect(files.length).toBeGreaterThan(0);

    // Make backups of all files
    const backups = await Promise.all(files.map(async file => {
      const content = await fs.readFile(file, 'utf8');
      const backupPath = `${file}.backup`;
      await fs.writeFile(backupPath, content);
      return { file, backupPath };
    }));

    try {
      // Process each file
      const results = await Promise.all(files.map(async file => {
        console.log('\nProcessing:', file);
        const result = await generator.processFile(file);
        console.log('Result:', result);
        
        if (result.error) {
          console.error('Error processing file:', file);
          console.error('Error details:', result.error);
        }
        
        return { file, result };
      }));

      // Analyze results
      const summary = results.reduce((acc, { file, result }) => {
        acc.total++;
        if (result.updated) acc.updated++;
        if (result.error) acc.errors++;
        return acc;
      }, { total: 0, updated: 0, errors: 0 });

      console.log('\nProcessing Summary:');
      console.log(`Total files: ${summary.total}`);
      console.log(`Updated: ${summary.updated}`);
      console.log(`Errors: ${summary.errors}`);

      expect(summary.total).toEqual(files.length);
      
    } finally {
      // Restore all backups
      await Promise.all(backups.map(async ({ file, backupPath }) => {
        await fs.copyFile(backupPath, file);
        await fs.unlink(backupPath);
      }));
    }
  });
}); 