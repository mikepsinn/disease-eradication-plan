import fs from 'fs/promises';
import {
  generateClaudeOpus41Content,
  extractJsonFromResponse,
  loadPromptTemplate
} from '../lib/llm';
import {
  readFileWithMatter,
  updateFileWithHash
} from '../lib/file-utils';

interface ToneReplacement {
  find: string;
  replace: string;
  reason: string;
}

interface ToneResponse {
  status: 'changes_needed' | 'no_changes_needed';
  replacements: ToneReplacement[];
}

/**
 * Elevates the tone and voice of a file to be more wry, philosophical, and detached
 * in the style of Vonnegut, Handey, and Cunk
 */
export async function elevateToneWithLLM(filePath: string): Promise<void> {
  console.log(`\n📝 Elevating tone and voice for ${filePath}...`);
  const { frontmatter, body } = await readFileWithMatter(filePath);

  // Load the prompt template with examples
  const prompt = await loadPromptTemplate('scripts/prompts/elevate-tone-voice.md', {
    '{{filePath}}': filePath,
    '{{content}}': body
  });

  // Get response from Claude Opus
  const responseText = await generateClaudeOpus41Content(prompt);

  // Parse JSON response
  let response: ToneResponse;
  try {
    response = extractJsonFromResponse<ToneResponse>(responseText);
  } catch (error) {
    console.error(`❌ Failed to parse LLM response as JSON:`, error);
    console.error('Response was:', responseText);
    return;
  }

  // Check if changes are needed
  if (response.status === 'no_changes_needed' || !response.replacements || response.replacements.length === 0) {
    console.log(`✅ File ${filePath} already has appropriate tone. Updating metadata.`);
    await updateFileWithHash(filePath, body, frontmatter, 'lastToneElevationHash');
    return;
  }

  // Apply replacements
  let modifiedBody = body;
  let replacementCount = 0;

  console.log(`\n🔄 Applying ${response.replacements.length} tone improvements:`);

  for (const replacement of response.replacements) {
    // Count occurrences
    const occurrences = (modifiedBody.match(new RegExp(escapeRegExp(replacement.find), 'g')) || []).length;

    if (occurrences === 0) {
      console.warn(`  ⚠ Could not find text to replace: "${replacement.find.substring(0, 50)}..."`);
      continue;
    } else if (occurrences > 1) {
      console.warn(`  ⚠ Found ${occurrences} occurrences of: "${replacement.find.substring(0, 50)}..."`);
      console.warn(`     Replacing all occurrences.`);
    }

    // Perform replacement
    modifiedBody = modifiedBody.replace(replacement.find, replacement.replace);
    replacementCount++;

    // Log the change
    console.log(`  ✓ Transformed: "${replacement.find.substring(0, 40)}..."`);
    console.log(`    → "${replacement.replace.substring(0, 40)}..."`);
    console.log(`    Reason: ${replacement.reason}`);
  }

  if (replacementCount === 0) {
    console.log(`⚠ No replacements could be applied. File unchanged.`);
    return;
  }

  // Save the modified file
  await updateFileWithHash(filePath, modifiedBody, frontmatter, 'lastToneElevationHash');
  console.log(`\n✅ Successfully elevated tone for ${filePath} (${replacementCount} changes applied).`);
}

/**
 * Utility function to escape special regex characters
 */
function escapeRegExp(string: string): string {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Get files that need tone elevation (haven't been checked or content has changed)
 */
export async function getStaleFilesForTone(directory: string): Promise<string[]> {
  const { glob } = await import('glob');
  const files = await glob(`${directory}/**/*.qmd`, {
    ignore: [
      '**/node_modules/**',
      '**/_book/**',
      '**/.quarto/**'
    ]
  });

  const staleFiles: string[] = [];

  for (const file of files) {
    const { frontmatter, body } = await readFileWithMatter(file);
    const currentHash = await import('../lib/file-utils').then(m => m.getBodyHash(body));

    if (!frontmatter.lastToneElevationHash || frontmatter.lastToneElevationHash !== currentHash) {
      staleFiles.push(file);
    }
  }

  return staleFiles;
}