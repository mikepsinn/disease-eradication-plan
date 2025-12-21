import { getBookFilesForProcessing } from './utils';
import { updateFileWithHash } from '../lib/file-utils';
import { generateGeminiFlashContent } from '../lib/llm';
import dotenv from 'dotenv';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// ES module equivalent of __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config();

// Audience types and their instruction files
const AUDIENCES = {
  foundations: 'instructions-foundations-prompt.md',
  academic: 'instructions-academic-prompt.md',
} as const;

type AudienceType = keyof typeof AUDIENCES;

/**
 * Update QMD links to point to the same audience version
 * Excludes: figures/, references.qmd, parameters-and-calculations.qmd
 */
function updateQmdLinks(content: string, audience: AudienceType): string {
  // Match markdown links: [text](path.qmd) or [text](path.qmd#anchor)
  return content.replace(/\[([^\]]+)\]\(([^)]+\.qmd(?:#[^)]*)?)\)/g, (match, linkText, linkPath) => {
    // Check if this link should be excluded
    const normalizedPath = linkPath.toLowerCase();

    // Exclude references.qmd
    if (normalizedPath.includes('references.qmd')) {
      return match;
    }

    // Exclude parameters-and-calculations.qmd
    if (normalizedPath.includes('parameters-and-calculations.qmd')) {
      return match;
    }

    // Exclude anything in figures/ folder
    if (normalizedPath.includes('/figures/')) {
      return match;
    }

    // Exclude if already has an audience suffix
    if (normalizedPath.includes('-foundations.qmd') || normalizedPath.includes('-academic.qmd')) {
      return match;
    }

    // Add audience suffix before .qmd (preserve any anchor)
    const updatedPath = linkPath.replace(/\.qmd(#.*)?$/, `-${audience}.qmd$1`);
    return `[${linkText}](${updatedPath})`;
  });
}

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
  instruction: string,
  audience: AudienceType
): Promise<void> {
  console.log(`\n  Transforming for audience: ${path.basename(targetFilePath)}...`);

  const matter = await import('gray-matter');
  const fs = await import('fs/promises');

  // Read the entire file content (frontmatter + body)
  const originalContent = await fs.readFile(sourceFilePath, 'utf-8');

  const prompt = `${instruction}

---

FILE CONTENT (complete .qmd file with YAML frontmatter):

${originalContent}

---

INSTRUCTIONS:
1. Apply the audience-specific transformation rules to the ENTIRE file
2. Transform frontmatter fields (title, description) to match the audience tone
3. Transform body content according to the rules
4. Keep technical frontmatter fields unchanged (author, date, etc.)
5. Return the COMPLETE transformed file with frontmatter and body
6. Do NOT include markdown code fences around your response
7. Preserve all existing formatting, spacing, structure, and ESPECIALLY all citations and references
8. Keep ALL quantitative data, statistics, and calculations unchanged
9. NEVER remove or modify citation links or reference tags

Return the complete .qmd file starting with --- and the YAML frontmatter.`;

  const responseText = await generateGeminiFlashContent(prompt);

  // Strip markdown code blocks if the LLM wrapped the response
  let cleanedResponse = responseText.trim();
  cleanedResponse = cleanedResponse.replace(/^```[a-z]*\n?/i, '');
  cleanedResponse = cleanedResponse.replace(/\n?```\s*$/i, '');

  // Parse the transformed content to extract frontmatter and body
  const { data: finalFrontmatter, content: body } = matter.default(cleanedResponse);

  // Update QMD links to point to the same audience version
  const finalBody = updateQmdLinks(body, audience);

  console.log(`    ✓ Transformed complete file`);

  // Write to target file with transformed frontmatter and body
  const hashField = 'lastAudienceTransformHash';
  await updateFileWithHash(targetFilePath, finalBody, finalFrontmatter, hashField);
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
  await transformFileForAudience(sourceFile, targetFile, instruction, audience);
}

async function main() {
  const args = process.argv.slice(2);

  // Parse arguments
  let specificFile: string | null = null;
  let audienceArg: string | null = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--file=')) {
      specificFile = args[i].substring('--file='.length);
    } else if (args[i] === '--file' || args[i] === '-f') {
      specificFile = args[++i];
    } else {
      audienceArg = args[i];
    }
  }

  // Parse audience type
  if (!audienceArg) {
    console.error('ERROR: No audience type provided.');
    console.error('\nUsage:');
    console.error('  npx tsx scripts/review/generate-audience-versions.ts <audience> [--file=<path>]');
    console.error('\nAvailable audiences:');
    Object.keys(AUDIENCES).forEach(aud => console.error(`  - ${aud}`));
    console.error('\nExamples:');
    console.error('  npx tsx scripts/review/generate-audience-versions.ts foundations');
    console.error('  npx tsx scripts/review/generate-audience-versions.ts academic --file=knowledge/solution.qmd');
    process.exit(1);
  }

  if (!(audienceArg.toLowerCase() in AUDIENCES)) {
    console.error(`ERROR: Unknown audience type "${audienceArg}"`);
    console.error('\nAvailable audiences:');
    Object.keys(AUDIENCES).forEach(aud => console.error(`  - ${aud}`));
    process.exit(1);
  }

  const audience = audienceArg.toLowerCase() as AudienceType;

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

  // Filter to specific file if requested
  let filesToProcess = sourceFiles;
  if (specificFile) {
    const absoluteSpecificFile = path.resolve(specificFile);
    filesToProcess = sourceFiles.filter(file => path.resolve(file) === absoluteSpecificFile);

    if (filesToProcess.length === 0) {
      console.error(`\nERROR: File not found or not a valid source file: ${specificFile}`);
      console.error('Make sure the file path is relative to the project root and is a source .qmd file (not -academic or -foundations)');
      process.exit(1);
    }

    console.log(`\nProcessing single file: ${specificFile}`);
  }

  console.log(`Found ${allBookFiles.length} total book files`);
  console.log(`  - ${allBookFiles.length - sourceFiles.length} excluded (references, existing versions)`);
  console.log(`  - ${filesToProcess.length} source file(s) to process\n`);

  if (filesToProcess.length === 0) {
    console.log('No source files to process!');
    return;
  }

  // Show files that will be processed
  console.log('Source files to transform:');
  filesToProcess.forEach(file => {
    const parsedPath = path.parse(file);
    const targetName = `${parsedPath.name}-${audience}${parsedPath.ext}`;
    console.log(`  ${path.basename(file)} → ${targetName}`);
  });
  console.log('\nPress Ctrl+C to cancel, or wait 5 seconds to continue...\n');

  await new Promise(resolve => setTimeout(resolve, 5000));

  let processedCount = 0;
  let successCount = 0;
  let errorCount = 0;

  for (const sourceFile of filesToProcess) {
    processedCount++;
    try {
      console.log(`\n[${ processedCount}/${filesToProcess.length}] Processing: ${path.basename(sourceFile)}`);

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
  console.log(`Total files: ${filesToProcess.length}`);
  console.log(`  ✓ Success: ${successCount}`);
  console.log(`  ✗ Errors: ${errorCount}`);
  console.log('='.repeat(80));
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
