import { analyzeRepository } from '../agent/src/tools/repository-analyzer';
import * as fs from 'fs/promises';
import * as path from 'path';

async function main() {
  console.log('Running repository analysis...');
  try {
    const report = await analyzeRepository();
    console.log('Analysis complete. Updating report file...');

    const reportPath = path.join(process.cwd(), 'operations', 'repository-health-report.md');
    
    // Read the existing file to preserve the frontmatter
    const existingContent = await fs.readFile(reportPath, 'utf-8');
    const frontmatterMatch = existingContent.match(/---[\s\S]*?---/);
    const frontmatter = frontmatterMatch ? frontmatterMatch[0] : '';
    
    const newContent = `${frontmatter}\n\n# Repository Health Report\n\n${report}`;

    await fs.writeFile(reportPath, newContent, 'utf-8');
    
    console.log('Successfully updated operations/repository-health-report.md');
    console.log('\n--- REPORT PREVIEW ---');
    console.log(report);
    console.log('--- END REPORT PREVIEW ---');

  } catch (error) {
    console.error('An error occurred while running the analysis:', error);
  }
}

main();
