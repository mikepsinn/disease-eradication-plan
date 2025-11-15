import fs from 'fs/promises';
import { readFileWithMatter, updateFileWithHash, stringifyWithFrontmatter } from '../lib/file-utils';
import { generateGeminiProContent, extractJsonFromResponse, loadPromptTemplate } from '../lib/llm';

interface InstructionalVoiceReplacement {
  find: string;
  replace: string;
  reason: string;
  lineNumber?: number;
}

interface InstructionalVoiceResponse {
  status: 'changes_needed' | 'no_changes_needed';
  replacements?: InstructionalVoiceReplacement[];
}

export async function fixInstructionalVoiceWithLLM(filePath: string, testMode: boolean = false): Promise<number> {
  console.log(`\nChecking instructional voice in ${filePath}...`);
  const { frontmatter, body } = await readFileWithMatter(filePath);

  // Load the style guide
  const styleGuide = await fs.readFile('GUIDES/STYLE_GUIDE.md', 'utf-8');

  const prompt = await loadPromptTemplate('scripts/prompts/fix-instructional-voice.md', {
    '{{styleGuide}}': styleGuide,
    '{{filePath}}': filePath,
    '{{body}}': body
  });

  const responseText = await generateGeminiProContent(prompt);

  let response: InstructionalVoiceResponse;
  try {
    response = extractJsonFromResponse(responseText, `instructional voice response for ${filePath}`);
  } catch (error) {
    console.error(`❌ ERROR parsing response:`, error);
    return 0;
  }

  // Check if changes are needed
  if (response.status === 'no_changes_needed' || !response.replacements || response.replacements.length === 0) {
    console.log(`✅ File ${filePath} already uses proper instructional voice.`);
    if (!testMode) {
      await updateFileWithHash(filePath, body, frontmatter, 'lastInstructionalVoiceHash');
    }
    return 0;
  }

  // Show proposed changes
  console.log(`\n📝 Found ${response.replacements.length} instances to fix:`);

  let updatedBody = body;
  let successfulChanges = 0;

  for (let i = 0; i < response.replacements.length; i++) {
    const replacement = response.replacements[i];
    console.log(`\n  ${i + 1}. ${replacement.reason}`);
    console.log(`     From: "${replacement.find.substring(0, 80)}${replacement.find.length > 80 ? '...' : ''}"`);
    console.log(`     To:   "${replacement.replace.substring(0, 80)}${replacement.replace.length > 80 ? '...' : ''}"`);

    if (!testMode) {
      // Check if the text to find actually exists
      if (updatedBody.includes(replacement.find)) {
        updatedBody = updatedBody.replace(replacement.find, replacement.replace);
        successfulChanges++;
      } else {
        console.warn(`     ⚠️  Could not find exact text to replace. Skipping.`);
      }
    } else {
      // In test mode, just check if we could find the text
      if (body.includes(replacement.find)) {
        successfulChanges++;
      } else {
        console.warn(`     ⚠️  Could not find exact text to replace. Would skip.`);
      }
    }
  }

  if (!testMode && successfulChanges > 0) {
    // Save the updated file
    const newContent = stringifyWithFrontmatter(updatedBody, frontmatter);
    await fs.writeFile(filePath, newContent, 'utf-8');
    console.log(`\n✅ Successfully fixed ${successfulChanges} instructional voice issues in ${filePath}`);

    // Update hash to prevent re-running
    await updateFileWithHash(filePath, updatedBody, frontmatter, 'lastInstructionalVoiceHash');
  } else if (testMode) {
    console.log(`\n🔍 Test mode: Would fix ${successfulChanges} issues`);
  } else {
    console.log(`\n⚠️  No replacements could be applied (text not found)`);
    // Still update hash to prevent re-running on unchanged file
    await updateFileWithHash(filePath, body, frontmatter, 'lastInstructionalVoiceHash');
  }

  return successfulChanges;
}