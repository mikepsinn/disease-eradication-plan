import fs from 'fs/promises';
import matter from 'gray-matter';
import { simpleGit } from 'simple-git';
import { glob } from 'glob';
import crypto from 'crypto';
import ignore from 'ignore';
import path from 'path';
import { generateGeminiContent, generateClaudeContent } from '../lib/llm';
import { saveFile, programmaticFormat } from '../lib/file-utils';

const git = simpleGit();

function getBodyHash(content: string): string {
  const { content: body } = matter(content);
  return crypto.createHash('sha256').update(body).digest('hex');
}

async function updateFileWithHash(
  filePath: string,
  body: string,
  frontmatter: any,
  hashFieldName: string
): Promise<void> {
  const tempContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  frontmatter[hashFieldName] = getBodyHash(tempContent);
  const newContent = matter.stringify(body, frontmatter, { lineWidth: -1 } as any);
  await saveFile(filePath, newContent);
}

export interface BookStructure {
  chapters: string[];
  appendices: string[];
}

export async function parseQuartoYml(): Promise<BookStructure> {
  const quartoYmlContent = await fs.readFile('_quarto.yml', 'utf-8');
  const chapters: string[] = [];
  const appendices: string[] = [];

  const lines = quartoYmlContent.split('\n');
  let inAppendices = false;
  let inChapters = false;

  for (const line of lines) {
    // Only recognize top-level (2-space indentation) chapters: and appendices:
    // This prevents nested chapters: inside appendices from switching modes
    const trimmedLine = line.trimStart();
    const indentLevel = line.length - trimmedLine.length;

    // Top-level book.chapters: has 2 spaces of indentation
    if (trimmedLine === 'chapters:' && indentLevel === 2) {
      inChapters = true;
      inAppendices = false;
      continue;
    }

    // Top-level book.appendices: has 2 spaces of indentation
    if (trimmedLine === 'appendices:' && indentLevel === 2) {
      inAppendices = true;
      inChapters = false;
      continue;
    }

    // Reset when we hit a top-level key (no indentation)
    if (!line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      inChapters = false;
      inAppendices = false;
    }

    const match = line.match(/^\s*-\s+(brain\/[^\s]+\.qmd)/);
    if (match) {
      if (inAppendices) {
        appendices.push(match[1]);
      } else if (inChapters) {
        chapters.push(match[1]);
      }
    }
  }

  return { chapters, appendices };
}

export async function getStaleFiles(hashFieldName: string, basePath?: string): Promise<string[]> {
  const gitignoreContent = await fs.readFile('.gitignore', 'utf-8');
  const ig = ignore().add(gitignoreContent);

  const searchPattern = basePath ? `${basePath}/**/*.qmd` : '**/*.qmd';
  const allQmdFiles = glob.sync(searchPattern, { ignore: 'node_modules/**' });
  const qmdFiles = ig.filter(allQmdFiles);
  
  const staleFiles: string[] = [];

  for (const file of qmdFiles) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data: frontmatter } = matter(content);

      const lastHash = frontmatter[hashFieldName];
      const currentBodyHash = getBodyHash(content);

      if (currentBodyHash !== lastHash) {
        staleFiles.push(file);
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }

  return staleFiles;
}

export async function formatFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nFormatting ${filePath} with Gemini...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const formattingGuide = await fs.readFile('GUIDES/FORMATTING_GUIDE.md', 'utf-8');
  let prompt = await fs.readFile('scripts/prompts/formatter.md', 'utf-8');
  prompt = prompt.replace('{{formattingGuide}}', formattingGuide).replace('{{body}}', body);

  const responseText = await generateGeminiContent(prompt);

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
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(originalContent);

  const styleGuide = await fs.readFile('GUIDES/STYLE_GUIDE.md', 'utf-8');
  let prompt = await fs.readFile('scripts/prompts/style-guide-review.md', 'utf-8');
  prompt = prompt.replace('{{styleGuide}}', styleGuide).replace('{{body}}', body);

  const responseText = await generateClaudeContent(prompt);

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

interface Reference {
  id: string;
  title: string;
  quotes: string[];
  source: string;
}

function parseReferences(referencesContent: string): Reference[] {
  const references: Reference[] = [];
  const anchorRegex = /<a\s+id="([^"]+)"><\/a>/g;
  const blocks: Array<{ id: string; content: string }> = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = anchorRegex.exec(referencesContent)) !== null) {
    if (blocks.length > 0) {
      blocks[blocks.length - 1].content = referencesContent.substring(lastIndex, match.index);
    }
    blocks.push({ id: match[1], content: '' });
    lastIndex = match.index + match[0].length;
  }

  if (blocks.length > 0) {
    blocks[blocks.length - 1].content = referencesContent.substring(lastIndex);
  }

  for (const block of blocks) {
    const lines = block.content.trim().split('\n');
    if (lines.length === 0) continue;

    const titleMatch = lines[0].match(/^-\s+\*\*(.+)\*\*$/);
    if (!titleMatch) {
      console.warn(`⚠ No title found for reference ${block.id}`);
      continue;
    }

    const title = titleMatch[1];
    const quotes: string[] = [];
    let source = '';
    let currentQuote = '';

    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) {
        if (currentQuote) {
          quotes.push(currentQuote.trim());
          currentQuote = '';
        }
        continue;
      }
      if (line.startsWith('>')) {
        const content = line.substring(1).trim();
        if (content.startsWith('—')) {
          if (currentQuote) {
            quotes.push(currentQuote.trim());
            currentQuote = '';
          }
          const newSource = content.substring(1).trim();
          if (source && source !== newSource) {
            source += ' | ' + newSource;
          } else if (!source) {
            source = newSource;
          }
        } else {
          if (currentQuote) {
            currentQuote += '\n' + content;
          } else {
            currentQuote = content;
          }
        }
      } else if (currentQuote && !line.startsWith('<') && !line.startsWith('-')) {
        currentQuote += '\n' + line;
      }
    }
    if (currentQuote) {
      quotes.push(currentQuote.trim());
    }
    references.push({
      id: block.id,
      title,
      quotes,
      source: source || '<!-- TODO: Add source URL -->'
    });
  }

  const seenIds = new Map<string, number>();
  const uniqueRefs: Reference[] = [];
  for (const ref of references) {
    if (seenIds.has(ref.id)) {
      console.warn(`⚠ Duplicate reference ID "${ref.id}" - merging`);
      const existingIndex = seenIds.get(ref.id)!;
      const existing = uniqueRefs[existingIndex];
      existing.quotes.push(...ref.quotes);
      if (ref.source && ref.source !== existing.source) {
        existing.source += ' | ' + ref.source;
      }
    } else {
      seenIds.set(ref.id, uniqueRefs.length);
      uniqueRefs.push(ref);
    }
  }
  return uniqueRefs;
}

function formatReferencesFile(references: Reference[], frontmatter: string): string {
  const sorted = references.sort((a, b) => a.id.localeCompare(b.id));
  let output = frontmatter + '\n\n';
  for (const ref of sorted) {
    output += `<a id="${ref.id}"></a>\n`;
    output += `- **${ref.title}**\n`;
    for (const quote of ref.quotes) {
      const quoteLines = quote.split('\n');
      for (const line of quoteLines) {
        output += `  > ${line}\n`;
      }
    }
    output += `  > — ${ref.source}\n\n`;
  }
  return output.trimEnd() + '\n';
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
    const responseText = await generateGeminiContent(prompt);
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON object found in response');
    }
    const resultData = JSON.parse(jsonMatch[0]);

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

export async function structureCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nChecking structure of ${filePath} with Gemini...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

  const outlineContent = await fs.readFile('OUTLINE.md', 'utf-8');
  const { chapters, appendices } = await parseQuartoYml();

  if (appendices.includes(filePath)) {
    console.log(`File ${filePath} is already in appendix. Skipping structure check.`);
    return;
  }

  const otherChapters = chapters.filter(ch => ch !== filePath);

  let prompt = await fs.readFile('scripts/prompts/structure-check.md', 'utf-8');
  prompt = prompt.replace('{{outlineContent}}', outlineContent)
                 .replace('{{otherChapters}}', otherChapters.join('\n'))
                 .replace('{{filePath}}', filePath)
                 .replace('{{body}}', body);

  const responseText = await generateGeminiContent(prompt);

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} is already structured correctly. Updating metadata.`);
    finalBody = body;
  } else {
    const trimmedResponse = responseText.trim();
    const originalLength = body.length;
    const responseLength = trimmedResponse.length;

    // Safety check: reject if response is >50% shorter (likely LLM deleted content)
    if (responseLength < originalLength * 0.5) {
      console.error(`❌ ERROR: LLM response is ${Math.round((1 - responseLength/originalLength) * 100)}% shorter than original!`);
      console.error(`   Original: ${originalLength} chars, Response: ${responseLength} chars`);
      console.error(`   This suggests the LLM deleted content instead of adding TODO comments.`);
      console.error(`   SKIPPING this file to prevent data loss.`);
      return; // Don't update the file
    }

    finalBody = trimmedResponse;
  }

  await updateFileWithHash(filePath, finalBody, frontmatter, 'lastStructureCheckHash');
  console.log(`Successfully checked structure for ${filePath}.`);
}

export async function linkCheckFile(filePath: string): Promise<void> {
  console.log(`\nChecking links in ${filePath}...`);
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

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
  let originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);
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

  const mergedBody = await generateGeminiContent(prompt);
  
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

  const responseText = await generateGeminiContent(prompt);
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
      await fs.unlink(filePath);
      console.log(`Successfully merged content into ${response.targetFile} and deleted archived file.`);
      break;

    case 'CREATE':
      if (!response.newFilePath || !response.newFileContent) {
        throw new Error('Invalid CREATE action: newFilePath and newFileContent are required.');
      }
      const newFilePath = response.newFilePath;
      console.log(`Decision: CREATE new file ${newFilePath}. Reason: ${response.reason}`);
      await saveFile(newFilePath, response.newFileContent);
      console.log(`TODO: Manually add ${newFilePath} to _quarto.yml`);
      await fs.unlink(filePath);
      console.log(`Successfully created ${newFilePath} and deleted archived file.`);
      break;

    case 'MOVE_TO_OPS':
      if (!response.newFilePath || !response.newFileContent) {
        throw new Error('Invalid MOVE_TO_OPS action: newFilePath and newFileContent are required.');
      }
      const opsFilePath = response.newFilePath;
      console.log(`Decision: MOVE to ${opsFilePath}. Reason: ${response.reason}`);
      await saveFile(opsFilePath, response.newFileContent);
      await fs.unlink(filePath);
      console.log(`Successfully moved file to ${opsFilePath} and deleted archived file.`);
      break;

    case 'DELETE':
      console.log(`Decision: DELETE file. Reason: ${response.reason}`);
      await fs.unlink(filePath);
      console.log(`Successfully deleted archived file.`);
      break;

    default:
      throw new Error(`Unknown action: ${response.action}`);
  }
}

export async function latexCheckFileWithLLM(filePath: string): Promise<void> {
  console.log(`\nChecking for LaTeX usage in ${filePath} with Gemini...`);
  const originalContent = await fs.readFile(filePath, 'utf-8');
  let { data: frontmatter, content: body } = matter(originalContent);

  let prompt = await fs.readFile('scripts/prompts/latex-check.md', 'utf-8');
  prompt = prompt.replace('{{body}}', body);

  const responseText = await generateGeminiContent(prompt);

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

  const responseText = await generateGeminiContent(prompt);

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
