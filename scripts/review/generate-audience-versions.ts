import { getBookFilesForProcessing } from './utils';
import { readFileWithMatter, updateFileWithHash } from '../lib/file-utils';
import { generateGeminiProContent } from '../lib/llm';
import dotenv from 'dotenv';
import fs from 'fs/promises';
import path from 'path';

dotenv.config();

// Audience types and their instruction files
const AUDIENCES = {
  foundations: 'instructions-foundations-prompt.md',
  academic: 'instructions-academic-prompt.md',
} as const;

type AudienceType = keyof typeof AUDIENCES;

async function loadInstructionsForAudience(audience: AudienceType): Promise<string> {
  const instructionFile = path.join(__dirname, AUDIENCES[audience]);
  try {
    const content = await fs.readFile(instructionFile, 'utf-8');
    return content.trim();
  } catch (error) {
    throw new Error(`Could not load instructions for audience "${audience}" from ${instructionFile}: ${error}`);
  }
}

async function transformFileForAudience(
  sourceFilePath: string,
  targetFilePath: string,
  instruction: string
): Promise<void> {
  console.log(`\n  Transforming for audience: ${path.basename(targetFilePath)}...`);

  const { frontmatter, body } = await readFileWithMatter(sourceFilePath);

  const prompt = `${instruction}

---

FILE CONTENT:

${body}

---

INSTRUCTIONS:
1. Apply the audience-specific transformation rules above to the file content
2. Return ONLY the updated file content (without frontmatter)
3. If no changes are needed, return exactly: NO_CHANGES_NEEDED
4. Do NOT include markdown code fences (no \`\`\`) in your response
5. Preserve all existing formatting, spacing, structure, and ESPECIALLY all citations and references
6. Keep ALL quantitative data, statistics, and calculations unchanged
7. NEVER remove or modify citation links or reference tags`;

  const responseText = await generateGeminiProContent(prompt);

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`    ○ No transformation needed`);
    finalBody = body;
  } else {
    // Strip markdown code blocks if present
    let cleaned = responseText.trim();
    cleaned = cleaned.replace(/^```[a-z]*\n?/i, '');
    cleaned = cleaned.replace(/\n?```\s*$/i, '');
    finalBody = cleaned.trim();
    console.log(`    ✓ Transformed`);
  }

  // Write to target file with original frontmatter
  const hashField = 'lastAudienceTransformHash';
  await updateFileWithHash(targetFilePath, finalBody, frontmatter, hashField);
}

async function generateVersionForAudience(
  sourceFile: string,
  audience: AudienceType,
  instruction: string
): Promise<void> {
  // Generate target filename by inserting audience suffix before extension
  const parsedPath = path.parse(sourceFile);
  const targetFile = path.join(
    parsedPath.dir,
    `${parsedPath.name}-${audience}${parsedPath.ext}`
  );

  console.log(`\n  Source: ${path.basename(sourceFile)}`);
  console.log(`  Target: ${path.basename(targetFile)}`);

  // Copy source to target first
  try {
    await fs.copyFile(sourceFile, targetFile);
    console.log(`  ✓ Copied source to target`);
  } catch (error) {
    console.error(`  ✗ Failed to copy: ${error}`);
    throw error;
  }

  // Transform the target file
  await transformFileForAudience(sourceFile, targetFile, instruction);
}

async function main() {
  const args = process.argv.slice(2);

  // Parse audience type
  if (args.length === 0) {
    console.error('ERROR: No audience type provided.');
    console.error('\nUsage:');
    console.error('  npx tsx scripts/review/generate-audience-versions.ts <audience>');
    console.error('\nAvailable audiences:');
    Object.keys(AUDIENCES).forEach(aud => console.error(`  - ${aud}`));
    console.error('\nExamples:');
    console.error('  npx tsx scripts/review/generate-audience-versions.ts foundations');
    console.error('  npx tsx scripts/review/generate-audience-versions.ts academic');
    process.exit(1);
  }

  const audienceArg = args[0].toLowerCase();
  if (!(audienceArg in AUDIENCES)) {
    console.error(`ERROR: Unknown audience type "${audienceArg}"`);
    console.error('\nAvailable audiences:');
    Object.keys(AUDIENCES).forEach(aud => console.error(`  - ${aud}`));
    process.exit(1);
  }

  const audience = audienceArg as AudienceType;

  console.log('='.repeat(80));
  console.log('GENERATE AUDIENCE-SPECIFIC VERSIONS');
  console.log('='.repeat(80));
  console.log(`\nAudience: ${audience}`);
  console.log(`Suffix: -${audience}.qmd\n`);

  // Load instructions for this audience
  const instruction = await loadInstructionsForAudience(audience);
  console.log(`Loaded transformation rules from ${AUDIENCES[audience]}\n`);

  // Get all book files
  const allBookFiles = await getBookFilesForProcessing();

  // Exclude patterns - we only want source files (no existing audience versions)
  const excludedPatterns = [
    /references\.qmd$/,  // Exclude references
    /-foundations\.qmd$/,  // Exclude existing foundation versions
    /-academic\.qmd$/,     // Exclude existing academic versions
    /knowledge[\/\\]figures[\/\\]/,  // Exclude all figure files (code, not prose)
  ];

  const excludedFiles = [
    'index.qmd',
  ];

  // Filter to get only source files
  const sourceFiles = allBookFiles.filter(file => {
    // Normalize path for consistent matching
    const normalizedFile = file.replace(/\\/g, '/');

    // Check exact file matches
    if (excludedFiles.includes(path.basename(file))) return false;

    // Exclude figures folder (check before pattern matching)
    if (normalizedFile.includes('knowledge/figures/')) return false;

    // Check pattern matches
    if (excludedPatterns.some(pattern => pattern.test(normalizedFile))) return false;

    return true;
  });

  console.log(`Found ${allBookFiles.length} total book files`);
  console.log(`  - ${allBookFiles.length - sourceFiles.length} excluded (references, existing versions)`);
  console.log(`  - ${sourceFiles.length} source files to process\n`);

  if (sourceFiles.length === 0) {
    console.log('No source files to process!');
    return;
  }

  // Show files that will be processed
  console.log('Source files to transform:');
  sourceFiles.forEach(file => {
    const parsedPath = path.parse(file);
    const targetName = `${parsedPath.name}-${audience}${parsedPath.ext}`;
    console.log(`  ${path.basename(file)} → ${targetName}`);
  });
  console.log('\nPress Ctrl+C to cancel, or wait 5 seconds to continue...\n');

  await new Promise(resolve => setTimeout(resolve, 5000));

  let processedCount = 0;
  let successCount = 0;
  let errorCount = 0;

  for (const sourceFile of sourceFiles) {
    processedCount++;
    try {
      console.log(`\n[${ processedCount}/${sourceFiles.length}] Processing: ${path.basename(sourceFile)}`);

      await generateVersionForAudience(sourceFile, audience, instruction);

      successCount++;
      console.log(`  ✓ Successfully generated ${audience} version`);
    } catch (error) {
      errorCount++;
      console.error(`\n  ❌ ERROR processing ${sourceFile}:`, error);
      console.error('  Continuing with next file...\n');
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log('GENERATION COMPLETE');
  console.log('='.repeat(80));
  console.log(`Total files: ${sourceFiles.length}`);
  console.log(`  ✓ Success: ${successCount}`);
  console.log(`  ✗ Errors: ${errorCount}`);
  console.log('='.repeat(80));
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
