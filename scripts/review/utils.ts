import fs from 'fs/promises';
import matter from 'gray-matter';
import { glob } from 'glob';
import path from 'path';
import { generateGeminiProContent, generateClaudeOpus41Content, extractJsonFromResponse, loadPromptTemplate, generateGeminiFlashContent } from '../lib/llm';
import { saveFile, getBodyHash, readFileWithMatter, updateFileWithHash, parseQuartoYml, getStaleFiles } from '../lib/file-utils';
import { parseReferences, formatReferencesFile, type Reference } from '../lib/references';

// Re-export functions from file-utils for convenience
export { getStaleFiles, parseQuartoYml };

export async function formatFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFormatting ${filePath} with Gemini...`);
  const { frontmatter, body } = await readFileWithMatter(filePath);

  const contentAndFormattingGuide = await fs.readFile('GUIDES/CONTENT_STANDARDS.md', 'utf-8');

  const prompt = await loadPromptTemplate('scripts/prompts/formatter.md', {
    '{{formattingGuide}}': contentAndFormattingGuide,
    '{{body}}': body
  });

  const responseText = await generateGeminiProContent(prompt);

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} is already formatted correctly. Updating metadata.`);
    finalBody = body;
  } else {
    finalBody = responseText.trim().replace(/(\s*---|\s*```)*\s*$/, '');
  }

  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastFormattedHash');
  console.log(`Successfully formatted ${filePath}.`);
}

export async function styleFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nImproving style and content quality for ${filePath} with Claude Opus...`);
  const { frontmatter, body } = await readFileWithMatter(filePath);

  const styleGuide = await fs.readFile('GUIDES/STYLE_GUIDE.md', 'utf-8');
  const prompt = await loadPromptTemplate('scripts/prompts/style-guide-review.md', {
    '{{styleGuide}}': styleGuide,
    '{{body}}': body
  });

  const responseText = await generateClaudeOpus41Content(prompt);

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} already adheres to the style guide. Updating metadata.`);
    finalBody = body;
  } else {
    finalBody = responseText.trim();
  }

  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastStyleHash');
  console.log(`Successfully improved style for ${filePath}.`);
}

export async function factCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFact-checking ${filePath} with Gemini...`);
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

  const frontmatterMatch = originalContent.match(/^---\n([\s\S]*?)\n---/);
  const originalFrontmatterText = frontmatterMatch ? frontmatterMatch[0] : null;

  let existingReferencesContent = '';
  let existingReferences: Reference[] = [];
  let referencesFrontmatter = '';

  try {
    existingReferencesContent = await fs.readFile('brain/book/references.qmd', 'utf-8');
    const refMatter = matter(existingReferencesContent);
    referencesFrontmatter = matter.stringify('', refMatter.data, { lineWidth: -1 } as any).trim();
    existingReferences = parseReferences(refMatter.content);
  } catch (error) {
    console.warn('Could not load references.qmd, will create new file');
  }

  const existingRefsSummary = existingReferences
    .map(ref => `- ID: ${ref.id}\n  Title: ${ref.title}\n  Quote: ${ref.quotes[0] || ''}`)
    .join('\n\n');

  const fileDir = path.dirname(filePath);
  const referencesPath = path.relative(fileDir, 'brain/book/references.qmd').replace(/\\/g, '/');

  let bookStructure = '';
  try {
    bookStructure = await fs.readFile('_quarto.yml', 'utf-8');
  } catch (error) {
    console.warn('Could not load _quarto.yml');
  }

  let prompt = await fs.readFile('scripts/prompts/fact-checker.md', 'utf-8');
  prompt = prompt.replace('{{referencesPath}}', referencesPath)
                 .replace('{{bookStructure}}', bookStructure)
                 .replace('{{existingRefsSummary}}', existingRefsSummary)
                 .replace('{{body}}', body);

  try {
    const responseText = await generateGeminiProContent(prompt);
    const resultData = extractJsonFromResponse(responseText, 'fact-check response');

    if (!resultData.updatedChapter) {
      throw new Error('LLM did not return updatedChapter');
    }
    body = resultData.updatedChapter;

    if (resultData.newReferences && resultData.newReferences.length > 0) {
      const newRefs: Reference[] = resultData.newReferences;
      const existingIds = new Set(existingReferences.map(r => r.id));
      const dedupedNewRefs = newRefs.filter(ref => {
        if (existingIds.has(ref.id)) {
          console.warn(`⚠ Skipping duplicate reference ID: ${ref.id}`);
          return false;
        }
        return true;
      });

      if (dedupedNewRefs.length > 0) {
        const allReferences = [...existingReferences, ...dedupedNewRefs];
        const newReferencesFile = formatReferencesFile(allReferences, referencesFrontmatter);
        await saveFile('brain/book/references.qmd', newReferencesFile);
        console.log(`✓ Added ${dedupedNewRefs.length} new reference(s) to references.qmd`);
      }
    } else {
      console.log(`✓ All claims linked to existing references (no new references added)`);
    }
  } catch (error) {
    console.error('Fact-check failed:', error);
    console.log('Skipping fact-check for this file');
  }

  frontmatter.lastFactCheckHash = getBodyHash(matter.stringify(body, frontmatter));

  let newContent: string;
  if (originalFrontmatterText) {
    const normalizedBody = body.trimEnd() + '\n';
    const updatedFrontmatter = originalFrontmatterText.replace(
      /(lastFactCheckHash:\s*)[^\n]*/,
      `$1${frontmatter.lastFactCheckHash}`
    );
    if (!updatedFrontmatter.includes('lastFactCheckHash:')) {
      newContent = originalFrontmatterText.replace(
        /\n---$/,
        `\nlastFactCheckHash: ${frontmatter.lastFactCheckHash}\n---`
      ) + '\n' + normalizedBody;
    } else {
      newContent = updatedFrontmatter + '\n' + normalizedBody;
    }
  } else {
    newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  }

  await saveFile(filePath, newContent);
  console.log(`Successfully updated ${filePath}`);
}

interface StructureComment {
  afterLine: number;
  type: 'CONTRADICTION' | 'DUPLICATION' | 'MISSING_REFERENCE' | 'OTHER';
  message: string;
  context: string;
}

interface StructureCheckResponse {
  status: 'issues_found' | 'no_changes_needed';
  comments: StructureComment[];
}

export async function structureCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nChecking structure of ${filePath} with Gemini...`);
  let { frontmatter, body } = await readFileWithMatter(filePath);

  const outlineContent = await fs.readFile('OUTLINE.md', 'utf-8');
  const { chapters, appendices } = await parseQuartoYml();

  if (appendices.includes(filePath)) {
    console.log(`File ${filePath} is already in appendix. Skipping structure check.`);
    return;
  }

  const otherChapters = chapters.filter(ch => ch !== filePath);

  const prompt = await loadPromptTemplate('scripts/prompts/structure-check.md', {
    '{{outlineContent}}': outlineContent,
    '{{otherChapters}}': otherChapters.join('\n'),
    '{{filePath}}': filePath,
    '{{body}}': body
  });

  const responseText = await generateGeminiProContent(prompt);

  // Parse JSON response
  let response: StructureCheckResponse;
  try {
    response = extractJsonFromResponse(responseText, `structure check response for ${filePath}`);
  } catch (error) {
    console.error(`❌ ERROR:`, error);
    return;
  }

  // Check if changes are needed
  if (response.status === 'no_changes_needed' || !response.comments || response.comments.length === 0) {
    console.log(`File ${filePath} is already structured correctly. Updating metadata.`);
    await updateFileWithHash(filePath, body, frontmatter, 'lastStructureCheckHash');
    return;
  }

  // Insert comments into the body
  const bodyLines = body.split('\n');
  const insertedComments: string[] = [];

  // Sort comments by line number (descending) to avoid line number shifts
  const sortedComments = [...response.comments].sort((a, b) => b.afterLine - a.afterLine);

  for (const comment of sortedComments) {
    // Validate line number
    if (comment.afterLine < 0 || comment.afterLine > bodyLines.length) {
      console.warn(`⚠ Skipping comment at invalid line ${comment.afterLine} (file has ${bodyLines.length} lines)`);
      continue;
    }

    // Optional: Validate context if provided
    if (comment.context && comment.afterLine > 0) {
      const lineContent = bodyLines[comment.afterLine - 1]; // afterLine is 1-indexed
      if (!lineContent.includes(comment.context)) {
        console.warn(`⚠ Context mismatch at line ${comment.afterLine}. Expected: "${comment.context}"`);
        console.warn(`   Actual line: "${lineContent.substring(0, 100)}..."`);
        // Continue anyway, but log the warning
      }
    }

    // Format the TODO comment
    const todoComment = `<!-- TODO: STRUCTURE (${comment.type}) - ${comment.message} -->`;

    // Insert after the specified line
    bodyLines.splice(comment.afterLine, 0, todoComment);
    insertedComments.push(`Line ${comment.afterLine}: ${comment.type} - ${comment.message.substring(0, 60)}...`);
  }

  console.log(`✓ Inserted ${insertedComments.length} structure comments:`);
  insertedComments.forEach(c => console.log(`  ${c}`));

  // Update the file with modified body
  const finalBody = bodyLines.join('\n');
  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastStructureCheckHash');
  console.log(`Successfully checked structure for ${filePath}.`);
}

export async function linkCheckFile(filePath: string): Promise<void> {
  console.log(`\nChecking links in ${filePath}...`);
  let { frontmatter, body } = await readFileWithMatter(filePath);

  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let newBody = body;
  let issuesFound = false;

  const matches = Array.from(body.matchAll(linkRegex));

  for (const match of matches) {
    const fullMatch = match[0];
    const link = match[2];

    if (link.startsWith('http') || link.startsWith('https') || !link) {
      continue;
    }

    const [linkPath, anchor] = link.split('#');
    const absolutePath = path.resolve(path.dirname(filePath), linkPath);
    let issueDescription = '';

    try {
      await fs.access(absolutePath);
      if (anchor) {
        const targetContent = await fs.readFile(absolutePath, 'utf-8');
        if (!targetContent.includes(`id="${anchor}"`)) {
          issueDescription = `Broken anchor: #${anchor} not found in ${linkPath}`;
        }
      }
    } catch (error) {
      issueDescription = `Broken link: ${linkPath} not found.`;
    }

    if (issueDescription) {
      issuesFound = true;
      const todoComment = `<!-- TODO: LINK_CHECK - ${issueDescription} -->`;
      if (!newBody.includes(todoComment)) {
        newBody = newBody.replace(fullMatch, `${todoComment}\n${fullMatch}`);
      }
    }
  }

  if (issuesFound) {
    console.warn(`WARNING: Found and marked broken links in ${filePath}.`);
    body = newBody;
  } else {
    console.log(`No broken links found in ${filePath}.`);
  }

  await updateFileWithHash(filePath, body, frontmatter, 'lastLinkCheckHash');
  console.log(`Successfully updated link-check metadata for ${filePath}.`);
}

export async function figureCheckFile(filePath: string): Promise<void> {
  console.log(`\nChecking figures and design elements in ${filePath}...`);
  let { frontmatter, body } = await readFileWithMatter(filePath);
  let newBody = body;
  let issuesFound = false;

  const includeRegex = /{{<\s*include\s+([^>]+)\s*>}}/g;
  const includeMatches = Array.from(body.matchAll(includeRegex));
  for (const match of includeMatches) {
    const fullMatch = match[0];
    const includedPath = match[1].trim();
    if (includedPath.startsWith('brain/figures')) {
      const chartFilePath = path.resolve(includedPath);
      try {
        const chartContent = await fs.readFile(chartFilePath, 'utf-8');
        const violations = [];
        if (chartContent.includes('plt.tight_layout()')) {
          violations.push(`Use of 'plt.tight_layout()' is discouraged.`);
        }
        if (!chartContent.includes('setup_chart_style()')) {
          violations.push(`Missing 'setup_chart_style()'.`);
        }
        if (!chartContent.includes('add_watermark()')) {
          violations.push(`Missing 'add_watermark()'.`);
        }
        if (violations.length > 0) {
          issuesFound = true;
          const todoComment = `<!-- TODO: FIGURE_CHECK - Design violations in ${includedPath}: ${violations.join(' ')} -->`;
          if (!newBody.includes(todoComment)) {
            newBody = newBody.replace(fullMatch, `${todoComment}\n${fullMatch}`);
          }
        }
      } catch (error) {
        // This case is handled by the link checker
      }
    }
  }

  const imageRegex = /!\[[^\]]*\]\(([^)]+)\)/g;
  const imageMatches = Array.from(body.matchAll(imageRegex));
  for (const match of imageMatches) {
    const fullMatch = match[0];
    const imagePath = match[1];
    if (!imagePath.startsWith('http') && !imagePath.includes('assets/')) {
      issuesFound = true;
      const todoComment = `<!-- TODO: FIGURE_CHECK - Static image '${imagePath}' should be in the 'assets/' directory. -->`;
      if (!newBody.includes(todoComment)) {
        newBody = newBody.replace(fullMatch, `${todoComment}\n${fullMatch}`);
      }
    }
  }

  if (issuesFound) {
    console.warn(`WARNING: Found and marked design guide violations in ${filePath}.`);
    body = newBody;
  } else {
    console.log(`No design guide violations found in ${filePath}.`);
  }

  await updateFileWithHash(filePath, body, frontmatter, 'lastFigureCheckHash');
  console.log(`Successfully updated figure-check metadata for ${filePath}.`);
}

async function mergeContentWithLLM(archivedContent: string, targetFilePath: string): Promise<string> {
  console.log(`Intelligently merging content into ${targetFilePath}...`);
  const targetContent = await fs.readFile(targetFilePath, 'utf-8');
  const styleGuide = await fs.readFile('GUIDES/STYLE_GUIDE.md', 'utf-8');

  const { content: archivedBody } = matter(archivedContent);
  const { data: targetFrontmatter, content: targetBody } = matter(targetContent);

  let prompt = await fs.readFile('scripts/prompts/content-merger.md', 'utf-8');
  prompt = prompt.replace('{{styleGuide}}', styleGuide)
                 .replace('{{targetFilePath}}', targetFilePath)
                 .replace('{{targetBody}}', targetBody)
                 .replace('{{archivedBody}}', archivedBody);

  const mergedBody = await generateGeminiProContent(prompt);
  
  const finalContent = matter.stringify(mergedBody, targetFrontmatter);
  return finalContent;
}

export async function analyzeArchivedFile(filePath: string): Promise<void> {
  console.log(`Analyzing archived file: ${filePath}`);
  const archivedContent = await fs.readFile(filePath, 'utf-8');
  const quartoYmlContent = await fs.readFile('_quarto.yml', 'utf-8');
  const bookOutline = await fs.readFile('OUTLINE.MD', 'utf-8');

  let prompt = await fs.readFile('scripts/prompts/archive-analysis.md', 'utf-8');
  prompt = prompt.replace('{{quartoYmlContent}}', quartoYmlContent)
                 .replace('{{bookOutline}}', bookOutline)
                 .replace('{{filePath}}', filePath)
                 .replace('{{archivedContent}}', archivedContent);

  const responseText = await generateGeminiProContent(prompt);
  const jsonMatch = responseText.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error(`No JSON object found in LLM response. Response text: ${responseText}`);
  }
  // Sanitize the JSON string by removing newline and carriage return characters
  // which can cause parsing errors if they are not properly escaped in the LLM response.
  const sanitizedJsonString = jsonMatch[0].replace(/[\r\n]/g, "");
  const response = JSON.parse(sanitizedJsonString);

  switch (response.action) {
    case 'MERGE':
      if (!response.targetFile) {
        throw new Error('Invalid MERGE action: targetFile is required.');
      }
      console.log(`Decision: MERGE into ${response.targetFile}. Reason: ${response.reason}`);
      const finalContent = await mergeContentWithLLM(archivedContent, response.targetFile);
      await saveFile(response.targetFile, finalContent);
      // await fs.unlink(filePath);
      console.log(`Successfully merged content into ${response.targetFile}.`);
      break;

    case 'CREATE':
      if (!response.newFilePath || !response.newFileContent) {
        throw new Error('Invalid CREATE action: newFilePath and newFileContent are required.');
      }
      const newFilePath = response.newFilePath;
      console.log(`Decision: CREATE new file ${newFilePath}. Reason: ${response.reason}`);
      await saveFile(newFilePath, response.newFileContent);
      console.log(`TODO: Manually add ${newFilePath} to _quarto.yml`);
      // await fs.unlink(filePath);
      console.log(`Successfully created ${newFilePath}.`);
      break;

    case 'MOVE_TO_OPS':
      if (!response.newFilePath || !response.newFileContent) {
        throw new Error('Invalid MOVE_TO_OPS action: newFilePath and newFileContent are required.');
      }
      const opsFilePath = response.newFilePath;
      console.log(`Decision: MOVE to ${opsFilePath}. Reason: ${response.reason}`);
      await saveFile(opsFilePath, response.newFileContent);
      // await fs.unlink(filePath);
      console.log(`Successfully moved file to ${opsFilePath}.`);
      break;

    case 'DELETE':
      console.log(`Decision: DELETE file. Reason: ${response.reason}`);
      // await fs.unlink(filePath);
      console.log(`File would be deleted (deletion disabled for safety).`);
      break;

    default:
      throw new Error(`Unknown action: ${response.action}`);
  }
}

export async function latexCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nChecking for LaTeX usage in ${filePath} with Gemini...`);
  let { frontmatter, body } = await readFileWithMatter(filePath);

  const prompt = await loadPromptTemplate('scripts/prompts/latex-check.md', {
    '{{body}}': body
  });

  const responseText = await generateGeminiProContent(prompt);

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} already uses LaTeX correctly. Updating metadata.`);
    finalBody = body;
  } else {
    finalBody = responseText.trim();
  }

  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastLatexCheckHash');
  console.log(`Successfully checked LaTeX usage for ${filePath}.`);
}

export async function generateFigureForChapter(filePath: string): Promise<{ action: 'create' | 'include' | 'none', filename?: string, code?: string, insertion_paragraph?: string }> {
  console.log(`\nAnalyzing chapter ${filePath} for potential figures...`);
  const chapterContent = await fs.readFile(filePath, 'utf-8');
  const { content: chapterBody } = matter(chapterContent);

  // Get list of existing figures
  const figureFiles = await glob('brain/figures/**/*.qmd');
  const existingFigures = figureFiles.join('\n');

  // Get Design Guide and Example File Content
  const designGuide = await fs.readFile('GUIDES/DESIGN_GUIDE.md', 'utf-8');
  
  let prompt = await fs.readFile('scripts/prompts/figure-generator-prompt.md', 'utf-8');
  
  // Inject the design guide
  prompt = prompt.replace('... [The full design guide content as provided previously] ...', designGuide);

  // The prompt now has placeholders for multiple examples, so we don't need to load them here.
  // The LLM will use the examples hardcoded in the prompt file.

  prompt = prompt
    .replace('{{existing_figures}}', existingFigures)
    .replace('{{chapter_content}}', chapterBody);

  const responseText = await generateGeminiProContent(prompt);

  if (responseText.trim() === 'NO_ACTION_NEEDED') {
    console.log(`No new figure needed for ${filePath}.`);
    return { action: 'none' };
  }

  // More robustly find the JSON object, even with leading text and markdown fences.
  const jsonStart = responseText.indexOf('{');
  const jsonEnd = responseText.lastIndexOf('}');

  if (jsonStart === -1 || jsonEnd === -1 || jsonEnd < jsonStart) {
    console.error(`No valid JSON object found in LLM response for ${filePath}.`);
    console.error("Raw response:", responseText);
    throw new Error(`No valid JSON object found in LLM response for ${filePath}.`);
  }

  const jsonString = responseText.substring(jsonStart, jsonEnd + 1);
  const responseJson = JSON.parse(jsonString);

  if (responseJson.existing_figure) {
    console.log(`Found existing figure for ${filePath}: ${responseJson.existing_figure}`);
    return { action: 'include', filename: responseJson.existing_figure };
  }
  if (responseJson.filename && responseJson.code && responseJson.insertion_paragraph) {
    console.log(`Generated new figure for ${filePath}: ${responseJson.filename}`);
    return { 
      action: 'create', 
      filename: responseJson.filename, 
      code: responseJson.code,
      insertion_paragraph: responseJson.insertion_paragraph
    };
  }

  return { action: 'none' };
}

/**
 * Validates inline Python code replacements for common syntax errors
 */
function validatePythonReplacement(replacement: string): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Check for escaped backticks
  if (replacement.includes('\\`')) {
    errors.push('Contains escaped backtick (\\`) - backticks should never be escaped');
  }

  // Check for extra closing brace after closing paren: )}` pattern
  if (/\)}`/.test(replacement)) {
    errors.push('Contains extra closing brace after paren: )}`  - should be )`');
  }

  // Check for double closing parens: ))` pattern
  if (/\)\)`/.test(replacement)) {
    errors.push('Contains double closing parens: ))`  - should be )`');
  }

  // Check for format specs without f-string: {python} VAR:,.0f} pattern
  if (/`\{python\}\s+[A-Z_]+:[,.\d]+[fde].*?`/.test(replacement) && !replacement.includes('f"')) {
    errors.push('Format specifier without f-string - use f"{VAR:,.0f}" not VAR:,.0f}');
  }

  return { valid: errors.length === 0, errors };
}

export async function parameterizeFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nChecking for hardcoded numbers in ${filePath} with Gemini...`);
  let { frontmatter, body } = await readFileWithMatter(filePath);

  const parametersFile = await fs.readFile('brain/book/appendix/economic_parameters.py', 'utf-8');
  const exampleFile = await fs.readFile('index.qmd', 'utf-8');

  const prompt = await loadPromptTemplate('scripts/prompts/parameterizer.md', {
    '{{parametersFile}}': parametersFile,
    '{{exampleFile}}': exampleFile,
    '{{body}}': body
  });

  const responseText = await generateGeminiFlashContent(prompt);

  let result;
  try {
    result = extractJsonFromResponse(responseText, `parameterization response for ${filePath}`);
  } catch (error) {
    console.error(`❌ ERROR:`, error);
    return;
  }

  if (result.status === 'NO_CHANGES_NEEDED') {
    console.log(`No parameterization needed for ${filePath}.`);
  } else {
    let updatedBody = body;
    if (result.chapterReplacements && result.chapterReplacements.length > 0) {
      // Validate all replacements first
      const validationErrors: string[] = [];
      for (let i = 0; i < result.chapterReplacements.length; i++) {
        const replacement = result.chapterReplacements[i];
        const validation = validatePythonReplacement(replacement.replace);
        if (!validation.valid) {
          validationErrors.push(`\n  Replacement ${i + 1}: "${replacement.replace}"`);
          validation.errors.forEach(err => validationErrors.push(`    - ${err}`));
        }
      }

      if (validationErrors.length > 0) {
        console.error(`❌ VALIDATION FAILED for ${filePath}:`);
        console.error(validationErrors.join('\n'));
        console.error(`\n⚠️  Skipping parameterization to prevent syntax errors.`);
        return;
      }

      // All validations passed, apply replacements
      for (const replacement of result.chapterReplacements) {
        updatedBody = updatedBody.replace(replacement.find, replacement.replace);
      }
      const newContent = matter.stringify(updatedBody, frontmatter);
      await saveFile(filePath, newContent);
      console.log(`✓ Successfully parameterized ${filePath}.`);
      body = updatedBody; // Update body for hash calculation
    }
    if (result.newParameterCode) {
      await fs.appendFile('brain/book/appendix/economic_parameters.py', '\n' + result.newParameterCode);
      console.log(`✓ Successfully updated economic_parameters.py.`);
    }
  }

  // Update hash to prevent re-running
  await updateFileWithHash(filePath, body, frontmatter, 'lastParamCheckHash');
}
