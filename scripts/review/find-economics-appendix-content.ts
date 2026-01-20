import { getBookFilesForProcessing } from './utils';
import { generateGeminiFlashContent } from '../lib/llm';
import dotenv from 'dotenv';
import fs from 'fs/promises';
import path from 'path';

dotenv.config();

const ECONOMICS_FILE = 'knowledge/economics/1-pct-treaty-impact.qmd';

async function analyzeFile(economicsContent: string, filePath: string): Promise<string> {
  console.log(`\nAnalyzing: ${path.basename(filePath)}`);

  // Read the chapter/appendix file
  const fileContent = await fs.readFile(filePath, 'utf-8');

  const prompt = `You are analyzing content for an economics research paper about redirecting military spending to medical research.

ECONOMICS PAPER CONTENT:
${economicsContent}

---

CHAPTER/APPENDIX FILE (${path.basename(filePath)}):
${fileContent}

---

TASK: Does this chapter/appendix file contain valuable information, data, statistics, examples, or arguments that are NOT already covered in the economics paper but would strengthen the paper's appendix?

Consider:
- Concrete examples or case studies
- Statistical data or calculations
- Historical precedents
- Implementation details
- Supporting arguments or evidence
- Technical mechanisms or frameworks

If YES, provide:
1. Brief summary of what valuable content exists (2-3 sentences max)
2. Specific examples or quotes that should be extracted

If NO, just respond: "No valuable appendix content found."

Be concise and specific.`;

  const response = await generateGeminiFlashContent(prompt);

  // Check if there's valuable content
  if (response.toLowerCase().includes('no valuable')) {
    console.log(`  ✓ No valuable appendix content found`);
  } else {
    console.log(`  🔍 VALUABLE CONTENT FOUND:`);
    console.log(`  ${response.split('\n').join('\n  ')}`);
    console.log('');
  }

  return response;
}

async function main() {
  console.log('='.repeat(80));
  console.log('FIND VALUABLE CONTENT FOR 1-PCT-TREATY-IMPACT.QMD APPENDIX');
  console.log('='.repeat(80));
  console.log();

  // Read the economics paper
  console.log(`Reading base file: ${ECONOMICS_FILE}`);
  const economicsContent = await fs.readFile(ECONOMICS_FILE, 'utf-8');
  console.log(`✓ Loaded 1-pct-treaty-impact.qmd (${economicsContent.length} characters)`);
  console.log();

  // Get all book files
  const allBookFiles = await getBookFilesForProcessing();

  // Filter out:
  // - audience variants (-academic, -foundations)
  // - economics.qmd itself
  // - references and auto-generated files
  const filesToAnalyze = allBookFiles.filter(file => {
    const normalizedFile = file.replace(/\\/g, '/');

    // Exclude audience variants
    if (normalizedFile.includes('-academic.qmd')) return false;
    if (normalizedFile.includes('-foundations.qmd')) return false;

    // Exclude the 1% treaty impact paper itself and related files
    if (normalizedFile.includes('1-pct-treaty-impact.qmd')) return false;
    if (normalizedFile.includes('knowledge/economics/')) return false;

    return true;
  });

  console.log(`Found ${filesToAnalyze.length} files to analyze\n`);
  console.log('Press Ctrl+C to cancel, or wait 5 seconds to continue...\n');
  await new Promise(resolve => setTimeout(resolve, 5000));

  let processedCount = 0;
  let valuableContentFound = 0;

  for (const file of filesToAnalyze) {
    processedCount++;
    console.log(`[${processedCount}/${filesToAnalyze.length}]`);

    try {
      const response = await analyzeFile(economicsContent, file);

      if (!response.toLowerCase().includes('no valuable')) {
        valuableContentFound++;
      }
    } catch (error) {
      console.error(`  ❌ ERROR: ${error}`);
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log('ANALYSIS COMPLETE');
  console.log('='.repeat(80));
  console.log(`Total files analyzed: ${filesToAnalyze.length}`);
  console.log(`Files with valuable content: ${valuableContentFound}`);
  console.log('='.repeat(80));
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
